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

## Version 7

- **No booms**: the music has no drums, timpani rolls or sub hits any more (`scripts/strings_score4.py`).
- **More movement in the strings for retention**, after comparing with AB Nasdaq as well as Iman
  (`scripts/music_events.py`): violins alternate every 4 bars between re-bowed pairs (Iman) and broken chords (AB),
  4-bar swells, and a melody that walks into each chord. Sound and level are the same as v6.
- `scripts/level_score.py` now keeps the true section levels (it used to renormalise to the loudest peak, which
  only worked while the booms were the peaks).
- **No zoom on the opening**; the first zoom is "I was this close". The other zooms are unchanged.

## Version 8

- **Music back to v6's violins** (`scripts/strings_score5.py`): v7's alternating broken-chord "tick-tock" violins
  are gone; the strings are exactly v6's, without the booms, playing at v6's level. The light tambourine tick from v6
  sits 2-3 dB quieter.
- **Subtle sound effects** (`scripts/sfx2.py`, built from real CC0 recordings: tambourine, sleigh bells,
  glockenspiel, triangle; cues in `v8/edl8.json`):
  - a cash-register "cha-ching" on the money moments ("$10,000 in just three days" twice, "$300,000",
    "my first $10,000 month", the payout card)
  - three quick, rising lighter ones on "sale after sale after sale"
  - a soft whoosh under the five quicker zooms
  - a soft pop as each number lands on the 01 / 02 / 03 cards and the recap
  - a phone "ding" on "my personal phone number"
  All sit a few dB under Ricky's voice.
- Picture is the same as v7.

## Version 9

- **v6's music exactly**, the version that was liked, with only the long sub "drop" boom under each hit removed
  (`scripts/strings_score3.py --no-sub`). The timpani hits and rolls that build the tension stay. Iman's bed has the
  same shape: short low hits on key phrases about every 15 s and constant string motion, no long crescendos.
  v7/v8 had removed every hit and roll, which flattened the tension.
- Sound effects as in v8 (cash register, pops, whooshes, ding). Picture as in v7.

## Variant A: "Me And The Devil" (instrumental)

- `scripts/song_bed.py` turns the uploaded track into a bed: keeps only its tonal part (harmonic/percussive
  separation drops every kick, 808 hit and snare), cuts everything under 160 Hz so no boom is left (the sub band
  falls from −8 dB to −48 dB relative to the rest), loops it on its own 2-beat grid at the points where the music
  matches best (`variant-a-song/loop_plan.json`), and evens the level so the tension holds the whole 6:19.
- Same picture and sound effects as v9; the music sits about 15 dB under Ricky's voice.
- The song file isn't in this repo (it's copyrighted and this repo is public). Using it in a paid ad needs a licence.

## Variant B: AB Nasdaq style (`scripts/plan_ab.py`, `scripts/cards_ab.py`)

Measured on AB's video first (`scripts/ab_zoom_analysis.py`): a cut every ~4 s between his face, graphics and
proof, and on his face the shot is never still: about 80% of face shots slowly push in or pull out by 15-25% over
5-15 s.

- Word-group captions (2-4 words, one line, white, tight Apple-style sans with a soft shadow, no punctuation).
- Key phrases drop to their own line in heavy electric-blue caps with a glow ("THIS CLOSE", "$10,000 IN 3 DAYS",
  "DO NOT CLICK OFF", "COMPLETELY FREE", "DOWN BELOW"...).
- The always-moving zoom on Ricky, cropped from the 4K original, held wide wherever text needs the empty side.
- The hook as stacked regular + heavy-caps text in the empty left side, then a big blue "$87".
- White keynote cards with black words appearing as he says them; big blue numbers on white ($0, 18,000,000, $87).
- Proof as clean cards on a light-grey keynote plate; photos beside him in thin white frames; clips framed on white.
- "YOUTUBE SHORTS" in giant letters behind his head (his outline cut out per frame with OpenCV GrabCut).
- "The three things" as a list in the empty side of the frame with an arrow on the one he's on.
- The offer as a split screen ("WHAT'S INCLUDED INSIDE YTD") building line by line.
- A whoosh or pop on every graphic, cash-register sounds on the money moments, the boom-free song bed softer
  underneath (17 dB under the voice, like AB's quieter bed).

## Variant B2: AB Nasdaq 1:1 (`scripts/plan_ab2.py`, breakdown in `01-vsls/reference-vsls/AB-BREAKDOWN.md`)

- Word captions exactly like AB's: lowercase, no punctuation, his size and tight spacing, hard switches, now 1-2
  words at a time, over AB's dark fade along the bottom of the frame.
- AB's side text used for ~30 key lines through the whole video: a regular line, then heavy caps with the key word in
  blue, built as Ricky says it (letter-by-letter blur-in) on a white fade from that edge; the bottom captions step
  aside while it's up. The "three things" list sits on AB's dark grey fade instead.
- A subtle mouse click on every caption and every piece of text (no more pops), whooshes on cards, the cash sounds.
- "YOUTUBE SHORTS" now sits fully visible at the top (in front of him, nothing cut off).
- The zoom never moves faster than 5% per second and only drifts while side text needs the room.
- A slot for his diner photo or 2-second clip on "dining server" (both times): upload it to
  `02-results-and-b-roll/` named `diner.jpg` / `diner.mov` (or `.heic`, `.png`, `.mp4`) and it drops in beside him.
