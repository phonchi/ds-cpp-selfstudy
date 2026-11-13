"""Chapter 8 static checks: compile every data-cpp block, compare outputs, ids, anchors, figures, inline JS."""
import json
import os
import subprocess
import tempfile
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).parent
HEADERS = '/home/phonchi/ds_cpp/Slides'
PAGE = ROOT / 'graphs.html'
html = PAGE.read_text()
soup = BeautifulSoup(html, 'html.parser', preserve_whitespace_tags={'pre', 'span'})
report = {'examples': [], 'errors': []}


def err(msg):
    report['errors'].append(msg)


def shown_output(el):
    """The visible output paired with a run block: same card, or right after the enclosing details."""
    card = el.find_parent(class_='deck-extra')
    pre = card.select_one('.expected-out pre') if card else None
    if pre is None:
        det = el.find_parent('details')
        nxt = det.find_next_sibling() if det else None
        if nxt is not None and 'expected-out' in (nxt.get('class') or []):
            pre = nxt.select_one('pre')
    return None if pre is None else pre.get_text()


with tempfile.TemporaryDirectory(prefix='ch8-cpp-') as tmp:
    for i, el in enumerate(soup.select('[data-cpp]')):
        kind = el['data-cpp']
        if kind not in ('run', 'compile-error', 'exercise'):
            continue
        src = '\n'.join(x.get_text() for x in el.select('.line'))
        label = el.find_parent(class_='deck-extra').select_one('.dx-label').get_text()
        name = f'ex{i:02d}'
        cpp, exe = Path(tmp) / f'{name}.cpp', Path(tmp) / name
        cpp.write_text(src + '\n')
        c = subprocess.run(['g++', '-std=c++17', '-Wall', '-Wextra', '-pedantic', '-I' + HEADERS,
                            str(cpp), '-o', str(exe)], text=True, capture_output=True)
        rec = {'id': name, 'label': label, 'kind': kind}
        if kind in ('compile-error', 'exercise'):
            rec['passed'] = c.returncode != 0
            rec['compiler'] = c.stderr.strip().splitlines()[:3]
            if not rec['passed']:
                err(f'{label}: compile-error block compiled')
        else:
            if c.returncode != 0 or c.stderr:
                err(f'{label}: compile failed or warned: {c.stderr[:400]}')
                rec['passed'] = False
            else:
                r = subprocess.run([str(exe)], text=True, capture_output=True, timeout=10, cwd=HEADERS)
                expected = el.get('data-expected')
                shown = shown_output(el)
                silent = expected == '' and shown is None   # assert-only program: prints nothing
                rec.update(stdout=r.stdout, exit=r.returncode,
                           matches_data_expected=r.stdout == expected,
                           matches_visible=silent or (shown is not None and r.stdout == shown + '\n'))
                rec['passed'] = r.returncode == 0 and rec['matches_data_expected'] and rec['matches_visible']
                if not rec['passed']:
                    err(f'{label}: output mismatch {r.stdout!r} vs {expected!r} / {shown!r}')
        report['examples'].append(rec)

    ids = [e['id'] for e in soup.select('[id]')]
    dup = sorted({x for x in ids if ids.count(x) > 1})
    if dup:
        err(f'duplicate ids: {dup}')
    for a in soup.select('a[href^="#"]'):
        if a['href'] != '#' and a['href'][1:] not in ids:
            err(f'dangling anchor {a["href"]}')
    for img in soup.select('img'):
        if not (ROOT / img['src']).exists():
            err(f'missing image {img["src"]}')
        for attr in ('alt', 'width', 'height', 'loading'):
            if not img.get(attr):
                err(f'img {img["src"]} lacks {attr}')
    for i, sc in enumerate(soup.select('script:not([src])')):
        js = Path(tmp) / f's{i}.js'
        js.write_text(sc.string or sc.get_text())
        r = subprocess.run(['node', '--check', str(js)], capture_output=True, text=True)
        if r.returncode:
            err(f'inline script {i}: {r.stderr[:300]}')
    report['scripts_checked'] = i + 1
    report['ids'] = len(ids)

# Every h2 section of the chapter body has at least one h3.
for sec in soup.select('section[id]'):
    if sec['id'] not in ('cards', 'bankquiz') and not sec.select('h3'):
        err(f'section {sec["id"]} has no h3')
# Quizzes: four options, each with its own feedback.
for q in soup.select('.quiz-options'):
    opts = q.select('.quiz-opt')
    report.setdefault('quiz_option_counts', []).append(len(opts))
    if len(opts) != 4:
        err(f'{q["id"]}: {len(opts)} options')
    if any(not o.get('data-fb') for o in opts):
        err(f'{q["id"]}: option without feedback')

runs = [r for r in report['examples'] if r['kind'] == 'run']
# quiz-box checks (in-text and bank): four options, exactly one correct, letters, feedback HTML is safe text.
from bs4 import BeautifulSoup as _BS
if soup.select('.sq-item'):
    err(f'{len(soup.select(".sq-item"))} sq-item blocks remain')
if 'function quizCheck' not in html:
    err('quizCheck missing')
qids = []
for box in soup.select('.quiz-box'):
    ops = box.select('.quiz-options')
    if len(ops) != 1:
        err('quiz-box without one .quiz-options'); continue
    qid = ops[0]['id'][:-len('Options')]
    qids.append(qid)
    opts = ops[0].select('.quiz-opt')
    if len(opts) != 4 or sum(o.get('data-correct') == 'true' for o in opts) != 1:
        err(f'{qid}: options/correct count wrong')
    if not box.select_one(f'#{qid}Feedback'):
        err(f'{qid}: feedback box missing')
    for o in opts:
        if not o.select_one('.opt-letter') or f"quizCheck('{qid}'" not in (o.get('onclick') or ''):
            err(f'{qid}: option lacks letter or handler')
        fb = o.get('data-fb') or ''
        if not fb.strip():
            err(f'{qid}: option without feedback')
        if fb.startswith(('正確。', '不對。')):
            err(f'{qid}: feedback repeats 正確／不對')
        tags = {t.name for t in _BS(fb, 'html.parser').find_all()}
        if tags - {'code', 'strong', 'em', 'sub', 'sup', 'br'}:
            err(f'{qid}: feedback would render tags {sorted(tags)}: {fb[:80]}')
dupq = sorted({x for x in qids if qids.count(x) > 1})
if dupq:
    err(f'duplicate quiz ids {dupq}')
report['quiz_boxes'] = len(qids)
report['bank_quiz_boxes'] = len(soup.select('#bankquiz .quiz-box'))
report['summary'] = {'run': len(runs), 'run_passed': sum(r['passed'] for r in runs),
                     'compile_error': len(report['examples']) - len(runs), 'errors': len(report['errors'])}
(OUT / 'content-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=1) + '\n')
print(json.dumps(report['summary'], ensure_ascii=False))
for e in report['errors']:
    print('ERROR', e)
raise SystemExit(1 if report['errors'] else 0)
