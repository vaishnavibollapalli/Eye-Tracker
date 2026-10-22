# Clustering Method Comparison -- per poster

## poster_ArminHofman-1955
**Winner: DBSCAN**  -  DBSCAN wins: highest separation score (0.796 after a 20% noise discount), k=3 regions, silhouette 0.750, Davies-Bouldin 0.324; Agglomerative scored 0.031 at k=3 (silhouette 0.635, DB 0.434); Divisive scored 0.009 at k=3 (silhouette 0.637, DB 0.441). k chosen per method: DBSCAN=3, Agglomerative=3, Divisive=3.

| method        |   k |   silhouette |   davies_bouldin |   noise_pct | crosses   |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|:----------|-------------------:|
| DBSCAN        |   3 |        0.75  |            0.324 |        20.4 | False     |              0.796 |
| Agglomerative |   3 |        0.635 |            0.434 |         0   | False     |              0.031 |
| Divisive      |   3 |        0.637 |            0.441 |         0   | False     |              0.009 |

## poster_BarryCeck-1988
**Winner: Agglomerative**  -  Agglomerative wins: highest separation score (1.000), k=4 regions, silhouette 0.461, Davies-Bouldin 0.739; DBSCAN scored 0.026 at k=7 (silhouette 0.393, DB 0.865, 8% noise); Divisive scored 0.202 at k=8 (silhouette 0.420, DB 0.873). k chosen per method: DBSCAN=7, Agglomerative=4, Divisive=8.

| method        |   k |   silhouette |   davies_bouldin |   noise_pct | crosses   |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|:----------|-------------------:|
| DBSCAN        |   7 |        0.393 |            0.865 |           8 | True      |              0.026 |
| Agglomerative |   4 |        0.461 |            0.739 |           0 | False     |              1     |
| Divisive      |   8 |        0.42  |            0.873 |           0 | False     |              0.202 |

## poster_DavidCarson
**Winner: Divisive**  -  Divisive wins: highest separation score (0.619), k=4 regions, silhouette 0.491, Davies-Bouldin 0.666; DBSCAN scored 0.460 at k=7 (silhouette 0.449, DB 0.522, 24% noise); Agglomerative scored 0.000 at k=8 (silhouette 0.437, DB 0.712). k chosen per method: DBSCAN=7, Agglomerative=8, Divisive=4.

| method        |   k |   silhouette |   davies_bouldin |   noise_pct | crosses   |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|:----------|-------------------:|
| DBSCAN        |   7 |        0.449 |            0.522 |        24.3 | False     |              0.46  |
| Agglomerative |   8 |        0.437 |            0.712 |         0   | False     |              0     |
| Divisive      |   4 |        0.491 |            0.666 |         0   | False     |              0.619 |

## poster_DavidCarson-1990
**Winner: Divisive**  -  Divisive wins: highest separation score (0.568), k=3 regions, silhouette 0.571, Davies-Bouldin 0.609; DBSCAN scored 0.409 at k=7 (silhouette 0.529, DB 0.488, 18% noise); Agglomerative scored 0.416 at k=3 (silhouette 0.564, DB 0.628). k chosen per method: DBSCAN=7, Agglomerative=3, Divisive=3.

| method        |   k |   silhouette |   davies_bouldin |   noise_pct | crosses   |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|:----------|-------------------:|
| DBSCAN        |   7 |        0.529 |            0.488 |        18.2 | False     |              0.409 |
| Agglomerative |   3 |        0.564 |            0.628 |         0   | False     |              0.416 |
| Divisive      |   3 |        0.571 |            0.609 |         0   | False     |              0.568 |

## poster_EllaRosenblatt-2021
**Winner: DBSCAN**  -  DBSCAN wins: highest separation score (0.788 after a 21% noise discount), k=6 regions, silhouette 0.697, Davies-Bouldin 0.397; Agglomerative scored 0.053 at k=6 (silhouette 0.572, DB 0.604); Divisive scored 0.064 at k=5 (silhouette 0.557, DB 0.577). k chosen per method: DBSCAN=6, Agglomerative=6, Divisive=5.

| method        |   k |   silhouette |   davies_bouldin |   noise_pct | crosses   |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|:----------|-------------------:|
| DBSCAN        |   6 |        0.697 |            0.397 |        21.2 | False     |              0.788 |
| Agglomerative |   6 |        0.572 |            0.604 |         0   | False     |              0.053 |
| Divisive      |   5 |        0.557 |            0.577 |         0   | False     |              0.064 |

