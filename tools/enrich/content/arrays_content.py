"""第三章教學正文。由 enrich_arrays.py 產生受管 section。"""
from pathlib import Path
from html import escape
from enrich_lib import hl
HERE = Path(__file__).parent

def code(title, src, output=None, kind='fragment'):
    attrs = f' data-cpp="{kind}"'
    if output is not None:
        attrs += ' data-expected="' + escape(output, quote=True).replace('\n', '&#10;') + '"'
    out = f'<div class="deck-extra"><div class="dx-label">{title}</div><div class="pseudo-code"{attrs}>{hl(src)}</div>'
    if output is not None:
        out += '<div class="expected-out"><span class="eo-tag">預期輸出</span><pre>' + escape(output).replace(' \n', '&#32;\n') + '</pre></div>'
    return out + '</div>'

def details(title, body):
    return f'<details class="chapter-extra"><summary>{escape(title)}</summary><div class="extra-body">{body}</div></details>'

def table(head, rows):
    return '<div class="chapter-table"><table class="cmp-table"><thead><tr>' + ''.join('<th>'+x+'</th>' for x in head) + '</tr></thead><tbody>' + ''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in rows) + '</tbody></table></div>'

def widget(name): return (HERE/f'arrays_{name}_widget.html').read_text()
def section(sid, title, body):
    return f'<section id="{sid}">\n<!-- gen:arrays-{sid} -->\n<h2>{title}</h2>\n{body}\n<!-- /gen:arrays-{sid} -->\n</section>'

