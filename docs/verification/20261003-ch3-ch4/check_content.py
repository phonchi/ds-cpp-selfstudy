"""Compile the new teaching examples and check bounded chapter generation."""
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).parent
HEADERS=Path('/home/phonchi/ds_cpp/Slides')
sys.path.insert(0,str(ROOT/'tools/enrich'))
from content.linked_depth import EXAMPLES
report=[]
with tempfile.TemporaryDirectory(prefix='chapters-cpp-') as tmp:
 for page in ['arrays','linked_lists']:
  soup=BeautifulSoup((ROOT/(page+'.html')).read_text(),'html.parser')
  ids=[e['id'] for e in soup.select('[id]')]
  assert len(ids)==len(set(ids)), (page,'duplicate id')
  for a in soup.select('a[href^="#"]'):
   assert a['href'][1:] in ids,(page,a['href'])
  examples=[]
  if page=='arrays':
   for i,el in enumerate(soup.select('[data-cpp]')):
    if el['data-cpp'] in ['run','compile-error']:
     src='\n'.join(x.get_text() for x in el.select('.line'))
     examples.append((f'arrays-{i}',src,el.get('data-expected'),el['data-cpp']))
  else:
   for i,card in enumerate(soup.select('.deck-extra')):
    block=card.select_one('.pseudo-code');expected=card.select_one('.expected-out pre')
    if block and expected:
     src='\n'.join(x.get_text() for x in block.select('.line'))
     if re.search(r'int\s+main\s*\(',src):
      examples.append((f'linked-{i}',src,expected.get_text()+'\n','run'))
  for name,src,expected,kind in examples:
   path=Path(tmp)/(name+'.cpp');exe=Path(tmp)/name;path.write_text(src)
   cmd=['g++','-std=c++17','-Wall','-Wextra','-pedantic','-I'+str(HEADERS),str(path),'-o',str(exe)]
   c=subprocess.run(cmd,text=True,capture_output=True)
   if kind=='compile-error':
    assert c.returncode!=0,(name,'must fail to compile')
   else:
    assert c.returncode==0,(name,c.stderr)
    run=subprocess.run([str(exe)],text=True,capture_output=True,timeout=10)
    assert run.returncode==0,(name,run.stderr)
    assert run.stdout==expected,(name,repr(run.stdout),repr(expected))
   report.append({'example':name,'kind':kind,'passed':True})
  before=(ROOT/(page+'.html')).read_bytes()
  script='enrich_arrays.py' if page=='arrays' else 'enrich_linked.py'
  subprocess.run([sys.executable,str(ROOT/'tools/enrich'/script)],check=True,capture_output=True)
  assert before==(ROOT/(page+'.html')).read_bytes(),(page,'generator not idempotent')
  for i,script in enumerate(soup.select('script:not([src])')):
   path=Path(tmp)/(page+str(i)+'.js');path.write_text(script.string or script.get_text())
   js=subprocess.run(['node','--check',str(path)],capture_output=True,text=True)
   assert js.returncode==0,js.stderr
(OUT/'content-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'{len(report)} examples passed; both generators stable; IDs, anchors and JS syntax passed')
