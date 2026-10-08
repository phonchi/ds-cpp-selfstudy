"""Chapter 7 programs: lecture listings from 07_Searching and Sorting.ipynb (headers: searching.hpp,
hashtable.hpp, sorting.hpp). OUT holds the exact stdout of every runnable program."""

# ---------------------------------------------------------------- searching
FIND = '''#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    vector<int> v = {3, 5, 2, 4, 1};
    cout << boolalpha << (find(v.begin(), v.end(), 15) != v.end()) << endl;
    cout << boolalpha << (find(v.begin(), v.end(), 3) != v.end()) << endl;
    return 0;
}'''

SEQ = '''#include <iostream>
#include <vector>
using namespace std;

bool sequentialSearch(vector<int> aList, int item) {
    unsigned pos = 0;
    while (pos < aList.size()) {
        if (aList[pos] == item) {
            return true;
        }
        pos = pos + 1;
    }
    return false;
}

int main() {
    vector<int> testList = {54, 26, 93, 17, 77, 31, 44, 55, 20, 65};
    cout << boolalpha;
    cout << sequentialSearch(testList, 44) << endl;
    cout << sequentialSearch(testList, 50) << endl;
    return 0;
}'''

ORDERED = '''#include <iostream>
#include <vector>
using namespace std;

bool orderedSequentialSearch(const vector<int>& aList, int item) {
    unsigned pos = 0;
    while (pos < aList.size()) {
        if (aList[pos] == item) return true;
        if (aList[pos] > item) return false;   // passed the spot: stop early!
        pos = pos + 1;
    }
    return false;
}

int main() {
    vector<int> testList = {17, 20, 26, 31, 44, 54, 55, 65, 77, 93};
    cout << boolalpha << orderedSequentialSearch(testList, 44) << endl;
    cout << orderedSequentialSearch(testList, 50) << endl;
    return 0;
}'''

BIN = '''#include <iostream>
#include "pythonds3/cppds/searching.hpp"   // the searches of this chapter
using namespace std;

int main() {
    vector<int> testList = {17, 20, 26, 31, 44, 54, 55, 65, 77, 93};
    cout << boolalpha;
    cout << binarySearch(testList, 44) << endl;
    cout << binarySearch(testList, 50) << endl;
    return 0;
}'''

BIN_REC = '''#include <iostream>
#include "pythonds3/cppds/searching.hpp"
using namespace std;

int main() {
    vector<int> testList = {17, 20, 26, 31, 44, 54, 55, 65, 77, 93};
    cout << boolalpha;
    cout << binarySearchRec(testList, 44) << endl;
    cout << binarySearchRec(testList, 50) << endl;
    return 0;
}'''

EX1_BLANK = '''#include <iostream>
#include <vector>
using namespace std;
bool binarySearchRec2(const vector<int>& a, int item, int first, int last) {
    if (____) return false;              // base case: empty range
    int midpoint = ____;
    if (a[midpoint] == item) return true;
    if (item < a[midpoint]) return binarySearchRec2(____);
    return binarySearchRec2(____);
}
int main() {
    vector<int> a = {17, 20, 26, 31, 44, 54, 55, 65, 77, 93};
    cout << boolalpha << binarySearchRec2(a, 44, 0, a.size()-1) << endl;
}'''

EX1_SOL = '''#include <iostream>
#include <vector>
using namespace std;
bool binarySearchRec2(const vector<int>& a, int item, int first, int last) {
    if (first > last) return false;              // base case: empty range
    int midpoint = first + (last - first) / 2;
    if (a[midpoint] == item) return true;
    if (item < a[midpoint]) return binarySearchRec2(a, item, first, midpoint - 1);
    return binarySearchRec2(a, item, midpoint + 1, last);
}
int main() {
    vector<int> a = {17, 20, 26, 31, 44, 54, 55, 65, 77, 93};
    cout << boolalpha << binarySearchRec2(a, 44, 0, a.size()-1) << endl;
    cout << binarySearchRec2(a, 50, 0, a.size()-1) << endl;
}'''

