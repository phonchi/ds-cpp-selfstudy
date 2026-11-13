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
    why = d.ul([
        '<strong>已排序的 vector 找最小值</strong>：最小的就在索引 0，看一格就好，$O(1)$。',
        '<strong>已排序的 vector 列出 $[a, b]$ 之間的值</strong>：先用二分搜尋找到第一個不小於 $a$ 的位置（標準函式庫的 <code>lower_bound</code> 就是做這件事），最多比 $\\lfloor \\log_2 n \\rfloor + 1$ 次。'
        '接著從那裡往後一個一個看：看到的值不大於 $b$ 就印出來，這種情況剛好發生 $k$ 次；第一次看到大於 $b$ 的值就停，最多再多看 1 個。'
        '總共最多 $(\\lfloor \\log_2 n \\rfloor + 1) + (k + 1)$ 次比較，也就是 $O(\\log n + k)$。答案本身有 $k$ 筆，任何方法至少都要花 $k$ 步把它們列出來，所以 $k$ 這一項省不掉。',
        '<strong>平衡的二元搜尋樹</strong>：樹高約 $\\log_2 n$。找最小值是從根一路往左走到底，$O(\\log n)$。列出範圍時，從根往下找 $a$ 與 $b$ 的兩條路徑，每條最多經過樹高那麼多個節點；'
        '比 $a$ 小或比 $b$ 大的子樹整棵跳過，範圍內的 $k$ 個節點各拜訪一次，所以是 $O(\\log n + k)$。',
        '<strong>最小堆積</strong>：只規定父節點不大於子節點，所以最小值一定在根，$O(1)$。兄弟之間、不同分支之間沒有大小關係，找某個值或列出範圍都可能要看遍 $n$ 個元素，$O(n)$。',
        '<strong>雜湊表</strong>：假設表的大小 $m$ 和 $n$ 同一個量級、負載因子控制得當、雜湊函數分布良好，而且算一次雜湊值、比一次 key 都是 $O(1)$（例如整數 key）。位置由雜湊值決定，和大小無關，相鄰的值（例如 20 和 21）可能放在表的兩端，所以找最小值、列範圍都得把整張表看一遍，$O(m) = O(n)$；只有「在不在」能直接算出位置，平均 $O(1)$。',
    ])
    fold_body = ('<p>沒有一種存法在每種操作上都最快。下表比較幾種存法處理 $n$ 筆資料時的三種問題，$k$ 是範圍內的筆數：</p>'
                 + full + '<h4>這些次數怎麼來的</h4>' + why +
                 '<p>第 9 章會正式介紹二元搜尋樹（Binary Search Tree，BST）與堆積（heap）。要選哪一種存法，看最常做的是哪一種操作。</p>')
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
                  note='第一行是 64 位元系統上 <code>size_t</code> 的最大值 $2^{64} - 1$；第二行先轉成 <code>int</code>，才得到 -1。把超出範圍的無號值直接存進 <code>int</code>，C++20 以前的結果由編譯器決定，C++20 起才規定成取模的結果。')
    return f'''<h3>為什麼寫 <code>static_cast&lt;int&gt;(aList.size()) - 1</code></h3>
<p><code>size()</code> 回傳的型別是 <code>size_t</code>，一種<strong>無號</strong>（unsigned）整數，不能表示負數。空的 vector 算 <code>aList.size() - 1</code> 時，<code>0 - 1</code> 在無號整數裡會繞回最大值，而不是 -1。標頭裡的 <code>binarySearch</code> 和 <code>binarySearchRec</code> 都先把大小轉成 <code>int</code> 再減 1，空 vector 就得到 <code>last = -1</code>，<code>first &gt; last</code>，馬上回傳 false。</p>
<p>不轉型、直接把 <code>aList.size() - 1</code> 存進 <code>int</code>，在常見的電腦上碰巧也會得到 -1；但那是把超出 <code>int</code> 範圍的值塞進 <code>int</code>，不該依賴。先轉型再減，意圖清楚，前提是 vector 的長度不超過 <code>int</code> 能表示的範圍，本課程的例子都符合。</p>
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
    return f'''<p>折疊法和平方取中法的出發點相同：讓 key 的<strong>每一位數</strong>都影響雜湊值。實際的 key 常有規律，只看最後幾位很容易撞在一起。例如商品售價常訂成 199、299、399、1299 元，用 $h(k) = k \\bmod 100$ 只看最後兩位，四個全落在 99 這一格；每 60 秒記一筆的時間戳記（從 1970 年起算的秒數）1763000000、1763000060、1763000120……，最後兩位只會輪流出現 00、60、20、80、40，100 格只用到 5 格。</p>
