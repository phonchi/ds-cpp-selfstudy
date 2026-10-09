"""Hand-written section bodies of trees.html (widgets, explanations), moved here from the page.
trees_depth.py fills their {{slot:NAME}} tokens with the lecture material. Edit here, then rerun
tools/enrich/enrich_trees.py."""

LEGACY = {}

LEGACY['prologue'] = r'''  <p>樹（tree）出現在作業系統、編譯器、資料庫、網路路由、機器學習等許多領域。和前面學過的線性結構（list、stack、queue）不同，樹是<strong>階層式</strong>的：一個節點可以連到多個子節點，整體組成一個由根（root）往下分支的層次。</p>
{{slot:examples}}

  <div class="info-box">
    <span class="info-label">本章內容</span>
    <strong>1. 抽象結構：</strong>樹的術語、Tree ADT、用 nodes &amp; references 實作。<br>
    <strong>2. 應用：</strong>解析樹（parse tree）把數學運算式轉成可遞迴計算的結構。<br>
    <strong>3. 三種走訪：</strong>preorder、inorder、postorder，都用遞迴實作。<br>
    <strong>4. 兩個樹型 ADT：</strong>用陣列實作的 <strong>Binary Heap</strong>（優先佇列）與用節點實作的 <strong>Binary Search Tree</strong>（map）。<br>
    <strong>5. 平衡的代價：</strong>BST 在最差情況退化為 $O(n)$，AVL 樹用旋轉維持 $O(\log n)$ 上界。
  </div>

  <h3>顏色語義（整頁通用）</h3>
  <div class="legend">
    <span class="legend-item"><span class="lg-swatch" style="background:var(--node-default)"></span>未處理</span>
    <span class="legend-item"><span class="lg-swatch" style="background:var(--node-active)"></span>正在處理 / 比較</span>
    <span class="legend-item"><span class="lg-swatch" style="background:var(--node-current)"></span>當前 / 交換</span>
    <span class="legend-item"><span class="lg-swatch" style="background:var(--node-visited)"></span>已訪問 / 完成</span>
    <span class="legend-item"><span class="lg-swatch" style="background:var(--node-parent)"></span>父節點</span>
    <span class="legend-item"><span class="lg-swatch" style="background:var(--node-target)"></span>找到目標</span>
    <span class="legend-item"><span class="lg-swatch" style="background:#e67e22"></span>路徑</span>
  </div>

  <p>每一節都採相同的版面：左邊是<strong>視覺化畫布與控制列</strong>，右邊是<strong>即時統計、虛擬碼與複雜度分析</strong>。按 <span class="pill pill-green">▶ 開始</span> 看完整動畫，或按 <span class="pill pill-blue">→ 單步</span> 一格一格觀察。</p>
'''

LEGACY['vocabulary'] = r'''{{slot:terms}}
  <p>進入演算法之前，先統一用語。把滑鼠移到下方互動樹的任何一個節點上，<strong>右側面板會即時顯示該節點的所有屬性</strong>；點擊節點則會高亮它的「祖先路徑（path-to-root）」與「子樹（subtree）」。</p>

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div class="tree-canvas" id="canvas-vocab">
          <svg class="edges-layer"></svg>
          <div class="nodes-layer"></div>
        </div>
        <div class="status-banner"><span class="status-icon">›</span><span class="status-text" id="vocabStatus">將滑鼠移到節點上看屬性，點擊節點高亮路徑與子樹</span></div>
        <div class="controls-bar">
          <button class="btn btn-reset" id="vocabReset">↺ 清除高亮</button>
          <span style="font-size:.78rem;color:var(--muted);margin-left:.5rem;">點擊不同節點觀察 path-to-root 與 subtree 的差異</span>
        </div>
      </div>
    </div>

    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">節點屬性 <span class="ic-badge">LIVE</span></div>
        <div class="ic-row"><span class="ic-label">key</span><span class="ic-value highlight" id="vocabKey">—</span></div>
        <div class="ic-row"><span class="ic-label">parent</span><span class="ic-value" id="vocabParent">—</span></div>
        <div class="ic-row"><span class="ic-label">children</span><span class="ic-value" id="vocabChildren">—</span></div>
        <div class="ic-row"><span class="ic-label">siblings</span><span class="ic-value" id="vocabSibs">—</span></div>
        <div class="ic-row"><span class="ic-label">level</span><span class="ic-value" id="vocabLevel">—</span></div>
        <div class="ic-row"><span class="ic-label">subtree height</span><span class="ic-value" id="vocabHeight">—</span></div>
        <div class="ic-row"><span class="ic-label">is leaf?</span><span class="ic-value" id="vocabLeaf">—</span></div>
      </div>
      <details class="tree-detail"><summary>關鍵術語的整理</summary><div class="tree-detail-body"><div class="info-card">
        <div class="ic-title">關鍵術語</div>
        <div style="font-size:.83rem;line-height:1.55;color:var(--ink);">
          <strong>Root</strong>：唯一沒有 parent 的節點。<br>
          <strong>Edge</strong>：連接 parent 與 child 的單向連結。<br>
          <strong>Path</strong>：邊串成的節點序列。<br>
          <strong>Leaf</strong>：沒有 children 的節點。<br>
          <strong>Subtree</strong>：某節點與其所有後代。<br>
          <strong>Level</strong>：root 到該節點的邊數。<br>
          <strong>Height</strong>：樹中任何節點的最大 level。
        </div>
      </div></div></details>
    </div>
  </div>

  <div class="info-box">
    <span class="info-label">兩個等價的定義</span>
    <strong>定義一（集合式）：</strong>樹是節點集合 $V$ 與邊集合 $E$ 的二元組，滿足：（1）恰有一個 root，（2）除 root 外每個節點恰有一個 incoming edge，（3）從 root 到每個節點存在唯一路徑。<br>
    <strong>定義二（遞迴式）：</strong>樹要嘛是空的；要嘛由一個 root 連接到零或多個 subtree，每個 subtree 本身也是一棵樹。
    <br><br>
    遞迴定義對寫程式特別友善：它直接告訴你 base case（空樹）和 recursive step（處理 root + 遞迴處理子樹），這也是後面所有走訪、求值、刪除演算法的骨架。
  </div>
{{slot:defs}}

  <h3>二元樹（Binary Tree）</h3>
  <p>本章只討論每個節點最多有<strong>兩個子節點</strong>的樹，稱為二元樹。兩個子節點分別叫 <code>leftChild</code> 和 <code>rightChild</code>，左右的順序在解析樹（運算子的左右運算元）和 BST（小的在左、大的在右）中都有意義。</p>

'''

LEGACY['nodes-refs'] = r'''  <p>本課程用 <strong>nodes and references</strong>（節點物件 + 指標）表示二元樹：每個 <code>BinaryTree</code> 帶 <code>key</code>、<code>leftChild</code>、<code>rightChild</code>，子指標不是 <code>NULL</code> 時就指向另一棵遞迴定義的樹。</p>

{{slot:class}}

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div class="tree-canvas" id="canvas-nr" style="height:320px;">
          <svg class="edges-layer"></svg>
          <div class="nodes-layer"></div>
        </div>
        <div class="status-banner"><span class="status-icon">›</span><span class="status-text" id="nrStatus">按「下一步」逐行執行程式碼，看樹如何長出來</span></div>
        <div class="controls-bar">
          <button class="btn btn-step" id="nrStep">→ 下一步</button>
          <button class="btn btn-reset" id="nrReset">↺ 重置</button>
          <button class="btn btn-play" id="nrPlay">▶ 自動播放</button>
          <div style="flex:1;min-width:120px;display:flex;align-items:center;gap:.5rem;">
            <span style="font-size:.78rem;color:var(--muted);">速度</span>
            <input type="range" id="nrSpeed" min="200" max="1500" step="100" value="700" style="flex:1;accent-color:var(--accent3);">
          </div>
        </div>
      </div>
    </div>

    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">當前指令 <span class="ic-badge" style="background:var(--accent2)">CODE</span></div>
        <div class="pseudo-code" id="nrCode" style="font-size:.74rem;"><span class="line">#include &quot;pythonds3/cppds/binarytree.hpp&quot;</span><span class="line"><span class="kw">int</span> main() {</span>
<span class="line" data-l="1">    BinaryTree aTree(<span class="str">&quot;a&quot;</span>);</span>
<span class="line" data-l="2">    aTree.<span class="fn">insertLeft</span>(<span class="str">&quot;b&quot;</span>);</span>
<span class="line" data-l="3">    aTree.<span class="fn">insertRight</span>(<span class="str">&quot;c&quot;</span>);</span>
<span class="line" data-l="4">    aTree.<span class="fn">getLeftChild</span>()-&gt;<span class="fn">insertRight</span>(<span class="str">&quot;d&quot;</span>);</span>
<span class="line" data-l="5">    aTree.<span class="fn">getRightChild</span>()-&gt;<span class="fn">insertLeft</span>(<span class="str">&quot;e&quot;</span>);</span>
<span class="line" data-l="6">    aTree.<span class="fn">getRightChild</span>()-&gt;<span class="fn">insertRight</span>(<span class="str">&quot;f&quot;</span>);</span>
<span class="line">    <span class="kw">return</span> <span class="num">0</span>; }</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">BinaryTree 類別 <span class="ic-badge" style="background:var(--accent3)">CLASS</span></div>
        <details class="tree-detail tree-code-fold"><summary>程式：BinaryTree 類別</summary><div class="pseudo-code" style="font-size:.72rem;">
<span class="line"><span class="kw">class</span> <span class="fn">BinaryTree</span> {</span>
<span class="line">  <span class="kw">public</span>:</span>
<span class="line">    string key;</span>
<span class="line">    BinaryTree* leftChild;</span>
<span class="line">    BinaryTree* rightChild;</span>
<span class="line">    <span class="fn">BinaryTree</span>(string rootObj) {</span>
<span class="line">        key = rootObj;</span>
<span class="line">        leftChild = <span class="num">NULL</span>;</span>
<span class="line">        rightChild = <span class="num">NULL</span>;</span>
<span class="line">    }</span>
<span class="line"> </span>
<span class="line">    <span class="kw">void</span> <span class="fn">insertLeft</span>(string newNode) {</span>
<span class="line">        <span class="kw">if</span> (leftChild == <span class="num">NULL</span>) {</span>
<span class="line">            leftChild = <span class="kw">new</span> <span class="fn">BinaryTree</span>(newNode);</span>
<span class="line">        } <span class="kw">else</span> {</span>
<span class="line">            BinaryTree* newChild = <span class="kw">new</span> <span class="fn">BinaryTree</span>(newNode);</span>
<span class="line">            newChild-&gt;leftChild = leftChild;   <span class="com">// 舊子樹下推</span></span>
<span class="line">            leftChild = newChild;</span>
<span class="line">        }</span>
<span class="line">    }</span>
<span class="line">};</span></div></details>
      </div>
    </div>
  </div>

  <details class="tree-detail"><summary>insertLeft 兩種情況的整理</summary><div class="tree-detail-body"><div class="info-box warm">
    <span class="info-label">注意 insertLeft 的兩種情況</span>
    <strong>Case 1（左邊空）：</strong>直接把新節點掛上去。<br>
    <strong>Case 2（左邊已有東西）：</strong>新節點插在中間，<strong>把原本的左子樹整個推到新節點的左邊一層</strong>。這個「往下推」的設計避免了破壞原本的子結構。<code>insertRight</code> 對稱地處理右邊。
  </div></div></details>
{{slot:run}}
{{slot:lol}}
'''

