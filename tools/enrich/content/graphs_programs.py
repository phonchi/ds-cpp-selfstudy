"""Chapter 8 programs. Lecture listings are copied from 08_Graphs and Graphing Algorithms.ipynb;
HEADER_* come from pythonds3/cppds/graph.hpp and graph_algos.hpp. OUT holds the exact stdout."""

VERTEX_LECTURE = r'''class Vertex {
    public:
        string key;
        map<string, int> neighbors;   // neighbor key -> edge weight

        Vertex() {}
        Vertex(string k) {
            key = k;
        }

        int getNeighbor(string other) {
            if (neighbors.count(other)) {
                return neighbors[other];
            }
            return -1;   // no such edge
        }
        void setNeighbor(string other, int weight = 0) {
            neighbors[other] = weight;
        }
};'''

GRAPH_LECTURE = r'''class Graph {
    public:
        map<string, Vertex> vertices;

        void setVertex(string key) {
            if (vertices.count(key) == 0) vertices.emplace(key, Vertex(key));
        }
        void addEdge(string fromVert, string toVert, int weight = 0) {
            if (vertices.count(fromVert) == 0) setVertex(fromVert);
            if (vertices.count(toVert) == 0) setVertex(toVert);
            vertices[fromVert].neighbors[toVert] = weight;
        }
        bool contains(string key) {
            return vertices.count(key) > 0;
        }
};'''

BUILDGRAPH = r'''Graph buildGraph(vector<string> words) {
    map<string, set<string>> buckets;
    Graph theGraph;

    // create buckets of words that differ by one letter
    for (string word : words) {
        for (unsigned i = 0; i < word.length(); i++) {
            string bucket = word.substr(0, i) + "_" + word.substr(i + 1);
            buckets[bucket].insert(word);
        }
    }

    // add edges between different words in the same bucket
    for (auto& pair : buckets) {
        for (const string& word1 : pair.second) {
            for (const string& word2 : pair.second) {
                if (word1 != word2) {
                    theGraph.addEdge(word1, word2);
                }
            }
        }
    }
    return theGraph;
}'''

BFS_LECTURE = r'''void bfs(Graph& g, string startKey) {
    g.vertices[startKey].distance = 0;
    g.vertices[startKey].previous = "";
    queue<string> vertQueue;
    vertQueue.push(startKey);
    while (!vertQueue.empty()) {
        string currentKey = vertQueue.front();
        vertQueue.pop();
        Vertex& current = g.vertices[currentKey];
        for (auto& n : current.neighbors) {
            Vertex& neighbor = g.vertices[n.first];
            if (neighbor.color == "white") {
                neighbor.color = "gray";
                neighbor.distance = current.distance + 1;
                neighbor.previous = currentKey;
                vertQueue.push(n.first);
            }
        }
        current.color = "black";
    }
}'''

TRAVERSE = r'''void traverse(Graph& g, string startingKey) {
    string current = startingKey;
    while (current != "") {
        cout << current;
        if (g.vertices[current].previous != "") {
            cout << "->";
        }
        current = g.vertices[current].previous;
    }
    cout << endl;
}'''

KNIGHTGRAPH = r'''Graph knightGraph(int boardSize) {
    Graph ktGraph;
    for (int row = 0; row < boardSize; row++) {
        for (int col = 0; col < boardSize; col++) {
            int nodeId = row * boardSize + col;
            for (auto& move : genLegalMoves(row, col, boardSize)) {
                int otherNodeId = move.first * boardSize + move.second;
                ktGraph.addEdge(to_string(nodeId), to_string(otherNodeId));
            }
        }
    }
    return ktGraph;
}'''

GENLEGALMOVES = r'''vector<pair<int, int>> genLegalMoves(int row, int col, int boardSize) {
    vector<pair<int, int>> newMoves;
    vector<pair<int, int>> moveOffsets = {
        {-1, -2}, {-1, 2}, {-2, -1}, {-2, 1},
        {1, -2},  {1, 2},  {2, -1},  {2, 1}};
    for (auto& off : moveOffsets) {
        int newRow = row + off.first;
        int newCol = col + off.second;
        if (0 <= newRow && newRow < boardSize && 0 <= newCol && newCol < boardSize) {
            newMoves.push_back({newRow, newCol});
        }
    }
    return newMoves;
}'''

