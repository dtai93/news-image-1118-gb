// Reads data/stories.json and writes build/page.html (1024×1024).
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { artFor } from './art/index.mjs';
import { mapSvg, MAP_LEGEND } from './map.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const { stories } = JSON.parse(readFileSync(join(root, 'data/stories.json'), 'utf8'));
const leads = stories.filter((s) => s.tier === 'lead');
const mains = stories.filter((s) => s.tier === 'main');
const also = stories.filter((s) => s.tier === 'also');
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;',
}[c]));

function motif(n, kind) {
  return artFor(n, kind);
}

const FIELD_COLOR = {
  DIPLOMACY: '#1a4f8b',
  'IRAN WAR': '#8f1d1a',
  TECH: '#1d6b3a',
  POLITICS: '#6b3fa0',
  HEALTH: '#c45c12',
  CLIMATE: '#0e7c6b',
  COURTS: '#3d3428',
  ENERGY: '#a67c00',
};
const KEY = [
  ['DIPLOMACY', 'Diplomacy'],
  ['IRAN WAR', 'War'],
  ['POLITICS', 'Politics'],
  ['TECH', 'Tech'],
  ['HEALTH', 'Health'],
  ['CLIMATE', 'Climate'],
  ['COURTS', 'Courts'],
  ['ENERGY', 'Energy'],
];

function dekHtml(text) {
  return esc(text).replace(/(\d+)-(\d+)/g, '<span class="nb">$1-$2</span>');
}

function card(s, kind) {
  const H = kind === 'lead' ? 'h2' : 'h3';
  const color = FIELD_COLOR[s.field] || '#1c140e';
  return `<article class="${kind}" style="--c:${color}"><div class="art">${motif(s.n, kind)}<b class="pin">${s.n}</b></div><div class="copy"><p class="tag">${s.n} · ${esc(s.region)} · ${esc(s.field)}</p><${H}>${esc(s.headline)}</${H}><p class="dek">${dekHtml(s.dek)}</p></div></article>`;
}

const sources = [...new Set(stories.map((s) => s.source))].sort((a, b) => a.localeCompare(b));
const mid = Math.ceil(also.length / 2);
const alsoCol = (list) => list.map((s) => `<p class="also-item"><b>${s.n}</b> ${esc(s.headline)}</p>`).join('');
const srcLine = `Sources: ${sources.join(', ')}. Original drawings.`;
const keyHtml = KEY.map(([field, label]) => `<span style="--c:${FIELD_COLOR[field]}"><i></i>${label}</span>`).join('');