LEGACY['parse-tree'] = r'''{{slot:intro}}
  <p>完全括號化（fully parenthesized）的運算式，例如 <code>((7 + 3) * (5 - 2))</code>，可以變成一棵樹：<strong>運算子放在內部節點、運算元放在葉子上</strong>。樹的階層反映了運算的優先順序：求值時只要遞迴地<em>先算左子樹、再算右子樹、最後套用 root 的運算子</em>。</p>
{{slot:tree}}

  <p>建構演算法用一個 <strong>stack 追蹤 parent</strong>：往下走進一個 child（看到 <code>(</code> 或運算子）時，把目前節點 push 進 stack；需要回到 parent（看到 <code>)</code> 或讀完一個數字）時就 pop。</p>
{{slot:build}}

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div class="tree-canvas" id="canvas-parse" style="height:340px;">
          <svg class="edges-layer"></svg>
          <div class="nodes-layer"></div>
        </div>
        <div class="status-banner"><span class="status-icon">›</span><span class="status-text" id="parseStatus">按「開始」逐 token 建構解析樹</span></div>
        <div class="token-strip" id="parseTokens"></div>
        <div class="input-row">
          <label>表達式：</label>
          <input type="text" id="parseInput" value="( ( 7 + 3 ) * ( 5 - 2 ) )">
          <button class="btn btn-shuffle" id="parseApply">套用</button>
        </div>
        <div class="preset-row">
          <button class="preset-btn active" data-expr="( ( 7 + 3 ) * ( 5 - 2 ) )">((7+3)*(5-2))</button>
          <button class="preset-btn" data-expr="( 3 + ( 4 * 5 ) )">(3+(4*5))</button>
          <button class="preset-btn" data-expr="( ( 1 + 2 ) + ( 3 + 4 ) )">((1+2)+(3+4))</button>
          <button class="preset-btn" data-expr="( ( 10 / 2 ) - ( 6 - 3 ) )">((10/2)-(6-3))</button>
        </div>
        <div class="controls-bar">
          <button class="btn btn-play" id="parsePlay">▶ 開始建構</button>
          <button class="btn btn-step" id="parseStep">→ 單步</button>
          <button class="btn btn-reset" id="parseReset">↺ 重置</button>
          <button class="btn btn-toggle" id="parseEvalBtn">⊕ 評估表達式</button>
          <div style="flex:1;min-width:120px;display:flex;align-items:center;gap:.5rem;">
            <span style="font-size:.78rem;color:var(--muted);">速度</span>
            <input type="range" id="parseSpeed" min="200" max="2000" step="100" value="700" style="flex:1;accent-color:var(--accent3);">
          </div>
        </div>
      </div>
    </div>

    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">即時狀態 <span class="ic-badge">LIVE</span></div>
        <div class="ic-row"><span class="ic-label">當前 token</span><span class="ic-value highlight" id="parseTok">—</span></div>
        <div class="ic-row"><span class="ic-label">當前 node</span><span class="ic-value" id="parseCur">—</span></div>
        <div class="ic-row"><span class="ic-label">stack 深度</span><span class="ic-value" id="parseStackD">0</span></div>
        <div class="ic-row"><span class="ic-label">評估結果</span><span class="ic-value highlight" id="parseResult">—</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">parent stack <span class="ic-badge" style="background:var(--accent2)">STACK</span></div>
        <div class="stack-vis" id="parseStack">
          <div class="stack-label">parent ↓</div>
        </div>
      </div>
      <div class="info-card">
        <div class="ic-title">建構規則 <span class="ic-badge" style="background:var(--accent2)">RULES</span></div>
        <div style="font-size:.78rem;line-height:1.55;">
          <strong>1.</strong> <code>(</code> → 新增 left child，下移到 left；push parent。<br>
          <strong>2.</strong> <code>+ - * /</code> → 設 root 為運算子，新增 right child，下移到 right；push parent。<br>
          <strong>3.</strong> 數字 → 設 root 為數字，pop 回到 parent。<br>
          <strong>4.</strong> <code>)</code> → pop 回到 parent。
        </div>
      </div>
    </div>
  </div>

  <details class="tree-detail"><summary>為什麼求值要用 postorder？（補充）</summary><div class="tree-detail-body"><div class="info-box green">
    <span class="info-label">為什麼求值要用 postorder？</span>
    要計算一個運算子節點的值，必須先有<strong>左右兩個子樹的值</strong>。這正好是 <strong>postorder（後序）</strong>的拜訪順序：先左子樹、再右子樹、最後 root。<code>evaluate</code> 其實就是 postorder 走訪，再加上在 root 執行運算；解析樹的求值是走訪演算法的一個特例。
  </div></div></details>
{{slot:eval}}
'''

LEGACY['traversals'] = r'''  <p>「走訪」（traversal）就是按某種順序拜訪樹中每個節點。對二元樹有<strong>三種對稱遞迴的走訪</strong>，差別只在「何時拜訪 root」：</p>

  <div class="info-box">
    <span class="info-label">三種走訪的定義</span>
    <strong>Preorder（前序）：</strong>root → 左子樹 → 右子樹<br>
    <strong>Inorder（中序）：</strong>左子樹 → root → 右子樹<br>
    <strong>Postorder（後序）：</strong>左子樹 → 右子樹 → root
    <br><br>
    寫成程式碼時，幾乎就是把定義<strong>逐字翻譯</strong>，因為樹本身就是遞迴定義的。
  </div>
{{slot:book}}

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div class="tree-canvas" id="canvas-trav" style="height:300px;">
          <svg class="edges-layer"></svg>
          <div class="nodes-layer"></div>
        </div>
        <div class="status-banner"><span class="status-icon">›</span><span class="status-text" id="travStatus">選擇走訪方式並按「開始」</span></div>
        <div class="traversal-output" id="travOutput"><span style="color:rgba(255,255,255,.4)">輸出將顯示在此 →</span></div>
        <div class="preset-row">
          <button class="preset-btn active" data-trav="preorder">Preorder 前序</button>
          <button class="preset-btn" data-trav="inorder">Inorder 中序</button>
          <button class="preset-btn" data-trav="postorder">Postorder 後序</button>
        </div>
        <div class="preset-row">
          <button class="preset-btn active" data-tree="parse">解析樹 (3+(4*5))</button>
          <button class="preset-btn" data-tree="bst">BST 範例</button>
          <button class="preset-btn" data-tree="balanced">cppds 走訪範例樹</button>
          <button class="preset-btn" data-tree="book">講義：書的章節樹</button>
        </div>
        <div class="controls-bar">
          <button class="btn btn-play" id="travPlay">▶ 開始</button>
          <button class="btn btn-step" id="travStep">→ 單步</button>
          <button class="btn btn-reset" id="travReset">↺ 重置</button>
          <div style="flex:1;min-width:160px;display:flex;align-items:center;gap:.5rem;">
            <span style="font-size:.78rem;color:var(--muted);">速度</span>
            <input type="range" id="travSpeed" min="200" max="1800" step="100" value="700" style="flex:1;accent-color:var(--accent3);">
          </div>
        </div>
      </div>
    </div>

    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">虛擬碼 <span class="ic-badge" style="background:var(--accent2)">CODE</span></div>
        <div class="pseudo-code" id="travCode"><span class="line">#include &quot;pythonds3/cppds/binarytree.hpp&quot;</span>
<span class="line" data-l="1"><span class="kw">void</span> <span class="fn">preorder</span>(BinaryTree* tree) {</span>
<span class="line" data-l="2">    <span class="kw">if</span> (tree != <span class="num">NULL</span>) {</span>
<span class="line" data-l="3">        cout &lt;&lt; tree-&gt;<span class="fn">getRootVal</span>() &lt;&lt; <span class="str">" "</span>;   <span class="com">// root</span></span>
<span class="line" data-l="4">        <span class="fn">preorder</span>(tree-&gt;<span class="fn">getLeftChild</span>());</span>
<span class="line" data-l="5">        <span class="fn">preorder</span>(tree-&gt;<span class="fn">getRightChild</span>());</span>
<span class="line">    }</span>
<span class="line">}</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">遞迴呼叫堆疊 <span class="ic-badge" style="background:var(--accent2)">STACK</span></div>
        <div class="stack-vis" id="travStack">
          <div class="stack-label">call stack ↓</div>
        </div>
      </div>
      <details class="tree-detail"><summary>三種走訪的用途（補充）</summary><div class="tree-detail-body"><div class="info-card">
        <div class="ic-title">用途</div>
        <div style="font-size:.83rem;line-height:1.55;">
          <strong>Preorder</strong>：複製樹、序列化、目錄列表（先列父再進子）。<br>
          <strong>Inorder</strong>：BST 上得到<strong>排序輸出</strong>；解析樹上得到中序運算式。<br>
          <strong>Postorder</strong>：解析樹的<strong>運算式求值</strong>、刪除整棵樹（先刪 child 才能釋放 parent）。
        </div>
      </div></div></details>
    </div>
  </div>
{{slot:code}}
  <details class="tree-detail"><summary>小實驗：對解析樹 (3+(4*5)) 做三種走訪（補充）</summary><div class="tree-detail-body"><div class="info-box warm">
    <span class="info-label">小實驗：對解析樹 (3+(4*5)) 做三種走訪</span>
    <div class="table-scroll" tabindex="0" aria-label="比較表，可左右捲動"><table style="width:100%;font-family:'JetBrains Mono',monospace;font-size:.86rem;margin-top:.4rem;">
      <tr><td style="padding:.3rem;width:35%;"><strong>Preorder</strong></td><td>+ 3 * 4 5</td><td style="color:var(--muted);">前序（prefix）形式</td></tr>
      <tr style="background:#fef0e7;"><td style="padding:.3rem;"><strong>Inorder</strong></td><td>3 + 4 * 5</td><td style="color:var(--muted);">中序（沒有括號，看不出運算順序）</td></tr>
      <tr><td style="padding:.3rem;"><strong>Postorder</strong></td><td>3 4 5 * +</td><td style="color:var(--muted);">後序（postfix）形式</td></tr>
    </table></div>
    這也是<strong>後序式（RPN）</strong>能用 stack 直接計算的原因：照 postorder 的順序，可以一邊讀一邊算。
  </div></div></details>
{{slot:printexp}}
'''

