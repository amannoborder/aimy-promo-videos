import base64, io, json, sys
from PIL import Image
P='/home/dell/aimy-promo/biz-promos/en-pack/'
spec={ # name: (file, maxW, maxH, crop(l,t,r,b) frac or None, fmt)
 'logosheet':('logo-sheet-nine-en.png',1000,1000,None,'JPEG'),
 'vyralogo':('vyra-logo-en.png',600,200,None,'PNG'),
 'brandboard':('brandboard-en.jpg',1280,800,(0,0,1,0.5),'JPEG'),
 'selfie':('01-original-photo.jpg',600,760,None,'JPEG'),
 'portrait':('02-portrait.jpg',600,760,None,'JPEG'),
 'website':('website-hero-en.jpg',1280,800,None,'JPEG'),
 'cover3':('cover-en-fitness-3.jpg',1280,400,None,'JPEG'),
 'cover1':('cover-en-fitness-1.jpg',1280,400,None,'JPEG'),
 'covercity':('cover-en-move-your-city.jpg',1280,400,None,'JPEG'),
 'gcover1':('girl-cover-1.png',1280,400,None,'JPEG'),
 'gcover2':('girl-cover-2.png',1280,400,None,'JPEG'),
 'gcover3':('girl-cover-3.png',1280,400,None,'JPEG'),
 'thumb1':('thumb-en-1.jpg',900,506,None,'JPEG'),
 'thumb2':('thumb-en-2.jpg',640,360,None,'JPEG'),
 'thumb3':('thumb-en-3.jpg',640,360,None,'JPEG'),
 'pose1':('girl-pose-1.jpg',400,700,None,'JPEG'),
 'pose2':('girl-pose-2.jpg',400,700,None,'JPEG'),
 'pose3':('girl-pose-3.jpg',400,700,None,'JPEG'),
 'pose4':('girl-pose-4.jpg',400,700,None,'JPEG'),
 'mp1':('07-model-photo-1.jpg',420,420,None,'JPEG'),
 'mp2':('07-model-photo-2.jpg',420,420,None,'JPEG'),
 'mp3':('07-model-photo-3.jpg',420,420,None,'JPEG'),
 'mp4':('07-model-photo-4.jpg',420,420,None,'JPEG'),
 'adgirl':('ad-en-vyra-girl.jpg',600,600,None,'JPEG'),
 'adbusy':('ad-en-busy-routine.jpg',600,600,None,'JPEG'),
 'banner':('banner-en.jpg',1000,300,None,'JPEG'),
 'tiktok':('tiktok-en-squat.jpg',450,800,None,'JPEG'),
 'brandhero':('brand-hero-en.jpg',900,700,None,'JPEG'),
}
out={}
for k,(f,mw,mh,crop,fmt) in spec.items():
  im=Image.open(P+f)
  if fmt=='JPEG':
    if im.mode in('RGBA','LA','P'):
      im=im.convert('RGBA');bg=Image.new('RGB',im.size,(255,255,255));bg.paste(im,mask=im.split()[3]);im=bg
    else: im=im.convert('RGB')
  if crop:
    w,h=im.size;im=im.crop((int(crop[0]*w),int(crop[1]*h),int(crop[2]*w),int(crop[3]*h)))
  im.thumbnail((mw,mh),Image.LANCZOS)
  b=io.BytesIO();im.save(b,fmt,quality=88) if fmt=='JPEG' else im.save(b,fmt)
  out[k]='data:image/%s;base64,'%('jpeg' if fmt=='JPEG' else 'png')+base64.b64encode(b.getvalue()).decode()
open('assets.js','w').write('window.ASSETS='+json.dumps(out)+';')
print(len(out))
