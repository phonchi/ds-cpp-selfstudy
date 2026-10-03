"""MathJax markup for chapter prose; preserve C++/JS and existing HTML verbatim."""
from html.parser import HTMLParser
from html import escape
from pathlib import Path
import re

FORMULAS = {
    'offset = i × Cols + j': r'$\mathrm{offset}=i\times\mathrm{Cols}+j$',
    'offset = j × Rows + i': r'$\mathrm{offset}=j\times\mathrm{Rows}+i$',
    'B + (i × Cols + j) × s': r'$B+(i\times\mathrm{Cols}+j)\times s$',
    'B + (j × Rows + i) × s': r'$B+(j\times\mathrm{Rows}+i)\times s$',
    '(1 + 2 + … + n) / n = (n + 1) / 2': r'$\frac{1+2+\cdots+n}{n}=\frac{n+1}{2}$',
    '1−a/(rows×cols)': r'$1-\frac{a}{\mathrm{rows}\times\mathrm{cols}}$',
    'n−1−i': r'$n-1-i$',
    'n−i': r'$n-i$',
    'log₂n': r'$\log_2 n$',
}

# Explicit algebra keeps programming notation (pointers, assignments, paths) intact.
FORMULAS.update({
    's = sizeof(T)': r'$s=\operatorname{sizeof}(T)$',
    'Cols × sizeof(T)': r'$\mathrm{Cols}\times\operatorname{sizeof}(T)$',
    'Cols×sizeof(int)': r'$\mathrm{Cols}\times\operatorname{sizeof}(\mathrm{int})$',
    'Rows×Cols': r'$\mathrm{Rows}\times\mathrm{Cols}$',
    'B＝diag(5,6,7)': r'$B=\operatorname{diag}(5,6,7)$',
    'B = 1000': r'$B=1000$',
    'base = 2000': r'$\mathrm{base}=2000$',
    'base=1000': r'$\mathrm{base}=1000$',
    'int=4B': r'$\operatorname{sizeof}(\mathrm{int})=4\,\mathrm{B}$',
    'A(i,k)': r'$A(i,k)$', 'B(l,j)': r'$B(l,j)$',
    'A+B': r'$A+B$', 'A−B': r'$A-B$', 'A×B': r'$A\times B$',
    'k=l': r'$k=l$', 'i=n': r'$i=n$', 'i<n': r'$i\lt n$',
    'n−1': r'$n-1$', 'n²': r'$n^2$', 'n log n': r'$n\log n$',
    '2n': r'$2n$',
    'sizeof(double)=8': r'$\operatorname{sizeof}(\mathrm{double})=8$',
    'i×欄數(4)+j': r'$i\times4+j$', '+j = 2': r'$+j=2$',
    'y = x + (Cols×i + j)×sizeof = 0 + (4×7 + 2)×1 = 30':
        r'$$\begin{aligned}y&=x+(\mathrm{Cols}\times i+j)\times s\\&=0+(4\times7+2)\times1\\&=30\end{aligned}$$',
    '10¹⁰ × 4B = 40GB': r'$10^{10}\times4\,\mathrm{B}=40\,\mathrm{GB}$',
    'offset = j * Rows + i': r'$\mathrm{offset}=j\times\mathrm{Rows}+i$',
})

INLINE_MATH = {
    'cur-&gt;getData() ≥ item': r'<code>cur-&gt;getData()</code> $\ge\mathrm{item}$',
    '0 ≤ i &lt; n': r'$0\le i\lt n$',
    '0 ≤ lastIndex ≤ maxSize': r'$0\le\mathrm{lastIndex}\le\mathrm{maxSize}$',
    'base + i × sizeof(T)': r'$\mathrm{base}+i\times\operatorname{sizeof}(T)$',
    '6 * sizeof(double)': r'$6\times\operatorname{sizeof}(\mathrm{double})$',
    'n * sizeof(int)': r'$n\times\operatorname{sizeof}(\mathrm{int})$',
    'n * sizeof(int*)': r'$n\times\operatorname{sizeof}(\mathrm{int*})$',
    '1+2+4+…': r'$1+2+4+\cdots$',
}

def outside_math(text, transform):
    parts=re.split(r'(\$\$.*?\$\$|\$[^$]*\$)',text,flags=re.S)
    return ''.join(p if p.startswith('$') else transform(p) for p in parts)

def math_text(text):
    keys=re.compile('|'.join(re.escape(k) for k in sorted(FORMULAS,key=len,reverse=True)))
    def bigo(match):
        expr=match[0].replace('²','^2').replace('³','^3').replace('×',r'\times ')
        expr=re.sub(r'\blog\b',lambda _:r'\log ',expr)
        for name in ['capacity','Rows','Cols','nnz']:
            expr=re.sub(r'\b'+name+r'\b',lambda m:r'\mathrm{'+m[0]+'}',expr)
        return '$'+expr+'$'
    pattern=r'\bO\((?:[^()\n]|\((?:[^()\n]|\([^()\n]*\))*\))*\)'
    # Process O(...) before its subexpressions to avoid nested delimiters.
    text=outside_math(text,lambda s:re.sub(pattern,bigo,s))
    text=outside_math(text,lambda s:keys.sub(lambda m:FORMULAS[m[0]],s))
    text=outside_math(text,lambda s:re.sub(r'\bn\s*/\s*2\b',lambda _:r'$\frac{n}{2}$',s))
    supers=str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹','0123456789')
    atom=r'\d+(?:[⁰¹²³⁴⁵⁶⁷⁸⁹]+)?'
    term=rf'(?:{atom}|\(\s*{atom}(?:\s*[×+＝=]\s*{atom})+\s*\))'
    numeric=rf'(?<![\w]){term}(?:\s*[×+＝=]\s*{term})+'
    def numbers(m):
        expr=re.sub(r'([⁰¹²³⁴⁵⁶⁷⁸⁹]+)',lambda x:'^{'+x[0].translate(supers)+'}',m[0])
        return '$'+expr.replace('×',r'\times ').replace('＝','=')+'$'
    text=outside_math(text,lambda s:re.sub(numeric,numbers,s))
    text=outside_math(text,lambda s:re.sub(r'\d+[⁰¹²³⁴⁵⁶⁷⁸⁹]+',numbers,s))
    return text

