"""Chapter 5 programs: lecture code from 05_Linear_Structure.ipynb and pythonds3/cppds/*.hpp.

Complete programs keep the lecture's names and includes. OUTPUT holds the exact program output
without the final newline; linear_depth adds it back for data-expected.
"""

# ---------------------------------------------------------------- stack
STL_STACK_SNIPPET = '''#include <stack>

std::stack<std::string> s;
s.push("first");
s.push("second");
std::cout << s.top();   // second
s.pop();               // removes second; returns void'''

STL_STACK = '''#include <iostream>
#include <stack>
#include <string>
using namespace std;

int main() {
    stack<string> s;
    s.push("4"); s.push("dog"); s.push("true");
    cout << s.size() << endl;
    cout << boolalpha << s.empty() << endl;
    cout << s.top() << endl;
    s.pop();
    cout << s.top() << endl;
}'''

STACK2_CLASS = '''template <typename T>
class Stack2 {
    private:
        vector<T> items;

    public:
        bool isEmpty() {
            return items.empty();
        }
        void push(T item) {
            items.insert(items.begin(), item);   // O(n)!
        }
        T pop() {
            T top = items.front();
            items.erase(items.begin());   // O(n)!
            return top;
        }
        T peek() {
            return items.front();
        }
        int size() {
            return items.size();
        }
};'''

STACK2_MAIN = '''#include <iostream>
#include "pythonds3/cppds/stack.hpp"   // Stack2: top at the front, O(n) ops
using namespace std;

int main() {
    Stack2<double> s;
    cout << boolalpha << s.isEmpty() << endl;
    s.push(4);
    s.push(7.5);
    cout << s.peek() << endl;
    s.push(2);
    cout << s.size() << endl;
    cout << s.pop() << endl;
    cout << s.pop() << endl;
    cout << s.size() << endl;
    return 0;
}'''

STACK_HPP = '''template <typename T>
class Stack {
    private:
        vector<T> items;
    public:
        bool isEmpty() { return items.empty(); }
        void push(T item) { items.push_back(item); }
        T pop() { T top = items.back(); items.pop_back(); return top; }
        T peek() { return items.back(); }
        int size() { return items.size(); }
        void display() { for (T x : items) cout << x << " "; cout << endl; }
};'''

REV_EXERCISE = '''#include <iostream>
#include <stack>
using namespace std;

string revString(string myStr) {
    stack<char> s;
    // Step 1: push every char onto s;  Step 2: pop to build rStr
    string rStr = "";
    while (!s.empty()) {
        rStr =
    }
    return rStr;
}

int main() {
    cout << revString("NSYSU") << endl;
    return 0;
}'''

REV_SOLUTION = '''#include <iostream>
#include <stack>
using namespace std;

string revString(string myStr) {
    stack<char> s;
    for (char ch : myStr) {
        s.push(ch);              // Step 1: push every char onto s
    }
    string rStr = "";
    while (!s.empty()) {
        rStr = rStr + s.top();   // Step 2: the top is the last char not used yet
        s.pop();
    }
    return rStr;
}

int main() {
    cout << revString("NSYSU") << endl;
    return 0;
}'''

# ---------------------------------------------------------------- balanced symbols
PAR_CHECKER = '''#include <iostream>
#include <stack>
#include <string>
using namespace std;

bool parChecker(string symbolString) {
    stack<char> s;
    for (char symbol : symbolString) {
        if (symbol == '(') {
            s.push(symbol);
        } else {
            if (s.empty()) {
                return false;
            } else {
                s.pop();
            }
        }
    }
    return s.empty();
}

int main() {
    cout << boolalpha;
    cout << parChecker("((()))") << endl;    // expected true
    cout << parChecker("((()()))") << endl;  // expected true
    cout << parChecker("(()") << endl;       // expected false
    cout << parChecker(")(") << endl;        // expected false
    return 0;
}'''

