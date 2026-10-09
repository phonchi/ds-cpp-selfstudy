"""Chapter 5 section bodies. Each value of sections() fills one <!-- gen:NAME --> block.

Lecture code comes from 05_Linear_Structure.ipynb and pythonds3/cppds/*.hpp (see linear_programs);
expected outputs come from compiling the programs.
"""
from html import escape
from enrich_lib import hl
from content.linear_figures import figure, pair
from content.linear_programs import *  # noqa: F401,F403  (programs and OUTPUT)


def details(summary, body, cls='linear-detail', did=''):
    ident = f' id="{did}"' if did else ''
    return f'<details class="{cls}"{ident}><summary>{summary}</summary><div class="linear-detail-body">{body}</div></details>'


def fold(title, body, did=''):
    """Content the lecture does not cover: collapsed and labelled （補充）."""
    return details(title + '（補充）', body, did=did)


def table(headers, rows):
    return ('<div style="overflow-x:auto"><table class="cmp-table"><thead><tr>'
            + ''.join(f'<th>{h}</th>' for h in headers) + '</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{v}</td>' for v in r) + '</tr>' for r in rows)
            + '</tbody></table></div>')


def quiz(qid, label, question, options, code=None):
    """options: [(correct, text, feedback)]; the page shuffles option order at load time."""
    opts = ''.join(
        f'<div class="quiz-opt" data-correct="{"true" if ok else "false"}" data-fb="{escape(fb, quote=True)}" '
        f'onclick="quizCheck(\'{qid}\', this)"><span class="opt-letter">({chr(65 + i)})</span> <span class="opt-text">{text}</span></div>'
        for i, (ok, text, fb) in enumerate(options))
    shown = f'\n  <div class="pseudo-code linear-quiz-code" data-cpp="fragment">{hl(code)}</div>' if code else ''
    return (f'<div class="quiz-box">\n  <div class="quiz-label">{label}</div>\n  <p>{question}</p>{shown}\n'
            f'  <div class="quiz-options" id="{qid}Options">\n    {opts}\n  </div>\n'
            f'  <div class="quiz-feedback" id="{qid}Feedback"></div>\n</div>')


def _expected_attr(output):
    return ' data-expected="' + escape(output + '\n', quote=True).replace('\n', '&#10;') + '"'


def _expected_out(output, tag='預期輸出'):
    return (f'<div class="expected-out"><span class="eo-tag">{tag}</span><pre>'
            + escape(output) + '</pre></div>')


def snippet(label, code, output=None, note=None, kind=None, out_tag='預期輸出'):
    """Code card. kind: run | fragment | compile-error | exercise | header (chapter-3 convention);
    data-expected holds the exact stdout of a run block."""
    if kind is None:
        kind = 'run' if output is not None and 'int main' in code else 'fragment'
    attrs = f' data-cpp="{kind}"' + (_expected_attr(output) if kind == 'run' and output is not None else '')
    parts = ['<div class="deck-extra">', f'  <div class="dx-label">{label}</div>',
             f'  <div class="pseudo-code" style="font-size:.8rem;"{attrs}>{hl(code)}</div>']
    if output is not None:
        parts.append('  ' + _expected_out(output, out_tag))
    if note:
        parts.append(f'  <p class="dx-note">{note}</p>')
    parts.append('</div>')
    return '\n'.join(parts)


def lecture_program(summary, label, key, note=None):
    """Lecture program: the code is collapsed, the expected output and the note stay visible."""
    code, output = PROGRAMS[key], OUTPUT[key]
    card = snippet(label, code, kind='run').replace('data-cpp="run"', 'data-cpp="run"' + _expected_attr(output), 1)
    out = _expected_out(output)
    if note:
        out += f'<p class="dx-note">{note}</p>'
    return details(summary, card) + out


def run_card(label, key, note=None):
    """Complete program shown with its output in one card (used inside （補充） folds)."""
    return snippet(label, PROGRAMS[key], OUTPUT[key], note=note, kind='run')


def ul(items, cls='linear-ul'):
    return f'<ul class="{cls}">' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'


def ol(items):
    return '<ol class="linear-ol">' + ''.join(f'<li>{x}</li>' for x in items) + '</ol>'


# ---------------------------------------------------------------- P00
def prologue():
    rows = table(['結構', '加入的位置', '移除的位置', '順序原則', 'C++ 標準函式庫', '課程標頭'], [
        ('Stack 堆疊', 'top', 'top（同一端）', 'LIFO：後進先出', '<code>std::stack&lt;T&gt;</code>', '<code>stack.hpp</code> 的 <code>Stack&lt;T&gt;</code>'),
        ('Queue 佇列', 'rear', 'front', 'FIFO：先進先出', '<code>std::queue&lt;T&gt;</code>', '<code>queue.hpp</code> 的 <code>Queue&lt;T&gt;</code>'),
        ('Deque 雙端佇列', '兩端皆可', '兩端皆可', '不限定，由使用者決定', '<code>std::deque&lt;T&gt;</code>', '<code>deque.hpp</code> 的 <code>Deque&lt;T&gt;</code>'),
    ])
    return f'''<h3>什麼是線性結構</h3>
<p>線性結構是一群依加入或移除的方式而有順序的資料。一個元素加入之後，相對於比它早來和比它晚來的元素，它的位置就固定了。這類集合稱為<strong>線性 ADT</strong>（linear ADT）。</p>
<p>線性 ADT 可以想成有兩端，有時叫左端與右端，有時叫 front（前端）與 rear（後端）。各種線性結構的差別，在於元素從<strong>哪一端加入、從哪一端移除</strong>：</p>
{rows}
<h3>本章程式使用的兩套介面</h3>
<p>本章的程式以 C++ 標準函式庫（STL）為主：<code>std::stack</code>、<code>std::queue</code>、<code>std::deque</code>。它們的 <code>pop()</code> 只移除元素、不回傳值，需要值的時候要先用 <code>top()</code> 或 <code>front()</code> 讀出來。</p>
<p>課程標頭 <code>pythonds3/cppds/</code> 另外提供以 <code>vector</code> 實作的 <code>Stack&lt;T&gt;</code>、<code>Queue&lt;T&gt;</code>、<code>Deque&lt;T&gt;</code>，方法名稱是 <code>peek</code>、<code>isEmpty</code>、<code>enqueue</code>、<code>dequeue</code>、<code>addFront</code> 這一類，<code>pop</code>／<code>dequeue</code> 會回傳被移除的值。作業明確要求時才用課程標頭；兩套介面的方法名稱不同，不能混用。各節都會列出兩者的對照。</p>'''


# ---------------------------------------------------------------- P01 stack
def stack_intro():
    return f'''<h3>top 與 base</h3>
<p>stack（也叫 push-down stack）是一個有順序的集合，新增元素與移除元素<strong>永遠在同一端</strong>進行，這一端叫 <strong>top</strong>，另一端叫 <strong>base</strong>。越靠近 base 的元素在 stack 裡待得越久；最近加入的元素，會最先被移除。這個原則叫 <strong>LIFO</strong>（last in, first out，後進先出）。所以 stack 依「在集合中待了多久」排列元素：新的靠近 top，舊的靠近 base。</p>
<p>餐廳裡疊起來的餐盤就是一例：客人拿走最上面的一個，下面的一個才露出來。桌上的一疊書也一樣，只看得到最上面那本的封面；要拿下面的書，得先把壓在上面的書拿走。</p>
{figure('books')}
<h3>stack 會反轉順序</h3>
<p>從空桌面開始，一本一本把書往上疊，就是在建立一個 stack。開始拿書時，拿走的順序正好和放上去的順序相反。stack 的一個重要用途就是<strong>反轉順序</strong>：移除的順序是加入順序的反向。</p>
{figure('reverse')}
<p>瀏覽器的「上一頁」按鈕也是 stack。每瀏覽一個新網頁，它的網址就放到 stack 上；目前看的網頁在 top，最早看的網頁在 base。按下「上一頁」，就依相反的順序一頁一頁退回去。</p>'''


