#include <algorithm>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <unordered_map>
#include <vector>
#include "dstimer.hpp"
using namespace std;

void check(bool condition) {
    if (!condition) throw runtime_error("benchmark correctness check failed");
}

int main() {
    cout << "experiment,method,n,repeat,operations,target,hits,total_ms\n";
    cout << setprecision(12);
    for (int trial = 0; trial < 7; ++trial) {
        // Reset once per trial, matching a fresh execution of the notebook.
        srand(1);
        for (int n : {100'000, 200'000, 400'000, 800'000}) {
            vector<int> v(n);
            unordered_map<int, int> m;
            for (int i = 0; i < n; i++) { v[i] = i; m[i] = 0; }
            int target = rand() % (2 * n), hits = 0;
            DSTimer t1;
            for (int r = 0; r < 100; r++)
                hits += (find(v.begin(), v.end(), target) != v.end());
            double tv = t1.millis();
            int vector_hits = hits;
            DSTimer t2;
            for (int r = 0; r < 100; r++)
                hits += (m.find(target) != m.end());
            double tm = t2.millis(); // Stop before formatting/output.
            check(vector_hits == (target < n ? 100 : 0));
            check(hits == 2 * vector_hits);
            cout << "lookup,std_find," << n << ',' << trial
                 << ",100," << target << ',' << vector_hits << ',' << tv << '\n';
            cout << "lookup,unordered_map_find," << n << ',' << trial
                 << ",100," << target << ',' << hits-vector_hits << ',' << tm << '\n';
        }
        for (int n = 2'500'000; n <= 10'000'000; n += 2'500'000) {
            vector<int> x(n);
            DSTimer te;
            for (int r = 0; r < 100; r++) x.erase(x.begin());
            double eraseT = te.millis();
            vector<int> y(n);
            DSTimer tp;
            for (int r = 0; r < 100; r++) y.pop_back();
            double popT = tp.millis();
            check(x.size() == size_t(n-100) && y.size() == size_t(n-100));
            check(all_of(x.begin(), x.end(), [](int v) { return v == 0; }));
            check(all_of(y.begin(), y.end(), [](int v) { return v == 0; }));
            cout << "pop,erase_begin," << n << ',' << trial << ",100,-1,-1," << eraseT << '\n';
            cout << "pop,pop_back," << n << ',' << trial << ",100,-1,-1," << popT << '\n';
        }
    }
    cerr << "PASS: 56 lookup hit counts and 56 vector final states verified.\n";
}
