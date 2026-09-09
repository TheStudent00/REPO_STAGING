# log 170 — task 66: render_back, the return path

Date: 2026-09-03. Node `hq.research.compiler_graph.term.render_back`
(0_3_5_6_5). Every figure below was computed this session from
`PseudoCoupHQ/Research/op_pipeline/` and is pasted with
its population. §5.1a labels throughout: LITERAL is the stored object,
GLOSS is a plain-words reading sitting next to it.

---

# 0. What was done, in plain words

The standing rule says a tool may transform a record only if it can
get back — "a valid simplified expression is rendered back into
canonical runnable instructions; a result that cannot return is an
intermediate, not a result" (AgentMemory, the owner 2026-08-26). Since
round 10 that way back did not exist. Log 147 §8.1 named it: "it does
not render the term back into arch instructions … A term-to-
instructions renderer is named here as work not done."

It is now built. A unit's z3 term — the thing the pipeline reads off
the unit's ledger and simplifies — is turned back into x86-64
instructions by one fixed rule, wrapped into the same canonical form
the unit's own machine code is wrapped into, handed to the real
assembler `as`, read back with `objdump -d`, and proved by the same
gate against the unit's own optimized machine code.

Over the 158 members of pool entry `E00029` — the entry whose one
term prints `v0 + v1`, spanning seven languages — all 158 rendered,
all 158 assembled, all 158 round-tripped, all 158 proved. Their 12
distinct wrapped texts became 5 distinct rendered texts.

Over all 26,040 proved terms, 5,909 rendered, all 5,909 assembled and
round-tripped, 5,873 proved. The other 20,131 were refused by name
across 17 causes, the largest being that a term carrying a conditional
has no template yet. Nothing was rendered approximately.

The CORE was insufficient for the work and was corrected first, before
any code — §1 says exactly what it lacked and what was written.

---

# 1. The CORE was corrected first, and what it lacked

The brief says: "if the CORE's shape is insufficient, correct the CORE
first and say so." It was, and it was.

## 1.1 What the CORE said before

LITERAL — the whole of `## design` as it stood
(`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_6_term/node_0_3_5_6_5_render_back/CORE_0_3_5_6_5_render_back.md`):

```
Term.render_back
	methods:
		render
			"""
			z3 term -> arch text that computes
			the same value, in the canonical
			form's own notation. NOT BUILT
			"""
		verify
			"""
			the rendered text -> gated against
			the term it came from, so the return
			path is proved rather than trusted
			"""
```

## 1.2 The five questions it did not answer

- Where does the inverse map come from? An unanswered version invites
  a second table of meanings, which is exactly what the term CORE's
  own settled rule forbids.
- Where do temporaries live? The brief says "TEMP rows through the
  standardized loads/stores", and a naive reading writes memory
  addressing into the body — which `CanonicalForm.wrap` refuses.
- Which registers may the walk use, and what happens when it runs out?
- Which arrival contract does a rendering use — the unit's own, or a
  standard one? This decides whether the gate can compare at all.
- Which gate outcome counts? `PROVED_BY_CONSTRUCTION` here would be
  circular.

## 1.3 What was written into it

A `## design` naming `template_table`, `temp_pool`, `render`,
`wrap_rendered`, `verify`, `refuse`; a paragraph "WHY THE ARRIVAL
FAMILIES ARE THE UNIT'S OWN"; and five settled rules, each with its
decision source — the reference CORE's one-table rule and log_166
TASK 66 for the inverse map; `ledger.walk_dataflow` and
`CanonicalForm.wrap`'s ledger-symbol refusal for temporaries;
AgentMemory 2026-08-28 for the pool; `gate.check_one` and log_146 §5.3
for the outcome; the accumulate ruling for what a rendered text is.

Recorded in the node's PROGRESS at the moment it was written, before
any code. Nothing here was put to the owner: every one of the five is
answered by a CORE or by AgentMemory.

---

# 2. The return path, with values moving

## 2.1 The unit, and what its three layers say

`c/op_109` is a C addition of two 64-bit integers. Its arrival
contract names `%rdi` and `%rsi`; its answer home is `%rax`, 64 bits
wide.

