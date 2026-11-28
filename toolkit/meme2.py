"""Dark-humour meme: starting every IELTS Speaking answer with 'I think...'."""
import os, sys, math
os.environ.setdefault("OUTRO", "Subscribe for a daily English fix")
_src = open("/home/claude/reel/meme.py").read().rsplit('if __name__ == "__main__":', 1)[0]
exec(_src)

BONE = (242, 236, 222); BONE_D = (196, 188, 170); NIGHT = (22, 20, 52); NIGHT2 = (36, 32, 80); GRASS = (52, 110, 92); STONE = (150, 150, 170); STONE_D = (120, 120, 142)

def bub(cv, cx, cy, w, h, k, tail_x, fill=WHITE):
    if k <= 0: return
    s = lerp(.4, 1, spring(k))
    cv.save(); cv.translate(cx, cy); cv.scale(s, s); cv.saveLayerAlpha(None, int(255 * clamp(k * 3)))
    rrect(cv, -w / 2, -h / 2 + 14, w / 2, h / 2 + 14, 40, P(NAVY, 60, blur=7)); rrect(cv, -w / 2, -h / 2, w / 2, h / 2, 40, P(fill))
    tl = skia.Path(); tl.moveTo(tail_x - 34, h / 2 - 2); tl.lineTo(tail_x + 18, h / 2 - 2); tl.lineTo(tail_x - 6, h / 2 + 58); tl.close(); cv.drawPath(tl, P(fill))
    cv.restore(); cv.restore()

def bub_text(cv, cx, cy, w, h, k, tail_x, txt, f, col=NAVY, fill=WHITE):
    bub(cv, cx, cy, w, h, k, tail_x, fill)
    if k > 0:
        s = lerp(.4, 1, spring(k)); cv.save(); cv.translate(cx, cy); cv.scale(s, s)
        text(cv, txt, 0, 2, f, col, 255 * clamp(k * 3)); cv.restore()

def examiner2(cv, x, y, s, t, age=0.0, brow=0.0):
    cv.save(); cv.translate(x, y); cv.scale(s, s)
    SK = mixc((238, 196, 166), (226, 206, 196), age); CARD = (150, 58, 82); HAIRG = mixc((180, 180, 194), (250, 250, 252), age)
    body = skia.Path(); body.moveTo(-150, 210); body.cubicTo(-300, 240, -340, 320, -350, 900); body.lineTo(350, 900)
    body.cubicTo(340, 320, 300, 240, 150, 210); body.close(); cv.drawPath(body, P(CARD))
    col = skia.Path(); col.moveTo(-90, 215); col.lineTo(0, 320); col.lineTo(90, 215); col.close(); cv.drawPath(col, P(WHITE))
    tie = skia.Path(); tie.moveTo(-18, 250); tie.lineTo(18, 250); tie.lineTo(30, 420); tie.lineTo(0, 460); tie.lineTo(-30, 420); tie.close(); cv.drawPath(tie, P(NAVY))
    rrect(cv, -60, 120, 60, 240, 30, P(mixc((214, 172, 144), (200, 184, 176), age)))
    cv.drawCircle(-150, 10, 34, P(SK)); cv.drawCircle(150, 10, 34, P(SK))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-150, -180, 150, 175), 140, 160), P(SK))
    for sgn in (-1, 1): cv.drawOval(skia.Rect.MakeLTRB(sgn * 150 - 40, -110, sgn * 150 + 40, 10 + 60 * age), P(HAIRG))
    if age > .3:
        for i in range(3):
            yy = -120 + i * 22; cv.drawLine(-70, yy, 70, yy + 4 * (i % 2), P(mixc(SK, (150, 120, 110), .6), 255 * (age - .3) / .7, stroke=5))
        for sgn in (-1, 1):
            cv.drawLine(sgn * 100, 40, sgn * 120, 70, P((150, 120, 110), 200 * age, stroke=5))
    for sgn in (-1, 1):
        cv.drawCircle(sgn * 60, 20, 44, P(NAVY, stroke=9)); cv.drawCircle(sgn * 60, 22, 9 - 3 * age, P(HAIR))
        lift = brow * 26 if sgn == 1 else brow * 6
        cv.save(); cv.translate(sgn * 60, -46 - lift); cv.rotate(sgn * (-6 * brow)); rrect(cv, -34, -8, 34, 8, 8, P(HAIRG)); cv.restore()
    cv.drawLine(-16, 20, 16, 20, P(NAVY, stroke=8))
    ms = skia.Path(); ms.moveTo(-60, 100); ms.cubicTo(-30, 75, 30, 75, 60, 100); ms.cubicTo(30, 92, -30, 92, -60, 100); ms.close()
    cv.drawPath(ms, P(HAIRG, stroke=20 + 14 * age))
    m = skia.Path(); m.moveTo(-26, 132); m.quadTo(0, 120 - 20 * age, 26, 132); cv.drawPath(m, P((150, 70, 70), stroke=8))
    clipboard(cv)
    cv.restore()

