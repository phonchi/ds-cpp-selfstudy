"""Chapter 4 complete programs that turn the lecture's worked scenarios into runnable code.

Each program uses the lecture's names and pythonds3/cppds/linked_list.hpp. OUTPUT holds the exact
program output without the final newline; linked_depth adds it back for data-expected.
"""

UL_EMPTY = '''#include <iostream>
#include "pythonds3/cppds/linked_list.hpp"
using namespace std;

int main() {
    UnorderedList<int> myList;   // the constructor sets head to NULL
    cout << boolalpha << myList.isEmpty() << endl;
    cout << myList.size() << endl;
    myList.add(31);              // now head points to one node
    cout << myList.isEmpty() << endl;
    cout << myList.size() << endl;
    return 0;
}'''

UL_ADDS = '''#include <iostream>
#include "pythonds3/cppds/linked_list.hpp"
using namespace std;

int main() {
    UnorderedList<int> myList;
    myList.add(31); cout << myList << endl;
    myList.add(77); cout << myList << endl;
    myList.add(17); cout << myList << endl;
    myList.add(93); cout << myList << endl;
    myList.add(26); cout << myList << endl;
    myList.add(54); cout << myList << endl;
    return 0;
}'''

UL_SIZE_MAIN = '''#include <iostream>
#include "pythonds3/cppds/linked_list.hpp"
using namespace std;

int main() {
    UnorderedList<int> myList;
    cout << myList.size() << endl;          // empty: the loop body never runs
    for (int value : {31, 77, 17, 93, 26, 54}) {
        myList.add(value);
    }
    cout << myList.size() << endl;          // six nodes visited
    myList.remove(93);
    cout << myList.size() << endl;
    return 0;
}'''

UL_SEARCH_MAIN = '''#include <iostream>
#include "pythonds3/cppds/linked_list.hpp"
using namespace std;

int main() {
    UnorderedList<int> myList;
    for (int value : {31, 77, 17, 93, 26, 54}) {
        myList.add(value);
    }
    cout << myList << endl;
    cout << boolalpha << myList.search(17) << endl;   // stops at the 4th node
    cout << myList.search(54) << endl;                // first node
    cout << myList.search(45) << endl;                // walks to NULL
    return 0;
}'''

UL_REMOVE_MID = '''#include <iostream>
#include "pythonds3/cppds/linked_list.hpp"
using namespace std;

int main() {
    UnorderedList<int> myList;
    for (int value : {31, 77, 17, 93, 26, 54}) {
        myList.add(value);
    }
    cout << myList << endl;
    myList.remove(17);       // previous stops at 93, current at 17
    cout << myList << endl;
    cout << myList.size() << endl;
    cout << boolalpha << myList.search(17) << endl;
    return 0;
}'''

UL_REMOVE_HEAD = '''#include <iostream>
#include "pythonds3/cppds/linked_list.hpp"
using namespace std;

int main() {
    UnorderedList<int> myList;
    for (int value : {31, 77, 17, 93, 26, 54}) {
        myList.add(value);
    }
    myList.remove(54);       // previous is still NULL: head changes
    cout << myList << endl;
    myList.remove(31);       // last node: previous->setNext(NULL)
    cout << myList << endl;
    myList.remove(45);       // not found: the list is unchanged
    cout << myList << endl;

    UnorderedList<int> one;
    one.add(7);
    one.remove(7);           // the only node: head becomes NULL
    cout << boolalpha << one.isEmpty() << endl;
    return 0;
}'''

OL_SEARCH_MAIN = '''#include <iostream>
#include "pythonds3/cppds/linked_list.hpp"
using namespace std;

int main() {
    OrderedList<int> myList;
    for (int value : {31, 77, 17, 93, 26, 54}) {
        myList.add(value);
    }
    cout << myList << endl;
    cout << boolalpha << myList.search(45) << endl;   // stops at 54
    cout << myList.search(31) << endl;
    cout << myList.search(10) << endl;                // stops at 17
    cout << myList.search(100) << endl;               // walks to NULL
    return 0;
}'''

