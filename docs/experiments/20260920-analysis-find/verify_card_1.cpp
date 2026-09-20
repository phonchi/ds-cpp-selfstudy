#include <iomanip>
#include <iostream>
#include <vector>
#include "pythonds3/cppds/dstimer.hpp"
using namespace std;
 
int main() {
    cout << left << setw(10) << "n" << right << setw(14) << "erase(begin)"  << setw(12) << "pop_back" << endl;
 for (int n = 2'500'000; n <= 10'000'000; n += 2'500'000) {
        vector<int> x(n);
        DSTimer te;
 for (int r = 0; r < 100; r++) x.erase(x.begin());
 double eraseT = te.millis();
        vector<int> y(n);
        DSTimer tp;
 for (int r = 0; r < 100; r++) y.pop_back();
        cout << left << setw(10) << n << right << fixed << setprecision(5)
             << setw(14) << eraseT << setw(12) << tp.millis() << endl;
    }
}
