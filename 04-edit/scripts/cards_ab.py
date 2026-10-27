"""AB Nasdaq-style cards: clean Apple-keynote look. Screenshots get rounded corners, a hairline border and a soft
shadow (for light-grey or white plates); photos beside Ricky get a thin white frame and a soft shadow."""
import os, sys
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, "/home/user/work/scripts")
import cards2 as C2

OUT = "/home/user/work/gfx/ab"
os.makedirs(OUT, exist_ok=True)


def fit(im, max_w, max_h):
    s = min(max_w / im.width, max_h / im.height)
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)


def shadowed(im, radius, pad=70, blur=26, alpha=70, frame=0, frame_rgb=(255, 255, 255), hairline=None):
    w, h = im.width + 2 * frame, im.height + 2 * frame
    card = Image.new("RGBA", (w, h), frame_rgb + (255,))
    card.paste(im, (frame, frame))
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius, fill=255)
    card.putalpha(m)
    if hairline:
        ImageDraw.Draw(card).rounded_rectangle((0, 0, w - 1, h - 1), radius, outline=hairline, width=2)
    out = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("L", out.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle((pad, pad + 14, pad + w, pad + h + 14), radius, fill=alpha)
    out.putalpha(sh.filter(ImageFilter.GaussianBlur(blur)))
    out.alpha_composite(card, (pad, pad))
    return out


def proof(name, max_w=1250, max_h=780):
    """Screenshot as a clean card for a light-grey plate."""
    p = f"{OUT}/proof_{name}_{max_w}x{max_h}.png"
    if not os.path.exists(p):
        im, _ = C2.source(name)
        shadowed(fit(im.convert("RGB"), max_w, max_h), 28, hairline=(0, 0, 0, 28)).save(p)
    return p


def photo(name, max_w=560, max_h=600):
    """Photo / screenshot beside Ricky: thin white frame, soft shadow."""
    p = f"{OUT}/photo_{name}_{max_w}x{max_h}.png"
    if not os.path.exists(p):
        im, _ = C2.source(name)
        shadowed(fit(im.convert("RGB"), max_w - 16, max_h - 16), 14, frame=8, alpha=120, blur=22).save(p)
    return p


def behind_text(text, size=172, cy=205, font="/usr/share/fonts/opentype/inter/InterDisplay-Black.otf", tracking=-6):
    """Full-frame text layer for the text-behind-him effect: giant white caps with a soft dark shadow."""
    from PIL import ImageFont
    p = f"{OUT}/behind_{text.replace(' ', '_')}_{size}.png"
    if os.path.exists(p):
        return p
    f = ImageFont.truetype(font, size)
    widths = [f.getlength(c) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    layer = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    sh = Image.new("L", (1920, 1080), 0)
    x = 960 - total / 2
    asc, desc = f.getmetrics()
    y = cy - (asc + desc) / 2
    d, ds = ImageDraw.Draw(layer), ImageDraw.Draw(sh)
    for c, w in zip(text, widths):
        d.text((x, y), c, font=f, fill=(255, 255, 255, 255))
        ds.text((x, y + 6), c, font=f, fill=150)
        x += w + tracking
    out = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    out.putalpha(sh.filter(ImageFilter.GaussianBlur(16)))
    out.alpha_composite(layer)
    out.save(p)
    return p
