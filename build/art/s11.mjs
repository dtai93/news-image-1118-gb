// Main 11 — courtroom bench and a calendar block reading 330.
const C = '#efe4cf';
const T = '#e4d5ba';
const I = '#1c140e';
const R = '#8f1d1a';
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

export function s11() {
  return `<svg viewBox="0 0 320 65" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
<rect width="320" height="65" fill="${C}"/>
<rect x="8" y="8" width="168" height="12" fill="${I}"/>
<rect x="18" y="20" width="148" height="30" fill="${T}" stroke="${I}" stroke-width="1.6"/>
<rect x="30" y="26" width="124" height="8" fill="${W}"/>
<rect x="36" y="50" width="16" height="10" fill="${I}"/>
<rect x="132" y="50" width="16" height="10" fill="${I}"/>
<rect x="196" y="6" width="116" height="54" fill="${W}" stroke="${I}" stroke-width="1.8"/>
<rect x="196" y="6" width="116" height="12" fill="${R}"/>
${segs(330, 214, 24, 30, I)}
</svg>`;
}
