"""Chapter 7 (searching_sorting.html) section bodies. Each value of sections() fills one <!-- gen:NAME --> block.

The hand-written part of every section (widgets, explanations) lives in search_legacy.py; it carries
{{slot:NAME}} tokens where the lecture material below is inserted. Lecture text and code follow
07_Searching and Sorting.ipynb and the course headers searching.hpp, hashtable.hpp and sorting.hpp.
Expected outputs come from compiling the programs (search_programs.OUT).
"""
import re
from html import escape
from enrich_lib import hl
from content.search_figures import figure
from content.search_programs import *  # noqa: F401,F403
from content.search_programs import OUT
from content.search_headers import HPP
from content.search_legacy import LEGACY
from content.search_quizzes import LECTURE_QUIZ


# ---------------------------------------------------------------- helpers (chapter 3/4/6 conventions)
def details(summary, body, cls='srch-detail', did=''):
    ident = f' id="{did}"' if did else ''
    return f'<details class="{cls}"{ident}><summary>{summary}</summary><div class="srch-detail-body">{body}</div></details>'


def fold(title, body, did=''):
    """Content that the lecture does not cover: collapsed and labelled （補充）."""
    return details(title + '（補充）', body, did=did)


def steps(title, fids, note=''):
    """Further frames of a step-by-step figure sequence, collapsed."""
    return details('逐步圖：' + title, (f'<p>{note}</p>' if note else '') + ''.join(figure(f) for f in fids))


def table(headers, rows):
    return ('<div class="table-scroll" tabindex="0" aria-label="表格，可左右捲動"><table class="cmp-table"><thead><tr>'
            + ''.join(f'<th>{h}</th>' for h in headers) + '</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{v}</td>' for v in r) + '</tr>' for r in rows)
            + '</tbody></table></div>')


def quiz(key, label='QUIZ'):
    """A lecture quiz in this page's sq-item markup (the page script binds every .sq-item)."""
    q = LECTURE_QUIZ[key]
    assert len(q['answers']) == 4 and sum(a['correct'] for a in q['answers']) == 1, key
    opts = '\n'.join(
        f'      <button class="sq-opt" data-c="{1 if a["correct"] else 0}" data-fb="{escape(a["feedback"], quote=True)}">'
        f'{escape(a["answer"], quote=False)}</button>' for a in q['answers'])
    return (f'<div class="sq-item srch-quiz" id="quiz-{key}">\n    <div class="sq-q"><span class="sq-num">{label}</span>'
            f'{escape(q["question"], quote=False)}</div>\n    <div class="sq-opts">\n{opts}\n    </div>\n'
            f'    <div class="sq-fb"></div>\n  </div>')


def _expected_attr(stdout):
    return ' data-expected="' + escape(stdout, quote=True).replace('\n', '&#10;') + '"'


def _expected_out(stdout, label='預期輸出'):
    return (f'<div class="expected-out"><span class="eo-tag">{label}</span><pre>'
            + escape(stdout.rstrip('\n')) + '</pre></div>')


def code(code_text, kind, stdout=None):
    attrs = f' data-cpp="{kind}"' + (_expected_attr(stdout) if kind == 'run' else '')
    return f'  <div class="pseudo-code" style="font-size:.8rem;"{attrs}>{hl(code_text)}</div>'


def card(label, code_text, kind='fragment', stdout=None, note=None, out_label='預期輸出', show_out=False):
    parts = ['<div class="deck-extra">', f'  <div class="dx-label">{label}</div>', code(code_text, kind, stdout)]
    if show_out:
        parts.append('  ' + _expected_out(stdout, out_label))
    if note:
        parts.append(f'  <p class="dx-note">{note}</p>')
    parts.append('</div>')
    return '\n'.join(parts)


def program(summary, label, key, note=None, out_label='預期輸出', headers=(), header_label=''):
    """Lecture program: code (and the header functions it calls) collapsed, the output and note visible."""
    body = ''
    if headers:
        body += card(header_label, '\n\n'.join(HPP[h] for h in headers), kind='header')
    body += card(label, RUN[key], kind='run', stdout=OUT[key])
    out = _expected_out(OUT[key], out_label)
    if note:
        out += f'<p class="dx-note">{note}</p>'
    return details(summary, body) + out


def exercise(label, blank, solution_key, solution_label, extra=''):
    """Lecture exercise: the fill-in program stays visible (it does not compile); the answer is collapsed."""
    ex = card(label, blank, kind='exercise')
    sol = card(solution_label, RUN[solution_key], kind='run', stdout=OUT[solution_key],
               show_out=True, out_label='解答的輸出')
    return ex + details('看解答', extra + sol)


def ul(items):
    return '<ul class="srch-ul">' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'


def fill(sid, slots):
    """Insert the lecture material into the hand-written section body."""
    body = LEGACY[sid]
    for name, html in slots.items():
        token = '{{slot:' + name + '}}'
        assert body.count(token) == 1, (sid, name)
        body = body.replace(token, html)
    left = re.findall(r'\{\{slot:[^}]+\}\}', body)
    assert not left, (sid, left)
    return body.rstrip('\n')


VISUALGO = '<a href="https://visualgo.net/en/sorting" target="_blank" rel="noopener">VisuAlgo 的排序動畫</a>'


