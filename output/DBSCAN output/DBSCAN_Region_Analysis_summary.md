# DBSCAN Region Analysis -- summary

Posters: poster_EllaRosenblatt-2021, poster_IrisChung-2015, poster_JanTschichold-1927-DieFrauohneNamen, poster_JanTschichold-1938-Der, poster_JoostSchmidt-1923-Saatliches
Participants pooled: 48

## poster_EllaRosenblatt-2021

- Number of regions (k) chosen by best-achievable silhouette across k=3..7:

|   k |   silhouette |   eps |   min_samples |   noise_frac |
|----:|-------------:|------:|--------------:|-------------:|
|   7 |     0.577004 |    30 |            20 |    0.243222  |
|   6 |     0.568576 |    35 |            25 |    0.199214  |
|   4 |     0.509428 |    35 |             8 |    0.0428291 |
|   5 |     0.500059 |    35 |            20 |    0.147348  |
|   3 |     0.335858 |    50 |            15 |    0.0290766 |

- Chosen k=7  ->  DBSCAN eps=30px, min_samples=20, silhouette=0.577
- 24.3% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R2 -> R3 -> R5 -> R4 -> R7 -> R6

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               0 |            1 |           787 |           30.02 |             202.3 |                  77.1 |            400 |                      100   |               1 |      936   |      570.2 |
|               1 |            2 |           575 |           23.79 |             219.5 |                   4.2 |           2311 |                      100   |               2 |      794.1 |      827   |
|               2 |            3 |           573 |           20.96 |             194   |                  16.7 |           3413 |                      100   |               3 |     1114.7 |      205.1 |
|               3 |            4 |           324 |           13.82 |             226.3 |                   0   |           5948 |                       95.8 |               5 |     1102   |     1082.2 |
|               4 |            5 |           152 |            6.42 |             224.1 |                   0   |           4958 |                       93.8 |               4 |      943.4 |     1039.3 |
|               6 |            6 |            95 |            3.78 |             211.2 |                   0   |           8291 |                       81.2 |               7 |      661.5 |     1100.8 |
|               5 |            7 |            39 |            1.22 |             165.4 |                   2.1 |           6524 |                       47.9 |               6 |      739   |      649.6 |

## poster_IrisChung-2015

- Number of regions (k) chosen by best-achievable silhouette across k=3..7:

|   k |   silhouette |   eps |   min_samples |   noise_frac |
|----:|-------------:|------:|--------------:|-------------:|
|   6 |     0.442739 |    40 |            18 |    0.134796  |
|   7 |     0.400131 |    35 |            12 |    0.11011   |
|   3 |     0.396476 |    55 |            25 |    0.0615204 |
|   5 |     0.255383 |    45 |            20 |    0.107367  |
|   4 |     0.193645 |    60 |            30 |    0.0532915 |

- Chosen k=6  ->  DBSCAN eps=40px, min_samples=18, silhouette=0.443
- 13.5% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R2 -> R3 -> R6 -> R4 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               0 |            1 |          1230 |           43.07 |             179.4 |                  83.3 |            340 |                      100   |               1 |      965.6 |      317.3 |
|               1 |            2 |           422 |           18.05 |             219.1 |                  10.4 |           4701 |                      100   |               2 |      979.1 |      854.7 |
|               2 |            3 |           292 |           13.67 |             239.9 |                   2.1 |           5467 |                       97.9 |               3 |      695.7 |      730.4 |
|               5 |            4 |           284 |           11.43 |             206.1 |                   0   |           6925 |                       95.8 |               5 |      740.9 |     1109.9 |
|               4 |            5 |           200 |            8.87 |             227.3 |                   0   |           8460 |                       97.9 |               6 |     1221.7 |     1086.2 |
|               3 |            6 |           124 |            4.9  |             202.6 |                   4.2 |           6332 |                       83.3 |               4 |     1231.6 |      641.4 |

## poster_JanTschichold-1927-DieFrauohneNamen

- Number of regions (k) chosen by best-achievable silhouette across k=3..7:

|   k |   silhouette |   eps |   min_samples |   noise_frac |
|----:|-------------:|------:|--------------:|-------------:|
|   7 |     0.625659 |    35 |            20 |    0.147607  |
|   6 |     0.600696 |    30 |            15 |    0.165045  |
|   3 |     0.508394 |    50 |            15 |    0.0300081 |
|   4 |     0.459649 |    50 |            20 |    0.0486618 |
|   5 |     0.459641 |    40 |            15 |    0.0713706 |