KNIGHTTOUR = r'''bool knightTour(int n, vector<string>& path, string uKey, int limit, Graph& g) {
    g.vertices[uKey].color = "gray";
    path.push_back(uKey);
    if (n < limit) {
        bool done = false;
        for (auto& nb : g.vertices[uKey].neighbors) {
            if (done) break;
            if (g.vertices[nb.first].color == "white") {
                done = knightTour(n + 1, path, nb.first, limit, g);
            }
        }
        if (!done) {   // prepare to backtrack
            path.pop_back();
            g.vertices[uKey].color = "white";
        }
        return done;
    }
    return true;
}'''

ORDERBYAVAIL = r'''vector<string> orderByAvail(Graph& g, string uKey) {
    vector<pair<int, string>> resList;
    for (auto& nb : g.vertices[uKey].neighbors) {
        if (g.vertices[nb.first].color == "white") {
            int c = 0;
            for (auto& w : g.vertices[nb.first].neighbors) {
                if (g.vertices[w.first].color == "white") {
                    c++;
                }
            }
            resList.push_back({c, nb.first});
        }
    }
    sort(resList.begin(), resList.end());   // fewest onward moves first
    vector<string> result;
    for (auto& p : resList) {
        result.push_back(p.second);
    }
    return result;
}'''

KNIGHTTOUR_W_LECTURE = r'''bool knightTour(int n, vector<string>& path, string uKey, int limit, Graph& g) {
    g.vertices[uKey].color = "gray";
    path.push_back(uKey);
    if (n < limit) {
        bool done = false;
        for (string nbKey : orderByAvail(g, uKey)) {   // Warnsdorff order
            if (done) break;
            if (g.vertices[nbKey].color == "white") {
                done = knightTour(n + 1, path, nbKey, limit, g);
            }
        }
        if (!done) {
            path.pop_back();
            g.vertices[uKey].color = "white";
        }
        return done;
    }
    return true;
}'''

DFSGRAPH = r'''class DFSGraph : public Graph {
    public:
        int time = 0;
        map<string, int> discovery;
        map<string, int> closing;

        void dfs() {
            for (auto& p : vertices) {
                p.second.color = "white";
                p.second.previous = "";
            }
            for (auto& p : vertices) {
                if (p.second.color == "white") {
                    dfsVisit(p.first);
                }
            }
        }'''

DFSVISIT = r'''    ...
        void dfsVisit(string startKey) {
            vertices[startKey].color = "gray";
            time = time + 1;
            discovery[startKey] = time;
            for (auto& n : vertices[startKey].neighbors) {
                if (vertices[n.first].color == "white") {
                    vertices[n.first].previous = startKey;
                    dfsVisit(n.first);
                }
            }
            vertices[startKey].color = "black";
            time = time + 1;
            closing[startKey] = time;
        }
};'''

DIJKSTRA = r'''void dijkstra(Graph& g, string startKey) {
    // min-heap of (distance, vertex key) pairs
    priority_queue<pair<int, string>,
                   vector<pair<int, string>>,
                   greater<pair<int, string>>> pq;
    g.vertices[startKey].distance = 0;
    pq.push({0, startKey});

    while (!pq.empty()) {
        auto [distance, currentKey] = pq.top();
        pq.pop();
        if (distance > g.vertices[currentKey].distance) {
            continue;   // stale entry - an older candidate superseded by a better one
        }
        for (auto& n : g.vertices[currentKey].neighbors) {
            int newDistance = g.vertices[currentKey].distance + n.second;
            if (newDistance < g.vertices[n.first].distance) {
                g.vertices[n.first].distance = newDistance;
                g.vertices[n.first].previous = currentKey;
                pq.push({newDistance, n.first});
            }
        }
    }
}'''

