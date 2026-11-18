# synthesized quiet UI SFX timed to the structure events in index.html
import numpy as np, wave
SR=48000; DUR=54.44; out=np.zeros((int(DUR*SR),2))
rng=np.random.default_rng(18)
def place(sig,t,g=1.0,pan=0.0):
    i=int(t*SR); n=min(len(sig),len(out)-i)
    if n<=0: return
    out[i:i+n,0]+=sig[:n]*g*(1-max(0,pan)); out[i:i+n,1]+=sig[:n]*g*(1+min(0,pan))
def env(n,a,d): t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/d)
def thock(f=110,d=0.09,noise=0.25,L=0.35):
    n=int(L*SR); t=np.arange(n)/SR; fr=f*(1+1.2*np.exp(-t/0.012))
    s=np.sin(2*np.pi*np.cumsum(fr)/SR)*env(n,0.002,d)
    nz=rng.standard_normal(n)*env(n,0.001,0.015)*noise
    return s+nz
def click(f=2400,L=0.06): n=int(L*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*f*t)*env(n,0.0005,0.008)
def whoosh(L=0.6,up=True):
    n=int(L*SR); x=rng.standard_normal(n); x=np.convolve(x,np.ones(30)/30,'same'); e=np.sin(np.pi*np.arange(n)/n)**2; return x*e*0.6
def chime(f=660,L=2.5):
    n=int(L*SR); t=np.arange(n)/SR; s=sum(np.sin(2*np.pi*f*k*t)/k**1.5 for k in (1,2,3)); return s*env(n,0.004,0.7)
beams=[12.04,13.22,14.34,15.74,16.76,17.94,20.86,22.02,25.08,26.84,27.72,28.8,30.2,31.36,32.54,33.66,34.7,35.54,36.76,38.12]
imgs=[18.82,21.36,22.94,23.64,25.62,29.36,36.08,37.3,38.66]
for i,t in enumerate(beams): place(thock(95+8*(i%3)),t+0.1,0.5,0.35*(-1 if i%2==0 else 1)); place(click(1800),t+0.14,0.12)
for t in imgs: place(thock(180,0.05,0.4,0.2),t+0.08,0.3); place(click(3200),t+0.1,0.1)
place(whoosh(0.7),3.25,0.35)              # TEAM lifts out
place(thock(70,0.2,0.3,0.6),4.95,0.7)     # ONE CHAT foundation
place(thock(60,0.25,0.2,0.7),8.95,0.5)    # 52
place(click(2600),19.8,0.25)              # pick one
place(whoosh(1.0),39.0,0.25)              # crane
place(whoosh(0.35),44.5,0.3)              # approve falls
place(thock(48,0.35,0.6,1.0),44.84,1.0)   # approve lands
place(chime(523.25),47.14,0.22); place(chime(783.99),47.2,0.12)
out/=np.max(np.abs(out))*1.25
w=wave.open('sfx.wav','w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
