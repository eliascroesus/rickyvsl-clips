# Iman Gadzhi: how his audio builds tension

A closer look at the music and sound in `imangadzhivsl.mp4`, and how Ricky's score copies it.

How it was measured: Iman talks almost nonstop (only 21 pauses long enough to hear the music on its own, about
4 seconds in total), so the music was studied three ways: in those pauses, by filtering out his voice (his speaking
pitch sits around A2, about 110 Hz), and in the deep bass below his voice, where the music is on its own.

## What he does

| What | Measured | Why it works |
| --- | --- | --- |
| Music from the first frame | Bed is already playing under "All right, congratulations…" | No warm-up. You're inside a scene, not watching a video start |
| Thin and airy at first | Almost no bass in the first 3 s (sub-bass around −47 dB) | Leaves room for the hit, and feels unresolved |
| A big hit right after the hook | Sub-bass jumps about 18 dB at 3.3 s and again at 4.4 s, with a whoosh, as the logo slams in | The "oh shit, what is this" moment. Your body reacts before your brain does |
| A driving pulse after the hit | Bass repeats in eighth notes at about 115 BPM, strongest in the first 10 s | Momentum. It feels like something is about to happen |
| It never stops | Speech in 89–99% of every 5 s, music under all of it, loudness range only 2.6 LU | No dead air, so there's never a natural moment to click away |
| Sits under the voice | About 12–15 dB below his voice | Felt more than heard; the words stay clear |
| Hits on graphics | Swooshes on every text card, extra sub hits on key moments (e.g. around 1:35) | Each graphic feels like an event |
| Ends with him | Rings out on an open A–E chord (no third) after the last word | Unresolved and confident at the same time |
| Key | Centres on A | |

## How Ricky's score copies it (`04-edit/scripts/music3.py`, cues in `music_cues3.py`)

- **0:00 to "$87":** starts on frame 1 with an eerie high string cluster (A, B♭, E, a semitone rub) and fast muted
  ticks, no bass, while a riser builds for 5.7 seconds.
- **"$87":** braam-and-boom hit (a cinematic low brass-like stab with a sub drop) with the title card.
- **"I owed money to my mom…":** a driving eighth-note bass pulse at 115 BPM in A, with a low drone.
- **"Then, I changed three simple things":** a second, smaller hit and the chords open up (Am–F–C–G), with the pulse
  following them.
- **The rest:** the pedal pulse and cluster come back for tension (the pain section, the open loop, "don't click
  off", "what most people don't understand"), with a hit on each title card. The only silence is the half second
  before "YouTube Shorts", which lands with the biggest hit. The music sits 12–14 dB under Ricky the whole way and
  rings out on the A drone after "I will see you inside."

A cleaner breakdown (his music fully separated from his voice) needs the Demucs separation model, whose download
host (`dl.fbaipublicfiles.com`) is blocked in this environment.
