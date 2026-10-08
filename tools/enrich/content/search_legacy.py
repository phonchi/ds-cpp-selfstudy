"""Hand-written section bodies of searching_sorting.html (widgets, explanations), moved here from the page.
search_depth.py splits them at fixed anchors and interleaves the lecture material. Edit here, then rerun
tools/enrich/enrich_search.py."""

LEGACY = {}

LEGACY['prologue'] = r'''  <p>本章探討兩件事：<strong>搜尋（searching）</strong> 從一堆資料中找出特定元素，<strong>排序（sorting）</strong> 把資料重新排列成有序狀態。我們會從最樸素的「逐一比對」開始，逐步揭開背後的演算法，並且<strong>用「比較次數」當作分析的單位</strong>。</p>
{{slot:find}}
  <div class="info-box">
    <span class="info-label">分析的兩個約定</span>
    <strong>1. 計算單位 = 比較次數。</strong>對搜尋而言，是「拿目標和某個元素比一下」算一次；對排序而言，是「比較兩個元素誰大誰小」算一次。<br>
    <strong>2. 等機率假設。</strong>搜尋成功時，假設目標出現在每個位置的機率都相同；這樣才能合理地討論「平均情況」。
  </div>

  <h3>顏色語義（整頁通用）</h3>
  <div class="legend">
    <span class="legend-item"><span class="lg-swatch" style="background:var(--bar-default)"></span>未處理</span>
    <span class="legend-item"><span class="lg-swatch" style="background:var(--bar-compare)"></span>正在比較</span>
    <span class="legend-item"><span class="lg-swatch" style="background:var(--bar-swap)"></span>正在交換</span>
    <span class="legend-item"><span class="lg-swatch" style="background:var(--bar-sorted)"></span>已排序</span>
    <span class="legend-item"><span class="lg-swatch" style="background:var(--bar-pivot)"></span>樞紐值 (pivot)</span>
    <span class="legend-item"><span class="lg-swatch" style="background:var(--bar-key)"></span>插入鍵值 (curVal)</span>
    <span class="legend-item"><span class="lg-swatch" style="background:var(--bar-found)"></span>找到目標</span>
  </div>

  <p>每一節都採用相同的版面：左邊是「視覺化畫布」與「控制列」，右邊是「即時統計」、「對應虛擬碼（pseudo-code）」與「複雜度分析」。請大膽地按 <span class="pill pill-green">▶ 開始</span> 看完整動畫，或按 <span class="pill pill-blue">→ 單步</span> 一格一格觀察。</p>

'''

LEGACY['seq-search'] = r'''  <p>把資料想像成一排櫃子，要找某個物件，最直覺的辦法就是<strong>從第 0 格開始、一格一格打開來看</strong>。這就是 <em>sequential search</em>，也叫 linear search。它<strong>不要求資料有序</strong>，是處理一般 list 時最基本的搜尋方法。</p>
{{slot:seq-program}}

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div class="algo-canvas" id="canvas-seq"><div class="bars-container"></div><div class="baseline"></div></div>
        <div class="status-banner"><span class="status-icon">›</span><span class="status-text" id="seqStatus">設定目標值後按「開始」</span></div>
        <div class="input-row">
          <label>陣列：</label>
          <input type="text" id="seqArrInput" value="54, 26, 93, 17, 77, 31, 44, 55, 20, 65">
          <label>目標：</label>
          <input type="number" id="seqTarget" value="44" style="width:70px;">
          <button class="btn btn-shuffle" id="seqApply">套用</button>
        </div>
        <div class="controls-bar">
          <button class="btn btn-play" id="seqPlay">▶ 開始</button>
          <button class="btn btn-step" id="seqStep">→ 單步</button>
          <button class="btn btn-reset" id="seqReset">↺ 重置</button>
          <div style="flex:1;min-width:160px;display:flex;align-items:center;gap:.5rem;">
            <span style="font-size:.78rem;color:var(--muted);">速度</span>
            <input type="range" id="seqSpeed" min="100" max="1500" step="50" value="600" style="flex:1;accent-color:var(--accent3);">
          </div>
        </div>
      </div>
    </div>

    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">即時統計 <span class="ic-badge">LIVE</span></div>
        <div class="stats-grid">
          <div class="stat-tile compare"><div class="stat-label">比較次數</div><div class="stat-value" id="seqCmp">0</div></div>
          <div class="stat-tile"><div class="stat-label">當前 pos</div><div class="stat-value" id="seqPos">—</div></div>
        </div>
        <div class="ic-row" style="margin-top:.6rem;"><span class="ic-label">結果</span><span class="ic-value highlight" id="seqResult">—</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">虛擬碼 <span class="ic-badge" style="background:var(--accent2)">CODE</span></div>
        <div class="pseudo-code" id="seqCode"><span class="line" data-l="1"><span class="kw">bool</span> <span class="fn">sequentialSearch</span>(<span class="kw">const</span> vector&lt;<span class="kw">int</span>&gt;&amp; aList, <span class="kw">int</span> item) {</span><span class="line" data-l="2">&nbsp;&nbsp;&nbsp;&nbsp;size_t pos = <span class="num">0</span>;</span><span class="line" data-l="3">&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">while</span> (pos &lt; aList.<span class="fn">size</span>()) {</span><span class="line" data-l="4">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">if</span> (aList[pos] == item) {</span><span class="line" data-l="5">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">return</span> <span class="num">true</span>;</span><span class="line" data-l="6">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;} ++pos;</span><span class="line" data-l="7">&nbsp;&nbsp;&nbsp;&nbsp;} <span class="kw">return</span> <span class="num">false</span>;</span><span class="line" data-l="8">}</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">複雜度</div>
        <div class="ic-row"><span class="ic-label">最佳 (item 在頭)</span><span class="ic-value">$O(1)$</span></div>
        <div class="ic-row"><span class="ic-label">最差 (沒找到)</span><span class="ic-value">$O(n)$</span></div>
        <div class="ic-row"><span class="ic-label">平均 (找得到)</span><span class="ic-value">$O(n/2)=O(n)$</span></div>
      </div>
    </div>
  </div>

  <div class="info-box warm">
    <span class="info-label">為何平均是 n/2？</span>
    在「等機率假設」下，目標出現在每個位置的機率相同。若 list 長度是 $n$，找到所需的比較次數為 $1, 2, \ldots, n$，平均為 $\dfrac{1+2+\cdots+n}{n} = \dfrac{n+1}{2}$；用大 O 仍是 $O(n)$。<strong>找不到的情形需要 $n$ 次比較</strong>：必須逐一檢查每一格。
  </div>

  <h3>有序版本：可以提前停止</h3>
  <p>如果 list 已經<strong>排序好</strong>了，就有捷徑：當看到的元素已經比目標大（升冪情況下），後面就不可能有了，可以立刻回傳 <code>false</code>。雖然找到的時候沒省到比較次數，但<strong>找不到時平均能少做一半</strong>：預期比較次數降到 $n/2$（仍是 $O(n)$，但常數變小）。</p>

{{slot:seq-ordered}}

  <div class="info-box green" style="margin-top:.8rem;">
    <span class="info-label">關鍵差異對比表</span>
    <div style="font-size:.86rem;line-height:1.65;margin-top:.4rem;">
      <div class="table-scroll" tabindex="0" aria-label="比較表，可左右捲動"><table style="width:100%;font-family:'JetBrains Mono',monospace;font-size:.78rem;">
        <thead><tr><th style="text-align:left;padding:.3rem;">情境</th><th style="padding:.3rem;">最佳</th><th style="padding:.3rem;">最差</th><th style="padding:.3rem;">平均</th></tr></thead>
        <tbody>
          <tr><td style="padding:.3rem;">item 在 list 中（兩種版本）</td><td style="text-align:center;">$1$</td><td style="text-align:center;">$n$</td><td style="text-align:center;">$n/2$</td></tr>
          <tr style="background:#fef0e7;"><td style="padding:.3rem;">item <strong>不在</strong>（普通版）</td><td style="text-align:center;">$n$</td><td style="text-align:center;">$n$</td><td style="text-align:center;">$n$</td></tr>
          <tr style="background:#eafaf1;"><td style="padding:.3rem;">item <strong>不在</strong>（有序版）</td><td style="text-align:center;">$1$</td><td style="text-align:center;">$n$</td><td style="text-align:center;">$n/2$</td></tr>
        </tbody>
      </table></div>
    </div>
    結論：兩種版本的<strong>大 $O$ 都是 $O(n)$</strong>，有序版只是<strong>常數變小</strong>。要真正快，得換演算法 → 二分搜尋。
  </div>
{{slot:seq-quiz}}
'''

LEGACY['bin-search'] = r'''  <p>當 list <strong>已排序</strong>，可以用更聰明的策略：直接看<strong>正中間</strong>那一個。比目標大就往左半找；比目標小就往右半找；剛好相等就找到了。每次比較<strong>排除掉一半</strong>，所以總比較次數最多 $\lceil \log_2 n \rceil + 1$。</p>
{{slot:bin-program}}

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div class="algo-canvas" id="canvas-bin" style="height:380px;"><div class="bars-container"></div><div class="baseline"></div></div>
        <div class="status-banner"><span class="status-icon">›</span><span class="status-text" id="binStatus">陣列已排序，按「開始」執行二分搜尋</span></div>
        <div class="input-row">
          <label>已排序陣列：</label>
          <input type="text" id="binArrInput" value="17, 20, 26, 31, 44, 54, 55, 65, 77, 93">
          <label>目標：</label>
          <input type="number" id="binTarget" value="44" style="width:70px;">
          <button class="btn btn-shuffle" id="binApply">套用</button>
        </div>
        <div class="controls-bar">
          <button class="btn btn-play" id="binPlay">▶ 開始</button>
          <button class="btn btn-step" id="binStep">→ 單步</button>
          <button class="btn btn-reset" id="binReset">↺ 重置</button>
          <div style="flex:1;min-width:160px;display:flex;align-items:center;gap:.5rem;">
            <span style="font-size:.78rem;color:var(--muted);">速度</span>
            <input type="range" id="binSpeed" min="200" max="1800" step="50" value="800" style="flex:1;accent-color:var(--accent3);">
          </div>
        </div>
      </div>
    </div>

    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">當前指標 <span class="ic-badge">LIVE</span></div>
        <div class="ic-row"><span class="ic-label">first</span><span class="ic-value" id="binLow" style="color:#2980b9;">0</span></div>
        <div class="ic-row"><span class="ic-label">last</span><span class="ic-value" id="binHigh" style="color:var(--accent);">9</span></div>
        <div class="ic-row"><span class="ic-label">midpoint = first + (last-first)/2</span><span class="ic-value" id="binMid" style="color:var(--accent3);">4</span></div>
        <div class="ic-row" style="margin-top:.4rem;border-top:1px solid var(--card-border);padding-top:.4rem;"><span class="ic-label">比較次數</span><span class="ic-value highlight" id="binCmp">0</span></div>
        <div class="ic-row"><span class="ic-label">結果</span><span class="ic-value highlight" id="binResult">—</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">虛擬碼 <span class="ic-badge" style="background:var(--accent2)">CODE</span></div>
        <div class="pseudo-code" id="binCode"><span class="line" data-l="1"><span class="kw">bool</span> <span class="fn">binarySearch</span>(<span class="kw">const</span> vector&lt;<span class="kw">int</span>&gt;&amp; aList, <span class="kw">int</span> item) {</span><span class="line" data-l="2">&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">int</span> first = <span class="num">0</span>;</span><span class="line" data-l="3">&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">int</span> last = <span class="kw">static_cast</span>&lt;<span class="kw">int</span>&gt;(aList.<span class="fn">size</span>()) - <span class="num">1</span>;</span><span class="line" data-l="4">&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">while</span> (first &lt;= last) {</span><span class="line" data-l="5">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">int</span> midpoint = first + (last - first) / <span class="num">2</span>;</span><span class="line" data-l="6">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">if</span> (aList[midpoint] == item)</span><span class="line" data-l="7">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">return</span> <span class="num">true</span>;</span><span class="line" data-l="8">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">if</span> (item &lt; aList[midpoint])</span><span class="line" data-l="9">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;last = midpoint - <span class="num">1</span>;</span><span class="line" data-l="10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">else</span></span><span class="line" data-l="11">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;first = midpoint + <span class="num">1</span>;</span><span class="line" data-l="12">&nbsp;&nbsp;&nbsp;&nbsp;} <span class="kw">return</span> <span class="num">false</span>;</span><span class="line" data-l="13">}</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">複雜度</div>
        <div class="ic-row"><span class="ic-label">最佳 (mid 命中)</span><span class="ic-value">$O(1)$</span></div>
        <div class="ic-row"><span class="ic-label">最差 / 平均</span><span class="ic-value">$O(\log n)$</span></div>
        <div class="ic-row"><span class="ic-label">前置條件</span><span class="ic-value">必須<strong>已排序</strong></span></div>
      </div>
    </div>
  </div>

{{slot:bin-analysis}}
  <div class="info-box green">
    <span class="info-label">為何是 log n？</span>
    每次比較讓搜尋範圍變成原本的一半。$n \to n/2 \to n/4 \to \cdots \to 1$，要做 $\log_2 n$ 次切割。<br>
    <strong>數值感受：</strong> $n=1{,}000{,}000$ 的 list，循序搜尋最多 $10^6$ 次比較，二分搜尋只要 $\lceil \log_2 10^6 \rceil = 20$ 次！
  </div>

  <div class="info-box warm">
    <span class="info-label">陷阱</span>
    二分搜尋的<strong>排序成本</strong>不能忽略。若 list 只搜尋一次，先 $O(n\log n)$ 排序再 $O(\log n)$ 搜尋，反而慢於直接 $O(n)$ 循序搜尋。<strong>多次搜尋同一份排序好的資料</strong>時，二分搜尋才划算。
  </div>

  <div class="info-box">
    <span class="info-label">小細節</span>
    若每次遞迴都建構新的子 vector，單一路徑會複製 $n/2+n/4+\cdots=O(n)$ 個元素，因此是 $O(n)$ 時間與 $O(n)$ 峰值元素儲存，而非嚴格的 $O(\log n)$。改傳同一個 <code>const vector&lt;int&gt;&amp;</code> 與 <code>first</code>、<code>last</code> 邊界後，才保留 $O(\log n)$ 比較與 $O(\log n)$ call stack。
  </div>
{{slot:bin-end}}
'''

