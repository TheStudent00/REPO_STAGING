# log_118 — TASK 30, designated memory, the park-reload idiom, and the arrival-mode dimension

**Role:** Claude Code implementer, TASK 30 of
`log_115_claude_code_task_briefs_round6.md`. Date: 2026-09-01. No
sub-agents used — every artifact below was built and run directly in
this session with `/tmp/reconnect_venv/bin/python3`.

**Evidence class is stated per claim.** Every "I verified X" sentence
pastes the command and its output.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line — not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate set
for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention — never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 — the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

---

# 1. What happened

## 1.1 The counts, before anything else

- **36 of the 74 not-converged units now carry canonical text and are
  PROVED EQUAL to their own ship code.** Zero DISPROVED. The
  remaining 38 refuse by name: 28 at the rendering stage, 10 at the
  checker's own boundary.
- **All 8 units your brief named are among the 36** — cpp/op_765,
  cpp/op_770, rust/op_642, rust/op_649, rust/op_678, rust/op_685,
  swift/op_703, swift/op_739.
- **The 12 own-frame units log_117's survey named were checked.** Six
  of them (c/op_30, c/op_33, c/op_34, cpp/op_42, cpp/op_45,
  cpp/op_46) were already converged and were never in this
  population; the other six (c/op_31, c/op_32, c/op_35, cpp/op_43,
  cpp/op_44, cpp/op_47) were in it and all six now prove.
- **Nothing was advanced.** The 36 proofs exist; no recorded status
  was rewritten. §6 states what the counts WOULD become.

## 1.2 The one thing your brief got wrong, stated first because it
## changes how the rest reads

Your brief says of the refusal: *"NOTE the refusal fires against the
ANCHOR build and its message does not say which build — fix that
labelling in your new code."*

**It fires against the SHIP build.** Measured over all 1,779 compiled
units, not sampled:

```
$ /tmp/reconnect_venv/bin/python3 canon33_designated.py
STEP 1 -- WHICH BUILD IS THE RECORD DERIVED FROM
   sem_anchored `mnem` compared line-by-line with op_units `ship.mnem`:
      identical : 1779
      different : 0 []
      no probe record : 0
   so the text every refusal in this line fired against is the SHIP build, not the anchor build.
```

- Evidence class: **forced by construction** — `canon4.py` reads
  `sem_anchored_<lang>.json`'s `mnem`, and that field is line-identical
  to `op_units_<lang>.json`'s own `probes[n]["ship"]["mnem"]` for
  every one of the 1,779.
- The labelling fix you asked for is done anyway, and is now
  worth more than a label: **every refusal this lap's code emits names
  the build in its own text** — "of the unit's own SHIP build".

## 1.3 What was actually blocking the 22 units, in plain words

The refusal text was `two stack-spilled operands in one instruction`.
It names one thing. It was hiding two, and neither is about memory
being unsupported.

- **The count was wrong.** The test counted operand pieces that do not
  begin with `%`. An IMMEDIATE does not begin with `%`. So
  `and $0x1,-0x8(%rsp)` — one memory operand, a legal instruction —
  was counted as two and the whole unit was refused.
- **The pool was two registers deep.** `canon.py`'s `TEMPS` is
  `["r10", "r11"]` and `VECTOR_TEMPS` is `["xmm2", "xmm3"]`. Your
  2026-08-28 ruling ("TEMP REGISTERS ARE STANDARDIZED, NOT LIMITED")
  had been applied in `canon7_render.py` and never in this path, so a
  unit with nine live values pushed seven of them to stack homes and
  then met two of them in one instruction.

---

# 2. Designated memory, with values in motion

## 2.1 The names, glossed before use

- **A designated location** is a standardized virtual slot named
  `S0`, `S1`, … — a designation, exactly as `a` is a designation and
  `%rdi` is the register it maps to.
- **The directory** is the map designation → slot: which slot holds
  which designation, at which real stack offset.
- **Parking** is writing a value into its designated location.
  **Reloading** is reading it back into a register for the length of
  one instruction. **Re-parking** is writing the result back.
- **The reload registers** are `%r11`/`%r10` (general file) and
  `%xmm15`/`%xmm14` (vector file), held out of the value pools so no
  live value can ever occupy them.

## 2.2 The scheme

- Slot `i` is at `-0x%x(%rsp)` for `8*(i+1)`: `-0x8(%rsp)`,
  `-0x10(%rsp)`, `-0x18(%rsp)`, … Eight bytes each, growing down from
  the stack pointer.
- **They are runnable with no prologue** because the first 16 land
  inside the System V 128-byte red zone. A unit needing a 17th is
  REFUSED BY NAME (`RedZoneExhausted`), not silently emitted. Six go
  units hit exactly that this lap and are refused (§5.2).
