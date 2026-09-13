# Task rv9 — the arch-opcode axis on RISC-V, under the owner's rule: the four multiply-high cells and every remaining refusal, by the two untailored routes; nothing written for any opcode

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it.
Then `Research/GLOSSARY.md`, logs 265, 267, 268 (the RISC-V tables
"of 255": native 240–246, backstop 143–196, bit-blast 136–203; the
four with no proof anywhere: `mulh`, `mulhsu` at 64, two operand forms
each; the divide family's remaining refusals on c), the drivers
`construct/general/rv6_all_langs.py` (native + backstop, ship flags)
and `bb1_run.py` + `bitblast.py` (the bit-blast route), `rv4_o0.py`
(the optimization-off wrapper: what it changes and how), and
`Research/oracle/riscv/rv4_o0.jsonl` (rv4: optimization off made the
check WORSE and the cause was never measured — this task measures it).
Instance `rv9.conf` (copy `rv4.conf`). Lanes under
`Research/oracle/riscv/lanes_rv9/`.

## 0. the owner's rule, 2026-09-13, that binds every line of this task
The method may know only what every arch-opcode gives it: its
definition from Sail and the language's primitive operators. Nothing
is written because someone knows a particular cell is a multiply or
a divide. If a change you are about to make would be different for
`mulh` than for `add`, it is refused by this rule; say so in the log
and stop that line. The two routes allowed here: the language's own
operator (native) and z3's own circuit (bit-blast). Task sl1 runs
beside you on the lifter; you do not touch `riscv_reference.py`.

## 1. The native route on the four: name the cause
`mulh` on c and rust went UNDECIDED at ship flags although both
languages hold a 128-bit product. Measure, per (cell, language), and
paste LITERAL: the rendered source; the compiled body; whether the
body calls a library routine (a `call`/`jal` to a symbol outside the
unit — then the standing rule applies: the callee's body is attached
from the toolchain archive and walked, never excluded); the lifted
formula's text beside the definition's text; whether `Term.normalize`
makes them identical; and if not, the first node where they differ.
A GENERIC normalization rule (one that holds for every term, e.g. an
extract of a sign-extended product) is allowed; a rule that names
the cell is not.

## 2. The bit-blast route with structure preserved
The blast route compiled at ship flags let the compiler rewrite z3's
circuit, so the check compared two unlike circuits. Measure the same
four cells, plus every RISC-V cell the blast route left undecided or
refused (log_267), at THREE settings per language: ship flags, `-O1`
(rust `opt-level=1`, go with inlining off), and optimization off
(rv4's flags). For each: compiled / carved / lifted / verdict /
seconds / body instructions; and for optimization off, the cause of
rv4's regression named at last (paste one body: is it stack traffic,
an instruction the lifter lacks, or the walk order?). The check's
budget is the standing 30 s; the 4,000-instruction ceiling stands and
a body over it is NOT_GATED with its size.

## 3. Report
The table "of 255" per language for the union of every route after
this task, beside log_268's; the four cells' rows with their causes;
the three-setting table; every flag LITERAL. Guard; log (next free
number); verifier; PROGRESS on the riscv64 node; sync-back; instance
down. Memory bound 6g, abort `ABORT_MEMORY_RV9`. One process; no
pools.
