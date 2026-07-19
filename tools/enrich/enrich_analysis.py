#!/usr/bin/env python3
"""analysis.html 完整自學充實。冪等。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib import card, ensure_style, insert_end_of_section

PAGE = Path.home() / "ds-cpp-selfstudy/analysis.html"
s = PAGE.read_text()
s = ensure_style(s)

pro = f'''<h3 id="dx-pro">講義完整範例：同一題的兩張臉</h3>
{card("講義 02 · sumOfN：好讀的版本", """#include <iostream>
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
}""",
"55")}
{card("講義 02 · foo：一樣的演算法、糟糕的可讀性", """long long foo(long long tom) {
    long long fred = 0;
    for (long long bill = 1; bill <= tom; bill++) {
        long long barney = bill;
        fred = fred + barney;
    }
    return fred;
}""",
"55", out_label="foo(10) 的輸出",
note="foo 和 sumOfN 做的事一模一樣、效率也一樣：<strong>可讀性</strong>跟<strong>效率</strong>是兩回事。演算法分析比的是後者：同一個問題，不同「解法」消耗的資源。")}
{card("講義 02 · 用 chrono 量時間", """#include <iostream>
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
"55",
note="steady_clock 是單調時鐘，適合量耗時（system_clock 會被校時影響）。量出來的秒數用<strong>傳參考</strong>的 seconds 帶回：一個函式想「回傳兩個值」時的慣用手法。")}'''
s, c1 = insert_end_of_section(s, "prologue", pro, 'id="dx-pro"')

bigo = f'''{card("講義 02 · 練習題原始碼：T(n) 逐項數", """int n = 100;
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
int d = 33;""",
None,
note='<span id="dx-bigo"></span>逐項數：開頭 3 個指定；雙層迴圈本體 3 個指定，各跑 n² 次；單層迴圈 2 個指定，跑 n 次；收尾 1 個。T(n) = 3 + 3n² + 2n + 1，只留主導項就是 <strong>O(n²)</strong>。這題是講義的自我檢測題，先自己數完再看這段解說。')}'''
s, c2 = insert_end_of_section(s, "bigo", bigo, 'id="dx-bigo"')

vec = f'''<h3 id="dx-vec">講義完整範例：把四種寫法真的量一次</h3>
{card("講義 02 · 四種填滿 vector 的方式", """#include <iostream>
#include <vector>
#include "dstimer.hpp"
using namespace std;

void test1(int n) { vector<int> v; for (int i = 0; i < n; i++) v.insert(v.begin(), i); }
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
        printf("%-16s%9.2f ms\\n", names[k], t.millis());
    }
}""",
"insert at front   285.31 ms\\npush_back            6.42 ms\\nwith reserve         3.85 ms\\ndirect index         2.10 ms", out_label="示範執行（數字依機器而異，看量級）",
note="前端插入每次都要搬動整段資料，所以慢兩個量級。push_back 偶爾要搬家（容量翻倍），先 reserve 就不搬了；直接索引又省掉容量檢查。")}
{card("講義 02 · erase(begin) vs pop_back：n 變大會怎樣", """#include <iostream>
#include <vector>
#include "dstimer.hpp"
using namespace std;

int main() {
    printf("%-10s%14s%12s\\n", "n", "erase(begin)", "pop_back");
    for (int n = 2500000; n <= 10000000; n += 2500000) {
        vector<int> x(n);
        DSTimer te;
        for (int r = 0; r < 100; r++) x.erase(x.begin());
        double eraseT = te.millis();
        vector<int> y(n);
        DSTimer tp;
        for (int r = 0; r < 100; r++) y.pop_back();
        printf("%-10d%14.5f%12.5f\\n", n, eraseT, tp.millis());
    }
}""",
"n           erase(begin)    pop_back\\n2500000        155.20031     0.00022\\n5000000        311.87542     0.00021\\n7500000        468.11289     0.00023\\n10000000       625.40067     0.00022", out_label="示範執行（數字依機器而異，看走勢）",
note="重點在<strong>走勢</strong>：n 翻倍，erase(begin()) 的時間跟著翻倍（O(n)）；pop_back 文風不動（O(1)）。這就是「量測驗證 Big-O」的標準做法。")}'''
s, c3 = insert_end_of_section(s, "vectors", vec, 'id="dx-vec"')

hsh = f'''<h3 id="dx-hash">講義完整範例：contains 的兩個世界</h3>
{card("講義 02 · vector 線性掃描 vs unordered_map 雜湊", """#include <unordered_map>
#include "dstimer.hpp"
using namespace std;

int main() {
    printf("%-10s%10s%12s\\n", "n", "vector", "hash table");
    for (int n : {250000, 500000, 1000000}) {
        vector<int> x(n);
        unordered_map<int, int> m;
        for (int j = 0; j < n; j++) { x[j] = j; m[j] = 0; }
        int hits = 0;
        DSTimer tv;
        for (int r = 0; r < 100; r++)
            hits += (find(x.begin(), x.end(), rand() % n) != x.end());
        double vecT = tv.millis();
        DSTimer tm;
        for (int r = 0; r < 100; r++) hits += m.count(rand() % n);
        printf("%-10d%10.3f%12.3f\\n", n, vecT, tm.millis());
    }
}""",
"n             vector  hash table\\n250000         8.512       0.011\\n500000        17.204       0.012\\n1000000       35.917       0.012", out_label="示範執行（數字依機器而異，看走勢）",
note="vector 的 find 是線性掃描：n 翻倍、時間翻倍。雜湊表的 count 平均 O(1)：n 翻四倍也不動。代價在第 5 章雜湊一節會算清楚：空間、雜湊函數品質、碰撞。")}'''
s, c4 = insert_end_of_section(s, "hash", hsh, 'id="dx-hash"')

PAGE.write_text(s)
print("inserted:", [n for n, ok in zip("pro bigo vec hash".split(), [c1, c2, c3, c4]) if ok])
