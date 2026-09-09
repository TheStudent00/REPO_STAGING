---
id: hq.research.compiler_graph.term.render_back
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method), work
node:
    name: render_back
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_6_term/node_0_3_1_6_5_render_back/CORE_0_3_1_6_5_render_back.md
super_node:
    name: term
    path: ../CORE_0_3_1_6_term.md
sub_nodes: []
---

# CORE 0_3_1_6_5 — render_back

## metadata

- **id:** hq.research.compiler_graph.term.render_back
- **level:** 4
- **status:** draft
- **designation:** code (method), work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [term](../CORE_0_3_1_6_term.md)

## sub_nodes

*(none yet)*

## definition

The return path from a z3 term back to arch text — turning a term into
machine code again — which the standing rule about transforms requires.
The rule is that a tool may transform a record only if it can get back:
without a way home, layer 5 would be a one-way door and the term would
become a claim nothing can be checked against. This node was the named
debt of log_147 §8.1; it was BUILT on 2026-09-03 (task 66, log_170), so
a proved term whose operators the fixed rule has a template for now
returns to runnable instructions, is assembled by `as`, and is gated
against the unit's own ship code. Layer 3 remains the unit's own
machine code and is replaced by nothing; the rendered text is a SECOND
canonical rendering beside it. A term the rule has no template for
still has no return path, and every such refusal is named by cause.

## design

```
Term.render_back
	attributes:
		template_table
			"""
			z3 operator -> instruction template,
			DERIVED from
			Reference.opcode_table's builders
			read backwards. One table, not a
			second one: an entry exists here
			only where a builder there produces
			that z3 operator
			"""
		temp_pool
			"""
			the fixed ordered register pool the
			walk assigns from, in first-needed
			order, minus the unit's own arrival
			families and canon.NEVER_RENAME.
			Exhaustion is a loud refusal, never
			a silent spill
			"""
		condition_table
			"""
			z3 predicate operator -> condition
			suffix, DERIVED from
			`condition_table.SUFFIX_TO_COND`
			read backwards, one suffix per
			condition (the shortest spelling,
			ties by alphabet -- which is the
			spelling the corpus's own bodies
			write, measured). The COMPLEMENT of
			a condition is not a written table
			either: it is PROVED at construction
			from `condition_table.cond_to_z3`
			itself, by asking z3 which condition
			equals the negation of which, over
			fresh symbols
			"""
	methods:
		render
			"""
			z3 term -> body lines. A post-order
			walk: each sub-term is computed into
			the pool register at its own depth,
			the operator's template combines the
			two, and the root is moved to the
			result register at the result width.
			Free symbols are the arrival
			registers the prelude fills from the
			IN rows; the root reaches OUT-0
			through the epilogue; every
			intermediate becomes a TEMP row when
			the ledger walks the rendered body
			"""
		emit_condition
			"""
			A PREDICATE IS NOT COMPUTED INTO A
			REGISTER. The walk's rule -- every
			sub-term into the pool register at
			its own depth -- does not reach a
			term whose sort is Bool: on this
			machine a comparison leaves its
			answer in the FLAGS, and the next
			instruction's suffix reads them.
			So a predicate renders as: both
			sides into pool registers, then one
			`cmp right,left` at their shared
			width, and the suffix travels to the
			instruction that reads it. Nothing
			is left in a register by this step.
			THE ORDER IS FORCED: the comparison
			must be the LAST flag-setting
			instruction before its reader, so
			the arms of a choice are emitted
			BEFORE the comparison, never after
			"""
		emit_choice
			"""
			`If(predicate, then, else)` over bit
			vectors, the two shapes the corpus's
			own ship bodies write:
			(1) the arms are the literals 1 and
			0 -- `set<cc> %reg8`, the corpus's
			most frequent conditional shape,
			with the suffix complemented when
			the arms are the other way round; an
			answer wider than 8 bits is that
			`set` plus the zero-extend template
			the table already holds, which is
			the widening the corpus writes;
			(2) any other pair of arms --
			`cmov<cc> then,else` at 16, 32 or 64
			bits. An 8-bit choice has NO
			conditional-move instruction on this
			machine and is refused by name.
			A choice inside a choice, or a
			choice under a bit operator, is
			ordinary recursion: it composes by
			this same rule, which is what the
			corpus writes too
			"""
		wrap_rendered
			"""
			body lines -> a wrapped text, by
			CanonicalForm.wrap over the unit's
			OWN arrival families and result
			home. The rendered text is therefore
			a second canonical rendering of the
			same unit, in the same form as layer
			3, and is comparable to it character
			for character
			"""
		verify
			"""
			the rendered wrapped text ->
			Gate.prove_wrapped against the
			unit's OWN ship body, exactly as a
			layer-3 wrapped text is gated. Only
			PROVED_ON_SHIP counts: the
			structural route asks whether the
			body is present unchanged, which a
			rendered body is not, so a
			PROVED_BY_CONSTRUCTION here would be
			circular and is refused
			"""
		refuse
			"""
			a z3 operator with no template, or a
			pool exhausted, or an assembler
			rejection -- named by cause, never
			rendered approximately
			"""
```

