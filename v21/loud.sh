#!/bin/bash
# loud.sh in out : gain to -14 LUFS then true-peak-safe limiter, iterate twice
in=$1; out=$2; cp $in /tmp/claude-1000/-home-dell-aimy-chat/4de436d9-e14d-4a36-9f11-a7f9c9fc6d81/scratchpad/l0.wav
cur=/tmp/claude-1000/-home-dell-aimy-chat/4de436d9-e14d-4a36-9f11-a7f9c9fc6d81/scratchpad/l0.wav
for k in 1 2 3; do
  I=$(ffmpeg -hide_banner -i $cur -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}')
  g=$(python3 -c "print(-14-($I))")
  ffmpeg -y -loglevel error -i $cur -af "volume=${g}dB,aresample=192000,alimiter=limit=0.79:attack=1:release=60:level=disabled,aresample=48000" -c:a pcm_s16le /tmp/claude-1000/-home-dell-aimy-chat/4de436d9-e14d-4a36-9f11-a7f9c9fc6d81/scratchpad/l$k.wav
  cur=/tmp/claude-1000/-home-dell-aimy-chat/4de436d9-e14d-4a36-9f11-a7f9c9fc6d81/scratchpad/l$k.wav
done
cp $cur $out