def stack_stl():
    apis = table(['介面', '建立', '讀取 top', '移除 top'], [
        ('STL <code>std::stack&lt;T&gt;</code>', '<code>std::stack&lt;T&gt; s;</code>', '<code>top()</code>', '<code>pop()</code>，回傳 <code>void</code>'),
        ('課程標頭 <code>stack.hpp</code> 的 <code>Stack&lt;T&gt;</code>', '<code>Stack&lt;T&gt; s;</code>', '<code>peek()</code>', '<code>pop()</code>，回傳 <code>T</code>'),
        ('HW3 定容量 stack', '<code>Stack&lt;T&gt; s(capacity);</code>', '<code>stackTop()</code> 或 <code>peek(index)</code>', '<code>pop()</code>，回傳 <code>T</code>'),
    ])
    moves = table(['n（push n 次、再全部 pop）', 'Stack（top 在尾端）搬移元素數', 'Stack2（top 在開頭）搬移元素數'], [
        ('n = 10', '0', '90'), ('n = 100', '0', '9,900'), ('n = 1,000', '0', '999,000')])
    moves_note = ('<p>Stack2 第 k 次 push 時，stack 裡已有 k − 1 個元素，<code>insert(begin())</code> 要把它們全部往後搬一格；pop 時 <code>erase(begin())</code> 也要把其餘元素往前搬。push n 次共搬 $0+1+\\cdots+(n-1)=\\frac{n(n-1)}{2}$ 次，全部 pop 再搬同樣多次，合計 $n(n-1)$ 次，約 $n^2$。'
                  '以 vector 尾端當 top 的 Stack 只動最後一格，不必搬移任何元素（容量不足時的重新配置除外）。</p>')
    return f'''<h3>在 C++ 使用 std::stack</h3>
<p>C++ 標準函式庫的 <code>std::stack&lt;T&gt;</code> 是一種<strong>容器轉接器</strong>（container adapter）：元素預設存放在 <code>std::deque</code> 裡，但對外只開放 LIFO 的操作。使用 stack 的程式只依賴 stack 的介面，不能讀寫底層容器的任意位置。</p>
{ul([
    '<code>push(item)</code>：把 item 放到 top，回傳 <code>void</code>。',
    '<code>top()</code>：讀取 top 的元素，但不移除。',
    '<code>pop()</code>：移除 top 的元素，回傳 <code>void</code>；需要那個值時，先呼叫 <code>top()</code>。',
    '<code>empty()</code> 檢查是否為空；<code>size()</code> 回傳元素個數。',
    '對空的 stack 呼叫 <code>top()</code> 或 <code>pop()</code> 違反前提條件（precondition），結果是未定義行為。',
])}
<p>一個 stack 物件只存一種型別，例如 <code>stack&lt;string&gt;</code>：</p>
{snippet('std::stack 的基本用法', STL_STACK_SNIPPET, kind='fragment')}
<p>下面的程式依序 push 三個字串，再檢查大小、是否為空，以及 top 的元素：</p>
{lecture_program('完整程式：使用 std::stack', 'std::stack&lt;string&gt; 的基本操作', 'stl_stack',
                 note='"true" 最後 push，所以在 top；pop 移除它之後，top 變成 "dog"。<code>boolalpha</code> 讓 bool 值印成 true／false 而不是 1／0。')}
<h3>課程中的三套 stack 介面</h3>
{apis}
<p>HW3 的類別另外提供 <code>isFull()</code>。三套介面的方法名稱不同，寫程式時要看清楚用的是哪一套。課程標頭的 <code>Stack&lt;T&gt;</code> 以 vector 的尾端當 top，push 與 pop 都只動最後一格：</p>
{details('課程標頭 stack.hpp 的 Stack&lt;T&gt;', snippet('pythonds3/cppds/stack.hpp · Stack', STACK_HPP, kind='header'))}
<h3>把 top 放在 vector 開頭：Stack2</h3>
<p>也可以把 top 放在 vector 的<strong>開頭</strong>。這時 <code>push_back()</code> 與 <code>pop_back()</code> 碰不到 top，只能改用 <code>insert(begin())</code> 與 <code>erase(begin())</code>。每次 push 和 pop 都要把其餘元素搬動一格，原本 $O(1)$ 的操作變成 $O(n)$。</p>
{snippet('Stack2：top 在 vector 開頭', STACK2_CLASS, kind='fragment')}
<p><code>stack.hpp</code> 也提供這個 Stack2。用起來和其他 stack 完全一樣：</p>
{lecture_program('完整程式：透過 stack.hpp 使用 Stack2', 'Stack2&lt;double&gt; 的操作', 'stack2_main',
                 note='輸出顯示 Stack2 的行為仍然正確：peek 看到最後 push 的 7.5；連續兩次 pop 依序取出 2 與 7.5，最後剩 1 個元素。')}
<p>換掉實作方式、保留邏輯上的行為，就是抽象化。不過兩種實作的效能不同：<code>std::stack</code> 預設以 deque 為底層，push、pop、top 都是常數時間；以 vector 尾端當 top 的 Stack，<code>push_back</code> 是攤銷 $O(1)$，<code>pop_back</code> 是 $O(1)$；Stack2 刻意把 top 放在 <code>vector::begin()</code>，插入與刪除都要搬動元素，成本是 $O(n)$。ADT 的行為相同，不代表實作的成本相同。</p>
{fold('Stack 與 Stack2 的搬移次數', moves + moves_note)}
{quiz('qStack1', 'QUIZ · stack 操作後的 top',
      '執行下列程式之後，top 的元素是什麼？', [
          (False, '<code>"x"</code>', '"x" 還在 stack 裡，但壓在最底下；push("z") 之後，top 是 "z"。'),
          (False, '<code>"y"</code>', '"y" 已經被 pop() 移除了。'),
          (True, '<code>"z"</code>', '追蹤一次：push("x") 得到 [x]；push("y") 得到 [x, y]；pop() 移除 y，剩 [x]；push("z") 得到 [x, z]，所以 top() 是 "z"。'),
          (False, 'stack 是空的', '最後 stack 裡還有 "x" 與 "z" 兩個元素。'),
      ], code='std::stack<std::string> m;\nm.push("x");\nm.push("y");\nm.pop();\nm.push("z");\nm.top();')}
{quiz('qStack2', 'QUIZ · 連續 pop',
      '執行下列 <code>std::stack</code> 程式會發生什麼事？', [
          (False, '最後剩下 <code>"x"</code>', '第一輪迴圈結束時確實剩下 "x"，但 stack 還不是空的，迴圈會再跑一輪。'),
          (False, 'stack 變成空的，程式正常結束', 'stack 的確會在過程中變空，但第二輪的第二個 pop() 是對空 stack 呼叫的，程式沒辦法正常完成。'),
          (True, '對空的 stack 呼叫 pop()，屬於未定義行為（很可能當掉）', '第一輪的兩次 pop 移除 "z" 與 "y"，剩一個元素；第二輪先移除 "x"，接著對空的 std::stack 呼叫 pop()，違反前提條件，結果未定義。'),
          (False, '最後剩下 <code>"z"</code>', '"z" 在 top，第一次 pop 就把它移除了。'),
      ], code='std::stack<std::string> m;\nm.push("x");\nm.push("y");\nm.push("z");\nwhile (!m.empty()) {\n    m.pop();\n    m.pop();\n}')}'''