def quiz(qid, title, question, answers):
    return f'<div class="quiz-box"><div class="quiz-label">{title}</div><p>{question}</p><div class="quiz-options" id="{qid}Options">'+''.join(f'<div class="quiz-opt" data-correct="{str(ok).lower()}" data-fb="{escape(fb,quote=True)}" onclick="quizCheck(\'{qid}\', this)"><span class="opt-letter">({chr(65+i)})</span> {a}</div>' for i,(a,ok,fb) in enumerate(answers))+f'</div><div class="quiz-feedback" id="{qid}Feedback"></div></div>'

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
    family += details('補充：vector<bool> 為什麼是例外？', '''<p><code>std::vector&lt;bool&gt;</code> 是為 bool 提供的特殊化版本。為了節省空間，實作可以把多個布林值壓進位元中，因此不能把它看成一排可逐個取址的 bool 物件。</p>
<p>讀取 <code>v[i]</code> 可以得到布林值，也能用 <code>v[i] = true</code> 修改。但非 const 的索引運算子回傳的是代表該位元的代理物件，不是一般 vector 的元素參考，所以不能用 <code>bool&amp; r = v[i]</code> 綁定它。學習本章的連續儲存與參考行為時，先用 <code>vector&lt;int&gt;</code> 理解即可。</p>''')
    family += details('補充：陣列退化成指標後，為什麼不能用 sizeof 算長度？', '''<p>對仍保有陣列型別的 <code>int a[3]</code>，<code>sizeof(a)</code> 是整個陣列的空間，除以一個元素的大小 <code>sizeof(a[0])</code>，就能得到元素數量 3。sizeof 在這裡不會讓陣列退化成指標。</p>
<p>但在 <code>int* p = a</code> 中，a 會轉換成指向第一個元素的指標，這個轉換稱為「陣列退化成指標」。p 只保存位址，不包含陣列有幾格的資訊。此時 <code>sizeof(p)</code> 算的是指標本身的大小，<code>sizeof(p) / sizeof(p[0])</code> 無法用來判斷陣列長度；即使剛好算出相同數字，也只是巧合。</p>
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
}''','3\n20\n10 20 30 \n','run')+'''<p>陣列本身沒有因為這個轉換而消失，a 仍是三格陣列；失去長度資訊的是接收端的指標型別。<code>std::array</code> 與 <code>std::vector</code> 都提供 <code>.size()</code>，不必用這個除法取得元素數量。</p>''')
    sections['prologue']=section('prologue','低階陣列：連續、等寬的儲存格',details('先比較：原生陣列、std::array、std::vector',family)+'''
<p>從程式的位址模型來看，記憶體是一條按位元組編號的序列。陣列把同型別的元素連續排在這條序列上，每格大小相同。因此只要知道起始位址、索引和元素大小，就能直接找到元素。</p>
<p>本章依序介紹低階陣列與 ArrayList、compact／referential、二維矩陣如何攤平，以及 COO、DOK、線性串列三種稀疏表示。</p>
<p id="dx-low"><code>double a[6]</code> 佔 <code>6 * sizeof(double)</code> bytes；若此環境的 double 是 8 bytes，總共就是 48 bytes。型別大小以 sizeof 的結果為準，不同平台可能不同。</p>''')
    layout='''<p>有效索引 <code>0 ≤ i &lt; n</code> 的元素位址為 <code>base + i × sizeof(T)</code>。乘法與加法的次數不隨 n 增加，因此索引是 O(1)。以下位址與型別大小是示意。</p>'''+widget('layout')
    layout+='''<h3>兩個限制：不能直接擴增，也不會替你檢查邊界</h3>
<p><code>int a[3]</code> 只有三格。寫入 <code>a[3]</code> 不是追加，而是越界；原生 <code>[]</code> 不會先確認索引是否合法。即使寫入後沒有訊息或當機，這仍是<strong>未定義行為</strong>，可能改壞別的資料，也可能有其他結果。</p>
<p>程式存取未映射或沒有存取權限的記憶體頁面時，執行環境可能回報 segmentation fault。作業系統通常不知道某個 C++ 陣列的元素邊界：越界一格可能仍落在可存取頁面，也可能剛好跨入不可存取頁面；不能用「走得夠遠才會出錯」判斷。空指標、懸空指標等也可能造成相同錯誤。</p>
<h3>用 ArrayList 把檢查與擴容包起來</h3>
<p>接著實作 ArrayList：內部用原生陣列儲存資料，容量不夠時擴容，索引存取前先檢查範圍。<code>myArray</code> 指向配置區，<code>lastIndex</code> 是目前元素數量，也是下一個空位；<code>maxSize</code> 是容量。操作時須維持 <code>0 ≤ lastIndex ≤ maxSize</code>。</p>
<p>例如容量 4、元素數量 3 時，只有索引 0、1、2 有效。第 3 格留給下一次 push_back；不能因為它已配置就把它當成現有元素。</p>'''
    layout+=code('ArrayList 的索引運算子：這是類別內的方法片段',r'''int& operator[](int idx) {
    if (0 <= idx && idx < lastIndex) {
        return myArray[idx];
    }
    throw out_of_range("index out of bounds");
}''')
    layout+='''<h3>為什麼回傳 int&amp;？讓 a[i] 代表陣列裡的那一格</h3>
<p><code>int&amp;</code> 是原元素的別名，不是複製出的整數。<code>a[0]</code> 先取得那一格的參考：放在讀取位置就讀其值，放在指定運算左邊就修改該格；不需要另寫一個「指定版本」的 operator[]。</p>'''
    layout+=code('讀取複本、直接指定、保留別名',r'''#include <iostream>
#include "pythonds3/cppds/arraylist.hpp"
int main() {
    ArrayList a(2);
    a.push_back(10);
    int x = a[0];       // x 是值為 10 的另一個整數
    a[0] = 42;         // 改的是陣列中的元素
    int& r = a[0];      // r 是該元素的別名
    r += 8;
    std::cout << x << ' ' << a[0] << ' ' << r << '\n';
}''','10 50 50\n','run')
    layout+=details('對照：回傳 int 為何不能直接指定？',code('刻意無法編譯的反例',r'''int value() { return 10; }
int main() {
    value() = 42; // 回傳的是 int 值，不是可修改的原元素
}''',kind='compile-error')+'<p>若把索引運算子的回傳型別改成 int，讀取仍可取得複本，但 <code>a[i] = 42</code> 不能編譯。也不能回傳函式內區域整數的參考：函式結束後該物件已不存在。ArrayList 擴容會刪掉舊陣列，因此先前取得的元素參考與指標也會失效；需要時應重新用索引取得。</p>')
    layout+=code('追加、擴容：類別內的方法片段',r'''void push_back(int val) {
    if (lastIndex == maxSize) grow();
    myArray[lastIndex++] = val;
}
void grow() {
    if (maxSize > numeric_limits<int>::max() / 2)
        throw length_error("capacity too large");
    int newCapacity = (maxSize == 0) ? 1 : maxSize * 2;
    int* bigger = new int[newCapacity];
    for (int i = 0; i < lastIndex; ++i)
        bigger[i] = myArray[i];
    delete[] myArray;
    myArray = bigger;
    maxSize = newCapacity;
}''')
    layout+='''<p>建構時配置 <code>new int[maxSize]</code>，解構時以 <code>delete[] myArray</code> 釋放；容量為零時先擴充到 1。grow 先配置新空間、複製元素，再釋放舊空間；只把容量數字改大，並不會真的得到更多儲存格。</p>
<h3>插入從右往左搬，刪除從左往右補</h3><p>在有 n 個元素的序列中，若要插入到索引 i，須先把 i 到 n−1 的元素向右搬一格，共 n−i 個。從尾端開始才不會蓋掉還沒複製的值。刪除索引 i 則把右邊 n−1−i 個元素往左搬。insert 允許 i=n；erase 與 [] 必須 i&lt;n。</p>'''
    layout+=code('插入與刪除：類別內的方法片段',r'''void insert(int idx, int val) {
    if (idx < 0 || idx > lastIndex)
        throw out_of_range("insert index out of bounds");
    if (lastIndex == maxSize) grow();
    for (int i = lastIndex; i > idx; --i)
        myArray[i] = myArray[i - 1];
    myArray[idx] = val;
    ++lastIndex;
}
void erase(int idx) {
    checkIndex(idx); // 檢查 0 <= idx && idx < lastIndex
    for (int i = idx; i < lastIndex - 1; ++i)
        myArray[i] = myArray[i + 1];
    --lastIndex;
}''')
    layout+=table(['操作','ArrayList／一般 vector 的成本','原因'],[
        ['有效索引 []／at','O(1)','固定次數的檢查與位址定位'],['size／empty','O(1)','讀取已記錄的元素數量'],['push_back','攤還 O(1)，擴容那次 O(n)','多數直接填一格；擴容須搬移 n 個元素'],['insert／erase','最壞 O(n)','插入或刪除點後的元素須搬移'],['pop_back','O(1)','移除尾端，不搬移前面的元素']])
    layout+=details('補充：元素本身的操作也要花時間', '<p>上表將單一元素的複製、移動與解構視為 O(1)，先看需要處理多少個元素。若 vector 存的是字串或其他物件，這些操作本身也可能有額外成本，分析時要一起計入。</p><p>例如 pop_back 不必搬移其他元素，但仍會解構被移除的物件；插入與擴容則可能複製或移動多個元素。</p>')
    layout+='''<p>從固定小容量開始加倍，搬移量形成 <code>1+2+4+…</code> 的等比級數。連續追加 n 次，全部搬移量是 O(n)，連同 n 次放入，平均攤到每次 O(1)。這是<strong>攤還分析</strong>，不是說每次操作都一樣快，也不需要假設隨機輸入。</p>
<p>實務上推薦 <code>vector</code>，因為它已處理資源管理、複製、迭代器等細節。從 ArrayList 的搬移過程可以理解這些操作的成本。不過，兩者介面有些差異：課程 ArrayList 的 [] 會檢查，vector 的 [] 不會；vector 要用 at 才有範圍檢查。vector 的成長倍率由實作決定，不保證每次加倍。</p>'''
    layout+=details('用 vector 看 size、容量與邊界',code('reserve 配置容量，並不新增元素',r'''#include <iostream>
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
}''','2\ntrue\n99\nout of range\n','run')+'<p>此時 size 是 2，索引 2 仍越界。課程標頭另提供 ArrayList 的深層複製、const 索引及容量檢查；含 new[]／delete[] 的簡化骨架不可直接依賴預設淺層複製。</p>')
    sections['layout']=section('layout','低階陣列與 ArrayList：從位址計算到動態擴容',layout)
    compact='''<p><strong>Compact</strong> 指主要資料直接放在陣列格子內，例如 <code>int values[]</code>。<strong>Referential</strong> 則在格子裡保存到其他物件的連結，例如 <code>int* pointers[]</code>。兩者的格子都連續、等寬，差別是取出格子內容後，是否還要跟著連結取得主要資料。</p>
<p>指標指向的物件不一定在 heap，也可能是區域變數或靜態物件。指標大小依實作而定；64-bit 環境常見 8 bytes，但應以 sizeof 判斷。長短不同的名字也可放在 <code>vector&lt;string&gt;</code>：每個 string 物件大小相同，管理的字元數量可以不同，不必一律改用指標陣列。</p>'''+widget('compact')
    compact+=code('複製值與指向原物件，修改結果不同',r'''#include <iostream>
int main() {
    int x = 10, y = 20;
    int values[] = {x, y};
    int* pointers[] = {&x, &y};
    values[0] = 99;      // 只改陣列裡的複本
    *pointers[1] = 77;   // 改 y
    std::cout << x << ' ' << y << ' ' << values[0] << '\n';
}''','10 77 99\n','run')
    compact+=details('用 reference_wrapper 表示參考式陣列', '''<p>C++ 不允許 <code>int&amp; refs[2]</code> 這種「參考的陣列」。可以改存 <code>&lt;functional&gt;</code> 提供的 <code>std::reference_wrapper&lt;int&gt;</code> 物件，用 <code>std::ref</code> 包住既有變數、<code>.get()</code> 取得其參考。</p>'''+code('改變被參考的值，與改變參考目標',r'''#include <functional>
#include <iostream>
int main() {
    int x = 10, y = 20;
    std::reference_wrapper<int> refs[] = {std::ref(x), std::ref(y)};
    refs[0].get() = 42;        // 修改 x
    refs[0] = std::ref(y);     // 將包裝物件改成參考 y
    refs[0].get() += 1;        // 現在修改 y
    std::cout << x << ' ' << y << '\n';
}''','42 21\n','run')+table(['性質','值陣列','指標陣列','reference_wrapper 陣列'],[
        ['修改原物件','存入時是複本，之後互不影響','以 *p 存取原物件','以 .get() 存取原物件'],['空值','依元素型別','可以存 nullptr','須綁定物件，沒有 nullptr 狀態'],['改變目標','指定新值','可改指向其他物件','指定另一個 wrapper 可重新綁定'],['生命週期','陣列擁有元素','不會自動延長目標生命週期','不會自動延長目標生命週期']])+'<p>兩種間接表示都要確保目標仍存在；reference_wrapper 不是生命週期管理工具，也不保證比指標更省空間。</p>')
    compact+='''<p id="dx-comp">比較儲存空間：n 個 int 的 compact 陣列佔 <code>n * sizeof(int)</code>；指標陣列本身佔 <code>n * sizeof(int*)</code>，目標物件另外計算。若多個指標共用同一個物件，計算總空間時只計入該物件一次。Compact 不等於「容量必須剛好等於大小」；vector 即使預留容量，元素仍直接連續儲存。</p>'''
    chars='''<p>C-style string 沒有另外儲存字串長度，必須以特殊字元 <code>'\\0'</code> 告訴程式：「字串到這裡結束」。</p>'''+code('字串常值會自動附加終止字元',r'''char s[] = "SAMPLE";
// 等同於 char s[] = {'S','A','M','P','L','E','\0'};''')+'''<pre class="memory-text">index:  0   1   2   3   4   5   6
        S   A   M   P   L   E  \\0
讀取：  S → A → M → P → L → E → \\0（停止）</pre>
<p>六個可見字元需要七格。<code>strlen(s)</code>、<code>cout &lt;&lt; s</code> 與 <code>printf("%s", s)</code> 都依賴終止字元；輸出字串的概念可用下列迴圈理解：</p>'''+code('概念上的逐字元輸出',r'''int i = 0;
while (s[i] != '\0') {
    cout << s[i];
    ++i;
}''')+code('陣列空間與字串長度',r'''#include <cstring>
#include <iostream>
int main() {
    char s[] = "SAMPLE";
    std::cout << s << '\n';
    std::cout << sizeof(s) << ' ' << std::strlen(s) << '\n';
    std::cout << static_cast<int>('\0') << '\n';
}''','SAMPLE\n7 6\n0\n','run')+code('合法 char 陣列，但不是 null-terminated C string',r'''char s[6] = {'S', 'A', 'M', 'P', 'L', 'E'};
// cout << s;  // 不可這樣當成 C string 使用：會越界尋找 '\0' ''')+'''<p>缺少終止字元時，操作可能繼續讀到後方記憶體，印出垃圾或造成非法存取；一旦越界就已是未定義行為，不能保證最終一定遇到零。若已知有六個字元，可用長度受控的迴圈，或 <code>cout.write(s, 6)</code> 輸出。</p>
<p><code>'\\0'</code> 是數值 0 的 char；<code>'0'</code> 是可見的數字字元，在 ASCII 編碼中數值為 48，兩者不同。sizeof(s) 計算整個陣列的空間，包含終止字元；strlen(s) 計算第一個終止字元前的字元數，須逐個掃描，成本 O(L)。</p>'''
    compact+=details('字元陣列與 C-style string：為什麼 SAMPLE 需要七格？',chars)
    compact+=(HERE/'arrays_compact_quizzes.html').read_text()
    sections['compact']=section('compact','Compact 與 Referential：格子裡存值，還是連結？',compact)
    multi='''<p>矩陣有 Rows 列、Cols 欄，但程式使用的記憶體位址是一維的。因此二維索引 (i,j) 必須轉成一維位置；這是<strong>邏輯形狀</strong>與<strong>實際儲存順序</strong>的區別。以下一律使用零起始索引、row＝列、column＝欄。</p>
<h3>先算跳過幾格，再換成位元組</h3>
<p>Row-major 先放完整的一列：前面有 i 列，每列 Cols 格，然後再走 j 格，所以 <strong>offset = i × Cols + j</strong>。Column-major 先放完整的一欄：前面有 j 欄，每欄 Rows 格，再走 i 格，所以 <strong>offset = j × Rows + i</strong>。</p>
<p>若起始位址是 B，每格佔 s = sizeof(T) bytes，位址公式分別為 <strong>B + (i × Cols + j) × s</strong> 與 <strong>B + (j × Rows + i) × s</strong>。offset 是格數，不能與 byte 位址混用。</p>
<p>C++ 原生 <code>T M[Rows][Cols]</code> 是「陣列的陣列」，採 row-major；一列的 Cols 個元素放完才接下一列。需要 column-major 時，可以用一維容器配合第二條公式表示。</p>'''
    multi+=(HERE/'arrays_mapping.html').read_text()
    multi+='''<h3>相同的儲存排列，也能用不同順序走訪</h3><p>下方固定採 row-major 儲存，只改變讀取順序。沿同一欄由上一列往下一列走時，跨距是 Cols × sizeof(T) bytes；換欄時會回到較前方的位址。連續走訪通常有利於快取，但實際差距取決於矩陣大小、硬體與運算內容。</p>'''+widget('multidim')
    multi+=code('用兩種公式保存相同的 2×3 矩陣',r'''#include <iostream>
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
}''','1 2 3 4 5 6 \n1 4 2 5 3 6 \n','run')
    multi+='''<p id="dx-multi">講義的 <code>students[100][4]</code>：<code>students[5][3]</code> 的 row-major offset 是 5×4+3＝23；同一邏輯矩陣若改存 column-major，offset 是 3×100+5＝305。再乘元素大小才得到相對位元組位址。公式描述佈局，不代表可以拿指向第一列的 int* 跨越該列進行 C++ 指標運算。</p>'''
    multi+=details('二維 vector 與一維 vector：同樣能表示矩陣，配置不同',code('初始化、逐列走訪與攤平',r'''#include <iostream>
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
}''','0 0 0 \n0 0 7 \n7\n','run')+'<p>外層 vector 連續存放的是各列的 vector 物件，不是所有 int。每列自己的 int 連續，不保證相鄰兩列的 int 接在一起，而且各列長度可以不同。單一 flat vector 的所有 int 才連續；使用攤平公式前仍須分別確認 i&lt;rows、j&lt;cols，因為錯誤的 j 可能算出仍在 flat 範圍內的位置。</p>')
    sections['multidim']=section('multidim','多維陣列：把 logical matrix 放入一維記憶體',multi)
    sections['sparse']=section('sparse','稀疏矩陣：COO、DOK 與線性串列',sparse_content())
    sections['reference']=section('reference','陣列家族總覽',table(['表示','空間','讀取','適合用途／限制'],[
      ['原生陣列／std::array','O(n)','O(1)','大小固定；資料直接連續存放'],['vector&lt;T&gt;','O(capacity)','O(1)','動態大小；中間增刪最壞 O(n)'],['指標／reference_wrapper 陣列','O(n)，目標另計','O(1)，多一層間接存取','可共享物件；須維持目標生命週期'],['row-major／column-major 密矩陣','O(Rows×Cols)','O(1)','按公式定位；走訪順序影響快取'],['COO','O(a)','未排序 O(a)；排序後可 O(log(a+1))','適合收集三元組；更新可能搬移'],['DOK（std::map）','O(a)','O(log(a+1))','按座標查找；每項另有樹節點成本'],['有序單一鏈結串列','O(a)','O(a)','合併走訪方便；不能隨機跳到第 i 個節點']])+'<p>a 是儲存項數。固定寬度的資料、可直接計算的位置帶來 O(1) 索引；參考式結構與鏈結結構增加間接存取。稀疏格式省下零值空間，但需多存座標或指標，也不保證每種運算都更快。</p>')
    return sections

