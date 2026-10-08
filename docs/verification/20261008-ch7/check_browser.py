"""Chapter 7 browser acceptance at 1440 and 390 px: details, images, Animator panels, hash panel,
quizzes, flashcards, horizontal overflow, page errors."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).parent
CHROME = '/home/phonchi/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'
PANELS = ['seq', 'bin', 'bubble', 'sel', 'ins', 'shell', 'merge', 'quick']
STAT = {'seq': 'seqCmp', 'bin': 'binCmp', 'bubble': 'bubbleCmp', 'sel': 'selCmp', 'ins': 'insCmp',
        'shell': 'shellCmp', 'merge': 'mergeCmp', 'quick': 'quickCmp'}
report = {}
with sync_playwright() as p:
    browser = p.chromium.launch(timeout=20000, executable_path=CHROME, headless=True, args=['--no-sandbox'])
    for width in (1440, 390):
        page = browser.new_page(viewport={'width': width, 'height': 1000})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.route('https://**/*', lambda r: r.abort())   # local files only
        page.set_default_timeout(15000)
        page.goto((ROOT / 'searching_sorting.html').as_uri(), wait_until='load')
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
        # Animator panels: step from a fresh state (no ▶ first), check the code highlight, reset, apply, play to the end.
        panels = {}
        for pid in PANELS:
            r = {}
            page.locator(f'#{pid}Reset').click()
            before = page.locator(f'#{pid}Status').inner_text()
            for _ in range(5):
                page.locator(f'#{pid}Step').click()
            r['status_after_step'] = page.locator(f'#{pid}Status').inner_text()
            r['cmp_after_5_steps'] = page.locator('#' + STAT[pid]).inner_text()
            r['active_code_line'] = page.locator(f'#{pid}Code .line.active').count()
            assert r['status_after_step'] != before or r['cmp_after_5_steps'] != '0', (pid, r)
            page.locator(f'#{pid}Reset').click()
            r['cmp_after_reset'] = page.locator('#' + STAT[pid]).inner_text()
            page.locator(f'#{pid}Apply').click()
            page.evaluate("p=>{const s=document.getElementById(p+'Speed');s.value=s.min;}", pid)
            page.locator(f'#{pid}Play').click()
            page.wait_for_function("p=>document.getElementById(p+'Play').textContent.includes('重播')", arg=pid, timeout=120000)
            r['final_status'] = page.locator(f'#{pid}Status').inner_text()
            panels[pid] = r
        res['panels'] = panels
        # Preset toggles (shell gaps, quick pivot) regenerate without errors.
        page.locator('[data-gap="2k-1"]').click()
        page.locator('#shellStep').click()
        page.locator('[data-pivot="median"]').click()
        page.locator('#quickStep').click()
        # Hash panel.
        page.locator('#hashClear').click()
        page.locator('#hashBatchInsert').click()
        page.wait_for_function("()=>document.getElementById('hashUsed').textContent.trim().startsWith('6 ')", timeout=60000)
        page.wait_for_timeout(1500)
        page.fill('#hashVal', '44')
        page.locator('#hashInsert').click()
        page.wait_for_function("()=>document.getElementById('hashUsed').textContent.trim().startsWith('7 ')", timeout=30000)
        page.wait_for_timeout(1500)
        res['hash'] = {'linear_used': page.locator('#hashUsed').inner_text(), 'insert_status': page.locator('#hashStatus').inner_text()}
        page.fill('#hashVal', '44')
        page.locator('#hashSearch').click()
        page.wait_for_timeout(3000)
        res['hash']['search_status'] = page.locator('#hashStatus').inner_text()
        res['hash']['search_ops'] = page.locator('#hashOps').inner_text()
        page.locator('[data-strategy="chain"]').click()
        page.locator('#hashBatchInsert').click()
        page.wait_for_function("()=>document.getElementById('hashUsed').textContent.trim().startsWith('6 ')", timeout=60000)
        res['hash']['chain_used'] = page.locator('#hashUsed').inner_text()
        # Quizzes (sq-item): a wrong answer then the right one; feedback must show.
        items = page.locator('.sq-item')
        for i in range(items.count()):
            it = items.nth(i)
            assert it.locator('.sq-opt').count() == 4
            it.locator('.sq-opt[data-c="0"]').first.click()
            assert 'wrong' in it.locator('.sq-opt[data-c="0"]').first.get_attribute('class')
            assert it.locator('.sq-fb').inner_text().strip(), i
            it.locator('.sq-opt[data-c="1"]').click()
            assert 'correct' in it.locator('.sq-opt[data-c="1"]').get_attribute('class')
        res['quizzes'] = items.count()
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
        page.locator('#hashing').screenshot(path=str(OUT / f'searching_sorting-hashing-{width}.png'))
        page.locator('#quick').screenshot(path=str(OUT / f'searching_sorting-quick-{width}.png'))
        res['page_errors'] = errors
        assert not errors, errors
        report[str(width)] = res
        page.close()
    browser.close()
(OUT / 'browser-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=1) + '\n')
print(json.dumps(report, ensure_ascii=False))
