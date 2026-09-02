# verdicts5 -- the third candidate rule

A unit alone in its class, nominated against every
other class carrying the same class key (same operand
types, same result type).  No operator token takes
part in the nomination; each member carries its token
as a display label only.

- classes read: 1113
- classes of size 1: 737
- nominations: 7246
- distinct unit pairs judged: 4348
- tally: {'UNMATCHED': 3118, 'UNDECIDED': 3945, 'MATCHED': 159, 'DIFFERS-BY-DESIGN': 24}

## the MATCHED pairs

| left | right | left label | right label | operand types | result | ground |
|---|---|---|---|---|---|---|
| cpp/op_1000 | cpp/op_532 | `not_eq` | `!=` | bool,f64 | bool | byte identity |
| cpp/op_2 | cpp/op_26 | `!` | `not` | u64,None | bool | byte identity |
| cpp/op_26 | cpp/op_2 | `not` | `!` | u64,None | bool | byte identity |
| cpp/op_27 | cpp/op_3 | `not` | `!` | f32,None | bool | byte identity |
| cpp/op_28 | cpp/op_4 | `not` | `!` | f64,None | bool | byte identity |
| cpp/op_284 | cpp/op_788 | `||` | `or` | i32,u64 | bool | byte identity |
| cpp/op_290 | cpp/op_794 | `||` | `or` | i64,u64 | bool | byte identity |
| cpp/op_294 | cpp/op_798 | `||` | `or` | u64,i32 | bool | byte identity |
| cpp/op_295 | cpp/op_799 | `||` | `or` | u64,i64 | bool | byte identity |
| cpp/op_296 | cpp/op_800 | `||` | `or` | u64,u64 | bool | byte identity |
| cpp/op_297 | cpp/op_801 | `||` | `or` | u64,f32 | bool | byte identity |
| cpp/op_298 | cpp/op_802 | `||` | `or` | u64,f64 | bool | byte identity |
| cpp/op_299 | cpp/op_803 | `||` | `or` | u64,bool | bool | byte identity |
| cpp/op_3 | cpp/op_27 | `!` | `not` | f32,None | bool | byte identity |
| cpp/op_302 | cpp/op_806 | `||` | `or` | f32,u64 | bool | byte identity |
| cpp/op_308 | cpp/op_812 | `||` | `or` | f64,u64 | bool | byte identity |
| cpp/op_314 | cpp/op_818 | `||` | `or` | bool,u64 | bool | byte identity |
| cpp/op_315 | cpp/op_819 | `||` | `or` | bool,f32 | bool | byte identity |
| cpp/op_316 | cpp/op_820 | `||` | `or` | bool,f64 | bool | byte identity |
| cpp/op_320 | cpp/op_824 | `&&` | `and` | i32,u64 | bool | byte identity |
| cpp/op_326 | cpp/op_830 | `&&` | `and` | i64,u64 | bool | byte identity |
| cpp/op_330 | cpp/op_834 | `&&` | `and` | u64,i32 | bool | byte identity |
| cpp/op_331 | cpp/op_835 | `&&` | `and` | u64,i64 | bool | byte identity |
| cpp/op_332 | cpp/op_836 | `&&` | `and` | u64,u64 | bool | byte identity |
| cpp/op_333 | cpp/op_837 | `&&` | `and` | u64,f32 | bool | byte identity |
| cpp/op_334 | cpp/op_838 | `&&` | `and` | u64,f64 | bool | byte identity |
| cpp/op_335 | cpp/op_839 | `&&` | `and` | u64,bool | bool | byte identity |
| cpp/op_338 | cpp/op_842 | `&&` | `and` | f32,u64 | bool | byte identity |
| cpp/op_344 | cpp/op_848 | `&&` | `and` | f64,u64 | bool | byte identity |
| cpp/op_350 | cpp/op_854 | `&&` | `and` | bool,u64 | bool | byte identity |
| cpp/op_351 | cpp/op_855 | `&&` | `and` | bool,f32 | bool | byte identity |
| cpp/op_352 | cpp/op_856 | `&&` | `and` | bool,f64 | bool | byte identity |
| cpp/op_4 | cpp/op_28 | `!` | `not` | f64,None | bool | byte identity |
| cpp/op_463 | swift/op_511 | `==` | `==` | i32,i64 | bool | z3 over the two lifted forms |
| cpp/op_468 | swift/op_516 | `==` | `==` | i64,i32 | bool | z3 over the two lifted forms |
| cpp/op_500 | cpp/op_968 | `!=` | `not_eq` | i32,u64 | bool | byte identity |
| cpp/op_501 | cpp/op_969 | `!=` | `not_eq` | i32,f32 | bool | byte identity |
| cpp/op_502 | cpp/op_970 | `!=` | `not_eq` | i32,f64 | bool | byte identity |
| cpp/op_503 | cpp/op_971 | `!=` | `not_eq` | i32,bool | bool | byte identity |
| cpp/op_506 | cpp/op_974 | `!=` | `not_eq` | i64,u64 | bool | byte identity |
| cpp/op_507 | cpp/op_975 | `!=` | `not_eq` | i64,f32 | bool | byte identity |
| cpp/op_508 | cpp/op_976 | `!=` | `not_eq` | i64,f64 | bool | byte identity |
| cpp/op_510 | cpp/op_978 | `!=` | `not_eq` | u64,i32 | bool | byte identity |
| cpp/op_511 | cpp/op_979 | `!=` | `not_eq` | u64,i64 | bool | byte identity |
| cpp/op_513 | cpp/op_981 | `!=` | `not_eq` | u64,f32 | bool | byte identity |
| cpp/op_514 | cpp/op_982 | `!=` | `not_eq` | u64,f64 | bool | byte identity |
| cpp/op_515 | cpp/op_983 | `!=` | `not_eq` | u64,bool | bool | byte identity |
| cpp/op_516 | cpp/op_984 | `!=` | `not_eq` | f32,i32 | bool | byte identity |
| cpp/op_517 | cpp/op_985 | `!=` | `not_eq` | f32,i64 | bool | byte identity |
| cpp/op_518 | cpp/op_986 | `!=` | `not_eq` | f32,u64 | bool | byte identity |
| cpp/op_520 | cpp/op_988 | `!=` | `not_eq` | f32,f64 | bool | byte identity |
| cpp/op_521 | cpp/op_989 | `!=` | `not_eq` | f32,bool | bool | byte identity |
| cpp/op_522 | cpp/op_990 | `!=` | `not_eq` | f64,i32 | bool | byte identity |
| cpp/op_523 | cpp/op_991 | `!=` | `not_eq` | f64,i64 | bool | byte identity |
| cpp/op_524 | cpp/op_992 | `!=` | `not_eq` | f64,u64 | bool | byte identity |
| cpp/op_525 | cpp/op_993 | `!=` | `not_eq` | f64,f32 | bool | byte identity |
| cpp/op_527 | cpp/op_995 | `!=` | `not_eq` | f64,bool | bool | byte identity |
| cpp/op_530 | cpp/op_998 | `!=` | `not_eq` | bool,u64 | bool | byte identity |
| cpp/op_531 | cpp/op_999 | `!=` | `not_eq` | bool,f32 | bool | byte identity |
| cpp/op_532 | cpp/op_1000 | `!=` | `not_eq` | bool,f64 | bool | byte identity |
| cpp/op_535 | swift/op_331 | `>` | `>` | i32,i64 | bool | z3 over the two lifted forms |
| cpp/op_540 | swift/op_336 | `>` | `>` | i64,i32 | bool | z3 over the two lifted forms |
| cpp/op_571 | swift/op_403 | `>=` | `>=` | i32,i64 | bool | z3 over the two lifted forms |
| cpp/op_576 | swift/op_408 | `>=` | `>=` | i64,i32 | bool | z3 over the two lifted forms |
| cpp/op_607 | swift/op_367 | `<=` | `<=` | i32,i64 | bool | z3 over the two lifted forms |
| cpp/op_612 | swift/op_372 | `<=` | `<=` | i64,i32 | bool | z3 over the two lifted forms |
| cpp/op_643 | swift/op_295 | `<` | `<` | i32,i64 | bool | z3 over the two lifted forms |
| cpp/op_648 | swift/op_300 | `<` | `<` | i64,i32 | bool | z3 over the two lifted forms |
| cpp/op_788 | cpp/op_284 | `or` | `||` | i32,u64 | bool | byte identity |
| cpp/op_794 | cpp/op_290 | `or` | `||` | i64,u64 | bool | byte identity |
| cpp/op_798 | cpp/op_294 | `or` | `||` | u64,i32 | bool | byte identity |
| cpp/op_799 | cpp/op_295 | `or` | `||` | u64,i64 | bool | byte identity |
| cpp/op_800 | cpp/op_296 | `or` | `||` | u64,u64 | bool | byte identity |
| cpp/op_801 | cpp/op_297 | `or` | `||` | u64,f32 | bool | byte identity |
| cpp/op_802 | cpp/op_298 | `or` | `||` | u64,f64 | bool | byte identity |
| cpp/op_803 | cpp/op_299 | `or` | `||` | u64,bool | bool | byte identity |
| cpp/op_806 | cpp/op_302 | `or` | `||` | f32,u64 | bool | byte identity |
| cpp/op_812 | cpp/op_308 | `or` | `||` | f64,u64 | bool | byte identity |
| cpp/op_818 | cpp/op_314 | `or` | `||` | bool,u64 | bool | byte identity |
| cpp/op_819 | cpp/op_315 | `or` | `||` | bool,f32 | bool | byte identity |
| cpp/op_820 | cpp/op_316 | `or` | `||` | bool,f64 | bool | byte identity |
| cpp/op_824 | cpp/op_320 | `and` | `&&` | i32,u64 | bool | byte identity |
| cpp/op_830 | cpp/op_326 | `and` | `&&` | i64,u64 | bool | byte identity |
| cpp/op_834 | cpp/op_330 | `and` | `&&` | u64,i32 | bool | byte identity |
| cpp/op_835 | cpp/op_331 | `and` | `&&` | u64,i64 | bool | byte identity |
| cpp/op_836 | cpp/op_332 | `and` | `&&` | u64,u64 | bool | byte identity |
| cpp/op_837 | cpp/op_333 | `and` | `&&` | u64,f32 | bool | byte identity |
| cpp/op_838 | cpp/op_334 | `and` | `&&` | u64,f64 | bool | byte identity |
| cpp/op_839 | cpp/op_335 | `and` | `&&` | u64,bool | bool | byte identity |
| cpp/op_842 | cpp/op_338 | `and` | `&&` | f32,u64 | bool | byte identity |
| cpp/op_848 | cpp/op_344 | `and` | `&&` | f64,u64 | bool | byte identity |
| cpp/op_854 | cpp/op_350 | `and` | `&&` | bool,u64 | bool | byte identity |
| cpp/op_855 | cpp/op_351 | `and` | `&&` | bool,f32 | bool | byte identity |
| cpp/op_856 | cpp/op_352 | `and` | `&&` | bool,f64 | bool | byte identity |
| cpp/op_968 | cpp/op_500 | `not_eq` | `!=` | i32,u64 | bool | byte identity |
| cpp/op_969 | cpp/op_501 | `not_eq` | `!=` | i32,f32 | bool | byte identity |
| cpp/op_970 | cpp/op_502 | `not_eq` | `!=` | i32,f64 | bool | byte identity |
| cpp/op_971 | cpp/op_503 | `not_eq` | `!=` | i32,bool | bool | byte identity |
| cpp/op_974 | cpp/op_506 | `not_eq` | `!=` | i64,u64 | bool | byte identity |
| cpp/op_975 | cpp/op_507 | `not_eq` | `!=` | i64,f32 | bool | byte identity |
| cpp/op_976 | cpp/op_508 | `not_eq` | `!=` | i64,f64 | bool | byte identity |
| cpp/op_978 | cpp/op_510 | `not_eq` | `!=` | u64,i32 | bool | byte identity |
| cpp/op_979 | cpp/op_511 | `not_eq` | `!=` | u64,i64 | bool | byte identity |
| cpp/op_981 | cpp/op_513 | `not_eq` | `!=` | u64,f32 | bool | byte identity |
| cpp/op_982 | cpp/op_514 | `not_eq` | `!=` | u64,f64 | bool | byte identity |
| cpp/op_983 | cpp/op_515 | `not_eq` | `!=` | u64,bool | bool | byte identity |
| cpp/op_984 | cpp/op_516 | `not_eq` | `!=` | f32,i32 | bool | byte identity |
| cpp/op_985 | cpp/op_517 | `not_eq` | `!=` | f32,i64 | bool | byte identity |
| cpp/op_986 | cpp/op_518 | `not_eq` | `!=` | f32,u64 | bool | byte identity |
| cpp/op_988 | cpp/op_520 | `not_eq` | `!=` | f32,f64 | bool | byte identity |
| cpp/op_989 | cpp/op_521 | `not_eq` | `!=` | f32,bool | bool | byte identity |
| cpp/op_990 | cpp/op_522 | `not_eq` | `!=` | f64,i32 | bool | byte identity |
| cpp/op_991 | cpp/op_523 | `not_eq` | `!=` | f64,i64 | bool | byte identity |
| cpp/op_992 | cpp/op_524 | `not_eq` | `!=` | f64,u64 | bool | byte identity |
| cpp/op_993 | cpp/op_525 | `not_eq` | `!=` | f64,f32 | bool | byte identity |
| cpp/op_995 | cpp/op_527 | `not_eq` | `!=` | f64,bool | bool | byte identity |
| cpp/op_998 | cpp/op_530 | `not_eq` | `!=` | bool,u64 | bool | byte identity |
| cpp/op_999 | cpp/op_531 | `not_eq` | `!=` | bool,f32 | bool | byte identity |
| go/op_17 | c/op_47 | `!` | `--` | bool,None | bool | z3 over the two lifted forms |
| go/op_456 | cpp/op_462 | `==` | `==` | i32,i32 | bool | z3 over the two lifted forms |
| go/op_463 | cpp/op_469 | `==` | `==` | i64,i64 | bool | z3 over the two lifted forms |
| go/op_470 | cpp/op_476 | `==` | `==` | u64,u64 | bool | z3 over the two lifted forms |
| go/op_491 | cpp/op_497 | `==` | `==` | bool,bool | bool | z3 over the two lifted forms (tier 1) |
| go/op_492 | cpp/op_498 | `!=` | `!=` | i32,i32 | bool | z3 over the two lifted forms |
| go/op_499 | cpp/op_505 | `!=` | `!=` | i64,i64 | bool | z3 over the two lifted forms |
| go/op_506 | cpp/op_512 | `!=` | `!=` | u64,u64 | bool | z3 over the two lifted forms |
| go/op_527 | cpp/op_1001 | `!=` | `not_eq` | bool,bool | bool | z3 over the two lifted forms (tier 1) |
| go/op_528 | cpp/op_642 | `<` | `<` | i32,i32 | bool | z3 over the two lifted forms |
| go/op_535 | cpp/op_649 | `<` | `<` | i64,i64 | bool | z3 over the two lifted forms |
| go/op_542 | cpp/op_656 | `<` | `<` | u64,u64 | bool | z3 over the two lifted forms |
| go/op_636 | cpp/op_570 | `>=` | `>=` | i32,i32 | bool | z3 over the two lifted forms |
| go/op_643 | cpp/op_577 | `>=` | `>=` | i64,i64 | bool | z3 over the two lifted forms |
| go/op_650 | cpp/op_584 | `>=` | `>=` | u64,u64 | bool | z3 over the two lifted forms |
| swift/op_295 | cpp/op_643 | `<` | `<` | i32,i64 | bool | z3 over the two lifted forms |
| swift/op_300 | cpp/op_648 | `<` | `<` | i64,i32 | bool | z3 over the two lifted forms |
| swift/op_331 | cpp/op_535 | `>` | `>` | i32,i64 | bool | z3 over the two lifted forms |
| swift/op_336 | cpp/op_540 | `>` | `>` | i64,i32 | bool | z3 over the two lifted forms |
| swift/op_367 | cpp/op_607 | `<=` | `<=` | i32,i64 | bool | z3 over the two lifted forms |
| swift/op_372 | cpp/op_612 | `<=` | `<=` | i64,i32 | bool | z3 over the two lifted forms |
| swift/op_403 | cpp/op_571 | `>=` | `>=` | i32,i64 | bool | z3 over the two lifted forms |
| swift/op_408 | cpp/op_576 | `>=` | `>=` | i64,i32 | bool | z3 over the two lifted forms |
| swift/op_439 | cpp/op_499 | `!=` | `!=` | i32,i64 | bool | z3 over the two lifted forms |
| swift/op_444 | cpp/op_504 | `!=` | `!=` | i64,i32 | bool | z3 over the two lifted forms |
| swift/op_511 | cpp/op_463 | `==` | `==` | i32,i64 | bool | z3 over the two lifted forms |
| swift/op_516 | cpp/op_468 | `==` | `==` | i64,i32 | bool | z3 over the two lifted forms |
| swift/op_690 | swift/op_726 | `<<` | `>>` | i32,i32 | i32 | byte identity |
| swift/op_691 | swift/op_727 | `<<` | `>>` | i32,i64 | i32 | byte identity |
| swift/op_692 | swift/op_728 | `<<` | `>>` | i32,u64 | i32 | byte identity |
| swift/op_696 | swift/op_732 | `<<` | `>>` | i64,i32 | i64 | byte identity |
| swift/op_697 | swift/op_733 | `<<` | `>>` | i64,i64 | i64 | byte identity |
| swift/op_698 | swift/op_734 | `<<` | `>>` | i64,u64 | i64 | byte identity |
| swift/op_702 | swift/op_738 | `<<` | `>>` | u64,i32 | u64 | byte identity |
| swift/op_726 | swift/op_690 | `>>` | `<<` | i32,i32 | i32 | byte identity |
| swift/op_727 | swift/op_691 | `>>` | `<<` | i32,i64 | i32 | byte identity |
| swift/op_728 | swift/op_692 | `>>` | `<<` | i32,u64 | i32 | byte identity |
| swift/op_732 | swift/op_696 | `>>` | `<<` | i64,i32 | i64 | byte identity |
| swift/op_733 | swift/op_697 | `>>` | `<<` | i64,i64 | i64 | byte identity |
| swift/op_734 | swift/op_698 | `>>` | `<<` | i64,u64 | i64 | byte identity |
| swift/op_738 | swift/op_702 | `>>` | `<<` | u64,i32 | u64 | byte identity |