def sparse_content():
    s='''<p>大部分元素是零時，可以只記錄非零值的位置，未記錄的位置視為零。密矩陣要 O(Rows×Cols) 空間；下列三種表示儲存 a 項需 O(a) 空間，但每項還要保存座標或連結。講義以非零比例低於 5% 作為例子，5% 不是通用定義或必然省空間的分界。</p>
<p>先看同一個 3×3 矩陣 A：下列三種表示描述完全相同的資料。</p><pre class="memory-text">A = [0 2 0]
    [3 0 0]
    [0 0 4]</pre>
<h3>COO：三條陣列的同一個索引是一筆資料</h3>
<pre class="memory-text">row = [0, 1, 2]
col = [1, 0, 2]
val = [2, 3, 4]</pre>
<p>第 k 項表示 <code>A[row[k]][col[k]] = val[k]</code>。三條陣列長度必須相同；也可用含 row、col、value 的三元組陣列表達同樣資訊。收集資料時追加方便，但未排序時查一個座標須掃 O(a)。按 (row,col) 排序且座標唯一後，可以二分搜尋 O(log(a+1))；在有序陣列中插入仍可能搬移 O(a) 項。</p>
<p>若輸入含重複座標，須先決定它們是相加的貢獻還是覆寫。本節運算先把重複座標加總、刪除零值，得到座標唯一的表示。</p>
<h3>DOK：用座標當作 map 的鍵</h3>
<pre class="memory-text">{ (0,1):2, (1,0):3, (2,2):4 }</pre>
<p><code>map&lt;pair&lt;size_t,size_t&gt;,double&gt;</code> 的鍵是 (row,column)，值是 double。std::map 依鍵排序，pair 先比 row，再比 column，正好是 row-major 的座標順序。查詢／插入成本為 O(log(a+1))；它不是平均 O(1) 的雜湊表。</p>
<h3>size_t 是什麼？</h3>
<p><code>std::size_t</code> 是 <code>&lt;cstddef&gt;</code> 提供、用於物件大小的無號整數型別，也是 sizeof 結果的型別。容器大小與索引常使用它，但位元寬度依平台決定，不一定是 unsigned int。<code>pair&lt;size_t,size_t&gt;</code> 就是一對用這種型別保存的列、欄索引。</p>
<p>無號型別仍需要邊界檢查。負數轉成 size_t 可能成為很大的正數；讀入有號索引時，應先檢查非負且在維度內，再轉型。避免用 <code>i &gt;= 0</code> 作為無號倒數迴圈的終止條件。</p>'''
    s+=code('DOK 的兩種存取：類別內的方法片段',r'''// private:
map<pair<size_t, size_t>, double> data;
// public:
double operator()(size_t i, size_t j) const {
    auto it = data.find({i, j});
    return it != data.end() ? it->second : 0.0;
}
double& operator()(size_t i, size_t j) {
    return data[{i, j}];
}
size_t nnz() const { return data.size(); }''')
    s+='''<p>const 版本用 find 查詢，不存在便回傳 0；非 const 版本透過 map 的 [] 取得可寫入的參考，鍵不存在時會先插入值為零的項目。這個多載由物件是否為 const 決定，<strong>不是由你打算讀或寫來決定</strong>。</p>
<h3>A.4.3 Linear list：按座標串成一條串列</h3>
<pre class="memory-text">head → (0,1,2) → (1,0,3) → (2,2,4) → nullptr</pre>'''
    s+=code('每個節點保存座標、值與下一個節點',r'''struct Node {
    int row, col;
    double value;
    Node* next;
};''')
    s+='''<p>講義的表示是一條依 (row,col) 排序的鏈結串列。節點不必相鄰，依 next 才能找到下一筆；找指定座標最壞 O(a)。已有前驅時接入或移除節點 O(1)，但找到前驅仍可能 O(a)。每列各設一個串列入口是另一種延伸設計，不是此處的單一串列。</p>
<h3>操作矩陣，對照三種儲存內容</h3><p>下方使用 5×6 矩陣；點格子切換零與非零，觀察相同資料如何出現在三種表示裡。</p>'''+widget('sparse')
    s+='''<h3>加減乘：先定義工作量</h3>
<p>a、b 是輸入 A、B 的儲存項數；q 是符合 <code>A(i,k)</code> 與 <code>B(k,j)</code> 的項目配對數，c 是結果在累加過程中出現的不同座標數（含最後相消為零的座標）。加減要求形狀相同；乘法要求 A 的欄數等於 B 的列數。</p>
<p>以 B＝diag(5,6,7) 為例，A+B 的三列是 [5,2,0]、[3,6,0]、[0,0,11]；A−B 是 [−5,2,0]、[3,−6,0]、[0,0,−3]；A×B 是 [0,12,0]、[15,0,0]、[0,0,28]。</p>'''
    merge=code('合併兩個有序序列（偽碼；減法把 B 的值乘 −1）',r'''while A 或 B 還有項目:
    若 B 已結束，或（A 未結束且 A 的座標較小）:
        輸出 A 的項目；前進 A
    否則若 A 已結束，或 B 的座標較小:
        輸出 (B.row, B.col, sign * B.value)；前進 B
    否則:
        sum = A.value + sign * B.value
        若 sum != 0: 輸出共同座標與 sum
        同時前進 A、B''',kind='pseudocode')
    s+=details('COO 的 +、−、×：排序、合併與累加', '''<p>加減先確保兩邊按 (row,col) 排序、座標唯一，再用兩個索引合併。每筆最多走過一次，時間 O(a+b)，結果最多 a+b 項。若原本未排序，另加 O(a log(a+1)+b log(b+1)) 的排序成本。</p>'''+merge+code('COO 乘法（偽碼）',r'''products = 空三元組陣列
for 每筆 (i,k,x) in A:
    for 每筆 (l,j,y) in B:
        if k == l: products.push_back((i,j,x*y))
依 (row,col) 排序 products
合併相同座標的值，略過總和為零者''',kind='pseudocode')+'''<p>兩兩檢查 O(ab)，產生 q 筆乘積後排序 O(q log(q+1))、合併 O(q)，總時間 O(ab+q log(q+1))，暫存 O(q)。不同的 k 可能貢獻給同一個 (i,j)，不能只留下最後一筆。空輸入直接回傳空結果。</p>''')
    s+=details('DOK 的 +、−、×：把 map 的成本也算進去',code('加法：講義類別內的方法；減法同理',r'''SparseMatrix operator+(const SparseMatrix& other) const {
    SparseMatrix result;
    for (const auto& item : data) {
        result.data[item.first] = item.second
            + other(item.first.first, item.first.second);
    }
    for (const auto& item : other.data) {
        if (data.find(item.first) == data.end())
            result.data[item.first] = item.second;
    }
    return result;
}''')+'''<p>第一輪處理 A 的所有鍵，第二輪補 B 獨有的鍵；每筆還有樹狀 map 查詢或插入，因此上界是 O((a+b) log(a+b+1))，結果空間 O(a+b)。減法第一輪改成相減，第二輪放入 B 值的負值；不能只把第一輪的加號改掉。</p>'''+code('乘法：講義類別內的方法',r'''SparseMatrix operator*(const SparseMatrix& other) const {
    SparseMatrix result;
    for (const auto& x : data) {
        for (const auto& y : other.data) {
            if (x.first.second == y.first.first)
                result(x.first.first, y.first.second)
                    += x.second * y.second;
        }
    }
    return result;
}''')+'''<p>即使 k 不相等，內外迴圈仍會檢查那一對項目，分析成本時也要計入。時間是 O(ab+q log(c+1))，結果儲存 O(c)；空輸入可直接回傳。稀疏乘積可能變密，c 可能接近結果的全部格數。</p>''')
    s+=details('Linear list 的 +、−、×：走訪節點如何完成運算？','''<p>加減使用兩個節點指標，依座標合併；結果維護 tail，才能每次 O(1) 接上新節點。時間 O(a+b)，輸出空間 O(a+b)。若每次輸出都從 head 重新找尾端，還要加上這段走訪的成本。</p>'''+merge+code('單一串列乘法，使用輔助 map 累加（偽碼）',r'''acc = 空 map，鍵為 (row,col)，值為累加值
for p 從 A.head 沿 next 走:
    for t 從 B.head 沿 next 走:
        if p.col == t.row:
            acc[(p.row,t.col)] += p.value * t.value
依 acc 的座標順序走訪:
    若值不為零，以 tail 接到結果串列尾端''',kind='pseudocode')+'''<p>仍須 O(ab) 配對檢查，q 次累加共 O(q log(c+1))，輸出另需 O(c)。輔助 map 與結果各用 O(c) 空間。這裡借用 DOK 累加各座標的值。若改成在結果串列逐筆尋找座標，每次可能需要 O(c)，無法直接以 O(1) 定位。</p>''')
    s+=details('SparseMatrix 使用例與教學類別的限制',code('直接使用課程標頭進行加減乘',r'''#include <iostream>
#include "pythonds3/cppds/sparsematrix.hpp"
int main() {
    SparseMatrix A({{{0,1},2}, {{1,0},3}, {{2,2},4}});
    SparseMatrix B({{{0,0},5}, {{1,1},6}, {{2,2},7}});
    std::cout << A + B << '\n' << A - B << '\n' << A * B << '\n';
    const SparseMatrix& readOnly = A;
    std::cout << readOnly(0,0) << ' ' << A.nnz() << '\n';
    double zero = A(0,0); // 非 const 存取，會插入零項目
    std::cout << zero << ' ' << A.nnz() << '\n';
}''','(0, 0): 5  (0, 1): 2  (1, 0): 3  (1, 1): 6  (2, 2): 11  \n(0, 0): -5  (0, 1): 2  (1, 0): 3  (1, 1): -6  (2, 2): -3  \n(0, 1): 12  (1, 0): 15  (2, 2): 28  \n0 3\n0 4\n','run')+'''<p id="dx-sp">課程類別提供 nnz() 與 sparsity()，但 data.size() 實際數的是儲存項目。寫入零、讀取非 const 物件的空位置，或加減相消都可能留下零項目，因此它不一定等於數學上的非零數。上方互動示範會刪除零項目，兩者行為不同。</p>
<p>類別本身不保存 rows／cols，所以不能自動檢查矩陣形狀或越界，也不能從空 map 判斷零矩陣大小。使用者須另記維度。sparsity(rows,cols) 的公式是 1−a/(rows×cols)，使用時須確認維度乘積有效且非零，儲存項也符合矩陣內容。fromDenseMatrix 會加入非零項但不清空舊 map；要完整轉換新的矩陣，請使用新物件。</p>''')
    s+=quiz('qSpAdd','QUIZ · map 加法成本','兩個各有 n 筆儲存項的 std::map DOK，依講義逐筆查詢與插入相加，上界為何？',[
        ('O(n log(n+1))',True,'總共走訪 O(n) 項，每項 map 查詢或插入還有對數成本。'),('O(n)',False,'O(n) 是已排序序列合併的成本；講義這份程式逐筆操作 map。'),('O(n²)',False,'加法不需要將 A 的每項與 B 的每項兩兩配對。')])
    s+=quiz('qSp','QUIZ · 空間取捨','為何不能只看非零項數，就保證小矩陣用 DOK 一定省空間？',[
        ('每項還有座標、樹節點與配置的額外成本',True,'std::map 的節點大小依實作而定，不能假定 key+value 就是全部。'),('因為 DOK 還是配置所有零值',False,'未存入的座標不佔 map 節點。'),('因為 map 不允許零值',False,'map 可以存零，課程類別也不會自動清除零項。')])
    return s