<p>折疊法把每兩位一段加起來，前面的位數也參與計算：199 切成 1|99，和是 100；299、399、1299 的和是 101、102、111，再對 100 取餘數，四個售價就分到 0、1、2、11 四格。不過加法不管順序：日期寫成「月日」四位數時，3 月 12 日（03|12）和 12 月 3 日（12|03）的和都是 15，一定碰撞。平方取中法用乘法把各位數混在一起，再取中間幾位：$199^2 = 39601$，補成偶數位 039601 後中間兩位是 96；299、399、1299 依序得到 94、92、87，同樣分開了。兩種方法都不保證分布均勻，效果仍要看實際的 key。</p>
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
    body = f'''<p>上式的 size 就是表的大小 $m$。從某一格出發、每次跳 $s$ 格（$s$ 就是 skip），會走過幾格？設 $g$ 是 $s$ 與 $m$ 的最大公因數（greatest common divisor，gcd）。從 0 出發時，每一步的位置都是 $g$ 的倍數，因為 $s$ 與 $m$ 都是 $g$ 的倍數，取餘數之後還是；0 到 $m - 1$ 之間 $g$ 的倍數只有 $\\dfrac{{m}}{{g}}$ 個。它們也全部走得到：寫成 $s = gs'$、$m = gm'$，這時 $s'$ 與 $m'$ 互質。從 0 出發走 $t$ 步回到 0，表示 $m$ 整除 $ts$，也就是 $m'$ 整除 $ts'$；因為 $s'$ 與 $m'$ 互質，只能是 $m'$ 整除 $t$。所以最少要走 $m' = \\dfrac{{m}}{{g}}$ 步才回到起點，而且這之前不會走到重複的格子（重複就表示更早回到同一格），$\\dfrac{{m}}{{g}}$ 步剛好走過那 $\\dfrac{{m}}{{g}}$ 個 $g$ 的倍數。所以答案是 $\\dfrac{{m}}{{\\gcd(s, m)}}$ 格，接著回到起點重複；真正的條件是 <strong>$s$ 和 $m$ 互質</strong>，也就是 $\\gcd(s, m) = 1$。按下面的按鈕換幾組數字試試：</p>
{PROBE_TOOL}
<p>講義建議表的大小用質數，理由就在這裡：$m$ 是質數時，1 到 $m - 1$ 的任何跳格數都和 $m$ 互質，怎麼跳都走得遍。質數不是必要條件：$m = 10$、$s = 3$ 也互質，一樣走得遍；線性探查每次只跳 1 格，任何大小都沒問題。</p>
<p>至於餘數法本身，取質數只是經驗法則。兩個 key 碰撞的條件是 $k_1 \\bmod m = k_2 \\bmod m$，也就是 $m$ 整除 $k_1 - k_2$；不論 $m$ 是不是質數，這個條件都可能成立，質數不能保證不碰撞。key 都是 10 的倍數（10, 20, 30, …）時，$m = 10$ 讓它們全擠在 slot 0，$m = 11$ 就分散開來；反過來，11, 22, 33, 44 對 $m = 11$ 全部碰撞，對 $m = 10$ 卻分別落在 1、2、3、4。選質數只是降低「key 的規律剛好和 $m$ 有公因數」的機會。</p>
{prog}
{d.quiz('probe-cycle')}
{d.quiz('prime')}
'''
    return f'''<p>碰撞後另找一個 slot 的過程統稱為<strong>重新雜湊</strong>（rehashing）。線性探查的重新雜湊函數是 $\\text{{rehash}}(pos) = (pos + skip) \\bmod size$。跳的格數必須讓表中每個 slot 最後都會被拜訪到，否則有一部分的表用不到；所以表的大小通常建議用<strong>質數</strong>。例如表有 12 格、每次跳 3 格，從 slot 0 出發只會試 0、3、6、9，其他 8 格永遠用不到；表改成 11 格，同樣每次跳 3 格就能走遍全部 11 格。</p>
{d.fold('為什麼質數走得遍：gcd 條件與探查週期', body)}
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
    body = f'''<p><strong>雜湊值相同的 key 仍然走同一條路線</strong>：44 和 55 都從 0 出發，都依序試 1、4、9……，這稱為次要群聚（secondary clustering）；前面線性探查的群聚則稱為主要群聚（primary clustering）。</p>