# ---------------------------------------------------------------- P00
def prologue():
    find = f'''<h3 id="dx-srch">先用標準函式庫：std::find</h3>
<p><strong>搜尋</strong>（searching）是在一群資料中找出特定元素的過程。最常見的問法是「這個值在不在裡面」，答案是 <code>true</code> 或 <code>false</code>。</p>
<p>C++ 做一般的線性成員檢查，可以用 <code>&lt;algorithm&gt;</code> 的 <code>std::find(first, last, item)</code>：它從 <code>first</code> 一路往後比到 <code>last</code> 之前，找到就回傳指向那個元素的迭代器，找不到就回傳 <code>last</code>。所以對 <code>vector&lt;int&gt; aList</code>，判斷式寫成 <code>find(aList.begin(), aList.end(), item) != aList.end()</code>。</p>
{program("講義完整程式：用 std::find 檢查成員", "講義 07 · std::find", 'find',
         note="15 不在 {3, 5, 2, 4, 1} 裡，find 回傳 v.end()，比較結果是 false；3 在裡面，結果是 true。這一行寫起來很短，背後仍然要一個一個比對；搜尋還有其他做法，接下來幾節逐一介紹。")}
'''
    return fill('prologue', {'find': find})


# ---------------------------------------------------------------- P01
def seq_search():
    prog = f'''{figure('seqsearch')}
<p>vector 裡的元素有線性（循序）的關係，每個元素都可以用索引存取。索引本身有順序，所以可以從索引 0 開始依序拜訪每一格，這就是<strong>循序搜尋</strong>（sequential search）。下面的函式需要兩個參數：要搜尋的 vector 與要找的值，回傳值是 <code>bool</code>。</p>
{program("講義完整程式：sequentialSearch", "講義 07 · sequentialSearch", 'seq',
         note="找 44 時比到索引 6 就回傳 true；找 50 時要比完全部 10 個元素才能確定不在，回傳 false。這個版本以值傳遞 <code>vector&lt;int&gt; aList</code>，每次呼叫都會複製整個 vector；課程標頭 <code>searching.hpp</code> 的版本改用 <code>const vector&lt;int&gt;&amp;</code>，不複製，也保證不修改資料。")}
<h3>分析：比較次數</h3>
<p>分析搜尋演算法時，以「比較」作為基本的計算單位，並假設要找的值出現在每個位置的機率都相同。值<strong>不在</strong> list 裡時，唯一的確認方法是跟每個元素都比一次，$n$ 個元素就要比 $n$ 次。值在 list 裡時，最好的情況是第一個就找到（1 次），最差是比到最後一個（$n$ 次），平均約 $\\frac{{n}}{{2}}$ 次。所以循序搜尋是 $O(n)$。</p>
'''
    ordered = f'''{figure('seqsearch2')}
{program("講義完整程式：orderedSequentialSearch", "講義 07 · orderedSequentialSearch", 'ordered',
         note="44 在索引 4 找到；找 50 時比到 54 就停下，只比了 6 次，不必走完 10 個元素。")}
<p>兩個版本的比較次數如下。值在 list 裡時，有序與否沒有差別；值不在時，有序版平均只要比一半就能停下。</p>
{table(['情況', '最佳', '最差', '平均'], [['值在 list 裡（兩種版本）', '1', '$n$', '$\\frac{n}{2}$'],
                                        ['值不在（未排序）', '$n$', '$n$', '$n$'],
                                        ['值不在（已排序）', '1', '$n$', '$\\frac{n}{2}$']])}
'''
    return fill('seq-search', {'seq-program': prog, 'seq-ordered': ordered, 'seq-quiz': quiz('sequential')})


# ---------------------------------------------------------------- P02
def bin_search():
    prog = f'''{figure('binsearch')}
<p>如果中間的值不是要找的值，就利用「有序」這個性質排除一半：要找的值比中間大，左半邊連同中間那個都不可能是答案，只要在右半邊繼續找；比中間小就換成左半邊。在剩下的一半重複同樣的動作。</p>
<h3>課程標頭裡的 binarySearch</h3>
<p>本章的搜尋函式都放在課程標頭 <code>pythonds3/cppds/searching.hpp</code>，程式 <code>#include</code> 之後就能直接呼叫。標頭版的 <code>binarySearch</code> 在每次比較前印出 <code>midpoint - first</code>，也就是中點離目前範圍左端有幾格，方便觀察範圍怎麼縮小。</p>
{program("講義完整程式：binarySearch（含標頭裡的函式）", "講義 07 · 呼叫 binarySearch", 'bin',
         headers=['binarySearch'], header_label='pythonds3/cppds/searching.hpp · binarySearch',
         out_label='預期輸出（每次比較先印出中點離左端的距離）',
         note="找 44：範圍是索引 0 到 9，中點 4 離左端 4 格，第一次就找到。找 50：先比索引 4 的 44，50 比較大，範圍縮成 5 到 9，中點 7 離左端 2 格；65 比 50 大，範圍縮成 5 到 6，中點 5 離左端 0 格；54 也比 50 大，範圍變空，回傳 false。")}
<p>二分搜尋是<strong>分而治之</strong>（divide and conquer）策略的例子：把問題切成較小的部分，用某種方式解決較小的部分，再組合出整個問題的答案。</p>
<h3>遞迴版：只傳索引範圍</h3>
<p>改寫成遞迴時，每次遞迴呼叫處理的是<strong>同一個 vector 上較小的索引範圍</strong>。傳入 <code>first</code> 與 <code>last</code> 就能改變搜尋區間，不必複製出子 vector。<code>binarySearchRec</code> 只是包裝，從整個範圍開始呼叫 <code>binarySearchRecRange</code>。</p>
{program("講義完整程式：binarySearchRec（含標頭裡的函式）", "講義 07 · 呼叫 binarySearchRec", 'bin_rec',
         headers=['binarySearchRecRange', 'binarySearchRec'], header_label='pythonds3/cppds/searching.hpp · 遞迴版',
         out_label='預期輸出（每次比較先印出中點的值）',
         note="標頭的遞迴版印出每次比較的值：找 44 時只比了 44；找 50 時依序比 44、65、54，範圍變空就回傳 false。和迴圈版比較的是同樣幾個位置。")}
<p>下面的動畫用迴圈版逐步執行，可以改陣列與目標值，看 first、last、midpoint 怎麼移動。</p>
'''
    analysis = f'''<h3>分析：最多比幾次</h3>
<p>從 $n$ 個元素開始，第一次比較後大約剩 $\\frac{{n}}{{2}}$ 個，第二次後剩 $\\frac{{n}}{{4}}$，接著 $\\frac{{n}}{{8}}$……</p>
{table(['比較次數', '大約剩下的元素數'], [['1', '$\\frac{n}{2}$'], ['2', '$\\frac{n}{4}$'], ['3', '$\\frac{n}{8}$'], ['…', '…'], ['$i$', '$\\frac{n}{2^i}$']])}
<p>一直切到只剩一個元素時，它要嘛是要找的值，要嘛不是。這時的比較次數 $i$ 滿足 $\\frac{{n}}{{2^i}} = 1$，解得 $i = \\log n$。最多比較次數和元素個數成對數關係，所以二分搜尋是 $O(\\log n)$。</p>
'''
    ex1 = exercise('練習 1 · 填空（目前無法編譯）', EX1_BLANK, 'ex1', '練習 1 · binarySearchRec2 解答',
                   extra='<p>base case 是範圍變空（<code>first &gt; last</code>）。中點用 <code>first + (last - first) / 2</code>，兩次遞迴呼叫都傳同一個 <code>a</code>，只改範圍的一端。解答的 <code>main</code> 多查一次 50，確認找不到時會回傳 false。</p>')
    end = f'''{quiz('binary')}
<h3 id="ex-binary-rec2">練習 1：不複製子 vector 的遞迴二分搜尋</h3>
<p>用遞迴實作二分搜尋，而且不複製子 vector：除了 vector 本身，還要把目前範圍的起點與終點索引一起傳下去。把下面的空格補好，讓程式能編譯，找得到 44、找不到 50。</p>
{ex1}
'''
    return fill('bin-search', {'bin-program': prog, 'bin-analysis': analysis, 'bin-end': end})


