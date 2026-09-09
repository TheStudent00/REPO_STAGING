# log 089 — Task 3: the 34 c/cpp branching seeds

Date: 2026-08-31. Session: Claude Code, TASK 3 of
`log_083_claude_code_task_briefs.md`. Worked alone in
`PseudoCoupHQ/Research/op_pipeline`, new files only.

## Plain-words walkthrough

`seed_extract1.py` (an earlier lap) split every branching arch-unit
into blocks and, when a unit's normal-path computation forked into
two disjoint groups that both reach a `ret` (no trap), tried to tell
which group was "the seed" by looking its text up character-for-
character in the existing straight-line table. For 36 units that
lookup found either zero or two matches, so they stayed unresolved.
34 of the 36 are c/cpp; the other 2 are swift. I read the swift two
first to make sure they were not part of my job: they are the
32-bit-fits-fast-path unsigned division guard (check if the divisor
and dividend both fit in 32 bits, use the cheap 32-bit `div` if so,
else the full 64-bit `div`) — a genuinely different idiom, not a
conversion, and the task brief's title says "34 c/cpp branching
seeds", so I left those two exactly as they were (status still
"unresolved", reason appended to say why they are out of scope, not
silently dropped).

The 34 c/cpp units are all one shape: an unsigned 64-bit integer is
being converted to a 32-bit float and then combined with a second
float argument by an operator (+, -, *, /, ==, !=, >, >=, <=, <, or
cpp's `not_eq`). A plain "treat the bits as signed and convert"
instruction (`cvtsi2ss`) is wrong once the top bit of the u64 is
set (it would read a huge positive number as a negative one), so
the compiler emits TWO paths: the cheap direct-conversion path,
taken for values that fit in the positive range of a signed 64-bit
number, and a halve-then-double path for the rest (shift the value
right by one bit, remember the dropped bit, convert the halved
value, then double the float result — the halving keeps the value
inside the safe positive range for the direct conversion). Both
paths are real computation, neither is a trap, so `seed_extract1.py`
correctly recorded them as "2 disjoint computation groups, 0
matched" — and it was right to give up rather than guess, because
neither path's FULL text (conversion machinery plus operator) is
identical to any existing table entry: the two paths are two
different implementations of the SAME conversion, feeding the SAME
operator.

The task brief already told me the right shape for the answer
(AgentMemory's SEEDED GROUPING amendment, part b, restated in the
brief): the conversion is CONTEXT feeding the seed, not the seed
itself and not a guard. So my job reduced to: cut each candidate
path into "the conversion" and "the operator", and show the two
candidates' operator parts are the same computation.

The cut point is mechanical, not a guess: every one of these units
has one designated register that already holds the SECOND argument
(the one that was already a float — `%xmm0` in this corpus, the
canonical form's own naming). The conversion machinery never reads
or writes that register; the operator is exactly the first step
that touches it, and everything after. So I split each candidate's
text at "the first step that mentions `%xmm0`" — a register-
identity rule, not an operator-spelling rule, so it does not
collide with the spelling ban.

Once split, the two candidates' operator halves use DIFFERENT
scratch register names for "the converted float value" (one path
built it in `%xmm3`, the other in `%xmm2`), because they are
different physical code paths with independently allocated temps.
I found "the converted-value register" by liveness (the last new
`%xmm` register the conversion machinery wrote, never a name
guess), renamed it to one shared placeholder in both operator
halves, and ran BOTH halves through the SAME z3 machinery
`cross_unit_prover.py` already uses (`canon20_behaviour_check.Sim20`
for arithmetic, a reused `Sim20Cmp` for comparisons) with a shared
symbolic seed dict. That proves the two operator halves compute the
identical function for EVERY possible converted value and EVERY
possible second argument — not a sample.

Two mechanical cleanups were needed before the prover could run at
all, both are genuine compiler bookkeeping, not computation:
- a stack spill-and-reload of the result (`movaps %xmmN,-0x8(%rsp)`
  immediately followed by `mov -0x8(%rsp),%xmm0`, same offset) is
  collapsed to a direct register move — the compiler round-tripped
  the value through the stack because it could not keep it live in
  a register across the two joined blocks, not because the maths
  needed it;
- a dead GP-register write that never touches an `%xmm` register
  (e.g. `mov %edi,%eax`, a leftover from the halving idiom's
  dropped-bit bookkeeping) is dropped from ARITHMETIC operator
  halves only (never from comparison halves, where the GP register
  IS the answer).

All 34 units proved equal. Zero DISPROVED, zero UNDECIDED, zero
REFUSED.

## Instances

Worked example, `c/op_117` ("+", u64 + f32):

candidate L1 (direct path): `cvtsi2ss %rdi,%xmm3; addss %xmm3,%xmm0; ret`
candidate L2 (halving path): `shr $1,%rdi; and $0x1,%edi; or %rdi,%rdi; cvtsi2ss %rdi,%xmm2; addss %xmm2,%xmm2; addss %xmm2,%xmm0; mov %edi,%eax; ret`

Split (first touch of `%xmm0`):
- L1 idiom = `cvtsi2ss %rdi,%xmm3`; L1 operator = `addss %xmm3,%xmm0; ret`
- L2 idiom = `shr $1,%rdi; and $0x1,%edi; or %rdi,%rdi; cvtsi2ss %rdi,%xmm2; addss %xmm2,%xmm2`; L2 operator = `addss %xmm2,%xmm0; mov %edi,%eax; ret`

After renaming the idiom-output register to `%xmm8` in both, and
dropping the dead `mov %edi,%eax` from the arithmetic operator half,
the prover ran on:
- `addss %xmm8,%xmm0` (from L1)
- `addss %xmm8,%xmm0` (from L2, after cleanup)

`z3.Solver().check()` returned `unsat` for `val_a != val_b` — PROVED,
verbatim solver detail: `"no input makes the two suffixes disagree"`.

Seed resolved to the simpler (fewer-byte) candidate per THE
REPRESENTATIVE RULE: `seed_text = "addss %xmm3,%xmm0; ret"`
(candidate L1). The conversion machinery is recorded on a `context`
field, not folded into `guards`, not called part of the seed.

Worked example, `c/op_477` ("==", u64 == f32) — a comparison, so
the GP answer register matters and nothing is dropped:

- L1 operator (after rename): `cmpeqss %xmm8,%xmm0; movd %xmm0,%r11d; and $0x1,%r11d; mov %r11d,%eax; ret`
- L2 operator (after rename): `cmpeqss %xmm8,%xmm0; movd %xmm0,%r10d; and $0x1,%r10d; mov %r10d,%eax; ret`

PROVED (`unsat`) even though the temp GP register spellings differ
(`%r10d` vs `%r11d`) — the prover reads GP values by FAMILY
(`canon.py`'s `FAMILY_OF`), not by bare spelling, so this is not a
coincidence of naming, it is the instrument already doing the right
thing.

## The design choice flagged for the owner

The 34 resolved entries in `seeds2.json` each carry a new `context`
field, e.g.:

```
"context": [{
  "kind": "idiom-context (PROVISIONAL LABEL, not ratified -- flagged for the owner, see log_089)",
  "extent": "u64_to_float halving/doubling conversion (ExpandLegalINT_TO_FP, graph_cpp2.json)",
  "idiom_text_by_candidate": {"L1": "cvtsi2ss %rdi,%xmm3", "L2": "shr $1,%rdi; ..."}
}]
```

This is a THIRD component kind next to `seed_text` and `guards`. I
did not fold it into `guards` (it is not a trap or an alternate-
response condition — both paths always compute, there is no
"response") and I did not silently invent a ratified name for it.
The brief's own stop rule names this exact situation ("if recording
that needs a third component kind, FLAG THE DESIGN CHOICE for the owner").
Flagging it here: does `context` belong in the seed schema as a
first-class field, under some other name, or should the idiom
machinery instead be recorded ONLY in Task 6's `super_ops.json`
(which already names `ExpandLegalINT_TO_FP` as the emitting
function) with the seed files staying silent about it? I built the
minimal version (a labeled, clearly-provisional field) so the
finding is not lost, not to preempt the ruling.

## Numbers

- `seeds1.json`: 36 unresolved units total (34 c/cpp, 2 swift).
- `seed_extract2.py` (new file): resolves all 34 c/cpp units.
  0 DISPROVED, 0 UNDECIDED, 0 REFUSED. The 2 swift units are marked
  out-of-scope, not resolved, not dropped.
- Per-unit resolution status for all 34 (operator, both langs):
  c: `+`(x2), `-`(x2), `*`(x2), `/`(x2), `==`(x2), `!=`(x2), `>`(x2),
  `>=`(x2), `<=`(x2), `<`(x2) — all `status: ok`.
  cpp: `+`(x2), `-`(x2), `*`(x2), `/`(x2), `==`(x2), `!=`(x2),
  `not_eq`(x2) — all `status: ok`.
- `check_no_spelling_keys.py seeds2.json` — PASS, no exemption.
- `build_table23c.py` (new file), applied onto the
  `dominant_table23b.json` (901 classes) / `dom_ops21b.json` (26 dom
  ops, 0 singleton, 20 unattached) lineage, per the brief NOT
  table24/dom_ops22 (reserved for Task 7):
  - classes: 901 -> 925 (+24 new, +10 merged into existing rows).
  - the 10 merged units are ALL cpp's comparison seeds (op_117,
    122, 153, 158, 189, 194, 225, 230, 981, 986) — cpp already had a
    straight-line unit of the same (type_pair, result_type) whose
    rendered text is character-identical to the extracted seed.
  - the 24 new-class units are all of c's 20 units plus cpp's 4
    arithmetic ones NOT in the merged list above — their seed text
    still carries this extraction's own scratch-register numbering
    (`%xmm2`/`%xmm3`/`%r10d`/`%r11d`), which the canon7-canon24
    render chain has not been run over for seed FRAGMENTS (only for
    whole 0-branch units). Named as a remainder, not patched around:
    these 24 classes are correct as proved-equal content, but may
    still re-merge with existing classes once that render chain is
    extended to seed fragments — a follow-up, not done here.
  - `dom_ops21c.json`: dom_op family count UNCHANGED at 26 (0
    singleton, 20 unattached), same as `dom_ops21b.json` — the 34
    new units did not gain a cross-language mutual edge this lap
    (expected: no go/rust/swift unit shares this exact idiom shape
    in the current corpus).
  - zero regressions: verified programmatically that all 901
    pre-existing `dominant_table23b.json` classes/members are present
    with byte-identical `(type_pair, result_type, canonical_text)`
    keys and a superset of members in `dominant_table23c.json`.
  - `check_no_spelling_keys.py` PASS on both `dominant_table23c.json`
    (full check, no exemption) and `dom_ops21c.json` (exempt as
    generator provenance, same as `dom_ops21b.json` before it).

## Files

- `op_pipeline/seed_extract2.py` (new) — resolver.
- `op_pipeline/seeds2.json` (new) — 34 resolved + 2 out-of-scope,
  additive over `seeds1.json`.
- `op_pipeline/build_table23c.py` (new) — table/dom_ops rebuild.
- `op_pipeline/dominant_table23c.json`, `op_pipeline/dom_ops21c.json`
  (new) — the updated lineage artifacts.
- PROGRESS.md updated:
  `Planning/node_0_3_research/node_0_3_5_compiler_graph/PROGRESS.md`
  (dated entry appended, single `# PROGRESS` heading preserved).
