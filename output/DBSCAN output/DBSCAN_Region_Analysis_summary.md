# DBSCAN Region Analysis -- summary

Posters: poster_ArminHofman-1955, poster_BarryCeck-1988, poster_DavidCarson, poster_DavidCarson-1990, poster_EllaRosenblatt-2021, poster_IrisChung-2015, poster_JanTschichold-1927-DieFrauohneNamen, poster_JanTschichold-1938-Der, poster_JoostSchmidt-1923-Saatliches, poster_PaulRand-1947, poster_PaulaScher-1995, poster_ScottBarry-2010, poster_SeanAlatorre, poster_bookcover, poster_nancy
Participants pooled: 48

## poster_ArminHofman-1955

- Dropped 178 stray/isolated fixations before clustering (7.3%)
- Number of regions (k) chosen by best combined separation score (silhouette + Davies-Bouldin) across k=3..5:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac |    score |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|---------:|
|   3 |     0.750202 |         0.323725 |            14288.2  |    35 |            30 |     0.203696 | 1        |
|   5 |     0.696887 |         0.461643 |             7798.34 |    25 |            15 |     0.209855 | 0.846438 |
|   4 |     0.541081 |         0.432456 |             7868.89 |    28 |            15 |     0.117906 | 0.74155  |

- Chosen k=3  ->  DBSCAN eps=35px, min_samples=30, silhouette=0.750, Davies-Bouldin=0.324
- 20.4% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R2 -> R1 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               1 |            1 |          1002 |           49.28 |             240.1 |                  29.2 |           1913 |                        100 |               2 |     1019.8 |      786.2 |
|               0 |            2 |           916 |           34.72 |             185.1 |                  70.8 |            372 |                        100 |               1 |     1132.3 |      209.2 |
|               2 |            3 |           355 |           16    |             220   |                   0   |           5292 |                        100 |               3 |     1220.6 |     1073.6 |

## poster_BarryCeck-1988

- Dropped 140 stray/isolated fixations before clustering (5.2%)
- Number of regions (k) chosen by best combined separation score (silhouette + Davies-Bouldin) across k=3..5:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac |    score |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|---------:|
|   4 |     0.130485 |         0.902917 |             639.853 |    55 |            15 |    0.0354086 | 0.856089 |
|   3 |     0.155311 |         1.04469  |             926.714 |    60 |            18 |    0.0330739 | 0.704803 |

- Chosen k=4  ->  DBSCAN eps=55px, min_samples=15, silhouette=0.130, Davies-Bouldin=0.903
- 3.5% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R2 -> R3 -> R4

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               0 |            1 |          1965 |           75.6  |             172.8 |                  97.9 |            210 |                      100   |               1 |     1055   |      530.6 |
|               1 |            2 |           431 |           16.68 |             173.8 |                   2.1 |           6044 |                      100   |               2 |      348.2 |      906.6 |
|               2 |            3 |           152 |            6.86 |             202.8 |                   0   |           6246 |                       77.1 |               3 |     1419.2 |      572.7 |
|               3 |            4 |            22 |            0.86 |             176.2 |                   0   |           8519 |                       35.4 |               4 |      365.2 |       48.6 |

## poster_DavidCarson

- Dropped 131 stray/isolated fixations before clustering (5.0%)
- Number of regions (k) chosen by best combined separation score (silhouette + Davies-Bouldin) across k=3..5:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac |    score |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|---------:|
|   5 |     0.525151 |         0.515103 |             3134.94 |    50 |            30 |    0.231732  | 1        |
|   3 |     0.504036 |         0.725243 |             3288.76 |    60 |            25 |    0.0294711 | 0.413512 |
|   4 |     0.418913 |         0.632187 |             2423.11 |    55 |            20 |    0.0270488 | 0.24058  |

- Chosen k=5  ->  DBSCAN eps=50px, min_samples=30, silhouette=0.525, Davies-Bouldin=0.515
- 23.2% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R2 -> R3 -> R4 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               1 |            1 |          1066 |           43.82 |             182.3 |                  75   |            370 |                      100   |               1 |      686.1 |      349   |
|               0 |            2 |           623 |           25.25 |             179.8 |                  14.6 |           2597 |                      100   |               2 |      567.9 |      832.8 |
|               3 |            3 |           596 |           23.71 |             176.4 |                   8.3 |           3431 |                      100   |               3 |     1482.5 |      552.6 |
|               2 |            4 |           145 |            5.25 |             160.8 |                   2.1 |           4120 |                       89.6 |               4 |      255.2 |      179   |
|               4 |            5 |            47 |            1.97 |             185.6 |                   0   |           6445 |                       56.2 |               5 |     1086   |      823   |