# ---------------------------------------------------------------- P03
def hashing():
    table_intro = f'''<p><strong>雜湊表</strong>（hash table）把元素存放在容易再找回來的位置。表中的每個位置稱為 <strong>slot</strong>，從 0 開始編號。一開始表是空的，可以用一個 <code>vector&lt;int&gt;</code> 實作，所有 slot 先放保留值 <code>-1</code>，表示空槽；表的大小記為 $m$。</p>
{figure('hashtable')}
<p>把元素對應到 slot 的規則稱為<strong>雜湊函數</strong>（hash function）：它接受任何一個元素，回傳 0 到 $m - 1$ 之間的整數。</p>
'''
    load = f'''{figure('hashtable2')}
<p>佔用的比例稱為<strong>負載因子</strong>（load factor）$\\lambda = \\frac{{\\text{{元素個數}}}}{{\\text{{表的大小}}}}$。要搜尋某個值時，只要用雜湊函數算出 slot，再看那一格是不是它，搜尋只要 $O(1)$。</p>
<h3>碰撞</h3>
<p>這個方法只有在每個元素都對應到不同 slot 時才行得通。如果下一個要放的是 44，$44 \\bmod 11 = 0$，和 77 落在同一格。兩個以上的元素被雜湊到同一個 slot，稱為<strong>碰撞</strong>（collision，也叫 clash），雜湊必須有辦法處理它。</p>
<p>能把每個元素都對應到不同 slot 的雜湊函數稱為<strong>完美雜湊函數</strong>（perfect hash function）。給定任意一組資料，並沒有系統化的方法造出完美雜湊函數；好在雜湊函數不必完美也能提升效率。目標是：碰撞少、容易計算、讓元素平均分布在表中。不論用哪種方法，最後通常都要取一次餘數，才能把結果限制在 slot 的編號範圍內。</p>
'''
    funcs = f'''<h3>餘數法與平方取中法的程式</h3>
{program("講義完整程式：remainderMethod 與 midsquareMethod", "講義 07 · 兩種雜湊函數", 'hash_funcs',
         note="平方取中：54² = 2916，取中間兩位 91，91 % 11 = 3；17² = 289 只有三位，先補成 0289 再取中間的 28，28 % 11 = 6。同一批數用兩種函數，落點不同。")}
<h3>字串的雜湊函數</h3>
<p>字串也能雜湊。把 "cat" 看成三個字元的序數值（ASCII 碼），加起來再用餘數法：</p>
{figure('stringhash')}
{program("講義完整程式：hashStr", "講義 07 · hashStr", 'hash_str',
         note="<code>int(c)</code> 取得字元的序數值：99 + 97 + 116 = 312，312 % 11 = 4。")}
<p>這個函數有個缺點：字母相同、順序不同的字（anagram），例如 "cat"、"act"、"tac"，雜湊值一定相同。改善方法是用字元的位置當權重：</p>
{figure('stringhash2')}
{fold('把位置權重寫成程式', card('hashStr 與加權版 hashStrWeighted', HASH_STR_WEIGHTED, kind='run', stdout=OUT['hash_str_w'], show_out=True, out_label='預期輸出（字：一般版 加權版）', note='三個字的一般版都是 4；加權版分別是 3、5、2，不再撞在同一格。'))}
<p>雜湊函數本身<strong>必須有效率</strong>，不能讓計算雜湊值變成儲存與搜尋中最花時間的部分；否則還不如直接用前面的搜尋方法。</p>
'''
    probing = f'''<p>回到碰撞的問題。兩個元素雜湊到同一個 slot 時，需要有系統的方法把第二個元素放進表裡，這個過程稱為<strong>碰撞解決</strong>（collision resolution）。簡單的做法是從原本的雜湊位置開始，一格一格往後找，直到碰到第一個空的 slot；走到表尾就繞回開頭，才能涵蓋整張表。</p>
<p>這種「找下一個空位」的方法稱為<strong>開放定址</strong>（open addressing）；一次看一格的版本稱為<strong>線性探查</strong>（linear probing）。把 54, 26, 93, 17, 77, 31, 44, 55, 20 依序放進表裡：前六個直接落在自己的雜湊位置，接著 44 想進 slot 0 卻撞到 77，往後找到 slot 1；55 與 20 也一樣往後找：</p>
{figure('linearprobing1')}
<p>用開放定址與線性探查建好的表，搜尋時也必須用同樣的方法。找 20 時，雜湊值是 9，但 slot 9 放的是 31。不能直接回傳 false，因為 20 可能是碰撞後被推到別處；只能從 slot 10 開始循序往後找，直到找到 20 或碰到空槽。</p>
<p>線性探查的缺點是<strong>群聚</strong>（clustering）：同一個雜湊值碰撞很多次時，附近的 slot 會被一個個填滿，之後插入的元素也受影響。上面放 20 時，就得跳過一整段雜湊到 0 的元素才找到空位：</p>
{figure('clustering')}
<p>處理群聚的一個方法是<strong>跳格</strong>：碰撞後不找下一格，而是每次跳過幾格，讓碰撞的元素分散開來。例如「加 3」探查，碰撞後每隔 3 格檢查一次，直到找到空位。</p>
{steps('「加 3」探查的結果', ['linearprobing2'])}
<p>碰撞後另找一個 slot 的過程統稱為<strong>重新雜湊</strong>（rehashing）。線性探查的重新雜湊函數是 $\\text{{rehash}}(pos) = (pos + skip) \\bmod size$。跳的格數必須讓表中每個 slot 最後都會被拜訪到，否則有一部分的表用不到；所以表的大小通常建議用<strong>質數</strong>。</p>
{program("講義完整程式：用線性探查建表", "講義 07 · 線性探查", 'linear_probe',
         out_label='預期輸出（slot:元素，-1 是空槽）',
         note="結果和上面的圖一致：44、55、20 因為碰撞落在 1、2、3，slot 7、8 仍是空的。")}
<p><strong>平方探查</strong>（quadratic probing）是線性探查的變形：重新雜湊時依序加 1、4、9……，不加固定的格數。第一個雜湊值是 $h$ 時，接著試的位置是 $h+1$、$h+4$、$h+9$ 等，跳的距離是連續的完全平方數。</p>
{figure('quadratic')}
<p>另一種處理碰撞的方法是<strong>鏈結法</strong>（chaining）：每個 slot 存一個集合（鏈），同一個 slot 可以放很多個元素。碰撞時，元素一樣放在自己的雜湊位置；只是同一個位置的元素越多，在那個集合裡找東西就越費時。</p>
{figure('chaining')}
<p>搜尋時先用雜湊函數算出元素應該在的 slot，再用搜尋方法檢查那個 slot 的集合裡有沒有它。</p>
'''
    ex2 = exercise('練習 2 · 填空（目前無法編譯）', EX2_BLANK, 'ex2', '練習 2 · quadraticProbing 解答',
                   extra='<p>第 <code>probe</code> 次重新雜湊要試 <code>h + probe * probe</code>，再對表的大小取餘數。<code>++probe</code> 寫在計算之前，所以第一次試的是 <code>h + 1</code>。</p>')
    exercise_html = f'''{quiz('hash1')}
{quiz('hash2')}
<h3 id="ex-quadratic">練習 2：用平方探查重新雜湊</h3>
<p>實作以平方探查當作重新雜湊方法的 <code>quadraticProbing</code>：探查序列是 $h, h+1, h+4, h+9, \\dots$。把迴圈裡的空格補好，讓九個鍵都落在大小 11 的表中不同的 slot。</p>
{ex2}
<p class="dx-note">第一個值 105 出現在 slot 0：105 的雜湊值是 6，依序試 7、10、4 都有資料，最後落在 (6 + 16) % 11 = 0。99 的雜湊值 0 已被 105 占用，依序試 1、4、9，落在 (0 + 16) % 11 = 5。和線性探查的測驗題比較，同一組鍵的落點不同。</p>
'''
    frag_note = ('<p><code>hashFunction</code> 是簡單的餘數法，碰撞時用「加 1」的線性探查。<code>put</code> 假設最後一定會找到空位；'
                 '如果某個非空 slot 裡已經是同一個 key，就<strong>用新的值取代舊的值</strong>。</p>'
                 '<p><code>get</code> 先算出起始的雜湊值，不在那一格就用 <code>rehash</code> 找下一個可能的位置。'
                 '迴圈裡檢查 <code>position == startSlot</code>，確保繞回起點時就停止：所有可能的 slot 都看過了，這個 key 一定不在表中。</p>')
    map_html = f'''<p>Map ADT 是由 key 與 data 的對應組成的無序集合。<code>HashTable</code> 用兩個平行的 vector 實作：<code>slots</code> 存整數 key，<code>data</code> 在相同的索引存對應的字串。<code>-1</code> 代表空槽，所以這個教學版保留 <code>-1</code>，不接受它當作 key。</p>
{details('講義程式片段：HashTable 的骨架、put 與 get',
         card('講義 07 · HashTable 的資料成員與輔助函式', HT_CLASS)
         + card('講義 07 · put', HT_PUT_FRAG) + card('講義 07 · get', HT_GET_FRAG) + frag_note)}
<h3 id="dx-hash">使用 hashtable.hpp</h3>
<p>完整的教學類別放在 <code>pythonds3/cppds/hashtable.hpp</code>。標頭版的 <code>put</code> 最多探查一整圈，表滿時丟出 <code>std::overflow_error</code>；<code>get</code> 一樣探查一圈就停。下面依序放入九組 key 與 value：</p>
{program("講義完整程式：建表並印出 slots 與 data", "講義 07 · HashTable 使用範例", 'ht1',
         out_label='預期輸出（第一行是 slots，第二行是 data，- 表示空字串）',
         note="slots 的排列和前面線性探查的結果相同：類別只是把「key 的探查」和「value 跟著放進同一格」包在一起。")}
<p>接著讀取並修改表中的資料，注意 key 20 的 value 被取代：</p>
{program("講義完整程式：get 與覆寫", "講義 07 · get 與 put 覆寫", 'ht2',
         note="get(20) 沿著探查鏈在 slot 3 找到 chicken；put(20, \"duck\") 找到同一個 key，只改 data，slots 不變。get(99) 找不到，回傳空字串，所以印出 []。")}
'''
    return fill('hashing', {'hash-table': table_intro, 'hash-load': load, 'hash-functions': funcs,
                            'hash-probing': probing, 'hash-exercise': exercise_html, 'hash-map': map_html})


