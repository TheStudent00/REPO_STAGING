# log 153 — TASK 53: layer 4 read off canon38, and the census re-filtered

Date: 2026-09-03. Home: `PseudoCoupHQ/Research/op_pipeline`.
Reads: `canon38_wrapped_{c,cpp,go,rust,swift}.json`, `canon38_interp.json`,
`canon38_regen_store/*.json` (log 152). Compares against: log 147 §13.5 and
`name_census3.json`.

---

# 0. The walk, in plain words, before any figure

**The three names, each introduced before it is used.**

- **THE LEDGER** is canon38's provenance table for one arch-unit: one row
  per value the unit's own machine code produces, each row saying what
  produced it and which rows it read. `OUT-0` is the row holding the
  answer.
- **LAYER 4** is that table read as arithmetic. Start at `OUT-0`, take its
  producer and its operand rows, recurse: what comes out is one z3 term
  over the unit's inputs. No mining, no instruction-sequence patterns —
  a transcription.
- **THE CENSUS** is the filter that falls out of it: the rows whose
  producer has no arithmetic written for it. Nothing is surveyed; the
  census is exactly the set of places the transcription raised `NoTerm`.

**What this lap changed.** Task 48 did all three over canon37, whose ledger
had six blocks. canon38 (task 52) gave the ledger a `STACK` block, an `X87`
block, a per-opcode destination table, a `flags only` row type, positional
branch labels, and typed producers. So the census was rebuilt against the
new ledger rather than adjusted. The headline: **8,044 census rows over
5,507 units becomes 1,719 rows over 1,668 units**, and the three causes the
brief predicted would leave — the machine stack (4,298 rows), the implicit
destination (1,558), the x87 pairs (1,072) — are all at **zero**.

**What did not go the predicted way, said here rather than buried.** The
826 withdrawn units did NOT all prove. 410 of them did — every one whose
answer reads the division's QUOTIENT half. 415 stayed withdrawn, and §5
shows why with the counterexample: the route-one reference simulator
computes the division REMAINDER with z3's `%` operator, which is
sign-follows-the-divisor, while the machine's remainder follows the
dividend. The ledger's term is the correct one; the reference is wrong at
that one opcode.

---

# 1. The verdict, with its population

## 1.1 The population line

Every unit task 52 proved: **9 interpreter, 1,763 original, 28,664
regenerated — 30,436 in all**. Nothing is sampled; both gate routes ran on
every one.

LITERAL — `zero_regression53_printed.txt`, CLAIM THREE:

```
  population          canon38    task 53    delta
  interpreter               9          9        0
  original               1763       1763        0
  regenerated           28664      28664        0
  all three             30436      30436        0
```

## 1.2 The one-line state

**30,436 ledgers transcribed with 0 replay refusals; 29,149 carry an OUT-0
term; 23,132 of those terms are proved on at least one gate route; 415 are
disproved and withdrawn; 5,602 are undecided on both routes; 1,287 units
build no term at all.**

## 1.3 The four figures against log 147 §13.5, with the population each
## covered

Log 147 §13.5's block covered **the same population** — its own line reads
`units 30436` — so the two are directly comparable.

| figure | log 147 §13.5 (canon37) | this lap (canon38) | delta |
|---|---|---|---|
| term proved on at least one route | 23,414 | 23,132 | −282 |
| term DISPROVED — withdrawn | 826 | 415 | −411 |
| term undecided on both routes | 2,054 | 5,602 | +3,548 |
| no term built | 4,142 | 1,287 | −2,855 |
| units | 30,436 | 30,436 | 0 |

LITERAL — `audit53_printed.txt`, the totals block:

```
ALL THREE POPULATIONS
  no term built                                       1287
  proved on route one (the ship simulation)          17489
  proved on route two (the text-order walk)          22715
  term DISPROVED -- withdrawn                          415
  term built                                         29149
  term proved on at least one route                  23132
  term undecided on both routes                       5602
  units                                              30436

CONSISTENCY -- units proved on one route and disproved on the other: 0
```

GLOSS, and the honest reading of the one figure that went the wrong way.
2,855 units left "no term" and 3,548 arrived in "undecided": the ledger now
builds terms for thousands of bodies neither gate route can DECIDE, because
neither reference models the machine stack or the x87 stack (§6). The
proved count moved by −282, and §4 accounts for every unit of that movement
by name.

## 1.4 Per population

LITERAL — `audit53_printed.txt`:

```
POPULATION: interpreter
  proved on route one (the ship simulation)              9
  proved on route two (the text-order walk)              8
  term built                                             9
  term proved on at least one route                      9
  units                                                  9

POPULATION: original
  no term built                                         35
  proved on route one (the ship simulation)            951
  proved on route two (the text-order walk)           1623
  term DISPROVED -- withdrawn                           12
  term built                                          1728
  term proved on at least one route                   1635
  term undecided on both routes                         81
  units                                               1763

POPULATION: regenerated
  no term built                                       1252
  proved on route one (the ship simulation)          16529
  proved on route two (the text-order walk)          21084
  term DISPROVED -- withdrawn                          403
  term built                                         27412
  term proved on at least one route                  21488
  term undecided on both routes                       5521
  units                                              28664
```

---

# 2. One transcription, literally, with values moving

The brief's step 1. `c/op_104` is c's `a + b` with `a` a 32-bit signed
integer and `b` a 64-bit one. Take `a = -5`, `b = 100`.

