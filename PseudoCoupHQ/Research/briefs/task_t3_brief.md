# Task t3 — named intermediates in the renderers, the x87 arrival as words, the tier on the code version: what opens the divider, the softfloats and the x87 family

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it (waits in short
calls). Then `task_t2_brief.md` and its log `DevComms/log_257` (§"Awaiting
the owner" 1–5 are this task's inputs; `construct/lean/OWED.md`), `task_ref2_brief.md`
and its log (ref2 runs BEFORE this task: the reference is corrected and
the stores re-derived; every term text you meet is the new one), the
renderers (`emulate.py` and the four subclasses), `Research/op_pipeline/lean/term_to_lean.py`,
`construct/schemas.py`, `construct/construct.py`, `handful.code_version`.
Instance `t3.conf`. Artifact folder: `.../emulation/` (the renderers,
`construct/`), lanes under `construct/lanes_t3/`.

## 1. What this is
t2 built the second tier and proved 14 places by Lean lemma; the compiler
collapsed none (LANDED 0 of 14). Three named things stop the rest, and
they are mechanical, not a ruling:
| blocker (log_257) | the change | where | guard |
|---|---|---|---|
| the renderers print ONE nested expression: a step that reads its previous step three times is written 3^width times, so a divider, a softfloat, any iterated schema cannot be rendered or stated | render a term as a SEQUENCE of named intermediates (`let`/`const` per sub-term the term walk shares; a local variable in c/cpp/rust/go/swift; `let` in the Lean statement), sharing every sub-term that occurs more than once — the term is a DAG and is printed as one | `emulate.py` (the base `Renderer`, so every subclass inherits it), `term_to_lean.py` | every certificate's source re-rendered: the compiled body's carve and gate verdict unchanged on the 5% audit; sources shrink — report the size distribution before → after; the L2 check 259/172/87 (ref2's new tally if it changed) unchanged |
| the x87 family, 129 of t2's 149, refused at the arrival or answer home | an 80-bit arrival/answer is stated as TWO integer words (64 + 16, the significand and the sign-exponent), which the constructed schema reads and writes as integers; the gate reassembles: `X87_k == Concat(hi16, lo64)` on the region the certificate names — a contract stated by a constraint, in the spirit of the ruling of 2026-09-09 | the driver's contract (not `ledger.py`) | rust/go/swift's x87 cells before → after; `long double` on c/cpp unchanged |
| the tier's source is not in `code_version`, so a tier change forces a full pass; and (ref2, log_261) the bank's re-attempt rule hashes the driver, the loop and the renderer but NOT `reference.py`/`condition_table.py`, so a corrected reference would hold back every key it changed | `construct/*.py`, the schema lemmas' sources, AND `reference.py` + `condition_table.py` join `handful.code_version` (an existing field's definition, not a new field) | driver | the next pass is a DELTA: runs and seconds beside t2's 669 / 2,301 s |
| the product's high half has no proof | write the algebraic statement of `OWED.md` §2 in Lean and attempt it; if it does not close, the cost and where it stops, LITERAL, and the `mulh` places stay refused by cause | `construct/lean/` | the count of `mul`/`imul` gpr_one places proved before → after |

## 2. Then the tier's pass, as a delta
Both routes per uncertified place; the collapse column per constructed
certificate (LANDED / NOT_COLLAPSED and the instruction count) — the owner's
question "can the c compiler simplify the constructions" measured on the
larger population; the proof-form counts; the three readings beside t2's.
Guard over every json; log (next free number); verifier lane; PROGRESS on
the autopoly node and the lean node; sync-back; instance down. Memory
bound 6g, sample 20, peak RSS, abort `ABORT_MEMORY_T3`; z3 30 s hard.
Shared files this brief authorises: `emulate.py` (the base renderer's
printing), `term_to_lean.py` (the statement's `let`), and nothing under
`Research/op_pipeline/` besides that one file. Never delete anything under
`<runs>/` or `PUBLIC/Airlock/`. Reply with the four guards,
the size distribution, the x87 before → after, the delta's cost line, the
collapse counts, the three readings, the tally, the two lists.
