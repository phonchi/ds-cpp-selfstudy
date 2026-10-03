/* ---------- P02 unordered ---------- */
function linkedPlaybackControls(section, state) {
  document.querySelectorAll(`#${section} .controls-bar button`).forEach(btn => {
    const action = btn.getAttribute('onclick') || '';
    if (action.includes('.toggle(') || action.includes('.step(')) {
      btn.disabled = state !== 'playing';
      if (action.includes('.toggle(')) btn.textContent = state === 'done' ? '已完成' : '⏸ 暫停';
    }
  });
}
function linkedStart(player, section) {
  linkedPlaybackControls(section, 'playing');
  player.onDone = () => linkedPlaybackControls(section, 'done');
  const step = player.step.bind(player);
  player.step = () => { if (!player._done) step(); };
  const toggle = player.toggle.bind(player);
  player.toggle = btn => { if (!player._done) toggle(btn); };
  player.reset();
  player.play();
}
let ull = [31, 77, 17, 93];
let ullPlayer = null;
function ullStop() {
  if (ullPlayer) ullPlayer.stop();
  ullPlayer = null;
  linkedPlaybackControls('unordered', 'idle');
}
function ullRender(opts={}, msg) {
  renderLinked('ullVis', ull, opts);
  if (msg) setStatus('ullStatus', msg);
}
function ullAdd() { ullStop();
  const v = parseInt($('ullInput').value || '54', 10);
  const frames = [
    {hl:-1, line:2, msg:`new Node(${v})`},
    {hl:-1, line:3, msg:`temp->setNext(head)（新節點接住 ${ull[0] ?? 'NULL'} 開頭的整條串列）`},
    {act:'do', hl:0, line:4, msg:`head = temp → ${v} 成為新的第一個節點。O(1) 完工！`},
  ];
  ullPlayer = new Player({frames, apply: f => {
    if (f.act === 'do' && !f.done) { ull.unshift(v); f.done = true; }
    ullRender({hl:f.hl}, f.msg); hlLine('ullCode', f.line);
  }, delayInput: $('ullSpeed')});
  linkedStart(ullPlayer, 'unordered');
}
function ullSearch() { ullStop();
  const v = parseInt($('ullInput').value || '17', 10);
  const frames = [];
  for (let i = 0; i < ull.length; i++) {
    frames.push({hl:i, line:9, msg:ull[i] === v ? String.raw`$${ull[i]}=${v}$ → <strong>找到 ✓</strong>` : String.raw`$${ull[i]}\ne ${v}$，<code>cur = cur-&gt;getNext()</code>`});
    if (ull[i] === v) break;
  }
  if (ull.indexOf(v) < 0) frames.push({hl:-1, line:11, msg:`cur 走到 NULL → <strong>${v} 不在串列中 ✗</strong>`});
  ullPlayer = new Player({frames, apply: f => { ullRender({hl:f.hl}, f.msg); hlLine('ullCode', f.line); }, delayInput: $('ullSpeed')});
  linkedStart(ullPlayer, 'unordered');
}
function ullRemove() { ullStop();
  const v = parseInt($('ullInput').value || '17', 10);
  const idx = ull.indexOf(v);
  if (idx < 0) { ullRender({}, `${v} 不在串列裡，先 add 或換個值。`); return; }
  const frames = [];
  for (let i = 0; i <= idx; i++)
    frames.push({hl:i, prevHl:i-1, line:15, msg:`目前節點的值是 ${ull[i]}${i===idx?'（就是它！）':'，prev 跟上'}`});
  frames.push({act:'do', hl:-1, line:18,
    msg: idx===0 ? `prev 是 NULL → head = cur->getNext()。別忘了 delete cur！`
                 : `prev->setNext(cur->getNext())，${ull[idx-1]} 直接跳過 ${v}。別忘了 delete cur！`});
  ullPlayer = new Player({frames, apply: f => {
    if (f.act === 'do' && !f.done) { ull.splice(idx,1); f.done = true; }
    ullRender({hl:f.hl, prevHl:f.prevHl}, f.msg); hlLine('ullCode', f.line);
  }, delayInput: $('ullSpeed')});
  linkedStart(ullPlayer, 'unordered');
}
function ullReset() { ullStop(); ull = [31,77,17,93]; ullRender({}, '已重置為 31→77→17→93。'); }
linkedPlaybackControls('unordered', 'idle');
ullRender();

/* ---------- P03 ordered ---------- */
let oll = [17, 26, 31, 54, 77, 93];
let ollPlayer = null;
function ollStop() {
  if (ollPlayer) ollPlayer.stop();
  ollPlayer = null;
  linkedPlaybackControls('ordered', 'idle');
}
function ollRender(opts={}, msg) { renderLinked('ollVis', oll, opts); if (msg) setStatus('ollStatus', msg); }
function ollAdd() { ollStop();
  const v = parseInt($('ollInput').value || '40', 10);
  const frames = [];
  let i = 0;
  while (i < oll.length && oll[i] < v) {
    frames.push({hl:i, line:3, msg:String.raw`目前節點的值 $${oll[i]}\lt ${v}$，繼續前進`});
    i++;
  }
  const at = i;
  frames.push({hl: i < oll.length ? i : -1, line:5,
    msg: i < oll.length ? String.raw`目前節點的值 $${oll[i]}\ge ${v}$ → 插在 prev 與 cur 之間` : `走到尾端 → 插在最後`});
  frames.push({act:'do', hl:at, line: at===0?7:8,
    msg: at===0 ? `插在最前：temp->setNext(head); head = temp` : `temp->setNext(cur); prev->setNext(temp) ✓`});
  ollPlayer = new Player({frames, apply: f => {
    if (f.act === 'do' && !f.done) { oll.splice(at,0,v); f.done = true; }
    ollRender({hl:f.hl}, f.msg); hlLine('ollCode', f.line);
  }, delayInput: $('ollSpeed')});
  linkedStart(ollPlayer, 'ordered');
}
function ollReset() { ollStop(); oll = [17,26,31,54,77,93]; ollRender({}, '已重置。'); }
linkedPlaybackControls('ordered', 'idle');
ollRender();

