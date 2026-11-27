"""Meme-style cartoon: practising at home vs the actual IELTS Speaking test."""
import os, sys, math
_src = open("/home/claude/reel/cartoon.py").read().replace('if __name__ == "__main__":', 'if False:')
exec(_src)

GREY_WALL = (208, 216, 236); GREY_D = (176, 186, 214); WOOD = (150, 118, 168); WOOD_D = (122, 94, 142)
SWEAT = (120, 196, 255)

def star(cv, x, y, s, col):
    if s < 1: return
    p = skia.Path(); p.moveTo(x, y - s); p.lineTo(x + s * .3, y - s * .3); p.lineTo(x + s, y); p.lineTo(x + s * .3, y + s * .3)
    p.lineTo(x, y + s); p.lineTo(x - s * .3, y + s * .3); p.lineTo(x - s, y); p.lineTo(x - s * .3, y - s * .3); p.close(); cv.drawPath(p, P(col))

def learner(cv, x, y, s, t, mood="calm", shake=0.0, brush=False):
    cv.save(); cv.translate(x + shake, y); cv.scale(s, s)
    HOOD = TEAL; HOOD_D = (44, 160, 156); SK = (240, 186, 150); HR = (110, 58, 36)
    bob = 5 * math.sin(t * 7) if mood == "happy" else 0
    body = skia.Path(); body.moveTo(-150, 210); body.cubicTo(-300, 240, -340, 320, -350, 900); body.lineTo(350, 900)
    body.cubicTo(340, 320, 300, 240, 150, 210); body.close(); cv.drawPath(body, P(HOOD))
    hd = skia.Path(); hd.moveTo(-170, 215); hd.cubicTo(-120, 300, 120, 300, 170, 215); cv.drawPath(hd, P(HOOD_D, stroke=30))
    rrect(cv, -60, 120, 60, 240, 30, P((214, 160, 128)))
    cv.save(); cv.translate(0, bob); cv.rotate(4 * math.sin(t * 5) if mood == "happy" else 0)
    cv.drawCircle(0, -150, 150, P(HR)); cv.drawCircle(0, -262, 64, P(HR))
    cv.drawCircle(-150, 10, 34, P(SK)); cv.drawCircle(150, 10, 34, P(SK))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-150, -170, 150, 175), 140, 160), P(SK))
    fr = skia.Path(); fr.moveTo(-150, -40); fr.cubicTo(-140, -190, 140, -200, 150, -40); fr.cubicTo(80, -110, -60, -120, -150, -40); fr.close()
    cv.drawPath(fr, P(HR))
    if mood == "happy":
        for sgn in (-1, 1):
            a = skia.Path(); a.moveTo(sgn * 60 - 26, 32); a.quadTo(sgn * 60, 2, sgn * 60 + 26, 32); cv.drawPath(a, P(HAIR, stroke=10))
            cv.save(); cv.translate(sgn * 60, -34); cv.rotate(sgn * -8); rrect(cv, -34, -8, 34, 8, 8, P(HR)); cv.restore()
        m = skia.Path(); m.moveTo(-52, 92); m.cubicTo(-40, 160, 40, 160, 52, 92); m.close(); cv.drawPath(m, P((120, 40, 50)))
        cv.save(); cv.clipPath(m, doAntiAlias=True); rrect(cv, -55, 86, 55, 108, 6, P(WHITE)); cv.drawCircle(0, 150, 30, P((236, 110, 120))); cv.restore()
        cv.drawCircle(-95, 75, 26, P(PINK, 90)); cv.drawCircle(95, 75, 26, P(PINK, 90))
    else:
        for sgn in (-1, 1):
            cv.drawCircle(sgn * 60, 24, 30, P(WHITE)); cv.drawCircle(sgn * 60 + 3 * math.sin(t * 9), 26, 8, P(HAIR))
            cv.save(); cv.translate(sgn * 60, -26); cv.rotate(sgn * 16); rrect(cv, -32, -7, 32, 7, 7, P(HR)); cv.restore()
        w = skia.Path(); w.moveTo(-40, 112)
        for i in range(1, 9): w.lineTo(-40 + i * 10, 112 + (6 if i % 2 else -6))
        cv.drawPath(w, P((150, 70, 70), stroke=7))
        cv.drawCircle(-95, 75, 22, P((170, 200, 230), 70)); cv.drawCircle(95, 75, 22, P((170, 200, 230), 70))
        for k, (sx, sy, ph) in enumerate([(128, -60, 0), (-132, -20, .45), (142, 20, .8)]):
            f = (t * .9 + ph) % 1
            dy = 120 * f; a = 255 * (1 - f)
            d = skia.Path(); cx, cy = sx, sy + dy
            d.moveTo(cx, cy - 26); d.cubicTo(cx + 18, cy - 4, cx + 16, cy + 14, cx, cy + 14); d.cubicTo(cx - 16, cy + 14, cx - 18, cy - 4, cx, cy - 26)
            cv.drawPath(d, P(SWEAT, a))
    cv.restore()
    if brush:
        cv.save(); cv.translate(170, 150); cv.rotate(-30)
        rrect(cv, -18, -10, 18, 210, 16, P((120, 76, 50)))
        cv.drawOval(skia.Rect.MakeLTRB(-48, -120, 48, 0), P((255, 140, 170)))
        for i in range(5): cv.drawLine(-30 + i * 15, -100, -30 + i * 15, -20, P((230, 100, 140), stroke=4))
        cv.restore()
        cv.drawCircle(200, 260, 46, P(SK))
    cv.restore()

