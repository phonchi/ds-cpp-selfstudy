"""Chapter 9 round-2 check: from a fresh load, single-step every changed Player widget frame by frame.
Status text must match the highlighted code line / side-panel fields; at the end, 單步 must not redo anything."""
import json, re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).parent
CHROME = '/home/phonchi/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'

SNAP = """([code, status, fields, canvas]) => {
  const act = code ? document.querySelector(`#${code} .line.active`) : null;
  const o = {msg: document.getElementById(status).textContent,
             line: act ? act.textContent.replace(/\\u00a0/g, ' ').trim() : null};
  for (const f of fields) o[f] = document.getElementById(f).textContent;
  if (canvas) o.nodes = [...document.querySelectorAll(`#${canvas} .t-node`)].map(n => n.textContent);
  return o;
}"""


def step_all(page, btn, args, limit=500):
    frames = [page.evaluate(SNAP, args)]
    while True:
        page.locator('#' + btn).click()
        f = page.evaluate(SNAP, args)
        if f == frames[-1]:
            break
        frames.append(f)
        assert len(frames) < limit
    page.locator('#' + btn).click()
    page.wait_for_timeout(300)
    again = page.evaluate(SNAP, args)
    return frames, again == frames[-1]


def bst_compare_line(op, msg):
    a, b = map(int, re.search(r'比較 key=(\d+) 與 (\d+)', msg).groups())
    if a == b:
        return 'if (key == currentNode->key)' if op == 'put' else 'if (currentNode->key == key)'
    if a < b:
        return 'if (key < currentNode->key)'
    return '} else {' if op == 'put' else 'else'


def check(frames, rules, op=None):
    bad = []
    for i, f in enumerate(frames):
        if op and f['msg'].startswith('比較 key='):
            want = bst_compare_line(op, f['msg'])
            if f['line'] is None or not f['line'].startswith(want):
                bad.append({'frame': i, 'why': f'expected {want!r}', **f})
            continue
        rule = next((r for r in rules if re.search(r[0], f['msg'])), None)
        if rule is None:
            bad.append({'frame': i, 'why': 'no rule', **f}); continue
        want = rule[1]
        if want is None:
            if f['line'] is not None: bad.append({'frame': i, 'why': 'expected no line', **f})
        elif f['line'] is None or want not in f['line']:
            bad.append({'frame': i, 'why': f'expected {want!r}', **f})
    return bad


DEL_RULES = [
 (r'^_get\(|往(左|右)下移到|不在樹中', '_get(key, root)'),
 (r'屬於 Case 1', 'isLeaf()'), (r'屬於 Case 3', 'hasBothChildren()'), (r'屬於 Case 2', '} else {'),
 (r'^葉節點', '父節點指向它的指標改成 NULL'),
 (r'^只有一個', '唯一的子節點接到父節點'),
 (r'findSuccessor\(\)，找右子樹', 'findSuccessor();'),
 (r'^rightChild->findMin\(\)', 'TreeNode* cur = this;'),
 (r'^cur 還有左子', 'cur = cur->leftChild;'),
 (r'findMin\(\) 回傳它', 'return cur;'),
 (r'spliceOut\(\)', 'successor->spliceOut();'),
 (r'搬到原本', 'currentNode->key = successor->key;'),
 (r'刪除完成', None)]
HEAP_RULES = [
 (r'^heap\.push_back', 'heap.push_back(item);'),
 (r'^parentIdx = ', 'if (heap[i] < heap[parentIdx])'),
 (r'交換 heap\[\d+\] 與 heap\[\d+\]，接著 i = \d+$', None),   # resolved below per op
 (r'break：停止上浮', 'break;'),
 (r'已經是根，while 結束', 'while (i > 0)'),
 (r'^插入完成', None),
 (r'^delMin\(\)：最小值', 'int delMin()'),
 (r'^swap\(heap\[0\]', 'swap(heap[0], heap[heap.size() - 1]);'),
 (r'^result = heap\.back', 'int result = heap.back();'),
 (r'^heap\.pop_back', 'heap.pop_back();'),
 (r'^i = \d+：呼叫 percDown', 'percDown(i);'),
 (r'呼叫 percDown\(0\)', 'if (!heap.empty()) percDown(0);'),
 (r'^smChild = getMinChild', 'int smChild = getMinChild(i);'),
 (r'break：heap 性質已滿足', 'break;'),
 (r'沒有子節點.*while 結束', 'while (2 * i + 1 < (int)heap.size())'),
 (r'^return result', 'return result;'),
 (r'^i = heap\.size\(\) / 2 - 1', 'int i = heap.size() / 2 - 1;'),
 (r'^i = -1，while 結束', 'while (i >= 0)')]


