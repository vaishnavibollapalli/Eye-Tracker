# Clustering Method Comparison -- per poster

## poster_ArminHofman-1955
**Winner: DBSCAN**  -  DBSCAN wins: highest separation score (0.796 after a 20% noise discount), silhouette 0.750, Davies-Bouldin 0.324; Agglomerative scored 0.031 (silhouette 0.635, DB 0.434); Divisive scored 0.009 (silhouette 0.637, DB 0.441).

| method        |   k |   silhouette |   davies_bouldin |   noise_pct |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|-------------------:|
| DBSCAN        |   3 |        0.75  |            0.324 |        20.4 |              0.796 |
| Agglomerative |   3 |        0.635 |            0.434 |         0   |              0.031 |
| Divisive      |   3 |        0.637 |            0.441 |         0   |              0.009 |

## poster_BarryCeck-1988
**Winner: Agglomerative**  -  Agglomerative wins: highest separation score (1.000), silhouette 0.461, Davies-Bouldin 0.739; DBSCAN scored 0.000 (silhouette 0.130, DB 0.903, 4% noise); Divisive scored 0.899 (silhouette 0.449, DB 0.766).

| method        |   k |   silhouette |   davies_bouldin |   noise_pct |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|-------------------:|
| DBSCAN        |   4 |        0.13  |            0.903 |         3.5 |              0     |
| Agglomerative |   4 |        0.461 |            0.739 |         0   |              1     |
| Divisive      |   4 |        0.449 |            0.766 |         0   |              0.899 |

## poster_DavidCarson
**Winner: DBSCAN**  -  DBSCAN wins: highest separation score (0.768 after a 23% noise discount), silhouette 0.525, Davies-Bouldin 0.515; Agglomerative scored 0.156 (silhouette 0.470, DB 0.643); Divisive scored 0.429 (silhouette 0.517, DB 0.700).

| method        |   k |   silhouette |   davies_bouldin |   noise_pct |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|-------------------:|
| DBSCAN        |   5 |        0.525 |            0.515 |        23.2 |              0.768 |
| Agglomerative |   5 |        0.47  |            0.643 |         0   |              0.156 |
| Divisive      |   3 |        0.517 |            0.7   |         0   |              0.429 |

## poster_DavidCarson-1990
**Winner: Divisive**  -  Divisive wins: highest separation score (0.709), silhouette 0.571, Davies-Bouldin 0.609; DBSCAN scored 0.433 (silhouette 0.532, DB 0.582, 13% noise); Agglomerative scored 0.410 (silhouette 0.564, DB 0.628).

| method        |   k |   silhouette |   davies_bouldin |   noise_pct |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|-------------------:|
| DBSCAN        |   5 |        0.532 |            0.582 |        13.5 |              0.433 |
| Agglomerative |   3 |        0.564 |            0.628 |         0   |              0.41  |
| Divisive      |   3 |        0.571 |            0.609 |         0   |              0.709 |

## poster_EllaRosenblatt-2021
**Winner: Agglomerative**  -  Agglomerative wins: highest separation score (0.500), silhouette 0.574, Davies-Bouldin 0.584; DBSCAN scored 0.455 (silhouette 0.500, DB 0.532, 9% noise); Divisive scored 0.444 (silhouette 0.557, DB 0.577).

| method        |   k |   silhouette |   davies_bouldin |   noise_pct |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|-------------------:|
| DBSCAN        |   5 |        0.5   |            0.532 |           9 |              0.455 |
| Agglomerative |   5 |        0.574 |            0.584 |           0 |              0.5   |
| Divisive      |   5 |        0.557 |            0.577 |           0 |              0.444 |

## poster_IrisChung-2015
**Winner: Agglomerative**  -  Agglomerative wins: highest separation score (0.655), silhouette 0.431, Davies-Bouldin 0.730; DBSCAN scored 0.485 (silhouette 0.399, DB 0.521, 3% noise); Divisive scored 0.121 (silhouette 0.407, DB 0.824).

| method        |   k |   silhouette |   davies_bouldin |   noise_pct |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|-------------------:|
| DBSCAN        |   3 |        0.399 |            0.521 |         2.9 |              0.485 |
| Agglomerative |   4 |        0.431 |            0.73  |         0   |              0.655 |
| Divisive      |   5 |        0.407 |            0.824 |         0   |              0.121 |

## poster_JanTschichold-1927-DieFrauohneNamen
**Winner: DBSCAN**  -  DBSCAN wins: highest separation score (0.912 after a 9% noise discount), silhouette 0.626, Davies-Bouldin 0.444; Agglomerative scored 0.191 (silhouette 0.501, DB 0.669); Divisive scored 0.000 (silhouette 0.484, DB 0.748).

| method        |   k |   silhouette |   davies_bouldin |   noise_pct |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|-------------------:|
| DBSCAN        |   7 |        0.626 |            0.444 |         8.8 |              0.912 |
| Agglomerative |   5 |        0.501 |            0.669 |         0   |              0.191 |
| Divisive      |   5 |        0.484 |            0.748 |         0   |              0     |

## poster_JanTschichold-1938-Der
**Winner: Agglomerative**  -  Agglomerative wins: highest separation score (1.000), silhouette 0.642, Davies-Bouldin 0.475; DBSCAN scored 0.018 (silhouette 0.608, DB 0.531, 2% noise); Divisive scored 0.096 (silhouette 0.606, DB 0.520).

