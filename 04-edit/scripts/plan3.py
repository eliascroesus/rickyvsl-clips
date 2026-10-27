"""Version 3: plain static subtitles, no animated headlines, screen shares untouched, results popping up beside Ricky
with a thud, title cards kept. Music is cued separately (music_cues3.py).

    python plan3.py transcript.json silences.txt OUTDIR
"""
import json, os, re, sys

sys.path.insert(0, "/home/user/work/scripts")
import brand as B
import cards2 as C2
import plan as P1
import plan2 as P2

CLIPDIR = P2.CLIPDIR
PU = P2.PU
SCREEN = [(24.30, 32.70), (207.43, 220.87), (233.73, 260.60)]       # his screen shares (raw time), left untouched

PLATE_CARDS = [  # name, t0, t1, max_w, max_h, tilt
    ("shop_11k", 38.45, 42.15, 1150, 720, 6),
    ("night_laptop", 61.95, 65.35, 760, 760, -5),
    ("shop_payout", 323.60, 326.80, 900, 760, -5),
]
STICKERS = [  # results / photos popping up beside Ricky: name, t0, t1, cx, cy, rotation, max_w, max_h
    ("shop_11k", 20.35, 22.30, 1450, 430, -3, 620, 480),
    ("playbutton_lv", 220.90, 223.55, 1470, 470, -4, 520, 560),
    ("shop_36k", 227.60, 230.60, 1450, 450, 3, 600, 520),
    ("shop_today_2k", 230.70, 233.60, 1450, 450, -3, 600, 520),
    ("gwagon", 267.00, 270.05, 1470, 470, 3, 520, 560),
    ("yt_sept_91m", 322.35, 323.55, 1430, 430, -2, 700, 420),
]
CLIPS = [  # file, t0, t1, in, mode, clip audio dB
    ("IMG_5163.MOV", 204.50, 206.75, 0.0, "plate", None),
    ("IMG_3996.MOV", 263.30, 266.95, 0.0, "pop", None),
    ("IMG_8117.mov", 270.50, 277.00, 3.0, "plate", -16),
]

SUBS = P2.STYLES.replace(
    "Style: Cap,Inter Display,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,-1,0,0,0,100,100,-0.5,0,1,0,3,2,140,140,70,1",
    "Style: Cap,Inter Display SemiBold,50,&H00FFFFFF,&H00FFFFFF,&H00000000,&H8C000000,0,0,0,0,100,100,0,0,1,0,2,2,160,160,64,1\n"
    "Style: CapS,Inter Display SemiBold,46,&H00FFFFFF,&H00FFFFFF,&H50000000,&H8C000000,0,0,0,0,100,100,0,0,3,10,0,1,110,820,48,1")
assert "Style: CapS" in SUBS and "Inter Display SemiBold,50" in SUBS


