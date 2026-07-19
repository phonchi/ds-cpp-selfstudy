#!/usr/bin/env python3
"""arrays.html 完整自學充實。冪等。"""
import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib import card, ensure_style, insert_end_of_section

PAGE = Path.home() / "ds-cpp-selfstudy/arrays.html"
s = PAGE.read_text()
s = ensure_style(s)
secs = re.findall(r'<section id="([a-z0-9]+)"', s)
print("sections:", secs)

low = f'''{card("講義 03 · sizeof 與位址親眼看", """using namespace std;
cout << sizeof(double) << " bytes per double" << endl;
cout << sizeof(int) << " bytes per int" << endl;
cout << sizeof(char) << " byte per char" << endl;

double data[6];
cout << sizeof(data) << " bytes for the whole array" << endl;
cout << &data[0] << " <- base address" << endl;
cout << &data[1] << " <- 8 bytes later" << endl;""",
"8 bytes per double\\n4 bytes per int\\n1 byte per char\\n48 bytes for the whole array\\n0x7ffcd3b1e2a0 <- base address\\n0x7ffcd3b1e2a8 <- 8 bytes later", out_label="示範執行（位址每次不同）",
note='<span id="dx-low"></span>兩個位址恰好差 8（十六進位 a0 → a8）：陣列元素<strong>連續</strong>排在記憶體裡，一格一個 double。整個陣列 6 × 8 = 48 bytes，一條 sizeof 全算得出來。')}'''
s, c1 = insert_end_of_section(s, secs[0], low, 'id="dx-low"')

comp = f'''{card("講義 03 · compact 與 referential 的空間帳", """using namespace std;
int primes[] = {2, 3, 5, 7, 11, 13, 17, 19};

cout << sizeof(primes[0]) << " bytes per element" << endl;
cout << sizeof(primes) << " bytes in total" << endl;
cout << sizeof(primes) / sizeof(primes[0]) << " elements" << endl;

string* names[3];   // referential array：3 根指標，各 8 bytes
cout << sizeof(names) << " bytes for three pointers" << endl;""",
"4 bytes per element\\n32 bytes in total\\n8 elements\\n24 bytes for three pointers",
note='<span id="dx-comp"></span>sizeof(陣列) / sizeof(第一個元素) 是經典的「元素個數」算法（只在原生陣列上有效，退化成指標後就失靈）。referential 版本存的是指標：資料本體另外住，陣列只付 3 × 8 bytes 的「門牌費」。')}'''
s, c2 = insert_end_of_section(s, secs[1] if len(secs) > 1 else "compact", comp, 'id="dx-comp"')

multi = f'''<h3 id="dx-multi">講義完整範例：二維陣列的每一種看法</h3>
{card("講義 03 · 宣告、走列、走行、看位址", """using namespace std;
int M[2][2] = {{1, 1}, {2, 2}};   // 巢狀大括號初始化

cout << "M has " << sizeof(M) / sizeof(M[0]) << " rows and "
     << sizeof(M[0]) / sizeof(M[0][0]) << " columns, "
     << sizeof(M) << " bytes in total" << endl;

for (int j = 0; j < 2; j++) cout << M[0][j] << " ";   // 第 0 列
cout << endl;
for (int i = 0; i < 2; i++) cout << M[i][0] << " ";   // 第 0 行
cout << endl;

cout << &M[0][0] << " " << &M[0][1] << endl;   // 差 4 bytes
cout << &M[1][0] << " " << &M[1][1] << endl;   // 下一列緊接著""",
"M has 2 rows and 2 columns, 16 bytes in total\\n1 1 \\n1 2 \\n0x7ffe013c4e50 0x7ffe013c4e54\\n0x7ffe013c4e58 0x7ffe013c4e5c", out_label="示範執行（位址每次不同）",
note="四個位址一路 +4：C++ 的二維陣列就是「一條連續記憶體」按 row-major 攤平。M[1][0] 緊跟在 M[0][1] 後面，中間沒有縫。")}
{card("講義 03 · 動手攤平：column-major 版", """using namespace std;
int flat[4];
int rows = 2, cols = 2;
int M[2][2] = {{1, 1}, {2, 2}};

for (int i = 0; i < rows; i++)
    for (int j = 0; j < cols; j++)
        flat[j * rows + i] = M[i][j];   // column-major：j*Rows + i

for (int k = 0; k < 4; k++) cout << flat[k] << " ";
cout << endl;""",
"1 2 1 2 ",
note="row-major 的攤平公式是 i*Cols + j；column-major 換成 j*Rows + i，一行一行直著放。輸出 1 2 1 2 就是「第 0 行、第 1 行」依序排開。")}
{card("講義 03 · 練習：用平面索引找 student[5][3]", """#include <cassert>
using namespace std;

int main() {
    int student[100][4];
    for (int i = 0; i < 100; i++)
        for (int j = 0; j < 4; j++) student[i][j] = i * 4 + j;
    int* s = &student[0][0];   // 把二維陣列當一維看
    // 把 ? 換成你的答案
    assert(student[5][3] == s[?]);
    cout << "Pass" << endl;
    return 0;
}""",
"Pass", out_label="填對之後的輸出",
note="row-major 公式 i*Cols + j = 5×4 + 3 = <strong>23</strong>。assert 是驗收利器：條件為假直接中止程式，考自己最誠實。")}'''
s, c3 = insert_end_of_section(s, "multidim" if "multidim" in secs else secs[2], multi, 'id="dx-multi"')

sp = f'''{card("講義 03 · SparseMatrix 使用畫面：加減乘一次看", """#include <iostream>
#include "sparsematrix.hpp"
using namespace std;

int main() {
    vector<vector<double>> denseMatrix = {{1, 0, 0}, {0, 2, 0}, {0, 0, 3}};
    SparseMatrix sparseMatrix;
    sparseMatrix.fromDenseMatrix(denseMatrix);
    cout << sparseMatrix << endl;

    SparseMatrix matrix1({{{0, 1}, 1}, {{1, 1}, 2}, {{2, 2}, 3}});
    SparseMatrix matrix2({{{1, 1}, 3}, {{2, 2}, 4}});

    cout << matrix1 + matrix2 << endl;
    cout << matrix1 - matrix2 << endl;
    cout << matrix1 * matrix2 << endl;
    return 0;
}""",
"(0, 0): 1  (1, 1): 2  (2, 2): 3  \\n(0, 1): 1  (1, 1): 5  (2, 2): 7  \\n(0, 1): 1  (1, 1): -1  (2, 2): -1  \\n(0, 1): 3  (1, 1): 6  (2, 2): 12  ",
note='<span id="dx-sp"></span>乘法那行值得慢讀：DOK 版本的矩陣乘法只要「A 的 (i, k) 遇上 B 的 (k, j)」才產生貢獻，兩層迴圈都只走<strong>非零元素</strong>。(0,1)×(1,1) 給 (0,1)：3；(1,1)×(1,1) 給 (1,1)：6；(2,2)×(2,2) 給 (2,2)：12。')}'''
s, c4 = insert_end_of_section(s, "sparse" if "sparse" in secs else secs[3], sp, 'id="dx-sp"')

PAGE.write_text(s)
print("inserted:", [n for n, ok in zip("low comp multi sparse".split(), [c1, c2, c3, c4]) if ok])