LEGACY['heap'] = r'''  <p>優先佇列每次取出優先權最高的元素。若用 <code>vector</code>，維持排序會讓取最小為 $O(1)$、插入因搬移而為 $O(n)$；不排序則插入 $O(1)$、尋找並刪除最小值 $O(n)$。<strong>Binary heap</strong> 讓 insert 與 delete-min 都是 $O(\log n)$。</p>
{{slot:ops}}

  <div class="info-box">
    <span class="info-label">cppds §8.8：Priority Queue Example</span>
    排程工作 <code>(2, compile)</code>、<code>(5, backup)</code>、<code>(1, interrupt)</code>、<code>(3, render)</code> 放進 min-heap 後，依序取出 interrupt、compile、render、backup。Heap 只保證 root 是當前最小者，不會把其餘元素完整排序。
  </div>

{{slot:figs}}

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div class="tree-canvas" id="canvas-heap" style="height:280px;">
          <svg class="edges-layer"></svg>
          <div class="nodes-layer"></div>
        </div>
        <div style="margin-top:.5rem;font-family:'JetBrains Mono',monospace;font-size:.74rem;color:var(--muted);">陣列表示（heap[i]）：</div>
        <div class="heap-list" id="heapList"></div>
        <div class="status-banner"><span class="status-icon">›</span><span class="status-text" id="heapStatus">選擇操作後按「開始」</span></div>
        <div class="preset-row">
          <button class="preset-btn active" data-op="insert">Insert</button>
          <button class="preset-btn" data-op="delete">Delete-min</button>
          <button class="preset-btn" data-op="heapify">Heapify (建堆積)</button>
        </div>
        <div class="preset-row">
          <button class="preset-btn" data-heapdemo="insert" data-arr="5, 9, 11, 14, 18, 19, 21, 33, 17, 27" data-key="7" data-msg="講義圖的 heap，插入 7：按「開始」或「單步」看 percUp">講義：插入 7</button>
          <button class="preset-btn" data-heapdemo="delete" data-arr="5, 9, 11, 14, 18, 19, 21, 33, 17, 27" data-msg="講義圖的 heap：按「開始」或「單步」看 delMin 與 percDown">講義：delMin</button>
          <button class="preset-btn" data-heapdemo="heapify" data-arr="9, 6, 5, 2, 3" data-msg="講義的 [9, 6, 5, 2, 3]：按「開始」或「單步」看 buildHeap">講義：buildHeap [9, 6, 5, 2, 3]</button>
        </div>
        <div class="input-row" id="heapInsertRow">
          <label>插入 key：</label>
          <input type="number" id="heapInsertKey" value="7" style="width:80px;">
          <button class="btn btn-shuffle" id="heapInsertBtn">插入</button>
          <span style="font-size:.78rem;color:var(--muted);">當前 heap：</span>
          <input type="text" id="heapArrInput" value="5, 9, 11, 14, 18, 19, 21, 33, 17, 27" style="flex:1;min-width:140px;">
          <button class="btn btn-reset" id="heapApplyArr">套用</button>
        </div>
        <div class="controls-bar">
          <button class="btn btn-play" id="heapPlay">▶ 開始</button>
          <button class="btn btn-step" id="heapStep">→ 單步</button>
          <button class="btn btn-reset" id="heapReset">↺ 重置</button>
          <div style="flex:1;min-width:160px;display:flex;align-items:center;gap:.5rem;">
            <span style="font-size:.78rem;color:var(--muted);">速度</span>
            <input type="range" id="heapSpeed" min="200" max="2000" step="100" value="700" style="flex:1;accent-color:var(--accent3);">
          </div>
        </div>
      </div>
    </div>

    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">即時統計 <span class="ic-badge">LIVE</span></div>
        <div class="stats-grid">
          <div class="stat-tile"><div class="stat-label">交換次數</div><div class="stat-value" id="heapSwap">0</div></div>
          <div class="stat-tile"><div class="stat-label">比較次數</div><div class="stat-value" id="heapCmp">0</div></div>
        </div>
        <div class="ic-row" style="margin-top:.6rem;"><span class="ic-label">當前索引 i</span><span class="ic-value highlight" id="heapIdx">—</span></div>
        <div class="ic-row"><span class="ic-label">parent (i-1)/2</span><span class="ic-value" id="heapPar">—</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">虛擬碼 <span class="ic-badge" style="background:var(--accent2)">CODE</span></div>
        <div class="pseudo-code" id="heapCode" style="font-size:.74rem;"><span class="line"><span class="com">// BinaryHeap 的成員函式（binaryheap.hpp）</span></span>
<span class="line" data-l="1"><span class="kw">void</span> <span class="fn">insert</span>(<span class="kw">int</span> item) {</span>
<span class="line" data-l="2">    heap.<span class="fn">push_back</span>(item);</span>
<span class="line" data-l="3">    <span class="fn">percUp</span>(heap.<span class="fn">size</span>() - <span class="num">1</span>);</span>
<span class="line" data-l="4">}</span>
<span class="line" data-l="5"><span class="kw">void</span> <span class="fn">percUp</span>(<span class="kw">int</span> i) {</span>
<span class="line" data-l="6">    <span class="kw">while</span> (i &gt; <span class="num">0</span>) {</span>
<span class="line" data-l="7">        <span class="kw">int</span> parentIdx = (i - <span class="num">1</span>) / <span class="num">2</span>;</span>
<span class="line" data-l="8">        <span class="kw">if</span> (heap[i] &lt; heap[parentIdx]) {</span>
<span class="line" data-l="9">            <span class="fn">swap</span>(heap[i], heap[parentIdx]);</span>
<span class="line" data-l="10">        } <span class="kw">else</span> {</span>
<span class="line" data-l="11">            <span class="kw">break</span>;</span>
<span class="line" data-l="12">        }</span>
<span class="line" data-l="13">        i = parentIdx;</span>
<span class="line" data-l="14">    }</span>
<span class="line" data-l="15">}</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">複雜度</div>
        <div class="ic-row"><span class="ic-label">insert</span><span class="ic-value">$O(\log n)$</span></div>
        <div class="ic-row"><span class="ic-label">delete-min</span><span class="ic-value">$O(\log n)$</span></div>
        <div class="ic-row"><span class="ic-label">get-min</span><span class="ic-value highlight">$O(1)$</span></div>
        <div class="ic-row"><span class="ic-label">heapify</span><span class="ic-value highlight">$O(n)$</span></div>
      </div>
    </div>
  </div>
{{slot:perc}}
{{slot:build}}

{{slot:heapclass}}

  <h3>應用：Heap Sort（堆排序）</h3>
  <p>有了 <code>heapify</code>（$O(n)$）和 $n$ 次 <code>delete-min</code>（每次 $O(\log n)$），教學版可把結果寫到另一個 vector，總時間 $O(n \log n)$、額外空間 $O(n)$。真正的 in-place heapsort 則直接在原陣列管理 heap 範圍。</p>
{{slot:sort}}

'''

