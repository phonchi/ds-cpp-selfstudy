#!/usr/bin/env python3
"""recursion.html 完整自學充實。冪等。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib import card, ensure_style, insert_end_of_section

PAGE = Path.home() / "ds-cpp-selfstudy/recursion.html"
s = PAGE.read_text()
s = ensure_style(s)

fr = f'''<h3 id="dx-fr">講義完整範例：用 stack 模擬遞迴、用 depth 看見遞迴</h3>
{card("講義 06 · 遞迴拿掉、換成自己管理的 stack", """#include <iostream>
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

int main() { cout << toStr(1453, 16) << endl; }""",
"5AD",
note="這版沒有遞迴：自己開一個 stack 存餘數字元、最後倒出來。它證明了一件事：<strong>遞迴版其實是把同一個 stack 藏進了「呼叫堆疊」</strong>，每一層呼叫的區域變數就是一格 stack frame。")}
{card("講義 06 · 印出深度，親眼看呼叫堆疊長高", """#include <iostream>
#include <string>
#include <cstdio>
using namespace std;

int depth = 0;   // 明著追蹤遞迴深度

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
}""",
"  depth=1, n=10\\n  depth=2, n=5\\n  depth=3, n=2\\n  depth=4, n=1\\n1010",
note="深度一路長到 4：n 每除一次 2 就多一層 frame。最深那層（n=1）先回傳「1」，然後一路「回程」把餘數黏在後面，1010 是回程時由左往右組出來的。")}'''
s, c1 = insert_end_of_section(s, "frames", fr, 'id="dx-fr"')

hn = f'''{card("講義 06 · moveTower 完整程式與 3 層塔的輸出", """#include <iostream>
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

int main() { moveTower(3, "A", "B", "C"); }""",
"moving disk from A to B\\nmoving disk from A to C\\nmoving disk from B to C\\nmoving disk from A to B\\nmoving disk from C to A\\nmoving disk from C to B\\nmoving disk from A to B",
note='<span id="dx-hn"></span>7 行輸出 = 2³ − 1 步，跟理論下限一模一樣。注意基底情況是「height &lt; 1 什麼都不做」：它藏在 if 的反面，這種「隱形 base case」是遞迴的常見寫法。拿上面的互動動畫對照，每一行輸出對應一次圓盤移動。')}'''
s, c2 = insert_end_of_section(s, "hanoi", hn, 'id="dx-hn"')

mz = f'''{card("講義 06 · 迷宮主程式與輸出圖", """#include <iostream>
#include "maze.hpp"   // Maze 類別 + searchFrom（上面的完整列表）
using namespace std;

int main() {
    Maze myMaze("maze2.txt");
    searchFrom(myMaze, myMaze.startRow, myMaze.startCol);
    myMaze.print();   // O = 成功路徑，. = 試過，- = 死路
    return 0;
}""",
"++++++++++++++++++++++\\n+   +   ++ ++     +   \\n+ O +   ++ ++  +++ + ++\\n+ O +   ++ ++  +++   + \\n+ OOOOOOOO ++ OOO  + + \\n+++++ O +++++ O +++  + \\n+     O  ++  OO      + \\n+ +++++  ++ O ++++++ + \\n+ +   +  + OO ++  + + +\\n+++ +  +++ O +++    + +\\n++++++++++ O +++++++++", out_label="示範輸出（節錄；依 maze2.txt 而異）",
note='<span id="dx-mz"></span>O 是最後成功的那條路，點點是「試過但退回」的格子：遞迴回溯的痕跡全印在圖上。四個方向的 || 短路串接讓「找到一條就收工」，找不到才會把整片區域踩成點點。')}'''
s, c3 = insert_end_of_section(s, "maze", mz, 'id="dx-mz"')

PAGE.write_text(s)
print("inserted:", [n for n, ok in zip("frames hanoi maze".split(), [c1, c2, c3]) if ok])
