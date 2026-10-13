# Divisive (Bisecting K-Means) Region Analysis -- summary

Posters: poster_ArminHofman-1955, poster_BarryCeck-1988, poster_DavidCarson, poster_DavidCarson-1990, poster_EllaRosenblatt-2021, poster_IrisChung-2015, poster_JanTschichold-1927-DieFrauohneNamen, poster_JanTschichold-1938-Der, poster_JoostSchmidt-1923-Saatliches, poster_PaulRand-1947, poster_PaulaScher-1995, poster_ScottBarry-2010, poster_SeanAlatorre, poster_bookcover, poster_nancy
Participants pooled: 48

## poster_ArminHofman-1955

- Dropped 178 stray/isolated fixations before clustering (7.3%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   3 |     0.63671  |         0.441292 |             7416.18 | 1        |
|   4 |     0.567747 |         0.627885 |             8472.91 | 0.502345 |
|   5 |     0.469316 |         0.761168 |             7858.67 | 0        |

- Chosen k=3, silhouette=0.637, Davies-Bouldin=0.441
- Aggregate viewing order: R2 -> R1 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |           943 |           47.23 |             244.5 |                  16.7 |           2334 |                        100 |               2 |     1020.5 |      796.6 |
|               1 |            2 |           968 |           36.56 |             184.4 |                  83.3 |            340 |                        100 |               1 |     1125.5 |      223.6 |
|               4 |            3 |           362 |           16.21 |             218.7 |                   0   |           5279 |                        100 |               3 |     1218.5 |     1072.4 |

## poster_BarryCeck-1988

- Dropped 140 stray/isolated fixations before clustering (5.2%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   4 |     0.449431 |         0.765688 |             2832.02 | 1        |
|   5 |     0.411543 |         0.768022 |             2868.17 | 0.490264 |
|   3 |     0.411503 |         0.87944  |             2352.83 | 0        |

- Chosen k=4, silhouette=0.449, Davies-Bouldin=0.766
- Aggregate viewing order: R2 -> R1 -> R4 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |           892 |           36.55 |             184   |                  50   |           1389 |                        100 |               2 |      996.4 |      812.6 |
|               6 |            2 |           608 |           22.32 |             164.8 |                  45.8 |            673 |                        100 |               1 |      963.9 |      230.6 |
|               4 |            3 |           553 |           21.45 |             174.2 |                   4.2 |           3513 |                        100 |               4 |      402.9 |      818.8 |
|               5 |            4 |           517 |           19.69 |             171.1 |                   0   |           3262 |                        100 |               3 |     1475.3 |      345.1 |

## poster_DavidCarson

- Dropped 131 stray/isolated fixations before clustering (5.0%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   3 |     0.517369 |         0.700103 |             3848.98 | 0.916109 |
|   4 |     0.491165 |         0.666333 |             3286    | 0.85926  |
|   5 |     0.424275 |         0.867609 |             3094.08 | 0        |

- Chosen k=3, silhouette=0.517, Davies-Bouldin=0.700
- Aggregate viewing order: R1 -> R3 -> R2

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               4 |            1 |          1114 |           45.15 |             179.8 |                  68.8 |            381 |                        100 |               1 |      618.7 |      326.7 |
|               1 |            2 |           711 |           28.06 |             175   |                   8.3 |           3113 |                        100 |               3 |     1423.5 |      545.5 |
|               3 |            3 |           652 |           26.8  |             182.3 |                  22.9 |           2095 |                        100 |               2 |      565.5 |      818.4 |

## poster_DavidCarson-1990

- Dropped 146 stray/isolated fixations before clustering (5.9%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   3 |     0.570976 |         0.608779 |             4641.38 | 1        |
|   4 |     0.497724 |         0.827164 |             4034.77 | 0.439124 |
|   5 |     0.410621 |         0.937208 |             3740.37 | 0        |

- Chosen k=3, silhouette=0.571, Davies-Bouldin=0.609
- Aggregate viewing order: R3 -> R2 -> R1

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               4 |            1 |           857 |           36.91 |             203.1 |                  20.8 |           2173 |                        100 |               3 |      614.4 |      783.6 |
|               2 |            2 |           815 |           35.54 |             205.7 |                  43.8 |           1151 |                        100 |               2 |     1298.1 |      581.8 |
|               3 |            3 |           663 |           27.56 |             196.1 |                  35.4 |           1088 |                        100 |               1 |      529.7 |      298.5 |

## poster_EllaRosenblatt-2021

- Dropped 163 stray/isolated fixations before clustering (6.4%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   5 |     0.556684 |         0.577281 |             5919.03 | 1        |
|   4 |     0.541319 |         0.61153  |             5621.01 | 0.655718 |
|   3 |     0.485238 |         0.649612 |             3433.65 | 0        |

- Chosen k=5, silhouette=0.557, Davies-Bouldin=0.577
- Aggregate viewing order: R2 -> R1 -> R3 -> R4 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               7 |            1 |           748 |           32.57 |             217.3 |                  22.9 |           1272 |                      100   |               2 |      818.7 |      781   |
|               5 |            2 |           549 |           21.7  |             197.2 |                  62.5 |            870 |                      100   |               1 |      947.4 |      541   |
|               6 |            3 |           543 |           21.36 |             196.3 |                  14.6 |           3570 |                      100   |               3 |     1115.9 |      205.3 |
|               4 |            4 |           454 |           20.43 |             224.6 |                   0   |           4660 |                       97.9 |               4 |     1048.2 |     1065   |
|               8 |            5 |            88 |            3.93 |             223   |                   0   |           8514 |                       83.3 |               5 |      664.1 |     1086   |

## poster_IrisChung-2015

- Dropped 105 stray/isolated fixations before clustering (4.1%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   5 |     0.406617 |         0.82446  |             2771.94 | 0.862878 |
|   3 |     0.425383 |         0.980109 |             2479.45 | 0.648178 |
|   4 |     0.356954 |         1.04566  |             2544.85 | 0        |

- Chosen k=5, silhouette=0.407, Davies-Bouldin=0.824
- Aggregate viewing order: R3 -> R1 -> R4 -> R2 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               6 |            1 |           654 |           24.85 |             188   |                  20.8 |           1135 |                      100   |               2 |      999.3 |      192.2 |
|               4 |            2 |           489 |           22.79 |             230.6 |                  10.4 |           4938 |                      100   |               4 |     1097.6 |      948.4 |
|               5 |            3 |           617 |           22.06 |             176.9 |                  64.6 |            917 |                      100   |               1 |      959.3 |      503.7 |
|               7 |            4 |           416 |           18.85 |             224.3 |                   4.2 |           4639 |                      100   |               3 |      746.6 |      745.7 |
|               8 |            5 |           271 |           11.46 |             209.2 |                   0   |           6934 |                       95.8 |               5 |      738.4 |     1111.4 |

## poster_JanTschichold-1927-DieFrauohneNamen

- Dropped 162 stray/isolated fixations before clustering (6.6%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   5 |     0.484054 |         0.748391 |             3139.16 | 1        |
|   4 |     0.477506 |         0.888583 |             3040.67 | 0.455641 |
|   3 |     0.459918 |         0.919899 |             3035    | 0        |

- Chosen k=5, silhouette=0.484, Davies-Bouldin=0.748
- Aggregate viewing order: R4 -> R5 -> R1 -> R3 -> R2

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |           629 |           26.14 |             201.5 |                  12.5 |           1860 |                      100   |               3 |     1133.7 |      367.5 |
|               5 |            2 |           425 |           21.66 |             247.1 |                   0   |           6377 |                      100   |               5 |     1149.9 |     1031.3 |
|               6 |            3 |           437 |           20.49 |             227.3 |                  14.6 |           3078 |                      100   |               4 |      825.9 |      887.7 |
|               7 |            4 |           518 |           18.87 |             176.6 |                  37.5 |           1365 |                      100   |               1 |      854   |      185.7 |
|               8 |            5 |           295 |           12.84 |             211   |                  35.4 |           1847 |                       97.9 |               2 |      758.5 |      473   |

## poster_JanTschichold-1938-Der

- Dropped 239 stray/isolated fixations before clustering (9.4%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   5 |     0.606179 |         0.520158 |             5389.61 | 1        |
|   4 |     0.520999 |         0.687499 |             3398.77 | 0.162146 |
|   3 |     0.54135  |         0.767811 |             3163    | 0.119461 |

- Chosen k=5, silhouette=0.606, Davies-Bouldin=0.520
- Aggregate viewing order: R3 -> R2 -> R4 -> R1 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               6 |            1 |           542 |           25.82 |             216.5 |                   0   |           5105 |                      100   |               4 |     1471.2 |      949   |
|               3 |            2 |           637 |           25.65 |             183   |                  14.6 |           1558 |                      100   |               2 |      569   |      676.3 |
|               7 |            3 |           423 |           19.11 |             205.3 |                  68.8 |           1063 |                      100   |               1 |     1124.5 |      368.6 |
|               5 |            4 |           432 |           18.45 |             194.1 |                  12.5 |           2687 |                      100   |               3 |     1057.6 |      913.7 |
|               8 |            5 |           265 |           10.98 |             188.3 |                   4.2 |           6006 |                       95.8 |               5 |      664.2 |      103.2 |

## poster_JoostSchmidt-1923-Saatliches

- Dropped 140 stray/isolated fixations before clustering (5.6%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   3 |     0.432323 |         0.789155 |             2323.36 | 0.5      |
|   5 |     0.455652 |         0.885461 |             2723.58 | 0.5      |
|   4 |     0.437726 |         0.8468   |             2644.94 | 0.316513 |

- Chosen k=3, silhouette=0.432, Davies-Bouldin=0.789
- Aggregate viewing order: R2 -> R1 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |           869 |           39.92 |             223.8 |                  31.2 |           1828 |                        100 |               2 |     1069.4 |      702.8 |
|               1 |            2 |           920 |           36.88 |             195.3 |                  58.3 |            567 |                        100 |               1 |      885.8 |      296.1 |
|               4 |            3 |           553 |           23.2  |             204.3 |                  10.4 |           3581 |                        100 |               3 |      800.8 |      761.2 |

## poster_PaulRand-1947

- Dropped 99 stray/isolated fixations before clustering (3.8%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   score |
|----:|-------------:|-----------------:|--------------------:|--------:|
|   3 |     0.54498  |         0.647973 |             3355.21 |  1      |
|   4 |     0.532835 |         0.676212 |             3277.25 |  0.7059 |
|   5 |     0.514739 |         0.799318 |             3493.97 |  0      |

- Chosen k=3, silhouette=0.545, Davies-Bouldin=0.648
- Aggregate viewing order: R1 -> R3 -> R2

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |          1056 |           40.21 |             188.1 |                  60.4 |            517 |                        100 |               1 |      687.9 |      632.6 |
|               1 |            2 |           749 |           33.11 |             218.3 |                   4.2 |           3185 |                        100 |               3 |      953.6 |     1023.1 |
|               4 |            3 |           670 |           26.68 |             196.7 |                  35.4 |           1955 |                        100 |               2 |     1094.2 |      452.4 |

## poster_PaulaScher-1995

- Dropped 77 stray/isolated fixations before clustering (2.8%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   3 |     0.479497 |         0.763238 |             3149.18 | 1        |
|   4 |     0.431761 |         0.829773 |             3717.94 | 0.485722 |
|   5 |     0.39365  |         0.904055 |             3336.28 | 0        |

- Chosen k=3, silhouette=0.479, Davies-Bouldin=0.763
- Aggregate viewing order: R1 -> R3 -> R2

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               2 |            1 |          1509 |           56.25 |             187.9 |                  93.8 |            265 |                        100 |               1 |      952.8 |      302.6 |
|               3 |            2 |           618 |           23.86 |             194.6 |                   4.2 |           5544 |                        100 |               3 |     1125.1 |      889.8 |
|               4 |            3 |           517 |           19.88 |             193.8 |                   2.1 |           4699 |                        100 |               2 |      724.7 |      950.3 |

## poster_ScottBarry-2010

- Dropped 174 stray/isolated fixations before clustering (6.6%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   5 |     0.451753 |         0.729691 |             3323.69 | 1        |
|   4 |     0.449585 |         0.83257  |             3180.12 | 0.772273 |
|   3 |     0.404615 |         0.980947 |             2831.64 | 0        |

- Chosen k=5, silhouette=0.452, Davies-Bouldin=0.730
- Aggregate viewing order: R3 -> R4 -> R1 -> R2 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               4 |            1 |           764 |           33    |             208.6 |                   8.3 |           2792 |                      100   |               3 |     1055.2 |      994.1 |
|               7 |            2 |           507 |           21.45 |             204.3 |                   8.3 |           3319 |                      100   |               4 |     1150.2 |      695.8 |
|               5 |            3 |           513 |           18.5  |             174.1 |                  45.8 |           1162 |                      100   |               1 |      825.3 |      257.2 |
|               8 |            4 |           342 |           13.73 |             193.9 |                  35.4 |           2100 |                      100   |               2 |      871.4 |      649.5 |
|               6 |            5 |           326 |           13.31 |             197.2 |                   2.1 |           3849 |                       95.8 |               5 |     1229.7 |      186.8 |

## poster_SeanAlatorre

- Dropped 96 stray/isolated fixations before clustering (3.9%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   5 |     0.532622 |         0.671141 |             3916.36 | 0.959225 |
|   4 |     0.539963 |         0.75766  |             3499.86 | 0.853792 |
|   3 |     0.449948 |         0.967018 |             2420.79 | 0        |

- Chosen k=5, silhouette=0.533, Davies-Bouldin=0.671
- Aggregate viewing order: R1 -> R5 -> R2 -> R4 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               6 |            1 |           572 |           22.72 |             198.4 |                  31.2 |           1650 |                      100   |               1 |      875.6 |      236   |
|               4 |            2 |           472 |           20.43 |             216.2 |                  29.2 |           2198 |                      100   |               3 |      851.1 |      799.5 |
|               8 |            3 |           438 |           19.88 |             226.8 |                   8.3 |           4556 |                       97.9 |               5 |     1225.8 |      766.5 |
|               7 |            4 |           450 |           19.59 |             217.5 |                  29.2 |           2552 |                      100   |               4 |     1064.2 |      568.5 |
|               5 |            5 |           441 |           17.38 |             196.9 |                   2.1 |           2149 |                       95.8 |               2 |     1262.9 |      127.7 |

## poster_bookcover

- Dropped 103 stray/isolated fixations before clustering (4.0%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   5 |     0.423832 |         0.864823 |             3653.07 | 0.879901 |
|   3 |     0.429473 |         0.903931 |             3591.78 | 0.5      |
|   4 |     0.405987 |         0.893347 |             3486.47 | 0.135322 |

- Chosen k=5, silhouette=0.424, Davies-Bouldin=0.865
- Aggregate viewing order: R3 -> R5 -> R2 -> R4 -> R1

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |           572 |           25.9  |             228.1 |                   0   |           4407 |                        100 |               5 |     1006   |      967.7 |
|               6 |            2 |           558 |           20.85 |             188.2 |                   8.3 |           2328 |                        100 |               3 |     1091.7 |      189.1 |
|               5 |            3 |           535 |           20.26 |             190.7 |                  58.3 |            660 |                        100 |               1 |      882.7 |      329.5 |
|               8 |            4 |           468 |           19.88 |             213.9 |                  10.4 |           3293 |                        100 |               4 |     1067.9 |      708.6 |
|               7 |            5 |           362 |           13.1  |             182.3 |                  22.9 |           1926 |                        100 |               2 |      834.3 |      633.9 |

## poster_nancy

- Dropped 265 stray/isolated fixations before clustering (10.9%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   score |
|----:|-------------:|-----------------:|--------------------:|--------:|
|   4 |     0.533924 |         0.644117 |             3933.18 | 1       |
|   3 |     0.51716  |         0.672859 |             2864.35 | 0.66224 |
|   5 |     0.47016  |         0.713776 |             3567.04 | 0       |

- Chosen k=4, silhouette=0.534, Davies-Bouldin=0.644
- Aggregate viewing order: R4 -> R2 -> R1 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               4 |            1 |           803 |           42.2  |             258.7 |                   8.3 |           2615 |                        100 |               3 |     1088.3 |      775.2 |
|               6 |            2 |           523 |           21.96 |             206.7 |                  39.6 |           1300 |                        100 |               2 |      869.2 |      270.4 |
|               3 |            3 |           401 |           18.16 |             222.9 |                   8.3 |           2733 |                        100 |               4 |      817.3 |      860.8 |
|               5 |            4 |           429 |           17.68 |             202.8 |                  43.8 |            747 |                        100 |               1 |      840.9 |      561.1 |
