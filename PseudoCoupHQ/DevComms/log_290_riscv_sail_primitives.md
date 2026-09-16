# log 290 — the RISC-V model's primitives at the Sail level

## 1. how this was counted

- source: `SOURCES/sail-riscv`, commit `3243f93905c1de3504e910f76c07f96fef1394d7` (2026-09-09), 170 `.sail` files
- read: every `val` declaration in those 170 files, joined across continuation lines — 265 of them
- split: a declaration whose body is an extern (a backend name, not Sail code) against one that is only a type
- then: every name used in call position anywhere in the model, minus every name the repo itself binds
- the Lean side is log 289's; here it is only the cross-check, against `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/sail_primitives_inventory.json`
- **the two commits are not the same.** Our cached Lean emit came from model commit `6266b40c`; this clone is `3243f93` and does not carry `6266b40c` (`git cat-file -t 6266b40c` → not a valid object name). Differences found are named in §6.7.
- Sail's compiler and its library are NOT on this machine (no `sail` binary, no `share/sail`). Every `$include <...>` target is unopened. Anything below that rests on the library file is marked **unverified**.

## 2. the spellings

### 2.1 what the model actually uses

| spelling | count | example |
|---|---|---|
| `val NAME = pure\|impure {backend: "..."} : type` | 114 | `model/core/softfloat_interface.sail:38` |
| `val NAME = pure "name" : type` | 2 | `model/prelude/prelude.sail:56`, `:244` |
| `val "NAME" : type` | 2 | `model/prelude/prelude.sail:180`, `:181` |
| **extern total** | **118** | |
| `$[extern] ...` | 0 | not used at this commit |
| `val extern NAME` | 0 | not used at this commit |
| the bare word `extern` anywhere in a `.sail` file | 0 | |

### 2.2 the qualifier and the backend keys

| field | tally |
|---|---|
| `pure` | 111 |
| `impure` | 5 |
| no qualifier (the `val "NAME"` spelling) | 2 |
| key `cpp` | 114 |
| key `lem` | 79 |
| key `interpreter` | 10 |
| key `c` | 10 |
| key `lean` | 6 |
| key `rocq` | 4 |
| key `_` (every other backend) | 3 |

### 2.3 the rest of the `val` declarations

| kind | count |
|---|---|
| `val NAME : type` with a Sail `function` or `mapping` for it in the repo | 145 |
| `val NAME : type` with no definition anywhere in the repo | 2 |
| **plain total** | **147** |

- the two with no definition: `__TraceMemoryWrite`, `__TraceMemoryRead`, both `model/core/phys_mem_interface.sail:151`–`152`, `forall 'n 'm. (int('n), bits('m), bits(8 * 'n)) -> unit`. Neither is called anywhere in the model.

### 2.4 extern with and without a Sail fallback

| | count |
|---|---|
| extern that ALSO has a Sail `function` body (other backends fall back to it) | 33 |
| extern with no Sail body at all (every backend must write its own) | 85 |

## 3. the primitives

### 3.1 fixed-width values and bit operations

#### 3.1.1 declared extern in the model — 4

| name | Sail type as written | where | Lean key |
|---|---|---|---|
| `sub_vec` | `forall 'n. (bits('n), bits('n)) -> bits('n)` | `model/prelude/prelude.sail:37` | `_lean_sub` |
| `sub_vec_int` | `forall 'n. (bits('n), int) -> bits('n)` | `model/prelude/prelude.sail:39` | `BitVec.subInt` |
| `shift_bits_right` | `forall 'n 'm. (bits('n), bits('m)) -> bits('n)` | `model/prelude/prelude.sail:180` | none |
| `shift_bits_left` | `forall 'n 'm. (bits('n), bits('m)) -> bits('n)` | `model/prelude/prelude.sail:181` | none |

#### 3.1.2 used, never declared — 20 (Sail's library; signatures unverified)

