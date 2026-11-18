#!/bin/bash
set -e
cd /home/dell/aimy-promo/biz-promos/v22
D=/home/dell/Downloads/aimy-business-promos
ffmpeg -v error -y -framerate 30 -i frames/%05d.png -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -movflags +faststart video.mp4
ffmpeg -v error -y -i video.mp4 -i audio/final-sfx.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $D/22-output-wall-60s.mp4
ffmpeg -v error -y -i video.mp4 -i audio/final-vo-music.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $D/22-output-wall-60s-vo-music.mp4
echo encoded
