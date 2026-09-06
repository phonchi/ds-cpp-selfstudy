#!/usr/bin/env python3
"""Verify every prerequisite trace, quiz option, card and main-chapter visual contract.
Requires Playwright with Chromium. All pages are loaded locally; external requests are blocked.
"""
import argparse,json,re
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent
STYLE_JS="""() => {
 const spec={'body':['backgroundColor','color','fontFamily','fontSize','lineHeight'],'.hero':['backgroundImage','minHeight','paddingTop','paddingRight','paddingBottom','paddingLeft'],'.container':['maxWidth','paddingTop','paddingRight','paddingBottom','paddingLeft'],'h1':['fontFamily','fontSize','fontWeight','color'],'h2':['fontFamily','fontSize','fontWeight','color'],'.toc':['backgroundColor','borderRadius','boxShadow'],'.pseudo-code:not([style])':['backgroundColor','color','fontFamily','fontSize','lineHeight']};
 const out={}; for(const [sel,keys] of Object.entries(spec)){const el=document.querySelector(sel);if(!el)throw Error('missing style target '+sel);const cs=getComputedStyle(el);out[sel]=Object.fromEntries(keys.map(k=>[k,cs[k]]));}return out;
}"""
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--pages',nargs='+',choices=[f'p{i}' for i in range(1,10)])
 parser.add_argument('--screenshots',type=Path)
 args=parser.parse_args()
 if args.screenshots:args.screenshots.mkdir(parents=True,exist_ok=True)
 reports=[]
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,timeout=15000,args=['--no-sandbox','--disable-dev-shm-usage'])
  baseline={}
  for width in (1440,390):
   ref=browser.new_page(viewport={'width':width,'height':960})
   ref.route(re.compile('^https?://'),lambda route:route.abort())
   ref.goto((ROOT/'introduction.html').as_uri(),wait_until='load')
   baseline[width]=ref.evaluate(STYLE_JS);ref.close()
  for chapter in args.pages or [f'p{i}' for i in range(1,10)]:
   path=next(ROOT.glob(chapter+'_*.html'));report={'page':path.name,'errors':[]}
   page=browser.new_page(viewport={'width':1440,'height':960});page.set_default_timeout(5000)
   page.route(re.compile('^https?://'),lambda route:route.abort())
   page.on('pageerror',lambda e,r=report:r['errors'].append(str(e)))
   page.add_init_script("const nativeInterval=window.setInterval.bind(window);window.setInterval=(fn,ms,...args)=>nativeInterval(fn,Math.min(ms,80),...args);")
   try:
    page.goto(path.as_uri(),wait_until='load')
    traces=page.locator('.lesson-trace');assert traces.count()>=2,'need at least two substantive traces'
    for i in range(traces.count()):
     trace=traces.nth(i);play=trace.locator('[data-action="play"]');step=trace.locator('[data-action="next"]');prev=trace.locator('[data-action="prev"]');reset=trace.locator('[data-action="reset"]')
     assert trace.get_attribute('data-frame')=='0'
     step.click();assert trace.get_attribute('data-frame')=='1'
     prev.click();assert trace.get_attribute('data-frame')=='0'
     play.click();assert '暫停' in play.inner_text()
     play.click();paused=trace.get_attribute('data-frame');page.wait_for_timeout(180);assert trace.get_attribute('data-frame')==paused
     reset.click();play.click();step.click();assert '暫停' not in play.inner_text()
     reset.click();play.click()
     page.wait_for_function("id=>document.getElementById(id).querySelector('[data-action=play]').textContent.includes('重播')",arg=trace.get_attribute('id'))
     assert trace.get_attribute('data-frame')==str(int(trace.get_attribute('data-frames'))-1)
     assert trace.locator('.trace-note').inner_text().strip()
     play.click();reset.click();page.wait_for_timeout(180);assert trace.get_attribute('data-frame')=='0'
    report['traces']=traces.count()
    qs=page.locator('.sq-item');assert qs.count()>=6,'insufficient topic questions'
    options_checked=0;positions=[]
    for i in range(qs.count()):
     q=qs.nth(i);opts=q.locator('.sq-opt')
     for j in range(opts.count()):
      b=opts.nth(j);good=b.get_attribute('data-c')=='1';b.click();assert ('correct' if good else 'wrong') in b.get_attribute('class')
      assert q.locator('.sq-fb').is_visible();assert q.locator('.sq-fb').inner_text()==b.get_attribute('data-fb')
      options_checked+=1
      if good:positions.append(j+1)
    report.update(questions=qs.count(),options=options_checked,correct_positions=positions)
    expected=json.loads((ROOT/f'data/flashcards_zh/{chapter}.json').read_text())
    cards=page.locator('.fc-card');assert cards.count()==len(expected)
    for i,card in enumerate(expected):
     assert cards.nth(i).locator('.fc-front').inner_text()==card['front']
     assert cards.nth(i).locator('.fc-back').inner_text()==card['back']
    cards.first.focus();page.keyboard.press('Enter');assert 'flipped' in cards.first.get_attribute('class')
    page.locator('#fcUnflip').click();assert page.locator('.fc-card.flipped').count()==0
    page.locator('#fcFlipAll').click();assert page.locator('.fc-card.flipped').count()==cards.count()
    page.locator('#fcShuffle').click();assert cards.count()==len(expected)
    report['cards']=cards.count()
    assert page.locator('.chapter-nav a').count()>=2
    for width in (1440,390):
     page.set_viewport_size({'width':width,'height':960});page.wait_for_timeout(100)
     actual=page.evaluate(STYLE_JS)
     differences=[(sel,key,val,actual[sel][key]) for sel,props in baseline[width].items() for key,val in props.items() if actual[sel][key]!=val]
     assert not differences,f'{width}px style drift: {differences}'
     assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 2'),f'{width}px overflow'
     if width==390:assert not page.locator('.float-nav').is_visible()
     if args.screenshots:
      for region,selector in [('top','#top'),('lesson','section'),('interaction','.lesson-trace'),('cards','#cards')]:
       page.locator(selector).first.evaluate("el=>{document.documentElement.style.scrollBehavior='auto';el.scrollIntoView({block:'start',behavior:'instant'});}")
       page.wait_for_timeout(100);page.screenshot(path=str(args.screenshots/f'{chapter}-{width}-{region}.png'))
    report['styles']='match introduction.html at 1440px/390px'
   except Exception as exc:report['errors'].append(str(exc))
   page.close();reports.append(report);print(json.dumps(report,ensure_ascii=False),flush=True)
  browser.close()
 return any(r['errors'] for r in reports)
if __name__=='__main__':raise SystemExit(main())
