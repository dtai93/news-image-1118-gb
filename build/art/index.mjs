import { s1 } from './s1.mjs';
import { s2 } from './s2.mjs';
import { s3 } from './s3.mjs';
import { s4 } from './s4.mjs';
import { s5 } from './s5.mjs';
import { s6 } from './s6.mjs';

const byN = { 1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6 };

function fallback(n, kind) {
  const shift = (n % 4) * 14;
  if (kind === 'main') {
    return `<svg viewBox="0 0 320 40" preserveAspectRatio="xMidYMid meet" aria-hidden="true"><rect width="320" height="40" fill="#efe4cf"/><circle cx="${250 + shift}" cy="20" r="12" fill="#8f1d1a"/><rect x="28" y="11" width="78" height="7" fill="#1c140e"/><rect x="28" y="23" width="52" height="5" fill="#5c5146"/></svg>`;
  }
  return `<svg viewBox="0 0 320 150" preserveAspectRatio="xMidYMid meet" aria-hidden="true"><rect width="320" height="150" fill="#efe4cf"/><rect y="116" width="320" height="34" fill="#e4d5ba"/><circle cx="${92 + shift}" cy="66" r="34" fill="#8f1d1a"/><rect x="160" y="46" width="130" height="14" fill="#1c140e"/><rect x="160" y="70" width="96" height="10" fill="#5c5146"/><rect x="160" y="88" width="64" height="10" fill="#5c5146"/></svg>`;
}

export function artFor(n, kind) {
  const draw = byN[n];
  return draw ? draw() : fallback(n, kind);
}