# ---------------------------------------------------------------- P04
def bubble():
    intro = f'''<h3>排序要數什麼：比較與交換</h3>
<p><strong>排序</strong>（sorting）是把集合中的元素排成某種順序，例如把單字依字母或長度排列。前面的二分搜尋就得益於排好的資料。排序大量資料很耗計算資源，效率同樣和資料量有關：資料少時，複雜的方法可能得不償失；資料多時，就值得用上各種改進。</p>
<p>分析排序時看兩種操作。第一是<strong>比較</strong>：判斷兩個值哪個比較小，總比較次數是最常用的衡量方式。第二是<strong>交換</strong>：兩個值的順序不對時要交換位置，交換的成本高，總交換次數也會影響效率。</p>
{figure('bubblepass')}
<p>list 有 $n$ 個元素時，第一輪要比較 $n-1$ 對。第二輪開始時最大值已經就位，剩下 $n-1$ 個元素、$n-2$ 對要比。每一輪讓下一個最大值就位，所以總共要 $n-1$ 輪。</p>
<h3>交換兩個值</h3>
<p>C++ 可以用一個暫存變數明確地交換兩個值：</p>
{card('講義 07 · 用暫存變數交換', SWAP_FRAG)}
<p>沒有暫存變數，第一個指定就會蓋掉其中一個值。標準函式庫的 <code>swap()</code> 做同樣的事：<code>swap(aList[j], aList[j + 1]);</code>。</p>
'''
    end = f'''<h3 id="dx-bub">講義程式：bubbleSort</h3>
<p>本章所有排序函式都在課程標頭 <code>pythonds3/cppds/sorting.hpp</code>，<code>printl</code> 用來印出整個 vector。標頭版的 <code>bubbleSort</code> 在每一輪開始前印一行。</p>
{program("講義完整程式：bubbleSort（含標頭裡的函式）", "講義 07 · 呼叫 bubbleSort", 'bubble',
         headers=['printl', 'bubbleSort'], header_label='pythonds3/cppds/sorting.hpp · printl 與 bubbleSort',
         out_label='預期輸出（每輪開始前一行，最後一行是排序結果）',
         note="7 個元素共 6 輪。第一輪把 29 送到最右邊，第二輪把 21 放到倒數第二格。第三輪結束時已經排好，但這個版本不會提早停，後面幾輪照樣比較。")}
<p>想看其他排序法的動畫，也可以到 {VISUALGO}。</p>
{quiz('bubble')}
<h3>分析：比較次數與 short bubble</h3>
<p>不論一開始怎麼排列，$n$ 個元素都要跑 $n-1$ 輪：</p>
{table(['輪次', '比較次數'], [['1', '$n-1$'], ['2', '$n-2$'], ['3', '$n-3$'], ['…', '…'], ['$n-1$', '1']])}
<p>總比較次數是前 $n-1$ 個整數的和 $\\frac{{1}}{{2}}n^{{2}} - \\frac{{1}}{{2}}n$，也就是 $O(n^2)$。氣泡排序常被認為是最沒效率的排序法，因為它在知道元素最終位置之前就不斷交換，這些「白做」的交換成本很高。</p>
<p>不過它每一輪都走過整個未排序的部分，所以能做到大多數排序法做不到的事：<strong>某一輪完全沒有交換，就表示 list 已經排好</strong>，可以提早結束。這個版本常稱為 short bubble。</p>
{program("講義完整程式：bubbleSortShort（含標頭裡的函式）", "講義 07 · 呼叫 bubbleSortShort", 'short',
         headers=['bubbleSortShort'], header_label='pythonds3/cppds/sorting.hpp · bubbleSortShort',
         out_label='預期輸出（bubbleSortShort 不印每一輪，只印最後結果）',
         note="這個 list 只有 90 不在正確位置。第一輪把 90 換到 100 前面，第二輪沒有任何交換，迴圈就 break，不必跑完 9 輪。")}
'''
    return fill('bubble', {'bubble-intro': intro, 'bubble-end': end})


