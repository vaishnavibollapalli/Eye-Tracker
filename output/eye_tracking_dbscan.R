## =============================================================================
## Eye-Tracking Poster Attention Analysis — DBSCAN variant
## =============================================================================
## Drop-in alternative to the K-means clustering step (cluster_poster_regions)
## in eye_tracking_analysis.R. Source that script FIRST — this file reuses its
## objects: `fixations`, OUT_DIR, SCRATCH, CROP_X0/CROP_Y0/CROP_W/CROP_H,
## N_PARTICIPANTS, POSTERS, build_density(), turbo_lut(), region_stats().
##
## As with the K-means script, this was translated from a working Python
## (scikit-learn) pipeline and has NOT been run in R. Test on one poster and
## check the intermediate outputs before trusting it fully. # CHECK marks the
## spots most likely to need a tweak.
##
## Additional packages needed beyond eye_tracking_analysis.R:
##   install.packages(c("dbscan", "class"))
## =============================================================================

library(dbscan)   # fast DBSCAN implementation; NOTE: its noise label is 0, not -1
library(class)     # knn(), used to fold noise points into their nearest region
library(dplyr)
library(ggplot2)
library(magick)

## =============================================================================
## STEP 4 (DBSCAN version) — data-driven region clustering
## =============================================================================
## Unlike K-means, DBSCAN isn't told how many regions to find (k), and it
## doesn't force every fixation into a region — sparse/isolated points are
## left as "noise". Both of its parameters (eps = neighbourhood radius,
## min_samples = density threshold) are chosen the same data-driven way k was
## chosen for K-means: grid-search both, keep combinations that land on a
## sensible 3-7 regions with a reasonable noise share, and take whichever
## scores highest on silhouette.
##
## Fixation duration is NOT used to weight the clustering geometry here
## (DBSCAN's neighbour-counting doesn't support weights the way K-means'
## centroid update does — weighting a point would just fake extra density
## around it). Duration is still used for every *downstream* number (region
## size on the map, % of gaze time, average fixation duration) exactly as
## before, via region_stats().

cluster_poster_regions_dbscan <- function(poster,
                                           min_samples_grid = c(8, 10, 12, 15, 18, 20, 25, 30),
                                           eps_grid = c(18, 20, 22, 25, 28, 30, 35, 40, 45, 50, 55, 60, 70, 80),
                                           k_range = 3:7,
                                           noise_range = c(0.02, 0.40)) {
  sub <- fixations %>% filter(poster == !!poster) %>%
    mutate(px = canvas_x - CROP_X0, py = canvas_y - CROP_Y0)
  X <- as.matrix(sub[, c("px", "py")])
  w <- sub$duration

  best <- NULL
  tried <- list()
  for (ms in min_samples_grid) {
    for (eps in eps_grid) {
      db <- dbscan::dbscan(X, eps = eps, minPts = ms)
      labels <- db$cluster                       # 0 = noise in this package
      n_clusters <- length(unique(labels[labels != 0]))
      noise_frac <- mean(labels == 0)
      if (n_clusters < min(k_range) || n_clusters > max(k_range)) next
      if (noise_frac < noise_range[1] || noise_frac > noise_range[2]) next
      mask <- labels != 0
      if (sum(mask) < 10) next
      sil <- cluster::silhouette(labels[mask], dist(X[mask, , drop = FALSE]))
      score <- mean(sil[, 3])
      tried[[length(tried) + 1]] <- data.frame(min_samples = ms, eps = eps, score = score,
                                                n_clusters = n_clusters, noise_frac = noise_frac)
      if (is.null(best) || score > best$score) {
        best <- list(min_samples = ms, eps = eps, labels = labels, score = score,
                      n_clusters = n_clusters, noise_frac = noise_frac)
      }
    }
  }
  if (is.null(best)) stop("No viable DBSCAN parameters found for ", poster, " - widen the grid")

  tried_df <- do.call(rbind, tried)
  tried_df <- tried_df[order(-tried_df$score), ]
  message(poster, ": top DBSCAN combos tried (min_samples, eps, k, noise%, silhouette)")
  print(utils::head(tried_df, 8))

  labels <- best$labels
  sub$region_raw <- labels        # 0 = noise, kept for transparency / reporting

  # fold noise points into whichever region their single nearest labelled
  # neighbour belongs to (a 1-NN fill-in, same trick as the Python version)
  noise_mask <- labels == 0
  labels_filled <- labels
  if (any(noise_mask)) {
    nn <- class::knn(train = X[!noise_mask, , drop = FALSE],
                      test  = X[noise_mask, , drop = FALSE],
                      cl    = factor(labels[!noise_mask]), k = 1)
    labels_filled[noise_mask] <- as.integer(as.character(nn))
  }
  sub$region <- labels_filled

  # duration-weighted centroid per final region (DBSCAN has no built-in
  # "center" the way K-means does, so this is computed after the fact,
  # identically to the Python version)
  region_ids <- sort(unique(labels_filled))
  centers <- t(sapply(region_ids, function(r) {
    idx <- labels_filled == r
    c(px = stats::weighted.mean(sub$px[idx], w[idx]),
      py = stats::weighted.mean(sub$py[idx], w[idx]))
  }))
  rownames(centers) <- region_ids   # CHECK: downstream code keys off these rownames, not row position

  message(poster, " -> DBSCAN chosen: min_samples=", best$min_samples, " eps=", best$eps,
          " k=", best$n_clusters, " noise=", round(best$noise_frac * 100, 1), "%  ",
          "silhouette=", round(best$score, 4))

  list(data = sub, centers = centers, k = best$n_clusters, silhouette = best$score,
       eps = best$eps, min_samples = best$min_samples, noise_frac = best$noise_frac,
       region_ids = region_ids)
}

