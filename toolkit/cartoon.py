"""Flat-vector explainer-style test Reel: cartoon Teacher Jak, 'I am agree' -> 'I agree'."""
import sys, os, math, subprocess
import numpy as np
import skia

W, H, FPS = 1080, 1920, 30
FD = "/usr/share/fonts/truetype/google-fonts/"
TF = {w: skia.Typeface.MakeFromFile(FD + f"Poppins-{w}.ttf") for w in ("Bold", "Medium", "Regular")}
_FONTS = {}
def font(w, s):
    k = (w, int(s))
    if k not in _FONTS: _FONTS[k] = skia.Font(TF[w], int(s))
    return _FONTS[k]

def C(c, a=255): return skia.Color(int(c[0]), int(c[1]), int(c[2]), int(max(0, min(255, a))))
def P(c, a=255, stroke=0, cap=True, blur=0):
    p = skia.Paint(Color=C(c, a), AntiAlias=True)
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke)
        if cap: p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p

def clamp(x): return max(0.0, min(1.0, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def back(x): x = clamp(x); c = 1.8; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def spring(x): x = clamp(x); return 1 - math.exp(-6.5 * x) * math.cos(11 * x)
def prog(t, a, d): return clamp((t - a) / d)
def lerp(a, b, k): return a + (b - a) * k
def mixc(a, b, k): return tuple(lerp(a[i], b[i], k) for i in range(3))

# palette (original, built around the Teacher Jak purple)
NAVY = (38, 33, 92); PURP = (88, 70, 196); PURP_L = (122, 106, 224); PURP_D = (66, 52, 160)
LILAC = (236, 230, 255); LILAC_D = (214, 205, 248); WHITE = (255, 255, 255)
MINT = (104, 228, 180); MINT_D = (40, 170, 128); PINK = (255, 98, 146); AMBER = (255, 186, 76)
TEAL = (62, 196, 190); SKY = (178, 214, 255)
SKIN = (218, 162, 124); SKIN_S = (200, 142, 106); SKIN_D = (180, 122, 90)
HAIR = (26, 20, 36); BEARD = (48, 34, 40); JACKET = (34, 31, 46); JACKET_L = (52, 48, 68); TEE = (30, 128, 92); TEE_D = (22, 100, 72)

def text(cv, s, x, y, f, col, a=255, align="center"):
    w = f.measureText(s); m = f.getMetrics()
    xx = x - w / 2 if align == "center" else x
    cv.drawString(s, xx, y - (m.fAscent + m.fDescent) / 2, f, P(col, a))
    return w

def rrect(cv, l, t, r, b, rad, paint):
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(l, t, r, b), rad, rad), paint)

def shadow_rrect(cv, l, t, r, b, rad, a=70, dy=14):
    rrect(cv, l, t + dy, r, b + dy, rad, P(NAVY, a, blur=10))