# ---------------------------------------------------------------- P05
def selection():
    intro = f'''<p>和氣泡排序一樣，第一輪之後最大值就位，第二輪之後第二大的值就位；$n$ 個元素需要 $n-1$ 輪，因為前 $n-1$ 輪結束後，最後一個元素一定也在正確位置。</p>
{figure('selectionsortnew')}
'''
    end = f'''<h3 id="dx-sel">講義程式：selectionSort</h3>
{program("講義完整程式：selectionSort（含標頭裡的函式）", "講義 07 · 呼叫 selectionSort", 'selection',
         headers=['selectionSort'], header_label='pythonds3/cppds/sorting.hpp · selectionSort',
         out_label='預期輸出（每輪開始前一行，最後一行是排序結果）',
         note="第一輪最大值 20 已經在最後一格，positionOfMax 等於 fillSlot，不必交換，所以前兩行相同。之後每一行的右側都多一個就位的數。")}
<p>選擇排序的比較次數和氣泡排序相同，也是 $O(n^2)$；但交換次數少得多，所以在實測中通常跑得比較快。</p>
'''
    return fill('selection', {'selection-intro': intro, 'selection-end': end})


# ---------------------------------------------------------------- P06
def insertion():
    intro = f'''{figure('insertionsort')}
<p>一開始假設只有位置 0 的一個元素是排好的子清單。每一輪處理位置 1 到 $n-1$ 中的一個元素，往回跟子清單比較：比它大的元素往右移一格；碰到比它小的元素或子清單的開頭時，就把它放進空出的位置。</p>
{figure('insertionpass')}
'''
    end = f'''<h3 id="dx-ins">講義程式：insertionSort</h3>
<p><code>insertionSort()</code> 同樣要跑 $n-1$ 輪。迴圈從位置 1 走到 $n-1$，這些就是要插回子清單的元素。</p>
{program("講義完整程式：insertionSort（含標頭裡的函式）", "講義 07 · 呼叫 insertionSort", 'insertion',
         headers=['insertionSort'], header_label='pythonds3/cppds/sorting.hpp · insertionSort',
         out_label='預期輸出（每次插入前一行，最後一行是排序結果）',
         note="每一行左邊排好的部分多一個元素。兩個 5 與兩個 9 的先後順序沒有改變：比較用的是嚴格的 <code>&gt;</code>，相等的元素不會被移到彼此前面。")}
<p>一次移動的工作量大約只有一次交換的三分之一，因為移動只做一次指定。在實測中，插入排序的表現相當好。</p>
'''
    return fill('insertion', {'insertion-intro': intro, 'insertion-end': end})


