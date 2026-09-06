# P5-P9 fidelity restoration map

Baseline: `b97fe81`. Target: current prerequisite pages. Course-specific examples were replaced with independent examples; corrected C++17 semantics take precedence where the baseline was implementation-specific.

| Page | Baseline evidence | Restored destination | Disposition |
|---|---|---|---|
| P5 | `p5_vector_string.html:552-559` array/vector 3x3 | `#restore-p5-array-vector` | Restored three decision dimensions without course counts. |
| P5 | `:599-610` six course uses | `#restore-p5-array-vector`, `#restore-p5-costs`, `#restore-p5-constructors` | Uses redistributed as independent function/range/sort/heap motivations; statistics omitted. |
| P5 | `:627-636`, `:707-735`, `:776-790` construction tables | `#restore-p5-constructors` | Restored type/name/arguments and empty/count/value/list/copy/range forms. |
| P5 | `:918-1138` reallocation and reserve visuals | `#capacity`, `#restore-p5-costs` | Restored arrow-linked four-stage SVG with per-element moves; stage 4 keeps the released old block dashed and the live new block solid. No guaranteed growth factor is claimed. |
| P5 | `:1152-1219` three walks | `#walk` | Retained with auto/reference explanation. |
| P5 / P2 | P2 range-for value/reference comparison and P5 walk details | `#restore-p5-range-bindings` | Restored the full 3x5 value, mutable-reference, const-reference matrix; P2 may link here after vector is introduced. |
| P5 | `:1263-1273` invalidation table | `#restore-p5-invalidation` | Corrected erased-element/past-the-end rules and split resize into grow without reallocation, grow with reallocation, and shrink. |
| P5 | `:1351-1397` adaptor matrices | `#restore-p5-adaptors` | Restored six columns, pop/void contrast, and runnable deque example. |
| P5 | `:1467-1648` string methods/conversions | `#string`, `#restore-p5-string-convert` | Retained npos/substr/UTF-8; restored literal+literal, char wrapping, visible joined output, stoi/to_string. |
| P5 | `:1705-1727` 19-row cost table | `#restore-p5-costs` | Restored 19 rows with corrected `+=` cost proportional to appended length. |
| P5 | `:1733-1748` 12-row operation comparison | `#restore-p5-depth` final matrix | Converted to need/C++/boundary while retaining C++ operations. |
| P5 | `:1762-1771` resource table | `#restore-p5-uses-resources` | Restored five independent C++ lookup destinations. |
| P6 | `p6_map_set.html:665-675` seven map actions | `#restore-p6-map-api` | Restored effects and return values. |
| P6 | `:756-786` missing-key matrix | `#restore-p6-map-api` second table | Restored mutation/size/error dimensions without Python prerequisite. |
| P6 | `:840-849` set/map matrix | `#restore-p6-set-map` | Restored five operations. |
| P6 | `:928-955` ordered-only operations | `#restore-p6-ordered` | Runnable begin/rbegin/lower_bound/end example. |
| P6 | `:980-1032` iterator symbols and range diagram | `#restore-p6-iterator-table`; existing hero/inline SVG | Restored six-symbol matrix; restored SVG is maintained by root. |
| P6 | `:1122-1199` algorithms | `#restore-p6-algorithms` | Restored sort/find/reverse/count/min/max/swap and member-find distinction. |
| P6 | `:1213-1268` three map walks | `#restore-p6-iterator-table` second table | Restored iterator/pair/structured-binding parallel comparison. |
| P6 | `:1324-1357` four patterns | `#restore-p6-patterns` | Restored counting, unique kinds, visited membership, grouping. |
| P6 | `:1403-1415` 8x5 four-container matrix | `#restore-p6-four-containers` | Restored eight comparison dimensions. |
| P6 | `:1444-1460` operation comparison | `#restore-p6-map-api`, `#restore-p6-set-map`, `#reference` | C++ operations retained without Python dependency. |
| P6 | `:1471-1480` resource table | `#restore-p6-resources` | Restored six API and prerequisite destinations. |
| P7 | `p7_files_exceptions.html:581-590` five stream forms | `#restore-p7-stream-five` | Restored open/truncate/append/getline/RAII matrix. |
| P7 | `:666-675` five exception constructs | `#restore-p7-exception-flow` | Converted to syntax/control-flow/resource matrix. |
| P7 | `:764-773` standard exceptions | `#restore-p7-standard-table` | Restored stoi invalid_argument and bad_alloc, with P4/P9 cross-page destinations. |
| P7 | `:936-944` resource table | `#restore-p7-resources` | Restored stream-state and exception references. |
| P7 | `:785-830` custom exception | P9 `#custom_exception` | Moved after inheritance is introduced; behavior retained. |
| P8 | `p8_oop_basics.html:548-558` ADT mapping | P8 restoration owned by depth-a | Recorded for integration; no P8 edit made here. |
| P8 | `:673-680` access matrix | P8 plus P9 `#restore-p9-inherit-symbols` | Protected/inheritance boundary retained in P9. |
| P8 | constructor-selection warning near `:781-858` | P8 restoration owned by depth-a | Most-vexing-parse restoration delegated. |
| P9 | `p9_oop_advanced.html:548-558` purpose map | `#restore-p9-entry` | Restored three problem/mechanism/evidence rows. |
| P9 | `:600-611` inheritance symbols | `#restore-p9-inherit-symbols` | Restored four syntax rows. |
| P9 | `:741-913` equality/order and sorting | `#operators`, `#restore-p9-less-consumers` | Correct strict weak ordering retained; added runnable sort/set consumer and trace. |
| P9 | priority-queue table within `:766-913` | `#restore-p9-priority-matrix` | Restored three template parameters and pair tie-break. |
| P9 | `:916-948` ordered/unordered | `#restore-p9-ordered-hash` | Restored 2x4 requirements/cost matrix; corrected custom hasher remains primary. |
| P9 | `:956-970` six protocol rows | `#restore-p9-container-protocol` | Restored size/read-write index/equality/order/range-for contracts. |
| P9 | `:975-1048` inheritance/composition | `#restore-p9-composition-matrix` | Restored four dimensions with Parcel/Mailbox-neutral model. |
| P9 | `:1142-1160` seven operator rows | `#restore-p9-operator-matrix` | Restored operator matrix and runnable `operator+`. |
| P9 | `:1168-1177` resource table | `#restore-p9-resources` | Restored four primary language references. |
| P5-P9 | page-specific hero SVGs near each old hero | current page heroes | Restored by root; this change does not overwrite them. |

Learning-data additions cover range construction, char/string conversion, algorithms/member find, lower_bound, unwinding/bad_alloc, operator+, pair ordering, and STL comparison contracts. Every question has four distinct options and one Boolean-marked answer. Wrong-option feedback now names the rejected claim and explains the governing rule; P7 working-directory distractors separately explain why source location, compiler installation, and home directory do not determine the process working directory. Root applies JSON to HTML after parallel edits converge.

## 主代理最終逐列補核

- P5原成本表中的size、empty、capacity、std::find均有獨立列；insert與erase分列，string length/size與索引分列。
  原操作沒有以新增resize／deque等不同操作替代；新增列保留，所以不再以「剛好19列」宣稱完成。
- P6完整矩陣包含四個標頭，保留新增重複鍵列，並同時標出lower_bound／rbegin；標題不寫容易過期的維度數。
- P7恢復in >> word的token擷取，RAII另保留成新增列；標題不再稱只有五種寫法。
- 圖示由對照讀者核對方向與新舊區塊關係；主代理再以實際瀏覽器檢視可讀尺寸。
- 原有字卡缺詞已補，所有front中英文與背面逐項核對。錯項feedback經退回後逐項手寫理由，無共用句模板。