WHY THE ARRIVAL FAMILIES ARE THE UNIT'S OWN, and not a standard set.
The free symbols of a term are the reference simulator's own
`seed_<family>` symbols. The gate proves the rendered text against the
unit's own ship body by binding input row i to the symbol of arrival
family i. Rendering against a standardized family list would compare
`f(seed_rdi, seed_rsi)` with `g(seed_xmm0, seed_rdi)` — different
symbols, so the solver would answer DISPROVED on a correct rendering.
The consequence, recorded rather than hidden: two units with the same
layer-5 term but different arrival families render to different texts,
so the collapse count is measured, never assumed to be one.

What it is owed for, stated:

1. A transform without a return path breaks the accumulate ruling: a
   record that cannot be recovered has been replaced, not added to.
2. Until it exists, layer 5 may be used only as a comparison key, and
   the pool's merges on layer-5 identity are merges of PROVED terms
   for exactly that reason.
3. A rendered text is itself gated; a render that does not prove is
   withdrawn like any other term. Measured 2026-09-03: 5,909 rendered,
   5,873 PROVED_ON_SHIP, and the 36 that did not prove failed on the
   reference's side — it has no model for something the unit's OWN
   ship body spells — not on the rendering's.

## settled rules

- **Any transform must have a return path.** Decision: log_075
  ("tools may transform only with a return path").
- **The debt is named rather than worked around.** Decision: log_147
  §8.1; carried in [term](../CORE_0_3_1_6_term.md) settled rules.
- **Layer 3 stays the unit's own machine code.** It was the only
  runnable record while this node was unbuilt; now that a rendering
  exists, layer 3 is still never replaced by it — the two are kept
  side by side. Decision: [term](../CORE_0_3_1_6_term.md) settled
  rules; the accumulate ruling.
- **A rendered text would be gated, not trusted.** Decision:
  [gate](../../node_0_3_1_5_gate/CORE_0_3_1_5_gate.md), "proved is
  counted".
- **The inverse map comes from the one opcode table.** The template for
  a z3 operator is that operator's own builder in
  `Reference.opcode_table` read backwards; no second table of meanings
  is written here, for the same reason `term.py` carries none.
  Decision: [reference](../../node_0_3_1_4_reference/CORE_0_3_1_4_reference.md),
  "meanings come from one table"; log_166 TASK 66, "operator ->
  instruction template over the ledger's rows … derived from
  `Reference.opcode_table`'s builders inverted, not from a second
  table", 2026-09-03.
- **Temporaries are the ledger's TEMP rows, not memory the body
  addresses.** A rendered body may not spell the ledger symbol —
  `CanonicalForm.wrap` refuses a body that does — so an intermediate
  is held in a pool register and becomes a TEMP row when
  `Ledger.walk_dataflow` walks the rendered body, which is how every
  layer-3 body's intermediates already become TEMP rows. Decision:
  `ledger.py`'s `walk_dataflow` (the TEMP row it adds per produced
  value); `canonical_form.CanonicalForm.wrap`'s ledger-symbol refusal.
- **The pool is ordered and unlimited within the machine.** Temps are
  assigned in first-needed order from a fixed pool; exhaustion refuses
  loudly. There is no two-temp limit. Decision: AgentMemory, "TEMP
  REGISTERS ARE STANDARDIZED, NOT LIMITED" (the owner, 2026-08-28).
- **Only PROVED_ON_SHIP counts for a rendered text.** The structural
  route's first check is that the compiler's body appears
  character-for-character in the wrapped text; a rendered body is by
  construction not that body, so accepting the structural route here
  would be accepting a rendering because it is a rendering. Decision:
  `gate.Gate.check_one`; log_146 §5.3 (the structural route is never a
  cheaper first choice).
