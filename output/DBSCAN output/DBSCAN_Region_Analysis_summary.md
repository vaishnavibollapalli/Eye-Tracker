# DBSCAN Region Analysis -- summary

Posters: poster_ArminHofman-1955, poster_BarryCeck-1988, poster_DavidCarson, poster_DavidCarson-1990, poster_EllaRosenblatt-2021, poster_IrisChung-2015, poster_JanTschichold-1927-DieFrauohneNamen, poster_JanTschichold-1938-Der, poster_JoostSchmidt-1923-Saatliches, poster_PaulRand-1947, poster_PaulaScher-1995, poster_ScottBarry-2010, poster_SeanAlatorre, poster_bookcover, poster_nancy
Participants pooled: 48

## poster_ArminHofman-1955

- Dropped 178 stray/isolated fixations before clustering (7.3%)
- Number of regions (k) across k=3..8, decided by: Davies-Bouldin primary, silhouette secondary check, crossing regions disqualified, most clusters wins among what survives:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac | crosses   | chosen   |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|:----------|:---------|
|   3 |     0.750202 |         0.323725 |            14288.2  |    35 |            30 |    0.203696  | False     | True     |
|   4 |     0.541081 |         0.432456 |             7868.89 |    28 |            15 |    0.117906  | True      | False    |
|   5 |     0.696887 |         0.461643 |             7798.34 |    25 |            15 |    0.209855  | False     | False    |
|   6 |     0.537602 |         0.54056  |             6241.47 |    30 |            20 |    0.173339  | False     | False    |
|   7 |     0.442093 |         0.466466 |             3761.19 |    22 |             8 |    0.0923889 | True      | False    |
|   8 |     0.497972 |         0.613591 |             4494.89 |    22 |            10 |    0.137264  | False     | False    |

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
- Number of regions (k) across k=3..8, decided by: Davies-Bouldin primary, silhouette secondary check, crossing regions disqualified, most clusters wins among what survives:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac | crosses   | chosen   |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|:----------|:---------|
|   3 |     0.155311 |         1.04469  |             926.714 |    60 |            18 |    0.0330739 | True      | False    |
|   4 |     0.130485 |         0.902917 |             639.853 |    55 |            15 |    0.0354086 | True      | False    |
|   6 |     0.135223 |         1.00275  |             594.148 |    50 |            15 |    0.0587549 | True      | False    |
|   7 |     0.392531 |         0.865235 |            2292.57  |    55 |            20 |    0.0797665 | True      | True     |

- Chosen k=7  ->  DBSCAN eps=55px, min_samples=20, silhouette=0.393, Davies-Bouldin=0.865  _(all candidates crossed -- used anyway)_
- 8.0% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R3 -> R2 -> R1 -> R5 -> R6 -> R7 -> R4

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               2 |            1 |           884 |           35.68 |             181.3 |                  37.5 |           2140 |                      100   |               3 |      995.4 |      838   |
|               0 |            2 |           443 |           16.45 |             166.7 |                  43.8 |           1138 |                      100   |               2 |      974.1 |      401.1 |
|               1 |            3 |           372 |           14.39 |             173.7 |                  16.7 |           1032 |                       97.9 |               1 |      899.5 |      126.2 |
|               5 |            4 |           343 |           13.62 |             178.3 |                   0   |           7196 |                       95.8 |               7 |      357.1 |      943.2 |
|               3 |            5 |           291 |           10.09 |             155.8 |                   0   |           4169 |                       93.8 |               4 |     1560.2 |      190.4 |
|               6 |            6 |           151 |            6.78 |             201.6 |                   0   |           6143 |                       75   |               5 |     1418.3 |      574.3 |
|               4 |            7 |            86 |            2.99 |             156.3 |                   2.1 |           6719 |                       87.5 |               6 |      303.6 |      743.9 |

## poster_DavidCarson

