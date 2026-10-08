"""Chapter 5 browser acceptance at 1440 and 390 px: details, images, players, widgets, quizzes, flashcards, overflow."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).parent
CHROME = '/home/phonchi/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'

# (player variable, how to start one case, code panel id or None)
CASES = [
    ('introPlayer', "introStart()", None),
    ('parPlayer', "parStart()", 'parCode'),
    ('parPlayer', "parLoad('(()')", 'parCode'),
    ('parPlayer', "parLoad('())(')", 'parCode'),
    ('parPlayer', "($('parInput').value='[{()]', parStart())", 'parCode'),
    ('basePlayer', "($('baseSel').value='2', baseStart())", 'baseCode'),
    ('basePlayer', "($('baseSel').value='8', baseStart())", 'baseCode'),
    ('basePlayer', "($('baseSel').value='16', baseStart())", 'baseCode'),
    ('i2pPlayer', "($('i2pSel').selectedIndex=0, i2pStart())", 'i2pCode'),
    ('i2pPlayer', "($('i2pSel').selectedIndex=1, i2pStart())", 'i2pCode'),
    ('i2pPlayer', "($('i2pSel').selectedIndex=2, i2pStart())", 'i2pCode'),
    ('pevalPlayer', "pevalStart()", 'pevalCode'),
    ('hpPlayer', "hpStart()", 'hpCode'),
    ('palPlayer', "($('palInput').value='radar', palStart())", 'palCode'),
    ('palPlayer', "($('palInput').value='lsdkjfskf', palStart())", 'palCode'),
]

STEP_JS = """([v, start, code]) => {
  eval(start);
  const pl = eval(v);
  pl.pause(); pl.reset();
  const total = pl.frames.length; let n = 0, active = false;
  while (!pl._done && n <= total + 1) {
    pl.step(); n++;
    if (code && document.querySelector('#' + code + ' .line.active')) active = true;
  }
  if (!pl._done || pl.i !== total - 1) throw Error('stepping did not finish: ' + start);
  return {frames: total, steps: n, codeHighlighted: active};
}"""

report = {}
with sync_playwright() as p:
    browser = p.chromium.launch(timeout=20000, executable_path=CHROME, headless=True, args=['--no-sandbox'])
    for width in (1440, 390):
        page = browser.new_page(viewport={'width': width, 'height': 1000})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.route('https://**/*', lambda r: r.abort())   # local files only
        page.set_default_timeout(15000)
        page.goto((ROOT / 'linear_structures.html').as_uri(), wait_until='load')
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
        # Players: step every case from frame 0 to the end; code panels must highlight a line.
        cases = []
        for var, start, code in CASES:
            r = page.evaluate(STEP_JS, [var, start, code])
            if code:
                assert r['codeHighlighted'], (start, r)
            cases.append({'case': start, **r})
        res['player_cases'] = cases
        # Play every player at the fastest speed and wait until it finishes.
        for var, start, _ in CASES:
            page.evaluate("([v, start]) => { eval(start); const pl = eval(v); pl.setDelay(20); pl.reset(); pl.play(); }", [var, start])
            page.wait_for_function("v => eval(v)._done", arg=var, timeout=30000)
        res['played'] = len(CASES)
        # Pause / continue toggle on one player.
        page.evaluate("hpStart()")
        page.evaluate("hpPlayer.toggle(); hpPlayer.toggle();")
        # Interactive widgets without a player.
        res['stack_widget'] = page.evaluate("""() => {
          const n0 = $('stackVis').querySelectorAll('.bs-item').length;
          $('stackInput').value = '9'; stackPush();
          const n1 = $('stackVis').querySelectorAll('.bs-item').length;
          stackPeek(); const peek = $('stackStatus').textContent;
          stackPop(); const n2 = $('stackVis').querySelectorAll('.bs-item').length;
          stackReset();
          return {before: n0, afterPush: n1, afterPop: n2, peek};
        }""")
        sw = res['stack_widget']
        assert sw['afterPush'] == sw['before'] + 1 and sw['afterPop'] == sw['before'] and '9' in sw['peek'], sw
        res['queue_widget'] = page.evaluate("""() => {
          const cnt = () => $('queueVis').querySelectorAll('.bq-item, .bq-cell, div').length;
          const n0 = cnt(); $('queueInput').value = 'cat'; queueEnq(); const n1 = cnt();
          const txt = $('queueVis').textContent; queueDeq(); const n2 = cnt(); queueReset();
          return {before: n0, afterPush: n1, afterPop: n2, hasCat: txt.includes('cat')};
        }""")
        qw = res['queue_widget']
        assert qw['afterPush'] > qw['before'] and qw['afterPop'] < qw['afterPush'] and qw['hasCat'], qw
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
        assert not res['overflow'], res
        page.locator('#stack').screenshot(path=str(OUT / f'linear_structures-stack-{width}.png'))
        page.locator('#infix').screenshot(path=str(OUT / f'linear_structures-infix-{width}.png'))
        res['page_errors'] = errors
        assert not errors, errors
        report[str(width)] = res
        page.close()
    browser.close()
(OUT / 'browser-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=1) + '\n')
print(json.dumps({w: {k: v for k, v in r.items() if k != 'player_cases'} for w, r in report.items()}, ensure_ascii=False))
