import numpy as np, wave
SR=48000; DUR=53.4; N=int(DUR*SR)
def rd(p):
    w=wave.open(p); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float).reshape(-1,w.getnchannels())/32768; w.close(); return a
def wr(p,a):
    a=np.atleast_2d(a.T).T
    if a.shape[1]==1: a=np.repeat(a,2,1)
    w=wave.open(p,'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(a,-1,1)*32767).astype(np.int16).tobytes()); w.close()
# ---- VO retime ----
vo=rd('audio/vo48.wav')[:,0]
S=[0.8,4.6,10.6,15.1,19.9,23.5,26.4,29.8,32.5,36.0,38.6,43.6,47.2]
O=[0.0,3.74,9.72,14.16,18.88,22.42,25.3,27.58,30.26,33.9,36.46,41.18,43.9]
E=[2.98,9.1,13.64,18.24,21.84,24.68,27.02,29.62,33.06,35.8,40.38,43.12,47.12]
V=np.zeros(N)
for s,o,e in zip(S,O,E):
    a,b=int(max(0,o-.12)*SR),int(min(len(vo)/SR,e+.25)*SR); seg=vo[a:b].copy()
    f=int(.02*SR); seg[:f]*=np.linspace(0,1,f); seg[-f:]*=np.linspace(1,0,f)
    i=int((s-(o-a/SR))*SR); V[i:i+len(seg)]+=seg[:N-i]
# ---- music: first 49.4 s + crossfade into the track's own ending ----
mu=rd('audio/music48.wav'); L=len(mu)/SR
tail=mu[int((L-4.0)*SR):]; head=mu[:int(50.4*SR)]
xf=int(1.0*SR); r=np.linspace(0,1,xf)[:,None]
M=np.concatenate([head[:-xf], head[-xf:]*(1-r)+tail[:xf]*r, tail[xf:]])
M=np.pad(M,((0,max(0,N-len(M))),(0,0)))[:N]
# ---- SFX ----
rng=np.random.default_rng(24); SF=np.zeros((N,2))
def place(sig,t,g=1.0,pan=0.0):
    i=int(t*SR); n=min(len(sig),N-i)
    if n<=0: return
    SF[i:i+n,0]+=sig[:n]*g*(1-max(0,pan)); SF[i:i+n,1]+=sig[:n]*g*(1+min(0,pan))
def env(n,a,d): t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/d)
def click(f=2400,L=.06): n=int(L*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*f*t)*env(n,.0005,.008)
def thock(f=110,d=.09,noise=.25,L=.35):
    n=int(L*SR); t=np.arange(n)/SR; fr=f*(1+1.2*np.exp(-t/.012)); s=np.sin(2*np.pi*np.cumsum(fr)/SR)*env(n,.002,d)
    return s+rng.standard_normal(n)*env(n,.001,.015)*noise
def whoosh(L=1.25,peak=.8,bright=1.0):
    n=int(L*SR); x=rng.standard_normal(n); k=max(3,int(40/bright)); x=np.convolve(x,np.ones(k)/k,'same')
    t=np.arange(n)/n; e=np.where(t<peak,(t/peak)**2,((1-t)/(1-peak))**1.5); return x*e*0.9
def chime(f=660,L=2.5): n=int(L*SR); t=np.arange(n)/SR; return sum(np.sin(2*np.pi*f*k*t)/k**1.5 for k in (1,2,3))*env(n,.004,.7)
ARR=[0,4.0,11.6,16.4,21.1,23.45,26.35,29.75,32.45,35.95,38.7]
for i,a in enumerate(ARR[1:]):
    place(whoosh(1.3,.85,1+.15*i),a-1.25,.42,.2*(-1)**i); place(thock(80,.12,.2,.4),a-.02,.35)
for k in range(12): place(click(2000+300*(k%3),.04),2.75+k*.11,.07)       # typing
place(click(2600),4.3,.22); place(thock(160,.06,.3,.2),5.4,.18); place(thock(140,.08,.3,.25),7.2,.25)
for i in range(14): place(click(3000,.05),11.95+i*.09,.06)                # plan checks
for i in range(9): place(thock(220,.04,.3,.15),13.0+i*.24,.12)            # logo ideas pop
place(click(2600),18.75,.25); place(chime(880,1.2),18.78,.08)             # pick
for i in range(5): place(thock(200,.05,.3,.15),21.8+i*.08,.1)
place(click(2600),42.2,.3); place(thock(60,.25,.4,.8),42.22,.6); place(chime(523.25),42.3,.18); place(chime(783.99),42.36,.1)
place(whoosh(3.3,.55,.8)[::-1],43.35,.55)                                 # pull-out (reverse swell)
place(chime(523.25,3),46.75,.2); place(chime(659.25,3),46.8,.12)
SF/=np.max(np.abs(SF))*1.6
# ---- mix ----
rms=lambda a: np.sqrt(np.mean(a[np.abs(a)>1e-4]**2))
V*=0.1/rms(V); M*=0.1/rms(M)
t=np.arange(N)/SR; act=np.abs(V)>2e-3; duck=np.zeros(N)
# VO activity spans
spans=[[s-.1,s+(e-o)+.15] for s,o,e in zip(S,O,E)]
for s,e in spans: duck=np.maximum(duck,np.clip(np.minimum((t-(s-.25))/.25,((e+.35)-t)/.35),0,1))
g=10**((-6-11*duck)/20); fi=np.clip(t/.4,0,1); fo=np.clip((DUR-.05-t)/1.2,0,1)
M=M*(g*fi*fo)[:,None]
wr('audio/mix-vo-music.wav',V[:,None]+M+SF*.6); wr('audio/mix-sfx.wav',SF); print('ok')
