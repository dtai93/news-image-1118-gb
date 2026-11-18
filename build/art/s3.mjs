// Lead 3 — green chip, a crossed return arrow, a bar marked 116.
const C = '#efe4cf';
const T = '#e4d5ba';
const I = '#1c140e';
const R = '#8f1d1a';
const G = '#0d7a3a';

function segs(n, x, y, h, fill) {
  const w = h * 0.58;
  const t = h * 0.16;
  const map = ['1111110', '0110000', '1101101', '1111001', '0110011', '1011011', '1011111', '1110000', '1111111', '1111011'];
  let out = '';
  const s = String(n);
  for (let i = 0; i < s.length; i++) {
    const m = map[Number(s[i])];
    const dx = x + i * (w + t);
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

export function s3() {
  let pins = '';
  for (let i = 0; i < 7; i++) {
    const y = 36 + i * 13;
    pins += `<rect x="22" y="${y}" width="16" height="6" fill="${I}"/><rect x="214" y="${y}" width="16" height="6" fill="${I}"/>`;
  }
  return `<svg viewBox="0 0 320 156" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
<rect width="320" height="156" fill="${C}"/>
${pins}
<rect x="38" y="26" width="176" height="104" fill="${G}"/>
<rect x="62" y="44" width="128" height="68" fill="${I}"/>
<rect x="74" y="78" width="104" height="26" fill="${T}"/>
${segs(116, 82, 80, 22, I)}
<path d="M248 118 H300 V62" fill="none" stroke="${R}" stroke-width="8"/>
<polygon points="300,46 286,66 314,66" fill="${R}"/>
<path d="M256 52 L316 128" stroke="${I}" stroke-width="8"/>
</svg>`;
}
