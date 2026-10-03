from pathlib import Path
from bs4 import BeautifulSoup
import re,json,subprocess
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).parent
base='395a2be'
remaining=[];counts={}
for name in ['arrays','linked_lists']:
 current=BeautifulSoup((ROOT/(name+'.html')).read_text(),'html.parser',preserve_whitespace_tags={'pre','span'})
 old=BeautifulSoup(subprocess.check_output(['git','show',base+':'+name+'.html'],cwd=ROOT,text=True),'html.parser',preserve_whitespace_tags={'pre','span'})
 selectors='.pseudo-code,.expected-out pre'
 assert [e.get_text() for e in current.select(selectors)]==[e.get_text() for e in old.select(selectors)],name
 def scan(text,kind):
  bare=re.sub(r'\$\$.*?\$\$|\$[^$]*\$','',text,flags=re.S)
  if re.search(r'[×²³⁵⁶¹⁰]|\bn\s*/\s*2\b|\d+\s*[+<>＝=]\s*\d+|\bO\(',bare):remaining.append([name,kind,bare])
 for node in current.find_all(string=True):
  if node.find_parent(['script','style','pre','code']) or node.find_parent(class_='pseudo-code'):continue
  scan(str(node),node.parent.name)
 for node in current.select('[data-fb]'):scan(node['data-fb'],'feedback')
 data=json.loads((ROOT/'data/flashcards_zh'/('ch3.json' if name=='arrays' else 'ch4.json')).read_text())
 for card in data:scan(card['back'],'flashcard')
 summaries=[x.get_text() for x in current.select('summary')]
 exception='SparseMatrix：完整 C++ 類別、使用範例與加減乘'
 assert all(t.endswith('（補充）') or t==exception for t in summaries)
 counts[name]={'supplementary':sum(t.endswith('（補充）') for t in summaries),'lecture_code':summaries.count(exception)}
assert not remaining,remaining
(OUT/'static-audit.json').write_text(json.dumps({'base':base,'protected_code_selectors':selectors,'code_unchanged':True,'remaining_candidates':remaining,'details':counts},ensure_ascii=False,indent=2)+'\n')
print('Static formula scan, C++ preservation and supplementary labels passed')
