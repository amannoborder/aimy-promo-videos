#!/bin/bash
# encode video + two mixes, loudnorm to -14 LUFS / TP -1
set -e
cd /home/dell/aimy-promo/biz-promos/v25
L=/home/dell/aimy-promo/biz-promos/render.lock
[ -f video.mp4 ] || flock $L timeout 5400 ffmpeg -v error -y -framerate 30 -i frames/%05d.png -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p video.mp4
for k in sfx vo-music; do
  J=$(ffmpeg -hide_banner -i audio/mix-$k.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
  mi=$(echo "$J"|python3 -c "import json,sys;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
  ffmpeg -v error -y -i audio/mix-$k.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:$mi:linear=true -ar 48000 -ac 2 audio/final-$k.wav
done
D=/home/dell/Downloads/aimy-business-promos
flock $L ffmpeg -v error -y -i video.mp4 -i audio/final-sfx.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $D/25-macro-layers-60s.mp4
flock $L ffmpeg -v error -y -i video.mp4 -i audio/final-vo-music.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $D/25-macro-layers-60s-vo-music.mp4
for f in $D/25-macro-layers-60s.mp4 $D/25-macro-layers-60s-vo-music.mp4; do
  ffprobe -v error -show_entries format=duration:stream=width,height -of csv=p=0 $f
  ffmpeg -hide_banner -i $f -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I:|Peak:)" | tail -2
done