## poster_DavidCarson-1990

- Dropped 146 stray/isolated fixations before clustering (5.9%)
- Number of regions (k) chosen by best combined separation score (silhouette + Davies-Bouldin) across k=3..5:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac |    score |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|---------:|
|   5 |     0.532227 |         0.582353 |            4238.26  |    60 |            30 |    0.134904  | 1        |
|   3 |     0.200976 |         0.931164 |             615.274 |    60 |            20 |    0.0432548 | 0.551649 |
|   4 |     0.145249 |         0.892993 |             504.917 |    70 |            30 |    0.0501071 | 0.522939 |

- Chosen k=5  ->  DBSCAN eps=60px, min_samples=30, silhouette=0.532, Davies-Bouldin=0.582
- 13.5% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R2 -> R3 -> R1 -> R4 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               0 |            1 |           776 |           33.02 |             200.7 |                  25   |           1899 |                      100   |               3 |      610.4 |      735.6 |
|               2 |            2 |           660 |           28.77 |             205.6 |                  41.7 |           1171 |                      100   |               1 |     1284.4 |      644.7 |
|               1 |            3 |           642 |           26.64 |             195.8 |                  31.2 |           1174 |                      100   |               2 |      522.7 |      291.8 |
|               4 |            4 |           152 |            6.66 |             206.6 |                   2.1 |           4525 |                       81.2 |               4 |     1363.5 |      310   |
|               3 |            5 |           105 |            4.91 |             220.8 |                   0   |           8328 |                       66.7 |               5 |      670.8 |     1047.6 |

## poster_EllaRosenblatt-2021

- Dropped 163 stray/isolated fixations before clustering (6.4%)
- Number of regions (k) chosen by best combined separation score (silhouette + Davies-Bouldin) across k=3..5:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac |   score |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|--------:|
|   5 |     0.500198 |         0.532127 |             3284.35 |    35 |            20 |    0.0898405 |       1 |

- Chosen k=5  ->  DBSCAN eps=35px, min_samples=20, silhouette=0.500, Davies-Bouldin=0.532
- 9.0% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R2 -> R3 -> R5 -> R4

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               0 |            1 |          1287 |           53.98 |             209.3 |                  83.3 |            389 |                      100   |               1 |      866.9 |      685.9 |
|               2 |            2 |           543 |           21.36 |             196.3 |                  14.6 |           3570 |                      100   |               2 |     1115.9 |      205.3 |
|               1 |            3 |           407 |           18.74 |             229.8 |                   0   |           4990 |                       95.8 |               3 |     1046.6 |     1084.2 |
|               3 |            4 |            81 |            3.57 |             219.8 |                   0   |           8577 |                       77.1 |               5 |      656.3 |     1100.5 |
|               4 |            5 |            64 |            2.34 |             182.7 |                   2.1 |           6636 |                       72.9 |               4 |     1066   |      826.3 |

## poster_IrisChung-2015

- Dropped 105 stray/isolated fixations before clustering (4.1%)
- Number of regions (k) chosen by best combined separation score (silhouette + Davies-Bouldin) across k=3..5:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac |    score |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|---------:|
|   3 |     0.398754 |         0.521078 |             987.004 |    55 |            25 |    0.0290151 | 1        |
|   5 |     0.255649 |         0.728412 |             819.793 |    45 |            20 |    0.0698815 | 0.705447 |
|   4 |     0.194601 |         0.767782 |             721.651 |    60 |            30 |    0.0245198 | 0.609861 |

- Chosen k=3  ->  DBSCAN eps=55px, min_samples=25, silhouette=0.399, Davies-Bouldin=0.521
- 2.9% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R2 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               0 |            1 |          1998 |           80.05 |             198.3 |                   100 |            241 |                      100   |               1 |      933.6 |      527.9 |
|               2 |            2 |           272 |           11.48 |             208.8 |                     0 |           6934 |                       95.8 |               2 |      738.7 |     1111.6 |
|               1 |            3 |           177 |            8.47 |             236.8 |                     0 |           8867 |                       95.8 |               3 |     1218.4 |     1094.8 |

## poster_JanTschichold-1927-DieFrauohneNamen

