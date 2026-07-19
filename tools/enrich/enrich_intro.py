#!/usr/bin/env python3
"""introduction.html 完整自學充實：依講義 01 逐節補完整範例碼＋預期輸出。冪等。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib import hl, card, ensure_style, insert_end_of_section

PAGE = Path.home() / "ds-cpp-selfstudy/introduction.html"
s = PAGE.read_text()
s = ensure_style(s)

# ---------- P01 types ----------
types_html = f'''<h3 id="dx-types">講義完整範例：把運算子親手跑一遍</h3>
<p>下面三段是講義 01 的原始示範，值得抄進編譯器跑一次。第一段的重點是<strong>整數除法會截斷</strong>：
兩個 int 相除結果還是 int，小數部分直接丟掉；只要有一邊是 double，就變成浮點除法。</p>
{card("講義 01 · 算術運算子與整數除法", """using namespace std;
cout << 2 + 3 * 4 << endl;
cout << (2 + 3) * 4 << endl;
cout << pow(2, 10) << endl;
cout << 6 / 3 << endl;
cout << 7 / 3 << endl;   // 整數除法：截斷！
cout << 7.0 / 3 << endl; // 有一個 double，就是浮點除法
cout << 7 % 3 << endl;
cout << pow(2, 100) << endl; // double 的近似值，不是精確整數""",
"14\\n20\\n1024\\n2\\n2\\n2.33333\\n1\\n1.26765e+30",
note="pow() 回傳 double：2<sup>100</sup> 印出來是 1.26765e+30 這種科學記號近似值，不是精確整數。要大整數得另找函式庫。")}
{card("講義 01 · 比較運算子與一個大陷阱", """using namespace std;
cout << boolalpha;
cout << (5 == 10) << endl;
cout << (10 > 5) << endl;
cout << ((5 >= 1) && (5 <= 10)) << endl;
cout << ((1 < 5) || (10 < 1)) << endl;

// 注意：連鎖比較不是你想的那樣！
cout << (10 < 5 < 3) << endl;  // (10 < 5) 先算出 0，然後 0 < 3 是 true！""",
"false\\ntrue\\ntrue\\ntrue\\ntrue")}
<div class="warn-box"><b>⚠️ 連鎖比較陷阱：</b>數學課寫的 10 &lt; 5 &lt; 3 在 C++ 是合法程式，
但意思是 (10 &lt; 5) &lt; 3：先算出 false（也就是 0），再算 0 &lt; 3 得到 true。
範圍判斷一律拆成兩段用 <code>&amp;&amp;</code> 接：<code>(3 &lt; x) &amp;&amp; (x &lt; 5)</code>。</div>
{card("講義 01 · bool 悄悄變 int", """using namespace std;
int the_sum = 0;
cout << the_sum << endl;

the_sum = the_sum + 1;
cout << the_sum << endl;

the_sum = true;  // 合法，但 bool 被轉成 int 的 1
cout << the_sum << endl;""",
"0\\n1\\n1",
note="C++ 允許 bool 和數值互轉：true 是 1、false 是 0。方便，但也是 bug 溫床：<code>if (x = 1)</code>（少個等號）永遠為真而且編譯得過。")}'''
s, ch1 = insert_end_of_section(s, "types", types_html, 'id="dx-types"')

# ---------- P02 pointers ----------
ptr_html = f'''<h3 id="dx-ptr">講義完整範例：位址親眼看一次</h3>
{card("講義 01 · 取址、存址、解參考", """using namespace std;
int var_n = 100;
int *ptr_n = &var_n;   // ptr_n 存的是 var_n 的位址

cout << "value of var_n:   " << var_n << endl;
cout << "address of var_n: " << &var_n << endl;
cout << "ptr_n stores:     " << ptr_n << endl;
cout << "*ptr_n gives:     " << *ptr_n << endl;""",
"value of var_n:   100\\naddress of var_n: 0x7ffd4c2a5b44\\nptr_n stores:     0x7ffd4c2a5b44\\n*ptr_n gives:     100",
note="位址每次執行都不一樣（0x 開頭的十六進位數），但第二、三行一定相同：ptr_n 存的就是 var_n 的位址。")}
{card("講義 01 · 透過指標改值", """using namespace std;
int var_n = 100;
int *ptr_n = &var_n;

*ptr_n = 50;             // 從「另一扇門」走進同一格記憶體
cout << var_n << endl;   // var_n 變成 50""",
"50",
note="這一行是整章的關鍵畫面：*ptr_n = 50 改的不是 ptr_n，是它<strong>指向的那格記憶體</strong>。之後的鏈結串列、樹、圖全靠這個動作把結構串起來。")}'''
s, ch2 = insert_end_of_section(s, "pointers", ptr_html, 'id="dx-ptr"')

# ---------- P03 collections ----------
coll_html = f'''<h3 id="dx-coll">講義完整範例：五種容器逐一跑過</h3>
<p>表格看熟之後，把講義的示範程式親手跑一遍，輸出先用腦袋預測再對答案。</p>
{card("講義 01 · vector：增刪改", """using namespace std;
vector<double> my_list = {1024, 3, 1, 6.5};

my_list.push_back(0);                      // 加到尾端
for (double x : my_list) cout << x << " ";
cout << endl;

my_list.insert(my_list.begin() + 2, 4.5);  // 插進索引 2
for (double x : my_list) cout << x << " ";
cout << endl;

my_list.pop_back();                        // 移除最後一項
my_list.erase(my_list.begin() + 1);        // 移除索引 1
for (double x : my_list) cout << x << " ";
cout << endl;""",
"1024 3 1 6.5 0 \\n1024 3 4.5 1 6.5 0 \\n1024 4.5 1 6.5 ")}
{card("講義 01 · vector 配 <algorithm>：sort、reverse、count、find", """using namespace std;
vector<double> my_list = {1024, 4.5, 6.5, 1};

sort(my_list.begin(), my_list.end());
for (double x : my_list) cout << x << " ";
cout << endl;

reverse(my_list.begin(), my_list.end());
for (double x : my_list) cout << x << " ";
cout << endl;

cout << count(my_list.begin(), my_list.end(), 6.5) << endl;

my_list.erase(find(my_list.begin(), my_list.end(), 6.5));  // 按值移除
for (double x : my_list) cout << x << " ";
cout << endl;""",
"1 4.5 6.5 1024 \\n1024 6.5 4.5 1 \\n1\\n1024 4.5 1 ",
note="C++ 把「容器」和「演算法」拆開：sort、reverse、count、find 都吃一對疊代器 (begin, end)，所以同一套演算法能用在不同容器上。")}
{card("講義 01 · string 的常用操作", """using namespace std;
string my_name = "David";
char initial = 'D';    // 單引號：單一字元

cout << my_name << endl;
cout << my_name[3] << endl;
cout << my_name + my_name << endl;   // 串接
cout << my_name.length() << endl;
cout << my_name.substr(2, 3) << endl; // 從索引 2 取 3 個字元
cout << my_name.find("v") << endl;

my_name.append(" Ranum");
cout << my_name << endl;""",
"David\\ni\\nDavidDavid\\n5\\nvid\\n2\\nDavid Ranum")}
{card("講義 01 · 可變性與原生陣列的危險", """using namespace std;
vector<int> my_list = {1, 3, 6};
my_list[0] = 1024;               // 合法：vector 元素可變
for (int x : my_list) cout << x << " ";
cout << endl;

string my_name = "David";
my_name[0] = 'X';                // string 的字元也可以直接改
cout << my_name << endl;

int my_arr[] = {2, 1, 4};       // 原生陣列：大小永遠固定 3
my_arr[1] = 99;
cout << my_arr[1] << endl;
cout << my_arr[3] << endl;       // 危險！沒有界限檢查，讀到垃圾值""",
"1024 3 6 \\nXavid\\n99\\n32764   ← 未定義行為：每次執行都可能不同",
note="最後一行是<strong>未定義行為</strong>（undefined behavior）：編譯過、跑得動、答案是垃圾。原生陣列不做界限檢查，這就是課程偏好 vector（配 .at()）的原因。")}
{card("講義 01 · set：去重、查成員、集合運算", """#include <iostream>
#include <set>
#include <algorithm>
#include <iterator>
using namespace std;

int main() {
    set<int> my_set = {3, 6, 4, 6, 3};   // 重複的直接被丟掉
    for (int x : my_set) cout << x << " ";
    cout << endl;
    cout << my_set.count(3) << endl;     // 1 = 在裡面
    cout << my_set.count(99) << endl;    // 0 = 不在

    my_set.insert(99);
    my_set.erase(4);
    for (int x : my_set) cout << x << " ";
    cout << endl;

    set<int> your_set = {99, 3, 100};
    set<int> result;
    set_intersection(my_set.begin(), my_set.end(),
                     your_set.begin(), your_set.end(),
                     inserter(result, result.begin()));
    for (int x : result) cout << x << " ";  // 交集
    cout << endl;
    return 0;
}""",
"3 4 6 \\n1\\n0\\n3 6 99 \\n3 99 ",
note="set 自動排序又自動去重；交集、聯集（set_union）、子集判斷（includes）都在 &lt;algorithm&gt; 裡，一樣吃疊代器範圍。")}
{card("講義 01 · map：鍵值對、走訪、安全查詢", """#include <iostream>
#include <map>
using namespace std;

int main() {
    map<string, int> phone_ext = {{"david", 1410}, {"brad", 1137}, {"roman", 1171}};

    phone_ext["kent"] = 2001;               // 加新配對
    for (auto& p : phone_ext) cout << p.first << " ";   // 鍵（自動按序）
    cout << endl;
    for (auto& p : phone_ext) cout << p.second << " ";  // 值
    cout << endl;

    cout << phone_ext.count("alice") << endl;           // 0：不存在
    if (phone_ext.find("alice") == phone_ext.end()) {
        cout << "NO ENTRY" << endl;   // 查無此鍵時給預設行為
    }
    return 0;
}""",
"brad david kent roman \\n1137 1410 2001 1171 \\n0\\nNO ENTRY",
note="小心 map 的 []：查一個<strong>不存在的鍵</strong>會默默把它插進去（值為 0）。純查詢用 .count() 或 .find()，別用 []。")}'''
s, ch3 = insert_end_of_section(s, "collections", coll_html, 'id="dx-coll"')

# ---------- P04 io ----------
io_html = f'''<h3 id="dx-io">講義完整範例：輸入與格式化輸出</h3>
{card("講義 01 · cin：型別決定轉換", """using namespace std;
double radius;
cout << "Please enter the radius of the circle ";
cin >> radius;

double diameter = 2 * radius;
cout << diameter << endl;""",
"Please enter the radius of the circle 4.5\\n9", out_label="示範執行（輸入 4.5）")}
{card("講義 01 · 完整的格式化組合技", """using namespace std;
int price = 24;
string item = "banana";

cout << "The " << setw(10) << item << " costs "
     << setw(10) << fixed << setprecision(2) << double(price) << " cents" << endl;
cout << "The " << left << setw(10) << item << " costs "
     << setw(10) << double(price) << " cents" << right << endl;
cout << "The " << setw(10) << item << " costs "
     << setfill('0') << setw(10) << double(price) << " cents" << setfill(' ') << endl;

cout << "Item:" << setfill('.') << setw(10) << item << endl;
cout << "Price:" << setfill('.') << setw(4) << "$"
     << setfill(' ') << setw(5) << double(price) << endl;""",
"The     banana costs      24.00 cents\\nThe banana     costs 24.00      cents\\nThe     banana costs 0000024.00 cents\\nItem:....banana\\nPrice:...$24.00",
note="setw 只影響下一個值；fixed、setprecision、left、setfill 則持續有效，直到你改掉它。左邊第三行的 0000024.00 就是 setfill('0') 的效果。")}
{card("講義 01 · printf 也還在", """using namespace std;
int price = 24;
string item = "banana";
printf("The %s costs %d cents\\n", item.c_str(), price);
printf("The %10s costs %5.2f cents\\n", item.c_str(), double(price));""",
"The banana costs 24 cents\\nThe     banana costs 24.00 cents",
note="C 家族的 printf 在 C++ 一樣能用：%10s 是寬度 10 的字串、%5.2f 是寬度 5、小數 2 位。注意 string 要先 .c_str() 轉成 C 字串。")}'''
s, ch4 = insert_end_of_section(s, "io", io_html, 'id="dx-io"')

# ---------- P05 control ----------
ctrl_html = f'''<h3 id="dx-ctrl">講義完整範例：巢狀迴圈與一個練習</h3>
{card("講義 01 · 巢狀 range-based for：攤平字母", """using namespace std;
vector<string> word_list = {"cat", "dog", "rabbit"};
vector<char> letter_list;
for (string a_word : word_list) {
    for (char a_letter : a_word) {
        letter_list.push_back(a_letter);
    }
}
for (char c : letter_list) cout << c << " ";
cout << endl;""",
"c a t d o g r a b b i t ",
note="外層走訪每個單字、內層走訪單字裡的每個字母。這種「攤平」寫法之後在建圖（word ladder buckets）會再出現。")}
{card("講義 01 · 練習：把 average() 寫完", """#include <iostream>
#include <vector>
#include <iomanip>
using namespace std;

void average(vector<int> a_list) {
    if (a_list.empty()) { cout << "Vector is empty" << endl; return; }
    // 你的程式碼：算出 avg，及格與否放進 status（"pass"/"fail"），然後：
    // cout << status << " (Average: " << fixed << setprecision(1) << avg << ")" << endl;
}

int main() {
    average({99, 100, 74, 63, 100, 100});
    average({22, 19, 74, 63, 100, 44});
    return 0;
}""",
"pass (Average: 89.3)\\nfail (Average: 53.7)", out_label="完成後的預期輸出",
note="提示：總和用 int 累加，平均前記得轉 double，不然 536/6 會整數除法變 89。這正是本頁 P01 的陷阱重出江湖。")}'''
s, ch5 = insert_end_of_section(s, "control", ctrl_html, 'id="dx-ctrl"')

# ---------- P06 exceptions ----------
exc_html = f'''<h3 id="dx-exc">講義補充：沒接住會怎樣？</h3>
{card("講義 01 · 沒有 try/catch 的下場", """using namespace std;
vector<int> v = {1, 2, 3};

// 索引 10 不存在：.at() 丟出 out_of_range 例外，
// 沒被接住的例外會讓程式當場終止
cout << v.at(10) << endl;""",
"terminate called after throwing an instance of 'std::out_of_range'\\n  what():  vector::_M_range_check: __n (which is 10) >= this->size() (which is 3)",
out_label="執行期錯誤訊息",
note="對照上面接住的版本：同一行程式，有 try/catch 就能優雅收場，沒有就整支程式陣亡。另外注意 v[10]（不用 .at()）連例外都不丟，直接未定義行為。")}'''
s, ch6 = insert_end_of_section(s, "exceptions", exc_html, 'id="dx-exc"')

# ---------- P07 functions ----------
fn_html = f'''{card("講義 01 · 函式可以疊著呼叫", """#include <iostream>
using namespace std;

int square(int n) {
    return n * n;
}

int main() {
    cout << square(3) << endl;
    cout << square(square(3)) << endl;   // 先算內層 9，再平方
    return 0;
}""",
"9\\n81",
note='<span id="dx-fn"></span>square(square(3)) 由內往外算：內層回傳 9，外層拿 9 再平方。這種「函式結果餵給函式」的組合思維是遞迴章的前菜。')}'''
s, ch7 = insert_end_of_section(s, "functions", fn_html, 'id="dx-fn"')

# ---------- P08 classes ----------
cls_html = f'''<h3 id="dx-cls">收工驗收：完整 Fraction 的使用畫面</h3>
{card("講義 01 · 五步蓋完之後（dscpp/fraction.hpp）", """#include <iostream>
#include "fraction.hpp"   // 本節蓋好的完整類別
using namespace std;

int main() {
    Fraction x(1, 2);
    Fraction y(2, 3);
    cout << y << endl;
    cout << x + y << endl;               // operator+：通分後約分
    cout << boolalpha << (x == y) << endl;

    Fraction z(2, 4);
    cout << (x == z) << endl;   // 深相等：1/2 == 2/4
    return 0;
}""",
"2/3\\n7/6\\nfalse\\ntrue",
note="最後一行是<strong>深相等</strong>的驗收：x 和 z 是兩個不同的物件，但 operator== 用交叉相乘比「值」，所以 1/2 == 2/4 是 true。如果比的是「是不是同一個物件」（位址），那叫淺相等。")}
{card("講義 01 · 課後練習：負分母與大小比較", """class Fraction {
    // 你的程式碼：
    //  - 建構子把負分母正規化（-9/-10 → 9/10、9/-10 → -9/10）
    //  - bool operator>(Fraction& other)
    //  - bool operator<(Fraction& other)
};

int main() {
    Fraction a(3, 5);
    Fraction b(9, -10);
    cout << boolalpha << (a > b) << endl;
    return 0;
}""",
"true", out_label="完成後的預期輸出",
note="提示：比大小跟 operator== 一樣用交叉相乘就好，不用真的除；但要先把「負號都搬到分子」，交叉相乘的不等號方向才不會被負分母翻轉。")}'''
s, ch8 = insert_end_of_section(s, "classes", cls_html, 'id="dx-cls"')

# ---------- P09 inherit ----------
inh_html = f'''<h3 id="dx-inh">講義完整範例：整座電路的程式版</h3>
{card("講義 01 · 用類別把電路接起來（dscpp/gates.hpp）", """#include <iostream>
#include "gates.hpp"   // 本節的完整閘類別階層
using namespace std;

int main() {
    AndGate g1("gand1");
    AndGate g2("gand2");
    OrGate  g3("gor3");
    NotGate g4("gnot4");
    Connector c1(&g1, &g3);   // g1 輸出 → g3 輸入
    Connector c2(&g2, &g3);
    Connector c3(&g3, &g4);
    cout << g4.getOutput() << endl;
    return 0;
}""",
"Enter input for gate gand1 (0/1): 1\\nEnter input for gate gand1 (0/1): 1\\nEnter input for gate gand2 (0/1): 0\\nEnter input for gate gand2 (0/1): 0\\n0", out_label="示範執行（A=B=1、C=D=0）",
note="呼叫 g4.getOutput() 會沿著 Connector 一路「往上游要值」：NOT 問 OR、OR 問兩個 AND、AND 才向使用者要輸入。所以 NOT((1 AND 1) OR (0 AND 0)) = NOT(1) = 0。拿上面的互動電路對照：同樣輸入應該得到同樣的 0。")}'''
s, ch9 = insert_end_of_section(s, "inherit", inh_html, 'id="dx-inh"')

PAGE.write_text(s)
print("inserted:", [n for n, ok in zip("types ptr coll io ctrl exc fn cls inh".split(),
      [ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8, ch9]) if ok])
