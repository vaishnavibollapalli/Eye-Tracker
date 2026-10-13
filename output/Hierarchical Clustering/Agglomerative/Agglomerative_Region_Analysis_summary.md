# Agglomerative (Ward) Region Analysis -- summary

Posters: poster_ArminHofman-1955, poster_BarryCeck-1988, poster_DavidCarson, poster_DavidCarson-1990, poster_EllaRosenblatt-2021, poster_IrisChung-2015, poster_JanTschichold-1927-DieFrauohneNamen, poster_JanTschichold-1938-Der, poster_JoostSchmidt-1923-Saatliches, poster_PaulRand-1947, poster_PaulaScher-1995, poster_ScottBarry-2010, poster_SeanAlatorre, poster_bookcover, poster_nancy
Participants pooled: 48

## poster_ArminHofman-1955

- Dropped 178 stray/isolated fixations before clustering (7.3%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   3 |     0.634745 |         0.434047 |             7139.44 | 1        |
|   4 |     0.559655 |         0.642668 |             8371.37 | 0.491436 |
|   5 |     0.440841 |         0.76526  |             7435.02 | 0        |

- Chosen k=3, silhouette=0.635, Davies-Bouldin=0.434
- Aggregate viewing order: R2 -> R1 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |           914 |           45.81 |             244.7 |                  16.7 |           2347 |                        100 |               2 |     1016.8 |      803.2 |
|               1 |            2 |           995 |           37.9  |             186   |                  83.3 |            340 |                        100 |               1 |     1126.1 |      235.8 |
|               2 |            3 |           364 |           16.28 |             218.4 |                   0   |           5289 |                        100 |               3 |     1218   |     1071.7 |

## poster_BarryCeck-1988

- Dropped 140 stray/isolated fixations before clustering (5.2%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   4 |     0.461482 |         0.738644 |             3102.36 | 1        |
|   5 |     0.432627 |         0.884672 |             2814.27 | 0.245218 |
|   3 |     0.404855 |         0.83799  |             2208.08 | 0.15984  |

- Chosen k=4, silhouette=0.461, Davies-Bouldin=0.739
- Aggregate viewing order: R2 -> R1 -> R3 -> R4

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               4 |            1 |           754 |           31.02 |             184.8 |                  31.2 |           2443 |                        100 |               2 |     1040.2 |      855.7 |
|               1 |            2 |           634 |           24.33 |             172.4 |                  64.6 |            487 |                        100 |               1 |      865.9 |      266.1 |
|               2 |            3 |           633 |           23.7  |             168.2 |                   0   |           3018 |                        100 |               3 |     1414.6 |      335.2 |
|               3 |            4 |           549 |           20.94 |             171.3 |                   4.2 |           5359 |                        100 |               4 |      417.5 |      870.8 |

## poster_DavidCarson

- Dropped 131 stray/isolated fixations before clustering (5.0%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |     score |
|----:|-------------:|-----------------:|--------------------:|----------:|
|   5 |     0.469979 |         0.642555 |             3378.45 | 0.621866  |
|   3 |     0.494751 |         0.743296 |             3286.07 | 0.5       |
|   4 |     0.461996 |         0.731565 |             3211.45 | 0.0582245 |

- Chosen k=5, silhouette=0.470, Davies-Bouldin=0.643
- Aggregate viewing order: R1 -> R3 -> R4 -> R2 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               5 |            1 |          1044 |           42.95 |             182.5 |                  72.9 |            363 |                      100   |               1 |      591.4 |      341.1 |
|               1 |            2 |           552 |           22.12 |             177.8 |                   8.3 |           3707 |                      100   |               4 |     1494   |      574.6 |
|               3 |            3 |           416 |           16.82 |             179.3 |                   2.1 |           3529 |                      100   |               2 |      439.7 |      841.8 |
|               2 |            4 |           265 |           10.78 |             180.5 |                  12.5 |           3646 |                       97.9 |               3 |      861.9 |      810.3 |
|               4 |            5 |           200 |            7.33 |             162.6 |                   4.2 |           7901 |                       83.3 |               5 |     1076.6 |      235.8 |

## poster_DavidCarson-1990

- Dropped 146 stray/isolated fixations before clustering (5.9%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   3 |     0.563963 |         0.627794 |             4525.02 | 1        |
|   4 |     0.487209 |         0.846103 |             3879.96 | 0.290123 |
|   5 |     0.43212  |         0.888433 |             3531.05 | 0        |

- Chosen k=3, silhouette=0.564, Davies-Bouldin=0.628
- Aggregate viewing order: R3 -> R2 -> R1

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               2 |            1 |           836 |           36.17 |             204.1 |                  20.8 |           2270 |                        100 |               3 |      611.2 |      789   |
|               1 |            2 |           798 |           34.82 |             205.8 |                  37.5 |           1359 |                        100 |               2 |     1305   |      583.3 |
|               3 |            3 |           701 |           29.01 |             195.2 |                  41.7 |           1042 |                        100 |               1 |      546.5 |      309.3 |

## poster_EllaRosenblatt-2021

- Dropped 163 stray/isolated fixations before clustering (6.4%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   5 |     0.574095 |         0.583619 |             5886.91 | 1        |
|   4 |     0.559887 |         0.628231 |             5931.58 | 0.681199 |
|   3 |     0.505372 |         0.687163 |             4239.23 | 0        |

- Chosen k=5, silhouette=0.574, Davies-Bouldin=0.584
- Aggregate viewing order: R1 -> R2 -> R3 -> R4 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               5 |            1 |           724 |           28.79 |             198.4 |                  75   |            428 |                      100   |               1 |      926.4 |      569.5 |
|               3 |            2 |           638 |           27.93 |             218.4 |                  10.4 |           1995 |                      100   |               2 |      823.7 |      821.6 |
|               4 |            3 |           543 |           21.36 |             196.3 |                  14.6 |           3570 |                      100   |               3 |     1115.9 |      205.3 |
|               1 |            4 |           396 |           18.35 |             231.2 |                   0   |           5070 |                       93.8 |               4 |     1048.4 |     1086.9 |
|               2 |            5 |            81 |            3.57 |             219.8 |                   0   |           8577 |                       77.1 |               5 |      656.3 |     1100.5 |

## poster_IrisChung-2015

- Dropped 105 stray/isolated fixations before clustering (4.1%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   4 |     0.431304 |         0.730366 |             2653.82 | 1        |
|   5 |     0.426887 |         0.883131 |             2721.49 | 0.321864 |
|   3 |     0.421626 |         0.900135 |             2937.87 | 0        |

- Chosen k=4, silhouette=0.431, Davies-Bouldin=0.730
- Aggregate viewing order: R2 -> R1 -> R4 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               2 |            1 |          1100 |           45.28 |             203.7 |                  43.8 |           1229 |                      100   |               2 |      886.1 |      673.4 |
|               1 |            2 |           798 |           29.97 |             185.9 |                  54.2 |            737 |                      100   |               1 |      999.9 |      227.1 |
|               4 |            3 |           275 |           13.22 |             237.9 |                   2.1 |           7770 |                       95.8 |               4 |     1128.6 |     1072   |
|               3 |            4 |           274 |           11.54 |             208.4 |                   0   |           6934 |                       95.8 |               3 |      739.6 |     1111.3 |

## poster_JanTschichold-1927-DieFrauohneNamen

- Dropped 162 stray/isolated fixations before clustering (6.6%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   5 |     0.501311 |         0.669107 |             3451.51 | 1        |
|   4 |     0.444531 |         0.810485 |             2947.32 | 0.411762 |
|   3 |     0.411356 |         0.928384 |             2647.9  | 0        |

- Chosen k=5, silhouette=0.501, Davies-Bouldin=0.669
- Aggregate viewing order: R2 -> R1 -> R4 -> R3 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |           632 |           27.98 |             214.6 |                  31.2 |           2094 |                      100   |               2 |      960.7 |      657.3 |
|               2 |            2 |           692 |           26.77 |             187.6 |                  64.6 |            437 |                      100   |               1 |      789.9 |      318.4 |
|               4 |            3 |           420 |           21.53 |             248.5 |                   0   |           6552 |                      100   |               4 |     1150.3 |     1032.6 |
|               1 |            4 |           434 |           18.01 |             201.1 |                   4.2 |           2287 |                      100   |               3 |     1144.7 |      211.8 |
|               5 |            5 |           126 |            5.71 |             219.8 |                   0   |           9792 |                       72.9 |               5 |      685.6 |     1181.5 |

## poster_JanTschichold-1938-Der

- Dropped 239 stray/isolated fixations before clustering (9.4%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   score |
|----:|-------------:|-----------------:|--------------------:|--------:|
|   5 |     0.642007 |         0.475168 |             6060.82 | 1       |
|   4 |     0.567742 |         0.619306 |             3708.46 | 0.64528 |
|   3 |     0.446174 |         0.911666 |             2486.75 | 0       |

- Chosen k=5, silhouette=0.642, Davies-Bouldin=0.475
- Aggregate viewing order: R3 -> R1 -> R4 -> R2 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               5 |            1 |           698 |           29.1  |             189.4 |                  14.6 |           1951 |                      100   |               2 |      974   |      888   |
|               3 |            2 |           508 |           24.51 |             219.3 |                   0   |           5287 |                      100   |               4 |     1477.5 |      953.9 |
|               4 |            3 |           427 |           19.22 |             204.5 |                  68.8 |           1063 |                      100   |               1 |     1124.6 |      369.9 |
|               2 |            4 |           401 |           16.2  |             183.6 |                  12.5 |           2850 |                      100   |               3 |      457.3 |      581.5 |
|               1 |            5 |           265 |           10.98 |             188.3 |                   4.2 |           6006 |                       95.8 |               5 |      664.2 |      103.2 |

## poster_JoostSchmidt-1923-Saatliches

- Dropped 140 stray/isolated fixations before clustering (5.6%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   5 |     0.499273 |         0.689857 |             2971.55 | 0.774718 |
|   3 |     0.524177 |         0.789105 |             2753.47 | 0.568534 |
|   4 |     0.468904 |         0.80487  |             2668.57 | 0        |

- Chosen k=5, silhouette=0.499, Davies-Bouldin=0.690
- Aggregate viewing order: R2 -> R1 -> R4 -> R3 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               4 |            1 |           706 |           32.62 |             225.1 |                  35.4 |           1935 |                      100   |               2 |     1008.7 |      738.5 |
|               1 |            2 |           729 |           27.93 |             186.6 |                  52.1 |            708 |                      100   |               1 |      788.7 |      305   |
|               5 |            3 |           485 |           20.27 |             203.5 |                   8.3 |           3787 |                      100   |               4 |      784.6 |      763.9 |
|               3 |            4 |           360 |           15.1  |             204.3 |                   4.2 |           3756 |                      100   |               3 |     1170.9 |      541.1 |
|               2 |            5 |            62 |            4.09 |             321.4 |                   0   |           8008 |                       60.4 |               5 |     1327.6 |       92   |

## poster_PaulRand-1947

- Dropped 99 stray/isolated fixations before clustering (3.8%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   3 |     0.507547 |         0.714057 |             2925.64 | 1        |
|   5 |     0.499444 |         0.772648 |             3233.74 | 0.243449 |
|   4 |     0.501606 |         0.828247 |             2837.88 | 0.133381 |

- Chosen k=3, silhouette=0.508, Davies-Bouldin=0.714
- Aggregate viewing order: R1 -> R3 -> R2

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               2 |            1 |           912 |           33.99 |             184.1 |                  41.7 |            591 |                        100 |               1 |      660.8 |      621.1 |
|               1 |            2 |           751 |           33.2  |             218.4 |                   0   |           3276 |                        100 |               3 |      941.7 |     1022.4 |
|               3 |            3 |           812 |           32.81 |             199.6 |                  58.3 |           1217 |                        100 |               2 |     1057.7 |      497.4 |

## poster_PaulaScher-1995

- Dropped 77 stray/isolated fixations before clustering (2.8%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   4 |     0.448961 |         0.772845 |             3619.64 | 0.549093 |
|   5 |     0.411577 |         0.722591 |             3271.49 | 0.5      |
|   3 |     0.438975 |         0.778317 |             3298.9  | 0.366437 |

- Chosen k=4, silhouette=0.449, Davies-Bouldin=0.773
- Aggregate viewing order: R1 -> R3 -> R2 -> R4

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |          1030 |           38.73 |             189.5 |                  91.7 |            269 |                      100   |               1 |      871.7 |      241.7 |
|               4 |            2 |           632 |           23.2  |             185.1 |                   2.1 |           4538 |                      100   |               3 |     1170.6 |      505.5 |
|               2 |            3 |           586 |           22.6  |             194.4 |                   4.2 |           3694 |                      100   |               2 |      734.3 |      912.6 |
|               1 |            4 |           396 |           15.46 |             196.8 |                   2.1 |           6998 |                       93.8 |               4 |     1121.4 |      998.2 |

## poster_ScottBarry-2010

- Dropped 174 stray/isolated fixations before clustering (6.6%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   5 |     0.520775 |         0.663624 |             3962.86 | 1        |
|   4 |     0.481038 |         0.740793 |             3291.01 | 0.611451 |
|   3 |     0.439504 |         0.931438 |             3038.24 | 0        |

- Chosen k=5, silhouette=0.521, Davies-Bouldin=0.664
- Aggregate viewing order: R4 -> R3 -> R2 -> R1 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |           741 |           32.15 |             209.5 |                   8.3 |           2877 |                      100   |               4 |     1048.8 |      997.2 |
|               5 |            2 |           603 |           25.01 |             200.3 |                  12.5 |           2761 |                      100   |               3 |     1153.6 |      682.4 |
|               4 |            3 |           424 |           16.65 |             189.6 |                  52.1 |           1481 |                      100   |               2 |      868.1 |      613.5 |
|               2 |            4 |           417 |           15.09 |             174.8 |                  27.1 |           1478 |                      100   |               1 |      815.2 |      203.7 |
|               1 |            5 |           267 |           11.1  |             200.8 |                   0   |           4374 |                       95.8 |               5 |     1241.7 |      134.3 |

## poster_SeanAlatorre

- Dropped 96 stray/isolated fixations before clustering (3.9%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   3 |     0.542216 |         0.567759 |             2827.07 | 1        |
|   4 |     0.533281 |         0.74855  |             3416.43 | 0.384487 |
|   5 |     0.503541 |         0.68524  |             3635.4  | 0.175091 |

- Chosen k=3, silhouette=0.542, Davies-Bouldin=0.568
- Aggregate viewing order: R2 -> R1 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               1 |            1 |          1323 |           58.7  |             221.7 |                  47.9 |           1815 |                      100   |               2 |     1048.3 |      716.7 |
|               3 |            2 |           609 |           23.92 |             196.2 |                  50   |           1385 |                      100   |               1 |      876.5 |      250.9 |
|               2 |            3 |           441 |           17.38 |             196.9 |                   2.1 |           2149 |                       95.8 |               3 |     1262.9 |      127.7 |

## poster_bookcover

- Dropped 103 stray/isolated fixations before clustering (4.0%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   5 |     0.473305 |         0.748898 |             3763.79 | 0.888805 |
|   4 |     0.43919  |         0.714248 |             3474.49 | 0.567406 |
|   3 |     0.433874 |         0.870056 |             3723.52 | 0        |

- Chosen k=5, silhouette=0.473, Davies-Bouldin=0.749
- Aggregate viewing order: R2 -> R1 -> R3 -> R5 -> R4

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |           723 |           29.07 |             202.5 |                  18.8 |           1637 |                        100 |               2 |     1007.7 |      190.7 |
|               5 |            2 |           696 |           23.16 |             167.5 |                  70.8 |            721 |                        100 |               1 |      901.3 |      503.1 |
|               2 |            3 |           435 |           20.17 |             233.5 |                   8.3 |           3887 |                        100 |               3 |      896.3 |      814.3 |
|               1 |            4 |           435 |           19.02 |             220.2 |                   0   |           4752 |                        100 |               5 |     1078.1 |      992.6 |
|               4 |            5 |           206 |            8.58 |             209.7 |                   2.1 |           4276 |                        100 |               4 |     1179.3 |      650.1 |

## poster_nancy

- Dropped 265 stray/isolated fixations before clustering (10.9%)
- k selection (silhouette + Davies-Bouldin separation score by k):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |    score |
|----:|-------------:|-----------------:|--------------------:|---------:|
|   4 |     0.588227 |         0.557326 |             4593.7  | 1        |
|   5 |     0.531395 |         0.59864  |             4082.44 | 0.606785 |
|   3 |     0.495367 |         0.794202 |             2959.74 | 0        |

- Chosen k=4, silhouette=0.588, Davies-Bouldin=0.557
- Aggregate viewing order: R2 -> R3 -> R1 -> R4

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               2 |            1 |           725 |           39.03 |             265   |                   2.1 |           3089 |                        100 |               3 |     1097   |      784   |
|               3 |            2 |           587 |           24.14 |             202.4 |                  56.2 |            671 |                        100 |               1 |      859.3 |      590.1 |
|               1 |            3 |           525 |           22.11 |             207.3 |                  39.6 |           1300 |                        100 |               2 |      870.7 |      271.5 |
|               4 |            4 |           319 |           14.72 |             227.1 |                   2.1 |           3856 |                        100 |               4 |      809.1 |      907.1 |
