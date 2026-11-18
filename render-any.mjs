// node render-any.mjs <index.html> <framesdir> <fps> <W> <H> [from=0] [to=all]   (window.seek(t) + window.DUR; frames %05d.png)
import fs from "node:fs"; import path from "node:path";
import { chromium } from "/home/dell/aimy-chat/node_modules/playwright/index.mjs";
const [html, out, fpsA, wA, hA, fA, tA] = process.argv.slice(2);
const fps = +fpsA; fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +wA, height: +hA } }); p.setDefaultTimeout(30000);
await p.goto("file://" + path.resolve(html)); await p.waitForTimeout(2000);   // never await document.fonts.ready (it hung before)
const n = Math.round((await p.evaluate(() => window.DUR)) * fps);
const from = +(fA || 0), to = Math.min(n, +(tA || n));
for (let i = from; i < to; i++) {
  if (fs.existsSync(`${out}/${String(i).padStart(5, "0")}.png`) && process.env.RESUME) continue;
  await p.evaluate((t) => window.seek(t), i / fps);
  await p.screenshot({ path: `${out}/${String(i).padStart(5, "0")}.png`, timeout: 30000 });
}
await b.close(); console.log("frames", from, to);