MATCHES = '''bool matches(char symLeft, char symRight) {
    string allLefts = "([{";
    string allRights = ")]}";
    return allLefts.find(symLeft) == allRights.find(symRight);
}'''

BALANCE_CHECKER = '''#include <iostream>
#include <stack>
#include <string>
using namespace std;

bool matches(char symLeft, char symRight) {
    string allLefts = "([{";
    string allRights = ")]}";
    return allLefts.find(symLeft) == allRights.find(symRight);
}

bool balanceChecker(string symbolString) {
    stack<char> s;
    for (char symbol : symbolString) {
        if (symbol == '(' || symbol == '[' || symbol == '{') {
            s.push(symbol);
        } else {
            if (s.empty()) {
                return false;
            } else {
                char top = s.top();
                s.pop();
                if (!matches(top, symbol)) {
                    return false;
                }
            }
        }
    }
    return s.empty();
}

int main() {
    cout << boolalpha;
    cout << balanceChecker("{({([][])}())}") << endl;  // expected true
    cout << balanceChecker("[{()]") << endl;           // expected false
    return 0;
}'''

# ---------------------------------------------------------------- base conversion
DIVIDE_BY_2 = '''#include <iostream>
#include <stack>
#include <string>
using namespace std;

string divideBy2(int decimalNum) {
    stack<int> remStack;
    while (decimalNum > 0) {
        remStack.push(decimalNum % 2);
        decimalNum = decimalNum / 2;
    }
    string binString = "";
    while (!remStack.empty()) {
        binString += to_string(remStack.top());
        remStack.pop();
    }
    return binString;
}

int main() {
    cout << divideBy2(42) << " " << divideBy2(31) << endl;
    return 0;
}'''

BASE_CONVERTER = '''#include <iostream>
#include <stack>
using namespace std;

string baseConverter(int decimalNum, int base) {
    string digits = "0123456789ABCDEF";
    stack<int> remStack;
    while (decimalNum > 0) {
        remStack.push(decimalNum % base);  decimalNum /= base;
    }
    string newString = "";
    while (!remStack.empty()) {
        newString += digits[remStack.top()];  remStack.pop();
    }
    return newString;
}

int main() {
    cout << baseConverter(25, 2) << " " << baseConverter(25, 16) << endl;
    return 0;
}'''

# ---------------------------------------------------------------- expressions
I2P_CORE = '''for (string token : tokenList) {
    if (isalnum(token[0])) {
        postfixList.push_back(token);
    } else if (token == "(") {
        opStack.push(token);
    } else if (token == ")") {
        while (!opStack.empty() && opStack.top() != "(") {
            postfixList.push_back(opStack.top());
            opStack.pop();
        }
        opStack.pop();   // pop the "("
    } else {
        while (!opStack.empty() && prec[opStack.top()] >= prec[token]) {
            postfixList.push_back(opStack.top());
            opStack.pop();
        }
        opStack.push(token);
    }
}'''

I2P_HEADER = '''string infixToPostfix(string infixExpr) {
    map<string, int> prec = {{"*", 3}, {"/", 3}, {"+", 2}, {"-", 2}, {"(", 1}};
    stack<string> opStack;
    vector<string> postfixList;
    stringstream ss(infixExpr);
    string token;
    while (ss >> token) {
        if (isalnum(token[0])) {
            postfixList.push_back(token);
        } else if (token == "(") {
            opStack.push(token);
        } else if (token == ")") {
            while (!opStack.empty() && opStack.top() != "(") {
                postfixList.push_back(opStack.top());
                opStack.pop();
            }
            opStack.pop();
        } else {
            while (!opStack.empty() && prec[opStack.top()] >= prec[token]) {
                postfixList.push_back(opStack.top());
                opStack.pop();
            }
            opStack.push(token);
        }
    }
    while (!opStack.empty()) {
        postfixList.push_back(opStack.top());
        opStack.pop();
    }
    string result = "";
    for (unsigned i = 0; i < postfixList.size(); i++) {
        if (i > 0) result += " ";
        result += postfixList[i];
    }
    return result;
}'''

