"""Chapter 4 browser acceptance at 1440 and 390 px: details, images, players, quizzes, flashcards, overflow."""
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
        page.goto((ROOT / 'linked_lists.html').as_uri(), wait_until='load')
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
        # Players: every case button, step through every frame, then play to the end.
        players = page.evaluate("Object.keys(LLB)")
        frames = 0
        cases = page.locator('button.ll-case')
        for i in range(cases.count()):
            b = cases.nth(i)
            pid = b.get_attribute('data-ll')
            b.click()
            n = page.evaluate("""p=>{const pl=LLP[p];pl.pause&&pl.pause();
                const total=pl.frames.length;let n=0;
                if(pl.i!==0)throw Error('not at frame 0: '+p);
                while(!pl._done && n<=total+1){llStep(p);n++;}
                if(!pl._done)throw Error('stepping did not finish: '+p);
                const txt=document.getElementById(p+'Count').textContent;
                if(!txt.includes(`${total-1} / ${total-1}`))throw Error('count '+p+' '+txt);
                return n;}""", pid)
            frames += n
        # Play one case per player at fastest speed and confirm it finishes.
        for pid in players:
            page.locator(f'button.ll-case[data-ll="{pid}"]').first.click()
            page.evaluate("p=>{document.getElementById(p+'Speed').value=120;llPlay(p);}", pid)
        page.wait_for_function("ps=>ps.every(p=>LLP[p]._done)", arg=players, timeout=30000)
        res['players'] = len(players)
        res['case_buttons'] = cases.count()
        res['frames_stepped'] = frames
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
        page.locator('#variants').screenshot(path=str(OUT / f'linked_lists-variants-{width}.png'))
        page.locator('#unordered').screenshot(path=str(OUT / f'linked_lists-unordered-{width}.png'))
        res['page_errors'] = errors
        assert not errors, errors
        report[str(width)] = res
        page.close()
    browser.close()
(OUT / 'browser-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=1) + '\n')
print(json.dumps(report, ensure_ascii=False))
