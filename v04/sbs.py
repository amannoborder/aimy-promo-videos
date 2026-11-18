import sys,subprocess,os
from PIL import Image,ImageDraw
old,newdir,out=sys.argv[1],sys.argv[2],sys.argv[3]; ts=sys.argv[4:]
W,H=640,360
S=Image.new('RGB',(W*2,H*len(ts)),(40,40,40));d=ImageDraw.Draw(S)
for i,t in enumerate(ts):
  o=f'/tmp/claude-1000/-home-dell-aimy-chat/4de436d9-e14d-4a36-9f11-a7f9c9fc6d81/scratchpad/o{t}.jpg'
  subprocess.run(['ffmpeg','-v','error','-y','-ss',t,'-i',old,'-frames:v','1','-vf','scale=640:360',o])
  S.paste(Image.open(o),(0,i*H)); S.paste(Image.open(f'{newdir}/p{float(t):.2f}.jpg').resize((W,H)),(W,i*H)); d.text((5,i*H+5),t,fill='yellow')
S.save(out,quality=80)
