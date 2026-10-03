/* Only text nodes are formatted. Markup, existing code and LaTeX stay intact. */
(() => {
  const tokens = new RegExp(/*TOKEN_PATTERN*/, 'g');
  const isTermProse = (token, before, after) => {
    if (token==='string' && /(?:C-style|C)\s+$/.test(before)) return true;
    if (token==='double' && /^\s+free\b/.test(after)) return true;
    if (token==='Linear' && /^\s+Linked\b/.test(after)) return true;
    if (token==='row' && /\(\s*$/.test(before) && /^\s*,\s*(col|column)\b/.test(after)) return true;
    if (['col','column'].includes(token) && /\(\s*row\s*,\s*$/.test(before) && /^\s*[,)]/.test(after)) return true;
    if (['val','value'].includes(token) && /\(\s*row\s*,\s*(col|column)\s*,\s*$/.test(before) && /^\s*\)/.test(after)) return true;
    if (['Linear', 'list'].includes(token) && (/(Linear|linked)\s+$/i.test(before) || /^\s+list\b/.test(after))) return true;
    if (token === 'Node' && /[（(]\s*$/.test(before) && /^\s*[）)]/.test(after)) return true;
    return ['row','col','column'].includes(token) && /^\s*[＝=：:]\s*[列欄]/.test(after);
  };
  window.chapterFormatCode = html => {
    const template = document.createElement('template');
    template.innerHTML = html;
    const walker = document.createTreeWalker(template.content, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (!node.parentElement?.closest('code,pre,script,style,svg,.pseudo-code,mjx-container')) nodes.push(node);
    }
    for (const node of nodes) {
      const replacement = document.createDocumentFragment();
      for (const part of node.data.split(/(\$\$[\s\S]*?\$\$|\$[^$]*\$)/g)) {
        if (part.startsWith('$')) { replacement.append(document.createTextNode(part)); continue; }
        let last = 0;
        for (const match of part.matchAll(tokens)) {
          replacement.append(document.createTextNode(part.slice(last, match.index)));
          if (isTermProse(match[0],part.slice(0,match.index),part.slice(match.index+match[0].length))) {
            replacement.append(document.createTextNode(match[0]));
          } else {
            const code = document.createElement('code');code.textContent = match[0];replacement.append(code);
          }
          last = match.index + match[0].length;
        }
        replacement.append(document.createTextNode(part.slice(last)));
      }
      node.replaceWith(replacement);
    }
    return template.innerHTML;
  };
})();
