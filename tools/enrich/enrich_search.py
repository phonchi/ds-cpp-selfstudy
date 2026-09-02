#!/usr/bin/env python3
"""searching_sorting.html 完整自學充實：真 C++ 實作（取自 pythonds3/cppds/sorting.hpp 等）＋模擬計算的真實輸出。冪等。"""
import sys, re, io
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib import card, ensure_style, insert_end_of_section

PAGE = Path.home() / "ds-cpp-selfstudy/searching_sorting.html"
HPP = Path.home() / "ds_cpp/Slides/pythonds3/cppds/sorting.hpp"
hpp = HPP.read_text()

def func_src(name):
    m = re.search(rf'^(?:void|int|bool) {name}\(.*?\n\}}', hpp, re.S | re.M)
    return m.group(0)

# ---------- Python 模擬（照 C++ 逐行翻，收集 print 輸出）----------
out = None
def printl(a): out.append(" ".join(map(str, a)) + " ")

def bubble(a):
    for i in range(len(a)-1, 0, -1):
        printl(a)
        for j in range(i):
            if a[j] > a[j+1]: a[j], a[j+1] = a[j+1], a[j]

def selection(a):
    n = len(a)
    for i in range(n-1):
        printl(a)
        mi = i
        for j in range(i+1, n):
            if a[j] < a[mi]: mi = j
        if mi != i: a[i], a[mi] = a[mi], a[i]

def insertion(a):
    for i in range(1, len(a)):
        printl(a)
        cv, cp = a[i], i
        while cp > 0 and a[cp-1] > cv:
            a[cp] = a[cp-1]; cp -= 1
        a[cp] = cv

def gapins(a, start, gap):
    for i in range(start+gap, len(a), gap):
        cv, cp = a[i], i
        while cp >= gap and a[cp-gap] > cv:
            a[cp] = a[cp-gap]; cp -= gap
        a[cp] = cv

def shell(a):
    sc = len(a)//2
    while sc > 0:
        for ps in range(sc): gapins(a, ps, sc)
        out.append(f"After increments of size {sc} the list is " + " ".join(map(str,a)) + " ")
        sc //= 2

def merge(a):
    out.append("Splitting " + " ".join(map(str,a)) + " ")
    if len(a) > 1:
        mid = len(a)//2
        L, R = a[:mid], a[mid:]
        merge(L); merge(R)
        i=j=k=0
        while i < len(L) and j < len(R):
            if L[i] <= R[j]: a[k]=L[i]; i+=1
            else: a[k]=R[j]; j+=1
            k+=1
        while i < len(L): a[k]=L[i]; i+=1; k+=1
        while j < len(R): a[k]=R[j]; j+=1; k+=1
    out.append("Merging " + " ".join(map(str,a)) + " ")

def part(a, first, last):
    pv = a[first]; lm = first+1; rm = last
    while True:
        while lm <= rm and a[lm] <= pv: lm += 1
        while lm <= rm and a[rm] >= pv: rm -= 1
        if rm < lm: break
        a[lm], a[rm] = a[rm], a[lm]
    a[first], a[rm] = a[rm], a[first]
    return rm

def quick(a, first, last):
    if first < last:
        sp = part(a, first, last)
        printl(a)
        quick(a, first, sp-1)
        quick(a, sp+1, last)

def run(fn, a, final_printl=True):
    global out
    out = []
    fn(a)
    if final_printl: printl(a)
    return "\n".join(out)

o_bub = run(bubble, [4, 14, 5, 21, 29, 12, 16])
o_sel = run(selection, [11, 7, 12, 14, 19, 1, 6, 18, 8, 20])
o_ins = run(insertion, [9, 2, 5, 5, 7, 9, 1])
o_shl = run(shell, [54, 26, 93, 17, 77, 31, 44, 55, 20])
o_mrg = run(merge, [54, 26, 93, 17], final_printl=False)
o_qck = run(lambda a: quick(a, 0, len(a)-1), [54, 26, 93, 17, 77, 31, 44, 55, 20])

s = PAGE.read_text()
s = ensure_style(s)

USAGE = """#include <iostream>
#include "sorting.hpp"
using namespace std;

int main() {
    vector<int> aList = %s;
    %s(aList);%s
    printl(aList);
    return 0;
}"""

def sort_block(sec, marker, fname, init, output, note, extra_src="", comment=""):
    src = (extra_src + "\n\n" if extra_src else "") + func_src(fname)
    usage = USAGE % (init, fname, "   // " + comment if comment else "")
    html = (f'<h3 id="{marker}">講義完整實作與逐 pass 輸出</h3>\n'
            + card(f"講義 07 · {fname} 的 C++ 全文（pythonds3/cppds/sorting.hpp）", src, None)
            + "\n" + card("使用畫面", usage, output, out_label="輸出（每個 pass 一行）", note=note))
    return insert_end_of_section(s, sec, html, marker)

