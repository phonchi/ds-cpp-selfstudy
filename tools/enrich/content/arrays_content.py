"""第三章教學正文。由 enrich_arrays.py 產生受管 section。"""
import re
from pathlib import Path
from html import escape
from enrich_lib import hl
from arrays_headers import ARRAYLIST
HERE = Path(__file__).parent

def code(title, src, output=None, kind='fragment', cid=None):
    """kind：run（完整程式，輸出逐字比對）、run-addr（輸出含位址，比對時位址正規化）、
    run-free（完整程式，輸出不固定，不附預期輸出）、fragment、compile-error、exercise、header。"""
    attrs = f' data-cpp="{kind}"' + (f' id="{cid}"' if cid else '')
    if output is not None:
        attrs += ' data-expected="' + escape(output, quote=True).replace('\n', '&#10;') + '"'
    out = f'<div class="deck-extra"><div class="dx-label">{title}</div><div class="pseudo-code"{attrs}>{hl(src)}</div>'
    if output is not None:
        out += '<div class="expected-out"><span class="eo-tag">預期輸出</span><pre>' + escape(output).replace(' \n', '&#32;\n') + '</pre></div>'
    return out + '</div>'

_EXPECTED_OUT = re.compile(r'<div class="expected-out">.*?</pre></div>', re.S)

def details(title, body, tag='補充'):
    """tag：'補充'＝講義沒有的內容；'與講義寫法不同'；None＝講義內容，只因篇幅收合。
    講義內容只收合程式，預期輸出移到收合區外保持可見。"""
    after = ''
    if tag:
        title += f'（{tag}）'
    else:
        after = ''.join(_EXPECTED_OUT.findall(body))
        body = _EXPECTED_OUT.sub('', body)
    return f'<details class="chapter-extra"><summary>{escape(title)}</summary><div class="extra-body">{body}</div></details>{after}'

def table(head, rows):
    return '<div class="chapter-table"><table class="cmp-table"><thead><tr>' + ''.join('<th>'+x+'</th>' for x in head) + '</tr></thead><tbody>' + ''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in rows) + '</tbody></table></div>'

def widget(name): return (HERE/f'arrays_{name}_widget.html').read_text()
def section(sid, title, body):
    return f'<section id="{sid}">\n<!-- gen:arrays-{sid} -->\n<h2>{title}</h2>\n{body}\n<!-- /gen:arrays-{sid} -->\n</section>'

def quiz(qid, title, question, answers):
    return f'<div class="quiz-box"><div class="quiz-label">{title}</div><p>{question}</p><div class="quiz-options" id="{qid}Options">'+''.join(f'<div class="quiz-opt" data-correct="{str(ok).lower()}" data-fb="{escape(fb,quote=True)}" onclick="quizCheck(\'{qid}\', this)"><span class="opt-letter">({chr(65+i)})</span> {a}</div>' for i,(a,ok,fb) in enumerate(answers))+f'</div><div class="quiz-feedback" id="{qid}Feedback"></div></div>'

def figure(filename, alt, caption, narrow=False):
    cls = 'arrays-figure narrow' if narrow else 'arrays-figure'
    return f'<figure class="{cls}"><div class="arrays-figure-scroll" tabindex="0" aria-label="{escape(alt, quote=True)}"><img src="assets/figures/ch3/{filename}" alt="{escape(alt, quote=True)}" loading="lazy"></div><figcaption>{caption}</figcaption></figure>'

def speed(prefix):
    return (f'<span class="mono" style="font-size:.8rem;color:var(--muted);">速度 <input id="{prefix}Speed" type="range" '
            'min="120" max="1200" value="650" style="vertical-align:middle;"></span>')

def controls(prefix, extra=''):
    return (f'<div class="controls-bar">{extra}'
            f'<button class="btn btn-play" onclick="{prefix}Play()">▶ 播放</button>'
            f'<button class="btn btn-step" onclick="{prefix}Step()">→ 單步</button>'
            f'<button class="btn" onclick="{prefix}Player &amp;&amp; {prefix}Player.toggle(this)">⏸ 暫停</button>'
            + speed(prefix) + '</div>')

AL_CODE = r'''void push_back(int val) {
    if (lastIndex == maxSize) grow();
    myArray[lastIndex] = val;
    lastIndex++;
}
void grow() {
    int newCapacity = (maxSize == 0) ? 1 : maxSize * 2;
    int* bigger = new int[newCapacity];
    for (int i = 0; i < lastIndex; ++i)
        bigger[i] = myArray[i];
    delete[] myArray;
    myArray = bigger;
    maxSize = newCapacity;
}
void insert(int idx, int val) {
    if (idx < 0 || idx > lastIndex)
        throw out_of_range("insert index out of bounds");
    if (lastIndex == maxSize) grow();
    for (int i = lastIndex; i > idx; --i)
        myArray[i] = myArray[i - 1];
    myArray[idx] = val;
    ++lastIndex;
}
void erase(int idx) {
    checkIndex(idx); // 0 <= idx && idx < lastIndex
    for (int i = idx; i < lastIndex - 1; ++i)
        myArray[i] = myArray[i + 1];
    --lastIndex;
}'''

def arraylist_widget():
    options = ''.join(f'<option value="{v}">{t}</option>' for v, t in [
        ('push', 'push_back(40)：還有空位'), ('grow', 'push_back(50)：已滿，先 grow'),
        ('insert', 'insert(1, 99)：中間插入'), ('erase', 'erase(1)：中間刪除'),
        ('insertTail', 'insert(3, 40)：插在尾端'), ('eraseTail', 'erase(3)：刪除最後一項')])
    select = (f'<label class="mono" style="font-size:.85rem;">操作 <select class="mono" id="alScenario" onchange="alLoad()" '
              f'style="padding:.35rem;border-radius:6px;border:1px solid var(--card-border);">{options}</select></label>')
    return f'''<div class="viz-layout">
<div>
<div class="viz-panel">
<div id="alVis" class="al-vis" aria-live="polite"></div>
<div class="al-vars mono" id="alVars"></div>
<div class="status-banner" id="alStatus"><span class="status-icon">›</span><span class="status-text">選擇一個操作，按 ▶ 播放或 → 單步。</span></div>
{controls('al', select)}
</div>
</div>
<div class="side-panel">
<div class="info-card"><div class="ic-title">程式 <span class="ic-badge">CODE</span></div>
<div class="pseudo-code" id="alCode" data-cpp="fragment">{hl(AL_CODE)}</div></div>
<div class="info-card"><div class="ic-title">圖例</div><div class="al-legend">
<span><i class="al-chip al-valid"></i>有效元素（索引小於 lastIndex）</span>
<span><i class="al-chip al-stale"></i>不在有效區：仍有舊值，但不算元素</span>
<span><i class="al-chip al-empty"></i>尚未寫入的空位</span></div></div>
</div>
</div>'''

MM_ROW = r'''for (int i = 0; i < Rows; ++i)
    for (int j = 0; j < Cols; ++j)
        visit(i, j);'''
MM_COL = r'''for (int j = 0; j < Cols; ++j)
    for (int i = 0; i < Rows; ++i)
        visit(i, j);'''

def mapping_widget():
    sel = lambda sid, opts: (f'<select class="mono" id="{sid}" onchange="mmConfig()" style="padding:.35rem;border-radius:6px;'
                             'border:1px solid var(--card-border);">' + ''.join(f'<option value="{v}">{t}</option>' for v, t in opts) + '</select>')
    extra = ('<label class="mono" style="font-size:.85rem;">儲存 ' + sel('mmStore', [('row', 'row-major'), ('col', 'column-major（一維容器）')]) + '</label>'
             '<label class="mono" style="font-size:.85rem;">走訪 ' + sel('mmWalk', [('row', '外層 i、內層 j'), ('col', '外層 j、內層 i')]) + '</label>')
    return f'''<div class="viz-layout matrix-mapping" id="matrixMapping">
<div>
<div class="viz-panel">
<div id="mmGrid" class="mapping-grid" aria-label="3 列 4 欄邏輯矩陣"></div>
<div class="memory-scroll" tabindex="0" aria-label="一維記憶體"><div id="mmBand" class="memory-band"></div></div>
<p id="mmFormula" class="mapping-formula"></p>
<div class="status-banner" id="mmStatus"><span class="status-icon">›</span><span class="status-text">選好儲存方式與走訪順序後播放；也可以直接點矩陣格子查位址。</span></div>
{controls('mm', extra)}
</div>
</div>
<div class="side-panel">
<div class="info-card"><div class="ic-title">走訪程式 <span class="ic-badge">CODE</span></div>
<div class="pseudo-code" id="mmCodeRow" data-cpp="fragment">{hl(MM_ROW)}</div>
<div class="pseudo-code" id="mmCodeCol" data-cpp="fragment" hidden>{hl(MM_COL)}</div></div>
<div class="info-card"><div class="ic-title">假設</div><div style="font-size:.87rem;line-height:1.8;">Rows = 3、Cols = 4，每個 int 佔 4 bytes，起始位址 B = 1000。記憶體帶每格下方是 offset。</div></div>
</div>
</div>'''

