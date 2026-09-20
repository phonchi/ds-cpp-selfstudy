#!/usr/bin/env python3
"""analysis.html 完整自學充實。

與其他八章不同，這支是「可重跑」的：卡片區塊包在 <!-- gen:name --> … <!-- /gen:name -->
之間，重跑只替換註解之間的內容，手寫的章節、內文與 quiz 不受影響。
首次注入的位置由 analysis.html 裡的 <!-- slot:name --> 標記決定。
想把某個區塊搬到別的位置：光移動 <!-- slot:name --> 沒有用（區塊已存在就就地替換），
要先把頁面裡那對 <!-- gen:name --> … <!-- /gen:name --> 整段刪掉，再重跑。

範例輸出一律用 run_cpp() 實際編譯執行取得（需要 ~/ds_cpp/Slides/pythonds3/cppds）；
量時間的 benchmark 使用講義輸出或具備原始數據的實測結果，不捏造代表值。

注意：這個檔刻意不用 f-string 包 card(...)。C++ 的大括號寫在 f-string 的
replacement field 裡時，Python 不會還原 {{ -> {，會把字面的雙大括號印到頁面上。
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib import card, ensure_style, insert_before, run_cpp

PAGE = Path(__file__).resolve().parents[2] / "analysis.html"
s = PAGE.read_text()
s = ensure_style(s)

SIZE = None   # analysis.html 的 .pseudo-code base 已是 .82rem，不再蓋 inline 字級


def live(label, code, note=None, out_label="預期輸出"):
    """實跑取得輸出的範例卡。編譯失敗會直接看出來（輸出會是 [編譯失敗]）。"""
    out = run_cpp(code)
    if out.startswith("[編譯失敗]") or "[執行結束碼" in out:
        raise SystemExit("範例無法編譯／執行：" + label + "\n" + out)
    return card(label, code, out, note=note, out_label=out_label, size=SIZE)


def fixed(label, code, output, note=None, out_label="預期輸出"):
    """輸出取自講義或實測的範例卡（量時間的 benchmark 用）。"""
    return card(label, code, output, note=note, out_label=out_label, size=SIZE)


def put(slot, name, block):
    global s
    s2, ok = insert_before(s, "<!-- slot:%s -->" % slot, block, "gen:%s" % name, name=name)
    assert ok, "slot:%s 找不到，也沒有既有的 gen:%s 區塊" % (slot, name)
    s = s2
    return name


done = []

# ═══════════════════ PROLOGUE ═══════════════════
pro = '<h3>講義完整範例：同一題的兩張臉</h3>\n'

pro += live("講義 02 · sumOfN：好讀的版本", """#include <iostream>
using namespace std;

long long sumOfN(long long n) {
    long long theSum = 0;
    for (long long i = 1; i <= n; i++) {
        theSum = theSum + i;
    }
    return theSum;
}

int main() {
    cout << sumOfN(10) << endl;
    return 0;
}""") + "\n"

pro += live("講義 02 · foo：一樣的演算法、糟糕的可讀性", """#include <iostream>
using namespace std;

long long foo(long long tom) {
    long long fred = 0;
    for (long long bill = 1; bill <= tom; bill++) {
        long long barney = bill;
        fred = fred + barney;
    }
    return fred;
}

int main() {
    cout << foo(10) << endl;
    return 0;
}""",
note="foo 和 sumOfN 做的事一模一樣、效率也一樣，差別只在看不看得懂。"
     "<strong>可讀性</strong>跟<strong>效率</strong>是兩回事，演算法分析比的是後者："
     "同一個問題，不同解法消耗的資源。") + "\n"

pro += live("講義 02 · 用 chrono 量時間", """#include <iostream>
#include <chrono>
using namespace std;
using namespace std::chrono;

long long sumOfN2(long long n, double& seconds) {
    auto start = steady_clock::now();
    long long theSum = 0;
    for (long long i = 1; i <= n; i++) theSum = theSum + i;
    seconds = duration<double>(steady_clock::now() - start).count();
    return theSum;
}