def stack_exercise():
    return f'''<h3 id="linear-ex-rev">練習：用 stack 反轉字串</h3>
<p>用 <code>std::stack&lt;char&gt;</code> 寫出 <code>revString</code>，把字串反過來。程式留了兩個空：第一步把每個字元 push 到 s 上，第二步從 s 一個一個 pop，組成 rStr。</p>
{snippet('練習：revString', REV_EXERCISE, output='USYSN', kind='exercise', out_tag='完成後的預期輸出')}
{fold('revString 參考解答', run_card('revString 完整程式', 'rev_solution',
      note='N、S、Y、S、U 依序 push 之後，最後的 U 在 top；pop 的順序是 U、S、Y、S、N，接起來就是反轉後的字串。'))}'''


# ---------------------------------------------------------------- P02 balanced symbols
def parens():
    return f'''<h3>什麼是平衡的括號</h3>
<p>寫算術式 $(5 + 6) \\times (7 + 8) / (4 + 3)$ 時，括號用來決定運算的順序。有些程式語言的語法也大量使用括號，例如：</p>
<pre class="linear-pre">(defun square(n)
     (* n n))</pre>
<p>這兩個例子中，括號都必須<strong>平衡</strong>：每個左括號都有對應的右括號，而且成對的括號正確地巢狀。能分辨括號平衡與否，是辨認許多程式語言結構的重要一步。問題是：由左到右讀一串括號，判斷它們是否平衡。</p>
<p>由左到右處理時，下一個右括號必須和<strong>最近</strong>的一個左括號配對；第一個左括號，則可能要等到最後一個符號才配對。</p>
{figure('paren')}
<p>右括號配對左括號的順序，和左括號出現的順序相反，由內往外配對，這是可以用 stack 解決的線索。</p>
<h3>演算法與 parChecker</h3>
{ol([
    '從空的 stack 開始，由左到右處理字串中的每個括號。',
    '遇到左括號就 push，當作「之後需要一個右括號」的記號。',
    '遇到右括號就 pop 一次。',
    '每個右括號都 pop 得到一個左括號，而且讀完字串時 stack 是空的，字串才平衡。若遇到右括號時 stack 已經空了，或讀完時 stack 還有東西，字串就不平衡。',
])}
{lecture_program('完整程式：parChecker', 'parChecker：只處理小括號', 'par_checker',
                 note='前兩個字串平衡，輸出 true；"(()" 讀完時 stack 還剩一個左括號，")(" 第一個符號就是右括號而 stack 是空的，兩者都輸出 false。')}
<p>parChecker 遇到 <code>(</code> 就 push；其他符號都當成右括號處理。這裡的 <code>pop()</code> 只是移除符號，不需要它的值，因為 stack 裡放的一定是先前讀到的 <code>(</code>。如果字串還沒讀完 stack 就空了，表示右括號太多，函式立刻回傳 false；讀完之後，只有 stack 完全清空，字串才是平衡的。</p>
<p>下面的動畫已經能處理三種括號，下一小節會說明這個一般化的版本。</p>'''


def parens_general():
    return f'''<h3>一般化：三種括號混用</h3>
<p>在 C++ 中，方括號用於陣列索引，大括號界定區塊或初始化，小括號用於分組運算式與函式呼叫。只要每一種括號各自維持正確的開閉關係，就可以混合使用。下面的字串是平衡的：每個左符號都有對應的右符號，而且種類相符：</p>
<pre class="linear-pre">{{ {{ ( [ ] [ ] ) }} ( ) }}

[ [ {{ {{ ( ( ) ) }} }} ] ]

[ ] [ ] [ ] ( ) {{ }}</pre>
<p>下面這些則不平衡：</p>
<pre class="linear-pre">( [ ) ]

( ( ( ) ] ) )

[ {{ ( ) ]</pre>
<p>左符號一樣 push 到 stack 上，等待對應的右符號。遇到右符號時，唯一多出來的工作是確認它和 stack 頂端的左符號<strong>種類相符</strong>；不相符，字串就不平衡。整個字串處理完、stack 也清空了，字串才是平衡的。講義用一個輔助函式 <code>matches(open, close)</code> 做這個檢查：</p>
{snippet('matches：檢查左右符號是否同一種', MATCHES, kind='fragment',
         note='allLefts 與 allRights 把同一種括號放在相同的位置；兩個符號各自 find 到的位置相同，就是一對。')}
{lecture_program('完整程式：balanceChecker', 'balanceChecker：三種括號', 'balance_checker',
                 note='"{({([][])}())}" 平衡；"[{()]" 讀到最後的 ] 時，stack 頂端是 {，種類不合，所以回傳 false。可以在上方動畫輸入 [{()] 觀察這一步。')}
<p>處理程式語言的結構時常會用到 stack：幾乎任何記法都有需要成對、而且依正確順序配對的符號。</p>'''


# ---------------------------------------------------------------- P03 base conversion
def base_intro():
    return f'''<h3>二進位與「除以 2」</h3>
<p>電腦裡所有的值都以二進位數字，也就是一串 0 與 1 存放。我們平常用十進位表示整數；十進位的 $233_{{10}}$ 與它的二進位 $11101001_2$ 分別代表：</p>
<p class="linear-math">$$2\\times10^{{2}} + 3\\times10^{{1}} + 3\\times10^{{0}}$$
$$1\\times2^{{7}} + 1\\times2^{{6}} + 1\\times2^{{5}} + 0\\times2^{{4}} + 1\\times2^{{3}} + 0\\times2^{{2}} + 0\\times2^{{1}} + 1\\times2^{{0}}$$</p>
<p>把整數轉成二進位的方法叫 Divide by 2，它用 stack 記錄結果的每一位。演算法假設從一個大於 0 的整數開始，不斷除以 2，並記下每次的餘數。</p>
<p>第一次除以 2 的餘數說明這個數是偶數還是奇數：偶數的個位是 0，奇數的個位是 1。把結果看成一串數字，<strong>第一個算出的餘數其實是最後一位</strong>。</p>
{figure('divide')}
<p>這裡又出現了反轉的性質，表示 stack 很可能是合適的資料結構。下面的 <code>divideBy2()</code> 接收一個十進位數，不斷除以 2，把餘數 push 到 stack，最後依序 pop 組成二進位字串：</p>
{lecture_program('完整程式：divideBy2', 'divideBy2：十進位轉二進位', 'divide_by_2',
                 note='42 的二進位是 101010，31 是 11111。<code>to_string</code> 把 int 型別的餘數轉成字串，再接到 binString 後面。')}'''


def base_general():
    return f'''<h3>推廣到任意進位：baseConverter</h3>
<p>這個方法很容易推廣到其他進位。電腦科學中常用的除了二進位，還有八進位（base 8）與十六進位（base 16）。$233_{{10}}$ 的八進位是 $351_8$，十六進位是 $E9_{{16}}$，分別代表：</p>
<p class="linear-math">$$3\\times8^{{2}} + 5\\times8^{{1}} + 1\\times8^{{0}}$$
$$14\\times16^{{1}} + 9\\times16^{{0}}$$</p>
<p>只要把「除以 2」換成「除以 base」，<code>divideBy2()</code> 就能接收要轉換的進位。二到十進位最多需要 10 個數字，0 到 9 就夠用；超過十進位時，10 以上的餘數本身是兩位數，不能直接寫進結果，需要另外的符號。<code>digits</code> 字串用 A 到 F 表示 10 到 15，餘數就是 digits 的索引。</p>
{lecture_program('完整程式：baseConverter', 'baseConverter：十進位轉任意進位（2 到 16）', 'base_converter',
                 note='25 的二進位是 11001，十六進位是 19（1 × 16 + 9）。上方動畫可以選 base 16，觀察餘數 10 以上時 digits 的作用。')}
{quiz('qConvert', 'QUIZ · 八進位',
      '十進位的 25 寫成八進位是多少？', [
          (True, '<code>31</code>', '25 = 3 × 8 + 1，所以八進位是 31。在 C++ 原始碼中，整數常數 031 開頭的 0 代表八進位，它的值就是 25。'),
          (False, '<code>11001</code>', '11001 是 25 的二進位；這題問的是八進位。'),
          (False, '<code>19</code>', '19 是 25 的十六進位（1 × 16 + 9）。'),
          (False, '<code>13</code>', '25 % 8 = 1、3 % 8 = 3，餘數依產生順序是 1、3；直接接起來就忘了 stack 的反轉，正確結果要反過來讀。'),
      ])}'''


