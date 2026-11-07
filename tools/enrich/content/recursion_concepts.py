"""Focused explanations that connect the chapter's existing recursion examples."""
from enrich_lib import hl
from content.recursion_opening import why_recursion, strategies
from html import escape


def code(source):
    return '<div class="pseudo-code" data-cpp="fragment">' + hl(source) + '</div>'


def detail(title, body):
    return ('<details class="rec-detail"><summary>' + title
            + '</summary><div class="rec-detail-body">' + body + '</div></details>')


INDEX_REVERSE_PROGRAM = r'''#include <cstddef>
#include <initializer_list>
#include <iostream>
#include <string>

void appendReversed(const std::string& input, std::size_t index,
                    std::string& output) {
    if (index == input.size()) {
        return;
    }
    appendReversed(input, index + 1, output);
    output.push_back(input[index]);
}

std::string reversedByIndex(const std::string& input) {
    std::string output;
    output.reserve(input.size());
    appendReversed(input, 0, output);
    return output;
}

int main() {
    for (const std::string& input : {std::string(""), std::string("a"),
                                    std::string("hello")}) {
        std::cout << '"' << input << "\" -> \""
                  << reversedByIndex(input) << "\"\n";
    }
}'''

INDEX_REVERSE_OUTPUT = '"" -> ""\n"a" -> "a"\n"hello" -> "olleh"\n'




def size_type():
    return r'''<h3><code>size_t</code> 與 <code>&lt;cstddef&gt;</code></h3>
<p><code>&lt;cstddef&gt;</code> 宣告了 <code>std::size_t</code>。範例中的 <code>using namespace std;</code> 讓參數可以簡寫成 <code>size_t index</code>；若不使用這行，就寫 <code>std::size_t index</code>。這個標頭是為了型別，與函式是否遞迴無關。</p>
<details class="rec-detail"><summary>型別寬度、容器索引與標頭的選擇</summary><div class="rec-detail-body">
<p><code>size_t</code> 是用來表示物件大小的無號整數型別，不是專門為大資料設計的型別。它的寬度由實作決定，不能假設一定是 64 位元，也不能假設一定比 <code>unsigned int</code> 寬。小範例使用 <code>unsigned int</code> 也可能得到相同結果，但未必能表示容器所有可能的索引。</p>
<p><code>vector&lt;int&gt;::size()</code> 回傳 <code>vector&lt;int&gt;::size_type</code>；使用預設 allocator 時，它通常就是 <code>std::size_t</code>。也可以把索引直接宣告成 <code>vector&lt;int&gt;::size_type</code>。選索引型別時，應與容器大小的型別相配。</p>
<p>雖然其他標頭可能間接引入這個名稱，使用 <code>std::size_t</code> 時仍應明確 include <code>&lt;cstddef&gt;</code>。無號也不代表不會出錯：例如對 0 做減一不會得到負數；本例的索引只往上增加，不需要這種倒數寫法。</p>
</div></details>'''


def calls():
    return '''<h3>6 次呼叫，為什麼又說遞迴了 5 次？</h3>
<p>先說清楚數的是哪一個函式。五個元素會讓 <code>listSumFrom</code> 依序以 <code>index = 0、1、2、3、4、5</code> 執行，共 6 次。索引 0 的那一次由包裝函式 <code>listSum</code> 發出；其餘 5 次才是 <code>listSumFrom</code> 在函式內呼叫自己的遞迴呼叫。</p>
<p>所以「<code>listSumFrom</code> 總共被呼叫幾次」是 6，「它發出了幾次遞迴呼叫」是 5。兩者都不把包裝函式 <code>listSum</code> 本身算進去。若輸入為空 vector，只有最初的 1 次 <code>listSumFrom</code>，沒有任何遞迴呼叫。</p>'''


