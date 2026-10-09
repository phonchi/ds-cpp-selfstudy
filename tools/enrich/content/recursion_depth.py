"""Chapter 6 (recursion.html) section bodies. Each value of sections() fills one <!-- gen:NAME --> block.

Lecture text and code follow 06_Recursion.ipynb; header code follows pythonds3/cppds/maze.hpp.
Expected outputs come from compiling the programs (see recursion_programs.OUT).
"""
from html import escape
from enrich_lib import hl
from content.recursion_figures import figure
from content.recursion_programs import *  # noqa: F401,F403
from content import recursion_widgets as W


# ---------------------------------------------------------------- helpers (same conventions as chapter 4)
def details(summary, body, cls='rec-detail', did=''):
    ident = f' id="{did}"' if did else ''
    return f'<details class="{cls}"{ident}><summary>{summary}</summary><div class="rec-detail-body">{body}</div></details>'


def fold(title, body, did=''):
    """Content that the lecture does not cover: collapsed and labelled （補充）."""
    return details(title + '（補充）', body, did=did)


def table(headers, rows):
    return ('<div style="overflow-x:auto"><table class="cmp-table"><thead><tr>'
            + ''.join(f'<th>{h}</th>' for h in headers) + '</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{v}</td>' for v in r) + '</tr>' for r in rows)
            + '</tbody></table></div>')


def quiz(qid, label, question, options):
    """options: [(correct, text, feedback)], four per quiz; the page shuffles option order at load time."""
    assert len(options) == 4 and sum(ok for ok, _, _ in options) == 1, qid
    opts = ''.join(
        f'<div class="quiz-opt" data-correct="{"true" if ok else "false"}" data-fb="{escape(fb, quote=True)}" '
        f'onclick="quizCheck(\'{qid}\', this)"><span class="opt-letter">({chr(65 + i)})</span> <span class="opt-text">{text}</span></div>'
        for i, (ok, text, fb) in enumerate(options))
    return (f'<div class="quiz-box">\n  <div class="quiz-label">{label}</div>\n  <p>{question}</p>\n'
            f'  <div class="quiz-options" id="{qid}Options">\n    {opts}\n  </div>\n'
            f'  <div class="quiz-feedback" id="{qid}Feedback"></div>\n</div>')


def _expected_attr(output):
    return ' data-expected="' + escape(output + '\n', quote=True).replace('\n', '&#10;') + '"'


def _expected_out(output, label='預期輸出'):
    return (f'<div class="expected-out"><span class="eo-tag">{label}</span><pre>'
            + escape(output) + '</pre></div>')


def snippet(label, code, output=None, note=None, kind=None):
    """Code card. kind: run | fragment | compile-error | exercise | header (chapter-3 convention);
    a run block carries data-expected with the exact stdout."""
    if kind is None:
        kind = 'run' if output is not None and 'int main' in code else 'fragment'
    attrs = f' data-cpp="{kind}"' + (_expected_attr(output) if kind == 'run' and output is not None else '')
    parts = ['<div class="deck-extra">', f'  <div class="dx-label">{label}</div>',
             f'  <div class="pseudo-code" style="font-size:.8rem;"{attrs}>{hl(code)}</div>']
    if output is not None:
        parts.append('  ' + _expected_out(output))
    if note:
        parts.append(f'  <p class="dx-note">{note}</p>')
    parts.append('</div>')
    return '\n'.join(parts)


def lecture_program(summary, label, code, output, note=None):
    """Lecture full program: collapse the code, keep the expected output and the note visible."""
    card = snippet(label, code, kind='run').replace('data-cpp="run"', 'data-cpp="run"' + _expected_attr(output), 1)
    out = _expected_out(output)
    if note:
        out += f'<p class="dx-note">{note}</p>'
    return details(summary, card) + out


def silent_program(label, code, note):
    """A complete program whose correct run prints nothing (assert-based checks)."""
    return ('<div class="deck-extra">\n'
            f'  <div class="dx-label">{label}</div>\n'
            f'  <div class="pseudo-code" style="font-size:.8rem;" data-cpp="run" data-expected="">{hl(code)}</div>\n'
            f'  <p class="dx-note">{note}</p>\n</div>')


def ul(items, cls='rec-ul'):
    return f'<ul class="{cls}">' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'


def ol(items):
    return '<ol class="rec-ul">' + ''.join(f'<li>{x}</li>' for x in items) + '</ol>'


SKIPPED = '<p class="rec-skip">上課時略過本節，留給自學。</p>'
TURTLE_NOTE = ('<div class="warn-box"><b>這些程式需要另外安裝圖形函式庫。</b>'
               'cppds 的 C++ 範例使用只有標頭檔的 <code>CTurtle.hpp</code>：<code>cturtle::TurtleScreen</code> 負責繪圖視窗，'
               '<code>cturtle::Turtle</code> 在視窗裡移動。課程的 notebook 只執行主控台程式，所以本節的 CTurtle 程式只供閱讀，不會執行。'
               '想在自己的電腦上執行，要另外取得 <code>CTurtle.hpp</code>，放在原始檔旁邊，再編譯成桌面程式。'
               '本頁的互動圖用瀏覽器的 canvas 畫出同樣的圖形，不需要安裝。</div>')


