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

## Version 4 audio (real strings)

- `scripts/strings_score.py`: the score played with real recorded strings and percussion from the Versilian Studios
  Chamber Orchestra 2 Community Edition (VSCO 2 CE, public domain / CC0, https://github.com/sgossner/VSCO-2-CE), so it's
  safe for ads. A minor, 115 BPM: cello + bass eighth-note ostinato, viola sixteenth ticks, long swelling violin notes,
  violin tremolo for the hook, timpani rolls into timpani + bass drum + low-string hits.
- `scripts/vsco_index.py`: indexes the samples and checks each one's real pitch.
- Video is the same as version 3; only the music and hits changed (`v3/edl4.json`).

## Version 5 (zooms + strings rewritten after Iman's violins)

- **Zooms on Ricky** (`ZOOMS` in `scripts/plan3.py`, drawn by the `Zoom` class in `scripts/compositor.py`): 13
  moves at the tense lines. Slow push-ins (e.g. the hook into "$87", the mom quote, "everybody was right about me",
  the build into "YouTube Shorts", the guarantee into "60 DAYS") and snap punch-ins ("I was *this close*", "the truth
  is, you don't", "I can't do this anymore", "you're falling for the TikTok scams", "please do not click off").
  Each one cuts back to the wide shot at its end. They're cropped from the 4K original, so they stay sharp, and never
  run during screen shares or title cards.
- **Strings rewritten** (`scripts/strings_score2.py`) after measuring how the strings move in Iman's bed
  (`01-vsls/reference-vsls/IMAN-AUDIO.md`, tool: `scripts/iman_violins.py`): chords every 2 beats over a falling
  A-G-F-E bass, violins re-bowing on every 16th, an E pedal ticking in eighths, a melody that moves with each
  chord, a rising staircase into the reveal and a slide down into "what most people don't understand".
- `scripts/level_score.py`: levels the score per section; the music then sits 2 dB lower than in v4 (`v5/edl5.json`).
- `scripts/render_chunks.sh`: renders the video in parallel chunks that can be resumed.

## Version 6

- **Score rebuilt to match the sound of Iman's bed** (`scripts/strings_score3.py`, compared with
  `scripts/compare_bed.py`): 102 BPM, a ticking tambourine layer in 16ths panned wide, crisp short strings with less
  reverb, a narrower stereo image, a brighter top end and sub under the hits. Findings in
  `01-vsls/reference-vsls/IMAN-AUDIO.md`. The tambourine comes from VSCO 2 CE's "Miscellania Raw" folder (CC0).
- **Music about 1 dB louder than v5** (`v6/edl6.json`).
- **Zooms are smooth now**: every move is a set of keyframes eased in and out (`ZOOMS` in `scripts/plan3.py`), no
  instant punch-ins or snap-backs; where a move starts or ends wide it crossfades with the footage.
- **The opening "$87" is a red number on top of Ricky** (top-left, with "IN SALES." under it) instead of its own black
  page, so you see him lift his phone with the real stats at the same time (`OVERLAY_TITLES` in `scripts/plan3.py`).