LEGACY['hashing'] = r'''  <p>有沒有可能讓搜尋變成 $O(1)$？只要我們<strong>事先決定每個值該存哪裡</strong>就行。<em>hash function</em> $h(\text{item})$ 把每個值對應到一個槽（slot）的索引。最簡單的 hash 函數是 <strong>remainder method</strong>：$h(\text{item}) = \text{item} \bmod m$，其中 $m$ 是表的大小。</p>
{{slot:hash-table}}
  <div class="info-box">
    <span class="info-label">範例：m = 11，存入 [54, 26, 93, 17, 77, 31]</span>
    <div style="font-family:'JetBrains Mono',monospace;font-size:.88rem;line-height:1.8;margin-top:.4rem;">
      $54 \bmod 11 = 10$　$26 \bmod 11 = 4$　$93 \bmod 11 = 5$<br>
      $17 \bmod 11 = 6$　$77 \bmod 11 = 0$　$31 \bmod 11 = 9$
    </div>
    全部都落在不同槽，<em>load factor</em> $\lambda = 6/11 \approx 0.55$。
  </div>
{{slot:hash-load}}

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <h3 style="margin-top:0;">雜湊表 (m = 11)</h3>
        <div class="hash-table-wrap" id="hashTable"></div>
        <div class="status-banner"><span class="status-icon">›</span><span class="status-text" id="hashStatus">輸入要插入或搜尋的值</span></div>
        <div class="input-row">
          <label>值：</label>
          <input type="number" id="hashVal" value="44" style="width:80px;">
          <button class="btn btn-step" id="hashInsert">插入 (insert)</button>
          <button class="btn btn-play" id="hashSearch">搜尋 (search)</button>
        </div>
        <div class="input-row">
          <label>策略：</label>
          <button class="preset-btn active" data-strategy="linear">線性探查</button>
          <button class="preset-btn" data-strategy="chain">鏈結法</button>
          <button class="btn btn-reset" id="hashClear" style="margin-left:auto;">↺ 清空表</button>
        </div>
        <div class="input-row">
          <label>批次：</label>
          <input type="text" id="hashBatch" value="54, 26, 93, 17, 77, 31" style="flex:1;">
          <button class="btn btn-shuffle" id="hashBatchInsert">全部插入</button>
        </div>
      </div>
    </div>

    <div class="side-panel">
      <div class="eq-card">
        <div class="eq-label">餘數雜湊函數</div>
        <div class="eq-formula">$h(item) = item \bmod m$</div>
        <div class="eq-sub">$m = 11$（表大小，建議用質數）</div>
      </div>
      <div class="info-card">
        <div class="ic-title">即時統計 <span class="ic-badge">LIVE</span></div>
        <div class="ic-row"><span class="ic-label">已用槽數</span><span class="ic-value" id="hashUsed">0 / 11</span></div>
        <div class="ic-row"><span class="ic-label">負載因子 λ</span><span class="ic-value highlight" id="hashLoad">0.00</span></div>
        <div class="ic-row"><span class="ic-label">本次比較次數</span><span class="ic-value" id="hashOps">0</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">何謂碰撞 collision</div>
        <div style="font-size:.84rem;line-height:1.65;">
          兩個不同的 item 雜湊到<strong>同一個 slot</strong>就是碰撞。處理方法：<br>
          <span class="pill pill-blue">線性探查</span> 往後找第一個空的<br>
          <span class="pill pill-purple">鏈結法</span> 在該 slot 接一條 list
        </div>
      </div>
      <div class="info-card">
        <div class="ic-title">複雜度</div>
        <div class="ic-row"><span class="ic-label">理想 (無碰撞)</span><span class="ic-value">$O(1)$</span></div>
        <div class="ic-row"><span class="ic-label">線性探查 search</span><span class="ic-value">$\frac{1}{2}\!\left(1+\frac{1}{1-\lambda}\right)$</span></div>
        <div class="ic-row"><span class="ic-label">鏈結法 search</span><span class="ic-value">$1 + \lambda/2$</span></div>
      </div>
    </div>
  </div>

  <h3 style="margin-top:1.5rem;">其他常見的雜湊函數</h3>
  <div class="viz-layout" style="margin-top:.8rem;">
    <div>
      <div class="info-card">
        <div class="ic-title">折疊法 folding method</div>
        <div style="font-size:.84rem;line-height:1.65;">
          把 item 切成<strong>等長的片段</strong>，加總後再取餘數。例如電話號碼 <code>436-555-4601</code> 切成 <code>43, 65, 55, 46, 01</code>，加總得 $210$；除以 11 得 $h = 210 \bmod 11 = 1$。<br>
          進階：<strong>反轉版本</strong>把每隔一片反過來再相加，例如 <code>34 + 56 + 55 + 64 + 10 = 219 → 219 mod 11 = 10</code>。
        </div>
      </div>
      <div class="info-card">
        <div class="ic-title">平方取中法 mid-square</div>
        <div style="font-size:.84rem;line-height:1.65;">
          先把 item 平方，取中間幾位數，再取餘數。<br>
          例：item = 44 → $44^2 = 1936$ → 取中間兩位 <code>93</code> → $93 \bmod 11 = 5$。<br>
          <span class="pill pill-blue">範例對照表</span> &nbsp; <code>54→3, 26→1, 93→9, 17→6, 77→4, 31→8</code>
          <p style="font-size:.78rem;color:var(--muted);margin-top:.4rem;font-style:italic;">
            ⓘ 對 17, 31 這類平方後位數不夠的情況，先補 0 至偶數位再取「正中間兩位」做 mod 11 是統一的做法。例如 $17^2 = 289$ → 補成 <code>0289</code> → 取 <code>28</code> → $28 \bmod 11 = 6$；$31^2 = 961$ → 補成 <code>0961</code> → 取 <code>96</code> → $96 \bmod 11 = 8$。
          </p>
        </div>
      </div>
    </div>

    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">字串雜湊 string hashing</div>
        <div style="font-size:.84rem;line-height:1.65;">
          字串可以用每個字元的 <strong>ordinal value</strong>（ASCII 碼）相加再取餘數，程式見下方的 <code>hashStr</code>。<br>
          <strong>陷阱：</strong>"cat"、"act"、"tac" 全是同樣 ord 總和，會撞在一起（anagrams 衝突）。改良：<strong>用位置當權重</strong>，例如 $\sum i \cdot \text{ord}(c_i) \bmod m$。
        </div>
      </div>
      <div class="info-card">
        <div class="ic-title">設計目標</div>
        <div style="font-size:.84rem;line-height:1.65;">
          理想的 hash 函數應該：<br>
          <span class="pill pill-blue">易於計算</span> 不能比直接搜尋還慢<br>
          <span class="pill pill-purple">分布均勻</span> 減少碰撞機率<br>
          <span class="pill pill-orange">Perfect hash</span> 對特定資料集無碰撞，但<strong>不存在通用方法</strong>
        </div>
      </div>
    </div>
  </div>

{{slot:hash-functions}}
  <h3 style="margin-top:1.5rem;">碰撞解決：除了線性探查還有什麼？</h3>
{{slot:hash-probing}}
  <div class="info-box">
    <span class="info-label">rehash 通式：$\text{rehash}(\text{pos}) = (\text{pos} + \text{skip}) \bmod m$</span>
    <strong>線性探查 (linear probing)</strong>：skip = 1，每次往後找下一格。簡單但容易產生<em>聚集 (clustering)</em>：許多碰撞在同一段連續 slot 累積，後續插入會被牽連。<br><br>
    <strong>+3 探查 (plus-3)</strong>：skip = 3，跳格搜尋。要求 skip 與 $m$ 互質，否則會循環走不完整個表（這也是為何 $m$ 常選<strong>質數</strong>）。<br><br>
    <strong>平方探查 (quadratic probing)</strong>：skip 不是定值，而是 $1, 4, 9, 16, \ldots$（連續完全平方數）。即 $h, h+1, h+4, h+9, \ldots$。能有效打散聚集。<br><br>
    <strong>鏈結法 (chaining)</strong>：每個 slot 存一條 list（或其他 collection），所有 hash 到該 slot 的 item 都掛在同一條鏈上。$\lambda$ 可以超過 1。
  </div>
{{slot:hash-exercise}}

  <h3 style="margin-top:1.5rem;">應用：Map ADT (字典/HashTable)</h3>
  <div class="info-box warm">
    <span class="info-label">用 hash 表實作 key-value 字典</span>
    Map ADT 是介面概念；<code>std::unordered_map</code> 是標準函式庫的具體 hash-table 容器。本頁的固定容量 <code>HashTable</code> 只實作 <code>put/get</code> 與顯示輔助，下面同時列出完整 ADT 常見操作作為對照：
    <div style="font-size:.84rem;line-height:1.7;margin:.5rem 0;">
      <div class="table-scroll" tabindex="0" aria-label="比較表，可左右捲動"><table style="width:100%;font-family:'JetBrains Mono',monospace;font-size:.78rem;border-collapse:collapse;">
        <thead><tr style="background:var(--paper);border-bottom:2px solid var(--card-border);"><th style="text-align:left;padding:.35rem;">操作</th><th style="text-align:left;padding:.35rem;">語意</th></tr></thead>
        <tbody>
          <tr><td style="padding:.3rem;color:var(--accent2);font-weight:600;">HashTable(size)</td><td>建立固定容量的教學用 hash table</td></tr>
          <tr style="background:#fff;"><td style="padding:.3rem;color:var(--accent2);font-weight:600;">put(key, val)</td><td>新增 key–value 對；若 key 已存在則覆寫舊值</td></tr>
          <tr><td style="padding:.3rem;color:var(--accent2);font-weight:600;">get(key)</td><td>教學版傳回對應 value；找不到回空字串，因此無法區分「不存在」與「值本來就是空字串」</td></tr>
          <tr style="background:#fff;"><td style="padding:.3rem;color:var(--accent2);font-weight:600;">erase(key)</td><td>刪除指定的 key–value 對</td></tr>
          <tr><td style="padding:.3rem;color:var(--accent2);font-weight:600;">size()</td><td>回傳目前儲存的 key–value 對總數</td></tr>
          <tr style="background:#fff;"><td style="padding:.3rem;color:var(--accent2);font-weight:600;">contains(key)</td><td>判斷 key 是否在表中，回傳 <code>true</code>/<code>false</code></td></tr>
        </tbody>
      </table></div>
    </div>
    <div class="pseudo-code" style="margin-top:.4rem;">
<span class="line"><span class="kw">class</span> <span class="fn">HashTable</span> {</span>
<span class="line">  <span class="kw">public</span>:</span>
<span class="line">    <span class="kw">void</span> <span class="fn">put</span>(<span class="kw">int</span> key, string value);</span>
<span class="line">    string <span class="fn">get</span>(<span class="kw">int</span> key);</span>
<span class="line">  <span class="kw">private</span>:</span>
<span class="line">    vector&lt;<span class="kw">int</span>&gt; slots; <span class="com">// -1 保留為空槽</span></span>
<span class="line">    vector&lt;string&gt; data;</span>
<span class="line">};</span>
<span class="line"><span class="com">// put 探查一圈仍無空位時 throw overflow_error</span></span></div>
    <strong>關鍵：</strong>用兩個平行 vector (<code>slots</code>、<code>data</code>) 分別存 key 和 value，索引位置必須對齊。<code>get</code> 時要走和 <code>put</code> 一樣的 rehash 路徑，且要偵測「<strong>繞回起點</strong>」(<code>position == startSlot</code>) 以結束搜尋（代表整個探查鏈都沒有該 key）。
  </div>
{{slot:hash-map}}

  <h3 style="margin-top:1.5rem;">分析：載入因子 $\lambda$ 與比較次數</h3>
  <div class="info-box green">
    <span class="info-label">當 $\lambda$ 變大，效能如何下降？</span>
    <strong>線性探查 + 開放定址 (open addressing)：</strong><br>
    　・成功搜尋平均比較次數 $\approx \dfrac{1}{2}\!\left(1 + \dfrac{1}{1-\lambda}\right)$<br>
    　・失敗搜尋平均比較次數 $\approx \dfrac{1}{2}\!\left(1 + \left(\dfrac{1}{1-\lambda}\right)^2\right)$<br><br>
    <strong>鏈結法 (chaining)：</strong><br>
    　・成功搜尋平均比較次數 $\approx 1 + \dfrac{\lambda}{2}$<br>
    　・失敗搜尋平均比較次數 $\approx \lambda$<br><br>
    當 $\lambda \to 1$ 時，線性探查的失敗搜尋會爆炸性增加；鏈結法則是線性增加，較為穩定。
  </div>

  <div class="info-box warm">
    <span class="info-label">小實驗</span>
    試試<strong>用「線性探查」</strong>把 <code>54, 26, 93, 17, 77, 31, 44, 55, 20</code> 全部插入：你會發現 44、55、20 都會發生碰撞，被推到別的槽去。再切換到<strong>「鏈結法」</strong>清空、重做一次，會看到撞到的 item 直接掛在槽下面，不會佔走別人的位置。
  </div>

'''

