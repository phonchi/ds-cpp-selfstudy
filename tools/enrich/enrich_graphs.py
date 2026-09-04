#!/usr/bin/env python3
"""graphs.html 完整自學充實。冪等。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib import card, ensure_style, insert_end_of_section

PAGE = Path.home() / "ds-cpp-selfstudy/graphs.html"
s = PAGE.read_text()
s = ensure_style(s)

rep = f'''<h3 id="dx-rep">講義完整範例：Graph 類別的使用畫面</h3>
{card("講義 08 · 建頂點、加邊、走訪相鄰串列", """#include <iostream>
#include "graph.hpp"   // Vertex + Graph（上面的完整列表）
using namespace std;

int main() {{
    Graph g;
    g.addEdge("0","1",5); g.addEdge("0","5",2); g.addEdge("1","2",4);
    g.addEdge("2","3",9); g.addEdge("3","4",7); g.addEdge("3","5",3);
    g.addEdge("4","0",1); g.addEdge("5","4",8); g.addEdge("5","2",1);

    for (auto& p : g.vertices)
        for (auto& n : p.second.neighbors)
            cout << "(" << p.first << "," << n.first << "," << n.second << ") ";
    cout << endl;
    return 0;
}}""".replace("{{","{").replace("}}","}"),
"(0,1,5) (0,5,2) (1,2,4) (2,3,9) (3,4,7) (3,5,3) (4,0,1) (5,2,1) (5,4,8) ",
note="每組 (from, to, weight) 對應一條有向邊。addEdge 會補上不存在的頂點；setVertex 對既有 key 是 no-op，不會清掉 edges/state。ordered map 查頂點為 O(log |V|)、查特定鄰邊為 O(log deg(v))。")}'''
s, c1 = insert_end_of_section(s, "representation", rep, 'id="dx-rep"')

bfs = f'''<h3 id="dx-bfs">講義完整範例：Word Ladder 的實際執行</h3>
{card("講義 08 · bfs + traverse：從 fool 爬到 sage", """#include <iostream>
#include "graph_algos.hpp"   // buildGraph + bfs + traverse
using namespace std;

int main() {{
    Graph g = buildGraph({{"fool", "cool", "pool", "poll", "pole",
                         "pall", "fall", "fail", "foil", "foul",
                         "pope", "pale", "sale", "sage", "page"}});
    bfs(g, "fool");
    traverse(g, "sage");                 // 沿 previous 指標回溯
    for (auto& p : g.vertices)           // 單字（與 fool 的距離）
        cout << p.first << "(" << p.second.distance << ") ";
    cout << endl;
    return 0;
}}""".replace("{{","{").replace("}}","}"),
"sage->sale->pale->pall->poll->pool->fool\\ncool(1) fail(2) fall(3) foil(1) fool(0) foul(1) page(5) pale(4) pall(3) pole(3) poll(2) pool(1) pope(4) sage(6) sale(5)", out_label="示範執行（回溯路徑可能因探索順序略異，長度必為 6 步）",
note="每次 bfs 前會先重設全部 color、previous，並把 distance 設為 INT_MAX；起點在 enqueue 前標 gray。traverse 印 previous 鏈，任何可達單字回溯到 fool 都是最短路。")}'''
s, c2 = insert_end_of_section(s, "bfs", bfs, 'id="dx-bfs"')

dfs = f'''{card("講義 08 · DFSGraph：discovery / closing time 全表", """#include <iostream>
#include "graph_algos.hpp"   // DFSGraph（上面的完整列表）
using namespace std;

