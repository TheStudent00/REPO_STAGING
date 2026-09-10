# Task t4 — the general construction: any cell's term built from `& | ^ ~`, constant shifts, a conditional and variables, one construction per OPERATION KIND, composed over the term; measured against the eight-schema tier

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it (the
layout: real paths on the laptop, flat on the tower; waits in short
calls). Then `Research/GLOSSARY.md`, `task_t2_brief.md` and `log_257`
(the eight schemas, the Lean lemmas, `construct/lean/OWED.md`),
`task_t3_brief.md` (NOT run yet; this task does not wait for it:
`render_general` below binds EVERY node of the term to a named variable
itself — a `let`/`const`/local per node, in every target and in the
Lean statement — so nested printing is not this task's problem, and t3
shrinks to the x87 arrival and the code version), `task_ap6_brief.md`
and `log_255` (tier 1; the bank; `code_version`), `Research/op_pipeline/term.py`.
Instance `t4.conf` (copy `t3.conf`). Artifact folder:
`Research/oracle/cross_construction/emulation/construct/general/`; lanes
under `lanes_t4/`.

## 0. Priority (the owner, 2026-09-10: "i would argue its the top priority because it is meant to be capable of proving as a guarantee")
This task runs NOW, beside ref2, ahead of t3 and rv3b. It reads the
stores as they are when it starts (ref2 writes corrected ones BESIDE
the old; record the hashes you read, as rv2 and rv3 did) and touches
nothing under `Research/op_pipeline/` and nothing ref2 writes. If
ref2 closes while you run, do not switch stores mid-pass; say so in
the log, and the bank's delta on the corrected terms is the next pass.

## 1. What this is, and the owner's ruling it carries out
the owner, 2026-09-10: "why isn't everything proven at least via the method
I've described with the primitives". The method: a language with
`& | ^ ~`, a conditional and variables has every gate a processor is
built from, so every opcode's mapping is constructible; "whoever gets
there first" (the language's own operator when it has one, the
construction when it does not). What t2 built is EIGHT hand-written
schemas for eight cells' shapes. That is not the method. This task
builds the method.

`operation kind`
- one node kind of a term: `bvadd bvsub bvmul bvudiv bvsdiv bvurem
  bvsrem bvshl bvlshr bvashr bvand bvor bvxor bvnot concat extract
  zero_extend sign_extend ite` and the comparisons; the float kinds
  (`fp.add fp.mul fp.div fp.sqrt fp.to_sbv fp.to_fp ...`) as the
  softfloat constructions over integers.
- built: `Term.normalize`'s own node vocabulary, listed from the term
  store: every kind that occurs, with the widths it occurs at, counted.

`construction`
- for one operation kind at width n over a target whose widest word is
  W: a sequence of named intermediates using only `& | ^ ~`, shifts by
  CONSTANTS (wiring, not a gate), a conditional and variables, over
  ⌈n/W⌉ words per value. One construction per kind, general in (n, W):
  add by carry-lookahead in log₂ n rounds; mul by shift-add in n rounds;
  udiv/urem by restoring division in n rounds; shifts by a barrel of
  log₂ n stages; compare by the borrow of a subtraction; sign kinds by
  their unsigned kind and a sign fix; float kinds by the softfloat
  algorithms over the integer constructions.
- proved ONCE per kind, general in n and W, as a Lean lemma in the
  form t2 used for its eight; where a lemma does not close in the task's
  budget, the instantiation is proved by z3 at every width the store
  uses, and the lemma is recorded in `OWED.md` with where it stops.

`general render`
```
render_general(term, lang):
    for node in term, leaves first:
        if lang has node.kind at node.width:            # whoever gets there first
            emit the language's operator                # tier 1, unchanged
        else:
            emit construction[node.kind](node.width, W) # this task
            over the node's children's names            # named intermediates (t3)
    return the source                                    # compiled, carved, gated as ever
```

## 2. The measurement (the point of the task)
Run the loop with this tier in place of the eight schemas, on every
cell that has no proved certificate for a target (both architectures:
x86-64 and riscv64), the bank as the delta. Report, in this order:
1. per operation kind: constructed / proved by lemma / proved by z3 /
   undecided / refused, with the width and the target — THE TABLE THAT
   ANSWERS "why isn't everything proven": every cell without a proof
   sits in a row with a named cause.
2. the three readings on x86 beside t2's (96 / 154 / 141 of 205) and
   the RISC-V count beside rv3's 117 of 255.
3. the collapse column (LANDED / NOT COLLAPSED, instruction counts) per
   constructed certificate: the owner's compiler question on the general tier.
4. the gate's cost where it runs out: which kinds at which widths z3
   cannot close in 30 s (multiply and divide at 64 are expected here);
   for those, the proof form actually used (lemma / z3 / none), LITERAL.
5. the size of the constructed sources (lines) by kind and width.

## 3. Discipline
Guard over every json/jsonl; log (next free number); verifier lane;
PROGRESS on the autopoly node, the lean node and both architecture
nodes; sync-back; instance down. Memory bound 6g, peak RSS, abort
`ABORT_MEMORY_T4`; z3 30 s hard. Shared files this brief authorises:
`construct/` (new sub-folder `general/`), the driver's tier dispatch,
`bank.py` only for `code_version`; nothing under `Research/op_pipeline/`.
Never delete anything under `<runs>/` or `PUBLIC/Airlock/`.
Reply with the per-kind table, the readings beside t2's and rv3's, the
collapse counts, the gate's cost line, every flag LITERAL.
