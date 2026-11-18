import numpy as np, soundfile as sf, subprocess, io
SR=48000; DUR=54.5; N=int(SR*DUR)
rng=np.random.default_rng(7)
def load(path):
    out=subprocess.run(['ffmpeg','-v','error','-i',path,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(out,dtype=np.float32).copy()
vo=load('audio/vo2.wav'); mus=load('audio/music.mp3')
# ---- VO placement
SEG=[(0.0,4.75,0.6),(5.7,7.1,5.4),(7.95,11.4,6.95),(12.5,17.12,10.42),(18.0,20.5,15.6),(21.3,23.74,18.55),(24.8,27.39,22.1),(28.08,30.75,26.15),(31.86,35.39,31.0),(36.55,39.16,37.5),(40.2,43.68,45.3)]
V=np.zeros(N,np.float32); voiced=np.zeros(N,np.float32)
for a,b,at in SEG:
    s=vo[int(a*SR):int(b*SR)].copy(); f=int(0.02*SR); s[:f]*=np.linspace(0,1,f); s[-f:]*=np.linspace(1,0,f)
    i=int(at*SR); V[i:i+len(s)]+=s[:N-i]; voiced[i:i+len(s)]=1
# ---- SFX
def env(n,a,d): t=np.arange(n)/SR; return np.minimum(1,t/max(a,1e-4))*np.exp(-t/d)
def tone(f,dur,a=0.003,d=0.12,amp=0.3,f2=None):
    n=int(dur*SR); t=np.arange(n)/SR; ff=f if f2 is None else np.linspace(f,f2,n)
    ph=2*np.pi*np.cumsum(ff)/SR; return (np.sin(ph)+0.25*np.sin(2*ph))*env(n,a,d)*amp
def noise_sweep(dur,amp=0.15,lo=300,hi=4000,rise=True):
    from scipy.signal import butter,lfilter
    n=int(dur*SR); x=rng.standard_normal(n); out=np.zeros(n); blk=1024
    for k in range(0,n,blk):
        u=k/n; fc=lo+(hi-lo)*(u if rise else 1-u); b,a=butter(2,[max(50,fc*0.6)/(SR/2),min(0.99,fc*1.4/(SR/2))],'band'); out[k:k+blk]=lfilter(b,a,x[k:k+blk])
    w=np.sin(np.pi*np.arange(n)/n)**1.5; return out*w*amp
S=np.zeros(N,np.float32)
def put(sig,t,g=1.0):
    i=int(t*SR); j=min(N,i+len(sig)); S[i:j]+=(sig[:j-i]*g).astype(np.float32)
click=lambda amp=0.18: tone(2400,0.04,0.0005,0.008,amp)+tone(900,0.04,0.0005,0.012,amp*0.6)
pop=lambda f=880,amp=0.16: tone(f,0.12,0.002,0.04,amp,f*1.6)
# typing 1.3-2.8
for k in range(18): put(click(0.07+0.03*rng.random()),1.3+k*0.083+rng.random()*0.02)
put(noise_sweep(0.35,0.10,800,5000),3.1); put(pop(1200,0.12),3.15)
put(pop(700,0.10),4.0)
# chips appearing
for i in range(20): put(pop(900+i*25,0.045),6.35+i*0.05)
# whooshes on big moves
for t,d in [(7.3,1.2),(15.0,0.9),(21.8,0.9),(25.6,0.9),(30.6,1.3),(35.3,1.3),(43.6,1.4)]: put(noise_sweep(d,0.07,250,2200,True),t)
# desk ticks
CT=[10.6,11.9,12.9,13.9,14.9,16.9,19.0,20.2,21.4,22.6,23.45,24.3,25.3,26.4,26.95,27.45,27.9,28.6,29.4]
for c in CT: put(click(0.05),c-0.45)
# done pings (soft)
for c in CT:
    if c!=16.9: put(tone(1568,0.25,0.003,0.09,0.035),c+0.35)
# needs-you dings
for t in (15.8,34.45): put(tone(988,0.5,0.004,0.18,0.12),t); put(tone(1319,0.4,0.004,0.18,0.10),t+0.09)
put(click(0.12),17.85); put(tone(1760,0.35,0.003,0.12,0.08),18.05)
# legend highlights
for t in (32.6,33.45,34.35): put(pop(1000,0.06),t)
# modal in, approve click, success chime
put(noise_sweep(0.3,0.06,1000,4000),36.95); put(click(0.16),41.0)
for k,f in enumerate((1047,1319,1568)): put(tone(f,0.6,0.004,0.25,0.09),41.1+k*0.08)
# end card chime
for k,f in enumerate((784,1175,1568)): put(tone(f,1.6,0.01,0.6,0.07),47.5+k*0.12)
# ---- music: trim, fades, ducking
M=np.zeros(N,np.float32); m=mus[:N]; M[:len(m)]=m
t=np.arange(N)/SR; M*=np.clip(t/0.6,0,1); M*=np.clip((DUR-t)/3.2,0,1)
from scipy.ndimage import uniform_filter1d
duck=uniform_filter1d(voiced,int(0.35*SR)); g=10**(-11*np.clip(duck*1.3,0,1)/20)
M*=g.astype(np.float32)
def rms_db(x): return 20*np.log10(np.sqrt(np.mean(x[np.abs(x)>1e-5]**2))+1e-9)
print('vo',rms_db(V),'mus',rms_db(M),'sfx',rms_db(S))
# set music bed so unducked music ~ -6 dB under VO speech level
musg=10**((rms_db(V)-6-rms_db(mus[:N]))/20); M*=musg
sfx_only=S.copy()
full=V+M+S*0.8
sf.write('audio/sfx_only_raw.wav',sfx_only,SR,subtype='FLOAT')
sf.write('audio/full_raw.wav',full,SR,subtype='FLOAT')