# ---------------------------------------------------------------- P07
def shell():
    intro = f'''<p>希爾排序又稱<strong>遞減增量排序</strong>（diminishing increment sort）。它用一個增量 $i$（稱為 <strong>gap</strong>）切子清單：子清單裡的元素彼此相隔 $i$ 個位置，不是相鄰的元素。增量為 3 時有三個子清單，各自用插入排序排好：</p>
{figure('shellsortA')}
{figure('shellsortB')}
<p>子清單排好後，元素已經移到靠近最終位置的地方。最後用增量 1，也就是一般的插入排序收尾；因為前面已經做過子清單排序，需要的移動次數少很多，這個例子只要再 4 次移動。增量怎麼選，是希爾排序最有特色的地方。</p>
{steps('增量 1 收尾，以及程式實際用的增量 4', ['shellsortC', 'shellsortD'])}
'''
    end = f'''<h3 id="dx-shl">講義程式：shellSort</h3>
{program("講義完整程式：shellSort（含標頭裡的函式）", "講義 07 · 呼叫 shellSort", 'shell',
         headers=['gapInsertionSort', 'shellSort'], header_label='pythonds3/cppds/sorting.hpp · gapInsertionSort 與 shellSort',
         out_label='預期輸出（每個增量做完後一行，最後一行是 printl 的結果）',
         note="一開始有 $\\frac{n}{2}$ 個子清單（9 個數時增量為 4），下一輪 $\\frac{n}{4}$ 個（增量 2），最後增量 1，用一般的插入排序排好整個 list。")}
<p>希爾排序的一般分析超出本課範圍，大致介於 $O(n)$ 與 $O(n^2)$ 之間。改用 $2^k-1$（1、3、7、15、31……）當增量，希爾排序可以達到 $O(n^{{\\frac{{3}}{{2}}}})$。</p>
'''
    return fill('shell', {'shell-intro': intro, 'shell-end': end})


# ---------------------------------------------------------------- P08
def merge():
    intro = f'''{figure('mergesortA')}
<p>兩半都排好之後，執行最基本的操作<strong>合併</strong>（merge）：把兩個較小的已排序 list 組合成一個新的已排序 list。</p>
{figure('mergesortB')}
'''
    end = f'''<h3 id="dx-mrg">講義程式：mergeSort</h3>
{program("講義完整程式：mergeSort（含標頭裡的函式）", "講義 07 · 呼叫 mergeSort", 'merge',
         headers=['mergeSort'], header_label='pythonds3/cppds/sorting.hpp · mergeSort',
         out_label='預期輸出（Splitting 是進入呼叫時，Merging 是合併完成時）',
         note="Splitting 一路把 vector 切到只剩一個元素，Merging 再把排好的兩半合併回去。最後一行 Merging 就是排序結果。")}
<p>對左右兩半呼叫 <code>mergeSort()</code> 之後，就假設它們已經排好；函式剩下的部分負責把兩個較小的已排序 list 合併成一個。合併時反覆挑出兩邊前端較小的那個，一次一個寫回原本的 <code>aList</code>。比較用的是 <code>leftHalf[i] &lt;= rightHalf[j]</code>，相等時先拿左邊的，所以相等元素的相對順序不變，這個實作是<strong>穩定</strong>的。</p>
<h3>分析</h3>
<p>mergeSort 有兩個部分。遞迴把 vector 切成兩半，共 $\\log n$ 層。合併時每個元素最後都要處理一次、放進排好的 list，所以<strong>每一層</strong>的合併需要 $n$ 次操作。$\\log n$ 層、每層 $n$，總共 $n\\log n$ 次操作：合併排序是 $O(n\\log n)$ 的演算法。</p>
<p>暫存的左右兩半最多需要 $O(n)$ 的額外元素空間，遞迴堆疊再加上 $O(\\log n)$。資料量很大時，這個記憶體成本可能是問題。</p>
{quiz('merge')}
'''
    return fill('merge', {'merge-intro': intro, 'merge-end': end})


