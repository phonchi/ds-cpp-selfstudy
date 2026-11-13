"""The seven lecture quizzes of chapter 7 (questions/ch7/*.json, translated). Shown inline in their sections."""

LECTURE_QUIZ = {
    'binary': {"question": "遞迴版二分搜尋傳入索引邊界，並令 midpoint = first + (last - first) / 2。對已排序 vector {3, 5, 6, 8, 11, 12, 14, 15, 17, 18} 找 16，依序比較哪些值？", "answers": [{"answer": "12, 17, 15", "correct": False, "feedback": "不對。初始邊界是 0 到 9，整數除法得到索引 4（值 11），不是索引 5。"}, {"answer": "18, 17, 15", "correct": False, "feedback": "不對。二分搜尋從目前索引範圍的中點開始，不是從尾端。"}, {"answer": "11, 14, 17", "correct": False, "feedback": "不對。第一次比較 11 後，邊界變成 5..9；下一個中點是索引 7，也就是 15，不是 14。"}, {"answer": "11, 15, 17", "correct": True, "feedback": "正確。邊界 0..9 比 11；5..9 比 15；8..9 比 17；下一個範圍為空。整個過程只改索引，不複製子 vector。"}]},
    'bubble': {"question": "對 {5, 1, 4, 2, 8} 做遞增氣泡排序，完整跑完第一輪後 vector 是哪一個？", "answers": [{"answer": "{1, 4, 2, 5, 8}", "correct": True, "feedback": "正確。5 依序越過 1、4、2；最後 5 與 8 已是正確順序，所以第一輪結束時最大值 8 固定在尾端。"}, {"answer": "{1, 4, 2, 8, 5}", "correct": False, "feedback": "不對。5 與 8 已是遞增順序，不會交換。"}, {"answer": "{1, 2, 4, 5, 8}", "correct": False, "feedback": "這是全部排序完成的結果，不是只跑一輪。"}, {"answer": "{5, 1, 4, 2, 8}", "correct": False, "feedback": "至少前三組相鄰元素逆序，第一輪一定會交換。"}]},
    'hash1': {"question": "大小為 13 的雜湊表，鍵 27 與 130 分別會對應到哪個索引位置？", "answers": [{"answer": "1, 10", "correct": False, "feedback": "不對。27 對應到 1 沒錯，但 130 不會對應到 10。"}, {"answer": "13, 0", "correct": False, "feedback": "不對。大小 13 的表不可能有索引 13：索引範圍是 0 到 12。"}, {"answer": "1, 0", "correct": True, "feedback": "正確。用餘數法（key % 大小）：27 % 13 = 1、130 % 13 = 0。"}, {"answer": "2, 3", "correct": False, "feedback": "不對。請重新算一次兩個鍵的模運算。"}]},
    'hash2': {"question": "把這組鍵依序插入恰好 11 格的雜湊表：113, 117, 97, 100, 114, 108, 116, 105, 99，用線性探查解決碰撞。全部插完後，表的內容最接近下列哪一個？", "answers": [{"answer": "100, __, __, 113, 114, 105, 116, 117, 97, 108, 99", "correct": False, "feedback": "不對。這一組把 100 放在索引 0，但 100 % 11 = 1，應該在索引 1。"}, {"answer": "99, 100, __, 113, 114, __, 116, 117, 105, 97, 108", "correct": True, "feedback": "正確。各鍵對應：99→0、100→1、113→3、114→4、116→6、117→7、105 碰撞後探查到 8、97→9、108 碰撞後探查到 10。"}, {"answer": "100, 113, 117, 97, 14, 108, 116, 105, 99, __, __", "correct": False, "feedback": "不對。這個排列不符合各鍵取餘數後的結果。"}, {"answer": "117, 114, 108, 116, 105, 99, __, __, 97, 100, 113", "correct": False, "feedback": "不對。這個鍵的分布不符合 mod 11 的運算結果。"}]},
    'merge': {"question": "串列 [21, 1, 26, 45, 29, 28, 2, 9, 16, 49, 39, 27, 43, 34, 46, 40] 執行 mergesort。第 3 次遞迴呼叫時要排序的串列是下列哪一個？", "answers": [{"answer": "[16, 49, 39, 27, 43, 34, 46, 40]", "correct": False, "feedback": "不對。這是原串列的右半，要等整個左半處理並合併完才會輪到。"}, {"answer": "[21, 1]", "correct": True, "feedback": "正確。mergesort 先對半切、再先遞迴左半：16 個元素的串列，第 1 次遞迴拿前 8 個、第 2 次拿前 4 個、第 3 次拿前 2 個，也就是 [21, 1]。"}, {"answer": "[21, 1, 26, 45]", "correct": False, "feedback": "不對。這個 4 元素串列是第 2 次遞迴呼叫的輸入。"}, {"answer": "[21]", "correct": False, "feedback": "不對。單一元素的串列是第 4 次遞迴呼叫的輸入，它會直接觸發基底情況。"}]},
    'quick': {"question": "串列 [14, 17, 13, 15, 19, 10, 3, 16, 9, 12] 執行 quicksort。第二次分割（partition）之後，串列內容是下列哪一個？", "answers": [{"answer": "[9, 3, 10, 13, 12]", "correct": False, "feedback": "不對。這只是第二次分割後的左子串列，不是整條串列的狀態。"}, {"answer": "[9, 3, 10, 13, 12, 14]", "correct": False, "feedback": "不對。這條串列被截掉了，少了右邊分割區的元素。"}, {"answer": "[9, 3, 10, 13, 12, 14, 17, 16, 15, 19]", "correct": False, "feedback": "不對。右半（19, 16, 15, 17）在輪到它自己的遞迴呼叫之前，會維持第一次分割後的狀態。"}, {"answer": "[9, 3, 10, 13, 12, 14, 19, 16, 15, 17]", "correct": True, "feedback": "正確。第一次以 pivot 14 分割後，串列是 [10, 12, 13, 9, 3, 14, 19, 16, 15, 17]。第二次分割處理左子串列 [10, 12, 13, 9, 3]、pivot 是 10，得到 [9, 3, 10, 13, 12]；放回整條串列就是這個答案。"}]},
    'sequential': {"question": "對有序串列 [3, 5, 6, 8, 11, 12, 14, 15, 17, 18] 做循序搜尋，要判定 key 13 不在裡面，需要幾次比較？", "answers": [{"answer": "10", "correct": False, "feedback": "不對。無序串列的循序搜尋才需要看完全部 10 個；有序串列一碰到比目標大的值就能提前停止。"}, {"answer": "5", "correct": False, "feedback": "不對。比較 5 次後只走到 11；11 比 13 小，還得繼續往後找。"}, {"answer": "7", "correct": True, "feedback": "正確。有序串列的搜尋會逐一比較，直到找到目標或碰到比目標大的值：13 依序跟 3, 5, 6, 8, 11, 12, 14 比較，共 7 次。比到 14 時發現 14 > 13，就能斷定 13 不可能在後面，搜尋停止。"}, {"answer": "6", "correct": False, "feedback": "不對。比較 6 次後走到 12；12 比 13 小，還需要第 7 次跟 14 比較，才能確定 13 不在串列裡。"}]},
}

