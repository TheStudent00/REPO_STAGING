# compiler_operators_used

| compiler | written in | source files parsed | offered (grammar total) | offered, lowered by the corpus | used in own source | used ∩ lowered | in lowered, never used | used, not in lowered |
|---|---|---|---|---|---|---|---|---|
| clang/llvm (c, cpp) | cpp | 561 (SPARSE: llvm/lib/CodeGen/SelectionDAG, llvm/include/llvm/{CodeGen,IR,MC,Target} only) | 65 | 32 | 41 | 23 | 9 | 18 |
| go (cmd/compile) | go | 734 (full checkout (11,622 files); this row = src/cmd/compile only) | 51 | 20 | 26 | 20 | 0 | 6 |
| go (standard library, rest of checkout) | go | 7339 (full checkout (11,622 files); this row = everything except src/cmd/compile) | 51 | 20 | 26 | 20 | 0 | 6 |
| rustc | rust | 187 (SPARSE: compiler/rustc_codegen_{cranelift,llvm,ssa} only (187 files)) | 51 | 21 | 29 | 20 | 1 | 9 |
| swiftc (compiler) | cpp | 2118 (full checkout (21,854 files); this row = lib/ + include/) | 65 | 32 | 41 | 24 | 8 | 17 |
| swift (standard library) | swift | 403 (full checkout (403 .swift files under stdlib/); every .swift file parsed) | 61 | 26 | 36 | 25 | 1 | 11 |

## clang/llvm (c, cpp)

- parse failures: 0 (sample: [])
- **used ∩ lowered** (23):
    - `!` -- 4280 occurrences in 200 files
    - `!=` -- 2360 occurrences in 162 files
    - `%` -- 182 occurrences in 16 files
    - `&` -- 1894 occurrences in 237 files
    - `&&` -- 7610 occurrences in 220 files
    - `*` -- 3130 occurrences in 214 files
    - `+` -- 1619 occurrences in 108 files
    - `++` -- 1063 occurrences in 91 files
    - `-` -- 1077 occurrences in 104 files
    - `--` -- 109 occurrences in 24 files
    - `/` -- 373 occurrences in 34 files
    - `<` -- 1087 occurrences in 144 files
    - `<<` -- 2146 occurrences in 93 files
    - `<=` -- 338 occurrences in 69 files
    - `==` -- 7627 occurrences in 214 files
    - `>` -- 556 occurrences in 112 files
    - `>=` -- 406 occurrences in 70 files
    - `>>` -- 53 occurrences in 21 files
    - `^` -- 15 occurrences in 9 files
    - `sizeof` -- 68 occurrences in 24 files
    - `|` -- 252 occurrences in 46 files
    - `||` -- 2937 occurrences in 156 files
    - `~` -- 269 occurrences in 83 files
- **in lowered, never used** (9):
    - `<=>` -- 0 occurrences in 0 files
    - `and` -- 0 occurrences in 0 files
    - `bitand` -- 0 occurrences in 0 files
    - `bitor` -- 0 occurrences in 0 files
    - `compl` -- 0 occurrences in 0 files
    - `not` -- 0 occurrences in 0 files
    - `not_eq` -- 0 occurrences in 0 files
    - `or` -- 0 occurrences in 0 files
    - `xor` -- 0 occurrences in 0 files
- **used, not in lowered** (18):
    - `%=` -- 1 occurrences in 1 files
    - `&=` -- 91 occurrences in 20 files
    - `*=` -- 18 occurrences in 8 files
    - `+=` -- 256 occurrences in 38 files
    - `,` -- 107 occurrences in 27 files
    - `-=` -- 52 occurrences in 12 files
    - `->` -- 17444 occurrences in 206 files
    - `.` -- 44457 occurrences in 321 files
    - `.*` -- 3 occurrences in 1 files
    - `...` -- 143 occurrences in 19 files
    - `/=` -- 6 occurrences in 3 files
    - `<<=` -- 16 occurrences in 6 files
    - `=` -- 9026 occurrences in 253 files
    - `>>=` -- 12 occurrences in 7 files
    - `^=` -- 6 occurrences in 2 files
    - `delete` -- 62 occurrences in 42 files
    - `new` -- 122 occurrences in 30 files
    - `|=` -- 166 occurrences in 35 files

## go (cmd/compile)

