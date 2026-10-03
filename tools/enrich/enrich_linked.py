#!/usr/bin/env python3
"""linked_lists.html 完整自學充實。冪等。"""
import sys
import re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib import card, ensure_style, insert_end_of_section

PAGE = Path(__file__).resolve().parents[2] / "linked_lists.html"
s = PAGE.read_text()
s = ensure_style(s)
# Adopt the earlier insert-only tails once; subsequent runs replace named blocks.
legacy = {"node": '<div class="deck-extra">',
          "unordered": '<h3 id="dx-uno">',
          "ordered": '<div class="deck-extra">',
          "exercises": '<div class="deck-extra" id="dx-exx">'}
for sid, anchor in legacy.items():
    m = re.search(rf'<section id="{sid}">.*?</section>', s, re.S)
    part = m.group()
    if '<!-- gen:linked-' not in part and anchor in part:
        start = part.index(anchor)
        part = part[:start] + '</section>'
        s = s[:m.start()] + part + s[m.end():]


node = f'''{card("講義 04 · Node 的使用畫面", """#include <iostream>
#include "pythonds3/cppds/linked_list.hpp"   // Node / UnorderedList / OrderedList
using namespace std;

int main() {
    Node<int> *temp = new Node<int>(93);
    cout << temp->getData() << endl;
    cout << boolalpha << (temp->getNext() == nullptr) << endl;
    delete temp;
    return 0;
}""",
"93\\ntrue",
note='<span id="dx-node"></span>new 出來的節點住在 heap，用指標操作、用 -&gt; 呼叫方法。getNext() 是空指標：新節點還沒接上任何人。使用完畢後，以 delete 釋放這個節點。')}'''
s, c1 = insert_end_of_section(s, "node", node, 'id="dx-node"', name='linked-node')

uno = f'''<h3 id="dx-uno">講義完整範例：UnorderedList 全套操作</h3>
{card("講義 04 · add / size / search / remove", """#include <iostream>
#include "pythonds3/cppds/linked_list.hpp"
using namespace std;

int main() {
    UnorderedList<int> myList;
    myList.add(31); myList.add(77); myList.add(17);
    myList.add(93); myList.add(26); myList.add(54);

    cout << myList << endl;
    cout << myList.size() << endl;
    cout << boolalpha << myList.search(93) << endl;

    myList.remove(54);
    myList.remove(93);
    myList.remove(31);
    cout << myList << endl;
    return 0;
}""",
"54 26 93 17 77 31 \\n6\\ntrue\\n26 17 77 ",
note="第一行輸出可以看出 add 採用<strong>頭插</strong>：最後加入的 54 排最前面。三次 remove 分別刪除頭端、中間與尾端節點。接著逐步看指標如何更新。")}
<div class="deck-extra">
  <div class="dx-label">講義 04 · remove(26) 的指標更新步驟</div>
  <table style="width:100%;border-collapse:collapse;font-size:.88rem;">
    <tr style="border-bottom:2px solid var(--card-border);"><th style="text-align:left;padding:.4rem;">步驟</th><th style="text-align:left;">prev</th><th style="text-align:left;">cur</th><th style="text-align:left;">動作</th></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.4rem;">開始</td><td>NULL</td><td>head（54）</td><td>兩根指標起跑</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.4rem;">比對 54</td><td>54</td><td>26</td><td>不是目標：prev 跟上、cur 前進</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.4rem;">比對 26</td><td>54</td><td>26</td><td>找到了，停</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.4rem;">摘除</td><td colspan="2">prev-&gt;setNext(cur-&gt;getNext())</td><td>54 直接指向 93，26 被跳過</td></tr>
    <tr><td style="padding:.4rem;">收尾</td><td colspan="2">delete cur</td><td>歸還記憶體；若刪 head，必須先移動 head 再 delete</td></tr>
  </table>
  <p class="dx-note">刪除單向串列的非首節點時，需要更新<strong>前驅節點的 next</strong>，因此走訪時同時保存 prev 與 cur。若刪除的是 head，則直接更新 head。</p>
</div>'''
s, c2 = insert_end_of_section(s, "unordered", uno, 'id="dx-uno"', name='linked-uno')

