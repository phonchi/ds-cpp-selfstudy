"""One-time hand edits on searching_sorting.html outside the gen blocks (after place_markers.py):
add the recap section and its navigation entries, reword the supplement heading, point the study guide
at the recap and at the （補充） folds. Refuses to run twice."""
import sys
from pathlib import Path

P = Path('/home/phonchi/ds-cpp-selfstudy/searching_sorting.html')
s = P.read_text()
if 'id="recap"' in s:
    sys.exit('hand edits already applied; this one-time script must not run again')


def once(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit(f'expected 1 match, got {n}: {old[:80]!r}')
    s = s.replace(old, new)


once('''<!-- /gen:search-supplement -->
</section>

<section id="bankquiz">''', '''<!-- /gen:search-supplement -->
</section>

<!-- ============================================================ -->
<!-- RECAP -->
<!-- ============================================================ -->
<section id="recap">
  <div class="section-number">SUMMARY · 重點回顧</div>
  <h2>重點回顧 <span class="sec-badge">本章總結</span></h2>
<!-- gen:search-recap -->
<!-- /gen:search-recap -->
</section>

<section id="bankquiz">''')
once('''  <a href="#supplement" data-target="supplement"><span class="fn-num">SUP</span><span class="fn-name">補充</span></a>
''', '''  <a href="#supplement" data-target="supplement"><span class="fn-num">SUP</span><span class="fn-name">補充</span></a>
  <a href="#recap" data-target="recap"><span class="fn-num">SUM</span><span class="fn-name">重點回顧</span></a>
''')
once('''    <a href="#supplement"><span class="toc-num">SUP</span>補充：quadratic & put 分支</a>
''', '''    <a href="#supplement"><span class="toc-num">SUP</span>補充：quadratic & put 分支</a>
    <a href="#recap"><span class="toc-num">SUM</span>重點回顧</a>
''')
once('<h2>補充：兩個 PDF 上不容易看出來的細節 <span class="sec-badge">課程補充</span></h2>',
     '<h2>補充：平方探查與 put() 分支的逐步追蹤 <span class="sec-badge">課程補充</span></h2>')
once('並用 REF 總覽區當速查表。標「講義補充」的節是課堂沒細講的延伸，第一輪可略過。</p>',
     '並用 REF 總覽區當速查表，章末的<a href="#recap">重點回顧</a>可以用來複習。標「課程補充」的節與標「（補充）」的收合區是課堂沒細講的延伸，第一輪可略過。</p>')
P.write_text(s)
print('hand edits applied')
