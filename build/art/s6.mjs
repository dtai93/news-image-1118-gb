// Main 6 — Alaska outline, a ballot, and the figures 56 and 44.
const C = '#efe4cf';
const T = '#e4d5ba';
const I = '#1c140e';
const R = '#8f1d1a';

function segs(n, x, y, h, fill) {
  const w = h * 0.56;
  const t = Math.max(2, h * 0.18);
  const map = ['1111110', '0110000', '1101101', '1111001', '0110011', '1011011', '1011111', '1110000', '1111111', '1111011'];
  let out = '';
  const s = String(n);
  for (let i = 0; i < s.length; i++) {
    const m = map[Number(s[i])];
    const dx = x + i * (w + t * 0.8);
    const box = [
      [dx, y, w, t],
      [dx + w - t, y, t, h / 2],
      [dx + w - t, y + h / 2, t, h / 2],
      [dx, y + h - t, w, t],
      [dx, y + h / 2, t, h / 2],
      [dx, y, t, h / 2],
      [dx, y + (h - t) / 2, w, t],
    ];
    for (let k = 0; k < 7; k++) {
      if (m[k] === '1') {
        const [rx, ry, rw, rh] = box[k];
        out += `<rect x="${rx.toFixed(1)}" y="${ry.toFixed(1)}" width="${rw.toFixed(1)}" height="${rh.toFixed(1)}" fill="${fill}"/>`;
      }
    }
  }
  return out;
}

export function s6() {
  return `<svg viewBox="0 0 320 40" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
<rect width="320" height="40" fill="${C}"/>
<path d="M40 4 h28 l8 7 -6 3 5 4 -5 2 -6 -3 -6 3 -4 7 -7 -3 -8 2 -6 -5 3 -4 -2 -5 8 -3 z" fill="${I}"/>
<path d="M68 16 l8 7 3 12 -6 1 -3 -11 -5 -4 z" fill="${I}"/>
<circle cx="16" cy="26" r="2.1" fill="${I}"/>
<circle cx="8" cy="31" r="1.7" fill="${I}"/>
<circle cx="24" cy="22" r="1.8" fill="${I}"/>
<rect x="96" y="5" width="26" height="30" fill="${T}" stroke="${I}" stroke-width="1.7"/>
<path d="M101 20 l6 7 12 -14" fill="none" stroke="${R}" stroke-width="2.6"/>
${segs(56, 132, 6, 28, I)}
<rect x="178" y="18" width="12" height="4" fill="${I}"/>
${segs(44, 196, 6, 28, I)}
</svg>`;
}