# ---------------------------------------------------------------- P00
def prologue():
    q = quiz('qSumCalls', 'QUIZ · 數呼叫次數',
             '用本頁的 <code>listSum</code> 計算 <code>{2, 4, 6, 8, 10}</code>。<code>listSumFrom</code> 總共被呼叫幾次（包含 <code>listSum</code> 發出的第一次）？', [
                 (True, '6 次', 'index 依序是 0、1、2、3、4、5。前五次各處理一個元素，第六次 index == numList.size()，是回傳 0 的 base case。'),
                 (False, '5 次', '五個元素各一次之後，還要再呼叫一次 index 等於 size() 的 base case，才會開始回傳。'),
                 (False, '4 次', '這是「只剩一個元素就停」的版本中，第一次之後的遞迴呼叫次數。本頁的 base case 是空的範圍，要多走到尾端。'),
                 (False, '30 次', '呼叫次數只跟元素個數有關，跟元素的值或總和 30 無關。'),
             ])
    return f'''<p><strong>遞迴</strong>（recursion）是一種解題方法：把問題<strong>拆成越來越小的子問題</strong>，直到子問題小到可以直接解決。寫成程式時，通常就是函式呼叫自己。有些問題用迴圈很難寫，用遞迴卻能寫得簡潔。</p>
<h3>先用迴圈：計算 vector 的總和</h3>
<p>要算 <code>{{1, 3, 5, 7, 9}}</code> 的總和，迴圈版用一個<strong>累加變數</strong> <code>theSum</code>：從 0 開始，把每個數依序加進去，迴圈結束時 <code>theSum</code> 就是總和。</p>
{lecture_program("講義完整程式：迴圈版 listSum", "講義 06 · 用累加變數求和", LISTSUM_ITER, OUT['listsum_iter'],
                 note="第一行是 1 + 3 + 5 + 7 + 9 = 25；空的 vector 沒有元素可加，theSum 維持 0。參數用 const 參考傳入，不會複製 vector，也保證函式不會修改它。")}
<h3>不用迴圈：完全括號化的運算式</h3>
<p>如果不能用迴圈，要怎麼加總？先想起加法是「兩個數」的運算。把整串加法改寫成<strong>完全括號化的運算式</strong>（fully parenthesized expression），每一對括號裡只做一次兩數相加：</p>
{figure('eq1')}
<p>最裡面的 (7 + 9) 不需要迴圈或任何特殊結構就能算。算完之後換成 16，式子少了一層括號，形狀卻沒變。照這個方法一路化簡：</p>
{figure('eq2')}
<p>每一步都在解一個「比原本少一項」的同型問題。這就是遞迴的想法：相信較短的問題有辦法解決，再用它的答案組出原本問題的答案。</p>
<h3>遞迴版：listSumFrom</h3>
<p>改用 C++ 的 vector 描述同一件事：<strong>從索引 index 開始的總和</strong>，等於 <code>numList[index]</code> 加上從 <code>index + 1</code> 開始的總和。當 <code>index == numList.size()</code> 時，剩下的範圍是空的，總和是 0。每次呼叫都只傳同一個 vector 和一個索引，不必配置新的子 vector。</p>
{figure('eq3')}
{lecture_program("講義完整程式：遞迴版 listSum", "講義 06 · listSumFrom 與 listSum", LISTSUM_REC, OUT['listsum_rec'],
                 note="輸出和迴圈版相同。listSum 只是包裝：從索引 0 開始呼叫 listSumFrom。")}
{ul(['<code>listSumFrom</code> 在 <code>index == numList.size()</code> 時停止。這個 base case 代表「剩下的範圍是空的」，總和為 0，所以 <code>listSum({})</code> 也能安全地回傳 0。',
     '遞迴呼叫把 <code>index</code> 加一。同一個 vector 以 <code>const</code> 參考傳下去，遞迴過程中不會被複製，也不會被修改。'])}
<h3>展開與回傳</h3>
<p>下圖是加總 {{1, 3, 5, 7, 9}} 所需的一連串遞迴呼叫（圖中的 sum(3,5,7,9) 表示「從 3 開始到結尾的總和」）。把這串呼叫看成一連串的化簡：每次呼叫都把問題縮短一項。</p>
{figure('sum')}
<p>問題簡化到不能再簡單時，就開始把各個小問題的答案組合起來，一路回到最初的問題：</p>
{figure('sum2')}
<p>下面的動畫把同一件事拆成一步一步：先往下展開，碰到 base case 之後再一層層回傳。按「→ 單步」可以停在任何一步。</p>
{W.w_sum()}
{q}
{fold("遞迴和迴圈可以互換嗎", "<p>可以。凡是遞迴能算的，迴圈都能算，反過來也一樣；遞迴時由系統替你保存每一層的狀態，改寫成迴圈時就要自己保存，例如用一個 stack。遞迴的好處是讓程式的形狀跟問題的定義一致：listSumFrom 的兩行幾乎就是上面那條分段定義。後面的樹、分治與回溯問題，用遞迴寫特別自然。</p>")}'''


# ---------------------------------------------------------------- P01
def laws():
    cards = '''<div class="viz-panel">
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1rem;">
      <div class="info-card"><div class="ic-title">法則 1</div>
        <div style="font-size:.95rem;line-height:1.9;"><strong>必須有 base case</strong><br>
        <span style="color:var(--muted);font-size:.85rem;">小到能直接回答的情況（listSumFrom：索引到達尾端，空範圍的總和為 0）。</span></div></div>
      <div class="info-card"><div class="ic-title">法則 2</div>
        <div style="font-size:.95rem;line-height:1.9;"><strong>必須改變狀態，朝 base case 前進</strong><br>
        <span style="color:var(--muted);font-size:.85rem;">每次呼叫都要縮小問題（未處理的範圍變短、n 變小）。</span></div></div>
      <div class="info-card"><div class="ic-title">法則 3</div>
        <div style="font-size:.95rem;line-height:1.9;"><strong>必須呼叫自己</strong><br>
        <span style="color:var(--muted);font-size:.85rem;">相信較小的問題已經解決，再用它組合出大問題的答案。</span></div></div>
    </div>
  </div>'''
    q1 = quiz('qLaws', 'QUIZ · 抓出壞遞迴', '<code>int f(int n) { return n + f(n - 1); }</code> 違反了哪條法則？執行會怎樣？', [
        (True, '缺 base case，最後 stack overflow', '沒有終止條件，每次呼叫都在 call stack 疊一層新 frame，直到把 stack 記憶體用完（C++ 通常直接 segfault）。'),
        (False, '沒有呼叫自己', '它有呼叫自己（法則 3 沒問題），缺的是法則 1。'),
        (False, '沒有縮小問題', 'n - 1 確實在縮小；問題是縮到底也沒有停下來的條件。'),
        (False, '沒有違反，n 減到 0 就會停', 'n 減到 0 之後還會繼續呼叫 f(-1)、f(-2)……，沒有任何條件讓它停下。'),
    ])
    q2 = quiz('qFact', 'QUIZ · 階乘的 base case',
              '要寫遞迴的 <code>fact(n)</code>，回傳 n × (n−1) × (n−2) × …，並規定 0 的階乘是 1。哪一個 base case 最合適，而且最有效率？', [
                  (True, '<code>n &lt;= 1</code>', '0! 與 1! 都是 1。這個條件讓正整數在 n = 1 就停下，fact(0) 也能正確回傳 1。'),
                  (False, '<code>n == 0</code>', '結果正確，但 n 為正整數時，會多一次 fact(0) 的呼叫才停下。'),
                  (False, '<code>n == 1</code>', '題目規定 fact(0) 要回傳 1，這個條件處理不到 n = 0，會一路呼叫 fact(-1)、fact(-2)……。'),
                  (False, '<code>n &gt;= 0</code>', '這是在檢查輸入是否合法，不是終止條件：所有非負整數都會在第一次呼叫就停下，算不出階乘。'),
              ])
    return f'''{cards}
<p>就像艾西莫夫小說裡的機器人要遵守三大法則，所有遞迴演算法也必須遵守下面三條法則。寫完遞迴之後，用它們逐條檢查。</p>
<h3>三條法則套在 listSumFrom 上</h3>
{ol(['<strong>base case</strong> 是小到可以直接解決的問題。listSumFrom 的 base case 是剩下的範圍為空（<code>index == numList.size()</code>），總和為 0。',
     '<strong>改變狀態</strong>是指朝 base case 前進。listSumFrom 不動 vector，只把 <code>index</code> 加一，所以每次遞迴呼叫，未處理的範圍都短一項。',
     '最後一條法則是演算法必須<strong>呼叫自己</strong>，這正是遞迴的定義。'])}
<h3>用自己解決自己，為什麼不會繞圈？</h3>
<p>學寫函式時，我們學到可以把大問題拆成小問題，每個小問題各寫一個函式。講到遞迴，聽起來像在繞圈子：要用一個函式解決問題，這個函式卻靠呼叫自己來解決。關鍵在法則 2：每次呼叫自己時，問題都比原本<strong>更小、更容易</strong>，而且一定會碰到可以直接回答的 base case。</p>
{q1}
{q2}'''


