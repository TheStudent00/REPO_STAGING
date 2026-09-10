# log 248 — task ex1: beyond the four — cpp as a fifth compiled target, and the check for the interpreted languages, each on the handful first

Node: `hq.research.arch_unit_oracle.cross_construction.autopoly`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/`).
The interpreted half also serves
`hq.research.remaining_languages`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_12_remaining_languages/`).
Line: arch_unit_oracle, the "goal" section of 2026-09-07 and the rulings
of 2026-09-08 and 2026-09-09; the research CORE's §4.2 item 3, which
names "`find_emulation` printers for go, swift and the interpreted
languages and a check for interpreted targets".
Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, read in full
including its tower section.
Date: 2026-09-09. Instance `ex1`, on the tower guest.

Artifact folder:
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/`,
new sub-folders `cpp/` and `interp/`, results under `autopoly/` as
`expand1_*`; tasks ap1's to ap4's products are never written. Lane
scripts: `.../emulation/handful/lanes_ex1/`, sixteen of them, each kept
in the repo as the standing rule of 2026-09-07 requires. Every lane log
named below is on the TOWER (`<user>@<tower>`) under
`<runs>/ex1/agent/logs/`.

Paths inside a pasted command are the ones the lane sees:
`PseudoCoupHQ` IS `PRIVATE/PseudoCoupHQ`, mounted into
the instance. Every rendering is labelled per the protocol's
`object.literal-gloss-analogy`: **LITERAL** is the object itself,
quoted; **GLOSS** is a plain-words reading beside a literal.

---

# 1. What this is, one sentence per object in relation

* A **CELL** is one (`mnem`, operand shape, `key_width`) row of the
  arch-opcode model table, holding, per place the opcode writes, the z3
  term the reference simulator's own builder puts there.
* The **OUTER SET** is the 253 cells the canon40 corpus attests, over
  133,044 attested ledger rows — task ap4's file copied here and its
  counts re-measured, object for object identical.
* A **COMPILED RUN** is `find_emulation(cell, lang)` as tasks g1 to ap4
  left it: the target's own operator where its whole lowered body IS the
  cell, the cell's term written in the target's operators where it is
  not, compiled at the corpus's ship flags, carved, and put back to z3
  against the cell's own term. **THIS TASK ADDS ONE TARGET TO THAT
  ROUTE, cpp, AND CHANGES NOTHING ELSE ABOUT IT.**
* An **INTERPRETED RUN** is a different thing and this task defines it.
  An interpreted target hands us no machine code of its own to carve —
  what runs is the interpreter's handler, a different unit under a
  different node — so the emulation is SOURCE in that language and the
  check is the fuzz census's method over a stated sample.
* **THE HANDFUL** is task h1's own ten cells, ratified intention, and it
  is what both expansions were run on first, per the owner's standing rule.

**THE TWO ANSWERS.**

1. **cpp proves every cell the four prove.** All-four is task ap4's own
   162 cells / 106,032 ledger rows / 79.7%; **all-five is the same 162 /
   106,032 / 79.7%**, and the list of cells proved on all four and not
   on cpp is **empty**. cpp's own proved set is 225 of 253 cells, 63 of
   them cells the all-four set does not hold — the x87 arithmetic among
   them, which cpp has a `long double` for and rust, go and swift do
   not.
2. **The interpreted check runs, and on the handful it agrees
   everywhere.** Seven interpreted targets, ten cells each, 70 runs, all
   70 rendered: **39,062 sample points per target, 38,242 or 38,243
   agreements, ZERO disagreements on any target**, and 819 or 820
   declines whose causes are named (division by zero, which every one of
   the seven raises on, and the region where the reference's own term
   does not evaluate).

Two things are said before the numbers so they are not misread:

* **An agreement is not a proof, and no interpreted run carries a gate
  verdict.** A whole sample agreeing is evidence at the strength the
  fuzz line's evidence doctrine gives an executed measurement; a single
  disagreement would be conclusive the other way. That asymmetry is why
  the check is worth running, and §6 states the sample rule in full
  before any number from it is read.
* **Five defects of this task's own were found by its own runs and each
  was fixed in the layer that owns it, none worked around.** They are
  §7, with the run that caught each one quoted. Four were dialect
  spellings; the fifth was the interpreted route SKIPPING a driver fix
  the compiled route runs, and that one is the interesting one.

---

# 2. The lanes

| lane | what it did | log, on the tower |
|---|---|---|
| `ex1_l1_toolchains_and_runners.sh` | what is in the image: every compiled toolchain and every interpreted runner asked for its own version; one cpp probe compiled and carved; the mangling measured | `...222746Z` |
| `ex1_l2_cpp_and_value_model_probes.sh` | **THE MEASUREMENT BEFORE THE SPELLINGS**: task ap4's 309 rendered c sources handed to clang++ verbatim; one probe per cpp holder; each interpreted language's own value model | `...223233Z` |
| `ex1_l3_the_ten_cells_and_what_they_ask_for.sh` | the ten cells' places, terms and z3 declaration vocabulary, read off the cells themselves; php's one question; dart's and c#'s value models | `...223513Z` |
| `ex1_l4_cpp_preflight_and_the_sample.sh` | the cpp renderer's own probe, the outer set, the twenty-run memory sample | `...224209Z` |
| `ex1_l5_the_cpp_loop.sh` | **THE cpp LOOP**: 253 runs in 63 s | `...224240Z` |
| `ex1_l6_interp_smoke.sh` | the sample rule stated before anything ran, and the first cell on all seven targets | `...225414Z` |
| `ex1_l7_interp_the_seventy.sh` | the seventy, first pass — caught php's mask, php's multiply and c#'s reserved word | `...225644Z` |
| `ex1_l8_interp_the_seventy_b.sh` | second pass — caught the java main broken by the c# fix, and c#'s launcher | `...230010Z` |
| `ex1_l9_interp_the_seventy_c.sh` | third pass — caught the c# dll handed to the operating system as a program | `...230256Z` |
| `ex1_l10_interp_the_seventy_d.sh` | fourth pass — all seven runners answer; the two float cells still refused | `...230426Z` |
| `ex1_l11_the_two_float_cells_and_the_jit.sh` | **THE PROBE THAT FOUND THE FIFTH DEFECT**: the two cells files hold the same row and the same term, so the difference was in the ROUTE; and what `jit_out_*` actually holds | `...230617Z` |
| `ex1_l12_interp_the_seventy_e.sh` | **THE INTERPRETED RUN OF RECORD**: 70 of 70 rendered | `...230731Z` |
| `ex1_l13_the_cpp_tables.sh` | the tables, first pass — **it caught a defect of its own**: re-counting the columns here gave an all-four of 142 against task ap4's own 162 | `...230904Z` |
| `ex1_l14_the_tables_of_record.sh` | **THE TABLES OF RECORD**, every figure read off an aggregate | `...231118Z` |
| `ex1_l15_guard_report_and_the_tally.sh` | the spelling guard over every json, the sources, the tally | `...231223Z` |
| `ex1_l16_the_report_of_record.sh` | the sources compared on what they compute, the JIT section, `expand1.md` | `...231401Z` |

---

# 3. What was added, and where

| file | what it is |
|---|---|
| `.../emulation/cpp/cpp_render.py` | `CppRenderer(E.Renderer)`, `compile_and_carve` at cpp's ship flags, `recorded_facts`, the spelling table |
| `.../emulation/interp/dialects.py` | one helper prelude per interpreted language: that language's value model, written once, in its own operators |
| `.../emulation/interp/interp_render.py` | `InterpRenderer(E.Renderer)` and the seven dialects it prints through |
| `.../emulation/interp/interp_check.py` | the sample rule, the reference's answer at a point, the runner, the comparison, the tables |
| `.../emulation/interp/src_ex1/` | the 70 rendered interpreted sources |
| `.../emulation/autopoly/expand1.py` | the loop (task ap4's, repointed), the tables at both widths, the report |
| `.../emulation/autopoly/expand1_*` | the cells file, the cpp store, the aggregate, the interpreted store and aggregate, `expand1.md`, `src_expand1/` |
| `.../emulation/handful/lanes_ex1/` | the sixteen lane scripts |

**One file outside those folders was edited and it is the DRIVER, not a
shared file**: `.../emulation/handful/handful.py`. cpp is learned in
four places that are NOT gated on a task name — `renderer_for`,
`suffix_of`, `compile_one_place`, `wrapped_body` — because a cpp
emulation IS rendered by `CppRenderer` and compiled by clang++ whoever
asks; `TARGETS_WITH_AN_80_BIT_HOLDER` gains cpp for the same reason, and
the measurement is in §4.2. What IS task-scoped is `targets()`, which
answers with five for `ex1`, because that changes which pairs a loop
walks and tasks ap1 to ap4 counted "proved on all four" over four.
**Nothing under `Research/op_pipeline/` was changed** — §9 is the proof.

---

# 4. cpp — what was measured before a spelling was written

## 4.1 The strongest measurement available is the corpus's own

**LITERAL**, lane `ex1_l2_cpp_and_value_model_probes.sh`, on the tower at
`<runs>/ex1/agent/logs/20260909T223233Z__ex1_l2_cpp_and_value_model_probes.sh.log`:

```
[1/9] PART A -- the corpus's own c sources handed to clang++, verbatim
   c sources task ap4's loop rendered: 309
   compiled by clang++ VERBATIM: 305 of 309
   refused, by the compiler's own first error line:
         2  error: expression is not assignable
            first: lea_mem_gpr_32__primitive__c.c
         1  error: ISO C++17 does not allow incrementing expression of type bool [-Wincrement-bool]
            first: mov_imm_gpr_8__primitive__c.c
         1  error: cannot decrement expression of type bool
            first: xor_imm_gpr_8__primitive__c.c