# ---------------------------------------------------------------- P09
def quick():
    intro = f'''<p>選 pivot 的方法有很多，這裡直接用 list 的第一個元素。pivot 在最終排好的 list 中的位置稱為<strong>分割點</strong>（split point），之後的遞迴呼叫就以它為界把 list 分成兩段。下例用 54 當第一個 pivot：</p>
{figure('firstsplit')}
<p>接下來是 <strong>partition</strong> 過程：找出分割點，同時把其他元素移到正確的一側。先在剩下元素的頭尾放兩個位置標記 <code>leftMark</code> 與 <code>rightMark</code>，目標是把放錯邊的元素換過去，同時逼近分割點。</p>
{figure('partitionA')}
<p>先把 <code>leftMark</code> 往右移，直到找到比 pivot 大的值；再把 <code>rightMark</code> 往左移，直到找到比 pivot 小的值。這兩個值相對於分割點都放錯邊了，交換它們，再重複同樣的步驟。當 <code>rightMark</code> 跑到 <code>leftMark</code> 左邊時停止，<code>rightMark</code> 的位置就是分割點。把 pivot 和分割點的值交換，pivot 就到了最終位置。</p>
{figure('partitionB')}
<p>此時分割點左邊都小於 pivot，右邊都大於 pivot。在分割點把 list 分成兩半，對兩半各自遞迴呼叫 quicksort。</p>
'''
    sketch = card('講義 07 · 練習 3 的解法綱要', QDESC_SKETCH)
    hdr = card('pythonds3/cppds/sorting.hpp · partitionDesc、quickSortHelperDesc 與 quickSortDesc',
               '\n\n'.join(HPP[h] for h in ('partitionDesc', 'quickSortHelperDesc', 'quickSortDesc')), kind='header')
    end = f'''<h3 id="dx-qck">講義程式：quickSort</h3>
{program("講義完整程式：quickSort（含標頭裡的函式）", "講義 07 · 呼叫 quickSort", 'quick',
         headers=['partition', 'quickSortHelper', 'quickSort'], header_label='pythonds3/cppds/sorting.hpp · partition、quickSortHelper 與 quickSort',
         out_label='預期輸出（每次 partition 後一行，最後一行是排序結果）',
         note="第一行是以 54 分割的結果，和上面的圖相同：54 在索引 5，左邊都比它小，右邊都比它大。之後每一行再多一個 pivot 就位；長度不到 2 的範圍不做 partition，也不印。")}
<h3>分析與 median of three</h3>
<p>找分割點時，$n$ 個元素都要和 pivot 比一次。分割點都落在中間附近時，會切 $\\log n$ 層，結果是 $O(n\\log n)$；而且不像合併排序需要額外的記憶體。</p>
<p>可惜最差的情況下，分割點可能非常偏左或偏右，切得很不平均：每次都分成 0 個與 $n-1$ 個元素，接著 $n-1$ 個又分成 0 個與 $n-2$ 個……結果是 $O(n^2)$，還要加上遞迴本身的額外成本。</p>
<p>選 pivot 的一種改進方法是 <strong>median of three</strong>：看 list 的第一個、中間與最後一個元素，取三者的中位數當 pivot。上面的例子中三個值是 54、77、20，中位數是 54。當第一個元素不屬於 list 的中段時，這樣能選到比較接近中間的值，對原本就部分排好的 list 特別有用。</p>
{quiz('quick')}
<h3 id="ex-quick-desc">練習 3：讓 quickSort 支援遞減排序</h3>
<p>替 quickSort 加一個 <code>bool descending</code> 參數，讓同一套程式既能遞增也能遞減排序。先自己想想：遞迴的骨架要改什麼？partition 裡哪幾個比較要改方向？</p>
{details('看解答', sketch + '<p>遞迴骨架只是把 <code>descending</code> 往下傳，真正要改的是 partition：遞減時，<code>leftMark</code> 找「比 pivot 小」的值，<code>rightMark</code> 找「比 pivot 大」的值，也就是兩個內層 while 的比較方向對調。課程標頭把這一組函式命名為 <code>partitionDesc</code>、<code>quickSortHelperDesc</code> 與 <code>quickSortDesc</code>，才能和遞增版的 <code>quickSort</code> 放在同一個標頭裡。</p>' + hdr)}
{program("講義完整程式：quickSortDesc", "講義 07 · 呼叫 quickSortDesc", 'qdesc',
         note="同一套 partition 的想法兩個方向都能排，只是比較的方向反過來。")}
<h3>實務上：std::sort</h3>
<p>本章的排序函式都收在 <code>pythonds3/cppds/sorting.hpp</code>。實際寫程式時，優先用標準函式庫的 <code>std::sort</code>。C++ 標準要求它對一般的隨機存取範圍最差做 $O(n\\log n)$ 次比較，但不規定實作策略；常見的標準函式庫用類似 introsort 的混合做法。</p>
{program("講義完整程式：std::sort", "講義 07 · std::sort", 'std_sort')}
'''
    return fill('quick', {'quick-intro': intro, 'quick-end': end})


# ---------------------------------------------------------------- site additions (folded)
def depends():
    body = LEGACY['depends']
    k = body.index('  <h3>兩種基本存取模式</h3>')
    lead, rest = body[:k], body[k:]
    return lead + fold('完整內容：存取模式、對照表與選擇底層結構', rest.rstrip('\n'))


def reference():
    lead = '<p>把本章的搜尋與排序演算法放在同一張表比較：時間、空間、是否穩定、是否就地排序，以及什麼情況該選哪一個。</p>\n'
    return lead + fold('九個演算法的比較表與選擇指南', LEGACY['reference'].strip('\n'))


def supplement():
    body = LEGACY['supplement']
    a = body.index('  <!-- ============= PART A')
    b = body.index('  <h3 id="sup-put"')
    k = body.rfind('<!--', a + 10, b)
    k = k if k > a else b
    lead, part_a, part_b = body[:a], body[a:k], body[k:]
    return (lead + fold('A. 平方探查全程追蹤', part_a.rstrip('\n'))
            + '\n' + fold('B. put() 會遇到的 4 種情況', part_b.rstrip('\n')))