- Dropped 131 stray/isolated fixations before clustering (5.0%)
- Number of regions (k) across k=3..8, decided by: Davies-Bouldin primary, silhouette secondary check, crossing regions disqualified, most clusters wins among what survives:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac | crosses   | chosen   |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|:----------|:---------|
|   3 |     0.504036 |         0.725243 |             3288.76 |    60 |            25 |    0.0294711 | False     | False    |
|   4 |     0.418913 |         0.632187 |             2423.11 |    55 |            20 |    0.0270488 | False     | False    |
|   5 |     0.525151 |         0.515103 |             3134.94 |    50 |            30 |    0.231732  | False     | False    |
|   6 |     0.451407 |         0.560619 |             2451.53 |    55 |            30 |    0.147356  | False     | False    |
|   7 |     0.449006 |         0.52182  |             2554.61 |    45 |            25 |    0.242632  | False     | True     |
|   8 |     0.348286 |         0.60326  |             1993.84 |    55 |            25 |    0.0726686 | False     | False    |

- Chosen k=7  ->  DBSCAN eps=45px, min_samples=25, silhouette=0.449, Davies-Bouldin=0.522
- 24.3% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R2 -> R3 -> R4 -> R7 -> R5 -> R6

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               1 |            1 |           915 |           38.11 |             184.7 |                  68.8 |            389 |                      100   |               1 |      637.4 |      363.7 |
|               0 |            2 |           624 |           25.31 |             179.9 |                  14.6 |           2565 |                      100   |               2 |      567   |      832.1 |
|               3 |            3 |           552 |           22.12 |             177.8 |                   8.3 |           3707 |                      100   |               3 |     1494   |      574.6 |
|               2 |            4 |           142 |            5.18 |             161.8 |                   2.1 |           3855 |                       87.5 |               4 |      252.4 |      179.1 |
|               4 |            5 |           128 |            4.96 |             171.9 |                   6.2 |           7512 |                       83.3 |               6 |      985.7 |      241.9 |
|               5 |            6 |            67 |            2.29 |             151.9 |                   0   |           9467 |                       58.3 |               7 |     1286.1 |      244   |
|               6 |            7 |            49 |            2.02 |             182.7 |                   0   |           6341 |                       58.3 |               5 |     1084   |      822.5 |

## poster_DavidCarson-1990

- Dropped 146 stray/isolated fixations before clustering (5.9%)
- Number of regions (k) across k=3..8, decided by: Davies-Bouldin primary, silhouette secondary check, crossing regions disqualified, most clusters wins among what survives:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac | crosses   | chosen   |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|:----------|:---------|
|   3 |     0.200976 |         0.931164 |             615.274 |    60 |            20 |    0.0432548 | False     | False    |
|   4 |     0.145249 |         0.892993 |             504.917 |    70 |            30 |    0.0501071 | True      | False    |
|   5 |     0.532227 |         0.582353 |            4238.26  |    60 |            30 |    0.134904  | False     | False    |
|   6 |     0.560711 |         0.504153 |            3715.69  |    40 |            15 |    0.182869  | False     | False    |
|   7 |     0.529409 |         0.48763  |            3428.79  |    45 |            20 |    0.182441  | False     | True     |
|   8 |    -0.155814 |         1.21404  |             240.409 |    40 |            10 |    0.0753747 | True      | False    |

- Chosen k=7  ->  DBSCAN eps=45px, min_samples=20, silhouette=0.529, Davies-Bouldin=0.488
- 18.2% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R2 -> R3 -> R1 -> R4 -> R6 -> R7 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               0 |            1 |           782 |           33.23 |             200.5 |                  29.2 |           1770 |                      100   |               3 |      612.2 |      733.8 |
|               1 |            2 |           638 |           26.53 |             196.1 |                  29.2 |           1178 |                      100   |               1 |      521.1 |      291.2 |
|               2 |            3 |           551 |           23.87 |             204.3 |                  18.8 |           1549 |                      100   |               2 |     1326.9 |      621.4 |
|               4 |            4 |           146 |            6.49 |             209.8 |                   2.1 |           4578 |                       81.2 |               4 |     1362.6 |      306.5 |
|               3 |            5 |           104 |            4.89 |             221.9 |                   0   |           8690 |                       66.7 |               7 |      670.7 |     1048.1 |
|               5 |            6 |            76 |            3.29 |             204.4 |                  18.8 |           5598 |                       79.2 |               5 |     1012.9 |      633.5 |
|               6 |            7 |            38 |            1.69 |             210.3 |                   2.1 |           8231 |                       37.5 |               6 |     1238   |      988.5 |

