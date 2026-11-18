#!/bin/bash
# preview: frames at 1 fps (or $FPS) + contact sheets
cd /home/dell/aimy-promo/biz-promos/v25 && rm -rf prev && node ../render-any.mjs index.html prev ${FPS:-1} 1080 1920 ${FROM:-} ${TO:-} >/dev/null && python3 - <<'PY'
from PIL import Image,ImageDraw;import glob
fs=sorted(glob.glob('prev/*.png'))
for k in range(0,len(fs),20):
  S=Image.new('RGB',(10*216,2*384),'black');d=ImageDraw.Draw(S)
  for i,f in enumerate(fs[k:k+20]):
    im=Image.open(f).convert('RGB').resize((214,382));S.paste(im,((i%10)*216,(i//10)*384));d.text(((i%10)*216+4,(i//10)*384+366),f[-9:-4],fill='red')
  S.save(f'prev/sheet{k//20}.jpg',quality=85)
PY
