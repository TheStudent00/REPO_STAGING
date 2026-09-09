---
id: hq.research.compiler_graph.ledger.destination_rules
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (attribute), rule
node:
    name: destination_rules
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_3_ledger/node_0_3_1_3_3_destination_rules/CORE_0_3_1_3_3_destination_rules.md
super_node:
    name: ledger
    path: ../CORE_0_3_1_3_ledger.md
sub_nodes: []
---

# CORE 0_3_1_3_3 — destination_rules

## metadata

- **id:** hq.research.compiler_graph.ledger.destination_rules
- **level:** 4
- **status:** draft
- **designation:** code (attribute), rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [ledger](../CORE_0_3_1_3_ledger.md)

## sub_nodes

*(none yet)*

## definition

The per-opcode table saying which registers an instruction writes and
which it reads WITHOUT naming them in its operands. It exists because
several x86 instructions leave their answer somewhere they never
mention: `idiv` writes the quotient to the accumulator and the
remainder to the data register while naming only the divisor. Without
the table the ledger attached the answer row to the divisor, which is
the defect log_147 §5 found. The table is keyed by mnemonic with one
size suffix stripped, so `idivl` and `idivq` both find `idiv`, and it
is qualified by operand count so the two- and three-operand `imul`
stay on the ordinary rule.

## design

The table, as it stands. ACCUMULATOR is the `%rax` family, DATA
REGISTER the `%rdx` family.

| opcode | writes | reads implicitly | only at operand count |
|---|---|---|---|
| `idiv` (width 32/64) | rax = quotient, rdx = remainder | rax, rdx | any |
| `div` (width 32/64) | rax = quotient, rdx = remainder | rax, rdx | any |
| `idiv` (width 16) | ax = quotient, dx = remainder | ax, dx | any |
| `div` (width 16) | ax = quotient, dx = remainder | ax, dx | any |
| `idiv` (width 8) | al = quotient, ah = remainder | ax | any |
| `div` (width 8) | al = quotient, ah = remainder | ax | any |
| `mul` (width 32/64) | rax = low half, rdx = high half | rax | 1 |
| `imul` (width 32/64) | rax = low half, rdx = high half | rax | 1 |
| `mul` (width 16) | ax = low half, dx = high half | ax | 1 |
| `imul` (width 16) | ax = low half, dx = high half | ax | 1 |
| `mul` (width 8) | ax = the whole product | al | 1 |
| `imul` (width 8) | ax = the whole product | al | 1 |
| `cltd` | rdx | rax | 0 |
| `cqto` | rdx | rax | 0 |
| `cwtl` | rax | rax | 0 |
| `cltq` | rax | rax | 0 |
| `cbtw` | rax | rax | 0 |

The rules that govern the table:

1. The lookup strips one operand-size suffix before matching.
2. An entry applies only at the stated operand count, so the forms
   that DO name their destination stay on the ordinary rule.
3. An opcode not in the table writes the destination its own operands
   name. The table is an exception list, not a full instruction set.
4. A transfer into the compiler's OWN runtime writes EVERY REGISTER
   FAMILY THE ATTACHED CALLEE'S OWN BODY CHANGES, one row per family,
   each produced by `{"kind": "runtime_callee", "callee": ...}`. The
   families are READ OFF THE CALLEE'S BODY (see the settled rule "THE
   ANSWER REGISTERS ARE READ OFF THE ATTACHED CALLEE'S BODY" below);
   they are never asserted and never taken from a list of names. It is
   NOT keyed by the transfer's mnemonic in the table above: it fires
   only when the callee is a routine one of this machine's toolchain
   archives DEFINES — machine-form evidence, read out of the archive's
   own symbol index by `runtime_callee.py`, never from the name's
   spelling. When no such set is handed to the ledger the rule does
   not fire and a transfer is left exactly as it was.
   - SUPERSEDED WORDING, kept so the change is visible: "writes the
     accumulator, and the row it writes is …" (one row, on `%rax`).
     That was wrong twice over — wrong register for every float
     lowering, and one row where the body writes several places. See
     the settled rule below.
   - The callee's name is read from the RELOCATION the unit's object
     file carries (`!!reloc=R_X86_64_PLT32:__divti3-0x4`) as well as
     from the assembler identifier the positional-label pass leaves
     (`call x___divti3`). An unlinked `call` disassembles as a
     transfer to an address inside the unit, so the label pass writes
     `call L0` and only the relocation still says where it goes.
   - Written into this CORE 2026-09-03, ahead of the code, under round
     12's binding rule 2. Provenance: the owner, 2026-09-03, "if its within
     the compiler, its not a library call"; log_158 TASK 59 (b). It
     answers the question log_152 §9.2 put to the owner and log_153 §3.4
     declined to invent.

