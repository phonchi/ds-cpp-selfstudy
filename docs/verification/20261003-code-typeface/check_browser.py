from pathlib import Path
from playwright.sync_api import sync_playwright
import json,re,sys
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'tools/enrich'))
from content.inline_code import TOKEN_RE,is_term_prose
report=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/home/phonchi/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome',headless=True,args=['--no-sandbox'])
 for name in ['arrays','linked_lists']:
  page=browser.new_page(viewport={'width':1440,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.route('https://**/*',lambda r:r.continue_() if r.request.url.startswith('https://cdn.jsdelivr.net/npm/mathjax@3/') else r.abort())
  page.goto((ROOT/(name+'.html')).as_uri(),wait_until='domcontentloaded');page.wait_for_function('window.MathJax && MathJax.startup && MathJax.startup.document');page.evaluate('MathJax.startup.promise');page.evaluate('chapterMathIdle()')
  for detail in page.locator('details').all():detail.locator(':scope > summary').click()
  samples=page.locator('code').filter(has_text=re.compile(r'^(pop_back|std::list|std::forward_list|push_back|ArrayList|size_t)$'))
  assert samples.count()>8
  assert samples.evaluate_all('xs=>xs.every(x=>/mono/i.test(getComputedStyle(x).fontFamily))')
  for option in page.locator('.quiz-opt').all():
   option.click();page.evaluate('chapterMathIdle()');assert not page.locator('.quiz-feedback code code').count()
  for _ in range(3):page.locator('#fcShuffle').click();page.evaluate('chapterMathIdle()')
  assert page.locator('#fcGrid code').count()>0
  assert page.locator('#fcGrid code').evaluate_all('xs=>xs.every(x=>/mono/i.test(getComputedStyle(x).fontFamily))')
  assert page.locator('mjx-container code').count()==0
  assert page.locator('mjx-merror').count()==0
  if name=='linked_lists':
   page.evaluate("ullReset();$('ullInput').value='99';ullAdd();ullPlayer.pause();while(!ullPlayer._done)ullPlayer.step();")
   page.evaluate('chapterMathIdle()');assert page.locator('#ullStatus code').count()>0
  nodes=page.evaluate('''()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT),xs=[];while(w.nextNode()){const n=w.currentNode,p=n.parentElement;if(!p||p.closest('code,pre,script,style,svg,mjx-container,.pseudo-code'))continue;xs.push({text:n.data,font:getComputedStyle(p).fontFamily});}return xs;}''')
  misses=[]
  for node in nodes:
   for text in re.split(r'\$\$.*?\$\$|\$[^$]*\$',node['text'],flags=re.S):
    for m in TOKEN_RE.finditer(text):
     if not is_term_prose(m[0],text[:m.start()],text[m.end():]) and 'mono' not in node['font'].lower():misses.append([m[0],node])
  assert not misses,(name,misses)
  for width in [1440,390]:
   page.set_viewport_size({'width':width,'height':1000});page.wait_for_timeout(100)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(name,width)
   if name=='arrays':
    page.locator('#layout .chapter-table').screenshot(path=str(OUT/f'array-cost-table-{width}.png'))
    page.locator('#prologue details').first.locator(':scope > summary').screenshot(path=str(OUT/f'array-summary-{width}.png'))
   else:
    page.locator('#stl details').first.locator(':scope > summary').screenshot(path=str(OUT/f'list-summary-{width}.png'))
    page.locator('#stl details').first.locator('p').first.screenshot(path=str(OUT/f'list-prose-{width}.png'))
  assert not errors and not page.evaluate('window.chapterMathError || null')
  report.append({'page':name,'code_font':'monospace','card_inline_code':page.locator('#fcGrid code').count(),'plain_code_identifiers':misses,'mathjax_errors':0,'page_errors':errors,'viewports':[1440,390]});page.close()
 browser.close()
(OUT/'font-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(report)
