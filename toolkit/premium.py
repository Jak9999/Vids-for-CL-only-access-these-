"""Premium Teacher Jak Reel: animated background, glass cards, kinetic type, band meter, motion blur, grain."""
import os, sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H, FPS = 1080, 1920, 30
FD = "/usr/share/fonts/truetype/google-fonts/"
_F = {}
def F(w, s):
    k = (w, s)
    if k not in _F: _F[k] = ImageFont.truetype(FD + f"Poppins-{w}.ttf", s)
    return _F[k]

LAV = (206, 203, 246); LAV_L = (238, 237, 254); WHITE = (255, 255, 255); DARK = (38, 33, 92)
RED_D = (232, 84, 84); RED = (245, 140, 140); GRN = (93, 202, 165); GRN_D = (4, 52, 44)
AMB = (250, 199, 117); AMB_D = (65, 36, 2)

def clamp(x): return max(0.0, min(1.0, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def back(x): x = clamp(x); c = 1.7; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def spring(x): x = clamp(x); return 1 - math.exp(-6 * x) * math.cos(10 * x)
def prog(t, a, d): return clamp((t - a) / d)
def mix(a, b, k): return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))

def fade(spr, a):
    if a >= 0.999: return spr
    s = spr.copy(); s.putalpha(s.getchannel("A").point(lambda p: int(p * max(0, a)))); return s
def scaled(spr, s):
    if abs(s - 1) < 0.003: return spr
    return spr.resize((max(1, int(spr.width * s)), max(1, int(spr.height * s))), Image.BICUBIC)
def put(im, spr, cx, cy, alpha=1.0, scale=1.0):
    if alpha <= 0.01 or scale <= 0.02: return
    s = fade(scaled(spr, scale), alpha)
    im.paste(s, (int(cx - s.width / 2), int(cy - s.height / 2)), s)

# ---------- background ----------
yy = np.linspace(0, 1, H)[:, None]
_top = np.array([24, 19, 66.0]); _bot = np.array([48, 37, 118.0])
BG = Image.fromarray(np.ascontiguousarray(np.broadcast_to((_top + (_bot - _top) * yy)[:, None, :], (H, W, 3))).astype(np.uint8))
def blob(color, size, a):
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).ellipse((size * .22, size * .22, size * .78, size * .78), fill=int(255 * a))
    m = m.filter(ImageFilter.GaussianBlur(size * .13))
    im = Image.new("RGBA", (size, size), color + (0,)); im.putalpha(m); return im
BLOBS = [(blob((127, 119, 221), 1100, .55), 230, 420, 240, 160, .045, 0.0),
         (blob((212, 83, 126), 950, .28), 860, 1250, 200, 240, .035, 1.7),
         (blob((29, 158, 117), 850, .20), 280, 1650, 180, 130, .03, 3.1),
         (blob((127, 119, 221), 800, .30), 900, 300, 150, 200, .04, 4.4)]
rng = np.random.default_rng(3)
PARTS = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(15, 45), rng.uniform(1.5, 4.5), rng.uniform(0, 6.28), rng.uniform(.25, .7)) for _ in range(46)]
vm = np.zeros((H, W), np.float32)
yv, xv = np.mgrid[0:H, 0:W]
r = np.sqrt(((xv - W / 2) / (W * .62)) ** 2 + ((yv - H / 2) / (H * .62)) ** 2)
VIG = Image.new("RGBA", (W, H), (8, 5, 25, 0)); VIG.putalpha(Image.fromarray((np.clip(r - 0.55, 0, 1) * 330).clip(0, 150).astype(np.uint8)))
del yv, xv, r
GRAIN = []
for i in range(6):
    n = rng.integers(0, 256, (H // 2, W // 2), dtype=np.uint8)
    g = Image.fromarray(n).resize((W, H), Image.NEAREST)
    GRAIN.append(Image.merge("RGBA", (g, g, g, Image.new("L", (W, H), 11))))

def background(gt):
    im = BG.copy()
    for spr, bx, by, ax, ay, sp, ph in BLOBS:
        cx = bx + ax * math.sin(gt * sp * 6.28 + ph); cy = by + ay * math.cos(gt * sp * 5.1 + ph)
        im.paste(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)), spr)
    d = ImageDraw.Draw(im)
    for x0, y0, spd, sz, ph, br in PARTS:
        y = (y0 - spd * gt) % (H + 40) - 20; x = x0 + 18 * math.sin(gt * .6 + ph)
        tw = 0.6 + 0.4 * math.sin(gt * 2 + ph)
        c = mix((48, 40, 115), LAV_L, br * tw)
        d.ellipse((x - sz, y - sz, x + sz, y + sz), fill=c)
    im.paste(VIG, (0, 0), VIG)
    return im

