"""Chapter 6 programs: lecture listings from 06_Recursion.ipynb (and pythonds3/cppds/maze.hpp),
plus the few site additions that are labelled （補充） on the page. OUT holds exact stdout."""

LISTSUM_ITER = '''#include <iostream>
#include <vector>
using namespace std;

int listSum(const vector<int>& numList) {
    int theSum = 0;
    for (int value : numList) {
        theSum += value;
    }
    return theSum;
}

int main() {
    cout << listSum({1, 3, 5, 7, 9}) << endl;
    cout << listSum({}) << endl;   // the empty vector sums to 0
    return 0;
}'''

LISTSUM_REC = '''#include <cstddef>
#include <iostream>
#include <vector>
using namespace std;

int listSumFrom(const vector<int>& numList, size_t index) {
    if (index == numList.size()) {
        return 0;                              // empty remaining range
    }
    return numList[index] + listSumFrom(numList, index + 1);
}

int listSum(const vector<int>& numList) {
    return listSumFrom(numList, 0);
}

int main() {
    cout << listSum({1, 3, 5, 7, 9}) << endl;
    cout << listSum({}) << endl;               // safe: prints 0
    return 0;
}'''

TOSTR_MAIN = '''#include <iostream>
#include <string>
using namespace std;

// The algorithm outlined above for any base between 2 and 16.
string toStr(int n, int base) {
    string convertString = "0123456789ABCDEF";
    if (n < base) {
        return string(1, convertString[n]);
    } else {
        return toStr(n / base, base) + convertString[n % base];
    }
}

int main() {
    cout << toStr(1453, 16) << endl;
    return 0;
}'''

REVERSE_BLANK = '''#include <cassert>
#include <string>
using namespace std;
string reverse(string s) {
    if (s.size() <= 1) {
        return ____;            // handles "" and one character
    }
    return ____ + s[0];
}
int main() {
    assert(reverse("") == "");
    assert(reverse("hello") == "olleh");
}'''

REVERSE_SOLVED = '''#include <cassert>
#include <string>
using namespace std;
string reverse(string s) {
    if (s.size() <= 1) {
        return s;               // handles "" and one character
    }
    return reverse(s.substr(1)) + s[0];
}
int main() {
    assert(reverse("") == "");
    assert(reverse("hello") == "olleh");
}'''

TOSTR_STACK = '''#include <iostream>
#include <stack>
#include <string>
using namespace std;

string toStr(int n, int base) {
    stack<char> rStack;
    string convertString = "0123456789ABCDEF";
    while (n > 0) {
        rStack.push(convertString[n % base]);
        n = n / base;
    }
    string res = "";
    while (!rStack.empty()) {
        res = res + rStack.top();
        rStack.pop();
    }
    return res;
}

int main() { cout << toStr(1453, 16) << endl; }'''

TOSTR_DEPTH = '''#include <iostream>
#include <string>
#include <cstdio>
using namespace std;

int depth = 0;   // track the recursion depth explicitly

string toStr(int n, int base) {
    depth++;
    printf("  depth=%d, n=%d\\n", depth, n);
    string convertString = "0123456789ABCDEF";
    if (n < base) {
        return string(1, convertString[n]);
    }
    return toStr(n / base, base) + convertString[n % base];
}

int main() {
    cout << toStr(10, 2) << endl;
    return 0;
}'''

SPIRAL_MAIN = '''#include <CTurtle.hpp>
namespace ct = cturtle;

void spiral(ct::Turtle& turtle, int length) {
    if (length > 0) {
        turtle.forward(length);
        turtle.right(90);
        spiral(turtle, length - 5);
    }
}

int main() {
    ct::TurtleScreen screen;
    ct::Turtle turtle(screen);
    spiral(turtle, 100);
    screen.bye();
}'''

TREE = '''#include <CTurtle.hpp>
namespace ct = cturtle;

void tree(int branchLen, ct::Turtle& turtle) {
    if (branchLen > 5) {
        turtle.forward(branchLen);
        turtle.right(20);
        tree(branchLen - 15, turtle);
        turtle.left(40);
        tree(branchLen - 15, turtle);
        turtle.right(20);
        turtle.backward(branchLen);
    }
}'''