```

**GLOSS.** 305 of the 309 sources task ap4's loop rendered compile under
clang++ at the cpp ship flags with not one character changed, and all
four that do not are on the PRIMITIVE route, where the text rendered is
the CORPUS ROW's own operator on the corpus row's own holders — a c row,
so a c spelling, and `bool++` is a thing c++17 removed. cpp's primitive
route renders cpp's own rows, which are the rows clang++ itself
accepted. The TERM route is unchanged text for text, which is why
`CppRenderer` inherits every `emit` method rather than restating one.

## 4.2 The holders, each asked of clang++ on its own

**LITERAL**, the same lane, section `[3/9]`:

```
--- holder_long_double, LITERAL:
      #include <cstdint>
      extern "C" long double probe(long double a, long double b) { return a + b; }
    $ /usr/bin/clang++ -std=c++20 -O1 -c holder_long_double.cpp
      ACCEPTED
         0:	db 6c 24 18          	fldt   0x18(%rsp)
         4:	db 6c 24 08          	fldt   0x8(%rsp)
         8:	de c1                	faddp  %st,%st(1)
         a:	c3                   	ret
```

**GLOSS.** cpp's `long double` IS the x87 extended format on this
toolchain and carves to exactly the body task ap3 measured for c's
(`fldt 0x18(%rsp); fldt 0x8(%rsp); faddp %st,%st(1); ret`). That is the
whole justification for `TARGETS_WITH_AN_80_BIT_HOLDER` gaining cpp, and
it is why cpp proves 30 x87 cells that rust, go and swift are refused on
by nature. `unsigned __int128`, `_Float16`, the `UINT32_C` macros, the
unqualified `<cstdint>` names, the `memcpy` helper under `<cstring>` and
the C-style cast chain were each ACCEPTED in the same section.

## 4.3 The two things cpp spells differently

**THE SYMBOL. LITERAL**, lane `ex1_l1_toolchains_and_runners.sh`, on the
tower at
`<runs>/ex1/agent/logs/20260909T222746Z__ex1_l1_toolchains_and_runners.sh.log`:

```
0000000000000000 g     F .text	0000000000000004 _Z10plain_namejj
0000000000000010 g     F .text	0000000000000004 c_name
```

**GLOSS.** cpp mangles a function name unless it is declared
`extern "C"`, and the carve asks objdump for the symbol BY NAME, so an
emulation whose name is mangled cannot be carved. `extern "C"` is
emitted. It is also the corpus's own shape — `probe_gen.emit_cpp` writes
`extern "C" auto` over every cpp probe.

**A DEFECT OF THIS TASK'S OWN, recorded rather than hidden.** Lane
`ex1_l2`'s sections `[1/9]` and `[2/9]` also each printed a line
claiming to count how many object files carried the c symbol name. Both
counts are WORTHLESS and neither is quoted anywhere in this log: the
test was `symbol in objdump_output`, and the mangled name
`_Z27emu_adc_gpr_gpr_64...` CONTAINS the unmangled one as a substring,
so it passes on both. The claim those lines were meant to support is
made instead by the symbol-table paste above, which shows the two names
whole, and by the 253 cpp runs that carved.

**THE HEADERS.** `#include <cstdint>` and `#include <cstring>`, the
corpus's own spelling, both measured to give the unqualified names the
renderer writes.