# ---------- sprites ----------
_T = {}
def tspr(txt, font, color, shadow=True):
    k = (txt, font.path, font.size, color, shadow)
    if k in _T: return _T[k]
    bb = font.getbbox(txt); tw, th = bb[2] - bb[0], bb[3] - bb[1]; p = 40
    lay = Image.new("RGBA", (tw + 2 * p, th + 2 * p), (0, 0, 0, 0))
    if shadow:
        m = Image.new("L", lay.size, 0)
        ImageDraw.Draw(m).text((p - bb[0], p - bb[1] + 6), txt, font=font, fill=140)
        m = m.filter(ImageFilter.GaussianBlur(9))
        sh = Image.new("RGBA", lay.size, (8, 5, 30, 0)); sh.putalpha(m); lay.alpha_composite(sh)
    t = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    ImageDraw.Draw(t).text((p - bb[0], p - bb[1]), txt, font=font, fill=color + (255,))
    lay.alpha_composite(t); _T[k] = lay; return lay

_G = {}
def gspr(w, h, tint=WHITE, fa=0.11, ba=0.42, r=44):
    k = (w, h, tint, fa, ba, r)
    if k in _G: return _G[k]
    p = 50; size = (w + 2 * p, h + 2 * p)
    card = Image.new("L", size, 0); ImageDraw.Draw(card).rounded_rectangle((p, p, p + w, p + h), r, fill=255)
    sh = Image.new("L", size, 0); ImageDraw.Draw(sh).rounded_rectangle((p + 6, p + 18, p + w - 6, p + h + 18), r, fill=120)
    sh = ImageChops.subtract(sh.filter(ImageFilter.GaussianBlur(20)), card)
    im = Image.new("RGBA", size, (6, 4, 24, 0)); im.putalpha(sh)
    lay = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((p, p, p + w, p + h), r, fill=tint + (int(255 * fa),), outline=(255, 255, 255, int(255 * ba)), width=3)
    d.line((p + r, p + 5, p + w - r, p + 5), fill=(255, 255, 255, int(255 * min(1, ba + .2))), width=2)
    im.alpha_composite(lay); _G[k] = im; return im

def pill_spr(txt, fill, tc):
    k = ("pill", txt, fill)
    if k in _T: return _T[k]
    f = F("Bold", 40); pw = int(f.getlength(txt)) + 90; ph = 86
    im = Image.new("RGBA", (pw + 40, ph + 40), (0, 0, 0, 0))
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((20, 28, 20 + pw, 28 + ph), 43, fill=110)
    sh = Image.new("RGBA", im.size, (8, 5, 30, 0)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(10))); im.alpha_composite(sh)
    d = ImageDraw.Draw(im); d.rounded_rectangle((20, 20, 20 + pw, 20 + ph), 43, fill=fill + (255,))
    d.text((20 + pw / 2, 20 + ph / 2), txt, font=f, fill=tc + (255,), anchor="mm"); _T[k] = im; return im

