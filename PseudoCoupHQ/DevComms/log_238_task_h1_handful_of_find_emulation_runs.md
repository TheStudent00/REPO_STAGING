# log 238 — task h1: a handful of `find_emulation` runs from the arch-opcode model table

Node: `hq.research.arch_unit_oracle`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`,
the "goal" section of 2026-09-07 and the ruling of 2026-09-08). The
PROGRESS entry is on the autopoly sub-node
(`.../node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/PROGRESS.md`),
beside tasks o12 and o13.

Date: 2026-09-09. Instance `h1`, on the TOWER, brought down at the end
of this log. Artifact folder:
[`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/`](file://PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/).
The deliverables are
[`handful.py`](file://PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py)
(the driver; it wires the existing pieces and adds nothing project-new),
[`handful.json`](file://PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.json)
(the twenty runs, every intermediate object on the record) and
[`handful.md`](file://PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.md)
(one section per run, then the twenty-row table, then what did not work
by cause). This log carries the conclusion and points into them.

Every rendering here is labelled per the protocol's
`object.literal-gloss-analogy`: **LITERAL** is the object itself,
quoted; **GLOSS** is a plain-words reading beside a literal. No gloss
appears without its literal.

Paths inside a pasted command are the ones the lane sees:
`PseudoCoupHQ` IS `PRIVATE/PseudoCoupHQ`, mounted into
the instance. Prose names host paths. **The lane logs are on the
TOWER** (`<user>@<tower>`), under
`<runs>/h1/agent/logs/`, and every attribution
below names one of them.

| lane | what it did | log, on the tower |
|---|---|---|
| `h1_l1_cells.sh` | the ten cells pulled out of the 73 MB `model_table.json` into a ten-row `handful_cells.json`; peak RSS printed | `20260909T042405Z__h1_l1_cells.sh.log` |
| `h1_l2_probe.sh` | step 1 alone: the z3 term of every place each cell writes, before anything acted on it | `20260909T043103Z__h1_l2_probe.sh.log` |
| `h1_l3_run.sh` | the twenty runs, first pass | `20260909T043217Z__h1_l3_run.sh.log` |
| `h1_l4_report.sh` | the report, first pass, and the spelling guard | `20260909T043305Z__h1_l4_report.sh.log` |
| `h1_l5_recheck.sh` | the four UNDECIDED gate calls re-posed at 300,000 ms | `20260909T043459Z__h1_l5_recheck.sh.log` |
| `h1_l6_run_recheck_report.sh` | run, re-pose and report again in ONE lane, so `handful.json` is written end to end by one version of the program (`landing_of` had gained two fields; §7) — THIS IS THE RUN OF RECORD | `20260909T045655Z__h1_l6_run_recheck_report.sh.log` |
| `h1_l7_evidence.sh` | a first evidence pass, SUPERSEDED: two of its `sed` addresses spell the table's `|` literally, and the verifier splits a pasted command on `|` to check each stage's head, so it scored those two claims REFUSED (`head_not_on_the_read_only_allowlist -- \`) | `20260909T051913Z__h1_l7_evidence.sh.log` |
| `h1_l8_verify.sh` | a first verifier pass over this log: 0 MATCHES lost, but 1 DIFFERS and 2 REFUSED, which is what produced the two fixes above | `20260909T052351Z__h1_l8_verify.sh.log` |
| `h1_l10_verify2.sh` | the verifier again, over this log as it stands apart from the ADDENDUM below | `20260909T052606Z__h1_l10_verify2.sh.log` |
| `h1_l9_evidence2.sh` | EVERY transcript this log pastes, plus the guard and `grep -c exempt`, with both fixes: the `sed` anchors spell `.` where the table's `|` sits, and `handful.py` is named by its full path so the command runs from any working directory | `20260909T052457Z__h1_l9_evidence2.sh.log` |

Every lane script is kept in the repo at
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h1/`
and was submitted from there.

---

# 1. What the objects are

- **a cell** — one (`mnem`, operand shape, `key_width`) row of the
  arch-opcode model table
  (`PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json`,
  tasks m1/m1b, log 236 and log 237), which holds, per PLACE the opcode
  writes, the z3 term the reference simulator's own builder puts there.
  The triple is the key the ruling of 2026-09-08 states is machine form.
- **a place** — one thing an opcode writes: a register (`reg_rdi`,
  `reg_rax`, `reg_rdx`, `reg_xmm0`) or the flags. A cell writes one,
  two or three of them, and the table carries a term for each.
- **a run** — `find_emulation(cell, lang)`: the cell's term written in
  the target language's own operators by the EXISTING renderer
  (`emulate.Renderer` for c, `rust_render.RustRenderer` for rust,
  neither modified), compiled at that corpus's own ship flags, carved
  with the pipeline's objdump reader, and put back to z3 against the
  cell's own term.
- **what is different from task o8** — task o8 (log 220) ran this on
  SINGLETON UNITS, so the gate had the unit's own body as the other
  side. A cell of the table has no unit behind it: it is a mapping and
  nothing else. So the other side of the gate call here is THE CELL'S
  OWN TERM, and the question is whether the body the compiler emitted
  answers as the table says the opcode does.