LEGACY['bst'] = r'''  <p>Map ADT 把 key 對應到 value（就像 C++ 的 <code>unordered_map</code>）。我們已經學過兩種實作：<strong>排序陣列 + binary search</strong>（搜尋 $O(\log n)$ 但插入 $O(n)$）和<strong>雜湊表</strong>（平均 $O(1)$，但有碰撞風險、鍵沒有順序）。BST 提供第三條路。</p>
{{slot:ops}}

  <details class="tree-detail"><summary>Map 的規則與節點的擁有權（補充）</summary><div class="tree-detail-body"><div class="info-box">
    <span class="info-label">Map 的規則與節點的擁有權</span>
    <code>put(key, value)</code> 遇到重複的 key 時<strong>更新 value、不增加 size</strong>。<code>remove()</code> 會釋放被移除的節點；整棵樹有 destructor、deep copy 與 move，避免兩個物件共用同一批節點。
    平衡樹的子類別透過 protected virtual 的 <code>insertOrAssign()</code> 擴充插入，不會繞過公開的 <code>put()</code> 對 size 的計算。
  </div></div></details>

  <div class="info-box">
    <span class="info-label">BST 性質（BST property）</span>
    對樹中每個節點 $x$：<strong>left subtree 內所有 key &lt; $x$.key &lt; right subtree 內所有 key</strong>。<br>
    這個性質帶來兩個結果：<br>
    1. 從 root 出發比較 key，每一步會<strong>排除整個不可能的子樹，但不保證剛好一半</strong>；成本是 $O(h)$，平衡時才是 $O(\log n)$。<br>
    2. 對 BST 做 <strong>inorder traversal 直接得到排序的 key 序列</strong>。
  </div>
{{slot:impl}}

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div class="tree-canvas" id="canvas-bst" style="height:380px;">
          <svg class="edges-layer"></svg>
          <div class="nodes-layer"></div>
        </div>
        <div class="status-banner"><span class="status-icon">›</span><span class="status-text" id="bstStatus">輸入 key 並選擇操作</span></div>
        <div class="input-row">
          <label>初始 keys：</label>
          <input type="text" id="bstInitInput" value="70, 31, 93, 94, 14, 23, 73">
          <button class="btn btn-reset" id="bstApplyInit">建立樹</button>
          <button class="btn btn-shuffle" id="bstShuffle">隨機</button>
        </div>
        <div class="input-row">
          <label>操作 key：</label>
          <input type="number" id="bstOpKey" value="40" style="width:80px;">
          <button class="btn btn-play" data-bstop="put">put (插入)</button>
          <button class="btn btn-play" data-bstop="get" style="background:var(--accent2);">get (搜尋)</button>
        </div>
        <div class="controls-bar">
          <button class="btn btn-step" id="bstStep">→ 單步</button>
          <button class="btn btn-reset" id="bstReset">↺ 重置</button>
          <div style="flex:1;min-width:160px;display:flex;align-items:center;gap:.5rem;">
            <span style="font-size:.78rem;color:var(--muted);">速度</span>
            <input type="range" id="bstSpeed" min="200" max="1800" step="100" value="700" style="flex:1;accent-color:var(--accent3);">
          </div>
        </div>
      </div>
    </div>

    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">即時狀態 <span class="ic-badge">LIVE</span></div>
        <div class="ic-row"><span class="ic-label">當前操作</span><span class="ic-value highlight" id="bstOpName">—</span></div>
        <div class="ic-row"><span class="ic-label">比較次數</span><span class="ic-value" id="bstCmp">0</span></div>
        <div class="ic-row"><span class="ic-label">當前 node</span><span class="ic-value" id="bstCur">—</span></div>
        <div class="ic-row"><span class="ic-label">樹高度</span><span class="ic-value" id="bstHeight">—</span></div>
        <div class="ic-row"><span class="ic-label">節點數</span><span class="ic-value" id="bstSize">—</span></div>
        <div class="ic-row"><span class="ic-label">結果</span><span class="ic-value" id="bstResult">—</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title" id="bstCodeTitle">虛擬碼 — put <span class="ic-badge" style="background:var(--accent2)">CODE</span></div>
        <details class="tree-detail tree-code-fold"><summary>程式：put 的簡化版（展開後可看動畫逐行高亮）</summary><div class="pseudo-code" id="bstCode" style="font-size:.73rem;">
<span class="line"><span class="kw">#include</span> &lt;string&gt;</span>
<span class="line"><span class="kw">struct</span> TreeNode {</span>
<span class="line">    std::string key, value;</span>
<span class="line">    TreeNode *leftChild = <span class="kw">nullptr</span>, *rightChild = <span class="kw">nullptr</span>, *parent = <span class="kw">nullptr</span>;</span>
<span class="line">    TreeNode(std::string k, std::string v, TreeNode* p = <span class="kw">nullptr</span>)</span>
<span class="line">        : key(k), value(v), parent(p) {}</span>
<span class="line">};</span>
<span class="line" data-l="1"><span class="kw">void</span> <span class="fn">put</span>(<span class="kw">const</span> std::string&amp; key, <span class="kw">const</span> std::string&amp; value, TreeNode* currentNode) {</span>
<span class="line" data-l="2">    <span class="kw">if</span> (key == currentNode->key) { currentNode->value = value; <span class="kw">return</span>; }</span>
<span class="line" data-l="3">    <span class="kw">if</span> (key &lt; currentNode->key) {</span>
<span class="line" data-l="4">        <span class="kw">if</span> (currentNode->leftChild != <span class="kw">nullptr</span>)</span>
<span class="line" data-l="5">            <span class="fn">put</span>(key, value, currentNode->leftChild);</span>
<span class="line" data-l="6">        <span class="kw">else</span> currentNode->leftChild = <span class="kw">new</span> <span class="fn">TreeNode</span>(key, value, currentNode);</span>
<span class="line" data-l="7">    } <span class="kw">else</span> {</span>
<span class="line" data-l="8">        <span class="kw">if</span> (currentNode->rightChild != <span class="kw">nullptr</span>)</span>
<span class="line" data-l="9">            <span class="fn">put</span>(key, value, currentNode->rightChild);</span>
<span class="line" data-l="10">        <span class="kw">else</span></span>
<span class="line" data-l="11">            currentNode->rightChild = <span class="kw">new</span> <span class="fn">TreeNode</span>(key, value, currentNode);</span>
<span class="line">    }</span>
<span class="line">}</span>
</div></details>
      </div>
    </div>
  </div>

  <details class="tree-detail"><summary>build BST 的順序很重要（補充）</summary><div class="tree-detail-body"><div class="info-box warm">
    <span class="info-label">build BST 的順序很重要</span>
    把 keys $70, 31, 93, 94, 14, 23, 73$ 依序插入會得到一棵還算平衡的 BST；但若插入順序是 $14, 23, 31, 70, 73, 93, 94$（已排序），<strong>新樹會退化成一條鏈</strong>：高度從 $O(\log n)$ 變成 $O(n)$。試試上面的「隨機」按鈕和輸入排序的 keys 比較看看。<a href="#bst-analysis">BST 的限制</a>一節會分析這種退化，<a href="#avl">AVL Tree</a> 一節再說明怎麼避免。
  </div></div></details>
{{slot:get}}

'''