# ---------------------------------------------------------------- P02
def tostr():
    rev_note = ('用三法則檢查：base case 是長度不超過 1，空字串與單一字元本身就是自己的反轉；'
                '<code>s.substr(1)</code> 每次少一個字元，確實朝 base case 前進；而且它呼叫自己。'
                '跟 toStr 是同一個骨架：<strong>把「接上字元」延後到遞迴回來之後</strong>，順序就自動反過來。執行時沒有輸出，表示兩個 assert 都通過。')
    q_rev = quiz('qRevBase', 'QUIZ · reverse 的 base case',
                 '哪一個 base case 能讓遞迴的 <code>reverse(string s)</code> 同時正確處理空字串與單一字元？', [
                     (True, '<code>if (s.size() &lt;= 1) return s;</code>', '兩種輸入本身就是自己的反轉，空字串的情況也安全。'),
                     (False, '<code>if (s.size() == 1) return s;</code>', '處理得了單一字元，卻漏掉空字串；從空字串繼續取 s[0] 或遞迴下去就會出錯。'),
                     (False, '<code>if (s.empty()) return s[0];</code>', '空字串沒有索引 0 的元素。'),
                     (False, '<code>if (s.size() &gt;= 1) return s;</code>', '所有非空字串都會立刻停下，長度超過 1 的字串永遠不會被反轉。'),
                 ])
    q_swap = quiz('qRevRec', 'QUIZ · 換個接法', '把最後一行改成 <code>return s[0] + reverse(s.substr(1));</code>，會得到什麼？', [
        (True, '原字串，一點都沒反', '頭一個字元接在「前面」，就維持原本的順序。反轉的關鍵是把 s[0] 排到遞迴結果的後面：接的位置決定順序。'),
        (False, '一樣是反轉', '接的順序就是輸出的順序：s[0] 在前，結果就以 s[0] 開頭，沒有反轉。'),
        (False, '編譯錯誤', 'char 與 string 可以用 + 串接，語法沒有問題；這是邏輯上的差異，編譯器不會攔。'),
        (False, '無窮遞迴', 'substr(1) 仍然每次少一個字元，一樣會走到 base case，只是接的順序不同。'),
    ])
    return f'''<p>假設要把整數轉成 2 到 16 進位之間某種進位的字串。例如把整數 10 轉成十進位的 "10"，或二進位的 "1010"。這個問題有很多種解法，上一章用 stack 就做過一次；用遞迴寫則特別簡潔。</p>
<h3>找出 base case：小於進位的數</h3>
<p>以十進位的 769 為例。先準備一串字元 <code>convertString = "0123456789"</code>，對應前 10 個數字。小於 10 的數很容易轉換：直接用它當索引查表。</p>
<p>如果能把 769 拆成 7、6、9 三個一位數，轉成字串就很簡單。「小於進位的數」聽起來就是個好的 base case。確定 base case 之後，整個演算法有三個部分：</p>
{ol(['把原本的數拆成一連串的一位數。', '用查表把每個一位數轉成字串。', '把這些一位數的字串接成最後的結果。'])}
<h3>朝 base case 前進：整數除法</h3>
<p>下一步要決定怎麼改變狀態、朝 base case 前進。能讓數字變小的運算，最可能是除法與減法。減法也許可行，但不清楚該減什麼；整數除法加上餘數，方向就很明確。</p>
<p>769 除以 10，商 76、餘數 9，同時得到兩個有用的結果：餘數小於進位，可以馬上查表轉成字串；商比原本的數小，往「只剩一個小於進位的數」的 base case 前進了一步。接著把 76 再除以 10，得到 7 與 6：</p>
{figure('num2str')}
<p>要記住的數字，都在圖右側的餘數格裡。</p>
<h3>講義程式：toStr</h3>
{lecture_program("講義完整程式：toStr", "講義 06 · 任意進位（2 到 16）", TOSTR_MAIN, OUT['tostr'],
                 note="1453 = 5 × 256 + 10 × 16 + 13，三個位數 5、10、13 查表後是 5、A、D。<code>if (n &lt; base)</code> 檢查 base case：一旦 n 小於要轉換的進位，就停止遞迴，直接從 convertString 取出字元。else 分支同時滿足第二與第三條法則：用除法縮小問題，並呼叫自己。")}
<h3>追蹤 toStr(10, 2)</h3>
<p>再追蹤一次，這次把 10 轉成二進位字串 "1010"：</p>
{figure('num2str2')}
<p>餘數產生的順序看起來是反的，但結果是對的：程式<strong>先</strong>做遞迴呼叫，等它回傳之後，<strong>才</strong>接上餘數的字元。如果把這兩件事的順序對調，先接上查到的字元、再處理商，得到的字串就會倒過來。把串接延後到遞迴呼叫回來之後，結果就是正確的順序。這和上一章討論的 stack 是同一個道理。</p>
<p>在下面的動畫中輸入其他數字或換成二進位、十六進位，觀察每一層何時展開、何時接上自己的餘數。</p>
{W.w_tostr()}
<h3>講義練習：用遞迴反轉字串</h3>
<p>寫一個遞迴函式，接收一個字串，回傳順序相反的新字串。講義的程式挖了兩個空格，先自己想想再看解答。</p>
{snippet("講義 06 · 練習：填入兩個空格", REVERSE_BLANK, kind='exercise', note="照原樣編譯會失敗：<code>____</code> 是要填的空格。")}
{details("參考解答", silent_program("reverse：剩下的部分先反轉，再接上第一個字元", REVERSE_SOLVED, rev_note))}
{q_rev}
{q_swap}'''


# ---------------------------------------------------------------- P03
def frames():
    return f'''<p>假設在 toStr 裡不做遞迴呼叫，而是把查到的字元推入一個 stack。用 STL 的 <code>stack</code>，就能用一個存放字元的顯式堆疊取代遞迴：</p>
{lecture_program("講義完整程式：用 stack 取代遞迴", "講義 06 · 顯式堆疊版 toStr", TOSTR_STACK, OUT['tostr_stack'],
                 note="輸出和遞迴版相同。第一個迴圈從最低位開始，把每個餘數字元推入 rStack；第二個迴圈從頂端依序取出，最高位就排在最前面。")}
<h3 id="dx-fr">顯式堆疊裡放了什麼</h3>
<p>每做一次除法，就推入一個字元。回到前面轉換 10 的例子，除完四次之後，堆疊長這樣：</p>
{figure('stack')}
<p>接著只要把字元一個個 pop 出來接成字串，就得到 "1010"。</p>
<h3>C++ 怎麼實作遞迴呼叫</h3>
<p>上面的例子說明了 C++ 實作遞迴呼叫的方式。對每一個進行中的函式呼叫，執行環境都維護一個 <strong>stack frame</strong>，裡面放著這次呼叫的參數、區域變數與返回資訊。函式回傳時，回傳值留在堆疊頂端，讓呼叫它的函式取用。下圖是 return 之後的呼叫堆疊：</p>
{figure('stack2')}
<p>toStr(2 / 2, 2) 回傳 "1"。這個值代回 toStr(1, 2) + convertString[2 % 2]，得到 "10"，之後較早的呼叫才繼續依序回傳。</p>
<p>這樣看來，C++ 的呼叫堆疊取代了我們剛才明確使用的 stack。在 vector 加總的例子裡，也可以把堆疊上的回傳值想成取代了累加變數的角色。</p>
<p>stack frame 也為函式的變數提供了<strong>作用域</strong>。雖然一再呼叫的是同一個函式，每次呼叫都會建立新的作用域，存放這次呼叫自己的區域變數：toStr(10, 2) 與 toStr(5, 2) 各有一個 n，彼此不會互相覆蓋。</p>
<h3>動畫：toStr(10, 2) 的呼叫堆疊</h3>
<p>按「→ 單步」看每一次呼叫推入一個 frame，碰到 base case 之後再一格一格彈出。第 5 步就是上圖的狀態。</p>
{W.w_frames_tostr()}
<h3>印出遞迴深度</h3>
<p>在函式裡用一個全域變數記錄目前是第幾次呼叫，就能在輸出中看到堆疊長高的過程。</p>
{lecture_program("講義程式：印出遞迴深度（上課略過）", "講義 06 · 用 depth 追蹤呼叫", TOSTR_DEPTH, OUT['tostr_depth'],
                 note="四次呼叫的 n 依序是 10、5、2、1，n 每除一次 2 就多一層 frame。最深的那層先回傳 \"1\"，回程時再依序接上 0、1、0。這裡的 depth 只增不減，所以它記錄的是「第幾次呼叫」；在這條單一路徑上，剛好也等於深度。")}
{fold("fact(4) 的呼叫堆疊動畫，以及 stack overflow", "<p>另一個常見的例子是階乘。fact(4) 要等 fact(3)，fact(3) 要等 fact(2)……每一層都在堆疊上留下一個 frame，直到 fact(1) 回傳 1，再一路乘回來。</p>" + W.w_fact())}'''


