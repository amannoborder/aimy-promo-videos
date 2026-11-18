import sys
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[2] if len(sys.argv)>2 else "small",device="cpu",compute_type="int8")
segs,_=m.transcribe(sys.argv[1],word_timestamps=True)
for s in segs:
    print(" ".join(f"{w.word.strip()}@{w.start:.2f}-{w.end:.2f}" for w in s.words))
