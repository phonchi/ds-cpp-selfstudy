"""Chapter 4 section bodies. Each value of sections() fills one <!-- gen:NAME --> block.

Code shown as lecture or header code is copied from 04_Linear_Linked_Structure.ipynb and
pythonds3/cppds/linked_list.hpp; expected outputs come from compiling the programs.
"""
from html import escape
from enrich_lib import hl
from content.linked_figures import figure, steps
from content.linked_programs import *  # noqa: F401,F403  (complete programs and OUTPUT)


def details(summary, body, cls='linked-detail', did=''):
    ident = f' id="{did}"' if did else ''
    return f'<details class="{cls}"{ident}><summary>{summary}</summary><div class="linked-detail-body">{body}</div></details>'


def fold(title, body, did=''):
    """Content that the lecture does not cover: collapsed and labelled （補充）."""
    return details(title + '（補充）', body, did=did)


def table(headers, rows):
    return ('<div style="overflow-x:auto"><table class="cmp-table"><thead><tr>'
            + ''.join(f'<th>{h}</th>' for h in headers) + '</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{v}</td>' for v in r) + '</tr>' for r in rows)
            + '</tbody></table></div>')


def quiz(qid, label, question, options):
    """options: [(correct, text, feedback)]; the page shuffles option order at load time."""
    opts = ''.join(
        f'<div class="quiz-opt" data-correct="{"true" if ok else "false"}" data-fb="{escape(fb, quote=True)}" '
        f'onclick="quizCheck(\'{qid}\', this)"><span class="opt-letter">({chr(65 + i)})</span> <span class="opt-text">{text}</span></div>'
        for i, (ok, text, fb) in enumerate(options))
    return (f'<div class="quiz-box">\n  <div class="quiz-label">{label}</div>\n  <p>{question}</p>\n'
            f'  <div class="quiz-options" id="{qid}Options">\n    {opts}\n  </div>\n'
            f'  <div class="quiz-feedback" id="{qid}Feedback"></div>\n</div>')


LEGEND = {
    'hl': ('#fff3cd', '#d68910', '正在處理的節點'),
    'cmp': ('#f4ecf7', '#7d3c98', '正在比較的節點'),
    'found': ('#d5f5e3', 'var(--accent3)', '找到的節點'),
    'new': ('#e9f7ef', 'var(--accent3)', '新節點或剛改過的指標'),
    'del': ('transparent', 'var(--accent)', '已釋放的節點'),
    'lost': ('var(--card)', 'var(--muted)', '無法再到達的節點'),
    'skip': ('var(--card)', 'var(--node-gray)', '未走訪的節點'),
    'sent': ('#eceff1', 'var(--muted)', '哨兵節點'),
}


def widget(p, cases, status, codes=(), legend=(), extra='', aside=''):
    """One player-v2 animation: case buttons pick a scenario; ▶／→／⏸ and the speed slider drive it."""
    leg = ''.join(f'<span><i class="ll-sw" style="background:{bg};border-color:{bd};"></i>{txt}</span>'
                  for bg, bd, txt in (LEGEND[k] for k in legend))
    btns = ''.join(f'<button class="btn ll-case" data-ll="{p}" onclick="llCase(\'{p}\', \'{k}\', this)">{label}</button>'
                   for k, label in cases)
    panel = f'''<div class="viz-panel">
  <div class="ll-canvas" id="{p}Vis"></div>
  {f'<div class="ll-legend">{leg}</div>' if leg else ''}
  <div class="status-banner" id="{p}Status"><span class="status-icon">›</span><span class="status-text">{status}</span></div>
  <div class="controls-bar">{btns}{extra}</div>
  <div class="controls-bar ll-play">
    <button class="btn btn-play" onclick="llPlay('{p}')">▶ 播放</button>
    <button class="btn btn-step" onclick="llStep('{p}')">→ 單步</button>
    <button class="btn btn-toggle" id="{p}Toggle" onclick="llToggle('{p}', this)">⏸ 暫停</button>
    <span class="mono" style="font-size:.8rem;color:var(--muted);">速度 <input id="{p}Speed" type="range" min="120" max="1200" value="650" style="vertical-align:middle;" aria-label="每一步的間隔"></span>
    <span class="ll-count" id="{p}Count"></span>
  </div>
</div>'''
    side = ''.join(
        f'<div class="info-card" data-ll-code="{p}" data-idx="{j}"{" hidden" if j else ""}><div class="ic-title"><span>{title}</span> <span class="ic-badge">CODE</span></div>'
        f'<div class="pseudo-code" id="{p}Code{j}">{hl(code)}</div></div>'
        for j, (title, code) in enumerate(codes)) + aside
    if not side:
        return f'<div class="ll-widget">{panel}</div>'
    return f'<div class="viz-layout ll-widget"><div>{panel}</div><div class="side-panel">{side}</div></div>'


def _expected_attr(output):
    return ' data-expected="' + escape(output + '\n', quote=True).replace('\n', '&#10;') + '"'


def _expected_out(output):
    return ('<div class="expected-out"><span class="eo-tag">預期輸出</span><pre>'
            + escape(output) + '</pre></div>')


def snippet(label, code, output=None, note=None, kind=None):
    """Code card. kind follows the chapter-3 convention (data-cpp = run | fragment | compile-error | header);
    complete programs with an output default to run, and data-expected holds the exact stdout."""
    if kind is None:
        kind = 'run' if output is not None and 'int main' in code else 'fragment'
    attrs = f' data-cpp="{kind}"' + (_expected_attr(output) if kind == 'run' and output is not None else '')
    parts = ['<div class="deck-extra">', f'  <div class="dx-label">{label}</div>',
             f'  <div class="pseudo-code" style="font-size:.8rem;"{attrs}>{hl(code)}</div>']
    if output is not None:
        parts.append('  ' + _expected_out(output))
    if note:
        parts.append(f'  <p class="dx-note">{note}</p>')
    parts.append('</div>')
    return '\n'.join(parts)


def lecture_program(summary, label, code, output, note=None):
    """Lecture full program: collapse the code, keep the expected output and note visible."""
    card = snippet(label, code, kind='run').replace('data-cpp="run"', 'data-cpp="run"' + _expected_attr(output), 1)
    out = _expected_out(output)
    if note:
        out += f'<p class="dx-note">{note}</p>'
    return details(summary, card) + out


# ---------------------------------------------------------------- lecture / header code
NODE_CLASS = '''template <typename T>
class Node {
    private:
        T data;           // data of generic type
        Node<T> *next;    // pointer to the next node
    public:
        Node(T initdata) {
            data = initdata;
            next = NULL;
        }
        T getData() const {
            return data;
        }
        Node<T> *getNext() const {
            return next;
        }
        void setData(T newData) {
            data = newData;
        }
        void setNext(Node<T> *newnext) {
            next = newnext;
        }
};'''

NODE_LINES = '''Node<int> *temp = new Node<int>(93);
cout << temp->getData() << endl;
cout << temp->getNext() << endl;   // NULL prints as 0
delete temp;'''

NODE_MAIN = '''#include <iostream>
#include "pythonds3/cppds/linked_list.hpp"   // Node / UnorderedList / OrderedList
using namespace std;

int main() {
    Node<int> *temp = new Node<int>(93);
    cout << temp->getData() << endl;
    cout << temp->getNext() << endl;   // NULL prints as 0
    delete temp;
    return 0;
}'''

UL_SKELETON = '''template <typename T>
class UnorderedList {
    private:
        Node<T> *head;
    public:
        UnorderedList() {
            head = NULL;
        }
};'''

IS_EMPTY = '''bool isEmpty() const {
    return head == NULL;
}'''

UL_ADD = '''void add(T item) {
    Node<T> *temp = new Node<T>(item);
    temp->setNext(head);
    head = temp;
}'''

UL_ADD_WRONG = '''void add(T item) {   // wrong order
    Node<T> *temp = new Node<T>(item);
    head = temp;
    temp->setNext(head);
}'''

UL_SIZE = '''int size() const {
    Node<T> *current = head;
    int count = 0;
    while (current != NULL) {
        count++;
        current = current->getNext();
    }
    return count;
}'''

UL_SEARCH = '''bool search(T item) const {
    Node<T> *current = head;
    while (current != NULL) {
        if (current->getData() == item) {
            return true;
        }
        current = current->getNext();
    }
    return false;
}'''

UL_REMOVE = '''void remove(T item) {
    Node<T> *current = head;
    Node<T> *previous = NULL;
    bool found = false;
    // Step 1: traverse to find the item
    while (!found && current != NULL) {
        if (current->getData() == item) {
            found = true;
        } else {
            previous = current;
            current = current->getNext();
        }
    }
    // Step 2: unlink and FREE the node (C++ has no garbage collector!)
    if (found) {
        if (previous == NULL) {
            head = current->getNext();
        } else {
            previous->setNext(current->getNext());
        }
        delete current;
    }
}'''

UL_MAIN = '''#include <iostream>
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
}'''

UL_PRINT = '''friend ostream& operator<<(ostream& os, const UnorderedList<T>& ol) {
    Node<T> *current = ol.head;
    while (current != NULL) {
        os << current->getData() << " ";
        current = current->getNext();
    }
    return os;
}'''

EDGES = r'''#include <iostream>
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
}'''

OWNERSHIP = '''UnorderedList<int> a;
a.add(1); a.add(2);
UnorderedList<int> b = a;  // copies the whole chain
b.remove(2);               // must not change a'''

APPEND = '''void append(T item) {
    Node<T> *temp = new Node<T>(item);
    if (head == NULL) {
        head = temp;
        return;
    }
    Node<T> *current = head;
    while (current->getNext() != NULL) {
        current = current->getNext();
    }
    current->setNext(temp);
}'''

OL_SKELETON = '''template <typename T>
class OrderedList {
    private:
        Node<T> *head;

    public:
        OrderedList() {
            head = NULL;
        }
};'''