| name | uses | signature we can read in this repo |
|---|---|---|
| `unsigned` | 352 | none; used as `unsigned(x) : int` (`model/prelude/prelude.sail:168`) |
| `signed` | 119 | none; used as `signed(x) : int` (`model/prelude/prelude.sail:164`) |
| `truncate` | 8 | wrapper `val trunc : forall 'm 'n, 'm >= 0 & 'm <= 'n. (implicit('m), bits('n)) -> bits('m)` (`prelude.sail:102`) |
| `count_trailing_zeros` | 6 | none |
| `count_leading_zeros` | 5 | none |
| `get_slice_int` | 4 | wrapper `val to_bits : forall 'l 'x, 'l >= 0 & 0 <= 'x < 2 ^ 'l . (implicit('l), int('x)) -> bits('l)` (`prelude.sail:122`) |
| `vector_update_subrange` | 4 | none |
| `sail_zero_extend` | 3 | wrapper `val zero_extend : forall 'n 'm, 'm >= 'n. (implicit('m), bits('n)) -> bits('m)` (`prelude.sail:89`) |
| `sail_sign_extend` | 1 | wrapper `val sign_extend : forall 'n 'm, 'm >= 'n. (implicit('m), bits('n)) -> bits('m)` (`prelude.sail:88`) |
| `sail_zeros` | 1 | wrapper `val zeros : forall 'n, 'n >= 0 . implicit('n) -> bits('n)` (`prelude.sail:94`) |
| `sail_ones` | 1 | wrapper `val ones : forall 'n, 'n >= 0 . implicit('n) -> bits('n)` (`prelude.sail:97`) |
| `sail_arith_shiftright` | 1 | wrapper `val shift_bits_right_arith : forall 'm 'n, 'n >= 1 . (bits('n), bits('m)) -> bits('n)` (`prelude.sail:186`) |
| `append` | 1 | none |
| `not_bool` | 1 | wrapper `val not : forall ('p : Bool). bool('p) -> bool(not('p))` (`prelude.sail:28`) |
| `and_vec` | overload only | `overload operator & = {and_vec}` (`prelude.sail:31`) |
| `or_vec` | overload only | `overload operator \| = {or_vec}` (`prelude.sail:33`) |
| `xor_vec` | overload only | `overload operator ^ = {xor_vec, concat_str}` (`prelude.sail:35`) |
| `not_vec` | overload only | `overload ~ = {not_bool, not_vec, not_bit}` (`prelude.sail:25`) |
| `sail_shiftleft` | overload only | `overload operator << = {shift_bits_left, sail_shiftleft}` (`prelude.sail:184`) |
| `sail_shiftright` | overload only | `overload operator >> = {shift_bits_right, sail_shiftright}` (`prelude.sail:183`) |

#### 3.1.3 operators with no declaration in the model

| symbol | textual occurrences in the 170 files, comments and strings removed |
|---|---|
| `@` (join two values end to end) | 2946 |
| `==` | 1313 |
| `!=` | 227 |
| `<=` | 382 |
| `>=` | 222 |
| `<<` (not `<<<`) | 69 |
| `>>` (not `>>>`) | 92 |
| `<<<` | 34 |
| `>>>` | 52 |
| `&`, `\|`, `^` | not separable — the same symbols carry type constraints, match arms and string joining; **unverified** |

- the eight signed and unsigned comparisons ARE defined in Sail in the model: `operator <_s` etc., `model/prelude/prelude.sail:155`–`171`, on top of `signed` / `unsigned`

### 3.2 unbounded numbers

#### 3.2.1 declared extern in the model — 4

| name | Sail type as written | where | Lean key |
|---|---|---|---|
| `quot_positive_round_zero` | `forall 'n 'm, 'n >= 0 & 'm > 0. (int('n), int('m)) -> int(div('n, 'm))` | `prelude.sail:43` | `Int.tdiv` |
| `quot_round_zero` | `forall 'm, 'm != 0 . (int, int('m)) -> int` | `prelude.sail:44` | `Int.tdiv` |
| `rem_positive_round_zero` | `forall 'n 'm, 'n >= 0 & 'm > 0. (int('n), int('m)) -> int(mod('n, 'm))` | `prelude.sail:46` | `Int.tmod` |
| `rem_round_zero` | `forall 'm, 'm != 0 . (int, int('m)) -> int` | `prelude.sail:47` | `Int.tmod` |

