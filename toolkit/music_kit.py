import numpy as np, sys, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
from scipy.signal import butter, sosfilt
from scipy.io import wavfile
SR = 44100
rng = np.random.default_rng(5)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def bp(x, a, b): return sosfilt(butter(2, [a, b], "band", fs=SR, output="sos"), x)
def T(d): return np.arange(int(d * SR)) / SR
def bell(m, d):
    t = T(d); f = hz(m)
    s = np.sin(2 * np.pi * f * t + 0.6 * np.sin(2 * np.pi * f * 3.5 * t) * np.exp(-t * 5))
    return s * np.minimum(1, t / .004) * np.exp(-t * 2.5)
def make(events, total, out):
    bed = np.load(os.path.join(HERE, "bed.npy"))
    n = int(total * SR); sfx = np.zeros(len(bed))
    def add(sig, t0):
        i = int(t0 * SR); j = min(len(sfx), i + len(sig))
        if 0 <= i < len(sfx): sfx[i:j] += sig[: j - i]
    for t0, k in events:
        if k == "swish":
            t = T(.5); add(bp(rng.standard_normal(len(t)), 800, 3000) * np.sin(np.pi * t / t[-1]) ** 2 * 0.05, t0 - .25)
        elif k == "wrong":
            for m, dt in ((62, 0), (58, .14)):
                t = T(.35); add(np.sin(2 * np.pi * hz(m) * t) * np.exp(-t * 9) * 0.22, t0 + dt)
        elif k == "right":
            for m, dt in ((76, 0), (79, .08), (84, .16)): add(bell(m, .9) * 0.16, t0 + dt)
        elif k == "tick":
            t = T(.05); add(np.sin(2 * np.pi * 1200 * t) * np.exp(-t * 80) * 0.08, t0)
        elif k == "wink":
            for m, dt in ((84, 0), (88, .06), (91, .12), (96, .2)): add(bell(m, .8) * 0.13, t0 + dt)
        elif k == "hello":
            for m, dt in ((72, 0), (79, .07)): add(bell(m, .5) * 0.10, t0 + dt)
    mix = (bed + sfx)[:n]
    fi = int(.5 * SR); mix[:fi] *= np.linspace(0, 1, fi)
    fo = int(1.5 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
    mix /= np.max(np.abs(mix)) * 1.12
    L = mix.copy(); R = mix.copy(); d = int(.015 * SR)
    R[d:] = 0.75 * mix[:-d] + 0.25 * mix[d:]
    wavfile.write(out, SR, (np.stack([L, R], 1) * 32767).astype(np.int16))