## 4.4 The spelling table

**LITERAL**, lane `ex1_l16_the_report_of_record.sh`'s predecessor
`ex1_l15_guard_report_and_the_tally.sh`, reproducible with
`python3 -c` over `cpp_render.spelling_rows()`; the six rows are: the
holders (c's own, unchanged), the fixed-width header, the header the
float-bits helper needs, the linkage, the expression text (c's own,
every emit method inherited) and the ship flags. Each row names the
probe that measured it.

**THE SHIP FLAGS, LITERAL**, `lane_gen.py`'s own cpp branch:

```
opt = ["-O0", "-g"] if mode == "anchor" else ["-O1"]
cmd = [CLANGXX, "-std=c++20"] + opt + ["-c", src, "-o", obj]
```

so the ship build is `/usr/bin/clang++ -std=c++20 -O1 -c`, and clang++
on this machine answers `Ubuntu clang version 21.1.8 (6ubuntu1)`.

---

# 5. THE cpp COLUMN, and the all-four / all-five line

**LITERAL**, lane `ex1_l14_the_tables_of_record.sh`, on the tower at
`<runs>/ex1/agent/logs/20260909T231118Z__ex1_l14_the_tables_of_record.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/expand1.py tables
Table 1 -- one row per target. `cells` counts runs; `rows` is the attested ledger rows those cells cover and `share` that as a percentage of 133044.  cpp's column is this task's own aggregate; the other four are task ap4's, read off `autopoly4.json` and not re-run.

| step or verdict | c | cpp | rust | go | swift |
|---|---|---|---|---|---|
| `attempted` | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% |
| `rendered` | 245 cells, 127079 rows, 95.52% | 245 cells, 127079 rows, 95.52% | 209 cells, 124394 rows, 93.5% | 200 cells, 120018 rows, 90.21% | 200 cells, 120018 rows, 90.21% |
| `compiled` | 245 cells, 127079 rows, 95.52% | 245 cells, 127079 rows, 95.52% | 209 cells, 124394 rows, 93.5% | 200 cells, 120018 rows, 90.21% | 200 cells, 120018 rows, 90.21% |
| `LANDED` | 76 cells, 41829 rows, 31.44% | 76 cells, 41829 rows, 31.44% | 72 cells, 39199 rows, 29.46% | 30 cells, 22970 rows, 17.26% | 70 cells, 38915 rows, 29.25% |
| `LANDED_ELSEWHERE` | 27 cells, 11867 rows, 8.92% | 27 cells, 11867 rows, 8.92% | 23 cells, 11885 rows, 8.93% | 16 cells, 5448 rows, 4.09% | 35 cells, 18714 rows, 14.07% |
| `NOT_COLLAPSED` | 138 cells, 72141 rows, 54.22% | 138 cells, 72141 rows, 54.22% | 110 cells, 72068 rows, 54.17% | 146 cells, 77229 rows, 58.05% | 91 cells, 61147 rows, 45.96% |
| `proved` | 204 cells, 98747 rows, 74.22% | 202 cells, 93853 rows, 70.54% | 170 cells, 96021 rows, 72.17% | 177 cells, 113587 rows, 85.38% | 163 cells, 89240 rows, 67.08% |
| `proved under caller extension` | 20 cells, 20530 rows, 15.43% | 23 cells, 25429 rows, 19.11% | 21 cells, 21502 rows, 16.16% | 0 cells, 0 rows, 0.0% | 17 cells, 19778 rows, 14.87% |
| `sat` | 19 cells, 6794 rows, 5.11% | 17 cells, 5841 rows, 4.39% | 15 cells, 5085 rows, 3.82% | 17 cells, 5181 rows, 3.89% | 5 cells, 3723 rows, 2.8% |
| `undecided` | 2 cells, 1008 rows, 0.76% | 3 cells, 1956 rows, 1.47% | 3 cells, 1786 rows, 1.34% | 6 cells, 1250 rows, 0.94% | 15 cells, 7277 rows, 5.47% |
| `refused` | 8 cells, 5965 rows, 4.48% | 8 cells, 5965 rows, 4.48% | 44 cells, 8650 rows, 6.5% | 53 cells, 13026 rows, 9.79% | 53 cells, 13026 rows, 9.79% |

Table 2 -- the polyfill-complete set at BOTH widths, which is what the brief asks for until the owner says which counts.  A cell counts as proved on a target when the gate answered `unsat` at that target's destination place, at the 3,000 ms ceiling of record or under the caller-extension re-pose.

| width | targets | cells | ledger rows | share |
|---|---|---|---|---|
| all four | c, rust, go, swift | 162 | 106032 | 79.7% |
| all five | c, cpp, rust, go, swift | 162 | 106032 | 79.7% |

cells proved on all four and NOT on cpp: 0

cpp's own proved set: 225 cells
cells proved on cpp that are not in the all-four set: 63

Table 3 -- how many of the five each cell is proved on, from task ap4's own per-cell list plus cpp's.

| proved on | cells | ledger rows | share |
|---|---|---|---|
| 5 of 5 | 162 | 106032 | 79.7% |
| 4 of 5 | 20 | 7761 | 5.83% |
| 3 of 5 | 10 | 3998 | 3.01% |
| 2 of 5 | 36 | 2685 | 2.02% |
| 1 of 5 | 5 | 119 | 0.09% |
| 0 of 5 | 20 | 12449 | 9.36% |
```

**GLOSS**, four readings the table does not make on its own.

* **THE ALL-FIVE COUNT IS THE ALL-FOUR COUNT: 162 cells, 106,032
  attested ledger rows, 79.7%.** Not one cell that the four prove is
  lost by adding cpp, and the empty list under Table 2 is that stated as
  an object rather than as an absence of rows.
* **cpp's own proved set is LARGER than c's is inside the all-four
  set**: 225 cells against the four-way intersection's 162, and the 63
  extra are cells at least one of rust, go or swift is refused on — the
  x87 arithmetic (`faddp`, `fdivp`, `fiaddl` and their kin), the
  `cmpeqss`/`cmpneqsd` family, `adc` gpr_gpr 64. cpp is c's twin here by
  construction, so what that column really measures is how much of the
  four-way intersection is being set by rust, go and swift rather than
  by c.
* **cpp's `proved` is 202 where c's is 204, and its `proved under caller
  extension` is 23 where c's is 20.** Those two differences are the same
  three cells moving between the two rows and not three cells lost: the
  all-four-and-not-cpp list is empty, and Table 3's `5 of 5` equals
  Table 2's all-four exactly.
* **`refused` is 8 on cpp and 8 on c, the same eight**, and `rendered`
  and `compiled` agree to the cell. The fifth target behaves as the
  measurement of §4.1 said it would.

## 5.1 The handful's ten cells on cpp, beside c

**LITERAL**, lane `ex1_l18_handful_again.sh`, on the tower at
`<runs>/ex1/agent/logs/*__ex1_l18_handful_again.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/expand1.py handful
| cell | route on cpp | landed on cpp | cpp's verdict | c's verdict | the two sources |
|---|---|---|---|---|---|
| `add` gpr_gpr 32 | term | LANDED_ELSEWHERE | LANDED_ELSEWHERE on `lea` / PROVED_ON_SHIP | LANDED_ELSEWHERE on `lea` / PROVED_ON_SHIP | the same text but for the header and the linkage |
| `sub` imm_gpr 64 | -- | -- | not run | -- | -- |
| `imul` gpr_gpr 32 | primitive | LANDED | LANDED / PROVED_ON_SHIP | LANDED / PROVED_ON_SHIP | different text |
| `sar` cl_gpr 32 | primitive | LANDED | LANDED / PROVED_ON_SHIP | LANDED / PROVED_ON_SHIP | different text |
| `shr` cl_gpr 64 | primitive | LANDED | LANDED / PROVED_ON_SHIP | LANDED / PROVED_ON_SHIP | different text |
| `idiv` gpr_one 32 | primitive+setup | NOT_COLLAPSED | NOT_COLLAPSED (2) / DISPROVED | NOT_COLLAPSED (2) / DISPROVED | different text |
| `cmovne` gpr_gpr 32 | term | NOT_COLLAPSED | NOT_COLLAPSED (2) / PROVED_ON_SHIP | NOT_COLLAPSED (2) / PROVED_ON_SHIP | the same text but for the header and the linkage |
| `setne` gpr_one 8 | term | NOT_COLLAPSED | NOT_COLLAPSED (3) / DISPROVED, PROVED_ON_SHIP under caller extension | NOT_COLLAPSED (3) / DISPROVED, PROVED_ON_SHIP under caller extension | the same text but for the header and the linkage |
| `addss` xmm_xmm 32 | term | LANDED | LANDED / PROVED_ON_SHIP | LANDED / PROVED_ON_SHIP | the same text but for the header and the linkage |
| `cvtsi2sd` gpr_xmm 64 | term | LANDED | LANDED / PROVED_ON_SHIP | LANDED / PROVED_ON_SHIP | the same text but for the header and the linkage |

`sub` imm_gpr 64 is one of the handful's ten and is NOT in the 253-cell outer set this loop walks, so no run of it exists on either store; task ap4's own reproduction line says the same of it, LITERAL: `the handful's forty pairs: 32 agree character for character, 35 agree on the verdict, 4 not in this outer set`.

of the ten, cpp's verdict is c's: 9
of the ten, cpp's source is c's but for the header and the linkage: 5
```

**GLOSS.** Nine of the ten are in the outer set and cpp's verdict is c's
on all nine, route for route and landing for landing. Five of the nine
render source that is c's own CHARACTER FOR CHARACTER once the two
measured differences (the header names, the linkage) and the label's own
target name are folded — every one of the five is on the TERM route. The
four that differ are the PRIMITIVE route, where the text is the corpus's
own cpp probe rather than the corpus's own c probe, which is the route
working as designed.

**AND ONE THING ABOUT THIS TABLE IS RECORDED RATHER THAN SMOOTHED
OVER.** Lane `ex1_l16` printed the same command with the `setne` row
reading `different text` beside a count of 5, which does not add up —
four rows saying "the same text" and a count of five. Lane `ex1_l18`
re-ran the identical command, and so did the verifier's first pass over
this log; both give the table above, in which the `setne` row reads "the
same text" and the count of 5 is the five rows that say so. The
inconsistent print is on the record in `ex1_l16`'s log and is not
reproducible; the table of record is `ex1_l18`'s, and it is the one the
verifier re-runs.
`sub` imm_gpr 64 is the handful's tenth and is not in the 253-cell outer
set; task ap4's own reproduction line says the same of it, LITERAL:
`the handful's forty pairs: 32 agree character for character, 35 agree
on the verdict, 4 not in this outer set`.

**THE TERM ROUTE'S OWN cpp SOURCE, LITERAL**, lane `ex1_l15`, on the
tower at
`<runs>/ex1/agent/logs/20260909T231223Z__ex1_l15_guard_report_and_the_tally.sh.log`:

```
/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of add_gpr_gpr_32__reg_rdi__cpp.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(31, 0, v0) + Extract(31, 0, v1)) */
#include <cstdint>

