# log 270 — AutoPoly progress report, 2026-09-12: what is proved, how far it reaches, and where it sits in the disciplines matrix

Written by the coordinator (Fable) for the owner, on request: "a properly
documented report, concise, following the comms protocol." Every
number below is read from a log written by the task that measured it;
the log is named in the last column or in §8.

## §0. Purpose, in two sentences

AutoPoly proves, per language, that a piece of source computes an
arch-opcode's definition, so a hub can express any program out of
proved pieces. This report says how many arch-opcodes are proved per
language, how much real code that already covers, and how those
results fit the discipline rows the project settled in July.

## §1. The words, declared before use

`arch-opcode`
- one machine instruction the compiler can write, keyed by mnemonic,
  operand form and width. x86 holds 253 attested ones; RISC-V 255.

`proved`
- for one arch-opcode and one language: source in that language which,
  compiled at shipping settings and read back into logic, z3 confirms
  equal to the machine's definition for every input. The definition is
  the Sail model (RISC-V) or the corrected reference checked against
  the K-framework reading (x86).
- `destination` reading: the answer register is proved. `strict`: every
  written place, flags included. RISC-V has no flags, so its two
  readings coincide.

`agreed`
- for an interpreted language: the same source run beside the
  definition at test points, edge values first. Evidence, never proof;
  no machine body exists to check.

`expressible in y`
- a real compiled unit of language x whose every arch-opcode is proved
  on y, so the whole unit could be rewritten in y out of proved pieces.

`discipline row`
- one of the eight divergence classes of the PCv5 study (full path in
  §9), each with a disposition: Wrap (a polyfill), Forbid (a rule), or
  a capability flag.

`border verdict`
- the PCv7 border grammar's three-way verdict on a value crossing a
  frame: identical, convertible, incompatible.

## §2. Proved arch-opcodes per language (any route: the language's own operator, the backstop, z3's circuits)

| language | x86, destination | x86, strict | of | RISC-V | of | source |
|---|---|---|---|---|---|---|
| c | 207 | 168 | 253 | 243 | 255 | log_269, log_267 |
| c++ | 229 | 197 | 253 | 243 | 255 | log_269, log_267 |
| rust | 176 | 138 | 253 | 247 | 255 | log_269, log_267 |
| go | 164 | 119 | 253 | 241 | 255 | log_269, log_268 |
| swift | 167 | 124 | 253 | no RISC-V toolchain | 255 | log_269 |
| on at least one compiled language | 233 | 201 | 253 | 251 | 255 | |
| on every compiled language | 154 | 111 | 253 | 235 | 255 | |

Interpreted languages, x86, `agreed`: python, php, ruby, javascript,
dart, c# 166 of 253 each; java 162; all seven 162 of 253 (log_269).

## §3. How far the proofs reach: real units expressible per language pair

RISC-V, populations c 369 units and go 105 (log_266):

| from \ into | c | c++ | go | rust |
|---|---|---|---|---|
| c | 351 of 369 | 351 | 349 | 369 |
| go | 100 of 105 | 100 | 102 | 105 |

x86, destination reading, populations c 10,367; c++ 17,569; rust 685;
go 577; swift 1,229 (log_266):

| from \ into | c | c++ | rust | go | swift |
|---|---|---|---|---|---|
| c | 4,578 of 10,367 | 4,578 | 4,152 | 3,887 | 3,504 |
| c++ | 7,631 of 17,569 | 7,631 | 7,056 | 6,647 | 5,928 |
| rust | 489 of 685 | 489 | 489 | 489 | 489 |
| go | 157 of 577 | 157 | 157 | 153 | 157 |
| swift | 237 of 1,229 | 237 | 237 | 226 | 237 |

## §4. What blocks the rest, and what kind of thing each blocker is

| blocker, x86 | units it sinks (c corpus) | kind | where it belongs |
|---|---|---|---|
| `cmp`, `test` | 1,354 and 903 | writes only flags, no answer register | a compare feeding a branch: a border crossing, not an operator |
| `push` | 1,251 | the stack | calling convention: a border crossing |
| `movslq` | 1,400 (into swift) | a widening move | the arrival contract: a `convertible` verdict |
| `setne` and the flag pairs | 1,772 (strict) | flag consumers | the same crossing, strict reading |
| RISC-V: divide, remainder, `czero.eqz` | 4 to 6 each | operator cells | the checker runs out; the lifter lacks two instructions |

