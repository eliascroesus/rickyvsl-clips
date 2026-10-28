"""Audio for Ricky's thank-you video: his cleaned-up voice cut like the picture, the music bed flat under it
(about 19 dB under the voice, no ducking, like AB), no sound effects; loudness-normalised to -14 LUFS.

    python ty_mix.py plan.json bed.wav out.wav [music_under_db]
"""
import json, subprocess, sys
import numpy as np
import soundfile as sf

SR = 48000


def main():
    plan = json.load(open(sys.argv[1]))
    bed, sr = sf.read(sys.argv[2], dtype="float64")
    out = sys.argv[3]
    under = float(sys.argv[4]) if len(sys.argv) > 4 else 19.0
    v, vsr = sf.read("/home/user/work/edit/ty/voice_proc.wav", dtype="float64")
    assert vsr == SR and sr == SR
    n = int(round(plan["dur"] * SR))
    voice = np.zeros((n, 2))
    pos, fade = 0, int(0.008 * SR)
    for a, b in plan["keep"]:
        seg = v[int(round(a * SR)):int(round(b * SR))].copy()
        seg[:fade] *= np.linspace(0, 1, fade)[:, None]
        seg[-fade:] *= np.linspace(1, 0, fade)[:, None]
        m = min(len(seg), n - pos)
        voice[pos:pos + m] += seg[:m]
        pos += len(seg)
    # speech level: RMS over 50 ms windows that are clearly talking
    hop = int(0.05 * SR)
    k = n // hop
    e = np.sqrt((voice[:k * hop].mean(1).reshape(k, hop) ** 2).mean(1))
    talk = e[e > np.percentile(e, 60) * 0.5]
    v_rms = np.sqrt((talk ** 2).mean())
    pivot = int(plan["music"]["pivot"] * SR)
    m_rms = np.sqrt((bed[:pivot] ** 2).mean())
    g = v_rms / m_rms * 10 ** (-under / 20)
    music = np.zeros((n, 2))
    m = min(n, len(bed))
    music[:m] = bed[:m] * g
    mix = voice + music
    tmp = out + ".pre.wav"
    sf.write(tmp, mix.astype(np.float32), SR, subtype="FLOAT")
    r = subprocess.run(["ffmpeg", "-v", "info", "-hide_banner", "-i", tmp, "-af",
                        "loudnorm=I=-14:TP=-1.2:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    st = json.loads(r.stderr[r.stderr.rindex("{"):])
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-af",
                    f"loudnorm=I=-14:TP=-1.2:LRA=9:measured_I={st['input_i']}:measured_TP={st['input_tp']}:"
                    f"measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:linear=true",
                    "-ar", str(SR), "-c:a", "pcm_s24le", out], check=True)
    print(f"voice cut into {len(plan['keep'])} pieces, music {under:.0f} dB under the voice (gain {20 * np.log10(g):.1f} dB)")


if __name__ == "__main__":
    main()