# ---------- characters ----------
def jak(cv, x, y, s, t, look=(0, 0), brow=0.0, mouth="smile", blink=0.0, wink=0.0, wave=None, tilt=0.0):
    """Cartoon Teacher Jak bust, head centre at (x, y)."""
    cv.save(); cv.translate(x, y); cv.scale(s, s)
    br = 1 + 0.012 * math.sin(t * 2.2)
    # torso
    cv.save(); cv.scale(1, br)
    body = skia.Path(); body.moveTo(-170, 300); body.cubicTo(-330, 330, -390, 420, -400, 1100); body.lineTo(400, 1100)
    body.cubicTo(390, 420, 330, 330, 170, 300); body.close(); cv.drawPath(body, P(JACKET))
    tee = skia.Path(); tee.moveTo(-120, 300); tee.lineTo(0, 470); tee.lineTo(120, 300); tee.cubicTo(150, 420, 140, 600, 130, 1100)
    tee.lineTo(-130, 1100); tee.cubicTo(-140, 600, -150, 420, -120, 300); tee.close(); cv.drawPath(tee, P(TEE))
    vn = skia.Path(); vn.moveTo(-105, 300); vn.lineTo(0, 455); vn.lineTo(105, 300); cv.drawPath(vn, P(TEE_D, stroke=22))
    for sgn in (-1, 1):
        lap = skia.Path(); lap.moveTo(sgn * 125, 300); lap.cubicTo(sgn * 175, 420, sgn * 160, 560, sgn * 150, 1100)
        lap.lineTo(sgn * 205, 1100); lap.cubicTo(sgn * 220, 540, sgn * 220, 400, sgn * 175, 305); lap.close(); cv.drawPath(lap, P(JACKET_L))
    zp = skia.Path(); zp.moveTo(150, 480); zp.lineTo(150, 1100); cv.drawPath(zp, P((80, 76, 96), stroke=6))
    cv.restore()
    # waving arm (behind head layer, in front of body)
    if wave is not None:
        ang = 18 + 14 * math.sin(wave * 9)
        cv.save(); cv.translate(300, 420); cv.rotate(ang)
        arm = skia.Path(); arm.moveTo(0, 0); arm.lineTo(0, -330); cv.drawPath(arm, P(JACKET, stroke=120))
        cv.drawCircle(0, -400, 74, P(SKIN)); rrect(cv, -88, -430, -40, -380, 22, P(SKIN))
        for i in range(4): rrect(cv, -50 + i * 30, -510, -22 + i * 30, -430, 14, P(SKIN))
        cv.restore()
    # neck (thick)
    rrect(cv, -118, 140, 118, 340, 55, P(SKIN_D))
    nk = skia.Path(); nk.moveTo(-118, 230); nk.quadTo(0, 290, 118, 230); cv.drawPath(nk, P(SKIN_S, 70, stroke=10))
    cv.save(); cv.rotate(tilt)
    # back hair mass
    cv.drawOval(skia.Rect.MakeLTRB(-232, -345, 232, -10), P(HAIR))
    # ears
    for sgn in (-1, 1):
        cv.drawOval(skia.Rect.MakeLTRB(sgn * 212 - 40, -15, sgn * 212 + 40, 85), P(SKIN))
        cv.drawOval(skia.Rect.MakeLTRB(sgn * 212 - 20, 8, sgn * 212 + 20, 62), P(SKIN_S))
    head = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-214, -232, 214, 258), 205, 225)
    cv.drawRRect(head, P(SKIN))
    for sgn in (-1, 1): cv.drawCircle(sgn * 125, 62, 34, P(PINK, 22))
    # nose (symmetric)
    for sgn in (-1, 1): cv.drawCircle(sgn * 30, 72, 22, P(SKIN_S))
    cv.drawOval(skia.Rect.MakeLTRB(-30, 30, 30, 92), P(SKIN_S))
    for sgn in (-1, 1): cv.drawOval(skia.Rect.MakeLTRB(sgn * 22 - 10, 74, sgn * 22 + 10, 88), P(SKIN_D))
    br_ = skia.Path(); br_.moveTo(-8, -10); br_.quadTo(-14, 25, -10, 45); cv.drawPath(br_, P(SKIN_S, 200, stroke=8))
    # mouth
    if mouth == "o":
        cv.drawOval(skia.Rect.MakeLTRB(-24, 140, 24, 190), P((60, 20, 34)))
    elif mouth == "grin":
        m = skia.Path(); m.moveTo(-76, 140); m.cubicTo(-48, 210, 48, 210, 76, 140); m.close()
        cv.drawPath(m, P((70, 22, 38))); cv.save(); cv.clipPath(m, doAntiAlias=True)
        rrect(cv, -80, 130, 80, 160, 10, P(WHITE)); cv.restore()
    else:
        m = skia.Path(); m.moveTo(-58, 146); m.cubicTo(-32, 178, 32, 178, 58, 146)
        cv.drawPath(m, P((80, 26, 42), stroke=13))
    # eyes
    for sgn in (-1, 1):
        ex, ey = sgn * 90, -12
        closed = max(wink if sgn == 1 else 0.0, blink)
        if closed > 0.85:
            arc = skia.Path(); arc.moveTo(ex - 38, ey + 4); arc.quadTo(ex, ey - 24, ex + 38, ey + 4)
            cv.drawPath(arc, P(HAIR, stroke=11))
        else:
            cv.save(); cv.translate(ex, ey); cv.scale(1, max(.08, 1 - closed))
            eye = skia.Path(); eye.moveTo(-42, 4); eye.cubicTo(-28, -34, 28, -34, 42, 0); eye.cubicTo(28, 28, -28, 30, -42, 4); eye.close()
            cv.drawPath(eye, P(WHITE))
            cv.save(); cv.clipPath(eye, doAntiAlias=True)
            px, py = look[0] * 15, look[1] * 10
            cv.drawCircle(px, py, 21, P((70, 40, 28))); cv.drawCircle(px, py, 12, P(HAIR)); cv.drawCircle(px + 7, py - 7, 6, P(WHITE))
            cv.restore()
            lid = skia.Path(); lid.moveTo(-44, 4); lid.cubicTo(-28, -36, 28, -36, 44, 0); cv.drawPath(lid, P(HAIR, stroke=7))
            cv.restore()
        lift = brow * 18
        cv.save(); cv.translate(ex, ey - 66 - lift); cv.rotate(sgn * (4 + brow * 3))
        bp_ = skia.Path(); bp_.moveTo(-60 * sgn, 6); bp_.quadTo(0, -20, 60 * sgn, 0)
        cv.drawPath(bp_, P(HAIR, stroke=24)); cv.restore()
    # front hair: messy wavy volume, rounded silhouette, covers temples
    out = [(-222, -50), (-246, -105), (-238, -205), (-192, -292), (-118, -348), (-28, -370), (62, -364), (142, -334),
           (202, -278), (238, -195), (244, -100), (222, -50)]
    hp = skia.Path(); hp.moveTo(*out[0])
    for i, ((x0, y0), (x1, y1)) in enumerate(zip(out, out[1:])):
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2; dx, dy = mx, my + 120; d = math.hypot(dx, dy) or 1
        push = 20 + 8 * ((i * 7) % 3)
        hp.quadTo(mx + dx / d * push, my + dy / d * push, x1, y1)
    hp.cubicTo(215, -120, 190, -168, 140, -180); hp.cubicTo(90, -195, 30, -188, 0, -192)
    hp.cubicTo(-30, -188, -90, -195, -140, -180); hp.cubicTo(-190, -168, -215, -120, -222, -50); hp.close()
    cv.drawPath(hp, P(HAIR))
    HL = (64, 54, 80)
    for (x, y, w, ang) in [(-150, -250, 80, -35), (-60, -300, 90, -20), (40, -305, 90, -10), (130, -265, 80, 15),
                           (-170, -180, 60, -60), (175, -190, 60, 55), (-10, -225, 70, -5), (90, -215, 60, 10)]:
        cv.save(); cv.translate(x, y); cv.rotate(ang)
        wv = skia.Path(); wv.moveTo(-w / 2, 0); wv.cubicTo(-w / 4, -22, w / 4, 22, w / 2, 0); cv.drawPath(wv, P(HL, stroke=9))
        cv.restore()
    fl = skia.Path(); fl.moveTo(10, -192); fl.cubicTo(-30, -180, -40, -165, -70, -168)
    cv.drawPath(fl, P(HAIR, stroke=16))
    cv.restore()  # tilt
    if wave is not None:
        ang = 18 + 14 * math.sin(wave * 9)
        cv.save(); cv.translate(300, 420); cv.rotate(ang)
        arm = skia.Path(); arm.moveTo(0, 0); arm.lineTo(0, -330); cv.drawPath(arm, P(JACKET, stroke=120))
        cv.drawLine(-40, -40, -40, -300, P(JACKET_L, stroke=14))
        cv.drawCircle(0, -400, 74, P(SKIN)); rrect(cv, -96, -440, -46, -380, 24, P(SKIN))
        for i in range(4): rrect(cv, -50 + i * 32, -520, -20 + i * 32, -420, 15, P(SKIN))
        cv.restore()
    cv.restore()