class ProseMath(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out=[];self.stack=[]
    def handle_starttag(self,tag,attrs):
        raw=self.get_starttag_text();pairs=dict(attrs)
        if 'data-fb' in pairs:
            value=escape(math_text(pairs['data-fb']),quote=True)
            raw=re.sub(r'data-fb="[^"]*"',lambda _: 'data-fb="'+value+'"',raw)
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:
            self.stack.append((tag,tag in {'script','style','pre','code'} or 'pseudo-code' in pairs.get('class','').split()))
        self.out.append(raw)
    def handle_startendtag(self,tag,attrs):self.out.append(self.get_starttag_text())
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:self.stack=self.stack[:i];break
        self.out.append('</'+tag+'>')
    def handle_data(self,data):self.out.append(data if any(skip for _,skip in self.stack) else math_text(data))
    def handle_entityref(self,name):self.out.append('&'+name+';')
    def handle_charref(self,name):self.out.append('&#'+name+';')
    def handle_comment(self,data):self.out.append('<!--'+data+'-->')
    def handle_decl(self,data):self.out.append('<!'+data+'>')

def render_math(text):
    text=text.replace('$y=x+(\\mathrm{Cols}\\times i+j)\\times\\operatorname{sizeof}=0+(4\\times7+2)\\times1=30$','$$\\begin{aligned}y&=x+(\\mathrm{Cols}\\times i+j)\\times s\\\\&=0+(4\\times7+2)\\times1\\\\&=30\\end{aligned}$$')
    text=text.replace('跟上一題同一條公式，只是 sizeof 是 1。', 's 是每個元素占的空間；這一題為 $s=1$。')
    for old,new in INLINE_MATH.items():
        text=text.replace('<code>'+old+'</code>',new)
    text=text.replace("setStatus('addrStatus', `addr(a[${i}]) = 1000 + ${i} × ${size} = <strong>${1000 + i*size}</strong>：不管 i 多大都是一個乘加。`);",
        r"setStatus('addrStatus', String.raw`$\operatorname{addr}(a[${i}])=1000+${i}\times${size}=${1000+i*size}$：不管 i 多大都是一個乘加。`);")
    text=text.replace("setStatus('mdStatus', `a[${i}][${j}] → 攤平 offset = ${i}×${MD_C} + ${j} = <strong>${k}</strong>，位址 = 1000 + ${k}×4 = ${1000 + k*4}。`);",
        r"setStatus('mdStatus', String.raw`<code>a[${i}][${j}]</code> → 攤平索引 $${i}\times${MD_C}+${j}=${k}$，位址 $1000+${k}\times4=${1000+k*4}$。`);")
    text=text.replace("$('spDensity').innerHTML = `nnz = ${nnz} / ${total}<br>sparsity = ${(100*(1 - nnz/total)).toFixed(1)}%`;",
        r"chapterSetMath($('spDensity'), String.raw`$\mathrm{nnz}=${nnz}$（共 ${total} 格）<br>$\mathrm{sparsity}=${(100*(1-nnz/total)).toFixed(1)}\%$`);")
    parser=ProseMath();parser.feed(text);parser.close()
    text=''.join(parser.out)
    text=text.replace('$$。s 是每個元素', '$$s 是每個元素')
    runtime='<script id="chapter-math-runtime">\n'+(Path(__file__).parent/'chapter_math.js').read_text()+'</script>'
    style = '<style id="chapter-math-layout">.quiz-feedback,.mapping-formula{overflow-x:auto;}.status-text{min-width:0;}.status-text mjx-container{max-width:100%;overflow-x:auto;overflow-y:hidden;}</style>'
    text=re.sub(r'<script id="chapter-math-runtime">.*?</script>\n?', '', text, flags=re.S)
    text=re.sub(r'<style id="chapter-math-layout">.*?</style>\n?', '', text, flags=re.S)
    text=text.replace('</head>',runtime+'\n'+style+'\n</head>',1)
    text=text.replace("fb.innerHTML = (isCorrect ? '<strong>正確 ✓</strong> ' : '<strong>不對 ✗</strong> ') + (optEl.dataset.fb || '');", "chapterSetMath(fb, (isCorrect ? '<strong>正確 ✓</strong> ' : '<strong>不對 ✗</strong> ') + (optEl.dataset.fb || ''));")
    text=text.replace("const el = $(id); if (el) el.querySelector('.status-text').innerHTML = html;", "const el = $(id); if (el) chapterSetMath(el.querySelector('.status-text'), html);")
    text=re.sub(r"grid\.innerHTML = (cards\.map\(c =>.*?\)\.join\(''\));",lambda m:'chapterSetMath(grid, '+m[1]+');',text,flags=re.S)
    return text
