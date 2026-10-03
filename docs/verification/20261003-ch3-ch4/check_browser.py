"""Bounded desktop/mobile interaction acceptance for Chapters 3 and 4."""
from pathlib import Path
import os
import json,re
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(os.environ.get("DSCPP_VERIFY_OUT", str(Path(__file__).parent)))
OUT.mkdir(parents=True, exist_ok=True)
report=[]
print('Starting Playwright',flush=True)
with sync_playwright() as p:
 print('Launching Chromium',flush=True)
 browser=p.chromium.launch(timeout=20000,executable_path='/home/phonchi/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome',headless=True,args=['--no-sandbox'])
 print('Browser ready',flush=True)
 for name in ['arrays','linked_lists']:
  print('Checking',name,flush=True)
  page=browser.new_page(viewport={'width':1440,'height':1000})
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.route('https://**/*',lambda r: r.continue_() if os.environ.get('DSCPP_MATHJAX')=='1' and r.request.url.startswith('https://cdn.jsdelivr.net/npm/mathjax@3/') else r.abort())
  page.set_default_timeout(15000)
  page.goto((ROOT/(name+'.html')).as_uri(),wait_until='domcontentloaded')
  if os.environ.get('DSCPP_MATHJAX')=='1':
   page.wait_for_function('window.MathJax && MathJax.startup && MathJax.startup.document',timeout=30000)
   page.evaluate('MathJax.startup.promise')
   assert page.locator('mjx-container').count()>30
   assert page.locator('mjx-merror').count()==0
  print('Loaded',flush=True)
  assert not errors,errors
  for el in page.locator('details').all():
   assert not el.get_attribute('open')
   el.locator(':scope > summary').click();assert el.evaluate('e=>e.open')
  print('Details opened',flush=True)
  if name=='arrays':
   page.evaluate('addrRender(3)')
   page.select_option('#addrSize','8')
   assert '每格 8 bytes' in page.locator('#addrStatus').inner_text()
   assert '1012' not in page.locator('#addrStatus').inner_text()
   page.locator('#mappingStep').click()
   assert page.locator('#mappingProgress').input_value()=='1'
   for k in range(12):
    page.locator(f'#mappingGrid [data-logical="{k}"]').click()
    r,c=divmod(k,4);coloffset=c*3+r
    assert page.locator('#mappingRow .is-selected').get_attribute('data-offset')==str(k)
    assert page.locator('#mappingCol .is-selected').get_attribute('data-offset')==str(coloffset)
    assert page.locator('#mappingRow .is-selected').get_attribute('data-value')==str(k+1)
   assert page.locator('#mappingCol .memory-cell').evaluate_all('(xs)=>xs.map(x=>+x.dataset.value)')==[1,5,9,2,6,10,3,7,11,4,8,12]
   page.locator('#mappingReset').click()
   assert page.locator('#mappingProgress').input_value()=='0'
   page.locator('#mappingDelay').select_option('250')
   page.locator('#mappingPlay').click();page.wait_for_timeout(330)
   page.locator('#mappingPlay').click();value=page.locator('#mappingProgress').input_value()
   page.wait_for_timeout(350);assert page.locator('#mappingProgress').input_value()==value
   page.locator('#mappingPlay').click()
   page.wait_for_function('document.querySelector("#mappingProgress").value==="12"')
   assert page.locator('#mappingPlay').inner_text()=='重播'
   page.locator('#mappingPlay').click();page.locator('#mappingReset').click()
   page.wait_for_timeout(350);assert page.locator('#mappingProgress').input_value()=='0'
   page.locator('#mappingProgress').evaluate('e=>{e.value=6;e.dispatchEvent(new Event("input"))}')
   assert page.locator('#mappingRow .memory-cell[data-value=""]').count()==6
   page.locator('#mappingGrid [data-logical="6"]').click()
   page.evaluate('spRandom()');assert 'Linear list' in page.locator('#spStore').inner_text()
   page.evaluate('spClear()');assert 'head → nullptr' in page.locator('#spStore').inner_text()
  if name=='linked_lists':
   race = page.evaluate("""async () => {
    ullReset(); $('ullInput').value='93'; ullRemove();
    $('ullInput').value='99'; ullAdd(); ullPlayer.pause();
    while (!ullPlayer._done) ullPlayer.step();
    await new Promise(r=>setTimeout(r,650));
    if(JSON.stringify(ull)!==JSON.stringify([99,31,77,17,93])) throw Error('stale removal changed list');
    ullReset(); $('ullInput').value='93'; ullRemove(); ullReset();
    await new Promise(r=>setTimeout(r,650));
    if(ullPlayer!==null || JSON.stringify(ull)!==JSON.stringify([31,77,17,93])) throw Error('reset kept removal');
    ollReset(); $('ollInput').value='40'; ollAdd(); ollReset();
    await new Promise(r=>setTimeout(r,650));
    if(ollPlayer!==null || JSON.stringify(oll)!==JSON.stringify([17,26,31,54,77,93])) throw Error('reset kept insertion');
    ullReset();$('ullInput').value='17';ullRemove();ullPlayer.pause();
    while(!ullPlayer._done)ullPlayer.step();
    const doneState=JSON.stringify(ull), index=ullPlayer.i;ullPlayer.toggle();ullPlayer.step();
    if(JSON.stringify(ull)!==doneState || ullPlayer.i!==index)throw Error('completed mutation replayed');
    if(!document.querySelector('#unordered button[onclick*=toggle]').disabled)throw Error('completed button enabled');
    return 'timer cancellation and completed replay checks passed';
   }""")
   print(race,flush=True)
  page.locator('img[src^="assets/figures/ch"]').evaluate_all("async xs=>{for(const im of xs){im.loading='eager';await im.decode();if(!im.naturalWidth)throw Error(im.src);}}")
  print('New mapping checked',flush=True)
  # Exercise existing controls and every frame of their players.
  names=sorted(set(re.findall(r'(\w+Player)\s*=\s*new Player',(ROOT/(name+'.html')).read_text())))
  frames=0
  for b in page.locator('section button[onclick]').all():
   print('Control',b.get_attribute('onclick'),flush=True)
   # Native prompt actions are not present in these chapters; defaults are bounded.
   if b.is_disabled(): continue
   b.click()
   for player in names:
    frames+=page.evaluate('''name=>{
      const p=eval(name);if(!p)return 0;p.pause();let n=0;
      while(!p._done && n<=p.frames.length+1){p.step();n++;}
      if(!p._done||p.playing)throw Error('player not stopped: '+name);
      return n;
    }''',player)
  for q in page.locator('.quiz-options').all():
   assert q.locator('[data-correct="true"]').count()==1
   q.locator('[data-correct="true"]').click()
  page.locator('#fcGrid .fc-card').first.click()
  assert 'flipped' in page.locator('#fcGrid .fc-card').first.get_attribute('class')
  page.locator('#fcUnflip').click()
  for width in [1440,390]:
   page.set_viewport_size({'width':width,'height':1000})
   page.wait_for_timeout(100)
   overflow=page.evaluate('''()=>[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+2 && getComputedStyle(e).position!=='fixed').slice(0,15).map(e=>[e.tagName,e.id,e.className,e.getBoundingClientRect().right])''')
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(name,width,overflow)
   target=page.locator('#matrixMapping' if name=='arrays' else '#stl')
   target.screenshot(path=str(OUT/f'{name}-{width}.png'))
   if name=='arrays':
    for mode in ['Row','Col']:
     assert page.locator('#mapping'+mode+' .is-selected').evaluate('e=>{const a=e.getBoundingClientRect(), b=e.parentElement.parentElement.getBoundingClientRect();return a.left>=b.left-1 && a.right<=b.right+1;}')
   else:
    page.locator('#stl details').first.screenshot(path=str(OUT/f'linked-example-{width}.png'))
  figures=page.locator('figure:has(img[src^="assets/figures/ch"])')
  assert figures.count()==3,(name,figures.count())
  for i in range(figures.count()):
   figures.nth(i).screenshot(path=str(OUT/f'{name}-figure-{i+1}-390.png'))
  if os.environ.get('DSCPP_MATHJAX')=='1':
   assert page.locator('mjx-merror').count()==0
   page.locator('#sparse' if name=='arrays' else '#ordered').screenshot(path=str(OUT/f'{name}-math-content-390.png'))
  assert not errors,errors
  report.append({'page':name,'details':page.locator('details').count(),'player_frames_checked':frames,'viewports':[1440,390],'page_errors':errors})
  page.close()
 browser.close()
(OUT/'browser-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
