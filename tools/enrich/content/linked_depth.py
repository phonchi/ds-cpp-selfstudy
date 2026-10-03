"""Chapter 4 supplemental teaching blocks; compiled examples are kept with outputs."""
from enrich_lib import card

def fold(title, body):
    return f'<details class="linked-detail"><summary>{title}</summary><div class="linked-detail-body">{body}</div></details>'

def table(headers, rows):
    return '<div style="overflow-x:auto"><table class="cmp-table"><thead><tr>'+''.join(f'<th>{h}</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{v}</td>' for v in r)+'</tr>' for r in rows)+'</tbody></table></div>'

EXAMPLES = {
'list': (r'''#include <iostream>
#include <list>
int main() {
    std::list<int> a{20, 30};
    a.push_front(10);
    a.push_back(40);              // 10 20 30 40
    auto pos = a.begin();
    ++pos;                       // points to 20; no a[1]
    auto inserted = a.insert(pos, 15); // before pos
    a.erase(inserted);           // erase 15; pos still points to 20
    a.pop_front();
    a.pop_back();                // 20 30
    a.push_back(35);
    for (auto it = a.begin(); it != a.end(); ) {
        if (*it % 2 == 0) it = a.erase(it);
        else ++it;
    }
    for (int x : a) std::cout << x << ' ';
    std::cout << "\nsize = " << a.size() << '\n';
}''', '35 \nsize = 1'),
'forward': (r'''#include <forward_list>
#include <iostream>
#include <iterator>
int main() {
    std::forward_list<int> a{20, 30};
    a.push_front(10);
    a.pop_front();                  // 20 30
    auto before = a.before_begin(); // position before first element
    a.insert_after(before, 10);     // 10 20 30
    auto first = a.begin();
    a.insert_after(first, 15);      // 10 15 20 30
    a.erase_after(first);           // 10 20 30
    auto prev = a.before_begin();
    auto cur = a.begin();
    while (cur != a.end()) {
        if (*cur >= 20) cur = a.erase_after(prev);
        else { prev = cur; ++cur; }
    }
    for (int x : a) std::cout << x << ' ';
    std::cout << "\ncount = " << std::distance(a.begin(), a.end()) << '\n';
}''', '10 \ncount = 1'),
'algorithms': (r'''#include <iostream>
#include <list>
template<class C> void show(const C& a) {
    for (int x : a) std::cout << x << ' ';
    std::cout << '\n';
}
int main() {
    std::list<int> a{3, 1, 1, 3, 2, 2};
    a.unique(); show(a); // only adjacent equal values
    a.remove(3); show(a); // all occurrences of 3
    a.push_back(1);
    a.sort(); show(a);
    a.unique(); show(a);
}''', '3 1 3 2 \n1 2 \n1 1 2 \n1 2 '),
'edges': (r'''#include <iostream>
#include "pythonds3/cppds/linked_list.hpp"
int main() {
    UnorderedList<int> a;
    a.remove(9);                        // empty: unchanged
    std::cout << std::boolalpha << a.isEmpty() << '\n';
    a.add(7); a.remove(7);              // only node
    std::cout << a.isEmpty() << '\n';
    a.add(10); a.add(20); a.add(20); a.add(30);
    a.remove(20);                      // first matching 20 only
    std::cout << a << '\n';
    a.remove(99);                      // missing: unchanged
    a.remove(30);                      // head
    a.remove(10);                      // tail
    std::cout << a << '\n';
    OrderedList<int> b;
    b.add(20); b.add(10); b.add(20);
    b.remove(20);
    std::cout << b << '\n';
}''', 'true\ntrue\n30 20 10 \n20 \n10 20 ')
}