int main() {
    double secs;
    cout << sumOfN2(10, secs) << endl;   // secs 由參考參數帶回
    return 0;
}""",
note="這支程式出現的三個零件——<code>steady_clock</code>、<code>duration</code>、<code>.count()</code>"
     "——以及 <code>double&amp; seconds</code> 這個「回傳兩個值」的寫法，下面兩個收合區逐一拆開講。")
done.append(put("pro", "dx-pro", pro))

# ═══════════════════ PART 01 · 數操作 ═══════════════════
cnt = live("cppds 的數法：數賦值敘述", """#include <iostream>
using namespace std;

long long sumOfN(long long n) {
    long long theSum = 0;        // 賦值 1 次
    for (long long i = 1; i <= n; i++)
        theSum = theSum + i;     // 賦值 n 次
    return theSum;
}

int main() {
    cout << sumOfN(10) << endl;
    return 0;
}""",
note="只數<strong>賦值敘述</strong>：迴圈外 1 次、迴圈內 n 次，所以 "
     "<span class=\"mono\">T(n) = 1 + n</span>。") + "\n"

cnt += live("Hello 演算法的數法：逐行 +1", """#include <iostream>
using namespace std;

void algorithm(int n) {
    int a = 1;      // +1
    a = a + 1;      // +1
    a = a * 2;      // +1
    for (int i = 0; i < n; i++)   // +n（每輪都要做 i++ 與比較）
        cout << 0 << endl;        // +n
}

int main() {
    algorithm(3);
    return 0;
}""",
note="連宣告、迴圈控制都各算一次，得到 <span class=\"mono\">T(n) = 3 + 2n</span>。"
     "比上面的常數項與係數都大，但兩者一樣都是 <strong>O(n)</strong>。")
done.append(put("count", "dx-count", cnt))

# ═══════════════════ PART 02 · Big-O ═══════════════════
bigo = live("講義 02 · 練習題原始碼：T(n) 逐項數", """#include <iostream>
using namespace std;

int main() {
    int n = 100;
    // 從這裡開始數
    int a = 5;
    int b = 6;
    int c = 10;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            int x = i * i;
            int y = j * j;
            int z = i * j;
        }
    }
    for (int k = 0; k < n; k++) {
        int w = a * k + 45;
        int v = b * b;
    }
    int d = 33;
    cout << "done" << endl;
    return 0;
}""",
note="照課本的數法（數賦值敘述）：開頭 3 個；雙層迴圈本體 3 個，各跑 n² 次；"
     "單層迴圈 2 個，跑 n 次；收尾 1 個。"
     "<span class=\"mono\">T(n) = 3 + 3n² + 2n + 1 = 3n² + 2n + 4</span>，"
     "只留主導項就是 <strong>O(n²)</strong>。這是講義的自我檢測題，先自己數完再看這段解說。")
done.append(put("bigo", "dx-bigo", bigo))

# ═══════════════════ PART 04 · Anagram ═══════════════════
ana12 = live("解法 1：Checking Off — O(n²)", """#include <iostream>
#include <string>
#include <vector>
using namespace std;

bool anagramSolution1(string s1, string s2) {
    bool stillOK = true;
    if (s1.length() != s2.length()) stillOK = false;
    vector<char> aList(s2.begin(), s2.end());
    unsigned pos1 = 0;
    while (pos1 < s1.length() && stillOK) {          // 外圈：n 次
        unsigned pos2 = 0;
        bool found = false;
        while (pos2 < aList.size() && !found) {      // 內圈：最多 n 次
            if (s1[pos1] == aList[pos2]) found = true;
            else pos2 = pos2 + 1;
        }
        if (found) aList.erase(aList.begin() + pos2);  // 劃掉，也是 O(n)
        else stillOK = false;
        pos1 = pos1 + 1;
    }
    return stillOK;
}

int main() {
    cout << boolalpha;
    cout << anagramSolution1("earth", "heart") << endl;
    cout << anagramSolution1("apple", "pleap") << endl;
    cout << anagramSolution1("abcd", "abce") << endl;
    return 0;
}""",
note="外圈每跑一輪，內圈最多要看過 aList 剩下的所有字元。第一輪看 n 個、第二輪 n−1 個……"
     "總比較次數是 $1+2+\\dots+n=\\frac{n(n+1)}{2}$，主導項 $n^2/2$，所以是 <strong>O(n²)</strong>。"
     "這支是課程標頭 <code>pythonds3/cppds/anagram.hpp</code> 裡的版本，劃掉的作法與課本略有不同——下面說明。") + "\n"

ana12 += live("解法 2：Sort and Compare — O(n log n)", """#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

