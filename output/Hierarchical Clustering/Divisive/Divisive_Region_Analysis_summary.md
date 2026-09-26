# Divisive (Bisecting K-Means) Region Analysis -- summary

Posters: poster_EllaRosenblatt-2021, poster_IrisChung-2015, poster_JanTschichold-1927-DieFrauohneNamen, poster_JanTschichold-1938-Der, poster_JoostSchmidt-1923-Saatliches
Participants pooled: 48

## poster_EllaRosenblatt-2021

- k selection (silhouette by k):

|   k |   silhouette |
|----:|-------------:|
|   5 |     0.516441 |
|   4 |     0.514956 |
|   7 |     0.488664 |
|   6 |     0.482749 |
|   3 |     0.471893 |

- Chosen k=5, silhouette=0.516
- Aggregate viewing order: R2 -> R1 -> R4 -> R3 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               7 |            1 |           746 |           30.42 |             216.3 |                  22.9 |           1273 |                      100   |               2 |      817.9 |      778.8 |
|               5 |            2 |           592 |           22.11 |             198.2 |                  62.5 |            844 |                      100   |               1 |      944.8 |      532.6 |
|               3 |            3 |           508 |           21.27 |             222.2 |                   0   |           4422 |                       97.9 |               4 |     1051.9 |     1057.1 |
|               6 |            4 |           572 |           21.04 |             195.2 |                  14.6 |           3554 |                      100   |               3 |     1110.6 |      203.6 |
|               8 |            5 |           127 |            5.15 |             215.1 |                   0   |           7909 |                       89.6 |               5 |      681.7 |     1054.3 |

## poster_IrisChung-2015

- k selection (silhouette by k):

|   k |   silhouette |
|----:|-------------:|
|   3 |     0.423732 |
|   7 |     0.420316 |
|   6 |     0.404043 |
|   5 |     0.39643  |
|   4 |     0.353351 |

- Chosen k=3, silhouette=0.424
- Aggregate viewing order: R1 -> R2 -> R3

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               1 |            1 |          1301 |           46.06 |             181.4 |                  87.5 |            329 |                        100 |               1 |      983.3 |      334.7 |
|               3 |            2 |           710 |           29.99 |             216.4 |                   2.1 |           4138 |                        100 |               2 |      745.2 |      884.8 |
|               4 |            3 |           541 |           23.95 |             226.8 |                  10.4 |           4846 |                        100 |               3 |     1105.8 |      943.6 |

## poster_JanTschichold-1927-DieFrauohneNamen

- k selection (silhouette by k):

|   k |   silhouette |
|----:|-------------:|
|   7 |     0.558749 |
|   6 |     0.496633 |
|   5 |     0.460452 |
|   4 |     0.457762 |
|   3 |     0.451826 |

- Chosen k=7, silhouette=0.559
- Aggregate viewing order: R2 -> R5 -> R4 -> R3 -> R6 -> R1 -> R7

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               6 |            1 |           455 |           21.8  |             247.4 |                   0   |           6358 |                      100   |               6 |     1147.2 |     1028.8 |
|               7 |            2 |           536 |           18.29 |             176.2 |                  35.4 |           1345 |                      100   |               1 |      849.6 |      184.3 |
|              12 |            3 |           354 |           16.02 |             233.6 |                  14.6 |           3112 |                      100   |               4 |      880.1 |      779   |
|               9 |            4 |           383 |           14.59 |             196.6 |                   2.1 |           2595 |                      100   |               3 |     1193.1 |      239.6 |
|               8 |            5 |           318 |           12.58 |             204.2 |                  35.4 |           1657 |                      100   |               2 |      760.8 |      471.2 |
|              10 |            6 |           278 |           10.8  |             200.6 |                  12.5 |           4265 |                      100   |               5 |     1052.8 |      525.1 |
|              11 |            7 |           142 |            5.93 |             215.4 |                   0   |           9368 |                       79.2 |               7 |      690   |     1170.6 |

## poster_JanTschichold-1938-Der

- k selection (silhouette by k):

|   k |   silhouette |
|----:|-------------:|
|   6 |     0.582246 |
|   7 |     0.579806 |
|   5 |     0.549816 |
|   3 |     0.507194 |
|   4 |     0.475688 |

- Chosen k=6, silhouette=0.582
- Aggregate viewing order: R2 -> R3 -> R4 -> R6 -> R1 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               5 |            1 |           601 |           26.02 |             213.2 |                   0   |           4883 |                      100   |               5 |     1472.2 |      926.4 |
|               8 |            2 |           477 |           19.14 |             197.5 |                  66.7 |            644 |                      100   |               1 |     1117.6 |      373.7 |
|               6 |            3 |           489 |           19.03 |             191.6 |                  10.4 |           2446 |                      100   |               2 |     1067.2 |      894.3 |
|               9 |            4 |           421 |           15.58 |             182.2 |                   6.2 |           2762 |                      100   |               3 |      455.6 |      585.4 |
|               7 |            5 |           291 |           10.86 |             183.7 |                   8.3 |           5567 |                       97.9 |               6 |      665.9 |      106.5 |
|              10 |            6 |           259 |            9.36 |             178   |                   8.3 |           2768 |                      100   |               4 |      756.4 |      836.2 |

## poster_JoostSchmidt-1923-Saatliches

- k selection (silhouette by k):

|   k |   silhouette |
|----:|-------------:|
|   5 |     0.442936 |
|   4 |     0.433863 |
|   7 |     0.420547 |
|   3 |     0.419614 |
|   6 |     0.403154 |

- Chosen k=5, silhouette=0.443
- Aggregate viewing order: R2 -> R1 -> R3 -> R4 -> R5

|   region_raw_id |   region_num |   n_fixations |   pct_gaze_time |   avg_fixation_ms |   first_attention_pct |   avg_entry_ms |   participant_coverage_pct |   viewing_order |   center_x |   center_y |
|----------------:|-------------:|--------------:|----------------:|------------------:|----------------------:|---------------:|---------------------------:|----------------:|-----------:|-----------:|
|               8 |            1 |           635 |           28.37 |             228.3 |                  31.2 |           2123 |                      100   |               2 |     1021.1 |      749.2 |
|               5 |            2 |           729 |           26.49 |             185.6 |                  50   |            690 |                      100   |               1 |      779.3 |      303.8 |
|               4 |            3 |           590 |           23.41 |             202.7 |                   8.3 |           3486 |                      100   |               3 |      798.2 |      769.9 |
|               6 |            4 |           258 |           11.06 |             219   |                   8.3 |           3655 |                       97.9 |               4 |     1165.2 |      281.2 |
|               7 |            5 |           270 |           10.66 |             201.8 |                   2.1 |           5071 |                       95.8 |               5 |     1210.6 |      603.5 |
