"""Premium-style meme: home vs actual test, with the user's photo avatar."""
import os, sys, math
_src = open("/home/claude/reel/premium.py").read().split('if __name__ == "__main__":')[0]
exec(_src)

SWEAT = (140, 206, 255)
def eio(x): x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def tw(txt, f): return f.getlength(txt)

def left_text(im, txt, f, col, x0, cy, alpha=1.0):
    if not txt: return
    w = tw(txt, f); put(im, tspr(txt, f, col), x0 + w / 2, cy, alpha)

def sweat(im, cx, cy, d, t):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(lay)
    for k, (ox, oy, ph) in enumerate([(.5, -.3, 0), (-.52, -.1, .4), (.47, .16, .72), (-.4, .25, .2)]):
        f = (t * .8 + ph) % 1; a = int(255 * min(1, (1 - f) * 1.6))
        x = cx + ox * d; y = cy + oy * d + 120 * f; s = 34
        dr.polygon([(x, y - s * 1.5), (x + s * .78, y + s * .05), (x - s * .78, y + s * .05)], fill=SWEAT + (a,))
        dr.ellipse((x - s * .8, y - s * .65, x + s * .8, y + s * .95), fill=SWEAT + (a,))
        dr.ellipse((x - s * .35, y - s * .2, x - s * .05, y + s * .15), fill=(255, 255, 255, a))
    im.paste(lay, (0, 0), lay)

def card_lines(im, cy, w, lines, shown, f, col, alpha, lh=78, tint=WHITE, fa=.11):
    h = lh * len(lines) + 70
    put(im, gspr(w, h, tint=tint, fa=fa), W / 2, cy, alpha)
    x0 = W / 2 - w / 2 + 50; y0 = cy - (len(lines) - 1) * lh / 2
    for i, (ln, n) in enumerate(zip(lines, shown)):
        if n > 0: left_text(im, ln[:n], f, col, x0, y0 + i * lh, alpha)

HOME = ["Well, in my opinion,", "technology has completely", "transformed how we live!"]
def m_home(im, t, gt):
    p = ease(prog(t, 0, .3)); put(im, pill_spr("Me practising IELTS Speaking at home", (159, 225, 203), (4, 52, 44)), W / 2, 240, p, .7 + .3 * spring(prog(t, 0, .4)))
    a = back(prog(t, -.2, .6)); bob = 12 * math.sin(t * 6)
    avatar(im, W / 2, 520 + bob, 360 * max(.01, a), "smile", clamp(a), gt)
    for i in range(7):
        sparkle(im, W / 2, 520, ((t * .8 + i / 7) % 1), AMB if i % 2 else LAV_L, n=4, rad=120 + 15 * i)
    f = F("Bold", 56); total = sum(len(l) for l in HOME); n = int(clamp((t - .4) / 1.6) * total); shown = []
    for l in HOME: shown.append(min(len(l), n)); n = max(0, n - len(l))
    card_lines(im, 960, 920, HOME, shown, f, WHITE, ease(prog(t, .2, .3)))
    k = ease(prog(t, 2.2, .4)); kinetic(im, ["Fluent.", "Confident.", "Band", "9."], 1250, F("Bold", 64), [AMB], t, 2.2, .12, .4)
    if t > 4.0:
        fl = Image.new("RGB", (W, H), (255, 255, 255)); im.paste(Image.blend(im, fl, prog(t, 4.0, .2)))

