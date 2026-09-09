## =============================================================================
## Eye-Tracking Poster Attention Analysis — full R pipeline
## =============================================================================
## Ported from a working Python (pandas/numpy/scipy) pipeline that produced:
##   - average heatmaps for 0-2s / 0-5s / 0-16s windows
##   - data-driven K-means region clustering (k chosen via silhouette score)
##   - region-level stats (first attention, dwell time, viewing order)
##   - average_gaze_path.png and average_gaze_animation.gif per poster
##
## IMPORTANT: R was not available in the sandbox this was written in, so this
## script has NOT been executed/tested. Run it on 2-3 participants first
## (set N_PARTICIPANTS <- 3 below) and open each intermediate PNG before
## committing to the full 48-participant run. Most likely trouble spots are
## flagged with # CHECK comments.
##
## Required packages:
install.packages(c("readr","dplyr","tidyr","ggplot2","magick","cluster"))
   if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
   BiocManager::install("EBImage")   # used for pixel-array work + Gaussian blur


library(readr)
library(dplyr)
library(tidyr)
library(ggplot2)
library(magick)
library(cluster)
library(EBImage)

## ---------------------------------------------------------------------------
## CONFIG — edit these paths for your machine
## ---------------------------------------------------------------------------
BASE_DIR <- "C:/path/to/Renamed Signals"   # folder containing p1, p2, ... p48
OUT_DIR  <- "C:/path/to/output"            # folder containing poster_* subfolders
SCRATCH  <- file.path(OUT_DIR, "_scratch") # intermediate files land here
dir.create(SCRATCH, showWarnings = FALSE)

N_PARTICIPANTS <- 48

# poster output-folder name -> exact SourceStimuliName string in the CSVs
POSTERS <- list(
  "poster_ArminHofman-1955" = "Armin Hofman- 1955",
  "poster_BarryCeck-1988"   = "Barry Ceck - 1988"
)

# canvas transform: screen coords (1920x1200) -> the 1950x1350 plot canvas
# used by the existing per-participant heatmap_plot.png / gaze_path_plot.png
# (validated against those files: 100% of fixations landed on the drawn path)
CROP_X0 <- 7;   CROP_Y0 <- 68
CROP_X1 <- 1943; CROP_Y1 <- 1276
CROP_W  <- CROP_X1 - CROP_X0     # 1936
CROP_H  <- CROP_Y1 - CROP_Y0     # 1208
OFFSET_X <- 7;   SCALE_X <- 1936/1920
OFFSET_Y <- 68;  SCALE_Y <- 1208/1200
SIGMA <- 45   # gaussian blur sigma (px) for heatmaps, tuned to match the
# existing individual heatmap_plot.png blob size

transform_xy <- function(x, y) {
  list(x = OFFSET_X + x * SCALE_X, y = OFFSET_Y + y * SCALE_Y)
}

## =============================================================================
## STEP 1 — extract & transform fixations for both posters, all participants
## =============================================================================

extract_all_fixations <- function() {
  all_rows <- list()

  for (i in seq_len(N_PARTICIPANTS)) {
    pid  <- paste0("p", i)
    pdir <- file.path(BASE_DIR, pid)
    se_path <- file.path(pdir, "Native_SlideEvents.csv")
    gz_path <- file.path(pdir, "ET_RExtAPI-GazeAnalysis.csv")
    if (!file.exists(se_path) || !file.exists(gz_path)) {
      warning("Missing files for ", pid); next
    }

    # header row is line 18 -> skip the first 17 lines
    se <- read_csv(se_path, skip = 17, show_col_types = FALSE, progress = FALSE)
    # header row is line 21 -> skip the first 20 lines               # CHECK line counts if your export differs
    gz <- read_csv(gz_path, skip = 20, show_col_types = FALSE, progress = FALSE)

    # force numeric (readr sometimes infers character when a column has blanks)
    num_cols <- c("Fixation Start","Fixation End","Fixation X","Fixation Y",
                  "Fixation Duration","Fixation Index")
    gz <- gz %>% mutate(across(all_of(num_cols), as.numeric))
    se <- se %>% mutate(Timestamp = as.numeric(Timestamp))

    fix <- gz %>%
      filter(!is.na(`Fixation Start`)) %>%
      distinct(`Fixation Index`, .keep_all = TRUE)

    for (poster_folder in names(POSTERS)) {
      stim_name <- POSTERS[[poster_folder]]
      ev <- se %>% filter(SourceStimuliName == stim_name)
      t0 <- ev %>% filter(SlideEvent == "StartMedia") %>% pull(Timestamp)
      t1 <- ev %>% filter(SlideEvent == "EndMedia")   %>% pull(Timestamp)
      if (length(t0) == 0 || length(t1) == 0) next
      t0 <- t0[1]; t1 <- t1[1]

      win <- fix %>% filter(`Fixation Start` >= t0, `Fixation Start` <= t1)
      if (nrow(win) == 0) next

      xy <- transform_xy(win$`Fixation X`, win$`Fixation Y`)
      all_rows[[length(all_rows) + 1]] <- tibble(
        participant = pid,
        poster      = poster_folder,
        canvas_x    = xy$x,
        canvas_y    = xy$y,
        duration    = win$`Fixation Duration`,
        rel_start   = win$`Fixation Start` - t0,
        rel_end     = win$`Fixation End` - t0
      )
    }
    message("done: ", pid)
  }

  bind_rows(all_rows)
}