LEGACY['bst-delete'] = r'''  <p>BST 的 <code>put</code> 與 <code>get</code> 直觀，但<strong>刪除是最麻煩的操作</strong>，因為刪掉一個內部節點後，必須維持 BST 性質。我們把情境分成三類：</p>

  <details class="tree-detail"><summary>三種刪除情境的整理</summary><div class="tree-detail-body"><div class="info-box red">
    <span class="info-label">三種刪除情境</span>
    <strong>Case 1：要刪的是葉節點。</strong>直接把 parent 的指標設為 <code>NULL</code>。最簡單。<br>
    <strong>Case 2：要刪的節點只有<em>一個</em>子節點。</strong>把這個 child「提升」上來取代被刪節點。<br>
    <strong>Case 3：要刪的節點有<em>兩個</em>子節點。</strong>找它的 <strong>in-order successor（中序後繼）</strong>（也就是右子樹中 key 最小的節點），把它的 key 複製到當前節點，然後從原位置「splice out」successor。
  </div></div></details>
{{slot:cases}}


  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div class="tree-canvas" id="canvas-bstdel" style="height:360px;">
          <svg class="edges-layer"></svg>
          <div class="nodes-layer"></div>
        </div>
        <div class="status-banner"><span class="status-icon">›</span><span class="status-text" id="delStatus">點選樹中節點選擇要刪除的 key</span></div>
        <div class="input-row">
          <label>樹結構（依序插入）：</label>
          <input type="text" id="delInitInput" value="50, 30, 70, 20, 40, 60, 80, 35, 45, 75">
          <button class="btn btn-reset" id="delApplyInit">建立樹</button>
        </div>
        <div class="input-row">
          <label>刪除 key：</label>
          <input type="number" id="delKey" value="30" style="width:80px;">
          <button class="btn btn-play" id="delPlay">▶ 刪除</button>
          <button class="btn btn-step" id="delStep">→ 單步</button>
          <button class="btn btn-reset" id="delReset">↺ 重建</button>
          <div style="flex:1;min-width:120px;display:flex;align-items:center;gap:.5rem;">
            <span style="font-size:.78rem;color:var(--muted);">速度</span>
            <input type="range" id="delSpeed" min="200" max="1800" step="100" value="700" style="flex:1;accent-color:var(--accent3);">
          </div>
        </div>
        <div class="preset-row">
          <button class="preset-btn" data-delk="20">Case 1：刪 20（葉）</button>
          <button class="preset-btn" data-delk="80">Case 2：刪 80（一子）</button>
          <button class="preset-btn" data-delk="30">Case 3：刪 30（兩子）</button>
          <button class="preset-btn" data-delk="50">Case 3：刪 50（root）</button>
        </div>
      </div>
    </div>

    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">當前情境 <span class="ic-badge">CASE</span></div>
        <div class="ic-row"><span class="ic-label">情境</span><span class="ic-value highlight" id="delCase">—</span></div>
        <div class="ic-row"><span class="ic-label">target key</span><span class="ic-value" id="delTarget">—</span></div>
        <div class="ic-row"><span class="ic-label">successor</span><span class="ic-value" id="delSucc">—</span></div>
        <div class="ic-row"><span class="ic-label">階段</span><span class="ic-value" id="delPhase">—</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">刪除流程與 findSuccessor <span class="ic-badge" style="background:var(--accent2)">CODE</span></div>
        <details class="tree-detail tree-code-fold"><summary>程式：刪除流程與 findSuccessor（展開後可看動畫逐行高亮）</summary><div class="pseudo-code" id="delCode" style="font-size:.72rem;"><span class="line" data-l="1">TreeNode* currentNode = <span class="fn">_get</span>(key, root);</span>
<span class="line" data-l="2"><span class="kw">if</span> (currentNode-&gt;<span class="fn">isLeaf</span>()) {               <span class="com">// Case 1</span></span>
<span class="line" data-l="3">    <span class="com">// 父節點指向它的指標改成 NULL</span></span>
<span class="line" data-l="4">} <span class="kw">else if</span> (currentNode-&gt;<span class="fn">hasBothChildren</span>()) { <span class="com">// Case 3</span></span>
<span class="line" data-l="5">    TreeNode* successor = currentNode-&gt;<span class="fn">findSuccessor</span>();</span>
<span class="line" data-l="6">    successor-&gt;<span class="fn">spliceOut</span>();</span>
<span class="line" data-l="7">    currentNode-&gt;key = successor-&gt;key;   <span class="com">// value 也一起搬</span></span>
<span class="line" data-l="8">} <span class="kw">else</span> {                                  <span class="com">// Case 2</span></span>
<span class="line" data-l="9">    <span class="com">// 唯一的子節點接到父節點原本指向它的位置</span></span>
<span class="line" data-l="10">}</span>
<span class="line" data-l="11">TreeNode* <span class="fn">findSuccessor</span>() {</span>
<span class="line" data-l="12">    <span class="kw">if</span> (rightChild != <span class="num">NULL</span>) <span class="kw">return</span> rightChild-&gt;<span class="fn">findMin</span>();</span>
<span class="line" data-l="13">    <span class="kw">return</span> <span class="num">NULL</span>;</span>
<span class="line" data-l="14">}</span>
<span class="line" data-l="15">TreeNode* <span class="fn">findMin</span>() {</span>
<span class="line" data-l="16">    TreeNode* cur = <span class="kw">this</span>;</span>
<span class="line" data-l="17">    <span class="kw">while</span> (cur-&gt;leftChild != <span class="num">NULL</span>)</span>
<span class="line" data-l="18">        cur = cur-&gt;leftChild;</span>
<span class="line" data-l="19">    <span class="kw">return</span> cur;</span>
<span class="line" data-l="20">}</span></div></details>
      </div>
      <div class="info-card">
        <div class="ic-title">圖例</div>
        <div style="font-size:.78rem;line-height:1.55;">
          <span class="legend-item"><span class="lg-swatch" style="background:var(--node-current)"></span>要刪除的節點</span><br>
          <span class="legend-item"><span class="lg-swatch" style="background:var(--node-target)"></span>successor</span><br>
          <span class="legend-item"><span class="lg-swatch" style="background:#e67e22"></span>搜尋路徑</span>
        </div>
      </div>
    </div>
  </div>

  <h3>講義的完整拼圖：findSuccessor 三情境與 spliceOut</h3>
  <p>側欄的 findSuccessor 是刪除專用的精簡版（刪除時節點必有右子樹，successor 就是右子樹的最小值）。
  一般的 successor 有三種情境（下方左欄），另外兩種在沒有右子樹、需要往上找時才用得到。
  successor 找到之後，用 <code>spliceOut()</code> 把它從原位置「縫」出來：
  successor 保證最多一個 child，所以只有兩種縫法。</p>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:.8rem;">
    <div class="info-card"><div class="ic-title">findSuccessor 完整版（TreeNode 的方法） <span class="ic-badge">CODE</span></div>
      <details class="tree-detail tree-code-fold"><summary>程式：findSuccessor 完整版</summary><div class="pseudo-code" style="font-size:.72rem;">
<span class="line">TreeNode* <span class="fn">findSuccessor</span>() {</span>
<span class="line">    TreeNode* successor = <span class="num">NULL</span>;</span>
<span class="line">    <span class="kw">if</span> (rightChild != <span class="num">NULL</span>) {          <span class="com">// 情境 1：有右子樹</span></span>
<span class="line">        successor = rightChild-&gt;<span class="fn">findMin</span>();</span>
<span class="line">    } <span class="kw">else if</span> (parent != <span class="num">NULL</span>) {</span>
<span class="line">        <span class="kw">if</span> (<span class="fn">isLeftChild</span>()) {           <span class="com">// 情境 2：自己是左子 → 父就是後繼</span></span>
<span class="line">            successor = parent;</span>
<span class="line">        } <span class="kw">else</span> {                       <span class="com">// 情境 3：暫時斷開自己，問父親</span></span>
<span class="line">            parent-&gt;rightChild = <span class="num">NULL</span>;</span>
<span class="line">            successor = parent-&gt;<span class="fn">findSuccessor</span>();</span>
<span class="line">            parent-&gt;rightChild = <span class="kw">this</span>;</span>
<span class="line">        }</span>
<span class="line">    }</span>
<span class="line">    <span class="kw">return</span> successor;</span>
<span class="line">}</span></div></details>
      <div style="font-size:.8rem;color:var(--muted);margin-top:.3rem;">刪除只會用到情境 1：Case 3 的節點一定有右子樹。</div></div>
    <div class="info-card"><div class="ic-title">spliceOut ＋ Case 3 呼叫端 <span class="ic-badge">CODE</span></div>
      <details class="tree-detail tree-code-fold"><summary>程式：spliceOut 與 Case 3 呼叫端</summary><div class="pseudo-code" style="font-size:.72rem;">
<span class="line"><span class="kw">void</span> <span class="fn">spliceOut</span>() {</span>
<span class="line">    <span class="kw">if</span> (<span class="fn">isLeaf</span>()) {                    <span class="com">// 縫法 1：葉節點直接拆</span></span>
<span class="line">        <span class="kw">if</span> (<span class="fn">isLeftChild</span>()) parent-&gt;leftChild = <span class="num">NULL</span>;</span>
<span class="line">        <span class="kw">else</span>               parent-&gt;rightChild = <span class="num">NULL</span>;</span>
<span class="line">    } <span class="kw">else if</span> (<span class="fn">hasAnyChild</span>()) {        <span class="com">// 縫法 2：孩子上位</span></span>
<span class="line">        TreeNode* child = (leftChild != <span class="num">NULL</span>) ? leftChild : rightChild;</span>
<span class="line">        <span class="kw">if</span> (<span class="fn">isLeftChild</span>()) parent-&gt;leftChild = child;</span>
<span class="line">        <span class="kw">else</span>               parent-&gt;rightChild = child;</span>
<span class="line">        child-&gt;parent = parent;</span>
<span class="line">    }</span>
<span class="line">}</span>
<span class="line"> </span>
<span class="line"><span class="com">// remove 的 Case 3 分支長這樣：</span></span>
<span class="line">TreeNode* successor = currentNode-&gt;<span class="fn">findSuccessor</span>();</span>
<span class="line">successor-&gt;<span class="fn">spliceOut</span>();</span>
<span class="line">currentNode-&gt;key   = successor-&gt;key;   <span class="com">// 只搬 key/value</span></span>
<span class="line">currentNode-&gt;value = successor-&gt;value; <span class="com">// 節點本身不動</span></span>
<span class="line"><span class="kw">delete</span> successor;</span></div></details></div>
  </div>
{{slot:inorder}}
'''