def clipboard(cv):
    cv.save(); cv.translate(-40, 470); cv.rotate(-8)
    rrect(cv, -150, -110, 150, 170, 18, P((176, 126, 80))); rrect(cv, -125, -80, 125, 150, 8, P(WHITE))
    rrect(cv, -50, -128, 50, -92, 10, P((120, 120, 136)))
    for i in range(4): cv.drawLine(-100, -40 + i * 42, 60 if i < 3 else -10, -40 + i * 42, P(GREY_D, stroke=8))
    cv.restore()

def skeleton(cv, x, y, s, t):
    cv.save(); cv.translate(x, y); cv.scale(s, s)
    body = skia.Path(); body.moveTo(-150, 210); body.cubicTo(-300, 240, -340, 320, -350, 900); body.lineTo(350, 900)
    body.cubicTo(340, 320, 300, 240, 150, 210); body.close(); cv.drawPath(body, P((150, 58, 82)))
    col = skia.Path(); col.moveTo(-90, 215); col.lineTo(0, 320); col.lineTo(90, 215); col.close(); cv.drawPath(col, P(WHITE))
    tie = skia.Path(); tie.moveTo(-18, 250); tie.lineTo(18, 250); tie.lineTo(30, 420); tie.lineTo(0, 460); tie.lineTo(-30, 420); tie.close(); cv.drawPath(tie, P(NAVY))
    for i in range(4): rrect(cv, -22, 120 + i * 26, 22, 140 + i * 26, 8, P(BONE))
    cv.save(); cv.rotate(6 * math.sin(t * 1.3))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-140, -190, 140, 110), 140, 150), P(BONE))
    rrect(cv, -90, 70, 90, 170, 40, P(BONE))
    for sgn in (-1, 1):
        cv.drawOval(skia.Rect.MakeLTRB(sgn * 60 - 42, -40, sgn * 60 + 42, 40), P(NAVY))
        cv.drawCircle(sgn * 60, 20, 44, P((60, 60, 70), stroke=9))
    tri = skia.Path(); tri.moveTo(0, 50); tri.lineTo(-18, 88); tri.lineTo(18, 88); tri.close(); cv.drawPath(tri, P(NAVY))
    for i in range(6): rrect(cv, -66 + i * 23, 118, -48 + i * 23, 152, 4, P(WHITE)); cv.drawLine(-70, 135, 70, 135, P(BONE_D, stroke=4))
    cv.drawLine(-80, -150, -20, -110, P(BONE_D, stroke=5)); cv.drawLine(-20, -110, -40, -80, P(BONE_D, stroke=5))
    cv.restore()
    clipboard(cv)
    # cobwebs
    for (cx, cy, r0) in [(-200, -230, 150), (230, 380, 120)]:
        for i in range(5):
            a = math.pi / 2 * i / 4
            cv.drawLine(cx, cy, cx + math.cos(a) * r0 * (1 if cx < 0 else -1), cy + math.sin(a) * r0, P((230, 230, 240), 180, stroke=3))
        for j in (.4, .7, 1.0):
            pth = skia.Path(); pts = [(cx + math.cos(math.pi / 2 * i / 4) * r0 * j * (1 if cx < 0 else -1), cy + math.sin(math.pi / 2 * i / 4) * r0 * j) for i in range(5)]
            pth.moveTo(*pts[0]); [pth.lineTo(*p) for p in pts[1:]]; cv.drawPath(pth, P((230, 230, 240), 160, stroke=3, cap=False))
    cv.restore()

