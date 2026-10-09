import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path('/home/phonchi/ds-cpp-selfstudy')
CHROME = '/home/phonchi/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'
STEP = """([start, pl, code, status])=>{eval(start); const P=eval(pl); P.pause(); P.i=-1; P._done=false;
 const out=[]; while(P.i+1<P.frames.length){P.step();
  const a=document.querySelector('#'+code+' .line.active');
  out.push({line: a? a.getAttribute('data-l'):null, code: a? a.textContent.trim():null,
            msg: document.querySelector('#'+status+' .status-text').textContent});}
 return out;}"""
cases = {
 'linear_structures': [
   ("parStart()", 'parPlayer', 'parCode', 'parStatus'),
   ("parLoad('())(')", 'parPlayer', 'parCode', 'parStatus'),
   ("($('parInput').value='[{()]', parStart())", 'parPlayer', 'parCode', 'parStatus'),
   ("parLoad('(()')", 'parPlayer', 'parCode', 'parStatus'),
   ("baseStart()", 'basePlayer', 'baseCode', 'baseStatus'),
   ("i2pStart()", 'i2pPlayer', 'i2pCode', 'i2pStatus'),
   ("($('i2pSel').selectedIndex=$('i2pSel').options.length-1, i2pStart())", 'i2pPlayer', 'i2pCode', 'i2pStatus'),
   ("pevalStart()", 'pevalPlayer', 'pevalCode', 'pevalStatus'),
   ("($('palInput').value='radar', palStart())", 'palPlayer', 'palCode', 'palStatus'),
   ("($('palInput').value='lsdkjfskf', palStart())", 'palPlayer', 'palCode', 'palStatus'),
 ],
 'recursion': [
   ("($('hanoiN').value='3', hanoiStart())", 'hanoiPlayer', 'hanoiCode', 'hanoiStatus'),
 ],
}
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, headless=True, args=['--no-sandbox'])
    for page_name, cs in cases.items():
        pg = b.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.route('https://**/*', lambda r: r.abort())
        pg.goto((ROOT/f'{page_name}.html').as_uri(), wait_until='load')
        for c in cs:
            res[f'{page_name}:{c[0]}'] = pg.evaluate(STEP, list(c))
        if page_name == 'recursion':
            # hanoi pegs at end, for n=3,4,5
            for n in (3,4,5):
                fr = pg.evaluate(f"hanoiFrames({n})")
                res[f'hanoi{n}'] = {'frames': len(fr), 'moves': len(fr)-2, 'final': fr[-1]['pegs'], 'last': fr[-1]['msg']}
            res['viz'] = pg.evaluate("""()=>{spiralStart(); const s=document.querySelector('#vizStatus .status-text').textContent;
              const px=id=>{const c=document.getElementById(id);const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let n=0;for(let i=3;i<d.length;i+=4)if(d[i])n++;return n;};
              const out={spiral:s, spiralPx:px('spiralCv')}; for(const k of [1,2,3,4,5]){$('treeDepth').value=k;treeDraw();out['tree'+k]=document.querySelector('#vizStatus .status-text').textContent;}
              out.treePx=px('treeCv'); out.sliderMax=$('treeDepth').max; return out;}""")
            pg.locator('#spiralCv').screenshot(path=str(Path(sys.argv[1])/'spiral.png'))
            pg.locator('#treeCv').screenshot(path=str(Path(sys.argv[1])/'tree.png'))
        res[page_name+':errors'] = errs
    pg = b.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route('https://**/*', lambda r: r.abort())
    pg.goto((ROOT/'linked_lists.html').as_uri(), wait_until='load')
    pg.locator('button.ll-case[data-ll="dIns"]').first.click()
    res['dIns'] = pg.evaluate("""()=>{const pl=LLP.dIns; pl.pause&&pl.pause(); const out=[];
       while(!pl._done && out.length<20){llStep('dIns'); const a=document.querySelector('#dInsCode .line.active, [id^=dInsCode] .line.active');
       const st=document.querySelector('#dInsStatus .status-text, #dInsStatus'); out.push({line:a?a.getAttribute('data-l'):null, code:a?a.textContent.trim():null, msg: st?st.textContent:null});} return out;}""")
    res['linked:errors']=errs
    b.close()
json.dump(res, open(Path(sys.argv[1])/'step.json','w'), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