# ---------------------------------------------------------------- P04 expressions
def infix_paren():
    return f'''<h3>完全括號化</h3>
<p>寫 <code>B * C</code> 時，運算子 * 出現在兩個運算元之間，所以知道是 B 乘以 C；運算子夾在運算元中間的寫法叫<strong>中序</strong>（infix）。<code>A + B * C</code> 就有歧義了：+ 作用在 A 與 B，還是 * 作用在 B 與 C？每個運算子都有<strong>優先權</strong>（precedence level），優先權高的先算；只有括號能改變這個順序。乘除的優先權高於加減；優先權相同時，依<strong>結合律</strong>（associativity）由左到右計算。所以 <code>A + B * C</code> 先算 B 乘 C 再加 A；<code>(A + B) * C</code> 先算 A 加 B；<code>A + B + C</code> 先算左邊的 +。</p>
<p>電腦必須確切知道要做哪些運算、以什麼順序做。一種保證沒有歧義的寫法叫<strong>完全括號運算式</strong>（fully parenthesized expression）：每個運算子都有一對括號，括號決定運算的順序。例如 <code>A + B * C + D</code> 寫成 <code>((A + (B * C)) + D)</code>，表示先乘、再算左邊的加法；<code>A + B + C + D</code> 寫成 <code>(((A + B) + C) + D)</code>，因為加法由左往右結合。</p>
<h3>用括號的位置轉成前序與後序</h3>
<p>看 <code>(A + (B * C))</code> 中子式 <code>(B * C)</code> 的<strong>右括號</strong>：把 * 移到這個位置，再刪掉對應的左括號，得到 <code>B C *</code>，子式就轉成了後序。+ 也移到它的右括號、刪掉對應的左括號，就得到完整的後序式。若改成移到<strong>左括號</strong>的位置，得到的是前序。一對括號的位置，就是括號內運算子最後的位置。</p>
<div class="linear-figure-pair">{figure('post-move')}{figure('pre-move')}</div>
<p>所以不論運算式多複雜，都可以先依運算順序把它完全括號化，再依需要把每個運算子移到左括號（前序）或右括號（後序）的位置：</p>
{figure('full-paren')}'''


def infix_convert():
    trace = table(['token', 'opStack（top 在右）', 'postfixList'], [
        ('A', '', 'A'), ('*', '*', 'A'), ('B', '*', 'A B'),
        ('+', '+（* 優先權較高，先 pop 到輸出）', 'A B *'), ('C', '+', 'A B * C'),
        ('*', '+ *（* 比 + 高，直接 push）', 'A B * C'), ('D', '+ *', 'A B * C D'),
        ('結束', '依序 pop 剩下的運算子', 'A B * C D * +')])
    return f'''<h3>為什麼用 stack 保存運算子</h3>
<p>再看一次 <code>A + B * C</code>，它的後序是 <code>A B C * +</code>。運算元 A、B、C 的相對位置沒有改變，移動的只有運算子。由左往右，第一個出現的運算子是 +，但在後序中 + 排在最後，因為後面的 * 優先權比較高。<strong>原式中運算子的順序，在後序中反轉了</strong>。</p>
<p>處理運算式時，運算子的右運算元還沒讀到，運算子必須先存起來；而且因為優先權，存起來的運算子可能要反轉順序。所以用 stack 保存運算子，等到需要時再取出。</p>
<p><code>(A + B) * C</code> 的後序是 <code>A B + C *</code>。由左往右處理時同樣先看到 +；不同的是，讀到 * 的時候，+ 已經輸出了，因為括號讓它的優先權高於 *。轉換演算法讀到左括號時把它存起來，表示之後會有一個高優先權的運算子；這個運算子要等對應的右括號出現，才決定它的位置。右括號出現時，就從 stack 把運算子 pop 出來。</p>
<p>假設中序式是一串以空白分隔的 token，運算子有 *、/、+、-，以及左右括號。演算法的核心迴圈如下：運算元直接輸出，運算子在 stack 上等待，直到讀到優先權較低的運算子：</p>
{snippet('infixToPostfix 的核心迴圈', I2P_CORE, kind='fragment')}
{figure('i2p-trace')}
{fold('逐 token 追蹤 A * B + C * D 的文字表', trace)}
<p>下面的動畫可以逐步觀察三個例子；右側的程式是動畫所用的簡化流程。</p>'''