int main() {{
    DFSGraph g;
    g.addEdge("A", "B");  g.addEdge("B", "C");
    g.addEdge("A", "D");  g.addEdge("B", "D");
    g.addEdge("D", "E");  g.addEdge("E", "B");
    g.addEdge("E", "F");  g.addEdge("F", "C");
    g.dfs();
    printf("%4s|%9s|%8s|%9s\\n", "Key", "Discover", "Closing", "Previous");
    for (auto& p : g.vertices)
        printf("%4s|%9d|%8d|%9s\\n", p.first.c_str(),
               g.discovery[p.first], g.closing[p.first], p.second.previous.c_str());
    return 0;
}}""".replace("{{","{").replace("}}","}"),
" Key| Discover| Closing| Previous\\n   A|        1|      12|         \\n   B|        2|      11|        A\\n   C|        3|       4|        B\\n   D|        5|      10|        B\\n   E|        6|       9|        D\\n   F|        7|       8|        E",
note='<span id="dx-dfs"></span>對照括號性質：C 的 [3,4] 完全包在 B 的 [2,11] 裡（C 是 B 的子孫）；每個頂點的區間要嘛互相包住、要嘛完全分開，絕不交錯。E→B 那條邊指向還是灰色的祖先，是一條 back edge：它宣告圖裡有循環。')}'''
s, c3 = insert_end_of_section(s, "dfs", dfs, 'id="dx-dfs"')

dij = f'''{card("講義 08 · dijkstra + findPath 的使用畫面", """#include <iostream>
#include "graph_algos.hpp"   // dijkstra + findPath
using namespace std;

int main() {{
    Graph g;   // 講義的 6 頂點範例圖（雙向邊）
    g.addEdge("u","v",2); g.addEdge("v","u",2); g.addEdge("v","w",3); g.addEdge("w","v",3);
    g.addEdge("w","z",5); g.addEdge("z","w",5); g.addEdge("u","x",1); g.addEdge("x","u",1);
    g.addEdge("u","w",5); g.addEdge("w","u",5); g.addEdge("x","v",2); g.addEdge("v","x",2);
    g.addEdge("x","w",3); g.addEdge("w","x",3); g.addEdge("x","y",1); g.addEdge("y","x",1);
    g.addEdge("y","w",1); g.addEdge("w","y",1); g.addEdge("y","z",1); g.addEdge("z","y",1);

    dijkstra(g, "u");
    for (auto& p : g.vertices)   // 頂點: 距離 (previous)
        cout << p.first << ": " << p.second.distance
             << " (" << p.second.previous << ")" << endl;
    for (string v : findPath(g, "u", "z")) cout << v << " ";
    cout << endl;
    return 0;
}}""".replace("{{","{").replace("}}","}"),
"u: 0 ()\\nv: 2 (u)\\nw: 3 (y)\\nx: 1 (u)\\ny: 2 (x)\\nz: 3 (y)\\nu x y z ",
note='<span id="dx-dij"></span>w 的直達候選是 5，最後下修為 3（u→x→y→w）。lazy PQ 會 push 新的 (3,w)，舊的 (5,w) 出列時因 stale 被略過；不需要在 heap 中搜尋並 decrease-key。u 到 z 的最短路是 u x y z，總長 3。')}'''
s, c4 = insert_end_of_section(s, "dijkstra", dij, 'id="dx-dij"')

prm = f'''{card("講義 08 · prim 的使用畫面：長出 MST", """#include <iostream>
#include "graph_algos.hpp"   // prim
using namespace std;

int main() {{
    Graph g;   // 講義的廣播範例圖（雙向邊）
    g.addEdge("A","B",2); g.addEdge("B","A",2); g.addEdge("A","C",3); g.addEdge("C","A",3);
    g.addEdge("B","D",1); g.addEdge("D","B",1); g.addEdge("B","C",1); g.addEdge("C","B",1);
    g.addEdge("B","E",4); g.addEdge("E","B",4); g.addEdge("D","E",1); g.addEdge("E","D",1);
    g.addEdge("C","F",5); g.addEdge("F","C",5); g.addEdge("E","F",1); g.addEdge("F","E",1);
    g.addEdge("F","G",1); g.addEdge("G","F",1);

    prim(g, "A");
    cout << "MST edges: ";
    for (auto& p : g.vertices)
        if (p.second.previous != "")
            cout << "(" << p.second.previous << "," << p.first << ") ";
    cout << endl;
    return 0;
}}""".replace("{{","{").replace("}}","}"),
"MST edges: (A,B) (B,C) (B,D) (D,E) (E,F) (F,G) ",
note='<span id="dx-prm"></span>六條邊總權重 7。每次選的是跨越「目前樹／樹外頂點」之 cut 的最小權重 safe edge。若圖不連通，課程 void prim() 會丟出 invalid_argument，不會靜默回傳 forest。')}'''
s, c5 = insert_end_of_section(s, "prim", prm, 'id="dx-prm"')

PAGE.write_text(s)
print("inserted:", [n for n,ok in zip("rep bfs dfs dij prim".split(),[c1,c2,c3,c4,c5]) if ok])
