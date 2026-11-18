#!/bin/bash
# preview: 1 fps frames + contact sheets
cd /home/dell/aimy-promo/biz-promos/v18 && rm -rf prev && node ../render-any.mjs index.html prev 1 1080 1080 >/dev/null && python3 - <<'PY'
from PIL import Image,ImageDraw;import glob
fs=sorted(glob.glob('prev/*.png'))
for k in range(0,len(fs),20):
  S=Image.new('RGB',(5*360,4*360),'black');d=ImageDraw.Draw(S)
  for i,f in enumerate(fs[k:k+20]):
    im=Image.open(f).convert('RGB').resize((356,356));S.paste(im,((i%5)*360,(i//5)*360));d.text(((i%5)*360+4,(i//5)*360+340),str(k+i),fill='red')
  S.save(f'prev/sheet{k//20}.jpg',quality=85)
PY
