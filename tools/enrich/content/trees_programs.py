"""Chapter 9 programs: lecture listings from 09_Trees and Tree Algorithms.ipynb (headers: binarytree.hpp,
binaryheap.hpp, bst.hpp). OUT holds the exact stdout of every runnable program (checked by compiling)."""

# ---------------------------------------------------------------- BinaryTree, parse tree, traversals
BINARYTREE = '''#include <iostream>
#include "pythonds3/cppds/binarytree.hpp"   // the class of this section
using namespace std;

int main() {
    BinaryTree aTree("a");
    cout << aTree.getRootVal() << endl;
    cout << aTree.getLeftChild() << endl;      // NULL prints as 0
    aTree.insertLeft("b");
    cout << aTree.getLeftChild()->getRootVal() << endl;
    aTree.insertRight("c");
    cout << aTree.getRightChild()->getRootVal() << endl;
    aTree.getRightChild()->setRootVal("hello");
    cout << aTree.getRightChild()->getRootVal() << endl;
    return 0;
}'''

PARSE_INORDER = '''#include <iostream>
#include "pythonds3/cppds/binarytree.hpp"   // buildParseTree
using namespace std;

int main() {
    BinaryTree* pt = buildParseTree("( 3 + ( 4 * 5 ) )");
    inorder(pt);   // defined and explained in the next section
    cout << endl;
    return 0;
}'''

EVALUATE = '''#include <iostream>
#include "pythonds3/cppds/binarytree.hpp"   // evaluate
using namespace std;

int main() {
    BinaryTree* pt = buildParseTree("( 3 + ( 4 * 5 ) )");
    cout << evaluate(pt) << endl;
    return 0;
}'''

BOOK = '''#include <iostream>
#include "pythonds3/cppds/binarytree.hpp"   // BinaryTree, preorder
using namespace std;

int main() {
    BinaryTree book("Book");
    book.insertLeft("Chapter1");
    book.insertRight("Chapter2");
    BinaryTree* ch1 = book.getLeftChild();
    ch1->insertLeft("Section1.1");
    ch1->insertRight("Section1.2");
    ch1->getRightChild()->insertLeft("Section1.2.1");
    ch1->getRightChild()->insertRight("Section1.2.2");
    BinaryTree* ch2 = book.getRightChild();
    ch2->insertLeft("Section2.1");
    ch2->insertRight("Section2.2");
    ch2->getRightChild()->insertLeft("Section2.2.1");
    ch2->getRightChild()->insertRight("Section2.2.2");

    preorder(&book);
    cout << endl;
    return 0;
}'''

TRAVERSALS = '''#include <iostream>
#include "pythonds3/cppds/binarytree.hpp"   // preorder, inorder, postorder, postordereval
using namespace std;

int main() {
    BinaryTree* pt = buildParseTree("( 3 + ( 4 * 5 ) )");
    cout << "preorder:  ";
    preorder(pt);
    cout << endl << "inorder:   ";
    inorder(pt);
    cout << endl << "postorder: ";
    postorder(pt);
    cout << endl << "postordereval: " << postordereval(pt) << endl;
    return 0;
}'''

PRINTEXP = '''#include <iostream>
#include "pythonds3/cppds/binarytree.hpp"   // printExp
using namespace std;

int main() {
    BinaryTree* pt = buildParseTree("( 3 + ( 4 * 5 ) )");
    cout << printExp(pt) << endl;
    return 0;
}'''

EX1_START = '''#include <iostream>
#include "pythonds3/cppds/binarytree.hpp"
using namespace std;

// Modify printExp so leaf numbers are not wrapped in parentheses
string printExp2(BinaryTree* tree) {
    string result = "";
    if (tree != NULL) {
        result = "(" + printExp2(tree->getLeftChild());
        result = result + tree->getRootVal();
        result = result + printExp2(tree->getRightChild()) + ")";
    }
    return result;
}

int main() {
    BinaryTree* pt = buildParseTree("( 3 + ( 4 * 5 ) )");
    cout << printExp2(pt) << endl;
    return 0;
}'''

