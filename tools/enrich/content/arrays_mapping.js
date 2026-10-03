/* gen:matrix-mapping */
(() => {
  const root = document.getElementById('matrixMapping');
  const find = id => root.querySelector('#' + id);
  const R = 3, C = 4, N = R * C;
  let progress = 0, selected = -1, timer = null, playing = false;
  const grid = find('mappingGrid');
  for (let k = 0; k < N; k++) {
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'mapping-cell';
    b.dataset.logical = k;
    b.innerHTML = `<small>(${Math.floor(k/C)}, ${k%C})</small><b>${k+1}</b>`;
    b.setAttribute('aria-label', `M[${Math.floor(k/C)}][${k%C}]，值 ${k+1}`);
    b.onclick = () => { pause(); progress = N; selected = k; render(); };
    grid.appendChild(b);
  }
  function pause() {
    if (timer !== null) clearTimeout(timer);
    timer = null; playing = false;
    find('mappingPlay').textContent = progress === N ? '重播' : '播放';
  }
  function render() {
    grid.querySelectorAll('button').forEach((b,k) => {
      b.classList.toggle('is-selected', k === selected);
      b.setAttribute('aria-pressed', String(k === selected));
    });
    for (const mode of ['Row','Col']) {
      const band = find('mapping' + mode); band.innerHTML = '';
      for (let offset = 0; offset < N; offset++) {
        const i = mode === 'Row' ? Math.floor(offset/C) : offset%R;
        const j = mode === 'Row' ? offset%C : Math.floor(offset/R);
        const k = i*C+j, placed = k < progress;
        const cell = document.createElement('div');
        cell.className = 'memory-cell' + (k === selected ? ' is-selected' : '');
        cell.dataset.logical = k; cell.dataset.offset = offset;
        cell.dataset.value = placed ? k+1 : '';
        cell.innerHTML = `<small>(${i},${j})</small><b>${placed ? k+1 : '·'}</b><small>${offset}</small>`;
        band.appendChild(cell);
      }
      const active = band.querySelector(".is-selected");
      if (active) band.parentElement.scrollLeft = active.offsetLeft - band.offsetLeft - (band.parentElement.clientWidth - active.offsetWidth)/2;
    }
    if (selected >= 0) {
      const i = Math.floor(selected/C), j = selected%C;
      find('mappingRowFormula').textContent = `${i} × ${C} + ${j} = ${selected} 格；位址 1000 + ${selected} × 4 = ${1000+selected*4}`;
      const k = j*R+i;
      find('mappingColFormula').textContent = `${j} × ${R} + ${i} = ${k} 格；位址 1000 + ${k} × 4 = ${1000+k*4}`;
      find('mappingStatus').textContent = `已放入 ${progress} / ${N} 個元素。選取 M[${i}][${j}] = ${selected+1}；邏輯座標相同，兩種排列的 offset 可能不同。`;
    } else {
      find('mappingRowFormula').textContent = 'offset = i × Cols + j';
      find('mappingColFormula').textContent = 'offset = j × Rows + i';
      find('mappingStatus').textContent = '尚未放入元素（0 / 12）。';
    }
    find('mappingProgress').value = progress;
    find('mappingStep').disabled = progress === N;
    if (!playing) find('mappingPlay').textContent = progress === N ? '重播' : '播放';
  }
  function advance() {
    if (progress < N) { selected = progress; progress++; render(); }
    if (progress === N) pause();
  }
  function tick() {
    if (!playing) return;
    advance();
    if (playing) timer = setTimeout(tick, Number(find('mappingDelay').value));
  }
  find('mappingPlay').onclick = () => {
    if (playing) { pause(); return; }
    if (progress === N) { progress = 0; selected = -1; }
    playing = true; find('mappingPlay').textContent = '暫停'; tick();
  };
  find('mappingStep').onclick = () => { pause(); advance(); };
  find('mappingReset').onclick = () => { pause(); progress = 0; selected = -1; render(); };
  find('mappingProgress').oninput = e => { pause(); progress = Number(e.target.value); selected = progress-1; render(); };
  document.addEventListener('visibilitychange', () => { if (document.hidden) pause(); });
  new ResizeObserver(() => {
    for (const mode of ['Row', 'Col']) {
      const band = find('mapping' + mode), active = band.querySelector('.is-selected');
      if (active) band.parentElement.scrollLeft = active.offsetLeft - band.offsetLeft - (band.parentElement.clientWidth - active.offsetWidth)/2;
    }
  }).observe(root);
  render();
})();
/* /gen:matrix-mapping */
