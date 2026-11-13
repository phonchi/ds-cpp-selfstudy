"""Chapter 7 additions that explain or sharpen lecture points (why search and sort, when binary search stops,
static_cast<int>(size()), the gcd condition behind "use a prime table size", clustering, open addressing
versus chaining). Material the lecture does not teach (double hashing, deletion, STL search tools) is folded
and labelled （補充）. search_depth.py calls these functions; helpers are imported lazily to avoid a cycle.
"""
from content.search_programs import RUN, OUT


def _h():
    from content import search_depth as d
    return d


# ---------------------------------------------------------------- prologue
def why_block():
    d = _h()
    full = d.table(['存法', '某個值在不在', '最小值', '列出某個範圍內的值'], [
        ['未排序的 vector', '$O(n)$', '$O(n)$', '$O(n)$'],
        ['已排序的 vector', '$O(\\log n)$', '$O(1)$', '$O(\\log n + k)$'],
        ['平衡的二元搜尋樹', '$O(\\log n)$', '$O(\\log n)$', '$O(\\log n + k)$'],
        ['最小堆積（min heap）', '$O(n)$', '$O(1)$', '$O(n)$'],
        ['雜湊表', '平均 $O(1)$', '$O(n)$', '$O(n)$'],
    ])
    fold_body = ('<p>沒有一種存法在每種操作上都最快。下表比較幾種存法處理 $n$ 筆資料時的三種問題，$k$ 是範圍內的筆數：</p>'
                 + full +
                 '<p>雜湊表擅長回答「在不在」，但它依雜湊值擺放元素，不保留大小順序，找最小值或列出一段範圍時只能整張表看一遍。'
                 '已排序的 vector 做範圍查詢時，先用二分搜尋找到範圍的起點，再往後一個一個列出 $k$ 筆。'
                 '第 9 章的二元搜尋樹（Binary Search Tree，BST）平衡時也一樣：沿著樹找到起點，比範圍小的子樹整棵跳過。'
                 '堆積（heap）只保證最小值在最上面，其他元素沒有排好，所以找一般的值或列出範圍都得全部看過。'
                 '要選哪一種存法，看最常做的是哪一種操作。</p>')
    return f'''<h3>為什麼搜尋與排序放在資料結構課</h3>
<p>同樣是「找一個值」，資料怎麼存，決定了要花多少功夫。資料隨便放，只能一個一個比；資料排好序，每次比較可以排除一半；用雜湊表存，可以直接算出該去哪一格找。本章依序介紹這三種搜尋，再介紹排序：排序讓二分搜尋成為可能，也是練習分析比較次數、最佳與最差情況的好題材。</p>
{d.fold('不同存法擅長的操作', fold_body, did='srch-ops')}
'''


def stl_note():
    d = _h()
    body = ('<p>STL 大致由四個部分組成：<strong>容器</strong>（<code>vector</code>、<code>set</code>、<code>unordered_map</code> 等）負責存資料，'
            '<strong>演算法</strong>（<code>find</code>、<code>sort</code> 等）負責處理資料，<strong>迭代器</strong>（<code>begin()</code>、<code>end()</code>）把兩者接起來，'
            '<strong>函式物件</strong>（例如 <code>greater&lt;int&gt;()</code>）讓演算法換一種比較規則，例如 <code>sort</code> 預設由小到大，傳入 <code>greater&lt;int&gt;()</code> 就改成由大到小。</p>'
            + d.table(['寫法', '做法', '需要的條件', '比較次數'], [
                ['<code>find(first, last, x)</code>', '循序搜尋', '無', '$O(n)$'],
                ['<code>binary_search(first, last, x)</code>', '二分搜尋，回傳 <code>bool</code>', '範圍已排序', '$O(\\log n)$'],
                ['<code>lower_bound(first, last, x)</code>', '二分搜尋，回傳第一個不小於 <code>x</code> 的位置', '範圍已排序', '$O(\\log n)$'],
                ['<code>set&lt;int&gt;::find(x)</code>', '沿著平衡搜尋樹往下找', '用 <code>set</code> 存', '$O(\\log n)$'],
                ['<code>unordered_set&lt;int&gt;::count(x)</code>', '雜湊', '用 <code>unordered_set</code> 存', '平均 $O(1)$'],
            ])
            + d.card('標準函式庫的幾種搜尋', RUN['stl_search'], kind='run', stdout=OUT['stl_search'], show_out=True,
                     note='同一份已排序的資料：<code>find</code> 找到 54；<code>binary_search</code> 判斷 50 不在；'
                          '<code>lower_bound</code> 指向第一個不小於 50 的 54，索引 5；<code>set</code> 找到 44；<code>unordered_set</code> 裡 65 出現 1 次。'))
    return ('<p><code>std::find</code> 是標準模板庫（Standard Template Library，STL）裡的演算法。它只要求能一格一格往後走，所以各種容器都能用；'
            '代價是它不會利用資料的順序，就算 vector 已經排好，<code>find</code> 仍然從頭比到尾。要利用順序，就得改用下一節的二分搜尋。</p>\n'
            + d.fold('標準函式庫裡的其他搜尋工具', body) + '\n')