# ---------------------------------------------------------------- P04
def viz():
    return f'''{SKIPPED}
<p>有時候很難在腦中想像遞迴函式到底在做什麼，這也是遞迴不容易掌握的原因之一。本節用遞迴畫出一些圖形。看著圖形一步步成形，比較容易看清遞迴的過程。</p>
<h3>CTurtle 程式要另外安裝</h3>
{TURTLE_NOTE}
<h3>遞迴畫螺旋</h3>
<p>先看一個簡單的例子：用遞迴畫螺旋。base case 是要畫的線段長度減到 0 或以下。長度大於 0 時，讓烏龜往前走 length 單位、右轉 90 度，再用短一點的長度呼叫自己。</p>
{snippet("講義 06 · spiral（CTurtle，需另外安裝）", SPIRAL_MAIN, kind='fragment',
         note="遞迴呼叫時長度減 5。長度減到 0 或以下時函式直接回傳；整個圖畫完之後，<code>screen.bye()</code> 關閉 CTurtle 的視窗。")}
<h3>碎形樹</h3>
<p>接著看<strong>碎形</strong>（fractal）。碎形來自數學的一個分支，和遞迴有很多共通點。依定義，碎形不管放大多少倍，基本形狀都一樣。大自然中的例子有海岸線、雪花、山脈，甚至樹木與灌木。因為這種性質，程式設計師可以用碎形為電腦動畫產生非常逼真的景物。</p>
<p>既然碎形在各種放大倍率下看起來都一樣，套到樹上就是：連一根小樹枝，都和整棵樹有相同的形狀與特徵。所以可以這樣定義樹：<strong>一棵樹是一段樹幹，右邊長出一棵較小的樹，左邊也長出一棵較小的樹</strong>。用遞迴的觀點看這個定義，就是把同一個定義再套用到左右兩棵較小的樹上。</p>
{snippet("講義 06 · tree（CTurtle，需另外安裝）", TREE, kind='fragment',
         note="完整的桌面程式會建立 <code>cturtle::TurtleScreen</code>、讓烏龜朝上，呼叫 <code>tree(75, turtle)</code>，畫完後關閉視窗。")}
<p>兩次遞迴呼叫分別發生在右轉 20 度與左轉 40 度之後：左轉 40 度先抵銷原本的右轉 20 度，再往左多轉 20 度。每次呼叫都把 <code>branchLen</code> 減 15，<code>branchLen &gt; 5</code> 不成立時就不再遞迴，這就是 base case。最後的右轉 20 度與後退，讓烏龜回到這次呼叫開始時的位置與方向，上一層才能接著畫另一邊。</p>
<p>下面用 canvas 畫出同樣的兩個圖形。拉動樹的深度，比較每多一層時樹多長出多少枝。</p>
{W.w_viz()}
<h3>樹是怎麼畫出來的</h3>
<p>注意樹上的每個分岔點都對應一次遞迴呼叫，而且程式會一路往右畫到最短的小樹枝：</p>
{figure('viz1')}
<p>接著程式沿著樹幹往回退，直到整棵樹的右半邊都畫完：</p>
{figure('viz2')}
<p>然後開始畫左半邊，但不是一路往左畫到底。左子樹的右半邊同樣會先整個畫完，最後才走到最左邊的小樹枝。這個簡單的樹程式只是起點：程式畫的樹完全對稱，所以看起來不太真實，大自然可沒有這麼整齊。</p>'''


# ---------------------------------------------------------------- P05
def sierpinski():
    q = quiz('qSier', 'QUIZ · 數三角形', 'degree = 3 時，sierpinski 總共被呼叫幾次（含最外層那一次）？', [
        (True, '1 + 3 + 9 + 27 = 40 次', '每一層是前一層的 3 倍：3⁰ + 3¹ + 3² + 3³。三路遞迴的呼叫數以 3 的冪次成長。'),
        (False, '3 × 3 = 9 次', '每次呼叫都會再發出三次呼叫，直到 degree 歸零；是一層層連乘，不是只乘一次。'),
        (False, '27 次', '27 只是最深那一層的呼叫數，上面各層的呼叫也要算進去。'),
        (False, '13 次', '1 + 3 + 9 = 13 是 degree = 2 的總數；degree = 3 還要加上最深一層的 27 次。'),
    ])
    return f'''{SKIPPED}
<p>Sierpinski 三角形是一個<strong>三路遞迴</strong>的例子。用手畫的步驟很簡單：</p>
{ol(['先畫一個大三角形。', '連接三邊的中點，把大三角形分成四個小三角形。', '中間那個不管，對三個角落的小三角形套用同樣的步驟。'])}
{figure('triangle')}
<p>base case 是什麼？這裡的 base case 是人為設定的：要把三角形分割幾次。這個次數稱為碎形的 <strong>degree</strong>（深度）。每做一次遞迴呼叫，degree 就減 1；degree 減到 0 時，不再遞迴呼叫。</p>
<h3>講義程式（CTurtle，需另外安裝）</h3>
<p>程式分成三段。第一段的 drawTriangle 用指定顏色畫出並填滿一個三角形：</p>
{snippet("講義 06 · drawTriangle（CTurtle，需另外安裝）", DRAW_TRIANGLE, kind='fragment')}
<p>第二段是 sierpinski 本身。它有三個遞迴呼叫，每個呼叫對應連接中點之後得到的一個角落小三角形：</p>
{snippet("講義 06 · sierpinski", SIERPINSKI, kind='fragment',
         note="<code>ct::middle(a, b)</code> 回傳 a、b 兩點的中點。顏色用 degree 當索引，所以同一層的三角形顏色相同。")}
<p>第三段的 main 建立視窗，設定三個頂點，用 degree 3 開始畫：</p>
{snippet("講義 06 · main", SIER_MAIN, kind='fragment',
         note="這是 CTurtle 的桌面程式，在 notebook 中只供閱讀；三個頂點依序是左下、上方、右下。")}
<p>下面用 canvas 畫出同樣的圖形，拉動 degree 觀察三角形的數量怎麼成長。</p>
{W.w_sierpinski()}
<h3>畫的順序</h3>
<p>看著程式想想看，三角形會以什麼順序畫出來？假設三個角依序是左下、上方、右下。因為 sierpinski 呼叫自己的方式，它會先一路畫到左下角最小的三角形，再往回補齊其他三角形。接著往上方角落，一路畫到最上面最小的三角形；最後才是右下角。把遞迴演算法畫成函式呼叫圖，常常有助於理解：</p>
{figure('triangle2')}
<p>正在執行的函式畫成黑框，還沒執行的呼叫是灰色。越往下，三角形越小。函式一次完成一層：左下角畫完之後，才移到下方中間，依此類推。</p>
{q}'''


