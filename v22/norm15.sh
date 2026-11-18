#!/bin/bash
# norm.sh in.wav out.wav  -> two-pass loudnorm -14 LUFS TP -1.5
set -e
J=$(ffmpeg -hide_banner -i "$1" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
g(){ echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i "$1" -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" -ac 2 "$2"
