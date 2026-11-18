import { chromium } from "/home/dell/aimy-chat/node_modules/playwright/index.mjs";
import path from "node:path";
const [html,out,...ts]=process.argv.slice(2);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
p.on('pageerror',e=>console.log('ERR',e.message));p.on('console',m=>{if(m.type()=='error')console.log('CERR',m.text())});
await p.goto("file://"+path.resolve(html));await p.waitForTimeout(2500);
for(const t of ts){await p.evaluate(t=>window.seek(t),+t);await p.screenshot({path:`${out}/p${(+t).toFixed(2)}.jpg`,type:'jpeg',quality:80});}
await b.close();