LEGACY['bubble'] = r'''  <p><strong>Bubble sort</strong> 的想法很單純：每一輪從頭走到尾，遇到「左邊比右邊大」就交換。經過一輪之後，<strong>最大的元素一定會被送到最右邊</strong>，就像氣泡浮到水面一樣。下一輪只要處理剩下的部分，依此類推。</p>
{{slot:bubble-intro}}

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div class="algo-canvas" id="canvas-bubble"><div class="bars-container"></div><div class="baseline"></div></div>
        <div class="status-banner"><span class="status-icon">›</span><span class="status-text" id="bubbleStatus">按「開始」執行氣泡排序</span></div>
        <div class="input-row">
          <label>陣列：</label>
          <input type="text" id="bubbleArrInput" value="54, 26, 93, 17, 77, 31, 44, 55, 20">
          <button class="btn btn-shuffle" id="bubbleShuffle">隨機洗牌</button>
          <button class="btn btn-shuffle" id="bubbleApply" style="background:var(--accent2);">套用</button>
        </div>
        <div class="controls-bar">
          <button class="btn btn-play" id="bubblePlay">▶ 開始</button>
          <button class="btn btn-step" id="bubbleStep">→ 單步</button>
          <button class="btn btn-reset" id="bubbleReset">↺ 重置</button>
          <div style="flex:1;min-width:160px;display:flex;align-items:center;gap:.5rem;">
            <span style="font-size:.78rem;color:var(--muted);">速度</span>
            <input type="range" id="bubbleSpeed" min="50" max="1200" step="50" value="500" style="flex:1;accent-color:var(--accent3);">
          </div>
        </div>
      </div>
    </div>

    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">即時統計 <span class="ic-badge">LIVE</span></div>
        <div class="stats-grid">
          <div class="stat-tile compare"><div class="stat-label">比較</div><div class="stat-value" id="bubbleCmp">0</div></div>
          <div class="stat-tile swap"><div class="stat-label">交換</div><div class="stat-value" id="bubbleSwp">0</div></div>
        </div>
        <div class="ic-row" style="margin-top:.6rem;"><span class="ic-label">當前 pass</span><span class="ic-value" id="bubblePass">0</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">虛擬碼 <span class="ic-badge" style="background:var(--accent2)">CODE</span></div>
        <div class="pseudo-code" id="bubbleCode"><span class="line" data-l="1"><span class="kw">void</span> <span class="fn">bubbleSort</span>(vector&lt;<span class="kw">int</span>&gt;&amp; a) {</span><span class="line" data-l="2">&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">for</span> (<span class="kw">int</span> i = a.<span class="fn">size</span>() - <span class="num">1</span>; i &gt; <span class="num">0</span>; --i) {</span><span class="line" data-l="3">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">for</span> (<span class="kw">int</span> j = <span class="num">0</span>; j &lt; i; ++j) {</span><span class="line" data-l="4">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">if</span> (a[j] &gt; a[j + <span class="num">1</span>])</span><span class="line" data-l="5">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="fn">swap</span>(a[j], a[j + <span class="num">1</span>]);</span><span class="line" data-l="6">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}</span><span class="line" data-l="7">&nbsp;&nbsp;&nbsp;&nbsp;}</span><span class="line" data-l="8">}</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">複雜度</div>
        <div class="ic-row"><span class="ic-label">比較次數</span><span class="ic-value">$\binom{n}{2} = \frac{n(n-1)}{2}$</span></div>
        <div class="ic-row"><span class="ic-label">時間 (各情況)</span><span class="ic-value">$O(n^2)$</span></div>
        <div class="ic-row"><span class="ic-label">空間</span><span class="ic-value">$O(1)$</span></div>
      </div>
    </div>
  </div>

  <div class="info-box green">
    <span class="info-label">短路最佳化 short bubble</span>
    若某一輪<strong>都沒發生交換</strong>，代表已經完全排序了，可以提早結束！這時最佳情況變成 $O(n)$（已排序時只需一輪）。但平均與最差仍是 $O(n^2)$。
  </div>
{{slot:bubble-end}}
'''

LEGACY['selection'] = r'''  <p><strong>Selection sort</strong> 跟氣泡排序的<strong>比較次數一樣多</strong>，但聰明在「<strong>每一輪只交換一次</strong>」：先掃一遍找出未排序區裡<strong>最大</strong>的元素，再把它和未排序區的<strong>最後一格</strong>直接交換，就完成一輪。氣泡排序每比一次就可能交換，selection sort 把交換成本壓到最低。<small>（與 cppds 與 HW4 一致：找最大值放到未排序區尾端。）</small></p>
{{slot:selection-intro}}

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div class="algo-canvas" id="canvas-sel"><div class="bars-container"></div><div class="baseline"></div></div>
        <div class="status-banner"><span class="status-icon">›</span><span class="status-text" id="selStatus">按「開始」執行選擇排序</span></div>
        <div class="input-row">
          <label>陣列：</label>
          <input type="text" id="selArrInput" value="54, 26, 93, 17, 77, 31, 44, 55, 20">
          <button class="btn btn-shuffle" id="selShuffle">隨機洗牌</button>
          <button class="btn btn-shuffle" id="selApply" style="background:var(--accent2);">套用</button>
        </div>
        <div class="controls-bar">
          <button class="btn btn-play" id="selPlay">▶ 開始</button>
          <button class="btn btn-step" id="selStep">→ 單步</button>
          <button class="btn btn-reset" id="selReset">↺ 重置</button>
          <div style="flex:1;min-width:160px;display:flex;align-items:center;gap:.5rem;">
            <span style="font-size:.78rem;color:var(--muted);">速度</span>
            <input type="range" id="selSpeed" min="50" max="1200" step="50" value="500" style="flex:1;accent-color:var(--accent3);">
          </div>
        </div>
      </div>
    </div>

    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">即時統計 <span class="ic-badge">LIVE</span></div>
        <div class="stats-grid">
          <div class="stat-tile compare"><div class="stat-label">比較</div><div class="stat-value" id="selCmp">0</div></div>
          <div class="stat-tile swap"><div class="stat-label">交換</div><div class="stat-value" id="selSwp">0</div></div>
        </div>
        <div class="ic-row" style="margin-top:.6rem;"><span class="ic-label">本輪當前最大 idx</span><span class="ic-value highlight" id="selMinIdx">—</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">虛擬碼</div>
        <div class="pseudo-code" id="selCode"><span class="line" data-l="1"><span class="kw">void</span> <span class="fn">selectionSort</span>(vector&lt;<span class="kw">int</span>&gt;&amp; a) {</span><span class="line" data-l="2">&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">for</span> (<span class="kw">int</span> fill = a.<span class="fn">size</span>() - <span class="num">1</span>; fill &gt; <span class="num">0</span>; --fill) {</span><span class="line" data-l="3">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">int</span> maxPos = <span class="num">0</span>;</span><span class="line" data-l="4">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">for</span> (<span class="kw">int</span> j = <span class="num">1</span>; j &lt;= fill; ++j) {</span><span class="line" data-l="5">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">if</span> (a[j] &gt; a[maxPos])</span><span class="line" data-l="6">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;maxPos = j;</span><span class="line" data-l="7">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}</span><span class="line" data-l="8">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="fn">swap</span>(a[maxPos], a[fill]);</span><span class="line" data-l="9">&nbsp;&nbsp;&nbsp;&nbsp;}</span><span class="line" data-l="10">}</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">複雜度</div>
        <div class="ic-row"><span class="ic-label">比較次數</span><span class="ic-value">$\frac{n(n-1)}{2}$</span></div>
        <div class="ic-row"><span class="ic-label">交換次數</span><span class="ic-value class="best">最多 $n-1$</span></div>
        <div class="ic-row"><span class="ic-label">時間</span><span class="ic-value">$O(n^2)$</span></div>
      </div>
    </div>
  </div>

  <div class="info-box">
    <span class="info-label">vs. 氣泡</span>
    <strong>比較次數相同</strong>都是 $O(n^2)$，但 selection sort <strong>每輪最多交換一次</strong>，氣泡排序每輪可能交換很多次。當「交換成本」很高（例如要移動的物件很大）時，selection sort 表現會比 bubble sort 好。
  </div>
{{slot:selection-end}}
'''