- **the landing question** — task o8's Q0, unchanged: chaff-strip the
  carved body by task o2's own narrow rule
  (`single_opcode_units.strip_chaff`, imported), and if exactly one
  arch opcode remains and it is the cell's own `mnem`, LANDED; one but
  a different one, LANDED_ELSEWHERE; anything else, NOT_COLLAPSED.

---

# 2. What was done and what came back

the owner asked for this on 2026-09-09, quoted in the brief: "id like to see
how a handful of `find_emulation` runs go. like literally just a
handful. i dont want to try for long runs and find out somethings
broken or it cant find any."

Ten cells were named in the brief and all ten are in the table at
exactly the key asked for, so no substitution was needed. Each was run
against c and against rust, twenty runs, and every run's four
objects — the cell's term per place, the rendered source, the compiled
and carved body, and the gate's verdict — is in `handful.md` in full.

Sixteen of the twenty runs got as far as a compiled body. The four that
did not are the two float cells, `addss` and `cvtsi2sd`, and they were
refused for one cause in both targets: the table's term for a vector
place keeps the WHOLE 128-bit register, joining the computed lane back
onto the bits above it, and neither renderer has a holder for a vector
arrival read above its low 64 bits. That refusal is the existing
renderer's own, by its own cause word, and this task did not extend the
renderers to get around it.

Of the twenty-four places that compiled, six landed on exactly the
cell's own arch opcode, six landed on a different one, and twelve left
more than one behind. The six that landed elsewhere are all the same
substitution task o8 and task o11 already found: clang and rustc both
answer a two-register sum and a subtract-a-constant with `lea`, the
address instruction, rather than `add` or `sub`. The twelve that did not
collapse split into three causes, none of them a failure to find the
opcode: four are the flags place, which in this reference is not an
operation at all but the pair of values the setter compared; four are
the two flag consumers, whose emulation is a PAIR by construction
(the comparison and then the select) so one opcode was never possible;
and four are `idiv`, whose 51 remaining opcodes are the term's own
32-copy spelling of a sign extension, with `cqto; idiv` at the end of
them.

The proofs are the strong part. Eighteen of the twenty-four places were
proved equal to the cell's own term for every input at the gate's 3,000
ms ceiling, and two more once narrow arguments are taken to arrive
already widened to the register — c's and rust's own caller-extension
rule, the same re-pose task o7 uses. The remaining four are `idiv`'s
two places in each target, and they are UNDECIDED, not disproved: the
solver did not answer inside 3,000 ms, and re-posed with a hundred
times the room (300,000 ms) it still did not answer. That is reported
as a limit, not as a verdict.

One thing came out that nobody asked for and is worth naming: **the two
targets emitted the same machine code, byte for byte, in every one of
the twelve places both compiled.** clang at `-O1` and rustc at
`opt-level=1` were handed two very differently spelled sources — rust's
is written with `wrapping_add`, `wrapping_shr` and an unreachable hint
around its divide — and produced identical bodies for all twelve.

---

# 3. The population: the ten cells, and the one row chosen for each

**LITERAL**, block `[1/2]` of
`<runs>/h1/agent/logs/20260909T042405Z__h1_l1_cells.sh.log`
(the lane that read `model_table.json`), the count line and the ten
cells' own row counts:

> `rows in the table: 71778`
> `CELL add gpr_gpr 32: 1 row(s) at this key, 1 TRANSLATED`
> `CELL sub imm_gpr 64: 1 row(s) at this key, 1 TRANSLATED`
> `CELL imul gpr_gpr 32: 1 row(s) at this key, 1 TRANSLATED`
> `CELL sar cl_gpr 32: 1 row(s) at this key, 1 TRANSLATED`
> `CELL shr cl_gpr 64: 1 row(s) at this key, 1 TRANSLATED`
> `CELL idiv gpr_one 32: 1 row(s) at this key, 1 TRANSLATED`
> `CELL cmovne gpr_gpr 32: 15 row(s) at this key, 11 TRANSLATED`
> `CELL setne gpr_one 8: 15 row(s) at this key, 11 TRANSLATED`
> `CELL addss xmm_xmm 32: 4 row(s) at this key, 4 TRANSLATED`
> `CELL cvtsi2sd gpr_xmm 64: 4 row(s) at this key, 4 TRANSLATED`

**GLOSS.** All ten are present at exactly the key the brief names, so
the brief's fallback ("take the nearest attested cell of the same
mnemonic and say which") was never used. Four cells carry more than one
sweep row, for two mechanical reasons the table itself states, and
`handful.chosen_row` picks one by two rules, both machine form and both
printed on every run's own section of `handful.md`:

- **A vector or convert cell carries one row per sweep WIDTH.** The
  sweep walks widths 8, 16, 32 and 64, and `key_width` is the
  operation's own lane width (log 237 §7), so `addss xmm_xmm` has four
  rows all keyed 32 and `cvtsi2sd gpr_xmm` four all keyed 64. The rule:
  take the row whose own `width` equals the cell's `key_width` —
  `r00332` (`addss %xmm1,%xmm0`) and `r02658` (`cvtsi2sd %rdi,%xmm0`).