Units of one to five instructions mostly pass; units over ten almost
never do, because one crossing sinks a unit (log_266 §5).

## §5. AutoPoly on the disciplines matrix

| discipline row | disposition (PCv5) | what AutoPoly supplies | status |
|---|---|---|---|
| 1 value-model | Wrap: self-hosted polyfills | the proved emulations, per language, against the machine definition | x86 154 of 253 on all five; RISC-V 235 of 255 on all four |
| 8 encoding | Wrap | not addressed by AutoPoly; a string polyfill | unchanged |
| 2 copy-model, 3 evaluation-order, 4 lifetime, 5 dispatch, 6 collection-order | Forbid: discipline rules | nothing; these are legislation the ingress enforces | unchanged, as designed |
| 7 concurrency | capability flag per target | nothing | unchanged |
| the border grammar | identical / convertible / incompatible | the bank already records the three: proved / proved under caller extension / refused at arrival | present under other names; not yet keyed by the lattice's names |
| dominance | the hub canon every language maps into with no semantic distance | the term, with equality decided by z3 | the canon is the machine definition itself |

## §6. What proven fidelity across all languages still needs, in order of units unblocked

| piece | what it is | unblocks |
|---|---|---|
| the flags-consumer contract | a compare and its branch proved as one hub `if` | `cmp`, `test`, `setne`: the top blocker in every x86 pair |
| the calling convention as hub structure | how values arrive, answer, and use the frame | `push`, `movslq`, the arrival refusals |
| the branch-following walk | reading a compiled `if` correctly on RISC-V | the disproofs that are reading errors |
| the last operator cells | 64-bit multiply-high and divides, x87, packed compares | the remaining 4 RISC-V and about 20 x86 arch-opcodes |
| swift on RISC-V | a toolchain install | the fifth RISC-V column |
| the interpreted seven | no machine body: agreement only | none by this method |

## §7. The four anchors

| anchor | one line |
|---|---|
| the research | the Wrap row of the disciplines matrix is now proved, not authored, for 154 of 253 x86 and 235 of 255 RISC-V arch-opcodes on every compiled language |
| mine next | the flags-consumer contract and the calling convention as hub structure, each a brief; the bank keyed by the lattice's three verdict names |
| yours | the two rulings of the plan: where the pipeline lives (PseudoIR as drawn), and the exchange node's added clause; restoring `PRIVATE/PseudoCoup_v5/Designing/` from that repo's history so the intention tables are readable |
| theirs | the other conversation: the daemon restart that splits the two oversized files |

## §8. Decided, recorded for audit / awaiting the owner

Decided: every table row carries its population; the destination
reading is the standard and strict is shown beside it; interpreted
agreement is never counted as proof; all numbers from logs 262, 264,
265, 266, 267, 268, 269 and the PCv5 divergence study.

Awaiting the owner: the two plan rulings above; whether the bank's verdicts
are renamed to the border grammar's three.

## §9. Pointers, by full path

- the disciplines: `0_Archive/PyHaxe/README.md` (the
  discipline: required, forbidden, wrapper, allowed);
  `0_Archive/PseudoDart/DISCIPLINE.md`;
  `PUBLIC/PseudoCoup/README.md` (the universal
  discipline: Map, Wrap, Fail).
- the eight divergence classes with their dispositions, and PCv7's
  border grammar:
  `PRIVATE/PseudoCoup_v5/DevComms/language_divergence_study_log.md`
- the intention tables and verdicts are named in
  `PRIVATE/PseudoCoup_v5/DevComms/project_state.md`; the
  files lived under `PRIVATE/PseudoCoup_v5/Designing/`
  (gutted 2026-07-31; in that repo's history under
  `PCv5-archived-research`).
- the measurements: `PRIVATE/PseudoCoupHQ/DevComms/`,
  logs 262, 264, 265, 266, 267, 268, 269 (each file name begins
  `log_<number>_`).
- the per-cell verdicts:
  `PRIVATE/PseudoCoupHQ/Research/oracle/coverage/bank_x86.json`
  and `bank_riscv64.json` in the same folder.
- the next brief:
  `PRIVATE/PseudoCoupHQ/Research/briefs/task_cov2_brief.md`
- the code-level companion, what one can code with:
  `PRIVATE/PseudoCoupHQ/DevComms/log_271_what_you_can_code_with_today.md`
