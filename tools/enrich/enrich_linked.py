#!/usr/bin/env python3
"""linked_lists.html 完整自學充實。冪等。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib import card, ensure_style, insert_end_of_section

PAGE = Path.home() / "ds-cpp-selfstudy/linked_lists.html"
s = PAGE.read_text()
s = ensure_style(s)

node = f'''{card("講義 04 · Node 的使用畫面", """#include <iostream>
#include "linked_list.hpp"   // Node / UnorderedList / OrderedList
using namespace std;

int main() {
    Node<int> *temp = new Node<int>(93);
    cout << temp->getData() << endl;
    cout << temp->getNext() << endl;   // NULL 印出來是 0
    delete temp;
    return 0;
}""",
"93\\n0",
note='<span id="dx-node"></span>new 出來的節點住在 heap，用指標操作、用 -&gt; 呼叫方法。getNext() 是 0（NULL）：新節點還沒接上任何人。用完 delete，這是 C++ 跟你的約定。')}'''
s, c1 = insert_end_of_section(s, "node", node, 'id="dx-node"')

uno = f'''<h3 id="dx-uno">講義完整範例：UnorderedList 全套操作</h3>
{card("講義 04 · add / size / search / remove", """#include <iostream>
#include "linked_list.hpp"
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
note="第一行輸出印證了 add 是<strong>頭插</strong>：最後加入的 54 排最前面。三次 remove 分別打中「中間、中間、尾巴」三種位置，下一張卡把指標動作攤開看。")}
<div class="deck-extra">
  <div class="dx-label">講義 04 · remove(26) 的指標舞步逐格看</div>
  <table style="width:100%;border-collapse:collapse;font-size:.88rem;">
    <tr style="border-bottom:2px solid var(--card-border);"><th style="text-align:left;padding:.4rem;">步驟</th><th style="text-align:left;">prev</th><th style="text-align:left;">cur</th><th style="text-align:left;">動作</th></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.4rem;">開始</td><td>NULL</td><td>head（54）</td><td>兩根指標起跑</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.4rem;">比對 54</td><td>54</td><td>26</td><td>不是目標：prev 跟上、cur 前進</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.4rem;">比對 26</td><td>54</td><td>26</td><td>找到了，停</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.4rem;">摘除</td><td colspan="2">prev-&gt;setNext(cur-&gt;getNext())</td><td>54 直接指向 93，26 被跳過</td></tr>
    <tr><td style="padding:.4rem;">收尾</td><td colspan="2">delete cur</td><td>歸還記憶體（若 cur == head，改成 head = head-&gt;getNext()）</td></tr>
  </table>
  <p class="dx-note">要背的只有一件事：<strong>單向串列摘節點需要「前一個」的協助</strong>，所以永遠帶著 prev、cur 兩根指標同行；目標剛好是 head 時沒有 prev，單獨處理。</p>
</div>'''
s, c2 = insert_end_of_section(s, "unordered", uno, 'id="dx-uno"')

odr = f'''{card("講義 04 · OrderedList：一樣的介面、排好的內容", """#include <iostream>
#include "linked_list.hpp"
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
note='<span id="dx-odr"></span>同樣六次 add、同樣的呼叫介面，印出來卻是由小到大：差別全在 add 內部「找到正確位置再插」。search(100) 也更聰明：一碰到比 100 大的節點就能放棄（這條串列裡沒有更大的希望了）。')}'''
s, c3 = insert_end_of_section(s, "ordered", odr, 'id="dx-odr"')

exx = f'''<div class="deck-extra" id="dx-exx">
  <div class="dx-label">cppds Ch.4 課後題精選（自我挑戰）</div>
  <ol style="font-size:.92rem;line-height:1.9;padding-left:1.4rem;">
    <li><strong>size 的 O(1) 版</strong>：現在的 size() 要走訪整條串列。把「節點數」存成成員變數，改寫 add / remove / size，讓 size() 變 O(1)。</li>
    <li><strong>防呆 remove</strong>：目標不在串列裡時，現在的 remove 會怎樣？改成安全版本（提示：cur 走到 NULL 就該停）。</li>
    <li><strong>補完 ADT</strong>：實作 append、index、pop、insert 四個缺席的方法，並分析各自的 Big-O。</li>
    <li><strong>slice(start, stop)</strong>：回傳從 start 到 stop（不含）的新串列。</li>
    <li><strong>用繼承減少重複</strong>：OrderedList 與 UnorderedList 大量方法相同。設計繼承階層，讓共同的部分只寫一次。</li>
    <li><strong>串列版 Stack／Queue／Deque</strong>：用鏈結串列各實作一次，跟第 3 章的 vector 版比效能。哪些操作變快、哪些變慢？</li>
  </ol>
  <p class="dx-note">完整題目在 <a href="https://github.com/pearcej/cppds/blob/master/_sources/LinearLinked/ProgrammingExercises.rst" target="_blank" rel="noopener">cppds ProgrammingExercises</a>；第 1、2 題是課本的自我檢測熱身，第 5 題會逼你把兩個類別的差異想透。</p>
</div>'''
s, c4 = insert_end_of_section(s, "exercises", exx, 'id="dx-exx"')

PAGE.write_text(s)
print("inserted:", [n for n, ok in zip("node uno odr exx".split(), [c1, c2, c3, c4]) if ok])