OL_SEARCH = '''bool search(T item) const {
    Node<T> *current = head;
    while (current != NULL) {
        if (current->getData() == item) {
            return true;
        } else if (current->getData() > item) {
            return false;   // passed the spot: stop early!
        }
        current = current->getNext();
    }
    return false;
}'''

OL_ADD = '''void add(T item) {
    Node<T> *newNode = new Node<T>(item);
    if (head == NULL || head->getData() >= item) {
        newNode->setNext(head);
        head = newNode;
    } else {
        Node<T> *current = head;
        while (current->getNext() != NULL && current->getNext()->getData() < item) {
            current = current->getNext();
        }
        newNode->setNext(current->getNext());
        current->setNext(newNode);
    }
}'''

OL_ADD_BOOK = '''void add(int item) {
    if (head == nullptr) {
        Node *newNode = new Node(item);
        head = newNode;
    } else {
        Node *current = head;
        Node *previous = nullptr;
        bool stop = false;
        while (current != nullptr && !stop) {
            if (current->getData() > item) {
                stop = true;
            } else {
                previous = current;
                current = current->getNext();
            }
        }
        Node *temp = new Node(item);
        if (previous == nullptr) {
            temp->setNext(head);
            head = temp;
        } else {
            temp->setNext(current);
            previous->setNext(temp);
        }
    }
}'''

OL_REMOVE = '''void remove(T item) {
    Node<T> *current = head, *previous = NULL;
    while (current != NULL && current->getData() < item) {
        previous = current;
        current = current->getNext();
    }
    if (current == NULL || current->getData() != item) return;
    if (previous == NULL) head = current->getNext();
    else previous->setNext(current->getNext());
    delete current;
}'''

OL_MAIN = '''#include <iostream>
#include "pythonds3/cppds/linked_list.hpp"
using namespace std;

int main() {
    OrderedList<int> myList;
    for (int value : {31, 77, 17, 93, 26, 54}) myList.add(value);
    cout << myList << endl;
    cout << myList.size() << endl;
    cout << boolalpha << myList.search(93) << endl;
    cout << myList.search(100) << endl;
    myList.remove(31);
    myList.remove(100);  // missing value: no-op
    cout << myList << endl;
}'''

STL_MAIN = '''#include <forward_list>
#include <iostream>
#include <list>
using namespace std;

int main() {
    forward_list<int> singly = {31, 54};
    singly.insert_after(singly.before_begin(), 17);
    list<int> doubly = {17, 31, 54};
    auto pos = next(doubly.begin());
    doubly.insert(pos, 26);
    for (int x : singly) cout << x << ' ';
    cout << endl;
    for (int x : doubly) cout << x << ' ';
    cout << endl;
}'''

STL_LIST = r'''#include <iostream>
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
}'''

STL_FORWARD = r'''#include <forward_list>
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
}'''

STL_ALGOS = r'''#include <iostream>
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
}'''

CIRCULAR = '''if (head != nullptr) {
    Node<int>* current = head;
    do {
        std::cout << current->getData() << ' ';
        current = current->getNext();
    } while (current != head);
}'''

D_INSERT = '''// Insert newNode between adjacent nodes pred and succ.
newNode->prev = pred;
newNode->next = succ;
pred->next = newNode;
succ->prev = newNode;'''

D_ERASE = '''// Erase a real data node; never erase a sentinel.
auto pred = node->prev;
auto succ = node->next;
pred->next = succ;
succ->prev = pred;
delete node;'''

# Outputs were obtained by compiling each program with g++ -std=c++17 against the course headers.
OUT = {
    'node': '93\n0',
    'ul': '54 26 93 17 77 31 \n6\ntrue\n26 17 77 ',
    'edges': 'true\ntrue\n30 20 10 \n20 \n10 20 ',
    'ol': '17 26 31 54 77 93 \n6\ntrue\nfalse\n17 26 54 77 93 ',
    'stl': '17 31 54 \n17 26 31 54 ',
    'list': '35 \nsize = 1',
    'forward': '10 \ncount = 1',
    'algos': '3 1 3 2 \n1 2 \n1 1 2 \n1 2 ',
}
OUT.update(OUTPUT)


def prologue():
    adt = table(['操作', '作用', '課程標頭的 <code>UnorderedList</code>'], [
        ('UnorderedList()', '建立空串列', '提供'),
        ('isEmpty()', '檢查 head == NULL', '提供'),
        ('add(item)', '在 head 加入新元素，$O(1)$', '提供'),
        ('size()', '回傳元素個數', '提供'),
        ('search(item)', '回傳 item 是否在串列中', '提供'),
        ('remove(item)', '移除第一個相等的元素；找不到時串列不變', '提供'),
        ('append(item)', '把新元素加到尾端，成為最後一項', '未提供，留作練習'),
        ('index(item)', '回傳 item 的位置', '未提供'),
        ('insert(pos, item)', '在位置 pos 加入新元素', '未提供'),
        ('pop()／pop(pos)', '移除並回傳最後一項／位置 pos 的項', '未提供'),
    ])
    aside = '''<div class="info-card">
  <div class="ic-title">取捨一覽</div>
  <div class="ic-row"><span class="ic-label">依位置讀取</span><span class="ic-value">陣列 $O(1)$｜串列 $O(n)$</span></div>
  <div class="ic-row"><span class="ic-label">頭端插入／刪除</span><span class="ic-value">陣列 $O(n)$｜串列 $O(1)$</span></div>
  <div class="ic-row"><span class="ic-label">額外空間</span><span class="ic-value">串列每個節點多存指標</span></div>
</div>
<div class="info-card">
  <div class="ic-title">分時系統的例子（課本）</div>
  <div style="font-size:.86rem;line-height:1.9;">作業系統讓多個工作輪流使用 CPU，每個工作分到一小段時間後換下一個。課本以這種分時（timesharing）說明鏈結結構：輪流的順序可以用環狀鏈結串列表示。</div>
</div>'''
    return f'''<p>前面的 ArrayList 建立在連續的原生陣列上。本章改用<strong>節點（node）與指標（pointer）</strong>組成集合：元素不必放在相鄰的記憶體位置，每個節點記得下一個節點在哪裡。只要知道第一個節點（<strong>head</strong>），就能沿著指標依序找到其他元素。</p>
<h3>串列 ADT：元素之間有相對位置</h3>
<p>串列（List）是一群元素的集合，每個元素相對於其他元素有固定的位置：有第一項、第二項、第三項……。若這個順序與元素的值無關，就稱為<strong>無序串列</strong>（Unordered List）。定義 ADT 時，講義與課本為了簡化，假設串列中沒有重複的元素。無序串列 ADT 可能包含下列操作：</p>
{adt}
<p>後四項屬於較完整的串列 ADT。課程標頭 <code>pythonds3/cppds/linked_list.hpp</code> 的 UnorderedList 只實作前六項；append 留到本頁的練習區。</p>
<p>較完整的 ADT 也寫明了各操作的前提：append 與 insert 假設元素原本不在串列中；index 假設元素一定在串列中；insert(pos, item) 假設串列已有足夠的元素，位置 pos 才存在；pop() 假設串列至少有一個元素。實作這些操作時，要先決定違反前提時怎麼處理，例如課程標頭的 remove 在找不到元素時，選擇讓串列保持不變。</p>
<h3>為什麼需要另一種表示法</h3>
<p>ArrayList 把元素放在一段連續的陣列裡，依位置讀取很快，代價是要維持「連續」：在最前面插入一項，後面每一項都得往後搬一格；容量用完時，還要配置更大的陣列並把元素全部複製過去。如果程式經常在前端或中間插入、刪除，這些搬移就會成為主要成本。</p>
<p>串列真正需要維持的只有元素之間的<strong>相對順序</strong>，並不要求它們在記憶體中相鄰。只要每個元素記得下一個元素在哪裡，順序就保存下來了；找到位置之後，插入或刪除只要改幾個指標，不必搬動其他元素。</p>
<h3>鏈結表示：每一項記住下一項在哪裡</h3>
<p>下面六個整數放在記憶體中的不同位置。只看它們的位置，看不出誰是第一項、誰排在誰後面。</p>
{figure('scatter')}
<p>如果每一項都多存一筆明確的資訊，也就是<strong>下一項的位置</strong>，那麼順著這些連結，從一項走到下一項，就能重建整個順序：</p>
{figure('linked')}
<p>這個表示法有兩個必要條件。第一，<strong>第一項的位置必須另外記住</strong>：知道第一項在哪裡，第一項就能告訴我們第二項在哪裡，依此類推。這個指向第一項的外部參考稱為串列的 <strong>head</strong>。第二，<strong>最後一項必須知道後面沒有下一項</strong>，走訪時才知道何時停下。下一節的 Node 類別用一個資料欄位存元素、用 next 指標存下一項的位置，並以 NULL 表示「沒有下一項」。</p>
<h3>記憶體裡的樣子：用公式定位，或沿指標前進</h3>
<p>同樣讀第 k 項（零起始），陣列用位址公式一次算出位置；鏈結串列沒有這種公式，只能從 head 出發，沿 next 一步一步走過去。選一種表示法與 k，用「→ 單步」比較兩者需要的步數。</p>
{widget("mem", [("array", "陣列：讀 a[k]"), ("linked", "鏈結串列：讀第 k 項")],
        "選一種表示法，再按 ▶ 播放或 → 單步。", legend=("hl", "found"),
        extra='<label class="mono" style="font-size:.85rem;">k = <input id="memK" type="number" min="0" max="4" value="3" style="width:56px;padding:.3rem .4rem;border:1px solid var(--card-border);border-radius:6px;" onchange="llRecase(\'mem\')"></label>',
        aside=aside)}'''


