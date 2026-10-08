"""One-time: reorder graphs.html sections to the lecture order (08_Graphs and Graphing Algorithms.ipynb).

Old: prologue, representation, bfs, word-ladder, dfs, knight, dijkstra, prim, topsort, scc, exercises, ...
New: prologue, representation, word-ladder, bfs, knight, dfs, topsort, scc, dijkstra, prim, exercises, ...

Each chunk runs from its banner comment through </section>; ids, widgets and DOM move unchanged
(all widget JS sits in the script after the content and looks elements up by id).
Renumbers the PART labels, banner comments, float-nav and table of contents.
Usage: python3 reorder_sections.py [PATH]   (default: graphs.html in the repo)
"""
import re
import sys
from pathlib import Path

P = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3] / 'graphs.html'
s = P.read_text()

OLD = ['representation', 'bfs', 'word-ladder', 'dfs', 'knight', 'dijkstra', 'prim', 'topsort', 'scc']
NEW = ['representation', 'word-ladder', 'bfs', 'knight', 'dfs', 'topsort', 'scc', 'dijkstra', 'prim']
NUM = {sid: i + 1 for i, sid in enumerate(NEW)}        # PART numbers in the new order

order = re.findall(r'<section id="([\w-]+)">', s)
if order[1:10] == NEW:
    sys.exit('sections already in lecture order; this one-time script must not run again')
assert order[1:10] == OLD, order

BANNER = '<!-- ============================================================ -->\n<!-- '
start = s.index(BANNER + 'PART 01')
end = s.index(BANNER + 'EXERCISES')
region = s[start:end]
cuts = [m.start() for m in re.finditer(re.escape(BANNER) + 'PART ', region)] + [len(region)]
chunks = {}
for a, b in zip(cuts, cuts[1:]):
    chunk = region[a:b]
    sid = re.search(r'<section id="([\w-]+)">', chunk).group(1)
    chunks[sid] = chunk
assert list(chunks) == OLD, list(chunks)


def renumber(sid, chunk):
    n = NUM[sid]
    chunk, k1 = re.subn(r'<!-- PART \d\d:', f'<!-- PART {n:02d}:', chunk, count=1)
    chunk, k2 = re.subn(r'<div class="section-number">PART \d\d ·', f'<div class="section-number">PART {n:02d} ·', chunk, count=1)
    assert (k1, k2) == (1, 1), sid
    return chunk


s = s[:start] + ''.join(renumber(sid, chunks[sid]) for sid in NEW) + s[end:]

# The BFS map example points readers to the Dijkstra section by its PART number.
assert s.count('看完再回頭讀 PART 06：') == 1
s = s.replace('看完再回頭讀 PART 06：', f'看完再回頭讀 PART {NUM["dijkstra"]:02d}：')

# Float-nav and table of contents: reorder the entries and renumber P01..P09.
for pat in (r'  <a href="#{sid}" data-target="{sid}"><span class="fn-num">P\d\d</span>.*?</a>\n',
            r'    <a href="#{sid}"><span class="toc-num">P\d\d</span>.*?</a>\n'):
    lines = {}
    for sid in OLD:
        m = re.search(pat.format(sid=re.escape(sid)), s)
        assert m, (pat, sid)
        lines[sid] = m
    first = min(m.start() for m in lines.values())
    last = max(m.end() for m in lines.values())
    block = ''.join(re.sub(r'>P\d\d<', f'>P{NUM[sid]:02d}<', lines[sid].group()) for sid in NEW)
    assert len(block) == last - first, 'entries are not contiguous'
    s = s[:first] + block + s[last:]

P.write_text(s)
print('reordered:', ', '.join(NEW))