## poster_EllaRosenblatt-2021

- Dropped 163 stray/isolated fixations before clustering (6.4%)
- Number of regions (k) across k=3..8, decided by: Davies-Bouldin primary, silhouette secondary check, crossing regions disqualified, most clusters wins among what survives:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac | crosses   | chosen   |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|:----------|:---------|
|   5 |     0.500198 |         0.532127 |             3284.35 |    35 |            20 |    0.0898405 | True      | False    |
|   6 |     0.697077 |         0.397377 |            10688.2  |    35 |            30 |    0.212427  | False     | True     |
|   7 |     0.577004 |         0.440815 |             8521.1  |    30 |            20 |    0.191436  | True      | False    |
|   8 |     0.561886 |         0.435429 |             6657.12 |    30 |            18 |    0.149874  | False     | False    |

- Chosen k=6  ->  DBSCAN eps=35px, min_samples=30, silhouette=0.697, Davies-Bouldin=0.397
- 21.2% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R2 -> R3 -> R5 -> R4 -> R6

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               0 |            1 |           750 |           30.23 |             201.1 |                  77.1 |            415 |                      100   |               1 |      937.9 |      581.6 |
|               1 |            2 |           563 |           24.72 |             219.1 |                   8.3 |           2411 |                      100   |               2 |      788.2 |      816.8 |
|               2 |            3 |           543 |           21.36 |             196.3 |                  14.6 |           3570 |                      100   |               3 |     1115.9 |      205.3 |
|               3 |            4 |           295 |           13.42 |             227.1 |                   0   |           6461 |                       93.8 |               5 |     1094.1 |     1092.5 |
|               4 |            5 |           150 |            6.69 |             222.5 |                   0   |           4963 |                       93.8 |               4 |      954.3 |     1023.1 |
|               5 |            6 |            81 |            3.57 |             219.8 |                   0   |           8577 |                       77.1 |               6 |      656.3 |     1100.5 |

## poster_IrisChung-2015

- Dropped 105 stray/isolated fixations before clustering (4.1%)
- Number of regions (k) across k=3..8, decided by: Davies-Bouldin primary, silhouette secondary check, crossing regions disqualified, most clusters wins among what survives:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac | crosses   | chosen   |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|:----------|:---------|
|   3 |     0.398754 |         0.521078 |             987.004 |    55 |            25 |    0.0290151 | False     | False    |
|   4 |     0.194601 |         0.767782 |             721.651 |    60 |            30 |    0.0245198 | True      | False    |
|   5 |     0.255649 |         0.728412 |             819.793 |    45 |            20 |    0.0698815 | True      | False    |
|   6 |     0.442639 |         0.547264 |            1937.11  |    40 |            18 |    0.0980793 | False     | False    |
|   7 |     0.400131 |         0.561146 |            1667.12  |    35 |            12 |    0.0719248 | False     | True     |
|   8 |     0.367147 |         0.58094  |            1846.22  |    45 |            25 |    0.112791  | True      | False    |

- Chosen k=7  ->  DBSCAN eps=35px, min_samples=12, silhouette=0.400, Davies-Bouldin=0.561
- 7.2% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R2 -> R3 -> R4 -> R6 -> R5 -> R7

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               0 |            1 |          1205 |           43.83 |             180   |                  89.6 |            346 |                      100   |               1 |      962.7 |      320.4 |
|               1 |            2 |           389 |           17.27 |             219.8 |                   6.2 |           4793 |                      100   |               2 |      979.9 |      834.1 |
|               2 |            3 |           286 |           13.95 |             241.4 |                   2.1 |           5475 |                       97.9 |               3 |      694.7 |      730   |
|               5 |            4 |           272 |           11.48 |             208.8 |                   0   |           6934 |                       95.8 |               4 |      738.7 |     1111.6 |
|               4 |            5 |           160 |            7.66 |             237   |                   0   |           8925 |                       95.8 |               6 |     1231.5 |     1091.5 |
|               3 |            6 |            96 |            4.05 |             208.9 |                   0   |           7132 |                       79.2 |               5 |     1228.9 |      631.1 |
|               6 |            7 |            39 |            1.76 |             223.9 |                   2.1 |          10185 |                       45.8 |               7 |     1041.5 |     1121.6 |