def node_section():
    pointer_note = '''<div style="font-size:.9rem;line-height:2;" class="mono">
<code>Node&lt;int&gt; *p = new Node&lt;int&gt;(93);</code><br>
<code>p-&gt;getData()</code>  // 93<br>
<code>p-&gt;getNext()</code>  // NULL<br>
<code>delete p;</code>  // 釋放節點</div>
<p><code>p-&gt;getNext()</code> 透過指標 p 呼叫節點的方法，等同於 <code>(*p).getNext()</code>；使用前要確認 p 指向有效的節點。講義使用 NULL 表示空指標；現代 C++ 通常寫 nullptr，兩者在這裡的意思相同。</p>
<p>指標只記住位置，不會複製節點：令 current = head 只複製位址，兩者指向同一個節點；令 current = current-&gt;getNext() 只移動 current，不會改變 head 或任何鏈結。current-&gt;setData(42) 修改節點的資料，previous-&gt;setNext(current) 才會修改鏈結。</p>'''
    methods = table(['成員函式', '作用', '會不會改變節點'], [
        ('Node(T initdata)', '建構子：data 設成 initdata，next 設成 NULL', '建立新節點'),
        ('getData() const', '回傳資料欄位的值', '不會（const）'),
        ('getNext() const', '回傳 next 指標，也就是下一個節點的位址；沒有下一個節點時回傳 NULL', '不會（const）'),
        ('setData(newData)', '把資料欄位改成 newData', '只改資料，不改鏈結'),
        ('setNext(newnext)', '把 next 改成指向 newnext', '改變鏈結'),
    ])
    return f'''<p>節點是鏈結串列的基本單位。每個節點至少保存兩項資訊：<strong>資料欄位</strong> data 存放元素本身，next 指向下一個節點。講義把 Node 寫成類別模板，T 是元素的型別：Node&lt;int&gt; 存整數，Node&lt;string&gt; 存字串，鏈結的寫法完全相同。</p>
{snippet("講義 04 · Node 類別（pythonds3/cppds/linked_list.hpp）", NODE_CLASS)}
<h3>封裝：只能透過四個成員函式存取</h3>
<p>data 與 next 兩個欄位都是 private。串列的程式與使用者的程式都只能透過 getData()、getNext()、setData()、setNext() 存取節點；直接寫 node-&gt;next 是刻意不允許的寫法，無法通過編譯。</p>
{methods}
<p>兩個 get 函式標成 const，表示呼叫它們不會修改節點，所以在 size()、search() 這類 const 成員函式裡也能使用。要特別分清楚 setData 與 setNext：前者只換掉節點裡的值，後者才會改變節點之間的連接方式。</p>
{snippet("直接存取 private 欄位：無法編譯", NODE_PRIVATE, kind='compile-error', note="編譯器會指出 next 是 private 成員。要讓節點不指向任何東西，應該寫 temp-&gt;setNext(NULL)。")}
<h3>建立、使用與釋放一個節點</h3>
<p>用 new 在 heap 配置節點，取得它的位址；用 -&gt; 透過指標呼叫方法；用完後以 delete 釋放。按 → 單步，看 temp 在每一行之後指向什麼。</p>
{widget("node", [("run", "執行這四行")], "按 ▶ 播放或 → 單步。", codes=[("講義 04 · 使用 Node", NODE_LINES)], legend=("new", "hl", "del"))}
{lecture_program("講義完整程式：建立一個 Node", "講義 04 · Node 的使用", NODE_MAIN, OUT['node'], note="第一行是節點的資料 93。第二行印出 next 指標：新節點的 next 是 NULL，用 cout 印出空指標時會顯示 0。")}
{figure('node93')}
<h3>NULL：沒有下一個節點</h3>
<p>C++ 的特殊指標值 NULL 在 Node 類別與之後的串列中都很重要：next 等於 NULL，表示這個節點後面沒有節點。之後的 size、search、remove 都是走到 NULL 才停下，串列的 head 等於 NULL 則表示串列是空的。</p>
<p>注意建構子把 next 明確設成 NULL。指標若沒有初始化，裡面是無法預測的值；把它當成位址去讀取，結果是未定義行為，程式可能當掉，也可能看似正常卻讀到錯誤的資料。所以建立指標時，一律先給它明確的初值。課本把 next 為空的節點稱為 grounded（接地），圖中用電路的接地符號表示（課本）。</p>
{fold("指標語法速記", pointer_note)}
{fold("用 setNext 手動接起三個節點", snippet("三個節點接成 54 → 26 → 93", NODE_CHAIN, OUT['node_chain'], note="setNext 決定誰接在誰後面；setData(27) 只改了第二個節點的值，鏈結不變。while 迴圈用 current 沿 next 前進、遇到 NULL 停下，這就是下一節 size 與 search 使用的走訪寫法。"))}'''