# fixations <- extract_all_fixations()
# write_csv(fixations, file.path(SCRATCH, "fixations_master.csv"))
# fixations <- read_csv(file.path(SCRATCH, "fixations_master.csv"), show_col_types = FALSE)

## =============================================================================
## STEP 2 — recover a clean poster background from the 48 individual plots
## =============================================================================
## Only needed if you don't still have the original, unmarked stimulus image.
## If you DO have the original poster image, skip this step entirely and just
## read + crop that instead — it'll be cleaner and much faster.
##
## Method: "running lowest-saturation pixel" across all 48 gaze_path_plot.png
## images. The true poster background is low-saturation (black/white/cream);
## the viridis/plasma scanpath overlay is highly saturated, so keeping
## whichever of the 48 samples is least saturated at each pixel recovers the
## background even in heavily-traced areas (as long as at least one of the 48
## participants' paths didn't cross that exact pixel).

saturation <- function(img_arr) {
  # img_arr: EBImage array, dim = (width, height, 3), values in [0,1]
  r <- img_arr[,,1]; g <- img_arr[,,2]; b <- img_arr[,,3]
  pmax(r, g, b) - pmin(r, g, b)
}

recover_background <- function(poster) {
  best <- NULL
  best_sat <- NULL
  for (i in seq_len(N_PARTICIPANTS)) {
    p <- file.path(OUT_DIR, poster, paste0("p", i), "gaze_path_plot.png")
    im <- readImage(p)[,,1:3]                # drop alpha channel if present
    s  <- saturation(im)
    if (is.null(best)) {
      best <- im; best_sat <- s
    } else {
      take_new <- s < best_sat               # per-pixel logical mask
      for (ch in 1:3) {
        chan <- best[,,ch]
        chan[take_new] <- im[,,ch][take_new]
        best[,,ch] <- chan
      }
      best_sat[take_new] <- s[take_new]
    }
    if (i %% 10 == 0) message(poster, ": processed ", i, "/", N_PARTICIPANTS)
  }
  writeImage(best, file.path(SCRATCH, paste0("bg_", poster, ".png")))
  best
}

# bg_armin <- recover_background("poster_ArminHofman-1955")
# bg_barry <- recover_background("poster_BarryCeck-1988")

## =============================================================================
## STEP 3 — average heatmaps for 0-2s / 0-5s / 0-16s windows
## =============================================================================

build_density <- function(fix_sub, window_ms, crop_w = CROP_W, crop_h = CROP_H,
                          x0 = CROP_X0, y0 = CROP_Y0, sigma = SIGMA,
                          n_participants = N_PARTICIPANTS) {
  w <- fix_sub %>%
    filter(rel_start < window_ms) %>%
    mutate(clip_end = pmin(rel_end, window_ms),
           weight   = pmax(clip_end - rel_start, 0),
           px = round(canvas_x - x0),
           py = round(canvas_y - y0)) %>%
    filter(px >= 0, px < crop_w, py >= 0, py < crop_h)

  hist <- matrix(0, nrow = crop_h, ncol = crop_w)
  # accumulate weights per pixel (vectorised via a lookup table, avoids an R loop)
  key <- w$py * crop_w + w$px
  agg <- tapply(w$weight, key, sum)
  idx <- as.integer(names(agg))
  hist[cbind(idx %/% crop_w + 1, idx %% crop_w + 1)] <- as.numeric(agg)

  # EBImage::gblur expects an EBImage/array; sigma matches scipy.ndimage.gaussian_filter
  smoothed <- gblur(hist, sigma = sigma)
  smoothed / n_participants
}

turbo_lut <- function(n = 256) {
  # approximate 'turbo' colormap using a built-in-ish gradient;
  # swap for your favourite palette if you like (viridis, etc.)
  colorRampPalette(c("#30123b","#4145ab","#2ab8ba","#a4fc3c","#eec434","#e6402a","#7a0403"))(n)
}