LEGACY['bst-analysis'] = r'''  <p>BST 的 <code>put</code>、<code>get</code>、<code>contains</code>、<code>remove</code> 都沿 root-to-leaf path 前進，時間複雜度正比於<strong>樹高 $h$</strong>。所以關鍵問題是：給定 $n$ 個節點，$h$ 會是多少？</p>

  <details class="tree-detail"><summary>高度與節點數的關係（補充）</summary><div class="tree-detail-body"><div class="info-box">
    <span class="info-label">高度與節點數的關係</span>
    完美平衡二元樹（每層填滿）有 $2^{h+1}-1$ 個節點，所以 $h \approx \log_2 n$。<br>
    若 keys 隨機插入，高度期望也是 $O(\log n)$，因為大概一半 key 進左、一半進右。<br>
    但<strong>最差情況 $h = n - 1$</strong>：把已排序 keys 依序插入就會發生：每個新節點都比當前所有節點大（或小），永遠落到右（或左）這一支，BST 退化成鏈結串列。
  </div></div></details>
{{slot:skew}}

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
          <div>
            <h4 style="font-family:'JetBrains Mono',monospace;font-size:.85rem;color:var(--accent3);margin-bottom:.4rem;">隨機順序插入</h4>
            <div class="tree-canvas" id="canvas-bstrand" style="height:280px;">
              <svg class="edges-layer"></svg>
              <div class="nodes-layer"></div>
            </div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:.78rem;text-align:center;margin-top:.4rem;">
              height = <span id="bstRandH" style="color:var(--accent3);font-weight:700;font-size:1.1rem;">—</span>
            </div>
          </div>
          <div>
            <h4 style="font-family:'JetBrains Mono',monospace;font-size:.85rem;color:var(--accent);margin-bottom:.4rem;">已排序順序插入</h4>
            <div class="tree-canvas" id="canvas-bstsorted" style="height:280px;">
              <svg class="edges-layer"></svg>
              <div class="nodes-layer"></div>
            </div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:.78rem;text-align:center;margin-top:.4rem;">
              height = <span id="bstSortedH" style="color:var(--accent);font-weight:700;font-size:1.1rem;">—</span>
            </div>
          </div>
        </div>
        <div class="input-row">
          <label>節點數 n：</label>
          <input type="number" id="bstAnalN" value="10" min="3" max="20" style="width:70px;">
          <button class="btn btn-shuffle" id="bstAnalRegen">重新產生並比較</button>
        </div>
      </div>
    </div>

    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">複雜度對照</div>
        <div class="table-scroll" tabindex="0" aria-label="比較表，可左右捲動"><table class="cmp-table" style="font-size:.78rem;">
          <thead><tr><th>操作</th><th>平均</th><th>最差</th></tr></thead>
          <tbody>
            <tr><td>put</td><td class="best">$O(\log n)$</td><td class="worst">$O(n)$</td></tr>
            <tr><td>get</td><td class="best">$O(\log n)$</td><td class="worst">$O(n)$</td></tr>
            <tr><td>remove</td><td class="best">$O(\log n)$</td><td class="worst">$O(n)$</td></tr>
          </tbody>
        </table></div>
      </div>
      <details class="tree-detail"><summary>應用：Tree Sort（補充）</summary><div class="tree-detail-body"><div class="info-card">
        <div class="ic-title">應用：Tree Sort</div>
        <div style="font-size:.83rem;line-height:1.55;">
          把 $n$ 個 keys 全部 <code>put</code> 進 BST 再做 inorder traversal，平均得到 $O(n \log n)$ 的排序。但最差情況退化為 $O(n^2)$，這也是 quick sort 在最差情況下退化的同一個原因（pivot 選不好等於插入排序好的 keys 進 BST）。
        </div>
      </div></div></details>
    </div>
  </div>
'''

LEGACY['avl'] = r'''  <p>BST 退化的原因是<strong>插入順序</strong>。AVL 樹（Adelson-Velsky 和 Landis，1962）讓樹在每次插入／刪除時<strong>自動旋轉</strong>，保證它一直是「近似平衡」。代價只是常數因子的開銷。</p>

  <div class="info-box">
    <span class="info-label">balance factor（平衡因子）</span>
    對每個節點 $x$，定義 $\text{bf}(x) = \text{height}(x.\text{left}) - \text{height}(x.\text{right})$。<br>
    AVL 規則：<strong>每個節點的 bf 必須是 $-1$、$0$ 或 $+1$</strong>。超出這個範圍的節點會觸發旋轉來修正。<br>
    bf $&gt; 0$：left-heavy；bf $&lt; 0$：right-heavy；bf $= 0$：完美平衡。
  </div>
{{slot:bf}}

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div class="tree-canvas" id="canvas-avl" style="height:380px;">
          <svg class="edges-layer"></svg>
          <div class="nodes-layer"></div>
        </div>
        <div class="status-banner"><span class="status-icon">›</span><span class="status-text" id="avlStatus">選擇旋轉情境並按「執行」</span></div>
        <div class="preset-row">
          <button class="preset-btn active" data-avlcase="LL">LL：右旋</button>
          <button class="preset-btn" data-avlcase="RR">RR：左旋</button>
          <button class="preset-btn" data-avlcase="LR">LR：左右旋</button>
          <button class="preset-btn" data-avlcase="RL">RL：右左旋</button>
        </div>
        <div class="controls-bar">
          <button class="btn btn-play" id="avlPlay">▶ 執行旋轉</button>
          <button class="btn btn-step" id="avlStep">→ 單步</button>
          <button class="btn btn-reset" id="avlReset">↺ 重置</button>
          <div style="flex:1;min-width:160px;display:flex;align-items:center;gap:.5rem;">
            <span style="font-size:.78rem;color:var(--muted);">速度</span>
            <input type="range" id="avlSpeed" min="300" max="2000" step="100" value="900" style="flex:1;accent-color:var(--accent3);">
          </div>
        </div>
      </div>
    </div>

    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">當前情境 <span class="ic-badge">CASE</span></div>
        <div class="ic-row"><span class="ic-label">不平衡類型</span><span class="ic-value highlight" id="avlCase">LL</span></div>
        <div class="ic-row"><span class="ic-label">解法</span><span class="ic-value" id="avlFix">右旋 (Right Rotate)</span></div>
        <div class="ic-row"><span class="ic-label">平衡因子 bf</span><span class="ic-value" id="avlBf">—</span></div>
        <div class="ic-row"><span class="ic-label">階段</span><span class="ic-value" id="avlPhase">—</span></div>
      </div>
      <details class="tree-detail"><summary>四種旋轉的整理</summary><div class="tree-detail-body"><div class="info-card">
        <div class="ic-title">四種旋轉</div>
        <div style="font-size:.8rem;line-height:1.55;">
          <strong>LL（左左不平衡）：</strong>對 root 做<strong>單一右旋</strong>。<br>
          <strong>RR（右右不平衡）：</strong>對 root 做<strong>單一左旋</strong>。<br>
          <strong>LR（左右不平衡）：</strong>先對 left child 左旋，再對 root 右旋。<br>
          <strong>RL（右左不平衡）：</strong>先對 right child 右旋，再對 root 左旋。
        </div>
      </div></div></details>
      <details class="tree-detail"><summary>高度上界的整理</summary><div class="tree-detail-body"><div class="info-card">
        <div class="ic-title">高度上界</div>
        <div class="eq-card">
          <div class="eq-label">AVL HEIGHT BOUND</div>
          <div class="eq-formula">$h &lt; 1.44 \log_2(n+1)$</div>
          <div class="eq-sub">由 Fibonacci 樹（最瘦的 AVL 樹）推導</div>
        </div>
      </div></div></details>
    </div>
  </div>

<p style="font-size:.88rem;color:var(--muted);">AVL 的效能分析與實作細節屬於選讀內容。課堂上只要知道：插入後沿路更新平衡因子，LL、RR 不平衡做一次旋轉，LR、RL 做兩次，每次旋轉 $O(1)$。</p>
<details class="tree-detail tree-optional"><summary>選讀：AVL 樹的效能分析與實作（cppds §8.16–8.17）</summary><div class="tree-detail-body">
{{slot:perf}}
  <div class="info-box green">
    <span class="info-label">為什麼是 1.44 log n？</span>
    最瘦的 AVL 樹滿足 $N_h = 1 + N_{h-1} + N_{h-2}$、$N_0=1$、$N_1=2$，所以 <strong>$N_h=F_{h+3}-1$</strong>。當 $h$ 很大時 $N_h \approx \Phi^{h+3}/\sqrt 5-1$。反解得到的是<strong>高度上界</strong>而非每棵 AVL 的精確等式：
    $$ h = O(\log n),\qquad h < 1.44\log_2(n+1) $$
    這比完美平衡的 $\log_2 n$ 只大了一個常數因子，<strong>所有 BST 操作仍是 $O(\log n)$</strong>。
  </div>

  <h3>實作內幕：updateBalance、rotateLeft、rebalance <span class="sec-badge">cppds §8.17 · 選讀</span></h3>
  <p>AVL 的 <code>insertOrAssign()</code> 跟 BST 幾乎一樣，唯一差別是掛上新節點後多呼叫一次
  <code>updateBalance()</code>：它沿著 parent 指標往上修正平衡因子，
  一發現 |bf| &gt; 1 就地 <code>rebalance()</code>。旋轉最多兩次、每次 O(1)，
  往上修正最多走 log n 層，所以 <strong>put 整體仍是 O(log n)</strong>。
  上面的動畫可以對照著看：四個按鈕（LL/RR/LR/RL）正是 rebalance 的四個分支。刪除後的重平衡，講義留作練習。</p>

{{slot:rot}}
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:.8rem;">
    <div class="info-card"><div class="ic-title">insertOrAssign() 的差異 ＋ updateBalance <span class="ic-badge">CODE</span></div>
      <details class="tree-detail tree-code-fold"><summary>程式：insertOrAssign() 的差異與 updateBalance</summary><p class="dx-note">這段的 <code>TreeNode*&amp; slot</code> 是「指標的參考」，修改 slot 會一起改到呼叫端保存的指標；<code>auto*</code> 讓編譯器推導指向的型別。<code>static_cast&lt;AVLTreeNode*&gt;(slot)</code> 把基底類別指標轉成衍生類別指標，前提是本樹的節點確實都由 AVLTreeNode 建立；它不會在執行時檢查型別，不能拿來轉換任意 TreeNode。<code>override</code> 要求編譯器確認此函式覆寫基底類別的 virtual 函式。</p><div class="pseudo-code" style="font-size:.72rem;">
<span class="line" data-l="1"><span class="com">// insertOrAssign() 的差異：新葉掛上後多呼叫一次 updateBalance</span></span>
<span class="line" data-l="2"><span class="kw">bool</span> <span class="fn">insertOrAssign</span>(string key, string value,</span>
<span class="line" data-l="3">                    TreeNode*&amp; slot, TreeNode* parent) <span class="kw">override</span> {</span>
<span class="line" data-l="4">    <span class="kw">if</span> (slot == <span class="fn">NULL</span>) {</span>
<span class="line" data-l="5">        <span class="kw">auto</span>* node = <span class="kw">new</span> AVLTreeNode(key, value, <span class="num">0</span>, parent);</span>
<span class="line" data-l="6">        slot = node;</span>
<span class="line" data-l="7">        updateBalance(node);</span>
<span class="line" data-l="8">        <span class="kw">return</span> <span class="fn">true</span>;</span>
<span class="line" data-l="9">    }</span>
<span class="line" data-l="10">    <span class="kw">auto</span>* current = <span class="kw">static_cast</span>&lt;AVLTreeNode*&gt;(slot);</span>
<span class="line" data-l="11">    <span class="kw">if</span> (key == current-&gt;key) {</span>
<span class="line" data-l="12">        current-&gt;value = value;</span>
<span class="line" data-l="13">        <span class="kw">return</span> <span class="fn">false</span>;</span>
<span class="line" data-l="14">    }</span>
<span class="line" data-l="15">    TreeNode*&amp; child = (key &lt; current-&gt;key)</span>
<span class="line" data-l="16">                     ? current-&gt;leftChild : current-&gt;rightChild;</span>
<span class="line" data-l="17">    <span class="kw">return</span> insertOrAssign(key, value, child, current);</span>
<span class="line" data-l="18">}</span>
<span class="line" data-l="19"> </span>
<span class="line" data-l="20"><span class="kw">void</span> <span class="fn">updateBalance</span>(AVLTreeNode* node) {</span>
<span class="line" data-l="21">    <span class="kw">if</span> (node-&gt;balanceFactor &gt; <span class="num">1</span> ||</span>
<span class="line" data-l="22">        node-&gt;balanceFactor &lt; <span class="num">-1</span>) {</span>
<span class="line" data-l="23">        rebalance(node);   <span class="com">// 就地修，不再往上</span></span>
<span class="line" data-l="24">        <span class="kw">return</span>;</span>
<span class="line" data-l="25">    }</span>
<span class="line" data-l="26">    <span class="kw">if</span> (node-&gt;parent != <span class="fn">NULL</span>) {</span>
<span class="line" data-l="27">        <span class="kw">if</span> (node-&gt;isLeftChild())</span>
<span class="line" data-l="28">            node-&gt;parent-&gt;balanceFactor += <span class="num">1</span>;</span>
<span class="line" data-l="29">        <span class="kw">else</span> <span class="kw">if</span> (node-&gt;isRightChild())</span>
<span class="line" data-l="30">            node-&gt;parent-&gt;balanceFactor -= <span class="num">1</span>;</span>
<span class="line" data-l="31">        <span class="kw">if</span> (node-&gt;parent-&gt;balanceFactor != <span class="num">0</span>)</span>
<span class="line" data-l="32">            updateBalance(node-&gt;parent);  <span class="com">// 繼續往上</span></span>
<span class="line" data-l="33">    }</span>
<span class="line" data-l="34">}</span></div></details></div>
    <div class="info-card"><div class="ic-title">rotateLeft（rotateRight 對稱） <span class="ic-badge">CODE</span></div>
      <details class="tree-detail tree-code-fold"><summary>程式：rotateLeft</summary><div class="pseudo-code" style="font-size:.7rem;">
<span class="line"><span class="kw">void</span> <span class="fn">rotateLeft</span>(AVLTreeNode* rotationRoot) {</span>
<span class="line">    AVLTreeNode* newRoot = rotationRoot-&gt;rightChild;</span>
<span class="line">    rotationRoot-&gt;rightChild = newRoot-&gt;leftChild;</span>
<span class="line">    <span class="kw">if</span> (newRoot-&gt;leftChild != <span class="num">NULL</span>)</span>
<span class="line">        newRoot-&gt;leftChild-&gt;parent = rotationRoot;</span>
<span class="line">    newRoot-&gt;parent = rotationRoot-&gt;parent;</span>
<span class="line">    <span class="kw">if</span> (rotationRoot-&gt;<span class="fn">isRoot</span>())</span>
<span class="line">        root = newRoot;</span>
<span class="line">    <span class="kw">else if</span> (rotationRoot-&gt;<span class="fn">isLeftChild</span>())</span>
<span class="line">        rotationRoot-&gt;parent-&gt;leftChild = newRoot;</span>
<span class="line">    <span class="kw">else</span></span>
<span class="line">        rotationRoot-&gt;parent-&gt;rightChild = newRoot;</span>
<span class="line">    newRoot-&gt;leftChild = rotationRoot;</span>
<span class="line">    rotationRoot-&gt;parent = newRoot;</span>
<span class="line">    rotationRoot-&gt;balanceFactor = rotationRoot-&gt;balanceFactor</span>
<span class="line">        + <span class="num">1</span> - <span class="fn">min</span>(newRoot-&gt;balanceFactor, <span class="num">0</span>);</span>
<span class="line">    newRoot-&gt;balanceFactor = newRoot-&gt;balanceFactor</span>
<span class="line">        + <span class="num">1</span> + <span class="fn">max</span>(rotationRoot-&gt;balanceFactor, <span class="num">0</span>);</span>
<span class="line">}</span></div></details>
      <div style="font-size:.8rem;color:var(--muted);margin-top:.3rem;">難點有二：parent 指標要全部接對；
      最後兩行用 min/max 直接推出新的平衡因子，不用重算高度。</div></div>
    <div class="info-card"><div class="ic-title">rebalance：四情境對照動畫按鈕 <span class="ic-badge">CODE</span></div>
      <details class="tree-detail tree-code-fold"><summary>程式：rebalance</summary><div class="pseudo-code" style="font-size:.72rem;">
<span class="line"><span class="kw">void</span> <span class="fn">rebalance</span>(AVLTreeNode* node) {</span>
<span class="line">    <span class="kw">if</span> (node-&gt;balanceFactor &lt; <span class="num">0</span>) {          <span class="com">// right-heavy</span></span>
<span class="line">        <span class="kw">if</span> (node-&gt;rightChild-&gt;balanceFactor &gt; <span class="num">0</span>) {</span>
<span class="line">            <span class="fn">rotateRight</span>(node-&gt;rightChild);   <span class="com">// RL：先右旋子</span></span>
<span class="line">            <span class="fn">rotateLeft</span>(node);                <span class="com">//     再左旋根</span></span>
<span class="line">        } <span class="kw">else</span> {</span>
<span class="line">            <span class="fn">rotateLeft</span>(node);                <span class="com">// RR：單一左旋</span></span>
<span class="line">        }</span>
<span class="line">    } <span class="kw">else if</span> (node-&gt;balanceFactor &gt; <span class="num">0</span>) {   <span class="com">// left-heavy</span></span>
<span class="line">        <span class="kw">if</span> (node-&gt;leftChild-&gt;balanceFactor &lt; <span class="num">0</span>) {</span>
<span class="line">            <span class="fn">rotateLeft</span>(node-&gt;leftChild);     <span class="com">// LR：先左旋子</span></span>
<span class="line">            <span class="fn">rotateRight</span>(node);               <span class="com">//     再右旋根</span></span>
<span class="line">        } <span class="kw">else</span> {</span>
<span class="line">            <span class="fn">rotateRight</span>(node);               <span class="com">// LL：單一右旋</span></span>
<span class="line">        }</span>
<span class="line">    }</span>
<span class="line">}</span></div></details>
      <div style="font-size:.8rem;color:var(--muted);margin-top:.3rem;">先看「歪向哪邊」，再看「子節點歪向哪邊」決定要不要先轉子節點：跟上面動畫的四個 preset 一一對應。</div></div>
  </div>
{{slot:bfd}}
</div></details>
{{slot:avlquiz}}
'''