def heap_rules(op):
    swap_line = 'swap(heap[i], heap[parentIdx]);' if op == 'insert' else 'swap(heap[i], heap[smChild]);'
    return [(r, swap_line if r.startswith('交換') else w) for r, w in HEAP_RULES]


TRAV_RULES = {
 'preorder':  [(r'^呼叫 preorder', 'void preorder'), (r'左子，', 'preorder(tree->getLeftChild());'),
               (r'右子，', 'preorder(tree->getRightChild());'), (r'印出', 'cout <<'), (r'結束', '}'), (r'完成$', None)],
 'inorder':   [(r'^呼叫 inorder', 'void inorder'), (r'左子，', 'inorder(tree->getLeftChild());'),
               (r'右子，', 'inorder(tree->getRightChild());'), (r'印出', 'cout <<'), (r'結束', '}'), (r'完成$', None)],
 'postorder': [(r'^呼叫 postorder', 'void postorder'), (r'左子，', 'postorder(tree->getLeftChild());'),
               (r'右子，', 'postorder(tree->getRightChild());'), (r'印出', 'cout <<'), (r'結束', '}'), (r'完成$', None)],
}
BST_RULES = {
 'put': [(r'^比較 key=(\d+) 與', None), (r'往左$', 'put(key, value, currentNode->leftChild);'),
         (r'往右$', 'put(key, value, currentNode->rightChild);'),
         (r'插入為左子', 'currentNode->leftChild = new TreeNode'), (r'插入為右子', 'currentNode->rightChild = new TreeNode'),
         (r'已存在', 'currentNode->value = value'), (r'完成', None)],
 'get': [(r'^比較 key=', None), (r'往左$', 'return get(key, currentNode->leftChild);'),
         (r'往右$', 'return get(key, currentNode->rightChild);'), (r'^找到', 'return currentNode;'),
         (r'不在樹中', 'if (currentNode == nullptr) return nullptr;')],
}


