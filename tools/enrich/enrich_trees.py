#!/usr/bin/env python3
"""trees.html 完整自學充實。冪等。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib import card, ensure_style, insert_end_of_section

PAGE = Path.home() / "ds-cpp-selfstudy/trees.html"
s = PAGE.read_text()
s = ensure_style(s)

voc = f'''<h3 id="dx-voc">講義完整範例：BinaryTree 與解析樹的使用畫面</h3>
{card("講義 09 · BinaryTree 基本操作", """#include <iostream>
#include "binarytree.hpp"   // 本節的完整類別
using namespace std;

int main() {{
    BinaryTree aTree("a");
    cout << aTree.getRootVal() << endl;
    cout << aTree.getLeftChild() << endl;      // NULL 印出來是 0
    aTree.insertLeft("b");
    cout << aTree.getLeftChild()->getRootVal() << endl;
    aTree.insertRight("c");
    cout << aTree.getRightChild()->getRootVal() << endl;
    aTree.getRightChild()->setRootVal("hello");
    cout << aTree.getRightChild()->getRootVal() << endl;
    return 0;
}}""".replace("{{","{").replace("}}","}"),
"a\\n0\\nb\\nc\\nhello",
note="getLeftChild() 回傳的是<strong>整棵左子樹</strong>（BinaryTree*），不只是值：所以能一路 -&gt; 下去操作任何深度的節點。insertLeft 若遇到既有左子樹，會把它「往下推」成新節點的左子樹。")}
{card("講義 09 · 解析樹：建樹、求值、還原", """#include <iostream>
#include "binarytree.hpp"   // buildParseTree + evaluate + printExp
using namespace std;

int main() {{
    BinaryTree* pt = buildParseTree("( 3 + ( 4 * 5 ) )");
    inorder(pt);                      // 中序走訪：印回運算式的骨架
    cout << endl;
    cout << evaluate(pt) << endl;     // 後序邏輯：先算子樹再套運算子
    cout << printExp(pt) << endl;     // 中序＋括號還原
    return 0;
}}""".replace("{{","{").replace("}}","}"),
"3 + 4 * 5 \\n23\\n((3)+((4)*(5)))",
note="三個函式就是三種走訪的應用：inorder 印骨架（但括號不見了）、evaluate 是後序（算 4*5=20 再算 3+20）、printExp 是中序加括號（每個子樹都包一層，連葉節點也包）。課後練習：改 printExp，讓葉節點不要包括號，輸出變成 (3+(4*5))。")}'''
s, c1 = insert_end_of_section(s, "vocabulary", voc, 'id="dx-voc"')

hp = f'''{card("講義 09 · heapify 的使用畫面＋heapSort 練習", """#include <iostream>
#include <vector>
#include "binaryheap.hpp"
using namespace std;

vector<int> heapSort(vector<int> unsortedList) {{
    BinaryHeap heap;
    vector<int> sortedList;
    ____;                  // 1. heap.buildHeap(unsortedList)，O(n)
    while (____) {{         // 2. !heap.isEmpty()
        ____;
    }}
    return sortedList;
}}

int main() {{
    BinaryHeap aHeap;
    aHeap.buildHeap({{10, 4, 9, 8, 12, 15, 3, 5, 14, 18}});
    aHeap.print();

    for (int x : heapSort({{10, 3, 5, 1, 15, 7, 9, 2, 8}})) cout << x << " ";
    cout << endl;
    return 0;
}}""".replace("{{","{").replace("}}","}"),
"3 4 9 5 12 15 10 8 14 18\\n1 2 3 5 7 8 9 10 15", out_label="buildHeap 快照＋heapSort 完成後的輸出",
note='<span id="dx-hp"></span>第一行是 buildHeap 後的陣列：不是排序！只保證每個節點 ≤ 兩個小孩。buildHeap 為 O(n)，逐一 insert 則是 O(n log n)；delMin 每次 O(log n)。舊名稱 heapify/delet 仍相容。')}'''
s, c2 = insert_end_of_section(s, "heap", hp, 'id="dx-hp"')

bst = f'''{card("講義 09 · BinarySearchTree 當 Map 用＋treeSort 練習", """#include <iostream>
#include <vector>
#include "bst.hpp"   // TreeNode + BinarySearchTree
using namespace std;

vector<string> treeSort(vector<string> values) {{
    BinarySearchTree bst;
    vector<string> result;
    ____;   // 1. 全部 put 進去（平均每次 O(log n)）
    ____;   // 2. 中序走訪，鍵自動由小到大（O(n)）
    return result;
}}

int main() {{
    BinarySearchTree myTree;
    myTree.put("a", "a");      myTree.put("q", "quick");
    myTree.put("b", "brown");  myTree.put("f", "fox");
    myTree.put("j", "jumps");  myTree.put("o", "over");
    myTree.put("t", "the");    myTree.put("l", "lazy");
    myTree.put("d", "dog");

    cout << myTree.get("q") << " " << myTree.get("l") << endl;
    cout << "There are " << myTree.length() << " items in this tree" << endl;
    myTree.remove("a");
    cout << "There are " << myTree.length() << " items in this tree" << endl;
    myTree.inorder(myTree.root);   // 依鍵序印出 value
    cout << endl;
    return 0;
}}""".replace("{{","{").replace("}}","}"),
"quick lazy\\nThere are 9 items in this tree\\nThere are 8 items in this tree\\nbrown dog fox jumps lazy over quick the ",
note='<span id="dx-bst"></span>中序走訪 BST 會依鍵排序。put 遇到重複 key 時更新 value、size 不變；protected virtual insertOrAssign hook 讓 AVL 延伸插入而不繞過 size 契約。remove 釋放節點，整棵樹使用 deep-copy/move ownership。'.replace("{{","{").replace("}}","}"))}'''
s, c3 = insert_end_of_section(s, "bst", bst, 'id="dx-bst"')

PAGE.write_text(s)
print("inserted:", [n for n,ok in zip("voc heap bst".split(),[c1,c2,c3]) if ok])
