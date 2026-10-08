"""One-time edits on tools/enrich/content/trees_legacy.py right after place_markers.py: put {{slot:…}} tokens
where the lecture material goes, split off the parts that become （補充） folds, and fix legacy wording
(Python-only remarks, production notes, non-lecture code in side panels). Refuses to run twice."""
import sys
from pathlib import Path

P = Path('/home/phonchi/ds-cpp-selfstudy/tools/enrich/content/trees_legacy.py')
s = P.read_text()
if '{{slot:examples}}' in s:
    sys.exit('legacy edits already applied')


def once(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit(f'expected 1 match, got {n}: {old[:90]!r}')
    s = s.replace(old, new)


def cut(start, end):
    """Remove s[start:end-inclusive] and return it."""
    global s
    assert s.count(start) == 1 and s.count(end) == 1, (start[:40], end[:40])
    a = s.index(start)
    b = s.index(end, a) + len(end)
    piece = s[a:b]
    s = s[:a] + '@@CUT@@' + s[b:]
    return piece


# ---- prologue
once("""LEGACY['prologue'] = r'''  <p>樹（tree）""", """LEGACY['prologue'] = r'''  <p>樹（tree）""")
once("""整體組成一個由根（root）往下分支的層次。</p>
""", """整體組成一個由根（root）往下分支的層次。</p>
{{slot:examples}}
""")

# ---- vocabulary
once("""LEGACY['vocabulary'] = r'''  <p>在進入演算法之前""", """LEGACY['vocabulary'] = r'''{{slot:terms}}
  <p>在進入演算法之前""")
once("""這也是後面所有走訪、評估、刪除演算法的骨架。
  </div>
""", """這也是後面所有走訪、評估、刪除演算法的骨架。
  </div>
{{slot:defs}}
""")

# ---- nodes-refs
once("""  <p>Python 原書另示範 <strong>list of lists</strong>（巢狀串列）；這裡只保留為語言比較。C++ 主線採 <strong>nodes and references</strong>（節點物件 + 指標）：""",
     """  <p>本課程用 <strong>nodes and references</strong>（節點物件 + 指標）表示二元樹：""")
lol = cut("""  <h3>語言比較：List of Lists""", """  課堂投影片跳過這一小節（RISE skip），列為自學補充。</p>
""")
lol = lol.split('\n', 1)[1]  # drop the h3 line; the fold summary replaces it
lol = lol.replace("""  所以我們直接採用下面的 nodes and references 表示法（對 C++ 來說本來就更自然）。
  課堂投影片跳過這一小節（RISE skip），列為自學補充。</p>
""", """  所以我們直接採用 nodes and references 表示法（對 C++ 來說本來就更自然）。</p>
""")
once('@@CUT@@', '{{slot:class}}\n')
once("""<span class="line">        BinaryTree *t = <span class="kw">new</span> <span class="fn">BinaryTree</span>(newNode);</span>
<span class="line">        <span class="kw">if</span> (leftChild != <span class="num">NULL</span>)</span>
<span class="line">            t-&gt;leftChild = leftChild;   <span class="com">// 舊子樹下推</span></span>
<span class="line">        leftChild = t;</span>
<span class="line">    }</span>""", """<span class="line">        <span class="kw">if</span> (leftChild == <span class="num">NULL</span>) {</span>
<span class="line">            leftChild = <span class="kw">new</span> <span class="fn">BinaryTree</span>(newNode);</span>
<span class="line">        } <span class="kw">else</span> {</span>
<span class="line">            BinaryTree* newChild = <span class="kw">new</span> <span class="fn">BinaryTree</span>(newNode);</span>
<span class="line">            newChild-&gt;leftChild = leftChild;   <span class="com">// 舊子樹下推</span></span>
<span class="line">            leftChild = newChild;</span>
<span class="line">        }</span>
<span class="line">    }</span>""")
once("""<span class="line">    <span class="fn">BinaryTree</span>(string rootObj)</span>
<span class="line">      : key(rootObj), leftChild(<span class="num">NULL</span>), rightChild(<span class="num">NULL</span>) {}</span>""",
     """<span class="line">    <span class="fn">BinaryTree</span>(string rootObj) {</span>
<span class="line">        key = rootObj;</span>
<span class="line">        leftChild = <span class="num">NULL</span>;</span>
<span class="line">        rightChild = <span class="num">NULL</span>;</span>
<span class="line">    }</span>""")
once("""<span class="line">    BinaryTree *leftChild, *rightChild;</span>""",
     """<span class="line">    BinaryTree* leftChild;</span>
<span class="line">    BinaryTree* rightChild;</span>""")
once("""<code>insertRight</code> 對稱地處理右邊。
  </div>
""", """<code>insertRight</code> 對稱地處理右邊。
  </div>
{{slot:run}}
{{slot:lol}}
""")

# ---- parse-tree
once("""LEGACY['parse-tree'] = r'''  <p>對於完全括號化""", """LEGACY['parse-tree'] = r'''{{slot:intro}}
  <p>對於完全括號化""")
once("""最後套用 root 的運算子</em>。</p>
""", """最後套用 root 的運算子</em>。</p>
{{slot:tree}}
""")
once("""就把當前節點 push 進 stack；當需要回到 parent（看到 <code>)</code> 或讀完一個數字）就 pop。</p>
""", """就把當前節點 push 進 stack；當需要回到 parent（看到 <code>)</code> 或讀完一個數字）就 pop。</p>
{{slot:build}}
""")
once("""解析樹的計算演算法就是走訪演算法的特例。
  </div>
""", """解析樹的計算演算法就是走訪演算法的特例。
  </div>
{{slot:eval}}
""")

# ---- traversals
once("""    寫成程式碼<strong>幾乎是逐字翻譯</strong>定義，這正是樹的遞迴定義帶來的優雅：
  </div>
""", """    寫成程式碼<strong>幾乎是逐字翻譯</strong>定義，這正是樹的遞迴定義帶來的優雅。
  </div>
{{slot:book}}
""")
once("""          <button class="preset-btn" data-tree="balanced">cppds 走訪範例樹</button>
""", """          <button class="preset-btn" data-tree="balanced">cppds 走訪範例樹</button>
          <button class="preset-btn" data-tree="book">講義：書的章節樹</button>
""")
once("""<span class="line" data-l="1"><span class="kw">void</span> <span class="fn">preorderPanel</span>(BinaryTree* tree) {</span>
<span class="line" data-l="2">    <span class="kw">if</span> (tree != NULL) {</span>
<span class="line" data-l="3">        cout &lt;&lt; tree-&gt;<span class="fn">getRootVal</span>() &lt;&lt; <span class="str">&quot; &quot;</span>;</span>
<span class="line" data-l="4">        <span class="fn">preorderPanel</span>(tree-&gt;<span class="fn">getLeftChild</span>());</span>
<span class="line" data-l="5">        <span class="fn">preorderPanel</span>(tree-&gt;<span class="fn">getRightChild</span>()); } }</span>""",
     """<span class="line" data-l="1"><span class="kw">void</span> <span class="fn">preorder</span>(BinaryTree* tree) {</span>
<span class="line" data-l="2">    <span class="kw">if</span> (tree != <span class="num">NULL</span>) {</span>
<span class="line" data-l="3">        cout &lt;&lt; tree-&gt;<span class="fn">getRootVal</span>() &lt;&lt; <span class="str">" "</span>;   <span class="com">// root</span></span>
<span class="line" data-l="4">        <span class="fn">preorder</span>(tree-&gt;<span class="fn">getLeftChild</span>());</span>
<span class="line" data-l="5">        <span class="fn">preorder</span>(tree-&gt;<span class="fn">getRightChild</span>());</span>
<span class="line">    }</span>
<span class="line">}</span>""")
once("""        </div>
      </div>
    </div>
  </div>

  <div class="info-box warm">
    <span class="info-label">小實驗：對解析樹 (3+(4*5)) 做三種走訪</span>""", """        </div>
      </div>
    </div>
  </div>
{{slot:code}}
  <div class="info-box warm">
    <span class="info-label">小實驗：對解析樹 (3+(4*5)) 做三種走訪</span>""")
once("""postorder 的順序就是「邊計算邊累積」的最佳順序。
  </div>
""", """postorder 的順序就是「邊計算邊累積」的最佳順序。
  </div>
{{slot:printexp}}
""")

# ---- heap
once("""<strong>Binary heap</strong> 讓 insert 與 delete-min 都是 $O(\\log n)$。</p>
""", """<strong>Binary heap</strong> 讓 insert 與 delete-min 都是 $O(\\log n)$。</p>
{{slot:ops}}
""")
once("""完全不需要指標！
  </div>
""", """完全不需要指標。
  </div>
{{slot:figs}}
""")
once("""          <button class="preset-btn" data-op="heapify">Heapify (建堆積)</button>
        </div>
""", """          <button class="preset-btn" data-op="heapify">Heapify (建堆積)</button>
        </div>
        <div class="preset-row">
          <button class="preset-btn" data-heapdemo="insert" data-arr="5, 9, 11, 14, 18, 19, 21, 33, 17, 27" data-key="7" data-msg="講義圖的 heap，插入 7：按「開始」或「單步」看 percUp">講義：插入 7</button>
          <button class="preset-btn" data-heapdemo="delete" data-arr="5, 9, 11, 14, 18, 19, 21, 33, 17, 27" data-msg="講義圖的 heap：按「開始」或「單步」看 delMin 與 percDown">講義：delMin</button>
          <button class="preset-btn" data-heapdemo="heapify" data-arr="9, 6, 5, 2, 3" data-msg="講義的 [9, 6, 5, 2, 3]：按「開始」或「單步」看 buildHeap">講義：buildHeap [9, 6, 5, 2, 3]</button>
        </div>
""")
once("""<input type="number" id="heapInsertKey" value="2" style="width:80px;">""",
     """<input type="number" id="heapInsertKey" value="7" style="width:80px;">""")
once("""<input type="text" id="heapArrInput" value="3, 5, 9, 7, 11, 15, 14" style="flex:1;min-width:140px;">""",
     """<input type="text" id="heapArrInput" value="5, 9, 11, 14, 18, 19, 21, 33, 17, 27" style="flex:1;min-width:140px;">""")
once("""<span class="line" data-l="1"><span class="kw">void</span> <span class="fn">percUp</span>(vector&lt;<span class="kw">int</span>&gt;&amp; heap, <span class="kw">int</span> i) {</span>
<span class="line" data-l="2">    <span class="kw">while</span> (i &gt; <span class="num">0</span>) {</span>
<span class="line" data-l="3">        <span class="kw">int</span> parent = (i - <span class="num">1</span>) / <span class="num">2</span>;</span>
<span class="line" data-l="4">        <span class="kw">if</span> (heap[i] &lt; heap[parent])</span>
<span class="line" data-l="5">            <span class="fn">swap</span>(heap[i], heap[parent]); <span class="kw">else</span> <span class="kw">break</span>;</span>
<span class="line" data-l="6">        i = parent; } }</span>""",
     """<span class="line" data-l="1"><span class="kw">void</span> <span class="fn">percUp</span>(<span class="kw">int</span> i) {</span>
<span class="line" data-l="2">    <span class="kw">while</span> (i &gt; <span class="num">0</span>) {</span>
<span class="line" data-l="3">        <span class="kw">int</span> parentIdx = (i - <span class="num">1</span>) / <span class="num">2</span>;</span>
<span class="line" data-l="4">        <span class="kw">if</span> (heap[i] &lt; heap[parentIdx]) {</span>
<span class="line" data-l="5">            <span class="fn">swap</span>(heap[i], heap[parentIdx]);</span>
<span class="line">        } <span class="kw">else</span> {</span>
<span class="line">            <span class="kw">break</span>;</span>
<span class="line">        }</span>
<span class="line" data-l="6">        i = parentIdx;</span>
<span class="line">    }</span>
<span class="line">}</span>""")
once("""<span class="line">#include &lt;algorithm&gt;</span><span class="line">#include &lt;vector&gt;</span><span class="line"><span class="kw">using</span> namespace std;</span>
""", """<span class="line"><span class="com">// BinaryHeap 的成員函式（binaryheap.hpp）</span></span>
""")
once("""      </div>
    </div>
  </div>

  <div class="info-box green">
    <span class="info-label">為什麼 heapify 是 O(n) 而不是 O(n log n)？</span>""", """      </div>
    </div>
  </div>
{{slot:perc}}
  <div class="info-box green">
    <span class="info-label">為什麼 heapify 是 O(n) 而不是 O(n log n)？</span>""")
once("""兩者相乘的總和是 $O(n)$</strong>。
  </div>
""", """兩者相乘的總和是 $O(n)$</strong>。
  </div>
{{slot:build}}
""")
once("""  <p style="font-size:.85rem;color:var(--muted);margin-top:.5rem;">講義的 demo 依序 insert
  {10, 4, 9, 8, 12, 15, 3, 5, 14, 18}：不管插入順序怎麼亂，<code>heap[0]</code> 永遠是目前最小值，
  <code>delet()</code> 也總是取出最小者。""", """  <p style="font-size:.85rem;color:var(--muted);margin-top:.5rem;">不管資料以什麼順序進來，<code>heap[0]</code> 永遠是目前最小值，
  <code>delet()</code> 也總是取出最小者。""")
once("""額外空間 $O(n)$。真正的 in-place heapsort 則直接在原陣列管理 heap 範圍。</p>
""", """額外空間 $O(n)$。真正的 in-place heapsort 則直接在原陣列管理 heap 範圍。</p>
{{slot:sort}}
""")

# ---- bst
once("""（就像 `C++` 的 <code>unordered_map</code>）""", """（就像 C++ 的 <code>unordered_map</code>）""")
once("""和<strong>雜湊表</strong>（平均 $O(1)$ 但有衝突風險、無排序）。BST 提供第三條路：</p>
""", """和<strong>雜湊表</strong>（平均 $O(1)$ 但有衝突風險、無排序）。BST 提供第三條路。</p>
{{slot:ops}}
""")
once("""    2. 對 BST 做 <strong>inorder traversal 直接得到排序的 key 序列</strong>。
  </div>
""", """    2. 對 BST 做 <strong>inorder traversal 直接得到排序的 key 序列</strong>。
  </div>
{{slot:impl}}
""")
once("""這就是下一節要解決的問題。
  </div>
""", """這就是下一節要解決的問題。
  </div>
{{slot:get}}
""")

# ---- bst-delete
once("""然後從原位置「splice out」 successor。
  </div>
""", """然後從原位置「splice out」 successor。
  </div>
{{slot:cases}}
""")
once("""  講義的完整版其實處理三種情境，另外兩種在中序走訪相關的練習會用到。""",
     """  一般的 successor 有三種情境（下方左欄），另外兩種在沒有右子樹、需要往上找時才用得到。""")
# end of section
s = s.replace("""<span class="line"><span class="kw">delete</span> successor;</span></div></div>
  </div>
'''""", """<span class="line"><span class="kw">delete</span> successor;</span></div></div>
  </div>
{{slot:inorder}}
'''""", 1)

# ---- bst-analysis
once("""BST 退化成連結串列。
  </div>
""", """BST 退化成連結串列。
  </div>
{{slot:skew}}
""")

# ---- avl
once("""bf $&gt; 0$：left-heavy；bf $&lt; 0$：right-heavy；bf $= 0$：完美平衡。
  </div>
""", """bf $&gt; 0$：left-heavy；bf $&lt; 0$：right-heavy；bf $= 0$：完美平衡。
  </div>
{{slot:bf}}
""")
once("""  <div class="info-box green">
    <span class="info-label">為什麼是 1.44 log n？</span>""", """{{slot:perf}}
  <div class="info-box green">
    <span class="info-label">為什麼是 1.44 log n？</span>""")
once("""  <h3>實作內幕：updateBalance、rotateLeft、rebalance <span class="sec-badge">cppds §8.16–8.17 · 講義補充</span></h3>
  <p style="font-size:.88rem;color:var(--muted);">課堂投影片跳過 §8.16（AVL 效能）與 §8.17（AVL 實作）這兩節（RISE skip，講義標 Optional）：屬自學補充。</p>""",
     """  <h3>實作內幕：updateBalance、rotateLeft、rebalance <span class="sec-badge">cppds §8.17 · 選讀</span></h3>
  <p style="font-size:.88rem;color:var(--muted);">AVL 的效能分析與實作細節屬於選讀內容。課堂上只要知道：插入後沿路更新平衡因子，LL、RR 不平衡做一次旋轉，LR、RL 做兩次，每次旋轉 $O(1)$。</p>""")
once("""<code>override</code> 要求編譯器確認此函式覆寫基底類別的 virtual 函式。</p>
""", """<code>override</code> 要求編譯器確認此函式覆寫基底類別的 virtual 函式。</p>
{{slot:rot}}
""")
s = s.replace("""跟上面動畫的四個 preset 一一對應。</div></div>
  </div>
'''""", """跟上面動畫的四個 preset 一一對應。</div></div>
  </div>
{{slot:bfd}}
'''""", 1)

# ---- summary
real = cut("""  <h3>樹結構在實際系統中的地位</h3>""", """  </ul>
""")
once('@@CUT@@', '{{slot:real}}\n')

s = s.rstrip('\n') + '\n\n# Folded （補充） parts split off the sections above.\n'
s += f"\nLEGACY['lol'] = r'''{lol}'''\n"
s += f"\nLEGACY['real'] = r'''{real.split(chr(10), 1)[1]}'''\n"
P.write_text(s)
print('slots:', s.count('{{slot:'))