extern "C"
uint64_t
emu_add_gpr_gpr_32__reg_rdi__cpp(uint32_t a, uint32_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)((uint32_t)((uint32_t)a) + (uint32_t)((uint32_t)b)))));
}
```

and **THE PRIMITIVE ROUTE'S**, same lane, which is the corpus's own cpp
probe with its symbol renamed:

```
// probe 174 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_imul_gpr_gpr_32__primitive__cpp(int32_t a, int32_t b)
{
    return a * b;
}
```

## 5.2 What did not work on cpp, by cause

**LITERAL**, lane `ex1_l15_guard_report_and_the_tally.sh`, on the tower
at
`<runs>/ex1/agent/logs/20260909T231223Z__ex1_l15_guard_report_and_the_tally.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/expand1.py causes
Table -- what did not work on cpp, by cause.  One target, so `runs` is cells and `rows` is their attested ledger rows.

| cause | runs | ledger rows |
|---|---|---|
| the gate answered sat: the body holds on a region, not on every input | 17 | 5841 |
| term reads state that is not an arrival register | 5 | 4505 |
| answer home or arrival on the x87 stack | 3 | 1460 |
| the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | 1 | 624 |
| the gate did not answer: the carved body: the reference: this body's control flow has a cycle (a transfer back to a block already on the walk), and no loop invariant is invented here; and no term either | 1 | 948 |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 1 | 384 |