- **The value pools are the ratified ORDER, not a pair.**
  `designated_memory.py` carries
  `["r9","r8","rbx","r12","r13","r14","r15"]` and `xmm2 … xmm13` —
  `canon7_render.py`'s own recorded pool order with the two reload
  registers removed.
- A designation is assigned exactly once per unit and never
  reassigned, which is the rule the register bench already obeyed.

## 2.3 The park-reload idiom, walked with real values

Take `cpp/op_765` at the point where its ninth live value has already
overflowed. The erased form says `answer = cmovbe(u7, u8)` where `u8`
lives in designation `S2` (`-0x20(%rsp)`) and `u7` lives in `S1`
(`-0x18(%rsp)`).

- **What x86-64 will not encode.** `cmovbe` has no memory-destination
  form at all, and no instruction may carry two memory operands. The
  old code met this and refused the unit.
- **What the compilers themselves do**, and what this lap does: bring
  the values into registers for the length of one instruction.

```
  WHAT THE ERASED FORM SAYS
      answer = cmovbe(u7, u8)          u7 in S1, u8 in S2

  WHAT IS EMITTED (measured, from canon33_units.json's own record)
      mov -0x18(%rsp),%r10d            reload the SOURCE   (S1 -> reload register 1)
      mov -0x20(%rsp),%r11d            reload the DESTINATION (S2 -> reload register 0)
      cmovbe %r10d,%r11d               the instruction, both operands now registers
      mov %r11d,-0x20(%rsp)            re-park the result into S2
```

- **Why the destination is reloaded FIRST and not merely written.**
  `cmovbe` is conditional: when its condition is false it leaves the
  destination untouched. If `%r11d` were not loaded with S2's current
  value first, the false case would re-park whatever happened to be in
  `%r11d`. The reload is emitted only when the step's own record says
  `write_kind == "rw"`; for a plain `def` write (e.g.
  `mov $0xff,%r11d ; mov %r11d,-0x20(%rsp)`) it is not.
- **Flags are safe.** Every line added is a `mov`-family load or
  store, and no x86-64 `mov` writes the flags — so an instruction that
  sets flags for a later branch is never separated from that branch by
  something that changes them.