I2P_MAIN = '''#include <iostream>
#include "pythonds3/cppds/expression.hpp"   // infixToPostfix, postfixEval, doMath
using namespace std;

int main() {
    cout << infixToPostfix("A * B + C * D") << endl;
    cout << infixToPostfix("( A + B ) * C - ( D - E ) * ( F + G )") << endl;
    return 0;
}'''

DO_MATH = '''double doMath(string op, double op1, double op2) {
    if (op == "*") {
        return op1 * op2;
    } else if (op == "/") {
        return op1 / op2;
    } else if (op == "+") {
        return op1 + op2;
    } else {
        return op1 - op2;
    }
}'''

POSTFIX_EVAL_HEADER = '''double postfixEval(string postfixExpr) {
    stack<double> operandStack;
    stringstream ss(postfixExpr);
    string token;
    while (ss >> token) {
        if (isdigit(token[0])) {
            operandStack.push(stod(token));
        } else {
            double operand2 = operandStack.top(); operandStack.pop();
            double operand1 = operandStack.top(); operandStack.pop();
            operandStack.push(doMath(token, operand1, operand2));
        }
    }
    return operandStack.top();
}'''

POSTFIX_MAIN = '''#include <iostream>
#include "pythonds3/cppds/expression.hpp"   // doMath + postfixEval
using namespace std;

int main() {
    cout << postfixEval("7 8 + 3 2 + /") << endl;
    return 0;
}'''

CARET_EXERCISE = '''#include <iostream>
#include <stack>
#include <vector>
#include <map>
#include <sstream>
#include <string>
#include <cctype>
using namespace std;

string infixToPostfix(string infixExpr) {
    // Your code here: add support for the right-associative ^ operator

    return result;
}

int main() {
    cout << infixToPostfix("5 * 3 ^ ( 4 - 2 )") << endl;
    return 0;
}'''

CARET_SOLUTION = '''#include <iostream>
#include <stack>
#include <vector>
#include <map>
#include <sstream>
#include <string>
#include <cctype>
using namespace std;

string infixToPostfix(string infixExpr) {
    map<string, int> prec = {{"^", 4}, {"*", 3}, {"/", 3}, {"+", 2}, {"-", 2}, {"(", 1}};
    stack<string> opStack;
    vector<string> postfixList;
    stringstream ss(infixExpr);
    string token;
    while (ss >> token) {
        if (isalnum(token[0])) {
            postfixList.push_back(token);
        } else if (token == "(") {
            opStack.push(token);
        } else if (token == ")") {
            while (!opStack.empty() && opStack.top() != "(") {
                postfixList.push_back(opStack.top());
                opStack.pop();
            }
            opStack.pop();
        } else {
            // ^ is right-associative: an equal ^ on the stack must wait
            while (!opStack.empty() &&
                   (prec[opStack.top()] > prec[token] ||
                    (prec[opStack.top()] == prec[token] && token != "^"))) {
                postfixList.push_back(opStack.top());
                opStack.pop();
            }
            opStack.push(token);
        }
    }
    while (!opStack.empty()) {
        postfixList.push_back(opStack.top());
        opStack.pop();
    }
    string result = "";
    for (unsigned i = 0; i < postfixList.size(); i++) {
        if (i > 0) result += " ";
        result += postfixList[i];
    }
    return result;
}

int main() {
    cout << infixToPostfix("5 * 3 ^ ( 4 - 2 )") << endl;
    cout << infixToPostfix("2 ^ 3 ^ 2") << endl;
    return 0;
}'''

# ---------------------------------------------------------------- queue
STL_QUEUE_SNIPPET = '''#include <queue>

std::queue<std::string> q;
q.push("first");
q.push("second");
std::cout << q.front(); // first
q.pop();                // removes first; returns void'''