# ---------------------------------------------------------------- binary search
def bin_stop():
    d = _h()
    trace = d.table(['第幾次比較', 'first', 'last', 'midpoint', 'aList[midpoint]', '結果'], [
        ['1', '0', '9', '4', '44', '44 &lt; 50，<code>first = 5</code>'],
        ['2', '5', '9', '7', '65', '65 &gt; 50，<code>last = 6</code>'],
        ['3', '5', '6', '5', '54', '54 &gt; 50，<code>last = 4</code>'],
        ['—', '5', '4', '—', '—', '<code>first &gt; last</code>，回傳 false'],
    ])
    return f'''<h3>什麼時候停下來</h3>
<p>找得到時，比到相等就立刻 <code>return true</code>，不必等範圍縮小。找不到時，要一直縮到範圍變空才停。迴圈條件 <code>first &lt;= last</code> 的意思是：候選位置還在閉區間 <code>[first, last]</code> 裡。<code>first == last</code> 時還剩一個候選，仍然要比；<code>first &gt; last</code> 時一個候選都不剩，才能確定不在。下表是找 50 的過程：</p>
{trace}
<p>第三次比較時範圍只剩索引 5、6 兩格；54 比 50 大，<code>last</code> 變成 4，比 <code>first</code> 還小，迴圈結束。迴圈版的中點寫成 <code>(first + last) / 2</code>，遞迴版寫成 <code>first + (last - first) / 2</code>，兩者算出的索引相同；後者在 <code>first + last</code> 大到超出 <code>int</code> 範圍時也不會溢位。</p>
{d.quiz('bin-stop')}
'''


def size_cast():
    d = _h()
    demo = d.card('size_t 減 1 會繞回最大值', RUN['size_cast'], kind='run', stdout=OUT['size_cast'], show_out=True,
                  note='第一行是 64 位元系統上 <code>size_t</code> 的最大值 $2^{64} - 1$；第二行先轉成 <code>int</code>，才得到 -1。')
    return f'''<h3>為什麼寫 <code>static_cast&lt;int&gt;(aList.size()) - 1</code></h3>
<p><code>size()</code> 回傳的型別是 <code>size_t</code>，一種<strong>無號</strong>（unsigned）整數，不能表示負數。空的 vector 算 <code>aList.size() - 1</code> 時，<code>0 - 1</code> 在無號整數裡會繞回最大值，而不是 -1。標頭裡的 <code>binarySearch</code> 和 <code>binarySearchRec</code> 都先把大小轉成 <code>int</code> 再減 1，空 vector 就得到 <code>last = -1</code>，<code>first &gt; last</code>，馬上回傳 false。</p>
<p>不轉型、直接把 <code>aList.size() - 1</code> 存進 <code>int</code>，在常見的電腦上碰巧也會得到 -1；但那是把超出 <code>int</code> 範圍的值塞進 <code>int</code>，C++20 以前的結果由編譯器決定，不該依賴。先轉型再減，意圖清楚，前提是 vector 的長度不超過 <code>int</code> 能表示的範圍，本課程的例子都符合。</p>
{d.fold('實際印出來看', demo)}
'''