def build():
    sections={}
    family=table(['比較','原生陣列 <code>int a[3]</code>','<code>std::array&lt;int,3&gt;</code>','<code>std::vector&lt;int&gt;</code>'],[
      ['需要的標頭','不需容器標頭','<code>&lt;array&gt;</code>','<code>&lt;vector&gt;</code>'],
      ['元素數量','固定；new[] 可在執行時決定配置大小，但配置後不變','固定；大小是型別的一部分','可增減，另有 capacity'],
      ['元素排列','元素連續儲存','元素連續儲存','元素連續儲存'],
      ['查大小','<code>sizeof(a) / sizeof(a[0])</code>','<code>a.size()</code>','<code>v.size()</code>'],
      ['索引','<code>[]</code> 不檢查','<code>[]</code> 不檢查；<code>.at()</code> 檢查','<code>[]</code> 不檢查；<code>.at()</code> 檢查'],
      ['整體複製／指定','不能直接以 a=b 指定整個陣列','支援值複製','支援值複製'],
      ['常見用途','理解底層與既有 C 介面','數量固定的資料','數量可能改變的一般序列']])
    family += code('三種容器，讀取方式相似',r'''#include <array>
#include <iostream>
#include <vector>
int main() {
    int raw[3] = {10, 20, 30};
    std::array<int, 3> fixed = {10, 20, 30};
    std::vector<int> dynamic = {10, 20, 30};
    dynamic.push_back(40);
    std::cout << raw[1] << ' ' << fixed.at(1) << ' '
              << dynamic.at(3) << '\n';
    std::cout << fixed.size() << ' ' << dynamic.size() << '\n';
}''','20 20 40\n3 4\n','run')
    vbool = '''<p><code>std::vector&lt;bool&gt;</code> 是為 bool 提供的特殊化版本。為了節省空間，實作可以把多個布林值壓進位元中，因此不能把它看成一排可逐個取址的 bool 物件。</p>
<p>讀取 <code>v[i]</code> 可以得到布林值，也能用 <code>v[i] = true</code> 修改。但非 const 的索引運算子回傳的是代表該位元的代理物件，不是一般 vector 的元素參考，所以不能用 <code>bool&amp; r = v[i]</code> 綁定它。學習本章的連續儲存與參考行為時，先用 <code>vector&lt;int&gt;</code> 理解即可。</p>'''
    decay = '''<p>對仍保有陣列型別的 <code>int a[3]</code>，<code>sizeof(a)</code> 是整個陣列的空間，除以一個元素的大小 <code>sizeof(a[0])</code>，就能得到元素數量 3。</p>
<p>但在 <code>int* p = a</code> 中，a 會轉換成指向第一個元素的指標，這個轉換稱為「陣列退化成指標」。p 只保存位址，不包含陣列有幾格的資訊，所以 <code>sizeof(p)</code> 算的是指標本身的大小，不能用來求陣列長度。</p>
<p>函式參數寫成 <code>const int values[]</code> 時，參數型別也會調整成 <code>const int*</code>，因此下面另外傳入 count 告訴函式元素數量：</p>'''+code('在呼叫端算出長度，和陣列一起傳入函式',r'''#include <cstddef>
#include <iostream>
void show(const int values[], std::size_t count) {
    for (std::size_t i = 0; i < count; ++i)
        std::cout << values[i] << ' ';
    std::cout << '\n';
}
int main() {
    int a[3] = {10, 20, 30};
    std::size_t count = sizeof(a) / sizeof(a[0]);
    int* p = a;
    std::cout << count << '\n';
    std::cout << p[1] << '\n';
    show(a, count);
}''','3\n20\n10 20 30 \n','run')+'''<p><code>std::array</code> 與 <code>std::vector</code> 都提供 <code>.size()</code>，不必用這個除法取得元素數量。</p>'''
    prologue='''<p>陣列是 C、C++、Java 等許多語言共有的資料型別；<code>std::vector</code> 這類動態序列也是建立在陣列之上。一個陣列<strong>只存一種型別的資料</strong>：可以有整數陣列或浮點數陣列，但不能把兩者混在同一個陣列裡。陣列只支援兩種操作：<strong>用索引讀取</strong>，以及<strong>對某個索引指定新值</strong>。</p>
<p>把陣列想成記憶體裡一整段<strong>連續的位元組</strong>，切成大小相同的格子；每格多大，由元素型別決定。因此只要知道起始位址、索引和元素大小，就能直接算出元素的位置。</p>
<p id="dx-low">在 C++ 中，一個 double 通常佔 8 bytes，所以六個 double 的陣列 <code>double a[6]</code> 共佔 <code>6 * sizeof(double)</code> = 48 bytes。陣列開始的位置稱為<strong>基底位址</strong>（base address）。<code>sizeof</code> 可以查出任何型別或物件的大小，<code>&amp;</code> 可以取得物件的位址：</p>'''
    prologue+=code('用 sizeof 與 &amp; 觀察陣列',r'''#include <iostream>
using namespace std;
int main() {
    cout << sizeof(double) << " bytes per double" << endl;
    cout << sizeof(int) << " bytes per int" << endl;
    cout << sizeof(char) << " byte per char" << endl;

    double data[6];
    cout << sizeof(data) << " bytes for the whole array" << endl;
    cout << &data[0] << " <- base address" << endl;
    cout << &data[1] << " <- 8 bytes later" << endl;
}''','8 bytes per double\n4 bytes per int\n1 byte per char\n48 bytes for the whole array\n0x7ffd5c8e1a30 <- base address\n0x7ffd5c8e1a38 <- 8 bytes later\n','run-addr')
    prologue+='''<p>位址以十六進位顯示，每次執行都可能不同；但 <code>&amp;data[1]</code> 一定比 <code>&amp;data[0]</code> 多 <code>sizeof(double)</code>（本例是 8）。int 與 double 的大小依平台而定，以 sizeof 的結果為準。</p>
<p>本章依序介紹低階陣列與 ArrayList、緊湊陣列與參考式陣列、二維矩陣如何攤平，以及 COO、DOK、線性串列三種稀疏矩陣表示。</p>'''
    prologue+=details('原生陣列、std::array、std::vector 比較', family)
    prologue+=details('vector<bool> 為什麼是例外？', vbool)
    prologue+=details('陣列退化成指標後，為什麼不能用 sizeof 算長度？', decay)
    sections['prologue']=section('prologue','低階陣列：連續、等寬的儲存格',prologue)

    L='''<h3>位址公式：一次乘法、一次加法</h3>
<p>陣列的索引運算只靠一個簡單的計算：第 i 個元素的位址是 <code>base + i × sizeof(T)</code>。例如陣列從位址 0x000040（十進位 64）開始，每個 double 佔 8 bytes，索引 4 的元素就在 64 + 4×8 = 96。不論陣列有多長，都只做一次乘法和一次加法，所以索引是 O(1)。</p>
<p>在下方點選一格，依序看「索引 → 位元組偏移 → 加上基底 → 讀寫」。最右邊的 a[6] 是陣列尾端之後的位置（one-past）：可以算出它的位址，但不能讀寫。</p>'''+widget('layout')
    L+='''<h3>兩個風險：大小固定，也不檢查邊界</h3>
<p>第一，陣列大小固定，不能一直往尾端加元素。第二，C++ 原生 <code>[]</code> 不檢查邊界：<code>int a[3]</code> 只有三格，寫入 <code>a[3]</code> 不是追加，而是越界，不會自動產生錯誤訊息。</p>
<div class="info-box warm"><span class="info-label">越界是未定義行為</span><p>在 Linux 上，越界存取常會得到「segmentation fault」，這個錯誤訊息幾乎看不出原因。但越界寫入是<strong>未定義行為</strong>：它可能改壞別的資料而沒有任何訊息，所以不能用「程式沒當掉」判斷索引合法。</p></div>
<h3>動態陣列的策略</h3>
<p><code>std::vector</code> 這類動態陣列採用以下策略：</p>
<ul class="chapter-list"><li>配置一個有<strong>額外容量</strong>的原生陣列，並記住實際用了幾格。</li><li>陣列滿了，就配置一個<strong>更大</strong>的陣列（通常是兩倍），把元素複製過去，再釋放舊陣列。元素仍連續存放，索引維持 O(1)。</li></ul>
<p>因此 vector 的 capacity() 可以大於 size()，多數 push_back() 不需要重新配置。下面用一個只存 int 的簡化類別 ArrayList 實作這個策略。</p>
<h3>ArrayList 的成員與建構</h3>
<p>類別有三個成員：<code>maxSize</code> 是目前陣列的容量；<code>lastIndex</code> 是目前的元素數量，也是下一個空位的索引；<code>myArray</code> 指向用 <code>new int[maxSize]</code> 配置的原生陣列。</p>'''
    L+=code('ArrayList 的骨架：建構子與解構子',r'''class ArrayList {
    public:
        ArrayList(int initialCapacity = 8) {
            maxSize = initialCapacity;
            lastIndex = 0;
            myArray = new int[maxSize]; // 配置原生陣列
        }
        ~ArrayList() {
            delete[] myArray;
        }
    private:
        int maxSize;
        int lastIndex;
        int* myArray;   // 原生動態陣列
};''')
    L+='''<p>建構子設定兩個整數成員，再配置 <code>maxSize</code> 格的陣列；預設容量是 8。解構子以 <code>delete[]</code> 釋放這塊陣列。接著是追加元素與查詢大小：</p>'''
    L+=code('push_back、size、empty：類別內的方法片段',r'''void push_back(int val) {
    if (lastIndex == maxSize) grow();
    myArray[lastIndex] = val;
    lastIndex++;
}
int size() {
    return lastIndex;
}
bool empty() {
    return lastIndex == 0;
}''')
    L+='''<p>操作時須維持 <code>0 ≤ lastIndex ≤ maxSize</code>。例如容量 4、元素數量 3 時，只有索引 0、1、2 是有效元素；第 3 格雖然已配置，仍是留給下一次 push_back 的空位。課程標頭另有 <code>capacity()</code> 回傳 maxSize。</p>'''
    L+=details('複製 ArrayList 物件時要注意什麼？', '<p>上面的骨架只有建構子與解構子。若直接複製物件，預設的複製只會複製 myArray 這個指標，兩個物件會共用同一塊陣列，各自解構時重複 <code>delete[]</code>。課程標頭另外寫了複製建構子與指定運算子，讓每個物件擁有自己的陣列（深層複製）。</p>')
    L+='''<h3>索引運算子：檢查範圍，再回傳參考</h3>
<p>內建的索引運算已經做了 <code>base + idx * sizeof(int)</code> 的計算；ArrayList 的 <code>operator[]</code> 先檢查索引，再交給它。索引不合法就丟出例外：</p>'''
    L+=code('ArrayList 的索引運算子：類別內的方法片段',r'''int& operator[](int idx) {
    if (0 <= idx && idx < lastIndex) {
        return myArray[idx];
    }
    throw out_of_range("index out of bounds");
}''')
    L+='''<p>回傳型別是<strong>參考</strong> <code>int&amp;</code>，也就是原元素的別名，不是複製出的整數。所以同一個運算子既能讀取 <code>a[i]</code>，也能指定 <code>a[i] = val</code>：放在讀取位置就讀其值，放在指定運算左邊就修改那一格。</p>'''
    L+=details('完整程式：讀取複本、直接指定、保留別名',code('int x 是複本，int&amp; r 是別名',r'''#include <iostream>
#include "pythonds3/cppds/arraylist.hpp"
int main() {
    ArrayList a(2);
    a.push_back(10);
    int x = a[0];       // x 是值為 10 的另一個整數
    a[0] = 42;         // 改的是陣列中的元素
    int& r = a[0];      // r 是該元素的別名
    r += 8;
    std::cout << x << ' ' << a[0] << ' ' << r << '\n';
}''','10 50 50\n','run')+'<p>擴容會刪掉舊陣列，所以擴容前取得的參考 r 之後就失效；需要時應重新用索引取得。</p>', tag=None)
    L+=details('對照：回傳 int 為何不能直接指定？',code('刻意無法編譯的反例',r'''int value() { return 10; }
int main() {
    value() = 42; // 回傳的是 int 值，不是可修改的原元素
}''',kind='compile-error')+'<p>若把索引運算子的回傳型別改成 int，讀取仍可取得複本，但 <code>a[i] = 42</code> 不能編譯。</p>')
    L+='''<h3>push_back 與 grow：滿了才換更大的陣列</h3>
<p><code>push_back</code> 先比較元素數量與容量；還有空位就直接寫入 <code>myArray[lastIndex]</code>，再把 lastIndex 加一。已滿時先呼叫 <code>grow()</code>：</p>'''
    L+=code('grow：簡化片段（完整版另有容量上限檢查）',r'''void grow() {
    int newCapacity = (maxSize == 0) ? 1 : maxSize * 2;
    int* bigger = new int[newCapacity];
    for (int i = 0; i < lastIndex; ++i)
        bigger[i] = myArray[i];
    delete[] myArray;
    myArray = bigger;
    maxSize = newCapacity;
}''')
    L+='''<p>grow 先配置新陣列，此時新舊陣列同時存在；把元素逐一複製過去後，才釋放舊陣列並更新指標與容量。只把 maxSize 改大，並不會真的多出儲存格。容量為零時先擴充到 1。</p>'''
    L+=details('課程標頭 arraylist.hpp 全文',code('pythonds3/cppds/arraylist.hpp',ARRAYLIST,kind='header')+'<p>完整版的 grow 先確認加倍後不會超過 int 的上限；insert 與 erase 先檢查索引；另有 <code>at</code>、<code>pop_back</code>、<code>clear</code> 與深層複製。</p>', tag=None)
    L+='''<h3>insert：從尾端往前搬</h3>
<p>在 ArrayList 中插入元素，要先把插入點與其後的元素都往後移一格，空出位置。下圖中 lastIndex 指向第一個空位：</p>'''
    L+=figure('insert_list.png', '插入索引 2 前，依箭頭編號從索引 5 向索引 2 倒序右移。', '先把索引 5 的值搬到空位 6，再依序搬移 4、3、2，才不會蓋掉尚未複製的值。圖中數值用來示意搬移。')
    L+='''<p>搬移時不能蓋掉還沒複製的資料，所以要<strong>從陣列尾端往插入點方向，把資料往後複製</strong>。迴圈從 lastIndex 開始、往下到 idx + 1，所以第一次是把資料複製到尚未使用的空位，之後每次覆蓋的都是已經搬走的舊值。若從插入點開始往後複製，原本的值就會永遠遺失。</p>'''
    L+=code('insert：類別內的方法片段',r'''void insert(int idx, int val) {
    if (idx < 0 || idx > lastIndex)
        throw out_of_range("insert index out of bounds");
    if (lastIndex == maxSize) grow();
    for (int i = lastIndex; i > idx; --i)
        myArray[i] = myArray[i - 1];
    myArray[idx] = val;
    ++lastIndex;
}''')
    L+='''<p>講義的 insert 片段只列出搬移與寫入；這裡沿用課程標頭的寫法，開頭先確認 <code>0 ≤ idx ≤ lastIndex</code>（允許插在尾端），陣列已滿就先 grow。最壞情況是插在索引 0，整個陣列都要往後移，所以是 O(n)；平均也要搬一半，仍是 O(n)。</p>
<h3>erase：從刪除點往後補</h3>
<p><code>erase(idx)</code> 刪除指定索引的元素：先檢查索引，再把 idx 之後的每個元素往前移一格，最後把 lastIndex 減一。</p>'''
    L+=figure('remove_list.png', '刪除 idx 後，從 idx 開始依序把右側元素往左移。', '刪除時從左往右補空位；每格取右邊一格的值。最後減少 lastIndex，原本的末項位置就不再屬於有效元素。')
    L+=code('erase：類別內的方法片段',r'''void erase(int idx) {
    checkIndex(idx); // 0 <= idx && idx < lastIndex
    for (int i = idx; i < lastIndex - 1; ++i)
        myArray[i] = myArray[i + 1];
    --lastIndex;
}''')
    L+='''<p>檢查索引是 O(1)，之後要搬移 n−1−idx 個元素。最壞情況是刪除第一個元素（idx = 0），所以也是 O(n)。刪除後，原本最後一格仍留著舊值，但它已不在有效區內。</p>
<h3>逐步觀察：push_back、grow、insert、erase</h3>
<p>選一個操作後單步執行。每一格都顯示 lastIndex（size）、maxSize（capacity）與迴圈變數 i，右側同步標出正在執行的程式行。insert 的每一步只做一次 <code>a[i] = a[i-1]</code>，所以中途會暫時出現兩個相同的值：這是複製，不是交換。</p>'''+arraylist_widget()
    L+=details('完整示範：插入、刪除與印出 size、capacity',code('ArrayList 的使用範例',r'''#include <iostream>
#include "pythonds3/cppds/arraylist.hpp"   // the complete class of this section
using namespace std;
void print(const ArrayList& a) {
    for (int i = 0; i < a.size(); i++) cout << a[i] << " ";
    cout << "(size " << a.size() << ", capacity " << a.capacity() << ")" << endl;
}
int main() {
    ArrayList myArray;
    myArray.push_back(31); myArray.push_back(77);
    myArray.push_back(17); myArray.push_back(93);
    print(myArray);
    cout << myArray[3] << " " << myArray.size() << endl;

    myArray.insert(3, 20);
    myArray.erase(0);          // remove 31, which sits at index 0
    print(myArray);

    myArray.erase(2);
    myArray[0] = 50;
    print(myArray);
    return 0;
}''','31 77 17 93 (size 4, capacity 8)\n93 4\n77 17 20 93 (size 4, capacity 8)\n50 17 93 (size 3, capacity 8)\n','run')+'<p>預設容量是 8，這裡最多只有五個元素，所以容量始終是 8；erase 不會縮小容量。</p>', tag=None)
    L+=table(['操作','ArrayList 的成本','原因'],[
        ['有效索引 []','O(1)','固定次數的檢查與位址計算'],['size／empty','O(1)','讀取已記錄的元素數量'],['push_back','攤還 O(1)；擴容那次 O(n)','多數直接填一格；擴容要複製 n 個元素'],['insert／erase','最壞 O(n)','插入或刪除點之後的元素都要搬移']])
    L+='''<p>容量從固定值開始加倍時，各次擴容搬移的元素數形成 <code>1+2+4+…</code> 的等比級數。連續 push_back n 次，搬移總量是 O(n)，平均到每次是 O(1)。這是<strong>攤還分析</strong>：不是說每次操作都一樣快，而是一連串操作的總成本平均起來是常數。</p>'''
    L+=quiz('qGrow','QUIZ · grow() 的攤還成本','從空的 ArrayList（初始容量 8，滿了加倍）連續 push_back n 個元素，總共大約搬移幾個元素？',[
        ('O(n) 個：每次 push_back 攤還 O(1)',True,'擴容發生在容量 8、16、32、…用完時，每次搬移當時的元素數。這些數量相加小於 2n，平均到每次 push_back 是常數。'),
        ('約 n² 個',False,'每次只加一格容量才會這樣：幾乎每次 push_back 都要整批搬移。加倍可以避免這種情況。'),
        ('約 n log n 個',False,'擴容次數約為 log₂n，但每次搬移量不同；由大到小看是等比級數，總和小於 2n。')])
    L+='''<div class="info-box"><span class="info-label">實務上先用 vector</span><p>實際寫程式時，建議使用 <code>vector</code>，它已處理好資源管理、複製與迭代器等細節；ArrayList 用來理解這些操作的成本。兩者有一點不同：課程 ArrayList 的 [] 會檢查索引，vector 的 [] 不檢查，要用 at 才有範圍檢查。vector 的成長倍率由實作決定，不一定是兩倍。</p></div>'''
    L+=details('用 vector 看 size、容量與邊界',code('reserve 配置容量，並不新增元素',r'''#include <iostream>
#include <stdexcept>
#include <vector>
int main() {
    std::vector<int> v;
    v.reserve(4);
    v.push_back(10);
    v.push_back(20);
    std::cout << v.size() << '\n';
    std::cout << std::boolalpha << (v.capacity() >= 4) << '\n';
    v.at(0) = 99;
    std::cout << v.at(0) << '\n';
    try { std::cout << v.at(2); }
    catch (const std::out_of_range&) { std::cout << "out of range\n"; }
}''','2\ntrue\n99\nout of range\n','run')+'<p>此時 size 是 2，索引 2 仍越界。</p>')
    L+=details('元素本身的操作也要花時間', '<p>上表把單一 int 的複製視為 O(1)。若 vector 存的是字串或其他物件，複製、移動與解構這些元素本身也有成本，分析時要一起計入。</p>')
    sections['layout']=section('layout','位址計算與 ArrayList：從索引到動態擴容',L)

    C='''<p>假設要存一組名字，例如 <code>{"Rene", "Joseph", "Janet", "Jonas", "Helen", "Virginia", ...}</code>。陣列要求每格使用相同的位元組數，但名字長短不一，要怎麼放進陣列？</p>
<p>講義的作法是存一個<strong>指標陣列</strong>（<code>string*</code>）：每格放一個固定大小的位址（64 位元環境常見 8 bytes），字串本身存在別處。雖然字串長度不同，每格大小相同，索引仍是 O(1)。這種格子裡存「到其他物件的連結」的陣列稱為<strong>參考式陣列</strong>（referential array）。</p>
<p>不過，名字不一定要用指標陣列：<code>std::string</code> 物件本身的大小固定，字元另外存放、長度可以不同，所以 <code>vector&lt;string&gt;</code> 也能直接存放名字。陣列需要的只是「每格等寬」。</p>
<h3>緊湊陣列：格子裡直接存資料</h3>
<p>C-style string 例如 <code>char s[] = "SAMPLE"</code> 是一個 char 陣列，格子裡存的是字元本身，再加上結尾的 <code>'\\0'</code>，不是指標陣列。陣列直接存放主要資料的位元（字串的情況就是字元），稱為<strong>緊湊陣列</strong>（compact array）。</p>'''
    C+=code('字串常值會自動附加終止字元',r'''char s[] = "SAMPLE";
// 等同於 char s[] = {'S','A','M','P','L','E','\0'};''')
    C+='''<pre class="memory-text">index:  0   1   2   3   4   5   6
        S   A   M   P   L   E  \\0
讀取：  S → A → M → P → L → E → \\0（停止）</pre>
<p>六個可見字元需要七格。C-style string 沒有另外記錄長度，<code>strlen(s)</code> 與 <code>cout &lt;&lt; s</code> 都是一路讀到 <code>'\\0'</code> 才停。sizeof(s) 是整個陣列的大小，包含終止字元；strlen(s) 是終止字元之前的字元數：</p>'''
    C+=code('陣列空間與字串長度',r'''#include <cstring>
#include <iostream>
int main() {
    char s[] = "SAMPLE";
    std::cout << s << '\n';
    std::cout << sizeof(s) << ' ' << std::strlen(s) << '\n';
}''','SAMPLE\n7 6\n','run')
    C+=details('少了終止字元會怎樣？',code('合法 char 陣列，但不是 C-style string',r'''char s[6] = {'S', 'A', 'M', 'P', 'L', 'E'};
// cout << s;  // 不可這樣當成 C-style string 輸出：會越界尋找 '\0' ''')+'''<p>缺少終止字元時，輸出會繼續讀到陣列後方的記憶體，這是未定義行為。已知有六個字元時，可以用長度受控的迴圈，或 <code>cout.write(s, 6)</code> 輸出。</p>
<p><code>'\\0'</code> 是數值 0 的 char；<code>'0'</code> 是可見的數字字元，在 ASCII 編碼中數值為 48，兩者不同。strlen 要逐字掃描，成本與字串長度成正比。</p>''')
    C+='''<p>緊湊結構的總記憶體用量通常低得多，因為不必另外存放一串記憶體位址。參考式陣列每格通常要 8 bytes 存位址，物件本身的空間還要另外計算。在 C++ 中，一般陣列<strong>本來就是緊湊的</strong>：元素型別決定每格佔幾個 bytes。</p>'''
    C+=code('緊湊陣列與指標陣列的大小',r'''#include <iostream>
#include <string>
using namespace std;
int main() {
    int primes[] = {2, 3, 5, 7, 11, 13, 17, 19};
    cout << sizeof(primes[0]) << " bytes per element" << endl;
    cout << sizeof(primes) << " bytes in total" << endl;
    cout << sizeof(primes) / sizeof(primes[0]) << " elements" << endl;

    string* names[3];   // a referential array: 3 pointers, 8 bytes each
    cout << sizeof(names) << " bytes for three pointers" << endl;
}''','4 bytes per element\n32 bytes in total\n8 elements\n24 bytes for three pointers\n','run')
    C+='''<h3>int a[6] 與 int* p[6]</h3>
<p>元素型別告訴<strong>編譯器</strong>每個元素用幾個 bytes：int 4 bytes、double 8 bytes、char 1 byte。比較同樣存六個整數的兩種寫法（假設 int 4 bytes、指標 8 bytes）：</p>
<ul class="chapter-list"><li><strong>緊湊</strong> <code>int a[6]</code>：陣列本體 6×4 = 24 bytes，值直接存在格子裡，沒有其他物件。</li>
<li><strong>參考式</strong> <code>int* p[6]</code>：陣列本體是六個指標，6×8 = 48 bytes；指向的六個 int 另外存放，再加 6×4 = 24 bytes。</li></ul>
<p>下方選一個索引播放，比較兩種陣列「讀出 a[i]」需要的步驟：緊湊陣列定位槽位後直接讀值；參考式陣列定位後讀到的是位址，還要沿著指標找到目標物件才讀到值。</p>'''+widget('compact')
    C+='''<p>緊湊與否看的是格子裡存的是不是主要資料本身，與容量是否等於元素數量無關：vector 預留了額外容量，元素仍直接連續存放，所以仍是緊湊的。</p>
<p><code>&lt;cstdint&gt;</code> 的固定寬度型別 <code>int32_t</code> 與 <code>int64_t</code> 保證恰好 32 與 64 位元；一般的 int 與 long 大小由實作決定，要用 sizeof 確認。</p>'''
    C+=details('Example 1：用 chrono 比較兩種走訪的時間',code('int 陣列與 vector&lt;int*&gt;：各把每個元素加一',r'''#include <chrono>
#include <iostream>
#include <vector>
using namespace std;
int main() {
    const int N = 10000;
    static int values[N];
    vector<int*> pointers;
    for (int i = 0; i < N; i++) {
        values[i] = i;
        pointers.push_back(new int(i));   // 每個 int 分開配置
    }

    auto t0 = chrono::steady_clock::now();
    for (int i = 0; i < N; i++) values[i]++;
    auto t1 = chrono::steady_clock::now();
    for (int i = 0; i < N; i++) (*pointers[i])++;
    auto t2 = chrono::steady_clock::now();

    cout << "compact:     " << chrono::duration<double, micro>(t1 - t0).count() << " us" << endl;
    cout << "referential: " << chrono::duration<double, micro>(t2 - t1).count() << " us" << endl;
    for (int* p : pointers) delete p;
}''',kind='run-free')+'<p>印出的時間依電腦、編譯選項與執行時的狀況而不同，請自己執行比較。緊湊版的資料連續排列，CPU 一次載入的快取區塊裡就有好幾個相鄰元素；指標版每次都要先讀位址、再跳到另一個位置讀值，分開配置的物件也不一定相鄰，因此通常較慢。</p>', tag=None)
    C+=details('複製值與指向原物件，修改結果不同',code('值陣列與指標陣列',r'''#include <iostream>
int main() {
    int x = 10, y = 20;
    int values[] = {x, y};
    int* pointers[] = {&x, &y};
    values[0] = 99;      // 只改陣列裡的複本
    *pointers[1] = 77;   // 改 y
    std::cout << x << ' ' << y << ' ' << values[0] << '\n';
}''','10 77 99\n','run')+'<p>指標指向的物件不一定在 heap，也可能是區域變數或靜態物件；使用時要確保目標仍然存在。</p>')
    C+=details('用 reference_wrapper 表示參考式陣列', '''<p>C++ 不允許 <code>int&amp; refs[2]</code> 這種「參考的陣列」。可以改存 <code>&lt;functional&gt;</code> 提供的 <code>std::reference_wrapper&lt;int&gt;</code>，用 <code>std::ref</code> 包住既有變數、<code>.get()</code> 取得其參考。</p>'''+code('改變被參考的值，與改變參考目標',r'''#include <functional>
#include <iostream>
int main() {
    int x = 10, y = 20;
    std::reference_wrapper<int> refs[] = {std::ref(x), std::ref(y)};
    refs[0].get() = 42;        // 修改 x
    refs[0] = std::ref(y);     // 將包裝物件改成參考 y
    refs[0].get() += 1;        // 現在修改 y
    std::cout << x << ' ' << y << '\n';
}''','42 21\n','run')+'<p>它和指標一樣不會延長目標物件的生命週期，但一定綁定某個物件，沒有 nullptr 的狀態。</p>')
    C+=(HERE/'arrays_compact_quizzes.html').read_text()
    sections['compact']=section('compact','緊湊陣列與參考式陣列：格子裡存值，還是存連結？',C)

    M='''<p>目前為止的陣列只朝一個方向排列，稱為<strong>一維陣列</strong>。許多應用需要多於一個方向的資料，最常見的是由列（row）與欄（column）組成的表格，也就是<strong>二維陣列</strong>（矩陣）。以下一律使用零起始索引。</p>'''
    M+=figure('multiarray.png','int scores[5][4]：五列四欄的表格，第一個索引是列（學生），第二個索引是欄（小考），scores[2][3] 被標示出來。','<code>scores[2][3]</code> 是第三位學生（列 2）的第四次小考（欄 3）成績：第一個索引選列，第二個索引選欄。', narrow=True)
    M+='''<p>例如 <code>int scores[5][4]</code> 存一個班級的成績：五位學生是列 <code>[0]</code>…<code>[4]</code>，每位學生四次小考是欄 <code>[0]</code>…<code>[3]</code>。超過二維的陣列也可以，例如 <code>int cube[2][3][4]</code>；它的元素同樣依序排在一段連續記憶體中。</p>
<p>二維陣列可以用巢狀大括號初始化。sizeof 除以一列的大小得到列數，一列的大小除以一個元素的大小得到欄數：</p>'''
    M+=code('用 sizeof 算出列數與欄數',r'''#include <iostream>
using namespace std;
int main() {
    // a matrix: initialize a 2D array with nested braces
    int M[2][2] = {{1, 1}, {2, 2}};

    cout << "M has " << sizeof(M) / sizeof(M[0]) << " rows and "
         << sizeof(M[0]) / sizeof(M[0][0]) << " columns, "
         << sizeof(M) << " bytes in total" << endl;
}''','M has 2 rows and 2 columns, 16 bytes in total\n','run')
    M+=figure('arraylayout.png','2×2 矩陣 M，i 是列索引、j 是欄索引；右側是各列總和 2 與 4，下方是各欄總和 3 與 3。','固定 i、沿 j 方向走是一列；固定 j、沿 i 方向走是一欄。右側是各列的總和，下方是各欄的總和。', narrow=True)
    M+='''<p>C++ 陣列沒有切片（slicing）語法：要讀一列，就固定 i、對 j 跑迴圈；要讀一欄，就固定 j、對 i 跑迴圈。</p>'''
    M+=code('讀第 0 列、第 0 欄與單一元素',r'''#include <iostream>
using namespace std;
int main() {
    int M[2][2] = {{1, 1}, {2, 2}};
    for (int j = 0; j < 2; j++) {
        cout << M[0][j] << " ";   // row 0
    }
    cout << endl;
    for (int i = 0; i < 2; i++) {
        cout << M[i][0] << " ";   // column 0
    }
    cout << endl;
    cout << M[1][1] << endl;   // row 1, column 1
}''','1 1 \n1 2 \n2\n','run')
    M+='''<p><code>M[0]</code> 本身是一整列，但直接 <code>cout &lt;&lt; M[0]</code> 印出的是這一列開頭的位址，不是列中的數值。</p>
<h3>記憶體排列：row-major 與 column-major</h3>
<p>一維陣列的索引直接對應元素在記憶體中的相對位置；二維陣列卻有列與欄，而記憶體位址只有一維，所以 (i, j) 必須轉成一維的位置。<strong>Row-major</strong> 先存完一整列，再存下一列；<strong>column-major</strong> 先存完一整欄，再存下一欄。Row-major 比較常見。</p>
<p>Row-major 時，(i, j) 前面有 i 個完整的列，每列 Cols 格，再往後 j 格，所以 <strong>offset = i × Cols + j</strong>。Column-major 時，前面有 j 個完整的欄，每欄 Rows 格，再往後 i 格，所以 <strong>offset = j × Rows + i</strong>。</p>
<div class="info-box"><span class="info-label">從索引算出位址</span><p>若起始位址是 B，每格佔 <code>s = sizeof(T)</code> bytes：</p><p><strong>Row-major：</strong>B + (i × Cols + j) × s</p><p><strong>Column-major：</strong>B + (j × Rows + i) × s</p><p>offset 是格數，乘上元素大小才是相對的位元組數。當每個元素只佔一個位置、起始位址為 x 時，講義寫成 y = x + Cols × i + j。</p></div>
<p>下方的儲存方式與走訪順序可以分開切換：切換走訪順序時，記憶體中的資料不會重排，只改變讀取順序。每一步先決定下一個 (i, j)，代入 offset 公式，再到記憶體帶上找到那一格，並顯示與前一次讀取相差多少 bytes。建議先在 row-major 下比較兩種走訪，再改成 column-major 看看。</p>'''+mapping_widget()
    M+='''<p>沿記憶體順序走訪時，每步只前進一個元素；沿著跨列的方向走時，每步跳過 Cols × sizeof(T) bytes，換欄時又回到前方。連續走訪通常較有利於快取，實際差距取決於矩陣大小與硬體。</p>
<p>C++ 的二維陣列<strong>依定義採 row-major</strong>：語言標準保證 <code>M[0][0]</code>、<code>M[0][1]</code>、<code>M[1][0]</code>、<code>M[1][1]</code> 依序相鄰。印出位址就能直接看到：</p>'''
    M+=code('印出位址，確認 row-major',r'''#include <iostream>
using namespace std;
int main() {
    int M[2][2] = {{1, 1}, {2, 2}};
    cout << &M[0][0] << " " << &M[0][1] << endl;   // 4 bytes apart
    cout << &M[1][0] << " " << &M[1][1] << endl;   // next row follows immediately
}''','0x7ffe2b4c9a90 0x7ffe2b4c9a94\n0x7ffe2b4c9a98 0x7ffe2b4c9a9c\n','run-addr')
    M+='''<p>位址每次執行都可能不同，但相鄰元素一定相差 <code>sizeof(int)</code>（本例是 4 bytes），而且 <code>M[1][0]</code> 緊接在 <code>M[0][1]</code> 之後。</p>
<p id="dx-multi">以 <code>scores[5][4]</code> 為例：<code>scores[2][3]</code> 的 row-major offset 是 2×4+3 = 11；若同一個邏輯矩陣改存成 column-major，offset 是 3×5+2 = 17。</p>
<p>需要 column-major 時，可以配置一維容器，自己用第二條公式定位。下面的迴圈把同一個 2×3 矩陣同時存成兩種排列：</p>'''
    M+=code('用兩種公式寫入一維容器',r'''for (int i = 0; i < 2; ++i)
    for (int j = 0; j < 3; ++j) {
        row[i * 3 + j] = M[i][j];   // row-major：i × Cols + j
        col[j * 2 + i] = M[i][j];   // column-major：j × Rows + i
    }''')
    M+=details('完整程式：用兩種公式保存相同的 2×3 矩陣',code('兩種排列的輸出',r'''#include <iostream>
#include <vector>
int main() {
    int M[2][3] = {{1,2,3}, {4,5,6}};
    std::vector<int> row(6), col(6);
    for (int i = 0; i < 2; ++i)
        for (int j = 0; j < 3; ++j) {
            row[i * 3 + j] = M[i][j];
            col[j * 2 + i] = M[i][j];
        }
    for (int x : row) std::cout << x << ' ';
    std::cout << '\n';
    for (int x : col) std::cout << x << ' ';
    std::cout << '\n';
}''','1 2 3 4 5 6 \n1 4 2 5 3 6 \n','run'))
    M+=details('二維 vector 與一維 vector：同樣能表示矩陣，配置不同',code('初始化、逐列走訪與攤平',r'''#include <iostream>
#include <vector>
int main() {
    const std::size_t rows = 2, cols = 3;
    std::vector<std::vector<int>> M(rows, std::vector<int>(cols, 0));
    M.at(1).at(2) = 7;
    std::vector<int> flat(rows * cols, 0);
    for (std::size_t i = 0; i < rows; ++i) {
        for (std::size_t j = 0; j < cols; ++j) {
            flat.at(i * cols + j) = M.at(i).at(j);
            std::cout << M[i][j] << ' ';
        }
        std::cout << '\n';
    }
    std::cout << flat.at(1 * cols + 2) << '\n';
}''','0 0 0 \n0 0 7 \n7\n','run')+'<p>外層 vector 連續存放的是各列的 vector 物件，不是所有 int。每列自己的 int 連續，但相鄰兩列不保證接在一起，各列長度也可以不同。單一的一維 vector 才讓所有 int 連續；使用攤平公式前，仍須分別確認 i 小於 rows、j 小於 cols。</p>')
    sections['multidim']=section('multidim','多維陣列：把矩陣放進一維記憶體',M)
    sections['sparse']=section('sparse','稀疏矩陣：COO、DOK 與線性串列',sparse_content())
    sections['reference']=section('reference','陣列家族總覽',table(['表示','空間','讀取','適合用途'],[
      ['原生陣列／std::array','O(n)','O(1)','大小固定；資料直接連續存放'],['vector&lt;T&gt;／ArrayList','O(capacity)','O(1)','大小可變；中間增刪最壞 O(n)'],['指標陣列','O(n)，目標物件另計','O(1)，多一層間接存取','元素大小不一或要共用物件'],['row-major／column-major 密矩陣','O(Rows×Cols)','O(1)','按公式定位；走訪順序影響快取'],['COO','O(nnz)','未排序時 O(nnz)','依序收集三元組，建好後再轉換'],['DOK（std::map）','O(nnz)','O(log nnz)','隨機讀寫指定座標'],['有序線性串列','O(nnz)','O(nnz)','依序走訪、合併兩個矩陣']])+'<p>nnz 是儲存的項數。固定寬度的格子讓位置可以直接計算，帶來 O(1) 索引；參考式與鏈結結構多一層間接存取。稀疏格式省下零值的空間，但每項要多存座標或指標。</p>')
    sections['recap']=section('recap','重點回顧與常見疑問',recap())
    return sections

