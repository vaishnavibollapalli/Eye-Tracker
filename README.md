# Eye-Tracker: Gaze Visualization in R

A set of R scripts that visualize eye-tracking data from a single subject viewing a stimulus image. Produces a static scanpath plot, a raw gaze path, a density heatmap, and a frame-by-frame animated Gaze replay — all overlaid on the original stimulus.

## Repository Structure

```
Eye-Tracker/
│
├── test1_F_S.csv                  # Fixation & saccade data (iMotions export)
├── test1_gazetracking_clean.csv   # Raw gaze coordinates (cleaned)
├── test1_gazetracking.csv         # Raw gaze coordinates (original, uncleaned)
├── David Carson.jpg               # Stimulus image shown to the subject
│
├── scanpath_visualization.R       # Static plots (scanpath, gaze path, heatmap)
├── scanpath_animation.R           # Animated gaze replay GIF
│
└── README.md
```

## Data Files

### `test1_F_S.csv` — Fixations & Saccades

Exported from iMotions. Each row represents either a fixation event or a saccade event.

| Column | Description |
|--------|-------------|
| `Fixation Index by Stimulus` | Sequential fixation number (1, 2, 3...) |
| `Fixation X` | Horizontal position of fixation on screen (pixels) |
| `Fixation Y` | Vertical position of fixation on screen (pixels) |
| `Fixation Duration` | How long the eye stayed at that point (milliseconds) |
| `Saccade Index by Stimulus` | Sequential saccade number |
| `Saccade Duration` | Duration of the eye movement (ms) |
| `Saccade Amplitude` | Distance traveled during saccade (degrees of visual angle) |
| `Saccade Direction` | Angle of eye movement (degrees, 0° = right) |

**Subject stats:** 61 fixations, durations ranging from 66.7 ms to 283.3 ms.

> **Fixation** = the eye is relatively still, actively processing information.  
> **Saccade** = the rapid jump between fixations.

---

### `test1_gazetracking_clean.csv` — Raw Gaze Data

Cleaned version of the continuous gaze stream sampled at ~120 Hz (~8ms per sample).

| Column | Description |
|--------|-------------|
| `Timestamp` | Time since recording started (milliseconds) |
| `Gaze X` | Horizontal gaze position on screen (pixels) |
| `Gaze Y` | Vertical gaze position on screen (pixels) |

**Subject stats:** 2,042 samples. X range: 158–1718 px. Y range: 141–967 px. Screen resolution: 1920×1200.

> Unlike the fixation file, this contains every raw sample including the movements between fixations.

---

## Scripts

### `scanpath_visualization.R` — Three Static Plots

Produces three PNG files saved to your working directory.

#### How it works

**1. Load & filter data**
```r
fixations <- fs %>%
  filter(!is.na(Fixation.X) & !is.na(Fixation.Y))
```
The F&S CSV has rows for both fixations and saccades. Since saccade rows have empty Fixation X/Y columns, filtering on those gives us only fixation events, ordered by their sequence number.

**2. Y-axis flip**
```r
y_flip = img_h - y
```
Eye trackers place the origin (0,0) at the **top-left** of the screen with Y increasing downward. ggplot places the origin at the **bottom-left** with Y increasing upward. Without this flip, the plot would appear vertically mirrored.

**3. Background image**
```r
annotation_raster(bg_img, xmin=0, xmax=img_w, ymin=0, ymax=img_h)
```
Renders the stimulus JPEG as a static pixel layer. All gaze coordinates are in the same pixel space, so no rescaling is needed.

#### Output files

| File | What it shows |
|------|---------------|
| `scanpath_plot.png` | Numbered fixation circles connected by saccade lines. Circle size = fixation duration. |
| `gaze_path_plot.png` | Continuous raw gaze trace coloured by time (early = dark, late = bright). |
| `heatmap_plot.png` | 2D density heatmap — warmer colours where the eye spent the most time. |

---

### `scanpath_animation.R` — "Through Their Eyes" Replay

Produces `gaze_animation.gif` — a frame-by-frame replay of where the subject's eye was at every moment, with a fading trail behind the current gaze position.

#### How it works

**1. Frame index**
```r
gaze <- gaze %>% mutate(frame = row_number())
```
Each of the 2,042 gaze samples becomes one frame of the animation.

**2. Fading trail**
```r
trail_length <- 20
gaze_with_trail <- lapply(gaze$frame, function(f) {
  start <- max(1, f - trail_length + 1)
  slice <- gaze[start:f, ]
  slice$age <- seq_len(nrow(slice))
  ...
})
```
For each frame, the last 20 gaze samples are collected. Each sample is assigned an `age` value (1 = oldest, 20 = current). Older points are rendered smaller and more transparent, creating a comet-tail effect.

**3. Two point layers**
- **Blue fading dots** — the trail (`alpha` and `size` controlled by `age`)
- **White ring** — the current gaze position, always rendered on top at full opacity

**4. gganimate**
```r
transition_manual(current_frame)
```
Steps through frames one at a time in order, producing a temporally accurate replay.

#### Controlling playback speed

```r
animate(p, nframes = nrow(gaze), fps = 60, ...)
```

| FPS | Effect |
|-----|--------|
| `125` | Real-time (data sampled every ~8ms) |
| `60` | Half speed — easier to follow |
| `30` | Slow motion — good for analysis |

---

## Setup & Installation

### Prerequisites
- R 4.0 or later
- RStudio (recommended)

### Install required packages
```r
install.packages(c(
  "ggplot2",   # plotting
  "jpeg",      # reading the background image
  "grid",      # raster rendering
  "dplyr",     # data wrangling
  "scales",    # alpha/colour helpers
  "ggrepel",   # non-overlapping labels
  "gganimate", # animation
  "gifski"     # GIF renderer
))
```

### Run

1. Open `Eye Tracker.Rproj` in RStudio — this sets the working directory automatically
2. Rename the F&S file if needed (iMotions exports it as `test1_F&S.csv`):
```r
file.rename("test1_F&S.csv", "test1_F_S.csv")
```
3. Run `scanpath_visualization.R` for the static plots (~5 seconds)
4. Run `scanpath_animation.R` for the GIF (~1–2 minutes to render)

---

## Understanding Eye-Tracking Metrics

| Term | Definition |
|------|------------|
| **Fixation** | A period where the eye is relatively still (typically 100–500ms). Indicates the brain is processing that region. |
| **Saccade** | A rapid eye movement jumping from one fixation to the next. Usually 20–200ms. No visual processing occurs during saccades. |
| **Scanpath** | The sequence of fixations and saccades across a stimulus — reveals reading order and areas of interest. |
| **Gaze density / heatmap** | A spatial summary of where total dwell time was concentrated. |
| **Fixation duration** | Longer fixations suggest more cognitive effort being spent on that region. |

---

## Data Source

Data collected using **iMotions** biometric research platform with a screen-based eye tracker. The stimulus is a 1920×1200px image of a David Carson magazine layout (1990). This dataset represents a single participant viewing session.