# ---------------------------------------------------------------- P06
def hanoi():
    return f'''<div class="info-box"><span class="info-label">接下來的問題</span>前面的問題用遞迴解很容易，或主要用來建立對遞迴的直覺。接下來兩個問題用迴圈很難寫，用遞迴卻很簡潔：河內塔與迷宮。最後的找零錢問題正好相反：遞迴寫法很漂亮，執行起來卻慢得無法接受。</div>
<h3>傳說與規則</h3>
<p>河內塔是法國數學家 Édouard Lucas 在 1883 年發明的謎題。他的靈感來自一個傳說：一座印度教寺廟裡，年輕的僧侶被交付這個謎題。一開始他們拿到三根柱子，以及疊成一疊的 64 個金盤，每個盤子都比下面那個小一點。他們要把 64 個盤子從一根柱子全部搬到另一根，並遵守兩條規則：</p>
{ol(['一次只能搬一個盤子。', '大盤子永遠不能放在小盤子上面。'])}
<p>傳說僧侶日夜不停，每秒搬一個盤子，搬完的那天，寺廟會化為塵土，世界也將消失。不必擔心：正確搬完 64 個盤子需要 $2^{{64}}-1 = 18{{,}}446{{,}}744{{,}}073{{,}}709{{,}}551{{,}}615$ 步，每秒一步要花 $584{{,}}942{{,}}417{{,}}355$ 年。</p>
<p>下圖是從第一根柱子搬到第三根的過程中，某個時刻的樣子。依照規則，每根柱子上都是小盤在上、大盤在下：</p>
{figure('hanoi')}
<h3>由下往上想</h3>
<p>假設第一根柱子上有五個盤子。如果你已經知道怎麼把四個盤子的塔搬到第二根柱子，就能把最下面的盤子搬到第三根，再把那四個盤子從第二根搬到第三根。</p>
<p>可是如果不知道怎麼搬四個盤子呢？假設你知道怎麼把三個盤子的塔搬到第三根柱子，那就能把第四個盤子搬到第二根，再把三個盤子從第三根疊到它上面。如果連三個盤子都還不會呢？至少把一個盤子搬到第三根柱子很容易，簡單到不值一提。這聽起來就是 base case。</p>
<h3>三步驟大綱</h3>
<p>把高度 h 的塔從起始柱（fromPole）搬到目標柱（toPole），中途借用中間柱（withPole）：</p>
{ol(['借用目標柱，把上面高度 h−1 的塔從起始柱搬到中間柱。', '把剩下的一個盤子從起始柱搬到目標柱。', '借用起始柱，把高度 h−1 的塔從中間柱搬到目標柱。'])}
<p>最簡單的非空河內塔只有一個盤子：直接把它搬到目的地。程式中的 base case 是高度 0 的塔，什麼都不用搬。步驟 1 與步驟 3 都讓塔的高度減一，所以會朝 base case 前進。每一層各搬一個盤子，搬 n 個盤子總共要 $2^n - 1$ 步。</p>
{W.w_hanoi()}
<h3>講義程式：moveTower</h3>
{lecture_program("講義完整程式：moveTower 與 moveDisk", "講義 06 · 三個盤子的河內塔", HANOI, OUT['hanoi'],
                 note="main 呼叫 <code>moveTower(3, \"A\", \"B\", \"C\")</code>：從 A 搬到 B，借用 C。7 行輸出等於 2³ − 1 步。base case 是高度 0 的塔：這時什麼都不做，moveTower 直接回傳。base case 一回傳，上一層就接著執行 moveDisk。")}
<h3>柱子上的盤子由誰記住？</h3>
<p>看完 moveTower 與 moveDisk，你也許會疑惑：為什麼沒有一個資料結構明確記錄每根柱子上有哪些盤子？如果要明確追蹤，可以用三個 <code>Stack</code> 物件，每根柱子一個。遞迴的 C++ 程式則是靠執行時的呼叫堆疊，記住所有暫停中的呼叫：每個還沒結束的 moveTower 都記得自己要從哪裡搬到哪裡、搬到第幾步。</p>'''


# ---------------------------------------------------------------- P07
def maze():
    return f'''<p>這一節要解一個和機器人有關的問題：怎麼走出迷宮？我們要幫一隻烏龜走出虛擬的迷宮。迷宮問題可以追溯到希臘神話：忒修斯被派進迷宮殺死牛頭人，他用一團線標記來路，事後才找得到出口。這裡假設烏龜被丟在迷宮中間某處，必須自己找到出口。</p>
{figure('maze')}
<h3>探索程序</h3>
<p>為了簡化，假設迷宮被切成方格，每一格不是通道就是牆。烏龜只能走通道，撞到牆就換一個方向。程序如下：</p>
{ol(['從目前的位置先往北走一格，<strong>再從那裡遞迴地執行同一個程序</strong>。',
     '往北走不出去，就改往南走一格，再遞迴地執行同一個程序。',
     '往南也不行，就往西走一格，再遞迴地執行。',
     '北、南、西都失敗，就從往東一格的位置遞迴地執行。',
     '四個方向都不行，就表示走不出迷宮，回報失敗。'])}
<p>聽起來很簡單，但有個細節要處理。假設第一步往北，照程序，下一步還是先往北；如果北邊是牆，就改試南邊。可是往南一步就回到了原本的起點，從那裡再執行程序，又會往北走一步，然後無限循環下去。所以必須記住走過哪些地方。</p>
<p>假設烏龜帶著一袋<strong>麵包屑</strong>，邊走邊撒。往某個方向走一步，發現那一格已經有麵包屑，就立刻退回來，試程序中的下一個方向。之後看程式就會知道：<strong>退回來，就只是從遞迴呼叫回傳</strong>。</p>
<h3>四個 base case</h3>
{ol(['烏龜撞到牆。這一格是牆，無法再探索。',
     '烏龜走到已經探索過的格子。不從這裡繼續探索，以免陷入迴圈。',
     '走到迷宮的邊緣，而且那一格不是牆。也就是找到出口了。',
     '這一格往四個方向都探索過，全部失敗。'])}
<h3>Maze 類別</h3>
<p>以下面這個迷宮為例：<code>+</code> 是牆，空白是通道，<code>S</code> 是起點。</p>
<pre class="rec-maze">{escape(MAZE_TEXT)}</pre>
<p>Maze 物件提供下列方法，供搜尋演算法使用：</p>
{ol(['<code>Maze(filename)</code>：建構子，讀入代表迷宮的資料檔，建立迷宮的內部表示，並找出起點的位置。',
     '<code>print()</code>：印出目前的字元格子。',
     '<code>updatePosition()</code>：更新迷宮中某一格存放的字元。',
     '<code>isExit()</code>：檢查目前位置是不是迷宮的出口。'])}
<p>另外還有 <code>get(row, col)</code>，讓演算法可以讀取任一格的狀態。迷宮的每種狀態用一個具名常數表示。C++ 版不畫烏龜動畫，而是把進度印成文字：</p>
{snippet("講義 06 · 迷宮的字元常數", MAZE_CONSTS, kind='fragment',
         note="START 是起點，OBSTACLE 是牆，TRIED 是走過的格子（麵包屑），DEAD_END 是確定走不通的格子，PART_OF_PATH 是通往出口的路。")}
<p>建構子 <code>Maze(filename)</code> 只有一個參數：檔名。這個文字檔用 <code>+</code> 表示牆、空白表示通道、字母 <code>S</code> 表示起點。</p>
{snippet("講義 06 · Maze 的建構子與資料成員", MAZE_CLASS, kind='fragment',
         note="建構子逐列讀檔，把每一列放進 <code>mazeList</code>，記下列數與欄數，再找出 S 所在的列與欄。<code>startRow</code>、<code>startCol</code> 是 public，main 要用它們開始搜尋；<code>mazeList</code>、<code>rowsInMaze</code>、<code>columnsInMaze</code> 是 private，只能透過成員函式存取。")}
<p>C++ 的 Maze 把字元格子存在名為 <code>mazeList</code> 的 <code>vector&lt;string&gt;</code> 裡。每個 string 是一列，所以 <code>mazeList[row][col]</code> 就是一格。C++ 版保留同樣的遞迴狀態轉換，並印出字元格子；每次更新都會留在最後的格子裡，不需要圖形視窗：</p>
{snippet("講義 06 · updatePosition 與 print", MAZE_UPDATE_PRINT, kind='fragment')}
<p><code>isExit()</code> 用目前的位置檢查是否到達出口：只要烏龜走到迷宮的邊緣，也就是第 0 列、第 0 欄、最右邊一欄或最下面一列，就是出口。</p>
{snippet("講義 06 · isExit 與 get", MAZE_EXIT_GET, kind='fragment')}
<h3>searchFrom：遞迴搜尋</h3>
<p>搜尋函式叫做 <code>searchFrom()</code>，有三個參數：一個 Maze 物件、起始的列與起始的欄。起始位置要當成參數傳入，因為它是遞迴函式，每次遞迴呼叫，搜尋在邏輯上都從新的位置重新開始。</p>
{snippet("講義 06 · searchFrom（完整程式在 pythonds3/cppds/maze.hpp）", SEARCH_FROM, kind='fragment',
         note="前三個 if 是 base case 1 到 3；四個方向都回傳 false，就是 base case 4，這一格標成 DEAD_END。")}
<p>遞迴步驟裡有四個 <code>searchFrom()</code> 呼叫，很難事先知道會用到幾個，因為它們用 <code>||</code> 連接：只要前面的呼叫成功，<strong>短路求值</strong>就會跳過後面的呼叫。如果第一個呼叫（往北）回傳 true，其他三個都不會執行；從幾何上看，北邊那一步就在通往出口的路上。往北失敗，才依序試南、西、東。四個呼叫都回傳 false，目前這一格就是死路。</p>
<p>下面的動畫在一個較小的迷宮上執行同樣的 searchFrom。注意每一格怎麼先被標成走過，四個方向都試完後，再改成路徑或死路。</p>
{W.w_maze()}
<h3>講義程式：在 maze2.txt 上執行</h3>
<p>課程資料夾裡已經有迷宮檔 <code>maze2.txt</code>：</p>
<pre class="rec-maze">{escape(MAZE2_TXT)}</pre>
{lecture_program("講義完整程式：讀入 maze2.txt 並搜尋", "講義 06 · 迷宮主程式", MAZE_MAIN, OUT['maze'],
                 note="印出的結果中，<code>O</code> 是成功的路徑，<code>-</code> 是死路，<code>.</code> 是走過的格子。這次的結果裡沒有 <code>.</code>：每一格離開 searchFrom 之前，都會從 TRIED 改成 PART_OF_PATH 或 DEAD_END。路徑從 S 往北走，最後在左邊第 2 列的邊緣找到出口；左下方那一大片 <code>-</code>，是往南與往西探索後退回來的痕跡。")}'''