# ---------------------------------------------------------------- hashing
HASH_FUNCS = '''#include <iostream>
#include <string>
using namespace std;

int remainderMethod(int item, int divisor) { return item % divisor; }
int midsquareMethod(int item, int divisor) {
    string squared = to_string(item * item);
    if (squared.length() % 2 != 0) squared = "0" + squared;
    int mid = squared.length() / 2;
    return stoi(squared.substr(mid - 1, 2)) % divisor;
}

int main() {
    printf("%6s %10s %11s\\n", "Item", "Remainder", "Mid-Square");
    for (int item : {54, 26, 93, 17})
        printf("%6d %10d %11d\\n", item,
               remainderMethod(item, 11), midsquareMethod(item, 11));
    return 0;
}'''

HASH_STR = '''#include <iostream>
#include <string>
using namespace std;

int hashStr(string aString, int tableSize) {
    int sum = 0;
    for (char c : aString) {
        sum = sum + int(c);   // the ordinal value of the character
    }
    return sum % tableSize;
}

int main() {
    cout << hashStr("cat", 11) << endl;
    return 0;
}'''

HASH_STR_WEIGHTED = '''#include <iostream>
#include <string>
using namespace std;

int hashStr(string aString, int tableSize) {
    int sum = 0;
    for (char c : aString) sum = sum + int(c);
    return sum % tableSize;
}

// weight each character by its position: index i gets weight i + 1
int hashStrWeighted(string aString, int tableSize) {
    int sum = 0;
    for (size_t i = 0; i < aString.size(); i++) {
        sum = sum + int(aString[i]) * int(i + 1);
    }
    return sum % tableSize;
}

int main() {
    for (string w : {"cat", "act", "tac"})
        cout << w << ": " << hashStr(w, 11) << " " << hashStrWeighted(w, 11) << endl;
    return 0;
}'''

LINEAR_PROBE = '''#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> items = {54, 26, 93, 17, 77, 31, 44, 55, 20};
    vector<int> hashTable(11, -1);            // -1 is the reserved empty-slot marker
    for (int item : items) {
        int hashIndex = item % 11;
        while (hashTable[hashIndex] != -1)    // linear probing on collision
            hashIndex = (hashIndex + 1) % 11;
        hashTable[hashIndex] = item;
    }
    for (int idx = 0; idx < 11; idx++)
        cout << idx << ":" << hashTable[idx] << "  ";   // slot:item
    cout << endl;
    return 0;
}'''

EX2_BLANK = '''#include <iostream>
#include <stdexcept>
#include <vector>
using namespace std;
vector<int> quadraticProbing(const vector<int>& items, int divisor) {
    vector<int> table(divisor, -1);
    for (int item : items) {
        int h = item % divisor, probe = 0, index = h;
        while (table[index] != -1) {
            if (++probe >= divisor) throw overflow_error("probe exhausted");
            index = ____;  // h, h+1, h+4, h+9, ...
        }
        table[index] = item;
    }
    return table;
}
int main() { for (int v : quadraticProbing(
    {113,117,97,100,114,108,116,105,99}, 11)) cout << v << " "; }'''

EX2_SOL = EX2_BLANK.replace('index = ____;  // h, h+1, h+4, h+9, ...',
                            'index = (h + probe * probe) % divisor;  // h, h+1, h+4, h+9, ...')

HT_CLASS = '''class HashTable {
    public:
        HashTable(int sz) {
            size = sz;
            slots = vector<int>(size, -1);        // -1 marks an empty slot
            data = vector<string>(size, "");
        }

        int hashFunction(int key) {
            return key % size;
        }

        int rehash(int oldHash) {
            return (oldHash + 1) % size;
        }

    private:
        int size;
        vector<int> slots;
        vector<string> data;
};'''

HT_PUT_FRAG = '''void put(int key, string value) {
    int hashValue = hashFunction(key);

    if (slots[hashValue] == -1) {
        slots[hashValue] = key;
        data[hashValue] = value;
    } else {
        if (slots[hashValue] == key) {
            data[hashValue] = value;   // replace
        } else {
            int nextSlot = rehash(hashValue);
            while (slots[nextSlot] != -1 && slots[nextSlot] != key) {
                nextSlot = rehash(nextSlot);
            }
            slots[nextSlot] = key;
            data[nextSlot] = value;
        }
    }
}'''

HT_GET_FRAG = '''string get(int key) {
    int startSlot = hashFunction(key);

    int position = startSlot;
    while (slots[position] != -1) {
        if (slots[position] == key) {
            return data[position];
        }
        position = rehash(position);
        if (position == startSlot) {
            return "";   // not found: return the empty string
        }
    }
    return "";
}'''

