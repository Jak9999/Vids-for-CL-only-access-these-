# Teacher Jak Reel toolkit

Makes the branded IELTS/English-tip Reels for @ieltswithteacherjak.

- `reelkit.py` – purple brand template and scene builders: `intro`, `wrong`, `right`, `items`, `quiz`, `quiz_reveal`, `outro` (avatar bounce-in, corner badge, wink outro).
- `music_bed.py` – regenerates the fixed lo-fi track (`bed.npy`, deterministic). Run once per fresh machine.
- `music_kit.py` – cuts the track to each Reel and adds the sound effects (hello, swish, wrong, right, tick, wink).
- `build.py` – renders a Reel from a week file in `weeks/`.
- `assets/` – round avatar images (smile + wink).

Setup: `pip install numpy scipy pillow`, plus ffmpeg and the Poppins font.

    python3 music_bed.py
    python3 build.py week_2026_11_24 2026-11-25-discuss stills
    for i in 0 1 2 3 4; do python3 build.py week_2026_11_24 2026-11-25-discuss scene $i; done
    python3 build.py week_2026_11_24 2026-11-25-discuss final

Finished videos go in `../reels/YYYY-MM-DD-topic.mp4`, then into Metricool via their raw.githubusercontent.com link.
