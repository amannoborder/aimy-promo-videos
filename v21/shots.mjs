import { chromium } from "/home/dell/aimy-chat/node_modules/playwright/index.mjs";
import path from "node:path"; import fs from "node:fs";
const ts=process.argv.slice(3).map(Number), out=process.argv[2]; fs.mkdirSync(out,{recursive:true});
const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto("file://"+path.resolve("index.html")); await p.waitForTimeout(2000);
for(const t of ts){await p.evaluate(t=>window.seek(t),t); await p.screenshot({path:`${out}/t${t.toFixed(2)}.png`})}
await b.close();
