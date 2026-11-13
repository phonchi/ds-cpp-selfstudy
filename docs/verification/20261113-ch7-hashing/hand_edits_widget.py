"""One-time hand edit outside the gen regions of searching_sorting.html: initHashing() learns the plus-3 and
quadratic strategies (the buttons come from search_legacy.py). Open-addressing strategies share one table;
'chain' keeps its own. Clearing or switching strategy bumps an epoch, so an animation still running (or a batch
insert) stops instead of writing its stale table back. Replaces the whole initHashing() block, so rerunning is
harmless."""
from pathlib import Path

PAGE = Path(__file__).resolve().parents[3] / 'searching_sorting.html'
s = PAGE.read_text()

NEW = r"""// --- 03: Hashing (interactive, NOT frame-based) ---
function initHashing() {
  const M = 11;
  const wrap = $('hashTable');
  const NAMES = {linear: '線性探查', plus3: '加 3 探查', quad: '平方探查', chain: '鏈結法'};
  let strategy = 'linear';
  let table = new Array(M).fill(null);    // open addressing (linear, plus3, quad): number or null
  let chain = Array.from({length: M}, () => []); // for chaining: list of numbers per slot
  let highlightSlot = -1;
  let highlightCls = '';
  let probedSlots = []; // recently visited slots
  let opCount = 0;
  let epoch = 0;        // bumped by clear / strategy switch; stale animations stop
  const isOpen = () => strategy !== 'chain';
  // slot of the i-th probe (i = 0 is the hash value itself)
  function probeAt(h, i) {
    if (strategy === 'plus3') return (h + 3 * i) % M;
    if (strategy === 'quad') return (h + i * i) % M;
    return (h + i) % M;
  }
  function nextHint(i) {
    if (strategy === 'plus3') return '往後跳 3 格';
    if (strategy === 'quad') return `改試 h + ${(i + 1) * (i + 1)}`;
    return '線性探查下一個';
  }

  function buildTable() {
    wrap.innerHTML = '';
    for (let i = 0; i < M; i++) {
      const slot = document.createElement('div');
      slot.className = 'hash-slot';
      slot.dataset.idx = i;
      const idxEl = document.createElement('div');
      idxEl.className = 'slot-idx';
      idxEl.textContent = i;
      const valEl = document.createElement('div');
      valEl.className = 'slot-val';
      valEl.textContent = '—';
      const chainEl = document.createElement('div');
      chainEl.className = 'hash-chain';
      slot.appendChild(idxEl);
      slot.appendChild(valEl);
      slot.appendChild(chainEl);
      slot.classList.add('empty');
      wrap.appendChild(slot);
    }
  }

  function refresh() {
    const slots = wrap.children;
    for (let i = 0; i < M; i++) {
      const slot = slots[i];
      slot.className = 'hash-slot';
      const valEl = slot.querySelector('.slot-val');
      const chainEl = slot.querySelector('.hash-chain');
      chainEl.innerHTML = '';
      if (isOpen()) {
        if (table[i] != null) { valEl.textContent = table[i]; }
        else { valEl.textContent = '—'; slot.classList.add('empty'); }
      } else {
        // chain
        if (chain[i].length === 0) { valEl.textContent = '—'; slot.classList.add('empty'); }
        else {
          valEl.textContent = chain[i][0];
          for (let k = 1; k < chain[i].length; k++) {
            const node = document.createElement('div');
            node.className = 'chain-node';
            node.textContent = chain[i][k];
            chainEl.appendChild(node);
          }
        }
      }
      // apply highlight
      if (probedSlots.includes(i)) slot.classList.add('searching');
    }
    if (highlightSlot >= 0 && highlightCls) {
      slots[highlightSlot].classList.remove('empty','searching');
      slots[highlightSlot].classList.add(highlightCls);
    }
    // stats
    let used;
    if (isOpen()) used = table.filter(x => x != null).length;
    else used = chain.reduce((s, c) => s + (c.length > 0 ? 1 : 0), 0);
    $('hashUsed').textContent = `${used} / ${M}`;
    let load;
    if (isOpen()) load = used / M;
    else load = chain.reduce((s,c)=>s+c.length,0) / M;
    $('hashLoad').textContent = load.toFixed(2);
    $('hashOps').textContent = opCount;
  }

  function setStatus(msg) { $('hashStatus').textContent = msg; }

  function clearHighlights() {
    highlightSlot = -1; highlightCls = ''; probedSlots = [];
  }

  async function animate(steps, ep) {
    for (const s of steps) {
      if (ep !== epoch) return false;
      if ('highlightSlot' in s) highlightSlot = s.highlightSlot;
      if ('highlightCls' in s) highlightCls = s.highlightCls;
      if ('probedSlots' in s) probedSlots = s.probedSlots;
      if ('msg' in s) setStatus(s.msg);
      if ('table' in s) table = s.table;
      if ('chain' in s) chain = s.chain;
      refresh();
      await new Promise(r => setTimeout(r, 600));
    }
    return ep === epoch;
  }

  async function insert(val) {
    if (isNaN(val)) return;
    const ep = epoch;
    opCount = 0;
    clearHighlights();
    const h = ((val % M) + M) % M;
    if (isOpen()) {
      const probed = [];
      for (let i = 0; i < M; i++) {
        const p = probeAt(h, i);
        opCount++;
        probed.push(p);
        if (table[p] == null) {
          await animate([
            {msg: i === 0 ? `h(${val}) = ${val} mod ${M} = ${h}，試 slot ${p}` : `雜湊值 ${h} 那一格已被佔用，第 ${i + 1} 次試 slot ${p}`, highlightSlot: p, highlightCls: 'searching', probedSlots: [...probed]},
            {msg: `slot ${p} 為空 → 插入 ${val}`, highlightSlot: p, highlightCls: 'placed', probedSlots: probed.slice(0,-1), table: (() => { const t=[...table]; t[p]=val; return t; })()}
          ], ep);
          return;
        }
        if (table[p] === val) {
          await animate([{msg: `slot ${p} 已是 ${val}（重複）`, highlightSlot: p, highlightCls: 'collision', probedSlots: probed}], ep);
          return;
        }
        if (!await animate([{msg: `slot ${p} 被 ${table[p]} 佔用 → ${nextHint(i)}`, highlightSlot: p, highlightCls: 'collision', probedSlots: [...probed]}], ep)) return;
      }
      if (ep !== epoch) return;
      const distinct = new Set(probed).size;
      setStatus(distinct === M ? '表已滿，無法插入'
        : `探查 ${M} 次只碰到 ${distinct} 個不同的 slot，都已被佔用，無法插入 ${val}`);
    } else {
      // chain
      opCount++;
      const c = [...chain[h]];
      if (c.includes(val)) {
        await animate([{msg: `slot ${h} 的鏈結串列已含 ${val}（重複）`, highlightSlot: h, highlightCls: 'collision'}], ep);
        return;
      }
      const newChain = chain.map((x,idx) => idx === h ? [...x, val] : x);
      await animate([
        {msg: `h(${val}) = ${h}，插入 slot ${h} 的鏈結串列`, highlightSlot: h, highlightCls: 'searching'},
        {msg: `slot ${h} 已加入 ${val}（鏈長 ${newChain[h].length}）`, highlightSlot: h, highlightCls: 'placed', chain: newChain}
      ], ep);
    }
  }

  async function search(val) {
    if (isNaN(val)) return;
    const ep = epoch;
    opCount = 0;
    clearHighlights();
    const h = ((val % M) + M) % M;
    if (isOpen()) {
      const probed = [];
      for (let i = 0; i < M; i++) {
        const p = probeAt(h, i);
        opCount++;
        probed.push(p);
        if (table[p] == null) {
          await animate([{msg: `slot ${p} 為空 → 找不到 ${val}`, highlightSlot: p, highlightCls: 'collision', probedSlots: probed.slice(0,-1)}], ep);
          return;
        }
        if (table[p] === val) {
          await animate([{msg: `✓ 在 slot ${p} 找到 ${val}！比較了 ${opCount} 次`, highlightSlot: p, highlightCls: 'found', probedSlots: probed.slice(0,-1)}], ep);
          return;
        }
        if (!await animate([{msg: `slot ${p} = ${table[p]} ≠ ${val}，繼續探查`, highlightSlot: p, highlightCls: 'searching', probedSlots: [...probed]}], ep)) return;
      }
      if (ep !== epoch) return;
      const distinct = new Set(probed).size;
      setStatus(distinct === M ? `找不到 ${val}（已掃過整個表）`
        : `找不到 ${val}（探查序列碰得到的 ${distinct} 個 slot 都看過了）`);
    } else {
      const c = chain[h];
      for (let k = 0; k < c.length; k++) {
        opCount++;
        if (c[k] === val) {
          await animate([{msg: `✓ 在 slot ${h} 鏈結串列第 ${k+1} 位找到 ${val}（比較 ${opCount} 次）`, highlightSlot: h, highlightCls: 'found'}], ep);
          return;
        }
      }
      const why = c.length === 0 ? `slot ${h} 的鏈結串列是空的，找不到 ${val}` : `slot ${h} 的鏈結串列中沒有 ${val}`;
      await animate([{msg: `${why}（比較 ${opCount} 次）`, highlightSlot: h, highlightCls: 'collision'}], ep);
    }
  }

  buildTable();
  refresh();

  $('hashInsert').onclick = () => insert(parseInt($('hashVal').value));
  $('hashSearch').onclick = () => search(parseInt($('hashVal').value));
  $('hashClear').onclick = () => {
    epoch++;
    table = new Array(M).fill(null);
    chain = Array.from({length: M}, () => []);
    opCount = 0;
    clearHighlights();
    refresh();
    setStatus('已清空雜湊表');
  };
  $('hashBatchInsert').onclick = async () => {
    const arr = parseArr($('hashBatch').value);
    const ep = epoch;
    for (const v of arr) {
      if (ep !== epoch) return;
      await insert(v);
      await new Promise(r => setTimeout(r, 200));
    }
  };
  // strategy buttons
  document.querySelectorAll('#hashing .preset-btn[data-strategy]').forEach(btn => {
    btn.onclick = () => {
      document.querySelectorAll('#hashing .preset-btn[data-strategy]').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      strategy = btn.dataset.strategy;
      epoch++;
      // clear table when switching for clarity
      table = new Array(M).fill(null);
      chain = Array.from({length: M}, () => []);
      opCount = 0;
      clearHighlights();
      refresh();
      setStatus(`已切換為「${NAMES[strategy]}」並清空表`);
    };
  });
}

"""

a = s.index('// --- 03: Hashing (interactive, NOT frame-based) ---')
b = s.index('// --- 04: Bubble Sort ---')
s = s[:a] + NEW + s[b:]
PAGE.write_text(s)
print('initHashing replaced:', b - a, '->', len(NEW), 'chars')