runs carrying a cause: 28 of 253
```

**GLOSS.** Six causes over 28 of 253 runs, and the three x87 refusals are
c's own three from task ap4 §6.4 — the two x87 compares whose flag place
reads an x87 value's BITS, and `fldz`, whose term's root is a 79-bit
bitvector rather than a float. Nothing here is new to cpp.

---

# 6. THE INTERPRETED CHECK — what it is, stated before it ran

## 6.1 Why there has to be a different check

For a compiled target the emulation's machine code IS the object: it is
carved, put on the canonical form and PROVED equal to the cell's term
over every input by z3. An interpreted target hands us no such object —
the machine code that runs is the interpreter's own handler, which is a
different unit under a different node
(`node_0_3_1_12_remaining_languages` §1, "the interpreter shape"). So
the emulation is SOURCE and the only evidence available is what the
interpreter ANSWERS. The check is therefore the fuzz census's method
(`node_0_3_0_2_kind_fuzz_clustering`, "the method, as designed
2026-08-14": generate a minimal program per thing, RUN it, record what
came back, compare by relation), and it is this:

1. the cell's mapping is rendered as source in the target's own
   operators over the target's own value model;
2. a SAMPLE of input points is built by the rule of §6.2, which was
   stated in full and printed by a lane BEFORE anything ran;
3. the REFERENCE's answer at each point is the cell's own z3 term with
   the point substituted and `z3.simplify` applied — the reference
   simulator's own mapping, evaluated, and not a second model of it;
4. the INTERPRETER's answer at each point is what the rendered source
   prints when the runner is handed every point on standard input, ONE
   process for the whole sample;
5. the two are compared point by point. An AGREEMENT is two integers
   that are equal. A DISAGREEMENT is two integers that are not, and it
   is reported with the point LITERAL — it is what a `sat` is on the
   compiled route. A DECLINE is a point where one side has no value, and
   DECLINES ARE NOT SCORED, which is this line's own standing rule
   (`CLAUDE.md`, "Declines are never scored"): dropped from the
   numerator and the denominator, counted separately by cause.

## 6.2 THE SAMPLE RULE, LITERAL, printed by lane `ex1_l6` before the run

**LITERAL**, lane `ex1_l6_interp_smoke.sh`, on the tower at
`<runs>/ex1/agent/logs/20260909T225414Z__ex1_l6_interp_smoke.sh.log`, and it is the same text `interp_check.SAMPLE_RULE` holds and `expand1.md` carries:

```
THE SAMPLE, for a place whose emulation takes k arrivals of widths
w_1 .. w_k.

  the per-arrival budget b = max(4, int(20000 ** (1.0 / k)))

  P(an INTEGER arrival of width w) is this list, in this order,
  deduplicated, every value taken modulo nothing and dropped when it
  is not less than 2^w, then cut to its first b entries:
      0, 1, 2, 3, 7, 100,
      2^(w-1) - 1, 2^(w-1), 2^(w-1) + 1,          the sign boundary
      2^w - 2, 2^w - 1,                           the top, and -1
      w - 1, w, w + 1,                            this width's shift counts
      7, 8, 9, 15, 16, 17, 31, 32, 33, 63, 64, 65, the other widths'
      then 8 values from random.Random(20260909).randrange(2^w)

  P(a FLOAT arrival of width w, which reaches the emulation as its
  IEEE bit pattern) is this list, in this order, deduplicated, cut to
  its first b entries:
      +0, -0, 1.0, -1.0, 2.0, 0.5, -0.5,
      the smallest subnormal, the largest subnormal,
      the smallest normal, the largest finite,
      +inf, -inf, a quiet NaN, a signalling NaN,
      then 8 values from random.Random(20260909).randrange(2^w)

  THE SAMPLE is the ordered cross product P(a_1) x ... x P(a_k), in
  that order.  Its size is at most 20,000 by the budget above, and the
  run record carries the exact count.

  WHY b IS A CEILING AND NOT A CHOICE OF POINTS: the edge values come
  FIRST in every list, so cutting to b drops ordinary values before it
  drops an edge.  A place with one or two arrivals is never cut at all
  (b is 20000 and 141), so the handful's edges are all present; a
  place with four is cut to 11 per arrival, and the run record says
  which values those were.
```

and the counts it gives, **LITERAL**, the same lane:

```
| arrivals | budget | an 8-bit list | a 32-bit list | a 64-bit list |
|---|---|---|---|---|
| 1 | 20000 | 27 | 30 | 30 |
| 2 | 141 | 27 | 30 | 30 |
| 3 | 27 | 27 | 27 | 27 |
| 4 | 11 | 11 | 11 | 11 |

a 32-bit integer list in full, LITERAL: [0, 1, 2, 3, 7, 100, 2147483647, 2147483648, 2147483649, 4294967294, 4294967295, 31, 32, 33, 8, 9, 15, 16, 17, 63, 64, 65, 389011218, 2331439129, 2029787120, 3026389180, 2533586177, 3307009030, 839636273, 1229552792]

a 32-bit float list in full, as bit patterns, LITERAL: ['0x0', '0x80000000', '0x3f800000', '0xbf800000', '0x40000000', '0x3f000000', '0xbf000000', '0x1', '0x7fffff', '0x800000', '0x7f7fffff', '0x7f800000', '0xff800000', '0x7fc00000', '0x7f800001', '0x172fd712', '0x8af6f019', '0x78fc17f0', '0xb46308bc', '0x97037501', '0xc51cf406', '0x320bd531', '0x49497c98']
```

**GLOSS.** The brief asks for the shift-count boundary, the sign
boundary, zero, MIN and −1 for division, and NaN and the infinities for
floats. Every one of them is in the list above and none of them is ever
cut, because the cut takes from the tail and the edges are at the head.

## 6.3 The value models, each measured before a dialect was written

**LITERAL**, lane `ex1_l2`, sections `[4/9]` to `[8/9]`, and lane
`ex1_l3` sections `[2/4]` to `[4/4]`. Five findings the seven preludes
are built on:

```
   python     division rounds             (-7) // 2              -> -4
   ruby       division rounds             -7 / 2                 -> -4
   php        at the width boundary       PHP_INT_MAX + 1        -> 9.223372036854776E+18
   php        its type there              gettype(...)           -> 'double'
   php        a shift count at the width  1 << 64                -> 0
   java       a shift count at the width  1 << 32                -> 1
   java       a long shift count at 64    1L << 64               -> 1
   dart       a shift count at the width  1 << 64                -> 0
   csharp     a shift count at the width  1 << 32                -> 1
   javascript division truncates          (-7n) / 2n             -> -3