STL_QUEUE = '''#include <iostream>
#include <queue>
#include <string>
using namespace std;

int main() {
    queue<string> q;
    q.push("4"); q.push("dog"); q.push("true");
    cout << q.size() << endl;
    cout << boolalpha << q.empty() << endl;
    cout << q.front() << endl;
    q.pop();
    cout << q.front() << endl;
}'''

QUEUE_HPP = '''template <typename T>
class Queue {
    private:
        vector<T> items;
    public:
        bool isEmpty() { return items.empty(); }
        void enqueue(T item) { items.insert(items.begin(), item); }
        T dequeue() { T front = items.back(); items.pop_back(); return front; }
        int size() { return items.size(); }
};'''

HOT_POTATO = '''#include <iostream>
#include <queue>
#include <vector>
using namespace std;

// STL queue: front() reads, pop() removes (returns nothing)
string hotPotato(vector<string> nameList, int num) {
    queue<string> simQueue;
    for (string name : nameList) simQueue.push(name);
    while (simQueue.size() > 1) {
        for (int i = 0; i < num; i++) {
            simQueue.push(simQueue.front());
            simQueue.pop();
        }
        simQueue.pop();
    }
    return simQueue.front();
}

int main() {
    cout << hotPotato({"Bill", "David", "Susan", "Jane", "Kent", "Brad"}, 7) << endl;
    return 0;
}'''

HOT_POTATO_COURSE = '''#include <iostream>
#include <string>
#include <vector>
#include "pythonds3/cppds/queue.hpp"   // Queue<T>: enqueue / dequeue / isEmpty / size
using namespace std;

string hotPotato(vector<string> nameList, int num) {
    Queue<string> simQueue;
    for (string name : nameList) simQueue.enqueue(name);   // push    -> enqueue
    while (simQueue.size() > 1) {
        for (int i = 0; i < num; i++) {
            simQueue.enqueue(simQueue.dequeue());          // front + pop -> dequeue
        }
        simQueue.dequeue();                                // value not needed
    }
    return simQueue.dequeue();                             // the only one left
}

int main() {
    cout << hotPotato({"Bill", "David", "Susan", "Jane", "Kent", "Brad"}, 7) << endl;
    return 0;
}'''

HOT_POTATO_TRACE = '''#include <iostream>
#include <queue>
#include <vector>
using namespace std;

// hotPotato with one extra line: print who leaves the circle in each round
string hotPotato(vector<string> nameList, int num) {
    queue<string> simQueue;
    for (string name : nameList) simQueue.push(name);
    while (simQueue.size() > 1) {
        for (int i = 0; i < num; i++) {
            simQueue.push(simQueue.front());
            simQueue.pop();
        }
        cout << "out: " << simQueue.front() << endl;
        simQueue.pop();
    }
    return simQueue.front();
}

int main() {
    string winner = hotPotato({"Bill", "David", "Susan", "Jane", "Kent", "Brad"}, 7);
    cout << "winner: " << winner << endl;
    return 0;
}'''

# ---------------------------------------------------------------- printer simulation
PRINTER_CLASS = '''class Printer {
    int pageRate;
    optional<Task> currentTask;
    double timeRemaining = 0;
public:
    explicit Printer(int ppm) : pageRate(ppm) {}
    bool busy() const { return currentTask.has_value(); }
    void startNext(const Task& task) {
        currentTask = task;
        timeRemaining = task.getPages() * 60.0 / pageRate;
    }
    void tick() {
        if (currentTask && --timeRemaining <= 0) currentTask.reset();
    }
};'''

TASK_CLASS = '''class Task {
    int timestamp;
    int pages;
public:
    Task(int time, int pageCount) : timestamp(time), pages(pageCount) {}
    int getPages() const { return pages; }
    int waitTime(int now) const { return now - timestamp; }
};'''