## poster_JanTschichold-1927-DieFrauohneNamen

- Dropped 162 stray/isolated fixations before clustering (6.6%)
- Number of regions (k) across k=3..8, decided by: Davies-Bouldin primary, silhouette secondary check, crossing regions disqualified, most clusters wins among what survives:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac | crosses   | chosen   |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|:----------|:---------|
|   6 |     0.600696 |         0.531424 |             4398.78 |    30 |            15 |    0.106337  | False     | False    |
|   7 |     0.625883 |         0.444253 |             5933.26 |    35 |            20 |    0.0881076 | False     | True     |
|   8 |     0.510264 |         0.57062  |             3254.44 |    25 |            10 |    0.115451  | True      | False    |

- Chosen k=7  ->  DBSCAN eps=35px, min_samples=20, silhouette=0.626, Davies-Bouldin=0.444
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
- Number of regions (k) across k=3..8, decided by: Davies-Bouldin primary, silhouette secondary check, crossing regions disqualified, most clusters wins among what survives:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac | crosses   | chosen   |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|:----------|:---------|
|   6 |     0.60753  |         0.530918 |             6018.24 |    45 |            30 |    0.0200087 | False     | True     |
|   7 |     0.577295 |         0.66403  |             5870.3  |    30 |            15 |    0.0674206 | False     | False    |
|   8 |     0.560433 |         0.635586 |             5084.69 |    28 |            12 |    0.0630709 | False     | False    |

- Chosen k=6  ->  DBSCAN eps=45px, min_samples=30, silhouette=0.608, Davies-Bouldin=0.531
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
- Number of regions (k) across k=3..8, decided by: Davies-Bouldin primary, silhouette secondary check, crossing regions disqualified, most clusters wins among what survives:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac | crosses   | chosen   |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|:----------|:---------|
|   4 |     0.475004 |         0.525862 |             1810.76 |    35 |            18 |    0.0320239 | False     | False    |
|   5 |     0.515011 |         0.458561 |             2277.38 |    30 |            15 |    0.0572161 | False     | False    |
|   6 |     0.47681  |         0.482874 |             2519.92 |    35 |            25 |    0.0828352 | False     | True     |
|   7 |     0.325863 |         0.50726  |             1504.57 |    22 |             8 |    0.060205  | False     | False    |
|   8 |     0.304089 |         0.588751 |             1932.58 |    25 |            12 |    0.087959  | True      | False    |

- Chosen k=6  ->  DBSCAN eps=35px, min_samples=25, silhouette=0.477, Davies-Bouldin=0.483
- 8.3% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R2 -> R1 -> R3 -> R5 -> R4 -> R6

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               1 |            1 |          1031 |           45.8  |             216.4 |                  41.7 |           1348 |                      100   |               2 |      950.3 |      732.5 |
|               0 |            2 |           724 |           27.76 |             186.8 |                  52.1 |            708 |                      100   |               1 |      787.6 |      304.2 |
|               5 |            3 |           203 |            7.86 |             188.5 |                   6.2 |           4132 |                      100   |               3 |     1079.6 |      449.4 |
|               3 |            4 |           170 |            7.72 |             221.1 |                   0   |           7054 |                       91.7 |               5 |     1253.1 |      630.6 |
|               2 |            5 |           152 |            6.78 |             217.3 |                   0   |           6133 |                       89.6 |               4 |      733   |      865.6 |
|               4 |            6 |            62 |            4.09 |             321.4 |                   0   |           8008 |                       60.4 |               6 |     1327.6 |       92   |

