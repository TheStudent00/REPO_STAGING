---
id: hq.research.compiler_graph.canonical_form
level: 3
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (class), rule
node:
    name: canonical_form
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_2_canonical_form/CORE_0_3_1_2_canonical_form.md
super_node:
    name: operator_equivalence
    path: ../CORE_0_3_1_operator_equivalence.md
sub_nodes:
    - name: block_order
      designation: code (attribute)
      realize: false
    - name: wrapped_text
      designation: code (attribute)
      realize: false
    - name: prelude
      path: node_0_3_1_2_2_prelude/CORE_0_3_1_2_2_prelude.md
    - name: epilogue
      path: node_0_3_1_2_3_epilogue/CORE_0_3_1_2_3_epilogue.md
    - name: labels
      path: node_0_3_1_2_4_labels/CORE_0_3_1_2_4_labels.md
    - name: wrap
      designation: code (method)
      realize: false
    - name: assemble
      designation: code (method)
      realize: false
    - name: refuse
      path: node_0_3_1_2_7_refuse/CORE_0_3_1_2_7_refuse.md
---

# CORE 0_3_1_2 — canonical_form

## metadata

- **id:** hq.research.compiler_graph.canonical_form
- **level:** 3
- **status:** draft
- **designation:** code (class), rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [operator_equivalence](../CORE_0_3_1_operator_equivalence.md)

## sub_nodes

- block_order — code (attribute) *(realize: false)*
- wrapped_text — code (attribute) *(realize: false)*
- [prelude](node_0_3_1_2_2_prelude/CORE_0_3_1_2_2_prelude.md) — The standardized lines placed BEFORE the compiler's body that put each arriving value into the register the compiler's own code expects it in.
- [epilogue](node_0_3_1_2_3_epilogue/CORE_0_3_1_2_3_epilogue.md) — The standardized lines placed BEFORE every `ret` in the compiler's body that store the compiler's own result register into OUT-0, the answer row.
- [labels](node_0_3_1_2_4_labels/CORE_0_3_1_2_4_labels.md) — The rewrite that replaces every branch target inside a unit with a positional name — `L0`, `L1`, … in address order — so that two units with the same shape of jumps get the same text instead of two texts differing only by their own addresses and their own function names.
- wrap — code (method) *(realize: false)*
- assemble — code (method) *(realize: false)*
- [refuse](node_0_3_1_2_7_refuse/CORE_0_3_1_2_7_refuse.md) — The named reasons a unit cannot be put into the canonical form at all, each recorded as a cause with a real unit shown under it rather than a count.

## definition

THE one form every arch-unit is rendered into so that units from
different compilers become comparable and stay runnable: the
compiler's body kept character-for-character, between a standardized
PRELUDE that loads each argument out of a memory row into the register
the compiler expects it in, and a standardized EPILOGUE that stores
the compiler's result register into the answer's row. Rows live in
typed blocks reached through a ledger at an absolute address; no
register is reserved; no register is renamed. This node supersedes
every earlier form (register-designated, red-zone slots, universal
scratch rewrite, %r15 anchor) and is the only form the pipeline may
render.

## design

```
class CanonicalForm
	attributes:
		block_order
			"""
			IN, CONST, TEMP, OWN, STACK, X87,
			GUARD, OUT — fixed; eight 8-byte
			ledger entries, 0x40 bytes
			"""
		wrapped_text
			"""
			prelude + body verbatim + epilogue,
			one string; the runnable record
			(layer 3)
			"""
	methods:
		wrap
			"""
			ArchUnit -> wrapped_text + Ledger.
			Calls prelude, labels, epilogue; the
			body is never touched
			"""
		assemble
			"""
			wrapped_text -> object file via
			`as --64`; `objdump -d`/`-r` read back;
			the ledger symbol appears only as
			R_X86_64_PC32 relocations
			"""
		refuse
			"""
			sub-node: the named reasons a unit
			cannot be wrapped (never returns; no
			answer home), each a class with its
			instance
			"""
```

Call flow:

```
CanonicalForm.wrap(unit)
    --> CanonicalForm.prelude(unit.arrival_contract)
    --> CanonicalForm.labels(unit.body_text, unit.body_bytes)
    --> CanonicalForm.epilogue(unit.answer_home)
    --> Ledger.build(unit)
```

## settled rules

- **The compiler's body is verbatim.** Its register assignment is
  compiler-proven conflict-free; renaming it is forbidden. Decision:
  AgentMemory "THE MEMORY-WRAPPED FORM" (the owner, 2026-09-02).
- **The ledger lives at an absolute address**, rip-relative; no
  register is a region base. Decision: same.
- **Rows are sized by type**; a 16-byte value gets a 16-byte row.
  Decision: log_141 §8, log_146 §2.5.
- **Blocks are typed lineages**: every distinct origin of a value has
  its block — inputs, constants, temporaries, the unit's own stack
  addresses, the machine stack, the x87 stack, guard outcomes, the
  answer. Decision: AgentMemory "REFINEMENT — NO DESIGNATED
  REGISTERS" + "ROUND 10 RULINGS" (2).
- **Branch labels are positional** (`L0..` in address order); an
  out-of-unit transfer keeps its callee as the operand and drops
  address and symbol comment. Decision: "ROUND 10 RULINGS" (4);
  log_152 §4.1.
- **IN rows are numbered in `arrival_contract` order, and the prelude
  emits in that same order.** The prelude's vector-first ordering
  (log_153 §9) is a defect against this line. Decision: this CORE,
  2026-09-03, refining the wrapped-form ruling; the count of affected
  units is owed by the next lap.