def unordered_section():
    trace = '''<div class="deck-extra">
  <div class="dx-label">講義 04 · remove(26) 的指標更新步驟</div>
  <p>從六次 add 後的串列 54 → 26 → 93 → 17 → 77 → 31 開始。</p>
  <div style="overflow-x:auto"><table class="cmp-table">
    <thead><tr><th>步驟</th><th>previous</th><th>current</th><th>found</th><th>動作</th></tr></thead>
    <tbody>
    <tr><td>開始</td><td>NULL</td><td>54</td><td>false</td><td>current = head</td></tr>
    <tr><td>比對 54</td><td>54</td><td>26</td><td>false</td><td>不相等：previous 先移到 current，current 再前進</td></tr>
    <tr><td>比對 26</td><td>54</td><td>26</td><td>true</td><td>相等：found = true，離開迴圈</td></tr>
    <tr><td>移除</td><td colspan="3">previous-&gt;setNext(current-&gt;getNext())</td><td>54 改指 93，26 被跳過</td></tr>
    <tr><td>釋放</td><td colspan="3">delete current</td><td>釋放 26 的節點</td></tr>
    </tbody>
  </table></div>
</div>'''
    edges = table(['情況', 'head 或前驅的更新', '結果'], [
        ('空串列 remove', '不更新', '仍為空'),
        ('只剩一個節點且命中', 'head = current-&gt;getNext()，也就是 NULL', '變成空串列'),
        ('刪頭', 'head = current-&gt;getNext()', '新的 head 是原本的第二個節點'),
        ('刪中間', 'previous-&gt;setNext(current-&gt;getNext())', '前後兩段接回'),
        ('刪尾', 'previous-&gt;setNext(NULL)', 'previous 成為最後一個節點'),
        ('找不到', '不更新', '串列不變'),
        ('多個相同值', '只跳過第一個命中的節點', '其餘相同值保留'),
    ])
    ownership = snippet("所有權與深層複製", OWNERSHIP, note="串列物件擁有它用 new 配置的節點：解構子要逐一 delete；複製建構子與複製指派要複製整條鏈（deep copy）。若只複製 head，兩個串列會共用同一批節點，之後可能重複釋放。課程標頭已依這個規則實作。")
    q_order = quiz('qUll', 'QUIZ · add 的兩行順序',
                   'add 裡若把兩行寫反（先 head = temp，再 temp-&gt;setNext(head)），會發生什麼事？', [
                       (True, 'temp 的 next 指向自己，原本的節點全部無法到達',
                        'head 先被改成 temp，之後 temp->setNext(head) 讓新節點指向自己；原本的節點沒有任何指標可以到達，也無法再釋放。'),
                       (False, '沒有差別，結果一樣',
                        '順序很重要：必須先讓新節點接住原本的串列，才能移動 head。'),
                       (False, '編譯錯誤',
                        '兩行都是合法的 C++，可以通過編譯；問題出在執行時指標指向哪裡。'),
                       (False, '串列自動變成環狀串列',
                        '環狀串列是最後一個節點指回第一個節點、所有節點仍連在環上；這裡只有新節點指向自己，原本的節點全部脫離。'),
                   ])
    return f'''<p>無序串列的類別本身不存放任何節點，只保存一個指向第一個節點的指標 head。以下依序實作 add、size、search、remove；其中 size、search、remove 都建立在<strong>走訪</strong>（traversal）上：用一個外部指標從 head 出發，沿著 next 逐一拜訪節點，直到遇到 NULL。</p>
<h3>head 與空串列</h3>
{snippet("講義 04 · UnorderedList 的資料成員與建構子", UL_SKELETON)}
<p><code>UnorderedList&lt;int&gt; myList;</code> 會建立空串列：建構子把 head 設為 NULL，此時沒有任何節點。</p>
{figure('empty')}
<p>和 Node 一樣，這裡的 NULL 表示 head 沒有指向任何節點。加入元素之後，前面那六個整數最後會以下面的鏈結形式存放：</p>
{figure('chain')}
<p>head 指向第一個節點，第一個節點存放串列的第一項，並指向下一個節點，依此類推。要特別注意：<strong>UnorderedList 物件本身並不包含任何節點</strong>，它只保存一個指向鏈結結構中第一個節點的指標；節點都是用 new 另外配置在 heap 上的。</p>
<p>isEmpty() 只要檢查 head 是否為 NULL：串列沒有任何節點時，正好回傳 true。它只看一個指標，所以是 $O(1)$。</p>
{snippet("講義 04 · isEmpty", IS_EMPTY)}
{lecture_program("完整程式：空串列與 isEmpty", "空串列的 isEmpty 與 size", UL_EMPTY, OUT['ul_empty'], note="剛建立的 myList 是空串列：isEmpty() 為 true、size() 為 0。加入 31 之後，head 指向一個節點，isEmpty() 變成 false。")}
<h3>add：把新節點放在 head</h3>
<p>無序串列不在乎新元素放在哪裡，所以放在最容易的位置。其他節點都只能從 head 沿 next 走到，唯有第一個節點可以直接存取，因此新節點加在 head。連續執行 add(31)、add(77)、add(17)、add(93)、add(26)、add(54) 之後，最先加入的 31 在最後面，最後加入的 54 在最前面。</p>
<p>第 3 行先讓新節點的 next 接住原本的第一個節點，第 4 行才讓 head 指向新節點。按 → 單步觀察：在第 3 行之後，head 與新節點同時指向 93，所以後段不會遺失。</p>
{widget("uAdd", [("mid", "add(26)"), ("empty", "空串列 add(26)"), ("wrong", "兩行順序對調")],
        "選一個情況，再按 ▶ 播放或 → 單步。", codes=[("講義 04 · add", UL_ADD), ("兩行順序對調（錯誤示範）", UL_ADD_WRONG)], legend=("new", "lost"))}
{figure('add')}
{lecture_program("完整程式：六次 add，每次印出串列", "講義 04 · 依序 add(31)、add(77)、add(17)、add(93)、add(26)、add(54)", UL_ADDS, OUT['ul_adds'], note="每一行都比上一行多一個值，而且新值總是出現在最前面：最先加入的 31 一路被推到最後，最後加入的 54 成為第一個節點。")}
<p>兩行的順序不能對調。若先執行 head = temp，原本唯一指向 93 的 head 就被改掉，原來的節點再也找不到，也無法 delete；接著 temp-&gt;setNext(head) 讓新節點指向自己。</p>
{figure('wrong')}
{q_order}
<h3>size：走訪並計數</h3>
<p>current 從 head 出發；每進入一次迴圈，先把 count 加一，再讓 current 沿 next 前進。current 變成 NULL 時，每個節點都恰好數過一次。這份實作沒有另存元素個數，所以 size() 是 $O(n)$；若類別另外維護一個計數成員，size() 可以是 $O(1)$，代價是每次新增與刪除都要更新它。</p>
{widget("uSize", [("four", "四個節點"), ("empty", "空串列")], "選一個情況，再按 ▶ 播放或 → 單步。", codes=[("講義 04 · size", UL_SIZE)], legend=("hl",))}
<p>以六個節點的串列為例，current 依序停在每個節點，最後停在 NULL：</p>
{figure('size')}
<p>第 2 行讓 current 指向 head，這時還沒看過任何節點，所以 count 從 0 開始。第 4 至 6 行是走訪本身：只要 current 還沒走到串列結尾（NULL），就把 count 加一，再用第 6 行的指定敘述讓 current 移到下一個節點。能把指標拿來和 NULL 比較，是走訪能停下來的關鍵。迴圈結束後回傳 count。空串列時 current 一開始就是 NULL，迴圈一次也不執行，回傳 0。</p>
{lecture_program("完整程式：size 的三種情況", "size()：空串列、六個節點、刪除一個之後", UL_SIZE_MAIN, OUT['ul_size'])}
<h3>search：找到就停</h3>
<p>search 也從 head 開始走訪，每到一個節點就比對資料：相等就立刻回傳 true，不必再往後找；不相等才前進。走到 NULL 表示每個節點都比過了，回傳 false。</p>
{widget("uSearch", [("hit", "search(17)"), ("miss", "search(45)")], "選一個情況，再按 ▶ 播放或 → 單步。", codes=[("講義 04 · search", UL_SEARCH)], legend=("hl", "cmp", "found"))}
<p>講義以 myList.search(17) 為例：17 在串列中，走訪到它所在的節點就停下，search(17) 回傳 true。</p>
{figure('search')}
<p>若一路走到串列結尾都沒遇到，就表示要找的元素不在串列中；反過來，一旦找到就不必繼續往後走。所以找得越前面，比較次數越少；找不到時，每個節點都要比較一次。</p>
{lecture_program("完整程式：search 找到與找不到", "search(17)、search(54)、search(45)", UL_SEARCH_MAIN, OUT['ul_search'], note="17 在第四個節點，比較四次就回傳 true；54 是第一個節點，比較一次就找到；45 不在串列中，要比較完六個節點、走到 NULL 才回傳 false。")}
<h3>remove：previous 跟在 current 後面</h3>
<p>remove 分兩步：先像 search 一樣找到第一個相等的節點，再把它從鏈結中移除並 delete。找到時 current 指向要刪的節點，但要修改的是<strong>前一個節點的 next</strong>；單向串列無法往回走，current 停下時已經越過了要修改的位置。</p>
<p>解決辦法是走訪時同時用兩個外部指標：current 和之前一樣標出目前走到哪裡；新的 previous 一直落後 current 一個節點。這樣 current 停在要刪的節點時，previous 正好指向要修改的那個節點。前進時必須先執行 previous = current，再移動 current。開始時 previous 是 NULL，因為 current 指向的第一個節點前面沒有節點。</p>
{figure('remove-steps')}
{steps("逐步圖：remove 開始時的 previous 與 current", ['remove-start'])}
{widget("uRemove", [("mid", "刪中間 17"), ("head", "刪頭端 54"), ("tail", "刪尾端 31"), ("only", "唯一節點 7"), ("miss", "找不到 45")],
        "選一個情況，再按 ▶ 播放或 → 單步。", codes=[("講義 04 · remove", UL_REMOVE)], legend=("cmp", "hl", "found", "new", "del"))}
<p>有一個特殊情況要處理：要刪的正好是第一個節點時，current 指向第一個節點，previous 仍是 NULL。這時沒有「前一個節點」可以修改，要改的是串列的 head。</p>
{figure('remove-head')}
<p>第 16 行檢查這個情況：previous 沒有移動過，迴圈結束時仍是 NULL，就讓 head 改指 current 的下一個節點（第 17 行），等於把第一個節點從串列中移除；否則要刪的節點在串列中段或尾端，previous 就是 next 需要修改的節點（第 19 行）。兩種情況的新目標都是 current-&gt;getNext()。節點脫離鏈結後，第 21 行 delete current 釋放它；C++ 沒有垃圾回收，少了這一行就會留下無法再釋放的記憶體。串列的解構子也用同樣方式釋放剩下的所有節點。另一種做法是在最前面放一個不存資料的 header 節點，讓第一個資料節點也有前一個節點，就不需要這個特殊情況；這留作練習。</p>
{figure('remove')}
{lecture_program("完整程式：刪除中間的 17", "remove(17) 前後的串列", UL_REMOVE_MID, OUT['ul_remove_mid'], note="17 被跳過後，93 直接接到 77，串列剩 5 個節點，再搜尋 17 得到 false。")}
<div class="info-box"><span class="info-label">ADT 的假設與實作的行為</span><p>ADT 說明假設串列沒有重複元素。課程標頭的實作其實接受重複值：add 不檢查，remove 只刪第一個相等的節點。課本的 remove 假設要刪的項目一定在串列中；講義與課程標頭則在找不到時不做任何修改。</p></div>
{trace}
<p>各種情況下，remove 要更新哪個指標，整理如下：</p>
{edges}
<div class="info-box warm"><span class="info-label">想一想（課本）</span><p>① 要刪的是最後一個節點時，上面兩種情況夠用嗎？② 串列只有一個節點，而且正是要刪的節點時呢？先自己推演，再展開答案。</p>
{details("參考答案", "<p>① 刪最後一個節點時，previous 指向倒數第二個節點，current-&gt;getNext() 是 NULL，於是 previous-&gt;setNext(NULL)，previous 成為新的最後一個節點，不需要另外處理。② 只有一個節點時，迴圈第一次比對就命中，previous 仍是 NULL，執行 head = current-&gt;getNext()，head 變成 NULL，串列成為空串列。上面的動畫可以選「刪尾端 31」與「唯一節點 7」對照。</p>")}</div>
{lecture_program("完整程式：刪頭端、刪尾端、找不到與唯一節點", "remove 的特殊情況", UL_REMOVE_HEAD, OUT['ul_remove_head'], note="刪 54 時 previous 是 NULL，改的是 head，新的第一項是 26。刪 31 時 previous 停在 77，77 的 next 變成 NULL。remove(45) 找不到，串列不變。唯一的節點被刪掉後，head 變成 NULL，串列又是空的。")}
{lecture_program("講義完整程式：UnorderedList 的 add、size、search、remove", "講義 04 · UnorderedList 全套操作", UL_MAIN, OUT['ul'], note="第一行可以看出 add 採用頭插：最後加入的 54 排在最前面。三次 remove 分別刪除頭端、中間與尾端的節點。")}
{fold("<code>cout &lt;&lt; myList</code> 如何印出串列", snippet("課程標頭 · operator&lt;&lt;", UL_PRINT, note="範例中的 <code>cout &lt;&lt; myList</code> 使用標頭裡的 operator&lt;&lt;：它同樣從 head 走訪，每個值後面接一個空格，所以輸出的行尾有一個空格。"))}
{fold("空串列、重複值與頭尾刪除的完整程式", snippet("邊界情況", EDGES, OUT['edges']))}
{fold("所有權與深層複製", ownership)}'''