## 2.1 The body and the ledger as stored

LITERAL — `acceptance53_printed.txt`, part (a):

```
  c/op_104
    LITERAL -- body:  movslq %edi,%rax; add %rsi,%rax; ret
    LITERAL -- the stored ledger:
      row       size type                 produced by     operands
      IN-0      8    8-byte general value arrival
      IN-1      8    8-byte general value arrival
      TEMP-0    8    8-byte general value movslq          IN-0
      TEMP-1    8    8-byte general value add             IN-1,TEMP-0
      OUT-0     8    8-byte general value add             TEMP-1
```

## 2.2 Those two values moving through the five rows

- `IN-0` is where `a` arrives. With `a = -5`, the runner writes the 32-bit
  pattern `0xfffffffb` into it; the row is 8 bytes, so `%rdi` holds
  `0x00000000fffffffb`.
- `IN-1` is where `b` arrives: `100`, that is `0x64`.
- `TEMP-0` is `movslq %edi,%rax` — take the low 32 bits and sign-extend
  them to 64. `0xfffffffb` becomes `0xfffffffffffffffb`, which is `−5` at
  64 bits. The row records that `movslq` made it and that it read `IN-0`.
- `TEMP-1` is `add %rsi,%rax` — `−5 + 100 = 95`. The row records `add` and
  the two rows it read.
- `OUT-0` reads `TEMP-1` and is what the runner reads back: `95`.

## 2.3 The same five rows as terms, which is layer 4

LITERAL — same file, the term each row reads to:

```
      IN-0      seed_rdi
      IN-1      seed_rsi
      TEMP-0    SignExt(32, Extract(31, 0, seed_rdi))
      TEMP-1    SignExt(32, Extract(31, 0, seed_rdi)) + seed_rsi
      OUT-0     SignExt(32, Extract(31, 0, seed_rdi)) + seed_rsi
```

GLOSS: read the last line with `seed_rdi = 0x00000000fffffffb` and
`seed_rsi = 100` and it is the walk of §2.2 with the concrete values put
back. The term is the ledger read from `OUT-0` downward and nothing else.

## 2.4 Both gate routes on this one unit

LITERAL — same file:

```
    route one (the ship simulation): PROVED_EQUAL
        z3 proved the ledger-transcribed OUT-0 term equal to the value the
        unit's own ship body leaves in its own answer home, for every value
        of every register either side reads before writing
    route two (the text-order walk): PROVED_EQUAL
        z3 proved the ledger-transcribed OUT-0 term equal to the same body
        walked in text order, for every value of every register either walk
        reads before writing
```

---

# 3. THE CENSUS, printed

Population: every row of every canon38 ledger of all 30,436 units.
Source: `name_census4.json`, printed into `name_census4_printed.txt`.
**54 producers, 1,719 rows, 1,668 units.**

## 3.1 The table

LITERAL — `name_census4_printed.txt`:

```
producer                             rows  units kind       languages
----------------------------------------------------------------------
the body's last write to %rax         303    303 irregular  c,cpp,go
sbb + setl                            232    193 irregular  c,cpp,rust
fucomip + setae                       186    186 irregular  c,cpp,swift
sbb + setb                            175    175 irregular  c,cpp,rust,swift
sbb + setae                           162    162 irregular  c,cpp,rust
sbb + setge                           154    154 irregular  c,cpp,rust
fadds                                  96     96 irregular  c,cpp
the body's last write to %xmm0         32     32 irregular  c,cpp,go,rust,swift
fiadds                                 28     28 irregular  c,cpp
fimuls                                 28     28 irregular  c,cpp
faddp                                  22     22 irregular  c,cpp
fmulp                                  22     22 irregular  c,cpp
fiaddl                                 16     16 irregular  c,cpp
fimull                                 16     16 irregular  c,cpp
fidivrs                                14     14 irregular  c,cpp
fidivs                                 14     14 irregular  c,cpp
fisubrs                                14     14 irregular  c,cpp
fisubs                                 14     14 irregular  c,cpp
fdivp                                  11     11 irregular  c,cpp
fdivrp                                 11     11 irregular  c,cpp
fsubp                                  11     11 irregular  c,cpp
fsubrp                                 11     11 irregular  c,cpp
sbb + jae                              11     11 irregular  swift
sbb + jl                               10      9 irregular  swift
sbb + cmovae                            9      9 irregular  swift
fidivl                                  8      8 irregular  c,cpp
fidivrl                                 8      8 irregular  c,cpp
fisubl                                  8      8 irregular  c,cpp
fisubrl                                 8      8 irregular  c,cpp
fmuls                                   8      8 irregular  c,cpp
movzbl                                  7      7 regular    c,cpp,rust,swift
mul + jo                                6      6 irregular  swift
sbb + jb                                5      5 irregular  swift
sbb + jge                               5      5 irregular  swift
faddl                                   4      4 irregular  c,cpp
fdivrs                                  4      4 irregular  c,cpp
fdivs                                   4      4 irregular  c,cpp
fmull                                   4      4 irregular  c,cpp
fsubrs                                  4      4 irregular  c,cpp
fsubs                                   4      4 irregular  c,cpp
mul + seto                              4      2 irregular  swift
sbb + cmovb                             4      4 irregular  swift
sbb + cmovl                             4      2 irregular  swift
fdivl                                   2      2 irregular  c,cpp
fdivrl                                  2      2 irregular  c,cpp
fsubl                                   2      2 irregular  c,cpp
fsubrl                                  2      2 irregular  c,cpp
movsbl                                  2      2 regular    rust,swift
pmovmskb                                2      2 irregular  rust
sbb + jo                                2      2 irregular  swift
adc + jb                                1      1 irregular  swift
adc + jo                                1      1 irregular  swift
imul + jo                               1      1 irregular  swift
sbb + setne                             1      1 irregular  swift
```

