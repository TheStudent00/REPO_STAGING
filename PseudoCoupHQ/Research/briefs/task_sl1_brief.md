# Task sl1 — the RISC-V lifter GENERATED from the Sail model: no instruction transcribed by anyone, every ratified instruction known, the table rebuilt by the run

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it
(waits in short calls; the spelling ban; sync args in the flat form).
Then `Research/GLOSSARY.md`, `Research/oracle/riscv/riscv_reference.py`
(the lifter as it stands: 49 instructions typed in by a person from
Sail's text, one builder per family; its `simulate`/walk interface is
what the whole line consumes and MUST be kept), `sail_points.py` (the
point check against Sail's C simulator: it becomes this task's guard),
logs 258, 264, 267 (every "the lifter has no entry for ..." row:
`binvi`, `fsgnjn.s`, `bexti`, `orn`, `c.not` — the defect this task
removes for good). The Sail model is mounted at `/sources/sail-riscv`
in the container (`model/extensions/I/base_insts.sail`, `M/`, `F/`,
`D/`, `Zb*/`, `C/`); the image has `sail` 0.20.2 (opam) and
`sail_riscv_sim`. Instance `sl1.conf` (copy `rv4.conf`). Artifact
folder: `Research/oracle/riscv/sail_lifter/`; lanes under `lanes_sl1/`.

## 0. the owner's criterion, 2026-09-13, that this task exists for
"if i stop making updates to the repo and things that it processes
churn, the system will still be able to re-generate essentially all
the proofs, Hub, and whatever else downstream by running the system."
And: "no human intelligence (LLM or biological) is pointing to a
spelling and saying 'that's div!'". So: the lifter's table
(instruction → definition as a z3 formula per written register) is
PRODUCED BY A TOOL from the Sail model on every run. Nobody types a
row. Nobody names an instruction. A new compiler that writes an
instruction Sail defines needs no person.

## 1. What to build
`the generated table`
- for every instruction the model defines in the subset the image's
  compilers target (rv64gc + Zba/Zbb/Zbs + Zicond, at least: the
  census of `bb1`/`rv6` bodies is the floor), its definition as a z3
  formula per written register, with the operand decoding the model's
  own (`mapping clause assembly`), produced from the Sail source by a
  Sail backend or exporter, never by reading the text and typing.
- measure the routes FIRST, in a sample lane, and pick the one that
  closes, LITERAL outputs pasted: (a) Sail's own SMT/`-smt` or
  property export per `execute` clause; (b) the Lean backend
  (`sail --lean`, if this version has it) and a Lean→z3 reading; (c)
  Isla built against the Sail version it pins (`opam pin` to that
  commit inside the instance; the earlier attempt failed against
  master — pin, do not use master); (d) the Jib/IR dump (`sail -ir`
  or the compiler's intermediate) walked symbolically by a small
  interpreter of ours that knows Jib's dozen constructs and NOTHING
  about any instruction. Any route that requires a per-instruction
  case in our code is refused by the criterion.
`the drop-in`
- `riscv_reference.py`'s walk keeps its interface; its builders are
  replaced by lookups into the generated table; the generator runs as
  the first step of every lane that needs the lifter (a cached table
  keyed by the Sail model's git commit is fine: churn in Sail
  regenerates it, nothing else does).
`the guard`
- `sail_points.py` on EVERY generated instruction: the generated
  formula against the C simulator at points, edge values first. The
  transcription had 0 disagreements at 860,304 points; the generated
  table must show its own number, and a disagreement is a defect in
  the generator, never a row edited by hand.

## 2. What to measure and report
1. instructions in the generated table, by extension, beside the 49
   of the transcription; the ones the transcription lacked
   (`binvi`, `bexti`, `orn`, `c.not`, `fsgnjn.s`, ...) present by
   construction.
2. the point check: instructions × points, agree / disagree.
3. rv6 again (`rv6_all_langs.py`, every RISC-V cell, c cpp go rust,
   one process) on the generated lifter: the table with "of 255" on
   every row beside log_268's; every former WALK_REFUSED row's new
   verdict.
4. the regeneration test, LITERAL: delete the generated table, run
   the lane, the table is back and byte-identical (or its diff named).
Guard over every json; log (next free number); verifier; PROGRESS on
the riscv64 node; sync-back; instance down. Memory bound 6g, abort
`ABORT_MEMORY_SL1`. Shared files this brief authorises:
`riscv_reference.py` (builders → lookups; the interface unchanged),
nothing under `Research/op_pipeline/`. Never a case per instruction
name in anything this task writes.