## poster_PaulRand-1947

- Dropped 99 stray/isolated fixations before clustering (3.8%)
- Number of regions (k) across k=3..8, decided by: Davies-Bouldin primary, silhouette secondary check, crossing regions disqualified, most clusters wins among what survives:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac | crosses   | chosen   |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|:----------|:---------|
|   3 |     0.296353 |         0.668981 |             477.408 |    45 |            12 |    0.0238384 | False     | False    |
|   4 |     0.503198 |         0.580651 |            2069.79  |    55 |            25 |    0.0549495 | False     | False    |
|   5 |     0.475747 |         0.519262 |            1938.99  |    45 |            20 |    0.0977778 | False     | False    |
|   6 |     0.583523 |         0.408153 |            2344.64  |    40 |            25 |    0.197172  | False     | False    |
|   7 |     0.599817 |         0.389224 |            2128.28  |    30 |            15 |    0.222222  | False     | True     |
|   8 |     0.575603 |         0.45737  |            3643.88  |    40 |            30 |    0.235152  | False     | False    |

- Chosen k=7  ->  DBSCAN eps=30px, min_samples=15, silhouette=0.600, Davies-Bouldin=0.389
- 22.2% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R3 -> R4 -> R2 -> R6 -> R7 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               0 |            1 |          1441 |           55.64 |             190.7 |                  97.9 |            209 |                      100   |               1 |      755.1 |      602.6 |
|               1 |            2 |           389 |           16.08 |             204.1 |                   0   |           5081 |                      100   |               4 |      893.4 |     1079.1 |
|               2 |            3 |           241 |           11.49 |             235.4 |                   2.1 |           4209 |                       97.9 |               2 |     1153.6 |      960.2 |
|               4 |            4 |           197 |            8.19 |             205.2 |                   0   |           5076 |                       93.8 |               3 |     1194.7 |      424   |
|               3 |            5 |            70 |            3.24 |             228.7 |                   0   |           9678 |                       60.4 |               7 |      629.7 |     1096.8 |
|               5 |            6 |            75 |            2.93 |             192.7 |                   0   |           8384 |                       79.2 |               5 |     1282.6 |      640   |
|               6 |            7 |            62 |            2.45 |             194.9 |                   0   |           8660 |                       62.5 |               6 |     1319.9 |      234.5 |

## poster_PaulaScher-1995

- Dropped 77 stray/isolated fixations before clustering (2.8%)
- Number of regions (k) across k=3..8, decided by: Davies-Bouldin primary, silhouette secondary check, crossing regions disqualified, most clusters wins among what survives:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac | crosses   | chosen   |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|:----------|:---------|
|   3 |    0.275852  |         0.813801 |            1599.32  |    45 |            15 |    0.0257186 | False     | False    |
|   4 |    0.280224  |         0.718152 |            1358.93  |    60 |            30 |    0.0321483 | False     | True     |
|   5 |    0.130606  |         0.802825 |            1033.87  |    45 |            18 |    0.051059  | True      | False    |
|   6 |    0.261357  |         0.560131 |            1361.45  |    50 |            30 |    0.192511  | True      | False    |
|   7 |    0.0596065 |         0.751457 |             709.148 |    50 |            25 |    0.091528  | True      | False    |
|   8 |    0.123379  |         0.732965 |             982.654 |    40 |            20 |    0.212179  | True      | False    |

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
- Number of regions (k) across k=3..8, decided by: Davies-Bouldin primary, silhouette secondary check, crossing regions disqualified, most clusters wins among what survives:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac | crosses   | chosen   |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|:----------|:---------|
|   5 |     0.524233 |         0.583897 |             3826.7  |    40 |            15 |    0.0244698 | False     | False    |
|   6 |     0.457408 |         0.588992 |             3144.6  |    45 |            20 |    0.0269168 | False     | True     |
|   7 |     0.433535 |         0.64237  |             2925.17 |    35 |            15 |    0.0636215 | False     | False    |
|   8 |     0.655988 |         0.470043 |             8069.82 |    35 |            30 |    0.221044  | True      | False    |