EX1_SOL = '''#include <iostream>
#include "pythonds3/cppds/binarytree.hpp"
using namespace std;

// Leaf numbers are printed without parentheses
string printExp2(BinaryTree* tree) {
    string result = "";
    if (tree != NULL) {
        if (tree->getLeftChild() == NULL && tree->getRightChild() == NULL) {
            return tree->getRootVal();          // a leaf: just the number
        }
        result = "(" + printExp2(tree->getLeftChild());
        result = result + tree->getRootVal();
        result = result + printExp2(tree->getRightChild()) + ")";
    }
    return result;
}

int main() {
    BinaryTree* pt = buildParseTree("( 3 + ( 4 * 5 ) )");
    cout << printExp2(pt) << endl;
    return 0;
}'''

# ---------------------------------------------------------------- binary heap
HEAP_BASIC = '''#include <iostream>
#include "pythonds3/cppds/binaryheap.hpp"   // the class of this section
using namespace std;

int main() {
    BinaryHeap myHeap;
    myHeap.insert(5);
    myHeap.insert(7);
    myHeap.insert(3);
    myHeap.insert(11);

    cout << myHeap.delet() << endl;
    cout << myHeap.delet() << endl;
    cout << myHeap.delet() << endl;
    cout << myHeap.delet() << endl;
    return 0;
}'''

HEAP_FIGS = '''#include <iostream>
#include "pythonds3/cppds/binaryheap.hpp"
using namespace std;

int main() {
    BinaryHeap h;
    h.heap = {5, 9, 11, 14, 18, 19, 21, 33, 17, 27};   // the heap in the figures
    h.insert(7);                  // percUp: 7 rises past 18 and 9
    h.print();

    BinaryHeap d;
    d.heap = {5, 9, 11, 14, 18, 19, 21, 33, 17, 27};
    cout << d.delMin() << endl;   // percDown: 27 sinks past 9, 14 and 17
    d.print();
    return 0;
}'''

HEAP_OPS = '''#include <iostream>
#include "pythonds3/cppds/binaryheap.hpp"
using namespace std;

int main() {
    BinaryHeap heap;
    heap.buildHeap({10, 4, 9, 8, 12, 15, 3, 5, 14, 18});
    cout << heap.findMin() << " " << heap.size() << endl;
    while (!heap.isEmpty()) cout << heap.delMin() << " ";
    cout << endl;
    return 0;
}'''

BUILD_SMALL = '''#include <iostream>
#include "pythonds3/cppds/binaryheap.hpp"
using namespace std;

int main() {
    BinaryHeap aHeap;
    aHeap.buildHeap({9, 6, 5, 2, 3});
    aHeap.print();
    return 0;
}'''

HEAPIFY = '''#include <iostream>
#include "pythonds3/cppds/binaryheap.hpp"
using namespace std;

int main() {
    BinaryHeap aHeap;
    aHeap.heapify({10, 4, 9, 8, 12, 15, 3, 5, 14, 18});
    aHeap.print();
    return 0;
}'''

EX2_BLANK = '''#include <iostream>
#include <vector>
#include "pythonds3/cppds/binaryheap.hpp"
using namespace std;

vector<int> heapSort(vector<int> unsortedList) {
    BinaryHeap heap;
    vector<int> sortedList;
    ____;                  // 1. build the heap in O(n)
    while (____) {         // 2. repeatedly delete the minimum, O(log n) each
        ____;
    }
    return sortedList;
}
int main() {
    for (int x : heapSort({10, 3, 5, 1, 15, 7, 9, 2, 8})) cout << x << " ";
    return 0;
}'''

EX2_SOL = '''#include <iostream>
#include <vector>
#include "pythonds3/cppds/binaryheap.hpp"
using namespace std;

vector<int> heapSort(vector<int> unsortedList) {
    BinaryHeap heap;
    vector<int> sortedList;
    heap.buildHeap(unsortedList);              // 1. build the heap in O(n)
    while (!heap.isEmpty()) {                  // 2. repeatedly delete the minimum
        sortedList.push_back(heap.delMin());   //    O(log n) each
    }
    return sortedList;
}
int main() {
    for (int x : heapSort({10, 3, 5, 1, 15, 7, 9, 2, 8})) cout << x << " ";
    return 0;
}'''