def string_constructor():
    examples = '''char digit = 'A';
string one(1, digit);     // "A"
string three(3, digit);   // "AAA"
string prefix = "10";
string result = prefix + digit; // "10A": string + char is valid
// string wrong(digit);  // no constructor for a single char'''
    return '''<h3>把一個 <code>char</code> 變成 <code>string</code></h3>
<p><code>convertString[n]</code> 取出的是一個 <code>char</code>，但 <code>toStr</code> 要回傳 <code>string</code>。<code>string(1, convertString[n])</code> 使用「數量、字元」建構子：重複指定字元 1 次，建立長度為 1 的字串。</p>
<p><code>string(convertString[n])</code> 少了數量，無法使用這個建構子：C++ 的 <code>string</code> 沒有接收單一 <code>char</code> 的建構子。至於 <code>else</code> 中的 <code>toStr(n / base, base) + convertString[n % base]</code>，左邊已是 <code>string</code>，可直接使用 <code>string + char</code> 串接，不必再把右邊轉成字串。</p>''' + detail('char、字串常值與建構子的範例', code(examples) + '''<p><code>'A'</code> 與 <code>"A"</code> 不同，前者是字元，後者是含有結尾零字元的字元陣列，可用來建立字串。<code>string(1, 'A')</code> 中的 1 表示重複次數；換成 3 就得到 <code>"AAA"</code>。</p>''')


def pending_concat():
    explicit = '''char digit = convertString[n % base];
string prefix = toStr(n / base, base);
return prefix + digit;'''
    return '''<p>要分清楚「計算餘數」和「把字元接上結果」。原式 <code>toStr(n / base, base) + convertString[n % base]</code> 沒有規定 <code>+</code> 的左右運算元誰先求值；不能因此說餘數一定等遞迴返回後才計算。串接要等遞迴結果可用，且字元放在結果右邊，才決定了最後的位數順序。</p>
<p>動畫中的「待接字元」是在表示這次呼叫還沒做完的串接工作；原程式未必會配置一個名叫 <code>digit</code> 的堆疊欄位。</p>''' + detail('用三個敘述明確指定求值順序', '''<p>若想明確規定先記下字元、再呼叫遞迴，可以把原本的 <code>else</code> 區塊寫成下面三個敘述。對本例合法的 <code>n &gt;= 0</code>、<code>2 &lt;= base &lt;= 16</code>，得到相同的字串：</p>''' + code(explicit))


