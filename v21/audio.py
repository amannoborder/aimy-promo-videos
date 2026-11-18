import numpy as np, wave, json
SR=48000; DUR=58.0; N=int(DUR*SR)
def rd(p):
    w=wave.open(p); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float).reshape(-1,w.getnchannels())/32768; sr=w.getframerate(); w.close()
    if a.shape[1]==1: a=np.repeat(a,2,1)
    if sr!=SR:
        x=np.arange(0,len(a),sr/SR); a=np.stack([np.interp(x,np.arange(len(a)),a[:,c]) for c in (0,1)],1)
    return a
def wr(p,a):
    w=wave.open(p,'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(a,-1,1)*32767).astype(np.int16).tobytes()); w.close()
def place(out,sig,t,g=1.0,pan=0.0):
    i=int(t*SR); n=min(len(sig),len(out)-i)
    if n<=0: return
    if sig.ndim==1: sig=np.stack([sig*(1-max(0,pan)),sig*(1+min(0,pan))],1)
    out[i:i+n]+=sig[:n]*g
# ---- VO: cut source lines at silences, place at scene times
vo=rd('vo.wav')
cuts=[0,1.6,5.75,8.65,11.2,13.95,15.97,18.34,21.06,23.53,27.28,30.8]
at=[0.4,6.7,12.3,17.4,21.95,26.8,31.0,35.5,41.0,45.0,53.6]
V=np.zeros((N,2)); spans=[]
for k in range(11):
    s,e=int(cuts[k]*SR),int(cuts[k+1]*SR); seg=vo[s:e].copy(); f=int(.02*SR); seg[:f]*=np.linspace(0,1,f)[:,None]; seg[-f:]*=np.linspace(1,0,f)[:,None]
    place(V,seg,at[k]); spans.append((at[k],at[k]+(e-s)/SR))
wr('vo-timed.wav',V); json.dump(spans,open('vo-spans.json','w'))
# ---- music: film 0-52.75 = music 8.4.. ; crossfade 0.6 into music 122.75 (natural ending)
M=rd('music.wav'); mu=np.zeros((N,2))
a0=int(8.4*SR); L1=int(53.05*SR); mu[:L1]=M[a0:a0+L1]
xf=int(.6*SR); b0=int((122.75-0.3)*SR); tail=M[b0:b0+(N-int(52.45*SR))]
i0=int(52.45*SR); fade=np.linspace(0,1,xf)[:,None]
mu[i0:i0+xf]=mu[i0:i0+xf]*(1-fade)+tail[:xf]*fade; mu[i0+xf:i0+len(tail)]=tail[xf:]
t=np.arange(N)/SR; mu*=np.clip(t/0.5,0,1)[:,None]*np.clip((DUR-t)/1.0,0,1)[:,None]
wr('music-cut.wav',mu)
# ---- SFX (synth, quiet)
rng=np.random.default_rng(21); S=np.zeros((N,2))
def env(n,a,d): tt=np.arange(n)/SR; return np.minimum(1,tt/a)*np.exp(-tt/d)
def thock(f=110,d=0.09,noise=0.25,L=0.35):
    n=int(L*SR); tt=np.arange(n)/SR; fr=f*(1+1.2*np.exp(-tt/0.012)); return np.sin(2*np.pi*np.cumsum(fr)/SR)*env(n,0.002,d)+rng.standard_normal(n)*env(n,0.001,0.015)*noise
def click(f=2400,L=0.06): n=int(L*SR); tt=np.arange(n)/SR; return np.sin(2*np.pi*f*tt)*env(n,0.0005,0.008)
def key(): n=int(.05*SR); x=rng.standard_normal(n)*env(n,.0005,.006); return np.convolve(x,np.ones(4)/4,'same')+click(rng.uniform(1800,3200),.05)*.3
def whoosh(L=0.6):
    n=int(L*SR); x=rng.standard_normal(n); x=np.convolve(x,np.ones(30)/30,'same'); return x*np.sin(np.pi*np.arange(n)/n)**2*0.6
def chime(f=660,L=2.0):
    n=int(L*SR); tt=np.arange(n)/SR; return sum(np.sin(2*np.pi*f*k*tt)/k**1.5 for k in (1,2,3))*env(n,0.004,0.6)
P='Launch VYRA, my home-fitness brand.'
# reproduce index.html ctimes
s=1;acc=0;arr=[]
for i,ch in enumerate(P):
    s=(s*9301+49297)%233280; d=.6+.8*(s/233280)
    if ch==' ': d*=1.4
    if i>0 and P[i-1]==',': d*=2.4
    acc+=d; arr.append(acc)
for x in arr: place(S,key(),1.0+3.25*x/acc,0.35,rng.uniform(-.3,.3))
place(S,click(1500),4.62,0.4); place(S,thock(140,.08,.3,.3),4.7,0.6)
place(S,whoosh(0.7),4.85,0.35); place(S,whoosh(0.9),5.0,0.25)
place(S,thock(220,.05,.2,.2),5.75,0.3); place(S,click(3000),6.25,0.15)
Ts=[6.6,12.0,17.1,21.6,26.4,30.6,35.1,40.6,44.6]
for i,T in enumerate(Ts):
    place(S,whoosh(0.55),T,0.4,0.4*(-1)**i); place(S,thock(85+10*(i%3),.12,.35,.45),T+0.55,0.8); place(S,click(2600),T+1.0,0.2)
for i in range(16): place(S,thock(300+15*(i%4),.03,.2,.12),6.6+.95+i*.11,0.12,0.3*np.sin(i))
for k in [0,1,2,3,4]: place(S,thock(320,.03,.2,.12),12.9+k*.13,0.15)
place(S,click(2200),15.35,0.35); place(S,chime(880,1.2),15.45,0.12)
place(S,whoosh(0.8),17.25,0.25)
n=int(1.2*SR); sw=rng.standard_normal(n); sw=np.convolve(sw,np.ones(12)/12,'same')*np.sin(np.pi*np.arange(n)/n); place(S,sw*0.4,23.4,0.25)
for T,c in [(26.4+1.45,1),(30.6+1.3,1),(35.1+.85,3),(40.6+.85,4),(44.6+.85,3)]:
    for k in range(c): place(S,thock(260,.04,.25,.15),T+k*.18,0.18)
place(S,click(1900),48.85,0.45); place(S,chime(523.25,1.5),49.3,0.22); place(S,chime(783.99,1.5),49.36,0.12)
place(S,whoosh(1.0),49.75,0.45); place(S,thock(55,.3,.5,.9),50.7,0.9)
place(S,thock(120,.08,.3,.3),51.2,0.5); place(S,thock(110,.08,.3,.3),51.45,0.5)
place(S,whoosh(0.8),52.6,0.35); place(S,chime(659.25,2.5),53.45,0.22); place(S,chime(987.77,2.5),53.5,0.1)
S/=np.max(np.abs(S))*1.25
wr('sfx.wav',S)
# ---- mix
rms=lambda a: np.sqrt(np.mean(a[np.abs(a).max(1)>1e-4]**2))
Vn=V*(0.1/rms(V)); Mn=mu*(0.1/rms(mu))
duck=np.zeros(N)
for s_,e_ in spans: duck=np.maximum(duck,np.clip(np.minimum((t-(s_-0.25))/0.25,((e_+0.35)-t)/0.35),0,1))
g=10**((-6-11*duck)/20)
mix=Vn+Mn*g[:,None]+S*0.35
wr('mix-vo-music.wav',mix); wr('mix-sfx.wav',S)
print('spans',[(round(a,2),round(b,2)) for a,b in spans])
