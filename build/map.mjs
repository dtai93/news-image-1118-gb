// Dotted equirectangular world, plus numbered pins for stories 1-12.
import { COLS, ROWS, LAT_NORTH, LAT_SOUTH, LAND_ROWS } from './landmask.mjs';

// Badge-centre offsets in cell units. Clusters (Shenzhen, Washington) get leaders.
const SHIFT = {
  1: [-2.8, -2.4],
  2: [3.2, 2.6],
  3: [-3.6, 0.2],
  4: [4.8, 3.0],
  5: [5.8, 0.8],
  6: [1.6, 2.4],
  7: [8.6, 4.4],
  8: [4.8, -1.8],
  9: [8.2, -2.6],
  10: [-5.0, 0.1],
  11: [5.2, -5.0],
  12: [-1.2, -2.4],
};

export const MAP_LEGEND = 'Asia 1·4·12 · Gulf 2 · Americas 3·5-7·9·11 · Europe 8·10';

export function project(lat, lon) {
  const x = ((Number(lon) + 180) / 360) * COLS;
  const y = ((LAT_NORTH - Number(lat)) / (LAT_NORTH - LAT_SOUTH)) * ROWS;
  return [x, y];
}

function dots() {
  const parts = [];
  for (let r = 0; r < ROWS; r++) {
    const line = LAND_ROWS[r];
    for (let c = 0; c < COLS; c++) {
      if (line[c] === '#') parts.push(`<circle cx="${c + 0.5}" cy="${r + 0.5}" r="0.4"/>`);
    }
  }
  return parts.join('');
}

function badge(n, x, y) {
  const [dx, dy] = SHIFT[n];
  const label = String(n);
  const w = label.length > 1 ? 3.5 : 2.4;
  const h = 2.25;
  const left = Math.max(0.25, Math.min(COLS - w - 0.25, x + dx - w / 2));
  const top = Math.max(0.2, Math.min(ROWS - h - 0.2, y + dy - h / 2));
  const cx = (left + w / 2).toFixed(2);
  const cy = (top + h / 2).toFixed(2);
  return `<line x1="${x.toFixed(2)}" y1="${y.toFixed(2)}" x2="${cx}" y2="${cy}" stroke="#8f1d1a" stroke-width="0.22"/><circle cx="${x.toFixed(2)}" cy="${y.toFixed(2)}" r="0.46" fill="#8f1d1a"/><rect x="${left.toFixed(2)}" y="${top.toFixed(2)}" width="${w}" height="${h}" rx="0.3" fill="#8f1d1a"/><text x="${cx}" y="${cy}" text-anchor="middle" dominant-baseline="central" font-family="Source Sans Pro,Inter,sans-serif" font-size="1.55" font-weight="700" fill="#fbf7f0">${label}</text>`;
}

export function mapSvg(stories) {
  const pins = stories
    .filter((s) => s.n >= 1 && s.n <= 12)
    .sort((a, b) => a.n - b.n)
    .map((s) => {
      const [x, y] = project(s.lat, s.lon);
      return badge(s.n, x, y);
    })
    .join('');
  return `<svg viewBox="0 0 ${COLS} ${ROWS}" preserveAspectRatio="xMidYMid meet" aria-hidden="true"><rect width="${COLS}" height="${ROWS}" fill="#d7e3ea"/><g fill="#1c140e">${dots()}</g>${pins}</svg>`;
}