def infix_code():
    eval_steps = ol([
        '建立 <code>std::stack&lt;double&gt; operandStack</code>。',
        '用 <code>std::istringstream</code>（講義程式用 <code>stringstream</code>）切出 token，由左到右處理。',
        '若 token 是運算元，用 <code>stod</code> 把字串轉成數字，push 到 operandStack。',
        '若 token 是運算子 *、/、+、-，它需要兩個運算元：pop 兩次，<strong>第一次 pop 出來的是第二個運算元</strong>，第二次才是第一個運算元。計算後把結果 push 回去。',
        '整個運算式處理完，結果就在 stack 上，回傳 operandStack 的 top。',
    ])
    caret_note = ('右結合表示 2 ^ 3 ^ 2 = 2 ^ (3 ^ 2) = 512，而不是 (2 ^ 3) ^ 2 = 64。程式第二行的輸出 2 3 2 ^ ^ 就是先算 3 ^ 2。'
                  '只提高 ^ 的優先權還不夠，同優先權時要不要 pop 的條件也必須改。')
    return f'''<h3>infixToPostfix 完整程式</h3>
<p>完整的轉換器放在課程標頭 <code>pythonds3/cppds/expression.hpp</code>：用 stringstream 以空白切出 token，跑完核心迴圈後，把 stack 剩下的運算子全部 pop 到輸出，再把 postfixList 接成以空白分隔的字串。</p>
{details('expression.hpp 的 infixToPostfix', snippet('pythonds3/cppds/expression.hpp · infixToPostfix', I2P_HEADER, kind='header'))}
<p>prec 把 <code>(</code> 的優先權設成最低的 1：左括號留在 stack 裡時，任何運算子都不會因為優先權把它 pop 出去，它只會在讀到右括號時被移除。</p>
{lecture_program('完整程式：呼叫 infixToPostfix', 'include expression.hpp 後轉換兩個運算式', 'i2p_main',
                 note='token 之間必須有空白，程式才切得出來。第二個運算式的括號在後序中全部消失了。')}
<h3>後序求值</h3>
<p>接著計算一個已經是後序的運算式，stack 仍然是合適的資料結構。不過這一次，掃描時<strong>等待的是運算元</strong>，而不是轉換時的運算子。換個角度說：每讀到一個運算子，就拿最近的兩個運算元來計算。</p>
<p>以 <code>4 5 6 * +</code> 為例：由左往右先讀到 4 與 5，這時還不知道要拿它們做什麼，得等看到下一個符號。把它們放到 stack 上，若接下來是運算子，就能立刻取用。</p>
{figure('eval-1')}
<p>稍微複雜的例子是 <code>7 8 + 3 2 + /</code>。這裡有兩點要注意：第一，計算子式時，stack 會先變高、變矮、再變高；第二，除法要小心處理。後序只改變運算子的位置，運算元仍是原來的順序；從 stack pop 出除法的兩個運算元時，順序是反過來的。除法不滿足交換律，所以不能把兩個運算元的順序弄反。</p>
{figure('eval-2')}
{eval_steps}
<p>計算一個運算子需要一個小輔助函式 <code>doMath()</code>，把運算子套用到兩個運算元：</p>
{snippet('doMath：套用一個運算子', DO_MATH, kind='fragment')}
{details('expression.hpp 的 postfixEval', snippet('pythonds3/cppds/expression.hpp · postfixEval', POSTFIX_EVAL_HEADER, kind='header'))}
{lecture_program('完整程式：呼叫 postfixEval', 'include expression.hpp 後計算 7 8 + 3 2 + /', 'postfix_main',
                 note='結果 3 就是 (7 + 8) / (3 + 2)。postfixEval 回傳 double，值剛好是整數 3.0 時，cout 印成 3。')}
<p>轉換與求值兩個程式都假設輸入的運算式沒有錯誤。</p>
{quiz('qC1', 'QUIZ · 中序轉後序',
      '把中序式 <code>10 + 3 * 5 / ( 16 - 4 )</code> 轉成後序：', [
          (True, '<code>10 3 5 * 16 4 - / +</code>', '運算元直接輸出，運算子依優先權在 stack 中等待；括號讓 (16 - 4) 先處理成 16 4 -，接著才輪到 /，最後是 +。'),
          (False, '<code>10 3 5 * / 16 4 - +</code>', '這表示 / 在括號內的子式處理之前就輸出了；/ 的右運算元是整個 (16 - 4)，必須等它完成。'),
          (False, '<code>10 3 5 16 4 - / * +</code>', '這樣 * 被放到 / 的後面；* 與 / 優先權相同，由左往右結合，3 * 5 要先算。'),
          (False, '<code>10 3 + 5 * 16 4 - /</code>', '這違反了乘除優先於加法：10 + 3 不應該先算。'),
      ])}
{quiz('qC2', 'QUIZ · 後序求值',
      '計算後序式 <code>17 10 + 3 * 9 /</code> 的值：', [
          (True, '<code>9</code>', '依序計算：17 + 10 = 27；27 × 3 = 81；81 / 9 = 9。'),
          (False, '<code>15</code>', '運算子套用的順序或運算元弄錯了；每個運算子都作用在 stack 最上面的兩個值。'),
          (False, '<code>27</code>', '27 只是第一步 17 + 10 的結果。'),
          (False, '<code>81</code>', '81 是除以 9 之前的結果，還少了最後一步。'),
      ])}
<h3 id="linear-ex-caret">練習：加入次方運算子 ^</h3>
<p>擴充 <code>infixToPostfix()</code>，讓它能轉換 <code>5 * 3 ^ ( 4 - 2 )</code>。</p>
{snippet('練習：支援 ^ 的 infixToPostfix', CARET_EXERCISE, output='5 3 4 2 - ^ *', kind='exercise', out_tag='完成後的預期輸出')}
<p>提示：給 ^ 最高的優先權。因為 ^ 是<strong>右結合</strong>，讀到 ^ 時，只有當 stack 上運算子的優先權<strong>嚴格大於</strong> ^ 時才 pop。轉換結果 <code>5 3 4 2 - ^ *</code> 的值是 45。</p>
{fold('支援 ^ 的參考解答', run_card('infixToPostfix 加上右結合的 ^', 'caret_solution', note=caret_note))}'''


# ---------------------------------------------------------------- P05 queue
def queue_intro():
    return f'''<h3>front 與 rear</h3>
<p>queue 是一個有順序的集合，新元素從一端加入，這一端叫 <strong>rear</strong>；既有的元素從另一端移除，這一端叫 <strong>front</strong>。元素從 rear 進入後，一路往 front 移動，直到輪到它被移除。在集合中待得最久的元素位於 front。這個原則叫 <strong>FIFO</strong>（first in, first out，先進先出）。</p>
<p>最簡單的例子是排隊：排隊看電影、在超市排隊結帳、在餐廳排隊取餐。規矩的隊伍限制很嚴格，只有一個入口、一個出口；不能從中間插隊，也不能在輪到之前離開。</p>
{figure('queue')}
<p>電腦科學裡也常見 queue。作業系統用好幾種不同的 queue 管理電腦裡的行程（process）：接下來要執行什麼，通常由一個排隊演算法決定，目標是盡快執行程式，同時服務越多使用者越好。</p>
<h3>Queue ADT</h3>
{ul([
    '<code>std::queue&lt;T&gt; q;</code> 建立一個空的 queue。',
    '<code>push(item)</code> 把 item 加到 rear，回傳 <code>void</code>。',
    '<code>front()</code> 與 <code>back()</code> 讀取兩端的元素。',
    '<code>pop()</code> 移除 front 的元素，回傳 <code>void</code>。',
    '<code>empty()</code> 與 <code>size()</code> 檢查 queue 的狀態。',
])}
<p>需要被移除的那個值時，先呼叫 <code>front()</code>，再呼叫 <code>pop()</code>。對空的 queue 呼叫 <code>front()</code>、<code>back()</code> 或 <code>pop()</code> 都違反前提條件。下表把 <code>front()</code> 畫在左邊、<code>back()</code> 畫在右邊，和 STL 的一般看法一致：</p>'''


def queue_stl():
    trans = table(['std::queue&lt;T&gt;', '課程標頭 Queue&lt;T&gt;', '說明'], [
        ('<code>push(x)</code>', '<code>enqueue(x)</code>', '加到 rear'),
        ('<code>front()</code> 再 <code>pop()</code>', '<code>dequeue()</code>', 'dequeue 移除 front 並回傳它的值'),
        ('<code>empty()</code>', '<code>isEmpty()</code>', '是否為空'),
        ('<code>size()</code>', '<code>size()</code>', '元素個數'),
        ('<code>back()</code>', '沒有對應的方法', 'Queue&lt;T&gt; 不提供讀取 rear'),
    ])
    return f'''<h3>在 C++ 使用 std::queue</h3>
<p>C++ 標準函式庫的 <code>std::queue&lt;T&gt;</code> 用 <code>push</code> 加入，用 <code>front</code> 讀取，再用 <code>pop</code> 移除（回傳 <code>void</code>）；<code>back</code> 讀取 rear 的元素。以預設的 deque 為底層時，這些操作都是 $O(1)$。</p>
{snippet('std::queue 的基本用法', STL_QUEUE_SNIPPET, kind='fragment')}
{lecture_program('完整程式：使用 std::queue', 'std::queue&lt;string&gt; 的基本操作', 'stl_queue',
                 note='"4" 最先 push，所以在 front；pop 移除它之後，front 變成 "dog"。和 stack 的例子用同樣的三個字串，取出的順序正好相反。')}
<h3>課程標頭的 Queue&lt;T&gt;</h3>
<p>課程標頭 <code>pythonds3/cppds/queue.hpp</code> 為了作業使用 <code>enqueue</code>、會回傳值的 <code>dequeue</code> 與 <code>isEmpty</code>。它把 rear 放在 vector 的開頭、front 放在尾端：<code>dequeue</code> 是 <code>pop_back</code>，$O(1)$；<code>enqueue</code> 要 <code>insert(begin())</code>，把所有元素往後搬一格，$O(n)$。</p>
{trans}
{details('課程標頭 queue.hpp 的 Queue&lt;T&gt;', snippet('pythonds3/cppds/queue.hpp · Queue', QUEUE_HPP, kind='header'))}
{quiz('qQueue', 'QUIZ · queue 剩下哪些元素',
      '執行下列 queue 操作之後，queue 裡還有哪些元素？', [
          (True, '<code>{"dog", "3"}</code>', 'queue 是 FIFO：push 加到 rear，pop 移除 front 的 "hello"（回傳 void），剩下 "dog" 與 "3"。'),
          (False, '<code>{"hello", "dog"}</code>', '這是 pop 移除最後加入的元素（LIFO）的結果，那是 stack 的行為，不是 queue。'),
          (False, '<code>{"hello", "dog", "3"}</code>', '這是 pop 之前的狀態；queue::pop 會從 front 移除一個元素。'),
          (False, '<code>{"3"}</code>', '這表示 pop 了兩次，或 queue 只保留最後加入的元素。'),
      ], code='std::queue<std::string> q;\nq.push("hello");\nq.push("dog");\nq.push("3");\nq.pop();')}'''