- Chosen k=6  ->  DBSCAN eps=45px, min_samples=20, silhouette=0.457, Davies-Bouldin=0.589
- 2.7% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R3 -> R2 -> R4 -> R5 -> R6

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               0 |            1 |          1026 |           41.65 |             196   |                  62.5 |            968 |                      100   |               1 |     1039.9 |      655   |
|               3 |            2 |           489 |           20.28 |             200.3 |                   8.3 |           2898 |                      100   |               3 |      930.2 |      966.1 |
|               1 |            3 |           418 |           15.11 |             174.5 |                  29.2 |           1474 |                      100   |               2 |      815.2 |      203.9 |
|               2 |            4 |           267 |           11.1  |             200.8 |                   0   |           4374 |                       95.8 |               4 |     1241.7 |      134.3 |
|               4 |            5 |           209 |            9.78 |             225.8 |                   0   |           7693 |                       97.9 |               5 |     1276.4 |     1066.1 |
|               5 |            6 |            43 |            2.09 |             234.5 |                   0   |           8818 |                       35.4 |               6 |     1127.9 |      974.9 |

## poster_SeanAlatorre

- Dropped 96 stray/isolated fixations before clustering (3.9%)
- Number of regions (k) across k=3..8, decided by: Davies-Bouldin primary, silhouette secondary check, crossing regions disqualified, most clusters wins among what survives:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac | crosses   | chosen   |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|:----------|:---------|
|   4 |     0.296765 |         0.618447 |             728.682 |    60 |            25 |    0.0332912 | False     | False    |
|   5 |     0.582858 |         0.462472 |            2731.27  |    45 |            25 |    0.113359  | True      | False    |
|   6 |     0.495711 |         0.504288 |            2021.46  |    50 |            18 |    0.0387695 | False     | False    |
|   7 |     0.606998 |         0.484091 |            4093.96  |    35 |            15 |    0.140329  | False     | False    |
|   8 |     0.599953 |         0.474892 |            3905.17  |    30 |            15 |    0.194269  | False     | True     |

- Chosen k=8  ->  DBSCAN eps=30px, min_samples=15, silhouette=0.600, Davies-Bouldin=0.475
- 19.4% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R2 -> R3 -> R4 -> R8 -> R5 -> R6 -> R7

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               1 |            1 |           790 |           33.41 |             211.3 |                  62.5 |           1258 |                      100   |               1 |      986.2 |      605.6 |
|               0 |            2 |           547 |           21.71 |             198.3 |                  31.2 |           1670 |                      100   |               2 |      868.7 |      228   |
|               3 |            3 |           441 |           17.38 |             196.9 |                   2.1 |           2149 |                       95.8 |               3 |     1262.9 |      127.7 |
|               4 |            4 |           290 |           13.74 |             236.7 |                   2.1 |           5623 |                       97.9 |               4 |     1248.6 |      714.6 |
|               2 |            5 |           101 |            5.01 |             247.6 |                   0   |           7598 |                       83.3 |               6 |      962.3 |      998.3 |
|               7 |            6 |            77 |            3.37 |             219   |                   0   |           8184 |                       62.5 |               7 |     1226.9 |      956.2 |
|               5 |            7 |            71 |            3.14 |             220.8 |                   0   |           8324 |                       56.2 |               8 |      670.3 |      964.7 |
|               6 |            8 |            56 |            2.24 |             199.7 |                   2.1 |           7026 |                       60.4 |               5 |     1105.1 |      812.7 |

## poster_bookcover

