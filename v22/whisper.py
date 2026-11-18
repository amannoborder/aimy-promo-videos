import sys,json
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[3] if len(sys.argv)>3 else "medium",device="cpu",compute_type="int8")
segs,_=m.transcribe(sys.argv[1],language="en",word_timestamps=True)
W=[{"w":w.word.strip(),"s":round(w.start,3),"e":round(w.end,3)} for s in segs for w in s.words]
json.dump(W,open(sys.argv[2],"w"),indent=0)
print(" ".join(f"{x['w']}@{x['s']}" for x in W))