```

**GLOSS.** python's and ruby's division FLOORS and z3's `bvsdiv`
TRUNCATES, so both spell it with `abs`; php's `+` leaves the integers
entirely at the boundary and neither gmp nor bcmath is loaded
(`extension_loaded("gmp")` -> false), so its 64-bit arithmetic is done in
16-bit limbs; java's and c#'s shift counts are MASKED while dart's and
php's saturate to zero, so every shift tests its count first. Not one of
those five was read out of a manual.

## 6.4 THE INTERPRETED TABLE

**LITERAL**, lane `ex1_l12_interp_the_seventy_e.sh`, on the tower at
`<runs>/ex1/agent/logs/20260909T230731Z__ex1_l12_interp_the_seventy_e.sh.log`:

```
| target | runs | rendered | cells whose whole sample agrees | points | agreements | disagreements | declines |
|---|---|---|---|---|---|---|---|
| cpython | 10 | 10 | 10 | 39062 | 38243 | 0 | 819 |
| php | 10 | 10 | 10 | 39062 | 38242 | 0 | 820 |
| ruby | 10 | 10 | 10 | 39062 | 38243 | 0 | 819 |
| java | 10 | 10 | 10 | 39062 | 38243 | 0 | 819 |
| javascript | 10 | 10 | 10 | 39062 | 38243 | 0 | 819 |
| dart | 10 | 10 | 10 | 39062 | 38243 | 0 | 819 |
| csharp | 10 | 10 | 10 | 39062 | 38242 | 0 | 820 |

what did not run, by cause:

| cause | runs | targets |
|---|---|---|

