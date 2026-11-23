"""Teacher Jak Reel template: purple brand, avatar intro/badge/wink outro, scene builders."""
import subprocess, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
FD = "/usr/share/fonts/truetype/google-fonts/"
_FC = {}
def F(w, s):
    k = (w, s)
    if k not in _FC: _FC[k] = ImageFont.truetype(FD + f"Poppins-{w}.ttf", s)
    return _FC[k]

BG = (38, 33, 92); BG2 = (48, 42, 112); CARD = (60, 52, 137)
LAV = (206, 203, 246); LAV_L = (238, 237, 254)
RED = (240, 149, 149); RED_D = (226, 75, 74)
GRN = (93, 202, 165); GRN_L = (225, 245, 238); GRN_D = (4, 52, 44)
WHITE = (255, 255, 255)
# accent pills per format (fill, text)
ACCENTS = {
    "mistake": (LAV_L, BG),
    "vocab": ((250, 199, 117), (65, 36, 2)),
    "quiz": ((159, 225, 203), (4, 52, 44)),
    "speaking": ((244, 192, 209), (75, 21, 40)),
}

def clamp(x): return max(0.0, min(1.0, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def back(x): x = clamp(x); c = 1.6; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def prog(t, a, d): return clamp((t - a) / d)

_BASE = None
def base():
    global _BASE
    if _BASE is None:
        im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
        d.ellipse((-260, -200, 420, 480), fill=BG2); d.ellipse((760, 1500, 1400, 2140), fill=BG2)
        _BASE = im
    return _BASE.copy()

def fit(text, weight, size, maxw):
    while size > 28 and F(weight, size).getlength(text) > maxw: size -= 2
    return F(weight, size)

def text_layer(im, txt, font, color, cx, cy, alpha=1.0, dy=0, scale=1.0):
    if alpha <= 0: return
    bb = font.getbbox(txt); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    lay = Image.new("RGBA", (tw + 40, th + 40), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((20 - bb[0], 20 - bb[1]), txt, font=font, fill=color + (255,))
    if scale != 1.0:
        lay = lay.resize((max(1, int(lay.width * scale)), max(1, int(lay.height * scale))), Image.LANCZOS)
    if alpha < 1: lay.putalpha(lay.split()[3].point(lambda p: int(p * alpha)))
    im.paste(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2 + dy)), lay)
    return tw * scale

def pill(im, txt, cy, alpha, accent="mistake"):
    if alpha <= 0: return
    fill, tc = ACCENTS[accent]; f = F("Medium", 40)
    pw = int(f.getlength(txt)) + 80; ph = 84
    lay = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((0, 0, pw - 1, ph - 1), radius=42, fill=fill + (255,))
    d.text((pw / 2, ph / 2), txt, font=f, fill=tc + (255,), anchor="mm")
    lay.putalpha(lay.split()[3].point(lambda p: int(p * alpha)))
    im.paste(lay, (int(W / 2 - pw / 2), int(cy - ph / 2)), lay)

def card(im, cy, h, color, alpha, scale=1.0, w=860):
    if alpha <= 0: return
    w = int(w * scale); hh = int(h * scale)
    if w < 2 or hh < 2: return
    lay = Image.new("RGBA", (w, hh), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle((0, 0, w - 1, hh - 1), radius=max(1, int(40 * scale)), fill=color + (int(255 * alpha),))
    im.paste(lay, (int(W / 2 - w / 2), int(cy - hh / 2)), lay)

def icon(im, kind, cx, cy, k):
    if k <= 0: return
    r = int(70 * k); d = ImageDraw.Draw(im)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=RED_D if kind == "x" else GRN)
    if k > 0.5:
        if kind == "x":
            q = int(26 * k)
            d.line((cx - q, cy - q, cx + q, cy + q), fill=WHITE, width=14)
            d.line((cx - q, cy + q, cx + q, cy - q), fill=WHITE, width=14)
        else:
            d.line((cx - 30, cy + 2, cx - 8, cy + 26, cx + 34, cy - 24), fill=BG, width=14, joint="curve")

def progress_bar(im, gt, total):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 70, W - 60, 80), radius=5, fill=(70, 64, 140))
    d.rounded_rectangle((60, 70, 60 + int((W - 120) * clamp(gt / total)), 80), radius=5, fill=LAV_L)

