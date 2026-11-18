import { chromium } from "/home/dell/aimy-chat/node_modules/playwright/index.mjs";
import path from "node:path"; import fs from "node:fs";
const ts=process.argv.slice(2).map(Number);fs.mkdirSync("chk",{recursive:true});
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto("file://"+path.resolve("index.html"));await p.waitForTimeout(2000);
const out=[];
for(const t of ts){await p.evaluate(t=>window.seek(t),t);const f=`chk/t${t}.png`;await p.screenshot({path:f});out.push(f);}
fs.writeFileSync("chk/list.txt",out.join("\n"));await b.close();
