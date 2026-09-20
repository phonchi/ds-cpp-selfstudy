#include <iostream>
#include <iomanip>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <unordered_map>
#include "pythonds3/cppds/dstimer.hpp"
using namespace std;
int main() {
    cout << setw(10) << "n" << setw(12) << "vector" << setw(12) << "hash" << endl;
 for (int n : {100'000, 200'000, 400'000, 800'000}) {
        vector<int> v(n);
        unordered_map<int, int> m;
 for (int i = 0; i < n; i++) { v[i] = i; m[i] = 0; }
 int target = rand() % (2 * n), hits = 0;
 
        DSTimer t1;
 for (int r = 0; r < 100; r++)
            hits += (find(v.begin(), v.end(), target) != v.end());
 double tv = t1.millis();
        DSTimer t2;
 for (int r = 0; r < 100; r++)
            hits += (m.find(target) != m.end());
        cout << setw(10) << n << fixed << setprecision(3)
             << setw(12) << tv << setw(12) << t2.millis() << endl;}
}
