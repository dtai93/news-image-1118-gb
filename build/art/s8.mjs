// Main 8 — sun, a draft paper marked 2030, a small Australia map.
const C = '#efe4cf';
const I = '#1c140e';
const R = '#8f1d1a';
const Y = '#f0c400';
const W = '#fbf7f0';

function segs(n, x, y, h, fill) {
  const w = h * 0.56;
  const t = Math.max(2, h * 0.16);
  const map = ['1111110', '0110000', '1101101', '1111001', '0110011', '1011011', '1011111', '1110000', '1111111', '1111011'];
  let out = '';
  const s = String(n);
  for (let i = 0; i < s.length; i++) {
    const m = map[Number(s[i])];
    const dx = x + i * (w + t);
    const b = [
      [dx, y, w, t], [dx + w - t, y, t, h / 2], [dx + w - t, y + h / 2, t, h / 2],
      [dx, y + h - t, w, t], [dx, y + h / 2, t, h / 2], [dx, y, t, h / 2],
      [dx, y + (h - t) / 2, w, t],
    ];
    for (let k = 0; k < 7; k++) if (m[k] === '1') {
      const [rx, ry, rw, rh] = b[k];
      out += `<rect x="${rx.toFixed(1)}" y="${ry.toFixed(1)}" width="${rw.toFixed(1)}" height="${rh.toFixed(1)}" fill="${fill}"/>`;
    }
  }
  return out;
}

function rays(cx, cy, r0, r1) {
  let out = '';
  for (let i = 0; i < 8; i++) {
    const a = (i / 8) * Math.PI * 2;
    const x1 = cx + Math.cos(a) * r0;
    const y1 = cy + Math.sin(a) * r0;
    const x2 = cx + Math.cos(a) * r1;
    const y2 = cy + Math.sin(a) * r1;
    out += `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="${Y}" stroke-width="3.5"/>`;
  }
  return out;
}

export function s8() {
  return `<svg viewBox="0 0 320 65" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
<rect width="320" height="65" fill="${C}"/>
${rays(40, 34, 16, 28)}
<circle cx="40" cy="34" r="13" fill="${Y}" stroke="${I}" stroke-width="1.5"/>
<path d="M108 34 L100 20 L112 12 L120 2 L128 14 L140 10 L132 28 L150 16 L168 20 L174 34 L164 50 L136 56 L110 52 L98 40 Z" fill="${I}"/>
<path d="M150 54 L164 52 L168 62 L152 63 Z" fill="${I}"/>
<rect x="196" y="6" width="116" height="52" fill="${W}" stroke="${I}" stroke-width="1.6"/>
<rect x="196" y="6" width="116" height="10" fill="${R}"/>
${segs(2030, 214, 22, 30, I)}
</svg>`;
}
