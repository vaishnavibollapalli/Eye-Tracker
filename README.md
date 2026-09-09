# Eye-Tracker: Gaze Visualization & Attention Analysis for Graphic Design Posters

An R-based pipeline that turns raw eye-tracking exports (iMotions / Smart Eye Aurora) into
scanpath plots, gaze-density heatmaps, and animated gaze replays. The project started as a
single-subject pilot on one poster and grew into a full study covering **15 graphic design
posters across 48 participants**, with data-driven region-of-interest analysis on top.

## Project History

| Stage | What it covers |
|-------|-----------------|
| **Pilot** (`test/`, `Path_Visualization.Rmd`) | One participant, one poster (David Carson, 1990). Proved out the core visualization approach: scanpath, gaze path, heatmap, animated replay. |
| **Single-participant, all posters** (`participant_one/`) | Same pipeline re-run across all 15 posters for one participant, plus a Word comparison summary (`Gaze_Comparison_Summary.docx`). |
| **Full study** (`Renamed Signals/`, `output/`, `generate_all_plots.Rmd`) | All 15 posters × up to 48 participants. Produces per-participant plots, averaged/aggregated heatmaps per poster, and data-driven region (attention hotspot) analysis. Presented at the SURS Undergraduate Research Symposium at Georgia State University. |

## Repository Structure

```
Eye-Tracker/
├── Renamed Signals/           # Raw per-participant iMotions exports (p1 … p48)
├── posters/                   # 15 stimulus images (the posters shown to participants)
├── participant_one/           # Single-participant pilot run across all 15 posters
│   ├── <PosterName>/          #   scanpath, gaze path, heatmap, animated GIF per poster
│   ├── ET_Eyetracker.csv      #   raw iMotions eye-tracker export
│   ├── ET_RExtAPI-GazeAnalysis.csv
│   ├── Native_SlideEvents.csv #   slide/poster timing (SourceStimuliName, StartSlide, Duration)
│   ├── summary_stats.csv
│   └── Gaze_Comparison_Summary.docx
├── output/                    # Full 15-poster × 48-participant analysis
│   ├── poster_<Name>/         #   per-poster folder: per-participant p1…p48 outputs +
│   │                          #   averaged heatmaps (0-2s / 0-5s / 0-16s) and average gaze path/animation
│   ├── DBSCAN output/         #   region analysis using the DBSCAN clustering variant
│   ├── eye_tracking_analysis.R    # K-means region clustering pipeline (region stats, dwell time, viewing order)
│   ├── eye_tracking_dbscan.R      # DBSCAN drop-in alternative to the K-means clustering step
│   ├── Eye_Tracking_Poster.pptx
│   ├── Eye_Tracking_Region_Analysis.docx
│   ├── Methods_Visual.png / .pptx
│   ├── Poster_Presentation_Content.docx
│   └── Presentation_Script.docx
├── test/                      # Original single-subject, single-poster pilot artifacts
│   ├── test1_gazetracking.csv      # Raw gaze coordinates (original, uncleaned)
│   ├── test1_gazetracking_clean.csv
│   ├── test1_F&S.csv               # Fixation & saccade data (iMotions export)
│   └── scanpath_plot.png / gaze_path_plot.png / heatmap_plot.png / gaze_animation.gif
├── generate_all_plots.Rmd     # Multi-poster, multi-participant plot generator (reads Renamed Signals/ + posters/, writes output/)
├── Path_Visualization.Rmd     # Original pilot notebook (single participant, single poster)
├── Eye Tracker.Rproj
└── README.md
```

## Data Files

### Raw iMotions exports (`Renamed Signals/`, `participant_one/`, `test/`)

| Column | Description |
|--------|-------------|
| `Fixation X` / `Fixation Y` | Position of a fixation on screen (pixels) |
| `Fixation Duration` | How long the eye stayed at that point (ms) |
| `Saccade Duration` / `Saccade Amplitude` / `Saccade Direction` | Duration, distance, and angle of the eye movement between fixations |
| `Gaze X` / `Gaze Y` | Continuous raw gaze position, sampled at ~120 Hz |
| `Timestamp` | Time since recording started (ms) |

