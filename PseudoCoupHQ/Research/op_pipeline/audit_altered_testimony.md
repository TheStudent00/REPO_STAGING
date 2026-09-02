# audit -- testimony altered by the `|` -> `/` substitution

Counts are per STORE FILE, never per operator spelling.

| store file | records | with diagnostic | records with a token-position `/` | ALTERED fields | GENUINE fields | UNDECIDABLE | no source |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| op_pipeline/op_units_asg_c.json | 396 | 120 | 0 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_asg_cpp.json | 504 | 180 | 0 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_asg_go.json | 432 | 373 | 64 | 33 | 31 | 0 | 0 |
| op_pipeline/op_units_asg_rust.json | 396 | 335 | 32 | 26 | 6 | 0 | 0 |
| op_pipeline/op_units_asg_swift.json | 216 | 187 | 6 | 0 | 6 | 0 | 0 |
| op_pipeline/op_units_c.json | 750 | 140 | 0 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_cpp.json | 1002 | 232 | 0 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_cpython.json | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_cpython2.json | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_cpython2_reextracted.json | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_cpython_reextracted.json | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_csharp.json | 253 | 0 | 0 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_dart.json | 82 | 0 | 0 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_go.json | 744 | 637 | 99 | 68 | 31 | 0 | 0 |
| op_pipeline/op_units_java.json | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_java2.json | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_javascript.json | 291 | 0 | 0 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_php.json | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_ruby.json | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_rust.json | 858 | 733 | 32 | 32 | 0 | 0 | 0 |
| op_pipeline/op_units_swift.json | 1086 | 919 | 14 | 9 | 5 | 0 | 0 |
| stage_asg/op_units_c.json | 1146 | 260 | 0 | 0 | 0 | 0 | 0 |
| stage_asg/op_units_cpp.json | 1506 | 412 | 0 | 0 | 0 | 0 | 0 |
| stage_asg/op_units_go.json | 1176 | 1010 | 163 | 101 | 62 | 0 | 0 |
| stage_asg/op_units_rust.json | 1254 | 1068 | 64 | 58 | 6 | 0 | 0 |
| stage_asg/op_units_swift.json | 1302 | 1106 | 20 | 9 | 11 | 0 | 0 |
| **total** | 13412 | 7712 | 494 | 336 | 158 | 0 | 0 |

DWARF attribute fields examined: 20020; records where a DWARF field carries a comma (the `;` -> `,` substitution's weak fingerprint): 0.

## the first ten ALTERED fields, stored vs suspected

| store file | record | field | stored | suspected original |
| --- | ---: | --- | --- | --- |
| op_pipeline/op_units_asg_go.json | 325 | refused | `./main.go:6:2: invalid operation: a /= b (mismatched types int32 and int64)` | `./main.go:6:2: invalid operation: a \|= b (mismatched types int32 and int64)` |
| op_pipeline/op_units_asg_go.json | 326 | refused | `./main.go:6:2: invalid operation: a /= b (mismatched types int32 and uint64)` | `./main.go:6:2: invalid operation: a \|= b (mismatched types int32 and uint64)` |
| op_pipeline/op_units_asg_go.json | 327 | refused | `./main.go:6:2: invalid operation: a /= b (mismatched types int32 and float32)` | `./main.go:6:2: invalid operation: a \|= b (mismatched types int32 and float32)` |
| op_pipeline/op_units_asg_go.json | 328 | refused | `./main.go:6:2: invalid operation: a /= b (mismatched types int32 and float64)` | `./main.go:6:2: invalid operation: a \|= b (mismatched types int32 and float64)` |
| op_pipeline/op_units_asg_go.json | 329 | refused | `./main.go:6:2: invalid operation: a /= b (mismatched types int32 and bool)` | `./main.go:6:2: invalid operation: a \|= b (mismatched types int32 and bool)` |
| op_pipeline/op_units_asg_go.json | 330 | refused | `./main.go:6:2: invalid operation: a /= b (mismatched types int64 and int32)` | `./main.go:6:2: invalid operation: a \|= b (mismatched types int64 and int32)` |
| op_pipeline/op_units_asg_go.json | 332 | refused | `./main.go:6:2: invalid operation: a /= b (mismatched types int64 and uint64)` | `./main.go:6:2: invalid operation: a \|= b (mismatched types int64 and uint64)` |
| op_pipeline/op_units_asg_go.json | 333 | refused | `./main.go:6:2: invalid operation: a /= b (mismatched types int64 and float32)` | `./main.go:6:2: invalid operation: a \|= b (mismatched types int64 and float32)` |
| op_pipeline/op_units_asg_go.json | 334 | refused | `./main.go:6:2: invalid operation: a /= b (mismatched types int64 and float64)` | `./main.go:6:2: invalid operation: a \|= b (mismatched types int64 and float64)` |
| op_pipeline/op_units_asg_go.json | 335 | refused | `./main.go:6:2: invalid operation: a /= b (mismatched types int64 and bool)` | `./main.go:6:2: invalid operation: a \|= b (mismatched types int64 and bool)` |
