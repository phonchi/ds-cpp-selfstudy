#!/usr/bin/env python3
"""Check reviewed teaching units still exist; additions are allowed, silent deletions are not.
The contract is a reviewed snapshot, not a generator or a substitute for comparing b97fe81.
Uses only the standard library. Regenerating the contract requires a new content review.
"""
from collections import Counter
from hashlib import sha256
from html.parser import HTMLParser
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
CONTRACT=ROOT/'data/prereq_fidelity_contract.json'
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
def norm(s):return re.sub(r'\s+',' ',s).strip()
def digest(value):return sha256(json.dumps(value,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
class Units(HTMLParser):
 def __init__(self,source):
  super().__init__(convert_charrefs=True);self.stack=[];self.tables=[];self.paragraphs=[];self.svgs=[];self.table=None;self.row=None;self.cell=None;self.par=None;self.svg=None;self.feed(source)
 def scope(self):return [attrs.get('id') for _,attrs in self.stack if attrs.get('id')]
 def teaching(self):
  return any('container' in attrs.get('class','').split() for _,attrs in self.stack) and not any(x in ('bankquiz','cards') for x in self.scope())
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if self.svg is not None:self.svg['tokens'].append([tag,attrs])
  elif tag=='svg':self.svg={'scope':self.scope(),'line':self.getpos()[0],'tokens':[[tag,attrs]]}
  if tag=='table' and self.teaching():self.table={'scope':self.scope(),'line':self.getpos()[0],'rows':[]}
  if tag=='tr' and self.table is not None:self.row=[]
  if tag in ('th','td') and self.row is not None:self.cell=[]
  if tag=='p' and self.teaching():self.par={'scope':self.scope(),'line':self.getpos()[0],'text':[]}
  if tag not in VOID:self.stack.append((tag,attrs))
 def handle_startendtag(self,tag,attrs):
  self.handle_starttag(tag,attrs)
  if tag not in VOID:self.handle_endtag(tag)
 def handle_data(self,text):
  if self.cell is not None:self.cell.append(text)
  if self.par is not None:self.par['text'].append(text)
  if self.svg is not None and norm(text):self.svg['tokens'].append(['text',norm(text)])
 def handle_endtag(self,tag):
  if self.svg is not None:
   self.svg['tokens'].append(['/'+tag])
   if tag=='svg':self.svgs.append(self.svg);self.svg=None
  if tag in ('td','th') and self.cell is not None:
   self.row.append(norm(''.join(self.cell)));self.cell=None
  if tag=='tr' and self.row is not None:self.table['rows'].append(self.row);self.row=None
  if tag=='table' and self.table is not None:self.tables.append(self.table);self.table=None
  if tag=='p' and self.par is not None:
   self.par['text']=norm(''.join(self.par['text']))
   if self.par['text']:self.paragraphs.append(self.par)
   self.par=None
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:
    del self.stack[i:];break
 def records(self):
  def rec(u,key):return {'scope':' / '.join(u['scope']),'line':u['line'],'digest':digest(u[key]),'excerpt':norm(str(u[key]))[:140]}
  return {'tables':[dict(rec(u,'rows'),rows=len(u['rows']),columns=max(map(len,u['rows']),default=0)) for u in self.tables],
          'paragraphs':[rec(u,'text') for u in self.paragraphs],
          'svgs':[rec(u,'tokens') for u in self.svgs]}
def validate(source,expected):
 actual=Units(source).records();errors=[]
 for kind,units in expected.items():
  counts=Counter(u['digest'] for u in actual[kind])
  for unit in units:
   if counts[unit['digest']]:counts[unit['digest']]-=1
   else:errors.append(f"{kind}: reviewed unit missing/changed at {unit['scope']}: {unit['excerpt']}")
 return errors

def main():
 contract=json.loads(CONTRACT.read_text());errors=[];counts=Counter()
 for name,expected in contract['pages'].items():
  errors.extend(name+': '+e for e in validate((ROOT/name).read_text(),expected))
  counts.update({key:len(value) for key,value in expected.items()})
 print('Reviewed units:',dict(counts))
 for error in errors:print('FAIL',error)
 print(len(errors),'fidelity errors')
 return bool(errors)
if __name__=='__main__':raise SystemExit(main())
