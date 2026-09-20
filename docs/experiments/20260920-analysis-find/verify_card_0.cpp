#include <iomanip>
#include <iostream>
#include <vector>
#include "pythonds3/cppds/dstimer.hpp"
using namespace std;
 
void test1(int n) { vector<int> v; for (int i = n - 1; i >= 0; i--) v.insert(v.begin(), i); }
void test2(int n) { vector<int> v; for (int i = 0; i < n; i++) v.push_back(i); }
void test3(int n) { vector<int> v; v.reserve(n);
 for (int i = 0; i < n; i++) v.push_back(i); }
void test4(int n) { vector<int> v(n); for (int i = 0; i < n; i++) v[i] = i; }
 
int main() {
 void (*tests[])(int) = {test1, test2, test3, test4};
 const char* names[] = {"insert at front", "push_back", "with reserve", "direct index"};
 for (int k = 0; k < 4; k++) {
        DSTimer t;
 for (int r = 0; r < 1000; r++) tests[k](1000);
        cout << left << setw(16) << names[k] << right << setw(9)
             << fixed << setprecision(2) << t.millis()
             << " ms" << endl;
    }
}
