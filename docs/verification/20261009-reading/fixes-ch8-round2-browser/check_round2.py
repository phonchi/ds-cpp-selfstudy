"""Round-2 reader fixes for graphs.html: step-from-load and gating for topsort/SCC, knight 5x5 and 7x7 starts,
Prim stale-entry highlight, Dijkstra wording, DFS root selector note. Writes round2-results.json next to this file."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).parent
CHROME = '/home/phonchi/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'
res = {}


def fresh(browser):
    page = browser.new_page(viewport={'width': 1440, 'height': 1000})
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.route('https://**/*', lambda r: r.abort())
    page.set_default_timeout(15000)
    page.goto((ROOT / 'graphs.html').as_uri(), wait_until='load')
    return page, errors


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME, headless=True, args=['--no-sandbox'])

    # ---------------- topological sort
    page, errors = fresh(browser)
    step = page.locator('#topsort button', has_text='單步')
    order = page.locator('#topsort button', has_text='②')
    step.click()
    ts = {'after_first_step_i': page.evaluate('tsPlayer && tsPlayer.i'),
          'after_first_step_playing': page.evaluate('tsPlayer.playing'),
          'status_1': page.locator('#tsStatus').inner_text()}
    step.click(); step.click()
    order.click()
    ts['blocked_status'] = page.locator('#tsStatus').inner_text()
    ts['blocked_out'] = page.locator('#tsOrderOut').inner_text()
    ts['i_after_block'] = page.evaluate('tsPlayer.i')
    n = 0
    while not page.evaluate('tsDfsComplete()'):
        step.click(); n += 1
    ts['steps_to_finish'] = n + 3
    ts['frames'] = page.evaluate('tsPlayer.frames.length')
    page.evaluate("document.getElementById('tsSpeed').value=150")
    order.click()
    page.wait_for_function('()=>tsPlayer._done', timeout=30000)
    ts['order'] = page.locator('#tsOrderOut').inner_text()
    ts['final_status'] = page.locator('#tsStatus').inner_text()
    ts['page_errors'] = errors
    assert ts['after_first_step_i'] == 0 and not ts['after_first_step_playing'], ts
    assert '還沒播完' in ts['blocked_status'] and ts['blocked_out'] == '' and ts['i_after_block'] == 2, ts
    assert ts['steps_to_finish'] == ts['frames'] == 18, ts
    assert ts['order'].count('→') == 8 and not errors, ts
    res['topsort'] = ts
    page.close()

    # ---------------- SCC
    page, errors = fresh(browser)
    step = page.locator('#scc button', has_text='單步')
    b2 = page.locator('#scc button', has_text='② 轉置')
    b3 = page.locator('#scc button', has_text='③')
    step.click()
    sc = {'after_first_step_i': page.evaluate('sccPlayer && sccPlayer.i'),
          'status_1': page.locator('#sccStatus').inner_text()}
    for _ in range(4):
        step.click()
    b2.click()
    sc['blocked2_status'] = page.locator('#sccStatus').inner_text()
    b3.click()
    sc['blocked3_status'] = page.locator('#sccStatus').inner_text()
    sc['onGT_after_block'] = page.evaluate('sccOnGT')
    sc['sccOut_after_block'] = page.locator('#sccOut').inner_text()
    n = 0
    while not page.evaluate('sccDfsComplete()'):
        step.click(); n += 1
    sc['phase1_steps'] = n + 5
    b2.click()
    sc['onGT'] = page.evaluate('sccOnGT')
    step.click()   # player is null after the transpose: step builds phase 3 and advances one frame
    sc['phase3_first_i'] = page.evaluate('sccPlayer && sccPlayer.i')
    n = 1
    while not page.evaluate('sccPlayer._done'):
        step.click(); n += 1
    sc['phase3_clicks'] = n
    sc['out'] = page.locator('#sccOut').inner_text()
    sc['final_status'] = page.locator('#sccStatus').inner_text()
    sc['page_errors'] = errors
    assert sc['after_first_step_i'] == 0, sc
    assert '還沒播完' in sc['blocked2_status'] and '還沒播完' in sc['blocked3_status'], sc
    assert sc['onGT_after_block'] is False and sc['sccOut_after_block'] == '', sc
    assert sc['phase1_steps'] == 16 and sc['onGT'] and sc['phase3_first_i'] == 0, sc
    assert sc['out'].count('SCC') == 3 and '3 個強連通元件' in sc['final_status'] and not errors, sc
    res['scc'] = sc
    page.close()

    # ---------------- knight
    page, errors = fresh(browser)
    kn = {'default_size': page.evaluate("document.getElementById('knightSize').value"),
          'ctrl_size': page.evaluate('knightCtrl.size'),
          'stat_label': page.locator('#knightSteps').locator('xpath=..').locator('.stat-label').inner_text()}
    starts = {}
    for n in (5, 6, 7, 8):
        page.evaluate(f"()=>{{const s=document.getElementById('knightSize');s.value='{n}';s.dispatchEvent(new Event('change'));}}")
        starts[n] = page.evaluate("[...document.querySelectorAll('#knightStart option')].map(o=>o.textContent)")
    kn['starts'] = starts
    seven_odd = [t for t in starts[7] if sum(int(x) for x in t.strip('()').split(',')) % 2]
    five_odd = [t for t in starts[5] if sum(int(x) for x in t.strip('()').split(',')) % 2]
    page.evaluate("()=>{const s=document.getElementById('knightSize');s.value='5';s.dispatchEvent(new Event('change'));"
                  "const e=document.getElementById('knightSpeed');e.value=e.min;}")
    for heur in (True, False):
        page.evaluate(f"()=>{{knightCtrl.useHeur={'true' if heur else 'false'};knightCtrl.reset();}}")
        page.locator('#knightPlay').click()
        page.wait_for_function('()=>knightCtrl.steps.length>0 && knightCtrl.idx>=3', timeout=30000)
        page.evaluate('knightCtrl.stop()')
        # highlight on a move frame and a start frame
        cur = page.evaluate('knightCtrl.steps[knightCtrl.idx-1].kind')
        active = page.evaluate("(document.querySelector('#knightCode .line.active')||{}).dataset?.l")
        first_cell = page.evaluate("document.getElementById('cell-0-0').innerText.trim()")
        page.evaluate('()=>{knightCtrl.idx=knightCtrl.steps.length-1;knightCtrl.step();}')
        nums = page.evaluate("[...document.querySelectorAll('#knightBoard .step-num')].map(e=>+e.textContent).sort((a,b)=>a-b)")
        r = {'frames': page.evaluate('knightCtrl.steps.length'),
             'back': page.locator('#knightBack').inner_text(),
             'result': page.locator('#knightResult').inner_text(),
             'cells_walked': page.locator('#knightSteps').inner_text(),
             'start_cell': page.evaluate("document.getElementById('cell-0-0').innerText.trim()"),
             'numbers_are_0_to_24': nums == list(range(25)),
             'midrun_kind': cur, 'midrun_active_line': active, 'midrun_start_cell': first_cell,
             'final_active_line': page.evaluate("(document.querySelector('#knightCode .line.active')||{}).dataset?.l")}
        kn['warnsdorff' if heur else 'plain'] = r
        assert 'SUCCESS' in r['result'] and r['cells_walked'] == '25' and r['start_cell'] == '0' and r['numbers_are_0_to_24'], r
        assert r['midrun_active_line'] in ('3', '10', '14') and r['final_active_line'] == '19', r
    # the limit message on 6x6 (3,3) without Warnsdorff
    page.evaluate("()=>{const s=document.getElementById('knightSize');s.value='6';s.dispatchEvent(new Event('change'));"
                  "document.getElementById('knightStart').value=String(3*6+3);knightCtrl.useHeur=false;knightCtrl.reset();}")
    page.locator('#knightPlay').click()
    page.wait_for_function('()=>knightCtrl.steps.length>0 && knightCtrl.idx>=1', timeout=60000)
    page.evaluate('()=>{knightCtrl.stop();knightCtrl.idx=knightCtrl.steps.length-1;knightCtrl.step();}')
    kn['limit_6x6_plain'] = {'status': page.locator('#knightStatus').inner_text(),
                             'result': page.locator('#knightResult').inner_text()}
    kn['page_errors'] = errors
    assert kn['default_size'] == '5' and kn['ctrl_size'] == 5 and kn['stat_label'] == '已走格數', kn
    assert not seven_odd and not five_odd and len(starts[7]) == 4, kn
    assert '改用 Warnsdorff' not in kn['limit_6x6_plain']['status'] and '上限' in kn['limit_6x6_plain']['status'], kn
    assert not errors, errors
    res['knight'] = kn
    page.close()

    # ---------------- Prim stale-entry highlight
    page, errors = fresh(browser)
    page.evaluate("primCtrl.generate(document.getElementById('primStart').value)")
    stale_idx = page.evaluate("primCtrl.steps.map((s,i)=>s.kind==='stale'?i:-1).filter(i=>i>=0)")
    pr = {'stale_frames': stale_idx, 'highlights': []}
    for i in stale_idx:
        page.evaluate(f"()=>{{primCtrl.idx={i};primCtrl.step();}}")
        el = page.locator('#primCode .line.active')
        pr['highlights'].append([el.get_attribute('data-l'), el.inner_text().strip()])
    pr['page_errors'] = errors
    assert stale_idx and all(h[0] == '9' and 'continue' in h[1] for h in pr['highlights']), pr
    res['prim'] = pr
    page.close()

    # ---------------- Dijkstra wording
    page, errors = fresh(browser)
    page.locator('#dijStep').click()
    page.locator('#dijStep').click()
    dj = {'status_after_pop': page.locator('#dijStatus').inner_text(),
          'table_header': page.locator('#dijTable thead').inner_text()}
    page.evaluate("dijCtrl.generate(dijCtrl.start||'u')")
    msgs = page.evaluate("dijCtrl.steps.map(s=>s.msg).join('\\n')")
    dj['visited_in_messages'] = 'visited' in msgs
    dj['page_errors'] = errors
    assert '展開它的鄰居' in dj['status_after_pop'] and '已展開' in dj['table_header'], dj
    assert 'visited' not in dj['table_header'] and not dj['visited_in_messages'], dj
    res['dijkstra'] = dj
    page.close()

    # ---------------- DFS root selector
    page, errors = fresh(browser)
    df = {'label': page.locator('#dfs .slider-label').first.inner_text(),
          'note_visible': page.locator('#dfs p', has_text='依 key 的順序').is_visible()}
    page.select_option('#dfsStart', 'C')
    page.locator('#dfsStep').click()
    df['first_status_with_C'] = page.locator('#dfsStatus').inner_text()
    df['page_errors'] = errors
    assert df['label'] == '第一棵樹的根' and df['note_visible'] and not errors, df
    res['dfs'] = df
    page.close()
    browser.close()

(OUT / 'round2-results.json').write_text(json.dumps(res, ensure_ascii=False, indent=1) + '\n')
print(json.dumps(res, ensure_ascii=False, indent=1))
