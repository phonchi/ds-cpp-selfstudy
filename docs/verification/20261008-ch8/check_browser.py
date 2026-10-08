"""Chapter 8 browser acceptance at 1440 and 390 px: details, images, the ten widgets, quizzes, flashcards, overflow."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).parent
CHROME = '/home/phonchi/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'
# controller variable, code panel id (None: no line highlighting), play/step/reset button ids
CTRLS = {'bfsCtrl': ('bfsCode', 'bfs'), 'wlCtrl': (None, 'wl'), 'dfsCtrl': ('dfsCode', 'dfs'),
         'dijCtrl': ('dijCode', 'dij'), 'primCtrl': ('primCode', 'prim')}
report = {}
with sync_playwright() as p:
    browser = p.chromium.launch(timeout=20000, executable_path=CHROME, headless=True, args=['--no-sandbox'])
    import os
    for width in [int(w) for w in os.environ.get('WIDTHS', '1440,390').split(',')]:
        page = browser.new_page(viewport={'width': width, 'height': 1000})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.route('https://**/*', lambda r: r.abort())   # local files only
        page.set_default_timeout(15000)
        page.goto((ROOT / 'graphs.html').as_uri(), wait_until='load')
        res = {}
        dets = page.locator('details')
        res['details'] = dets.count()
        for i in range(dets.count()):
            d = dets.nth(i)
            if not d.evaluate('e=>e.open'):
                d.locator(':scope > summary').click()
            assert d.evaluate('e=>e.open'), i
        res['images'] = page.locator('img').evaluate_all(
            "async xs=>{const bad=[];for(const im of xs){im.loading='eager';try{await im.decode();}catch(e){}"
            "if(!im.naturalWidth)bad.push(im.getAttribute('src'));}return {count:xs.length,broken:bad};}")
        assert not res['images']['broken'], res['images']

        # Static widgets: terminology highlight and representation highlight.
        page.evaluate("()=>{introHighlight('path');introHighlight('cycle');introHighlight('clear');adjHighlight('v3');}")
        res['adj_highlight'] = page.evaluate("()=>document.querySelectorAll('#adjMatrixViz .hl, #adjMatrixViz [class*=\"hl\"], #adjListViz [class*=\"hl\"]').length")

        # Step-through controllers: click the step button until the last step, checking the code line.
        stepped = {}
        for ctrl, (code, pre) in CTRLS.items():
            page.locator(f'#{pre}Reset').click()
            n = 0
            while True:
                page.locator(f'#{pre}Step').click()
                n += 1
                st = page.evaluate(f"()=>{{const c={ctrl};const s=c.steps[c.idx-1];return [c.idx,c.steps.length,s?s.codeLine:null];}}")
                if code and st[2] is not None:
                    assert page.locator(f'#{code} .line.active').count() == 1, (ctrl, n)
                    assert page.locator(f'#{code} .line.active').get_attribute('data-l') == str(st[2]), (ctrl, n)
                if st[0] >= st[1]:
                    break
                assert n < 500, ctrl
            stepped[ctrl] = n
        # Then play each one at the fastest speed until it stops by itself.
        for ctrl, (code, pre) in CTRLS.items():
            page.evaluate(f"()=>{{const e=document.getElementById('{pre}Speed');e.value=e.min;{ctrl}.reset();}}")
            page.locator(f'#{pre}Play').click()
        page.wait_for_function("cs=>cs.every(c=>{const x=eval(c);return !x.playing && x.idx>=x.steps.length && x.steps.length>0;})",
                               arg=list(CTRLS), timeout=90000)
        res['controllers_stepped'] = stepped
        # Knight's tour: play (no step button by design), both with and without the heuristic on 5x5.
        knight = {}
        for heur in (True, False):
            page.evaluate(f"()=>{{document.getElementById('knightSize').value='5';"
                          "document.getElementById('knightSize').dispatchEvent(new Event('change'));"
                          f"knightCtrl.useHeur={'true' if heur else 'false'};knightCtrl.reset();"
                          "const e=document.getElementById('knightSpeed');e.value=e.min;}")
            page.locator('#knightPlay').click()
            page.wait_for_function("()=>knightCtrl.steps.length>0 && knightCtrl.idx>=1", timeout=30000)
            if not heur:
                # Plain DFS on 5x5 backtracks thousands of times: watch it play a while, then jump to the last step.
                page.wait_for_function("()=>knightCtrl.idx>=20", timeout=30000)
                page.evaluate("()=>{knightCtrl.stop();knightCtrl.idx=knightCtrl.steps.length-1;knightCtrl.step();}")
            page.wait_for_function("()=>!knightCtrl.playing && knightCtrl.idx>=knightCtrl.steps.length", timeout=120000)
            knight['warnsdorff' if heur else 'plain'] = [page.evaluate('knightCtrl.steps.length'),
                                                         page.locator('#knightResult').inner_text()]
        res['knight'] = knight
        # Topological sort and SCC (player-v2): run each phase at the fastest speed; single-step works.
        page.evaluate("()=>{for(const id of ['tsSpeed','sccSpeed']){const e=document.getElementById(id);e.value=e.min;}}")
        page.evaluate('tsRunDFS()')
        page.evaluate('tsPlayer.pause()')
        i0 = page.evaluate('tsPlayer.i')
        page.locator('#topsort button', has_text='單步').click()
        assert page.evaluate('tsPlayer.i') == i0 + 1
        page.evaluate('tsPlayer.play()')
        page.wait_for_function('()=>tsPlayer._done', timeout=30000)
        page.evaluate('tsOrder()')
        page.wait_for_function('()=>tsPlayer._done', timeout=30000)
        res['topsort_order'] = page.locator('#tsOrderOut').inner_text()
        for step in ('sccStep1', 'sccStep2', 'sccStep3'):
            page.evaluate(f'{step}()')
            page.wait_for_function('()=>!sccPlayer || sccPlayer._done', timeout=30000)
        page.locator('#scc button', has_text='暫停').click()
        res['scc_out'] = page.locator('#sccOut').inner_text()
        assert res['topsort_order'] and res['scc_out'], res
        # Quizzes: wrong then right, feedback text must appear.
        qs = page.locator('.quiz-options')
        for i in range(qs.count()):
            q = qs.nth(i)
            assert q.locator('.quiz-opt').count() == 4
            assert q.locator('[data-correct="true"]').count() == 1
            q.locator('[data-correct="false"]').first.click()
            fb = page.locator('#' + q.get_attribute('id').replace('Options', 'Feedback'))
            assert '不對' in fb.inner_text(), i
            q.locator('[data-correct="true"]').click()
            assert '正確' in fb.inner_text(), i
        res['quizzes'] = qs.count()
        bq = page.locator('#bankquiz .sq-item')
        for i in range(bq.count()):
            bq.nth(i).locator('.sq-opt[data-c="1"]').click()
            assert bq.nth(i).locator('.sq-fb').inner_text().strip(), i
        res['bankquiz'] = bq.count()
        cards = page.locator('#fcGrid .fc-card')
        res['flashcards'] = cards.count()
        cards.first.click()
        assert 'flipped' in cards.first.get_attribute('class')
        page.locator('#fcFlipAll').click()
        page.locator('#fcUnflip').click()
        page.locator('#fcShuffle').click()
        assert cards.count() == res['flashcards']
        page.wait_for_timeout(200)
        res['scrollWidth'] = page.evaluate('document.documentElement.scrollWidth')
        res['innerWidth'] = page.evaluate('innerWidth')
        res['overflow'] = res['scrollWidth'] > res['innerWidth'] + 1
        res['overflow_elements'] = page.evaluate("""()=>{const out=[];for(const e of document.querySelectorAll('body *')){const r=e.getBoundingClientRect();
          if(r.right>innerWidth && r.width>0){let a=e.parentElement,clip=false;while(a&&a!==document.body){if(getComputedStyle(a).overflowX!=='visible'){clip=true;break;}a=a.parentElement;}
          if(!clip)out.push(e.tagName+'#'+e.id+'.'+String(e.className).slice(0,40)+' '+r.right.toFixed(1));}}return out.slice(0,10);}""")
        assert not res['overflow'], res
        page.locator('#knight').screenshot(path=str(OUT / f'graphs-knight-{width}.png'))
        page.locator('#dijkstra').screenshot(path=str(OUT / f'graphs-dijkstra-{width}.png'))
        res['page_errors'] = errors
        assert not errors, errors
        report[str(width)] = res
        page.close()
    browser.close()
(OUT / 'browser-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=1) + '\n')
print(json.dumps(report, ensure_ascii=False))
