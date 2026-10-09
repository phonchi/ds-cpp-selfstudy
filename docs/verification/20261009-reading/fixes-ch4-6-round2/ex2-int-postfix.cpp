// EXERCISE 2 check: evaluate "10 3 5 * 16 4 - / +" with int operands (integer division).
#include <iostream>
#include <sstream>
#include <stack>
#include <string>
using namespace std;

int postfixEvalInt(const string& expr) {
    stack<int> operandStack;
    istringstream in(expr);
    string token;
    while (in >> token) {
        if (isdigit(static_cast<unsigned char>(token[0]))) {
            operandStack.push(stoi(token));
        } else {
            int operand2 = operandStack.top(); operandStack.pop();
            int operand1 = operandStack.top(); operandStack.pop();
            int r = token == "+" ? operand1 + operand2
                  : token == "-" ? operand1 - operand2
                  : token == "*" ? operand1 * operand2
                  : operand1 / operand2;
            cout << operand1 << ' ' << token << ' ' << operand2 << " = " << r << '\n';
            operandStack.push(r);
        }
    }
    return operandStack.top();
}

int main() {
    int result = postfixEvalInt("10 3 5 * 16 4 - / +");
    cout << "result = " << result << '\n';
}