def examiner(cv, x, y, s, t, brow=0.0, writing=False):
    cv.save(); cv.translate(x, y); cv.scale(s, s)
    SK = (238, 196, 166); CARD = (150, 58, 82); HAIRG = (180, 180, 194)
    body = skia.Path(); body.moveTo(-150, 210); body.cubicTo(-300, 240, -340, 320, -350, 900); body.lineTo(350, 900)
    body.cubicTo(340, 320, 300, 240, 150, 210); body.close(); cv.drawPath(body, P(CARD))
    col = skia.Path(); col.moveTo(-90, 215); col.lineTo(0, 320); col.lineTo(90, 215); col.close(); cv.drawPath(col, P(WHITE))
    tie = skia.Path(); tie.moveTo(-18, 250); tie.lineTo(18, 250); tie.lineTo(30, 420); tie.lineTo(0, 460); tie.lineTo(-30, 420); tie.close(); cv.drawPath(tie, P(NAVY))
    rrect(cv, -60, 120, 60, 240, 30, P((214, 172, 144)))
    cv.drawCircle(-150, 10, 34, P(SK)); cv.drawCircle(150, 10, 34, P(SK))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-150, -180, 150, 175), 140, 160), P(SK))
    for sgn in (-1, 1): cv.drawOval(skia.Rect.MakeLTRB(sgn * 150 - 40, -110, sgn * 150 + 30 * (1 if sgn > 0 else -1) * 0 + 40, 10), P(HAIRG))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-150, -180, 150, 175), 140, 160), P(SK, 0))
    for sgn in (-1, 1):
        cv.drawCircle(sgn * 60, 20, 44, P(NAVY, stroke=9)); cv.drawCircle(sgn * 60, 22, 9, P(HAIR))
        lift = brow * 26 if sgn == 1 else brow * 4
        cv.save(); cv.translate(sgn * 60, -46 - lift); cv.rotate(sgn * (-6 * brow)); rrect(cv, -34, -8, 34, 8, 8, P(HAIRG)); cv.restore()
    cv.drawLine(-16, 20, 16, 20, P(NAVY, stroke=8))
    ms = skia.Path(); ms.moveTo(-60, 100); ms.cubicTo(-30, 75, 30, 75, 60, 100); ms.cubicTo(30, 92, -30, 92, -60, 100); ms.close()
    cv.drawPath(ms, P(HAIRG, stroke=20))
    m = skia.Path(); m.moveTo(-26, 128); m.lineTo(26, 128); cv.drawPath(m, P((150, 70, 70), stroke=8))
    # clipboard
    cv.save(); cv.translate(-40, 470); cv.rotate(-8)
    rrect(cv, -150, -110, 150, 170, 18, P((176, 126, 80))); rrect(cv, -125, -80, 125, 150, 8, P(WHITE))
    rrect(cv, -50, -128, 50, -92, 10, P((120, 120, 136)))
    for i in range(4): cv.drawLine(-100, -40 + i * 42, 60 if i < 3 else -10, -40 + i * 42, P(GREY_D, stroke=8))
    if writing:
        px = -100 + (t * 260) % 160; py = 86 + 6 * math.sin(t * 30)
        cv.drawLine(-100, 86, px, py, P(RED_D if 'RED_D' in globals() else PINK, stroke=7))
        cv.save(); cv.translate(px, py); cv.rotate(35); rrect(cv, -10, -120, 10, 0, 8, P(NAVY)); cv.restore()
        cv.drawCircle(150, 60, 50, P(SK))
    cv.restore()
    cv.restore()