# FAQ entries that come straight from the lecture notes (no （補充） tag).
IN_NOTES = {'二分搜尋一定比循序搜尋好嗎？', 'get 回傳空字串，怎麼知道 key 到底在不在？'}


def recap():
    qa = [
        ('二分搜尋一定比循序搜尋好嗎？',
         '<p>不一定。二分搜尋要求資料已排序，而排序本身要 $O(n\\log n)$。只搜尋一次時，直接循序搜尋 $O(n)$ 反而比較省；同一份資料要搜尋很多次，排序的成本才攤得掉。資料量很小時，兩者差距也不明顯。</p>'),
        ('get 回傳空字串，怎麼知道 key 到底在不在？',
         '<p>在這個教學版的 <code>HashTable</code> 裡分不出來：key 不存在與 value 本來就是空字串，回傳值都是 <code>""</code>。完整的 Map ADT 會另外提供 <code>contains(key)</code>；<code>std::unordered_map</code> 則可以用 <code>find</code> 或 <code>count</code> 判斷。</p>'),
        ('為什麼表的大小常選質數？',
         '<p>重新雜湊時每次跳 skip 格。如果 skip 和表的大小有公因數，探查只會在部分 slot 之間打轉，其他 slot 永遠用不到。表的大小是質數時，任何不是它倍數的 skip 都和它互質，最後一定能拜訪到每個 slot。</p>'),
        ('快速排序最差是 $O(n^2)$，為什麼實務上還常用？',
         '<p>pivot 選得不差時，quicksort 平均是 $O(n\\log n)$，不需要合併排序那樣的 $O(n)$ 暫存空間，存取也集中在同一個 vector 上。median of three 等選 pivot 的方法能降低碰到最差情況的機會；<code>std::sort</code> 常見的實作還會在遞迴太深時改用其他方法，保證最差 $O(n\\log n)$。</p>'),
        ('哪些排序是穩定的？',
         '<p>本章的實作中，氣泡排序、插入排序與合併排序是穩定的：相等的元素不會被交換或移到彼此前面。選擇排序、希爾排序與快速排序會把元素跨過一段距離交換，相等元素的順序可能改變。</p>'),
    ]
    faq = ''.join(details(q if q in IN_NOTES else f'{q}（補充）', a, cls='srch-detail srch-faq') for q, a in qa)
    return f'''<ul class="srch-ul srch-recap">
<li>搜尋回答「在不在」。<code>std::find</code> 與循序搜尋逐一比對，都是 $O(n)$；資料已排序時，循序搜尋可以提前停止，但仍是 $O(n)$。</li>
<li>二分搜尋每次比較中間的值，排除一半的範圍，是 $O(\\log n)$；前提是資料已排序。遞迴版傳索引範圍 <code>first</code>、<code>last</code>，不複製子 vector。</li>
<li>雜湊用雜湊函數把元素直接對應到 slot：餘數法、折疊法、平方取中法，字串可以加總字元的序數值。負載因子 $\\lambda$ 越大，碰撞越多。</li>
<li>碰撞解決：開放定址（線性探查、跳格、平方探查）在表內另找空位，線性探查容易群聚；鏈結法讓同一個 slot 存一條鏈。搜尋時必須沿用插入時的探查方法。</li>
<li><code>HashTable</code> 用平行的 <code>slots</code> 與 <code>data</code> 實作 Map ADT 的 <code>put</code>、<code>get</code>：同一個 key 再 put 會取代 value；探查繞回起點就停止。</li>
<li>氣泡、選擇、插入排序都是 $O(n^2)$ 次比較。選擇排序每輪最多交換一次；插入排序用移動取代交換，對幾乎排好的資料很快；short bubble 在某一輪沒有交換時提早結束。</li>
<li>希爾排序先用較大的 gap 對子清單做插入排序，最後 gap 為 1，大致介於 $O(n)$ 與 $O(n^2)$ 之間。</li>
<li>合併排序切半再合併，$O(n\\log n)$、穩定，但需要 $O(n)$ 額外空間；快速排序用 pivot 做 partition，平均 $O(n\\log n)$、不需額外陣列，最差 $O(n^2)$，可用 median of three 改善。實務上用 <code>std::sort</code>。</li>
</ul>
<h3>常見疑問</h3>
{faq}'''


def sections():
    return {
        'search-prologue': prologue(),
        'search-seq-search': seq_search(),
        'search-bin-search': bin_search(),
        'search-hashing': hashing(),
        'search-bubble': bubble(),
        'search-selection': selection(),
        'search-insertion': insertion(),
        'search-shell': shell(),
        'search-merge': merge(),
        'search-quick': quick(),
        'search-depends': depends(),
        'search-reference': reference(),
        'search-supplement': supplement(),
        'search-recap': recap(),
    }


STYLE = """<style id="search-depth-style">
.srch-detail{margin:1rem 0;border:1px solid var(--card-border);border-radius:8px;background:var(--card);}
.srch-detail>summary{cursor:pointer;padding:.9rem 1rem;font-weight:600;line-height:1.6;}
.srch-detail-body{padding:0 1rem 1rem;min-width:0;}
.srch-detail-body .pseudo-code,.deck-extra .pseudo-code,.side-panel .pseudo-code{max-width:100%;overflow-x:auto;}
.srch-ul{padding-left:1.4rem;margin:.6rem 0 1rem;}
.srch-ul li{margin:.3rem 0;line-height:1.8;}
.srch-quiz{margin-top:1.2rem;}
.srch-quiz .sq-num{margin-right:.6rem;}
.viz-layout,.viz-layout>div{min-width:0;}
</style>"""