## 3.2 The census is a different shape, not a shorter version of the old one

- **`push`, `pop`, `idiv`, `div`, `mul`, and every `fucomip`/`fucomi`
  comparison pair are gone from the table.** Those were 6,928 of
  census3's 8,044 rows.
- **What replaced them was hidden BEHIND them.** The x87 ARITHMETIC family
  (`fadds`, `faddp`, `fmulp`, `fidivl`, …) is 400 rows and is new to the
  census — canon37 could not reach those rows at all, because with no x87
  block the walk stopped at the comparison. The same is true of the `sbb`
  and `adc` flag pairs: canon37's layer 4 answered them from a stale
  earlier comparison's flags, so they never appeared as census rows. §4.2
  is that mechanism in full.

## 3.3 The delta by cause, computed

The grouping key is the **recorded reason sentence each census entry
carries**, never a producer's spelling. Every entry in both files was
matched against that sentence.

LITERAL — `audit53_printed.txt`:

```
cause (the artifact's own recorded reason)                   rows 3   rows 4    delta
----------------------------------------------------------------------------------------
an unconditional transfer is not a flag reader                  325        0     -325
no opcode in the body writes the answer register                 36      335      299
not yet grouped: no z3 term is written for this arch opcod        0        2        2
not yet grouped: no z3 term is written for this x87 arch o        0      400      400
not yet grouped: this suffix reads the carry bit, and the         0      186      186
the flags the setter left are not in the ledger                 746      787       41
the implicit destination                                       1558        0    -1558
the machine stack has no block                                 4298        0    -4298
the second byte of a register has no row                          8        9        1
the x87 stack has no rows                                      1072        0    -1072
this opcode reads a carry no earlier opcode set                   1        0       -1
----------------------------------------------------------------------------------------
TOTAL ROWS                                                     8044     1719    -6325
DISTINCT PRODUCERS                                               47       54        7
UNITS CARRYING AT LEAST ONE SUCH ROW                           5507     1668    -3839
```

GLOSS, cause by cause:

- **THE MACHINE STACK HAS NO BLOCK — 4,298 → 0.** Ruling 2's `STACK` block
  closed it entirely.
- **THE IMPLICIT DESTINATION — 1,558 → 0.** Ruling 3's destination table
  gave `idiv`/`div`/`mul`/one-operand `imul`/`cltd`/`cqto`/`cwtl`/`cltq`/
  `cbtw` their own rows, and this lap wrote the arithmetic for both halves
  of each (§4.1).
- **THE X87 STACK HAS NO ROWS — 1,072 → 0.** Ruling 2's `X87` block closed
  the COMPARISON pairs. The x87 ARITHMETIC behind them is now visible as a
  new cause, 400 rows.
- **AN UNCONDITIONAL TRANSFER IS NOT A FLAG READER — 325 → 0.** ledger48
  no longer makes a guard row for an unconditional transfer, so the defect
  and its census rows are both gone.
- **THE FLAGS THE SETTER LEFT — 746 → 787.** Slightly worse, and the
  reason is the honesty repair of §4.2: the flag state is now taken from
  the row ledger48 linked, so a pair whose setter has no flag model is a
  census row instead of quietly answering from an older comparison.
- **NO OPCODE WRITES THE ANSWER REGISTER — 36 → 335.** This is the `call`
  finding arriving as a census row; §3.4.
- **THE CARRY BIT OFF AN X87 COMPARISON — 0 → 186 (new).** `fucomip +
  setae` reads the carry flag; layer 4's float-comparison model carries
  the ordered/unordered bits but no carry for an x87 setter. Recorded
  reason, LITERAL: `this suffix reads the carry bit, and the flag-setting
  arch opcode 'fucomip' has no carry model in this file`.

## 3.4 THE `call` CAUSE — a census row, not a blocker

The coordinator's ruling for this task: **no destination rule for `call`
was invented.** The units are reported with their callee names and the
question is left where log 152 §9.2 left it.

LITERAL — `name_census4_printed.txt`:

```
THE ANSWER PRODUCED BY A LIBRARY CALL -- a census row, not a blocker
  units: 300
  cause: the answer is produced by a library call -- no opcode in the body
         writes OUT-0 -- awaiting the owner's ruling on `call` as a producer
      __udivti3                                77 unit(s)
      __umodti3                                77 unit(s)
      __divti3                                 73 unit(s)
      __modti3                                 73 unit(s)
```

**300 here against log 152 §5.1's 305, reconciled rather than rounded.**
Computed this session over all 30,436 ledgers:

```
OUT-0 producer is a phrase: 620
  of which the body transfers out: 305
  of which it does not: 315
```

The five that are in the 305 and not in the 300 are `go/regen_142`, `143`,
`144`, `145`, `147`. LITERAL, one of them:

```
  go/regen_142 push %rbp; mov %rsp,%rbp; test %rbx,%rbx; je L0; xor %edx,%edx;
               div %rbx; pop %rbp; ret; L0:; call x_runtime_panicdivide; nop
   OUT-0 operands: [['IN-0']]
```

GLOSS: their answer row HAS an operand and therefore has a term, and their
transfer is to a panic routine, not to a routine that computes the answer.
They are not census members. 300 is the count of units whose answer is
actually produced by a library call.

---

# 4. The rows this lap wrote, and the gate's verdict on each family

The rule the brief states: **a term that does not prove is not a row.**
This section answers it family by family, and one family fails it.

## 4.1 The destination table's halves — WRITTEN AND PROVED

The arithmetic written this lap, one entry per half the table names:

- `idiv` / `div`: the dividend is the data register and the accumulator
  concatenated, at twice the operand width; the quotient half is the
  truncating division of that by the named operand, the remainder half is
  the remainder whose sign follows the dividend.
- one-operand `mul` / `imul`: the product of the accumulator and the named
  operand at twice the width; the low half and the high half.
- `cltd` / `cqto`: the accumulator's top bit spread through the data
  register.
- `cwtl` / `cltq` / `cbtw`: the accumulator sign-extended in place.

**The values moving.** LITERAL — `acceptance53_printed.txt`, part (d),
`c/op_253` (`a % b` at 64 bits):

```
    LITERAL -- body:  mov %rdi,%rax; cqto; idiv %rsi; mov %rdx,%rax; ret
      row       produced by                          operands
      TEMP-0    mov                                  IN-0
      TEMP-1    cqto [the sign of the accumulator]   TEMP-0
      TEMP-2    idiv [quotient]                      TEMP-0,TEMP-1,IN-1
      TEMP-3    idiv [remainder]                     TEMP-0,TEMP-1,IN-1
      TEMP-4    mov                                  TEMP-3
      OUT-0     mov                                  TEMP-4
    LITERAL -- the term each row reads to:
      TEMP-0    seed_rdi
      TEMP-1    If(1 == Extract(63, 63, seed_rdi), 18446744073709551615, 0)
      TEMP-2    Extract(63, 0, Concat(TEMP-1, seed_rdi) / SignExt(64, seed_rsi))
      TEMP-3    Extract(63, 0, SRem(Concat(TEMP-1, seed_rdi), SignExt(64, seed_rsi)))
      OUT-0     Extract(63, 0, SRem(Concat(TEMP-1, seed_rdi), SignExt(64, seed_rsi)))
```

(The `TEMP-1` inside `TEMP-2` and `TEMP-3` is written out in full in the
file; it is folded here for width.)

With `a = 7` and `b = −3`: `TEMP-0 = 7`; `cqto` sees bit 63 of 7 clear, so
`TEMP-1 = 0`; the dividend is `Concat(0, 7) = 7` at 128 bits; the divisor
is `−3` sign-extended; `TEMP-2` is `−2`, `TEMP-3` is `1`; the body moves
`TEMP-3` to the answer, so `OUT-0 = 1`. That is what the machine leaves.

EVIDENCE: **410 units moved from withdrawn to proved** on the strength of
these rows — every one whose answer reads the QUOTIENT half. The
transition table in §4.4 carries that figure.

## 4.2 The flag link — WRITTEN, AND IT COSTS 699 OLD PROOFS

ledger48 types a comparison's row `flags only` and puts it FIRST in the
operand list of the next flag-reading row. This lap reads the flag state
from that row and from nowhere else.

**What that replaced.** layer4.py (canon37) carried the flags in a running
variable and only cleared it when a row was blocked. So for a body like
`cmp %rax,%rsi; sbb $0x0,%rdx; setl %al`, `sbb` left flags layer4 has no
model for, the running variable still held `cmp`'s, and the pair
`['sbb','setl']` built its answer from **the wrong comparison**. It proved
on route two because textwalk48 makes the identical substitution — two
walks sharing one error.

LITERAL — `c/regen_34943`'s hole, this lap:

```
   hole GUARD-0 {'kind': 'flag_pair', 'mnem': ['sbb', 'setl']}
        the flag-setting arch opcode 'sbb' left flags this file could not build
```

MEASURED: **699 units moved from proved to no-term** on this repair. They
are the `sbb`/`adc` flag-pair census rows of §3.1. Writing a real flag
model for `sbb`/`adc` is the work that returns them, and it is named here
as work not done.

**A correction inside this lap, recorded rather than smoothed.** A first
version of the link fell back to searching the REST of the operand list
when the linked row had no flag state. On `c/regen_36623`
(`mov %rdi,%rax; sar $0x3f,%rax; cmp %rdi,%rsi; sbb %rax,%rdx; setl %al;
movzbl %al,%eax; ret`) that fallback found the row `setl`'s own
destination operand resolved to — the SHIFT's row — and answered from a
shift's flags. Route two disproved 72 units on it. The fallback was
removed; route-two disproofs are now **0**.

## 4.3 The STACK and X87 rows — WRITTEN, LINEAGE CLOSED, BUT NOT PROVED

This is the family that fails the brief's rule, and it fails it because of
the two REFERENCES, not because of the ledger.

LITERAL — `acceptance53_printed.txt`, part (c), the x87 instance:

```
  cpp/regen_36796
    LITERAL -- body:  fldt 0x18(%rsp); fldt 0x8(%rsp); fucomip %st(1),%st;
                      fstp %st(0); seta %al; ret
      row       type                 produced by       operands
      X87-0     x87 stack value      fldt
      X87-1     x87 stack value      fldt
      TEMP-0    flags only           fucomip           X87-0,X87-1
      GUARD-0   flag-derived value   fucomip + seta    TEMP-0
      OUT-0     1-byte general value fucomip + seta    GUARD-0
    LITERAL -- the term each row reads to:
      X87-0     x87_0x18_rsp_
      X87-1     x87_0x8_rsp_
      GUARD-0   ZeroExt(56, If(And(Not(x87_0x8_rsp_ < x87_0x18_rsp_),
                                   Not(fpEQ(x87_0x8_rsp_, x87_0x18_rsp_)),
                                   Not(Or(fpIsNaN(x87_0x8_rsp_),
                                          fpIsNaN(x87_0x18_rsp_)))), 1, 0))
    route one (the ship simulation): UNDECIDED
        this body has a flag-reading arch opcode whose nearest preceding
        flag-setting arch opcode is outside the reference simulator's own
        remembered set (cmp, test, ucomisd, ucomiss) ...
    route two (the text-order walk): UNDECIDED
        the text-order walk: no z3 term is written for this arch opcode
```

GLOSS, with values. An x87 register holds the 80-bit extended form, so
each `fldt` row is a `FPSort(15, 64)` value keyed by the memory operand it
loaded. Take `0x18(%rsp) = 2.0` and `0x8(%rsp) = 3.0`.

- The first `fldt` loads `2.0` and makes `X87-0`. The x87 stack is
  `[X87-0]`, so position 0 holds `2.0`.
- The second `fldt` loads `3.0` and makes `X87-1`, pushing on top. The
  stack is `[X87-1, X87-0]`: position 0 holds `3.0`, position 1 holds
  `2.0`.
- `fucomip %st(1),%st` is AT&T order — source `%st(1)`, destination `%st`.
  It compares the top against position 1: `3.0` against `2.0`. `TEMP-0`
  records the flags and names both rows.
- `seta` asks for "above and ordered": `3.0 > 2.0` and neither side is
  NaN, so `GUARD-0` is `1` and `OUT-0` is `1`.

The lineage runs unbroken from the answer to the two loads, which is
exactly what canon37 could not do — its guard row had no operands at all.

MEASURED — `audit53_printed.txt`:

```
  STACK: units carrying such a row                        3360
  STACK: units undecided on both routes                   3360
  STACK: units with an OUT-0 term                         3056
  X87: units carrying such a row                          1405
  X87: units undecided on both routes                     1405
  X87: units with an OUT-0 term                           1163
```

**THE HONEST STATEMENT: not one of those 4,765 units is gate-proved.** Both
references refuse them by name, and the refusals are the references'
limits:

- Route one, LITERAL on `go/op_110`: `the reference simulator: mnemonic
  'je' has no symbolic model in this checker`; on the x87 units, the
  stale-flag guard quoted above.
- Route two, LITERAL on `go/op_110`: `the text-order walk: this opcode
  moves a value to or from the machine stack, and the ledger has no block
  for the machine stack: no row holds the value it wrote` — that sentence
  is `layer4.py`'s own, reused unchanged, and it is now describing the
  TEXT walk, which has no ledger at all.

So under "a term that does not prove is not a row", the STACK and X87 rows
are recorded as **built and undecided**, never as proved. Giving them a
gate needs a reference that models the machine stack and the x87 stack.
That is named here as work not done; nothing was counted as proved on
their strength.

## 4.4 The transition, unit by unit

LITERAL — `audit53_printed.txt`:

```
  task 48        task 53           units   examples
  proved         proved            22715   c/op_0, c/op_1, c/op_101
  no term        undecided          3700   go/op_110, rust/op_642, rust/op_649
  undecided      undecided          1901   c/op_212, c/op_218, c/op_222
  proved         no term             699   c/regen_34943, c/regen_35988, c/regen_36007
  no term        no term             442   c/op_100, c/op_21, c/op_22
  withdrawn      withdrawn           415   c/op_246, c/op_247, c/op_252
  withdrawn      proved              410   c/op_210, c/op_211, c/op_216
  undecided      no term             146   c/regen_30547, c/regen_30550, c/regen_31317
  undecided      proved                7   c/regen_12733, c/regen_12746, cpp/regen_12108
  withdrawn      undecided             1   cpp/regen_14397
  units in task 53 with no task-48 record: 0
```

GLOSS: the proved count's net −282 is `+410 +7 −699`. Every one of those
three groups has a named mechanism: +410 is §4.1's destination table, +7 is
the solver deciding at the margin, −699 is §4.2's flag-link repair. The
146 `undecided → no term` are units like `c/regen_30547` whose x87
ARITHMETIC (`fadds`) has no model, which is §3.3's new 400-row cause.

---

# 5. THE FINDING: the reference's remainder is the wrong remainder

## 5.1 The claim, with the counterexample

All **415** route-one disproofs read the division's REMAINDER half. Route
two disproves nothing at all.

LITERAL — `audit53_printed.txt`, computed by walking each disproved unit's
OUT-0 lineage and collecting the `written_half` fields it reaches:

```
THE ROUTE-ONE DISPROOFS, split by the ledger's own `written_half` field
  route-one disproofs in all: 415
    remainder / the sign of the accumulator               305   c/op_246, c/op_247, c/op_252
    remainder                                             110   c/op_276, c/op_277, cpp/op_276
```