def sparse_content():
    from sparse_examples import EXAMPLES
    s=r'''<p><strong>稀疏矩陣</strong>（sparse matrix）是大部分元素為零的矩陣。講義的判準是：非零元素個數（NNZ，Number of Non-Zero）除以總格數，若<strong>小於 0.05</strong>，就算稀疏；換句話說，稀疏度（sparsity，等於 1 減去密度）要大於 95%。</p>'''
    s+=figure('sparse_matrix.png','左邊的 5×7 密矩陣存全部 35 格；右邊只記錄 13 個非零值，沒記錄的位置視為 0。','左邊的密矩陣存下全部 35 格，右邊只記錄 13 個非零值。13／35 約 37%，遠高於 0.05：這張圖只用來說明「只記非零」的想法，真正的稀疏矩陣要空得多。')
    s+=r'''<p>存下所有零值很浪費，所以稀疏表示假設<strong>沒記錄的位置都是 0</strong>。這樣可以比對應的密矩陣省記憶體，運算也可以更快。不同的稀疏格式各有長短：通常先用<strong>適合建構</strong>的格式收集資料，準備計算時再<strong>轉成適合計算</strong>的格式。</p>
<p>以下用同一個 3×3 矩陣 A 比較三種表示；部分程式另以 B＝diag(5,6,7) 作為另一個運算元。</p>
<div class="matrix-equations"><div>$$A=\begin{bmatrix}0&2&0\\3&0&0\\0&0&4\end{bmatrix}$$</div><div>$$B=\begin{bmatrix}5&0&0\\0&6&0\\0&0&7\end{bmatrix}$$</div></div>
<h3 id="sparse-coo">COO：三條陣列的同一個索引是一筆資料</h3>
<p>最容易理解的稀疏格式是<strong>座標格式</strong>（COOrdinate，COO）：用三個子陣列分別存列、欄與值。</p>
<div class="coo-equations">$$\begin{aligned}\mathrm{row}&=[0,1,2]\\\mathrm{col}&=[1,0,2]\\\mathrm{val}&=[2,3,4]\end{aligned}$$</div>
<p>第 k 項表示 <code>A[row[k]][col[k]] = val[k]</code>；三條陣列長度相同，讀取時把同一個 k 的列、欄與值一起看。矩陣越大，省下的記憶體越可觀；管理三個子陣列的額外成本，在資料變多後就相對很小。COO 適合依序收集資料；要找某個座標時，未排序的 COO 得逐項掃描。</p>'''
    s+=details('COO 的加減乘：完整 C++ 程式與複雜度', '''<p>加減使用兩個索引，由小到大比較座標。座標較小的一邊先輸出；相同時將值相加或相減，兩邊一起前進，結果為零就不存。append 必須按 (row,col) 遞增順序加入、同一座標只加一次，加減才能這樣合併，時間與輸出空間都是 O(a+b)，a、b 是兩邊的項數。</p>
<p>乘法把每個 A(i,k) 與 B(l,j) 配對，只有 k=l 時產生對 (i,j) 的貢獻；不同 k 的貢獻要累加。設成功配對的乘積有 q 筆，先存下來再依座標排序、合併，時間為 O(ab+q log q)。</p>'''+code('COO：三條平行陣列，加法、減法與乘法',*EXAMPLES['coo'],kind='run')+'''<p>三行依序是 A+B、A−B、A×B。例如乘積的 (0,1) 是 2×6＝12，(1,0) 是 3×5＝15，(2,2) 是 4×7＝28。</p>''')
    s+='''<h3 id="sparse-dok">DOK：用座標當作 map 的鍵</h3>
<pre class="memory-text">{ (0,1):2, (1,0):3, (2,2):4 }</pre>
<p><strong>DOK</strong>（Dictionary Of Keys）和 COO 很像，差別是用一個 <strong>map，以 (row, column) 配對當鍵</strong>，把座標與值存成鍵值對。課程實作使用 <code>std::map</code>（平衡搜尋樹），查一次是 O(log nnz)；改用 <code>std::unordered_map</code>（雜湊表）平均是 O(1)。需要關聯容器的功能時可以用這個格式，但樹或雜湊表的節點比陣列佔更多記憶體。</p>
<p><code>SparseMatrix</code> 類別用 <code>map&lt;pair&lt;size_t, size_t&gt;, double&gt;</code> 存資料：鍵是列、欄配對，值是元素。讀取用 const 版本的 <code>operator()</code>，沒記錄的位置回傳 0：</p>'''
    s+=code('const 版本的 operator()：只讀',r'''class SparseMatrix {
    public:
        SparseMatrix() {}
        // read access: return the stored value, or 0 for unset positions
        double operator()(size_t i, size_t j) const {
            auto it = data.find({i, j});
            if (it != data.end()) {
                return it->second;
            }
            return 0.0;
        }
    private:
        map<pair<size_t, size_t>, double> data;
};''')
    s+=code('非 const 版本的 operator() 與 nnz：類別內的方法片段',r'''// write access: inserts the position if absent
double& operator()(size_t i, size_t j) {
    return data[{i, j}];
}

size_t nnz() const {
    return data.size();   // number of stored entries
}''')
    s+='''<p>非 const 版本回傳 <code>double&amp;</code>，所以可以寫 <code>m(i, j) = value</code>。它用 map 的 [] 取值：座標不存在時，會先插入一個值為 0 的項目。</p>
<div class="info-box warm"><span class="info-label">讀取也可能新增項目</span><p>對非 const 物件呼叫 <code>m(i, j)</code> 時，編譯器選的是非 const 版本。所以即使只寫 <code>double x = m(i, j)</code> 讀值，空位置也會被插入一筆 0。只想讀取時，透過 const 參考呼叫，就會選到只查詢的 const 版本。</p></div>'''
    s+=code('非 const 讀取會插入，const 讀取不會',r'''#include <iostream>
#include "pythonds3/cppds/sparsematrix.hpp"
int main() {
    SparseMatrix m;
    m(0, 1) = 2;
    std::cout << m.nnz() << '\n';
    double x = m(5, 5);              // 非 const 版本：插入 (5,5):0
    std::cout << x << ' ' << m.nnz() << '\n';
    const SparseMatrix& view = m;
    double y = view(7, 7);           // const 版本：只查詢
    std::cout << y << ' ' << m.nnz() << '\n';
}''','1\n0 2\n0 2\n','run')
    s+='''<p>因此 <code>nnz()</code> 回傳的 <code>data.size()</code> 是<strong>儲存的項數</strong>，不一定等於真正的非零元素個數：讀取空位置、寫入 0 或加減後相消，都可能留下值為 0 的項目。</p>
<p>關係運算直接比較兩個 map；sparsity 則依給定的列數與欄數計算 1−a/(rows×cols)，其中 a 是儲存項數。加減運算稍微複雜：任一個運算元出現的座標，都要出現在結果中。</p>'''
    s+=code('operator+：類別內的方法片段',r'''SparseMatrix operator+(const SparseMatrix& other) const {
    SparseMatrix result;
    for (const auto& item : data) {
        result.data[item.first] = item.second + other(item.first.first, item.first.second);
    }
    for (const auto& item : other.data) {
        if (data.find(item.first) == data.end()) {
            result.data[item.first] = item.second;
        }
    }
    return result;
}''')
    s+='''<p>第一個迴圈處理自己的每一項，加上 other 在同一座標的值；other 是 const 參考，所以 <code>other(...)</code> 用的是只查詢的 const 版本。第二個迴圈補上只出現在 other 的座標。減法的寫法相同。</p>
<p>乘法只需要走訪兩個運算元的非零項，這正是稀疏表示划算的地方：</p>'''
    s+=code('operator*：類別內的方法片段',r'''SparseMatrix operator*(const SparseMatrix& other) const {
    SparseMatrix result;
    for (const auto& item1 : data) {
        for (const auto& item2 : other.data) {
            if (item1.first.second == item2.first.first) {
                result(item1.first.first, item2.first.second)
                    += item1.second * item2.second;
            }
        }
    }
    return result;
}''')
    s+='''<p>只有 A 的欄索引等於 B 的列索引時，兩項相乘才會貢獻到結果的 (A 的列, B 的欄)；<code>result(...) +=</code> 用非 const 版本，第一次遇到的座標會先插入 0 再累加。從密矩陣轉換時，只把非零值放進 map：</p>'''
    s+=code('fromDenseMatrix：類別內的方法片段',r'''void fromDenseMatrix(const vector<vector<double>>& matrix) {
    for (size_t i = 0; i < matrix.size(); ++i) {
        for (size_t j = 0; j < matrix[i].size(); ++j) {
            if (matrix[i][j] != 0) {
                data[{i, j}] = matrix[i][j];
            }
        }
    }
}''')
    s+=details('SparseMatrix 完整標頭與使用範例', code('pythonds3/cppds/sparsematrix.hpp',EXAMPLES['dok_header'],kind='header')+'<p>標頭另提供以 map 建構的建構子、減法與 <code>operator&lt;&lt;</code>。下面的程式先從密矩陣轉換，再做加減乘：</p>'+code('SparseMatrix 的使用範例',*EXAMPLES['dok'],kind='run')+'<p>每一行把儲存的項目列成 (row, column): value，沒列出的位置都是 0。第三行的 (1, 1): -1 與 (2, 2): -1 是相減的結果，仍是非零。</p>', tag=None)
    s+=details('使用這個 SparseMatrix 時要注意什麼？', '''<p>類別不保存列數與欄數，因此不能自動檢查形狀或索引是否越界，sparsity 也要由呼叫端提供維度。operator== 比較的是 map 的儲存內容：一個物件存了 (0,0):0、另一個是空 map，兩者都表示零矩陣，但 == 會得到 false。fromDenseMatrix 不會先清空原有資料。</p>
<p>成本方面，加減法對每一項做 map 查詢或插入，時間上界是 O((a+b) log(a+b))；乘法的兩層迴圈要檢查所有 a×b 個項目配對。</p>''')
    s+=details('size_t 是什麼？', '''<p><code>std::size_t</code> 是 <code>&lt;cstddef&gt;</code> 提供的無號整數型別，用來表示物件大小，也是 sizeof 結果的型別。負數轉成 size_t 會變成很大的正數，所以讀入有號索引時，先確認非負且在維度內，再轉型。</p>''')
    s+='''<h3 id="sparse-linear">線性串列：按座標串成一條鏈</h3>
<p>第三種表示把每個非零項存成一個節點 <code>{row, col, value, next}</code>，依 row-major 順序串成一條串列：</p>'''
    s+=code('線性串列的節點：講義的 struct',r'''struct Node { int row, col; double value; Node* next; };''')
    s+='''<pre class="memory-text">head → (0,1,2) → (1,0,3) → (2,2,4) → nullptr</pre>'''
    s+=figure('sparse_matrixlist.png','矩陣的非零項依列、欄順序共用同一個 head；每個節點保存 row、col、value、next。','圖中的 4×5 矩陣有六個非零項，全都串在同一條串列裡。next 會跨過矩陣的列界線；空的第 2 列不需要節點。')
    s+='''<p>節點不必相鄰，要跟著 next 才找得到下一筆，所以找指定座標最壞要走過全部 nnz 個節點。兩條依座標排序的串列可以像合併一樣同時往前走。下一章會仔細說明這些指標怎麼連接。</p>'''
    s+=details('線性串列的加減乘：完整 C++ 程式與複雜度', '''<p>加減用兩個節點指標依序比較座標，做法與 COO 的合併相同；結果保存 tail，每次接到尾端只需 O(1)，整體時間 O(a+b)。乘法兩兩走訪節點，以 map 累加相同的結果座標，再依序輸出。</p>'''+code('Linear：一條有序鏈結串列，加法、減法與乘法',*EXAMPLES['linear'],kind='run')+'''<p>三行仍是 A+B、A−B、A×B。類別解構時逐一釋放節點；此版本停用複製，並以移動建構把結果串列交給接收端，避免兩個物件重複釋放同一批節點。</p>''')
    s+='''<h3>操作矩陣，對照三種儲存內容</h3><p>下面是展示格式用的 5×6 小矩陣，預設有 4 個非零項，密度約 13%，並不符合 0.05 的稀疏判準，只用來對照格式。點一個格子選取它：COO 中同一個 k 的三格、DOK 的鍵與串列中的節點會同時標出。輸入數值後按「寫入」：改成另一個非零值時項數不變；寫入 0 則刪除該項。本互動只保存非零項。</p>'''+widget('sparse')
    s+=quiz('qSpAdd','QUIZ · map 加法成本','兩個各有 n 筆儲存項的 DOK（std::map）相加，逐筆查詢與插入，時間上界為何？',[
        ('O(n log n)',True,'總共處理 O(n) 項，每項的 map 查詢或插入是對數成本。'),('O(n)',False,'O(n) 是兩條已排序序列合併的成本；這份程式逐筆操作 map。'),('O(n²)',False,'加法不需要把 A 的每一項與 B 的每一項兩兩配對；乘法才需要。')])
    s+=quiz('qSp','QUIZ · 空間取捨','為何不能只看非零項數，就斷定小矩陣用 DOK 一定省空間？',[
        ('每項還有座標、樹節點與配置的額外成本',True,'std::map 的每個節點除了鍵與值，還有連結其他節點的指標等額外空間。'),('因為 DOK 還是配置所有零值',False,'沒存入的座標不佔 map 節點。'),('因為 map 不允許零值',False,'map 可以存零；這個類別也不會自動清除零項。')])
    return s