LEGACY['insertion'] = r'''  <p><strong>Insertion sort</strong> 把陣列分成「已排序」（左半）和「未排序」（右半）兩區。每一輪取出未排序的第一張當 <em>curVal</em>（current value，當前要插入的值），往左在已排序區裡找出該插入的位置：遇到比它大的，就把它<strong>右移一格</strong>讓出空間。注意：這裡做的是<strong>位移（shift）而不是交換</strong>，所以可能比氣泡排序快一點。</p>
{{slot:insertion-intro}}

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div class="algo-canvas" id="canvas-ins"><div class="bars-container"></div><div class="baseline"></div></div>
        <div class="status-banner"><span class="status-icon">›</span><span class="status-text" id="insStatus">按「開始」執行插入排序</span></div>
        <div class="input-row">
          <label>陣列：</label>
          <input type="text" id="insArrInput" value="54, 26, 93, 17, 77, 31, 44, 55, 20">
          <button class="btn btn-shuffle" id="insShuffle">隨機洗牌</button>
          <button class="btn btn-shuffle" id="insApply" style="background:var(--accent2);">套用</button>
        </div>
        <div class="controls-bar">
          <button class="btn btn-play" id="insPlay">▶ 開始</button>
          <button class="btn btn-step" id="insStep">→ 單步</button>
          <button class="btn btn-reset" id="insReset">↺ 重置</button>
          <div style="flex:1;min-width:160px;display:flex;align-items:center;gap:.5rem;">
            <span style="font-size:.78rem;color:var(--muted);">速度</span>
            <input type="range" id="insSpeed" min="50" max="1200" step="50" value="500" style="flex:1;accent-color:var(--accent3);">
          </div>
        </div>
      </div>
    </div>

    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">即時統計 <span class="ic-badge">LIVE</span></div>
        <div class="stats-grid">
          <div class="stat-tile compare"><div class="stat-label">比較</div><div class="stat-value" id="insCmp">0</div></div>
          <div class="stat-tile" style="background:#fef0e7;"><div class="stat-label">位移 shift</div><div class="stat-value" id="insShift" style="color:#d68910;">0</div></div>
        </div>
        <div class="ic-row" style="margin-top:.6rem;"><span class="ic-label">當前 curVal</span><span class="ic-value highlight" id="insKey">—</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">虛擬碼</div>
        <div class="pseudo-code" id="insCode"><span class="line" data-l="1"><span class="kw">void</span> <span class="fn">insertionSort</span>(vector&lt;<span class="kw">int</span>&gt;&amp; a) {</span><span class="line" data-l="2">&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">for</span> (size_t i = <span class="num">1</span>; i &lt; a.<span class="fn">size</span>(); ++i) {</span><span class="line" data-l="3">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">int</span> curVal = a[i];</span><span class="line" data-l="4">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;size_t curPos = i;</span><span class="line" data-l="5">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">while</span> (curPos &gt; <span class="num">0</span> &amp;&amp; a[curPos - <span class="num">1</span>] &gt; curVal) {</span><span class="line" data-l="6">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a[curPos] = a[curPos - <span class="num">1</span>];</span><span class="line" data-l="7">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--curPos;</span><span class="line" data-l="8">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;} a[curPos] = curVal;</span><span class="line" data-l="9">&nbsp;&nbsp;&nbsp;&nbsp;}</span><span class="line" data-l="10">}</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">複雜度</div>
        <div class="ic-row"><span class="ic-label">最佳 (已排序)</span><span class="ic-value best">$O(n)$</span></div>
        <div class="ic-row"><span class="ic-label">最差 / 平均</span><span class="ic-value">$O(n^2)$</span></div>
      </div>
    </div>
  </div>

  <div class="info-box green">
    <span class="info-label">為什麼適合「幾乎排序好」的資料？</span>
    insertion sort 處理已排序資料時非常快：每個 key 只需要一次比較就能確認位置，時間複雜度降到 $O(n)$。如果你正在「<strong>插入新資料到已排序的 list</strong>」這個情境，insertion sort 是最自然的選擇。
  </div>
{{slot:insertion-end}}
'''

LEGACY['shell'] = r'''  <p><strong>Shell sort</strong> 是 1959 年 Donald Shell 提出的方法。觀察到 insertion sort 對「幾乎排序好」的資料很快，但對亂序資料慢。Shell sort 的策略：先用一個<strong>較大的 gap</strong> 把陣列拆成數個「子陣列」（每個子陣列的元素彼此相距 gap），對每個子陣列各自做插入排序；接著縮小 gap 再做一次；最後 gap = 1（變成普通的 insertion sort），但<strong>此時資料已經幾乎排序好</strong>。</p>
{{slot:shell-intro}}

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div class="algo-canvas" id="canvas-shell" style="height:380px;"><div class="bars-container"></div><div class="baseline"></div></div>
        <div class="status-banner"><span class="status-icon">›</span><span class="status-text" id="shellStatus">按「開始」執行希爾排序</span></div>
        <div class="input-row">
          <label>陣列：</label>
          <input type="text" id="shellArrInput" value="54, 26, 93, 17, 77, 31, 44, 55, 20">
          <button class="btn btn-shuffle" id="shellShuffle">隨機洗牌</button>
          <button class="btn btn-shuffle" id="shellApply" style="background:var(--accent2);">套用</button>
        </div>
        <div class="input-row">
          <label>gap 序列：</label>
          <button class="preset-btn active" data-gap="half">n/2 折半 (Shell 原版)</button>
          <button class="preset-btn" data-gap="2k-1">2^k − 1 = 1,3,7,15,... (Hibbard)</button>
        </div>
        <div class="controls-bar">
          <button class="btn btn-play" id="shellPlay">▶ 開始</button>
          <button class="btn btn-step" id="shellStep">→ 單步</button>
          <button class="btn btn-reset" id="shellReset">↺ 重置</button>
          <div style="flex:1;min-width:160px;display:flex;align-items:center;gap:.5rem;">
            <span style="font-size:.78rem;color:var(--muted);">速度</span>
            <input type="range" id="shellSpeed" min="50" max="1200" step="50" value="500" style="flex:1;accent-color:var(--accent3);">
          </div>
        </div>
      </div>
    </div>

    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">即時統計 <span class="ic-badge">LIVE</span></div>
        <div class="ic-row"><span class="ic-label">當前 gap</span><span class="ic-value highlight" id="shellGap" style="font-size:1.2rem;">—</span></div>
        <div class="stats-grid" style="margin-top:.4rem;">
          <div class="stat-tile compare"><div class="stat-label">比較</div><div class="stat-value" id="shellCmp">0</div></div>
          <div class="stat-tile swap"><div class="stat-label">交換</div><div class="stat-value" id="shellSwp">0</div></div>
        </div>
      </div>
      <div class="info-card">
        <div class="ic-title">虛擬碼 (對齊講義 §7.6)</div>
        <div class="pseudo-code" id="shellCode"><span class="line"><span class="kw">void</span> <span class="fn">gapInsertionSort</span>(vector&lt;<span class="kw">int</span>&gt;&amp;, <span class="kw">int</span>, <span class="kw">int</span>);</span><span class="line" data-l="1"><span class="kw">void</span> <span class="fn">shellSort</span>(vector&lt;<span class="kw">int</span>&gt;&amp; a) {</span><span class="line" data-l="2">&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">int</span> gap = a.<span class="fn">size</span>() / <span class="num">2</span>;</span><span class="line" data-l="3">&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">while</span> (gap &gt; <span class="num">0</span>) {</span><span class="line" data-l="4">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">for</span> (<span class="kw">int</span> start = <span class="num">0</span>; start &lt; gap; ++start)</span><span class="line" data-l="5">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="fn">gapInsertionSort</span>(a, start, gap);</span><span class="line" data-l="6">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;gap /= <span class="num">2</span>;</span><span class="line" data-l="7">&nbsp;&nbsp;&nbsp;&nbsp;}</span><span class="line" data-l="8">}</span><span class="line"><span class="kw">void</span> <span class="fn">gapInsertionSort</span>(vector&lt;<span class="kw">int</span>&gt;&amp; a, <span class="kw">int</span> start, <span class="kw">int</span> gap) {</span><span class="line" data-l="9">&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">for</span> (<span class="kw">int</span> i = start + gap; i &lt; a.<span class="fn">size</span>(); i += gap) {</span><span class="line" data-l="10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">int</span> curVal = a[i];</span><span class="line" data-l="11">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">int</span> curPos = i;</span><span class="line" data-l="12">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">while</span> (curPos &gt;= gap &amp;&amp; a[curPos-gap] &gt; curVal) {</span><span class="line" data-l="13">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a[curPos] = a[curPos-gap];</span><span class="line" data-l="14">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;curPos -= gap;</span><span class="line" data-l="15">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;} a[curPos] = curVal;</span><span class="line" data-l="16">&nbsp;&nbsp;&nbsp;&nbsp;}</span><span class="line">}</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">複雜度</div>
        <div class="ic-row"><span class="ic-label">時間 (依 gap 序列)</span><span class="ic-value">$O(n^{3/2}) \sim O(n^2)$</span></div>
        <div class="ic-row"><span class="ic-label">Hibbard 序列 $2^k-1$</span><span class="ic-value best">$O(n^{3/2})$</span></div>
        <div class="ic-row"><span class="ic-label">空間</span><span class="ic-value">$O(1)$</span></div>
      </div>
    </div>
  </div>

  <div class="info-box">
    <span class="info-label">關鍵直覺</span>
    當 gap 大時：每個子陣列很短，<strong>大跨度的調整很快</strong>，亂度迅速降低。<br>
    當 gap 小時：陣列已接近排好，<strong>小範圍的微調很便宜</strong>。<br>
    Shell sort 不像 merge / quick sort 那麼快，但<strong>程式碼短、不需要遞迴、空間 $O(1)$</strong>，是嵌入式系統與小型應用常見的選擇。
  </div>
{{slot:shell-end}}
'''