LITERAL — its LAYER 3, the wrapped text: the compiler's own machine
code, verbatim, between the standardized prelude and epilogue
(`render_back_E00029.json`, unit `c/op_109`):

```
mov ledger+0x00(%rip),%rdi; mov 0x0(%rdi),%rdi;
mov ledger+0x00(%rip),%rsi; mov 0x8(%rsi),%rsi;
lea (%rdi,%rsi,1),%rax;
mov ledger+0x38(%rip),%r11; mov %rax,0x0(%r11); ret
```

GLOSS: read the IN block's base out of the ledger, read row IN-0 out
of that block into `%rdi`; the same for IN-1 into `%rsi`; the
compiler's one instruction `lea (%rdi,%rsi,1),%rax` adds them; read
the OUT block's base, store the answer into OUT-0, return.

LITERAL — its LAYER 5, the normalized term (same file, same unit):

```
v0 + v1
```

GLOSS: the computation as an expression, with the input registers
renamed positionally so that two units differing only in which
register an argument arrived in print the same characters. It is a
comparison key. It does not run.

## 2.2 The term, with the symbols the gate binds

Before printing, the term carries the reference simulator's own
symbols rather than `v0` / `v1`. For this unit it is:

```
seed_rdi + seed_rsi
```

GLOSS: `seed_rdi` is the free symbol standing for whatever value the
runner puts in input row IN-0, which the prelude loads into `%rdi`.
Those symbol names are load-bearing: the gate binds input row i to
arrival family i's own symbol, so a rendering must keep them.

## 2.3 The walk, one step at a time

The rule is a post-order walk. Each sub-term is computed into the pool
register at its own depth. The pool is the fixed ordered scratch list
minus this unit's arrival families and `%rsp`/`%rbp`, so for a unit
arriving in `%rdi` and `%rsi` the pool starts `r11, r10, rax, rcx,
…`.

- depth 0 takes `%r11`, depth 1 takes `%r10`.
- The left sub-term is `seed_rdi`. It is a free symbol, so it names
  input row IN-0, which the prelude has already put in `%rdi`. Emit
  `mov %rdi,%r11`. `%r11` now holds the first argument.
- The right sub-term is `seed_rsi`. Emit `mov %rsi,%r10`. `%r10` now
  holds the second argument.
- The node is a `bvadd`. Its template is `add`, taken from
  `build_binary` in `reference.py` read backwards: that builder's
  `add` branch computes `left + right` and writes it to the
  destination, so inverted, the destination register holds the left
  sub-term and the source holds the right. Emit `add %r10,%r11`.
  `%r11` now holds the sum.
- The root is at `%r11`, 64 bits, and the answer home is `%rax`, 64
  bits. Emit `mov %r11,%rax`, then `ret`.

LITERAL — the rendered body (`render_back_E00029.json`,
`c/op_109.rendered_body`):

```
mov %rdi,%r11
mov %rsi,%r10
add %r10,%r11
mov %r11,%rax
ret
```

## 2.4 Where the temporaries went

Each of `%r11` and `%r10` holds one intermediate. When
`CanonicalForm.wrap` walks this rendered body, `Ledger.walk_dataflow`
adds a TEMP row for each value the body produces — the same thing it
does for every layer-3 body. That is what "temporaries through the
TEMP rows" means here, and it is why the body itself never spells the
ledger symbol: a body that did would be refused by `wrap` outright.

## 2.5 The rendered text, wrapped

LITERAL — the RENDERED wrapped text
(`render_back_E00029.json`, `c/op_109.rendered_wrapped_text`):

```
mov ledger+0x00(%rip),%rdi; mov 0x0(%rdi),%rdi;
mov ledger+0x00(%rip),%rsi; mov 0x8(%rsi),%rsi;
mov %rdi,%r11; mov %rsi,%r10; add %r10,%r11; mov %r11,%rax;
mov ledger+0x38(%rip),%r11; mov %rax,0x0(%r11); ret
```

Same prelude, same epilogue, same form — the difference is the three
lines in the middle where the compiler wrote one `lea`.

## 2.6 The assembler, then the gate