DRAW_TRIANGLE = '''#include <CTurtle.hpp>
namespace ct = cturtle;

void drawTriangle(ct::Point a, ct::Point b, ct::Point c,
                  ct::Color color, ct::Turtle& turtle) {
    turtle.fillcolor(color);
    turtle.penup(); turtle.goTo(a); turtle.pendown();
    turtle.begin_fill();
    turtle.goTo(c); turtle.goTo(b); turtle.goTo(a);
    turtle.end_fill();
}'''

SIERPINSKI = '''void sierpinski(ct::Point a, ct::Point b, ct::Point c,
                int degree, ct::Turtle& turtle) {
    const string colors[] = {
        "blue", "red", "green", "white", "yellow", "violet", "orange"
    };
    drawTriangle(a, b, c, {colors[degree]}, turtle);
    if (degree > 0) {
        sierpinski(a, ct::middle(a, b), ct::middle(a, c), degree - 1, turtle);
        sierpinski(b, ct::middle(a, b), ct::middle(b, c), degree - 1, turtle);
        sierpinski(c, ct::middle(c, b), ct::middle(a, c), degree - 1, turtle);
    }
}'''

SIER_MAIN = '''int main() {
    ct::TurtleScreen screen;
    screen.tracer(3);
    ct::Turtle turtle(screen);
    ct::Point points[] = {{-100, -50}, {0, 100}, {100, -50}};
    sierpinski(points[0], points[1], points[2], 3, turtle);
    screen.bye();
}'''

HANOI = '''#include <iostream>
#include <string>
using namespace std;

void moveDisk(string fromP, string toP) {
    cout << "moving disk from " << fromP << " to " << toP << endl;
}
void moveTower(int height, string fromPole, string toPole, string withPole) {
    if (height >= 1) {
        moveTower(height - 1, fromPole, withPole, toPole);
        moveDisk(fromPole, toPole);
        moveTower(height - 1, withPole, toPole, fromPole);
    }
}

int main() { moveTower(3, "A", "B", "C"); }'''

MAZE_TEXT = '''++++++++++++++++++++++
+   +   ++ ++     +
+ +   +       +++ + ++
+ + +  ++  ++++   + ++
+++ ++++++    +++ +  +
+          ++  ++    +
+++++ ++++++   +++++ +
+     +   +++++++  + +
+ +++++++      S +   +
+                + +++
++++++++++++++++++ +++'''

MAZE_CONSTS = '''const char START = 'S';
const char OBSTACLE = '+';
const char TRIED = '.';
const char DEAD_END = '-';
const char PART_OF_PATH = 'O';'''

MAZE_CLASS = '''class Maze {
    public:
        Maze(string mazeFilename) {
            ifstream mazeFile(mazeFilename);
            string line;
            while (getline(mazeFile, line)) {
                mazeList.push_back(line);
            }
            rowsInMaze = mazeList.size();
            columnsInMaze = mazeList[0].size();
            for (int row = 0; row < rowsInMaze; row++) {
                size_t col = mazeList[row].find(START);
                if (col != string::npos) {
                    startRow = row;
                    startCol = col;
                    break;
                }
            }
        }

        int startRow;
        int startCol;
    private:
        vector<string> mazeList;
        int rowsInMaze;
        int columnsInMaze;
};'''

MAZE_UPDATE_PRINT = '''void updatePosition(int row, int col, char val) {
    mazeList[row][col] = val;
}

void print() {
    for (string& row : mazeList) {
        cout << row << endl;
    }
}'''

MAZE_EXIT_GET = '''bool isExit(int row, int col) {
    return (row == 0 || row == rowsInMaze - 1 ||
            col == 0 || col == columnsInMaze - 1);
}

char get(int row, int col) {
    return mazeList[row][col];
}'''

SEARCH_FROM = '''bool searchFrom(Maze& maze, int row, int column) {
    // Base Case return values:
    //  1. We have run into an obstacle, return false
    if (maze.get(row, column) == OBSTACLE) {
        return false;
    }
    //  2. We have found an already explored square
    if (maze.get(row, column) == TRIED || maze.get(row, column) == DEAD_END) {
        return false;
    }
    //  3. We have found an exit
    if (maze.isExit(row, column)) {
        maze.updatePosition(row, column, PART_OF_PATH);
        return true;
    }
    maze.updatePosition(row, column, TRIED);
    // Otherwise, use logical short circuiting to try each direction
    bool found = searchFrom(maze, row - 1, column)
              || searchFrom(maze, row + 1, column)
              || searchFrom(maze, row, column - 1)
              || searchFrom(maze, row, column + 1);
    if (found) {
        maze.updatePosition(row, column, PART_OF_PATH);
    } else {
        maze.updatePosition(row, column, DEAD_END);
    }
    return found;
}'''