LEGACY['merge'] = r'''  <p><strong>Merge sort</strong> 是一個遞迴演算法，分成兩個動作：<br>
  <strong>(1) Divide 切：</strong> 把 list 從中間切成左、右兩半，各自呼叫 merge sort。<br>
  <strong>(2) Conquer + Merge 合：</strong> 兩半都排序好之後，<em>合併</em>成一個有序的大 list：用兩個指標分別走過左、右，每次把較小的那個寫回原本的 vector。<br>
  Base case：list 長度 ≤ 1 時自然有序，直接回傳。</p>
{{slot:merge-intro}}

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div class="algo-canvas" id="canvas-merge" style="height:380px;"><div class="bars-container"></div><div class="baseline"></div></div>
        <div class="status-banner"><span class="status-icon">›</span><span class="status-text" id="mergeStatus">按「開始」執行合併排序</span></div>
        <div class="input-row">
          <label>陣列：</label>
          <input type="text" id="mergeArrInput" value="54, 26, 93, 17, 77, 31, 44, 55">
          <button class="btn btn-shuffle" id="mergeShuffle">隨機洗牌</button>
          <button class="btn btn-shuffle" id="mergeApply" style="background:var(--accent2);">套用</button>
        </div>
        <div class="controls-bar">
          <button class="btn btn-play" id="mergePlay">▶ 開始</button>
          <button class="btn btn-step" id="mergeStep">→ 單步</button>
          <button class="btn btn-reset" id="mergeReset">↺ 重置</button>
          <div style="flex:1;min-width:160px;display:flex;align-items:center;gap:.5rem;">
            <span style="font-size:.78rem;color:var(--muted);">速度</span>
            <input type="range" id="mergeSpeed" min="100" max="1500" step="50" value="500" style="flex:1;accent-color:var(--accent3);">
          </div>
        </div>
      </div>

      <h3>遞迴呼叫樹 (recursion tree)</h3>
      <div class="tree-canvas" id="mergeTree"></div>
    </div>

    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">即時統計 <span class="ic-badge">LIVE</span></div>
        <div class="stats-grid">
          <div class="stat-tile compare"><div class="stat-label">比較</div><div class="stat-value" id="mergeCmp">0</div></div>
          <div class="stat-tile" style="background:#eef5fc;"><div class="stat-label">寫入</div><div class="stat-value" id="mergeWrite" style="color:#2980b9;">0</div></div>
        </div>
        <div class="ic-row" style="margin-top:.6rem;"><span class="ic-label">當前階段</span><span class="ic-value" id="mergePhase">—</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">虛擬碼</div>
        <div class="pseudo-code" id="mergeCode"><span class="line" data-l="1"><span class="kw">void</span> <span class="fn">mergeSort</span>(vector&lt;<span class="kw">int</span>&gt;&amp; a) {</span><span class="line" data-l="2">&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">if</span> (a.<span class="fn">size</span>() &lt;= <span class="num">1</span>) <span class="kw">return</span>;</span><span class="line" data-l="3">&nbsp;&nbsp;&nbsp;&nbsp;size_t mid = a.<span class="fn">size</span>() / <span class="num">2</span>;</span><span class="line" data-l="4">&nbsp;&nbsp;&nbsp;&nbsp;vector&lt;<span class="kw">int</span>&gt; left(a.<span class="fn">begin</span>(), a.<span class="fn">begin</span>() + mid);</span><span class="line" data-l="5">&nbsp;&nbsp;&nbsp;&nbsp;<span class="fn">mergeSort</span>(left);</span><span class="line" data-l="6">&nbsp;&nbsp;&nbsp;&nbsp;vector&lt;<span class="kw">int</span>&gt; right(a.<span class="fn">begin</span>() + mid, a.<span class="fn">end</span>()); <span class="fn">mergeSort</span>(right);</span><span class="line" data-l="7">&nbsp;&nbsp;&nbsp;&nbsp;<span class="com">// merge left and right back into a</span></span><span class="line" data-l="8">&nbsp;&nbsp;&nbsp;&nbsp;size_t i = <span class="num">0</span>, j = <span class="num">0</span>, k = <span class="num">0</span>;</span><span class="line" data-l="9">&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">while</span> (i &lt; left.<span class="fn">size</span>() &amp;&amp; j &lt; right.<span class="fn">size</span>()) {</span><span class="line" data-l="10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">if</span> (left[i] &lt;= right[j])</span><span class="line" data-l="11">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a[k++] = left[i++];</span><span class="line" data-l="12">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">else</span></span><span class="line" data-l="13">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a[k++] = right[j++];</span><span class="line" data-l="14">&nbsp;&nbsp;&nbsp;&nbsp;} <span class="com">// then copy either remaining tail</span></span><span class="line">&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">while</span> (i &lt; left.<span class="fn">size</span>()) a[k++] = left[i++];</span><span class="line">&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">while</span> (j &lt; right.<span class="fn">size</span>()) a[k++] = right[j++];</span><span class="line" data-l="15">}</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">複雜度</div>
        <div class="ic-row"><span class="ic-label">時間 (各情況)</span><span class="ic-value best">$O(n \log n)$</span></div>
        <div class="ic-row"><span class="ic-label">空間</span><span class="ic-value worst">$O(n)$ 額外</span></div>
        <div class="ic-row"><span class="ic-label">是否穩定</span><span class="ic-value">穩定 ✓</span></div>
      </div>
    </div>
  </div>

  <div class="info-box green">
    <span class="info-label">為何是 n log n？</span>
    每一層遞迴把問題切成兩半 → 共 $\log_2 n$ 層；每一層的「merge 動作」總共要看過所有 $n$ 個元素 → 每層 $O(n)$。整體 $O(n) \times O(\log n) = O(n \log n)$。<br>
    這是<strong>比較式排序的下界</strong>：任何只透過比較來排序的演算法都至少要 $\Omega(n\log n)$，merge sort 達到這個下界。
  </div>

  <div class="info-box warm">
    <span class="info-label">代價：額外空間</span>
    merge sort 需要<strong>額外 $O(n)$ 的暫存空間</strong>來存 L、R 半段（實作中需額外配置 L、R 兩段暫存 vector）。處理超大資料時，這個記憶體開銷可能成為問題。
  </div>
{{slot:merge-end}}
'''

LEGACY['quick'] = r'''  <p><strong>Quicksort</strong> 也是分而治之，但策略不同：先選一個元素當 <em>pivot</em>（樞紐值），用一個 <strong>partition</strong> 過程把陣列重新排成「<span class="pill pill-blue">比 pivot 小</span> ｜ <span class="pill pill-purple">pivot</span> ｜ <span class="pill pill-orange">比 pivot 大</span>」三段，pivot 就<strong>確定到了它的最終位置</strong>。接著對左、右兩段各自遞迴呼叫 quicksort。和 merge sort 不一樣，<strong>不需要額外陣列</strong>，partition 就地完成。</p>

  <div class="info-box">
    <span class="info-label">partition 的雙指標技術</span>
    從 pivot 右邊開始：<span class="pill pill-green">leftMark</span> 從左往右走、找<strong>大於 pivot 的</strong>；<span class="pill pill-orange">rightMark</span> 從右往左走、找<strong>小於 pivot 的</strong>。兩者都停下時就交換它們。當 leftMark 越過 rightMark 之後，把 pivot 和 rightMark 交換，pivot 就到位了。
  </div>

{{slot:quick-intro}}
  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div class="algo-canvas" id="canvas-quick" style="height:380px;"><div class="bars-container"></div><div class="baseline"></div></div>
        <div class="status-banner"><span class="status-icon">›</span><span class="status-text" id="quickStatus">按「開始」執行快速排序</span></div>
        <div class="input-row">
          <label>陣列：</label>
          <input type="text" id="quickArrInput" value="54, 26, 93, 17, 77, 31, 44, 55, 20">
          <button class="btn btn-shuffle" id="quickShuffle">隨機洗牌</button>
          <button class="btn btn-shuffle" id="quickApply" style="background:var(--accent2);">套用</button>
        </div>
        <div class="input-row">
          <label>pivot 策略：</label>
          <button class="preset-btn active" data-pivot="first">第一個 (講義版本)</button>
          <button class="preset-btn" data-pivot="median">三者取中 median-of-three</button>
        </div>
        <div class="controls-bar">
          <button class="btn btn-play" id="quickPlay">▶ 開始</button>
          <button class="btn btn-step" id="quickStep">→ 單步</button>
          <button class="btn btn-reset" id="quickReset">↺ 重置</button>
          <div style="flex:1;min-width:160px;display:flex;align-items:center;gap:.5rem;">
            <span style="font-size:.78rem;color:var(--muted);">速度</span>
            <input type="range" id="quickSpeed" min="100" max="1500" step="50" value="500" style="flex:1;accent-color:var(--accent3);">
          </div>
        </div>
      </div>
    </div>

    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">即時狀態 <span class="ic-badge">LIVE</span></div>
        <div class="ic-row"><span class="ic-label">當前 pivot</span><span class="ic-value highlight" id="quickPivot">—</span></div>
        <div class="ic-row"><span class="ic-label">左右範圍 [first, last]</span><span class="ic-value" id="quickRange">—</span></div>
        <div class="ic-row"><span class="ic-label">leftMark</span><span class="ic-value" id="quickLM" style="color:#16a085;">—</span></div>
        <div class="ic-row"><span class="ic-label">rightMark</span><span class="ic-value" id="quickRM" style="color:#d35400;">—</span></div>
        <div class="stats-grid" style="margin-top:.5rem;">
          <div class="stat-tile compare"><div class="stat-label">比較</div><div class="stat-value" id="quickCmp">0</div></div>
          <div class="stat-tile swap"><div class="stat-label">交換</div><div class="stat-value" id="quickSwp">0</div></div>
        </div>
      </div>
      <div class="info-card">
        <div class="ic-title">虛擬碼</div>
        <div class="pseudo-code" id="quickCode"><span class="line"><span class="kw">void</span> <span class="fn">quickSortHelper</span>(vector&lt;<span class="kw">int</span>&gt;&amp; a, <span class="kw">int</span> first, <span class="kw">int</span> last) {</span><span class="line">&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">if</span> (first &lt; last) {</span><span class="line">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">int</span> split = <span class="fn">partition</span>(a, first, last);</span><span class="line">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="fn">quickSortHelper</span>(a, first, split - <span class="num">1</span>);</span><span class="line">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="fn">quickSortHelper</span>(a, split + <span class="num">1</span>, last);</span><span class="line">&nbsp;&nbsp;&nbsp;&nbsp;}</span><span class="line">}</span></div>
      </div>
      <div class="info-card">
        <div class="ic-title">複雜度</div>
        <div class="ic-row"><span class="ic-label">最佳 / 平均</span><span class="ic-value best">$O(n \log n)$</span></div>
        <div class="ic-row"><span class="ic-label">最差 (pivot 極差)</span><span class="ic-value worst">$O(n^2)$</span></div>
        <div class="ic-row"><span class="ic-label">空間 (遞迴)</span><span class="ic-value">$O(\log n)$ 期望</span></div>
      </div>
    </div>
  </div>

  <div class="info-box warm">
    <span class="info-label">最差情況：當 pivot 是極端值</span>
    若每次選的 pivot 剛好是最大或最小（例如已排序的陣列 + 「選第一個當 pivot」策略），每次只能切下 1 個元素 → 退化成 $O(n^2)$。<strong>median-of-three</strong> 取「first、middle、last 三者中位數」當 pivot，能大幅降低最差情況的機率，對「幾乎排序好」的資料尤其有效。
  </div>

  <div class="info-box">
    <span class="info-label">vs. merge sort</span>
    quicksort <strong>就地排序，不需要 $O(n)$ 額外空間</strong>，常數係數也比 merge sort 小，<strong>實務上通常更快</strong>。但 quicksort 不穩定、且最差是 $O(n^2)$；merge sort 任何情況都是 $O(n\log n)$ 且穩定。C++ 標準只規定 <code>std::sort()</code> 的最差比較次數為 $O(n\log n)$，不指定實作策略；常見標準函式庫採 introsort 類混合實作。<code>std::stable_sort()</code> 保證穩定，但實作方式同樣由函式庫決定。
  </div>
{{slot:quick-end}}
'''