def recap():
    r='''<ul class="chapter-list">
<li>陣列是一段連續、等寬的記憶體；第 i 個元素在 <code>base + i × sizeof(T)</code>，所以索引是 O(1)。原生陣列大小固定，也不檢查邊界。</li>
<li>ArrayList 用 <code>lastIndex</code> 記元素數量、<code>maxSize</code> 記容量；滿了就配置兩倍大的陣列再複製，push_back 攤還 O(1)。insert 從尾端往前搬、erase 從刪除點往後補，最壞 O(n)。</li>
<li>緊湊陣列直接存放主要資料；參考式陣列存放到其他物件的連結，取值要多一層間接存取，物件空間另計。</li>
<li>二維陣列要攤平成一維：row-major 的 offset = i × Cols + j，column-major 的 offset = j × Rows + i。C++ 原生二維陣列採 row-major。</li>
<li>密度（NNZ／總格數）小於 0.05 的矩陣算稀疏。COO 用三條陣列、DOK 用以座標為鍵的 map、線性串列用依座標排序的節點，都只記錄有存的項目，沒記錄的位置視為 0。本課的 DOK 在寫入 0、非 const 讀取空位置或加減相消時，可能留下值為 0 的項目。</li>
</ul>
<h3>常見疑問</h3>'''
    qa=[('為什麼索引從 0 開始？','<p>索引其實是「離起點幾格」。第一個元素就在基底位址上，偏移 0 格，位址公式 <code>base + i × sizeof(T)</code> 代入 i = 0 剛好是 base，不必再減一。</p>'),
        ('為什麼陣列的元素要同一種型別？','<p>位址公式只用一個 <code>sizeof(T)</code>，前提是每格一樣寬。若要存長短不同的資料，就讓每格存固定大小的東西，例如指標或 string 物件，真正長度不同的部分放在別處。</p>'),
        ('push_back 是不是永遠 O(1)？','<p>不是。剛好遇到容量已滿的那一次要配置新陣列並複製全部元素，是 O(n)。但加倍讓擴容越來越少發生，一連串 push_back 平均下來每次是 O(1)，這叫攤還 O(1)。</p>'),
        ('區域陣列和 new 出來的陣列有什麼不同？','<p><code>int a[6]</code> 這種區域陣列在函式的堆疊（stack）上，大小要在編譯時決定，離開作用域就自動釋放。<code>new int[n]</code> 配置在 heap（自由儲存區），大小可以在執行時決定，用完要自己 <code>delete[]</code>。兩者的元素都連續存放，索引方式相同。</p>'),
        ('COO 和 DOK 各適合什麼情況？','<p>COO 適合依序收集 (row, col, value) 三元組、一次建好，之後再轉成適合計算的格式；在未排序的 COO 中找特定座標要逐項掃描。DOK 適合反覆讀寫任意座標，std::map 每次查詢 O(log nnz)，代價是每項的節點額外空間較多。</p>')]
    return r+''.join(details(q,a) for q,a in qa)