LITERAL — what `as --64` and `objdump -d` said about it
(`render_back_E00029.json`, `c/op_109.assembly`):

```
{"assembled": true, "instructions_written": 11,
 "instructions_disassembled": 11, "round_trips": true,
 "assembler_notes": []}
```

GLOSS: eleven instructions went in, eleven came back out of the object
file. This is real machine code, not a notation.

The gate is then asked the same question it is asked of a layer-3
text, with one side swapped:

- OURS: OUT-0 of the RENDERED wrapped text, walked by the reference,
  with input row i bound to arrival family i's symbol.
- THEIRS: the value the unit's OWN ship body leaves in its own answer
  home — `body_verbatim`, `result_family`, `arrival_contract_bindings`
  all the unit's, untouched.

Verdict: `PROVED_ON_SHIP`.

Only that outcome is counted. The gate's structural route asks whether
the compiler's body appears in the wrapped text character for
character; a rendered body is by construction not that body, so a
structural pass here would be accepting a rendering because it is a
rendering. Where the reference cannot model something, the rendering
lands in `UNDECIDED` and is not counted.

---

# 3. What the rendered text IS, relative to layers 3 and 5

- **Layer 3** is the unit's own machine code, wrapped. It is what the
  compiler wrote.
- **Layer 5** is that computation as a simplified expression printed
  by one fixed rule. It is a comparison key and does not run.
- **The rendered text is the layer-5 term made runnable.** The same
  simplified expression, emitted as instructions by one fixed rule and
  wrapped into the same form layer 3 has. It is a SECOND canonical
  rendering of the same unit, beside the first.

It replaces nothing. Layer 3 stays the unit's own machine code, and
whether a rendered text happens to coincide with it is measured, never
assumed — see §4.3 and §5.4, where the answer is that it never does.

## 3.1 One decision worth naming: what exactly is rendered

The layer-5 rule has three steps: simplify once, rename the free
symbols positionally, print on one line. Step one is applied before
rendering — the thing owed a return path is the SIMPLIFIED expression.
Step two is NOT applied: `v0` and `v1` are a printing for comparison,
while a rendering must keep the symbols the gate binds input rows to.

This was measured, not reasoned. Before step one was applied, 86 of
E00029's 158 members carried a multiply by one that no compiler ever
wrote, and the entry rendered to 8 distinct texts instead of 5.

---

# 4. POPULATION ONE — the 158 members of `E00029`

Population line: the 158 members of pool entry `E00029` in
`the_pool4.json`, spanning c, cpp, cpython, go, php, ruby, rust; the
entry records one layer-5 text and 12 distinct wrapped texts.

## 4.1 The counts

LITERAL — `render_back_E00029_printed.txt`:

```
counts, each with its population of 158 members:
  rendered                           158
  assembled_by_as                    158
  round_tripped_through_objdump      158
  proved_on_ship                     158
  character_identical_to_layer_3     0
  distinct_rendered_texts            5
  distinct_layer_3_texts             12

refusals by cause:
  none

rendered but not proved, by cause:
  none
```

Per-member verdicts: all 158 are `PROVED_ON_SHIP`, listed one per line
in the same file.

## 4.2 The five texts, and why five and not one

LITERAL — the five distinct rendered wrapped texts with their member
counts (`render_back_E00029_printed.txt`, abridged to the middle
section of each, since prelude and epilogue are the same rule):

| members | the rendered body |
|---|---|
| 93 | `mov %rdi,%r11; mov %rsi,%r10; add %r10,%r11; mov %r11,%rax` |
| 24 | `mov %rdi,%r11; mov %rdx,%r10; add %r10,%r11; mov %r11,%rax` |
| 24 | `mov %rdi,%r11; mov %rsi,%r10; add %r10,%r11; mov %r11,%rax` |
| 10 | `mov %rdi,%r11; mov %rdx,%r10; add %r10,%r11; mov %r11,%rax` |
| 7 | `mov %rax,%r11; mov %rbx,%r10; add %r10,%r11; mov %r11,%rax` |

GLOSS: the bodies repeat because the texts differ in their PRELUDE —
how many input rows the unit's arrival contract names and which
registers they arrive in. The 7-member text is go's, whose contract
arrives in `%rax` and `%rbx`. The two 24-member rows differ by which
of three input rows the computation reads.