def ordered_section():
    q_ana = quiz('qAna', 'QUIZ · 平均走一半，為什麼還是 $O(n)$？',
                 '假設搜尋成功，而且每個位置被找到的機會相同，平均約檢查 n/2 個節點。為什麼仍寫成 $O(n)$？', [
                     (True, '係數在 Big-O 裡沒有意義，且最壞情況要走完全程',
                      '平均比較次數隨 n 線性成長，常數係數不改變 O(n)。最壞情況也要走到底，例如搜尋比所有元素都大的值。'),
                     (False, '因為 n/2 四捨五入之後就是 n',
                      'Big-O 不是四捨五入，而是把成長率相同的函數視為同一類。'),
                     (False, '平均情況根本不能分析',
                      '平均情況可以分析；只是它和最壞情況同樣是線性成長，結論不變。'),
                     (False, '因為串列的節點不連續，平均情況要乘上 2',
                      '節點是否連續影響的是實際執行時的快取表現，不會改變比較次數的成長率。'),
                 ])
    q_ord = quiz('qOrd', 'QUIZ · 有序串列的 search',
                 '元素不在串列中時，OrderedList 的 search(item) 比 UnorderedList 的版本多了什麼優勢？', [
                     (False, '可以用二分搜尋，在對數時間內找到',
                      '二分搜尋要能直接跳到中間的元素；串列只能從 head 沿 next 一步步走，做不到。'),
                     (True, '遇到比目標大的值就能提早停止',
                      '串列遞增，看到比 item 大的值時，後面只會更大，item 不可能出現，可以直接回傳 false。'),
                     (False, '可以跳回 head 更快地重新掃描',
                      '單向串列不能往回走，而且重新掃描只會更慢。'),
                     (False, '每個節點都存有索引，可以直接存取',
                      'Node 只有 data 與 next，沒有索引；依位置找節點仍然要走訪。'),
                 ])
    q_cx = quiz('qCx', 'QUIZ · 哪個操作是 $O(1)$？',
                '下列 UnorderedList 的成員函式中，哪一個在平均與最壞情況下都是 $O(1)$？', [
                    (False, 'size()', '這份實作沒有另存元素個數，size() 要走訪整條串列，是 O(n)。'),
                    (True, 'isEmpty()', 'isEmpty() 只檢查 head 是否為 NULL，不論串列多長都只做一次比較。'),
                    (False, 'search(item)', '最壞情況要比較每個節點；平均也約要比較一半的節點，仍是 O(n)。'),
                    (False, 'remove(item)', 'remove 要先走訪找到節點，最壞情況要走完整條串列，是 O(n)；只有接線本身是 O(1)。'),
                ])
    book = details('課本的 add：previous 與 current 兩個指標（課本寫法）', snippet('課本 · OrderedList::add', OL_ADD_BOOK) +
                   '<p>課本用 previous 與 current 兩個指標：current 遇到大於 item 的值才停止，新節點插在 previous 與 current 之間；previous 仍是 nullptr 時，新節點放在最前面。因為遇到相等的值不會停，重複值會排在原有相等值的後面，這點和講義版相反。兩種寫法都能維持遞增順序。</p>')
    return f'''<p>有序串列（Ordered List）中，每個元素的相對位置由元素本身的某種特性決定，通常是遞增或遞減；這裡假設元素之間已有明確的比較運算。前面的整數若改成遞增的有序串列，就是 17、26、31、54、77、93：17 最小，排在第一個位置；93 最大，排在最後。</p>
<p>有序串列的許多操作與無序串列相同：</p>
<ul class="linked-ul">
<li>OrderedList() 建立空的有序串列。</li>
<li>add(item) 加入新元素，並維持排序。</li>
<li>remove(item) 移除第一個相等的元素；找不到時串列不變。</li>
<li>search(item) 回傳元素是否存在；越過目標應在的位置後就可以停止。</li>
<li>isEmpty() 檢查 head 是否為 NULL；size() 以走訪計算節點數。</li>
</ul>
<p>較完整的有序串列 ADT 還有 index、pop 等依位置的操作，課程標頭的 OrderedList 沒有提供。實作方式與無序串列相同：空串列仍以 head == NULL 表示，isEmpty() 與 size() 的寫法不變。search、add、remove 則可以利用排序。</p>
<p>前面的遞增串列 17、26、31、54、77、93 可以用下面的鏈結結構表示。節點與連結同樣適合表示元素的相對位置：</p>
{figure('ordered')}
<p>實作 OrderedList 的方法和無序串列相同，空串列一樣以 head 指向 NULL 表示：</p>
{snippet("講義 04 · OrderedList 的資料成員與建構子", OL_SKELETON)}
<h3>search：越過目標就停止</h3>
<p>無序串列的 search 要逐一走訪節點，直到找到目標或走到 NULL。有序串列沿用同一個方法也完全正確：目標在串列中時，做法不需要任何修改。差別在目標不在串列中的時候，<strong>可以利用排序盡早停下</strong>。</p>
<p>以搜尋 45 為例：從 head 開始，先比 17，不是要找的值，前進到 26；仍然不是，再前進到 31、54。到 54 時情況不同了：照原本的策略要繼續往後，但串列是遞增的，54 已經比 45 大，後面的 77、93 只會更大，45 不可能出現在更後面，可以直接回傳 false。</p>
{figure('ordered-search')}
<p>只要在迴圈中多加一個判斷（第 6 行）：節點的值大於目標時立刻回傳 false。走訪只在節點的值小於目標時才繼續。</p>
{widget("oSearch", [("stop", "search(45)"), ("hit", "search(31)"), ("miss", "search(100)")],
        "選一個情況，再按 ▶ 播放或 → 單步。", codes=[("講義 04 · OrderedList::search", OL_SEARCH)], legend=("hl", "cmp", "found", "skip"))}
{lecture_program("完整程式：有序串列的 search", "search(45)、search(31)、search(10)、search(100)", OL_SEARCH_MAIN, OUT['ol_search'], note="四個呼叫的比較次數不同：search(45) 比到 54 就停（4 次）；search(31) 在第 3 個節點找到；search(10) 第一次比較就看到 17 &gt; 10，立刻停止；search(100) 比所有值都大，要走完全部 6 個節點才回傳 false。")}
<h3>add：先找到位置再接上</h3>
<p>改動最大的是 add。無序串列的 add 可以直接把新節點放在 head，因為那裡最容易存取；有序串列不能這樣做，必須先找出新元素在現有排序中的位置。例如在 17、26、54、77、93 中加入 31，add 要判斷出新節點屬於 26 與 54 之間：</p>
{figure('ordered-add')}
<p>和無序串列的 remove 一樣，光靠停在 54 的指標無法修改 26 的 next，所以需要知道插入點<strong>前一個</strong>節點。圖中用 previous 與 current 兩個指標標出這個位置；講義的程式則只用一個 current，改成每次先看下一個節點。</p>
<p>講義的 add 只用一個 current，並且每次<strong>先看下一個節點</strong>：若串列是空的，或 head 的值已經大於或等於 item，新節點直接放在最前面；否則 current 從 head 出發，只要 current-&gt;getNext() 不是 NULL，而且它的值小於 item，就前進一步。停下時，新節點要接在 current 後面：先 newNode-&gt;setNext(current-&gt;getNext())，再 current-&gt;setNext(newNode)。和相等的值比較時不會前進，所以重複值會插在原有相等值的前面。</p>
{widget("oAdd", [("mid", "add(31)"), ("head", "add(10)：插在最前"), ("tail", "add(100)：插在最後"), ("empty", "空串列 add(31)")],
        "選一個情況，再按 ▶ 播放或 → 單步。", codes=[("講義 04 · OrderedList::add", OL_ADD)], legend=("hl", "cmp", "new"))}
{book}
{lecture_program("完整程式：有序串列的 add", "add(31)、add(10)、add(100)", OL_ADD_MAIN, OUT['ol_add'], note="不論加入順序為何，印出來永遠由小到大。31 插在 26 與 54 之間；10 比 head 的 17 小，成為新的 head；100 比所有值大，current 一路走到最後一個節點 93，新節點接在它後面。")}
<h3>remove：利用排序提早放棄</h3>
<p>有序版的 remove 在 current 的值小於 item 時前進。迴圈停下後，若 current 是 NULL，或它的值不等於 item，就表示 item 不在串列中，直接 return；找到時的接線與 delete 和無序串列相同。</p>
{widget("oRemove", [("mid", "remove(54)"), ("head", "remove(17)"), ("miss", "remove(45)")],
        "選一個情況，再按 ▶ 播放或 → 單步。", codes=[("講義 04 · OrderedList::remove", OL_REMOVE)], legend=("hl", "cmp", "found", "new", "del", "skip"))}
{lecture_program("完整程式：有序串列的 remove", "remove(54)、remove(17)、remove(45)", OL_REMOVE_MAIN, OUT['ol_remove'], note="remove(54) 在 54 停下並找到它，31 改接 77。remove(17) 刪的是第一個節點，previous 仍是 NULL，改的是 head。remove(45) 走到 77 時已經比 45 大，迴圈停下，77 不等於 45，直接 return，串列不變。")}
{lecture_program("講義完整程式：OrderedList", "講義 04 · OrderedList", OL_MAIN, OUT['ol'], note="同樣加入六個值，輸出卻由小到大排列，差別全在 add 內部先找位置再插入。remove(100) 找不到目標，串列不變。")}
{q_ord}
<h3>分析：哪些操作需要走訪（cppds §4.6.1）</h3>
<p>判斷方式是看操作是否需要走訪。isEmpty() 只看 head，是 $O(1)$；size() 沒有另存個數，必須數完 n 個節點，是 $O(n)$。無序串列的 add 在 head 插入，是 $O(1)$；search、remove，以及有序串列的 add 都可能走完整條串列，最壞情況是 $O(n)$。有序搜尋可以提早停止，但最壞情況仍是 $O(n)$。已經握有前驅的指標時，插入或刪除一個節點只要 $O(1)$；找到那個位置則可能需要 $O(n)$。</p>
<p>若搜尋成功，而且每個位置被找到的機會相同，平均約檢查 n/2 個節點，平均成本仍是 $O(n)$。</p>
{q_cx}
{fold("平均要比較幾次？", "<p>成功搜尋 n 個位置的比較次數依序為 1、2、…、n。若每個位置等可能，平均為 (1 + 2 + … + n) / n = (n + 1) / 2，約為 n/2；因此隨 n 線性成長。</p>", did="linked-average-detail")}
<p>鏈結串列與連續陣列的取捨正好相反：串列在前端插入是 $O(1)$、依位置存取是 $O(n)$；陣列依位置存取是 $O(1)$、在前端插入則要搬移元素。哪一種較合適，取決於程式最常做哪些操作。各操作的完整比較見<a href="#reference">操作成本總覽</a>。</p>
{q_ana}
{fold("有序串列能不能做二分搜尋？", "<p>二分搜尋每一步都要直接取得中間的元素。陣列可以用索引一次算出中點；鏈結串列沒有這種索引，要找到中間節點就得從 head 走過去。因此有序串列不能直接套用陣列二分搜尋的 $O(\\log n)$ 成本。</p>")}
{fold("元素的比較、複製與解構成本", "<p>上面的分析把單一元素的比較、複製與解構視為 $O(1)$，只計算走訪多少個節點、更新多少次指標。若節點存放的物件需要較多時間才能比較、複製或解構，還要把這些成本加進去。</p>")}'''