- these four are the only externs in the model that name both a `lean` and a `rocq` key
- `/` and `%` are bound to the positive forms only, on purpose — `prelude.sail:219`–`224` says division with a negative number is almost always a mistake here

#### 3.2.2 used, never declared — 8 (Sail's library; signatures unverified)

| name | uses | note |
|---|---|---|
| `abs_int` | 7 | size without the sign |
| `mod` | 3 | also a type-level function in constraints |
| `negate` | 2 | |
| `div` | 1 | also a type-level function in constraints |
| `mult_atom` | overload only | `overload operator * = {mult_atom, mult_int}` (`prelude.sail:218`) |
| `mult_int` | overload only | same line |
| `min_int` | overload only | `overload min = {min_int}` (`prelude.sail:53`) |
| `max_int` | overload only | `overload max = {max_int}` (`prelude.sail:54`) |

### 3.3 containers

#### 3.3.1 declared extern in the model — 0

#### 3.3.2 vectors, options, results — 6 used and never declared

| name | uses |
|---|---|
| `Ok` | 285 |
| `Some` | 164 |
| `Err` | 162 |
| `None` | 159 |
| `vector_init` | 20 |
| `length` | 4 |

- from `$include <option.sail>` and Sail's result type — **unverified**, the library files are not on this machine

#### 3.3.3 strings and assembly text — 33 used and never declared

| name | uses | note |
|---|---|---|
| `sep` | 553 | the separator in an assembly mapping |
| `spc` | 350 | a space in an assembly mapping |
| `bits_str` | 80 | |
| `dec_str` | 54 | |
| `opt_spc` | 32 | |
| `hex_str` | 10 | |
| `string_drop` | 2 | |
| `string_length` | 1 | |
| `concat_str` | overload only | `overload operator ^ = {xor_vec, concat_str}` |
| `hex_bits_N` | 13 widths, 58 uses | `_2 _4 _5 _6 _7 _8 _9 _10 _11 _12 _16 _20 _32` |
| `hex_bits_signed_N` | 8 widths, 31 uses | `_5 _6 _9 _10 _12 _13 _20 _21` |
| `dec_bits_N` | 3 widths, 3 uses | `_3 _4 _5` |

- the `hex_bits_*` / `dec_bits_*` families come from `$include <hex_bits.sail>`, `<hex_bits_signed.sail>`, `<dec_bits.sail>` (`model/prelude/prelude.sail:18`–`20`) — **unverified**

### 3.4 machine state

#### 3.4.1 registers

- 195 `register` declarations in the model, all distinct. Reading and writing a register is a Sail language construct, not a `val` — the model declares no primitive for it.
- CSRs are registers among those 195; the CSR dispatch (`read_CSR`, `write_CSR`) is written in Sail in the model.

#### 3.4.2 memory and the concurrency interface — 12 used, never declared

| name | uses | note |
|---|---|---|
| `sail_mem_read` | 2 | instantiated at `model/core/phys_mem_interface.sail:121` |
| `sail_mem_write` | 3 | instantiated at `model/core/phys_mem_interface.sail:73` |
| `sail_barrier` | 12 | instantiated at `model/core/phys_mem_interface.sail:149` |
| `Mem_read_request` | 1 | the request record type |
| `Mem_write_request` | 1 | the request record type |
| `AK_explicit` | 6 | access kind |
| `AK_arch` | 2 | access kind |
| `AK_ifetch` | 1 | access kind |
| `sail_end_cycle` | 3 | `model/postlude/step.sail:316`, `model/main/main.sail:16`, `:37` |
| `sail_instr_announce` | 2 | `model/postlude/step.sail:125`, `:152` |
| `sail_branch_announce` | 1 | `model/core/pc_access.sail:23` |
| `isla_reset_registers` | 1 | from `$include <isla.sail>` |