def student(cv, x, y, s, t, typing=True):
    cv.save(); cv.translate(x, y); cv.scale(s, s)
    bob = 4 * math.sin(t * 18) if typing else 0
    HOOD = TEAL; HOOD_D = (44, 160, 156); SK = (240, 186, 150); HR = (110, 58, 36)
    body = skia.Path(); body.moveTo(-150, 210); body.cubicTo(-300, 240, -340, 320, -350, 520); body.lineTo(350, 520)
    body.cubicTo(340, 320, 300, 240, 150, 210); body.close(); cv.drawPath(body, P(HOOD))
    hd = skia.Path(); hd.moveTo(-170, 215); hd.cubicTo(-120, 300, 120, 300, 170, 215); cv.drawPath(hd, P(HOOD_D, stroke=30))
    rrect(cv, -55, 120, 55, 240, 30, P((214, 160, 128)))
    cv.save(); cv.translate(0, bob)
    cv.drawCircle(0, -150, 150, P(HR)); cv.drawCircle(0, -260, 62, P(HR))
    cv.drawCircle(-150, 10, 34, P(SK)); cv.drawCircle(150, 10, 34, P(SK))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-150, -170, 150, 175), 140, 160), P(SK))
    fr = skia.Path(); fr.moveTo(-150, -40); fr.cubicTo(-140, -190, 140, -200, 150, -40); fr.cubicTo(80, -110, -60, -120, -150, -40); fr.close()
    cv.drawPath(fr, P(HR))
    for sgn in (-1, 1):
        cv.drawOval(skia.Rect.MakeLTRB(sgn * 60 - 22, 10, sgn * 60 + 22, 44), P(WHITE))
        cv.drawCircle(sgn * 60, 34, 12, P(HAIR))
        rrect(cv, sgn * 60 - 32, -26, sgn * 60 + 32, -12, 7, P(HR))
    cv.drawCircle(-95, 75, 22, P(PINK, 50)); cv.drawCircle(95, 75, 22, P(PINK, 50))
    m = skia.Path(); m.moveTo(-22, 110); m.quadTo(0, 120, 22, 110); cv.drawPath(m, P((150, 70, 70), stroke=9))
    cv.restore(); cv.restore()