def exam_room(cv, t):
    cv.clear(C(GREY_WALL))
    for i in range(8): cv.drawRect(skia.Rect.MakeLTRB(-60 + i * 160, 0, 20 + i * 160, 1500), P(GREY_D, 70))
    cx, cy, r = 930, 430, 95
    cv.drawCircle(cx, cy + 8, r, P(NAVY, 50, blur=6)); cv.drawCircle(cx, cy, r, P(WHITE)); cv.drawCircle(cx, cy, r, P(NAVY, stroke=12))
    for i in range(12):
        a = i * math.pi / 6; cv.drawLine(cx + math.cos(a) * 78, cy + math.sin(a) * 78, cx + math.cos(a) * 88, cy + math.sin(a) * 88, P(NAVY, stroke=6))
    sa = -math.pi / 2 + int(t * 2) * (math.pi / 30)
    cv.drawLine(cx, cy, cx + math.cos(sa) * 80, cy + math.sin(sa) * 80, P(PINK, stroke=5))
    cv.drawLine(cx, cy, cx + 50, cy - 10, P(NAVY, stroke=10)); cv.drawLine(cx, cy, cx - 10, cy - 66, P(NAVY, stroke=10))
    rrect(cv, 90, 380, 520, 480, 16, P(NAVY)); text(cv, "SPEAKING TEST", 305, 430, font("Bold", 46), WHITE)
    text(cv, "Please stay quiet", 305, 515, font("Medium", 32), (120, 130, 160))

def desk(cv):
    rrect(cv, -100, 1570, 1180, 1630, 18, P(WOOD)); cv.drawRect(skia.Rect.MakeLTRB(-100, 1620, 1180, 2400), P(WOOD_D))

def lines_bubble(cv, cx, cy, w, lines, f, shown, k, col=NAVY, lh=78, fill=WHITE):
    h = lh * max(1, len(lines)) + 70
    bubble(cv, cx, cy, w, h, lerp(.4, 1, spring(k)), 255 * clamp(k * 3), fill=fill)
    if k <= 0: return
    y0 = cy - (len(lines) - 1) * lh / 2
    for i, (ln, n) in enumerate(zip(lines, shown)):
        if n > 0: text(cv, ln[:n], cx - w / 2 + 50, y0 + i * lh, f, col, align="left")

HOME = ["Well, in my opinion,", "technology has completely", "transformed how we live!"]
def sA(cv, t, gt):  # at home, fluent (4.2 s)
    room(cv, gt)
    for i in range(10):
        a = i * .63 + gt; rr = 380 + 30 * math.sin(gt * 2 + i)
        star(cv, 540 + math.cos(a) * rr, 1100 + math.sin(a) * rr * .8, 14 + 8 * math.sin(gt * 4 + i), AMBER)
    learner(cv, 540, 1150, .95, t, "happy", brush=True)
    pill(cv, W / 2, 220, "Me practising IELTS Speaking at home", font("Bold", 40), MINT, NAVY, prog(t, 0, .35))
    k = prog(t, .25, .35); f = font("Bold", 58)
    total = sum(len(l) for l in HOME); n = int(clamp((t - .5) / 1.7) * total); shown = []
    for l in HOME: shown.append(min(len(l), n)); n = max(0, n - len(l))
    lines_bubble(cv, 540, 560, 900, HOME, f, shown, k)
    if t > 2.3: text(cv, "Fluent. Confident. Band 9.", 540, 790, font("Bold", 50), NAVY, 255 * ease(prog(t, 2.3, .4)))
    if t > 4.0: cv.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), P(WHITE, 255 * prog(t, 4.0, .2)))

TEST = ["Ehm…", "I think…", "it’s very… very important…"]
TT = [.7, 1.7, 2.7]
def sB(cv, t, gt):  # the real test (5.2 s)
    z = 1 + .15 * eio(prog(t, 3.6, 1.2)); fx, fy = 760, 1000
    cv.save(); cv.translate(fx, fy); cv.scale(z, z); cv.translate(-fx, -fy)
    exam_room(cv, t)
    examiner(cv, 250, 1150, .62, gt, brow=ease(prog(t, 2.0, .3)), writing=t > 3.1)
    sh = 6 * math.sin(t * 40) * (.3 + .7 * prog(t, 1.5, 2))
    learner(cv, 770, 1170, .80, t, "nervous", shake=sh)
    desk(cv)
    f = font("Bold", 52); shown = [len(l) if t > TT[i] else 0 for i, l in enumerate(TEST)]
    lines_bubble(cv, 580, 660, 900, TEST, f, shown, prog(t, .4, .3))
    cv.restore()
    pill(cv, W / 2, 220, "Me in the actual test", font("Bold", 44), PINK, WHITE, prog(t, 0, .3))
    if t < .25: cv.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), P(WHITE, 255 * (1 - t / .25)))