This is the consequence the corrected CORE records rather than hides:
a rendering must use the unit's OWN arrival families, because the
gate binds input row i to arrival family i's symbol. Rendering to a
standardized contract would compare `f(seed_rdi, seed_rsi)` against
`g(seed_rax, seed_rbx)` and the solver would answer DISPROVED on a
correct rendering.

## 4.3 The collapse

Twelve distinct layer-3 texts → five distinct rendered texts, over one
layer-5 text. GLOSS: the twelve are twelve different instruction
selections the compilers made for the same addition — `lea` here,
`mov`+`add` there. The rendering erases the selection differences and
keeps only the differences that are real facts about the unit: its
arrival contract. Zero of the 158 are character-identical to their own
layer-3 text.

---

# 5. POPULATION TWO — every proved term

Population line: the 26,040 units whose layer-4 term `term61_store`
records as PROVED, out of the 30,432 units canon39 records as
WRAPPED_TEXT_PROVED. The other 4,392 canon39-proved units have no
proved term and therefore nothing to render back; they are counted,
never rendered.

## 5.1 The counts

LITERAL — `render_back_tally_printed.txt`:

```
population, computed from render_back_store/ over 332 shards:
  units with a proved layer-4 term   26040
  canon39-proved units skipped for   4392
    having no proved term

counts, each against the 26040 units with a proved term:
  rendered                               5909
  assembled_by_as                        5909
  round_tripped_through_objdump          5909
  proved_on_ship                         5873
  character_identical_to_layer_3         0

the collapse, over the same 26040 units:
  distinct rendered texts            105
  distinct layer-3 wrapped texts     1905
```

GLOSS of the two lines that matter: every text the rule rendered
assembled, and every one round-tripped — there is no gap between
"rendered" and "is machine code". And 5,873 of the 5,909 were proved
equal to the unit's own optimized machine code.

Per language, of the 26,040:

| language | units | rendered | proved |
|---|---|---|---|
| c | 8,736 | 1,971 | 1,971 |
| cpp | 15,172 | 3,418 | 3,418 |
| cpython | 1 | 1 | 1 |
| go | 402 | 130 | 130 |
| java | 2 | 1 | 1 |
| php | 4 | 4 | 4 |
| ruby | 2 | 2 | 2 |
| rust | 647 | 188 | 184 |
| swift | 1,074 | 194 | 162 |

## 5.2 Refused to render, BY CAUSE — 20,131 units, 17 causes

Each row is a CAUSE with its unit count; the sightings are its
evidence, not the item.

| units | cause |
|---|---|
| 13,027 | no template for the z3 operator `if` |
| 2,083 | a shift whose count is not a literal |
| 1,587 | a joining whose upper piece is not a literal |
| 1,140 | a joining of 33 pieces |
| 464 | no template for the z3 operator `fp.to_ieee_bv` |
| 417 | no template for the z3 operator `bvsdiv_i` |
| 416 | no template for the z3 operator `bvsrem_i` |
| 345 | an 8-bit multiply has no two-operand instruction |
| 233 | no template for the z3 operator `bvudiv_i` |
| 233 | no template for the z3 operator `bvurem_i` |
| 65 | the term reads a register the arrival contract does not name |
| 41 | a joining of 3 pieces |
| 38 | a value of 128 bits fits no register width |
| 22 | a free symbol that is not an input row |
| 12 | a value of 1 bits fits no register width |
| 6 | a joining of 25 pieces |
| 2 | a joining of 17 pieces |

LITERAL — the written reason the largest cause carries, quoted from
`render_back_tally.json`:

```
no instruction template is written for the z3 operator 'if', so this
term has no return path by the fixed rule
```

GLOSS of the top four, since they are the round-14 work list:

- `if` — a term carrying a conditional. Inverting it means rendering
  the CONDITION as a comparison that leaves flags, and the choice as a
  conditional move. `build_set_condition` and `build_move_condition`
  in the one table read a flag triple that this rule does not yet
  produce. It is the single largest thing between the current 5,909
  and the 26,040.
