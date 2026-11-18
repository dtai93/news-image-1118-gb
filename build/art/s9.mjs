// Main 9 — server rack, one amber light, a check mark.
const C = '#efe4cf';
const T = '#e4d5ba';
const I = '#1c140e';
const R = '#8f1d1a';
const Y = '#f0c400';
const W = '#fbf7f0';

function rack(x, amber) {
  let lights = '';
  for (let row = 0; row < 4; row++) {
    for (let col = 0; col < 3; col++) {
      const on = amber && row === 1 && col === 1;
      const fill = on ? Y : (row + col) % 2 === 0 ? I : T;
      lights += `<rect x="${x + 7 + col * 12}" y="${14 + row * 12}" width="8" height="6" fill="${fill}"/>`;
    }
  }
  return `<rect x="${x}" y="6" width="46" height="54" fill="${W}" stroke="${I}" stroke-width="1.6"/>${lights}`;
}

export function s9() {
  return `<svg viewBox="0 0 320 65" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
<rect width="320" height="65" fill="${C}"/>
${rack(8, false)}${rack(60, true)}${rack(112, false)}
<path d="M188 36 l22 20 62 -46" fill="none" stroke="${R}" stroke-width="8" stroke-linecap="square" stroke-linejoin="miter"/>
</svg>`;
}