render_heatmap <- function(poster, bg_img, window_ms, label) {
  dens <- build_density(fixations %>% filter(poster == !!poster), window_ms)
  vmax <- max(dens); if (vmax <= 0) vmax <- 1
  norm_d <- pmin(dens / vmax, 1)

  lut <- turbo_lut(256)
  idx <- pmax(1, pmin(256, round(norm_d * 255) + 1))
  heat_rgb <- array(0, dim = c(CROP_H, CROP_W, 3))
  rgb_lut <- t(col2rgb(lut)) / 255   # 256 x 3
  for (ch in 1:3) heat_rgb[,,ch] <- matrix(rgb_lut[idx, ch], nrow = CROP_H, ncol = CROP_W)

  alpha <- (pmin(norm_d * 1.15, 1) ^ 0.6) * 0.88

  bg_gray <- channel(bg_img, "gray")                 # EBImage, dim (W,H)
  bg_gray_rgb <- array(rep(as.numeric(t(bg_gray)), 3), dim = c(CROP_H, CROP_W, 3)) # CHECK orientation

  composite <- array(0, dim = c(CROP_H, CROP_W, 3))
  for (ch in 1:3) composite[,,ch] <- bg_gray_rgb[,,ch] * (1 - alpha) + heat_rgb[,,ch] * alpha

  img <- Image(aperm(composite, c(2,1,3)), colormode = Color)  # back to (W,H,3) for EBImage
  img <- transpose(img)  # CHECK: verify orientation matches source (no mirroring)

  out_path <- file.path(OUT_DIR, poster, paste0("heatmap_avg_", label, ".png"))
  writeImage(img, out_path)

  # add title/subtitle/colour key with magick (simpler & more reliable for text)
  m <- image_read(out_path)
  m <- image_border(m, "black", "0x70")  # top margin for title text  # CHECK geometry
  m <- image_annotate(m, "Eye Tracking — Average Gaze Density Heatmap",
                      gravity = "north", location = "+0+8", size = 26,
                      color = "white", weight = 700)
  m <- image_annotate(m,
                      sprintf("Warmer colours = more time spent looking  —  averaged across %d participants (%s)",
                              N_PARTICIPANTS, label),
                      gravity = "north", location = "+0+42", size = 14, color = "gray80")
  image_write(m, out_path)
  message("saved ", out_path)
}

# for (poster in names(POSTERS)) {
#   bg <- readImage(file.path(SCRATCH, paste0("bg_", poster, ".png")))
#   bg_crop <- bg[(CROP_X0+1):CROP_X1, (CROP_Y0+1):CROP_Y1, 1:3]  # EBImage index = (x,y)
#   for (spec in list(c("2s", 2000), c("5s", 5000), c("16s", 16000))) {
#     render_heatmap(poster, bg_crop, as.numeric(spec[2]), spec[1])
#   }
# }

## =============================================================================
## STEP 4 — data-driven region clustering (weighted K-means + silhouette)
## =============================================================================

weighted_kmeans <- function(X, w, k, iter.max = 50, nstart = 10, seed = 42) {
  set.seed(seed)
  best <- NULL
  n <- nrow(X)
  for (start in seq_len(nstart)) {
    centers <- X[sample(n, k), , drop = FALSE]
    assign <- rep(1L, n)
    for (it in seq_len(iter.max)) {
      d2 <- sapply(seq_len(k), function(j) rowSums(sweep(X, 2, centers[j, ])^2))
      new_assign <- max.col(-d2)  # index of min distance per row
      new_centers <- centers
      for (j in seq_len(k)) {
        idx <- which(new_assign == j)
        if (length(idx) == 0) next
        new_centers[j, ] <- colSums(X[idx, , drop = FALSE] * w[idx]) / sum(w[idx])
      }
      converged <- all(new_assign == assign) && it > 1
      assign <- new_assign; centers <- new_centers
      if (converged) break
    }
    wcss <- sum(w * rowSums((X - centers[assign, , drop = FALSE])^2))
    if (is.null(best) || wcss < best$wcss) {
      best <- list(centers = centers, assign = assign, wcss = wcss)
    }
  }
  best
}