## poster_IrisChung-2015
**Winner: Agglomerative**  -  Agglomerative wins: highest separation score (0.742), k=8 regions, silhouette 0.458, Davies-Bouldin 0.688; DBSCAN scored 0.464 at k=7 (silhouette 0.400, DB 0.561, 7% noise); Divisive scored 0.360 at k=8 (silhouette 0.442, DB 0.807). k chosen per method: DBSCAN=7, Agglomerative=8, Divisive=8.

| method        |   k |   silhouette |   davies_bouldin |   noise_pct | crosses   |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|:----------|-------------------:|
| DBSCAN        |   7 |        0.4   |            0.561 |         7.2 | False     |              0.464 |
| Agglomerative |   8 |        0.458 |            0.688 |         0   | False     |              0.742 |
| Divisive      |   8 |        0.442 |            0.807 |         0   | False     |              0.36  |

## poster_JanTschichold-1927-DieFrauohneNamen
**Winner: DBSCAN**  -  DBSCAN wins: highest separation score (0.912 after a 9% noise discount), k=7 regions, silhouette 0.626, Davies-Bouldin 0.444; Agglomerative scored 0.068 at k=8 (silhouette 0.596, DB 0.534); Divisive scored 0.082 at k=7 (silhouette 0.591, DB 0.519). k chosen per method: DBSCAN=7, Agglomerative=8, Divisive=7.

| method        |   k |   silhouette |   davies_bouldin |   noise_pct | crosses   |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|:----------|-------------------:|
| DBSCAN        |   7 |        0.626 |            0.444 |         8.8 | False     |              0.912 |
| Agglomerative |   8 |        0.596 |            0.534 |         0   | False     |              0.068 |
| Divisive      |   7 |        0.591 |            0.519 |         0   | False     |              0.082 |

## poster_JanTschichold-1938-Der
**Winner: Divisive**  -  Divisive wins: highest separation score (1.000), k=6 regions, silhouette 0.650, Davies-Bouldin 0.482; DBSCAN scored 0.000 at k=6 (silhouette 0.608, DB 0.531, 2% noise); Agglomerative scored 0.730 at k=6 (silhouette 0.634, DB 0.490). k chosen per method: DBSCAN=6, Agglomerative=6, Divisive=6.

| method        |   k |   silhouette |   davies_bouldin |   noise_pct | crosses   |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|:----------|-------------------:|
| DBSCAN        |   6 |        0.608 |            0.531 |           2 | False     |               0    |
| Agglomerative |   6 |        0.634 |            0.49  |           0 | False     |               0.73 |
| Divisive      |   6 |        0.65  |            0.482 |           0 | False     |               1    |

## poster_JoostSchmidt-1923-Saatliches
**Winner: DBSCAN**  -  DBSCAN wins: highest separation score (0.712 after a 8% noise discount), k=6 regions, silhouette 0.477, Davies-Bouldin 0.483; Agglomerative scored 0.500 at k=3 (silhouette 0.524, DB 0.789); Divisive scored 0.071 at k=8 (silhouette 0.418, DB 0.746). k chosen per method: DBSCAN=6, Agglomerative=3, Divisive=8.

| method        |   k |   silhouette |   davies_bouldin |   noise_pct | crosses   |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|:----------|-------------------:|
| DBSCAN        |   6 |        0.477 |            0.483 |         8.3 | False     |              0.712 |
| Agglomerative |   3 |        0.524 |            0.789 |         0   | False     |              0.5   |
| Divisive      |   8 |        0.418 |            0.746 |         0   | False     |              0.071 |

## poster_PaulRand-1947
**Winner: DBSCAN**  -  DBSCAN wins: highest separation score (0.778 after a 22% noise discount), k=7 regions, silhouette 0.600, Davies-Bouldin 0.389; Agglomerative scored 0.000 at k=8 (silhouette 0.498, DB 0.719); Divisive scored 0.235 at k=4 (silhouette 0.533, DB 0.676). k chosen per method: DBSCAN=7, Agglomerative=8, Divisive=4.

| method        |   k |   silhouette |   davies_bouldin |   noise_pct | crosses   |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|:----------|-------------------:|
| DBSCAN        |   7 |        0.6   |            0.389 |        22.2 | False     |              0.778 |
| Agglomerative |   8 |        0.498 |            0.719 |         0   | False     |              0     |
| Divisive      |   4 |        0.533 |            0.676 |         0   | False     |              0.235 |