> **Fixation** = the eye is relatively still, actively processing information.
> **Saccade** = the rapid jump between fixations.

iMotions CSVs have multi-row metadata headers before the actual data starts, marked by a
`#DATA` line (which can have a trailing comma). Slide/poster timing comes from
`Native_SlideEvents.csv` via `SourceStimuliName` / `StartSlide` / `Duration`.

### `Native_SlideEvents.csv` — Poster Timing

Used to slice each participant's continuous signal into per-poster windows.

## Scripts

### `generate_all_plots.Rmd` — Multi-Poster, Multi-Participant Pipeline

Reads every participant's signal from `Renamed Signals/` and every stimulus from `posters/`,
slices each participant's data per poster using `Native_SlideEvents.csv`, and writes four
outputs per participant per poster into `output/poster_<Name>/pN/`:

| Output | What it shows |
|--------|---------------|
| `scanpath_plot.png` | Numbered fixation circles connected by saccade lines. Circle size = fixation duration. |
| `gaze_path_plot.png` | Continuous raw gaze trace coloured by time (early = dark, late = bright). |
| `heatmap_plot.png` | 2D density heatmap — warmer colours where the eye spent the most time. |
| `gaze_animation.gif` | Frame-by-frame replay of gaze position with a fading trail, overlaid on the poster. |

It also produces per-poster **averaged** outputs across all participants
(`average_gaze_path.png`, `average_gaze_animation.gif`, and heatmaps for 0-2s / 0-5s / 0-16s
viewing windows).

### `output/eye_tracking_analysis.R` and `output/eye_tracking_dbscan.R` — Region Analysis

Data-driven attention-region clustering on top of the aggregated fixations: which parts of
each poster draw attention first, how long they hold it, and in what order they're viewed.
`eye_tracking_analysis.R` uses K-means (k chosen via silhouette score); `eye_tracking_dbscan.R`
is a drop-in DBSCAN alternative that doesn't require specifying the number of regions up front
and can leave sparse points unclustered as noise. Both were ported from a working Python
(pandas/scikit-learn) pipeline — see the `# CHECK` comments in each file for spots worth
verifying on a small participant subset before a full re-run.

### `Path_Visualization.Rmd` — Original Pilot Notebook

The single-participant, single-poster notebook the rest of the pipeline grew out of. Useful as
a minimal, fully worked example of the core visualization approach.

## Setup & Installation

### Prerequisites
- R 4.0 or later
- RStudio (recommended)

### Install required packages
```r
install.packages(c(
  "tidyverse", "ggplot2", "jpeg", "png", "grid", "MASS",
  "dplyr", "scales", "ggrepel", "gganimate", "gifski",
  "readr", "tidyr", "magick", "cluster", "dbscan", "class"
))
if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
BiocManager::install("EBImage")
```

### Run

1. Open `Eye Tracker.Rproj` in RStudio — this sets the working directory automatically.
2. For the full study: run `generate_all_plots.Rmd` (reads `Renamed Signals/` + `posters/`,
   writes `output/`).
3. For region/attention analysis on top of the generated output: run
   `output/eye_tracking_analysis.R`, optionally followed by `output/eye_tracking_dbscan.R`.
4. For the original single-poster pilot: run `Path_Visualization.Rmd`.

## Understanding Eye-Tracking Metrics

| Term | Definition |
|------|------------|
| **Fixation** | A period where the eye is relatively still (typically 100–500ms). Indicates the brain is processing that region. |
| **Saccade** | A rapid eye movement jumping from one fixation to the next. Usually 20–200ms. No visual processing occurs during saccades. |
| **Scanpath** | The sequence of fixations and saccades across a stimulus — reveals reading order and areas of interest. |
| **Gaze density / heatmap** | A spatial summary of where total dwell time was concentrated. |
| **Fixation duration** | Longer fixations suggest more cognitive effort being spent on that region. |

## Data Source

Data collected using the **iMotions** biometric research platform (and Smart Eye Aurora) with
a screen-based eye tracker, across 15 graphic design posters and up to 48 participants. This
work was presented at the SURS Undergraduate Research Symposium at Georgia State University.
