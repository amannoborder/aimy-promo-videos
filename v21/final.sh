#!/bin/bash
set -e
cd /home/dell/aimy-promo/biz-promos/v21
OUT=/home/dell/Downloads/aimy-business-promos
[ -s video.mp4 ] || flock ../render.lock timeout 5400 ffmpeg -y -loglevel error -framerate 30 -i frames/%05d.png -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -movflags +faststart video.mp4
for k in sfx vo-music; do
  in=audio/mix-$k.wav
  ./loud.sh $in audio/final-$k.wav
done
flock ../render.lock timeout 900 ffmpeg -y -loglevel error -i video.mp4 -i audio/final-sfx.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $OUT/21-chat-build-60s.mp4
flock ../render.lock timeout 900 ffmpeg -y -loglevel error -i video.mp4 -i audio/final-vo-music.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $OUT/21-chat-build-60s-vo-music.mp4
for f in $OUT/21-chat-build-60s.mp4 $OUT/21-chat-build-60s-vo-music.mp4; do
  ffprobe -v error -show_entries format=duration:stream=width,height -of csv=p=0 $f
  ffmpeg -hide_banner -i $f -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I:|Peak:)" | tail -2
done
