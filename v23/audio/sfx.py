# quiet synthesized UI SFX from the composition's own SFX event list (sfx.json)
import numpy as np, wave, json
SR=48000; DUR=58.0; out=np.zeros((int(DUR*SR),2)); rng=np.random.default_rng(23)
def env(n,a,d): t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/d)
def place(sig,t,g,pan=0.0):
    i=int(t*SR); n=min(len(sig),len(out)-i)
    if n<=0 or i<0: return
    out[i:i+n,0]+=sig[:n]*g*(1-max(0,pan)); out[i:i+n,1]+=sig[:n]*g*(1+min(0,pan))
def pop(f=900):
    n=int(.12*SR); t=np.arange(n)/SR; fr=f*(1+.6*np.exp(-t/.01)); return np.sin(2*np.pi*np.cumsum(fr)/SR)*env(n,.001,.03)
def whoosh(L=.6):
    n=int(L*SR); x=rng.standard_normal(n); x=np.convolve(x,np.ones(40)/40,'same'); return x*np.sin(np.pi*np.arange(n)/n)**2*.9
def swell(L=.7):
    n=int(L*SR); t=np.arange(n)/SR; x=np.convolve(rng.standard_normal(n),np.ones(18)/18,'same')
    return (x*.6+.3*np.sin(2*np.pi*(300+500*t/L)*t))*(t/L)**2*np.exp(-np.maximum(0,t-L*.85)/.03)
def thock(f=120,d=.08):
    n=int(.35*SR); t=np.arange(n)/SR; fr=f*(1+1.2*np.exp(-t/.012)); return np.sin(2*np.pi*np.cumsum(fr)/SR)*env(n,.002,d)+rng.standard_normal(n)*env(n,.001,.012)*.2
def tap(): n=int(.06*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*2600*t)*env(n,.0005,.008)+thock(160,.05)[:n]
def chime(f=659.25):
    n=int(2.5*SR); t=np.arange(n)/SR; return sum(np.sin(2*np.pi*f*k*t)/k**1.5 for k in (1,2,3))*env(n,.004,.7)
K={'pop':pop,'whoosh':whoosh,'swell':swell,'thock':thock,'tap':tap,'chime':chime}
for i,e in enumerate(json.load(open('sfx.json'))):
    place(K[e['k']](),e['t'],e.get('g',.5),.25*(-1 if i%2 else 1))
place(chime(523.25),51.75,.35); place(chime(783.99),51.8,.18)
out/=np.max(np.abs(out))*1.2
w=wave.open('sfx.wav','w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