- a shift whose count is not a literal — `build_shift` models an
  immediate count and `%cl`; this rule writes only the immediate, so a
  shift by a computed amount needs the `%cl` path, which means
  reserving one more register by rule.
- a joining whose upper piece is not a literal, and the joinings of
  33 / 25 / 17 / 3 pieces — these are bit-level assemblies the
  simplifier leaves, and each needs its own template rather than one
  general one.
- the division and remainder operators — `build_division` in the one
  table writes the accumulator PAIR (quotient and remainder), so
  inverting it means emitting `cltd`/`cqto` plus `idiv` and reading
  one of two destinations. That is a template with two writes, which
  the current walk's one-register-per-node shape does not express.

Two causes were found and fixed inside this task rather than reported
twice (AgentMemory, "FIX A CAUSE AT FIRST OBSERVATION"):

- A joining whose upper piece is a zero literal IS a zero extension —
  the shape `build_extension(..., signed=False)` produces and the
  simplifier prints as `concat`. Adding that template moved rendered
  from 5,360 to 5,909 and closed a 5,280-unit cause.
- The 8-bit multiply. The machine has no two-operand 8-bit `imul`, so
  `as` refused 85 rust texts with "operand size mismatch". It is now
  refused by name before any text is written, rather than emitted and
  rejected.

## 5.3 Rendered but NOT proved — 36 units, 5 causes

| units | cause |
|---|---|
| 15 | the reference has no model for arch opcode `jae` |
| 14 | the reference has no model for arch opcode `js` |
| 4 | the reference has no model for arch opcode `movdqu` |
| 2 | the reference has no model for arch opcode `jl` |
| 1 | the reference has no model for arch opcode `jbe` |

GLOSS, and it matters: all 36 fail on the REFERENCE's side, not the
rendering's. The gate could not simulate the unit's OWN ship body,
because that body spells a conditional transfer the reference refuses
(it walks a body in text order) or a mnemonic the one table does not
hold. These units' terms were proved by route two — the text walk —
rather than route one. Their renderings were never disproved; they are
`UNDECIDED`. Task 64's branch-following is what decides them.

LITERAL — the assembler's tally over the whole population:

```
THE ASSEMBLER REFUSED, by cause (0 causes):
  none
```

## 5.4 The collapse, and the one thing it says

105 distinct rendered texts where the same 26,040 units carry 1,905
distinct layer-3 wrapped texts. GLOSS: over the units the rule can
render, eighteen wrapped texts collapse to one on average — the
instruction-selection differences between five compilers, erased.

Zero of the 5,909 are character-identical to their layer-3 text, and
the reason is structural rather than incidental: the fixed rule always
routes a value through the temp pool (`mov %rdi,%r11` … `mov
%r11,%rax`) where a compiler writes in place. Making the two coincide
would mean a peephole rule that recognises when the pool register is
unnecessary. That is a real option and it is NOT taken here, because
the CORE's settled rule says the rendered text is a second rendering
beside layer 3 and identity with it is a measurement, not a target.

---

# 6. The standing requirements

## 6.1 The guard — unmodified, one process, zero exempt

`guard66.py` runs `check_no_spelling_keys.py` UNMODIFIED, as a separate
process, over every JSON artifact this task writes: the two report
documents, the resume state, and all 332 shards of
`render_back_store/`. Nothing was added to any field set, no artifact
declares `role: generator provenance`, and nothing was declared out of
the walk.

LITERAL — the command and its output, run this session:

```
$ /tmp/reconnect_venv/bin/python3 guard66.py
TASK 66: 335 paths  PASS 335  FAIL 0  exempt 0  exit 0

$ grep -c exempt guard66_transcript.txt
0
```

## 6.2 The spelling ban

No operator token appears in any key, grouping, pairing, row structure,
candidate selection or comparison scope in any file this task wrote.
The population of §4 comes from the POOL — machine-form evidence — and
never from a token. The `operator` field is copied onto a member as a
display label and is never read, grouped or paired on. The paragraph is
pasted verbatim at the head of `term.py`, `render_back_run.py`,
`render_back_E00029.py`, `render_back_tally.py` and `guard66.py`.