def substring_reverse():
    examples = '''string s = "hello";
string rest = s.substr(1);     // "ello"
string middle = s.substr(1, 3); // "ell"'''
    mapping = '''<p>C++17 沒有 Python 的切片語法。<code>substr(pos, count)</code> 可取出一段連續字串；省略 <code>count</code> 時取到結尾。這個 <code>count</code> 是要取的長度，不是結束索引，也沒有 Python 切片的步長參數。以 <code>s = "hello"</code> 為例：</p>
<div style="overflow-x:auto"><table class="cmp-table"><thead><tr><th>Python</th><th>C++17</th><th>結果</th></tr></thead><tbody>
<tr><td><code>s[1:]</code></td><td><code>s.substr(1)</code></td><td><code>"ello"</code></td></tr>
<tr><td><code>s[1:4]</code></td><td><code>s.substr(1, 3)</code></td><td><code>"ell"</code></td></tr>
<tr><td><code>s[::-1]</code></td><td><code>string(s.rbegin(), s.rend())</code></td><td>新的 <code>"olleh"</code></td></tr>
</tbody></table></div>''' + code(examples) + '''<p>這些對照適用於上面的合法索引，不能直接套用到所有切片。Python 的負索引會從尾端計算，超出範圍的切片端點會被截到合法邊界；<code>substr</code> 的位置與長度則是無號值，不提供負索引語意。若 <code>pos &gt; s.size()</code>，它會丟出 <code>std::out_of_range</code>；<code>pos == s.size()</code> 得到空字串，<code>count</code> 太長則只取到結尾。</p>
<p><code>string(s.rbegin(), s.rend())</code> 使用反向迭代器建立新字串，保留原本的 <code>s</code>。另一個選擇是 include <code>&lt;algorithm&gt;</code> 後呼叫 <code>std::reverse(s.begin(), s.end())</code>，直接修改 <code>s</code>，不回傳反轉後的字串。這兩種標準函式庫寫法能完成同一個問題，但不會呈現這裡要練習的遞迴結構。</p>'''
    program = ('<div class="deck-extra"><div class="dx-label">C++17：用索引遞迴，返回時寫入結果</div>'
               '<div class="pseudo-code" data-cpp="run" data-expected="'
               + escape(INDEX_REVERSE_OUTPUT, quote=True).replace('\n', '&#10;') + '">'
               + hl(INDEX_REVERSE_PROGRAM) + '</div></div>')
    output = ('<div class="expected-out"><span class="eo-tag">索引版預期輸出</span><pre>'
              + escape(INDEX_REVERSE_OUTPUT.rstrip('\n')) + '</pre></div>')
    indexed = r'''<p>不必每次建立新的子字串。讓各層以 <code>const string&amp;</code> 共用唯讀輸入，用索引表示目前位置，並以 <code>string&amp;</code> 共用輸出。遞迴走到結尾後，在返回時依序 <code>push_back</code>，就會先寫入最後一個字元。</p>
<p>包裝函式先用 <code>reserve(input.size())</code> 預留足夠容量，之後每個字元只寫入一次，也沒有逐層字串串接。對長度為 $n$ 的輸入，時間為 $O(n)$；呼叫深度與輸出空間各為 $O(n)$。這個版本仍然會遞迴到字串結尾，並未消除過深呼叫的風險。</p>''' + program
    return '''<h3><code>substr(1)</code> 與反轉字串</h3>
<p>填空的兩個答案是 <code>s</code> 與 <code>reverse(s.substr(1))</code>。前者處理空字串和單字元；後者先反轉索引 1 開始的剩餘字串，再把 <code>s[0]</code> 接在右邊。先檢查基本情況，也讓空字串不會執行 <code>s[0]</code> 或 <code>substr(1)</code>。</p>
<p><code>s.substr(1)</code> 會建立不含第一個字元的新字串；<code>s.substr(1, 3)</code> 則從索引 1 開始取最多 3 個字元。第二個參數是長度，不是結束索引。</p>''' + r'''<p>就這個遞迴版本而言，<code>reverse(s.substr(1)) + s[0]</code> 已經直接表達了「剩餘部分反轉，再接回第一個字元」。但它會建立子字串，而且參數以值傳遞；各層子字串的長度相加約為 $n+(n-1)+\cdots+1$。這份程式雖然只有 $n$ 層遞迴，卻也要複製各層的子字串，不能只用層數判定為 $O(n)$ 時間；光是複製就有 $O(n^2)$ 的總工作量。</p>''' + detail('Python 切片與 C++17 字串操作的對照', mapping) + detail('避免逐層複製：索引、參照與共用輸出字串', indexed) + output