OL_ADD_MAIN = '''#include <iostream>
#include "pythonds3/cppds/linked_list.hpp"
using namespace std;

int main() {
    OrderedList<int> myList;
    for (int value : {93, 17, 77, 26, 54}) {
        myList.add(value);
    }
    cout << myList << endl;
    myList.add(31);          // between 26 and 54
    cout << myList << endl;
    myList.add(10);          // head->getData() >= item: new head
    cout << myList << endl;
    myList.add(100);         // current stops at the last node
    cout << myList << endl;
    return 0;
}'''

NODE_PRIVATE = '''#include "pythonds3/cppds/linked_list.hpp"

int main() {
    Node<int> *temp = new Node<int>(93);
    temp->next = NULL;        // error: 'next' is private
    delete temp;
    return 0;
}'''

NODE_CHAIN = '''#include <iostream>
#include "pythonds3/cppds/linked_list.hpp"
using namespace std;

int main() {
    Node<int> *a = new Node<int>(54);
    Node<int> *b = new Node<int>(26);
    Node<int> *c = new Node<int>(93);
    a->setNext(b);            // 54 -> 26
    b->setNext(c);            // 26 -> 93, c->getNext() is still NULL
    b->setData(27);           // changes data only; links stay the same

    Node<int> *current = a;
    while (current != NULL) {
        cout << current->getData() << " ";
        current = current->getNext();
    }
    cout << endl;
    cout << (a->getNext()->getNext() == c) << endl;   // 1 means true
    delete a; delete b; delete c;
    return 0;
}'''

CIRC_MAIN = '''#include <iostream>
#include "pythonds3/cppds/linked_list.hpp"
using namespace std;

void printCircular(Node<int> *head) {
    if (head == NULL) return;
    Node<int> *current = head;
    do {                                   // stop when we are back at the start
        cout << current->getData() << " ";
        current = current->getNext();
    } while (current != head);
    cout << endl;
}

int main() {
    Node<int> *head = new Node<int>(54);
    Node<int> *tail = head;
    for (int value : {26, 93, 17}) {
        Node<int> *temp = new Node<int>(value);
        tail->setNext(temp);
        tail = temp;
    }
    tail->setNext(head);                   // tail->next == head
    printCircular(head);
    cout << tail->getNext()->getData() << endl;

    Node<int> *temp = new Node<int>(11);   // append in O(1) with tail
    temp->setNext(head);
    tail->setNext(temp);
    tail = temp;
    printCircular(head);
    printCircular(head->getNext()->getNext());   // any node can be the start

    tail->setNext(NULL);                   // break the ring, then free every node
    while (head != NULL) {
        Node<int> *next = head->getNext();
        delete head;
        head = next;
    }
    return 0;
}'''

DLL_COMMON = '''#include <iostream>
using namespace std;

struct DNode {                 // header and trailer are sentinels: their data is unused
    int data;
    DNode *prev;
    DNode *next;
    DNode(int d = 0) : data(d), prev(NULL), next(NULL) {}
};

void insertBetween(int item, DNode *pred, DNode *succ) {
    DNode *newNode = new DNode(item);
    newNode->prev = pred;      // 1
    newNode->next = succ;      // 2
    pred->next = newNode;      // 3
    succ->prev = newNode;      // 4
}

void print(DNode *header, DNode *trailer) {
    for (DNode *p = header->next; p != trailer; p = p->next) cout << p->data << " ";
    cout << "| ";
    for (DNode *p = trailer->prev; p != header; p = p->prev) cout << p->data << " ";
    cout << endl;
}
'''

DLL_INSERT = DLL_COMMON + '''
int main() {
    DNode *header = new DNode, *trailer = new DNode;
    header->next = trailer;            // empty list: the sentinels meet
    trailer->prev = header;
    print(header, trailer);

    insertBetween(54, trailer->prev, trailer);   // every insertion has two neighbours
    insertBetween(26, trailer->prev, trailer);
    insertBetween(93, trailer->prev, trailer);
    print(header, trailer);

    DNode *pred = header->next->next;            // 26
    insertBetween(77, pred, pred->next);         // between 26 and 93
    print(header, trailer);
    insertBetween(10, header, header->next);     // at the front
    print(header, trailer);

    while (header != NULL) { DNode *n = header->next; delete header; header = n; }
    return 0;
}'''

