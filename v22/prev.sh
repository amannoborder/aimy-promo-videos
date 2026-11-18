#!/bin/bash
# prev.sh <fps-ish step> : render preview frames at given fps and make sheets
cd /home/dell/aimy-promo/biz-promos/v22 && rm -rf prev && node ../render-any.mjs index.html prev ${1:-1} 1920 1080 >/dev/null && python3 - <<'PY'
from PIL import Image,ImageDraw;import glob
fs=sorted(glob.glob('prev/*.png'))
for k in range(0,len(fs),20):
  S=Image.new('RGB',(4*480,5*270),'black');d=ImageDraw.Draw(S)
  for i,f in enumerate(fs[k:k+20]):
    im=Image.open(f).convert('RGB').resize((476,268));S.paste(im,((i%4)*480,(i//4)*270));d.text(((i%4)*480+4,(i//4)*270+254),str(k+i),fill='red')
  S.save(f'prev/sheet{k//20}.jpg',quality=85)
PY