def blocks():
    node = '''<h3>指標記住位置，不會複製節點</h3>
<p><code>head</code> 是串列物件保存的入口；<code>current</code> 是走訪時的游標；<code>previous</code> 記住 current 的前驅。令 <code>current = head</code> 只複製位址，兩者指向同一節點；令 <code>current = current-&gt;getNext()</code> 只移動游標，不會改變 head 或接線。</p>
<p><code>current-&gt;setData(42)</code> 會修改節點資料，<code>previous-&gt;setNext(current)</code> 才會修改鏈結。空串列的 <code>head == nullptr</code>；解參考前先檢查空指標。講義使用的 NULL 與此處 nullptr 都表示空指標，現代 C++ 通常使用 nullptr。</p>
<p>節點不必相鄰：next 存的是下一個節點的位置，不是下一個陣列索引。配置方式也不是 Node 類別本身的限制；此處用 new 動態配置，串列負責 delete。</p>'''
    uno = '''<h3>更新指標時，要維持哪些關係？</h3>
<p>尋找時維持：current 是待比較節點；若 previous 非空，<code>previous-&gt;getNext() == current</code>。前進必須先 <code>previous = current</code>，再更新 current；若反過來，兩者會停在同一節點。</p>
<ol><li><strong>插入：</strong>先讓新節點的 next 接到原來的後段，再讓 head 或前驅接到新節點。只有入口切換，後段不必搬移。</li><li><strong>刪除：</strong>先讀取 current 的 next，再讓 head 或前驅跳過 current，最後才 delete current。delete 之後不能再讀 current 的欄位。</li><li><strong>找不到：</strong>current 到達空指標就返回，不能解參考，也不應更動串列。</li></ol>'''+table(['情況','head／前驅的更新','結果'],[
('空串列 remove','不更新','仍為空'),('只剩一個節點且命中','head = current 的 next（空指標）','變成空串列'),('刪頭','head = current 的 next','新 head 是原第二節點'),('刪中間','previous 的 next = current 的 next','前後段接回'),('刪尾','previous 的 next = 空指標','previous 成為尾端'),('多個相同值','只跳過第一個命中節點','其餘相同值保留')])+card('空串列、重複值與頭尾刪除',*EXAMPLES['edges'])+fold('延伸：保存元素數量，讓 size() 變成 O(1)', '<p>本課實作的 size() 每次從 head 數到尾端，所以是 O(n)。可另存 count，成功新增後加一、確實刪除後減一；找不到時不減。建構、清空、複製與移動時也要維護 count。多保存一個計數，就能省下 size() 的走訪；因此 size() 的成本取決於類別的實作。</p>')
    ordered = '''<h3>有排序，為什麼搜尋仍是 O(n)？</h3>
<p>搜尋 45 時依序看 17、26、31、54；遇到 54 &gt; 45 就能停止，後方不可能有 45。搜尋 100 則必須看完所有節點。排序讓部分失敗搜尋提早結束，最壞情況仍要走訪 n 個節點；鏈結串列沒有 O(1) 的中點索引，不能直接套用陣列二分搜尋的 O(log n) 存取成本。</p>
<p>add(31) 必須先找出 26 與 54 之間的位置，再接上新節點。講義標頭用 current 找前驅，先接 <code>newNode-&gt;setNext(current-&gt;getNext())</code>，再接 <code>current-&gt;setNext(newNode)</code>。空串列或新值不大於首項時改走頭插；重複值允許存在，新值插在原有相等值之前。remove 只刪第一個相等值，遇到更大的值就停止。</p>'''+table(['操作','UnorderedList','OrderedList','成本來源'],[
('isEmpty()','O(1)','O(1)','只看 head'),('size()','O(n)','O(n)','逐節點計數'),('add(item)','O(1)','最壞 O(n)','有序版先定位'),('search / remove(item)','最壞 O(n)','最壞 O(n)','依值尋找'),('已知所需前驅後插／刪一個節點','O(1)','O(1)','固定次數接線；另須保持排序')])+ '<p>以上以元素比較、複製與析構為 O(1) 分析。刪除整段 k 個節點仍要 O(k)；「接線 O(1)」不包含尋找位置或逐一釋放整段。</p>'
    variants = '''<h3>環狀串列：回到起點才結束</h3>
<p>非空環狀串列的 tail-&gt;next 指向 head；不能再用「走到 NULL」判斷結束。先處理空串列，再至少拜訪一次起點；只有一個節點時，其 next 指向自己，也剛好拜訪一次。</p>'''+card('環狀走訪片段（假設鏈結已形成完整環）', '''if (head != nullptr) {
    Node<int>* current = head;
    do {
        std::cout << current->getData() << ' ';
        current = current->getNext();
    } while (current != head);
}''')+'''<p>保存 tail 時，可用 tail-&gt;next 取得 head，頭插或尾插可在 O(1) 完成；刪除單向環的尾節點仍需找前驅，最壞 O(n)。環狀只改變終止關係，沒有增加反向走訪能力。</p>
<h3>雙向串列：左右兩邊都要接回</h3>
<p>以不存使用者資料的 header、trailer 作哨兵：空串列為 <code>header ↔ trailer</code>，非空為 <code>header ↔ 第一項 ↔ … ↔ 最後一項 ↔ trailer</code>。header 的 prev 與 trailer 的 next 可為空；走訪停在 trailer，不能把哨兵當資料讀取或刪除。</p>'''+card('雙向插入／刪除的接線片段（prev、next 為示意欄位）', '''// Insert a newly allocated node x between adjacent nodes left and right.
x->prev = left;
x->next = right;
left->next = x;
right->prev = x;

// Erase a real data node x; never erase a sentinel.
auto left = x->prev;
auto right = x->next;
left->next = right;
right->prev = left;
delete x;''')+'''<p>第一個與最後一個資料節點也都有兩個鄰居，因此使用同一套接線；刪掉最後一項後自然恢復 header ↔ trailer。已知 x 時刪除為 O(1)，但依值尋找 x 仍為 O(n)。只保存 head 的雙向串列仍需尋找尾端；要 O(1) 尾端操作，還需保存 tail 或 trailer。</p>'''
    stl = fold('實作練習：std::list 的建立、頭尾增刪與安全刪除迴圈',card('雙向串列：插在位置之前，刪除後接回下一個位置',*EXAMPLES['list'])+'''<p>begin() 指向第一項，end() 是尾後位置，不能解參考。insert(pos,x) 插在 pos 前並回傳新項位置；erase(it) 回傳被刪項的下一個位置。迴圈刪除後使用這個回傳值，不能對已失效的 it 做 ++it。</p><p>push_front / push_back / pop_front / pop_back 與單項 insert / erase 都是 O(1)，前提是位置已知且符合操作前提。pop、front、back 要求非空；erase(end()) 不合法；insert(end(),x) 則是合法尾插。std::find 或逐步 ++ 找位置是 O(n)。</p>''')+fold('實作練習：std::forward_list 與 before_begin()',card('單向串列：保留前驅才能安全刪除',*EXAMPLES['forward'])+'''<p>before_begin() 是「第一項前面」的特殊位置，不能解參考，但可傳給 insert_after / erase_after，統一處理頭端。end() 是尾後位置，不能拿來 insert_after；erase_after(prev) 要求 prev 後確實有可刪的元素。</p><p>刪除 current 後，previous 留在原處，current 接回 erase_after 的回傳值；保留 current 時才一起前進。這正對應前面 previous/current 的指標關係。forward_list 沒有 size()、back() 或 push_back()；std::distance(begin(),end()) 需要 O(n) 走訪。std::list::size() 在 C++11 起為 O(1)。兩者都沒有 [] 與 at()；std::next(it,k) 需要 O(k) 前進，不是直接索引。</p>''')+fold('延伸：remove、unique、sort 與迭代器有效性',card('先分清楚「全部符合」與「相鄰重複」',*EXAMPLES['algorithms'])+table(['成員操作（兩種串列皆有）','效果','成本'],[('remove(x) / remove_if(pred)','刪掉所有符合項；不同於本課 remove 只刪第一項','O(n) 次比較／條件判斷'),('unique()','每一段相鄰相等值只保留第一項；不會搜尋隔開的重複值','O(n) 次比較'),('sort()','穩定排序；相等元素保留原相對次序','約 O(n log n) 次比較')])+'''<p>兩種串列皆可使用同樣的三個成員操作。若要移除整個串列中的重複值，可先 sort 再 unique，但元素原順序會改變；只想移除某值就用 remove。std::sort 需要隨機存取迭代器，因此不能套在這兩種串列，應用成員 sort()。</p><p>單項插入不使既有節點的迭代器或參考失效；刪除只使被刪節點的迭代器／參考失效，其他節點仍有效。remove 與 unique 也適用此規則。sort 會改變走訪順序，但保留指向元素的迭代器／參考。容器析構或 clear 後，原元素全部消失，不能再使用指向它們的迭代器。</p><p>參考：<a href="https://eel.is/c++draft/list">C++ 標準草案：list</a>、<a href="https://eel.is/c++draft/forward.list">forward_list</a>。</p>''')+fold('如何選擇 vector、list 與 forward_list？','''<p>需要依索引讀取、緊密儲存與大量循序掃描時，可先選 vector。頻繁在已知位置插刪、需要保留其他元素的參考或迭代器時，再考慮鏈結容器。list 可雙向走訪並提供 O(1) 頭尾操作；forward_list 只向前走，需要自己保留前驅。若每次插入前都從頭尋找位置，整體仍是 O(n)。節點額外指標與分散配置可能增加記憶體及快取成本，不能只比較接線次數。</p>''')
    return {'node':node,'unordered':uno,'ordered':ordered,'variants':variants,'stl':stl}