# ---------------------------------------------------------------- P06 hot potato
def hp_intro():
    return f'''<h3>遊戲規則</h3>
<p>燙手山芋是一個兒童遊戲：小朋友圍成一圈，盡快把手上的東西傳給旁邊的人。遊戲在某個時刻停下，拿著山芋的人離開圓圈，其他人繼續玩，直到只剩一個人。</p>
{figure('potato-circle')}
<h3>用 queue 模擬圓圈</h3>
<p>模擬程式 <code>hotPotato</code> 接收一個 <code>vector&lt;string&gt;</code> 名單與次數 num。進行中的圓圈用 <code>std::queue&lt;string&gt;</code> 表示，函式回傳最後剩下的名字。</p>
<p>假設拿著山芋的人在 queue 的 front。傳一次山芋，模擬程式就把這個人從 front 移除，再立刻加到 rear，讓他排到隊伍最後面：</p>
{figure('potato-queue')}
<p>做完 num 次「移除再加入」之後，front 的人永久移除，開始下一輪。持續進行，直到只剩一個名字，也就是 queue 的大小為 1。</p>'''


def hp_code():
    return f'''<h3>hotPotato 完整程式</h3>
{lecture_program('完整程式：hotPotato', 'hotPotato：用 std::queue 模擬', 'hot_potato',
                 note='名字依給定的順序 push，所以第一個名字一開始在 <code>front()</code>。移動一位玩家，就是複製 <code>front()</code> 的值、push 到 rear，再 pop 掉原本的 front。')}
<p>每一輪傳 num 次，共要淘汰 n − 1 個人，所以整個模擬做了約 $(n-1)\\times num$ 次傳遞，每次傳遞是常數個 queue 操作，總成本是 $O(n \\cdot num)$。</p>
{fold('印出每一輪出局的人', run_card('hotPotato 加上一行輸出', 'hot_potato_trace',
      note='每一輪結束時印出 front 的名字再 pop。出局順序是 David、Kent、Jane、Bill、Brad，最後剩下 Susan。'))}
<h3 id="linear-ex-hp">練習：改用課程的 Queue&lt;T&gt;</h3>
<p>用課程標頭 <code>queue.hpp</code> 的 <code>Queue&lt;T&gt;</code> 實作同樣的模擬，並寫下兩套 API 怎麼對應。注意 <code>Queue&lt;T&gt;</code> 沒有 <code>front()</code>，但 <code>dequeue()</code> 會回傳被移除的元素，所以 STL 的「<code>front()</code> 再 <code>pop()</code>」在這裡合成一次 <code>dequeue()</code>；<code>push</code> 改成 <code>enqueue</code>。</p>
{fold('改用 Queue&lt;T&gt; 的參考解答', run_card('hotPotato：用 queue.hpp 的 Queue&lt;T&gt;', 'hot_potato_course',
      note='結果與 STL 版本相同。不過 Queue&lt;T&gt; 的 enqueue 是 O(n)，每次傳遞都要搬動整個 vector，這個版本比 std::queue 慢。'))}'''


# ---------------------------------------------------------------- P07 printer simulation
def printer_intro():
    return f'''<h3>問題與假設</h3>
<p>學生把列印工作送到實驗室共用的印表機，工作放進一個 queue，依先來先印的順序處理。平常每小時大約有 10 位學生在實驗室，每人在這段時間最多印兩次，每份工作 1 到 20 頁。實驗室的印表機每分鐘可以印 10 頁；切換成品質較好的模式時，每分鐘只能印 5 頁。印得慢可能讓學生等太久，該用哪一種速度？</p>
{figure('printer')}
<p>模擬需要表示學生、列印工作與印表機。學生送出列印工作時，工作加入印表機的等待佇列；印表機印完一份工作，就看 queue 裡還有沒有工作要處理。我們關心的是<strong>學生平均要等多久才拿到列印的東西</strong>，也就是工作在 queue 中平均等待的時間。</p>'''


def printer_body():
    steps = ol([
        '建立一個列印工作的 queue，一開始是空的。每個工作在抵達時會得到一個時間戳記（timestamp）。',
        '對每一秒（now）：'
        + ul(['有沒有新的列印工作產生？有的話，以 now 當時間戳記，把它加入 queue。',
              '如果印表機沒在忙，而且有工作在等：從 queue 取出下一個工作交給印表機；用 now 減掉時間戳記，得到這個工作的等待時間，加到 vector <code>waits</code> 留著計算；再依工作的頁數算出需要多少時間。',
              '必要時，印表機印一秒，需要的時間減少一秒。',
              '如果工作完成，也就是需要的時間減到 0，印表機就不忙了。']),
        '模擬結束後，計算記錄下來的等待時間的平均；要另外處理完全沒有樣本的情況。',
    ])
    whatif = ul([
        '人數增加 20 位：每小時約 (10 + 20) × 2 = 60 件，平均每 60 秒一件，<code>arrival</code> 改成 1 到 60。',
        '週末比較能容忍等待：模型可以不變，改變的是「等多久算太久」的判斷標準。',
        '平均頁數下降：把 <code>pages</code> 的範圍改小，例如 1 到 10。',
    ])
    return f'''<h3>主要模擬步驟</h3>
{steps}
<h3>C++ 實作：Task、Printer 與 simulation()</h3>
<p>C++17 的模型用 <code>Task</code> 值、<code>queue&lt;Task&gt;</code>，以及印表機裡的 <code>optional&lt;Task&gt;</code>。物件的擁有權由語言自動處理：整個模擬沒有原始的 <code>new</code> 或 <code>delete</code>，一次試驗結束時也不會留下沒釋放的工作。</p>
{snippet('Printer：印表機', PRINTER_CLASS, kind='fragment')}
<p><code>busy()</code> 看 optional 裡有沒有工作。<code>startNext()</code> 依頁數算出這份工作要印多少秒：頁數 × 60 ÷ 每分鐘頁數。<code>tick()</code> 把剩下的時間減一秒，工作完成時用 <code>reset()</code> 清空 optional。</p>
<p>每個工作也要記錄時間戳記，用來計算等待時間；時間戳記代表工作產生並放進印表機 queue 的時刻。</p>
{snippet('Task：列印工作', TASK_CLASS, kind='fragment')}
<p>等待的隊伍是 <code>std::queue&lt;Task&gt;</code>，裡面放的是值，不是指標：</p>
{snippet('主迴圈中與 queue 有關的步驟', PRINT_QUEUE, kind='fragment')}
<h3>用 mt19937 產生亂數</h3>
<p>C++ 的 <code>&lt;random&gt;</code> 把產生亂數分成兩部分。<strong>引擎</strong> <code>std::mt19937</code> 產生一長串看起來隨機的整數；<strong>分佈</strong> <code>std::uniform_int_distribution&lt;int&gt;(a, b)</code> 把引擎的輸出轉成 a 到 b 之間、每個值機率相同的整數。用法是把引擎傳給分佈：<code>pages(rng)</code> 每呼叫一次，引擎就前進一步，得到下一個值。</p>
<p>模擬中，<code>uniform_int_distribution&lt;int&gt;(1, 180)</code> 每秒產生 180 個等可能值中的一個；把其中一個值（180）當成「有新工作」，平均就是每小時 20 件。頁數由 <code>uniform_int_distribution&lt;int&gt;(1, 20)</code> 決定。引擎以固定的種子（seed）初始化，例如 <code>mt19937 rng(42)</code>，每次執行都得到同一串亂數，課堂示範才能重現。</p>
<p>完整的程式把這些組合起來。<code>simulation()</code> 跑指定的秒數，最後印出平均等待時間，以及時間到時還留在 queue 裡的工作數；同一個引擎以參考 <code>mt19937&amp;</code> 傳入，兩次模擬接續使用同一串亂數：</p>
{lecture_program('完整程式：印表機模擬', 'Task、Printer 與 simulation()', 'simulation',
                 note='第一行是每分鐘 5 頁、第二行是每分鐘 10 頁，各模擬一小時（3600 秒）。tasks remaining 是一小時結束時還在 queue 裡、沒有開始印的工作數。這一次的亂數下兩者的平均等待差不多，只跑一次還看不出速度的影響。')}
<h3>討論</h3>
<p>講義以每分鐘 5 頁跑了 10 次獨立的一小時試驗。因為模擬使用亂數，每次的結果都不同，平均等待時間的變化很大。把速度改成每分鐘 10 頁再跑 10 次，等待時間通常會下降：速度較快時，一小時內能完成更多工作。</p>
{details('完整程式：每種速度各跑 10 次', run_card('simulation() 各跑 10 次', 'simulation_trials',
      note='每分鐘 5 頁時，平均等待從約 37 秒到 245 秒，常有工作沒印完；每分鐘 10 頁時，10 次中有 8 次在 20 秒以內，只有偶爾因為短時間湧入較多工作而拉長。'))}
<p>我們要回答的問題是：把印表機切成品質較好、速度較慢的模式，是否還應付得了工作量。做法是寫一個模擬，把列印工作看成抵達時間與長度都隨機的事件。結果顯示，以每分鐘 5 頁列印時等待時間起伏很大，放慢印表機換取品質可能不是好主意：學生趕著上下一堂課，等不了那麼久。這是模型在上述到達率與頁數假設下的結果，和使用哪一種程式語言無關。</p>
<p>也可以模擬其他的工作量，例如：</p>
{ul(['選課人數增加 20 位會怎樣？', '週末的工作量可以容忍較長的等待，結論會不同嗎？', '平均列印頁數下降會怎樣？'])}
<p>這些問題都可以藉由修改模型的參數來測試。結論的可靠程度，取決於這些假設。</p>
{fold('三個問題各要改哪裡', whatif)}'''