- **The rendered text is a SECOND canonical rendering of the unit,
  beside layer 3, and replaces nothing.** Whether it is
  character-identical to the layer-3 wrapped text is a per-unit
  measurement to be recorded, not a target. Decision: AgentMemory, the
  accumulate ruling; "THE CANONICAL FORM IS ENFORCED", 2026-08-26.

- **A predicate has no register; it has the flags.** The six-part
  design of round 13 covered only terms whose sort is a bit vector,
  because that was every operator it had a template for. A conditional
  brings a term whose sort is Bool, and the machine does not put a
  Bool in a register: `cmp` leaves it in the flags and a suffix reads
  it. So the walk has a second kind of step, which computes into no
  register and returns no width. This shape was ADDED to the design
  before the code was written, which is why it is written here.
  Decision: the corpus's own ship bodies, measured 2026-09-03 over the
  31,078 units of the 332 canon39 shards —
  `probe80_conditional_shapes_printed.txt`: 20,136 flag reads that
  write a place and bind to a flag setter in the same body (18,788 of
  them `set<cc>`, 1,348 `cmov<cc>`), of which 15,604 `set<cc>` reads
  sit exactly one line after their own flag-setting arch opcode, and
  the most frequent single shape is `test <0>,<0>; setne <1>` at 5,691
  sightings.
- **The comparison is emitted after the arms, never before.** Flags
  persist until the next flag-setting instruction, so the reader binds
  to the MOST RECENT setter; emitting an arm after the comparison
  would let that arm's own arithmetic overwrite the flags the reader
  needs. Decision: `condition_table.py`'s own section-2 rule ("most
  recent flag setter"), and `reference.predicate_of`, which reads
  `state.flags` — the triple the last flag-setting opcode left.
- **The condition suffix and its complement come from the one
  condition table, not from a second one.** The suffix is
  `condition_table.SUFFIX_TO_COND` read backwards, one suffix per
  condition, chosen as the shortest spelling with ties by alphabet;
  the complement pairs are PROVED at construction out of
  `condition_table.cond_to_z3` over fresh symbols rather than typed
  in. Measured confirmation, recorded rather than assumed: the 14
  suffixes that rule picks are character-for-character the 14 the
  corpus's own bodies write (`probe80_conditional_shapes_printed.txt`,
  "condition suffixes on the flag READ"). Decision:
  [reference](../../node_0_3_1_4_reference/CORE_0_3_1_4_reference.md),
  "meanings come from one table"; `reference.predicate_of`, which is
  the builder this template inverts.
- **An 8-bit choice is refused by name.** `cmov` exists at 16, 32 and
  64 bits only. The rule refuses rather than emitting a branchless
  mask the corpus never writes. Decision: the same discipline as the
  8-bit multiply refusal already in this file (`as` rejects the text,
  so the rule refuses first).

## realization (what exists on disk, 2026-09-03)

| part | current file | status |
|---|---|---|
| template_table | `term.py` — `TWO_PLACE_MNEMONIC`, `ONE_PLACE_MNEMONIC`, `SHIFT_MNEMONIC`, `SIGN_EXTEND_MNEMONIC`, `ZERO_EXTEND_MNEMONIC`, checked against `Reference.opcode_table` at construction | done |
| temp_pool | `term.py` — `RenderBack.temp_pool` over `ledger.SCRATCH_POOL` | done |
| condition_table | `term.py` — `RenderBack.condition_suffix` / `.complement`, both derived from `condition_table.py` at construction | done, 2026-09-03 (task 80) |
| emit_condition | `term.py` — `RenderBack.emit_condition` | done, 2026-09-03 (task 80) |
| emit_choice | `term.py` — `RenderBack.emit_choice` | done, 2026-09-03 (task 80) |
| the shape read off the corpus | `probe80_conditional_shapes.py` + `_printed.txt` | done, 2026-09-03 (task 80) |
| render | `term.py` — `RenderBack.render` / `.emit*` | done: 5,909 of 26,040 proved terms; 17 named refusal causes |
| wrap_rendered | `term.py` — `RenderBack.wrap_rendered`, through `CanonicalForm.wrap` | done |
| verify | `term.py` — `RenderBack.verify`; driver `render_back_run.py` | done: 5,873 PROVED_ON_SHIP |
| the two populations | `render_back_E00029.py` (158 members), `render_back_run.py` + `render_back_tally.py` (26,040) | done |
| the guard | `guard66.py` | done: 335 PASS, 0 FAIL, 0 exempt |
| the debt recorded | log_147 §8.1; [term](../CORE_0_3_1_6_term.md) realization table | done — and DISCHARGED 2026-09-03, log_170 |
