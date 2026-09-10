# log_260 — task rv3: the RISC-V lifter gains the five rows clang 21 writes, each checked against the Sail model at points, and the inheritance re-run on the image that carries the riscv64 standard libraries — the two rows that read the corrected x86 store WAIT FOR ref2

Project node: **riscv64**
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/CORE_0_3_2_3_1_riscv64.md`),
under **arch_unit_oracle**
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`).
Written 2026-09-10 by the implementer of task rv3, brief
`PRIVATE/PseudoCoupHQ/Research/briefs/task_rv3_brief.md`.

Deliverables, all under `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/`:
`riscv_reference.py` (five rows added), `sail_points.py` (the harness that
can state them), `inherit_rv3.py` (the four compile routes), `census_rv3.json`,
`level0_points_rv3.json` and `level0_points_rv3_sample.json`,
`certificates_riscv64_rv3.jsonl` and `.json`, and their `_sample` twins.
Lanes: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/lanes_rv3/`. Lane
logs are on the TOWER at
`<runs>/rv3/agent/logs/<stamp>__<lane>.log` — that is
a tower path, not a path on this laptop.

---

## 1. What was done and what came of it — the walkthrough, before any figures

Task rv2 ended with four named things keeping most of the RISC-V table out
of the transfer, and this task was given the two of them that need nothing
from anybody else: the lifter had no entry for a handful of instructions
clang 21 writes, and the image had no riscv64 standard libraries, so most
of the rendered sources could not be built at all. The brief's own order
says to do those two first, then look at whether task ref2 has closed, and
to stop if it has not. It has not, so this log carries those two and marks
the other two.

The lifter first. Rather than decide from a list which instructions to add,
I compiled every source the inheritance would attempt, on all four compiled
targets, carved each body, and counted the mnemonics the opcode table has
no entry for. That census is the evidence, and it named three; task rv2's
own loop store names two more, each with the body line it refused on. Five
in all. Each was written into the reference in its own shape, and each was
then run against the ratified Sail model's own simulator at concrete points
before anything used it — which is what task rv1 did for the base set. The
float one refused at first, and the refusal turned out to be the model being
right rather than the reference being wrong: at reset a RISC-V machine has
its floating-point unit switched off, so the model trapped, exactly as real
hardware would. Enabling it in the harness's prologue was the fix, and the
five rows then agreed with the model at every point sampled.

The image second. It has since gained a rust target with a standard
library, the riscv64 gcc cross toolchain whose glibc and libstdc++ headers
clang can be pointed at, and therefore a route for c++ as well. With those
four routes in place I re-ran task rv2's inheritance unchanged in every
other respect — the same twins, the same bank records, the same alignment,
the same gate, the same two widths — so that the only thing that moved
between the two runs is the image. Every source that rv2 could not build now
builds, every body carves, every body walks, and every one of them is proved.
Nothing was disproved and nothing was undecided.

What that comes to is this. The certificates that arrived by inheritance
went from 103 to 244, the refusals from 197 to 56, and the 56 that remain
are one target and one cause: there is no swift compiler in the image at
all. The number of RISC-V cells the inheritance reaches moved by one, from
34 to 35, and that is the honest shape of the result — the workload the
transfer removes is bounded by how much of its own table the x86 loop has
proved, not by the compilers, and the compilers are now no longer the
binding constraint at all.

The two rows that read the corrected x86 store are not in this log. Task
ref2 has not closed: its DevComms log does not exist. The brief's stop rule
names that as the test, and this log marks those rows and stops.

---

## 2. What the objects are, one sentence each, in relation

- **the LIFTER** — `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/riscv_reference.py`:
  the one table from a RISC-V mnemonic to its meaning as a z3 term, and the
  walk that turns a carved body into a term by applying it line by line.
- **a ROW of the lifter** — one mnemonic's entry in that table: which places
  it reads, which it writes, and the builder that turns its operands into a
  term.
- **the CENSUS** — every certificate source on a compiled target, built for
  riscv64 and carved, with the mnemonics the lifter has no entry for
  counted; it is the evidence that decides which rows the lifter gains, and
  it asks no gate and builds no term.
- **the SAIL CHECK (level 0)** — the ratified Sail model's own simulator run
  over a bare-metal program that executes one instruction at many concrete
  inputs, against the lifter's own term for it evaluated at the same inputs.
  It is a CHECK AT POINTS, NOT AN EQUALITY.
- **the INHERITANCE** — every certificate the bank holds about an x86 cell a
  RISC-V cell twins, its SOURCE taken unchanged, compiled for riscv64 at the
  corpus's own ship flags, carved, lifted, and gated against the same term.
- **an INHERITED CERTIFICATE** — the same banked record re-measured on
  riscv64, carrying `arch` and `inherited_from`.

---

## 3. What was read, exactly as it stood, and the stop rule tested

Every figure below is an as-of. Task ref2 is changing the x86 reference and
the bank in the same hours; these are the bytes this task read.

| file (full path) | sha256 |
|---|---|
| `PRIVATE/PseudoCoupHQ/Research/op_pipeline/reference.py` AS IT STANDS | `40df3b55455f8d7a6e35ef04b7219701b957af65ad08f4d81fd550d911525e72` |
| `PRIVATE/PseudoCoupHQ/Research/op_pipeline/condition_table.py` AS IT STANDS | `f9a102f765ea0909b831cbef0a114aa1ef9c6d2db03a91bd512b3676e8c55415` |
| `PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/level0/ref2_originals/reference.py` — **the one this task walked with** | `3893363145df57944286222c18756465757d4e69a6eea0783e0f03265b7156e0` |
| `PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/level0/ref2_originals/condition_table.py` — likewise | `be2d0ad6425bdb4c437c04565c3b421ba57551e933e1df40daaef00fe408667f` |
| `PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table_rows.json` — the OLD table | `f146dcba5893bac47bf00b2f0a97f7944fd19d86f3db22749b69b6b7599dfcd8` |
| `PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/level0/model_table_rows_ref2_c4.json` — the RE-DERIVED table, beside the old | `43433ae26c2b231f41eff3d5dfa14a4fb588a32d96391c61ad451df9ddfd221e` |
| `PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl` — the bank | `bfd80360c0afdb4e6d2d227d6ea399f9781fcd0671dc121d676c18e02c2d49b8` |
| `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/twins.json` — task rv2's | `3ebdad9e3313c8663d9ac8cf0701ffb47801ce53dcc7e31a2c10701ad1dd473e` |
| `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/inherit.py` — task rv2's, READ and CALLED, not written | `51743de858454d3bf1a7bfb493f571019c8d217552d2c04b9f9fa1d2ffdc59c4` |
| `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/riscv_reference.py` — AFTER this task's five rows | `6b9e57ec07a2daef1f546f52f5da6d5c67acc28e15926dce8fd933ee46aa6b87` |
| `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/sail_points.py` — AFTER this task's harness additions | `c55442da54f6b740361b60a115a69ddc32552971b269b4134c0ba8a8f7c7f467` |
| `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/inherit_rv3.py` — new | `4e31b9cac61f1b42cf83dc4d90851948624b1c748497dc5317c0798de6e3bd72` |

**THE BRIEF'S STOP RULE, tested item by item.** Section 3 of the brief names
three conditions and says to do the second and fourth rows and section 2
only if ALL THREE hold.

| condition | as measured, 2026-09-10 16:01 EDT | holds |
|---|---|---|
| task ref2's DevComms log exists | `ls PRIVATE/PseudoCoupHQ/DevComms \| grep -i ref2` prints nothing; the highest log is `log_259` | **NO** |
| `Research/op_pipeline/reference.py` carries the four corrections, sha256 `40df3b55…25e2` | `40df3b55455f8d7a6e35ef04b7219701b957af65ad08f4d81fd550d911525e72` | yes |
| the re-derived model table is on disk beside the old | `Research/oracle/arch_opcodes/level0/model_table_rows_ref2_c4.json`, 61,448,774 bytes, written 15:01 | yes |

The first does not hold, so **section 1 rows 2 and 4 and all of section 2
are marked `WAITS FOR ref2`** and are section 6 of this log. The look was
taken ONCE, after rows 1 and 3 were finished, as the brief directs; nothing
polled for ref2.

---

## 4. The lifter's new rows — section 1 row 1

### 4.1 The census that decided the vocabulary, rather than a list

The x86 table's own rule is that no entry is invented for an opcode no body
contains. So the vocabulary was not chosen: it was READ OFF CARVED BODIES.
Lane `rv3_l2_census.sh`, artifact
`PRIVATE/PseudoCoupHQ/Research/oracle/riscv/census_rv3.json`.

| what | count |
|---|---|
| certificates on a twinned cell in the bank | 734 |
| of those, on a compiled target (`c`, `cpp`, `rust`, `go`) | 244 |
| sources built for riscv64 and carved | **244 of 244** |
| sources the build refused | **0** |
| mnemonics in the lifter's table before | 108 |
| distinct mnemonics with no entry, over all 244 bodies | **3** |

**LITERAL**, read out of the census artifact itself (lane
`rv3_l11_more_transcripts.sh`):

```
$ python3 -c "import json; d=json.load(open('PseudoCoupHQ/Research/oracle/riscv/census_rv3.json'))['no_entry_in_the_opcode_table']; [print('%-10s lines %3d  sources %3d  targets %s' % (m, d[m]['lines'], d[m]['sources'], ','.join(d[m]['targets']))) for m in sorted(d, key=lambda k: -d[k]['lines'])]"
c.zext.w   lines  12  sources  12  targets c,cpp
add.uw     lines   8  sources   8  targets c,cpp
c.mul      lines   6  sources   6  targets c,cpp
```

Two more come from task rv2's own loop store,
`PRIVATE/PseudoCoupHQ/Research/oracle/riscv/rv_loop.jsonl`, each with
the body line the walk refused on — **LITERAL**, read out of that file:

```
$ python3 -c "import json, re; seen={}; [seen.setdefault(re.search(chr(39)+'([a-z0-9.]+)'+chr(39), (json.loads(l).get('verdict') or {}).get('reason') or '').group(1), ((json.loads(l).get('verdict') or {}).get('reason') or '')[:96]) for l in open('PseudoCoupHQ/Research/oracle/riscv/rv_loop.jsonl') if 'no entry in the riscv opcode table' in ((json.loads(l).get('verdict') or {}).get('reason') or '')]; [print(seen[m]) for m in sorted(seen) if m in ('bseti', 'fsgnjn.d')]"
NotModeled: no entry in the riscv opcode table for 'bseti' (line 'bseti a2, zero, 0x3f')
NotModeled: no entry in the riscv opcode table for 'fsgnjn.d' (line 'fsgnjn.d ft0, ft0, ft0')
```

Five in all, which is exactly the five the brief names.

### 4.2 The five rows, each with its meaning and where it sits

Three are new entries in the opcode table; two are compressed spellings, and
a compressed instruction IS one of the others with its operands restricted,
so it is written as an EXPANSION and the meaning stays in one place.

| mnemonic | extension | what the row says | where |
|---|---|---|---|
| `add.uw` | Zba | the FIRST source cut to its low 32 bits and ZERO-extended, added to the whole second source. Every other 32-bit form in this file sign-extends; this one does not, because its purpose is to turn an unsigned 32-bit index into a 64-bit address | entry, `build_add_unsigned_word` |
| `bseti` | Zbs | the first source with the single bit named by the immediate SET; the shift amount is the low six bits at 64, the same masking rule the shift-immediate forms use | entry, `build_bit_set_immediate` |
| `fsgnjn.d` | D | the result carries the first source's every bit BUT the sign, and the OPPOSITE of the second source's sign bit. Written on the BITS, not through the float sort: sign injection raises no exception, does not canonicalise a NaN and moves a signalling NaN through unchanged | entry, `build_float_sign_inject` |
| `c.mul` | Zcb | `mul rd, rd, rs2` — the destination is also the first source | expansion |
| `c.zext.w` | Zcb | `add.uw rd, rd, zero` — one named register, which is both the destination and the only source | expansion |

The table now holds **111** entries where it held 108; the two compressed
forms are in the expansion table, not the entry table, which is why the
count moves by three and not five.

### 4.3 Level 0 for the five new rows — the check at points

**THE HEADLINE CARRIES ITS READING: THIS IS A CHECK AT POINTS, NOT AN
EQUALITY.** Agreement at every point sampled is evidence that the two
readings compute the same mapping; it is not a proof. Lane
`rv3_l6_sail_new_rows_again.sh`, artifacts `level0_points_rv3.json` (the
brief's cap of 20,000 points per instruction) and
`level0_points_rv3_sample.json` (the sample, 200 points per instruction).

| `mnem` | outcome | variants | points | agree | disagree |
|---|---|---|---|---|---|
| `add.uw` | AGREES_AT_EVERY_POINT | 1 | 20,000 | 20,000 | 0 |
| `bseti` | AGREES_AT_EVERY_POINT | 64 | 19,968 | 19,968 | 0 |
| `c.mul` | AGREES_AT_EVERY_POINT | 1 | 20,000 | 20,000 | 0 |
| `c.zext.w` | AGREES_AT_EVERY_POINT | 1 | 20,000 | 20,000 | 0 |
| `fsgnjn.d` | AGREES_AT_EVERY_POINT | 1 | 20,000 | 20,000 | 0 |
| **all five** | | **68** | **99,968** | **99,968** | **0** |

**Zero disagreements, so zero defects were found and no row had to be
fixed.** The brief's instruction — "a disagreement is a defect fixed with
the row shown" — had nothing to act on, exactly as task rv1 found for the
base set.

`bseti` reads 19,968 points and not 20,000 because its shape is one program
per shift amount: 64 amounts at 312 points each is 19,968, and the harness
never rounds a count up to make a headline read better.

**Three things the rv1 harness could not say, and each is a fact rather
than a convenience.**

1. **An `-march` string that names the new extensions.** **LITERAL**, lane
   `rv3_l3_new_rows_probe.sh`, the assembler under task rv1's own string:
   ```
   /work/rv3probe2/five.S:3:5: error: instruction requires the following: 'Zba' (Address Generation Instructions)
   /work/rv3probe2/five.S:4:5: error: instruction requires the following: 'Zbs' (Single-Bit Instructions)
   /work/rv3probe2/five.S:5:5: error: instruction requires the following: 'Zcb' (Compressed basic bit manipulation instructions)
   /work/rv3probe2/five.S:6:5: error: instruction requires the following: 'Zba' (Address Generation Instructions), 'Zcb' (Compressed basic bit manipulation instructions)
   ```
   The five rows assemble under `rv64gc_zba_zbb_zbs_zcb_zicond`; task rv1's
   own rows keep `rv64gc_zicond` and nothing about them changed.
2. **A destination that is also a source.** A compressed form names two
   registers, not three, so `c.mul a0, a1` leaves its answer in `a0` and
   `c.zext.w a0` in `a0`. The harness gained a per-row statement of where
   the two inputs go and where the answer is read from; every rv1 row takes
   rv1's own values as the default.
3. **A float round trip, and THE MODEL BEING RIGHT.** `fsgnjn.d` reads and
   writes the float file and the harness stores from an integer register, so
   the two operands are moved in with `fmv.d.x` and the answer out with
   `fmv.x.d`. On the first run the model refused. **LITERAL**, lane
   `rv3_l5_float_trap_probe.sh`, the program exactly as the rv1 harness
   writes it:
   ```
   FAILURE: possible trap loop detected with MEPC=0x80000016 and SEPC=0x0
   ```
   **AT RESET THE FLOAT UNIT IS OFF**: `mstatus.FS` holds Off and every
   floating-point instruction raises an illegal-instruction trap, which is
   what real hardware does. `csrs mstatus, 0x6000` sets FS to Dirty, and the
   same program then answers — **LITERAL**, same lane, the model's own
   signature beside the reference's own reading of the same two points:
   ```
   SUCCESS
   -- signature:
   00000000
   bff00000
   00000000
   402e0000
   [3/3] what the reference says the same two points give
   0xbff0000000000000
   0x402e000000000000
   ```
   This reference walks a body inside a function that a running program
   called, where FS is already on, so the prologue states the condition the
   walk already assumes.

**THE `fsgnjn.d` ROW IS A COMPOSITE AND SAYS SO ON ITSELF.** Its agreement
is an agreement about `fmv.d.x`, `fsgnjn.d` and `fmv.x.d` together, because
those three are what the program runs and what the reference walks. The row
carries that as `harness_note`; it is not counted as three separate checks.

---

## 5. The inheritance re-run — section 1 row 3

### 5.1 The installs, verified, each with its own probe

Lane `rv3_l1_installs.sh`. Each line below is **LITERAL** from that lane's
log.

| what | probe | output |
|---|---|---|
| rust riscv64 with a standard library | `rustup target list --installed` | `riscv64gc-unknown-linux-gnu` / `riscv64gc-unknown-none-elf` / `x86_64-unknown-linux-gnu` |
| rustc on a source needing `std` | `rustc --crate-type=lib --emit=obj -C opt-level=1 --target=riscv64gc-unknown-linux-gnu` on a `Vec` function | `rustc riscv64 std rc=0` |
| the riscv64 gcc cross toolchain | `riscv64-linux-gnu-g++ --version \| head -1` | `riscv64-linux-gnu-g++ (Ubuntu 15.2.0-16ubuntu1) 15.2.0` |
| its glibc headers | `ls /usr/riscv64-linux-gnu/include/string.h` | `/usr/riscv64-linux-gnu/include/string.h` |
| clang for riscv64 c, with `string.h` and `memcpy` | `clang -std=c17 -O1 --target=riscv64-linux-gnu --gcc-toolchain=/usr -c` | `clang c riscv64 rc=0` |
| clang++ for riscv64 cpp, with `<vector>` | `/usr/bin/clang++ -std=c++20 -O1 --target=riscv64-linux-gnu --gcc-toolchain=/usr -c` | `clang++ cpp riscv64 rc=0` |
| swift, anywhere | `which swiftc` | `/drop/rv3_l1_installs.sh: line 83: swiftc: command not found` |

**The optimisation levels are the corpus's own and are not touched**:
`-O1` for c, `-O1` for cpp, `-C opt-level=1` for rust, no flag for go —
`PRIVATE/PseudoCoupHQ/Research/op_pipeline/lane_gen.py`'s own ship
table with the target added and nothing else changed. `--emit=obj` means
rust needs NO LINKER: the object is carved directly, so a missing riscv64
linker cannot refuse a source that compiled.

### 5.2 The per-target table, task rv2's run beside this one

Lane `rv3_l7_inherit_again.sh`, artifacts `certificates_riscv64_rv3.jsonl`
(734 records) and `certificates_riscv64_rv3.json`. **The twins read, the
bank records chosen, the alignment (an argument's position), the gate and
the record shape are task rv2's own and are CALLED, not copied — the only
thing that moved is the compile route.**

| target | rv2 (log_259) | rv3 (this task) |
|---|---|---|
| `c` | PROVED 32, BUILD_REFUSED 15, WALK_REFUSED 11 | **PROVED 58** |
| `cpp` | NOT_ATTEMPTED 54 | **PROVED 54** |
| `go` | PROVED 71 | PROVED 71 |
| `rust` | BUILD_REFUSED 61 | **PROVED 61** |
| `swift` | NOT_ATTEMPTED 56 | NOT_ATTEMPTED 56 |
| `cpython` `php` `ruby` `java` `javascript` `dart` `csharp` | TRANSFERS_AS_IT_IS 62 each, 434 in all | TRANSFERS_AS_IT_IS 62 each, 434 in all |

| what | rv2 | rv3 |
|---|---|---|
| certificates attempted | 734 | 734 |
| **PROVED on riscv64**, at the cell's own `key_width` | 103 | **244** |
| **DISPROVED on riscv64** | 0 | **0** |
| UNDECIDED at 3,000 ms | 0 | **0** |
| transferred as they are (interpreted) | 434 | 434 |
| refused, with a cause | 197 | **56** |
| distinct RISC-V cells with an inherited PROVED certificate | 34 | **35** |

**Every certificate whose source built now builds, carves, walks and is
proved.** The 56 refusals left are one target and one cause: there is no
`swiftc` in the image at all, so no swift source was compiled for any
architecture here. **LITERAL**, lane `rv3_l11_more_transcripts.sh`:

```
$ python3 -c "import json, collections; rows=[json.loads(l) for l in open('PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64_rv3.jsonl')]; r=[x for x in rows if x['kind']=='refused']; print('refused', len(r), sorted(collections.Counter((x['target'], (x['verdict'] or {}).get('outcome')) for x in r).items()))"
refused 56 [(('swift', 'NOT_ATTEMPTED'), 56)]
```

### 5.3 The two widths, and the one fact between them

| reading | rows |
|---|---|
| PROVED at the cell's own `key_width` (the headline; the pipeline's own rule for a narrow answer) | 244 |
| of those, also PROVED at the WHOLE written place | 174 |
| of those, DISPROVED above the operation's own width | 70 |

The 70 are the extension rule task rv2 recorded and not a computation
difference: a c function returning a 32-bit value leaves it SIGN-extended in
`a0` under the riscv64 psABI, and the x86 cell's term says the upper 32 bits
are ZERO. Each row carries it as `verdict_at_the_whole_place`; none is
hidden.

### 5.4 The cells, and the count beside 116 of 255

| what | cells | share of the 255 |
|---|---|---|
| RISC-V cells the model table holds | 255 | 100% |
| reached by an INHERITED proved certificate, rv2 | 34 | 13.3% |
| reached by an INHERITED proved certificate, rv3 | **35** | **13.7%** |
| PROVED by task rv2's own loop | 82 | 32.2% |
| **union, rv2's own headline** | **116** | **45.5%** |
| **union, this task's inheritance with rv2's loop** | **117** | **45.9%** |

**THE 117 CARRIES ITS READING AND IT IS NOT THE FINAL NUMBER.** It is the
union of THIS task's inheritance with TASK RV2's loop, and rv2's loop ran
over the cells untwinned under the PRE-correction x86 table with the lifter
as it stood before this task's five rows. The count the brief's section 2
asks for — the loop re-run over the cells still untwinned after ref2's
re-derivation, with the five new rows in the lifter — is section 6 and waits
for ref2. What 117 does say is the direction and the size of the move: the
compilers were never the binding constraint on this number, and they are now
not a constraint at all.

The one cell the re-run gained is `('fsub.s', 'fpr_fpr_fpr', 32)` and none
was lost; the sixth block of section 10 is the command that prints it.
141 more certificates were proved and they landed on one new cell, because
the certificates rv2 could not build were overwhelmingly other targets'
readings of cells `c` and `go` had already reached. That is a fact about the
bank's shape, and it is the same fact log_259 reported from the other side:
the limit is on the x86 side.

---

## 6. What waits for ref2 — section 1 rows 2 and 4, and section 2

Each is stated with what it needs and what is already measured for it, so a
follow-on lane starts with the numbers rather than the search.

| brief item | status | what it needs | what is already on disk for it |
|---|---|---|---|
| section 1 row 2 — `twins.json` re-derived against ref2's corrected model table; both readings beside rv2's 102 / 161; every twin that appeared or vanished, by cell, with the term text that changed | **WAITS FOR ref2** | ref2's DevComms log, and its re-derived model table declared final | the re-derived table is on disk as `PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/level0/model_table_rows_ref2_c4.json`, sha256 `43433ae2…d221e`; rv2's `twins.py` takes the rows file as an argument, so the re-run is a one-argument change |
| section 1 row 4 — the riscv64 certificates joined to `certificates.jsonl` with `arch` and `inherited_from`; `bank.py`'s delta and 5% audit reading `arch` as part of the key; bank count before → after | **WAITS FOR ref2** | ref2 is itself writing the bank (its brief section 2(d) adds `reference_version` and marks `reference_superseded`), so appending now would collide | **bank before: 24,758 records, every one with `arch` absent** — LITERAL, `records 24758 by arch [('None', 24758)]`. The 734 rv3 records are in `certificates_riscv64_rv3.jsonl` in the bank's own record shape, each carrying `arch: "riscv64"` and `inherited_from`; they are a concatenation away |
| section 2 — the loop over the cells still untwinned after the re-derivation, both routes; the collapse column; the cells-proved count; the three readings | **WAITS FOR ref2** | row 2's `twins.json` | the lifter's five new rows are in place, so the 16 loop runs task rv2 recorded as refused on a missing mnemonic will now walk; `rv_loop.py` takes the twins file as an argument |

**Nothing under `PRIVATE/PseudoCoupHQ/Research/op_pipeline/` was
written, and neither was the bank file.** `bank.py` was not modified: the
brief authorises the `arch` key as part of row 4, and row 4 waits.

---

## 7. The flags

Each is a flag with its literal output, not a workaround and not a redesign.
Status is on every item.

1. **Task rv2's flag 2 (rust refused 61 for want of `std`) — CLOSED.** The
   image carries `riscv64gc-unknown-linux-gnu`. All 61 rust certificates now
   compile, carve, walk and are PROVED. **LITERAL**, lane
   `rv3_l1_installs.sh`: `rustc riscv64 std rc=0`; and from the artifact,
   lane `rv3_l11_more_transcripts.sh`:

```
$ python3 -c "import json, collections; rows=[json.loads(l) for l in open('PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64_rv3.jsonl')]; r=[x for x in rows if x['target']=='rust']; print('rust rows', len(r), sorted(collections.Counter(x['kind'] for x in r).items()), 'compiler', sorted(set((x.get('compiler') or {}).get('target_triple') for x in r)))"
rust rows 61 [('proved', 61)] compiler ['riscv64gc-unknown-linux-gnu (rustc --target, --emit=obj)']
```
2. **Task rv2's flag 3 (15 c certificates refused on `string.h`) — CLOSED.**
   The riscv64 glibc headers are at `/usr/riscv64-linux-gnu/include` and
   clang reaches them with `--target=riscv64-linux-gnu --gcc-toolchain=/usr`.
   All 58 c certificates are PROVED, including the 11 task rv2 recorded as
   WALK_REFUSED, because those refused on a missing lifter row that this task
   added. **LITERAL**, lane `rv3_l1_installs.sh`: `clang c riscv64 rc=0`.
3. **Task rv2's flag 4 (27 rows refused on Zba/Zbb/Zbs and compressed forms)
   — CLOSED.** The lifter gained exactly the five, each checked against the
   Sail model at 20,000 points. Section 4.
4. **Task rv2's flag 7 (`cpp` was not attempted) — CLOSED.** `clang++` aims
   at riscv64 by the same route as `clang`, `<vector>` resolves, and all 54
   cpp certificates are PROVED. **LITERAL**, lane `rv3_l1_installs.sh`:
   `clang++ cpp riscv64 rc=0`.
5. **`swift` has no compiler in this image at all — OPEN, and it is a wider
   fact than "no riscv64 swift".** **LITERAL**, lane `rv3_l1_installs.sh`:
   `/drop/rv3_l1_installs.sh: line 83: swiftc: command not found`. The `rv3`
   instance mounts `sandbox-persist` read-only exactly as `rv2` did, and
   `swiftc` is not on the path there either. 56 certificates sit
   NOT_ATTEMPTED for that reason alone. A riscv64 swift toolchain is an
   install and therefore the coordinator's.
6. **The Sail harness needed the float unit switched on, and the model was
   right to refuse without it — RESOLVED, and recorded because it is a fact
   of the machine.** **LITERAL**, lane `rv3_l5_float_trap_probe.sh`:
   `FAILURE: possible trap loop detected with MEPC=0x80000016 and SEPC=0x0`.
   Two instructions of prologue (`li t0, 0x6000` / `csrs mstatus, t0`) state
   the condition a called function already sits under.
7. **`sail_points.py` prints the abort name `ABORT_MEMORY_RV1`, not
   `ABORT_MEMORY_RV3` — REPORTED, not renamed.** The ceiling is the same
   6 GB the brief states, and the peak of the five-row run was 57.5 MB. The
   constant is task rv1's own and lives in its own file; this task's own
   driver `inherit_rv3.py` names `ABORT_MEMORY_RV3`. Renaming a closed task's
   constant would falsify its log's own transcripts, so it was not done.
8. **Task ref2 has not closed — REPORTED, and it is the brief's own stop
   rule rather than a problem.** Section 3's table. Rows 2 and 4 and section
   2 are section 6 of this log. Nothing polled for ref2.
9. **A `cpp` and a `rust` argument sequence had to be stated — DECIDED,
   mechanical.** `claim_check.py` states the x86-64 and riscv64 argument
   sequences for `c` and `go` only. Both cpp and rust render `extern "C"`
   functions, so both arrive under the System V AMD64 C sequence
   (`rdi, rsi, rdx, rcx, r8, r9`; `xmm0..`) and the RISC-V psABI's own
   (`a0..a7`; `fa0..fa7`) — the same sequences the file already states for
   `c`. They are added to its tables at import time by `inherit_rv3.py`;
   nothing in `claim_check.py` was rewritten.

---

## 8. The guard, memory, and where nothing was written

- **The spelling guard passes on every json and jsonl this task wrote.**
  **LITERAL**, lane `rv3_l8_counts_and_guard.sh`:
  `operator inventory: 91 tokens read from probe_manifest_*.json`, then
  `PASS census_rv3.json`, `PASS census_rv3_sample.json`,
  `PASS level0_points_rv3.json`, `PASS level0_points_rv3_sample.json`,
  `PASS certificates_riscv64_rv3.json`,
  `PASS certificates_riscv64_rv3_sample.json`,
  `PASS certificates_riscv64_rv3.jsonl.as_one.json`,
  `PASS certificates_riscv64_rv3_sample.jsonl.as_one.json`, `guard rc=0`.
  The guard was not modified.
- **The count of the word the guard hunts for, over every file this task
  added or changed:** **LITERAL**, same lane:
  `deliverable files scanned: 13` / `deliverable files containing the word: 0`.
- **Memory.** Bound 6 GB, named abort `ABORT_MEMORY_RV3`, never raised. Peak
  resident per stage: the census 120.7 MB; the Sail check 57.5 MB; the
  inheritance 252.2 MB. The sample the law asks for ran first in every case:
  the census at 20 sources (121 MB), the Sail check at 200 points per
  instruction (47.5 MB), the inheritance at 20 certificates (252.2 MB).
- **Nothing was written outside
  `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/`**, this log, and the
  two PROGRESS files the brief names. `reference.py`, `condition_table.py`,
  `term.py`, `model_translate.py`, `model_table.py`, `bank.py`,
  `check_no_spelling_keys.py`, `inherit.py`, `twins.py`, `claim_check.py`,
  `riscv_carve.py` and the bank were READ.
- **Nothing under `PUBLIC/Airlock/` or `<runs>/` was
  deleted**, on either machine.

---

## 9. How to re-run any of it

`$R` is `bash PUBLIC/Airlock/remote_lane.sh` with
`AIRLOCK_REMOTE=<user>@<tower>` and
`AIRLOCK_REMOTE_ROOT=Programming/Airlock`.

| what | command |
|---|---|
| the instance | `bash PUBLIC/Airlock/remote_lane.sh conf PUBLIC/Airlock/instances/rv3.conf` then `bash PUBLIC/Airlock/remote_lane.sh up --instance rv3` |
| mirror the folder | `bash PUBLIC/Airlock/remote_lane.sh sync-to Programming/PseudoCoupHQ/Research/oracle/riscv` |
| any lane | `bash PUBLIC/Airlock/remote_lane.sh submit --instance rv3 --batch rv3 --weight 1 PRIVATE/PseudoCoupHQ/Research/oracle/riscv/lanes_rv3/<lane>.sh` |
| wait for it | `bash PUBLIC/Airlock/remote_lane.sh wait --instance rv3 <lane>.sh` — repeated, each call at most 100 s |
| bring it back | `bash PUBLIC/Airlock/remote_lane.sh sync-back Programming/PseudoCoupHQ/Research/oracle/riscv` |

Inside a lane, where this repository is mounted at `PseudoCoupHQ`,
the three commands that produce the deliverable are, in order:

- `python3 PseudoCoupHQ/Research/oracle/riscv/inherit_rv3.py census PseudoCoupHQ/Research/oracle/arch_opcodes/level0/ref2_originals PseudoCoupHQ/Research/op_pipeline PseudoCoupHQ/Research/oracle/riscv/twins.json PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly PseudoCoupHQ/Research/oracle/riscv/census_rv3 /work/rv3census`
- `python3 PseudoCoupHQ/Research/oracle/riscv/sail_points.py PseudoCoupHQ/Research/oracle/riscv/level0_points_rv3 /work/rv3sail2 --points 20000 --only add.uw,bseti,c.mul,c.zext.w,fsgnjn.d`
- `python3 PseudoCoupHQ/Research/oracle/riscv/inherit_rv3.py run PseudoCoupHQ/Research/oracle/arch_opcodes/level0/ref2_originals PseudoCoupHQ/Research/op_pipeline PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table_rows.json PseudoCoupHQ/Research/oracle/riscv/twins.json PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64_rv3 /work/rv3inh`

---

## 10. The claims, each with the command that reproduces it

Every block below is a transcript from lane `rv3_l9_claim_transcripts.sh`,
pasted whole and not tidied. Each command runs INSIDE the `rv3` instance,
where this repository is mounted at `PseudoCoupHQ`.

The census — the counts of section 4.1:

```
$ python3 -c "import json, collections; d=json.load(open('PseudoCoupHQ/Research/oracle/riscv/census_rv3.json')); print('sources', len(d['rows']), sorted(collections.Counter(r['outcome'] for r in d['rows']).items())); print('no entry:', sorted((m, d['no_entry_in_the_opcode_table'][m]['lines'], d['no_entry_in_the_opcode_table'][m]['targets']) for m in d['no_entry_in_the_opcode_table']))"
sources 244 [('CARVED', 244)]
no entry: [('add.uw', 8, ['c', 'cpp']), ('c.mul', 6, ['c', 'cpp']), ('c.zext.w', 12, ['c', 'cpp'])]
```

The five new rows against the Sail model — the counts of section 4.3:

```
$ python3 -c "import json; d=json.load(open('PseudoCoupHQ/Research/oracle/riscv/level0_points_rv3.json')); r=d['rows']; print('rows', len(r), 'outcomes', sorted(set(x['outcome'] for x in r))); print('variants', sum(x['variants'] for x in r), 'points', sum(x['points'] for x in r), 'agree', sum(x['agree'] for x in r), 'disagree', sum(x['disagree'] for x in r))"
rows 5 outcomes ['AGREES_AT_EVERY_POINT']
variants 68 points 99968 agree 99968 disagree 0
```

The inheritance, per target — the table of section 5.2:

```
$ python3 -c "import json, collections; rows=[json.loads(l) for l in open('PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64_rv3.jsonl')]; t=collections.defaultdict(collections.Counter); [t[r['target']].update([(r['verdict'] or {}).get('outcome')]) for r in rows]; print(sorted((k, sorted(v.items())) for k, v in t.items()))"
[('c', [('PROVED', 58)]), ('cpp', [('PROVED', 54)]), ('cpython', [('TRANSFERS_AS_IT_IS', 62)]), ('csharp', [('TRANSFERS_AS_IT_IS', 62)]), ('dart', [('TRANSFERS_AS_IT_IS', 62)]), ('go', [('PROVED', 71)]), ('java', [('TRANSFERS_AS_IT_IS', 62)]), ('javascript', [('TRANSFERS_AS_IT_IS', 62)]), ('php', [('TRANSFERS_AS_IT_IS', 62)]), ('ruby', [('TRANSFERS_AS_IT_IS', 62)]), ('rust', [('PROVED', 61)]), ('swift', [('NOT_ATTEMPTED', 56)])]
```

The inheritance's tally, task rv2's beside this one — section 5.2:

```
$ python3 -c "import json, collections; old=[json.loads(l) for l in open('PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64.jsonl')]; new=[json.loads(l) for l in open('PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64_rv3.jsonl')]; print('rv2', sorted(collections.Counter(r['kind'] for r in old).items())); print('rv3', sorted(collections.Counter(r['kind'] for r in new).items()))"
rv2 [('agreed', 434), ('proved', 103), ('refused', 197)]
rv3 [('agreed', 434), ('proved', 244), ('refused', 56)]
```

The whole-place reading on the proved rows — section 5.3:

```
$ python3 -c "import json, collections; rows=[json.loads(l) for l in open('PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64_rv3.jsonl')]; p=[r for r in rows if r['kind']=='proved']; print('proved at key_width', len(p), 'at the whole place', sorted(collections.Counter((r.get('verdict_at_the_whole_place') or {}).get('outcome') for r in p).items()))"
proved at key_width 244 at the whole place [('DISPROVED', 70), ('PROVED', 174)]
```

The cells, and the union with task rv2's own loop — section 5.4:

```
$ python3 -c "
import json
RV='PseudoCoupHQ/Research/oracle/riscv'
def cells(path):
    out=set()
    for line in open(path):
        line=line.strip()
        if not line: continue
        r=json.loads(line)
        if r['kind']!='proved': continue
        c=r['cell']; out.add((c.get('mnem'),c.get('shape'),c.get('key_width')))
    return out