MAZE_MAIN = '''#include <iostream>
#include "pythonds3/cppds/maze.hpp"   // Maze class + searchFrom (md listing above)
using namespace std;

int main() {
    Maze myMaze("maze2.txt");
    searchFrom(myMaze, myMaze.startRow, myMaze.startCol);
    myMaze.print();   // O = path, . = tried, - = dead end
    return 0;
}'''

MAZE2_TXT = '''++++++++++++++++++++++
+   +   ++ ++        +
      +     ++++++++++
+ +    ++  ++++ +++ ++
+ +   + + ++    +++  +
+          ++  ++  + +
+++++ + +      ++  + +
+++++ +++  + +  ++   +
+          + + S+ +  +
+++++ +  + + +     + +
++++++++++++++++++++++'''

MC1 = '''#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

int makeChange1(vector<int> coinDenoms, int change) {
    if (find(coinDenoms.begin(), coinDenoms.end(), change) != coinDenoms.end()) {
        return 1;
    }
    int minCoins = INT_MAX;
    for (int i : coinDenoms) {
        if (i <= change) {
            int numCoins = 1 + makeChange1(coinDenoms, change - i);
            minCoins = min(numCoins, minCoins);
        }
    }
    return minCoins;
}

int main() {
    // 26 cents makes 377 total calls; 63 cents makes 67,716,925.
    cout << makeChange1({1, 5, 10, 25}, 26) << endl;
    return 0;
}'''

# Site addition: the lecture states the call counts; this version counts them.
MC_COUNT = '''#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

long calls1 = 0;   // how many times makeChange1 runs
long calls2 = 0;   // how many times makeChange2 runs

int makeChange1(vector<int> coinDenoms, int change) {
    calls1++;
    if (find(coinDenoms.begin(), coinDenoms.end(), change) != coinDenoms.end()) {
        return 1;
    }
    int minCoins = INT_MAX;
    for (int i : coinDenoms) {
        if (i <= change) {
            int numCoins = 1 + makeChange1(coinDenoms, change - i);
            minCoins = min(numCoins, minCoins);
        }
    }
    return minCoins;
}

int makeChange2(const vector<int>& coins, int change,
                vector<int>& knownResults) {
    calls2++;
    int minCoins = change;
    for (int coin : coins) {
        if (coin == change) {
            knownResults[change] = 1;
            return 1;
        } else if (knownResults[change] > 0) {
            return knownResults[change];
        }
    }
    for (int coin : coins) {
        if (coin <= change) {
            int candidate = 1 + makeChange2(
                coins, change - coin, knownResults);
            if (candidate < minCoins) {
                minCoins = candidate;
                knownResults[change] = minCoins;
            }
        }
    }
    return minCoins;
}

int main() {
    for (int change : {26, 15}) {
        calls1 = 0;
        int n = makeChange1({1, 5, 10, 25}, change);
        cout << "makeChange1(" << change << "): " << n << " coins, "
             << calls1 << " calls" << endl;
    }
    vector<int> knownResults(64, 0);
    int n = makeChange2({1, 5, 10, 25}, 63, knownResults);
    cout << "makeChange2(63): " << n << " coins, " << calls2 << " calls" << endl;
    cout << "knownResults[0..10]:";
    for (int i = 0; i <= 10; i++) cout << " " << knownResults[i];
    cout << endl;
    return 0;
}'''

MC2 = '''#include <iostream>
#include <vector>
using namespace std;

int makeChange2(const vector<int>& coins, int change,
                vector<int>& knownResults) {
    int minCoins = change;
    for (int coin : coins) {
        if (coin == change) {
            knownResults[change] = 1;
            return 1;
        } else if (knownResults[change] > 0) {
            return knownResults[change];
        }
    }
    for (int coin : coins) {
        if (coin <= change) {
            int candidate = 1 + makeChange2(
                coins, change - coin, knownResults);
            if (candidate < minCoins) {
                minCoins = candidate;
                knownResults[change] = minCoins;
            }
        }
    }
    return minCoins;
}

int main() {
    vector<int> knownResults(64, 0);
    cout << makeChange2({1, 5, 10, 25}, 63, knownResults) << endl;
}'''