def frame_details():
    return r'''<h3>呼叫堆疊替我們記住什麼？</h3>
<p>理解程式時，可以把每個尚未結束的呼叫畫成一個 frame：這次的參數、仍需使用的區域狀態，以及呼叫返回後要接著做的事。<code>toStr(10, 2)</code> 等待較高位字串回來，再完成自己的串接；這就是「待完成運算」。</p>
<p>有了這個呼叫機制，程式設計者通常不必自己建立 stack 來保存這些呼叫。若改寫成顯式 stack，便要自行保存演算法真正需要的狀態，例如目前節點與下一個要探索的方向。單純的加總則只要累加變數，不必照搬整套 stack。</p>
<p>以每層保存固定大小資料的呼叫堆疊模型計算，最大深度為 $d$ 時需要 $O(d)$ 的額外空間。每層若還複製字串或容器，這些資料的空間也要另外計入。遞迴太深可能耗盡呼叫堆疊；C++ 並不保證會替你消除遞迴呼叫。</p>
<details class="rec-detail"><summary>frame 裡可能保存什麼？FP、SP 與返回位址</summary><div class="rec-detail-body">
<p>在使用 frame pointer 的常見實作中，CPU 通常以暫存器保存<strong>目前的 frame pointer（FP）</strong>，用來定位目前 frame 的基準位置。它不同於儲存在 frame 中的<strong>呼叫者 FP 舊值</strong>；後者在返回時可用來恢復上一層的定位。</p>
<div style="overflow-x:auto"><table class="cmp-table"><thead><tr><th>名稱</th><th>作用</th></tr></thead><tbody>
<tr><td>目前的 FP</td><td>定位目前 frame 的基準；常見做法是放在專用暫存器中。</td></tr>
<tr><td>保存的呼叫者 FP</td><td>記錄上一層的 frame 基準，供返回時恢復。</td></tr>
<tr><td>stack pointer（SP）</td><td>追蹤目前堆疊頂端；配置或釋放堆疊空間時可能改變。</td></tr>
<tr><td>return address</td><td>返回呼叫者後要繼續執行的指令位置，通常是呼叫指令之後的下一個指令。</td></tr>
</tbody></table></div>
<p>例如 A 呼叫 B：B 執行時，目前 FP 定位 B 的 frame；若保存了呼叫者 FP，該值對應 A 的 frame；返回位址則對應 A 中呼叫 B 之後的接續指令。前兩者處理 frame 的定位，返回位址處理接下來執行哪個指令，不能互換。</p>
<p>frame 也可能保存參數、區域變數、需要還原的暫存器與暫時值。哪些項目真的放進堆疊、如何排列，以及堆疊往哪個方向成長，由平台的 ABI（呼叫慣例等約定）、編譯器與最佳化決定，不是 C++ 規定的固定配置。編譯器可能省略 FP、讓參數與區域變數留在暫存器，也可能將函式內聯；回傳值不保證放在堆疊頂端。</p>
<p>還要區分 <code>string</code> 物件與它管理的字元儲存空間。物件可能保存長度、容量及指向字元的資訊；字元可能在動態配置的記憶體中，也可能因短字串最佳化（SSO）直接放在物件內。不能把每個字元都畫成 heap 上的資料，也不能假設每個參數都在 stack 上。計算遞迴空間時，要連同各層仍存活的字元資料一起考慮。</p>
</div></details>'''


def hanoi_count():
    return r'''<h3>從三步驟推導移動次數</h3>
<p>令 $T(h)$ 表示這個三柱問題搬完 $h$ 個盤子所需的最少步數，且 $h$ 為非負整數。搬最大盤之前，至少要把上面的 $h-1$ 個盤子移到借用柱；搬最大盤花 1 步；之後再把 $h-1$ 個盤子移到目標柱。三步驟的遞迴做法恰好達到這個下界，因此：</p>
<p>$$T(0)=0,\qquad T(h)=2T(h-1)+1.$$</p>
<p>把兩邊加 1，得到 $T(h)+1=2\bigl(T(h-1)+1\bigr)$。反覆展開至 $T(0)+1=1$，可得 $T(h)+1=2^h$，所以 $T(h)=2^h-1$。例如 3 個盤子要 $2\times3+1=7$ 步；它同時也是兩次搬 2 個盤子各 3 步，再加中間那 1 步。</p>'''


def void_return():
    return '''<h3>沒有寫 <code>return</code>，怎麼回到上一層？</h3>
<p><code>moveTower</code> 的型別是 <code>void</code>，表示不回傳數值。當 <code>height == 0</code> 時，<code>if (height &gt;= 1)</code> 的內容不執行，函式到達結尾便把控制權交回呼叫者。也可以在函式開頭明寫 <code>if (height &lt; 1) return;</code>，再放其餘三個敘述。</p>
<p><code>return;</code> 是返回控制權，<code>return value;</code> 還多帶一個結果；兩者都會讓呼叫者接續執行。<code>main</code> 也有特例：雖然回傳型別是 <code>int</code>，到達結尾會視同 <code>return 0;</code>。一般的 <code>int</code> 或 <code>string</code> 函式不適用這個特例。</p>'''