# ---------------------------------------------------------------- hashing
def hash_design():
    d = _h()
    body = ('<p>把 key 寫成 $k = aB + b$，$b$ 是低位的部分、$a$ 是高位的部分（例如 $B = 100$）。平方之後</p>'
            '<p>$$k^2 = a^2B^2 + 2abB + b^2$$</p>'
            '<p>中間的 $2abB$ 同時受高位與低位影響，平方結果中段的數字因此混進了整個 key 的資訊。反過來，平方的最後幾位只由 key 的最後幾位決定'
            '（$k^2 \\bmod 100$ 只看 $k \\bmod 100$），前面幾位主要反映 key 有多大，所以傳統上取中間。例如 $1234^2 = 1522756$，取中間三位得 227。'
            '這只是設計上的直覺，不保證每組 key 都分得均勻。</p>')
    return f'''<p>折疊法和平方取中法的出發點相同：讓 key 的<strong>每一位數</strong>都影響雜湊值。只用 $h(k) = k \\bmod 100$ 時只看最後兩位，12345678 和 99345678 會落在同一格；折疊法把每一段加起來，前面的位數也參與計算。不過加法不管順序，<code>12|34|56|78</code> 和 <code>78|56|34|12</code> 的總和相同，一定碰撞。平方取中法用乘法把各位數混在一起，再取高位與低位共同影響的中間幾位。兩種方法都不保證分布均勻，效果仍要看實際的 key。</p>
{d.fold('為什麼平方之後要取中間', body)}
'''


PROBE_TOOL = '''<div class="pc-tool" id="pcTool">
  <div class="pc-title">探查週期：從 slot 0 出發，每次跳 skip 格</div>
  <div class="input-row"><label>表的大小 m：</label>
    <button class="preset-btn" data-pc-m="10">10</button>
    <button class="preset-btn" data-pc-m="11">11</button>
    <button class="preset-btn active" data-pc-m="12">12</button>
  </div>
  <div class="input-row"><label>skip：</label>
    <button class="preset-btn" data-pc-s="1">1</button>
    <button class="preset-btn" data-pc-s="2">2</button>
    <button class="preset-btn active" data-pc-s="3">3</button>
    <button class="preset-btn" data-pc-s="4">4</button>
  </div>
  <div class="pc-slots" id="pcSlots"></div>
  <p class="pc-seq" id="pcSeq"></p>
  <p class="pc-stat" id="pcStat" aria-live="polite"></p>
</div>
<script>
(function () {
  var tool = document.getElementById('pcTool');
  if (!tool) return;
  var m = 12, s = 3;
  function gcd(a, b) { return b === 0 ? a : gcd(b, a % b); }
  function render() {
    var seq = [], p = 0;
    do { seq.push(p); p = (p + s) % m; } while (p !== 0);
    var g = gcd(m, s), slots = document.getElementById('pcSlots');
    slots.innerHTML = '';
    for (var i = 0; i < m; i++) {
      var k = seq.indexOf(i), cell = document.createElement('div');
      cell.className = 'pc-slot' + (k >= 0 ? ' pc-hit' : '');
      cell.innerHTML = '<span class="pc-idx">' + i + '</span><span class="pc-ord">' + (k >= 0 ? '第 ' + (k + 1) + ' 次' : '走不到') + '</span>';
      slots.appendChild(cell);
    }
    document.getElementById('pcSeq').textContent = '探查順序：' + seq.join(' → ') + ' → 回到 0';
    document.getElementById('pcStat').textContent = 'gcd(' + s + ', ' + m + ') = ' + g + '，走得到 ' + (m / g) + ' / ' + m + ' 格'
      + (g === 1 ? '：整張表都走得到。' : '：有 ' + (m - m / g) + ' 格永遠試不到。');
  }
  tool.querySelectorAll('[data-pc-m], [data-pc-s]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var attr = btn.hasAttribute('data-pc-m') ? 'data-pc-m' : 'data-pc-s';
      tool.querySelectorAll('[' + attr + ']').forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      if (attr === 'data-pc-m') m = +btn.getAttribute(attr); else s = +btn.getAttribute(attr);
      render();
    });
  });
  render();
})();
</script>'''