# clust_armin_db <- cluster_poster_regions_dbscan("poster_ArminHofman-1955")
# clust_barry_db <- cluster_poster_regions_dbscan("poster_BarryCeck-1988")
#
# stats_armin_db <- region_stats(clust_armin_db)   # region_stats() from the main script works unchanged
# stats_barry_db <- region_stats(clust_barry_db)

## =============================================================================
## STEP 6 (DBSCAN version) — average_gaze_path.png with convex-hull regions
## =============================================================================
## DBSCAN regions aren't round blobs around a center the way K-means regions
## are, so instead of a Voronoi/nearest-centroid split, each region is drawn
## as the convex hull of its own (noise-filled) points — a closer visual match
## to "the actual footprint DBSCAN found" than a forced tessellation.

plot_average_gaze_path_dbscan <- function(poster, clust, stats, bg_path) {
  rank_map <- stats$rank_map
  region_ids <- as.integer(rownames(clust$centers))
  centers <- as.data.frame(clust$centers) %>%
    mutate(region = region_ids) %>%
    left_join(rank_map, by = "region") %>%
    left_join(stats$pct_time, by = "region")

  order_ids <- stats$visit_order   # already region ids (see region_stats())
  arrows_df <- data.frame(
    x    = centers$px[match(order_ids[-length(order_ids)], centers$region)],
    y    = centers$py[match(order_ids[-length(order_ids)], centers$region)],
    xend = centers$px[match(order_ids[-1], centers$region)],
    yend = centers$py[match(order_ids[-1], centers$region)]
  )

  # convex hull polygon per region, for the shaded footprint
  hulls <- clust$data %>%
    group_by(region) %>%
    slice(chull(px, py)) %>%
    ungroup() %>%
    left_join(rank_map, by = "region")

  bg <- image_read(bg_path)
  info <- image_info(bg)

  g <- ggplot() +
    annotation_raster(as.raster(bg), xmin = 0, xmax = info$width, ymin = info$height, ymax = 0) +
    geom_polygon(data = hulls, aes(px, py, group = region, fill = factor(region_num)),
                 alpha = 0.28, color = "white", linewidth = 0.8) +
    geom_segment(data = arrows_df, aes(x, y, xend = xend, yend = yend),
                 arrow = arrow(length = unit(0.3, "cm")), color = "white", linewidth = 1.2) +
    geom_point(data = centers, aes(px, py, size = pct), color = "black", alpha = 0.85) +
    geom_text(data = centers, aes(px, py, label = paste0("Region ", region_num, "\n",
                                                           round(pct, 0), "% of gaze time")),
              color = "white", fontface = "bold", size = 3.2, vjust = -0.6) +
    scale_size_continuous(range = c(6, 16), guide = "none") +
    scale_fill_brewer(palette = "Set1", guide = "none") +
    scale_y_reverse() +
    coord_fixed(xlim = c(0, info$width), ylim = c(info$height, 0)) +
    theme_void() +
    theme(plot.background = element_rect(fill = "black"),
          plot.title = element_text(color = "white", face = "bold", hjust = 0.5, size = 15),
          plot.subtitle = element_text(color = "gray70", hjust = 0.5, size = 9)) +
    ggtitle("Eye Tracking — Average Scanpath by Region (DBSCAN)",
            subtitle = sprintf("k=%d regions, eps=%.0fpx, min_samples=%d, %.0f%% noise re-assigned to nearest region",
                                clust$k, clust$eps, clust$min_samples, clust$noise_frac * 100))

  out_path <- file.path(DBSCAN_OUT, poster, "average_gaze_path.png")
  ggsave(out_path, g, width = 9, height = 7, dpi = 150, bg = "black")
  message("saved ", out_path)
}

