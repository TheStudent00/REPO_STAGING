# transfer.md -- what carried from x86 to riscv64, measured

Task rv2, node `hq.research.arch_unit_oracle`. Written by `transfer.py`; never hand-edited. Every figure below is read out of this folder's own json.

**The hypothesis this measures, the owner 2026-09-10, LITERAL:** *"If we already know what is proven in x86 with their combination of high-level compiler-operators to emulate arch-opcodes, it should also be true in RISC-V ... it should shrink the workload substantially."*

## 1. The two model tables, and the join between them

Table 1 -- the RISC-V model table, as `model_table_rv.py` swept it.

| what | count |
|---|---|
| sweep attempts | 1512 |
| rows NOT_SPELLED | 88 |
| rows NO_BUILDER | 70 |
| rows REFUSED | 1034 |
| rows TRANSLATED | 320 |
| mnemonics in the reference's table | 108 |
| CELLS -- distinct (`mnem`, shape, `key_width`) with at least one written place | 255 |

Table 2 -- the twin, by TERM, in its two readings. READING 1 is the whole written place; READING 2 cuts both sides to the RISC-V cell's own `key_width`. RISC-V writes all 64 bits of a register and its 32-bit forms SIGN-extend, where x86's 32-bit write ZERO-extends, so at the whole place a `w` form can never twin an x86 32-bit form.

| twin | reading 1 | reading 2 |
|---|---|---|
| TEXT | 101 | 158 |
| Z3 | 1 | 3 |
| NONE | 153 | 94 |
| **cells with a twin** | **102** | **161** |
| **of** | **255** | **255** |

Table 3 -- the cells with NO twin under either reading, by mnemonic.

| `mnem` | untwinned shapes |
|---|---|
| `auipc` | 1 |
| `beq` | 4 |
| `bge` | 4 |
| `bgeu` | 4 |
| `blt` | 4 |
| `bltu` | 4 |
| `bne` | 4 |
| `czero.eqz` | 1 |
| `czero.nez` | 2 |
| `div` | 2 |
| `divu` | 2 |
| `divuw` | 2 |
| `divw` | 2 |
| `fadd.d` | 1 |
| `fcvt.d.l` | 1 |
| `fcvt.d.lu` | 1 |
| `fcvt.d.s` | 2 |
| `fcvt.d.w` | 1 |
| `fcvt.d.wu` | 1 |
| `fcvt.s.d` | 2 |
| `fcvt.s.lu` | 1 |
| `fcvt.s.w` | 1 |
| `fcvt.s.wu` | 1 |
| `fdiv.d` | 1 |
| `feq.d` | 1 |
| `feq.s` | 1 |
| `fle.d` | 1 |
| `fle.s` | 1 |
| `flt.d` | 1 |
| `flt.s` | 1 |
| `fmul.d` | 1 |
| `fsub.d` | 1 |
| `jal` | 8 |
| `jalr` | 8 |
| `lui` | 1 |
| `mulh` | 1 |
| `mulhsu` | 2 |
| `mulhu` | 1 |
| `rem` | 2 |
| `remu` | 2 |
| `remuw` | 1 |
| `remw` | 1 |
| `sll` | 1 |
| `sllw` | 1 |
| `slt` | 1 |
| `slti` | 1 |
| `sltiu` | 1 |
| `sltu` | 1 |
| `sra` | 1 |
| `sraw` | 1 |
| `srl` | 1 |
| `srlw` | 1 |

## 2. The inheritance -- section 2.3 of the brief

Every preferred `proved`/`agreed` certificate in the bank whose x86 cell a RISC-V cell twins: the certificate's own SOURCE taken unchanged, compiled for riscv64 at the corpus's ship flags, carved, lifted with the RISC-V reference, and gated by z3 against the certificate's own x86-64 body, both as functions of the same arguments.

Table 4 -- the inherited certificates, per target.

| target | certificates | outcome |
|---|---|---|
| `c` | 32 | proved / PROVED |
| `c` | 15 | refused / BUILD_REFUSED |
| `c` | 11 | refused / WALK_REFUSED |
| `cpp` | 54 | refused / NOT_ATTEMPTED |
| `cpython` | 62 | agreed / TRANSFERS_AS_IT_IS |
| `csharp` | 62 | agreed / TRANSFERS_AS_IT_IS |
| `dart` | 62 | agreed / TRANSFERS_AS_IT_IS |
| `go` | 71 | proved / PROVED |
| `java` | 62 | agreed / TRANSFERS_AS_IT_IS |
| `javascript` | 62 | agreed / TRANSFERS_AS_IT_IS |
| `php` | 62 | agreed / TRANSFERS_AS_IT_IS |
| `ruby` | 62 | agreed / TRANSFERS_AS_IT_IS |
| `rust` | 61 | refused / BUILD_REFUSED |
| `swift` | 56 | refused / NOT_ATTEMPTED |

Table 5 -- the inheritance, in one line per number.

| what | count |
|---|---|
| certificates attempted | 734 |
| PROVED on riscv64, at the cell's own `key_width` | 103 |
| DISPROVED on riscv64 | 0 |
| transferred as they are (interpreted targets) | 434 |
| refused, with a cause | 197 |
| of the PROVED, also proved at the WHOLE written place | 83 |
| of the PROVED, differing above the operation's own width | 20 |
| distinct RISC-V cells with an inherited PROVED certificate | 34 |
| distinct RISC-V cells with an inherited `agreed` certificate | 33 |

Table 6 -- every refusal, by cause. A refusal is a FLAG, not a verdict.

