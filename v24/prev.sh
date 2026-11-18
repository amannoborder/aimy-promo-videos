#!/bin/bash
# preview frames at given fps + contact sheets
cd /home/dell/aimy-promo/biz-promos/v24 && rm -rf prev && node ../render-any.mjs index.html prev ${1:-1} 1920 1080 >/dev/null && python3 - <<'PY'
from PIL import Image,ImageDraw;import glob
fs=sorted(glob.glob('prev/*.png'))
for k in range(0,len(fs),16):
  S=Image.new('RGB',(4*480,4*270),'black');d=ImageDraw.Draw(S)
  for i,f in enumerate(fs[k:k+16]):
    im=Image.open(f).convert('RGB').resize((476,268));S.paste(im,((i%4)*480,(i//4)*270));d.text(((i%4)*480+4,(i//4)*270+250),str(k+i),fill='red')
  S.save(f'prev/sheet{k//16}.jpg',quality=85)
PY