# Quizzes written for this site (not in the lecture). They check the clarifications added to the sections.
SITE_QUIZ = {
    'bin-stop': {"label": "二分搜尋的停止條件",
                 "question": "迴圈版 binarySearch 在 {17, 20, 26, 31, 44, 54, 55, 65, 77, 93} 中找 50，最後回傳 false。迴圈結束時 first 和 last 各是多少？",
                 "answers": [
                     {"answer": "first = 5，last = 4", "correct": True, "feedback": "依序比 44、65、54：44 太小，first 變成 5；65 太大，last 變成 6；54 太大，last 變成 4。first > last，範圍是空的。"},
                     {"answer": "first = 5，last = 5", "correct": False, "feedback": "first == last 時還剩一個候選，迴圈還會再比一次；迴圈結束時一定是 first > last。"},
                     {"answer": "first = 4，last = 5", "correct": False, "feedback": "這時 first <= last，迴圈還沒結束；而且第一次比較 44 之後，first 就已經變成 5。"},
                     {"answer": "first = 0，last = -1", "correct": False, "feedback": "這是空 vector 一開始的狀態。這裡有 10 個元素，範圍是一步一步縮小的。"}]},
    'probe-cycle': {"label": "探查週期",
                    "question": "表的大小 m = 12，從 slot 0 出發，每次碰撞後跳 3 格（skip = 3）。一直碰撞下去，最多能探查到幾個不同的 slot？",
                    "answers": [
                        {"answer": "4 個", "correct": True, "feedback": "gcd(3, 12) = 3，只能走 12 / 3 = 4 格：0、3、6、9，然後回到 0。"},
                        {"answer": "12 個", "correct": False, "feedback": "skip 和 m 互質時才走得遍。3 和 12 有公因數 3，走到 9 之後就回到 0。"},
                        {"answer": "3 個", "correct": False, "feedback": "3 是 gcd(3, 12)；能走的格數是 12 / 3 = 4。"},
                        {"answer": "11 個", "correct": False, "feedback": "能走的格數是 m / gcd(skip, m)，和 m − 1 無關。"}]},
    'prime': {"label": "表的大小與質數",
              "question": "關於「雜湊表的大小常選質數」，下列哪一句正確？",
              "answers": [
                  {"answer": "表的大小是質數時，1 到 m − 1 的任何跳格數都走得遍整張表", "correct": True, "feedback": "m 是質數時，1 到 m − 1 的任何 skip 都和 m 互質，探查序列會走過每個 slot。"},
                  {"answer": "表的大小用質數，餘數法就保證不會碰撞", "correct": False, "feedback": "11、22、33、44 對 m = 11 全部碰撞。碰撞的條件是 m 整除兩個 key 的差，和 m 是不是質數無關。"},
                  {"answer": "線性探查的表大小不是質數，就會有 slot 永遠用不到", "correct": False, "feedback": "線性探查每次跳 1 格，gcd(1, m) = 1，任何大小都走得遍。"},
                  {"answer": "只要 skip 是質數，任何大小的表都走得遍", "correct": False, "feedback": "條件是 skip 和 m 互質。skip = 3 是質數，但 m = 12 時只能走 4 格。"}]},
    'quad': {"label": "平方探查走得到幾格",
             "question": "表的大小 m = 11，平方探查依序試 h、h + 1、h + 4、h + 9……（每次都對 11 取餘數）。一個 key 的探查序列最多會碰到幾個不同的 slot？",
             "answers": [
                 {"answer": "6 個", "correct": True, "feedback": "m 是奇質數時，i² 除以 m 的餘數只有 (m + 1) / 2 種。從 slot 2 出發依序是 2, 3, 6, 0, 7, 5，之後重複。"},
                 {"answer": "11 個", "correct": False, "feedback": "平方探查不一定走得遍：i 和 11 − i 的平方除以 11 的餘數相同，後半段會重複前半段的位置。"},
                 {"answer": "10 個", "correct": False, "feedback": "i 從 0 試到 10 共 11 次，但 i 和 11 − i 落在同一格，不同的 slot 只有 6 個。"},
                 {"answer": "5 個", "correct": False, "feedback": "起點本身也要算：i = 0 到 5 的平方除以 11 的餘數 0, 1, 4, 9, 5, 3 各不相同，共 6 個。"}]},
    'open-chain': {"label": "開放定址與鏈結法",
                   "question": "下列關於開放定址與鏈結法的敘述，哪一句正確？",
                   "answers": [
                       {"answer": "鏈結法的負載因子可以超過 1", "correct": True, "feedback": "鏈結法把元素掛在 slot 的鏈上，元素可以比 slot 多；開放定址每個 slot 只放一個元素，λ 最多是 1。"},
                       {"answer": "開放定址搜尋失敗時，一定只需要檢查雜湊值那一格", "correct": False, "feedback": "元素可能因為碰撞被推到別處，要沿著探查序列找，直到碰到空槽或繞回起點。"},
                       {"answer": "鏈結法不會發生碰撞", "correct": False, "feedback": "碰撞照樣會發生，只是碰撞的元素留在同一個 slot 的鏈上，不去佔別的 slot。"},
                       {"answer": "平方探查屬於鏈結法的一種", "correct": False, "feedback": "平方探查在表裡另找空位，屬於開放定址。"}]},
}