def counter(cv, n, k, pulse):
    if k <= 0: return
    s = (1 + .15 * pulse) * lerp(.5, 1, spring(k))
    cv.save(); cv.translate(540, 1500); cv.rotate(-3); cv.scale(s, s)
    rrect(cv, -330, -62, 330, 76, 28, P(NAVY, 90, blur=6)); rrect(cv, -330, -66, 330, 66, 28, P(RED_D if False else (232, 70, 90)))
    text(cv, f"“I think” counter: {n}", 0, 2, font("Bold", 54), WHITE); cv.restore()

QA = [(0.15, "Where are you from?", 0.75, "I think… Portugal."), (1.6, "Do you work or study?", 2.2, "I think… both?"),
      (3.0, "What’s your name?", 3.55, "I think… Ana?")]
def s1(cv, t, gt):  # 5.7 s: the interview
    exam_room(cv, gt)
    b = ease(prog(t, 2.0, 2.0))
    examiner2(cv, 250, 1150, .62, gt, age=.6 * b, brow=ease(prog(t, .9, .3)))
    learner(cv, 770, 1170, .80, t, "nervous", shake=3 * math.sin(t * 30))
    desk(cv)
    for i, (tq, q, ta, a) in enumerate(QA):
        nxt = QA[i + 1][0] if i + 1 < len(QA) else 9
        if tq <= t < nxt: bub_text(cv, 380, 780, 600, 130, prog(t, tq, .3), -150, q, font("Bold", 46))
        if ta <= t < nxt: bub_text(cv, 700, 600, 640, 130, prog(t, ta, .3), 120, a, font("Bold", 52), PINK if False else NAVY, (255, 236, 244))
    n = sum(1 for _, _, ta, _ in QA if t >= ta)
    pulse = max([clamp(1 - (t - ta) / .25) if t >= ta else 0 for _, _, ta, _ in QA] + [0])
    counter(cv, n, prog(t, .75, .3), pulse)
    pill(cv, W / 2, 220, "POV: every answer starts with “I think…”", font("Bold", 38), PINK, WHITE, prog(t, -.3, .3))
    if t > 4.4:
        k = prog(t, 4.4, .25); cv.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), P(NIGHT, 255 * k))
        if t > 4.55:
            kk = prog(t, 4.55, .3); s = lerp(.6, 1, spring(kk))
            cv.save(); cv.translate(540, 900); cv.scale(s, s); text(cv, "3 hours later…", 0, 0, font("Bold", 110), AMBER, 255 * clamp(kk * 3)); cv.restore()
            for i in range(12):
                a = t * 9 + i * .52; cv.drawCircle(540 + math.cos(a) * 220, 900 + math.sin(a) * 220, 6, P(LILAC, 120))

def s2(cv, t, gt):  # 3.4 s: skeleton examiner
    exam_room(cv, gt * 6)
    skeleton(cv, 250, 1150, .62, gt)
    learner(cv, 770, 1170, .80, t, "nervous", shake=3 * math.sin(t * 30))
    desk(cv)
    bub_text(cv, 700, 600, 640, 130, prog(t, .3, .3), 120, "I think… I think…", font("Bold", 52), NAVY, (255, 236, 244))
    n = 3 + int(44 * ease(prog(t, .2, 1.6)))
    counter(cv, n, 1, (t * 8) % 1 * (t < 1.8))
    pill(cv, W / 2, 220, "The examiner:", font("Bold", 44), NAVY, WHITE, prog(t, .1, .3))
    if t < .25: cv.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), P(NIGHT, 255 * (1 - t / .25)))