def return_and_undo():
    example = '''path.push_back(choice); // choose: remember this choice
explore();              // explore: try what follows
path.pop_back();        // undo: remove this choice before the next one'''
    return '''<h3>返回上一層，與撤銷資料是兩件事</h3>
<p>假設 A 呼叫 B，B 又呼叫 C。C 回傳 <code>false</code> 時，控制流程回到 B 發出這次呼叫的位置；B 可以接著嘗試下一個方向。呼叫機制記住了 B 的參數與接續位置，因此不必自行尋找上一層的呼叫。</p>
<p>這裡的回退指的是<strong>控制流程返回</strong>，不是烏龜或機器人自動往回移動一格，也不是所有資料恢復原狀。此處的 <code>Maze&amp;</code> 是共用迷宮；呼叫結束後，寫入的 <code>TRIED</code>、<code>DEAD_END</code> 等標記仍在。這個演算法只要找一條出口路徑，保留標記能避免反覆搜尋同一格。</p>
<p>若問題改成列舉所有合法組合或所有路徑，可能需要自行撤銷某些共用狀態。是否需要撤銷、撤銷哪些資料，要由問題與狀態的意義決定；不能把它一律加進本頁的迷宮程式。</p>''' + detail('選擇、探索與撤銷：共用 path 的概念片段', '''<p>下面的 <code>path</code> 只記錄目前這條選擇路徑：</p>''' + code(example) + '''<p><code>pop_back()</code> 是程式明確要求的撤銷，不是 <code>return</code> 自動替你做的。</p>''')


def maze_guards():
    return '''<h3>四種情況不是四個互斥的入口條件</h3>
<p>一個邊界格也可能是牆，因此「是牆」與「位在邊界」這兩個條件可以同時成立。程式依序檢查：先排除牆，再排除已探索的格子，通過這兩關後，才把邊界視為出口。每次提早 <code>return</code> 都使後面的判斷不再執行。</p>
<p>「四個方向都失敗」則不是進入格子時就能判定的事。它要等北、南、西、東的子呼叫都回傳 <code>false</code>，才把目前格子標為 <code>DEAD_END</code>。所以前三種是入口檢查，最後一種是探索完成後的結果。</p>
<p>回溯也不是遞迴三法則之外的第四條法則。一般遞迴仍需有終止條件與向終止條件前進的狀態；回溯法是在搜尋選擇時利用這些呼叫與返回。迷宮的列、欄不會一路變小，前進的依據是尚未探索的通道逐漸減少，以及遇到牆、已探索格或出口時立即停止。</p>'''


def npos():
    return '''<h3><code>find()</code> 回傳的 <code>string::npos</code></h3>
<p><code>mazeList[row].find(START)</code> 在這一列找 <code>'S'</code>。找得到時，結果是字元索引；找不到時，結果是特殊值 <code>string::npos</code>。因此 <code>col != string::npos</code> 的分支才可以把 <code>col</code> 當成起點的欄索引。</p>
<p>例如 <code>string s = "ABCDE";</code>，<code>s.find('C')</code> 得到索引 <code>2</code>，<code>s.find('Z')</code> 則得到 <code>string::npos</code>。不要把 <code>npos</code> 當成可用索引；直接與 <code>string::npos</code> 比較即可。</p>
<details class="rec-detail"><summary>為什麼 npos 常寫成無號型別的 −1？</summary><div class="rec-detail-body">
<p><code>npos</code> 是 <code>string::size_type</code> 型別的特殊常數，可寫成該型別的 <code>-1</code> 轉換結果。<code>size_type</code> 是無號整數型別，把 <code>-1</code> 轉成這個型別會得到該型別可表示的最大值。因此它不是負的索引，而是「找不到」的特殊標記。型別寬度可能因實作而不同，不要假設它在每台電腦上都是某個固定的十進位數字。</p>
</div></details>'''
