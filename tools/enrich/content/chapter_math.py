"""MathJax markup for chapter prose; preserve C++/JS and existing HTML verbatim."""
from html.parser import HTMLParser
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

def plain_math(text):
    def bigo(match):
        expr=match.group()
        expr=expr.replace('²','^2').replace('³','^3').replace('×',r'\times ')
        expr=re.sub(r'\blog\b',lambda _:r'\log ',expr)
        for name in ['capacity','Rows','Cols','nnz']:
            expr=re.sub(r'\b'+name+r'\b',lambda m:r'\mathrm{'+m[0]+'}',expr)
        return '$'+expr+'$'
    # Cost expressions here have at most two nested pairs of parentheses.
    pattern=r'\bO\((?:[^()\n]|\((?:[^()\n]|\([^()\n]*\))*\))*\)'
    text=re.sub(pattern,bigo,text)
    for old,new in FORMULAS.items():text=text.replace(old,new)
    return text

def math_text(text):
    parts=re.split(r'(\$\$.*?\$\$|\$[^$]*\$)',text,flags=re.S)
    return ''.join(p if p.startswith('$') else plain_math(p) for p in parts)

class ProseMath(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out=[];self.stack=[]
    def handle_starttag(self,tag,attrs):
        raw=self.get_starttag_text();pairs=dict(attrs)
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
    text=text.replace('<code>1+2+4+…</code>',r'$1+2+4+\cdots$')
    parser=ProseMath();parser.feed(text);parser.close()
    return ''.join(parser.out)