HT_SESSION1 = '''#include <iostream>
#include "pythonds3/cppds/hashtable.hpp"   // the class of this section
using namespace std;

int main() {
    HashTable h(11);
    int keys[] = {54, 26, 93, 17, 77, 31, 44, 55, 20};
    string vals[] = {"cat", "dog", "lion", "tiger", "bird",
                     "cow", "goat", "pig", "chicken"};
    for (int i = 0; i < 9; i++) h.put(keys[i], vals[i]);

    h.printSlots();
    h.printData();
    return 0;
}'''

HT_SESSION2 = '''#include <iostream>
#include "pythonds3/cppds/hashtable.hpp"
using namespace std;

int main() {
    HashTable h(11);
    int keys[] = {54, 26, 93, 17, 77, 31, 44, 55, 20};
    string vals[] = {"cat", "dog", "lion", "tiger", "bird",
                     "cow", "goat", "pig", "chicken"};
    for (int i = 0; i < 9; i++) h.put(keys[i], vals[i]);

    cout << h.get(20) << " " << h.get(17) << endl;
    h.put(20, "duck");                            // replace the value for key 20
    cout << h.get(20) << endl;
    h.printData();
    cout << "[" << h.get(99) << "]" << endl;      // not in the table: empty string
    return 0;
}'''

# ---------------------------------------------------------------- sorting
SWAP_FRAG = '''int temp = aList[i];
aList[i] = aList[j];
aList[j] = temp;'''


def sort_main(comment_include, init, call, final_printl=True):
    return ('#include <iostream>\n#include "pythonds3/cppds/sorting.hpp"' + comment_include + '\nusing namespace std;\n\n'
            'int main() {\n    vector<int> aList = ' + init + ';\n    ' + call + '\n'
            + ('    printl(aList);\n' if final_printl else '') + '    return 0;\n}')


BUBBLE = sort_main('   // printl + the sorts of this chapter', '{4, 14, 5, 21, 29, 12, 16}',
                   'bubbleSort(aList);   // prints the vector at the start of every pass')
SHORT = sort_main('', '{20, 30, 40, 90, 50, 60, 70, 80, 100, 110}',
                  'bubbleSortShort(aList);   // stops as soon as a pass makes no exchange')
SELECTION = sort_main('', '{11, 7, 12, 14, 19, 1, 6, 18, 8, 20}',
                      'selectionSort(aList);   // prints the vector at the start of every pass')
INSERTION = sort_main('', '{9, 2, 5, 5, 7, 9, 1}',
                      'insertionSort(aList);   // prints the vector before every insertion pass')
SHELL = sort_main('   // gapInsertionSort + shellSort', '{54, 26, 93, 17, 77, 31, 44, 55, 20}', 'shellSort(aList);')
MERGE = sort_main('', '{54, 26, 93, 17}', 'mergeSort(aList);   // the final Merging line is the sorted result',
                  final_printl=False)
QUICK = sort_main('   // partition + quickSort (md listing above)', '{54, 26, 93, 17, 77, 31, 44, 55, 20}',
                  'quickSort(aList);   // prints the vector after every partition')

QDESC_SKETCH = '''void quickSort(vector<int>& aList, bool descending = false) {
    quickSortHelper(aList, 0, aList.size() - 1, descending);
}

void quickSortHelper(vector<int>& aList, int first, int last, bool descending) {
    if (first < last) {
        int split = partition(aList, first, last, descending);
        quickSortHelper(aList, first, split - 1, descending);
        quickSortHelper(aList, split + 1, last, descending);
    }
}'''

QDESC = '''#include <iostream>
#include "pythonds3/cppds/sorting.hpp"   // quickSortDesc (solution listing above)
using namespace std;

int main() {
    vector<int> aList = {54, 26, 93, 17, 77, 31, 44, 55, 20};
    quickSortDesc(aList, false);
    cout << "Ascending:  ";
    printl(aList);
    quickSortDesc(aList, true);
    cout << "Descending: ";
    printl(aList);
    return 0;
}'''

STD_SORT = '''#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    vector<int> aList = {54, 26, 93, 17, 77, 31, 44, 55, 20};
    sort(aList.begin(), aList.end());          // the STL built-in sort
    for (int x : aList) cout << x << " ";
    cout << endl;
    return 0;
}'''

