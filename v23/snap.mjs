// node snap.mjs out.jpg t1 t2 ...  -> horizontal strip of frames at given times
import path from "node:path";
import { chromium } from "/home/dell/aimy-chat/node_modules/playwright/index.mjs";
const [out,...ts]=process.argv.slice(2);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto("file://"+path.resolve("index.html"));await p.waitForTimeout(2000);
for(const t of ts){await p.evaluate(t=>window.seek(t),+t);await p.screenshot({path:`snap-${t}.png`})}
await b.close();
