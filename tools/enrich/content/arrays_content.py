"""第三章教學正文。由 enrich_arrays.py 產生受管 section。"""
from pathlib import Path
from html import escape
import re
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
    if title != 'SparseMatrix：完整 C++ 類別、使用範例與加減乘':
        title = re.sub(r'^(?:補充|延伸|實作練習)：', '', title) + '（補充）'
    return f'<details class="chapter-extra"><summary>{escape(title)}</summary><div class="extra-body">{body}</div></details>'

def table(head, rows):
    return '<div class="chapter-table"><table class="cmp-table"><thead><tr>' + ''.join('<th>'+x+'</th>' for x in head) + '</tr></thead><tbody>' + ''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in rows) + '</tbody></table></div>'

def widget(name): return (HERE/f'arrays_{name}_widget.html').read_text()
def section(sid, title, body):
    return f'<section id="{sid}">\n<!-- gen:arrays-{sid} -->\n<h2>{title}</h2>\n{body}\n<!-- /gen:arrays-{sid} -->\n</section>'

def quiz(qid, title, question, answers):
    return f'<div class="quiz-box"><div class="quiz-label">{title}</div><p>{question}</p><div class="quiz-options" id="{qid}Options">'+''.join(f'<div class="quiz-opt" data-correct="{str(ok).lower()}" data-fb="{escape(fb,quote=True)}" onclick="quizCheck(\'{qid}\', this)"><span class="opt-letter">({chr(65+i)})</span> {a}</div>' for i,(a,ok,fb) in enumerate(answers))+f'</div><div class="quiz-feedback" id="{qid}Feedback"></div></div>'

def figure(filename, alt, caption):
    return f'<figure class="arrays-figure"><div class="arrays-figure-scroll" tabindex="0" aria-label="{escape(alt, quote=True)}"><img src="assets/figures/ch3/{filename}" alt="{escape(alt, quote=True)}" loading="lazy"></div><figcaption>{caption}</figcaption></figure>'

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
<p>從程式的位址模型來看，記憶體是一條按位元組編號的序列。陣列把同型別的元素排在這條序列上，<strong>元素連續儲存，每格大小相同</strong>。因此只要知道起始位址、索引和元素大小，就能直接找到元素。</p>
<p>本章依序介紹低階陣列與 ArrayList、compact／referential、二維矩陣如何攤平，以及 COO、DOK、線性串列三種稀疏表示。</p>
<p id="dx-low"><code>double a[6]</code> 佔 <code>6 * sizeof(double)</code> bytes；若此環境的 double 是 8 bytes，總共就是 48 bytes。型別大小以 sizeof 的結果為準，不同平台可能不同。</p>''')
    layout='''<p>有效索引 <code>0 ≤ i &lt; n</code> 的元素位址為 <code>base + i × sizeof(T)</code>。乘法與加法的次數不隨 n 增加，因此索引是 O(1)。以下位址與型別大小是示意。</p>'''+widget('layout')
    layout+='''<h3>兩個限制：不能直接擴增，也不會替你檢查邊界</h3>
