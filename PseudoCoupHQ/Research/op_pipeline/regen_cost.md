# regeneration cost, measured from the lane runs that already happened

Nothing was compiled to produce this page. Every runtime is the Airlock daemon's own footer line.

## the measured lanes

| language | lane | probes | accepted | refused | measured |
|---|---|---:|---:|---:|---:|
| c | `op_c.sh` | 750 | 610 | 140 | 42.4s |
| c | `op_asg_c.sh` | 396 | 276 | 120 | 12.0s |
| cpp | `op_cpp.sh` | 1002 | 770 | 232 | 74.1s |
| cpp | `op_asg_cpp.sh` | 504 | 324 | 180 | 27.4s |
| go | `op_go.sh` | 744 | 107 | 637 | 48.5s |
| go | `op_asg_go.sh` | 432 | 59 | 373 | 23.0s |
| rust | `op_rust.sh` | 858 | 125 | 733 | 24.1s |
| rust | `op_asg_rust.sh` | 396 | 61 | 335 | 8.9s |
| swift | `op_swift.sh` | 1086 | 167 | 919 | 159.8s |
| swift | `op_asg_swift.sh` | 216 | 29 | 187 | 31.1s |

## the two rates, solved per language

| language | refused probe | accepted probe | rate used | residue | serial |
|---|---:|---:|---:|---:|---:|
| c | -0.1268s | 0.0986s | 0.0475s | 51829 | 2460s |
| cpp | -0.0459s | 0.1101s | 0.0674s | 70991 | 4785s |
| go | -0.1720s | 1.4774s | 0.0608s | 553 | 34s |
| rust | 0.1260s | -0.5461s | 0.0263s | 1993 | 52s |
| swift | 0.1222s | 0.2843s | 0.2843s | 4187 | 1190s |
| **total** | | | | **129553** | **8522s** |

## where the two-rate solve failed, and what was used instead

The two lanes are not only two mixes: the assignment lane compiles a DIFFERENT PROBE SHAPE, so its per-probe cost differs for reasons the accepted/refused split does not carry. Where that shows up, the solve returns a negative rate, and a negative rate is refused rather than clamped.

- **c** -- the solved split has a negative rate, which means the two lanes' totals are not explained by the accepted/refused mix alone; the blended rate is used instead and the solved pair is kept for the record. Rate used: 0.0475s (blended).
- **cpp** -- the solved split has a negative rate, which means the two lanes' totals are not explained by the accepted/refused mix alone; the blended rate is used instead and the solved pair is kept for the record. Rate used: 0.0674s (blended).
- **go** -- the solved split has a negative rate, which means the two lanes' totals are not explained by the accepted/refused mix alone; the blended rate is used instead and the solved pair is kept for the record. Rate used: 0.0608s (blended).
- **rust** -- the solved split has a negative rate, which means the two lanes' totals are not explained by the accepted/refused mix alone; the blended rate is used instead and the solved pair is kept for the record. Rate used: 0.0263s (blended).
- **swift** -- solved cleanly; the accepted rate 0.2843s is used.

## the answer

- serial, one probe at a time: **8522 s = 2.37 hours**
- CPU time: the same 8522 s -- the work does not change when it is spread.
- at the cap (6 of 12 cores, 6 workers, 0.8 efficiency assumed): **0.49 hours** wall clock.

