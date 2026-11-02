# Fixed-point timing samples

These are single calls. They are not the production grid. The serial estimates multiply the measured wall time by 10,848 calls. Kinematic variation is not measured.

The continuous benchmark is `cross_section` at `x = 0.2`, `y = 0.5`, `z = 0.4`, `P_T² = 0.09`, `φ_h = 0`. It is not an analysis-bin index.

| Call | Wall time | Result | Compared with |
| --- | --- | --- | --- |
| SF 0 continuous | 0.98 s | RC 0.9155114884432165 | documented SF 0 value, matched |
| SF 2 continuous | 6.18 s | RC 0.916582037287526 | documented SF 2 value, matched |
| `correct.py -m RC -q 1 -z 1 -p 1 -s 0` | 1.08 s | RC 0.9468221137573274 at Q² 2.2, y 0.7, z 0.555, p_T 0.135, φ_h 7.5° | not the continuous benchmark |
| `correct.py -m RC -q 1 -z 1 -p 1 -s 2` | 6.36 s | RC 0.9378642490724497 at the same analysis-bin center | A_ep spline, Γ omitted; not the continuous benchmark |
| `correct.py -m BC -q 1 -z 1 -p 1` | 0.29 s | BC 0.962648406941639, 405 sub-bins, center 203 | raw-amplitude spline, not an RC |

Bin 1 edges are ΔQ² 0.4, Δy 0.1, Δz 0.31, and ΔP_T 0.17.

Serial estimate at one process: SF 0 about 3.3 h, SF 2 about 19.2 h, BC about 0.9 h. The two RC grids together are about 22.4 h. Each saved JSON is a few kilobytes, so the full cache is on the order of 100 MB.

## SF 2 concurrency benchmark

Eight retained bins, the same list at every worker count, each count in its own directory. Every `cross_section` process had one thread. No run added a swapout. Memory free percentage stayed near 47–48. Peak resident set for five processes was 117 MB.

| Workers | Elapsed | Throughput | Mean job | Peak CPU | Peak RSS | Swapout delta | Full-grid estimate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 49.14 s | 0.163 /s | 6.14 s | 100% | 31 MB | 0 | 18.5 h |
| 2 | 25.45 s | 0.314 /s | 6.36 s | 200% | 63 MB | 0 | 9.6 h |
| 3 | 19.51 s | 0.410 /s | 6.51 s | 300% | 63 MB | 0 | 7.3 h |
| 4 | 13.55 s | 0.590 /s | 6.75 s | 400% | 110 MB | 0 | 5.1 h |
| 5 | 14.18 s | 0.564 /s | 7.24 s | 498% | 117 MB | 0 | 5.3 h |

Five workers were slower than four. The recommendation is 4. The workflow argument is `rc_sf2_workers`, and that is the default. SF 0 and spline BC stay at one process. These full-grid times are `10848 / throughput` from the eight bins, not a measured 10,848-point run. The grid was not started.
