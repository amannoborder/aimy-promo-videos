import { chromium } from "/home/dell/aimy-chat/node_modules/playwright/index.mjs";
import path from "node:path";
const [html,out,...ts]=process.argv.slice(2);
const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1920,height:1080}});
p.on('console',m=>console.log('console',m.type(),m.text())); p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto("file://"+path.resolve(html)); await p.waitForTimeout(2000);
for(const t of ts){const t0=Date.now(); await p.evaluate(t=>window.seek(t),+t); await p.screenshot({path:`${out}/p-${(+t).toFixed(2)}.png`}); console.log(t, Date.now()-t0,'ms');}
await b.close();
