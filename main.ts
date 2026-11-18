// news-image-20261118 — Node 22, standard library only, no network.
// The finished picture sits beside this file as entry.png. Copy those
// bytes to $MAKEFUN_OUTPUT_DIR/entry.png, or to /output/entry.png when
// the variable is unset. The grader reads only the file that lands there.

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
const destDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(source, join(destDir, 'entry.png'));