a=cells(RV+'/certificates_riscv64.jsonl'); b=cells(RV+'/certificates_riscv64_rv3.jsonl'); l=cells(RV+'/rv_loop.jsonl')
print('inherited rv2',len(a),'inherited rv3',len(b),'loop rv2',len(l))
print('union rv2',len(a|l),'union rv3 inheritance + rv2 loop',len(b|l))
print('gained',sorted(b-a),'lost',sorted(a-b))
"
inherited rv2 34 inherited rv3 35 loop rv2 82
union rv2 116 union rv3 inheritance + rv2 loop 117
gained [('fsub.s', 'fpr_fpr_fpr', 32)] lost []
```

The bank, before this task appends anything — section 6:

```
$ python3 -c "import json, collections; n=0; a=collections.Counter(); [ (n:=n) for _ in ()]; rows=[json.loads(l) for l in open('PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl') if l.strip()]; print('records', len(rows), 'by arch', sorted(collections.Counter(str(r.get('arch')) for r in rows).items()))"
records 24758 by arch [('None', 24758)]
```

The spelling guard over every json and jsonl this task wrote — section 8:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/riscv/census_rv3.json PseudoCoupHQ/Research/oracle/riscv/census_rv3_sample.json PseudoCoupHQ/Research/oracle/riscv/level0_points_rv3.json PseudoCoupHQ/Research/oracle/riscv/level0_points_rv3_sample.json PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64_rv3.json PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64_rv3_sample.json PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64_rv3.jsonl.as_one.json PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64_rv3_sample.jsonl.as_one.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS census_rv3.json -- no operator token in any key, grouping, pairing or row structure
PASS census_rv3_sample.json -- no operator token in any key, grouping, pairing or row structure
PASS level0_points_rv3.json -- no operator token in any key, grouping, pairing or row structure
PASS level0_points_rv3_sample.json -- no operator token in any key, grouping, pairing or row structure
PASS certificates_riscv64_rv3.json -- no operator token in any key, grouping, pairing or row structure
PASS certificates_riscv64_rv3_sample.json -- no operator token in any key, grouping, pairing or row structure
PASS certificates_riscv64_rv3.jsonl.as_one.json -- no operator token in any key, grouping, pairing or row structure
PASS certificates_riscv64_rv3_sample.jsonl.as_one.json -- no operator token in any key, grouping, pairing or row structure
```