- parse failures: 0 (sample: [])
- **used ∩ lowered** (20):
    - `!` -- 11630 occurrences in 355 files
    - `!=` -- 28435 occurrences in 517 files
    - `%` -- 798 occurrences in 65 files
    - `&` -- 4540 occurrences in 373 files
    - `&&` -- 7405 occurrences in 309 files
    - `&^` -- 74 occurrences in 22 files
    - `*` -- 1960 occurrences in 220 files
    - `+` -- 6780 occurrences in 359 files
    - `-` -- 10402 occurrences in 352 files
    - `/` -- 766 occurrences in 87 files
    - `<` -- 2539 occurrences in 315 files
    - `<<` -- 1668 occurrences in 143 files
    - `<=` -- 3840 occurrences in 139 files
    - `==` -- 11054 occurrences in 455 files
    - `>` -- 2020 occurrences in 271 files
    - `>=` -- 1749 occurrences in 173 files
    - `>>` -- 1173 occurrences in 56 files
    - `^` -- 476 occurrences in 51 files
    - `|` -- 738 occurrences in 90 files
    - `||` -- 5428 occurrences in 301 files
- **in lowered, never used** (0):
    - (none)
- **used, not in lowered** (6):
    - `++` -- 1053 occurrences in 268 files
    - `--` -- 210 occurrences in 104 files
    - `.` -- 279348 occurrences in 643 files
    - `...` -- 443 occurrences in 123 files
    - `:=` -- 90306 occurrences in 600 files
    - `<-` -- 53 occurrences in 14 files

## go (standard library, rest of checkout)

- parse failures: 0 (sample: [])
- **used ∩ lowered** (20):
    - `!` -- 16386 occurrences in 2415 files
    - `!=` -- 64968 occurrences in 3852 files
    - `%` -- 1357 occurrences in 464 files
    - `&` -- 39557 occurrences in 3225 files
    - `&&` -- 16882 occurrences in 2083 files
    - `&^` -- 576 occurrences in 168 files
    - `*` -- 19522 occurrences in 2249 files
    - `+` -- 34693 occurrences in 2604 files
    - `-` -- 29275 occurrences in 2427 files
    - `/` -- 3675 occurrences in 833 files
    - `<` -- 13968 occurrences in 2282 files
    - `<<` -- 12668 occurrences in 1084 files
    - `<=` -- 4107 occurrences in 968 files
    - `==` -- 38719 occurrences in 3268 files
    - `>` -- 9257 occurrences in 1951 files
    - `>=` -- 3982 occurrences in 1218 files
    - `>>` -- 4447 occurrences in 572 files
    - `^` -- 1868 occurrences in 342 files
    - `|` -- 19022 occurrences in 768 files
    - `||` -- 11128 occurrences in 1969 files
- **in lowered, never used** (0):
    - (none)
- **used, not in lowered** (6):
    - `++` -- 9614 occurrences in 1816 files
    - `--` -- 1265 occurrences in 506 files
    - `.` -- 514793 occurrences in 5584 files
    - `...` -- 2649 occurrences in 785 files
    - `:=` -- 132313 occurrences in 4699 files
    - `<-` -- 4281 occurrences in 462 files

## rustc

- parse failures: 0 (sample: [])
- **used ∩ lowered** (20):
    - `!` -- 3440 occurrences in 157 files
    - `!=` -- 205 occurrences in 71 files
    - `%` -- 5 occurrences in 4 files
    - `&` -- 2837 occurrences in 143 files
    - `&&` -- 375 occurrences in 67 files
    - `*` -- 606 occurrences in 95 files
    - `+` -- 181 occurrences in 56 files
    - `-` -- 184 occurrences in 41 files
    - `..` -- 151 occurrences in 47 files
    - `..=` -- 2 occurrences in 2 files
    - `/` -- 20 occurrences in 13 files
    - `<` -- 50 occurrences in 27 files
    - `<<` -- 21 occurrences in 13 files
    - `<=` -- 8 occurrences in 6 files
    - `==` -- 665 occurrences in 100 files
    - `>` -- 63 occurrences in 27 files
    - `>=` -- 30 occurrences in 16 files
    - `>>` -- 20 occurrences in 11 files
    - `|` -- 106 occurrences in 14 files
    - `||` -- 213 occurrences in 57 files
- **in lowered, never used** (1):
    - `^` -- 0 occurrences in 0 files
- **used, not in lowered** (9):
    - `&=` -- 2 occurrences in 2 files
    - `+=` -- 64 occurrences in 16 files
    - `-=` -- 4 occurrences in 2 files
    - `.` -- 28036 occurrences in 163 files
    - `::` -- 16374 occurrences in 182 files
    - `=` -- 422 occurrences in 76 files
    - `?` -- 222 occurrences in 35 files
    - `as` -- 691 occurrences in 92 files
    - `|=` -- 49 occurrences in 8 files

## swiftc (compiler)