## 5.2 The mechanism, in the reference's own source

LITERAL — `canon9_behaviour_check.py`, the `idiv` branch that
`canon10_behaviour_check.Sim10` inherits and `gate48.py` calls:

```
            quotient_wide = dividend / divisor_wide       # z3 SDiv
            remainder_wide = dividend % divisor_wide       # z3 SRem
```

The comment says `SRem`. It is not. LITERAL — measured this session in the
same interpreter the pipeline uses:

```
a % b      = 4294967294
SRem(a,b)  = 1
```

with `a = 7` and `b = −3` at 32 bits. `4294967294` is `−2`. z3py's `%` on a
bit-vector is **bvsmod**, whose remainder takes the sign of the DIVISOR;
x86's `idiv` leaves a remainder whose sign follows the DIVIDEND, which is
**bvsrem**. `layer4c.py` writes `z3.SRem`.

## 5.3 The counterexample the solver returns is exactly that shape

LITERAL — `acceptance53_printed.txt`, part (d), `c/op_246`
(`mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret`):

```
    route one (the ship simulation): DISPROVED
        z3 found a starting state under which the ledger-transcribed term
        and the unit's own ship body differ:
        [seed_rsi = 3388997629, seed_rdi = 872415233]
```

`3388997629` as a signed 32-bit value is negative and `872415233` is
positive — opposite signs, which is precisely where bvsmod and bvsrem
part.

## 5.4 What follows

- The 415 are reported as WITHDRAWN, because that is what the gate said
  and no verdict was overridden. They are not counted as proved.
- The ledger's term is the correct one and the reference is wrong at one
  opcode. `canon12_behaviour_check.py` already exists and its own header
  says it models `idiv`/`div`; `gate48.py` calls `canon10`, not `canon12`.
  Pointing route one at a reference whose remainder is `SRem` is the fix,
  and it is one line in a NEW gate file. It was not done here because the
  brief says reuse `gate48.py` and edit no reused file.
- This closes log 147 §13.5's open observation that "826 of 826 spell a
  division opcode" — the shape was right and the cause is now named.

---

# 6. Layer 5, and layer 3 against it

The rule is unchanged from log 147 §8.1: the proved term through z3's own
simplifier once, free symbols renamed positionally `v0, v1, …`, printed on
one line.

## 6.1 The instance the ruling is for

LITERAL — `acceptance53_printed.txt`, part (e):

```
  c/op_109
    LITERAL -- body:      lea (%rdi,%rsi,1),%rax; ret
    LITERAL -- layer 3:   mov ledger+0x00(%rip),%rdi; mov 0x0(%rdi),%rdi;
                          mov ledger+0x00(%rip),%rsi; mov 0x8(%rsi),%rsi;
                          lea (%rdi,%rsi,1),%rax; mov ledger+0x38(%rip),%r11;
                          mov %rax,0x0(%r11); ret
    LITERAL -- layer 5:   v0 + v1
  go/op_319
    LITERAL -- body:      add %rbx,%rax; ret
    LITERAL -- layer 3:   mov ledger+0x00(%rip),%rax; mov 0x0(%rax),%rax;
                          mov ledger+0x00(%rip),%rbx; mov 0x8(%rbx),%rbx;
                          add %rbx,%rax; mov ledger+0x38(%rip),%r11;
                          mov %rax,0x0(%r11); ret
    LITERAL -- layer 5:   v0 + v1

  layer 3 texts identical: False
  layer 5 texts identical: True
```

## 6.2 The counts, per population

LITERAL — `audit53_printed.txt`:

```
POPULATION: interpreter
  distinct layer-3 texts, every unit with a term         7
  distinct layer-5 texts, every unit with a term         3
  distinct layer-3 texts, proved units only              7
  distinct layer-5 texts, proved units only              3

POPULATION: original
  distinct layer-3 texts, every unit with a term       655
  distinct layer-5 texts, every unit with a term       451
  distinct layer-3 texts, proved units only            591
  distinct layer-5 texts, proved units only            421

POPULATION: regenerated
  distinct layer-3 texts, every unit with a term      2703
  distinct layer-5 texts, every unit with a term      1539
  distinct layer-3 texts, proved units only           1471
  distinct layer-5 texts, proved units only           1035
```

Against log 147 §8.3 / §13.5 (canon37, same populations): original 665
against 433, regenerated 2,810 against 1,146; proved-only 599/423 and
1,726/1,058. The collapse ratio is the same shape on a differently-shaped
population.

---

# 7. The guard, unmodified, one process

`check_no_spelling_keys.py` was not edited. Its committed copy is
`fdff0b2` of 2026-08-26 and `git status --porcelain` over it is empty;
its sha256 is `a377462b38e8610d8bb60ac668f0a5adc72ee571d15efab85e40a9afdaa511f7`.
No file this task writes declares `role: generator provenance`, and
nothing was added to any field set.

LITERAL — the command and its result:

```
$ /tmp/reconnect_venv/bin/python3 guard53.py
TASK 53: 334 paths  PASS 334  FAIL 0  exempt 0  exit 0
guard exit=0
```

LITERAL — the transcript's own head and tail (`guard53_transcript.txt`):