PRINT_QUEUE = '''queue<Task> printQueue;
if (arrival(rng) == 180) printQueue.emplace(now, pages(rng));
if (!printer.busy() && !printQueue.empty()) {
    Task nextTask = printQueue.front();
    printQueue.pop();
    waits.push_back(nextTask.waitTime(now));
    printer.startNext(nextTask);
}'''

RANDOM_DEMO = '''#include <iostream>
#include <random>
using namespace std;

int main() {
    mt19937 rng(42);                                  // engine with a fixed seed
    uniform_int_distribution<int> pages(1, 20);       // 1..20, equally likely
    uniform_int_distribution<int> arrival(1, 180);    // 1..180, equally likely
    for (int i = 0; i < 5; ++i) cout << pages(rng) << " ";
    cout << endl;
    int created = 0;
    for (int now = 0; now < 3600; ++now)
        if (arrival(rng) == 180) ++created;
    cout << "tasks in one hour: " << created << endl;
    return 0;
}'''

SIMULATION = '''#include <iostream>
#include <optional>
#include <queue>
#include <random>
#include <vector>
using namespace std;

class Task {
    int timestamp;
    int pages;
public:
    Task(int time, int pageCount) : timestamp(time), pages(pageCount) {}
    int getPages() const { return pages; }
    int waitTime(int now) const { return now - timestamp; }
};

class Printer {
    int pageRate;
    optional<Task> currentTask;
    double timeRemaining = 0;
public:
    explicit Printer(int ppm) : pageRate(ppm) {}
    bool busy() const { return currentTask.has_value(); }
    void startNext(const Task& task) {
        currentTask = task;
        timeRemaining = task.getPages() * 60.0 / pageRate;
    }
    void tick() {
        if (currentTask && --timeRemaining <= 0) currentTask.reset();
    }
};

void simulation(int seconds, int ppm, mt19937& rng) {
    uniform_int_distribution<int> arrival(1, 180), pages(1, 20);
    Printer printer(ppm);
    queue<Task> tasks;
    vector<int> waits;
    for (int now = 0; now < seconds; ++now) {
        if (arrival(rng) == 180) tasks.emplace(now, pages(rng));
        if (!printer.busy() && !tasks.empty()) {
            Task nextTask = tasks.front();
            tasks.pop();
            waits.push_back(nextTask.waitTime(now));
            printer.startNext(nextTask);
        }
        printer.tick();
    }
    double total = 0;
    for (int wait : waits) total += wait;
    cout << "average wait = " << (waits.empty() ? 0 : total / waits.size())
         << ", tasks remaining = " << tasks.size() << endl;
}

int main() {
    mt19937 rng(42);
    simulation(3600, 5, rng);
    simulation(3600, 10, rng);
}'''

SIMULATION_TRIALS_MAIN = '''int main() {
    mt19937 rng(42);
    cout << "5 pages per minute" << endl;
    for (int i = 0; i < 10; ++i) simulation(3600, 5, rng);
    cout << "10 pages per minute" << endl;
    for (int i = 0; i < 10; ++i) simulation(3600, 10, rng);
}'''

SIMULATION_TRIALS = SIMULATION[:SIMULATION.index('int main() {')] + SIMULATION_TRIALS_MAIN

# ---------------------------------------------------------------- deque
STL_DEQUE_SNIPPET = '''#include <deque>

std::deque<int> d;
d.push_front(2);
d.push_back(7);
int first = d.front();
d.pop_front();
int last = d.back();
d.pop_back();'''

DEQUE_HPP = '''template <typename T>
class Deque {
    private:
        vector<T> items;
    public:
        bool isEmpty() { return items.empty(); }
        void addFront(T item) { items.push_back(item); }
        void addRear(T item) { items.insert(items.begin(), item); }
        T removeFront() { T front = items.back(); items.pop_back(); return front; }
        T removeRear() { T rear = items.front(); items.erase(items.begin()); return rear; }
        int size() { return items.size(); }
};'''