- **A flag-reading cell carries one row per flag-SETTING mnemonic the
  sweep saw.** The rule: take the row whose arriving flag state was
  written by the setter the cell's OWN attestation records the most
  ledger rows for. For `cmovne gpr_gpr 32` the attestation names one
  setter, `test` (2 ledger rows), giving `r27756`. For `setne gpr_one
  8` it names eight, and `test` is the largest at 5,691 of 10,335,
  giving `r64972`.

The corpus's attestation of the ten, from the same lane: `add` 11
units, `sub` 0, `imul` 266, `sar` 335, `shr` 251, `idiv` 389,
`cmovne` 2, `setne` 6,691, `addss` 198, `cvtsi2sd` 860.

---

# 4. The conventions this task had to state, and where each is shown

The brief asks for these by name: "If the walk over the carved body
needs arrival/answer facts the body has no unit to supply, state the
convention you used (the renderer's parameter order, the target's
calling convention) and show it."

## 4.1 The parameter order, and how the two sides are aligned

A cell's term reads `seed_<register family>` symbols — the registers
the sweep's own operand spelling names. The rendered function's
parameters arrive in the registers the C calling rule gives them
(`emulate.expected_c_families`: general in rdi, rsi, rdx, rcx, r8, r9;
float in xmm0 upwards, in declaration order; rust's `extern "C"` is the
same rule, measured in task o11, log 226 §3.1). Those two lists are
different registers, so the two sides are aligned BY ROW INDEX, exactly
as `pool100_entry_equivalence.align_by_row` aligns any two units: the
cell's i-th family and the body's i-th family both become `IN_i`.

The convention is the ORDER of the cell's list: the layer-5 print order
of the term's free symbols — so `v0` is the first — with general
registers before vector ones, because the calling rule fills them in
that order and position i must be the same KIND on both sides.

**LITERAL**, `handful.md` §1.13, the alignment table of `cmovne
gpr_gpr 32 -> c`:

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdx | rdi |
| IN-1 | rcx | rsi |
| IN-2 | rsi | rdx |
| IN-3 | rdi | rcx |

**GLOSS.** Four values arrive. The cell's term reads them as rdx, rcx,
rsi, rdi (that is the order `v0`..`v3` appear in its printed text); the
compiled function reads them as rdi, rsi, rdx, rcx (that is the C
calling rule). `IN-0` is the same value on both sides — the first of
the two the setter compared — and so on down.

## 4.2 The flags place has no register home

Five of the ten cells write the flags, and the flags are not a register
the calling rule can answer in. THE CONVENTION: the rendered function
answers the flags place in the answer register the calling rule already
uses, and its return type is the term's own width. It is stated on
every such place in `handful.json` (`home.source`) and is why the
`sub imm_gpr 64` flags place returns 128 bits — the flag model there is
the pair of two 64-bit values.

## 4.3 A flag CONSUMER is rendered as a PAIR, one function

