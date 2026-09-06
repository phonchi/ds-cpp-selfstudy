#!/usr/bin/env python3
"""Compare prerequisite structure with b97fe81 without requiring a newer authoring DOM."""
import argparse,hashlib,json,re,subprocess
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent;CONTRACT=ROOT/'data/prereq_fidelity_contract.json'
GEOM={'viewbox','width','height','x','y','x1','y1','x2','y2','cx','cy','r','rx','ry','d','points','transform','marker-end'}
class Shape(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=True);self.sections=[];self.tables=[];self.svgs=[];self.table=None;self.row=None;self.cell=None;self.svg=None;self.feed(s)
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='section' and a.get('id'):self.sections.append(a['id'])
  if t=='table':self.table=[]
  elif t=='tr' and self.table is not None:self.row=[]
  elif t in ('th','td') and self.row is not None:self.cell=[]
  if t=='svg':self.svg=[]
  if self.svg is not None and t in ('svg','path','rect','circle','line','polygon','polyline','ellipse'):self.svg.append((t,tuple(sorted((k.lower(),v) for k,v in a.items() if k.lower() in GEOM))))
 def handle_data(self,s):
  if self.cell is not None:self.cell.append(s)
 def handle_endtag(self,t):
  if t in ('th','td') and self.cell is not None:self.row.append(re.sub(r'\s+',' ',' '.join(self.cell)).strip());self.cell=None
  elif t=='tr' and self.row is not None:self.table.append(self.row);self.row=None
  elif t=='table' and self.table is not None:self.tables.append(self.table);self.table=None
  if t=='svg' and self.svg is not None:self.svgs.append(self.svg);self.svg=None
def dims(t):return len(t),max(map(len,t),default=0)
def table_contract(t):
 header=t[0] if t else []
 stable=tuple(x for x in header if x and not re.search(r'課程|講義|Python|本站|出處|第\s*\d+\s*章',x,re.I))
 return dims(t),stable
def sig(s):return hashlib.sha256(json.dumps(s,ensure_ascii=False).encode()).hexdigest()
def validate(newsrc, oldsrc, cfg):
 old=Shape(oldsrc);new=Shape(newsrc);errors=[]
 required_sections=cfg.get('section_order', [x for x in old.sections if x not in cfg.get('allow_removed_sections',[])])
 actual_sections=[x for x in new.sections if x in required_sections]
 if actual_sections!=required_sections:errors.append('missing or reordered baseline sections')
 pats=[re.compile(x) for x in cfg.get('allow_removed_table_patterns',[])]
 renames=cfg.get('table_header_renames',{})
 required=[(shape,tuple(renames.get(h,h) for h in headers)) for shape,headers in [table_contract(t) for t in old.tables if not any(p.search(' '.join(sum(t,[]))) for p in pats)]]
 actual=[(dims(t),tuple(t[0]) if t else ()) for t in new.tables];j=0
 for need in required:
  while j<len(actual) and not (actual[j][0]==need[0] and all(x in actual[j][1] for x in need[1])):j+=1
  if j==len(actual):errors.append(f'missing ordered baseline table rows={need[0][0]} columns={need[0][1]} headers={need[1]}');break
  j+=1
 newsigs=[sig(x) for x in new.svgs]
 for i,x in enumerate(old.svgs,1):
  key=sig(x)
  if key not in newsigs:errors.append(f'baseline SVG {i} geometry changed or disappeared')
  else:newsigs.remove(key)
 plain=re.sub(r'<[^>]+>',' ',newsrc)
 for term in cfg.get('required_terms',[]):
  if not re.search(term,plain,re.I):errors.append(f'required concept missing: {term}')
 return errors

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--pages',nargs='+');args=ap.parse_args();spec=json.loads(CONTRACT.read_text());errors=[]
 for ch in args.pages or list(spec['pages']):
  cfg=spec['pages'][ch];name=cfg['file'];oldsrc=subprocess.check_output(['git','show',f"{spec['source_baseline']}:{name}"],cwd=ROOT,text=True);newsrc=(ROOT/name).read_text();new=Shape(newsrc)
  errors.extend(f'{name}: {e}' for e in validate(newsrc,oldsrc,cfg))
  print(f'{name}: sections={len(new.sections)} tables={len(new.tables)} svgs={len(new.svgs)}')
 for e in errors:print('FAIL',e)
 print(f'{len(errors)} fidelity errors');return bool(errors)
if __name__=='__main__':raise SystemExit(main())