def s3(cv, t, gt):  # 3.0 s: RIP band 7
    cv.clear(C(NIGHT))
    for i in range(40):
        r = np.random.default_rng(i); x = r.uniform(0, W); y = r.uniform(0, 1100)
        cv.drawCircle(x, y, r.uniform(2, 5), P(WHITE, 120 + 100 * math.sin(gt * 3 + i)))
    cv.drawCircle(860, 330, 90, P((250, 240, 200))); cv.drawCircle(900, 300, 80, P(NIGHT))
    gr = skia.Path(); gr.moveTo(-50, 1400); gr.cubicTo(300, 1300, 800, 1300, 1130, 1400); gr.lineTo(1130, 2000); gr.lineTo(-50, 2000); gr.close(); cv.drawPath(gr, P(GRASS))
    rise = ease(prog(t, 0, .5)); yb = 1400 + (1 - rise) * 500
    st = skia.Path(); st.moveTo(300, yb); st.lineTo(300, yb - 560); st.cubicTo(300, yb - 800, 780, yb - 800, 780, yb - 560); st.lineTo(780, yb); st.close()
    cv.drawPath(st, P(STONE_D)); cv.save(); cv.translate(-14, 0); cv.drawPath(st, P(STONE)); cv.restore()
    text(cv, "RIP", 526, yb - 560, font("Bold", 120), (90, 90, 110))
    text(cv, "my Band 7", 526, yb - 420, font("Bold", 64), (70, 70, 92))
    text(cv, "2026 – 2026", 526, yb - 330, font("Medium", 44), (90, 90, 110))
    text(cv, "Killed by “I think” ×47", 526, yb - 230, font("Medium", 36), (90, 90, 110))
    for i, c in enumerate([PINK, AMBER, MINT, PINK]):
        fx = 360 + i * 110; cv.drawLine(fx, yb + 10, fx, yb - 70, P(MINT_D, stroke=8)); cv.drawCircle(fx, yb - 80, 26, P(c)); cv.drawCircle(fx, yb - 80, 10, P(AMBER))
    gk = prog(t, .9, 2.0)
    if gk > 0:
        gx = 560 + 40 * math.sin(t * 4); gy = 900 - 420 * ease(gk)
        g = skia.Path(); g.moveTo(gx - 90, gy + 120)
        for i in range(5): g.quadTo(gx - 90 + i * 45 + 22, gy + 150 - 30 * (i % 2), gx - 90 + (i + 1) * 45 - 10, gy + 120)
        g.lineTo(gx + 90, gy); g.cubicTo(gx + 90, gy - 130, gx - 90, gy - 130, gx - 90, gy); g.close()
        cv.saveLayerAlpha(None, int(230 * clamp(gk * 3))); cv.drawPath(g, P(WHITE))
        cv.drawOval(skia.Rect.MakeLTRB(gx - 45, gy - 40, gx - 15, gy), P(NAVY)); cv.drawOval(skia.Rect.MakeLTRB(gx + 15, gy - 40, gx + 45, gy), P(NAVY))
        text(cv, "7", gx, gy + 60, font("Bold", 80), PINK); cv.restore()
    pill(cv, W / 2, 220, "Me, after the test:", font("Bold", 44), PINK, WHITE, prog(t, .1, .3))

FIX = ["In my opinion, …", "From my perspective, …", "I’d say that …"]
SCENES = [(s1, 5.7), (s2, 3.4), (s3, 3.2), (sC, 3.6), (sD, 3.6)]
STARTS = np.cumsum([0] + [d for _, d in SCENES])[:-1]; TOTAL = sum(d for _, d in SCENES)