ownership = f'''{card("講義 04 · 所有權與 deep copy", """UnorderedList<int> a;
a.add(1); a.add(2);
UnorderedList<int> b = a;  // 必須複製整條鏈
b.remove(2);               // 不可改到 a
""",
None,
note='<span id="dx-own"></span>教學類別擁有 new 出來的節點：destructor 要逐一 delete；copy constructor 與 copy assignment 要 deep copy。若只複製 head，兩個物件會共用節點，最後可能 double free。remove 採 erase-if-found，找不到時保持不變。')}'''
from content.linked_depth import fold
ownership = fold("延伸：所有權與深層複製", ownership)
s, c5 = insert_end_of_section(s, "unordered", ownership, 'id="dx-own"', name='linked-ownership')

odr = f'''{card("講義 04 · OrderedList：一樣的介面、排好的內容", """#include <iostream>
#include "pythonds3/cppds/linked_list.hpp"
using namespace std;

int main() {
    OrderedList<int> myList;
    myList.add(31);
    myList.add(77);
    myList.add(17);
    myList.add(93);
    myList.add(26);
    myList.add(54);

    cout << myList << endl;
    cout << myList.size() << endl;
    cout << boolalpha << myList.search(93) << endl;
    cout << myList.search(100) << endl;
    return 0;
}""",
"17 26 31 54 77 93 \\n6\\ntrue\\nfalse",
note='<span id="dx-odr"></span>同樣六次 add、同樣的呼叫介面，印出來卻是由小到大：差別全在 add 內部「找到正確位置再插」。search(100) 必須走到底；search(45) 則遇到 54 就能停止，因為後方只會更大。')}'''
s, c3 = insert_end_of_section(s, "ordered", odr, 'id="dx-odr"', name='linked-ordered')

exx = f'''<div class="deck-extra" id="dx-exx">
  <div class="dx-label">cppds Ch.4 課後題精選（自我挑戰）</div>
  <ol style="font-size:.92rem;line-height:1.9;padding-left:1.4rem;">
    <li><strong>size 的 O(1) 版</strong>：現在的 size() 要走訪整條串列。把「節點數」存成成員變數，改寫 add / remove / size，讓 size() 變 O(1)。</li>
    <li><strong>驗證 remove 契約</strong>：目標不在串列裡時應保持不變。替空串列、缺少目標、刪 head、刪尾端各寫一個測試。</li>
    <li><strong>補完 ADT</strong>：實作 append、index、pop、insert 四個缺席的方法，並分析各自的 Big-O。</li>
    <li><strong>slice(start, stop)</strong>：回傳從 start 到 stop（不含）的新串列。</li>
    <li><strong>用繼承減少重複</strong>：OrderedList 與 UnorderedList 大量方法相同。設計繼承階層，讓共同的部分只寫一次。</li>
    <li><strong>串列版 Stack／Queue／Deque</strong>：用鏈結串列各實作一次，跟第 3 章的 vector 版比效能。哪些操作變快、哪些變慢？</li>
  </ol>
  <p class="dx-note">完整題目在 <a href="https://runestone.academy/ns/books/published/cppds/LinearLinked/ProgrammingExercises.html" target="_blank" rel="noopener">cppds ProgrammingExercises</a>；第 1、2 題是課本的自我檢測熱身，第 5 題則練習比較兩個類別的差異。</p>
</div>'''
s, c4 = insert_end_of_section(s, "exercises", exx, 'id="dx-exx"', name='linked-exercises')

from content.linked_depth import blocks
for sid, content in blocks().items():
    s, _ = insert_end_of_section(s, sid, content, '', name='linked-depth-' + sid)
style = """<style id="linked-depth-style">
.linked-detail{margin:1rem 0;border:1px solid var(--card-border);border-radius:8px;background:var(--card);}
.linked-detail>summary{cursor:pointer;padding:.9rem 1rem;font-weight:600;line-height:1.6;}
.linked-detail-body{padding:0 1rem 1rem;min-width:0;}
.linked-detail-body .pseudo-code{max-width:100%;overflow-x:auto;}
.linked-detail-body .cmp-table{min-width:500px;}
</style>"""
if 'id="linked-depth-style"' in s:
    s = re.sub(r'<style id="linked-depth-style">.*?</style>', lambda m: style, s, flags=re.S)
else:
    s = s.replace('</head>', style + '\n</head>', 1)
