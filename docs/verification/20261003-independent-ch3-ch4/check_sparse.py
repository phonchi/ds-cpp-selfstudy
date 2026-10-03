"""Dense-oracle checks of the actual three self-contained teaching programs."""
import importlib.util,subprocess,tempfile,re,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).parent
spec=importlib.util.spec_from_file_location('sparse_examples',ROOT/'tools/enrich/content/sparse_examples.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
cases=[([[0,2,0],[3,0,0],[0,0,4]],[[5,0,0],[0,6,0],[0,0,7]]),([[0,0],[0,0]],[[1,2],[3,4]]),([[1,2],[3,4]],[[0,0],[0,0]]),([[1,2],[3,4]],[[-1,-2],[-3,-4]]),([[1,0],[0,0]],[[0,0],[0,2]]),([[1,2],[3,4]],[[5,6],[7,8]]),([[1,1]],[[1],[-1]]),([[1,0,2],[0,3,4]],[[2,0],[0,1],[5,6]])]
report=[]
with tempfile.TemporaryDirectory() as tmp:
 for name,(code,_) in mod.EXAMPLES.items():
  setup=[];expected=[]
  for A,B in cases:
   cls={'coo':'COO','dok':'SparseMatrix','linear':'Linear'}[name]
   setup.append('{')
   for var,M in [('a',A),('b',B)]:
    setup.append(f'{cls} {var};' if name=='dok' else f'{cls} {var}({len(M)},{len(M[0])});')
    for i,row in enumerate(M):
     for j,v in enumerate(row):
      if v:setup.append(f'{var}({i},{j})={v};' if name=='dok' else f'{var}.append({i},{j},{v});')
   operations=['*']
   if len(A)==len(B) and len(A[0])==len(B[0]):operations=['+','-','*']
   for op in operations:
    setup.append(f'std::cout << (a {op} b) << "\\n";' if name=='dok' else f'(a {op} b).print();')
    if op=='*':result=[[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
    else:result=[[A[i][j]+(1 if op=='+' else -1)*B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    expected.append({(i,j):v for i,row in enumerate(result) for j,v in enumerate(row) if v})
   setup.append('}')
  source=code[:code.rindex('int main()')]+ 'int main(){\n'+'\n'.join(setup)+'\n}\n'
  path=Path(tmp)/(name+'.cpp');exe=Path(tmp)/name;path.write_text(source)
  subprocess.run(['g++','-std=c++17','-Wall','-Wextra','-pedantic','-fno-elide-constructors',str(path),'-o',str(exe)],check=True)
  proc=subprocess.run([str(exe)],capture_output=True,text=True,check=True);(OUT/(name+'-oracle-output.txt')).write_text(proc.stdout)
  lines=proc.stdout.splitlines();assert len(lines)==len(expected)
  for line,want in zip(lines,expected):
   items=re.findall(r'\((\d+),\s*(\d+)\):\s*(-?[\d.]+)',line)
   actual={(int(i),int(j)):float(v) for i,j,v in items if float(v)!=0}
   assert actual==want,(name,actual,want)
  report.append({'format':name,'cases':len(cases),'results':len(expected),'passed':True})
(OUT/'sparse-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(report)
