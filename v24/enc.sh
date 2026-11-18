#!/bin/bash
set -e
cd /home/dell/aimy-promo/biz-promos/v24
[ -s video.mp4 ] || exit 1
for k in vo-music sfx; do
  J=$(ffmpeg -hide_banner -i audio/mix-$k.wav -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
  g(){ echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
  ffmpeg -loglevel error -y -i audio/mix-$k.wav -af "loudnorm=I=-14:TP=-2.2:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true" -ar 48000 -ac 2 audio/final-$k.wav
done
ffmpeg -loglevel error -y -i video.mp4 -i audio/final-sfx.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart /home/dell/Downloads/aimy-business-promos/24-zoom-through-60s.mp4
ffmpeg -loglevel error -y -i video.mp4 -i audio/final-vo-music.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart /home/dell/Downloads/aimy-business-promos/24-zoom-through-60s-vo-music.mp4