- all from `$include <concurrency_interface.sail>` / `<isla.sail>` — **unverified**, the library files are not on this machine
- the model's instantiation fixes the types: `'pa = physaddrbits`, `'translation_summary = unit`, `'arch_ak = RISCV_strong_access`, `'abort = unit`, `'barrier = barrier_kind`

#### 3.4.3 the tracing hooks

- `__TraceMemoryWrite` and `__TraceMemoryRead` are declared with no body and never called (§2.3)
- `__ReadRAM_Meta` and `__WriteRAM_Meta` ARE written in Sail in the model

### 3.5 float — the softfloat externs

- one file: `model/core/softfloat_interface.sail`, lines 38–121, **67 declarations**
- every one is `pure`, every one names exactly two backends (`cpp`, `lem`), **none** names `lean` or `rocq`, **none** has a Sail body
- all 67 are called by the model
- the argument types are the file's own names (`model/core/softfloat_interface.sail:22`–`33`): `bits_rm = bits(3)`, `bits_fflags = bits(5)`, `bits_H = bits(16)`, `bits_S = bits(32)`, `bits_D = bits(64)`, `bits_BF16 = bits(16)`, `bits_W`/`bits_WU` `= bits(32)`, `bits_L`/`bits_LU` `= bits(64)`

#### 3.5.1 add, subtract, multiply, divide — 12

| name | Sail type as written |
|---|---|
| `riscv_f16Add` `riscv_f16Sub` `riscv_f16Mul` `riscv_f16Div` | `(bits_rm, bits_H, bits_H) -> (bits_fflags, bits_H)` |
| `riscv_f32Add` `riscv_f32Sub` `riscv_f32Mul` `riscv_f32Div` | `(bits_rm, bits_S, bits_S) -> (bits_fflags, bits_S)` |
| `riscv_f64Add` `riscv_f64Sub` `riscv_f64Mul` `riscv_f64Div` | `(bits_rm, bits_D, bits_D) -> (bits_fflags, bits_D)` |

#### 3.5.2 multiply then add — 3, square root — 3, round to whole — 3

| name | Sail type as written |
|---|---|
| `riscv_f16MulAdd` | `(bits_rm, bits_H, bits_H, bits_H) -> (bits_fflags, bits_H)` |
| `riscv_f32MulAdd` | `(bits_rm, bits_S, bits_S, bits_S) -> (bits_fflags, bits_S)` |
| `riscv_f64MulAdd` | `(bits_rm, bits_D, bits_D, bits_D) -> (bits_fflags, bits_D)` |
| `riscv_f16Sqrt` | `(bits_rm, bits_H) -> (bits_fflags, bits_H)` |
| `riscv_f32Sqrt` | `(bits_rm, bits_S) -> (bits_fflags, bits_S)` |
| `riscv_f64Sqrt` | `(bits_rm, bits_D) -> (bits_fflags, bits_D)` |
| `riscv_f16roundToInt` | `(bits_rm, bits_H, bool) -> (bits_fflags, bits_H)` |
| `riscv_f32roundToInt` | `(bits_rm, bits_S, bool) -> (bits_fflags, bits_S)` |
| `riscv_f64roundToInt` | `(bits_rm, bits_D, bool) -> (bits_fflags, bits_D)` |

#### 3.5.3 compare — 15

| name | Sail type as written |
|---|---|
| `riscv_f16Lt` `riscv_f16Lt_quiet` `riscv_f16Le` `riscv_f16Le_quiet` `riscv_f16Eq` | `(bits_H, bits_H) -> (bits_fflags, bool)` |
| `riscv_f32Lt` `riscv_f32Lt_quiet` `riscv_f32Le` `riscv_f32Le_quiet` `riscv_f32Eq` | `(bits_S, bits_S) -> (bits_fflags, bool)` |
| `riscv_f64Lt` `riscv_f64Lt_quiet` `riscv_f64Le` `riscv_f64Le_quiet` `riscv_f64Eq` | `(bits_D, bits_D) -> (bits_fflags, bool)` |

#### 3.5.4 conversions — 31

| family | count | Sail type shape |
|---|---|---|
| float to signed whole (`riscv_fNToI32`, `riscv_fNToI64`) | 6 | `(bits_rm, bits_<N>) -> (bits_fflags, bits_W\|bits_L)` |
| float to unsigned whole (`riscv_fNToUi32`, `riscv_fNToUi64`) | 6 | `(bits_rm, bits_<N>) -> (bits_fflags, bits_WU\|bits_LU)` |
| signed whole to float (`riscv_i32ToFN`, `riscv_i64ToFN`) | 6 | `(bits_rm, bits_W\|bits_L) -> (bits_fflags, bits_<N>)` |
| unsigned whole to float (`riscv_ui32ToFN`, `riscv_ui64ToFN`) | 6 | `(bits_rm, bits_WU\|bits_LU) -> (bits_fflags, bits_<N>)` |
| float width to float width | 6 | `riscv_f16ToF32` `riscv_f16ToF64` `riscv_f32ToF64` `riscv_f32ToF16` `riscv_f64ToF16` `riscv_f64ToF32` |
| brain float | 1 | `riscv_f32ToBF16 : (bits_rm, bits_S) -> (bits_fflags, bits_BF16)` |
| *(the three `roundToInt` are counted in §3.5.2, not here)* | | |

#### 3.5.5 float tests used and never declared — 9

| name | uses |
|---|---|
| `float_classify` | 10 |
| `float_is_positive` | 5 |
| `float_is_negative` | 5 |
| `float_is_inf` | 3 |
| `float_is_normal` | 3 |
| `float_is_subnormal` | 3 |
| `float_is_zero` | 3 |
| `float_is_qnan` | 2 |
| `float_is_snan` | 2 |

- from `$include <float/interface.sail>` (`model/prelude/prelude.sail:21`) — **unverified**

### 3.6 platform

#### 3.6.1 declared extern with no Sail body — 8

| name | Sail type as written | where | qualifier |
|---|---|---|---|
| `plat_term_write` | `bits(8) -> unit` | `model/sys/platform.sail:240` | `impure` |
| `plat_term_read` | `unit -> bits(8)` | `model/sys/platform.sail:241` | `impure` |
| `load_reservation` | `forall 'n, 0 < 'n < max_mem_access . (physaddrbits, int('n)) -> unit` | `model/sys/sys_reservation.sail:20` | `impure` |
| `match_reservation` | `physaddrbits -> bool` | `model/sys/sys_reservation.sail:21` | `pure` |
| `cancel_reservation` | `unit -> unit` | `model/sys/sys_reservation.sail:22` | `impure` |
| `valid_reservation` | `unit -> bool` | `model/sys/sys_reservation.sail:23` | `pure` |
| `get_16_random_bits` | `unit -> bits(16)` | `model/core/sys_regs.sail:1219` | `impure` |
| `sys_enable_experimental_extensions` | `unit -> bool` | `model/prelude/prelude.sail:244` | `pure` |

| name | call sites in the model |
|---|---|
| `plat_term_write` | 1 — `model/sys/platform.sail:351` |
| `plat_term_read` | **0** |
| `load_reservation` | 1 — `model/sys/vmem_utils.sail:156` |
| `match_reservation` | 1 — `model/sys/vmem_utils.sail:249` |
| `cancel_reservation` | 2 — `model/sys/sys_control.sail:448`, `model/extensions/A/zalrsc_insts.sail:76` |
| `valid_reservation` | 1 — `model/postlude/step.sail:33` |
| `get_16_random_bits` | 1 — `model/extensions/K/zkr_control.sail:35` |
| `sys_enable_experimental_extensions` | 4 — `model/core/extensions.sail:111`, `:168`, `:397`, `:595` |

#### 3.6.2 declared extern WITH a Sail fallback body — 33

| group | count | where |
|---|---|---|
| core callbacks (`fetch_callback`, `mem_read_callback`, `mem_write_callback`, `mem_exception_callback`, `pc_write_callback`, `xreg_full_write_callback`, `csr_full_write_callback`, `csr_full_read_callback`, `redirect_callback`, `trap_callback`, `xret_callback`) | 11 | `model/core/callbacks.sail:13`–`60` |
| page-walk and instret callbacks | 5 | `model/sys/callbacks.sail:17`–`31` |
| TLB callbacks | 4 | `model/sys/vmem_tlb.sail:86`–`95` |
| float register write callback | 1 | `model/extensions/FD/fdext_regs.sail:74` |
| vector register write callback | 1 | `model/extensions/V/vext_regs.sail:24` |
| `get_config_print_*` / `get_config_rvfi` / `get_config_use_abi_names` | 9 | `model/prelude/prelude.sail:68`–`76` |
| `print_log_instr`, `print_step` | 2 | `model/prelude/prelude.sail:62`, `:65` |

- every one of these 33 names only `cpp`. Every other backend gets the Sail body, which does nothing (`() `, `false`, or a plain print).

#### 3.6.3 printing — 2 externs with no Sail body

| name | Sail type as written | where |
|---|---|---|
| `print_string` | `(string, string) -> unit` | `model/prelude/prelude.sail:56` |
| `print_log` | `string -> unit` | `model/prelude/prelude.sail:59` |

#### 3.6.4 printing and ending, used and never declared — 6

| name | uses |
|---|---|
| `assert` | 298 |
| `print_endline` | 133 |
| `print_bits` | 22 |
| `print` | 2 |
| `print_int` | 1 |
| `exit` | 1 |

#### 3.6.5 configuration — a language construct, not a `val`

- `config <key>` reads a value out of the JSON configuration file handed to the compiler
- **426 reads over 235 distinct keys**, comments and strings removed
- the model declares nothing for it; Sail resolves it while compiling

### 3.7 the whole tally

| section | extern declarations | library names used and never declared |
|---|---|---|
| fixed-width values and bit operations | 4 | 20 |
| unbounded numbers | 4 | 8 |
| containers — vectors, options, results | 0 | 6 |
| containers — strings and assembly text | 0 | 33 |
| machine state | 0 | 12 |
| float | 67 | 9 |
| platform | 43 (8 bodyless + 33 with a fallback + 2 printing) | 6 |
| **total** | **118** | **94** |

## 4. where each extern has a body, per backend

### 4.1 the files

| file | lines | what it covers |
|---|---|---|
| `handwritten_support/RiscvExtras.lean` | 118 | 75 `axiom` lines, 5 `def` helpers |
| `handwritten_support/RiscvExtrasExecutable.lean` | 118 | 80 `def` lines — 5 helpers, 72 that `panic`, 3 that answer (`cancel_reservation`, `valid_reservation`, `sys_enable_experimental_extensions`) |
| `handwritten_support/riscv_extras.lem` | 58 | 15 `let` — the 8 platform operations, the two shifts, and printing |
| `handwritten_support/riscv_extras_fdext.lem` | 223 | 67 `let softfloat_*`, **every one of them `fail`** |
| `handwritten_support/riscv_extras_sequential.lem` | 103 | 38 `let` — the same platform names plus `read_ram` / `write_ram` and the memory helpers |
| `handwritten_support/riscv_extras.v` | 34 | 8 `Definition` only |
| `c_emulator/riscv_softfloat.h` / `.cpp` | — | 67 `softfloat_*` symbols, on Berkeley SoftFloat in `dependencies/softfloat` |
| `c_emulator/riscv_platform_if.cpp`, `riscv_model_impl.cpp` | — | the 8 platform operations, as virtual methods |

### 4.2 the coverage

| group | C++ | Lem | Rocq | Lean (proof) | Lean (run) |
|---|---|---|---|---|---|
| 67 float | 67 real | 67 `fail` | **0** | 67 `axiom` | 67 `panic` |
| 8 platform | 8 real | 8 real | 1 (`sys_enable_experimental_extensions`) | 8 `axiom` | 5 `panic`, 3 answer |
| 33 callbacks and config getters | 33 real | Sail fallback | Sail fallback | Sail fallback | Sail fallback |
| `shift_bits_left` / `shift_bits_right` | Sail's own C | 2 real | 2 real | from the lean-sail package | same |
| `print_string`, `print_log` | Sail's own C | real | 1 (`print_string`) | `def print_string := ()` | same |

- the Lean flavour is picked by `--lean-import-file`: `model/CMakeLists.txt:437` takes `RiscvExtras.lean`, `:441` takes `RiscvExtrasExecutable.lean`
- `riscv_extras.v` also defines `get_time_ns`, `mults_vec`, `mult_vec` — none of the three is declared or used anywhere in the model at this commit

## 5. the Sail level against the Lean level

### 5.1 what agrees

| claim | Sail level | Lean level (`sail_primitives_inventory.json`) |
|---|---|---|
| operations with no body anywhere | 67 float + 8 platform = 75 | `axioms` = 75, names identical |
| float declarations | 67 | 67 names starting `riscv_` |
| platform declarations | 8 | the same 8 names |
| the axioms are copied, not generated | `handwritten_support/RiscvExtras.lean` holds 75 `axiom` lines | the emit carries `LeanIM/RiscvExtras.lean` verbatim, 75 `axiom` lines |
| `quot_*` / `rem_*` reach Lean's own division | keys `lean: "Int.tdiv"` / `"Int.tmod"` | `Int.tdiv` 71, `Int.tmod` 35 occurrences in the emit |
| `sub_vec_int` reaches Lean's own | key `lean: "BitVec.subInt"` | `BitVec.subInt` 11 occurrences in the emit |
| `shift_bits_left` / `shift_bits_right` have no Lean key and no Sail body | 2 declarations, no key | 12 and 10 occurrences in the emit, 0 definitions — supplied by the lean-sail package |

### 5.2 what disagrees

| # | the disagreement |
|---|---|
| 1 | `plat_term_read` is `unit -> bits(8)` in Sail (`model/sys/platform.sail:241`) and `Unit → SailM String` in Lean (`handwritten_support/RiscvExtras.lean:32`). Both files are in the SAME commit. |
| 2 | `plat_term_write` is `bits(8) -> unit` in Sail and `{α} : α → SailM Unit` in Lean (`handwritten_support/RiscvExtras.lean:31`) — the width is gone. |
| 3 | `load_reservation` / `match_reservation` take `physaddrbits` in Sail (`model/sys/sys_reservation.sail:20`–`21`) and `Arch.pa` in Lean (`handwritten_support/RiscvExtras.lean:35`–`36`). Whether the two are the same type cannot be checked here — Lean is not run in this session. **unverified** |
| 4 | the inventory gives three different counts of the same thing: `axioms` dict = 75, `counts.axioms` = 74, group `declared with no body (axiom)` = 72. |
| 5 | log 289 §2.5 says 73 of the 75 are reached from the execute clauses. The inventory's own group says **72**. The three never reached are `plat_term_read`, `plat_term_write`, `valid_reservation`. |
| 6 | `sail_end_cycle` is called 3 times in the model and appears **0** times in the cached emit. |
| 7 | `sub_vec` carries `lean: "_lean_sub"` at `3243f93`. Neither `_lean_sub` nor `sub_vec` appears anywhere in the `6266b40c` emit. Whether the key existed at `6266b40c` cannot be checked — that commit is not in this clone. **unverified** |

### 5.3 what the Sail level has that the Lean level does not show as a primitive

| name | why |
|---|---|
| `hex_bits_N`, `dec_bits_N`, `sep`, `spc`, `opt_spc` | Sail's library writes them IN SAIL; they arrive in the emit as `<name>_forwards` / `_backwards` pairs (`LeanIM/HexBits.lean`, `LeanIM/Mapping.lean`) |
| `and_vec`, `or_vec`, `xor_vec`, `not_vec`, `sail_shiftleft`, `sail_shiftright`, `sail_arith_shiftright`, `mult_atom`, `mult_int`, `min_int`, `max_int`, `concat_str`, `sail_zeros`, `sail_zero_extend`, `vector_update_subrange`, `bits_str`, `dec_str`, `hex_str`, `string_drop`, `isla_reset_registers` | 0 occurrences in the emit — the Lean backend rewrites each into a Lean operation before printing, so the Sail name never appears |
| `config <key>` | resolved while compiling. `config extensions.Zibi.supported` is printed as the literal `(true : Bool)` — `LeanIM/PlatformConfig.lean:1191` |

## 6. the problems

### 6.1 the 67 float operations have no meaning in any prover

- no Sail body; no `lean` key; no `rocq` key; Rocq's handwritten file defines **0** of them; Lem defines all 67 as `fail`; Lean's proof flavour states all 67 as `axiom`
- consequence: an arch-opcode that touches float has no value we can compute on any proof path the model ships.

### 6.2 the 8 platform operations have no meaning in any prover

- terminal read and write, the four reservation operations, random bits, the experimental-extensions flag
- Rocq defines 1 of the 8; Lean states all 8 as `axiom`; the runnable Lean flavour makes 5 of them `panic`
- consequence: the atomic arch-opcodes (`lr` / `sc`) and the system arch-opcodes cannot be expressed as a value.

### 6.3 the configuration is baked in and then vanishes

- 426 `config` reads over 235 distinct keys, resolved by the compiler into literals
- consequence: the emit we hold is ONE machine (`rv64d_v256_e64`), not the family. A claim proved on it says nothing about any other configuration, and there is no primitive left to quantify over.

### 6.4 94 operations the model uses have no signature we can read

- Sail's compiler and its library are not on this machine; every `$include <...>` is unopened
- consequence: for `unsigned` (352 uses), `signed` (119), `truncate` (8) and 91 others we have the model's use and the model's own wrapper type, and nothing authoritative. Every statement about them in this log is inferred, not read.

### 6.5 the same operation has two types in the same commit

- `plat_term_read`: `unit -> bits(8)` in Sail, `Unit → SailM String` in Lean, both at `3243f93`. `plat_term_write` loses `bits(8)` to a type variable.
- consequence: the width is dropped exactly where log 281's gate already found `operator_for` dropping holder widths. A width that is not carried cannot be checked.

### 6.6 the counts on the Lean side do not agree with each other

- 75 / 74 / 72 for the same set, inside one file; log 289 reported a fourth number, 73
- consequence: any figure quoted from that inventory has to be re-derived before it is used.

### 6.7 the two commits are not interchangeable

- the emit is `6266b40c`, this clone is `3243f93`, and `6266b40c` is not an object in this clone
- found at `3243f93` and absent from the emit: the `lean: "_lean_sub"` key on `sub_vec`; `sail_end_cycle`
- consequence: a primitive read off `3243f93` cannot be assumed present in the cached emit without checking the emit for it by name.

### 6.8 two declarations go nowhere

- `__TraceMemoryWrite`, `__TraceMemoryRead`: declared, no body, never called. `plat_term_read`: declared extern, never called.
- consequence: three of the leaves are not reachable from any arch-opcode, so three of the 75 need no meaning at all.

## 7. pointers

- the clone: `SOURCES/sail-riscv`, commit `3243f93`
- the extern declarations: `model/core/softfloat_interface.sail` (67), `model/prelude/prelude.sail` (22), `model/core/callbacks.sail` (11), `model/sys/callbacks.sail` (5), `model/sys/sys_reservation.sail` (4), `model/sys/vmem_tlb.sail` (4), `model/sys/platform.sail` (2), `model/core/sys_regs.sail` (1), `model/extensions/FD/fdext_regs.sail` (1), `model/extensions/V/vext_regs.sail` (1)
- the model's own prelude and what it pulls in: `model/prelude/prelude.sail:11`–`21`, thirteen `$include <...>` lines
- the backend bodies: `handwritten_support/`, `c_emulator/riscv_softfloat.cpp`, `c_emulator/riscv_platform_if.cpp`
- which Lean flavour the build takes: `model/CMakeLists.txt:437` and `:441`
- the Lean side: log 289, and `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/sail_primitives_inventory.json`
- the cached emit and its provenance: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/MANIFEST.md`