# ---------- props ----------
def room(cv, t):
    cv.clear(C(LILAC))
    for i in range(7): cv.drawRect(skia.Rect.MakeLTRB(-200 + i * 220, -400, -110 + i * 220, 1400), P(LILAC_D, 90))
    # window
    rrect(cv, 90, 260, 470, 760, 26, P(WHITE)); rrect(cv, 115, 285, 445, 735, 16, P(SKY))
    for cx, cy, sc in [(220, 420, 1), (360, 560, .8)]:
        cx += 20 * math.sin(t * .4)
        for dx, dy, rr in [(-40, 10, 38), (0, -10, 50), (45, 8, 40)]: cv.drawCircle(cx + dx * sc, cy + dy * sc, rr * sc, P(WHITE))
    cv.drawRect(skia.Rect.MakeLTRB(270, 285, 290, 735), P(WHITE)); cv.drawRect(skia.Rect.MakeLTRB(115, 500, 445, 520), P(WHITE))
    # frames and shelf
    rrect(cv, 640, 250, 820, 430, 14, P(PURP_L)); rrect(cv, 660, 270, 800, 410, 8, P(AMBER))
    cv.drawCircle(730, 340, 40, P(PINK))
    rrect(cv, 850, 300, 990, 440, 14, P(PURP_L)); rrect(cv, 868, 318, 972, 422, 8, P(MINT))
    rrect(cv, 620, 640, 1020, 668, 12, P(PURP_D))
    bx = 650
    for wdt, hgt, col in [(46, 150, PINK), (40, 130, AMBER), (52, 160, PURP), (38, 120, TEAL), (48, 140, NAVY)]:
        rrect(cv, bx, 640 - hgt, bx + wdt, 640, 8, P(col)); bx += wdt + 6
    pot = skia.Path(); pot.moveTo(930, 640); pot.lineTo(990, 640); pot.lineTo(980, 560); pot.lineTo(940, 560); pot.close()
    for i, (lx, ly, ang) in enumerate([(960, 520, -30), (930, 500, -60), (990, 505, 20), (960, 470, -5)]):
        cv.save(); cv.translate(lx, ly); cv.rotate(ang + 4 * math.sin(t * 1.3 + i))
        cv.drawOval(skia.Rect.MakeLTRB(-22, -60, 22, 60), P(MINT_D)); cv.restore()
    cv.drawPath(pot, P(PINK))

def desk_front(cv, t, lid=True):
    rrect(cv, -100, 1330, 1180, 1400, 20, P(PURP_L)); cv.drawRect(skia.Rect.MakeLTRB(-100, 1385, 1180, 2400), P(PURP))
    cv.drawRect(skia.Rect.MakeLTRB(-100, 1385, 1180, 1420), P(PURP_D))
    # laptop (back of lid)
    rrect(cv, 270, 1010, 810, 1350, 30, P((214, 210, 240))); rrect(cv, 270, 1320, 810, 1350, 16, P((190, 184, 226)))
    cv.drawCircle(540, 1170, 40, P(WHITE, 200)); cv.drawCircle(540, 1170, 18, P(PURP_L))
    # mug
    rrect(cv, 870, 1220, 990, 1340, 22, P(AMBER)); cv.drawCircle(995, 1280, 34, P(AMBER, 255)); cv.drawCircle(995, 1280, 18, P(PURP_L))
    for i in range(3):
        k = ((t * .7 + i / 3) % 1); a = int(160 * math.sin(k * math.pi))
        st = skia.Path(); x0 = 905 + i * 28; st.moveTo(x0, 1200 - k * 120); st.quadTo(x0 + 16, 1170 - k * 120, x0, 1140 - k * 120)
        cv.drawPath(st, P(WHITE, a, stroke=8))
    # books
    rrect(cv, 90, 1270, 250, 1300, 8, P(PINK)); rrect(cv, 105, 1240, 240, 1270, 8, P(TEAL)); rrect(cv, 95, 1300, 255, 1332, 8, P(NAVY))

def bubble(cv, cx, cy, w, h, scale, alpha, tail="down", fill=WHITE):
    if scale <= 0.01 or alpha <= 0: return
    cv.save(); cv.translate(cx, cy); cv.scale(scale, scale)
    if alpha < 255: cv.saveLayerAlpha(None, int(alpha))
    rrect(cv, -w / 2, -h / 2 + 16, w / 2, h / 2 + 16, 46, P(NAVY, 60, blur=8))
    rrect(cv, -w / 2, -h / 2, w / 2, h / 2, 46, P(fill))
    tl = skia.Path()
    if tail == "down": tl.moveTo(-60, h / 2 - 2); tl.lineTo(-10, h / 2 - 2); tl.lineTo(-80, h / 2 + 60); tl.close()
    cv.drawPath(tl, P(fill))
    if alpha < 255: cv.restore()
    cv.restore()

def shards(cv, t, seed, cx, cy, bw, bh, cols, n=70, power=1.0):
    if t <= 0 or t > 1.6: return
    r = np.random.default_rng(seed)
    for i in range(n):
        x0 = cx + r.uniform(-bw / 2, bw / 2); y0 = cy + r.uniform(-bh / 2, bh / 2)
        ang = math.atan2(y0 - cy, x0 - cx + 1e-3) + r.uniform(-.5, .5); spd = r.uniform(500, 1500) * power
        vx = math.cos(ang) * spd; vy = math.sin(ang) * spd - r.uniform(300, 900) * power
        x = x0 + vx * t; y = y0 + vy * t + 0.5 * 2600 * t * t
        a = 255 * clamp((1.5 - t) / .6); sz = r.uniform(8, 26) * (1 - .4 * t)
        rot = r.uniform(-1, 1) * 900 * t; col = cols[i % len(cols)]
        cv.save(); cv.translate(x, y); cv.rotate(rot)
        if i % 3 == 0: rrect(cv, -sz * 1.4, -sz * .35, sz * 1.4, sz * .35, sz * .35, P(col, a))
        else:
            tri = skia.Path(); tri.moveTo(0, -sz); tri.lineTo(sz * .9, sz * .7); tri.lineTo(-sz * .8, sz * .6); tri.close(); cv.drawPath(tri, P(col, a))
        cv.restore()