MC3 = '''#include <iostream>
#include <vector>
using namespace std;

int makeChange3(vector<int>& coinValueList, int change, vector<int>& minCoins) {
    for (int cents = 0; cents <= change; cents++) {
        int coinCount = cents;
        for (int j : coinValueList) {
            if (j <= cents && minCoins[cents - j] + 1 < coinCount) {
                coinCount = minCoins[cents - j] + 1;
            }
        }
        minCoins[cents] = coinCount;
    }
    return minCoins[change];
}

int main() {
    vector<int> coins = {1, 5, 10, 25};
    vector<int> minCoins(64, 0);
    cout << makeChange3(coins, 63, minCoins) << endl;
    return 0;
}'''

MC4_FUNCS = '''int makeChange4(vector<int>& coinValueList, int change,
                vector<int>& minCoins, vector<int>& coinsUsed) {
    for (int cents = 0; cents <= change; cents++) {
        int coinCount = cents;
        int newCoin = 1;
        for (int j : coinValueList) {
            if (j <= cents && minCoins[cents - j] + 1 < coinCount) {
                coinCount = minCoins[cents - j] + 1;
                newCoin = j;
            }
        }
        minCoins[cents] = coinCount;
        coinsUsed[cents] = newCoin;
    }
    return minCoins[change];
}

void printCoins(vector<int>& coinsUsed, int change) {
    int coin = change;
    while (coin > 0) {
        int thisCoin = coinsUsed[coin];
        cout << thisCoin << " ";
        coin = coin - thisCoin;
    }
    cout << endl;
}'''

MC4 = '''#include <iostream>
#include <vector>
using namespace std;

''' + MC4_FUNCS + '''

int main() {
    int amnt = 63;
    vector<int> clist = {1, 5, 10, 21, 25};
    vector<int> coinsUsed(amnt + 1, 0);
    vector<int> coinCount(amnt + 1, 0);

    cout << "Making change for " << amnt << " requires the following "
         << makeChange4(clist, amnt, coinCount, coinsUsed) << " coins: ";
    printCoins(coinsUsed, amnt);
    cout << "The used list is as follows:" << endl;
    for (int c : coinsUsed) cout << c << " ";
    cout << endl;
    return 0;
}'''

OUT = {
    'listsum_iter': '25\n0',
    'listsum_rec': '25\n0',
    'tostr': '5AD',
    'tostr_stack': '5AD',
    'tostr_depth': '  depth=1, n=10\n  depth=2, n=5\n  depth=3, n=2\n  depth=4, n=1\n1010',
    'hanoi': ('moving disk from A to B\nmoving disk from A to C\nmoving disk from B to C\n'
              'moving disk from A to B\nmoving disk from C to A\nmoving disk from C to B\nmoving disk from A to B'),
    'maze': '''++++++++++++++++++++++
+-OO+OOO++ ++        +
OOOOOO+OOO  ++++++++++
+-+-OO ++O ++++ +++ ++
+-+-OO+ +O++ OO +++  +
+---OO   OO++OO++  + +
+++++-+ +-OOOOO++  + +
+++++-+++--+-+OO++   +
+----------+-+ O+ +  +
+++++-+--+-+-+     + +
++++++++++++++++++++++''',
    'mc1': '2',
    'mc_count': ('makeChange1(26): 2 coins, 377 calls\nmakeChange1(15): 2 coins, 52 calls\n'
                 'makeChange2(63): 6 coins, 221 calls\nknownResults[0..10]: 0 1 0 0 0 1 2 3 4 5 1'),
    'mc2': '6',
    'mc3': '6',
    'mc4': ('Making change for 63 requires the following 3 coins: 21 21 21 \nThe used list is as follows:\n'
            '1 1 1 1 1 5 1 1 1 1 10 1 1 1 1 5 1 1 1 1 10 21 1 1 1 25 1 1 1 1 5 10 1 1 1 10 1 1 1 1 5 10 21 1 1 10 21 1 1 1 25 1 10 1 1 5 10 1 1 1 10 1 10 21 '),
}