bool anagramSolution2(string s1, string s2) {
    sort(s1.begin(), s1.end());      // O(n log n)
    sort(s2.begin(), s2.end());      // O(n log n)
    unsigned pos = 0;
    bool matches = true;
    while (pos < s1.length() && matches) {   // O(n)
        if (s1[pos] == s2[pos]) pos = pos + 1;
        else matches = false;
    }
    return matches;
}

int main() {
    cout << boolalpha;
    cout << anagramSolution2("earth", "heart") << endl;
    cout << anagramSolution2("apple", "pleap") << endl;
    cout << anagramSolution2("abcd", "abce") << endl;
    return 0;
}""",
note="函式本體只有一個迴圈，看起來像 O(n)——但 <code>sort</code> 那兩行才是最貴的。"
     "整體由最貴的步驟主導，所以是 <strong>O(n log n)</strong>。"
     "這是「一行不等於一次」最經典的例子。"
     "（照課本原版，這支假設兩個字串等長，實際使用前應先檢查長度。）")
done.append(put("ana12", "dx-ana12", ana12))

ana4 = live("解法 4：Count and Compare — O(n)", """#include <iostream>
#include <string>
using namespace std;

bool anagramSolution4(string s1, string s2) {
    int c1[26] = {0};
    int c2[26] = {0};
    // 兩個迴圈各掃一遍字串，各 n 次
    for (unsigned i = 0; i < s1.length(); i++) c1[s1[i] - 'a']++;
    for (unsigned i = 0; i < s2.length(); i++) c2[s2[i] - 'a']++;
    // 這個迴圈跑固定的 26 次，與 n 無關
    for (int i = 0; i < 26; i++) {
        if (c1[i] != c2[i]) return false;
    }
    return true;
}

int main() {
    cout << boolalpha;
    cout << anagramSolution4("earth", "heart") << endl;
    cout << anagramSolution4("apple", "pleap") << endl;
    cout << anagramSolution4("abcd", "abce") << endl;
    return 0;
}""",
note="兩個迴圈各掃一遍字串（各 n 次），最後那個迴圈跑的是<strong>固定的 26 次</strong>，與 n 無關。"
     "<span class=\"mono\">T(n) = 2n + 26</span>，也就是 <strong>O(n)</strong>——"
     "本節開頭的互動動畫逐行高亮的就是這個演算法（那裡是省略 include 與 main 的精簡版）。"
     "（<code>c1[s1[i] - 'a']</code> 假設輸入只有小寫英文字母。）")
done.append(put("ana4", "dx-ana4", ana4))

# ═══════════════════ PART 05 · vector ═══════════════════
cap = live("觀察容量怎麼長：push_back 十次", """#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v;
    cout << "第幾次\tsize\tcapacity" << endl;
    for (int i = 1; i <= 10; i++) {
        size_t before = v.capacity();
        v.push_back(i);
        cout << i << "\t" << v.size() << "\t" << v.capacity();
        if (v.capacity() != before) cout << "\t<-- 擴充並搬家";
        cout << endl;
    }
    return 0;
}""",
note="搬家只發生在 capacity 跳動的那幾次，而且愈來愈稀疏——這就是攤還 O(1) 的全部秘密。"
     "上面的輸出來自 libstdc++（倍率 2），MSVC 會看到 1.5 倍的成長。")
done.append(put("cap", "dx-cap", cap))

vec = '<h3>講義完整範例：把四種寫法真的量一次</h3>\n'
vec += fixed('講義 02 · 四種填滿 vector 的方式', r"""#include <iomanip>
#include <iostream>
#include <vector>
#include "pythonds3/cppds/dstimer.hpp"
using namespace std;