# ---------------------------------------------------------------- binary search tree
BST = '''#include <iostream>
#include "pythonds3/cppds/bst.hpp"   // TreeNode + BinarySearchTree
using namespace std;

int main() {
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
    myTree.inorder(myTree.root);
    cout << endl;
    return 0;
}'''

EX3_BLANK = '''#include <iostream>
#include <vector>
#include "pythonds3/cppds/bst.hpp"
using namespace std;

vector<string> treeSort(vector<string> values) {
    BinarySearchTree bst;
    vector<string> result;
    ____;   // 1. insert all elements (O(log n) each on average)
    ____;   // 2. in-order traversal visits keys in sorted order (O(n))
    return result;
}
int main() {
    for (string s : treeSort({"t", "a", "o", "j", "d", "b", "q", "f", "l"}))
        cout << s << " ";
    return 0;
}'''

EX3_SOL = '''#include <iostream>
#include <vector>
#include "pythonds3/cppds/bst.hpp"
using namespace std;

void inorderKeys(TreeNode* node, vector<string>& keys) {
    if (node == NULL) return;
    inorderKeys(node->leftChild, keys);
    keys.push_back(node->key);
    inorderKeys(node->rightChild, keys);
}

vector<string> treeSort(vector<string> values) {
    BinarySearchTree bst;
    vector<string> result;
    for (string v : values) bst.put(v, v);   // 1. insert all elements
    inorderKeys(bst.root, result);           // 2. in-order traversal: sorted keys
    return result;
}
int main() {
    for (string s : treeSort({"t", "a", "o", "j", "d", "b", "q", "f", "l"}))
        cout << s << " ";
    return 0;
}'''

RUN = {'binarytree': BINARYTREE, 'parse_inorder': PARSE_INORDER, 'evaluate': EVALUATE, 'book': BOOK,
       'traversals': TRAVERSALS, 'printexp': PRINTEXP, 'ex1_start': EX1_START, 'ex1': EX1_SOL,
       'heap_basic': HEAP_BASIC, 'heap_ops': HEAP_OPS, 'heap_figs': HEAP_FIGS, 'build_small': BUILD_SMALL, 'heapify': HEAPIFY,
       'ex2': EX2_SOL, 'bst': BST, 'ex3': EX3_SOL}

OUT = {  # exact stdout (trailing newline included when the program prints one)
    'binarytree': 'a\n0\nb\nc\nhello\n',
    'parse_inorder': '3 + 4 * 5 \n',
    'evaluate': '23\n',
    'book': 'Book Chapter1 Section1.1 Section1.2 Section1.2.1 Section1.2.2 Chapter2 Section2.1 Section2.2 Section2.2.1 Section2.2.2 \n',
    'traversals': 'preorder:  + 3 * 4 5 \ninorder:   3 + 4 * 5 \npostorder: 3 4 5 * + \npostordereval: 23\n',
    'printexp': '((3)+((4)*(5)))\n',
    'ex1_start': '((3)+((4)*(5)))\n',
    'ex1': '(3+(4*5))\n',
    'heap_basic': '3\n5\n7\n11\n',
    'heap_ops': '3 10\n3 4 5 8 9 10 12 14 15 18 \n',
    'heap_figs': '5 7 11 14 9 19 21 33 17 27 18 \n5\n9 14 11 17 18 19 21 33 27 \n',
    'build_small': '2 3 5 6 9 \n',
    'heapify': '3 4 9 5 12 15 10 8 14 18 \n',
    'ex2': '1 2 3 5 7 8 9 10 15 ',
    'bst': 'quick lazy\nThere are 9 items in this tree\nThere are 8 items in this tree\nbrown dog fox jumps lazy over quick the \n',
    'ex3': 'a b d f j l o q t ',
}
assert set(OUT) == set(RUN)
