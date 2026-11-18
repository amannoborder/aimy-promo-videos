# AIMY business promos — shared brief (rebuilt 2026-11-17 after a reboot wiped /tmp)

WORK ONLY UNDER `/home/dell/aimy-promo/biz-promos/<vNN>/` — persistent disk. Never put work in /tmp (a reboot just
deleted every work dir). Deliver to `/home/dell/Downloads/aimy-business-promos/`.

## AIMY facts (say only what is true)
"A company of AI employees in one chat." You give the work in one chat; AI employees do it in a fixed order; 52
employees in total. Roster used in promos: 01 Project Manager · 02 Counseling · 05 Market Analysis · 11 Knowledge ·
12 Funnel · 13 Logo (nine ideas, you pick one) · 14 Brand Kit · 15 Portrait (selfie → studio portrait) · 17 Website ·
21 YouTube · 22 Long Video · 23 Thumbnail · 24 X · 25 Instagram · 26 Short Video · 27 Threads · 28 TikTok ·
29 Facebook · 35 SNS Cover · 42 Ads (nothing spends until you approve). Demo customer: VYRA home-fitness brand.
No invented performance numbers.

## Hard rules
- **No Japanese anywhere** (images, mock UIs, captions, HTML text). Use only the English pack below; rebuild any
  social/app screen in HTML with English copy.
- **AIMY logo**: only `en-pack/aimy-logo-dark.png` (light grounds) / `aimy-logo-white.png` (dark grounds), 900×634,
  stacked symbol over wordmark — used WHOLE, scaled only. Never crop symbol and word apart, never side-by-side, never an
  app-icon tile with the symbol alone, never a retyped wordmark.
- **Girl model only** — never a man, not even a male-reading silhouette/figure. (Robots/abstract avatars are fine.)

## English pack `/home/dell/aimy-promo/biz-promos/en-pack/` (all checked JP-free; look before using)
brandboard-en.jpg (English Brand Kit board) · brand-hero-en.jpg (VYRA logo + "Move at Home. Fit into Your Life." + girl)
· website-hero-en.jpg (laptop LP "Move First. Feel Strong.") · lp-phone-screen-en.jpg · lp-tall-en.jpg (780×3073
scrolling LP) · thumb-en-1/2/3.jpg (16:9) · cover-en-move-your-city.jpg, cover-en-fitness-1/3.jpg (1400×383),
girl-cover-1/2/3.png (1546×423) · banner-en.jpg (1200×306) · ad-en-vyra-girl.jpg (900²), ad-en-busy-routine.jpg
(1254², different girl model) · tiktok-en-squat.jpg (9:16) · logo-sheet-nine-en.png (nine VYRA logo ideas) ·
vyra-logo-en.png (picked VYRA logo, transparent, dark letters) · sns-cover-concepts-en-ui.jpg · photos without text:
girl-pose-1..4.jpg, view-list-photos.jpg, 07-model-photo-1..4.jpg, 02-portrait.jpg, 01-original-photo.jpg ·
aimy-logo-dark.png / aimy-logo-white.png.

## Build + render
- One `index.html` per film; every visual a pure function of time in `window.seek(t)`; `window.DUR` set.
  Canvas/SVG/GSAP (paused timeline)/Three.js fine. Google Fonts via <link> fine.
- Renderer: `node /home/dell/aimy-promo/biz-promos/render-any.mjs <index.html> <framesdir> <fps> <W> <H> [from] [to]`
  (`RESUME=1` skips frames already on disk — use it after any interruption). Preview a frame per second first.
- Full renders and encodes ONLY under the shared lock + timeout:
  `flock /home/dell/aimy-promo/biz-promos/render.lock timeout 5400 <cmd>` (4-core laptop, one render at a time).
  Never hold the lock while not rendering. libx264 crf 18, yuv420p, +faststart.
- Do not use `pkill -f` with your own pattern. No git, servers, deploys or posting.

## Sound
- VO: `node ~/.claude/qa/gtts-local.mjs Charon "<all lines, blank line between>" vo.wav` — Gemini
  `gemini-3.8-flash-tts`, Charon, NORMAL speed, ONE call, write "Amy" for AIMY; on 429 wait 90 s, retry once.
- Music: `node ~/.claude/qa/gmusic-local.mjs "<prompt>" music` (Lyria lyria-3.5, ~60 s instrumental) — prompt starts
  "Instrumental only, no vocals.", max 2 generations, end with a fade/clean ending on the end card.
- Mix: duck music ~11 dB under VO, quiet synthesized UI SFX, final −14 LUFS, true peak ≤ −1 dB, AAC 192k.
- Never print the Gemini key.

## QA before delivering
- `/home/dell/.claude/qa/jpcheck-video.sh <file.mp4>` must say `JP frames=0` (Gemini vision, 1 frame/s). If a frame is
  flagged, look at it — "Official LINE | ¥2,980" has been a false alarm before; re-run to confirm.
- 1-fps frame sheet, look at every frame (girl only, official logo whole, nothing clipped/empty, text readable).
- faster-whisper (`HF_HUB_OFFLINE=1`) on the final mix: every VO line said, "Amy" pronounced, no music vocals.
- Report: paths, length, aspect, what you built, VO script, music prompt, jpcheck + loudness, honest weaknesses.