LEGACY['depends'] = r'''  <p>同樣的演算法，搬到不同的資料結構上效能可能截然不同，甚至根本跑不動。本節整理本章九個演算法各自<strong>能在哪些資料結構上有效執行</strong>，重點放在「為什麼某些演算法<em>必須</em>用 Array 而不能用 Linked List」這個關鍵差異上。</p>

  <h3>兩種基本存取模式</h3>
  <div class="viz-layout">
    <div>
      <div class="info-card">
        <div class="ic-title">Random Access — 隨機存取 <span class="ic-badge" style="background:#2980b9;">FAST</span></div>
        <div style="font-size:.86rem;line-height:1.7;">
          可以用「索引」<strong>$O(1)$ 跳到任意位置</strong>。陣列 (Array) 最典型：記憶體連續，<code>a[i]</code> 直接用 <code>base + i × sizeof(T)</code> 算出位址即可。<br><br>
          <span class="pill pill-blue">代表結構</span> C++ <code>vector</code>、C 風格 array、Java <code>ArrayList</code><br>
          <span class="pill pill-green">關鍵動作</span> <code>a[i]</code> = $O(1)$，<code>a[i] = v</code> = $O(1)$，連續走訪 cache 友善
        </div>
      </div>
    </div>
    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">Sequential Access — 循序存取 <span class="ic-badge" style="background:var(--accent);">SLOW INDEX</span></div>
        <div style="font-size:.86rem;line-height:1.7;">
          只能<strong>從頭往後一個一個走</strong>（透過 <code>node.next</code>）；想跳到第 $k$ 個必須走過前 $k-1$ 個 → $O(k)$。<br><br>
          <span class="pill pill-purple">代表結構</span> Linked List (鏈結串列)、Iterator、Generator、Stream<br>
          <span class="pill pill-orange">優勢</span> 中間插入/刪除 $O(1)$（已知前一節點時）、不用連續記憶體
        </div>
      </div>
    </div>
  </div>

  <h3>核心對照表：每個演算法所需的資料結構</h3>
  <div class="table-scroll" tabindex="0" aria-label="比較表，可左右捲動"><table class="cmp-table">
    <thead>
      <tr>
        <th>演算法</th>
        <th>必要屬性</th>
        <th style="background:#2980b9;">Array</th>
        <th style="background:#8e44ad;">Linked List</th>
        <th>關鍵原因</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>循序搜尋</td>
        <td>可逐一拜訪</td>
        <td class="best">✓ 自然</td>
        <td class="best">✓ 自然</td>
        <td>只需 sequential access，兩種結構都可以</td>
      </tr>
      <tr>
        <td>有序循序搜尋</td>
        <td>可逐一拜訪 + <strong>有序</strong></td>
        <td class="best">✓</td>
        <td class="best">✓</td>
        <td>遇到 a[pos] &gt; item 即停，鏈結串列也行</td>
      </tr>
      <tr style="background:#fef0e7;">
        <td><strong>二分搜尋</strong></td>
        <td>$O(1)$ 隨機存取 + 有序</td>
        <td class="best">✓ <strong>必須</strong></td>
        <td class="worst">✗ 不行</td>
        <td>跳到 midpoint 在鏈結串列要 $O(n)$，破壞 $\log n$</td>
      </tr>
      <tr>
        <td>雜湊表 (Hashing)</td>
        <td>固定大小 array 當底層</td>
        <td class="best">✓ <strong>必須</strong></td>
        <td class="worst">✗</td>
        <td>$h(\text{item}) \to$ slot 索引，必須隨機存取</td>
      </tr>
      <tr>
        <td>氣泡排序</td>
        <td>隨機存取 + 可變</td>
        <td class="best">✓</td>
        <td>△ 慢但可</td>
        <td>需要 a[j] 與 a[j+1] 的相鄰比較交換</td>
      </tr>
      <tr>
        <td>選擇排序</td>
        <td>隨機存取 + 可交換</td>
        <td class="best">✓</td>
        <td>△ 慢但可</td>
        <td>找到 maxPos 後 swap a[maxPos] ↔ a[fill]</td>
      </tr>
      <tr>
        <td>插入排序</td>
        <td>隨機存取（位移）</td>
        <td class="best">✓</td>
        <td>△ 變體可行</td>
        <td>位移 a[curPos-1] → a[curPos] 在 array 是 $O(1)$</td>
      </tr>
      <tr style="background:#fef0e7;">
        <td><strong>希爾排序</strong></td>
        <td>隨機存取（gap 跳格）</td>
        <td class="best">✓ <strong>必須</strong></td>
        <td class="worst">✗ 不行</td>
        <td>需要 a[pos − gap]，鏈結串列做不到「跳 gap 格」</td>
      </tr>
      <tr style="background:#eafaf1;">
        <td><strong>合併排序</strong></td>
        <td>可拆分 + 可合併</td>
        <td>✓ 但需 $O(n)$ 額外空間</td>
        <td class="best">✓ <strong>更佳！</strong> $O(1)$ 額外空間</td>
        <td>鏈結串列 merge 只重接指標，不必複製 ★</td>
      </tr>
      <tr style="background:#fef0e7;">
        <td><strong>快速排序</strong></td>
        <td>雙向隨機存取（雙指標）</td>
        <td class="best">✓ <strong>必須</strong></td>
        <td class="worst">✗ 不行</td>
        <td>partition 需要左右雙指標雙向走，singly-linked 無法</td>
      </tr>
    </tbody>
  </table></div>
  <p style="font-size:.82rem;color:var(--muted);margin-top:.4rem;">
    <span class="pill" style="background:var(--accent3);color:#fff;">✓</span> 自然支援　
    <span class="pill" style="background:#f39c12;color:#fff;">△</span> 可以但效能下降　
    <span class="pill" style="background:var(--accent);color:#fff;">✗</span> 演算法的核心動作做不到，必須換結構
  </p>

  <h3>三個值得記住的關鍵案例</h3>

  <div class="info-box warm">
    <span class="info-label">為何「Binary Search 必須要 Array」？</span>
    Binary search 每次跳到 <code>midpoint = first + (last-first)/2</code>。<br>
    　・在 Array：用記憶體位址計算就能 $O(1)$ 取到 a[midpoint]<br>
    　・在 Linked List：要走到第 midpoint 個 node 必須<strong>從頭走 midpoint 步</strong>，每次比較都要 $O(n)$<br><br>
    這樣總時間就從 $O(\log n)$ 退化成 $O(n \log n)$，比循序搜尋還慢！結論：<strong>排序好的資料若以 Linked List 儲存，binary search 沒有意義</strong>，必須轉成 Array（或一開始就用 Array）。
  </div>

  <div class="info-box warm">
    <span class="info-label">為何「Quick Sort 不能用 Singly Linked List」？</span>
    Partition 需要兩個指標 <code>leftMark</code>、<code>rightMark</code>：一個從左往右、一個<strong>從右往左</strong>走。<br><br>
    但<strong>單向鏈結串列只能從左往右</strong>（每個 node 只有 <code>next</code>，沒有 <code>prev</code>），<code>rightMark--</code> 沒有有效率的實作方式。雖然 <em>doubly-linked list</em> 可以雙向走，但每次比較都要追指標、cache miss 嚴重，常數係數比 Array 大太多。<br><br>
    這就是為什麼<strong>快速排序的教科書版本永遠用 Array 來講</strong>：partition 的優美只在 Array 上才成立。
  </div>

  <div class="info-box green">
    <span class="info-label">為何「Merge Sort 反而<em>更</em>適合 Linked List」？★ 反直覺！</span>
    Array 版的 merge sort 需要 $O(n)$ 額外空間存 L、R 子陣列。但<strong>Linked List 版的 merge 只需重接指標</strong>：把較小的 node 從左/右串列上「摘下」，接到結果串列尾端，<strong>完全不需要複製資料</strong>，額外空間只有 $O(1)$（幾個指標變數而已）。<br><br>
    換句話說，merge sort 在 linked list 上反而<strong>更省記憶體、更乾淨</strong>。所以當資料天生就是 linked list 形式（functional 語言、stream pipeline、某些 OS 內部資料結構），merge sort 是首選排序法。<br><br>
    <strong>實務小知識：</strong>Java 的 <code>java.util.LinkedList.sort()</code> 內部就是先轉成 Array 再用 mergesort，因為 cache 表現更好；但概念上 linked list mergesort 是經典範例。
  </div>

  <h3>Hash Table 自身的內部結構</h3>
  <div class="info-box">
    <span class="info-label">Hash Table 是什麼底層結構？答：仍然是 Array！</span>
    Hash table <strong>本身的底層</strong>就是一個固定大小（$m$）的 Array：
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:.6rem;margin-top:.5rem;">
      <div style="background:#fff;padding:.7rem;border-radius:6px;border:1px solid var(--card-border);">
        <strong style="color:var(--bar-default);">線性 / 平方探查</strong><br>
        <span style="font-family:'JetBrains Mono',monospace;font-size:.78rem;">純 Array of (key, value)；衝突時往別的 slot 找空位</span>
      </div>
      <div style="background:#fff;padding:.7rem;border-radius:6px;border:1px solid var(--card-border);">
        <strong style="color:var(--accent2);">鏈結法 chaining</strong><br>
        <span style="font-family:'JetBrains Mono',monospace;font-size:.78rem;">Array of <em>Linked List</em>；每個 slot 是一條 list 的 head</span>
      </div>
      <div style="background:#fff;padding:.7rem;border-radius:6px;border:1px solid var(--card-border);grid-column:1/-1;">
        <strong style="color:var(--accent3);">Map ADT 實作（講義版本）</strong><br>
        <span style="font-family:'JetBrains Mono',monospace;font-size:.78rem;">兩個平行 Array：<code>slots[]</code> 存 key、<code>data[]</code> 存 value，索引位置一一對齊</span>
      </div>
    </div>
    這就是為何 C++ <code>unordered_map</code>、Java <code>HashMap</code> 內部都看得到 Array：雜湊表離不開 random access。
  </div>

  <h3>選擇底層結構的決策樹</h3>
  <div class="info-card">
    <div class="ic-title">給定情境，該選哪種底層結構？</div>
    <div style="font-size:.88rem;line-height:1.85;">
      <strong>① 需要快速隨機存取 + 排序後重複搜尋？</strong><br>
      &nbsp;&nbsp;→ <span class="pill pill-blue">Array</span> + 排序 $O(n\log n)$ 一次 + 二分搜尋 $O(\log n)$ 多次<br>
      <br>
      <strong>② 大量「鍵值對」key-value 查詢？</strong><br>
      &nbsp;&nbsp;→ <span class="pill pill-purple">Hash Table</span>（底層 Array），平均 $O(1)$ 查詢<br>
      <br>
      <strong>③ 頻繁從中間插入/刪除元素？</strong><br>
      &nbsp;&nbsp;→ <span class="pill pill-orange">Linked List</span>，必要時排序選 merge sort（$O(1)$ 額外空間版本）<br>
      <br>
      <strong>④ 資料天然有序、僅追加（如 log）？</strong><br>
      &nbsp;&nbsp;→ 順序儲存（Array 或 file stream），搜尋用循序或二分皆可
    </div>
  </div>

  <div class="info-box warm">
    <span class="info-label">本章其他資料結構的關係（前情提要）</span>
    本書前幾章學過的資料結構，在本章扮演的角色：
    <ul style="margin:.4rem 0;padding-left:1.4rem;font-size:.86rem;line-height:1.7;">
      <li><strong>Stack：</strong>quick sort / merge sort 的<strong>遞迴呼叫堆疊</strong>就是 stack；如果改寫成 iterative 版本，會明確使用一個 stack 來模擬遞迴。</li>
      <li><strong>Queue：</strong>iterative merge sort 的「bottom-up」版本可以用 queue 來組織待合併的子串列。</li>
      <li><strong>Linked List：</strong>chaining 法雜湊表的 collision bucket、merge sort 的最佳載體。</li>
      <li><strong>Tree：</strong>合併排序的遞迴呼叫關係本身就是一棵<strong>二元樹</strong>（PART 08 的視覺化就是把這棵樹畫出來）。</li>
    </ul>
    搜尋與排序不是孤立的章節：它們是建立在前面所有資料結構之上的<strong>應用範例</strong>。
  </div>
'''

