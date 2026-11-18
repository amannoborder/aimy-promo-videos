#!/bin/bash
cd /home/dell/aimy-promo/biz-promos/v12
for r in "0 420" "420 840" "840 1260" "1260 1635"; do
  set -- $r
  RESUME=1 flock /home/dell/aimy-promo/biz-promos/render.lock timeout 5400 node /home/dell/aimy-promo/biz-promos/render-any.mjs index.html frames 30 1920 1080 $1 $2 || echo "chunk $1 failed"
done
ls frames | wc -l