- **Two reload registers, not one, and why.** Reload register 0 always
  serves the destination, register 1 always serves the source. The
  order is fixed so two units of the same shape render the same text.
  The second register was added when this exact instruction was
  measured: with one register the pass refused by name ("both the
  destination and a source … one reload register cannot serve both").

## 2.4 What the directory records

`designated_memory.Directory.directory()` returns, per designation:

```
  "S2": {"designation": "S2", "slot_index": 2, "offset": -32,
         "text": "-0x20(%rsp)", "file": "general", "holds": "u8"}
```

- `holds` is the erased-form value name that owns the designation for
  the whole unit.
- The scheme is documented in full in the header of
  `designated_memory.py`, as your brief requires.

---

# 3. The mechanism, and why canon4.py was not edited

## 3.1 The rule: new files only, and a machine-made copy

- The park-reload rule is one change inside two long functions that
  already exist and are already gate-proved on 1,635 units:
  `canon4.py`'s `derive_runnable3` and `derive_block_body`.
- **`parkload_derive.py` is MACHINE-COPIED from `canon4.py`'s own
  source text** by `parkload_make.py`, which applies named literal
  edits and REFUSES to write if any edit no longer matches its source.
  A reviewer can therefore tell an intended edit from a transcription
  slip, which a hand copy would not allow.
- The generator prints its own proof that it did not touch its source:

```
$ /tmp/reconnect_venv/bin/python3 parkload_make.py
EDIT 3 (the answer move's width) applied
EDIT 4a (step index) applied
EDIT 4b (in-place clobber, straight line) applied
EDIT 5a (sign-extend width) applied
EDIT 5b (dividend width) applied
EDIT 4c (step index) applied
EDIT 4d (in-place clobber, per block) applied
EDIT 5c (sign-extend width) applied
EDIT 5d (dividend width) applied
EDIT 1 (derive_runnable3)  applied
EDIT 2 (derive_block_body) applied
wrote parkload_derive.py -- 37114 bytes
canon4.py sha256 before: b2c43a2ff45729fefc704fdc0a1b9b99cf17b8ba06a899086e628e45fcb8243d
canon4.py sha256 after:  b2c43a2ff45729fefc704fdc0a1b9b99cf17b8ba06a899086e628e45fcb8243d
canon4.py UNCHANGED (opened read-only)
```

## 3.2 How the new deriving half is installed

- `canon33_designated.py`'s `Rebound` context manager rebinds four of
  `canon4`'s module globals **in its own process only** — `Bench`,
  `derive_runnable3`, `derive_block_body`, `dead_mov_cleanup`,
  `render_control_line` — and restores them on exit. All of canon4's
  block cutting, contract building and control-line machinery is
  reused unchanged; only the deriving half is this lap's.
- The driver prints canon4.py's sha256 before and after its whole run;
  both runs above report `canon4.py UNCHANGED: True`.

## 3.3 Four more causes, found because these units finally reached a
## gate

Each of these was already in canon4's deriving pass. None could be
SEEN before, because every unit that exposes them was refused earlier,
at the two-parked-operands rule, and never reached a gate. Each was
fixed at first observation (AgentMemory, 2026-08-28), and each is
named here with the measurement that exposed it.

### 3.3.1 CAUSE 1 — a fall-through block emitted no jump while the
### blocks were reordered

- canon4 emits a unit's blocks in the order its path walk discovered
  them, which is not their address order (it cannot be: one block can
  be rendered several times, once per incoming path). A block ending
  in a conditional branch is safe — canon4 already makes both edges
  explicit. A block with NO control instruction was given nothing.
- **MEASURED on `cpp/op_765`.** Its real ship code runs L0, L1, L2, L3
  in address order; the walk discovered L0, L2, L1, L3. L2 ends with
  `addss` and no control instruction, so in the rendered text it fell
  into L1 — which recomputes the conversion and throws L2's work away.
- **The gate caught it**, with a counterexample, before any claim was
  made. Fixed in `canon33_fixes.render_control_line33`: a block with
  no control instruction and exactly one successor emits
  `jmp <that successor>`, using the label canon4's own walk already
  recorded.

### 3.3.2 CAUSE 2 — the dead-mov cleanup was alias-blind

- canon4's `dead_mov_cleanup` deletes a `mov` whose destination text
  does not appear again later. It compares SPELLINGS. `%rcx`, `%ecx`,
  `%cx` and `%cl` are four spellings of one register.
- **MEASURED on `swift/op_703`.** A variable shift count is
  hardware-pinned to `%cl`, so the pass emits `mov %esi,%ecx` and the
  shift then reads `%cl`. The cleanup searched later text for the
  literal `%ecx`, did not find it, and deleted the mov — leaving the
  shift reading whatever was in `%cl`. The gate DISPROVED it with
  `b = 64`, `%cl = 8`.
- Fixed by resolving the destination to its family (canon.py's own
  `FAMILY_OF`) and looking for ANY spelling of that family
  (canon.py's own `GP_NAMES` row).

### 3.3.3 CAUSE 3 — the answer move was always 32 bits

- Both return paths landed the finished value in the answer register
  with a move rendered at width index 1 — the 32-bit alias — whatever
  the answer's width. A 64-bit answer was truncated: the unit computed
  the right value and returned the wrong one.
- **MEASURED on `swift/op_703`**, whose answer is a 64-bit shifted
  value. DISPROVED with `b = 11`, `a = 4914318053212165` — an answer
  above 2^32, exactly where the truncation shows.
- Fixed by rendering that move at the 64-bit alias. This is never
  worse: a value written by a 32-bit instruction already has zeroes
  above bit 31 on x86-64, so the wide move carries exactly what the
  narrow one carried.

### 3.3.4 CAUSE 4 — an in-place write clobbered a still-live value

- An instruction that reads and writes one operand was rendered on top
  of the value it reads, even when a later step still reads that
  value.
- **MEASURED on `cpp/op_765`.** The erased form is
  `u0 = shr(a) ; u1 = and(a) ; u2 = or(u0,u1)`. The rendering put
  `u0` in `a`'s own register: `shr $1,%rdi` destroyed `a`, and the
  next line's `and $0x1,%edi` then read the shifted value instead of
  `a`.
- Fixed by `preserve_if_live`: when the old value is read by a later
  step — or is a contract value (`a`/`b`), which a later BLOCK this
  function cannot see may read — it is copied to a fresh home first.
  That is the same shape the compiler itself emitted:
  `mov %rdi,%rax ; shr $1,%rax`.

### 3.3.5 CAUSE 5 — the divide family's widths were fixed at 32 bits

- The dividend was moved into the answer register with a 32-bit move
  before every sign-extend, and the two dividend halves were ensured
  at 32 bits before every divide.
- **MEASURED on `rust/op_649`**, a 64-bit divide (`cqto` +
  `idiv %rsi`): the candidate said `mov %edi,%eax` where the ship code
  says `mov %rdi,%rax`. DISPROVED with `b = 1`,
  `a = 10990797176293339890`.
- Fixed by reading the width from the sign-extend mnemonic
  (`cltd` → 32, `cqto` → 64) and from the step's own recorded divisor
  width. An unrecorded sign-extend mnemonic refuses by name.

---

# 4. The gate

## 4.1 Why the existing gate could not be used unchanged

`canon10_behaviour_check.Sim10` models register families only. A
designated location reaches `width_of_operand` and is refused as an
unknown register spelling. Four table gaps were fixed in
`canon33_gate.py`, in a SUBCLASS, with
`canon10_behaviour_check.py` and everything below it imported and
unchanged (§6.3 pastes their sha256s).

## 4.2 GAP 1 — the designated-location store

- A slot is a value written by a store and read back by a load, keyed
  by the slot's own text. **Exact, not uninterpreted.**
- **Its soundness rests on a property the renderer guarantees**, not
  on an assumption: `parkload_derive.py` emits a designated location
  in exactly two shapes, `mov <reg>,<slot>` and `mov <slot>,<reg>`.
  Nothing else ever names a slot, so there is no aliasing question.
  Sim33 refuses by name if a slot appears anywhere else.
- A slot read before it is written takes a shared symbolic seed keyed
  by the slot text, exactly as an unwritten register family does, so
  both texts start from the same unconstrained value.

## 4.3 GAP 2 — `lea` with a displacement, and `lea` is not a load

- canon5's Sim models only the plain `(base,index,scale)` form and
  refused `-0x41(%rsi)` by name. The displacement form is ordinary
  exact arithmetic and is modelled here.
- **`lea` READS NO MEMORY.** Its memory-shaped operand is an address
  computation. Sim33 therefore handles `lea` BEFORE the slot check, so
  a stack-relative operand inside a `lea` is never mistaken for a
  designated location. Measured: that mistake alone was refusing six
  own-frame units (c/op_31, c/op_32, c/op_35, cpp/op_43, cpp/op_44,
  cpp/op_47), all six of which prove once it is corrected.

## 4.4 GAP 3 — the rip guard was wider than its own argument

- The guard refuses when the ordered list of rip-relative-operand
  mnemonics differs between two texts, because positional keying of
  constants would be unsound. A path-duplicating canonical text
  renders one trap block twice, which changes that list without
  changing any constant.
- The NARROWED guard drops only the lines whose constant cannot reach
  an answer: a `call` through a rip-relative operand (the walker
  raises Trap on every `call`), and a `lea <rip>,<reg>` IMMEDIATELY
  FOLLOWED by a `call` (the trapping call's own argument). Everything
  else is still compared, in order.
- Control 4 exercises the narrowing in both directions (§5.4).

## 4.5 GAP 4 — the trapping call's argument

- `neutralize_trap_arguments` rewrites `lea <rip-relative>,<register>`
  to `mov $0x0,<register>` when the very next line of the same block
  is a `call`, applied IDENTICALLY to the real text and the candidate.
- **Why it is sound and not a convenience.** The walker raises Trap on
  every `call`, so execution of that block stops at the next line and
  the register just written is never read by anything. Any value at
  all may be written there without changing a single answer.
- Without it the checker refused four rust units by name, about a
  value that provably cannot matter.

---

# 5. The controls

A gate that accepts everything proves nothing. Four controls,
`canon33_controls.py`. Evidence class: **tool testimony,
reproducible.**

```
$ /tmp/reconnect_venv/bin/python3 canon33_controls.py
CONTROL 1 (negative, mutation) over 36 accepted units
   {'applied': 107, 'rejected': 96, 'still_proved': 11, 'not_applicable': 73, 'units_with_a_rejection': 36, 'units_with_no_rejection': 0}
   NOTE ON SURVIVORS.  A mutation that STILL proves equal to the unit's own real ship code is not a gate failure: z3 has just proved the mutant computes the same answers, so the mutant is another correct canonical text (measured: the flipped constant is a trapping call's argument, or a guard bound the later guards already cover).  The control's question is whether the gate is LIVE on each unit, which is the units_with_a_rejection count.
   PASS -- every one of the 36 accepted units rejected at least one mutation of its own text

CONTROL 2 (positive, real against real)
   {'tested': 36, 'proved': 36, 'not_proved': 0}
   PASS -- every unit's own ship text proves equal to itself

CONTROL 3 (the designated-location model is not vacuous)
   parking in S0 and reading back S1: DISPROVED
   PASS -- the slot store distinguishes two designated locations

CONTROL 4 (the narrowed rip guard)
   duplicated trap path passes the guard: True
   differing data constants still refused: True
   PASS -- the narrowing is exactly as wide as its own argument

wrote canon33_controls.json
```

## 5.1 What each control answers

- **Control 1** mutates every accepted text five ways —
  swap two register operands, delete one instruction, flip an
  immediate, retarget one branch, narrow the answer move back to 32
  bits (the shape CAUSE 3 fixed) — and re-runs the IDENTICAL gate.
- **The 11 survivors are named and disposed of, not waved away.** A
  mutant that still proves equal to the unit's own ship code has just
  been proved by z3 to compute the same answers; it is another correct
  canonical text, not an acceptance the gate should have refused. They
  are the flipped constants of trapping calls, and one guard bound the
  later guards already cover. The control's real question — is the
  gate live on each unit — is answered by
  `units_with_no_rejection: 0`.
- **Control 2** is what makes a DISPROVED verdict a statement about a
  candidate rather than about the checker. For a block-structured
  unit the ship text is cut into its own real blocks first, the same
  cut the gate itself uses, so like is compared with like.
- **Control 3** would pass trivially if the slot store were ignored or
  uninterpreted: parking in S0 and reading back S1 is DISPROVED, so
  the store distinguishes two designated locations.
- **Control 4** shows the rip-guard narrowing is exactly as wide as
  its own argument.

## 5.2 The 38 that did not converge, by named cause

| count | outcome | cause |
|---|---|---|
| 16 | refused at rendering | a branch target address could not be resolved to any walked block (a tail jump outside the unit's own block set) |
| 6 | refused at rendering | the unit needs designated location S16, below the red zone this canonical form relies on — go/op_30 … go/op_35 |
| 5 | refused at rendering | log_117's five sret units; this path does not anchor them and does not pretend to — they are proved in log_117 by the three-seat contract |
| 1 | refused at rendering | value `w0` is read before it is defined or before the entry contract names it |
| 7 | undecided at the gate | mnemonic `sbb` has no symbolic model in this checker |
| 3 | undecided at the gate | the unit's own real ship code never writes `%xmm0` or an rax-family register, so no answer home can be read off the ground truth |
| **38** | | |

- **The 6 go units are a genuine finding, not a shrug.** They need
  more than sixteen 8-byte designated locations, which means their
  path duplication is producing more simultaneously-live values than
  the red zone holds. A frame would make them runnable; whether the
  canonical form should ever carry a prologue is your call, not a
  mechanical detail (§8.2).
- **`sbb` is the next mechanical table gap** and it is named here
  once, with its size (7 units), rather than carried as a recurring
  line.

---

# 6. Zero regressions

## 6.1 The baseline, stated precisely and not flattened

- **RECORDED converged: 1,635** — what the `status` field of
  `canon31_units_<lang>.json` says.
- **HONEST standing converged: 1,622** — after log_112's branching
  audit re-gated 18 recorded-converged branching units and 13 did not
  re-prove.
- **The 13 withdrawn are a SEPARATE POPULATION**, not a subtraction
  folded into one number.
- **log_117's 5 sret proofs are NOT advanced** — your call, still
  open. They are not counted anywhere below.

## 6.2 The check, recomputed from disk

```
$ /tmp/reconnect_venv/bin/python3 canon33_zero_regression.py
recorded converged, recomputed from disk, per language:
   c         583  (plus 20 unchanged)
   cpp       728  (plus 22 unchanged)
   go         72  (plus 16 unchanged)
   rust      112  (plus 2 unchanged)
   swift     140  (plus 10 unchanged)
   TOTAL    1635
withdrawn by log_112's branching audit (recorded converged, re-gate did not prove): 13
honest standing converged: 1622
converged-or-unchanged: 1705

units this lap re-derived: 74
of those, recorded statuses rewritten by this lap: 0 []
this lap's outcomes: {'newly_converged': 36, 'undecided': 10, 'still_refused': 28}

IF the 36 newly proved units were advanced -- NOT done here, it is a call about the record --
   recorded converged would become 1671
   honest standing would become     1658
   converged-or-unchanged would become 1741
   the not-converged remainder would become 38

sha256 of every shared module this lap imported and did not edit:
   canon.py                         f9f04f6a5bdae952d192f7041144ab078349d60cd2378875e70d28824b730665
   canon2.py                        10b6fc7e8f52ff9ae0a3436254e241639e66d838d250feeb995b9a38e62b10a3
   canon4.py                        b2c43a2ff45729fefc704fdc0a1b9b99cf17b8ba06a899086e628e45fcb8243d
   canon5_behaviour_check.py        043d5f43bc214e95b5639973c06ccfb2e1d7feab9f67ca58019c5835d879ea36
   canon8_behaviour_check.py        726d73d9775e18af9caa93eb410a49333d730fe06ef15f37a63d81312bedcf23
   canon10_behaviour_check.py       944c1caee7571c2a3291ca529914c958a16d4d3392437afd9282c9dd78e3f7f0
   real_blocks.py                   16bfee2deecb5f6570648c2a17cd7580d0ab728cd7f5b65d8ba8a1321c0b206a
   check_no_spelling_keys.py        a377462b38e8610d8bb60ac668f0a5adc72ee571d15efab85e40a9afdaa511f7

ZERO-REGRESSION CHECK: PASS
wrote canon33_zero_regression.json
```

## 6.3 The write-claim, checked against the vcs and not against the
## files

The daemon commits every 30 seconds, so `git status` is clean and
proves nothing; the history is what proves it. This session began at
16:39. Everything under `Research/op_pipeline` committed since 16:00:

```
$ cd ~/Programming/PseudoCoupHQ && git log --since="16:00" --name-status --pretty=format:'' -- Research/op_pipeline | grep -E '^[AM]' | awk '{print $2}' | sort -u
Research/op_pipeline/arrival_modes.py
Research/op_pipeline/canon32_sret_controls.json
Research/op_pipeline/canon32_sret_controls.py
Research/op_pipeline/canon32_sret.py
Research/op_pipeline/canon32_sret_survey.json
Research/op_pipeline/canon32_sret_units.json
Research/op_pipeline/canon32_zero_regression.json
Research/op_pipeline/canon32_zero_regression.py
Research/op_pipeline/canon33_arrival_modes.json
Research/op_pipeline/canon33_controls.json
Research/op_pipeline/canon33_controls.py
Research/op_pipeline/canon33_designated.py
Research/op_pipeline/canon33_fixes.py
Research/op_pipeline/canon33_gate.py
Research/op_pipeline/canon33_guard.py
Research/op_pipeline/canon33_pointer_modes.py
Research/op_pipeline/canon33_units.json
Research/op_pipeline/canon33_zero_regression.json
Research/op_pipeline/canon33_zero_regression.py
Research/op_pipeline/designated_memory.py
Research/op_pipeline/entry_contract3.py
Research/op_pipeline/parkload_derive.py
Research/op_pipeline/parkload_make.py
Research/op_pipeline/sret_gate.py
Research/op_pipeline/sret_render.py
Research/op_pipeline/type_inventory.json
Research/op_pipeline/type_inventory.md
Research/op_pipeline/type_inventory.py
Research/op_pipeline/type_inventory_validate.py
Research/op_pipeline/type_inventory_validation.json
Research/op_pipeline/type_inventory_validation.md
```

- **Not one shared pipeline file is in that list.** The `canon32_*` /
  `sret_*` / `entry_contract3.py` entries are TASK 31's and the
  `type_inventory*` entries are TASK 29's; they are named here for
  honesty about what else landed in the same window, not claimed as
  this lap's work.
- **A caution about a wider window, checked rather than assumed.** A
  six-hour window DOES show `canon10_behaviour_check.py`,
  `real_blocks.py`, `canon31_units_*.json` and `lineage_carve.py` as
  modified. Their commits are timestamped 11:47–11:54, hours before
  this session opened at 16:39, and none was touched after 16:00.
  Checking the vcs rather than the file state is what distinguishes
  those two readings.
- **No table was rebuilt.** `dominant_table24` / `dom_ops22` were not
  opened by any program in this lap.

---

# 7. The arrival-mode dimension (your brief's part c)

## 7.1 The vocabulary, and where it comes from

Three names, and no fourth is invented:

- **plain** — the operand arrives AS ITS VALUE in its seat.
- **typed-pointer(T)** — the operand arrives as the ADDRESS of a T;
  the value is behind one or more field reads.
- **tagged** — the operand arrives as a machine word that is sometimes
  a value and sometimes a pointer, told apart by bits of the word
  itself.

## 7.2 For compiled units the mode is MEASURED, not asserted

Your brief says compiled units are plain. This lap does not take that
on faith; it measures it on each unit's own ship text and reports
every unit that is not.

- **The test:** an argument's arrival register is DEREFERENCED by the
  unit — it appears inside a memory operand — before anything in the
  unit writes that register.
- **`lea` is excluded**, and the exclusion is the whole reason the
  test is a measurement rather than a coincidence counter. `lea`
  computes an address and reads no memory;
  `lea (%rdi,%rsi,1),%eax` is the ordinary spelling of an integer
  addition on two plain values. Counting it reported 48 units as
  pointer-arrival units when 45 of them add two plain integers.
- **A register written by a `call` is excluded** for the same kind of
  reason: a dereference of `%rax` after a call is a dereference of the
  callee's result, not of an argument that arrived from outside. That
  exclusion removed nine go units that allocate through
  `runtime.newobject` — the same nine log_117 §4.3 named as the
  instructive negative for its own test.

```
$ /tmp/reconnect_venv/bin/python3 canon33_pointer_modes.py
STEP 1 -- the arrival mode of every compiled unit, measured on its own ship text
   plain                                    1776
   typed-pointer(i32)                       1
   typed-pointer(i64)                       1
   typed-pointer(u64)                       1
   TOTAL                                    1779
   compiled units that are NOT plain: 3 ['rust/op_786', 'rust/op_793', 'rust/op_800']
```

- **The three are exactly TASK 31's integer sret units**, found by a
  completely different test — this one knows nothing about stores,
  answer registers or result destinations; it only asks which arrival
  seats get dereferenced. Their recorded contract calls `%rdi` the
  value `a`; `%rdi` is in fact an address. **Two independent grounds
  agreeing** is the standing pattern (AgentMemory's evidence
  doctrine), and here they agree.
- The float pair `rust/op_807` and `rust/op_814` are correctly plain
  by this test: their two operands really do arrive in
  `%xmm0`/`%xmm1` as values, which is exactly why log_117's refusal
  text differed for them.

## 7.3 The interpreter handlers: recorded, then simplified or refused

```
STEP 2 -- the interpreter/JIT handlers' recorded arrival representation, and whether the simplification happened
   cpython/long_add                                     typed-pointer(PyLongObject*)       REFUSED
   php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER typed-pointer(zval*)               REFUSED
   php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER     typed-pointer(zval*)               REFUSED
   php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER          typed-pointer(zval*)               REFUSED
   php/add_function                                     typed-pointer(zval*)               REFUSED
   ruby/rb_big_plus                                     None                               REFUSED
   ruby/rb_fix_plus                                     tagged                             DONE
   ruby/rb_fix_plus_fix                                 None                               DONE
   ruby/rb_int_plus                                     tagged                             DONE
   ruby/vm_opt_plus                                     tagged                             REFUSED
   tally: {'tagged': 3, 'None': 2, 'typed-pointer(zval*)': 4, 'typed-pointer(PyLongObject*)': 1}
```

- **DONE means the second half of your ruling has actually happened**
  for that unit: the carve isolated a computation part and a canonical
  text was produced for it, so the unit is no longer a pointer unit —
  its recorded text is a value computation.
- **REFUSED means it has not**, and the refusal is quoted per unit in
  `canon33_arrival_modes.json` rather than smoothed over.
- **Two `None`s, and neither is forced.** `ruby/rb_big_plus`'s
  recorded representation is `"mixed: typed-pointer(RBignum*) +
  tagged-value(Fixnum)"` — it does not fit the three-name vocabulary
  and is NOT bent to fit; the row says so. `ruby/rb_fix_plus_fix` is
  an additional route symbol sliced for the proofs and has no row in
  the recorded representation column, so no mode is asserted for it.

## 7.4 The finding your ruling predicted, measured

```
STEP 3 -- proved-equal pairs, with their arrival modes side by side
   proved pairs examined: 24
   pairs whose arrival modes DIFFER: 24
      ruby/rb_fix_plus [tagged]
         simplified: mov %rsi,%rax; add %rdi,%rax; ret
      c/op_109 [plain]
         simplified: mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret
      ruby/rb_int_plus [tagged]
         simplified: mov %rdi,%rax; add %rsi,%rax; ret
      c/op_109 [plain]
         simplified: mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret
      ruby/rb_fix_plus_fix [None]
         simplified: mov %rsi,%rax; add %rdi,%rax; ret
      c/op_109 [plain]
         simplified: mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret
```

- **Every one of the 24 proved pairs differs in mode.** These are not
  new proofs — they are the PROVED relations already on record in
  `prove_interp_computation.json`, read read-only. What is new is the
  mode column beside them.
- **This is the shape your ruling named**: two units agreeing on the
  simplified instructions and differing in the recorded mode. The
  difference is recorded on every pair, in
  `canon33_arrival_modes.json`'s `mode_difference_findings`, and
  nothing is discarded.
- **The candidate set is machine-form throughout.** The pairs come
  from the existing proved-equality list; no token chose any of them.

---

# 8. The spelling guard, without exemption

`check_no_spelling_keys.py` grants a generator-provenance exemption to
a document whose top-level meta declares that role and which carries
no top-level grouping field. Your brief requires guards on everything
grouping-shaped or matching-shaped WITHOUT exemption, so
`canon33_guard.py` calls the checker's own `inventory` and `walk`
directly on every artifact, exemption bypassed.

```
$ /tmp/reconnect_venv/bin/python3 canon33_guard.py
PASS canon33_units.json -- no operator token in any key, grouping, pairing or row structure (checked IN FULL, the generator-provenance exemption deliberately bypassed)
PASS canon33_arrival_modes.json -- no operator token in any key, grouping, pairing or row structure (checked IN FULL, the generator-provenance exemption deliberately bypassed)
PASS canon33_controls.json -- no operator token in any key, grouping, pairing or row structure (checked IN FULL, the generator-provenance exemption deliberately bypassed)
PASS canon33_zero_regression.json -- no operator token in any key, grouping, pairing or row structure (checked IN FULL, the generator-provenance exemption deliberately bypassed)
ALL 4 ARTIFACTS PASS THE GUARD WITHOUT EXEMPTION
```

**The guard caught a violation in this lap's own output, and it is
recorded rather than quietly fixed.** An earlier draft of
`canon33_pointer_modes.py` put a `display_labels` dict on each
mode-difference finding, keyed by unit with the operator token as the
value. The guard refused it by name — 40 places — because a finding is
a PAIRING row and a token on a pairing row is exactly what the ban
forbids:

```
FAIL canon33_arrival_modes.json -- 40 spelling-keyed place(s), exemption bypassed
   ('$.mode_difference_findings[0].display_labels.c/op_109', "operator token '+' on a structure field -- this is a grouping/row key, not a per-unit label")
```

The token now stays where it belongs: once per unit, on that unit's
own row in the `compiled` / `interpreter` sections.

---

# 9. Two lists

## 9.1 Decided, recorded for audit (mechanical)

- Designated locations are named `S0`, `S1`, … at `-8*(i+1)(%rsp)`,
  assigned in first-needed order, one designation per value for the
  life of the unit, with a directory recording which value holds each.
- `%r11`/`%r10` (general) and `%xmm15`/`%xmm14` (vector) are reserved
  as the two reload registers per file and removed from the value
  pools; reload register 0 always serves a destination re-park,
  register 1 a source reload.
- Sixteen slots is the ceiling, because that is the red zone; a
  seventeenth refuses by name rather than emitting text that needs a
  frame.
- The park-reload idiom loads the destination first only when the
  step's own record says the instruction reads its destination.
- The five gate/render causes 1–5 in §3.3 and §4, each fixed at first
  observation with the measurement that exposed it.
- The rip guard is narrowed to the constants that can reach an answer;
  the trapping call's argument is neutralized identically on both
  sides.
- No recorded status was rewritten and no table was opened.

## 9.2 Awaiting the owner (kept minimal)

1. **Should the 36 be advanced to converged?** They are proved against
   their own ship code with four passing controls. Advancing them
   makes the counts 1,671 recorded / 1,658 honest, remainder 38. That
   is a call about the record, the same one log_117 left open for its
   5.
2. **May the canonical form carry a prologue?** Six go units need more
   than 16 designated locations. A `sub $N,%rsp` prologue plus its
   matching epilogue would make them runnable; today the form has no
   prologue and they refuse by name. This is an ontology question
   about the canonical form, not a mechanical detail.

---

# 10. Complete file inventory — every file created this lap

All new. No existing artifact was modified or deleted; §6.3 is the vcs
proof.

| file | bytes | what it is |
|---|---|---|
| `op_pipeline/designated_memory.py` | 9244 | the designated-location scheme: pools, designations, slot addresses, the directory, the reload registers; the scheme documented in the header |
| `op_pipeline/parkload_make.py` | 28618 | the generator: machine-copies canon4's two deriving functions and applies the named edits, refusing if any no longer matches |
| `op_pipeline/parkload_derive.py` | 39153 | MACHINE-GENERATED. the park-reload idiom and causes 3–5, over canon4's own copied source |
| `op_pipeline/canon33_fixes.py` | 8172 | causes 1 and 2: the fall-through jump and the alias-aware dead-mov cleanup |
| `op_pipeline/canon33_gate.py` | 16482 | Sim33 and the two gates: the designated-location store, the displacement `lea`, the narrowed rip guard, the trap-argument neutralizer |
| `op_pipeline/canon33_designated.py` | 13423 | the driver: ground-truth check, population, re-derive, assemble, gate, delta |
| `op_pipeline/arrival_modes.py` | 6773 | the three-name arrival vocabulary and the machine-form test for a compiled unit |
| `op_pipeline/canon33_pointer_modes.py` | 10856 | the arrival-mode driver: measure, read, and report the mode differences on proved pairs |
| `op_pipeline/canon33_controls.py` | 14007 | the four controls |
| `op_pipeline/canon33_guard.py` | 2225 | the spelling guard on every artifact, exemption bypassed |
| `op_pipeline/canon33_zero_regression.py` | 5693 | the baseline recount, the untouched-status check, the input hashes |
| `op_pipeline/canon33_units.json` | 68912 | the 74 units: old refusal, new outcome, candidate text, verdict, park-reload records |
| `op_pipeline/canon33_arrival_modes.json` | 957680 | the arrival mode of all 1,779 compiled units and 10 interpreter rows, plus the 24 mode-difference findings |
| `op_pipeline/canon33_controls.json` | 4821 | every mutation, its verdict, and the four control results |
| `op_pipeline/canon33_zero_regression.json` | 4278 | the recount and the input sha256 list |
| `DevComms/log_118_task30_designated_memory.md` | this file | the report |

Files opened READ-ONLY and unchanged: `canon.py`, `canon2.py`,
`canon4.py`, `canon5_behaviour_check.py`, `canon8_behaviour_check.py`,
`canon10_behaviour_check.py`, `real_blocks.py`,
`check_no_spelling_keys.py`, `canon4_units_<lang>.json`,
`canon31_units_<lang>.json`, `canon_units_<lang>.json`,
`op_units_<lang>.json`, `sem_anchored_<lang>.json`,
`sem_anchored_spill_<lang>.json`,
`proposal_representation_dimension3.json`,
`prove_interp_computation.json`.

---

# 11. Banking

The daemon commits and pushes every 30 seconds; every artifact above
has already landed, and §6.3 reads the history rather than asserting a
state. This log is the message written for posterity, per the
2026-08-31 ruling.