def gcd_block():
    d = _h()
    prog = d.card('印出幾組 m 與 skip 的探查週期', RUN['probe_cycle'], kind='run', stdout=OUT['probe_cycle'], show_out=True,
                  note='<code>gcd</code> 在 <code>&lt;numeric&gt;</code>（C++17）。m = 12、skip = 3 只走 4 格；m = 10、skip = 3 雖然 10 不是質數，仍然走得遍。')
    return f'''<p>碰撞後另找一個 slot 的過程統稱為<strong>重新雜湊</strong>（rehashing）。線性探查的重新雜湊函數是 $\\text{{rehash}}(pos) = (pos + skip) \\bmod size$。跳的格數必須讓表中每個 slot 最後都會被拜訪到，否則有一部分的表用不到。</p>
<h3>跳格要能走遍整張表：gcd 條件</h3>
<p>上式的 size 就是表的大小 $m$。從某一格出發、每次跳 $s$ 格（$s$ 就是 skip），會走過幾格？設 $g$ 是 $s$ 與 $m$ 的最大公因數（greatest common divisor，gcd）。從 0 出發時，每一步的位置都是 $g$ 的倍數，因為 $s$ 與 $m$ 都是 $g$ 的倍數，取餘數之後還是；0 到 $m - 1$ 之間 $g$ 的倍數只有 $\\dfrac{{m}}{{g}}$ 個，而它們剛好全部走得到。所以答案是 $\\dfrac{{m}}{{\\gcd(s, m)}}$ 格，接著回到起點重複。例如 $m = 12$、$s = 3$ 只走 0、3、6、9 四格；換成 $m = 11$ 就能走完全部 11 格。所以真正的條件是 <strong>$s$ 和 $m$ 互質</strong>，也就是 $\\gcd(s, m) = 1$。按下面的按鈕換幾組數字試試：</p>
{PROBE_TOOL}
<p>講義建議表的大小用<strong>質數</strong>，理由就在這裡：$m$ 是質數時，1 到 $m - 1$ 的任何跳格數都和 $m$ 互質，怎麼跳都走得遍。質數不是必要條件：$m = 10$、$s = 3$ 也互質，一樣走得遍；線性探查每次只跳 1 格，任何大小都沒問題。</p>
<p>至於餘數法本身，取質數只是經驗法則。兩個 key 碰撞的條件是 $k_1 \\bmod m = k_2 \\bmod m$，也就是 $m$ 整除 $k_1 - k_2$；不論 $m$ 是不是質數，這個條件都可能成立，質數不能保證不碰撞。key 都是 10 的倍數（10, 20, 30, …）時，$m = 10$ 讓它們全擠在 slot 0，$m = 11$ 就分散開來；反過來，11, 22, 33, 44 對 $m = 11$ 全部碰撞，對 $m = 10$ 卻分別落在 1、2、3、4。選質數只是降低「key 的規律剛好和 $m$ 有公因數」的機會。</p>
{d.fold('程式：印出探查週期', prog)}
{d.quiz('probe-cycle')}
{d.quiz('prime')}
'''


def plus3_note():
    d = _h()
    body = ('<p>沿著「每次加 3」的順序把 slot 重新排一排：0, 3, 6, 9, 1, 4, 7, 10, 2, 5, 8。在這個新順序裡，加 3 探查就是「往下一格」，'
            '和線性探查一模一樣。線性探查會連成一串的情形，加 3 探查一樣會發生，只是這一串在原本的表上看起來是分散的。</p>')
    return ('<p>跳格讓碰撞的元素在表裡的位置比較分散，但沒有根本解決群聚：每個 key 走的都是同一套「每次加 3」的路線，'
            '沿著這條路線，被佔用的 slot 一樣會連成一串，後來的 key 一樣要走過整串。</p>\n'
            + d.fold('為什麼加 3 探查仍然會群聚', body) + '\n')


def quad_note():
    d = _h()
    return f'''<p>平方探查跳的距離越來越大，雜湊值不同的 key 很快就分開，不容易像線性探查那樣連成一長串。代價有兩個。第一，<strong>雜湊值相同的 key 仍然走完全相同的路線</strong>：44 和 55 都從 0 出發，都依序試 1、4、9……，這稱為次要群聚（secondary clustering），前面線性探查的群聚則稱為主要群聚（primary clustering）。第二，<strong>平方探查不一定走得遍整張表</strong>：$m$ 是奇質數時，一個 key 的探查序列只會碰到 $\\frac{{m+1}}{{2}}$ 個不同的 slot。$m = 11$、從 slot 2 出發，依序是 2, 3, 6, 0, 7, 5，接著 5, 7, 0, 6, 3 重複。原因是 $i^2$ 和 $(m - i)^2$ 除以 $m$ 的餘數相同，後半段只是把前半段的位置倒著再走一次。這 $\\frac{{m+1}}{{2}}$ 個位置彼此不同，所以插入前表裡的元素不超過一半時，它們至少有一格是空的，一定找得到空位：11 格的表只放了 5 個以下，6 個候選位置不可能全被佔住；表本身仍然可以放超過一半，講義的九個數就放進了 11 格。</p>
{d.quiz('quad')}
'''


