// Main 4 — China and Korea flags, a peninsula, a linked chip chain.
const C = '#efe4cf';
const T = '#e4d5ba';
const I = '#1c140e';
const R = '#8f1d1a';
const Y = '#f0c400';
const B = '#1a56c4';
const W = '#fbf7f0';

function star(cx, cy, r, rot) {
  const p = [];
  for (let i = 0; i < 10; i++) {
    const a = rot + (i * Math.PI) / 5;
    const rad = i % 2 === 0 ? r : r * 0.4;
    p.push(`${(cx + Math.cos(a) * rad).toFixed(1)},${(cy + Math.sin(a) * rad).toFixed(1)}`);
  }
  return `<polygon points="${p.join(' ')}" fill="${Y}"/>`;
}

function china(x, y, w, h) {
  const X = (u) => x + (u / 30) * w;
  const Yc = (v) => y + (v / 20) * h;
  let out = `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${R}"/>`;
  out += star(X(5), Yc(5), (3 / 20) * h, -Math.PI / 2);
  for (const [u, v] of [[10, 2], [12, 4], [12, 7], [10, 9]]) {
    const ang = Math.atan2(Yc(5) - Yc(v), X(5) - X(u));
    out += star(X(u), Yc(v), Math.max(2.1, (1 / 20) * h), ang);
  }
  return out;
}

function bars(cx, cy, parts) {
  return parts.map((part, i) => {
    const yy = (cy + (i - 1) * 3.2).toFixed(1);
    if (part) return `<rect x="${cx - 5}" y="${yy}" width="10" height="1.7" fill="${I}"/>`;
    return `<rect x="${cx - 5}" y="${yy}" width="4" height="1.7" fill="${I}"/><rect x="${cx + 1}" y="${yy}" width="4" height="1.7" fill="${I}"/>`;
  }).join('');
}

function korea(x, y) {
  return `<rect x="${x}" y="${y}" width="54" height="36" fill="${W}" stroke="${I}" stroke-width="1"/>
<circle cx="${x + 27}" cy="${y + 18}" r="8" fill="${R}"/>
<path d="M${x + 27} ${y + 10} A8 8 0 0 0 ${x + 27} ${y + 26} A4 4 0 0 0 ${x + 27} ${y + 18} A4 4 0 0 1 ${x + 27} ${y + 10}" fill="${B}"/>
${bars(x + 8, y + 7, [1, 1, 1])}
${bars(x + 8, y + 29, [1, 0, 1])}
${bars(x + 46, y + 7, [0, 1, 0])}
${bars(x + 46, y + 29, [0, 0, 0])}`;
}

function chip(x) {
  return `<rect x="${x}" y="12" width="26" height="16" fill="${T}" stroke="${I}" stroke-width="1.4"/>
<rect x="${x + 8}" y="16" width="10" height="8" fill="${I}"/>`;
}

export function s4() {
  return `<svg viewBox="0 0 320 40" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
<rect width="320" height="40" fill="${C}"/>
${china(2, 2, 54, 36)}
${korea(60, 2)}
<path d="M124 3 L146 4 L150 12 L144 16 L148 22 L140 28 L134 37 L128 28 L120 26 L116 16 L120 8 Z" fill="${I}"/>
<rect x="172" y="18" width="112" height="3" fill="${I}"/>
${chip(176)}${chip(218)}${chip(260)}
</svg>`;
}