def sound2(out):
    sys.path.insert(0, "/home/claude/reel"); import music_kit as mk
    from scipy.io import wavfile
    SR = mk.SR; bed = np.load("/home/claude/reel/bed.npy").astype(np.float64); n = int(TOTAL * SR)
    rng = np.random.default_rng(21); sfx = np.zeros(len(bed))
    def add(sig, t0, g=1.0):
        i = int(t0 * SR); j = min(len(sfx), i + len(sig))
        if 0 <= i < len(sfx): sfx[i:j] += sig[: j - i] * g
    def bellseq(t0, notes, g=.13, dt=.07):
        for k, m in enumerate(notes): add(mk.bell(m, .9), t0 + k * dt, g)
    def tick(t0, g=.08, f=1300): tt = mk.T(.05); add(np.sin(2 * np.pi * f * tt) * np.exp(-tt * 80), t0, g)
    def popsnd(t0): tt = mk.T(.12); f = 500 + 1400 * tt / .12; add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 30), t0, .2)
    def thump(t0, g=.55): tt = mk.T(.35); f = 55 + 120 * np.exp(-tt * 30); add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 10), t0, g)
    def buzz(t0): tt = mk.T(.22); add(mk.bp(np.sign(np.sin(2 * np.pi * 120 * tt)), 200, 2000) * np.exp(-tt * 8), t0, .18)
    def poof(t0): tt = mk.T(.5); add(mk.bp(rng.standard_normal(len(tt)), 300, 2500) * np.exp(-tt * 7), t0, .25)
    def crickets(t0, dur):
        for k in range(int(dur * 3)):
            tt = mk.T(.12); ch = np.sin(2 * np.pi * 4300 * tt) * (np.sin(2 * np.pi * 60 * tt) > 0) * np.exp(-tt * 12); add(ch, t0 + k / 3 + .1 * (k % 2), .05)
    def sad(t0):
        for k, m in enumerate([62, 61, 60, 59]):
            dur = .5 if k < 3 else 1.1; tt = mk.T(dur); f = mk.hz(m) * (1 + .012 * np.sin(2 * np.pi * 5.5 * tt) * (k == 3))
            ph = 2 * np.pi * np.cumsum(f) / SR; s = (np.sin(ph) + .5 * np.sin(2 * ph) + .3 * np.sin(3 * ph)) * np.minimum(1, tt / .03) * np.exp(-tt * (1.2 if k == 3 else 2.5))
            add(mk.bp(s, 120, 2500), t0 + k * .45, .22)
    a, b, c, d, e = STARTS
    bellseq(a + .05, [72, 79], .08)
    for tq, _, ta, _ in QA: popsnd(a + tq); buzz(a + ta + .05)
    for k in range(6): tick(a + 4.6 + k * .18, .12, 900)
    poof(b); crickets(b + .2, 3.1)
    for k in range(20): tick(b + .2 + k * .08, .05, 2000)
    sad(c + .25)
    thump(d + .05)
    for i in range(3): popsnd(d + .8 + i * .4)
    bellseq(d + 1.0, [76, 79, 84], .12); popsnd(d + 2.0)
    popsnd(e + .1); bellseq(e + 1.5, [84, 88, 91, 96], .12)
    gain = np.full(len(bed), .75); i0 = int((a + 4.4) * SR); i1 = int(d * SR); r = int(.1 * SR)
    gain[i0:i1] = 0.0; gain[i0 - r:i0] = np.linspace(.75, 0, r); gain[i1:] = 1.0; gain[i1:i1 + r] = np.linspace(0, 1, r)
    mix = (bed * gain + sfx)[:n]; fi = int(.3 * SR); mix[:fi] *= np.linspace(0, 1, fi)
    fo = int(1.2 * SR); mix[-fo:] *= np.linspace(1, 0, fo); mix /= np.max(np.abs(mix)) * 1.12
    L = mix.copy(); R = mix.copy(); dd = int(.015 * SR); R[dd:] = .75 * mix[:-dd] + .25 * mix[dd:]
    wavfile.write(out, SR, (np.stack([L, R], 1) * 32767).astype(np.int16))

if __name__ == "__main__":
    out = "/home/claude/reel/meme2"; os.makedirs(out, exist_ok=True)
    m = sys.argv[1]
    if m == "stills":
        from PIL import Image
        ts = [float(x) for x in sys.argv[2].split(",")]
        ims = [Image.fromarray(draw(t)[:, :, [2, 1, 0]]).resize((270, 480)) for t in ts]
        c = Image.new("RGB", (270 * len(ims), 480)); [c.paste(im, (i * 270, 0)) for i, im in enumerate(ims)]; c.save(f"{out}/contact.png")
    elif m == "part":
        render(int(sys.argv[2]), int(sys.argv[3]), f"{out}/part{sys.argv[4]}.mp4")
    elif m == "sound":
        sound2(f"{out}/music.wav"); print(int(round(TOTAL * FPS)))
