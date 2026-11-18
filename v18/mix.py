import numpy as np, wave, json, subprocess
SR=48000
def rd(p):
    w=wave.open(p); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float).reshape(-1,w.getnchannels())/32768; w.close(); return a
def wr(p,a):
    w=wave.open(p,'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(a,-1,1)*32767).astype(np.int16).tobytes()); w.close()
N=int(54.44*SR)
def fitN(a): return np.pad(a,((0,max(0,N-len(a))),(0,0)))[:N]
vo,mu,sf=fitN(rd('vo2.wav')),fitN(rd('music-cut.wav')),fitN(rd('sfx.wav'))
rms=lambda a: np.sqrt(np.mean(a[np.abs(a).max(1)>1e-4]**2))
vo*=0.1/rms(vo); mu*=0.1/rms(mu)            # equal RMS reference
W=json.load(open('words-timed.json')); W[0]['s']=0.8
spans=[]
for x in W:
    s,e=x['s']-0.15,x['e']+0.2
    if spans and s-spans[-1][1]<0.7: spans[-1][1]=e
    else: spans.append([s,e])
t=np.arange(N)/SR; duck=np.zeros(N)
for s,e in spans:
    duck=np.maximum(duck,np.clip(np.minimum((t-(s-0.25))/0.25,((e+0.35)-t)/0.35),0,1))
g=10**((-6-11*duck)/20)                      # music bed -6 dB, -17 dB under VO (11 dB duck)
fi=np.clip(t/0.4,0,1); fo=np.clip((54.3-t)/1.6,0,1)
mu=mu*(g*fi*fo)[:,None]
mix=vo+mu+sf*0.35
wr('mix-vo-music.wav',mix); wr('mix-sfx.wav',sf)
print(spans[:3],len(spans))
