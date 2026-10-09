"""Chapter 7 round-2 check: from a fresh load, single-step every changed Animator panel frame by frame.
Each frame's status message must match the highlighted code line; at the end, 單步 must leave the frame unchanged."""
import json, re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).parent
CHROME = '/home/phonchi/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'

# (message regex, substring the active line must contain; None = no active line)
RULES = {
 'quick': [
  (r'^初始：呼叫 quickSortHelper', 'void quickSortHelper'),
  (r'三者取中|中位數搬到', 'median-of-three'),
  (r'^pivotVal = a\[', 'int pivotVal = a[first]'),
  (r'^leftMark = first \+ 1', 'int leftMark = first + 1'),
  (r'leftMark (右移|停下)', 'a[leftMark] <= pivotVal'),
  (r'rightMark (左移|停下)', 'a[rightMark] >= pivotVal'),
  (r'done = true', 'if (rightMark < leftMark)'),
  (r'rightMark ≥ leftMark → 交換', 'else swap(a[leftMark], a[rightMark])'),
  (r'pivot 歸位', 'swap(a[first], a[rightMark])'),
  (r'排序完成', None)],
 'shell': [
  (r'^gap = a\.size\(\) / 2', 'int gap = a.size() / 2'),
  (r'^gap = 不超過 n=\d+ 的最大 2\^k−1', 'largestHibbardGap'),
  (r'^while \(gap > 0\)', 'while (gap > 0)'),
  (r'^for \(start = 0', 'for (int start = 0; start < gap; ++start)'),
  (r'^gapInsertionSort\(a, \d+, \d+\)', 'gapInsertionSort(a, start, gap);'),
  (r'^for \(i = ', 'for (int i = start + gap'),
  (r'^curVal = a\[', 'int curVal = a[i]'),
  (r'^curPos = i', 'int curPos = i'),
  (r'^while：', 'while (curPos >= gap'),
  (r'（位移）$', 'a[curPos] = a[curPos-gap]'),
  (r'^curPos -= gap', 'curPos -= gap'),
  (r'^a\[\d+\] = curVal', 'a[curPos] = curVal'),
  (r'^gap /= 2', 'gap /= 2'),
  (r'排序完成', 'void shellSort')],
 'sel': [
  (r'^初始陣列', 'void selectionSort'),
  (r'初始 maxPos = 0', 'int maxPos = 0'),
  (r'^比較 a\[', 'if (a[j] > a[maxPos])'),
  (r'^更大！更新 maxPos', 'maxPos = j'),
  (r'!= fill .* 交換', 'swap(a[maxPos], a[fill])'),
  (r'^maxPos == fill', 'if (maxPos != fill)'),
  (r'結束：a\[\d+\]=\d+ 已就位，--fill', 'for (int fill'),
  (r'排序完成', 'void selectionSort')],
 'bin': [
  (r'^對已排序陣列', 'int last ='),
  (r'^midpoint = \d+ \+ \(\d+ - \d+\) / 2 = \d+', 'int midpoint = first + (last - first) / 2'),
  (r'命中', 'return true'),
  (r'last = ', 'last = midpoint - 1'),
  (r'first = ', 'first = midpoint + 1'),
  (r'沒找到', 'return false')],
 'merge': [
  (r'^初始：呼叫 mergeSort', 'void mergeSort'),
  (r'^split ', 'size_t mid = a.size() / 2'),
  (r'開始合併', '// merge left and right back into a'),
  (r'^比較 L\[', 'if (left[i] <= right[j])'),
  (r'≤ R\[.*寫入', 'a[k++] = left[i++];'),
  (r'> R\[.*寫入', 'a[k++] = right[j++];'),
  (r'^R 已用完，複製 L', 'while (i < left.size()) a[k++] = left[i++];'),
  (r'^L 已用完，複製 R', 'while (j < right.size()) a[k++] = right[j++];'),
  (r'合併完成', '}'),
  (r'排序完成', 'void mergeSort')],
}


