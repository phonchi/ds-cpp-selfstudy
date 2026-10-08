#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;
long calls=0;
int makeChange1(vector<int> coinDenoms, int change) {
    calls++;
    if (find(coinDenoms.begin(), coinDenoms.end(), change) != coinDenoms.end()) return 1;
    int minCoins = INT_MAX;
    for (int i : coinDenoms) if (i <= change) { int numCoins = 1 + makeChange1(coinDenoms, change - i); minCoins = min(numCoins, minCoins);}
    return minCoins;
}
long calls2=0;
int makeChange2(const vector<int>& coins, int change, vector<int>& knownResults) {
    calls2++;
    int minCoins = change;
    for (int coin : coins) {
        if (coin == change) { knownResults[change] = 1; return 1; }
        else if (knownResults[change] > 0) return knownResults[change];
    }
    for (int coin : coins) if (coin <= change) {
        int candidate = 1 + makeChange2(coins, change - coin, knownResults);
        if (candidate < minCoins) { minCoins = candidate; knownResults[change] = minCoins; }
    }
    return minCoins;
}
int main(){
  for (int c : {15, 26, 11, 63}) { calls=0; int r=makeChange1({1,5,10,25}, c); cout<<c<<": "<<r<<" calls "<<calls<<endl; }
  vector<int> k(64,0); cout<<makeChange2({1,5,10,25},63,k)<<" calls2 "<<calls2<<endl;
  for(int i=0;i<64;i++) cout<<k[i]<<" "; cout<<endl;
  vector<int> k2(27,0); calls2=0; cout<<makeChange2({1,5,10,25},26,k2)<<" calls2 26: "<<calls2<<endl;
}
