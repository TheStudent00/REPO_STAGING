# verdicts4 -- the relations as columns over core+modes

Every unit is a CORE (the normal-path lifted form) and a list of MODES (condition, response, detection).  The relation between two units is not decided by a cascade; it is read off the two records.

- `total equality` -- the cores are equal and the mode sets are equal.
- `core equality, modes differ` -- the cores are equal and the mode sets are not.  The modes one side has and the other has not are printed as data.  That list is the fence.
- `core difference` -- the cores are not equal.

Rows are verdicts3's machine-form groups, imported.  A row is never named by an operator token; each member carries its token as a display label.

- units considered: 1758
- distinct unit pairs: 4694
- column tally: {'total equality': 1192, 'core equality, modes differ': 66, 'core difference': 3436}
- mode responses: {'continue-with-a-different-answer': 186, 'wrap-continue': 36, 'panic-call': 28, 'clamp-continue': 18, 'trap': 31}
- units: {'units with 0 modes': 1510, 'units with 1+ modes': 248}
- lifter: pyvex 9.2.213 / archinfo 9.2.213 / libVEX via ArchAMD64

## the fences, gathered

| left | right | mode | condition | response | detection |
| --- | --- | --- | --- | --- | --- |
| c/op_47 | cpp/op_5 | on the right | in0 >= 64 (unsigned) | continue-with-a-different-answer | solver-localized |
| c/op_47 | cpp/op_29 | on the right | in0 >= 64 (unsigned) | continue-with-a-different-answer | solver-localized |
| c/op_47 | rust/op_17 | on the right | in0 >= 64 (unsigned) | continue-with-a-different-answer | solver-localized |
| c/op_47 | swift/op_29 | on the right | in0 >= 64 (unsigned) | continue-with-a-different-answer | solver-localized |
| c/op_12 | swift/op_12 | on the left | 0 - in0 overflows 32 bits (signed) | wrap-continue | branch-to-response |
| c/op_12 | swift/op_12 | on the right | 0 - in0 overflows 32 bits (signed) | trap | branch-to-response |
| cpp/op_12 | swift/op_12 | on the left | 0 - in0 overflows 32 bits (signed) | wrap-continue | branch-to-response |
| cpp/op_12 | swift/op_12 | on the right | 0 - in0 overflows 32 bits (signed) | trap | branch-to-response |
| go/op_6 | swift/op_12 | on the left | 0 - in0 overflows 32 bits (signed) | wrap-continue | branch-to-response |
| go/op_6 | swift/op_12 | on the right | 0 - in0 overflows 32 bits (signed) | trap | branch-to-response |
| rust/op_0 | swift/op_12 | on the left | 0 - in0 overflows 32 bits (signed) | wrap-continue | branch-to-response |
| rust/op_0 | swift/op_12 | on the right | 0 - in0 overflows 32 bits (signed) | trap | branch-to-response |
| c/op_210 | rust/op_642 | on the right | ((-2147483648 + in0) / ~in1) == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow | branch-to-response |
| c/op_210 | rust/op_642 | on the right | in1 == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero | branch-to-response |
| c/op_246 | rust/op_678 | on the right | ((-2147483648 + in0) / ~in1) == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow | branch-to-response |
| c/op_246 | rust/op_678 | on the right | in1 == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero | branch-to-response |
| c/op_210 | swift/op_150 | on the right | in1 == -1 | trap | branch-to-response |
| c/op_210 | swift/op_150 | on the right | in1 == 0 | trap | branch-to-response |
| c/op_246 | swift/op_186 | on the right | in1 == -1 | trap | branch-to-response |
| c/op_246 | swift/op_186 | on the right | in1 == 0 | trap | branch-to-response |
| cpp/op_210 | rust/op_642 | on the right | ((-2147483648 + in0) / ~in1) == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow | branch-to-response |
| cpp/op_210 | rust/op_642 | on the right | in1 == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero | branch-to-response |
| cpp/op_246 | rust/op_678 | on the right | ((-2147483648 + in0) / ~in1) == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow | branch-to-response |
| cpp/op_246 | rust/op_678 | on the right | in1 == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero | branch-to-response |
| cpp/op_210 | swift/op_150 | on the right | in1 == -1 | trap | branch-to-response |
| cpp/op_210 | swift/op_150 | on the right | in1 == 0 | trap | branch-to-response |
| cpp/op_246 | swift/op_186 | on the right | in1 == -1 | trap | branch-to-response |
| cpp/op_246 | swift/op_186 | on the right | in1 == 0 | trap | branch-to-response |
| rust/op_642 | swift/op_150 | on the left | ((-2147483648 + in0) / ~in1) == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow | branch-to-response |
| rust/op_642 | swift/op_150 | on the left | in1 == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero | branch-to-response |
| rust/op_642 | swift/op_150 | on the right | in1 == -1 | trap | branch-to-response |
| rust/op_642 | swift/op_150 | on the right | in1 == 0 | trap | branch-to-response |
| rust/op_678 | swift/op_186 | on the left | ((-2147483648 + in0) / ~in1) == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow | branch-to-response |
| rust/op_678 | swift/op_186 | on the left | in1 == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero | branch-to-response |
| rust/op_678 | swift/op_186 | on the right | in1 == -1 | trap | branch-to-response |
| rust/op_678 | swift/op_186 | on the right | in1 == 0 | trap | branch-to-response |
| c/op_102 | swift/op_222 | on the left | in0 + in1 overflows 32 bits (signed) | wrap-continue | branch-to-response |
| c/op_102 | swift/op_222 | on the right | in0 + in1 overflows 32 bits (signed) | trap | branch-to-response |
| cpp/op_102 | swift/op_222 | on the left | in0 + in1 overflows 32 bits (signed) | wrap-continue | branch-to-response |
| cpp/op_102 | swift/op_222 | on the right | in0 + in1 overflows 32 bits (signed) | trap | branch-to-response |
| go/op_312 | swift/op_222 | on the left | in0 + in1 overflows 32 bits (signed) | wrap-continue | branch-to-response |
| go/op_312 | swift/op_222 | on the right | in0 + in1 overflows 32 bits (signed) | trap | branch-to-response |
| rust/op_534 | swift/op_222 | on the left | in0 + in1 overflows 32 bits (signed) | wrap-continue | branch-to-response |
| rust/op_534 | swift/op_222 | on the right | in0 + in1 overflows 32 bits (signed) | trap | branch-to-response |
| c/op_138 | swift/op_258 | on the left | in0 - in1 overflows 32 bits (signed) | wrap-continue | branch-to-response |
| c/op_138 | swift/op_258 | on the right | in0 - in1 overflows 32 bits (signed) | trap | branch-to-response |
| cpp/op_138 | swift/op_258 | on the left | in0 - in1 overflows 32 bits (signed) | wrap-continue | branch-to-response |
| cpp/op_138 | swift/op_258 | on the right | in0 - in1 overflows 32 bits (signed) | trap | branch-to-response |
| go/op_348 | swift/op_258 | on the left | in0 - in1 overflows 32 bits (signed) | wrap-continue | branch-to-response |
| go/op_348 | swift/op_258 | on the right | in0 - in1 overflows 32 bits (signed) | trap | branch-to-response |
| rust/op_570 | swift/op_258 | on the left | in0 - in1 overflows 32 bits (signed) | wrap-continue | branch-to-response |
| rust/op_570 | swift/op_258 | on the right | in0 - in1 overflows 32 bits (signed) | trap | branch-to-response |
| c/op_174 | swift/op_114 | on the left | in1 * in0 overflows 32 bits (signed) | wrap-continue | branch-to-response |
| c/op_174 | swift/op_114 | on the right | in1 * in0 overflows 32 bits (signed) | trap | branch-to-response |
| cpp/op_174 | swift/op_114 | on the left | in1 * in0 overflows 32 bits (signed) | wrap-continue | branch-to-response |
| cpp/op_174 | swift/op_114 | on the right | in1 * in0 overflows 32 bits (signed) | trap | branch-to-response |
| go/op_60 | swift/op_114 | on the left | in1 * in0 overflows 32 bits (signed) | wrap-continue | branch-to-response |
| go/op_60 | swift/op_114 | on the right | in1 * in0 overflows 32 bits (signed) | trap | branch-to-response |
| rust/op_606 | swift/op_114 | on the left | in1 * in0 overflows 32 bits (signed) | wrap-continue | branch-to-response |
| rust/op_606 | swift/op_114 | on the right | in1 * in0 overflows 32 bits (signed) | trap | branch-to-response |
| c/op_13 | swift/op_13 | on the left | 0 - in0 overflows 64 bits (signed) | wrap-continue | branch-to-response |
| c/op_13 | swift/op_13 | on the right | 0 - in0 overflows 64 bits (signed) | trap | branch-to-response |
| cpp/op_13 | swift/op_13 | on the left | 0 - in0 overflows 64 bits (signed) | wrap-continue | branch-to-response |
| cpp/op_13 | swift/op_13 | on the right | 0 - in0 overflows 64 bits (signed) | trap | branch-to-response |
| go/op_7 | swift/op_13 | on the left | 0 - in0 overflows 64 bits (signed) | wrap-continue | branch-to-response |
| go/op_7 | swift/op_13 | on the right | 0 - in0 overflows 64 bits (signed) | trap | branch-to-response |
| rust/op_1 | swift/op_13 | on the left | 0 - in0 overflows 64 bits (signed) | wrap-continue | branch-to-response |
| rust/op_1 | swift/op_13 | on the right | 0 - in0 overflows 64 bits (signed) | trap | branch-to-response |
| c/op_217 | rust/op_649 | on the right | (~in1 / (-9223372036854775808 ^ in0)) == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow | branch-to-response |
| c/op_217 | rust/op_649 | on the right | in1 == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero | branch-to-response |
| c/op_253 | rust/op_685 | on the right | (~in1 / (-9223372036854775808 ^ in0)) == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow | branch-to-response |
| c/op_253 | rust/op_685 | on the right | in1 == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero | branch-to-response |
| cpp/op_217 | rust/op_649 | on the right | (~in1 / (-9223372036854775808 ^ in0)) == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow | branch-to-response |
| cpp/op_217 | rust/op_649 | on the right | in1 == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero | branch-to-response |
| cpp/op_253 | rust/op_685 | on the right | (~in1 / (-9223372036854775808 ^ in0)) == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow | branch-to-response |
| cpp/op_253 | rust/op_685 | on the right | in1 == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero | branch-to-response |
| c/op_109 | swift/op_229 | on the left | in0 + in1 overflows 64 bits (signed) | wrap-continue | branch-to-response |
| c/op_109 | swift/op_229 | on the right | in0 + in1 overflows 64 bits (signed) | trap | branch-to-response |
| cpp/op_109 | swift/op_229 | on the left | in0 + in1 overflows 64 bits (signed) | wrap-continue | branch-to-response |
| cpp/op_109 | swift/op_229 | on the right | in0 + in1 overflows 64 bits (signed) | trap | branch-to-response |
| go/op_319 | swift/op_229 | on the left | in0 + in1 overflows 64 bits (signed) | wrap-continue | branch-to-response |
| go/op_319 | swift/op_229 | on the right | in0 + in1 overflows 64 bits (signed) | trap | branch-to-response |
| rust/op_541 | swift/op_229 | on the left | in0 + in1 overflows 64 bits (signed) | wrap-continue | branch-to-response |
| rust/op_541 | swift/op_229 | on the right | in0 + in1 overflows 64 bits (signed) | trap | branch-to-response |
| c/op_145 | swift/op_265 | on the left | in0 - in1 overflows 64 bits (signed) | wrap-continue | branch-to-response |
| c/op_145 | swift/op_265 | on the right | in0 - in1 overflows 64 bits (signed) | trap | branch-to-response |
| cpp/op_145 | swift/op_265 | on the left | in0 - in1 overflows 64 bits (signed) | wrap-continue | branch-to-response |
| cpp/op_145 | swift/op_265 | on the right | in0 - in1 overflows 64 bits (signed) | trap | branch-to-response |
| go/op_355 | swift/op_265 | on the left | in0 - in1 overflows 64 bits (signed) | wrap-continue | branch-to-response |
| go/op_355 | swift/op_265 | on the right | in0 - in1 overflows 64 bits (signed) | trap | branch-to-response |
| rust/op_577 | swift/op_265 | on the left | in0 - in1 overflows 64 bits (signed) | wrap-continue | branch-to-response |
| rust/op_577 | swift/op_265 | on the right | in0 - in1 overflows 64 bits (signed) | trap | branch-to-response |
| c/op_181 | swift/op_121 | on the left | in1 * in0 overflows 64 bits (signed) | wrap-continue | branch-to-response |
| c/op_181 | swift/op_121 | on the right | in1 * in0 overflows 64 bits (signed) | trap | branch-to-response |
| cpp/op_181 | swift/op_121 | on the left | in1 * in0 overflows 64 bits (signed) | wrap-continue | branch-to-response |
| cpp/op_181 | swift/op_121 | on the right | in1 * in0 overflows 64 bits (signed) | trap | branch-to-response |
| go/op_67 | swift/op_121 | on the left | in1 * in0 overflows 64 bits (signed) | wrap-continue | branch-to-response |
| go/op_67 | swift/op_121 | on the right | in1 * in0 overflows 64 bits (signed) | trap | branch-to-response |
| rust/op_613 | swift/op_121 | on the left | in1 * in0 overflows 64 bits (signed) | wrap-continue | branch-to-response |
| rust/op_613 | swift/op_121 | on the right | in1 * in0 overflows 64 bits (signed) | trap | branch-to-response |
| c/op_224 | go/op_110 | on the right | in1 == 0 | panic-call:runtime.panicdivide | branch-to-response |
| c/op_260 | go/op_146 | on the right | in1 == 0 | panic-call:runtime.panicdivide | branch-to-response |
| c/op_224 | rust/op_656 | on the right | in1 == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero | branch-to-response |
| c/op_260 | rust/op_692 | on the right | in1 == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero | branch-to-response |
| cpp/op_224 | go/op_110 | on the right | in1 == 0 | panic-call:runtime.panicdivide | branch-to-response |
| cpp/op_260 | go/op_146 | on the right | in1 == 0 | panic-call:runtime.panicdivide | branch-to-response |
| cpp/op_224 | rust/op_656 | on the right | in1 == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero | branch-to-response |
| cpp/op_260 | rust/op_692 | on the right | in1 == 0 | panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero | branch-to-response |
| c/op_116 | swift/op_236 | on the left | in0 + in1 carries out of 64 bits (unsigned) | wrap-continue | branch-to-response |
| c/op_116 | swift/op_236 | on the right | in0 + in1 carries out of 64 bits (unsigned) | trap | branch-to-response |
| cpp/op_116 | swift/op_236 | on the left | in0 + in1 carries out of 64 bits (unsigned) | wrap-continue | branch-to-response |
| cpp/op_116 | swift/op_236 | on the right | in0 + in1 carries out of 64 bits (unsigned) | trap | branch-to-response |
| go/op_326 | swift/op_236 | on the left | in0 + in1 carries out of 64 bits (unsigned) | wrap-continue | branch-to-response |
| go/op_326 | swift/op_236 | on the right | in0 + in1 carries out of 64 bits (unsigned) | trap | branch-to-response |
| rust/op_548 | swift/op_236 | on the left | in0 + in1 carries out of 64 bits (unsigned) | wrap-continue | branch-to-response |
| rust/op_548 | swift/op_236 | on the right | in0 + in1 carries out of 64 bits (unsigned) | trap | branch-to-response |
| c/op_152 | swift/op_272 | on the right | in0 < in1 (unsigned) | trap | branch-to-response |
| cpp/op_152 | swift/op_272 | on the right | in0 < in1 (unsigned) | trap | branch-to-response |
| go/op_362 | swift/op_272 | on the right | in0 < in1 (unsigned) | trap | branch-to-response |
| rust/op_584 | swift/op_272 | on the right | in0 < in1 (unsigned) | trap | branch-to-response |

## rows

### byte-identical group [c3] · (f32,None)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `+` (f32,None, 0 modes); c `__extension__` (f32,None, 0 modes); c `++` (f32,None, 0 modes); c `--` (f32,None, 0 modes); cpp `+` (f32,None, 0 modes); cpp `++` (f32,None, 0 modes); cpp `--` (f32,None, 0 modes); go `+` (f32,None, 0 modes); rust `..` (f32,None, 0 modes); rust `..=` (f32,None, 0 modes); swift `+` (f32,None, 0 modes)

  - c/op_21 / cpp/op_21 -- **total equality**
  - c/op_21 / cpp/op_87 -- **total equality**
  - c/op_21 / cpp/op_93 -- **total equality**
  - c/op_87 / cpp/op_21 -- **total equality**
  - c/op_87 / cpp/op_87 -- **total equality**
  - c/op_87 / cpp/op_93 -- **total equality**
  - c/op_93 / cpp/op_21 -- **total equality**
  - c/op_93 / cpp/op_87 -- **total equality**
  - c/op_93 / cpp/op_93 -- **total equality**
  - c/op_99 / cpp/op_21 -- **total equality**
  - c/op_99 / cpp/op_87 -- **total equality**
  - c/op_99 / cpp/op_93 -- **total equality**
  - c/op_21 / go/op_3 -- **total equality**
  - c/op_87 / go/op_3 -- **total equality**
  - c/op_93 / go/op_3 -- **total equality**
  - c/op_99 / go/op_3 -- **total equality**
  - c/op_21 / rust/op_39 -- **total equality**
  - c/op_21 / rust/op_45 -- **total equality**
  - c/op_87 / rust/op_39 -- **total equality**
  - c/op_87 / rust/op_45 -- **total equality**
  - c/op_93 / rust/op_39 -- **total equality**
  - c/op_93 / rust/op_45 -- **total equality**
  - c/op_99 / rust/op_39 -- **total equality**
  - c/op_99 / rust/op_45 -- **total equality**
  - c/op_21 / swift/op_21 -- **total equality**
  - c/op_87 / swift/op_21 -- **total equality**
  - c/op_93 / swift/op_21 -- **total equality**
  - c/op_99 / swift/op_21 -- **total equality**
  - cpp/op_21 / go/op_3 -- **total equality**
  - cpp/op_87 / go/op_3 -- **total equality**
  - cpp/op_93 / go/op_3 -- **total equality**
  - cpp/op_21 / rust/op_39 -- **total equality**
  - cpp/op_21 / rust/op_45 -- **total equality**
  - cpp/op_87 / rust/op_39 -- **total equality**
  - cpp/op_87 / rust/op_45 -- **total equality**
  - cpp/op_93 / rust/op_39 -- **total equality**
  - cpp/op_93 / rust/op_45 -- **total equality**
  - cpp/op_21 / swift/op_21 -- **total equality**
  - cpp/op_87 / swift/op_21 -- **total equality**
  - cpp/op_93 / swift/op_21 -- **total equality**
  - go/op_3 / rust/op_39 -- **total equality**
  - go/op_3 / rust/op_45 -- **total equality**
  - go/op_3 / swift/op_21 -- **total equality**
  - rust/op_39 / swift/op_21 -- **total equality**
  - rust/op_45 / swift/op_21 -- **total equality**

### byte-identical group [c3] · (f32,f32)

- ground: cluster
- languages: rust, swift
- members: rust `..` (f32,f32, 0 modes); swift `??` (f32,f32, 0 modes)

  - rust/op_735 / swift/op_855 -- **total equality**

### byte-identical group [c3] · (f64,None)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `+` (f64,None, 0 modes); c `__extension__` (f64,None, 0 modes); c `++` (f64,None, 0 modes); c `--` (f64,None, 0 modes); cpp `+` (f64,None, 0 modes); cpp `++` (f64,None, 0 modes); cpp `--` (f64,None, 0 modes); go `+` (f64,None, 0 modes); rust `..` (f64,None, 0 modes); rust `..=` (f64,None, 0 modes); swift `+` (f64,None, 0 modes)

  - c/op_22 / cpp/op_22 -- **total equality**
  - c/op_22 / cpp/op_88 -- **total equality**
  - c/op_22 / cpp/op_94 -- **total equality**
  - c/op_88 / cpp/op_22 -- **total equality**
  - c/op_88 / cpp/op_88 -- **total equality**
  - c/op_88 / cpp/op_94 -- **total equality**
  - c/op_94 / cpp/op_22 -- **total equality**
  - c/op_94 / cpp/op_88 -- **total equality**
  - c/op_94 / cpp/op_94 -- **total equality**
  - c/op_100 / cpp/op_22 -- **total equality**
  - c/op_100 / cpp/op_88 -- **total equality**
  - c/op_100 / cpp/op_94 -- **total equality**
  - c/op_22 / go/op_4 -- **total equality**
  - c/op_88 / go/op_4 -- **total equality**
  - c/op_94 / go/op_4 -- **total equality**
  - c/op_100 / go/op_4 -- **total equality**
  - c/op_22 / rust/op_40 -- **total equality**
  - c/op_22 / rust/op_46 -- **total equality**
  - c/op_88 / rust/op_40 -- **total equality**
  - c/op_88 / rust/op_46 -- **total equality**
  - c/op_94 / rust/op_40 -- **total equality**
  - c/op_94 / rust/op_46 -- **total equality**
  - c/op_100 / rust/op_40 -- **total equality**
  - c/op_100 / rust/op_46 -- **total equality**
  - c/op_22 / swift/op_22 -- **total equality**
  - c/op_88 / swift/op_22 -- **total equality**
  - c/op_94 / swift/op_22 -- **total equality**
  - c/op_100 / swift/op_22 -- **total equality**
  - cpp/op_22 / go/op_4 -- **total equality**
  - cpp/op_88 / go/op_4 -- **total equality**
  - cpp/op_94 / go/op_4 -- **total equality**
  - cpp/op_22 / rust/op_40 -- **total equality**
  - cpp/op_22 / rust/op_46 -- **total equality**
  - cpp/op_88 / rust/op_40 -- **total equality**
  - cpp/op_88 / rust/op_46 -- **total equality**
  - cpp/op_94 / rust/op_40 -- **total equality**
  - cpp/op_94 / rust/op_46 -- **total equality**
  - cpp/op_22 / swift/op_22 -- **total equality**
  - cpp/op_88 / swift/op_22 -- **total equality**
  - cpp/op_94 / swift/op_22 -- **total equality**
  - go/op_4 / rust/op_40 -- **total equality**
  - go/op_4 / rust/op_46 -- **total equality**
  - go/op_4 / swift/op_22 -- **total equality**
  - rust/op_40 / swift/op_22 -- **total equality**
  - rust/op_46 / swift/op_22 -- **total equality**

### byte-identical group [c3] · (f64,f64)

- ground: cluster
- languages: rust, swift
- members: rust `..` (f64,f64, 0 modes); swift `??` (f64,f64, 0 modes)

  - rust/op_742 / swift/op_862 -- **total equality**

### byte-identical group [48 89 f8 c3] · (i64,None)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `+` (i64,None, 0 modes); c `__extension__` (i64,None, 0 modes); c `++` (i64,None, 0 modes); c `--` (i64,None, 0 modes); cpp `+` (i64,None, 0 modes); cpp `++` (i64,None, 0 modes); cpp `--` (i64,None, 0 modes); rust `..` (i64,None, 0 modes); rust `..=` (i64,None, 0 modes); swift `+` (i64,None, 0 modes)

  - c/op_19 / cpp/op_19 -- **total equality**
  - c/op_19 / cpp/op_85 -- **total equality**
  - c/op_19 / cpp/op_91 -- **total equality**
  - c/op_85 / cpp/op_19 -- **total equality**
  - c/op_85 / cpp/op_85 -- **total equality**
  - c/op_85 / cpp/op_91 -- **total equality**
  - c/op_91 / cpp/op_19 -- **total equality**
  - c/op_91 / cpp/op_85 -- **total equality**
  - c/op_91 / cpp/op_91 -- **total equality**
  - c/op_97 / cpp/op_19 -- **total equality**
  - c/op_97 / cpp/op_85 -- **total equality**
  - c/op_97 / cpp/op_91 -- **total equality**
  - c/op_19 / rust/op_37 -- **total equality**
  - c/op_19 / rust/op_43 -- **total equality**
  - c/op_85 / rust/op_37 -- **total equality**
  - c/op_85 / rust/op_43 -- **total equality**
  - c/op_91 / rust/op_37 -- **total equality**
  - c/op_91 / rust/op_43 -- **total equality**
  - c/op_97 / rust/op_37 -- **total equality**
  - c/op_97 / rust/op_43 -- **total equality**
  - c/op_19 / swift/op_19 -- **total equality**
  - c/op_85 / swift/op_19 -- **total equality**
  - c/op_91 / swift/op_19 -- **total equality**
  - c/op_97 / swift/op_19 -- **total equality**
  - cpp/op_19 / rust/op_37 -- **total equality**
  - cpp/op_19 / rust/op_43 -- **total equality**
  - cpp/op_85 / rust/op_37 -- **total equality**
  - cpp/op_85 / rust/op_43 -- **total equality**
  - cpp/op_91 / rust/op_37 -- **total equality**
  - cpp/op_91 / rust/op_43 -- **total equality**
  - cpp/op_19 / swift/op_19 -- **total equality**
  - cpp/op_85 / swift/op_19 -- **total equality**
  - cpp/op_91 / swift/op_19 -- **total equality**
  - rust/op_37 / swift/op_19 -- **total equality**
  - rust/op_43 / swift/op_19 -- **total equality**

### byte-identical group [48 89 f8 c3] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `/` (i64,bool, 0 modes); cpp `/` (i64,bool, 0 modes)

  - c/op_221 / cpp/op_221 -- **total equality**

### byte-identical group [48 89 f8 c3] · (u64,None)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `+` (u64,None, 0 modes); c `__extension__` (u64,None, 0 modes); c `++` (u64,None, 0 modes); c `--` (u64,None, 0 modes); cpp `+` (u64,None, 0 modes); cpp `++` (u64,None, 0 modes); cpp `--` (u64,None, 0 modes); rust `..` (u64,None, 0 modes); rust `..=` (u64,None, 0 modes); swift `+` (u64,None, 0 modes)

  - c/op_20 / cpp/op_20 -- **total equality**
  - c/op_20 / cpp/op_86 -- **total equality**
  - c/op_20 / cpp/op_92 -- **total equality**
  - c/op_86 / cpp/op_20 -- **total equality**
  - c/op_86 / cpp/op_86 -- **total equality**
  - c/op_86 / cpp/op_92 -- **total equality**
  - c/op_92 / cpp/op_20 -- **total equality**
  - c/op_92 / cpp/op_86 -- **total equality**
  - c/op_92 / cpp/op_92 -- **total equality**
  - c/op_98 / cpp/op_20 -- **total equality**
  - c/op_98 / cpp/op_86 -- **total equality**
  - c/op_98 / cpp/op_92 -- **total equality**
  - c/op_20 / rust/op_38 -- **total equality**
  - c/op_20 / rust/op_44 -- **total equality**
  - c/op_86 / rust/op_38 -- **total equality**
  - c/op_86 / rust/op_44 -- **total equality**
  - c/op_92 / rust/op_38 -- **total equality**
  - c/op_92 / rust/op_44 -- **total equality**
  - c/op_98 / rust/op_38 -- **total equality**
  - c/op_98 / rust/op_44 -- **total equality**
  - c/op_20 / swift/op_20 -- **total equality**
  - c/op_86 / swift/op_20 -- **total equality**
  - c/op_92 / swift/op_20 -- **total equality**
  - c/op_98 / swift/op_20 -- **total equality**
  - cpp/op_20 / rust/op_38 -- **total equality**
  - cpp/op_20 / rust/op_44 -- **total equality**
  - cpp/op_86 / rust/op_38 -- **total equality**
  - cpp/op_86 / rust/op_44 -- **total equality**
  - cpp/op_92 / rust/op_38 -- **total equality**
  - cpp/op_92 / rust/op_44 -- **total equality**
  - cpp/op_20 / swift/op_20 -- **total equality**
  - cpp/op_86 / swift/op_20 -- **total equality**
  - cpp/op_92 / swift/op_20 -- **total equality**
  - rust/op_38 / swift/op_20 -- **total equality**
  - rust/op_44 / swift/op_20 -- **total equality**

### byte-identical group [48 89 f8 c3] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `/` (u64,bool, 0 modes); cpp `/` (u64,bool, 0 modes)

  - c/op_227 / cpp/op_227 -- **total equality**

### byte-identical group [89 f8 c3] · (bool,None)

- ground: cluster
- languages: c, cpp, rust
- members: c `+` (bool,None, 0 modes); c `__extension__` (bool,None, 0 modes); c `++` (bool,None, 0 modes); c `--` (bool,None, 0 modes); cpp `+` (bool,None, 0 modes); rust `..` (bool,None, 0 modes); rust `..=` (bool,None, 0 modes)

  - c/op_23 / cpp/op_23 -- **total equality**
  - c/op_89 / cpp/op_23 -- **total equality**
  - c/op_95 / cpp/op_23 -- **total equality**
  - c/op_101 / cpp/op_23 -- **total equality**
  - c/op_23 / rust/op_41 -- **total equality**
  - c/op_23 / rust/op_47 -- **total equality**
  - c/op_89 / rust/op_41 -- **total equality**
  - c/op_89 / rust/op_47 -- **total equality**
  - c/op_95 / rust/op_41 -- **total equality**
  - c/op_95 / rust/op_47 -- **total equality**
  - c/op_101 / rust/op_41 -- **total equality**
  - c/op_101 / rust/op_47 -- **total equality**
  - cpp/op_23 / rust/op_41 -- **total equality**
  - cpp/op_23 / rust/op_47 -- **total equality**

### byte-identical group [89 f8 c3] · (bool,bool)

- ground: cluster
- languages: c, cpp, swift
- members: c `/` (bool,bool, 0 modes); cpp `/` (bool,bool, 0 modes); swift `??` (bool,bool, 0 modes)

  - c/op_245 / cpp/op_245 -- **total equality**
  - c/op_245 / swift/op_869 -- **total equality**
  - cpp/op_245 / swift/op_869 -- **total equality**

### byte-identical group [89 f8 c3] · (i32,None)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `+` (i32,None, 0 modes); c `__extension__` (i32,None, 0 modes); c `++` (i32,None, 0 modes); c `--` (i32,None, 0 modes); cpp `+` (i32,None, 0 modes); cpp `++` (i32,None, 0 modes); cpp `--` (i32,None, 0 modes); rust `..` (i32,None, 0 modes); rust `..=` (i32,None, 0 modes); swift `+` (i32,None, 0 modes)

  - c/op_18 / cpp/op_18 -- **total equality**
  - c/op_18 / cpp/op_84 -- **total equality**
  - c/op_18 / cpp/op_90 -- **total equality**
  - c/op_84 / cpp/op_18 -- **total equality**
  - c/op_84 / cpp/op_84 -- **total equality**
  - c/op_84 / cpp/op_90 -- **total equality**
  - c/op_90 / cpp/op_18 -- **total equality**
  - c/op_90 / cpp/op_84 -- **total equality**
  - c/op_90 / cpp/op_90 -- **total equality**
  - c/op_96 / cpp/op_18 -- **total equality**
  - c/op_96 / cpp/op_84 -- **total equality**
  - c/op_96 / cpp/op_90 -- **total equality**
  - c/op_18 / rust/op_36 -- **total equality**
  - c/op_18 / rust/op_42 -- **total equality**
  - c/op_84 / rust/op_36 -- **total equality**
  - c/op_84 / rust/op_42 -- **total equality**
  - c/op_90 / rust/op_36 -- **total equality**
  - c/op_90 / rust/op_42 -- **total equality**
  - c/op_96 / rust/op_36 -- **total equality**
  - c/op_96 / rust/op_42 -- **total equality**
  - c/op_18 / swift/op_18 -- **total equality**
  - c/op_84 / swift/op_18 -- **total equality**
  - c/op_90 / swift/op_18 -- **total equality**
  - c/op_96 / swift/op_18 -- **total equality**
  - cpp/op_18 / rust/op_36 -- **total equality**
  - cpp/op_18 / rust/op_42 -- **total equality**
  - cpp/op_84 / rust/op_36 -- **total equality**
  - cpp/op_84 / rust/op_42 -- **total equality**
  - cpp/op_90 / rust/op_36 -- **total equality**
  - cpp/op_90 / rust/op_42 -- **total equality**
  - cpp/op_18 / swift/op_18 -- **total equality**
  - cpp/op_84 / swift/op_18 -- **total equality**
  - cpp/op_90 / swift/op_18 -- **total equality**
  - rust/op_36 / swift/op_18 -- **total equality**
  - rust/op_42 / swift/op_18 -- **total equality**

### byte-identical group [89 f8 c3] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `/` (i32,bool, 0 modes); cpp `/` (i32,bool, 0 modes)

  - c/op_215 / cpp/op_215 -- **total equality**

### byte-identical group [89 f8 21 f0 c3] · (bool,bool)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `*` (bool,bool, 0 modes); c `&&` (bool,bool, 0 modes); c `&` (bool,bool, 0 modes); cpp `*` (bool,bool, 0 modes); cpp `&&` (bool,bool, 0 modes); cpp `&` (bool,bool, 0 modes); cpp `and` (bool,bool, 0 modes); cpp `bitand` (bool,bool, 0 modes); rust `&&` (bool,bool, 0 modes); rust `&` (bool,bool, 0 modes); swift `&&` (bool,bool, 0 modes)

  - c/op_209 / cpp/op_209 -- **total equality**
  - c/op_209 / cpp/op_353 -- **total equality**
  - c/op_209 / cpp/op_461 -- **total equality**
  - c/op_209 / cpp/op_857 -- **total equality**
  - c/op_209 / cpp/op_965 -- **total equality**
  - c/op_353 / cpp/op_209 -- **total equality**
  - c/op_353 / cpp/op_353 -- **total equality**
  - c/op_353 / cpp/op_461 -- **total equality**
  - c/op_353 / cpp/op_857 -- **total equality**
  - c/op_353 / cpp/op_965 -- **total equality**
  - c/op_461 / cpp/op_209 -- **total equality**
  - c/op_461 / cpp/op_353 -- **total equality**
  - c/op_461 / cpp/op_461 -- **total equality**
  - c/op_461 / cpp/op_857 -- **total equality**
  - c/op_461 / cpp/op_965 -- **total equality**
  - c/op_209 / rust/op_101 -- **total equality**
  - c/op_209 / rust/op_173 -- **total equality**
  - c/op_353 / rust/op_101 -- **total equality**
  - c/op_353 / rust/op_173 -- **total equality**
  - c/op_461 / rust/op_101 -- **total equality**
  - c/op_461 / rust/op_173 -- **total equality**
  - c/op_209 / swift/op_797 -- **total equality**
  - c/op_353 / swift/op_797 -- **total equality**
  - c/op_461 / swift/op_797 -- **total equality**
  - cpp/op_209 / rust/op_101 -- **total equality**
  - cpp/op_209 / rust/op_173 -- **total equality**
  - cpp/op_353 / rust/op_101 -- **total equality**
  - cpp/op_353 / rust/op_173 -- **total equality**
  - cpp/op_461 / rust/op_101 -- **total equality**
  - cpp/op_461 / rust/op_173 -- **total equality**
  - cpp/op_857 / rust/op_101 -- **total equality**
  - cpp/op_857 / rust/op_173 -- **total equality**
  - cpp/op_965 / rust/op_101 -- **total equality**
  - cpp/op_965 / rust/op_173 -- **total equality**
  - cpp/op_209 / swift/op_797 -- **total equality**
  - cpp/op_353 / swift/op_797 -- **total equality**
  - cpp/op_461 / swift/op_797 -- **total equality**
  - cpp/op_857 / swift/op_797 -- **total equality**
  - cpp/op_965 / swift/op_797 -- **total equality**
  - rust/op_101 / swift/op_797 -- **total equality**
  - rust/op_173 / swift/op_797 -- **total equality**

### byte-identical group [89 f8 21 f0 c3] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `&` (bool,i32, 0 modes); cpp `&` (bool,i32, 0 modes); cpp `bitand` (bool,i32, 0 modes)

  - c/op_456 / cpp/op_456 -- **total equality**
  - c/op_456 / cpp/op_960 -- **total equality**

### byte-identical group [89 f8 21 f0 c3] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `&` (i32,bool, 0 modes); cpp `&` (i32,bool, 0 modes); cpp `bitand` (i32,bool, 0 modes)

  - c/op_431 / cpp/op_431 -- **total equality**
  - c/op_431 / cpp/op_935 -- **total equality**

### byte-identical group [89 f8 21 f0 c3] · (i32,i32)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `&` (i32,i32, 0 modes); cpp `&` (i32,i32, 0 modes); cpp `bitand` (i32,i32, 0 modes); rust `&` (i32,i32, 0 modes); swift `&` (i32,i32, 0 modes)

  - c/op_426 / cpp/op_426 -- **total equality**
  - c/op_426 / cpp/op_930 -- **total equality**
  - c/op_426 / rust/op_138 -- **total equality**
  - c/op_426 / swift/op_582 -- **total equality**
  - cpp/op_426 / rust/op_138 -- **total equality**
  - cpp/op_930 / rust/op_138 -- **total equality**
  - cpp/op_426 / swift/op_582 -- **total equality**
  - cpp/op_930 / swift/op_582 -- **total equality**
  - rust/op_138 / swift/op_582 -- **total equality**

### byte-identical group [89 f8 09 f0 c3] · (bool,bool)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `||` (bool,bool, 0 modes); c `|` (bool,bool, 0 modes); cpp `||` (bool,bool, 0 modes); cpp `|` (bool,bool, 0 modes); cpp `or` (bool,bool, 0 modes); cpp `bitor` (bool,bool, 0 modes); rust `||` (bool,bool, 0 modes); rust `|` (bool,bool, 0 modes); swift `||` (bool,bool, 0 modes)

  - c/op_317 / cpp/op_317 -- **total equality**
  - c/op_317 / cpp/op_389 -- **total equality**
  - c/op_317 / cpp/op_821 -- **total equality**
  - c/op_317 / cpp/op_893 -- **total equality**
  - c/op_389 / cpp/op_317 -- **total equality**
  - c/op_389 / cpp/op_389 -- **total equality**
  - c/op_389 / cpp/op_821 -- **total equality**
  - c/op_389 / cpp/op_893 -- **total equality**
  - c/op_317 / rust/op_137 -- **total equality**
  - c/op_317 / rust/op_209 -- **total equality**
  - c/op_389 / rust/op_137 -- **total equality**
  - c/op_389 / rust/op_209 -- **total equality**
  - c/op_317 / swift/op_833 -- **total equality**
  - c/op_389 / swift/op_833 -- **total equality**
  - cpp/op_317 / rust/op_137 -- **total equality**
  - cpp/op_317 / rust/op_209 -- **total equality**
  - cpp/op_389 / rust/op_137 -- **total equality**
  - cpp/op_389 / rust/op_209 -- **total equality**
  - cpp/op_821 / rust/op_137 -- **total equality**
  - cpp/op_821 / rust/op_209 -- **total equality**
  - cpp/op_893 / rust/op_137 -- **total equality**
  - cpp/op_893 / rust/op_209 -- **total equality**
  - cpp/op_317 / swift/op_833 -- **total equality**
  - cpp/op_389 / swift/op_833 -- **total equality**
  - cpp/op_821 / swift/op_833 -- **total equality**
  - cpp/op_893 / swift/op_833 -- **total equality**
  - rust/op_137 / swift/op_833 -- **total equality**
  - rust/op_209 / swift/op_833 -- **total equality**

### byte-identical group [89 f8 09 f0 c3] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `|` (bool,i32, 0 modes); cpp `|` (bool,i32, 0 modes); cpp `bitor` (bool,i32, 0 modes)

  - c/op_384 / cpp/op_384 -- **total equality**
  - c/op_384 / cpp/op_888 -- **total equality**

### byte-identical group [89 f8 09 f0 c3] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `|` (i32,bool, 0 modes); cpp `|` (i32,bool, 0 modes); cpp `bitor` (i32,bool, 0 modes)

  - c/op_359 / cpp/op_359 -- **total equality**
  - c/op_359 / cpp/op_863 -- **total equality**

### byte-identical group [89 f8 09 f0 c3] · (i32,i32)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `|` (i32,i32, 0 modes); cpp `|` (i32,i32, 0 modes); cpp `bitor` (i32,i32, 0 modes); rust `|` (i32,i32, 0 modes); swift `|` (i32,i32, 0 modes)

  - c/op_354 / cpp/op_354 -- **total equality**
  - c/op_354 / cpp/op_858 -- **total equality**
  - c/op_354 / rust/op_174 -- **total equality**
  - c/op_354 / swift/op_618 -- **total equality**
  - cpp/op_354 / rust/op_174 -- **total equality**
  - cpp/op_858 / rust/op_174 -- **total equality**
  - cpp/op_354 / swift/op_618 -- **total equality**
  - cpp/op_858 / swift/op_618 -- **total equality**
  - rust/op_174 / swift/op_618 -- **total equality**

### byte-identical group [89 f8 31 f0 c3] · (bool,bool)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `^` (bool,bool, 0 modes); c `!=` (bool,bool, 0 modes); cpp `^` (bool,bool, 0 modes); cpp `!=` (bool,bool, 0 modes); cpp `xor` (bool,bool, 0 modes); cpp `not_eq` (bool,bool, 0 modes); rust `^` (bool,bool, 0 modes); rust `!=` (bool,bool, 0 modes); swift `!=` (bool,bool, 0 modes)

  - c/op_425 / cpp/op_425 -- **total equality**
  - c/op_425 / cpp/op_533 -- **total equality**
  - c/op_425 / cpp/op_929 -- **total equality**
  - c/op_425 / cpp/op_1001 -- **total equality**
  - c/op_533 / cpp/op_425 -- **total equality**
  - c/op_533 / cpp/op_533 -- **total equality**
  - c/op_533 / cpp/op_929 -- **total equality**
  - c/op_533 / cpp/op_1001 -- **total equality**
  - c/op_425 / rust/op_245 -- **total equality**
  - c/op_425 / rust/op_317 -- **total equality**
  - c/op_533 / rust/op_245 -- **total equality**
  - c/op_533 / rust/op_317 -- **total equality**
  - c/op_425 / swift/op_473 -- **total equality**
  - c/op_533 / swift/op_473 -- **total equality**
  - cpp/op_425 / rust/op_245 -- **total equality**
  - cpp/op_425 / rust/op_317 -- **total equality**
  - cpp/op_533 / rust/op_245 -- **total equality**
  - cpp/op_533 / rust/op_317 -- **total equality**
  - cpp/op_929 / rust/op_245 -- **total equality**
  - cpp/op_929 / rust/op_317 -- **total equality**
  - cpp/op_1001 / rust/op_245 -- **total equality**
  - cpp/op_1001 / rust/op_317 -- **total equality**
  - cpp/op_425 / swift/op_473 -- **total equality**
  - cpp/op_533 / swift/op_473 -- **total equality**
  - cpp/op_929 / swift/op_473 -- **total equality**
  - cpp/op_1001 / swift/op_473 -- **total equality**
  - rust/op_245 / swift/op_473 -- **total equality**
  - rust/op_317 / swift/op_473 -- **total equality**

### byte-identical group [89 f8 31 f0 c3] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `^` (bool,i32, 0 modes); cpp `^` (bool,i32, 0 modes); cpp `xor` (bool,i32, 0 modes)

  - c/op_420 / cpp/op_420 -- **total equality**
  - c/op_420 / cpp/op_924 -- **total equality**

### byte-identical group [89 f8 31 f0 c3] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `^` (i32,bool, 0 modes); cpp `^` (i32,bool, 0 modes); cpp `xor` (i32,bool, 0 modes)

  - c/op_395 / cpp/op_395 -- **total equality**
  - c/op_395 / cpp/op_899 -- **total equality**

### byte-identical group [89 f8 31 f0 c3] · (i32,i32)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `^` (i32,i32, 0 modes); cpp `^` (i32,i32, 0 modes); cpp `xor` (i32,i32, 0 modes); rust `^` (i32,i32, 0 modes); swift `^` (i32,i32, 0 modes)

  - c/op_390 / cpp/op_390 -- **total equality**
  - c/op_390 / cpp/op_894 -- **total equality**
  - c/op_390 / rust/op_210 -- **total equality**
  - c/op_390 / swift/op_654 -- **total equality**
  - cpp/op_390 / rust/op_210 -- **total equality**
  - cpp/op_894 / rust/op_210 -- **total equality**
  - cpp/op_390 / swift/op_654 -- **total equality**
  - cpp/op_894 / swift/op_654 -- **total equality**
  - rust/op_210 / swift/op_654 -- **total equality**

### byte-identical group [48 89 f8 48 09 f0 c3] · (i64,i64)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `|` (i64,i64, 0 modes); cpp `|` (i64,i64, 0 modes); cpp `bitor` (i64,i64, 0 modes); rust `|` (i64,i64, 0 modes); swift `|` (i64,i64, 0 modes)

  - c/op_361 / cpp/op_361 -- **total equality**
  - c/op_361 / cpp/op_865 -- **total equality**
  - c/op_361 / rust/op_181 -- **total equality**
  - c/op_361 / swift/op_625 -- **total equality**
  - cpp/op_361 / rust/op_181 -- **total equality**
  - cpp/op_865 / rust/op_181 -- **total equality**
  - cpp/op_361 / swift/op_625 -- **total equality**
  - cpp/op_865 / swift/op_625 -- **total equality**
  - rust/op_181 / swift/op_625 -- **total equality**

### byte-identical group [48 89 f8 48 09 f0 c3] · (i64,u64)

- ground: cluster
- languages: c, cpp
- members: c `|` (i64,u64, 0 modes); cpp `|` (i64,u64, 0 modes); cpp `bitor` (i64,u64, 0 modes)

  - c/op_362 / cpp/op_362 -- **total equality**
  - c/op_362 / cpp/op_866 -- **total equality**

### byte-identical group [48 89 f8 48 09 f0 c3] · (u64,i64)

- ground: cluster
- languages: c, cpp
- members: c `|` (u64,i64, 0 modes); cpp `|` (u64,i64, 0 modes); cpp `bitor` (u64,i64, 0 modes)

  - c/op_367 / cpp/op_367 -- **total equality**
  - c/op_367 / cpp/op_871 -- **total equality**

### byte-identical group [48 89 f8 48 09 f0 c3] · (u64,u64)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `|` (u64,u64, 0 modes); cpp `|` (u64,u64, 0 modes); cpp `bitor` (u64,u64, 0 modes); rust `|` (u64,u64, 0 modes); swift `|` (u64,u64, 0 modes)

  - c/op_368 / cpp/op_368 -- **total equality**
  - c/op_368 / cpp/op_872 -- **total equality**
  - c/op_368 / rust/op_188 -- **total equality**
  - c/op_368 / swift/op_632 -- **total equality**
  - cpp/op_368 / rust/op_188 -- **total equality**
  - cpp/op_872 / rust/op_188 -- **total equality**
  - cpp/op_368 / swift/op_632 -- **total equality**
  - cpp/op_872 / swift/op_632 -- **total equality**
  - rust/op_188 / swift/op_632 -- **total equality**

### byte-identical group [48 89 f8 48 21 f0 c3] · (i64,i64)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `&` (i64,i64, 0 modes); cpp `&` (i64,i64, 0 modes); cpp `bitand` (i64,i64, 0 modes); rust `&` (i64,i64, 0 modes); swift `&` (i64,i64, 0 modes)

  - c/op_433 / cpp/op_433 -- **total equality**
  - c/op_433 / cpp/op_937 -- **total equality**
  - c/op_433 / rust/op_145 -- **total equality**
  - c/op_433 / swift/op_589 -- **total equality**
  - cpp/op_433 / rust/op_145 -- **total equality**
  - cpp/op_937 / rust/op_145 -- **total equality**
  - cpp/op_433 / swift/op_589 -- **total equality**
  - cpp/op_937 / swift/op_589 -- **total equality**
  - rust/op_145 / swift/op_589 -- **total equality**

### byte-identical group [48 89 f8 48 21 f0 c3] · (i64,u64)

- ground: cluster
- languages: c, cpp
- members: c `&` (i64,u64, 0 modes); cpp `&` (i64,u64, 0 modes); cpp `bitand` (i64,u64, 0 modes)

  - c/op_434 / cpp/op_434 -- **total equality**
  - c/op_434 / cpp/op_938 -- **total equality**

### byte-identical group [48 89 f8 48 21 f0 c3] · (u64,i64)

- ground: cluster
- languages: c, cpp
- members: c `&` (u64,i64, 0 modes); cpp `&` (u64,i64, 0 modes); cpp `bitand` (u64,i64, 0 modes)

  - c/op_439 / cpp/op_439 -- **total equality**
  - c/op_439 / cpp/op_943 -- **total equality**

### byte-identical group [48 89 f8 48 21 f0 c3] · (u64,u64)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `&` (u64,u64, 0 modes); cpp `&` (u64,u64, 0 modes); cpp `bitand` (u64,u64, 0 modes); rust `&` (u64,u64, 0 modes); swift `&` (u64,u64, 0 modes)

  - c/op_440 / cpp/op_440 -- **total equality**
  - c/op_440 / cpp/op_944 -- **total equality**
  - c/op_440 / rust/op_152 -- **total equality**
  - c/op_440 / swift/op_596 -- **total equality**
  - cpp/op_440 / rust/op_152 -- **total equality**
  - cpp/op_944 / rust/op_152 -- **total equality**
  - cpp/op_440 / swift/op_596 -- **total equality**
  - cpp/op_944 / swift/op_596 -- **total equality**
  - rust/op_152 / swift/op_596 -- **total equality**

### byte-identical group [48 89 f8 48 31 f0 c3] · (i64,i64)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `^` (i64,i64, 0 modes); cpp `^` (i64,i64, 0 modes); cpp `xor` (i64,i64, 0 modes); rust `^` (i64,i64, 0 modes); swift `^` (i64,i64, 0 modes)

  - c/op_397 / cpp/op_397 -- **total equality**
  - c/op_397 / cpp/op_901 -- **total equality**
  - c/op_397 / rust/op_217 -- **total equality**
  - c/op_397 / swift/op_661 -- **total equality**
  - cpp/op_397 / rust/op_217 -- **total equality**
  - cpp/op_901 / rust/op_217 -- **total equality**
  - cpp/op_397 / swift/op_661 -- **total equality**
  - cpp/op_901 / swift/op_661 -- **total equality**
  - rust/op_217 / swift/op_661 -- **total equality**

### byte-identical group [48 89 f8 48 31 f0 c3] · (i64,u64)

- ground: cluster
- languages: c, cpp
- members: c `^` (i64,u64, 0 modes); cpp `^` (i64,u64, 0 modes); cpp `xor` (i64,u64, 0 modes)

  - c/op_398 / cpp/op_398 -- **total equality**
  - c/op_398 / cpp/op_902 -- **total equality**

### byte-identical group [48 89 f8 48 31 f0 c3] · (u64,i64)

- ground: cluster
- languages: c, cpp
- members: c `^` (u64,i64, 0 modes); cpp `^` (u64,i64, 0 modes); cpp `xor` (u64,i64, 0 modes)

  - c/op_403 / cpp/op_403 -- **total equality**
  - c/op_403 / cpp/op_907 -- **total equality**

### byte-identical group [48 89 f8 48 31 f0 c3] · (u64,u64)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `^` (u64,u64, 0 modes); cpp `^` (u64,u64, 0 modes); cpp `xor` (u64,u64, 0 modes); rust `^` (u64,u64, 0 modes); swift `^` (u64,u64, 0 modes)

  - c/op_404 / cpp/op_404 -- **total equality**
  - c/op_404 / cpp/op_908 -- **total equality**
  - c/op_404 / rust/op_224 -- **total equality**
  - c/op_404 / swift/op_668 -- **total equality**
  - cpp/op_404 / rust/op_224 -- **total equality**
  - cpp/op_908 / rust/op_224 -- **total equality**
  - cpp/op_404 / swift/op_668 -- **total equality**
  - cpp/op_908 / swift/op_668 -- **total equality**
  - rust/op_224 / swift/op_668 -- **total equality**

### byte-identical group [b8 08 00 00 00 c3] · (f64,None)

- ground: cluster
- languages: c, cpp
- members: c `sizeof` (f64,None, 0 modes); c `__alignof__` (f64,None, 0 modes); c `__alignof` (f64,None, 0 modes); c `_Alignof` (f64,None, 0 modes); cpp `sizeof` (f64,None, 0 modes)

  - c/op_52 / cpp/op_64 -- **total equality**
  - c/op_58 / cpp/op_64 -- **total equality**
  - c/op_64 / cpp/op_64 -- **total equality**
  - c/op_82 / cpp/op_64 -- **total equality**

### byte-identical group [b8 08 00 00 00 c3] · (i64,None)

- ground: cluster
- languages: c, cpp
- members: c `sizeof` (i64,None, 0 modes); c `__alignof__` (i64,None, 0 modes); c `__alignof` (i64,None, 0 modes); c `_Alignof` (i64,None, 0 modes); cpp `sizeof` (i64,None, 0 modes)

  - c/op_49 / cpp/op_61 -- **total equality**
  - c/op_55 / cpp/op_61 -- **total equality**
  - c/op_61 / cpp/op_61 -- **total equality**
  - c/op_79 / cpp/op_61 -- **total equality**

### byte-identical group [b8 08 00 00 00 c3] · (u64,None)

- ground: cluster
- languages: c, cpp
- members: c `sizeof` (u64,None, 0 modes); c `__alignof__` (u64,None, 0 modes); c `__alignof` (u64,None, 0 modes); c `_Alignof` (u64,None, 0 modes); cpp `sizeof` (u64,None, 0 modes)

  - c/op_50 / cpp/op_62 -- **total equality**
  - c/op_56 / cpp/op_62 -- **total equality**
  - c/op_62 / cpp/op_62 -- **total equality**
  - c/op_80 / cpp/op_62 -- **total equality**

### byte-identical group [48 39 f7 0f 95 c0 c3] · (i64,i64)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `!=` (i64,i64, 0 modes); cpp `not_eq` (i64,i64, 0 modes); rust `!=` (i64,i64, 0 modes); swift `!=` (i64,i64, 0 modes)

  - cpp/op_505 / rust/op_289 -- **total equality**
  - cpp/op_973 / rust/op_289 -- **total equality**
  - cpp/op_505 / swift/op_445 -- **total equality**
  - cpp/op_973 / swift/op_445 -- **total equality**
  - rust/op_289 / swift/op_445 -- **total equality**

### byte-identical group [48 39 f7 0f 95 c0 c3] · (u64,u64)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `!=` (u64,u64, 0 modes); cpp `not_eq` (u64,u64, 0 modes); rust `!=` (u64,u64, 0 modes); swift `!=` (u64,u64, 0 modes)

  - cpp/op_512 / rust/op_296 -- **total equality**
  - cpp/op_980 / rust/op_296 -- **total equality**
  - cpp/op_512 / swift/op_452 -- **total equality**
  - cpp/op_980 / swift/op_452 -- **total equality**
  - rust/op_296 / swift/op_452 -- **total equality**

### byte-identical group [48 89 f1 48 89 f8 48 d3 e0 c3] · (i64,i64)

- ground: cluster
- languages: c, cpp, rust
- members: c `<<` (i64,i64, 0 modes); cpp `<<` (i64,i64, 0 modes); rust `<<` (i64,i64, 0 modes)

  - c/op_685 / cpp/op_685 -- **total equality**
  - c/op_685 / rust/op_469 -- **total equality**
  - cpp/op_685 / rust/op_469 -- **total equality**

### byte-identical group [48 89 f1 48 89 f8 48 d3 e0 c3] · (i64,u64)

- ground: cluster
- languages: c, cpp, rust
- members: c `<<` (i64,u64, 1 modes); cpp `<<` (i64,u64, 1 modes); rust `<<` (i64,u64, 1 modes)

  - c/op_686 / cpp/op_686 -- **total equality**
  - c/op_686 / rust/op_470 -- **total equality**
  - cpp/op_686 / rust/op_470 -- **total equality**

### byte-identical group [48 89 f1 48 89 f8 48 d3 e0 c3] · (u64,i64)

- ground: cluster
- languages: c, cpp, rust
- members: c `<<` (u64,i64, 0 modes); cpp `<<` (u64,i64, 0 modes); rust `<<` (u64,i64, 0 modes)

  - c/op_691 / cpp/op_691 -- **total equality**
  - c/op_691 / rust/op_475 -- **total equality**
  - cpp/op_691 / rust/op_475 -- **total equality**

### byte-identical group [48 89 f1 48 89 f8 48 d3 e0 c3] · (u64,u64)

- ground: cluster
- languages: c, cpp, rust
- members: c `<<` (u64,u64, 2 modes); cpp `<<` (u64,u64, 2 modes); rust `<<` (u64,u64, 2 modes)

  - c/op_692 / cpp/op_692 -- **total equality**
  - c/op_692 / rust/op_476 -- **total equality**
  - cpp/op_692 / rust/op_476 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f c2 c8 04 66 48 0f 7e c8 83 e0 01 c3] · (bool,f64)

- ground: cluster
- languages: c, cpp
- members: c `!=` (bool,f64, 0 modes); cpp `!=` (bool,f64, 0 modes); cpp `not_eq` (bool,f64, 0 modes)

  - c/op_532 / cpp/op_532 -- **total equality**
  - c/op_532 / cpp/op_1000 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f c2 c8 04 66 48 0f 7e c8 83 e0 01 c3] · (f64,bool)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f64,bool, 0 modes); cpp `!=` (f64,bool, 0 modes); cpp `not_eq` (f64,bool, 0 modes)

  - c/op_527 / cpp/op_527 -- **total equality**
  - c/op_527 / cpp/op_995 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f c2 c8 04 66 48 0f 7e c8 83 e0 01 c3] · (f64,i32)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f64,i32, 0 modes); cpp `!=` (f64,i32, 0 modes); cpp `not_eq` (f64,i32, 0 modes)

  - c/op_522 / cpp/op_522 -- **total equality**
  - c/op_522 / cpp/op_990 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f c2 c8 04 66 48 0f 7e c8 83 e0 01 c3] · (i32,f64)

- ground: cluster
- languages: c, cpp
- members: c `!=` (i32,f64, 0 modes); cpp `!=` (i32,f64, 0 modes); cpp `not_eq` (i32,f64, 0 modes)

  - c/op_502 / cpp/op_502 -- **total equality**
  - c/op_502 / cpp/op_970 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f c2 c8 04 66 0f 7e c8 83 e0 01 c3] · (bool,f32)

- ground: cluster
- languages: c, cpp
- members: c `!=` (bool,f32, 0 modes); cpp `!=` (bool,f32, 0 modes); cpp `not_eq` (bool,f32, 0 modes)

  - c/op_531 / cpp/op_531 -- **total equality**
  - c/op_531 / cpp/op_999 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f c2 c8 04 66 0f 7e c8 83 e0 01 c3] · (f32,bool)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f32,bool, 0 modes); cpp `!=` (f32,bool, 0 modes); cpp `not_eq` (f32,bool, 0 modes)

  - c/op_521 / cpp/op_521 -- **total equality**
  - c/op_521 / cpp/op_989 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f c2 c8 04 66 0f 7e c8 83 e0 01 c3] · (f32,i32)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f32,i32, 0 modes); cpp `!=` (f32,i32, 0 modes); cpp `not_eq` (f32,i32, 0 modes)

  - c/op_516 / cpp/op_516 -- **total equality**
  - c/op_516 / cpp/op_984 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f c2 c8 04 66 0f 7e c8 83 e0 01 c3] · (i32,f32)

- ground: cluster
- languages: c, cpp
- members: c `!=` (i32,f32, 0 modes); cpp `!=` (i32,f32, 0 modes); cpp `not_eq` (i32,f32, 0 modes)

  - c/op_501 / cpp/op_501 -- **total equality**
  - c/op_501 / cpp/op_969 -- **total equality**

### byte-identical group [48 89 f1 89 f8 d3 e0 c3] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `<<` (bool,i64, 0 modes); cpp `<<` (bool,i64, 0 modes)

  - c/op_709 / cpp/op_709 -- **total equality**

### byte-identical group [48 89 f1 89 f8 d3 e0 c3] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `<<` (bool,u64, 0 modes); cpp `<<` (bool,u64, 0 modes)

  - c/op_710 / cpp/op_710 -- **total equality**

### byte-identical group [48 89 f1 89 f8 d3 e0 c3] · (i32,i64)

- ground: cluster
- languages: c, cpp, rust
- members: c `<<` (i32,i64, 0 modes); cpp `<<` (i32,i64, 0 modes); rust `<<` (i32,i64, 0 modes)

  - c/op_679 / cpp/op_679 -- **total equality**
  - c/op_679 / rust/op_463 -- **total equality**
  - cpp/op_679 / rust/op_463 -- **total equality**

### byte-identical group [48 89 f1 89 f8 d3 e0 c3] · (i32,u64)

- ground: cluster
- languages: c, cpp, rust
- members: c `<<` (i32,u64, 1 modes); cpp `<<` (i32,u64, 1 modes); rust `<<` (i32,u64, 1 modes)

  - c/op_680 / cpp/op_680 -- **total equality**
  - c/op_680 / rust/op_464 -- **total equality**
  - cpp/op_680 / rust/op_464 -- **total equality**

### byte-identical group [48 89 f8 48 0f af c6 c3] · (i64,i64)

- ground: cluster
- languages: c, cpp, rust
- members: c `*` (i64,i64, 1 modes); cpp `*` (i64,i64, 1 modes); rust `*` (i64,i64, 1 modes)

  - c/op_181 / cpp/op_181 -- **total equality**
  - c/op_181 / rust/op_613 -- **total equality**
  - cpp/op_181 / rust/op_613 -- **total equality**

### byte-identical group [48 89 f8 48 0f af c6 c3] · (i64,u64)

- ground: cluster
- languages: c, cpp
- members: c `*` (i64,u64, 0 modes); cpp `*` (i64,u64, 0 modes)

  - c/op_182 / cpp/op_182 -- **total equality**

### byte-identical group [48 89 f8 48 0f af c6 c3] · (u64,i64)

- ground: cluster
- languages: c, cpp
- members: c `*` (u64,i64, 0 modes); cpp `*` (u64,i64, 0 modes)

  - c/op_187 / cpp/op_187 -- **total equality**

### byte-identical group [48 89 f8 48 0f af c6 c3] · (u64,u64)

- ground: cluster
- languages: c, cpp, rust
- members: c `*` (u64,u64, 0 modes); cpp `*` (u64,u64, 0 modes); rust `*` (u64,u64, 0 modes)

  - c/op_188 / cpp/op_188 -- **total equality**
  - c/op_188 / rust/op_620 -- **total equality**
  - cpp/op_188 / rust/op_620 -- **total equality**

### byte-identical group [48 89 f8 48 29 f0 c3] · (i64,i64)

- ground: cluster
- languages: c, cpp, rust
- members: c `-` (i64,i64, 1 modes); cpp `-` (i64,i64, 1 modes); rust `-` (i64,i64, 1 modes)

  - c/op_145 / cpp/op_145 -- **total equality**
  - c/op_145 / rust/op_577 -- **total equality**
  - cpp/op_145 / rust/op_577 -- **total equality**

### byte-identical group [48 89 f8 48 29 f0 c3] · (i64,u64)

- ground: cluster
- languages: c, cpp
- members: c `-` (i64,u64, 0 modes); cpp `-` (i64,u64, 0 modes)

  - c/op_146 / cpp/op_146 -- **total equality**

### byte-identical group [48 89 f8 48 29 f0 c3] · (u64,i64)

- ground: cluster
- languages: c, cpp
- members: c `-` (u64,i64, 0 modes); cpp `-` (u64,i64, 0 modes)

  - c/op_151 / cpp/op_151 -- **total equality**

### byte-identical group [48 89 f8 48 29 f0 c3] · (u64,u64)

- ground: cluster
- languages: c, cpp, rust
- members: c `-` (u64,u64, 0 modes); cpp `-` (u64,u64, 0 modes); rust `-` (u64,u64, 0 modes)

  - c/op_152 / cpp/op_152 -- **total equality**
  - c/op_152 / rust/op_584 -- **total equality**
  - cpp/op_152 / rust/op_584 -- **total equality**

### byte-identical group [48 89 f8 48 f7 d0 c3] · (i64,None)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `~` (i64,None, 0 modes); cpp `~` (i64,None, 0 modes); cpp `compl` (i64,None, 0 modes); rust `!` (i64,None, 0 modes); swift `~` (i64,None, 0 modes)

  - c/op_7 / cpp/op_7 -- **total equality**
  - c/op_7 / cpp/op_31 -- **total equality**
  - c/op_7 / rust/op_13 -- **total equality**
  - c/op_7 / swift/op_37 -- **total equality**
  - cpp/op_7 / rust/op_13 -- **total equality**
  - cpp/op_31 / rust/op_13 -- **total equality**
  - cpp/op_7 / swift/op_37 -- **total equality**
  - cpp/op_31 / swift/op_37 -- **total equality**
  - rust/op_13 / swift/op_37 -- **total equality**

### byte-identical group [48 89 f8 48 f7 d0 c3] · (u64,None)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `~` (u64,None, 0 modes); cpp `~` (u64,None, 0 modes); cpp `compl` (u64,None, 0 modes); rust `!` (u64,None, 0 modes); swift `~` (u64,None, 0 modes)

  - c/op_8 / cpp/op_8 -- **total equality**
  - c/op_8 / cpp/op_32 -- **total equality**
  - c/op_8 / rust/op_14 -- **total equality**
  - c/op_8 / swift/op_38 -- **total equality**
  - cpp/op_8 / rust/op_14 -- **total equality**
  - cpp/op_32 / rust/op_14 -- **total equality**
  - cpp/op_8 / swift/op_38 -- **total equality**
  - cpp/op_32 / swift/op_38 -- **total equality**
  - rust/op_14 / swift/op_38 -- **total equality**

### byte-identical group [48 8d 04 37 c3] · (i64,i64)

- ground: cluster
- languages: c, cpp, rust
- members: c `+` (i64,i64, 1 modes); cpp `+` (i64,i64, 1 modes); rust `+` (i64,i64, 1 modes)

  - c/op_109 / cpp/op_109 -- **total equality**
  - c/op_109 / rust/op_541 -- **total equality**
  - cpp/op_109 / rust/op_541 -- **total equality**

### byte-identical group [48 8d 04 37 c3] · (i64,u64)

- ground: cluster
- languages: c, cpp
- members: c `+` (i64,u64, 0 modes); cpp `+` (i64,u64, 0 modes)

  - c/op_110 / cpp/op_110 -- **total equality**

### byte-identical group [48 8d 04 37 c3] · (u64,i64)

- ground: cluster
- languages: c, cpp
- members: c `+` (u64,i64, 0 modes); cpp `+` (u64,i64, 0 modes)

  - c/op_115 / cpp/op_115 -- **total equality**

### byte-identical group [48 8d 04 37 c3] · (u64,u64)

- ground: cluster
- languages: c, cpp, rust
- members: c `+` (u64,u64, 1 modes); cpp `+` (u64,u64, 1 modes); rust `+` (u64,u64, 1 modes)

  - c/op_116 / cpp/op_116 -- **total equality**
  - c/op_116 / rust/op_548 -- **total equality**
  - cpp/op_116 / rust/op_548 -- **total equality**

### byte-identical group [89 f1 48 89 f8 48 d3 e0 c3] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `<<` (i64,bool, 0 modes); cpp `<<` (i64,bool, 0 modes)

  - c/op_689 / cpp/op_689 -- **total equality**

### byte-identical group [89 f1 48 89 f8 48 d3 e0 c3] · (i64,i32)

- ground: cluster
- languages: c, cpp, rust
- members: c `<<` (i64,i32, 0 modes); cpp `<<` (i64,i32, 0 modes); rust `<<` (i64,i32, 0 modes)

  - c/op_684 / cpp/op_684 -- **total equality**
  - c/op_684 / rust/op_468 -- **total equality**
  - cpp/op_684 / rust/op_468 -- **total equality**

### byte-identical group [89 f1 48 89 f8 48 d3 e0 c3] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `<<` (u64,bool, 0 modes); cpp `<<` (u64,bool, 0 modes)

  - c/op_695 / cpp/op_695 -- **total equality**

### byte-identical group [89 f1 48 89 f8 48 d3 e0 c3] · (u64,i32)

- ground: cluster
- languages: c, cpp, rust
- members: c `<<` (u64,i32, 0 modes); cpp `<<` (u64,i32, 0 modes); rust `<<` (u64,i32, 0 modes)

  - c/op_690 / cpp/op_690 -- **total equality**
  - c/op_690 / rust/op_474 -- **total equality**
  - cpp/op_690 / rust/op_474 -- **total equality**

### byte-identical group [b8 04 00 00 00 c3] · (f32,None)

- ground: cluster
- languages: c, cpp
- members: c `sizeof` (f32,None, 0 modes); c `__alignof__` (f32,None, 0 modes); c `__alignof` (f32,None, 0 modes); c `_Alignof` (f32,None, 0 modes); cpp `sizeof` (f32,None, 0 modes)

  - c/op_51 / cpp/op_63 -- **total equality**
  - c/op_57 / cpp/op_63 -- **total equality**
  - c/op_63 / cpp/op_63 -- **total equality**
  - c/op_81 / cpp/op_63 -- **total equality**

### byte-identical group [b8 04 00 00 00 c3] · (i32,None)

- ground: cluster
- languages: c, cpp
- members: c `sizeof` (i32,None, 0 modes); c `__alignof__` (i32,None, 0 modes); c `__alignof` (i32,None, 0 modes); c `_Alignof` (i32,None, 0 modes); cpp `sizeof` (i32,None, 0 modes)

  - c/op_48 / cpp/op_60 -- **total equality**
  - c/op_54 / cpp/op_60 -- **total equality**
  - c/op_60 / cpp/op_60 -- **total equality**
  - c/op_78 / cpp/op_60 -- **total equality**

### byte-identical group [89 f1 89 f8 d3 e0 c3] · (bool,bool)

- ground: cluster
- languages: c, cpp
- members: c `<<` (bool,bool, 0 modes); cpp `<<` (bool,bool, 0 modes)

  - c/op_713 / cpp/op_713 -- **total equality**

### byte-identical group [89 f1 89 f8 d3 e0 c3] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `<<` (bool,i32, 0 modes); cpp `<<` (bool,i32, 0 modes)

  - c/op_708 / cpp/op_708 -- **total equality**

### byte-identical group [89 f1 89 f8 d3 e0 c3] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `<<` (i32,bool, 0 modes); cpp `<<` (i32,bool, 0 modes)

  - c/op_683 / cpp/op_683 -- **total equality**

### byte-identical group [89 f1 89 f8 d3 e0 c3] · (i32,i32)

- ground: cluster
- languages: c, cpp, rust
- members: c `<<` (i32,i32, 0 modes); cpp `<<` (i32,i32, 0 modes); rust `<<` (i32,i32, 0 modes)

  - c/op_678 / cpp/op_678 -- **total equality**
  - c/op_678 / rust/op_462 -- **total equality**
  - cpp/op_678 / rust/op_462 -- **total equality**

### byte-identical group [89 f8 29 f0 c3] · (bool,bool)

- ground: cluster
- languages: c, cpp
- members: c `-` (bool,bool, 0 modes); cpp `-` (bool,bool, 0 modes)

  - c/op_173 / cpp/op_173 -- **total equality**

### byte-identical group [89 f8 29 f0 c3] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `-` (bool,i32, 0 modes); cpp `-` (bool,i32, 0 modes)

  - c/op_168 / cpp/op_168 -- **total equality**

### byte-identical group [89 f8 29 f0 c3] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `-` (i32,bool, 0 modes); cpp `-` (i32,bool, 0 modes)

  - c/op_143 / cpp/op_143 -- **total equality**

### byte-identical group [89 f8 29 f0 c3] · (i32,i32)

- ground: cluster
- languages: c, cpp, rust
- members: c `-` (i32,i32, 1 modes); cpp `-` (i32,i32, 1 modes); rust `-` (i32,i32, 1 modes)

  - c/op_138 / cpp/op_138 -- **total equality**
  - c/op_138 / rust/op_570 -- **total equality**
  - cpp/op_138 / rust/op_570 -- **total equality**

### byte-identical group [8d 04 37 c3] · (bool,bool)

- ground: cluster
- languages: c, cpp
- members: c `+` (bool,bool, 0 modes); cpp `+` (bool,bool, 0 modes)

  - c/op_137 / cpp/op_137 -- **total equality**

### byte-identical group [8d 04 37 c3] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `+` (bool,i32, 0 modes); cpp `+` (bool,i32, 0 modes)

  - c/op_132 / cpp/op_132 -- **total equality**

### byte-identical group [8d 04 37 c3] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `+` (i32,bool, 0 modes); cpp `+` (i32,bool, 0 modes)

  - c/op_107 / cpp/op_107 -- **total equality**

### byte-identical group [8d 04 37 c3] · (i32,i32)

- ground: cluster
- languages: c, cpp, rust
- members: c `+` (i32,i32, 1 modes); cpp `+` (i32,i32, 1 modes); rust `+` (i32,i32, 1 modes)

  - c/op_102 / cpp/op_102 -- **total equality**
  - c/op_102 / rust/op_534 -- **total equality**
  - cpp/op_102 / rust/op_534 -- **total equality**

### byte-identical group [0f 57 05 00 00 00 00 c3] · (f32,None)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `-` (f32,None, 0 modes); cpp `-` (f32,None, 0 modes); rust `-` (f32,None, 0 modes); swift `-` (f32,None, 0 modes)

  - c/op_15 / cpp/op_15 -- **total equality**
  - c/op_15 / rust/op_3 -- **total equality**
  - c/op_15 / swift/op_15 -- **total equality**
  - cpp/op_15 / rust/op_3 -- **total equality**
  - cpp/op_15 / swift/op_15 -- **total equality**
  - rust/op_3 / swift/op_15 -- **total equality**

### byte-identical group [0f 57 05 00 00 00 00 c3] · (f64,None)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `-` (f64,None, 0 modes); cpp `-` (f64,None, 0 modes); rust `-` (f64,None, 0 modes); swift `-` (f64,None, 0 modes)

  - c/op_16 / cpp/op_16 -- **total equality**
  - c/op_16 / rust/op_4 -- **total equality**
  - c/op_16 / swift/op_16 -- **total equality**
  - cpp/op_16 / rust/op_4 -- **total equality**
  - cpp/op_16 / swift/op_16 -- **total equality**
  - rust/op_4 / swift/op_16 -- **total equality**

### byte-identical group [31 c0 c3] · (bool,bool)

- ground: cluster
- languages: c, cpp
- members: c `%` (bool,bool, 0 modes); cpp `%` (bool,bool, 0 modes)

  - c/op_281 / cpp/op_281 -- **total equality**

### byte-identical group [31 c0 c3] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `%` (i32,bool, 0 modes); cpp `%` (i32,bool, 0 modes)

  - c/op_251 / cpp/op_251 -- **total equality**

### byte-identical group [31 c0 c3] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `%` (i64,bool, 0 modes); cpp `%` (i64,bool, 0 modes)

  - c/op_257 / cpp/op_257 -- **total equality**

### byte-identical group [31 c0 c3] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `%` (u64,bool, 0 modes); cpp `%` (u64,bool, 0 modes)

  - c/op_263 / cpp/op_263 -- **total equality**

### byte-identical group [48 39 f7 0f 94 c0 c3] · (i64,i64)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `==` (i64,i64, 0 modes); rust `==` (i64,i64, 0 modes); swift `==` (i64,i64, 0 modes)

  - cpp/op_469 / rust/op_253 -- **total equality**
  - cpp/op_469 / swift/op_517 -- **total equality**
  - rust/op_253 / swift/op_517 -- **total equality**

### byte-identical group [48 39 f7 0f 94 c0 c3] · (u64,u64)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `==` (u64,u64, 0 modes); rust `==` (u64,u64, 0 modes); swift `==` (u64,u64, 0 modes)

  - cpp/op_476 / rust/op_260 -- **total equality**
  - cpp/op_476 / swift/op_524 -- **total equality**
  - rust/op_260 / swift/op_524 -- **total equality**

### byte-identical group [89 f8 f7 d0 c3] · (bool,None)

- ground: cluster
- languages: c, cpp
- members: c `~` (bool,None, 0 modes); cpp `~` (bool,None, 0 modes); cpp `compl` (bool,None, 0 modes)

  - c/op_11 / cpp/op_11 -- **total equality**
  - c/op_11 / cpp/op_35 -- **total equality**

### byte-identical group [89 f8 f7 d0 c3] · (i32,None)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `~` (i32,None, 0 modes); cpp `~` (i32,None, 0 modes); cpp `compl` (i32,None, 0 modes); rust `!` (i32,None, 0 modes); swift `~` (i32,None, 0 modes)

  - c/op_6 / cpp/op_6 -- **total equality**
  - c/op_6 / cpp/op_30 -- **total equality**
  - c/op_6 / rust/op_12 -- **total equality**
  - c/op_6 / swift/op_36 -- **total equality**
  - cpp/op_6 / rust/op_12 -- **total equality**
  - cpp/op_30 / rust/op_12 -- **total equality**
  - cpp/op_6 / swift/op_36 -- **total equality**
  - cpp/op_30 / swift/op_36 -- **total equality**
  - rust/op_12 / swift/op_36 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f 58 c1 c3] · (bool,f64)

- ground: cluster
- languages: c, cpp
- members: c `+` (bool,f64, 0 modes); cpp `+` (bool,f64, 0 modes)

  - c/op_136 / cpp/op_136 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f 58 c1 c3] · (f64,bool)

- ground: cluster
- languages: c, cpp
- members: c `+` (f64,bool, 0 modes); cpp `+` (f64,bool, 0 modes)

  - c/op_131 / cpp/op_131 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f 58 c1 c3] · (f64,i32)

- ground: cluster
- languages: c, cpp
- members: c `+` (f64,i32, 0 modes); cpp `+` (f64,i32, 0 modes)

  - c/op_126 / cpp/op_126 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f 58 c1 c3] · (i32,f64)

- ground: cluster
- languages: c, cpp
- members: c `+` (i32,f64, 0 modes); cpp `+` (i32,f64, 0 modes)

  - c/op_106 / cpp/op_106 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f 59 c1 c3] · (bool,f64)

- ground: cluster
- languages: c, cpp
- members: c `*` (bool,f64, 0 modes); cpp `*` (bool,f64, 0 modes)

  - c/op_208 / cpp/op_208 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f 59 c1 c3] · (f64,bool)

- ground: cluster
- languages: c, cpp
- members: c `*` (f64,bool, 0 modes); cpp `*` (f64,bool, 0 modes)

  - c/op_203 / cpp/op_203 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f 59 c1 c3] · (f64,i32)

- ground: cluster
- languages: c, cpp
- members: c `*` (f64,i32, 0 modes); cpp `*` (f64,i32, 0 modes)

  - c/op_198 / cpp/op_198 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f 59 c1 c3] · (i32,f64)

- ground: cluster
- languages: c, cpp
- members: c `*` (i32,f64, 0 modes); cpp `*` (i32,f64, 0 modes)

  - c/op_178 / cpp/op_178 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f c2 c8 00 66 48 0f 7e c8 83 e0 01 c3] · (bool,f64)

- ground: cluster
- languages: c, cpp
- members: c `==` (bool,f64, 0 modes); cpp `==` (bool,f64, 0 modes)

  - c/op_496 / cpp/op_496 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f c2 c8 00 66 48 0f 7e c8 83 e0 01 c3] · (f64,bool)

- ground: cluster
- languages: c, cpp
- members: c `==` (f64,bool, 0 modes); cpp `==` (f64,bool, 0 modes)

  - c/op_491 / cpp/op_491 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f c2 c8 00 66 48 0f 7e c8 83 e0 01 c3] · (f64,i32)

- ground: cluster
- languages: c, cpp
- members: c `==` (f64,i32, 0 modes); cpp `==` (f64,i32, 0 modes)

  - c/op_486 / cpp/op_486 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f c2 c8 00 66 48 0f 7e c8 83 e0 01 c3] · (i32,f64)

- ground: cluster
- languages: c, cpp
- members: c `==` (i32,f64, 0 modes); cpp `==` (i32,f64, 0 modes)

  - c/op_466 / cpp/op_466 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f 58 c1 c3] · (bool,f32)

- ground: cluster
- languages: c, cpp
- members: c `+` (bool,f32, 0 modes); cpp `+` (bool,f32, 0 modes)

  - c/op_135 / cpp/op_135 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f 58 c1 c3] · (f32,bool)

- ground: cluster
- languages: c, cpp
- members: c `+` (f32,bool, 0 modes); cpp `+` (f32,bool, 0 modes)

  - c/op_125 / cpp/op_125 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f 58 c1 c3] · (f32,i32)

- ground: cluster
- languages: c, cpp
- members: c `+` (f32,i32, 0 modes); cpp `+` (f32,i32, 0 modes)

  - c/op_120 / cpp/op_120 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f 58 c1 c3] · (i32,f32)

- ground: cluster
- languages: c, cpp
- members: c `+` (i32,f32, 0 modes); cpp `+` (i32,f32, 0 modes)

  - c/op_105 / cpp/op_105 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f 59 c1 c3] · (bool,f32)

- ground: cluster
- languages: c, cpp
- members: c `*` (bool,f32, 0 modes); cpp `*` (bool,f32, 0 modes)

  - c/op_207 / cpp/op_207 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f 59 c1 c3] · (f32,bool)

- ground: cluster
- languages: c, cpp
- members: c `*` (f32,bool, 0 modes); cpp `*` (f32,bool, 0 modes)

  - c/op_197 / cpp/op_197 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f 59 c1 c3] · (f32,i32)

- ground: cluster
- languages: c, cpp
- members: c `*` (f32,i32, 0 modes); cpp `*` (f32,i32, 0 modes)

  - c/op_192 / cpp/op_192 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f 59 c1 c3] · (i32,f32)

- ground: cluster
- languages: c, cpp
- members: c `*` (i32,f32, 0 modes); cpp `*` (i32,f32, 0 modes)

  - c/op_177 / cpp/op_177 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f c2 c8 00 66 0f 7e c8 83 e0 01 c3] · (bool,f32)

- ground: cluster
- languages: c, cpp
- members: c `==` (bool,f32, 0 modes); cpp `==` (bool,f32, 0 modes)

  - c/op_495 / cpp/op_495 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f c2 c8 00 66 0f 7e c8 83 e0 01 c3] · (f32,bool)

- ground: cluster
- languages: c, cpp
- members: c `==` (f32,bool, 0 modes); cpp `==` (f32,bool, 0 modes)

  - c/op_485 / cpp/op_485 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f c2 c8 00 66 0f 7e c8 83 e0 01 c3] · (f32,i32)

- ground: cluster
- languages: c, cpp
- members: c `==` (f32,i32, 0 modes); cpp `==` (f32,i32, 0 modes)

  - c/op_480 / cpp/op_480 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f c2 c8 00 66 0f 7e c8 83 e0 01 c3] · (i32,f32)

- ground: cluster
- languages: c, cpp
- members: c `==` (i32,f32, 0 modes); cpp `==` (i32,f32, 0 modes)

  - c/op_465 / cpp/op_465 -- **total equality**

### byte-identical group [39 f7 0f 95 c0 c3] · (i32,i32)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `!=` (i32,i32, 0 modes); cpp `not_eq` (i32,i32, 0 modes); rust `!=` (i32,i32, 0 modes); swift `!=` (i32,i32, 0 modes)

  - cpp/op_498 / rust/op_282 -- **total equality**
  - cpp/op_966 / rust/op_282 -- **total equality**
  - cpp/op_498 / swift/op_438 -- **total equality**
  - cpp/op_966 / swift/op_438 -- **total equality**
  - rust/op_282 / swift/op_438 -- **total equality**

### byte-identical group [48 63 c6 48 09 f8 c3] · (i64,i32)

- ground: cluster
- languages: c, cpp
- members: c `|` (i64,i32, 0 modes); cpp `|` (i64,i32, 0 modes); cpp `bitor` (i64,i32, 0 modes)

  - c/op_360 / cpp/op_360 -- **total equality**
  - c/op_360 / cpp/op_864 -- **total equality**

### byte-identical group [48 63 c6 48 09 f8 c3] · (u64,i32)

- ground: cluster
- languages: c, cpp
- members: c `|` (u64,i32, 0 modes); cpp `|` (u64,i32, 0 modes); cpp `bitor` (u64,i32, 0 modes)

  - c/op_366 / cpp/op_366 -- **total equality**
  - c/op_366 / cpp/op_870 -- **total equality**

### byte-identical group [48 63 c6 48 21 f8 c3] · (i64,i32)

- ground: cluster
- languages: c, cpp
- members: c `&` (i64,i32, 0 modes); cpp `&` (i64,i32, 0 modes); cpp `bitand` (i64,i32, 0 modes)

  - c/op_432 / cpp/op_432 -- **total equality**
  - c/op_432 / cpp/op_936 -- **total equality**

### byte-identical group [48 63 c6 48 21 f8 c3] · (u64,i32)

- ground: cluster
- languages: c, cpp
- members: c `&` (u64,i32, 0 modes); cpp `&` (u64,i32, 0 modes); cpp `bitand` (u64,i32, 0 modes)

  - c/op_438 / cpp/op_438 -- **total equality**
  - c/op_438 / cpp/op_942 -- **total equality**

### byte-identical group [48 63 c6 48 31 f8 c3] · (i64,i32)

- ground: cluster
- languages: c, cpp
- members: c `^` (i64,i32, 0 modes); cpp `^` (i64,i32, 0 modes); cpp `xor` (i64,i32, 0 modes)

  - c/op_396 / cpp/op_396 -- **total equality**
  - c/op_396 / cpp/op_900 -- **total equality**

### byte-identical group [48 63 c6 48 31 f8 c3] · (u64,i32)

- ground: cluster
- languages: c, cpp
- members: c `^` (u64,i32, 0 modes); cpp `^` (u64,i32, 0 modes); cpp `xor` (u64,i32, 0 modes)

  - c/op_402 / cpp/op_402 -- **total equality**
  - c/op_402 / cpp/op_906 -- **total equality**

### byte-identical group [48 63 c7 48 09 f0 c3] · (i32,i64)

- ground: cluster
- languages: c, cpp
- members: c `|` (i32,i64, 0 modes); cpp `|` (i32,i64, 0 modes); cpp `bitor` (i32,i64, 0 modes)

  - c/op_355 / cpp/op_355 -- **total equality**
  - c/op_355 / cpp/op_859 -- **total equality**

### byte-identical group [48 63 c7 48 09 f0 c3] · (i32,u64)

- ground: cluster
- languages: c, cpp
- members: c `|` (i32,u64, 0 modes); cpp `|` (i32,u64, 0 modes); cpp `bitor` (i32,u64, 0 modes)

  - c/op_356 / cpp/op_356 -- **total equality**
  - c/op_356 / cpp/op_860 -- **total equality**

### byte-identical group [48 63 c7 48 21 f0 c3] · (i32,i64)

- ground: cluster
- languages: c, cpp
- members: c `&` (i32,i64, 0 modes); cpp `&` (i32,i64, 0 modes); cpp `bitand` (i32,i64, 0 modes)

  - c/op_427 / cpp/op_427 -- **total equality**
  - c/op_427 / cpp/op_931 -- **total equality**

### byte-identical group [48 63 c7 48 21 f0 c3] · (i32,u64)

- ground: cluster
- languages: c, cpp
- members: c `&` (i32,u64, 0 modes); cpp `&` (i32,u64, 0 modes); cpp `bitand` (i32,u64, 0 modes)

  - c/op_428 / cpp/op_428 -- **total equality**
  - c/op_428 / cpp/op_932 -- **total equality**

### byte-identical group [48 63 c7 48 31 f0 c3] · (i32,i64)

- ground: cluster
- languages: c, cpp
- members: c `^` (i32,i64, 0 modes); cpp `^` (i32,i64, 0 modes); cpp `xor` (i32,i64, 0 modes)

  - c/op_391 / cpp/op_391 -- **total equality**
  - c/op_391 / cpp/op_895 -- **total equality**

### byte-identical group [48 63 c7 48 31 f0 c3] · (i32,u64)

- ground: cluster
- languages: c, cpp
- members: c `^` (i32,u64, 0 modes); cpp `^` (i32,u64, 0 modes); cpp `xor` (i32,u64, 0 modes)

  - c/op_392 / cpp/op_392 -- **total equality**
  - c/op_392 / cpp/op_896 -- **total equality**

### byte-identical group [48 85 ff 78 07 f3 48 0f 2a cf eb 15 48 89 f8 48 d1 e8 83 e7 01 48 09 c7 f3 48 0f 2a cf f3 0f 58 c9 f3 0f c2 c1 04 66 0f 7e c0 83 e0 01 c3] · (f32,u64)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f32,u64, 0 modes); cpp `!=` (f32,u64, 0 modes); cpp `not_eq` (f32,u64, 0 modes)

  - c/op_518 / cpp/op_518 -- **total equality**
  - c/op_518 / cpp/op_986 -- **total equality**

### byte-identical group [48 85 ff 78 07 f3 48 0f 2a cf eb 15 48 89 f8 48 d1 e8 83 e7 01 48 09 c7 f3 48 0f 2a cf f3 0f 58 c9 f3 0f c2 c1 04 66 0f 7e c0 83 e0 01 c3] · (u64,f32)

- ground: cluster
- languages: c, cpp
- members: c `!=` (u64,f32, 0 modes); cpp `!=` (u64,f32, 0 modes); cpp `not_eq` (u64,f32, 0 modes)

  - c/op_513 / cpp/op_513 -- **total equality**
  - c/op_513 / cpp/op_981 -- **total equality**

### byte-identical group [48 89 f0 21 f8 c3] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `&` (bool,i64, 0 modes); cpp `&` (bool,i64, 0 modes); cpp `bitand` (bool,i64, 0 modes)

  - c/op_457 / cpp/op_457 -- **total equality**
  - c/op_457 / cpp/op_961 -- **total equality**

### byte-identical group [48 89 f0 21 f8 c3] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `&` (bool,u64, 0 modes); cpp `&` (bool,u64, 0 modes); cpp `bitand` (bool,u64, 0 modes)

  - c/op_458 / cpp/op_458 -- **total equality**
  - c/op_458 / cpp/op_962 -- **total equality**

### byte-identical group [48 89 f1 48 89 f8 48 d3 e8 c3] · (u64,i64)

- ground: cluster
- languages: c, cpp, rust
- members: c `>>` (u64,i64, 0 modes); cpp `>>` (u64,i64, 0 modes); rust `>>` (u64,i64, 0 modes)

  - c/op_727 / cpp/op_727 -- **total equality**
  - c/op_727 / rust/op_511 -- **total equality**
  - cpp/op_727 / rust/op_511 -- **total equality**

### byte-identical group [48 89 f1 48 89 f8 48 d3 e8 c3] · (u64,u64)

- ground: cluster
- languages: c, cpp, rust
- members: c `>>` (u64,u64, 2 modes); cpp `>>` (u64,u64, 2 modes); rust `>>` (u64,u64, 2 modes)

  - c/op_728 / cpp/op_728 -- **total equality**
  - c/op_728 / rust/op_512 -- **total equality**
  - cpp/op_728 / rust/op_512 -- **total equality**

### byte-identical group [48 89 f1 48 89 f8 48 d3 f8 c3] · (i64,i64)

- ground: cluster
- languages: c, cpp, rust
- members: c `>>` (i64,i64, 0 modes); cpp `>>` (i64,i64, 0 modes); rust `>>` (i64,i64, 0 modes)

  - c/op_721 / cpp/op_721 -- **total equality**
  - c/op_721 / rust/op_505 -- **total equality**
  - cpp/op_721 / rust/op_505 -- **total equality**

### byte-identical group [48 89 f1 48 89 f8 48 d3 f8 c3] · (i64,u64)

- ground: cluster
- languages: c, cpp, rust
- members: c `>>` (i64,u64, 0 modes); cpp `>>` (i64,u64, 0 modes); rust `>>` (i64,u64, 0 modes)

  - c/op_722 / cpp/op_722 -- **total equality**
  - c/op_722 / rust/op_506 -- **total equality**
  - cpp/op_722 / rust/op_506 -- **total equality**

### byte-identical group [48 89 f1 89 f8 d3 f8 c3] · (i32,i64)

- ground: cluster
- languages: c, cpp, rust
- members: c `>>` (i32,i64, 0 modes); cpp `>>` (i32,i64, 0 modes); rust `>>` (i32,i64, 0 modes)

  - c/op_715 / cpp/op_715 -- **total equality**
  - c/op_715 / rust/op_499 -- **total equality**
  - cpp/op_715 / rust/op_499 -- **total equality**

### byte-identical group [48 89 f1 89 f8 d3 f8 c3] · (i32,u64)

- ground: cluster
- languages: c, cpp, rust
- members: c `>>` (i32,u64, 0 modes); cpp `>>` (i32,u64, 0 modes); rust `>>` (i32,u64, 0 modes)

  - c/op_716 / cpp/op_716 -- **total equality**
  - c/op_716 / rust/op_500 -- **total equality**
  - cpp/op_716 / rust/op_500 -- **total equality**

### byte-identical group [48 89 f8 21 f0 c3] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `&` (i64,bool, 0 modes); cpp `&` (i64,bool, 0 modes); cpp `bitand` (i64,bool, 0 modes)

  - c/op_437 / cpp/op_437 -- **total equality**
  - c/op_437 / cpp/op_941 -- **total equality**

### byte-identical group [48 89 f8 21 f0 c3] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `&` (u64,bool, 0 modes); cpp `&` (u64,bool, 0 modes); cpp `bitand` (u64,bool, 0 modes)

  - c/op_443 / cpp/op_443 -- **total equality**
  - c/op_443 / cpp/op_947 -- **total equality**

### byte-identical group [48 89 f8 31 d2 48 f7 f6 48 89 d0 c3] · (i64,u64)

- ground: cluster
- languages: c, cpp
- members: c `%` (i64,u64, 0 modes); cpp `%` (i64,u64, 0 modes)

  - c/op_254 / cpp/op_254 -- **total equality**

### byte-identical group [48 89 f8 31 d2 48 f7 f6 48 89 d0 c3] · (u64,i64)

- ground: cluster
- languages: c, cpp
- members: c `%` (u64,i64, 0 modes); cpp `%` (u64,i64, 0 modes)

  - c/op_259 / cpp/op_259 -- **total equality**

### byte-identical group [48 89 f8 31 d2 48 f7 f6 48 89 d0 c3] · (u64,u64)

- ground: cluster
- languages: c, cpp
- members: c `%` (u64,u64, 0 modes); cpp `%` (u64,u64, 0 modes)

  - c/op_260 / cpp/op_260 -- **total equality**

### byte-identical group [48 89 f8 31 d2 48 f7 f6 c3] · (i64,u64)

- ground: cluster
- languages: c, cpp
- members: c `/` (i64,u64, 0 modes); cpp `/` (i64,u64, 0 modes)

  - c/op_218 / cpp/op_218 -- **total equality**

### byte-identical group [48 89 f8 31 d2 48 f7 f6 c3] · (u64,i64)

- ground: cluster
- languages: c, cpp
- members: c `/` (u64,i64, 0 modes); cpp `/` (u64,i64, 0 modes)

  - c/op_223 / cpp/op_223 -- **total equality**

### byte-identical group [48 89 f8 31 d2 48 f7 f6 c3] · (u64,u64)

- ground: cluster
- languages: c, cpp
- members: c `/` (u64,u64, 0 modes); cpp `/` (u64,u64, 0 modes)

  - c/op_224 / cpp/op_224 -- **total equality**

### byte-identical group [66 48 0f 6e cf 66 0f 62 0d 00 00 00 00 66 0f 5c 0d 00 00 00 00 66 0f 28 d1 66 0f 15 d1 f2 0f 58 d1 f2 0f c2 d0 04 66 48 0f 7e d0 83 e0 01 c3] · (f64,u64)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f64,u64, 0 modes); cpp `!=` (f64,u64, 0 modes); cpp `not_eq` (f64,u64, 0 modes)

  - c/op_524 / cpp/op_524 -- **total equality**
  - c/op_524 / cpp/op_992 -- **total equality**

### byte-identical group [66 48 0f 6e cf 66 0f 62 0d 00 00 00 00 66 0f 5c 0d 00 00 00 00 66 0f 28 d1 66 0f 15 d1 f2 0f 58 d1 f2 0f c2 d0 04 66 48 0f 7e d0 83 e0 01 c3] · (u64,f64)

- ground: cluster
- languages: c, cpp
- members: c `!=` (u64,f64, 0 modes); cpp `!=` (u64,f64, 0 modes); cpp `not_eq` (u64,f64, 0 modes)

  - c/op_514 / cpp/op_514 -- **total equality**
  - c/op_514 / cpp/op_982 -- **total equality**

### byte-identical group [89 f0 48 09 f8 c3] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `|` (i64,bool, 0 modes); cpp `|` (i64,bool, 0 modes); cpp `bitor` (i64,bool, 0 modes)

  - c/op_365 / cpp/op_365 -- **total equality**
  - c/op_365 / cpp/op_869 -- **total equality**

### byte-identical group [89 f0 48 09 f8 c3] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `|` (u64,bool, 0 modes); cpp `|` (u64,bool, 0 modes); cpp `bitor` (u64,bool, 0 modes)

  - c/op_371 / cpp/op_371 -- **total equality**
  - c/op_371 / cpp/op_875 -- **total equality**

### byte-identical group [89 f0 48 31 f8 c3] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `^` (i64,bool, 0 modes); cpp `^` (i64,bool, 0 modes); cpp `xor` (i64,bool, 0 modes)

  - c/op_401 / cpp/op_401 -- **total equality**
  - c/op_401 / cpp/op_905 -- **total equality**

### byte-identical group [89 f0 48 31 f8 c3] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `^` (u64,bool, 0 modes); cpp `^` (u64,bool, 0 modes); cpp `xor` (u64,bool, 0 modes)

  - c/op_407 / cpp/op_407 -- **total equality**
  - c/op_407 / cpp/op_911 -- **total equality**

### byte-identical group [89 f8 48 09 f0 c3] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `|` (bool,i64, 0 modes); cpp `|` (bool,i64, 0 modes); cpp `bitor` (bool,i64, 0 modes)

  - c/op_385 / cpp/op_385 -- **total equality**
  - c/op_385 / cpp/op_889 -- **total equality**

### byte-identical group [89 f8 48 09 f0 c3] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `|` (bool,u64, 0 modes); cpp `|` (bool,u64, 0 modes); cpp `bitor` (bool,u64, 0 modes)

  - c/op_386 / cpp/op_386 -- **total equality**
  - c/op_386 / cpp/op_890 -- **total equality**

### byte-identical group [89 f8 48 31 f0 c3] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `^` (bool,i64, 0 modes); cpp `^` (bool,i64, 0 modes); cpp `xor` (bool,i64, 0 modes)

  - c/op_421 / cpp/op_421 -- **total equality**
  - c/op_421 / cpp/op_925 -- **total equality**

### byte-identical group [89 f8 48 31 f0 c3] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `^` (bool,u64, 0 modes); cpp `^` (bool,u64, 0 modes); cpp `xor` (bool,u64, 0 modes)

  - c/op_422 / cpp/op_422 -- **total equality**
  - c/op_422 / cpp/op_926 -- **total equality**

### byte-identical group [f2 48 0f 2a cf f2 0f c2 c8 04 66 48 0f 7e c8 83 e0 01 c3] · (f64,i64)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f64,i64, 0 modes); cpp `!=` (f64,i64, 0 modes); cpp `not_eq` (f64,i64, 0 modes)

  - c/op_523 / cpp/op_523 -- **total equality**
  - c/op_523 / cpp/op_991 -- **total equality**

### byte-identical group [f2 48 0f 2a cf f2 0f c2 c8 04 66 48 0f 7e c8 83 e0 01 c3] · (i64,f64)

- ground: cluster
- languages: c, cpp
- members: c `!=` (i64,f64, 0 modes); cpp `!=` (i64,f64, 0 modes); cpp `not_eq` (i64,f64, 0 modes)

  - c/op_508 / cpp/op_508 -- **total equality**
  - c/op_508 / cpp/op_976 -- **total equality**

### byte-identical group [f3 48 0f 2a cf f3 0f c2 c8 04 66 0f 7e c8 83 e0 01 c3] · (f32,i64)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f32,i64, 0 modes); cpp `!=` (f32,i64, 0 modes); cpp `not_eq` (f32,i64, 0 modes)

  - c/op_517 / cpp/op_517 -- **total equality**
  - c/op_517 / cpp/op_985 -- **total equality**

### byte-identical group [f3 48 0f 2a cf f3 0f c2 c8 04 66 0f 7e c8 83 e0 01 c3] · (i64,f32)

- ground: cluster
- languages: c, cpp
- members: c `!=` (i64,f32, 0 modes); cpp `!=` (i64,f32, 0 modes); cpp `not_eq` (i64,f32, 0 modes)

  - c/op_507 / cpp/op_507 -- **total equality**
  - c/op_507 / cpp/op_975 -- **total equality**

### byte-identical group [48 39 f7 0f 92 c0 c3] · (u64,u64)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `<` (u64,u64, 0 modes); rust `<` (u64,u64, 0 modes); swift `<` (u64,u64, 0 modes)

  - cpp/op_656 / rust/op_332 -- **total equality**
  - cpp/op_656 / swift/op_308 -- **total equality**
  - rust/op_332 / swift/op_308 -- **total equality**

### byte-identical group [48 39 f7 0f 93 c0 c3] · (u64,u64)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `>=` (u64,u64, 0 modes); rust `>=` (u64,u64, 0 modes); swift `>=` (u64,u64, 0 modes)

  - cpp/op_584 / rust/op_440 -- **total equality**
  - cpp/op_584 / swift/op_416 -- **total equality**
  - rust/op_440 / swift/op_416 -- **total equality**

### byte-identical group [48 89 f8 48 f7 d8 c3] · (i64,None)

- ground: cluster
- languages: c, cpp, rust
- members: c `-` (i64,None, 1 modes); cpp `-` (i64,None, 1 modes); rust `-` (i64,None, 1 modes)

  - c/op_13 / cpp/op_13 -- **total equality**
  - c/op_13 / rust/op_1 -- **total equality**
  - cpp/op_13 / rust/op_1 -- **total equality**

### byte-identical group [48 89 f8 48 f7 d8 c3] · (u64,None)

- ground: cluster
- languages: c, cpp
- members: c `-` (u64,None, 0 modes); cpp `-` (u64,None, 0 modes)

  - c/op_14 / cpp/op_14 -- **total equality**

### byte-identical group [89 f1 48 89 f8 48 d3 e8 c3] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `>>` (u64,bool, 0 modes); cpp `>>` (u64,bool, 0 modes)

  - c/op_731 / cpp/op_731 -- **total equality**

### byte-identical group [89 f1 48 89 f8 48 d3 e8 c3] · (u64,i32)

- ground: cluster
- languages: c, cpp, rust
- members: c `>>` (u64,i32, 0 modes); cpp `>>` (u64,i32, 0 modes); rust `>>` (u64,i32, 0 modes)

  - c/op_726 / cpp/op_726 -- **total equality**
  - c/op_726 / rust/op_510 -- **total equality**
  - cpp/op_726 / rust/op_510 -- **total equality**

### byte-identical group [89 f1 48 89 f8 48 d3 f8 c3] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `>>` (i64,bool, 0 modes); cpp `>>` (i64,bool, 0 modes)

  - c/op_725 / cpp/op_725 -- **total equality**

### byte-identical group [89 f1 48 89 f8 48 d3 f8 c3] · (i64,i32)

- ground: cluster
- languages: c, cpp, rust
- members: c `>>` (i64,i32, 0 modes); cpp `>>` (i64,i32, 0 modes); rust `>>` (i64,i32, 0 modes)

  - c/op_720 / cpp/op_720 -- **total equality**
  - c/op_720 / rust/op_504 -- **total equality**
  - cpp/op_720 / rust/op_504 -- **total equality**

### byte-identical group [89 f1 89 f8 d3 f8 c3] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `>>` (i32,bool, 0 modes); cpp `>>` (i32,bool, 0 modes)

  - c/op_719 / cpp/op_719 -- **total equality**

### byte-identical group [89 f1 89 f8 d3 f8 c3] · (i32,i32)

- ground: cluster
- languages: c, cpp, rust
- members: c `>>` (i32,i32, 0 modes); cpp `>>` (i32,i32, 0 modes); rust `>>` (i32,i32, 0 modes)

  - c/op_714 / cpp/op_714 -- **total equality**
  - c/op_714 / rust/op_498 -- **total equality**
  - cpp/op_714 / rust/op_498 -- **total equality**

### byte-identical group [89 f8 34 01 c3] · (bool,None)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `--` (bool,None, 0 modes); cpp `!` (bool,None, 1 modes); cpp `not` (bool,None, 1 modes); rust `!` (bool,None, 1 modes); swift `!` (bool,None, 1 modes)

  - c/op_47 / cpp/op_5 -- **core equality, modes differ**
    - only on the right: `in0 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_47 / cpp/op_29 -- **core equality, modes differ**
    - only on the right: `in0 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_47 / rust/op_17 -- **core equality, modes differ**
    - only on the right: `in0 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_47 / swift/op_29 -- **core equality, modes differ**
    - only on the right: `in0 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - cpp/op_5 / rust/op_17 -- **total equality**
  - cpp/op_29 / rust/op_17 -- **total equality**
  - cpp/op_5 / swift/op_29 -- **total equality**
  - cpp/op_29 / swift/op_29 -- **total equality**
  - rust/op_17 / swift/op_29 -- **total equality**

### byte-identical group [89 f8 f7 d8 c3] · (bool,None)

- ground: cluster
- languages: c, cpp
- members: c `-` (bool,None, 0 modes); cpp `-` (bool,None, 0 modes)

  - c/op_17 / cpp/op_17 -- **total equality**

### byte-identical group [89 f8 f7 d8 c3] · (i32,None)

- ground: cluster
- languages: c, cpp, rust
- members: c `-` (i32,None, 1 modes); cpp `-` (i32,None, 1 modes); rust `-` (i32,None, 1 modes)

  - c/op_12 / cpp/op_12 -- **total equality**
  - c/op_12 / rust/op_0 -- **total equality**
  - cpp/op_12 / rust/op_0 -- **total equality**

### byte-identical group [b8 01 00 00 00 c3] · (bool,None)

- ground: cluster
- languages: c, cpp
- members: c `sizeof` (bool,None, 0 modes); c `__alignof__` (bool,None, 0 modes); c `__alignof` (bool,None, 0 modes); c `_Alignof` (bool,None, 0 modes); cpp `sizeof` (bool,None, 0 modes)

  - c/op_53 / cpp/op_65 -- **total equality**
  - c/op_59 / cpp/op_65 -- **total equality**
  - c/op_65 / cpp/op_65 -- **total equality**
  - c/op_83 / cpp/op_65 -- **total equality**

### byte-identical group [f2 0f 58 c1 c3] · (f64,f64)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `+` (f64,f64, 0 modes); cpp `+` (f64,f64, 0 modes); go `+` (f64,f64, 0 modes); rust `+` (f64,f64, 0 modes); swift `+` (f64,f64, 0 modes)

  - c/op_130 / cpp/op_130 -- **total equality**
  - c/op_130 / go/op_340 -- **total equality**
  - c/op_130 / rust/op_562 -- **total equality**
  - c/op_130 / swift/op_250 -- **total equality**
  - cpp/op_130 / go/op_340 -- **total equality**
  - cpp/op_130 / rust/op_562 -- **total equality**
  - cpp/op_130 / swift/op_250 -- **total equality**
  - go/op_340 / rust/op_562 -- **total equality**
  - go/op_340 / swift/op_250 -- **total equality**
  - rust/op_562 / swift/op_250 -- **total equality**

### byte-identical group [f2 0f 59 c1 c3] · (f64,f64)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `*` (f64,f64, 0 modes); cpp `*` (f64,f64, 0 modes); go `*` (f64,f64, 0 modes); rust `*` (f64,f64, 0 modes); swift `*` (f64,f64, 0 modes)

  - c/op_202 / cpp/op_202 -- **total equality**
  - c/op_202 / go/op_88 -- **total equality**
  - c/op_202 / rust/op_634 -- **total equality**
  - c/op_202 / swift/op_142 -- **total equality**
  - cpp/op_202 / go/op_88 -- **total equality**
  - cpp/op_202 / rust/op_634 -- **total equality**
  - cpp/op_202 / swift/op_142 -- **total equality**
  - go/op_88 / rust/op_634 -- **total equality**
  - go/op_88 / swift/op_142 -- **total equality**
  - rust/op_634 / swift/op_142 -- **total equality**

### byte-identical group [f2 0f 5c c1 c3] · (f64,f64)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `-` (f64,f64, 0 modes); cpp `-` (f64,f64, 0 modes); go `-` (f64,f64, 0 modes); rust `-` (f64,f64, 0 modes); swift `-` (f64,f64, 0 modes)

  - c/op_166 / cpp/op_166 -- **total equality**
  - c/op_166 / go/op_376 -- **total equality**
  - c/op_166 / rust/op_598 -- **total equality**
  - c/op_166 / swift/op_286 -- **total equality**
  - cpp/op_166 / go/op_376 -- **total equality**
  - cpp/op_166 / rust/op_598 -- **total equality**
  - cpp/op_166 / swift/op_286 -- **total equality**
  - go/op_376 / rust/op_598 -- **total equality**
  - go/op_376 / swift/op_286 -- **total equality**
  - rust/op_598 / swift/op_286 -- **total equality**

### byte-identical group [f2 0f 5e c1 c3] · (f64,f64)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `/` (f64,f64, 0 modes); cpp `/` (f64,f64, 0 modes); go `/` (f64,f64, 0 modes); rust `/` (f64,f64, 0 modes); swift `/` (f64,f64, 0 modes)

  - c/op_238 / cpp/op_238 -- **total equality**
  - c/op_238 / go/op_124 -- **total equality**
  - c/op_238 / rust/op_670 -- **total equality**
  - c/op_238 / swift/op_178 -- **total equality**
  - cpp/op_238 / go/op_124 -- **total equality**
  - cpp/op_238 / rust/op_670 -- **total equality**
  - cpp/op_238 / swift/op_178 -- **total equality**
  - go/op_124 / rust/op_670 -- **total equality**
  - go/op_124 / swift/op_178 -- **total equality**
  - rust/op_670 / swift/op_178 -- **total equality**

### byte-identical group [f2 0f c2 c1 04 66 48 0f 7e c0 83 e0 01 c3] · (f64,f64)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `!=` (f64,f64, 0 modes); cpp `!=` (f64,f64, 0 modes); cpp `not_eq` (f64,f64, 0 modes); rust `!=` (f64,f64, 0 modes); swift `!=` (f64,f64, 0 modes)

  - c/op_526 / cpp/op_526 -- **total equality**
  - c/op_526 / cpp/op_994 -- **total equality**
  - c/op_526 / rust/op_310 -- **total equality**
  - c/op_526 / swift/op_466 -- **total equality**
  - cpp/op_526 / rust/op_310 -- **total equality**
  - cpp/op_994 / rust/op_310 -- **total equality**
  - cpp/op_526 / swift/op_466 -- **total equality**
  - cpp/op_994 / swift/op_466 -- **total equality**
  - rust/op_310 / swift/op_466 -- **total equality**

### byte-identical group [f3 0f 58 c1 c3] · (f32,f32)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `+` (f32,f32, 0 modes); cpp `+` (f32,f32, 0 modes); go `+` (f32,f32, 0 modes); rust `+` (f32,f32, 0 modes); swift `+` (f32,f32, 0 modes)

  - c/op_123 / cpp/op_123 -- **total equality**
  - c/op_123 / go/op_333 -- **total equality**
  - c/op_123 / rust/op_555 -- **total equality**
  - c/op_123 / swift/op_243 -- **total equality**
  - cpp/op_123 / go/op_333 -- **total equality**
  - cpp/op_123 / rust/op_555 -- **total equality**
  - cpp/op_123 / swift/op_243 -- **total equality**
  - go/op_333 / rust/op_555 -- **total equality**
  - go/op_333 / swift/op_243 -- **total equality**
  - rust/op_555 / swift/op_243 -- **total equality**

### byte-identical group [f3 0f 59 c1 c3] · (f32,f32)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `*` (f32,f32, 0 modes); cpp `*` (f32,f32, 0 modes); go `*` (f32,f32, 0 modes); rust `*` (f32,f32, 0 modes); swift `*` (f32,f32, 0 modes)

  - c/op_195 / cpp/op_195 -- **total equality**
  - c/op_195 / go/op_81 -- **total equality**
  - c/op_195 / rust/op_627 -- **total equality**
  - c/op_195 / swift/op_135 -- **total equality**
  - cpp/op_195 / go/op_81 -- **total equality**
  - cpp/op_195 / rust/op_627 -- **total equality**
  - cpp/op_195 / swift/op_135 -- **total equality**
  - go/op_81 / rust/op_627 -- **total equality**
  - go/op_81 / swift/op_135 -- **total equality**
  - rust/op_627 / swift/op_135 -- **total equality**

### byte-identical group [f3 0f 5c c1 c3] · (f32,f32)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `-` (f32,f32, 0 modes); cpp `-` (f32,f32, 0 modes); go `-` (f32,f32, 0 modes); rust `-` (f32,f32, 0 modes); swift `-` (f32,f32, 0 modes)

  - c/op_159 / cpp/op_159 -- **total equality**
  - c/op_159 / go/op_369 -- **total equality**
  - c/op_159 / rust/op_591 -- **total equality**
  - c/op_159 / swift/op_279 -- **total equality**
  - cpp/op_159 / go/op_369 -- **total equality**
  - cpp/op_159 / rust/op_591 -- **total equality**
  - cpp/op_159 / swift/op_279 -- **total equality**
  - go/op_369 / rust/op_591 -- **total equality**
  - go/op_369 / swift/op_279 -- **total equality**
  - rust/op_591 / swift/op_279 -- **total equality**

### byte-identical group [f3 0f 5e c1 c3] · (f32,f32)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `/` (f32,f32, 0 modes); cpp `/` (f32,f32, 0 modes); go `/` (f32,f32, 0 modes); rust `/` (f32,f32, 0 modes); swift `/` (f32,f32, 0 modes)

  - c/op_231 / cpp/op_231 -- **total equality**
  - c/op_231 / go/op_117 -- **total equality**
  - c/op_231 / rust/op_663 -- **total equality**
  - c/op_231 / swift/op_171 -- **total equality**
  - cpp/op_231 / go/op_117 -- **total equality**
  - cpp/op_231 / rust/op_663 -- **total equality**
  - cpp/op_231 / swift/op_171 -- **total equality**
  - go/op_117 / rust/op_663 -- **total equality**
  - go/op_117 / swift/op_171 -- **total equality**
  - rust/op_663 / swift/op_171 -- **total equality**

### byte-identical group [f3 0f c2 c1 04 66 0f 7e c0 83 e0 01 c3] · (f32,f32)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `!=` (f32,f32, 0 modes); cpp `!=` (f32,f32, 0 modes); cpp `not_eq` (f32,f32, 0 modes); rust `!=` (f32,f32, 0 modes); swift `!=` (f32,f32, 0 modes)

  - c/op_519 / cpp/op_519 -- **total equality**
  - c/op_519 / cpp/op_987 -- **total equality**
  - c/op_519 / rust/op_303 -- **total equality**
  - c/op_519 / swift/op_459 -- **total equality**
  - cpp/op_519 / rust/op_303 -- **total equality**
  - cpp/op_987 / rust/op_303 -- **total equality**
  - cpp/op_519 / swift/op_459 -- **total equality**
  - cpp/op_987 / swift/op_459 -- **total equality**
  - rust/op_303 / swift/op_459 -- **total equality**

### byte-identical group [0f 2e c1 0f 93 c0 c3] · (f32,f32)

- ground: cluster
- languages: cpp, go, rust, swift
- members: cpp `>=` (f32,f32, 0 modes); go `>=` (f32,f32, 0 modes); rust `>=` (f32,f32, 0 modes); swift `>=` (f32,f32, 0 modes)

  - cpp/op_591 / go/op_657 -- **total equality**
  - cpp/op_591 / rust/op_447 -- **total equality**
  - cpp/op_591 / swift/op_423 -- **total equality**
  - go/op_657 / rust/op_447 -- **total equality**
  - go/op_657 / swift/op_423 -- **total equality**
  - rust/op_447 / swift/op_423 -- **total equality**

### byte-identical group [0f 2e c1 0f 97 c0 c3] · (f32,f32)

- ground: cluster
- languages: cpp, go, rust, swift
- members: cpp `>` (f32,f32, 0 modes); go `>` (f32,f32, 0 modes); rust `>` (f32,f32, 0 modes); swift `>` (f32,f32, 0 modes)

  - cpp/op_555 / go/op_621 -- **total equality**
  - cpp/op_555 / rust/op_411 -- **total equality**
  - cpp/op_555 / swift/op_351 -- **total equality**
  - go/op_621 / rust/op_411 -- **total equality**
  - go/op_621 / swift/op_351 -- **total equality**
  - rust/op_411 / swift/op_351 -- **total equality**

### byte-identical group [0f 2e c8 0f 93 c0 c3] · (f32,f32)

- ground: cluster
- languages: cpp, go, rust, swift
- members: cpp `<=` (f32,f32, 0 modes); go `<=` (f32,f32, 0 modes); rust `<=` (f32,f32, 0 modes); swift `<=` (f32,f32, 0 modes)

  - cpp/op_627 / go/op_585 -- **total equality**
  - cpp/op_627 / rust/op_375 -- **total equality**
  - cpp/op_627 / swift/op_387 -- **total equality**
  - go/op_585 / rust/op_375 -- **total equality**
  - go/op_585 / swift/op_387 -- **total equality**
  - rust/op_375 / swift/op_387 -- **total equality**

### byte-identical group [0f 2e c8 0f 97 c0 c3] · (f32,f32)

- ground: cluster
- languages: cpp, go, rust, swift
- members: cpp `<` (f32,f32, 0 modes); go `<` (f32,f32, 0 modes); rust `<` (f32,f32, 0 modes); swift `<` (f32,f32, 0 modes)

  - cpp/op_663 / go/op_549 -- **total equality**
  - cpp/op_663 / rust/op_339 -- **total equality**
  - cpp/op_663 / swift/op_315 -- **total equality**
  - go/op_549 / rust/op_339 -- **total equality**
  - go/op_549 / swift/op_315 -- **total equality**
  - rust/op_339 / swift/op_315 -- **total equality**

### byte-identical group [31 c0 85 f6 48 0f 45 c7 c3] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `*` (i64,bool, 0 modes); cpp `*` (i64,bool, 0 modes)

  - c/op_185 / cpp/op_185 -- **total equality**

### byte-identical group [31 c0 85 f6 48 0f 45 c7 c3] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `*` (u64,bool, 0 modes); cpp `*` (u64,bool, 0 modes)

  - c/op_191 / cpp/op_191 -- **total equality**

### byte-identical group [31 c0 85 ff 48 0f 45 c6 c3] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `*` (bool,i64, 0 modes); cpp `*` (bool,i64, 0 modes)

  - c/op_205 / cpp/op_205 -- **total equality**

### byte-identical group [31 c0 85 ff 48 0f 45 c6 c3] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `*` (bool,u64, 0 modes); cpp `*` (bool,u64, 0 modes)

  - c/op_206 / cpp/op_206 -- **total equality**

### byte-identical group [39 f7 0f 94 c0 c3] · (i32,i32)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `==` (i32,i32, 0 modes); rust `==` (i32,i32, 0 modes); swift `==` (i32,i32, 0 modes)

  - cpp/op_462 / rust/op_246 -- **total equality**
  - cpp/op_462 / swift/op_510 -- **total equality**
  - rust/op_246 / swift/op_510 -- **total equality**

### byte-identical group [39 f7 0f 9c c0 c3] · (i32,i32)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `<` (i32,i32, 0 modes); rust `<` (i32,i32, 0 modes); swift `<` (i32,i32, 0 modes)

  - cpp/op_642 / rust/op_318 -- **total equality**
  - cpp/op_642 / swift/op_294 -- **total equality**
  - rust/op_318 / swift/op_294 -- **total equality**

### byte-identical group [39 f7 0f 9d c0 c3] · (i32,i32)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `>=` (i32,i32, 0 modes); rust `>=` (i32,i32, 0 modes); swift `>=` (i32,i32, 0 modes)

  - cpp/op_570 / rust/op_426 -- **total equality**
  - cpp/op_570 / swift/op_402 -- **total equality**
  - rust/op_426 / swift/op_402 -- **total equality**

### byte-identical group [48 39 f7 0f 96 c0 c3] · (u64,u64)

- ground: cluster
- languages: cpp, rust
- members: cpp `<=` (u64,u64, 0 modes); rust `<=` (u64,u64, 0 modes)

  - cpp/op_620 / rust/op_368 -- **total equality**

### byte-identical group [48 39 f7 0f 97 c0 c3] · (u64,u64)

- ground: cluster
- languages: cpp, rust
- members: cpp `>` (u64,u64, 0 modes); rust `>` (u64,u64, 0 modes)

  - cpp/op_548 / rust/op_404 -- **total equality**

### byte-identical group [48 63 c6 48 01 f8 c3] · (i64,i32)

- ground: cluster
- languages: c, cpp
- members: c `+` (i64,i32, 0 modes); cpp `+` (i64,i32, 0 modes)

  - c/op_108 / cpp/op_108 -- **total equality**

### byte-identical group [48 63 c6 48 01 f8 c3] · (u64,i32)

- ground: cluster
- languages: c, cpp
- members: c `+` (u64,i32, 0 modes); cpp `+` (u64,i32, 0 modes)

  - c/op_114 / cpp/op_114 -- **total equality**

### byte-identical group [48 63 c6 48 0f af c7 c3] · (i64,i32)

- ground: cluster
- languages: c, cpp
- members: c `*` (i64,i32, 0 modes); cpp `*` (i64,i32, 0 modes)

  - c/op_180 / cpp/op_180 -- **total equality**

### byte-identical group [48 63 c6 48 0f af c7 c3] · (u64,i32)

- ground: cluster
- languages: c, cpp
- members: c `*` (u64,i32, 0 modes); cpp `*` (u64,i32, 0 modes)

  - c/op_186 / cpp/op_186 -- **total equality**

### byte-identical group [48 63 c7 48 01 f0 c3] · (i32,i64)

- ground: cluster
- languages: c, cpp
- members: c `+` (i32,i64, 0 modes); cpp `+` (i32,i64, 0 modes)

  - c/op_103 / cpp/op_103 -- **total equality**

### byte-identical group [48 63 c7 48 01 f0 c3] · (i32,u64)

- ground: cluster
- languages: c, cpp
- members: c `+` (i32,u64, 0 modes); cpp `+` (i32,u64, 0 modes)

  - c/op_104 / cpp/op_104 -- **total equality**

### byte-identical group [48 63 c7 48 0f af c6 c3] · (i32,i64)

- ground: cluster
- languages: c, cpp
- members: c `*` (i32,i64, 0 modes); cpp `*` (i32,i64, 0 modes)

  - c/op_175 / cpp/op_175 -- **total equality**

### byte-identical group [48 63 c7 48 0f af c6 c3] · (i32,u64)

- ground: cluster
- languages: c, cpp
- members: c `*` (i32,u64, 0 modes); cpp `*` (i32,u64, 0 modes)

  - c/op_176 / cpp/op_176 -- **total equality**

### byte-identical group [48 63 c7 48 29 f0 c3] · (i32,i64)

- ground: cluster
- languages: c, cpp
- members: c `-` (i32,i64, 0 modes); cpp `-` (i32,i64, 0 modes)

  - c/op_139 / cpp/op_139 -- **total equality**

### byte-identical group [48 63 c7 48 29 f0 c3] · (i32,u64)

- ground: cluster
- languages: c, cpp
- members: c `-` (i32,u64, 0 modes); cpp `-` (i32,u64, 0 modes)

  - c/op_140 / cpp/op_140 -- **total equality**

### byte-identical group [48 85 ff 78 07 f3 48 0f 2a cf eb 15 48 89 f8 48 d1 e8 83 e7 01 48 09 c7 f3 48 0f 2a cf f3 0f 58 c9 f3 0f c2 c1 00 66 0f 7e c0 83 e0 01 c3] · (f32,u64)

- ground: cluster
- languages: c, cpp
- members: c `==` (f32,u64, 0 modes); cpp `==` (f32,u64, 0 modes)

  - c/op_482 / cpp/op_482 -- **total equality**

### byte-identical group [48 85 ff 78 07 f3 48 0f 2a cf eb 15 48 89 f8 48 d1 e8 83 e7 01 48 09 c7 f3 48 0f 2a cf f3 0f 58 c9 f3 0f c2 c1 00 66 0f 7e c0 83 e0 01 c3] · (u64,f32)

- ground: cluster
- languages: c, cpp
- members: c `==` (u64,f32, 0 modes); cpp `==` (u64,f32, 0 modes)

  - c/op_477 / cpp/op_477 -- **total equality**

### byte-identical group [48 85 ff 78 0a f3 48 0f 2a cf f3 0f 58 c1 c3 48 89 f8 48 d1 e8 83 e7 01 48 09 c7 f3 48 0f 2a cf f3 0f 58 c9 f3 0f 58 c1 c3] · (f32,u64)

- ground: cluster
- languages: c, cpp
- members: c `+` (f32,u64, 0 modes); cpp `+` (f32,u64, 0 modes)

  - c/op_122 / cpp/op_122 -- **total equality**

### byte-identical group [48 85 ff 78 0a f3 48 0f 2a cf f3 0f 58 c1 c3 48 89 f8 48 d1 e8 83 e7 01 48 09 c7 f3 48 0f 2a cf f3 0f 58 c9 f3 0f 58 c1 c3] · (u64,f32)

- ground: cluster
- languages: c, cpp
- members: c `+` (u64,f32, 0 modes); cpp `+` (u64,f32, 0 modes)

  - c/op_117 / cpp/op_117 -- **total equality**

### byte-identical group [48 85 ff 78 0a f3 48 0f 2a cf f3 0f 59 c1 c3 48 89 f8 48 d1 e8 83 e7 01 48 09 c7 f3 48 0f 2a cf f3 0f 58 c9 f3 0f 59 c1 c3] · (f32,u64)

- ground: cluster
- languages: c, cpp
- members: c `*` (f32,u64, 0 modes); cpp `*` (f32,u64, 0 modes)

  - c/op_194 / cpp/op_194 -- **total equality**

### byte-identical group [48 85 ff 78 0a f3 48 0f 2a cf f3 0f 59 c1 c3 48 89 f8 48 d1 e8 83 e7 01 48 09 c7 f3 48 0f 2a cf f3 0f 58 c9 f3 0f 59 c1 c3] · (u64,f32)

- ground: cluster
- languages: c, cpp
- members: c `*` (u64,f32, 0 modes); cpp `*` (u64,f32, 0 modes)

  - c/op_189 / cpp/op_189 -- **total equality**

### byte-identical group [48 89 7c 24 f8 48 8d 44 24 f8 c3] · (i64,None)

- ground: cluster
- languages: c, cpp
- members: c `&` (i64,None, 0 modes); cpp `&` (i64,None, 0 modes)

  - c/op_31 / cpp/op_43 -- **total equality**

### byte-identical group [48 89 7c 24 f8 48 8d 44 24 f8 c3] · (u64,None)

- ground: cluster
- languages: c, cpp
- members: c `&` (u64,None, 0 modes); cpp `&` (u64,None, 0 modes)

  - c/op_32 / cpp/op_44 -- **total equality**

### byte-identical group [48 89 f1 89 f8 d3 e8 c3] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `>>` (bool,i64, 0 modes); cpp `>>` (bool,i64, 0 modes)

  - c/op_745 / cpp/op_745 -- **total equality**

### byte-identical group [48 89 f1 89 f8 d3 e8 c3] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `>>` (bool,u64, 0 modes); cpp `>>` (bool,u64, 0 modes)

  - c/op_746 / cpp/op_746 -- **total equality**

### byte-identical group [48 89 f8 48 63 ce 48 29 c8 c3] · (i64,i32)

- ground: cluster
- languages: c, cpp
- members: c `-` (i64,i32, 0 modes); cpp `-` (i64,i32, 0 modes)

  - c/op_144 / cpp/op_144 -- **total equality**

### byte-identical group [48 89 f8 48 63 ce 48 29 c8 c3] · (u64,i32)

- ground: cluster
- languages: c, cpp
- members: c `-` (u64,i32, 0 modes); cpp `-` (u64,i32, 0 modes)

  - c/op_150 / cpp/op_150 -- **total equality**

### byte-identical group [48 89 f8 89 f1 48 29 c8 c3] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `-` (i64,bool, 0 modes); cpp `-` (i64,bool, 0 modes)

  - c/op_149 / cpp/op_149 -- **total equality**

### byte-identical group [48 89 f8 89 f1 48 29 c8 c3] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `-` (u64,bool, 0 modes); cpp `-` (u64,bool, 0 modes)

  - c/op_155 / cpp/op_155 -- **total equality**

### byte-identical group [48 8d 47 01 c3] · (i64,None)

- ground: cluster
- languages: c, cpp
- members: c `++` (i64,None, 0 modes); cpp `++` (i64,None, 0 modes)

  - c/op_37 / cpp/op_49 -- **total equality**

### byte-identical group [48 8d 47 01 c3] · (u64,None)

- ground: cluster
- languages: c, cpp
- members: c `++` (u64,None, 0 modes); cpp `++` (u64,None, 0 modes)

  - c/op_38 / cpp/op_50 -- **total equality**

### byte-identical group [48 8d 47 ff c3] · (i64,None)

- ground: cluster
- languages: c, cpp
- members: c `--` (i64,None, 0 modes); cpp `--` (i64,None, 0 modes)

  - c/op_43 / cpp/op_55 -- **total equality**

### byte-identical group [48 8d 47 ff c3] · (u64,None)

- ground: cluster
- languages: c, cpp
- members: c `--` (u64,None, 0 modes); cpp `--` (u64,None, 0 modes)

  - c/op_44 / cpp/op_56 -- **total equality**

### byte-identical group [66 0f 2e c1 0f 93 c0 c3] · (f64,f64)

- ground: cluster
- languages: cpp, go, rust, swift
- members: cpp `>=` (f64,f64, 0 modes); go `>=` (f64,f64, 0 modes); rust `>=` (f64,f64, 0 modes); swift `>=` (f64,f64, 0 modes)

  - cpp/op_598 / go/op_664 -- **total equality**
  - cpp/op_598 / rust/op_454 -- **total equality**
  - cpp/op_598 / swift/op_430 -- **total equality**
  - go/op_664 / rust/op_454 -- **total equality**
  - go/op_664 / swift/op_430 -- **total equality**
  - rust/op_454 / swift/op_430 -- **total equality**

### byte-identical group [66 0f 2e c1 0f 97 c0 c3] · (f64,f64)

- ground: cluster
- languages: cpp, go, rust, swift
- members: cpp `>` (f64,f64, 0 modes); go `>` (f64,f64, 0 modes); rust `>` (f64,f64, 0 modes); swift `>` (f64,f64, 0 modes)

  - cpp/op_562 / go/op_628 -- **total equality**
  - cpp/op_562 / rust/op_418 -- **total equality**
  - cpp/op_562 / swift/op_358 -- **total equality**
  - go/op_628 / rust/op_418 -- **total equality**
  - go/op_628 / swift/op_358 -- **total equality**
  - rust/op_418 / swift/op_358 -- **total equality**

### byte-identical group [66 0f 2e c8 0f 93 c0 c3] · (f64,f64)

- ground: cluster
- languages: cpp, go, rust, swift
- members: cpp `<=` (f64,f64, 0 modes); go `<=` (f64,f64, 0 modes); rust `<=` (f64,f64, 0 modes); swift `<=` (f64,f64, 0 modes)

  - cpp/op_634 / go/op_592 -- **total equality**
  - cpp/op_634 / rust/op_382 -- **total equality**
  - cpp/op_634 / swift/op_394 -- **total equality**
  - go/op_592 / rust/op_382 -- **total equality**
  - go/op_592 / swift/op_394 -- **total equality**
  - rust/op_382 / swift/op_394 -- **total equality**

### byte-identical group [66 0f 2e c8 0f 97 c0 c3] · (f64,f64)

- ground: cluster
- languages: cpp, go, rust, swift
- members: cpp `<` (f64,f64, 0 modes); go `<` (f64,f64, 0 modes); rust `<` (f64,f64, 0 modes); swift `<` (f64,f64, 0 modes)

  - cpp/op_670 / go/op_556 -- **total equality**
  - cpp/op_670 / rust/op_346 -- **total equality**
  - cpp/op_670 / swift/op_322 -- **total equality**
  - go/op_556 / rust/op_346 -- **total equality**
  - go/op_556 / swift/op_322 -- **total equality**
  - rust/op_346 / swift/op_322 -- **total equality**

### byte-identical group [66 48 0f 6e cf 66 0f 62 0d 00 00 00 00 66 0f 5c 0d 00 00 00 00 66 0f 28 d1 66 0f 15 d1 f2 0f 58 d1 f2 0f 58 c2 c3] · (f64,u64)

- ground: cluster
- languages: c, cpp
- members: c `+` (f64,u64, 0 modes); cpp `+` (f64,u64, 0 modes)

  - c/op_128 / cpp/op_128 -- **total equality**

### byte-identical group [66 48 0f 6e cf 66 0f 62 0d 00 00 00 00 66 0f 5c 0d 00 00 00 00 66 0f 28 d1 66 0f 15 d1 f2 0f 58 d1 f2 0f 58 c2 c3] · (u64,f64)

- ground: cluster
- languages: c, cpp
- members: c `+` (u64,f64, 0 modes); cpp `+` (u64,f64, 0 modes)

  - c/op_118 / cpp/op_118 -- **total equality**

### byte-identical group [66 48 0f 6e cf 66 0f 62 0d 00 00 00 00 66 0f 5c 0d 00 00 00 00 66 0f 28 d1 66 0f 15 d1 f2 0f 58 d1 f2 0f 59 c2 c3] · (f64,u64)

- ground: cluster
- languages: c, cpp
- members: c `*` (f64,u64, 0 modes); cpp `*` (f64,u64, 0 modes)

  - c/op_200 / cpp/op_200 -- **total equality**

### byte-identical group [66 48 0f 6e cf 66 0f 62 0d 00 00 00 00 66 0f 5c 0d 00 00 00 00 66 0f 28 d1 66 0f 15 d1 f2 0f 58 d1 f2 0f 59 c2 c3] · (u64,f64)

- ground: cluster
- languages: c, cpp
- members: c `*` (u64,f64, 0 modes); cpp `*` (u64,f64, 0 modes)

  - c/op_190 / cpp/op_190 -- **total equality**

### byte-identical group [66 48 0f 6e cf 66 0f 62 0d 00 00 00 00 66 0f 5c 0d 00 00 00 00 66 0f 28 d1 66 0f 15 d1 f2 0f 58 d1 f2 0f c2 d0 00 66 48 0f 7e d0 83 e0 01 c3] · (f64,u64)

- ground: cluster
- languages: c, cpp
- members: c `==` (f64,u64, 0 modes); cpp `==` (f64,u64, 0 modes)

  - c/op_488 / cpp/op_488 -- **total equality**

### byte-identical group [66 48 0f 6e cf 66 0f 62 0d 00 00 00 00 66 0f 5c 0d 00 00 00 00 66 0f 28 d1 66 0f 15 d1 f2 0f 58 d1 f2 0f c2 d0 00 66 48 0f 7e d0 83 e0 01 c3] · (u64,f64)

- ground: cluster
- languages: c, cpp
- members: c `==` (u64,f64, 0 modes); cpp `==` (u64,f64, 0 modes)

  - c/op_478 / cpp/op_478 -- **total equality**

### byte-identical group [89 f0 48 01 f8 c3] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `+` (i64,bool, 0 modes); cpp `+` (i64,bool, 0 modes)

  - c/op_113 / cpp/op_113 -- **total equality**

### byte-identical group [89 f0 48 01 f8 c3] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `+` (u64,bool, 0 modes); cpp `+` (u64,bool, 0 modes)

  - c/op_119 / cpp/op_119 -- **total equality**

### byte-identical group [89 f1 89 f8 d3 e8 c3] · (bool,bool)

- ground: cluster
- languages: c, cpp
- members: c `>>` (bool,bool, 0 modes); cpp `>>` (bool,bool, 0 modes)

  - c/op_749 / cpp/op_749 -- **total equality**

### byte-identical group [89 f1 89 f8 d3 e8 c3] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `>>` (bool,i32, 0 modes); cpp `>>` (bool,i32, 0 modes)

  - c/op_744 / cpp/op_744 -- **total equality**

### byte-identical group [89 f8 48 01 f0 c3] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `+` (bool,i64, 0 modes); cpp `+` (bool,i64, 0 modes)

  - c/op_133 / cpp/op_133 -- **total equality**

### byte-identical group [89 f8 48 01 f0 c3] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `+` (bool,u64, 0 modes); cpp `+` (bool,u64, 0 modes)

  - c/op_134 / cpp/op_134 -- **total equality**

### byte-identical group [89 f8 48 29 f0 c3] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `-` (bool,i64, 0 modes); cpp `-` (bool,i64, 0 modes)

  - c/op_169 / cpp/op_169 -- **total equality**

### byte-identical group [89 f8 48 29 f0 c3] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `-` (bool,u64, 0 modes); cpp `-` (bool,u64, 0 modes)

  - c/op_170 / cpp/op_170 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f 5c c1 c3] · (f64,bool)

- ground: cluster
- languages: c, cpp
- members: c `-` (f64,bool, 0 modes); cpp `-` (f64,bool, 0 modes)

  - c/op_167 / cpp/op_167 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f 5c c1 c3] · (f64,i32)

- ground: cluster
- languages: c, cpp
- members: c `-` (f64,i32, 0 modes); cpp `-` (f64,i32, 0 modes)

  - c/op_162 / cpp/op_162 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f 5c c8 66 0f 28 c1 c3] · (bool,f64)

- ground: cluster
- languages: c, cpp
- members: c `-` (bool,f64, 0 modes); cpp `-` (bool,f64, 0 modes)

  - c/op_172 / cpp/op_172 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f 5c c8 66 0f 28 c1 c3] · (i32,f64)

- ground: cluster
- languages: c, cpp
- members: c `-` (i32,f64, 0 modes); cpp `-` (i32,f64, 0 modes)

  - c/op_142 / cpp/op_142 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f 5e c1 c3] · (f64,bool)

- ground: cluster
- languages: c, cpp
- members: c `/` (f64,bool, 0 modes); cpp `/` (f64,bool, 0 modes)

  - c/op_239 / cpp/op_239 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f 5e c1 c3] · (f64,i32)

- ground: cluster
- languages: c, cpp
- members: c `/` (f64,i32, 0 modes); cpp `/` (f64,i32, 0 modes)

  - c/op_234 / cpp/op_234 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f 5e c8 66 0f 28 c1 c3] · (bool,f64)

- ground: cluster
- languages: c, cpp
- members: c `/` (bool,f64, 0 modes); cpp `/` (bool,f64, 0 modes)

  - c/op_244 / cpp/op_244 -- **total equality**

### byte-identical group [f2 0f 2a cf f2 0f 5e c8 66 0f 28 c1 c3] · (i32,f64)

- ground: cluster
- languages: c, cpp
- members: c `/` (i32,f64, 0 modes); cpp `/` (i32,f64, 0 modes)

  - c/op_214 / cpp/op_214 -- **total equality**

### byte-identical group [f2 0f 58 05 00 00 00 00 c3] · (f64,None)

- ground: cluster
- languages: c, cpp
- members: c `++` (f64,None, 0 modes); c `--` (f64,None, 0 modes); cpp `++` (f64,None, 0 modes); cpp `--` (f64,None, 0 modes)

  - c/op_40 / cpp/op_52 -- **total equality**
  - c/op_40 / cpp/op_58 -- **total equality**
  - c/op_46 / cpp/op_52 -- **total equality**
  - c/op_46 / cpp/op_58 -- **total equality**

### byte-identical group [f2 0f c2 c1 00 66 48 0f 7e c0 83 e0 01 c3] · (f64,f64)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `==` (f64,f64, 0 modes); cpp `==` (f64,f64, 0 modes); rust `==` (f64,f64, 0 modes); swift `==` (f64,f64, 0 modes)

  - c/op_490 / cpp/op_490 -- **total equality**
  - c/op_490 / rust/op_274 -- **total equality**
  - c/op_490 / swift/op_538 -- **total equality**
  - cpp/op_490 / rust/op_274 -- **total equality**
  - cpp/op_490 / swift/op_538 -- **total equality**
  - rust/op_274 / swift/op_538 -- **total equality**

### byte-identical group [f2 48 0f 2a cf f2 0f 58 c1 c3] · (f64,i64)

- ground: cluster
- languages: c, cpp
- members: c `+` (f64,i64, 0 modes); cpp `+` (f64,i64, 0 modes)

  - c/op_127 / cpp/op_127 -- **total equality**

### byte-identical group [f2 48 0f 2a cf f2 0f 58 c1 c3] · (i64,f64)

- ground: cluster
- languages: c, cpp
- members: c `+` (i64,f64, 0 modes); cpp `+` (i64,f64, 0 modes)

  - c/op_112 / cpp/op_112 -- **total equality**

### byte-identical group [f2 48 0f 2a cf f2 0f 59 c1 c3] · (f64,i64)

- ground: cluster
- languages: c, cpp
- members: c `*` (f64,i64, 0 modes); cpp `*` (f64,i64, 0 modes)

  - c/op_199 / cpp/op_199 -- **total equality**

### byte-identical group [f2 48 0f 2a cf f2 0f 59 c1 c3] · (i64,f64)

- ground: cluster
- languages: c, cpp
- members: c `*` (i64,f64, 0 modes); cpp `*` (i64,f64, 0 modes)

  - c/op_184 / cpp/op_184 -- **total equality**

### byte-identical group [f2 48 0f 2a cf f2 0f c2 c8 00 66 48 0f 7e c8 83 e0 01 c3] · (f64,i64)

- ground: cluster
- languages: c, cpp
- members: c `==` (f64,i64, 0 modes); cpp `==` (f64,i64, 0 modes)

  - c/op_487 / cpp/op_487 -- **total equality**

### byte-identical group [f2 48 0f 2a cf f2 0f c2 c8 00 66 48 0f 7e c8 83 e0 01 c3] · (i64,f64)

- ground: cluster
- languages: c, cpp
- members: c `==` (i64,f64, 0 modes); cpp `==` (i64,f64, 0 modes)

  - c/op_472 / cpp/op_472 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f 5c c1 c3] · (f32,bool)

- ground: cluster
- languages: c, cpp
- members: c `-` (f32,bool, 0 modes); cpp `-` (f32,bool, 0 modes)

  - c/op_161 / cpp/op_161 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f 5c c1 c3] · (f32,i32)

- ground: cluster
- languages: c, cpp
- members: c `-` (f32,i32, 0 modes); cpp `-` (f32,i32, 0 modes)

  - c/op_156 / cpp/op_156 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f 5c c8 0f 28 c1 c3] · (bool,f32)

- ground: cluster
- languages: c, cpp
- members: c `-` (bool,f32, 0 modes); cpp `-` (bool,f32, 0 modes)

  - c/op_171 / cpp/op_171 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f 5c c8 0f 28 c1 c3] · (i32,f32)

- ground: cluster
- languages: c, cpp
- members: c `-` (i32,f32, 0 modes); cpp `-` (i32,f32, 0 modes)

  - c/op_141 / cpp/op_141 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f 5e c1 c3] · (f32,bool)

- ground: cluster
- languages: c, cpp
- members: c `/` (f32,bool, 0 modes); cpp `/` (f32,bool, 0 modes)

  - c/op_233 / cpp/op_233 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f 5e c1 c3] · (f32,i32)

- ground: cluster
- languages: c, cpp
- members: c `/` (f32,i32, 0 modes); cpp `/` (f32,i32, 0 modes)

  - c/op_228 / cpp/op_228 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f 5e c8 0f 28 c1 c3] · (bool,f32)

- ground: cluster
- languages: c, cpp
- members: c `/` (bool,f32, 0 modes); cpp `/` (bool,f32, 0 modes)

  - c/op_243 / cpp/op_243 -- **total equality**

### byte-identical group [f3 0f 2a cf f3 0f 5e c8 0f 28 c1 c3] · (i32,f32)

- ground: cluster
- languages: c, cpp
- members: c `/` (i32,f32, 0 modes); cpp `/` (i32,f32, 0 modes)

  - c/op_213 / cpp/op_213 -- **total equality**

### byte-identical group [f3 0f 58 05 00 00 00 00 c3] · (f32,None)

- ground: cluster
- languages: c, cpp
- members: c `++` (f32,None, 0 modes); c `--` (f32,None, 0 modes); cpp `++` (f32,None, 0 modes); cpp `--` (f32,None, 0 modes)

  - c/op_39 / cpp/op_51 -- **total equality**
  - c/op_39 / cpp/op_57 -- **total equality**
  - c/op_45 / cpp/op_51 -- **total equality**
  - c/op_45 / cpp/op_57 -- **total equality**

### byte-identical group [f3 0f c2 c1 00 66 0f 7e c0 83 e0 01 c3] · (f32,f32)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `==` (f32,f32, 0 modes); cpp `==` (f32,f32, 0 modes); rust `==` (f32,f32, 0 modes); swift `==` (f32,f32, 0 modes)

  - c/op_483 / cpp/op_483 -- **total equality**
  - c/op_483 / rust/op_267 -- **total equality**
  - c/op_483 / swift/op_531 -- **total equality**
  - cpp/op_483 / rust/op_267 -- **total equality**
  - cpp/op_483 / swift/op_531 -- **total equality**
  - rust/op_267 / swift/op_531 -- **total equality**

### byte-identical group [f3 48 0f 2a cf f3 0f 58 c1 c3] · (f32,i64)

- ground: cluster
- languages: c, cpp
- members: c `+` (f32,i64, 0 modes); cpp `+` (f32,i64, 0 modes)

  - c/op_121 / cpp/op_121 -- **total equality**

### byte-identical group [f3 48 0f 2a cf f3 0f 58 c1 c3] · (i64,f32)

- ground: cluster
- languages: c, cpp
- members: c `+` (i64,f32, 0 modes); cpp `+` (i64,f32, 0 modes)

  - c/op_111 / cpp/op_111 -- **total equality**

### byte-identical group [f3 48 0f 2a cf f3 0f 59 c1 c3] · (f32,i64)

- ground: cluster
- languages: c, cpp
- members: c `*` (f32,i64, 0 modes); cpp `*` (f32,i64, 0 modes)

  - c/op_193 / cpp/op_193 -- **total equality**

### byte-identical group [f3 48 0f 2a cf f3 0f 59 c1 c3] · (i64,f32)

- ground: cluster
- languages: c, cpp
- members: c `*` (i64,f32, 0 modes); cpp `*` (i64,f32, 0 modes)

  - c/op_183 / cpp/op_183 -- **total equality**

### byte-identical group [f3 48 0f 2a cf f3 0f c2 c8 00 66 0f 7e c8 83 e0 01 c3] · (f32,i64)

- ground: cluster
- languages: c, cpp
- members: c `==` (f32,i64, 0 modes); cpp `==` (f32,i64, 0 modes)

  - c/op_481 / cpp/op_481 -- **total equality**

### byte-identical group [f3 48 0f 2a cf f3 0f c2 c8 00 66 0f 7e c8 83 e0 01 c3] · (i64,f32)

- ground: cluster
- languages: c, cpp
- members: c `==` (i64,f32, 0 modes); cpp `==` (i64,f32, 0 modes)

  - c/op_471 / cpp/op_471 -- **total equality**

### byte-identical group [0f 57 c9 f3 0f c2 c8 00 66 0f 7e c8 83 e0 01 c3] · (f32,None)

- ground: cluster
- languages: c, cpp
- members: c `!` (f32,None, 0 modes); cpp `!` (f32,None, 0 modes); cpp `not` (f32,None, 0 modes)

  - c/op_3 / cpp/op_3 -- **total equality**
  - c/op_3 / cpp/op_27 -- **total equality**

### byte-identical group [39 f7 0f 9e c0 c3] · (i32,i32)

- ground: cluster
- languages: cpp, rust
- members: cpp `<=` (i32,i32, 0 modes); rust `<=` (i32,i32, 0 modes)

  - cpp/op_606 / rust/op_354 -- **total equality**

### byte-identical group [39 f7 0f 9f c0 c3] · (i32,i32)

- ground: cluster
- languages: cpp, rust
- members: cpp `>` (i32,i32, 0 modes); rust `>` (i32,i32, 0 modes)

  - cpp/op_534 / rust/op_390 -- **total equality**

### byte-identical group [48 39 f7 0f 9c c0 c3] · (i64,i64)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `<` (i64,i64, 0 modes); rust `<` (i64,i64, 0 modes); swift `<` (i64,i64, 0 modes)

  - cpp/op_649 / rust/op_325 -- **total equality**
  - cpp/op_649 / swift/op_301 -- **total equality**
  - rust/op_325 / swift/op_301 -- **total equality**

### byte-identical group [48 39 f7 0f 9d c0 c3] · (i64,i64)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `>=` (i64,i64, 0 modes); rust `>=` (i64,i64, 0 modes); swift `>=` (i64,i64, 0 modes)

  - cpp/op_577 / rust/op_433 -- **total equality**
  - cpp/op_577 / swift/op_409 -- **total equality**
  - rust/op_433 / swift/op_409 -- **total equality**

### byte-identical group [66 0f 57 c9 f2 0f c2 c8 00 66 48 0f 7e c8 83 e0 01 c3] · (f64,None)

- ground: cluster
- languages: c, cpp
- members: c `!` (f64,None, 0 modes); cpp `!` (f64,None, 0 modes); cpp `not` (f64,None, 0 modes)

  - c/op_4 / cpp/op_4 -- **total equality**
  - c/op_4 / cpp/op_28 -- **total equality**

### byte-identical group [89 f8 0f af c6 c3] · (i32,i32)

- ground: cluster
- languages: c, cpp, rust
- members: c `*` (i32,i32, 1 modes); cpp `*` (i32,i32, 1 modes); rust `*` (i32,i32, 1 modes)

  - c/op_174 / cpp/op_174 -- **total equality**
  - c/op_174 / rust/op_606 -- **total equality**
  - cpp/op_174 / rust/op_606 -- **total equality**

### byte-identical group [89 f8 31 f0 34 01 c3] · (bool,bool)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `==` (bool,bool, 0 modes); rust `==` (bool,bool, 0 modes); swift `==` (bool,bool, 0 modes)

  - cpp/op_497 / rust/op_281 -- **total equality**
  - cpp/op_497 / swift/op_545 -- **total equality**
  - rust/op_281 / swift/op_545 -- **total equality**

### byte-identical group [f3 0f 5a c0 f2 0f c2 c1 04 66 48 0f 7e c0 83 e0 01 c3] · (f32,f64)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f32,f64, 0 modes); cpp `!=` (f32,f64, 0 modes); cpp `not_eq` (f32,f64, 0 modes)

  - c/op_520 / cpp/op_520 -- **total equality**
  - c/op_520 / cpp/op_988 -- **total equality**

### byte-identical group [f3 0f 5a c9 f2 0f c2 c8 04 66 48 0f 7e c8 83 e0 01 c3] · (f64,f32)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f64,f32, 0 modes); cpp `!=` (f64,f32, 0 modes); cpp `not_eq` (f64,f32, 0 modes)

  - c/op_525 / cpp/op_525 -- **total equality**
  - c/op_525 / cpp/op_993 -- **total equality**

### byte-identical group [40 88 7c 24 ff 48 8d 44 24 ff c3] · (bool,None)

- ground: cluster
- languages: c, cpp
- members: c `&` (bool,None, 0 modes); cpp `&` (bool,None, 0 modes)

  - c/op_35 / cpp/op_47 -- **total equality**

### byte-identical group [48 39 f7 0f 9e c0 c3] · (i64,i64)

- ground: cluster
- languages: cpp, rust
- members: cpp `<=` (i64,i64, 0 modes); rust `<=` (i64,i64, 0 modes)

  - cpp/op_613 / rust/op_361 -- **total equality**

### byte-identical group [48 39 f7 0f 9f c0 c3] · (i64,i64)

- ground: cluster
- languages: cpp, rust
- members: cpp `>` (i64,i64, 0 modes); rust `>` (i64,i64, 0 modes)

  - cpp/op_541 / rust/op_397 -- **total equality**

### byte-identical group [48 63 c7 31 d2 48 f7 f6 48 89 d0 c3] · (i32,u64)

- ground: cluster
- languages: c, cpp
- members: c `%` (i32,u64, 0 modes); cpp `%` (i32,u64, 0 modes)

  - c/op_248 / cpp/op_248 -- **total equality**

### byte-identical group [48 63 c7 31 d2 48 f7 f6 c3] · (i32,u64)

- ground: cluster
- languages: c, cpp
- members: c `/` (i32,u64, 0 modes); cpp `/` (i32,u64, 0 modes)

  - c/op_212 / cpp/op_212 -- **total equality**

### byte-identical group [48 63 c7 48 99 48 f7 fe 48 89 d0 c3] · (i32,i64)

- ground: cluster
- languages: c, cpp
- members: c `%` (i32,i64, 0 modes); cpp `%` (i32,i64, 0 modes)

  - c/op_247 / cpp/op_247 -- **total equality**

### byte-identical group [48 63 c7 48 99 48 f7 fe c3] · (i32,i64)

- ground: cluster
- languages: c, cpp
- members: c `/` (i32,i64, 0 modes); cpp `/` (i32,i64, 0 modes)

  - c/op_211 / cpp/op_211 -- **total equality**

### byte-identical group [48 85 ff 78 07 f3 48 0f 2a cf eb 15 48 89 f8 48 d1 e8 83 e7 01 48 09 c7 f3 48 0f 2a cf f3 0f 58 c9 f3 0f 5c c8 0f 28 c1 c3] · (u64,f32)

- ground: cluster
- languages: c, cpp
- members: c `-` (u64,f32, 0 modes); cpp `-` (u64,f32, 0 modes)

  - c/op_153 / cpp/op_153 -- **total equality**

### byte-identical group [48 85 ff 78 07 f3 48 0f 2a cf eb 15 48 89 f8 48 d1 e8 83 e7 01 48 09 c7 f3 48 0f 2a cf f3 0f 58 c9 f3 0f 5e c8 0f 28 c1 c3] · (u64,f32)

- ground: cluster
- languages: c, cpp
- members: c `/` (u64,f32, 0 modes); cpp `/` (u64,f32, 0 modes)

  - c/op_225 / cpp/op_225 -- **total equality**

### byte-identical group [48 85 ff 78 0a f3 48 0f 2a cf f3 0f 5c c1 c3 48 89 f8 48 d1 e8 83 e7 01 48 09 c7 f3 48 0f 2a cf f3 0f 58 c9 f3 0f 5c c1 c3] · (f32,u64)

- ground: cluster
- languages: c, cpp
- members: c `-` (f32,u64, 0 modes); cpp `-` (f32,u64, 0 modes)

  - c/op_158 / cpp/op_158 -- **total equality**

### byte-identical group [48 85 ff 78 0a f3 48 0f 2a cf f3 0f 5e c1 c3 48 89 f8 48 d1 e8 83 e7 01 48 09 c7 f3 48 0f 2a cf f3 0f 58 c9 f3 0f 5e c1 c3] · (f32,u64)

- ground: cluster
- languages: c, cpp
- members: c `/` (f32,u64, 0 modes); cpp `/` (f32,u64, 0 modes)

  - c/op_230 / cpp/op_230 -- **total equality**

### byte-identical group [48 89 f8 48 63 ce 31 d2 48 f7 f1 48 89 d0 c3] · (u64,i32)

- ground: cluster
- languages: c, cpp
- members: c `%` (u64,i32, 0 modes); cpp `%` (u64,i32, 0 modes)

  - c/op_258 / cpp/op_258 -- **total equality**

### byte-identical group [48 89 f8 48 63 ce 31 d2 48 f7 f1 c3] · (u64,i32)

- ground: cluster
- languages: c, cpp
- members: c `/` (u64,i32, 0 modes); cpp `/` (u64,i32, 0 modes)

  - c/op_222 / cpp/op_222 -- **total equality**

### byte-identical group [48 89 f8 48 63 ce 48 99 48 f7 f9 48 89 d0 c3] · (i64,i32)

- ground: cluster
- languages: c, cpp
- members: c `%` (i64,i32, 0 modes); cpp `%` (i64,i32, 0 modes)

  - c/op_252 / cpp/op_252 -- **total equality**

### byte-identical group [48 89 f8 48 63 ce 48 99 48 f7 f9 c3] · (i64,i32)

- ground: cluster
- languages: c, cpp
- members: c `/` (i64,i32, 0 modes); cpp `/` (i64,i32, 0 modes)

  - c/op_216 / cpp/op_216 -- **total equality**

### byte-identical group [48 89 f8 48 99 48 f7 fe 48 89 d0 c3] · (i64,i64)

- ground: cluster
- languages: c, cpp
- members: c `%` (i64,i64, 0 modes); cpp `%` (i64,i64, 0 modes)

  - c/op_253 / cpp/op_253 -- **total equality**

### byte-identical group [48 89 f8 48 99 48 f7 fe c3] · (i64,i64)

- ground: cluster
- languages: c, cpp
- members: c `/` (i64,i64, 0 modes); cpp `/` (i64,i64, 0 modes)

  - c/op_217 / cpp/op_217 -- **total equality**

### byte-identical group [66 48 0f 6e cf 66 0f 62 0d 00 00 00 00 66 0f 5c 0d 00 00 00 00 66 0f 28 d1 66 0f 15 d1 f2 0f 58 d1 f2 0f 5c c2 c3] · (f64,u64)

- ground: cluster
- languages: c, cpp
- members: c `-` (f64,u64, 0 modes); cpp `-` (f64,u64, 0 modes)

  - c/op_164 / cpp/op_164 -- **total equality**

### byte-identical group [66 48 0f 6e cf 66 0f 62 0d 00 00 00 00 66 0f 5c 0d 00 00 00 00 66 0f 28 d1 66 0f 15 d1 f2 0f 58 d1 f2 0f 5e c2 c3] · (f64,u64)

- ground: cluster
- languages: c, cpp
- members: c `/` (f64,u64, 0 modes); cpp `/` (f64,u64, 0 modes)

  - c/op_236 / cpp/op_236 -- **total equality**

### byte-identical group [66 48 0f 6e d7 66 0f 62 15 00 00 00 00 66 0f 5c 15 00 00 00 00 66 0f 28 ca 66 0f 15 ca f2 0f 58 ca f2 0f 5c c8 66 0f 28 c1 c3] · (u64,f64)

- ground: cluster
- languages: c, cpp
- members: c `-` (u64,f64, 0 modes); cpp `-` (u64,f64, 0 modes)

  - c/op_154 / cpp/op_154 -- **total equality**

### byte-identical group [66 48 0f 6e d7 66 0f 62 15 00 00 00 00 66 0f 5c 15 00 00 00 00 66 0f 28 ca 66 0f 15 ca f2 0f 58 ca f2 0f 5e c8 66 0f 28 c1 c3] · (u64,f64)

- ground: cluster
- languages: c, cpp
- members: c `/` (u64,f64, 0 modes); cpp `/` (u64,f64, 0 modes)

  - c/op_226 / cpp/op_226 -- **total equality**

### byte-identical group [89 7c 24 fc 48 8d 44 24 fc c3] · (i32,None)

- ground: cluster
- languages: c, cpp
- members: c `&` (i32,None, 0 modes); cpp `&` (i32,None, 0 modes)

  - c/op_30 / cpp/op_42 -- **total equality**

### byte-identical group [89 f0 34 01 40 08 f8 c3] · (bool,bool)

- ground: cluster
- languages: cpp, rust
- members: cpp `>=` (bool,bool, 1 modes); rust `>=` (bool,bool, 1 modes)

  - cpp/op_605 / rust/op_461 -- **total equality**

### byte-identical group [89 f0 34 01 40 20 f8 c3] · (bool,bool)

- ground: cluster
- languages: cpp, rust
- members: cpp `>` (bool,bool, 1 modes); rust `>` (bool,bool, 1 modes)

  - cpp/op_569 / rust/op_425 -- **total equality**

### byte-identical group [89 f0 85 ff 0f 44 c7 c3] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `*` (bool,i32, 0 modes); cpp `*` (bool,i32, 0 modes)

  - c/op_204 / cpp/op_204 -- **total equality**

### byte-identical group [89 f8 31 d2 48 f7 f6 48 89 d0 c3] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `%` (bool,u64, 0 modes); cpp `%` (bool,u64, 0 modes)

  - c/op_278 / cpp/op_278 -- **total equality**

### byte-identical group [89 f8 31 d2 48 f7 f6 c3] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `/` (bool,u64, 0 modes); cpp `/` (bool,u64, 0 modes)

  - c/op_242 / cpp/op_242 -- **total equality**

### byte-identical group [89 f8 31 d2 48 f7 fe 48 89 d0 c3] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `%` (bool,i64, 0 modes); cpp `%` (bool,i64, 0 modes)

  - c/op_277 / cpp/op_277 -- **total equality**

### byte-identical group [89 f8 31 d2 48 f7 fe c3] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `/` (bool,i64, 0 modes); cpp `/` (bool,i64, 0 modes)

  - c/op_241 / cpp/op_241 -- **total equality**

### byte-identical group [89 f8 31 d2 f7 fe 89 d0 c3] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `%` (bool,i32, 0 modes); cpp `%` (bool,i32, 0 modes)

  - c/op_276 / cpp/op_276 -- **total equality**

### byte-identical group [89 f8 31 d2 f7 fe c3] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `/` (bool,i32, 0 modes); cpp `/` (bool,i32, 0 modes)

  - c/op_240 / cpp/op_240 -- **total equality**

### byte-identical group [89 f8 34 01 40 08 f0 c3] · (bool,bool)

- ground: cluster
- languages: cpp, rust
- members: cpp `<=` (bool,bool, 1 modes); rust `<=` (bool,bool, 1 modes)

  - cpp/op_641 / rust/op_389 -- **total equality**

### byte-identical group [89 f8 34 01 40 20 f0 c3] · (bool,bool)

- ground: cluster
- languages: cpp, rust
- members: cpp `<` (bool,bool, 1 modes); rust `<` (bool,bool, 1 modes)

  - cpp/op_677 / rust/op_353 -- **total equality**

### byte-identical group [89 f8 85 f6 0f 44 c6 c3] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `*` (i32,bool, 0 modes); cpp `*` (i32,bool, 0 modes)

  - c/op_179 / cpp/op_179 -- **total equality**

### byte-identical group [89 f8 99 f7 fe 89 d0 c3] · (i32,i32)

- ground: cluster
- languages: c, cpp
- members: c `%` (i32,i32, 0 modes); cpp `%` (i32,i32, 0 modes)

  - c/op_246 / cpp/op_246 -- **total equality**

### byte-identical group [89 f8 99 f7 fe c3] · (i32,i32)

- ground: cluster
- languages: c, cpp
- members: c `/` (i32,i32, 0 modes); cpp `/` (i32,i32, 0 modes)

  - c/op_210 / cpp/op_210 -- **total equality**

### byte-identical group [8d 47 01 c3] · (i32,None)

- ground: cluster
- languages: c, cpp
- members: c `++` (i32,None, 0 modes); cpp `++` (i32,None, 0 modes)

  - c/op_36 / cpp/op_48 -- **total equality**

### byte-identical group [8d 47 ff c3] · (i32,None)

- ground: cluster
- languages: c, cpp
- members: c `--` (i32,None, 0 modes); cpp `--` (i32,None, 0 modes)

  - c/op_42 / cpp/op_54 -- **total equality**

### byte-identical group [f2 0f 11 44 24 f8 48 8d 44 24 f8 c3] · (f64,None)

- ground: cluster
- languages: c, cpp
- members: c `&` (f64,None, 0 modes); cpp `&` (f64,None, 0 modes)

  - c/op_34 / cpp/op_46 -- **total equality**

### byte-identical group [f2 48 0f 2a cf f2 0f 5c c1 c3] · (f64,i64)

- ground: cluster
- languages: c, cpp
- members: c `-` (f64,i64, 0 modes); cpp `-` (f64,i64, 0 modes)

  - c/op_163 / cpp/op_163 -- **total equality**

### byte-identical group [f2 48 0f 2a cf f2 0f 5c c8 66 0f 28 c1 c3] · (i64,f64)

- ground: cluster
- languages: c, cpp
- members: c `-` (i64,f64, 0 modes); cpp `-` (i64,f64, 0 modes)

  - c/op_148 / cpp/op_148 -- **total equality**

### byte-identical group [f2 48 0f 2a cf f2 0f 5e c1 c3] · (f64,i64)

- ground: cluster
- languages: c, cpp
- members: c `/` (f64,i64, 0 modes); cpp `/` (f64,i64, 0 modes)

  - c/op_235 / cpp/op_235 -- **total equality**

### byte-identical group [f2 48 0f 2a cf f2 0f 5e c8 66 0f 28 c1 c3] · (i64,f64)

- ground: cluster
- languages: c, cpp
- members: c `/` (i64,f64, 0 modes); cpp `/` (i64,f64, 0 modes)

  - c/op_220 / cpp/op_220 -- **total equality**

### byte-identical group [f3 0f 11 44 24 fc 48 8d 44 24 fc c3] · (f32,None)

- ground: cluster
- languages: c, cpp
- members: c `&` (f32,None, 0 modes); cpp `&` (f32,None, 0 modes)

  - c/op_33 / cpp/op_45 -- **total equality**

### byte-identical group [f3 0f 5a c0 f2 0f 58 c1 c3] · (f32,f64)

- ground: cluster
- languages: c, cpp
- members: c `+` (f32,f64, 0 modes); cpp `+` (f32,f64, 0 modes)

  - c/op_124 / cpp/op_124 -- **total equality**

### byte-identical group [f3 0f 5a c0 f2 0f 59 c1 c3] · (f32,f64)

- ground: cluster
- languages: c, cpp
- members: c `*` (f32,f64, 0 modes); cpp `*` (f32,f64, 0 modes)

  - c/op_196 / cpp/op_196 -- **total equality**

### byte-identical group [f3 0f 5a c0 f2 0f 5c c1 c3] · (f32,f64)

- ground: cluster
- languages: c, cpp
- members: c `-` (f32,f64, 0 modes); cpp `-` (f32,f64, 0 modes)

  - c/op_160 / cpp/op_160 -- **total equality**

### byte-identical group [f3 0f 5a c0 f2 0f 5e c1 c3] · (f32,f64)

- ground: cluster
- languages: c, cpp
- members: c `/` (f32,f64, 0 modes); cpp `/` (f32,f64, 0 modes)

  - c/op_232 / cpp/op_232 -- **total equality**

### byte-identical group [f3 0f 5a c0 f2 0f c2 c1 00 66 48 0f 7e c0 83 e0 01 c3] · (f32,f64)

- ground: cluster
- languages: c, cpp
- members: c `==` (f32,f64, 0 modes); cpp `==` (f32,f64, 0 modes)

  - c/op_484 / cpp/op_484 -- **total equality**

### byte-identical group [f3 0f 5a c9 f2 0f 58 c1 c3] · (f64,f32)

- ground: cluster
- languages: c, cpp
- members: c `+` (f64,f32, 0 modes); cpp `+` (f64,f32, 0 modes)

  - c/op_129 / cpp/op_129 -- **total equality**

### byte-identical group [f3 0f 5a c9 f2 0f 59 c1 c3] · (f64,f32)

- ground: cluster
- languages: c, cpp
- members: c `*` (f64,f32, 0 modes); cpp `*` (f64,f32, 0 modes)

  - c/op_201 / cpp/op_201 -- **total equality**

### byte-identical group [f3 0f 5a c9 f2 0f 5c c1 c3] · (f64,f32)

- ground: cluster
- languages: c, cpp
- members: c `-` (f64,f32, 0 modes); cpp `-` (f64,f32, 0 modes)

  - c/op_165 / cpp/op_165 -- **total equality**

### byte-identical group [f3 0f 5a c9 f2 0f 5e c1 c3] · (f64,f32)

- ground: cluster
- languages: c, cpp
- members: c `/` (f64,f32, 0 modes); cpp `/` (f64,f32, 0 modes)

  - c/op_237 / cpp/op_237 -- **total equality**

### byte-identical group [f3 0f 5a c9 f2 0f c2 c8 00 66 48 0f 7e c8 83 e0 01 c3] · (f64,f32)

- ground: cluster
- languages: c, cpp
- members: c `==` (f64,f32, 0 modes); cpp `==` (f64,f32, 0 modes)

  - c/op_489 / cpp/op_489 -- **total equality**

### byte-identical group [f3 48 0f 2a cf f3 0f 5c c1 c3] · (f32,i64)

- ground: cluster
- languages: c, cpp
- members: c `-` (f32,i64, 0 modes); cpp `-` (f32,i64, 0 modes)

  - c/op_157 / cpp/op_157 -- **total equality**

### byte-identical group [f3 48 0f 2a cf f3 0f 5c c8 0f 28 c1 c3] · (i64,f32)

- ground: cluster
- languages: c, cpp
- members: c `-` (i64,f32, 0 modes); cpp `-` (i64,f32, 0 modes)

  - c/op_147 / cpp/op_147 -- **total equality**

### byte-identical group [f3 48 0f 2a cf f3 0f 5e c1 c3] · (f32,i64)

- ground: cluster
- languages: c, cpp
- members: c `/` (f32,i64, 0 modes); cpp `/` (f32,i64, 0 modes)

  - c/op_229 / cpp/op_229 -- **total equality**

### byte-identical group [f3 48 0f 2a cf f3 0f 5e c8 0f 28 c1 c3] · (i64,f32)

- ground: cluster
- languages: c, cpp
- members: c `/` (i64,f32, 0 modes); cpp `/` (i64,f32, 0 modes)

  - c/op_219 / cpp/op_219 -- **total equality**

### sem-identical group B0 V[zx64(And32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (bool,bool)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `*` (bool,bool, 0 modes); c `&&` (bool,bool, 0 modes); c `&` (bool,bool, 0 modes); cpp `*` (bool,bool, 0 modes); cpp `&&` (bool,bool, 0 modes); cpp `&` (bool,bool, 0 modes); cpp `and` (bool,bool, 0 modes); cpp `bitand` (bool,bool, 0 modes); go `&&` (bool,bool, 0 modes); rust `&&` (bool,bool, 0 modes); rust `&` (bool,bool, 0 modes); swift `&&` (bool,bool, 0 modes)

  - c/op_209 / cpp/op_209 -- **total equality**
  - c/op_209 / cpp/op_353 -- **total equality**
  - c/op_209 / cpp/op_461 -- **total equality**
  - c/op_209 / cpp/op_857 -- **total equality**
  - c/op_209 / cpp/op_965 -- **total equality**
  - c/op_353 / cpp/op_209 -- **total equality**
  - c/op_353 / cpp/op_353 -- **total equality**
  - c/op_353 / cpp/op_461 -- **total equality**
  - c/op_353 / cpp/op_857 -- **total equality**
  - c/op_353 / cpp/op_965 -- **total equality**
  - c/op_461 / cpp/op_209 -- **total equality**
  - c/op_461 / cpp/op_353 -- **total equality**
  - c/op_461 / cpp/op_461 -- **total equality**
  - c/op_461 / cpp/op_857 -- **total equality**
  - c/op_461 / cpp/op_965 -- **total equality**
  - c/op_209 / go/op_707 -- **total equality**
  - c/op_353 / go/op_707 -- **total equality**
  - c/op_461 / go/op_707 -- **total equality**
  - c/op_209 / rust/op_101 -- **total equality**
  - c/op_209 / rust/op_173 -- **total equality**
  - c/op_353 / rust/op_101 -- **total equality**
  - c/op_353 / rust/op_173 -- **total equality**
  - c/op_461 / rust/op_101 -- **total equality**
  - c/op_461 / rust/op_173 -- **total equality**
  - c/op_209 / swift/op_797 -- **total equality**
  - c/op_353 / swift/op_797 -- **total equality**
  - c/op_461 / swift/op_797 -- **total equality**
  - cpp/op_209 / go/op_707 -- **total equality**
  - cpp/op_353 / go/op_707 -- **total equality**
  - cpp/op_461 / go/op_707 -- **total equality**
  - cpp/op_857 / go/op_707 -- **total equality**
  - cpp/op_965 / go/op_707 -- **total equality**
  - cpp/op_209 / rust/op_101 -- **total equality**
  - cpp/op_209 / rust/op_173 -- **total equality**
  - cpp/op_353 / rust/op_101 -- **total equality**
  - cpp/op_353 / rust/op_173 -- **total equality**
  - cpp/op_461 / rust/op_101 -- **total equality**
  - cpp/op_461 / rust/op_173 -- **total equality**
  - cpp/op_857 / rust/op_101 -- **total equality**
  - cpp/op_857 / rust/op_173 -- **total equality**
  - cpp/op_965 / rust/op_101 -- **total equality**
  - cpp/op_965 / rust/op_173 -- **total equality**
  - cpp/op_209 / swift/op_797 -- **total equality**
  - cpp/op_353 / swift/op_797 -- **total equality**
  - cpp/op_461 / swift/op_797 -- **total equality**
  - cpp/op_857 / swift/op_797 -- **total equality**
  - cpp/op_965 / swift/op_797 -- **total equality**
  - go/op_707 / rust/op_101 -- **total equality**
  - go/op_707 / rust/op_173 -- **total equality**
  - go/op_707 / swift/op_797 -- **total equality**
  - rust/op_101 / swift/op_797 -- **total equality**
  - rust/op_173 / swift/op_797 -- **total equality**

### sem-identical group B0 V[zx64(And32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `&` (bool,i32, 0 modes); cpp `&` (bool,i32, 0 modes); cpp `bitand` (bool,i32, 0 modes)

  - c/op_456 / cpp/op_456 -- **total equality**
  - c/op_456 / cpp/op_960 -- **total equality**

### sem-identical group B0 V[zx64(And32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `&` (bool,i64, 0 modes); cpp `&` (bool,i64, 0 modes); cpp `bitand` (bool,i64, 0 modes)

  - c/op_457 / cpp/op_457 -- **total equality**
  - c/op_457 / cpp/op_961 -- **total equality**

### sem-identical group B0 V[zx64(And32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `&` (bool,u64, 0 modes); cpp `&` (bool,u64, 0 modes); cpp `bitand` (bool,u64, 0 modes)

  - c/op_458 / cpp/op_458 -- **total equality**
  - c/op_458 / cpp/op_962 -- **total equality**

### sem-identical group B0 V[zx64(And32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `&` (i32,bool, 0 modes); cpp `&` (i32,bool, 0 modes); cpp `bitand` (i32,bool, 0 modes)

  - c/op_431 / cpp/op_431 -- **total equality**
  - c/op_431 / cpp/op_935 -- **total equality**

### sem-identical group B0 V[zx64(And32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (i32,i32)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `&` (i32,i32, 0 modes); cpp `&` (i32,i32, 0 modes); cpp `bitand` (i32,i32, 0 modes); go `&` (i32,i32, 0 modes); rust `&` (i32,i32, 0 modes); swift `&` (i32,i32, 0 modes)

  - c/op_426 / cpp/op_426 -- **total equality**
  - c/op_426 / cpp/op_930 -- **total equality**
  - c/op_426 / go/op_240 -- **total equality**
  - c/op_426 / rust/op_138 -- **total equality**
  - c/op_426 / swift/op_582 -- **total equality**
  - cpp/op_426 / go/op_240 -- **total equality**
  - cpp/op_930 / go/op_240 -- **total equality**
  - cpp/op_426 / rust/op_138 -- **total equality**
  - cpp/op_930 / rust/op_138 -- **total equality**
  - cpp/op_426 / swift/op_582 -- **total equality**
  - cpp/op_930 / swift/op_582 -- **total equality**
  - go/op_240 / rust/op_138 -- **total equality**
  - go/op_240 / swift/op_582 -- **total equality**
  - rust/op_138 / swift/op_582 -- **total equality**

### sem-identical group B0 V[zx64(And32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `&` (i64,bool, 0 modes); cpp `&` (i64,bool, 0 modes); cpp `bitand` (i64,bool, 0 modes)

  - c/op_437 / cpp/op_437 -- **total equality**
  - c/op_437 / cpp/op_941 -- **total equality**

### sem-identical group B0 V[zx64(And32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `&` (u64,bool, 0 modes); cpp `&` (u64,bool, 0 modes); cpp `bitand` (u64,bool, 0 modes)

  - c/op_443 / cpp/op_443 -- **total equality**
  - c/op_443 / cpp/op_947 -- **total equality**

### sem-identical group B0 V[] S[] E[ret] · (f32,None)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `+` (f32,None, 0 modes); c `__extension__` (f32,None, 0 modes); c `++` (f32,None, 0 modes); c `--` (f32,None, 0 modes); cpp `+` (f32,None, 0 modes); cpp `++` (f32,None, 0 modes); cpp `--` (f32,None, 0 modes); go `+` (f32,None, 0 modes); rust `..` (f32,None, 0 modes); rust `..=` (f32,None, 0 modes); swift `+` (f32,None, 0 modes)

  - c/op_21 / cpp/op_21 -- **total equality**
  - c/op_21 / cpp/op_87 -- **total equality**
  - c/op_21 / cpp/op_93 -- **total equality**
  - c/op_87 / cpp/op_21 -- **total equality**
  - c/op_87 / cpp/op_87 -- **total equality**
  - c/op_87 / cpp/op_93 -- **total equality**
  - c/op_93 / cpp/op_21 -- **total equality**
  - c/op_93 / cpp/op_87 -- **total equality**
  - c/op_93 / cpp/op_93 -- **total equality**
  - c/op_99 / cpp/op_21 -- **total equality**
  - c/op_99 / cpp/op_87 -- **total equality**
  - c/op_99 / cpp/op_93 -- **total equality**
  - c/op_21 / go/op_3 -- **total equality**
  - c/op_87 / go/op_3 -- **total equality**
  - c/op_93 / go/op_3 -- **total equality**
  - c/op_99 / go/op_3 -- **total equality**
  - c/op_21 / rust/op_39 -- **total equality**
  - c/op_21 / rust/op_45 -- **total equality**
  - c/op_87 / rust/op_39 -- **total equality**
  - c/op_87 / rust/op_45 -- **total equality**
  - c/op_93 / rust/op_39 -- **total equality**
  - c/op_93 / rust/op_45 -- **total equality**
  - c/op_99 / rust/op_39 -- **total equality**
  - c/op_99 / rust/op_45 -- **total equality**
  - c/op_21 / swift/op_21 -- **total equality**
  - c/op_87 / swift/op_21 -- **total equality**
  - c/op_93 / swift/op_21 -- **total equality**
  - c/op_99 / swift/op_21 -- **total equality**
  - cpp/op_21 / go/op_3 -- **total equality**
  - cpp/op_87 / go/op_3 -- **total equality**
  - cpp/op_93 / go/op_3 -- **total equality**
  - cpp/op_21 / rust/op_39 -- **total equality**
  - cpp/op_21 / rust/op_45 -- **total equality**
  - cpp/op_87 / rust/op_39 -- **total equality**
  - cpp/op_87 / rust/op_45 -- **total equality**
  - cpp/op_93 / rust/op_39 -- **total equality**
  - cpp/op_93 / rust/op_45 -- **total equality**
  - cpp/op_21 / swift/op_21 -- **total equality**
  - cpp/op_87 / swift/op_21 -- **total equality**
  - cpp/op_93 / swift/op_21 -- **total equality**
  - go/op_3 / rust/op_39 -- **total equality**
  - go/op_3 / rust/op_45 -- **total equality**
  - go/op_3 / swift/op_21 -- **total equality**
  - rust/op_39 / swift/op_21 -- **total equality**
  - rust/op_45 / swift/op_21 -- **total equality**

### sem-identical group B0 V[] S[] E[ret] · (f32,f32)

- ground: cluster
- languages: rust, swift
- members: rust `..` (f32,f32, 0 modes); swift `??` (f32,f32, 0 modes)

  - rust/op_735 / swift/op_855 -- **total equality**

### sem-identical group B0 V[] S[] E[ret] · (f64,None)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `+` (f64,None, 0 modes); c `__extension__` (f64,None, 0 modes); c `++` (f64,None, 0 modes); c `--` (f64,None, 0 modes); cpp `+` (f64,None, 0 modes); cpp `++` (f64,None, 0 modes); cpp `--` (f64,None, 0 modes); go `+` (f64,None, 0 modes); rust `..` (f64,None, 0 modes); rust `..=` (f64,None, 0 modes); swift `+` (f64,None, 0 modes)

  - c/op_22 / cpp/op_22 -- **total equality**
  - c/op_22 / cpp/op_88 -- **total equality**
  - c/op_22 / cpp/op_94 -- **total equality**
  - c/op_88 / cpp/op_22 -- **total equality**
  - c/op_88 / cpp/op_88 -- **total equality**
  - c/op_88 / cpp/op_94 -- **total equality**
  - c/op_94 / cpp/op_22 -- **total equality**
  - c/op_94 / cpp/op_88 -- **total equality**
  - c/op_94 / cpp/op_94 -- **total equality**
  - c/op_100 / cpp/op_22 -- **total equality**
  - c/op_100 / cpp/op_88 -- **total equality**
  - c/op_100 / cpp/op_94 -- **total equality**
  - c/op_22 / go/op_4 -- **total equality**
  - c/op_88 / go/op_4 -- **total equality**
  - c/op_94 / go/op_4 -- **total equality**
  - c/op_100 / go/op_4 -- **total equality**
  - c/op_22 / rust/op_40 -- **total equality**
  - c/op_22 / rust/op_46 -- **total equality**
  - c/op_88 / rust/op_40 -- **total equality**
  - c/op_88 / rust/op_46 -- **total equality**
  - c/op_94 / rust/op_40 -- **total equality**
  - c/op_94 / rust/op_46 -- **total equality**
  - c/op_100 / rust/op_40 -- **total equality**
  - c/op_100 / rust/op_46 -- **total equality**
  - c/op_22 / swift/op_22 -- **total equality**
  - c/op_88 / swift/op_22 -- **total equality**
  - c/op_94 / swift/op_22 -- **total equality**
  - c/op_100 / swift/op_22 -- **total equality**
  - cpp/op_22 / go/op_4 -- **total equality**
  - cpp/op_88 / go/op_4 -- **total equality**
  - cpp/op_94 / go/op_4 -- **total equality**
  - cpp/op_22 / rust/op_40 -- **total equality**
  - cpp/op_22 / rust/op_46 -- **total equality**
  - cpp/op_88 / rust/op_40 -- **total equality**
  - cpp/op_88 / rust/op_46 -- **total equality**
  - cpp/op_94 / rust/op_40 -- **total equality**
  - cpp/op_94 / rust/op_46 -- **total equality**
  - cpp/op_22 / swift/op_22 -- **total equality**
  - cpp/op_88 / swift/op_22 -- **total equality**
  - cpp/op_94 / swift/op_22 -- **total equality**
  - go/op_4 / rust/op_40 -- **total equality**
  - go/op_4 / rust/op_46 -- **total equality**
  - go/op_4 / swift/op_22 -- **total equality**
  - rust/op_40 / swift/op_22 -- **total equality**
  - rust/op_46 / swift/op_22 -- **total equality**

### sem-identical group B0 V[] S[] E[ret] · (f64,f64)

- ground: cluster
- languages: rust, swift
- members: rust `..` (f64,f64, 0 modes); swift `??` (f64,f64, 0 modes)

  - rust/op_742 / swift/op_862 -- **total equality**

### sem-identical group B0 V[in0:64] S[] E[ret] · (i64,None)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `+` (i64,None, 0 modes); c `__extension__` (i64,None, 0 modes); c `++` (i64,None, 0 modes); c `--` (i64,None, 0 modes); cpp `+` (i64,None, 0 modes); cpp `++` (i64,None, 0 modes); cpp `--` (i64,None, 0 modes); rust `..` (i64,None, 0 modes); rust `..=` (i64,None, 0 modes); swift `+` (i64,None, 0 modes)

  - c/op_19 / cpp/op_19 -- **total equality**
  - c/op_19 / cpp/op_85 -- **total equality**
  - c/op_19 / cpp/op_91 -- **total equality**
  - c/op_85 / cpp/op_19 -- **total equality**
  - c/op_85 / cpp/op_85 -- **total equality**
  - c/op_85 / cpp/op_91 -- **total equality**
  - c/op_91 / cpp/op_19 -- **total equality**
  - c/op_91 / cpp/op_85 -- **total equality**
  - c/op_91 / cpp/op_91 -- **total equality**
  - c/op_97 / cpp/op_19 -- **total equality**
  - c/op_97 / cpp/op_85 -- **total equality**
  - c/op_97 / cpp/op_91 -- **total equality**
  - c/op_19 / rust/op_37 -- **total equality**
  - c/op_19 / rust/op_43 -- **total equality**
  - c/op_85 / rust/op_37 -- **total equality**
  - c/op_85 / rust/op_43 -- **total equality**
  - c/op_91 / rust/op_37 -- **total equality**
  - c/op_91 / rust/op_43 -- **total equality**
  - c/op_97 / rust/op_37 -- **total equality**
  - c/op_97 / rust/op_43 -- **total equality**
  - c/op_19 / swift/op_19 -- **total equality**
  - c/op_85 / swift/op_19 -- **total equality**
  - c/op_91 / swift/op_19 -- **total equality**
  - c/op_97 / swift/op_19 -- **total equality**
  - cpp/op_19 / rust/op_37 -- **total equality**
  - cpp/op_19 / rust/op_43 -- **total equality**
  - cpp/op_85 / rust/op_37 -- **total equality**
  - cpp/op_85 / rust/op_43 -- **total equality**
  - cpp/op_91 / rust/op_37 -- **total equality**
  - cpp/op_91 / rust/op_43 -- **total equality**
  - cpp/op_19 / swift/op_19 -- **total equality**
  - cpp/op_85 / swift/op_19 -- **total equality**
  - cpp/op_91 / swift/op_19 -- **total equality**
  - rust/op_37 / swift/op_19 -- **total equality**
  - rust/op_43 / swift/op_19 -- **total equality**

### sem-identical group B0 V[in0:64] S[] E[ret] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `/` (i64,bool, 0 modes); cpp `/` (i64,bool, 0 modes)

  - c/op_221 / cpp/op_221 -- **total equality**

### sem-identical group B0 V[in0:64] S[] E[ret] · (u64,None)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `+` (u64,None, 0 modes); c `__extension__` (u64,None, 0 modes); c `++` (u64,None, 0 modes); c `--` (u64,None, 0 modes); cpp `+` (u64,None, 0 modes); cpp `++` (u64,None, 0 modes); cpp `--` (u64,None, 0 modes); rust `..` (u64,None, 0 modes); rust `..=` (u64,None, 0 modes); swift `+` (u64,None, 0 modes)

  - c/op_20 / cpp/op_20 -- **total equality**
  - c/op_20 / cpp/op_86 -- **total equality**
  - c/op_20 / cpp/op_92 -- **total equality**
  - c/op_86 / cpp/op_20 -- **total equality**
  - c/op_86 / cpp/op_86 -- **total equality**
  - c/op_86 / cpp/op_92 -- **total equality**
  - c/op_92 / cpp/op_20 -- **total equality**
  - c/op_92 / cpp/op_86 -- **total equality**
  - c/op_92 / cpp/op_92 -- **total equality**
  - c/op_98 / cpp/op_20 -- **total equality**
  - c/op_98 / cpp/op_86 -- **total equality**
  - c/op_98 / cpp/op_92 -- **total equality**
  - c/op_20 / rust/op_38 -- **total equality**
  - c/op_20 / rust/op_44 -- **total equality**
  - c/op_86 / rust/op_38 -- **total equality**
  - c/op_86 / rust/op_44 -- **total equality**
  - c/op_92 / rust/op_38 -- **total equality**
  - c/op_92 / rust/op_44 -- **total equality**
  - c/op_98 / rust/op_38 -- **total equality**
  - c/op_98 / rust/op_44 -- **total equality**
  - c/op_20 / swift/op_20 -- **total equality**
  - c/op_86 / swift/op_20 -- **total equality**
  - c/op_92 / swift/op_20 -- **total equality**
  - c/op_98 / swift/op_20 -- **total equality**
  - cpp/op_20 / rust/op_38 -- **total equality**
  - cpp/op_20 / rust/op_44 -- **total equality**
  - cpp/op_86 / rust/op_38 -- **total equality**
  - cpp/op_86 / rust/op_44 -- **total equality**
  - cpp/op_92 / rust/op_38 -- **total equality**
  - cpp/op_92 / rust/op_44 -- **total equality**
  - cpp/op_20 / swift/op_20 -- **total equality**
  - cpp/op_86 / swift/op_20 -- **total equality**
  - cpp/op_92 / swift/op_20 -- **total equality**
  - rust/op_38 / swift/op_20 -- **total equality**
  - rust/op_44 / swift/op_20 -- **total equality**

### sem-identical group B0 V[in0:64] S[] E[ret] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `/` (u64,bool, 0 modes); cpp `/` (u64,bool, 0 modes)

  - c/op_227 / cpp/op_227 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(in0:64))] S[] E[ret] · (bool,None)

- ground: cluster
- languages: c, cpp, rust
- members: c `+` (bool,None, 0 modes); c `__extension__` (bool,None, 0 modes); c `++` (bool,None, 0 modes); c `--` (bool,None, 0 modes); cpp `+` (bool,None, 0 modes); rust `..` (bool,None, 0 modes); rust `..=` (bool,None, 0 modes)

  - c/op_23 / cpp/op_23 -- **total equality**
  - c/op_89 / cpp/op_23 -- **total equality**
  - c/op_95 / cpp/op_23 -- **total equality**
  - c/op_101 / cpp/op_23 -- **total equality**
  - c/op_23 / rust/op_41 -- **total equality**
  - c/op_23 / rust/op_47 -- **total equality**
  - c/op_89 / rust/op_41 -- **total equality**
  - c/op_89 / rust/op_47 -- **total equality**
  - c/op_95 / rust/op_41 -- **total equality**
  - c/op_95 / rust/op_47 -- **total equality**
  - c/op_101 / rust/op_41 -- **total equality**
  - c/op_101 / rust/op_47 -- **total equality**
  - cpp/op_23 / rust/op_41 -- **total equality**
  - cpp/op_23 / rust/op_47 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(in0:64))] S[] E[ret] · (bool,bool)

- ground: cluster
- languages: c, cpp, swift
- members: c `/` (bool,bool, 0 modes); cpp `/` (bool,bool, 0 modes); swift `??` (bool,bool, 0 modes)

  - c/op_245 / cpp/op_245 -- **total equality**
  - c/op_245 / swift/op_869 -- **total equality**
  - cpp/op_245 / swift/op_869 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(in0:64))] S[] E[ret] · (i32,None)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `+` (i32,None, 0 modes); c `__extension__` (i32,None, 0 modes); c `++` (i32,None, 0 modes); c `--` (i32,None, 0 modes); cpp `+` (i32,None, 0 modes); cpp `++` (i32,None, 0 modes); cpp `--` (i32,None, 0 modes); rust `..` (i32,None, 0 modes); rust `..=` (i32,None, 0 modes); swift `+` (i32,None, 0 modes)

  - c/op_18 / cpp/op_18 -- **total equality**
  - c/op_18 / cpp/op_84 -- **total equality**
  - c/op_18 / cpp/op_90 -- **total equality**
  - c/op_84 / cpp/op_18 -- **total equality**
  - c/op_84 / cpp/op_84 -- **total equality**
  - c/op_84 / cpp/op_90 -- **total equality**
  - c/op_90 / cpp/op_18 -- **total equality**
  - c/op_90 / cpp/op_84 -- **total equality**
  - c/op_90 / cpp/op_90 -- **total equality**
  - c/op_96 / cpp/op_18 -- **total equality**
  - c/op_96 / cpp/op_84 -- **total equality**
  - c/op_96 / cpp/op_90 -- **total equality**
  - c/op_18 / rust/op_36 -- **total equality**
  - c/op_18 / rust/op_42 -- **total equality**
  - c/op_84 / rust/op_36 -- **total equality**
  - c/op_84 / rust/op_42 -- **total equality**
  - c/op_90 / rust/op_36 -- **total equality**
  - c/op_90 / rust/op_42 -- **total equality**
  - c/op_96 / rust/op_36 -- **total equality**
  - c/op_96 / rust/op_42 -- **total equality**
  - c/op_18 / swift/op_18 -- **total equality**
  - c/op_84 / swift/op_18 -- **total equality**
  - c/op_90 / swift/op_18 -- **total equality**
  - c/op_96 / swift/op_18 -- **total equality**
  - cpp/op_18 / rust/op_36 -- **total equality**
  - cpp/op_18 / rust/op_42 -- **total equality**
  - cpp/op_84 / rust/op_36 -- **total equality**
  - cpp/op_84 / rust/op_42 -- **total equality**
  - cpp/op_90 / rust/op_36 -- **total equality**
  - cpp/op_90 / rust/op_42 -- **total equality**
  - cpp/op_18 / swift/op_18 -- **total equality**
  - cpp/op_84 / swift/op_18 -- **total equality**
  - cpp/op_90 / swift/op_18 -- **total equality**
  - rust/op_36 / swift/op_18 -- **total equality**
  - rust/op_42 / swift/op_18 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(in0:64))] S[] E[ret] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `/` (i32,bool, 0 modes); cpp `/` (i32,bool, 0 modes)

  - c/op_215 / cpp/op_215 -- **total equality**

### sem-identical group B0 V[zx64(Or32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (bool,bool)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `||` (bool,bool, 0 modes); c `|` (bool,bool, 0 modes); cpp `||` (bool,bool, 0 modes); cpp `|` (bool,bool, 0 modes); cpp `or` (bool,bool, 0 modes); cpp `bitor` (bool,bool, 0 modes); go `||` (bool,bool, 0 modes); rust `||` (bool,bool, 0 modes); rust `|` (bool,bool, 0 modes); swift `||` (bool,bool, 0 modes)

  - c/op_317 / cpp/op_317 -- **total equality**
  - c/op_317 / cpp/op_389 -- **total equality**
  - c/op_317 / cpp/op_821 -- **total equality**
  - c/op_317 / cpp/op_893 -- **total equality**
  - c/op_389 / cpp/op_317 -- **total equality**
  - c/op_389 / cpp/op_389 -- **total equality**
  - c/op_389 / cpp/op_821 -- **total equality**
  - c/op_389 / cpp/op_893 -- **total equality**
  - c/op_317 / go/op_743 -- **total equality**
  - c/op_389 / go/op_743 -- **total equality**
  - c/op_317 / rust/op_137 -- **total equality**
  - c/op_317 / rust/op_209 -- **total equality**
  - c/op_389 / rust/op_137 -- **total equality**
  - c/op_389 / rust/op_209 -- **total equality**
  - c/op_317 / swift/op_833 -- **total equality**
  - c/op_389 / swift/op_833 -- **total equality**
  - cpp/op_317 / go/op_743 -- **total equality**
  - cpp/op_389 / go/op_743 -- **total equality**
  - cpp/op_821 / go/op_743 -- **total equality**
  - cpp/op_893 / go/op_743 -- **total equality**
  - cpp/op_317 / rust/op_137 -- **total equality**
  - cpp/op_317 / rust/op_209 -- **total equality**
  - cpp/op_389 / rust/op_137 -- **total equality**
  - cpp/op_389 / rust/op_209 -- **total equality**
  - cpp/op_821 / rust/op_137 -- **total equality**
  - cpp/op_821 / rust/op_209 -- **total equality**
  - cpp/op_893 / rust/op_137 -- **total equality**
  - cpp/op_893 / rust/op_209 -- **total equality**
  - cpp/op_317 / swift/op_833 -- **total equality**
  - cpp/op_389 / swift/op_833 -- **total equality**
  - cpp/op_821 / swift/op_833 -- **total equality**
  - cpp/op_893 / swift/op_833 -- **total equality**
  - go/op_743 / rust/op_137 -- **total equality**
  - go/op_743 / rust/op_209 -- **total equality**
  - go/op_743 / swift/op_833 -- **total equality**
  - rust/op_137 / swift/op_833 -- **total equality**
  - rust/op_209 / swift/op_833 -- **total equality**

### sem-identical group B0 V[zx64(Or32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `|` (bool,i32, 0 modes); cpp `|` (bool,i32, 0 modes); cpp `bitor` (bool,i32, 0 modes)

  - c/op_384 / cpp/op_384 -- **total equality**
  - c/op_384 / cpp/op_888 -- **total equality**

### sem-identical group B0 V[zx64(Or32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `|` (i32,bool, 0 modes); cpp `|` (i32,bool, 0 modes); cpp `bitor` (i32,bool, 0 modes)

  - c/op_359 / cpp/op_359 -- **total equality**
  - c/op_359 / cpp/op_863 -- **total equality**

### sem-identical group B0 V[zx64(Or32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (i32,i32)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `|` (i32,i32, 0 modes); cpp `|` (i32,i32, 0 modes); cpp `bitor` (i32,i32, 0 modes); go `|` (i32,i32, 0 modes); rust `|` (i32,i32, 0 modes); swift `|` (i32,i32, 0 modes)

  - c/op_354 / cpp/op_354 -- **total equality**
  - c/op_354 / cpp/op_858 -- **total equality**
  - c/op_354 / go/op_384 -- **total equality**
  - c/op_354 / rust/op_174 -- **total equality**
  - c/op_354 / swift/op_618 -- **total equality**
  - cpp/op_354 / go/op_384 -- **total equality**
  - cpp/op_858 / go/op_384 -- **total equality**
  - cpp/op_354 / rust/op_174 -- **total equality**
  - cpp/op_858 / rust/op_174 -- **total equality**
  - cpp/op_354 / swift/op_618 -- **total equality**
  - cpp/op_858 / swift/op_618 -- **total equality**
  - go/op_384 / rust/op_174 -- **total equality**
  - go/op_384 / swift/op_618 -- **total equality**
  - rust/op_174 / swift/op_618 -- **total equality**

### sem-identical group B0 V[zx64(Xor32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (bool,bool)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `^` (bool,bool, 0 modes); c `!=` (bool,bool, 0 modes); cpp `^` (bool,bool, 0 modes); cpp `!=` (bool,bool, 0 modes); cpp `xor` (bool,bool, 0 modes); cpp `not_eq` (bool,bool, 0 modes); rust `^` (bool,bool, 0 modes); rust `!=` (bool,bool, 0 modes); swift `!=` (bool,bool, 0 modes)

  - c/op_425 / cpp/op_425 -- **total equality**
  - c/op_425 / cpp/op_533 -- **total equality**
  - c/op_425 / cpp/op_929 -- **total equality**
  - c/op_425 / cpp/op_1001 -- **total equality**
  - c/op_533 / cpp/op_425 -- **total equality**
  - c/op_533 / cpp/op_533 -- **total equality**
  - c/op_533 / cpp/op_929 -- **total equality**
  - c/op_533 / cpp/op_1001 -- **total equality**
  - c/op_425 / rust/op_245 -- **total equality**
  - c/op_425 / rust/op_317 -- **total equality**
  - c/op_533 / rust/op_245 -- **total equality**
  - c/op_533 / rust/op_317 -- **total equality**
  - c/op_425 / swift/op_473 -- **total equality**
  - c/op_533 / swift/op_473 -- **total equality**
  - cpp/op_425 / rust/op_245 -- **total equality**
  - cpp/op_425 / rust/op_317 -- **total equality**
  - cpp/op_533 / rust/op_245 -- **total equality**
  - cpp/op_533 / rust/op_317 -- **total equality**
  - cpp/op_929 / rust/op_245 -- **total equality**
  - cpp/op_929 / rust/op_317 -- **total equality**
  - cpp/op_1001 / rust/op_245 -- **total equality**
  - cpp/op_1001 / rust/op_317 -- **total equality**
  - cpp/op_425 / swift/op_473 -- **total equality**
  - cpp/op_533 / swift/op_473 -- **total equality**
  - cpp/op_929 / swift/op_473 -- **total equality**
  - cpp/op_1001 / swift/op_473 -- **total equality**
  - rust/op_245 / swift/op_473 -- **total equality**
  - rust/op_317 / swift/op_473 -- **total equality**

### sem-identical group B0 V[zx64(Xor32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `^` (bool,i32, 0 modes); cpp `^` (bool,i32, 0 modes); cpp `xor` (bool,i32, 0 modes)

  - c/op_420 / cpp/op_420 -- **total equality**
  - c/op_420 / cpp/op_924 -- **total equality**

### sem-identical group B0 V[zx64(Xor32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `^` (i32,bool, 0 modes); cpp `^` (i32,bool, 0 modes); cpp `xor` (i32,bool, 0 modes)

  - c/op_395 / cpp/op_395 -- **total equality**
  - c/op_395 / cpp/op_899 -- **total equality**

### sem-identical group B0 V[zx64(Xor32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (i32,i32)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `^` (i32,i32, 0 modes); cpp `^` (i32,i32, 0 modes); cpp `xor` (i32,i32, 0 modes); go `^` (i32,i32, 0 modes); rust `^` (i32,i32, 0 modes); swift `^` (i32,i32, 0 modes)

  - c/op_390 / cpp/op_390 -- **total equality**
  - c/op_390 / cpp/op_894 -- **total equality**
  - c/op_390 / go/op_420 -- **total equality**
  - c/op_390 / rust/op_210 -- **total equality**
  - c/op_390 / swift/op_654 -- **total equality**
  - cpp/op_390 / go/op_420 -- **total equality**
  - cpp/op_894 / go/op_420 -- **total equality**
  - cpp/op_390 / rust/op_210 -- **total equality**
  - cpp/op_894 / rust/op_210 -- **total equality**
  - cpp/op_390 / swift/op_654 -- **total equality**
  - cpp/op_894 / swift/op_654 -- **total equality**
  - go/op_420 / rust/op_210 -- **total equality**
  - go/op_420 / swift/op_654 -- **total equality**
  - rust/op_210 / swift/op_654 -- **total equality**

### sem-identical group B0 V[And64(in0:64,in1:64)] S[] E[ret] · (i64,i64)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `&` (i64,i64, 0 modes); cpp `&` (i64,i64, 0 modes); cpp `bitand` (i64,i64, 0 modes); go `&` (i64,i64, 0 modes); rust `&` (i64,i64, 0 modes); swift `&` (i64,i64, 0 modes)

  - c/op_433 / cpp/op_433 -- **total equality**
  - c/op_433 / cpp/op_937 -- **total equality**
  - c/op_433 / go/op_247 -- **total equality**
  - c/op_433 / rust/op_145 -- **total equality**
  - c/op_433 / swift/op_589 -- **total equality**
  - cpp/op_433 / go/op_247 -- **total equality**
  - cpp/op_937 / go/op_247 -- **total equality**
  - cpp/op_433 / rust/op_145 -- **total equality**
  - cpp/op_937 / rust/op_145 -- **total equality**
  - cpp/op_433 / swift/op_589 -- **total equality**
  - cpp/op_937 / swift/op_589 -- **total equality**
  - go/op_247 / rust/op_145 -- **total equality**
  - go/op_247 / swift/op_589 -- **total equality**
  - rust/op_145 / swift/op_589 -- **total equality**

### sem-identical group B0 V[And64(in0:64,in1:64)] S[] E[ret] · (i64,u64)

- ground: cluster
- languages: c, cpp
- members: c `&` (i64,u64, 0 modes); cpp `&` (i64,u64, 0 modes); cpp `bitand` (i64,u64, 0 modes)

  - c/op_434 / cpp/op_434 -- **total equality**
  - c/op_434 / cpp/op_938 -- **total equality**

### sem-identical group B0 V[And64(in0:64,in1:64)] S[] E[ret] · (u64,i64)

- ground: cluster
- languages: c, cpp
- members: c `&` (u64,i64, 0 modes); cpp `&` (u64,i64, 0 modes); cpp `bitand` (u64,i64, 0 modes)

  - c/op_439 / cpp/op_439 -- **total equality**
  - c/op_439 / cpp/op_943 -- **total equality**

### sem-identical group B0 V[And64(in0:64,in1:64)] S[] E[ret] · (u64,u64)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `&` (u64,u64, 0 modes); cpp `&` (u64,u64, 0 modes); cpp `bitand` (u64,u64, 0 modes); go `&` (u64,u64, 0 modes); rust `&` (u64,u64, 0 modes); swift `&` (u64,u64, 0 modes)

  - c/op_440 / cpp/op_440 -- **total equality**
  - c/op_440 / cpp/op_944 -- **total equality**
  - c/op_440 / go/op_254 -- **total equality**
  - c/op_440 / rust/op_152 -- **total equality**
  - c/op_440 / swift/op_596 -- **total equality**
  - cpp/op_440 / go/op_254 -- **total equality**
  - cpp/op_944 / go/op_254 -- **total equality**
  - cpp/op_440 / rust/op_152 -- **total equality**
  - cpp/op_944 / rust/op_152 -- **total equality**
  - cpp/op_440 / swift/op_596 -- **total equality**
  - cpp/op_944 / swift/op_596 -- **total equality**
  - go/op_254 / rust/op_152 -- **total equality**
  - go/op_254 / swift/op_596 -- **total equality**
  - rust/op_152 / swift/op_596 -- **total equality**

### sem-identical group B0 V[Or64(in0:64,in1:64)] S[] E[ret] · (i64,i64)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `|` (i64,i64, 0 modes); cpp `|` (i64,i64, 0 modes); cpp `bitor` (i64,i64, 0 modes); go `|` (i64,i64, 0 modes); rust `|` (i64,i64, 0 modes); swift `|` (i64,i64, 0 modes)

  - c/op_361 / cpp/op_361 -- **total equality**
  - c/op_361 / cpp/op_865 -- **total equality**
  - c/op_361 / go/op_391 -- **total equality**
  - c/op_361 / rust/op_181 -- **total equality**
  - c/op_361 / swift/op_625 -- **total equality**
  - cpp/op_361 / go/op_391 -- **total equality**
  - cpp/op_865 / go/op_391 -- **total equality**
  - cpp/op_361 / rust/op_181 -- **total equality**
  - cpp/op_865 / rust/op_181 -- **total equality**
  - cpp/op_361 / swift/op_625 -- **total equality**
  - cpp/op_865 / swift/op_625 -- **total equality**
  - go/op_391 / rust/op_181 -- **total equality**
  - go/op_391 / swift/op_625 -- **total equality**
  - rust/op_181 / swift/op_625 -- **total equality**

### sem-identical group B0 V[Or64(in0:64,in1:64)] S[] E[ret] · (i64,u64)

- ground: cluster
- languages: c, cpp
- members: c `|` (i64,u64, 0 modes); cpp `|` (i64,u64, 0 modes); cpp `bitor` (i64,u64, 0 modes)

  - c/op_362 / cpp/op_362 -- **total equality**
  - c/op_362 / cpp/op_866 -- **total equality**

### sem-identical group B0 V[Or64(in0:64,in1:64)] S[] E[ret] · (u64,i64)

- ground: cluster
- languages: c, cpp
- members: c `|` (u64,i64, 0 modes); cpp `|` (u64,i64, 0 modes); cpp `bitor` (u64,i64, 0 modes)

  - c/op_367 / cpp/op_367 -- **total equality**
  - c/op_367 / cpp/op_871 -- **total equality**

### sem-identical group B0 V[Or64(in0:64,in1:64)] S[] E[ret] · (u64,u64)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `|` (u64,u64, 0 modes); cpp `|` (u64,u64, 0 modes); cpp `bitor` (u64,u64, 0 modes); go `|` (u64,u64, 0 modes); rust `|` (u64,u64, 0 modes); swift `|` (u64,u64, 0 modes)

  - c/op_368 / cpp/op_368 -- **total equality**
  - c/op_368 / cpp/op_872 -- **total equality**
  - c/op_368 / go/op_398 -- **total equality**
  - c/op_368 / rust/op_188 -- **total equality**
  - c/op_368 / swift/op_632 -- **total equality**
  - cpp/op_368 / go/op_398 -- **total equality**
  - cpp/op_872 / go/op_398 -- **total equality**
  - cpp/op_368 / rust/op_188 -- **total equality**
  - cpp/op_872 / rust/op_188 -- **total equality**
  - cpp/op_368 / swift/op_632 -- **total equality**
  - cpp/op_872 / swift/op_632 -- **total equality**
  - go/op_398 / rust/op_188 -- **total equality**
  - go/op_398 / swift/op_632 -- **total equality**
  - rust/op_188 / swift/op_632 -- **total equality**

### sem-identical group B0 V[Xor64(in0:64,in1:64)] S[] E[ret] · (i64,i64)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `^` (i64,i64, 0 modes); cpp `^` (i64,i64, 0 modes); cpp `xor` (i64,i64, 0 modes); go `^` (i64,i64, 0 modes); rust `^` (i64,i64, 0 modes); swift `^` (i64,i64, 0 modes)

  - c/op_397 / cpp/op_397 -- **total equality**
  - c/op_397 / cpp/op_901 -- **total equality**
  - c/op_397 / go/op_427 -- **total equality**
  - c/op_397 / rust/op_217 -- **total equality**
  - c/op_397 / swift/op_661 -- **total equality**
  - cpp/op_397 / go/op_427 -- **total equality**
  - cpp/op_901 / go/op_427 -- **total equality**
  - cpp/op_397 / rust/op_217 -- **total equality**
  - cpp/op_901 / rust/op_217 -- **total equality**
  - cpp/op_397 / swift/op_661 -- **total equality**
  - cpp/op_901 / swift/op_661 -- **total equality**
  - go/op_427 / rust/op_217 -- **total equality**
  - go/op_427 / swift/op_661 -- **total equality**
  - rust/op_217 / swift/op_661 -- **total equality**

### sem-identical group B0 V[Xor64(in0:64,in1:64)] S[] E[ret] · (i64,u64)

- ground: cluster
- languages: c, cpp
- members: c `^` (i64,u64, 0 modes); cpp `^` (i64,u64, 0 modes); cpp `xor` (i64,u64, 0 modes)

  - c/op_398 / cpp/op_398 -- **total equality**
  - c/op_398 / cpp/op_902 -- **total equality**

### sem-identical group B0 V[Xor64(in0:64,in1:64)] S[] E[ret] · (u64,i64)

- ground: cluster
- languages: c, cpp
- members: c `^` (u64,i64, 0 modes); cpp `^` (u64,i64, 0 modes); cpp `xor` (u64,i64, 0 modes)

  - c/op_403 / cpp/op_403 -- **total equality**
  - c/op_403 / cpp/op_907 -- **total equality**

### sem-identical group B0 V[Xor64(in0:64,in1:64)] S[] E[ret] · (u64,u64)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `^` (u64,u64, 0 modes); cpp `^` (u64,u64, 0 modes); cpp `xor` (u64,u64, 0 modes); go `^` (u64,u64, 0 modes); rust `^` (u64,u64, 0 modes); swift `^` (u64,u64, 0 modes)

  - c/op_404 / cpp/op_404 -- **total equality**
  - c/op_404 / cpp/op_908 -- **total equality**
  - c/op_404 / go/op_434 -- **total equality**
  - c/op_404 / rust/op_224 -- **total equality**
  - c/op_404 / swift/op_668 -- **total equality**
  - cpp/op_404 / go/op_434 -- **total equality**
  - cpp/op_908 / go/op_434 -- **total equality**
  - cpp/op_404 / rust/op_224 -- **total equality**
  - cpp/op_908 / rust/op_224 -- **total equality**
  - cpp/op_404 / swift/op_668 -- **total equality**
  - cpp/op_908 / swift/op_668 -- **total equality**
  - go/op_434 / rust/op_224 -- **total equality**
  - go/op_434 / swift/op_668 -- **total equality**
  - rust/op_224 / swift/op_668 -- **total equality**

### sem-identical group B0 V[8:64] S[] E[ret] · (f64,None)

- ground: cluster
- languages: c, cpp
- members: c `sizeof` (f64,None, 0 modes); c `__alignof__` (f64,None, 0 modes); c `__alignof` (f64,None, 0 modes); c `_Alignof` (f64,None, 0 modes); cpp `sizeof` (f64,None, 0 modes)

  - c/op_52 / cpp/op_64 -- **total equality**
  - c/op_58 / cpp/op_64 -- **total equality**
  - c/op_64 / cpp/op_64 -- **total equality**
  - c/op_82 / cpp/op_64 -- **total equality**

### sem-identical group B0 V[8:64] S[] E[ret] · (i64,None)

- ground: cluster
- languages: c, cpp
- members: c `sizeof` (i64,None, 0 modes); c `__alignof__` (i64,None, 0 modes); c `__alignof` (i64,None, 0 modes); c `_Alignof` (i64,None, 0 modes); cpp `sizeof` (i64,None, 0 modes)

  - c/op_49 / cpp/op_61 -- **total equality**
  - c/op_55 / cpp/op_61 -- **total equality**
  - c/op_61 / cpp/op_61 -- **total equality**
  - c/op_79 / cpp/op_61 -- **total equality**

### sem-identical group B0 V[8:64] S[] E[ret] · (u64,None)

- ground: cluster
- languages: c, cpp
- members: c `sizeof` (u64,None, 0 modes); c `__alignof__` (u64,None, 0 modes); c `__alignof` (u64,None, 0 modes); c `_Alignof` (u64,None, 0 modes); cpp `sizeof` (u64,None, 0 modes)

  - c/op_50 / cpp/op_62 -- **total equality**
  - c/op_56 / cpp/op_62 -- **total equality**
  - c/op_62 / cpp/op_62 -- **total equality**
  - c/op_80 / cpp/op_62 -- **total equality**

### sem-identical group B0 V[Add64(in0:64,in1:64)] S[] E[ret] · (i64,i64)

- ground: cluster
- languages: c, cpp, go, rust
- members: c `+` (i64,i64, 1 modes); cpp `+` (i64,i64, 1 modes); go `+` (i64,i64, 1 modes); rust `+` (i64,i64, 1 modes)

  - c/op_109 / cpp/op_109 -- **total equality**
  - c/op_109 / go/op_319 -- **total equality**
  - c/op_109 / rust/op_541 -- **total equality**
  - cpp/op_109 / go/op_319 -- **total equality**
  - cpp/op_109 / rust/op_541 -- **total equality**
  - go/op_319 / rust/op_541 -- **total equality**

### sem-identical group B0 V[Add64(in0:64,in1:64)] S[] E[ret] · (i64,u64)

- ground: cluster
- languages: c, cpp
- members: c `+` (i64,u64, 0 modes); cpp `+` (i64,u64, 0 modes)

  - c/op_110 / cpp/op_110 -- **total equality**

### sem-identical group B0 V[Add64(in0:64,in1:64)] S[] E[ret] · (u64,i64)

- ground: cluster
- languages: c, cpp
- members: c `+` (u64,i64, 0 modes); cpp `+` (u64,i64, 0 modes)

  - c/op_115 / cpp/op_115 -- **total equality**

### sem-identical group B0 V[Add64(in0:64,in1:64)] S[] E[ret] · (u64,u64)

- ground: cluster
- languages: c, cpp, go, rust
- members: c `+` (u64,u64, 1 modes); cpp `+` (u64,u64, 1 modes); go `+` (u64,u64, 1 modes); rust `+` (u64,u64, 1 modes)

  - c/op_116 / cpp/op_116 -- **total equality**
  - c/op_116 / go/op_326 -- **total equality**
  - c/op_116 / rust/op_548 -- **total equality**
  - cpp/op_116 / go/op_326 -- **total equality**
  - cpp/op_116 / rust/op_548 -- **total equality**
  - go/op_326 / rust/op_548 -- **total equality**

### sem-identical group B0 V[Mul64(in0:64,in1:64)] S[] E[ret] · (i64,i64)

- ground: cluster
- languages: c, cpp, go, rust
- members: c `*` (i64,i64, 1 modes); cpp `*` (i64,i64, 1 modes); go `*` (i64,i64, 1 modes); rust `*` (i64,i64, 1 modes)

  - c/op_181 / cpp/op_181 -- **total equality**
  - c/op_181 / go/op_67 -- **total equality**
  - c/op_181 / rust/op_613 -- **total equality**
  - cpp/op_181 / go/op_67 -- **total equality**
  - cpp/op_181 / rust/op_613 -- **total equality**
  - go/op_67 / rust/op_613 -- **total equality**

### sem-identical group B0 V[Mul64(in0:64,in1:64)] S[] E[ret] · (i64,u64)

- ground: cluster
- languages: c, cpp
- members: c `*` (i64,u64, 0 modes); cpp `*` (i64,u64, 0 modes)

  - c/op_182 / cpp/op_182 -- **total equality**

### sem-identical group B0 V[Mul64(in0:64,in1:64)] S[] E[ret] · (u64,i64)

- ground: cluster
- languages: c, cpp
- members: c `*` (u64,i64, 0 modes); cpp `*` (u64,i64, 0 modes)

  - c/op_187 / cpp/op_187 -- **total equality**

### sem-identical group B0 V[Mul64(in0:64,in1:64)] S[] E[ret] · (u64,u64)

- ground: cluster
- languages: c, cpp, go, rust
- members: c `*` (u64,u64, 0 modes); cpp `*` (u64,u64, 0 modes); go `*` (u64,u64, 0 modes); rust `*` (u64,u64, 0 modes)

  - c/op_188 / cpp/op_188 -- **total equality**
  - c/op_188 / go/op_74 -- **total equality**
  - c/op_188 / rust/op_620 -- **total equality**
  - cpp/op_188 / go/op_74 -- **total equality**
  - cpp/op_188 / rust/op_620 -- **total equality**
  - go/op_74 / rust/op_620 -- **total equality**

### sem-identical group B0 V[Not64(in0:64)] S[] E[ret] · (i64,None)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `~` (i64,None, 0 modes); cpp `~` (i64,None, 0 modes); cpp `compl` (i64,None, 0 modes); go `^` (i64,None, 0 modes); rust `!` (i64,None, 0 modes); swift `~` (i64,None, 0 modes)

  - c/op_7 / cpp/op_7 -- **total equality**
  - c/op_7 / cpp/op_31 -- **total equality**
  - c/op_7 / go/op_19 -- **total equality**
  - c/op_7 / rust/op_13 -- **total equality**
  - c/op_7 / swift/op_37 -- **total equality**
  - cpp/op_7 / go/op_19 -- **total equality**
  - cpp/op_31 / go/op_19 -- **total equality**
  - cpp/op_7 / rust/op_13 -- **total equality**
  - cpp/op_31 / rust/op_13 -- **total equality**
  - cpp/op_7 / swift/op_37 -- **total equality**
  - cpp/op_31 / swift/op_37 -- **total equality**
  - go/op_19 / rust/op_13 -- **total equality**
  - go/op_19 / swift/op_37 -- **total equality**
  - rust/op_13 / swift/op_37 -- **total equality**

### sem-identical group B0 V[Not64(in0:64)] S[] E[ret] · (u64,None)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `~` (u64,None, 0 modes); cpp `~` (u64,None, 0 modes); cpp `compl` (u64,None, 0 modes); go `^` (u64,None, 0 modes); rust `!` (u64,None, 0 modes); swift `~` (u64,None, 0 modes)

  - c/op_8 / cpp/op_8 -- **total equality**
  - c/op_8 / cpp/op_32 -- **total equality**
  - c/op_8 / go/op_20 -- **total equality**
  - c/op_8 / rust/op_14 -- **total equality**
  - c/op_8 / swift/op_38 -- **total equality**
  - cpp/op_8 / go/op_20 -- **total equality**
  - cpp/op_32 / go/op_20 -- **total equality**
  - cpp/op_8 / rust/op_14 -- **total equality**
  - cpp/op_32 / rust/op_14 -- **total equality**
  - cpp/op_8 / swift/op_38 -- **total equality**
  - cpp/op_32 / swift/op_38 -- **total equality**
  - go/op_20 / rust/op_14 -- **total equality**
  - go/op_20 / swift/op_38 -- **total equality**
  - rust/op_14 / swift/op_38 -- **total equality**

### sem-identical group B0 V[Shl64(in0:64,And8(63:8,ex8@0(in1:64)))] S[] E[ret] · (i64,i64)

- ground: cluster
- languages: c, cpp, rust
- members: c `<<` (i64,i64, 0 modes); cpp `<<` (i64,i64, 0 modes); rust `<<` (i64,i64, 0 modes)

  - c/op_685 / cpp/op_685 -- **total equality**
  - c/op_685 / rust/op_469 -- **total equality**
  - cpp/op_685 / rust/op_469 -- **total equality**

### sem-identical group B0 V[Shl64(in0:64,And8(63:8,ex8@0(in1:64)))] S[] E[ret] · (i64,u64)

- ground: cluster
- languages: c, cpp, rust
- members: c `<<` (i64,u64, 1 modes); cpp `<<` (i64,u64, 1 modes); rust `<<` (i64,u64, 1 modes)

  - c/op_686 / cpp/op_686 -- **total equality**
  - c/op_686 / rust/op_470 -- **total equality**
  - cpp/op_686 / rust/op_470 -- **total equality**

### sem-identical group B0 V[Shl64(in0:64,And8(63:8,ex8@0(in1:64)))] S[] E[ret] · (u64,i64)

- ground: cluster
- languages: c, cpp, rust
- members: c `<<` (u64,i64, 0 modes); cpp `<<` (u64,i64, 0 modes); rust `<<` (u64,i64, 0 modes)

  - c/op_691 / cpp/op_691 -- **total equality**
  - c/op_691 / rust/op_475 -- **total equality**
  - cpp/op_691 / rust/op_475 -- **total equality**

### sem-identical group B0 V[Shl64(in0:64,And8(63:8,ex8@0(in1:64)))] S[] E[ret] · (u64,u64)

- ground: cluster
- languages: c, cpp, rust
- members: c `<<` (u64,u64, 2 modes); cpp `<<` (u64,u64, 2 modes); rust `<<` (u64,u64, 2 modes)

  - c/op_692 / cpp/op_692 -- **total equality**
  - c/op_692 / rust/op_476 -- **total equality**
  - cpp/op_692 / rust/op_476 -- **total equality**

### sem-identical group B0 V[Sub64(in0:64,in1:64)] S[] E[ret] · (i64,i64)

- ground: cluster
- languages: c, cpp, go, rust
- members: c `-` (i64,i64, 1 modes); cpp `-` (i64,i64, 1 modes); go `-` (i64,i64, 1 modes); rust `-` (i64,i64, 1 modes)

  - c/op_145 / cpp/op_145 -- **total equality**
  - c/op_145 / go/op_355 -- **total equality**
  - c/op_145 / rust/op_577 -- **total equality**
  - cpp/op_145 / go/op_355 -- **total equality**
  - cpp/op_145 / rust/op_577 -- **total equality**
  - go/op_355 / rust/op_577 -- **total equality**

### sem-identical group B0 V[Sub64(in0:64,in1:64)] S[] E[ret] · (i64,u64)

- ground: cluster
- languages: c, cpp
- members: c `-` (i64,u64, 0 modes); cpp `-` (i64,u64, 0 modes)

  - c/op_146 / cpp/op_146 -- **total equality**

### sem-identical group B0 V[Sub64(in0:64,in1:64)] S[] E[ret] · (u64,i64)

- ground: cluster
- languages: c, cpp
- members: c `-` (u64,i64, 0 modes); cpp `-` (u64,i64, 0 modes)

  - c/op_151 / cpp/op_151 -- **total equality**

### sem-identical group B0 V[Sub64(in0:64,in1:64)] S[] E[ret] · (u64,u64)

- ground: cluster
- languages: c, cpp, go, rust
- members: c `-` (u64,u64, 0 modes); cpp `-` (u64,u64, 0 modes); go `-` (u64,u64, 0 modes); rust `-` (u64,u64, 0 modes)

  - c/op_152 / cpp/op_152 -- **total equality**
  - c/op_152 / go/op_362 -- **total equality**
  - c/op_152 / rust/op_584 -- **total equality**
  - cpp/op_152 / go/op_362 -- **total equality**
  - cpp/op_152 / rust/op_584 -- **total equality**
  - go/op_362 / rust/op_584 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(5:64,8:64,in0:64,in1:64,u0:64)))] S[] E[ret] · (i64,i64)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `!=` (i64,i64, 0 modes); cpp `not_eq` (i64,i64, 0 modes); rust `!=` (i64,i64, 0 modes); swift `!=` (i64,i64, 0 modes)

  - cpp/op_505 / rust/op_289 -- **total equality**
  - cpp/op_973 / rust/op_289 -- **total equality**
  - cpp/op_505 / swift/op_445 -- **total equality**
  - cpp/op_973 / swift/op_445 -- **total equality**
  - rust/op_289 / swift/op_445 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(5:64,8:64,in0:64,in1:64,u0:64)))] S[] E[ret] · (u64,u64)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `!=` (u64,u64, 0 modes); cpp `not_eq` (u64,u64, 0 modes); rust `!=` (u64,u64, 0 modes); swift `!=` (u64,u64, 0 modes)

  - cpp/op_512 / rust/op_296 -- **total equality**
  - cpp/op_980 / rust/op_296 -- **total equality**
  - cpp/op_512 / swift/op_452 -- **total equality**
  - cpp/op_980 / swift/op_452 -- **total equality**
  - rust/op_296 / swift/op_452 -- **total equality**

### sem-identical group B0 V[4:64] S[] E[ret] · (f32,None)

- ground: cluster
- languages: c, cpp
- members: c `sizeof` (f32,None, 0 modes); c `__alignof__` (f32,None, 0 modes); c `__alignof` (f32,None, 0 modes); c `_Alignof` (f32,None, 0 modes); cpp `sizeof` (f32,None, 0 modes)

  - c/op_51 / cpp/op_63 -- **total equality**
  - c/op_57 / cpp/op_63 -- **total equality**
  - c/op_63 / cpp/op_63 -- **total equality**
  - c/op_81 / cpp/op_63 -- **total equality**

### sem-identical group B0 V[4:64] S[] E[ret] · (i32,None)

- ground: cluster
- languages: c, cpp
- members: c `sizeof` (i32,None, 0 modes); c `__alignof__` (i32,None, 0 modes); c `__alignof` (i32,None, 0 modes); c `_Alignof` (i32,None, 0 modes); cpp `sizeof` (i32,None, 0 modes)

  - c/op_48 / cpp/op_60 -- **total equality**
  - c/op_54 / cpp/op_60 -- **total equality**
  - c/op_60 / cpp/op_60 -- **total equality**
  - c/op_78 / cpp/op_60 -- **total equality**

### sem-identical group B0 V[Shl64(in0:64,And8(63:8,ex8@0(in1:64))) zx64(ex32@0(in1:64))] S[] E[ret] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `<<` (i64,bool, 0 modes); cpp `<<` (i64,bool, 0 modes)

  - c/op_689 / cpp/op_689 -- **total equality**

### sem-identical group B0 V[Shl64(in0:64,And8(63:8,ex8@0(in1:64))) zx64(ex32@0(in1:64))] S[] E[ret] · (i64,i32)

- ground: cluster
- languages: c, cpp, rust
- members: c `<<` (i64,i32, 0 modes); cpp `<<` (i64,i32, 0 modes); rust `<<` (i64,i32, 0 modes)

  - c/op_684 / cpp/op_684 -- **total equality**
  - c/op_684 / rust/op_468 -- **total equality**
  - cpp/op_684 / rust/op_468 -- **total equality**

### sem-identical group B0 V[Shl64(in0:64,And8(63:8,ex8@0(in1:64))) zx64(ex32@0(in1:64))] S[] E[ret] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `<<` (u64,bool, 0 modes); cpp `<<` (u64,bool, 0 modes)

  - c/op_695 / cpp/op_695 -- **total equality**

### sem-identical group B0 V[Shl64(in0:64,And8(63:8,ex8@0(in1:64))) zx64(ex32@0(in1:64))] S[] E[ret] · (u64,i32)

- ground: cluster
- languages: c, cpp, rust
- members: c `<<` (u64,i32, 0 modes); cpp `<<` (u64,i32, 0 modes); rust `<<` (u64,i32, 0 modes)

  - c/op_690 / cpp/op_690 -- **total equality**
  - c/op_690 / rust/op_474 -- **total equality**
  - cpp/op_690 / rust/op_474 -- **total equality**

### sem-identical group B0 V[zx64(Add32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (bool,bool)

- ground: cluster
- languages: c, cpp
- members: c `+` (bool,bool, 0 modes); cpp `+` (bool,bool, 0 modes)

  - c/op_137 / cpp/op_137 -- **total equality**

### sem-identical group B0 V[zx64(Add32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `+` (bool,i32, 0 modes); cpp `+` (bool,i32, 0 modes)

  - c/op_132 / cpp/op_132 -- **total equality**

### sem-identical group B0 V[zx64(Add32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `+` (i32,bool, 0 modes); cpp `+` (i32,bool, 0 modes)

  - c/op_107 / cpp/op_107 -- **total equality**

### sem-identical group B0 V[zx64(Add32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (i32,i32)

- ground: cluster
- languages: c, cpp, go, rust
- members: c `+` (i32,i32, 1 modes); cpp `+` (i32,i32, 1 modes); go `+` (i32,i32, 1 modes); rust `+` (i32,i32, 1 modes)

  - c/op_102 / cpp/op_102 -- **total equality**
  - c/op_102 / go/op_312 -- **total equality**
  - c/op_102 / rust/op_534 -- **total equality**
  - cpp/op_102 / go/op_312 -- **total equality**
  - cpp/op_102 / rust/op_534 -- **total equality**
  - go/op_312 / rust/op_534 -- **total equality**

### sem-identical group B0 V[zx64(Sub32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (bool,bool)

- ground: cluster
- languages: c, cpp
- members: c `-` (bool,bool, 0 modes); cpp `-` (bool,bool, 0 modes)

  - c/op_173 / cpp/op_173 -- **total equality**

### sem-identical group B0 V[zx64(Sub32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `-` (bool,i32, 0 modes); cpp `-` (bool,i32, 0 modes)

  - c/op_168 / cpp/op_168 -- **total equality**

### sem-identical group B0 V[zx64(Sub32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `-` (i32,bool, 0 modes); cpp `-` (i32,bool, 0 modes)

  - c/op_143 / cpp/op_143 -- **total equality**

### sem-identical group B0 V[zx64(Sub32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (i32,i32)

- ground: cluster
- languages: c, cpp, go, rust
- members: c `-` (i32,i32, 1 modes); cpp `-` (i32,i32, 1 modes); go `-` (i32,i32, 1 modes); rust `-` (i32,i32, 1 modes)

  - c/op_138 / cpp/op_138 -- **total equality**
  - c/op_138 / go/op_348 -- **total equality**
  - c/op_138 / rust/op_570 -- **total equality**
  - cpp/op_138 / go/op_348 -- **total equality**
  - cpp/op_138 / rust/op_570 -- **total equality**
  - go/op_348 / rust/op_570 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))] S[] E[ret] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `<<` (bool,i64, 0 modes); cpp `<<` (bool,i64, 0 modes)

  - c/op_709 / cpp/op_709 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))] S[] E[ret] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `<<` (bool,u64, 0 modes); cpp `<<` (bool,u64, 0 modes)

  - c/op_710 / cpp/op_710 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))] S[] E[ret] · (i32,i64)

- ground: cluster
- languages: c, cpp, rust
- members: c `<<` (i32,i64, 0 modes); cpp `<<` (i32,i64, 0 modes); rust `<<` (i32,i64, 0 modes)

  - c/op_679 / cpp/op_679 -- **total equality**
  - c/op_679 / rust/op_463 -- **total equality**
  - cpp/op_679 / rust/op_463 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))] S[] E[ret] · (i32,u64)

- ground: cluster
- languages: c, cpp, rust
- members: c `<<` (i32,u64, 1 modes); cpp `<<` (i32,u64, 1 modes); rust `<<` (i32,u64, 1 modes)

  - c/op_680 / cpp/op_680 -- **total equality**
  - c/op_680 / rust/op_464 -- **total equality**
  - cpp/op_680 / rust/op_464 -- **total equality**

### sem-identical group B0 V[zx64(Not32(ex32@0(in0:64)))] S[] E[ret] · (bool,None)

- ground: cluster
- languages: c, cpp
- members: c `~` (bool,None, 0 modes); cpp `~` (bool,None, 0 modes); cpp `compl` (bool,None, 0 modes)

  - c/op_11 / cpp/op_11 -- **total equality**
  - c/op_11 / cpp/op_35 -- **total equality**

### sem-identical group B0 V[zx64(Not32(ex32@0(in0:64)))] S[] E[ret] · (i32,None)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `~` (i32,None, 0 modes); cpp `~` (i32,None, 0 modes); cpp `compl` (i32,None, 0 modes); go `^` (i32,None, 0 modes); rust `!` (i32,None, 0 modes); swift `~` (i32,None, 0 modes)

  - c/op_6 / cpp/op_6 -- **total equality**
  - c/op_6 / cpp/op_30 -- **total equality**
  - c/op_6 / go/op_18 -- **total equality**
  - c/op_6 / rust/op_12 -- **total equality**
  - c/op_6 / swift/op_36 -- **total equality**
  - cpp/op_6 / go/op_18 -- **total equality**
  - cpp/op_30 / go/op_18 -- **total equality**
  - cpp/op_6 / rust/op_12 -- **total equality**
  - cpp/op_30 / rust/op_12 -- **total equality**
  - cpp/op_6 / swift/op_36 -- **total equality**
  - cpp/op_30 / swift/op_36 -- **total equality**
  - go/op_18 / rust/op_12 -- **total equality**
  - go/op_18 / swift/op_36 -- **total equality**
  - rust/op_12 / swift/op_36 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) zx64(ex32@0(in1:64))] S[] E[ret] · (bool,bool)

- ground: cluster
- languages: c, cpp
- members: c `<<` (bool,bool, 0 modes); cpp `<<` (bool,bool, 0 modes)

  - c/op_713 / cpp/op_713 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) zx64(ex32@0(in1:64))] S[] E[ret] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `<<` (bool,i32, 0 modes); cpp `<<` (bool,i32, 0 modes)

  - c/op_708 / cpp/op_708 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) zx64(ex32@0(in1:64))] S[] E[ret] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `<<` (i32,bool, 0 modes); cpp `<<` (i32,bool, 0 modes)

  - c/op_683 / cpp/op_683 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) zx64(ex32@0(in1:64))] S[] E[ret] · (i32,i32)

- ground: cluster
- languages: c, cpp, rust
- members: c `<<` (i32,i32, 0 modes); cpp `<<` (i32,i32, 0 modes); rust `<<` (i32,i32, 0 modes)

  - c/op_678 / cpp/op_678 -- **total equality**
  - c/op_678 / rust/op_462 -- **total equality**
  - cpp/op_678 / rust/op_462 -- **total equality**

### sem-identical group B0 V[0:64] S[] E[ret] · (bool,bool)

- ground: cluster
- languages: c, cpp
- members: c `%` (bool,bool, 0 modes); cpp `%` (bool,bool, 0 modes)

  - c/op_281 / cpp/op_281 -- **total equality**

### sem-identical group B0 V[0:64] S[] E[ret] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `%` (i32,bool, 0 modes); cpp `%` (i32,bool, 0 modes)

  - c/op_251 / cpp/op_251 -- **total equality**

### sem-identical group B0 V[0:64] S[] E[ret] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `%` (i64,bool, 0 modes); cpp `%` (i64,bool, 0 modes)

  - c/op_257 / cpp/op_257 -- **total equality**

### sem-identical group B0 V[0:64] S[] E[ret] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `%` (u64,bool, 0 modes); cpp `%` (u64,bool, 0 modes)

  - c/op_263 / cpp/op_263 -- **total equality**

### sem-identical group B0 V[XorV128(ex128@0(in0:256),ld128/g0(7:64))] S[] E[riprel xorps | ret] · (f32,None)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `-` (f32,None, 0 modes); cpp `-` (f32,None, 0 modes); rust `-` (f32,None, 0 modes); swift `-` (f32,None, 0 modes)

  - c/op_15 / cpp/op_15 -- **total equality**
  - c/op_15 / rust/op_3 -- **total equality**
  - c/op_15 / swift/op_15 -- **total equality**
  - cpp/op_15 / rust/op_3 -- **total equality**
  - cpp/op_15 / swift/op_15 -- **total equality**
  - rust/op_3 / swift/op_15 -- **total equality**

### sem-identical group B0 V[XorV128(ex128@0(in0:256),ld128/g0(7:64))] S[] E[riprel xorps | ret] · (f64,None)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `-` (f64,None, 0 modes); cpp `-` (f64,None, 0 modes); rust `-` (f64,None, 0 modes); swift `-` (f64,None, 0 modes)

  - c/op_16 / cpp/op_16 -- **total equality**
  - c/op_16 / rust/op_4 -- **total equality**
  - c/op_16 / swift/op_16 -- **total equality**
  - cpp/op_16 / rust/op_4 -- **total equality**
  - cpp/op_16 / swift/op_16 -- **total equality**
  - rust/op_4 / swift/op_16 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(4:64,8:64,in0:64,in1:64,u0:64)))] S[] E[ret] · (i64,i64)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `==` (i64,i64, 0 modes); rust `==` (i64,i64, 0 modes); swift `==` (i64,i64, 0 modes)

  - cpp/op_469 / rust/op_253 -- **total equality**
  - cpp/op_469 / swift/op_517 -- **total equality**
  - rust/op_253 / swift/op_517 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(4:64,8:64,in0:64,in1:64,u0:64)))] S[] E[ret] · (u64,u64)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `==` (u64,u64, 0 modes); rust `==` (u64,u64, 0 modes); swift `==` (u64,u64, 0 modes)

  - cpp/op_476 / rust/op_260 -- **total equality**
  - cpp/op_476 / swift/op_524 -- **total equality**
  - rust/op_260 / swift/op_524 -- **total equality**

### sem-identical group B0 V[Sub64(0:64,in0:64)] S[] E[ret] · (i64,None)

- ground: cluster
- languages: c, cpp, go, rust
- members: c `-` (i64,None, 1 modes); cpp `-` (i64,None, 1 modes); go `-` (i64,None, 1 modes); rust `-` (i64,None, 1 modes)

  - c/op_13 / cpp/op_13 -- **total equality**
  - c/op_13 / go/op_7 -- **total equality**
  - c/op_13 / rust/op_1 -- **total equality**
  - cpp/op_13 / go/op_7 -- **total equality**
  - cpp/op_13 / rust/op_1 -- **total equality**
  - go/op_7 / rust/op_1 -- **total equality**

### sem-identical group B0 V[Sub64(0:64,in0:64)] S[] E[ret] · (u64,None)

- ground: cluster
- languages: c, cpp, go
- members: c `-` (u64,None, 0 modes); cpp `-` (u64,None, 0 modes); go `-` (u64,None, 0 modes)

  - c/op_14 / cpp/op_14 -- **total equality**
  - c/op_14 / go/op_8 -- **total equality**
  - cpp/op_14 / go/op_8 -- **total equality**

### sem-identical group B0 V[And64(in0:64,sx64(ex32@0(in1:64)))] S[] E[ret] · (i64,i32)

- ground: cluster
- languages: c, cpp
- members: c `&` (i64,i32, 0 modes); cpp `&` (i64,i32, 0 modes); cpp `bitand` (i64,i32, 0 modes)

  - c/op_432 / cpp/op_432 -- **total equality**
  - c/op_432 / cpp/op_936 -- **total equality**

### sem-identical group B0 V[And64(in0:64,sx64(ex32@0(in1:64)))] S[] E[ret] · (u64,i32)

- ground: cluster
- languages: c, cpp
- members: c `&` (u64,i32, 0 modes); cpp `&` (u64,i32, 0 modes); cpp `bitand` (u64,i32, 0 modes)

  - c/op_438 / cpp/op_438 -- **total equality**
  - c/op_438 / cpp/op_942 -- **total equality**

### sem-identical group B0 V[And64(in1:64,sx64(ex32@0(in0:64)))] S[] E[ret] · (i32,i64)

- ground: cluster
- languages: c, cpp
- members: c `&` (i32,i64, 0 modes); cpp `&` (i32,i64, 0 modes); cpp `bitand` (i32,i64, 0 modes)

  - c/op_427 / cpp/op_427 -- **total equality**
  - c/op_427 / cpp/op_931 -- **total equality**

### sem-identical group B0 V[And64(in1:64,sx64(ex32@0(in0:64)))] S[] E[ret] · (i32,u64)

- ground: cluster
- languages: c, cpp
- members: c `&` (i32,u64, 0 modes); cpp `&` (i32,u64, 0 modes); cpp `bitand` (i32,u64, 0 modes)

  - c/op_428 / cpp/op_428 -- **total equality**
  - c/op_428 / cpp/op_932 -- **total equality**

### sem-identical group B0 V[Or64(in0:64,sx64(ex32@0(in1:64)))] S[] E[ret] · (i64,i32)

- ground: cluster
- languages: c, cpp
- members: c `|` (i64,i32, 0 modes); cpp `|` (i64,i32, 0 modes); cpp `bitor` (i64,i32, 0 modes)

  - c/op_360 / cpp/op_360 -- **total equality**
  - c/op_360 / cpp/op_864 -- **total equality**

### sem-identical group B0 V[Or64(in0:64,sx64(ex32@0(in1:64)))] S[] E[ret] · (u64,i32)

- ground: cluster
- languages: c, cpp
- members: c `|` (u64,i32, 0 modes); cpp `|` (u64,i32, 0 modes); cpp `bitor` (u64,i32, 0 modes)

  - c/op_366 / cpp/op_366 -- **total equality**
  - c/op_366 / cpp/op_870 -- **total equality**

### sem-identical group B0 V[Or64(in0:64,zx64(ex32@0(in1:64)))] S[] E[ret] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `|` (i64,bool, 0 modes); cpp `|` (i64,bool, 0 modes); cpp `bitor` (i64,bool, 0 modes)

  - c/op_365 / cpp/op_365 -- **total equality**
  - c/op_365 / cpp/op_869 -- **total equality**

### sem-identical group B0 V[Or64(in0:64,zx64(ex32@0(in1:64)))] S[] E[ret] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `|` (u64,bool, 0 modes); cpp `|` (u64,bool, 0 modes); cpp `bitor` (u64,bool, 0 modes)

  - c/op_371 / cpp/op_371 -- **total equality**
  - c/op_371 / cpp/op_875 -- **total equality**

### sem-identical group B0 V[Or64(in1:64,sx64(ex32@0(in0:64)))] S[] E[ret] · (i32,i64)

- ground: cluster
- languages: c, cpp
- members: c `|` (i32,i64, 0 modes); cpp `|` (i32,i64, 0 modes); cpp `bitor` (i32,i64, 0 modes)

  - c/op_355 / cpp/op_355 -- **total equality**
  - c/op_355 / cpp/op_859 -- **total equality**

### sem-identical group B0 V[Or64(in1:64,sx64(ex32@0(in0:64)))] S[] E[ret] · (i32,u64)

- ground: cluster
- languages: c, cpp
- members: c `|` (i32,u64, 0 modes); cpp `|` (i32,u64, 0 modes); cpp `bitor` (i32,u64, 0 modes)

  - c/op_356 / cpp/op_356 -- **total equality**
  - c/op_356 / cpp/op_860 -- **total equality**

### sem-identical group B0 V[Or64(in1:64,zx64(ex32@0(in0:64)))] S[] E[ret] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `|` (bool,i64, 0 modes); cpp `|` (bool,i64, 0 modes); cpp `bitor` (bool,i64, 0 modes)

  - c/op_385 / cpp/op_385 -- **total equality**
  - c/op_385 / cpp/op_889 -- **total equality**

### sem-identical group B0 V[Or64(in1:64,zx64(ex32@0(in0:64)))] S[] E[ret] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `|` (bool,u64, 0 modes); cpp `|` (bool,u64, 0 modes); cpp `bitor` (bool,u64, 0 modes)

  - c/op_386 / cpp/op_386 -- **total equality**
  - c/op_386 / cpp/op_890 -- **total equality**

### sem-identical group B0 V[Sar64(in0:64,And8(63:8,ex8@0(in1:64)))] S[] E[ret] · (i64,i64)

- ground: cluster
- languages: c, cpp, rust
- members: c `>>` (i64,i64, 0 modes); cpp `>>` (i64,i64, 0 modes); rust `>>` (i64,i64, 0 modes)

  - c/op_721 / cpp/op_721 -- **total equality**
  - c/op_721 / rust/op_505 -- **total equality**
  - cpp/op_721 / rust/op_505 -- **total equality**

### sem-identical group B0 V[Sar64(in0:64,And8(63:8,ex8@0(in1:64)))] S[] E[ret] · (i64,u64)

- ground: cluster
- languages: c, cpp, rust
- members: c `>>` (i64,u64, 0 modes); cpp `>>` (i64,u64, 0 modes); rust `>>` (i64,u64, 0 modes)

  - c/op_722 / cpp/op_722 -- **total equality**
  - c/op_722 / rust/op_506 -- **total equality**
  - cpp/op_722 / rust/op_506 -- **total equality**

### sem-identical group B0 V[Shr64(in0:64,And8(63:8,ex8@0(in1:64)))] S[] E[ret] · (u64,i64)

- ground: cluster
- languages: c, cpp, rust
- members: c `>>` (u64,i64, 0 modes); cpp `>>` (u64,i64, 0 modes); rust `>>` (u64,i64, 0 modes)

  - c/op_727 / cpp/op_727 -- **total equality**
  - c/op_727 / rust/op_511 -- **total equality**
  - cpp/op_727 / rust/op_511 -- **total equality**

### sem-identical group B0 V[Shr64(in0:64,And8(63:8,ex8@0(in1:64)))] S[] E[ret] · (u64,u64)

- ground: cluster
- languages: c, cpp, rust
- members: c `>>` (u64,u64, 2 modes); cpp `>>` (u64,u64, 2 modes); rust `>>` (u64,u64, 2 modes)

  - c/op_728 / cpp/op_728 -- **total equality**
  - c/op_728 / rust/op_512 -- **total equality**
  - cpp/op_728 / rust/op_512 -- **total equality**

### sem-identical group B0 V[Xor64(in0:64,sx64(ex32@0(in1:64)))] S[] E[ret] · (i64,i32)

- ground: cluster
- languages: c, cpp
- members: c `^` (i64,i32, 0 modes); cpp `^` (i64,i32, 0 modes); cpp `xor` (i64,i32, 0 modes)

  - c/op_396 / cpp/op_396 -- **total equality**
  - c/op_396 / cpp/op_900 -- **total equality**

### sem-identical group B0 V[Xor64(in0:64,sx64(ex32@0(in1:64)))] S[] E[ret] · (u64,i32)

- ground: cluster
- languages: c, cpp
- members: c `^` (u64,i32, 0 modes); cpp `^` (u64,i32, 0 modes); cpp `xor` (u64,i32, 0 modes)

  - c/op_402 / cpp/op_402 -- **total equality**
  - c/op_402 / cpp/op_906 -- **total equality**

### sem-identical group B0 V[Xor64(in0:64,zx64(ex32@0(in1:64)))] S[] E[ret] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `^` (i64,bool, 0 modes); cpp `^` (i64,bool, 0 modes); cpp `xor` (i64,bool, 0 modes)

  - c/op_401 / cpp/op_401 -- **total equality**
  - c/op_401 / cpp/op_905 -- **total equality**

### sem-identical group B0 V[Xor64(in0:64,zx64(ex32@0(in1:64)))] S[] E[ret] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `^` (u64,bool, 0 modes); cpp `^` (u64,bool, 0 modes); cpp `xor` (u64,bool, 0 modes)

  - c/op_407 / cpp/op_407 -- **total equality**
  - c/op_407 / cpp/op_911 -- **total equality**

### sem-identical group B0 V[Xor64(in1:64,sx64(ex32@0(in0:64)))] S[] E[ret] · (i32,i64)

- ground: cluster
- languages: c, cpp
- members: c `^` (i32,i64, 0 modes); cpp `^` (i32,i64, 0 modes); cpp `xor` (i32,i64, 0 modes)

  - c/op_391 / cpp/op_391 -- **total equality**
  - c/op_391 / cpp/op_895 -- **total equality**

### sem-identical group B0 V[Xor64(in1:64,sx64(ex32@0(in0:64)))] S[] E[ret] · (i32,u64)

- ground: cluster
- languages: c, cpp
- members: c `^` (i32,u64, 0 modes); cpp `^` (i32,u64, 0 modes); cpp `xor` (i32,u64, 0 modes)

  - c/op_392 / cpp/op_392 -- **total equality**
  - c/op_392 / cpp/op_896 -- **total equality**

### sem-identical group B0 V[Xor64(in1:64,zx64(ex32@0(in0:64)))] S[] E[ret] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `^` (bool,i64, 0 modes); cpp `^` (bool,i64, 0 modes); cpp `xor` (bool,i64, 0 modes)

  - c/op_421 / cpp/op_421 -- **total equality**
  - c/op_421 / cpp/op_925 -- **total equality**

### sem-identical group B0 V[Xor64(in1:64,zx64(ex32@0(in0:64)))] S[] E[ret] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `^` (bool,u64, 0 modes); cpp `^` (bool,u64, 0 modes); cpp `xor` (bool,u64, 0 modes)

  - c/op_422 / cpp/op_422 -- **total equality**
  - c/op_422 / cpp/op_926 -- **total equality**

### sem-identical group B0 V[ex64@0(DivModU128to64(64HLto128(0:64,in0:64),in1:64)) ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64))] S[] E[ret] · (i64,u64)

- ground: cluster
- languages: c, cpp
- members: c `/` (i64,u64, 0 modes); cpp `/` (i64,u64, 0 modes)

  - c/op_218 / cpp/op_218 -- **total equality**

### sem-identical group B0 V[ex64@0(DivModU128to64(64HLto128(0:64,in0:64),in1:64)) ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64))] S[] E[ret] · (u64,i64)

- ground: cluster
- languages: c, cpp
- members: c `/` (u64,i64, 0 modes); cpp `/` (u64,i64, 0 modes)

  - c/op_223 / cpp/op_223 -- **total equality**

### sem-identical group B0 V[ex64@0(DivModU128to64(64HLto128(0:64,in0:64),in1:64)) ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64))] S[] E[ret] · (u64,u64)

- ground: cluster
- languages: c, cpp
- members: c `/` (u64,u64, 0 modes); cpp `/` (u64,u64, 0 modes)

  - c/op_224 / cpp/op_224 -- **total equality**

### sem-identical group B0 V[ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64)) ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64))] S[] E[ret] · (i64,u64)

- ground: cluster
- languages: c, cpp
- members: c `%` (i64,u64, 0 modes); cpp `%` (i64,u64, 0 modes)

  - c/op_254 / cpp/op_254 -- **total equality**

### sem-identical group B0 V[ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64)) ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64))] S[] E[ret] · (u64,i64)

- ground: cluster
- languages: c, cpp
- members: c `%` (u64,i64, 0 modes); cpp `%` (u64,i64, 0 modes)

  - c/op_259 / cpp/op_259 -- **total equality**

### sem-identical group B0 V[ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64)) ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64))] S[] E[ret] · (u64,u64)

- ground: cluster
- languages: c, cpp
- members: c `%` (u64,u64, 0 modes); cpp `%` (u64,u64, 0 modes)

  - c/op_260 / cpp/op_260 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))),XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256)))) zx64(And32(1:32,ex32@0(XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256))))))] S[] E[ret] · (bool,f32)

- ground: cluster
- languages: c, cpp
- members: c `!=` (bool,f32, 0 modes); cpp `!=` (bool,f32, 0 modes); cpp `not_eq` (bool,f32, 0 modes)

  - c/op_531 / cpp/op_531 -- **total equality**
  - c/op_531 / cpp/op_999 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))),XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256)))) zx64(And32(1:32,ex32@0(XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256))))))] S[] E[ret] · (i32,f32)

- ground: cluster
- languages: c, cpp
- members: c `!=` (i32,f32, 0 modes); cpp `!=` (i32,f32, 0 modes); cpp `not_eq` (i32,f32, 0 modes)

  - c/op_501 / cpp/op_501 -- **total equality**
  - c/op_501 / cpp/op_969 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64)))),XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))),ex128@0(in0:256)))) zx64(And32(1:32,ex32@0(XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))),ex128@0(in0:256))))))] S[] E[ret] · (f32,bool)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f32,bool, 0 modes); cpp `!=` (f32,bool, 0 modes); cpp `not_eq` (f32,bool, 0 modes)

  - c/op_521 / cpp/op_521 -- **total equality**
  - c/op_521 / cpp/op_989 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64)))),XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))),ex128@0(in0:256)))) zx64(And32(1:32,ex32@0(XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))),ex128@0(in0:256))))))] S[] E[ret] · (f32,i32)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f32,i32, 0 modes); cpp `!=` (f32,i32, 0 modes); cpp `not_eq` (f32,i32, 0 modes)

  - c/op_516 / cpp/op_516 -- **total equality**
  - c/op_516 / cpp/op_984 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))),XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256)))) zx64(And32(1:32,ex32@0(XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256))))))] S[] E[ret] · (bool,f64)

- ground: cluster
- languages: c, cpp
- members: c `!=` (bool,f64, 0 modes); cpp `!=` (bool,f64, 0 modes); cpp `not_eq` (bool,f64, 0 modes)

  - c/op_532 / cpp/op_532 -- **total equality**
  - c/op_532 / cpp/op_1000 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))),XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256)))) zx64(And32(1:32,ex32@0(XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256))))))] S[] E[ret] · (i32,f64)

- ground: cluster
- languages: c, cpp
- members: c `!=` (i32,f64, 0 modes); cpp `!=` (i32,f64, 0 modes); cpp `not_eq` (i32,f64, 0 modes)

  - c/op_502 / cpp/op_502 -- **total equality**
  - c/op_502 / cpp/op_970 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))),XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))),ex128@0(in0:256)))) zx64(And32(1:32,ex32@0(XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))),ex128@0(in0:256))))))] S[] E[ret] · (f64,bool)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f64,bool, 0 modes); cpp `!=` (f64,bool, 0 modes); cpp `not_eq` (f64,bool, 0 modes)

  - c/op_527 / cpp/op_527 -- **total equality**
  - c/op_527 / cpp/op_995 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))),XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))),ex128@0(in0:256)))) zx64(And32(1:32,ex32@0(XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))),ex128@0(in0:256))))))] S[] E[ret] · (f64,i32)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f64,i32, 0 modes); cpp `!=` (f64,i32, 0 modes); cpp `not_eq` (f64,i32, 0 modes)

  - c/op_522 / cpp/op_522 -- **total equality**
  - c/op_522 / cpp/op_990 -- **total equality**

### sem-identical group B0 V[zx64(Sub32(0:32,ex32@0(in0:64)))] S[] E[ret] · (bool,None)

- ground: cluster
- languages: c, cpp
- members: c `-` (bool,None, 0 modes); cpp `-` (bool,None, 0 modes)

  - c/op_17 / cpp/op_17 -- **total equality**

### sem-identical group B0 V[zx64(Sub32(0:32,ex32@0(in0:64)))] S[] E[ret] · (i32,None)

- ground: cluster
- languages: c, cpp, go, rust
- members: c `-` (i32,None, 1 modes); cpp `-` (i32,None, 1 modes); go `-` (i32,None, 1 modes); rust `-` (i32,None, 1 modes)

  - c/op_12 / cpp/op_12 -- **total equality**
  - c/op_12 / go/op_6 -- **total equality**
  - c/op_12 / rust/op_0 -- **total equality**
  - cpp/op_12 / go/op_6 -- **total equality**
  - cpp/op_12 / rust/op_0 -- **total equality**
  - go/op_6 / rust/op_0 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))] S[] E[ret] · (i32,i64)

- ground: cluster
- languages: c, cpp, rust
- members: c `>>` (i32,i64, 0 modes); cpp `>>` (i32,i64, 0 modes); rust `>>` (i32,i64, 0 modes)

  - c/op_715 / cpp/op_715 -- **total equality**
  - c/op_715 / rust/op_499 -- **total equality**
  - cpp/op_715 / rust/op_499 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))] S[] E[ret] · (i32,u64)

- ground: cluster
- languages: c, cpp, rust
- members: c `>>` (i32,u64, 0 modes); cpp `>>` (i32,u64, 0 modes); rust `>>` (i32,u64, 0 modes)

  - c/op_716 / cpp/op_716 -- **total equality**
  - c/op_716 / rust/op_500 -- **total equality**
  - cpp/op_716 / rust/op_500 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(5:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64)))] S[] E[ret] · (i32,i32)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `!=` (i32,i32, 0 modes); cpp `not_eq` (i32,i32, 0 modes); rust `!=` (i32,i32, 0 modes); swift `!=` (i32,i32, 0 modes)

  - cpp/op_498 / rust/op_282 -- **total equality**
  - cpp/op_966 / rust/op_282 -- **total equality**
  - cpp/op_498 / swift/op_438 -- **total equality**
  - cpp/op_966 / swift/op_438 -- **total equality**
  - rust/op_282 / swift/op_438 -- **total equality**

### sem-identical group B0 V[1:64] S[] E[ret] · (bool,None)

- ground: cluster
- languages: c, cpp
- members: c `sizeof` (bool,None, 0 modes); c `__alignof__` (bool,None, 0 modes); c `__alignof` (bool,None, 0 modes); c `_Alignof` (bool,None, 0 modes); cpp `sizeof` (bool,None, 0 modes)

  - c/op_53 / cpp/op_65 -- **total equality**
  - c/op_59 / cpp/op_65 -- **total equality**
  - c/op_65 / cpp/op_65 -- **total equality**
  - c/op_83 / cpp/op_65 -- **total equality**

### sem-identical group B0 V[Add32F0x4(ex128@0(in0:256),ex128@0(in1:256))] S[] E[ret] · (f32,f32)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `+` (f32,f32, 0 modes); cpp `+` (f32,f32, 0 modes); go `+` (f32,f32, 0 modes); rust `+` (f32,f32, 0 modes); swift `+` (f32,f32, 0 modes)

  - c/op_123 / cpp/op_123 -- **total equality**
  - c/op_123 / go/op_333 -- **total equality**
  - c/op_123 / rust/op_555 -- **total equality**
  - c/op_123 / swift/op_243 -- **total equality**
  - cpp/op_123 / go/op_333 -- **total equality**
  - cpp/op_123 / rust/op_555 -- **total equality**
  - cpp/op_123 / swift/op_243 -- **total equality**
  - go/op_333 / rust/op_555 -- **total equality**
  - go/op_333 / swift/op_243 -- **total equality**
  - rust/op_555 / swift/op_243 -- **total equality**

### sem-identical group B0 V[Add64F0x2(ex128@0(in0:256),ex128@0(in1:256))] S[] E[ret] · (f64,f64)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `+` (f64,f64, 0 modes); cpp `+` (f64,f64, 0 modes); go `+` (f64,f64, 0 modes); rust `+` (f64,f64, 0 modes); swift `+` (f64,f64, 0 modes)

  - c/op_130 / cpp/op_130 -- **total equality**
  - c/op_130 / go/op_340 -- **total equality**
  - c/op_130 / rust/op_562 -- **total equality**
  - c/op_130 / swift/op_250 -- **total equality**
  - cpp/op_130 / go/op_340 -- **total equality**
  - cpp/op_130 / rust/op_562 -- **total equality**
  - cpp/op_130 / swift/op_250 -- **total equality**
  - go/op_340 / rust/op_562 -- **total equality**
  - go/op_340 / swift/op_250 -- **total equality**
  - rust/op_562 / swift/op_250 -- **total equality**

### sem-identical group B0 V[Div32F0x4(ex128@0(in0:256),ex128@0(in1:256))] S[] E[ret] · (f32,f32)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `/` (f32,f32, 0 modes); cpp `/` (f32,f32, 0 modes); go `/` (f32,f32, 0 modes); rust `/` (f32,f32, 0 modes); swift `/` (f32,f32, 0 modes)

  - c/op_231 / cpp/op_231 -- **total equality**
  - c/op_231 / go/op_117 -- **total equality**
  - c/op_231 / rust/op_663 -- **total equality**
  - c/op_231 / swift/op_171 -- **total equality**
  - cpp/op_231 / go/op_117 -- **total equality**
  - cpp/op_231 / rust/op_663 -- **total equality**
  - cpp/op_231 / swift/op_171 -- **total equality**
  - go/op_117 / rust/op_663 -- **total equality**
  - go/op_117 / swift/op_171 -- **total equality**
  - rust/op_663 / swift/op_171 -- **total equality**

### sem-identical group B0 V[Div64F0x2(ex128@0(in0:256),ex128@0(in1:256))] S[] E[ret] · (f64,f64)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `/` (f64,f64, 0 modes); cpp `/` (f64,f64, 0 modes); go `/` (f64,f64, 0 modes); rust `/` (f64,f64, 0 modes); swift `/` (f64,f64, 0 modes)

  - c/op_238 / cpp/op_238 -- **total equality**
  - c/op_238 / go/op_124 -- **total equality**
  - c/op_238 / rust/op_670 -- **total equality**
  - c/op_238 / swift/op_178 -- **total equality**
  - cpp/op_238 / go/op_124 -- **total equality**
  - cpp/op_238 / rust/op_670 -- **total equality**
  - cpp/op_238 / swift/op_178 -- **total equality**
  - go/op_124 / rust/op_670 -- **total equality**
  - go/op_124 / swift/op_178 -- **total equality**
  - rust/op_670 / swift/op_178 -- **total equality**

### sem-identical group B0 V[Mul32F0x4(ex128@0(in0:256),ex128@0(in1:256))] S[] E[ret] · (f32,f32)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `*` (f32,f32, 0 modes); cpp `*` (f32,f32, 0 modes); go `*` (f32,f32, 0 modes); rust `*` (f32,f32, 0 modes); swift `*` (f32,f32, 0 modes)

  - c/op_195 / cpp/op_195 -- **total equality**
  - c/op_195 / go/op_81 -- **total equality**
  - c/op_195 / rust/op_627 -- **total equality**
  - c/op_195 / swift/op_135 -- **total equality**
  - cpp/op_195 / go/op_81 -- **total equality**
  - cpp/op_195 / rust/op_627 -- **total equality**
  - cpp/op_195 / swift/op_135 -- **total equality**
  - go/op_81 / rust/op_627 -- **total equality**
  - go/op_81 / swift/op_135 -- **total equality**
  - rust/op_627 / swift/op_135 -- **total equality**

### sem-identical group B0 V[Mul64F0x2(ex128@0(in0:256),ex128@0(in1:256))] S[] E[ret] · (f64,f64)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `*` (f64,f64, 0 modes); cpp `*` (f64,f64, 0 modes); go `*` (f64,f64, 0 modes); rust `*` (f64,f64, 0 modes); swift `*` (f64,f64, 0 modes)

  - c/op_202 / cpp/op_202 -- **total equality**
  - c/op_202 / go/op_88 -- **total equality**
  - c/op_202 / rust/op_634 -- **total equality**
  - c/op_202 / swift/op_142 -- **total equality**
  - cpp/op_202 / go/op_88 -- **total equality**
  - cpp/op_202 / rust/op_634 -- **total equality**
  - cpp/op_202 / swift/op_142 -- **total equality**
  - go/op_88 / rust/op_634 -- **total equality**
  - go/op_88 / swift/op_142 -- **total equality**
  - rust/op_634 / swift/op_142 -- **total equality**

### sem-identical group B0 V[Sar64(in0:64,And8(63:8,ex8@0(in1:64))) zx64(ex32@0(in1:64))] S[] E[ret] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `>>` (i64,bool, 0 modes); cpp `>>` (i64,bool, 0 modes)

  - c/op_725 / cpp/op_725 -- **total equality**

### sem-identical group B0 V[Sar64(in0:64,And8(63:8,ex8@0(in1:64))) zx64(ex32@0(in1:64))] S[] E[ret] · (i64,i32)

- ground: cluster
- languages: c, cpp, rust
- members: c `>>` (i64,i32, 0 modes); cpp `>>` (i64,i32, 0 modes); rust `>>` (i64,i32, 0 modes)

  - c/op_720 / cpp/op_720 -- **total equality**
  - c/op_720 / rust/op_504 -- **total equality**
  - cpp/op_720 / rust/op_504 -- **total equality**

### sem-identical group B0 V[Shr64(in0:64,And8(63:8,ex8@0(in1:64))) zx64(ex32@0(in1:64))] S[] E[ret] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `>>` (u64,bool, 0 modes); cpp `>>` (u64,bool, 0 modes)

  - c/op_731 / cpp/op_731 -- **total equality**

### sem-identical group B0 V[Shr64(in0:64,And8(63:8,ex8@0(in1:64))) zx64(ex32@0(in1:64))] S[] E[ret] · (u64,i32)

- ground: cluster
- languages: c, cpp, rust
- members: c `>>` (u64,i32, 0 modes); cpp `>>` (u64,i32, 0 modes); rust `>>` (u64,i32, 0 modes)

  - c/op_726 / cpp/op_726 -- **total equality**
  - c/op_726 / rust/op_510 -- **total equality**
  - cpp/op_726 / rust/op_510 -- **total equality**

### sem-identical group B0 V[Sub32F0x4(ex128@0(in0:256),ex128@0(in1:256))] S[] E[ret] · (f32,f32)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `-` (f32,f32, 0 modes); cpp `-` (f32,f32, 0 modes); go `-` (f32,f32, 0 modes); rust `-` (f32,f32, 0 modes); swift `-` (f32,f32, 0 modes)

  - c/op_159 / cpp/op_159 -- **total equality**
  - c/op_159 / go/op_369 -- **total equality**
  - c/op_159 / rust/op_591 -- **total equality**
  - c/op_159 / swift/op_279 -- **total equality**
  - cpp/op_159 / go/op_369 -- **total equality**
  - cpp/op_159 / rust/op_591 -- **total equality**
  - cpp/op_159 / swift/op_279 -- **total equality**
  - go/op_369 / rust/op_591 -- **total equality**
  - go/op_369 / swift/op_279 -- **total equality**
  - rust/op_591 / swift/op_279 -- **total equality**

### sem-identical group B0 V[Sub64F0x2(ex128@0(in0:256),ex128@0(in1:256))] S[] E[ret] · (f64,f64)

- ground: cluster
- languages: c, cpp, go, rust, swift
- members: c `-` (f64,f64, 0 modes); cpp `-` (f64,f64, 0 modes); go `-` (f64,f64, 0 modes); rust `-` (f64,f64, 0 modes); swift `-` (f64,f64, 0 modes)

  - c/op_166 / cpp/op_166 -- **total equality**
  - c/op_166 / go/op_376 -- **total equality**
  - c/op_166 / rust/op_598 -- **total equality**
  - c/op_166 / swift/op_286 -- **total equality**
  - cpp/op_166 / go/op_376 -- **total equality**
  - cpp/op_166 / rust/op_598 -- **total equality**
  - cpp/op_166 / swift/op_286 -- **total equality**
  - go/op_376 / rust/op_598 -- **total equality**
  - go/op_376 / swift/op_286 -- **total equality**
  - rust/op_598 / swift/op_286 -- **total equality**

### sem-identical group B0 V[ins@0(zx64(ex32@0(in0:64)),Xor8(1:8,ex8@0(in0:64)))] S[] E[ret] · (bool,None)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `--` (bool,None, 0 modes); cpp `!` (bool,None, 1 modes); cpp `not` (bool,None, 1 modes); rust `!` (bool,None, 1 modes); swift `!` (bool,None, 1 modes)

  - c/op_47 / cpp/op_5 -- **core equality, modes differ**
    - only on the right: `in0 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_47 / cpp/op_29 -- **core equality, modes differ**
    - only on the right: `in0 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_47 / rust/op_17 -- **core equality, modes differ**
    - only on the right: `in0 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_47 / swift/op_29 -- **core equality, modes differ**
    - only on the right: `in0 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - cpp/op_5 / rust/op_17 -- **total equality**
  - cpp/op_29 / rust/op_17 -- **total equality**
  - cpp/op_5 / swift/op_29 -- **total equality**
  - cpp/op_29 / swift/op_29 -- **total equality**
  - rust/op_17 / swift/op_29 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(in0:256),ex128@0(in1:256))))))] S[] E[ret] · (f64,f64)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `!=` (f64,f64, 0 modes); cpp `!=` (f64,f64, 0 modes); cpp `not_eq` (f64,f64, 0 modes); rust `!=` (f64,f64, 0 modes); swift `!=` (f64,f64, 0 modes)

  - c/op_526 / cpp/op_526 -- **total equality**
  - c/op_526 / cpp/op_994 -- **total equality**
  - c/op_526 / rust/op_310 -- **total equality**
  - c/op_526 / swift/op_466 -- **total equality**
  - cpp/op_526 / rust/op_310 -- **total equality**
  - cpp/op_994 / rust/op_310 -- **total equality**
  - cpp/op_526 / swift/op_466 -- **total equality**
  - cpp/op_994 / swift/op_466 -- **total equality**
  - rust/op_310 / swift/op_466 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(in0:256),ex128@0(in1:256))))))] S[] E[ret] · (f32,f32)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `!=` (f32,f32, 0 modes); cpp `!=` (f32,f32, 0 modes); cpp `not_eq` (f32,f32, 0 modes); rust `!=` (f32,f32, 0 modes); swift `!=` (f32,f32, 0 modes)

  - c/op_519 / cpp/op_519 -- **total equality**
  - c/op_519 / cpp/op_987 -- **total equality**
  - c/op_519 / rust/op_303 -- **total equality**
  - c/op_519 / swift/op_459 -- **total equality**
  - cpp/op_519 / rust/op_303 -- **total equality**
  - cpp/op_987 / rust/op_303 -- **total equality**
  - cpp/op_519 / swift/op_459 -- **total equality**
  - cpp/op_987 / swift/op_459 -- **total equality**
  - rust/op_303 / swift/op_459 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) zx64(ex32@0(in1:64))] S[] E[ret] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `>>` (i32,bool, 0 modes); cpp `>>` (i32,bool, 0 modes)

  - c/op_719 / cpp/op_719 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) zx64(ex32@0(in1:64))] S[] E[ret] · (i32,i32)

- ground: cluster
- languages: c, cpp, rust
- members: c `>>` (i32,i32, 0 modes); cpp `>>` (i32,i32, 0 modes); rust `>>` (i32,i32, 0 modes)

  - c/op_714 / cpp/op_714 -- **total equality**
  - c/op_714 / rust/op_498 -- **total equality**
  - cpp/op_714 / rust/op_498 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(2:64,8:64,in0:64,in1:64,u0:64)))] S[] E[ret] · (u64,u64)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `<` (u64,u64, 0 modes); rust `<` (u64,u64, 0 modes); swift `<` (u64,u64, 0 modes)

  - cpp/op_656 / rust/op_332 -- **total equality**
  - cpp/op_656 / swift/op_308 -- **total equality**
  - rust/op_332 / swift/op_308 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(3:64,8:64,in0:64,in1:64,u0:64)))] S[] E[ret] · (u64,u64)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `>=` (u64,u64, 0 modes); rust `>=` (u64,u64, 0 modes); swift `>=` (u64,u64, 0 modes)

  - cpp/op_584 / rust/op_440 -- **total equality**
  - cpp/op_584 / swift/op_416 -- **total equality**
  - rust/op_440 / swift/op_416 -- **total equality**

### sem-identical group B0 V[Add32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))))] S[] E[ret] · (f32,bool)

- ground: cluster
- languages: c, cpp
- members: c `+` (f32,bool, 0 modes); cpp `+` (f32,bool, 0 modes)

  - c/op_125 / cpp/op_125 -- **total equality**

### sem-identical group B0 V[Add32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))))] S[] E[ret] · (f32,i32)

- ground: cluster
- languages: c, cpp
- members: c `+` (f32,i32, 0 modes); cpp `+` (f32,i32, 0 modes)

  - c/op_120 / cpp/op_120 -- **total equality**

### sem-identical group B0 V[Add32F0x4(ex128@0(in0:256),zx128(ld32/g0(8:64)))] S[] E[riprel addss | ret] · (f32,None)

- ground: cluster
- languages: c, cpp
- members: c `++` (f32,None, 0 modes); c `--` (f32,None, 0 modes); cpp `++` (f32,None, 0 modes); cpp `--` (f32,None, 0 modes)

  - c/op_39 / cpp/op_51 -- **total equality**
  - c/op_39 / cpp/op_57 -- **total equality**
  - c/op_45 / cpp/op_51 -- **total equality**
  - c/op_45 / cpp/op_57 -- **total equality**

### sem-identical group B0 V[Add32F0x4(ex128@0(in1:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))))] S[] E[ret] · (bool,f32)

- ground: cluster
- languages: c, cpp
- members: c `+` (bool,f32, 0 modes); cpp `+` (bool,f32, 0 modes)

  - c/op_135 / cpp/op_135 -- **total equality**

### sem-identical group B0 V[Add32F0x4(ex128@0(in1:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))))] S[] E[ret] · (i32,f32)

- ground: cluster
- languages: c, cpp
- members: c `+` (i32,f32, 0 modes); cpp `+` (i32,f32, 0 modes)

  - c/op_105 / cpp/op_105 -- **total equality**

### sem-identical group B0 V[Add64(18446744073709551608:64,SP:64)] S[st64(Add64(18446744073709551608:64,SP:64))=in0:64] E[ret] · (i64,None)

- ground: cluster
- languages: c, cpp
- members: c `&` (i64,None, 0 modes); cpp `&` (i64,None, 0 modes)

  - c/op_31 / cpp/op_43 -- **total equality**

### sem-identical group B0 V[Add64(18446744073709551608:64,SP:64)] S[st64(Add64(18446744073709551608:64,SP:64))=in0:64] E[ret] · (u64,None)

- ground: cluster
- languages: c, cpp
- members: c `&` (u64,None, 0 modes); cpp `&` (u64,None, 0 modes)

  - c/op_32 / cpp/op_44 -- **total equality**

### sem-identical group B0 V[Add64(18446744073709551615:64,in0:64)] S[] E[ret] · (i64,None)

- ground: cluster
- languages: c, cpp
- members: c `--` (i64,None, 0 modes); cpp `--` (i64,None, 0 modes)

  - c/op_43 / cpp/op_55 -- **total equality**

### sem-identical group B0 V[Add64(18446744073709551615:64,in0:64)] S[] E[ret] · (u64,None)

- ground: cluster
- languages: c, cpp
- members: c `--` (u64,None, 0 modes); cpp `--` (u64,None, 0 modes)

  - c/op_44 / cpp/op_56 -- **total equality**

### sem-identical group B0 V[Add64(1:64,in0:64)] S[] E[ret] · (i64,None)

- ground: cluster
- languages: c, cpp
- members: c `++` (i64,None, 0 modes); cpp `++` (i64,None, 0 modes)

  - c/op_37 / cpp/op_49 -- **total equality**

### sem-identical group B0 V[Add64(1:64,in0:64)] S[] E[ret] · (u64,None)

- ground: cluster
- languages: c, cpp
- members: c `++` (u64,None, 0 modes); cpp `++` (u64,None, 0 modes)

  - c/op_38 / cpp/op_50 -- **total equality**

### sem-identical group B0 V[Add64(in0:64,sx64(ex32@0(in1:64)))] S[] E[ret] · (i64,i32)

- ground: cluster
- languages: c, cpp
- members: c `+` (i64,i32, 0 modes); cpp `+` (i64,i32, 0 modes)

  - c/op_108 / cpp/op_108 -- **total equality**

### sem-identical group B0 V[Add64(in0:64,sx64(ex32@0(in1:64)))] S[] E[ret] · (u64,i32)

- ground: cluster
- languages: c, cpp
- members: c `+` (u64,i32, 0 modes); cpp `+` (u64,i32, 0 modes)

  - c/op_114 / cpp/op_114 -- **total equality**

### sem-identical group B0 V[Add64(in0:64,zx64(ex32@0(in1:64)))] S[] E[ret] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `+` (i64,bool, 0 modes); cpp `+` (i64,bool, 0 modes)

  - c/op_113 / cpp/op_113 -- **total equality**

### sem-identical group B0 V[Add64(in0:64,zx64(ex32@0(in1:64)))] S[] E[ret] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `+` (u64,bool, 0 modes); cpp `+` (u64,bool, 0 modes)

  - c/op_119 / cpp/op_119 -- **total equality**

### sem-identical group B0 V[Add64(in1:64,sx64(ex32@0(in0:64)))] S[] E[ret] · (i32,i64)

- ground: cluster
- languages: c, cpp
- members: c `+` (i32,i64, 0 modes); cpp `+` (i32,i64, 0 modes)

  - c/op_103 / cpp/op_103 -- **total equality**

### sem-identical group B0 V[Add64(in1:64,sx64(ex32@0(in0:64)))] S[] E[ret] · (i32,u64)

- ground: cluster
- languages: c, cpp
- members: c `+` (i32,u64, 0 modes); cpp `+` (i32,u64, 0 modes)

  - c/op_104 / cpp/op_104 -- **total equality**

### sem-identical group B0 V[Add64(in1:64,zx64(ex32@0(in0:64)))] S[] E[ret] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `+` (bool,i64, 0 modes); cpp `+` (bool,i64, 0 modes)

  - c/op_133 / cpp/op_133 -- **total equality**

### sem-identical group B0 V[Add64(in1:64,zx64(ex32@0(in0:64)))] S[] E[ret] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `+` (bool,u64, 0 modes); cpp `+` (bool,u64, 0 modes)

  - c/op_134 / cpp/op_134 -- **total equality**

### sem-identical group B0 V[Add64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))))] S[] E[ret] · (f64,bool)

- ground: cluster
- languages: c, cpp
- members: c `+` (f64,bool, 0 modes); cpp `+` (f64,bool, 0 modes)

  - c/op_131 / cpp/op_131 -- **total equality**

### sem-identical group B0 V[Add64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))))] S[] E[ret] · (f64,i32)

- ground: cluster
- languages: c, cpp
- members: c `+` (f64,i32, 0 modes); cpp `+` (f64,i32, 0 modes)

  - c/op_126 / cpp/op_126 -- **total equality**

### sem-identical group B0 V[Add64F0x2(ex128@0(in0:256),zx128(ld64/g0(8:64)))] S[] E[riprel addsd | ret] · (f64,None)

- ground: cluster
- languages: c, cpp
- members: c `++` (f64,None, 0 modes); c `--` (f64,None, 0 modes); cpp `++` (f64,None, 0 modes); cpp `--` (f64,None, 0 modes)

  - c/op_40 / cpp/op_52 -- **total equality**
  - c/op_40 / cpp/op_58 -- **total equality**
  - c/op_46 / cpp/op_52 -- **total equality**
  - c/op_46 / cpp/op_58 -- **total equality**

### sem-identical group B0 V[Add64F0x2(ex128@0(in1:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))))] S[] E[ret] · (bool,f64)

- ground: cluster
- languages: c, cpp
- members: c `+` (bool,f64, 0 modes); cpp `+` (bool,f64, 0 modes)

  - c/op_136 / cpp/op_136 -- **total equality**

### sem-identical group B0 V[Add64F0x2(ex128@0(in1:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))))] S[] E[ret] · (i32,f64)

- ground: cluster
- languages: c, cpp
- members: c `+` (i32,f64, 0 modes); cpp `+` (i32,f64, 0 modes)

  - c/op_106 / cpp/op_106 -- **total equality**

### sem-identical group B0 V[Div32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))))] S[] E[ret] · (f32,bool)

- ground: cluster
- languages: c, cpp
- members: c `/` (f32,bool, 0 modes); cpp `/` (f32,bool, 0 modes)

  - c/op_233 / cpp/op_233 -- **total equality**

### sem-identical group B0 V[Div32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))))] S[] E[ret] · (f32,i32)

- ground: cluster
- languages: c, cpp
- members: c `/` (f32,i32, 0 modes); cpp `/` (f32,i32, 0 modes)

  - c/op_228 / cpp/op_228 -- **total equality**

### sem-identical group B0 V[Div64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))))] S[] E[ret] · (f64,bool)

- ground: cluster
- languages: c, cpp
- members: c `/` (f64,bool, 0 modes); cpp `/` (f64,bool, 0 modes)

  - c/op_239 / cpp/op_239 -- **total equality**

### sem-identical group B0 V[Div64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))))] S[] E[ret] · (f64,i32)

- ground: cluster
- languages: c, cpp
- members: c `/` (f64,i32, 0 modes); cpp `/` (f64,i32, 0 modes)

  - c/op_234 / cpp/op_234 -- **total equality**

### sem-identical group B0 V[Mul32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))))] S[] E[ret] · (f32,bool)

- ground: cluster
- languages: c, cpp
- members: c `*` (f32,bool, 0 modes); cpp `*` (f32,bool, 0 modes)

  - c/op_197 / cpp/op_197 -- **total equality**

### sem-identical group B0 V[Mul32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))))] S[] E[ret] · (f32,i32)

- ground: cluster
- languages: c, cpp
- members: c `*` (f32,i32, 0 modes); cpp `*` (f32,i32, 0 modes)

  - c/op_192 / cpp/op_192 -- **total equality**

### sem-identical group B0 V[Mul32F0x4(ex128@0(in1:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))))] S[] E[ret] · (bool,f32)

- ground: cluster
- languages: c, cpp
- members: c `*` (bool,f32, 0 modes); cpp `*` (bool,f32, 0 modes)

  - c/op_207 / cpp/op_207 -- **total equality**

### sem-identical group B0 V[Mul32F0x4(ex128@0(in1:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))))] S[] E[ret] · (i32,f32)

- ground: cluster
- languages: c, cpp
- members: c `*` (i32,f32, 0 modes); cpp `*` (i32,f32, 0 modes)

  - c/op_177 / cpp/op_177 -- **total equality**

### sem-identical group B0 V[Mul64(in0:64,sx64(ex32@0(in1:64)))] S[] E[ret] · (i64,i32)

- ground: cluster
- languages: c, cpp
- members: c `*` (i64,i32, 0 modes); cpp `*` (i64,i32, 0 modes)

  - c/op_180 / cpp/op_180 -- **total equality**

### sem-identical group B0 V[Mul64(in0:64,sx64(ex32@0(in1:64)))] S[] E[ret] · (u64,i32)

- ground: cluster
- languages: c, cpp
- members: c `*` (u64,i32, 0 modes); cpp `*` (u64,i32, 0 modes)

  - c/op_186 / cpp/op_186 -- **total equality**

### sem-identical group B0 V[Mul64(in1:64,sx64(ex32@0(in0:64)))] S[] E[ret] · (i32,i64)

- ground: cluster
- languages: c, cpp
- members: c `*` (i32,i64, 0 modes); cpp `*` (i32,i64, 0 modes)

  - c/op_175 / cpp/op_175 -- **total equality**

### sem-identical group B0 V[Mul64(in1:64,sx64(ex32@0(in0:64)))] S[] E[ret] · (i32,u64)

- ground: cluster
- languages: c, cpp
- members: c `*` (i32,u64, 0 modes); cpp `*` (i32,u64, 0 modes)

  - c/op_176 / cpp/op_176 -- **total equality**

### sem-identical group B0 V[Mul64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))))] S[] E[ret] · (f64,bool)

- ground: cluster
- languages: c, cpp
- members: c `*` (f64,bool, 0 modes); cpp `*` (f64,bool, 0 modes)

  - c/op_203 / cpp/op_203 -- **total equality**

### sem-identical group B0 V[Mul64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))))] S[] E[ret] · (f64,i32)

- ground: cluster
- languages: c, cpp
- members: c `*` (f64,i32, 0 modes); cpp `*` (f64,i32, 0 modes)

  - c/op_198 / cpp/op_198 -- **total equality**

### sem-identical group B0 V[Mul64F0x2(ex128@0(in1:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))))] S[] E[ret] · (bool,f64)

- ground: cluster
- languages: c, cpp
- members: c `*` (bool,f64, 0 modes); cpp `*` (bool,f64, 0 modes)

  - c/op_208 / cpp/op_208 -- **total equality**

### sem-identical group B0 V[Mul64F0x2(ex128@0(in1:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))))] S[] E[ret] · (i32,f64)

- ground: cluster
- languages: c, cpp
- members: c `*` (i32,f64, 0 modes); cpp `*` (i32,f64, 0 modes)

  - c/op_178 / cpp/op_178 -- **total equality**

### sem-identical group B0 V[Sub32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))))] S[] E[ret] · (f32,bool)

- ground: cluster
- languages: c, cpp
- members: c `-` (f32,bool, 0 modes); cpp `-` (f32,bool, 0 modes)

  - c/op_161 / cpp/op_161 -- **total equality**

### sem-identical group B0 V[Sub32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))))] S[] E[ret] · (f32,i32)

- ground: cluster
- languages: c, cpp
- members: c `-` (f32,i32, 0 modes); cpp `-` (f32,i32, 0 modes)

  - c/op_156 / cpp/op_156 -- **total equality**

### sem-identical group B0 V[Sub64(in0:64,sx64(ex32@0(in1:64)))] S[] E[ret] · (i64,i32)

- ground: cluster
- languages: c, cpp
- members: c `-` (i64,i32, 0 modes); cpp `-` (i64,i32, 0 modes)

  - c/op_144 / cpp/op_144 -- **total equality**

### sem-identical group B0 V[Sub64(in0:64,sx64(ex32@0(in1:64)))] S[] E[ret] · (u64,i32)

- ground: cluster
- languages: c, cpp
- members: c `-` (u64,i32, 0 modes); cpp `-` (u64,i32, 0 modes)

  - c/op_150 / cpp/op_150 -- **total equality**

### sem-identical group B0 V[Sub64(in0:64,zx64(ex32@0(in1:64)))] S[] E[ret] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `-` (i64,bool, 0 modes); cpp `-` (i64,bool, 0 modes)

  - c/op_149 / cpp/op_149 -- **total equality**

### sem-identical group B0 V[Sub64(in0:64,zx64(ex32@0(in1:64)))] S[] E[ret] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `-` (u64,bool, 0 modes); cpp `-` (u64,bool, 0 modes)

  - c/op_155 / cpp/op_155 -- **total equality**

### sem-identical group B0 V[Sub64(sx64(ex32@0(in0:64)),in1:64)] S[] E[ret] · (i32,i64)

- ground: cluster
- languages: c, cpp
- members: c `-` (i32,i64, 0 modes); cpp `-` (i32,i64, 0 modes)

  - c/op_139 / cpp/op_139 -- **total equality**

### sem-identical group B0 V[Sub64(sx64(ex32@0(in0:64)),in1:64)] S[] E[ret] · (i32,u64)

- ground: cluster
- languages: c, cpp
- members: c `-` (i32,u64, 0 modes); cpp `-` (i32,u64, 0 modes)

  - c/op_140 / cpp/op_140 -- **total equality**

### sem-identical group B0 V[Sub64(zx64(ex32@0(in0:64)),in1:64)] S[] E[ret] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `-` (bool,i64, 0 modes); cpp `-` (bool,i64, 0 modes)

  - c/op_169 / cpp/op_169 -- **total equality**

### sem-identical group B0 V[Sub64(zx64(ex32@0(in0:64)),in1:64)] S[] E[ret] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `-` (bool,u64, 0 modes); cpp `-` (bool,u64, 0 modes)

  - c/op_170 / cpp/op_170 -- **total equality**

### sem-identical group B0 V[Sub64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))))] S[] E[ret] · (f64,bool)

- ground: cluster
- languages: c, cpp
- members: c `-` (f64,bool, 0 modes); cpp `-` (f64,bool, 0 modes)

  - c/op_167 / cpp/op_167 -- **total equality**

### sem-identical group B0 V[Sub64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))))] S[] E[ret] · (f64,i32)

- ground: cluster
- languages: c, cpp
- members: c `-` (f64,i32, 0 modes); cpp `-` (f64,i32, 0 modes)

  - c/op_162 / cpp/op_162 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))),Div32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256)))] S[] E[ret] · (bool,f32)

- ground: cluster
- languages: c, cpp
- members: c `/` (bool,f32, 0 modes); cpp `/` (bool,f32, 0 modes)

  - c/op_243 / cpp/op_243 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))),Div32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256)))] S[] E[ret] · (i32,f32)

- ground: cluster
- languages: c, cpp
- members: c `/` (i32,f32, 0 modes); cpp `/` (i32,f32, 0 modes)

  - c/op_213 / cpp/op_213 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))),Sub32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256)))] S[] E[ret] · (bool,f32)

- ground: cluster
- languages: c, cpp
- members: c `-` (bool,f32, 0 modes); cpp `-` (bool,f32, 0 modes)

  - c/op_171 / cpp/op_171 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))),Sub32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256)))] S[] E[ret] · (i32,f32)

- ground: cluster
- languages: c, cpp
- members: c `-` (i32,f32, 0 modes); cpp `-` (i32,f32, 0 modes)

  - c/op_141 / cpp/op_141 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))),Div64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256)))] S[] E[ret] · (bool,f64)

- ground: cluster
- languages: c, cpp
- members: c `/` (bool,f64, 0 modes); cpp `/` (bool,f64, 0 modes)

  - c/op_244 / cpp/op_244 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))),Div64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256)))] S[] E[ret] · (i32,f64)

- ground: cluster
- languages: c, cpp
- members: c `/` (i32,f64, 0 modes); cpp `/` (i32,f64, 0 modes)

  - c/op_214 / cpp/op_214 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))),Sub64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256)))] S[] E[ret] · (bool,f64)

- ground: cluster
- languages: c, cpp
- members: c `-` (bool,f64, 0 modes); cpp `-` (bool,f64, 0 modes)

  - c/op_172 / cpp/op_172 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))),Sub64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256)))] S[] E[ret] · (i32,f64)

- ground: cluster
- languages: c, cpp
- members: c `-` (i32,f64, 0 modes); cpp `-` (i32,f64, 0 modes)

  - c/op_142 / cpp/op_142 -- **total equality**

### sem-identical group B0 V[ite(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64)),in1:64,0:64)] S[] E[ret] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `*` (bool,i64, 0 modes); cpp `*` (bool,i64, 0 modes)

  - c/op_205 / cpp/op_205 -- **total equality**

### sem-identical group B0 V[ite(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64)),in1:64,0:64)] S[] E[ret] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `*` (bool,u64, 0 modes); cpp `*` (bool,u64, 0 modes)

  - c/op_206 / cpp/op_206 -- **total equality**

### sem-identical group B0 V[ite(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64)),in0:64,0:64)] S[] E[ret] · (i64,bool)

- ground: cluster
- languages: c, cpp
- members: c `*` (i64,bool, 0 modes); cpp `*` (i64,bool, 0 modes)

  - c/op_185 / cpp/op_185 -- **total equality**

### sem-identical group B0 V[ite(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64)),in0:64,0:64)] S[] E[ret] · (u64,bool)

- ground: cluster
- languages: c, cpp
- members: c `*` (u64,bool, 0 modes); cpp `*` (u64,bool, 0 modes)

  - c/op_191 / cpp/op_191 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(in0:256,CmpEQ32F0x4(ex128@0(in0:256),ex128@0(in1:256))))))] S[] E[ret] · (f32,f32)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `==` (f32,f32, 0 modes); cpp `==` (f32,f32, 0 modes); rust `==` (f32,f32, 0 modes); swift `==` (f32,f32, 0 modes)

  - c/op_483 / cpp/op_483 -- **total equality**
  - c/op_483 / rust/op_267 -- **total equality**
  - c/op_483 / swift/op_531 -- **total equality**
  - cpp/op_483 / rust/op_267 -- **total equality**
  - cpp/op_483 / swift/op_531 -- **total equality**
  - rust/op_267 / swift/op_531 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(in0:256,CmpEQ64F0x2(ex128@0(in0:256),ex128@0(in1:256))))))] S[] E[ret] · (f64,f64)

- ground: cluster
- languages: c, cpp, rust, swift
- members: c `==` (f64,f64, 0 modes); cpp `==` (f64,f64, 0 modes); rust `==` (f64,f64, 0 modes); swift `==` (f64,f64, 0 modes)

  - c/op_490 / cpp/op_490 -- **total equality**
  - c/op_490 / rust/op_274 -- **total equality**
  - c/op_490 / swift/op_538 -- **total equality**
  - cpp/op_490 / rust/op_274 -- **total equality**
  - cpp/op_490 / swift/op_538 -- **total equality**
  - rust/op_274 / swift/op_538 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))),CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256))))))] S[] E[ret] · (bool,f32)

- ground: cluster
- languages: c, cpp
- members: c `==` (bool,f32, 0 modes); cpp `==` (bool,f32, 0 modes)

  - c/op_495 / cpp/op_495 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))),CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256))))))] S[] E[ret] · (i32,f32)

- ground: cluster
- languages: c, cpp
- members: c `==` (i32,f32, 0 modes); cpp `==` (i32,f32, 0 modes)

  - c/op_465 / cpp/op_465 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64)))),CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))),ex128@0(in0:256))))))] S[] E[ret] · (f32,bool)

- ground: cluster
- languages: c, cpp
- members: c `==` (f32,bool, 0 modes); cpp `==` (f32,bool, 0 modes)

  - c/op_485 / cpp/op_485 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64)))),CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))),ex128@0(in0:256))))))] S[] E[ret] · (f32,i32)

- ground: cluster
- languages: c, cpp
- members: c `==` (f32,i32, 0 modes); cpp `==` (f32,i32, 0 modes)

  - c/op_480 / cpp/op_480 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))),CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256))))))] S[] E[ret] · (bool,f64)

- ground: cluster
- languages: c, cpp
- members: c `==` (bool,f64, 0 modes); cpp `==` (bool,f64, 0 modes)

  - c/op_496 / cpp/op_496 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))),CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256))))))] S[] E[ret] · (i32,f64)

- ground: cluster
- languages: c, cpp
- members: c `==` (i32,f64, 0 modes); cpp `==` (i32,f64, 0 modes)

  - c/op_466 / cpp/op_466 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))),CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))),ex128@0(in0:256))))))] S[] E[ret] · (f64,bool)

- ground: cluster
- languages: c, cpp
- members: c `==` (f64,bool, 0 modes); cpp `==` (f64,bool, 0 modes)

  - c/op_491 / cpp/op_491 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))),CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))),ex128@0(in0:256))))))] S[] E[ret] · (f64,i32)

- ground: cluster
- languages: c, cpp
- members: c `==` (f64,i32, 0 modes); cpp `==` (f64,i32, 0 modes)

  - c/op_486 / cpp/op_486 -- **total equality**

### sem-identical group B0 V[zx64(Mul32(ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (i32,i32)

- ground: cluster
- languages: c, cpp, go, rust
- members: c `*` (i32,i32, 1 modes); cpp `*` (i32,i32, 1 modes); go `*` (i32,i32, 1 modes); rust `*` (i32,i32, 1 modes)

  - c/op_174 / cpp/op_174 -- **total equality**
  - c/op_174 / go/op_60 -- **total equality**
  - c/op_174 / rust/op_606 -- **total equality**
  - cpp/op_174 / go/op_60 -- **total equality**
  - cpp/op_174 / rust/op_606 -- **total equality**
  - go/op_60 / rust/op_606 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(Shr64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) zx64(ex32@0(in1:64))] S[] E[ret] · (bool,bool)

- ground: cluster
- languages: c, cpp
- members: c `>>` (bool,bool, 0 modes); cpp `>>` (bool,bool, 0 modes)

  - c/op_749 / cpp/op_749 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(Shr64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) zx64(ex32@0(in1:64))] S[] E[ret] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `>>` (bool,i32, 0 modes); cpp `>>` (bool,i32, 0 modes)

  - c/op_744 / cpp/op_744 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(Shr64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))] S[] E[ret] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `>>` (bool,i64, 0 modes); cpp `>>` (bool,i64, 0 modes)

  - c/op_745 / cpp/op_745 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(Shr64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))] S[] E[ret] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `>>` (bool,u64, 0 modes); cpp `>>` (bool,u64, 0 modes)

  - c/op_746 / cpp/op_746 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(12:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64)))] S[] E[ret] · (i32,i32)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `<` (i32,i32, 0 modes); rust `<` (i32,i32, 0 modes); swift `<` (i32,i32, 0 modes)

  - cpp/op_642 / rust/op_318 -- **total equality**
  - cpp/op_642 / swift/op_294 -- **total equality**
  - rust/op_318 / swift/op_294 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(13:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64)))] S[] E[ret] · (i32,i32)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `>=` (i32,i32, 0 modes); rust `>=` (i32,i32, 0 modes); swift `>=` (i32,i32, 0 modes)

  - cpp/op_570 / rust/op_426 -- **total equality**
  - cpp/op_570 / swift/op_402 -- **total equality**
  - rust/op_426 / swift/op_402 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(ex32@0(in1:256))))),0:64,u0:64)))] S[] E[ret] · (f32,f32)

- ground: cluster
- languages: cpp, go, rust, swift
- members: cpp `>=` (f32,f32, 0 modes); go `>=` (f32,f32, 0 modes); rust `>=` (f32,f32, 0 modes); swift `>=` (f32,f32, 0 modes)

  - cpp/op_591 / go/op_657 -- **total equality**
  - cpp/op_591 / rust/op_447 -- **total equality**
  - cpp/op_591 / swift/op_423 -- **total equality**
  - go/op_657 / rust/op_447 -- **total equality**
  - go/op_657 / swift/op_423 -- **total equality**
  - rust/op_447 / swift/op_423 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256))))),0:64,u0:64)))] S[] E[ret] · (f32,f32)

- ground: cluster
- languages: cpp, go, rust, swift
- members: cpp `<=` (f32,f32, 0 modes); go `<=` (f32,f32, 0 modes); rust `<=` (f32,f32, 0 modes); swift `<=` (f32,f32, 0 modes)

  - cpp/op_627 / go/op_585 -- **total equality**
  - cpp/op_627 / rust/op_375 -- **total equality**
  - cpp/op_627 / swift/op_387 -- **total equality**
  - go/op_585 / rust/op_375 -- **total equality**
  - go/op_585 / swift/op_387 -- **total equality**
  - rust/op_375 / swift/op_387 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(in1:256)))),0:64,u0:64)))] S[] E[ret] · (f64,f64)

- ground: cluster
- languages: cpp, go, rust, swift
- members: cpp `>=` (f64,f64, 0 modes); go `>=` (f64,f64, 0 modes); rust `>=` (f64,f64, 0 modes); swift `>=` (f64,f64, 0 modes)

  - cpp/op_598 / go/op_664 -- **total equality**
  - cpp/op_598 / rust/op_454 -- **total equality**
  - cpp/op_598 / swift/op_430 -- **total equality**
  - go/op_664 / rust/op_454 -- **total equality**
  - go/op_664 / swift/op_430 -- **total equality**
  - rust/op_454 / swift/op_430 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(in0:256)))),0:64,u0:64)))] S[] E[ret] · (f64,f64)

- ground: cluster
- languages: cpp, go, rust, swift
- members: cpp `<=` (f64,f64, 0 modes); go `<=` (f64,f64, 0 modes); rust `<=` (f64,f64, 0 modes); swift `<=` (f64,f64, 0 modes)

  - cpp/op_634 / go/op_592 -- **total equality**
  - cpp/op_634 / rust/op_382 -- **total equality**
  - cpp/op_634 / swift/op_394 -- **total equality**
  - go/op_592 / rust/op_382 -- **total equality**
  - go/op_592 / swift/op_394 -- **total equality**
  - rust/op_382 / swift/op_394 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(4:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64)))] S[] E[ret] · (i32,i32)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `==` (i32,i32, 0 modes); rust `==` (i32,i32, 0 modes); swift `==` (i32,i32, 0 modes)

  - cpp/op_462 / rust/op_246 -- **total equality**
  - cpp/op_462 / swift/op_510 -- **total equality**
  - rust/op_246 / swift/op_510 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(6:64,8:64,in0:64,in1:64,u0:64)))] S[] E[ret] · (u64,u64)

- ground: cluster
- languages: cpp, rust
- members: cpp `<=` (u64,u64, 0 modes); rust `<=` (u64,u64, 0 modes)

  - cpp/op_620 / rust/op_368 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(ex32@0(in1:256))))),0:64,u0:64)))] S[] E[ret] · (f32,f32)

- ground: cluster
- languages: cpp, go, rust, swift
- members: cpp `>` (f32,f32, 0 modes); go `>` (f32,f32, 0 modes); rust `>` (f32,f32, 0 modes); swift `>` (f32,f32, 0 modes)

  - cpp/op_555 / go/op_621 -- **total equality**
  - cpp/op_555 / rust/op_411 -- **total equality**
  - cpp/op_555 / swift/op_351 -- **total equality**
  - go/op_621 / rust/op_411 -- **total equality**
  - go/op_621 / swift/op_351 -- **total equality**
  - rust/op_411 / swift/op_351 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256))))),0:64,u0:64)))] S[] E[ret] · (f32,f32)

- ground: cluster
- languages: cpp, go, rust, swift
- members: cpp `<` (f32,f32, 0 modes); go `<` (f32,f32, 0 modes); rust `<` (f32,f32, 0 modes); swift `<` (f32,f32, 0 modes)

  - cpp/op_663 / go/op_549 -- **total equality**
  - cpp/op_663 / rust/op_339 -- **total equality**
  - cpp/op_663 / swift/op_315 -- **total equality**
  - go/op_549 / rust/op_339 -- **total equality**
  - go/op_549 / swift/op_315 -- **total equality**
  - rust/op_339 / swift/op_315 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(in1:256)))),0:64,u0:64)))] S[] E[ret] · (f64,f64)

- ground: cluster
- languages: cpp, go, rust, swift
- members: cpp `>` (f64,f64, 0 modes); go `>` (f64,f64, 0 modes); rust `>` (f64,f64, 0 modes); swift `>` (f64,f64, 0 modes)

  - cpp/op_562 / go/op_628 -- **total equality**
  - cpp/op_562 / rust/op_418 -- **total equality**
  - cpp/op_562 / swift/op_358 -- **total equality**
  - go/op_628 / rust/op_418 -- **total equality**
  - go/op_628 / swift/op_358 -- **total equality**
  - rust/op_418 / swift/op_358 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(in0:256)))),0:64,u0:64)))] S[] E[ret] · (f64,f64)

- ground: cluster
- languages: cpp, go, rust, swift
- members: cpp `<` (f64,f64, 0 modes); go `<` (f64,f64, 0 modes); rust `<` (f64,f64, 0 modes); swift `<` (f64,f64, 0 modes)

  - cpp/op_670 / go/op_556 -- **total equality**
  - cpp/op_670 / rust/op_346 -- **total equality**
  - cpp/op_670 / swift/op_322 -- **total equality**
  - go/op_556 / rust/op_346 -- **total equality**
  - go/op_556 / swift/op_322 -- **total equality**
  - rust/op_346 / swift/op_322 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(7:64,8:64,in0:64,in1:64,u0:64)))] S[] E[ret] · (u64,u64)

- ground: cluster
- languages: cpp, rust
- members: cpp `>` (u64,u64, 0 modes); rust `>` (u64,u64, 0 modes)

  - cpp/op_548 / rust/op_404 -- **total equality**

### sem-identical group B0 V[] S[] E[branch js B2 [ex1@0(amd64g_calculate_condition(8:64,20:64,in0:64,0:64,u0:64))]]  B1 V[F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))] S[] E[jmp B3]  B2 V[ins@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64))))))),Add32F0x4(ex128@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64)))))))),ex128@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64))))))))))] S[] E[]  B3 V[zx64(And32(1:32,ex32@0(XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(in1:256),ex128@0(u2:256))))))] S[] E[ret] · (u64,f32)

- ground: cluster
- languages: c, cpp
- members: c `!=` (u64,f32, 0 modes); cpp `!=` (u64,f32, 0 modes); cpp `not_eq` (u64,f32, 0 modes)

  - c/op_513 / cpp/op_513 -- **total equality**
  - c/op_513 / cpp/op_981 -- **total equality**

### sem-identical group B0 V[] S[] E[branch js B2 [ex1@0(amd64g_calculate_condition(8:64,20:64,in1:64,0:64,u0:64))]]  B1 V[F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))] S[] E[jmp B3]  B2 V[ins@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64))))))),Add32F0x4(ex128@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64)))))))),ex128@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64))))))))))] S[] E[]  B3 V[zx64(And32(1:32,ex32@0(XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(in0:256),ex128@0(u2:256))))))] S[] E[ret] · (f32,u64)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f32,u64, 0 modes); cpp `!=` (f32,u64, 0 modes); cpp `not_eq` (f32,u64, 0 modes)

  - c/op_518 / cpp/op_518 -- **total equality**
  - c/op_518 / cpp/op_986 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(in0:256,F32toF64(ex32@0(in0:256))),XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))),ex128@0(in1:256)))) zx64(And32(1:32,ex32@0(XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))),ex128@0(in1:256))))))] S[] E[ret] · (f32,f64)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f32,f64, 0 modes); cpp `!=` (f32,f64, 0 modes); cpp `not_eq` (f32,f64, 0 modes)

  - c/op_520 / cpp/op_520 -- **total equality**
  - c/op_520 / cpp/op_988 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(in1:256,F32toF64(ex32@0(in1:256))),XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(in1:256,F32toF64(ex32@0(in1:256)))),ex128@0(in0:256)))) zx64(And32(1:32,ex32@0(XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(in1:256,F32toF64(ex32@0(in1:256)))),ex128@0(in0:256))))))] S[] E[ret] · (f64,f32)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f64,f32, 0 modes); cpp `!=` (f64,f32, 0 modes); cpp `not_eq` (f64,f32, 0 modes)

  - c/op_525 / cpp/op_525 -- **total equality**
  - c/op_525 / cpp/op_993 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)))),ex128@0(in1:256)))) zx64(And32(1:32,ex32@0(XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)))),ex128@0(in1:256))))))] S[] E[ret] · (i64,f32)

- ground: cluster
- languages: c, cpp
- members: c `!=` (i64,f32, 0 modes); cpp `!=` (i64,f32, 0 modes); cpp `not_eq` (i64,f32, 0 modes)

  - c/op_507 / cpp/op_507 -- **total equality**
  - c/op_507 / cpp/op_975 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))),XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)))),ex128@0(in0:256)))) zx64(And32(1:32,ex32@0(XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)))),ex128@0(in0:256))))))] S[] E[ret] · (f32,i64)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f32,i64, 0 modes); cpp `!=` (f32,i64, 0 modes); cpp `not_eq` (f32,i64, 0 modes)

  - c/op_517 / cpp/op_517 -- **total equality**
  - c/op_517 / cpp/op_985 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)),XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),ex128@0(in1:256)))) zx64(And32(1:32,ex32@0(XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),ex128@0(in1:256))))))] S[] E[ret] · (i64,f64)

- ground: cluster
- languages: c, cpp
- members: c `!=` (i64,f64, 0 modes); cpp `!=` (i64,f64, 0 modes); cpp `not_eq` (i64,f64, 0 modes)

  - c/op_508 / cpp/op_508 -- **total equality**
  - c/op_508 / cpp/op_976 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)),XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))),ex128@0(in0:256)))) zx64(And32(1:32,ex32@0(XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))),ex128@0(in0:256))))))] S[] E[ret] · (f64,i64)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f64,i64, 0 modes); cpp `!=` (f64,i64, 0 modes); cpp `not_eq` (f64,i64, 0 modes)

  - c/op_523 / cpp/op_523 -- **total equality**
  - c/op_523 / cpp/op_991 -- **total equality**

### sem-identical group B0 V[ins@0(zx64(Xor32(ex32@0(in0:64),ex32@0(in1:64))),Xor8(1:8,Xor8(ex8@0(in0:64),ex8@0(in1:64))))] S[] E[ret] · (bool,bool)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `==` (bool,bool, 0 modes); rust `==` (bool,bool, 0 modes); swift `==` (bool,bool, 0 modes)

  - cpp/op_497 / rust/op_281 -- **total equality**
  - cpp/op_497 / swift/op_545 -- **total equality**
  - rust/op_281 / swift/op_545 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(XorV128(18446744073709551615:128,CmpEQ64F0x2(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex128@0(in1:256))))))] S[] E[riprel punpckldq | riprel subpd | ret] · (u64,f64)

- ground: cluster
- languages: c, cpp
- members: c `!=` (u64,f64, 0 modes); cpp `!=` (u64,f64, 0 modes); cpp `not_eq` (u64,f64, 0 modes)

  - c/op_514 / cpp/op_514 -- **total equality**
  - c/op_514 / cpp/op_982 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(XorV128(18446744073709551615:128,CmpEQ64F0x2(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex128@0(in0:256))))))] S[] E[riprel punpckldq | riprel subpd | ret] · (f64,u64)

- ground: cluster
- languages: c, cpp
- members: c `!=` (f64,u64, 0 modes); cpp `!=` (f64,u64, 0 modes); cpp `not_eq` (f64,u64, 0 modes)

  - c/op_524 / cpp/op_524 -- **total equality**
  - c/op_524 / cpp/op_992 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,0:128),CmpEQ32F0x4(0:128,ex128@0(in0:256))))))] S[] E[ret] · (f32,None)

- ground: cluster
- languages: c, cpp
- members: c `!` (f32,None, 0 modes); cpp `!` (f32,None, 0 modes); cpp `not` (f32,None, 0 modes)

  - c/op_3 / cpp/op_3 -- **total equality**
  - c/op_3 / cpp/op_27 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,0:128),CmpEQ64F0x2(0:128,ex128@0(in0:256))))))] S[] E[ret] · (f64,None)

- ground: cluster
- languages: c, cpp
- members: c `!` (f64,None, 0 modes); cpp `!` (f64,None, 0 modes); cpp `not` (f64,None, 0 modes)

  - c/op_4 / cpp/op_4 -- **total equality**
  - c/op_4 / cpp/op_28 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(12:64,7:64,zx64(ex32@0(in1:64)),zx64(ex32@0(in0:64)),u0:64)))] S[] E[ret] · (i32,i32)

- ground: cluster
- languages: go, swift
- members: go `>` (i32,i32, 0 modes); swift `>` (i32,i32, 0 modes)

  - go/op_600 / swift/op_330 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(12:64,8:64,in0:64,in1:64,u0:64)))] S[] E[ret] · (i64,i64)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `<` (i64,i64, 0 modes); rust `<` (i64,i64, 0 modes); swift `<` (i64,i64, 0 modes)

  - cpp/op_649 / rust/op_325 -- **total equality**
  - cpp/op_649 / swift/op_301 -- **total equality**
  - rust/op_325 / swift/op_301 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(13:64,7:64,zx64(ex32@0(in1:64)),zx64(ex32@0(in0:64)),u0:64)))] S[] E[ret] · (i32,i32)

- ground: cluster
- languages: go, swift
- members: go `<=` (i32,i32, 0 modes); swift `<=` (i32,i32, 0 modes)

  - go/op_564 / swift/op_366 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(13:64,8:64,in0:64,in1:64,u0:64)))] S[] E[ret] · (i64,i64)

- ground: cluster
- languages: cpp, rust, swift
- members: cpp `>=` (i64,i64, 0 modes); rust `>=` (i64,i64, 0 modes); swift `>=` (i64,i64, 0 modes)

  - cpp/op_577 / rust/op_433 -- **total equality**
  - cpp/op_577 / swift/op_409 -- **total equality**
  - rust/op_433 / swift/op_409 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(14:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64)))] S[] E[ret] · (i32,i32)

- ground: cluster
- languages: cpp, rust
- members: cpp `<=` (i32,i32, 0 modes); rust `<=` (i32,i32, 0 modes)

  - cpp/op_606 / rust/op_354 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(15:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64)))] S[] E[ret] · (i32,i32)

- ground: cluster
- languages: cpp, rust
- members: cpp `>` (i32,i32, 0 modes); rust `>` (i32,i32, 0 modes)

  - cpp/op_534 / rust/op_390 -- **total equality**

### sem-identical group B0 V[Add32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)))))] S[] E[ret] · (f32,i64)

- ground: cluster
- languages: c, cpp
- members: c `+` (f32,i64, 0 modes); cpp `+` (f32,i64, 0 modes)

  - c/op_121 / cpp/op_121 -- **total equality**

### sem-identical group B0 V[Add32F0x4(ex128@0(in1:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)))))] S[] E[ret] · (i64,f32)

- ground: cluster
- languages: c, cpp
- members: c `+` (i64,f32, 0 modes); cpp `+` (i64,f32, 0 modes)

  - c/op_111 / cpp/op_111 -- **total equality**

### sem-identical group B0 V[Add64(18446744073709551608:64,SP:64)] S[st64(Add64(18446744073709551608:64,SP:64))=ex64@0(in0:256)] E[ret] · (f64,None)

- ground: cluster
- languages: c, cpp
- members: c `&` (f64,None, 0 modes); cpp `&` (f64,None, 0 modes)

  - c/op_34 / cpp/op_46 -- **total equality**

### sem-identical group B0 V[Add64(18446744073709551612:64,SP:64)] S[st32(Add64(18446744073709551612:64,SP:64))=ex32@0(in0:256)] E[ret] · (f32,None)

- ground: cluster
- languages: c, cpp
- members: c `&` (f32,None, 0 modes); cpp `&` (f32,None, 0 modes)

  - c/op_33 / cpp/op_45 -- **total equality**

### sem-identical group B0 V[Add64(18446744073709551612:64,SP:64)] S[st32(Add64(18446744073709551612:64,SP:64))=ex32@0(in0:64)] E[ret] · (i32,None)

- ground: cluster
- languages: c, cpp
- members: c `&` (i32,None, 0 modes); cpp `&` (i32,None, 0 modes)

  - c/op_30 / cpp/op_42 -- **total equality**

### sem-identical group B0 V[Add64(18446744073709551615:64,SP:64)] S[st8(Add64(18446744073709551615:64,SP:64))=ex8@0(in0:64)] E[ret] · (bool,None)

- ground: cluster
- languages: c, cpp
- members: c `&` (bool,None, 0 modes); cpp `&` (bool,None, 0 modes)

  - c/op_35 / cpp/op_47 -- **total equality**

### sem-identical group B0 V[Add64F0x2(ex128@0(in0:256),Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))))] S[] E[riprel punpckldq | riprel subpd | ret] · (f64,u64)

- ground: cluster
- languages: c, cpp
- members: c `+` (f64,u64, 0 modes); cpp `+` (f64,u64, 0 modes)

  - c/op_128 / cpp/op_128 -- **total equality**

### sem-identical group B0 V[Add64F0x2(ex128@0(in0:256),ex128@0(ins@0(in1:256,F32toF64(ex32@0(in1:256)))))] S[] E[ret] · (f64,f32)

- ground: cluster
- languages: c, cpp
- members: c `+` (f64,f32, 0 modes); cpp `+` (f64,f32, 0 modes)

  - c/op_129 / cpp/op_129 -- **total equality**

### sem-identical group B0 V[Add64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))))] S[] E[ret] · (f64,i64)

- ground: cluster
- languages: c, cpp
- members: c `+` (f64,i64, 0 modes); cpp `+` (f64,i64, 0 modes)

  - c/op_127 / cpp/op_127 -- **total equality**

### sem-identical group B0 V[Add64F0x2(ex128@0(in1:256),Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))))] S[] E[riprel punpckldq | riprel subpd | ret] · (u64,f64)

- ground: cluster
- languages: c, cpp
- members: c `+` (u64,f64, 0 modes); cpp `+` (u64,f64, 0 modes)

  - c/op_118 / cpp/op_118 -- **total equality**

### sem-identical group B0 V[Add64F0x2(ex128@0(in1:256),ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))))] S[] E[ret] · (i64,f64)

- ground: cluster
- languages: c, cpp
- members: c `+` (i64,f64, 0 modes); cpp `+` (i64,f64, 0 modes)

  - c/op_112 / cpp/op_112 -- **total equality**

### sem-identical group B0 V[Div32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)))))] S[] E[ret] · (f32,i64)

- ground: cluster
- languages: c, cpp
- members: c `/` (f32,i64, 0 modes); cpp `/` (f32,i64, 0 modes)

  - c/op_229 / cpp/op_229 -- **total equality**

### sem-identical group B0 V[Div64F0x2(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex128@0(in1:256)) Div64F0x2(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex128@0(in1:256))] S[] E[riprel punpckldq | riprel subpd | ret] · (u64,f64)

- ground: cluster
- languages: c, cpp
- members: c `/` (u64,f64, 0 modes); cpp `/` (u64,f64, 0 modes)

  - c/op_226 / cpp/op_226 -- **total equality**

### sem-identical group B0 V[Div64F0x2(ex128@0(in0:256),Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))))] S[] E[riprel punpckldq | riprel subpd | ret] · (f64,u64)

- ground: cluster
- languages: c, cpp
- members: c `/` (f64,u64, 0 modes); cpp `/` (f64,u64, 0 modes)

  - c/op_236 / cpp/op_236 -- **total equality**

### sem-identical group B0 V[Div64F0x2(ex128@0(in0:256),ex128@0(ins@0(in1:256,F32toF64(ex32@0(in1:256)))))] S[] E[ret] · (f64,f32)

- ground: cluster
- languages: c, cpp
- members: c `/` (f64,f32, 0 modes); cpp `/` (f64,f32, 0 modes)

  - c/op_237 / cpp/op_237 -- **total equality**

### sem-identical group B0 V[Div64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))))] S[] E[ret] · (f64,i64)

- ground: cluster
- languages: c, cpp
- members: c `/` (f64,i64, 0 modes); cpp `/` (f64,i64, 0 modes)

  - c/op_235 / cpp/op_235 -- **total equality**

### sem-identical group B0 V[Mul32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)))))] S[] E[ret] · (f32,i64)

- ground: cluster
- languages: c, cpp
- members: c `*` (f32,i64, 0 modes); cpp `*` (f32,i64, 0 modes)

  - c/op_193 / cpp/op_193 -- **total equality**

### sem-identical group B0 V[Mul32F0x4(ex128@0(in1:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)))))] S[] E[ret] · (i64,f32)

- ground: cluster
- languages: c, cpp
- members: c `*` (i64,f32, 0 modes); cpp `*` (i64,f32, 0 modes)

  - c/op_183 / cpp/op_183 -- **total equality**

### sem-identical group B0 V[Mul64F0x2(ex128@0(in0:256),Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))))] S[] E[riprel punpckldq | riprel subpd | ret] · (f64,u64)

- ground: cluster
- languages: c, cpp
- members: c `*` (f64,u64, 0 modes); cpp `*` (f64,u64, 0 modes)

  - c/op_200 / cpp/op_200 -- **total equality**

### sem-identical group B0 V[Mul64F0x2(ex128@0(in0:256),ex128@0(ins@0(in1:256,F32toF64(ex32@0(in1:256)))))] S[] E[ret] · (f64,f32)

- ground: cluster
- languages: c, cpp
- members: c `*` (f64,f32, 0 modes); cpp `*` (f64,f32, 0 modes)

  - c/op_201 / cpp/op_201 -- **total equality**

### sem-identical group B0 V[Mul64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))))] S[] E[ret] · (f64,i64)

- ground: cluster
- languages: c, cpp
- members: c `*` (f64,i64, 0 modes); cpp `*` (f64,i64, 0 modes)

  - c/op_199 / cpp/op_199 -- **total equality**

### sem-identical group B0 V[Mul64F0x2(ex128@0(in1:256),Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))))] S[] E[riprel punpckldq | riprel subpd | ret] · (u64,f64)

- ground: cluster
- languages: c, cpp
- members: c `*` (u64,f64, 0 modes); cpp `*` (u64,f64, 0 modes)

  - c/op_190 / cpp/op_190 -- **total equality**

### sem-identical group B0 V[Mul64F0x2(ex128@0(in1:256),ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))))] S[] E[ret] · (i64,f64)

- ground: cluster
- languages: c, cpp
- members: c `*` (i64,f64, 0 modes); cpp `*` (i64,f64, 0 modes)

  - c/op_184 / cpp/op_184 -- **total equality**

### sem-identical group B0 V[Sub32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)))))] S[] E[ret] · (f32,i64)

- ground: cluster
- languages: c, cpp
- members: c `-` (f32,i64, 0 modes); cpp `-` (f32,i64, 0 modes)

  - c/op_157 / cpp/op_157 -- **total equality**

### sem-identical group B0 V[Sub64F0x2(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex128@0(in1:256)) Sub64F0x2(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex128@0(in1:256))] S[] E[riprel punpckldq | riprel subpd | ret] · (u64,f64)

- ground: cluster
- languages: c, cpp
- members: c `-` (u64,f64, 0 modes); cpp `-` (u64,f64, 0 modes)

  - c/op_154 / cpp/op_154 -- **total equality**

### sem-identical group B0 V[Sub64F0x2(ex128@0(in0:256),Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))))] S[] E[riprel punpckldq | riprel subpd | ret] · (f64,u64)

- ground: cluster
- languages: c, cpp
- members: c `-` (f64,u64, 0 modes); cpp `-` (f64,u64, 0 modes)

  - c/op_164 / cpp/op_164 -- **total equality**

### sem-identical group B0 V[Sub64F0x2(ex128@0(in0:256),ex128@0(ins@0(in1:256,F32toF64(ex32@0(in1:256)))))] S[] E[ret] · (f64,f32)

- ground: cluster
- languages: c, cpp
- members: c `-` (f64,f32, 0 modes); cpp `-` (f64,f32, 0 modes)

  - c/op_165 / cpp/op_165 -- **total equality**

### sem-identical group B0 V[Sub64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))))] S[] E[ret] · (f64,i64)

- ground: cluster
- languages: c, cpp
- members: c `-` (f64,i64, 0 modes); cpp `-` (f64,i64, 0 modes)

  - c/op_163 / cpp/op_163 -- **total equality**

### sem-identical group B0 V[] S[] E[branch js B2 [ex1@0(amd64g_calculate_condition(8:64,20:64,in0:64,0:64,u0:64))]]  B1 V[Add32F0x4(ex128@0(in1:256),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),in0:64)))))] S[] E[ret]  B2 V[Add32F0x4(ex128@0(in1:256),Add32F0x4(ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64)))))))),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64)))))))))) ins@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64))))))),Add32F0x4(ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64)))))))),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64))))))))))] S[] E[ret] · (u64,f32)

- ground: cluster
- languages: c, cpp
- members: c `+` (u64,f32, 0 modes); cpp `+` (u64,f32, 0 modes)

  - c/op_117 / cpp/op_117 -- **total equality**

### sem-identical group B0 V[] S[] E[branch js B2 [ex1@0(amd64g_calculate_condition(8:64,20:64,in0:64,0:64,u0:64))]]  B1 V[F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))] S[] E[jmp B3]  B2 V[ins@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64))))))),Add32F0x4(ex128@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64)))))))),ex128@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64))))))))))] S[] E[]  B3 V[Div32F0x4(ex128@0(u2:256),ex128@0(in1:256)) Div32F0x4(ex128@0(u2:256),ex128@0(in1:256))] S[] E[ret] · (u64,f32)

- ground: cluster
- languages: c, cpp
- members: c `/` (u64,f32, 0 modes); cpp `/` (u64,f32, 0 modes)

  - c/op_225 / cpp/op_225 -- **total equality**

### sem-identical group B0 V[] S[] E[branch js B2 [ex1@0(amd64g_calculate_condition(8:64,20:64,in0:64,0:64,u0:64))]]  B1 V[F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))] S[] E[jmp B3]  B2 V[ins@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64))))))),Add32F0x4(ex128@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64)))))))),ex128@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64))))))))))] S[] E[]  B3 V[Sub32F0x4(ex128@0(u2:256),ex128@0(in1:256)) Sub32F0x4(ex128@0(u2:256),ex128@0(in1:256))] S[] E[ret] · (u64,f32)

- ground: cluster
- languages: c, cpp
- members: c `-` (u64,f32, 0 modes); cpp `-` (u64,f32, 0 modes)

  - c/op_153 / cpp/op_153 -- **total equality**

### sem-identical group B0 V[] S[] E[branch js B2 [ex1@0(amd64g_calculate_condition(8:64,20:64,in0:64,0:64,u0:64))]]  B1 V[F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))] S[] E[jmp B3]  B2 V[ins@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64))))))),Add32F0x4(ex128@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64)))))))),ex128@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64))))))))))] S[] E[]  B3 V[zx64(And32(1:32,ex32@0(ins@0(in1:256,CmpEQ32F0x4(ex128@0(in1:256),ex128@0(u2:256))))))] S[] E[ret] · (u64,f32)

- ground: cluster
- languages: c, cpp
- members: c `==` (u64,f32, 0 modes); cpp `==` (u64,f32, 0 modes)

  - c/op_477 / cpp/op_477 -- **total equality**

### sem-identical group B0 V[] S[] E[branch js B2 [ex1@0(amd64g_calculate_condition(8:64,20:64,in0:64,0:64,u0:64))]]  B1 V[Mul32F0x4(ex128@0(in1:256),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),in0:64)))))] S[] E[ret]  B2 V[Mul32F0x4(ex128@0(in1:256),Add32F0x4(ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64)))))))),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64)))))))))) ins@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64))))))),Add32F0x4(ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64)))))))),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64))))))))))] S[] E[ret] · (u64,f32)

- ground: cluster
- languages: c, cpp
- members: c `*` (u64,f32, 0 modes); cpp `*` (u64,f32, 0 modes)

  - c/op_189 / cpp/op_189 -- **total equality**

### sem-identical group B0 V[] S[] E[branch js B2 [ex1@0(amd64g_calculate_condition(8:64,20:64,in1:64,0:64,u0:64))]]  B1 V[Add32F0x4(ex128@0(in0:256),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),in1:64)))))] S[] E[ret]  B2 V[Add32F0x4(ex128@0(in0:256),Add32F0x4(ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64)))))))),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64)))))))))) ins@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64))))))),Add32F0x4(ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64)))))))),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64))))))))))] S[] E[ret] · (f32,u64)

- ground: cluster
- languages: c, cpp
- members: c `+` (f32,u64, 0 modes); cpp `+` (f32,u64, 0 modes)

  - c/op_122 / cpp/op_122 -- **total equality**

### sem-identical group B0 V[] S[] E[branch js B2 [ex1@0(amd64g_calculate_condition(8:64,20:64,in1:64,0:64,u0:64))]]  B1 V[Div32F0x4(ex128@0(in0:256),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),in1:64)))))] S[] E[ret]  B2 V[Div32F0x4(ex128@0(in0:256),Add32F0x4(ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64)))))))),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64)))))))))) ins@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64))))))),Add32F0x4(ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64)))))))),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64))))))))))] S[] E[ret] · (f32,u64)

- ground: cluster
- languages: c, cpp
- members: c `/` (f32,u64, 0 modes); cpp `/` (f32,u64, 0 modes)

  - c/op_230 / cpp/op_230 -- **total equality**

### sem-identical group B0 V[] S[] E[branch js B2 [ex1@0(amd64g_calculate_condition(8:64,20:64,in1:64,0:64,u0:64))]]  B1 V[F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))] S[] E[jmp B3]  B2 V[ins@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64))))))),Add32F0x4(ex128@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64)))))))),ex128@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64))))))))))] S[] E[]  B3 V[zx64(And32(1:32,ex32@0(ins@0(in0:256,CmpEQ32F0x4(ex128@0(in0:256),ex128@0(u2:256))))))] S[] E[ret] · (f32,u64)

- ground: cluster
- languages: c, cpp
- members: c `==` (f32,u64, 0 modes); cpp `==` (f32,u64, 0 modes)

  - c/op_482 / cpp/op_482 -- **total equality**

### sem-identical group B0 V[] S[] E[branch js B2 [ex1@0(amd64g_calculate_condition(8:64,20:64,in1:64,0:64,u0:64))]]  B1 V[Mul32F0x4(ex128@0(in0:256),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),in1:64)))))] S[] E[ret]  B2 V[Mul32F0x4(ex128@0(in0:256),Add32F0x4(ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64)))))))),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64)))))))))) ins@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64))))))),Add32F0x4(ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64)))))))),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64))))))))))] S[] E[ret] · (f32,u64)

- ground: cluster
- languages: c, cpp
- members: c `*` (f32,u64, 0 modes); cpp `*` (f32,u64, 0 modes)

  - c/op_194 / cpp/op_194 -- **total equality**

### sem-identical group B0 V[] S[] E[branch js B2 [ex1@0(amd64g_calculate_condition(8:64,20:64,in1:64,0:64,u0:64))]]  B1 V[Sub32F0x4(ex128@0(in0:256),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),in1:64)))))] S[] E[ret]  B2 V[Sub32F0x4(ex128@0(in0:256),Add32F0x4(ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64)))))))),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64)))))))))) ins@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64))))))),Add32F0x4(ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64)))))))),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64))))))))))] S[] E[ret] · (f32,u64)

- ground: cluster
- languages: c, cpp
- members: c `-` (f32,u64, 0 modes); cpp `-` (f32,u64, 0 modes)

  - c/op_158 / cpp/op_158 -- **total equality**

### sem-identical group B0 V[ex64@0(DivModS128to64(64HLto128(0:64,zx64(ex32@0(in0:64))),in1:64)) ex64@64(DivModS128to64(64HLto128(0:64,zx64(ex32@0(in0:64))),in1:64))] S[] E[ret] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `/` (bool,i64, 0 modes); cpp `/` (bool,i64, 0 modes)

  - c/op_241 / cpp/op_241 -- **total equality**

### sem-identical group B0 V[ex64@0(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64)) ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))] S[] E[ret] · (i64,i64)

- ground: cluster
- languages: c, cpp
- members: c `/` (i64,i64, 0 modes); cpp `/` (i64,i64, 0 modes)

  - c/op_217 / cpp/op_217 -- **total equality**

### sem-identical group B0 V[ex64@0(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),sx64(ex32@0(in1:64)))) ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),sx64(ex32@0(in1:64))))] S[] E[ret] · (i64,i32)

- ground: cluster
- languages: c, cpp
- members: c `/` (i64,i32, 0 modes); cpp `/` (i64,i32, 0 modes)

  - c/op_216 / cpp/op_216 -- **total equality**

### sem-identical group B0 V[ex64@0(DivModS128to64(64HLto128(Sar64(sx64(ex32@0(in0:64)),63:8),sx64(ex32@0(in0:64))),in1:64)) ex64@64(DivModS128to64(64HLto128(Sar64(sx64(ex32@0(in0:64)),63:8),sx64(ex32@0(in0:64))),in1:64))] S[] E[ret] · (i32,i64)

- ground: cluster
- languages: c, cpp
- members: c `/` (i32,i64, 0 modes); cpp `/` (i32,i64, 0 modes)

  - c/op_211 / cpp/op_211 -- **total equality**

### sem-identical group B0 V[ex64@0(DivModU128to64(64HLto128(0:64,in0:64),sx64(ex32@0(in1:64)))) ex64@64(DivModU128to64(64HLto128(0:64,in0:64),sx64(ex32@0(in1:64))))] S[] E[ret] · (u64,i32)

- ground: cluster
- languages: c, cpp
- members: c `/` (u64,i32, 0 modes); cpp `/` (u64,i32, 0 modes)

  - c/op_222 / cpp/op_222 -- **total equality**

### sem-identical group B0 V[ex64@0(DivModU128to64(64HLto128(0:64,sx64(ex32@0(in0:64))),in1:64)) ex64@64(DivModU128to64(64HLto128(0:64,sx64(ex32@0(in0:64))),in1:64))] S[] E[ret] · (i32,u64)

- ground: cluster
- languages: c, cpp
- members: c `/` (i32,u64, 0 modes); cpp `/` (i32,u64, 0 modes)

  - c/op_212 / cpp/op_212 -- **total equality**

### sem-identical group B0 V[ex64@0(DivModU128to64(64HLto128(0:64,zx64(ex32@0(in0:64))),in1:64)) ex64@64(DivModU128to64(64HLto128(0:64,zx64(ex32@0(in0:64))),in1:64))] S[] E[ret] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `/` (bool,u64, 0 modes); cpp `/` (bool,u64, 0 modes)

  - c/op_242 / cpp/op_242 -- **total equality**

### sem-identical group B0 V[ex64@64(DivModS128to64(64HLto128(0:64,zx64(ex32@0(in0:64))),in1:64)) ex64@64(DivModS128to64(64HLto128(0:64,zx64(ex32@0(in0:64))),in1:64))] S[] E[ret] · (bool,i64)

- ground: cluster
- languages: c, cpp
- members: c `%` (bool,i64, 0 modes); cpp `%` (bool,i64, 0 modes)

  - c/op_277 / cpp/op_277 -- **total equality**

### sem-identical group B0 V[ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64)) ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))] S[] E[ret] · (i64,i64)

- ground: cluster
- languages: c, cpp
- members: c `%` (i64,i64, 0 modes); cpp `%` (i64,i64, 0 modes)

  - c/op_253 / cpp/op_253 -- **total equality**

### sem-identical group B0 V[ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),sx64(ex32@0(in1:64)))) ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),sx64(ex32@0(in1:64))))] S[] E[ret] · (i64,i32)

- ground: cluster
- languages: c, cpp
- members: c `%` (i64,i32, 0 modes); cpp `%` (i64,i32, 0 modes)

  - c/op_252 / cpp/op_252 -- **total equality**

### sem-identical group B0 V[ex64@64(DivModS128to64(64HLto128(Sar64(sx64(ex32@0(in0:64)),63:8),sx64(ex32@0(in0:64))),in1:64)) ex64@64(DivModS128to64(64HLto128(Sar64(sx64(ex32@0(in0:64)),63:8),sx64(ex32@0(in0:64))),in1:64))] S[] E[ret] · (i32,i64)

- ground: cluster
- languages: c, cpp
- members: c `%` (i32,i64, 0 modes); cpp `%` (i32,i64, 0 modes)

  - c/op_247 / cpp/op_247 -- **total equality**

### sem-identical group B0 V[ex64@64(DivModU128to64(64HLto128(0:64,in0:64),sx64(ex32@0(in1:64)))) ex64@64(DivModU128to64(64HLto128(0:64,in0:64),sx64(ex32@0(in1:64))))] S[] E[ret] · (u64,i32)

- ground: cluster
- languages: c, cpp
- members: c `%` (u64,i32, 0 modes); cpp `%` (u64,i32, 0 modes)

  - c/op_258 / cpp/op_258 -- **total equality**

### sem-identical group B0 V[ex64@64(DivModU128to64(64HLto128(0:64,sx64(ex32@0(in0:64))),in1:64)) ex64@64(DivModU128to64(64HLto128(0:64,sx64(ex32@0(in0:64))),in1:64))] S[] E[ret] · (i32,u64)

- ground: cluster
- languages: c, cpp
- members: c `%` (i32,u64, 0 modes); cpp `%` (i32,u64, 0 modes)

  - c/op_248 / cpp/op_248 -- **total equality**

### sem-identical group B0 V[ex64@64(DivModU128to64(64HLto128(0:64,zx64(ex32@0(in0:64))),in1:64)) ex64@64(DivModU128to64(64HLto128(0:64,zx64(ex32@0(in0:64))),in1:64))] S[] E[ret] · (bool,u64)

- ground: cluster
- languages: c, cpp
- members: c `%` (bool,u64, 0 modes); cpp `%` (bool,u64, 0 modes)

  - c/op_278 / cpp/op_278 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(in0:256,F32toF64(ex32@0(in0:256))),Add64F0x2(ex128@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))),ex128@0(in1:256)))] S[] E[ret] · (f32,f64)

- ground: cluster
- languages: c, cpp
- members: c `+` (f32,f64, 0 modes); cpp `+` (f32,f64, 0 modes)

  - c/op_124 / cpp/op_124 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(in0:256,F32toF64(ex32@0(in0:256))),Div64F0x2(ex128@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))),ex128@0(in1:256)))] S[] E[ret] · (f32,f64)

- ground: cluster
- languages: c, cpp
- members: c `/` (f32,f64, 0 modes); cpp `/` (f32,f64, 0 modes)

  - c/op_232 / cpp/op_232 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(in0:256,F32toF64(ex32@0(in0:256))),Mul64F0x2(ex128@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))),ex128@0(in1:256)))] S[] E[ret] · (f32,f64)

- ground: cluster
- languages: c, cpp
- members: c `*` (f32,f64, 0 modes); cpp `*` (f32,f64, 0 modes)

  - c/op_196 / cpp/op_196 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(in0:256,F32toF64(ex32@0(in0:256))),Sub64F0x2(ex128@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))),ex128@0(in1:256)))] S[] E[ret] · (f32,f64)

- ground: cluster
- languages: c, cpp
- members: c `-` (f32,f64, 0 modes); cpp `-` (f32,f64, 0 modes)

  - c/op_160 / cpp/op_160 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),Div32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)))),ex128@0(in1:256)))] S[] E[ret] · (i64,f32)

- ground: cluster
- languages: c, cpp
- members: c `/` (i64,f32, 0 modes); cpp `/` (i64,f32, 0 modes)

  - c/op_219 / cpp/op_219 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),Sub32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)))),ex128@0(in1:256)))] S[] E[ret] · (i64,f32)

- ground: cluster
- languages: c, cpp
- members: c `-` (i64,f32, 0 modes); cpp `-` (i64,f32, 0 modes)

  - c/op_147 / cpp/op_147 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)),Div64F0x2(ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),ex128@0(in1:256)))] S[] E[ret] · (i64,f64)

- ground: cluster
- languages: c, cpp
- members: c `/` (i64,f64, 0 modes); cpp `/` (i64,f64, 0 modes)

  - c/op_220 / cpp/op_220 -- **total equality**

### sem-identical group B0 V[ins@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)),Sub64F0x2(ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),ex128@0(in1:256)))] S[] E[ret] · (i64,f64)

- ground: cluster
- languages: c, cpp
- members: c `-` (i64,f64, 0 modes); cpp `-` (i64,f64, 0 modes)

  - c/op_148 / cpp/op_148 -- **total equality**

### sem-identical group B0 V[ins@0(zx64(ex32@0(in0:64)),And8(Xor8(1:8,ex8@0(in0:64)),ex8@0(in1:64)))] S[] E[ret] · (bool,bool)

- ground: cluster
- languages: cpp, rust
- members: cpp `<` (bool,bool, 1 modes); rust `<` (bool,bool, 1 modes)

  - cpp/op_677 / rust/op_353 -- **total equality**

### sem-identical group B0 V[ins@0(zx64(ex32@0(in0:64)),Or8(Xor8(1:8,ex8@0(in0:64)),ex8@0(in1:64)))] S[] E[ret] · (bool,bool)

- ground: cluster
- languages: cpp, rust
- members: cpp `<=` (bool,bool, 1 modes); rust `<=` (bool,bool, 1 modes)

  - cpp/op_641 / rust/op_389 -- **total equality**

### sem-identical group B0 V[ins@0(zx64(ex32@0(in1:64)),And8(Xor8(1:8,ex8@0(in1:64)),ex8@0(in0:64)))] S[] E[ret] · (bool,bool)

- ground: cluster
- languages: cpp, rust
- members: cpp `>` (bool,bool, 1 modes); rust `>` (bool,bool, 1 modes)

  - cpp/op_569 / rust/op_425 -- **total equality**

### sem-identical group B0 V[ins@0(zx64(ex32@0(in1:64)),Or8(Xor8(1:8,ex8@0(in1:64)),ex8@0(in0:64)))] S[] E[ret] · (bool,bool)

- ground: cluster
- languages: cpp, rust
- members: cpp `>=` (bool,bool, 1 modes); rust `>=` (bool,bool, 1 modes)

  - cpp/op_605 / rust/op_461 -- **total equality**

### sem-identical group B0 V[zx64(Add32(1:32,ex32@0(in0:64)))] S[] E[ret] · (i32,None)

- ground: cluster
- languages: c, cpp
- members: c `++` (i32,None, 0 modes); cpp `++` (i32,None, 0 modes)

  - c/op_36 / cpp/op_48 -- **total equality**

### sem-identical group B0 V[zx64(Add32(4294967295:32,ex32@0(in0:64)))] S[] E[ret] · (i32,None)

- ground: cluster
- languages: c, cpp
- members: c `--` (i32,None, 0 modes); cpp `--` (i32,None, 0 modes)

  - c/op_42 / cpp/op_54 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(ins@0(in0:256,F32toF64(ex32@0(in0:256))),CmpEQ64F0x2(ex128@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))),ex128@0(in1:256))))))] S[] E[ret] · (f32,f64)

- ground: cluster
- languages: c, cpp
- members: c `==` (f32,f64, 0 modes); cpp `==` (f32,f64, 0 modes)

  - c/op_484 / cpp/op_484 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(ins@0(in1:256,F32toF64(ex32@0(in1:256))),CmpEQ64F0x2(ex128@0(ins@0(in1:256,F32toF64(ex32@0(in1:256)))),ex128@0(in0:256))))))] S[] E[ret] · (f64,f32)

- ground: cluster
- languages: c, cpp
- members: c `==` (f64,f32, 0 modes); cpp `==` (f64,f32, 0 modes)

  - c/op_489 / cpp/op_489 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),CmpEQ64F0x2(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex128@0(in1:256))))))] S[] E[riprel punpckldq | riprel subpd | ret] · (u64,f64)

- ground: cluster
- languages: c, cpp
- members: c `==` (u64,f64, 0 modes); cpp `==` (u64,f64, 0 modes)

  - c/op_478 / cpp/op_478 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),CmpEQ64F0x2(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex128@0(in0:256))))))] S[] E[riprel punpckldq | riprel subpd | ret] · (f64,u64)

- ground: cluster
- languages: c, cpp
- members: c `==` (f64,u64, 0 modes); cpp `==` (f64,u64, 0 modes)

  - c/op_488 / cpp/op_488 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)))),ex128@0(in1:256))))))] S[] E[ret] · (i64,f32)

- ground: cluster
- languages: c, cpp
- members: c `==` (i64,f32, 0 modes); cpp `==` (i64,f32, 0 modes)

  - c/op_471 / cpp/op_471 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))),CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)))),ex128@0(in0:256))))))] S[] E[ret] · (f32,i64)

- ground: cluster
- languages: c, cpp
- members: c `==` (f32,i64, 0 modes); cpp `==` (f32,i64, 0 modes)

  - c/op_481 / cpp/op_481 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)),CmpEQ64F0x2(ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),ex128@0(in1:256))))))] S[] E[ret] · (i64,f64)

- ground: cluster
- languages: c, cpp
- members: c `==` (i64,f64, 0 modes); cpp `==` (i64,f64, 0 modes)

  - c/op_472 / cpp/op_472 -- **total equality**

### sem-identical group B0 V[zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)),CmpEQ64F0x2(ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))),ex128@0(in0:256))))))] S[] E[ret] · (f64,i64)

- ground: cluster
- languages: c, cpp
- members: c `==` (f64,i64, 0 modes); cpp `==` (f64,i64, 0 modes)

  - c/op_487 / cpp/op_487 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(DivModS64to32(32HLto64(0:32,ex32@0(in0:64)),ex32@0(in1:64)))) zx64(ex32@32(DivModS64to32(32HLto64(0:32,ex32@0(in0:64)),ex32@0(in1:64))))] S[] E[ret] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `/` (bool,i32, 0 modes); cpp `/` (bool,i32, 0 modes)

  - c/op_240 / cpp/op_240 -- **total equality**

### sem-identical group B0 V[zx64(ex32@0(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64)))) zx64(ex32@32(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64))))] S[] E[ret] · (i32,i32)

- ground: cluster
- languages: c, cpp
- members: c `/` (i32,i32, 0 modes); cpp `/` (i32,i32, 0 modes)

  - c/op_210 / cpp/op_210 -- **total equality**

### sem-identical group B0 V[zx64(ex32@32(DivModS64to32(32HLto64(0:32,ex32@0(in0:64)),ex32@0(in1:64)))) zx64(ex32@32(DivModS64to32(32HLto64(0:32,ex32@0(in0:64)),ex32@0(in1:64))))] S[] E[ret] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `%` (bool,i32, 0 modes); cpp `%` (bool,i32, 0 modes)

  - c/op_276 / cpp/op_276 -- **total equality**

### sem-identical group B0 V[zx64(ex32@32(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64)))) zx64(ex32@32(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64))))] S[] E[ret] · (i32,i32)

- ground: cluster
- languages: c, cpp
- members: c `%` (i32,i32, 0 modes); cpp `%` (i32,i32, 0 modes)

  - c/op_246 / cpp/op_246 -- **total equality**

### sem-identical group B0 V[zx64(ite(ex1@0(amd64g_calculate_condition(4:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64)),ex32@0(in0:64),ex32@0(in1:64)))] S[] E[ret] · (bool,i32)

- ground: cluster
- languages: c, cpp
- members: c `*` (bool,i32, 0 modes); cpp `*` (bool,i32, 0 modes)

  - c/op_204 / cpp/op_204 -- **total equality**

### sem-identical group B0 V[zx64(ite(ex1@0(amd64g_calculate_condition(4:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64)),ex32@0(in1:64),ex32@0(in0:64)))] S[] E[ret] · (i32,bool)

- ground: cluster
- languages: c, cpp
- members: c `*` (i32,bool, 0 modes); cpp `*` (i32,bool, 0 modes)

  - c/op_179 / cpp/op_179 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(12:64,8:64,in1:64,in0:64,u0:64)))] S[] E[ret] · (i64,i64)

- ground: cluster
- languages: go, swift
- members: go `>` (i64,i64, 0 modes); swift `>` (i64,i64, 0 modes)

  - go/op_607 / swift/op_337 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(13:64,8:64,in1:64,in0:64,u0:64)))] S[] E[ret] · (i64,i64)

- ground: cluster
- languages: go, swift
- members: go `<=` (i64,i64, 0 modes); swift `<=` (i64,i64, 0 modes)

  - go/op_571 / swift/op_373 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(14:64,8:64,in0:64,in1:64,u0:64)))] S[] E[ret] · (i64,i64)

- ground: cluster
- languages: cpp, rust
- members: cpp `<=` (i64,i64, 0 modes); rust `<=` (i64,i64, 0 modes)

  - cpp/op_613 / rust/op_361 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(15:64,8:64,in0:64,in1:64,u0:64)))] S[] E[ret] · (i64,i64)

- ground: cluster
- languages: cpp, rust
- members: cpp `>` (i64,i64, 0 modes); rust `>` (i64,i64, 0 modes)

  - cpp/op_541 / rust/op_397 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(2:64,8:64,in1:64,in0:64,u0:64)))] S[] E[ret] · (u64,u64)

- ground: cluster
- languages: go, swift
- members: go `>` (u64,u64, 0 modes); swift `>` (u64,u64, 0 modes)

  - go/op_614 / swift/op_344 -- **total equality**

### sem-identical group B0 V[zx8(ex1@0(amd64g_calculate_condition(3:64,8:64,in1:64,in0:64,u0:64)))] S[] E[ret] · (u64,u64)

- ground: cluster
- languages: go, swift
- members: go `<=` (u64,u64, 0 modes); swift `<=` (u64,u64, 0 modes)

  - go/op_578 / swift/op_380 -- **total equality**

### shared-core group st8(Add64(18446744073709551615:64,SP:64))=ex8@0(in0:64) · (bool,None)

- ground: connection
- languages: c, cpp
- members: c `&` (bool,None, 0 modes); cpp `&` (bool,None, 0 modes)

  - c/op_35 / cpp/op_47 -- **total equality**

### shared-core group ins@0(zx64(ex32@0(in0:64)),Xor8(1:8,ex8@0(in0:64))) · (bool,None)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `--` (bool,None, 0 modes); cpp `not` (bool,None, 1 modes); cpp `!` (bool,None, 1 modes); rust `!` (bool,None, 1 modes); swift `!` (bool,None, 1 modes)

  - c/op_47 / cpp/op_29 -- **core equality, modes differ**
    - only on the right: `in0 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_47 / cpp/op_5 -- **core equality, modes differ**
    - only on the right: `in0 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_47 / rust/op_17 -- **core equality, modes differ**
    - only on the right: `in0 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_47 / swift/op_29 -- **core equality, modes differ**
    - only on the right: `in0 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - cpp/op_29 / rust/op_17 -- **total equality**
  - cpp/op_5 / rust/op_17 -- **total equality**
  - cpp/op_29 / swift/op_29 -- **total equality**
  - cpp/op_5 / swift/op_29 -- **total equality**
  - rust/op_17 / swift/op_29 -- **total equality**

### shared-core group zx64(Sub32(0:32,ex32@0(in0:64))) · (bool,None)

- ground: connection
- languages: c, cpp
- members: c `-` (bool,None, 0 modes); cpp `-` (bool,None, 0 modes)

  - c/op_17 / cpp/op_17 -- **total equality**

### shared-core group zx64(Not32(ex32@0(in0:64))) · (bool,None)

- ground: connection
- languages: c, cpp
- members: c `~` (bool,None, 0 modes); cpp `~` (bool,None, 0 modes); cpp `compl` (bool,None, 0 modes)

  - c/op_11 / cpp/op_11 -- **total equality**
  - c/op_11 / cpp/op_35 -- **total equality**

### shared-core group Xor8(1:8,ex8@0(in0:64)) · (bool,None)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `--` (bool,None, 0 modes); c `!` (bool,None, 4 modes); cpp `not` (bool,None, 1 modes); cpp `!` (bool,None, 1 modes); rust `!` (bool,None, 1 modes); swift `!` (bool,None, 1 modes)

  - c/op_47 / cpp/op_29 -- **core equality, modes differ**
    - only on the right: `in0 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_47 / cpp/op_5 -- **core equality, modes differ**
    - only on the right: `in0 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_5 / cpp/op_29 -- **core difference**
  - c/op_5 / cpp/op_5 -- **core difference**
  - c/op_47 / rust/op_17 -- **core equality, modes differ**
    - only on the right: `in0 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_5 / rust/op_17 -- **core difference**
  - c/op_47 / swift/op_29 -- **core equality, modes differ**
    - only on the right: `in0 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_5 / swift/op_29 -- **core difference**
  - cpp/op_29 / rust/op_17 -- **total equality**
  - cpp/op_5 / rust/op_17 -- **total equality**
  - cpp/op_29 / swift/op_29 -- **total equality**
  - cpp/op_5 / swift/op_29 -- **total equality**
  - rust/op_17 / swift/op_29 -- **total equality**

### shared-core group ins@0(zx64(Xor32(ex32@0(in0:64),ex32@0(in1:64))),Xor8(1:8,Xor8(ex8@0(in0:64),ex8@0(in1:64)))) · (bool,bool)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `==` (bool,bool, 0 modes); cpp `==` (bool,bool, 0 modes); rust `==` (bool,bool, 0 modes); swift `==` (bool,bool, 0 modes)

  - c/op_497 / cpp/op_497 -- **core difference**
  - c/op_497 / rust/op_281 -- **core difference**
  - c/op_497 / swift/op_545 -- **core difference**
  - cpp/op_497 / rust/op_281 -- **total equality**
  - cpp/op_497 / swift/op_545 -- **total equality**
  - rust/op_281 / swift/op_545 -- **total equality**

### shared-core group ins@0(zx64(ex32@0(in1:64)),And8(Xor8(1:8,ex8@0(in1:64)),ex8@0(in0:64))) · (bool,bool)

- ground: connection
- languages: cpp, rust
- members: cpp `>` (bool,bool, 1 modes); rust `>` (bool,bool, 1 modes)

  - cpp/op_569 / rust/op_425 -- **total equality**

### shared-core group ins@0(zx64(ex32@0(in0:64)),And8(Xor8(1:8,ex8@0(in0:64)),ex8@0(in1:64))) · (bool,bool)

- ground: connection
- languages: cpp, rust
- members: cpp `<` (bool,bool, 1 modes); rust `<` (bool,bool, 1 modes)

  - cpp/op_677 / rust/op_353 -- **total equality**

### shared-core group ins@0(zx64(ex32@0(in1:64)),Or8(Xor8(1:8,ex8@0(in1:64)),ex8@0(in0:64))) · (bool,bool)

- ground: connection
- languages: cpp, rust
- members: cpp `>=` (bool,bool, 1 modes); rust `>=` (bool,bool, 1 modes)

  - cpp/op_605 / rust/op_461 -- **total equality**

### shared-core group ins@0(zx64(ex32@0(in0:64)),Or8(Xor8(1:8,ex8@0(in0:64)),ex8@0(in1:64))) · (bool,bool)

- ground: connection
- languages: cpp, rust
- members: cpp `<=` (bool,bool, 1 modes); rust `<=` (bool,bool, 1 modes)

  - cpp/op_641 / rust/op_389 -- **total equality**

### shared-core group zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) · (bool,bool)

- ground: connection
- languages: c, cpp
- members: c `<<` (bool,bool, 0 modes); cpp `<<` (bool,bool, 0 modes)

  - c/op_713 / cpp/op_713 -- **total equality**

### shared-core group zx64(ex32@0(Shr64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) · (bool,bool)

- ground: connection
- languages: c, cpp
- members: c `>>` (bool,bool, 0 modes); cpp `>>` (bool,bool, 0 modes)

  - c/op_749 / cpp/op_749 -- **total equality**

### shared-core group And8(Xor8(1:8,ex8@0(in1:64)),ex8@0(in0:64)) · (bool,bool)

- ground: connection
- languages: c, cpp, rust
- members: c `>` (bool,bool, 2 modes); cpp `>` (bool,bool, 1 modes); rust `>` (bool,bool, 1 modes)

  - c/op_569 / cpp/op_569 -- **core difference**
  - c/op_569 / rust/op_425 -- **core difference**
  - cpp/op_569 / rust/op_425 -- **total equality**

### shared-core group And8(Xor8(1:8,ex8@0(in0:64)),ex8@0(in1:64)) · (bool,bool)

- ground: connection
- languages: c, cpp, rust
- members: c `<` (bool,bool, 2 modes); cpp `<` (bool,bool, 1 modes); rust `<` (bool,bool, 1 modes)

  - c/op_677 / cpp/op_677 -- **core difference**
  - c/op_677 / rust/op_353 -- **core difference**
  - cpp/op_677 / rust/op_353 -- **total equality**

### shared-core group zx64(Add32(ex32@0(in0:64),ex32@0(in1:64))) · (bool,bool)

- ground: connection
- languages: c, cpp
- members: c `+` (bool,bool, 0 modes); cpp `+` (bool,bool, 0 modes)

  - c/op_137 / cpp/op_137 -- **total equality**

### shared-core group zx64(Sub32(ex32@0(in0:64),ex32@0(in1:64))) · (bool,bool)

- ground: connection
- languages: c, cpp
- members: c `-` (bool,bool, 0 modes); cpp `-` (bool,bool, 0 modes)

  - c/op_173 / cpp/op_173 -- **total equality**

### shared-core group zx64(And32(ex32@0(in0:64),ex32@0(in1:64))) · (bool,bool)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `*` (bool,bool, 0 modes); c `&&` (bool,bool, 0 modes); c `&` (bool,bool, 0 modes); cpp `*` (bool,bool, 0 modes); cpp `&&` (bool,bool, 0 modes); cpp `&` (bool,bool, 0 modes); cpp `and` (bool,bool, 0 modes); cpp `bitand` (bool,bool, 0 modes); go `&&` (bool,bool, 0 modes); rust `&&` (bool,bool, 0 modes); rust `&` (bool,bool, 0 modes); swift `&&` (bool,bool, 0 modes)

  - c/op_209 / cpp/op_209 -- **total equality**
  - c/op_209 / cpp/op_353 -- **total equality**
  - c/op_209 / cpp/op_461 -- **total equality**
  - c/op_209 / cpp/op_857 -- **total equality**
  - c/op_209 / cpp/op_965 -- **total equality**
  - c/op_353 / cpp/op_209 -- **total equality**
  - c/op_353 / cpp/op_353 -- **total equality**
  - c/op_353 / cpp/op_461 -- **total equality**
  - c/op_353 / cpp/op_857 -- **total equality**
  - c/op_353 / cpp/op_965 -- **total equality**
  - c/op_461 / cpp/op_209 -- **total equality**
  - c/op_461 / cpp/op_353 -- **total equality**
  - c/op_461 / cpp/op_461 -- **total equality**
  - c/op_461 / cpp/op_857 -- **total equality**
  - c/op_461 / cpp/op_965 -- **total equality**
  - c/op_209 / go/op_707 -- **total equality**
  - c/op_353 / go/op_707 -- **total equality**
  - c/op_461 / go/op_707 -- **total equality**
  - c/op_209 / rust/op_101 -- **total equality**
  - c/op_209 / rust/op_173 -- **total equality**
  - c/op_353 / rust/op_101 -- **total equality**
  - c/op_353 / rust/op_173 -- **total equality**
  - c/op_461 / rust/op_101 -- **total equality**
  - c/op_461 / rust/op_173 -- **total equality**
  - c/op_209 / swift/op_797 -- **total equality**
  - c/op_353 / swift/op_797 -- **total equality**
  - c/op_461 / swift/op_797 -- **total equality**
  - cpp/op_209 / go/op_707 -- **total equality**
  - cpp/op_353 / go/op_707 -- **total equality**
  - cpp/op_461 / go/op_707 -- **total equality**
  - cpp/op_857 / go/op_707 -- **total equality**
  - cpp/op_965 / go/op_707 -- **total equality**
  - cpp/op_209 / rust/op_101 -- **total equality**
  - cpp/op_209 / rust/op_173 -- **total equality**
  - cpp/op_353 / rust/op_101 -- **total equality**
  - cpp/op_353 / rust/op_173 -- **total equality**
  - cpp/op_461 / rust/op_101 -- **total equality**
  - cpp/op_461 / rust/op_173 -- **total equality**
  - cpp/op_857 / rust/op_101 -- **total equality**
  - cpp/op_857 / rust/op_173 -- **total equality**
  - cpp/op_965 / rust/op_101 -- **total equality**
  - cpp/op_965 / rust/op_173 -- **total equality**
  - cpp/op_209 / swift/op_797 -- **total equality**
  - cpp/op_353 / swift/op_797 -- **total equality**
  - cpp/op_461 / swift/op_797 -- **total equality**
  - cpp/op_857 / swift/op_797 -- **total equality**
  - cpp/op_965 / swift/op_797 -- **total equality**
  - go/op_707 / rust/op_101 -- **total equality**
  - go/op_707 / rust/op_173 -- **total equality**
  - go/op_707 / swift/op_797 -- **total equality**
  - rust/op_101 / swift/op_797 -- **total equality**
  - rust/op_173 / swift/op_797 -- **total equality**

### shared-core group zx64(Xor32(ex32@0(in0:64),ex32@0(in1:64))) · (bool,bool)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `^` (bool,bool, 0 modes); c `==` (bool,bool, 0 modes); c `!=` (bool,bool, 0 modes); cpp `not_eq` (bool,bool, 0 modes); cpp `^` (bool,bool, 0 modes); cpp `==` (bool,bool, 0 modes); cpp `!=` (bool,bool, 0 modes); cpp `xor` (bool,bool, 0 modes); rust `^` (bool,bool, 0 modes); rust `==` (bool,bool, 0 modes); rust `!=` (bool,bool, 0 modes); swift `!=` (bool,bool, 0 modes); swift `==` (bool,bool, 0 modes)

  - c/op_425 / cpp/op_1001 -- **total equality**
  - c/op_425 / cpp/op_425 -- **total equality**
  - c/op_425 / cpp/op_497 -- **core difference**
  - c/op_425 / cpp/op_533 -- **total equality**
  - c/op_425 / cpp/op_929 -- **total equality**
  - c/op_497 / cpp/op_1001 -- **core difference**
  - c/op_497 / cpp/op_425 -- **core difference**
  - c/op_497 / cpp/op_497 -- **core difference**
  - c/op_497 / cpp/op_533 -- **core difference**
  - c/op_497 / cpp/op_929 -- **core difference**
  - c/op_533 / cpp/op_1001 -- **total equality**
  - c/op_533 / cpp/op_425 -- **total equality**
  - c/op_533 / cpp/op_497 -- **core difference**
  - c/op_533 / cpp/op_533 -- **total equality**
  - c/op_533 / cpp/op_929 -- **total equality**
  - c/op_425 / rust/op_245 -- **total equality**
  - c/op_425 / rust/op_281 -- **core difference**
  - c/op_425 / rust/op_317 -- **total equality**
  - c/op_497 / rust/op_245 -- **core difference**
  - c/op_497 / rust/op_281 -- **core difference**
  - c/op_497 / rust/op_317 -- **core difference**
  - c/op_533 / rust/op_245 -- **total equality**
  - c/op_533 / rust/op_281 -- **core difference**
  - c/op_533 / rust/op_317 -- **total equality**
  - c/op_425 / swift/op_473 -- **total equality**
  - c/op_425 / swift/op_545 -- **core difference**
  - c/op_497 / swift/op_473 -- **core difference**
  - c/op_497 / swift/op_545 -- **core difference**
  - c/op_533 / swift/op_473 -- **total equality**
  - c/op_533 / swift/op_545 -- **core difference**
  - cpp/op_1001 / rust/op_245 -- **total equality**
  - cpp/op_1001 / rust/op_281 -- **core difference**
  - cpp/op_1001 / rust/op_317 -- **total equality**
  - cpp/op_425 / rust/op_245 -- **total equality**
  - cpp/op_425 / rust/op_281 -- **core difference**
  - cpp/op_425 / rust/op_317 -- **total equality**
  - cpp/op_497 / rust/op_245 -- **core difference**
  - cpp/op_497 / rust/op_281 -- **total equality**
  - cpp/op_497 / rust/op_317 -- **core difference**
  - cpp/op_533 / rust/op_245 -- **total equality**
  - cpp/op_533 / rust/op_281 -- **core difference**
  - cpp/op_533 / rust/op_317 -- **total equality**
  - cpp/op_929 / rust/op_245 -- **total equality**
  - cpp/op_929 / rust/op_281 -- **core difference**
  - cpp/op_929 / rust/op_317 -- **total equality**
  - cpp/op_1001 / swift/op_473 -- **total equality**
  - cpp/op_1001 / swift/op_545 -- **core difference**
  - cpp/op_425 / swift/op_473 -- **total equality**
  - cpp/op_425 / swift/op_545 -- **core difference**
  - cpp/op_497 / swift/op_473 -- **core difference**
  - cpp/op_497 / swift/op_545 -- **total equality**
  - cpp/op_533 / swift/op_473 -- **total equality**
  - cpp/op_533 / swift/op_545 -- **core difference**
  - cpp/op_929 / swift/op_473 -- **total equality**
  - cpp/op_929 / swift/op_545 -- **core difference**
  - rust/op_245 / swift/op_473 -- **total equality**
  - rust/op_245 / swift/op_545 -- **core difference**
  - rust/op_281 / swift/op_473 -- **core difference**
  - rust/op_281 / swift/op_545 -- **total equality**
  - rust/op_317 / swift/op_473 -- **total equality**
  - rust/op_317 / swift/op_545 -- **core difference**

### shared-core group Or8(Xor8(1:8,ex8@0(in1:64)),ex8@0(in0:64)) · (bool,bool)

- ground: connection
- languages: c, cpp, rust
- members: c `>=` (bool,bool, 2 modes); cpp `>=` (bool,bool, 1 modes); rust `>=` (bool,bool, 1 modes)

  - c/op_605 / cpp/op_605 -- **core difference**
  - c/op_605 / rust/op_461 -- **core difference**
  - cpp/op_605 / rust/op_461 -- **total equality**

### shared-core group Or8(Xor8(1:8,ex8@0(in0:64)),ex8@0(in1:64)) · (bool,bool)

- ground: connection
- languages: c, cpp, rust
- members: c `<=` (bool,bool, 2 modes); cpp `<=` (bool,bool, 1 modes); rust `<=` (bool,bool, 1 modes)

  - c/op_641 / cpp/op_641 -- **core difference**
  - c/op_641 / rust/op_389 -- **core difference**
  - cpp/op_641 / rust/op_389 -- **total equality**

### shared-core group zx64(Or32(ex32@0(in0:64),ex32@0(in1:64))) · (bool,bool)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `||` (bool,bool, 0 modes); c `|` (bool,bool, 0 modes); cpp `||` (bool,bool, 0 modes); cpp `|` (bool,bool, 0 modes); cpp `or` (bool,bool, 0 modes); cpp `bitor` (bool,bool, 0 modes); go `||` (bool,bool, 0 modes); rust `||` (bool,bool, 0 modes); rust `|` (bool,bool, 0 modes); swift `||` (bool,bool, 0 modes)

  - c/op_317 / cpp/op_317 -- **total equality**
  - c/op_317 / cpp/op_389 -- **total equality**
  - c/op_317 / cpp/op_821 -- **total equality**
  - c/op_317 / cpp/op_893 -- **total equality**
  - c/op_389 / cpp/op_317 -- **total equality**
  - c/op_389 / cpp/op_389 -- **total equality**
  - c/op_389 / cpp/op_821 -- **total equality**
  - c/op_389 / cpp/op_893 -- **total equality**
  - c/op_317 / go/op_743 -- **total equality**
  - c/op_389 / go/op_743 -- **total equality**
  - c/op_317 / rust/op_137 -- **total equality**
  - c/op_317 / rust/op_209 -- **total equality**
  - c/op_389 / rust/op_137 -- **total equality**
  - c/op_389 / rust/op_209 -- **total equality**
  - c/op_317 / swift/op_833 -- **total equality**
  - c/op_389 / swift/op_833 -- **total equality**
  - cpp/op_317 / go/op_743 -- **total equality**
  - cpp/op_389 / go/op_743 -- **total equality**
  - cpp/op_821 / go/op_743 -- **total equality**
  - cpp/op_893 / go/op_743 -- **total equality**
  - cpp/op_317 / rust/op_137 -- **total equality**
  - cpp/op_317 / rust/op_209 -- **total equality**
  - cpp/op_389 / rust/op_137 -- **total equality**
  - cpp/op_389 / rust/op_209 -- **total equality**
  - cpp/op_821 / rust/op_137 -- **total equality**
  - cpp/op_821 / rust/op_209 -- **total equality**
  - cpp/op_893 / rust/op_137 -- **total equality**
  - cpp/op_893 / rust/op_209 -- **total equality**
  - cpp/op_317 / swift/op_833 -- **total equality**
  - cpp/op_389 / swift/op_833 -- **total equality**
  - cpp/op_821 / swift/op_833 -- **total equality**
  - cpp/op_893 / swift/op_833 -- **total equality**
  - go/op_743 / rust/op_137 -- **total equality**
  - go/op_743 / rust/op_209 -- **total equality**
  - go/op_743 / swift/op_833 -- **total equality**
  - rust/op_137 / swift/op_833 -- **total equality**
  - rust/op_209 / swift/op_833 -- **total equality**

### shared-core group Xor8(ex8@0(in0:64),ex8@0(in1:64)) · (bool,bool)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `==` (bool,bool, 0 modes); cpp `==` (bool,bool, 0 modes); cpp `<=>` (bool,bool, 0 modes); rust `==` (bool,bool, 0 modes); swift `==` (bool,bool, 0 modes)

  - c/op_497 / cpp/op_497 -- **core difference**
  - c/op_497 / cpp/op_785 -- **core difference**
  - c/op_497 / rust/op_281 -- **core difference**
  - c/op_497 / swift/op_545 -- **core difference**
  - cpp/op_497 / rust/op_281 -- **total equality**
  - cpp/op_785 / rust/op_281 -- **core difference**
  - cpp/op_497 / swift/op_545 -- **total equality**
  - cpp/op_785 / swift/op_545 -- **core difference**
  - rust/op_281 / swift/op_545 -- **total equality**

### shared-core group And8(31:8,ex8@0(in1:64)) · (bool,bool)

- ground: connection
- languages: c, cpp
- members: c `<<` (bool,bool, 0 modes); c `>>` (bool,bool, 0 modes); cpp `<<` (bool,bool, 0 modes); cpp `>>` (bool,bool, 0 modes)

  - c/op_713 / cpp/op_713 -- **total equality**
  - c/op_713 / cpp/op_749 -- **core difference**
  - c/op_749 / cpp/op_713 -- **core difference**
  - c/op_749 / cpp/op_749 -- **total equality**

### shared-core group Xor8(1:8,ex8@0(in1:64)) · (bool,bool)

- ground: connection
- languages: c, cpp, rust
- members: c `>` (bool,bool, 2 modes); c `>=` (bool,bool, 2 modes); cpp `>` (bool,bool, 1 modes); cpp `>=` (bool,bool, 1 modes); rust `>` (bool,bool, 1 modes); rust `>=` (bool,bool, 1 modes)

  - c/op_569 / cpp/op_569 -- **core difference**
  - c/op_569 / cpp/op_605 -- **core difference**
  - c/op_605 / cpp/op_569 -- **core difference**
  - c/op_605 / cpp/op_605 -- **core difference**
  - c/op_569 / rust/op_425 -- **core difference**
  - c/op_569 / rust/op_461 -- **core difference**
  - c/op_605 / rust/op_425 -- **core difference**
  - c/op_605 / rust/op_461 -- **core difference**
  - cpp/op_569 / rust/op_425 -- **total equality**
  - cpp/op_569 / rust/op_461 -- **core difference**
  - cpp/op_605 / rust/op_425 -- **core difference**
  - cpp/op_605 / rust/op_461 -- **total equality**

### shared-core group Xor8(1:8,ex8@0(in0:64)) · (bool,bool)

- ground: connection
- languages: c, cpp, rust
- members: c `<=` (bool,bool, 2 modes); c `<` (bool,bool, 2 modes); cpp `<=` (bool,bool, 1 modes); cpp `<` (bool,bool, 1 modes); rust `<` (bool,bool, 1 modes); rust `<=` (bool,bool, 1 modes)

  - c/op_641 / cpp/op_641 -- **core difference**
  - c/op_641 / cpp/op_677 -- **core difference**
  - c/op_677 / cpp/op_641 -- **core difference**
  - c/op_677 / cpp/op_677 -- **core difference**
  - c/op_641 / rust/op_353 -- **core difference**
  - c/op_641 / rust/op_389 -- **core difference**
  - c/op_677 / rust/op_353 -- **core difference**
  - c/op_677 / rust/op_389 -- **core difference**
  - cpp/op_641 / rust/op_353 -- **core difference**
  - cpp/op_641 / rust/op_389 -- **total equality**
  - cpp/op_677 / rust/op_353 -- **total equality**
  - cpp/op_677 / rust/op_389 -- **core difference**

### shared-core group And8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64)))),ex8@0(in0:64)) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `&&` (bool,f32, 0 modes); cpp `&&` (bool,f32, 0 modes); cpp `and` (bool,f32, 0 modes)

  - c/op_351 / cpp/op_351 -- **core difference**
  - c/op_351 / cpp/op_855 -- **core difference**

### shared-core group Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64)))),ex8@0(in0:64)) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `||` (bool,f32, 0 modes); cpp `||` (bool,f32, 0 modes); cpp `or` (bool,f32, 0 modes)

  - c/op_315 / cpp/op_315 -- **core difference**
  - c/op_315 / cpp/op_819 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64)))) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `||` (bool,f32, 0 modes); c `&&` (bool,f32, 0 modes); cpp `||` (bool,f32, 0 modes); cpp `&&` (bool,f32, 0 modes); cpp `or` (bool,f32, 0 modes); cpp `and` (bool,f32, 0 modes)

  - c/op_315 / cpp/op_315 -- **core difference**
  - c/op_315 / cpp/op_351 -- **core difference**
  - c/op_315 / cpp/op_819 -- **core difference**
  - c/op_315 / cpp/op_855 -- **core difference**
  - c/op_351 / cpp/op_315 -- **core difference**
  - c/op_351 / cpp/op_351 -- **core difference**
  - c/op_351 / cpp/op_819 -- **core difference**
  - c/op_351 / cpp/op_855 -- **core difference**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))),CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256)))))) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `==` (bool,f32, 0 modes); cpp `==` (bool,f32, 0 modes)

  - c/op_495 / cpp/op_495 -- **total equality**

### shared-core group ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))),XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256)))) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `!=` (bool,f32, 0 modes); cpp `!=` (bool,f32, 0 modes); cpp `not_eq` (bool,f32, 0 modes)

  - c/op_531 / cpp/op_531 -- **total equality**
  - c/op_531 / cpp/op_999 -- **total equality**

### shared-core group ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))),Sub32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256))) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `-` (bool,f32, 0 modes); cpp `-` (bool,f32, 0 modes)

  - c/op_171 / cpp/op_171 -- **total equality**

### shared-core group ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))),Div32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256))) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `/` (bool,f32, 0 modes); cpp `/` (bool,f32, 0 modes)

  - c/op_243 / cpp/op_243 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in0:64)))),F32toF64(ex32@0(in1:256))))),0:64,u1:64))) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `>` (bool,f32, 0 modes); cpp `>` (bool,f32, 0 modes)

  - c/op_567 / cpp/op_567 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in0:64)))),F32toF64(ex32@0(in1:256))))),0:64,u1:64))) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `>=` (bool,f32, 0 modes); cpp `>=` (bool,f32, 0 modes)

  - c/op_603 / cpp/op_603 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in0:64))))))),0:64,u1:64))) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `<=` (bool,f32, 0 modes); cpp `<=` (bool,f32, 0 modes)

  - c/op_639 / cpp/op_639 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in0:64))))))),0:64,u1:64))) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `<` (bool,f32, 0 modes); cpp `<` (bool,f32, 0 modes)

  - c/op_675 / cpp/op_675 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in0:64)))),F32toF64(ex32@0(in1:256))))) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `>` (bool,f32, 0 modes); c `>=` (bool,f32, 0 modes); cpp `>` (bool,f32, 0 modes); cpp `>=` (bool,f32, 0 modes)

  - c/op_567 / cpp/op_567 -- **core difference**
  - c/op_567 / cpp/op_603 -- **core difference**
  - c/op_603 / cpp/op_567 -- **core difference**
  - c/op_603 / cpp/op_603 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in0:64))))))) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `<=` (bool,f32, 0 modes); c `<` (bool,f32, 0 modes); cpp `<=` (bool,f32, 0 modes); cpp `<` (bool,f32, 0 modes)

  - c/op_639 / cpp/op_639 -- **core difference**
  - c/op_639 / cpp/op_675 -- **core difference**
  - c/op_675 / cpp/op_639 -- **core difference**
  - c/op_675 / cpp/op_675 -- **core difference**

### shared-core group CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256)) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `==` (bool,f32, 0 modes); c `!=` (bool,f32, 0 modes); cpp `==` (bool,f32, 0 modes); cpp `!=` (bool,f32, 0 modes); cpp `not_eq` (bool,f32, 0 modes)

  - c/op_495 / cpp/op_495 -- **total equality**
  - c/op_495 / cpp/op_531 -- **core difference**
  - c/op_495 / cpp/op_999 -- **core difference**
  - c/op_531 / cpp/op_495 -- **core difference**
  - c/op_531 / cpp/op_531 -- **total equality**
  - c/op_531 / cpp/op_999 -- **total equality**

### shared-core group Add32F0x4(ex128@0(in1:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))))) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `+` (bool,f32, 0 modes); cpp `+` (bool,f32, 0 modes)

  - c/op_135 / cpp/op_135 -- **total equality**

### shared-core group Mul32F0x4(ex128@0(in1:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))))) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `*` (bool,f32, 0 modes); cpp `*` (bool,f32, 0 modes)

  - c/op_207 / cpp/op_207 -- **total equality**

### shared-core group ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `+` (bool,f32, 0 modes); c `-` (bool,f32, 0 modes); c `*` (bool,f32, 0 modes); c `/` (bool,f32, 0 modes); c `==` (bool,f32, 0 modes); c `!=` (bool,f32, 0 modes); cpp `+` (bool,f32, 0 modes); cpp `-` (bool,f32, 0 modes); cpp `*` (bool,f32, 0 modes); cpp `/` (bool,f32, 0 modes); cpp `==` (bool,f32, 0 modes); cpp `!=` (bool,f32, 0 modes); cpp `not_eq` (bool,f32, 0 modes)

  - c/op_135 / cpp/op_135 -- **total equality**
  - c/op_135 / cpp/op_171 -- **core difference**
  - c/op_135 / cpp/op_207 -- **core difference**
  - c/op_135 / cpp/op_243 -- **core difference**
  - c/op_135 / cpp/op_495 -- **core difference**
  - c/op_135 / cpp/op_531 -- **core difference**
  - c/op_135 / cpp/op_999 -- **core difference**
  - c/op_171 / cpp/op_135 -- **core difference**
  - c/op_171 / cpp/op_171 -- **total equality**
  - c/op_171 / cpp/op_207 -- **core difference**
  - c/op_171 / cpp/op_243 -- **core difference**
  - c/op_171 / cpp/op_495 -- **core difference**
  - c/op_171 / cpp/op_531 -- **core difference**
  - c/op_171 / cpp/op_999 -- **core difference**
  - c/op_207 / cpp/op_135 -- **core difference**
  - c/op_207 / cpp/op_171 -- **core difference**
  - c/op_207 / cpp/op_207 -- **total equality**
  - c/op_207 / cpp/op_243 -- **core difference**
  - c/op_207 / cpp/op_495 -- **core difference**
  - c/op_207 / cpp/op_531 -- **core difference**
  - c/op_207 / cpp/op_999 -- **core difference**
  - c/op_243 / cpp/op_135 -- **core difference**
  - c/op_243 / cpp/op_171 -- **core difference**
  - c/op_243 / cpp/op_207 -- **core difference**
  - c/op_243 / cpp/op_243 -- **total equality**
  - c/op_243 / cpp/op_495 -- **core difference**
  - c/op_243 / cpp/op_531 -- **core difference**
  - c/op_243 / cpp/op_999 -- **core difference**
  - c/op_495 / cpp/op_135 -- **core difference**
  - c/op_495 / cpp/op_171 -- **core difference**
  - c/op_495 / cpp/op_207 -- **core difference**
  - c/op_495 / cpp/op_243 -- **core difference**
  - c/op_495 / cpp/op_495 -- **total equality**
  - c/op_495 / cpp/op_531 -- **core difference**
  - c/op_495 / cpp/op_999 -- **core difference**
  - c/op_531 / cpp/op_135 -- **core difference**
  - c/op_531 / cpp/op_171 -- **core difference**
  - c/op_531 / cpp/op_207 -- **core difference**
  - c/op_531 / cpp/op_243 -- **core difference**
  - c/op_531 / cpp/op_495 -- **core difference**
  - c/op_531 / cpp/op_531 -- **total equality**
  - c/op_531 / cpp/op_999 -- **total equality**

### shared-core group F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in0:64)))) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `>` (bool,f32, 0 modes); c `>=` (bool,f32, 0 modes); c `<=` (bool,f32, 0 modes); c `<` (bool,f32, 0 modes); cpp `>` (bool,f32, 0 modes); cpp `>=` (bool,f32, 0 modes); cpp `<=` (bool,f32, 0 modes); cpp `<` (bool,f32, 0 modes)

  - c/op_567 / cpp/op_567 -- **core difference**
  - c/op_567 / cpp/op_603 -- **core difference**
  - c/op_567 / cpp/op_639 -- **core difference**
  - c/op_567 / cpp/op_675 -- **core difference**
  - c/op_603 / cpp/op_567 -- **core difference**
  - c/op_603 / cpp/op_603 -- **core difference**
  - c/op_603 / cpp/op_639 -- **core difference**
  - c/op_603 / cpp/op_675 -- **core difference**
  - c/op_639 / cpp/op_567 -- **core difference**
  - c/op_639 / cpp/op_603 -- **core difference**
  - c/op_639 / cpp/op_639 -- **core difference**
  - c/op_639 / cpp/op_675 -- **core difference**
  - c/op_675 / cpp/op_567 -- **core difference**
  - c/op_675 / cpp/op_603 -- **core difference**
  - c/op_675 / cpp/op_639 -- **core difference**
  - c/op_675 / cpp/op_675 -- **core difference**

### shared-core group I32StoF64(ex32@0(in0:64)) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `+` (bool,f32, 0 modes); c `-` (bool,f32, 0 modes); c `*` (bool,f32, 0 modes); c `/` (bool,f32, 0 modes); c `==` (bool,f32, 0 modes); c `!=` (bool,f32, 0 modes); c `>` (bool,f32, 0 modes); c `>=` (bool,f32, 0 modes); c `<=` (bool,f32, 0 modes); c `<` (bool,f32, 0 modes); cpp `+` (bool,f32, 0 modes); cpp `-` (bool,f32, 0 modes); cpp `*` (bool,f32, 0 modes); cpp `/` (bool,f32, 0 modes); cpp `==` (bool,f32, 0 modes); cpp `!=` (bool,f32, 0 modes); cpp `>` (bool,f32, 0 modes); cpp `>=` (bool,f32, 0 modes); cpp `<=` (bool,f32, 0 modes); cpp `<` (bool,f32, 0 modes); cpp `not_eq` (bool,f32, 0 modes)

  - c/op_135 / cpp/op_135 -- **total equality**
  - c/op_135 / cpp/op_171 -- **core difference**
  - c/op_135 / cpp/op_207 -- **core difference**
  - c/op_135 / cpp/op_243 -- **core difference**
  - c/op_135 / cpp/op_495 -- **core difference**
  - c/op_135 / cpp/op_531 -- **core difference**
  - c/op_135 / cpp/op_567 -- **core difference**
  - c/op_135 / cpp/op_603 -- **core difference**
  - c/op_135 / cpp/op_639 -- **core difference**
  - c/op_135 / cpp/op_675 -- **core difference**
  - c/op_135 / cpp/op_999 -- **core difference**
  - c/op_171 / cpp/op_135 -- **core difference**
  - c/op_171 / cpp/op_171 -- **total equality**
  - c/op_171 / cpp/op_207 -- **core difference**
  - c/op_171 / cpp/op_243 -- **core difference**
  - c/op_171 / cpp/op_495 -- **core difference**
  - c/op_171 / cpp/op_531 -- **core difference**
  - c/op_171 / cpp/op_567 -- **core difference**
  - c/op_171 / cpp/op_603 -- **core difference**
  - c/op_171 / cpp/op_639 -- **core difference**
  - c/op_171 / cpp/op_675 -- **core difference**
  - c/op_171 / cpp/op_999 -- **core difference**
  - c/op_207 / cpp/op_135 -- **core difference**
  - c/op_207 / cpp/op_171 -- **core difference**
  - c/op_207 / cpp/op_207 -- **total equality**
  - c/op_207 / cpp/op_243 -- **core difference**
  - c/op_207 / cpp/op_495 -- **core difference**
  - c/op_207 / cpp/op_531 -- **core difference**
  - c/op_207 / cpp/op_567 -- **core difference**
  - c/op_207 / cpp/op_603 -- **core difference**
  - c/op_207 / cpp/op_639 -- **core difference**
  - c/op_207 / cpp/op_675 -- **core difference**
  - c/op_207 / cpp/op_999 -- **core difference**
  - c/op_243 / cpp/op_135 -- **core difference**
  - c/op_243 / cpp/op_171 -- **core difference**
  - c/op_243 / cpp/op_207 -- **core difference**
  - c/op_243 / cpp/op_243 -- **total equality**
  - c/op_243 / cpp/op_495 -- **core difference**
  - c/op_243 / cpp/op_531 -- **core difference**
  - c/op_243 / cpp/op_567 -- **core difference**
  - c/op_243 / cpp/op_603 -- **core difference**
  - c/op_243 / cpp/op_639 -- **core difference**
  - c/op_243 / cpp/op_675 -- **core difference**
  - c/op_243 / cpp/op_999 -- **core difference**
  - c/op_495 / cpp/op_135 -- **core difference**
  - c/op_495 / cpp/op_171 -- **core difference**
  - c/op_495 / cpp/op_207 -- **core difference**
  - c/op_495 / cpp/op_243 -- **core difference**
  - c/op_495 / cpp/op_495 -- **total equality**
  - c/op_495 / cpp/op_531 -- **core difference**
  - c/op_495 / cpp/op_567 -- **core difference**
  - c/op_495 / cpp/op_603 -- **core difference**
  - c/op_495 / cpp/op_639 -- **core difference**
  - c/op_495 / cpp/op_675 -- **core difference**
  - c/op_495 / cpp/op_999 -- **core difference**
  - c/op_531 / cpp/op_135 -- **core difference**
  - c/op_531 / cpp/op_171 -- **core difference**
  - c/op_531 / cpp/op_207 -- **core difference**
  - c/op_531 / cpp/op_243 -- **core difference**
  - c/op_531 / cpp/op_495 -- **core difference**
  - c/op_531 / cpp/op_531 -- **total equality**
  - c/op_531 / cpp/op_567 -- **core difference**
  - c/op_531 / cpp/op_603 -- **core difference**
  - c/op_531 / cpp/op_639 -- **core difference**
  - c/op_531 / cpp/op_675 -- **core difference**
  - c/op_531 / cpp/op_999 -- **total equality**
  - c/op_567 / cpp/op_135 -- **core difference**
  - c/op_567 / cpp/op_171 -- **core difference**
  - c/op_567 / cpp/op_207 -- **core difference**
  - c/op_567 / cpp/op_243 -- **core difference**
  - c/op_567 / cpp/op_495 -- **core difference**
  - c/op_567 / cpp/op_531 -- **core difference**
  - c/op_567 / cpp/op_567 -- **core difference**
  - c/op_567 / cpp/op_603 -- **core difference**
  - c/op_567 / cpp/op_639 -- **core difference**
  - c/op_567 / cpp/op_675 -- **core difference**
  - c/op_567 / cpp/op_999 -- **core difference**
  - c/op_603 / cpp/op_135 -- **core difference**
  - c/op_603 / cpp/op_171 -- **core difference**
  - c/op_603 / cpp/op_207 -- **core difference**
  - c/op_603 / cpp/op_243 -- **core difference**
  - c/op_603 / cpp/op_495 -- **core difference**
  - c/op_603 / cpp/op_531 -- **core difference**
  - c/op_603 / cpp/op_567 -- **core difference**
  - c/op_603 / cpp/op_603 -- **core difference**
  - c/op_603 / cpp/op_639 -- **core difference**
  - c/op_603 / cpp/op_675 -- **core difference**
  - c/op_603 / cpp/op_999 -- **core difference**
  - c/op_639 / cpp/op_135 -- **core difference**
  - c/op_639 / cpp/op_171 -- **core difference**
  - c/op_639 / cpp/op_207 -- **core difference**
  - c/op_639 / cpp/op_243 -- **core difference**
  - c/op_639 / cpp/op_495 -- **core difference**
  - c/op_639 / cpp/op_531 -- **core difference**
  - c/op_639 / cpp/op_567 -- **core difference**
  - c/op_639 / cpp/op_603 -- **core difference**
  - c/op_639 / cpp/op_639 -- **core difference**
  - c/op_639 / cpp/op_675 -- **core difference**
  - c/op_639 / cpp/op_999 -- **core difference**
  - c/op_675 / cpp/op_135 -- **core difference**
  - c/op_675 / cpp/op_171 -- **core difference**
  - c/op_675 / cpp/op_207 -- **core difference**
  - c/op_675 / cpp/op_243 -- **core difference**
  - c/op_675 / cpp/op_495 -- **core difference**
  - c/op_675 / cpp/op_531 -- **core difference**
  - c/op_675 / cpp/op_567 -- **core difference**
  - c/op_675 / cpp/op_603 -- **core difference**
  - c/op_675 / cpp/op_639 -- **core difference**
  - c/op_675 / cpp/op_675 -- **core difference**
  - c/op_675 / cpp/op_999 -- **core difference**

### shared-core group F32toF64(ex32@0(in1:256)) · (bool,f32)

- ground: connection
- languages: c, cpp
- members: c `||` (bool,f32, 0 modes); c `&&` (bool,f32, 0 modes); c `>` (bool,f32, 0 modes); c `>=` (bool,f32, 0 modes); c `<=` (bool,f32, 0 modes); c `<` (bool,f32, 0 modes); cpp `||` (bool,f32, 0 modes); cpp `&&` (bool,f32, 0 modes); cpp `>` (bool,f32, 0 modes); cpp `>=` (bool,f32, 0 modes); cpp `<=` (bool,f32, 0 modes); cpp `<` (bool,f32, 0 modes); cpp `or` (bool,f32, 0 modes); cpp `and` (bool,f32, 0 modes)

  - c/op_315 / cpp/op_315 -- **core difference**
  - c/op_315 / cpp/op_351 -- **core difference**
  - c/op_315 / cpp/op_567 -- **core difference**
  - c/op_315 / cpp/op_603 -- **core difference**
  - c/op_315 / cpp/op_639 -- **core difference**
  - c/op_315 / cpp/op_675 -- **core difference**
  - c/op_315 / cpp/op_819 -- **core difference**
  - c/op_315 / cpp/op_855 -- **core difference**
  - c/op_351 / cpp/op_315 -- **core difference**
  - c/op_351 / cpp/op_351 -- **core difference**
  - c/op_351 / cpp/op_567 -- **core difference**
  - c/op_351 / cpp/op_603 -- **core difference**
  - c/op_351 / cpp/op_639 -- **core difference**
  - c/op_351 / cpp/op_675 -- **core difference**
  - c/op_351 / cpp/op_819 -- **core difference**
  - c/op_351 / cpp/op_855 -- **core difference**
  - c/op_567 / cpp/op_315 -- **core difference**
  - c/op_567 / cpp/op_351 -- **core difference**
  - c/op_567 / cpp/op_567 -- **core difference**
  - c/op_567 / cpp/op_603 -- **core difference**
  - c/op_567 / cpp/op_639 -- **core difference**
  - c/op_567 / cpp/op_675 -- **core difference**
  - c/op_567 / cpp/op_819 -- **core difference**
  - c/op_567 / cpp/op_855 -- **core difference**
  - c/op_603 / cpp/op_315 -- **core difference**
  - c/op_603 / cpp/op_351 -- **core difference**
  - c/op_603 / cpp/op_567 -- **core difference**
  - c/op_603 / cpp/op_603 -- **core difference**
  - c/op_603 / cpp/op_639 -- **core difference**
  - c/op_603 / cpp/op_675 -- **core difference**
  - c/op_603 / cpp/op_819 -- **core difference**
  - c/op_603 / cpp/op_855 -- **core difference**
  - c/op_639 / cpp/op_315 -- **core difference**
  - c/op_639 / cpp/op_351 -- **core difference**
  - c/op_639 / cpp/op_567 -- **core difference**
  - c/op_639 / cpp/op_603 -- **core difference**
  - c/op_639 / cpp/op_639 -- **core difference**
  - c/op_639 / cpp/op_675 -- **core difference**
  - c/op_639 / cpp/op_819 -- **core difference**
  - c/op_639 / cpp/op_855 -- **core difference**
  - c/op_675 / cpp/op_315 -- **core difference**
  - c/op_675 / cpp/op_351 -- **core difference**
  - c/op_675 / cpp/op_567 -- **core difference**
  - c/op_675 / cpp/op_603 -- **core difference**
  - c/op_675 / cpp/op_639 -- **core difference**
  - c/op_675 / cpp/op_675 -- **core difference**
  - c/op_675 / cpp/op_819 -- **core difference**
  - c/op_675 / cpp/op_855 -- **core difference**

### shared-core group And8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64)))),ex8@0(in0:64)) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `&&` (bool,f64, 0 modes); cpp `&&` (bool,f64, 0 modes); cpp `and` (bool,f64, 0 modes)

  - c/op_352 / cpp/op_352 -- **core difference**
  - c/op_352 / cpp/op_856 -- **core difference**

### shared-core group Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64)))),ex8@0(in0:64)) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `||` (bool,f64, 0 modes); cpp `||` (bool,f64, 0 modes); cpp `or` (bool,f64, 0 modes)

  - c/op_316 / cpp/op_316 -- **core difference**
  - c/op_316 / cpp/op_820 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64)))) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `||` (bool,f64, 0 modes); c `&&` (bool,f64, 0 modes); cpp `||` (bool,f64, 0 modes); cpp `&&` (bool,f64, 0 modes); cpp `or` (bool,f64, 0 modes); cpp `and` (bool,f64, 0 modes)

  - c/op_316 / cpp/op_316 -- **core difference**
  - c/op_316 / cpp/op_352 -- **core difference**
  - c/op_316 / cpp/op_820 -- **core difference**
  - c/op_316 / cpp/op_856 -- **core difference**
  - c/op_352 / cpp/op_316 -- **core difference**
  - c/op_352 / cpp/op_352 -- **core difference**
  - c/op_352 / cpp/op_820 -- **core difference**
  - c/op_352 / cpp/op_856 -- **core difference**

### shared-core group ins@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))),XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256)))) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `!=` (bool,f64, 0 modes); cpp `not_eq` (bool,f64, 0 modes); cpp `!=` (bool,f64, 0 modes)

  - c/op_532 / cpp/op_1000 -- **total equality**
  - c/op_532 / cpp/op_532 -- **total equality**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))),CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256)))))) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `==` (bool,f64, 0 modes); cpp `==` (bool,f64, 0 modes)

  - c/op_496 / cpp/op_496 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex64@0(in1:256)))),0:64,u1:64))) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `>` (bool,f64, 0 modes); cpp `>` (bool,f64, 0 modes)

  - c/op_568 / cpp/op_568 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex64@0(in1:256)))),0:64,u1:64))) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `>=` (bool,f64, 0 modes); cpp `>=` (bool,f64, 0 modes)

  - c/op_604 / cpp/op_604 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))))))),0:64,u1:64))) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `<=` (bool,f64, 0 modes); cpp `<=` (bool,f64, 0 modes)

  - c/op_640 / cpp/op_640 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))))))),0:64,u1:64))) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `<` (bool,f64, 0 modes); cpp `<` (bool,f64, 0 modes)

  - c/op_676 / cpp/op_676 -- **core difference**

### shared-core group ins@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))),Sub64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256))) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `-` (bool,f64, 0 modes); cpp `-` (bool,f64, 0 modes)

  - c/op_172 / cpp/op_172 -- **total equality**

### shared-core group ins@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))),Div64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256))) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `/` (bool,f64, 0 modes); cpp `/` (bool,f64, 0 modes)

  - c/op_244 / cpp/op_244 -- **total equality**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex64@0(in1:256)))) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `>` (bool,f64, 0 modes); c `>=` (bool,f64, 0 modes); cpp `>` (bool,f64, 0 modes); cpp `>=` (bool,f64, 0 modes)

  - c/op_568 / cpp/op_568 -- **core difference**
  - c/op_568 / cpp/op_604 -- **core difference**
  - c/op_604 / cpp/op_568 -- **core difference**
  - c/op_604 / cpp/op_604 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))))))) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `<=` (bool,f64, 0 modes); c `<` (bool,f64, 0 modes); cpp `<=` (bool,f64, 0 modes); cpp `<` (bool,f64, 0 modes)

  - c/op_640 / cpp/op_640 -- **core difference**
  - c/op_640 / cpp/op_676 -- **core difference**
  - c/op_676 / cpp/op_640 -- **core difference**
  - c/op_676 / cpp/op_676 -- **core difference**

### shared-core group CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256)) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `==` (bool,f64, 0 modes); c `!=` (bool,f64, 0 modes); cpp `not_eq` (bool,f64, 0 modes); cpp `==` (bool,f64, 0 modes); cpp `!=` (bool,f64, 0 modes)

  - c/op_496 / cpp/op_1000 -- **core difference**
  - c/op_496 / cpp/op_496 -- **total equality**
  - c/op_496 / cpp/op_532 -- **core difference**
  - c/op_532 / cpp/op_1000 -- **total equality**
  - c/op_532 / cpp/op_496 -- **core difference**
  - c/op_532 / cpp/op_532 -- **total equality**

### shared-core group Add64F0x2(ex128@0(in1:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))))) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `+` (bool,f64, 0 modes); cpp `+` (bool,f64, 0 modes)

  - c/op_136 / cpp/op_136 -- **total equality**

### shared-core group Mul64F0x2(ex128@0(in1:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))))) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `*` (bool,f64, 0 modes); cpp `*` (bool,f64, 0 modes)

  - c/op_208 / cpp/op_208 -- **total equality**

### shared-core group ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `+` (bool,f64, 0 modes); c `-` (bool,f64, 0 modes); c `*` (bool,f64, 0 modes); c `/` (bool,f64, 0 modes); c `==` (bool,f64, 0 modes); c `!=` (bool,f64, 0 modes); cpp `not_eq` (bool,f64, 0 modes); cpp `+` (bool,f64, 0 modes); cpp `-` (bool,f64, 0 modes); cpp `*` (bool,f64, 0 modes); cpp `/` (bool,f64, 0 modes); cpp `==` (bool,f64, 0 modes); cpp `!=` (bool,f64, 0 modes)

  - c/op_136 / cpp/op_1000 -- **core difference**
  - c/op_136 / cpp/op_136 -- **total equality**
  - c/op_136 / cpp/op_172 -- **core difference**
  - c/op_136 / cpp/op_208 -- **core difference**
  - c/op_136 / cpp/op_244 -- **core difference**
  - c/op_136 / cpp/op_496 -- **core difference**
  - c/op_136 / cpp/op_532 -- **core difference**
  - c/op_172 / cpp/op_1000 -- **core difference**
  - c/op_172 / cpp/op_136 -- **core difference**
  - c/op_172 / cpp/op_172 -- **total equality**
  - c/op_172 / cpp/op_208 -- **core difference**
  - c/op_172 / cpp/op_244 -- **core difference**
  - c/op_172 / cpp/op_496 -- **core difference**
  - c/op_172 / cpp/op_532 -- **core difference**
  - c/op_208 / cpp/op_1000 -- **core difference**
  - c/op_208 / cpp/op_136 -- **core difference**
  - c/op_208 / cpp/op_172 -- **core difference**
  - c/op_208 / cpp/op_208 -- **total equality**
  - c/op_208 / cpp/op_244 -- **core difference**
  - c/op_208 / cpp/op_496 -- **core difference**
  - c/op_208 / cpp/op_532 -- **core difference**
  - c/op_244 / cpp/op_1000 -- **core difference**
  - c/op_244 / cpp/op_136 -- **core difference**
  - c/op_244 / cpp/op_172 -- **core difference**
  - c/op_244 / cpp/op_208 -- **core difference**
  - c/op_244 / cpp/op_244 -- **total equality**
  - c/op_244 / cpp/op_496 -- **core difference**
  - c/op_244 / cpp/op_532 -- **core difference**
  - c/op_496 / cpp/op_1000 -- **core difference**
  - c/op_496 / cpp/op_136 -- **core difference**
  - c/op_496 / cpp/op_172 -- **core difference**
  - c/op_496 / cpp/op_208 -- **core difference**
  - c/op_496 / cpp/op_244 -- **core difference**
  - c/op_496 / cpp/op_496 -- **total equality**
  - c/op_496 / cpp/op_532 -- **core difference**
  - c/op_532 / cpp/op_1000 -- **total equality**
  - c/op_532 / cpp/op_136 -- **core difference**
  - c/op_532 / cpp/op_172 -- **core difference**
  - c/op_532 / cpp/op_208 -- **core difference**
  - c/op_532 / cpp/op_244 -- **core difference**
  - c/op_532 / cpp/op_496 -- **core difference**
  - c/op_532 / cpp/op_532 -- **total equality**

### shared-core group ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `>` (bool,f64, 0 modes); c `>=` (bool,f64, 0 modes); c `<=` (bool,f64, 0 modes); c `<` (bool,f64, 0 modes); cpp `>` (bool,f64, 0 modes); cpp `>=` (bool,f64, 0 modes); cpp `<=` (bool,f64, 0 modes); cpp `<` (bool,f64, 0 modes)

  - c/op_568 / cpp/op_568 -- **core difference**
  - c/op_568 / cpp/op_604 -- **core difference**
  - c/op_568 / cpp/op_640 -- **core difference**
  - c/op_568 / cpp/op_676 -- **core difference**
  - c/op_604 / cpp/op_568 -- **core difference**
  - c/op_604 / cpp/op_604 -- **core difference**
  - c/op_604 / cpp/op_640 -- **core difference**
  - c/op_604 / cpp/op_676 -- **core difference**
  - c/op_640 / cpp/op_568 -- **core difference**
  - c/op_640 / cpp/op_604 -- **core difference**
  - c/op_640 / cpp/op_640 -- **core difference**
  - c/op_640 / cpp/op_676 -- **core difference**
  - c/op_676 / cpp/op_568 -- **core difference**
  - c/op_676 / cpp/op_604 -- **core difference**
  - c/op_676 / cpp/op_640 -- **core difference**
  - c/op_676 / cpp/op_676 -- **core difference**

### shared-core group ins@0(u0:256,I32StoF64(ex32@0(in0:64))) · (bool,f64)

- ground: connection
- languages: c, cpp
- members: c `+` (bool,f64, 0 modes); c `-` (bool,f64, 0 modes); c `*` (bool,f64, 0 modes); c `/` (bool,f64, 0 modes); c `==` (bool,f64, 0 modes); c `!=` (bool,f64, 0 modes); c `>` (bool,f64, 0 modes); c `>=` (bool,f64, 0 modes); c `<=` (bool,f64, 0 modes); c `<` (bool,f64, 0 modes); cpp `not_eq` (bool,f64, 0 modes); cpp `+` (bool,f64, 0 modes); cpp `-` (bool,f64, 0 modes); cpp `*` (bool,f64, 0 modes); cpp `/` (bool,f64, 0 modes); cpp `==` (bool,f64, 0 modes); cpp `!=` (bool,f64, 0 modes); cpp `>` (bool,f64, 0 modes); cpp `>=` (bool,f64, 0 modes); cpp `<=` (bool,f64, 0 modes); cpp `<` (bool,f64, 0 modes)

  - c/op_136 / cpp/op_1000 -- **core difference**
  - c/op_136 / cpp/op_136 -- **total equality**
  - c/op_136 / cpp/op_172 -- **core difference**
  - c/op_136 / cpp/op_208 -- **core difference**
  - c/op_136 / cpp/op_244 -- **core difference**
  - c/op_136 / cpp/op_496 -- **core difference**
  - c/op_136 / cpp/op_532 -- **core difference**
  - c/op_136 / cpp/op_568 -- **core difference**
  - c/op_136 / cpp/op_604 -- **core difference**
  - c/op_136 / cpp/op_640 -- **core difference**
  - c/op_136 / cpp/op_676 -- **core difference**
  - c/op_172 / cpp/op_1000 -- **core difference**
  - c/op_172 / cpp/op_136 -- **core difference**
  - c/op_172 / cpp/op_172 -- **total equality**
  - c/op_172 / cpp/op_208 -- **core difference**
  - c/op_172 / cpp/op_244 -- **core difference**
  - c/op_172 / cpp/op_496 -- **core difference**
  - c/op_172 / cpp/op_532 -- **core difference**
  - c/op_172 / cpp/op_568 -- **core difference**
  - c/op_172 / cpp/op_604 -- **core difference**
  - c/op_172 / cpp/op_640 -- **core difference**
  - c/op_172 / cpp/op_676 -- **core difference**
  - c/op_208 / cpp/op_1000 -- **core difference**
  - c/op_208 / cpp/op_136 -- **core difference**
  - c/op_208 / cpp/op_172 -- **core difference**
  - c/op_208 / cpp/op_208 -- **total equality**
  - c/op_208 / cpp/op_244 -- **core difference**
  - c/op_208 / cpp/op_496 -- **core difference**
  - c/op_208 / cpp/op_532 -- **core difference**
  - c/op_208 / cpp/op_568 -- **core difference**
  - c/op_208 / cpp/op_604 -- **core difference**
  - c/op_208 / cpp/op_640 -- **core difference**
  - c/op_208 / cpp/op_676 -- **core difference**
  - c/op_244 / cpp/op_1000 -- **core difference**
  - c/op_244 / cpp/op_136 -- **core difference**
  - c/op_244 / cpp/op_172 -- **core difference**
  - c/op_244 / cpp/op_208 -- **core difference**
  - c/op_244 / cpp/op_244 -- **total equality**
  - c/op_244 / cpp/op_496 -- **core difference**
  - c/op_244 / cpp/op_532 -- **core difference**
  - c/op_244 / cpp/op_568 -- **core difference**
  - c/op_244 / cpp/op_604 -- **core difference**
  - c/op_244 / cpp/op_640 -- **core difference**
  - c/op_244 / cpp/op_676 -- **core difference**
  - c/op_496 / cpp/op_1000 -- **core difference**
  - c/op_496 / cpp/op_136 -- **core difference**
  - c/op_496 / cpp/op_172 -- **core difference**
  - c/op_496 / cpp/op_208 -- **core difference**
  - c/op_496 / cpp/op_244 -- **core difference**
  - c/op_496 / cpp/op_496 -- **total equality**
  - c/op_496 / cpp/op_532 -- **core difference**
  - c/op_496 / cpp/op_568 -- **core difference**
  - c/op_496 / cpp/op_604 -- **core difference**
  - c/op_496 / cpp/op_640 -- **core difference**
  - c/op_496 / cpp/op_676 -- **core difference**
  - c/op_532 / cpp/op_1000 -- **total equality**
  - c/op_532 / cpp/op_136 -- **core difference**
  - c/op_532 / cpp/op_172 -- **core difference**
  - c/op_532 / cpp/op_208 -- **core difference**
  - c/op_532 / cpp/op_244 -- **core difference**
  - c/op_532 / cpp/op_496 -- **core difference**
  - c/op_532 / cpp/op_532 -- **total equality**
  - c/op_532 / cpp/op_568 -- **core difference**
  - c/op_532 / cpp/op_604 -- **core difference**
  - c/op_532 / cpp/op_640 -- **core difference**
  - c/op_532 / cpp/op_676 -- **core difference**
  - c/op_568 / cpp/op_1000 -- **core difference**
  - c/op_568 / cpp/op_136 -- **core difference**
  - c/op_568 / cpp/op_172 -- **core difference**
  - c/op_568 / cpp/op_208 -- **core difference**
  - c/op_568 / cpp/op_244 -- **core difference**
  - c/op_568 / cpp/op_496 -- **core difference**
  - c/op_568 / cpp/op_532 -- **core difference**
  - c/op_568 / cpp/op_568 -- **core difference**
  - c/op_568 / cpp/op_604 -- **core difference**
  - c/op_568 / cpp/op_640 -- **core difference**
  - c/op_568 / cpp/op_676 -- **core difference**
  - c/op_604 / cpp/op_1000 -- **core difference**
  - c/op_604 / cpp/op_136 -- **core difference**
  - c/op_604 / cpp/op_172 -- **core difference**
  - c/op_604 / cpp/op_208 -- **core difference**
  - c/op_604 / cpp/op_244 -- **core difference**
  - c/op_604 / cpp/op_496 -- **core difference**
  - c/op_604 / cpp/op_532 -- **core difference**
  - c/op_604 / cpp/op_568 -- **core difference**
  - c/op_604 / cpp/op_604 -- **core difference**
  - c/op_604 / cpp/op_640 -- **core difference**
  - c/op_604 / cpp/op_676 -- **core difference**
  - c/op_640 / cpp/op_1000 -- **core difference**
  - c/op_640 / cpp/op_136 -- **core difference**
  - c/op_640 / cpp/op_172 -- **core difference**
  - c/op_640 / cpp/op_208 -- **core difference**
  - c/op_640 / cpp/op_244 -- **core difference**
  - c/op_640 / cpp/op_496 -- **core difference**
  - c/op_640 / cpp/op_532 -- **core difference**
  - c/op_640 / cpp/op_568 -- **core difference**
  - c/op_640 / cpp/op_604 -- **core difference**
  - c/op_640 / cpp/op_640 -- **core difference**
  - c/op_640 / cpp/op_676 -- **core difference**
  - c/op_676 / cpp/op_1000 -- **core difference**
  - c/op_676 / cpp/op_136 -- **core difference**
  - c/op_676 / cpp/op_172 -- **core difference**
  - c/op_676 / cpp/op_208 -- **core difference**
  - c/op_676 / cpp/op_244 -- **core difference**
  - c/op_676 / cpp/op_496 -- **core difference**
  - c/op_676 / cpp/op_532 -- **core difference**
  - c/op_676 / cpp/op_568 -- **core difference**
  - c/op_676 / cpp/op_604 -- **core difference**
  - c/op_676 / cpp/op_640 -- **core difference**
  - c/op_676 / cpp/op_676 -- **core difference**

### shared-core group zx64(ite(ex1@0(amd64g_calculate_condition(4:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64)),ex32@0(in0:64),ex32@0(in1:64))) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `*` (bool,i32, 0 modes); cpp `*` (bool,i32, 0 modes)

  - c/op_204 / cpp/op_204 -- **total equality**

### shared-core group And8(ex8@0(in0:64),zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64)))) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `&&` (bool,i32, 0 modes); cpp `&&` (bool,i32, 0 modes); cpp `and` (bool,i32, 0 modes)

  - c/op_348 / cpp/op_348 -- **core difference**
  - c/op_348 / cpp/op_852 -- **core difference**

### shared-core group Or8(ex8@0(in0:64),zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64)))) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `||` (bool,i32, 0 modes); cpp `||` (bool,i32, 0 modes); cpp `or` (bool,i32, 0 modes)

  - c/op_312 / cpp/op_312 -- **core difference**
  - c/op_312 / cpp/op_816 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(12:64,7:64,zx64(ex32@0(in1:64)),zx64(ex32@0(in0:64)),u0:64))) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `>` (bool,i32, 0 modes); cpp `>` (bool,i32, 0 modes)

  - c/op_564 / cpp/op_564 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(14:64,7:64,zx64(ex32@0(in1:64)),zx64(ex32@0(in0:64)),u0:64))) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `>=` (bool,i32, 0 modes); cpp `>=` (bool,i32, 0 modes)

  - c/op_600 / cpp/op_600 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(13:64,7:64,zx64(ex32@0(in1:64)),zx64(ex32@0(in0:64)),u0:64))) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `<=` (bool,i32, 0 modes); cpp `<=` (bool,i32, 0 modes)

  - c/op_636 / cpp/op_636 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(15:64,7:64,zx64(ex32@0(in1:64)),zx64(ex32@0(in0:64)),u0:64))) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `<` (bool,i32, 0 modes); cpp `<` (bool,i32, 0 modes)

  - c/op_672 / cpp/op_672 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(4:64,7:64,zx64(ex32@0(in1:64)),zx64(ex32@0(in0:64)),u0:64))) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `==` (bool,i32, 0 modes); cpp `==` (bool,i32, 0 modes)

  - c/op_492 / cpp/op_492 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,7:64,zx64(ex32@0(in1:64)),zx64(ex32@0(in0:64)),u0:64))) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `!=` (bool,i32, 0 modes); cpp `!=` (bool,i32, 0 modes); cpp `not_eq` (bool,i32, 0 modes)

  - c/op_528 / cpp/op_528 -- **core difference**
  - c/op_528 / cpp/op_996 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64))) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `||` (bool,i32, 0 modes); c `&&` (bool,i32, 0 modes); cpp `||` (bool,i32, 0 modes); cpp `&&` (bool,i32, 0 modes); cpp `or` (bool,i32, 0 modes); cpp `and` (bool,i32, 0 modes)

  - c/op_312 / cpp/op_312 -- **core difference**
  - c/op_312 / cpp/op_348 -- **core difference**
  - c/op_312 / cpp/op_816 -- **core difference**
  - c/op_312 / cpp/op_852 -- **core difference**
  - c/op_348 / cpp/op_312 -- **core difference**
  - c/op_348 / cpp/op_348 -- **core difference**
  - c/op_348 / cpp/op_816 -- **core difference**
  - c/op_348 / cpp/op_852 -- **core difference**

### shared-core group zx64(ex32@32(DivModS64to32(32HLto64(0:32,ex32@0(in0:64)),ex32@0(in1:64)))) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `/` (bool,i32, 0 modes); c `%` (bool,i32, 0 modes); cpp `/` (bool,i32, 0 modes); cpp `%` (bool,i32, 0 modes)

  - c/op_240 / cpp/op_240 -- **total equality**
  - c/op_240 / cpp/op_276 -- **core difference**
  - c/op_276 / cpp/op_240 -- **core difference**
  - c/op_276 / cpp/op_276 -- **total equality**

### shared-core group zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `<<` (bool,i32, 0 modes); cpp `<<` (bool,i32, 0 modes)

  - c/op_708 / cpp/op_708 -- **total equality**

### shared-core group zx64(ex32@0(Shr64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `>>` (bool,i32, 0 modes); cpp `>>` (bool,i32, 0 modes)

  - c/op_744 / cpp/op_744 -- **total equality**

### shared-core group zx64(Add32(ex32@0(in0:64),ex32@0(in1:64))) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `+` (bool,i32, 0 modes); cpp `+` (bool,i32, 0 modes)

  - c/op_132 / cpp/op_132 -- **total equality**

### shared-core group zx64(Sub32(ex32@0(in0:64),ex32@0(in1:64))) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `-` (bool,i32, 0 modes); cpp `-` (bool,i32, 0 modes)

  - c/op_168 / cpp/op_168 -- **total equality**

### shared-core group zx64(Xor32(ex32@0(in0:64),ex32@0(in1:64))) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `^` (bool,i32, 0 modes); cpp `^` (bool,i32, 0 modes); cpp `xor` (bool,i32, 0 modes)

  - c/op_420 / cpp/op_420 -- **total equality**
  - c/op_420 / cpp/op_924 -- **total equality**

### shared-core group zx64(And32(ex32@0(in0:64),ex32@0(in1:64))) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `&` (bool,i32, 0 modes); cpp `&` (bool,i32, 0 modes); cpp `bitand` (bool,i32, 0 modes)

  - c/op_456 / cpp/op_456 -- **total equality**
  - c/op_456 / cpp/op_960 -- **total equality**

### shared-core group zx64(Or32(ex32@0(in0:64),ex32@0(in1:64))) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `|` (bool,i32, 0 modes); cpp `|` (bool,i32, 0 modes); cpp `bitor` (bool,i32, 0 modes)

  - c/op_384 / cpp/op_384 -- **total equality**
  - c/op_384 / cpp/op_888 -- **total equality**

### shared-core group And8(31:8,ex8@0(in1:64)) · (bool,i32)

- ground: connection
- languages: c, cpp
- members: c `<<` (bool,i32, 0 modes); c `>>` (bool,i32, 0 modes); cpp `<<` (bool,i32, 0 modes); cpp `>>` (bool,i32, 0 modes)

  - c/op_708 / cpp/op_708 -- **total equality**
  - c/op_708 / cpp/op_744 -- **core difference**
  - c/op_744 / cpp/op_708 -- **core difference**
  - c/op_744 / cpp/op_744 -- **total equality**

### shared-core group ite(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64)),in1:64,0:64) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `*` (bool,i64, 0 modes); cpp `*` (bool,i64, 0 modes)

  - c/op_205 / cpp/op_205 -- **total equality**

### shared-core group And8(ex8@0(in0:64),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `&&` (bool,i64, 0 modes); cpp `&&` (bool,i64, 0 modes); cpp `and` (bool,i64, 0 modes)

  - c/op_349 / cpp/op_349 -- **core difference**
  - c/op_349 / cpp/op_853 -- **core difference**

### shared-core group Or8(ex8@0(in0:64),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `||` (bool,i64, 0 modes); cpp `||` (bool,i64, 0 modes); cpp `or` (bool,i64, 0 modes)

  - c/op_313 / cpp/op_313 -- **core difference**
  - c/op_313 / cpp/op_817 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(12:64,8:64,in1:64,zx64(ex32@0(in0:64)),u0:64))) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `>` (bool,i64, 1 modes); cpp `>` (bool,i64, 1 modes)

  - c/op_565 / cpp/op_565 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(14:64,8:64,in1:64,zx64(ex32@0(in0:64)),u0:64))) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `>=` (bool,i64, 1 modes); cpp `>=` (bool,i64, 1 modes)

  - c/op_601 / cpp/op_601 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(13:64,8:64,in1:64,zx64(ex32@0(in0:64)),u0:64))) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `<=` (bool,i64, 1 modes); cpp `<=` (bool,i64, 1 modes)

  - c/op_637 / cpp/op_637 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(15:64,8:64,in1:64,zx64(ex32@0(in0:64)),u0:64))) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `<` (bool,i64, 1 modes); cpp `<` (bool,i64, 1 modes)

  - c/op_673 / cpp/op_673 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(4:64,8:64,in1:64,zx64(ex32@0(in0:64)),u0:64))) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `==` (bool,i64, 1 modes); cpp `==` (bool,i64, 1 modes)

  - c/op_493 / cpp/op_493 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,8:64,in1:64,zx64(ex32@0(in0:64)),u0:64))) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `!=` (bool,i64, 2 modes); cpp `!=` (bool,i64, 1 modes); cpp `not_eq` (bool,i64, 1 modes)

  - c/op_529 / cpp/op_529 -- **core difference**
  - c/op_529 / cpp/op_997 -- **core difference**

### shared-core group ex64@64(DivModS128to64(64HLto128(0:64,zx64(ex32@0(in0:64))),in1:64)) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `/` (bool,i64, 0 modes); c `%` (bool,i64, 0 modes); cpp `/` (bool,i64, 0 modes); cpp `%` (bool,i64, 0 modes)

  - c/op_241 / cpp/op_241 -- **total equality**
  - c/op_241 / cpp/op_277 -- **core difference**
  - c/op_277 / cpp/op_241 -- **core difference**
  - c/op_277 / cpp/op_277 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64))) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `||` (bool,i64, 0 modes); c `&&` (bool,i64, 0 modes); cpp `||` (bool,i64, 0 modes); cpp `&&` (bool,i64, 0 modes); cpp `or` (bool,i64, 0 modes); cpp `and` (bool,i64, 0 modes)

  - c/op_313 / cpp/op_313 -- **core difference**
  - c/op_313 / cpp/op_349 -- **core difference**
  - c/op_313 / cpp/op_817 -- **core difference**
  - c/op_313 / cpp/op_853 -- **core difference**
  - c/op_349 / cpp/op_313 -- **core difference**
  - c/op_349 / cpp/op_349 -- **core difference**
  - c/op_349 / cpp/op_817 -- **core difference**
  - c/op_349 / cpp/op_853 -- **core difference**

### shared-core group zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `<<` (bool,i64, 0 modes); cpp `<<` (bool,i64, 0 modes)

  - c/op_709 / cpp/op_709 -- **total equality**

### shared-core group zx64(ex32@0(Shr64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `>>` (bool,i64, 0 modes); cpp `>>` (bool,i64, 0 modes)

  - c/op_745 / cpp/op_745 -- **total equality**

### shared-core group zx64(And32(ex32@0(in0:64),ex32@0(in1:64))) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `&` (bool,i64, 0 modes); cpp `&` (bool,i64, 0 modes); cpp `bitand` (bool,i64, 0 modes)

  - c/op_457 / cpp/op_457 -- **total equality**
  - c/op_457 / cpp/op_961 -- **total equality**

### shared-core group Add64(in1:64,zx64(ex32@0(in0:64))) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `+` (bool,i64, 0 modes); cpp `+` (bool,i64, 0 modes)

  - c/op_133 / cpp/op_133 -- **total equality**

### shared-core group Sub64(zx64(ex32@0(in0:64)),in1:64) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `-` (bool,i64, 0 modes); cpp `-` (bool,i64, 0 modes)

  - c/op_169 / cpp/op_169 -- **total equality**

### shared-core group Xor64(in1:64,zx64(ex32@0(in0:64))) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `^` (bool,i64, 0 modes); cpp `^` (bool,i64, 0 modes); cpp `xor` (bool,i64, 0 modes)

  - c/op_421 / cpp/op_421 -- **total equality**
  - c/op_421 / cpp/op_925 -- **total equality**

### shared-core group Or64(in1:64,zx64(ex32@0(in0:64))) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `|` (bool,i64, 0 modes); cpp `|` (bool,i64, 0 modes); cpp `bitor` (bool,i64, 0 modes)

  - c/op_385 / cpp/op_385 -- **total equality**
  - c/op_385 / cpp/op_889 -- **total equality**

### shared-core group And8(31:8,ex8@0(in1:64)) · (bool,i64)

- ground: connection
- languages: c, cpp
- members: c `<<` (bool,i64, 0 modes); c `>>` (bool,i64, 0 modes); cpp `<<` (bool,i64, 0 modes); cpp `>>` (bool,i64, 0 modes)

  - c/op_709 / cpp/op_709 -- **total equality**
  - c/op_709 / cpp/op_745 -- **core difference**
  - c/op_745 / cpp/op_709 -- **core difference**
  - c/op_745 / cpp/op_745 -- **total equality**

### shared-core group ite(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64)),in1:64,0:64) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `*` (bool,u64, 0 modes); cpp `*` (bool,u64, 0 modes)

  - c/op_206 / cpp/op_206 -- **total equality**

### shared-core group And8(ex8@0(in0:64),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `&&` (bool,u64, 0 modes); cpp `&&` (bool,u64, 0 modes); cpp `and` (bool,u64, 0 modes)

  - c/op_350 / cpp/op_350 -- **core difference**
  - c/op_350 / cpp/op_854 -- **core difference**

### shared-core group And8(ex8@0(in0:64),zx8(ex1@0(amd64g_calculate_condition(4:64,20:64,in1:64,0:64,u0:64)))) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `>` (bool,u64, 0 modes); cpp `>` (bool,u64, 0 modes)

  - c/op_566 / cpp/op_566 -- **core difference**

### shared-core group Or8(ex8@0(in0:64),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `||` (bool,u64, 0 modes); cpp `||` (bool,u64, 0 modes); cpp `or` (bool,u64, 0 modes)

  - c/op_314 / cpp/op_314 -- **core difference**
  - c/op_314 / cpp/op_818 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(4:64,8:64,in1:64,zx64(ex32@0(in0:64)),u0:64))) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `==` (bool,u64, 1 modes); cpp `==` (bool,u64, 1 modes)

  - c/op_494 / cpp/op_494 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,8:64,in1:64,zx64(ex32@0(in0:64)),u0:64))) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `!=` (bool,u64, 2 modes); cpp `!=` (bool,u64, 1 modes); cpp `not_eq` (bool,u64, 1 modes)

  - c/op_530 / cpp/op_530 -- **core difference**
  - c/op_530 / cpp/op_998 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(6:64,8:64,in1:64,zx64(ex32@0(in0:64)),u0:64))) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `>=` (bool,u64, 1 modes); cpp `>=` (bool,u64, 1 modes)

  - c/op_602 / cpp/op_602 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,8:64,in1:64,zx64(ex32@0(in0:64)),u0:64))) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `<=` (bool,u64, 1 modes); cpp `<=` (bool,u64, 1 modes)

  - c/op_638 / cpp/op_638 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,8:64,in1:64,zx64(ex32@0(in0:64)),u0:64))) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `<` (bool,u64, 1 modes); cpp `<` (bool,u64, 1 modes)

  - c/op_674 / cpp/op_674 -- **core difference**

### shared-core group ex64@64(DivModU128to64(64HLto128(0:64,zx64(ex32@0(in0:64))),in1:64)) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `/` (bool,u64, 0 modes); c `%` (bool,u64, 0 modes); cpp `/` (bool,u64, 0 modes); cpp `%` (bool,u64, 0 modes)

  - c/op_242 / cpp/op_242 -- **total equality**
  - c/op_242 / cpp/op_278 -- **core difference**
  - c/op_278 / cpp/op_242 -- **core difference**
  - c/op_278 / cpp/op_278 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64))) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `||` (bool,u64, 0 modes); c `&&` (bool,u64, 0 modes); cpp `||` (bool,u64, 0 modes); cpp `&&` (bool,u64, 0 modes); cpp `or` (bool,u64, 0 modes); cpp `and` (bool,u64, 0 modes)

  - c/op_314 / cpp/op_314 -- **core difference**
  - c/op_314 / cpp/op_350 -- **core difference**
  - c/op_314 / cpp/op_818 -- **core difference**
  - c/op_314 / cpp/op_854 -- **core difference**
  - c/op_350 / cpp/op_314 -- **core difference**
  - c/op_350 / cpp/op_350 -- **core difference**
  - c/op_350 / cpp/op_818 -- **core difference**
  - c/op_350 / cpp/op_854 -- **core difference**

### shared-core group zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `<<` (bool,u64, 0 modes); cpp `<<` (bool,u64, 0 modes)

  - c/op_710 / cpp/op_710 -- **total equality**

### shared-core group zx64(ex32@0(Shr64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `>>` (bool,u64, 0 modes); cpp `>>` (bool,u64, 0 modes)

  - c/op_746 / cpp/op_746 -- **total equality**

### shared-core group zx64(And32(ex32@0(in0:64),ex32@0(in1:64))) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `&` (bool,u64, 0 modes); cpp `&` (bool,u64, 0 modes); cpp `bitand` (bool,u64, 0 modes)

  - c/op_458 / cpp/op_458 -- **total equality**
  - c/op_458 / cpp/op_962 -- **total equality**

### shared-core group Add64(in1:64,zx64(ex32@0(in0:64))) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `+` (bool,u64, 0 modes); cpp `+` (bool,u64, 0 modes)

  - c/op_134 / cpp/op_134 -- **total equality**

### shared-core group Sub64(zx64(ex32@0(in0:64)),in1:64) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `-` (bool,u64, 0 modes); cpp `-` (bool,u64, 0 modes)

  - c/op_170 / cpp/op_170 -- **total equality**

### shared-core group Xor64(in1:64,zx64(ex32@0(in0:64))) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `^` (bool,u64, 0 modes); cpp `^` (bool,u64, 0 modes); cpp `xor` (bool,u64, 0 modes)

  - c/op_422 / cpp/op_422 -- **total equality**
  - c/op_422 / cpp/op_926 -- **total equality**

### shared-core group Or64(in1:64,zx64(ex32@0(in0:64))) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `|` (bool,u64, 0 modes); cpp `|` (bool,u64, 0 modes); cpp `bitor` (bool,u64, 0 modes)

  - c/op_386 / cpp/op_386 -- **total equality**
  - c/op_386 / cpp/op_890 -- **total equality**

### shared-core group And8(31:8,ex8@0(in1:64)) · (bool,u64)

- ground: connection
- languages: c, cpp
- members: c `<<` (bool,u64, 0 modes); c `>>` (bool,u64, 0 modes); cpp `<<` (bool,u64, 0 modes); cpp `>>` (bool,u64, 0 modes)

  - c/op_710 / cpp/op_710 -- **total equality**
  - c/op_710 / cpp/op_746 -- **core difference**
  - c/op_746 / cpp/op_710 -- **core difference**
  - c/op_746 / cpp/op_746 -- **total equality**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,0:128),CmpEQ32F0x4(0:128,ex128@0(in0:256)))))) · (f32,None)

- ground: connection
- languages: c, cpp
- members: c `!` (f32,None, 0 modes); cpp `not` (f32,None, 0 modes); cpp `!` (f32,None, 0 modes)

  - c/op_3 / cpp/op_27 -- **total equality**
  - c/op_3 / cpp/op_3 -- **total equality**

### shared-core group st32(Add64(18446744073709551612:64,SP:64))=ex32@0(in0:256) · (f32,None)

- ground: connection
- languages: c, cpp
- members: c `&` (f32,None, 0 modes); cpp `&` (f32,None, 0 modes)

  - c/op_33 / cpp/op_45 -- **total equality**

### shared-core group Add32F0x4(ex128@0(in0:256),zx128(ld32/g0(8:64))) · (f32,None)

- ground: connection
- languages: c, cpp
- members: c `++` (f32,None, 0 modes); c `--` (f32,None, 0 modes); cpp `++` (f32,None, 0 modes); cpp `--` (f32,None, 0 modes)

  - c/op_39 / cpp/op_51 -- **total equality**
  - c/op_39 / cpp/op_57 -- **total equality**
  - c/op_45 / cpp/op_51 -- **total equality**
  - c/op_45 / cpp/op_57 -- **total equality**

### shared-core group XorV128(ex128@0(in0:256),ld128/g0(7:64)) · (f32,None)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `-` (f32,None, 0 modes); cpp `-` (f32,None, 0 modes); rust `-` (f32,None, 0 modes); swift `-` (f32,None, 0 modes)

  - c/op_15 / cpp/op_15 -- **total equality**
  - c/op_15 / rust/op_3 -- **total equality**
  - c/op_15 / swift/op_15 -- **total equality**
  - cpp/op_15 / rust/op_3 -- **total equality**
  - cpp/op_15 / swift/op_15 -- **total equality**
  - rust/op_3 / swift/op_15 -- **total equality**

### shared-core group And8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64)))),ex8@0(in1:64)) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `&&` (f32,bool, 0 modes); cpp `&&` (f32,bool, 0 modes); cpp `and` (f32,bool, 0 modes)

  - c/op_341 / cpp/op_341 -- **core difference**
  - c/op_341 / cpp/op_845 -- **core difference**

### shared-core group Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64)))),ex8@0(in1:64)) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `||` (f32,bool, 0 modes); cpp `||` (f32,bool, 0 modes); cpp `or` (f32,bool, 0 modes)

  - c/op_305 / cpp/op_305 -- **core difference**
  - c/op_305 / cpp/op_809 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64)))) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `||` (f32,bool, 0 modes); c `&&` (f32,bool, 0 modes); cpp `||` (f32,bool, 0 modes); cpp `&&` (f32,bool, 0 modes); cpp `or` (f32,bool, 0 modes); cpp `and` (f32,bool, 0 modes)

  - c/op_305 / cpp/op_305 -- **core difference**
  - c/op_305 / cpp/op_341 -- **core difference**
  - c/op_305 / cpp/op_809 -- **core difference**
  - c/op_305 / cpp/op_845 -- **core difference**
  - c/op_341 / cpp/op_305 -- **core difference**
  - c/op_341 / cpp/op_341 -- **core difference**
  - c/op_341 / cpp/op_809 -- **core difference**
  - c/op_341 / cpp/op_845 -- **core difference**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64)))),CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))),ex128@0(in0:256)))))) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `==` (f32,bool, 0 modes); cpp `==` (f32,bool, 0 modes)

  - c/op_485 / cpp/op_485 -- **total equality**

### shared-core group ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64)))),XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))),ex128@0(in0:256)))) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `!=` (f32,bool, 0 modes); cpp `!=` (f32,bool, 0 modes); cpp `not_eq` (f32,bool, 0 modes)

  - c/op_521 / cpp/op_521 -- **total equality**
  - c/op_521 / cpp/op_989 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in1:64))))))),0:64,u1:64))) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `>` (f32,bool, 0 modes); cpp `>` (f32,bool, 0 modes)

  - c/op_557 / cpp/op_557 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in1:64))))))),0:64,u1:64))) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `>=` (f32,bool, 0 modes); cpp `>=` (f32,bool, 0 modes)

  - c/op_593 / cpp/op_593 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in1:64)))),F32toF64(ex32@0(in0:256))))),0:64,u1:64))) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `<=` (f32,bool, 0 modes); cpp `<=` (f32,bool, 0 modes)

  - c/op_629 / cpp/op_629 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in1:64)))),F32toF64(ex32@0(in0:256))))),0:64,u1:64))) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `<` (f32,bool, 0 modes); cpp `<` (f32,bool, 0 modes)

  - c/op_665 / cpp/op_665 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in1:64))))))) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `>` (f32,bool, 0 modes); c `>=` (f32,bool, 0 modes); cpp `>` (f32,bool, 0 modes); cpp `>=` (f32,bool, 0 modes)

  - c/op_557 / cpp/op_557 -- **core difference**
  - c/op_557 / cpp/op_593 -- **core difference**
  - c/op_593 / cpp/op_557 -- **core difference**
  - c/op_593 / cpp/op_593 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in1:64)))),F32toF64(ex32@0(in0:256))))) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `<=` (f32,bool, 0 modes); c `<` (f32,bool, 0 modes); cpp `<=` (f32,bool, 0 modes); cpp `<` (f32,bool, 0 modes)

  - c/op_629 / cpp/op_629 -- **core difference**
  - c/op_629 / cpp/op_665 -- **core difference**
  - c/op_665 / cpp/op_629 -- **core difference**
  - c/op_665 / cpp/op_665 -- **core difference**

### shared-core group CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))),ex128@0(in0:256)) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `==` (f32,bool, 0 modes); c `!=` (f32,bool, 0 modes); cpp `==` (f32,bool, 0 modes); cpp `!=` (f32,bool, 0 modes); cpp `not_eq` (f32,bool, 0 modes)

  - c/op_485 / cpp/op_485 -- **total equality**
  - c/op_485 / cpp/op_521 -- **core difference**
  - c/op_485 / cpp/op_989 -- **core difference**
  - c/op_521 / cpp/op_485 -- **core difference**
  - c/op_521 / cpp/op_521 -- **total equality**
  - c/op_521 / cpp/op_989 -- **total equality**

### shared-core group Add32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64)))))) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `+` (f32,bool, 0 modes); cpp `+` (f32,bool, 0 modes)

  - c/op_125 / cpp/op_125 -- **total equality**

### shared-core group Sub32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64)))))) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `-` (f32,bool, 0 modes); cpp `-` (f32,bool, 0 modes)

  - c/op_161 / cpp/op_161 -- **total equality**

### shared-core group Mul32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64)))))) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `*` (f32,bool, 0 modes); cpp `*` (f32,bool, 0 modes)

  - c/op_197 / cpp/op_197 -- **total equality**

### shared-core group Div32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64)))))) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `/` (f32,bool, 0 modes); cpp `/` (f32,bool, 0 modes)

  - c/op_233 / cpp/op_233 -- **total equality**

### shared-core group ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `+` (f32,bool, 0 modes); c `-` (f32,bool, 0 modes); c `*` (f32,bool, 0 modes); c `/` (f32,bool, 0 modes); c `==` (f32,bool, 0 modes); c `!=` (f32,bool, 0 modes); cpp `+` (f32,bool, 0 modes); cpp `-` (f32,bool, 0 modes); cpp `*` (f32,bool, 0 modes); cpp `/` (f32,bool, 0 modes); cpp `==` (f32,bool, 0 modes); cpp `!=` (f32,bool, 0 modes); cpp `not_eq` (f32,bool, 0 modes)

  - c/op_125 / cpp/op_125 -- **total equality**
  - c/op_125 / cpp/op_161 -- **core difference**
  - c/op_125 / cpp/op_197 -- **core difference**
  - c/op_125 / cpp/op_233 -- **core difference**
  - c/op_125 / cpp/op_485 -- **core difference**
  - c/op_125 / cpp/op_521 -- **core difference**
  - c/op_125 / cpp/op_989 -- **core difference**
  - c/op_161 / cpp/op_125 -- **core difference**
  - c/op_161 / cpp/op_161 -- **total equality**
  - c/op_161 / cpp/op_197 -- **core difference**
  - c/op_161 / cpp/op_233 -- **core difference**
  - c/op_161 / cpp/op_485 -- **core difference**
  - c/op_161 / cpp/op_521 -- **core difference**
  - c/op_161 / cpp/op_989 -- **core difference**
  - c/op_197 / cpp/op_125 -- **core difference**
  - c/op_197 / cpp/op_161 -- **core difference**
  - c/op_197 / cpp/op_197 -- **total equality**
  - c/op_197 / cpp/op_233 -- **core difference**
  - c/op_197 / cpp/op_485 -- **core difference**
  - c/op_197 / cpp/op_521 -- **core difference**
  - c/op_197 / cpp/op_989 -- **core difference**
  - c/op_233 / cpp/op_125 -- **core difference**
  - c/op_233 / cpp/op_161 -- **core difference**
  - c/op_233 / cpp/op_197 -- **core difference**
  - c/op_233 / cpp/op_233 -- **total equality**
  - c/op_233 / cpp/op_485 -- **core difference**
  - c/op_233 / cpp/op_521 -- **core difference**
  - c/op_233 / cpp/op_989 -- **core difference**
  - c/op_485 / cpp/op_125 -- **core difference**
  - c/op_485 / cpp/op_161 -- **core difference**
  - c/op_485 / cpp/op_197 -- **core difference**
  - c/op_485 / cpp/op_233 -- **core difference**
  - c/op_485 / cpp/op_485 -- **total equality**
  - c/op_485 / cpp/op_521 -- **core difference**
  - c/op_485 / cpp/op_989 -- **core difference**
  - c/op_521 / cpp/op_125 -- **core difference**
  - c/op_521 / cpp/op_161 -- **core difference**
  - c/op_521 / cpp/op_197 -- **core difference**
  - c/op_521 / cpp/op_233 -- **core difference**
  - c/op_521 / cpp/op_485 -- **core difference**
  - c/op_521 / cpp/op_521 -- **total equality**
  - c/op_521 / cpp/op_989 -- **total equality**

### shared-core group F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in1:64)))) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `>` (f32,bool, 0 modes); c `>=` (f32,bool, 0 modes); c `<=` (f32,bool, 0 modes); c `<` (f32,bool, 0 modes); cpp `>` (f32,bool, 0 modes); cpp `>=` (f32,bool, 0 modes); cpp `<=` (f32,bool, 0 modes); cpp `<` (f32,bool, 0 modes)

  - c/op_557 / cpp/op_557 -- **core difference**
  - c/op_557 / cpp/op_593 -- **core difference**
  - c/op_557 / cpp/op_629 -- **core difference**
  - c/op_557 / cpp/op_665 -- **core difference**
  - c/op_593 / cpp/op_557 -- **core difference**
  - c/op_593 / cpp/op_593 -- **core difference**
  - c/op_593 / cpp/op_629 -- **core difference**
  - c/op_593 / cpp/op_665 -- **core difference**
  - c/op_629 / cpp/op_557 -- **core difference**
  - c/op_629 / cpp/op_593 -- **core difference**
  - c/op_629 / cpp/op_629 -- **core difference**
  - c/op_629 / cpp/op_665 -- **core difference**
  - c/op_665 / cpp/op_557 -- **core difference**
  - c/op_665 / cpp/op_593 -- **core difference**
  - c/op_665 / cpp/op_629 -- **core difference**
  - c/op_665 / cpp/op_665 -- **core difference**

### shared-core group I32StoF64(ex32@0(in1:64)) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `+` (f32,bool, 0 modes); c `-` (f32,bool, 0 modes); c `*` (f32,bool, 0 modes); c `/` (f32,bool, 0 modes); c `==` (f32,bool, 0 modes); c `!=` (f32,bool, 0 modes); c `>` (f32,bool, 0 modes); c `>=` (f32,bool, 0 modes); c `<=` (f32,bool, 0 modes); c `<` (f32,bool, 0 modes); cpp `+` (f32,bool, 0 modes); cpp `-` (f32,bool, 0 modes); cpp `*` (f32,bool, 0 modes); cpp `/` (f32,bool, 0 modes); cpp `==` (f32,bool, 0 modes); cpp `!=` (f32,bool, 0 modes); cpp `>` (f32,bool, 0 modes); cpp `>=` (f32,bool, 0 modes); cpp `<=` (f32,bool, 0 modes); cpp `<` (f32,bool, 0 modes); cpp `not_eq` (f32,bool, 0 modes)

  - c/op_125 / cpp/op_125 -- **total equality**
  - c/op_125 / cpp/op_161 -- **core difference**
  - c/op_125 / cpp/op_197 -- **core difference**
  - c/op_125 / cpp/op_233 -- **core difference**
  - c/op_125 / cpp/op_485 -- **core difference**
  - c/op_125 / cpp/op_521 -- **core difference**
  - c/op_125 / cpp/op_557 -- **core difference**
  - c/op_125 / cpp/op_593 -- **core difference**
  - c/op_125 / cpp/op_629 -- **core difference**
  - c/op_125 / cpp/op_665 -- **core difference**
  - c/op_125 / cpp/op_989 -- **core difference**
  - c/op_161 / cpp/op_125 -- **core difference**
  - c/op_161 / cpp/op_161 -- **total equality**
  - c/op_161 / cpp/op_197 -- **core difference**
  - c/op_161 / cpp/op_233 -- **core difference**
  - c/op_161 / cpp/op_485 -- **core difference**
  - c/op_161 / cpp/op_521 -- **core difference**
  - c/op_161 / cpp/op_557 -- **core difference**
  - c/op_161 / cpp/op_593 -- **core difference**
  - c/op_161 / cpp/op_629 -- **core difference**
  - c/op_161 / cpp/op_665 -- **core difference**
  - c/op_161 / cpp/op_989 -- **core difference**
  - c/op_197 / cpp/op_125 -- **core difference**
  - c/op_197 / cpp/op_161 -- **core difference**
  - c/op_197 / cpp/op_197 -- **total equality**
  - c/op_197 / cpp/op_233 -- **core difference**
  - c/op_197 / cpp/op_485 -- **core difference**
  - c/op_197 / cpp/op_521 -- **core difference**
  - c/op_197 / cpp/op_557 -- **core difference**
  - c/op_197 / cpp/op_593 -- **core difference**
  - c/op_197 / cpp/op_629 -- **core difference**
  - c/op_197 / cpp/op_665 -- **core difference**
  - c/op_197 / cpp/op_989 -- **core difference**
  - c/op_233 / cpp/op_125 -- **core difference**
  - c/op_233 / cpp/op_161 -- **core difference**
  - c/op_233 / cpp/op_197 -- **core difference**
  - c/op_233 / cpp/op_233 -- **total equality**
  - c/op_233 / cpp/op_485 -- **core difference**
  - c/op_233 / cpp/op_521 -- **core difference**
  - c/op_233 / cpp/op_557 -- **core difference**
  - c/op_233 / cpp/op_593 -- **core difference**
  - c/op_233 / cpp/op_629 -- **core difference**
  - c/op_233 / cpp/op_665 -- **core difference**
  - c/op_233 / cpp/op_989 -- **core difference**
  - c/op_485 / cpp/op_125 -- **core difference**
  - c/op_485 / cpp/op_161 -- **core difference**
  - c/op_485 / cpp/op_197 -- **core difference**
  - c/op_485 / cpp/op_233 -- **core difference**
  - c/op_485 / cpp/op_485 -- **total equality**
  - c/op_485 / cpp/op_521 -- **core difference**
  - c/op_485 / cpp/op_557 -- **core difference**
  - c/op_485 / cpp/op_593 -- **core difference**
  - c/op_485 / cpp/op_629 -- **core difference**
  - c/op_485 / cpp/op_665 -- **core difference**
  - c/op_485 / cpp/op_989 -- **core difference**
  - c/op_521 / cpp/op_125 -- **core difference**
  - c/op_521 / cpp/op_161 -- **core difference**
  - c/op_521 / cpp/op_197 -- **core difference**
  - c/op_521 / cpp/op_233 -- **core difference**
  - c/op_521 / cpp/op_485 -- **core difference**
  - c/op_521 / cpp/op_521 -- **total equality**
  - c/op_521 / cpp/op_557 -- **core difference**
  - c/op_521 / cpp/op_593 -- **core difference**
  - c/op_521 / cpp/op_629 -- **core difference**
  - c/op_521 / cpp/op_665 -- **core difference**
  - c/op_521 / cpp/op_989 -- **total equality**
  - c/op_557 / cpp/op_125 -- **core difference**
  - c/op_557 / cpp/op_161 -- **core difference**
  - c/op_557 / cpp/op_197 -- **core difference**
  - c/op_557 / cpp/op_233 -- **core difference**
  - c/op_557 / cpp/op_485 -- **core difference**
  - c/op_557 / cpp/op_521 -- **core difference**
  - c/op_557 / cpp/op_557 -- **core difference**
  - c/op_557 / cpp/op_593 -- **core difference**
  - c/op_557 / cpp/op_629 -- **core difference**
  - c/op_557 / cpp/op_665 -- **core difference**
  - c/op_557 / cpp/op_989 -- **core difference**
  - c/op_593 / cpp/op_125 -- **core difference**
  - c/op_593 / cpp/op_161 -- **core difference**
  - c/op_593 / cpp/op_197 -- **core difference**
  - c/op_593 / cpp/op_233 -- **core difference**
  - c/op_593 / cpp/op_485 -- **core difference**
  - c/op_593 / cpp/op_521 -- **core difference**
  - c/op_593 / cpp/op_557 -- **core difference**
  - c/op_593 / cpp/op_593 -- **core difference**
  - c/op_593 / cpp/op_629 -- **core difference**
  - c/op_593 / cpp/op_665 -- **core difference**
  - c/op_593 / cpp/op_989 -- **core difference**
  - c/op_629 / cpp/op_125 -- **core difference**
  - c/op_629 / cpp/op_161 -- **core difference**
  - c/op_629 / cpp/op_197 -- **core difference**
  - c/op_629 / cpp/op_233 -- **core difference**
  - c/op_629 / cpp/op_485 -- **core difference**
  - c/op_629 / cpp/op_521 -- **core difference**
  - c/op_629 / cpp/op_557 -- **core difference**
  - c/op_629 / cpp/op_593 -- **core difference**
  - c/op_629 / cpp/op_629 -- **core difference**
  - c/op_629 / cpp/op_665 -- **core difference**
  - c/op_629 / cpp/op_989 -- **core difference**
  - c/op_665 / cpp/op_125 -- **core difference**
  - c/op_665 / cpp/op_161 -- **core difference**
  - c/op_665 / cpp/op_197 -- **core difference**
  - c/op_665 / cpp/op_233 -- **core difference**
  - c/op_665 / cpp/op_485 -- **core difference**
  - c/op_665 / cpp/op_521 -- **core difference**
  - c/op_665 / cpp/op_557 -- **core difference**
  - c/op_665 / cpp/op_593 -- **core difference**
  - c/op_665 / cpp/op_629 -- **core difference**
  - c/op_665 / cpp/op_665 -- **core difference**
  - c/op_665 / cpp/op_989 -- **core difference**

### shared-core group F32toF64(ex32@0(in0:256)) · (f32,bool)

- ground: connection
- languages: c, cpp
- members: c `||` (f32,bool, 0 modes); c `&&` (f32,bool, 0 modes); c `>` (f32,bool, 0 modes); c `>=` (f32,bool, 0 modes); c `<=` (f32,bool, 0 modes); c `<` (f32,bool, 0 modes); cpp `||` (f32,bool, 0 modes); cpp `&&` (f32,bool, 0 modes); cpp `>` (f32,bool, 0 modes); cpp `>=` (f32,bool, 0 modes); cpp `<=` (f32,bool, 0 modes); cpp `<` (f32,bool, 0 modes); cpp `or` (f32,bool, 0 modes); cpp `and` (f32,bool, 0 modes)

  - c/op_305 / cpp/op_305 -- **core difference**
  - c/op_305 / cpp/op_341 -- **core difference**
  - c/op_305 / cpp/op_557 -- **core difference**
  - c/op_305 / cpp/op_593 -- **core difference**
  - c/op_305 / cpp/op_629 -- **core difference**
  - c/op_305 / cpp/op_665 -- **core difference**
  - c/op_305 / cpp/op_809 -- **core difference**
  - c/op_305 / cpp/op_845 -- **core difference**
  - c/op_341 / cpp/op_305 -- **core difference**
  - c/op_341 / cpp/op_341 -- **core difference**
  - c/op_341 / cpp/op_557 -- **core difference**
  - c/op_341 / cpp/op_593 -- **core difference**
  - c/op_341 / cpp/op_629 -- **core difference**
  - c/op_341 / cpp/op_665 -- **core difference**
  - c/op_341 / cpp/op_809 -- **core difference**
  - c/op_341 / cpp/op_845 -- **core difference**
  - c/op_557 / cpp/op_305 -- **core difference**
  - c/op_557 / cpp/op_341 -- **core difference**
  - c/op_557 / cpp/op_557 -- **core difference**
  - c/op_557 / cpp/op_593 -- **core difference**
  - c/op_557 / cpp/op_629 -- **core difference**
  - c/op_557 / cpp/op_665 -- **core difference**
  - c/op_557 / cpp/op_809 -- **core difference**
  - c/op_557 / cpp/op_845 -- **core difference**
  - c/op_593 / cpp/op_305 -- **core difference**
  - c/op_593 / cpp/op_341 -- **core difference**
  - c/op_593 / cpp/op_557 -- **core difference**
  - c/op_593 / cpp/op_593 -- **core difference**
  - c/op_593 / cpp/op_629 -- **core difference**
  - c/op_593 / cpp/op_665 -- **core difference**
  - c/op_593 / cpp/op_809 -- **core difference**
  - c/op_593 / cpp/op_845 -- **core difference**
  - c/op_629 / cpp/op_305 -- **core difference**
  - c/op_629 / cpp/op_341 -- **core difference**
  - c/op_629 / cpp/op_557 -- **core difference**
  - c/op_629 / cpp/op_593 -- **core difference**
  - c/op_629 / cpp/op_629 -- **core difference**
  - c/op_629 / cpp/op_665 -- **core difference**
  - c/op_629 / cpp/op_809 -- **core difference**
  - c/op_629 / cpp/op_845 -- **core difference**
  - c/op_665 / cpp/op_305 -- **core difference**
  - c/op_665 / cpp/op_341 -- **core difference**
  - c/op_665 / cpp/op_557 -- **core difference**
  - c/op_665 / cpp/op_593 -- **core difference**
  - c/op_665 / cpp/op_629 -- **core difference**
  - c/op_665 / cpp/op_665 -- **core difference**
  - c/op_665 / cpp/op_809 -- **core difference**
  - c/op_665 / cpp/op_845 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(ex32@0(in1:256))))),0:64,u0:64))) · (f32,f32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `>` (f32,f32, 0 modes); cpp `>` (f32,f32, 0 modes); go `>` (f32,f32, 0 modes); rust `>` (f32,f32, 0 modes); swift `>` (f32,f32, 0 modes)

  - c/op_555 / cpp/op_555 -- **core difference**
  - c/op_555 / go/op_621 -- **core difference**
  - c/op_555 / rust/op_411 -- **core difference**
  - c/op_555 / swift/op_351 -- **core difference**
  - cpp/op_555 / go/op_621 -- **total equality**
  - cpp/op_555 / rust/op_411 -- **total equality**
  - cpp/op_555 / swift/op_351 -- **total equality**
  - go/op_621 / rust/op_411 -- **total equality**
  - go/op_621 / swift/op_351 -- **total equality**
  - rust/op_411 / swift/op_351 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(ex32@0(in1:256))))),0:64,u0:64))) · (f32,f32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `>=` (f32,f32, 0 modes); cpp `>=` (f32,f32, 0 modes); go `>=` (f32,f32, 0 modes); rust `>=` (f32,f32, 0 modes); swift `>=` (f32,f32, 0 modes)

  - c/op_591 / cpp/op_591 -- **core difference**
  - c/op_591 / go/op_657 -- **core difference**
  - c/op_591 / rust/op_447 -- **core difference**
  - c/op_591 / swift/op_423 -- **core difference**
  - cpp/op_591 / go/op_657 -- **total equality**
  - cpp/op_591 / rust/op_447 -- **total equality**
  - cpp/op_591 / swift/op_423 -- **total equality**
  - go/op_657 / rust/op_447 -- **total equality**
  - go/op_657 / swift/op_423 -- **total equality**
  - rust/op_447 / swift/op_423 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256))))),0:64,u0:64))) · (f32,f32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `<=` (f32,f32, 0 modes); cpp `<=` (f32,f32, 0 modes); go `<=` (f32,f32, 0 modes); rust `<=` (f32,f32, 0 modes); swift `<=` (f32,f32, 0 modes)

  - c/op_627 / cpp/op_627 -- **core difference**
  - c/op_627 / go/op_585 -- **core difference**
  - c/op_627 / rust/op_375 -- **core difference**
  - c/op_627 / swift/op_387 -- **core difference**
  - cpp/op_627 / go/op_585 -- **total equality**
  - cpp/op_627 / rust/op_375 -- **total equality**
  - cpp/op_627 / swift/op_387 -- **total equality**
  - go/op_585 / rust/op_375 -- **total equality**
  - go/op_585 / swift/op_387 -- **total equality**
  - rust/op_375 / swift/op_387 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256))))),0:64,u0:64))) · (f32,f32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `<` (f32,f32, 0 modes); cpp `<` (f32,f32, 0 modes); go `<` (f32,f32, 0 modes); rust `<` (f32,f32, 0 modes); swift `<` (f32,f32, 0 modes)

  - c/op_663 / cpp/op_663 -- **core difference**
  - c/op_663 / go/op_549 -- **core difference**
  - c/op_663 / rust/op_339 -- **core difference**
  - c/op_663 / swift/op_315 -- **core difference**
  - cpp/op_663 / go/op_549 -- **total equality**
  - cpp/op_663 / rust/op_339 -- **total equality**
  - cpp/op_663 / swift/op_315 -- **total equality**
  - go/op_549 / rust/op_339 -- **total equality**
  - go/op_549 / swift/op_315 -- **total equality**
  - rust/op_339 / swift/op_315 -- **total equality**

### shared-core group ex32@0(AndV128(XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(in0:256),0:128)),XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(in1:256),0:128)))) · (f32,f32)

- ground: connection
- languages: c, cpp
- members: c `&&` (f32,f32, 0 modes); cpp `&&` (f32,f32, 0 modes); cpp `and` (f32,f32, 0 modes)

  - c/op_339 / cpp/op_339 -- **core difference**
  - c/op_339 / cpp/op_843 -- **core difference**

### shared-core group ex32@0(OrV128(XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(in0:256),0:128)),XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(in1:256),0:128)))) · (f32,f32)

- ground: connection
- languages: c, cpp
- members: c `||` (f32,f32, 0 modes); cpp `||` (f32,f32, 0 modes); cpp `or` (f32,f32, 0 modes)

  - c/op_303 / cpp/op_303 -- **core difference**
  - c/op_303 / cpp/op_807 -- **core difference**

### shared-core group zx64(And32(1:32,ex32@0(XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(in0:256),ex128@0(in1:256)))))) · (f32,f32)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `!=` (f32,f32, 0 modes); cpp `!=` (f32,f32, 0 modes); cpp `not_eq` (f32,f32, 0 modes); rust `!=` (f32,f32, 0 modes); swift `!=` (f32,f32, 0 modes)

  - c/op_519 / cpp/op_519 -- **total equality**
  - c/op_519 / cpp/op_987 -- **total equality**
  - c/op_519 / rust/op_303 -- **total equality**
  - c/op_519 / swift/op_459 -- **total equality**
  - cpp/op_519 / rust/op_303 -- **total equality**
  - cpp/op_987 / rust/op_303 -- **total equality**
  - cpp/op_519 / swift/op_459 -- **total equality**
  - cpp/op_987 / swift/op_459 -- **total equality**
  - rust/op_303 / swift/op_459 -- **total equality**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(in0:256,CmpEQ32F0x4(ex128@0(in0:256),ex128@0(in1:256)))))) · (f32,f32)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `==` (f32,f32, 0 modes); cpp `==` (f32,f32, 0 modes); rust `==` (f32,f32, 0 modes); swift `==` (f32,f32, 0 modes)

  - c/op_483 / cpp/op_483 -- **total equality**
  - c/op_483 / rust/op_267 -- **total equality**
  - c/op_483 / swift/op_531 -- **total equality**
  - cpp/op_483 / rust/op_267 -- **total equality**
  - cpp/op_483 / swift/op_531 -- **total equality**
  - rust/op_267 / swift/op_531 -- **total equality**

### shared-core group And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(ex32@0(in1:256))))) · (f32,f32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `>` (f32,f32, 0 modes); c `>=` (f32,f32, 0 modes); cpp `>` (f32,f32, 0 modes); cpp `>=` (f32,f32, 0 modes); cpp `<=>` (f32,f32, 0 modes); go `==` (f32,f32, 0 modes); go `!=` (f32,f32, 0 modes); go `>` (f32,f32, 0 modes); go `>=` (f32,f32, 0 modes); rust `>` (f32,f32, 0 modes); rust `>=` (f32,f32, 0 modes); swift `>` (f32,f32, 0 modes); swift `>=` (f32,f32, 0 modes)

  - c/op_555 / cpp/op_555 -- **core difference**
  - c/op_555 / cpp/op_591 -- **core difference**
  - c/op_555 / cpp/op_771 -- **core difference**
  - c/op_591 / cpp/op_555 -- **core difference**
  - c/op_591 / cpp/op_591 -- **core difference**
  - c/op_591 / cpp/op_771 -- **core difference**
  - c/op_555 / go/op_477 -- **core difference**
  - c/op_555 / go/op_513 -- **core difference**
  - c/op_555 / go/op_621 -- **core difference**
  - c/op_555 / go/op_657 -- **core difference**
  - c/op_591 / go/op_477 -- **core difference**
  - c/op_591 / go/op_513 -- **core difference**
  - c/op_591 / go/op_621 -- **core difference**
  - c/op_591 / go/op_657 -- **core difference**
  - c/op_555 / rust/op_411 -- **core difference**
  - c/op_555 / rust/op_447 -- **core difference**
  - c/op_591 / rust/op_411 -- **core difference**
  - c/op_591 / rust/op_447 -- **core difference**
  - c/op_555 / swift/op_351 -- **core difference**
  - c/op_555 / swift/op_423 -- **core difference**
  - c/op_591 / swift/op_351 -- **core difference**
  - c/op_591 / swift/op_423 -- **core difference**
  - cpp/op_555 / go/op_477 -- **core difference**
  - cpp/op_555 / go/op_513 -- **core difference**
  - cpp/op_555 / go/op_621 -- **total equality**
  - cpp/op_555 / go/op_657 -- **core difference**
  - cpp/op_591 / go/op_477 -- **core difference**
  - cpp/op_591 / go/op_513 -- **core difference**
  - cpp/op_591 / go/op_621 -- **core difference**
  - cpp/op_591 / go/op_657 -- **total equality**
  - cpp/op_771 / go/op_477 -- **core difference**
  - cpp/op_771 / go/op_513 -- **core difference**
  - cpp/op_771 / go/op_621 -- **core difference**
  - cpp/op_771 / go/op_657 -- **core difference**
  - cpp/op_555 / rust/op_411 -- **total equality**
  - cpp/op_555 / rust/op_447 -- **core difference**
  - cpp/op_591 / rust/op_411 -- **core difference**
  - cpp/op_591 / rust/op_447 -- **total equality**
  - cpp/op_771 / rust/op_411 -- **core difference**
  - cpp/op_771 / rust/op_447 -- **core difference**
  - cpp/op_555 / swift/op_351 -- **total equality**
  - cpp/op_555 / swift/op_423 -- **core difference**
  - cpp/op_591 / swift/op_351 -- **core difference**
  - cpp/op_591 / swift/op_423 -- **total equality**
  - cpp/op_771 / swift/op_351 -- **core difference**
  - cpp/op_771 / swift/op_423 -- **core difference**
  - go/op_477 / rust/op_411 -- **core difference**
  - go/op_477 / rust/op_447 -- **core difference**
  - go/op_513 / rust/op_411 -- **core difference**
  - go/op_513 / rust/op_447 -- **core difference**
  - go/op_621 / rust/op_411 -- **total equality**
  - go/op_621 / rust/op_447 -- **core difference**
  - go/op_657 / rust/op_411 -- **core difference**
  - go/op_657 / rust/op_447 -- **total equality**
  - go/op_477 / swift/op_351 -- **core difference**
  - go/op_477 / swift/op_423 -- **core difference**
  - go/op_513 / swift/op_351 -- **core difference**
  - go/op_513 / swift/op_423 -- **core difference**
  - go/op_621 / swift/op_351 -- **total equality**
  - go/op_621 / swift/op_423 -- **core difference**
  - go/op_657 / swift/op_351 -- **core difference**
  - go/op_657 / swift/op_423 -- **total equality**
  - rust/op_411 / swift/op_351 -- **total equality**
  - rust/op_411 / swift/op_423 -- **core difference**
  - rust/op_447 / swift/op_351 -- **core difference**
  - rust/op_447 / swift/op_423 -- **total equality**

### shared-core group And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256))))) · (f32,f32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `<=` (f32,f32, 0 modes); c `<` (f32,f32, 0 modes); cpp `<=` (f32,f32, 0 modes); cpp `<` (f32,f32, 0 modes); cpp `<=>` (f32,f32, 0 modes); go `<` (f32,f32, 0 modes); go `<=` (f32,f32, 0 modes); rust `<` (f32,f32, 0 modes); rust `<=` (f32,f32, 0 modes); swift `<` (f32,f32, 0 modes); swift `<=` (f32,f32, 0 modes); swift `..<` (f32,f32, 1 modes); swift `...` (f32,f32, 1 modes)

  - c/op_627 / cpp/op_627 -- **core difference**
  - c/op_627 / cpp/op_663 -- **core difference**
  - c/op_627 / cpp/op_771 -- **core difference**
  - c/op_663 / cpp/op_627 -- **core difference**
  - c/op_663 / cpp/op_663 -- **core difference**
  - c/op_663 / cpp/op_771 -- **core difference**
  - c/op_627 / go/op_549 -- **core difference**
  - c/op_627 / go/op_585 -- **core difference**
  - c/op_663 / go/op_549 -- **core difference**
  - c/op_663 / go/op_585 -- **core difference**
  - c/op_627 / rust/op_339 -- **core difference**
  - c/op_627 / rust/op_375 -- **core difference**
  - c/op_663 / rust/op_339 -- **core difference**
  - c/op_663 / rust/op_375 -- **core difference**
  - c/op_627 / swift/op_315 -- **core difference**
  - c/op_627 / swift/op_387 -- **core difference**
  - c/op_627 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - c/op_627 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - c/op_663 / swift/op_315 -- **core difference**
  - c/op_663 / swift/op_387 -- **core difference**
  - c/op_663 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - c/op_663 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_627 / go/op_549 -- **core difference**
  - cpp/op_627 / go/op_585 -- **total equality**
  - cpp/op_663 / go/op_549 -- **total equality**
  - cpp/op_663 / go/op_585 -- **core difference**
  - cpp/op_771 / go/op_549 -- **core difference**
  - cpp/op_771 / go/op_585 -- **core difference**
  - cpp/op_627 / rust/op_339 -- **core difference**
  - cpp/op_627 / rust/op_375 -- **total equality**
  - cpp/op_663 / rust/op_339 -- **total equality**
  - cpp/op_663 / rust/op_375 -- **core difference**
  - cpp/op_771 / rust/op_339 -- **core difference**
  - cpp/op_771 / rust/op_375 -- **core difference**
  - cpp/op_627 / swift/op_315 -- **core difference**
  - cpp/op_627 / swift/op_387 -- **total equality**
  - cpp/op_627 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_627 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_663 / swift/op_315 -- **total equality**
  - cpp/op_663 / swift/op_387 -- **core difference**
  - cpp/op_663 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_663 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_771 / swift/op_315 -- **core difference**
  - cpp/op_771 / swift/op_387 -- **core difference**
  - cpp/op_771 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_771 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_549 / rust/op_339 -- **total equality**
  - go/op_549 / rust/op_375 -- **core difference**
  - go/op_585 / rust/op_339 -- **core difference**
  - go/op_585 / rust/op_375 -- **total equality**
  - go/op_549 / swift/op_315 -- **total equality**
  - go/op_549 / swift/op_387 -- **core difference**
  - go/op_549 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_549 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_585 / swift/op_315 -- **core difference**
  - go/op_585 / swift/op_387 -- **total equality**
  - go/op_585 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_585 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_339 / swift/op_315 -- **total equality**
  - rust/op_339 / swift/op_387 -- **core difference**
  - rust/op_339 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_339 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_375 / swift/op_315 -- **core difference**
  - rust/op_375 / swift/op_387 -- **total equality**
  - rust/op_375 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_375 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)

### shared-core group XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(in1:256),0:128)) · (f32,f32)

- ground: connection
- languages: c, cpp
- members: c `||` (f32,f32, 0 modes); c `&&` (f32,f32, 0 modes); cpp `||` (f32,f32, 0 modes); cpp `&&` (f32,f32, 0 modes); cpp `or` (f32,f32, 0 modes); cpp `and` (f32,f32, 0 modes)

  - c/op_303 / cpp/op_303 -- **core difference**
  - c/op_303 / cpp/op_339 -- **core difference**
  - c/op_303 / cpp/op_807 -- **core difference**
  - c/op_303 / cpp/op_843 -- **core difference**
  - c/op_339 / cpp/op_303 -- **core difference**
  - c/op_339 / cpp/op_339 -- **core difference**
  - c/op_339 / cpp/op_807 -- **core difference**
  - c/op_339 / cpp/op_843 -- **core difference**

### shared-core group XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(in0:256),0:128)) · (f32,f32)

- ground: connection
- languages: c, cpp
- members: c `||` (f32,f32, 0 modes); c `&&` (f32,f32, 0 modes); cpp `||` (f32,f32, 0 modes); cpp `&&` (f32,f32, 0 modes); cpp `or` (f32,f32, 0 modes); cpp `and` (f32,f32, 0 modes)

  - c/op_303 / cpp/op_303 -- **core difference**
  - c/op_303 / cpp/op_339 -- **core difference**
  - c/op_303 / cpp/op_807 -- **core difference**
  - c/op_303 / cpp/op_843 -- **core difference**
  - c/op_339 / cpp/op_303 -- **core difference**
  - c/op_339 / cpp/op_339 -- **core difference**
  - c/op_339 / cpp/op_807 -- **core difference**
  - c/op_339 / cpp/op_843 -- **core difference**

### shared-core group CmpEQ32F0x4(ex128@0(in0:256),ex128@0(in1:256)) · (f32,f32)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `==` (f32,f32, 0 modes); c `!=` (f32,f32, 0 modes); cpp `==` (f32,f32, 0 modes); cpp `!=` (f32,f32, 0 modes); cpp `not_eq` (f32,f32, 0 modes); rust `==` (f32,f32, 0 modes); rust `!=` (f32,f32, 0 modes); swift `!=` (f32,f32, 0 modes); swift `==` (f32,f32, 0 modes)

  - c/op_483 / cpp/op_483 -- **total equality**
  - c/op_483 / cpp/op_519 -- **core difference**
  - c/op_483 / cpp/op_987 -- **core difference**
  - c/op_519 / cpp/op_483 -- **core difference**
  - c/op_519 / cpp/op_519 -- **total equality**
  - c/op_519 / cpp/op_987 -- **total equality**
  - c/op_483 / rust/op_267 -- **total equality**
  - c/op_483 / rust/op_303 -- **core difference**
  - c/op_519 / rust/op_267 -- **core difference**
  - c/op_519 / rust/op_303 -- **total equality**
  - c/op_483 / swift/op_459 -- **core difference**
  - c/op_483 / swift/op_531 -- **total equality**
  - c/op_519 / swift/op_459 -- **total equality**
  - c/op_519 / swift/op_531 -- **core difference**
  - cpp/op_483 / rust/op_267 -- **total equality**
  - cpp/op_483 / rust/op_303 -- **core difference**
  - cpp/op_519 / rust/op_267 -- **core difference**
  - cpp/op_519 / rust/op_303 -- **total equality**
  - cpp/op_987 / rust/op_267 -- **core difference**
  - cpp/op_987 / rust/op_303 -- **total equality**
  - cpp/op_483 / swift/op_459 -- **core difference**
  - cpp/op_483 / swift/op_531 -- **total equality**
  - cpp/op_519 / swift/op_459 -- **total equality**
  - cpp/op_519 / swift/op_531 -- **core difference**
  - cpp/op_987 / swift/op_459 -- **total equality**
  - cpp/op_987 / swift/op_531 -- **core difference**
  - rust/op_267 / swift/op_459 -- **core difference**
  - rust/op_267 / swift/op_531 -- **total equality**
  - rust/op_303 / swift/op_459 -- **total equality**
  - rust/op_303 / swift/op_531 -- **core difference**

### shared-core group Add32F0x4(ex128@0(in0:256),ex128@0(in1:256)) · (f32,f32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `+` (f32,f32, 0 modes); cpp `+` (f32,f32, 0 modes); go `+` (f32,f32, 0 modes); rust `+` (f32,f32, 0 modes); swift `+` (f32,f32, 0 modes)

  - c/op_123 / cpp/op_123 -- **total equality**
  - c/op_123 / go/op_333 -- **total equality**
  - c/op_123 / rust/op_555 -- **total equality**
  - c/op_123 / swift/op_243 -- **total equality**
  - cpp/op_123 / go/op_333 -- **total equality**
  - cpp/op_123 / rust/op_555 -- **total equality**
  - cpp/op_123 / swift/op_243 -- **total equality**
  - go/op_333 / rust/op_555 -- **total equality**
  - go/op_333 / swift/op_243 -- **total equality**
  - rust/op_555 / swift/op_243 -- **total equality**

### shared-core group Sub32F0x4(ex128@0(in0:256),ex128@0(in1:256)) · (f32,f32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `-` (f32,f32, 0 modes); cpp `-` (f32,f32, 0 modes); go `-` (f32,f32, 0 modes); rust `-` (f32,f32, 0 modes); swift `-` (f32,f32, 0 modes)

  - c/op_159 / cpp/op_159 -- **total equality**
  - c/op_159 / go/op_369 -- **total equality**
  - c/op_159 / rust/op_591 -- **total equality**
  - c/op_159 / swift/op_279 -- **total equality**
  - cpp/op_159 / go/op_369 -- **total equality**
  - cpp/op_159 / rust/op_591 -- **total equality**
  - cpp/op_159 / swift/op_279 -- **total equality**
  - go/op_369 / rust/op_591 -- **total equality**
  - go/op_369 / swift/op_279 -- **total equality**
  - rust/op_591 / swift/op_279 -- **total equality**

### shared-core group Mul32F0x4(ex128@0(in0:256),ex128@0(in1:256)) · (f32,f32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `*` (f32,f32, 0 modes); cpp `*` (f32,f32, 0 modes); go `*` (f32,f32, 0 modes); rust `*` (f32,f32, 0 modes); swift `*` (f32,f32, 0 modes)

  - c/op_195 / cpp/op_195 -- **total equality**
  - c/op_195 / go/op_81 -- **total equality**
  - c/op_195 / rust/op_627 -- **total equality**
  - c/op_195 / swift/op_135 -- **total equality**
  - cpp/op_195 / go/op_81 -- **total equality**
  - cpp/op_195 / rust/op_627 -- **total equality**
  - cpp/op_195 / swift/op_135 -- **total equality**
  - go/op_81 / rust/op_627 -- **total equality**
  - go/op_81 / swift/op_135 -- **total equality**
  - rust/op_627 / swift/op_135 -- **total equality**

### shared-core group Div32F0x4(ex128@0(in0:256),ex128@0(in1:256)) · (f32,f32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `/` (f32,f32, 0 modes); cpp `/` (f32,f32, 0 modes); go `/` (f32,f32, 0 modes); rust `/` (f32,f32, 0 modes); swift `/` (f32,f32, 0 modes)

  - c/op_231 / cpp/op_231 -- **total equality**
  - c/op_231 / go/op_117 -- **total equality**
  - c/op_231 / rust/op_663 -- **total equality**
  - c/op_231 / swift/op_171 -- **total equality**
  - cpp/op_231 / go/op_117 -- **total equality**
  - cpp/op_231 / rust/op_663 -- **total equality**
  - cpp/op_231 / swift/op_171 -- **total equality**
  - go/op_117 / rust/op_663 -- **total equality**
  - go/op_117 / swift/op_171 -- **total equality**
  - rust/op_663 / swift/op_171 -- **total equality**

### shared-core group F32toF64(ex32@0(in1:256)) · (f32,f32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `>` (f32,f32, 0 modes); c `>=` (f32,f32, 0 modes); c `<=` (f32,f32, 0 modes); c `<` (f32,f32, 0 modes); cpp `>` (f32,f32, 0 modes); cpp `>=` (f32,f32, 0 modes); cpp `<=` (f32,f32, 0 modes); cpp `<` (f32,f32, 0 modes); cpp `<=>` (f32,f32, 0 modes); go `==` (f32,f32, 0 modes); go `!=` (f32,f32, 0 modes); go `<` (f32,f32, 0 modes); go `<=` (f32,f32, 0 modes); go `>` (f32,f32, 0 modes); go `>=` (f32,f32, 0 modes); rust `<` (f32,f32, 0 modes); rust `<=` (f32,f32, 0 modes); rust `>` (f32,f32, 0 modes); rust `>=` (f32,f32, 0 modes); swift `<` (f32,f32, 0 modes); swift `>` (f32,f32, 0 modes); swift `<=` (f32,f32, 0 modes); swift `>=` (f32,f32, 0 modes); swift `..<` (f32,f32, 1 modes); swift `...` (f32,f32, 1 modes)

  - c/op_555 / cpp/op_555 -- **core difference**
  - c/op_555 / cpp/op_591 -- **core difference**
  - c/op_555 / cpp/op_627 -- **core difference**
  - c/op_555 / cpp/op_663 -- **core difference**
  - c/op_555 / cpp/op_771 -- **core difference**
  - c/op_591 / cpp/op_555 -- **core difference**
  - c/op_591 / cpp/op_591 -- **core difference**
  - c/op_591 / cpp/op_627 -- **core difference**
  - c/op_591 / cpp/op_663 -- **core difference**
  - c/op_591 / cpp/op_771 -- **core difference**
  - c/op_627 / cpp/op_555 -- **core difference**
  - c/op_627 / cpp/op_591 -- **core difference**
  - c/op_627 / cpp/op_627 -- **core difference**
  - c/op_627 / cpp/op_663 -- **core difference**
  - c/op_627 / cpp/op_771 -- **core difference**
  - c/op_663 / cpp/op_555 -- **core difference**
  - c/op_663 / cpp/op_591 -- **core difference**
  - c/op_663 / cpp/op_627 -- **core difference**
  - c/op_663 / cpp/op_663 -- **core difference**
  - c/op_663 / cpp/op_771 -- **core difference**
  - c/op_555 / go/op_477 -- **core difference**
  - c/op_555 / go/op_513 -- **core difference**
  - c/op_555 / go/op_549 -- **core difference**
  - c/op_555 / go/op_585 -- **core difference**
  - c/op_555 / go/op_621 -- **core difference**
  - c/op_555 / go/op_657 -- **core difference**
  - c/op_591 / go/op_477 -- **core difference**
  - c/op_591 / go/op_513 -- **core difference**
  - c/op_591 / go/op_549 -- **core difference**
  - c/op_591 / go/op_585 -- **core difference**
  - c/op_591 / go/op_621 -- **core difference**
  - c/op_591 / go/op_657 -- **core difference**
  - c/op_627 / go/op_477 -- **core difference**
  - c/op_627 / go/op_513 -- **core difference**
  - c/op_627 / go/op_549 -- **core difference**
  - c/op_627 / go/op_585 -- **core difference**
  - c/op_627 / go/op_621 -- **core difference**
  - c/op_627 / go/op_657 -- **core difference**
  - c/op_663 / go/op_477 -- **core difference**
  - c/op_663 / go/op_513 -- **core difference**
  - c/op_663 / go/op_549 -- **core difference**
  - c/op_663 / go/op_585 -- **core difference**
  - c/op_663 / go/op_621 -- **core difference**
  - c/op_663 / go/op_657 -- **core difference**
  - c/op_555 / rust/op_339 -- **core difference**
  - c/op_555 / rust/op_375 -- **core difference**
  - c/op_555 / rust/op_411 -- **core difference**
  - c/op_555 / rust/op_447 -- **core difference**
  - c/op_591 / rust/op_339 -- **core difference**
  - c/op_591 / rust/op_375 -- **core difference**
  - c/op_591 / rust/op_411 -- **core difference**
  - c/op_591 / rust/op_447 -- **core difference**
  - c/op_627 / rust/op_339 -- **core difference**
  - c/op_627 / rust/op_375 -- **core difference**
  - c/op_627 / rust/op_411 -- **core difference**
  - c/op_627 / rust/op_447 -- **core difference**
  - c/op_663 / rust/op_339 -- **core difference**
  - c/op_663 / rust/op_375 -- **core difference**
  - c/op_663 / rust/op_411 -- **core difference**
  - c/op_663 / rust/op_447 -- **core difference**
  - c/op_555 / swift/op_315 -- **core difference**
  - c/op_555 / swift/op_351 -- **core difference**
  - c/op_555 / swift/op_387 -- **core difference**
  - c/op_555 / swift/op_423 -- **core difference**
  - c/op_555 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - c/op_555 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - c/op_591 / swift/op_315 -- **core difference**
  - c/op_591 / swift/op_351 -- **core difference**
  - c/op_591 / swift/op_387 -- **core difference**
  - c/op_591 / swift/op_423 -- **core difference**
  - c/op_591 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - c/op_591 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - c/op_627 / swift/op_315 -- **core difference**
  - c/op_627 / swift/op_351 -- **core difference**
  - c/op_627 / swift/op_387 -- **core difference**
  - c/op_627 / swift/op_423 -- **core difference**
  - c/op_627 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - c/op_627 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - c/op_663 / swift/op_315 -- **core difference**
  - c/op_663 / swift/op_351 -- **core difference**
  - c/op_663 / swift/op_387 -- **core difference**
  - c/op_663 / swift/op_423 -- **core difference**
  - c/op_663 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - c/op_663 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_555 / go/op_477 -- **core difference**
  - cpp/op_555 / go/op_513 -- **core difference**
  - cpp/op_555 / go/op_549 -- **core difference**
  - cpp/op_555 / go/op_585 -- **core difference**
  - cpp/op_555 / go/op_621 -- **total equality**
  - cpp/op_555 / go/op_657 -- **core difference**
  - cpp/op_591 / go/op_477 -- **core difference**
  - cpp/op_591 / go/op_513 -- **core difference**
  - cpp/op_591 / go/op_549 -- **core difference**
  - cpp/op_591 / go/op_585 -- **core difference**
  - cpp/op_591 / go/op_621 -- **core difference**
  - cpp/op_591 / go/op_657 -- **total equality**
  - cpp/op_627 / go/op_477 -- **core difference**
  - cpp/op_627 / go/op_513 -- **core difference**
  - cpp/op_627 / go/op_549 -- **core difference**
  - cpp/op_627 / go/op_585 -- **total equality**
  - cpp/op_627 / go/op_621 -- **core difference**
  - cpp/op_627 / go/op_657 -- **core difference**
  - cpp/op_663 / go/op_477 -- **core difference**
  - cpp/op_663 / go/op_513 -- **core difference**
  - cpp/op_663 / go/op_549 -- **total equality**
  - cpp/op_663 / go/op_585 -- **core difference**
  - cpp/op_663 / go/op_621 -- **core difference**
  - cpp/op_663 / go/op_657 -- **core difference**
  - cpp/op_771 / go/op_477 -- **core difference**
  - cpp/op_771 / go/op_513 -- **core difference**
  - cpp/op_771 / go/op_549 -- **core difference**
  - cpp/op_771 / go/op_585 -- **core difference**
  - cpp/op_771 / go/op_621 -- **core difference**
  - cpp/op_771 / go/op_657 -- **core difference**
  - cpp/op_555 / rust/op_339 -- **core difference**
  - cpp/op_555 / rust/op_375 -- **core difference**
  - cpp/op_555 / rust/op_411 -- **total equality**
  - cpp/op_555 / rust/op_447 -- **core difference**
  - cpp/op_591 / rust/op_339 -- **core difference**
  - cpp/op_591 / rust/op_375 -- **core difference**
  - cpp/op_591 / rust/op_411 -- **core difference**
  - cpp/op_591 / rust/op_447 -- **total equality**
  - cpp/op_627 / rust/op_339 -- **core difference**
  - cpp/op_627 / rust/op_375 -- **total equality**
  - cpp/op_627 / rust/op_411 -- **core difference**
  - cpp/op_627 / rust/op_447 -- **core difference**
  - cpp/op_663 / rust/op_339 -- **total equality**
  - cpp/op_663 / rust/op_375 -- **core difference**
  - cpp/op_663 / rust/op_411 -- **core difference**
  - cpp/op_663 / rust/op_447 -- **core difference**
  - cpp/op_771 / rust/op_339 -- **core difference**
  - cpp/op_771 / rust/op_375 -- **core difference**
  - cpp/op_771 / rust/op_411 -- **core difference**
  - cpp/op_771 / rust/op_447 -- **core difference**
  - cpp/op_555 / swift/op_315 -- **core difference**
  - cpp/op_555 / swift/op_351 -- **total equality**
  - cpp/op_555 / swift/op_387 -- **core difference**
  - cpp/op_555 / swift/op_423 -- **core difference**
  - cpp/op_555 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_555 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_591 / swift/op_315 -- **core difference**
  - cpp/op_591 / swift/op_351 -- **core difference**
  - cpp/op_591 / swift/op_387 -- **core difference**
  - cpp/op_591 / swift/op_423 -- **total equality**
  - cpp/op_591 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_591 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_627 / swift/op_315 -- **core difference**
  - cpp/op_627 / swift/op_351 -- **core difference**
  - cpp/op_627 / swift/op_387 -- **total equality**
  - cpp/op_627 / swift/op_423 -- **core difference**
  - cpp/op_627 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_627 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_663 / swift/op_315 -- **total equality**
  - cpp/op_663 / swift/op_351 -- **core difference**
  - cpp/op_663 / swift/op_387 -- **core difference**
  - cpp/op_663 / swift/op_423 -- **core difference**
  - cpp/op_663 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_663 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_771 / swift/op_315 -- **core difference**
  - cpp/op_771 / swift/op_351 -- **core difference**
  - cpp/op_771 / swift/op_387 -- **core difference**
  - cpp/op_771 / swift/op_423 -- **core difference**
  - cpp/op_771 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_771 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_477 / rust/op_339 -- **core difference**
  - go/op_477 / rust/op_375 -- **core difference**
  - go/op_477 / rust/op_411 -- **core difference**
  - go/op_477 / rust/op_447 -- **core difference**
  - go/op_513 / rust/op_339 -- **core difference**
  - go/op_513 / rust/op_375 -- **core difference**
  - go/op_513 / rust/op_411 -- **core difference**
  - go/op_513 / rust/op_447 -- **core difference**
  - go/op_549 / rust/op_339 -- **total equality**
  - go/op_549 / rust/op_375 -- **core difference**
  - go/op_549 / rust/op_411 -- **core difference**
  - go/op_549 / rust/op_447 -- **core difference**
  - go/op_585 / rust/op_339 -- **core difference**
  - go/op_585 / rust/op_375 -- **total equality**
  - go/op_585 / rust/op_411 -- **core difference**
  - go/op_585 / rust/op_447 -- **core difference**
  - go/op_621 / rust/op_339 -- **core difference**
  - go/op_621 / rust/op_375 -- **core difference**
  - go/op_621 / rust/op_411 -- **total equality**
  - go/op_621 / rust/op_447 -- **core difference**
  - go/op_657 / rust/op_339 -- **core difference**
  - go/op_657 / rust/op_375 -- **core difference**
  - go/op_657 / rust/op_411 -- **core difference**
  - go/op_657 / rust/op_447 -- **total equality**
  - go/op_477 / swift/op_315 -- **core difference**
  - go/op_477 / swift/op_351 -- **core difference**
  - go/op_477 / swift/op_387 -- **core difference**
  - go/op_477 / swift/op_423 -- **core difference**
  - go/op_477 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_477 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_513 / swift/op_315 -- **core difference**
  - go/op_513 / swift/op_351 -- **core difference**
  - go/op_513 / swift/op_387 -- **core difference**
  - go/op_513 / swift/op_423 -- **core difference**
  - go/op_513 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_513 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_549 / swift/op_315 -- **total equality**
  - go/op_549 / swift/op_351 -- **core difference**
  - go/op_549 / swift/op_387 -- **core difference**
  - go/op_549 / swift/op_423 -- **core difference**
  - go/op_549 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_549 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_585 / swift/op_315 -- **core difference**
  - go/op_585 / swift/op_351 -- **core difference**
  - go/op_585 / swift/op_387 -- **total equality**
  - go/op_585 / swift/op_423 -- **core difference**
  - go/op_585 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_585 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_621 / swift/op_315 -- **core difference**
  - go/op_621 / swift/op_351 -- **total equality**
  - go/op_621 / swift/op_387 -- **core difference**
  - go/op_621 / swift/op_423 -- **core difference**
  - go/op_621 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_621 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_657 / swift/op_315 -- **core difference**
  - go/op_657 / swift/op_351 -- **core difference**
  - go/op_657 / swift/op_387 -- **core difference**
  - go/op_657 / swift/op_423 -- **total equality**
  - go/op_657 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_657 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_339 / swift/op_315 -- **total equality**
  - rust/op_339 / swift/op_351 -- **core difference**
  - rust/op_339 / swift/op_387 -- **core difference**
  - rust/op_339 / swift/op_423 -- **core difference**
  - rust/op_339 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_339 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_375 / swift/op_315 -- **core difference**
  - rust/op_375 / swift/op_351 -- **core difference**
  - rust/op_375 / swift/op_387 -- **total equality**
  - rust/op_375 / swift/op_423 -- **core difference**
  - rust/op_375 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_375 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_411 / swift/op_315 -- **core difference**
  - rust/op_411 / swift/op_351 -- **total equality**
  - rust/op_411 / swift/op_387 -- **core difference**
  - rust/op_411 / swift/op_423 -- **core difference**
  - rust/op_411 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_411 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_447 / swift/op_315 -- **core difference**
  - rust/op_447 / swift/op_351 -- **core difference**
  - rust/op_447 / swift/op_387 -- **core difference**
  - rust/op_447 / swift/op_423 -- **total equality**
  - rust/op_447 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_447 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)

### shared-core group F32toF64(ex32@0(in0:256)) · (f32,f32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `>` (f32,f32, 0 modes); c `>=` (f32,f32, 0 modes); c `<=` (f32,f32, 0 modes); c `<` (f32,f32, 0 modes); cpp `>` (f32,f32, 0 modes); cpp `>=` (f32,f32, 0 modes); cpp `<=` (f32,f32, 0 modes); cpp `<` (f32,f32, 0 modes); cpp `<=>` (f32,f32, 0 modes); go `==` (f32,f32, 0 modes); go `!=` (f32,f32, 0 modes); go `<` (f32,f32, 0 modes); go `<=` (f32,f32, 0 modes); go `>` (f32,f32, 0 modes); go `>=` (f32,f32, 0 modes); rust `<` (f32,f32, 0 modes); rust `<=` (f32,f32, 0 modes); rust `>` (f32,f32, 0 modes); rust `>=` (f32,f32, 0 modes); swift `<` (f32,f32, 0 modes); swift `>` (f32,f32, 0 modes); swift `<=` (f32,f32, 0 modes); swift `>=` (f32,f32, 0 modes); swift `..<` (f32,f32, 1 modes); swift `...` (f32,f32, 1 modes)

  - c/op_555 / cpp/op_555 -- **core difference**
  - c/op_555 / cpp/op_591 -- **core difference**
  - c/op_555 / cpp/op_627 -- **core difference**
  - c/op_555 / cpp/op_663 -- **core difference**
  - c/op_555 / cpp/op_771 -- **core difference**
  - c/op_591 / cpp/op_555 -- **core difference**
  - c/op_591 / cpp/op_591 -- **core difference**
  - c/op_591 / cpp/op_627 -- **core difference**
  - c/op_591 / cpp/op_663 -- **core difference**
  - c/op_591 / cpp/op_771 -- **core difference**
  - c/op_627 / cpp/op_555 -- **core difference**
  - c/op_627 / cpp/op_591 -- **core difference**
  - c/op_627 / cpp/op_627 -- **core difference**
  - c/op_627 / cpp/op_663 -- **core difference**
  - c/op_627 / cpp/op_771 -- **core difference**
  - c/op_663 / cpp/op_555 -- **core difference**
  - c/op_663 / cpp/op_591 -- **core difference**
  - c/op_663 / cpp/op_627 -- **core difference**
  - c/op_663 / cpp/op_663 -- **core difference**
  - c/op_663 / cpp/op_771 -- **core difference**
  - c/op_555 / go/op_477 -- **core difference**
  - c/op_555 / go/op_513 -- **core difference**
  - c/op_555 / go/op_549 -- **core difference**
  - c/op_555 / go/op_585 -- **core difference**
  - c/op_555 / go/op_621 -- **core difference**
  - c/op_555 / go/op_657 -- **core difference**
  - c/op_591 / go/op_477 -- **core difference**
  - c/op_591 / go/op_513 -- **core difference**
  - c/op_591 / go/op_549 -- **core difference**
  - c/op_591 / go/op_585 -- **core difference**
  - c/op_591 / go/op_621 -- **core difference**
  - c/op_591 / go/op_657 -- **core difference**
  - c/op_627 / go/op_477 -- **core difference**
  - c/op_627 / go/op_513 -- **core difference**
  - c/op_627 / go/op_549 -- **core difference**
  - c/op_627 / go/op_585 -- **core difference**
  - c/op_627 / go/op_621 -- **core difference**
  - c/op_627 / go/op_657 -- **core difference**
  - c/op_663 / go/op_477 -- **core difference**
  - c/op_663 / go/op_513 -- **core difference**
  - c/op_663 / go/op_549 -- **core difference**
  - c/op_663 / go/op_585 -- **core difference**
  - c/op_663 / go/op_621 -- **core difference**
  - c/op_663 / go/op_657 -- **core difference**
  - c/op_555 / rust/op_339 -- **core difference**
  - c/op_555 / rust/op_375 -- **core difference**
  - c/op_555 / rust/op_411 -- **core difference**
  - c/op_555 / rust/op_447 -- **core difference**
  - c/op_591 / rust/op_339 -- **core difference**
  - c/op_591 / rust/op_375 -- **core difference**
  - c/op_591 / rust/op_411 -- **core difference**
  - c/op_591 / rust/op_447 -- **core difference**
  - c/op_627 / rust/op_339 -- **core difference**
  - c/op_627 / rust/op_375 -- **core difference**
  - c/op_627 / rust/op_411 -- **core difference**
  - c/op_627 / rust/op_447 -- **core difference**
  - c/op_663 / rust/op_339 -- **core difference**
  - c/op_663 / rust/op_375 -- **core difference**
  - c/op_663 / rust/op_411 -- **core difference**
  - c/op_663 / rust/op_447 -- **core difference**
  - c/op_555 / swift/op_315 -- **core difference**
  - c/op_555 / swift/op_351 -- **core difference**
  - c/op_555 / swift/op_387 -- **core difference**
  - c/op_555 / swift/op_423 -- **core difference**
  - c/op_555 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - c/op_555 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - c/op_591 / swift/op_315 -- **core difference**
  - c/op_591 / swift/op_351 -- **core difference**
  - c/op_591 / swift/op_387 -- **core difference**
  - c/op_591 / swift/op_423 -- **core difference**
  - c/op_591 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - c/op_591 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - c/op_627 / swift/op_315 -- **core difference**
  - c/op_627 / swift/op_351 -- **core difference**
  - c/op_627 / swift/op_387 -- **core difference**
  - c/op_627 / swift/op_423 -- **core difference**
  - c/op_627 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - c/op_627 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - c/op_663 / swift/op_315 -- **core difference**
  - c/op_663 / swift/op_351 -- **core difference**
  - c/op_663 / swift/op_387 -- **core difference**
  - c/op_663 / swift/op_423 -- **core difference**
  - c/op_663 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - c/op_663 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_555 / go/op_477 -- **core difference**
  - cpp/op_555 / go/op_513 -- **core difference**
  - cpp/op_555 / go/op_549 -- **core difference**
  - cpp/op_555 / go/op_585 -- **core difference**
  - cpp/op_555 / go/op_621 -- **total equality**
  - cpp/op_555 / go/op_657 -- **core difference**
  - cpp/op_591 / go/op_477 -- **core difference**
  - cpp/op_591 / go/op_513 -- **core difference**
  - cpp/op_591 / go/op_549 -- **core difference**
  - cpp/op_591 / go/op_585 -- **core difference**
  - cpp/op_591 / go/op_621 -- **core difference**
  - cpp/op_591 / go/op_657 -- **total equality**
  - cpp/op_627 / go/op_477 -- **core difference**
  - cpp/op_627 / go/op_513 -- **core difference**
  - cpp/op_627 / go/op_549 -- **core difference**
  - cpp/op_627 / go/op_585 -- **total equality**
  - cpp/op_627 / go/op_621 -- **core difference**
  - cpp/op_627 / go/op_657 -- **core difference**
  - cpp/op_663 / go/op_477 -- **core difference**
  - cpp/op_663 / go/op_513 -- **core difference**
  - cpp/op_663 / go/op_549 -- **total equality**
  - cpp/op_663 / go/op_585 -- **core difference**
  - cpp/op_663 / go/op_621 -- **core difference**
  - cpp/op_663 / go/op_657 -- **core difference**
  - cpp/op_771 / go/op_477 -- **core difference**
  - cpp/op_771 / go/op_513 -- **core difference**
  - cpp/op_771 / go/op_549 -- **core difference**
  - cpp/op_771 / go/op_585 -- **core difference**
  - cpp/op_771 / go/op_621 -- **core difference**
  - cpp/op_771 / go/op_657 -- **core difference**
  - cpp/op_555 / rust/op_339 -- **core difference**
  - cpp/op_555 / rust/op_375 -- **core difference**
  - cpp/op_555 / rust/op_411 -- **total equality**
  - cpp/op_555 / rust/op_447 -- **core difference**
  - cpp/op_591 / rust/op_339 -- **core difference**
  - cpp/op_591 / rust/op_375 -- **core difference**
  - cpp/op_591 / rust/op_411 -- **core difference**
  - cpp/op_591 / rust/op_447 -- **total equality**
  - cpp/op_627 / rust/op_339 -- **core difference**
  - cpp/op_627 / rust/op_375 -- **total equality**
  - cpp/op_627 / rust/op_411 -- **core difference**
  - cpp/op_627 / rust/op_447 -- **core difference**
  - cpp/op_663 / rust/op_339 -- **total equality**
  - cpp/op_663 / rust/op_375 -- **core difference**
  - cpp/op_663 / rust/op_411 -- **core difference**
  - cpp/op_663 / rust/op_447 -- **core difference**
  - cpp/op_771 / rust/op_339 -- **core difference**
  - cpp/op_771 / rust/op_375 -- **core difference**
  - cpp/op_771 / rust/op_411 -- **core difference**
  - cpp/op_771 / rust/op_447 -- **core difference**
  - cpp/op_555 / swift/op_315 -- **core difference**
  - cpp/op_555 / swift/op_351 -- **total equality**
  - cpp/op_555 / swift/op_387 -- **core difference**
  - cpp/op_555 / swift/op_423 -- **core difference**
  - cpp/op_555 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_555 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_591 / swift/op_315 -- **core difference**
  - cpp/op_591 / swift/op_351 -- **core difference**
  - cpp/op_591 / swift/op_387 -- **core difference**
  - cpp/op_591 / swift/op_423 -- **total equality**
  - cpp/op_591 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_591 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_627 / swift/op_315 -- **core difference**
  - cpp/op_627 / swift/op_351 -- **core difference**
  - cpp/op_627 / swift/op_387 -- **total equality**
  - cpp/op_627 / swift/op_423 -- **core difference**
  - cpp/op_627 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_627 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_663 / swift/op_315 -- **total equality**
  - cpp/op_663 / swift/op_351 -- **core difference**
  - cpp/op_663 / swift/op_387 -- **core difference**
  - cpp/op_663 / swift/op_423 -- **core difference**
  - cpp/op_663 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_663 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_771 / swift/op_315 -- **core difference**
  - cpp/op_771 / swift/op_351 -- **core difference**
  - cpp/op_771 / swift/op_387 -- **core difference**
  - cpp/op_771 / swift/op_423 -- **core difference**
  - cpp/op_771 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - cpp/op_771 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_477 / rust/op_339 -- **core difference**
  - go/op_477 / rust/op_375 -- **core difference**
  - go/op_477 / rust/op_411 -- **core difference**
  - go/op_477 / rust/op_447 -- **core difference**
  - go/op_513 / rust/op_339 -- **core difference**
  - go/op_513 / rust/op_375 -- **core difference**
  - go/op_513 / rust/op_411 -- **core difference**
  - go/op_513 / rust/op_447 -- **core difference**
  - go/op_549 / rust/op_339 -- **total equality**
  - go/op_549 / rust/op_375 -- **core difference**
  - go/op_549 / rust/op_411 -- **core difference**
  - go/op_549 / rust/op_447 -- **core difference**
  - go/op_585 / rust/op_339 -- **core difference**
  - go/op_585 / rust/op_375 -- **total equality**
  - go/op_585 / rust/op_411 -- **core difference**
  - go/op_585 / rust/op_447 -- **core difference**
  - go/op_621 / rust/op_339 -- **core difference**
  - go/op_621 / rust/op_375 -- **core difference**
  - go/op_621 / rust/op_411 -- **total equality**
  - go/op_621 / rust/op_447 -- **core difference**
  - go/op_657 / rust/op_339 -- **core difference**
  - go/op_657 / rust/op_375 -- **core difference**
  - go/op_657 / rust/op_411 -- **core difference**
  - go/op_657 / rust/op_447 -- **total equality**
  - go/op_477 / swift/op_315 -- **core difference**
  - go/op_477 / swift/op_351 -- **core difference**
  - go/op_477 / swift/op_387 -- **core difference**
  - go/op_477 / swift/op_423 -- **core difference**
  - go/op_477 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_477 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_513 / swift/op_315 -- **core difference**
  - go/op_513 / swift/op_351 -- **core difference**
  - go/op_513 / swift/op_387 -- **core difference**
  - go/op_513 / swift/op_423 -- **core difference**
  - go/op_513 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_513 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_549 / swift/op_315 -- **total equality**
  - go/op_549 / swift/op_351 -- **core difference**
  - go/op_549 / swift/op_387 -- **core difference**
  - go/op_549 / swift/op_423 -- **core difference**
  - go/op_549 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_549 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_585 / swift/op_315 -- **core difference**
  - go/op_585 / swift/op_351 -- **core difference**
  - go/op_585 / swift/op_387 -- **total equality**
  - go/op_585 / swift/op_423 -- **core difference**
  - go/op_585 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_585 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_621 / swift/op_315 -- **core difference**
  - go/op_621 / swift/op_351 -- **total equality**
  - go/op_621 / swift/op_387 -- **core difference**
  - go/op_621 / swift/op_423 -- **core difference**
  - go/op_621 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_621 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_657 / swift/op_315 -- **core difference**
  - go/op_657 / swift/op_351 -- **core difference**
  - go/op_657 / swift/op_387 -- **core difference**
  - go/op_657 / swift/op_423 -- **total equality**
  - go/op_657 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - go/op_657 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_339 / swift/op_315 -- **total equality**
  - rust/op_339 / swift/op_351 -- **core difference**
  - rust/op_339 / swift/op_387 -- **core difference**
  - rust/op_339 / swift/op_423 -- **core difference**
  - rust/op_339 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_339 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_375 / swift/op_315 -- **core difference**
  - rust/op_375 / swift/op_351 -- **core difference**
  - rust/op_375 / swift/op_387 -- **total equality**
  - rust/op_375 / swift/op_423 -- **core difference**
  - rust/op_375 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_375 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_411 / swift/op_315 -- **core difference**
  - rust/op_411 / swift/op_351 -- **total equality**
  - rust/op_411 / swift/op_387 -- **core difference**
  - rust/op_411 / swift/op_423 -- **core difference**
  - rust/op_411 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_411 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_447 / swift/op_315 -- **core difference**
  - rust/op_447 / swift/op_351 -- **core difference**
  - rust/op_447 / swift/op_387 -- **core difference**
  - rust/op_447 / swift/op_423 -- **total equality**
  - rust/op_447 / swift/op_891 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)
  - rust/op_447 / swift/op_927 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(ex32@0(in0:256)))), 0)` -> `trap` (branch-to-response)

### shared-core group And8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64)))),Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64))))) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `&&` (f32,f64, 0 modes); cpp `&&` (f32,f64, 0 modes); cpp `and` (f32,f64, 0 modes)

  - c/op_340 / cpp/op_340 -- **core difference**
  - c/op_340 / cpp/op_844 -- **core difference**

### shared-core group Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64)))),Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64))))) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `||` (f32,f64, 0 modes); cpp `||` (f32,f64, 0 modes); cpp `or` (f32,f64, 0 modes)

  - c/op_304 / cpp/op_304 -- **core difference**
  - c/op_304 / cpp/op_808 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64)))) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `||` (f32,f64, 0 modes); c `&&` (f32,f64, 0 modes); cpp `||` (f32,f64, 0 modes); cpp `&&` (f32,f64, 0 modes); cpp `or` (f32,f64, 0 modes); cpp `and` (f32,f64, 0 modes)

  - c/op_304 / cpp/op_304 -- **core difference**
  - c/op_304 / cpp/op_340 -- **core difference**
  - c/op_304 / cpp/op_808 -- **core difference**
  - c/op_304 / cpp/op_844 -- **core difference**
  - c/op_340 / cpp/op_304 -- **core difference**
  - c/op_340 / cpp/op_340 -- **core difference**
  - c/op_340 / cpp/op_808 -- **core difference**
  - c/op_340 / cpp/op_844 -- **core difference**

### shared-core group ins@0(ins@0(in0:256,F32toF64(ex32@0(in0:256))),XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))),ex128@0(in1:256)))) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `!=` (f32,f64, 0 modes); cpp `!=` (f32,f64, 0 modes); cpp `not_eq` (f32,f64, 0 modes)

  - c/op_520 / cpp/op_520 -- **total equality**
  - c/op_520 / cpp/op_988 -- **total equality**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(ins@0(in0:256,F32toF64(ex32@0(in0:256))),CmpEQ64F0x2(ex128@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))),ex128@0(in1:256)))))) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `==` (f32,f64, 0 modes); cpp `==` (f32,f64, 0 modes)

  - c/op_484 / cpp/op_484 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))),ex64@0(in1:256)))),0:64,u0:64))) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `>` (f32,f64, 0 modes); cpp `>` (f32,f64, 0 modes)

  - c/op_556 / cpp/op_556 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))),ex64@0(in1:256)))),0:64,u0:64))) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `>=` (f32,f64, 0 modes); cpp `>=` (f32,f64, 0 modes)

  - c/op_592 / cpp/op_592 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(ins@0(in0:256,F32toF64(ex32@0(in0:256))))))),0:64,u0:64))) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `<=` (f32,f64, 0 modes); cpp `<=` (f32,f64, 0 modes)

  - c/op_628 / cpp/op_628 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(ins@0(in0:256,F32toF64(ex32@0(in0:256))))))),0:64,u0:64))) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `<` (f32,f64, 0 modes); cpp `<` (f32,f64, 0 modes)

  - c/op_664 / cpp/op_664 -- **core difference**

### shared-core group ins@0(ins@0(in0:256,F32toF64(ex32@0(in0:256))),Add64F0x2(ex128@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))),ex128@0(in1:256))) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `+` (f32,f64, 0 modes); cpp `+` (f32,f64, 0 modes)

  - c/op_124 / cpp/op_124 -- **total equality**

### shared-core group ins@0(ins@0(in0:256,F32toF64(ex32@0(in0:256))),Sub64F0x2(ex128@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))),ex128@0(in1:256))) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `-` (f32,f64, 0 modes); cpp `-` (f32,f64, 0 modes)

  - c/op_160 / cpp/op_160 -- **total equality**

### shared-core group ins@0(ins@0(in0:256,F32toF64(ex32@0(in0:256))),Mul64F0x2(ex128@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))),ex128@0(in1:256))) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `*` (f32,f64, 0 modes); cpp `*` (f32,f64, 0 modes)

  - c/op_196 / cpp/op_196 -- **total equality**

### shared-core group ins@0(ins@0(in0:256,F32toF64(ex32@0(in0:256))),Div64F0x2(ex128@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))),ex128@0(in1:256))) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `/` (f32,f64, 0 modes); cpp `/` (f32,f64, 0 modes)

  - c/op_232 / cpp/op_232 -- **total equality**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))),ex64@0(in1:256)))) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `>` (f32,f64, 0 modes); c `>=` (f32,f64, 0 modes); cpp `>` (f32,f64, 0 modes); cpp `>=` (f32,f64, 0 modes); cpp `<=>` (f32,f64, 0 modes)

  - c/op_556 / cpp/op_556 -- **core difference**
  - c/op_556 / cpp/op_592 -- **core difference**
  - c/op_556 / cpp/op_772 -- **core difference**
  - c/op_592 / cpp/op_556 -- **core difference**
  - c/op_592 / cpp/op_592 -- **core difference**
  - c/op_592 / cpp/op_772 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(ins@0(in0:256,F32toF64(ex32@0(in0:256))))))) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `<=` (f32,f64, 0 modes); c `<` (f32,f64, 0 modes); cpp `<=` (f32,f64, 0 modes); cpp `<` (f32,f64, 0 modes); cpp `<=>` (f32,f64, 0 modes)

  - c/op_628 / cpp/op_628 -- **core difference**
  - c/op_628 / cpp/op_664 -- **core difference**
  - c/op_628 / cpp/op_772 -- **core difference**
  - c/op_664 / cpp/op_628 -- **core difference**
  - c/op_664 / cpp/op_664 -- **core difference**
  - c/op_664 / cpp/op_772 -- **core difference**

### shared-core group CmpEQ64F0x2(ex128@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))),ex128@0(in1:256)) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `==` (f32,f64, 0 modes); c `!=` (f32,f64, 0 modes); cpp `==` (f32,f64, 0 modes); cpp `!=` (f32,f64, 0 modes); cpp `not_eq` (f32,f64, 0 modes)

  - c/op_484 / cpp/op_484 -- **total equality**
  - c/op_484 / cpp/op_520 -- **core difference**
  - c/op_484 / cpp/op_988 -- **core difference**
  - c/op_520 / cpp/op_484 -- **core difference**
  - c/op_520 / cpp/op_520 -- **total equality**
  - c/op_520 / cpp/op_988 -- **total equality**

### shared-core group ex128@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `+` (f32,f64, 0 modes); c `-` (f32,f64, 0 modes); c `*` (f32,f64, 0 modes); c `/` (f32,f64, 0 modes); c `==` (f32,f64, 0 modes); c `!=` (f32,f64, 0 modes); cpp `+` (f32,f64, 0 modes); cpp `-` (f32,f64, 0 modes); cpp `*` (f32,f64, 0 modes); cpp `/` (f32,f64, 0 modes); cpp `==` (f32,f64, 0 modes); cpp `!=` (f32,f64, 0 modes); cpp `not_eq` (f32,f64, 0 modes)

  - c/op_124 / cpp/op_124 -- **total equality**
  - c/op_124 / cpp/op_160 -- **core difference**
  - c/op_124 / cpp/op_196 -- **core difference**
  - c/op_124 / cpp/op_232 -- **core difference**
  - c/op_124 / cpp/op_484 -- **core difference**
  - c/op_124 / cpp/op_520 -- **core difference**
  - c/op_124 / cpp/op_988 -- **core difference**
  - c/op_160 / cpp/op_124 -- **core difference**
  - c/op_160 / cpp/op_160 -- **total equality**
  - c/op_160 / cpp/op_196 -- **core difference**
  - c/op_160 / cpp/op_232 -- **core difference**
  - c/op_160 / cpp/op_484 -- **core difference**
  - c/op_160 / cpp/op_520 -- **core difference**
  - c/op_160 / cpp/op_988 -- **core difference**
  - c/op_196 / cpp/op_124 -- **core difference**
  - c/op_196 / cpp/op_160 -- **core difference**
  - c/op_196 / cpp/op_196 -- **total equality**
  - c/op_196 / cpp/op_232 -- **core difference**
  - c/op_196 / cpp/op_484 -- **core difference**
  - c/op_196 / cpp/op_520 -- **core difference**
  - c/op_196 / cpp/op_988 -- **core difference**
  - c/op_232 / cpp/op_124 -- **core difference**
  - c/op_232 / cpp/op_160 -- **core difference**
  - c/op_232 / cpp/op_196 -- **core difference**
  - c/op_232 / cpp/op_232 -- **total equality**
  - c/op_232 / cpp/op_484 -- **core difference**
  - c/op_232 / cpp/op_520 -- **core difference**
  - c/op_232 / cpp/op_988 -- **core difference**
  - c/op_484 / cpp/op_124 -- **core difference**
  - c/op_484 / cpp/op_160 -- **core difference**
  - c/op_484 / cpp/op_196 -- **core difference**
  - c/op_484 / cpp/op_232 -- **core difference**
  - c/op_484 / cpp/op_484 -- **total equality**
  - c/op_484 / cpp/op_520 -- **core difference**
  - c/op_484 / cpp/op_988 -- **core difference**
  - c/op_520 / cpp/op_124 -- **core difference**
  - c/op_520 / cpp/op_160 -- **core difference**
  - c/op_520 / cpp/op_196 -- **core difference**
  - c/op_520 / cpp/op_232 -- **core difference**
  - c/op_520 / cpp/op_484 -- **core difference**
  - c/op_520 / cpp/op_520 -- **total equality**
  - c/op_520 / cpp/op_988 -- **total equality**

### shared-core group ex64@0(ins@0(in0:256,F32toF64(ex32@0(in0:256)))) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `>` (f32,f64, 0 modes); c `>=` (f32,f64, 0 modes); c `<=` (f32,f64, 0 modes); c `<` (f32,f64, 0 modes); cpp `>` (f32,f64, 0 modes); cpp `>=` (f32,f64, 0 modes); cpp `<=` (f32,f64, 0 modes); cpp `<` (f32,f64, 0 modes); cpp `<=>` (f32,f64, 0 modes)

  - c/op_556 / cpp/op_556 -- **core difference**
  - c/op_556 / cpp/op_592 -- **core difference**
  - c/op_556 / cpp/op_628 -- **core difference**
  - c/op_556 / cpp/op_664 -- **core difference**
  - c/op_556 / cpp/op_772 -- **core difference**
  - c/op_592 / cpp/op_556 -- **core difference**
  - c/op_592 / cpp/op_592 -- **core difference**
  - c/op_592 / cpp/op_628 -- **core difference**
  - c/op_592 / cpp/op_664 -- **core difference**
  - c/op_592 / cpp/op_772 -- **core difference**
  - c/op_628 / cpp/op_556 -- **core difference**
  - c/op_628 / cpp/op_592 -- **core difference**
  - c/op_628 / cpp/op_628 -- **core difference**
  - c/op_628 / cpp/op_664 -- **core difference**
  - c/op_628 / cpp/op_772 -- **core difference**
  - c/op_664 / cpp/op_556 -- **core difference**
  - c/op_664 / cpp/op_592 -- **core difference**
  - c/op_664 / cpp/op_628 -- **core difference**
  - c/op_664 / cpp/op_664 -- **core difference**
  - c/op_664 / cpp/op_772 -- **core difference**

### shared-core group ins@0(in0:256,F32toF64(ex32@0(in0:256))) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `+` (f32,f64, 0 modes); c `-` (f32,f64, 0 modes); c `*` (f32,f64, 0 modes); c `/` (f32,f64, 0 modes); c `==` (f32,f64, 0 modes); c `!=` (f32,f64, 0 modes); c `>` (f32,f64, 0 modes); c `>=` (f32,f64, 0 modes); c `<=` (f32,f64, 0 modes); c `<` (f32,f64, 0 modes); cpp `+` (f32,f64, 0 modes); cpp `-` (f32,f64, 0 modes); cpp `*` (f32,f64, 0 modes); cpp `/` (f32,f64, 0 modes); cpp `==` (f32,f64, 0 modes); cpp `!=` (f32,f64, 0 modes); cpp `>` (f32,f64, 0 modes); cpp `>=` (f32,f64, 0 modes); cpp `<=` (f32,f64, 0 modes); cpp `<` (f32,f64, 0 modes); cpp `<=>` (f32,f64, 0 modes); cpp `not_eq` (f32,f64, 0 modes)

  - c/op_124 / cpp/op_124 -- **total equality**
  - c/op_124 / cpp/op_160 -- **core difference**
  - c/op_124 / cpp/op_196 -- **core difference**
  - c/op_124 / cpp/op_232 -- **core difference**
  - c/op_124 / cpp/op_484 -- **core difference**
  - c/op_124 / cpp/op_520 -- **core difference**
  - c/op_124 / cpp/op_556 -- **core difference**
  - c/op_124 / cpp/op_592 -- **core difference**
  - c/op_124 / cpp/op_628 -- **core difference**
  - c/op_124 / cpp/op_664 -- **core difference**
  - c/op_124 / cpp/op_772 -- **core difference**
  - c/op_124 / cpp/op_988 -- **core difference**
  - c/op_160 / cpp/op_124 -- **core difference**
  - c/op_160 / cpp/op_160 -- **total equality**
  - c/op_160 / cpp/op_196 -- **core difference**
  - c/op_160 / cpp/op_232 -- **core difference**
  - c/op_160 / cpp/op_484 -- **core difference**
  - c/op_160 / cpp/op_520 -- **core difference**
  - c/op_160 / cpp/op_556 -- **core difference**
  - c/op_160 / cpp/op_592 -- **core difference**
  - c/op_160 / cpp/op_628 -- **core difference**
  - c/op_160 / cpp/op_664 -- **core difference**
  - c/op_160 / cpp/op_772 -- **core difference**
  - c/op_160 / cpp/op_988 -- **core difference**
  - c/op_196 / cpp/op_124 -- **core difference**
  - c/op_196 / cpp/op_160 -- **core difference**
  - c/op_196 / cpp/op_196 -- **total equality**
  - c/op_196 / cpp/op_232 -- **core difference**
  - c/op_196 / cpp/op_484 -- **core difference**
  - c/op_196 / cpp/op_520 -- **core difference**
  - c/op_196 / cpp/op_556 -- **core difference**
  - c/op_196 / cpp/op_592 -- **core difference**
  - c/op_196 / cpp/op_628 -- **core difference**
  - c/op_196 / cpp/op_664 -- **core difference**
  - c/op_196 / cpp/op_772 -- **core difference**
  - c/op_196 / cpp/op_988 -- **core difference**
  - c/op_232 / cpp/op_124 -- **core difference**
  - c/op_232 / cpp/op_160 -- **core difference**
  - c/op_232 / cpp/op_196 -- **core difference**
  - c/op_232 / cpp/op_232 -- **total equality**
  - c/op_232 / cpp/op_484 -- **core difference**
  - c/op_232 / cpp/op_520 -- **core difference**
  - c/op_232 / cpp/op_556 -- **core difference**
  - c/op_232 / cpp/op_592 -- **core difference**
  - c/op_232 / cpp/op_628 -- **core difference**
  - c/op_232 / cpp/op_664 -- **core difference**
  - c/op_232 / cpp/op_772 -- **core difference**
  - c/op_232 / cpp/op_988 -- **core difference**
  - c/op_484 / cpp/op_124 -- **core difference**
  - c/op_484 / cpp/op_160 -- **core difference**
  - c/op_484 / cpp/op_196 -- **core difference**
  - c/op_484 / cpp/op_232 -- **core difference**
  - c/op_484 / cpp/op_484 -- **total equality**
  - c/op_484 / cpp/op_520 -- **core difference**
  - c/op_484 / cpp/op_556 -- **core difference**
  - c/op_484 / cpp/op_592 -- **core difference**
  - c/op_484 / cpp/op_628 -- **core difference**
  - c/op_484 / cpp/op_664 -- **core difference**
  - c/op_484 / cpp/op_772 -- **core difference**
  - c/op_484 / cpp/op_988 -- **core difference**
  - c/op_520 / cpp/op_124 -- **core difference**
  - c/op_520 / cpp/op_160 -- **core difference**
  - c/op_520 / cpp/op_196 -- **core difference**
  - c/op_520 / cpp/op_232 -- **core difference**
  - c/op_520 / cpp/op_484 -- **core difference**
  - c/op_520 / cpp/op_520 -- **total equality**
  - c/op_520 / cpp/op_556 -- **core difference**
  - c/op_520 / cpp/op_592 -- **core difference**
  - c/op_520 / cpp/op_628 -- **core difference**
  - c/op_520 / cpp/op_664 -- **core difference**
  - c/op_520 / cpp/op_772 -- **core difference**
  - c/op_520 / cpp/op_988 -- **total equality**
  - c/op_556 / cpp/op_124 -- **core difference**
  - c/op_556 / cpp/op_160 -- **core difference**
  - c/op_556 / cpp/op_196 -- **core difference**
  - c/op_556 / cpp/op_232 -- **core difference**
  - c/op_556 / cpp/op_484 -- **core difference**
  - c/op_556 / cpp/op_520 -- **core difference**
  - c/op_556 / cpp/op_556 -- **core difference**
  - c/op_556 / cpp/op_592 -- **core difference**
  - c/op_556 / cpp/op_628 -- **core difference**
  - c/op_556 / cpp/op_664 -- **core difference**
  - c/op_556 / cpp/op_772 -- **core difference**
  - c/op_556 / cpp/op_988 -- **core difference**
  - c/op_592 / cpp/op_124 -- **core difference**
  - c/op_592 / cpp/op_160 -- **core difference**
  - c/op_592 / cpp/op_196 -- **core difference**
  - c/op_592 / cpp/op_232 -- **core difference**
  - c/op_592 / cpp/op_484 -- **core difference**
  - c/op_592 / cpp/op_520 -- **core difference**
  - c/op_592 / cpp/op_556 -- **core difference**
  - c/op_592 / cpp/op_592 -- **core difference**
  - c/op_592 / cpp/op_628 -- **core difference**
  - c/op_592 / cpp/op_664 -- **core difference**
  - c/op_592 / cpp/op_772 -- **core difference**
  - c/op_592 / cpp/op_988 -- **core difference**
  - c/op_628 / cpp/op_124 -- **core difference**
  - c/op_628 / cpp/op_160 -- **core difference**
  - c/op_628 / cpp/op_196 -- **core difference**
  - c/op_628 / cpp/op_232 -- **core difference**
  - c/op_628 / cpp/op_484 -- **core difference**
  - c/op_628 / cpp/op_520 -- **core difference**
  - c/op_628 / cpp/op_556 -- **core difference**
  - c/op_628 / cpp/op_592 -- **core difference**
  - c/op_628 / cpp/op_628 -- **core difference**
  - c/op_628 / cpp/op_664 -- **core difference**
  - c/op_628 / cpp/op_772 -- **core difference**
  - c/op_628 / cpp/op_988 -- **core difference**
  - c/op_664 / cpp/op_124 -- **core difference**
  - c/op_664 / cpp/op_160 -- **core difference**
  - c/op_664 / cpp/op_196 -- **core difference**
  - c/op_664 / cpp/op_232 -- **core difference**
  - c/op_664 / cpp/op_484 -- **core difference**
  - c/op_664 / cpp/op_520 -- **core difference**
  - c/op_664 / cpp/op_556 -- **core difference**
  - c/op_664 / cpp/op_592 -- **core difference**
  - c/op_664 / cpp/op_628 -- **core difference**
  - c/op_664 / cpp/op_664 -- **core difference**
  - c/op_664 / cpp/op_772 -- **core difference**
  - c/op_664 / cpp/op_988 -- **core difference**

### shared-core group F32toF64(ex32@0(in0:256)) · (f32,f64)

- ground: connection
- languages: c, cpp
- members: c `+` (f32,f64, 0 modes); c `-` (f32,f64, 0 modes); c `*` (f32,f64, 0 modes); c `/` (f32,f64, 0 modes); c `||` (f32,f64, 0 modes); c `&&` (f32,f64, 0 modes); c `==` (f32,f64, 0 modes); c `!=` (f32,f64, 0 modes); c `>` (f32,f64, 0 modes); c `>=` (f32,f64, 0 modes); c `<=` (f32,f64, 0 modes); c `<` (f32,f64, 0 modes); cpp `+` (f32,f64, 0 modes); cpp `-` (f32,f64, 0 modes); cpp `*` (f32,f64, 0 modes); cpp `/` (f32,f64, 0 modes); cpp `||` (f32,f64, 0 modes); cpp `&&` (f32,f64, 0 modes); cpp `==` (f32,f64, 0 modes); cpp `!=` (f32,f64, 0 modes); cpp `>` (f32,f64, 0 modes); cpp `>=` (f32,f64, 0 modes); cpp `<=` (f32,f64, 0 modes); cpp `<` (f32,f64, 0 modes); cpp `<=>` (f32,f64, 0 modes); cpp `or` (f32,f64, 0 modes); cpp `and` (f32,f64, 0 modes); cpp `not_eq` (f32,f64, 0 modes)

  - c/op_124 / cpp/op_124 -- **total equality**
  - c/op_124 / cpp/op_160 -- **core difference**
  - c/op_124 / cpp/op_196 -- **core difference**
  - c/op_124 / cpp/op_232 -- **core difference**
  - c/op_124 / cpp/op_304 -- **core difference**
  - c/op_124 / cpp/op_340 -- **core difference**
  - c/op_124 / cpp/op_484 -- **core difference**
  - c/op_124 / cpp/op_520 -- **core difference**
  - c/op_124 / cpp/op_556 -- **core difference**
  - c/op_124 / cpp/op_592 -- **core difference**
  - c/op_124 / cpp/op_628 -- **core difference**
  - c/op_124 / cpp/op_664 -- **core difference**
  - c/op_124 / cpp/op_772 -- **core difference**
  - c/op_124 / cpp/op_808 -- **core difference**
  - c/op_124 / cpp/op_844 -- **core difference**
  - c/op_124 / cpp/op_988 -- **core difference**
  - c/op_160 / cpp/op_124 -- **core difference**
  - c/op_160 / cpp/op_160 -- **total equality**
  - c/op_160 / cpp/op_196 -- **core difference**
  - c/op_160 / cpp/op_232 -- **core difference**
  - c/op_160 / cpp/op_304 -- **core difference**
  - c/op_160 / cpp/op_340 -- **core difference**
  - c/op_160 / cpp/op_484 -- **core difference**
  - c/op_160 / cpp/op_520 -- **core difference**
  - c/op_160 / cpp/op_556 -- **core difference**
  - c/op_160 / cpp/op_592 -- **core difference**
  - c/op_160 / cpp/op_628 -- **core difference**
  - c/op_160 / cpp/op_664 -- **core difference**
  - c/op_160 / cpp/op_772 -- **core difference**
  - c/op_160 / cpp/op_808 -- **core difference**
  - c/op_160 / cpp/op_844 -- **core difference**
  - c/op_160 / cpp/op_988 -- **core difference**
  - c/op_196 / cpp/op_124 -- **core difference**
  - c/op_196 / cpp/op_160 -- **core difference**
  - c/op_196 / cpp/op_196 -- **total equality**
  - c/op_196 / cpp/op_232 -- **core difference**
  - c/op_196 / cpp/op_304 -- **core difference**
  - c/op_196 / cpp/op_340 -- **core difference**
  - c/op_196 / cpp/op_484 -- **core difference**
  - c/op_196 / cpp/op_520 -- **core difference**
  - c/op_196 / cpp/op_556 -- **core difference**
  - c/op_196 / cpp/op_592 -- **core difference**
  - c/op_196 / cpp/op_628 -- **core difference**
  - c/op_196 / cpp/op_664 -- **core difference**
  - c/op_196 / cpp/op_772 -- **core difference**
  - c/op_196 / cpp/op_808 -- **core difference**
  - c/op_196 / cpp/op_844 -- **core difference**
  - c/op_196 / cpp/op_988 -- **core difference**
  - c/op_232 / cpp/op_124 -- **core difference**
  - c/op_232 / cpp/op_160 -- **core difference**
  - c/op_232 / cpp/op_196 -- **core difference**
  - c/op_232 / cpp/op_232 -- **total equality**
  - c/op_232 / cpp/op_304 -- **core difference**
  - c/op_232 / cpp/op_340 -- **core difference**
  - c/op_232 / cpp/op_484 -- **core difference**
  - c/op_232 / cpp/op_520 -- **core difference**
  - c/op_232 / cpp/op_556 -- **core difference**
  - c/op_232 / cpp/op_592 -- **core difference**
  - c/op_232 / cpp/op_628 -- **core difference**
  - c/op_232 / cpp/op_664 -- **core difference**
  - c/op_232 / cpp/op_772 -- **core difference**
  - c/op_232 / cpp/op_808 -- **core difference**
  - c/op_232 / cpp/op_844 -- **core difference**
  - c/op_232 / cpp/op_988 -- **core difference**
  - c/op_304 / cpp/op_124 -- **core difference**
  - c/op_304 / cpp/op_160 -- **core difference**
  - c/op_304 / cpp/op_196 -- **core difference**
  - c/op_304 / cpp/op_232 -- **core difference**
  - c/op_304 / cpp/op_304 -- **core difference**
  - c/op_304 / cpp/op_340 -- **core difference**
  - c/op_304 / cpp/op_484 -- **core difference**
  - c/op_304 / cpp/op_520 -- **core difference**
  - c/op_304 / cpp/op_556 -- **core difference**
  - c/op_304 / cpp/op_592 -- **core difference**
  - c/op_304 / cpp/op_628 -- **core difference**
  - c/op_304 / cpp/op_664 -- **core difference**
  - c/op_304 / cpp/op_772 -- **core difference**
  - c/op_304 / cpp/op_808 -- **core difference**
  - c/op_304 / cpp/op_844 -- **core difference**
  - c/op_304 / cpp/op_988 -- **core difference**
  - c/op_340 / cpp/op_124 -- **core difference**
  - c/op_340 / cpp/op_160 -- **core difference**
  - c/op_340 / cpp/op_196 -- **core difference**
  - c/op_340 / cpp/op_232 -- **core difference**
  - c/op_340 / cpp/op_304 -- **core difference**
  - c/op_340 / cpp/op_340 -- **core difference**
  - c/op_340 / cpp/op_484 -- **core difference**
  - c/op_340 / cpp/op_520 -- **core difference**
  - c/op_340 / cpp/op_556 -- **core difference**
  - c/op_340 / cpp/op_592 -- **core difference**
  - c/op_340 / cpp/op_628 -- **core difference**
  - c/op_340 / cpp/op_664 -- **core difference**
  - c/op_340 / cpp/op_772 -- **core difference**
  - c/op_340 / cpp/op_808 -- **core difference**
  - c/op_340 / cpp/op_844 -- **core difference**
  - c/op_340 / cpp/op_988 -- **core difference**
  - c/op_484 / cpp/op_124 -- **core difference**
  - c/op_484 / cpp/op_160 -- **core difference**
  - c/op_484 / cpp/op_196 -- **core difference**
  - c/op_484 / cpp/op_232 -- **core difference**
  - c/op_484 / cpp/op_304 -- **core difference**
  - c/op_484 / cpp/op_340 -- **core difference**
  - c/op_484 / cpp/op_484 -- **total equality**
  - c/op_484 / cpp/op_520 -- **core difference**
  - c/op_484 / cpp/op_556 -- **core difference**
  - c/op_484 / cpp/op_592 -- **core difference**
  - c/op_484 / cpp/op_628 -- **core difference**
  - c/op_484 / cpp/op_664 -- **core difference**
  - c/op_484 / cpp/op_772 -- **core difference**
  - c/op_484 / cpp/op_808 -- **core difference**
  - c/op_484 / cpp/op_844 -- **core difference**
  - c/op_484 / cpp/op_988 -- **core difference**
  - c/op_520 / cpp/op_124 -- **core difference**
  - c/op_520 / cpp/op_160 -- **core difference**
  - c/op_520 / cpp/op_196 -- **core difference**
  - c/op_520 / cpp/op_232 -- **core difference**
  - c/op_520 / cpp/op_304 -- **core difference**
  - c/op_520 / cpp/op_340 -- **core difference**
  - c/op_520 / cpp/op_484 -- **core difference**
  - c/op_520 / cpp/op_520 -- **total equality**
  - c/op_520 / cpp/op_556 -- **core difference**
  - c/op_520 / cpp/op_592 -- **core difference**
  - c/op_520 / cpp/op_628 -- **core difference**
  - c/op_520 / cpp/op_664 -- **core difference**
  - c/op_520 / cpp/op_772 -- **core difference**
  - c/op_520 / cpp/op_808 -- **core difference**
  - c/op_520 / cpp/op_844 -- **core difference**
  - c/op_520 / cpp/op_988 -- **total equality**
  - c/op_556 / cpp/op_124 -- **core difference**
  - c/op_556 / cpp/op_160 -- **core difference**
  - c/op_556 / cpp/op_196 -- **core difference**
  - c/op_556 / cpp/op_232 -- **core difference**
  - c/op_556 / cpp/op_304 -- **core difference**
  - c/op_556 / cpp/op_340 -- **core difference**
  - c/op_556 / cpp/op_484 -- **core difference**
  - c/op_556 / cpp/op_520 -- **core difference**
  - c/op_556 / cpp/op_556 -- **core difference**
  - c/op_556 / cpp/op_592 -- **core difference**
  - c/op_556 / cpp/op_628 -- **core difference**
  - c/op_556 / cpp/op_664 -- **core difference**
  - c/op_556 / cpp/op_772 -- **core difference**
  - c/op_556 / cpp/op_808 -- **core difference**
  - c/op_556 / cpp/op_844 -- **core difference**
  - c/op_556 / cpp/op_988 -- **core difference**
  - c/op_592 / cpp/op_124 -- **core difference**
  - c/op_592 / cpp/op_160 -- **core difference**
  - c/op_592 / cpp/op_196 -- **core difference**
  - c/op_592 / cpp/op_232 -- **core difference**
  - c/op_592 / cpp/op_304 -- **core difference**
  - c/op_592 / cpp/op_340 -- **core difference**
  - c/op_592 / cpp/op_484 -- **core difference**
  - c/op_592 / cpp/op_520 -- **core difference**
  - c/op_592 / cpp/op_556 -- **core difference**
  - c/op_592 / cpp/op_592 -- **core difference**
  - c/op_592 / cpp/op_628 -- **core difference**
  - c/op_592 / cpp/op_664 -- **core difference**
  - c/op_592 / cpp/op_772 -- **core difference**
  - c/op_592 / cpp/op_808 -- **core difference**
  - c/op_592 / cpp/op_844 -- **core difference**
  - c/op_592 / cpp/op_988 -- **core difference**
  - c/op_628 / cpp/op_124 -- **core difference**
  - c/op_628 / cpp/op_160 -- **core difference**
  - c/op_628 / cpp/op_196 -- **core difference**
  - c/op_628 / cpp/op_232 -- **core difference**
  - c/op_628 / cpp/op_304 -- **core difference**
  - c/op_628 / cpp/op_340 -- **core difference**
  - c/op_628 / cpp/op_484 -- **core difference**
  - c/op_628 / cpp/op_520 -- **core difference**
  - c/op_628 / cpp/op_556 -- **core difference**
  - c/op_628 / cpp/op_592 -- **core difference**
  - c/op_628 / cpp/op_628 -- **core difference**
  - c/op_628 / cpp/op_664 -- **core difference**
  - c/op_628 / cpp/op_772 -- **core difference**
  - c/op_628 / cpp/op_808 -- **core difference**
  - c/op_628 / cpp/op_844 -- **core difference**
  - c/op_628 / cpp/op_988 -- **core difference**
  - c/op_664 / cpp/op_124 -- **core difference**
  - c/op_664 / cpp/op_160 -- **core difference**
  - c/op_664 / cpp/op_196 -- **core difference**
  - c/op_664 / cpp/op_232 -- **core difference**
  - c/op_664 / cpp/op_304 -- **core difference**
  - c/op_664 / cpp/op_340 -- **core difference**
  - c/op_664 / cpp/op_484 -- **core difference**
  - c/op_664 / cpp/op_520 -- **core difference**
  - c/op_664 / cpp/op_556 -- **core difference**
  - c/op_664 / cpp/op_592 -- **core difference**
  - c/op_664 / cpp/op_628 -- **core difference**
  - c/op_664 / cpp/op_664 -- **core difference**
  - c/op_664 / cpp/op_772 -- **core difference**
  - c/op_664 / cpp/op_808 -- **core difference**
  - c/op_664 / cpp/op_844 -- **core difference**
  - c/op_664 / cpp/op_988 -- **core difference**

### shared-core group And8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64)))) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `&&` (f32,i32, 0 modes); cpp `&&` (f32,i32, 0 modes); cpp `and` (f32,i32, 0 modes)

  - c/op_336 / cpp/op_336 -- **core difference**
  - c/op_336 / cpp/op_840 -- **core difference**

### shared-core group Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64)))) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `||` (f32,i32, 0 modes); cpp `||` (f32,i32, 0 modes); cpp `or` (f32,i32, 0 modes)

  - c/op_300 / cpp/op_300 -- **core difference**
  - c/op_300 / cpp/op_804 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64)))) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `||` (f32,i32, 0 modes); c `&&` (f32,i32, 0 modes); cpp `||` (f32,i32, 0 modes); cpp `&&` (f32,i32, 0 modes); cpp `or` (f32,i32, 0 modes); cpp `and` (f32,i32, 0 modes)

  - c/op_300 / cpp/op_300 -- **core difference**
  - c/op_300 / cpp/op_336 -- **core difference**
  - c/op_300 / cpp/op_804 -- **core difference**
  - c/op_300 / cpp/op_840 -- **core difference**
  - c/op_336 / cpp/op_300 -- **core difference**
  - c/op_336 / cpp/op_336 -- **core difference**
  - c/op_336 / cpp/op_804 -- **core difference**
  - c/op_336 / cpp/op_840 -- **core difference**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64)))),CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))),ex128@0(in0:256)))))) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `==` (f32,i32, 0 modes); cpp `==` (f32,i32, 0 modes)

  - c/op_480 / cpp/op_480 -- **total equality**

### shared-core group ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64)))),XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))),ex128@0(in0:256)))) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `!=` (f32,i32, 0 modes); cpp `!=` (f32,i32, 0 modes); cpp `not_eq` (f32,i32, 0 modes)

  - c/op_516 / cpp/op_516 -- **total equality**
  - c/op_516 / cpp/op_984 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in1:64))))))),0:64,u1:64))) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `>` (f32,i32, 0 modes); cpp `>` (f32,i32, 0 modes)

  - c/op_552 / cpp/op_552 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in1:64))))))),0:64,u1:64))) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `>=` (f32,i32, 0 modes); cpp `>=` (f32,i32, 0 modes)

  - c/op_588 / cpp/op_588 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in1:64)))),F32toF64(ex32@0(in0:256))))),0:64,u1:64))) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `<=` (f32,i32, 0 modes); cpp `<=` (f32,i32, 0 modes)

  - c/op_624 / cpp/op_624 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in1:64)))),F32toF64(ex32@0(in0:256))))),0:64,u1:64))) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `<` (f32,i32, 0 modes); cpp `<` (f32,i32, 0 modes)

  - c/op_660 / cpp/op_660 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in1:64))))))) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `>` (f32,i32, 0 modes); c `>=` (f32,i32, 0 modes); cpp `>` (f32,i32, 0 modes); cpp `>=` (f32,i32, 0 modes); cpp `<=>` (f32,i32, 0 modes)

  - c/op_552 / cpp/op_552 -- **core difference**
  - c/op_552 / cpp/op_588 -- **core difference**
  - c/op_552 / cpp/op_768 -- **core difference**
  - c/op_588 / cpp/op_552 -- **core difference**
  - c/op_588 / cpp/op_588 -- **core difference**
  - c/op_588 / cpp/op_768 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in1:64)))),F32toF64(ex32@0(in0:256))))) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `<=` (f32,i32, 0 modes); c `<` (f32,i32, 0 modes); cpp `<=` (f32,i32, 0 modes); cpp `<` (f32,i32, 0 modes); cpp `<=>` (f32,i32, 0 modes)

  - c/op_624 / cpp/op_624 -- **core difference**
  - c/op_624 / cpp/op_660 -- **core difference**
  - c/op_624 / cpp/op_768 -- **core difference**
  - c/op_660 / cpp/op_624 -- **core difference**
  - c/op_660 / cpp/op_660 -- **core difference**
  - c/op_660 / cpp/op_768 -- **core difference**

### shared-core group CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))),ex128@0(in0:256)) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `==` (f32,i32, 0 modes); c `!=` (f32,i32, 0 modes); cpp `==` (f32,i32, 0 modes); cpp `!=` (f32,i32, 0 modes); cpp `not_eq` (f32,i32, 0 modes)

  - c/op_480 / cpp/op_480 -- **total equality**
  - c/op_480 / cpp/op_516 -- **core difference**
  - c/op_480 / cpp/op_984 -- **core difference**
  - c/op_516 / cpp/op_480 -- **core difference**
  - c/op_516 / cpp/op_516 -- **total equality**
  - c/op_516 / cpp/op_984 -- **total equality**

### shared-core group Add32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64)))))) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `+` (f32,i32, 0 modes); cpp `+` (f32,i32, 0 modes)

  - c/op_120 / cpp/op_120 -- **total equality**

### shared-core group Sub32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64)))))) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `-` (f32,i32, 0 modes); cpp `-` (f32,i32, 0 modes)

  - c/op_156 / cpp/op_156 -- **total equality**

### shared-core group Mul32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64)))))) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `*` (f32,i32, 0 modes); cpp `*` (f32,i32, 0 modes)

  - c/op_192 / cpp/op_192 -- **total equality**

### shared-core group Div32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64)))))) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `/` (f32,i32, 0 modes); cpp `/` (f32,i32, 0 modes)

  - c/op_228 / cpp/op_228 -- **total equality**

### shared-core group ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in1:64))))) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `+` (f32,i32, 0 modes); c `-` (f32,i32, 0 modes); c `*` (f32,i32, 0 modes); c `/` (f32,i32, 0 modes); c `==` (f32,i32, 0 modes); c `!=` (f32,i32, 0 modes); cpp `+` (f32,i32, 0 modes); cpp `-` (f32,i32, 0 modes); cpp `*` (f32,i32, 0 modes); cpp `/` (f32,i32, 0 modes); cpp `==` (f32,i32, 0 modes); cpp `!=` (f32,i32, 0 modes); cpp `not_eq` (f32,i32, 0 modes)

  - c/op_120 / cpp/op_120 -- **total equality**
  - c/op_120 / cpp/op_156 -- **core difference**
  - c/op_120 / cpp/op_192 -- **core difference**
  - c/op_120 / cpp/op_228 -- **core difference**
  - c/op_120 / cpp/op_480 -- **core difference**
  - c/op_120 / cpp/op_516 -- **core difference**
  - c/op_120 / cpp/op_984 -- **core difference**
  - c/op_156 / cpp/op_120 -- **core difference**
  - c/op_156 / cpp/op_156 -- **total equality**
  - c/op_156 / cpp/op_192 -- **core difference**
  - c/op_156 / cpp/op_228 -- **core difference**
  - c/op_156 / cpp/op_480 -- **core difference**
  - c/op_156 / cpp/op_516 -- **core difference**
  - c/op_156 / cpp/op_984 -- **core difference**
  - c/op_192 / cpp/op_120 -- **core difference**
  - c/op_192 / cpp/op_156 -- **core difference**
  - c/op_192 / cpp/op_192 -- **total equality**
  - c/op_192 / cpp/op_228 -- **core difference**
  - c/op_192 / cpp/op_480 -- **core difference**
  - c/op_192 / cpp/op_516 -- **core difference**
  - c/op_192 / cpp/op_984 -- **core difference**
  - c/op_228 / cpp/op_120 -- **core difference**
  - c/op_228 / cpp/op_156 -- **core difference**
  - c/op_228 / cpp/op_192 -- **core difference**
  - c/op_228 / cpp/op_228 -- **total equality**
  - c/op_228 / cpp/op_480 -- **core difference**
  - c/op_228 / cpp/op_516 -- **core difference**
  - c/op_228 / cpp/op_984 -- **core difference**
  - c/op_480 / cpp/op_120 -- **core difference**
  - c/op_480 / cpp/op_156 -- **core difference**
  - c/op_480 / cpp/op_192 -- **core difference**
  - c/op_480 / cpp/op_228 -- **core difference**
  - c/op_480 / cpp/op_480 -- **total equality**
  - c/op_480 / cpp/op_516 -- **core difference**
  - c/op_480 / cpp/op_984 -- **core difference**
  - c/op_516 / cpp/op_120 -- **core difference**
  - c/op_516 / cpp/op_156 -- **core difference**
  - c/op_516 / cpp/op_192 -- **core difference**
  - c/op_516 / cpp/op_228 -- **core difference**
  - c/op_516 / cpp/op_480 -- **core difference**
  - c/op_516 / cpp/op_516 -- **total equality**
  - c/op_516 / cpp/op_984 -- **total equality**

### shared-core group F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in1:64)))) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `>` (f32,i32, 0 modes); c `>=` (f32,i32, 0 modes); c `<=` (f32,i32, 0 modes); c `<` (f32,i32, 0 modes); cpp `>` (f32,i32, 0 modes); cpp `>=` (f32,i32, 0 modes); cpp `<=` (f32,i32, 0 modes); cpp `<` (f32,i32, 0 modes); cpp `<=>` (f32,i32, 0 modes)

  - c/op_552 / cpp/op_552 -- **core difference**
  - c/op_552 / cpp/op_588 -- **core difference**
  - c/op_552 / cpp/op_624 -- **core difference**
  - c/op_552 / cpp/op_660 -- **core difference**
  - c/op_552 / cpp/op_768 -- **core difference**
  - c/op_588 / cpp/op_552 -- **core difference**
  - c/op_588 / cpp/op_588 -- **core difference**
  - c/op_588 / cpp/op_624 -- **core difference**
  - c/op_588 / cpp/op_660 -- **core difference**
  - c/op_588 / cpp/op_768 -- **core difference**
  - c/op_624 / cpp/op_552 -- **core difference**
  - c/op_624 / cpp/op_588 -- **core difference**
  - c/op_624 / cpp/op_624 -- **core difference**
  - c/op_624 / cpp/op_660 -- **core difference**
  - c/op_624 / cpp/op_768 -- **core difference**
  - c/op_660 / cpp/op_552 -- **core difference**
  - c/op_660 / cpp/op_588 -- **core difference**
  - c/op_660 / cpp/op_624 -- **core difference**
  - c/op_660 / cpp/op_660 -- **core difference**
  - c/op_660 / cpp/op_768 -- **core difference**

### shared-core group I32StoF64(ex32@0(in1:64)) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `+` (f32,i32, 0 modes); c `-` (f32,i32, 0 modes); c `*` (f32,i32, 0 modes); c `/` (f32,i32, 0 modes); c `==` (f32,i32, 0 modes); c `!=` (f32,i32, 0 modes); c `>` (f32,i32, 0 modes); c `>=` (f32,i32, 0 modes); c `<=` (f32,i32, 0 modes); c `<` (f32,i32, 0 modes); cpp `+` (f32,i32, 0 modes); cpp `-` (f32,i32, 0 modes); cpp `*` (f32,i32, 0 modes); cpp `/` (f32,i32, 0 modes); cpp `==` (f32,i32, 0 modes); cpp `!=` (f32,i32, 0 modes); cpp `>` (f32,i32, 0 modes); cpp `>=` (f32,i32, 0 modes); cpp `<=` (f32,i32, 0 modes); cpp `<` (f32,i32, 0 modes); cpp `<=>` (f32,i32, 0 modes); cpp `not_eq` (f32,i32, 0 modes)

  - c/op_120 / cpp/op_120 -- **total equality**
  - c/op_120 / cpp/op_156 -- **core difference**
  - c/op_120 / cpp/op_192 -- **core difference**
  - c/op_120 / cpp/op_228 -- **core difference**
  - c/op_120 / cpp/op_480 -- **core difference**
  - c/op_120 / cpp/op_516 -- **core difference**
  - c/op_120 / cpp/op_552 -- **core difference**
  - c/op_120 / cpp/op_588 -- **core difference**
  - c/op_120 / cpp/op_624 -- **core difference**
  - c/op_120 / cpp/op_660 -- **core difference**
  - c/op_120 / cpp/op_768 -- **core difference**
  - c/op_120 / cpp/op_984 -- **core difference**
  - c/op_156 / cpp/op_120 -- **core difference**
  - c/op_156 / cpp/op_156 -- **total equality**
  - c/op_156 / cpp/op_192 -- **core difference**
  - c/op_156 / cpp/op_228 -- **core difference**
  - c/op_156 / cpp/op_480 -- **core difference**
  - c/op_156 / cpp/op_516 -- **core difference**
  - c/op_156 / cpp/op_552 -- **core difference**
  - c/op_156 / cpp/op_588 -- **core difference**
  - c/op_156 / cpp/op_624 -- **core difference**
  - c/op_156 / cpp/op_660 -- **core difference**
  - c/op_156 / cpp/op_768 -- **core difference**
  - c/op_156 / cpp/op_984 -- **core difference**
  - c/op_192 / cpp/op_120 -- **core difference**
  - c/op_192 / cpp/op_156 -- **core difference**
  - c/op_192 / cpp/op_192 -- **total equality**
  - c/op_192 / cpp/op_228 -- **core difference**
  - c/op_192 / cpp/op_480 -- **core difference**
  - c/op_192 / cpp/op_516 -- **core difference**
  - c/op_192 / cpp/op_552 -- **core difference**
  - c/op_192 / cpp/op_588 -- **core difference**
  - c/op_192 / cpp/op_624 -- **core difference**
  - c/op_192 / cpp/op_660 -- **core difference**
  - c/op_192 / cpp/op_768 -- **core difference**
  - c/op_192 / cpp/op_984 -- **core difference**
  - c/op_228 / cpp/op_120 -- **core difference**
  - c/op_228 / cpp/op_156 -- **core difference**
  - c/op_228 / cpp/op_192 -- **core difference**
  - c/op_228 / cpp/op_228 -- **total equality**
  - c/op_228 / cpp/op_480 -- **core difference**
  - c/op_228 / cpp/op_516 -- **core difference**
  - c/op_228 / cpp/op_552 -- **core difference**
  - c/op_228 / cpp/op_588 -- **core difference**
  - c/op_228 / cpp/op_624 -- **core difference**
  - c/op_228 / cpp/op_660 -- **core difference**
  - c/op_228 / cpp/op_768 -- **core difference**
  - c/op_228 / cpp/op_984 -- **core difference**
  - c/op_480 / cpp/op_120 -- **core difference**
  - c/op_480 / cpp/op_156 -- **core difference**
  - c/op_480 / cpp/op_192 -- **core difference**
  - c/op_480 / cpp/op_228 -- **core difference**
  - c/op_480 / cpp/op_480 -- **total equality**
  - c/op_480 / cpp/op_516 -- **core difference**
  - c/op_480 / cpp/op_552 -- **core difference**
  - c/op_480 / cpp/op_588 -- **core difference**
  - c/op_480 / cpp/op_624 -- **core difference**
  - c/op_480 / cpp/op_660 -- **core difference**
  - c/op_480 / cpp/op_768 -- **core difference**
  - c/op_480 / cpp/op_984 -- **core difference**
  - c/op_516 / cpp/op_120 -- **core difference**
  - c/op_516 / cpp/op_156 -- **core difference**
  - c/op_516 / cpp/op_192 -- **core difference**
  - c/op_516 / cpp/op_228 -- **core difference**
  - c/op_516 / cpp/op_480 -- **core difference**
  - c/op_516 / cpp/op_516 -- **total equality**
  - c/op_516 / cpp/op_552 -- **core difference**
  - c/op_516 / cpp/op_588 -- **core difference**
  - c/op_516 / cpp/op_624 -- **core difference**
  - c/op_516 / cpp/op_660 -- **core difference**
  - c/op_516 / cpp/op_768 -- **core difference**
  - c/op_516 / cpp/op_984 -- **total equality**
  - c/op_552 / cpp/op_120 -- **core difference**
  - c/op_552 / cpp/op_156 -- **core difference**
  - c/op_552 / cpp/op_192 -- **core difference**
  - c/op_552 / cpp/op_228 -- **core difference**
  - c/op_552 / cpp/op_480 -- **core difference**
  - c/op_552 / cpp/op_516 -- **core difference**
  - c/op_552 / cpp/op_552 -- **core difference**
  - c/op_552 / cpp/op_588 -- **core difference**
  - c/op_552 / cpp/op_624 -- **core difference**
  - c/op_552 / cpp/op_660 -- **core difference**
  - c/op_552 / cpp/op_768 -- **core difference**
  - c/op_552 / cpp/op_984 -- **core difference**
  - c/op_588 / cpp/op_120 -- **core difference**
  - c/op_588 / cpp/op_156 -- **core difference**
  - c/op_588 / cpp/op_192 -- **core difference**
  - c/op_588 / cpp/op_228 -- **core difference**
  - c/op_588 / cpp/op_480 -- **core difference**
  - c/op_588 / cpp/op_516 -- **core difference**
  - c/op_588 / cpp/op_552 -- **core difference**
  - c/op_588 / cpp/op_588 -- **core difference**
  - c/op_588 / cpp/op_624 -- **core difference**
  - c/op_588 / cpp/op_660 -- **core difference**
  - c/op_588 / cpp/op_768 -- **core difference**
  - c/op_588 / cpp/op_984 -- **core difference**
  - c/op_624 / cpp/op_120 -- **core difference**
  - c/op_624 / cpp/op_156 -- **core difference**
  - c/op_624 / cpp/op_192 -- **core difference**
  - c/op_624 / cpp/op_228 -- **core difference**
  - c/op_624 / cpp/op_480 -- **core difference**
  - c/op_624 / cpp/op_516 -- **core difference**
  - c/op_624 / cpp/op_552 -- **core difference**
  - c/op_624 / cpp/op_588 -- **core difference**
  - c/op_624 / cpp/op_624 -- **core difference**
  - c/op_624 / cpp/op_660 -- **core difference**
  - c/op_624 / cpp/op_768 -- **core difference**
  - c/op_624 / cpp/op_984 -- **core difference**
  - c/op_660 / cpp/op_120 -- **core difference**
  - c/op_660 / cpp/op_156 -- **core difference**
  - c/op_660 / cpp/op_192 -- **core difference**
  - c/op_660 / cpp/op_228 -- **core difference**
  - c/op_660 / cpp/op_480 -- **core difference**
  - c/op_660 / cpp/op_516 -- **core difference**
  - c/op_660 / cpp/op_552 -- **core difference**
  - c/op_660 / cpp/op_588 -- **core difference**
  - c/op_660 / cpp/op_624 -- **core difference**
  - c/op_660 / cpp/op_660 -- **core difference**
  - c/op_660 / cpp/op_768 -- **core difference**
  - c/op_660 / cpp/op_984 -- **core difference**

### shared-core group F32toF64(ex32@0(in0:256)) · (f32,i32)

- ground: connection
- languages: c, cpp
- members: c `||` (f32,i32, 0 modes); c `&&` (f32,i32, 0 modes); c `>` (f32,i32, 0 modes); c `>=` (f32,i32, 0 modes); c `<=` (f32,i32, 0 modes); c `<` (f32,i32, 0 modes); cpp `||` (f32,i32, 0 modes); cpp `&&` (f32,i32, 0 modes); cpp `>` (f32,i32, 0 modes); cpp `>=` (f32,i32, 0 modes); cpp `<=` (f32,i32, 0 modes); cpp `<` (f32,i32, 0 modes); cpp `<=>` (f32,i32, 0 modes); cpp `or` (f32,i32, 0 modes); cpp `and` (f32,i32, 0 modes)

  - c/op_300 / cpp/op_300 -- **core difference**
  - c/op_300 / cpp/op_336 -- **core difference**
  - c/op_300 / cpp/op_552 -- **core difference**
  - c/op_300 / cpp/op_588 -- **core difference**
  - c/op_300 / cpp/op_624 -- **core difference**
  - c/op_300 / cpp/op_660 -- **core difference**
  - c/op_300 / cpp/op_768 -- **core difference**
  - c/op_300 / cpp/op_804 -- **core difference**
  - c/op_300 / cpp/op_840 -- **core difference**
  - c/op_336 / cpp/op_300 -- **core difference**
  - c/op_336 / cpp/op_336 -- **core difference**
  - c/op_336 / cpp/op_552 -- **core difference**
  - c/op_336 / cpp/op_588 -- **core difference**
  - c/op_336 / cpp/op_624 -- **core difference**
  - c/op_336 / cpp/op_660 -- **core difference**
  - c/op_336 / cpp/op_768 -- **core difference**
  - c/op_336 / cpp/op_804 -- **core difference**
  - c/op_336 / cpp/op_840 -- **core difference**
  - c/op_552 / cpp/op_300 -- **core difference**
  - c/op_552 / cpp/op_336 -- **core difference**
  - c/op_552 / cpp/op_552 -- **core difference**
  - c/op_552 / cpp/op_588 -- **core difference**
  - c/op_552 / cpp/op_624 -- **core difference**
  - c/op_552 / cpp/op_660 -- **core difference**
  - c/op_552 / cpp/op_768 -- **core difference**
  - c/op_552 / cpp/op_804 -- **core difference**
  - c/op_552 / cpp/op_840 -- **core difference**
  - c/op_588 / cpp/op_300 -- **core difference**
  - c/op_588 / cpp/op_336 -- **core difference**
  - c/op_588 / cpp/op_552 -- **core difference**
  - c/op_588 / cpp/op_588 -- **core difference**
  - c/op_588 / cpp/op_624 -- **core difference**
  - c/op_588 / cpp/op_660 -- **core difference**
  - c/op_588 / cpp/op_768 -- **core difference**
  - c/op_588 / cpp/op_804 -- **core difference**
  - c/op_588 / cpp/op_840 -- **core difference**
  - c/op_624 / cpp/op_300 -- **core difference**
  - c/op_624 / cpp/op_336 -- **core difference**
  - c/op_624 / cpp/op_552 -- **core difference**
  - c/op_624 / cpp/op_588 -- **core difference**
  - c/op_624 / cpp/op_624 -- **core difference**
  - c/op_624 / cpp/op_660 -- **core difference**
  - c/op_624 / cpp/op_768 -- **core difference**
  - c/op_624 / cpp/op_804 -- **core difference**
  - c/op_624 / cpp/op_840 -- **core difference**
  - c/op_660 / cpp/op_300 -- **core difference**
  - c/op_660 / cpp/op_336 -- **core difference**
  - c/op_660 / cpp/op_552 -- **core difference**
  - c/op_660 / cpp/op_588 -- **core difference**
  - c/op_660 / cpp/op_624 -- **core difference**
  - c/op_660 / cpp/op_660 -- **core difference**
  - c/op_660 / cpp/op_768 -- **core difference**
  - c/op_660 / cpp/op_804 -- **core difference**
  - c/op_660 / cpp/op_840 -- **core difference**

### shared-core group And8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `&&` (f32,i64, 0 modes); cpp `&&` (f32,i64, 0 modes); cpp `and` (f32,i64, 0 modes)

  - c/op_337 / cpp/op_337 -- **core difference**
  - c/op_337 / cpp/op_841 -- **core difference**

### shared-core group Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `||` (f32,i64, 0 modes); cpp `||` (f32,i64, 0 modes); cpp `or` (f32,i64, 0 modes)

  - c/op_301 / cpp/op_301 -- **core difference**
  - c/op_301 / cpp/op_805 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64)))) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `||` (f32,i64, 0 modes); c `&&` (f32,i64, 0 modes); cpp `||` (f32,i64, 0 modes); cpp `&&` (f32,i64, 0 modes); cpp `or` (f32,i64, 0 modes); cpp `and` (f32,i64, 0 modes)

  - c/op_301 / cpp/op_301 -- **core difference**
  - c/op_301 / cpp/op_337 -- **core difference**
  - c/op_301 / cpp/op_805 -- **core difference**
  - c/op_301 / cpp/op_841 -- **core difference**
  - c/op_337 / cpp/op_301 -- **core difference**
  - c/op_337 / cpp/op_337 -- **core difference**
  - c/op_337 / cpp/op_805 -- **core difference**
  - c/op_337 / cpp/op_841 -- **core difference**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))),CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)))),ex128@0(in0:256)))))) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `==` (f32,i64, 0 modes); cpp `==` (f32,i64, 0 modes)

  - c/op_481 / cpp/op_481 -- **total equality**

### shared-core group ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))),XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)))),ex128@0(in0:256)))) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `!=` (f32,i64, 0 modes); cpp `!=` (f32,i64, 0 modes); cpp `not_eq` (f32,i64, 0 modes)

  - c/op_517 / cpp/op_517 -- **total equality**
  - c/op_517 / cpp/op_985 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I64StoF64(And32(3:32,ex32@0(u0:64)),in1:64)))))),0:64,u1:64))) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `>` (f32,i64, 0 modes); cpp `>` (f32,i64, 0 modes)

  - c/op_553 / cpp/op_553 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I64StoF64(And32(3:32,ex32@0(u0:64)),in1:64)))))),0:64,u1:64))) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `>=` (f32,i64, 0 modes); cpp `>=` (f32,i64, 0 modes)

  - c/op_589 / cpp/op_589 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I64StoF64(And32(3:32,ex32@0(u0:64)),in1:64))),F32toF64(ex32@0(in0:256))))),0:64,u1:64))) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `<=` (f32,i64, 0 modes); cpp `<=` (f32,i64, 0 modes)

  - c/op_625 / cpp/op_625 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I64StoF64(And32(3:32,ex32@0(u0:64)),in1:64))),F32toF64(ex32@0(in0:256))))),0:64,u1:64))) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `<` (f32,i64, 0 modes); cpp `<` (f32,i64, 0 modes)

  - c/op_661 / cpp/op_661 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I64StoF64(And32(3:32,ex32@0(u0:64)),in1:64)))))) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `>` (f32,i64, 0 modes); c `>=` (f32,i64, 0 modes); cpp `>` (f32,i64, 0 modes); cpp `>=` (f32,i64, 0 modes); cpp `<=>` (f32,i64, 0 modes)

  - c/op_553 / cpp/op_553 -- **core difference**
  - c/op_553 / cpp/op_589 -- **core difference**
  - c/op_553 / cpp/op_769 -- **core difference**
  - c/op_589 / cpp/op_553 -- **core difference**
  - c/op_589 / cpp/op_589 -- **core difference**
  - c/op_589 / cpp/op_769 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I64StoF64(And32(3:32,ex32@0(u0:64)),in1:64))),F32toF64(ex32@0(in0:256))))) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `<=` (f32,i64, 0 modes); c `<` (f32,i64, 0 modes); cpp `<=` (f32,i64, 0 modes); cpp `<` (f32,i64, 0 modes); cpp `<=>` (f32,i64, 0 modes)

  - c/op_625 / cpp/op_625 -- **core difference**
  - c/op_625 / cpp/op_661 -- **core difference**
  - c/op_625 / cpp/op_769 -- **core difference**
  - c/op_661 / cpp/op_625 -- **core difference**
  - c/op_661 / cpp/op_661 -- **core difference**
  - c/op_661 / cpp/op_769 -- **core difference**

### shared-core group CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)))),ex128@0(in0:256)) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `==` (f32,i64, 0 modes); c `!=` (f32,i64, 0 modes); cpp `==` (f32,i64, 0 modes); cpp `!=` (f32,i64, 0 modes); cpp `not_eq` (f32,i64, 0 modes)

  - c/op_481 / cpp/op_481 -- **total equality**
  - c/op_481 / cpp/op_517 -- **core difference**
  - c/op_481 / cpp/op_985 -- **core difference**
  - c/op_517 / cpp/op_481 -- **core difference**
  - c/op_517 / cpp/op_517 -- **total equality**
  - c/op_517 / cpp/op_985 -- **total equality**

### shared-core group Add32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))))) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `+` (f32,i64, 0 modes); cpp `+` (f32,i64, 0 modes)

  - c/op_121 / cpp/op_121 -- **total equality**

### shared-core group Sub32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))))) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `-` (f32,i64, 0 modes); cpp `-` (f32,i64, 0 modes)

  - c/op_157 / cpp/op_157 -- **total equality**

### shared-core group Mul32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))))) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `*` (f32,i64, 0 modes); cpp `*` (f32,i64, 0 modes)

  - c/op_193 / cpp/op_193 -- **total equality**

### shared-core group Div32F0x4(ex128@0(in0:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))))) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `/` (f32,i64, 0 modes); cpp `/` (f32,i64, 0 modes)

  - c/op_229 / cpp/op_229 -- **total equality**

### shared-core group ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)))) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `+` (f32,i64, 0 modes); c `-` (f32,i64, 0 modes); c `*` (f32,i64, 0 modes); c `/` (f32,i64, 0 modes); c `==` (f32,i64, 0 modes); c `!=` (f32,i64, 0 modes); cpp `+` (f32,i64, 0 modes); cpp `-` (f32,i64, 0 modes); cpp `*` (f32,i64, 0 modes); cpp `/` (f32,i64, 0 modes); cpp `==` (f32,i64, 0 modes); cpp `!=` (f32,i64, 0 modes); cpp `not_eq` (f32,i64, 0 modes)

  - c/op_121 / cpp/op_121 -- **total equality**
  - c/op_121 / cpp/op_157 -- **core difference**
  - c/op_121 / cpp/op_193 -- **core difference**
  - c/op_121 / cpp/op_229 -- **core difference**
  - c/op_121 / cpp/op_481 -- **core difference**
  - c/op_121 / cpp/op_517 -- **core difference**
  - c/op_121 / cpp/op_985 -- **core difference**
  - c/op_157 / cpp/op_121 -- **core difference**
  - c/op_157 / cpp/op_157 -- **total equality**
  - c/op_157 / cpp/op_193 -- **core difference**
  - c/op_157 / cpp/op_229 -- **core difference**
  - c/op_157 / cpp/op_481 -- **core difference**
  - c/op_157 / cpp/op_517 -- **core difference**
  - c/op_157 / cpp/op_985 -- **core difference**
  - c/op_193 / cpp/op_121 -- **core difference**
  - c/op_193 / cpp/op_157 -- **core difference**
  - c/op_193 / cpp/op_193 -- **total equality**
  - c/op_193 / cpp/op_229 -- **core difference**
  - c/op_193 / cpp/op_481 -- **core difference**
  - c/op_193 / cpp/op_517 -- **core difference**
  - c/op_193 / cpp/op_985 -- **core difference**
  - c/op_229 / cpp/op_121 -- **core difference**
  - c/op_229 / cpp/op_157 -- **core difference**
  - c/op_229 / cpp/op_193 -- **core difference**
  - c/op_229 / cpp/op_229 -- **total equality**
  - c/op_229 / cpp/op_481 -- **core difference**
  - c/op_229 / cpp/op_517 -- **core difference**
  - c/op_229 / cpp/op_985 -- **core difference**
  - c/op_481 / cpp/op_121 -- **core difference**
  - c/op_481 / cpp/op_157 -- **core difference**
  - c/op_481 / cpp/op_193 -- **core difference**
  - c/op_481 / cpp/op_229 -- **core difference**
  - c/op_481 / cpp/op_481 -- **total equality**
  - c/op_481 / cpp/op_517 -- **core difference**
  - c/op_481 / cpp/op_985 -- **core difference**
  - c/op_517 / cpp/op_121 -- **core difference**
  - c/op_517 / cpp/op_157 -- **core difference**
  - c/op_517 / cpp/op_193 -- **core difference**
  - c/op_517 / cpp/op_229 -- **core difference**
  - c/op_517 / cpp/op_481 -- **core difference**
  - c/op_517 / cpp/op_517 -- **total equality**
  - c/op_517 / cpp/op_985 -- **total equality**

### shared-core group F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I64StoF64(And32(3:32,ex32@0(u0:64)),in1:64))) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `>` (f32,i64, 0 modes); c `>=` (f32,i64, 0 modes); c `<=` (f32,i64, 0 modes); c `<` (f32,i64, 0 modes); cpp `>` (f32,i64, 0 modes); cpp `>=` (f32,i64, 0 modes); cpp `<=` (f32,i64, 0 modes); cpp `<` (f32,i64, 0 modes); cpp `<=>` (f32,i64, 0 modes)

  - c/op_553 / cpp/op_553 -- **core difference**
  - c/op_553 / cpp/op_589 -- **core difference**
  - c/op_553 / cpp/op_625 -- **core difference**
  - c/op_553 / cpp/op_661 -- **core difference**
  - c/op_553 / cpp/op_769 -- **core difference**
  - c/op_589 / cpp/op_553 -- **core difference**
  - c/op_589 / cpp/op_589 -- **core difference**
  - c/op_589 / cpp/op_625 -- **core difference**
  - c/op_589 / cpp/op_661 -- **core difference**
  - c/op_589 / cpp/op_769 -- **core difference**
  - c/op_625 / cpp/op_553 -- **core difference**
  - c/op_625 / cpp/op_589 -- **core difference**
  - c/op_625 / cpp/op_625 -- **core difference**
  - c/op_625 / cpp/op_661 -- **core difference**
  - c/op_625 / cpp/op_769 -- **core difference**
  - c/op_661 / cpp/op_553 -- **core difference**
  - c/op_661 / cpp/op_589 -- **core difference**
  - c/op_661 / cpp/op_625 -- **core difference**
  - c/op_661 / cpp/op_661 -- **core difference**
  - c/op_661 / cpp/op_769 -- **core difference**

### shared-core group F32toF64(ex32@0(in0:256)) · (f32,i64)

- ground: connection
- languages: c, cpp
- members: c `||` (f32,i64, 0 modes); c `&&` (f32,i64, 0 modes); c `>` (f32,i64, 0 modes); c `>=` (f32,i64, 0 modes); c `<=` (f32,i64, 0 modes); c `<` (f32,i64, 0 modes); cpp `||` (f32,i64, 0 modes); cpp `&&` (f32,i64, 0 modes); cpp `>` (f32,i64, 0 modes); cpp `>=` (f32,i64, 0 modes); cpp `<=` (f32,i64, 0 modes); cpp `<` (f32,i64, 0 modes); cpp `<=>` (f32,i64, 0 modes); cpp `or` (f32,i64, 0 modes); cpp `and` (f32,i64, 0 modes)

  - c/op_301 / cpp/op_301 -- **core difference**
  - c/op_301 / cpp/op_337 -- **core difference**
  - c/op_301 / cpp/op_553 -- **core difference**
  - c/op_301 / cpp/op_589 -- **core difference**
  - c/op_301 / cpp/op_625 -- **core difference**
  - c/op_301 / cpp/op_661 -- **core difference**
  - c/op_301 / cpp/op_769 -- **core difference**
  - c/op_301 / cpp/op_805 -- **core difference**
  - c/op_301 / cpp/op_841 -- **core difference**
  - c/op_337 / cpp/op_301 -- **core difference**
  - c/op_337 / cpp/op_337 -- **core difference**
  - c/op_337 / cpp/op_553 -- **core difference**
  - c/op_337 / cpp/op_589 -- **core difference**
  - c/op_337 / cpp/op_625 -- **core difference**
  - c/op_337 / cpp/op_661 -- **core difference**
  - c/op_337 / cpp/op_769 -- **core difference**
  - c/op_337 / cpp/op_805 -- **core difference**
  - c/op_337 / cpp/op_841 -- **core difference**
  - c/op_553 / cpp/op_301 -- **core difference**
  - c/op_553 / cpp/op_337 -- **core difference**
  - c/op_553 / cpp/op_553 -- **core difference**
  - c/op_553 / cpp/op_589 -- **core difference**
  - c/op_553 / cpp/op_625 -- **core difference**
  - c/op_553 / cpp/op_661 -- **core difference**
  - c/op_553 / cpp/op_769 -- **core difference**
  - c/op_553 / cpp/op_805 -- **core difference**
  - c/op_553 / cpp/op_841 -- **core difference**
  - c/op_589 / cpp/op_301 -- **core difference**
  - c/op_589 / cpp/op_337 -- **core difference**
  - c/op_589 / cpp/op_553 -- **core difference**
  - c/op_589 / cpp/op_589 -- **core difference**
  - c/op_589 / cpp/op_625 -- **core difference**
  - c/op_589 / cpp/op_661 -- **core difference**
  - c/op_589 / cpp/op_769 -- **core difference**
  - c/op_589 / cpp/op_805 -- **core difference**
  - c/op_589 / cpp/op_841 -- **core difference**
  - c/op_625 / cpp/op_301 -- **core difference**
  - c/op_625 / cpp/op_337 -- **core difference**
  - c/op_625 / cpp/op_553 -- **core difference**
  - c/op_625 / cpp/op_589 -- **core difference**
  - c/op_625 / cpp/op_625 -- **core difference**
  - c/op_625 / cpp/op_661 -- **core difference**
  - c/op_625 / cpp/op_769 -- **core difference**
  - c/op_625 / cpp/op_805 -- **core difference**
  - c/op_625 / cpp/op_841 -- **core difference**
  - c/op_661 / cpp/op_301 -- **core difference**
  - c/op_661 / cpp/op_337 -- **core difference**
  - c/op_661 / cpp/op_553 -- **core difference**
  - c/op_661 / cpp/op_589 -- **core difference**
  - c/op_661 / cpp/op_625 -- **core difference**
  - c/op_661 / cpp/op_661 -- **core difference**
  - c/op_661 / cpp/op_769 -- **core difference**
  - c/op_661 / cpp/op_805 -- **core difference**
  - c/op_661 / cpp/op_841 -- **core difference**

### shared-core group ins@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64))))))),Add32F0x4(ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64)))))))),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64)))))))))) · (f32,u64)

- ground: connection
- languages: c, cpp
- members: c `+` (f32,u64, 0 modes); c `-` (f32,u64, 0 modes); c `*` (f32,u64, 0 modes); c `/` (f32,u64, 0 modes); cpp `+` (f32,u64, 0 modes); cpp `-` (f32,u64, 0 modes); cpp `*` (f32,u64, 0 modes); cpp `/` (f32,u64, 0 modes)

  - c/op_122 / cpp/op_122 -- **total equality**
  - c/op_122 / cpp/op_158 -- **core difference**
  - c/op_122 / cpp/op_194 -- **core difference**
  - c/op_122 / cpp/op_230 -- **core difference**
  - c/op_158 / cpp/op_122 -- **core difference**
  - c/op_158 / cpp/op_158 -- **total equality**
  - c/op_158 / cpp/op_194 -- **core difference**
  - c/op_158 / cpp/op_230 -- **core difference**
  - c/op_194 / cpp/op_122 -- **core difference**
  - c/op_194 / cpp/op_158 -- **core difference**
  - c/op_194 / cpp/op_194 -- **total equality**
  - c/op_194 / cpp/op_230 -- **core difference**
  - c/op_230 / cpp/op_122 -- **core difference**
  - c/op_230 / cpp/op_158 -- **core difference**
  - c/op_230 / cpp/op_194 -- **core difference**
  - c/op_230 / cpp/op_230 -- **total equality**

### shared-core group ins@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64))))))),Add32F0x4(ex128@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64)))))))),ex128@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in1:64,1:8),zx64(And32(1:32,ex32@0(in1:64)))))))))) · (f32,u64)

- ground: connection
- languages: c, cpp
- members: c `==` (f32,u64, 0 modes); c `!=` (f32,u64, 0 modes); c `>` (f32,u64, 0 modes); c `>=` (f32,u64, 0 modes); c `<=` (f32,u64, 0 modes); c `<` (f32,u64, 0 modes); cpp `==` (f32,u64, 0 modes); cpp `!=` (f32,u64, 0 modes); cpp `>` (f32,u64, 0 modes); cpp `>=` (f32,u64, 0 modes); cpp `<=` (f32,u64, 0 modes); cpp `<` (f32,u64, 0 modes); cpp `<=>` (f32,u64, 0 modes); cpp `not_eq` (f32,u64, 0 modes)

  - c/op_482 / cpp/op_482 -- **total equality**
  - c/op_482 / cpp/op_518 -- **core difference**
  - c/op_482 / cpp/op_554 -- **core difference**
  - c/op_482 / cpp/op_590 -- **core difference**
  - c/op_482 / cpp/op_626 -- **core difference**
  - c/op_482 / cpp/op_662 -- **core difference**
  - c/op_482 / cpp/op_770 -- **core difference**
  - c/op_482 / cpp/op_986 -- **core difference**
  - c/op_518 / cpp/op_482 -- **core difference**
  - c/op_518 / cpp/op_518 -- **total equality**
  - c/op_518 / cpp/op_554 -- **core difference**
  - c/op_518 / cpp/op_590 -- **core difference**
  - c/op_518 / cpp/op_626 -- **core difference**
  - c/op_518 / cpp/op_662 -- **core difference**
  - c/op_518 / cpp/op_770 -- **core difference**
  - c/op_518 / cpp/op_986 -- **total equality**
  - c/op_554 / cpp/op_482 -- **core difference**
  - c/op_554 / cpp/op_518 -- **core difference**
  - c/op_554 / cpp/op_554 -- **core difference**
  - c/op_554 / cpp/op_590 -- **core difference**
  - c/op_554 / cpp/op_626 -- **core difference**
  - c/op_554 / cpp/op_662 -- **core difference**
  - c/op_554 / cpp/op_770 -- **core difference**
  - c/op_554 / cpp/op_986 -- **core difference**
  - c/op_590 / cpp/op_482 -- **core difference**
  - c/op_590 / cpp/op_518 -- **core difference**
  - c/op_590 / cpp/op_554 -- **core difference**
  - c/op_590 / cpp/op_590 -- **core difference**
  - c/op_590 / cpp/op_626 -- **core difference**
  - c/op_590 / cpp/op_662 -- **core difference**
  - c/op_590 / cpp/op_770 -- **core difference**
  - c/op_590 / cpp/op_986 -- **core difference**
  - c/op_626 / cpp/op_482 -- **core difference**
  - c/op_626 / cpp/op_518 -- **core difference**
  - c/op_626 / cpp/op_554 -- **core difference**
  - c/op_626 / cpp/op_590 -- **core difference**
  - c/op_626 / cpp/op_626 -- **core difference**
  - c/op_626 / cpp/op_662 -- **core difference**
  - c/op_626 / cpp/op_770 -- **core difference**
  - c/op_626 / cpp/op_986 -- **core difference**
  - c/op_662 / cpp/op_482 -- **core difference**
  - c/op_662 / cpp/op_518 -- **core difference**
  - c/op_662 / cpp/op_554 -- **core difference**
  - c/op_662 / cpp/op_590 -- **core difference**
  - c/op_662 / cpp/op_626 -- **core difference**
  - c/op_662 / cpp/op_662 -- **core difference**
  - c/op_662 / cpp/op_770 -- **core difference**
  - c/op_662 / cpp/op_986 -- **core difference**

### shared-core group And8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (f32,u64)

- ground: connection
- languages: c, cpp
- members: c `&&` (f32,u64, 0 modes); cpp `&&` (f32,u64, 0 modes); cpp `and` (f32,u64, 0 modes)

  - c/op_338 / cpp/op_338 -- **core difference**
  - c/op_338 / cpp/op_842 -- **core difference**

### shared-core group Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (f32,u64)

- ground: connection
- languages: c, cpp
- members: c `||` (f32,u64, 0 modes); cpp `||` (f32,u64, 0 modes); cpp `or` (f32,u64, 0 modes)

  - c/op_302 / cpp/op_302 -- **core difference**
  - c/op_302 / cpp/op_806 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),F32toF64(0:32)))),0:64,u0:64)))) · (f32,u64)

- ground: connection
- languages: c, cpp
- members: c `||` (f32,u64, 0 modes); c `&&` (f32,u64, 0 modes); cpp `||` (f32,u64, 0 modes); cpp `&&` (f32,u64, 0 modes); cpp `or` (f32,u64, 0 modes); cpp `and` (f32,u64, 0 modes)

  - c/op_302 / cpp/op_302 -- **core difference**
  - c/op_302 / cpp/op_338 -- **core difference**
  - c/op_302 / cpp/op_806 -- **core difference**
  - c/op_302 / cpp/op_842 -- **core difference**
  - c/op_338 / cpp/op_302 -- **core difference**
  - c/op_338 / cpp/op_338 -- **core difference**
  - c/op_338 / cpp/op_806 -- **core difference**
  - c/op_338 / cpp/op_842 -- **core difference**

### shared-core group ex1@0(amd64g_calculate_condition(8:64,20:64,in1:64,0:64,u0:64)) · (f32,u64)

- ground: connection
- languages: c, cpp
- members: c `+` (f32,u64, 0 modes); c `-` (f32,u64, 0 modes); c `*` (f32,u64, 0 modes); c `/` (f32,u64, 0 modes); c `==` (f32,u64, 0 modes); c `!=` (f32,u64, 0 modes); c `>` (f32,u64, 0 modes); c `>=` (f32,u64, 0 modes); c `<=` (f32,u64, 0 modes); c `<` (f32,u64, 0 modes); cpp `+` (f32,u64, 0 modes); cpp `-` (f32,u64, 0 modes); cpp `*` (f32,u64, 0 modes); cpp `/` (f32,u64, 0 modes); cpp `==` (f32,u64, 0 modes); cpp `!=` (f32,u64, 0 modes); cpp `>` (f32,u64, 0 modes); cpp `>=` (f32,u64, 0 modes); cpp `<=` (f32,u64, 0 modes); cpp `<` (f32,u64, 0 modes); cpp `<=>` (f32,u64, 0 modes); cpp `not_eq` (f32,u64, 0 modes)

  - c/op_122 / cpp/op_122 -- **total equality**
  - c/op_122 / cpp/op_158 -- **core difference**
  - c/op_122 / cpp/op_194 -- **core difference**
  - c/op_122 / cpp/op_230 -- **core difference**
  - c/op_122 / cpp/op_482 -- **core difference**
  - c/op_122 / cpp/op_518 -- **core difference**
  - c/op_122 / cpp/op_554 -- **core difference**
  - c/op_122 / cpp/op_590 -- **core difference**
  - c/op_122 / cpp/op_626 -- **core difference**
  - c/op_122 / cpp/op_662 -- **core difference**
  - c/op_122 / cpp/op_770 -- **core difference**
  - c/op_122 / cpp/op_986 -- **core difference**
  - c/op_158 / cpp/op_122 -- **core difference**
  - c/op_158 / cpp/op_158 -- **total equality**
  - c/op_158 / cpp/op_194 -- **core difference**
  - c/op_158 / cpp/op_230 -- **core difference**
  - c/op_158 / cpp/op_482 -- **core difference**
  - c/op_158 / cpp/op_518 -- **core difference**
  - c/op_158 / cpp/op_554 -- **core difference**
  - c/op_158 / cpp/op_590 -- **core difference**
  - c/op_158 / cpp/op_626 -- **core difference**
  - c/op_158 / cpp/op_662 -- **core difference**
  - c/op_158 / cpp/op_770 -- **core difference**
  - c/op_158 / cpp/op_986 -- **core difference**
  - c/op_194 / cpp/op_122 -- **core difference**
  - c/op_194 / cpp/op_158 -- **core difference**
  - c/op_194 / cpp/op_194 -- **total equality**
  - c/op_194 / cpp/op_230 -- **core difference**
  - c/op_194 / cpp/op_482 -- **core difference**
  - c/op_194 / cpp/op_518 -- **core difference**
  - c/op_194 / cpp/op_554 -- **core difference**
  - c/op_194 / cpp/op_590 -- **core difference**
  - c/op_194 / cpp/op_626 -- **core difference**
  - c/op_194 / cpp/op_662 -- **core difference**
  - c/op_194 / cpp/op_770 -- **core difference**
  - c/op_194 / cpp/op_986 -- **core difference**
  - c/op_230 / cpp/op_122 -- **core difference**
  - c/op_230 / cpp/op_158 -- **core difference**
  - c/op_230 / cpp/op_194 -- **core difference**
  - c/op_230 / cpp/op_230 -- **total equality**
  - c/op_230 / cpp/op_482 -- **core difference**
  - c/op_230 / cpp/op_518 -- **core difference**
  - c/op_230 / cpp/op_554 -- **core difference**
  - c/op_230 / cpp/op_590 -- **core difference**
  - c/op_230 / cpp/op_626 -- **core difference**
  - c/op_230 / cpp/op_662 -- **core difference**
  - c/op_230 / cpp/op_770 -- **core difference**
  - c/op_230 / cpp/op_986 -- **core difference**
  - c/op_482 / cpp/op_122 -- **core difference**
  - c/op_482 / cpp/op_158 -- **core difference**
  - c/op_482 / cpp/op_194 -- **core difference**
  - c/op_482 / cpp/op_230 -- **core difference**
  - c/op_482 / cpp/op_482 -- **total equality**
  - c/op_482 / cpp/op_518 -- **core difference**
  - c/op_482 / cpp/op_554 -- **core difference**
  - c/op_482 / cpp/op_590 -- **core difference**
  - c/op_482 / cpp/op_626 -- **core difference**
  - c/op_482 / cpp/op_662 -- **core difference**
  - c/op_482 / cpp/op_770 -- **core difference**
  - c/op_482 / cpp/op_986 -- **core difference**
  - c/op_518 / cpp/op_122 -- **core difference**
  - c/op_518 / cpp/op_158 -- **core difference**
  - c/op_518 / cpp/op_194 -- **core difference**
  - c/op_518 / cpp/op_230 -- **core difference**
  - c/op_518 / cpp/op_482 -- **core difference**
  - c/op_518 / cpp/op_518 -- **total equality**
  - c/op_518 / cpp/op_554 -- **core difference**
  - c/op_518 / cpp/op_590 -- **core difference**
  - c/op_518 / cpp/op_626 -- **core difference**
  - c/op_518 / cpp/op_662 -- **core difference**
  - c/op_518 / cpp/op_770 -- **core difference**
  - c/op_518 / cpp/op_986 -- **total equality**
  - c/op_554 / cpp/op_122 -- **core difference**
  - c/op_554 / cpp/op_158 -- **core difference**
  - c/op_554 / cpp/op_194 -- **core difference**
  - c/op_554 / cpp/op_230 -- **core difference**
  - c/op_554 / cpp/op_482 -- **core difference**
  - c/op_554 / cpp/op_518 -- **core difference**
  - c/op_554 / cpp/op_554 -- **core difference**
  - c/op_554 / cpp/op_590 -- **core difference**
  - c/op_554 / cpp/op_626 -- **core difference**
  - c/op_554 / cpp/op_662 -- **core difference**
  - c/op_554 / cpp/op_770 -- **core difference**
  - c/op_554 / cpp/op_986 -- **core difference**
  - c/op_590 / cpp/op_122 -- **core difference**
  - c/op_590 / cpp/op_158 -- **core difference**
  - c/op_590 / cpp/op_194 -- **core difference**
  - c/op_590 / cpp/op_230 -- **core difference**
  - c/op_590 / cpp/op_482 -- **core difference**
  - c/op_590 / cpp/op_518 -- **core difference**
  - c/op_590 / cpp/op_554 -- **core difference**
  - c/op_590 / cpp/op_590 -- **core difference**
  - c/op_590 / cpp/op_626 -- **core difference**
  - c/op_590 / cpp/op_662 -- **core difference**
  - c/op_590 / cpp/op_770 -- **core difference**
  - c/op_590 / cpp/op_986 -- **core difference**
  - c/op_626 / cpp/op_122 -- **core difference**
  - c/op_626 / cpp/op_158 -- **core difference**
  - c/op_626 / cpp/op_194 -- **core difference**
  - c/op_626 / cpp/op_230 -- **core difference**
  - c/op_626 / cpp/op_482 -- **core difference**
  - c/op_626 / cpp/op_518 -- **core difference**
  - c/op_626 / cpp/op_554 -- **core difference**
  - c/op_626 / cpp/op_590 -- **core difference**
  - c/op_626 / cpp/op_626 -- **core difference**
  - c/op_626 / cpp/op_662 -- **core difference**
  - c/op_626 / cpp/op_770 -- **core difference**
  - c/op_626 / cpp/op_986 -- **core difference**
  - c/op_662 / cpp/op_122 -- **core difference**
  - c/op_662 / cpp/op_158 -- **core difference**
  - c/op_662 / cpp/op_194 -- **core difference**
  - c/op_662 / cpp/op_230 -- **core difference**
  - c/op_662 / cpp/op_482 -- **core difference**
  - c/op_662 / cpp/op_518 -- **core difference**
  - c/op_662 / cpp/op_554 -- **core difference**
  - c/op_662 / cpp/op_590 -- **core difference**
  - c/op_662 / cpp/op_626 -- **core difference**
  - c/op_662 / cpp/op_662 -- **core difference**
  - c/op_662 / cpp/op_770 -- **core difference**
  - c/op_662 / cpp/op_986 -- **core difference**

### shared-core group F32toF64(ex32@0(in0:256)) · (f32,u64)

- ground: connection
- languages: c, cpp
- members: c `||` (f32,u64, 0 modes); c `&&` (f32,u64, 0 modes); c `>` (f32,u64, 0 modes); c `>=` (f32,u64, 0 modes); c `<=` (f32,u64, 0 modes); c `<` (f32,u64, 0 modes); cpp `||` (f32,u64, 0 modes); cpp `&&` (f32,u64, 0 modes); cpp `>` (f32,u64, 0 modes); cpp `>=` (f32,u64, 0 modes); cpp `<=` (f32,u64, 0 modes); cpp `<` (f32,u64, 0 modes); cpp `<=>` (f32,u64, 0 modes); cpp `or` (f32,u64, 0 modes); cpp `and` (f32,u64, 0 modes)

  - c/op_302 / cpp/op_302 -- **core difference**
  - c/op_302 / cpp/op_338 -- **core difference**
  - c/op_302 / cpp/op_554 -- **core difference**
  - c/op_302 / cpp/op_590 -- **core difference**
  - c/op_302 / cpp/op_626 -- **core difference**
  - c/op_302 / cpp/op_662 -- **core difference**
  - c/op_302 / cpp/op_770 -- **core difference**
  - c/op_302 / cpp/op_806 -- **core difference**
  - c/op_302 / cpp/op_842 -- **core difference**
  - c/op_338 / cpp/op_302 -- **core difference**
  - c/op_338 / cpp/op_338 -- **core difference**
  - c/op_338 / cpp/op_554 -- **core difference**
  - c/op_338 / cpp/op_590 -- **core difference**
  - c/op_338 / cpp/op_626 -- **core difference**
  - c/op_338 / cpp/op_662 -- **core difference**
  - c/op_338 / cpp/op_770 -- **core difference**
  - c/op_338 / cpp/op_806 -- **core difference**
  - c/op_338 / cpp/op_842 -- **core difference**
  - c/op_554 / cpp/op_302 -- **core difference**
  - c/op_554 / cpp/op_338 -- **core difference**
  - c/op_554 / cpp/op_554 -- **core difference**
  - c/op_554 / cpp/op_590 -- **core difference**
  - c/op_554 / cpp/op_626 -- **core difference**
  - c/op_554 / cpp/op_662 -- **core difference**
  - c/op_554 / cpp/op_770 -- **core difference**
  - c/op_554 / cpp/op_806 -- **core difference**
  - c/op_554 / cpp/op_842 -- **core difference**
  - c/op_590 / cpp/op_302 -- **core difference**
  - c/op_590 / cpp/op_338 -- **core difference**
  - c/op_590 / cpp/op_554 -- **core difference**
  - c/op_590 / cpp/op_590 -- **core difference**
  - c/op_590 / cpp/op_626 -- **core difference**
  - c/op_590 / cpp/op_662 -- **core difference**
  - c/op_590 / cpp/op_770 -- **core difference**
  - c/op_590 / cpp/op_806 -- **core difference**
  - c/op_590 / cpp/op_842 -- **core difference**
  - c/op_626 / cpp/op_302 -- **core difference**
  - c/op_626 / cpp/op_338 -- **core difference**
  - c/op_626 / cpp/op_554 -- **core difference**
  - c/op_626 / cpp/op_590 -- **core difference**
  - c/op_626 / cpp/op_626 -- **core difference**
  - c/op_626 / cpp/op_662 -- **core difference**
  - c/op_626 / cpp/op_770 -- **core difference**
  - c/op_626 / cpp/op_806 -- **core difference**
  - c/op_626 / cpp/op_842 -- **core difference**
  - c/op_662 / cpp/op_302 -- **core difference**
  - c/op_662 / cpp/op_338 -- **core difference**
  - c/op_662 / cpp/op_554 -- **core difference**
  - c/op_662 / cpp/op_590 -- **core difference**
  - c/op_662 / cpp/op_626 -- **core difference**
  - c/op_662 / cpp/op_662 -- **core difference**
  - c/op_662 / cpp/op_770 -- **core difference**
  - c/op_662 / cpp/op_806 -- **core difference**
  - c/op_662 / cpp/op_842 -- **core difference**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,0:128),CmpEQ64F0x2(0:128,ex128@0(in0:256)))))) · (f64,None)

- ground: connection
- languages: c, cpp
- members: c `!` (f64,None, 0 modes); cpp `not` (f64,None, 0 modes); cpp `!` (f64,None, 0 modes)

  - c/op_4 / cpp/op_28 -- **total equality**
  - c/op_4 / cpp/op_4 -- **total equality**

### shared-core group st64(Add64(18446744073709551608:64,SP:64))=ex64@0(in0:256) · (f64,None)

- ground: connection
- languages: c, cpp
- members: c `&` (f64,None, 0 modes); cpp `&` (f64,None, 0 modes)

  - c/op_34 / cpp/op_46 -- **total equality**

### shared-core group Add64F0x2(ex128@0(in0:256),zx128(ld64/g0(8:64))) · (f64,None)

- ground: connection
- languages: c, cpp
- members: c `++` (f64,None, 0 modes); c `--` (f64,None, 0 modes); cpp `++` (f64,None, 0 modes); cpp `--` (f64,None, 0 modes)

  - c/op_40 / cpp/op_52 -- **total equality**
  - c/op_40 / cpp/op_58 -- **total equality**
  - c/op_46 / cpp/op_52 -- **total equality**
  - c/op_46 / cpp/op_58 -- **total equality**

### shared-core group XorV128(ex128@0(in0:256),ld128/g0(7:64)) · (f64,None)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `-` (f64,None, 0 modes); cpp `-` (f64,None, 0 modes); rust `-` (f64,None, 0 modes); swift `-` (f64,None, 0 modes)

  - c/op_16 / cpp/op_16 -- **total equality**
  - c/op_16 / rust/op_4 -- **total equality**
  - c/op_16 / swift/op_16 -- **total equality**
  - cpp/op_16 / rust/op_4 -- **total equality**
  - cpp/op_16 / swift/op_16 -- **total equality**
  - rust/op_4 / swift/op_16 -- **total equality**

### shared-core group And8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64)))),ex8@0(in1:64)) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `&&` (f64,bool, 0 modes); cpp `&&` (f64,bool, 0 modes); cpp `and` (f64,bool, 0 modes)

  - c/op_347 / cpp/op_347 -- **core difference**
  - c/op_347 / cpp/op_851 -- **core difference**

### shared-core group Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64)))),ex8@0(in1:64)) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `||` (f64,bool, 0 modes); cpp `||` (f64,bool, 0 modes); cpp `or` (f64,bool, 0 modes)

  - c/op_311 / cpp/op_311 -- **core difference**
  - c/op_311 / cpp/op_815 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64)))) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `||` (f64,bool, 0 modes); c `&&` (f64,bool, 0 modes); cpp `||` (f64,bool, 0 modes); cpp `&&` (f64,bool, 0 modes); cpp `or` (f64,bool, 0 modes); cpp `and` (f64,bool, 0 modes)

  - c/op_311 / cpp/op_311 -- **core difference**
  - c/op_311 / cpp/op_347 -- **core difference**
  - c/op_311 / cpp/op_815 -- **core difference**
  - c/op_311 / cpp/op_851 -- **core difference**
  - c/op_347 / cpp/op_311 -- **core difference**
  - c/op_347 / cpp/op_347 -- **core difference**
  - c/op_347 / cpp/op_815 -- **core difference**
  - c/op_347 / cpp/op_851 -- **core difference**

### shared-core group ins@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))),XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))),ex128@0(in0:256)))) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `!=` (f64,bool, 0 modes); cpp `!=` (f64,bool, 0 modes); cpp `not_eq` (f64,bool, 0 modes)

  - c/op_527 / cpp/op_527 -- **total equality**
  - c/op_527 / cpp/op_995 -- **total equality**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))),CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))),ex128@0(in0:256)))))) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `==` (f64,bool, 0 modes); cpp `==` (f64,bool, 0 modes)

  - c/op_491 / cpp/op_491 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))))))),0:64,u1:64))) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `>` (f64,bool, 0 modes); cpp `>` (f64,bool, 0 modes)

  - c/op_563 / cpp/op_563 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))))))),0:64,u1:64))) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `>=` (f64,bool, 0 modes); cpp `>=` (f64,bool, 0 modes)

  - c/op_599 / cpp/op_599 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))),ex64@0(in0:256)))),0:64,u1:64))) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `<=` (f64,bool, 0 modes); cpp `<=` (f64,bool, 0 modes)

  - c/op_635 / cpp/op_635 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))),ex64@0(in0:256)))),0:64,u1:64))) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `<` (f64,bool, 0 modes); cpp `<` (f64,bool, 0 modes)

  - c/op_671 / cpp/op_671 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))))))) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `>` (f64,bool, 0 modes); c `>=` (f64,bool, 0 modes); cpp `>` (f64,bool, 0 modes); cpp `>=` (f64,bool, 0 modes)

  - c/op_563 / cpp/op_563 -- **core difference**
  - c/op_563 / cpp/op_599 -- **core difference**
  - c/op_599 / cpp/op_563 -- **core difference**
  - c/op_599 / cpp/op_599 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))),ex64@0(in0:256)))) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `<=` (f64,bool, 0 modes); c `<` (f64,bool, 0 modes); cpp `<=` (f64,bool, 0 modes); cpp `<` (f64,bool, 0 modes)

  - c/op_635 / cpp/op_635 -- **core difference**
  - c/op_635 / cpp/op_671 -- **core difference**
  - c/op_671 / cpp/op_635 -- **core difference**
  - c/op_671 / cpp/op_671 -- **core difference**

### shared-core group CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))),ex128@0(in0:256)) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `==` (f64,bool, 0 modes); c `!=` (f64,bool, 0 modes); cpp `==` (f64,bool, 0 modes); cpp `!=` (f64,bool, 0 modes); cpp `not_eq` (f64,bool, 0 modes)

  - c/op_491 / cpp/op_491 -- **total equality**
  - c/op_491 / cpp/op_527 -- **core difference**
  - c/op_491 / cpp/op_995 -- **core difference**
  - c/op_527 / cpp/op_491 -- **core difference**
  - c/op_527 / cpp/op_527 -- **total equality**
  - c/op_527 / cpp/op_995 -- **total equality**

### shared-core group Add64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))))) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `+` (f64,bool, 0 modes); cpp `+` (f64,bool, 0 modes)

  - c/op_131 / cpp/op_131 -- **total equality**

### shared-core group Sub64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))))) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `-` (f64,bool, 0 modes); cpp `-` (f64,bool, 0 modes)

  - c/op_167 / cpp/op_167 -- **total equality**

### shared-core group Mul64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))))) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `*` (f64,bool, 0 modes); cpp `*` (f64,bool, 0 modes)

  - c/op_203 / cpp/op_203 -- **total equality**

### shared-core group Div64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))))) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `/` (f64,bool, 0 modes); cpp `/` (f64,bool, 0 modes)

  - c/op_239 / cpp/op_239 -- **total equality**

### shared-core group ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `+` (f64,bool, 0 modes); c `-` (f64,bool, 0 modes); c `*` (f64,bool, 0 modes); c `/` (f64,bool, 0 modes); c `==` (f64,bool, 0 modes); c `!=` (f64,bool, 0 modes); cpp `+` (f64,bool, 0 modes); cpp `-` (f64,bool, 0 modes); cpp `*` (f64,bool, 0 modes); cpp `/` (f64,bool, 0 modes); cpp `==` (f64,bool, 0 modes); cpp `!=` (f64,bool, 0 modes); cpp `not_eq` (f64,bool, 0 modes)

  - c/op_131 / cpp/op_131 -- **total equality**
  - c/op_131 / cpp/op_167 -- **core difference**
  - c/op_131 / cpp/op_203 -- **core difference**
  - c/op_131 / cpp/op_239 -- **core difference**
  - c/op_131 / cpp/op_491 -- **core difference**
  - c/op_131 / cpp/op_527 -- **core difference**
  - c/op_131 / cpp/op_995 -- **core difference**
  - c/op_167 / cpp/op_131 -- **core difference**
  - c/op_167 / cpp/op_167 -- **total equality**
  - c/op_167 / cpp/op_203 -- **core difference**
  - c/op_167 / cpp/op_239 -- **core difference**
  - c/op_167 / cpp/op_491 -- **core difference**
  - c/op_167 / cpp/op_527 -- **core difference**
  - c/op_167 / cpp/op_995 -- **core difference**
  - c/op_203 / cpp/op_131 -- **core difference**
  - c/op_203 / cpp/op_167 -- **core difference**
  - c/op_203 / cpp/op_203 -- **total equality**
  - c/op_203 / cpp/op_239 -- **core difference**
  - c/op_203 / cpp/op_491 -- **core difference**
  - c/op_203 / cpp/op_527 -- **core difference**
  - c/op_203 / cpp/op_995 -- **core difference**
  - c/op_239 / cpp/op_131 -- **core difference**
  - c/op_239 / cpp/op_167 -- **core difference**
  - c/op_239 / cpp/op_203 -- **core difference**
  - c/op_239 / cpp/op_239 -- **total equality**
  - c/op_239 / cpp/op_491 -- **core difference**
  - c/op_239 / cpp/op_527 -- **core difference**
  - c/op_239 / cpp/op_995 -- **core difference**
  - c/op_491 / cpp/op_131 -- **core difference**
  - c/op_491 / cpp/op_167 -- **core difference**
  - c/op_491 / cpp/op_203 -- **core difference**
  - c/op_491 / cpp/op_239 -- **core difference**
  - c/op_491 / cpp/op_491 -- **total equality**
  - c/op_491 / cpp/op_527 -- **core difference**
  - c/op_491 / cpp/op_995 -- **core difference**
  - c/op_527 / cpp/op_131 -- **core difference**
  - c/op_527 / cpp/op_167 -- **core difference**
  - c/op_527 / cpp/op_203 -- **core difference**
  - c/op_527 / cpp/op_239 -- **core difference**
  - c/op_527 / cpp/op_491 -- **core difference**
  - c/op_527 / cpp/op_527 -- **total equality**
  - c/op_527 / cpp/op_995 -- **total equality**

### shared-core group ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `>` (f64,bool, 0 modes); c `>=` (f64,bool, 0 modes); c `<=` (f64,bool, 0 modes); c `<` (f64,bool, 0 modes); cpp `>` (f64,bool, 0 modes); cpp `>=` (f64,bool, 0 modes); cpp `<=` (f64,bool, 0 modes); cpp `<` (f64,bool, 0 modes)

  - c/op_563 / cpp/op_563 -- **core difference**
  - c/op_563 / cpp/op_599 -- **core difference**
  - c/op_563 / cpp/op_635 -- **core difference**
  - c/op_563 / cpp/op_671 -- **core difference**
  - c/op_599 / cpp/op_563 -- **core difference**
  - c/op_599 / cpp/op_599 -- **core difference**
  - c/op_599 / cpp/op_635 -- **core difference**
  - c/op_599 / cpp/op_671 -- **core difference**
  - c/op_635 / cpp/op_563 -- **core difference**
  - c/op_635 / cpp/op_599 -- **core difference**
  - c/op_635 / cpp/op_635 -- **core difference**
  - c/op_635 / cpp/op_671 -- **core difference**
  - c/op_671 / cpp/op_563 -- **core difference**
  - c/op_671 / cpp/op_599 -- **core difference**
  - c/op_671 / cpp/op_635 -- **core difference**
  - c/op_671 / cpp/op_671 -- **core difference**

### shared-core group ins@0(u0:256,I32StoF64(ex32@0(in1:64))) · (f64,bool)

- ground: connection
- languages: c, cpp
- members: c `+` (f64,bool, 0 modes); c `-` (f64,bool, 0 modes); c `*` (f64,bool, 0 modes); c `/` (f64,bool, 0 modes); c `==` (f64,bool, 0 modes); c `!=` (f64,bool, 0 modes); c `>` (f64,bool, 0 modes); c `>=` (f64,bool, 0 modes); c `<=` (f64,bool, 0 modes); c `<` (f64,bool, 0 modes); cpp `+` (f64,bool, 0 modes); cpp `-` (f64,bool, 0 modes); cpp `*` (f64,bool, 0 modes); cpp `/` (f64,bool, 0 modes); cpp `==` (f64,bool, 0 modes); cpp `!=` (f64,bool, 0 modes); cpp `>` (f64,bool, 0 modes); cpp `>=` (f64,bool, 0 modes); cpp `<=` (f64,bool, 0 modes); cpp `<` (f64,bool, 0 modes); cpp `not_eq` (f64,bool, 0 modes)

  - c/op_131 / cpp/op_131 -- **total equality**
  - c/op_131 / cpp/op_167 -- **core difference**
  - c/op_131 / cpp/op_203 -- **core difference**
  - c/op_131 / cpp/op_239 -- **core difference**
  - c/op_131 / cpp/op_491 -- **core difference**
  - c/op_131 / cpp/op_527 -- **core difference**
  - c/op_131 / cpp/op_563 -- **core difference**
  - c/op_131 / cpp/op_599 -- **core difference**
  - c/op_131 / cpp/op_635 -- **core difference**
  - c/op_131 / cpp/op_671 -- **core difference**
  - c/op_131 / cpp/op_995 -- **core difference**
  - c/op_167 / cpp/op_131 -- **core difference**
  - c/op_167 / cpp/op_167 -- **total equality**
  - c/op_167 / cpp/op_203 -- **core difference**
  - c/op_167 / cpp/op_239 -- **core difference**
  - c/op_167 / cpp/op_491 -- **core difference**
  - c/op_167 / cpp/op_527 -- **core difference**
  - c/op_167 / cpp/op_563 -- **core difference**
  - c/op_167 / cpp/op_599 -- **core difference**
  - c/op_167 / cpp/op_635 -- **core difference**
  - c/op_167 / cpp/op_671 -- **core difference**
  - c/op_167 / cpp/op_995 -- **core difference**
  - c/op_203 / cpp/op_131 -- **core difference**
  - c/op_203 / cpp/op_167 -- **core difference**
  - c/op_203 / cpp/op_203 -- **total equality**
  - c/op_203 / cpp/op_239 -- **core difference**
  - c/op_203 / cpp/op_491 -- **core difference**
  - c/op_203 / cpp/op_527 -- **core difference**
  - c/op_203 / cpp/op_563 -- **core difference**
  - c/op_203 / cpp/op_599 -- **core difference**
  - c/op_203 / cpp/op_635 -- **core difference**
  - c/op_203 / cpp/op_671 -- **core difference**
  - c/op_203 / cpp/op_995 -- **core difference**
  - c/op_239 / cpp/op_131 -- **core difference**
  - c/op_239 / cpp/op_167 -- **core difference**
  - c/op_239 / cpp/op_203 -- **core difference**
  - c/op_239 / cpp/op_239 -- **total equality**
  - c/op_239 / cpp/op_491 -- **core difference**
  - c/op_239 / cpp/op_527 -- **core difference**
  - c/op_239 / cpp/op_563 -- **core difference**
  - c/op_239 / cpp/op_599 -- **core difference**
  - c/op_239 / cpp/op_635 -- **core difference**
  - c/op_239 / cpp/op_671 -- **core difference**
  - c/op_239 / cpp/op_995 -- **core difference**
  - c/op_491 / cpp/op_131 -- **core difference**
  - c/op_491 / cpp/op_167 -- **core difference**
  - c/op_491 / cpp/op_203 -- **core difference**
  - c/op_491 / cpp/op_239 -- **core difference**
  - c/op_491 / cpp/op_491 -- **total equality**
  - c/op_491 / cpp/op_527 -- **core difference**
  - c/op_491 / cpp/op_563 -- **core difference**
  - c/op_491 / cpp/op_599 -- **core difference**
  - c/op_491 / cpp/op_635 -- **core difference**
  - c/op_491 / cpp/op_671 -- **core difference**
  - c/op_491 / cpp/op_995 -- **core difference**
  - c/op_527 / cpp/op_131 -- **core difference**
  - c/op_527 / cpp/op_167 -- **core difference**
  - c/op_527 / cpp/op_203 -- **core difference**
  - c/op_527 / cpp/op_239 -- **core difference**
  - c/op_527 / cpp/op_491 -- **core difference**
  - c/op_527 / cpp/op_527 -- **total equality**
  - c/op_527 / cpp/op_563 -- **core difference**
  - c/op_527 / cpp/op_599 -- **core difference**
  - c/op_527 / cpp/op_635 -- **core difference**
  - c/op_527 / cpp/op_671 -- **core difference**
  - c/op_527 / cpp/op_995 -- **total equality**
  - c/op_563 / cpp/op_131 -- **core difference**
  - c/op_563 / cpp/op_167 -- **core difference**
  - c/op_563 / cpp/op_203 -- **core difference**
  - c/op_563 / cpp/op_239 -- **core difference**
  - c/op_563 / cpp/op_491 -- **core difference**
  - c/op_563 / cpp/op_527 -- **core difference**
  - c/op_563 / cpp/op_563 -- **core difference**
  - c/op_563 / cpp/op_599 -- **core difference**
  - c/op_563 / cpp/op_635 -- **core difference**
  - c/op_563 / cpp/op_671 -- **core difference**
  - c/op_563 / cpp/op_995 -- **core difference**
  - c/op_599 / cpp/op_131 -- **core difference**
  - c/op_599 / cpp/op_167 -- **core difference**
  - c/op_599 / cpp/op_203 -- **core difference**
  - c/op_599 / cpp/op_239 -- **core difference**
  - c/op_599 / cpp/op_491 -- **core difference**
  - c/op_599 / cpp/op_527 -- **core difference**
  - c/op_599 / cpp/op_563 -- **core difference**
  - c/op_599 / cpp/op_599 -- **core difference**
  - c/op_599 / cpp/op_635 -- **core difference**
  - c/op_599 / cpp/op_671 -- **core difference**
  - c/op_599 / cpp/op_995 -- **core difference**
  - c/op_635 / cpp/op_131 -- **core difference**
  - c/op_635 / cpp/op_167 -- **core difference**
  - c/op_635 / cpp/op_203 -- **core difference**
  - c/op_635 / cpp/op_239 -- **core difference**
  - c/op_635 / cpp/op_491 -- **core difference**
  - c/op_635 / cpp/op_527 -- **core difference**
  - c/op_635 / cpp/op_563 -- **core difference**
  - c/op_635 / cpp/op_599 -- **core difference**
  - c/op_635 / cpp/op_635 -- **core difference**
  - c/op_635 / cpp/op_671 -- **core difference**
  - c/op_635 / cpp/op_995 -- **core difference**
  - c/op_671 / cpp/op_131 -- **core difference**
  - c/op_671 / cpp/op_167 -- **core difference**
  - c/op_671 / cpp/op_203 -- **core difference**
  - c/op_671 / cpp/op_239 -- **core difference**
  - c/op_671 / cpp/op_491 -- **core difference**
  - c/op_671 / cpp/op_527 -- **core difference**
  - c/op_671 / cpp/op_563 -- **core difference**
  - c/op_671 / cpp/op_599 -- **core difference**
  - c/op_671 / cpp/op_635 -- **core difference**
  - c/op_671 / cpp/op_671 -- **core difference**
  - c/op_671 / cpp/op_995 -- **core difference**

### shared-core group And8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64)))),Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64))))) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `&&` (f64,f32, 0 modes); cpp `&&` (f64,f32, 0 modes); cpp `and` (f64,f32, 0 modes)

  - c/op_345 / cpp/op_345 -- **core difference**
  - c/op_345 / cpp/op_849 -- **core difference**

### shared-core group Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64)))),Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64))))) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `||` (f64,f32, 0 modes); cpp `||` (f64,f32, 0 modes); cpp `or` (f64,f32, 0 modes)

  - c/op_309 / cpp/op_309 -- **core difference**
  - c/op_309 / cpp/op_813 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64)))) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `||` (f64,f32, 0 modes); c `&&` (f64,f32, 0 modes); cpp `||` (f64,f32, 0 modes); cpp `&&` (f64,f32, 0 modes); cpp `or` (f64,f32, 0 modes); cpp `and` (f64,f32, 0 modes)

  - c/op_309 / cpp/op_309 -- **core difference**
  - c/op_309 / cpp/op_345 -- **core difference**
  - c/op_309 / cpp/op_813 -- **core difference**
  - c/op_309 / cpp/op_849 -- **core difference**
  - c/op_345 / cpp/op_309 -- **core difference**
  - c/op_345 / cpp/op_345 -- **core difference**
  - c/op_345 / cpp/op_813 -- **core difference**
  - c/op_345 / cpp/op_849 -- **core difference**

### shared-core group ins@0(ins@0(in1:256,F32toF64(ex32@0(in1:256))),XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(in1:256,F32toF64(ex32@0(in1:256)))),ex128@0(in0:256)))) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `!=` (f64,f32, 0 modes); cpp `!=` (f64,f32, 0 modes); cpp `not_eq` (f64,f32, 0 modes)

  - c/op_525 / cpp/op_525 -- **total equality**
  - c/op_525 / cpp/op_993 -- **total equality**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(ins@0(in1:256,F32toF64(ex32@0(in1:256))),CmpEQ64F0x2(ex128@0(ins@0(in1:256,F32toF64(ex32@0(in1:256)))),ex128@0(in0:256)))))) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `==` (f64,f32, 0 modes); cpp `==` (f64,f32, 0 modes)

  - c/op_489 / cpp/op_489 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(ins@0(in1:256,F32toF64(ex32@0(in1:256))))))),0:64,u0:64))) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `>` (f64,f32, 0 modes); cpp `>` (f64,f32, 0 modes)

  - c/op_561 / cpp/op_561 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(ins@0(in1:256,F32toF64(ex32@0(in1:256))))))),0:64,u0:64))) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `>=` (f64,f32, 0 modes); cpp `>=` (f64,f32, 0 modes)

  - c/op_597 / cpp/op_597 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(ins@0(in1:256,F32toF64(ex32@0(in1:256)))),ex64@0(in0:256)))),0:64,u0:64))) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `<=` (f64,f32, 0 modes); cpp `<=` (f64,f32, 0 modes)

  - c/op_633 / cpp/op_633 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(ins@0(in1:256,F32toF64(ex32@0(in1:256)))),ex64@0(in0:256)))),0:64,u0:64))) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `<` (f64,f32, 0 modes); cpp `<` (f64,f32, 0 modes)

  - c/op_669 / cpp/op_669 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(ins@0(in1:256,F32toF64(ex32@0(in1:256))))))) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `>` (f64,f32, 0 modes); c `>=` (f64,f32, 0 modes); cpp `>` (f64,f32, 0 modes); cpp `>=` (f64,f32, 0 modes); cpp `<=>` (f64,f32, 0 modes)

  - c/op_561 / cpp/op_561 -- **core difference**
  - c/op_561 / cpp/op_597 -- **core difference**
  - c/op_561 / cpp/op_777 -- **core difference**
  - c/op_597 / cpp/op_561 -- **core difference**
  - c/op_597 / cpp/op_597 -- **core difference**
  - c/op_597 / cpp/op_777 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(ins@0(in1:256,F32toF64(ex32@0(in1:256)))),ex64@0(in0:256)))) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `<=` (f64,f32, 0 modes); c `<` (f64,f32, 0 modes); cpp `<=` (f64,f32, 0 modes); cpp `<` (f64,f32, 0 modes); cpp `<=>` (f64,f32, 0 modes)

  - c/op_633 / cpp/op_633 -- **core difference**
  - c/op_633 / cpp/op_669 -- **core difference**
  - c/op_633 / cpp/op_777 -- **core difference**
  - c/op_669 / cpp/op_633 -- **core difference**
  - c/op_669 / cpp/op_669 -- **core difference**
  - c/op_669 / cpp/op_777 -- **core difference**

### shared-core group CmpEQ64F0x2(ex128@0(ins@0(in1:256,F32toF64(ex32@0(in1:256)))),ex128@0(in0:256)) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `==` (f64,f32, 0 modes); c `!=` (f64,f32, 0 modes); cpp `==` (f64,f32, 0 modes); cpp `!=` (f64,f32, 0 modes); cpp `not_eq` (f64,f32, 0 modes)

  - c/op_489 / cpp/op_489 -- **total equality**
  - c/op_489 / cpp/op_525 -- **core difference**
  - c/op_489 / cpp/op_993 -- **core difference**
  - c/op_525 / cpp/op_489 -- **core difference**
  - c/op_525 / cpp/op_525 -- **total equality**
  - c/op_525 / cpp/op_993 -- **total equality**

### shared-core group Add64F0x2(ex128@0(in0:256),ex128@0(ins@0(in1:256,F32toF64(ex32@0(in1:256))))) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `+` (f64,f32, 0 modes); cpp `+` (f64,f32, 0 modes)

  - c/op_129 / cpp/op_129 -- **total equality**

### shared-core group Sub64F0x2(ex128@0(in0:256),ex128@0(ins@0(in1:256,F32toF64(ex32@0(in1:256))))) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `-` (f64,f32, 0 modes); cpp `-` (f64,f32, 0 modes)

  - c/op_165 / cpp/op_165 -- **total equality**

### shared-core group Mul64F0x2(ex128@0(in0:256),ex128@0(ins@0(in1:256,F32toF64(ex32@0(in1:256))))) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `*` (f64,f32, 0 modes); cpp `*` (f64,f32, 0 modes)

  - c/op_201 / cpp/op_201 -- **total equality**

### shared-core group Div64F0x2(ex128@0(in0:256),ex128@0(ins@0(in1:256,F32toF64(ex32@0(in1:256))))) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `/` (f64,f32, 0 modes); cpp `/` (f64,f32, 0 modes)

  - c/op_237 / cpp/op_237 -- **total equality**

### shared-core group ex128@0(ins@0(in1:256,F32toF64(ex32@0(in1:256)))) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `+` (f64,f32, 0 modes); c `-` (f64,f32, 0 modes); c `*` (f64,f32, 0 modes); c `/` (f64,f32, 0 modes); c `==` (f64,f32, 0 modes); c `!=` (f64,f32, 0 modes); cpp `+` (f64,f32, 0 modes); cpp `-` (f64,f32, 0 modes); cpp `*` (f64,f32, 0 modes); cpp `/` (f64,f32, 0 modes); cpp `==` (f64,f32, 0 modes); cpp `!=` (f64,f32, 0 modes); cpp `not_eq` (f64,f32, 0 modes)

  - c/op_129 / cpp/op_129 -- **total equality**
  - c/op_129 / cpp/op_165 -- **core difference**
  - c/op_129 / cpp/op_201 -- **core difference**
  - c/op_129 / cpp/op_237 -- **core difference**
  - c/op_129 / cpp/op_489 -- **core difference**
  - c/op_129 / cpp/op_525 -- **core difference**
  - c/op_129 / cpp/op_993 -- **core difference**
  - c/op_165 / cpp/op_129 -- **core difference**
  - c/op_165 / cpp/op_165 -- **total equality**
  - c/op_165 / cpp/op_201 -- **core difference**
  - c/op_165 / cpp/op_237 -- **core difference**
  - c/op_165 / cpp/op_489 -- **core difference**
  - c/op_165 / cpp/op_525 -- **core difference**
  - c/op_165 / cpp/op_993 -- **core difference**
  - c/op_201 / cpp/op_129 -- **core difference**
  - c/op_201 / cpp/op_165 -- **core difference**
  - c/op_201 / cpp/op_201 -- **total equality**
  - c/op_201 / cpp/op_237 -- **core difference**
  - c/op_201 / cpp/op_489 -- **core difference**
  - c/op_201 / cpp/op_525 -- **core difference**
  - c/op_201 / cpp/op_993 -- **core difference**
  - c/op_237 / cpp/op_129 -- **core difference**
  - c/op_237 / cpp/op_165 -- **core difference**
  - c/op_237 / cpp/op_201 -- **core difference**
  - c/op_237 / cpp/op_237 -- **total equality**
  - c/op_237 / cpp/op_489 -- **core difference**
  - c/op_237 / cpp/op_525 -- **core difference**
  - c/op_237 / cpp/op_993 -- **core difference**
  - c/op_489 / cpp/op_129 -- **core difference**
  - c/op_489 / cpp/op_165 -- **core difference**
  - c/op_489 / cpp/op_201 -- **core difference**
  - c/op_489 / cpp/op_237 -- **core difference**
  - c/op_489 / cpp/op_489 -- **total equality**
  - c/op_489 / cpp/op_525 -- **core difference**
  - c/op_489 / cpp/op_993 -- **core difference**
  - c/op_525 / cpp/op_129 -- **core difference**
  - c/op_525 / cpp/op_165 -- **core difference**
  - c/op_525 / cpp/op_201 -- **core difference**
  - c/op_525 / cpp/op_237 -- **core difference**
  - c/op_525 / cpp/op_489 -- **core difference**
  - c/op_525 / cpp/op_525 -- **total equality**
  - c/op_525 / cpp/op_993 -- **total equality**

### shared-core group ex64@0(ins@0(in1:256,F32toF64(ex32@0(in1:256)))) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `>` (f64,f32, 0 modes); c `>=` (f64,f32, 0 modes); c `<=` (f64,f32, 0 modes); c `<` (f64,f32, 0 modes); cpp `>` (f64,f32, 0 modes); cpp `>=` (f64,f32, 0 modes); cpp `<=` (f64,f32, 0 modes); cpp `<` (f64,f32, 0 modes); cpp `<=>` (f64,f32, 0 modes)

  - c/op_561 / cpp/op_561 -- **core difference**
  - c/op_561 / cpp/op_597 -- **core difference**
  - c/op_561 / cpp/op_633 -- **core difference**
  - c/op_561 / cpp/op_669 -- **core difference**
  - c/op_561 / cpp/op_777 -- **core difference**
  - c/op_597 / cpp/op_561 -- **core difference**
  - c/op_597 / cpp/op_597 -- **core difference**
  - c/op_597 / cpp/op_633 -- **core difference**
  - c/op_597 / cpp/op_669 -- **core difference**
  - c/op_597 / cpp/op_777 -- **core difference**
  - c/op_633 / cpp/op_561 -- **core difference**
  - c/op_633 / cpp/op_597 -- **core difference**
  - c/op_633 / cpp/op_633 -- **core difference**
  - c/op_633 / cpp/op_669 -- **core difference**
  - c/op_633 / cpp/op_777 -- **core difference**
  - c/op_669 / cpp/op_561 -- **core difference**
  - c/op_669 / cpp/op_597 -- **core difference**
  - c/op_669 / cpp/op_633 -- **core difference**
  - c/op_669 / cpp/op_669 -- **core difference**
  - c/op_669 / cpp/op_777 -- **core difference**

### shared-core group ins@0(in1:256,F32toF64(ex32@0(in1:256))) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `+` (f64,f32, 0 modes); c `-` (f64,f32, 0 modes); c `*` (f64,f32, 0 modes); c `/` (f64,f32, 0 modes); c `==` (f64,f32, 0 modes); c `!=` (f64,f32, 0 modes); c `>` (f64,f32, 0 modes); c `>=` (f64,f32, 0 modes); c `<=` (f64,f32, 0 modes); c `<` (f64,f32, 0 modes); cpp `+` (f64,f32, 0 modes); cpp `-` (f64,f32, 0 modes); cpp `*` (f64,f32, 0 modes); cpp `/` (f64,f32, 0 modes); cpp `==` (f64,f32, 0 modes); cpp `!=` (f64,f32, 0 modes); cpp `>` (f64,f32, 0 modes); cpp `>=` (f64,f32, 0 modes); cpp `<=` (f64,f32, 0 modes); cpp `<` (f64,f32, 0 modes); cpp `<=>` (f64,f32, 0 modes); cpp `not_eq` (f64,f32, 0 modes)

  - c/op_129 / cpp/op_129 -- **total equality**
  - c/op_129 / cpp/op_165 -- **core difference**
  - c/op_129 / cpp/op_201 -- **core difference**
  - c/op_129 / cpp/op_237 -- **core difference**
  - c/op_129 / cpp/op_489 -- **core difference**
  - c/op_129 / cpp/op_525 -- **core difference**
  - c/op_129 / cpp/op_561 -- **core difference**
  - c/op_129 / cpp/op_597 -- **core difference**
  - c/op_129 / cpp/op_633 -- **core difference**
  - c/op_129 / cpp/op_669 -- **core difference**
  - c/op_129 / cpp/op_777 -- **core difference**
  - c/op_129 / cpp/op_993 -- **core difference**
  - c/op_165 / cpp/op_129 -- **core difference**
  - c/op_165 / cpp/op_165 -- **total equality**
  - c/op_165 / cpp/op_201 -- **core difference**
  - c/op_165 / cpp/op_237 -- **core difference**
  - c/op_165 / cpp/op_489 -- **core difference**
  - c/op_165 / cpp/op_525 -- **core difference**
  - c/op_165 / cpp/op_561 -- **core difference**
  - c/op_165 / cpp/op_597 -- **core difference**
  - c/op_165 / cpp/op_633 -- **core difference**
  - c/op_165 / cpp/op_669 -- **core difference**
  - c/op_165 / cpp/op_777 -- **core difference**
  - c/op_165 / cpp/op_993 -- **core difference**
  - c/op_201 / cpp/op_129 -- **core difference**
  - c/op_201 / cpp/op_165 -- **core difference**
  - c/op_201 / cpp/op_201 -- **total equality**
  - c/op_201 / cpp/op_237 -- **core difference**
  - c/op_201 / cpp/op_489 -- **core difference**
  - c/op_201 / cpp/op_525 -- **core difference**
  - c/op_201 / cpp/op_561 -- **core difference**
  - c/op_201 / cpp/op_597 -- **core difference**
  - c/op_201 / cpp/op_633 -- **core difference**
  - c/op_201 / cpp/op_669 -- **core difference**
  - c/op_201 / cpp/op_777 -- **core difference**
  - c/op_201 / cpp/op_993 -- **core difference**
  - c/op_237 / cpp/op_129 -- **core difference**
  - c/op_237 / cpp/op_165 -- **core difference**
  - c/op_237 / cpp/op_201 -- **core difference**
  - c/op_237 / cpp/op_237 -- **total equality**
  - c/op_237 / cpp/op_489 -- **core difference**
  - c/op_237 / cpp/op_525 -- **core difference**
  - c/op_237 / cpp/op_561 -- **core difference**
  - c/op_237 / cpp/op_597 -- **core difference**
  - c/op_237 / cpp/op_633 -- **core difference**
  - c/op_237 / cpp/op_669 -- **core difference**
  - c/op_237 / cpp/op_777 -- **core difference**
  - c/op_237 / cpp/op_993 -- **core difference**
  - c/op_489 / cpp/op_129 -- **core difference**
  - c/op_489 / cpp/op_165 -- **core difference**
  - c/op_489 / cpp/op_201 -- **core difference**
  - c/op_489 / cpp/op_237 -- **core difference**
  - c/op_489 / cpp/op_489 -- **total equality**
  - c/op_489 / cpp/op_525 -- **core difference**
  - c/op_489 / cpp/op_561 -- **core difference**
  - c/op_489 / cpp/op_597 -- **core difference**
  - c/op_489 / cpp/op_633 -- **core difference**
  - c/op_489 / cpp/op_669 -- **core difference**
  - c/op_489 / cpp/op_777 -- **core difference**
  - c/op_489 / cpp/op_993 -- **core difference**
  - c/op_525 / cpp/op_129 -- **core difference**
  - c/op_525 / cpp/op_165 -- **core difference**
  - c/op_525 / cpp/op_201 -- **core difference**
  - c/op_525 / cpp/op_237 -- **core difference**
  - c/op_525 / cpp/op_489 -- **core difference**
  - c/op_525 / cpp/op_525 -- **total equality**
  - c/op_525 / cpp/op_561 -- **core difference**
  - c/op_525 / cpp/op_597 -- **core difference**
  - c/op_525 / cpp/op_633 -- **core difference**
  - c/op_525 / cpp/op_669 -- **core difference**
  - c/op_525 / cpp/op_777 -- **core difference**
  - c/op_525 / cpp/op_993 -- **total equality**
  - c/op_561 / cpp/op_129 -- **core difference**
  - c/op_561 / cpp/op_165 -- **core difference**
  - c/op_561 / cpp/op_201 -- **core difference**
  - c/op_561 / cpp/op_237 -- **core difference**
  - c/op_561 / cpp/op_489 -- **core difference**
  - c/op_561 / cpp/op_525 -- **core difference**
  - c/op_561 / cpp/op_561 -- **core difference**
  - c/op_561 / cpp/op_597 -- **core difference**
  - c/op_561 / cpp/op_633 -- **core difference**
  - c/op_561 / cpp/op_669 -- **core difference**
  - c/op_561 / cpp/op_777 -- **core difference**
  - c/op_561 / cpp/op_993 -- **core difference**
  - c/op_597 / cpp/op_129 -- **core difference**
  - c/op_597 / cpp/op_165 -- **core difference**
  - c/op_597 / cpp/op_201 -- **core difference**
  - c/op_597 / cpp/op_237 -- **core difference**
  - c/op_597 / cpp/op_489 -- **core difference**
  - c/op_597 / cpp/op_525 -- **core difference**
  - c/op_597 / cpp/op_561 -- **core difference**
  - c/op_597 / cpp/op_597 -- **core difference**
  - c/op_597 / cpp/op_633 -- **core difference**
  - c/op_597 / cpp/op_669 -- **core difference**
  - c/op_597 / cpp/op_777 -- **core difference**
  - c/op_597 / cpp/op_993 -- **core difference**
  - c/op_633 / cpp/op_129 -- **core difference**
  - c/op_633 / cpp/op_165 -- **core difference**
  - c/op_633 / cpp/op_201 -- **core difference**
  - c/op_633 / cpp/op_237 -- **core difference**
  - c/op_633 / cpp/op_489 -- **core difference**
  - c/op_633 / cpp/op_525 -- **core difference**
  - c/op_633 / cpp/op_561 -- **core difference**
  - c/op_633 / cpp/op_597 -- **core difference**
  - c/op_633 / cpp/op_633 -- **core difference**
  - c/op_633 / cpp/op_669 -- **core difference**
  - c/op_633 / cpp/op_777 -- **core difference**
  - c/op_633 / cpp/op_993 -- **core difference**
  - c/op_669 / cpp/op_129 -- **core difference**
  - c/op_669 / cpp/op_165 -- **core difference**
  - c/op_669 / cpp/op_201 -- **core difference**
  - c/op_669 / cpp/op_237 -- **core difference**
  - c/op_669 / cpp/op_489 -- **core difference**
  - c/op_669 / cpp/op_525 -- **core difference**
  - c/op_669 / cpp/op_561 -- **core difference**
  - c/op_669 / cpp/op_597 -- **core difference**
  - c/op_669 / cpp/op_633 -- **core difference**
  - c/op_669 / cpp/op_669 -- **core difference**
  - c/op_669 / cpp/op_777 -- **core difference**
  - c/op_669 / cpp/op_993 -- **core difference**

### shared-core group F32toF64(ex32@0(in1:256)) · (f64,f32)

- ground: connection
- languages: c, cpp
- members: c `+` (f64,f32, 0 modes); c `-` (f64,f32, 0 modes); c `*` (f64,f32, 0 modes); c `/` (f64,f32, 0 modes); c `||` (f64,f32, 0 modes); c `&&` (f64,f32, 0 modes); c `==` (f64,f32, 0 modes); c `!=` (f64,f32, 0 modes); c `>` (f64,f32, 0 modes); c `>=` (f64,f32, 0 modes); c `<=` (f64,f32, 0 modes); c `<` (f64,f32, 0 modes); cpp `+` (f64,f32, 0 modes); cpp `-` (f64,f32, 0 modes); cpp `*` (f64,f32, 0 modes); cpp `/` (f64,f32, 0 modes); cpp `||` (f64,f32, 0 modes); cpp `&&` (f64,f32, 0 modes); cpp `==` (f64,f32, 0 modes); cpp `!=` (f64,f32, 0 modes); cpp `>` (f64,f32, 0 modes); cpp `>=` (f64,f32, 0 modes); cpp `<=` (f64,f32, 0 modes); cpp `<` (f64,f32, 0 modes); cpp `<=>` (f64,f32, 0 modes); cpp `or` (f64,f32, 0 modes); cpp `and` (f64,f32, 0 modes); cpp `not_eq` (f64,f32, 0 modes)

  - c/op_129 / cpp/op_129 -- **total equality**
  - c/op_129 / cpp/op_165 -- **core difference**
  - c/op_129 / cpp/op_201 -- **core difference**
  - c/op_129 / cpp/op_237 -- **core difference**
  - c/op_129 / cpp/op_309 -- **core difference**
  - c/op_129 / cpp/op_345 -- **core difference**
  - c/op_129 / cpp/op_489 -- **core difference**
  - c/op_129 / cpp/op_525 -- **core difference**
  - c/op_129 / cpp/op_561 -- **core difference**
  - c/op_129 / cpp/op_597 -- **core difference**
  - c/op_129 / cpp/op_633 -- **core difference**
  - c/op_129 / cpp/op_669 -- **core difference**
  - c/op_129 / cpp/op_777 -- **core difference**
  - c/op_129 / cpp/op_813 -- **core difference**
  - c/op_129 / cpp/op_849 -- **core difference**
  - c/op_129 / cpp/op_993 -- **core difference**
  - c/op_165 / cpp/op_129 -- **core difference**
  - c/op_165 / cpp/op_165 -- **total equality**
  - c/op_165 / cpp/op_201 -- **core difference**
  - c/op_165 / cpp/op_237 -- **core difference**
  - c/op_165 / cpp/op_309 -- **core difference**
  - c/op_165 / cpp/op_345 -- **core difference**
  - c/op_165 / cpp/op_489 -- **core difference**
  - c/op_165 / cpp/op_525 -- **core difference**
  - c/op_165 / cpp/op_561 -- **core difference**
  - c/op_165 / cpp/op_597 -- **core difference**
  - c/op_165 / cpp/op_633 -- **core difference**
  - c/op_165 / cpp/op_669 -- **core difference**
  - c/op_165 / cpp/op_777 -- **core difference**
  - c/op_165 / cpp/op_813 -- **core difference**
  - c/op_165 / cpp/op_849 -- **core difference**
  - c/op_165 / cpp/op_993 -- **core difference**
  - c/op_201 / cpp/op_129 -- **core difference**
  - c/op_201 / cpp/op_165 -- **core difference**
  - c/op_201 / cpp/op_201 -- **total equality**
  - c/op_201 / cpp/op_237 -- **core difference**
  - c/op_201 / cpp/op_309 -- **core difference**
  - c/op_201 / cpp/op_345 -- **core difference**
  - c/op_201 / cpp/op_489 -- **core difference**
  - c/op_201 / cpp/op_525 -- **core difference**
  - c/op_201 / cpp/op_561 -- **core difference**
  - c/op_201 / cpp/op_597 -- **core difference**
  - c/op_201 / cpp/op_633 -- **core difference**
  - c/op_201 / cpp/op_669 -- **core difference**
  - c/op_201 / cpp/op_777 -- **core difference**
  - c/op_201 / cpp/op_813 -- **core difference**
  - c/op_201 / cpp/op_849 -- **core difference**
  - c/op_201 / cpp/op_993 -- **core difference**
  - c/op_237 / cpp/op_129 -- **core difference**
  - c/op_237 / cpp/op_165 -- **core difference**
  - c/op_237 / cpp/op_201 -- **core difference**
  - c/op_237 / cpp/op_237 -- **total equality**
  - c/op_237 / cpp/op_309 -- **core difference**
  - c/op_237 / cpp/op_345 -- **core difference**
  - c/op_237 / cpp/op_489 -- **core difference**
  - c/op_237 / cpp/op_525 -- **core difference**
  - c/op_237 / cpp/op_561 -- **core difference**
  - c/op_237 / cpp/op_597 -- **core difference**
  - c/op_237 / cpp/op_633 -- **core difference**
  - c/op_237 / cpp/op_669 -- **core difference**
  - c/op_237 / cpp/op_777 -- **core difference**
  - c/op_237 / cpp/op_813 -- **core difference**
  - c/op_237 / cpp/op_849 -- **core difference**
  - c/op_237 / cpp/op_993 -- **core difference**
  - c/op_309 / cpp/op_129 -- **core difference**
  - c/op_309 / cpp/op_165 -- **core difference**
  - c/op_309 / cpp/op_201 -- **core difference**
  - c/op_309 / cpp/op_237 -- **core difference**
  - c/op_309 / cpp/op_309 -- **core difference**
  - c/op_309 / cpp/op_345 -- **core difference**
  - c/op_309 / cpp/op_489 -- **core difference**
  - c/op_309 / cpp/op_525 -- **core difference**
  - c/op_309 / cpp/op_561 -- **core difference**
  - c/op_309 / cpp/op_597 -- **core difference**
  - c/op_309 / cpp/op_633 -- **core difference**
  - c/op_309 / cpp/op_669 -- **core difference**
  - c/op_309 / cpp/op_777 -- **core difference**
  - c/op_309 / cpp/op_813 -- **core difference**
  - c/op_309 / cpp/op_849 -- **core difference**
  - c/op_309 / cpp/op_993 -- **core difference**
  - c/op_345 / cpp/op_129 -- **core difference**
  - c/op_345 / cpp/op_165 -- **core difference**
  - c/op_345 / cpp/op_201 -- **core difference**
  - c/op_345 / cpp/op_237 -- **core difference**
  - c/op_345 / cpp/op_309 -- **core difference**
  - c/op_345 / cpp/op_345 -- **core difference**
  - c/op_345 / cpp/op_489 -- **core difference**
  - c/op_345 / cpp/op_525 -- **core difference**
  - c/op_345 / cpp/op_561 -- **core difference**
  - c/op_345 / cpp/op_597 -- **core difference**
  - c/op_345 / cpp/op_633 -- **core difference**
  - c/op_345 / cpp/op_669 -- **core difference**
  - c/op_345 / cpp/op_777 -- **core difference**
  - c/op_345 / cpp/op_813 -- **core difference**
  - c/op_345 / cpp/op_849 -- **core difference**
  - c/op_345 / cpp/op_993 -- **core difference**
  - c/op_489 / cpp/op_129 -- **core difference**
  - c/op_489 / cpp/op_165 -- **core difference**
  - c/op_489 / cpp/op_201 -- **core difference**
  - c/op_489 / cpp/op_237 -- **core difference**
  - c/op_489 / cpp/op_309 -- **core difference**
  - c/op_489 / cpp/op_345 -- **core difference**
  - c/op_489 / cpp/op_489 -- **total equality**
  - c/op_489 / cpp/op_525 -- **core difference**
  - c/op_489 / cpp/op_561 -- **core difference**
  - c/op_489 / cpp/op_597 -- **core difference**
  - c/op_489 / cpp/op_633 -- **core difference**
  - c/op_489 / cpp/op_669 -- **core difference**
  - c/op_489 / cpp/op_777 -- **core difference**
  - c/op_489 / cpp/op_813 -- **core difference**
  - c/op_489 / cpp/op_849 -- **core difference**
  - c/op_489 / cpp/op_993 -- **core difference**
  - c/op_525 / cpp/op_129 -- **core difference**
  - c/op_525 / cpp/op_165 -- **core difference**
  - c/op_525 / cpp/op_201 -- **core difference**
  - c/op_525 / cpp/op_237 -- **core difference**
  - c/op_525 / cpp/op_309 -- **core difference**
  - c/op_525 / cpp/op_345 -- **core difference**
  - c/op_525 / cpp/op_489 -- **core difference**
  - c/op_525 / cpp/op_525 -- **total equality**
  - c/op_525 / cpp/op_561 -- **core difference**
  - c/op_525 / cpp/op_597 -- **core difference**
  - c/op_525 / cpp/op_633 -- **core difference**
  - c/op_525 / cpp/op_669 -- **core difference**
  - c/op_525 / cpp/op_777 -- **core difference**
  - c/op_525 / cpp/op_813 -- **core difference**
  - c/op_525 / cpp/op_849 -- **core difference**
  - c/op_525 / cpp/op_993 -- **total equality**
  - c/op_561 / cpp/op_129 -- **core difference**
  - c/op_561 / cpp/op_165 -- **core difference**
  - c/op_561 / cpp/op_201 -- **core difference**
  - c/op_561 / cpp/op_237 -- **core difference**
  - c/op_561 / cpp/op_309 -- **core difference**
  - c/op_561 / cpp/op_345 -- **core difference**
  - c/op_561 / cpp/op_489 -- **core difference**
  - c/op_561 / cpp/op_525 -- **core difference**
  - c/op_561 / cpp/op_561 -- **core difference**
  - c/op_561 / cpp/op_597 -- **core difference**
  - c/op_561 / cpp/op_633 -- **core difference**
  - c/op_561 / cpp/op_669 -- **core difference**
  - c/op_561 / cpp/op_777 -- **core difference**
  - c/op_561 / cpp/op_813 -- **core difference**
  - c/op_561 / cpp/op_849 -- **core difference**
  - c/op_561 / cpp/op_993 -- **core difference**
  - c/op_597 / cpp/op_129 -- **core difference**
  - c/op_597 / cpp/op_165 -- **core difference**
  - c/op_597 / cpp/op_201 -- **core difference**
  - c/op_597 / cpp/op_237 -- **core difference**
  - c/op_597 / cpp/op_309 -- **core difference**
  - c/op_597 / cpp/op_345 -- **core difference**
  - c/op_597 / cpp/op_489 -- **core difference**
  - c/op_597 / cpp/op_525 -- **core difference**
  - c/op_597 / cpp/op_561 -- **core difference**
  - c/op_597 / cpp/op_597 -- **core difference**
  - c/op_597 / cpp/op_633 -- **core difference**
  - c/op_597 / cpp/op_669 -- **core difference**
  - c/op_597 / cpp/op_777 -- **core difference**
  - c/op_597 / cpp/op_813 -- **core difference**
  - c/op_597 / cpp/op_849 -- **core difference**
  - c/op_597 / cpp/op_993 -- **core difference**
  - c/op_633 / cpp/op_129 -- **core difference**
  - c/op_633 / cpp/op_165 -- **core difference**
  - c/op_633 / cpp/op_201 -- **core difference**
  - c/op_633 / cpp/op_237 -- **core difference**
  - c/op_633 / cpp/op_309 -- **core difference**
  - c/op_633 / cpp/op_345 -- **core difference**
  - c/op_633 / cpp/op_489 -- **core difference**
  - c/op_633 / cpp/op_525 -- **core difference**
  - c/op_633 / cpp/op_561 -- **core difference**
  - c/op_633 / cpp/op_597 -- **core difference**
  - c/op_633 / cpp/op_633 -- **core difference**
  - c/op_633 / cpp/op_669 -- **core difference**
  - c/op_633 / cpp/op_777 -- **core difference**
  - c/op_633 / cpp/op_813 -- **core difference**
  - c/op_633 / cpp/op_849 -- **core difference**
  - c/op_633 / cpp/op_993 -- **core difference**
  - c/op_669 / cpp/op_129 -- **core difference**
  - c/op_669 / cpp/op_165 -- **core difference**
  - c/op_669 / cpp/op_201 -- **core difference**
  - c/op_669 / cpp/op_237 -- **core difference**
  - c/op_669 / cpp/op_309 -- **core difference**
  - c/op_669 / cpp/op_345 -- **core difference**
  - c/op_669 / cpp/op_489 -- **core difference**
  - c/op_669 / cpp/op_525 -- **core difference**
  - c/op_669 / cpp/op_561 -- **core difference**
  - c/op_669 / cpp/op_597 -- **core difference**
  - c/op_669 / cpp/op_633 -- **core difference**
  - c/op_669 / cpp/op_669 -- **core difference**
  - c/op_669 / cpp/op_777 -- **core difference**
  - c/op_669 / cpp/op_813 -- **core difference**
  - c/op_669 / cpp/op_849 -- **core difference**
  - c/op_669 / cpp/op_993 -- **core difference**

### shared-core group ex32@0(AndV128(XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(in0:256),0:128)),XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(in1:256),0:128)))) · (f64,f64)

- ground: connection
- languages: c, cpp
- members: c `&&` (f64,f64, 0 modes); cpp `&&` (f64,f64, 0 modes); cpp `and` (f64,f64, 0 modes)

  - c/op_346 / cpp/op_346 -- **core difference**
  - c/op_346 / cpp/op_850 -- **core difference**

### shared-core group ex32@0(OrV128(XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(in0:256),0:128)),XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(in1:256),0:128)))) · (f64,f64)

- ground: connection
- languages: c, cpp
- members: c `||` (f64,f64, 0 modes); cpp `||` (f64,f64, 0 modes); cpp `or` (f64,f64, 0 modes)

  - c/op_310 / cpp/op_310 -- **core difference**
  - c/op_310 / cpp/op_814 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(in1:256)))),0:64,u0:64))) · (f64,f64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `>` (f64,f64, 0 modes); cpp `>` (f64,f64, 0 modes); go `>` (f64,f64, 0 modes); rust `>` (f64,f64, 0 modes); swift `>` (f64,f64, 0 modes)

  - c/op_562 / cpp/op_562 -- **core difference**
  - c/op_562 / go/op_628 -- **core difference**
  - c/op_562 / rust/op_418 -- **core difference**
  - c/op_562 / swift/op_358 -- **core difference**
  - cpp/op_562 / go/op_628 -- **total equality**
  - cpp/op_562 / rust/op_418 -- **total equality**
  - cpp/op_562 / swift/op_358 -- **total equality**
  - go/op_628 / rust/op_418 -- **total equality**
  - go/op_628 / swift/op_358 -- **total equality**
  - rust/op_418 / swift/op_358 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(in1:256)))),0:64,u0:64))) · (f64,f64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `>=` (f64,f64, 0 modes); cpp `>=` (f64,f64, 0 modes); go `>=` (f64,f64, 0 modes); rust `>=` (f64,f64, 0 modes); swift `>=` (f64,f64, 0 modes)

  - c/op_598 / cpp/op_598 -- **core difference**
  - c/op_598 / go/op_664 -- **core difference**
  - c/op_598 / rust/op_454 -- **core difference**
  - c/op_598 / swift/op_430 -- **core difference**
  - cpp/op_598 / go/op_664 -- **total equality**
  - cpp/op_598 / rust/op_454 -- **total equality**
  - cpp/op_598 / swift/op_430 -- **total equality**
  - go/op_664 / rust/op_454 -- **total equality**
  - go/op_664 / swift/op_430 -- **total equality**
  - rust/op_454 / swift/op_430 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(in0:256)))),0:64,u0:64))) · (f64,f64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `<=` (f64,f64, 0 modes); cpp `<=` (f64,f64, 0 modes); go `<=` (f64,f64, 0 modes); rust `<=` (f64,f64, 0 modes); swift `<=` (f64,f64, 0 modes)

  - c/op_634 / cpp/op_634 -- **core difference**
  - c/op_634 / go/op_592 -- **core difference**
  - c/op_634 / rust/op_382 -- **core difference**
  - c/op_634 / swift/op_394 -- **core difference**
  - cpp/op_634 / go/op_592 -- **total equality**
  - cpp/op_634 / rust/op_382 -- **total equality**
  - cpp/op_634 / swift/op_394 -- **total equality**
  - go/op_592 / rust/op_382 -- **total equality**
  - go/op_592 / swift/op_394 -- **total equality**
  - rust/op_382 / swift/op_394 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(in0:256)))),0:64,u0:64))) · (f64,f64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `<` (f64,f64, 0 modes); cpp `<` (f64,f64, 0 modes); go `<` (f64,f64, 0 modes); rust `<` (f64,f64, 0 modes); swift `<` (f64,f64, 0 modes)

  - c/op_670 / cpp/op_670 -- **core difference**
  - c/op_670 / go/op_556 -- **core difference**
  - c/op_670 / rust/op_346 -- **core difference**
  - c/op_670 / swift/op_322 -- **core difference**
  - cpp/op_670 / go/op_556 -- **total equality**
  - cpp/op_670 / rust/op_346 -- **total equality**
  - cpp/op_670 / swift/op_322 -- **total equality**
  - go/op_556 / rust/op_346 -- **total equality**
  - go/op_556 / swift/op_322 -- **total equality**
  - rust/op_346 / swift/op_322 -- **total equality**

### shared-core group zx64(And32(1:32,ex32@0(XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(in0:256),ex128@0(in1:256)))))) · (f64,f64)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `!=` (f64,f64, 0 modes); cpp `!=` (f64,f64, 0 modes); cpp `not_eq` (f64,f64, 0 modes); rust `!=` (f64,f64, 0 modes); swift `!=` (f64,f64, 0 modes)

  - c/op_526 / cpp/op_526 -- **total equality**
  - c/op_526 / cpp/op_994 -- **total equality**
  - c/op_526 / rust/op_310 -- **total equality**
  - c/op_526 / swift/op_466 -- **total equality**
  - cpp/op_526 / rust/op_310 -- **total equality**
  - cpp/op_994 / rust/op_310 -- **total equality**
  - cpp/op_526 / swift/op_466 -- **total equality**
  - cpp/op_994 / swift/op_466 -- **total equality**
  - rust/op_310 / swift/op_466 -- **total equality**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(in0:256,CmpEQ64F0x2(ex128@0(in0:256),ex128@0(in1:256)))))) · (f64,f64)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `==` (f64,f64, 0 modes); cpp `==` (f64,f64, 0 modes); rust `==` (f64,f64, 0 modes); swift `==` (f64,f64, 0 modes)

  - c/op_490 / cpp/op_490 -- **total equality**
  - c/op_490 / rust/op_274 -- **total equality**
  - c/op_490 / swift/op_538 -- **total equality**
  - cpp/op_490 / rust/op_274 -- **total equality**
  - cpp/op_490 / swift/op_538 -- **total equality**
  - rust/op_274 / swift/op_538 -- **total equality**

### shared-core group XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(in0:256),0:128)) · (f64,f64)

- ground: connection
- languages: c, cpp
- members: c `||` (f64,f64, 0 modes); c `&&` (f64,f64, 0 modes); cpp `||` (f64,f64, 0 modes); cpp `&&` (f64,f64, 0 modes); cpp `or` (f64,f64, 0 modes); cpp `and` (f64,f64, 0 modes)

  - c/op_310 / cpp/op_310 -- **core difference**
  - c/op_310 / cpp/op_346 -- **core difference**
  - c/op_310 / cpp/op_814 -- **core difference**
  - c/op_310 / cpp/op_850 -- **core difference**
  - c/op_346 / cpp/op_310 -- **core difference**
  - c/op_346 / cpp/op_346 -- **core difference**
  - c/op_346 / cpp/op_814 -- **core difference**
  - c/op_346 / cpp/op_850 -- **core difference**

### shared-core group XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(in1:256),0:128)) · (f64,f64)

- ground: connection
- languages: c, cpp
- members: c `||` (f64,f64, 0 modes); c `&&` (f64,f64, 0 modes); cpp `||` (f64,f64, 0 modes); cpp `&&` (f64,f64, 0 modes); cpp `or` (f64,f64, 0 modes); cpp `and` (f64,f64, 0 modes)

  - c/op_310 / cpp/op_310 -- **core difference**
  - c/op_310 / cpp/op_346 -- **core difference**
  - c/op_310 / cpp/op_814 -- **core difference**
  - c/op_310 / cpp/op_850 -- **core difference**
  - c/op_346 / cpp/op_310 -- **core difference**
  - c/op_346 / cpp/op_346 -- **core difference**
  - c/op_346 / cpp/op_814 -- **core difference**
  - c/op_346 / cpp/op_850 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(in1:256)))) · (f64,f64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `>` (f64,f64, 0 modes); c `>=` (f64,f64, 0 modes); cpp `>` (f64,f64, 0 modes); cpp `>=` (f64,f64, 0 modes); cpp `<=>` (f64,f64, 0 modes); go `==` (f64,f64, 0 modes); go `!=` (f64,f64, 0 modes); go `>` (f64,f64, 0 modes); go `>=` (f64,f64, 0 modes); rust `>` (f64,f64, 0 modes); rust `>=` (f64,f64, 0 modes); swift `>` (f64,f64, 0 modes); swift `>=` (f64,f64, 0 modes)

  - c/op_562 / cpp/op_562 -- **core difference**
  - c/op_562 / cpp/op_598 -- **core difference**
  - c/op_562 / cpp/op_778 -- **core difference**
  - c/op_598 / cpp/op_562 -- **core difference**
  - c/op_598 / cpp/op_598 -- **core difference**
  - c/op_598 / cpp/op_778 -- **core difference**
  - c/op_562 / go/op_484 -- **core difference**
  - c/op_562 / go/op_520 -- **core difference**
  - c/op_562 / go/op_628 -- **core difference**
  - c/op_562 / go/op_664 -- **core difference**
  - c/op_598 / go/op_484 -- **core difference**
  - c/op_598 / go/op_520 -- **core difference**
  - c/op_598 / go/op_628 -- **core difference**
  - c/op_598 / go/op_664 -- **core difference**
  - c/op_562 / rust/op_418 -- **core difference**
  - c/op_562 / rust/op_454 -- **core difference**
  - c/op_598 / rust/op_418 -- **core difference**
  - c/op_598 / rust/op_454 -- **core difference**
  - c/op_562 / swift/op_358 -- **core difference**
  - c/op_562 / swift/op_430 -- **core difference**
  - c/op_598 / swift/op_358 -- **core difference**
  - c/op_598 / swift/op_430 -- **core difference**
  - cpp/op_562 / go/op_484 -- **core difference**
  - cpp/op_562 / go/op_520 -- **core difference**
  - cpp/op_562 / go/op_628 -- **total equality**
  - cpp/op_562 / go/op_664 -- **core difference**
  - cpp/op_598 / go/op_484 -- **core difference**
  - cpp/op_598 / go/op_520 -- **core difference**
  - cpp/op_598 / go/op_628 -- **core difference**
  - cpp/op_598 / go/op_664 -- **total equality**
  - cpp/op_778 / go/op_484 -- **core difference**
  - cpp/op_778 / go/op_520 -- **core difference**
  - cpp/op_778 / go/op_628 -- **core difference**
  - cpp/op_778 / go/op_664 -- **core difference**
  - cpp/op_562 / rust/op_418 -- **total equality**
  - cpp/op_562 / rust/op_454 -- **core difference**
  - cpp/op_598 / rust/op_418 -- **core difference**
  - cpp/op_598 / rust/op_454 -- **total equality**
  - cpp/op_778 / rust/op_418 -- **core difference**
  - cpp/op_778 / rust/op_454 -- **core difference**
  - cpp/op_562 / swift/op_358 -- **total equality**
  - cpp/op_562 / swift/op_430 -- **core difference**
  - cpp/op_598 / swift/op_358 -- **core difference**
  - cpp/op_598 / swift/op_430 -- **total equality**
  - cpp/op_778 / swift/op_358 -- **core difference**
  - cpp/op_778 / swift/op_430 -- **core difference**
  - go/op_484 / rust/op_418 -- **core difference**
  - go/op_484 / rust/op_454 -- **core difference**
  - go/op_520 / rust/op_418 -- **core difference**
  - go/op_520 / rust/op_454 -- **core difference**
  - go/op_628 / rust/op_418 -- **total equality**
  - go/op_628 / rust/op_454 -- **core difference**
  - go/op_664 / rust/op_418 -- **core difference**
  - go/op_664 / rust/op_454 -- **total equality**
  - go/op_484 / swift/op_358 -- **core difference**
  - go/op_484 / swift/op_430 -- **core difference**
  - go/op_520 / swift/op_358 -- **core difference**
  - go/op_520 / swift/op_430 -- **core difference**
  - go/op_628 / swift/op_358 -- **total equality**
  - go/op_628 / swift/op_430 -- **core difference**
  - go/op_664 / swift/op_358 -- **core difference**
  - go/op_664 / swift/op_430 -- **total equality**
  - rust/op_418 / swift/op_358 -- **total equality**
  - rust/op_418 / swift/op_430 -- **core difference**
  - rust/op_454 / swift/op_358 -- **core difference**
  - rust/op_454 / swift/op_430 -- **total equality**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(in0:256)))) · (f64,f64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `<=` (f64,f64, 0 modes); c `<` (f64,f64, 0 modes); cpp `<=` (f64,f64, 0 modes); cpp `<` (f64,f64, 0 modes); cpp `<=>` (f64,f64, 0 modes); go `<` (f64,f64, 0 modes); go `<=` (f64,f64, 0 modes); rust `<` (f64,f64, 0 modes); rust `<=` (f64,f64, 0 modes); swift `<` (f64,f64, 0 modes); swift `<=` (f64,f64, 0 modes); swift `..<` (f64,f64, 1 modes); swift `...` (f64,f64, 1 modes)

  - c/op_634 / cpp/op_634 -- **core difference**
  - c/op_634 / cpp/op_670 -- **core difference**
  - c/op_634 / cpp/op_778 -- **core difference**
  - c/op_670 / cpp/op_634 -- **core difference**
  - c/op_670 / cpp/op_670 -- **core difference**
  - c/op_670 / cpp/op_778 -- **core difference**
  - c/op_634 / go/op_556 -- **core difference**
  - c/op_634 / go/op_592 -- **core difference**
  - c/op_670 / go/op_556 -- **core difference**
  - c/op_670 / go/op_592 -- **core difference**
  - c/op_634 / rust/op_346 -- **core difference**
  - c/op_634 / rust/op_382 -- **core difference**
  - c/op_670 / rust/op_346 -- **core difference**
  - c/op_670 / rust/op_382 -- **core difference**
  - c/op_634 / swift/op_322 -- **core difference**
  - c/op_634 / swift/op_394 -- **core difference**
  - c/op_634 / swift/op_898 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(ex64@0(in1:256),ex64@0(in0:256))), 0)` -> `trap` (branch-to-response)
  - c/op_634 / swift/op_934 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(ex64@0(in1:256),ex64@0(in0:256))), 0)` -> `trap` (branch-to-response)
  - c/op_670 / swift/op_322 -- **core difference**
  - c/op_670 / swift/op_394 -- **core difference**
  - c/op_670 / swift/op_898 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(ex64@0(in1:256),ex64@0(in0:256))), 0)` -> `trap` (branch-to-response)
  - c/op_670 / swift/op_934 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(ex64@0(in1:256),ex64@0(in0:256))), 0)` -> `trap` (branch-to-response)
  - cpp/op_634 / go/op_556 -- **core difference**
  - cpp/op_634 / go/op_592 -- **total equality**
  - cpp/op_670 / go/op_556 -- **total equality**
  - cpp/op_670 / go/op_592 -- **core difference**
  - cpp/op_778 / go/op_556 -- **core difference**
  - cpp/op_778 / go/op_592 -- **core difference**
  - cpp/op_634 / rust/op_346 -- **core difference**
  - cpp/op_634 / rust/op_382 -- **total equality**
  - cpp/op_670 / rust/op_346 -- **total equality**
  - cpp/op_670 / rust/op_382 -- **core difference**
  - cpp/op_778 / rust/op_346 -- **core difference**
  - cpp/op_778 / rust/op_382 -- **core difference**
  - cpp/op_634 / swift/op_322 -- **core difference**
  - cpp/op_634 / swift/op_394 -- **total equality**
  - cpp/op_634 / swift/op_898 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(ex64@0(in1:256),ex64@0(in0:256))), 0)` -> `trap` (branch-to-response)
  - cpp/op_634 / swift/op_934 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(ex64@0(in1:256),ex64@0(in0:256))), 0)` -> `trap` (branch-to-response)
  - cpp/op_670 / swift/op_322 -- **total equality**
  - cpp/op_670 / swift/op_394 -- **core difference**
  - cpp/op_670 / swift/op_898 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(ex64@0(in1:256),ex64@0(in0:256))), 0)` -> `trap` (branch-to-response)
  - cpp/op_670 / swift/op_934 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(ex64@0(in1:256),ex64@0(in0:256))), 0)` -> `trap` (branch-to-response)
  - cpp/op_778 / swift/op_322 -- **core difference**
  - cpp/op_778 / swift/op_394 -- **core difference**
  - cpp/op_778 / swift/op_898 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(ex64@0(in1:256),ex64@0(in0:256))), 0)` -> `trap` (branch-to-response)
  - cpp/op_778 / swift/op_934 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(ex64@0(in1:256),ex64@0(in0:256))), 0)` -> `trap` (branch-to-response)
  - go/op_556 / rust/op_346 -- **total equality**
  - go/op_556 / rust/op_382 -- **core difference**
  - go/op_592 / rust/op_346 -- **core difference**
  - go/op_592 / rust/op_382 -- **total equality**
  - go/op_556 / swift/op_322 -- **total equality**
  - go/op_556 / swift/op_394 -- **core difference**
  - go/op_556 / swift/op_898 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(ex64@0(in1:256),ex64@0(in0:256))), 0)` -> `trap` (branch-to-response)
  - go/op_556 / swift/op_934 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(ex64@0(in1:256),ex64@0(in0:256))), 0)` -> `trap` (branch-to-response)
  - go/op_592 / swift/op_322 -- **core difference**
  - go/op_592 / swift/op_394 -- **total equality**
  - go/op_592 / swift/op_898 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(ex64@0(in1:256),ex64@0(in0:256))), 0)` -> `trap` (branch-to-response)
  - go/op_592 / swift/op_934 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(ex64@0(in1:256),ex64@0(in0:256))), 0)` -> `trap` (branch-to-response)
  - rust/op_346 / swift/op_322 -- **total equality**
  - rust/op_346 / swift/op_394 -- **core difference**
  - rust/op_346 / swift/op_898 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(ex64@0(in1:256),ex64@0(in0:256))), 0)` -> `trap` (branch-to-response)
  - rust/op_346 / swift/op_934 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(ex64@0(in1:256),ex64@0(in0:256))), 0)` -> `trap` (branch-to-response)
  - rust/op_382 / swift/op_322 -- **core difference**
  - rust/op_382 / swift/op_394 -- **total equality**
  - rust/op_382 / swift/op_898 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(ex64@0(in1:256),ex64@0(in0:256))), 0)` -> `trap` (branch-to-response)
  - rust/op_382 / swift/op_934 -- **core difference**
    - only on the right: `B after COPY64((69 & CmpF64(ex64@0(in1:256),ex64@0(in0:256))), 0)` -> `trap` (branch-to-response)

### shared-core group CmpEQ64F0x2(ex128@0(in0:256),ex128@0(in1:256)) · (f64,f64)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `==` (f64,f64, 0 modes); c `!=` (f64,f64, 0 modes); cpp `==` (f64,f64, 0 modes); cpp `!=` (f64,f64, 0 modes); cpp `not_eq` (f64,f64, 0 modes); rust `==` (f64,f64, 0 modes); rust `!=` (f64,f64, 0 modes); swift `!=` (f64,f64, 0 modes); swift `==` (f64,f64, 0 modes)

  - c/op_490 / cpp/op_490 -- **total equality**
  - c/op_490 / cpp/op_526 -- **core difference**
  - c/op_490 / cpp/op_994 -- **core difference**
  - c/op_526 / cpp/op_490 -- **core difference**
  - c/op_526 / cpp/op_526 -- **total equality**
  - c/op_526 / cpp/op_994 -- **total equality**
  - c/op_490 / rust/op_274 -- **total equality**
  - c/op_490 / rust/op_310 -- **core difference**
  - c/op_526 / rust/op_274 -- **core difference**
  - c/op_526 / rust/op_310 -- **total equality**
  - c/op_490 / swift/op_466 -- **core difference**
  - c/op_490 / swift/op_538 -- **total equality**
  - c/op_526 / swift/op_466 -- **total equality**
  - c/op_526 / swift/op_538 -- **core difference**
  - cpp/op_490 / rust/op_274 -- **total equality**
  - cpp/op_490 / rust/op_310 -- **core difference**
  - cpp/op_526 / rust/op_274 -- **core difference**
  - cpp/op_526 / rust/op_310 -- **total equality**
  - cpp/op_994 / rust/op_274 -- **core difference**
  - cpp/op_994 / rust/op_310 -- **total equality**
  - cpp/op_490 / swift/op_466 -- **core difference**
  - cpp/op_490 / swift/op_538 -- **total equality**
  - cpp/op_526 / swift/op_466 -- **total equality**
  - cpp/op_526 / swift/op_538 -- **core difference**
  - cpp/op_994 / swift/op_466 -- **total equality**
  - cpp/op_994 / swift/op_538 -- **core difference**
  - rust/op_274 / swift/op_466 -- **core difference**
  - rust/op_274 / swift/op_538 -- **total equality**
  - rust/op_310 / swift/op_466 -- **total equality**
  - rust/op_310 / swift/op_538 -- **core difference**

### shared-core group Add64F0x2(ex128@0(in0:256),ex128@0(in1:256)) · (f64,f64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `+` (f64,f64, 0 modes); cpp `+` (f64,f64, 0 modes); go `+` (f64,f64, 0 modes); rust `+` (f64,f64, 0 modes); swift `+` (f64,f64, 0 modes)

  - c/op_130 / cpp/op_130 -- **total equality**
  - c/op_130 / go/op_340 -- **total equality**
  - c/op_130 / rust/op_562 -- **total equality**
  - c/op_130 / swift/op_250 -- **total equality**
  - cpp/op_130 / go/op_340 -- **total equality**
  - cpp/op_130 / rust/op_562 -- **total equality**
  - cpp/op_130 / swift/op_250 -- **total equality**
  - go/op_340 / rust/op_562 -- **total equality**
  - go/op_340 / swift/op_250 -- **total equality**
  - rust/op_562 / swift/op_250 -- **total equality**

### shared-core group Sub64F0x2(ex128@0(in0:256),ex128@0(in1:256)) · (f64,f64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `-` (f64,f64, 0 modes); cpp `-` (f64,f64, 0 modes); go `-` (f64,f64, 0 modes); rust `-` (f64,f64, 0 modes); swift `-` (f64,f64, 0 modes)

  - c/op_166 / cpp/op_166 -- **total equality**
  - c/op_166 / go/op_376 -- **total equality**
  - c/op_166 / rust/op_598 -- **total equality**
  - c/op_166 / swift/op_286 -- **total equality**
  - cpp/op_166 / go/op_376 -- **total equality**
  - cpp/op_166 / rust/op_598 -- **total equality**
  - cpp/op_166 / swift/op_286 -- **total equality**
  - go/op_376 / rust/op_598 -- **total equality**
  - go/op_376 / swift/op_286 -- **total equality**
  - rust/op_598 / swift/op_286 -- **total equality**

### shared-core group Mul64F0x2(ex128@0(in0:256),ex128@0(in1:256)) · (f64,f64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `*` (f64,f64, 0 modes); cpp `*` (f64,f64, 0 modes); go `*` (f64,f64, 0 modes); rust `*` (f64,f64, 0 modes); swift `*` (f64,f64, 0 modes)

  - c/op_202 / cpp/op_202 -- **total equality**
  - c/op_202 / go/op_88 -- **total equality**
  - c/op_202 / rust/op_634 -- **total equality**
  - c/op_202 / swift/op_142 -- **total equality**
  - cpp/op_202 / go/op_88 -- **total equality**
  - cpp/op_202 / rust/op_634 -- **total equality**
  - cpp/op_202 / swift/op_142 -- **total equality**
  - go/op_88 / rust/op_634 -- **total equality**
  - go/op_88 / swift/op_142 -- **total equality**
  - rust/op_634 / swift/op_142 -- **total equality**

### shared-core group Div64F0x2(ex128@0(in0:256),ex128@0(in1:256)) · (f64,f64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `/` (f64,f64, 0 modes); cpp `/` (f64,f64, 0 modes); go `/` (f64,f64, 0 modes); rust `/` (f64,f64, 0 modes); swift `/` (f64,f64, 0 modes)

  - c/op_238 / cpp/op_238 -- **total equality**
  - c/op_238 / go/op_124 -- **total equality**
  - c/op_238 / rust/op_670 -- **total equality**
  - c/op_238 / swift/op_178 -- **total equality**
  - cpp/op_238 / go/op_124 -- **total equality**
  - cpp/op_238 / rust/op_670 -- **total equality**
  - cpp/op_238 / swift/op_178 -- **total equality**
  - go/op_124 / rust/op_670 -- **total equality**
  - go/op_124 / swift/op_178 -- **total equality**
  - rust/op_670 / swift/op_178 -- **total equality**

### shared-core group And8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64)))) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `&&` (f64,i32, 0 modes); cpp `&&` (f64,i32, 0 modes); cpp `and` (f64,i32, 0 modes)

  - c/op_342 / cpp/op_342 -- **core difference**
  - c/op_342 / cpp/op_846 -- **core difference**

### shared-core group Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64)))) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `||` (f64,i32, 0 modes); cpp `||` (f64,i32, 0 modes); cpp `or` (f64,i32, 0 modes)

  - c/op_306 / cpp/op_306 -- **core difference**
  - c/op_306 / cpp/op_810 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64)))) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `||` (f64,i32, 0 modes); c `&&` (f64,i32, 0 modes); cpp `||` (f64,i32, 0 modes); cpp `&&` (f64,i32, 0 modes); cpp `or` (f64,i32, 0 modes); cpp `and` (f64,i32, 0 modes)

  - c/op_306 / cpp/op_306 -- **core difference**
  - c/op_306 / cpp/op_342 -- **core difference**
  - c/op_306 / cpp/op_810 -- **core difference**
  - c/op_306 / cpp/op_846 -- **core difference**
  - c/op_342 / cpp/op_306 -- **core difference**
  - c/op_342 / cpp/op_342 -- **core difference**
  - c/op_342 / cpp/op_810 -- **core difference**
  - c/op_342 / cpp/op_846 -- **core difference**

### shared-core group ins@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))),XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))),ex128@0(in0:256)))) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `!=` (f64,i32, 0 modes); cpp `!=` (f64,i32, 0 modes); cpp `not_eq` (f64,i32, 0 modes)

  - c/op_522 / cpp/op_522 -- **total equality**
  - c/op_522 / cpp/op_990 -- **total equality**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))),CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))),ex128@0(in0:256)))))) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `==` (f64,i32, 0 modes); cpp `==` (f64,i32, 0 modes)

  - c/op_486 / cpp/op_486 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))))))),0:64,u1:64))) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `>` (f64,i32, 0 modes); cpp `>` (f64,i32, 0 modes)

  - c/op_558 / cpp/op_558 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))))))),0:64,u1:64))) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `>=` (f64,i32, 0 modes); cpp `>=` (f64,i32, 0 modes)

  - c/op_594 / cpp/op_594 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))),ex64@0(in0:256)))),0:64,u1:64))) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `<=` (f64,i32, 0 modes); cpp `<=` (f64,i32, 0 modes)

  - c/op_630 / cpp/op_630 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))),ex64@0(in0:256)))),0:64,u1:64))) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `<` (f64,i32, 0 modes); cpp `<` (f64,i32, 0 modes)

  - c/op_666 / cpp/op_666 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))))))) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `>` (f64,i32, 0 modes); c `>=` (f64,i32, 0 modes); cpp `>` (f64,i32, 0 modes); cpp `>=` (f64,i32, 0 modes); cpp `<=>` (f64,i32, 0 modes)

  - c/op_558 / cpp/op_558 -- **core difference**
  - c/op_558 / cpp/op_594 -- **core difference**
  - c/op_558 / cpp/op_774 -- **core difference**
  - c/op_594 / cpp/op_558 -- **core difference**
  - c/op_594 / cpp/op_594 -- **core difference**
  - c/op_594 / cpp/op_774 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))),ex64@0(in0:256)))) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `<=` (f64,i32, 0 modes); c `<` (f64,i32, 0 modes); cpp `<=` (f64,i32, 0 modes); cpp `<` (f64,i32, 0 modes); cpp `<=>` (f64,i32, 0 modes)

  - c/op_630 / cpp/op_630 -- **core difference**
  - c/op_630 / cpp/op_666 -- **core difference**
  - c/op_630 / cpp/op_774 -- **core difference**
  - c/op_666 / cpp/op_630 -- **core difference**
  - c/op_666 / cpp/op_666 -- **core difference**
  - c/op_666 / cpp/op_774 -- **core difference**

### shared-core group CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))),ex128@0(in0:256)) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `==` (f64,i32, 0 modes); c `!=` (f64,i32, 0 modes); cpp `==` (f64,i32, 0 modes); cpp `!=` (f64,i32, 0 modes); cpp `not_eq` (f64,i32, 0 modes)

  - c/op_486 / cpp/op_486 -- **total equality**
  - c/op_486 / cpp/op_522 -- **core difference**
  - c/op_486 / cpp/op_990 -- **core difference**
  - c/op_522 / cpp/op_486 -- **core difference**
  - c/op_522 / cpp/op_522 -- **total equality**
  - c/op_522 / cpp/op_990 -- **total equality**

### shared-core group Add64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))))) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `+` (f64,i32, 0 modes); cpp `+` (f64,i32, 0 modes)

  - c/op_126 / cpp/op_126 -- **total equality**

### shared-core group Sub64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))))) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `-` (f64,i32, 0 modes); cpp `-` (f64,i32, 0 modes)

  - c/op_162 / cpp/op_162 -- **total equality**

### shared-core group Mul64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))))) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `*` (f64,i32, 0 modes); cpp `*` (f64,i32, 0 modes)

  - c/op_198 / cpp/op_198 -- **total equality**

### shared-core group Div64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64))))) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `/` (f64,i32, 0 modes); cpp `/` (f64,i32, 0 modes)

  - c/op_234 / cpp/op_234 -- **total equality**

### shared-core group ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `+` (f64,i32, 0 modes); c `-` (f64,i32, 0 modes); c `*` (f64,i32, 0 modes); c `/` (f64,i32, 0 modes); c `==` (f64,i32, 0 modes); c `!=` (f64,i32, 0 modes); cpp `+` (f64,i32, 0 modes); cpp `-` (f64,i32, 0 modes); cpp `*` (f64,i32, 0 modes); cpp `/` (f64,i32, 0 modes); cpp `==` (f64,i32, 0 modes); cpp `!=` (f64,i32, 0 modes); cpp `not_eq` (f64,i32, 0 modes)

  - c/op_126 / cpp/op_126 -- **total equality**
  - c/op_126 / cpp/op_162 -- **core difference**
  - c/op_126 / cpp/op_198 -- **core difference**
  - c/op_126 / cpp/op_234 -- **core difference**
  - c/op_126 / cpp/op_486 -- **core difference**
  - c/op_126 / cpp/op_522 -- **core difference**
  - c/op_126 / cpp/op_990 -- **core difference**
  - c/op_162 / cpp/op_126 -- **core difference**
  - c/op_162 / cpp/op_162 -- **total equality**
  - c/op_162 / cpp/op_198 -- **core difference**
  - c/op_162 / cpp/op_234 -- **core difference**
  - c/op_162 / cpp/op_486 -- **core difference**
  - c/op_162 / cpp/op_522 -- **core difference**
  - c/op_162 / cpp/op_990 -- **core difference**
  - c/op_198 / cpp/op_126 -- **core difference**
  - c/op_198 / cpp/op_162 -- **core difference**
  - c/op_198 / cpp/op_198 -- **total equality**
  - c/op_198 / cpp/op_234 -- **core difference**
  - c/op_198 / cpp/op_486 -- **core difference**
  - c/op_198 / cpp/op_522 -- **core difference**
  - c/op_198 / cpp/op_990 -- **core difference**
  - c/op_234 / cpp/op_126 -- **core difference**
  - c/op_234 / cpp/op_162 -- **core difference**
  - c/op_234 / cpp/op_198 -- **core difference**
  - c/op_234 / cpp/op_234 -- **total equality**
  - c/op_234 / cpp/op_486 -- **core difference**
  - c/op_234 / cpp/op_522 -- **core difference**
  - c/op_234 / cpp/op_990 -- **core difference**
  - c/op_486 / cpp/op_126 -- **core difference**
  - c/op_486 / cpp/op_162 -- **core difference**
  - c/op_486 / cpp/op_198 -- **core difference**
  - c/op_486 / cpp/op_234 -- **core difference**
  - c/op_486 / cpp/op_486 -- **total equality**
  - c/op_486 / cpp/op_522 -- **core difference**
  - c/op_486 / cpp/op_990 -- **core difference**
  - c/op_522 / cpp/op_126 -- **core difference**
  - c/op_522 / cpp/op_162 -- **core difference**
  - c/op_522 / cpp/op_198 -- **core difference**
  - c/op_522 / cpp/op_234 -- **core difference**
  - c/op_522 / cpp/op_486 -- **core difference**
  - c/op_522 / cpp/op_522 -- **total equality**
  - c/op_522 / cpp/op_990 -- **total equality**

### shared-core group ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in1:64)))) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `>` (f64,i32, 0 modes); c `>=` (f64,i32, 0 modes); c `<=` (f64,i32, 0 modes); c `<` (f64,i32, 0 modes); cpp `>` (f64,i32, 0 modes); cpp `>=` (f64,i32, 0 modes); cpp `<=` (f64,i32, 0 modes); cpp `<` (f64,i32, 0 modes); cpp `<=>` (f64,i32, 0 modes)

  - c/op_558 / cpp/op_558 -- **core difference**
  - c/op_558 / cpp/op_594 -- **core difference**
  - c/op_558 / cpp/op_630 -- **core difference**
  - c/op_558 / cpp/op_666 -- **core difference**
  - c/op_558 / cpp/op_774 -- **core difference**
  - c/op_594 / cpp/op_558 -- **core difference**
  - c/op_594 / cpp/op_594 -- **core difference**
  - c/op_594 / cpp/op_630 -- **core difference**
  - c/op_594 / cpp/op_666 -- **core difference**
  - c/op_594 / cpp/op_774 -- **core difference**
  - c/op_630 / cpp/op_558 -- **core difference**
  - c/op_630 / cpp/op_594 -- **core difference**
  - c/op_630 / cpp/op_630 -- **core difference**
  - c/op_630 / cpp/op_666 -- **core difference**
  - c/op_630 / cpp/op_774 -- **core difference**
  - c/op_666 / cpp/op_558 -- **core difference**
  - c/op_666 / cpp/op_594 -- **core difference**
  - c/op_666 / cpp/op_630 -- **core difference**
  - c/op_666 / cpp/op_666 -- **core difference**
  - c/op_666 / cpp/op_774 -- **core difference**

### shared-core group ins@0(u0:256,I32StoF64(ex32@0(in1:64))) · (f64,i32)

- ground: connection
- languages: c, cpp
- members: c `+` (f64,i32, 0 modes); c `-` (f64,i32, 0 modes); c `*` (f64,i32, 0 modes); c `/` (f64,i32, 0 modes); c `==` (f64,i32, 0 modes); c `!=` (f64,i32, 0 modes); c `>` (f64,i32, 0 modes); c `>=` (f64,i32, 0 modes); c `<=` (f64,i32, 0 modes); c `<` (f64,i32, 0 modes); cpp `+` (f64,i32, 0 modes); cpp `-` (f64,i32, 0 modes); cpp `*` (f64,i32, 0 modes); cpp `/` (f64,i32, 0 modes); cpp `==` (f64,i32, 0 modes); cpp `!=` (f64,i32, 0 modes); cpp `>` (f64,i32, 0 modes); cpp `>=` (f64,i32, 0 modes); cpp `<=` (f64,i32, 0 modes); cpp `<` (f64,i32, 0 modes); cpp `<=>` (f64,i32, 0 modes); cpp `not_eq` (f64,i32, 0 modes)

  - c/op_126 / cpp/op_126 -- **total equality**
  - c/op_126 / cpp/op_162 -- **core difference**
  - c/op_126 / cpp/op_198 -- **core difference**
  - c/op_126 / cpp/op_234 -- **core difference**
  - c/op_126 / cpp/op_486 -- **core difference**
  - c/op_126 / cpp/op_522 -- **core difference**
  - c/op_126 / cpp/op_558 -- **core difference**
  - c/op_126 / cpp/op_594 -- **core difference**
  - c/op_126 / cpp/op_630 -- **core difference**
  - c/op_126 / cpp/op_666 -- **core difference**
  - c/op_126 / cpp/op_774 -- **core difference**
  - c/op_126 / cpp/op_990 -- **core difference**
  - c/op_162 / cpp/op_126 -- **core difference**
  - c/op_162 / cpp/op_162 -- **total equality**
  - c/op_162 / cpp/op_198 -- **core difference**
  - c/op_162 / cpp/op_234 -- **core difference**
  - c/op_162 / cpp/op_486 -- **core difference**
  - c/op_162 / cpp/op_522 -- **core difference**
  - c/op_162 / cpp/op_558 -- **core difference**
  - c/op_162 / cpp/op_594 -- **core difference**
  - c/op_162 / cpp/op_630 -- **core difference**
  - c/op_162 / cpp/op_666 -- **core difference**
  - c/op_162 / cpp/op_774 -- **core difference**
  - c/op_162 / cpp/op_990 -- **core difference**
  - c/op_198 / cpp/op_126 -- **core difference**
  - c/op_198 / cpp/op_162 -- **core difference**
  - c/op_198 / cpp/op_198 -- **total equality**
  - c/op_198 / cpp/op_234 -- **core difference**
  - c/op_198 / cpp/op_486 -- **core difference**
  - c/op_198 / cpp/op_522 -- **core difference**
  - c/op_198 / cpp/op_558 -- **core difference**
  - c/op_198 / cpp/op_594 -- **core difference**
  - c/op_198 / cpp/op_630 -- **core difference**
  - c/op_198 / cpp/op_666 -- **core difference**
  - c/op_198 / cpp/op_774 -- **core difference**
  - c/op_198 / cpp/op_990 -- **core difference**
  - c/op_234 / cpp/op_126 -- **core difference**
  - c/op_234 / cpp/op_162 -- **core difference**
  - c/op_234 / cpp/op_198 -- **core difference**
  - c/op_234 / cpp/op_234 -- **total equality**
  - c/op_234 / cpp/op_486 -- **core difference**
  - c/op_234 / cpp/op_522 -- **core difference**
  - c/op_234 / cpp/op_558 -- **core difference**
  - c/op_234 / cpp/op_594 -- **core difference**
  - c/op_234 / cpp/op_630 -- **core difference**
  - c/op_234 / cpp/op_666 -- **core difference**
  - c/op_234 / cpp/op_774 -- **core difference**
  - c/op_234 / cpp/op_990 -- **core difference**
  - c/op_486 / cpp/op_126 -- **core difference**
  - c/op_486 / cpp/op_162 -- **core difference**
  - c/op_486 / cpp/op_198 -- **core difference**
  - c/op_486 / cpp/op_234 -- **core difference**
  - c/op_486 / cpp/op_486 -- **total equality**
  - c/op_486 / cpp/op_522 -- **core difference**
  - c/op_486 / cpp/op_558 -- **core difference**
  - c/op_486 / cpp/op_594 -- **core difference**
  - c/op_486 / cpp/op_630 -- **core difference**
  - c/op_486 / cpp/op_666 -- **core difference**
  - c/op_486 / cpp/op_774 -- **core difference**
  - c/op_486 / cpp/op_990 -- **core difference**
  - c/op_522 / cpp/op_126 -- **core difference**
  - c/op_522 / cpp/op_162 -- **core difference**
  - c/op_522 / cpp/op_198 -- **core difference**
  - c/op_522 / cpp/op_234 -- **core difference**
  - c/op_522 / cpp/op_486 -- **core difference**
  - c/op_522 / cpp/op_522 -- **total equality**
  - c/op_522 / cpp/op_558 -- **core difference**
  - c/op_522 / cpp/op_594 -- **core difference**
  - c/op_522 / cpp/op_630 -- **core difference**
  - c/op_522 / cpp/op_666 -- **core difference**
  - c/op_522 / cpp/op_774 -- **core difference**
  - c/op_522 / cpp/op_990 -- **total equality**
  - c/op_558 / cpp/op_126 -- **core difference**
  - c/op_558 / cpp/op_162 -- **core difference**
  - c/op_558 / cpp/op_198 -- **core difference**
  - c/op_558 / cpp/op_234 -- **core difference**
  - c/op_558 / cpp/op_486 -- **core difference**
  - c/op_558 / cpp/op_522 -- **core difference**
  - c/op_558 / cpp/op_558 -- **core difference**
  - c/op_558 / cpp/op_594 -- **core difference**
  - c/op_558 / cpp/op_630 -- **core difference**
  - c/op_558 / cpp/op_666 -- **core difference**
  - c/op_558 / cpp/op_774 -- **core difference**
  - c/op_558 / cpp/op_990 -- **core difference**
  - c/op_594 / cpp/op_126 -- **core difference**
  - c/op_594 / cpp/op_162 -- **core difference**
  - c/op_594 / cpp/op_198 -- **core difference**
  - c/op_594 / cpp/op_234 -- **core difference**
  - c/op_594 / cpp/op_486 -- **core difference**
  - c/op_594 / cpp/op_522 -- **core difference**
  - c/op_594 / cpp/op_558 -- **core difference**
  - c/op_594 / cpp/op_594 -- **core difference**
  - c/op_594 / cpp/op_630 -- **core difference**
  - c/op_594 / cpp/op_666 -- **core difference**
  - c/op_594 / cpp/op_774 -- **core difference**
  - c/op_594 / cpp/op_990 -- **core difference**
  - c/op_630 / cpp/op_126 -- **core difference**
  - c/op_630 / cpp/op_162 -- **core difference**
  - c/op_630 / cpp/op_198 -- **core difference**
  - c/op_630 / cpp/op_234 -- **core difference**
  - c/op_630 / cpp/op_486 -- **core difference**
  - c/op_630 / cpp/op_522 -- **core difference**
  - c/op_630 / cpp/op_558 -- **core difference**
  - c/op_630 / cpp/op_594 -- **core difference**
  - c/op_630 / cpp/op_630 -- **core difference**
  - c/op_630 / cpp/op_666 -- **core difference**
  - c/op_630 / cpp/op_774 -- **core difference**
  - c/op_630 / cpp/op_990 -- **core difference**
  - c/op_666 / cpp/op_126 -- **core difference**
  - c/op_666 / cpp/op_162 -- **core difference**
  - c/op_666 / cpp/op_198 -- **core difference**
  - c/op_666 / cpp/op_234 -- **core difference**
  - c/op_666 / cpp/op_486 -- **core difference**
  - c/op_666 / cpp/op_522 -- **core difference**
  - c/op_666 / cpp/op_558 -- **core difference**
  - c/op_666 / cpp/op_594 -- **core difference**
  - c/op_666 / cpp/op_630 -- **core difference**
  - c/op_666 / cpp/op_666 -- **core difference**
  - c/op_666 / cpp/op_774 -- **core difference**
  - c/op_666 / cpp/op_990 -- **core difference**

### shared-core group And8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `&&` (f64,i64, 0 modes); cpp `&&` (f64,i64, 0 modes); cpp `and` (f64,i64, 0 modes)

  - c/op_343 / cpp/op_343 -- **core difference**
  - c/op_343 / cpp/op_847 -- **core difference**

### shared-core group Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `||` (f64,i64, 0 modes); cpp `||` (f64,i64, 0 modes); cpp `or` (f64,i64, 0 modes)

  - c/op_307 / cpp/op_307 -- **core difference**
  - c/op_307 / cpp/op_811 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64)))) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `||` (f64,i64, 0 modes); c `&&` (f64,i64, 0 modes); cpp `||` (f64,i64, 0 modes); cpp `&&` (f64,i64, 0 modes); cpp `or` (f64,i64, 0 modes); cpp `and` (f64,i64, 0 modes)

  - c/op_307 / cpp/op_307 -- **core difference**
  - c/op_307 / cpp/op_343 -- **core difference**
  - c/op_307 / cpp/op_811 -- **core difference**
  - c/op_307 / cpp/op_847 -- **core difference**
  - c/op_343 / cpp/op_307 -- **core difference**
  - c/op_343 / cpp/op_343 -- **core difference**
  - c/op_343 / cpp/op_811 -- **core difference**
  - c/op_343 / cpp/op_847 -- **core difference**

### shared-core group ins@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)),XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))),ex128@0(in0:256)))) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `!=` (f64,i64, 0 modes); cpp `!=` (f64,i64, 0 modes); cpp `not_eq` (f64,i64, 0 modes)

  - c/op_523 / cpp/op_523 -- **total equality**
  - c/op_523 / cpp/op_991 -- **total equality**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)),CmpEQ64F0x2(ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))),ex128@0(in0:256)))))) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `==` (f64,i64, 0 modes); cpp `==` (f64,i64, 0 modes)

  - c/op_487 / cpp/op_487 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)))))),0:64,u2:64))) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `>` (f64,i64, 0 modes); cpp `>` (f64,i64, 0 modes)

  - c/op_559 / cpp/op_559 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)))))),0:64,u2:64))) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `>=` (f64,i64, 0 modes); cpp `>=` (f64,i64, 0 modes)

  - c/op_595 / cpp/op_595 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))),ex64@0(in0:256)))),0:64,u2:64))) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `<=` (f64,i64, 0 modes); cpp `<=` (f64,i64, 0 modes)

  - c/op_631 / cpp/op_631 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))),ex64@0(in0:256)))),0:64,u2:64))) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `<` (f64,i64, 0 modes); cpp `<` (f64,i64, 0 modes)

  - c/op_667 / cpp/op_667 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)))))) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `>` (f64,i64, 0 modes); c `>=` (f64,i64, 0 modes); cpp `>` (f64,i64, 0 modes); cpp `>=` (f64,i64, 0 modes); cpp `<=>` (f64,i64, 0 modes)

  - c/op_559 / cpp/op_559 -- **core difference**
  - c/op_559 / cpp/op_595 -- **core difference**
  - c/op_559 / cpp/op_775 -- **core difference**
  - c/op_595 / cpp/op_559 -- **core difference**
  - c/op_595 / cpp/op_595 -- **core difference**
  - c/op_595 / cpp/op_775 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))),ex64@0(in0:256)))) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `<=` (f64,i64, 0 modes); c `<` (f64,i64, 0 modes); cpp `<=` (f64,i64, 0 modes); cpp `<` (f64,i64, 0 modes); cpp `<=>` (f64,i64, 0 modes)

  - c/op_631 / cpp/op_631 -- **core difference**
  - c/op_631 / cpp/op_667 -- **core difference**
  - c/op_631 / cpp/op_775 -- **core difference**
  - c/op_667 / cpp/op_631 -- **core difference**
  - c/op_667 / cpp/op_667 -- **core difference**
  - c/op_667 / cpp/op_775 -- **core difference**

### shared-core group CmpEQ64F0x2(ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))),ex128@0(in0:256)) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `==` (f64,i64, 0 modes); c `!=` (f64,i64, 0 modes); cpp `==` (f64,i64, 0 modes); cpp `!=` (f64,i64, 0 modes); cpp `not_eq` (f64,i64, 0 modes)

  - c/op_487 / cpp/op_487 -- **total equality**
  - c/op_487 / cpp/op_523 -- **core difference**
  - c/op_487 / cpp/op_991 -- **core difference**
  - c/op_523 / cpp/op_487 -- **core difference**
  - c/op_523 / cpp/op_523 -- **total equality**
  - c/op_523 / cpp/op_991 -- **total equality**

### shared-core group Add64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)))) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `+` (f64,i64, 0 modes); cpp `+` (f64,i64, 0 modes)

  - c/op_127 / cpp/op_127 -- **total equality**

### shared-core group Sub64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)))) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `-` (f64,i64, 0 modes); cpp `-` (f64,i64, 0 modes)

  - c/op_163 / cpp/op_163 -- **total equality**

### shared-core group Mul64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)))) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `*` (f64,i64, 0 modes); cpp `*` (f64,i64, 0 modes)

  - c/op_199 / cpp/op_199 -- **total equality**

### shared-core group Div64F0x2(ex128@0(in0:256),ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)))) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `/` (f64,i64, 0 modes); cpp `/` (f64,i64, 0 modes)

  - c/op_235 / cpp/op_235 -- **total equality**

### shared-core group ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `+` (f64,i64, 0 modes); c `-` (f64,i64, 0 modes); c `*` (f64,i64, 0 modes); c `/` (f64,i64, 0 modes); c `==` (f64,i64, 0 modes); c `!=` (f64,i64, 0 modes); cpp `+` (f64,i64, 0 modes); cpp `-` (f64,i64, 0 modes); cpp `*` (f64,i64, 0 modes); cpp `/` (f64,i64, 0 modes); cpp `==` (f64,i64, 0 modes); cpp `!=` (f64,i64, 0 modes); cpp `not_eq` (f64,i64, 0 modes)

  - c/op_127 / cpp/op_127 -- **total equality**
  - c/op_127 / cpp/op_163 -- **core difference**
  - c/op_127 / cpp/op_199 -- **core difference**
  - c/op_127 / cpp/op_235 -- **core difference**
  - c/op_127 / cpp/op_487 -- **core difference**
  - c/op_127 / cpp/op_523 -- **core difference**
  - c/op_127 / cpp/op_991 -- **core difference**
  - c/op_163 / cpp/op_127 -- **core difference**
  - c/op_163 / cpp/op_163 -- **total equality**
  - c/op_163 / cpp/op_199 -- **core difference**
  - c/op_163 / cpp/op_235 -- **core difference**
  - c/op_163 / cpp/op_487 -- **core difference**
  - c/op_163 / cpp/op_523 -- **core difference**
  - c/op_163 / cpp/op_991 -- **core difference**
  - c/op_199 / cpp/op_127 -- **core difference**
  - c/op_199 / cpp/op_163 -- **core difference**
  - c/op_199 / cpp/op_199 -- **total equality**
  - c/op_199 / cpp/op_235 -- **core difference**
  - c/op_199 / cpp/op_487 -- **core difference**
  - c/op_199 / cpp/op_523 -- **core difference**
  - c/op_199 / cpp/op_991 -- **core difference**
  - c/op_235 / cpp/op_127 -- **core difference**
  - c/op_235 / cpp/op_163 -- **core difference**
  - c/op_235 / cpp/op_199 -- **core difference**
  - c/op_235 / cpp/op_235 -- **total equality**
  - c/op_235 / cpp/op_487 -- **core difference**
  - c/op_235 / cpp/op_523 -- **core difference**
  - c/op_235 / cpp/op_991 -- **core difference**
  - c/op_487 / cpp/op_127 -- **core difference**
  - c/op_487 / cpp/op_163 -- **core difference**
  - c/op_487 / cpp/op_199 -- **core difference**
  - c/op_487 / cpp/op_235 -- **core difference**
  - c/op_487 / cpp/op_487 -- **total equality**
  - c/op_487 / cpp/op_523 -- **core difference**
  - c/op_487 / cpp/op_991 -- **core difference**
  - c/op_523 / cpp/op_127 -- **core difference**
  - c/op_523 / cpp/op_163 -- **core difference**
  - c/op_523 / cpp/op_199 -- **core difference**
  - c/op_523 / cpp/op_235 -- **core difference**
  - c/op_523 / cpp/op_487 -- **core difference**
  - c/op_523 / cpp/op_523 -- **total equality**
  - c/op_523 / cpp/op_991 -- **total equality**

### shared-core group ex64@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64))) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `>` (f64,i64, 0 modes); c `>=` (f64,i64, 0 modes); c `<=` (f64,i64, 0 modes); c `<` (f64,i64, 0 modes); cpp `>` (f64,i64, 0 modes); cpp `>=` (f64,i64, 0 modes); cpp `<=` (f64,i64, 0 modes); cpp `<` (f64,i64, 0 modes); cpp `<=>` (f64,i64, 0 modes)

  - c/op_559 / cpp/op_559 -- **core difference**
  - c/op_559 / cpp/op_595 -- **core difference**
  - c/op_559 / cpp/op_631 -- **core difference**
  - c/op_559 / cpp/op_667 -- **core difference**
  - c/op_559 / cpp/op_775 -- **core difference**
  - c/op_595 / cpp/op_559 -- **core difference**
  - c/op_595 / cpp/op_595 -- **core difference**
  - c/op_595 / cpp/op_631 -- **core difference**
  - c/op_595 / cpp/op_667 -- **core difference**
  - c/op_595 / cpp/op_775 -- **core difference**
  - c/op_631 / cpp/op_559 -- **core difference**
  - c/op_631 / cpp/op_595 -- **core difference**
  - c/op_631 / cpp/op_631 -- **core difference**
  - c/op_631 / cpp/op_667 -- **core difference**
  - c/op_631 / cpp/op_775 -- **core difference**
  - c/op_667 / cpp/op_559 -- **core difference**
  - c/op_667 / cpp/op_595 -- **core difference**
  - c/op_667 / cpp/op_631 -- **core difference**
  - c/op_667 / cpp/op_667 -- **core difference**
  - c/op_667 / cpp/op_775 -- **core difference**

### shared-core group ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in1:64)) · (f64,i64)

- ground: connection
- languages: c, cpp
- members: c `+` (f64,i64, 0 modes); c `-` (f64,i64, 0 modes); c `*` (f64,i64, 0 modes); c `/` (f64,i64, 0 modes); c `==` (f64,i64, 0 modes); c `!=` (f64,i64, 0 modes); c `>` (f64,i64, 0 modes); c `>=` (f64,i64, 0 modes); c `<=` (f64,i64, 0 modes); c `<` (f64,i64, 0 modes); cpp `+` (f64,i64, 0 modes); cpp `-` (f64,i64, 0 modes); cpp `*` (f64,i64, 0 modes); cpp `/` (f64,i64, 0 modes); cpp `==` (f64,i64, 0 modes); cpp `!=` (f64,i64, 0 modes); cpp `>` (f64,i64, 0 modes); cpp `>=` (f64,i64, 0 modes); cpp `<=` (f64,i64, 0 modes); cpp `<` (f64,i64, 0 modes); cpp `<=>` (f64,i64, 0 modes); cpp `not_eq` (f64,i64, 0 modes)

  - c/op_127 / cpp/op_127 -- **total equality**
  - c/op_127 / cpp/op_163 -- **core difference**
  - c/op_127 / cpp/op_199 -- **core difference**
  - c/op_127 / cpp/op_235 -- **core difference**
  - c/op_127 / cpp/op_487 -- **core difference**
  - c/op_127 / cpp/op_523 -- **core difference**
  - c/op_127 / cpp/op_559 -- **core difference**
  - c/op_127 / cpp/op_595 -- **core difference**
  - c/op_127 / cpp/op_631 -- **core difference**
  - c/op_127 / cpp/op_667 -- **core difference**
  - c/op_127 / cpp/op_775 -- **core difference**
  - c/op_127 / cpp/op_991 -- **core difference**
  - c/op_163 / cpp/op_127 -- **core difference**
  - c/op_163 / cpp/op_163 -- **total equality**
  - c/op_163 / cpp/op_199 -- **core difference**
  - c/op_163 / cpp/op_235 -- **core difference**
  - c/op_163 / cpp/op_487 -- **core difference**
  - c/op_163 / cpp/op_523 -- **core difference**
  - c/op_163 / cpp/op_559 -- **core difference**
  - c/op_163 / cpp/op_595 -- **core difference**
  - c/op_163 / cpp/op_631 -- **core difference**
  - c/op_163 / cpp/op_667 -- **core difference**
  - c/op_163 / cpp/op_775 -- **core difference**
  - c/op_163 / cpp/op_991 -- **core difference**
  - c/op_199 / cpp/op_127 -- **core difference**
  - c/op_199 / cpp/op_163 -- **core difference**
  - c/op_199 / cpp/op_199 -- **total equality**
  - c/op_199 / cpp/op_235 -- **core difference**
  - c/op_199 / cpp/op_487 -- **core difference**
  - c/op_199 / cpp/op_523 -- **core difference**
  - c/op_199 / cpp/op_559 -- **core difference**
  - c/op_199 / cpp/op_595 -- **core difference**
  - c/op_199 / cpp/op_631 -- **core difference**
  - c/op_199 / cpp/op_667 -- **core difference**
  - c/op_199 / cpp/op_775 -- **core difference**
  - c/op_199 / cpp/op_991 -- **core difference**
  - c/op_235 / cpp/op_127 -- **core difference**
  - c/op_235 / cpp/op_163 -- **core difference**
  - c/op_235 / cpp/op_199 -- **core difference**
  - c/op_235 / cpp/op_235 -- **total equality**
  - c/op_235 / cpp/op_487 -- **core difference**
  - c/op_235 / cpp/op_523 -- **core difference**
  - c/op_235 / cpp/op_559 -- **core difference**
  - c/op_235 / cpp/op_595 -- **core difference**
  - c/op_235 / cpp/op_631 -- **core difference**
  - c/op_235 / cpp/op_667 -- **core difference**
  - c/op_235 / cpp/op_775 -- **core difference**
  - c/op_235 / cpp/op_991 -- **core difference**
  - c/op_487 / cpp/op_127 -- **core difference**
  - c/op_487 / cpp/op_163 -- **core difference**
  - c/op_487 / cpp/op_199 -- **core difference**
  - c/op_487 / cpp/op_235 -- **core difference**
  - c/op_487 / cpp/op_487 -- **total equality**
  - c/op_487 / cpp/op_523 -- **core difference**
  - c/op_487 / cpp/op_559 -- **core difference**
  - c/op_487 / cpp/op_595 -- **core difference**
  - c/op_487 / cpp/op_631 -- **core difference**
  - c/op_487 / cpp/op_667 -- **core difference**
  - c/op_487 / cpp/op_775 -- **core difference**
  - c/op_487 / cpp/op_991 -- **core difference**
  - c/op_523 / cpp/op_127 -- **core difference**
  - c/op_523 / cpp/op_163 -- **core difference**
  - c/op_523 / cpp/op_199 -- **core difference**
  - c/op_523 / cpp/op_235 -- **core difference**
  - c/op_523 / cpp/op_487 -- **core difference**
  - c/op_523 / cpp/op_523 -- **total equality**
  - c/op_523 / cpp/op_559 -- **core difference**
  - c/op_523 / cpp/op_595 -- **core difference**
  - c/op_523 / cpp/op_631 -- **core difference**
  - c/op_523 / cpp/op_667 -- **core difference**
  - c/op_523 / cpp/op_775 -- **core difference**
  - c/op_523 / cpp/op_991 -- **total equality**
  - c/op_559 / cpp/op_127 -- **core difference**
  - c/op_559 / cpp/op_163 -- **core difference**
  - c/op_559 / cpp/op_199 -- **core difference**
  - c/op_559 / cpp/op_235 -- **core difference**
  - c/op_559 / cpp/op_487 -- **core difference**
  - c/op_559 / cpp/op_523 -- **core difference**
  - c/op_559 / cpp/op_559 -- **core difference**
  - c/op_559 / cpp/op_595 -- **core difference**
  - c/op_559 / cpp/op_631 -- **core difference**
  - c/op_559 / cpp/op_667 -- **core difference**
  - c/op_559 / cpp/op_775 -- **core difference**
  - c/op_559 / cpp/op_991 -- **core difference**
  - c/op_595 / cpp/op_127 -- **core difference**
  - c/op_595 / cpp/op_163 -- **core difference**
  - c/op_595 / cpp/op_199 -- **core difference**
  - c/op_595 / cpp/op_235 -- **core difference**
  - c/op_595 / cpp/op_487 -- **core difference**
  - c/op_595 / cpp/op_523 -- **core difference**
  - c/op_595 / cpp/op_559 -- **core difference**
  - c/op_595 / cpp/op_595 -- **core difference**
  - c/op_595 / cpp/op_631 -- **core difference**
  - c/op_595 / cpp/op_667 -- **core difference**
  - c/op_595 / cpp/op_775 -- **core difference**
  - c/op_595 / cpp/op_991 -- **core difference**
  - c/op_631 / cpp/op_127 -- **core difference**
  - c/op_631 / cpp/op_163 -- **core difference**
  - c/op_631 / cpp/op_199 -- **core difference**
  - c/op_631 / cpp/op_235 -- **core difference**
  - c/op_631 / cpp/op_487 -- **core difference**
  - c/op_631 / cpp/op_523 -- **core difference**
  - c/op_631 / cpp/op_559 -- **core difference**
  - c/op_631 / cpp/op_595 -- **core difference**
  - c/op_631 / cpp/op_631 -- **core difference**
  - c/op_631 / cpp/op_667 -- **core difference**
  - c/op_631 / cpp/op_775 -- **core difference**
  - c/op_631 / cpp/op_991 -- **core difference**
  - c/op_667 / cpp/op_127 -- **core difference**
  - c/op_667 / cpp/op_163 -- **core difference**
  - c/op_667 / cpp/op_199 -- **core difference**
  - c/op_667 / cpp/op_235 -- **core difference**
  - c/op_667 / cpp/op_487 -- **core difference**
  - c/op_667 / cpp/op_523 -- **core difference**
  - c/op_667 / cpp/op_559 -- **core difference**
  - c/op_667 / cpp/op_595 -- **core difference**
  - c/op_667 / cpp/op_631 -- **core difference**
  - c/op_667 / cpp/op_667 -- **core difference**
  - c/op_667 / cpp/op_775 -- **core difference**
  - c/op_667 / cpp/op_991 -- **core difference**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),CmpEQ64F0x2(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex128@0(in0:256)))))) · (f64,u64)

- ground: connection
- languages: c, cpp
- members: c `==` (f64,u64, 0 modes); cpp `==` (f64,u64, 0 modes)

  - c/op_488 / cpp/op_488 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))))))),0:64,u0:64))) · (f64,u64)

- ground: connection
- languages: c, cpp
- members: c `>` (f64,u64, 0 modes); cpp `>` (f64,u64, 0 modes)

  - c/op_560 / cpp/op_560 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))))))),0:64,u0:64))) · (f64,u64)

- ground: connection
- languages: c, cpp
- members: c `>=` (f64,u64, 0 modes); cpp `>=` (f64,u64, 0 modes)

  - c/op_596 / cpp/op_596 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),ex64@0(in0:256)))),0:64,u0:64))) · (f64,u64)

- ground: connection
- languages: c, cpp
- members: c `<=` (f64,u64, 0 modes); cpp `<=` (f64,u64, 0 modes)

  - c/op_632 / cpp/op_632 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),ex64@0(in0:256)))),0:64,u0:64))) · (f64,u64)

- ground: connection
- languages: c, cpp
- members: c `<` (f64,u64, 0 modes); cpp `<` (f64,u64, 0 modes)

  - c/op_668 / cpp/op_668 -- **core difference**

### shared-core group zx64(And32(1:32,ex32@0(XorV128(18446744073709551615:128,CmpEQ64F0x2(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex128@0(in0:256)))))) · (f64,u64)

- ground: connection
- languages: c, cpp
- members: c `!=` (f64,u64, 0 modes); cpp `!=` (f64,u64, 0 modes); cpp `not_eq` (f64,u64, 0 modes)

  - c/op_524 / cpp/op_524 -- **total equality**
  - c/op_524 / cpp/op_992 -- **total equality**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(in0:256),ex64@0(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))))))) · (f64,u64)

- ground: connection
- languages: c, cpp
- members: c `>` (f64,u64, 0 modes); c `>=` (f64,u64, 0 modes); cpp `>` (f64,u64, 0 modes); cpp `>=` (f64,u64, 0 modes); cpp `<=>` (f64,u64, 0 modes)

  - c/op_560 / cpp/op_560 -- **core difference**
  - c/op_560 / cpp/op_596 -- **core difference**
  - c/op_560 / cpp/op_776 -- **core difference**
  - c/op_596 / cpp/op_560 -- **core difference**
  - c/op_596 / cpp/op_596 -- **core difference**
  - c/op_596 / cpp/op_776 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),ex64@0(in0:256)))) · (f64,u64)

- ground: connection
- languages: c, cpp
- members: c `<=` (f64,u64, 0 modes); c `<` (f64,u64, 0 modes); cpp `<=` (f64,u64, 0 modes); cpp `<` (f64,u64, 0 modes); cpp `<=>` (f64,u64, 0 modes)

  - c/op_632 / cpp/op_632 -- **core difference**
  - c/op_632 / cpp/op_668 -- **core difference**
  - c/op_632 / cpp/op_776 -- **core difference**
  - c/op_668 / cpp/op_632 -- **core difference**
  - c/op_668 / cpp/op_668 -- **core difference**
  - c/op_668 / cpp/op_776 -- **core difference**

### shared-core group CmpEQ64F0x2(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex128@0(in0:256)) · (f64,u64)

- ground: connection
- languages: c, cpp
- members: c `==` (f64,u64, 0 modes); c `!=` (f64,u64, 0 modes); cpp `==` (f64,u64, 0 modes); cpp `!=` (f64,u64, 0 modes); cpp `not_eq` (f64,u64, 0 modes)

  - c/op_488 / cpp/op_488 -- **total equality**
  - c/op_488 / cpp/op_524 -- **core difference**
  - c/op_488 / cpp/op_992 -- **core difference**
  - c/op_524 / cpp/op_488 -- **core difference**
  - c/op_524 / cpp/op_524 -- **total equality**
  - c/op_524 / cpp/op_992 -- **total equality**

### shared-core group Add64F0x2(ex128@0(in0:256),Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))) · (f64,u64)

- ground: connection
- languages: c, cpp
- members: c `+` (f64,u64, 0 modes); cpp `+` (f64,u64, 0 modes)

  - c/op_128 / cpp/op_128 -- **total equality**

### shared-core group Sub64F0x2(ex128@0(in0:256),Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))) · (f64,u64)

- ground: connection
- languages: c, cpp
- members: c `-` (f64,u64, 0 modes); cpp `-` (f64,u64, 0 modes)

  - c/op_164 / cpp/op_164 -- **total equality**

### shared-core group Mul64F0x2(ex128@0(in0:256),Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))) · (f64,u64)

- ground: connection
- languages: c, cpp
- members: c `*` (f64,u64, 0 modes); cpp `*` (f64,u64, 0 modes)

  - c/op_200 / cpp/op_200 -- **total equality**

### shared-core group Div64F0x2(ex128@0(in0:256),Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))) · (f64,u64)

- ground: connection
- languages: c, cpp
- members: c `/` (f64,u64, 0 modes); cpp `/` (f64,u64, 0 modes)

  - c/op_236 / cpp/op_236 -- **total equality**

### shared-core group And8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (f64,u64)

- ground: connection
- languages: c, cpp
- members: c `&&` (f64,u64, 0 modes); cpp `&&` (f64,u64, 0 modes); cpp `and` (f64,u64, 0 modes)

  - c/op_344 / cpp/op_344 -- **core difference**
  - c/op_344 / cpp/op_848 -- **core difference**

### shared-core group Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (f64,u64)

- ground: connection
- languages: c, cpp
- members: c `||` (f64,u64, 0 modes); cpp `||` (f64,u64, 0 modes); cpp `or` (f64,u64, 0 modes)

  - c/op_308 / cpp/op_308 -- **core difference**
  - c/op_308 / cpp/op_812 -- **core difference**

### shared-core group ex64@0(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))) · (f64,u64)

- ground: connection
- languages: c, cpp
- members: c `>` (f64,u64, 0 modes); c `>=` (f64,u64, 0 modes); c `<=` (f64,u64, 0 modes); c `<` (f64,u64, 0 modes); cpp `>` (f64,u64, 0 modes); cpp `>=` (f64,u64, 0 modes); cpp `<=` (f64,u64, 0 modes); cpp `<` (f64,u64, 0 modes); cpp `<=>` (f64,u64, 0 modes)

  - c/op_560 / cpp/op_560 -- **core difference**
  - c/op_560 / cpp/op_596 -- **core difference**
  - c/op_560 / cpp/op_632 -- **core difference**
  - c/op_560 / cpp/op_668 -- **core difference**
  - c/op_560 / cpp/op_776 -- **core difference**
  - c/op_596 / cpp/op_560 -- **core difference**
  - c/op_596 / cpp/op_596 -- **core difference**
  - c/op_596 / cpp/op_632 -- **core difference**
  - c/op_596 / cpp/op_668 -- **core difference**
  - c/op_596 / cpp/op_776 -- **core difference**
  - c/op_632 / cpp/op_560 -- **core difference**
  - c/op_632 / cpp/op_596 -- **core difference**
  - c/op_632 / cpp/op_632 -- **core difference**
  - c/op_632 / cpp/op_668 -- **core difference**
  - c/op_632 / cpp/op_776 -- **core difference**
  - c/op_668 / cpp/op_560 -- **core difference**
  - c/op_668 / cpp/op_596 -- **core difference**
  - c/op_668 / cpp/op_632 -- **core difference**
  - c/op_668 / cpp/op_668 -- **core difference**
  - c/op_668 / cpp/op_776 -- **core difference**

### shared-core group Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in1:64)),ld128/g0(21:64))) · (f64,u64)

- ground: connection
- languages: c, cpp
- members: c `+` (f64,u64, 0 modes); c `-` (f64,u64, 0 modes); c `*` (f64,u64, 0 modes); c `/` (f64,u64, 0 modes); c `==` (f64,u64, 0 modes); c `!=` (f64,u64, 0 modes); c `>` (f64,u64, 0 modes); c `>=` (f64,u64, 0 modes); c `<=` (f64,u64, 0 modes); c `<` (f64,u64, 0 modes); cpp `+` (f64,u64, 0 modes); cpp `-` (f64,u64, 0 modes); cpp `*` (f64,u64, 0 modes); cpp `/` (f64,u64, 0 modes); cpp `==` (f64,u64, 0 modes); cpp `!=` (f64,u64, 0 modes); cpp `>` (f64,u64, 0 modes); cpp `>=` (f64,u64, 0 modes); cpp `<=` (f64,u64, 0 modes); cpp `<` (f64,u64, 0 modes); cpp `<=>` (f64,u64, 0 modes); cpp `not_eq` (f64,u64, 0 modes)

  - c/op_128 / cpp/op_128 -- **total equality**
  - c/op_128 / cpp/op_164 -- **core difference**
  - c/op_128 / cpp/op_200 -- **core difference**
  - c/op_128 / cpp/op_236 -- **core difference**
  - c/op_128 / cpp/op_488 -- **core difference**
  - c/op_128 / cpp/op_524 -- **core difference**
  - c/op_128 / cpp/op_560 -- **core difference**
  - c/op_128 / cpp/op_596 -- **core difference**
  - c/op_128 / cpp/op_632 -- **core difference**
  - c/op_128 / cpp/op_668 -- **core difference**
  - c/op_128 / cpp/op_776 -- **core difference**
  - c/op_128 / cpp/op_992 -- **core difference**
  - c/op_164 / cpp/op_128 -- **core difference**
  - c/op_164 / cpp/op_164 -- **total equality**
  - c/op_164 / cpp/op_200 -- **core difference**
  - c/op_164 / cpp/op_236 -- **core difference**
  - c/op_164 / cpp/op_488 -- **core difference**
  - c/op_164 / cpp/op_524 -- **core difference**
  - c/op_164 / cpp/op_560 -- **core difference**
  - c/op_164 / cpp/op_596 -- **core difference**
  - c/op_164 / cpp/op_632 -- **core difference**
  - c/op_164 / cpp/op_668 -- **core difference**
  - c/op_164 / cpp/op_776 -- **core difference**
  - c/op_164 / cpp/op_992 -- **core difference**
  - c/op_200 / cpp/op_128 -- **core difference**
  - c/op_200 / cpp/op_164 -- **core difference**
  - c/op_200 / cpp/op_200 -- **total equality**
  - c/op_200 / cpp/op_236 -- **core difference**
  - c/op_200 / cpp/op_488 -- **core difference**
  - c/op_200 / cpp/op_524 -- **core difference**
  - c/op_200 / cpp/op_560 -- **core difference**
  - c/op_200 / cpp/op_596 -- **core difference**
  - c/op_200 / cpp/op_632 -- **core difference**
  - c/op_200 / cpp/op_668 -- **core difference**
  - c/op_200 / cpp/op_776 -- **core difference**
  - c/op_200 / cpp/op_992 -- **core difference**
  - c/op_236 / cpp/op_128 -- **core difference**
  - c/op_236 / cpp/op_164 -- **core difference**
  - c/op_236 / cpp/op_200 -- **core difference**
  - c/op_236 / cpp/op_236 -- **total equality**
  - c/op_236 / cpp/op_488 -- **core difference**
  - c/op_236 / cpp/op_524 -- **core difference**
  - c/op_236 / cpp/op_560 -- **core difference**
  - c/op_236 / cpp/op_596 -- **core difference**
  - c/op_236 / cpp/op_632 -- **core difference**
  - c/op_236 / cpp/op_668 -- **core difference**
  - c/op_236 / cpp/op_776 -- **core difference**
  - c/op_236 / cpp/op_992 -- **core difference**
  - c/op_488 / cpp/op_128 -- **core difference**
  - c/op_488 / cpp/op_164 -- **core difference**
  - c/op_488 / cpp/op_200 -- **core difference**
  - c/op_488 / cpp/op_236 -- **core difference**
  - c/op_488 / cpp/op_488 -- **total equality**
  - c/op_488 / cpp/op_524 -- **core difference**
  - c/op_488 / cpp/op_560 -- **core difference**
  - c/op_488 / cpp/op_596 -- **core difference**
  - c/op_488 / cpp/op_632 -- **core difference**
  - c/op_488 / cpp/op_668 -- **core difference**
  - c/op_488 / cpp/op_776 -- **core difference**
  - c/op_488 / cpp/op_992 -- **core difference**
  - c/op_524 / cpp/op_128 -- **core difference**
  - c/op_524 / cpp/op_164 -- **core difference**
  - c/op_524 / cpp/op_200 -- **core difference**
  - c/op_524 / cpp/op_236 -- **core difference**
  - c/op_524 / cpp/op_488 -- **core difference**
  - c/op_524 / cpp/op_524 -- **total equality**
  - c/op_524 / cpp/op_560 -- **core difference**
  - c/op_524 / cpp/op_596 -- **core difference**
  - c/op_524 / cpp/op_632 -- **core difference**
  - c/op_524 / cpp/op_668 -- **core difference**
  - c/op_524 / cpp/op_776 -- **core difference**
  - c/op_524 / cpp/op_992 -- **total equality**
  - c/op_560 / cpp/op_128 -- **core difference**
  - c/op_560 / cpp/op_164 -- **core difference**
  - c/op_560 / cpp/op_200 -- **core difference**
  - c/op_560 / cpp/op_236 -- **core difference**
  - c/op_560 / cpp/op_488 -- **core difference**
  - c/op_560 / cpp/op_524 -- **core difference**
  - c/op_560 / cpp/op_560 -- **core difference**
  - c/op_560 / cpp/op_596 -- **core difference**
  - c/op_560 / cpp/op_632 -- **core difference**
  - c/op_560 / cpp/op_668 -- **core difference**
  - c/op_560 / cpp/op_776 -- **core difference**
  - c/op_560 / cpp/op_992 -- **core difference**
  - c/op_596 / cpp/op_128 -- **core difference**
  - c/op_596 / cpp/op_164 -- **core difference**
  - c/op_596 / cpp/op_200 -- **core difference**
  - c/op_596 / cpp/op_236 -- **core difference**
  - c/op_596 / cpp/op_488 -- **core difference**
  - c/op_596 / cpp/op_524 -- **core difference**
  - c/op_596 / cpp/op_560 -- **core difference**
  - c/op_596 / cpp/op_596 -- **core difference**
  - c/op_596 / cpp/op_632 -- **core difference**
  - c/op_596 / cpp/op_668 -- **core difference**
  - c/op_596 / cpp/op_776 -- **core difference**
  - c/op_596 / cpp/op_992 -- **core difference**
  - c/op_632 / cpp/op_128 -- **core difference**
  - c/op_632 / cpp/op_164 -- **core difference**
  - c/op_632 / cpp/op_200 -- **core difference**
  - c/op_632 / cpp/op_236 -- **core difference**
  - c/op_632 / cpp/op_488 -- **core difference**
  - c/op_632 / cpp/op_524 -- **core difference**
  - c/op_632 / cpp/op_560 -- **core difference**
  - c/op_632 / cpp/op_596 -- **core difference**
  - c/op_632 / cpp/op_632 -- **core difference**
  - c/op_632 / cpp/op_668 -- **core difference**
  - c/op_632 / cpp/op_776 -- **core difference**
  - c/op_632 / cpp/op_992 -- **core difference**
  - c/op_668 / cpp/op_128 -- **core difference**
  - c/op_668 / cpp/op_164 -- **core difference**
  - c/op_668 / cpp/op_200 -- **core difference**
  - c/op_668 / cpp/op_236 -- **core difference**
  - c/op_668 / cpp/op_488 -- **core difference**
  - c/op_668 / cpp/op_524 -- **core difference**
  - c/op_668 / cpp/op_560 -- **core difference**
  - c/op_668 / cpp/op_596 -- **core difference**
  - c/op_668 / cpp/op_632 -- **core difference**
  - c/op_668 / cpp/op_668 -- **core difference**
  - c/op_668 / cpp/op_776 -- **core difference**
  - c/op_668 / cpp/op_992 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in0:256),0:64))),0:64,u0:64)))) · (f64,u64)

- ground: connection
- languages: c, cpp
- members: c `||` (f64,u64, 0 modes); c `&&` (f64,u64, 0 modes); cpp `||` (f64,u64, 0 modes); cpp `&&` (f64,u64, 0 modes); cpp `or` (f64,u64, 0 modes); cpp `and` (f64,u64, 0 modes)

  - c/op_308 / cpp/op_308 -- **core difference**
  - c/op_308 / cpp/op_344 -- **core difference**
  - c/op_308 / cpp/op_812 -- **core difference**
  - c/op_308 / cpp/op_848 -- **core difference**
  - c/op_344 / cpp/op_308 -- **core difference**
  - c/op_344 / cpp/op_344 -- **core difference**
  - c/op_344 / cpp/op_812 -- **core difference**
  - c/op_344 / cpp/op_848 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(4:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64))) · (i32,None)

- ground: connection
- languages: c, cpp
- members: c `!` (i32,None, 0 modes); cpp `!` (i32,None, 0 modes); cpp `not` (i32,None, 0 modes)

  - c/op_0 / cpp/op_0 -- **core difference**
  - c/op_0 / cpp/op_24 -- **core difference**

### shared-core group st32(Add64(18446744073709551612:64,SP:64))=ex32@0(in0:64) · (i32,None)

- ground: connection
- languages: c, cpp
- members: c `&` (i32,None, 0 modes); cpp `&` (i32,None, 0 modes)

  - c/op_30 / cpp/op_42 -- **total equality**

### shared-core group zx64(Add32(4294967295:32,ex32@0(in0:64))) · (i32,None)

- ground: connection
- languages: c, cpp
- members: c `--` (i32,None, 0 modes); cpp `--` (i32,None, 0 modes)

  - c/op_42 / cpp/op_54 -- **total equality**

### shared-core group zx64(Sub32(0:32,ex32@0(in0:64))) · (i32,None)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `-` (i32,None, 1 modes); cpp `-` (i32,None, 1 modes); go `-` (i32,None, 1 modes); rust `-` (i32,None, 1 modes); swift `-` (i32,None, 1 modes)

  - c/op_12 / cpp/op_12 -- **total equality**
  - c/op_12 / go/op_6 -- **total equality**
  - c/op_12 / rust/op_0 -- **total equality**
  - c/op_12 / swift/op_12 -- **core equality, modes differ**
    - only on the left: `0 - in0 overflows 32 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `0 - in0 overflows 32 bits (signed)` -> `trap` (branch-to-response)
  - cpp/op_12 / go/op_6 -- **total equality**
  - cpp/op_12 / rust/op_0 -- **total equality**
  - cpp/op_12 / swift/op_12 -- **core equality, modes differ**
    - only on the left: `0 - in0 overflows 32 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `0 - in0 overflows 32 bits (signed)` -> `trap` (branch-to-response)
  - go/op_6 / rust/op_0 -- **total equality**
  - go/op_6 / swift/op_12 -- **core equality, modes differ**
    - only on the left: `0 - in0 overflows 32 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `0 - in0 overflows 32 bits (signed)` -> `trap` (branch-to-response)
  - rust/op_0 / swift/op_12 -- **core equality, modes differ**
    - only on the left: `0 - in0 overflows 32 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `0 - in0 overflows 32 bits (signed)` -> `trap` (branch-to-response)

### shared-core group zx64(Add32(1:32,ex32@0(in0:64))) · (i32,None)

- ground: connection
- languages: c, cpp
- members: c `++` (i32,None, 0 modes); cpp `++` (i32,None, 0 modes)

  - c/op_36 / cpp/op_48 -- **total equality**

### shared-core group zx64(Not32(ex32@0(in0:64))) · (i32,None)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `~` (i32,None, 0 modes); cpp `compl` (i32,None, 0 modes); cpp `~` (i32,None, 0 modes); go `^` (i32,None, 0 modes); rust `!` (i32,None, 0 modes); swift `~` (i32,None, 0 modes)

  - c/op_6 / cpp/op_30 -- **total equality**
  - c/op_6 / cpp/op_6 -- **total equality**
  - c/op_6 / go/op_18 -- **total equality**
  - c/op_6 / rust/op_12 -- **total equality**
  - c/op_6 / swift/op_36 -- **total equality**
  - cpp/op_30 / go/op_18 -- **total equality**
  - cpp/op_6 / go/op_18 -- **total equality**
  - cpp/op_30 / rust/op_12 -- **total equality**
  - cpp/op_6 / rust/op_12 -- **total equality**
  - cpp/op_30 / swift/op_36 -- **total equality**
  - cpp/op_6 / swift/op_36 -- **total equality**
  - go/op_18 / rust/op_12 -- **total equality**
  - go/op_18 / swift/op_36 -- **total equality**
  - rust/op_12 / swift/op_36 -- **total equality**

### shared-core group zx64(ite(ex1@0(amd64g_calculate_condition(4:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64)),ex32@0(in1:64),ex32@0(in0:64))) · (i32,bool)

- ground: connection
- languages: c, cpp
- members: c `*` (i32,bool, 0 modes); cpp `*` (i32,bool, 0 modes)

  - c/op_179 / cpp/op_179 -- **total equality**

### shared-core group And8(ex8@0(in1:64),zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64)))) · (i32,bool)

- ground: connection
- languages: c, cpp
- members: c `&&` (i32,bool, 0 modes); cpp `&&` (i32,bool, 0 modes); cpp `and` (i32,bool, 0 modes)

  - c/op_323 / cpp/op_323 -- **core difference**
  - c/op_323 / cpp/op_827 -- **core difference**

### shared-core group Or8(ex8@0(in1:64),zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64)))) · (i32,bool)

- ground: connection
- languages: c, cpp
- members: c `||` (i32,bool, 0 modes); cpp `||` (i32,bool, 0 modes); cpp `or` (i32,bool, 0 modes)

  - c/op_287 / cpp/op_287 -- **core difference**
  - c/op_287 / cpp/op_791 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(15:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64))) · (i32,bool)

- ground: connection
- languages: c, cpp
- members: c `>` (i32,bool, 0 modes); cpp `>` (i32,bool, 0 modes)

  - c/op_539 / cpp/op_539 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(13:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64))) · (i32,bool)

- ground: connection
- languages: c, cpp
- members: c `>=` (i32,bool, 0 modes); cpp `>=` (i32,bool, 0 modes)

  - c/op_575 / cpp/op_575 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(14:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64))) · (i32,bool)

- ground: connection
- languages: c, cpp
- members: c `<=` (i32,bool, 0 modes); cpp `<=` (i32,bool, 0 modes)

  - c/op_611 / cpp/op_611 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(12:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64))) · (i32,bool)

- ground: connection
- languages: c, cpp
- members: c `<` (i32,bool, 0 modes); cpp `<` (i32,bool, 0 modes)

  - c/op_647 / cpp/op_647 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(4:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64))) · (i32,bool)

- ground: connection
- languages: c, cpp
- members: c `==` (i32,bool, 0 modes); cpp `==` (i32,bool, 0 modes)

  - c/op_467 / cpp/op_467 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64))) · (i32,bool)

- ground: connection
- languages: c, cpp
- members: c `!=` (i32,bool, 0 modes); cpp `!=` (i32,bool, 0 modes); cpp `not_eq` (i32,bool, 0 modes)

  - c/op_503 / cpp/op_503 -- **core difference**
  - c/op_503 / cpp/op_971 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64))) · (i32,bool)

- ground: connection
- languages: c, cpp
- members: c `||` (i32,bool, 0 modes); c `&&` (i32,bool, 0 modes); cpp `||` (i32,bool, 0 modes); cpp `&&` (i32,bool, 0 modes); cpp `or` (i32,bool, 0 modes); cpp `and` (i32,bool, 0 modes)

  - c/op_287 / cpp/op_287 -- **core difference**
  - c/op_287 / cpp/op_323 -- **core difference**
  - c/op_287 / cpp/op_791 -- **core difference**
  - c/op_287 / cpp/op_827 -- **core difference**
  - c/op_323 / cpp/op_287 -- **core difference**
  - c/op_323 / cpp/op_323 -- **core difference**
  - c/op_323 / cpp/op_791 -- **core difference**
  - c/op_323 / cpp/op_827 -- **core difference**

### shared-core group zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) · (i32,bool)

- ground: connection
- languages: c, cpp
- members: c `<<` (i32,bool, 0 modes); cpp `<<` (i32,bool, 0 modes)

  - c/op_683 / cpp/op_683 -- **total equality**

### shared-core group zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) · (i32,bool)

- ground: connection
- languages: c, cpp
- members: c `>>` (i32,bool, 0 modes); cpp `>>` (i32,bool, 0 modes)

  - c/op_719 / cpp/op_719 -- **total equality**

### shared-core group zx64(Add32(ex32@0(in0:64),ex32@0(in1:64))) · (i32,bool)

- ground: connection
- languages: c, cpp
- members: c `+` (i32,bool, 0 modes); cpp `+` (i32,bool, 0 modes)

  - c/op_107 / cpp/op_107 -- **total equality**

### shared-core group zx64(Sub32(ex32@0(in0:64),ex32@0(in1:64))) · (i32,bool)

- ground: connection
- languages: c, cpp
- members: c `-` (i32,bool, 0 modes); cpp `-` (i32,bool, 0 modes)

  - c/op_143 / cpp/op_143 -- **total equality**

### shared-core group zx64(Xor32(ex32@0(in0:64),ex32@0(in1:64))) · (i32,bool)

- ground: connection
- languages: c, cpp
- members: c `^` (i32,bool, 0 modes); cpp `^` (i32,bool, 0 modes); cpp `xor` (i32,bool, 0 modes)

  - c/op_395 / cpp/op_395 -- **total equality**
  - c/op_395 / cpp/op_899 -- **total equality**

### shared-core group zx64(And32(ex32@0(in0:64),ex32@0(in1:64))) · (i32,bool)

- ground: connection
- languages: c, cpp
- members: c `&` (i32,bool, 0 modes); cpp `&` (i32,bool, 0 modes); cpp `bitand` (i32,bool, 0 modes)

  - c/op_431 / cpp/op_431 -- **total equality**
  - c/op_431 / cpp/op_935 -- **total equality**

### shared-core group zx64(Or32(ex32@0(in0:64),ex32@0(in1:64))) · (i32,bool)

- ground: connection
- languages: c, cpp
- members: c `|` (i32,bool, 0 modes); cpp `|` (i32,bool, 0 modes); cpp `bitor` (i32,bool, 0 modes)

  - c/op_359 / cpp/op_359 -- **total equality**
  - c/op_359 / cpp/op_863 -- **total equality**

### shared-core group And8(31:8,ex8@0(in1:64)) · (i32,bool)

- ground: connection
- languages: c, cpp
- members: c `<<` (i32,bool, 0 modes); c `>>` (i32,bool, 0 modes); cpp `<<` (i32,bool, 0 modes); cpp `>>` (i32,bool, 0 modes)

  - c/op_683 / cpp/op_683 -- **total equality**
  - c/op_683 / cpp/op_719 -- **core difference**
  - c/op_719 / cpp/op_683 -- **core difference**
  - c/op_719 / cpp/op_719 -- **total equality**

### shared-core group And8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64)))) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `&&` (i32,f32, 0 modes); cpp `&&` (i32,f32, 0 modes); cpp `and` (i32,f32, 0 modes)

  - c/op_321 / cpp/op_321 -- **core difference**
  - c/op_321 / cpp/op_825 -- **core difference**

### shared-core group Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64)))) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `||` (i32,f32, 0 modes); cpp `||` (i32,f32, 0 modes); cpp `or` (i32,f32, 0 modes)

  - c/op_285 / cpp/op_285 -- **core difference**
  - c/op_285 / cpp/op_789 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64)))) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `||` (i32,f32, 0 modes); c `&&` (i32,f32, 0 modes); cpp `||` (i32,f32, 0 modes); cpp `&&` (i32,f32, 0 modes); cpp `or` (i32,f32, 0 modes); cpp `and` (i32,f32, 0 modes)

  - c/op_285 / cpp/op_285 -- **core difference**
  - c/op_285 / cpp/op_321 -- **core difference**
  - c/op_285 / cpp/op_789 -- **core difference**
  - c/op_285 / cpp/op_825 -- **core difference**
  - c/op_321 / cpp/op_285 -- **core difference**
  - c/op_321 / cpp/op_321 -- **core difference**
  - c/op_321 / cpp/op_789 -- **core difference**
  - c/op_321 / cpp/op_825 -- **core difference**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))),CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256)))))) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `==` (i32,f32, 0 modes); cpp `==` (i32,f32, 0 modes)

  - c/op_465 / cpp/op_465 -- **total equality**

### shared-core group ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))),XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256)))) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `!=` (i32,f32, 0 modes); cpp `!=` (i32,f32, 0 modes); cpp `not_eq` (i32,f32, 0 modes)

  - c/op_501 / cpp/op_501 -- **total equality**
  - c/op_501 / cpp/op_969 -- **total equality**

### shared-core group ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))),Sub32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256))) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `-` (i32,f32, 0 modes); cpp `-` (i32,f32, 0 modes)

  - c/op_141 / cpp/op_141 -- **total equality**

### shared-core group ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))),Div32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256))) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `/` (i32,f32, 0 modes); cpp `/` (i32,f32, 0 modes)

  - c/op_213 / cpp/op_213 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in0:64)))),F32toF64(ex32@0(in1:256))))),0:64,u1:64))) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `>` (i32,f32, 0 modes); cpp `>` (i32,f32, 0 modes)

  - c/op_537 / cpp/op_537 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in0:64)))),F32toF64(ex32@0(in1:256))))),0:64,u1:64))) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `>=` (i32,f32, 0 modes); cpp `>=` (i32,f32, 0 modes)

  - c/op_573 / cpp/op_573 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in0:64))))))),0:64,u1:64))) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `<=` (i32,f32, 0 modes); cpp `<=` (i32,f32, 0 modes)

  - c/op_609 / cpp/op_609 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in0:64))))))),0:64,u1:64))) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `<` (i32,f32, 0 modes); cpp `<` (i32,f32, 0 modes)

  - c/op_645 / cpp/op_645 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in0:64)))),F32toF64(ex32@0(in1:256))))) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `>` (i32,f32, 0 modes); c `>=` (i32,f32, 0 modes); cpp `>` (i32,f32, 0 modes); cpp `>=` (i32,f32, 0 modes); cpp `<=>` (i32,f32, 0 modes)

  - c/op_537 / cpp/op_537 -- **core difference**
  - c/op_537 / cpp/op_573 -- **core difference**
  - c/op_537 / cpp/op_753 -- **core difference**
  - c/op_573 / cpp/op_537 -- **core difference**
  - c/op_573 / cpp/op_573 -- **core difference**
  - c/op_573 / cpp/op_753 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in0:64))))))) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `<=` (i32,f32, 0 modes); c `<` (i32,f32, 0 modes); cpp `<=` (i32,f32, 0 modes); cpp `<` (i32,f32, 0 modes); cpp `<=>` (i32,f32, 0 modes)

  - c/op_609 / cpp/op_609 -- **core difference**
  - c/op_609 / cpp/op_645 -- **core difference**
  - c/op_609 / cpp/op_753 -- **core difference**
  - c/op_645 / cpp/op_609 -- **core difference**
  - c/op_645 / cpp/op_645 -- **core difference**
  - c/op_645 / cpp/op_753 -- **core difference**

### shared-core group CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))),ex128@0(in1:256)) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `==` (i32,f32, 0 modes); c `!=` (i32,f32, 0 modes); cpp `==` (i32,f32, 0 modes); cpp `!=` (i32,f32, 0 modes); cpp `not_eq` (i32,f32, 0 modes)

  - c/op_465 / cpp/op_465 -- **total equality**
  - c/op_465 / cpp/op_501 -- **core difference**
  - c/op_465 / cpp/op_969 -- **core difference**
  - c/op_501 / cpp/op_465 -- **core difference**
  - c/op_501 / cpp/op_501 -- **total equality**
  - c/op_501 / cpp/op_969 -- **total equality**

### shared-core group Add32F0x4(ex128@0(in1:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))))) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `+` (i32,f32, 0 modes); cpp `+` (i32,f32, 0 modes)

  - c/op_105 / cpp/op_105 -- **total equality**

### shared-core group Mul32F0x4(ex128@0(in1:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64)))))) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `*` (i32,f32, 0 modes); cpp `*` (i32,f32, 0 modes)

  - c/op_177 / cpp/op_177 -- **total equality**

### shared-core group ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I32StoF64(ex32@0(in0:64))))) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `+` (i32,f32, 0 modes); c `-` (i32,f32, 0 modes); c `*` (i32,f32, 0 modes); c `/` (i32,f32, 0 modes); c `==` (i32,f32, 0 modes); c `!=` (i32,f32, 0 modes); cpp `+` (i32,f32, 0 modes); cpp `-` (i32,f32, 0 modes); cpp `*` (i32,f32, 0 modes); cpp `/` (i32,f32, 0 modes); cpp `==` (i32,f32, 0 modes); cpp `!=` (i32,f32, 0 modes); cpp `not_eq` (i32,f32, 0 modes)

  - c/op_105 / cpp/op_105 -- **total equality**
  - c/op_105 / cpp/op_141 -- **core difference**
  - c/op_105 / cpp/op_177 -- **core difference**
  - c/op_105 / cpp/op_213 -- **core difference**
  - c/op_105 / cpp/op_465 -- **core difference**
  - c/op_105 / cpp/op_501 -- **core difference**
  - c/op_105 / cpp/op_969 -- **core difference**
  - c/op_141 / cpp/op_105 -- **core difference**
  - c/op_141 / cpp/op_141 -- **total equality**
  - c/op_141 / cpp/op_177 -- **core difference**
  - c/op_141 / cpp/op_213 -- **core difference**
  - c/op_141 / cpp/op_465 -- **core difference**
  - c/op_141 / cpp/op_501 -- **core difference**
  - c/op_141 / cpp/op_969 -- **core difference**
  - c/op_177 / cpp/op_105 -- **core difference**
  - c/op_177 / cpp/op_141 -- **core difference**
  - c/op_177 / cpp/op_177 -- **total equality**
  - c/op_177 / cpp/op_213 -- **core difference**
  - c/op_177 / cpp/op_465 -- **core difference**
  - c/op_177 / cpp/op_501 -- **core difference**
  - c/op_177 / cpp/op_969 -- **core difference**
  - c/op_213 / cpp/op_105 -- **core difference**
  - c/op_213 / cpp/op_141 -- **core difference**
  - c/op_213 / cpp/op_177 -- **core difference**
  - c/op_213 / cpp/op_213 -- **total equality**
  - c/op_213 / cpp/op_465 -- **core difference**
  - c/op_213 / cpp/op_501 -- **core difference**
  - c/op_213 / cpp/op_969 -- **core difference**
  - c/op_465 / cpp/op_105 -- **core difference**
  - c/op_465 / cpp/op_141 -- **core difference**
  - c/op_465 / cpp/op_177 -- **core difference**
  - c/op_465 / cpp/op_213 -- **core difference**
  - c/op_465 / cpp/op_465 -- **total equality**
  - c/op_465 / cpp/op_501 -- **core difference**
  - c/op_465 / cpp/op_969 -- **core difference**
  - c/op_501 / cpp/op_105 -- **core difference**
  - c/op_501 / cpp/op_141 -- **core difference**
  - c/op_501 / cpp/op_177 -- **core difference**
  - c/op_501 / cpp/op_213 -- **core difference**
  - c/op_501 / cpp/op_465 -- **core difference**
  - c/op_501 / cpp/op_501 -- **total equality**
  - c/op_501 / cpp/op_969 -- **total equality**

### shared-core group F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I32StoF64(ex32@0(in0:64)))) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `>` (i32,f32, 0 modes); c `>=` (i32,f32, 0 modes); c `<=` (i32,f32, 0 modes); c `<` (i32,f32, 0 modes); cpp `>` (i32,f32, 0 modes); cpp `>=` (i32,f32, 0 modes); cpp `<=` (i32,f32, 0 modes); cpp `<` (i32,f32, 0 modes); cpp `<=>` (i32,f32, 0 modes)

  - c/op_537 / cpp/op_537 -- **core difference**
  - c/op_537 / cpp/op_573 -- **core difference**
  - c/op_537 / cpp/op_609 -- **core difference**
  - c/op_537 / cpp/op_645 -- **core difference**
  - c/op_537 / cpp/op_753 -- **core difference**
  - c/op_573 / cpp/op_537 -- **core difference**
  - c/op_573 / cpp/op_573 -- **core difference**
  - c/op_573 / cpp/op_609 -- **core difference**
  - c/op_573 / cpp/op_645 -- **core difference**
  - c/op_573 / cpp/op_753 -- **core difference**
  - c/op_609 / cpp/op_537 -- **core difference**
  - c/op_609 / cpp/op_573 -- **core difference**
  - c/op_609 / cpp/op_609 -- **core difference**
  - c/op_609 / cpp/op_645 -- **core difference**
  - c/op_609 / cpp/op_753 -- **core difference**
  - c/op_645 / cpp/op_537 -- **core difference**
  - c/op_645 / cpp/op_573 -- **core difference**
  - c/op_645 / cpp/op_609 -- **core difference**
  - c/op_645 / cpp/op_645 -- **core difference**
  - c/op_645 / cpp/op_753 -- **core difference**

### shared-core group I32StoF64(ex32@0(in0:64)) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `+` (i32,f32, 0 modes); c `-` (i32,f32, 0 modes); c `*` (i32,f32, 0 modes); c `/` (i32,f32, 0 modes); c `==` (i32,f32, 0 modes); c `!=` (i32,f32, 0 modes); c `>` (i32,f32, 0 modes); c `>=` (i32,f32, 0 modes); c `<=` (i32,f32, 0 modes); c `<` (i32,f32, 0 modes); cpp `+` (i32,f32, 0 modes); cpp `-` (i32,f32, 0 modes); cpp `*` (i32,f32, 0 modes); cpp `/` (i32,f32, 0 modes); cpp `==` (i32,f32, 0 modes); cpp `!=` (i32,f32, 0 modes); cpp `>` (i32,f32, 0 modes); cpp `>=` (i32,f32, 0 modes); cpp `<=` (i32,f32, 0 modes); cpp `<` (i32,f32, 0 modes); cpp `<=>` (i32,f32, 0 modes); cpp `not_eq` (i32,f32, 0 modes)

  - c/op_105 / cpp/op_105 -- **total equality**
  - c/op_105 / cpp/op_141 -- **core difference**
  - c/op_105 / cpp/op_177 -- **core difference**
  - c/op_105 / cpp/op_213 -- **core difference**
  - c/op_105 / cpp/op_465 -- **core difference**
  - c/op_105 / cpp/op_501 -- **core difference**
  - c/op_105 / cpp/op_537 -- **core difference**
  - c/op_105 / cpp/op_573 -- **core difference**
  - c/op_105 / cpp/op_609 -- **core difference**
  - c/op_105 / cpp/op_645 -- **core difference**
  - c/op_105 / cpp/op_753 -- **core difference**
  - c/op_105 / cpp/op_969 -- **core difference**
  - c/op_141 / cpp/op_105 -- **core difference**
  - c/op_141 / cpp/op_141 -- **total equality**
  - c/op_141 / cpp/op_177 -- **core difference**
  - c/op_141 / cpp/op_213 -- **core difference**
  - c/op_141 / cpp/op_465 -- **core difference**
  - c/op_141 / cpp/op_501 -- **core difference**
  - c/op_141 / cpp/op_537 -- **core difference**
  - c/op_141 / cpp/op_573 -- **core difference**
  - c/op_141 / cpp/op_609 -- **core difference**
  - c/op_141 / cpp/op_645 -- **core difference**
  - c/op_141 / cpp/op_753 -- **core difference**
  - c/op_141 / cpp/op_969 -- **core difference**
  - c/op_177 / cpp/op_105 -- **core difference**
  - c/op_177 / cpp/op_141 -- **core difference**
  - c/op_177 / cpp/op_177 -- **total equality**
  - c/op_177 / cpp/op_213 -- **core difference**
  - c/op_177 / cpp/op_465 -- **core difference**
  - c/op_177 / cpp/op_501 -- **core difference**
  - c/op_177 / cpp/op_537 -- **core difference**
  - c/op_177 / cpp/op_573 -- **core difference**
  - c/op_177 / cpp/op_609 -- **core difference**
  - c/op_177 / cpp/op_645 -- **core difference**
  - c/op_177 / cpp/op_753 -- **core difference**
  - c/op_177 / cpp/op_969 -- **core difference**
  - c/op_213 / cpp/op_105 -- **core difference**
  - c/op_213 / cpp/op_141 -- **core difference**
  - c/op_213 / cpp/op_177 -- **core difference**
  - c/op_213 / cpp/op_213 -- **total equality**
  - c/op_213 / cpp/op_465 -- **core difference**
  - c/op_213 / cpp/op_501 -- **core difference**
  - c/op_213 / cpp/op_537 -- **core difference**
  - c/op_213 / cpp/op_573 -- **core difference**
  - c/op_213 / cpp/op_609 -- **core difference**
  - c/op_213 / cpp/op_645 -- **core difference**
  - c/op_213 / cpp/op_753 -- **core difference**
  - c/op_213 / cpp/op_969 -- **core difference**
  - c/op_465 / cpp/op_105 -- **core difference**
  - c/op_465 / cpp/op_141 -- **core difference**
  - c/op_465 / cpp/op_177 -- **core difference**
  - c/op_465 / cpp/op_213 -- **core difference**
  - c/op_465 / cpp/op_465 -- **total equality**
  - c/op_465 / cpp/op_501 -- **core difference**
  - c/op_465 / cpp/op_537 -- **core difference**
  - c/op_465 / cpp/op_573 -- **core difference**
  - c/op_465 / cpp/op_609 -- **core difference**
  - c/op_465 / cpp/op_645 -- **core difference**
  - c/op_465 / cpp/op_753 -- **core difference**
  - c/op_465 / cpp/op_969 -- **core difference**
  - c/op_501 / cpp/op_105 -- **core difference**
  - c/op_501 / cpp/op_141 -- **core difference**
  - c/op_501 / cpp/op_177 -- **core difference**
  - c/op_501 / cpp/op_213 -- **core difference**
  - c/op_501 / cpp/op_465 -- **core difference**
  - c/op_501 / cpp/op_501 -- **total equality**
  - c/op_501 / cpp/op_537 -- **core difference**
  - c/op_501 / cpp/op_573 -- **core difference**
  - c/op_501 / cpp/op_609 -- **core difference**
  - c/op_501 / cpp/op_645 -- **core difference**
  - c/op_501 / cpp/op_753 -- **core difference**
  - c/op_501 / cpp/op_969 -- **total equality**
  - c/op_537 / cpp/op_105 -- **core difference**
  - c/op_537 / cpp/op_141 -- **core difference**
  - c/op_537 / cpp/op_177 -- **core difference**
  - c/op_537 / cpp/op_213 -- **core difference**
  - c/op_537 / cpp/op_465 -- **core difference**
  - c/op_537 / cpp/op_501 -- **core difference**
  - c/op_537 / cpp/op_537 -- **core difference**
  - c/op_537 / cpp/op_573 -- **core difference**
  - c/op_537 / cpp/op_609 -- **core difference**
  - c/op_537 / cpp/op_645 -- **core difference**
  - c/op_537 / cpp/op_753 -- **core difference**
  - c/op_537 / cpp/op_969 -- **core difference**
  - c/op_573 / cpp/op_105 -- **core difference**
  - c/op_573 / cpp/op_141 -- **core difference**
  - c/op_573 / cpp/op_177 -- **core difference**
  - c/op_573 / cpp/op_213 -- **core difference**
  - c/op_573 / cpp/op_465 -- **core difference**
  - c/op_573 / cpp/op_501 -- **core difference**
  - c/op_573 / cpp/op_537 -- **core difference**
  - c/op_573 / cpp/op_573 -- **core difference**
  - c/op_573 / cpp/op_609 -- **core difference**
  - c/op_573 / cpp/op_645 -- **core difference**
  - c/op_573 / cpp/op_753 -- **core difference**
  - c/op_573 / cpp/op_969 -- **core difference**
  - c/op_609 / cpp/op_105 -- **core difference**
  - c/op_609 / cpp/op_141 -- **core difference**
  - c/op_609 / cpp/op_177 -- **core difference**
  - c/op_609 / cpp/op_213 -- **core difference**
  - c/op_609 / cpp/op_465 -- **core difference**
  - c/op_609 / cpp/op_501 -- **core difference**
  - c/op_609 / cpp/op_537 -- **core difference**
  - c/op_609 / cpp/op_573 -- **core difference**
  - c/op_609 / cpp/op_609 -- **core difference**
  - c/op_609 / cpp/op_645 -- **core difference**
  - c/op_609 / cpp/op_753 -- **core difference**
  - c/op_609 / cpp/op_969 -- **core difference**
  - c/op_645 / cpp/op_105 -- **core difference**
  - c/op_645 / cpp/op_141 -- **core difference**
  - c/op_645 / cpp/op_177 -- **core difference**
  - c/op_645 / cpp/op_213 -- **core difference**
  - c/op_645 / cpp/op_465 -- **core difference**
  - c/op_645 / cpp/op_501 -- **core difference**
  - c/op_645 / cpp/op_537 -- **core difference**
  - c/op_645 / cpp/op_573 -- **core difference**
  - c/op_645 / cpp/op_609 -- **core difference**
  - c/op_645 / cpp/op_645 -- **core difference**
  - c/op_645 / cpp/op_753 -- **core difference**
  - c/op_645 / cpp/op_969 -- **core difference**

### shared-core group F32toF64(ex32@0(in1:256)) · (i32,f32)

- ground: connection
- languages: c, cpp
- members: c `||` (i32,f32, 0 modes); c `&&` (i32,f32, 0 modes); c `>` (i32,f32, 0 modes); c `>=` (i32,f32, 0 modes); c `<=` (i32,f32, 0 modes); c `<` (i32,f32, 0 modes); cpp `||` (i32,f32, 0 modes); cpp `&&` (i32,f32, 0 modes); cpp `>` (i32,f32, 0 modes); cpp `>=` (i32,f32, 0 modes); cpp `<=` (i32,f32, 0 modes); cpp `<` (i32,f32, 0 modes); cpp `<=>` (i32,f32, 0 modes); cpp `or` (i32,f32, 0 modes); cpp `and` (i32,f32, 0 modes)

  - c/op_285 / cpp/op_285 -- **core difference**
  - c/op_285 / cpp/op_321 -- **core difference**
  - c/op_285 / cpp/op_537 -- **core difference**
  - c/op_285 / cpp/op_573 -- **core difference**
  - c/op_285 / cpp/op_609 -- **core difference**
  - c/op_285 / cpp/op_645 -- **core difference**
  - c/op_285 / cpp/op_753 -- **core difference**
  - c/op_285 / cpp/op_789 -- **core difference**
  - c/op_285 / cpp/op_825 -- **core difference**
  - c/op_321 / cpp/op_285 -- **core difference**
  - c/op_321 / cpp/op_321 -- **core difference**
  - c/op_321 / cpp/op_537 -- **core difference**
  - c/op_321 / cpp/op_573 -- **core difference**
  - c/op_321 / cpp/op_609 -- **core difference**
  - c/op_321 / cpp/op_645 -- **core difference**
  - c/op_321 / cpp/op_753 -- **core difference**
  - c/op_321 / cpp/op_789 -- **core difference**
  - c/op_321 / cpp/op_825 -- **core difference**
  - c/op_537 / cpp/op_285 -- **core difference**
  - c/op_537 / cpp/op_321 -- **core difference**
  - c/op_537 / cpp/op_537 -- **core difference**
  - c/op_537 / cpp/op_573 -- **core difference**
  - c/op_537 / cpp/op_609 -- **core difference**
  - c/op_537 / cpp/op_645 -- **core difference**
  - c/op_537 / cpp/op_753 -- **core difference**
  - c/op_537 / cpp/op_789 -- **core difference**
  - c/op_537 / cpp/op_825 -- **core difference**
  - c/op_573 / cpp/op_285 -- **core difference**
  - c/op_573 / cpp/op_321 -- **core difference**
  - c/op_573 / cpp/op_537 -- **core difference**
  - c/op_573 / cpp/op_573 -- **core difference**
  - c/op_573 / cpp/op_609 -- **core difference**
  - c/op_573 / cpp/op_645 -- **core difference**
  - c/op_573 / cpp/op_753 -- **core difference**
  - c/op_573 / cpp/op_789 -- **core difference**
  - c/op_573 / cpp/op_825 -- **core difference**
  - c/op_609 / cpp/op_285 -- **core difference**
  - c/op_609 / cpp/op_321 -- **core difference**
  - c/op_609 / cpp/op_537 -- **core difference**
  - c/op_609 / cpp/op_573 -- **core difference**
  - c/op_609 / cpp/op_609 -- **core difference**
  - c/op_609 / cpp/op_645 -- **core difference**
  - c/op_609 / cpp/op_753 -- **core difference**
  - c/op_609 / cpp/op_789 -- **core difference**
  - c/op_609 / cpp/op_825 -- **core difference**
  - c/op_645 / cpp/op_285 -- **core difference**
  - c/op_645 / cpp/op_321 -- **core difference**
  - c/op_645 / cpp/op_537 -- **core difference**
  - c/op_645 / cpp/op_573 -- **core difference**
  - c/op_645 / cpp/op_609 -- **core difference**
  - c/op_645 / cpp/op_645 -- **core difference**
  - c/op_645 / cpp/op_753 -- **core difference**
  - c/op_645 / cpp/op_789 -- **core difference**
  - c/op_645 / cpp/op_825 -- **core difference**

### shared-core group And8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64)))) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `&&` (i32,f64, 0 modes); cpp `&&` (i32,f64, 0 modes); cpp `and` (i32,f64, 0 modes)

  - c/op_322 / cpp/op_322 -- **core difference**
  - c/op_322 / cpp/op_826 -- **core difference**

### shared-core group Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64)))) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `||` (i32,f64, 0 modes); cpp `||` (i32,f64, 0 modes); cpp `or` (i32,f64, 0 modes)

  - c/op_286 / cpp/op_286 -- **core difference**
  - c/op_286 / cpp/op_790 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64)))) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `||` (i32,f64, 0 modes); c `&&` (i32,f64, 0 modes); cpp `||` (i32,f64, 0 modes); cpp `&&` (i32,f64, 0 modes); cpp `or` (i32,f64, 0 modes); cpp `and` (i32,f64, 0 modes)

  - c/op_286 / cpp/op_286 -- **core difference**
  - c/op_286 / cpp/op_322 -- **core difference**
  - c/op_286 / cpp/op_790 -- **core difference**
  - c/op_286 / cpp/op_826 -- **core difference**
  - c/op_322 / cpp/op_286 -- **core difference**
  - c/op_322 / cpp/op_322 -- **core difference**
  - c/op_322 / cpp/op_790 -- **core difference**
  - c/op_322 / cpp/op_826 -- **core difference**

### shared-core group ins@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))),XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256)))) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `!=` (i32,f64, 0 modes); cpp `!=` (i32,f64, 0 modes); cpp `not_eq` (i32,f64, 0 modes)

  - c/op_502 / cpp/op_502 -- **total equality**
  - c/op_502 / cpp/op_970 -- **total equality**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))),CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256)))))) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `==` (i32,f64, 0 modes); cpp `==` (i32,f64, 0 modes)

  - c/op_466 / cpp/op_466 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex64@0(in1:256)))),0:64,u1:64))) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `>` (i32,f64, 0 modes); cpp `>` (i32,f64, 0 modes)

  - c/op_538 / cpp/op_538 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex64@0(in1:256)))),0:64,u1:64))) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `>=` (i32,f64, 0 modes); cpp `>=` (i32,f64, 0 modes)

  - c/op_574 / cpp/op_574 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))))))),0:64,u1:64))) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `<=` (i32,f64, 0 modes); cpp `<=` (i32,f64, 0 modes)

  - c/op_610 / cpp/op_610 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))))))),0:64,u1:64))) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `<` (i32,f64, 0 modes); cpp `<` (i32,f64, 0 modes)

  - c/op_646 / cpp/op_646 -- **core difference**

### shared-core group ins@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))),Sub64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256))) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `-` (i32,f64, 0 modes); cpp `-` (i32,f64, 0 modes)

  - c/op_142 / cpp/op_142 -- **total equality**

### shared-core group ins@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))),Div64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256))) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `/` (i32,f64, 0 modes); cpp `/` (i32,f64, 0 modes)

  - c/op_214 / cpp/op_214 -- **total equality**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex64@0(in1:256)))) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `>` (i32,f64, 0 modes); c `>=` (i32,f64, 0 modes); cpp `>` (i32,f64, 0 modes); cpp `>=` (i32,f64, 0 modes); cpp `<=>` (i32,f64, 0 modes)

  - c/op_538 / cpp/op_538 -- **core difference**
  - c/op_538 / cpp/op_574 -- **core difference**
  - c/op_538 / cpp/op_754 -- **core difference**
  - c/op_574 / cpp/op_538 -- **core difference**
  - c/op_574 / cpp/op_574 -- **core difference**
  - c/op_574 / cpp/op_754 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))))))) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `<=` (i32,f64, 0 modes); c `<` (i32,f64, 0 modes); cpp `<=` (i32,f64, 0 modes); cpp `<` (i32,f64, 0 modes); cpp `<=>` (i32,f64, 0 modes)

  - c/op_610 / cpp/op_610 -- **core difference**
  - c/op_610 / cpp/op_646 -- **core difference**
  - c/op_610 / cpp/op_754 -- **core difference**
  - c/op_646 / cpp/op_610 -- **core difference**
  - c/op_646 / cpp/op_646 -- **core difference**
  - c/op_646 / cpp/op_754 -- **core difference**

### shared-core group CmpEQ64F0x2(ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))),ex128@0(in1:256)) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `==` (i32,f64, 0 modes); c `!=` (i32,f64, 0 modes); cpp `==` (i32,f64, 0 modes); cpp `!=` (i32,f64, 0 modes); cpp `not_eq` (i32,f64, 0 modes)

  - c/op_466 / cpp/op_466 -- **total equality**
  - c/op_466 / cpp/op_502 -- **core difference**
  - c/op_466 / cpp/op_970 -- **core difference**
  - c/op_502 / cpp/op_466 -- **core difference**
  - c/op_502 / cpp/op_502 -- **total equality**
  - c/op_502 / cpp/op_970 -- **total equality**

### shared-core group Add64F0x2(ex128@0(in1:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))))) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `+` (i32,f64, 0 modes); cpp `+` (i32,f64, 0 modes)

  - c/op_106 / cpp/op_106 -- **total equality**

### shared-core group Mul64F0x2(ex128@0(in1:256),ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64))))) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `*` (i32,f64, 0 modes); cpp `*` (i32,f64, 0 modes)

  - c/op_178 / cpp/op_178 -- **total equality**

### shared-core group ex128@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `+` (i32,f64, 0 modes); c `-` (i32,f64, 0 modes); c `*` (i32,f64, 0 modes); c `/` (i32,f64, 0 modes); c `==` (i32,f64, 0 modes); c `!=` (i32,f64, 0 modes); cpp `+` (i32,f64, 0 modes); cpp `-` (i32,f64, 0 modes); cpp `*` (i32,f64, 0 modes); cpp `/` (i32,f64, 0 modes); cpp `==` (i32,f64, 0 modes); cpp `!=` (i32,f64, 0 modes); cpp `not_eq` (i32,f64, 0 modes)

  - c/op_106 / cpp/op_106 -- **total equality**
  - c/op_106 / cpp/op_142 -- **core difference**
  - c/op_106 / cpp/op_178 -- **core difference**
  - c/op_106 / cpp/op_214 -- **core difference**
  - c/op_106 / cpp/op_466 -- **core difference**
  - c/op_106 / cpp/op_502 -- **core difference**
  - c/op_106 / cpp/op_970 -- **core difference**
  - c/op_142 / cpp/op_106 -- **core difference**
  - c/op_142 / cpp/op_142 -- **total equality**
  - c/op_142 / cpp/op_178 -- **core difference**
  - c/op_142 / cpp/op_214 -- **core difference**
  - c/op_142 / cpp/op_466 -- **core difference**
  - c/op_142 / cpp/op_502 -- **core difference**
  - c/op_142 / cpp/op_970 -- **core difference**
  - c/op_178 / cpp/op_106 -- **core difference**
  - c/op_178 / cpp/op_142 -- **core difference**
  - c/op_178 / cpp/op_178 -- **total equality**
  - c/op_178 / cpp/op_214 -- **core difference**
  - c/op_178 / cpp/op_466 -- **core difference**
  - c/op_178 / cpp/op_502 -- **core difference**
  - c/op_178 / cpp/op_970 -- **core difference**
  - c/op_214 / cpp/op_106 -- **core difference**
  - c/op_214 / cpp/op_142 -- **core difference**
  - c/op_214 / cpp/op_178 -- **core difference**
  - c/op_214 / cpp/op_214 -- **total equality**
  - c/op_214 / cpp/op_466 -- **core difference**
  - c/op_214 / cpp/op_502 -- **core difference**
  - c/op_214 / cpp/op_970 -- **core difference**
  - c/op_466 / cpp/op_106 -- **core difference**
  - c/op_466 / cpp/op_142 -- **core difference**
  - c/op_466 / cpp/op_178 -- **core difference**
  - c/op_466 / cpp/op_214 -- **core difference**
  - c/op_466 / cpp/op_466 -- **total equality**
  - c/op_466 / cpp/op_502 -- **core difference**
  - c/op_466 / cpp/op_970 -- **core difference**
  - c/op_502 / cpp/op_106 -- **core difference**
  - c/op_502 / cpp/op_142 -- **core difference**
  - c/op_502 / cpp/op_178 -- **core difference**
  - c/op_502 / cpp/op_214 -- **core difference**
  - c/op_502 / cpp/op_466 -- **core difference**
  - c/op_502 / cpp/op_502 -- **total equality**
  - c/op_502 / cpp/op_970 -- **total equality**

### shared-core group ex64@0(ins@0(u0:256,I32StoF64(ex32@0(in0:64)))) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `>` (i32,f64, 0 modes); c `>=` (i32,f64, 0 modes); c `<=` (i32,f64, 0 modes); c `<` (i32,f64, 0 modes); cpp `>` (i32,f64, 0 modes); cpp `>=` (i32,f64, 0 modes); cpp `<=` (i32,f64, 0 modes); cpp `<` (i32,f64, 0 modes); cpp `<=>` (i32,f64, 0 modes)

  - c/op_538 / cpp/op_538 -- **core difference**
  - c/op_538 / cpp/op_574 -- **core difference**
  - c/op_538 / cpp/op_610 -- **core difference**
  - c/op_538 / cpp/op_646 -- **core difference**
  - c/op_538 / cpp/op_754 -- **core difference**
  - c/op_574 / cpp/op_538 -- **core difference**
  - c/op_574 / cpp/op_574 -- **core difference**
  - c/op_574 / cpp/op_610 -- **core difference**
  - c/op_574 / cpp/op_646 -- **core difference**
  - c/op_574 / cpp/op_754 -- **core difference**
  - c/op_610 / cpp/op_538 -- **core difference**
  - c/op_610 / cpp/op_574 -- **core difference**
  - c/op_610 / cpp/op_610 -- **core difference**
  - c/op_610 / cpp/op_646 -- **core difference**
  - c/op_610 / cpp/op_754 -- **core difference**
  - c/op_646 / cpp/op_538 -- **core difference**
  - c/op_646 / cpp/op_574 -- **core difference**
  - c/op_646 / cpp/op_610 -- **core difference**
  - c/op_646 / cpp/op_646 -- **core difference**
  - c/op_646 / cpp/op_754 -- **core difference**

### shared-core group ins@0(u0:256,I32StoF64(ex32@0(in0:64))) · (i32,f64)

- ground: connection
- languages: c, cpp
- members: c `+` (i32,f64, 0 modes); c `-` (i32,f64, 0 modes); c `*` (i32,f64, 0 modes); c `/` (i32,f64, 0 modes); c `==` (i32,f64, 0 modes); c `!=` (i32,f64, 0 modes); c `>` (i32,f64, 0 modes); c `>=` (i32,f64, 0 modes); c `<=` (i32,f64, 0 modes); c `<` (i32,f64, 0 modes); cpp `+` (i32,f64, 0 modes); cpp `-` (i32,f64, 0 modes); cpp `*` (i32,f64, 0 modes); cpp `/` (i32,f64, 0 modes); cpp `==` (i32,f64, 0 modes); cpp `!=` (i32,f64, 0 modes); cpp `>` (i32,f64, 0 modes); cpp `>=` (i32,f64, 0 modes); cpp `<=` (i32,f64, 0 modes); cpp `<` (i32,f64, 0 modes); cpp `<=>` (i32,f64, 0 modes); cpp `not_eq` (i32,f64, 0 modes)

  - c/op_106 / cpp/op_106 -- **total equality**
  - c/op_106 / cpp/op_142 -- **core difference**
  - c/op_106 / cpp/op_178 -- **core difference**
  - c/op_106 / cpp/op_214 -- **core difference**
  - c/op_106 / cpp/op_466 -- **core difference**
  - c/op_106 / cpp/op_502 -- **core difference**
  - c/op_106 / cpp/op_538 -- **core difference**
  - c/op_106 / cpp/op_574 -- **core difference**
  - c/op_106 / cpp/op_610 -- **core difference**
  - c/op_106 / cpp/op_646 -- **core difference**
  - c/op_106 / cpp/op_754 -- **core difference**
  - c/op_106 / cpp/op_970 -- **core difference**
  - c/op_142 / cpp/op_106 -- **core difference**
  - c/op_142 / cpp/op_142 -- **total equality**
  - c/op_142 / cpp/op_178 -- **core difference**
  - c/op_142 / cpp/op_214 -- **core difference**
  - c/op_142 / cpp/op_466 -- **core difference**
  - c/op_142 / cpp/op_502 -- **core difference**
  - c/op_142 / cpp/op_538 -- **core difference**
  - c/op_142 / cpp/op_574 -- **core difference**
  - c/op_142 / cpp/op_610 -- **core difference**
  - c/op_142 / cpp/op_646 -- **core difference**
  - c/op_142 / cpp/op_754 -- **core difference**
  - c/op_142 / cpp/op_970 -- **core difference**
  - c/op_178 / cpp/op_106 -- **core difference**
  - c/op_178 / cpp/op_142 -- **core difference**
  - c/op_178 / cpp/op_178 -- **total equality**
  - c/op_178 / cpp/op_214 -- **core difference**
  - c/op_178 / cpp/op_466 -- **core difference**
  - c/op_178 / cpp/op_502 -- **core difference**
  - c/op_178 / cpp/op_538 -- **core difference**
  - c/op_178 / cpp/op_574 -- **core difference**
  - c/op_178 / cpp/op_610 -- **core difference**
  - c/op_178 / cpp/op_646 -- **core difference**
  - c/op_178 / cpp/op_754 -- **core difference**
  - c/op_178 / cpp/op_970 -- **core difference**
  - c/op_214 / cpp/op_106 -- **core difference**
  - c/op_214 / cpp/op_142 -- **core difference**
  - c/op_214 / cpp/op_178 -- **core difference**
  - c/op_214 / cpp/op_214 -- **total equality**
  - c/op_214 / cpp/op_466 -- **core difference**
  - c/op_214 / cpp/op_502 -- **core difference**
  - c/op_214 / cpp/op_538 -- **core difference**
  - c/op_214 / cpp/op_574 -- **core difference**
  - c/op_214 / cpp/op_610 -- **core difference**
  - c/op_214 / cpp/op_646 -- **core difference**
  - c/op_214 / cpp/op_754 -- **core difference**
  - c/op_214 / cpp/op_970 -- **core difference**
  - c/op_466 / cpp/op_106 -- **core difference**
  - c/op_466 / cpp/op_142 -- **core difference**
  - c/op_466 / cpp/op_178 -- **core difference**
  - c/op_466 / cpp/op_214 -- **core difference**
  - c/op_466 / cpp/op_466 -- **total equality**
  - c/op_466 / cpp/op_502 -- **core difference**
  - c/op_466 / cpp/op_538 -- **core difference**
  - c/op_466 / cpp/op_574 -- **core difference**
  - c/op_466 / cpp/op_610 -- **core difference**
  - c/op_466 / cpp/op_646 -- **core difference**
  - c/op_466 / cpp/op_754 -- **core difference**
  - c/op_466 / cpp/op_970 -- **core difference**
  - c/op_502 / cpp/op_106 -- **core difference**
  - c/op_502 / cpp/op_142 -- **core difference**
  - c/op_502 / cpp/op_178 -- **core difference**
  - c/op_502 / cpp/op_214 -- **core difference**
  - c/op_502 / cpp/op_466 -- **core difference**
  - c/op_502 / cpp/op_502 -- **total equality**
  - c/op_502 / cpp/op_538 -- **core difference**
  - c/op_502 / cpp/op_574 -- **core difference**
  - c/op_502 / cpp/op_610 -- **core difference**
  - c/op_502 / cpp/op_646 -- **core difference**
  - c/op_502 / cpp/op_754 -- **core difference**
  - c/op_502 / cpp/op_970 -- **total equality**
  - c/op_538 / cpp/op_106 -- **core difference**
  - c/op_538 / cpp/op_142 -- **core difference**
  - c/op_538 / cpp/op_178 -- **core difference**
  - c/op_538 / cpp/op_214 -- **core difference**
  - c/op_538 / cpp/op_466 -- **core difference**
  - c/op_538 / cpp/op_502 -- **core difference**
  - c/op_538 / cpp/op_538 -- **core difference**
  - c/op_538 / cpp/op_574 -- **core difference**
  - c/op_538 / cpp/op_610 -- **core difference**
  - c/op_538 / cpp/op_646 -- **core difference**
  - c/op_538 / cpp/op_754 -- **core difference**
  - c/op_538 / cpp/op_970 -- **core difference**
  - c/op_574 / cpp/op_106 -- **core difference**
  - c/op_574 / cpp/op_142 -- **core difference**
  - c/op_574 / cpp/op_178 -- **core difference**
  - c/op_574 / cpp/op_214 -- **core difference**
  - c/op_574 / cpp/op_466 -- **core difference**
  - c/op_574 / cpp/op_502 -- **core difference**
  - c/op_574 / cpp/op_538 -- **core difference**
  - c/op_574 / cpp/op_574 -- **core difference**
  - c/op_574 / cpp/op_610 -- **core difference**
  - c/op_574 / cpp/op_646 -- **core difference**
  - c/op_574 / cpp/op_754 -- **core difference**
  - c/op_574 / cpp/op_970 -- **core difference**
  - c/op_610 / cpp/op_106 -- **core difference**
  - c/op_610 / cpp/op_142 -- **core difference**
  - c/op_610 / cpp/op_178 -- **core difference**
  - c/op_610 / cpp/op_214 -- **core difference**
  - c/op_610 / cpp/op_466 -- **core difference**
  - c/op_610 / cpp/op_502 -- **core difference**
  - c/op_610 / cpp/op_538 -- **core difference**
  - c/op_610 / cpp/op_574 -- **core difference**
  - c/op_610 / cpp/op_610 -- **core difference**
  - c/op_610 / cpp/op_646 -- **core difference**
  - c/op_610 / cpp/op_754 -- **core difference**
  - c/op_610 / cpp/op_970 -- **core difference**
  - c/op_646 / cpp/op_106 -- **core difference**
  - c/op_646 / cpp/op_142 -- **core difference**
  - c/op_646 / cpp/op_178 -- **core difference**
  - c/op_646 / cpp/op_214 -- **core difference**
  - c/op_646 / cpp/op_466 -- **core difference**
  - c/op_646 / cpp/op_502 -- **core difference**
  - c/op_646 / cpp/op_538 -- **core difference**
  - c/op_646 / cpp/op_574 -- **core difference**
  - c/op_646 / cpp/op_610 -- **core difference**
  - c/op_646 / cpp/op_646 -- **core difference**
  - c/op_646 / cpp/op_754 -- **core difference**
  - c/op_646 / cpp/op_970 -- **core difference**

### shared-core group And8(zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64)))) · (i32,i32)

- ground: connection
- languages: c, cpp
- members: c `&&` (i32,i32, 0 modes); cpp `&&` (i32,i32, 0 modes); cpp `and` (i32,i32, 0 modes)

  - c/op_318 / cpp/op_318 -- **core difference**
  - c/op_318 / cpp/op_822 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(Or32(ex32@0(in0:64),ex32@0(in1:64))),0:64,u0:64))) · (i32,i32)

- ground: connection
- languages: c, cpp
- members: c `||` (i32,i32, 0 modes); cpp `||` (i32,i32, 0 modes); cpp `or` (i32,i32, 0 modes)

  - c/op_282 / cpp/op_282 -- **core difference**
  - c/op_282 / cpp/op_786 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(15:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64))) · (i32,i32)

- ground: connection
- languages: c, cpp, rust
- members: c `>` (i32,i32, 0 modes); cpp `>` (i32,i32, 0 modes); cpp `<=>` (i32,i32, 0 modes); rust `>` (i32,i32, 0 modes)

  - c/op_534 / cpp/op_534 -- **core difference**
  - c/op_534 / cpp/op_750 -- **core difference**
  - c/op_534 / rust/op_390 -- **core difference**
  - cpp/op_534 / rust/op_390 -- **total equality**
  - cpp/op_750 / rust/op_390 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(13:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64))) · (i32,i32)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `>=` (i32,i32, 0 modes); cpp `>=` (i32,i32, 0 modes); rust `>=` (i32,i32, 0 modes); swift `>=` (i32,i32, 0 modes)

  - c/op_570 / cpp/op_570 -- **core difference**
  - c/op_570 / rust/op_426 -- **core difference**
  - c/op_570 / swift/op_402 -- **core difference**
  - cpp/op_570 / rust/op_426 -- **total equality**
  - cpp/op_570 / swift/op_402 -- **total equality**
  - rust/op_426 / swift/op_402 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(14:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64))) · (i32,i32)

- ground: connection
- languages: c, cpp, rust
- members: c `<=` (i32,i32, 0 modes); cpp `<=` (i32,i32, 0 modes); rust `<=` (i32,i32, 0 modes)

  - c/op_606 / cpp/op_606 -- **core difference**
  - c/op_606 / rust/op_354 -- **core difference**
  - cpp/op_606 / rust/op_354 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(12:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64))) · (i32,i32)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `<` (i32,i32, 0 modes); cpp `<` (i32,i32, 0 modes); cpp `<=>` (i32,i32, 0 modes); rust `<` (i32,i32, 0 modes); swift `<` (i32,i32, 0 modes)

  - c/op_642 / cpp/op_642 -- **core difference**
  - c/op_642 / cpp/op_750 -- **core difference**
  - c/op_642 / rust/op_318 -- **core difference**
  - c/op_642 / swift/op_294 -- **core difference**
  - cpp/op_642 / rust/op_318 -- **total equality**
  - cpp/op_750 / rust/op_318 -- **core difference**
  - cpp/op_642 / swift/op_294 -- **total equality**
  - cpp/op_750 / swift/op_294 -- **core difference**
  - rust/op_318 / swift/op_294 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(13:64,7:64,zx64(ex32@0(in1:64)),zx64(ex32@0(in0:64)),u0:64))) · (i32,i32)

- ground: connection
- languages: go, swift
- members: go `<=` (i32,i32, 0 modes); swift `<=` (i32,i32, 0 modes)

  - go/op_564 / swift/op_366 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(12:64,7:64,zx64(ex32@0(in1:64)),zx64(ex32@0(in0:64)),u0:64))) · (i32,i32)

- ground: connection
- languages: go, swift
- members: go `>` (i32,i32, 0 modes); swift `>` (i32,i32, 0 modes)

  - go/op_600 / swift/op_330 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(4:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64))) · (i32,i32)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `==` (i32,i32, 0 modes); cpp `==` (i32,i32, 0 modes); rust `==` (i32,i32, 0 modes); swift `==` (i32,i32, 0 modes)

  - c/op_462 / cpp/op_462 -- **core difference**
  - c/op_462 / rust/op_246 -- **core difference**
  - c/op_462 / swift/op_510 -- **core difference**
  - cpp/op_462 / rust/op_246 -- **total equality**
  - cpp/op_462 / swift/op_510 -- **total equality**
  - rust/op_246 / swift/op_510 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64))) · (i32,i32)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `!=` (i32,i32, 0 modes); cpp `!=` (i32,i32, 0 modes); cpp `not_eq` (i32,i32, 0 modes); rust `!=` (i32,i32, 0 modes); swift `!=` (i32,i32, 0 modes)

  - c/op_498 / cpp/op_498 -- **core difference**
  - c/op_498 / cpp/op_966 -- **core difference**
  - c/op_498 / rust/op_282 -- **core difference**
  - c/op_498 / swift/op_438 -- **core difference**
  - cpp/op_498 / rust/op_282 -- **total equality**
  - cpp/op_966 / rust/op_282 -- **total equality**
  - cpp/op_498 / swift/op_438 -- **total equality**
  - cpp/op_966 / swift/op_438 -- **total equality**
  - rust/op_282 / swift/op_438 -- **total equality**

### shared-core group zx64(ex32@32(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64)))) · (i32,i32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `/` (i32,i32, 0 modes); c `%` (i32,i32, 0 modes); cpp `/` (i32,i32, 0 modes); cpp `%` (i32,i32, 0 modes); go `%` (i32,i32, 1 modes); go `/` (i32,i32, 1 modes); rust `/` (i32,i32, 2 modes); rust `%` (i32,i32, 2 modes); swift `/` (i32,i32, 2 modes); swift `%` (i32,i32, 2 modes)

  - c/op_210 / cpp/op_210 -- **total equality**
  - c/op_210 / cpp/op_246 -- **core difference**
  - c/op_246 / cpp/op_210 -- **core difference**
  - c/op_246 / cpp/op_246 -- **total equality**
  - c/op_210 / go/op_132 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - c/op_210 / go/op_96 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - c/op_246 / go/op_132 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - c/op_246 / go/op_96 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - c/op_210 / rust/op_642 -- **core equality, modes differ**
    - only on the right: `((-2147483648 + in0) | ~in1) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
  - c/op_210 / rust/op_678 -- **core difference**
    - only on the right: `((-2147483648 + in0) | ~in1) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
  - c/op_246 / rust/op_642 -- **core difference**
    - only on the right: `((-2147483648 + in0) | ~in1) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
  - c/op_246 / rust/op_678 -- **core equality, modes differ**
    - only on the right: `((-2147483648 + in0) | ~in1) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
  - c/op_210 / swift/op_150 -- **core equality, modes differ**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - c/op_210 / swift/op_186 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - c/op_246 / swift/op_150 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - c/op_246 / swift/op_186 -- **core equality, modes differ**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_210 / go/op_132 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - cpp/op_210 / go/op_96 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - cpp/op_246 / go/op_132 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - cpp/op_246 / go/op_96 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - cpp/op_210 / rust/op_642 -- **core equality, modes differ**
    - only on the right: `((-2147483648 + in0) | ~in1) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
  - cpp/op_210 / rust/op_678 -- **core difference**
    - only on the right: `((-2147483648 + in0) | ~in1) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
  - cpp/op_246 / rust/op_642 -- **core difference**
    - only on the right: `((-2147483648 + in0) | ~in1) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
  - cpp/op_246 / rust/op_678 -- **core equality, modes differ**
    - only on the right: `((-2147483648 + in0) | ~in1) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
  - cpp/op_210 / swift/op_150 -- **core equality, modes differ**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_210 / swift/op_186 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_246 / swift/op_150 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_246 / swift/op_186 -- **core equality, modes differ**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_132 / rust/op_642 -- **core difference**
    - only on the right: `((-2147483648 + in0) | ~in1) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow` (branch-to-response)
  - go/op_132 / rust/op_678 -- **core difference**
    - only on the right: `((-2147483648 + in0) | ~in1) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow` (branch-to-response)
  - go/op_96 / rust/op_642 -- **core difference**
    - only on the right: `((-2147483648 + in0) | ~in1) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow` (branch-to-response)
  - go/op_96 / rust/op_678 -- **core difference**
    - only on the right: `((-2147483648 + in0) | ~in1) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow` (branch-to-response)
  - go/op_132 / swift/op_150 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_132 / swift/op_186 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_96 / swift/op_150 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_96 / swift/op_186 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_642 / swift/op_150 -- **core equality, modes differ**
    - only on the left: `((-2147483648 + in0) | ~in1) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow` (branch-to-response)
    - only on the left: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_642 / swift/op_186 -- **core difference**
    - only on the left: `((-2147483648 + in0) | ~in1) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow` (branch-to-response)
    - only on the left: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_678 / swift/op_150 -- **core difference**
    - only on the left: `((-2147483648 + in0) | ~in1) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow` (branch-to-response)
    - only on the left: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_678 / swift/op_186 -- **core equality, modes differ**
    - only on the left: `((-2147483648 + in0) | ~in1) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow` (branch-to-response)
    - only on the left: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)

### shared-core group ex1@0(amd64g_calculate_condition(12:64,7:64,zx64(ex32@0(in1:64)),zx64(ex32@0(in0:64)),u0:64)) · (i32,i32)

- ground: connection
- languages: go, swift
- members: go `>` (i32,i32, 0 modes); swift `>` (i32,i32, 0 modes); swift `..<` (i32,i32, 1 modes); swift `...` (i32,i32, 1 modes)

  - go/op_600 / swift/op_330 -- **total equality**
  - go/op_600 / swift/op_870 -- **core difference**
    - only on the right: `in1 < in0 (signed)` -> `trap` (branch-to-response)
  - go/op_600 / swift/op_906 -- **core difference**
    - only on the right: `in1 < in0 (signed)` -> `trap` (branch-to-response)

### shared-core group zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) · (i32,i32)

- ground: connection
- languages: c, cpp, rust
- members: c `<<` (i32,i32, 0 modes); cpp `<<` (i32,i32, 0 modes); rust `<<` (i32,i32, 0 modes)

  - c/op_678 / cpp/op_678 -- **total equality**
  - c/op_678 / rust/op_462 -- **total equality**
  - cpp/op_678 / rust/op_462 -- **total equality**

### shared-core group zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) · (i32,i32)

- ground: connection
- languages: c, cpp, rust
- members: c `>>` (i32,i32, 0 modes); cpp `>>` (i32,i32, 0 modes); rust `>>` (i32,i32, 0 modes)

  - c/op_714 / cpp/op_714 -- **total equality**
  - c/op_714 / rust/op_498 -- **total equality**
  - cpp/op_714 / rust/op_498 -- **total equality**

### shared-core group ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))) · (i32,i32)

- ground: connection
- languages: c, cpp, go, rust
- members: c `<<` (i32,i32, 0 modes); cpp `<<` (i32,i32, 0 modes); go `<<` (i32,i32, 1 modes); rust `<<` (i32,i32, 0 modes)

  - c/op_678 / cpp/op_678 -- **total equality**
  - c/op_678 / go/op_168 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_678 / rust/op_462 -- **total equality**
  - cpp/op_678 / go/op_168 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_678 / rust/op_462 -- **total equality**
  - go/op_168 / rust/op_462 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)

### shared-core group zx64(Add32(ex32@0(in0:64),ex32@0(in1:64))) · (i32,i32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `+` (i32,i32, 1 modes); cpp `+` (i32,i32, 1 modes); go `+` (i32,i32, 1 modes); rust `+` (i32,i32, 1 modes); swift `+` (i32,i32, 1 modes)

  - c/op_102 / cpp/op_102 -- **total equality**
  - c/op_102 / go/op_312 -- **total equality**
  - c/op_102 / rust/op_534 -- **total equality**
  - c/op_102 / swift/op_222 -- **core equality, modes differ**
    - only on the left: `in0 + in1 overflows 32 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 + in1 overflows 32 bits (signed)` -> `trap` (branch-to-response)
  - cpp/op_102 / go/op_312 -- **total equality**
  - cpp/op_102 / rust/op_534 -- **total equality**
  - cpp/op_102 / swift/op_222 -- **core equality, modes differ**
    - only on the left: `in0 + in1 overflows 32 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 + in1 overflows 32 bits (signed)` -> `trap` (branch-to-response)
  - go/op_312 / rust/op_534 -- **total equality**
  - go/op_312 / swift/op_222 -- **core equality, modes differ**
    - only on the left: `in0 + in1 overflows 32 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 + in1 overflows 32 bits (signed)` -> `trap` (branch-to-response)
  - rust/op_534 / swift/op_222 -- **core equality, modes differ**
    - only on the left: `in0 + in1 overflows 32 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 + in1 overflows 32 bits (signed)` -> `trap` (branch-to-response)

### shared-core group zx64(Sub32(ex32@0(in0:64),ex32@0(in1:64))) · (i32,i32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `-` (i32,i32, 1 modes); cpp `-` (i32,i32, 1 modes); go `-` (i32,i32, 1 modes); rust `-` (i32,i32, 1 modes); swift `-` (i32,i32, 1 modes)

  - c/op_138 / cpp/op_138 -- **total equality**
  - c/op_138 / go/op_348 -- **total equality**
  - c/op_138 / rust/op_570 -- **total equality**
  - c/op_138 / swift/op_258 -- **core equality, modes differ**
    - only on the left: `in0 - in1 overflows 32 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 - in1 overflows 32 bits (signed)` -> `trap` (branch-to-response)
  - cpp/op_138 / go/op_348 -- **total equality**
  - cpp/op_138 / rust/op_570 -- **total equality**
  - cpp/op_138 / swift/op_258 -- **core equality, modes differ**
    - only on the left: `in0 - in1 overflows 32 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 - in1 overflows 32 bits (signed)` -> `trap` (branch-to-response)
  - go/op_348 / rust/op_570 -- **total equality**
  - go/op_348 / swift/op_258 -- **core equality, modes differ**
    - only on the left: `in0 - in1 overflows 32 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 - in1 overflows 32 bits (signed)` -> `trap` (branch-to-response)
  - rust/op_570 / swift/op_258 -- **core equality, modes differ**
    - only on the left: `in0 - in1 overflows 32 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 - in1 overflows 32 bits (signed)` -> `trap` (branch-to-response)

### shared-core group zx64(Mul32(ex32@0(in0:64),ex32@0(in1:64))) · (i32,i32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `*` (i32,i32, 1 modes); cpp `*` (i32,i32, 1 modes); go `*` (i32,i32, 1 modes); rust `*` (i32,i32, 1 modes); swift `*` (i32,i32, 1 modes)

  - c/op_174 / cpp/op_174 -- **total equality**
  - c/op_174 / go/op_60 -- **total equality**
  - c/op_174 / rust/op_606 -- **total equality**
  - c/op_174 / swift/op_114 -- **core equality, modes differ**
    - only on the left: `in1 * in0 overflows 32 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in1 * in0 overflows 32 bits (signed)` -> `trap` (branch-to-response)
  - cpp/op_174 / go/op_60 -- **total equality**
  - cpp/op_174 / rust/op_606 -- **total equality**
  - cpp/op_174 / swift/op_114 -- **core equality, modes differ**
    - only on the left: `in1 * in0 overflows 32 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in1 * in0 overflows 32 bits (signed)` -> `trap` (branch-to-response)
  - go/op_60 / rust/op_606 -- **total equality**
  - go/op_60 / swift/op_114 -- **core equality, modes differ**
    - only on the left: `in1 * in0 overflows 32 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in1 * in0 overflows 32 bits (signed)` -> `trap` (branch-to-response)
  - rust/op_606 / swift/op_114 -- **core equality, modes differ**
    - only on the left: `in1 * in0 overflows 32 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in1 * in0 overflows 32 bits (signed)` -> `trap` (branch-to-response)

### shared-core group zx64(Xor32(ex32@0(in0:64),ex32@0(in1:64))) · (i32,i32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `^` (i32,i32, 0 modes); cpp `^` (i32,i32, 0 modes); cpp `xor` (i32,i32, 0 modes); go `^` (i32,i32, 0 modes); rust `^` (i32,i32, 0 modes); swift `^` (i32,i32, 0 modes)

  - c/op_390 / cpp/op_390 -- **total equality**
  - c/op_390 / cpp/op_894 -- **total equality**
  - c/op_390 / go/op_420 -- **total equality**
  - c/op_390 / rust/op_210 -- **total equality**
  - c/op_390 / swift/op_654 -- **total equality**
  - cpp/op_390 / go/op_420 -- **total equality**
  - cpp/op_894 / go/op_420 -- **total equality**
  - cpp/op_390 / rust/op_210 -- **total equality**
  - cpp/op_894 / rust/op_210 -- **total equality**
  - cpp/op_390 / swift/op_654 -- **total equality**
  - cpp/op_894 / swift/op_654 -- **total equality**
  - go/op_420 / rust/op_210 -- **total equality**
  - go/op_420 / swift/op_654 -- **total equality**
  - rust/op_210 / swift/op_654 -- **total equality**

### shared-core group zx64(And32(ex32@0(in0:64),ex32@0(in1:64))) · (i32,i32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `&` (i32,i32, 0 modes); cpp `&` (i32,i32, 0 modes); cpp `bitand` (i32,i32, 0 modes); go `&` (i32,i32, 0 modes); rust `&` (i32,i32, 0 modes); swift `&` (i32,i32, 0 modes)

  - c/op_426 / cpp/op_426 -- **total equality**
  - c/op_426 / cpp/op_930 -- **total equality**
  - c/op_426 / go/op_240 -- **total equality**
  - c/op_426 / rust/op_138 -- **total equality**
  - c/op_426 / swift/op_582 -- **total equality**
  - cpp/op_426 / go/op_240 -- **total equality**
  - cpp/op_930 / go/op_240 -- **total equality**
  - cpp/op_426 / rust/op_138 -- **total equality**
  - cpp/op_930 / rust/op_138 -- **total equality**
  - cpp/op_426 / swift/op_582 -- **total equality**
  - cpp/op_930 / swift/op_582 -- **total equality**
  - go/op_240 / rust/op_138 -- **total equality**
  - go/op_240 / swift/op_582 -- **total equality**
  - rust/op_138 / swift/op_582 -- **total equality**

### shared-core group zx64(Or32(ex32@0(in0:64),ex32@0(in1:64))) · (i32,i32)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `||` (i32,i32, 0 modes); c `|` (i32,i32, 0 modes); cpp `||` (i32,i32, 0 modes); cpp `|` (i32,i32, 0 modes); cpp `or` (i32,i32, 0 modes); cpp `bitor` (i32,i32, 0 modes); go `|` (i32,i32, 0 modes); rust `|` (i32,i32, 0 modes); swift `|` (i32,i32, 0 modes)

  - c/op_282 / cpp/op_282 -- **core difference**
  - c/op_282 / cpp/op_354 -- **core difference**
  - c/op_282 / cpp/op_786 -- **core difference**
  - c/op_282 / cpp/op_858 -- **core difference**
  - c/op_354 / cpp/op_282 -- **core difference**
  - c/op_354 / cpp/op_354 -- **total equality**
  - c/op_354 / cpp/op_786 -- **core difference**
  - c/op_354 / cpp/op_858 -- **total equality**
  - c/op_282 / go/op_384 -- **core difference**
  - c/op_354 / go/op_384 -- **total equality**
  - c/op_282 / rust/op_174 -- **core difference**
  - c/op_354 / rust/op_174 -- **total equality**
  - c/op_282 / swift/op_618 -- **core difference**
  - c/op_354 / swift/op_618 -- **total equality**
  - cpp/op_282 / go/op_384 -- **core difference**
  - cpp/op_354 / go/op_384 -- **total equality**
  - cpp/op_786 / go/op_384 -- **core difference**
  - cpp/op_858 / go/op_384 -- **total equality**
  - cpp/op_282 / rust/op_174 -- **core difference**
  - cpp/op_354 / rust/op_174 -- **total equality**
  - cpp/op_786 / rust/op_174 -- **core difference**
  - cpp/op_858 / rust/op_174 -- **total equality**
  - cpp/op_282 / swift/op_618 -- **core difference**
  - cpp/op_354 / swift/op_618 -- **total equality**
  - cpp/op_786 / swift/op_618 -- **core difference**
  - cpp/op_858 / swift/op_618 -- **total equality**
  - go/op_384 / rust/op_174 -- **total equality**
  - go/op_384 / swift/op_618 -- **total equality**
  - rust/op_174 / swift/op_618 -- **total equality**

### shared-core group zx64(Not32(ex32@0(in1:64))) · (i32,i32)

- ground: connection
- languages: go, rust
- members: go `&^` (i32,i32, 0 modes); rust `/` (i32,i32, 2 modes); rust `%` (i32,i32, 2 modes)

  - go/op_276 / rust/op_642 -- **core difference**
    - only on the right: `((-2147483648 + in0) | ~in1) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
  - go/op_276 / rust/op_678 -- **core difference**
    - only on the right: `((-2147483648 + in0) | ~in1) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)

### shared-core group And8(31:8,ex8@0(in1:64)) · (i32,i32)

- ground: connection
- languages: c, cpp, go, rust
- members: c `<<` (i32,i32, 0 modes); c `>>` (i32,i32, 0 modes); cpp `<<` (i32,i32, 0 modes); cpp `>>` (i32,i32, 0 modes); go `<<` (i32,i32, 1 modes); rust `<<` (i32,i32, 0 modes); rust `>>` (i32,i32, 0 modes)

  - c/op_678 / cpp/op_678 -- **total equality**
  - c/op_678 / cpp/op_714 -- **core difference**
  - c/op_714 / cpp/op_678 -- **core difference**
  - c/op_714 / cpp/op_714 -- **total equality**
  - c/op_678 / go/op_168 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_714 / go/op_168 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_678 / rust/op_462 -- **total equality**
  - c/op_678 / rust/op_498 -- **core difference**
  - c/op_714 / rust/op_462 -- **core difference**
  - c/op_714 / rust/op_498 -- **total equality**
  - cpp/op_678 / go/op_168 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_714 / go/op_168 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_678 / rust/op_462 -- **total equality**
  - cpp/op_678 / rust/op_498 -- **core difference**
  - cpp/op_714 / rust/op_462 -- **core difference**
  - cpp/op_714 / rust/op_498 -- **total equality**
  - go/op_168 / rust/op_462 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - go/op_168 / rust/op_498 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)

### shared-core group And8(zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (i32,i64)

- ground: connection
- languages: c, cpp
- members: c `&&` (i32,i64, 0 modes); cpp `&&` (i32,i64, 0 modes); cpp `and` (i32,i64, 0 modes)

  - c/op_319 / cpp/op_319 -- **core difference**
  - c/op_319 / cpp/op_823 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (i32,i64)

- ground: connection
- languages: c, cpp
- members: c `||` (i32,i64, 0 modes); cpp `||` (i32,i64, 0 modes); cpp `or` (i32,i64, 0 modes)

  - c/op_283 / cpp/op_283 -- **core difference**
  - c/op_283 / cpp/op_787 -- **core difference**

### shared-core group ex64@64(DivModS128to64(64HLto128(Sar64(sx64(ex32@0(in0:64)),63:8),sx64(ex32@0(in0:64))),in1:64)) · (i32,i64)

- ground: connection
- languages: c, cpp
- members: c `/` (i32,i64, 0 modes); c `%` (i32,i64, 0 modes); cpp `/` (i32,i64, 0 modes); cpp `%` (i32,i64, 0 modes)

  - c/op_211 / cpp/op_211 -- **total equality**
  - c/op_211 / cpp/op_247 -- **core difference**
  - c/op_247 / cpp/op_211 -- **core difference**
  - c/op_247 / cpp/op_247 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(12:64,8:64,in1:64,sx64(ex32@0(in0:64)),u0:64))) · (i32,i64)

- ground: connection
- languages: c, cpp
- members: c `>` (i32,i64, 1 modes); cpp `>` (i32,i64, 1 modes)

  - c/op_535 / cpp/op_535 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(14:64,8:64,in1:64,sx64(ex32@0(in0:64)),u0:64))) · (i32,i64)

- ground: connection
- languages: c, cpp
- members: c `>=` (i32,i64, 1 modes); cpp `>=` (i32,i64, 1 modes)

  - c/op_571 / cpp/op_571 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(13:64,8:64,in1:64,sx64(ex32@0(in0:64)),u0:64))) · (i32,i64)

- ground: connection
- languages: c, cpp
- members: c `<=` (i32,i64, 1 modes); cpp `<=` (i32,i64, 1 modes)

  - c/op_607 / cpp/op_607 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(15:64,8:64,in1:64,sx64(ex32@0(in0:64)),u0:64))) · (i32,i64)

- ground: connection
- languages: c, cpp
- members: c `<` (i32,i64, 1 modes); cpp `<` (i32,i64, 1 modes)

  - c/op_643 / cpp/op_643 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(12:64,8:64,sx64(ex32@0(in0:64)),in1:64,u0:64))) · (i32,i64)

- ground: connection
- languages: cpp, swift
- members: cpp `<=>` (i32,i64, 0 modes); swift `<` (i32,i64, 0 modes)

  - cpp/op_751 / swift/op_295 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(15:64,8:64,sx64(ex32@0(in0:64)),in1:64,u0:64))) · (i32,i64)

- ground: connection
- languages: cpp, swift
- members: cpp `<=>` (i32,i64, 0 modes); swift `>` (i32,i64, 0 modes)

  - cpp/op_751 / swift/op_331 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(4:64,8:64,in1:64,sx64(ex32@0(in0:64)),u0:64))) · (i32,i64)

- ground: connection
- languages: c, cpp
- members: c `==` (i32,i64, 1 modes); cpp `==` (i32,i64, 1 modes)

  - c/op_463 / cpp/op_463 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,8:64,in1:64,sx64(ex32@0(in0:64)),u0:64))) · (i32,i64)

- ground: connection
- languages: c, cpp
- members: c `!=` (i32,i64, 2 modes); cpp `!=` (i32,i64, 1 modes); cpp `not_eq` (i32,i64, 1 modes)

  - c/op_499 / cpp/op_499 -- **core difference**
  - c/op_499 / cpp/op_967 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64))) · (i32,i64)

- ground: connection
- languages: c, cpp
- members: c `||` (i32,i64, 0 modes); c `&&` (i32,i64, 0 modes); cpp `||` (i32,i64, 0 modes); cpp `&&` (i32,i64, 0 modes); cpp `or` (i32,i64, 0 modes); cpp `and` (i32,i64, 0 modes)

  - c/op_283 / cpp/op_283 -- **core difference**
  - c/op_283 / cpp/op_319 -- **core difference**
  - c/op_283 / cpp/op_787 -- **core difference**
  - c/op_283 / cpp/op_823 -- **core difference**
  - c/op_319 / cpp/op_283 -- **core difference**
  - c/op_319 / cpp/op_319 -- **core difference**
  - c/op_319 / cpp/op_787 -- **core difference**
  - c/op_319 / cpp/op_823 -- **core difference**

### shared-core group zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) · (i32,i64)

- ground: connection
- languages: c, cpp, rust
- members: c `<<` (i32,i64, 0 modes); cpp `<<` (i32,i64, 0 modes); rust `<<` (i32,i64, 0 modes)

  - c/op_679 / cpp/op_679 -- **total equality**
  - c/op_679 / rust/op_463 -- **total equality**
  - cpp/op_679 / rust/op_463 -- **total equality**

### shared-core group zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) · (i32,i64)

- ground: connection
- languages: c, cpp, rust
- members: c `>>` (i32,i64, 0 modes); cpp `>>` (i32,i64, 0 modes); rust `>>` (i32,i64, 0 modes)

  - c/op_715 / cpp/op_715 -- **total equality**
  - c/op_715 / rust/op_499 -- **total equality**
  - cpp/op_715 / rust/op_499 -- **total equality**

### shared-core group ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))) · (i32,i64)

- ground: connection
- languages: c, cpp, go, rust
- members: c `<<` (i32,i64, 0 modes); cpp `<<` (i32,i64, 0 modes); go `<<` (i32,i64, 1 modes); rust `<<` (i32,i64, 0 modes)

  - c/op_679 / cpp/op_679 -- **total equality**
  - c/op_679 / go/op_169 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_679 / rust/op_463 -- **total equality**
  - cpp/op_679 / go/op_169 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_679 / rust/op_463 -- **total equality**
  - go/op_169 / rust/op_463 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)

### shared-core group Add64(in1:64,sx64(ex32@0(in0:64))) · (i32,i64)

- ground: connection
- languages: c, cpp
- members: c `+` (i32,i64, 0 modes); cpp `+` (i32,i64, 0 modes)

  - c/op_103 / cpp/op_103 -- **total equality**

### shared-core group Sub64(sx64(ex32@0(in0:64)),in1:64) · (i32,i64)

- ground: connection
- languages: c, cpp
- members: c `-` (i32,i64, 0 modes); cpp `-` (i32,i64, 0 modes)

  - c/op_139 / cpp/op_139 -- **total equality**

### shared-core group Mul64(in1:64,sx64(ex32@0(in0:64))) · (i32,i64)

- ground: connection
- languages: c, cpp
- members: c `*` (i32,i64, 0 modes); cpp `*` (i32,i64, 0 modes)

  - c/op_175 / cpp/op_175 -- **total equality**

### shared-core group Xor64(in1:64,sx64(ex32@0(in0:64))) · (i32,i64)

- ground: connection
- languages: c, cpp
- members: c `^` (i32,i64, 0 modes); cpp `^` (i32,i64, 0 modes); cpp `xor` (i32,i64, 0 modes)

  - c/op_391 / cpp/op_391 -- **total equality**
  - c/op_391 / cpp/op_895 -- **total equality**

### shared-core group And64(in1:64,sx64(ex32@0(in0:64))) · (i32,i64)

- ground: connection
- languages: c, cpp
- members: c `&` (i32,i64, 0 modes); cpp `&` (i32,i64, 0 modes); cpp `bitand` (i32,i64, 0 modes)

  - c/op_427 / cpp/op_427 -- **total equality**
  - c/op_427 / cpp/op_931 -- **total equality**

### shared-core group Or64(in1:64,sx64(ex32@0(in0:64))) · (i32,i64)

- ground: connection
- languages: c, cpp
- members: c `|` (i32,i64, 0 modes); cpp `|` (i32,i64, 0 modes); cpp `bitor` (i32,i64, 0 modes)

  - c/op_355 / cpp/op_355 -- **total equality**
  - c/op_355 / cpp/op_859 -- **total equality**

### shared-core group And8(31:8,ex8@0(in1:64)) · (i32,i64)

- ground: connection
- languages: c, cpp, go, rust
- members: c `<<` (i32,i64, 0 modes); c `>>` (i32,i64, 0 modes); cpp `<<` (i32,i64, 0 modes); cpp `>>` (i32,i64, 0 modes); go `<<` (i32,i64, 1 modes); rust `<<` (i32,i64, 0 modes); rust `>>` (i32,i64, 0 modes)

  - c/op_679 / cpp/op_679 -- **total equality**
  - c/op_679 / cpp/op_715 -- **core difference**
  - c/op_715 / cpp/op_679 -- **core difference**
  - c/op_715 / cpp/op_715 -- **total equality**
  - c/op_679 / go/op_169 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_715 / go/op_169 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_679 / rust/op_463 -- **total equality**
  - c/op_679 / rust/op_499 -- **core difference**
  - c/op_715 / rust/op_463 -- **core difference**
  - c/op_715 / rust/op_499 -- **total equality**
  - cpp/op_679 / go/op_169 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_715 / go/op_169 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_679 / rust/op_463 -- **total equality**
  - cpp/op_679 / rust/op_499 -- **core difference**
  - cpp/op_715 / rust/op_463 -- **core difference**
  - cpp/op_715 / rust/op_499 -- **total equality**
  - go/op_169 / rust/op_463 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - go/op_169 / rust/op_499 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)

### shared-core group And8(zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (i32,u64)

- ground: connection
- languages: c, cpp
- members: c `&&` (i32,u64, 0 modes); cpp `&&` (i32,u64, 0 modes); cpp `and` (i32,u64, 0 modes)

  - c/op_320 / cpp/op_320 -- **core difference**
  - c/op_320 / cpp/op_824 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (i32,u64)

- ground: connection
- languages: c, cpp
- members: c `||` (i32,u64, 0 modes); cpp `||` (i32,u64, 0 modes); cpp `or` (i32,u64, 0 modes)

  - c/op_284 / cpp/op_284 -- **core difference**
  - c/op_284 / cpp/op_788 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(4:64,8:64,in1:64,sx64(ex32@0(in0:64)),u0:64))) · (i32,u64)

- ground: connection
- languages: c, cpp
- members: c `==` (i32,u64, 1 modes); cpp `==` (i32,u64, 1 modes)

  - c/op_464 / cpp/op_464 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,8:64,in1:64,sx64(ex32@0(in0:64)),u0:64))) · (i32,u64)

- ground: connection
- languages: c, cpp
- members: c `!=` (i32,u64, 2 modes); cpp `!=` (i32,u64, 1 modes); cpp `not_eq` (i32,u64, 1 modes)

  - c/op_500 / cpp/op_500 -- **core difference**
  - c/op_500 / cpp/op_968 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(2:64,8:64,in1:64,sx64(ex32@0(in0:64)),u0:64))) · (i32,u64)

- ground: connection
- languages: c, cpp
- members: c `>` (i32,u64, 1 modes); cpp `>` (i32,u64, 1 modes)

  - c/op_536 / cpp/op_536 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(6:64,8:64,in1:64,sx64(ex32@0(in0:64)),u0:64))) · (i32,u64)

- ground: connection
- languages: c, cpp
- members: c `>=` (i32,u64, 1 modes); cpp `>=` (i32,u64, 1 modes)

  - c/op_572 / cpp/op_572 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,8:64,in1:64,sx64(ex32@0(in0:64)),u0:64))) · (i32,u64)

- ground: connection
- languages: c, cpp
- members: c `<=` (i32,u64, 1 modes); cpp `<=` (i32,u64, 1 modes)

  - c/op_608 / cpp/op_608 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,8:64,in1:64,sx64(ex32@0(in0:64)),u0:64))) · (i32,u64)

- ground: connection
- languages: c, cpp
- members: c `<` (i32,u64, 1 modes); cpp `<` (i32,u64, 1 modes)

  - c/op_644 / cpp/op_644 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64))) · (i32,u64)

- ground: connection
- languages: c, cpp
- members: c `||` (i32,u64, 0 modes); c `&&` (i32,u64, 0 modes); cpp `||` (i32,u64, 0 modes); cpp `&&` (i32,u64, 0 modes); cpp `or` (i32,u64, 0 modes); cpp `and` (i32,u64, 0 modes)

  - c/op_284 / cpp/op_284 -- **core difference**
  - c/op_284 / cpp/op_320 -- **core difference**
  - c/op_284 / cpp/op_788 -- **core difference**
  - c/op_284 / cpp/op_824 -- **core difference**
  - c/op_320 / cpp/op_284 -- **core difference**
  - c/op_320 / cpp/op_320 -- **core difference**
  - c/op_320 / cpp/op_788 -- **core difference**
  - c/op_320 / cpp/op_824 -- **core difference**

### shared-core group ex64@64(DivModU128to64(64HLto128(0:64,sx64(ex32@0(in0:64))),in1:64)) · (i32,u64)

- ground: connection
- languages: c, cpp
- members: c `/` (i32,u64, 0 modes); c `%` (i32,u64, 0 modes); cpp `/` (i32,u64, 0 modes); cpp `%` (i32,u64, 0 modes)

  - c/op_212 / cpp/op_212 -- **total equality**
  - c/op_212 / cpp/op_248 -- **core difference**
  - c/op_248 / cpp/op_212 -- **core difference**
  - c/op_248 / cpp/op_248 -- **total equality**

### shared-core group zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) · (i32,u64)

- ground: connection
- languages: c, cpp, rust
- members: c `<<` (i32,u64, 1 modes); cpp `<<` (i32,u64, 1 modes); rust `<<` (i32,u64, 1 modes)

  - c/op_680 / cpp/op_680 -- **total equality**
  - c/op_680 / rust/op_464 -- **total equality**
  - cpp/op_680 / rust/op_464 -- **total equality**

### shared-core group zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))) · (i32,u64)

- ground: connection
- languages: c, cpp, rust
- members: c `>>` (i32,u64, 0 modes); cpp `>>` (i32,u64, 0 modes); rust `>>` (i32,u64, 0 modes)

  - c/op_716 / cpp/op_716 -- **total equality**
  - c/op_716 / rust/op_500 -- **total equality**
  - cpp/op_716 / rust/op_500 -- **total equality**

### shared-core group ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))) · (i32,u64)

- ground: connection
- languages: c, cpp, go, rust
- members: c `<<` (i32,u64, 1 modes); cpp `<<` (i32,u64, 1 modes); go `<<` (i32,u64, 3 modes); rust `<<` (i32,u64, 1 modes)

  - c/op_680 / cpp/op_680 -- **total equality**
  - c/op_680 / go/op_170 -- **core difference**
    - only on the left: `in1 >= 32 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 32 (unsigned)` -> `clamp-continue` (solver-localized)
  - c/op_680 / rust/op_464 -- **total equality**
  - cpp/op_680 / go/op_170 -- **core difference**
    - only on the left: `in1 >= 32 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 32 (unsigned)` -> `clamp-continue` (solver-localized)
  - cpp/op_680 / rust/op_464 -- **total equality**
  - go/op_170 / rust/op_464 -- **core difference**
    - only on the left: `in1 >= 32 (unsigned)` -> `clamp-continue` (solver-localized)
    - only on the right: `in1 >= 32 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)

### shared-core group Add64(in1:64,sx64(ex32@0(in0:64))) · (i32,u64)

- ground: connection
- languages: c, cpp
- members: c `+` (i32,u64, 0 modes); cpp `+` (i32,u64, 0 modes)

  - c/op_104 / cpp/op_104 -- **total equality**

### shared-core group Sub64(sx64(ex32@0(in0:64)),in1:64) · (i32,u64)

- ground: connection
- languages: c, cpp
- members: c `-` (i32,u64, 0 modes); cpp `-` (i32,u64, 0 modes)

  - c/op_140 / cpp/op_140 -- **total equality**

### shared-core group Mul64(in1:64,sx64(ex32@0(in0:64))) · (i32,u64)

- ground: connection
- languages: c, cpp
- members: c `*` (i32,u64, 0 modes); cpp `*` (i32,u64, 0 modes)

  - c/op_176 / cpp/op_176 -- **total equality**

### shared-core group Xor64(in1:64,sx64(ex32@0(in0:64))) · (i32,u64)

- ground: connection
- languages: c, cpp
- members: c `^` (i32,u64, 0 modes); cpp `^` (i32,u64, 0 modes); cpp `xor` (i32,u64, 0 modes)

  - c/op_392 / cpp/op_392 -- **total equality**
  - c/op_392 / cpp/op_896 -- **total equality**

### shared-core group And64(in1:64,sx64(ex32@0(in0:64))) · (i32,u64)

- ground: connection
- languages: c, cpp
- members: c `&` (i32,u64, 0 modes); cpp `&` (i32,u64, 0 modes); cpp `bitand` (i32,u64, 0 modes)

  - c/op_428 / cpp/op_428 -- **total equality**
  - c/op_428 / cpp/op_932 -- **total equality**

### shared-core group Or64(in1:64,sx64(ex32@0(in0:64))) · (i32,u64)

- ground: connection
- languages: c, cpp
- members: c `|` (i32,u64, 0 modes); cpp `|` (i32,u64, 0 modes); cpp `bitor` (i32,u64, 0 modes)

  - c/op_356 / cpp/op_356 -- **total equality**
  - c/op_356 / cpp/op_860 -- **total equality**

### shared-core group And8(31:8,ex8@0(in1:64)) · (i32,u64)

- ground: connection
- languages: c, cpp, go, rust
- members: c `<<` (i32,u64, 1 modes); c `>>` (i32,u64, 0 modes); cpp `<<` (i32,u64, 1 modes); cpp `>>` (i32,u64, 0 modes); go `<<` (i32,u64, 3 modes); rust `<<` (i32,u64, 1 modes); rust `>>` (i32,u64, 0 modes)

  - c/op_680 / cpp/op_680 -- **total equality**
  - c/op_680 / cpp/op_716 -- **core difference**
    - only on the left: `in1 >= 32 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_716 / cpp/op_680 -- **core difference**
    - only on the right: `in1 >= 32 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_716 / cpp/op_716 -- **total equality**
  - c/op_680 / go/op_170 -- **core difference**
    - only on the left: `in1 >= 32 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 32 (unsigned)` -> `clamp-continue` (solver-localized)
  - c/op_716 / go/op_170 -- **core difference**
    - only on the right: `in1 >= 32 (unsigned)` -> `clamp-continue` (solver-localized)
  - c/op_680 / rust/op_464 -- **total equality**
  - c/op_680 / rust/op_500 -- **core difference**
    - only on the left: `in1 >= 32 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_716 / rust/op_464 -- **core difference**
    - only on the right: `in1 >= 32 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_716 / rust/op_500 -- **total equality**
  - cpp/op_680 / go/op_170 -- **core difference**
    - only on the left: `in1 >= 32 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 32 (unsigned)` -> `clamp-continue` (solver-localized)
  - cpp/op_716 / go/op_170 -- **core difference**
    - only on the right: `in1 >= 32 (unsigned)` -> `clamp-continue` (solver-localized)
  - cpp/op_680 / rust/op_464 -- **total equality**
  - cpp/op_680 / rust/op_500 -- **core difference**
    - only on the left: `in1 >= 32 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - cpp/op_716 / rust/op_464 -- **core difference**
    - only on the right: `in1 >= 32 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - cpp/op_716 / rust/op_500 -- **total equality**
  - go/op_170 / rust/op_464 -- **core difference**
    - only on the left: `in1 >= 32 (unsigned)` -> `clamp-continue` (solver-localized)
    - only on the right: `in1 >= 32 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - go/op_170 / rust/op_500 -- **core difference**
    - only on the left: `in1 >= 32 (unsigned)` -> `clamp-continue` (solver-localized)

### shared-core group zx8(ex1@0(amd64g_calculate_condition(4:64,20:64,in0:64,0:64,u0:64))) · (i64,None)

- ground: connection
- languages: c, cpp
- members: c `!` (i64,None, 0 modes); cpp `!` (i64,None, 0 modes); cpp `not` (i64,None, 0 modes)

  - c/op_1 / cpp/op_1 -- **core difference**
  - c/op_1 / cpp/op_25 -- **core difference**

### shared-core group st64(Add64(18446744073709551608:64,SP:64))=in0:64 · (i64,None)

- ground: connection
- languages: c, cpp
- members: c `&` (i64,None, 0 modes); cpp `&` (i64,None, 0 modes)

  - c/op_31 / cpp/op_43 -- **total equality**

### shared-core group Add64(18446744073709551615:64,in0:64) · (i64,None)

- ground: connection
- languages: c, cpp
- members: c `--` (i64,None, 0 modes); cpp `--` (i64,None, 0 modes)

  - c/op_43 / cpp/op_55 -- **total equality**

### shared-core group Sub64(0:64,in0:64) · (i64,None)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `-` (i64,None, 1 modes); cpp `-` (i64,None, 1 modes); go `-` (i64,None, 1 modes); rust `-` (i64,None, 1 modes); swift `-` (i64,None, 1 modes)

  - c/op_13 / cpp/op_13 -- **total equality**
  - c/op_13 / go/op_7 -- **total equality**
  - c/op_13 / rust/op_1 -- **total equality**
  - c/op_13 / swift/op_13 -- **core equality, modes differ**
    - only on the left: `0 - in0 overflows 64 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `0 - in0 overflows 64 bits (signed)` -> `trap` (branch-to-response)
  - cpp/op_13 / go/op_7 -- **total equality**
  - cpp/op_13 / rust/op_1 -- **total equality**
  - cpp/op_13 / swift/op_13 -- **core equality, modes differ**
    - only on the left: `0 - in0 overflows 64 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `0 - in0 overflows 64 bits (signed)` -> `trap` (branch-to-response)
  - go/op_7 / rust/op_1 -- **total equality**
  - go/op_7 / swift/op_13 -- **core equality, modes differ**
    - only on the left: `0 - in0 overflows 64 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `0 - in0 overflows 64 bits (signed)` -> `trap` (branch-to-response)
  - rust/op_1 / swift/op_13 -- **core equality, modes differ**
    - only on the left: `0 - in0 overflows 64 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `0 - in0 overflows 64 bits (signed)` -> `trap` (branch-to-response)

### shared-core group Add64(1:64,in0:64) · (i64,None)

- ground: connection
- languages: c, cpp
- members: c `++` (i64,None, 0 modes); cpp `++` (i64,None, 0 modes)

  - c/op_37 / cpp/op_49 -- **total equality**

### shared-core group Not64(in0:64) · (i64,None)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `~` (i64,None, 0 modes); cpp `compl` (i64,None, 0 modes); cpp `~` (i64,None, 0 modes); go `^` (i64,None, 0 modes); rust `!` (i64,None, 0 modes); swift `~` (i64,None, 0 modes)

  - c/op_7 / cpp/op_31 -- **total equality**
  - c/op_7 / cpp/op_7 -- **total equality**
  - c/op_7 / go/op_19 -- **total equality**
  - c/op_7 / rust/op_13 -- **total equality**
  - c/op_7 / swift/op_37 -- **total equality**
  - cpp/op_31 / go/op_19 -- **total equality**
  - cpp/op_7 / go/op_19 -- **total equality**
  - cpp/op_31 / rust/op_13 -- **total equality**
  - cpp/op_7 / rust/op_13 -- **total equality**
  - cpp/op_31 / swift/op_37 -- **total equality**
  - cpp/op_7 / swift/op_37 -- **total equality**
  - go/op_19 / rust/op_13 -- **total equality**
  - go/op_19 / swift/op_37 -- **total equality**
  - rust/op_13 / swift/op_37 -- **total equality**

### shared-core group ite(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64)),in0:64,0:64) · (i64,bool)

- ground: connection
- languages: c, cpp
- members: c `*` (i64,bool, 0 modes); cpp `*` (i64,bool, 0 modes)

  - c/op_185 / cpp/op_185 -- **total equality**

### shared-core group And8(ex8@0(in1:64),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64)))) · (i64,bool)

- ground: connection
- languages: c, cpp
- members: c `&&` (i64,bool, 0 modes); cpp `&&` (i64,bool, 0 modes); cpp `and` (i64,bool, 0 modes)

  - c/op_329 / cpp/op_329 -- **core difference**
  - c/op_329 / cpp/op_833 -- **core difference**

### shared-core group Or8(ex8@0(in1:64),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64)))) · (i64,bool)

- ground: connection
- languages: c, cpp
- members: c `||` (i64,bool, 0 modes); cpp `||` (i64,bool, 0 modes); cpp `or` (i64,bool, 0 modes)

  - c/op_293 / cpp/op_293 -- **core difference**
  - c/op_293 / cpp/op_797 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(15:64,8:64,in0:64,zx64(ex32@0(in1:64)),u0:64))) · (i64,bool)

- ground: connection
- languages: c, cpp
- members: c `>` (i64,bool, 1 modes); cpp `>` (i64,bool, 1 modes)

  - c/op_545 / cpp/op_545 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(13:64,8:64,in0:64,zx64(ex32@0(in1:64)),u0:64))) · (i64,bool)

- ground: connection
- languages: c, cpp
- members: c `>=` (i64,bool, 1 modes); cpp `>=` (i64,bool, 1 modes)

  - c/op_581 / cpp/op_581 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(14:64,8:64,in0:64,zx64(ex32@0(in1:64)),u0:64))) · (i64,bool)

- ground: connection
- languages: c, cpp
- members: c `<=` (i64,bool, 1 modes); cpp `<=` (i64,bool, 1 modes)

  - c/op_617 / cpp/op_617 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(12:64,8:64,in0:64,zx64(ex32@0(in1:64)),u0:64))) · (i64,bool)

- ground: connection
- languages: c, cpp
- members: c `<` (i64,bool, 1 modes); cpp `<` (i64,bool, 1 modes)

  - c/op_653 / cpp/op_653 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(4:64,8:64,in0:64,zx64(ex32@0(in1:64)),u0:64))) · (i64,bool)

- ground: connection
- languages: c, cpp
- members: c `==` (i64,bool, 1 modes); cpp `==` (i64,bool, 1 modes)

  - c/op_473 / cpp/op_473 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,8:64,in0:64,zx64(ex32@0(in1:64)),u0:64))) · (i64,bool)

- ground: connection
- languages: c, cpp
- members: c `!=` (i64,bool, 2 modes); cpp `!=` (i64,bool, 1 modes); cpp `not_eq` (i64,bool, 1 modes)

  - c/op_509 / cpp/op_509 -- **core difference**
  - c/op_509 / cpp/op_977 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64))) · (i64,bool)

- ground: connection
- languages: c, cpp
- members: c `||` (i64,bool, 0 modes); c `&&` (i64,bool, 0 modes); cpp `||` (i64,bool, 0 modes); cpp `&&` (i64,bool, 0 modes); cpp `or` (i64,bool, 0 modes); cpp `and` (i64,bool, 0 modes)

  - c/op_293 / cpp/op_293 -- **core difference**
  - c/op_293 / cpp/op_329 -- **core difference**
  - c/op_293 / cpp/op_797 -- **core difference**
  - c/op_293 / cpp/op_833 -- **core difference**
  - c/op_329 / cpp/op_293 -- **core difference**
  - c/op_329 / cpp/op_329 -- **core difference**
  - c/op_329 / cpp/op_797 -- **core difference**
  - c/op_329 / cpp/op_833 -- **core difference**

### shared-core group zx64(And32(ex32@0(in0:64),ex32@0(in1:64))) · (i64,bool)

- ground: connection
- languages: c, cpp
- members: c `&` (i64,bool, 0 modes); cpp `&` (i64,bool, 0 modes); cpp `bitand` (i64,bool, 0 modes)

  - c/op_437 / cpp/op_437 -- **total equality**
  - c/op_437 / cpp/op_941 -- **total equality**

### shared-core group Shl64(in0:64,And8(63:8,ex8@0(in1:64))) · (i64,bool)

- ground: connection
- languages: c, cpp
- members: c `<<` (i64,bool, 0 modes); cpp `<<` (i64,bool, 0 modes)

  - c/op_689 / cpp/op_689 -- **total equality**

### shared-core group Sar64(in0:64,And8(63:8,ex8@0(in1:64))) · (i64,bool)

- ground: connection
- languages: c, cpp
- members: c `>>` (i64,bool, 0 modes); cpp `>>` (i64,bool, 0 modes)

  - c/op_725 / cpp/op_725 -- **total equality**

### shared-core group Add64(in0:64,zx64(ex32@0(in1:64))) · (i64,bool)

- ground: connection
- languages: c, cpp
- members: c `+` (i64,bool, 0 modes); cpp `+` (i64,bool, 0 modes)

  - c/op_113 / cpp/op_113 -- **total equality**

### shared-core group Sub64(in0:64,zx64(ex32@0(in1:64))) · (i64,bool)

- ground: connection
- languages: c, cpp
- members: c `-` (i64,bool, 0 modes); cpp `-` (i64,bool, 0 modes)

  - c/op_149 / cpp/op_149 -- **total equality**

### shared-core group Xor64(in0:64,zx64(ex32@0(in1:64))) · (i64,bool)

- ground: connection
- languages: c, cpp
- members: c `^` (i64,bool, 0 modes); cpp `^` (i64,bool, 0 modes); cpp `xor` (i64,bool, 0 modes)

  - c/op_401 / cpp/op_401 -- **total equality**
  - c/op_401 / cpp/op_905 -- **total equality**

### shared-core group Or64(in0:64,zx64(ex32@0(in1:64))) · (i64,bool)

- ground: connection
- languages: c, cpp
- members: c `|` (i64,bool, 0 modes); cpp `|` (i64,bool, 0 modes); cpp `bitor` (i64,bool, 0 modes)

  - c/op_365 / cpp/op_365 -- **total equality**
  - c/op_365 / cpp/op_869 -- **total equality**

### shared-core group And8(63:8,ex8@0(in1:64)) · (i64,bool)

- ground: connection
- languages: c, cpp
- members: c `<<` (i64,bool, 0 modes); c `>>` (i64,bool, 0 modes); cpp `<<` (i64,bool, 0 modes); cpp `>>` (i64,bool, 0 modes)

  - c/op_689 / cpp/op_689 -- **total equality**
  - c/op_689 / cpp/op_725 -- **core difference**
  - c/op_725 / cpp/op_689 -- **core difference**
  - c/op_725 / cpp/op_725 -- **total equality**

### shared-core group And8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64)))) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `&&` (i64,f32, 0 modes); cpp `&&` (i64,f32, 0 modes); cpp `and` (i64,f32, 0 modes)

  - c/op_327 / cpp/op_327 -- **core difference**
  - c/op_327 / cpp/op_831 -- **core difference**

### shared-core group Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64)))) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `||` (i64,f32, 0 modes); cpp `||` (i64,f32, 0 modes); cpp `or` (i64,f32, 0 modes)

  - c/op_291 / cpp/op_291 -- **core difference**
  - c/op_291 / cpp/op_795 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64)))) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `||` (i64,f32, 0 modes); c `&&` (i64,f32, 0 modes); cpp `||` (i64,f32, 0 modes); cpp `&&` (i64,f32, 0 modes); cpp `or` (i64,f32, 0 modes); cpp `and` (i64,f32, 0 modes)

  - c/op_291 / cpp/op_291 -- **core difference**
  - c/op_291 / cpp/op_327 -- **core difference**
  - c/op_291 / cpp/op_795 -- **core difference**
  - c/op_291 / cpp/op_831 -- **core difference**
  - c/op_327 / cpp/op_291 -- **core difference**
  - c/op_327 / cpp/op_327 -- **core difference**
  - c/op_327 / cpp/op_795 -- **core difference**
  - c/op_327 / cpp/op_831 -- **core difference**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)))),ex128@0(in1:256)))))) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `==` (i64,f32, 0 modes); cpp `==` (i64,f32, 0 modes)

  - c/op_471 / cpp/op_471 -- **total equality**

### shared-core group ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),XorV128(4294967295:128,CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)))),ex128@0(in1:256)))) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `!=` (i64,f32, 0 modes); cpp `!=` (i64,f32, 0 modes); cpp `not_eq` (i64,f32, 0 modes)

  - c/op_507 / cpp/op_507 -- **total equality**
  - c/op_507 / cpp/op_975 -- **total equality**

### shared-core group ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),Sub32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)))),ex128@0(in1:256))) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `-` (i64,f32, 0 modes); cpp `-` (i64,f32, 0 modes)

  - c/op_147 / cpp/op_147 -- **total equality**

### shared-core group ins@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),Div32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)))),ex128@0(in1:256))) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `/` (i64,f32, 0 modes); cpp `/` (i64,f32, 0 modes)

  - c/op_219 / cpp/op_219 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I64StoF64(And32(3:32,ex32@0(u0:64)),in0:64))),F32toF64(ex32@0(in1:256))))),0:64,u1:64))) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `>` (i64,f32, 0 modes); cpp `>` (i64,f32, 0 modes)

  - c/op_543 / cpp/op_543 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I64StoF64(And32(3:32,ex32@0(u0:64)),in0:64))),F32toF64(ex32@0(in1:256))))),0:64,u1:64))) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `>=` (i64,f32, 0 modes); cpp `>=` (i64,f32, 0 modes)

  - c/op_579 / cpp/op_579 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I64StoF64(And32(3:32,ex32@0(u0:64)),in0:64)))))),0:64,u1:64))) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `<=` (i64,f32, 0 modes); cpp `<=` (i64,f32, 0 modes)

  - c/op_615 / cpp/op_615 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I64StoF64(And32(3:32,ex32@0(u0:64)),in0:64)))))),0:64,u1:64))) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `<` (i64,f32, 0 modes); cpp `<` (i64,f32, 0 modes)

  - c/op_651 / cpp/op_651 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I64StoF64(And32(3:32,ex32@0(u0:64)),in0:64))),F32toF64(ex32@0(in1:256))))) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `>` (i64,f32, 0 modes); c `>=` (i64,f32, 0 modes); cpp `>` (i64,f32, 0 modes); cpp `>=` (i64,f32, 0 modes); cpp `<=>` (i64,f32, 0 modes)

  - c/op_543 / cpp/op_543 -- **core difference**
  - c/op_543 / cpp/op_579 -- **core difference**
  - c/op_543 / cpp/op_759 -- **core difference**
  - c/op_579 / cpp/op_543 -- **core difference**
  - c/op_579 / cpp/op_579 -- **core difference**
  - c/op_579 / cpp/op_759 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I64StoF64(And32(3:32,ex32@0(u0:64)),in0:64)))))) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `<=` (i64,f32, 0 modes); c `<` (i64,f32, 0 modes); cpp `<=` (i64,f32, 0 modes); cpp `<` (i64,f32, 0 modes); cpp `<=>` (i64,f32, 0 modes)

  - c/op_615 / cpp/op_615 -- **core difference**
  - c/op_615 / cpp/op_651 -- **core difference**
  - c/op_615 / cpp/op_759 -- **core difference**
  - c/op_651 / cpp/op_615 -- **core difference**
  - c/op_651 / cpp/op_651 -- **core difference**
  - c/op_651 / cpp/op_759 -- **core difference**

### shared-core group CmpEQ32F0x4(ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)))),ex128@0(in1:256)) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `==` (i64,f32, 0 modes); c `!=` (i64,f32, 0 modes); cpp `==` (i64,f32, 0 modes); cpp `!=` (i64,f32, 0 modes); cpp `not_eq` (i64,f32, 0 modes)

  - c/op_471 / cpp/op_471 -- **total equality**
  - c/op_471 / cpp/op_507 -- **core difference**
  - c/op_471 / cpp/op_975 -- **core difference**
  - c/op_507 / cpp/op_471 -- **core difference**
  - c/op_507 / cpp/op_507 -- **total equality**
  - c/op_507 / cpp/op_975 -- **total equality**

### shared-core group Add32F0x4(ex128@0(in1:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))))) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `+` (i64,f32, 0 modes); cpp `+` (i64,f32, 0 modes)

  - c/op_111 / cpp/op_111 -- **total equality**

### shared-core group Mul32F0x4(ex128@0(in1:256),ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))))) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `*` (i64,f32, 0 modes); cpp `*` (i64,f32, 0 modes)

  - c/op_183 / cpp/op_183 -- **total equality**

### shared-core group ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)))) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `+` (i64,f32, 0 modes); c `-` (i64,f32, 0 modes); c `*` (i64,f32, 0 modes); c `/` (i64,f32, 0 modes); c `==` (i64,f32, 0 modes); c `!=` (i64,f32, 0 modes); cpp `+` (i64,f32, 0 modes); cpp `-` (i64,f32, 0 modes); cpp `*` (i64,f32, 0 modes); cpp `/` (i64,f32, 0 modes); cpp `==` (i64,f32, 0 modes); cpp `!=` (i64,f32, 0 modes); cpp `not_eq` (i64,f32, 0 modes)

  - c/op_111 / cpp/op_111 -- **total equality**
  - c/op_111 / cpp/op_147 -- **core difference**
  - c/op_111 / cpp/op_183 -- **core difference**
  - c/op_111 / cpp/op_219 -- **core difference**
  - c/op_111 / cpp/op_471 -- **core difference**
  - c/op_111 / cpp/op_507 -- **core difference**
  - c/op_111 / cpp/op_975 -- **core difference**
  - c/op_147 / cpp/op_111 -- **core difference**
  - c/op_147 / cpp/op_147 -- **total equality**
  - c/op_147 / cpp/op_183 -- **core difference**
  - c/op_147 / cpp/op_219 -- **core difference**
  - c/op_147 / cpp/op_471 -- **core difference**
  - c/op_147 / cpp/op_507 -- **core difference**
  - c/op_147 / cpp/op_975 -- **core difference**
  - c/op_183 / cpp/op_111 -- **core difference**
  - c/op_183 / cpp/op_147 -- **core difference**
  - c/op_183 / cpp/op_183 -- **total equality**
  - c/op_183 / cpp/op_219 -- **core difference**
  - c/op_183 / cpp/op_471 -- **core difference**
  - c/op_183 / cpp/op_507 -- **core difference**
  - c/op_183 / cpp/op_975 -- **core difference**
  - c/op_219 / cpp/op_111 -- **core difference**
  - c/op_219 / cpp/op_147 -- **core difference**
  - c/op_219 / cpp/op_183 -- **core difference**
  - c/op_219 / cpp/op_219 -- **total equality**
  - c/op_219 / cpp/op_471 -- **core difference**
  - c/op_219 / cpp/op_507 -- **core difference**
  - c/op_219 / cpp/op_975 -- **core difference**
  - c/op_471 / cpp/op_111 -- **core difference**
  - c/op_471 / cpp/op_147 -- **core difference**
  - c/op_471 / cpp/op_183 -- **core difference**
  - c/op_471 / cpp/op_219 -- **core difference**
  - c/op_471 / cpp/op_471 -- **total equality**
  - c/op_471 / cpp/op_507 -- **core difference**
  - c/op_471 / cpp/op_975 -- **core difference**
  - c/op_507 / cpp/op_111 -- **core difference**
  - c/op_507 / cpp/op_147 -- **core difference**
  - c/op_507 / cpp/op_183 -- **core difference**
  - c/op_507 / cpp/op_219 -- **core difference**
  - c/op_507 / cpp/op_471 -- **core difference**
  - c/op_507 / cpp/op_507 -- **total equality**
  - c/op_507 / cpp/op_975 -- **total equality**

### shared-core group F32toF64(F64toF32(And32(3:32,ex32@0(u0:64)),I64StoF64(And32(3:32,ex32@0(u0:64)),in0:64))) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `>` (i64,f32, 0 modes); c `>=` (i64,f32, 0 modes); c `<=` (i64,f32, 0 modes); c `<` (i64,f32, 0 modes); cpp `>` (i64,f32, 0 modes); cpp `>=` (i64,f32, 0 modes); cpp `<=` (i64,f32, 0 modes); cpp `<` (i64,f32, 0 modes); cpp `<=>` (i64,f32, 0 modes)

  - c/op_543 / cpp/op_543 -- **core difference**
  - c/op_543 / cpp/op_579 -- **core difference**
  - c/op_543 / cpp/op_615 -- **core difference**
  - c/op_543 / cpp/op_651 -- **core difference**
  - c/op_543 / cpp/op_759 -- **core difference**
  - c/op_579 / cpp/op_543 -- **core difference**
  - c/op_579 / cpp/op_579 -- **core difference**
  - c/op_579 / cpp/op_615 -- **core difference**
  - c/op_579 / cpp/op_651 -- **core difference**
  - c/op_579 / cpp/op_759 -- **core difference**
  - c/op_615 / cpp/op_543 -- **core difference**
  - c/op_615 / cpp/op_579 -- **core difference**
  - c/op_615 / cpp/op_615 -- **core difference**
  - c/op_615 / cpp/op_651 -- **core difference**
  - c/op_615 / cpp/op_759 -- **core difference**
  - c/op_651 / cpp/op_543 -- **core difference**
  - c/op_651 / cpp/op_579 -- **core difference**
  - c/op_651 / cpp/op_615 -- **core difference**
  - c/op_651 / cpp/op_651 -- **core difference**
  - c/op_651 / cpp/op_759 -- **core difference**

### shared-core group F32toF64(ex32@0(in1:256)) · (i64,f32)

- ground: connection
- languages: c, cpp
- members: c `||` (i64,f32, 0 modes); c `&&` (i64,f32, 0 modes); c `>` (i64,f32, 0 modes); c `>=` (i64,f32, 0 modes); c `<=` (i64,f32, 0 modes); c `<` (i64,f32, 0 modes); cpp `||` (i64,f32, 0 modes); cpp `&&` (i64,f32, 0 modes); cpp `>` (i64,f32, 0 modes); cpp `>=` (i64,f32, 0 modes); cpp `<=` (i64,f32, 0 modes); cpp `<` (i64,f32, 0 modes); cpp `<=>` (i64,f32, 0 modes); cpp `or` (i64,f32, 0 modes); cpp `and` (i64,f32, 0 modes)

  - c/op_291 / cpp/op_291 -- **core difference**
  - c/op_291 / cpp/op_327 -- **core difference**
  - c/op_291 / cpp/op_543 -- **core difference**
  - c/op_291 / cpp/op_579 -- **core difference**
  - c/op_291 / cpp/op_615 -- **core difference**
  - c/op_291 / cpp/op_651 -- **core difference**
  - c/op_291 / cpp/op_759 -- **core difference**
  - c/op_291 / cpp/op_795 -- **core difference**
  - c/op_291 / cpp/op_831 -- **core difference**
  - c/op_327 / cpp/op_291 -- **core difference**
  - c/op_327 / cpp/op_327 -- **core difference**
  - c/op_327 / cpp/op_543 -- **core difference**
  - c/op_327 / cpp/op_579 -- **core difference**
  - c/op_327 / cpp/op_615 -- **core difference**
  - c/op_327 / cpp/op_651 -- **core difference**
  - c/op_327 / cpp/op_759 -- **core difference**
  - c/op_327 / cpp/op_795 -- **core difference**
  - c/op_327 / cpp/op_831 -- **core difference**
  - c/op_543 / cpp/op_291 -- **core difference**
  - c/op_543 / cpp/op_327 -- **core difference**
  - c/op_543 / cpp/op_543 -- **core difference**
  - c/op_543 / cpp/op_579 -- **core difference**
  - c/op_543 / cpp/op_615 -- **core difference**
  - c/op_543 / cpp/op_651 -- **core difference**
  - c/op_543 / cpp/op_759 -- **core difference**
  - c/op_543 / cpp/op_795 -- **core difference**
  - c/op_543 / cpp/op_831 -- **core difference**
  - c/op_579 / cpp/op_291 -- **core difference**
  - c/op_579 / cpp/op_327 -- **core difference**
  - c/op_579 / cpp/op_543 -- **core difference**
  - c/op_579 / cpp/op_579 -- **core difference**
  - c/op_579 / cpp/op_615 -- **core difference**
  - c/op_579 / cpp/op_651 -- **core difference**
  - c/op_579 / cpp/op_759 -- **core difference**
  - c/op_579 / cpp/op_795 -- **core difference**
  - c/op_579 / cpp/op_831 -- **core difference**
  - c/op_615 / cpp/op_291 -- **core difference**
  - c/op_615 / cpp/op_327 -- **core difference**
  - c/op_615 / cpp/op_543 -- **core difference**
  - c/op_615 / cpp/op_579 -- **core difference**
  - c/op_615 / cpp/op_615 -- **core difference**
  - c/op_615 / cpp/op_651 -- **core difference**
  - c/op_615 / cpp/op_759 -- **core difference**
  - c/op_615 / cpp/op_795 -- **core difference**
  - c/op_615 / cpp/op_831 -- **core difference**
  - c/op_651 / cpp/op_291 -- **core difference**
  - c/op_651 / cpp/op_327 -- **core difference**
  - c/op_651 / cpp/op_543 -- **core difference**
  - c/op_651 / cpp/op_579 -- **core difference**
  - c/op_651 / cpp/op_615 -- **core difference**
  - c/op_651 / cpp/op_651 -- **core difference**
  - c/op_651 / cpp/op_759 -- **core difference**
  - c/op_651 / cpp/op_795 -- **core difference**
  - c/op_651 / cpp/op_831 -- **core difference**

### shared-core group And8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64)))) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `&&` (i64,f64, 0 modes); cpp `&&` (i64,f64, 0 modes); cpp `and` (i64,f64, 0 modes)

  - c/op_328 / cpp/op_328 -- **core difference**
  - c/op_328 / cpp/op_832 -- **core difference**

### shared-core group Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64)))) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `||` (i64,f64, 0 modes); cpp `||` (i64,f64, 0 modes); cpp `or` (i64,f64, 0 modes)

  - c/op_292 / cpp/op_292 -- **core difference**
  - c/op_292 / cpp/op_796 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64)))) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `||` (i64,f64, 0 modes); c `&&` (i64,f64, 0 modes); cpp `||` (i64,f64, 0 modes); cpp `&&` (i64,f64, 0 modes); cpp `or` (i64,f64, 0 modes); cpp `and` (i64,f64, 0 modes)

  - c/op_292 / cpp/op_292 -- **core difference**
  - c/op_292 / cpp/op_328 -- **core difference**
  - c/op_292 / cpp/op_796 -- **core difference**
  - c/op_292 / cpp/op_832 -- **core difference**
  - c/op_328 / cpp/op_292 -- **core difference**
  - c/op_328 / cpp/op_328 -- **core difference**
  - c/op_328 / cpp/op_796 -- **core difference**
  - c/op_328 / cpp/op_832 -- **core difference**

### shared-core group ins@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)),XorV128(18446744073709551615:128,CmpEQ64F0x2(ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),ex128@0(in1:256)))) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `!=` (i64,f64, 0 modes); cpp `!=` (i64,f64, 0 modes); cpp `not_eq` (i64,f64, 0 modes)

  - c/op_508 / cpp/op_508 -- **total equality**
  - c/op_508 / cpp/op_976 -- **total equality**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)),CmpEQ64F0x2(ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),ex128@0(in1:256)))))) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `==` (i64,f64, 0 modes); cpp `==` (i64,f64, 0 modes)

  - c/op_472 / cpp/op_472 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),ex64@0(in1:256)))),0:64,u2:64))) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `>` (i64,f64, 0 modes); cpp `>` (i64,f64, 0 modes)

  - c/op_544 / cpp/op_544 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),ex64@0(in1:256)))),0:64,u2:64))) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `>=` (i64,f64, 0 modes); cpp `>=` (i64,f64, 0 modes)

  - c/op_580 / cpp/op_580 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)))))),0:64,u2:64))) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `<=` (i64,f64, 0 modes); cpp `<=` (i64,f64, 0 modes)

  - c/op_616 / cpp/op_616 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)))))),0:64,u2:64))) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `<` (i64,f64, 0 modes); cpp `<` (i64,f64, 0 modes)

  - c/op_652 / cpp/op_652 -- **core difference**

### shared-core group ins@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)),Sub64F0x2(ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),ex128@0(in1:256))) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `-` (i64,f64, 0 modes); cpp `-` (i64,f64, 0 modes)

  - c/op_148 / cpp/op_148 -- **total equality**

### shared-core group ins@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)),Div64F0x2(ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),ex128@0(in1:256))) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `/` (i64,f64, 0 modes); cpp `/` (i64,f64, 0 modes)

  - c/op_220 / cpp/op_220 -- **total equality**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),ex64@0(in1:256)))) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `>` (i64,f64, 0 modes); c `>=` (i64,f64, 0 modes); cpp `>` (i64,f64, 0 modes); cpp `>=` (i64,f64, 0 modes); cpp `<=>` (i64,f64, 0 modes)

  - c/op_544 / cpp/op_544 -- **core difference**
  - c/op_544 / cpp/op_580 -- **core difference**
  - c/op_544 / cpp/op_760 -- **core difference**
  - c/op_580 / cpp/op_544 -- **core difference**
  - c/op_580 / cpp/op_580 -- **core difference**
  - c/op_580 / cpp/op_760 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)))))) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `<=` (i64,f64, 0 modes); c `<` (i64,f64, 0 modes); cpp `<=` (i64,f64, 0 modes); cpp `<` (i64,f64, 0 modes); cpp `<=>` (i64,f64, 0 modes)

  - c/op_616 / cpp/op_616 -- **core difference**
  - c/op_616 / cpp/op_652 -- **core difference**
  - c/op_616 / cpp/op_760 -- **core difference**
  - c/op_652 / cpp/op_616 -- **core difference**
  - c/op_652 / cpp/op_652 -- **core difference**
  - c/op_652 / cpp/op_760 -- **core difference**

### shared-core group CmpEQ64F0x2(ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))),ex128@0(in1:256)) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `==` (i64,f64, 0 modes); c `!=` (i64,f64, 0 modes); cpp `==` (i64,f64, 0 modes); cpp `!=` (i64,f64, 0 modes); cpp `not_eq` (i64,f64, 0 modes)

  - c/op_472 / cpp/op_472 -- **total equality**
  - c/op_472 / cpp/op_508 -- **core difference**
  - c/op_472 / cpp/op_976 -- **core difference**
  - c/op_508 / cpp/op_472 -- **core difference**
  - c/op_508 / cpp/op_508 -- **total equality**
  - c/op_508 / cpp/op_976 -- **total equality**

### shared-core group Add64F0x2(ex128@0(in1:256),ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)))) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `+` (i64,f64, 0 modes); cpp `+` (i64,f64, 0 modes)

  - c/op_112 / cpp/op_112 -- **total equality**

### shared-core group Mul64F0x2(ex128@0(in1:256),ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)))) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `*` (i64,f64, 0 modes); cpp `*` (i64,f64, 0 modes)

  - c/op_184 / cpp/op_184 -- **total equality**

### shared-core group ex128@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `+` (i64,f64, 0 modes); c `-` (i64,f64, 0 modes); c `*` (i64,f64, 0 modes); c `/` (i64,f64, 0 modes); c `==` (i64,f64, 0 modes); c `!=` (i64,f64, 0 modes); cpp `+` (i64,f64, 0 modes); cpp `-` (i64,f64, 0 modes); cpp `*` (i64,f64, 0 modes); cpp `/` (i64,f64, 0 modes); cpp `==` (i64,f64, 0 modes); cpp `!=` (i64,f64, 0 modes); cpp `not_eq` (i64,f64, 0 modes)

  - c/op_112 / cpp/op_112 -- **total equality**
  - c/op_112 / cpp/op_148 -- **core difference**
  - c/op_112 / cpp/op_184 -- **core difference**
  - c/op_112 / cpp/op_220 -- **core difference**
  - c/op_112 / cpp/op_472 -- **core difference**
  - c/op_112 / cpp/op_508 -- **core difference**
  - c/op_112 / cpp/op_976 -- **core difference**
  - c/op_148 / cpp/op_112 -- **core difference**
  - c/op_148 / cpp/op_148 -- **total equality**
  - c/op_148 / cpp/op_184 -- **core difference**
  - c/op_148 / cpp/op_220 -- **core difference**
  - c/op_148 / cpp/op_472 -- **core difference**
  - c/op_148 / cpp/op_508 -- **core difference**
  - c/op_148 / cpp/op_976 -- **core difference**
  - c/op_184 / cpp/op_112 -- **core difference**
  - c/op_184 / cpp/op_148 -- **core difference**
  - c/op_184 / cpp/op_184 -- **total equality**
  - c/op_184 / cpp/op_220 -- **core difference**
  - c/op_184 / cpp/op_472 -- **core difference**
  - c/op_184 / cpp/op_508 -- **core difference**
  - c/op_184 / cpp/op_976 -- **core difference**
  - c/op_220 / cpp/op_112 -- **core difference**
  - c/op_220 / cpp/op_148 -- **core difference**
  - c/op_220 / cpp/op_184 -- **core difference**
  - c/op_220 / cpp/op_220 -- **total equality**
  - c/op_220 / cpp/op_472 -- **core difference**
  - c/op_220 / cpp/op_508 -- **core difference**
  - c/op_220 / cpp/op_976 -- **core difference**
  - c/op_472 / cpp/op_112 -- **core difference**
  - c/op_472 / cpp/op_148 -- **core difference**
  - c/op_472 / cpp/op_184 -- **core difference**
  - c/op_472 / cpp/op_220 -- **core difference**
  - c/op_472 / cpp/op_472 -- **total equality**
  - c/op_472 / cpp/op_508 -- **core difference**
  - c/op_472 / cpp/op_976 -- **core difference**
  - c/op_508 / cpp/op_112 -- **core difference**
  - c/op_508 / cpp/op_148 -- **core difference**
  - c/op_508 / cpp/op_184 -- **core difference**
  - c/op_508 / cpp/op_220 -- **core difference**
  - c/op_508 / cpp/op_472 -- **core difference**
  - c/op_508 / cpp/op_508 -- **total equality**
  - c/op_508 / cpp/op_976 -- **total equality**

### shared-core group ex64@0(ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64))) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `>` (i64,f64, 0 modes); c `>=` (i64,f64, 0 modes); c `<=` (i64,f64, 0 modes); c `<` (i64,f64, 0 modes); cpp `>` (i64,f64, 0 modes); cpp `>=` (i64,f64, 0 modes); cpp `<=` (i64,f64, 0 modes); cpp `<` (i64,f64, 0 modes); cpp `<=>` (i64,f64, 0 modes)

  - c/op_544 / cpp/op_544 -- **core difference**
  - c/op_544 / cpp/op_580 -- **core difference**
  - c/op_544 / cpp/op_616 -- **core difference**
  - c/op_544 / cpp/op_652 -- **core difference**
  - c/op_544 / cpp/op_760 -- **core difference**
  - c/op_580 / cpp/op_544 -- **core difference**
  - c/op_580 / cpp/op_580 -- **core difference**
  - c/op_580 / cpp/op_616 -- **core difference**
  - c/op_580 / cpp/op_652 -- **core difference**
  - c/op_580 / cpp/op_760 -- **core difference**
  - c/op_616 / cpp/op_544 -- **core difference**
  - c/op_616 / cpp/op_580 -- **core difference**
  - c/op_616 / cpp/op_616 -- **core difference**
  - c/op_616 / cpp/op_652 -- **core difference**
  - c/op_616 / cpp/op_760 -- **core difference**
  - c/op_652 / cpp/op_544 -- **core difference**
  - c/op_652 / cpp/op_580 -- **core difference**
  - c/op_652 / cpp/op_616 -- **core difference**
  - c/op_652 / cpp/op_652 -- **core difference**
  - c/op_652 / cpp/op_760 -- **core difference**

### shared-core group ins@0(u0:256,I64StoF64(And32(3:32,ex32@0(u1:64)),in0:64)) · (i64,f64)

- ground: connection
- languages: c, cpp
- members: c `+` (i64,f64, 0 modes); c `-` (i64,f64, 0 modes); c `*` (i64,f64, 0 modes); c `/` (i64,f64, 0 modes); c `==` (i64,f64, 0 modes); c `!=` (i64,f64, 0 modes); c `>` (i64,f64, 0 modes); c `>=` (i64,f64, 0 modes); c `<=` (i64,f64, 0 modes); c `<` (i64,f64, 0 modes); cpp `+` (i64,f64, 0 modes); cpp `-` (i64,f64, 0 modes); cpp `*` (i64,f64, 0 modes); cpp `/` (i64,f64, 0 modes); cpp `==` (i64,f64, 0 modes); cpp `!=` (i64,f64, 0 modes); cpp `>` (i64,f64, 0 modes); cpp `>=` (i64,f64, 0 modes); cpp `<=` (i64,f64, 0 modes); cpp `<` (i64,f64, 0 modes); cpp `<=>` (i64,f64, 0 modes); cpp `not_eq` (i64,f64, 0 modes)

  - c/op_112 / cpp/op_112 -- **total equality**
  - c/op_112 / cpp/op_148 -- **core difference**
  - c/op_112 / cpp/op_184 -- **core difference**
  - c/op_112 / cpp/op_220 -- **core difference**
  - c/op_112 / cpp/op_472 -- **core difference**
  - c/op_112 / cpp/op_508 -- **core difference**
  - c/op_112 / cpp/op_544 -- **core difference**
  - c/op_112 / cpp/op_580 -- **core difference**
  - c/op_112 / cpp/op_616 -- **core difference**
  - c/op_112 / cpp/op_652 -- **core difference**
  - c/op_112 / cpp/op_760 -- **core difference**
  - c/op_112 / cpp/op_976 -- **core difference**
  - c/op_148 / cpp/op_112 -- **core difference**
  - c/op_148 / cpp/op_148 -- **total equality**
  - c/op_148 / cpp/op_184 -- **core difference**
  - c/op_148 / cpp/op_220 -- **core difference**
  - c/op_148 / cpp/op_472 -- **core difference**
  - c/op_148 / cpp/op_508 -- **core difference**
  - c/op_148 / cpp/op_544 -- **core difference**
  - c/op_148 / cpp/op_580 -- **core difference**
  - c/op_148 / cpp/op_616 -- **core difference**
  - c/op_148 / cpp/op_652 -- **core difference**
  - c/op_148 / cpp/op_760 -- **core difference**
  - c/op_148 / cpp/op_976 -- **core difference**
  - c/op_184 / cpp/op_112 -- **core difference**
  - c/op_184 / cpp/op_148 -- **core difference**
  - c/op_184 / cpp/op_184 -- **total equality**
  - c/op_184 / cpp/op_220 -- **core difference**
  - c/op_184 / cpp/op_472 -- **core difference**
  - c/op_184 / cpp/op_508 -- **core difference**
  - c/op_184 / cpp/op_544 -- **core difference**
  - c/op_184 / cpp/op_580 -- **core difference**
  - c/op_184 / cpp/op_616 -- **core difference**
  - c/op_184 / cpp/op_652 -- **core difference**
  - c/op_184 / cpp/op_760 -- **core difference**
  - c/op_184 / cpp/op_976 -- **core difference**
  - c/op_220 / cpp/op_112 -- **core difference**
  - c/op_220 / cpp/op_148 -- **core difference**
  - c/op_220 / cpp/op_184 -- **core difference**
  - c/op_220 / cpp/op_220 -- **total equality**
  - c/op_220 / cpp/op_472 -- **core difference**
  - c/op_220 / cpp/op_508 -- **core difference**
  - c/op_220 / cpp/op_544 -- **core difference**
  - c/op_220 / cpp/op_580 -- **core difference**
  - c/op_220 / cpp/op_616 -- **core difference**
  - c/op_220 / cpp/op_652 -- **core difference**
  - c/op_220 / cpp/op_760 -- **core difference**
  - c/op_220 / cpp/op_976 -- **core difference**
  - c/op_472 / cpp/op_112 -- **core difference**
  - c/op_472 / cpp/op_148 -- **core difference**
  - c/op_472 / cpp/op_184 -- **core difference**
  - c/op_472 / cpp/op_220 -- **core difference**
  - c/op_472 / cpp/op_472 -- **total equality**
  - c/op_472 / cpp/op_508 -- **core difference**
  - c/op_472 / cpp/op_544 -- **core difference**
  - c/op_472 / cpp/op_580 -- **core difference**
  - c/op_472 / cpp/op_616 -- **core difference**
  - c/op_472 / cpp/op_652 -- **core difference**
  - c/op_472 / cpp/op_760 -- **core difference**
  - c/op_472 / cpp/op_976 -- **core difference**
  - c/op_508 / cpp/op_112 -- **core difference**
  - c/op_508 / cpp/op_148 -- **core difference**
  - c/op_508 / cpp/op_184 -- **core difference**
  - c/op_508 / cpp/op_220 -- **core difference**
  - c/op_508 / cpp/op_472 -- **core difference**
  - c/op_508 / cpp/op_508 -- **total equality**
  - c/op_508 / cpp/op_544 -- **core difference**
  - c/op_508 / cpp/op_580 -- **core difference**
  - c/op_508 / cpp/op_616 -- **core difference**
  - c/op_508 / cpp/op_652 -- **core difference**
  - c/op_508 / cpp/op_760 -- **core difference**
  - c/op_508 / cpp/op_976 -- **total equality**
  - c/op_544 / cpp/op_112 -- **core difference**
  - c/op_544 / cpp/op_148 -- **core difference**
  - c/op_544 / cpp/op_184 -- **core difference**
  - c/op_544 / cpp/op_220 -- **core difference**
  - c/op_544 / cpp/op_472 -- **core difference**
  - c/op_544 / cpp/op_508 -- **core difference**
  - c/op_544 / cpp/op_544 -- **core difference**
  - c/op_544 / cpp/op_580 -- **core difference**
  - c/op_544 / cpp/op_616 -- **core difference**
  - c/op_544 / cpp/op_652 -- **core difference**
  - c/op_544 / cpp/op_760 -- **core difference**
  - c/op_544 / cpp/op_976 -- **core difference**
  - c/op_580 / cpp/op_112 -- **core difference**
  - c/op_580 / cpp/op_148 -- **core difference**
  - c/op_580 / cpp/op_184 -- **core difference**
  - c/op_580 / cpp/op_220 -- **core difference**
  - c/op_580 / cpp/op_472 -- **core difference**
  - c/op_580 / cpp/op_508 -- **core difference**
  - c/op_580 / cpp/op_544 -- **core difference**
  - c/op_580 / cpp/op_580 -- **core difference**
  - c/op_580 / cpp/op_616 -- **core difference**
  - c/op_580 / cpp/op_652 -- **core difference**
  - c/op_580 / cpp/op_760 -- **core difference**
  - c/op_580 / cpp/op_976 -- **core difference**
  - c/op_616 / cpp/op_112 -- **core difference**
  - c/op_616 / cpp/op_148 -- **core difference**
  - c/op_616 / cpp/op_184 -- **core difference**
  - c/op_616 / cpp/op_220 -- **core difference**
  - c/op_616 / cpp/op_472 -- **core difference**
  - c/op_616 / cpp/op_508 -- **core difference**
  - c/op_616 / cpp/op_544 -- **core difference**
  - c/op_616 / cpp/op_580 -- **core difference**
  - c/op_616 / cpp/op_616 -- **core difference**
  - c/op_616 / cpp/op_652 -- **core difference**
  - c/op_616 / cpp/op_760 -- **core difference**
  - c/op_616 / cpp/op_976 -- **core difference**
  - c/op_652 / cpp/op_112 -- **core difference**
  - c/op_652 / cpp/op_148 -- **core difference**
  - c/op_652 / cpp/op_184 -- **core difference**
  - c/op_652 / cpp/op_220 -- **core difference**
  - c/op_652 / cpp/op_472 -- **core difference**
  - c/op_652 / cpp/op_508 -- **core difference**
  - c/op_652 / cpp/op_544 -- **core difference**
  - c/op_652 / cpp/op_580 -- **core difference**
  - c/op_652 / cpp/op_616 -- **core difference**
  - c/op_652 / cpp/op_652 -- **core difference**
  - c/op_652 / cpp/op_760 -- **core difference**
  - c/op_652 / cpp/op_976 -- **core difference**

### shared-core group And8(zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64)))) · (i64,i32)

- ground: connection
- languages: c, cpp
- members: c `&&` (i64,i32, 0 modes); cpp `&&` (i64,i32, 0 modes); cpp `and` (i64,i32, 0 modes)

  - c/op_324 / cpp/op_324 -- **core difference**
  - c/op_324 / cpp/op_828 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64)))) · (i64,i32)

- ground: connection
- languages: c, cpp
- members: c `||` (i64,i32, 0 modes); cpp `||` (i64,i32, 0 modes); cpp `or` (i64,i32, 0 modes)

  - c/op_288 / cpp/op_288 -- **core difference**
  - c/op_288 / cpp/op_792 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(15:64,8:64,in0:64,sx64(ex32@0(in1:64)),u0:64))) · (i64,i32)

- ground: connection
- languages: c, cpp
- members: c `>` (i64,i32, 1 modes); cpp `>` (i64,i32, 1 modes); cpp `<=>` (i64,i32, 0 modes)

  - c/op_540 / cpp/op_540 -- **core difference**
  - c/op_540 / cpp/op_756 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)

### shared-core group zx8(ex1@0(amd64g_calculate_condition(13:64,8:64,in0:64,sx64(ex32@0(in1:64)),u0:64))) · (i64,i32)

- ground: connection
- languages: c, cpp
- members: c `>=` (i64,i32, 1 modes); cpp `>=` (i64,i32, 1 modes)

  - c/op_576 / cpp/op_576 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(14:64,8:64,in0:64,sx64(ex32@0(in1:64)),u0:64))) · (i64,i32)

- ground: connection
- languages: c, cpp
- members: c `<=` (i64,i32, 1 modes); cpp `<=` (i64,i32, 1 modes)

  - c/op_612 / cpp/op_612 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(12:64,8:64,in0:64,sx64(ex32@0(in1:64)),u0:64))) · (i64,i32)

- ground: connection
- languages: c, cpp
- members: c `<` (i64,i32, 1 modes); cpp `<` (i64,i32, 1 modes); cpp `<=>` (i64,i32, 0 modes)

  - c/op_648 / cpp/op_648 -- **core difference**
  - c/op_648 / cpp/op_756 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)

### shared-core group zx8(ex1@0(amd64g_calculate_condition(4:64,8:64,in0:64,sx64(ex32@0(in1:64)),u0:64))) · (i64,i32)

- ground: connection
- languages: c, cpp
- members: c `==` (i64,i32, 1 modes); cpp `==` (i64,i32, 1 modes)

  - c/op_468 / cpp/op_468 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,8:64,in0:64,sx64(ex32@0(in1:64)),u0:64))) · (i64,i32)

- ground: connection
- languages: c, cpp
- members: c `!=` (i64,i32, 2 modes); cpp `!=` (i64,i32, 1 modes); cpp `not_eq` (i64,i32, 1 modes)

  - c/op_504 / cpp/op_504 -- **core difference**
  - c/op_504 / cpp/op_972 -- **core difference**

### shared-core group ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),sx64(ex32@0(in1:64)))) · (i64,i32)

- ground: connection
- languages: c, cpp
- members: c `/` (i64,i32, 0 modes); c `%` (i64,i32, 0 modes); cpp `/` (i64,i32, 0 modes); cpp `%` (i64,i32, 0 modes)

  - c/op_216 / cpp/op_216 -- **total equality**
  - c/op_216 / cpp/op_252 -- **core difference**
  - c/op_252 / cpp/op_216 -- **core difference**
  - c/op_252 / cpp/op_252 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64))) · (i64,i32)

- ground: connection
- languages: c, cpp
- members: c `||` (i64,i32, 0 modes); c `&&` (i64,i32, 0 modes); cpp `||` (i64,i32, 0 modes); cpp `&&` (i64,i32, 0 modes); cpp `or` (i64,i32, 0 modes); cpp `and` (i64,i32, 0 modes)

  - c/op_288 / cpp/op_288 -- **core difference**
  - c/op_288 / cpp/op_324 -- **core difference**
  - c/op_288 / cpp/op_792 -- **core difference**
  - c/op_288 / cpp/op_828 -- **core difference**
  - c/op_324 / cpp/op_288 -- **core difference**
  - c/op_324 / cpp/op_324 -- **core difference**
  - c/op_324 / cpp/op_792 -- **core difference**
  - c/op_324 / cpp/op_828 -- **core difference**

### shared-core group Shl64(in0:64,And8(63:8,ex8@0(in1:64))) · (i64,i32)

- ground: connection
- languages: c, cpp, go, rust
- members: c `<<` (i64,i32, 0 modes); cpp `<<` (i64,i32, 0 modes); go `<<` (i64,i32, 1 modes); rust `<<` (i64,i32, 0 modes)

  - c/op_684 / cpp/op_684 -- **total equality**
  - c/op_684 / go/op_174 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_684 / rust/op_468 -- **total equality**
  - cpp/op_684 / go/op_174 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_684 / rust/op_468 -- **total equality**
  - go/op_174 / rust/op_468 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)

### shared-core group Sar64(in0:64,And8(63:8,ex8@0(in1:64))) · (i64,i32)

- ground: connection
- languages: c, cpp, rust
- members: c `>>` (i64,i32, 0 modes); cpp `>>` (i64,i32, 0 modes); rust `>>` (i64,i32, 0 modes)

  - c/op_720 / cpp/op_720 -- **total equality**
  - c/op_720 / rust/op_504 -- **total equality**
  - cpp/op_720 / rust/op_504 -- **total equality**

### shared-core group Add64(in0:64,sx64(ex32@0(in1:64))) · (i64,i32)

- ground: connection
- languages: c, cpp
- members: c `+` (i64,i32, 0 modes); cpp `+` (i64,i32, 0 modes)

  - c/op_108 / cpp/op_108 -- **total equality**

### shared-core group Sub64(in0:64,sx64(ex32@0(in1:64))) · (i64,i32)

- ground: connection
- languages: c, cpp
- members: c `-` (i64,i32, 0 modes); cpp `-` (i64,i32, 0 modes)

  - c/op_144 / cpp/op_144 -- **total equality**

### shared-core group Mul64(in0:64,sx64(ex32@0(in1:64))) · (i64,i32)

- ground: connection
- languages: c, cpp
- members: c `*` (i64,i32, 0 modes); cpp `*` (i64,i32, 0 modes)

  - c/op_180 / cpp/op_180 -- **total equality**

### shared-core group Xor64(in0:64,sx64(ex32@0(in1:64))) · (i64,i32)

- ground: connection
- languages: c, cpp
- members: c `^` (i64,i32, 0 modes); cpp `^` (i64,i32, 0 modes); cpp `xor` (i64,i32, 0 modes)

  - c/op_396 / cpp/op_396 -- **total equality**
  - c/op_396 / cpp/op_900 -- **total equality**

### shared-core group And64(in0:64,sx64(ex32@0(in1:64))) · (i64,i32)

- ground: connection
- languages: c, cpp
- members: c `&` (i64,i32, 0 modes); cpp `&` (i64,i32, 0 modes); cpp `bitand` (i64,i32, 0 modes)

  - c/op_432 / cpp/op_432 -- **total equality**
  - c/op_432 / cpp/op_936 -- **total equality**

### shared-core group Or64(in0:64,sx64(ex32@0(in1:64))) · (i64,i32)

- ground: connection
- languages: c, cpp
- members: c `|` (i64,i32, 0 modes); cpp `|` (i64,i32, 0 modes); cpp `bitor` (i64,i32, 0 modes)

  - c/op_360 / cpp/op_360 -- **total equality**
  - c/op_360 / cpp/op_864 -- **total equality**

### shared-core group And8(63:8,ex8@0(in1:64)) · (i64,i32)

- ground: connection
- languages: c, cpp, go, rust
- members: c `<<` (i64,i32, 0 modes); c `>>` (i64,i32, 0 modes); cpp `<<` (i64,i32, 0 modes); cpp `>>` (i64,i32, 0 modes); go `<<` (i64,i32, 1 modes); rust `<<` (i64,i32, 0 modes); rust `>>` (i64,i32, 0 modes)

  - c/op_684 / cpp/op_684 -- **total equality**
  - c/op_684 / cpp/op_720 -- **core difference**
  - c/op_720 / cpp/op_684 -- **core difference**
  - c/op_720 / cpp/op_720 -- **total equality**
  - c/op_684 / go/op_174 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_720 / go/op_174 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_684 / rust/op_468 -- **total equality**
  - c/op_684 / rust/op_504 -- **core difference**
  - c/op_720 / rust/op_468 -- **core difference**
  - c/op_720 / rust/op_504 -- **total equality**
  - cpp/op_684 / go/op_174 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_720 / go/op_174 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_684 / rust/op_468 -- **total equality**
  - cpp/op_684 / rust/op_504 -- **core difference**
  - cpp/op_720 / rust/op_468 -- **core difference**
  - cpp/op_720 / rust/op_504 -- **total equality**
  - go/op_174 / rust/op_468 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - go/op_174 / rust/op_504 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)

### shared-core group And8(zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (i64,i64)

- ground: connection
- languages: c, cpp
- members: c `&&` (i64,i64, 0 modes); cpp `&&` (i64,i64, 0 modes); cpp `and` (i64,i64, 0 modes)

  - c/op_325 / cpp/op_325 -- **core difference**
  - c/op_325 / cpp/op_829 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,Or64(in0:64,in1:64),0:64,u0:64))) · (i64,i64)

- ground: connection
- languages: c, cpp
- members: c `||` (i64,i64, 0 modes); cpp `||` (i64,i64, 0 modes); cpp `or` (i64,i64, 0 modes)

  - c/op_289 / cpp/op_289 -- **core difference**
  - c/op_289 / cpp/op_793 -- **core difference**

### shared-core group ex1@0(amd64g_calculate_condition(4:64,8:64,in1:64,18446744073709551615:64,u0:64)) · (i64,i64)

- ground: connection
- languages: go, swift
- members: go `/` (i64,i64, 1 modes); go `%` (i64,i64, 1 modes); swift `/` (i64,i64, 2 modes); swift `%` (i64,i64, 2 modes)

  - go/op_103 / swift/op_157 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_103 / swift/op_193 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_139 / swift/op_157 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_139 / swift/op_193 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)

### shared-core group zx8(ex1@0(amd64g_calculate_condition(15:64,8:64,in0:64,in1:64,u0:64))) · (i64,i64)

- ground: connection
- languages: c, cpp, rust
- members: c `>` (i64,i64, 0 modes); cpp `>` (i64,i64, 0 modes); cpp `<=>` (i64,i64, 0 modes); rust `>` (i64,i64, 0 modes)

  - c/op_541 / cpp/op_541 -- **core difference**
  - c/op_541 / cpp/op_757 -- **core difference**
  - c/op_541 / rust/op_397 -- **core difference**
  - cpp/op_541 / rust/op_397 -- **total equality**
  - cpp/op_757 / rust/op_397 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(13:64,8:64,in0:64,in1:64,u0:64))) · (i64,i64)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `>=` (i64,i64, 0 modes); cpp `>=` (i64,i64, 0 modes); rust `>=` (i64,i64, 0 modes); swift `>=` (i64,i64, 0 modes)

  - c/op_577 / cpp/op_577 -- **core difference**
  - c/op_577 / rust/op_433 -- **core difference**
  - c/op_577 / swift/op_409 -- **core difference**
  - cpp/op_577 / rust/op_433 -- **total equality**
  - cpp/op_577 / swift/op_409 -- **total equality**
  - rust/op_433 / swift/op_409 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(14:64,8:64,in0:64,in1:64,u0:64))) · (i64,i64)

- ground: connection
- languages: c, cpp, rust
- members: c `<=` (i64,i64, 0 modes); cpp `<=` (i64,i64, 0 modes); rust `<=` (i64,i64, 0 modes)

  - c/op_613 / cpp/op_613 -- **core difference**
  - c/op_613 / rust/op_361 -- **core difference**
  - cpp/op_613 / rust/op_361 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(12:64,8:64,in0:64,in1:64,u0:64))) · (i64,i64)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `<` (i64,i64, 0 modes); cpp `<` (i64,i64, 0 modes); cpp `<=>` (i64,i64, 0 modes); rust `<` (i64,i64, 0 modes); swift `<` (i64,i64, 0 modes)

  - c/op_649 / cpp/op_649 -- **core difference**
  - c/op_649 / cpp/op_757 -- **core difference**
  - c/op_649 / rust/op_325 -- **core difference**
  - c/op_649 / swift/op_301 -- **core difference**
  - cpp/op_649 / rust/op_325 -- **total equality**
  - cpp/op_757 / rust/op_325 -- **core difference**
  - cpp/op_649 / swift/op_301 -- **total equality**
  - cpp/op_757 / swift/op_301 -- **core difference**
  - rust/op_325 / swift/op_301 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(13:64,8:64,in1:64,in0:64,u0:64))) · (i64,i64)

- ground: connection
- languages: go, swift
- members: go `<=` (i64,i64, 0 modes); swift `<=` (i64,i64, 0 modes)

  - go/op_571 / swift/op_373 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(12:64,8:64,in1:64,in0:64,u0:64))) · (i64,i64)

- ground: connection
- languages: go, swift
- members: go `>` (i64,i64, 0 modes); swift `>` (i64,i64, 0 modes)

  - go/op_607 / swift/op_337 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(4:64,8:64,in0:64,in1:64,u0:64))) · (i64,i64)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `==` (i64,i64, 0 modes); cpp `==` (i64,i64, 0 modes); rust `==` (i64,i64, 0 modes); swift `==` (i64,i64, 0 modes)

  - c/op_469 / cpp/op_469 -- **core difference**
  - c/op_469 / rust/op_253 -- **core difference**
  - c/op_469 / swift/op_517 -- **core difference**
  - cpp/op_469 / rust/op_253 -- **total equality**
  - cpp/op_469 / swift/op_517 -- **total equality**
  - rust/op_253 / swift/op_517 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,8:64,in0:64,in1:64,u0:64))) · (i64,i64)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `!=` (i64,i64, 0 modes); cpp `!=` (i64,i64, 0 modes); cpp `not_eq` (i64,i64, 0 modes); rust `!=` (i64,i64, 0 modes); swift `!=` (i64,i64, 0 modes)

  - c/op_505 / cpp/op_505 -- **core difference**
  - c/op_505 / cpp/op_973 -- **core difference**
  - c/op_505 / rust/op_289 -- **core difference**
  - c/op_505 / swift/op_445 -- **core difference**
  - cpp/op_505 / rust/op_289 -- **total equality**
  - cpp/op_973 / rust/op_289 -- **total equality**
  - cpp/op_505 / swift/op_445 -- **total equality**
  - cpp/op_973 / swift/op_445 -- **total equality**
  - rust/op_289 / swift/op_445 -- **total equality**

### shared-core group ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64)) · (i64,i64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `/` (i64,i64, 0 modes); c `%` (i64,i64, 0 modes); cpp `/` (i64,i64, 0 modes); cpp `%` (i64,i64, 0 modes); go `/` (i64,i64, 1 modes); go `%` (i64,i64, 1 modes); rust `/` (i64,i64, 2 modes); rust `%` (i64,i64, 2 modes); swift `/` (i64,i64, 2 modes); swift `%` (i64,i64, 2 modes)

  - c/op_217 / cpp/op_217 -- **total equality**
  - c/op_217 / cpp/op_253 -- **core difference**
  - c/op_253 / cpp/op_217 -- **core difference**
  - c/op_253 / cpp/op_253 -- **total equality**
  - c/op_217 / go/op_103 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - c/op_217 / go/op_139 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - c/op_253 / go/op_103 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - c/op_253 / go/op_139 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - c/op_217 / rust/op_649 -- **core equality, modes differ**
    - only on the right: `(~in1 | (-9223372036854775808 ^ in0)) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
  - c/op_217 / rust/op_685 -- **core difference**
    - only on the right: `(~in1 | (-9223372036854775808 ^ in0)) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
  - c/op_253 / rust/op_649 -- **core difference**
    - only on the right: `(~in1 | (-9223372036854775808 ^ in0)) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
  - c/op_253 / rust/op_685 -- **core equality, modes differ**
    - only on the right: `(~in1 | (-9223372036854775808 ^ in0)) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
  - c/op_217 / swift/op_157 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - c/op_217 / swift/op_193 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - c/op_253 / swift/op_157 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - c/op_253 / swift/op_193 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_217 / go/op_103 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - cpp/op_217 / go/op_139 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - cpp/op_253 / go/op_103 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - cpp/op_253 / go/op_139 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - cpp/op_217 / rust/op_649 -- **core equality, modes differ**
    - only on the right: `(~in1 | (-9223372036854775808 ^ in0)) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
  - cpp/op_217 / rust/op_685 -- **core difference**
    - only on the right: `(~in1 | (-9223372036854775808 ^ in0)) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
  - cpp/op_253 / rust/op_649 -- **core difference**
    - only on the right: `(~in1 | (-9223372036854775808 ^ in0)) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
  - cpp/op_253 / rust/op_685 -- **core equality, modes differ**
    - only on the right: `(~in1 | (-9223372036854775808 ^ in0)) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
  - cpp/op_217 / swift/op_157 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_217 / swift/op_193 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_253 / swift/op_157 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_253 / swift/op_193 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_103 / rust/op_649 -- **core difference**
    - only on the right: `(~in1 | (-9223372036854775808 ^ in0)) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow` (branch-to-response)
  - go/op_103 / rust/op_685 -- **core difference**
    - only on the right: `(~in1 | (-9223372036854775808 ^ in0)) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow` (branch-to-response)
  - go/op_139 / rust/op_649 -- **core difference**
    - only on the right: `(~in1 | (-9223372036854775808 ^ in0)) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow` (branch-to-response)
  - go/op_139 / rust/op_685 -- **core difference**
    - only on the right: `(~in1 | (-9223372036854775808 ^ in0)) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow` (branch-to-response)
  - go/op_103 / swift/op_157 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_103 / swift/op_193 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_139 / swift/op_157 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_139 / swift/op_193 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_649 / swift/op_157 -- **core difference**
    - only on the left: `(~in1 | (-9223372036854775808 ^ in0)) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow` (branch-to-response)
    - only on the left: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_649 / swift/op_193 -- **core difference**
    - only on the left: `(~in1 | (-9223372036854775808 ^ in0)) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow` (branch-to-response)
    - only on the left: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_685 / swift/op_157 -- **core difference**
    - only on the left: `(~in1 | (-9223372036854775808 ^ in0)) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow` (branch-to-response)
    - only on the left: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_685 / swift/op_193 -- **core difference**
    - only on the left: `(~in1 | (-9223372036854775808 ^ in0)) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow` (branch-to-response)
    - only on the left: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)

### shared-core group ex1@0(amd64g_calculate_condition(12:64,8:64,in1:64,in0:64,u0:64)) · (i64,i64)

- ground: connection
- languages: go, swift
- members: go `>` (i64,i64, 0 modes); swift `>` (i64,i64, 0 modes); swift `..<` (i64,i64, 1 modes); swift `...` (i64,i64, 1 modes)

  - go/op_607 / swift/op_337 -- **total equality**
  - go/op_607 / swift/op_877 -- **core difference**
    - only on the right: `in1 < in0 (signed)` -> `trap` (branch-to-response)
  - go/op_607 / swift/op_913 -- **core difference**
    - only on the right: `in1 < in0 (signed)` -> `trap` (branch-to-response)

### shared-core group Shl64(in0:64,And8(63:8,ex8@0(in1:64))) · (i64,i64)

- ground: connection
- languages: c, cpp, go, rust
- members: c `<<` (i64,i64, 0 modes); cpp `<<` (i64,i64, 0 modes); go `<<` (i64,i64, 1 modes); rust `<<` (i64,i64, 0 modes)

  - c/op_685 / cpp/op_685 -- **total equality**
  - c/op_685 / go/op_175 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_685 / rust/op_469 -- **total equality**
  - cpp/op_685 / go/op_175 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_685 / rust/op_469 -- **total equality**
  - go/op_175 / rust/op_469 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)

### shared-core group Sar64(in0:64,And8(63:8,ex8@0(in1:64))) · (i64,i64)

- ground: connection
- languages: c, cpp, rust
- members: c `>>` (i64,i64, 0 modes); cpp `>>` (i64,i64, 0 modes); rust `>>` (i64,i64, 0 modes)

  - c/op_721 / cpp/op_721 -- **total equality**
  - c/op_721 / rust/op_505 -- **total equality**
  - cpp/op_721 / rust/op_505 -- **total equality**

### shared-core group And8(63:8,ex8@0(in1:64)) · (i64,i64)

- ground: connection
- languages: c, cpp, go, rust
- members: c `<<` (i64,i64, 0 modes); c `>>` (i64,i64, 0 modes); cpp `<<` (i64,i64, 0 modes); cpp `>>` (i64,i64, 0 modes); go `<<` (i64,i64, 1 modes); rust `<<` (i64,i64, 0 modes); rust `>>` (i64,i64, 0 modes)

  - c/op_685 / cpp/op_685 -- **total equality**
  - c/op_685 / cpp/op_721 -- **core difference**
  - c/op_721 / cpp/op_685 -- **core difference**
  - c/op_721 / cpp/op_721 -- **total equality**
  - c/op_685 / go/op_175 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_721 / go/op_175 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_685 / rust/op_469 -- **total equality**
  - c/op_685 / rust/op_505 -- **core difference**
  - c/op_721 / rust/op_469 -- **core difference**
  - c/op_721 / rust/op_505 -- **total equality**
  - cpp/op_685 / go/op_175 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_721 / go/op_175 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_685 / rust/op_469 -- **total equality**
  - cpp/op_685 / rust/op_505 -- **core difference**
  - cpp/op_721 / rust/op_469 -- **core difference**
  - cpp/op_721 / rust/op_505 -- **total equality**
  - go/op_175 / rust/op_469 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - go/op_175 / rust/op_505 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)

### shared-core group Add64(in0:64,in1:64) · (i64,i64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `+` (i64,i64, 1 modes); cpp `+` (i64,i64, 1 modes); go `+` (i64,i64, 1 modes); rust `+` (i64,i64, 1 modes); swift `+` (i64,i64, 1 modes)

  - c/op_109 / cpp/op_109 -- **total equality**
  - c/op_109 / go/op_319 -- **total equality**
  - c/op_109 / rust/op_541 -- **total equality**
  - c/op_109 / swift/op_229 -- **core equality, modes differ**
    - only on the left: `in0 + in1 overflows 64 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 + in1 overflows 64 bits (signed)` -> `trap` (branch-to-response)
  - cpp/op_109 / go/op_319 -- **total equality**
  - cpp/op_109 / rust/op_541 -- **total equality**
  - cpp/op_109 / swift/op_229 -- **core equality, modes differ**
    - only on the left: `in0 + in1 overflows 64 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 + in1 overflows 64 bits (signed)` -> `trap` (branch-to-response)
  - go/op_319 / rust/op_541 -- **total equality**
  - go/op_319 / swift/op_229 -- **core equality, modes differ**
    - only on the left: `in0 + in1 overflows 64 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 + in1 overflows 64 bits (signed)` -> `trap` (branch-to-response)
  - rust/op_541 / swift/op_229 -- **core equality, modes differ**
    - only on the left: `in0 + in1 overflows 64 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 + in1 overflows 64 bits (signed)` -> `trap` (branch-to-response)

### shared-core group Sub64(in0:64,in1:64) · (i64,i64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `-` (i64,i64, 1 modes); cpp `-` (i64,i64, 1 modes); go `-` (i64,i64, 1 modes); rust `-` (i64,i64, 1 modes); swift `-` (i64,i64, 1 modes)

  - c/op_145 / cpp/op_145 -- **total equality**
  - c/op_145 / go/op_355 -- **total equality**
  - c/op_145 / rust/op_577 -- **total equality**
  - c/op_145 / swift/op_265 -- **core equality, modes differ**
    - only on the left: `in0 - in1 overflows 64 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 - in1 overflows 64 bits (signed)` -> `trap` (branch-to-response)
  - cpp/op_145 / go/op_355 -- **total equality**
  - cpp/op_145 / rust/op_577 -- **total equality**
  - cpp/op_145 / swift/op_265 -- **core equality, modes differ**
    - only on the left: `in0 - in1 overflows 64 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 - in1 overflows 64 bits (signed)` -> `trap` (branch-to-response)
  - go/op_355 / rust/op_577 -- **total equality**
  - go/op_355 / swift/op_265 -- **core equality, modes differ**
    - only on the left: `in0 - in1 overflows 64 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 - in1 overflows 64 bits (signed)` -> `trap` (branch-to-response)
  - rust/op_577 / swift/op_265 -- **core equality, modes differ**
    - only on the left: `in0 - in1 overflows 64 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 - in1 overflows 64 bits (signed)` -> `trap` (branch-to-response)

### shared-core group Mul64(in0:64,in1:64) · (i64,i64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `*` (i64,i64, 1 modes); cpp `*` (i64,i64, 1 modes); go `*` (i64,i64, 1 modes); rust `*` (i64,i64, 1 modes); swift `*` (i64,i64, 1 modes)

  - c/op_181 / cpp/op_181 -- **total equality**
  - c/op_181 / go/op_67 -- **total equality**
  - c/op_181 / rust/op_613 -- **total equality**
  - c/op_181 / swift/op_121 -- **core equality, modes differ**
    - only on the left: `in1 * in0 overflows 64 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in1 * in0 overflows 64 bits (signed)` -> `trap` (branch-to-response)
  - cpp/op_181 / go/op_67 -- **total equality**
  - cpp/op_181 / rust/op_613 -- **total equality**
  - cpp/op_181 / swift/op_121 -- **core equality, modes differ**
    - only on the left: `in1 * in0 overflows 64 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in1 * in0 overflows 64 bits (signed)` -> `trap` (branch-to-response)
  - go/op_67 / rust/op_613 -- **total equality**
  - go/op_67 / swift/op_121 -- **core equality, modes differ**
    - only on the left: `in1 * in0 overflows 64 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in1 * in0 overflows 64 bits (signed)` -> `trap` (branch-to-response)
  - rust/op_613 / swift/op_121 -- **core equality, modes differ**
    - only on the left: `in1 * in0 overflows 64 bits (signed)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in1 * in0 overflows 64 bits (signed)` -> `trap` (branch-to-response)

### shared-core group Xor64(in0:64,in1:64) · (i64,i64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `^` (i64,i64, 0 modes); cpp `^` (i64,i64, 0 modes); cpp `xor` (i64,i64, 0 modes); go `^` (i64,i64, 0 modes); rust `^` (i64,i64, 0 modes); swift `^` (i64,i64, 0 modes)

  - c/op_397 / cpp/op_397 -- **total equality**
  - c/op_397 / cpp/op_901 -- **total equality**
  - c/op_397 / go/op_427 -- **total equality**
  - c/op_397 / rust/op_217 -- **total equality**
  - c/op_397 / swift/op_661 -- **total equality**
  - cpp/op_397 / go/op_427 -- **total equality**
  - cpp/op_901 / go/op_427 -- **total equality**
  - cpp/op_397 / rust/op_217 -- **total equality**
  - cpp/op_901 / rust/op_217 -- **total equality**
  - cpp/op_397 / swift/op_661 -- **total equality**
  - cpp/op_901 / swift/op_661 -- **total equality**
  - go/op_427 / rust/op_217 -- **total equality**
  - go/op_427 / swift/op_661 -- **total equality**
  - rust/op_217 / swift/op_661 -- **total equality**

### shared-core group And64(in0:64,in1:64) · (i64,i64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `&` (i64,i64, 0 modes); cpp `&` (i64,i64, 0 modes); cpp `bitand` (i64,i64, 0 modes); go `&` (i64,i64, 0 modes); rust `&` (i64,i64, 0 modes); swift `&` (i64,i64, 0 modes)

  - c/op_433 / cpp/op_433 -- **total equality**
  - c/op_433 / cpp/op_937 -- **total equality**
  - c/op_433 / go/op_247 -- **total equality**
  - c/op_433 / rust/op_145 -- **total equality**
  - c/op_433 / swift/op_589 -- **total equality**
  - cpp/op_433 / go/op_247 -- **total equality**
  - cpp/op_937 / go/op_247 -- **total equality**
  - cpp/op_433 / rust/op_145 -- **total equality**
  - cpp/op_937 / rust/op_145 -- **total equality**
  - cpp/op_433 / swift/op_589 -- **total equality**
  - cpp/op_937 / swift/op_589 -- **total equality**
  - go/op_247 / rust/op_145 -- **total equality**
  - go/op_247 / swift/op_589 -- **total equality**
  - rust/op_145 / swift/op_589 -- **total equality**

### shared-core group Or64(in0:64,in1:64) · (i64,i64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `||` (i64,i64, 0 modes); c `|` (i64,i64, 0 modes); cpp `||` (i64,i64, 0 modes); cpp `|` (i64,i64, 0 modes); cpp `or` (i64,i64, 0 modes); cpp `bitor` (i64,i64, 0 modes); go `|` (i64,i64, 0 modes); rust `|` (i64,i64, 0 modes); swift `/` (i64,i64, 2 modes); swift `%` (i64,i64, 2 modes); swift `|` (i64,i64, 0 modes)

  - c/op_289 / cpp/op_289 -- **core difference**
  - c/op_289 / cpp/op_361 -- **core difference**
  - c/op_289 / cpp/op_793 -- **core difference**
  - c/op_289 / cpp/op_865 -- **core difference**
  - c/op_361 / cpp/op_289 -- **core difference**
  - c/op_361 / cpp/op_361 -- **total equality**
  - c/op_361 / cpp/op_793 -- **core difference**
  - c/op_361 / cpp/op_865 -- **total equality**
  - c/op_289 / go/op_391 -- **core difference**
  - c/op_361 / go/op_391 -- **total equality**
  - c/op_289 / rust/op_181 -- **core difference**
  - c/op_361 / rust/op_181 -- **total equality**
  - c/op_289 / swift/op_157 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - c/op_289 / swift/op_193 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - c/op_289 / swift/op_625 -- **core difference**
  - c/op_361 / swift/op_157 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - c/op_361 / swift/op_193 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - c/op_361 / swift/op_625 -- **total equality**
  - cpp/op_289 / go/op_391 -- **core difference**
  - cpp/op_361 / go/op_391 -- **total equality**
  - cpp/op_793 / go/op_391 -- **core difference**
  - cpp/op_865 / go/op_391 -- **total equality**
  - cpp/op_289 / rust/op_181 -- **core difference**
  - cpp/op_361 / rust/op_181 -- **total equality**
  - cpp/op_793 / rust/op_181 -- **core difference**
  - cpp/op_865 / rust/op_181 -- **total equality**
  - cpp/op_289 / swift/op_157 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_289 / swift/op_193 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_289 / swift/op_625 -- **core difference**
  - cpp/op_361 / swift/op_157 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_361 / swift/op_193 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_361 / swift/op_625 -- **total equality**
  - cpp/op_793 / swift/op_157 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_793 / swift/op_193 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_793 / swift/op_625 -- **core difference**
  - cpp/op_865 / swift/op_157 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_865 / swift/op_193 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_865 / swift/op_625 -- **total equality**
  - go/op_391 / rust/op_181 -- **total equality**
  - go/op_391 / swift/op_157 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_391 / swift/op_193 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_391 / swift/op_625 -- **total equality**
  - rust/op_181 / swift/op_157 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_181 / swift/op_193 -- **core difference**
    - only on the right: `in1 == -1` -> `trap` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_181 / swift/op_625 -- **total equality**

### shared-core group Not64(in1:64) · (i64,i64)

- ground: connection
- languages: go, rust
- members: go `&^` (i64,i64, 0 modes); rust `/` (i64,i64, 2 modes); rust `%` (i64,i64, 2 modes)

  - go/op_283 / rust/op_649 -- **core difference**
    - only on the right: `(~in1 | (-9223372036854775808 ^ in0)) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
  - go/op_283 / rust/op_685 -- **core difference**
    - only on the right: `(~in1 | (-9223372036854775808 ^ in0)) == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow` (branch-to-response)
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)

### shared-core group And8(zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (i64,u64)

- ground: connection
- languages: c, cpp
- members: c `&&` (i64,u64, 0 modes); cpp `&&` (i64,u64, 0 modes); cpp `and` (i64,u64, 0 modes)

  - c/op_326 / cpp/op_326 -- **core difference**
  - c/op_326 / cpp/op_830 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,Or64(in0:64,in1:64),0:64,u0:64))) · (i64,u64)

- ground: connection
- languages: c, cpp
- members: c `||` (i64,u64, 0 modes); cpp `||` (i64,u64, 0 modes); cpp `or` (i64,u64, 0 modes)

  - c/op_290 / cpp/op_290 -- **core difference**
  - c/op_290 / cpp/op_794 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(4:64,8:64,in0:64,in1:64,u0:64))) · (i64,u64)

- ground: connection
- languages: c, cpp, swift
- members: c `==` (i64,u64, 1 modes); cpp `==` (i64,u64, 1 modes); swift `==` (i64,u64, 2 modes)

  - c/op_470 / cpp/op_470 -- **core difference**
  - c/op_470 / swift/op_518 -- **core difference**
  - cpp/op_470 / swift/op_518 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,8:64,in0:64,in1:64,u0:64))) · (i64,u64)

- ground: connection
- languages: c, cpp, swift
- members: c `!=` (i64,u64, 1 modes); cpp `!=` (i64,u64, 1 modes); cpp `not_eq` (i64,u64, 1 modes); swift `!=` (i64,u64, 3 modes)

  - c/op_506 / cpp/op_506 -- **core difference**
  - c/op_506 / cpp/op_974 -- **core difference**
  - c/op_506 / swift/op_446 -- **core difference**
  - cpp/op_506 / swift/op_446 -- **core difference**
  - cpp/op_974 / swift/op_446 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,8:64,in0:64,in1:64,u0:64))) · (i64,u64)

- ground: connection
- languages: c, cpp
- members: c `>` (i64,u64, 0 modes); cpp `>` (i64,u64, 0 modes)

  - c/op_542 / cpp/op_542 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,8:64,in0:64,in1:64,u0:64))) · (i64,u64)

- ground: connection
- languages: c, cpp, swift
- members: c `>=` (i64,u64, 1 modes); cpp `>=` (i64,u64, 1 modes); swift `>=` (i64,u64, 2 modes)

  - c/op_578 / cpp/op_578 -- **core difference**
  - c/op_578 / swift/op_410 -- **core difference**
  - cpp/op_578 / swift/op_410 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(6:64,8:64,in0:64,in1:64,u0:64))) · (i64,u64)

- ground: connection
- languages: c, cpp
- members: c `<=` (i64,u64, 0 modes); cpp `<=` (i64,u64, 0 modes)

  - c/op_614 / cpp/op_614 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(2:64,8:64,in0:64,in1:64,u0:64))) · (i64,u64)

- ground: connection
- languages: c, cpp, swift
- members: c `<` (i64,u64, 1 modes); cpp `<` (i64,u64, 1 modes); swift `<` (i64,u64, 2 modes)

  - c/op_650 / cpp/op_650 -- **core difference**
  - c/op_650 / swift/op_302 -- **core difference**
  - cpp/op_650 / swift/op_302 -- **core difference**

### shared-core group ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64)) · (i64,u64)

- ground: connection
- languages: c, cpp
- members: c `/` (i64,u64, 0 modes); c `%` (i64,u64, 0 modes); cpp `/` (i64,u64, 0 modes); cpp `%` (i64,u64, 0 modes)

  - c/op_218 / cpp/op_218 -- **total equality**
  - c/op_218 / cpp/op_254 -- **core difference**
  - c/op_254 / cpp/op_218 -- **core difference**
  - c/op_254 / cpp/op_254 -- **total equality**

### shared-core group Shl64(in0:64,And8(63:8,ex8@0(in1:64))) · (i64,u64)

- ground: connection
- languages: c, cpp, go, rust
- members: c `<<` (i64,u64, 1 modes); cpp `<<` (i64,u64, 1 modes); go `<<` (i64,u64, 3 modes); rust `<<` (i64,u64, 1 modes)

  - c/op_686 / cpp/op_686 -- **total equality**
  - c/op_686 / go/op_176 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - c/op_686 / rust/op_470 -- **total equality**
  - cpp/op_686 / go/op_176 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - cpp/op_686 / rust/op_470 -- **total equality**
  - go/op_176 / rust/op_470 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)

### shared-core group Sar64(in0:64,And8(63:8,ex8@0(in1:64))) · (i64,u64)

- ground: connection
- languages: c, cpp, rust
- members: c `>>` (i64,u64, 0 modes); cpp `>>` (i64,u64, 0 modes); rust `>>` (i64,u64, 0 modes)

  - c/op_722 / cpp/op_722 -- **total equality**
  - c/op_722 / rust/op_506 -- **total equality**
  - cpp/op_722 / rust/op_506 -- **total equality**

### shared-core group And8(63:8,ex8@0(in1:64)) · (i64,u64)

- ground: connection
- languages: c, cpp, go, rust
- members: c `<<` (i64,u64, 1 modes); c `>>` (i64,u64, 0 modes); cpp `<<` (i64,u64, 1 modes); cpp `>>` (i64,u64, 0 modes); go `<<` (i64,u64, 3 modes); rust `<<` (i64,u64, 1 modes); rust `>>` (i64,u64, 0 modes)

  - c/op_686 / cpp/op_686 -- **total equality**
  - c/op_686 / cpp/op_722 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_722 / cpp/op_686 -- **core difference**
    - only on the right: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_722 / cpp/op_722 -- **total equality**
  - c/op_686 / go/op_176 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - c/op_722 / go/op_176 -- **core difference**
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - c/op_686 / rust/op_470 -- **total equality**
  - c/op_686 / rust/op_506 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_722 / rust/op_470 -- **core difference**
    - only on the right: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - c/op_722 / rust/op_506 -- **total equality**
  - cpp/op_686 / go/op_176 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - cpp/op_722 / go/op_176 -- **core difference**
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - cpp/op_686 / rust/op_470 -- **total equality**
  - cpp/op_686 / rust/op_506 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - cpp/op_722 / rust/op_470 -- **core difference**
    - only on the right: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - cpp/op_722 / rust/op_506 -- **total equality**
  - go/op_176 / rust/op_470 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - go/op_176 / rust/op_506 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)

### shared-core group Add64(in0:64,in1:64) · (i64,u64)

- ground: connection
- languages: c, cpp
- members: c `+` (i64,u64, 0 modes); cpp `+` (i64,u64, 0 modes)

  - c/op_110 / cpp/op_110 -- **total equality**

### shared-core group Sub64(in0:64,in1:64) · (i64,u64)

- ground: connection
- languages: c, cpp
- members: c `-` (i64,u64, 0 modes); cpp `-` (i64,u64, 0 modes)

  - c/op_146 / cpp/op_146 -- **total equality**

### shared-core group Mul64(in0:64,in1:64) · (i64,u64)

- ground: connection
- languages: c, cpp
- members: c `*` (i64,u64, 0 modes); cpp `*` (i64,u64, 0 modes)

  - c/op_182 / cpp/op_182 -- **total equality**

### shared-core group Xor64(in0:64,in1:64) · (i64,u64)

- ground: connection
- languages: c, cpp
- members: c `^` (i64,u64, 0 modes); cpp `^` (i64,u64, 0 modes); cpp `xor` (i64,u64, 0 modes)

  - c/op_398 / cpp/op_398 -- **total equality**
  - c/op_398 / cpp/op_902 -- **total equality**

### shared-core group And64(in0:64,in1:64) · (i64,u64)

- ground: connection
- languages: c, cpp
- members: c `&` (i64,u64, 0 modes); cpp `&` (i64,u64, 0 modes); cpp `bitand` (i64,u64, 0 modes)

  - c/op_434 / cpp/op_434 -- **total equality**
  - c/op_434 / cpp/op_938 -- **total equality**

### shared-core group Or64(in0:64,in1:64) · (i64,u64)

- ground: connection
- languages: c, cpp
- members: c `||` (i64,u64, 0 modes); c `|` (i64,u64, 0 modes); cpp `||` (i64,u64, 0 modes); cpp `|` (i64,u64, 0 modes); cpp `or` (i64,u64, 0 modes); cpp `bitor` (i64,u64, 0 modes)

  - c/op_290 / cpp/op_290 -- **core difference**
  - c/op_290 / cpp/op_362 -- **core difference**
  - c/op_290 / cpp/op_794 -- **core difference**
  - c/op_290 / cpp/op_866 -- **core difference**
  - c/op_362 / cpp/op_290 -- **core difference**
  - c/op_362 / cpp/op_362 -- **total equality**
  - c/op_362 / cpp/op_794 -- **core difference**
  - c/op_362 / cpp/op_866 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(4:64,20:64,in0:64,0:64,u0:64))) · (u64,None)

- ground: connection
- languages: c, cpp
- members: c `!` (u64,None, 0 modes); cpp `!` (u64,None, 0 modes); cpp `not` (u64,None, 0 modes)

  - c/op_2 / cpp/op_2 -- **core difference**
  - c/op_2 / cpp/op_26 -- **core difference**

### shared-core group st64(Add64(18446744073709551608:64,SP:64))=in0:64 · (u64,None)

- ground: connection
- languages: c, cpp
- members: c `&` (u64,None, 0 modes); cpp `&` (u64,None, 0 modes)

  - c/op_32 / cpp/op_44 -- **total equality**

### shared-core group Add64(18446744073709551615:64,in0:64) · (u64,None)

- ground: connection
- languages: c, cpp
- members: c `--` (u64,None, 0 modes); cpp `--` (u64,None, 0 modes)

  - c/op_44 / cpp/op_56 -- **total equality**

### shared-core group Sub64(0:64,in0:64) · (u64,None)

- ground: connection
- languages: c, cpp, go
- members: c `-` (u64,None, 0 modes); cpp `-` (u64,None, 0 modes); go `-` (u64,None, 0 modes)

  - c/op_14 / cpp/op_14 -- **total equality**
  - c/op_14 / go/op_8 -- **total equality**
  - cpp/op_14 / go/op_8 -- **total equality**

### shared-core group Add64(1:64,in0:64) · (u64,None)

- ground: connection
- languages: c, cpp
- members: c `++` (u64,None, 0 modes); cpp `++` (u64,None, 0 modes)

  - c/op_38 / cpp/op_50 -- **total equality**

### shared-core group Not64(in0:64) · (u64,None)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `~` (u64,None, 0 modes); cpp `compl` (u64,None, 0 modes); cpp `~` (u64,None, 0 modes); go `^` (u64,None, 0 modes); rust `!` (u64,None, 0 modes); swift `~` (u64,None, 0 modes)

  - c/op_8 / cpp/op_32 -- **total equality**
  - c/op_8 / cpp/op_8 -- **total equality**
  - c/op_8 / go/op_20 -- **total equality**
  - c/op_8 / rust/op_14 -- **total equality**
  - c/op_8 / swift/op_38 -- **total equality**
  - cpp/op_32 / go/op_20 -- **total equality**
  - cpp/op_8 / go/op_20 -- **total equality**
  - cpp/op_32 / rust/op_14 -- **total equality**
  - cpp/op_8 / rust/op_14 -- **total equality**
  - cpp/op_32 / swift/op_38 -- **total equality**
  - cpp/op_8 / swift/op_38 -- **total equality**
  - go/op_20 / rust/op_14 -- **total equality**
  - go/op_20 / swift/op_38 -- **total equality**
  - rust/op_14 / swift/op_38 -- **total equality**

### shared-core group ite(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64)),in0:64,0:64) · (u64,bool)

- ground: connection
- languages: c, cpp
- members: c `*` (u64,bool, 0 modes); cpp `*` (u64,bool, 0 modes)

  - c/op_191 / cpp/op_191 -- **total equality**

### shared-core group And8(ex8@0(in1:64),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64)))) · (u64,bool)

- ground: connection
- languages: c, cpp
- members: c `&&` (u64,bool, 0 modes); cpp `&&` (u64,bool, 0 modes); cpp `and` (u64,bool, 0 modes)

  - c/op_335 / cpp/op_335 -- **core difference**
  - c/op_335 / cpp/op_839 -- **core difference**

### shared-core group And8(ex8@0(in1:64),zx8(ex1@0(amd64g_calculate_condition(4:64,20:64,in0:64,0:64,u0:64)))) · (u64,bool)

- ground: connection
- languages: c, cpp
- members: c `<` (u64,bool, 0 modes); cpp `<` (u64,bool, 0 modes)

  - c/op_659 / cpp/op_659 -- **core difference**

### shared-core group Or8(ex8@0(in1:64),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64)))) · (u64,bool)

- ground: connection
- languages: c, cpp
- members: c `||` (u64,bool, 0 modes); cpp `||` (u64,bool, 0 modes); cpp `or` (u64,bool, 0 modes)

  - c/op_299 / cpp/op_299 -- **core difference**
  - c/op_299 / cpp/op_803 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(4:64,8:64,in0:64,zx64(ex32@0(in1:64)),u0:64))) · (u64,bool)

- ground: connection
- languages: c, cpp
- members: c `==` (u64,bool, 1 modes); cpp `==` (u64,bool, 1 modes)

  - c/op_479 / cpp/op_479 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,8:64,in0:64,zx64(ex32@0(in1:64)),u0:64))) · (u64,bool)

- ground: connection
- languages: c, cpp
- members: c `!=` (u64,bool, 2 modes); cpp `!=` (u64,bool, 1 modes); cpp `not_eq` (u64,bool, 1 modes)

  - c/op_515 / cpp/op_515 -- **core difference**
  - c/op_515 / cpp/op_983 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,8:64,in0:64,zx64(ex32@0(in1:64)),u0:64))) · (u64,bool)

- ground: connection
- languages: c, cpp
- members: c `>` (u64,bool, 1 modes); cpp `>` (u64,bool, 1 modes)

  - c/op_551 / cpp/op_551 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,8:64,in0:64,zx64(ex32@0(in1:64)),u0:64))) · (u64,bool)

- ground: connection
- languages: c, cpp
- members: c `>=` (u64,bool, 1 modes); cpp `>=` (u64,bool, 1 modes)

  - c/op_587 / cpp/op_587 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(6:64,8:64,in0:64,zx64(ex32@0(in1:64)),u0:64))) · (u64,bool)

- ground: connection
- languages: c, cpp
- members: c `<=` (u64,bool, 1 modes); cpp `<=` (u64,bool, 1 modes)

  - c/op_623 / cpp/op_623 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64))) · (u64,bool)

- ground: connection
- languages: c, cpp
- members: c `||` (u64,bool, 0 modes); c `&&` (u64,bool, 0 modes); cpp `||` (u64,bool, 0 modes); cpp `&&` (u64,bool, 0 modes); cpp `or` (u64,bool, 0 modes); cpp `and` (u64,bool, 0 modes)

  - c/op_299 / cpp/op_299 -- **core difference**
  - c/op_299 / cpp/op_335 -- **core difference**
  - c/op_299 / cpp/op_803 -- **core difference**
  - c/op_299 / cpp/op_839 -- **core difference**
  - c/op_335 / cpp/op_299 -- **core difference**
  - c/op_335 / cpp/op_335 -- **core difference**
  - c/op_335 / cpp/op_803 -- **core difference**
  - c/op_335 / cpp/op_839 -- **core difference**

### shared-core group zx64(And32(ex32@0(in0:64),ex32@0(in1:64))) · (u64,bool)

- ground: connection
- languages: c, cpp
- members: c `&` (u64,bool, 0 modes); cpp `&` (u64,bool, 0 modes); cpp `bitand` (u64,bool, 0 modes)

  - c/op_443 / cpp/op_443 -- **total equality**
  - c/op_443 / cpp/op_947 -- **total equality**

### shared-core group Shl64(in0:64,And8(63:8,ex8@0(in1:64))) · (u64,bool)

- ground: connection
- languages: c, cpp
- members: c `<<` (u64,bool, 0 modes); cpp `<<` (u64,bool, 0 modes)

  - c/op_695 / cpp/op_695 -- **total equality**

### shared-core group Shr64(in0:64,And8(63:8,ex8@0(in1:64))) · (u64,bool)

- ground: connection
- languages: c, cpp
- members: c `>>` (u64,bool, 0 modes); cpp `>>` (u64,bool, 0 modes)

  - c/op_731 / cpp/op_731 -- **total equality**

### shared-core group Add64(in0:64,zx64(ex32@0(in1:64))) · (u64,bool)

- ground: connection
- languages: c, cpp
- members: c `+` (u64,bool, 0 modes); cpp `+` (u64,bool, 0 modes)

  - c/op_119 / cpp/op_119 -- **total equality**

### shared-core group Sub64(in0:64,zx64(ex32@0(in1:64))) · (u64,bool)

- ground: connection
- languages: c, cpp
- members: c `-` (u64,bool, 0 modes); cpp `-` (u64,bool, 0 modes)

  - c/op_155 / cpp/op_155 -- **total equality**

### shared-core group Xor64(in0:64,zx64(ex32@0(in1:64))) · (u64,bool)

- ground: connection
- languages: c, cpp
- members: c `^` (u64,bool, 0 modes); cpp `^` (u64,bool, 0 modes); cpp `xor` (u64,bool, 0 modes)

  - c/op_407 / cpp/op_407 -- **total equality**
  - c/op_407 / cpp/op_911 -- **total equality**

### shared-core group Or64(in0:64,zx64(ex32@0(in1:64))) · (u64,bool)

- ground: connection
- languages: c, cpp
- members: c `|` (u64,bool, 0 modes); cpp `|` (u64,bool, 0 modes); cpp `bitor` (u64,bool, 0 modes)

  - c/op_371 / cpp/op_371 -- **total equality**
  - c/op_371 / cpp/op_875 -- **total equality**

### shared-core group And8(63:8,ex8@0(in1:64)) · (u64,bool)

- ground: connection
- languages: c, cpp
- members: c `<<` (u64,bool, 0 modes); c `>>` (u64,bool, 0 modes); cpp `<<` (u64,bool, 0 modes); cpp `>>` (u64,bool, 0 modes)

  - c/op_695 / cpp/op_695 -- **total equality**
  - c/op_695 / cpp/op_731 -- **core difference**
  - c/op_731 / cpp/op_695 -- **core difference**
  - c/op_731 / cpp/op_731 -- **total equality**

### shared-core group ins@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64))))))),Add32F0x4(ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64)))))))),ex128@0(ins@0(u1:256,F64toF32(And32(3:32,ex32@0(u2:64)),I64StoF64(And32(3:32,ex32@0(u2:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64)))))))))) · (u64,f32)

- ground: connection
- languages: c, cpp
- members: c `+` (u64,f32, 0 modes); c `*` (u64,f32, 0 modes); cpp `+` (u64,f32, 0 modes); cpp `*` (u64,f32, 0 modes)

  - c/op_117 / cpp/op_117 -- **total equality**
  - c/op_117 / cpp/op_189 -- **core difference**
  - c/op_189 / cpp/op_117 -- **core difference**
  - c/op_189 / cpp/op_189 -- **total equality**

### shared-core group ins@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64))))))),Add32F0x4(ex128@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64)))))))),ex128@0(ins@0(u2:256,F64toF32(And32(3:32,ex32@0(u1:64)),I64StoF64(And32(3:32,ex32@0(u1:64)),Or64(Shr64(in0:64,1:8),zx64(And32(1:32,ex32@0(in0:64)))))))))) · (u64,f32)

- ground: connection
- languages: c, cpp
- members: c `-` (u64,f32, 0 modes); c `/` (u64,f32, 0 modes); c `==` (u64,f32, 0 modes); c `!=` (u64,f32, 0 modes); c `>` (u64,f32, 0 modes); c `>=` (u64,f32, 0 modes); c `<=` (u64,f32, 0 modes); c `<` (u64,f32, 0 modes); cpp `-` (u64,f32, 0 modes); cpp `/` (u64,f32, 0 modes); cpp `==` (u64,f32, 0 modes); cpp `!=` (u64,f32, 0 modes); cpp `>` (u64,f32, 0 modes); cpp `>=` (u64,f32, 0 modes); cpp `<=` (u64,f32, 0 modes); cpp `<` (u64,f32, 0 modes); cpp `<=>` (u64,f32, 0 modes); cpp `not_eq` (u64,f32, 0 modes)

  - c/op_153 / cpp/op_153 -- **total equality**
  - c/op_153 / cpp/op_225 -- **core difference**
  - c/op_153 / cpp/op_477 -- **core difference**
  - c/op_153 / cpp/op_513 -- **core difference**
  - c/op_153 / cpp/op_549 -- **core difference**
  - c/op_153 / cpp/op_585 -- **core difference**
  - c/op_153 / cpp/op_621 -- **core difference**
  - c/op_153 / cpp/op_657 -- **core difference**
  - c/op_153 / cpp/op_765 -- **core difference**
  - c/op_153 / cpp/op_981 -- **core difference**
  - c/op_225 / cpp/op_153 -- **core difference**
  - c/op_225 / cpp/op_225 -- **total equality**
  - c/op_225 / cpp/op_477 -- **core difference**
  - c/op_225 / cpp/op_513 -- **core difference**
  - c/op_225 / cpp/op_549 -- **core difference**
  - c/op_225 / cpp/op_585 -- **core difference**
  - c/op_225 / cpp/op_621 -- **core difference**
  - c/op_225 / cpp/op_657 -- **core difference**
  - c/op_225 / cpp/op_765 -- **core difference**
  - c/op_225 / cpp/op_981 -- **core difference**
  - c/op_477 / cpp/op_153 -- **core difference**
  - c/op_477 / cpp/op_225 -- **core difference**
  - c/op_477 / cpp/op_477 -- **total equality**
  - c/op_477 / cpp/op_513 -- **core difference**
  - c/op_477 / cpp/op_549 -- **core difference**
  - c/op_477 / cpp/op_585 -- **core difference**
  - c/op_477 / cpp/op_621 -- **core difference**
  - c/op_477 / cpp/op_657 -- **core difference**
  - c/op_477 / cpp/op_765 -- **core difference**
  - c/op_477 / cpp/op_981 -- **core difference**
  - c/op_513 / cpp/op_153 -- **core difference**
  - c/op_513 / cpp/op_225 -- **core difference**
  - c/op_513 / cpp/op_477 -- **core difference**
  - c/op_513 / cpp/op_513 -- **total equality**
  - c/op_513 / cpp/op_549 -- **core difference**
  - c/op_513 / cpp/op_585 -- **core difference**
  - c/op_513 / cpp/op_621 -- **core difference**
  - c/op_513 / cpp/op_657 -- **core difference**
  - c/op_513 / cpp/op_765 -- **core difference**
  - c/op_513 / cpp/op_981 -- **total equality**
  - c/op_549 / cpp/op_153 -- **core difference**
  - c/op_549 / cpp/op_225 -- **core difference**
  - c/op_549 / cpp/op_477 -- **core difference**
  - c/op_549 / cpp/op_513 -- **core difference**
  - c/op_549 / cpp/op_549 -- **core difference**
  - c/op_549 / cpp/op_585 -- **core difference**
  - c/op_549 / cpp/op_621 -- **core difference**
  - c/op_549 / cpp/op_657 -- **core difference**
  - c/op_549 / cpp/op_765 -- **core difference**
  - c/op_549 / cpp/op_981 -- **core difference**
  - c/op_585 / cpp/op_153 -- **core difference**
  - c/op_585 / cpp/op_225 -- **core difference**
  - c/op_585 / cpp/op_477 -- **core difference**
  - c/op_585 / cpp/op_513 -- **core difference**
  - c/op_585 / cpp/op_549 -- **core difference**
  - c/op_585 / cpp/op_585 -- **core difference**
  - c/op_585 / cpp/op_621 -- **core difference**
  - c/op_585 / cpp/op_657 -- **core difference**
  - c/op_585 / cpp/op_765 -- **core difference**
  - c/op_585 / cpp/op_981 -- **core difference**
  - c/op_621 / cpp/op_153 -- **core difference**
  - c/op_621 / cpp/op_225 -- **core difference**
  - c/op_621 / cpp/op_477 -- **core difference**
  - c/op_621 / cpp/op_513 -- **core difference**
  - c/op_621 / cpp/op_549 -- **core difference**
  - c/op_621 / cpp/op_585 -- **core difference**
  - c/op_621 / cpp/op_621 -- **core difference**
  - c/op_621 / cpp/op_657 -- **core difference**
  - c/op_621 / cpp/op_765 -- **core difference**
  - c/op_621 / cpp/op_981 -- **core difference**
  - c/op_657 / cpp/op_153 -- **core difference**
  - c/op_657 / cpp/op_225 -- **core difference**
  - c/op_657 / cpp/op_477 -- **core difference**
  - c/op_657 / cpp/op_513 -- **core difference**
  - c/op_657 / cpp/op_549 -- **core difference**
  - c/op_657 / cpp/op_585 -- **core difference**
  - c/op_657 / cpp/op_621 -- **core difference**
  - c/op_657 / cpp/op_657 -- **core difference**
  - c/op_657 / cpp/op_765 -- **core difference**
  - c/op_657 / cpp/op_981 -- **core difference**

### shared-core group And8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64)))) · (u64,f32)

- ground: connection
- languages: c, cpp
- members: c `&&` (u64,f32, 0 modes); cpp `&&` (u64,f32, 0 modes); cpp `and` (u64,f32, 0 modes)

  - c/op_333 / cpp/op_333 -- **core difference**
  - c/op_333 / cpp/op_837 -- **core difference**

### shared-core group Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64)))) · (u64,f32)

- ground: connection
- languages: c, cpp
- members: c `||` (u64,f32, 0 modes); cpp `||` (u64,f32, 0 modes); cpp `or` (u64,f32, 0 modes)

  - c/op_297 / cpp/op_297 -- **core difference**
  - c/op_297 / cpp/op_801 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),F32toF64(0:32)))),0:64,u0:64)))) · (u64,f32)

- ground: connection
- languages: c, cpp
- members: c `||` (u64,f32, 0 modes); c `&&` (u64,f32, 0 modes); cpp `||` (u64,f32, 0 modes); cpp `&&` (u64,f32, 0 modes); cpp `or` (u64,f32, 0 modes); cpp `and` (u64,f32, 0 modes)

  - c/op_297 / cpp/op_297 -- **core difference**
  - c/op_297 / cpp/op_333 -- **core difference**
  - c/op_297 / cpp/op_801 -- **core difference**
  - c/op_297 / cpp/op_837 -- **core difference**
  - c/op_333 / cpp/op_297 -- **core difference**
  - c/op_333 / cpp/op_333 -- **core difference**
  - c/op_333 / cpp/op_801 -- **core difference**
  - c/op_333 / cpp/op_837 -- **core difference**

### shared-core group ex1@0(amd64g_calculate_condition(8:64,20:64,in0:64,0:64,u0:64)) · (u64,f32)

- ground: connection
- languages: c, cpp
- members: c `+` (u64,f32, 0 modes); c `-` (u64,f32, 0 modes); c `*` (u64,f32, 0 modes); c `/` (u64,f32, 0 modes); c `==` (u64,f32, 0 modes); c `!=` (u64,f32, 0 modes); c `>` (u64,f32, 0 modes); c `>=` (u64,f32, 0 modes); c `<=` (u64,f32, 0 modes); c `<` (u64,f32, 0 modes); cpp `+` (u64,f32, 0 modes); cpp `-` (u64,f32, 0 modes); cpp `*` (u64,f32, 0 modes); cpp `/` (u64,f32, 0 modes); cpp `==` (u64,f32, 0 modes); cpp `!=` (u64,f32, 0 modes); cpp `>` (u64,f32, 0 modes); cpp `>=` (u64,f32, 0 modes); cpp `<=` (u64,f32, 0 modes); cpp `<` (u64,f32, 0 modes); cpp `<=>` (u64,f32, 0 modes); cpp `not_eq` (u64,f32, 0 modes)

  - c/op_117 / cpp/op_117 -- **total equality**
  - c/op_117 / cpp/op_153 -- **core difference**
  - c/op_117 / cpp/op_189 -- **core difference**
  - c/op_117 / cpp/op_225 -- **core difference**
  - c/op_117 / cpp/op_477 -- **core difference**
  - c/op_117 / cpp/op_513 -- **core difference**
  - c/op_117 / cpp/op_549 -- **core difference**
  - c/op_117 / cpp/op_585 -- **core difference**
  - c/op_117 / cpp/op_621 -- **core difference**
  - c/op_117 / cpp/op_657 -- **core difference**
  - c/op_117 / cpp/op_765 -- **core difference**
  - c/op_117 / cpp/op_981 -- **core difference**
  - c/op_153 / cpp/op_117 -- **core difference**
  - c/op_153 / cpp/op_153 -- **total equality**
  - c/op_153 / cpp/op_189 -- **core difference**
  - c/op_153 / cpp/op_225 -- **core difference**
  - c/op_153 / cpp/op_477 -- **core difference**
  - c/op_153 / cpp/op_513 -- **core difference**
  - c/op_153 / cpp/op_549 -- **core difference**
  - c/op_153 / cpp/op_585 -- **core difference**
  - c/op_153 / cpp/op_621 -- **core difference**
  - c/op_153 / cpp/op_657 -- **core difference**
  - c/op_153 / cpp/op_765 -- **core difference**
  - c/op_153 / cpp/op_981 -- **core difference**
  - c/op_189 / cpp/op_117 -- **core difference**
  - c/op_189 / cpp/op_153 -- **core difference**
  - c/op_189 / cpp/op_189 -- **total equality**
  - c/op_189 / cpp/op_225 -- **core difference**
  - c/op_189 / cpp/op_477 -- **core difference**
  - c/op_189 / cpp/op_513 -- **core difference**
  - c/op_189 / cpp/op_549 -- **core difference**
  - c/op_189 / cpp/op_585 -- **core difference**
  - c/op_189 / cpp/op_621 -- **core difference**
  - c/op_189 / cpp/op_657 -- **core difference**
  - c/op_189 / cpp/op_765 -- **core difference**
  - c/op_189 / cpp/op_981 -- **core difference**
  - c/op_225 / cpp/op_117 -- **core difference**
  - c/op_225 / cpp/op_153 -- **core difference**
  - c/op_225 / cpp/op_189 -- **core difference**
  - c/op_225 / cpp/op_225 -- **total equality**
  - c/op_225 / cpp/op_477 -- **core difference**
  - c/op_225 / cpp/op_513 -- **core difference**
  - c/op_225 / cpp/op_549 -- **core difference**
  - c/op_225 / cpp/op_585 -- **core difference**
  - c/op_225 / cpp/op_621 -- **core difference**
  - c/op_225 / cpp/op_657 -- **core difference**
  - c/op_225 / cpp/op_765 -- **core difference**
  - c/op_225 / cpp/op_981 -- **core difference**
  - c/op_477 / cpp/op_117 -- **core difference**
  - c/op_477 / cpp/op_153 -- **core difference**
  - c/op_477 / cpp/op_189 -- **core difference**
  - c/op_477 / cpp/op_225 -- **core difference**
  - c/op_477 / cpp/op_477 -- **total equality**
  - c/op_477 / cpp/op_513 -- **core difference**
  - c/op_477 / cpp/op_549 -- **core difference**
  - c/op_477 / cpp/op_585 -- **core difference**
  - c/op_477 / cpp/op_621 -- **core difference**
  - c/op_477 / cpp/op_657 -- **core difference**
  - c/op_477 / cpp/op_765 -- **core difference**
  - c/op_477 / cpp/op_981 -- **core difference**
  - c/op_513 / cpp/op_117 -- **core difference**
  - c/op_513 / cpp/op_153 -- **core difference**
  - c/op_513 / cpp/op_189 -- **core difference**
  - c/op_513 / cpp/op_225 -- **core difference**
  - c/op_513 / cpp/op_477 -- **core difference**
  - c/op_513 / cpp/op_513 -- **total equality**
  - c/op_513 / cpp/op_549 -- **core difference**
  - c/op_513 / cpp/op_585 -- **core difference**
  - c/op_513 / cpp/op_621 -- **core difference**
  - c/op_513 / cpp/op_657 -- **core difference**
  - c/op_513 / cpp/op_765 -- **core difference**
  - c/op_513 / cpp/op_981 -- **total equality**
  - c/op_549 / cpp/op_117 -- **core difference**
  - c/op_549 / cpp/op_153 -- **core difference**
  - c/op_549 / cpp/op_189 -- **core difference**
  - c/op_549 / cpp/op_225 -- **core difference**
  - c/op_549 / cpp/op_477 -- **core difference**
  - c/op_549 / cpp/op_513 -- **core difference**
  - c/op_549 / cpp/op_549 -- **core difference**
  - c/op_549 / cpp/op_585 -- **core difference**
  - c/op_549 / cpp/op_621 -- **core difference**
  - c/op_549 / cpp/op_657 -- **core difference**
  - c/op_549 / cpp/op_765 -- **core difference**
  - c/op_549 / cpp/op_981 -- **core difference**
  - c/op_585 / cpp/op_117 -- **core difference**
  - c/op_585 / cpp/op_153 -- **core difference**
  - c/op_585 / cpp/op_189 -- **core difference**
  - c/op_585 / cpp/op_225 -- **core difference**
  - c/op_585 / cpp/op_477 -- **core difference**
  - c/op_585 / cpp/op_513 -- **core difference**
  - c/op_585 / cpp/op_549 -- **core difference**
  - c/op_585 / cpp/op_585 -- **core difference**
  - c/op_585 / cpp/op_621 -- **core difference**
  - c/op_585 / cpp/op_657 -- **core difference**
  - c/op_585 / cpp/op_765 -- **core difference**
  - c/op_585 / cpp/op_981 -- **core difference**
  - c/op_621 / cpp/op_117 -- **core difference**
  - c/op_621 / cpp/op_153 -- **core difference**
  - c/op_621 / cpp/op_189 -- **core difference**
  - c/op_621 / cpp/op_225 -- **core difference**
  - c/op_621 / cpp/op_477 -- **core difference**
  - c/op_621 / cpp/op_513 -- **core difference**
  - c/op_621 / cpp/op_549 -- **core difference**
  - c/op_621 / cpp/op_585 -- **core difference**
  - c/op_621 / cpp/op_621 -- **core difference**
  - c/op_621 / cpp/op_657 -- **core difference**
  - c/op_621 / cpp/op_765 -- **core difference**
  - c/op_621 / cpp/op_981 -- **core difference**
  - c/op_657 / cpp/op_117 -- **core difference**
  - c/op_657 / cpp/op_153 -- **core difference**
  - c/op_657 / cpp/op_189 -- **core difference**
  - c/op_657 / cpp/op_225 -- **core difference**
  - c/op_657 / cpp/op_477 -- **core difference**
  - c/op_657 / cpp/op_513 -- **core difference**
  - c/op_657 / cpp/op_549 -- **core difference**
  - c/op_657 / cpp/op_585 -- **core difference**
  - c/op_657 / cpp/op_621 -- **core difference**
  - c/op_657 / cpp/op_657 -- **core difference**
  - c/op_657 / cpp/op_765 -- **core difference**
  - c/op_657 / cpp/op_981 -- **core difference**

### shared-core group F32toF64(ex32@0(in1:256)) · (u64,f32)

- ground: connection
- languages: c, cpp
- members: c `||` (u64,f32, 0 modes); c `&&` (u64,f32, 0 modes); c `>` (u64,f32, 0 modes); c `>=` (u64,f32, 0 modes); c `<=` (u64,f32, 0 modes); c `<` (u64,f32, 0 modes); cpp `||` (u64,f32, 0 modes); cpp `&&` (u64,f32, 0 modes); cpp `>` (u64,f32, 0 modes); cpp `>=` (u64,f32, 0 modes); cpp `<=` (u64,f32, 0 modes); cpp `<` (u64,f32, 0 modes); cpp `<=>` (u64,f32, 0 modes); cpp `or` (u64,f32, 0 modes); cpp `and` (u64,f32, 0 modes)

  - c/op_297 / cpp/op_297 -- **core difference**
  - c/op_297 / cpp/op_333 -- **core difference**
  - c/op_297 / cpp/op_549 -- **core difference**
  - c/op_297 / cpp/op_585 -- **core difference**
  - c/op_297 / cpp/op_621 -- **core difference**
  - c/op_297 / cpp/op_657 -- **core difference**
  - c/op_297 / cpp/op_765 -- **core difference**
  - c/op_297 / cpp/op_801 -- **core difference**
  - c/op_297 / cpp/op_837 -- **core difference**
  - c/op_333 / cpp/op_297 -- **core difference**
  - c/op_333 / cpp/op_333 -- **core difference**
  - c/op_333 / cpp/op_549 -- **core difference**
  - c/op_333 / cpp/op_585 -- **core difference**
  - c/op_333 / cpp/op_621 -- **core difference**
  - c/op_333 / cpp/op_657 -- **core difference**
  - c/op_333 / cpp/op_765 -- **core difference**
  - c/op_333 / cpp/op_801 -- **core difference**
  - c/op_333 / cpp/op_837 -- **core difference**
  - c/op_549 / cpp/op_297 -- **core difference**
  - c/op_549 / cpp/op_333 -- **core difference**
  - c/op_549 / cpp/op_549 -- **core difference**
  - c/op_549 / cpp/op_585 -- **core difference**
  - c/op_549 / cpp/op_621 -- **core difference**
  - c/op_549 / cpp/op_657 -- **core difference**
  - c/op_549 / cpp/op_765 -- **core difference**
  - c/op_549 / cpp/op_801 -- **core difference**
  - c/op_549 / cpp/op_837 -- **core difference**
  - c/op_585 / cpp/op_297 -- **core difference**
  - c/op_585 / cpp/op_333 -- **core difference**
  - c/op_585 / cpp/op_549 -- **core difference**
  - c/op_585 / cpp/op_585 -- **core difference**
  - c/op_585 / cpp/op_621 -- **core difference**
  - c/op_585 / cpp/op_657 -- **core difference**
  - c/op_585 / cpp/op_765 -- **core difference**
  - c/op_585 / cpp/op_801 -- **core difference**
  - c/op_585 / cpp/op_837 -- **core difference**
  - c/op_621 / cpp/op_297 -- **core difference**
  - c/op_621 / cpp/op_333 -- **core difference**
  - c/op_621 / cpp/op_549 -- **core difference**
  - c/op_621 / cpp/op_585 -- **core difference**
  - c/op_621 / cpp/op_621 -- **core difference**
  - c/op_621 / cpp/op_657 -- **core difference**
  - c/op_621 / cpp/op_765 -- **core difference**
  - c/op_621 / cpp/op_801 -- **core difference**
  - c/op_621 / cpp/op_837 -- **core difference**
  - c/op_657 / cpp/op_297 -- **core difference**
  - c/op_657 / cpp/op_333 -- **core difference**
  - c/op_657 / cpp/op_549 -- **core difference**
  - c/op_657 / cpp/op_585 -- **core difference**
  - c/op_657 / cpp/op_621 -- **core difference**
  - c/op_657 / cpp/op_657 -- **core difference**
  - c/op_657 / cpp/op_765 -- **core difference**
  - c/op_657 / cpp/op_801 -- **core difference**
  - c/op_657 / cpp/op_837 -- **core difference**

### shared-core group zx64(And32(1:32,ex32@0(ins@0(ins@0(u0:256,Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),CmpEQ64F0x2(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex128@0(in1:256)))))) · (u64,f64)

- ground: connection
- languages: c, cpp
- members: c `==` (u64,f64, 0 modes); cpp `==` (u64,f64, 0 modes)

  - c/op_478 / cpp/op_478 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),ex64@0(in1:256)))),0:64,u0:64))) · (u64,f64)

- ground: connection
- languages: c, cpp
- members: c `>` (u64,f64, 0 modes); cpp `>` (u64,f64, 0 modes)

  - c/op_550 / cpp/op_550 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),ex64@0(in1:256)))),0:64,u0:64))) · (u64,f64)

- ground: connection
- languages: c, cpp
- members: c `>=` (u64,f64, 0 modes); cpp `>=` (u64,f64, 0 modes)

  - c/op_586 / cpp/op_586 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))))))),0:64,u0:64))) · (u64,f64)

- ground: connection
- languages: c, cpp
- members: c `<=` (u64,f64, 0 modes); cpp `<=` (u64,f64, 0 modes)

  - c/op_622 / cpp/op_622 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))))))),0:64,u0:64))) · (u64,f64)

- ground: connection
- languages: c, cpp
- members: c `<` (u64,f64, 0 modes); cpp `<` (u64,f64, 0 modes)

  - c/op_658 / cpp/op_658 -- **core difference**

### shared-core group zx64(And32(1:32,ex32@0(XorV128(18446744073709551615:128,CmpEQ64F0x2(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex128@0(in1:256)))))) · (u64,f64)

- ground: connection
- languages: c, cpp
- members: c `!=` (u64,f64, 0 modes); cpp `!=` (u64,f64, 0 modes); cpp `not_eq` (u64,f64, 0 modes)

  - c/op_514 / cpp/op_514 -- **total equality**
  - c/op_514 / cpp/op_982 -- **total equality**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),ex64@0(in1:256)))) · (u64,f64)

- ground: connection
- languages: c, cpp
- members: c `>` (u64,f64, 0 modes); c `>=` (u64,f64, 0 modes); cpp `>` (u64,f64, 0 modes); cpp `>=` (u64,f64, 0 modes); cpp `<=>` (u64,f64, 0 modes)

  - c/op_550 / cpp/op_550 -- **core difference**
  - c/op_550 / cpp/op_586 -- **core difference**
  - c/op_550 / cpp/op_766 -- **core difference**
  - c/op_586 / cpp/op_550 -- **core difference**
  - c/op_586 / cpp/op_586 -- **core difference**
  - c/op_586 / cpp/op_766 -- **core difference**

### shared-core group And64(69:64,zx64(CmpF64(ex64@0(in1:256),ex64@0(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))))))) · (u64,f64)

- ground: connection
- languages: c, cpp
- members: c `<=` (u64,f64, 0 modes); c `<` (u64,f64, 0 modes); cpp `<=` (u64,f64, 0 modes); cpp `<` (u64,f64, 0 modes); cpp `<=>` (u64,f64, 0 modes)

  - c/op_622 / cpp/op_622 -- **core difference**
  - c/op_622 / cpp/op_658 -- **core difference**
  - c/op_622 / cpp/op_766 -- **core difference**
  - c/op_658 / cpp/op_622 -- **core difference**
  - c/op_658 / cpp/op_658 -- **core difference**
  - c/op_658 / cpp/op_766 -- **core difference**

### shared-core group CmpEQ64F0x2(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex128@0(in1:256)) · (u64,f64)

- ground: connection
- languages: c, cpp
- members: c `==` (u64,f64, 0 modes); c `!=` (u64,f64, 0 modes); cpp `==` (u64,f64, 0 modes); cpp `!=` (u64,f64, 0 modes); cpp `not_eq` (u64,f64, 0 modes)

  - c/op_478 / cpp/op_478 -- **total equality**
  - c/op_478 / cpp/op_514 -- **core difference**
  - c/op_478 / cpp/op_982 -- **core difference**
  - c/op_514 / cpp/op_478 -- **core difference**
  - c/op_514 / cpp/op_514 -- **total equality**
  - c/op_514 / cpp/op_982 -- **total equality**

### shared-core group Add64F0x2(ex128@0(in1:256),Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))) · (u64,f64)

- ground: connection
- languages: c, cpp
- members: c `+` (u64,f64, 0 modes); cpp `+` (u64,f64, 0 modes)

  - c/op_118 / cpp/op_118 -- **total equality**

### shared-core group Sub64F0x2(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex128@0(in1:256)) · (u64,f64)

- ground: connection
- languages: c, cpp
- members: c `-` (u64,f64, 0 modes); cpp `-` (u64,f64, 0 modes)

  - c/op_154 / cpp/op_154 -- **total equality**

### shared-core group Mul64F0x2(ex128@0(in1:256),Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))) · (u64,f64)

- ground: connection
- languages: c, cpp
- members: c `*` (u64,f64, 0 modes); cpp `*` (u64,f64, 0 modes)

  - c/op_190 / cpp/op_190 -- **total equality**

### shared-core group Div64F0x2(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex128@0(in1:256)) · (u64,f64)

- ground: connection
- languages: c, cpp
- members: c `/` (u64,f64, 0 modes); cpp `/` (u64,f64, 0 modes)

  - c/op_226 / cpp/op_226 -- **total equality**

### shared-core group And8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64)))) · (u64,f64)

- ground: connection
- languages: c, cpp
- members: c `&&` (u64,f64, 0 modes); cpp `&&` (u64,f64, 0 modes); cpp `and` (u64,f64, 0 modes)

  - c/op_334 / cpp/op_334 -- **core difference**
  - c/op_334 / cpp/op_838 -- **core difference**

### shared-core group Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64)))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64)))) · (u64,f64)

- ground: connection
- languages: c, cpp
- members: c `||` (u64,f64, 0 modes); cpp `||` (u64,f64, 0 modes); cpp `or` (u64,f64, 0 modes)

  - c/op_298 / cpp/op_298 -- **core difference**
  - c/op_298 / cpp/op_802 -- **core difference**

### shared-core group ex64@0(Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))) · (u64,f64)

- ground: connection
- languages: c, cpp
- members: c `>` (u64,f64, 0 modes); c `>=` (u64,f64, 0 modes); c `<=` (u64,f64, 0 modes); c `<` (u64,f64, 0 modes); cpp `>` (u64,f64, 0 modes); cpp `>=` (u64,f64, 0 modes); cpp `<=` (u64,f64, 0 modes); cpp `<` (u64,f64, 0 modes); cpp `<=>` (u64,f64, 0 modes)

  - c/op_550 / cpp/op_550 -- **core difference**
  - c/op_550 / cpp/op_586 -- **core difference**
  - c/op_550 / cpp/op_622 -- **core difference**
  - c/op_550 / cpp/op_658 -- **core difference**
  - c/op_550 / cpp/op_766 -- **core difference**
  - c/op_586 / cpp/op_550 -- **core difference**
  - c/op_586 / cpp/op_586 -- **core difference**
  - c/op_586 / cpp/op_622 -- **core difference**
  - c/op_586 / cpp/op_658 -- **core difference**
  - c/op_586 / cpp/op_766 -- **core difference**
  - c/op_622 / cpp/op_550 -- **core difference**
  - c/op_622 / cpp/op_586 -- **core difference**
  - c/op_622 / cpp/op_622 -- **core difference**
  - c/op_622 / cpp/op_658 -- **core difference**
  - c/op_622 / cpp/op_766 -- **core difference**
  - c/op_658 / cpp/op_550 -- **core difference**
  - c/op_658 / cpp/op_586 -- **core difference**
  - c/op_658 / cpp/op_622 -- **core difference**
  - c/op_658 / cpp/op_658 -- **core difference**
  - c/op_658 / cpp/op_766 -- **core difference**

### shared-core group Add64F0x2(64HLtoV128(ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))),ex64@64(Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64)))),Sub64Fx2(0:32,InterleaveLO32x4(ld128/g0(13:64),zx128(in0:64)),ld128/g0(21:64))) · (u64,f64)

- ground: connection
- languages: c, cpp
- members: c `+` (u64,f64, 0 modes); c `-` (u64,f64, 0 modes); c `*` (u64,f64, 0 modes); c `/` (u64,f64, 0 modes); c `==` (u64,f64, 0 modes); c `!=` (u64,f64, 0 modes); c `>` (u64,f64, 0 modes); c `>=` (u64,f64, 0 modes); c `<=` (u64,f64, 0 modes); c `<` (u64,f64, 0 modes); cpp `+` (u64,f64, 0 modes); cpp `-` (u64,f64, 0 modes); cpp `*` (u64,f64, 0 modes); cpp `/` (u64,f64, 0 modes); cpp `==` (u64,f64, 0 modes); cpp `!=` (u64,f64, 0 modes); cpp `>` (u64,f64, 0 modes); cpp `>=` (u64,f64, 0 modes); cpp `<=` (u64,f64, 0 modes); cpp `<` (u64,f64, 0 modes); cpp `<=>` (u64,f64, 0 modes); cpp `not_eq` (u64,f64, 0 modes)

  - c/op_118 / cpp/op_118 -- **total equality**
  - c/op_118 / cpp/op_154 -- **core difference**
  - c/op_118 / cpp/op_190 -- **core difference**
  - c/op_118 / cpp/op_226 -- **core difference**
  - c/op_118 / cpp/op_478 -- **core difference**
  - c/op_118 / cpp/op_514 -- **core difference**
  - c/op_118 / cpp/op_550 -- **core difference**
  - c/op_118 / cpp/op_586 -- **core difference**
  - c/op_118 / cpp/op_622 -- **core difference**
  - c/op_118 / cpp/op_658 -- **core difference**
  - c/op_118 / cpp/op_766 -- **core difference**
  - c/op_118 / cpp/op_982 -- **core difference**
  - c/op_154 / cpp/op_118 -- **core difference**
  - c/op_154 / cpp/op_154 -- **total equality**
  - c/op_154 / cpp/op_190 -- **core difference**
  - c/op_154 / cpp/op_226 -- **core difference**
  - c/op_154 / cpp/op_478 -- **core difference**
  - c/op_154 / cpp/op_514 -- **core difference**
  - c/op_154 / cpp/op_550 -- **core difference**
  - c/op_154 / cpp/op_586 -- **core difference**
  - c/op_154 / cpp/op_622 -- **core difference**
  - c/op_154 / cpp/op_658 -- **core difference**
  - c/op_154 / cpp/op_766 -- **core difference**
  - c/op_154 / cpp/op_982 -- **core difference**
  - c/op_190 / cpp/op_118 -- **core difference**
  - c/op_190 / cpp/op_154 -- **core difference**
  - c/op_190 / cpp/op_190 -- **total equality**
  - c/op_190 / cpp/op_226 -- **core difference**
  - c/op_190 / cpp/op_478 -- **core difference**
  - c/op_190 / cpp/op_514 -- **core difference**
  - c/op_190 / cpp/op_550 -- **core difference**
  - c/op_190 / cpp/op_586 -- **core difference**
  - c/op_190 / cpp/op_622 -- **core difference**
  - c/op_190 / cpp/op_658 -- **core difference**
  - c/op_190 / cpp/op_766 -- **core difference**
  - c/op_190 / cpp/op_982 -- **core difference**
  - c/op_226 / cpp/op_118 -- **core difference**
  - c/op_226 / cpp/op_154 -- **core difference**
  - c/op_226 / cpp/op_190 -- **core difference**
  - c/op_226 / cpp/op_226 -- **total equality**
  - c/op_226 / cpp/op_478 -- **core difference**
  - c/op_226 / cpp/op_514 -- **core difference**
  - c/op_226 / cpp/op_550 -- **core difference**
  - c/op_226 / cpp/op_586 -- **core difference**
  - c/op_226 / cpp/op_622 -- **core difference**
  - c/op_226 / cpp/op_658 -- **core difference**
  - c/op_226 / cpp/op_766 -- **core difference**
  - c/op_226 / cpp/op_982 -- **core difference**
  - c/op_478 / cpp/op_118 -- **core difference**
  - c/op_478 / cpp/op_154 -- **core difference**
  - c/op_478 / cpp/op_190 -- **core difference**
  - c/op_478 / cpp/op_226 -- **core difference**
  - c/op_478 / cpp/op_478 -- **total equality**
  - c/op_478 / cpp/op_514 -- **core difference**
  - c/op_478 / cpp/op_550 -- **core difference**
  - c/op_478 / cpp/op_586 -- **core difference**
  - c/op_478 / cpp/op_622 -- **core difference**
  - c/op_478 / cpp/op_658 -- **core difference**
  - c/op_478 / cpp/op_766 -- **core difference**
  - c/op_478 / cpp/op_982 -- **core difference**
  - c/op_514 / cpp/op_118 -- **core difference**
  - c/op_514 / cpp/op_154 -- **core difference**
  - c/op_514 / cpp/op_190 -- **core difference**
  - c/op_514 / cpp/op_226 -- **core difference**
  - c/op_514 / cpp/op_478 -- **core difference**
  - c/op_514 / cpp/op_514 -- **total equality**
  - c/op_514 / cpp/op_550 -- **core difference**
  - c/op_514 / cpp/op_586 -- **core difference**
  - c/op_514 / cpp/op_622 -- **core difference**
  - c/op_514 / cpp/op_658 -- **core difference**
  - c/op_514 / cpp/op_766 -- **core difference**
  - c/op_514 / cpp/op_982 -- **total equality**
  - c/op_550 / cpp/op_118 -- **core difference**
  - c/op_550 / cpp/op_154 -- **core difference**
  - c/op_550 / cpp/op_190 -- **core difference**
  - c/op_550 / cpp/op_226 -- **core difference**
  - c/op_550 / cpp/op_478 -- **core difference**
  - c/op_550 / cpp/op_514 -- **core difference**
  - c/op_550 / cpp/op_550 -- **core difference**
  - c/op_550 / cpp/op_586 -- **core difference**
  - c/op_550 / cpp/op_622 -- **core difference**
  - c/op_550 / cpp/op_658 -- **core difference**
  - c/op_550 / cpp/op_766 -- **core difference**
  - c/op_550 / cpp/op_982 -- **core difference**
  - c/op_586 / cpp/op_118 -- **core difference**
  - c/op_586 / cpp/op_154 -- **core difference**
  - c/op_586 / cpp/op_190 -- **core difference**
  - c/op_586 / cpp/op_226 -- **core difference**
  - c/op_586 / cpp/op_478 -- **core difference**
  - c/op_586 / cpp/op_514 -- **core difference**
  - c/op_586 / cpp/op_550 -- **core difference**
  - c/op_586 / cpp/op_586 -- **core difference**
  - c/op_586 / cpp/op_622 -- **core difference**
  - c/op_586 / cpp/op_658 -- **core difference**
  - c/op_586 / cpp/op_766 -- **core difference**
  - c/op_586 / cpp/op_982 -- **core difference**
  - c/op_622 / cpp/op_118 -- **core difference**
  - c/op_622 / cpp/op_154 -- **core difference**
  - c/op_622 / cpp/op_190 -- **core difference**
  - c/op_622 / cpp/op_226 -- **core difference**
  - c/op_622 / cpp/op_478 -- **core difference**
  - c/op_622 / cpp/op_514 -- **core difference**
  - c/op_622 / cpp/op_550 -- **core difference**
  - c/op_622 / cpp/op_586 -- **core difference**
  - c/op_622 / cpp/op_622 -- **core difference**
  - c/op_622 / cpp/op_658 -- **core difference**
  - c/op_622 / cpp/op_766 -- **core difference**
  - c/op_622 / cpp/op_982 -- **core difference**
  - c/op_658 / cpp/op_118 -- **core difference**
  - c/op_658 / cpp/op_154 -- **core difference**
  - c/op_658 / cpp/op_190 -- **core difference**
  - c/op_658 / cpp/op_226 -- **core difference**
  - c/op_658 / cpp/op_478 -- **core difference**
  - c/op_658 / cpp/op_514 -- **core difference**
  - c/op_658 / cpp/op_550 -- **core difference**
  - c/op_658 / cpp/op_586 -- **core difference**
  - c/op_658 / cpp/op_622 -- **core difference**
  - c/op_658 / cpp/op_658 -- **core difference**
  - c/op_658 / cpp/op_766 -- **core difference**
  - c/op_658 / cpp/op_982 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,And64(69:64,zx64(CmpF64(ex64@0(in1:256),0:64))),0:64,u0:64)))) · (u64,f64)

- ground: connection
- languages: c, cpp
- members: c `||` (u64,f64, 0 modes); c `&&` (u64,f64, 0 modes); cpp `||` (u64,f64, 0 modes); cpp `&&` (u64,f64, 0 modes); cpp `or` (u64,f64, 0 modes); cpp `and` (u64,f64, 0 modes)

  - c/op_298 / cpp/op_298 -- **core difference**
  - c/op_298 / cpp/op_334 -- **core difference**
  - c/op_298 / cpp/op_802 -- **core difference**
  - c/op_298 / cpp/op_838 -- **core difference**
  - c/op_334 / cpp/op_298 -- **core difference**
  - c/op_334 / cpp/op_334 -- **core difference**
  - c/op_334 / cpp/op_802 -- **core difference**
  - c/op_334 / cpp/op_838 -- **core difference**

### shared-core group And8(zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64)))) · (u64,i32)

- ground: connection
- languages: c, cpp
- members: c `&&` (u64,i32, 0 modes); cpp `&&` (u64,i32, 0 modes); cpp `and` (u64,i32, 0 modes)

  - c/op_330 / cpp/op_330 -- **core difference**
  - c/op_330 / cpp/op_834 -- **core difference**

### shared-core group Or8(zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64)))) · (u64,i32)

- ground: connection
- languages: c, cpp
- members: c `||` (u64,i32, 0 modes); cpp `||` (u64,i32, 0 modes); cpp `or` (u64,i32, 0 modes)

  - c/op_294 / cpp/op_294 -- **core difference**
  - c/op_294 / cpp/op_798 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(4:64,8:64,in0:64,sx64(ex32@0(in1:64)),u0:64))) · (u64,i32)

- ground: connection
- languages: c, cpp
- members: c `==` (u64,i32, 1 modes); cpp `==` (u64,i32, 1 modes)

  - c/op_474 / cpp/op_474 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,8:64,in0:64,sx64(ex32@0(in1:64)),u0:64))) · (u64,i32)

- ground: connection
- languages: c, cpp
- members: c `!=` (u64,i32, 2 modes); cpp `!=` (u64,i32, 1 modes); cpp `not_eq` (u64,i32, 1 modes)

  - c/op_510 / cpp/op_510 -- **core difference**
  - c/op_510 / cpp/op_978 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,8:64,in0:64,sx64(ex32@0(in1:64)),u0:64))) · (u64,i32)

- ground: connection
- languages: c, cpp
- members: c `>` (u64,i32, 1 modes); cpp `>` (u64,i32, 1 modes)

  - c/op_546 / cpp/op_546 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,8:64,in0:64,sx64(ex32@0(in1:64)),u0:64))) · (u64,i32)

- ground: connection
- languages: c, cpp
- members: c `>=` (u64,i32, 1 modes); cpp `>=` (u64,i32, 1 modes)

  - c/op_582 / cpp/op_582 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(6:64,8:64,in0:64,sx64(ex32@0(in1:64)),u0:64))) · (u64,i32)

- ground: connection
- languages: c, cpp
- members: c `<=` (u64,i32, 1 modes); cpp `<=` (u64,i32, 1 modes)

  - c/op_618 / cpp/op_618 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(2:64,8:64,in0:64,sx64(ex32@0(in1:64)),u0:64))) · (u64,i32)

- ground: connection
- languages: c, cpp
- members: c `<` (u64,i32, 1 modes); cpp `<` (u64,i32, 1 modes)

  - c/op_654 / cpp/op_654 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64))) · (u64,i32)

- ground: connection
- languages: c, cpp
- members: c `||` (u64,i32, 0 modes); c `&&` (u64,i32, 0 modes); cpp `||` (u64,i32, 0 modes); cpp `&&` (u64,i32, 0 modes); cpp `or` (u64,i32, 0 modes); cpp `and` (u64,i32, 0 modes)

  - c/op_294 / cpp/op_294 -- **core difference**
  - c/op_294 / cpp/op_330 -- **core difference**
  - c/op_294 / cpp/op_798 -- **core difference**
  - c/op_294 / cpp/op_834 -- **core difference**
  - c/op_330 / cpp/op_294 -- **core difference**
  - c/op_330 / cpp/op_330 -- **core difference**
  - c/op_330 / cpp/op_798 -- **core difference**
  - c/op_330 / cpp/op_834 -- **core difference**

### shared-core group ex64@64(DivModU128to64(64HLto128(0:64,in0:64),sx64(ex32@0(in1:64)))) · (u64,i32)

- ground: connection
- languages: c, cpp
- members: c `/` (u64,i32, 0 modes); c `%` (u64,i32, 0 modes); cpp `/` (u64,i32, 0 modes); cpp `%` (u64,i32, 0 modes)

  - c/op_222 / cpp/op_222 -- **total equality**
  - c/op_222 / cpp/op_258 -- **core difference**
  - c/op_258 / cpp/op_222 -- **core difference**
  - c/op_258 / cpp/op_258 -- **total equality**

### shared-core group Shl64(in0:64,And8(63:8,ex8@0(in1:64))) · (u64,i32)

- ground: connection
- languages: c, cpp, go, rust
- members: c `<<` (u64,i32, 0 modes); cpp `<<` (u64,i32, 0 modes); go `<<` (u64,i32, 1 modes); rust `<<` (u64,i32, 0 modes)

  - c/op_690 / cpp/op_690 -- **total equality**
  - c/op_690 / go/op_180 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_690 / rust/op_474 -- **total equality**
  - cpp/op_690 / go/op_180 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_690 / rust/op_474 -- **total equality**
  - go/op_180 / rust/op_474 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)

### shared-core group Shr64(in0:64,And8(63:8,ex8@0(in1:64))) · (u64,i32)

- ground: connection
- languages: c, cpp, go, rust
- members: c `>>` (u64,i32, 0 modes); cpp `>>` (u64,i32, 0 modes); go `>>` (u64,i32, 1 modes); rust `>>` (u64,i32, 0 modes)

  - c/op_726 / cpp/op_726 -- **total equality**
  - c/op_726 / go/op_216 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_726 / rust/op_510 -- **total equality**
  - cpp/op_726 / go/op_216 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_726 / rust/op_510 -- **total equality**
  - go/op_216 / rust/op_510 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)

### shared-core group Add64(in0:64,sx64(ex32@0(in1:64))) · (u64,i32)

- ground: connection
- languages: c, cpp
- members: c `+` (u64,i32, 0 modes); cpp `+` (u64,i32, 0 modes)

  - c/op_114 / cpp/op_114 -- **total equality**

### shared-core group Sub64(in0:64,sx64(ex32@0(in1:64))) · (u64,i32)

- ground: connection
- languages: c, cpp
- members: c `-` (u64,i32, 0 modes); cpp `-` (u64,i32, 0 modes)

  - c/op_150 / cpp/op_150 -- **total equality**

### shared-core group Mul64(in0:64,sx64(ex32@0(in1:64))) · (u64,i32)

- ground: connection
- languages: c, cpp
- members: c `*` (u64,i32, 0 modes); cpp `*` (u64,i32, 0 modes)

  - c/op_186 / cpp/op_186 -- **total equality**

### shared-core group Xor64(in0:64,sx64(ex32@0(in1:64))) · (u64,i32)

- ground: connection
- languages: c, cpp
- members: c `^` (u64,i32, 0 modes); cpp `^` (u64,i32, 0 modes); cpp `xor` (u64,i32, 0 modes)

  - c/op_402 / cpp/op_402 -- **total equality**
  - c/op_402 / cpp/op_906 -- **total equality**

### shared-core group And64(in0:64,sx64(ex32@0(in1:64))) · (u64,i32)

- ground: connection
- languages: c, cpp
- members: c `&` (u64,i32, 0 modes); cpp `&` (u64,i32, 0 modes); cpp `bitand` (u64,i32, 0 modes)

  - c/op_438 / cpp/op_438 -- **total equality**
  - c/op_438 / cpp/op_942 -- **total equality**

### shared-core group Or64(in0:64,sx64(ex32@0(in1:64))) · (u64,i32)

- ground: connection
- languages: c, cpp
- members: c `|` (u64,i32, 0 modes); cpp `|` (u64,i32, 0 modes); cpp `bitor` (u64,i32, 0 modes)

  - c/op_366 / cpp/op_366 -- **total equality**
  - c/op_366 / cpp/op_870 -- **total equality**

### shared-core group And8(63:8,ex8@0(in1:64)) · (u64,i32)

- ground: connection
- languages: c, cpp, go, rust
- members: c `<<` (u64,i32, 0 modes); c `>>` (u64,i32, 0 modes); cpp `<<` (u64,i32, 0 modes); cpp `>>` (u64,i32, 0 modes); go `<<` (u64,i32, 1 modes); go `>>` (u64,i32, 1 modes); rust `<<` (u64,i32, 0 modes); rust `>>` (u64,i32, 0 modes)

  - c/op_690 / cpp/op_690 -- **total equality**
  - c/op_690 / cpp/op_726 -- **core difference**
  - c/op_726 / cpp/op_690 -- **core difference**
  - c/op_726 / cpp/op_726 -- **total equality**
  - c/op_690 / go/op_180 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_690 / go/op_216 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_726 / go/op_180 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_726 / go/op_216 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_690 / rust/op_474 -- **total equality**
  - c/op_690 / rust/op_510 -- **core difference**
  - c/op_726 / rust/op_474 -- **core difference**
  - c/op_726 / rust/op_510 -- **total equality**
  - cpp/op_690 / go/op_180 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_690 / go/op_216 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_726 / go/op_180 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_726 / go/op_216 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_690 / rust/op_474 -- **total equality**
  - cpp/op_690 / rust/op_510 -- **core difference**
  - cpp/op_726 / rust/op_474 -- **core difference**
  - cpp/op_726 / rust/op_510 -- **total equality**
  - go/op_180 / rust/op_474 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - go/op_180 / rust/op_510 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - go/op_216 / rust/op_474 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - go/op_216 / rust/op_510 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)

### shared-core group And8(zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (u64,i64)

- ground: connection
- languages: c, cpp
- members: c `&&` (u64,i64, 0 modes); cpp `&&` (u64,i64, 0 modes); cpp `and` (u64,i64, 0 modes)

  - c/op_331 / cpp/op_331 -- **core difference**
  - c/op_331 / cpp/op_835 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,Or64(in0:64,in1:64),0:64,u0:64))) · (u64,i64)

- ground: connection
- languages: c, cpp
- members: c `||` (u64,i64, 0 modes); cpp `||` (u64,i64, 0 modes); cpp `or` (u64,i64, 0 modes)

  - c/op_295 / cpp/op_295 -- **core difference**
  - c/op_295 / cpp/op_799 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(4:64,8:64,in0:64,in1:64,u0:64))) · (u64,i64)

- ground: connection
- languages: c, cpp, swift
- members: c `==` (u64,i64, 1 modes); cpp `==` (u64,i64, 1 modes); swift `==` (u64,i64, 2 modes)

  - c/op_475 / cpp/op_475 -- **core difference**
  - c/op_475 / swift/op_523 -- **core difference**
  - cpp/op_475 / swift/op_523 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,8:64,in0:64,in1:64,u0:64))) · (u64,i64)

- ground: connection
- languages: c, cpp, swift
- members: c `!=` (u64,i64, 1 modes); cpp `!=` (u64,i64, 1 modes); cpp `not_eq` (u64,i64, 1 modes); swift `!=` (u64,i64, 3 modes)

  - c/op_511 / cpp/op_511 -- **core difference**
  - c/op_511 / cpp/op_979 -- **core difference**
  - c/op_511 / swift/op_451 -- **core difference**
  - cpp/op_511 / swift/op_451 -- **core difference**
  - cpp/op_979 / swift/op_451 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,8:64,in0:64,in1:64,u0:64))) · (u64,i64)

- ground: connection
- languages: c, cpp
- members: c `>` (u64,i64, 0 modes); cpp `>` (u64,i64, 0 modes)

  - c/op_547 / cpp/op_547 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,8:64,in0:64,in1:64,u0:64))) · (u64,i64)

- ground: connection
- languages: c, cpp, swift
- members: c `>=` (u64,i64, 1 modes); cpp `>=` (u64,i64, 1 modes); swift `>=` (u64,i64, 2 modes)

  - c/op_583 / cpp/op_583 -- **core difference**
  - c/op_583 / swift/op_415 -- **core difference**
  - cpp/op_583 / swift/op_415 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(6:64,8:64,in0:64,in1:64,u0:64))) · (u64,i64)

- ground: connection
- languages: c, cpp
- members: c `<=` (u64,i64, 0 modes); cpp `<=` (u64,i64, 0 modes)

  - c/op_619 / cpp/op_619 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(2:64,8:64,in0:64,in1:64,u0:64))) · (u64,i64)

- ground: connection
- languages: c, cpp, swift
- members: c `<` (u64,i64, 1 modes); cpp `<` (u64,i64, 1 modes); swift `<` (u64,i64, 2 modes)

  - c/op_655 / cpp/op_655 -- **core difference**
  - c/op_655 / swift/op_307 -- **core difference**
  - cpp/op_655 / swift/op_307 -- **core difference**

### shared-core group ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64)) · (u64,i64)

- ground: connection
- languages: c, cpp
- members: c `/` (u64,i64, 0 modes); c `%` (u64,i64, 0 modes); cpp `/` (u64,i64, 0 modes); cpp `%` (u64,i64, 0 modes)

  - c/op_223 / cpp/op_223 -- **total equality**
  - c/op_223 / cpp/op_259 -- **core difference**
  - c/op_259 / cpp/op_223 -- **core difference**
  - c/op_259 / cpp/op_259 -- **total equality**

### shared-core group Shl64(in0:64,And8(63:8,ex8@0(in1:64))) · (u64,i64)

- ground: connection
- languages: c, cpp, go, rust
- members: c `<<` (u64,i64, 0 modes); cpp `<<` (u64,i64, 0 modes); go `<<` (u64,i64, 1 modes); rust `<<` (u64,i64, 0 modes)

  - c/op_691 / cpp/op_691 -- **total equality**
  - c/op_691 / go/op_181 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_691 / rust/op_475 -- **total equality**
  - cpp/op_691 / go/op_181 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_691 / rust/op_475 -- **total equality**
  - go/op_181 / rust/op_475 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)

### shared-core group Shr64(in0:64,And8(63:8,ex8@0(in1:64))) · (u64,i64)

- ground: connection
- languages: c, cpp, go, rust
- members: c `>>` (u64,i64, 0 modes); cpp `>>` (u64,i64, 0 modes); go `>>` (u64,i64, 1 modes); rust `>>` (u64,i64, 0 modes)

  - c/op_727 / cpp/op_727 -- **total equality**
  - c/op_727 / go/op_217 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_727 / rust/op_511 -- **total equality**
  - cpp/op_727 / go/op_217 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_727 / rust/op_511 -- **total equality**
  - go/op_217 / rust/op_511 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)

### shared-core group And8(63:8,ex8@0(in1:64)) · (u64,i64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `<<` (u64,i64, 0 modes); c `>>` (u64,i64, 0 modes); cpp `<<` (u64,i64, 0 modes); cpp `>>` (u64,i64, 0 modes); go `<<` (u64,i64, 1 modes); go `>>` (u64,i64, 1 modes); rust `<<` (u64,i64, 0 modes); rust `>>` (u64,i64, 0 modes); swift `<<` (u64,i64, 0 modes); swift `>>` (u64,i64, 0 modes)

  - c/op_691 / cpp/op_691 -- **total equality**
  - c/op_691 / cpp/op_727 -- **core difference**
  - c/op_727 / cpp/op_691 -- **core difference**
  - c/op_727 / cpp/op_727 -- **total equality**
  - c/op_691 / go/op_181 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_691 / go/op_217 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_727 / go/op_181 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_727 / go/op_217 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - c/op_691 / rust/op_475 -- **total equality**
  - c/op_691 / rust/op_511 -- **core difference**
  - c/op_727 / rust/op_475 -- **core difference**
  - c/op_727 / rust/op_511 -- **total equality**
  - c/op_691 / swift/op_703 -- **core difference**
  - c/op_691 / swift/op_739 -- **core difference**
  - c/op_727 / swift/op_703 -- **core difference**
  - c/op_727 / swift/op_739 -- **core difference**
  - cpp/op_691 / go/op_181 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_691 / go/op_217 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_727 / go/op_181 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_727 / go/op_217 -- **core difference**
    - only on the right: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - cpp/op_691 / rust/op_475 -- **total equality**
  - cpp/op_691 / rust/op_511 -- **core difference**
  - cpp/op_727 / rust/op_475 -- **core difference**
  - cpp/op_727 / rust/op_511 -- **total equality**
  - cpp/op_691 / swift/op_703 -- **core difference**
  - cpp/op_691 / swift/op_739 -- **core difference**
  - cpp/op_727 / swift/op_703 -- **core difference**
  - cpp/op_727 / swift/op_739 -- **core difference**
  - go/op_181 / rust/op_475 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - go/op_181 / rust/op_511 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - go/op_217 / rust/op_475 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - go/op_217 / rust/op_511 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - go/op_181 / swift/op_703 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - go/op_181 / swift/op_739 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - go/op_217 / swift/op_703 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - go/op_217 / swift/op_739 -- **core difference**
    - only on the left: `in1 < 0 (signed)` -> `panic-call:runtime.panicshift` (branch-to-response)
  - rust/op_475 / swift/op_703 -- **core difference**
  - rust/op_475 / swift/op_739 -- **core difference**
  - rust/op_511 / swift/op_703 -- **core difference**
  - rust/op_511 / swift/op_739 -- **core difference**

### shared-core group Add64(in0:64,in1:64) · (u64,i64)

- ground: connection
- languages: c, cpp
- members: c `+` (u64,i64, 0 modes); cpp `+` (u64,i64, 0 modes)

  - c/op_115 / cpp/op_115 -- **total equality**

### shared-core group Sub64(in0:64,in1:64) · (u64,i64)

- ground: connection
- languages: c, cpp
- members: c `-` (u64,i64, 0 modes); cpp `-` (u64,i64, 0 modes)

  - c/op_151 / cpp/op_151 -- **total equality**

### shared-core group Mul64(in0:64,in1:64) · (u64,i64)

- ground: connection
- languages: c, cpp
- members: c `*` (u64,i64, 0 modes); cpp `*` (u64,i64, 0 modes)

  - c/op_187 / cpp/op_187 -- **total equality**

### shared-core group Xor64(in0:64,in1:64) · (u64,i64)

- ground: connection
- languages: c, cpp
- members: c `^` (u64,i64, 0 modes); cpp `^` (u64,i64, 0 modes); cpp `xor` (u64,i64, 0 modes)

  - c/op_403 / cpp/op_403 -- **total equality**
  - c/op_403 / cpp/op_907 -- **total equality**

### shared-core group And64(in0:64,in1:64) · (u64,i64)

- ground: connection
- languages: c, cpp
- members: c `&` (u64,i64, 0 modes); cpp `&` (u64,i64, 0 modes); cpp `bitand` (u64,i64, 0 modes)

  - c/op_439 / cpp/op_439 -- **total equality**
  - c/op_439 / cpp/op_943 -- **total equality**

### shared-core group Or64(in0:64,in1:64) · (u64,i64)

- ground: connection
- languages: c, cpp
- members: c `||` (u64,i64, 0 modes); c `|` (u64,i64, 0 modes); cpp `||` (u64,i64, 0 modes); cpp `|` (u64,i64, 0 modes); cpp `or` (u64,i64, 0 modes); cpp `bitor` (u64,i64, 0 modes)

  - c/op_295 / cpp/op_295 -- **core difference**
  - c/op_295 / cpp/op_367 -- **core difference**
  - c/op_295 / cpp/op_799 -- **core difference**
  - c/op_295 / cpp/op_871 -- **core difference**
  - c/op_367 / cpp/op_295 -- **core difference**
  - c/op_367 / cpp/op_367 -- **total equality**
  - c/op_367 / cpp/op_799 -- **core difference**
  - c/op_367 / cpp/op_871 -- **total equality**

### shared-core group And8(zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in0:64,0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,in1:64,0:64,u0:64)))) · (u64,u64)

- ground: connection
- languages: c, cpp
- members: c `&&` (u64,u64, 0 modes); cpp `&&` (u64,u64, 0 modes); cpp `and` (u64,u64, 0 modes)

  - c/op_332 / cpp/op_332 -- **core difference**
  - c/op_332 / cpp/op_836 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,20:64,Or64(in0:64,in1:64),0:64,u0:64))) · (u64,u64)

- ground: connection
- languages: c, cpp
- members: c `||` (u64,u64, 0 modes); cpp `||` (u64,u64, 0 modes); cpp `or` (u64,u64, 0 modes)

  - c/op_296 / cpp/op_296 -- **core difference**
  - c/op_296 / cpp/op_800 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(4:64,8:64,in0:64,in1:64,u0:64))) · (u64,u64)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `==` (u64,u64, 0 modes); cpp `==` (u64,u64, 0 modes); rust `==` (u64,u64, 0 modes); swift `==` (u64,u64, 0 modes)

  - c/op_476 / cpp/op_476 -- **core difference**
  - c/op_476 / rust/op_260 -- **core difference**
  - c/op_476 / swift/op_524 -- **core difference**
  - cpp/op_476 / rust/op_260 -- **total equality**
  - cpp/op_476 / swift/op_524 -- **total equality**
  - rust/op_260 / swift/op_524 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(5:64,8:64,in0:64,in1:64,u0:64))) · (u64,u64)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `!=` (u64,u64, 0 modes); cpp `!=` (u64,u64, 0 modes); cpp `not_eq` (u64,u64, 0 modes); rust `!=` (u64,u64, 0 modes); swift `!=` (u64,u64, 0 modes)

  - c/op_512 / cpp/op_512 -- **core difference**
  - c/op_512 / cpp/op_980 -- **core difference**
  - c/op_512 / rust/op_296 -- **core difference**
  - c/op_512 / swift/op_452 -- **core difference**
  - cpp/op_512 / rust/op_296 -- **total equality**
  - cpp/op_980 / rust/op_296 -- **total equality**
  - cpp/op_512 / swift/op_452 -- **total equality**
  - cpp/op_980 / swift/op_452 -- **total equality**
  - rust/op_296 / swift/op_452 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(7:64,8:64,in0:64,in1:64,u0:64))) · (u64,u64)

- ground: connection
- languages: c, cpp, rust
- members: c `>` (u64,u64, 0 modes); cpp `>` (u64,u64, 0 modes); cpp `<=>` (u64,u64, 0 modes); rust `>` (u64,u64, 0 modes)

  - c/op_548 / cpp/op_548 -- **core difference**
  - c/op_548 / cpp/op_764 -- **core difference**
  - c/op_548 / rust/op_404 -- **core difference**
  - cpp/op_548 / rust/op_404 -- **total equality**
  - cpp/op_764 / rust/op_404 -- **core difference**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,8:64,in0:64,in1:64,u0:64))) · (u64,u64)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `>=` (u64,u64, 0 modes); cpp `>=` (u64,u64, 0 modes); rust `>=` (u64,u64, 0 modes); swift `>=` (u64,u64, 0 modes)

  - c/op_584 / cpp/op_584 -- **core difference**
  - c/op_584 / rust/op_440 -- **core difference**
  - c/op_584 / swift/op_416 -- **core difference**
  - cpp/op_584 / rust/op_440 -- **total equality**
  - cpp/op_584 / swift/op_416 -- **total equality**
  - rust/op_440 / swift/op_416 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(6:64,8:64,in0:64,in1:64,u0:64))) · (u64,u64)

- ground: connection
- languages: c, cpp, rust
- members: c `<=` (u64,u64, 0 modes); cpp `<=` (u64,u64, 0 modes); rust `<=` (u64,u64, 0 modes)

  - c/op_620 / cpp/op_620 -- **core difference**
  - c/op_620 / rust/op_368 -- **core difference**
  - cpp/op_620 / rust/op_368 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(2:64,8:64,in0:64,in1:64,u0:64))) · (u64,u64)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `<` (u64,u64, 0 modes); cpp `<` (u64,u64, 0 modes); rust `<` (u64,u64, 0 modes); swift `<` (u64,u64, 0 modes)

  - c/op_656 / cpp/op_656 -- **core difference**
  - c/op_656 / rust/op_332 -- **core difference**
  - c/op_656 / swift/op_308 -- **core difference**
  - cpp/op_656 / rust/op_332 -- **total equality**
  - cpp/op_656 / swift/op_308 -- **total equality**
  - rust/op_332 / swift/op_308 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(3:64,8:64,in1:64,in0:64,u0:64))) · (u64,u64)

- ground: connection
- languages: go, swift
- members: go `<=` (u64,u64, 0 modes); swift `<=` (u64,u64, 0 modes)

  - go/op_578 / swift/op_380 -- **total equality**

### shared-core group zx8(ex1@0(amd64g_calculate_condition(2:64,8:64,in1:64,in0:64,u0:64))) · (u64,u64)

- ground: connection
- languages: go, swift
- members: go `>` (u64,u64, 0 modes); swift `>` (u64,u64, 0 modes)

  - go/op_614 / swift/op_344 -- **total equality**

### shared-core group ex1@0(amd64g_calculate_condition(2:64,8:64,in0:64,in1:64,u0:64)) · (u64,u64)

- ground: connection
- languages: c, cpp, rust, swift
- members: c `<` (u64,u64, 0 modes); cpp `<` (u64,u64, 0 modes); rust `<` (u64,u64, 0 modes); swift `-` (u64,u64, 1 modes); swift `<` (u64,u64, 0 modes)

  - c/op_656 / cpp/op_656 -- **core difference**
  - c/op_656 / rust/op_332 -- **core difference**
  - c/op_656 / swift/op_272 -- **core difference**
    - only on the right: `in0 < in1 (unsigned)` -> `trap` (branch-to-response)
  - c/op_656 / swift/op_308 -- **core difference**
  - cpp/op_656 / rust/op_332 -- **total equality**
  - cpp/op_656 / swift/op_272 -- **core difference**
    - only on the right: `in0 < in1 (unsigned)` -> `trap` (branch-to-response)
  - cpp/op_656 / swift/op_308 -- **total equality**
  - rust/op_332 / swift/op_272 -- **core difference**
    - only on the right: `in0 < in1 (unsigned)` -> `trap` (branch-to-response)
  - rust/op_332 / swift/op_308 -- **total equality**

### shared-core group ex1@0(amd64g_calculate_condition(2:64,8:64,in1:64,in0:64,u0:64)) · (u64,u64)

- ground: connection
- languages: go, swift
- members: go `>` (u64,u64, 0 modes); swift `>` (u64,u64, 0 modes); swift `..<` (u64,u64, 1 modes); swift `...` (u64,u64, 1 modes)

  - go/op_614 / swift/op_344 -- **total equality**
  - go/op_614 / swift/op_884 -- **core difference**
    - only on the right: `in1 < in0 (unsigned)` -> `trap` (branch-to-response)
  - go/op_614 / swift/op_920 -- **core difference**
    - only on the right: `in1 < in0 (unsigned)` -> `trap` (branch-to-response)

### shared-core group ex1@0(amd64g_calculate_condition(4:64,20:64,in1:64,0:64,u0:64)) · (u64,u64)

- ground: connection
- languages: go, rust, swift
- members: go `/` (u64,u64, 1 modes); go `%` (u64,u64, 1 modes); rust `/` (u64,u64, 1 modes); rust `%` (u64,u64, 1 modes); swift `/` (u64,u64, 1 modes); swift `%` (u64,u64, 1 modes)

  - go/op_110 / rust/op_656 -- **total equality**
  - go/op_110 / rust/op_692 -- **core difference**
  - go/op_146 / rust/op_656 -- **core difference**
  - go/op_146 / rust/op_692 -- **total equality**
  - go/op_110 / swift/op_164 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_110 / swift/op_200 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_146 / swift/op_164 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_146 / swift/op_200 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_656 / swift/op_164 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_656 / swift/op_200 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_692 / swift/op_164 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_692 / swift/op_200 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)

### shared-core group ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64)) · (u64,u64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `/` (u64,u64, 0 modes); c `%` (u64,u64, 0 modes); cpp `/` (u64,u64, 0 modes); cpp `%` (u64,u64, 0 modes); go `/` (u64,u64, 1 modes); go `%` (u64,u64, 1 modes); rust `/` (u64,u64, 1 modes); rust `%` (u64,u64, 1 modes); swift `/` (u64,u64, 1 modes); swift `%` (u64,u64, 1 modes)

  - c/op_224 / cpp/op_224 -- **total equality**
  - c/op_224 / cpp/op_260 -- **core difference**
  - c/op_260 / cpp/op_224 -- **core difference**
  - c/op_260 / cpp/op_260 -- **total equality**
  - c/op_224 / go/op_110 -- **core equality, modes differ**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - c/op_224 / go/op_146 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - c/op_260 / go/op_110 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - c/op_260 / go/op_146 -- **core equality, modes differ**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - c/op_224 / rust/op_656 -- **core equality, modes differ**
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
  - c/op_224 / rust/op_692 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
  - c/op_260 / rust/op_656 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
  - c/op_260 / rust/op_692 -- **core equality, modes differ**
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
  - c/op_224 / swift/op_164 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - c/op_224 / swift/op_200 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - c/op_260 / swift/op_164 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - c/op_260 / swift/op_200 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_224 / go/op_110 -- **core equality, modes differ**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - cpp/op_224 / go/op_146 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - cpp/op_260 / go/op_110 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - cpp/op_260 / go/op_146 -- **core equality, modes differ**
    - only on the right: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
  - cpp/op_224 / rust/op_656 -- **core equality, modes differ**
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
  - cpp/op_224 / rust/op_692 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
  - cpp/op_260 / rust/op_656 -- **core difference**
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
  - cpp/op_260 / rust/op_692 -- **core equality, modes differ**
    - only on the right: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
  - cpp/op_224 / swift/op_164 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_224 / swift/op_200 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_260 / swift/op_164 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_260 / swift/op_200 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_110 / rust/op_656 -- **total equality**
  - go/op_110 / rust/op_692 -- **core difference**
  - go/op_146 / rust/op_656 -- **core difference**
  - go/op_146 / rust/op_692 -- **total equality**
  - go/op_110 / swift/op_164 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_110 / swift/op_200 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_146 / swift/op_164 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_146 / swift/op_200 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:runtime.panicdivide` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_656 / swift/op_164 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_656 / swift/op_200 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_692 / swift/op_164 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_692 / swift/op_200 -- **core difference**
    - only on the left: `in1 == 0` -> `panic-call:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero` (branch-to-response)
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)

### shared-core group Shl64(in0:64,And8(63:8,ex8@0(in1:64))) · (u64,u64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `<<` (u64,u64, 2 modes); cpp `<<` (u64,u64, 2 modes); go `<<` (u64,u64, 3 modes); rust `<<` (u64,u64, 2 modes); swift `<<` (u64,u64, 3 modes)

  - c/op_692 / cpp/op_692 -- **total equality**
  - c/op_692 / go/op_182 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - c/op_692 / rust/op_476 -- **total equality**
  - c/op_692 / swift/op_704 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - cpp/op_692 / go/op_182 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - cpp/op_692 / rust/op_476 -- **total equality**
  - cpp/op_692 / swift/op_704 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - go/op_182 / rust/op_476 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - go/op_182 / swift/op_704 -- **core difference**
  - rust/op_476 / swift/op_704 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)

### shared-core group Shr64(in0:64,And8(63:8,ex8@0(in1:64))) · (u64,u64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `>>` (u64,u64, 2 modes); cpp `>>` (u64,u64, 2 modes); go `>>` (u64,u64, 3 modes); rust `>>` (u64,u64, 2 modes); swift `>>` (u64,u64, 3 modes)

  - c/op_728 / cpp/op_728 -- **total equality**
  - c/op_728 / go/op_218 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - c/op_728 / rust/op_512 -- **total equality**
  - c/op_728 / swift/op_740 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - cpp/op_728 / go/op_218 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - cpp/op_728 / rust/op_512 -- **total equality**
  - cpp/op_728 / swift/op_740 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - go/op_218 / rust/op_512 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - go/op_218 / swift/op_740 -- **core difference**
  - rust/op_512 / swift/op_740 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)

### shared-core group And8(63:8,ex8@0(in1:64)) · (u64,u64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `<<` (u64,u64, 2 modes); c `>>` (u64,u64, 2 modes); cpp `<<` (u64,u64, 2 modes); cpp `>>` (u64,u64, 2 modes); go `<<` (u64,u64, 3 modes); go `>>` (u64,u64, 3 modes); rust `<<` (u64,u64, 2 modes); rust `>>` (u64,u64, 2 modes); swift `<<` (u64,u64, 3 modes); swift `>>` (u64,u64, 3 modes)

  - c/op_692 / cpp/op_692 -- **total equality**
  - c/op_692 / cpp/op_728 -- **core difference**
  - c/op_728 / cpp/op_692 -- **core difference**
  - c/op_728 / cpp/op_728 -- **total equality**
  - c/op_692 / go/op_182 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - c/op_692 / go/op_218 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - c/op_728 / go/op_182 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - c/op_728 / go/op_218 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - c/op_692 / rust/op_476 -- **total equality**
  - c/op_692 / rust/op_512 -- **core difference**
  - c/op_728 / rust/op_476 -- **core difference**
  - c/op_728 / rust/op_512 -- **total equality**
  - c/op_692 / swift/op_704 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - c/op_692 / swift/op_740 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - c/op_728 / swift/op_704 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - c/op_728 / swift/op_740 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - cpp/op_692 / go/op_182 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - cpp/op_692 / go/op_218 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - cpp/op_728 / go/op_182 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - cpp/op_728 / go/op_218 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - cpp/op_692 / rust/op_476 -- **total equality**
  - cpp/op_692 / rust/op_512 -- **core difference**
  - cpp/op_728 / rust/op_476 -- **core difference**
  - cpp/op_728 / rust/op_512 -- **total equality**
  - cpp/op_692 / swift/op_704 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - cpp/op_692 / swift/op_740 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - cpp/op_728 / swift/op_704 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - cpp/op_728 / swift/op_740 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - go/op_182 / rust/op_476 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - go/op_182 / rust/op_512 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - go/op_218 / rust/op_476 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - go/op_218 / rust/op_512 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
  - go/op_182 / swift/op_704 -- **core difference**
  - go/op_182 / swift/op_740 -- **core difference**
  - go/op_218 / swift/op_704 -- **core difference**
  - go/op_218 / swift/op_740 -- **core difference**
  - rust/op_476 / swift/op_704 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - rust/op_476 / swift/op_740 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - rust/op_512 / swift/op_704 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)
  - rust/op_512 / swift/op_740 -- **core difference**
    - only on the left: `in1 >= 64 (unsigned)` -> `continue-with-a-different-answer` (solver-localized)
    - only on the right: `in1 >= 64 (unsigned)` -> `clamp-continue` (solver-localized)

### shared-core group Add64(in0:64,in1:64) · (u64,u64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `+` (u64,u64, 1 modes); cpp `+` (u64,u64, 1 modes); go `+` (u64,u64, 1 modes); rust `+` (u64,u64, 1 modes); swift `+` (u64,u64, 1 modes)

  - c/op_116 / cpp/op_116 -- **total equality**
  - c/op_116 / go/op_326 -- **total equality**
  - c/op_116 / rust/op_548 -- **total equality**
  - c/op_116 / swift/op_236 -- **core equality, modes differ**
    - only on the left: `in0 + in1 carries out of 64 bits (unsigned)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 + in1 carries out of 64 bits (unsigned)` -> `trap` (branch-to-response)
  - cpp/op_116 / go/op_326 -- **total equality**
  - cpp/op_116 / rust/op_548 -- **total equality**
  - cpp/op_116 / swift/op_236 -- **core equality, modes differ**
    - only on the left: `in0 + in1 carries out of 64 bits (unsigned)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 + in1 carries out of 64 bits (unsigned)` -> `trap` (branch-to-response)
  - go/op_326 / rust/op_548 -- **total equality**
  - go/op_326 / swift/op_236 -- **core equality, modes differ**
    - only on the left: `in0 + in1 carries out of 64 bits (unsigned)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 + in1 carries out of 64 bits (unsigned)` -> `trap` (branch-to-response)
  - rust/op_548 / swift/op_236 -- **core equality, modes differ**
    - only on the left: `in0 + in1 carries out of 64 bits (unsigned)` -> `wrap-continue` (branch-to-response)
    - only on the right: `in0 + in1 carries out of 64 bits (unsigned)` -> `trap` (branch-to-response)

### shared-core group Sub64(in0:64,in1:64) · (u64,u64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `-` (u64,u64, 0 modes); cpp `-` (u64,u64, 0 modes); go `-` (u64,u64, 0 modes); rust `-` (u64,u64, 0 modes); swift `-` (u64,u64, 1 modes)

  - c/op_152 / cpp/op_152 -- **total equality**
  - c/op_152 / go/op_362 -- **total equality**
  - c/op_152 / rust/op_584 -- **total equality**
  - c/op_152 / swift/op_272 -- **core equality, modes differ**
    - only on the right: `in0 < in1 (unsigned)` -> `trap` (branch-to-response)
  - cpp/op_152 / go/op_362 -- **total equality**
  - cpp/op_152 / rust/op_584 -- **total equality**
  - cpp/op_152 / swift/op_272 -- **core equality, modes differ**
    - only on the right: `in0 < in1 (unsigned)` -> `trap` (branch-to-response)
  - go/op_362 / rust/op_584 -- **total equality**
  - go/op_362 / swift/op_272 -- **core equality, modes differ**
    - only on the right: `in0 < in1 (unsigned)` -> `trap` (branch-to-response)
  - rust/op_584 / swift/op_272 -- **core equality, modes differ**
    - only on the right: `in0 < in1 (unsigned)` -> `trap` (branch-to-response)

### shared-core group Mul64(in0:64,in1:64) · (u64,u64)

- ground: connection
- languages: c, cpp, go, rust
- members: c `*` (u64,u64, 0 modes); cpp `*` (u64,u64, 0 modes); go `*` (u64,u64, 0 modes); rust `*` (u64,u64, 0 modes)

  - c/op_188 / cpp/op_188 -- **total equality**
  - c/op_188 / go/op_74 -- **total equality**
  - c/op_188 / rust/op_620 -- **total equality**
  - cpp/op_188 / go/op_74 -- **total equality**
  - cpp/op_188 / rust/op_620 -- **total equality**
  - go/op_74 / rust/op_620 -- **total equality**

### shared-core group Xor64(in0:64,in1:64) · (u64,u64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `^` (u64,u64, 0 modes); cpp `^` (u64,u64, 0 modes); cpp `xor` (u64,u64, 0 modes); go `^` (u64,u64, 0 modes); rust `^` (u64,u64, 0 modes); swift `^` (u64,u64, 0 modes)

  - c/op_404 / cpp/op_404 -- **total equality**
  - c/op_404 / cpp/op_908 -- **total equality**
  - c/op_404 / go/op_434 -- **total equality**
  - c/op_404 / rust/op_224 -- **total equality**
  - c/op_404 / swift/op_668 -- **total equality**
  - cpp/op_404 / go/op_434 -- **total equality**
  - cpp/op_908 / go/op_434 -- **total equality**
  - cpp/op_404 / rust/op_224 -- **total equality**
  - cpp/op_908 / rust/op_224 -- **total equality**
  - cpp/op_404 / swift/op_668 -- **total equality**
  - cpp/op_908 / swift/op_668 -- **total equality**
  - go/op_434 / rust/op_224 -- **total equality**
  - go/op_434 / swift/op_668 -- **total equality**
  - rust/op_224 / swift/op_668 -- **total equality**

### shared-core group And64(in0:64,in1:64) · (u64,u64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `&` (u64,u64, 0 modes); cpp `&` (u64,u64, 0 modes); cpp `bitand` (u64,u64, 0 modes); go `&` (u64,u64, 0 modes); rust `&` (u64,u64, 0 modes); swift `&` (u64,u64, 0 modes)

  - c/op_440 / cpp/op_440 -- **total equality**
  - c/op_440 / cpp/op_944 -- **total equality**
  - c/op_440 / go/op_254 -- **total equality**
  - c/op_440 / rust/op_152 -- **total equality**
  - c/op_440 / swift/op_596 -- **total equality**
  - cpp/op_440 / go/op_254 -- **total equality**
  - cpp/op_944 / go/op_254 -- **total equality**
  - cpp/op_440 / rust/op_152 -- **total equality**
  - cpp/op_944 / rust/op_152 -- **total equality**
  - cpp/op_440 / swift/op_596 -- **total equality**
  - cpp/op_944 / swift/op_596 -- **total equality**
  - go/op_254 / rust/op_152 -- **total equality**
  - go/op_254 / swift/op_596 -- **total equality**
  - rust/op_152 / swift/op_596 -- **total equality**

### shared-core group Or64(in0:64,in1:64) · (u64,u64)

- ground: connection
- languages: c, cpp, go, rust, swift
- members: c `||` (u64,u64, 0 modes); c `|` (u64,u64, 0 modes); cpp `||` (u64,u64, 0 modes); cpp `|` (u64,u64, 0 modes); cpp `or` (u64,u64, 0 modes); cpp `bitor` (u64,u64, 0 modes); go `|` (u64,u64, 0 modes); rust `|` (u64,u64, 0 modes); swift `/` (u64,u64, 1 modes); swift `%` (u64,u64, 1 modes); swift `|` (u64,u64, 0 modes)

  - c/op_296 / cpp/op_296 -- **core difference**
  - c/op_296 / cpp/op_368 -- **core difference**
  - c/op_296 / cpp/op_800 -- **core difference**
  - c/op_296 / cpp/op_872 -- **core difference**
  - c/op_368 / cpp/op_296 -- **core difference**
  - c/op_368 / cpp/op_368 -- **total equality**
  - c/op_368 / cpp/op_800 -- **core difference**
  - c/op_368 / cpp/op_872 -- **total equality**
  - c/op_296 / go/op_398 -- **core difference**
  - c/op_368 / go/op_398 -- **total equality**
  - c/op_296 / rust/op_188 -- **core difference**
  - c/op_368 / rust/op_188 -- **total equality**
  - c/op_296 / swift/op_164 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - c/op_296 / swift/op_200 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - c/op_296 / swift/op_632 -- **core difference**
  - c/op_368 / swift/op_164 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - c/op_368 / swift/op_200 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - c/op_368 / swift/op_632 -- **total equality**
  - cpp/op_296 / go/op_398 -- **core difference**
  - cpp/op_368 / go/op_398 -- **total equality**
  - cpp/op_800 / go/op_398 -- **core difference**
  - cpp/op_872 / go/op_398 -- **total equality**
  - cpp/op_296 / rust/op_188 -- **core difference**
  - cpp/op_368 / rust/op_188 -- **total equality**
  - cpp/op_800 / rust/op_188 -- **core difference**
  - cpp/op_872 / rust/op_188 -- **total equality**
  - cpp/op_296 / swift/op_164 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_296 / swift/op_200 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_296 / swift/op_632 -- **core difference**
  - cpp/op_368 / swift/op_164 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_368 / swift/op_200 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_368 / swift/op_632 -- **total equality**
  - cpp/op_800 / swift/op_164 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_800 / swift/op_200 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_800 / swift/op_632 -- **core difference**
  - cpp/op_872 / swift/op_164 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_872 / swift/op_200 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - cpp/op_872 / swift/op_632 -- **total equality**
  - go/op_398 / rust/op_188 -- **total equality**
  - go/op_398 / swift/op_164 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_398 / swift/op_200 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - go/op_398 / swift/op_632 -- **total equality**
  - rust/op_188 / swift/op_164 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_188 / swift/op_200 -- **core difference**
    - only on the right: `in1 == 0` -> `trap` (branch-to-response)
  - rust/op_188 / swift/op_632 -- **total equality**
