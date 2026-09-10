# log 075 — the canonical form, clarified and enforced

Date: 2026-08-26. Follows
`PRIVATE/PseudoCoupHQ/DevComms/log_074_canonical_form_audit.md`,
which measured that the ratified canonical form was decorating
the pipeline rather than driving it. This log records what the owner
clarified afterwards, what was ruled, what was built in response,
and what the measurements said.

Companion ruling, held in
`PRIVATE/PseudoCoupHQ/AgentMemory.md` under "THE CANONICAL
FORM IS ENFORCED".

---

## 1. What the canonical form is

the owner's statement of it, his words, unchanged:

> * normalized arch opcodes
> * standardized designated registers for traced variables and all others
> * each call is on its own line
> * canonical form of arch-units are runnable with their respective
>   standardized and normalized context

Two elaborations were carried from earlier turns and put in
writing so nothing is lost silently:

- **The entry contract's adapter moves are part of the
  standardized context.** When the hardware pins a register — the
  `cltd` instruction can only read `%rax` — the move that brings
  the traced variable there is a line of the canonical text, not
  something outside it.
- **Branch labels are normalized positionally**, `L0`, `L1`, … in
  address order, so two branching units can be compared as text.

## 2. The two clarifications the owner gave after the audit

The audit's scorecard said 23% of class-forming evidence came from
"non-runnable notations", a bucket that lumped several things
together. the owner separated them.

- **An erased unit re-rendered as instructions IS canonical form.**
  The erasure of moves was never the problem. The problem was the
  pseudo-step notation it was written in.
    - the pseudo-step notation, which is NOT canonical:
      `u0 = cltd(a)` and `u1, answer = idiv(u0:a, b)`
    - the same unit as canonical text, which IS:
      `mov %edi,%eax` / `cltd` / `idiv %esi` / `mov %edx,%eax` / `ret`
    - the pseudo-step notation is retired to comments beside the
      instruction lines; it holds no role in matching, analysis or
      presentation.
- **Transformation is allowed; disappearance is not.** A tool may
  take the canonical text into another representation — lift it,
  simplify it with z3, saturate it in an e-graph — but a valid
  simplified expression must be rendered BACK into canonical
  runnable instructions.
    - the test, stated as a rule: a result that cannot return to
      canonical form is not a result, it is an intermediate.
    - this is what the code now calls the RETURN PATH.

## 3. The ruling that followed

The canonical form is the HOME REPRESENTATION: the default
material for matching, for analysis, and for presentation. Other
representations are kept — the owner's accumulate ruling stands, nothing
with utility is thrown away — but they are derived views, and the
canonical text is what a report shows and what matching is
answerable in.

The drift this replaces is worth naming plainly, because the
ruling exists to stop it recurring: matching was built on raw
compiler bytes and on lifted strings while the ratified form sat
in the files unused, and no one said so until the audit measured
it.

## 4. Canonical text versus canonical bytes — the measurement

the owner asked whether the assembled bytes are a semantic re-mapping of
the text, whether the two actually differ, and what utility the
bytes have over the text. Measured over the 1,562 units that carry
both, in
`PRIVATE/PseudoCoupHQ/Research/op_pipeline/canon_roundtrip.json`:

| question | measured answer |
|---|---|
| byte-strings whose canonical text differs | 0 |
| text-strings whose canonical bytes differ | 0 |

Evidence class: forced by construction — a full pass over the
stored field pairs, not a sample.

So the two are in perfect one-to-one correspondence, and neither
can ever separate a pair the other joins. They carry identical
discriminating power in this corpus.

The literal record for `c/op_246`, quoted from the file:

> "canon_mnem": ["mov %edi,%eax", "cltd", "idiv %esi",
>                "mov %edx,%eax", "ret"],
> "canon_bytes": ["89","f8","99","f7","fe","89","d0","c3"],
> "disassembled_mnem": ["mov %edi,%eax", "cltd", "idiv %esi",
>                       "mov %edx,%eax", "ret"],
> "text_survives_the_round_trip": true

Line for line: `mov %edi,%eax` is `89 f8`; `cltd` is `99`;
`idiv %esi` is `f7 fe`; `ret` is `c3`.

