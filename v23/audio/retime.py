import numpy as np, wave, json
w=wave.open('vo.wav'); sr=w.getframerate(); ch=w.getnchannels(); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768; w.close()
if ch>1: a=a.reshape(-1,ch).mean(1)
# find silence-centred cut points near the line boundaries
hop=int(.01*sr); e=np.array([np.sqrt(np.mean(a[i:i+hop]**2)) for i in range(0,len(a)-hop,hop)])
def cut(lo,hi):
    i0,i1=int(lo/.01),int(hi/.01); k=i0+np.argmin(np.convolve(e[i0:i1],np.ones(15)/15,'same')); return k*.01
B=[(5.4,6.15),(9.8,10.45),(13.1,13.85),(17.0,17.5),(19.6,20.25),(21.9,22.5),(24.5,25.05),(27.6,28.9),(30.6,31.25),(35.5,36.4)]
cuts=[0]+[cut(*b) for b in B]+[len(a)/sr]
print('cuts',[round(c,2) for c in cuts])
tgt=[0.8,7.1,11.85,16.5,20.7,24.9,28.9,33.1,37.5,41.7,48.5]
DUR=58.0; out=np.zeros(int(DUR*sr))
for (s,e2),tg in zip(zip(cuts[:-1],cuts[1:]),tgt):
    seg=a[int(s*sr):int(e2*sr)].copy(); on=np.argmax(np.abs(seg)>0.02)/sr; p=tg-on; print('onset',round(on,2)); n=len(seg); f=int(.01*sr); seg[:f]*=np.linspace(0,1,f); seg[-f:]*=np.linspace(1,0,f)
    i=int(p*sr); out[i:i+n]+=seg[:len(out)-i]
    print(f'line at {p:5.2f}  len {n/sr:.2f}  ends {p+n/sr:.2f}')
w=wave.open('vo-timed.wav','w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(out,-1,1)*32767).astype(np.int16).tobytes()); w.close()