def burst_lines(cv, t, cx, cy, col, n=12, r0=90, r1=260):
    if t <= 0 or t >= 1: return
    k = ease(t)
    for i in range(n):
        a = i * 6.283 / n + .2
        s0 = r0 + (r1 - r0) * k * .6; s1 = r0 + (r1 - r0) * k
        cv.drawLine(cx + math.cos(a) * s0, cy + math.sin(a) * s0, cx + math.cos(a) * s1, cy + math.sin(a) * s1, P(col, 255 * (1 - t), stroke=14 * (1 - t) + 2))

def confetti(cv, t, seed, cx, cy, n=46):
    if t <= 0 or t > 2.2: return
    r = np.random.default_rng(seed); cols = [PINK, AMBER, MINT, WHITE, TEAL]
    for i in range(n):
        ang = r.uniform(-math.pi, 0); spd = r.uniform(600, 1400)
        x = cx + math.cos(ang) * spd * t + 40 * math.sin(t * 8 + i); y = cy + math.sin(ang) * spd * t + 1300 * t * t
        a = 255 * clamp((2.2 - t) / .7)
        cv.save(); cv.translate(x, y); cv.rotate(i * 40 + t * 600 * (1 if i % 2 else -1))
        rrect(cv, -12, -6, 12, 6, 4, P(cols[i % 5], a)); cv.restore()

def check_badge(cv, x, y, k):
    if k <= 0: return
    r = 62 * k
    cv.drawCircle(x, y + 8, r, P(NAVY, 60, blur=6)); cv.drawCircle(x, y, r, P(MINT_D))
    if k > .5:
        p = skia.Path(); p.moveTo(x - 26 * k, y + 2); p.lineTo(x - 6 * k, y + 22 * k); p.lineTo(x + 30 * k, y - 20 * k)
        cv.drawPath(p, P(WHITE, stroke=13))

def slab(cv, cx, cy, txt, f, bg, fg, k, rot, padx=60, pady=34):
    if k <= 0: return
    w = f.measureText(txt) + padx * 2; m = f.getMetrics(); h = (m.fDescent - m.fAscent) * .78 + pady * 2
    sc = lerp(2.3, 1.0, spring(k)); a = 255 * clamp(k * 4)
    cv.save(); cv.translate(cx, cy); cv.rotate(rot); cv.scale(sc, sc)
    cv.saveLayerAlpha(None, int(a))
    cv.drawRect(skia.Rect.MakeLTRB(-w / 2 + 14, -h / 2 + 16, w / 2 + 14, h / 2 + 16), P(NAVY, 90))
    cv.drawRect(skia.Rect.MakeLTRB(-w / 2, -h / 2, w / 2, h / 2), P(bg))
    text(cv, txt, 0, 0, f, fg)
    cv.restore(); cv.restore()

def flat_bg(cv, col, col2, t, seed=1):
    cv.clear(C(col)); r = np.random.default_rng(seed)
    for i in range(6):
        x = r.uniform(0, W); y = r.uniform(0, H); rr = r.uniform(140, 380)
        cv.drawCircle(x + 30 * math.sin(t * .5 + i), y + 40 * math.cos(t * .4 + i), rr, P(col2))
    for i in range(18):
        x = (r.uniform(0, W) + t * r.uniform(-40, 40)) % W; y = (r.uniform(0, H) - t * r.uniform(20, 70)) % H
        cv.save(); cv.translate(x, y); cv.rotate(r.uniform(0, 180) + t * 20)
        rrect(cv, -20, -6, 20, 6, 6, P(WHITE, 90)); cv.restore()

def pill(cv, cx, cy, txt, f, bg, fg, k):
    if k <= 0: return
    w = f.measureText(txt) + 80; h = 86; s = lerp(.5, 1, spring(k))
    cv.save(); cv.translate(cx, cy); cv.scale(s, s); cv.saveLayerAlpha(None, int(255 * clamp(k * 3)))
    rrect(cv, -w / 2, -h / 2 + 10, w / 2, h / 2 + 10, h / 2, P(NAVY, 70, blur=5))
    rrect(cv, -w / 2, -h / 2, w / 2, h / 2, h / 2, P(bg)); text(cv, txt, 0, 2, f, fg)
    cv.restore(); cv.restore()

def progress(cv, gt, total):
    rrect(cv, 60, 64, W - 60, 76, 6, P(NAVY, 70)); rrect(cv, 60, 64, 60 + (W - 120) * clamp(gt / total), 76, 6, P(WHITE))

def speedlines(cv, k, seed=4):
    if k <= 0: return
    r = np.random.default_rng(seed)
    for i in range(26):
        y = r.uniform(0, H); x = r.uniform(-200, W); ln = r.uniform(200, 700)
        cv.drawLine(x, y, x + ln, y, P(WHITE, 200 * k, stroke=r.uniform(4, 14)))

