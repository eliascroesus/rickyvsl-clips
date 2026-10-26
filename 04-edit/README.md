# Edit

How Ricky's VSL is put together. Nothing in here needs uploading; it's the editing setup.

- `scripts/music.py`: the original score (A minor, 80 BPM), written from scratch so there's nothing to license.
  Rendered as separate layers (drone, pads, music box, arpeggio, heartbeat, clock ticks, hi-hats) so the music can
  build and drop with the edit.
- `scripts/sfx.py`: sound effects (whoosh, pop, boom, sub drop, riser, reverse swell, tick).
- `scripts/cards.py`: the results cards made from `02-results-and-b-roll/`: cropped, chargebacks and store name
  hidden, rounded corners, shadow, and a purple outline on the key number.
- `scripts/render.py`: renders the video from an edit list (cuts, results cards, phone clips, captions, titles,
  music, sound effects) and sets the final loudness to −14 LUFS.
- `scripts/voice_chain.txt`: the voice clean-up (low cut, clarity, compression, de-essing).
- `edl_test.json`: the edit list used for the 24-second style test.