- Dropped 103 stray/isolated fixations before clustering (4.0%)
- Number of regions (k) across k=3..8, decided by: Davies-Bouldin primary, silhouette secondary check, crossing regions disqualified, most clusters wins among what survives:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac | crosses   | chosen   |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|:----------|:---------|
|   3 |    0.0467825 |         1.30152  |            158.408  |    30 |            10 |    0.0496994 | True      | False    |
|   5 |   -0.299137  |         1.12211  |             85.3074 |    28 |             8 |    0.0408818 | True      | False    |
|   6 |    0.520415  |         0.570709 |           4100.18   |    45 |            30 |    0.0681363 | False     | False    |
|   7 |    0.64402   |         0.418577 |           6700.43   |    28 |            20 |    0.247295  | False     | False    |
|   8 |    0.582064  |         0.444527 |           5552.76   |    28 |            15 |    0.171142  | False     | True     |

- Chosen k=8  ->  DBSCAN eps=28px, min_samples=15, silhouette=0.582, Davies-Bouldin=0.445
- 17.1% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R2 -> R5 -> R6 -> R4 -> R3 -> R8 -> R7

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               0 |            1 |           634 |           21.37 |             169.7 |                  77.1 |            649 |                      100   |               1 |      878.1 |      512.1 |
|               3 |            2 |           533 |           19.77 |             186.8 |                  10.4 |           2785 |                      100   |               2 |     1090.3 |      179.8 |
|               5 |            3 |           434 |           19    |             220.5 |                   0   |           4755 |                      100   |               6 |     1078.2 |      992.7 |
|               7 |            4 |           273 |           12.25 |             225.9 |                   4.2 |           4528 |                       97.9 |               5 |      976.6 |      773   |
|               6 |            5 |           211 |            9.72 |             231.9 |                   6.2 |           3102 |                       97.9 |               3 |      851.3 |      219   |
|               2 |            6 |           217 |            8.86 |             205.7 |                   2.1 |           4272 |                      100   |               4 |     1175.5 |      649.3 |
|               4 |            7 |           151 |            7.67 |             255.9 |                   0   |           6188 |                       95.8 |               8 |      764.6 |      886.1 |
|               1 |            8 |            42 |            1.36 |             162.5 |                   0   |           4830 |                       47.9 |               7 |     1136.4 |      418.1 |

## poster_nancy

- Dropped 265 stray/isolated fixations before clustering (10.9%)
- Number of regions (k) across k=3..8, decided by: Davies-Bouldin primary, silhouette secondary check, crossing regions disqualified, most clusters wins among what survives:

|   k |   silhouette |   davies_bouldin |   calinski_harabasz |   eps |   min_samples |   noise_frac | crosses   | chosen   |
|----:|-------------:|-----------------:|--------------------:|------:|--------------:|-------------:|:----------|:---------|
|   3 |     0.563202 |         0.520029 |             2768.11 |    40 |            30 |     0.12013  | False     | False    |
|   4 |     0.695826 |         0.387123 |             7043.02 |    25 |            20 |     0.242115 | False     | False    |
|   5 |     0.645857 |         0.42796  |             5475.58 |    25 |            18 |     0.207792 | False     | True     |
|   6 |     0.540812 |         0.489852 |             4463.87 |    22 |            15 |     0.234694 | True      | False    |
|   7 |     0.493371 |         0.494154 |             3741.72 |    20 |            12 |     0.238868 | True      | False    |
|   8 |     0.380708 |         0.54079  |             3153.47 |    22 |            12 |     0.180427 | True      | False    |

- Chosen k=5  ->  DBSCAN eps=25px, min_samples=18, silhouette=0.646, Davies-Bouldin=0.428
- 20.8% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R2 -> R3 -> R1 -> R4 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |           774 |           40.86 |             259.8 |                   6.2 |           2826 |                      100   |               3 |     1093.3 |      780.2 |
|               1 |            2 |           536 |           22.32 |             205   |                  52.1 |            677 |                      100   |               1 |      851.7 |      585.3 |
|               0 |            3 |           532 |           22.27 |             206   |                  39.6 |           1297 |                      100   |               2 |      867.1 |      272.7 |
|               2 |            4 |           271 |           12.36 |             224.5 |                   2.1 |           4079 |                      100   |               4 |      786.6 |      896.3 |
|               4 |            5 |            43 |            2.19 |             250.6 |                   0   |           7569 |                       52.1 |               5 |      917.3 |      963.3 |