def ass_time(t):
    t = max(0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def ev(layer, t0, t1, style, text):
    return f"Dialogue: {layer},{ass_time(t0)},{ass_time(t1)},{style},,0,0,0,,{text}"


def wrap2(text, width):
    """Split into at most two balanced lines."""
    if len(text) <= width:
        return text
    words = text.split(" ")
    best, cut = None, 1
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        score = max(len(a), len(b))
        if best is None or score < best:
            best, cut = score, i
    return " ".join(words[:cut]) + "\\N" + " ".join(words[cut:])


def main():
    transcript, silences, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    words = P1.load_words(transcript)
    cuts = P1.load_cuts(silences)
    keep, t = [], 0.0
    for a, b in cuts:
        keep.append((t, a))
        t = b
    keep.append((t, P1.RAW_END))

    def m(x):
        out = 0.0
        for a, b in keep:
            if x <= a:
                return out
            if x < b:
                return out + x - a
            out += b - a
        return out

    total = m(P1.RAW_END)
    events, plates, elements, sfx, hide = [], [], [], [], []

    # ---- title cards (unchanged look); hits come from the music cue sheet
    for T in P2.TITLES:
        t0, t1 = m(T["t0"]), m(T["t1"])
        plates.append({"t0": t0, "t1": t1, "fade_in": 0.0 if T.get("fade_in") == 0 else 0.12, "fade_out": 0.12})
        hide.append((t0, t1))
        if not T["lines"]:
            continue
        size, n = T["size"], len(T["lines"])
        lh = size * 1.08
        extra = (60 if T.get("sub") else 0) + (70 if T.get("script") else 0)
        y0 = 540 - (n * lh + extra) / 2 + lh / 2 - 10
        clock = 0
        for li, parts in enumerate(T["lines"]):
            y = y0 + li * lh
            txt, _ = B.ass_rich_reveal(parts, start_ms=clock, stagger=max(18, 60 - len("".join(p for p, _ in parts)) * 2), dur=320, blur=16)
            events.append(ev(3, t0, t1, "Big", f"{{\\pos(960,{y:.0f})\\fs{size}\\fad(0,120)}}{txt}"))
            if T.get("underline"):
                full = "".join(p for p, _ in parts)
                if T["underline"] in full:
                    pre = full[:full.index(T["underline"])]
                    wfull = P2.M.width(full, P2.UNB_XB, size)
                    xs = 960 - wfull / 2 + P2.M.width(pre, P2.UNB_XB, size)
                    xe = xs + P2.M.width(T["underline"].strip(), P2.UNB_XB, size)
                    events.append(ev(3, t0, t1, "Box", B.ass_underline(int(xs), int(xe), int(y + size * 0.42), 650)))
            clock += 220
        ybot = y0 + (n - 1) * lh + size * 0.55
        if T.get("sub"):
            events.append(ev(3, t0, t1, "Sub", f"{{\\pos(960,{ybot + 48:.0f})\\fad(0,120)}}" + B.ass_reveal(T["sub"], clock + 150, 22, 280, 10)))
        if T.get("script"):
            events.append(ev(3, t0, t1, "Script", f"{{\\pos(960,{ybot + 60:.0f})\\c{P2.PS}\\fad(0,120)}}" + B.ass_reveal(T["script"], clock + 200, 16, 260, 8)))
        events.append(ev(3, t0, t1, "Mark", "{\\fad(200,120)}YTD"))
        sfx.append({"name": "whoosh_soft", "at": t0, "db": -17, "lead": 0.2})

    # ---- steps recap (unchanged)
    s0, s1, names = P2.STEPS
    t0, t1 = m(s0), m(s1)
    plates.append({"t0": t0, "t1": t1})
    hide.append((t0, t1))
    for i, (x, name) in enumerate(zip([460, 960, 1460], names)):
        d = 150 + i * 420
        events.append(ev(3, t0, t1, "Big", f"{{\\pos({x},470)\\fs120\\fad(0,120)}}" + B.ass_reveal(f"0{i + 1}", d, 60, 300, 14, PU)))
        events.append(ev(3, t0, t1, "Sub", f"{{\\pos({x},590)\\fs40\\fad(0,120)}}" + B.ass_reveal(name, d + 160, 30, 280, 10)))
        if i < 2:
            events.append(ev(3, t0, t1, "Box", B.ass_underline(x + 110, x + 390, 468, d + 260, 380, 4)))
    events.append(ev(3, t0, t1, "Mark", "{\\fad(200,120)}YTD"))
    sfx.append({"name": "whoosh_soft", "at": t0, "db": -17, "lead": 0.2})

    # ---- results on the plate
    for name, a, b, mw, mh, tilt in PLATE_CARDS:
        t0, t1 = m(a), m(b)
        p, ph = C2.card(name, mw, mh, tilt)
        plates.append({"t0": t0, "t1": t1})
        elements.append({"type": "card", "img": p, "hl_img": ph, "t0": t0, "t1": t1, "cx": 960, "cy": 500, "hl_delay": 0.55})
        sfx.append({"name": "whoosh", "at": t0, "db": -16, "lead": 0.12})
        sfx.append({"name": "hit_soft", "at": t0 + 0.02, "db": -12})
    # ---- results / photos popping up beside him, landing with a thud
    for name, a, b, cx, cy, rot, mw, mh in STICKERS:
        t0, t1 = m(a), m(b)
        elements.append({"type": "card", "img": C2.sticker(name, mw, mh, rot), "t0": t0, "t1": t1, "cx": cx, "cy": cy, "anim": "sticker"})
        sfx.append({"name": "hit_soft", "at": t0 + 0.06, "db": -10})
        sfx.append({"name": "whoosh", "at": t0, "db": -19, "lead": 0.1})
    audio_inserts = []
    for fn, a, b, cin, mode, adb in CLIPS:
        t0, t1 = m(a), m(b)
        if mode == "plate":
            plates.append({"t0": t0, "t1": t1})
            elements.append({"type": "clip", "file": f"{CLIPDIR}/{fn}", "in": cin, "t0": t0, "t1": t1, "h": 860, "cx": 960, "cy": 500})
        else:
            elements.append({"type": "clip", "file": f"{CLIPDIR}/{fn}", "in": cin, "t0": t0, "t1": t1, "h": 620, "cx": 1470, "cy": 470, "anim": "sticker"})
            sfx.append({"name": "hit_soft", "at": t0 + 0.06, "db": -12})
        if adb is not None:
            audio_inserts.append({"file": f"{CLIPDIR}/{fn}", "at": t0, "dur": t1 - t0, "in": cin, "audio_db": adb})
        sfx.append({"name": "whoosh", "at": t0, "db": -16, "lead": 0.12})
    for a, b, text in P2.LABELS:
        events.append(ev(2, m(a), m(b), "Label", "{\\fad(160,160)}" + text.replace("↓", "{\\fnInter Display}↓{\\fnUnbounded SemiBold}")))

    # ---- plain subtitles: phrase chunks, up to two balanced lines, no colour, no animation
    raw_titles = [(T["t0"], T["t1"]) for T in P2.TITLES] + [(P2.STEPS[0], P2.STEPS[1])]

    def in_title(x):
        return any(a <= x < b for a, b in raw_titles)

    def in_screen(x):
        return any(a <= x < b for a, b in SCREEN)

    groups, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        txt = " ".join(x["w"] for x in cur)
        gap = (nxt["s"] - w["e"]) if nxt else 9
        sent_end = w["w"][-1] in ".?!"
        comma = w["w"][-1] in ",;:"
        on_screen = any(a <= w["s"] <= b for a, b in SCREEN)
        limit = 50 if on_screen else 64
        boundary = nxt is not None and (in_title(w["s"]) != in_title(nxt["s"]) or in_screen(w["s"]) != in_screen(nxt["s"]))
        if not nxt or boundary or sent_end or gap > 0.5 or (comma and len(txt) > 22) or len(txt) > limit:
            groups.append(cur)
            cur = []
    for gi, g in enumerate(groups):
        c0 = m(g[0]["s"])
        c1 = m(groups[gi + 1][0]["s"]) if gi + 1 < len(groups) else m(g[-1]["e"]) + 0.4
        if c1 - m(g[-1]["e"]) > 0.7:
            c1 = m(g[-1]["e"]) + 0.35
        mid = (c0 + min(c1, m(g[-1]["e"]))) / 2
        if any(a - 0.05 <= mid <= b + 0.05 for a, b in hide):
            continue
        for a, b in hide:
            if c0 < a < c1:
                c1 = a
            if c0 < b < c1 and a <= c0:
                c0 = b
        text = " ".join(w["w"] for w in g)
        text = re.sub(r"\s+([,.?!])", r"\1", text).strip()
        text = re.sub(r"[,;:]$", "", text)
        text = re.sub(r"\bi\b", "I", text)
        on_screen = in_screen(g[0]["s"])
        style = "CapS" if on_screen else "Cap"
        # keep a subtitle inside its own region: clip it at the screen-share edges (output time)
        for a, b in SCREEN:
            if not on_screen and c0 < m(a) < c1:
                c1 = m(a)
            if on_screen and c0 < m(b) < c1:
                c1 = m(b)
        events.append(ev(1, c0, c1, style, wrap2(text, 26 if on_screen else 34)))
    events.append(ev(9, total - 0.6, total + 0.1, "Box", "{\\an7\\pos(0,0)\\c&H000000&\\fad(550,0)}{\\p1}m 0 0 l 1920 0 1920 1080 0 1080{\\p0}"))

    os.makedirs(outdir, exist_ok=True)
    open(f"{outdir}/text.ass", "w").write(SUBS + "\n".join(events) + "\n")
    json.dump({"plates": plates, "elements": elements}, open(f"{outdir}/elements.json", "w"), indent=1)
    edl = {"items": [{"kind": "aroll", "in": a, "out": b} for a, b in keep], "sfx": sfx, "inserts": audio_inserts,
           "music": [], "duck_db": 4, "total": total, "keep": keep}
    json.dump(edl, open(f"{outdir}/edl3.json", "w"), indent=1)
    caps = sum(1 for e in events if ",Cap" in e)
    print(f"{total:.1f}s; plate cards {len(PLATE_CARDS)}, pop-ups {len(STICKERS)}, clips {len(CLIPS)}, subtitles {caps}, sfx {len(sfx)}")


if __name__ == "__main__":
    main()