AV = {k: Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", f"avatar_{k}.png")).convert("RGBA") for k in ("smile", "wink")}
_AV = {}
def av_spr(which, d):
    k = (which, int(d))
    if k not in _AV: _AV[k] = AV[which].resize((int(d), int(d)), Image.LANCZOS)
    return _AV[k]
GLOW = blob((180, 172, 250), 900, .9)
def avatar(im, cx, cy, d, which="smile", alpha=1.0, gt=0, glow=True):
    if d < 6 or alpha <= 0: return
    if glow:
        put(im, GLOW, cx, cy, alpha * (0.55 + 0.15 * math.sin(gt * 3)), d / 520)
    put(im, av_spr(which, d), cx, cy, alpha)

def sparkle(im, cx, cy, k, color=LAV_L, n=5, rad=120):
    if k <= 0 or k >= 1: return
    d = ImageDraw.Draw(im)
    for i in range(n):
        a = i * 6.28 / n + 0.4; rr = rad * (0.4 + 0.8 * ease(k))
        x = cx + rr * math.cos(a); y = cy + rr * math.sin(a); s = 16 * (1 - k) * (1 + .4 * (i % 2))
        if s < 1: continue
        d.polygon([(x, y - s), (x + s * .28, y - s * .28), (x + s, y), (x + s * .28, y + s * .28), (x, y + s), (x - s * .28, y + s * .28), (x - s, y), (x - s * .28, y - s * .28)], fill=color)

def icon(im, kind, cx, cy, k):
    if k <= 0: return
    put(im, GLOW, cx, cy, 0.6 * clamp(k), 0.25)
    r = int(64 * k); d = ImageDraw.Draw(im)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=RED_D if kind == "x" else GRN)
    if k > 0.5:
        if kind == "x":
            q = int(24 * k); d.line((cx - q, cy - q, cx + q, cy + q), fill=WHITE, width=13); d.line((cx - q, cy + q, cx + q, cy - q), fill=WHITE, width=13)
        else:
            d.line((cx - 28, cy + 2, cx - 7, cy + 24, cx + 31, cy - 22), fill=DARK, width=13, joint="curve")

def kinetic(im, words, cy, font, colors, t, t0, stagger=0.13, dur=0.45):
    widths = [font.getlength(w) for w in words]; gap = font.getlength(" ")
    x = W / 2 - (sum(widths) + gap * (len(words) - 1)) / 2
    for i, w in enumerate(words):
        k = prog(t, t0 + i * stagger, dur)
        if k > 0:
            s = 1.7 - 0.7 * spring(k)
            put(im, tspr(w, font, colors[i % len(colors)]), x + widths[i] / 2, cy + (1 - ease(k)) * 30, ease(k * 1.6), s)
        x += widths[i] + gap

def meter(im, cy, value, alpha):
    if alpha <= 0: return
    put(im, gspr(860, 170), W / 2, cy, alpha)
    put(im, tspr("Your band", F("Medium", 38), LAV, False), 280, cy - 34, alpha)
    col = mix(AMB, GRN, clamp((value - 5.5) / 2))
    put(im, tspr(f"{value:.1f}", F("Bold", 50), col, False), 800, cy - 36, alpha)
    lay = Image.new("RGBA", (W, 60), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    x0, x1 = 160, 920; y = 30
    d.rounded_rectangle((x0, y - 9, x1, y + 9), 9, fill=(255, 255, 255, 50))
    fx = x0 + (x1 - x0) * clamp((value - 4) / 5)
    d.rounded_rectangle((x0, y - 9, max(x0 + 18, fx), y + 9), 9, fill=col + (255,))
    d.ellipse((fx - 15, y - 15, fx + 15, y + 15), fill=(255, 255, 255, 255))
    put(im, lay, W / 2, cy + 38, alpha)

BADGE = (150, 210, 170)
def badge(im, t, gt, pop=False, shake=None):
    s = back(prog(t, 0, .45)) if pop else 1.0
    dx = 0
    if shake is not None and shake <= t < shake + .5: dx = 12 * math.sin((t - shake) * 45) * (1 - (t - shake) / .5)
    avatar(im, BADGE[0] + dx, BADGE[1], BADGE[2] * max(.01, s), "smile", clamp(s), gt, glow=False)

def progress(im, gt, total):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 66, W - 60, 76), 5, fill=(80, 72, 150))
    d.rounded_rectangle((60, 66, 60 + int((W - 120) * clamp(gt / total)), 76), 5, fill=LAV_L)