- Dropped 162 stray/isolated fixations before clustering (6.6%)
- Number of regions (k) chosen by best combined separation score (silhouette + Davies-Bouldin) across k=3..5:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac |    score |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|---------:|
|   7 |     0.625883 |         0.444253 |             5933.26 |    35 |            20 |    0.0881076 | 0.979735 |
|   9 |     0.63319  |         0.474648 |             7119.99 |    28 |            15 |    0.143229  | 0.879735 |
|   6 |     0.600696 |         0.531424 |             4398.78 |    30 |            15 |    0.106337  | 0.564984 |
|   8 |     0.510264 |         0.57062  |             3254.44 |    25 |            10 |    0.115451  | 0.159127 |

- Chosen k=7  ->  DBSCAN eps=35px, min_samples=20, silhouette=0.626, Davies-Bouldin=0.444  _(relaxed grid)_
- 8.8% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R5 -> R3 -> R6 -> R4 -> R2 -> R7

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               0 |            1 |           660 |           24.46 |             179.7 |                  37.5 |           1351 |                      100   |               1 |      907.8 |      179.4 |
|               5 |            2 |           424 |           21.64 |             247.5 |                   0   |           6377 |                      100   |               6 |     1149.9 |     1031.5 |
|               3 |            3 |           293 |           14.33 |             237.1 |                  14.6 |           3154 |                      100   |               3 |      872   |      776.2 |
|               1 |            4 |           293 |           12.01 |             198.6 |                   0   |           4882 |                       95.8 |               5 |     1228.3 |      325.6 |
|               2 |            5 |           271 |           11.9  |             212.9 |                  31.2 |           1962 |                       97.9 |               2 |      749.3 |      466.6 |
|               4 |            6 |           237 |            9.94 |             203.4 |                  16.7 |           4161 |                      100   |               4 |     1020.3 |      569.4 |
|               6 |            7 |           126 |            5.71 |             219.8 |                   0   |           9792 |                       72.9 |               7 |      685.6 |     1181.5 |

## poster_JanTschichold-1938-Der

- Dropped 239 stray/isolated fixations before clustering (9.4%)
- Number of regions (k) chosen by best combined separation score (silhouette + Davies-Bouldin) across k=3..5:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac |    score |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|---------:|
|   6 |     0.60753  |         0.530918 |             6018.24 |    45 |            30 |    0.0200087 | 1        |
|   9 |     0.587616 |         0.583662 |             6348.18 |    35 |            25 |    0.0782949 | 0.81586  |
|   8 |     0.560433 |         0.635586 |             5084.69 |    28 |            12 |    0.0630709 | 0.607402 |
|   7 |     0.577295 |         0.66403  |             5870.3  |    30 |            15 |    0.0674206 | 0.607073 |

- Chosen k=6  ->  DBSCAN eps=45px, min_samples=30, silhouette=0.608, Davies-Bouldin=0.531  _(relaxed grid)_
- 2.0% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R2 -> R1 -> R3 -> R5 -> R6 -> R4

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               2 |            1 |           679 |           28.29 |             189.4 |                  14.6 |           1951 |                      100   |               2 |      962.5 |      888.6 |
|               0 |            2 |           427 |           19.22 |             204.5 |                  68.8 |           1063 |                      100   |               1 |     1124.6 |      369.9 |
|               4 |            3 |           401 |           16.2  |             183.6 |                  12.5 |           2850 |                      100   |               3 |      457.3 |      581.5 |
|               5 |            4 |           243 |           13.05 |             244.1 |                   0   |           7185 |                       93.8 |               6 |     1423.6 |     1021.1 |
|               3 |            5 |           284 |           12.26 |             196.2 |                   0   |           5326 |                       97.9 |               4 |     1528.3 |      876.5 |
|               1 |            6 |           265 |           10.98 |             188.3 |                   4.2 |           6006 |                       95.8 |               5 |      664.2 |      103.2 |

## poster_JoostSchmidt-1923-Saatliches

- Dropped 140 stray/isolated fixations before clustering (5.6%)
- Number of regions (k) chosen by best combined separation score (silhouette + Davies-Bouldin) across k=3..5:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac |   score |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|--------:|
|   5 |     0.515011 |         0.458561 |             2277.38 |    30 |            15 |    0.0572161 |       1 |
|   4 |     0.475004 |         0.525862 |             1810.76 |    35 |            18 |    0.0320239 |       0 |

