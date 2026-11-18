import numpy as np, subprocess, wave
SR=48000; DUR=59.0; N=int(SR*DUR)
rng=np.random.default_rng(3)
def load(path):
    raw=subprocess.run(['ffmpeg','-v','error','-i',path,'-f','f32le','-ac','2','-ar',str(SR),'-'],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
def add(buf,sig,t,g=1.0):
    i=int(t*SR); sig=sig if sig.ndim==2 else np.stack([sig,sig],1)
    j=min(N,i+len(sig)); buf[i:j]+=sig[:j-i]*g
def env(n,a,d): t=np.arange(n)/SR; return np.minimum(1,t/max(a,1e-4))*np.exp(-t/d)
def lp(x,k):  # one-pole lowpass
    y=np.empty_like(x); acc=0.0
    for i,v in enumerate(x): acc+=k*(v-acc); y[i]=acc
    return y
def noise(sec): return rng.standard_normal(int(sec*SR)).astype(np.float32)
def swoosh(sec):
    n=noise(sec); t=np.arange(len(n))/SR; e=np.sin(np.pi*t/sec)**2
    from numpy.fft import rfft,irfft
    F=rfft(n); f=np.fft.rfftfreq(len(n),1/SR); F*=np.exp(-((f-900)/700)**2); return irfft(F,len(n))*e*6
def bell(f,sec=1.6): t=np.arange(int(sec*SR))/SR; return (np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*f*2.01*t)+.2*np.sin(2*np.pi*f*3.02*t))*env(len(t),.004,sec/4)
def flap(): n=noise(.12); return lp(n,.25)*env(len(n),.002,.03)*2
def click(): n=noise(.03); return n*env(len(n),.0005,.006)
def thump():
    t=np.arange(int(.5*SR))/SR; return np.sin(2*np.pi*(55+40*np.exp(-t*20))*t)*env(len(t),.002,.12)*1.4+lp(noise(.5),.3)*env(len(t),.001,.04)
sfx=np.zeros((N,2),np.float32)
add(sfx,swoosh(2.3),0.3,.5); add(sfx,swoosh(2.0),50.2,.5)
ents=[14.4,17.4,19.1,20.9,22.1,23.3,27.4,29.6,33.3,35.4,36.4,37.3,38.6,40.6]
penta=[523.25,587.33,659.25,783.99,880.0]
for i,t in enumerate(ents):
    add(sfx,flap(),t+.1,.35); add(sfx,flap(),t+.45,.25)
    add(sfx,bell(penta[i%5]*(1 if i<5 else 2**(i//5*0.5) if False else 1)),t+.6,.06)
t=9.8
while t<11.3: add(sfx,click(),t,.25); t+=0.07+rng.random()*0.06
add(sfx,bell(1046.5,.4),11.6,.08)
add(sfx,bell(1318.5,1.2),24.8,.07); add(sfx,swoosh(.7),25.6,.2); add(sfx,swoosh(.7),31.6,.2)
add(sfx,thump(),44.5,.6)
for k in range(260):
    tt=48.0+rng.random()*3.0; add(sfx,click(),tt,.12*np.sin(np.pi*(tt-48)/3))
for f in (523.25,659.25,783.99): add(sfx,bell(f,3.0),52.6,.05)
# VO placement
vo=load('audio/vo.wav'); voT=np.zeros((N,2),np.float32)
P=[(0.00,5.45,2.2),(5.70,8.70,8.6),(9.15,12.65,12.2),(13.20,15.15,16.0),(15.65,17.65,19.4),(17.95,21.2,23.6),(21.3,22.35,27.8),(22.55,25.3,30.0),(25.6,31.75,33.6),(32.2,35.75,41.6),(35.9,40.04,52.2)]
mask=np.zeros(N,np.float32)
for a,b,f in P:
    s=vo[int(a*SR):int(b*SR)].copy(); fl=int(.02*SR); s[:fl]*=np.linspace(0,1,fl)[:,None]; s[-fl:]*=np.linspace(1,0,fl)[:,None]
    add(voT,s,f); mask[int(f*SR):int((f+b-a)*SR)]=1
# duck envelope (~11 dB) smoothed
k=int(.25*SR); m=np.convolve(mask,np.ones(k)/k,'same'); duck=10**(-11*np.clip(m*1.5,0,1)/20)
mus=load('audio/music.mp3')[:N]
if len(mus)<N: mus=np.vstack([mus,np.zeros((N-len(mus),2),np.float32)])
t=np.arange(N)/SR; mus*=np.clip((DUR-t)/3.5,0,1)[:,None]*np.clip(t/1.0,0,1)[:,None]
full=voT*1.0+mus*duck[:,None]*0.55+sfx*0.6
def w(path,x):
    x=np.clip(x,-1,1); d=(x*32767).astype(np.int16)
    with wave.open(path,'wb') as f: f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes(d.tobytes())
w('audio/mix-full.wav',full*0.5); w('audio/mix-sfx.wav',sfx*0.5)
print('ok')