# ---------- scenes ----------
VI = "“very important”"
def s_intro(im, t, gt):
    a = back(prog(t, 0, .6)); avatar(im, W / 2, 420, 330 * max(.01, a), "smile", clamp(a), gt)
    n = ease(prog(t, .3, .4)); put(im, tspr("Teacher Jak", F("Bold", 46), LAV_L), W / 2, 640 + (1 - n) * 20, n)
    p = prog(t, .25, .5); put(im, pill_spr("Vocabulary upgrade", AMB, AMB_D), W / 2, 765, ease(p * 2), 0.6 + 0.4 * spring(p))
    kinetic(im, ["Stop", "saying"], 930, F("Bold", 110), [WHITE], t, .55)
    k = prog(t, 1.0, .55)
    if k > 0:
        s = .7 + .3 * spring(k); put(im, gspr(840, 190), W / 2, 1100, ease(k * 2), s)
        put(im, tspr(VI, F("Bold", 92), AMB), W / 2, 1095, ease(k * 2), s)
    put(im, tspr("Try these for a higher band", F("Regular", 46), LAV), W / 2, 1265, ease(prog(t, 1.6, .5)))
def s_wrong(im, t, gt):
    badge(im, t, gt, pop=True, shake=1.2)
    k = prog(t, .05, .55); dx = 14 * math.sin((t - 1.2) * 45) * (1 - (t - 1.2) / .5) if 1.2 <= t < 1.7 else 0
    s = .7 + .3 * spring(k)
    put(im, gspr(880, 270), W / 2 + dx, 930, ease(k * 2), s)
    f = F("Bold", 100); tw = f.getlength(VI)
    put(im, tspr(VI, f, WHITE), W / 2 + dx, 925, ease(k * 2), s)
    st = ease(prog(t, .85, .4))
    if st > 0:
        x0 = W / 2 - tw / 2 - 20 + dx; ImageDraw.Draw(im).rounded_rectangle((x0, 918, x0 + (tw + 40) * st, 940), 11, fill=RED_D)
    icon(im, "x", W // 2, 700, back(prog(t, 1.2, .4)))
    put(im, tspr("Too basic", F("Bold", 58), RED), W / 2, 1130, ease(prog(t, 1.4, .4)))
    meter(im, 1400, 5.5, ease(prog(t, 1.6, .5)))
UP = ["crucial", "essential", "vital"]
def s_up(im, t, gt):
    badge(im, t, gt)
    kinetic(im, ["Say", "this", "instead"], 600, F("Bold", 82), [WHITE, WHITE, LAV], t, .05)
    val = 5.5
    for i, w in enumerate(UP):
        st = .45 + i * .55; k = prog(t, st, .6)
        if k > 0:
            x = W / 2 + (1 - spring(k)) * 750; cy = 790 + i * 175
            put(im, gspr(760, 140), x, cy, ease(k * 2))
            ImageDraw.Draw(im).ellipse((x - 320, cy - 11, x - 298, cy + 11), fill=AMB)
            put(im, tspr(w, F("Bold", 80), WHITE), x, cy - 4, ease(k * 2))
            sparkle(im, x + 300, cy, prog(t, st + .25, .6), AMB, rad=90)
            val += 0.7 * ease(prog(t, st + .2, .45))
    meter(im, 1400, val, 1.0)
SENT = "Sleep is essential."
def s_ex(im, t, gt):
    badge(im, t, gt)
    put(im, pill_spr("Example", GRN, GRN_D), W / 2, 640, ease(prog(t, .05, .4)), .6 + .4 * spring(prog(t, .05, .5)))
    k = prog(t, .15, .5); put(im, gspr(920, 240, tint=GRN, fa=.16, ba=.5), W / 2, 880, ease(k * 2), .8 + .2 * spring(k))
    f = F("Bold", 84); full = f.getlength(SENT); x0 = W / 2 - full / 2
    n = int(clamp((t - .5) * 16 / len(SENT) * len(SENT) / len(SENT) * 1.0) * 0 + max(0, min(len(SENT), int((t - .5) * 16))))
    d = ImageDraw.Draw(im)
    hi = ease(prog(t, 1.75, .45))
    if hi > 0:
        a = x0 + f.getlength("Sleep is "); b = a + f.getlength("essential")
        lay = Image.new("RGBA", (W, 120), (0, 0, 0, 0))
        ImageDraw.Draw(lay).rounded_rectangle((a - 12, 30, a - 12 + (b - a + 24) * hi, 100), 16, fill=AMB + (175,))
        im.paste(lay, (0, 806), lay)
    if n > 0:
        sub = SENT[:n]
        d.text((x0 + 2, 832 + 6), sub, font=f, fill=(14, 10, 40), anchor="lm") if False else None
        put_left = tspr(sub, f, WHITE)
        im.paste(put_left, (int(x0 - 40), int(875 - put_left.height / 2)), put_left)
    if n < len(SENT) or (t * 2) % 1 < .5:
        cx = x0 + f.getlength(SENT[:n]) + 8
        d.rounded_rectangle((cx, 838, cx + 7, 912), 3, fill=LAV_L)
    icon(im, "check", W // 2 + 440, 770, back(prog(t, 1.9, .4)))
    sparkle(im, W // 2 + 440, 770, prog(t, 2.0, .6), GRN, rad=110)
    put(im, tspr("Same meaning, stronger word.", F("Medium", 52), WHITE), W / 2, 1100 + (1 - ease(prog(t, 2.1, .4))) * 25, ease(prog(t, 2.1, .4)))
    put(im, tspr("Perfect for IELTS Writing and Speaking.", F("Medium", 46), LAV), W / 2, 1180 + (1 - ease(prog(t, 2.35, .4))) * 25, ease(prog(t, 2.35, .4)))
    meter(im, 1400, 7.6, 1.0)
def s_out(im, t, gt):
    a = back(prog(t, 0, .6)); which = "wink" if 1.5 <= t < 2.4 else "smile"
    bump = 1 + (.07 * math.sin(clamp((t - 1.5) / .25) * math.pi) if 1.5 <= t < 1.75 else 0)
    avatar(im, W / 2, 470, 420 * max(.01, a) * bump, which, clamp(a), gt)
    sparkle(im, W / 2 + 150, 380, prog(t, 1.5, .7), LAV_L, n=6, rad=80)
    kinetic(im, ["Save", "this"], 820, F("Bold", 124), [WHITE], t, .15, .15, .5)
    put(im, tspr("for your IELTS exam", F("Regular", 50), LAV), W / 2, 935, ease(prog(t, .6, .45)))
    k = prog(t, 1.0, .55)
    if k > 0:
        s = .8 + .2 * spring(k); put(im, gspr(860, 160, tint=LAV_L, fa=.96, ba=.0), W / 2, 1110, ease(k * 2), s)
        put(im, tspr("Follow for a daily English fix", F("Bold", 54), DARK, False), W / 2, 1106, ease(k * 2), s)
    put(im, tspr("@ieltswithteacherjak", F("Medium", 44), LAV), W / 2, 1265, ease(prog(t, 1.35, .4)))

SCENES = [(s_intro, 3.2, False, [(.05, "hello")] + [(.55 + i * .13, "tick") for i in range(2)]),
          (s_wrong, 3.0, True, [(.85, "swish"), (1.2, "wrong")]),
          (s_up, 4.4, True, [(.45 + i * .55, "tick") for i in range(3)]),
          (s_ex, 3.8, True, [(.5 + i / 16, "tick") for i in range(0, len(SENT), 3)] + [(1.9, "right")]),
          (s_out, 3.8, False, [(1.5, "wink")])]
STARTS = np.cumsum([0] + [s[1] for s in SCENES])[:-1]; TOTAL = sum(s[1] for s in SCENES)

def frame(idx, t):
    fn, dur, uses, _ = SCENES[idx]; gt = STARTS[idx] + t
    im = background(gt); fn(im, t, gt)
    z = 1 + 0.025 * t / dur
    endk = prog(t, dur - .35, .35) if idx < len(SCENES) - 1 else 0
    z += 0.10 * ease(endk) ** 2
    if z > 1.001:
        cw, ch = W / z, H / z; im = im.crop((int((W - cw) / 2), int((H - ch) / 2), int((W + cw) / 2), int((H + ch) / 2))).resize((W, H), Image.BILINEAR)
    if endk > 0:
        tgt = background(gt)
        if uses and SCENES[idx + 1][2]: badge(tgt, 0, gt)
        im = Image.blend(im, tgt, ease(endk))
    return im

def finish(im, prev, gt, i):
    arr = np.asarray(im, dtype=np.float32)
    if prev is not None: arr = arr * .62 + prev * .38
    out = Image.fromarray(arr.astype(np.uint8))
    g = GRAIN[i % len(GRAIN)]; out.paste(g, (0, 0), g)
    progress(out, gt, TOTAL); return out, arr

def render(idx, outdir):
    dur = SCENES[idx][1]; n = int(round(dur * FPS)); tmp = f"{outdir}/p{idx}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    prev = None
    for i in range(n):
        t = i / FPS; out, prev = finish(frame(idx, t), prev, STARTS[idx] + t, i); p.stdin.write(out.tobytes())
    p.stdin.close()
    if p.wait() == 0: os.rename(tmp, f"{outdir}/p{idx}.mp4")

if __name__ == "__main__":
    out = "/home/claude/reel/premium"; os.makedirs(out, exist_ok=True)
    if sys.argv[1] == "stills":
        ims = []
        for i, (fn, dur, _, _) in enumerate(SCENES):
            for t in (dur * .55, dur - .45):
                o, _ = finish(frame(i, t), None, STARTS[i] + t, 0); ims.append(o.resize((216, 384)))
        c = Image.new("RGB", (216 * 5, 384 * 2))
        for k, im in enumerate(ims): c.paste(im, ((k // 2) * 216, (k % 2) * 384))
        c.save(f"{out}/contact.png")
        frame(2, 3.6).save(f"{out}/full_s2.png"); frame(3, 3.0).save(f"{out}/full_s3.png")
    elif sys.argv[1] == "final":
        sys.path.insert(0, "/home/claude/reel"); import music_kit
        ev = []
        for i, s in enumerate(SCENES):
            if i: ev.append((STARTS[i], "swish"))
            ev += [(STARTS[i] + a, k) for a, k in s[3] if k != "swish"]
        music_kit.make(ev, TOTAL, f"{out}/music.wav")
        open(f"{out}/list.txt", "w").write("".join(f"file 'p{i}.mp4'\n" for i in range(len(SCENES))))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{out}/list.txt", "-c", "copy", f"{out}/v.mp4"], check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{out}/v.mp4", "-i", f"{out}/music.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-af", "acompressor=threshold=-22dB:ratio=2.5:attack=10:release=150:makeup=3,alimiter=limit=0.8:level=disabled,volume=-1.5dB",
                        "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", f"{out}/very_important_premium.mp4"], check=True)
    else:
        render(int(sys.argv[1]), out)