LEGACY['reference'] = r'''
  <h3>搜尋演算法</h3>
  <div class="table-scroll" tabindex="0" aria-label="比較表，可左右捲動"><table class="cmp-table">
    <thead><tr><th>演算法</th><th>最佳</th><th>平均</th><th>最差</th><th>前置條件</th><th>空間</th></tr></thead>
    <tbody>
      <tr><td>循序搜尋</td><td>$O(1)$</td><td>$O(n)$</td><td class="worst">$O(n)$</td><td>無</td><td>$O(1)$</td></tr>
      <tr><td>循序搜尋 (有序)</td><td>$O(1)$</td><td>$O(n/2)$</td><td>$O(n)$</td><td>已排序</td><td>$O(1)$</td></tr>
      <tr><td>二分搜尋</td><td class="best">$O(1)$</td><td class="best">$O(\log n)$</td><td class="best">$O(\log n)$</td><td>已排序</td><td>$O(1)$</td></tr>
      <tr><td>雜湊 (理想)</td><td class="best">$O(1)$</td><td class="best">$O(1)$</td><td class="worst">$O(n)$</td><td>有 hash 函數</td><td>$O(m)$</td></tr>
    </tbody>
  </table></div>

  <h3>排序演算法</h3>
  <div class="table-scroll" tabindex="0" aria-label="比較表，可左右捲動"><table class="cmp-table">
    <thead><tr><th>演算法</th><th>最佳</th><th>平均</th><th>最差</th><th>空間</th><th>穩定</th><th>就地</th></tr></thead>
    <tbody>
      <tr><td>氣泡排序 Bubble</td><td>$O(n)$ ★</td><td>$O(n^2)$</td><td class="worst">$O(n^2)$</td><td>$O(1)$</td><td>✓</td><td>✓</td></tr>
      <tr><td>選擇排序 Selection</td><td>$O(n^2)$</td><td>$O(n^2)$</td><td class="worst">$O(n^2)$</td><td>$O(1)$</td><td>✗</td><td>✓</td></tr>
      <tr><td>插入排序 Insertion</td><td class="best">$O(n)$</td><td>$O(n^2)$</td><td>$O(n^2)$</td><td>$O(1)$</td><td>✓</td><td>✓</td></tr>
      <tr><td>希爾排序 Shell</td><td>$O(n\log n)$</td><td>$O(n^{3/2})$</td><td>$O(n^2)$</td><td>$O(1)$</td><td>✗</td><td>✓</td></tr>
      <tr><td>合併排序 Merge</td><td class="best">$O(n\log n)$</td><td class="best">$O(n\log n)$</td><td class="best">$O(n\log n)$</td><td class="worst">$O(n)$</td><td>✓</td><td>✗</td></tr>
      <tr><td>快速排序 Quick</td><td class="best">$O(n\log n)$</td><td class="best">$O(n\log n)$</td><td class="worst">$O(n^2)$</td><td>$O(\log n)$</td><td>✗</td><td>✓</td></tr>
    </tbody>
  </table></div>
  <p style="font-size:.82rem;color:var(--muted);">★ 氣泡排序的 $O(n)$ 最佳情況需要使用<strong>「短路最佳化」</strong>（一輪沒交換就停）。</p>

  <h3>選擇指南</h3>
  <div class="table-scroll" tabindex="0" aria-label="比較表，可左右捲動"><table class="cmp-table">
    <thead><tr><th>情境</th><th>建議演算法</th><th>原因</th></tr></thead>
    <tbody>
      <tr><td>資料量小 (n &lt; 20)</td><td>插入排序</td><td>常數小、邏輯簡單</td></tr>
      <tr><td>資料幾乎已排序</td><td>插入排序 / 氣泡 (短路)</td><td>$O(n)$ 最佳</td></tr>
      <tr><td>需要穩定且效能保證</td><td>合併排序</td><td>始終 $O(n\log n)$、穩定</td></tr>
      <tr><td>記憶體有限</td><td>希爾 / 快速排序</td><td>就地排序</td></tr>
      <tr><td>實務通用、最快</td><td>快速排序 (含中位數策略)</td><td>常數最小</td></tr>
      <tr><td>大量搜尋同份資料</td><td>排序後二分搜尋 / 雜湊表</td><td>建立成本攤提</td></tr>
      <tr><td>需要 $O(1)$ 平均搜尋</td><td>雜湊表</td><td>用空間換時間</td></tr>
    </tbody>
  </table></div>

  <h3>關鍵概念複習</h3>
  <div class="info-box">
    <span class="info-label">穩定 stable</span>
    當兩個元素「比較相等」時，若排序後它們的<strong>相對順序不變</strong>，演算法就是穩定的。在多鍵排序（先按姓名再按部門）時很重要。
  </div>
  <div class="info-box">
    <span class="info-label">就地 in-place</span>
    僅使用 $O(1)$ 或 $O(\log n)$ 額外空間（除了輸入本身）的排序。merge sort 不是就地（需要 $O(n)$ 暫存），quick sort 是（只需遞迴堆疊）。
  </div>
  <div class="info-box green">
    <span class="info-label">比較式排序的下界</span>
    任何只透過「兩兩比較」來排序的演算法，最差情況都至少要 $\Omega(n\log n)$ 次比較。merge / heap / 平均下的 quick sort 都達到這個下界。要打破它必須使用「非比較」方法，例如 counting sort 或 radix sort（要求資料形態特定）。
  </div>
'''

