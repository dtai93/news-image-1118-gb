// Main 10 — gavel, UK flag, a row of small houses.
const C = '#efe4cf';
const T = '#e4d5ba';
const I = '#1c140e';
const R = '#8f1d1a';
const B = '#1a56c4';
const W = '#fbf7f0';

function jack(x, y, w, h) {
  const cx = x + w / 2;
  const cy = y + h / 2;
  const salt = w * 0.16;
  const cross = w * 0.2;
  const red = w * 0.1;
  return `<clipPath id="uj"><rect x="${x}" y="${y}" width="${w}" height="${h}"/></clipPath>
<g clip-path="url(#uj)">
<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${B}"/>
<path d="M${x} ${y} L${x + w} ${y + h} M${x + w} ${y} L${x} ${y + h}" stroke="${W}" stroke-width="${salt}"/>
<path d="M${x} ${y} L${x + w} ${y + h} M${x + w} ${y} L${x} ${y + h}" stroke="${R}" stroke-width="${salt * 0.42}"/>
<rect x="${cx - cross / 2}" y="${y}" width="${cross}" height="${h}" fill="${W}"/>
<rect x="${x}" y="${cy - cross / 2}" width="${w}" height="${cross}" fill="${W}"/>
<rect x="${cx - red / 2}" y="${y}" width="${red}" height="${h}" fill="${R}"/>
<rect x="${x}" y="${cy - red / 2}" width="${w}" height="${red}" fill="${R}"/>
</g>`;
}

function house(x) {
  return `<polygon points="${x},30 ${x + 12},18 ${x + 24},30" fill="${R}"/>
<rect x="${x + 2}" y="30" width="20" height="16" fill="${T}" stroke="${I}" stroke-width="1.2"/>
<rect x="${x + 8}" y="36" width="7" height="10" fill="${I}"/>`;
}

export function s10() {
  const row = [168, 196, 224, 252, 280].map(house).join('');
  return `<svg viewBox="0 0 320 65" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
<rect width="320" height="65" fill="${C}"/>
${jack(4, 8, 78, 50)}
<polygon points="96,16 132,8 138,18 102,26" fill="${T}" stroke="${I}" stroke-width="1.4"/>
<polygon points="112,22 120,19 136,52 128,55" fill="${I}"/>
${row}
</svg>`;
}
