"""Chapter 6 browser acceptance at 1440 and 390 px: details, images, players, quizzes, flashcards, overflow."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).parent
CHROME = '/home/phonchi/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'
report = {}
with sync_playwright() as p:
    browser = p.chromium.launch(timeout=20000, executable_path=CHROME, headless=True, args=['--no-sandbox'])
    for width in (1440, 390):
        page = browser.new_page(viewport={'width': width, 'height': 1000})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.route('https://**/*', lambda r: r.abort())   # local files only
        page.set_default_timeout(15000)
        page.goto((ROOT / 'recursion.html').as_uri(), wait_until='load')
        res = {}
        # Expand every details element.
        dets = page.locator('details')
        res['details'] = dets.count()
        for i in range(dets.count()):
            d = dets.nth(i)
            if not d.evaluate('e=>e.open'):
                d.locator(':scope > summary').click()
            assert d.evaluate('e=>e.open'), i
        # Images: load all and check natural size.
        res['images'] = page.locator('img').evaluate_all(
            "async xs=>{const bad=[];for(const im of xs){im.loading='eager';try{await im.decode();}catch(e){}"
            "if(!im.naturalWidth)bad.push(im.getAttribute('src'));}return {count:xs.length,broken:bad};}")
        assert not res['images']['broken'], res['images']
        # Players (player-v2): start, then rewind and single-step every frame; check the highlighted code line.
        PLAYERS = {'sum': 'sumCode', 'tostr': 'tostrCode', 'tsf': 'tsfCode', 'frame': None,
                   'hanoi': 'hanoiCode', 'maze': 'mazeCode', 'dp': 'dpCode'}
        stepped = {}
        for pid, code in PLAYERS.items():
            page.locator(f'button[onclick="{pid}Start()"]').click()
            stepped[pid] = page.evaluate("""([p, code])=>{const pl=eval(p+'Player');pl.pause();
                pl.i=-1;pl._done=false;const total=pl.frames.length;let n=0;
                while(!pl._done && n<=total+1){pl.step();n++;
                  if(code && pl.frames[pl.i] && pl.frames[pl.i].line!=null &&
                     !document.querySelector('#'+code+' .line.active'))throw Error('no active line '+p+' frame '+pl.i);}
                if(!pl._done || pl.i!==total-1)throw Error('stepping did not finish: '+p);
                return total;}""", [pid, code])
        for pid in PLAYERS:
            page.evaluate("p=>{document.getElementById(p+'Speed').value=document.getElementById(p+'Speed').min;eval(p+'Start')();}", pid)
        page.wait_for_function("ps=>ps.every(p=>eval(p+'Player')._done)", arg=list(PLAYERS), timeout=60000)
        res['players'] = stepped
        # Pause button toggles a running player.
        page.locator('button[onclick="hanoiStart()"]').click()
        page.locator('button[onclick="hanoiPlayer &amp;&amp; hanoiPlayer.toggle(this)"], button[onclick="hanoiPlayer && hanoiPlayer.toggle(this)"]').click()
        assert page.evaluate('hanoiPlayer.playing') is False
        # Canvases: redraw and confirm pixels were painted.
        page.evaluate("()=>{spiralStart();document.getElementById('treeDepth').value=5;treeDraw();"
                      "document.getElementById('sierDeg').value=4;sierDraw();}")
        res['canvas_painted'] = page.evaluate("""()=>['spiralCv','treeCv','sierCv'].map(id=>{const c=document.getElementById(id);
            const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let k=0;
            for(let i=3;i<d.length;i+=4)if(d[i])k++;return [id,k];})""")
        assert all(k > 100 for _, k in res['canvas_painted']), res['canvas_painted']
        res['status_text'] = {i: page.locator('#' + i + ' .status-text').inner_text() for i in ('vizStatus', 'sierStatus', 'tsfStatus', 'dpStatus')}
        # Quizzes: wrong then right, feedback text must appear.
        qs = page.locator('.quiz-options')
        for i in range(qs.count()):
            q = qs.nth(i)
            assert q.locator('.quiz-opt').count() == 4
            assert q.locator('[data-correct="true"]').count() == 1
            q.locator('[data-correct="false"]').first.click()
            fb = page.locator('#' + q.get_attribute('id').replace('Options', 'Feedback'))
            assert fb.inner_text().strip(), i
            q.locator('[data-correct="true"]').click()
            assert 'correct' in q.locator('[data-correct="true"]').get_attribute('class')
        res['quizzes'] = qs.count()
        # Flashcards.
        cards = page.locator('#fcGrid .fc-card')
        res['flashcards'] = cards.count()
        cards.first.click()
        assert 'flipped' in cards.first.get_attribute('class')
        page.locator('#fcFlipAll').click()
        page.locator('#fcUnflip').click()
        page.locator('#fcShuffle').click()
        assert cards.count() == res['flashcards']
        # Overflow.
        page.wait_for_timeout(200)
        res['scrollWidth'] = page.evaluate('document.documentElement.scrollWidth')
        res['innerWidth'] = page.evaluate('innerWidth')
        res['overflow'] = res['scrollWidth'] > res['innerWidth'] + 1
        assert not res['overflow'], res
        page.locator('#frames').screenshot(path=str(OUT / f'recursion-frames-{width}.png'))
        page.locator('#dp').screenshot(path=str(OUT / f'recursion-dp-{width}.png'))
        res['page_errors'] = errors
        assert not errors, errors
        report[str(width)] = res
        page.close()
    browser.close()
(OUT / 'browser-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=1) + '\n')
print(json.dumps(report, ensure_ascii=False))