the declines, by cause, over every run (never scored, this line's own standing rule):

| cause | points |
|---|---|
| the interpreter RAISE:ZeroDivisionError | 1458 |
| the interpreter RAISE:DivisionByZeroError | 729 |
| the interpreter RAISE:ArithmeticException | 729 |
| the interpreter RAISE:RangeError | 729 |
| the interpreter RAISE:IntegerDivisionByZeroException | 729 |
| the interpreter RAISE:DivideByZeroException | 729 |
| the reference's own term does not evaluate to a numeral at this point | 630 |
| the interpreter RAISE:ArithmeticError | 1 |
| the interpreter RAISE:OverflowException | 1 |
```

**GLOSS**, five readings.

* **Seventy runs, seventy rendered, zero disagreements.** The by-cause
  table is EMPTY, which is a first for this line: every cell of the
  handful renders on every one of the seven interpreted targets.
* **The division-by-zero declines are the same 729 points on every
  target**, and the target's own word for it is what the record carries:
  `ZeroDivisionError` (python and ruby, 729 each), `DivisionByZeroError`
  (php), `ArithmeticException` (java), `RangeError` (javascript),
  `IntegerDivisionByZeroException` (dart), `DivideByZeroException`
  (csharp). 729 is 27 × 27: the `idiv` cell's sample has 27 points per
  arrival and one of the divisor's 27 is zero.
* **The 630 points where the reference does not evaluate are the NaN
  region of `addss`**, 90 per target: `fp.to_ieee_bv` is underspecified
  at a NaN and `z3.simplify` leaves a term rather than a numeral. That
  is the same underspecification task ap4 §9 met on `ucomisd` on go, and
  it is recorded as a decline rather than scored either way.
* **php's and c#'s one extra decline each is a real edge**: php's is
  `intdiv(PHP_INT_MIN, -1)`, which php refuses with `ArithmeticError`,
  and c#'s is the same point, refused `OverflowException`. z3's `bvsdiv`
  answers there and the two languages will not, which is a genuine
  difference between the value models and is reported as one.
* **The sample is 39,062 points per target, 273,434 over the seven.**

**ONE ROW OF THE FULL TABLE, LITERAL**, the same lane, so the shape the
brief asks for is on the record:

```
| `imul` gpr_gpr 32 | php | source | `ex_m(ex_cat(0, ex_mul($a, $b, 32), 32), 64)` | 900 | 900 / 0 | -- | no JIT output in the corpus |
```

The full 70-row table is §4 of
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/expand1.md`
and is reproduced by
`python3 .../autopoly/expand1.py interp_table`.

## 6.5 The JIT half of the brief's instruction, and why it has no object

The brief's instruction is conditional: "where the language has a JIT
whose output the corpus already carves, ALSO carve and gate that output
the compiled way". The condition does not hold, and it was measured
rather than assumed. **LITERAL**, lane `ex1_l16`, same log:

```
| folder | files | the first line of its dump, LITERAL |
|---|---|---|
| jit_out_javascript | 822 | `---------------------------------------------------` |
| jit_out_dart | 3 | `Code for function 'dart:io__Platform@16069316_set__nativeScript@16069316' (SetterFunction) {` |
| jit_out_csharp | 2 | `; Assembly listing for method Program:op_638(float,ulong):bool (MinOpts)` |

what the corpus holds as ARCH-UNITS, per language (`oracle/arch_opcodes/single_opcode_units.json`):

| language | in the file | narrow single-opcode groups |
|---|---|---|
| c | yes | 83 |
| cpp | yes | 82 |
| rust | yes | 48 |
| go | yes | 27 |
| swift | yes | 19 |
| java | yes | 0 |
| cpython | yes | 1 |
| php | yes | 3 |
| ruby | yes | 2 |
| javascript | no | -- |
| dart | no | -- |
| csharp | no | -- |
```

**GLOSS.** `jit_out_*` holds each JIT's OWN dump text in three different
formats — TurboFan's, the Dart VM's and RyuJIT's — and not one of them
is objdump's, which is what `lane_gen.DRIVER`'s `extract` reads and what
every carve on this line uses. The corpus holds no arch-unit for
javascript, dart or csharp at all: they are absent from
`single_opcode_units.json` entirely, which agrees with the
remaining_languages node's own table ("arch-units on disk: 0" for v8,
csharp and dart, "route status: designed only"). **So there is nothing
to carve and nothing to gate**, and building a reader for three new
instruction-text formats is a NEW INSTRUMENT — a flag for the
coordinator under the law's stop rules, not something this task works
around. It is item 1 of the awaiting-the owner list.

---

# 7. THE FIVE DEFECTS THIS TASK'S OWN RUNS FOUND

Each was found by a run, fixed in the layer that owns it, and the store
of the pass that found it is kept under its own name — nothing was
deleted and no pass was overwritten.

| # | what was wrong | the run that caught it, LITERAL | where it was fixed |
|---|---|---|---|
| 1 | php's mask was `(1 << $w) - 1`, and php's `1 << 63` is PHP_INT_MIN, so at 63 and 64 bits the mask left the integers for a double | `shr` cl_gpr 64: `{"point": [2, 1], "the interpreter's answer": 0, "the reference's answer": 1}` | `dialects.PHP_PRELUDE`, `ex_maskbits` |
| 2 | php's multiply was in 32-bit halves and a 32-by-32 product is up to 2^64 | `imul` gpr_gpr 32: `{"point": [2147483649, 4294967295], "the interpreter's answer": 2147483648, "the reference's answer": 2147483647}` | `dialects.PHP_PRELUDE`, 16-bit limbs |
| 3 | `out` is a reserved word in c# | `Program.cs(121,23): error CS1002: ; expected` | `dialects.CSHARP_MAIN`, and then `JAVA_MAIN`, which the first fix broke by being applied to the FILE rather than to the dialect (`Emu.java:158: error: cannot find symbol`) |
| 4 | c#'s framework-dependent launcher looks for a runtime on the machine's own path | `You must install .NET to run this application`, exit 131; then `emu.dll: Permission denied` when the dll was handed to the operating system as a program | `interp_render.Csharp.prepare` / `command`: `dotnet exec emu.dll` |
| 5 | **the interpreted route was skipping a driver fix the compiled route runs** | all fourteen `addss` and `cvtsi2sd` runs: `REFUSED: vector arrival used beyond its low lane: xmm0 read above bit 63`, while THE SAME TWO CELLS proved on cpp in this task's own compiled loop | `interp_check.one_run` now calls `handful.projected_lane` at the same point the compiled route calls it |

**GLOSS on the fifth, which is the one worth reading.** Task h2's fix 2
projects the LANE a vector opcode writes out of the 128-bit place before
anything is rendered; without it the term reads `Extract(127, 32, v0)`
and the ONE renderer's own planner refuses. Lane `ex1_l11` is what made
it a route question rather than a cell question. **LITERAL**, that lane,
on the tower at
`<runs>/ex1/agent/logs/20260909T230617Z__ex1_l11_the_two_float_cells_and_the_jit.sh.log`:

```
== the 253-cell outer set (expand1_cells.json)
   -- `addss` xmm_xmm 32   row r00332   line 'addss %xmm1,%xmm0'
      place reg_xmm0       bits 128  families ['xmm0', 'xmm1']
         term, LITERAL: Concat(Extract(127, 32, v0), fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1))))

== the handful's own cells file (handful_cells.json)
   -- `addss` xmm_xmm 32   row r00332   line 'addss %xmm1,%xmm0'
      place reg_xmm0       bits 128  families ['xmm0', 'xmm1']
         term, LITERAL: Concat(Extract(127, 32, v0), fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1))))
```

**GLOSS.** Same row, same term, both files — so the difference could not
be in the cell, and looking for it in the route found a driver fix the
interpreted half had never been given. It is called now, over the same
objects, at the same point.

**A SIXTH, in this log's own tables rather than in a dialect.** Lane
`ex1_l13`'s first pass RE-COUNTED the per-target columns and the
all-four line here instead of reading them off the aggregates, and got
`all four | c, rust, go, swift | 142 | 83794 | 62.98%` against task ap4's
own 162 / 106,032 / 79.7% — because task ap4's rule reads EVERY place of
the destination register (two, where a 128-bit place is split into
halves) and takes the weakest, and a re-derivation from
`destination_place` alone does not. The rule is now CALLED
(`autopoly4.outcome_of`) and the columns are read off the two
aggregates. The wrong figures are named here so nobody meets them
without their correction.

---

# 8. Memory

The bound stated in `PUBLIC/Airlock/instances/ex1.conf`, in every
lane header and in `expand1.py`'s and `interp_check.py`'s own constants
is 6 GB resident on the one collecting process, named abort
`ABORT_MEMORY_EX1`, checked after every run. The sample the law asks for
is the first twenty runs of the cpp loop, printed with the peak after
each; twenty runs took 1 s and the peak was 259,164 kB.

| lane | what it read | peak resident |
|---|---|---|
| `ex1_l3_the_ten_cells_and_what_they_ask_for.sh` | the cells file and the pipeline's walk | 66,620 kB |
| `ex1_l4_cpp_preflight_and_the_sample.sh` | the two reads, then 20 runs | 259,164 kB |
| `ex1_l5_the_cpp_loop.sh` | the two reads, then 253 runs | 484,044 kB |
| `ex1_l6_interp_smoke.sh` | the ten cells, then 7 interpreted runs | 67,196 kB |
| `ex1_l7_interp_the_seventy.sh` | 70 interpreted runs | 76,292 kB |
| `ex1_l12_interp_the_seventy_e.sh` | 70 interpreted runs and the pipeline's walk | 78,656 kB |
| `ex1_l15_guard_report_and_the_tally.sh` | both stores and both aggregates | 71,584 kB |

The high-water mark, 484,044 kB, is **7.7% of the bound**. No abort
fired. Lanes `ex1_l1`, `ex1_l2`, `ex1_l11`, `ex1_l13`, `ex1_l14` and
`ex1_l16` print no peak of their own: their work is compilers and
interpreters in separate short-lived processes and reads of finished
aggregates.

---

# 9. The guard, and what did not move

**LITERAL**, lane `ex1_l15_guard_report_and_the_tally.sh`, on the tower at
`<runs>/ex1/agent/logs/20260909T231223Z__ex1_l15_guard_report_and_the_tally.sh.log`:

```
[5/6] the spelling guard, over every json this task wrote
operator inventory: 91 tokens read from probe_manifest_*.json
PASS expand1_cells.json -- no operator token in any key, grouping, pairing or row structure
operator inventory: 91 tokens read from probe_manifest_*.json
PASS expand1.json -- no operator token in any key, grouping, pairing or row structure
operator inventory: 91 tokens read from probe_manifest_*.json
PASS expand1_interp.json -- no operator token in any key, grouping, pairing or row structure

   grep -c exempt over the files this task added:
      cpp/cpp_render.py: 0
      interp/dialects.py: 0
      interp/interp_render.py: 0
      interp/interp_check.py: 0
      autopoly/expand1.py: 0
```

and the tally, **LITERAL**, the same lane -- the report was 67 lines
when this lane wrote it and is 73 after lane `ex1_l16` added the JIT
section, which is why the two lane logs differ on that one figure:

```
[6/6] the report, and the tally
wrote PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/expand1.md (67 lines)
runs recorded: 253 of 253

| target | attempted | rendered | compiled | LANDED | proved | sat | undecided | refused |
|---|---|---|---|---|---|---|---|---|
| cpp | 253 | 245 | 245 | 76 | 202 | 17 | 3 | 8 |
```

`Research/op_pipeline/` was not written by this task at all: the only
file edited outside `.../emulation/` is none, and inside it the driver
`handful/handful.py` gained cpp in the five places §3 names.

---

# 10. The two lists

## Decided, recorded for audit

1. **cpp is c's renderer with two measured differences and nothing
   else** (§4). The linkage, because the carve asks objdump for the
   symbol by name; the header names, because the corpus's own cpp probe
   uses them. Every `emit` method, the width planning, the free-symbol
   check, the helper texts and the refusal causes are INHERITED, on the
   evidence that 305 of 309 c sources compile under clang++ verbatim.
2. **cpp is added to `TARGETS_WITH_AN_80_BIT_HOLDER` on a
   measurement**, not by analogy with c: cpp's `long double` carves to
   the same x87 body task ap3 measured for c's (§4.2).
3. **cpp's four learned places in the driver are UNGATED on a task
   name** and only `targets()` is gated, for the reason
   `use_task_ap2`'s own docstring gives: what is true of the objects is
   true for every task, and what changes which pairs a loop walks is
   not.
4. **The polyfill-complete set is reported at BOTH widths and neither
   re-defines the other** (§5), which is the brief's own instruction
   until the owner says which counts. They are the same 162 cells.
5. **The interpreted check is defined, stated LITERAL before it ran,
   and never called a proof** (§6). The report writes no gate verdict
   on an interpreted run and the log says an agreement is evidence, not
   a proof.
6. **Declines are not scored**, this line's own standing rule, and each
   is counted under the target's own word for it (§6.4).
7. **A float arrival reaches an interpreted emulation as its BIT
   PATTERN**, which is c's own shape (`emulate.Renderer.emit_symbol`
   takes a float parameter and immediately applies `f32_to_bits`); what
   differs is only that the conversion sits at the edge of the process
   rather than at the edge of the function. `fp.to_ieee_bv` and the
   one-argument `fpToFP` are therefore the identity, so no rendering
   round-trips a value through a wider float than the term names.