- **The bytes are not a re-mapping.** They are the same
  instructions in the encoding the chip reads, produced by handing
  the canonical text to the assembler. Nothing is reinterpreted
  and nothing is decided.
- **The bytes' real utility is verification, not evidence
  ranking.** Assembling proves the text actually runs rather than
  merely looking plausible; disassembling the result back and
  finding the original text proves the bytes say what the text
  says.
- **Consequence for the evidence order:** ranking canonical bytes
  above canonical text was an empty distinction, since the bytes
  are derived from the text. The arrangement that matches the
  ruling: canonical text is the primary material and the presented
  one; the assembled bytes ride along as its validity check.

## 5. What was built, and what it measured

Programs added, all in
`PRIVATE/PseudoCoupHQ/Research/op_pipeline/`:

- `canon3.py` — canonical text for every unit it can reach,
  including the three populations that had been refused all
  session: branching units (per-block instructions, normalized
  labels), units that ran out of temporary registers (stack slots
  as overflow homes, still runnable), and units where two paths
  hand different values toward one use (each path rendered
  honestly with its own destination register; no invented merge
  point, because the conflict was in the value-NAMING layer and
  never in the instructions).
- `expr_to_canon.py` — the return path: a normalized expression
  rendered back to canonical instructions and assembled for
  validity.
- `dominant_table_canon.py` -> `dominant_table10.json`, and
  `dom_ops8.py` -> `dom_ops8.json` — the canon-text ground added
  to matching, with every class member row carrying its canonical
  text.

Measured results, evidence class as marked:

- **Coverage** (tool's own testimony, read off the artifacts):
  canonical text for 1,699 of 1,779 units — c 608/610, cpp
  744/770, go 83/107, rust 114/125, swift 150/167. The 80
  refusals are named and counted, not hidden.
- **Return path** (tool's own testimony): 384 expressions rendered
  back and assembled; 1,395 honest "no return path" records, of
  which 941 are one cause — operations the normalizer does not
  model yet.
- **Corroboration, not contradiction** (forced by construction):
  342 canonical-text-identical pairs, every one already joined by
  byte identity, and 0 byte-joined pairs whose canonical texts
  disagree among the 1,071 pairs where both sides have canonical
  text. Where both layers can speak, they agree everywhere.
- **Scorecard** (forced by construction): the canonical share of
  class-forming evidence went from 1.84% to 9.26%. Bytes still
  carry 69%, and the reason is coverage rather than preference —
  most byte-joined pairs have no canonical text on one side to
  re-check against, chiefly the 827 compound-assignment member
  slots `canon3` does not cover.
- **Prior results survive** (tool's own testimony): 1,068 classes,
  28 families, modulo still one family across all five languages,
  compound assignment still joining its plain operator's family.
- **The audit's regression case is fixed** (forced by
  construction): swift's division and modulo now differ in
  canonical text exactly where they differ in fact — one ends
  `idiv %esi` / `ret`, the other ends `idiv %esi` /
  `mov %edx,%eax` / `ret`.

## 6. The standing example, in canonical text

`c/op_246`, modulo on two 32-bit signed integers, one block:

> mov %edi,%eax
> cltd
> idiv %esi
> mov %edx,%eax
> ret

`go/op_132`, the same operator and the same types, eight labeled
blocks, quoted in the file's own order:

> L0: test %esi,%esi / je L5 / jmp L1
> L1: cmp $0xffffffff,%esi / jne L3 / jmp L2
> L3: mov %edi,%eax / cltd / idiv %esi
> L2: neg %edi / xor %r10d,%r10d / jmp L4_p1
> L4:    mov %edx,%eax / ret
> L4_p1: mov %r10d,%eax / ret
> L5: call runtime.panicdivide

Read together, these two carry the whole finding of the last two
days in one place: the same three instructions do the division in
both languages, and everything else in the Go unit is the guards
that C does not have.

## 7. Open, carried forward

- Canonical coverage for the 827 compound-assignment member slots,
  which is what holds the byte share at 69%.
- The 941 unmodeled operations blocking return paths.
- The 80 named canonical refusals.
- Ranking: canonical text primary, assembled bytes as its
  verification, per §4 — to be applied unless the owner wants them kept
  as separate grounds for the record.