TEST = ["Ehm…", "I think…", "it’s very… very important…"]
TT = [.7, 1.7, 2.7]
DARK_OV = Image.new("RGBA", (W, H), (6, 10, 30, 135))
def m_test(im, t, gt):
    im.paste(DARK_OV, (0, 0), DARK_OV)
    put(im, pill_spr("Me in the actual test", (245, 120, 160), (75, 21, 40)), W / 2, 240, ease(prog(t, 0, .3)))
    sh = 9 * math.sin(t * 38) * (.35 + .65 * prog(t, 1.2, 2)); z = 1 + .12 * eio(prog(t, 3.4, 1.4))
    d = 360 * z
    avatar(im, W / 2 + sh, 540, d, "smile", 1.0, gt, glow=False)
    sweat(im, W / 2 + sh, 540, d, t)
    f = F("Bold", 54); shown = [len(l) if t > TT[i] else 0 for i, l in enumerate(TEST)]
    card_lines(im, 960, 900, TEST, shown, f, LAV_L, ease(prog(t, .3, .3)))
    k = ease(prog(t, 2.9, .35))
    if k > 0:
        put(im, gspr(620, 170, tint=(255, 240, 240), fa=.92, ba=0), W / 2 + 120, 1290, k, .8 + .2 * spring(prog(t, 2.9, .5)))
        put(im, tspr("Examiner’s notes:", F("Medium", 34), (120, 70, 90), False), W / 2 - 20, 1250, k)
        note = "Band… 5.5?"; n = int(clamp((t - 3.3) / .8) * len(note))
        if n > 0: put(im, tspr(note[:n], F("Bold", 58), RED_D, False), W / 2 + 120 - (tw(note, F("Bold", 58)) - tw(note[:n], F("Bold", 58))) / 2, 1310, k)
    tick_k = (t * 2) % 1
    dr = ImageDraw.Draw(im); cx, cy, r = 900, 400, 60
    dr.ellipse((cx - r, cy - r, cx + r, cy + r), outline=LAV_L, width=6)
    a = -math.pi / 2 + int(t * 2) * math.pi / 30
    dr.line((cx, cy, cx + math.cos(a) * 48, cy + math.sin(a) * 48), fill=(245, 120, 160), width=5)
    dr.line((cx, cy, cx + 28, cy - 6), fill=LAV_L, width=7)

FIX = ["In my opinion, …", "From my experience, …", "To be honest, …"]
def m_fix(im, t, gt):
    badge(im, t, gt, pop=True)
    kinetic(im, ["THE", "FIX"], 420, F("Bold", 130), [WHITE, AMB], t, .05, .15, .45)
    put(im, tspr("Have 3 openers ready:", F("Bold", 58), LAV), W / 2, 580, ease(prog(t, .4, .4)))
    val = 5.5
    for i, w in enumerate(FIX):
        st = .7 + i * .45; k = prog(t, st, .55)
        if k > 0:
            x = W / 2 + (1 - spring(k)) * 750; cy = 760 + i * 165
            put(im, gspr(820, 135), x, cy, ease(k * 2))
            ImageDraw.Draw(im).ellipse((x - 375, cy - 11, x - 353, cy + 11), fill=AMB)
            put(im, tspr(w, F("Bold", 58), WHITE), x + 10, cy - 4, ease(k * 2))
            sparkle(im, x + 380, cy, prog(t, st + .2, .6), AMB, rad=80)
            val += .7 * ease(prog(t, st + .2, .45))
    meter(im, 1330, val, ease(prog(t, .5, .4)))

SCENES = [(m_home, 4.2, False, []), (m_test, 5.2, False, []), (m_fix, 3.6, True, []), (s_out, 3.8, False, [])]
STARTS = np.cumsum([0] + [s[1] for s in SCENES])[:-1]; TOTAL = sum(s[1] for s in SCENES)