PRIM_A = r'''void prim(Graph& g, string startKey) {
    priority_queue<pair<int, string>,
                   vector<pair<int, string>>,
                   greater<pair<int, string>>> pq;
    set<string> inTree;

    for (auto& p : g.vertices) {
        p.second.distance = INT_MAX;
        p.second.previous = "";
    }
    g.vertices[startKey].distance = 0;
    pq.push({0, startKey});
    ...'''

PRIM_B = r'''    ...
    while (!pq.empty()) {
        auto [distance, currentKey] = pq.top();
        pq.pop();
        if (inTree.count(currentKey)) continue;   // stale entry
        inTree.insert(currentKey);
        for (auto& n : g.vertices[currentKey].neighbors) {
            int newDistance = n.second;   // edge weight only, not path length!
            if (!inTree.count(n.first) && newDistance < g.vertices[n.first].distance) {
                g.vertices[n.first].distance = newDistance;
                g.vertices[n.first].previous = currentKey;
                pq.push({newDistance, n.first});
            }
        }
    }
    if (inTree.size() != g.vertices.size())
        throw invalid_argument("Prim requires a connected graph");
}'''

SETVERTEX_MAIN = r'''#include <iostream>
#include "pythonds3/cppds/graph.hpp"   // Vertex, Graph (graph.hpp listing above)
using namespace std;

int main() {
    Graph g;
    for (int i = 0; i < 6; i++) {
        g.setVertex(to_string(i));
    }
    for (auto& p : g.vertices) {
        cout << "Vertex(" << p.first << ") ";
    }
    cout << endl;
    return 0;
}'''

ADDEDGE_MAIN = r'''#include <iostream>
#include "pythonds3/cppds/graph.hpp"
using namespace std;

int main() {
    Graph g;
    g.addEdge("0","1",5); g.addEdge("0","5",2); g.addEdge("1","2",4);
    g.addEdge("2","3",9); g.addEdge("3","4",7); g.addEdge("3","5",3);
    g.addEdge("4","0",1); g.addEdge("5","4",8); g.addEdge("5","2",1);

    for (auto& p : g.vertices)
        for (auto& n : p.second.neighbors)
            cout << "(" << p.first << "," << n.first << "," << n.second << ") ";
    cout << endl;
    return 0;
}'''

WL_TRAVERSE_MAIN = r'''#include <iostream>
#include "pythonds3/cppds/graph_algos.hpp"   // buildGraph + bfs + traverse
using namespace std;

int main() {
    Graph g = buildGraph({"fool", "cool", "pool", "poll", "pole",
                         "pall", "fall", "fail", "foil", "foul",
                         "pope", "pale", "sale", "sage", "page"});
    g.vertices["fool"].color = "gray";
    bfs(g, "fool");
    traverse(g, "sage");
    return 0;
}'''

WL_DIST_MAIN = r'''#include <iostream>
#include "pythonds3/cppds/graph_algos.hpp"
using namespace std;

int main() {
    Graph g = buildGraph({"fool", "cool", "pool", "poll", "pole",
                         "pall", "fall", "fail", "foil", "foul",
                         "pope", "pale", "sale", "sage", "page"});
    bfs(g, "fool");
    for (auto& p : g.vertices)   // word(distance from fool)
        cout << p.first << "(" << p.second.distance << ") ";
    cout << endl;
    return 0;
}'''

KT5_MAIN = r'''#include <iostream>
#include "pythonds3/cppds/graph_algos.hpp"   // genLegalMoves + knightGraph + knightTour
using namespace std;

int main() {
    // brute force: 5x5 board - 8x8 without the heuristic takes far too long!
    int boardSize = 5;
    Graph ktGraph = knightGraph(boardSize);
    vector<string> path;
    bool finished = knightTour(1, path, "0", boardSize * boardSize, ktGraph);
    if (finished) printBoard(path, boardSize);   // squares show the move number
    else cout << "No path found." << endl;
    return 0;
}'''