void test1(int n) { vector<int> v; for (int i = n - 1; i >= 0; i--) v.insert(v.begin(), i); }
void test2(int n) { vector<int> v; for (int i = 0; i < n; i++) v.push_back(i); }
void test3(int n) { vector<int> v; v.reserve(n);
                    for (int i = 0; i < n; i++) v.push_back(i); }
void test4(int n) { vector<int> v(n); for (int i = 0; i < n; i++) v[i] = i; }

int main() {
    void (*tests[])(int) = {test1, test2, test3, test4};
    const char* names[] = {"insert at front", "push_back", "with reserve", "direct index"};
    for (int k = 0; k < 4; k++) {
        DSTimer t;
        for (int r = 0; r < 1000; r++) tests[k](1000);
        cout << left << setw(16) << names[k] << right << setw(9)
             << fixed << setprecision(2) << t.millis()
             << " ms" << endl;
    }
}""",
'insert at front     61.33 ms\npush_back            4.83 ms\nwith reserve         3.43 ms\ndirect index         1.37 ms',
out_label='講義執行範例',
note='前端插入每次都要搬動已有元素；由 n−1 遞減插入，最後得到 0 到 n−1，與其他三種寫法相同。這組數字沿用講義的執行結果，實際耗時會隨機器與編譯設定改變。') + '\n'
vec += fixed('講義 02 · erase(begin) vs pop_back：n 變大會怎樣', r"""#include <iomanip>
#include <iostream>
#include <vector>
#include "pythonds3/cppds/dstimer.hpp"
using namespace std;