```
guard53.py -- every artifact task 53 writes, unmodified guard, ONE process.
No file declares the provenance role and nothing was added to any field set.
$ python3 check_no_spelling_keys.py <334 paths, one process>

operator inventory: 91 tokens read from probe_manifest_*.json
PASS layer4c_terms_c.json -- no operator token in any key, grouping, pairing or row structure
...
PASS op_units2_swift_c0010.json -- no operator token in any key, grouping, pairing or row structure

GUARD EXIT CODE = 0
```

LITERAL — the counts over that transcript, computed rather than eyeballed:

```
$ grep -c "^PASS " guard53_transcript.txt
334
$ grep -c "^FAIL"  guard53_transcript.txt
0
$ grep -c exempt   guard53_transcript.txt
0
```

GLOSS: 334 PASS, 0 FAIL, exit 0, and **0 lines say "exempt"** — every line
says the guard walked the file.

---

# 8. Zero regressions

LITERAL — `zero_regression53_printed.txt`, the verdict:

```
VERDICT
  prior artifacts touched:      0
  prior paths dirty in the vcs: 0
  units missing from task 53:   0
```

CLAIM ONE's marker is `layer4c.py`, written `2026-09-03 00:00:45`; the 26
prior artifacts checked are all older, each listed with its modification
time and the first sixteen characters of its sha256. The load-bearing ones:

```
  canon38_wrapped_c.json      2026-09-02 23:24:26  491688037fb4adda
  canon38_regen_state.json    2026-09-02 23:25:05  663576d7c1a04546
  name_census3.json           2026-09-02 21:01:33  65b5f7cfaed41398
  layer4.py                   2026-09-02 20:55:51  d0afb92cb7abde69
  gate48.py                   2026-09-02 20:42:42  22250c7258d98862
  textwalk48.py               2026-09-02 20:31:09  a6b7e130cb78fc3f
  census48b.py                2026-09-02 20:56:32  44630aa30bac6d39
  ledger48.py                 2026-09-02 23:22:50  604e7945775bccb5
  check_no_spelling_keys.py   2026-08-26 12:32:37  a377462b38e8610d
```

CLAIM TWO, LITERAL: `git status --porcelain -- <26 prior paths>` produced
no output, so every prior path matches its committed copy.

---

# 9. What canon38 disagrees with itself about — reported, not fixed

`ledger48.build_prelude` emits the VECTOR arrivals first, so `IN-0` is the
row the prelude loads into the first vector family. `ledger48.walk_dataflow`
and the `arrival_contract_bindings` canon38 records both bind `IN-i` to
`arrival_families[i]` instead. The two differ only for a unit with both
vector and general arrivals.

LITERAL — `c/op_105` (`cvtsi2ss %edi,%xmm1; addss %xmm1,%xmm0; ret`):

```
arrival_families            ['rdi', 'xmm0', 'xmm1']
prelude_resolved            ['movdqu IN-0,%xmm0', 'movdqu IN-1,%xmm1', 'mov IN-2,%rdi']
arrival_contract_bindings   IN-0 <-> %rdi,  IN-1 <-> %xmm0,  IN-2 <-> %xmm1
ledger row TEMP-0           cvtsi2ss  reads IN-0, IN-2
```

GLOSS: the prelude says `IN-0` is `%xmm0`; the bindings and the ledger's own
wiring say `IN-0` is `%rdi`. `layer4c.py` follows the WIRING, because the
wiring is what it transcribes. With the prelude's binding `c/op_105`'s
term reads the wrong register for the addition's untouched upper lanes and
route two DISPROVES it; with the wiring's binding route two PROVES it
(route one is undecided on this unit, because its reference carries the
float vocabulary as uninterpreted functions). Which of the two canon38 should change is not this task's
call; it is recorded here and in `task53_resume.md`.

---

# 10. The complete file inventory

## 10.1 Code written this task (seven files, all new; nothing reused was edited)

| file | bytes | what it is |
|---|---|---|
| `layer4c.py` | 37,679 | LAYER 4 over canon38: replays ledger48's dataflow walk to recover each row's operand slots, checks the replay against the stored ledger, reuses layer4.py's producer table, and adds the machine-stack, x87 and destination-table arithmetic. |
| `census53.py` | 9,691 | the driver: layer 4 + both gate routes + layer 5 over all three populations, chunked and resumable. |
| `name_census4.py` | 13,343 | the census builder: typed producers, no role key, plus the `call` cause with its callee names. |
| `audit53.py` | 17,396 | the figures: per population, layer 3 against layer 5, the census delta by cause, the disproof split, the added-row verdicts, the per-unit transition. |
| `acceptance53.py` | 7,136 | the five literal instances (a)-(e). |
| `zero_regression53.py` | 8,064 | the three claims of §8. |
| `guard53.py` | 5,100 | runs the UNMODIFIED guard, one process, over every task-53 artifact. |

## 10.2 Data written this task

| file | bytes | what it is |
|---|---|---|
| `layer4c_terms_c.json` | 741,577 | 610 units |
| `layer4c_terms_cpp.json` | 970,731 | 770 units |
| `layer4c_terms_go.json` | 117,650 | 107 units |
| `layer4c_terms_rust.json` | 131,805 | 125 units |
| `layer4c_terms_swift.json` | 173,528 | 167 units |
| `layer4c_interp.json` | 10,034 | 9 units |
| `layer4c_regen_store/*.json` | 36,272,799 | 326 chunks, 28,664 units |
| `layer4c_state.json` | 24,585 | the resume state: 326 of 326 chunks done |
| `name_census4.json` | 79,404 | THE CENSUS. Supersedes `name_census3.json`. |
| `guard53.json` | 303 | the guard run's counts |

