# Poster Gaze Explorer

A local website showing where people looked on 15 graphic-design posters:
attention clusters, heatmaps, real-time gaze replays for one participant or the
whole group, and a side-by-side comparison of all posters.

## Start it

**Windows:** double-click `test_website/start_website.bat`. It starts the
website and opens it in your browser. Keep that window open while you use the
site; close it to stop.

**Any system**, from the repository root:

```
pip install flask numpy pandas scipy scikit-learn pillow
python test_website/app.py --open
```

The site runs at <http://127.0.0.1:5000>. The first start reads every
participant's recordings from `Renamed Signals/` (about a minute) and caches
them in `test_website/_cache/`, so later starts take seconds. If the recordings
change, add `--rebuild-cache`.

If the website is already running, a second start says so and exits instead of
starting another copy. Use the one that is running, or close its window first.

## Demo-day checklist

1. Start the site a few minutes early. It prepares the all-poster comparison in
   the background and prints *Comparison of all posters is ready* when done.
2. Switch to the light theme (☾ button, top right) if the projector washes out
   dark colours. The choice is remembered.
3. Press **P** (or *Present*) to hide the settings so the poster fills the screen.
4. Keyboard: **← / →** previous / next poster, **1 2 3** Clusters / Heatmap /
   Gaze replay, **Space** play / pause the replay, **C** compare all posters.
5. A link can open a particular view, which is handy for bookmarks, e.g.
   `http://127.0.0.1:5000/#poster=nancy_poster&view=replay&who=average&t=6`
   (`who` is a participant such as `p12`, or `average`; add `&present=1` for
   present mode; `#page=compare` opens the comparison).

## What it shows

1. **Pick a poster** at the top. It opens clustered with the default settings
   (the same as `demo.py`).
2. **Change the clustering** in the left panel, then *Run clustering* (or tick
   *Re-run automatically*).
   - **Hierarchical**: linkage, and either *Auto* k (searches a k range and picks
     the largest k whose combined score is within the tolerance of the best, as
     in `python/clustering.py`) or a *Fixed* k.
   - **DBSCAN**: `eps` (neighbourhood radius in poster pixels) and `min_samples`.
3. **Compare settings**: every run is listed with its silhouette (higher is
   better), Davies-Bouldin (lower is better) and Calinski-Harabasz (higher is
   better) scores; the best of each is highlighted. Click a run to show it.
4. **Three views of the chosen run:**
   - **Clusters**: outlines, fixation points, and each region's contents, share
     of viewing time and share of first looks.
   - **Heatmap**: fixation time for everyone or one participant, for the whole
     viewing or only the first few seconds.
   - **Gaze replay**: one participant's recorded gaze in real time, with the
     region they looked at first, the one they looked at longest, the regions in
     the order they first saw them, and their full path. **All participants
     (average)** shows the group's heatmap building up over time, with regions
     numbered in the order the group reached them (average time of each
     person's first look, as in `output/eye_tracking_analysis.R`).
5. **Compare all posters**: for every poster, the most-viewed region, the region
   looked at first, the group's order and the split of viewing time between
   text, images, shapes and background, plus a written summary. It uses the
   default settings, or your own where you changed them in the explorer.

## What a region contains

`poster_content.json` lists what is where on each poster (text, images and
shapes, each with a short label and boxes in percent of the poster) and the
poster names the site shows. A region's content is the element its fixation
time falls on most. Where boxes overlap the smallest wins, so text printed on a
shape counts as text; anything outside every box is background. The boxes were
drawn by hand from the poster images, so adjust them if a label looks wrong.
The site picks up edits without a restart.

## How it fits with the rest of the repository

- Clustering is `python/clustering.py`, the same code as `demo.py` and
  `python/make_cluster_animations.py`, so the numbers match theirs.
- Poster list, default settings and data loading come from
  `python/make_cluster_animations.py` (`PARAMS`).
- `app.py` is the server; `static/` holds the page (`index.html`, `app.js`,
  `style.css`). The page draws everything itself, so changing a setting does not
  require rendering a GIF.