- Chosen k=5  ->  DBSCAN eps=30px, min_samples=15, silhouette=0.515, Davies-Bouldin=0.459
- 5.7% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R2 -> R1 -> R4 -> R3 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               2 |            1 |          1186 |           52.7  |             216.4 |                  41.7 |           1343 |                      100   |               2 |      922.6 |      749.2 |
|               0 |            2 |           728 |           27.91 |             186.7 |                  52.1 |            708 |                      100   |               1 |      788.5 |      304.9 |
|               3 |            3 |           170 |            7.72 |             221.1 |                   0   |           7054 |                       91.7 |               4 |     1253.1 |      630.6 |
|               1 |            4 |           196 |            7.59 |             188.6 |                   6.2 |           4292 |                      100   |               3 |     1082.3 |      448.3 |
|               4 |            5 |            62 |            4.09 |             321.4 |                   0   |           8008 |                       60.4 |               5 |     1327.6 |       92   |

## poster_PaulRand-1947

- Dropped 99 stray/isolated fixations before clustering (3.8%)
- Number of regions (k) chosen by best combined separation score (silhouette + Davies-Bouldin) across k=3..5:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac |     score |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|----------:|
|   5 |     0.475747 |         0.519262 |            1938.99  |    45 |            20 |    0.0977778 | 0.944194  |
|   4 |     0.503198 |         0.580651 |            2069.79  |    55 |            25 |    0.0549495 | 0.794986  |
|   3 |     0.296353 |         0.668981 |             477.408 |    45 |            12 |    0.0238384 | 0.0794996 |

- Chosen k=5  ->  DBSCAN eps=45px, min_samples=20, silhouette=0.476, Davies-Bouldin=0.519
- 9.8% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R2 -> R3 -> R5 -> R4

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               0 |            1 |          1449 |           55.97 |             190.8 |                  97.9 |            209 |                      100   |               1 |      756.8 |      603   |
|               1 |            2 |           625 |           27.33 |             216   |                   2.1 |           3547 |                      100   |               2 |     1002.2 |     1031.1 |
|               3 |            3 |           254 |           10.45 |             203.1 |                   0   |           4961 |                       95.8 |               3 |     1225.8 |      378.6 |
|               2 |            4 |            71 |            3.28 |             227.9 |                   0   |           9678 |                       60.4 |               5 |      630.6 |     1095.1 |
|               4 |            5 |            76 |            2.97 |             193.1 |                   0   |           8378 |                       79.2 |               4 |     1280.6 |      639.7 |

## poster_PaulaScher-1995

- Dropped 77 stray/isolated fixations before clustering (2.8%)
- Number of regions (k) chosen by best combined separation score (silhouette + Davies-Bouldin) across k=3..5:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac |    score |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|---------:|
|   4 |     0.280224 |         0.718152 |             1358.93 |    60 |            30 |    0.0321483 | 0.995868 |
|   3 |     0.275852 |         0.813801 |             1599.32 |    45 |            15 |    0.0257186 | 0.68707  |
|   5 |     0.130606 |         0.802825 |             1033.87 |    45 |            18 |    0.051059  | 0.272741 |

- Chosen k=4  ->  DBSCAN eps=60px, min_samples=30, silhouette=0.280, Davies-Bouldin=0.718
- 3.2% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R4 -> R2 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               0 |            1 |          1790 |           66.86 |             188.3 |                  95.8 |            253 |                      100   |               1 |     1000.8 |      378.6 |
|               2 |            2 |           397 |           15.57 |             197.7 |                   2.1 |           5563 |                       97.9 |               3 |      690.3 |      968.3 |
|               3 |            3 |           379 |           14.82 |             197.2 |                   2.1 |           5945 |                       95.8 |               4 |     1033.3 |     1026.6 |
|               1 |            4 |            78 |            2.75 |             177.4 |                   0   |           5050 |                       79.2 |               2 |      685.5 |      562.1 |

## poster_ScottBarry-2010

- Dropped 174 stray/isolated fixations before clustering (6.6%)
- Number of regions (k) chosen by best combined separation score (silhouette + Davies-Bouldin) across k=3..5:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac |    score |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|---------:|
|   5 |     0.524233 |         0.583897 |              3826.7 |    40 |            15 |    0.0244698 | 0.993207 |