cluster_poster_regions <- function(poster, k_range = 3:7) {
  sub <- fixations %>% filter(poster == !!poster) %>%
    mutate(px = canvas_x - CROP_X0, py = canvas_y - CROP_Y0)
  X <- as.matrix(sub[, c("px", "py")])
  w <- sub$duration

  best_k <- NULL; best_score <- -2; best_fit <- NULL
  for (k in k_range) {
    fit <- weighted_kmeans(X, w, k)
    sil <- silhouette(fit$assign, dist(X))
    score <- mean(sil[, 3])
    message(poster, " k=", k, " silhouette=", round(score, 4))
    if (score > best_score) { best_score <- score; best_k <- k; best_fit <- fit }
  }
  message(poster, " -> chosen k=", best_k, " silhouette=", round(best_score, 4))

  sub$region <- best_fit$assign
  list(data = sub, centers = best_fit$centers, k = best_k, silhouette = best_score)
}

# clust_armin <- cluster_poster_regions("poster_ArminHofman-1955")
# clust_barry <- cluster_poster_regions("poster_BarryCeck-1988")

## =============================================================================
## STEP 5 — region-level statistics
## =============================================================================

region_stats <- function(clust) {
  df <- clust$data
  n_participants <- n_distinct(df$participant)
  total_dur <- sum(df$duration)

  pct_time <- df %>% group_by(region) %>% summarise(pct = sum(duration) / total_dur * 100)
  avg_span <- df %>% group_by(region) %>% summarise(avg_ms = mean(duration))

  first_fix <- df %>% group_by(participant) %>% slice_min(rel_start, n = 1, with_ties = FALSE)
  first_pct <- first_fix %>% count(region) %>% mutate(pct = n / n_participants * 100)

  entry <- df %>% group_by(participant, region) %>% summarise(t0 = min(rel_start), .groups = "drop")
  avg_entry <- entry %>% group_by(region) %>% summarise(avg_ms = mean(t0))
  coverage  <- entry %>% group_by(region) %>% summarise(pct = n_distinct(participant) / n_participants * 100)

  order <- avg_entry %>% arrange(avg_ms) %>% pull(region)

  # rank regions by descending % time so "Region 1" = most-viewed (matches the
  # numbering used in the write-up / images)
  rank_map <- pct_time %>% arrange(desc(pct)) %>% mutate(region_num = row_number()) %>%
    select(region, region_num)

  list(pct_time = pct_time, avg_span = avg_span, first_pct = first_pct,
       avg_entry = avg_entry, coverage = coverage, visit_order = order,
       rank_map = rank_map, n_participants = n_participants, k = clust$k)
}

# stats_armin <- region_stats(clust_armin)
# stats_barry <- region_stats(clust_barry)

## =============================================================================
## STEP 6 — average_gaze_path.png (region map + aggregate viewing order)
## =============================================================================

plot_average_gaze_path <- function(poster, clust, stats, bg_path) {
  rank_map <- stats$rank_map
  centers <- as.data.frame(clust$centers) %>%
    mutate(region = row_number()) %>%
    left_join(rank_map, by = "region") %>%
    left_join(stats$pct_time, by = "region")

  order_ranked <- rank_map$region_num[match(stats$visit_order, rank_map$region)]
  arrows_df <- data.frame(
    x    = centers$px[match(stats$visit_order[-length(stats$visit_order)], centers$region)],
    y    = centers$py[match(stats$visit_order[-length(stats$visit_order)], centers$region)],
    xend = centers$px[match(stats$visit_order[-1], centers$region)],
    yend = centers$py[match(stats$visit_order[-1], centers$region)]
  )

  bg <- image_read(bg_path)
  info <- image_info(bg)

  g <- ggplot() +
    annotation_raster(as.raster(bg), xmin = 0, xmax = info$width, ymin = info$height, ymax = 0) +
    geom_segment(data = arrows_df, aes(x, y, xend = xend, yend = yend),
                 arrow = arrow(length = unit(0.3, "cm")), color = "white", linewidth = 1.2) +
    geom_point(data = centers, aes(px, py, size = pct), color = "red", alpha = 0.85) +
    geom_text(data = centers, aes(px, py, label = paste0("Region ", region_num, "\n",
                                                         round(pct, 0), "% of gaze time")),
              color = "white", fontface = "bold", size = 3.2, vjust = -0.6) +
    scale_size_continuous(range = c(6, 16), guide = "none") +
    scale_y_reverse() +
    coord_fixed(xlim = c(0, info$width), ylim = c(info$height, 0)) +
    theme_void() +
    theme(plot.background = element_rect(fill = "black"),
          plot.title = element_text(color = "white", face = "bold", hjust = 0.5, size = 16)) +
    ggtitle("Eye Tracking — Average Scanpath by Region")

  out_path <- file.path(OUT_DIR, poster, "average_gaze_path.png")
  ggsave(out_path, g, width = 9, height = 7, dpi = 150, bg = "black")
  message("saved ", out_path)
}