LEGACY['supplement'] = r'''  <p>這一節把兩個容易卡住的地方一步一步追蹤一次：（A）平方探查把 44、55、20 放進表裡時，為什麼會落在那些位置；（B）Map ADT 的 <code>put()</code> 為什麼有 4 個 if/else 分支、每個分支什麼時候會被觸發，以及哪一種才是真正的 collision。</p>

  <!-- ============= PART A : quadratic probing trace ============= -->
  <h3 id="sup-quadratic" style="margin-top:1.5rem;">A. Quadratic probing 全程追蹤（m = 11）</h3>

  <div class="info-box">
    <span class="info-label">設定</span>
    <strong>雜湊函數</strong>：$h(\text{item}) = \text{item} \bmod 11$。<br>
    <strong>Rehash</strong>：$\text{rehash}(p, \text{skip}) = (p + \text{skip}) \bmod 11$，其中 skip 依序取 $1^2, 2^2, 3^2, 4^2, 5^2, \ldots = 1, 4, 9, 16, 25, \ldots$（這也是「quadratic」的由來）。<br>
    <strong>插入順序</strong>：<code>54, 26, 93, 17, 77, 31, 44, 55, 20</code>（和雜湊一節的圖使用同一組資料）。
  </div>

  <h4 style="margin-top:1.2rem;color:var(--accent2);font-family:'Noto Serif TC',serif;">Step 1：前六筆都直接落空槽</h4>
  <div class="table-scroll" tabindex="0" aria-label="比較表，可左右捲動"><table class="cmp-table">
    <thead><tr><th>item</th><th>item % 11</th><th>落點 slot</th><th>狀況</th></tr></thead>
    <tbody>
      <tr><td>54</td><td>10</td><td>10</td><td>空 ✓</td></tr>
      <tr><td>26</td><td>4</td><td>4</td><td>空 ✓</td></tr>
      <tr><td>93</td><td>5</td><td>5</td><td>空 ✓</td></tr>
      <tr><td>17</td><td>6</td><td>6</td><td>空 ✓</td></tr>
      <tr><td>77</td><td>0</td><td>0</td><td>空 ✓</td></tr>
      <tr><td>31</td><td>9</td><td>9</td><td>空 ✓</td></tr>
    </tbody>
  </table></div>
  <p>此時表的狀態：</p>
<pre style="background:#2d2d3f;color:#e8e6df;font-family:'JetBrains Mono',monospace;font-size:.82rem;padding:.85rem 1rem;border-radius:10px;line-height:1.6;overflow-x:auto;">idx :  0    1    2    3    4    5    6    7    8    9    10
val : 77    .    .    .   26   93   17    .    .   31    54</pre>

  <h4 style="margin-top:1.2rem;color:var(--accent2);font-family:'Noto Serif TC',serif;">Step 2：插 44（44 % 11 = 0，撞 77）</h4>
  <div class="table-scroll" tabindex="0" aria-label="比較表，可左右捲動"><table class="cmp-table">
    <thead><tr><th>嘗試</th><th>skip</th><th>計算位置</th><th>slot 內容</th><th>結果</th></tr></thead>
    <tbody>
      <tr><td>1</td><td>$1^2 = 1$</td><td>(0+1) % 11 = <strong>1</strong></td><td>空</td><td><span class="pill pill-green">落 slot 1</span></td></tr>
    </tbody>
  </table></div>

  <h4 style="margin-top:1.2rem;color:var(--accent2);font-family:'Noto Serif TC',serif;">Step 3：插 55（55 % 11 = 0，撞 77；之後又連撞 4 次）</h4>
  <div class="table-scroll" tabindex="0" aria-label="比較表，可左右捲動"><table class="cmp-table">
    <thead><tr><th>嘗試</th><th>skip</th><th>計算位置</th><th>slot 內容</th><th>結果</th></tr></thead>
    <tbody>
      <tr><td>1</td><td>$1^2 = 1$</td><td>(0+1) % 11 = 1</td><td>44</td><td>占用</td></tr>
      <tr><td>2</td><td>$2^2 = 4$</td><td>(0+4) % 11 = 4</td><td>26</td><td>占用</td></tr>
      <tr><td>3</td><td>$3^2 = 9$</td><td>(0+9) % 11 = 9</td><td>31</td><td>占用</td></tr>
      <tr><td>4</td><td>$4^2 = 16$</td><td>(0+16) % 11 = <strong>5</strong></td><td>93</td><td>占用</td></tr>
      <tr><td>5</td><td>$5^2 = 25$</td><td>(0+25) % 11 = <strong>3</strong></td><td>空</td><td><span class="pill pill-green">落 slot 3</span></td></tr>
    </tbody>
  </table></div>
  <div class="info-box warm">
    <span class="info-label">關鍵</span>
    skip 序列是「<strong>連續完全平方數本身</strong>」（$1, 4, 9, 16, 25$），<strong>不是累加</strong>。每次都從原始 hash 位置 $h$ 起算，所以第 4 次跳到 $(0+16) \bmod 11 = 5$、第 5 次跳到 $(0+25) \bmod 11 = 3$：兩次都「跨過」了表的另一端。這正是 quadratic probing 能打散 linear probing 那種連續聚集（clustering）的原因。
  </div>

  <h4 style="margin-top:1.2rem;color:var(--accent2);font-family:'Noto Serif TC',serif;">Step 4：插 20（20 % 11 = 9，撞 31）</h4>
  <div class="table-scroll" tabindex="0" aria-label="比較表，可左右捲動"><table class="cmp-table">
    <thead><tr><th>嘗試</th><th>skip</th><th>計算位置</th><th>slot 內容</th><th>結果</th></tr></thead>
    <tbody>
      <tr><td>1</td><td>$1^2 = 1$</td><td>(9+1) % 11 = 10</td><td>54</td><td>占用</td></tr>
      <tr><td>2</td><td>$2^2 = 4$</td><td>(9+4) % 11 = <strong>2</strong></td><td>空</td><td><span class="pill pill-green">落 slot 2</span></td></tr>
    </tbody>
  </table></div>

  <h4 style="margin-top:1.2rem;color:var(--accent2);font-family:'Noto Serif TC',serif;">最終表狀態</h4>
<pre style="background:#2d2d3f;color:#e8e6df;font-family:'JetBrains Mono',monospace;font-size:.82rem;padding:.85rem 1rem;border-radius:10px;line-height:1.6;overflow-x:auto;">idx :  0    1    2    3    4    5    6    7    8    9    10
val : 77   44   20   55   26   93   17    .    .   31    54</pre>


  <!-- ============= PART B : Map ADT put() 4 branches ============= -->
  <h3 id="sup-put" style="margin-top:2rem;">B. Map ADT <code>put()</code> 的 4 個分支（最容易跟 collision 搞混的地方）</h3>

  <div class="info-box warm">
    <span class="info-label">先講清楚：什麼是 collision、什麼不是？</span>
    <strong style="display:block;font-size:1.05em;color:var(--accent);">Collision 的判準是「<u>hash 值</u>相同」，不是「key 相同」，千萬別搞反。</strong>
    <p style="margin-top:.5rem;">正式定義：<strong>兩個<u>不同的 item</u> 經過 <code>hashFunction</code> 後得到<u>同一個 hash 值</u></strong>（也就是 <code>hash(k₁) == hash(k₂)</code>，因此被映射到同一個 slot），這才叫 collision。判 collision 看的是「hash 值」這個運算結果，不是「key 本身」。</p>
    <p>同一個 key 重複 <code>put</code>（如 <code>h.put(77, "bird")</code> 然後 <code>h.put(77, "eagle")</code>）：hash 值當然會相同，<strong>但兩次塞的是同一個 item</strong>，只是更新同一個 entry，<strong>這不是 collision，也不會觸發任何 rehash</strong>。collision 必須是「兩個不同 item 撞到同一格」。</p>
    <div class="table-scroll" tabindex="0" aria-label="比較表，可左右捲動"><table class="cmp-table" style="margin-top:.8rem;">
      <thead><tr><th>狀況</th><th>兩個 item 的 hash 值</th><th>是同一個 key 嗎？</th><th>這算 collision 嗎？</th><th><code>put</code> 要做的事</th></tr></thead>
      <tbody>
        <tr><td>情況一</td><td>相同（必然）</td><td>是（同 key 重複 put）</td><td><span class="pill pill-green">不是</span></td><td>直接覆寫舊值（字典「同 key 重新賦值」的語意）</td></tr>
        <tr><td>情況二</td><td><strong>相同</strong>（hash 撞到了）</td><td><strong>否</strong>（不同 key）</td><td><span class="pill pill-orange">是</span></td><td>啟動 rehash 探查，找下一個位置</td></tr>
        <tr><td>情況三</td><td>不同</td><td>否</td><td><span class="pill pill-green">不是</span></td><td>各走各的 slot，互不相干</td></tr>
      </tbody>
    </table></div>
    <p style="margin-top:.5rem;font-size:.92em;">情況一、二 在程式裡都會「<code>slots[hash]</code> 已經有東西」，但只有情況二才是真 collision：差別就在那個被佔的 slot 裡放的 key 跟我「是不是同一個 item」。</p>
  </div>

  <h4 style="margin-top:1.2rem;color:var(--accent2);font-family:'Noto Serif TC',serif;">課程強化版本的 <code>put()</code>：探查一圈就停</h4>
  <div class="pseudo-code">
<span class="line"><span class="kw">void</span> <span class="fn">put</span>(<span class="kw">int</span> key, string value) {</span>
<span class="line">    <span class="kw">int</span> start = <span class="fn">hashFunction</span>(key);</span>
<span class="line">    <span class="kw">int</span> position = start;</span>
<span class="line">    <span class="kw">do</span> {</span>
<span class="line">        <span class="kw">if</span> (slots[position] == -<span class="num">1</span>) { <span class="com">// ① 或 ③：插入</span></span>
<span class="line">            slots[position] = key; data[position] = value; <span class="kw">return</span>;</span>
<span class="line">        }</span>
<span class="line">        <span class="kw">if</span> (slots[position] == key) {   <span class="com">// ② 或 ④：更新</span></span>
<span class="line">            data[position] = value; <span class="kw">return</span>;</span>
<span class="line">        }</span>
<span class="line">        position = <span class="fn">rehash</span>(position);</span>
<span class="line">    } <span class="kw">while</span> (position != start);</span>
<span class="line">    <span class="kw">throw</span> overflow_error(<span class="str">"hash table is full"</span>);</span>
<span class="line">}</span></div>
  <p style="font-size:.9rem;color:var(--muted);">教科書的基本版若只寫「找到空槽或同 key 才停」，滿表時會無限繞圈。課程 header 用起點作哨兵：完整探查一圈後明確丟出 <code>overflow_error</code>。</p>

  <h4 style="margin-top:1.2rem;color:var(--accent2);font-family:'Noto Serif TC',serif;">把 4 個分支按「碰撞 / 探查」分類</h4>
  <div class="table-scroll" tabindex="0" aria-label="比較表，可左右捲動"><table class="cmp-table">
    <thead><tr><th></th><th>hash 第一次命中（無探查）</th><th>rehash 探查之後</th></tr></thead>
    <tbody>
      <tr><td><strong>新增 entry</strong>（slot 是空的）</td><td>① 起始槽直接插入</td><td>③ 探查後遇空槽<br><span style="color:var(--accent3);font-weight:700;">↑ 真正在「處理 collision」的路徑</span></td></tr>
      <tr><td><strong>覆寫已有同 key</strong>（不是 collision）</td><td>② 起始槽直接更新</td><td>④ 探查後遇同 key<br><span style="color:var(--muted);">沿探查路徑找回既有 key</span></td></tr>
    </tbody>
  </table></div>

  <h4 style="margin-top:1.2rem;color:var(--accent2);font-family:'Noto Serif TC',serif;">情境設定：4 步剛好走 4 個分支</h4>
  <p><code>HashTable h(11);</code>，<code>hash = key % 11</code>，<code>rehash = (p+1) % 11</code>。依序執行下列 4 條 <code>h.put(key, value)</code>，每一條剛好觸發一個分支：</p>

  <div class="table-scroll" tabindex="0" aria-label="比較表，可左右捲動"><table class="cmp-table">
    <thead><tr><th>步驟</th><th>操作</th><th>hash</th><th>slots[hash]</th><th>走哪條分支</th><th>是 collision 嗎？</th><th>為何</th></tr></thead>
    <tbody>
      <tr><td>1</td><td><code>h.put(77, "bird")</code></td><td>0</td><td><code>-1</code></td><td><strong>① 起始槽直接插入</strong></td><td>—</td><td style="text-align:left;font-family:'Noto Sans TC',sans-serif;">slot 0 空，直接寫入，不必探查</td></tr>
      <tr><td>2</td><td><code>h.put(77, "eagle")</code></td><td>0</td><td><code>77</code></td><td><strong>② 起始槽直接更新</strong></td><td><span class="pill pill-green">否</span></td><td style="text-align:left;font-family:'Noto Sans TC',sans-serif;">slot 0 已有的 key 就是 77 → 同 key 重新賦值，直接覆寫，<strong>不啟動 rehash</strong></td></tr>
      <tr><td>3</td><td><code>h.put(44, "goat")</code></td><td>0</td><td><code>77</code> (≠ 44)</td><td><strong>③ 探查後遇空槽</strong></td><td><span class="pill pill-orange">是</span></td><td style="text-align:left;font-family:'Noto Sans TC',sans-serif;">44 和 77 hash 值都是 0（不同 key、相同 hash） → collision → 探查到 slot 1 的空槽後插入</td></tr>
      <tr><td>4</td><td><code>h.put(44, "lamb")</code></td><td>0</td><td><code>77</code> (≠ 44)</td><td><strong>④ 探查後遇同 key</strong></td><td><span class="pill pill-green">不是新的 collision</span></td><td style="text-align:left;font-family:'Noto Sans TC',sans-serif;">44 真正存於 slot 1；沿既有碰撞探查鏈找到同 key 後覆寫 value</td></tr>
    </tbody>
  </table></div>

  <h4 style="margin-top:1.2rem;color:var(--accent2);font-family:'Noto Serif TC',serif;">每一步之後的表狀態（slots / data 同時看）</h4>
<pre style="background:#2d2d3f;color:#e8e6df;font-family:'JetBrains Mono',monospace;font-size:.78rem;padding:.85rem 1rem;border-radius:10px;line-height:1.6;overflow-x:auto;">init     :  slots = [ . , . , . , . , . , . , . , . , . , . , . ]
            data  = [ . , . , . , . , . , . , . , . , . , . , . ]

step 1 (① h.put(77, "bird")):
            slots = [77 , . , . , . , . , . , . , . , . , . , . ]
            data  = ["bird", . , . , . , . , . , . , . , . , . , . ]

step 2 (② h.put(77, "eagle")):  ← 同 key 覆寫，slots 不變
            slots = [77 , . , . , . , . , . , . , . , . , . , . ]
            data  = ["eagle", . , . , . , . , . , . , . , . , . , . ]

step 3 (③ h.put(44, "goat")):   ← collision，rehash 到 slot 1
            slots = [77 , 44 , . , . , . , . , . , . , . , . , . ]
            data  = ["eagle","goat", . , . , . , . , . , . , . , . , . ]

step 4 (④ h.put(44, "lamb")):   ← 不是 collision，沿著 rehash 路徑找到既存 key 44 並覆寫
            slots = [77 , 44 , . , . , . , . , . , . , . , . , . ]
            data  = ["eagle","lamb", . , . , . , . , . , . , . , . , . ]</pre>
  <p style="font-size:.86rem;color:var(--muted);">注意 <code>slots</code> 在第 4 步<strong>完全沒動</strong>，只動 <code>data</code>：這正是「同一個 key 永遠只占一格」的保證。</p>

  <div class="info-box green">
    <span class="info-label">結論</span>
    ①、③ 是插入；②、④ 是同 key 更新。③ 會為新碰撞的 key 找空槽，④ 則沿既有碰撞鏈找回舊 key。判 collision 看的是「<u>不同 item、相同 hash 值</u>」，不是「同一個 key 第二次來」。
  </div>

  <div class="info-box">
    <span class="info-label">每個探查位置都要檢查哪兩件事？</span>
    每到一格都依序判斷：
    <ul style="margin:.4rem 0 .4rem 1.4rem;line-height:1.8;">
      <li>撞到 <code>-1</code>（空槽）停 → 落到分支 ③（新插入）</li>
      <li>撞到 <code>== key</code> 停 → 落到分支 ④（覆寫）</li>
    </ul>
    <strong>不能只檢查空槽</strong>：否則「同 key 已在路徑上」時會繼續往下走，在另一格再寫一次，製造重複 key。也不能忘記「繞回起點」：滿表且 key 不存在時必須丟出 <code>overflow_error</code>，不能無限迴圈。
  </div>
'''
