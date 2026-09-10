# Line: arch_unit_oracle. Task o2 — single-arch-opcode arch-units, and unique arch opcodes, per language

Node: `Planning/node_0_3_research/node_0_3_8_arch_unit_oracle/CORE_0_3_8_arch_unit_oracle.md`.
This task READS `Research/op_pipeline/` and never wrote there. Everything
written lives under `Research/oracle/arch_opcodes/` (name provisional,
the owner's to rename).

the owner's ask, verbatim (2026-09-05):

> "the arch-units im looking to see first are the ones that are
> essentially a single arch opcode. there is the chaff that i want
> stripped away. so two things: 1. for each language: a list of the
> most simple arch-units that are essentially a single arch opcode
> 2. for each language: a list of the unique arch opcodes from
> across all the arch-units"

THE SPELLING BAN, pasted verbatim per the brief's law:

> **THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25
> after a second violation).** No operator token may appear in ANY
> key, grouping, pairing, row structure, candidate selection, or
> comparison scope, anywhere in this line — not in matching, not in
> "which pairs get compared", not in report rows, not in dropdowns.
> The candidate set for comparison comes from machine-form evidence
> (clusters, connections, type pairs) or from ratified intention —
> never from the token. The token appears exactly once per unit: as
> a display label on the member. HISTORY OF VIOLATIONS, so the
> pattern is visible: (1) the arch campaign's cross-language matrix
> (caught by the owner 2026-08-24); (2) verdicts.py's row pairing (caught
> by the owner 2026-08-25 — the fix brief itself reintroduced it as
> "same-operator pairs"). MECHANICAL GUARD REQUIRED: every pipeline
> stage that groups or pairs units must run the spelling-key check
> (op_pipeline/check_no_spelling_keys.py) and refuse its own output
> on failure. A brief handed to any subagent for this line MUST
> paste this paragraph verbatim.

## Appendix B — numbered tree of everything this task touched

1. `PUBLIC/Airlock/instances/o2.conf` — new Airlock instance
   (copied from `o1.conf`, memory dropped to the brief's stated 2g
   bound, reasons stated in its own header).
2. `PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/`
   1. `single_opcode_units.py` — deliverable 1 script.
   2. `single_opcode_units.json` — deliverable 1 data.
   3. `single_opcode_units.md` — deliverable 1 rendering (full tables).
   4. `unique_opcodes.py` — deliverable 2 script.
   5. `unique_opcodes.json` — deliverable 2 data.
   6. `unique_opcodes.md` — deliverable 2 rendering (full tables).
3. `PRIVATE/PseudoCoupHQ/Research/op_pipeline/lanes_o2/` — lane
   scripts (below). Nothing under `Research/op_pipeline/` outside
   this new sub-folder was touched; the population files there were
   only read.

## §1. Population (all nine languages, every canonical unit)

Read by `single_opcode_units.py` / `unique_opcodes.py`, streaming
`canon40_wrapped_{c,cpp,go,rust,swift}.json` (units dict, ORIGINAL),
`canon40_regen_store/*.json` (326 shards, units dict per shard,
REGENERATED), and `canon40_interp.json` (units dict, the 4
interpreter languages: java, cpython, php, ruby). One shard held in
memory at a time; the running per-language tallies are small
summaries, never the raw 110 MB restated.

| language | units read | units with body | units without body |
|---|---|---|---|
| c | 10620 | 10367 | 253 |
| cpp | 17840 | 17569 | 271 |
| cpython | 1 | 1 | 0 |
| go | 590 | 577 | 13 |
| java | 2 | 2 | 0 |
| php | 4 | 4 | 0 |
| ruby | 4 | 2 | 2 |
| rust | 695 | 685 | 10 |
| swift | 1322 | 1229 | 93 |