# ---------- scenes ----------
CFGS = {
 "agree": dict(words=["I", "am", "agree"], rm=1, size=100, bw=720, pill="English tip", slam1=("AGREE", 200), mid=["is", "already", "a"],
               slam2=("VERB", 170), sub="So: no \u201cam\u201d needed.", out="i_agree_cartoon"),
 "discuss": dict(words=["Let\u2019s", "discuss", "about", "it."], rm=2, size=80, bw=940, pill="IELTS Writing tip", slam1=("DISCUSS", 165),
                 mid=["already", "means"], slam2=("TALK ABOUT", 118), sub="So: no \u201cabout\u201d needed.", out="discuss_about_cartoon"),
}
CFG = CFGS[os.environ.get("REEL", "agree")]
WORDS = CFG["words"]; RM = CFG["rm"]; MSG = " ".join(WORDS)
F_MSG = font("Bold", CFG["size"]); BW = CFG["bw"]
def blink_at(t, every=2.7, off=0.3):
    ph = (t + off) % every
    return clamp(1 - abs(ph - .08) / .08) if ph < .16 else 0.0

def scene1(cv, t, gt):  # room, student types the mistake (3.4 s)
    z = lerp(1.22, 1.0, eio(prog(t, 0, 1.4))); oy = lerp(-160, 0, eio(prog(t, 0, 1.4)))
    wx = -1300 * eio(prog(t, 3.1, .3)) ** 2
    cv.save(); cv.translate(W / 2 + wx, H / 2); cv.scale(z, z); cv.translate(-W / 2, -H / 2 + oy)
    room(cv, gt); student(cv, 540, 860, .78, t); desk_front(cv, gt)
    k = prog(t, .7, .35)
    bubble(cv, 540, 560, BW, 190, lerp(.4, 1, spring(k)), 255 * clamp(k * 3))
    if 0.9 < t < 1.4:
        for i in range(3):
            j = .5 + .5 * math.sin(t * 14 - i * .9); cv.drawCircle(480 + i * 60, 560 - 12 * j, 16, P(NAVY, 120 + 120 * j))
    n = int(clamp((t - 1.4) / .9) * len(MSG))
    if n > 0:
        full = F_MSG.measureText(MSG); x0 = 540 - full / 2
        text(cv, MSG[:n], x0, 562, F_MSG, NAVY, align="left")
        if n < len(MSG) and (t * 3) % 1 < .6:
            cx = x0 + F_MSG.measureText(MSG[:n]) + 8; rrect(cv, cx, 520, cx + 8, 604, 4, P(PINK))
    cv.restore()
    pill(cv, W / 2, 230, CFG["pill"], font("Bold", 42), NAVY, WHITE, prog(t, .25, .5))
    speedlines(cv, prog(t, 3.1, .3))

def layout(gap_k):
    sp = F_MSG.measureText(" "); ws = [F_MSG.measureText(w) for w in WORDS]
    before = sum(ws) + sp * (len(ws) - 1); after = before - ws[RM] - sp
    xb, xa, x, y = [], [], 540 - before / 2, 540 - after / 2
    for i, w in enumerate(ws):
        xb.append(x); x += w + sp
        if i != RM: xa.append(y); y += w + sp
        else: xa.append(None)
    pos = [lerp(xb[i], xa[i], gap_k) if i != RM else xb[i] for i in range(len(ws))]
    return pos, ws

def scene2(cv, t, gt):  # Jak reacts, "am" shatters (3.2 s)
    wx = 1300 * (1 - eio(prog(t, 0, .3))) ** 2
    sh = 0
    if 1.35 <= t < 1.7: sh = 18 * math.sin(t * 90) * (1.7 - t) / .35
    cv.save(); cv.translate(wx + sh, sh * .6)
    flat_bg(cv, PURP, PURP_L, gt, 2)
    look = (0, -1) if t > .6 else (0, 0)
    brow = ease(prog(t, .6, .3)) * (1 - ease(prog(t, 1.9, .3)))
    mouth = "o" if .65 < t < 1.35 else ("grin" if t >= 1.9 else "smile")
    tilt = 6 * math.sin(clamp((t - 1.9) / .5) * math.pi) if t > 1.9 else 0
    pop = back(prog(t, .1, .5))
    jak(cv, 540, 1060 + (1 - pop) * 500, 1.0, gt, look=look, brow=brow, mouth=mouth, blink=blink_at(t), tilt=tilt)
    k = prog(t, .2, .35); bk = clamp(k * 3)
    green = ease(prog(t, 1.9, .3))
    bubble(cv, 540, 470, BW + 40, 200, lerp(.4, 1, spring(k)), 255 * bk, fill=mixc(WHITE, (226, 255, 242), green))
    if bk > 0:
        gap = eio(prog(t, 1.45, .45))
        pos, ws = layout(gap)
        col = mixc(NAVY, MINT_D, green)
        cv.save(); cv.translate(540, 470); cv.scale(lerp(.4, 1, spring(k)), lerp(.4, 1, spring(k))); cv.translate(-540, -470)
        for i, w in enumerate(WORDS):
            if i != RM: text(cv, w, pos[i], 472, F_MSG, col, align="left")
        xam, fam = pos[RM], ws[RM]
        if t < 1.3:
            wob = 4 * math.sin(t * 50) if t > .9 else 0
            if t > .7:
                rrect(cv, xam - 10, 425, xam + fam + 10, 519, 18, P(PINK, 70 * ease(prog(t, .7, .2))))
            text(cv, WORDS[RM], xam + wob, 472, F_MSG, PINK if t > .7 else NAVY, align="left")
        cv.restore()
        shards(cv, t - 1.3, 11, xam + fam / 2, 470, fam, 90, [PINK, NAVY, AMBER, PINK], n=80)
        burst_lines(cv, (t - 1.3) / .45, xam + fam / 2, 470, AMBER)
        check_badge(cv, min(540 + BW / 2, 960), 385, back(prog(t, 1.95, .4)))
        confetti(cv, t - 1.95, 5, 540, 420)
    cv.restore()

