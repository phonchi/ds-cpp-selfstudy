#!/usr/bin/env python3
"""linear_structures.html 完整自學充實。冪等。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib import card, ensure_style, insert_end_of_section

PAGE = Path.home() / "ds-cpp-selfstudy/linear_structures.html"
s = PAGE.read_text()
s = ensure_style(s)

base = f'''<h3 id="dx-base">講義完整實作：從虛擬碼到 C++</h3>
{card("講義 05 · divideBy2 與萬用 baseConverter", """#include <iostream>
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
    cout << divideBy2(42) << " " << divideBy2(31) << endl;
    cout << baseConverter(25, 2) << " " << baseConverter(25, 16) << endl;
    return 0;
}""",
"101010 11111\\n11001 19",
note="兩個函式的骨架一模一樣：餘數進 stack、商繼續除、最後把 stack 倒出來。baseConverter 只多了一張 digits 對照表，base 16 的餘數 10~15 才印得出 A~F。")}'''
s, c1 = insert_end_of_section(s, "base", base, 'id="dx-base"')

infix = f'''<h3 id="dx-infix">講義完整實作：轉換器與求值器的 C++ 全文</h3>
{card("講義 05 · infixToPostfix 完整程式（pythonds3/cppds/expression.hpp）", """string infixToPostfix(string infixExpr) {
    map<string, int> prec = {{"*", 3}, {"/", 3}, {"+", 2}, {"-", 2}, {"(", 1}};
    stack<string> opStack;
    vector<string> postfixList;
    stringstream ss(infixExpr);
    string token;
    while (ss >> token) {
        if (isalnum(token[0])) {
            postfixList.push_back(token);        // 運算元直接輸出
        } else if (token == "(") {
            opStack.push(token);
        } else if (token == ")") {
            while (!opStack.empty() && opStack.top() != "(") {
                postfixList.push_back(opStack.top());
                opStack.pop();
            }
            opStack.pop();                       // 丟掉那個 "("
        } else {
            // 優先級 >= 自己的都先請出來
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
}""",
None,
note="prec 表把「(」設成最低的 1 是關鍵巧思：左括號躺在 stack 裡時，誰都「贏不過」它，自然不會被提前彈出。整段程式就是上面互動動畫的逐行文字版。")}
{card("講義 05 · 轉換器使用畫面", """#include <iostream>
#include "expression.hpp"
using namespace std;

int main() {
    cout << infixToPostfix("A * B + C * D") << endl;
    cout << infixToPostfix("( A + B ) * C - ( D - E ) * ( F + G )") << endl;
    return 0;
}""",
"A B * C D * +\\nA B + C * D E - F G + * -",
note="注意 token 之間要有空白（程式用 stringstream 以空白切 token）。第二條把五組括號全部「編譯」掉了：後序完全不需要括號。")}
<div class="deck-extra">
  <div class="dx-label">講義 05 · A * B + C * D 逐 token 追蹤</div>
  <table style="width:100%;border-collapse:collapse;font-size:.86rem;font-family:'JetBrains Mono',monospace;">
    <tr style="border-bottom:2px solid var(--card-border);"><th style="text-align:left;padding:.35rem;">token</th><th style="text-align:left;">opStack（頂在右）</th><th style="text-align:left;">輸出串</th></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.35rem;">A</td><td></td><td>A</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.35rem;">*</td><td>*</td><td>A</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.35rem;">B</td><td>*</td><td>A B</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.35rem;">+</td><td>+&nbsp;&nbsp;<span style="color:var(--muted)">← * 優先級較高，先彈出</span></td><td>A B *</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.35rem;">C</td><td>+</td><td>A B * C</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.35rem;">*</td><td>+ *&nbsp;&nbsp;<span style="color:var(--muted)">← * 比 + 高，疊上去</span></td><td>A B * C</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.35rem;">D</td><td>+ *</td><td>A B * C D</td></tr>
    <tr><td style="padding:.35rem;">收尾</td><td><span style="color:var(--muted)">全部倒出</span></td><td>A B * C D * +</td></tr>
  </table>
</div>
{card("講義 05 · postfixEval 完整程式", """double doMath(string op, double op1, double op2) {
    if (op == "*") return op1 * op2;
    else if (op == "/") return op1 / op2;
    else if (op == "+") return op1 + op2;
    else return op1 - op2;
}

double postfixEval(string postfixExpr) {
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
}

int main() {
    cout << postfixEval("7 8 + 3 2 + /") << endl;
    return 0;
}""",
"3",
note="彈出順序是天大的事：<strong>先彈出的是 operand2（右運算元）</strong>。加法乘法看不出差別，除法減法一交換就錯：7 8 + 3 2 + / 是 15 ÷ 5 = 3，弄反就變 1/3。")}
{card("講義 05 · 課後練習：讓 ^ 右結合", """string infixToPostfix(string infixExpr) {
    // 你的程式碼：加入次方運算子 ^（優先級最高、右結合）
    // 提示：右結合代表「同優先級不彈出」，
    //       prec[opStack.top()] >= prec[token] 的 >= 要對 ^ 改成 >
    return result;
}

int main() {
    cout << infixToPostfix("5 * 3 ^ ( 4 - 2 )") << endl;
    return 0;
}""",
"5 3 4 2 - ^ *", out_label="完成後的預期輸出",
note="右結合是指 2 ^ 3 ^ 2 = 2 ^ (3 ^ 2) = 512，不是 (2 ^ 3) ^ 2 = 64。只改優先級不夠，還得改「同級要不要彈」的判斷。")}'''
s, c2 = insert_end_of_section(s, "infix", infix, 'id="dx-infix"')

dq = f'''{card("講義 05 · palChecker 的 C++ 全文", """#include <iostream>
#include <deque>
#include <string>
using namespace std;

bool palChecker(string aString) {
    deque<char> charDeque;
    for (char ch : aString) charDeque.push_back(ch);   // 全部從尾端進
    while (charDeque.size() > 1) {
        char first = charDeque.front(); charDeque.pop_front();
        char last = charDeque.back(); charDeque.pop_back();
        if (first != last) return false;
    }
    return true;
}

int main() {
    cout << boolalpha;
    cout << palChecker("lsdkjfskf") << endl;
    cout << palChecker("radar") << endl;
    return 0;
}""",
"false\\ntrue",
note='<span id="dx-dq"></span>while 條件是 size() &gt; 1 而不是 !empty()：剩一個字元（奇數長度的中點）不用比，它自己跟自己一定相等。兩端各取一個、兩邊往中間夾，deque 兩端 O(1) 的能力在這裡剛好用滿。')}'''
s, c3 = insert_end_of_section(s, "deque", dq, 'id="dx-dq"')

PAGE.write_text(s)
print("inserted:", [n for n, ok in zip("base infix deque".split(), [c1, c2, c3]) if ok])