| method        |   k |   silhouette |   davies_bouldin |   noise_pct |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|-------------------:|
| DBSCAN        |   6 |        0.608 |            0.531 |           2 |              0.018 |
| Agglomerative |   5 |        0.642 |            0.475 |           0 |              1     |
| Divisive      |   5 |        0.606 |            0.52  |           0 |              0.096 |

## poster_JoostSchmidt-1923-Saatliches
**Winner: DBSCAN**  -  DBSCAN wins: highest separation score (0.943 after a 6% noise discount), silhouette 0.515, Davies-Bouldin 0.459; Agglomerative scored 0.555 (silhouette 0.499, DB 0.690); Divisive scored 0.000 (silhouette 0.432, DB 0.789).

| method        |   k |   silhouette |   davies_bouldin |   noise_pct |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|-------------------:|
| DBSCAN        |   5 |        0.515 |            0.459 |         5.7 |              0.943 |
| Agglomerative |   5 |        0.499 |            0.69  |         0   |              0.555 |
| Divisive      |   3 |        0.432 |            0.789 |         0   |              0     |

## poster_PaulRand-1947
**Winner: Divisive**  -  Divisive wins: highest separation score (0.670), silhouette 0.545, Davies-Bouldin 0.648; DBSCAN scored 0.451 (silhouette 0.476, DB 0.519, 10% noise); Agglomerative scored 0.230 (silhouette 0.508, DB 0.714).

| method        |   k |   silhouette |   davies_bouldin |   noise_pct |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|-------------------:|
| DBSCAN        |   5 |        0.476 |            0.519 |         9.8 |              0.451 |
| Agglomerative |   3 |        0.508 |            0.714 |         0   |              0.23  |
| Divisive      |   3 |        0.545 |            0.648 |         0   |              0.67  |

## poster_PaulaScher-1995
**Winner: Divisive**  -  Divisive wins: highest separation score (0.588), silhouette 0.479, Davies-Bouldin 0.763; DBSCAN scored 0.484 (silhouette 0.280, DB 0.718, 3% noise); Agglomerative scored 0.423 (silhouette 0.449, DB 0.773).

| method        |   k |   silhouette |   davies_bouldin |   noise_pct |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|-------------------:|
| DBSCAN        |   4 |        0.28  |            0.718 |         3.2 |              0.484 |
| Agglomerative |   4 |        0.449 |            0.773 |         0   |              0.423 |
| Divisive      |   3 |        0.479 |            0.763 |         0   |              0.588 |

## poster_ScottBarry-2010
**Winner: DBSCAN**  -  DBSCAN wins: highest separation score (0.976 after a 2% noise discount), silhouette 0.524, Davies-Bouldin 0.584; Agglomerative scored 0.703 (silhouette 0.521, DB 0.664); Divisive scored 0.000 (silhouette 0.452, DB 0.730).

| method        |   k |   silhouette |   davies_bouldin |   noise_pct |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|-------------------:|
| DBSCAN        |   5 |        0.524 |            0.584 |         2.4 |              0.976 |
| Agglomerative |   5 |        0.521 |            0.664 |         0   |              0.703 |
| Divisive      |   5 |        0.452 |            0.73  |         0   |              0     |

## poster_SeanAlatorre
**Winner: DBSCAN**  -  DBSCAN wins: highest separation score (0.887 after a 11% noise discount), silhouette 0.583, Davies-Bouldin 0.462; Agglomerative scored 0.343 (silhouette 0.542, DB 0.568); Divisive scored 0.000 (silhouette 0.533, DB 0.671).

| method        |   k |   silhouette |   davies_bouldin |   noise_pct |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|-------------------:|
| DBSCAN        |   5 |        0.583 |            0.462 |        11.3 |              0.887 |
| Agglomerative |   3 |        0.542 |            0.568 |         0   |              0.343 |
| Divisive      |   5 |        0.533 |            0.671 |         0   |              0     |

## poster_bookcover
**Winner: Agglomerative**  -  Agglomerative wins: highest separation score (1.000), silhouette 0.473, Davies-Bouldin 0.749; DBSCAN scored 0.000 (silhouette 0.047, DB 1.302, 5% noise); Divisive scored 0.837 (silhouette 0.424, DB 0.865).

| method        |   k |   silhouette |   davies_bouldin |   noise_pct |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|-------------------:|
| DBSCAN        |   3 |        0.047 |            1.302 |           5 |              0     |
| Agglomerative |   5 |        0.473 |            0.749 |           0 |              1     |
| Divisive      |   5 |        0.424 |            0.865 |           0 |              0.837 |

## poster_nancy
**Winner: DBSCAN**  -  DBSCAN wins: highest separation score (0.758 after a 24% noise discount), silhouette 0.696, Davies-Bouldin 0.387; Agglomerative scored 0.337 (silhouette 0.588, DB 0.557); Divisive scored 0.000 (silhouette 0.534, DB 0.644).

| method        |   k |   silhouette |   davies_bouldin |   noise_pct |   separation_score |
|:--------------|----:|-------------:|-----------------:|------------:|-------------------:|
| DBSCAN        |   4 |        0.696 |            0.387 |        24.2 |              0.758 |
| Agglomerative |   4 |        0.588 |            0.557 |         0   |              0.337 |
| Divisive      |   4 |        0.534 |            0.644 |         0   |              0     |
