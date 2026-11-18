// Reads data/stories.json and writes build/page.html (1024×1024).
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const { stories } = JSON.parse(readFileSync(join(root, 'data/stories.json'), 'utf8'));
const leads = stories.filter((s) => s.tier === 'lead');
const mains = stories.filter((s) => s.tier === 'main');
const also = stories.filter((s) => s.tier === 'also');
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;',
}[c]));

function motif(n, kind) {
  const shift = (n % 4) * 14;
  if (kind === 'main') {
    return `<svg viewBox="0 0 320 40" preserveAspectRatio="xMidYMid meet" aria-hidden="true"><rect width="320" height="40" fill="#efe4cf"/><circle cx="${250 + shift}" cy="20" r="12" fill="#8f1d1a"/><rect x="28" y="11" width="78" height="7" fill="#1c140e"/><rect x="28" y="23" width="52" height="5" fill="#5c5146"/></svg>`;
  }
  return `<svg viewBox="0 0 320 150" preserveAspectRatio="xMidYMid meet" aria-hidden="true"><rect width="320" height="150" fill="#efe4cf"/><rect y="116" width="320" height="34" fill="#e4d5ba"/><circle cx="${92 + shift}" cy="66" r="34" fill="#8f1d1a"/><rect x="160" y="46" width="130" height="14" fill="#1c140e"/><rect x="160" y="70" width="96" height="10" fill="#5c5146"/><rect x="160" y="88" width="64" height="10" fill="#5c5146"/></svg>`;
}

function card(s, kind) {
  const H = kind === 'lead' ? 'h2' : 'h3';
  return `<article class="${kind}"><div class="art">${motif(s.n, kind)}<b class="pin">${s.n}</b></div><p class="tag">${s.n} · ${esc(s.region)} · ${esc(s.field)}</p><${H}>${esc(s.headline)}</${H}><p class="dek">${esc(s.dek)}</p></article>`;
}

const sources = [...new Set(stories.map((s) => s.source))].sort((a, b) => a.localeCompare(b));
const mid = Math.ceil(also.length / 2);
const alsoCol = (list) => list.map((s) => `<p class="also-item"><b>${s.n}</b> ${esc(s.headline)}</p>`).join('');
const srcLine = `Every story was reported on Wednesday 18 November 2026; disputed claims are attributed. Sources: ${sources.join(', ')}.`;