| target | cause | rows |
|---|---|---|
| `c` | BUILD_REFUSED | 15 |
| `c` | WALK_REFUSED | 11 |
| `cpp` | NOT_ATTEMPTED | 54 |
| `rust` | BUILD_REFUSED | 61 |
| `swift` | NOT_ATTEMPTED | 56 |

Table 7 -- the one interpreter's handful, re-run (`interp_recheck.json`). A check at points, NOT a proof.

| `mnem` | shape | `key_width` | place | outcome | agreements / points |
|---|---|---|---|---|---|
| `add` | gpr_gpr | 32 | reg_rdi | AGREES_AT_EVERY_POINT | 200 / 200 |
| `imul` | gpr_gpr | 32 | reg_rdi | AGREES_AT_EVERY_POINT | 200 / 200 |
| `sar` | cl_gpr | 32 | reg_rdi | AGREES_AT_EVERY_POINT | 200 / 200 |
| `shr` | cl_gpr | 64 | reg_rdi | AGREES_AT_EVERY_POINT | 200 / 200 |
| `addss` | xmm_xmm | 32 | reg_xmm0 | THE_CERTIFICATE_IS_ABOUT_A_RE_POSED_TERM | 0 / 0 |
| `cvtsi2sd` | gpr_xmm | 64 | reg_xmm0 | THE_CERTIFICATE_IS_ABOUT_A_RE_POSED_TERM | 0 / 0 |

## 3. The loop on the delta -- section 2.4 of the brief

`find_emulation` over the RISC-V cells with no twin under either reading, on c and go, both routes -- the term rendered by `handful`'s own renderer, and, where the corpus attests a riscv64 SINGLETON for the cell, that probe's own source.

Table 8 -- the loop's own counts.

| what | count |
|---|---|
| cells with no twin | 94 |
| runs (cells x written places x targets) | 188 |
| runs proved | 135 |
| runs refused | 42 |
| runs sat | 11 |
| distinct cells PROVED by the loop | 82 |
| riscv64 singletons the corpus attests | 31 |
| riscv64 cells the corpus attests | 57 |

Table 9 -- the corpus compiled for riscv64 (`attest_rv.json`), and the two builds' agreement.

| what | count |
|---|---|
| `c` probes in the manifest | 750 |
| `c` probes attempted for riscv64 | 500 |
| `c` probes the x86 unit store holds a ship body for | 610 |
| `go` probes in the manifest | 744 |
| `go` probes attempted for riscv64 | 744 |
| `go` probes the x86 unit store holds a ship body for | 107 |
| c|x86_body=False|riscv64_built=False | 100 |
| c|x86_body=True|riscv64_built=True | 400 |
| go|x86_body=False|riscv64_built=False | 637 |
| go|x86_body=True|riscv64_built=True | 107 |

## 4. The count -- section 2.5 of the brief

Table 10 -- the shrinkage of the workload, as a number.

| what | cells | share of the 255 RISC-V cells |
|---|---|---|
| RISC-V cells with at least one written place | 255 | 100% |
| with an x86 twin, READING 1 (the whole written place) | 102 | 40.0% |
| with an x86 twin, READING 2 (at the cell's own `key_width`) | 161 | 63.1% |
| reached by an INHERITED certificate (proved or agreed) | 34 | 13.3% |
| twinned, but the x86 bank holds NO proved or agreed certificate for the twin | 127 | 49.8% |
| the loop still had to run (the untwinned) | 94 | 36.9% |
| PROVED by the loop | 82 | 32.2% |
| **with at least one proved riscv64 emulation, from either route** | **116** | **45.5%** |
| **with none yet** | **139** | **54.5%** |

**The shrinkage, in three sentences, each with its reading.** Of the 255 RISC-V cells, 161 (63.1%) have an x86 cell that computes the same term at the cell's own width, so the LOOP had to be run on only 94 (36.9%) of them -- and that is the number the hypothesis asked for. What ACTUALLY arrived by inheritance is smaller and its reason is not the transfer: only 34 cells (13.3%) had an x86 twin the BANK holds a proved or agreed certificate for, because the x86 loop has itself proved only part of its own table, so 127 twinned cells have a twin and nothing yet to inherit from it. Between the two routes 116 cells (45.5%) now carry at least one proved riscv64 emulation and 139 do not.

Table 11 -- THE THREE READINGS of the polyfill-complete set, RISC-V beside x86. On RISC-V the three COINCIDE, and the reason is one fact: **the architecture has no flags register**, so a RISC-V cell writes exactly one place. Strict (every written place), destination-only (the destination alone) and corpus-needed (the destination plus the flags wherever a consumer reads them) are three ways of saying the same thing when there is one place and no flags.

| reading | what it counts | RISC-V | x86 |
|---|---|---|---|
| strict | every written place proved | 74 | 2007 |
| destination | the destination place proved | 74 | 2265 |
| corpus | the destination proved, and the flags wherever the corpus shows a consumer reading them | 74 | 2221 |

The x86 column is the bank's own count of proved (cell, target) PAIRS as `certificates.json` records it, and the RISC-V column counts CELLS with every written place proved or agreed on both compiled targets -- the two are not the same population and are printed side by side rather than divided.

Table 12 -- what the x86 bank held when this task read it.

| what | value |
|---|---|
| the bank file | `certificates.jsonl` |
| its sha256 | `bfd80360c0afdb4e6d2d227d6ea399f9781fcd0671dc121d676c18e02c2d49b8` |
| certificates in it | 24758 |
| keys in it | 8177 |
| the x86 reference this task walked with | `PseudoCoupHQ/Research/oracle/arch_opcodes/level0/ref2_originals/reference.py` |
| its sha256 | `3893363145df57944286222c18756465757d4e69a6eea0783e0f03265b7156e0` |

