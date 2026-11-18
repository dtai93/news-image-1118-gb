// Lead 1 — podium, China flag, open gate, ring of 21 trade arrows.
const C = '#efe4cf';
const T = '#e4d5ba';
const I = '#1c140e';
const R = '#8f1d1a';
const Y = '#f0c400';

function star(cx, cy, r, rot) {
  const p = [];
  for (let i = 0; i < 10; i++) {
    const a = rot + (i * Math.PI) / 5;
    const rad = i % 2 === 0 ? r : r * 0.38;
    p.push(`${(cx + Math.cos(a) * rad).toFixed(1)},${(cy + Math.sin(a) * rad).toFixed(1)}`);
  }
  return `<polygon points="${p.join(' ')}" fill="${Y}"/>`;
}

export function s1() {
  const fx = 24;
  const fy = 22;
  const fw = 90;
  const fh = 60;
  const X = (u) => fx + (u / 30) * fw;
  const Yc = (v) => fy + (v / 20) * fh;
  const big = star(X(5), Yc(5), (3 / 20) * fh, -Math.PI / 2);
  const small = [[10, 2], [12, 4], [12, 7], [10, 9]].map(([u, v]) => {
    const ang = Math.atan2(Yc(5) - Yc(v), X(5) - X(u));
    return star(X(u), Yc(v), (1 / 20) * fh, ang);
  }).join('');
  const cx = 276;
  const cy = 58;
  let arrows = '';
  for (let i = 0; i < 21; i++) {
    const a = (i / 21) * Math.PI * 2;
    const x = cx + Math.cos(a) * 34;
    const y = cy + Math.sin(a) * 34;
    const deg = (a * 180) / Math.PI + 180;
    arrows += `<polygon points="0,-6 2.5,4 -2.5,4" fill="${R}" transform="translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${deg.toFixed(1)})"/>`;
  }
  return `<svg viewBox="0 0 320 156" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
<rect width="320" height="156" fill="${C}"/>
<rect x="${fx - 4}" y="${fy}" width="4" height="124" fill="${I}"/>
<rect x="${fx}" y="${fy}" width="${fw}" height="${fh}" fill="${R}"/>
${big}${small}
<rect x="140" y="72" width="6" height="74" fill="${I}"/>
<rect x="196" y="72" width="6" height="74" fill="${I}"/>
<path d="M143 76 L126 142" fill="none" stroke="${I}" stroke-width="6"/>
<path d="M199 76 L226 142" fill="none" stroke="${I}" stroke-width="6"/>
<rect x="132" y="140" width="78" height="12" fill="${T}" stroke="${I}" stroke-width="2"/>
<rect x="142" y="128" width="58" height="12" fill="${T}" stroke="${I}" stroke-width="2"/>
<rect x="152" y="116" width="38" height="12" fill="${T}" stroke="${I}" stroke-width="2"/>
<circle cx="${cx}" cy="${cy}" r="34" fill="none" stroke="${T}" stroke-width="11"/>
${arrows}
</svg>`;
}
