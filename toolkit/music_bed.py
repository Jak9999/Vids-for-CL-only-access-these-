import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

SR = 44100
BPM = 82
BEAT = 60 / BPM
BAR = 4 * BEAT
LEN = 40.0
N = int((LEN + 2) * SR)
BARS = int(np.ceil(LEN / BAR)) + 1
SWING = 0.62  # position of the off-beat 8th within a beat
rng = np.random.default_rng(23)

def hz(m): return 440 * 2 ** ((m - 69) / 12)
def lp(x, f): return sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
def hp(x, f): return sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], "band", fs=SR, output="sos"), x)
def T(d): return np.arange(int(d * SR)) / SR
def add(buf, sig, t):
    i = int(t * SR); j = min(len(buf), i + len(sig))
    if 0 <= i < len(buf): buf[i:j] += sig[: j - i]
def eighth(beat, off):  # swung 8th position
    return beat * BEAT + (SWING * BEAT if off else 0)

def rhodes(m, d, vel=1.0):
    t = T(d); f = hz(m)
    idx = 1.8 * vel * np.exp(-t * 3)
    mod = np.sin(2 * np.pi * f * t) * idx
    s = np.sin(2 * np.pi * f * t + mod) + 0.25 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 6)
    env = np.minimum(1, t / .006) * np.exp(-t * 0.9) * np.minimum(1, (d - t) / .15)
    trem = 1 - 0.18 * (0.5 + 0.5 * np.sin(2 * np.pi * 4.2 * t))
    return s * env * trem * vel

keys = np.zeros(N); bass = np.zeros(N); drums = np.zeros(N); mel = np.zeros(N); sfx = np.zeros(N)

# jazzy lo-fi progression: Cmaj9 - Am9 - Dm9 - G13
chords = [[48, 55, 59, 62, 64], [45, 52, 55, 59, 60], [50, 57, 60, 64, 65], [43, 53, 57, 59, 64]]
roots = [36, 33, 38, 31]
for b in range(BARS):
    c = chords[b % 4]; t0 = b * BAR
    # chord hit on 1 (slightly strummed), soft re-hit on the swung "and" of 2
    for k, m in enumerate(c):
        add(keys, rhodes(m, BAR * 0.95, 0.8 + 0.2 * rng.random()), t0 + k * 0.012)
    for k, m in enumerate(c[1:]):
        add(keys, rhodes(m, BEAT * 1.4, 0.45), t0 + eighth(1, True) + k * 0.01)
    # warm sine sub bass
    for st, ln in [(0, 1.5), (eighth(2, True) / BEAT, 1.2)]:
        d = ln * BEAT; t = T(d); r = roots[b % 4]
        s = np.sin(2 * np.pi * hz(r) * t) + 0.2 * np.sin(2 * np.pi * hz(r + 12) * t)
        add(bass, s * np.minimum(1, t / .02) * np.exp(-t * 1.2) * np.minimum(1, (d - t) / .05), t0 + st * BEAT)

def kick():
    t = T(.35); f = 45 + 60 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
def snare():
    t = T(.3)
    nz = bp(rng.standard_normal(len(t)), 600, 3500) * np.exp(-t * 16)
    body = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 30)
    return lp(0.6 * nz + 0.4 * body, 4000)
def hat(v):
    t = T(.06); return hp(rng.standard_normal(len(t)), 6500) * np.exp(-t * 60) * v

K, S = kick(), snare()
duck = np.ones(N)
for b in range(BARS):
    t0 = b * BAR
    for pos in (eighth(0, False), eighth(1, True) + BEAT * 0.0 if False else eighth(2, False) - 0.0, eighth(2, True)):
        pass
    kick_pos = [eighth(0, False), eighth(1, True), eighth(2, True)] if b % 2 else [eighth(0, False), eighth(2, False), eighth(2, True)]
    for p in kick_pos:
        add(drums, K * 0.9, t0 + p)
        i = int((t0 + p) * SR); n = min(int(.25 * SR), N - i)
        if n > 0: duck[i:i + n] = np.minimum(duck[i:i + n], 0.7 + 0.3 * np.linspace(0, 1, n))
    for beat in (1, 3):
        add(drums, S * 0.55, t0 + beat * BEAT + 0.012)  # laid-back snare
    for beat in range(4):
        for off in (False, True):
            add(drums, hat(0.09 if off else 0.13), t0 + eighth(beat, off))

# gentle melody: soft bell/pluck, sparse, enters after the hook scene
def bell(m, d):
    t = T(d); f = hz(m)
    s = np.sin(2 * np.pi * f * t + 0.6 * np.sin(2 * np.pi * f * 3.5 * t) * np.exp(-t * 5))
    return s * np.minimum(1, t / .004) * np.exp(-t * 2.5)
melody = [(0, 76, 1), (0.62, 79, 1), (1.62, 81, 1.5), (3, 79, 1),
          (4, 76, 1.5), (5.62, 74, 1), (6.62, 72, 2),
          (8, 76, 1), (8.62, 79, 1), (9.62, 84, 1.5), (11, 81, 1),
          (12, 79, 1.5), (13.62, 76, 1), (14.62, 74, 2)]
start = BAR
for st, m, ln in melody:
    add(mel, bell(m, ln * BEAT + 0.6), start + st * BEAT)
mel_e = mel.copy(); dl = int(BEAT * 0.75 * SR)
mel_e[dl:] += 0.35 * mel[:-dl]; mel_e[2 * dl:] += 0.15 * mel[:-2 * dl]

# soft sfx synced to visuals
def soft_wrong(t0):  # two descending muted tones
    for m, dt in ((62, 0), (58, .14)):
        t = T(.35); s = np.sin(2 * np.pi * hz(m) * t) * np.exp(-t * 9)
        add(sfx, s * 0.22, t0 + dt)
def soft_right(t0):  # warm rising chime
    for m, dt in ((76, 0), (79, .08), (84, .16)):
        add(sfx, bell(m, .9) * 0.16, t0 + dt)
def swish(t0):
    t = T(.5); s = bp(rng.standard_normal(len(t)), 800, 3000) * np.sin(np.pi * t / t[-1]) ** 2
    add(sfx, s * 0.05, t0 - .25)
def tick(t0):
    t = T(.05); add(sfx, np.sin(2 * np.pi * 1200 * t) * np.exp(-t * 80) * 0.08, t0)

# lo-fi texture: vinyl crackle and hiss
crackle = np.zeros(N)
for _ in range(int(LEN * 18)):
    i = rng.integers(0, N - 200)
    crackle[i:i + 30] += rng.standard_normal(30) * np.exp(-np.arange(30) / 5) * rng.uniform(.1, .6)
crackle = hp(crackle, 1500) * 0.10 + lp(rng.standard_normal(N), 4000) * 0.006

music = 0.18 * keys * duck + 0.30 * bass + 0.45 * drums + 0.09 * mel_e
music = lp(music, 5200)                     # dark, warm top end
# tape wow: slow pitch wobble
t = np.arange(N) / SR
warp = t + 0.0022 * np.sin(2 * np.pi * 0.55 * t) + 0.0007 * np.sin(2 * np.pi * 3.1 * t)
music = np.interp(warp, t, music)
music = np.tanh(music * 1.2)

import os
np.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bed.npy"), (music + crackle)[: int(LEN * SR)].astype(np.float32))
print("bed ok")