# plot_average_gaze_path("poster_ArminHofman-1955", clust_armin, stats_armin,
#                         file.path(SCRATCH, "bg_poster_ArminHofman-1955.png"))

## =============================================================================
## STEP 7 — average_gaze_animation.gif (cumulative heatmap build-up)
## =============================================================================

make_average_gif <- function(poster, clust, bg_path, step_ms = 1000, max_ms = 16000) {
  bg <- readImage(bg_path)
  bg_crop <- bg[(CROP_X0+1):CROP_X1, (CROP_Y0+1):CROP_Y1, 1:3]

  sub <- fixations %>% filter(poster == !!poster)
  # fix a single global colour scale using the full 16s window so the
  # animation's colours are comparable frame to frame
  vmax <- max(build_density(sub, max_ms))

  frame_paths <- c()
  for (t in seq(step_ms, max_ms, by = step_ms)) {
    dens <- build_density(sub, t)
    norm_d <- pmin(dens / vmax, 1)

    lut <- turbo_lut(256)
    idx <- pmax(1, pmin(256, round(norm_d * 255) + 1))
    rgb_lut <- t(col2rgb(lut)) / 255
    heat_rgb <- array(0, dim = c(CROP_H, CROP_W, 3))
    for (ch in 1:3) heat_rgb[,,ch] <- matrix(rgb_lut[idx, ch], nrow = CROP_H, ncol = CROP_W)
    alpha <- (pmin(norm_d * 1.15, 1) ^ 0.6) * 0.88

    bg_gray <- channel(bg_crop, "gray")
    bg_gray_rgb <- array(rep(as.numeric(t(bg_gray)), 3), dim = c(CROP_H, CROP_W, 3)) # CHECK orientation

    composite <- array(0, dim = c(CROP_H, CROP_W, 3))
    for (ch in 1:3) composite[,,ch] <- bg_gray_rgb[,,ch] * (1 - alpha) + heat_rgb[,,ch] * alpha

    img <- Image(aperm(composite, c(2,1,3)), colormode = Color)
    img <- transpose(img)  # CHECK orientation

    fp <- file.path(SCRATCH, sprintf("%s_frame_%02d.png", poster, t / step_ms))
    writeImage(img, fp)

    m <- image_read(fp)
    m <- image_scale(m, "600x")   # downscale for a reasonably small gif
    m <- image_annotate(m, "Eye Tracking — Average Gaze Animation",
                        gravity = "north", location = "+0+4", size = 18,
                        color = "white", weight = 700)
    m <- image_annotate(m, sprintf("t = %.1fs  (averaged across %d participants)",
                                   t / 1000, N_PARTICIPANTS),
                        gravity = "north", location = "+0+26", size = 12, color = "gray80")
    image_write(m, fp)
    frame_paths <- c(frame_paths, fp)
  }

  frames <- image_read(frame_paths)
  anim <- image_animate(image_join(frames), fps = 1000 / 160)  # ~160ms/frame
  out_path <- file.path(OUT_DIR, poster, "average_gaze_animation.gif")
  image_write(anim, out_path)
  message("saved ", out_path)
}

# make_average_gif("poster_ArminHofman-1955", clust_armin,
#                   file.path(SCRATCH, "bg_poster_ArminHofman-1955.png"))

## =============================================================================
## RUN EVERYTHING
## =============================================================================
## Uncomment and run section by section (recommended) rather than all at once,
## so you can check each intermediate file before moving on.

# fixations <- extract_all_fixations()
# write_csv(fixations, file.path(SCRATCH, "fixations_master.csv"))
#
# results <- list()
# for (poster in names(POSTERS)) {
#   bg <- recover_background(poster)                 # or: read your original stimulus image instead
#   bg_crop <- bg[(CROP_X0+1):CROP_X1, (CROP_Y0+1):CROP_Y1, 1:3]
#
#   for (spec in list(c("2s", 2000), c("5s", 5000), c("16s", 16000))) {
#     render_heatmap(poster, bg_crop, as.numeric(spec[2]), spec[1])
#   }
#
#   clust <- cluster_poster_regions(poster)
#   stats <- region_stats(clust)
#   plot_average_gaze_path(poster, clust, stats, file.path(SCRATCH, paste0("bg_", poster, ".png")))
#   make_average_gif(poster, clust, file.path(SCRATCH, paste0("bg_", poster, ".png")))
#
#   results[[poster]] <- list(clust = clust, stats = stats)
# }
#
# # print a quick summary table
# for (poster in names(POSTERS)) {
#   cat("\n===", poster, "===\n")
#   print(results[[poster]]$stats$pct_time)
#   print(results[[poster]]$stats$visit_order)
# }