def stl_section():
    q_stl = quiz('qStl', 'QUIZ · 為什麼叫 insert_after？',
                 'forward_list 只提供 insert_after，不提供 insert（插在某個節點前面）。原因是？', [
                     (True, '單向串列不能直接找到前驅；提供前驅才能 $O(1)$ 接線',
                      '要插在 it 前面，必須修改前驅的 next。單向串列不能反向找前驅；從頭找需要 O(n)，提供前驅後接線才是 O(1)。'),
                     (False, '歷史因素，沒有技術上的原因',
                      '介面反映了資料結構的限制：已知前驅才能在常數時間內接線。std::list 有 prev 指標，可以由 pos 找到前驅，所以提供 insert。'),
                     (False, 'insert_after 比較快',
                      '若從頭找前驅，仍然可以插在某個節點之前，但需要 O(n)；insert_after 要求呼叫者直接提供前驅。'),
                     (False, 'forward_list 的元素不能重複，所以只能插在後面',
                      'forward_list 可以存放重複的值；介面只和「單向串列找不到前驅」有關。'),
                 ])
    compare = '''<div style="overflow-x:auto;">
  <table class="cmp-table" style="width:100%;font-size:.88rem;">
    <thead><tr><th></th><th>vector</th><th>forward_list（單向）</th><th>list（雙向）</th></tr></thead>
    <tbody>
      <tr><td>依索引存取 [i]</td><td>$O(1)$</td><td>不提供</td><td>不提供</td></tr>
      <tr><td>頭端插入</td><td>$O(n)$</td><td>$O(1)$ push_front</td><td>$O(1)$ push_front</td></tr>
      <tr><td>尾端插入</td><td>攤銷 $O(1)$</td><td>不提供 push_back</td><td>$O(1)$ push_back</td></tr>
      <tr><td>已知位置插入／刪除</td><td>$O(n)$</td><td>$O(1)$ insert_after／erase_after（給前驅）</td><td>$O(1)$ insert／erase</td></tr>
      <tr><td>每個元素的額外空間</td><td>預留容量</td><td>一個 next 指標</td><td>prev 與 next 兩個指標</td></tr>
      <tr><td>記憶體位置</td><td>連續，對快取友善</td><td colspan="2">節點分散在 heap 各處</td></tr>
    </tbody>
  </table>
</div>'''
    ops = table(['操作', '說明'], [
        ('forward_list&lt;T&gt; a;', '建立空的 forward_list'),
        ('push_front(x)／emplace_front(...)', '在最前面加入元素；emplace 版就地建構元素'),
        ('pop_front()', '移除第一個元素'),
        ('insert_after(it, x)／emplace_after(it, ...)', '在 it 指向的元素後面加入'),
        ('erase_after(it)', '刪除 it 後面的元素（也可以刪除一段範圍）'),
        ('clear()', '移除所有元素'),
    ])
    iter_note = '<p>begin() 指向第一項，end() 是尾後位置，不能解參考。list 的 insert(pos, x) 插在 pos 前面並回傳新元素的位置；erase(it) 回傳被刪元素的下一個位置，迴圈中刪除時要用這個回傳值繼續，不能對已刪除的 it 做 ++it。</p><p>forward_list 的 before_begin() 是「第一項前面」的位置，不能解參考，但可以傳給 insert_after／erase_after，讓頭端也用同一套寫法。刪除 current 時 previous 留在原地，current 接回 erase_after 的回傳值；保留 current 時兩者才一起前進，這正是前面 previous／current 的關係。forward_list 沒有 size()；std::distance(begin(), end()) 需要 $O(n)$。</p>'
    algos = '<p>兩種串列都有成員函式 remove(x)、unique()、sort()。remove(x) 刪掉<strong>所有</strong>等於 x 的元素，和本課 remove 只刪第一個不同；unique() 只合併<strong>相鄰</strong>的相等值；sort() 是穩定排序，約需 $O(n \\log n)$ 次比較。std::sort 需要隨機存取迭代器，不能用在這兩種串列上。插入不會使其他元素的迭代器失效；刪除只會使被刪元素的迭代器失效。</p>'
    return f'''<p>UnorderedList 與 OrderedList 讓你看清楚指標怎麼接、節點由誰釋放。實際寫程式時，優先使用 STL 容器：它們的解構、複製、迭代器與例外安全都已有明確規範並經過測試。</p>
<p>std::forward_list&lt;T&gt; 是單向串列，提供 push_front、insert_after、erase_after；std::list&lt;T&gt; 是雙向串列，可以用雙向迭代器在指定位置插入或刪除。兩者都不支援依索引的隨機存取。插入與刪除是 $O(1)$ 的前提是：手上已經有對應位置的迭代器。</p>
{snippet("講義 04 · forward_list 與 list", STL_MAIN, OUT['stl'], note="singly.insert_after(singly.before_begin(), 17) 插在「第一項之前的位置」後面，也就是成為新的第一項。next(doubly.begin()) 指向 31，doubly.insert(pos, 26) 把 26 插在 31 前面。")}
{compare}
<h3>forward_list 的常用操作（課本）</h3>
<p>forward_list 的插入與刪除都作用在指定元素的<strong>後面</strong>：insert_after、erase_after。課本列出的常用操作如下：</p>
{ops}
<div class="info-box warm" style="margin-top:.9rem;"><span class="info-label">選擇容器時的考量</span>需要依索引讀取，或大多是從頭到尾的循序掃描時，先考慮 vector：元素連續存放，對快取友善。經常在已知位置插入或刪除，而且手上已有該位置的迭代器時，再考慮 list 或 forward_list。</div>
{q_stl}
{fold("std::list 的頭尾增刪與迴圈中的刪除", snippet("雙向串列：插在位置之前，刪除後接回下一個位置", STL_LIST, OUT['list']) + iter_note)}
{fold("std::forward_list 與 before_begin()", snippet("單向串列：保留前驅才能安全刪除", STL_FORWARD, OUT['forward']))}
{fold("remove、unique、sort 成員函式", snippet("先分清楚「全部符合」與「相鄰重複」", STL_ALGOS, OUT['algos']) + algos)}'''