const css = `
*{box-sizing:border-box}
html,body{margin:0;width:1024px;height:1024px;overflow:hidden;background:#f4efe6}
.page{width:1024px;height:1024px;padding:6px 8px 5px;display:grid;
  grid-template-rows:90px 272px 360px 210px 65px;gap:4px;
  background:#f4efe6;color:#1c140e;
  font-family:"Source Sans Pro",Inter,Roboto,"DejaVu Sans",sans-serif}
.mast{display:flex;flex-direction:column;justify-content:flex-end;min-height:0}
.kicker{display:flex;justify-content:space-between;align-items:baseline;height:15px}
.kicker b{font-size:13px;line-height:15px;letter-spacing:.08em;font-weight:700}
.kicker span{font-size:12px;line-height:15px;font-weight:700;letter-spacing:.04em}
.date{margin:0;font-family:"Playfair Display","Source Serif Pro","DejaVu Serif",serif;
  font-weight:700;font-size:42px;line-height:44px;height:44px;letter-spacing:-.015em}
.key{display:flex;justify-content:space-between;align-items:center;height:14px;margin-top:1px}
.key span{display:flex;align-items:center;font-size:11px;line-height:14px;font-weight:700}
.key i{display:block;width:8px;height:8px;margin-right:3px;background:var(--c)}
.rules{height:6px;border-top:3px solid #1c140e;border-bottom:1px solid #1c140e;margin-top:2px}
.leads{display:grid;grid-template-rows:repeat(3,88px);gap:4px;min-height:0}
.mains{display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,118px);gap:3px;min-height:0}
.lead,.main{border:1px solid #1c140e;border-left:6px solid var(--c);background:#fbf7f0;min-height:0;overflow:hidden}
.lead{display:grid;grid-template-columns:186px 1fr;gap:8px;padding:4px 8px 3px 4px}
.lead .copy{display:flex;flex-direction:column;justify-content:center;min-width:0}
.main{display:grid;grid-template-rows:50px 13px 16px 26px;padding:2px 5px 1px;gap:1px}
.main .copy{display:contents}
.art{position:relative;overflow:hidden;background:#efe4cf;min-height:0}
.art svg{display:block;width:100%;height:100%}
.pin{position:absolute;top:3px;left:3px;background:#8f1d1a;color:#fbf7f0;
  font-size:12px;line-height:16px;min-width:18px;text-align:center;padding:0 3px;font-weight:700}
.tag{margin:0;color:#8f1d1a;font-size:12px;line-height:13px;font-weight:700;letter-spacing:.02em;
  white-space:nowrap;overflow:hidden}
.lead h2{margin:0;font-family:"Playfair Display","Source Serif Pro",serif;font-weight:700;
  font-size:36px;line-height:38px;white-space:nowrap;overflow:hidden}
.main h3{margin:0;font-size:15px;line-height:16px;font-weight:700;white-space:nowrap;overflow:hidden}
.lead .dek{margin:0;font-size:15px;line-height:17px;height:17px;white-space:nowrap;overflow:hidden}
.main .dek{margin:0;font-size:11px;line-height:13px;max-height:26px;overflow:hidden}
.nb{white-space:nowrap}
.band{display:grid;grid-template-columns:40fr 60fr;gap:6px;min-height:0}
.map,.also{border:1px solid #1c140e;background:#fbf7f0;min-height:0;display:flex;flex-direction:column;padding:3px 6px 3px}
.sec{margin:0;height:14px;font-size:12px;line-height:14px;font-weight:700;letter-spacing:.05em}
.map-frame{flex:1;min-height:0;background:#d7e3ea;position:relative;margin-top:2px}
.map-frame svg{display:block;width:100%;height:100%}
.map-cap{position:absolute;left:4px;right:4px;bottom:1px;margin:0;font-size:10px;line-height:12px;font-weight:700;white-space:nowrap;overflow:hidden}
.also-cols{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:0 8px;min-height:0;margin-top:1px}
.also-col+.also-col{border-left:1px solid #1c140e;padding-left:6px}
.also-item{margin:0;font-size:11px;line-height:13px;height:13px;white-space:nowrap;overflow:hidden;padding-right:4px}
.also-item b{color:#8f1d1a;font-weight:700}
.foot{min-height:0;display:flex;flex-direction:column;justify-content:flex-end;gap:2px;border-top:2px solid #1c140e;padding-top:2px}
.src{margin:0;font-size:11px;line-height:13px;white-space:nowrap;overflow:hidden}
.judge{border:1.5px solid #8f1d1a;background:#fbf7f0;padding:1px 6px 2px;margin:0}
.judge p{margin:0;font-size:12px;line-height:14px;font-weight:700;white-space:nowrap;overflow:hidden}
.judge b{color:#8f1d1a;letter-spacing:.04em}
`;

const world = mapSvg(stories);

const html = `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Wednesday 18 November 2026</title><style>${css}</style></head><body><div class="page">
<header class="mast"><div class="kicker"><b>THE DAY IN WORLD NEWS</b><span>${stories.length} STORIES · 6 CONTINENTS</span></div><h1 class="date">Wednesday 18 November 2026</h1><div class="key">${keyHtml}</div><div class="rules"></div></header>
<section class="leads">${leads.map((s) => card(s, 'lead')).join('')}</section>
<section class="mains">${mains.map((s) => card(s, 'main')).join('')}</section>
<section class="band"><aside class="map"><p class="sec">WHERE IT HAPPENED</p><div class="map-frame">${world}<p class="map-cap">${MAP_LEGEND}</p></div></aside>
<section class="also"><p class="sec">ALSO ON WEDNESDAY 18 NOVEMBER</p><div class="also-cols"><div class="also-col">${alsoCol(also.slice(0, mid))}</div><div class="also-col">${alsoCol(also.slice(mid))}</div></div></section></section>
<footer class="foot"><p class="src">${esc(srcLine)}</p><div class="judge"><p><b>JUDGE NOTE</b> Every story happened or was first reported on Wednesday 18 November 2026.</p><p>Disputed claims are attributed.</p></div></footer>
</div></body></html>`;

mkdirSync(join(root, 'build'), { recursive: true });
writeFileSync(join(root, 'build/page.html'), html);
console.log('wrote build/page.html', stories.length, 'stories');
