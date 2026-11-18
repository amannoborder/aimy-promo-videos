import sys
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[2] if len(sys.argv)>2 else "small",device="cpu",compute_type="int8")
segs,_=m.transcribe(sys.argv[1],word_timestamps=True,vad_filter=False)
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}")