# plot_average_gaze_path_dbscan("poster_ArminHofman-1955", clust_armin_db, stats_armin_db,
#                                file.path(SCRATCH, "bg_poster_ArminHofman-1955.png"))

## =============================================================================
## STEP 7 (DBSCAN version) — average_gaze_animation.gif
## =============================================================================
## Identical build_density()/heatmap logic as the K-means version (clustering
## method doesn't affect the density surface at all) — only the region-number
## labels overlaid on each frame come from the DBSCAN result.

make_average_gif_dbscan <- function(poster, clust, bg_path, step_ms = 1000, max_ms = 16000) {
  bg <- readImage(bg_path)
  bg_crop <- bg[(CROP_X0+1):CROP_X1, (CROP_Y0+1):CROP_Y1, 1:3]

  sub <- fixations %>% filter(poster == !!poster)
  vmax <- max(build_density(sub, max_ms))

  rank_map <- region_stats(clust)$rank_map
  region_ids <- as.integer(rownames(clust$centers))
  region_nums <- rank_map$region_num[match(region_ids, rank_map$region)]

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
    bg_gray_rgb <- array(rep(as.numeric(t(bg_gray)), 3), dim = c(CROP_H, CROP_W, 3))  # CHECK orientation

    composite <- array(0, dim = c(CROP_H, CROP_W, 3))
    for (ch in 1:3) composite[,,ch] <- bg_gray_rgb[,,ch] * (1 - alpha) + heat_rgb[,,ch] * alpha

    img <- Image(aperm(composite, c(2,1,3)), colormode = Color)
    img <- transpose(img)  # CHECK orientation

    fp <- file.path(SCRATCH, sprintf("%s_dbscan_frame_%02d.png", poster, t / step_ms))
    writeImage(img, fp)

    m <- image_read(fp)
    m <- image_scale(m, "600x")
    m <- image_annotate(m, "Eye Tracking — Average Gaze Animation (DBSCAN)",
                         gravity = "north", location = "+0+4", size = 16,
                         color = "white", weight = 700)
    m <- image_annotate(m, sprintf("t = %.1fs  (averaged across %d participants)",
                                    t / 1000, N_PARTICIPANTS),
                         gravity = "north", location = "+0+26", size = 12, color = "gray80")
    image_write(m, fp)
    frame_paths <- c(frame_paths, fp)
  }

  frames <- image_read(frame_paths)
  anim <- image_animate(image_join(frames), fps = 1000 / 160)
  out_path <- file.path(DBSCAN_OUT, poster, "average_gaze_animation.gif")
  image_write(anim, out_path)
  message("saved ", out_path)
}

# make_average_gif_dbscan("poster_ArminHofman-1955", clust_armin_db,
#                          file.path(SCRATCH, "bg_poster_ArminHofman-1955.png"))

## =============================================================================
## RUN EVERYTHING (DBSCAN)
## =============================================================================
# DBSCAN_OUT <- file.path(OUT_DIR, "DBSCAN output")
# dir.create(file.path(DBSCAN_OUT, "poster_ArminHofman-1955"), recursive = TRUE, showWarnings = FALSE)
# dir.create(file.path(DBSCAN_OUT, "poster_BarryCeck-1988"), recursive = TRUE, showWarnings = FALSE)
#
# results_db <- list()
# for (poster in names(POSTERS)) {
#   # heatmaps are identical to the K-means run (clustering doesn't affect them) -
#   # just copy them over rather than recomputing
#   file.copy(file.path(OUT_DIR, poster, c("heatmap_avg_2s.png","heatmap_avg_5s.png","heatmap_avg_16s.png")),
#             file.path(DBSCAN_OUT, poster), overwrite = TRUE)
#
#   clust <- cluster_poster_regions_dbscan(poster)
#   stt   <- region_stats(clust)
#   plot_average_gaze_path_dbscan(poster, clust, stt, file.path(SCRATCH, paste0("bg_", poster, ".png")))
#   make_average_gif_dbscan(poster, clust, file.path(SCRATCH, paste0("bg_", poster, ".png")))
#
#   results_db[[poster]] <- list(clust = clust, stats = stt)
# }
#
# for (poster in names(POSTERS)) {
#   cat("\n===", poster, "(DBSCAN) ===\n")
#   print(results_db[[poster]]$stats$pct_time)
#   print(results_db[[poster]]$stats$visit_order)
# }