- Chosen k=5  ->  DBSCAN eps=40px, min_samples=15, silhouette=0.524, Davies-Bouldin=0.584
- 2.4% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R3 -> R2 -> R5 -> R4

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               0 |            1 |          1020 |           41.43 |             196.1 |                  60.4 |           1027 |                      100   |               1 |     1040.4 |      655.4 |
|               3 |            2 |           491 |           20.33 |             199.9 |                   8.3 |           2856 |                      100   |               3 |      930.3 |      965.7 |
|               1 |            3 |           421 |           15.23 |             174.7 |                  31.2 |           1460 |                      100   |               2 |      815.3 |      205.6 |
|               4 |            4 |           253 |           11.9  |             227.2 |                   0   |           7641 |                       97.9 |               5 |     1250.2 |     1049.7 |
|               2 |            5 |           267 |           11.1  |             200.8 |                   0   |           4374 |                       95.8 |               4 |     1241.7 |      134.3 |

## poster_SeanAlatorre

- Dropped 96 stray/isolated fixations before clustering (3.9%)
- Number of regions (k) chosen by best combined separation score (silhouette + Davies-Bouldin) across k=3..5:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac |    score |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|---------:|
|   5 |     0.582858 |         0.462472 |            2731.27  |    45 |            25 |    0.113359  | 0.999408 |
|   4 |     0.296765 |         0.618447 |             728.682 |    60 |            25 |    0.0332912 | 0        |

- Chosen k=5  ->  DBSCAN eps=45px, min_samples=25, silhouette=0.583, Davies-Bouldin=0.462
- 11.3% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R2 -> R3 -> R4 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               1 |            1 |          1216 |           52.81 |             216.9 |                  66.7 |           1169 |                      100   |               1 |     1074.9 |      665.8 |
|               0 |            2 |           547 |           21.75 |             198.6 |                  31.2 |           1670 |                      100   |               2 |      869.1 |      228.2 |
|               3 |            3 |           441 |           17.38 |             196.9 |                   2.1 |           2149 |                       95.8 |               3 |     1262.9 |      127.7 |
|               2 |            4 |            96 |            4.87 |             253.6 |                   0   |           7618 |                       83.3 |               4 |      963   |     1000   |
|               4 |            5 |            73 |            3.19 |             218.5 |                   0   |           8176 |                       58.3 |               5 |      672.8 |      964.2 |

## poster_bookcover

- Dropped 103 stray/isolated fixations before clustering (4.0%)
- Number of regions (k) chosen by best combined separation score (silhouette + Davies-Bouldin) across k=3..5:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac |    score |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|---------:|
|   3 |    0.0467825 |          1.30152 |            158.408  |    30 |            10 |    0.0496994 | 0.571417 |
|   5 |   -0.299137  |          1.12211 |             85.3074 |    28 |             8 |    0.0408818 | 0.5      |

- Chosen k=3  ->  DBSCAN eps=30px, min_samples=10, silhouette=0.047, Davies-Bouldin=1.302
- 5.0% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R2 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               0 |            1 |          2136 |           83.68 |             197.3 |                  97.9 |            246 |                      100   |               1 |      989.5 |      545.6 |
|               1 |            2 |           209 |            8.66 |             208.7 |                   2.1 |           4272 |                      100   |               2 |     1178.3 |      650.3 |
|               2 |            3 |           150 |            7.65 |             256.9 |                   0   |           6188 |                       95.8 |               3 |      765.1 |      887   |

## poster_nancy

- Dropped 265 stray/isolated fixations before clustering (10.9%)
- Number of regions (k) chosen by best combined separation score (silhouette + Davies-Bouldin) across k=3..5:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac |    score |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|---------:|
|   4 |     0.695826 |         0.387123 |             7043.02 |    25 |            20 |     0.242115 | 1        |
|   5 |     0.645857 |         0.42796  |             5475.58 |    25 |            18 |     0.207792 | 0.911359 |
|   3 |     0.563202 |         0.520029 |             2768.11 |    40 |            30 |     0.12013  | 0.735915 |

- Chosen k=4  ->  DBSCAN eps=25px, min_samples=20, silhouette=0.696, Davies-Bouldin=0.387
- 24.2% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R3 -> R2 -> R1 -> R4

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |           777 |           40.94 |             259.3 |                   6.2 |           2822 |                        100 |               3 |     1093.1 |      780.4 |
|               0 |            2 |           533 |           22.3  |             205.9 |                  41.7 |           1283 |                        100 |               2 |      867.1 |      272.9 |
|               1 |            3 |           535 |           22.29 |             205.1 |                  50   |            746 |                        100 |               1 |      851.7 |      585.5 |
|               2 |            4 |           311 |           14.48 |             229.1 |                   2.1 |           3856 |                        100 |               4 |      805.4 |      906.3 |