def scene3(cv, t, gt):  # block slams (2.8 s)
    sh = 0
    for a in (.15, .85):
        if a <= t < a + .3: sh += 16 * math.sin(t * 95) * (a + .3 - t) / .3
    cv.save(); cv.translate(sh, sh * .5)
    flat_bg(cv, MINT, (134, 238, 198), gt, 3)
    slab(cv, 540, 700, CFG["slam1"][0], font("Bold", CFG["slam1"][1]), NAVY, WHITE, prog(t, .05, .35), -4)
    shards(cv, t - .2, 21, 540, 700, 700, 200, [NAVY, PINK, WHITE], n=36, power=.7)
    k = prog(t, .45, .35)
    if k > 0:
        f = font("Bold", 74); words = CFG["mid"]
        ws = [f.measureText(w) for w in words]; sp = f.measureText(" "); x = 540 - (sum(ws) + sp * 2) / 2
        for i, w in enumerate(words):
            kk = prog(t, .45 + i * .1, .35)
            if kk > 0:
                cv.save(); s = lerp(1.6, 1, spring(kk)); cv.translate(x + ws[i] / 2, 900 + (1 - ease(kk)) * 30); cv.scale(s, s)
                text(cv, w, 0, 0, f, NAVY, 255 * clamp(kk * 3)); cv.restore()
            x += ws[i] + sp
    slab(cv, 540, 1080, CFG["slam2"][0], font("Bold", CFG["slam2"][1]), PINK, WHITE, prog(t, .75, .35), 3)
    shards(cv, t - .9, 31, 540, 1080, 520, 180, [PINK, NAVY, AMBER], n=36, power=.7)
    k = prog(t, 1.5, .4)
    if k > 0:
        f = font("Medium", 58); s = lerp(.6, 1, spring(k))
        cv.save(); cv.translate(540, 1290); cv.scale(s, s)
        text(cv, CFG["sub"], 0, 0, f, NAVY, 255 * clamp(k * 3)); cv.restore()
    cv.restore()
    wx = -1300 * eio(prog(t, 2.5, .3)) ** 2
    if wx < -1:  # whip out
        cv.save(); cv.translate(wx + 1300, 0); flat_bg(cv, PURP, PURP_L, gt, 2); cv.restore()
        speedlines(cv, prog(t, 2.5, .3))

def scene4(cv, t, gt):  # outro wave + wink (3.6 s)
    flat_bg(cv, PURP, PURP_L, gt, 2)
    wink = 1.0 if 1.5 <= t < 2.4 else 0.0
    wave = t if .3 < t < 2.0 else None
    pop = back(prog(t, 0, .45))
    jak(cv, 540, 1090 + (1 - pop) * 400, .95, gt, look=(0, 0), brow=.3 if wink else 0, mouth="grin" if t > .3 else "smile",
        blink=blink_at(t, 3.3, 1.0) if not wink else 0, wink=wink, wave=wave, tilt=-4 * wink)
    if 1.5 <= t < 2.3:
        k = (t - 1.5) / .8
        for i in range(5):
            a = -2.4 + i * .35; rr = 120 + 80 * ease(k); x = 640 + math.cos(a) * rr; y = 990 + math.sin(a) * rr; s = 18 * (1 - k)
            st = skia.Path(); st.moveTo(x, y - s); st.lineTo(x + s * .3, y - s * .3); st.lineTo(x + s, y); st.lineTo(x + s * .3, y + s * .3)
            st.lineTo(x, y + s); st.lineTo(x - s * .3, y + s * .3); st.lineTo(x - s, y); st.lineTo(x - s * .3, y - s * .3); st.close()
            cv.drawPath(st, P(AMBER))
    slab(cv, 540, 250, "TEACHER JAK", font("Bold", 92), NAVY, WHITE, prog(t, .1, .35), -2)
    k = prog(t, .6, .4)
    if k > 0:
        f = font("Bold", 52); w = f.measureText(os.environ.get("OUTRO", "Follow for a daily English fix")) + 90; s = lerp(.6, 1, spring(k))
        cv.save(); cv.translate(540, 420); cv.scale(s, s); cv.saveLayerAlpha(None, int(255 * clamp(k * 3)))
        rrect(cv, -w / 2, -52, w / 2, 60, 56, P(NAVY, 70, blur=6)); rrect(cv, -w / 2, -56, w / 2, 56, 56, P(WHITE))
        text(cv, os.environ.get("OUTRO", "Follow for a daily English fix"), 0, 2, f, NAVY); cv.restore(); cv.restore()
    k = prog(t, 1.0, .4)
    if k > 0: text(cv, "@ieltswithteacherjak", 540, 530, font("Medium", 46), WHITE, 255 * ease(k))

