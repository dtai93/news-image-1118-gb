// Lead 2 — Kuwait coast, two intercepted drones, a radar dish.
const C = '#efe4cf';
const T = '#e4d5ba';
const I = '#1c140e';
const R = '#8f1d1a';
const G = '#0d7a3a';
const W = '#fbf7f0';
const S = '#5c5146';

function flag(x, y, w) {
  const h = w / 2;
  const u = w / 4;
  return `<rect x="${x}" y="${y}" width="${w}" height="${h / 3}" fill="${G}"/>
<rect x="${x}" y="${y + h / 3}" width="${w}" height="${h / 3}" fill="${W}"/>
<rect x="${x}" y="${y + (2 * h) / 3}" width="${w}" height="${h / 3}" fill="${R}"/>
<polygon points="${x},${y} ${x + u},${y + h / 3} ${x + u},${y + (2 * h) / 3} ${x},${y + h}" fill="${I}"/>`;
}

function drone(x, y) {
  const arm = (dx, dy) => `<line x1="${x}" y1="${y}" x2="${x + dx}" y2="${y + dy}" stroke="${I}" stroke-width="3"/>
<circle cx="${x + dx}" cy="${y + dy}" r="4.5" fill="${I}"/>`;
  return `${arm(-18, -12)}${arm(18, -12)}${arm(-18, 12)}${arm(18, 12)}
<rect x="${x - 8}" y="${y - 5}" width="16" height="10" fill="${I}"/>
<path d="M${x - 14} ${y - 14} l28 28 M${x + 14} ${y - 14} l-28 28" stroke="${R}" stroke-width="2.5"/>`;
}

export function s2() {
  return `<svg viewBox="0 0 320 156" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
<rect width="320" height="156" fill="${C}"/>
<path d="M0 100 Q90 86 170 102 T320 92 V156 H0 Z" fill="${T}"/>
<rect y="126" width="320" height="30" fill="${S}"/>
<rect x="12" y="18" width="4" height="112" fill="${I}"/>
${flag(16, 22, 116)}
${drone(176, 36)}
${drone(228, 68)}
<path d="M248 114 A 30 30 0 0 1 308 114 Z" fill="${T}" stroke="${I}" stroke-width="2.5"/>
<rect x="276" y="114" width="4" height="16" fill="${I}"/>
<rect x="260" y="128" width="36" height="5" fill="${I}"/>
<path d="M278 108 L228 74" stroke="${R}" stroke-width="2.5"/>
</svg>`;
}