---

## 10a. The verifier's tally

From lane `rv3_l13_verify_final.sh`, run from this task's own instance with
`python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_260_rv3_the_lifter_gains_what_clang_writes_and_the_inheritance_re_run.md`:

| outcome | claims |
|---|---|
| MATCHES | 12 |
| **DIFFERS** | **0** |
| UNVERIFIABLE | 4 |
| REFUSED | 0 |
| NOT_RERUNNABLE | 0 |
| population | 16 claims across 1 log |

Its one line: `12 of 16 claims reproduce; 4 (25%) carry nothing to re-run`.
Nothing was changed to make the tally read better and the verifier was not
touched. Two earlier passes are in the record and each was answered by
giving a citation a command rather than by deleting the citation: lane
`rv3_l10_verify.sh` read 8 of 15 with 7 unverifiable, lane
`rv3_l12_verify_again.sh` read 11 of 16 with 5.

The four that remain are prose the protocol asks for: two paragraphs of the
walkthrough (section 1), which `order.walkthrough-before-numbers` requires to
carry no figures of its own; the sentence in section 5.4 that points at
section 10's sixth block rather than repeating it; and the second flag of
section 7, whose evidence is the installs table of section 5.1.

**The pass above was over the log as it stood the moment before this section
was written, so a second pass was run over the log WITH it**, lane
`rv3_l14_verify_after_the_tally.sh`, and it reads the same six numbers:
16 claims, MATCHES 12, DIFFERS 0, UNVERIFIABLE 4, REFUSED 0,
NOT_RERUNNABLE 0 — this section carries no `$ ` line of its own and asserts
no check, so it adds no claim to either bucket.

