/* Serialize dynamic MathJax updates; the latest update for an element wins. */
(() => {
  const pending = new Map();
  let work = Promise.resolve(), scheduled = false;
  const formatCosts = text => text.split(/(\$\$[\s\S]*?\$\$|\$[^$]*\$)/g).map(part => {
    if (part.startsWith('$')) return part;
    return part.replace(/\bO\((?:[^()\n]|\((?:[^()\n]|\([^()\n]*\))*\))*\)/g,
      expr => '$' + expr.replace(/log\b/g, '\\log ').replace(/²/g, '^2').replace(/³/g, '^3') + '$');
  }).join('');
  async function drain() {
    try {
      await MathJax.startup.promise;
      while (pending.size) {
        const batch = [...pending].filter(([el]) => el.isConnected);
        pending.clear();
        const elements = batch.map(([el]) => el);
        MathJax.typesetClear(elements);
        for (const [el, html] of batch) el.innerHTML = html;
        if (elements.length) await MathJax.typesetPromise(elements);
      }
    } finally { scheduled = false; }
  }
  window.chapterSetMath = (el, html) => {
    if (!el) return;
    html = formatCosts(html);
    if (!window.MathJax?.typesetPromise) { el.innerHTML = html; return; }
    pending.set(el, html);
    if (!scheduled) {
      scheduled = true;
      work = work.then(drain).catch(error => {
        window.chapterMathError = String(error);
        for (const [target, latest] of pending) target.innerHTML = latest;
        pending.clear();
        console.error(error);
      });
    }
  };
  window.chapterMathIdle = () => work;
})();
