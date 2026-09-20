# Chapter 2 find benchmark refresh — 2026-09-20

The updated `ds_cpp/Slides/02_Analysis.ipynb` is the authority for the examples.
Its hash-table lookup now uses `unordered_map::find`, sizes 100000 / 200000 /
400000 / 800000, and one `rand() % (2*n)` target per size reused for 100 queries
in both containers. The front/back deletion experiment retains its original
2500000 / 5000000 / 7500000 / 10000000 sizes and 100 operations.

## Evidence and scope

- `lookup_source.cpp`, `pop_source.cpp`: exact source cells before integration.
- `provenance.json`: source hashes, compiler/platform, parameters.
- `benchmark.cpp`, `dstimer.hpp`: standalone measurement harness and original timer.
- `raw.csv`: all 112 timings (7 trials × 4 sizes × 2 methods × 2 experiments).
- `summary.json`: median/min/max for all 16 groups.
- `run.log`: complete measurement, plotting and rendering output, including failed checks and their subsequent correction.
- `dict_benchmark.png`, `pop_benchmark.png`, matching SVGs: measured plots.
- `all_figures.jpg`: complete two-figure overview. `comparison/` contains the lookup-method comparison table.
- `validation/`: browser screenshots, image checks, actual PDF page map and contact sheet.

The harness uses GCC 13.3 / C++17 / `-O0`. Lookup hit counts and vector final
states are checked after timing. Unlike the short notebook display code, the
harness stops the second timer before formatting output. Construction and
correctness checks are excluded. Each trial resets `srand(1)`, as in a fresh
process's default random sequence on this platform. Notebook kernels and other
C libraries can produce different targets. No extra seed was added to the
user's notebook, and its saved outputs were preserved.

Local targets are 89383 (hit), 130886 (hit), 92777 (hit), and 1036915 (miss).
The different target positions explain the non-monotonic vector curve. These
four targets are not a statistical estimate of average-case complexity.
`-O0` avoids dead-search elimination in this classroom measurement; this is
not a benchmark of optimized production code. Sub-microsecond deletion batches
are sensitive to timer overhead.

## Reproduce

Run in this directory with the existing Python Matplotlib/Pillow environment:

```bash
g++ -std=c++17 -O0 benchmark.cpp -o /tmp/analysis-find-benchmark
/tmp/analysis-find-benchmark > raw.csv
MPLCONFIGDIR=/tmp/analysis-mpl python plot.py
```

Copy the directory before collecting a new experiment so this run stays intact.
The HTML export uses Chromium via Playwright with the original Reveal settings
(including incremental fragment pages). Network image requests are fulfilled
with the freshly generated local PNGs before PDF printing, so the PDF never
uses stale GitHub raw images. Bookmarks are built from every visible H1/H2,
including headings containing inline code, then matched to actual PDF text.
A trailing empty Chromium print page is removed only if it has no text or images.

## Site integration

The self-study page keeps its current typography, colors, navigation, and
interactive components (extension mode; visual variance 3, motion 3, density 8,
asset dependence 4, brand fidelity 10). Updated plots retain the existing red/
green comparison convention; the old fixed-height crop is removed so captions
remain visible. The user's pre-existing comparison-table edits are retained.
Only relevant generated example blocks are replaced, and the enrichment source
is updated so re-running it will not restore `count` or the old lookup sizes.

The third lecture is dated 2026-09-21 and follows the existing lecture layout,
with C++ textbook and lookup references. Existing exercise notebooks already
contain paired C++/Python questions and are linked unchanged. No recording was
invented or copied from the prior Python lecture.

Final PDF: 134 pages and 7 verified bookmarks. Both chart widths were increased
from 40% to 75% for slide/PDF readability; all notebook code and saved outputs
are unchanged. Only markdown cells 123, 135 and 136 differ from the supplied notebook.
The later cout request is limited to Chapter 2; no other chapters were edited.