`cmovne` and `setne` compute a function OF THE FLAGS, so the sweep hands
their builder a state whose flags are (the setter's `mnem`,
`seed_FLAG_L`, `seed_FLAG_R`). Those two symbols are not registers and
nothing arrives in them. THE CONVENTION, which is the brief's own
instruction ("render the PAIR as one function: the comparison then the
select"): re-run the SETTER's own row, take the two values its builder
leaves in the flag state, and substitute them for the consumer's two
flag arrivals. The setter's own arrivals are moved onto argument
registers the consumer does not read, because in any real body the two
values compared and the two selected between are four different values.

**LITERAL**, `handful.md` §1.13, the composition for `cmovne gpr_gpr
32` (`test` is the setter, its own row is `r14507`, `test %esi,%edi`):

```
seed_FLAG_L := Extract(31, 0, seed_rdx) & Extract(31, 0, seed_rcx) ; seed_FLAG_R := 0
```

**GLOSS.** The consumer reads rdi and rsi, so the setter's two values
were moved to rdx and rcx — the next two argument registers the
consumer leaves free. The composed function takes four inputs: the two
compared, and the two selected between.

## 4.4 The flags place of a preseeded row is NOT rendered, and why

On a flag-reading row the table also carries a `flags` place, and its
term is character-for-character the flag state that ARRIVED. That is
not a place the opcode writes; the sweep records it because the state
still holds it after the line ran. Those four places are recorded as
not rendered, with that cause, rather than rendered as if the opcode
had written them.

---

# 5. The twenty runs, one row each

**LITERAL**, block `[1/6]` of
`<runs>/h1/agent/logs/20260909T052457Z__h1_l9_evidence2.sh.log`:

```
$ sed -n \\%\^.\ cell\ .\ lang%\,\\%\^\$%p PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.md
| cell | lang | rendered (GLOSS) | landed | gate | cause if refused |
|---|---|---|---|---|---|
| `add` gpr_gpr 32 | c | `((((UINT32_C(0x0)) << 32) \| (((a) + (b)))))` | LANDED_ELSEWHERE on `lea` | PROVED_ON_SHIP |  |
| `add` gpr_gpr 32 | rust | `(((((((0x0u32)) << 32) \| ((((((((a)))).wrapping_add((((b))))))))))))` | LANDED_ELSEWHERE on `lea` | PROVED_ON_SHIP |  |
| `sub` imm_gpr 64 | c | `(((a) + (UINT64_C(0xfffffffffffffffd))))` | LANDED_ELSEWHERE on `lea` | PROVED_ON_SHIP |  |
| `sub` imm_gpr 64 | rust | `((((((((a)))).wrapping_add(((0xfffffffffffffffdu64)))))))` | LANDED_ELSEWHERE on `lea` | PROVED_ON_SHIP |  |
| `imul` gpr_gpr 32 | c | `((((UINT32_C(0x0)) << 32) \| (((a) * (b)))))` | LANDED | PROVED_ON_SHIP |  |
| `imul` gpr_gpr 32 | rust | `(((((((0x0u32)) << 32) \| ((((((((a)))).wrapping_mul((((b))))))))))))` | LANDED | PROVED_ON_SHIP |  |
| `sar` cl_gpr 32 | c | `((((UINT32_C(0x0)) << 32) \| (((a) >> (unsigned)((((UINT32_C(0x0)) << 5) \| (((b >> 0) & UINT32_C(0x1f)))))))))` | LANDED | PROVED_ON_SHIP |  |
| `sar` cl_gpr 32 | rust | `(((((((0x0u32)) << 32) \| ((((((((a)))).wrapping_shr(((((((((0x0u32)) << 5) \| (((((((b)) >> 0)) & 0x1fu32)))))))))))))))))` | LANDED | PROVED_ON_SHIP |  |
| `shr` cl_gpr 64 | c | `(((a) >> (unsigned)((((UINT64_C(0x0)) << 6) \| (((b >> 0) & UINT32_C(0x3f)))))))` | LANDED | PROVED_ON_SHIP |  |
| `shr` cl_gpr 64 | rust | `(((((((a))).wrapping_shr(((((((((0x0u64)) << 6) \| (((((((b)) >> 0)) & 0x3fu32)))))))))))))` | LANDED | PROVED_ON_SHIP |  |
| `idiv` gpr_one 32 | c | `((((UINT32_C(0x0)) << 32) \| (((((((((a) << 32) \| (b)))) / (((((((c >> 31) & UINT32_C(0x1))) << 63) \| ((((c >> 31) & UINT32_C(0x1))) << 62) \| ((((c >> 31)...` | NOT_COLLAPSED (51) | UNDECIDED, UNDECIDED at 300000 ms |  |
| `idiv` gpr_one 32 | rust | `(((((((0x0u32)) << 32) \| ((((((((({ let n1: i64 = ((((((((((a))) << 32) \| (((b))))))))); let d1: i64 = ((((((((((((((c)) >> 31)) & 0x1u32))) << 63) \| ((((...` | NOT_COLLAPSED (51) | UNDECIDED, UNDECIDED at 300000 ms |  |
| `cmovne` gpr_gpr 32 | c | `((((UINT32_C(0x0)) << 32) \| ((((((~((((~(b))) \| ((~(a))))))) == (UINT32_C(0x0)))) ? (d) : (c)))))` | NOT_COLLAPSED (2) | PROVED_ON_SHIP |  |
| `cmovne` gpr_gpr 32 | rust | `(((((((0x0u32)) << 32) \| (((if ((((((!((((((((!(((b))))))) \| ((((!(((a))))))))))))))) == ((0x0u32)))) { (((d))) } else { (((c))) })))))))` | NOT_COLLAPSED (2) | PROVED_ON_SHIP |  |
| `setne` gpr_one 8 | c | `((((UINT64_C(0x0)) << 8) \| (((((((~((((((~(a)) & UINT32_C(0xff))) \| (((~(b)) & UINT32_C(0xff)))) & UINT32_C(0xff)))) & UINT32_C(0xff))) == (UINT32_C(0x0)))...` | NOT_COLLAPSED (3) | DISPROVED, PROVED_ON_SHIP under caller extension |  |
| `setne` gpr_one 8 | rust | `(((((((0x0u64)) << 8) \| (((if (((((((!((((((((((!(((a))))) & 0xffu32))) \| (((((!(((b))))) & 0xffu32))))) & 0xffu32))))) & 0xffu32))) == ((0x0u32)))) { ((0x...` | NOT_COLLAPSED (3) | DISPROVED, PROVED_ON_SHIP under caller extension |  |
| `addss` xmm_xmm 32 | c |  |  |  | vector arrival used beyond its low lane: xmm0 read above bit 63 |
| `addss` xmm_xmm 32 | rust |  |  |  | vector arrival used beyond its low lane: xmm0 read above bit 63 |
| `cvtsi2sd` gpr_xmm 64 | c |  |  |  | vector arrival used beyond its low lane: xmm0 read above bit 63 |
| `cvtsi2sd` gpr_xmm 64 | rust |  |  |  | vector arrival used beyond its low lane: xmm0 read above bit 63 |
```

**GLOSS.** The `rendered` column is the DESTINATION place's rendered
expression on one line with the casts stripped for reading, and is
marked GLOSS in the report's own caption; the LITERAL source of every
place sits in that run's section of `handful.md`. `landed` and `gate`
are the destination place's; a cell that writes a second place carries
its own verdicts in its section. Two runs of one cell always agree on
the landing and on the verdict — the row is the same for c and rust in
all ten cells.

---

# 6. Three instances, with the values in motion

## 6.1 LANDED: `imul` gpr_gpr 32, to c

The cell's term for the destination place, **LITERAL** (`handful.md`
§1.5):

```
Concat(0, Extract(31, 0, v0)*Extract(31, 0, v1))
```

The rendered source, **LITERAL**
([`src/imul_gpr_gpr_32__reg_rdi__c.c`](file://PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/src/imul_gpr_gpr_32__reg_rdi__c.c)):

```c
uint64_t
emu_imul_gpr_gpr_32__reg_rdi__c(uint32_t a, uint32_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)((uint32_t)((uint32_t)a) * (uint32_t)((uint32_t)b)))));
}
```

The carved body and the chaff-stripped body, **LITERAL**:

| what | text |
|---|---|
| the object's body | `mov %edi,%eax; imul %esi,%eax; ret` |
| chaff-stripped, narrow rule | `imul %esi,%eax` |

Verdicts: landing `LANDED`; gate `PROVED_ON_SHIP`.

**GLOSS.** The term says: take the low 32 bits of each arrival,
multiply them, and put the 32-bit answer in the low half of a 64-bit
place with zeros above. clang wrote one `imul` and one register move,
and the move is chaff by task o2's own rule, so what remains is exactly
the cell's own arch opcode. rust's source is spelled with
`wrapping_mul` and rustc emitted the same two instructions.

## 6.2 LANDED_ELSEWHERE: `add` gpr_gpr 32, to c and to rust

The two bodies, **LITERAL** (`handful.md` §1.1 and §1.2):

| side | body |
|---|---|
| the c emulation | `lea (%rdi,%rsi,1),%eax; ret` |
| the rust emulation | `lea (%rdi,%rsi,1),%eax; ret` |

Verdicts: landing `LANDED_ELSEWHERE` (landed on `lea`); gate
`PROVED_ON_SHIP`.

**GLOSS.** Both compilers answered a two-register 32-bit sum with the
address instruction rather than `add`. This is the same substitution
task o8 found for clang (log 220 §6.2) and task o11 found for rustc
(log 226 §10), now seen from the model table's side rather than from a
unit's: `lea` writes a third register and needs no move first, while
`add` writes one of its own operands. The gate proves the body computes
the cell's mapping; it is the OPCODE that differs, not the answer.

## 6.3 The gate's counterexample, and the re-pose: `setne` gpr_one 8, to c

The composed term for the destination place, **LITERAL** (`handful.md`
§1.15) — this is the pair, `test` then `setne`, as one function:

```
Concat(0, If(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)) == 0, 0, 1))
```

The carved body, **LITERAL**: `xor %eax,%eax; test %edi,%esi; setne %al; ret`

The first pose, **LITERAL**: `DISPROVED`, counterexample
`[IN_1 = 3841776640, IN_0 = 3841776640]`.

The re-pose, **LITERAL**: `PROVED_ON_SHIP` — "z3 proved the two equal
for every input whose narrow arguments are zero-extended to the
register".

**GLOSS**, the values in motion. The emulation's parameters are
`uint8_t`, so eight bits arrive and the callee reads the whole 32-bit
register `%edi`, taking the caller to have widened them — the C
calling rule, which rust's `extern "C"` follows too (measured in task
o11, log 226 §3.1, `wide_arrival_u8`). `3841776640` is `0xE4FF0000`: its
low eight bits are zero, so the cell's term computes `~(~0 | ~0) == 0`
→ answers 0, while the compiled body's `test %edi,%esi` looks at all
32 bits, finds `0xE4FF0000 & 0xE4FF0000` non-zero, and answers 1. That
input cannot arrive in a `uint8_t` argument under either language's own
calling rule; re-posed with the narrow rows zero-extended from their
holder width, the two agree everywhere. This is the same
caller-extension rescue task o7 uses and task o8 needed once (log 220
§3c).

---

# 7. The tally, and the two targets' bytes

**LITERAL**, block `[3/6]` of
`<runs>/h1/agent/logs/20260909T052457Z__h1_l9_evidence2.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py tally
add gpr_gpr 32               flags      SAME BYTES
add gpr_gpr 32               reg_rdi    SAME BYTES
cmovne gpr_gpr 32            reg_rdi    SAME BYTES
idiv gpr_one 32              reg_rax    SAME BYTES
idiv gpr_one 32              reg_rdx    SAME BYTES
imul gpr_gpr 32              flags      SAME BYTES
imul gpr_gpr 32              reg_rdi    SAME BYTES
sar cl_gpr 32                reg_rdi    SAME BYTES
setne gpr_one 8              reg_rdi    SAME BYTES
shr cl_gpr 64                reg_rdi    SAME BYTES
sub imm_gpr 64               flags      SAME BYTES
sub imm_gpr 64               reg_rdi    SAME BYTES
compiled places both targets have a body for: 12
   the two targets emitted the same bytes: 12
   the two targets emitted different bytes: 0

runs                             20
runs refused before any compile  4
places compiled and carved       24
LANDED                           6
LANDED_ELSEWHERE                 6
NOT_COLLAPSED                    12
PROVED_ON_SHIP                   18
proved under caller extension    2
neither                          4
```

**GLOSS.** Twenty runs; 4 refused before any compile (the two float
cells in both targets); 24 places compiled and carved (16 runs, some
writing two places). The landing splits 6 / 6 / 12 and the gate 18 + 2
proved, 4 neither — those 4 are `idiv`'s two places in each target, all
UNDECIDED. The byte comparison is per (cell, place): both targets have
a body for 12 of them and in all 12 the bytes are identical, so nothing
here distinguishes clang's lowering from rustc's on these sources.

`handful.py tally` is the same walk over `handful.json` the report's
prose rests on; run it from the artifact folder.

## 7.1 Why the run of record is lane `h1_l6` and not `h1_l3`

Lanes `h1_l3` and `h1_l5` ran the same two commands and their logs
stand. Between them and `h1_l6`, `handful.landing_of` gained two
fields — the arch opcodes that remain after the chaff strip, and
whether the cell's own opcode is among them — so that §3.2 of
`handful.md` can key its causes on a fact rather than on a reading.
Nothing about what is measured changed: the same ten cells, the same
two renderers, the same ship flags, the same gate, and `h1_l6` re-ran
the whole thing end to end so `handful.json` is one version's output.
The two runs agree on every verdict.

---

# 8. What did not work, by cause

**LITERAL**, block `[2/6]` of the same lane log:

```
$ sed -n \\%\^##\ 3\\.%\,\$p PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.md
## 3. What did not work, by cause

### 3.1 Refusals and gate calls that did not prove

- `the flags place of a preseeded row is the flag state that ARRIVED, not a place this opcode writes`: 4 -- cmovne gpr_gpr 32/c [flags], cmovne gpr_gpr 32/rust [flags], setne gpr_one 8/c [flags], setne gpr_one 8/rust [flags]
- `the gate answered UNDECIDED at 3,000 ms and again at 300000 ms`: 4 -- idiv gpr_one 32/c [reg_rax], idiv gpr_one 32/c [reg_rdx], idiv gpr_one 32/rust [reg_rax], idiv gpr_one 32/rust [reg_rdx]
- `vector arrival used beyond its low lane`: 4 -- addss xmm_xmm 32/c [reg_xmm0], addss xmm_xmm 32/rust [reg_xmm0], cvtsi2sd gpr_xmm 64/c [reg_xmm0], cvtsi2sd gpr_xmm 64/rust [reg_xmm0]

### 3.2 The landings that were not LANDED, by cause

- the cell's own arch opcode IS among the ones that remain; what sits beside it is what the term carries beyond the operation (51 remain): 4 -- idiv gpr_one 32/c [reg_rax], idiv gpr_one 32/c [reg_rdx], idiv gpr_one 32/rust [reg_rax], idiv gpr_one 32/rust [reg_rdx]
- the compiler chose another arch opcode for the same computation (`lea`): 4 -- add gpr_gpr 32/c [reg_rdi], add gpr_gpr 32/rust [reg_rdi], sub imm_gpr 64/c [reg_rdi], sub imm_gpr 64/rust [reg_rdi]
- the compiler chose another arch opcode for the same computation (`mov`): 2 -- sub imm_gpr 64/c [flags], sub imm_gpr 64/rust [flags]
- the emulation is a PAIR by construction (the setter's comparison, then the select), so more than one arch opcode was never possible (2 remain): 2 -- cmovne gpr_gpr 32/c [reg_rdi], cmovne gpr_gpr 32/rust [reg_rdi]
- the emulation is a PAIR by construction (the setter's comparison, then the select), so more than one arch opcode was never possible (3 remain): 2 -- setne gpr_one 8/c [reg_rdi], setne gpr_one 8/rust [reg_rdi]
- the flags place is the reference's flag model -- the two values the setter compared, repacked -- so it is not one operation and no single arch opcode is its landing (2 remain): 4 -- add gpr_gpr 32/c [flags], add gpr_gpr 32/rust [flags], imul gpr_gpr 32/c [flags], imul gpr_gpr 32/rust [flags]
```

**GLOSS**, one paragraph per cause, each with its status.

- **The vector place keeps the whole register**, 4 of 20 runs, status
  CLOSED as a refusal. The table's term for `addss xmm_xmm 32` is
  `Concat(Extract(127, 32, v0), fp.to_ieee_bv(fpToFP(Extract(31, 0,
  v0)) + fpToFP(Extract(31, 0, v1))))` — the 32-bit lane the
  instruction computes, joined back under the 96 bits it leaves alone.
  Both renderers plan an arrival's width from how the term reads it,
  and refuse a vector arrival read above bit 63 with their own cause
  word `emulate.CAUSE_LANE`. This is not a hole in the renderers'
  operator coverage: the float operators (`fpToFP`, `fp.to_ieee_bv`,
  float addition) are all covered, and the refusal is about the PLACE,
  not the operation. Extending the renderer to hold a 128-bit vector
  arrival was outside this task's own instruction ("Do not extend the
  renderers in this task beyond the arity/naming glue a cell needs").
- **The solver did not answer for `idiv`**, 4 of 24 places, status
  OPEN and reported as a limit. The term is a signed 64-by-64 divide
  whose divisor is a sign extension written as 32 separate copies of
  bit 31, and the body clang and rustc emit for it is 51 arch opcodes
  of shifts and ors ending in `cqto; idiv`. Re-posed at 300,000 ms —
  the law's rule that a time limit is a flag, not a verdict — the
  answer did not change; both remain UNDECIDED, never DISPROVED.
- **The flags place of a flag-reading row is a pass-through**, 4 of 24
  places, status CLOSED. Named in §4.4; it is recorded rather than
  rendered.
- **The landing question does not apply to the flags place**, 4
  sightings, status CLOSED. In this reference the flag state IS the
  pair of values the setter compared, so the flags term is a repacking
  of two arrivals and no single arch opcode could be its landing. The
  `sub` flags place is the extreme case: its term is `Concat(v0, 3)`,
  128 bits, and the body is `mov $0x3,%eax; mov %rdi,%rdx; ret` — the
  two halves of a 128-bit answer, so the landing reads `mov`.
- **A composed pair is two operations**, 4 sightings, status CLOSED by
  construction. `cmovne`'s emulation compiled to `test %edi,%esi;
  cmove %ecx,%eax` and `setne`'s to `xor %eax,%eax; test %edi,%esi;
  setne %al`. The interesting half is that the pair landed AS a pair:
  `test` with a conditional select or set beside it, which is the
  shape the ledger's own flag-pair rows record. `cmove` rather than
  `cmovne` is the same computation with the branches the other way
  round, and the gate proved it.

## 8.1 One caveat that is not a refusal: the gate cuts to the narrower width

`gate.Gate.decide` cuts both terms to the narrower of the two, which is
its own stated rule. A cell's destination place is the whole 64-bit
register, while the answer home read off the carved body is often the
32-bit or 8-bit register the compiler actually wrote — so a proof can
cover the low half of the place rather than all of it. Every such run
carries the two widths and a sentence naming the cut in `handful.json`
(`check.width_note`) and in its section of `handful.md`. This is the
shared machinery's own rule and was not changed; it is flagged in §11.

---

# 9. Bounds and memory

The stated bound: ONE collecting process, no forked workers, peak
resident checked after every run, named abort `ABORT_MEMORY_H1` at
4 GB (4,194,304 kB). The heavy read was sampled first, as the law
requires: lane `h1_l1` parsed the 73 MB `model_table.json` and printed
its peak before anything else ran.

**LITERAL**, block `[4/6]` of
`<runs>/h1/agent/logs/20260909T052457Z__h1_l9_evidence2.sh.log`:

```
$ sed -n \\%\^.\ memory\ bound%\,\\%\^\$%p PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.md
| memory bound | 4194304 kB, named abort ABORT_MEMORY_H1 |
| peak resident | 405812 kB |
```

**GLOSS.** 405,812 kB is 9.7% of the bound; the abort never fired and
the bound was never raised. The other peaks, from the lanes' own
printed lines: `h1_l1` 290,040 kB parsing the model table; `h1_l2`
69,544 kB for step 1 alone; the re-pose at 300,000 ms 337,156 kB. The
run of record took 1,216.0 s wall clock, of which about 1,200 s is the
four `idiv` obligations sitting at their new ceiling.

---

# 10. The guard, and `grep -c exempt`

**LITERAL**, blocks `[5/6]` and `[6/6]` of the same lane log:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful_cells.json PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS handful_cells.json -- no operator token in any key, grouping, pairing or row structure
PASS handful.json -- no operator token in any key, grouping, pairing or row structure
```

```
$ grep -c exempt PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.md PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h1/h1_l1_cells.sh PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h1/h1_l2_probe.sh PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h1/h1_l3_run.sh PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h1/h1_l4_report.sh PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h1/h1_l5_recheck.sh PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h1/h1_l6_run_recheck_report.sh
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.md:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h1/h1_l1_cells.sh:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h1/h1_l2_probe.sh:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h1/h1_l3_run.sh:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h1/h1_l4_report.sh:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h1/h1_l5_recheck.sh:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h1/h1_l6_run_recheck_report.sh:0
```

**GLOSS.** Both json files PASS the unmodified guard on their first
run: no field was renamed to dodge it and no exemption was claimed
anywhere. The field carrying a mnemonic is `mnem` throughout, and a
landed mnemonic sits at `landed.mnem`, which is task o11's own
resolution (log 226 §11) rather than anything new. Zero `exempt` in
every file this task added; the two evidence lanes
(`h1_l7_evidence.sh`, `h1_l9_evidence2.sh`) and the two verifier lanes
are not in the list because the word appears in the command those lanes
run, which is task o8's and o11's own precedent for that lane.

## 10.1 What was reused, and what was written

`emulate.py` and `rust_render.py` were IMPORTED, not forked:
`Renderer`, `RustRenderer`, `compile_and_carve` (both), `recorded_facts`
(both), `expected_c_families`, `body_answer`, `sanitize`, `Refused` and
its cause words, `GENERAL_ORDER`, `PARAM_NAMES`, `SHIP_FLAGS_SOURCE`
(both). `model_table.places_of_attempt` rebuilds each row's z3 terms.
`single_opcode_units.strip_chaff` / `parse_insn` are task o2's chaff
rule. `term97_walk.build`, `canonical_form.render_one`,
`reference.answer_for_unit`, `pool100_entry_equivalence` and
`gate.Gate.decide` are the pipeline's own. Nothing under
`Research/op_pipeline/` or `Research/oracle/arch_opcodes/` was edited.

ONE THING WAS RESTATED RATHER THAN CALLED, said out loud because the
law forbids silent substitution: `emulate.prove_against_x` is the
o7/o8/o11 proof step and it takes an X UNIT — a canon40 record whose
body is the other side of the comparison. This task's other side is a
table cell, which has no body and no record, so that function cannot be
handed the arguments it names. `handful.check_one_place` poses the same
obligation through the same objects (`input_rows` / `align_by_row` /
`classify_symbols` / `rename_constants_apart`, then `gate.Gate.decide`)
and re-poses a DISPROVED verdict under the same caller-extension
substitution. The reason is in `handful.py`'s own docstring.

---

# 11. Flag for the coordinator

- **The gate's width cut, §8.1.** A cell's place is the whole register;
  the answer home read off a carved body is the register the compiler
  wrote, which is often narrower. `gate.Gate.decide` cuts both to the
  narrower and proves over that. Every affected run says so on its own
  record. Whether the check should instead widen the body's answer to
  the place's width — a change in `Research/op_pipeline/`, which this
  brief forbids — is not this task's to decide, and nothing was
  changed.
- **`idiv` is out of the solver's reach at both ceilings.** Four
  obligations, 3,000 ms and 300,000 ms, both UNDECIDED. The cause is
  visible in the term: a signed divide whose divisor is a 32-copy
  concat of one sign bit. If the model table's own printer emitted
  `SignExt` where the builder means a sign extension, both the rendered
  source and the solver's job would be far smaller — but that is a
  change to how the table prints, which belongs to tasks m1/m1b.
- **The vector place is where the emulation route stops today.** Two of
  the ten cells are float, and both refuse in both targets for the same
  reason: the term keeps the whole 128-bit register. Every float
  operator the terms carry is already covered by both renderers. A
  renderer that could hold a vector arrival whole would turn these four
  refusals into runs; whether that is worth doing is a scope decision.

---

# 12. The two lists

## Decided, recorded for audit

- The ten cells are the brief's own, all present at exactly the
  (`mnem`, shape, `key_width`) asked for, so the brief's "nearest
  attested cell" fallback was never used.
- Where a cell carries several sweep rows, one is chosen by two
  mechanical rules — the row whose own `width` equals the cell's
  `key_width`, and the flag-reading row whose setter is the one the
  cell's own attestation records the most ledger rows for — and every
  run's section prints which rule chose its row.
- Every place the table records as written gets its own rendered
  function, compile, carve and gate call, including the flags place;
  the flags place of a flag-reading row is the exception, recorded as
  not written with that cause.
- The parameter order, the flags place's answer home, and the pair
  composition are conventions this task had to state; all three are in
  §4 with the object that shows each.
- The four float refusals are the existing renderers' own, by their own
  cause word, and the renderers were not extended to get around them.
- The UNDECIDED `idiv` verdicts of record are the 3,000 ms ones; the
  300,000 ms re-pose is recorded beside them and did not change the
  answer.
- `handful.json` is written by lane `h1_l6` end to end, after
  `landing_of` gained two fields; lanes `h1_l3` and `h1_l5` ran the
  same commands earlier and their logs stand (§7.1).

## Awaiting the owner

- Nothing. The three items in §11 are for the coordinator, not
  rulings.

---

# ADDENDUM — the verifier over this log

`h1_l8_verify.sh`, the first pass, found 1 DIFFERS and 2 REFUSED, and
both were about the COMMANDS the evidence lane printed, not about any
claim's wording. Neither was fixed by softening a claim; both were
fixed in the lane and every affected transcript was regenerated:

- DIFFERS: `python3 handful.py tally` runs from the artifact folder,
  and the verifier runs every command from `PseudoCoupHQ`,
  so the file was not found. The command now names `handful.py` by its
  full path.
- REFUSED, twice, `head_not_on_the_read_only_allowlist -- \`: the two
  `sed` addresses spelled the table's `|` literally, and the verifier
  splits a pasted command on `|` to check each pipeline stage's head,
  so it read the escaped `\|` inside the sed script as a pipe. The two
  addresses now spell `.` where the `|` sits.

`h1_l10_verify2.sh`, run after those fixes, **LITERAL**:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_238_task_h1_handful_of_find_emulation_runs.md
population: 17 claims across 1 logs
  MATCHES          6
  DIFFERS          0
  UNVERIFIABLE     11
  REFUSED          0
  NOT_RERUNNABLE   0

ONE LINE: 6 of 17 claims reproduce; 11 (65%) carry nothing to re-run

causes, by name:
  prose_only                       7
  attribution_only                 4

peak RSS after the pass: 17.5 MB
```

**TALLY: 17 claims, 6 MATCHES, 0 DIFFERS, 11 UNVERIFIABLE, 0 REFUSED,
0 NOT_RERUNNABLE. Zero DIFFERS, zero REFUSED.** The 11 that carry
nothing to re-run are seven prose verifications and four attributions
into `handful.md` and `src/`. Full untruncated verifier output:
`<runs>/h1/agent/logs/20260909T052606Z__h1_l10_verify2.sh.log`,
on the tower. Nothing above this ADDENDUM was edited after
`h1_l10_verify2.sh` ran.
