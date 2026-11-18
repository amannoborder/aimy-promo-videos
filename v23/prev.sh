#!/bin/bash
# preview: frames at given fps + contact sheets   usage: prev.sh <fps> <dir>
cd /home/dell/aimy-promo/biz-promos/v23 && rm -rf $2 && node ../render-any.mjs index.html $2 $1 1080 1920 >/dev/null && python3 - $2 <<'PY'
from PIL import Image,ImageDraw;import glob,sys
d=sys.argv[1];fs=sorted(glob.glob(d+'/0*.png'))
for k in range(0,len(fs),12):
  S=Image.new('RGB',(6*300,2*534),'black');D=ImageDraw.Draw(S)
  for i,f in enumerate(fs[k:k+12]):
    im=Image.open(f).convert('RGB').resize((296,526));S.paste(im,((i%6)*300,(i//6)*534));D.text(((i%6)*300+4,(i//6)*534+4),str(k+i),fill='red')
  S.save(f'{d}/sheet{k//12}.jpg',quality=85)
PY
