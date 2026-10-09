#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

long calls1 = 0;   // how many times makeChange1 runs
long calls2 = 0; int enter[64];   // how many times makeChange2 runs

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
    calls2++; enter[change]++;
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
    cout<<"enter:";for(int i=0;i<=10;i++)cout<<" "<<enter[i];cout<<endl; return 0;
}