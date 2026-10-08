"""One-time step for trees.html: move each section body (after its h2) into a <!-- gen:trees-SID --> block
and store the hand-written HTML in tools/enrich/content/trees_legacy.py. The three old injected example
cards (dx-voc, the heap card, the BST card) are dropped here; the new generator rebuilds them with data-cpp.
Refuses to run twice."""
import re, sys
from pathlib import Path

ROOT = Path('/home/phonchi/ds-cpp-selfstudy')
P = ROOT / 'trees.html'
LEG = ROOT / 'tools/enrich/content/trees_legacy.py'
s = P.read_text()
if '<!-- gen:trees-prologue -->' in s or LEG.exists():
    sys.exit('gen markers already placed; this one-time script must not run again')

SIDS = ['prologue', 'vocabulary', 'nodes-refs', 'parse-tree', 'traversals', 'heap', 'bst', 'bst-delete',
        'bst-analysis', 'avl', 'summary']
DROP_FROM = {'vocabulary': '<h3 id="dx-voc">', 'heap': '<div class="deck-extra">', 'bst': '<div class="deck-extra">'}

legacy = {}
for sid in SIDS:
    m = re.search(rf'(<section id="{sid}">.*?</h2>\n)(.*?)(</section>)', s, re.S)
    assert m, sid
    body = m.group(2)
    if sid in DROP_FROM:
        assert body.count(DROP_FROM[sid]) == 1, sid
        k = body.index(DROP_FROM[sid])
        body, dropped = body[:k], body[k:]
        print(f'{sid}: dropped {len(dropped)} chars of old injected HTML')
    assert "'''" not in body and not body.endswith('\\'), sid
    legacy[sid] = body
    s = s[:m.start(2)] + f'<!-- gen:trees-{sid} -->\n<!-- /gen:trees-{sid} -->\n' + s[m.end(2):]

out = ['"""Hand-written section bodies of trees.html (widgets, explanations), moved here from the page.',
       'trees_depth.py fills their {{slot:NAME}} tokens with the lecture material. Edit here, then rerun',
       'tools/enrich/enrich_trees.py."""', '', 'LEGACY = {}']
for sid, body in legacy.items():
    out.append(f"\nLEGACY[{sid!r}] = r'''{body}'''")
LEG.write_text('\n'.join(out) + '\n')
P.write_text(s)
print('markers placed:', len(SIDS))
