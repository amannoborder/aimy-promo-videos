# AIMY promo videos (code-animated)

Standalone promo films for AIMY ("a company of AI employees in one chat"), built as HTML/Canvas/Three.js
animations and rendered to MP4. Not part of the AIMY app, the Short Video agent or the Long Video agent.

- `BRIEF.md` — rules every film follows (official AIMY logo used whole, no Japanese, girl model only, VO/music settings, QA).
- `en-pack/` — English VYRA demo assets + official AIMY logo files.
- `render-any.mjs` — renders `index.html` frame by frame (`window.seek(t)`, `window.DUR`) with Playwright; encode with ffmpeg.
- `vNN/` — one film per folder (`index.html` + helper scripts). Versions 04, 08, 12, 16–18, 21–25.
  Sources for 01–03, 05–07, 09–11, 13–15, 19–20 were lost in a reboot; their final MP4s exist outside this repo.
- Style references: github.com/yihui-dev/awesome-opus5-5-videos (not vendored).

Not in git (local only): render frames, MP4s, audio (VO/music/SFX), reference downloads.
Voice = Gemini TTS (gemini-3.8-flash-tts, Charon); music = Gemini Lyria (lyria-3.5) via local scripts — no keys in this repo.

Render: `node render-any.mjs vNN/index.html vNN/frames 30 1920 1080` then
`ffmpeg -framerate 30 -i vNN/frames/%05d.png -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart out.mp4`.