def snapshot(page, prefix):
    return page.evaluate("""p => {
      const act = document.querySelector(`#${p}Code .line.active`);
      return {msg: document.getElementById(p + 'Status').textContent,
              line: act ? act.textContent.replace(/\\u00a0/g, ' ').trim() : null,
              dl: act ? act.dataset.l : null};
    }""", prefix)


def run_panel(page, prefix, rules, setup=None):
    if setup:
        setup(page)
    frames = [snapshot(page, prefix)]
    while True:
        page.locator(f'#{prefix}Step').click()
        f = snapshot(page, prefix)
        if f == frames[-1]:
            break
        frames.append(f)
        assert len(frames) < 3000, prefix
    # press once more at the end: nothing changes
    page.locator(f'#{prefix}Step').click()
    end_again = snapshot(page, prefix)
    bad = []
    for i, f in enumerate(frames):
        rule = next((r for r in rules if re.search(r[0], f['msg'])), None)
        if rule is None:
            bad.append({'frame': i, 'why': 'no rule', **f}); continue
        want = rule[1]
        if want is None:
            if f['line'] is not None: bad.append({'frame': i, 'why': 'expected no line', **f})
        elif f['line'] is None or want not in f['line']:
            bad.append({'frame': i, 'why': f'expected line containing {want!r}', **f})
    return {'frames': len(frames), 'stays_at_end': end_again == frames[-1], 'mismatches': bad,
            'first': frames[0], 'last': frames[-1], 'all': frames}


report = {}
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME, headless=True, args=['--no-sandbox'])
    def fresh():
        page = browser.new_page(viewport={'width': 1440, 'height': 1000})
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)))
        page.route('https://**/*', lambda r: r.abort())
        page.goto((ROOT / 'searching_sorting.html').as_uri(), wait_until='load')
        return page, errs
    cases = [
        ('quick', 'quick', None),
        ('quick-median', 'quick', lambda pg: pg.locator('#quick .preset-btn[data-pivot="median"]').click()),
        ('shell-half', 'shell', None),
        ('shell-hibbard', 'shell', lambda pg: pg.locator('#shell .preset-btn[data-gap="2k-1"]').click()),
        ('sel', 'sel', None),
        ('bin', 'bin', None),
        ('bin-miss', 'bin', lambda pg: (pg.fill('#binTarget', '50'), pg.dispatch_event('#binTarget', 'change'))),
        ('merge', 'merge', None),
    ]
    for name, prefix, setup in cases:
        page, errs = fresh()
        r = run_panel(page, prefix, RULES[prefix], setup)
        if name == 'shell-hibbard':
            r['line2'] = page.evaluate("()=>document.querySelector('#shellCode .line[data-l=\"2\"]').textContent")
        r['page_errors'] = errs
        report[name] = r
        page.close()
    # hashing, chaining: search a value whose chain is empty
    page, errs = fresh()
    page.locator('#hashing .preset-btn[data-strategy="chain"]').click()
    page.fill('#hashVal', '13')       # 13 mod 11 = 2, empty chain in an empty table
    page.locator('#hashSearch').click()
    page.wait_for_timeout(1200)
    empty = {'status': page.locator('#hashStatus').inner_text(), 'ops': page.locator('#hashOps').inner_text()}
    page.fill('#hashVal', '54'); page.locator('#hashInsert').click(); page.wait_for_timeout(1600)
    page.fill('#hashVal', '76'); page.locator('#hashSearch').click(); page.wait_for_timeout(1200)   # 76 mod 11 = 10, chain [54]
    miss = {'status': page.locator('#hashStatus').inner_text(), 'ops': page.locator('#hashOps').inner_text()}
    report['hash-chain'] = {'empty_chain': empty, 'nonempty_miss': miss, 'page_errors': errs,
                            'batch_default': page.input_value('#hashBatch')}
    page.close()
    browser.close()

summary = {k: {kk: v[kk] for kk in ('frames', 'stays_at_end', 'mismatches', 'page_errors', 'line2') if kk in v}
           if 'frames' in v else v for k, v in report.items()}
(OUT / 'ch7-step-frames.json').write_text(json.dumps(report, ensure_ascii=False, indent=1))
print(json.dumps(summary, ensure_ascii=False, indent=1))