## poster_PaulaScher-1995
**Winner: Agglomerative**  -  Agglomerative wins: highest separation score (0.794), k=8 regions, silhouette 0.415, Davies-Bouldin 0.751; DBSCAN scored 0.484 at k=4 (silhouette 0.280, DB 0.718, 3% noise); Divisive scored 0.500 at k=4 (silhouette 0.432, DB 0.830). k chosen per method: DBSCAN=4, Agglomerative=8, Divisive=4.

| method        |   k |   silhouette |   davies_bouldin |   noise_pct | crosses   |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|:----------|-------------------:|
| DBSCAN        |   4 |        0.28  |            0.718 |         3.2 | False     |              0.484 |
| Agglomerative |   8 |        0.415 |            0.751 |         0   | False     |              0.794 |
| Divisive      |   4 |        0.432 |            0.83  |         0   | False     |              0.5   |

## poster_ScottBarry-2010
**Winner: Agglomerative**  -  Agglomerative wins: highest separation score (1.000), k=8 regions, silhouette 0.561, Davies-Bouldin 0.575; DBSCAN scored 0.415 at k=6 (silhouette 0.457, DB 0.589, 3% noise); Divisive scored 0.291 at k=8 (silhouette 0.518, DB 0.668). k chosen per method: DBSCAN=6, Agglomerative=8, Divisive=8.

| method        |   k |   silhouette |   davies_bouldin |   noise_pct | crosses   |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|:----------|-------------------:|
| DBSCAN        |   6 |        0.457 |            0.589 |         2.7 | False     |              0.415 |
| Agglomerative |   8 |        0.561 |            0.575 |         0   | False     |              1     |
| Divisive      |   8 |        0.518 |            0.668 |         0   | False     |              0.291 |

## poster_SeanAlatorre
**Winner: DBSCAN**  -  DBSCAN wins: highest separation score (0.806 after a 19% noise discount), k=8 regions, silhouette 0.600, Davies-Bouldin 0.475; Agglomerative scored 0.103 at k=6 (silhouette 0.539, DB 0.626); Divisive scored 0.231 at k=7 (silhouette 0.567, DB 0.666). k chosen per method: DBSCAN=8, Agglomerative=6, Divisive=7.

| method        |   k |   silhouette |   davies_bouldin |   noise_pct | crosses   |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|:----------|-------------------:|
| DBSCAN        |   8 |        0.6   |            0.475 |        19.4 | False     |              0.806 |
| Agglomerative |   6 |        0.539 |            0.626 |         0   | False     |              0.103 |
| Divisive      |   7 |        0.567 |            0.666 |         0   | False     |              0.231 |

## poster_bookcover
**Winner: DBSCAN**  -  DBSCAN wins: highest separation score (0.829 after a 17% noise discount), k=8 regions, silhouette 0.582, Davies-Bouldin 0.445; Agglomerative scored 0.183 at k=8 (silhouette 0.521, DB 0.670); Divisive scored 0.036 at k=8 (silhouette 0.485, DB 0.653). k chosen per method: DBSCAN=8, Agglomerative=8, Divisive=8.

| method        |   k |   silhouette |   davies_bouldin |   noise_pct | crosses   |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|:----------|-------------------:|
| DBSCAN        |   8 |        0.582 |            0.445 |        17.1 | False     |              0.829 |
| Agglomerative |   8 |        0.521 |            0.67  |         0   | False     |              0.183 |
| Divisive      |   8 |        0.485 |            0.653 |         0   | False     |              0.036 |

## poster_nancy
**Winner: DBSCAN**  -  DBSCAN wins: highest separation score (0.792 after a 21% noise discount), k=5 regions, silhouette 0.646, Davies-Bouldin 0.428; Agglomerative scored 0.610 at k=4 (silhouette 0.588, DB 0.557); Divisive scored 0.000 at k=5 (silhouette 0.470, DB 0.714). k chosen per method: DBSCAN=5, Agglomerative=4, Divisive=5.

| method        |   k |   silhouette |   davies_bouldin |   noise_pct | crosses   |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|:----------|-------------------:|
| DBSCAN        |   5 |        0.646 |            0.428 |        20.8 | False     |              0.792 |
| Agglomerative |   4 |        0.588 |            0.557 |         0   | False     |              0.61  |
| Divisive      |   5 |        0.47  |            0.714 |         0   | False     |              0     |