<div class="info-box warm"><span class="info-label">越界與錯誤訊息</span><p><code>int a[3]</code> 只有三格。寫入 <code>a[3]</code> 不是追加，而是越界；原生 <code>[]</code> 不會先確認索引是否合法。即使寫入後沒有訊息或當機，這仍是<strong>未定義行為</strong>，可能改壞別的資料，也可能有其他結果。</p></div>
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
<h3>插入從右往左搬，刪除從左往右補</h3><p>在有 n 個元素的序列中，若要插入到索引 i，須先把 i 到 n−1 的元素向右搬一格，共 n−i 個。<strong>從尾端開始</strong>，才不會蓋掉還沒複製的值。刪除索引 i 則把右邊 n−1−i 個元素往左搬。insert 允許 i=n；erase 與 [] 必須 $i\\lt n$。</p>'''
    layout+=figure('insert_list.png', '插入索引 2 前，依箭頭編號從索引 5 向索引 2 倒序右移。', '先把索引 5 的值搬到空位 6，再依序搬移 4、3、2，才不會蓋掉尚未複製的值。圖中數值用來示意搬移，規則不隨元素值改變。')
    layout+=figure('remove_list.png', '刪除 idx 後，從 idx 開始依序把右側元素往左移。', '刪除時從左往右補空位；每格取右邊一格的值。最後減少 lastIndex，原本的末項位置就不再屬於有效元素。')
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
<div class="info-box"><span class="info-label">實務上先用 vector</span><p>實務上推薦 <code>vector</code>，因為它已處理資源管理、複製、迭代器等細節。從 ArrayList 的搬移過程可以理解這些操作的成本。不過，兩者介面有些差異：課程 ArrayList 的 [] 會檢查，vector 的 [] 不會；vector 要用 at 才有範圍檢查。vector 的成長倍率由實作決定，不保證每次加倍。</p></div>'''
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
<div class="info-box"><span class="info-label">從索引算出位址</span><p>若起始位址是 B，每格佔 s = sizeof(T) bytes：</p><p><strong>Row-major：</strong>B + (i × Cols + j) × s</p><p><strong>Column-major：</strong>B + (j × Rows + i) × s</p><p><strong>offset 是格數</strong>，乘上元素大小才得到相對位元組位址。</p></div>
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
    from sparse_examples import EXAMPLES
    s=r'''<p>大部分元素是零時，可以只記錄非零值的位置，<strong>未記錄的位置視為零</strong>。密矩陣需要 Rows×Cols 格；稀疏表示則另外記錄座標，省下零值的儲存空間。是否划算，還要看非零項有多少、每項需要多少額外資料。</p>
<p>以下用同一個 3×3 矩陣 A 比較三種表示。各小節的加減乘程式也沿用 A，並以 B＝diag(5,6,7) 作為另一個運算元。</p>
<div class="matrix-equations"><div>$$A=\begin{bmatrix}0&2&0\\3&0&0\\0&0&4\end{bmatrix}$$</div><div>$$B=\begin{bmatrix}5&0&0\\0&6&0\\0&0&7\end{bmatrix}$$</div></div>
<p>加減要求形狀相同；乘法要求 A 的欄數等於 B 的列數。下文以 a、b 表示兩個輸入的儲存項數。</p>
<h3 id="sparse-coo">COO：三條陣列的同一個索引是一筆資料</h3>
<div class="coo-equations">$$\begin{aligned}\mathrm{row}&=[0,1,2]\\\mathrm{col}&=[1,0,2]\\\mathrm{val}&=[2,3,4]\end{aligned}$$</div>
<p>第 k 項表示 <code>A[row[k]][col[k]] = val[k]</code>。三條陣列長度相同，讀取時把同一索引的列、欄與值一起看。未排序時，找一個座標最壞要掃過 a 筆資料；按座標排序後可以二分搜尋，但插入仍可能搬移後續元素。</p>'''
    s+=details('COO 的加減乘：完整 C++ 程式與複雜度', '''<p>加減使用兩個索引，由小到大比較座標。座標較小的一邊先輸出；相同時將值相加或相減，兩邊一起前進。結果為零就不存。</p>
<p>以下 append 按 (row,col) 遞增順序加入有效座標，同一座標只加入一次。三條陣列維持這個順序，加減便能用合併完成，時間 O(a+b)、輸出空間 O(a+b)。若資料原本未排序，要先排序並合併重複座標，另計 O(a log(a+1)+b log(b+1))。</p>
<p>乘法把每個 A(i,k) 與 B(l,j) 配對，只有 k=l 時產生對 (i,j) 的貢獻。設配對成功的乘積有 q 筆，先存下來，再依結果座標排序、合併。非空輸入的時間為 O(ab+q log(q+1))，暫存 O(q)；任一輸入為空便直接回傳。不同 k 的貢獻要累加，不能只留下最後一筆。</p>'''+code('COO：三條平行陣列，加法、減法與乘法',*EXAMPLES['coo'],kind='run')+'''<p>三行依序是 A+B、A−B、A×B。例如乘積的 (0,1) 是 2×6＝12，(1,0) 是 3×5＝15，(2,2) 是 4×7＝28。</p>''')
    s+='''<h3 id="sparse-dok">DOK：用座標當作 map 的鍵</h3>
<pre class="memory-text">{ (0,1):2, (1,0):3, (2,2):4 }</pre>
<p>DOK 以 (row,column) 當作鍵，保存該位置的值。std::map 按 row、再按 column 排序。令 $a$ 為 map 目前儲存的座標與值的筆數，查詢／插入需要 O(log(a+1))。用 <code>m(i,j) = value</code> 就能指定某個位置的值，不必自行搜尋三條陣列。</p>
<div class="info-box warm"><span class="info-label">讀取也可能新增項目</span><p><code>operator()</code> 回傳 <code>double&amp;</code>，讓 <code>m(i,j)</code> 代表 map 中那個可讀寫的值。若座標尚未存在，map 的 [] 會先插入值為零的項目；因此單純讀取空位置也會新增項目。</p></div>'''
    s+=details('size_t 是什麼？', '''<p><code>std::size_t</code> 是 <code>&lt;cstddef&gt;</code> 提供的無號整數型別，用來表示物件大小，也是 sizeof 結果的型別。<code>pair&lt;size_t,size_t&gt;</code> 把列、欄索引組成一個鍵，<code>map&lt;pair&lt;size_t,size_t&gt;,double&gt;</code> 則把這個鍵對應到 double 值。</p>
<p>無號型別仍需要邊界檢查。負數轉成 size_t 可能成為很大的正數；讀入有號索引時，先確認非負且在維度內，再轉型。不要用 <code>i &gt;= 0</code> 作為無號倒數迴圈的終止條件。</p>''')
    s+=details('SparseMatrix：完整 C++ 類別、使用範例與加減乘', '''<p>下面把建構、存取、加減乘與輸出放在完整類別中，可直接編譯執行。索引介面使用講義中回傳 double&amp; 的寫法。加減法在函式內用 find 查詢另一個矩陣，缺少的座標取零，不為了查詢而改動輸入。</p>
<p>加法第一輪處理 A 的所有鍵，第二輪補 B 獨有的鍵；減法第一輪相減，第二輪補 B 值的負值。<strong>每筆還有 map 查詢或插入的成本</strong>，時間上界為 O((a+b) log(a+b+1))，輸出空間 O(a+b)。</p>
<p>乘法保留講義的兩層迴圈。每一對項目都要檢查中間索引，即使沒有配對成功也有成本。設成功配對 q 次、累加過程出現 c 個結果座標，兩邊非空時需 O(ab+q log(c+1))，結果空間 O(c)。若 B 為空，這份寫法仍會走過 A 的 a 項。結果可能變密，也可能保留相消後的零值。</p>'''+code('SparseMatrix：以座標為鍵的 map',*EXAMPLES['dok'],kind='run')+'''<p id="dx-sp">三行依序是 A+B、A−B、A×B，與 COO 的結果相同。這個類別的 nnz() 回傳 data.size()，數的是儲存項數；寫入零、讀取空位置或相加相消，都可能讓它和真正的非零數不同。</p>''')
    s+=details('補充：使用這個 SparseMatrix 時要注意什麼？', '''<p>類別不保存 rows／cols，因此不能自動檢查形狀或索引是否越界，也無法從空 map 得知零矩陣的大小，使用時要另外記住維度。sparsity(rows,cols) 使用 1−a/(rows×cols)，須確認維度乘積有效且非零，儲存項也符合矩陣內容。</p>
<p>operator== 比較的是 map 的儲存內容。例如一個物件存了 (0,0):0，另一個是空 map，兩者都可表示零矩陣，但 == 會得到 false。要比較矩陣的數值是否相同，還須處理零項與維度。</p><p>fromDenseMatrix 會加入非零項，但不清空原有 map。要轉換另一個矩陣，請使用新物件。上方的 COO 程式與下方的串列程式另保存維度並略過零值；這裡保留 DOK 類別的行為，使用時要分清楚。</p>''')
    s+='''<h3 id="sparse-linear">Linear list：按座標串成一條串列</h3>
<pre class="memory-text">head → (0,1,2) → (1,0,3) → (2,2,4) → nullptr</pre>
<p>每個節點記錄 row、col、value 與 next，所有非零項按 (row,col) 串成同一條串列。節點不必相鄰，跟著 next 才能找到下一筆；找指定座標最壞需要 O(a)。已有前驅時接入或移除節點只需 O(1)，但尋找前驅的成本要另算。下一章會仔細說明這些指標怎麼連接。</p>'''
    s+=figure('sparse_matrixlist.png','矩陣的非零項依列、欄順序共用同一個 head；每個節點保存 row、col、value、next。','圖中的 4×5 矩陣有六個非零項，全都串在同一條串列裡。next 會跨過矩陣的列界線；空的第 2 列不需要節點。')
    s+=details('線性串列的加減乘：完整 C++ 程式與複雜度', '''<p>加減用兩個節點指標依序比較座標，做法與 COO 的合併相同。結果保存 tail，每次把新節點接到尾端只需 O(1)，因此整體時間 O(a+b)、輸出空間 O(a+b)。若每次都從 head 重新找尾端，還要加上那段走訪成本。</p>
<p>這份程式的 append 同樣要求有效座標按 (row,col) 遞增、沒有重複。乘法兩兩走訪節點，以 map 累加相同結果座標，再依序輸出串列。非空輸入的時間是 O(ab+q log(c+1)+c)，輔助 map 與輸出各用 O(c) 空間；任一輸入為空便直接回傳。q 是成功配對數，c 是累加時出現的不同座標數。</p>'''+code('Linear：一條有序鏈結串列，加法、減法與乘法',*EXAMPLES['linear'],kind='run')+'''<p>三行仍是 A+B、A−B、A×B。類別解構時逐一釋放節點；此版本停用複製，並以移動建構把結果串列交給接收端，避免兩個物件重複釋放同一批節點。</p>''')
    s+='''<h3>操作矩陣，對照三種儲存內容</h3><p>下面改用 5×6 矩陣。點格子切換零與非零，看同一筆資料如何出現在 COO、DOK 與單一串列中。這個互動會移除零項目。</p>'''+widget('sparse')
    s+=quiz('qSpAdd','QUIZ · map 加法成本','兩個各有 n 筆儲存項的 std::map DOK，逐筆查詢與插入相加，上界為何？',[
        ('O(n log(n+1))',True,'總共走訪 O(n) 項，每項 map 查詢或插入還有對數成本。'),('O(n)',False,'O(n) 是已排序序列合併的成本；這份程式逐筆操作 map。'),('O(n²)',False,'加法不需要將 A 的每項與 B 的每項兩兩配對。')])
    s+=quiz('qSp','QUIZ · 空間取捨','為何不能只看非零項數，就保證小矩陣用 DOK 一定省空間？',[
        ('每項還有座標、樹節點與配置的額外成本',True,'std::map 的節點大小依實作而定，不能假定 key+value 就是全部。'),('因為 DOK 還是配置所有零值',False,'未存入的座標不佔 map 節點。'),('因為 map 不允許零值',False,'map 可以存零，這個類別也不會自動清除零項。')])
    return s