---

## 11. Decided, recorded for audit

- **The lifter's new vocabulary was READ OFF CARVED BODIES, not chosen from
  a list.** `census_rv3.json` compiled every certificate source on the four
  compiled targets and counted the mnemonics with no entry; task rv2's own
  loop store supplied the other two with the body line each refused on. The
  x86 table's rule — no entry is invented for an opcode no body contains —
  is what the census implements.
- **Exactly five rows were added and not one more.** The neighbouring
  members of the same extensions (`sh1add`, `bclr`, `fsgnj.d`, and the rest)
  are NOT in the table, because no body this line has carved spells them.
- **A compressed form is written as an EXPANSION, never as a second
  meaning.** `c.mul` is `mul rd, rd, rs2` and `c.zext.w` is
  `add.uw rd, rd, zero`, which is how the architecture manual defines them,
  so the meaning stays in one place.
- **`fsgnjn.d` is written on the BITS, not through z3's float sort**, because
  sign injection raises no exception, does not canonicalise a NaN and moves a
  signalling NaN through unchanged.
- **The `fsgnjn.d` Sail row is a COMPOSITE of three instructions** and says so
  on itself as `harness_note`; its agreement is an agreement about
  `fmv.d.x` and `fmv.x.d` as well.
- **The harness enables the float unit before the loop**, because at reset
  `mstatus.FS` is Off and the model traps — the model being right. Every
  task rv1 row keeps rv1's own program, registers and `-march` string
  unchanged; the additions take those as their defaults.