LEGACY['summary'] = r'''  <p>第 7 章與本章我們學了四種實作 map ADT 的方式。下表整理 worst-case 複雜度；注意 hash table 的 $O(1)$ 是<strong>平均</strong>，最差情況（全部碰撞）會退化到 $O(n)$。</p>

  <div class="table-scroll" tabindex="0" aria-label="比較表，可左右捲動"><table class="cmp-table">
    <thead>
      <tr>
        <th>operation</th>
        <th>Sorted Vector<br><small>(binary search)</small></th>
        <th>Hash Table<br><small>(平均)</small></th>
        <th>BST<br><small>(最差)</small></th>
        <th>AVL Tree</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>put(key, val)</td>
        <td class="worst">$O(n)$</td>
        <td class="best">$O(1)$</td>
        <td class="worst">$O(n)$</td>
        <td class="best">$O(\log n)$</td>
      </tr>
      <tr>
        <td>get(key)</td>
        <td>$O(\log n)$</td>
        <td class="best">$O(1)$</td>
        <td class="worst">$O(n)$</td>
        <td class="best">$O(\log n)$</td>
      </tr>
      <tr>
        <td>contains(key)</td>
        <td>$O(\log n)$</td>
        <td class="best">$O(1)$</td>
        <td class="worst">$O(n)$</td>
        <td class="best">$O(\log n)$</td>
      </tr>
      <tr>
        <td>remove(key)</td>
        <td class="worst">$O(n)$</td>
        <td class="best">$O(1)$</td>
        <td class="worst">$O(n)$</td>
        <td class="best">$O(\log n)$</td>
      </tr>
      <tr>
        <td>排序輸出 (in-order)</td>
        <td class="best">$O(n)$</td>
        <td class="worst">$O(n \log n)$</td>
        <td class="best">$O(n)$</td>
        <td class="best">$O(n)$</td>
      </tr>
    </tbody>
  </table></div>

  <h3>怎麼選擇實作方式</h3>
  <div class="info-box">
    <span class="info-label">什麼時候選什麼？</span>
    <strong>需要 $O(1)$ 平均、不需要排序：</strong>選 <strong>hash table</strong>（C++ <code>unordered_map</code>、Java <code>HashMap</code>）。<br>
    <strong>需要保證 $O(\log n)$ worst-case、需要排序輸出：</strong>選 <strong>self-balancing BST</strong>（C++ <code>std::map</code>、Java <code>TreeMap</code> 用紅黑樹；AVL 是它的近親）。<br>
    <strong>資料是 read-only 且已排序：</strong>用<strong>陣列 + binary search</strong>，記憶體緊湊、cache 友善。<br>
    <strong>需要快速取出最小/最大值（優先佇列）：</strong>選 <strong>binary heap</strong>（C++ <code>priority_queue</code>），不需要完整排序就能 $O(\log n)$ 操作。
  </div>

{{slot:real}}

'''