# ---------------------------------------------------------------- P08
def dp():
    recurrence = r'''$$num\_coins = \min\begin{cases}1 + num\_coins(original\ amount - 1)\\ 1 + num\_coins(original\ amount - 5)\\ 1 + num\_coins(original\ amount - 10)\\ 1 + num\_coins(original\ amount - 25)\end{cases}$$'''
    versions = table(['版本', '策略', '{1, 5, 10, 25} 找 63 分'], [
        ('<code>makeChange1</code>', '天真遞迴', '67,716,925 次呼叫'),
        ('<code>makeChange2</code>', '記憶化（memoization），由上而下', '221 次呼叫'),
        ('<code>makeChange3</code>', '動態規劃，由小到大填表，不遞迴', '64 格 × 4 種硬幣的檢查，$O(AC)$'),
    ])
    q = quiz('qDp', 'QUIZ · DP 與天真遞迴', '天真遞迴找 63 分要約 6,772 萬次呼叫，DP 只要逐格檢查硬幣。DP 快的主要原因是什麼？', [
        (True, '每個子問題只算一次，答案存在表裡', '找零錢有重疊的子問題（例如 15 分會被重算很多次），把答案記在表裡就不必重算，計算量從指數級降到 $O(AC)$。'),
        (False, 'DP 用了比較聰明的硬幣順序', '硬幣的順序不影響計算量；快的關鍵是不重算。'),
        (False, '遞迴本身比迴圈慢上千倍', '函式呼叫的固定成本沒有這麼大，差別在計算量的量級。makeChange2 也是遞迴，只要 221 次呼叫。'),
        (False, 'DP 改用貪婪法，每次拿最大的硬幣', 'DP 每格都比較所有硬幣，不是貪婪法；貪婪法在有 21 分硬幣時找 63 分會給出 6 枚，不是最佳解。'),
    ])
    anim = ('<p>下面的動畫用 makeChange4 的硬幣 {1, 5, 10, 21, 25} 填 0 到 23 分的表。每一格都是「試每一種硬幣，查剩下金額那一格，取最少」。'
            '填完後沿著每格記下的最後一枚硬幣往回走，就能還原答案。23 分最少要 3 枚（21 + 1 + 1）。</p>'
            + W.w_dp())
    return f'''{SKIPPED}
<p>電腦科學中有許多程式是在<strong>最佳化</strong>某個值，例如找兩點之間的最短路徑、找最符合一組點的直線，或找出滿足某些條件的最小物件集合。電腦科學家解這類問題有很多策略，<strong>動態規劃</strong>（dynamic programming）是其中之一。</p>
<h3>找零錢與貪婪法</h3>
<p>最佳化問題的經典例子，是用最少的硬幣找零。假設你在販賣機公司寫程式，公司希望每筆交易找的硬幣越少越好。顧客投入一元紙鈔，買了 37 分的東西，要找 63 分。最少要用幾枚硬幣？</p>
<p>答案是 6 枚：兩個 25 分、一個 10 分、三個 1 分。怎麼得到的？從手上最大的硬幣（25 分）開始，能用幾枚就用幾枚，再換下一種較小的硬幣，依此類推。這種做法稱為<strong>貪婪法</strong>（greedy method），因為它每一步都想馬上解決盡量大的一部分問題。</p>
<p>用美國硬幣時，貪婪法沒有問題。但假設公司把販賣機賣到另一個國家，那裡除了 1、5、10、25 分，還有 21 分硬幣。這時貪婪法找 63 分仍然給出 6 枚，最佳解卻是三枚 21 分。</p>
<h3>遞迴寫法：makeChange1</h3>
<p>改用遞迴，先找 base case：要找的金額剛好等於某種硬幣的面額，答案很簡單，就是一枚。金額不相等時有幾種選擇：1 分硬幣加上「原金額減 1 分」所需的硬幣數、5 分硬幣加上「原金額減 5 分」所需的硬幣數，依此類推，取其中最小的。所以原金額需要的硬幣數是：</p>
{recurrence}
{lecture_program("講義完整程式：makeChange1", "講義 06 · 天真遞迴（26 分）", MC1, OUT['mc1'],
                 note="26 分最少要 2 枚（25 + 1）。函式一開始檢查 base case：金額是否剛好等於某一種硬幣。不是的話，對每一種不超過金額的硬幣各做一次遞迴呼叫，取最小值再加一。")}
<h3>問題：重複計算</h3>
<p>這個演算法的問題是效率極差。用 4 種硬幣找 63 分，要做 67,716,925 次遞迴呼叫才找到最佳解。下圖是找 26 分所需的 377 次呼叫中的一小部分：</p>
{figure('dp1')}
<p>圖中每個節點是一次 <code>makeChange1()</code> 呼叫，節點上的數字是這次要找零的金額，箭頭上的數字是剛用掉的硬幣。主要的問題在於<strong>重複做太多計算</strong>。例如圖中可以看到，15 分的最佳硬幣數至少被重算三次，而每算一次 15 分，本身就要 52 次函式呼叫。重算舊結果，白白浪費了大量時間。</p>
{fold("自己數一數呼叫次數", snippet("加上計數器的 makeChange1 與 makeChange2", MC_COUNT, OUT['mc_count'],
      note="每進入函式一次就把計數器加一。26 分與 15 分的次數就是上面說的 377 與 52；記憶化版本找 63 分只要 221 次。最後一行是 knownResults 的前 11 格：2、3、4 分是 0，表示這幾格從沒被填過。"))}
<h3>記住算過的結果：makeChange2</h3>
<p>減少計算量的關鍵，是記住過去的結果，避免重算已知的答案。簡單的做法是：每找到一個金額的最少硬幣數，就存進一張表。計算新的最小值之前，先查表；表裡已經有結果，就直接使用，不再重算。</p>
{lecture_program("講義完整程式：makeChange2", "講義 06 · 用 knownResults 記住結果", MC2, OUT['mc2'],
                 note="63 分最少要 6 枚（25 + 25 + 10 + 1 + 1 + 1）。knownResults 的索引是金額，0 表示還不知道答案。")}
<p>以上面這份程式來說，查表把 4 種硬幣、63 分的計算降到總共 221 次呼叫。呼叫次數取決於查表與存表放在哪裡，所以組織方式不同、但同樣做記憶化的函式，次數可能不一樣。</p>
<p>不過這看起來有點像拼湊出來的補丁。而且看看 knownResults 這張表，會發現表裡有些洞（例如 2、3、4 分始終沒有填）。嚴格說來，這樣做還不算動態規劃；我們是用一種叫做<strong>記憶化</strong>（memoization），更常稱為<strong>快取</strong>（caching）的技巧改善了程式的效能。</p>
<h3>由下往上填表：動態規劃</h3>
<p>真正的動態規劃演算法用更有系統的方式處理問題：從找 1 分開始，一路往上算到要找的金額。這樣保證演算法的每一步，都已經知道任何較小金額所需的最少硬幣數。看看找 11 分時，最少硬幣數的表格怎麼填：</p>
{figure('dp2')}
<p>從 1 分開始，唯一的找法是一枚硬幣。下一列是 1 分與 2 分的最小值，2 分同樣只能用兩個 1 分。第五列開始有意思：要考慮兩種選擇，五個 1 分或一個 5 分。怎麼決定哪個好？查表：4 分需要 4 枚，再加一個 1 分湊成 5 分，共 5 枚；或者 0 分再加一個 5 分，共 1 枚。1 與 5 取最小，表裡存 1。快轉到表的最後，看 11 分。</p>
{figure('dp3')}
<p>有三個選擇要考慮：</p>
{ol(['一個 1 分，加上找 11 − 1 = 10 分所需的最少硬幣數（1 枚）。',
     '一個 5 分，加上找 11 − 5 = 6 分所需的最少硬幣數（2 枚）。',
     '一個 10 分，加上找 11 − 10 = 1 分所需的最少硬幣數（1 枚）。'])}
<p>第 1 與第 3 個選擇都只要 1 + 1 = 2 枚，所以 11 分最少要 2 枚。</p>
<h3>makeChange3：動態規劃版本</h3>
<p><code>makeChange3()</code> 是由下往上的動態規劃版本。它接收合法的硬幣面額、要找的金額，以及一個 vector，存放 0 到目標金額每一個金額的最少硬幣數。</p>
{lecture_program("講義完整程式：makeChange3", "講義 06 · 由小到大填 minCoins", MC3, OUT['mc3'],
                 note="結果和 makeChange2 相同，都是 6 枚，但完全沒有遞迴。")}
<p><code>makeChange3()</code> 不是遞迴函式。對 0 到 <code>change</code> 的每個金額，內層迴圈檢查每一種面額，並存下由較小金額已算出的最佳結果。設目標金額為 $A$、硬幣種類數為 $C$，工作量是 $O(AC)$，表格使用 $O(A)$ 的空間。</p>
{versions}
<h3>記下用了哪些硬幣：makeChange4 與 printCoins</h3>
<p>只要再記住表中每一格「最後加上的那枚硬幣」，就能把 makeChange3 擴充成能追蹤用了哪些硬幣。知道最後加的硬幣，把金額減去它的面額，就找到表中前一格，那一格又記著它最後加的硬幣。一路往回追，直到金額為 0。</p>
{lecture_program("講義完整程式：makeChange4 與 printCoins", "講義 06 · 加入 21 分硬幣，找 63 分", MC4, OUT['mc4'],
                 note="這次的硬幣包含 21 分，最佳解是三枚 21 分。第二段輸出是 coinsUsed 的全部內容，索引 0 到 63。")}
<p><code>coinsUsed</code> 記錄每個金額最後選用的硬幣，<code>coinCount</code> 記錄每個金額的最少硬幣數，兩者都是以金額為索引的 vector。注意印出來的硬幣直接取自 coinsUsed：第一次從位置 63 開始，印出 21；接著看第 42 格，那裡也存著 21；最後第 21 格同樣是 21，於是得到三枚 21 分。</p>
{fold("填表動畫：23 分", anim)}
{q}'''