report = {}
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME, headless=True, args=['--no-sandbox'])

    def fresh():
        page = browser.new_page(viewport={'width': 1440, 'height': 1000})
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)))
        page.route('https://**/*', lambda r: r.abort())
        page.goto((ROOT / 'trees.html').as_uri(), wait_until='load')
        return page, errs

    # ---- BST delete: the four preset keys, stepping from a freshly built tree
    for k, case in (('20', 'Case 1'), ('80', 'Case 2'), ('30', 'Case 3'), ('50', 'Case 3')):
        page, errs = fresh()
        page.fill('#delKey', k)
        page.locator('#delApplyInit').click()
        frames, stays = step_all(page, 'delStep', ['delCode', 'delStatus', ['delTarget', 'delCase', 'delPhase', 'delSucc'], 'canvas-bstdel'])
        steps = frames[1:]     # frame 0 is the built tree before any step
        dup = [i for i, f in enumerate(steps) if len(f['nodes']) != len(set(f['nodes']))]
        report[f'del-{k}'] = {
            'frames': len(steps), 'stays_at_end': stays,
            'target_always_key': all(f['delTarget'] == k for f in steps),
            'case_final': steps[-1]['delCase'], 'case_ok': steps[-1]['delCase'] == case,
            'frames_with_duplicate_keys': dup, 'final_nodes': sorted(steps[-1]['nodes'], key=int),
            'key_gone': k not in steps[-1]['nodes'],
            'mismatches': check(steps, DEL_RULES), 'page_errors': errs, 'all': steps}
        page.close()

    # ---- BST put / get single-step
    page, errs = fresh()
    args = ['bstCode', 'bstStatus', ['bstOpName', 'bstResult', 'bstCmp', 'bstSize'], 'canvas-bst']
    page.locator('#bstStep').click()
    first = page.evaluate(SNAP, args)
    page.wait_for_timeout(1500)
    no_autoplay = page.evaluate(SNAP, args) == first
    frames, stays = step_all(page, 'bstStep', args)
    put = {'starts_on_step': first['bstOpName'] == 'put(40)', 'no_autoplay': no_autoplay, 'frames': len(frames),
           'stays_at_end': stays, 'size_after': frames[-1]['bstSize'], 'mismatches': check(frames, BST_RULES['put'], 'put'), 'all': frames}
    # get: run one get with the button, then change the key -> next 單步 starts a fresh get without autoplay
    page.locator('#bst button[data-bstop="get"]').click()
    page.wait_for_timeout(200)
    page.fill('#bstOpKey', '23'); page.dispatch_event('#bstOpKey', 'change')
    page.locator('#bstStep').click()
    first = page.evaluate(SNAP, args)
    page.wait_for_timeout(1500)
    no_autoplay = page.evaluate(SNAP, args) == first
    frames, stays = step_all(page, 'bstStep', args)
    get = {'starts_on_step': first['bstOpName'] == 'get(23)', 'no_autoplay': no_autoplay, 'frames': len(frames),
           'stays_at_end': stays, 'result': frames[-1]['bstResult'], 'mismatches': check(frames, BST_RULES['get'], 'get'), 'all': frames}
    report['bst-put'] = put; report['bst-get'] = get; report['bst-errors'] = errs
    page.close()

    # ---- heap: the three lecture demos, step to the end, then press 單步 twice more
    for demo in ('insert', 'delete', 'heapify'):
        page, errs = fresh()
        page.locator(f'#heap .preset-btn[data-heapdemo="{demo}"]').click()
        args = ['heapCode', 'heapStatus', ['heapSwap', 'heapCmp', 'heapIdx', 'heapPar', 'heapList']]
        frames, stays = step_all(page, 'heapStep', args)
        page.locator('#heapStep').click(); page.locator('#heapStep').click()
        after = page.evaluate(SNAP, args)
        report[f'heap-{demo}'] = {'frames': len(frames), 'stays_at_end': stays and after == frames[-1],
                                  'final_list': frames[-1]['heapList'], 'input_after': page.input_value('#heapArrInput'),
                                  'mismatches': check(frames[1:], heap_rules(demo)), 'page_errors': errs, 'all': frames}
        page.close()

    # ---- AVL LR / RL (and LL / RR): phase, bf and text describe the drawn tree
    page, errs = fresh()
    for case in ('LL', 'RR', 'LR', 'RL'):
        page.locator(f'#avl .preset-btn[data-avlcase="{case}"]').click()
        frames, stays = step_all(page, 'avlStep', [None, 'avlStatus', ['avlPhase', 'avlBf'], 'canvas-avl'])
        report[f'avl-{case}'] = {'frames': len(frames), 'stays_at_end': stays,
                                 'seq': [(f['avlPhase'], f['avlBf'], f['msg'], f['nodes'][0]) for f in frames]}
    report['avl-errors'] = errs
    page.close()

    # ---- traversals: three orders on the default parse tree
    for kind in ('preorder', 'inorder', 'postorder'):
        page, errs = fresh()
        page.locator(f'#traversals .preset-btn[data-trav="{kind}"]').click()
        frames, stays = step_all(page, 'travStep', ['travCode', 'travStatus', ['travOutput']])
        report[f'trav-{kind}'] = {'frames': len(frames), 'stays_at_end': stays, 'output': frames[-1]['travOutput'],
                                  'mismatches': check(frames, TRAV_RULES[kind]), 'page_errors': errs, 'all': frames}
        page.close()

    # ---- nodes & references status line names the highlighted C++ statement
    page, errs = fresh()
    frames, stays = step_all(page, 'nrStep', ['nrCode', 'nrStatus', []])
    bad = []
    for f in frames:
        stmt = re.sub(r'^Step \d+/\d+: ', '', f['msg']).split('：')[0]
        if f['line'] is None or stmt.replace('BinaryTree aTree', 'BinaryTree aTree') not in f['line'].replace('"', '"'):
            bad.append(f)
    report['nodes-refs'] = {'frames': len(frames), 'stays_at_end': stays, 'mismatches': bad, 'page_errors': errs, 'all': frames}
    page.close()
    browser.close()

(OUT / 'ch9-step-frames.json').write_text(json.dumps(report, ensure_ascii=False, indent=1))
summary = {}
for k, v in report.items():
    if isinstance(v, dict):
        summary[k] = {kk: (len(vv) if kk == 'mismatches' else vv) for kk, vv in v.items() if kk not in ('all', 'seq')}
        if 'seq' in v: summary[k]['seq'] = v['seq']
    else:
        summary[k] = v
print(json.dumps(summary, ensure_ascii=False, indent=1))