RUN = {'find': FIND, 'seq': SEQ, 'ordered': ORDERED, 'bin': BIN, 'bin_rec': BIN_REC, 'ex1': EX1_SOL,
       'hash_funcs': HASH_FUNCS, 'hash_str': HASH_STR, 'hash_str_w': HASH_STR_WEIGHTED,
       'linear_probe': LINEAR_PROBE, 'ex2': EX2_SOL, 'ht1': HT_SESSION1, 'ht2': HT_SESSION2,
       'bubble': BUBBLE, 'short': SHORT, 'selection': SELECTION, 'insertion': INSERTION, 'shell': SHELL,
       'merge': MERGE, 'quick': QUICK, 'qdesc': QDESC, 'std_sort': STD_SORT}

OUT = {  # exact stdout (trailing newline included when the program prints one)
    'find': 'false\ntrue\n',
    'seq': 'true\nfalse\n',
    'ordered': 'true\nfalse\n',
    'bin': '4\ntrue\n4\n2\n0\nfalse\n',
    'bin_rec': '44\ntrue\n44\n65\n54\nfalse\n',
    'ex1': 'true\nfalse\n',
    'hash_funcs': '  Item  Remainder  Mid-Square\n    54         10           3\n    26          4           1\n    93          5           9\n    17          6           6\n',
    'hash_str': '4\n',
    'hash_str_w': 'cat: 4 3\nact: 4 5\ntac: 4 2\n',
    'linear_probe': '0:77  1:44  2:55  3:20  4:26  5:93  6:17  7:-1  8:-1  9:31  10:54  \n',
    'ex2': '105 100 -1 113 114 99 116 117 -1 97 108 ',
    'ht1': '77 44 55 20 26 93 17 -1 -1 31 54 \nbird goat pig chicken dog lion tiger - - cow cat \n',
    'ht2': 'chicken tiger\nduck\nbird goat pig duck dog lion tiger - - cow cat \n[]\n',
    'bubble': '4 14 5 21 29 12 16 \n4 5 14 21 12 16 29 \n4 5 14 12 16 21 29 \n4 5 12 14 16 21 29 \n4 5 12 14 16 21 29 \n4 5 12 14 16 21 29 \n4 5 12 14 16 21 29 \n',
    'short': '20 30 40 50 60 70 80 90 100 110 \n',
    'selection': '11 7 12 14 19 1 6 18 8 20 \n11 7 12 14 19 1 6 18 8 20 \n11 7 12 14 8 1 6 18 19 20 \n11 7 12 14 8 1 6 18 19 20 \n11 7 12 6 8 1 14 18 19 20 \n11 7 1 6 8 12 14 18 19 20 \n8 7 1 6 11 12 14 18 19 20 \n6 7 1 8 11 12 14 18 19 20 \n6 1 7 8 11 12 14 18 19 20 \n1 6 7 8 11 12 14 18 19 20 \n',
    'insertion': '9 2 5 5 7 9 1 \n2 9 5 5 7 9 1 \n2 5 9 5 7 9 1 \n2 5 5 9 7 9 1 \n2 5 5 7 9 9 1 \n2 5 5 7 9 9 1 \n1 2 5 5 7 9 9 \n',
    'shell': 'After increments of size 4 the list is 20 26 44 17 54 31 93 55 77 \nAfter increments of size 2 the list is 20 17 44 26 54 31 77 55 93 \nAfter increments of size 1 the list is 17 20 26 31 44 54 55 77 93 \n17 20 26 31 44 54 55 77 93 \n',
    'merge': 'Splitting 54 26 93 17 \nSplitting 54 26 \nSplitting 54 \nMerging 54 \nSplitting 26 \nMerging 26 \nMerging 26 54 \nSplitting 93 17 \nSplitting 93 \nMerging 93 \nSplitting 17 \nMerging 17 \nMerging 17 93 \nMerging 17 26 54 93 \n',
    'quick': '31 26 20 17 44 54 77 55 93 \n17 26 20 31 44 54 77 55 93 \n17 26 20 31 44 54 77 55 93 \n17 20 26 31 44 54 77 55 93 \n17 20 26 31 44 54 55 77 93 \n17 20 26 31 44 54 55 77 93 \n',
    'qdesc': 'Ascending:  17 20 26 31 44 54 55 77 93 \nDescending: 93 77 55 54 44 31 26 20 17 \n',
    'std_sort': '17 20 26 31 44 54 55 77 93 \n',
}