const css = `
*{box-sizing:border-box}
html,body{margin:0;width:1024px;height:1024px;overflow:hidden;background:#f4efe6}
.page{width:1024px;height:1024px;padding:6px 8px 5px;display:grid;
  grid-template-rows:82px 240px 330px 299px 46px;gap:4px;
  background:#f4efe6;color:#1c140e;
  font-family:"Source Sans Pro",Inter,Roboto,"DejaVu Sans",sans-serif}
.mast{display:flex;flex-direction:column;justify-content:flex-end;min-height:0}
.kicker{display:flex;justify-content:space-between;align-items:baseline;height:16px}
.kicker b{font-size:13px;line-height:16px;letter-spacing:.08em;font-weight:700}
.kicker span{font-size:12px;line-height:16px;font-weight:700;letter-spacing:.04em}
.date{margin:0;font-family:"Playfair Display","Source Serif Pro","DejaVu Serif",serif;
  font-weight:700;font-size:46px;line-height:50px;height:50px;letter-spacing:-.015em}
.rules{height:6px;border-top:3px solid #1c140e;border-bottom:1px solid #1c140e;margin-top:3px}
.leads,.mains{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;min-height:0}
.mains{grid-template-rows:repeat(3,108px);gap:3px}
.lead,.main{border:1px solid #1c140e;background:#fbf7f0;min-height:0;overflow:hidden;
  display:grid;padding:4px 6px 3px;gap:2px}
.lead{grid-template-rows:156px 14px 20px 1fr}
.main{grid-template-rows:40px 13px 18px 1fr;padding:3px 5px 2px;gap:1px}
.art{position:relative;overflow:hidden;background:#efe4cf;min-height:0}
.art svg{display:block;width:100%;height:100%}
.pin{position:absolute;top:3px;left:3px;background:#8f1d1a;color:#fbf7f0;
  font-size:12px;line-height:16px;min-width:18px;text-align:center;padding:0 3px;font-weight:700}
.tag{margin:0;color:#8f1d1a;font-size:11px;line-height:13px;font-weight:700;letter-spacing:.03em;
  white-space:nowrap;overflow:hidden}
.lead h2{margin:0;font-family:"Playfair Display","Source Serif Pro",serif;font-weight:700;
  font-size:16px;line-height:20px;white-space:nowrap;overflow:hidden}
.main h3{margin:0;font-size:16px;line-height:18px;font-weight:700;white-space:nowrap;overflow:hidden}
.dek{margin:0;font-size:11px;line-height:13px;max-height:26px;overflow:hidden}
.band{display:grid;grid-template-columns:360px 1fr;gap:8px;min-height:0}
.map,.also{border:1px solid #1c140e;background:#fbf7f0;min-height:0;display:flex;flex-direction:column;padding:4px 6px 4px}
.sec{margin:0;height:16px;font-size:12px;line-height:16px;font-weight:700;letter-spacing:.06em}
.map-frame{flex:1;min-height:0;background:#efe4cf;position:relative;margin-top:3px}
.map-frame svg{display:block;width:100%;height:100%}
.map-cap{position:absolute;left:8px;bottom:6px;margin:0;font-size:12px;line-height:14px;font-weight:700}
.also-cols{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:0 10px;min-height:0;margin-top:2px}
.also-col+.also-col{border-left:1px solid #1c140e;padding-left:8px}
.also-item{margin:0;font-size:12px;line-height:17px;height:17px;white-space:nowrap;overflow:hidden}
.also-item b{color:#8f1d1a;font-weight:700}
.foot{min-height:0;border-top:2px solid #1c140e;padding-top:3px}
.foot p{margin:0;font-size:11px;line-height:13px}
.foot .note{margin-top:1px}
.foot .note b{color:#8f1d1a}
`;

const mapSvg = `<svg viewBox="0 0 360 240" preserveAspectRatio="xMidYMid meet" aria-hidden="true"><rect width="360" height="240" fill="#efe4cf"/><ellipse cx="180" cy="112" rx="150" ry="70" fill="none" stroke="#1c140e" stroke-width="2"/><ellipse cx="180" cy="112" rx="70" ry="70" fill="none" stroke="#1c140e" stroke-width="1"/><path d="M30 112 H330 M180 42 V182" fill="none" stroke="#1c140e" stroke-width="1"/></svg>`;

const html = `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Wednesday 18 November 2026</title><style>${css}</style></head><body><div class="page">
<header class="mast"><div class="kicker"><b>THE DAY IN WORLD NEWS</b><span>${stories.length} STORIES · 6 CONTINENTS</span></div><h1 class="date">Wednesday 18 November 2026</h1><div class="rules"></div></header>
<section class="leads">${leads.map((s) => card(s, 'lead')).join('')}</section>
<section class="mains">${mains.map((s) => card(s, 'main')).join('')}</section>
<section class="band"><aside class="map"><p class="sec">WHERE IT HAPPENED</p><div class="map-frame">${mapSvg}<p class="map-cap">40 datelines</p></div></aside>
<section class="also"><p class="sec">ALSO ON WEDNESDAY 18 NOVEMBER</p><div class="also-cols"><div class="also-col">${alsoCol(also.slice(0, mid))}</div><div class="also-col">${alsoCol(also.slice(mid))}</div></div></section></section>
<footer class="foot"><p>${esc(srcLine)}</p><p class="note"><b>JUDGE NOTE</b> Wednesday 18 November 2026 only. Disputed claims stay attributed to the outlet that reported them.</p></footer>
</div></body></html>`;

mkdirSync(join(root, 'build'), { recursive: true });
writeFileSync(join(root, 'build/page.html'), html);
console.log('wrote build/page.html', stories.length, 'stories');
