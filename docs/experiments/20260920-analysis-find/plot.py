"""Render the complete measured data, with no synthetic timings."""
import csv
import json
from pathlib import Path
from statistics import median
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parent
rows = list(csv.DictReader((ROOT / 'raw.csv').open()))
assert len(rows) == 112
summary = []
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 15,
                     'axes.spines.top': False, 'axes.spines.right': False})
for experiment, filename, title, methods in [
    ('lookup', 'dict_benchmark', 'C++ lookup: find()',
     [('std_find', 'std::find (vector)', '#bc4749'),
      ('unordered_map_find', 'unordered_map::find', '#247b78')]),
    ('pop', 'pop_benchmark', 'C++ vector: erase(begin()) vs pop_back()',
     [('erase_begin', 'erase(begin())', '#bc4749'),
      ('pop_back', 'pop_back()', '#247b78')]),
]:
    fig, ax = plt.subplots(figsize=(12, 7.73), dpi=150)
    fig.subplots_adjust(left=.12, right=.96, top=.80, bottom=.26)
    sizes = sorted({int(r['n']) for r in rows if r['experiment'] == experiment})
    for method, label, color in methods:
        values, lows, highs = [], [], []
        for n in sizes:
            group = [r for r in rows if r['experiment'] == experiment
                     and r['method'] == method and int(r['n']) == n]
            assert len(group) == 7 and all(int(r['operations']) == 100 for r in group)
            times = [float(r['total_ms']) for r in group]
            med = median(times)
            values.append(med); lows.append(med-min(times)); highs.append(max(times)-med)
            summary.append(dict(experiment=experiment, method=method, n=n,
                                target=int(group[0]['target']), hits=int(group[0]['hits']),
                                median_ms=med, min_ms=min(times), max_ms=max(times)))
        ax.errorbar(sizes, values, yerr=[lows, highs], color=color,
                    label=label, marker='o', linewidth=2.2, capsize=5)
    ax.set_yscale('log')
    ax.set_ylabel('Elapsed time for 100 operations (ms, log scale)')
    ax.set_xticks(sizes)
    ax.set_xticklabels([f'{n:,}' for n in sizes])
    ax.set_xlabel('Number of elements, n', labelpad=12)
    ax.grid(axis='y', alpha=.2, which='major')
    ax.legend(loc='best', frameon=False)
    fig.suptitle(title, y=.95, fontsize=23, weight='bold')
    fig.text(.12, .86, 'Median of 7 runs; error bars show min–max. GCC, C++17, -O0.', fontsize=13)
    if experiment == 'lookup':
        targets = [next(r for r in summary if r['method'] == 'std_find' and r['n'] == n) for n in sizes]
        line = ';  '.join(f"{r['target']:,} ({'hit' if r['hits'] else 'miss'})" for r in targets)
        note = ('One target per n, reused by both containers for all 100 queries.\n'
                'Targets (left to right): ' + line + '\n'
                'The target position / a miss changes the work; points need not rise monotonically.')
    else:
        note = ('Vectors are constructed before timing; 100 erases / pops are timed.\n'
                'Front erasure moves the remaining elements; removing the last element does not.\n'
                'Measured timings depend on the machine and compiler settings.')
    fig.text(.12, .055, note, fontsize=11.5, linespacing=1.65)
    fig.savefig(ROOT / (filename+'.png'))
    fig.savefig(ROOT / (filename+'.svg'))
    plt.close(fig)
(ROOT/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
images = [Image.open(ROOT/(name+'.png')).convert('RGB') for name in ['pop_benchmark','dict_benchmark']]
montage = Image.new('RGB', (max(i.width for i in images), sum(i.height for i in images)), 'white')
y = 0
for im in images:
    montage.paste(im, (0,y)); y += im.height
montage.save(ROOT/'all_figures.jpg', quality=90)
print('PASS: two figures, complete montage, and 16 median/min/max summaries generated.')