KT8_MAIN = r'''#include <iostream>
#include "pythonds3/cppds/graph_algos.hpp"   // orderByAvail + knightTourWarnsdorff
using namespace std;

int main() {
    int boardSize = 8;   // with the heuristic, 8x8 finishes instantly
    Graph ktGraph = knightGraph(boardSize);
    vector<string> path;
    bool finished = knightTourWarnsdorff(1, path, "0", boardSize * boardSize, ktGraph);
    if (finished) printBoard(path, boardSize);
    else cout << "No path found." << endl;
    return 0;
}'''

DFS_MAIN = r'''#include <iostream>
#include "pythonds3/cppds/graph_algos.hpp"   // DFSGraph: dfs, dfsVisit (DFSGraph listing above)
using namespace std;

int main() {
    DFSGraph g;
    g.addEdge("A", "B");  g.addEdge("B", "C");
    g.addEdge("A", "D");  g.addEdge("B", "D");
    g.addEdge("D", "E");  g.addEdge("E", "B");
    g.addEdge("E", "F");  g.addEdge("F", "C");
    g.dfs();
    printf("%4s|%9s|%8s|%9s\n", "Key", "Discover", "Closing", "Previous");
    for (auto& p : g.vertices)
        printf("%4s|%9d|%8d|%9s\n", p.first.c_str(),
               g.discovery[p.first], g.closing[p.first], p.second.previous.c_str());
    return 0;
}'''

DIJ_MAIN = r'''#include <iostream>
#include "pythonds3/cppds/graph_algos.hpp"   // dijkstra (dijkstra listing above)
using namespace std;

int main() {
    Graph g;
    g.addEdge("u","v",2); g.addEdge("v","u",2); g.addEdge("v","w",3); g.addEdge("w","v",3);
    g.addEdge("w","z",5); g.addEdge("z","w",5); g.addEdge("u","x",1); g.addEdge("x","u",1);
    g.addEdge("u","w",5); g.addEdge("w","u",5); g.addEdge("x","v",2); g.addEdge("v","x",2);
    g.addEdge("x","w",3); g.addEdge("w","x",3); g.addEdge("x","y",1); g.addEdge("y","x",1);
    g.addEdge("y","w",1); g.addEdge("w","y",1); g.addEdge("y","z",1); g.addEdge("z","y",1);
    dijkstra(g, "u");
    for (auto& p : g.vertices)   // key: distance (previous)
        cout << p.first << ": " << p.second.distance
             << " (" << p.second.previous << ")" << endl;
    return 0;
}'''

DIJ_PATH_MAIN = r'''#include <iostream>
#include "pythonds3/cppds/graph_algos.hpp"   // dijkstra + findPath
using namespace std;

int main() {
    Graph g;
    g.addEdge("u","v",2); g.addEdge("v","u",2); g.addEdge("v","w",3); g.addEdge("w","v",3);
    g.addEdge("w","z",5); g.addEdge("z","w",5); g.addEdge("u","x",1); g.addEdge("x","u",1);
    g.addEdge("u","w",5); g.addEdge("w","u",5); g.addEdge("x","v",2); g.addEdge("v","x",2);
    g.addEdge("x","w",3); g.addEdge("w","x",3); g.addEdge("x","y",1); g.addEdge("y","x",1);
    g.addEdge("y","w",1); g.addEdge("w","y",1); g.addEdge("y","z",1); g.addEdge("z","y",1);
    dijkstra(g, "u");
    for (string v : findPath(g, "u", "z")) cout << v << " ";
    cout << endl;
    return 0;
}'''

PRIM_MAIN = r'''#include <iostream>
#include "pythonds3/cppds/graph_algos.hpp"   // prim (prim listing above)
using namespace std;

int main() {
    Graph g;
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
}'''
# ---------------------------------------------------------------- assembled listings
# The lecture splits DFSGraph and prim over two slides ("..." marks the cut); the page shows each as one listing.
DFSGRAPH_FULL = DFSGRAPH + '\n\n' + DFSVISIT.split('\n', 1)[1]
PRIM_FULL = PRIM_A.rsplit('\n', 1)[0] + '\n' + PRIM_B.split('\n', 1)[1]