SCENES = [(scene1, 3.4), (scene2, 3.3), (scene3, 2.8), (scene4, 3.6)]
STARTS = np.cumsum([0] + [d for _, d in SCENES])[:-1]; TOTAL = sum(d for _, d in SCENES)

def draw(gt):
    surf = skia.Surface(W, H); cv = surf.getCanvas()
    for i, (fn, d) in enumerate(SCENES):
        if gt < STARTS[i] + d or i == len(SCENES) - 1:
            fn(cv, gt - STARTS[i], gt); break
    progress(cv, gt, TOTAL)
    return surf.makeImageSnapshot().toarray()

def render(a, b, path):
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", path + ".tmp.mp4"], stdin=subprocess.PIPE)
    for i in range(a, b): p.stdin.write(draw(i / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.rename(path + ".tmp.mp4", path)

def sound(out):
    sys.path.insert(0, "/home/claude/reel"); import music_kit as mk
    from scipy.io import wavfile
    SR = mk.SR; bed = np.load("/home/claude/reel/bed.npy"); n = int(TOTAL * SR); sfx = np.zeros(len(bed))
    rng = np.random.default_rng(9)
    def add(sig, t0):
        i = int(t0 * SR); j = min(len(sfx), i + len(sig))
        if 0 <= i < len(sfx): sfx[i:j] += sig[: j - i]
    def thump(t0, g=.5):
        tt = mk.T(.35); f = 55 + 120 * np.exp(-tt * 30); add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 10) * g, t0)
    def burst(t0):
        tt = mk.T(.6); add(mk.bp(rng.standard_normal(len(tt)), 1200, 7000) * np.exp(-tt * 8) * .22, t0); thump(t0, .45)
        for k in range(10):
            m = 84 + rng.integers(-5, 8); add(mk.bell(int(m), .25) * .05, t0 + .02 + k * .03)
    def swish(t0):
        tt = mk.T(.45); add(mk.bp(rng.standard_normal(len(tt)), 700, 3500) * np.sin(np.pi * tt / tt[-1]) ** 2 * .09, t0 - .2)
    def tick(t0): tt = mk.T(.05); add(np.sin(2 * np.pi * 1300 * tt) * np.exp(-tt * 80) * .08, t0)
    def popsnd(t0):
        tt = mk.T(.12); f = 500 + 1400 * tt / .12; add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 30) * .2, t0)
    def chime(t0, notes, g=.15):
        for k, m in enumerate(notes): add(mk.bell(m, .9) * g, t0 + k * .07)
    s1, s2, s3, s4 = STARTS
    chime(s1 + .25, [72, 79], .1); popsnd(s1 + .7)
    for i in range(len(MSG)): tick(s1 + 1.4 + i * .9 / len(MSG))
    swish(s2); popsnd(s2 + .2)
    for m, dt in ((62, 0), (58, .14)): tt = mk.T(.35); add(np.sin(2 * np.pi * mk.hz(m) * tt) * np.exp(-tt * 9) * .18, s2 + .75 + dt)
    burst(s2 + 1.3); chime(s2 + 1.95, [76, 79, 84])
    thump(s3 + .15, .6); thump(s3 + .85, .6); swish(s3 + 2.6)
    popsnd(s4 + .1); chime(s4 + 1.5, [84, 88, 91, 96], .12)
    mix = (bed + sfx)[:n]; fi = int(.4 * SR); mix[:fi] *= np.linspace(0, 1, fi)
    fo = int(1.2 * SR); mix[-fo:] *= np.linspace(1, 0, fo); mix /= np.max(np.abs(mix)) * 1.12
    L = mix.copy(); R = mix.copy(); d = int(.015 * SR); R[d:] = .75 * mix[:-d] + .25 * mix[d:]
    wavfile.write(out, SR, (np.stack([L, R], 1) * 32767).astype(np.int16))

if __name__ == "__main__":
    out = "/home/claude/reel/cartoon"; os.makedirs(out, exist_ok=True)
    mode = sys.argv[1]
    if mode == "stills":
        from PIL import Image
        ts = [float(x) for x in sys.argv[2].split(",")]
        ims = [Image.fromarray(draw(t)[:, :, [2, 1, 0]]).resize((270, 480)) for t in ts]
        c = Image.new("RGB", (270 * len(ims), 480)); [c.paste(im, (i * 270, 0)) for i, im in enumerate(ims)]; c.save(f"{out}/contact.png")
        if len(sys.argv) > 3: Image.fromarray(draw(float(sys.argv[3]))[:, :, [2, 1, 0]]).save(f"{out}/full.png")
    elif mode == "part":
        a, b, k = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]; render(a, b, f"{out}/part{k}.mp4")
    elif mode == "final":
        N = int(round(TOTAL * FPS)); print(N)
