import numpy as np, wave
SR=48000; N=int(58.0*SR)
def rd(p):
    w=wave.open(p); sr=w.getframerate(); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float).reshape(-1,w.getnchannels())/32768; w.close()
    if a.shape[1]==1: a=np.repeat(a,2,1)
    if sr!=SR: idx=np.arange(0,len(a),sr/SR); a=np.stack([np.interp(idx,np.arange(len(a)),a[:,c]) for c in (0,1)],1)
    return a
def fit(a,off=0.0):
    a=np.pad(a,((int(off*SR),0),(0,0))); return np.pad(a,((0,max(0,N-len(a))),(0,0)))[:N]
def wr(p,a):
    w=wave.open(p,'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(a,-1,1)*32767).astype(np.int16).tobytes()); w.close()
vo=fit(rd('vo-timed.wav')); mu=fit(rd('music.wav'),0.3); sf=fit(rd('sfx.wav'))
rms=lambda a: np.sqrt(np.mean(a[np.abs(a).max(1)>1e-4]**2))
vo*=0.1/rms(vo); mu*=0.1/rms(mu)
# duck from the VO envelope: speech regions (merged gaps <0.7 s)
hop=SR//100; e=np.array([np.abs(vo[i:i+hop]).max() for i in range(0,N,hop)])>0.02
sp=np.zeros(len(e)); last=-999
for i,v in enumerate(e):
    if v:
        if i-last<70: sp[last:i+1]=1
        sp[i]=1; last=i
k=np.ones(30)/30; d=np.clip(np.convolve(sp,k,'same')*1.5,0,1)
duck=np.interp(np.arange(N)/SR,np.arange(len(d))/100,d)
g=10**((-6-11*duck)/20); t=np.arange(N)/SR
mu=mu*(g*np.clip(t/0.3,0,1)*np.clip((57.9-t)/0.6,0,1))[:,None]
wr('mix-vo-music.wav',vo+mu+sf*0.3); wr('mix-sfx.wav',sf)