## settled rules

- **Implicit destinations are per-opcode rules.** Decision:
  AgentMemory "ROUND 10 RULINGS" (3); log_152 §2.
- **Nothing unruled is added to the table, and the one thing that was
  unruled has now been ruled.** `call` was left out and reported as a
  census row (log_153 §3.4; the question at log_152 §9.2); the owner ruled
  on 2026-09-03 and rule 4 above is that ruling written down.
- **A comparison writes flags, not its destination register.**
  Decision: log_152 §2.5.
- **The old rule is named as the defect it was**: `ledger47.py` took
  the last named operand as the destination. Decision: log_147 §5.

- **THE DESTINATION PAIR IS QUALIFIED BY OPERAND WIDTH, AND AT THE TWO
  NARROW WIDTHS IT IS TWO PARTS OF ONE REGISTER.** The table above was
  silent on width and named the 64-bit spellings, so a body dividing at
  8 or 16 bits found no rule; 20 units stopped there (log_160 §1.7).
  The machine's rule: the dividend is `AX` at width 8 and `DX:AX` at
  width 16, and the answers land in `AL`/`AH` and `AX`/`DX`. At width 8
  the two answers are two BYTES OF ONE REGISTER FAMILY, which is why
  the ledger writes one row for the accumulator rather than two rows
  for two families, and why the reference composes the family's new
  value from its old one instead of using the ordinary zero-extending
  write (the rule is in
  [machine_state](../../node_0_3_1_4_reference/node_0_3_1_4_1_machine_state/CORE_0_3_1_4_1_machine_state.md)).
  A one-operand widening multiply at width 8 has no high half at all:
  the whole 16-bit product IS `AX`. Decision: this CORE, 2026-09-03
  (task 64), written before the code, under round 12's binding rule 2.
  Provenance: log_160 §1.7's own recorded refusals -- "a division at
  width 16 is not modeled" (10 units), "at width 8" (5), "a widening
  multiply at width 8" (4), "at width 16" (1); log_166 TASK 64.