- **The inheritance re-run reads the SAME pre-correction x86 store task rv2
  read** (`ref2_originals/reference.py`, sha256 `3893363145…`, and
  `model_table_rows.json`, sha256 `f146dcba…`), so the per-target table can be
  read beside rv2's with the compile route as the only difference.
  Re-deriving against ref2's corrected table is row 2, and it waits.
- **`cpp` and `rust` take the `c` argument sequences**, because both render
  `extern "C"` functions; the tables are extended at import time and
  `claim_check.py` is not rewritten.
- **Task rv2's `inherit.py` is CALLED, not copied.** `inherit_rv3.py`
  replaces four compile routes, the not-attempted list and the abort name,
  and calls rv2's own `twinned_cells`, `bank_lines` and `one_certificate` for
  everything else.
- **`certificates_riscv64.jsonl` (task rv2's) was not overwritten**; this
  task's records are beside it in `certificates_riscv64_rv3.jsonl`, so the two
  runs can be read against each other.
- **`bank.py` was not modified and the bank file was not appended to**,
  because that is row 4 and row 4 waits for ref2.
- **The instance configuration `rv3.conf`** is at
  `PUBLIC/Airlock/instances/rv3.conf`.

## 12. Awaiting the owner

- **Whether the Hub's dictionary key must carry the arrival contract's
  extension rule.** Task rv2 left this open and this task moved the numbers:
  70 of 244 inherited proofs now hold at the operation's own width and not at
  the whole register, where rv2 had 20 of 103. The proportion barely moved
  (19.4% then, 28.7% now) and the fact is the same one — a 32-bit result is
  sign-extended into a riscv64 register and zero-extended into an x86 one.
  Whether the Hub keys on it or picks it by policy is a ruling, not a
  measurement.
- **A riscv64 swift toolchain, or a ruling that swift stays out of this
  line's riscv64 column.** 56 certificates are NOT_ATTEMPTED and the image
  has no `swiftc` at all.
