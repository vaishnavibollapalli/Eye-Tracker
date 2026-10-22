# Agglomerative (Ward) Region Analysis -- summary

Posters: poster_ArminHofman-1955, poster_BarryCeck-1988, poster_DavidCarson, poster_DavidCarson-1990, poster_EllaRosenblatt-2021, poster_IrisChung-2015, poster_JanTschichold-1927-DieFrauohneNamen, poster_JanTschichold-1938-Der, poster_JoostSchmidt-1923-Saatliches, poster_PaulRand-1947, poster_PaulaScher-1995, poster_ScottBarry-2010, poster_SeanAlatorre, poster_bookcover, poster_nancy
Participants pooled: 48

## poster_ArminHofman-1955

- Dropped 178 stray/isolated fixations before clustering (7.3%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.634745 |         0.434047 |             7139.44 | False     | 1        | True     |
|   4 |     0.559655 |         0.642668 |             8371.37 | False     | 0.590009 | False    |
|   5 |     0.440841 |         0.76526  |             7435.02 | False     | 0.196731 | False    |
|   6 |     0.389636 |         0.840221 |             7215.46 | True      | 0        | False    |
|   7 |     0.409726 |         0.730827 |             7490.68 | True      | 0.175645 | False    |
|   8 |     0.421281 |         0.765993 |             7559.32 | False     | 0.155926 | False    |

- Chosen k=3, silhouette=0.635, Davies-Bouldin=0.434
- Aggregate viewing order: R2 -> R1 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |           914 |           45.81 |             244.7 |                  16.7 |           2347 |                        100 |               2 |     1016.8 |      803.2 |
|               1 |            2 |           995 |           37.9  |             186   |                  83.3 |            340 |                        100 |               1 |     1126.1 |      235.8 |
|               2 |            3 |           364 |           16.28 |             218.4 |                   0   |           5289 |                        100 |               3 |     1218   |     1071.7 |

## poster_BarryCeck-1988

- Dropped 140 stray/isolated fixations before clustering (5.2%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.404855 |         0.83799  |             2208.08 | False     | 0.27163  | False    |
|   4 |     0.461482 |         0.738644 |             3102.36 | False     | 1        | True     |
|   5 |     0.432627 |         0.884672 |             2814.27 | False     | 0.324574 | False    |
|   6 |     0.394587 |         0.865213 |             2764.54 | False     | 0.110188 | False    |
|   7 |     0.408144 |         0.862062 |             2816.16 | False     | 0.21876  | False    |
|   8 |     0.392681 |         0.895418 |             2982.61 | False     | 0        | False    |

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
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.494751 |         0.743296 |             3286.07 | False     | 0.5      | False    |
|   4 |     0.461996 |         0.731565 |             3211.45 | False     | 0.272379 | False    |
|   5 |     0.469979 |         0.642555 |             3378.45 | False     | 0.783824 | False    |
|   6 |     0.482362 |         0.648742 |             3742.78 | False     | 0.861174 | False    |
|   7 |     0.46831  |         0.655312 |             3831.78 | False     | 0.705946 | False    |
|   8 |     0.437455 |         0.711629 |             3974.5  | False     | 0.157169 | True     |

- Chosen k=8, silhouette=0.437, Davies-Bouldin=0.712
- Aggregate viewing order: R1 -> R4 -> R2 -> R8 -> R5 -> R3 -> R7 -> R6

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               8 |            1 |           597 |           23.16 |             172   |                  47.9 |           1320 |                      100   |               1 |      703.1 |      314.6 |
|               4 |            2 |           416 |           16.82 |             179.3 |                   2.1 |           3529 |                      100   |               3 |      439.7 |      841.8 |
|               2 |            3 |           394 |           15.72 |             177   |                   8.3 |           3807 |                      100   |               6 |     1405.4 |      599.1 |
|               7 |            4 |           271 |           13.51 |             221.1 |                  20.8 |           1650 |                       97.9 |               2 |      537.5 |      461.5 |
|               3 |            5 |           265 |           10.78 |             180.5 |                  12.5 |           3646 |                       97.9 |               5 |      861.9 |      810.3 |
|               5 |            6 |           200 |            7.33 |             162.6 |                   4.2 |           7901 |                       83.3 |               8 |     1076.6 |      235.8 |
|               1 |            7 |           158 |            6.4  |             179.6 |                   0   |           6842 |                       93.8 |               7 |     1711.6 |      514.7 |
|               6 |            8 |           176 |            6.29 |             158.4 |                   4.2 |           3578 |                       89.6 |               4 |      295.7 |      180.3 |

## poster_DavidCarson-1990

- Dropped 146 stray/isolated fixations before clustering (5.9%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.563963 |         0.627794 |             4525.02 | False     | 1        | True     |
|   4 |     0.487209 |         0.846103 |             3879.96 | False     | 0.526593 | False    |
|   5 |     0.43212  |         0.888433 |             3531.05 | True      | 0.327639 | False    |
|   6 |     0.376363 |         1.03382  |             3461.06 | True      | 0        | False    |
|   7 |     0.391284 |         0.863785 |             3494.32 | True      | 0.249155 | False    |
|   8 |     0.390704 |         0.82936  |             3494.42 | True      | 0.290003 | False    |

- Chosen k=3, silhouette=0.564, Davies-Bouldin=0.628
- Aggregate viewing order: R3 -> R2 -> R1

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               2 |            1 |           836 |           36.17 |             204.1 |                  20.8 |           2270 |                        100 |               3 |      611.2 |      789   |
|               1 |            2 |           798 |           34.82 |             205.8 |                  37.5 |           1359 |                        100 |               2 |     1305   |      583.3 |
|               3 |            3 |           701 |           29.01 |             195.2 |                  41.7 |           1042 |                        100 |               1 |      546.5 |      309.3 |

## poster_EllaRosenblatt-2021

- Dropped 163 stray/isolated fixations before clustering (6.4%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.505372 |         0.687163 |             4239.23 | False     | 0.147788 | False    |
|   4 |     0.559887 |         0.628231 |             5931.58 | False     | 0.744874 | False    |
|   5 |     0.574095 |         0.583619 |             5886.91 | False     | 1        | False    |
|   6 |     0.571654 |         0.603576 |             6084.71 | False     | 0.914351 | True     |
|   7 |     0.52762  |         0.73061  |             6350.91 | False     | 0.161869 | False    |
|   8 |     0.523232 |         0.704987 |             6313.47 | False     | 0.2171   | False    |

- Chosen k=6, silhouette=0.572, Davies-Bouldin=0.604
- Aggregate viewing order: R1 -> R2 -> R3 -> R5 -> R4 -> R6

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               6 |            1 |           724 |           28.79 |             198.4 |                  75   |            428 |                      100   |               1 |      926.4 |      569.5 |
|               3 |            2 |           477 |           21.56 |             225.5 |                   2.1 |           2758 |                       97.9 |               2 |      776.5 |      824.6 |
|               5 |            3 |           543 |           21.36 |             196.3 |                  14.6 |           3570 |                      100   |               3 |     1115.9 |      205.3 |
|               1 |            4 |           396 |           18.35 |             231.2 |                   0   |           5070 |                       93.8 |               5 |     1048.4 |     1086.9 |
|               4 |            5 |           161 |            6.37 |             197.5 |                   8.3 |           3828 |                       95.8 |               4 |      983.5 |      811.5 |
|               2 |            6 |            81 |            3.57 |             219.8 |                   0   |           8577 |                       77.1 |               6 |      656.3 |     1100.5 |

## poster_IrisChung-2015

- Dropped 105 stray/isolated fixations before clustering (4.1%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.421626 |         0.900135 |             2937.87 | False     | 0        | False    |
|   4 |     0.431304 |         0.730366 |             2653.82 | False     | 0.533896 | False    |
|   5 |     0.426887 |         0.883131 |             2721.49 | True      | 0.112853 | False    |
|   6 |     0.431146 |         0.732726 |             2881.49 | False     | 0.526144 | False    |
|   7 |     0.426623 |         0.744812 |             3099.66 | False     | 0.435092 | False    |
|   8 |     0.45776  |         0.687914 |             3302.75 | False     | 1        | True     |

- Chosen k=8, silhouette=0.458, Davies-Bouldin=0.688
- Aggregate viewing order: R1 -> R3 -> R8 -> R6 -> R2 -> R7 -> R5 -> R4

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               2 |            1 |           613 |           23.26 |             187.8 |                  43.8 |            876 |                      100   |               1 |     1052.3 |      256.5 |
|               3 |            2 |           280 |           13.76 |             243.3 |                   0   |           5525 |                       97.9 |               5 |      693.3 |      730.3 |
|               6 |            3 |           395 |           13.52 |             169.4 |                  31.2 |           1651 |                      100   |               2 |      881.6 |      520.6 |
|               8 |            4 |           275 |           13.22 |             237.9 |                   2.1 |           7770 |                       95.8 |               8 |     1128.6 |     1072   |
|               7 |            5 |           274 |           11.54 |             208.4 |                   0   |           6934 |                       95.8 |               7 |      739.6 |     1111.3 |
|               4 |            6 |           231 |            9.72 |             208.4 |                  10.4 |           5414 |                      100   |               4 |      932.4 |      806.7 |
|               5 |            7 |           194 |            8.27 |             211   |                   2.1 |           6104 |                       91.7 |               6 |     1159.6 |      671.6 |
|               1 |            8 |           185 |            6.71 |             179.5 |                  10.4 |           2290 |                      100   |               3 |      818   |      125.2 |

## poster_JanTschichold-1927-DieFrauohneNamen

- Dropped 162 stray/isolated fixations before clustering (6.6%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.411356 |         0.928384 |             2647.9  | False     | 0        | False    |
|   4 |     0.444531 |         0.810485 |             2947.32 | False     | 0.239419 | False    |
|   5 |     0.501311 |         0.669107 |             3451.51 | False     | 0.572537 | False    |
|   6 |     0.529391 |         0.597602 |             4105.41 | False     | 0.739293 | False    |
|   7 |     0.573001 |         0.556941 |             5446.25 | False     | 0.908964 | False    |
|   8 |     0.596021 |         0.534316 |             6934.33 | False     | 1        | True     |

- Chosen k=8, silhouette=0.596, Davies-Bouldin=0.534
- Aggregate viewing order: R3 -> R5 -> R6 -> R2 -> R4 -> R7 -> R1 -> R8

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               7 |            1 |           420 |           21.53 |             248.5 |                   0   |           6552 |                      100   |               7 |     1150.3 |     1032.6 |
|               5 |            2 |           318 |           15.03 |             229.2 |                  16.7 |           3053 |                      100   |               4 |      877.2 |      772.1 |
|               4 |            3 |           420 |           14.85 |             171.4 |                  33.3 |           1558 |                      100   |               1 |      822.2 |      199.3 |
|               6 |            4 |           314 |           12.94 |             199.8 |                  14.6 |           3897 |                       97.9 |               5 |     1057.7 |      524.1 |
|               3 |            5 |           272 |           11.93 |             212.5 |                  31.2 |           1967 |                       97.9 |               2 |      749.6 |      466.6 |
|               2 |            6 |           241 |            9.65 |             194.1 |                   4.2 |           2624 |                       93.8 |               3 |     1040.5 |      149   |
|               1 |            7 |           193 |            8.36 |             209.9 |                   0   |           5231 |                       87.5 |               6 |     1264.9 |      284.2 |
|               8 |            8 |           126 |            5.71 |             219.8 |                   0   |           9792 |                       72.9 |               8 |      685.6 |     1181.5 |

## poster_JanTschichold-1938-Der

- Dropped 239 stray/isolated fixations before clustering (9.4%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.446174 |         0.911666 |             2486.75 | False     | 0        | False    |
|   4 |     0.567742 |         0.619306 |             3708.46 | False     | 0.64528  | False    |
|   5 |     0.642007 |         0.475168 |             6060.82 | False     | 1        | False    |
|   6 |     0.634442 |         0.490378 |             7998.33 | False     | 0.963263 | True     |
|   7 |     0.601379 |         0.587978 |             7966.82 | False     | 0.767046 | False    |
|   8 |     0.602353 |         0.6105   |             8387.94 | False     | 0.743736 | False    |

- Chosen k=6, silhouette=0.634, Davies-Bouldin=0.490
- Aggregate viewing order: R3 -> R2 -> R4 -> R6 -> R1 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |           508 |           24.51 |             219.3 |                   0   |           5287 |                      100   |               5 |     1477.5 |      953.9 |
|               6 |            2 |           474 |           20.07 |             192.5 |                  12.5 |           2590 |                      100   |               2 |     1073.2 |      909.4 |
|               4 |            3 |           427 |           19.22 |             204.5 |                  68.8 |           1063 |                      100   |               1 |     1124.6 |      369.9 |
|               2 |            4 |           401 |           16.2  |             183.6 |                  12.5 |           2850 |                      100   |               3 |      457.3 |      581.5 |
|               1 |            5 |           265 |           10.98 |             188.3 |                   4.2 |           6006 |                       95.8 |               6 |      664.2 |      103.2 |
|               5 |            6 |           224 |            9.02 |             183   |                   2.1 |           2989 |                      100   |               4 |      753.3 |      840.3 |

## poster_JoostSchmidt-1923-Saatliches

- Dropped 140 stray/isolated fixations before clustering (5.6%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.524177 |         0.789105 |             2753.47 | False     | 0.544005 | True     |
|   4 |     0.468904 |         0.80487  |             2668.57 | True      | 0.175824 | False    |
|   5 |     0.499273 |         0.689857 |             2971.55 | True      | 0.674979 | False    |
|   6 |     0.440778 |         0.72296  |             3013.33 | True      | 0.239496 | False    |
|   7 |     0.457683 |         0.628527 |             3313.72 | True      | 0.602242 | False    |
|   8 |     0.438926 |         0.625746 |             3353.65 | True      | 0.5      | False    |

- Chosen k=3, silhouette=0.524, Davies-Bouldin=0.789
- Aggregate viewing order: R2 -> R1 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |          1191 |           52.88 |             216.3 |                  43.8 |           1341 |                        100 |               2 |      922.8 |      748.2 |
|               1 |            2 |           729 |           27.93 |             186.6 |                  52.1 |            708 |                        100 |               1 |      788.7 |      305   |
|               2 |            3 |           422 |           19.19 |             221.5 |                   4.2 |           3480 |                        100 |               3 |     1204.3 |      445.4 |

## poster_PaulRand-1947

- Dropped 99 stray/isolated fixations before clustering (3.8%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.507547 |         0.714057 |             2925.64 | False     | 0.873193 | False    |
|   4 |     0.501606 |         0.828247 |             2837.88 | False     | 0.215218 | False    |
|   5 |     0.499444 |         0.772648 |             3233.74 | False     | 0.315595 | False    |
|   6 |     0.508149 |         0.685288 |             3336.97 | False     | 1        | False    |
|   7 |     0.496661 |         0.746618 |             3400.32 | False     | 0.285496 | False    |
|   8 |     0.498171 |         0.718638 |             3382.43 | False     | 0.449087 | True     |

- Chosen k=8, silhouette=0.498, Davies-Bouldin=0.719
- Aggregate viewing order: R1 -> R2 -> R7 -> R4 -> R5 -> R6 -> R3 -> R8

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               4 |            1 |           912 |           33.99 |             184.1 |                  41.7 |            591 |                      100   |               1 |      660.8 |      621.1 |
|               8 |            2 |           315 |           12.75 |             200   |                  33.3 |           1842 |                       97.9 |               2 |      949.3 |      640.8 |
|               3 |            3 |           285 |           12.26 |             212.5 |                   0   |           5313 |                       97.9 |               7 |      739.8 |     1028.1 |
|               1 |            4 |           228 |           10.92 |             236.6 |                   0   |           4262 |                       97.9 |               4 |     1158.7 |      963.9 |
|               6 |            5 |           258 |           10.55 |             202   |                   0   |           4961 |                       95.8 |               5 |     1224.2 |      379.5 |
|               2 |            6 |           238 |           10.02 |             207.9 |                   0   |           5228 |                      100   |               6 |      952.1 |     1079.4 |
|               7 |            7 |           169 |            6.77 |             198   |                  25   |           4085 |                       95.8 |               3 |      908.6 |      354.3 |
|               5 |            8 |            70 |            2.73 |             192.6 |                   0   |           8720 |                       75   |               8 |     1290.8 |      638.4 |

## poster_PaulaScher-1995

- Dropped 77 stray/isolated fixations before clustering (2.8%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |      score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|-----------:|:---------|
|   3 |     0.438975 |         0.778317 |             3298.9  | False     | 0.666201   | False    |
|   4 |     0.448961 |         0.772845 |             3619.64 | False     | 0.768694   | False    |
|   5 |     0.411577 |         0.722591 |             3271.49 | True      | 0.710586   | False    |
|   6 |     0.384527 |         0.831223 |             3202.31 | True      | 0.00118236 | False    |
|   7 |     0.384374 |         0.797244 |             3260.58 | True      | 0.156395   | False    |
|   8 |     0.414514 |         0.751423 |             3470.12 | False     | 0.600626   | True     |

- Chosen k=8, silhouette=0.415, Davies-Bouldin=0.751
- Aggregate viewing order: R4 -> R2 -> R7 -> R8 -> R1 -> R5 -> R6 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |           484 |           18.94 |             197.2 |                   4.2 |           4944 |                       97.9 |               5 |      744.9 |      964.4 |
|               6 |            2 |           438 |           15.68 |             180.4 |                  18.8 |           1891 |                       97.9 |               2 |      961.5 |      161   |
|               1 |            3 |           396 |           15.46 |             196.8 |                   2.1 |           6998 |                       93.8 |               8 |     1121.4 |      998.2 |
|               5 |            4 |           357 |           14.64 |             206.7 |                  68.8 |            527 |                      100   |               1 |      881.8 |      350.5 |
|               8 |            5 |           359 |           13.05 |             183.2 |                   2.1 |           5939 |                       97.9 |               6 |     1151.9 |      622   |
|               7 |            6 |           273 |           10.16 |             187.5 |                   0   |           5939 |                       93.8 |               7 |     1194.7 |      355.8 |
|               4 |            7 |           235 |            8.41 |             180.4 |                   4.2 |           2970 |                      100   |               3 |      686.6 |      202.5 |
|               2 |            8 |           102 |            3.66 |             181.1 |                   0   |           4816 |                       81.2 |               4 |      679.4 |      645   |

## poster_ScottBarry-2010

- Dropped 174 stray/isolated fixations before clustering (6.6%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.439504 |         0.931438 |             3038.24 | False     | 0        | False    |
|   4 |     0.481038 |         0.740793 |             3291.01 | False     | 0.400452 | False    |
|   5 |     0.520775 |         0.663624 |             3962.86 | False     | 0.643567 | False    |
|   6 |     0.580989 |         0.568779 |             5655.53 | False     | 0.98256  | False    |
|   7 |     0.56901  |         0.555672 |             5535.68 | False     | 0.957666 | False    |
|   8 |     0.560913 |         0.575412 |             5571.38 | False     | 0.902785 | True     |

- Chosen k=8, silhouette=0.561, Davies-Bouldin=0.575
- Aggregate viewing order: R3 -> R2 -> R1 -> R7 -> R6 -> R4 -> R8 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |           488 |           20.24 |             200.3 |                   8.3 |           2898 |                      100   |               3 |      930.3 |      966.4 |
|               5 |            2 |           424 |           16.65 |             189.6 |                  52.1 |           1481 |                      100   |               2 |      868.1 |      613.5 |
|               2 |            3 |           417 |           15.09 |             174.8 |                  27.1 |           1478 |                      100   |               1 |      815.2 |      203.7 |
|               8 |            4 |           315 |           12.6  |             193.1 |                   0   |           5004 |                      100   |               6 |     1220.3 |      717.8 |
|               4 |            5 |           253 |           11.9  |             227.2 |                   0   |           7641 |                       97.9 |               8 |     1250.2 |     1049.7 |
|               1 |            6 |           267 |           11.1  |             200.8 |                   0   |           4374 |                       95.8 |               5 |     1241.7 |      134.3 |
|               7 |            7 |           215 |            9.61 |             215.9 |                  10.4 |           3764 |                       89.6 |               4 |     1059.4 |      697.6 |
|               6 |            8 |            73 |            2.8  |             185.1 |                   2.1 |           6982 |                       56.2 |               7 |     1176.7 |      470.3 |

## poster_SeanAlatorre

- Dropped 96 stray/isolated fixations before clustering (3.9%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.542216 |         0.567759 |             2827.07 | False     | 1        | False    |
|   4 |     0.533281 |         0.74855  |             3416.43 | False     | 0.465448 | False    |
|   5 |     0.503541 |         0.68524  |             3635.4  | False     | 0.227701 | False    |
|   6 |     0.539256 |         0.626256 |             4041.22 | False     | 0.826151 | True     |
|   7 |     0.540695 |         0.718694 |             4067.39 | False     | 0.630493 | False    |
|   8 |     0.520741 |         0.78348  |             4348.41 | False     | 0.222368 | False    |

- Chosen k=6, silhouette=0.539, Davies-Bouldin=0.626
- Aggregate viewing order: R2 -> R3 -> R5 -> R1 -> R4 -> R6

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               4 |            1 |           559 |           25.16 |             224.8 |                  12.5 |           3755 |                      100   |               4 |     1188   |      761.7 |
|               6 |            2 |           609 |           23.92 |             196.2 |                  50   |           1385 |                      100   |               1 |      876.5 |      250.9 |
|               5 |            3 |           441 |           17.38 |             196.9 |                   2.1 |           2149 |                       95.8 |               2 |     1262.9 |      127.7 |
|               3 |            4 |           339 |           14.89 |             219.4 |                  10.4 |           4564 |                       97.9 |               5 |     1075.5 |      539.7 |
|               1 |            5 |           273 |           11.39 |             208.4 |                  25   |           2538 |                      100   |               3 |      846   |      674.7 |
|               2 |            6 |           152 |            7.27 |             239   |                   0   |           7583 |                       87.5 |               6 |      826.2 |      989.1 |

## poster_bookcover

- Dropped 103 stray/isolated fixations before clustering (4.0%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.433874 |         0.870056 |             3723.52 | False     | 0        | False    |
|   4 |     0.43919  |         0.714248 |             3474.49 | False     | 0.419419 | False    |
|   5 |     0.473305 |         0.748898 |             3763.79 | False     | 0.529702 | False    |
|   6 |     0.47803  |         0.69868  |             4074.36 | False     | 0.682251 | False    |
|   7 |     0.490843 |         0.787149 |             4473.67 | False     | 0.535399 | False    |
|   8 |     0.520576 |         0.669666 |             5217.05 | False     | 1        | True     |

- Chosen k=8, silhouette=0.521, Davies-Bouldin=0.670
- Aggregate viewing order: R5 -> R4 -> R6 -> R2 -> R3 -> R7 -> R1 -> R8

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               1 |            1 |           435 |           19.02 |             220.2 |                   0   |           4752 |                      100   |               7 |     1078.1 |      992.6 |
|               5 |            2 |           484 |           18.39 |             191.3 |                   6.2 |           3289 |                      100   |               4 |     1093.5 |      172.6 |
|               3 |            3 |           286 |           12.56 |             221.2 |                   8.3 |           4244 |                       97.9 |               5 |      976.3 |      770.2 |
|               7 |            4 |           346 |           11.83 |             172.2 |                  29.2 |           2010 |                      100   |               2 |      859.5 |      587   |
|               8 |            5 |           350 |           11.33 |             163   |                  41.7 |           1111 |                       97.9 |               1 |      944.9 |      415.5 |
|               4 |            6 |           239 |           10.68 |             225.1 |                  12.5 |           2322 |                       97.9 |               3 |      860.1 |      221.7 |
|               6 |            7 |           206 |            8.58 |             209.7 |                   2.1 |           4276 |                      100   |               6 |     1179.3 |      650.1 |
|               2 |            8 |           149 |            7.61 |             257.2 |                   0   |           6188 |                       95.8 |               8 |      764.3 |      887.1 |

## poster_nancy

- Dropped 265 stray/isolated fixations before clustering (10.9%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.495367 |         0.794202 |             2959.74 | True      | 0.248636 | False    |
|   4 |     0.588227 |         0.557326 |             4593.7  | False     | 1        | True     |
|   5 |     0.531395 |         0.59864  |             4082.44 | True      | 0.729446 | False    |
|   6 |     0.465537 |         0.776723 |             3842.65 | True      | 0.178145 | False    |
|   7 |     0.470005 |         0.78674  |             3834.84 | True      | 0.17519  | False    |
|   8 |     0.442585 |         0.831128 |             3781.1  | True      | 0        | False    |

- Chosen k=4, silhouette=0.588, Davies-Bouldin=0.557
- Aggregate viewing order: R2 -> R3 -> R1 -> R4

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               2 |            1 |           725 |           39.03 |             265   |                   2.1 |           3089 |                        100 |               3 |     1097   |      784   |
|               3 |            2 |           587 |           24.14 |             202.4 |                  56.2 |            671 |                        100 |               1 |      859.3 |      590.1 |
|               1 |            3 |           525 |           22.11 |             207.3 |                  39.6 |           1300 |                        100 |               2 |      870.7 |      271.5 |
|               4 |            4 |           319 |           14.72 |             227.1 |                   2.1 |           3856 |                        100 |               4 |      809.1 |      907.1 |
