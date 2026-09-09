# log 165 — audit of round 12's completion logs (159–164)

Date: 2026-09-03. Auditor: the coordinating session. Figures
recomputed from `~/Programming/PseudoCoupHQ/Research/op_pipeline/`;
commands and outputs pasted. §5.1a labels throughout.

# 1. Verdict

- Round 12 ran under the plan tree and delivered the six modules
  carrying their nodes' names: `reference.py`, `gate.py`,
  `ledger.py`, `canonical_form.py`, `term.py`, `pool.py`. Every
  round-12 node's PROGRESS moved off `planned` with evidence links.
  No question was put to the owner; four tree corrections were written
  before code (log 159 §4 x87 sort; log 160 §3 flag triple; log 161
  §2 sbb/adc rows; log 163 §1.5 `exception_families4` numbering).
- The counts hold on disk (§2): canon39 30,432 proved / 646 refused;
  terms 26,040 proved / 0 withdrawn / 3,865 undecided / 527 no term;
  pool4 1,961 entries / 573 multi-language / 3 compiled+interpreted;
  census5 52 producers. Guard PASS, no exempt; tree clean; vcs
  clean.
- The 415 remainder withdrawals are gone (0 disproved on either
  route); the IN-i ordering defect is fixed (5,818 units affected,
  all re-proved); the `sbb`/`adc` setters exist; the four division
  routines are attached for 304 of 308 callers.
- One finding of my own (§3): the "runtime callee" population is
  3,419 units, not 308. The four `__divti3` names are 9% of it; the
  rest are half-float / bfloat16 / 128-bit-float lowering routines
  from the same archives. The attachment must generalize to every
  symbol the archive index defines — the code already reads that
  index, so this is a loop, not a design. Written into the
  `runtime_callee` CORE as a settled line; round 13 codes it.
- A second finding: the swift toolchain is in the `trickle`
  instance's persist volume, not missing from the machine; task 59
  looked in a fresh instance. Recorded on the same CORE.

# 2. What was checked

LITERAL — recomputed this session:

```
canon39 {'WRAPPED_TEXT_PROVED': 30432, 'REFUSED': 646}
the_pool4 summary: entries 1961, multi-language 573,
   compiled+interpreted 3, brief-strict 5668
name_census5 entries 52
PASS the_pool4.json / name_census5.json /
     exception_families4.json / canon39_wrapped_c.json
git status --porcelain | wc -l  -> 0
check_plans under 0_3_5: 0 errors, 0 warnings
```

Modules present: `reference.py gate.py ledger.py canonical_form.py
term.py pool.py`. Term figures (log 163 §1.2, population 30,432):
proved 26,040 (+861 vs task 58), withdrawn 0, undecided 3,865, no
term 527; consistency line 0.

# 3. The finding — what the call-bearing units actually call

LITERAL — callee names in the relocation comments of canon39's
regenerated wrapped texts, counted this session:

```
__extendhfsf2 2308   __truncsfbf2 1168   __truncsfhf2 1143
__netf2 536   __floatsitf 310   __gttf2 157   __lttf2 157
__floatditf 112   __eqtf2 107   __getf2 104   __letf2 104
__floattisf 88   __floatuntisf 88   __udivti3 77   __umodti3 77
```

GLOSS: `__extendhfsf2` converts a 16-bit half float to a 32-bit
float; `__truncsfbf2` a float to bfloat16; `__netf2`/`__gttf2` compare
128-bit floats; `__floatsitf` converts an int to a 128-bit float. All
are the compiler's own lowering of operations the hardware has no
instruction for, shipped in libgcc / compiler-rt — the same class as
`__divti3`, and in scope by the owner's ruling. Log 161's
`is_runtime_routine` answers from the archive's own symbol index, so
the generalization is: attach every callee that index defines. The
reference then also has to STEP INTO the attached body, which today
it does not; that shape is written into the `reference` CORE.

Also from log 160 §1.7, the remaining undecided by cause: 3,419
runtime callees (above); 499 conditional transfers the reference
refuses because it walks in text order (branch following — written
into the `reference` CORE); 32 rip-relative address computations;
20 8/16-bit division and widening multiply (written into the CORE).

# 4. Nothing for the owner

All items above are implementation under settled rules; they are
recorded in the tree and become round 13's planned items.