# ---------- avatar ----------
_AV = {k: Image.open(os.path.join(HERE, "assets", f"avatar_{k}.png")).convert("RGBA") for k in ("smile", "wink")}
_AVC = {}
def avatar(im, cx, cy, d, which="smile", alpha=1.0, rot=0):
    if d < 4 or alpha <= 0: return
    key = (which, int(d))
    if key not in _AVC: _AVC[key] = _AV[which].resize((int(d), int(d)), Image.LANCZOS)
    a = _AVC[key]
    if rot: a = a.rotate(rot, resample=Image.BICUBIC)
    if alpha < 1:
        a = a.copy(); a.putalpha(a.split()[3].point(lambda p: int(p * alpha)))
    im.paste(a, (int(cx - a.width / 2), int(cy - a.height / 2)), a)

BADGE = (150, 200, 170)
def badge(im, t=0, pop=False, shake_at=None):
    s = back(prog(t, 0.0, 0.45)) if pop else 1.0
    rot = 0
    if shake_at is not None and shake_at <= t < shake_at + 0.45:
        rot = 9 * math.sin((t - shake_at) * 40) * (1 - (t - shake_at) / 0.45)
    avatar(im, BADGE[0], BADGE[1], BADGE[2] * max(0.01, s), "smile", clamp(s), rot)

# ---------- scene builders ----------
# each returns (draw_fn(t, dur, first_badge), duration, sfx list [(t, kind)], uses_badge)
def intro(label, line1, line2, sub, accent="mistake", dur=2.8):
    def f(t, dur, fb):
        im = base()
        a0 = back(prog(t, 0.0, 0.55)); avatar(im, W / 2, 400, 330 * max(0.01, a0), "smile", clamp(a0))
        n0 = ease(prog(t, 0.3, 0.4)); text_layer(im, "Teacher Jak", F("Bold", 46), LAV_L, W / 2, 615, n0, dy=(1 - n0) * 20)
        pill(im, label, 740, ease(prog(t, 0.1, 0.4)), accent)
        a = ease(prog(t, 0.35, 0.5)); text_layer(im, line1, fit(line1, "Bold", 104, 940), WHITE, W / 2, 900, a, dy=(1 - a) * 60)
        b = ease(prog(t, 0.6, 0.5)); text_layer(im, line2, fit(line2, "Bold", 104, 940), LAV, W / 2, 1030, b, dy=(1 - b) * 60)
        c = ease(prog(t, 1.2, 0.4)); text_layer(im, sub, F("Regular", 46), LAV, W / 2, 1170, c)
        return im
    return (f, dur, [(0.05, "hello")], False)

