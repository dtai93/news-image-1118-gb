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
    out += star(X(u), Yc(v), Math.max(2.2, (1 / 20) * h), ang);
  }
  return out;
}

function bars(cx, cy, parts) {
  return parts.map((part, i) => {
    const yy = (cy + (i - 1) * 4.2).toFixed(1);
    if (part) return `<rect x="${cx - 6}" y="${yy}" width="12" height="2.2" fill="${I}"/>`;
    return `<rect x="${cx - 6}" y="${yy}" width="5" height="2.2" fill="${I}"/><rect x="${cx + 1}" y="${yy}" width="5" height="2.2" fill="${I}"/>`;
  }).join('');
}

function korea(x, y) {
  return `<rect x="${x}" y="${y}" width="72" height="48" fill="${W}" stroke="${I}" stroke-width="1.4"/>
<circle cx="${x + 36}" cy="${y + 24}" r="10" fill="${R}"/>
<path d="M${x + 36} ${y + 14} A10 10 0 0 0 ${x + 36} ${y + 34} A5 5 0 0 0 ${x + 36} ${y + 24} A5 5 0 0 1 ${x + 36} ${y + 14}" fill="${B}"/>
${bars(x + 12, y + 10, [1, 1, 1])}
${bars(x + 12, y + 38, [1, 0, 1])}
${bars(x + 60, y + 10, [0, 1, 0])}
${bars(x + 60, y + 38, [0, 0, 0])}`;
}

function chip(x) {
  return `<rect x="${x}" y="22" width="30" height="22" fill="${T}" stroke="${I}" stroke-width="1.5"/>
<rect x="${x + 9}" y="28" width="12" height="10" fill="${I}"/>
<rect x="${x + 5}" y="17" width="3" height="6" fill="${I}"/>
<rect x="${x + 14}" y="17" width="3" height="6" fill="${I}"/>
<rect x="${x + 22}" y="17" width="3" height="6" fill="${I}"/>`;
}

export function s4() {
  return `<svg viewBox="0 0 320 65" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
<rect width="320" height="65" fill="${C}"/>
${china(2, 8, 72, 48)}
${korea(78, 8)}
<path d="M174 4 L184 10 L186 26 L194 38 L188 52 L180 62 L166 60 L160 44 L166 28 L164 12 Z" fill="${I}"/>
<rect x="204" y="32" width="108" height="4" fill="${I}"/>
${chip(206)}${chip(244)}${chip(282)}
</svg>`;
}