- **Erased-and-re-rendered is canonical; a tool may transform only
  with a return path.** Decision: log_075.
- **The fixed-rule re-render is a textual normalizer applied after
  proof, never the only route to a text.** Decision: "ROUND 10
  RULINGS" context, log_142 ruling 4. It lives in
  [term](../node_0_3_1_6_term/CORE_0_3_1_6_term.md), not here.

## the form, as the owner meant it — CORRECTION 2026-09-05

**The arch-unit is essentially UNCHANGED except for the loading and
unloading of registers into a virtual memory.** the owner, 2026-09-05,
correcting how his 2026-09-02 ruling was read: "you mean my
misinterpreted words? the arch-unit is supposed to be essentially
unchanged except for the loading/unloading of registers into a
virtual memory."

WHAT WAS MISREAD. `region36.py:10` quotes the 2026-09-02 ruling
("everything is loading from memory and storing in memory") and
implements it as: rewrite EVERY location in the body as
`0x<offset>(%r15)`. That requires one register to hold a fixed base
for a whole body, which is where the `%r15` collision comes from.

WHAT IS CORRECT, and it is already on disk. `canonical_form.py`
(canon40) wraps rather than rewrites. LITERAL, `c/op_135`:

    body, as the compiler emitted it:
      cvtsi2ss %edi,%xmm1; addss %xmm1,%xmm0; ret

    canon40's wrapped form:
      mov ledger+0x00(%rip),%rdi; mov 0x0(%rdi),%rdi;
      mov ledger+0x00(%rip),%r11; movdqu 0x10(%r11),%xmm0;
      mov ledger+0x00(%rip),%r11; movdqu 0x20(%r11),%xmm1;
        cvtsi2ss %edi,%xmm1; addss %xmm1,%xmm0;   <- body, untouched
      mov ledger+0x38(%rip),%r11; movq %xmm0,0x0(%r11); ret

Loads at the front, body verbatim, store at the back, addressed
rip-relative through the ledger. MEASURED 2026-09-05: **0 of the
1,779** compiled units' wrapped texts contain `%r15`.

CONSEQUENCES, all planned:
1. The eleven interpreter units move onto `canonical_form.py`. They
   are on `canon36_universal` + `region36`, which is the misread form.
2. The `%r15` collision is an ARTIFACT of the misreading, not a
   design conflict. Do not "fix" it by moving the region base.
3. Two of the three shortfalls log_199 flagged go with it -- "no
   block kind for memory obtained at run time" and "an input block
   holds a pointer" are consequences of re-addressing a body rather
   than wrapping it.

## the seventh block kind — an arriving addressable area (planned 2026-09-05)

`region36.py:271` allocates six kinds: input, constant, temp, result,
own-address, guard-outcome. Five hold ONE VALUE each. `own-address`
is already an addressable AREA -- 0x100 bytes the unit reaches into
at its own offsets, described there as "an affine image, not a slot
series", mapped so the unit's internal spacing is preserved and only
the base moves.

php's value frame is that same shape and ARRIVES rather than being
the unit's own scratch, and its offsets (0x40, 0x50, 0x60) are
constants sitting in the bytecode. So the gap is one kind, with a
working precedent, not a new capability.

the owner's observation, recorded because it inverts the assumption this
node was carrying: "wouldnt the pointer-arch-units essentially be in
the canon virtual memory form by default?" They would. A unit that
works through pointers is ALREADY loading from memory and storing to
memory. It is the compiled units, which take values in registers,
that need the wrapping.

## realization (what exists on disk, 2026-09-03)

| part | current file | status |
|---|---|---|
| wrap, prelude, epilogue, labels | `ledger48.py` (imports 20 names from `ledger47.py`), drivers `canon38_wrapped.py` / `canon38_interp.py` / `canon38_regen.py` | done: 30,436 of 31,078 wrapped and proved (log_152) |
| assemble | `canon38_assemble.py`; 2,728 offered / 2,728 assembled / 8,946 ledger relocations | done |
| refuse | 642 units by two causes: never returns (16 + 408), no answer home (216), no canonical text (2 interpreter) | done, named |
| superseded forms | `canon2` … `canon36_*`, `region36.py`, `canon35_universal_*`, `ledger47.py` | superseded; kept as record; 107 files named `canon*` predate this node |

### the lap of 2026-09-03 (task 60, log_162)

Both of the next-lap items are done. `canonical_form.py` exists and
carries this node's name: class `CanonicalForm` with `wrap`,
`assemble`, `refuse`, attributes `block_order` and `wrapped_text`, and
the four sub-nodes as the classes `Prelude`, `Epilogue`, `Labels`,
`Refuse`. It imports `ledger.py` and `gate.py` and imports nothing
from `ledger47/48.py`, `gate48.py` or any `canon37/38_*` driver.

| part | current file | status |
|---|---|---|
| wrap, prelude (contract order), epilogue, labels, refuse | `canonical_form.py` | done: 30,432 of 31,078 wrapped and proved |
| assemble | `canonical_form.py --assemble`; 2,728 offered / 2,728 assembled / 8,948 ledger relocations | done |
| refuse | 646 units by four causes: never returns 424, no answer home 216, no canonical text 2, no runtime callee body 4 | done, named |
| zero regression against canon38 | `canonical_form.py --zero-regression` -> `canon39_zero_regression.json`; 0 regressions without a named cause | done |
| superseded | `ledger48.py`'s prelude and the `canon38_*.py` drivers | superseded records, not edited |

The IN-i ordering defect affected 5,818 of the 31,078 units, and
exactly 5,818 wrapped texts changed. Evidence: log_162.
