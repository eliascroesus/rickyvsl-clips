# Edit

How Ricky's VSL is put together. Nothing in here needs uploading; it's the editing setup.

## Pieces

- `scripts/transcribe.py`: word-level transcript of the raw video (Whisper large-v3-turbo) → `transcript.json`.
- `scripts/plan.py`: the edit itself. A cue sheet in raw-video time (titles, results cards, phone clips, number
  outlines, top labels, music sections, sound effects) plus pause cutting and caption grouping, compiled into
  `edl.json`.
- `scripts/render.py`: renders the video from `edl.json` and mixes the audio to −14 LUFS.
- `scripts/music.py` / `scripts/sfx.py`: the original score (A minor, 80 BPM, in layers) and sound effects,
  written from scratch, so there's nothing to license.
- `scripts/cards.py`: the results cards made from `02-results-and-b-roll/` (cropped, chargebacks and store name
  hidden, purple outline on the key number).
- `scripts/qa_audio.py` / `scripts/qa_frames.py`: checks: music level under the voice per section, and a still
  from every title, card, outline, clip and label.
- `scripts/voice_chain.txt`: the voice clean-up (low cut, clarity, compression, de-essing).

## Changing something

Edit the cue sheet at the top of `scripts/plan.py` (times are in the raw video, see
`03-raw-vsl-footage/TRANSCRIPT.md`), then run `plan.py` and `render.py` again.

## Version 2 (Iman Gadzhi style)

- `scripts/brand.py`: the look. Near-black plate with a purple glow, per-letter blur-in text, headlines over
  Ricky with a handwritten sub-line (Unbounded + Caveat fonts), framed cards with a glow and slight tilt, photo stickers.
- `scripts/plan2.py`: the v2 cue sheet (title cards, headlines, results on the plate, photos popping up beside
  Ricky, screen recordings in glowing frames, phone clips) → `v2/elements.json`, `v2/text.ass`, `v2/edl2.json`.
- `scripts/compositor.py`: draws the animated graphics frame by frame over the cut footage and burns in the text.
- `scripts/music2.py` + `scripts/music_cues2.py`: the cinematic fallback score (string-style pads, sub swells, low
  pulse) and where each part plays. Swap in licensed tracks when available.

## Version 3

- `scripts/plan3.py`: plain static subtitles (no animation or colour), no animated headlines, screen shares left
  exactly as recorded, results and photos popping up beside Ricky with a thud, title cards kept.
- `scripts/music3.py` + `scripts/music_cues3.py`: the tension score modelled on Iman Gadzhi's bed (breakdown in
  `01-vsls/reference-vsls/IMAN-AUDIO.md`): starts on frame 1, hit after the hook, 115 BPM bass pulse, never silent.
- `scripts/separate.py`, `voice_comb.py`, `gap_music.py`, `analyze_bed.py`: the tools used to study Iman's audio.
