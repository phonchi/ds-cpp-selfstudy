"""One-time hand edits on trees.html outside the gen blocks (after place_markers.py):
new Tree ADT and recap sections with navigation entries, renumbered PART labels, study-guide wording,
and three small extensions of the page's own Player-based widgets (heap: lecture defaults and presets;
traversals: the lecture's book tree and C++ code panel). Refuses to run twice."""
import sys
from pathlib import Path

P = Path('/home/phonchi/ds-cpp-selfstudy/trees.html')
s = P.read_text()
if 'id="tree-adt"' in s:
    sys.exit('hand edits already applied; this one-time script must not run again')


def once(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit(f'expected 1 match, got {n}: {old[:80]!r}')
    s = s.replace(old, new)


# ---- new sections
once('''<!-- /gen:trees-vocabulary -->
</section>
''', '''<!-- /gen:trees-vocabulary -->
</section>

<!-- ============================================================ -->
<!-- PART 02: Tree ADT -->
<!-- ============================================================ -->
<section id="tree-adt">
  <div class="section-number">PART 02 · Tree ADT</div>
  <h2>Tree ADT：用哪些操作建立與操作二元樹 <span class="sec-badge">cppds §8.4</span></h2>
<!-- gen:trees-tree-adt -->
<!-- /gen:trees-tree-adt -->
</section>
''')
once('''<!-- /gen:trees-summary -->
</section>
''', '''<!-- /gen:trees-summary -->
</section>

<!-- ============================================================ -->
<!-- RECAP -->
<!-- ============================================================ -->
<section id="recap">
  <div class="section-number">SUMMARY · 重點回顧</div>
  <h2>重點回顧 <span class="sec-badge">本章總結</span></h2>
<!-- gen:trees-recap -->
<!-- /gen:trees-recap -->
</section>
''')

# ---- PART labels
for old, new in [('PART 09 · AVL 樹', 'PART 10 · AVL 樹'), ('PART 08 · BST 分析', 'PART 09 · BST 分析'),
                 ('PART 07 · BST 刪除三情境', 'PART 08 · BST 刪除三情境'), ('PART 06 · 二元搜尋樹', 'PART 07 · 二元搜尋樹'),
                 ('PART 05 · 二元堆積', 'PART 06 · 二元堆積'), ('PART 04 · 樹的走訪', 'PART 05 · 樹的走訪'),
                 ('PART 03 · 解析樹', 'PART 04 · 解析樹'), ('PART 02 · 樹的實作', 'PART 03 · 樹的實作')]:
    once(f'<div class="section-number">{old}</div>', f'<div class="section-number">{new}</div>')

# ---- float navigation
once('''  <a href="#nodes-refs" data-target="nodes-refs"><span class="fn-num">P02</span><span class="fn-name">Nodes &amp; References</span></a>
  <a href="#parse-tree" data-target="parse-tree"><span class="fn-num">P03</span><span class="fn-name">解析樹</span></a>
  <a href="#traversals" data-target="traversals"><span class="fn-num">P04</span><span class="fn-name">樹的走訪</span></a>
  <a href="#heap" data-target="heap"><span class="fn-num">P05</span><span class="fn-name">二元堆積</span></a>
  <a href="#bst" data-target="bst"><span class="fn-num">P06</span><span class="fn-name">二元搜尋樹</span></a>
  <a href="#bst-delete" data-target="bst-delete"><span class="fn-num">P07</span><span class="fn-name">BST 刪除</span></a>
  <a href="#bst-analysis" data-target="bst-analysis"><span class="fn-num">P08</span><span class="fn-name">BST 分析</span></a>
  <a href="#avl" data-target="avl"><span class="fn-num">P09</span><span class="fn-name">AVL 樹</span></a>
  <a href="#summary" data-target="summary"><span class="fn-num">REF</span><span class="fn-name">總覽比較</span></a>
    <a href="#bankquiz"''', '''  <a href="#tree-adt" data-target="tree-adt"><span class="fn-num">P02</span><span class="fn-name">Tree ADT</span></a>
  <a href="#nodes-refs" data-target="nodes-refs"><span class="fn-num">P03</span><span class="fn-name">Nodes &amp; References</span></a>
  <a href="#parse-tree" data-target="parse-tree"><span class="fn-num">P04</span><span class="fn-name">解析樹</span></a>
  <a href="#traversals" data-target="traversals"><span class="fn-num">P05</span><span class="fn-name">樹的走訪</span></a>
  <a href="#heap" data-target="heap"><span class="fn-num">P06</span><span class="fn-name">二元堆積</span></a>
  <a href="#bst" data-target="bst"><span class="fn-num">P07</span><span class="fn-name">二元搜尋樹</span></a>
  <a href="#bst-delete" data-target="bst-delete"><span class="fn-num">P08</span><span class="fn-name">BST 刪除</span></a>
  <a href="#bst-analysis" data-target="bst-analysis"><span class="fn-num">P09</span><span class="fn-name">BST 分析</span></a>
  <a href="#avl" data-target="avl"><span class="fn-num">P10</span><span class="fn-name">AVL 樹</span></a>
  <a href="#summary" data-target="summary"><span class="fn-num">REF</span><span class="fn-name">總覽比較</span></a>
  <a href="#recap" data-target="recap"><span class="fn-num">SUM</span><span class="fn-name">重點回顧</span></a>
    <a href="#bankquiz"''')

# ---- table of contents
once('''    <a href="#nodes-refs"><span class="toc-num">P02</span>Nodes &amp; References</a>
    <a href="#parse-tree"><span class="toc-num">P03</span>解析樹 Parse Tree</a>
    <a href="#traversals"><span class="toc-num">P04</span>樹的走訪</a>
    <a href="#heap"><span class="toc-num">P05</span>二元堆積</a>
    <a href="#bst"><span class="toc-num">P06</span>二元搜尋樹</a>
    <a href="#bst-delete"><span class="toc-num">P07</span>BST 刪除三情境</a>
    <a href="#bst-analysis"><span class="toc-num">P08</span>BST 分析</a>
    <a href="#avl"><span class="toc-num">P09</span>AVL 樹與旋轉</a>
    <a href="#summary"><span class="toc-num">REF</span>Map ADT 總覽比較</a>
''', '''    <a href="#tree-adt"><span class="toc-num">P02</span>Tree ADT</a>
    <a href="#nodes-refs"><span class="toc-num">P03</span>Nodes &amp; References</a>
    <a href="#parse-tree"><span class="toc-num">P04</span>解析樹 Parse Tree</a>
    <a href="#traversals"><span class="toc-num">P05</span>樹的走訪</a>
    <a href="#heap"><span class="toc-num">P06</span>二元堆積</a>
    <a href="#bst"><span class="toc-num">P07</span>二元搜尋樹</a>
    <a href="#bst-delete"><span class="toc-num">P08</span>BST 刪除三情境</a>
    <a href="#bst-analysis"><span class="toc-num">P09</span>BST 分析</a>
    <a href="#avl"><span class="toc-num">P10</span>AVL 樹與旋轉</a>
    <a href="#summary"><span class="toc-num">REF</span>Map ADT 總覽比較</a>
    <a href="#recap"><span class="toc-num">SUM</span>重點回顧</a>
''')

# ---- study guide
once('並用 REF 總覽區當速查表。標 Optional／Python 參考的內容第一輪可略過。</p>',
     '並用 REF 總覽區當速查表，章末的<a href="#recap">重點回顧</a>可以用來複習。標「選讀」的 AVL 內部實作與標「（補充）」的收合區是課堂沒細講的延伸，第一輪可略過。</p>')

# ---- heap widget: start from the heap in the lecture figures, add lecture presets
once('  let heapArr = [3, 5, 9, 7, 11, 15, 14];', '  let heapArr = [5, 9, 11, 14, 18, 19, 21, 33, 17, 27];')
once('''  $('heapInsertBtn').onclick = startOp;
''', '''  $('heapInsertBtn').onclick = startOp;
  // Lecture examples: set the operation, the array and the key, then let 開始／單步 run them.
  document.querySelectorAll('#heap .preset-btn[data-heapdemo]').forEach(btn => {
    btn.onclick = () => {
      const opBtn = document.querySelector(`#heap .preset-btn[data-op="${btn.dataset.heapdemo}"]`);
      if (opBtn) opBtn.click();
      $('heapArrInput').value = btn.dataset.arr;
      if (btn.dataset.key) $('heapInsertKey').value = btn.dataset.key;
      if (player) player.stop();
      player = null;
      heapArr = btn.dataset.arr.split(/[\\s,]+/).map(x => parseInt(x, 10)).filter(n => !isNaN(n));
      renderHeap(heapArr, {});
      setText($('heapStatus'), btn.dataset.msg || '');
      setText($('heapSwap'), '0'); setText($('heapCmp'), '0');
      setText($('heapIdx'), '—'); setText($('heapPar'), '—');
      hlLine($('heapCode'), null);
    };
  });
''')

# ---- traversal widget: the lecture's book tree, and the lecture's C++ functions in the code panel
once('''    balanced: () => {
      const arr = ['F','B','A',null,null,'D','C',null,null,'E',null,null,'G',null,'H',null,null];
      return buildFromArr(arr);
    }
  };''', '''    balanced: () => {
      const arr = ['F','B','A',null,null,'D','C',null,null,'E',null,null,'G',null,'H',null,null];
      return buildFromArr(arr);
    },
    book: () => {
      const arr = ['Book','Ch1','1.1',null,null,'1.2','1.2.1',null,null,'1.2.2',null,null,
                   'Ch2','2.1',null,null,'2.2','2.2.1',null,null,'2.2.2',null,null];
      return buildFromArr(arr);
    }
  };''')
once('''      preorder: `<span class="line" data-l="1"><span class="fn">preorder</span>(tree):</span>
<span class="line" data-l="2">    <span class="kw">if</span> tree != <span class="num">NULL</span>:</span>
<span class="line" data-l="3">        <span class="fn">visit</span>(tree-&gt;key)   <span class="com">// root</span></span>
<span class="line" data-l="4">        <span class="fn">preorder</span>(tree-&gt;left)</span>
<span class="line" data-l="5">        <span class="fn">preorder</span>(tree-&gt;right)</span>`,
      inorder: `<span class="line" data-l="1"><span class="fn">inorder</span>(tree):</span>
<span class="line" data-l="2">    <span class="kw">if</span> tree != <span class="num">NULL</span>:</span>
<span class="line" data-l="3">        <span class="fn">inorder</span>(tree-&gt;left)</span>
<span class="line" data-l="4">        <span class="fn">visit</span>(tree-&gt;key)   <span class="com">// root</span></span>
<span class="line" data-l="5">        <span class="fn">inorder</span>(tree-&gt;right)</span>`,
      postorder: `<span class="line" data-l="1"><span class="fn">postorder</span>(tree):</span>
<span class="line" data-l="2">    <span class="kw">if</span> tree != <span class="num">NULL</span>:</span>
<span class="line" data-l="3">        <span class="fn">postorder</span>(tree-&gt;left)</span>
<span class="line" data-l="4">        <span class="fn">postorder</span>(tree-&gt;right)</span>
<span class="line" data-l="5">        <span class="fn">visit</span>(tree-&gt;key)   <span class="com">// root</span></span>`,
    };''', '''      preorder: `<span class="line" data-l="1"><span class="kw">void</span> <span class="fn">preorder</span>(BinaryTree* tree) {</span>
<span class="line" data-l="2">    <span class="kw">if</span> (tree != <span class="num">NULL</span>) {</span>
<span class="line" data-l="3">        cout &lt;&lt; tree-&gt;<span class="fn">getRootVal</span>() &lt;&lt; <span class="str">" "</span>;   <span class="com">// root</span></span>
<span class="line" data-l="4">        <span class="fn">preorder</span>(tree-&gt;<span class="fn">getLeftChild</span>());</span>
<span class="line" data-l="5">        <span class="fn">preorder</span>(tree-&gt;<span class="fn">getRightChild</span>());</span>
<span class="line">    }</span>
<span class="line">}</span>`,
      inorder: `<span class="line" data-l="1"><span class="kw">void</span> <span class="fn">inorder</span>(BinaryTree* tree) {</span>
<span class="line" data-l="2">    <span class="kw">if</span> (tree != <span class="num">NULL</span>) {</span>
<span class="line" data-l="3">        <span class="fn">inorder</span>(tree-&gt;<span class="fn">getLeftChild</span>());</span>
<span class="line" data-l="4">        cout &lt;&lt; tree-&gt;<span class="fn">getRootVal</span>() &lt;&lt; <span class="str">" "</span>;   <span class="com">// root</span></span>
<span class="line" data-l="5">        <span class="fn">inorder</span>(tree-&gt;<span class="fn">getRightChild</span>());</span>
<span class="line">    }</span>
<span class="line">}</span>`,
      postorder: `<span class="line" data-l="1"><span class="kw">void</span> <span class="fn">postorder</span>(BinaryTree* tree) {</span>
<span class="line" data-l="2">    <span class="kw">if</span> (tree != <span class="num">NULL</span>) {</span>
<span class="line" data-l="3">        <span class="fn">postorder</span>(tree-&gt;<span class="fn">getLeftChild</span>());</span>
<span class="line" data-l="4">        <span class="fn">postorder</span>(tree-&gt;<span class="fn">getRightChild</span>());</span>
<span class="line" data-l="5">        cout &lt;&lt; tree-&gt;<span class="fn">getRootVal</span>() &lt;&lt; <span class="str">" "</span>;   <span class="com">// root</span></span>
<span class="line">    }</span>
<span class="line">}</span>`,
    };''')

P.write_text(s)
print('hand edits applied')
