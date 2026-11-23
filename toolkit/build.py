"""Usage:
  python3 build.py WEEK_MODULE NAME stills          # key-frame contact sheet
  python3 build.py WEEK_MODULE NAME scene IDX       # render one scene
  python3 build.py WEEK_MODULE NAME final           # music + join -> out/NAME/NAME.mp4
WEEK_MODULE is a file in weeks/ (without .py) defining REELS = {name: [scenes]}.
"""
import sys, os, subprocess, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "weeks"))
from reelkit import render_scene, frame, sfx_events
import music_kit
mod, name, mode = sys.argv[1], sys.argv[2], sys.argv[3]
sc = importlib.import_module(mod).REELS[name]
out = os.path.join(HERE, "out", name); os.makedirs(out, exist_ok=True)
if mode == "stills":
    from PIL import Image
    ims = [frame(sc, i, s[1] - 0.4).resize((270, 480)) for i, s in enumerate(sc)]
    c = Image.new("RGB", (270 * len(ims), 480)); [c.paste(im, (k * 270, 0)) for k, im in enumerate(ims)]
    c.save(f"{out}/contact.png")
elif mode == "scene":
    render_scene(sc, int(sys.argv[4]), out)
elif mode == "final":
    ev, total = sfx_events(sc)
    music_kit.make(ev, total, f"{out}/music.wav")
    with open(f"{out}/list.txt", "w") as f:
        for i in range(len(sc)): f.write(f"file 'scene{i}.mp4'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{out}/list.txt", "-c", "copy", f"{out}/video.mp4"], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{out}/video.mp4", "-i", f"{out}/music.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
        "-af", "acompressor=threshold=-22dB:ratio=2.5:attack=10:release=150:makeup=3,alimiter=limit=0.8:level=disabled,volume=-1.5dB",
        "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", f"{out}/{name}.mp4"], check=True)
    print(name, round(total, 1), "s")