## 10.3 Transcripts and logs written this task

| file | bytes | what it is |
|---|---|---|
| `guard53_transcript.txt` | 32,768 | 334 PASS, 0 FAIL, 0 exempt, exit 0 |
| `name_census4_printed.txt` | 12,348 | THE CENSUS, printed |
| `audit53_printed.txt` | 6,309 | every figure in §1, §3.3, §4.3, §4.4, §5.1, §6.2 |
| `acceptance53_printed.txt` | 11,486 | the five instances |
| `zero_regression53_printed.txt` | 2,960 | the three claims |
| `census53_run.log` | 18,834 | the run, chunk by chunk |
| `task53_resume.md` | 2,191 | the resume file, written before the work and updated during it |

## 10.4 Read, never written

`canon38_wrapped_{c,cpp,go,rust,swift}.json`, `canon38_interp.json`,
`canon38_regen_store/*.json`, `canon38_regen_state.json`, `ledger48.py`,
`layer4.py`, `gate48.py`, `textwalk48.py`, `census48b.py`,
`name_census3.py`, `layer4b_*`, `name_census3.json`, `layer5.py`,
`condition_table.py`, `canon10_behaviour_check.py`,
`check_no_spelling_keys.py`.

---

# 11. Resume state

## 11.1 Nothing is part-done

LITERAL — the last line of `census53_run.log`:

```
finished
```

`layer4c_state.json` records all 326 regenerated chunks plus the five
original languages and the interpreter as done, so re-running
`census53.py` is a no-op.

## 11.2 How to re-run, in order

1. `census53.py` — skips anything already in `layer4c_state.json`; delete
   that file and `layer4c_regen_store/` for a full redo.
2. `name_census4.py > name_census4_printed.txt`
3. `audit53.py > audit53_printed.txt`
4. `acceptance53.py > acceptance53_printed.txt`
5. `zero_regression53.py > zero_regression53_printed.txt`
6. `guard53.py` — LAST, because it walks `name_census4.json`.

All six run under `/tmp/reconnect_venv/bin/python3`. Steps 2-6 are
read-only over step 1's artifacts and are re-runnable at any time.

## 11.3 What task 54 reads

`layer4c_terms_{c,cpp,go,rust,swift}.json`, `layer4c_interp.json`,
`layer4c_regen_store/*.json`, `name_census4.json`. Each unit record
carries `term_built`, `layer5_normalized_text`, `layer3_wrapped_text`,
`gate_ship_verdict`, `gate_textorder_verdict`, `holes`, `cascades`,
`body_spells_a_call` and `callees`. The proved population for ruling 1's
three merge grounds is the 23,132 units whose record has `term_built`
true, no `DISPROVED` verdict, and at least one `PROVED_EQUAL`.

---

# 12. Decided and recorded for audit / awaiting the owner

## 12.1 Decided, recorded (no answer needed)

1. **The arrival binding follows the ledger's wiring, not the prelude's
   load order** (§9). The wiring is what layer 4 transcribes, it is what
   `arrival_contract_bindings` records, and units bound that way prove on
   both routes.
2. **An x87 value is `FPSort(15, 64)`** — the 80-bit extended form as z3
   spells it. `layer4.float_condition` is sort-generic, so the comparison
   rule is reused unchanged.
3. **A register a destination-table opcode reads without naming, and for
   which the ledger holds no row, is the machine's own starting state** —
   one symbol per family, the same rule `layer4.fill_slots` already
   applies to a NAMED operand in the same position and the same symbol the
   reference simulator seeds. This is what gives `go/op_110` its answer.
4. **`call` was NOT added to any destination table.** The 300 units are a
   census row with their callee names (§3.4), per the coordinator's ruling
   on this task.
5. **No verdict was overridden.** The 415 remainder units are reported as
   withdrawn even though §5 shows the reference is the party in error.

## 12.2 Awaiting the owner

1. **Should route one point at a reference whose remainder is `SRem`?**
   §5. `canon12_behaviour_check.py` already models the division family;
   `gate48.py` calls `canon10`. A new gate file pointing at `canon12`
   would decide the 415 without editing any reused file. Not done here
   because the brief says reuse `gate48.py`.
2. **`call` as a producer** — log 152 §9.2's question, unchanged. 300
   units, four callees (`__udivti3`, `__umodti3`, `__divti3`, `__modti3`).
3. **A gate route that models the machine stack and the x87 stack.**
   Without one, 3,360 STACK-carrying and 1,405 X87-carrying units have
   terms that no route can decide (§4.3). Neither is counted as proved.
\n\n## CORRECTION (2026-09-03, coordinator) — the "call as a producer" open call is WITHDRAWN\n\nThe 300 units whose answer comes from `call __udivti3` / `__umodti3` / `__divti3` / `__modti3` are LIBRARY ROUTINES, not compiler operations. By the standing ruling (AgentMemory line 135: layer 3 is "what the COMPILER can do to a representation — the measured dynamics, never builtins") they are OUT OF SCOPE. They should never have been posed as a question for the owner, and the phrase "library-call units" should not have been coined. Recorded as excluded in `Research/op_pipeline/out_of_scope_library_calls.json`; the next pool/proof rebuild drops them from its population. Nothing in this log's earlier text is edited.\n