PAL_CHECKER = '''#include <iostream>
#include <deque>
#include <string>
using namespace std;

bool palChecker(string aString) {
    deque<char> charDeque;
    for (char ch : aString) charDeque.push_back(ch);   // add to the rear
    while (charDeque.size() > 1) {
        char first = charDeque.front(); charDeque.pop_front();
        char last = charDeque.back(); charDeque.pop_back();
        if (first != last) return false;
    }
    return true;
}

int main() {
    cout << boolalpha;
    cout << palChecker("lsdkjfskf") << endl;   // false
    cout << palChecker("radar") << endl;       // true
    return 0;
}'''

PROGRAMS = {
    'stl_stack': STL_STACK, 'stack2_main': STACK2_MAIN, 'rev_solution': REV_SOLUTION,
    'par_checker': PAR_CHECKER, 'balance_checker': BALANCE_CHECKER,
    'divide_by_2': DIVIDE_BY_2, 'base_converter': BASE_CONVERTER,
    'i2p_main': I2P_MAIN, 'postfix_main': POSTFIX_MAIN, 'caret_solution': CARET_SOLUTION,
    'stl_queue': STL_QUEUE, 'hot_potato': HOT_POTATO, 'hot_potato_trace': HOT_POTATO_TRACE,
    'hot_potato_course': HOT_POTATO_COURSE,
    'random_demo': RANDOM_DEMO, 'simulation': SIMULATION, 'simulation_trials': SIMULATION_TRIALS,
    'pal_checker': PAL_CHECKER,
}

OUTPUT = {
    'stl_stack': '3\nfalse\ntrue\ndog',
    'stack2_main': 'true\n7.5\n3\n2\n7.5\n1',
    'rev_solution': 'USYSN',
    'par_checker': 'true\ntrue\nfalse\nfalse',
    'balance_checker': 'true\nfalse',
    'divide_by_2': '101010 11111',
    'base_converter': '11001 19',
    'i2p_main': 'A B * C D * +\nA B + C * D E - F G + * -',
    'postfix_main': '3',
    'caret_solution': '5 3 4 2 - ^ *\n2 3 2 ^ ^',
    'stl_queue': '3\nfalse\n4\ndog',
    'hot_potato': 'Susan',
    'hot_potato_trace': 'out: David\nout: Kent\nout: Jane\nout: Bill\nout: Brad\nwinner: Susan',
    'hot_potato_course': 'Susan',
    'random_demo': '8 16 20 4 15 \ntasks in one hour: 21',
    'simulation': 'average wait = 37.3, tasks remaining = 1\naverage wait = 34.45, tasks remaining = 0',
    'simulation_trials': '5 pages per minute\naverage wait = 37.3, tasks remaining = 1\naverage wait = 95.8889, tasks remaining = 2\naverage wait = 119.579, tasks remaining = 0\naverage wait = 173.72, tasks remaining = 0\naverage wait = 48.7222, tasks remaining = 0\naverage wait = 77.95, tasks remaining = 0\naverage wait = 245, tasks remaining = 0\naverage wait = 69.6087, tasks remaining = 0\naverage wait = 135.778, tasks remaining = 3\naverage wait = 43.3333, tasks remaining = 0\n10 pages per minute\naverage wait = 107.424, tasks remaining = 0\naverage wait = 7.31579, tasks remaining = 0\naverage wait = 19.8462, tasks remaining = 0\naverage wait = 11.6875, tasks remaining = 0\naverage wait = 5.55556, tasks remaining = 0\naverage wait = 4.375, tasks remaining = 0\naverage wait = 13.1667, tasks remaining = 0\naverage wait = 9.94737, tasks remaining = 0\naverage wait = 42.7, tasks remaining = 0\naverage wait = 11.3333, tasks remaining = 0',
    'pal_checker': 'false\ntrue',
}
