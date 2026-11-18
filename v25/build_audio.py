import numpy as np, wave, json, subprocess
SR=48000; DUR=57.0; N=int(DUR*SR)
def rd(p):
    w=wave.open(p); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float).reshape(-1,w.getnchannels())/32768; w.close(); return a
def wr(p,a):
    w=wave.open(p,'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(a,-1,1)*32767).astype(np.int16).tobytes()); w.close()
# ---- VO placed line by line
vo_src=rd('vo.wav'); vo=np.zeros((N,2))
CUES=[(0.0,1.95,0.7),(2.40,8.25,3.5),(8.95,12.1,9.85),(12.4,15.0,15.0),(15.55,17.4,19.9),(17.9,18.8,23.75),(19.05,19.9,27.75),
      (20.05,21.8,31.55),(22.15,24.0,36.6),(24.5,28.25,40.3),(29.1,31.0,47.4),(31.45,35.12,52.2)]
spans=[]
for s,e,d in CUES:
    seg=vo_src[int(s*SR):int(e*SR)].copy(); n=len(seg); f=int(.03*SR)
    seg[:f]*=np.linspace(0,1,f)[:,None]; seg[-f:]*=np.linspace(1,0,f)[:,None]
    i=int(d*SR); vo[i:i+n]+=seg; spans.append((d,d+(e-s)))
json.dump(spans,open('vo-spans.json','w'))
# ---- music: 0-46 then 2 s crossfade into the ending (src 111+)
mu_src=rd('music.wav'); mu=np.zeros((N,2)); X=46.0; S2=111.0; CF=2.0
a=mu_src[:int((X+CF/2)*SR)]; mu[:len(a)]=a
b=mu_src[int((S2-CF/2)*SR):int((S2-CF/2)*SR)+N-int((X-CF/2)*SR)]
t=np.arange(N)/SR
ga=np.clip(((X+CF/2)-t)/CF,0,1); gb=1-ga
mix_b=np.zeros((N,2)); i0=int((X-CF/2)*SR); mix_b[i0:i0+len(b)]=b
mu=mu*np.sqrt(ga)[:,None]+mix_b*np.sqrt(gb)[:,None]
# ---- SFX
rng=np.random.default_rng(25); sf=np.zeros((N,2))
def place(sig,tt,g=1.0,pan=0.0):
    i=int(tt*SR); n=min(len(sig),N-i)
    if n<=0: return
    sf[i:i+n,0]+=sig[:n]*g*(1-max(0,pan)); sf[i:i+n,1]+=sig[:n]*g*(1+min(0,pan))
def env(n,a,d): tt=np.arange(n)/SR; return np.minimum(1,tt/a)*np.exp(-tt/d)
def thock(f=110,d=0.09,noise=0.25,L=0.35):
    n=int(L*SR); tt=np.arange(n)/SR; fr=f*(1+1.2*np.exp(-tt/0.012))
    return np.sin(2*np.pi*np.cumsum(fr)/SR)*env(n,0.002,d)+rng.standard_normal(n)*env(n,0.001,0.015)*noise
def click(f=2400,L=0.06): n=int(L*SR); tt=np.arange(n)/SR; return np.sin(2*np.pi*f*tt)*env(n,0.0005,0.008)
def whoosh(L=0.6):
    n=int(L*SR); x=rng.standard_normal(n); x=np.convolve(x,np.ones(40)/40,'same'); return x*np.sin(np.pi*np.arange(n)/n)**2*0.6
def swell(L=1.4,f=55):
    n=int(L*SR); tt=np.arange(n)/SR; e=(tt/L)**2*np.exp(-(tt/L)**8*3); x=np.convolve(rng.standard_normal(n),np.ones(80)/80,'same')
    return (np.sin(2*np.pi*f*tt)*0.6+x*0.5)*e
def chime(f=660,L=2.5):
    n=int(L*SR); tt=np.arange(n)/SR; return sum(np.sin(2*np.pi*f*k*tt)/k**1.5 for k in (1,2,3))*env(n,0.004,0.7)
for k in range(35): place(click(3000+200*(k%3),.04),0.5+k*2.2/35,0.08,0.2*np.sin(k))
place(click(1800),2.9,0.3); place(thock(140,.06,.3,.25),2.95,0.35)
place(whoosh(1.1),3.15,0.25)
for m in [3.15,4.7,9.8,12.2,15.4,20.0,23.9,27.9,31.7,36.7,40.6,43.95]: place(click(2600),m,0.12); place(thock(220,.04,.2,.2),m,0.12)
for i in range(5): place(click(3400),7.0+i*.32,0.14,0.4*(-1)**i)
for i in range(9): place(thock(120+6*(i%3),.06,.3,.3),9.75+i*.08+.4,0.22,0.3*((i%3)-1))
place(click(2900),12.15,0.3); place(chime(783.99,2.0),12.85,0.10)
place(swell(1.3),13.0,0.55); place(thock(52,.3,.4,.9),14.25,0.6)
ARR=[15.0,15.14,15.28,15.42,15.9,19.9,20.6,21.0,23.8,24.3,24.6,27.7,28.3,28.5,31.6,31.9,32.1,32.3,32.5,36.6,36.78,36.96,40.6,40.85,41.1,41.9]
for i,a in enumerate(ARR): place(thock(95+8*(i%3),.08,.25,.35),a+.35,0.32,0.3*(-1)**i)
for tt in [19.25,23.25,27.25,31.0,35.9,39.6]: place(whoosh(0.9),tt,0.22)
place(click(2200),43.85,0.35); place(thock(60,.25,.4,.8),43.88,0.55); place(chime(659.25,1.6),44.0,0.08)
for i in range(8): place(thock(80+10*i,.07,.2,.3),46.4+i*.13+.3,0.22,0.25*(-1)**i)
place(whoosh(1.2),51.0,0.2)
place(chime(523.25,3.5),52.1,0.16); place(chime(783.99,3.5),52.16,0.09); place(thock(48,.4,.2,1.2),52.1,0.4)
sf/=np.max(np.abs(sf))*1.25
# ---- mix
rms=lambda x: np.sqrt(np.mean(x[np.abs(x).max(1)>1e-4]**2))
vo*=0.1/rms(vo); mu*=0.1/rms(mu)
duck=np.zeros(N)
for s,e in spans: duck=np.maximum(duck,np.clip(np.minimum((t-(s-0.3))/0.3,((e+0.4)-t)/0.4),0,1))
g=10**((-5-11*duck)/20)
fi=np.clip(t/0.3,0,1); fo=np.clip((DUR-0.2-t)/1.6,0,1)
mu=mu*(g*fi*fo)[:,None]
wr('mix-vo-music.wav',vo+mu+sf*0.35); wr('mix-sfx.wav',sf)
print('ok',spans[-1])