<p><strong>平方探查不一定走得遍整張表</strong>：表有 11 格、從 slot 2 出發，依序試 2, 3, 6, 0, 7, 5，接著 5, 7, 0, 6, 3 重複，11 格裡只碰得到 6 格。下面推導一般的情形。</p>
<p>設 $m$ 是奇質數，第 $i$ 次探查的位置是 $(h + i^2) \\bmod m$。起點 $h$ 對每一次都一樣，所以兩次探查落在同一格，等於 $i^2 \\equiv j^2 \\pmod m$，也就是 $m$ 整除 $i^2 - j^2 = (i - j)(i + j)$。</p>
<p>質數整除一個乘積，就一定整除其中一個因數，所以 $m \\mid (i - j)$ 或 $m \\mid (i + j)$。只看 $0 \\le i, j \\le m - 1$ 的情形：前者表示 $i = j$；後者表示 $i + j = m$，或 $i = j = 0$。所以第 $i$ 次和第 $m - i$ 次落在同一格，其他任兩次都落在不同的格子。</p>
<p>因此 $i = 0, 1, \\ldots, \\frac{{m-1}}{{2}}$ 這 $\\frac{{m+1}}{{2}}$ 次探查各落在不同的格子；$i = \\frac{{m+1}}{{2}}, \\ldots, m - 1$ 分別和第 $m - i$ 次同一格，只是把前半段倒著再走一遍。$i \\ge m$ 時，$i^2 \\bmod m$ 和 $(i \\bmod m)^2 \\bmod m$ 相同，也不會出現新位置。所以一個 key 最多碰到 $\\frac{{m+1}}{{2}}$ 個不同的 slot。$m = 11$ 時是 6 個：$i = 0$ 到 5 的 $i^2 \\bmod 11$ 依序是 0, 1, 4, 9, 5, 3。</p>
<p>反過來，插入前表裡最多只放了 $\\frac{{m-1}}{{2}}$ 個元素（負載因子不到一半）時，這 $\\frac{{m+1}}{{2}}$ 個彼此不同的候選位置不可能全被佔住，一定找得到空位：11 格的表只放了 5 個以下，6 個候選位置至少有一格是空的。這只是保證；表本身仍然可以放超過一半，講義的九個數就放進了 11 格，只是之後的 key 有可能找不到空位。</p>
{d.quiz('quad')}
'''
    return f'''<p>平方探查跳的距離越來越大，雜湊值不同的 key 很快就分開，不容易像線性探查那樣連成一長串。</p>
{d.fold('平方探查的兩個限制與推導', body)}
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
<p>開放定址也叫 closed hashing（元素一定待在表內）；鏈結法也叫 separate chaining、open hashing 或 closed addressing。Open addressing 和 open hashing 指的是相反的兩種做法，本章統一用「開放定址」與「鏈結法」。標準函式庫的 <code>std::unordered_map</code> 常見的實作用鏈結法。</p>
'''
    return f'''<h3>開放定址與鏈結法的比較</h3>
{cmp}
<p>雜湊函數分布良好、$\\lambda$ 控制得當時，兩種方法的搜尋都是平均 $O(1)$。本章下一小節的 <code>HashTable</code> 用開放定址。</p>
{d.quiz('open-chain')}
{d.fold('雙重雜湊、刪除與名稱', body)}
'''


def load_analysis():
    d = _h()
    formulas = d.table(['', '成功搜尋', '失敗搜尋'], [
        ['線性探查（探查的 slot 數）', '$\\approx \\frac{1}{2}\\left(1 + \\frac{1}{1-\\lambda}\\right)$', '$\\approx \\frac{1}{2}\\left(1 + \\frac{1}{(1-\\lambda)^2}\\right)$'],
        ['鏈結法（和 key 比較的次數）', '$\\approx 1 + \\frac{\\lambda}{2}$', '$\\approx \\lambda$'],
    ])
    body = f'''<p><strong>假設</strong>：雜湊函數把每個 key 平均、獨立地分到 $m$ 個 slot；表中已有 $n$ 個元素，負載因子 $\\lambda = n/m$（開放定址時 $0 \\le \\lambda &lt; 1$）；成功搜尋時要找的是表中每個 key 的機率相同；中間沒有刪除。下表的數字是表很大時的近似值：</p>
{formulas}
<p>兩列計的單位不同。線性探查計的是看了幾個 slot，失敗搜尋要把最後碰到的空槽也算進去；鏈結法計的是和鏈上幾個 key 比過。</p>
<h4>鏈結法</h4>
<p><strong>失敗搜尋</strong>：要找的 key 不在表中，得把它那個 slot 的整條鏈看完。$n$ 個元素平均分到 $m$ 條鏈，每條平均有 $n/m = \\lambda$ 個元素，所以平均比較 $\\lambda$ 次。</p>
<p><strong>成功搜尋</strong>：新元素接在鏈的尾端。第 $t$ 個放進去的元素（$t = 1, \\ldots, n$）進去時，表裡已有 $t - 1$ 個元素，它那條鏈前面平均已有 $\\frac{{t-1}}{{m}}$ 個；找它時要先比過這些，再比它自己，共 $1 + \\frac{{t-1}}{{m}}$ 次。對 $n$ 個元素取平均：</p>
<p>$$\\frac{{1}}{{n}}\\sum_{{t=1}}^{{n}}\\left(1 + \\frac{{t-1}}{{m}}\\right) = 1 + \\frac{{n-1}}{{2m}} \\approx 1 + \\frac{{\\lambda}}{{2}}$$</p>
<h4>線性探查</h4>
<p><strong>失敗搜尋</strong>：先看一個簡化的模型，假設每次探查都像重新隨機挑一個 slot。表裡 $\\lambda$ 比例的 slot 被佔用，每次撞到已佔用 slot 的機率約是 $\\lambda$。失敗搜尋要一直探查到碰見空槽：第 1 次一定要探查，需要第 2 次的機率約是 $\\lambda$，需要第 3 次的機率約是 $\\lambda^2$……，平均約是</p>
<p>$$1 + \\lambda + \\lambda^2 + \\cdots = \\frac{{1}}{{1-\\lambda}}$$</p>
<p>線性探查比這個模型慢，因為群聚：佔用的 slot 連成一段一段，撞進一段就得走到段尾，而段越長越容易被撞上。把群聚算進去的精確分析是 Knuth 的結果（《The Art of Computer Programming》第 3 卷 6.4 節），得到失敗搜尋約 $\\frac{{1}}{{2}}\\left(1 + \\frac{{1}}{{(1-\\lambda)^2}}\\right)$ 次。這一條是<strong>引用的結果</strong>，推導要對所有可能的群聚長度做組合計數，這裡不展開；上面的簡化模型只說明了分母的 $1 - \\lambda$ 從哪裡來。$\\lambda = 0.5$ 時是 2.5 次，簡化模型是 2 次；$\\lambda = 0.9$ 時是 50.5 次，簡化模型只有 10 次。群聚在表快滿時影響最大。</p>
<p><strong>成功搜尋</strong>可以從失敗搜尋推出來。找某個 key 時走的探查路線，和當初插入它時一模一樣；插入時探查的次數，就是「當時」做一次失敗搜尋的次數。設 $U(x)$ 是負載因子為 $x$ 時失敗搜尋的平均次數。元素是在負載因子從 0 慢慢長到 $\\lambda$ 的過程中一個一個放進去的，對所有元素平均，就是把 $U$ 在 $0, \\frac{{1}}{{m}}, \\ldots, \\frac{{n-1}}{{m}}$ 取平均；表很大時，這個平均約等於積分：</p>
<p>$$S(\\lambda) \\approx \\frac{{1}}{{\\lambda}}\\int_0^{{\\lambda}} U(x)\\,dx = \\frac{{1}}{{\\lambda}}\\int_0^{{\\lambda}} \\frac{{1}}{{2}}\\left(1 + \\frac{{1}}{{(1-x)^2}}\\right) dx = \\frac{{1}}{{2}}\\left(1 + \\frac{{1}}{{1-\\lambda}}\\right)$$</p>
<p>中間用到 $\\int_0^{{\\lambda}} \\frac{{dx}}{{(1-x)^2}} = \\frac{{1}}{{1-\\lambda}} - 1 = \\frac{{\\lambda}}{{1-\\lambda}}$。鏈結法的成功搜尋也能這樣算：插入時那條鏈的長度就是當時失敗搜尋的比較次數 $x$，找它要再多比自己一次，$1 + \\frac{{1}}{{\\lambda}}\\int_0^{{\\lambda}} x\\,dx = 1 + \\frac{{\\lambda}}{{2}}$，和上面的加總 $1 + \\frac{{n-1}}{{2m}}$ 只差 $\\frac{{1}}{{2m}}$，表很大時可以忽略。</p>
'''
    return ('<p>負載因子 $\\lambda$ 越大，碰撞越多，平均要比較的次數也越多。線性探查在 $\\lambda$ 接近 1 時會急遽變慢；'
            '鏈結法的比較次數大約只隨 $\\lambda$ 線性增加，比較穩定。</p>\n'
            + d.fold('平均比較次數的公式與推導', body) + '\n')


def seq_ordered_proof():
    d = _h()
    body = ('<p>假設元素互不相同，要找的值也不等於其中任何一個。$n$ 個元素把數線切成 $n + 1$ 個空隙，再假設要找的值落在每個空隙的機率相同。</p>'
            '<p>落在第 1 個元素之前：比第 1 個就發現它比目標大，停下，1 次。落在第 $i$ 個與第 $i + 1$ 個之間：要比到第 $i + 1$ 個才停，$i + 1$ 次。比全部都大：比完 $n$ 個，$n$ 次。平均是</p>'
            '<p>$$\\frac{1 + 2 + \\cdots + n + n}{n + 1} = \\frac{\\frac{n(n+1)}{2} + n}{n + 1} = \\frac{n}{2} + \\frac{n}{n+1} \\approx \\frac{n}{2}$$</p>'
            '<p>例如 $n = 10$ 時是 $\\frac{65}{11} \\approx 5.9$ 次。值在 list 裡、而且在每個位置的機率相同時，第 $i$ 個找到要比 $i$ 次，平均 $\\frac{1 + 2 + \\cdots + n}{n} = \\frac{n+1}{2}$，有序與否都一樣。表中的 $\\frac{n}{2}$ 是 $n$ 很大時的近似。</p>')
    return d.fold('有序版找不到時平均約 n/2 是怎麼算的', body) + '\n'


def selection_count():
    d = _h()
    body = ('<p><code>fillSlot</code> 從 $n - 1$ 遞減到 1。每一輪拿索引 1 到 <code>fillSlot</code> 的元素和目前的最大值比較，一輪 <code>fillSlot</code> 次，加起來</p>'
            '<p>$$(n-1) + (n-2) + \\cdots + 1 = \\frac{n(n-1)}{2}$$</p>'
            '<p>和氣泡排序一樣，而且不論資料原本怎麼排都是這麼多次。交換則每輪最多 1 次，總共最多 $n - 1$ 次；氣泡排序最差要交換 $\\frac{n(n-1)}{2}$ 次（完全反序時每次比較都交換）。</p>')
    return d.fold('比較與交換次數的計算', body) + '\n'


def insertion_count():
    d = _h()
    body = ('<p>處理位置 $i$ 的元素時（$i = 1, \\ldots, n-1$），它最多往回比 $i$ 次。</p>'
            '<p><strong>最佳</strong>：資料已排序，每個元素只和左邊一個比一次就停，共 $n - 1$ 次，$O(n)$。</p>'
            '<p><strong>最差</strong>：資料完全反序，每個元素都要一路比到開頭，共 $1 + 2 + \\cdots + (n-1) = \\frac{n(n-1)}{2}$ 次，$O(n^2)$。</p>'
            '<p><strong>平均</strong>：假設元素互不相同，而且每一種排列出現的機率相同。一對位置 $p &lt; q$ 如果 <code>a[p] &gt; a[q]</code>，稱為一個<strong>逆序對</strong>。插入排序每做一次移動，剛好消掉一個逆序對（較大的元素和被插入的元素換了先後），所以總移動次數就是逆序對的個數。'
            '任一對位置是逆序的機率是 $\\frac{1}{2}$，共有 $\\frac{n(n-1)}{2}$ 對，平均就有 $\\frac{n(n-1)}{4}$ 個逆序對。'
            '比較次數等於移動次數，再加上每一輪最後一次「不用移」的比較（最多 $n - 1$ 次），所以平均約 $\\frac{n^2}{4}$ 次，仍然是 $O(n^2)$，大約是最差情況的一半。有重複元素時就不能直接套這個平均，例如全部相等時只要 $n - 1$ 次。</p>')
    return d.fold('最佳、最差與平均比較次數', body) + '\n'


def shell_bounds():
    d = _h()
    body = ('<p><strong>最佳：$O(n\\log n)$</strong>。資料已排序時，增量 $g$ 那一輪的每個元素只和前一個同組元素比一次，共 $n - g$ 次。取 $n = 2^p$，增量 $n/2, n/4, \\ldots, 1$ 共 $p = \\log_2 n$ 輪，總共 $p\\,n - (n/2 + n/4 + \\cdots + 1) = n\\log_2 n - (n - 1)$ 次。</p>'
            '<p><strong>本章的折半增量，最差是 $\\Theta(n^2)$</strong>。上界：增量 $g$ 的那一輪有 $g$ 個子清單，每個長約 $n/g$，各做一次插入排序最多 $\\frac{1}{2}(n/g)^2$ 次，這一輪最多 $\\frac{n^2}{2g}$ 次。'
            '各輪的 $\\frac{1}{g}$ 加起來是 $1 + \\frac{1}{2} + \\frac{1}{4} + \\cdots + \\frac{2}{n} &lt; 2$，所以總共不超過 $n^2$ 次，$O(n^2)$。</p>'
            '<p>下界：取 $n = 2^p$，除了最後的 1，增量都是偶數。增量是偶數時，同一個子清單裡的位置奇偶相同，所以奇數位置的元素和偶數位置的元素在最後一輪之前從來沒有比過。'
            '如果一開始把最小的 $n/2$ 個數放在奇數位置、最大的 $n/2$ 個數放在偶數位置，前面幾輪都不會把兩群混在一起；最後一輪的插入排序，第 $j$ 小的數得越過排在它前面、比它大的 $j$ 個數。'
            '總移動次數是 $1 + 2 + \\cdots + \\frac{n}{2} \\approx \\frac{n^2}{8}$，也是 $n^2$ 的量級。實際排 1024 個數，移動 131328 次，正好是 $\\frac{512 \\times 513}{2}$。'
            '這也說明正文「最後一輪時資料通常已經接近排好」只是常見的情形，不是保證。</p>'
            '<p><strong>增量 $2^k - 1$ 的 $O(n^{3/2})$</strong>（Papernov 與 Stasevich，1965）。推導要用兩個事實：</p>'
            + d.ul(['先做過 $k$ 排序（相隔 $k$ 的元素都排好）再做 $h$ 排序，結果仍然是 $k$ 排序的。這是已知的定理，這裡不證明。',
                    '若 $a$、$b$ 互質，任何不小於 $(a-1)(b-1)$ 的整數都能寫成 $xa + yb$（$x, y \\ge 0$）。所以一個同時是 $a$ 排序與 $b$ 排序的陣列裡，相隔至少 $(a-1)(b-1)$ 的兩個元素一定已經排好順序：從前一個沿著若干步 $a$、若干步 $b$ 走到後一個，每一步都不會變小。'])
            + '<p>增量 $2^k - 1$ 中相鄰的兩個互質，而且 $h_{k+1} \\approx 2h_k$、$h_{k+2} \\approx 4h_k$。做增量 $h_k$ 那一輪時，陣列已經是 $h_{k+1}$ 與 $h_{k+2}$ 排序的，'
              '所以每個元素在自己的子清單裡最多往回移動約 $\\frac{h_{k+1}h_{k+2}}{h_k} \\approx 8h_k$ 步，這一輪是 $O(n h_k)$。增量大於 $\\sqrt{n}$ 的各輪改用上面的 $\\frac{n^2}{2g}$；'
              '兩部分各是一個等比級數，最大項都是 $n\\sqrt{n}$ 的量級，所以總共 $O(n^{3/2})$。細節見 Knuth《The Art of Computer Programming》第 3 卷 5.2.1 節。</p>')
    return d.fold('最佳情況、最差情況與增量的影響', body) + '\n'


def merge_bound():
    d = _h()
    body = ('<p><strong>寫回次數</strong>：每一層的合併把該層所有元素各寫回一次。設排 $n$ 個元素要寫回 $W(n)$ 次，則 $W(n) = 2W(n/2) + n$，$W(1) = 0$。取 $n = 2^p$ 一直展開：</p>'
            '<p>$$W(n) = 2W\\!\\left(\\tfrac{n}{2}\\right) + n = 4W\\!\\left(\\tfrac{n}{4}\\right) + 2n = \\cdots = 2^p\\,W(1) + p\\,n = n\\log_2 n$$</p>'
            '<p><strong>比較次數</strong>：合併兩個合計 $k$ 個元素的已排序 list，每比一次就寫回一個元素，最後一個元素不必再比，所以最多 $k - 1$ 次。'
            '最差的比較次數 $C(n)$ 滿足 $C(n) = 2C(n/2) + n - 1$，同樣展開得 $C(n) = n\\log_2 n - n + 1$，也是 $O(n\\log n)$。'
            '本章動畫排 [1, 2, 3, 4] 時只比了 4 次，因為一邊先用完時就不必再比，最佳情況比這個少。</p>'
            '<p><strong>額外空間為什麼是 $O(n)$，不是 $O(n\\log n)$</strong>：暫存的左右兩半在該層合併完就釋放。同一時間還存在的，只有目前這條遞迴路徑上各層的暫存，大小約 $n, \\frac{n}{2}, \\frac{n}{4}, \\ldots$，加起來小於 $2n$。</p>'
            '<p><strong>為什麼 $n\\log n$ 已經是極限</strong>：只靠比較的排序，可以畫成一棵決策樹，每個節點是一次「$a$ 和 $b$ 誰大」的比較，有兩個分支。'
            '$n$ 個不同的數有 $n!$ 種排列，每一種都要走到不同的葉子，演算法才知道該怎麼排，所以葉子至少有 $n!$ 片。比較 $h$ 次的樹最多 $2^h$ 片葉子，因此最差情況的比較次數 $h$ 滿足</p>'
            '<p>$$2^h \\ge n! \\quad\\Longrightarrow\\quad h \\ge \\log_2 (n!) \\ge \\log_2 \\left(\\tfrac{n}{2}\\right)^{n/2} = \\tfrac{n}{2}\\log_2 \\tfrac{n}{2}$$</p>'
            '<p>中間用到 $n!$ 裡至少有 $\\frac{n}{2}$ 個因數不小於 $\\frac{n}{2}$。右邊是 $\\Omega(n\\log n)$：任何比較式排序在最差情況下都至少要這麼多次比較，合併排序已經達到這個量級。</p>')
    return d.fold('遞迴式、額外空間與比較式排序的下界', body) + '\n'


def quick_analysis():
    d = _h()
    body = ('<p><strong>最差</strong>：每次分割都分成 0 個與 $n - 1$ 個時，各層分割大約要比 $n - 1, n - 2, \\ldots, 1$ 次，總和 $\\frac{n(n-1)}{2}$，$O(n^2)$。'
            '本章用第一個元素當 pivot，資料原本就排好或完全反序時就是這種情況；所有元素都相等時也是，因為 <code>leftMark</code> 會一路往右走到底。</p>'
            '<p><strong>平均</strong>：用一個理想模型來算。假設元素互不相同、每種排列機率相同，所以 pivot 最後落在每個位置的機率都是 $\\frac{1}{n}$；再假設一次分割剛好比 $n - 1$ 次（每個其他元素和 pivot 比一次）。'
            '設 $C(n)$ 是平均比較次數，pivot 落在位置 $k$ 時左右兩段長 $k$ 與 $n - 1 - k$：</p>'
            '<p>$$C(n) = (n - 1) + \\frac{1}{n}\\sum_{k=0}^{n-1}\\big(C(k) + C(n-1-k)\\big) = (n - 1) + \\frac{2}{n}\\sum_{k=0}^{n-1} C(k)$$</p>'
            '<p>兩邊乘以 $n$，再減去把 $n$ 換成 $n - 1$ 的同一條式子，總和就消掉了：</p>'
            '<p>$$nC(n) - (n-1)C(n-1) = 2(n-1) + 2C(n-1) \\quad\\Longrightarrow\\quad \\frac{C(n)}{n+1} = \\frac{C(n-1)}{n} + \\frac{2(n-1)}{n(n+1)}$$</p>'
            '<p>右邊最後一項約是 $\\frac{2}{n}$，一路累加回 $C(1) = 0$，得到 $\\frac{C(n)}{n+1} \\approx 2\\left(\\frac{1}{2} + \\frac{1}{3} + \\cdots + \\frac{1}{n}\\right) \\approx 2\\ln n$，所以 $C(n) \\approx 2n\\ln n$，平均是 $O(n\\log n)$。</p>'
            '<p>本章的 <code>partition</code> 會把交換前後的元素再比一次，實際比較次數比 $n - 1$ 多一些（例如排 6 個數平均約 15 次，理想模型是 10.3 次）；但每次分割的比較次數仍然和段長成正比，所以量級一樣是 $O(n\\log n)$。</p>')
    return d.fold('最差與平均比較次數的推導', body) + '\n'


def bin_exact():
    d = _h()
    body = ('<p>設 $B(n)$ 是範圍裡有 $n$ 個元素時最多要比的次數，$B(0) = 0$。比一次中點之後，若沒找到，剩下的較大那一邊有 $\\lfloor n/2 \\rfloor$ 個元素'
            '（中點取 $\\lfloor (first + last)/2 \\rfloor$，左邊 $\\lfloor (n-1)/2 \\rfloor$ 個、右邊 $\\lfloor n/2 \\rfloor$ 個），所以 $B(n) = 1 + B(\\lfloor n/2 \\rfloor)$。</p>'
            '<p>設 $2^p \\le n &lt; 2^{p+1}$，也就是 $p = \\lfloor \\log_2 n \\rfloor$。$n$ 每次除以 2 取整數，要 $p$ 次才變成 1，再一次變成 0，所以 $B(n) = p + 1 = \\lfloor \\log_2 n \\rfloor + 1$。例如 $n = 10$：$10 \\to 5 \\to 2 \\to 1 \\to 0$，最多 4 次，前面找 50 的例子比了 3 次。</p>')
    return d.fold('最多比較次數為什麼是 ⌊log₂ n⌋ + 1', body) + '\n'


def sort_by_structure():
    return ('<p>第 9 章還會看到兩種靠資料結構完成的排序：堆積排序（heap sort）反覆從堆積取出最大（或最小）的值；'
            '樹排序（tree sort）把資料放進二元搜尋樹，再用中序走訪依序讀出來。</p>')
