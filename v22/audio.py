# VO placement + synthesized SFX + music mix for v22
import numpy as np, subprocess, json, wave
SR=48000; DUR=59.5; N=int(DUR*SR)
rng=np.random.default_rng(22)
def load(p,ss=0):
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(ss),'-i',p,'-f','f32le','-ac','2','-ar',str(SR),'-'],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).astype(np.float64)
def wr(p,a):
    w=wave.open(p,'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(a,-1,1)*32767).astype(np.int16).tobytes()); w.close()
def add(buf,sig,t,g=1.0,pan=0.0):
    if sig.ndim==1: sig=np.stack([sig*(1-max(0,pan)),sig*(1+min(0,pan))],1)
    i=int(t*SR); j=min(len(buf),i+len(sig))
    if j>i: buf[i:j]+=sig[:j-i]*g
def env(n,a,d): t=np.arange(n)/SR; return np.minimum(1,t/max(a,1e-4))*np.exp(-t/d)
def thock(f=110,d=0.09,noise=0.25,L=0.35):
    n=int(L*SR); t=np.arange(n)/SR; fr=f*(1+1.2*np.exp(-t/0.012))
    return np.sin(2*np.pi*np.cumsum(fr)/SR)*env(n,0.002,d)+rng.standard_normal(n)*env(n,0.001,0.015)*noise
def click(f=2400,L=0.06): n=int(L*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*f*t)*env(n,0.0005,0.008)
def key(): n=int(.04*SR); x=rng.standard_normal(n)*env(n,.0003,.004); return np.convolve(x,np.ones(6)/6,'same')
def whoosh(L=0.6,c=900,w=700):
    n=int(L*SR); x=rng.standard_normal(n); F=np.fft.rfft(x); f=np.fft.rfftfreq(n,1/SR); F*=np.exp(-((f-c)/w)**2)
    return np.fft.irfft(F,n)*np.sin(np.pi*np.arange(n)/n)**2*8
def sweep(L,f0,f1):
    n=int(L*SR); x=rng.standard_normal(n); out=np.zeros(n); seg=2048
    for k in range(0,n,seg):
        c=f0+(f1-f0)*k/n; X=np.fft.rfft(x[k:k+seg]); f=np.fft.rfftfreq(len(x[k:k+seg]),1/SR); X*=np.exp(-((f-c)/(c*.35))**2); out[k:k+seg]=np.fft.irfft(X,len(x[k:k+seg]))
    return out*np.sin(np.pi*np.arange(n)/n)*6
def chime(f=660,L=2.0):
    n=int(L*SR); t=np.arange(n)/SR; return sum(np.sin(2*np.pi*f*k*t)/k**1.5 for k in (1,2,3))*env(n,0.004,L/4)
def thump():
    t=np.arange(int(.6*SR))/SR; return np.sin(2*np.pi*(52+45*np.exp(-t*22))*t)*env(len(t),.002,.14)*1.3+rng.standard_normal(len(t))*env(len(t),.001,.03)*.3
# ---------------- SFX ----------------
sfx=np.zeros((N,2))
HW=[1.0,1.12,1.38,2.04,2.3,2.62]
for t in HW: add(sfx,click(1800,.05),t,.12)
add(sfx,whoosh(.9,700,500),3.4,.35)
for i in range(34): add(sfx,key(),4.3+1.25*i/34+rng.random()*.015,.35,rng.uniform(-.2,.2))
add(sfx,click(2600),5.75,.35); add(sfx,thock(240,.04,.3,.2),5.85,.25); add(sfx,thock(200,.04,.3,.2),6.25,.25)
for i in range(10): add(sfx,click(3000+120*i,.05),6.7+i*.27+.32,.08)
add(sfx,click(2600),10.6,.35)
add(sfx,whoosh(1.0,500,450),10.7,.5); add(sfx,thock(70,.2,.3,.6),11.15,.55)
KEYS=[11.84,13.10,14.74,15.86,17.2,20.62,22.6,25.36,27.25,27.95,28.6,29.42,30.2,31.56,32.64,33.66,34.5]
for i,t in enumerate(KEYS): add(sfx,whoosh(.5,1200,800),t-.5,.12,.3*(-1)**i); add(sfx,thock(100+8*(i%3),.08,.25,.3),t,.32,.25*(-1)**i)
add(sfx,click(3200),19.05,.25); add(sfx,chime(880,1.2),19.35,.05)
add(sfx,whoosh(.7,1500,900),23.7,.18)
add(sfx,whoosh(1.2,500,400),35.2,.35)
add(sfx,sweep(1.9,400,4000),36.65,.16)
for t in (36.925,37.94,38.29): add(sfx,click(3400),t,.2); add(sfx,chime(1046.5,1.0),t,.05)
add(sfx,whoosh(.8,700,600),39.85,.3)
add(sfx,whoosh(1.0,1800,1200),43.5,.55); add(sfx,thock(80,.15,.3,.5),44.45,.5)
add(sfx,whoosh(.8,900,700),44.6,.25); add(sfx,whoosh(.5,1400,900),45.7,.15)
add(sfx,click(2600),48.75,.4); add(sfx,chime(783.99,1.6),48.85,.07); add(sfx,chime(1046.5,1.6),48.95,.05)
add(sfx,whoosh(.7,1100,800),49.05,.25)
add(sfx,thump(),51.0,.6); add(sfx,thump(),53.1,.55)
for f in (523.25,659.25,783.99): add(sfx,chime(f,3.0),54.4,.05)
sfx/=np.max(np.abs(sfx))*1.25
# ---------------- VO ----------------
vo=load('vo-raw.wav'); W=json.load(open('words.json'))
starts=[0,9,28,33,57,70,81,86,96,101]   # first word index of each line
offs=[0.6,0.7,1.2,1.2,1.2,1.6,2.4,4.2,5.0,5.0]
voT=np.zeros((N,2)); mask=np.zeros(N)
for k,(si,of) in enumerate(zip(starts,offs)):
    a=0 if k==0 else (W[si-1]['e']+W[si]['s'])/2
    b=len(vo)/SR if k==len(starts)-1 else (W[starts[k+1]-1]['e']+W[starts[k+1]]['s'])/2
    seg=vo[int(a*SR):int(b*SR)].copy(); fl=int(.03*SR); seg[:fl]*=np.linspace(0,1,fl)[:,None]; seg[-fl:]*=np.linspace(1,0,fl)[:,None]
    add(voT,seg,a+of); mask[int((W[si]['s']+of-.1)*SR):int((a+of+len(seg)/SR)*SR)]=1
    print(k,W[si]['w'],round(a,2),round(b,2),'->',round(a+of,2),round(b+of,2))
k=int(.3*SR); c=np.cumsum(np.concatenate([np.zeros(k//2),mask,np.zeros(k-k//2)])); m=np.clip((c[k:]-c[:-k])[:N]/k*1.4,0,1)
# ---------------- music ----------------
mu=load('music.mp3',3.9)[:N]
if len(mu)<N: mu=np.vstack([mu,np.zeros((N-len(mu),2))])
rms=lambda a: np.sqrt(np.mean(a[np.abs(a).max(1)>1e-4]**2))
voT*=0.1/rms(voT); mu*=0.1/rms(mu)
t=np.arange(N)/SR
g=10**((-5-11*m)/20)*np.clip(t/.5,0,1)*np.clip((59.3-t)/2.0,0,1)
mix=voT+mu*g[:,None]+sfx*0.22
wr('mix-pre.wav',mix*.5); wr('sfx-pre.wav',sfx*.5)
print('ok')