- Chosen k=7  ->  DBSCAN eps=35px, min_samples=20, silhouette=0.626
- 14.8% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R1 -> R4 -> R3 -> R6 -> R5 -> R2 -> R7

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               0 |            1 |           696 |           24.16 |             179.2 |                  35.4 |           1331 |                      100   |               1 |      906.8 |      179.4 |
|               5 |            2 |           457 |           21.87 |             247.1 |                   0   |           6361 |                      100   |               6 |     1146.6 |     1028.6 |
|               3 |            3 |           329 |           15.13 |             237.5 |                  14.6 |           3107 |                      100   |               3 |      868.5 |      785.2 |
|               2 |            4 |           287 |           11.63 |             209.2 |                  31.2 |           1928 |                      100   |               2 |      750.3 |      468.6 |
|               1 |            5 |           306 |           11.59 |             195.6 |                   2.1 |           4756 |                       95.8 |               5 |     1227.4 |      324.5 |
|               4 |            6 |           251 |            9.79 |             201.4 |                  16.7 |           4099 |                      100   |               4 |     1020   |      565.2 |
|               6 |            7 |           140 |            5.84 |             215.3 |                   0   |           9476 |                       79.2 |               7 |      689.6 |     1174.3 |

## poster_JanTschichold-1938-Der

- Number of regions (k) chosen by best-achievable silhouette across k=3..7:

|   k |   silhouette |   eps |   min_samples |   noise_frac |
|----:|-------------:|------:|--------------:|-------------:|
|   5 |     0.661037 |    45 |            25 |    0.0902285 |
|   6 |     0.606265 |    45 |            30 |    0.102443  |
|   7 |     0.577097 |    30 |            15 |    0.154846  |
|   4 |     0.542477 |    35 |            10 |    0.0839243 |

- Chosen k=5  ->  DBSCAN eps=45px, min_samples=25, silhouette=0.661
- 9.0% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R3 -> R1 -> R4 -> R2 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               2 |            1 |           746 |           28.17 |             185.9 |                  16.7 |           1618 |                      100   |               2 |      959.4 |      887.2 |
|               3 |            2 |           563 |           24.46 |             213.9 |                   0   |           5172 |                      100   |               4 |     1478.1 |      949.4 |
|               0 |            3 |           511 |           20.82 |             200.6 |                  62.5 |            724 |                      100   |               1 |     1137.9 |      384.8 |
|               4 |            4 |           424 |           15.53 |             180.3 |                  12.5 |           2609 |                      100   |               3 |      462.6 |      578.7 |
|               1 |            5 |           294 |           11.02 |             184.5 |                   8.3 |           5567 |                       97.9 |               5 |      668.8 |      106.8 |

## poster_JoostSchmidt-1923-Saatliches

- Number of regions (k) chosen by best-achievable silhouette across k=3..7:

|   k |   silhouette |   eps |   min_samples |   noise_frac |
|----:|-------------:|------:|--------------:|-------------:|
|   5 |     0.514934 |    30 |            15 |    0.109589  |
|   6 |     0.476997 |    35 |            25 |    0.13336   |
|   4 |     0.474252 |    35 |            18 |    0.0817889 |
|   7 |     0.403234 |    35 |            30 |    0.180097  |
|   3 |     0.235095 |    30 |            10 |    0.060838  |

- Chosen k=5  ->  DBSCAN eps=30px, min_samples=15, silhouette=0.515
- 11.0% of fixations were noise (folded into nearest region)
- Aggregate viewing order: R2 -> R1 -> R4 -> R3 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               2 |            1 |          1255 |           52.73 |             214.7 |                  41.7 |           1195 |                      100   |               2 |      922.9 |      755.5 |
|               0 |            2 |           759 |           27.6  |             185.7 |                  50   |            678 |                      100   |               1 |      787.9 |      304.3 |
|               3 |            3 |           183 |            7.73 |             215.7 |                   2.1 |           6749 |                       93.8 |               4 |     1253.6 |      628.1 |
|               1 |            4 |           207 |            7.59 |             187.4 |                   6.2 |           4283 |                      100   |               3 |     1085.7 |      445.2 |
|               4 |            5 |            78 |            4.36 |             285.3 |                   0   |           8511 |                       72.9 |               5 |     1324.6 |       94.6 |