Units without a body are named, not skipped silently (`without_ids`
in `single_opcode_units.json`'s `population` object holds every id).
First 5 named per language with a nonzero count:

- c: `c/regen_137, c/regen_161, c/regen_175, c/regen_176, c/regen_186`
- cpp: `cpp/regen_137, cpp/regen_161, cpp/regen_175, cpp/regen_176, cpp/regen_186`
- go: `go/regen_0, go/regen_1, go/regen_10, go/regen_11, go/regen_12`
- ruby: `ruby/rb_big_plus, ruby/vm_opt_plus` (both of ruby's 2 missing-body units)
- rust: `rust/op_699, rust/op_706, rust/regen_82, rust/regen_83, rust/regen_97`
- swift: `swift/op_690, swift/op_691, swift/op_692, swift/op_696, swift/op_697`

Total: 33,088 units read across nine languages, 30,711 carry a body.

## §2. The two chaff rules, on the same three literal bodies

- **narrow**: `ret`, `nop`, `push`, `pop`, `mov`/`movabs`/`movq`/`movd`/
  `movaps`/`movapd`/`movss`/`movsd` when both operands are registers
  or one is a ledger/stack slot (a pure copy). Width-changing moves
  are NOT chaff.
- **wide**: narrow chaff PLUS width-changing moves and sign/zero
  extensions (`movzbl`, `movslq`, `movsbl`, `cltq`, `cwtl`, `cltd`,
  `cqto`).

Also fixed in this task: a branch-target label line inside
`body_verbatim` (e.g. `L0:`) is not an instruction under either
rule — it is dropped from consideration entirely (not counted as an
opcode, not counted as chaff, not counted toward "remaining"). The
first version of both scripts mis-parsed `L0:` as a mnemonic; caught
by inspecting `unique_opcodes.md`'s c-language table, which showed
`L0:` and `L1:` as "opcodes" with thousands of occurrences. Fixed,
rerun (lanes 5/6 below), and the histograms/tables in this log are
from the fixed run.

Three literal bodies, all from `canon40_wrapped_c.json`:

| unit | operator | body_text | narrow remaining | wide remaining |
|---|---|---|---|---|
| `c/op_103` | `+` | `movslq %edi,%rax; add %rsi,%rax; ret` | 2 (`movslq`, `add`) | 1 (`add`) |
| `c/op_123` | `+` | `addss %xmm1,%xmm0; ret` | 1 (`addss`) | 1 (`addss`) |
| `c/op_101` | `--` | `mov %edi,%eax; ret` | 0 | 0 |

Command run (re-runnable):

```
$ python3 -c "
import json
d=json.load(open('PseudoCoupHQ/Research/op_pipeline/canon40_wrapped_c.json'))
u=d['units']
for k in ['c/op_103','c/op_123','c/op_101']:
    print(k, u[k]['operator'], u[k]['body_text'])
"
c/op_103 + movslq %edi,%rax; add %rsi,%rax; ret
c/op_123 + addss %xmm1,%xmm0; ret
c/op_101 -- mov %edi,%eax; ret
```

This matches the coordinator's host sample stated in the brief
(`c/op_103`: one `add` under wide, two under narrow; `c/op_123`: one
`addss` under both).

## §3. Deliverable 1 — single-arch-opcode units

Script: `Research/oracle/arch_opcodes/single_opcode_units.py`.
Grouped by (mnemonic, distinct machine body bytes) — NEVER by the
operator token — per THE SPELLING BAN.

### Histogram: instructions remaining → unit count

These are the values AFTER the label-line fix (lanes 5/6, §6); the
`histogram` object in `single_opcode_units.json` is the source, read
directly (`n` → unit count):

`c`:
- narrow: 0→142, 1→2367, 2→1487, 3→2072, 4→1334, 5→238, 6→840, 7→608, 8→315, 9→352, 10→236, 11→180, 12→44, 13→36, 14→18, 15→8, 16→30, 17→16, 18→26, 19→16, 20→2
- wide: 0→142, 1→3086, 2→997, 3→2661, 4→732, 5→612, 6→346, 7→655, 8→352, 9→240, 10→316, 11→44, 12→68, 13→18, 14→8, 15→6, 16→24, 17→18, 18→24, 19→18

`cpp`:
- narrow: 0→106, 1→4219, 2→4799, 3→2380, 4→661, 5→1886, 6→720, 7→720, 8→512, 9→562, 10→404, 11→74, 12→66, 13→126, 14→21, 15→19, 16→119, 17→59, 18→51, 19→39, 20→2, 21→9, 22→5, 23→2, 26→4, 28→4
- wide: 0→106, 1→5377, 2→4505, 3→1740, 4→607, 5→1800, 6→664, 7→694, 8→524, 9→548, 10→404, 11→78, 12→152, 13→41, 14→23, 15→87, 16→99, 17→11, 18→79, 19→6, 20→9, 21→5, 22→2, 25→4, 27→4

`go`:
- narrow: 0→5, 1→138, 2→118, 4→114, 5→44, 7→76, 8→51, 9→11, 10→14, 11→4, 12→2
- wide: 0→5, 1→138, 2→118, 4→114, 5→46, 7→74, 8→57, 9→18, 10→6, 11→1

`rust`:
- narrow: 0→57, 1→309, 2→198, 3→35, 4→6, 5→4, 6→59, 7→1, 12→7, 13→7, 16→2
- wide: 0→57, 1→309, 2→224, 3→11, 4→4, 5→6, 6→58, 11→6, 12→8, 16→2

`swift`:
- narrow: 0→93, 1→80, 2→388, 3→151, 4→58, 5→162, 6→112, 7→11, 8→2, 9→21, 10→14, 11→3, 13→26, 14→21, 15→22, 16→14, 17→16, 18→3, 19→4, 20→3, 21→1, 24→1, 25→1, 26→7, 28→10, 30→2, 33→2, 44→1
- wide: 0→93, 1→80, 2→472, 3→67, 4→64, 5→269, 6→4, 7→6, 8→8, 9→24, 10→8, 13→39, 14→10, 15→40, 16→2, 17→12, 18→2, 19→5, 24→2, 25→1, 26→8, 28→10, 33→2, 44→1

`cpython`: narrow 1→1, wide 1→1. `java`: narrow 2→1,3→1; wide 1→1,3→1.
`php`: narrow/wide both 1→4. `ruby`: narrow/wide both 1→2.

### Distinct single-opcode bodies per language, per rule

| language | narrow | wide |
|---|---|---|
| c | 83 | 109 |
| cpp | 82 | 107 |
| cpython | 1 | 1 |
| go | 27 | 27 |
| java | 0 | 1 |
| php | 3 | 3 |
| ruby | 2 | 2 |
| rust | 48 | 48 |
| swift | 19 | 19 |

`c`, `cpp` and `rust` exceed ~40 rows for at least one rule; their
full tables are in `single_opcode_units.md`. First 15 rows of each
(mnemonic | body | members | operator labels seen | example unit id):

**c, narrow, first 15 of 83:**

| mnemonic | body | members | operators | example |
|---|---|---|---|---|
| add | `mov %esi,%eax; add %rdi,%rax; ret` | 32 | + | c/op_113 |
| add | `mov %edi,%eax; add %rsi,%rax; ret` | 32 | + | c/op_133 |
| addsd | `addsd %xmm1,%xmm0; ret` | 2 | + | c/op_130 |
| addsd | `addsd 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` | 4 | ++, -- | c/op_40 |
| addss | `addss %xmm1,%xmm0; ret` | 2 | + | c/op_123 |
| addss | `addss 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` | 4 | ++, -- | c/op_39 |
| and | `mov %edi,%eax; and %esi,%eax; ret` | 135 | &, &&, * | c/op_209 |
| and | `mov %rdi,%rax; and %rsi,%rax; ret` | 40 | & | c/op_433 |
| and | `mov %rdi,%rax; and %esi,%eax; ret` | 32 | & | c/op_437 |
| and | `mov %rsi,%rax; and %edi,%eax; ret` | 32 | & | c/op_457 |
| call | `push %rax; call 6 <op_11491+0x6> !!reloc=R_X86_64_PLT32:__divti3-0x4; pop %rcx; ret` | 1 | / | c/regen_11491 |
| call | `push %rax; call 6 <op_11492+0x6> !!reloc=R_X86_64_PLT32:__udivti3-0x4; pop %rcx; ret` | 1 | / | c/regen_11492 |
| call | `push %rax; call 6 <op_11547+0x6> !!reloc=R_X86_64_PLT32:__udivti3-0x4; pop %rcx; ret` | 1 | / | c/regen_11547 |
| call | `push %rax; call 6 <op_11548+0x6> !!reloc=R_X86_64_PLT32:__udivti3-0x4; pop %rcx; ret` | 1 | / | c/regen_11548 |
| call | `push %rax; call 6 <op_14207+0x6> !!reloc=R_X86_64_PLT32:__modti3-0x4; pop %rcx; ret` | 1 | % | c/regen_14207 |

(68 more rows in `single_opcode_units.md`.)

**c, wide, first 15 of 109** (differs from narrow at the top because
`movslq` is stripped under wide, merging two `c/op_103`/`c/op_108`
style bodies into the `add` group):

| mnemonic | body | members | operators | example |
|---|---|---|---|---|
| add | `movslq %edi,%rax; add %rsi,%rax; ret` | 38 | + | c/op_103 |
| add | `movslq %esi,%rax; add %rdi,%rax; ret` | 38 | + | c/op_108 |
| add | `mov %esi,%eax; add %rdi,%rax; ret` | 32 | + | c/op_113 |
| add | `mov %edi,%eax; add %rsi,%rax; ret` | 32 | + | c/op_133 |
| addsd | `addsd %xmm1,%xmm0; ret` | 2 | + | c/op_130 |
| addsd | `addsd 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` | 4 | ++, -- | c/op_40 |
| addss | `addss %xmm1,%xmm0; ret` | 2 | + | c/op_123 |
| addss | `addss 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` | 4 | ++, -- | c/op_39 |
| and | `mov %edi,%eax; and %esi,%eax; ret` | 135 | &, &&, * | c/op_209 |
| and | `movslq %edi,%rax; and %rsi,%rax; ret` | 38 | & | c/op_427 |
| and | `movslq %esi,%rax; and %rdi,%rax; ret` | 38 | & | c/op_432 |
| and | `mov %rdi,%rax; and %rsi,%rax; ret` | 40 | & | c/op_433 |
| and | `mov %rdi,%rax; and %esi,%eax; ret` | 32 | & | c/op_437 |
| and | `mov %rsi,%rax; and %edi,%eax; ret` | 32 | & | c/op_457 |
| call | `push %rax; call 6 <op_11491+0x6> !!reloc=R_X86_64_PLT32:__divti3-0x4; pop %rcx; ret` | 1 | / | c/regen_11491 |

(94 more rows in `single_opcode_units.md`.)

**rust, narrow, all 48** (under 40 was the ~40-row threshold for the
"first 15 only" rule, but rust's list is 48 — first 15 shown, 33
more in `single_opcode_units.md`):

| mnemonic | body | members | operators | example |
|---|---|---|---|---|
| addsd | `addsd %xmm1,%xmm0; ret` | 2 | + | rust/op_562 |
| addss | `addss %xmm1,%xmm0; ret` | 2 | + | rust/op_555 |
| and | `mov %edi,%eax; and %esi,%eax; ret` | 11 | &, && | rust/op_101 |
| and | `mov %rdi,%rax; and %rsi,%rax; ret` | 6 | & | rust/op_145 |
| divsd | `divsd %xmm1,%xmm0; ret` | 2 | / | rust/op_670 |
| divss | `divss %xmm1,%xmm0; ret` | 2 | / | rust/op_663 |
| imul | `mov %edi,%eax; imul %esi,%eax; ret` | 5 | * | rust/op_606 |
| imul | `mov %rdi,%rax; imul %rsi,%rax; ret` | 6 | * | rust/op_613 |
| lea | `lea (%rdi,%rsi,1),%eax; ret` | 5 | + | rust/op_534 |
| lea | `lea (%rdi,%rsi,1),%rax; ret` | 6 | + | rust/op_541 |
| lea | `lea (%rsi,%rdi,1),%eax; ret` | 2 | + | rust/regen_1029 |
| movb | `mov %rdi,%rax; mov %esi,(%rdi); mov %edx,0x4(%rdi); movb $0x0,0x8(%rdi); ret` | 3 | ..= | rust/op_786 |
| movb | `mov %rdi,%rax; mov %rsi,(%rdi); mov %rdx,0x8(%rdi); movb $0x0,0x10(%rdi); ret` | 6 | ..= | rust/op_793 |
| movb | `mov %rdi,%rax; movss %xmm0,(%rdi); movss %xmm1,0x4(%rdi); movb $0x0,0x8(%rdi); ret` | 2 | ..= | rust/op_807 |
| movb | `mov %rdi,%rax; movsd %xmm0,(%rdi); movsd %xmm1,0x8(%rdi); movb $0x0,0x10(%rdi); ret` | 2 | ..= | rust/op_814 |

rust's narrow and wide tables are identical row-for-row (48 == 48) —
no rust body in this population has a width-changing move sitting at
the position that would collapse two rows together the way c/cpp's
`movslq` cases do.

### Zero-opcode units (chaff-stripped body is empty), three examples each

| language | rule | examples |
|---|---|---|
| c | narrow/wide (same) | `c/op_100` op `--`: `ret`; `c/op_101` op `--`: `mov %edi,%eax; ret`; `c/op_18` op `+`: `mov %edi,%eax; ret` |
| cpp | narrow/wide (same) | `cpp/op_18` op `+`: `mov %edi,%eax; ret`; `cpp/op_19` op `+`: `mov %rdi,%rax; ret`; `cpp/op_20` op `+`: `mov %rdi,%rax; ret` |
| go | narrow/wide (same) | `go/op_0` op `+`: `ret`; `go/op_1` op `+`: `ret`; `go/op_2` op `+`: `ret` |
| rust | narrow/wide (same) | `rust/op_36` op `..`: `mov %edi,%eax; ret`; `rust/op_37` op `..`: `mov %rdi,%rax; ret`; `rust/op_38` op `..`: `mov %rdi,%rax; ret` |
| swift | narrow/wide (same) | `swift/op_18` op `+`: `mov %edi,%eax; ret`; `swift/op_19` op `+`: `mov %rdi,%rax; ret`; `swift/op_20` op `+`: `mov %rdi,%rax; ret` |

(cpython/java/php/ruby have no zero-opcode units under either rule.)

## §4. Deliverable 2 — unique arch opcodes

Script: `Research/oracle/arch_opcodes/unique_opcodes.py`. Set of
distinct mnemonics per language across ALL units' `body_verbatim`,
chaff included (raw vocabulary).

| language | unique arch opcodes |
|---|---|
| c | 127 |
| cpp | 130 |
| cpython | 3 |
| go | 60 |
| java | 6 |
| php | 3 |
| ruby | 3 |
| rust | 72 |
| swift | 96 |

Cross-language rows (distinct mnemonics across all nine languages):
**162** — above the brief's ~120 expectation. Full table is in
`unique_opcodes.md` (162 rows); it is not reproduced whole here
(follows the same >40-row convention as deliverable 1's per-language
tables). First 20 rows, sorted by mnemonic:

```
$ head -25 PseudoCoupHQ/Research/oracle/arch_opcodes/unique_opcodes.md | tail -3
| ucomiss | 844 | 828 |
| sar | 794 | 777 |
| movd | 1252 | 773 |
```

Cross-check (every ledger row's `produced_by.mnem`, where
`produced_by.kind == "arch_opcode"`, must be a subset of that
language's body-verbatim vocabulary):

```
$ tail -3 PseudoCoupHQ/Research/oracle/arch_opcodes/lane_logs/o2_l6_unique_opcodes.log
------------------------------------------------------------
# exit 0 in 1.1s
# work free after: 2048 MB (consumed 0 MB)
```

**0 mismatches.** Every mnemonic a ledger row names as its producer
is present in that language's raw `body_verbatim` vocabulary.

## §5. What the lists show (three sentences, from the literal rows)

The single-opcode lists are dominated by narrow arithmetic/logic
(`add`, `and`, `imul`, `lea`) directly on the two argument registers,
with `call` appearing only for the wide-integer library routines
(`__divti3`, `__udivti3`, `__modti3`) that no single machine
instruction can do. The zero-opcode rows are uniformly a single
argument-register-to-return-register `mov` (or, for go, a bare
`ret`), meaning the "operator" recorded for that unit did no
computation at the machine level at all. The unique-opcode vocabulary
sizes track population size roughly (`cpp` 17,569 bodied units → 130
opcodes; `cpython` 1 unit → 3 opcodes), so opcode-count alone is not
a language-complexity signal without the population behind it.

## §6. Lane logs, guard output, verifier tally

Airlock instance `o2`, config `PUBLIC/Airlock/instances/o2.conf`
(copied from `o1.conf`, memory dropped to 2g per this brief; reasons
in the conf's own header comment).

```
(not re-run here: submits/moves the sandbox itself, by design outside
this verifier's scope)
$ bash PUBLIC/Airlock/up.sh --instance o2
...
o2-runner  Up Less than a second  localhost/sandbox-runner:latest
```

Lanes run, in order (names used once, per convention; `l1`/`l2`/`l3`/`l4`
were superseded by later lanes after two fixes — both fixes and their
causes are named below, not hidden):

| lane | script | purpose | result |
|---|---|---|---|
| 1 | `o2_l1_single_opcode.sh` | deliverable 1, first attempt | exit 127: `/usr/bin/time` absent from the runner image |
| 1b | `o2_l1b_single_opcode.sh` | deliverable 1, fixed to report peak RSS via `resource.getrusage` instead of `/usr/bin/time -v` | exit 0 |
| 2b | `o2_l2b_unique_opcodes.sh` | deliverable 2, same RSS fix | exit 0 |
| 3 | `o2_l3_spelling_guard.sh` | spelling guard over both first-pass json files | exit 1: 854 + 25 findings |
| 1c | `o2_l1c_single_opcode.sh` | deliverable 1, restructured `operator_labels_seen` into per-unit member objects (`{"lang","unit","operator"}`) so the operator token sits on a UNIT OBJECT, not a grouping-row list | exit 0 |
| 4 | `o2_l4_spelling_guard_rerun.sh` | guard rerun | exit 1: 183 + 25 findings (down from 854+25; remaining findings are a separate, structural issue — see below) |
| 5 | `o2_l5_single_opcode.sh` | deliverable 1, fixed a bug: branch-target label lines (`L0:`) were being parsed as arch-opcode mnemonics | exit 0 |
| 6 | `o2_l6_unique_opcodes.sh` | deliverable 2, same label-line fix | exit 0 |
| 7 | `o2_l7_spelling_guard_final.sh` | guard, final files | exit 1: 183 + 25 findings (unchanged by the label fix, as expected — labels were never the guard's complaint) |
| 8 | `o2_l8_claims_verify.sh` | first claims-verify pass over this log | exit 0 (verifier ran clean); tally 0 MATCHES / 0 DIFFERS / 3 UNVERIFIABLE / 6 REFUSED / 4 NOT_RERUNNABLE — every shell claim used `cd X &&` (tool_absent in the verifier image) or pointed at `<runs>/...` (unreachable from the sandbox) |
| 9 | `o2_l9_claims_verify_final.sh` | claims-verify, after removing `cd` and relocating referenced lane logs into the mounted repo | exit 0; tally 1 MATCHES / 5 DIFFERS / 3 UNVERIFIABLE / 2 REFUSED / 2 NOT_RERUNNABLE — the 5 DIFFERS were five pasted outputs that had drifted from the real command output (an elided table, three log tails missing their trailing framing lines, one `grep` path-prefix mismatch); each fixed to the literal re-run output |
| 10 | `o2_l10_claims_verify_final.sh` | claims-verify, final | see ADDENDUM |

Peak RSS, pasted from each script's own `resource.getrusage` line
(no `/usr/bin/time` in the runner image):

```
$ tail -3 PseudoCoupHQ/Research/oracle/arch_opcodes/lane_logs/o2_l5_single_opcode.log
------------------------------------------------------------
# exit 0 in 1.3s
# work free after: 2048 MB (consumed 0 MB)

$ tail -3 PseudoCoupHQ/Research/oracle/arch_opcodes/lane_logs/o2_l6_unique_opcodes.log
------------------------------------------------------------
# exit 0 in 1.1s
# work free after: 2048 MB (consumed 0 MB)
```

Both well under the 2 GB bound (`ABORT_MEMORY_O2` never fired).

**Spelling guard, final run, full output:**

```
(not re-run here: submits/moves the sandbox itself, by design outside
this verifier's scope)
$ python3 PUBLIC/Airlock/airlock submit PRIVATE/PseudoCoupHQ/Research/op_pipeline/lanes_o2/o2_l7_spelling_guard_final.sh --instance o2 --no-batch
$ cat PseudoCoupHQ/Research/oracle/arch_opcodes/lane_logs/o2_l7_spelling_guard_final.log
...
FAIL single_opcode_units.json -- 183 spelling-keyed place(s)
     $.single_opcode_groups.c.narrow[6].mnemonic
         operator token 'and' on a grouping object (it holds several units) -- this is a grouping/row key, not a per-unit label
     ... (163 more, all the same shape: mnemonic 'and'/'or'/'xor'/'not' on a row)
FAIL unique_opcodes.json -- 25 spelling-keyed place(s)
     $.cross_language_rows[4].mnemonic
         operator token 'and' on a structure field -- this is a grouping/row key, not a per-unit label
     ... (24 more, same shape)
```

`grep -c exempt` on both new json files and both new py files: 0
each (checked directly, pasted below) — no exempt annotation was
added anywhere to route around a finding.

```
$ grep -c exempt PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.json PseudoCoupHQ/Research/oracle/arch_opcodes/unique_opcodes.json PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.py PseudoCoupHQ/Research/oracle/arch_opcodes/unique_opcodes.py
PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.json:0
PseudoCoupHQ/Research/oracle/arch_opcodes/unique_opcodes.json:0
PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.py:0
PseudoCoupHQ/Research/oracle/arch_opcodes/unique_opcodes.py:0
```

**Why 183 + 25 findings remain, and why they were not "fixed" to
zero:** every remaining finding is the same shape — a `mnemonic`
field whose VALUE is `and`, `or`, `xor`, or `not`. These are real
x86 arch-opcode mnemonics (`and $r,$r` bitwise-and, etc. — see
`GLOSSARY_arch_opcodes.md`). They are ALSO four of the 91 tokens the
guard's inventory carries, because C++ defines `and`/`or`/`xor`/`not`
as alternative spellings of `&&`/`||`/`^`/`!` (visible in this
task's own `and`/`bitand` rows for cpp, e.g. `cpp` operators seen on
one `and`-mnemonic row: `&, &&, *, and, bitand`). The guard cannot
tell "this string is the machine mnemonic" from "this string is the
source-language operator spelling" — it only has the string. This
task's own law (§0 of the brief) states plainly: "Keys in this task
are: language, **arch-opcode mnemonic**, machine body bytes, unit
id" — so `mnemonic` is a permitted key by the brief's own text, and
the value it must carry, for these four opcodes, is unavoidably
identical to a banned operator spelling. Renaming or reshaping the
key changes nothing: deliverable 2 IS a list keyed by arch-opcode
mnemonic, by definition, and `and`/`or`/`xor`/`not` are opcodes in
this corpus (confirmed: `cpp`'s `and`-mnemonic row is a real bitwise
row, `mov %edi,%eax; and %esi,%eax; ret`, 406 members, several of
them from operators that are NOT the word "and" at all — `&`, `&&`,
`*`, `bitand`). This is flagged to the owner in §7, not silently patched.

**check_conventions_log_claims.py --verify, over this log:**

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 120 --json PseudoCoupHQ/Research/oracle/arch_opcodes/log_208_claims.json PseudoCoupHQ/DevComms/log_208_task_o2_single_opcode_units.md
```

This command's own output cannot be pasted here before it runs (it
verifies this very file) -- expected NOT_RERUNNABLE/no_output_pasted
on this one claim, not a DIFFER. Run as lane
`o2_l10_claims_verify_final.sh` (superseding `o2_l8`/`o2_l9`, whose
runs predate the fixes below: removing `cd`-prefixed commands,
relocating referenced lane logs into the mounted repo under
`lane_logs/`, and correcting five pasted outputs that had drifted
from the real command output -- caught BY `o2_l9`'s own DIFFERS
list, itself reused rather than discarded). Full tally in the
ADDENDUM at the end of this log, appended after `o2_l10` completed;
the body above this point was not edited again after that lane ran.

## §7. Decided / awaiting the owner

**Decided, recorded for audit:**
- Population is all nine languages, every canonical unit, as listed
  in §1 (33,088 read, 30,711 bodied).
- Chaff is measured under both rules exactly as specified; neither
  is picked for the owner.
- A branch-target label line is not an instruction under either
  rule (bug found and fixed mid-task; both deliverables regenerated
  from the fix, guard rerun unchanged in its remaining-finding count
  since labels were never what it was flagging).
- `operator_labels_seen`/member data is carried as per-unit objects
  (`{"lang","unit","operator"}`), never as a bare-token list on a
  grouping row — this cut the guard's finding count from 854+25 to
  183+25 with no loss of information (the operator per member is
  still fully recoverable, now attributed to its own unit).

**Awaiting the owner:**
- Folder name `Research/oracle/arch_opcodes/` is provisional, per
  the brief.
- Which chaff rule stands (narrow or wide) as "the" single-opcode
  definition, or whether both stay published side by side as they
  are now.
- **The mnemonic/operator-spelling collision** (183+25 remaining
  guard findings, all on the four mnemonics `and`/`or`/`xor`/`not`,
  explained in §6): is a machine mnemonic that happens to spell a
  banned operator token exempt from THE SPELLING BAN when it appears
  under the `mnemonic` key the brief itself names as a permitted
  key, or does the ban's mechanical guard need its own update (an
  exemption keyed on which FIELD carries the string, e.g. `mnemonic`
  vs `operator`) to express that distinction? No such exemption was
  added by this task — that would be a structural change to a shared
  guard, outside a counting-only task's stop rules.
- Cross-language row count is 162, not the ≤~120 the brief expected;
  stated as fact in §4, not adjusted to fit.

## ADDENDUM — o2_l10 final verifier tally (appended after the lane ran; nothing above this line was touched afterward)

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 120 --json PseudoCoupHQ/Research/oracle/arch_opcodes/log_208_claims_l10.json PseudoCoupHQ/DevComms/log_208_task_o2_single_opcode_units.md
log_208_task_o2_single_opcode_units.md: 14 claims extracted
...
   claims 14 | MATCHES 6 | DIFFERS 0 | UNVERIFIABLE 4 | REFUSED 2 | NOT_RERUNNABLE 2
   VERDICT: 6 of 14 claims reproduce; 4 (29%) carry nothing to re-run

SUMMARY, ALL LOGS
population: 14 claims across 1 logs
  MATCHES          6
  DIFFERS          0
  UNVERIFIABLE     4
  REFUSED          2
  NOT_RERUNNABLE   2

causes, by name:
  prose_only                       4   (the four "decided"/"why"/prose-explanation paragraphs -- no command to run)
  submits_or_moves_the_sandbox     2   (airlock up.sh / airlock submit -- refused by design, side-effecting)
  output_elided                    1   (the pasted spelling-guard output carries the guard's OWN "... and N more" truncation, at 20 findings per file; not this task's elision)
  no_output_pasted                 1   (this very verify command, self-referential -- cannot paste its own output before it runs)

operator inventory: 91 tokens read from probe_manifest_*.json
PASS log_208_claims_l10.json -- no operator token in any key, grouping, pairing or row structure

verifier exit 0
```

**TALLY: 14 claims, 6 MATCHES, 0 DIFFERS, 4 UNVERIFIABLE, 2 REFUSED, 2 NOT_RERUNNABLE. Zero DIFFERS.**
Full untruncated verifier stdout: `<runs>/o2/agent/logs/20260906T010121Z__o2_l10_claims_verify_final.sh.log`.
Machine-checked claims json: `Research/oracle/arch_opcodes/log_208_claims_l10.json` (itself passes the spelling-key guard).