int main() {
    cout << left << setw(10) << "n" << right << setw(14) << "erase(begin)"  << setw(12) << "pop_back" << endl;
    for (int n = 2'500'000; n <= 10'000'000; n += 2'500'000) {
        vector<int> x(n);
        DSTimer te;
        for (int r = 0; r < 100; r++) x.erase(x.begin());
        double eraseT = te.millis();
        vector<int> y(n);
        DSTimer tp;
        for (int r = 0; r < 100; r++) y.pop_back();
        cout << left << setw(10) << n << right << fixed << setprecision(5)
             << setw(14) << eraseT << setw(12) << tp.millis() << endl;
    }
}""",
'n           erase(begin)    pop_back\n2500000         20.52029     0.00028\n5000000         48.93541     0.00032\n7500000        104.64115     0.00030\n10000000       188.86044     0.00022',
out_label='本機實測：7 次中位數，單位 ms（GCC -O0）',
note='前端刪除要搬移後續元素，單次 O(n)；尾端刪除不必搬移，單次 O(1)。下方數字與圖片來自同一批 7 次實測的中位數，耗時也受快取與計時誤差影響，不必恰好按 n 的比例增加。')
done.append(put("vec", "dx-vec", vec))

# ═══════════════════ PART 06 · string ═══════════════════
strings = live("講義 02 · std::string 的成本實驗", """#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "data";
    s.push_back('!');          // 尾端加入：攤還 O(1)
    s.insert(0, "C++ ");       // 前端插入：要搬後方字元，O(n)
    cout << s << " | size=" << s.size() << endl;
    return 0;
}""",
note="C++11 起 <code>string</code> 的字元連續儲存，成本模型幾乎跟 <code>vector</code> 一樣："
     "索引與 <code>size()</code> 是 O(1)，<code>push_back</code> 是攤還 O(1)，"
     "在前端 <code>insert</code> 要搬移後方字元，最差 O(n)。"
     "順帶一提，一般的子字串搜尋不會因為連續儲存就變成 O(log n)，"
     "成本取決於搜尋演算法與兩個字串的長度。")
done.append(put("string", "dx-string", strings))

# ═══════════════════ PART 07 · unordered_map ═══════════════════
hsh = '<h3>講義完整範例：兩種 find 的查找成本</h3>\n'
hsh += fixed('講義 02 · std::find vs unordered_map::find', r"""#include <iostream>
#include <iomanip>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <unordered_map>
#include "pythonds3/cppds/dstimer.hpp"
using namespace std;
int main() {
    cout << setw(10) << "n" << setw(12) << "vector" << setw(12) << "hash" << endl;
    for (int n : {100'000, 200'000, 400'000, 800'000}) {
        vector<int> v(n);
        unordered_map<int, int> m;
        for (int i = 0; i < n; i++) { v[i] = i; m[i] = 0; }
        int target = rand() % (2 * n), hits = 0;

        DSTimer t1;
        for (int r = 0; r < 100; r++)
            hits += (find(v.begin(), v.end(), target) != v.end());
        double tv = t1.millis();
        DSTimer t2;
        for (int r = 0; r < 100; r++)
            hits += (m.find(target) != m.end());
        cout << setw(10) << n << fixed << setprecision(3)
             << setw(12) << tv << setw(12) << t2.millis() << endl;}
}""",
'         n      vector        hash\n    100000      25.908       0.004\n    200000      37.796       0.004\n    400000      26.646       0.004\n    800000     232.638       0.003',
out_label='本機實測：7 次中位數，單位 ms（GCC -O0）',
note='每個 n 先用 <code>rand() % (2 * n)</code> 選一個目標，兩個容器都重複查它 100 次。<code>std::find</code> 逐一比對；<code>m.find(target)</code> 利用雜湊找 key，最後都用 <code>!= end()</code> 判斷是否找到。目標可能不存在，命中位置也會不同，所以 n 加倍時耗時不一定加倍。雜湊查詢平均 O(1)、最差 O(n)。這裡的數字是下圖 7 次量測的中位數，不是固定答案。')
done.append(put("hash", "dx-hash", hsh))

# ═══════════════════ 實測圖（本機量測，2026-09-20；保留既有 figure id）═══════════════════
if 'id="benchmark-pop-20260906"' not in s:
    i = s.index('</section>', s.index('<section id="vectors">'))
    s = s[:i] + '\n<figure id="benchmark-pop-20260906" style="max-width:900px;margin:1.5rem auto;">\n  <div class="benchmark-chart" style=""><img src="assets/figures/pop_benchmark.png" alt="vector 前端刪除與尾端刪除的耗時比較；每組 100 次操作，7 次實測中位數，縱軸為毫秒的對數刻度" width="1800" height="1159" loading="lazy" style="display:block;width:100%;max-width:100%;height:auto;background:#fff;"></div>\n  <figcaption style="font-size:.9rem;line-height:1.7;margin-top:.6rem;">比較 vector 前端刪除與尾端刪除，每組各做 100 次；點為 7 次實測中位數，誤差棒為最小值到最大值。前端刪除需要搬移後續元素，尾端刪除則不需要。</figcaption>\n</figure>\n' + s[i:]
if 'id="benchmark-lookup-20260906"' not in s:
    i = s.index('</section>', s.index('<section id="hash">'))
    s = s[:i] + '\n<figure id="benchmark-lookup-20260906" style="max-width:900px;margin:1.5rem auto;">\n  <div class="benchmark-chart" style=""><img src="assets/figures/dict_benchmark.png" alt="std::find 與 unordered_map::find 的耗時比較；10、20、40、80 萬元素，每組同一目標查 100 次，包含命中與未命中，縱軸為毫秒的對數刻度" width="1800" height="1159" loading="lazy" style="display:block;width:100%;max-width:100%;height:auto;background:#fff;"></div>\n  <figcaption style="font-size:.9rem;line-height:1.7;margin-top:.6rem;">與新版講義相同：10、20、40、80 萬元素，各用同一目標查 100 次。點為 7 次實測中位數，誤差棒為最小值到最大值。本機前三組命中、最後一組未命中；隨機目標與耗時可能因平台不同而改變。</figcaption>\n</figure>\n' + s[i:]

s = s.replace('src="imgs/pop_benchmark.png"', 'src="assets/figures/pop_benchmark.png"')
s = s.replace('src="imgs/dict_benchmark.png"', 'src="assets/figures/dict_benchmark.png"')

if 'id="analysis-mobile-navigation"' not in s:
    s = s.replace('</head>', '<style id="analysis-mobile-navigation">\n@media (max-width: 768px) { .float-nav { display: none; } }\n</style>\n</head>', 1)

PAGE.write_text(s)
print("寫入完成，區塊：", " ".join(done))