# ---------------------------------------------------------------- P08 deque
def deque_intro():
    trans = table(['std::deque&lt;T&gt;', '課程標頭 Deque&lt;T&gt;', '課程版的成本'], [
        ('<code>push_front(x)</code>', '<code>addFront(x)</code>', '$O(1)$（vector 尾端 push_back）'),
        ('<code>push_back(x)</code>', '<code>addRear(x)</code>', '$O(n)$（insert(begin())）'),
        ('<code>front()</code> 再 <code>pop_front()</code>', '<code>removeFront()</code>', '$O(1)$（pop_back）'),
        ('<code>back()</code> 再 <code>pop_back()</code>', '<code>removeRear()</code>', '$O(n)$（erase(begin())）'),
        ('<code>empty()</code>／<code>size()</code>', '<code>isEmpty()</code>／<code>size()</code>', '$O(1)$'),
    ])
    return f'''<h3>兩端都能進出</h3>
<p>deque 也叫 double-ended queue（雙端佇列），是一個和 queue 類似的有序集合，有 front 與 rear 兩端。它的不同之處在於加入與移除不受限制：新元素可以加在 front 或 rear，既有元素也可以從任一端移除。因此一個 deque 就能當 stack 用，也能當 queue 用。</p>
{figure('deque')}
<h3>Deque ADT 與課程標頭</h3>
{ul([
    '<code>std::deque&lt;T&gt; d;</code> 建立一個空的 deque。',
    '<code>push_front(item)</code> 與 <code>push_back(item)</code> 分別加到兩端。',
    '<code>front()</code> 與 <code>back()</code> 讀取兩端的元素。',
    '<code>pop_front()</code> 與 <code>pop_back()</code> 移除兩端的元素，回傳 <code>void</code>。',
    '<code>empty()</code> 與 <code>size()</code> 檢查狀態。',
])}
{snippet('std::deque 的基本用法', STL_DEQUE_SNIPPET, kind='fragment')}
<p>課程標頭 <code>pythonds3/cppds/deque.hpp</code> 改為提供 <code>Deque&lt;T&gt;</code>，方法是 <code>addFront</code>、<code>addRear</code>，以及會回傳值的 <code>removeFront</code>／<code>removeRear</code> 與 <code>isEmpty</code>。它選擇的 vector 表示法讓其中一端的操作是 $O(n)$；這不是 <code>std::deque</code> 的複雜度。一般的 C++ 程式使用 <code>std::deque</code>；只有練習明確要求研究這種表示法與操作成本時，才用課程的 <code>Deque&lt;T&gt;</code>。</p>
{trans}
{details('課程標頭 deque.hpp 的 Deque&lt;T&gt;', snippet('pythonds3/cppds/deque.hpp · Deque', DEQUE_HPP, kind='header'))}
<p>下表把 <code>front()</code> 畫在左邊、<code>back()</code> 畫在右邊：</p>'''


def deque_pal():
    return f'''<h3>迴文檢查：palChecker</h3>
<p>迴文（palindrome）是正著讀和反著讀都一樣的字串，例如 radar、toot、madam。我們要寫一個演算法，輸入一串字元，檢查它是不是迴文。</p>
<p>做法是用 deque 存放字串的字元。由左到右處理字串，把每個字元加到 deque 的 rear；到這裡為止，deque 的用法就像普通的 queue。接著利用 deque 兩端的能力：front 是字串的第一個字元，rear 是最後一個字元。</p>
{figure('palindrome')}
<p>因為兩端的字元都能直接移除，就把它們拿出來比較，相同才繼續。若一路相同，最後 deque 不是空了，就是只剩一個字元，看原字串長度是偶數還是奇數而定。兩種情況下，字串都是迴文。</p>
{lecture_program('完整程式：palChecker', 'palChecker：用 std::deque 檢查迴文', 'pal_checker',
                 note='"lsdkjfskf" 第一次比較 l 與 f 就不同，回傳 false；"radar" 比較 r 與 r、a 與 a 之後只剩 d，回傳 true。while 的條件是 size() &gt; 1：剩下的一個字元是中點，不用再比。')}'''


# ---------------------------------------------------------------- EX / REF / recap
def exercises():
    return f'''<h3>講義的三個程式練習</h3>
<p>除了上面的選擇題，講義在各節留了三個寫程式的練習，題目與參考解答放在對應的小節：</p>
{ul([
    '<a href="#linear-ex-rev">用 stack 反轉字串</a>：寫出 revString，預期輸出 USYSN。',
    '<a href="#linear-ex-caret">加入次方運算子 ^</a>：讓 infixToPostfix 處理右結合的 ^，預期輸出 5 3 4 2 - ^ *。',
    '<a href="#linear-ex-hp">改用課程的 Queue&lt;T&gt;</a>：用 enqueue／dequeue 重寫 hotPotato，並寫下 API 的對應。',
])}'''