def wrong(text, label="Wrong", dur=3.0):
    def f(t, dur, fb):
        im = base(); badge(im, t, pop=fb, shake_at=1.45)
        s = back(prog(t, 0.05, 0.5)); card(im, 960, 300, CARD, clamp(s), max(0.01, s))
        font = fit(text, "Bold", 110, 760)
        if s > 0.6: tw = text_layer(im, text, font, WHITE, W / 2, 955, ease(prog(t, 0.3, 0.3)))
        else: tw = font.getlength(text)
        k = ease(prog(t, 1.0, 0.45))
        if k > 0:
            x0 = W / 2 - tw / 2 - 20; x1 = x0 + (tw + 40) * k
            ImageDraw.Draw(im).rounded_rectangle((x0, 950, x1, 972), radius=11, fill=RED_D)
        icon(im, "x", W // 2, 700, back(prog(t, 1.45, 0.4)))
        text_layer(im, label, F("Medium", 56), RED, W / 2, 1200, ease(prog(t, 1.6, 0.4)))
        return im
    return (f, dur, [(1.45, "wrong")], True)

def right(text, e1, e2, dur=3.6):
    def f(t, dur, fb):
        im = base(); badge(im, t, pop=fb)
        s = back(prog(t, 0.05, 0.5)); card(im, 900, 300, GRN_L, clamp(s), max(0.01, s))
        if s > 0.6: text_layer(im, text, fit(text, "Bold", 120, 780), GRN_D, W / 2, 895, ease(prog(t, 0.3, 0.3)))
        icon(im, "check", W // 2, 640, back(prog(t, 0.6, 0.4)))
        a = ease(prog(t, 1.1, 0.45)); text_layer(im, e1, fit(e1, "Medium", 52, 940), WHITE, W / 2, 1140, a, dy=(1 - a) * 30)
        b = ease(prog(t, 1.4, 0.45)); text_layer(im, e2, fit(e2, "Medium", 52, 940), LAV, W / 2, 1220, b, dy=(1 - b) * 30)
        return im
    return (f, dur, [(0.6, "right")], True)

def items(title, lines, dur=3.6, big=False):
    def f(t, dur, fb):
        im = base(); badge(im, t, pop=fb)
        text_layer(im, title, fit(title, "Bold", 76, 940), WHITE, W / 2, 620, ease(prog(t, 0.05, 0.4)))
        for i, ln in enumerate(lines):
            a = ease(prog(t, 0.45 + i * 0.45, 0.45)); cy = 820 + i * 190
            if a > 0:
                card(im, cy + (1 - a) * 40, 150, CARD, a)
                text_layer(im, ln, fit(ln, "Bold" if big else "Medium", 76 if big else 60, 780), WHITE, W / 2, cy, a, dy=(1 - a) * 40)
        return im
    return (f, dur, [(0.45 + i * 0.45, "tick") for i in range(len(lines))], True)

def quiz(question, opts, dur=4.2):
    def f(t, dur, fb):
        im = base(); badge(im, t, pop=fb)
        text_layer(im, question, fit(question, "Bold", 72, 940), WHITE, W / 2, 600, ease(prog(t, 0.05, 0.4)))
        for i, o in enumerate(opts):
            a = ease(prog(t, 0.35 + i * 0.35, 0.4)); cy = 790 + i * 190
            if a > 0:
                card(im, cy, 150, CARD, a)
                text_layer(im, o, fit(o, "Medium", 54, 800), WHITE, W / 2, cy, a)
        for k, n in enumerate(("3", "2", "1")):
            st = 1.3 + k * 0.9
            if st <= t < st + 0.9:
                p = (t - st) / 0.9; sc = 1.25 - 0.25 * ease(p * 3)
                d = ImageDraw.Draw(im); r = 95
                d.ellipse((W / 2 - r, 1300 - r, W / 2 + r, 1300 + r), outline=LAV_L, width=8)
                d.arc((W / 2 - r, 1300 - r, W / 2 + r, 1300 + r), -90, -90 + 360 * (1 - p), fill=(159, 225, 203), width=8)
                text_layer(im, n, F("Bold", 110), WHITE, W / 2, 1300, 1.0, scale=sc)
        return im
    return (f, dur, [(1.3 + k * 0.9, "tick") for k in range(3)], True)

def quiz_reveal(question, opts, correct, e1, e2, dur=4.0):
    def f(t, dur, fb):
        im = base(); badge(im, t, pop=fb)
        text_layer(im, question, fit(question, "Bold", 72, 940), WHITE, W / 2, 600, 1.0)
        k = ease(prog(t, 0.15, 0.4))
        for i, o in enumerate(opts):
            cy = 790 + i * 190
            if i == correct:
                card(im, cy, 150, GRN_L, 1.0, scale=1 + 0.04 * math.sin(k * math.pi))
                text_layer(im, o, fit(o, "Bold", 54, 800), GRN_D, W / 2, cy, 1.0)
            else:
                card(im, cy, 150, CARD, 1 - 0.5 * k)
                tw = text_layer(im, o, fit(o, "Medium", 54, 800), WHITE, W / 2, cy, 1 - 0.5 * k)
                if k > 0:
                    x0 = W / 2 - tw / 2 - 10
                    ImageDraw.Draw(im).rounded_rectangle((x0, cy - 6, x0 + (tw + 20) * k, cy + 8), radius=7, fill=RED_D)
        icon(im, "check", W // 2, 790 + len(opts) * 190 - 40, back(prog(t, 0.3, 0.4)))
        a = ease(prog(t, 1.0, 0.45)); text_layer(im, e1, fit(e1, "Medium", 52, 940), WHITE, W / 2, 1270, a, dy=(1 - a) * 30)
        b = ease(prog(t, 1.3, 0.45)); text_layer(im, e2, fit(e2, "Medium", 52, 940), LAV, W / 2, 1350, b, dy=(1 - b) * 30)
        return im
    return (f, dur, [(0.15, "right")], True)

def outro(sub="for your next conversation", dur=3.4):
    def f(t, dur, fb):
        im = base()
        av = back(prog(t, 0.0, 0.55)); which = "wink" if 1.45 <= t < 2.35 else "smile"
        bump = 1.0 + (0.06 * math.sin(clamp((t - 1.45) / 0.25) * math.pi) if 1.45 <= t < 1.7 else 0)
        avatar(im, W / 2, 470, 400 * max(0.01, av) * bump, which, clamp(av))
        a = back(prog(t, 0.05, 0.5)); text_layer(im, "Save this", F("Bold", 120), WHITE, W / 2, 800, clamp(a), scale=max(0.01, 0.6 + 0.4 * a))
        b = ease(prog(t, 0.5, 0.45)); text_layer(im, sub, fit(sub, "Regular", 50, 940), LAV, W / 2, 920, b)
        c = ease(prog(t, 1.0, 0.45))
        if c > 0:
            card(im, 1110 + (1 - c) * 40, 170, LAV_L, c)
            text_layer(im, "Follow for a daily English fix", F("Bold", 52), BG, W / 2, 1110, c, dy=(1 - c) * 40)
        h = ease(prog(t, 1.3, 0.4)); text_layer(im, "@ieltswithteacherjak", F("Medium", 44), LAV, W / 2, 1260, h)
        return im
    return (f, dur, [(1.45, "wink")], False)

# ---------- rendering ----------
def timeline(scenes):
    starts, t = [], 0.0
    for s in scenes: starts.append(t); t += s[1]
    return starts, t

def frame(scenes, idx, t):
    starts, total = timeline(scenes)
    fn, dur, _, uses = scenes[idx]
    first_badge = uses and (idx == 0 or not scenes[idx - 1][3])
    im = fn(t, dur, first_badge)
    if idx < len(scenes) - 1:
        k = clamp((t - (dur - 0.3)) / 0.3)
        if k > 0:
            tgt = base()
            if uses and scenes[idx + 1][3]: badge(tgt)
            im = Image.blend(im, tgt, k)
    progress_bar(im, starts[idx] + t, total)
    return im

def render_scene(scenes, idx, outdir):
    fn, dur, _, _ = scenes[idx]; n = int(round(dur * FPS))
    tmp = os.path.join(outdir, f"scene{idx}.tmp.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                          "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(frame(scenes, idx, i / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.rename(tmp, os.path.join(outdir, f"scene{idx}.mp4"))

def sfx_events(scenes):
    starts, total = timeline(scenes); ev = []
    for i, s in enumerate(scenes):
        if i > 0: ev.append((starts[i], "swish"))
        ev += [(starts[i] + t, k) for t, k in s[2]]
    return ev, total
