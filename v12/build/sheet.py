import sys,glob
from PIL import Image,ImageDraw
d=sys.argv[1];fs=sorted(glob.glob(d+'/p-*.png'),key=lambda f:float(f.split('p-')[-1][:-4]))
W,H=640,360;cols=3
for part in range(0,len(fs),6):
  sub=fs[part:part+6];s=Image.new('RGB',(W*cols,H*2))
  for i,f in enumerate(sub):
    im=Image.open(f).convert('RGB').resize((W,H));ImageDraw.Draw(im).text((5,5),f.split('/')[-1],fill=(255,0,0));s.paste(im,((i%cols)*W,(i//cols)*H))
  s.save(f'{d}/sheet{part//6}.jpg',quality=85)