def variants_section():
    q_var = quiz('qVar', 'QUIZ · 尾端刪除', '要讓「刪除最後一個節點」變成 $O(1)$，需要哪種配置？', [
        (True, '雙向串列加上 tail 指標（或 trailer 哨兵）',
         'tail 直接找到最後一個節點，tail->prev 直接找到倒數第二個；兩個指標都不必走訪。'),
        (False, '單向串列加上 tail 指標',
         'tail 找得到最後一個節點，但刪除時要把倒數第二個節點的 next 改成 NULL；單向串列找不到它，仍要 O(n) 走訪。'),
        (False, '環狀單向串列',
         '環狀只改變結尾的接法；刪除最後一個節點一樣需要前一個節點，仍是 O(n)。'),
        (False, '單向串列另存元素個數',
         '知道有幾個元素，仍然要從 head 走 n−2 步才能找到倒數第二個節點，是 O(n)。'),
    ])
    return f'''<p>以下是講義在本章最後介紹的兩種延伸：環狀串列與雙向串列。兩者的節點與單向串列相同，都是資料加上指標；差別在指標怎麼連接：環狀串列讓結尾接回開頭，雙向串列讓每個節點同時記住前後兩個鄰居。</p>
<h3>環狀串列：回到起點才結束</h3>
<p>讓最後一個節點的 next 指回第一個節點，就得到<strong>環狀鏈結串列</strong>（Circularly Linked List）。下圖中 tail 指向最後一個節點 17，它的 next 不是 NULL，而是繞回 head 指向的 54：</p>
{figure('circular')}
<p>它適合描述沒有明確起點與終點的循環資料，例如列車沿環狀路線停靠的站點，或遊戲中玩家輪流的順序。環本身沒有頭尾，但程式仍要保存某個節點的指標，才能使用這個串列。</p>
<p>前進的寫法一樣是 current = current-&gt;getNext()；但串列中沒有 NULL，所以走訪改成判斷是否回到出發的節點。空串列要先排除；只有一個節點時，它的 next 指向自己。</p>
{widget("cTrav", [("four", "四個節點"), ("one", "單一節點"), ("empty", "空串列")],
        "選一個情況，再按 ▶ 播放或 → 單步。", codes=[("環狀走訪（補充）", CIRCULAR)], legend=("hl", "cmp"))}
<h3>環狀串列的用途：輪流與 append</h3>
<p>講義指出，環狀串列適合輪流分配資源，也方便實作 append 一類的操作：若保存最後一個節點 tail，tail-&gt;getNext() 就是第一個節點，在頭端或尾端加入都只要 $O(1)$。只保存 tail 就夠了，不必另外保存 head。</p>
<p>以輪流使用資源為例：current 指向目前輪到的工作，處理完一段時間後執行 current = current-&gt;getNext()，就換到下一個工作；走到最後一個工作之後，會自然回到第一個，不需要另外判斷「是否到尾端、要不要回到開頭」。</p>
<p>環狀只改變結尾的接法，並沒有增加反向走訪的能力：要刪除某個節點，仍然需要它前一個節點。另外，因為串列中沒有 NULL，任何以「走到 NULL 為止」寫成的迴圈，在環狀串列上都不會結束；釋放節點時，也要先把環斷開，或改用「回到起點為止」的條件。</p>
{fold("完整程式：建立環狀串列、走訪與用 tail 做 append", snippet("環狀串列：以 Node 建立、do-while 走訪", CIRC_MAIN, OUT['circ'], note="printCircular 用 do-while：先印出起點，再前進，回到起點時停止。第二行確認 tail-&gt;getNext() 就是 54。append(11) 只改兩個指標，11 成為新的 tail，並指回 54。最後一行從 93 開始走，也能走完一整圈。釋放前先把 tail 的 next 設成 NULL，就能用一般串列的方式逐一 delete。"))}
<h3>單向串列的限制</h3>
<p>單向串列可以有效率地在頭端插入與刪除，也能在保存 tail 時快速加到尾端，但<strong>刪除尾端</strong>不容易：必須先找到倒數第二個節點。問題其實更普遍：只拿到某個節點的指標時，找不到它的前驅，也就無法立刻刪除它。</p>
<h3>雙向串列與哨兵節點</h3>
<p>為了讓兩個方向對稱，<strong>雙向鏈結串列</strong>（Doubly Linked List）讓每個節點同時保存指向後一個節點的 next 與指向前一個節點的 prev，因此能在任意位置以 $O(1)$ 完成更多種更新；需要反向走訪的演算法（例如檢查回文）也適合使用。</p>
<p>講義的設計在兩端各放一個不存使用者資料的<strong>哨兵節點</strong>（sentinel）：header 與 trailer。非空串列中，header 的 next 指向第一個資料節點，trailer 的 prev 指向最後一個資料節點；空串列時兩者直接相連。這樣每次插入都發生在兩個既有節點之間，每個要刪除的資料節點兩側也一定有鄰居，所以頭端、尾端與中間都能用同一套接線。走訪時要在 trailer 停下，哨兵不能當成資料讀取或刪除。</p>
{figure('sentinels')}
<p>哨兵的代價是每個串列多兩個不存資料的節點，換來的是程式裡不再需要「是不是第一個節點」「是不是最後一個節點」這類特殊情況。對照單向串列的 remove：刪除第一個節點時 previous 是 NULL，必須改成修改 head；有了 header，第一個資料節點前面永遠有一個節點，特殊情況就消失了。</p>
<h3>插入：先接新節點，再改兩邊的鄰居</h3>
<p>每次插入都發生在兩個既有節點之間。例如把新元素放在最前面，就是把新節點放在 header 與目前 header 後面的節點之間。下圖把 77 插在 26 與 93 之間：pred 是左邊的鄰居，succ 是右邊的鄰居。</p>
{figure('d-ins')}
{steps("逐步圖：插入 77 的前後", ['d-ins-before', 'd-ins-after'])}
<p>四行的順序有講究：前兩行只設定新節點自己的 prev 與 next，這時兩個鄰居都還沒改，原本的串列完整無缺；後兩行才讓 pred 的 next 與 succ 的 prev 改指新節點。下面的動畫照這四行逐步執行：先設定 newNode 自己的 prev、next，再讓 pred、succ 改指 newNode，共四個指標：</p>
{widget("dIns", [("mid", "插在 54 與 93 之間"), ("front", "插在最前面"), ("empty", "空串列插入")],
        "選一個情況，再按 ▶ 播放或 → 單步。", codes=[("講義 04 · 插入四步", D_INSERT)], legend=("new", "sent"))}
{lecture_program("完整程式：雙向串列的插入", "以 header、trailer 哨兵建立雙向串列並插入", DLL_INSERT, OUT['dll_insert'], note="每一行先由 header 往後印，直線後再由 trailer 往前印；兩個方向的結果正好相反，表示 next 與 prev 都接對了。第一行只有直線，表示空串列：header 與 trailer 直接相連。插在最前面時，pred 就是 header，不需要特別處理。")}
<h3>刪除：讓兩個鄰居直接相連</h3>
<p>刪除的步驟與插入相反：讓要刪除節點的兩個鄰居直接互相連接、跳過它。只要改兩個鏈結，這個節點就不再屬於串列，接著釋放它。因為有哨兵，刪除第一項或最後一項時，要刪的節點兩側也一定有鄰居，可以用同一段程式。已知節點時刪除是 $O(1)$，但依值尋找它仍要 $O(n)$。</p>
{figure('d-del')}
{steps("逐步圖：刪除 77 的前後", ['d-del-before', 'd-del-after'])}
{widget("dErase", [("mid", "刪除中間的 26"), ("first", "刪除第一項 54"), ("only", "刪除唯一的資料節點")],
        "選一個情況，再按 ▶ 播放或 → 單步。", codes=[("講義 04 · 刪除", D_ERASE)], legend=("found", "new", "del", "sent"))}
{lecture_program("完整程式：雙向串列的刪除", "刪除中間、第一項與最後一項", DLL_ERASE, OUT['dll_erase'], note="三次 erase 用的是同一個函式：刪 77 時兩側是 26 與 93；刪第一項 54 時左鄰居是 header；刪最後一項 93 時右鄰居是 trailer。每一行兩個方向的結果都互為反序。")}
{q_var}'''


def exercises_section():
    ex1 = quiz('ex1', 'EXERCISE 1 · 走訪計數', '一條長度 n 的單向串列，size()（用走訪實作）與「取第 k 個元素」的成本分別是？', [
        (True, '$O(n)$ 與 $O(k)$', '兩者都得從 head 一步步走；這是串列與陣列最根本的差別。'),
        (False, '$O(1)$ 與 $O(1)$', '除非另外維護元素個數，否則 size 必須走訪；取第 k 個元素也要從 head 走 k 步。'),
        (False, '$O(n)$ 與 $O(\\log k)$', '依位置取值要從 head 沿 next 走到該位置；串列沒有可以直接跳到中間的索引。'),
        (False, '$O(1)$ 與 $O(k)$', '這份 size() 沒有另存個數，要逐一數過 n 個節點，所以是 O(n)。'),
    ])
    ex2 = quiz('ex2', 'EXERCISE 2 · remove 邊界', 'remove(item) 用 previous／current 兩個指標。要刪的是 <strong>head 指向的節點</strong>時，正確動作是？', [
        (True, 'head = current-&gt;getNext()（此時 previous 是 NULL）', 'previous == NULL 代表 current 就是第一個節點，這時要直接修改 head。'),
        (False, 'previous-&gt;setNext(current-&gt;getNext())', 'previous 是 NULL，透過它存取節點是未定義行為。'),
        (False, '先把串列反轉再刪', '不需要；用 previous == NULL 判斷，直接修改 head 就能處理。'),
        (False, '只要 delete current，不必修改任何指標', 'head 仍指向被釋放的節點，之後透過 head 存取就是未定義行為。必須先讓 head 改指下一個節點，再釋放。'),
    ])
    ex3 = quiz('ex3', 'EXERCISE 3 · 記憶體', 'remove 把節點從鏈結中移除後，若少了 delete current，會發生什麼事？', [
        (True, '記憶體洩漏：那個節點再也無法釋放', '節點脫離鏈結後，只剩 current 知道它的位址；函式結束後連 current 也消失，這塊記憶體就無法再釋放。STL 容器會自動管理節點的生命週期。'),
        (False, '編譯錯誤', '少寫 delete 不影響編譯，問題要到執行時才會累積出來。'),
        (False, '什麼都不會發生', '每次 remove 都會留下一個無法釋放的節點；程式執行越久，累積的記憶體越多。'),
        (False, '節點會自動回到串列中', '前驅的 next 已經跳過它，沒有任何鏈結再指向這個節點；它不在串列中，只是記憶體沒有被釋放。'),
    ])
    ex4 = quiz('ex4', '練習 · append 的成本', '上面的 append() 是 $O(n)$。要讓它變成 $O(1)$，正確的做法是？', [
        (True, '類別另存一個 tail 指標，append 直接接在 tail 後面',
         'tail 直接找到最後一個節點：接上新節點後，再讓 tail 指向它。代價是 add、remove 都要一併維護 tail，尤其是刪到最後一個節點時。'),
        (False, '把串列改成從尾端往頭端指',
         '這只是把問題反過來：append 變快了，原本 O(1) 的頭端 add 就變成 O(n)。'),
        (False, '先把串列反轉、插入、再反轉回來', '兩次反轉各需 O(n)，比原本更慢。'),
        (False, '另存元素個數 size', '知道有幾個節點，仍然要從 head 走到最後一個節點才能接上，還是 O(n)。'),
    ])
    book = '''<div class="deck-extra" id="dx-exx">
  <div class="dx-label">課本 Programming Exercises 精選（課本）</div>
  <ol style="font-size:.92rem;line-height:1.9;padding-left:1.4rem;">
    <li><strong>size 的 $O(1)$ 版</strong>：把節點數存成資料成員，改寫 add、remove 與 size，讓 size() 變成 $O(1)$。</li>
    <li><strong>remove 找不到時</strong>：確認 remove 在項目不存在時也能正確運作，並替空串列、找不到、刪頭端、刪尾端各寫一個測試。</li>
    <li><strong>補完 ADT</strong>：實作 append、index、pop、insert，並分析各自的 Big-O。</li>
    <li><strong>slice(start, stop)</strong>：回傳從 start 到 stop（不含）的新串列。</li>
    <li><strong>用繼承減少重複</strong>：OrderedList 與 UnorderedList 有許多相同的方法。設計繼承階層，讓共同的部分只寫一次。</li>
    <li><strong>用串列實作 Stack、Queue、Deque</strong>：各實作一次，並與連續陣列的實作比較效能。哪些操作變快、哪些變慢？</li>
  </ol>
  <p class="dx-note">題目改寫自課本第 4 章 Programming Exercises 的第 4、5、9、10、12 題，以及第 13 至 15 題與第 17 題；完整題目見 <a href="https://runestone.academy/ns/books/published/cppds/LinearLinked/ProgrammingExercises.html" target="_blank" rel="noopener">cppds Programming Exercises</a>。</p>
</div>'''
    return f'''{ex1}
{ex2}
{ex3}
<h3>練習：實作 append()</h3>
<p>替 UnorderedList 加上 append(item)，把新元素接在<strong>尾端</strong>，使它成為最後一項。先自己寫寫看，再思考：你的方法時間複雜度是多少？</p>
{details("參考解答（講義）", snippet("講義 04 · append 的一種寫法", APPEND, note="這個寫法要走到最後一個節點，所以是 $O(n)$；若類別另存 tail 指標，可以做到 $O(1)$。") + "<p>UnorderedList 的 head 是 private，無法在類別外替它加成員函式。下面的 MyList 只保留 add 與 append，用來試跑這個寫法：</p>" + snippet("試用 append：MyList", APPEND_MAIN, OUT['append'], note="append(31) 時串列是空的，新節點直接成為 head；add(77) 放到最前面；append(17) 從 77 走到 31，再接在 31 後面。"))}
{ex4}
<h3>練習：加入 header 節點</h3>
<p>講義提到，可以在串列最前面放一個不存資料的 header 節點來簡化 remove。改寫 UnorderedList，讓 head 永遠指向這個 header：remove 還需要「previous == NULL」的特殊情況嗎？add、size、search 與 isEmpty 要怎麼跟著調整？</p>
{book}'''


