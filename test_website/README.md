# Poster Cluster Explorer

A small local website for trying clustering settings on each poster and seeing
the result as clusters, a heatmap and a real gaze replay.

## Run it

From the repository root:

```
pip install flask numpy pandas scipy scikit-learn pillow
python test_website/app.py
```

Then open <http://127.0.0.1:5000>. Stop it with Ctrl+C.

The first start reads every participant's recordings from `Renamed Signals/`
(about a minute) and saves them to `test_website/_cache/`, so later starts take
seconds. If the recordings change, run `python test_website/app.py --rebuild-cache`.

## Using it

1. **Pick a poster** at the top. It opens clustered with the same settings
   `demo.py` uses.
2. **Choose a method and change its parameters**, then press *Run clustering*
   (or tick *Re-run automatically*).
   - **Hierarchical**: linkage, and either *Auto* k (searches a k range and picks
     the largest k whose combined score is within the tolerance of the best,
     as in `python/clustering.py`) or a *Fixed* k.
   - **DBSCAN**: `eps` (neighbourhood radius in poster pixels) and `min_samples`.
3. **Compare settings**: every run is listed with its silhouette (higher is
   better), Davies-Bouldin (lower is better) and Calinski-Harabasz (higher is
   better) scores; the best of each is highlighted. Click a run to show it.
4. **Look at the chosen run** in three views:
   - **Clusters**: outlines, fixation points, and a table of each region's
     share of gaze time and of first looks.
   - **Heatmap**: fixation time density, for everyone or one participant, for
     the whole viewing or only the first few seconds, with the clusters on top.
   - **Gaze replay**: one participant's recorded gaze in real time. The dot
     takes the colour of the cluster being fixated and turns white during
     saccades. ★ marks the participant whose viewing best matches the group's.
     Beside it: the region they looked at first, the one they looked at
     longest, the regions in the order they first saw them, and their full
     path, each with what the region contains.
   - **Gaze replay → All participants (average)**: the group's fixation
     heatmap building up over time, with the regions numbered in the order the
     group reached them (average time of each person's first look, as in
     `output/eye_tracking_analysis.R`) and what each contains.
5. **Compare all posters** (top right): for every poster, the most-viewed
   region, the region looked at first, the group's order, and the split of
   fixation time between text, images, shapes and background, with a written
   summary across posters. It uses demo.py's settings, or the run you picked in
   the explorer for a poster.

## What a region contains

`poster_content.json` lists what is where on each poster: text, images and
shapes, each with a short label and boxes in percent of the poster. A region's
content is the element its fixation time falls on most (where boxes overlap,
the smallest box wins, so text printed on a shape counts as text; anything
outside every box is background). The boxes were drawn by hand from the poster
images, so adjust them if a label looks wrong; the site picks up edits without
a restart.

A link can open a view directly, for example
`http://127.0.0.1:5000/#poster=nancy_poster&view=replay&t=6`.

## How it fits with the rest of the repository

- Clustering is `python/clustering.py`, the same code as `demo.py` and
  `python/make_cluster_animations.py`, so the numbers match theirs.
- Poster list, clustering defaults and data loading come from
  `python/make_cluster_animations.py` (`PARAMS`).
- `app.py` is the server; `static/` holds the page (`index.html`, `app.js`,
  `style.css`). The page draws everything itself, so changing a setting does not
  require rendering a GIF.