- parse failures: 0 (sample: [])
- **used ∩ lowered** (24):
    - `!` -- 27739 occurrences in 1242 files
    - `!=` -- 7688 occurrences in 999 files
    - `%` -- 75 occurrences in 45 files
    - `&` -- 5612 occurrences in 799 files
    - `&&` -- 17265 occurrences in 1127 files
    - `*` -- 13669 occurrences in 1068 files
    - `+` -- 4539 occurrences in 541 files
    - `++` -- 3236 occurrences in 571 files
    - `-` -- 1799 occurrences in 425 files
    - `--` -- 343 occurrences in 153 files
    - `/` -- 199 occurrences in 83 files
    - `<` -- 1999 occurrences in 548 files
    - `<<` -- 20524 occurrences in 667 files
    - `<=` -- 698 occurrences in 231 files
    - `==` -- 18507 occurrences in 1201 files
    - `>` -- 1408 occurrences in 409 files
    - `>=` -- 890 occurrences in 314 files
    - `>>` -- 195 occurrences in 66 files
    - `^` -- 44 occurrences in 24 files
    - `and` -- 1 occurrences in 1 files
    - `sizeof` -- 780 occurrences in 151 files
    - `|` -- 1760 occurrences in 171 files
    - `||` -- 8777 occurrences in 876 files
    - `~` -- 395 occurrences in 116 files
- **in lowered, never used** (8):
    - `<=>` -- 0 occurrences in 0 files
    - `bitand` -- 0 occurrences in 0 files
    - `bitor` -- 0 occurrences in 0 files
    - `compl` -- 0 occurrences in 0 files
    - `not` -- 0 occurrences in 0 files
    - `not_eq` -- 0 occurrences in 0 files
    - `or` -- 0 occurrences in 0 files
    - `xor` -- 0 occurrences in 0 files
- **used, not in lowered** (17):
    - `&=` -- 140 occurrences in 58 files
    - `*=` -- 23 occurrences in 8 files
    - `+=` -- 1192 occurrences in 257 files
    - `,` -- 1912 occurrences in 64 files
    - `-=` -- 147 occurrences in 80 files
    - `->` -- 110986 occurrences in 1258 files
    - `.` -- 185678 occurrences in 1495 files
    - `.*` -- 15 occurrences in 5 files
    - `...` -- 598 occurrences in 136 files
    - `/=` -- 8 occurrences in 6 files
    - `<<=` -- 11 occurrences in 7 files
    - `=` -- 30278 occurrences in 1189 files
    - `>>=` -- 16 occurrences in 7 files
    - `^=` -- 44 occurrences in 11 files
    - `delete` -- 136 occurrences in 82 files
    - `new` -- 2853 occurrences in 489 files
    - `|=` -- 1409 occurrences in 275 files

## swift (standard library)

- parse failures: 0 (sample: [])
- **used ∩ lowered** (25):
    - `!` -- 1017 occurrences in 187 files
    - `!=` -- 592 occurrences in 146 files
    - `%` -- 57 occurrences in 25 files
    - `&` -- 1148 occurrences in 179 files
    - `&&` -- 568 occurrences in 129 files
    - `*` -- 141 occurrences in 52 files
    - `+` -- 935 occurrences in 154 files
    - `-` -- 769 occurrences in 133 files
    - `...` -- 170 occurrences in 46 files
    - `..<` -- 699 occurrences in 108 files
    - `/` -- 152 occurrences in 57 files
    - `<` -- 972 occurrences in 176 files
    - `<<` -- 92 occurrences in 22 files
    - `<=` -- 374 occurrences in 94 files
    - `==` -- 1609 occurrences in 217 files
    - `>` -- 620 occurrences in 146 files
    - `>=` -- 408 occurrences in 106 files
    - `>>` -- 61 occurrences in 25 files
    - `??` -- 85 occurrences in 45 files
    - `^` -- 17 occurrences in 7 files
    - `consume` -- 16 occurrences in 5 files
    - `try` -- 1292 occurrences in 133 files
    - `|` -- 129 occurrences in 32 files
    - `||` -- 265 occurrences in 92 files
    - `~` -- 69 occurrences in 26 files
- **in lowered, never used** (1):
    - `try!` -- 0 occurrences in 0 files
- **used, not in lowered** (11):
    - `!==` -- 1 occurrences in 1 files
    - `+=` -- 633 occurrences in 112 files
    - `-=` -- 57 occurrences in 29 files
    - `.` -- 26911 occurrences in 367 files
    - `=` -- 4203 occurrences in 288 files
    - `===` -- 30 occurrences in 13 files
    - `as` -- 203 occurrences in 42 files
    - `as!` -- 53 occurrences in 20 files
    - `as?` -- 114 occurrences in 37 files
    - `await` -- 205 occurrences in 37 files
    - `is` -- 33 occurrences in 15 files