s, c1 = sort_block("bubble", "dx-bub", "bubbleSort", "{4, 14, 5, 21, 29, 12, 16}", o_bub,
    "每一行是「該 pass 開始前」的內容：最大的值一輪一輪往右浮。最後一行是排序完成的結果。另有 bubbleSortShort：某一輪完全沒交換就提前收工。",
    comment="每個 pass 開頭印出目前狀態")
s, c2 = sort_block("selection", "dx-sel", "selectionSort", "{11, 7, 12, 14, 19, 1, 6, 18, 8, 20}", o_sel,
    "跟氣泡排序同樣 O(n²) 次比較，但每輪只交換一次：觀察每行開頭，已排序的前綴一格一格長大。")
s, c3 = sort_block("insertion", "dx-ins", "insertionSort", "{9, 2, 5, 5, 7, 9, 1}", o_ins,
    "curVal 抽出來、比它大的往右挪、找到洞再放回去：注意這裡是「挪動」不是「交換」，一次挪動只要一個指定，比一次交換便宜三倍。重複值 5、9 的相對順序不變：插入排序是穩定排序。")
s, c4 = sort_block("shell", "dx-shl", "shellSort", "{54, 26, 93, 17, 77, 31, 44, 55, 20}", o_shl,
    "gap 從 n/2 一路砍半到 1。gap=1 那一輪就是普通的插入排序，但這時序列已經「幾乎有序」，所以很便宜。", extra_src=func_src("gapInsertionSort"))
s, c5 = sort_block("merge", "dx-mrg", "mergeSort", "{54, 26, 93, 17}", o_mrg,
    "Splitting 一路劈到單元素（基底情況），Merging 從最小的開始兩兩合併回來。最後一行 Merging 就是排序結果。注意它需要 O(n) 的額外空間放 leftHalf/rightHalf。")
if True:
    src_q = func_src("partition") + "\n\n" + func_src("quickSortHelper") + "\n\n" + func_src("quickSort")
    usage_q = USAGE % ("{54, 26, 93, 17, 77, 31, 44, 55, 20}", "quickSort", "   // 每次 partition 後印出")
    html_q = ('<h3 id="dx-qck">講義完整實作與逐 partition 輸出</h3>\n'
              + card("講義 07 · partition + quickSort 的 C++ 全文", src_q, None,
                     note="partition 用左右兩根 mark 相向而行：左邊找「比 pivot 大的」、右邊找「比 pivot 小的」，交換，直到交錯；最後把 pivot 換到 rightMark 的位置，這格從此不再動。")
              + "\n" + card("使用畫面", usage_q, o_qck, out_label="輸出（每次 partition 一行）",
                     note="第一行：pivot 54 落到正確位置（左邊全 ≤ 54、右邊全 ≥ 54）。之後的行輪流處理左右子區段，每行都多一個「就定位」的 pivot。"))
    s, c6 = insert_end_of_section(s, "quick", html_q, "dx-qck")