def reference():
    adts = table(['ADT', '進', '出', '順序', '典型應用'], [
        ('<strong>Stack</strong>', 'top', 'top', 'LIFO', '括號配對、進位轉換、undo、函式呼叫堆疊、DFS'),
        ('<strong>Queue</strong>', 'rear', 'front', 'FIFO', '排程、模擬（燙手山芋、印表機）、BFS'),
        ('<strong>Deque</strong>', '兩端', '兩端', '由使用者決定', '迴文、滑動視窗'),
    ])
    costs = table(['操作', 'vector 尾端', 'vector 開頭'], [
        ('加入／移除', '$O(1)$（加入為攤銷）', '$O(n)$（其餘元素整體搬移）'),
        ('課程標頭放在這一端的', 'Stack 的 top、Queue 的 front、Deque 的 front', 'Stack2 的 top、Queue 的 rear、Deque 的 rear'),
    ])
    return f'''<h3>參考資料</h3>
<p>課本：<em>Problem Solving with Algorithms and Data Structures using C++</em>（cppds），第 3 章 Linear Structures：<a href="https://runestone.academy/ns/books/published/cppds/index.html" target="_blank" rel="noopener">Runestone 線上版</a>。</p>
<h3>三種 ADT 對照</h3>
{fold('三種線性 ADT 一次比較', adts)}
{fold('課程標頭的實作成本（以 vector 為底）', costs + '<p>STL 的 <code>std::stack</code>、<code>std::queue</code>、<code>std::deque</code> 預設都以分段連續儲存的 deque 為底層，兩端的操作都是 $O(1)$。</p>')}'''


def recap():
    qa = [
        ('為什麼 std::stack 的 pop() 不回傳被移除的值？',
         '<p>如果 pop 要回傳值，就得先把元素複製出來再移除。複製若在途中失敗（例如丟出例外），元素已經從 stack 拿掉，卻沒有交到呼叫者手上，資料就遺失了。STL 把「讀取」與「移除」拆成 top() 與 pop() 兩步，讀取失敗時 stack 仍保持原狀。課程標頭的 Stack&lt;T&gt; 為了和 Python 版課本一致，pop() 會回傳值。</p>'),
        ('對空的 stack 或 queue 呼叫 top()、front() 或 pop() 會怎樣？',
         '<p>這違反前提條件，屬於未定義行為：程式可能當掉，也可能讀到無意義的值而繼續執行，錯誤很難追。呼叫之前先用 empty() 檢查，或像 parChecker 那樣，在 pop 之前先處理 stack 為空的情況。</p>'),
        ('std::stack 的底層可以換成 vector 嗎？',
         '<p>可以，寫成 <code>std::stack&lt;int, std::vector&lt;int&gt;&gt;</code>，只要底層容器提供 back、push_back、pop_back。std::queue 需要從前端移除，要求 front 與 pop_front，所以不能用 vector，可以用預設的 deque 或 list。這也說明了 ADT 與實作分離：介面不變，底層可以換。</p>'),
        ('中序轉後序時，為什麼左括號的優先權設成最低？',
         '<p>左括號在 stack 裡代表一個還沒結束的子式。把它的優先權設成最低，任何運算子進來時都不會因為「優先權大於等於自己」而把它 pop 出去；它只會在讀到對應的右括號時被移除，括號內的運算子就不會和括號外的混在一起。</p>'),
        ('後序求值時，pop 出來的兩個運算元為什麼順序很重要？',
         '<p>後序只改變運算子的位置，運算元仍是原來的順序，所以先 push 的是左運算元。從 stack pop 時順序相反：先出來的是右運算元（operand2），後出來的才是左運算元（operand1）。加法與乘法看不出差別，減法與除法弄反就會算錯，例如 15 / 5 會變成 5 / 15。</p>'),
        ('模擬每次跑出來的數字都不一樣，要怎麼下結論？',
         '<p>單次結果受亂數影響很大，應該跑多次獨立試驗，觀察平均值與變化範圍，再比較不同設定。固定種子是為了讓同一個實驗能重現，方便除錯與說明；比較設定時，也可以換幾個不同的種子，確認結論不是某一串亂數造成的。</p>'),
    ]
    faq = ''.join(details(f'{q}（補充）', a, cls='linear-detail linear-faq') for q, a in qa)
    return f'''{ul([
    '線性結構中的元素依加入的順序排列；stack、queue、deque 的差別在於從哪一端加入、從哪一端移除。',
    'stack 只在 top 加入與移除（LIFO），移除的順序是加入順序的反向；凡是「產生順序和使用順序相反」的問題，都可以考慮 stack。',
    'std::stack 是容器轉接器：push、top、pop、empty、size；pop() 回傳 void，需要值時先讀 top()。課程標頭 Stack&lt;T&gt; 用 peek()、isEmpty()，pop() 會回傳值。',
    '把 top 放在 vector 開頭的 Stack2 行為一樣正確，但 push 與 pop 都變成 $O(n)$：相同的 ADT 行為，不代表相同的成本。',
    '括號配對：左括號 push；右括號 pop，並檢查種類；讀完時 stack 必須為空。',
    '進位轉換：反覆除以 base，餘數 push 到 stack，再依序 pop 得到由高位到低位的結果；digits 字串處理 10 以上的餘數。',
    '中序轉後序時，運算子在 stack 中等待，比自己優先權高或相同的先 pop 到輸出；後序求值時，運算元在 stack 中等待，第一次 pop 出來的是右運算元。',
    'queue 從 rear 加入、從 front 移除（FIFO）；std::queue 用 push、front、back、pop，課程標頭 Queue&lt;T&gt; 用 enqueue、dequeue、isEmpty。',
    'hot potato 把「傳一次」模擬成 front 移到 rear；印表機模擬用 queue 保存等待的工作，用 mt19937 與 uniform_int_distribution 產生隨機事件，結論取決於模型的假設。',
    'deque 兩端都能加入與移除；std::deque 兩端都是 $O(1)$，迴文檢查從兩端各取一個字元比較。',
], cls='linear-ul linear-recap')}
<h3>常見疑問</h3>
{faq}'''


def sections():
    return {
        'linear-prologue': prologue(),
        'linear-stack-intro': stack_intro(),
        'linear-stack-stl': stack_stl(),
        'linear-stack-ex': stack_exercise(),
        'linear-parens': parens(),
        'linear-parens-general': parens_general(),
        'linear-base-intro': base_intro(),
        'linear-base-general': base_general(),
        'linear-infix-paren': infix_paren(),
        'linear-infix-convert': infix_convert(),
        'linear-infix-code': infix_code(),
        'linear-queue-intro': queue_intro(),
        'linear-queue-stl': queue_stl(),
        'linear-hp-intro': hp_intro(),
        'linear-hp-code': hp_code(),
        'linear-printer-intro': printer_intro(),
        'linear-printer': printer_body(),
        'linear-deque-intro': deque_intro(),
        'linear-deque-pal': deque_pal(),
        'linear-exercises': exercises(),
        'linear-reference': reference(),
        'linear-recap': recap(),
    }


STYLE = """<style id="linear-depth-style">
.linear-detail{margin:1rem 0;border:1px solid var(--card-border);border-radius:8px;background:var(--card);}
.linear-detail>summary{cursor:pointer;padding:.9rem 1rem;font-weight:600;line-height:1.6;}
.linear-detail-body{padding:0 1rem 1rem;min-width:0;}
.linear-detail-body .pseudo-code{max-width:100%;overflow-x:auto;}
.linear-detail-body .cmp-table{min-width:460px;}
.linear-ul,.linear-ol{padding-left:1.4rem;margin:.4rem 0 1rem;line-height:1.9;}
.linear-ul li,.linear-ol li{margin:.25rem 0;}
.linear-ol .linear-ul{margin:.3rem 0;}
.linear-pre{font-family:'JetBrains Mono',monospace;font-size:.85rem;background:var(--card);border:1px solid var(--card-border);border-radius:8px;padding:.7rem 1rem;overflow-x:auto;white-space:pre;margin:.6rem 0 1rem;}
.linear-math{overflow-x:auto;}
.quiz-box .linear-quiz-code{font-size:.8rem;margin:.2rem 0 .8rem;max-width:100%;overflow-x:auto;}
.quiz-opt .opt-text{min-width:0;overflow-wrap:anywhere;}
</style>"""
