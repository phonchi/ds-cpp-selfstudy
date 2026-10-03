from pathlib import Path
import json,re
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).parent
results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/home/phonchi/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome',headless=True,args=['--no-sandbox'])
 for name in ['arrays','linked_lists']:
  page=b.new_page(viewport={'width':1440,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.route('https://**/*',lambda r:r.continue_() if r.request.url.startswith('https://cdn.jsdelivr.net/npm/mathjax@3/') else r.abort())
  page.goto((ROOT/(name+'.html')).as_uri(),wait_until='domcontentloaded')
  page.wait_for_function('window.MathJax && MathJax.startup && MathJax.startup.document',timeout=30000)
  page.evaluate('MathJax.startup.promise');page.evaluate('chapterMathIdle()')
  print('Loaded',name,flush=True)
  for d in page.locator('details').all():
   assert not d.evaluate('e=>e.open');d.locator(':scope > summary').click()
  def formulas(): return page.evaluate('Array.from(MathJax.startup.document.math).map(x=>x.math.replace(/\\s/g,""))')
  initial=page.locator('mjx-container').count();assert initial>50
  if name=='arrays':
   assert r'5\times4+3=23' in formulas()
   assert r'3\times100+5=305' in formulas()
   page.locator('#addrVis .bq-item').nth(3).click();page.evaluate('chapterMathIdle()')
   assert page.locator('#addrStatus mjx-container').count()==1
   page.select_option('#addrSize','8');page.locator('#addrVis .bq-item').nth(3).click();page.evaluate('chapterMathIdle()')
   assert r'\operatorname{addr}(a[3])=1000+3\times8=1024' in formulas()
   page.locator('#mdGrid .char-cell').nth(6).click();page.evaluate('chapterMathIdle()')
   assert page.locator('#mdStatus mjx-container').count()==2
   for k in range(12):
    page.locator(f'#mappingGrid [data-logical="{k}"]').click();page.evaluate('chapterMathIdle()')
    i,j=divmod(k,4)
    assert f'{i}\\times4+{j}={k}' in formulas()
    assert f'{j}\\times3+{i}={j*3+i}' in formulas()
   page.evaluate("for(let k=0;k<12;k++)document.querySelector('#mappingGrid [data-logical=\"'+k+'\"]').click();document.querySelector('#mappingReset').click();")
   page.evaluate('chapterMathIdle()');assert r'\mathrm{offset}=i\times\mathrm{Cols}+j' in formulas()
   assert page.locator('#mappingProgress').input_value()=='0'
   page.locator('#mappingDelay').select_option('250');page.locator('#mappingPlay').click()
   page.wait_for_function('document.querySelector("#mappingProgress").value==="12"');page.evaluate('chapterMathIdle()')
   assert r'2\times4+3=11' in formulas()
   page.evaluate('spRandom()');page.evaluate('chapterMathIdle()')
   assert r'\mathrm{nnz}=4' in formulas()
   page.evaluate('spClear()');page.evaluate('chapterMathIdle()');assert r'\mathrm{nnz}=0' in formulas()
  else:
   assert r'\frac{n}{2}' in formulas()
   assert r'54\gt45' in formulas()
   page.evaluate("ollReset();$('ollInput').value='40';ollAdd();ollPlayer.pause();")
   page.evaluate('chapterMathIdle()');assert r'17\lt40' in formulas()
   for _ in range(3):page.evaluate('ollPlayer.step()')
   page.evaluate('chapterMathIdle()');assert r'54\ge40' in formulas()
   page.evaluate("ollReset();ullReset();$('ullInput').value='17';ullSearch();ullPlayer.pause();")
   page.evaluate('chapterMathIdle()');assert r'31\ne17' in formulas()
   page.evaluate('ullPlayer.step();ullPlayer.step()');page.evaluate('chapterMathIdle()');assert '17=17' in formulas()

   page.evaluate("ullReset();$('ullInput').value='99';ullAdd();ullPlayer.pause();while(!ullPlayer._done)ullPlayer.step();")
   page.evaluate('chapterMathIdle()');assert page.locator('#ullStatus mjx-container').count()==1
  checked=0
  for opt in page.locator('.quiz-opt').all():
   opt.click();page.evaluate('chapterMathIdle()')
   expected=len(re.findall(r'\$\$.*?\$\$|\$[^$]*\$',opt.get_attribute('data-fb'),re.S))
   if expected:
    fb=opt.locator('xpath=ancestor::div[contains(@class,"quiz-box")]').locator('.quiz-feedback')
    assert fb.locator('mjx-container').count()==expected,(name,opt.inner_text(),expected,fb.inner_text())
   checked+=1
  count=page.evaluate('Array.from(MathJax.startup.document.math).length')
  for _ in range(3):
   page.locator('#fcShuffle').click();page.evaluate('chapterMathIdle()')
   assert page.evaluate('Array.from(MathJax.startup.document.math).length')==count
  assert page.locator('#fcGrid mjx-container').count()>0
  assert not page.evaluate('window.chapterMathError || null')
  assert page.locator('mjx-merror').count()==0;assert not errors,errors
  for width in [1440,390]:
   page.set_viewport_size({'width':width,'height':1000});page.wait_for_timeout(100)
   if name=='arrays':
    page.locator('#ex4Options .quiz-opt[data-correct="true"]').click();page.evaluate('chapterMathIdle()')
    page.locator('.matrix-equations').screenshot(path=str(OUT/f'matrices-{width}.png'))
    page.locator('#dx-multi').screenshot(path=str(OUT/f'student-offset-{width}.png'))
    page.locator('#ex4Feedback').screenshot(path=str(OUT/f'quiz-formula-{width}.png'))
    page.locator('#matrixMapping').screenshot(path=str(OUT/f'mapping-{width}.png'))
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(name,width,page.evaluate('document.documentElement.scrollWidth'))
  results.append({'page':name,'initial_rendered_math':initial,'quiz_options_checked':checked,'card_shuffles':3,'mathjax_errors':0,'page_errors':errors,'viewports':[1440,390]})
  page.close()
 b.close()
(OUT/'browser-results.json').write_text(json.dumps(results,indent=2)+'\n');print(results)