# ---------------------------------------------------------------- EX
def exercises():
    q1 = quiz('ex1', 'EXERCISE 1 · 追蹤遞迴', '<code>toStr(10, 2)</code> 的回傳值是什麼？（可以用 P02 的動畫驗證）', [
        (True, '<code>"1010"</code>', 'toStr(10,2) = toStr(5,2) + "0" = (toStr(2,2) + "1") + "0" = ((toStr(1,2) + "0") + "1") + "0" = "1010"。'),
        (False, '<code>"0101"</code>', '這是把餘數照產生的順序串起來。遞迴版不會這樣，因為餘數是在呼叫「回來之後」才接上。'),
        (False, '<code>"101"</code>', '少了最後一位 0：每一層都要接上 n % base 的餘數，包括最外層的 10 % 2。'),
        (False, '<code>"10"</code>', '"10" 是 toStr(2, 2) 的結果，外面還有兩層要接上 1 與 0。'),
    ])
    q2 = quiz('ex2', 'EXERCISE 2 · 河內塔', '4 個盤子的河內塔最少要搬幾次？其中最大的盤子搬了幾次？', [
        (True, '15 次；最大盤 1 次', '2⁴ − 1 = 15。最大盤只在「中間那一步」直接搬到目標柱，所以只搬 1 次。'),
        (False, '16 次；最大盤 2 次', '公式是 2ⁿ − 1，不是 2ⁿ；最大盤只搬一次，這是遞迴分解的關鍵。'),
        (False, '15 次；最大盤 4 次', '次數對了，但最大盤只動 1 次：要搬它之前，上面的盤子必須已經全部移開。'),
        (False, '8 次；最大盤 1 次', '8 是 2³。4 盤要先搬走上面 3 盤（7 步）、搬最大盤（1 步）、再把 3 盤搬回來（7 步），共 15 步。'),
    ])
    q3 = quiz('ex3', 'EXERCISE 3 · 迷宮的 base case', '如果 searchFrom 少寫「走過的格子直接 return false」，會發生什麼事？', [
        (True, '相鄰兩格互相呼叫，形成無窮遞迴', 'A 往北走到 B，B 往南又回到 A。沒有麵包屑標記，就不會朝 base case 前進，違反法則 2。'),
        (False, '答案錯誤，但程式會停', '程式不會停：兩格之間會一直互相呼叫，這是最典型的無窮遞迴。'),
        (False, '只是變慢', '沒有終止條件會持續遞迴，通常耗盡呼叫堆疊而終止；不能當成只是變慢。'),
        (False, '沒有影響，因為 DEAD_END 也會擋住', '格子要等四個方向都試完才會標成 DEAD_END；在那之前，相鄰的格子早已互相呼叫下去了。'),
    ])
    return f'''<h3>追蹤遞迴</h3>
{q1}
<h3>河內塔的步數</h3>
{q2}
<h3>迷宮的 base case</h3>
{q3}'''