## 6.3 One process

Every run above was a single Python process. `render_back_run.py`
takes a wall-clock budget and checkpoints per shard; there is no worker
pool and no second interpreter.

## 6.4 Superseded records

`canon*`, `layer4*`, `ledger47`, `ledger48` and `gate48` were neither
edited nor imported by any file this task wrote. `term.py` was the one
existing module extended, as the brief directs.

## 6.5 Claims against tool calls

Every count in §4 and §5 is quoted from a file this session's commands
produced, and both printed files are named. No figure here was carried
from memory.

---

# 7. Resume state

- The whole population is FINISHED. `render_back_state.json` lists all
  332 shards as done, and `render_back_run.log`'s last line reads
  `all 332 shards walked`.
- To re-run from clean: delete `render_back_store/` and
  `render_back_state.json`, then
  `/tmp/reconnect_venv/bin/python3 render_back_run.py <seconds>`. The
  driver skips shards already in the state file, so a stopped run
  continues rather than restarting; it exits 3 when its budget runs out
  with shards left.
- `render_back_E00029.py` and `render_back_tally.py` are both
  idempotent readers and can be re-run at any time.
- Nothing is half-written: the store's 332 shards, the two report
  documents, the two printed files and the guard's transcript were all
  produced by the final code and agree with each other.
- The repository is clean; the daemon has committed every artifact.

---

# 8. File inventory

## 8.1 Planning tree — every file touched

| file | what changed |
|---|---|
| `Planning/…/node_0_3_5_6_term/node_0_3_5_6_5_render_back/CORE_0_3_5_6_5_render_back.md` | `## design` rewritten (six named parts); "WHY THE ARRIVAL FAMILIES ARE THE UNIT'S OWN"; five settled rules with decision sources; definition updated from debt to discharged; realization table filled |
| `Planning/…/node_0_3_5_6_term/node_0_3_5_6_5_render_back/PROGRESS.md` | five entries: the CORE correction, `render`/`wrap_rendered`, `verify`, population one, population two, the guard, and the `if` cause left planned |
| `Planning/…/node_0_3_5_6_term/PROGRESS.md` | the same entries on the super-node |
| `Planning/…/node_0_3_5_6_term/CORE_0_3_5_6_term.md` | realization table: `render_back` moved from "nothing / planned; named debt" to the files and counts |

## 8.2 Code — new files, and the one extended

| file | new? | what it is |
|---|---|---|
| `Research/op_pipeline/term.py` | EXTENDED | section 5: `NoTemplate`, `Rendering`, the five template tables, `RenderBack`; `Term.render_back` now delegates instead of raising; module docstring updated |
| `Research/op_pipeline/render_back_run.py` | new | the driver over all 332 shards: render, assemble, gate, checkpoint |
| `Research/op_pipeline/render_back_E00029.py` | new | population one |
| `Research/op_pipeline/render_back_tally.py` | new | population two's tally, by cause |
| `Research/op_pipeline/guard66.py` | new | the unmodified guard over every JSON this task writes |

## 8.3 Artifacts written

| file | what it holds |
|---|---|
| `Research/op_pipeline/render_back_store/` | 332 shards, one per canon39 shard: per-unit rendered body, rendered wrapped text, assembly result, gate verdict |
| `Research/op_pipeline/render_back_state.json` | the resume state: 332 shards done |
| `Research/op_pipeline/render_back_run.log` | the run's own transcript |
| `Research/op_pipeline/render_back_E00029.json` | population one, per member |
| `Research/op_pipeline/render_back_E00029_printed.txt` | population one, printed: the five texts, the counts, the 158 verdicts |
| `Research/op_pipeline/render_back_tally.json` | population two, with every cause and its sightings |
| `Research/op_pipeline/render_back_tally_printed.txt` | population two, printed |
| `Research/op_pipeline/guard66.json` | the guard's summary |
| `Research/op_pipeline/guard66_transcript.txt` | the guard's own output, 335 PASS |

---

# 9. Nothing for the owner

Every decision in this task was implementation under settled rules,
decided against the tree. The five shapes the CORE lacked were written
into the CORE with their decision sources before code, as §1 records.
No question is put.
