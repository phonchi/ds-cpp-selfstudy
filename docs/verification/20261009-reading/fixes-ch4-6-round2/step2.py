"""Round-2 checks for ch5/ch6 players: step before ▶, maze walk, hanoi labels, sierpinski pixels."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path('/home/phonchi/ds-cpp-selfstudy')
OUT = Path(__file__).with_name('step2.json')
CHROME = '/home/phonchi/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'

# (player var, code panel id or None, status id)
PLAYERS = {
  'recursion': [('sum', 'sumCode', 'sumStatus'), ('tostr', 'tostrCode', 'tostrStatus'), ('tsf', 'tsfCode', 'tsfStatus'),
                ('frame', None, 'frameStatus'), ('hanoi', 'hanoiCode', 'hanoiStatus'), ('maze', 'mazeCode', 'mazeStatus'),
                ('dp', 'dpCode', 'dpStatus')],
  'linear_structures': [('intro', None, 'introStatus'), ('par', 'parCode', 'parStatus'), ('base', 'baseCode', 'baseStatus'),
                        ('i2p', 'i2pCode', 'i2pStatus'), ('peval', 'pevalCode', 'pevalStatus'), ('hp', 'hpCode', 'hpStatus'),
                        ('pal', 'palCode', 'palStatus')],
}
SNAP = """([p, code, status])=>{const P=eval(p+'Player');const a=code?document.querySelector('#'+code+' .line.active'):null;
  return {i:P?P.i:null, playing:P?P.playing:null, frameLine: P&&P.frames[P.i]?P.frames[P.i].line:null,
          active: a?+a.dataset.l:null, msg: document.querySelector('#'+status+' .status-text').textContent};}"""

def click_step(pg, p):
    pg.locator(f'button[onclick="{p}Player &amp;&amp; {p}Player.step()"], button[onclick="{p}Player && {p}Player.step()"]').first.click()

res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME, headless=True, args=['--no-sandbox'])
    for page_name, players in PLAYERS.items():
        for p, code, status in players:
            pg = b.new_page(); errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.route('https://**/*', lambda r: r.abort())
            pg.goto((ROOT / f'{page_name}.html').as_uri(), wait_until='load')
            pg.evaluate("()=>document.querySelectorAll('details').forEach(d=>d.open=true)")
            s0 = pg.evaluate(SNAP, [p, code, status])
            steps = []
            for _ in range(3):
                click_step(pg, p)
                steps.append(pg.evaluate(SNAP, [p, code, status]))
            ok = (s0['i'] == 0 and [x['i'] for x in steps] == [1, 2, 3]
                  and all(x['msg'] != y['msg'] for x, y in zip([s0] + steps, steps))
                  and all(code is None or x['frameLine'] is None or x['active'] == x['frameLine'] for x in steps))
            # ▶ still works from the loaded state
            pg.evaluate(f"()=>{{const sp=document.getElementById('{p}Speed'); if(sp) sp.value=sp.min;}}")
            pg.locator(f'button[onclick="{p}Start()"]').first.click()
            pg.wait_for_function(f"()=>{p}Player._done", timeout=60000)
            res[f'{page_name}:{p}'] = {'loaded': s0, 'after_steps': steps, 'ok': ok, 'play_done': True, 'errors': errs}
            pg.close()

    # Maze: from load, click 單步 until done; check final grid reaches E with a connected path.
    pg = b.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route('https://**/*', lambda r: r.abort())
    pg.goto((ROOT / 'recursion.html').as_uri(), wait_until='load')
    n = 0
    while not pg.evaluate('mazePlayer._done') and n < 2000:
        click_step(pg, 'maze'); n += 1
    maze = pg.evaluate("""()=>{const P=mazePlayer;const f=P.frames[P.frames.length-1];
       const lines=document.getElementById('mazeVis').innerText.split('\\n').filter(x=>x);
       let lineOk=true;
       for(const fr of P.frames){ /* every frame's highlight is consistent with its message */
         if(/是牆/.test(fr.msg)&&fr.line!==2) lineOk=false;
         if(/到達出口/.test(fr.msg)&&fr.line!==5) lineOk=false;
         if(/標記走過/.test(fr.msg)&&fr.line!==8) lineOk=false;
         if(/成功路徑/.test(fr.msg)&&fr.line!==13) lineOk=false;
         if(/死路/.test(fr.msg)&&fr.line!==14) lineOk=false; }
       return {frames:P.frames.length, i:P.i, grid:f.grid.map(r=>r.join('')), shown:lines,
               status:document.querySelector('#mazeStatus .status-text').textContent, lineOk};}""")
    g = maze['grid']
    path = {(r, c) for r, row in enumerate(g) for c, ch in enumerate(row) if ch == 'P'}
    # S cell is overwritten with P when on the path; E as well.
    start = (5, 1); exit_ = (5, 11)
    seen = {start}; stack = [start]
    while stack:
        r, c = stack.pop()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (r + dr, c + dc)
            if q in path and q not in seen:
                seen.add(q); stack.append(q)
    maze.update(clicks=n, path_cells=sorted(path), start_on_path=start in path, exit_on_path=exit_ in path,
                path_connected=exit_ in seen and len(seen) == len(path), errors=errs)
    res['maze_walk'] = maze

    # Hanoi pole labels and final frame highlight.
    pg.evaluate("()=>{$('hanoiN').value='4';$('hanoiN').dispatchEvent(new Event('change'));}")
    res['hanoi'] = pg.evaluate("""()=>{const labels=[...document.querySelectorAll('#hanoiVis .hanoi-pole')].map(e=>e.innerText.replace(/\\n/g,' '));
       const P=hanoiPlayer; while(!P._done) P.step();
       return {labels, frames:P.frames.length, lastLine:P.frames[P.frames.length-1].line,
               active:document.querySelectorAll('#hanoiCode .line.active').length,
               status:document.querySelector('#hanoiStatus .status-text').textContent,
               labelsAfter:[...document.querySelectorAll('#hanoiVis .hanoi-pole')].map(e=>e.innerText.replace(/\\n/g,' '))};}""")
    # Sierpinski pixels and colours used at degree 3.
    res['sierpinski'] = pg.evaluate("""()=>{const c=document.getElementById('sierCv');document.getElementById('sierDeg').value=3;sierDraw();
       const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let k=0;const cols=new Set();
       for(let i=0;i<d.length;i+=4){if(d[i+3]){k++;cols.add(d[i]+','+d[i+1]+','+d[i+2]);}}
       return {painted:k, distinctColours:cols.size, status:document.querySelector('#sierStatus .status-text').textContent};}""")
    pg.locator('#hanoiVis').screenshot(path=str(OUT.with_name('hanoi-labels.png')))
    pg.locator('#mazeVis').screenshot(path=str(OUT.with_name('maze-final.png')))
    pg.locator('#sierCv').screenshot(path=str(OUT.with_name('sierpinski.png')))
    res['recursion_page_errors'] = errs
    # Parens input keeps only bracket characters (parChecker treats anything else as a closing symbol).
    pg2 = b.new_page(); pg2.route('https://**/*', lambda r: r.abort())
    pg2.goto((ROOT / 'linear_structures.html').as_uri(), wait_until='load')
    pg2.fill('#parInput', '(a)'); pg2.locator('#parInput').dispatch_event('change')
    res['parens_sanitize'] = pg2.evaluate("""()=>{const r={input:$('parInput').value,
        frame0:document.querySelector('#parStatus .status-text').textContent};
        const P=parPlayer; while(!P._done) P.step(); r.final=document.querySelector('#parStatus .status-text').textContent; return r;}""")
    b.close()
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1))
bad = [k for k, v in res.items() if isinstance(v, dict) and v.get('ok') is False]
print('not ok:', bad)
print(json.dumps(res['maze_walk'], ensure_ascii=False)[:1500])
print(json.dumps(res['hanoi'], ensure_ascii=False))
print(json.dumps(res['sierpinski'], ensure_ascii=False))
print(json.dumps(res['parens_sanitize'], ensure_ascii=False))