def open_vs_chain():
    d = _h()
    cmp = d.table(['', '開放定址（線性、跳格、平方探查）', '鏈結法'], [
        ['碰撞的元素放哪裡', '表裡另一個空的 slot', '同一個 slot 的鏈上'],
        ['負載因子 $\\lambda$', '最多是 1，表滿就放不下', '可以超過 1'],
        ['搜尋時看哪些元素', '沿著探查序列，直到找到、碰到空槽或繞回起點', '只看自己那條鏈'],
        ['額外空間', '不需要', '每個元素多一個鏈結節點'],
        ['$\\lambda$ 變大時', '比較次數急遽上升', '大約隨 $\\lambda$ 線性增加'],
    ])
    dh_rows = d.table(['key', '$h_1(k) = k \\bmod 11$', '$h_2(k) = 1 + (k \\bmod 7)$', '依序試的 slot', '放在'], [
        ['22', '0', '2', '0', '0'],
        ['33', '0', '6', '0 → 6', '6'],
        ['44', '0', '3', '0 → 3', '3'],
    ])
    prog = d.card('雙重雜湊放入 22、33、44', RUN['double_hash'], kind='run', stdout=OUT['double_hash'], show_out=True,
                  note='三個 key 的 $h_1$ 都是 0，但跳的格數不同，各走各的路線。用線性探查的話，它們會擠在 0、1、2。')
    body = f'''<h4>雙重雜湊（double hashing）</h4>
<p>線性探查與平方探查的路線只由起點決定，雜湊值相同的 key 就走同一條路。雙重雜湊再用第二個雜湊函數 $h_2$ 決定<strong>每個 key 自己的跳格數</strong>：</p>
<p>$$h(k, i) = \\big(h_1(k) + i \\cdot h_2(k)\\big) \\bmod m, \\quad i = 0, 1, 2, \\ldots$$</p>
<p>以 $m = 11$、$h_2(k) = 1 + (k \\bmod 7)$ 依序放入 22、33、44：</p>
{dh_rows}
{prog}
<p>$h_2(k)$ 不可以是 0，而且要和 $m$ 互質，探查序列才走得遍整張表；這就是前面的 gcd 條件。$m$ 是質數、$1 \\le h_2(k) &lt; m$ 時自動成立。</p>
<h4>開放定址的刪除</h4>
<p>開放定址不能直接把要刪的格子清空。用講義的表為例：55 從 slot 0 探查到 2，如果刪掉 slot 1 的 44 並清成空槽，再找 55 時會在 slot 1 碰到空槽就停下，誤判 55 不在。常見的做法是改放「已刪除」的記號（tombstone）：搜尋時跳過它繼續找，插入時可以重新使用這一格。鏈結法只要把元素從鏈上拿掉。</p>
<h4>名稱容易混淆</h4>
<p>開放定址也叫 closed hashing（元素一定待在表內）；鏈結法也叫 separate chaining、open hashing 或 closed addressing。Open addressing 和 open hashing 指的是相反的兩種做法，本章統一用「開放定址」與「鏈結法」。</p>
'''
    return f'''<h3>開放定址與鏈結法的比較</h3>
{cmp}
<p>雜湊函數分布良好、$\\lambda$ 控制得當時，兩種方法的搜尋都是平均 $O(1)$。本章下一小節的 <code>HashTable</code> 用開放定址；<code>std::unordered_map</code> 常見的實作用鏈結法。</p>
{d.quiz('open-chain')}
{d.fold('雙重雜湊、刪除與名稱', body)}
'''


def sort_by_structure():
    return ('<p>第 9 章還會看到兩種靠資料結構完成的排序：堆積排序（heap sort）反覆從堆積取出最大（或最小）的值；'
            '樹排序（tree sort）把資料放進二元搜尋樹，再用中序走訪依序讀出來。</p>')
