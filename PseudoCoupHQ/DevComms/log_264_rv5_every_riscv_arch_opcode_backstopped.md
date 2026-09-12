# log 264 — rv5: every RISC-V arch-opcode through the loop, both routes, one process, five minutes

Written 2026-09-12 by the coordinator (Fable), who ran it. the owner: "i want
all of them backstopped since the computational complexity is
exceptionally low."

## §0. In plain words
Task t4's RISC-V driver, unchanged, at ship flags, with ONE change: the
population is every RISC-V arch-opcode in the model table (255), not
only the 94 that had no x86 twin. Two routes per arch-opcode and
language: the language's own operator first, and the backstop (every
node built from `& | ^ ~`, constant shifts, a conditional and
variables). 510 runs (255 × c, go) in 4 min 57 s, one process, peak 476
MB. RISC-V arch-opcodes with a proved emulation: **244 of 255 (95.7%)**,
from 117. the owner was right: the cost is small and the population filter
was the whole gap.

RETRACTION (coordinator, log_263): "the lifter has no memory model and
refuses loads and stores". False as stated: `riscv_reference.py` models
a load and a store on a named memory cell (`build_load`, `build_store`)
and this run proved `fld`, `ld` and their kin. What rv1 refused "by
name" were the Sail POINT checks for those mnemonics, not the lifter.
The optimization-off failure of rv4 therefore has a different cause
than I wrote, and it is not yet measured.

## §1. The lane
| lane | submitted | done | runs |
|---|---|---|---|
| rv5_l1_backstop_every_cell.sh (`construct/general/rv5_all.py`) | 01:38:57Z | 01:43:55Z | 510 |

## §2. Per route, over the 510 runs, and per language
| route | proved | disproved | undecided | refused (render / compile / walk) | not gated (body over the ceiling) | cells proved |
|---|---|---|---|---|---|---|
| the language's own operator first | 453 | 10 | 5 | 0 / 30 / 6 | 6 | 243 |
| the backstop, every node constructed | 326 | 36 | 2 | 40 / 5 / 77 | 24 | 195 |
| union | | | | | | **243** (+1 inherited = 244) |

| language | arch-opcodes proved | of 255 |
|---|---|---|
| c | 217 | 85% |
| go | 238 | 93% |

## §3. The 12 arch-opcodes without a proof on either language, by cause
| arch-opcode | c | go | cause |
|---|---|---|---|
| div, rem 64 | undecided | disproved | the divide check: z3 out of budget; go's own zero-divisor branch disproves the plain reading |
| remu 64 (two forms) | refused | refused | compile refusal, LITERAL in the store |
| mulh, mulhsu 64 (two forms each) | undecided | refused | the product's high half: the known hard check; go has no 128-bit product |
| fsub.s, fsub.d | refused | undecided | float subtraction: c's render refused; go's check out of budget |
| fcvt.s.lu, fcvt.d.lu | refused | disproved | unsigned 64-bit to float: c refused; go's answer disproved (a rounding path) |

## §4. Flags, named
1. The backstop route DISPROVED 36 runs that the native route proved:
   a constructed body whose walked meaning differs from the term. Either
   a construction defect at some width or a lifter reading of the longer
   body; NOT measured here; the counterexamples are in `rv5_all.jsonl`.
2. WALK_REFUSED 77 on the backstop route: the lifter met an instruction
   it does not model in the longer constructed bodies; the mnemonics are
   in the store, LITERAL, and are the lifter's next rows.
3. 24 constructed bodies above the gate's 4,000-instruction ceiling.
4. `chosen_policy` in the store records the route whose verdict was
   kept, not "the backstop was not run": both routes ran on every cell.