def reference_section():
    rows = table(['操作', 'vector／連續陣列', 'UnorderedList', 'OrderedList', '成本從哪裡來'], [
        ('isEmpty()', '$O(1)$', '$O(1)$', '$O(1)$', '只檢查一個值（陣列看 size，串列看 head）'),
        ('size()', '$O(1)$', '$O(n)$', '$O(n)$', '本課的串列沒有另存個數，要逐一計數'),
        ('讀零起始的第 k 項', '$O(1)$', '$O(k+1)$', '$O(k+1)$', '陣列用位址公式；串列要從 head 走 k 步'),
        ('add(item)', '尾端攤銷 $O(1)$；頭插 $O(n)$', '$O(1)$', '最壞 $O(n)$', '無序版插在 head；有序版要先找位置'),
        ('search(item)', '$O(n)$；已排序可二分 $O(\\log n)$', '$O(n)$', '$O(n)$，可提早停止', '串列只能依序走訪'),
        ('remove(item)', '$O(n)$', '最壞 $O(n)$', '最壞 $O(n)$', '先找到節點；接線本身是 $O(1)$'),
        ('已知前驅時插入或刪除一個節點', '$O(n)$（要搬移）', '$O(1)$', '$O(1)$', '只改固定幾個指標（有序串列另須維持排序）'),
        ('append(item)（練習）', '攤銷 $O(1)$', '$O(n)$；另存 tail 可 $O(1)$', '不適用', '要先走到最後一個節點'),
    ])
    return f'''<p>下表整理本章各操作的成本；最右欄說明成本從哪裡來。</p>
{rows}
<h3>從表格看取捨</h3>
<p>同一列由左往右讀，可以看出兩種表示法互補：陣列的優勢在依位置讀取與尾端加入，串列的優勢在頭端或已知位置的插入與刪除。兩者的 search 都要逐一比較；陣列排序後可以二分搜尋，有序串列只能提早停止。選擇資料結構時，先列出程式最常執行的操作，再用這張表比較它們的成本。</p>'''


def recap_section():
    qa = [
        ('為什麼 Node 的 data 與 next 要設成 private？',
         '<p>把欄位藏起來，所有修改都得經過 setData 與 setNext，類別就能控制節點怎麼被使用；串列類別也能確保自己擁有的節點只由它負責接線與釋放。代價是程式要多寫一層函式呼叫，例如 current-&gt;getNext() 而不是 current-&gt;next。STL 的容器更進一步，完全不讓使用者碰到節點，只提供迭代器。</p>'),
        ('環狀串列的走訪為什麼要用 do-while？',
         '<p>環狀串列沒有 NULL，結束條件是「回到起點」。若寫成 while (current != head)，第一次檢查時 current 就等於 head，迴圈一次也不執行。do-while 先處理起點、前進之後才檢查，正好走完一圈。空串列要在進入迴圈前另外排除，否則會解參考 NULL。</p>'),
        ('delete 之後要不要把指標設成 NULL？',
         '<p>delete 釋放的是指標所指的節點，指標變數本身仍保存舊位址，成為失效指標。若這個指標之後還會用到（例如類別的成員），把它設成 NULL，之後的 NULL 檢查才有作用；若它是即將結束的區域變數（例如 remove 裡的 current），設不設都不影響結果。重點是 delete 之後不能再透過它讀寫。另外，其他指向同一節點的指標並不會因此變成 NULL。</p>'),
        ('「插入、刪除 $O(1)$」和「要先找到位置 $O(n)$」怎麼合起來看？',
         '<p>$O(1)$ 指的是已經握有位置（單向串列還要有前驅）之後，修改指標的成本。若位置要靠比對值或從 head 數過去才能找到，尋找就要 $O(n)$，整個操作也是 $O(n)$。鏈結串列的優勢出現在位置本來就已知的情況，例如一直在 head 操作，或在走訪的同時順便插入、刪除。</p>'),
        ('什麼時候適合用 list 或 forward_list？',
         '<p>需要在已知位置頻繁插入、刪除，而且手上已有迭代器時。list 是雙向的，給一個迭代器就能在它前面插入，或刪除它本身；forward_list 只能往後走，操作時要提供前驅的位置（insert_after、erase_after），但每個節點少存一個指標。若主要是依索引讀取或循序掃描，vector 通常較合適。</p>'),
        ('陣列和串列的快取表現為什麼不同？',
         '<p>CPU 讀取記憶體時，會把相鄰的一小段資料一起載入快取（cache）。陣列元素連續存放，讀 a[i] 時，a[i+1]、a[i+2] 多半也已經在快取裡；串列的節點分散在 heap 各處，每走一步都可能讀到不在快取中的位置。因此即使兩者的走訪都是 $O(n)$，實際執行時陣列常常快得多。</p>'),
    ]
    faq = ''.join(details(f'{q}（補充）', a, cls='linked-detail linked-faq') for q, a in qa)
    return f'''<ul class="linked-ul linked-recap">
<li>串列 ADT 只要求元素有相對位置；無序串列的順序與元素值無關，有序串列的順序由元素值決定。</li>
<li>鏈結串列用 next 指標維持元素的相對順序，元素不必連續存放；head 是唯一的入口，串列物件本身只保存 head，不包含節點。</li>
<li>Node 存放 data 與 next 兩個 private 欄位，只能透過 getData、getNext、setData、setNext 存取；建構子把 next 設成 NULL，NULL 表示後面沒有節點。</li>
<li>插入時先接好新節點的 next，再修改 head 或前驅的 next，後段才不會遺失。</li>
<li>size、search、remove 都靠走訪；remove 讓 previous 跟在 current 後面，找到後改前驅的 next（或 head），再 delete 節點。</li>
<li>有序串列的 search 可以在越過目標時停止；add 用 current 先看下一個節點，找到位置後先接後段、再接前段。</li>
<li>isEmpty() 與無序串列的 add 是 $O(1)$；size、search、remove 與有序串列的 add 最壞都是 $O(n)$。已知前驅時接線只要 $O(1)$，找到位置才是主要成本。</li>
<li>環狀串列以回到起點作為走訪的結束；雙向串列配合 header、trailer 哨兵，任何位置的插入與刪除都用同一套接線。</li>
<li>實際寫程式時優先使用 std::list 或 std::forward_list；之後學遞迴時，也可以把串列看成「一個節點，加上剩下的串列」。</li>
</ul>
<h3>常見疑問</h3>
{faq}'''


def sections():
    return {
        'linked-prologue': prologue(),
        'linked-node': node_section(),
        'linked-unordered': unordered_section(),
        'linked-ordered': ordered_section(),
        'linked-stl': stl_section(),
        'linked-variants': variants_section(),
        'linked-exercises': exercises_section(),
        'linked-reference': reference_section(),
        'linked-recap': recap_section(),
    }


STYLE = """<style id="linked-depth-style">
.linked-detail{margin:1rem 0;border:1px solid var(--card-border);border-radius:8px;background:var(--card);}
.linked-detail>summary{cursor:pointer;padding:.9rem 1rem;font-weight:600;line-height:1.6;}
.linked-detail-body{padding:0 1rem 1rem;min-width:0;}
.linked-detail-body .pseudo-code{max-width:100%;overflow-x:auto;}
.linked-detail-body .cmp-table{min-width:500px;}
.info-box .linked-detail{background:var(--card);}
.ll-canvas{min-height:110px;min-width:0;}
.ll-scroll{overflow-x:auto;}
.ll-canvas svg{display:block;margin:0 auto;}
.ll-vars{display:flex;flex-wrap:wrap;gap:.2rem 1.1rem;font-size:.82rem;line-height:1.7;margin:.35rem 0 .1rem;color:var(--ink);}
.ll-legend{display:flex;flex-wrap:wrap;gap:.2rem .9rem;font-size:.78rem;color:var(--ink);margin-top:.4rem;}
.ll-sw{display:inline-block;width:.95em;height:.95em;border:2px solid;border-radius:3px;vertical-align:-.12em;margin-right:.3em;}
.ll-case{background:var(--card);color:var(--accent2);border:1px solid var(--card-border);}
.ll-case.on{background:#e8eefc;border-color:var(--accent2);box-shadow:inset 0 0 0 1px var(--accent2);}
.ll-count{font-family:'JetBrains Mono',monospace;font-size:.78rem;color:var(--ink);margin-left:auto;}
.ll-widget .info-card[hidden]{display:none;}
.viz-layout.ll-widget{grid-template-columns:minmax(0,1fr) 400px;}
@media(max-width:900px){.viz-layout.ll-widget{grid-template-columns:1fr;}}
.ll-widget .ic-title{text-transform:none;letter-spacing:.04em;}
.linked-ul{padding-left:1.4rem;margin-bottom:1rem;}
.linked-ul li{margin:.25rem 0;}
.quiz-opt .opt-text{min-width:0;overflow-wrap:anywhere;}
</style>"""