def m_sound(out):
    sys.path.insert(0, "/home/claude/reel"); import music_kit as mk
    from scipy.io import wavfile
    SR = mk.SR; bed = np.load("/home/claude/reel/bed.npy").astype(np.float64); n = int(TOTAL * SR)
    rng = np.random.default_rng(12); sfx = np.zeros(len(bed))
    def add(sig, t0, g=1.0):
        i = int(t0 * SR); j = min(len(sfx), i + len(sig))
        if 0 <= i < len(sfx): sfx[i:j] += sig[: j - i] * g
    def bellseq(t0, notes, g=.13, dt=.07):
        for k, m in enumerate(notes): add(mk.bell(m, .9), t0 + k * dt, g)
    def tick(t0, g=.08, f=1300): tt = mk.T(.05); add(np.sin(2 * np.pi * f * tt) * np.exp(-tt * 80), t0, g)
    def scratch(t0):
        tt = mk.T(.45); f = 900 - 1600 * (tt / .45) + 400 * np.sin(tt * 60)
        s = np.sin(2 * np.pi * np.cumsum(np.maximum(f, 80)) / SR) * .5 + mk.bp(rng.standard_normal(len(tt)), 600, 4000) * .5
        add(s * np.exp(-tt * 3), t0, .35)
    def popsnd(t0): tt = mk.T(.12); f = 500 + 1400 * tt / .12; add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 30), t0, .2)
    def thump(t0, g=.55): tt = mk.T(.35); f = 55 + 120 * np.exp(-tt * 30); add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 10), t0, g)
    def gulp(t0): tt = mk.T(.25); f = 400 - 900 * tt; add(np.sin(2 * np.pi * np.cumsum(np.maximum(f, 90)) / SR) * np.exp(-tt * 12), t0, .2)
    a, b, c, d = STARTS
    bellseq(a + .05, [72, 79], .1)
    for i in range(sum(len(l) for l in HOME)): tick(a + .4 + i * 1.6 / sum(len(l) for l in HOME), .05)
    bellseq(a + 2.2, [84, 88, 91, 96], .09, .05)
    scratch(b - .1)
    for k in range(10): tick(b + .3 + k * .5, .14, 900)
    for tt0 in TT: gulp(b + tt0 - .05)
    for k in range(4): tick(b + 3.3 + k * .2, .06, 2200)
    thump(c + .05)
    for i in range(3): popsnd(c + .7 + i * .45)
    bellseq(c + 1.0, [76, 79, 84], .12)
    add(np.zeros(1), 0); bellseq(d + 1.5, [84, 88, 91, 96], .12)
    gain = np.ones(len(bed)); i0 = int(b * SR); i1 = int(c * SR); r = int(.08 * SR)
    gain[i0:i1] = 0.0; gain[i0 - r:i0] = np.linspace(1, 0, r); gain[i1:i1 + r] = np.linspace(0, 1, r)
    mix = (bed * gain + sfx)[:n]; fi = int(.3 * SR); mix[:fi] *= np.linspace(0, 1, fi)
    fo = int(1.2 * SR); mix[-fo:] *= np.linspace(1, 0, fo); mix /= np.max(np.abs(mix)) * 1.12
    L = mix.copy(); R = mix.copy(); dd = int(.015 * SR); R[dd:] = .75 * mix[:-dd] + .25 * mix[dd:]
    wavfile.write(out, SR, (np.stack([L, R], 1) * 32767).astype(np.int16))

if __name__ == "__main__":
    out = "/home/claude/reel/premium_meme"; os.makedirs(out, exist_ok=True)
    m = sys.argv[1]
    if m == "stills":
        ts = [(int(a), float(b)) for a, b in (x.split(":") for x in sys.argv[2].split(","))]
        ims = [finish(frame(i, t), None, STARTS[i] + t, 0)[0].resize((270, 480)) for i, t in ts]
        c = Image.new("RGB", (270 * len(ims), 480)); [c.paste(im, (k * 270, 0)) for k, im in enumerate(ims)]; c.save(f"{out}/contact.png")
    elif m == "scene":
        render(int(sys.argv[2]), out)
    elif m == "final":
        m_sound(f"{out}/music.wav")
        open(f"{out}/list.txt", "w").write("".join(f"file 'p{i}.mp4'\n" for i in range(len(SCENES))))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{out}/list.txt", "-c", "copy", f"{out}/v.mp4"], check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{out}/v.mp4", "-i", f"{out}/music.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-af", "acompressor=threshold=-22dB:ratio=2.5:attack=10:release=150:makeup=3,alimiter=limit=0.8:level=disabled,volume=-1.5dB",
                        "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", f"{out}/meme_home_vs_test_premium.mp4"], check=True)