# Folded （補充） parts split off the sections above.

LEGACY['lol'] = r'''  <p>巢狀串列版把「根的值」放在第 0 格、左子樹放第 1 格、右子樹放第 2 格；
  每個子樹自己又是同樣格式的串列，<strong>結構本身就是遞迴的</strong>。
  葉節點就是「值＋兩個空串列」。它還有個好處：要表示多元樹（超過兩個子樹），再多掛一個串列就好。</p>
  <div class="info-card" style="max-width:600px;"><div class="ic-title">巢狀串列表示 <span class="ic-badge">CODE</span></div>
    <div class="pseudo-code" style="font-size:.74rem;">
<span class="line">my_tree = [<span class="num">"a"</span>,                        <span class="com"># [0] 根的值</span></span>
<span class="line">    [<span class="num">"b"</span>, [<span class="num">"d"</span>,[],[]], [<span class="num">"e"</span>,[],[]]],  <span class="com"># [1] 左子樹</span></span>
<span class="line">    [<span class="num">"c"</span>, [<span class="num">"f"</span>,[],[]], []        ]]   <span class="com"># [2] 右子樹</span></span>
<span class="line"> </span>
<span class="line">my_tree[<span class="num">0</span>]  <span class="com"># "a"：根</span></span>
<span class="line">my_tree[<span class="num">1</span>]  <span class="com"># 整個左子樹（又是一個同構的串列）</span></span>
<span class="line">my_tree[<span class="num">2</span>]  <span class="com"># 整個右子樹</span></span></div></div>
  <p style="font-size:.88rem;color:var(--muted);">C++ 是靜態型別語言，寫不出這種「值和串列混住」的巢狀字面值，
  所以我們直接採用 nodes and references 表示法（對 C++ 來說本來就更自然）。</p>
'''

LEGACY['real'] = r'''  <p>本章的樹結構在實際系統中很常見：</p>
  <ul style="margin-left:1.5rem;line-height:1.9;">
    <li><strong>檔案系統</strong>（樹）：每個目錄一個節點，檔案是葉子。</li>
    <li><strong>編譯器與直譯器</strong>（解析樹 / AST）：源碼解析成抽象語法樹，遞迴走訪做型別檢查、最佳化、產生機器碼。</li>
    <li><strong>資料庫索引</strong>（B-tree / B+tree）：BST 的多路推廣，每個節點容納上百個 keys，是磁碟導向的設計。</li>
    <li><strong>路由表 / IP lookup</strong>（Trie）：另一種樹型結構，依字元逐層走訪。</li>
    <li><strong>Heap 與優先佇列</strong>：Dijkstra 最短路徑、Huffman 編碼、$k$ 路合併、top-$k$ 問題都用到 priority queue。</li>
  </ul>
'''

LEGACY['heapclass'] = r'''  <p>把前面的函式放在一起看。整個類別只有一個成員 <code>vector&lt;int&gt; heap</code>：樹形是用索引「算」出來的
  （左子 2i+1、右子 2i+2、父 (i-1)/2），從頭到尾不需要指標。</p>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:.8rem;">
    <div class="info-card"><div class="ic-title">percUp ＋ insert：新元素往上浮 <span class="ic-badge">CODE</span></div>
      <div class="pseudo-code" style="font-size:.72rem;">
<span class="line"><span class="kw">void</span> <span class="fn">percUp</span>(<span class="kw">int</span> i) {</span>
<span class="line">    <span class="kw">while</span> (i &gt; <span class="num">0</span>) {</span>
<span class="line">        <span class="kw">int</span> parentIdx = (i - <span class="num">1</span>) / <span class="num">2</span>;</span>
<span class="line">        <span class="kw">if</span> (heap[i] &lt; heap[parentIdx])</span>
<span class="line">            <span class="fn">swap</span>(heap[i], heap[parentIdx]);</span>
<span class="line">        <span class="kw">else</span> <span class="kw">break</span>;   <span class="com">// 不再比父小就停</span></span>
<span class="line">        i = parentIdx;</span>
<span class="line">    }</span>
<span class="line">}</span>
<span class="line"><span class="kw">void</span> <span class="fn">insert</span>(<span class="kw">int</span> item) {</span>
<span class="line">    heap.<span class="fn">push_back</span>(item);      <span class="com">// 先掛最尾（保結構性質）</span></span>
<span class="line">    <span class="fn">percUp</span>(heap.<span class="fn">size</span>() - <span class="num">1</span>);  <span class="com">// 再浮上去（修順序性質）</span></span>
<span class="line">}</span></div></div>
    <div class="info-card"><div class="ic-title">getMinChild ＋ percDown：往下沉 <span class="ic-badge">CODE</span></div>
      <div class="pseudo-code" style="font-size:.72rem;">
<span class="line"><span class="kw">int</span> <span class="fn">getMinChild</span>(<span class="kw">int</span> i) {</span>
<span class="line">    <span class="kw">if</span> (<span class="num">2</span>*i + <span class="num">2</span> &gt; (<span class="kw">int</span>)heap.<span class="fn">size</span>() - <span class="num">1</span>)</span>
<span class="line">        <span class="kw">return</span> <span class="num">2</span>*i + <span class="num">1</span>;   <span class="com">// 只有左子</span></span>
<span class="line">    <span class="kw">if</span> (heap[<span class="num">2</span>*i+<span class="num">1</span>] &lt; heap[<span class="num">2</span>*i+<span class="num">2</span>])</span>
<span class="line">        <span class="kw">return</span> <span class="num">2</span>*i + <span class="num">1</span>;</span>
<span class="line">    <span class="kw">return</span> <span class="num">2</span>*i + <span class="num">2</span>;</span>
<span class="line">}</span>
<span class="line"><span class="kw">void</span> <span class="fn">percDown</span>(<span class="kw">int</span> i) {</span>
<span class="line">    <span class="kw">while</span> (<span class="num">2</span>*i + <span class="num">1</span> &lt; (<span class="kw">int</span>)heap.<span class="fn">size</span>()) {</span>
<span class="line">        <span class="kw">int</span> smChild = <span class="fn">getMinChild</span>(i);</span>
<span class="line">        <span class="kw">if</span> (heap[i] &gt; heap[smChild])</span>
<span class="line">            <span class="fn">swap</span>(heap[i], heap[smChild]);</span>
<span class="line">        <span class="kw">else</span> <span class="kw">break</span>;</span>
<span class="line">        i = smChild;   <span class="com">// 跟較小的子交換後繼續沉</span></span>
<span class="line">    }</span>
<span class="line">}</span></div></div>
    <div class="info-card"><div class="ic-title">delet ＋ heapify：取最小、批次建堆 <span class="ic-badge">CODE</span></div>
      <div class="pseudo-code" style="font-size:.72rem;">
<span class="line"><span class="kw">int</span> <span class="fn">delet</span>() {                <span class="com">// 取出最小值</span></span>
<span class="line">    <span class="kw">if</span> (heap.<span class="fn">empty</span>()) <span class="kw">throw</span> underflow_error(<span class="str">&quot;empty heap&quot;</span>);</span>
<span class="line">    <span class="fn">swap</span>(heap[<span class="num">0</span>], heap[heap.<span class="fn">size</span>() - <span class="num">1</span>]);</span>
<span class="line">    <span class="kw">int</span> result = heap.<span class="fn">back</span>();</span>
<span class="line">    heap.<span class="fn">pop_back</span>();</span>
<span class="line">    <span class="kw">if</span> (!heap.<span class="fn">empty</span>()) <span class="fn">percDown</span>(<span class="num">0</span>);</span>
<span class="line">    <span class="kw">return</span> result;</span>
<span class="line">}</span>
<span class="line"><span class="kw">void</span> <span class="fn">heapify</span>(vector&lt;<span class="kw">int</span>&gt; notAHeap) {</span>
<span class="line">    heap = notAHeap;</span>
<span class="line">    <span class="kw">int</span> i = heap.<span class="fn">size</span>() / <span class="num">2</span> - <span class="num">1</span>;  <span class="com">// 最後一個非葉</span></span>
<span class="line">    <span class="kw">while</span> (i &gt;= <span class="num">0</span>) {</span>
<span class="line">        <span class="fn">percDown</span>(i);</span>
<span class="line">        i = i - <span class="num">1</span>;   <span class="com">// 倒著做，正是 O(n) 的關鍵</span></span>
<span class="line">    }</span>
<span class="line">}</span></div></div>
  </div>
  <p style="font-size:.85rem;color:var(--muted);margin-top:.5rem;">不管資料以什麼順序進來，<code>heap[0]</code> 永遠是目前最小值，
  <code>delet()</code> 也總是取出最小者。<code>findMin()</code> 讀取最小值，<code>delMin()</code> 移除最小值，<code>size()</code> 回傳元素數，<code>buildHeap()</code> 從一批資料建堆。<code>delet()</code> 與 <code>heapify()</code> 分別是 <code>delMin()</code> 與 <code>buildHeap()</code> 的別名。</p>
'''