# Small corrections to preserved interactive explanations.
s = s.replace('多花兩個節點的記憶體，換到少一半的 if，很划算。', '哨兵統一頭尾接線，但仍須檢查空串列，且不能刪除哨兵。')
s = s.replace('作業系統的分時排程（輪流給每個程式一點 CPU）就是這樣繞圈的。', '可用來表達輪流分配執行機會的順序。')
s = s.replace('這是能力問題：雙向的 std::list 就有真正的 insert。', '介面反映已知前驅才能常數時間接線；std::list 可由 pos 找到前驅。')
s = s.replace('不是快慢問題，是「做不做得到」的問題。', '若從頭找前驅仍能插在某節點之前，但需要 O(n)；insert_after 明確要求呼叫者提供前驅。')
s = s.replace('任意位置插入/刪除 O(1)', '單項插入／刪除 O(1)')
s = s.replace('（拿到迭代器之後）', '（list 已知位置；forward_list 已知前驅）')
s = s.replace('<tr><td>每節點額外空間</td><td>0</td><td>1 指標</td><td>2 指標</td></tr>', '<tr><td>典型儲存額外成本</td><td>預留容量與容器狀態</td><td>每節點 next 與配置成本</td><td>每節點 prev／next 與配置成本</td></tr>')
s = s.replace('兩個方向都能走；<strong>環狀串列</strong>', '兩個方向都能走；<strong>環狀串列</strong>')
# Lecture places STL before circular/doubly linked extensions; keep anchors.
mvar = re.search(r'<section id="variants">.*?</section>', s, re.S)
mstl = re.search(r'<section id="stl">.*?</section>', s, re.S)
if mvar.start() < mstl.start():
    s = s[:mvar.start()] + mstl.group() + '\n\n' + mvar.group() + s[mstl.end():]
s = s.replace('PART 05 · 工業級', 'PART 04 · STL 容器').replace('PART 04 · 變化型', 'PART 05 · 變化型')
# Match navigation order and numbering to the section order.
for cls in ('fn-num', 'toc-num'):
    pattern = rf'(<a href="#variants"[^>]*><span class="{cls}">)P04(</span>.*?</a>)(\s*)(<a href="#stl"[^>]*><span class="{cls}">)P05(</span>.*?</a>)'
    s = re.sub(pattern, lambda m: m[4] + 'P04' + m[5] + m[3] + m[1] + 'P05' + m[2], s)
s = s.replace('doubly / circular｜STL list', 'STL list｜circular / doubly')
s = s.replace('單项插入', '單項插入')
s = s.replace('<tr><td>插入（頭）</td><td>O(n)</td><td><strong>O(1)</strong></td><td>O(n)（找位置）</td></tr>', '<tr><td>add／插入新值</td><td>頭插 O(n)</td><td>頭插 O(1)</td><td>定位最壞 O(n)；插在頭端 O(1)</td></tr>')
s = s.replace('<tr><td>remove（已找到）</td><td>O(n)（搬移）</td><td>O(1)（改指標）</td><td>O(1)（改指標）</td></tr>', '<tr><td>刪除單項（已知位置）</td><td>O(n)（搬移）</td><td>O(1)（另須知道前驅；頭端例外）</td><td>O(1)（另須知道前驅；頭端例外）</td></tr>')
s = s.replace('<th>vector／陣列</th>', '<th>vector／連續陣列表示</th>')
s = s.replace('<tr><td>存取第 k 個</td><td>O(1)</td><td>O(k)</td><td>O(k)</td></tr>', '<tr><td>存取零起始第 k 項</td><td>O(1)</td><td>O(k+1)</td><td>O(k+1)</td></tr>')
s = s.replace('C++ 沒有垃圾回收！', '釋放動態配置的節點')
s = s.replace('節點脫鉤後若不 delete，這塊 heap 記憶體永遠拿不回來：C++ 沒有垃圾回收，釋放永遠要自己來。', '這份以原生指標管理節點的實作，脫鉤後若失去最後的節點指標且未 delete，就會洩漏記憶體。STL 容器則會自動管理其節點生命週期。')
# Preserve output spaces as HTML entities without source trailing whitespace.
s = re.sub(r'<pre>.*?</pre>', lambda m: re.sub(r' +(?=\n)', lambda w: '&#32;' * len(w.group()), m.group()), s, flags=re.S)
s = re.sub(r'(?m)^[ \t]+$', '', s)
from content.teaching_copy import polish_preserved
s = polish_preserved("linked_lists", s)
PAGE.write_text(s)
print("inserted:", [n for n, ok in zip("node uno ownership odr exx".split(), [c1, c2, c5, c3, c4]) if ok])