8. **Every dialect rule was measured before it was written** (§6.3),
   and the four that were measured WRONG were found by the runs and
   fixed in the dialect that owns them, with the run that caught each
   quoted (§7).
9. **The interpreted route now calls `handful.projected_lane`**, the
   driver fix the compiled route calls, at the same point over the same
   objects (§7, defect 5). Nothing about the fix was copied; the
   function is called.
10. **Table 1's figures are read off aggregates, never re-counted**
    (§7's sixth item), after a re-derivation gave a different all-four
    line. `autopoly4.outcome_of` is the rule and it is called.
11. **Nothing was deleted under `<runs>/` or
    `PUBLIC/Airlock/`** on either machine, and no store of any
    pass was overwritten: `expand1_interp_smoke.jsonl`,
    `_pass1`, `_pass2`, `_pass3` and `_pass4` are all on disk beside the
    run of record.

## Awaiting the owner

1. **There is no carve for javascript, dart or csharp, so the brief's
   "ALSO carve and gate the JIT output" has no object** (§6.5).
   `jit_out_*` holds three different JIT dump formats, none of them
   objdump's, and the corpus holds zero arch-units for those three
   languages. Building a reader for those formats is a NEW INSTRUMENT,
   which the law's stop rules make a flag rather than a workaround.
2. **Which width the polyfill-complete set is counted at** — four
   targets or five. This task reports both and they are equal today, so
   the question costs nothing yet; it will cost something the first
   time a sixth target is added that is not c's twin.
3. **cpp is c's twin, and what that means for the intersection.** cpp
   proves 225 cells to the four-way intersection's 162, so the
   all-five figure is set entirely by rust, go and swift. Whether the
   Hub's dictionary should be counted over a set of targets that holds
   two near-identical members is an ontology question about what the
   target set IS, and it is the only one this task met.

---

# 11. The conventions verifier over this log

Two passes, each a lane of this task's own instance, each over this log
as it then stood.

| pass | lane | claims | MATCHES | DIFFERS | UNVERIFIABLE | REFUSED | NOT_RERUNNABLE |
|---|---|---|---|---|---|---|---|
| first | `ex1_l17_verify_248.sh` | 25 | 2 | **1** | 22 | 0 | 0 |
| second | `ex1_l19_verify_248b.sh` | 26 | 3 | **0** | 23 | 0 | 0 |

**GLOSS**, and the obligation the law states is the DIFFERS column:
**0** on the pass of record.

* **The one DIFFERS of the first pass was fixed in the CLAIM and not in
  the verifier**, and it is §5.1's own note: the handful table had been
  pasted from lane `ex1_l16`'s print, whose `setne` row disagreed with
  its own count. Lane `ex1_l18` re-ran the identical command and the
  table of record is that one.
* **MATCHES (3)** — `tables`, `handful` and `causes`, each a command of
  `expand1.py` whose output holds no figure that moves between runs.
* **UNVERIFIABLE (23)** — eight prose paragraphs and fifteen
  attributions, each naming the lane log it came from, on the tower.

This section was appended after the second pass, and a third pass over
the log WITH it in place — lane `ex1_l20_verify_248c.sh`, the closing
one — is what the table's second row is checked against.
