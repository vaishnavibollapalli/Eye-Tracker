# Divisive (Bisecting K-Means) Region Analysis -- summary

Posters: poster_ArminHofman-1955, poster_BarryCeck-1988, poster_DavidCarson, poster_DavidCarson-1990, poster_EllaRosenblatt-2021, poster_IrisChung-2015, poster_JanTschichold-1927-DieFrauohneNamen, poster_JanTschichold-1938-Der, poster_JoostSchmidt-1923-Saatliches, poster_PaulRand-1947, poster_PaulaScher-1995, poster_ScottBarry-2010, poster_SeanAlatorre, poster_bookcover, poster_nancy
Participants pooled: 48

## poster_ArminHofman-1955

- Dropped 178 stray/isolated fixations before clustering (7.3%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |     score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|----------:|:---------|
|   3 |     0.63671  |         0.441292 |             7416.18 | False     | 1         | True     |
|   4 |     0.567747 |         0.627885 |             8472.91 | False     | 0.658363  | False    |
|   5 |     0.469316 |         0.761168 |             7858.67 | False     | 0.303132  | False    |
|   6 |     0.425738 |         0.877035 |             7141.85 | False     | 0.0892823 | False    |
|   7 |     0.415619 |         0.943759 |             6806.94 | False     | 0         | False    |
|   8 |     0.422796 |         0.830384 |             6728.38 | False     | 0.12905   | False    |

- Chosen k=3, silhouette=0.637, Davies-Bouldin=0.441
- Aggregate viewing order: R2 -> R1 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |           943 |           47.23 |             244.5 |                  16.7 |           2334 |                        100 |               2 |     1020.5 |      796.6 |
|               1 |            2 |           968 |           36.56 |             184.4 |                  83.3 |            340 |                        100 |               1 |     1125.5 |      223.6 |
|               4 |            3 |           362 |           16.21 |             218.7 |                   0   |           5279 |                        100 |               3 |     1218.5 |     1072.4 |

## poster_BarryCeck-1988

- Dropped 140 stray/isolated fixations before clustering (5.2%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |     score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|----------:|:---------|
|   3 |     0.411503 |         0.87944  |             2352.83 | False     | 0.0337337 | False    |
|   4 |     0.449431 |         0.765688 |             2832.02 | False     | 1         | False    |
|   5 |     0.411543 |         0.768022 |             2868.17 | False     | 0.490956  | False    |
|   6 |     0.417323 |         0.887669 |             2861.84 | False     | 0.0767189 | False    |
|   7 |     0.421031 |         0.875976 |             2970.8  | False     | 0.173542  | False    |
|   8 |     0.420401 |         0.872667 |             3056.42 | False     | 0.178793  | True     |

- Chosen k=8, silhouette=0.420, Davies-Bouldin=0.873
- Aggregate viewing order: R4 -> R1 -> R7 -> R5 -> R8 -> R6 -> R2 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               7 |            1 |           509 |           19.6  |             173   |                  39.6 |           1585 |                      100   |               2 |      864.9 |      693.6 |
|               8 |            2 |           383 |           16.94 |             198.7 |                  10.4 |           5655 |                      100   |               7 |     1148.6 |      950.3 |
|              10 |            3 |           427 |           16.58 |             174.4 |                   2.1 |           6031 |                      100   |               8 |      348.2 |      908.7 |
|              13 |            4 |           367 |           14.01 |             171.5 |                  16.7 |           1175 |                      100   |               1 |      922.2 |      131.6 |
|              12 |            5 |           301 |           10.51 |             156.9 |                   0   |           3897 |                       93.8 |               4 |     1550.9 |      191.4 |
|              11 |            6 |           216 |            9.18 |             190.8 |                   0   |           5248 |                       91.7 |               6 |     1388.8 |      521.3 |
|              14 |            7 |           241 |            8.3  |             154.7 |                  29.2 |           2275 |                       97.9 |               3 |     1034.2 |      397.6 |
|               9 |            8 |           126 |            4.86 |             173.4 |                   2.1 |           4818 |                       85.4 |               5 |      589.6 |      512.2 |

## poster_DavidCarson

- Dropped 131 stray/isolated fixations before clustering (5.0%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.517369 |         0.700103 |             3848.98 | False     | 0.928232 | False    |
|   4 |     0.491165 |         0.666333 |             3286    | False     | 0.897046 | True     |
|   5 |     0.424275 |         0.867609 |             3094.08 | False     | 0.206495 | False    |
|   6 |     0.41648  |         0.819388 |             3325.27 | False     | 0.278348 | False    |
|   7 |     0.390108 |         0.901609 |             3382.92 | False     | 0        | False    |
|   8 |     0.395418 |         0.854456 |             3515.26 | False     | 0.121068 | False    |

- Chosen k=4, silhouette=0.491, Davies-Bouldin=0.666
- Aggregate viewing order: R1 -> R3 -> R2 -> R4

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               5 |            1 |           940 |           38.89 |             183.5 |                  64.6 |            404 |                      100   |               1 |      671.6 |      349.1 |
|               1 |            2 |           711 |           28.06 |             175   |                   8.3 |           3113 |                      100   |               3 |     1423.5 |      545.5 |
|               3 |            3 |           652 |           26.8  |             182.3 |                  22.9 |           2095 |                      100   |               2 |      565.5 |      818.4 |
|               6 |            4 |           174 |            6.26 |             159.5 |                   4.2 |           3552 |                       91.7 |               4 |      290.3 |      187.4 |

## poster_DavidCarson-1990

- Dropped 146 stray/isolated fixations before clustering (5.9%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.570976 |         0.608779 |             4641.38 | False     | 1        | True     |
|   4 |     0.497724 |         0.827164 |             4034.77 | False     | 0.496053 | False    |
|   5 |     0.410621 |         0.937208 |             3740.37 | False     | 0.110626 | False    |
|   6 |     0.38012  |         0.958708 |             3614.1  | False     | 0        | False    |
|   7 |     0.389402 |         0.882568 |             3610    | False     | 0.133109 | False    |
|   8 |     0.422328 |         0.794948 |             3945.74 | False     | 0.344566 | False    |

- Chosen k=3, silhouette=0.571, Davies-Bouldin=0.609
- Aggregate viewing order: R3 -> R2 -> R1

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               4 |            1 |           857 |           36.91 |             203.1 |                  20.8 |           2173 |                        100 |               3 |      614.4 |      783.6 |
|               2 |            2 |           815 |           35.54 |             205.7 |                  43.8 |           1151 |                        100 |               2 |     1298.1 |      581.8 |
|               3 |            3 |           663 |           27.56 |             196.1 |                  35.4 |           1088 |                        100 |               1 |      529.7 |      298.5 |

## poster_EllaRosenblatt-2021

- Dropped 163 stray/isolated fixations before clustering (6.4%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.485238 |         0.649612 |             3433.65 | False     | 0.325231 | False    |
|   4 |     0.541319 |         0.61153  |             5621.01 | False     | 0.809715 | False    |
|   5 |     0.556684 |         0.577281 |             5919.03 | False     | 1        | True     |
|   6 |     0.529728 |         0.75586  |             5935.95 | False     | 0.379873 | False    |
|   7 |     0.53138  |         0.714008 |             5780.05 | False     | 0.492551 | False    |
|   8 |     0.520074 |         0.784216 |             5980.65 | False     | 0.243793 | False    |

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
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.425383 |         0.980109 |             2479.45 | False     | 0.529844 | False    |
|   4 |     0.356954 |         1.04566  |             2544.85 | False     | 0        | False    |
|   5 |     0.406617 |         0.82446  |             2771.94 | False     | 0.717101 | False    |
|   6 |     0.411656 |         0.78462  |             2788.68 | False     | 0.823177 | False    |
|   7 |     0.428695 |         0.792838 |             3096.47 | False     | 0.908106 | False    |
|   8 |     0.441585 |         0.806781 |             3440.4  | False     | 0.957552 | True     |

- Chosen k=8, silhouette=0.442, Davies-Bouldin=0.807
- Aggregate viewing order: R2 -> R6 -> R3 -> R8 -> R1 -> R7 -> R5 -> R4

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               7 |            1 |           416 |           18.85 |             224.3 |                   4.2 |           4639 |                      100   |               5 |      746.6 |      745.7 |
|              13 |            2 |           419 |           14.58 |             172.3 |                  47.9 |           1185 |                      100   |               1 |      871.5 |      489.1 |
|               9 |            3 |           341 |           13.63 |             197.9 |                   2.1 |           1876 |                       97.9 |               3 |     1115.3 |      212.4 |
|              11 |            4 |           272 |           13.05 |             237.5 |                   2.1 |           7898 |                       97.9 |               8 |     1132.7 |     1074.9 |
|               8 |            5 |           271 |           11.46 |             209.2 |                   0   |           6934 |                       95.8 |               7 |      738.4 |     1111.4 |
|              10 |            6 |           313 |           11.21 |             177.3 |                  18.8 |           1470 |                      100   |               2 |      858.4 |      167.6 |
|              12 |            7 |           217 |            9.74 |             222   |                   8.3 |           5317 |                       95.8 |               6 |     1050.5 |      778.9 |
|              14 |            8 |           198 |            7.47 |             186.8 |                  16.7 |           3488 |                       89.6 |               4 |     1130.6 |      532.1 |

## poster_JanTschichold-1927-DieFrauohneNamen

- Dropped 162 stray/isolated fixations before clustering (6.6%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.459918 |         0.919899 |             3035    | False     | 0        | False    |
|   4 |     0.477506 |         0.888583 |             3040.67 | False     | 0.106011 | False    |
|   5 |     0.484054 |         0.748391 |             3139.16 | False     | 0.305983 | False    |
|   6 |     0.52327  |         0.664699 |             3677.77 | False     | 0.559677 | False    |
|   7 |     0.591352 |         0.519491 |             6138.97 | False     | 1        | True     |
|   8 |     0.549776 |         0.627417 |             6138.2  | False     | 0.707068 | False    |

- Chosen k=7, silhouette=0.591, Davies-Bouldin=0.519
- Aggregate viewing order: R2 -> R5 -> R3 -> R4 -> R6 -> R1 -> R7

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               5 |            1 |           425 |           21.66 |             247.1 |                   0   |           6377 |                      100   |               6 |     1149.9 |     1031.3 |
|               7 |            2 |           518 |           18.87 |             176.6 |                  37.5 |           1365 |                      100   |               1 |      854   |      185.7 |
|              10 |            3 |           366 |           15.06 |             199.5 |                   0   |           2685 |                      100   |               3 |     1194.6 |      244.5 |
|              11 |            4 |           311 |           14.77 |             230.3 |                  14.6 |           3119 |                      100   |               4 |      880.2 |      774.1 |
|               8 |            5 |           295 |           12.84 |             211   |                  35.4 |           1847 |                       97.9 |               2 |      758.5 |      473   |
|               9 |            6 |           263 |           11.08 |             204.2 |                  12.5 |           4350 |                       97.9 |               5 |     1050.9 |      534.6 |
|              12 |            7 |           126 |            5.71 |             219.8 |                   0   |           9792 |                       72.9 |               7 |      685.6 |     1181.5 |

## poster_JanTschichold-1938-Der

- Dropped 239 stray/isolated fixations before clustering (9.4%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |     score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|----------:|:---------|
|   3 |     0.54135  |         0.767811 |             3163    | False     | 0.0786426 | False    |
|   4 |     0.520999 |         0.687499 |             3398.77 | False     | 0.140575  | False    |
|   5 |     0.606179 |         0.520158 |             5389.61 | False     | 0.76264   | False    |
|   6 |     0.65039  |         0.482157 |             8580.82 | False     | 1         | True     |
|   7 |     0.607034 |         0.572444 |             8578.07 | False     | 0.674427  | False    |
|   8 |     0.590292 |         0.652163 |             8389.87 | False     | 0.470193  | False    |

- Chosen k=6, silhouette=0.650, Davies-Bouldin=0.482
- Aggregate viewing order: R2 -> R3 -> R4 -> R6 -> R1 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               6 |            1 |           542 |           25.82 |             216.5 |                   0   |           5105 |                      100   |               5 |     1471.2 |      949   |
|               7 |            2 |           423 |           19.11 |             205.3 |                  68.8 |           1063 |                      100   |               1 |     1124.5 |      368.6 |
|               5 |            3 |           432 |           18.45 |             194.1 |                  12.5 |           2687 |                      100   |               2 |     1057.6 |      913.7 |
|               9 |            4 |           401 |           16.2  |             183.6 |                  12.5 |           2850 |                      100   |               3 |      457.3 |      581.5 |
|               8 |            5 |           265 |           10.98 |             188.3 |                   4.2 |           6006 |                       95.8 |               6 |      664.2 |      103.2 |
|              10 |            6 |           236 |            9.45 |             182   |                   2.1 |           2985 |                      100   |               4 |      760.4 |      838.7 |

## poster_JoostSchmidt-1923-Saatliches

- Dropped 140 stray/isolated fixations before clustering (5.6%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.432323 |         0.789155 |             2323.36 | False     | 0.527487 | False    |
|   4 |     0.437726 |         0.8468   |             2644.94 | False     | 0.429415 | False    |
|   5 |     0.455652 |         0.885461 |             2723.58 | False     | 0.555131 | False    |
|   6 |     0.418307 |         0.90411  |             2693.32 | False     | 0        | False    |
|   7 |     0.436704 |         0.734972 |             3256.49 | False     | 0.74631  | False    |
|   8 |     0.41843  |         0.745631 |             3430.71 | False     | 0.470138 | True     |

- Chosen k=8, silhouette=0.418, Davies-Bouldin=0.746
- Aggregate viewing order: R2 -> R1 -> R5 -> R7 -> R3 -> R4 -> R6 -> R8

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               8 |            1 |           605 |           28.58 |             230.1 |                  31.2 |           2226 |                      100   |               2 |     1017.5 |      745.7 |
|              10 |            2 |           385 |           14.64 |             185.2 |                  39.6 |           1065 |                      100   |               1 |      850.7 |      330   |
|              13 |            3 |           355 |           14.5  |             199   |                  10.4 |           3868 |                      100   |               5 |      842.8 |      714.5 |
|               7 |            4 |           264 |           11.34 |             209.2 |                   0   |           5102 |                       95.8 |               6 |     1200.1 |      594.8 |
|               9 |            5 |           298 |           11.32 |             185.1 |                   8.3 |           2340 |                      100   |               3 |      677.2 |      268.4 |
|              14 |            6 |           198 |            8.7  |             214   |                   0   |           5403 |                       93.8 |               7 |      730.7 |      839.1 |
|              11 |            7 |           175 |            6.83 |             190   |                  10.4 |           3400 |                       95.8 |               4 |     1042.2 |      391.4 |
|              12 |            8 |            62 |            4.09 |             321.4 |                   0   |           8008 |                       60.4 |               8 |     1327.6 |       92   |

## poster_PaulRand-1947

- Dropped 99 stray/isolated fixations before clustering (3.8%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |     score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|----------:|:---------|
|   3 |     0.54498  |         0.647973 |             3355.21 | False     | 1         | False    |
|   4 |     0.532835 |         0.676212 |             3277.25 | False     | 0.882255  | True     |
|   5 |     0.514739 |         0.799318 |             3493.97 | False     | 0.510464  | False    |
|   6 |     0.432506 |         0.854311 |             3295.04 | False     | 0.0432877 | False    |
|   7 |     0.433354 |         0.792114 |             3273.77 | False     | 0.197448  | False    |
|   8 |     0.421845 |         0.83042  |             3230.4  | False     | 0.0578926 | False    |

- Chosen k=4, silhouette=0.533, Davies-Bouldin=0.676
- Aggregate viewing order: R1 -> R2 -> R4 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               3 |            1 |          1056 |           40.21 |             188.1 |                  60.4 |            517 |                        100 |               1 |      687.9 |      632.6 |
|               4 |            2 |           670 |           26.68 |             196.7 |                  35.4 |           1955 |                        100 |               2 |     1094.2 |      452.4 |
|               6 |            3 |           425 |           18.13 |             210.7 |                   0   |           4909 |                        100 |               4 |      815.2 |     1069.3 |
|               5 |            4 |           324 |           14.97 |             228.2 |                   4.2 |           3812 |                        100 |               3 |     1121.3 |      967.1 |

## poster_PaulaScher-1995

- Dropped 77 stray/isolated fixations before clustering (2.8%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.479497 |         0.763238 |             3149.18 | False     | 1        | False    |
|   4 |     0.431761 |         0.829773 |             3717.94 | False     | 0.63621  | True     |
|   5 |     0.39365  |         0.904055 |             3336.28 | False     | 0.293985 | False    |
|   6 |     0.396012 |         0.831806 |             3618.74 | False     | 0.480736 | False    |
|   7 |     0.389958 |         0.879516 |             3582.19 | False     | 0.33849  | False    |
|   8 |     0.36073  |         0.967552 |             3529.43 | False     | 0        | False    |

- Chosen k=4, silhouette=0.432, Davies-Bouldin=0.830
- Aggregate viewing order: R1 -> R3 -> R4 -> R2

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               5 |            1 |           938 |           35.64 |             191.5 |                  81.2 |            297 |                        100 |               1 |      836   |      250.9 |
|               3 |            2 |           618 |           23.86 |             194.6 |                   4.2 |           5544 |                        100 |               4 |     1125.1 |      889.8 |
|               6 |            3 |           571 |           20.61 |             182   |                  12.5 |           3037 |                        100 |               2 |     1154.9 |      392   |
|               4 |            4 |           517 |           19.88 |             193.8 |                   2.1 |           4699 |                        100 |               3 |      724.7 |      950.3 |

## poster_ScottBarry-2010

- Dropped 174 stray/isolated fixations before clustering (6.6%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.404615 |         0.980947 |             2831.64 | False     | 0        | False    |
|   4 |     0.449585 |         0.83257  |             3180.12 | False     | 0.381492 | False    |
|   5 |     0.451753 |         0.729691 |             3323.69 | False     | 0.53042  | False    |
|   6 |     0.530119 |         0.614281 |             4412.43 | False     | 1        | False    |
|   7 |     0.519938 |         0.70052  |             4774.41 | False     | 0.84184  | False    |
|   8 |     0.517731 |         0.668054 |             5145.78 | False     | 0.87732  | True     |

- Chosen k=8, silhouette=0.518, Davies-Bouldin=0.668
- Aggregate viewing order: R4 -> R3 -> R2 -> R1 -> R6 -> R7 -> R5 -> R8

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               7 |            1 |           507 |           21.45 |             204.3 |                   8.3 |           3319 |                      100   |               4 |     1150.2 |      695.8 |
|               9 |            2 |           487 |           20.24 |             200.7 |                   8.3 |           2919 |                      100   |               3 |      931.7 |      967.8 |
|               8 |            3 |           342 |           13.73 |             193.9 |                  35.4 |           2100 |                      100   |               2 |      871.4 |      649.5 |
|              11 |            4 |           383 |           13.73 |             173.1 |                  14.6 |           1789 |                      100   |               1 |      820.8 |      188.9 |
|              10 |            5 |           277 |           12.76 |             222.5 |                   0   |           7001 |                       97.9 |               7 |     1251.1 |     1035.8 |
|              13 |            6 |           268 |           11.12 |             200.4 |                   0   |           4353 |                       95.8 |               5 |     1241.3 |      134.3 |
|              12 |            7 |           130 |            4.77 |             177.1 |                  31.2 |           4426 |                       85.4 |               6 |      838.2 |      454.2 |
|              14 |            8 |            58 |            2.19 |             182.6 |                   2.1 |           7372 |                       54.2 |               8 |     1170.9 |      453.1 |

## poster_SeanAlatorre

- Dropped 96 stray/isolated fixations before clustering (3.9%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.449948 |         0.967018 |             2420.79 | False     | 0        | False    |
|   4 |     0.539963 |         0.75766  |             3499.86 | False     | 0.706207 | False    |
|   5 |     0.532622 |         0.671141 |             3916.36 | False     | 0.809748 | False    |
|   6 |     0.568214 |         0.645568 |             4622.31 | False     | 1        | False    |
|   7 |     0.567312 |         0.665509 |             4609.66 | False     | 0.96517  | True     |
|   8 |     0.519849 |         0.776927 |             4481.19 | False     | 0.591203 | False    |

- Chosen k=7, silhouette=0.567, Davies-Bouldin=0.666
- Aggregate viewing order: R1 -> R3 -> R5 -> R2 -> R4 -> R7 -> R6

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               6 |            1 |           572 |           22.72 |             198.4 |                  31.2 |           1650 |                      100   |               1 |      875.6 |      236   |
|               7 |            2 |           450 |           19.59 |             217.5 |                  29.2 |           2552 |                      100   |               4 |     1064.2 |      568.5 |
|               5 |            3 |           441 |           17.38 |             196.9 |                   2.1 |           2149 |                       95.8 |               2 |     1262.9 |      127.7 |
|              11 |            4 |           269 |           12.58 |             233.6 |                   8.3 |           5899 |                       97.9 |               5 |     1242.1 |      696.1 |
|               9 |            5 |           292 |           11.89 |             203.4 |                  29.2 |           2242 |                      100   |               3 |      848.2 |      671.4 |
|              10 |            6 |           180 |            8.54 |             237   |                   0   |           7210 |                       87.5 |               7 |      855.2 |      977.8 |
|              12 |            7 |           169 |            7.31 |             216   |                   0   |           6154 |                       85.4 |               6 |     1197.6 |      887.7 |

## poster_bookcover

- Dropped 103 stray/isolated fixations before clustering (4.0%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |     score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|----------:|:---------|
|   3 |     0.429473 |         0.903931 |             3591.78 | False     | 0.148383  | False    |
|   4 |     0.405987 |         0.893347 |             3486.47 | False     | 0.0211299 | False    |
|   5 |     0.423832 |         0.864823 |             3653.07 | False     | 0.190814  | False    |
|   6 |     0.452965 |         0.768277 |             3834.1  | False     | 0.567614  | False    |
|   7 |     0.467295 |         0.729253 |             4052.1  | False     | 0.736052  | False    |
|   8 |     0.485127 |         0.65347  |             4510.77 | False     | 1         | True     |

- Chosen k=8, silhouette=0.485, Davies-Bouldin=0.653
- Aggregate viewing order: R5 -> R3 -> R1 -> R6 -> R7 -> R4 -> R2 -> R8

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               6 |            1 |           558 |           20.85 |             188.2 |                   8.3 |           2328 |                      100   |               3 |     1091.7 |      189.1 |
|               9 |            2 |           461 |           20.08 |             219.4 |                   0   |           4674 |                      100   |               7 |     1073.3 |      984.5 |
|               7 |            3 |           362 |           13.1  |             182.3 |                  22.9 |           1926 |                      100   |               2 |      834.3 |      633.9 |
|              13 |            4 |           238 |           10.65 |             225.4 |                   6.2 |           4557 |                       95.8 |               6 |      980   |      762.5 |
|              11 |            5 |           325 |           10.62 |             164.5 |                  50   |           1072 |                       97.9 |               1 |      913.6 |      426.1 |
|              12 |            6 |           210 |            9.65 |             231.4 |                   8.3 |           2871 |                       95.8 |               4 |      848.8 |      223.2 |
|              14 |            7 |           230 |            9.23 |             202   |                   4.2 |           4159 |                      100   |               5 |     1169.4 |      646.4 |
|              10 |            8 |           111 |            5.82 |             264.2 |                   0   |           6239 |                       81.2 |               8 |      774   |      909.4 |

## poster_nancy

- Dropped 265 stray/isolated fixations before clustering (10.9%)
- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):

|   k |   silhouette |   davies_bouldin |   calinski_harabasz | crosses   |    score | chosen   |
|----:|-------------:|-----------------:|--------------------:|:----------|---------:|:---------|
|   3 |     0.51716  |         0.672859 |             2864.35 | False     | 0.809333 | False    |
|   4 |     0.533924 |         0.644117 |             3933.18 | False     | 1        | False    |
|   5 |     0.47016  |         0.713776 |             3567.04 | False     | 0.419135 | True     |
|   6 |     0.448934 |         0.748015 |             3574.33 | False     | 0.185555 | False    |
|   7 |     0.436526 |         0.781497 |             3702.79 | False     | 0        | False    |
|   8 |     0.450381 |         0.770557 |             3875.79 | False     | 0.11094  | False    |

- Chosen k=5, silhouette=0.470, Davies-Bouldin=0.714
- Aggregate viewing order: R3 -> R2 -> R1 -> R5 -> R4

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               4 |            1 |           803 |           42.2  |             258.7 |                   8.3 |           2615 |                      100   |               3 |     1088.3 |      775.2 |
|               6 |            2 |           523 |           21.96 |             206.7 |                  39.6 |           1300 |                      100   |               2 |      869.2 |      270.4 |
|               5 |            3 |           429 |           17.68 |             202.8 |                  43.8 |            747 |                      100   |               1 |      840.9 |      561.1 |
|               7 |            4 |           304 |           14.14 |             229   |                   2.1 |           4076 |                      100   |               5 |      806.7 |      910.8 |
|               8 |            5 |            97 |            4.01 |             203.7 |                   6.2 |           3961 |                       70.8 |               4 |      854.4 |      684.8 |
