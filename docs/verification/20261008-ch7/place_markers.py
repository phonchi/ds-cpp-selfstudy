"""One-time step for searching_sorting.html: move each section body (after its h2) into a
<!-- gen:search-SID --> block and store the hand-written HTML in tools/enrich/content/search_legacy.py.
The old injected cards (dx-*) and the old Exercise 3 block are dropped here; the new generator rebuilds them.
Refuses to run twice."""
import re, sys
from pathlib import Path

ROOT = Path('/home/phonchi/ds-cpp-selfstudy')
P = ROOT / 'searching_sorting.html'
LEG = ROOT / 'tools/enrich/content/search_legacy.py'
s = P.read_text()
if '<!-- gen:search-prologue -->' in s or LEG.exists():
    sys.exit('gen markers already placed; this one-time script must not run again')

SIDS = ['prologue', 'seq-search', 'bin-search', 'hashing', 'bubble', 'selection', 'insertion',
        'shell', 'merge', 'quick', 'depends', 'reference', 'supplement']
# Old injected blocks: from this marker to the end of the section body.
DROP_FROM = {'prologue': '<h3 id="dx-srch">', 'hashing': '<h3 id="dx-hash">', 'bubble': '<h3 id="dx-bub">',
             'selection': '<h3 id="dx-sel">', 'insertion': '<h3 id="dx-ins">', 'shell': '<h3 id="dx-shl">',
             'merge': '<h3 id="dx-mrg">', 'quick': '  <h3 style="margin-top:1.6rem;">講義練習：讓 quicksort 支援降冪排序（Exercise 3）</h3>'}

legacy = {}
for sid in SIDS:
    m = re.search(rf'(<section id="{sid}">.*?</h2>\n)(.*?)(</section>)', s, re.S)
    assert m, sid
    body = m.group(2)
    if sid in DROP_FROM:
        k = body.index(DROP_FROM[sid])
        assert body.count(DROP_FROM[sid]) == 1
        body, dropped = body[:k], body[k:]
        print(f'{sid}: dropped {len(dropped)} chars of old injected HTML')
    assert "'''" not in body and not body.endswith('\\'), sid
    legacy[sid] = body
    s = s[:m.start(2)] + f'<!-- gen:search-{sid} -->\n<!-- /gen:search-{sid} -->\n' + s[m.end(2):]

out = ['"""Hand-written section bodies of searching_sorting.html (widgets, explanations), moved here from the page.',
       'search_depth.py splits them at fixed anchors and interleaves the lecture material. Edit here, then rerun',
       'tools/enrich/enrich_search.py."""', '', 'LEGACY = {}']
for sid, body in legacy.items():
    out.append(f"\nLEGACY[{sid!r}] = r'''{body}'''")
LEG.write_text('\n'.join(out) + '\n')
P.write_text(s)
print('markers placed:', len(SIDS))