DLL_ERASE = DLL_COMMON + '''
void erase(DNode *node) {      // node must be a real data node, never a sentinel
    DNode *pred = node->prev;
    DNode *succ = node->next;
    pred->next = succ;
    succ->prev = pred;
    delete node;
}

int main() {
    DNode *header = new DNode, *trailer = new DNode;
    header->next = trailer;
    trailer->prev = header;
    for (int value : {54, 26, 77, 93}) insertBetween(value, trailer->prev, trailer);
    print(header, trailer);

    erase(header->next->next->next);   // 77: 26 and 93 become neighbours
    print(header, trailer);
    erase(header->next);               // first item: its pred is the header
    print(header, trailer);
    erase(trailer->prev);              // last item: its succ is the trailer
    print(header, trailer);

    while (header != NULL) { DNode *n = header->next; delete header; header = n; }
    return 0;
}'''

APPEND_MAIN = '''#include <iostream>
#include "pythonds3/cppds/linked_list.hpp"
using namespace std;

template <typename T>
class MyList {                 // only the parts needed to try append()
    private:
        Node<T> *head;
    public:
        MyList() { head = NULL; }
        ~MyList() {
            while (head != NULL) {
                Node<T> *next = head->getNext();
                delete head;
                head = next;
            }
        }
        void add(T item) {
            Node<T> *temp = new Node<T>(item);
            temp->setNext(head);
            head = temp;
        }
        void append(T item) {
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
        }
        void print() const {
            for (Node<T> *current = head; current != NULL; current = current->getNext())
                cout << current->getData() << " ";
            cout << endl;
        }
};

int main() {
    MyList<int> myList;
    myList.append(31);       // empty list: the new node becomes head
    myList.add(77);
    myList.append(17);       // walks to 31, then links 17 after it
    myList.print();
    return 0;
}'''

OL_REMOVE_MAIN = '''#include <iostream>
#include "pythonds3/cppds/linked_list.hpp"
using namespace std;

int main() {
    OrderedList<int> myList;
    for (int value : {31, 77, 17, 93, 26, 54}) {
        myList.add(value);
    }
    myList.remove(54);       // stops at 54: found, unlink it
    cout << myList << endl;
    myList.remove(17);       // previous is NULL: head changes
    cout << myList << endl;
    myList.remove(45);       // stops at 77 > 45: not found, no change
    cout << myList << endl;
    cout << myList.size() << endl;
    return 0;
}'''

OUTPUT = {
    'ul_empty': 'true\n0\nfalse\n1',
    'ul_adds': '31 \n77 31 \n17 77 31 \n93 17 77 31 \n26 93 17 77 31 \n54 26 93 17 77 31 ',
    'ul_size': '0\n6\n5',
    'ul_search': '54 26 93 17 77 31 \ntrue\ntrue\nfalse',
    'ul_remove_mid': '54 26 93 17 77 31 \n54 26 93 77 31 \n5\nfalse',
    'ul_remove_head': '26 93 17 77 31 \n26 93 17 77 \n26 93 17 77 \ntrue',
    'ol_search': '17 26 31 54 77 93 \nfalse\ntrue\nfalse\nfalse',
    'ol_add': '17 26 54 77 93 \n17 26 31 54 77 93 \n10 17 26 31 54 77 93 \n10 17 26 31 54 77 93 100 ',
    'node_chain': '54 27 93 \n1',
    'circ': '54 26 93 17 \n54\n54 26 93 17 11 \n93 17 11 54 26 ',
    'dll_insert': '| \n54 26 93 | 93 26 54 \n54 26 77 93 | 93 77 26 54 \n10 54 26 77 93 | 93 77 26 54 10 ',
    'dll_erase': '54 26 77 93 | 93 77 26 54 \n54 26 93 | 93 26 54 \n26 93 | 93 26 \n26 | 26 ',
    'append': '77 31 17 ',
    'ol_remove': '17 26 31 77 93 \n26 31 77 93 \n26 31 77 93 \n4',
}
