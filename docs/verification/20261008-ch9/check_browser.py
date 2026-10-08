"""Chapter 9 browser acceptance at 1440 and 390 px: details, images, every Player-driven widget (step and play),
the lecture heap presets, the book-tree traversal, quizzes, flashcards, horizontal overflow, page errors."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).parent
CHROME = '/home/phonchi/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'
HEAP_LIST = "()=>[...document.querySelectorAll('#heapList .heap-cell')].map(c=>c.lastChild.textContent).join(' ')"


def fast(page, sid):
    page.evaluate("s=>{const e=document.getElementById(s);e.value=e.min;e.dispatchEvent(new Event('input'));}", sid)


def text(page, sid):
    return page.locator('#' + sid).inner_text()


report = {}
with sync_playwright() as p:
    browser = p.chromium.launch(timeout=20000, executable_path=CHROME, headless=True, args=['--no-sandbox'])
    for width in (1440, 390):
        page = browser.new_page(viewport={'width': width, 'height': 1000})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.route('https://**/*', lambda r: r.abort())   # local files only
        page.set_default_timeout(15000)
        page.goto((ROOT / 'trees.html').as_uri(), wait_until='load')
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
        w = {}
        # vocabulary: click a node
        page.locator('#canvas-vocab .t-node').nth(1).click()
        w['vocab_key'] = text(page, 'vocabKey')
        assert w['vocab_key'] != '—'
        # nodes & references: step, then autoplay to the end
        before = text(page, 'nrStatus')
        page.locator('#nrStep').click()
        w['nr_step'] = text(page, 'nrStatus')
        assert w['nr_step'] != before
        fast(page, 'nrSpeed')
        page.locator('#nrPlay').click()
        page.wait_for_function("()=>document.getElementById('nrPlay').textContent.includes('自動播放')", timeout=60000)
        w['nr_nodes'] = page.locator('#canvas-nr .t-node').count()
        # parse tree: step, play, evaluate
        page.locator('#parseStep').click()
        w['parse_step_tok'] = text(page, 'parseTok')
        fast(page, 'parseSpeed')
        page.locator('#parsePlay').click()
        page.wait_for_timeout(6000)
        page.locator('#parseEvalBtn').click()
        page.wait_for_timeout(6000)
        w['parse_result'] = text(page, 'parseResult')
        # traversals: lecture book tree, preorder, step and play
        page.locator('#traversals [data-tree="book"]').click()
        page.locator('#traversals [data-trav="preorder"]').click()
        for _ in range(3):
            page.locator('#travStep').click()
        w['trav_step_status'] = text(page, 'travStatus')
        fast(page, 'travSpeed')
        page.locator('#travPlay').click()
        page.wait_for_function("()=>document.getElementById('travStatus').textContent.includes('完成')", timeout=60000)
        w['book_preorder'] = text(page, 'travOutput')
        w['trav_code_head'] = page.locator('#travCode .line').first.inner_text()
        # heap: three lecture presets, played to the end
        fast(page, 'heapSpeed')
        heap = {'initial': page.evaluate(HEAP_LIST)}
        for demo, done in (('insert', '插入完成'), ('delete', 'delete-min 完成'), ('heapify', 'heapify 完成')):
            page.locator(f'#heap [data-heapdemo="{demo}"]').click()
            page.locator('#heapStep').click()
            page.locator('#heapStep').click()
            heap[demo + '_after_2_steps'] = text(page, 'heapStatus')
            page.locator('#heapPlay').click()
            page.wait_for_function(f"()=>document.getElementById('heapStatus').textContent.includes('{done}')", timeout=60000)
            heap[demo] = page.evaluate(HEAP_LIST)
        assert heap['insert'] == '5 7 11 14 9 19 21 33 17 27 18', heap
        assert heap['delete'] == '9 14 11 17 18 19 21 33 27', heap
        assert heap['heapify'] == '2 3 5 6 9', heap
        w['heap'] = heap
        # BST: put 40 then get 23, stepping
        fast(page, 'bstSpeed')
        page.locator('#bst button[data-bstop="put"]').click()
        page.locator('#bstStep').click()
        page.wait_for_timeout(4000)
        w['bst_put'] = {'size': text(page, 'bstSize'), 'result': text(page, 'bstResult')}
        page.fill('#bstOpKey', '23')
        page.locator('#bst button[data-bstop="get"]').click()
        page.wait_for_timeout(4000)
        w['bst_get'] = text(page, 'bstResult')
        # BST delete: the four presets
        fast(page, 'delSpeed')
        dels = {}
        for k in ('20', '80', '30', '50'):
            page.locator(f'#bst-delete [data-delk="{k}"]').click()
            page.wait_for_timeout(6000)
            dels[k] = {'case': text(page, 'delCase'), 'phase': text(page, 'delPhase')}
        page.locator('#delReset').click()
        page.locator('#delStep').click()
        page.locator('#delStep').click()
        dels['step'] = text(page, 'delStatus')
        page.wait_for_timeout(1500)
        dels['step_is_paused'] = text(page, 'delStatus') == dels['step']
        assert not dels['step'].startswith('已建立') and dels['step_is_paused'], dels
        w['bst_delete'] = dels
        # BST analysis
        page.locator('#bstAnalRegen').click()
        w['bst_heights'] = [text(page, 'bstRandH'), text(page, 'bstSortedH')]
        # AVL: each case, step then play
        fast(page, 'avlSpeed')
        avl = {}
        for c in ('LL', 'RR', 'LR', 'RL'):
            page.locator(f'#avl [data-avlcase="{c}"]').click()
            page.locator('#avlStep').click()
            s1 = text(page, 'avlPhase')
            page.locator('#avlPlay').click()
            page.wait_for_timeout(5000)
            avl[c] = {'after_step': s1, 'final': text(page, 'avlStatus')}
        w['avl'] = avl
        res['widgets'] = w
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
        page.locator('#heap').screenshot(path=str(OUT / f'trees-heap-{width}.png'))
        page.locator('#traversals').screenshot(path=str(OUT / f'trees-traversals-{width}.png'))
        res['page_errors'] = errors
        assert not errors, errors
        report[str(width)] = res
        page.close()
    browser.close()
(OUT / 'browser-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=1) + '\n')
print(json.dumps(report, ensure_ascii=False))