# The course header (graph.hpp) that every program includes.
HEADER_GRAPH = r'''class Vertex {
    public:
        string key;
        map<string, int> neighbors;   // key -> weight
        string color = "white";
        // INT_MAX means that this vertex has not been reached from the source.
        int distance = numeric_limits<int>::max();
        string previous = "";
        Vertex() {}
        Vertex(string k) { key = k; }
};

class Graph {
    public:
        map<string, Vertex> vertices;
        // Preserve an existing vertex and all of its edges/traversal state.
        void setVertex(string key) {
            if (vertices.count(key) == 0) vertices.emplace(key, Vertex(key));
        }
        void addEdge(string fromVert, string toVert, int weight = 0) {
            if (vertices.count(fromVert) == 0) setVertex(fromVert);
            if (vertices.count(toVert) == 0) setVertex(toVert);
            vertices[fromVert].neighbors[toVert] = weight;
        }
};'''

# bfs as it appears in graph_algos.hpp: it resets every vertex first and paints the start gray.
HEADER_BFS = r'''void bfs(Graph& g, string startKey) {
    if (g.vertices.count(startKey) == 0) {
        throw invalid_argument("BFS start vertex is not in the graph");
    }
    for (auto& p : g.vertices) {
        p.second.color = "white";
        p.second.distance = INT_MAX;
        p.second.previous = "";
    }
    g.vertices[startKey].distance = 0;
    g.vertices[startKey].color = "gray";
    queue<string> vertQueue;
    vertQueue.push(startKey);
    while (!vertQueue.empty()) {
        string currentKey = vertQueue.front();
        vertQueue.pop();
        Vertex& current = g.vertices[currentKey];
        for (auto& n : current.neighbors) {
            Vertex& neighbor = g.vertices[n.first];
            if (neighbor.color == "white") {
                neighbor.color = "gray";
                neighbor.distance = current.distance + 1;
                neighbor.previous = currentKey;
                vertQueue.push(n.first);
            }
        }
        current.color = "black";
    }
}'''

HEADER_PRINTBOARD = r'''void printBoard(vector<string>& path, int boardSize) {
    vector<vector<int>> board(boardSize, vector<int>(boardSize, -1));
    for (unsigned i = 0; i < path.size(); i++) {
        int id = stoi(path[i]);
        board[id / boardSize][id % boardSize] = i;
    }
    for (auto& row : board) {
        for (int v : row) printf("%4d", v);
        printf("\n");
    }
}'''

HEADER_KTW = r'''bool knightTourWarnsdorff(int n, vector<string>& path, string uKey, int limit, Graph& g) {
    g.vertices[uKey].color = "gray";
    path.push_back(uKey);
    if (n < limit) {
        bool done = false;
        for (string nbKey : orderByAvail(g, uKey)) {
            if (done) break;
            if (g.vertices[nbKey].color == "white") {
                done = knightTourWarnsdorff(n + 1, path, nbKey, limit, g);
            }
        }
        if (!done) {
            path.pop_back();
            g.vertices[uKey].color = "white";
        }
        return done;
    }
    return true;
}'''

HEADER_FINDPATH = r'''vector<string> findPath(Graph& g, string startKey, string endKey) {
    vector<string> path;
    string current = endKey;
    while (current != "" && current != startKey) {
        path.push_back(current);
        current = g.vertices[current].previous;
    }
    if (current == "") return {};
    path.push_back(startKey);
    reverse(path.begin(), path.end());
    return path;
}'''

HEADER_DIJ_CHECK = r'''    for (auto& p : g.vertices) {
        p.second.distance = INT_MAX;
        p.second.previous = "";
        for (auto& edge : p.second.neighbors) {
            if (edge.second < 0) {
                throw invalid_argument("Dijkstra requires non-negative edge weights");
            }
        }
    }'''