# ---------------------------------------------------------------- REF
def reference():
    return f'''<h3>比較表</h3>
{table(['問題', 'base case', '縮小方式', '複雜度'], [
        ('listSum', '索引到達 vector 尾端', '索引加 1', '$O(n)$'),
        ('toStr(n, base)', 'n &lt; base', 'n / base', '$O(\\log n)$'),
        ('河內塔', 'height 為 0', 'height − 1（兩次）', '$O(2^n)$'),
        ('迷宮', '牆、走過、出口、四方向皆失敗', '相鄰格子', '$O(\\text{格子數})$'),
        ('找零錢（makeChange3）', '不遞迴；minCoins[0] = 0', '金額 − 硬幣面額（查表）', '$O(AC)$'),
    ])}
<h3>關鍵概念</h3>
<div class="info-box" style="margin-top:1rem;">
    <span class="info-label">關鍵概念複習</span>
    ① 三法則：有 base case、朝它前進、呼叫自己。<br>
    ② 呼叫堆疊是看不見的 stack：上一章自己管理的 stack，遞迴時交給系統代管。<br>
    ③ 分支遞迴（河內塔 2 支、迷宮 4 支）容易產生大量呼叫；子問題<strong>重疊</strong>時，用記憶化或動態規劃避免重算。<br>
    ④ Sierpinski 三角形等碎形在各種尺度下自我相似，可以直接用遞迴畫出來。
  </div>'''


# ---------------------------------------------------------------- recap
def recap():
    qa = [
        ('遞迴一定比迴圈慢嗎？',
         '<p>不一定。每次函式呼叫都有固定的額外成本（建立 frame、傳參數、回傳），所以同樣的計算量，迴圈通常稍快一些。但真正的差距多半來自演算法：makeChange1 慢，是因為重算了大量相同的子問題，不是因為它用了遞迴；同樣是遞迴的 makeChange2 只要 221 次呼叫。</p>'),
        ('遞迴可以多深？',
         '<p>每一層呼叫都佔用一個 stack frame，而呼叫堆疊的大小有限，上限取決於作業系統與編譯設定。像 listSumFrom 這種一層只處理一個元素的線性遞迴，對很長的 vector 可能用完堆疊；toStr 每層把 n 除以 base，深度只有對數級，不必擔心。</p>'),
        ('為什麼 makeChange2 的表裡會有洞？',
         '<p>記憶化只在遞迴真的走到某個金額時才填表。makeChange2 遇到 1 分或 5 分這種「剛好一枚」的金額時直接回傳，不會往下算 2、3、4 分，所以那幾格始終是 0。動態規劃由小到大逐格填，每一格都會填到。</p>'),
        ('河內塔的步數為什麼是 $2^n - 1$？',
         '<p>設 n 個盤子要 $T(n)$ 步。三步驟大綱是兩次搬 n−1 個盤子，加上一次搬最大盤，所以 $T(n) = 2T(n-1) + 1$，且 $T(0) = 0$。依序代入得到 1、3、7、15……，也就是 $T(n) = 2^n - 1$。</p>'),
        ('迷宮的搜尋一定找到最短路徑嗎？',
         '<p>不一定。searchFrom 依固定順序試北、南、西、東，找到第一條通往邊緣的路就停下，這條路未必最短。要找最短路徑，需要逐層往外擴展的搜尋方式，例如之後圖論章節的廣度優先搜尋。</p>'),
    ]
    faq = ''.join(details(f'{q}（補充）', a, cls='rec-detail rec-faq') for q, a in qa)
    return f'''<ul class="rec-ul rec-recap">
<li>遞迴把問題拆成更小的同型問題，直到小到可以直接解決。listSum 可以用累加變數寫成迴圈，也可以寫成「目前這一項加上剩下範圍的總和」。</li>
<li>遞迴三法則：必須有 base case、必須改變狀態朝 base case 前進、必須呼叫自己。base case 要涵蓋所有最小的合法輸入，例如 <code>size() &lt;= 1</code> 同時處理空字串與單一字元。</li>
<li>toStr 用整數除法縮小問題、用餘數查表取得字元；把串接放在遞迴呼叫回來之後，位數的順序就正確。</li>
<li>每個進行中的呼叫都有自己的 stack frame，存放參數、區域變數與返回資訊。呼叫堆疊取代了顯式的 stack，也讓每次呼叫有各自的作用域。</li>
<li>碎形在各種尺度下自我相似；spiral、tree 與 sierpinski 用遞迴畫出這類圖形。多路遞迴會先把第一個分支整個做完，才輪到下一個。</li>
<li>河內塔：搬 h−1 個到中間柱、搬最大盤、再搬 h−1 個到目標柱，共 $2^n - 1$ 步；暫停中的呼叫由呼叫堆疊記住。</li>
<li>迷宮：四個 base case（牆、走過、出口、四方向皆失敗），用麵包屑避免繞圈，<code>||</code> 的短路求值讓找到路就停。退回就是從遞迴呼叫回傳。</li>
<li>找零錢：貪婪法不保證最佳；天真遞迴重算重疊的子問題；記憶化由上而下把結果存起來；動態規劃由下往上填表，$O(AC)$ 時間、$O(A)$ 空間，再用 coinsUsed 還原用了哪些硬幣。</li>
</ul>
<h3>常見疑問</h3>
{faq}'''


def sections():
    return {
        'recursion-prologue': prologue(),
        'recursion-laws': laws(),
        'recursion-tostr': tostr(),
        'recursion-frames': frames(),
        'recursion-viz': viz(),
        'recursion-sierpinski': sierpinski(),
        'recursion-hanoi': hanoi(),
        'recursion-maze': maze(),
        'recursion-dp': dp(),
        'recursion-exercises': exercises(),
        'recursion-reference': reference(),
        'recursion-recap': recap(),
    }


STYLE = """<style id="recursion-depth-style">
.rec-detail{margin:1rem 0;border:1px solid var(--card-border);border-radius:8px;background:var(--card);}
.rec-detail>summary{cursor:pointer;padding:.9rem 1rem;font-weight:600;line-height:1.6;}
.rec-detail-body{padding:0 1rem 1rem;min-width:0;}
.rec-detail-body .pseudo-code{max-width:100%;overflow-x:auto;}
.deck-extra .pseudo-code{max-width:100%;overflow-x:auto;}
.side-panel .pseudo-code{max-width:100%;overflow-x:auto;}
.rec-ul{padding-left:1.4rem;margin:.6rem 0 1rem;}
.rec-ul li{margin:.3rem 0;line-height:1.8;}
.rec-skip{font-size:.88rem;color:var(--muted);}
.rec-maze{font-family:'JetBrains Mono',monospace;font-size:.8rem;line-height:1.35;background:var(--card);border:1px solid var(--card-border);border-radius:8px;padding:.6rem .9rem;overflow-x:auto;max-width:100%;white-space:pre;}
.viz-layout{min-width:0;}
.viz-layout>div{min-width:0;}
.quiz-opt .opt-text{min-width:0;overflow-wrap:anywhere;}
#tsfVis{flex-direction:column;}
#tsfVis .bs-item{width:auto;min-width:230px;max-width:100%;font-size:.85rem;}
</style>"""