- **THE ANSWER REGISTERS ARE READ OFF THE ATTACHED CALLEE'S BODY, AND
  THERE IS ONE ROW PER FAMILY THE BODY CHANGES.** The reading, stated
  as the machine-form procedure it is, and applied to the callee arch
  unit `runtime_callee.extract_callee` already attached:
  1. Walk the callee's own body once in text order, holding for each
     register family a token: the family starts at `entry(family)` and
     every instruction that writes it replaces the token — a move-like
     opcode PROPAGATES its source's token, every other opcode leaves a
     fresh `computed` token.
  2. The machine stack is tracked with it: `push` parks the source's
     token at the tracked stack depth, `pop` takes it back, and a
     store to and a load from a stack-pointer-relative slot do the
     same. So a routine that SAVES a family and RESTORES it ends with
     that family's token still `entry(family)`. The walk is ONE LINE
     of text, not one path, so a body with one `push` and one `pop`
     PER RETURN PATH would otherwise read as changed on the second
     path: a family whose arrival value the body was seen parking is
     therefore restored by a `pop` this reading cannot place.
     `clang/__eqtf2` is the measured instance — one `push %rbx`, two
     `pop %rbx`. Written into this CORE after the measurement that
     produced it, which is the reverse of the binding order and is
     said so here.
  3. At the end, the families whose token is no longer their own
     `entry` token are the families the body CHANGED. `%rsp`, `%rbp`
     and `%rip` are excluded, as they are everywhere else in the
     ledger (`canon.NEVER_RENAME`).
  4. A body whose last instruction is an unconditional transfer to
     another routine of the same archive (`__udivti3` is three
     instructions and a `jmp`) takes THAT routine's changed families
     as well, followed with a cycle guard.
  5. A body that leaves a value on the x87 stack (its `fld`/`fild`
     pushes outnumber its `fstp`/`fistp` pops) also answers there, and
     the caller's ledger gets an X87 row for it.
  6. WHERE THE READING CANNOT BE MADE — no `ret` and no resolvable
     tail transfer, or the tracked stack depth is lost — the callee is
     recorded as UNREADABLE BY NAME and the callers it would have
     served are refused by name. A guess is never substituted.
  This is what "the callee's own answer" means: the whole set of
  families it changes, not one chosen register. A family the routine
  merely clobbers is in the set on purpose — the callee did change it,
  and a row saying so is true where the old silence was false.
  Decision: this CORE, 2026-09-03 (task 78), written before the code.
  Provenance: log_168 §5.3's two-part finding (the accumulator is
  wrong for a routine answering in `%xmm0`; one row is wrong even when
  the register is right) and its 2,862 measured units; the callee
  bodies are `canon39_callee_units.json` (task 63, log_167).

- **A TRANSFER TO A ROUTINE NO ARCHIVE INDEX DEFINES IS NOT THIS
  RULE'S BUSINESS.** go's and rust's panic paths are not runtime
  lowerings; the shape they get is
  [runtime_callee](../../node_0_3_1_1_arch_unit/node_0_3_1_1_8_runtime_callee/CORE_0_3_1_1_8_runtime_callee.md)'s
  "guard exit" and it makes no row here. Decision: this CORE,
  2026-09-03 (task 78), pointing at the node that owns the shape.

## realization (what exists on disk, 2026-09-03)

Home: `~/Programming/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| the table | `ledger48.DESTINATION_RULES` (in `ledger48.py`) | done |
| effect measured | 3,807 destination-table rows over 31,078 units (log_152 §2.3) | done |
| acceptance instance | `c/op_210`, arguments 20 and 6 (log_152 §2.2) | done |
| the transfer into the runtime writes the accumulator | `ledger.py` (`RUNTIME_TRANSFER_RULE`, `transfer_callee`, the walk's runtime branch) | done 2026-09-03 (task 59); `c/regen_10427` and `c/regen_10428` printed in `ledger_sample_walk_printed.txt` |
| the table, under the node's own name | `ledger.py` (`DESTINATION_RULES`), importing nothing from `ledger47`/`ledger48` | done (task 59) |
| superseded | `ledger47.py`'s last-named-operand rule | superseded record |
| rule 4 CORRECTED: one row per family the attached callee's body changes | `ledger.py` (`RUNTIME_TRANSFER_RULE`, `answer_registers_of_body`, `answer_row_half`, the walk's runtime branch, `Ledger.runtime_answer`) | done 2026-09-03 (task 78) |
| the readings, as data | `runtime_answers78.py` -> `runtime_answers78.json`, `runtime_answers78_printed.txt` -- 76 bodies read, 0 refused, 6 leaving a value on the x87 stack | done (task 78) |
| the render under the corrected rule | `canon40_wrapped_*.json`, `canon40_interp.json`, `canon40_regen_store/` (326 shards), `canon40_assemble.json` | done (task 78) |
| the effect measured | `audit78_printed.txt`: canon39 3,619 units with a transfer into an archive-defined routine and NO row naming it; canon40 **0**. `runtime_callee` rows 608 -> 49,362 | done (task 78) |