# ---------------------------------------------------------------- site additions （補充）
TOPSORT_SUPP = r'''#include <algorithm>
#include <iostream>
#include "pythonds3/cppds/graph_algos.hpp"
using namespace std;

int main() {
    DFSGraph g;
    g.addEdge("3/4 cup milk", "1 cup mix");
    g.addEdge("1 egg", "1 cup mix");
    g.addEdge("1 Tbl oil", "1 cup mix");
    g.addEdge("1 cup mix", "pour 1/4 cup");
    g.addEdge("1 cup mix", "heat syrup");
    g.addEdge("heat griddle", "pour 1/4 cup");
    g.addEdge("pour 1/4 cup", "turn when bubbly");
    g.addEdge("turn when bubbly", "eat");
    g.addEdge("heat syrup", "eat");
    g.dfs();                                   // step 1: closing times

    vector<string> order;                      // step 2: sort by closing time, largest first
    for (auto& p : g.vertices) order.push_back(p.first);
    sort(order.begin(), order.end(), [&](const string& a, const string& b) {
        return g.closing[a] > g.closing[b];
    });
    for (string key : order)                   // step 3: the topological order
        cout << g.discovery[key] << "/" << g.closing[key] << "  " << key << endl;
    return 0;
}'''

EX1_SUPP = r'''#include <iostream>
#include "pythonds3/cppds/graph_algos.hpp"
using namespace std;

int main() {
    Graph g;   // the graph of Exercise 1 (directed)
    g.addEdge("A", "B", 2);  g.addEdge("A", "C", 7);  g.addEdge("A", "E", 12);
    g.addEdge("C", "B", 3);  g.addEdge("B", "D", 2);  g.addEdge("C", "D", -5);
    g.addEdge("C", "E", 2);  g.addEdge("D", "F", 2);  g.addEdge("F", "G", 4);
    g.addEdge("E", "G", -7);
    try {
        dijkstra(g, "A");
        cout << "dijkstra finished" << endl;
    } catch (const invalid_argument& e) {
        cout << "invalid_argument: " << e.what() << endl;
    }
    return 0;
}'''

OUT = {
    'setvertex': 'Vertex(0) Vertex(1) Vertex(2) Vertex(3) Vertex(4) Vertex(5) ',
    'addedge': '(0,1,5) (0,5,2) (1,2,4) (2,3,9) (3,4,7) (3,5,3) (4,0,1) (5,2,1) (5,4,8) ',
    'wl_traverse': 'sage->page->pale->pall->poll->pool->fool',
    'wl_dist': 'cool(1) fail(2) fall(3) foil(1) fool(0) foul(1) page(5) pale(4) pall(3) pole(3) poll(2) pool(1) pope(4) sage(6) sale(5) ',
    'kt5': '''   0   5  14  11  20
  15  10  19   6  13
   4   1  12  21  18
   9  16  23   2   7
  24   3   8  17  22''',
    'kt8': '''   0   3  40  19  38   5  42  21
  33  18   1   4  41  20  37   6
   2  51  34  39  36  55  22  43
  17  32  49  62  53  44   7  56
  50  13  52  35  48  57  54  23
  31  16  61  58  63  26  45   8
  12  59  14  29  10  47  24  27
  15  30  11  60  25  28   9  46''',
    'dfs': ''' Key| Discover| Closing| Previous
   A|        1|      12|         
   B|        2|      11|        A
   C|        3|       4|        B
   D|        5|      10|        B
   E|        6|       9|        D
   F|        7|       8|        E''',
    'topsort': '''17/18  heat griddle
15/16  3/4 cup milk
13/14  1 egg
1/12  1 Tbl oil
2/11  1 cup mix
7/10  pour 1/4 cup
8/9  turn when bubbly
3/6  heat syrup
4/5  eat''',
    'dij': '''u: 0 ()
v: 2 (u)
w: 3 (y)
x: 1 (u)
y: 2 (x)
z: 3 (y)''',
    'dij_path': 'u x y z ',
    'ex1': 'invalid_argument: Dijkstra requires non-negative edge weights',
    'prim': 'MST edges: (A,B) (B,C) (B,D) (D,E) (E,F) (F,G) ',
}