# hashing 區：雜湊函數對照表＋線性探查快照＋HashTable 使用畫面
hash_html = f'''<h3 id="dx-hash">講義完整範例：從雜湊函數到 Map 的使用畫面</h3>
{card("講義 07 · 兩種雜湊函數對照", """#include <iostream>
#include <string>
using namespace std;

int remainderMethod(int item, int divisor) {{ return item % divisor; }}
int midsquareMethod(int item, int divisor) {{
    string squared = to_string(item * item);
    if (squared.length() % 2 != 0) squared = "0" + squared;
    int mid = squared.length() / 2;
    return stoi(squared.substr(mid - 1, 2)) % divisor;
}}

int main() {{
    printf("%6s %10s %11s\\n", "Item", "Remainder", "Mid-Square");
    for (int item : {{54, 26, 93, 17}})
        printf("%6d %10d %11d\\n", item,
               remainderMethod(item, 11), midsquareMethod(item, 11));
    return 0;
}}""".replace("{{","{").replace("}}","}"),
"  Item  Remainder  Mid-Square\\n    54         10           3\\n    26          4           1\\n    93          5           9\\n    17          6           6",
note="平方取中：54² = 2916，取中間兩位 91，再 91 % 11 = 3。同一批鍵、兩種函數，落點完全不同：雜湊函數的選擇直接決定碰撞多寡。")}
{card("講義 07 · 線性探查的最終快照", """#include <iostream>
#include <vector>
using namespace std;

int main() {{
    vector<int> items = {{54, 26, 93, 17, 77, 31, 44, 55, 20}};
    vector<int> hashTable(11, -1);            // -1 代表空槽
    for (int item : items) {{
        int hashIndex = item % 11;
        while (hashTable[hashIndex] != -1)    // 碰撞就往下找（線性探查）
            hashIndex = (hashIndex + 1) % 11;
        hashTable[hashIndex] = item;
    }}
    for (int idx = 0; idx < 11; idx++)
        cout << idx << ":" << hashTable[idx] << "  ";   // 槽位:元素
    cout << endl;
    return 0;
}}""".replace("{{","{").replace("}}","}"),
"0:77  1:44  2:55  3:20  4:26  5:93  6:17  7:-1  8:-1  9:31  10:54  ",
note="值得手算一次：44 想進 0（44 % 11 = 0）但 77 已入住，探查到 1；55 探查到 2；20 想進 9，被 31、10 的 54、0、1、2 一路擋，最後落腳 3。這串「探查鏈」就是群聚（clustering）的長相。")}
{card("講義 07 · HashTable 類別的 put / get 使用畫面", """#include <iostream>
#include "hashtable.hpp"
using namespace std;

int main() {{
    HashTable h(11);
    int keys[] = {{54, 26, 93, 17, 77, 31, 44, 55, 20}};
    string vals[] = {{"cat", "dog", "lion", "tiger", "bird",
                     "cow", "goat", "pig", "chicken"}};
    for (int i = 0; i < 9; i++) h.put(keys[i], vals[i]);

    h.printSlots();
    h.printData();

    cout << h.get(20) << " " << h.get(17) << endl;
    h.put(20, "duck");                            // 同鍵：換值
    cout << h.get(20) << endl;
    cout << "[" << h.get(99) << "]" << endl;      // 不在表裡：空字串
    return 0;
}}""".replace("{{","{").replace("}}","}"),
"77 44 55 20 26 93 17 -1 -1 31 54 \\nbird goat pig chicken dog lion tiger - - cow cat \\nchicken tiger\\nduck\\n[]",
note="slots 的排列跟上一張卡完全一致：類別只是把「鍵探查」和「值跟著住進同一格」包起來。put 遇到同鍵是<strong>更新</strong>不是再探查，get 沿著同一條探查鏈找、繞回起點就放棄。")}'''
s, c7 = insert_end_of_section(s, "hashing", hash_html, 'id="dx-hash"')

# prologue（搜尋）：sequential/binary 完整程式
srch_html = f'''<h3 id="dx-srch">講義完整實作：三種搜尋的 C++ 全文</h3>
{card("講義 07 · sequentialSearch", """#include <iostream>
#include <vector>
using namespace std;

bool sequentialSearch(vector<int> aList, int item) {{
    unsigned pos = 0;
    while (pos < aList.size()) {{
        if (aList[pos] == item) {{
            return true;
        }}
        pos = pos + 1;
    }}
    return false;
}}

int main() {{
    vector<int> testList = {{54, 26, 93, 17, 77, 31, 44, 55, 20, 65}};
    cout << boolalpha;
    cout << sequentialSearch(testList, 44) << endl;
    cout << sequentialSearch(testList, 50) << endl;
    return 0;
}}""".replace("{{","{").replace("}}","}"),
"true\\nfalse")}
{card("講義 07 · binarySearch：迴圈版與遞迴版", """bool binarySearch(vector<int> aList, int item) {{
    int first = 0;
    int last = aList.size() - 1;
    while (first <= last) {{
        int midpoint = (first + last) / 2;
        if (aList[midpoint] == item) return true;
        else if (item < aList[midpoint]) last = midpoint - 1;
        else first = midpoint + 1;
    }}
    return false;
}}

bool binarySearchRec(vector<int> aList, int item) {{
    if (aList.size() == 0) return false;
    int midpoint = (aList.size() - 1) / 2;
    if (aList[midpoint] == item) return true;
    if (item < aList[midpoint]) {{
        vector<int> left(aList.begin(), aList.begin() + midpoint);
        return binarySearchRec(left, item);
    }}
    vector<int> right(aList.begin() + midpoint + 1, aList.end());
    return binarySearchRec(right, item);
}}""".replace("{{","{").replace("}}","}"),
"true\\nfalse", out_label="對 {17,20,26,31,44,54,55,65,77,93} 查 44、50 的輸出",
note="遞迴版每層都<strong>複製</strong>半條 vector 進 left/right：好懂，但複製本身是 O(n)，反而毀了 O(log n)。實務上用迴圈版，或改傳索引範圍（first, last）而不是切片。自我檢測區 Q1 的「中點取 (長度-1)/2」講的就是遞迴版。")}'''
s, c8 = insert_end_of_section(s, "prologue", srch_html, 'id="dx-srch"')

PAGE.write_text(s)
print("inserted:", [n for n,ok in zip("bub sel ins shl mrg qck hash srch".split(),[c1,c2,c3,c4,c5,c6,c7,c8]) if ok])