FIX = ["In my opinion, …", "From my experience, …", "To be honest, …"]
def sC(cv, t, gt):  # the fix (3.6 s)
    flat_bg(cv, MINT, (134, 238, 198), gt, 3)
    slab(cv, 540, 360, "THE FIX", font("Bold", 150), NAVY, WHITE, prog(t, .05, .35), -3)
    k = ease(prog(t, .45, .4))
    text(cv, "Have 3 openers ready:", 540, 560 + (1 - k) * 20, font("Bold", 60), NAVY, 255 * k)
    for i, ln in enumerate(FIX):
        kk = prog(t, .8 + i * .4, .4)
        if kk <= 0: continue
        s = lerp(.5, 1, spring(kk)); cy = 720 + i * 160
        cv.save(); cv.translate(540, cy); cv.scale(s, s); cv.saveLayerAlpha(None, int(255 * clamp(kk * 3)))
        rrect(cv, -400, -58, 400, 70, 50, P(NAVY, 60, blur=6)); rrect(cv, -400, -62, 400, 62, 50, P(WHITE))
        cv.drawCircle(-340, 0, 16, P(PINK)); text(cv, ln, 20, 0, font("Bold", 56), NAVY)
        cv.restore(); cv.restore()
    pop = back(prog(t, 1.9, .5))
    jak(cv, 540, 1620 + (1 - pop) * 400, .58, gt, mouth="grin", blink=blink_at(t))
    if t > 3.3: speedlines(cv, prog(t, 3.3, .3))

def sD(cv, t, gt): scene4(cv, t, gt)

SCENES = [(sA, 4.2), (sB, 5.2), (sC, 3.6), (sD, 3.6)]
STARTS = np.cumsum([0] + [d for _, d in SCENES])[:-1]; TOTAL = sum(d for _, d in SCENES)

def meme_sound(out):
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
    bellseq(a + .05, [72, 79], .1); popsnd(a + .25)
    for i in range(sum(len(l) for l in HOME)): tick(a + .5 + i * 1.7 / sum(len(l) for l in HOME), .05)
    bellseq(a + 2.3, [84, 88, 91, 96], .09, .05)
    scratch(b - .1)
    for k in range(int(5.2 * 2)): tick(b + .3 + k * .5, .14, 900)
    for tt0 in TT: gulp(b + tt0 - .05)
    thump(c + .05); popsnd(c + 2.0)
    for i in range(3): popsnd(c + .8 + i * .4)
    bellseq(c + 1.0, [76, 79, 84], .12)
    popsnd(d + .1); bellseq(d + 1.5, [84, 88, 91, 96], .12)
    gain = np.ones(len(bed)); i0 = int(b * SR); i1 = int(c * SR)
    gain[i0:i1] = 0.0; ramp = int(.08 * SR); gain[i0 - ramp:i0] = np.linspace(1, 0, ramp); gain[i1:i1 + ramp] = np.linspace(0, 1, ramp)
    mix = (bed * gain + sfx)[:n]; fi = int(.3 * SR); mix[:fi] *= np.linspace(0, 1, fi)
    fo = int(1.2 * SR); mix[-fo:] *= np.linspace(1, 0, fo); mix /= np.max(np.abs(mix)) * 1.12
    L = mix.copy(); R = mix.copy(); dd = int(.015 * SR); R[dd:] = .75 * mix[:-dd] + .25 * mix[dd:]
    wavfile.write(out, SR, (np.stack([L, R], 1) * 32767).astype(np.int16))

if __name__ == "__main__":
    out = "/home/claude/reel/meme"; os.makedirs(out, exist_ok=True)
    m = sys.argv[1]
    if m == "stills":
        from PIL import Image
        ts = [float(x) for x in sys.argv[2].split(",")]
        ims = [Image.fromarray(draw(t)[:, :, [2, 1, 0]]).resize((270, 480)) for t in ts]
        c = Image.new("RGB", (270 * len(ims), 480)); [c.paste(im, (i * 270, 0)) for i, im in enumerate(ims)]; c.save(f"{out}/contact.png")
    elif m == "part":
        render(int(sys.argv[2]), int(sys.argv[3]), f"{out}/part{sys.argv[4]}.mp4")
    elif m == "sound":
        meme_sound(f"{out}/music.wav"); print(int(round(TOTAL * FPS)))
