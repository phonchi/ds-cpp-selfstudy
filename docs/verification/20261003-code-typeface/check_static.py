from pathlib import Path
from bs4 import BeautifulSoup,Comment
import json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'tools/enrich'))
from content.inline_code import TOKEN_RE,is_term_prose
report=[]
for name in ['arrays','linked_lists']:
 text=(ROOT/(name+'.html')).read_text()
 soup=BeautifulSoup(text,'html.parser',preserve_whitespace_tags={'pre','span'})
 old=BeautifulSoup(subprocess.check_output(['git','show','09bcc0b:'+name+'.html'],cwd=ROOT,text=True),'html.parser',preserve_whitespace_tags={'pre','span'})
 assert [e.get_text() for e in soup.select('.pseudo-code,.expected-out pre')]==[e.get_text() for e in old.select('.pseudo-code,.expected-out pre')]
 assert [a.get('href') for a in soup.select('a')]==[a.get('href') for a in old.select('a')]
 assert not soup.select('code code')
 remaining=[]
 for node in soup.find_all(string=True):
  if isinstance(node,Comment):continue
  if node.find_parent(['code','pre','script','style','svg','title']) or node.find_parent(class_='pseudo-code'):continue
  for chunk in re.split(r'\$\$.*?\$\$|\$[^$]*\$',str(node),flags=re.S):
   for m in TOKEN_RE.finditer(chunk):
    if not is_term_prose(m[0],chunk[:m.start()],chunk[m.end():]):remaining.append([node.parent.name,m[0],chunk])
 assert not remaining,(name,remaining)
 report.append({'page':name,'static_inline_code':len(soup.select('code')),'code_and_output_unchanged':True,'links_unchanged':True,'nested_code':0,'remaining_identifiers':remaining})
(OUT/'static-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(report)
