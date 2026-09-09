# log 078 — the arch-unit branch: what is automated, and what a compiler move actually costs

Date: 2026-08-29. A MEASUREMENT audit, not a build. Every number below
was printed by a run performed today; nothing is asserted from reading
code alone. Where something could not be run it is marked unverified
with its reason.

Layer named, per the three-layer anchor: this audit serves **layer 3
(OPERATION)** — what the compiler can do to a representation. It does
not touch layer 1 (the data forms) or layer 2 (the per-language
holders).

Scope: `PseudoCoupHQ/Research/op_pipeline/`, its upstream
`PseudoCoupHQ/Research/kind_fuzz_clustering/`, and the
Airlock lane. Log 076 answered the same question for the census and
shape layers; this log does not repeat that work and does not restate
its numbers except where they are needed to read a number here.

**Vocabulary.** Structural relations are said with super-node,
sub-node, co-node, sub-tree. The outcome where the operating system
stops a process is ABORT.

**Cold terms, one line each** (they were warm on 2026-08-26 and are
cold now):

- **lane** — one shell script written into
  `Airlock/agent/drop/`; the file write is the run.
- **probe** — one compiled function that applies exactly one operator
  to parameters only; constants are banned so the operation cannot be
  folded away at compile time.
- **arch-unit** — the machine instructions one probe compiled to, read
  out of the object file by `objdump`, stored as a byte list and a
  mnemonic list.
- **ANCHOR / SHIP** — the same probe built twice: ANCHOR with the
  optimizer off and debug information on, SHIP with the optimizer on.
  Identity is established at the ANCHOR and carried to the SHIP by the
  difference between them.
- **canonical form** — the normalized, runnable arch-instruction
  rendering of a unit: standard registers, one instruction per line.
  Since 2026-08-26 it is the HOME representation.
- **class key** — what decides whether two units are the same: the
  operand type pair, the result type, and the canonical text. The
  operator token is never part of it (the spelling ban).
- **dom_op** — a dominant operator: a connected component of the
  mutual-best graph over (language, operator, arity) nodes.
- **alpha** — the smallest recurring component of an erased unit; no
  smaller component of it recurs elsewhere.

---

## 1. Plain-words walkthrough

### what this branch is, from the top

Take one operator of one language — rust's `+`, say — and ask what
machine the compiler actually builds for it. This branch answers that
mechanically, for five compiled languages, and then asks which
languages' answers are the same machine.

The chain has a shape worth holding before any file name appears.

**First, someone writes down what operators a language has.** That
list lives in one python file and is a person's typing, checked
afterwards by a machine against the language's own pinned grammar.

**Second, a generator crosses that list with six types** — 32-bit
signed integer, 64-bit signed, 64-bit unsigned, 32-bit float, 64-bit
float, truth value — and writes out one tiny source file per
combination. For rust that is 858 source files. Nothing decides which
of them are legal; that is the compiler's job.

**Third, all 858 are handed to the compiler.** The compiler accepts
125 of them and refuses 733, and its refusal text is kept as the
testimony for why. Each accepted one is built twice, once with the
optimizer off and once with it on, and `objdump` reads the
instructions back out of both object files. The compiler's own debug
table is read too, to learn which register each parameter arrived in.

**Fourth, the instructions are turned into a normal form.** The bytes
are lifted into a formula, the formula is simplified, and the result
is rendered BACK into instructions with standardized register names.
That last step — rendering back — is what makes the normal form
runnable rather than a description of something runnable. A unit that
survives the round trip and is then proved equal to the compiler's own
output is called converged. For rust, 98 of the 125 units are
converged today.

**Fifth, units with the same normal form are grouped.** Two units are
in one class when their operand types, result type and normalized text
all agree. The operator's spelling plays no part; it rides along as a
label on the member and nothing else. Those classes are then read for
which languages' operators answer the same way, and the result is a
table of dominant operators plus the places where languages disagree
on purpose.

### what the audit asked, and the shape of the answer

the owner's question is whether a target language moving to a new version is
something this machinery handles by itself. rust shipped 1.98.0 on
2026-08-20. rust 1.98.0 is installed beside the old one in the sandbox,
at `/persist/rustup076/`, and the image's default is still 1.96.1. The
pin was not moved.

So the whole rust extraction was run twice today, once at each
compiler, with one line of difference between the two lane scripts,
and the two results were compared record by record. Then the class
table was rebuilt from each result and the two tables were compared.

**The headline is that the compiler move changed nothing that the
pipeline uses, and changed 47 things that it stores.** Every one of
the 858 probes got the same verdict from both compilers. Every one of
the 733 refusal texts is identical. Every one of the 125 accepted
units has byte-identical machine code at both compilers, in both the
optimizer-off and optimizer-on builds. Every one of the 125 debug
tables is identical. The class table and the dominant-operator graph
came out byte-identical.

What did change is 47 of the 1,108 stored records, and in every one of
them the change is inside a NAME, not an instruction. When a rust unit
contains a call — a division that checks for zero, an addition that
checks for overflow at the un-optimized build — `objdump` cannot print
the callee's address, because in an object file that address is still
zero; the callee's name lives in a separate relocation entry, and the
extractor appends that name to the instruction text. Those names carry
two things rustc changed between the two releases: a hash identifying
the `core` library build, and the default scheme for spelling a
generic function's name. Neither is part of the instruction. Both are
stored inside the instruction column.

That is the whole blast radius of a rust version move on this branch,
measured: **zero bytes, zero verdicts, zero classes, and 3,668 stale
strings in 41 machine-written files, none of them hand-authored.**

### the second question, and the more interesting answer

The five new float methods rust 1.98.0 added — `algebraic_add` and its
four co-methods — are new operations of the language. Can they enter
this branch?

They can be extracted. One was carried as far as it goes today: a
twelve-probe manifest was hand-written and run through the branch's
own lane generator with no edit to any tool. At rust 1.96.1 all ten
algebraic probes were refused, ten times over, with the compiler
saying `use of unstable library feature 'float_algebraic'` — which is
the pipeline's own compile-or-refuse rule detecting a language change
for free, in four tenths of a second. At rust 1.98.0 all ten compiled
and all ten arch-units came out clean.

They cannot be GENERATED, and they should not yet be MERGED, and the
second of those is the finding.

They cannot be generated because the operator inventory has no place
for them. `algebraic_add` appears zero times in
`operator_arity.json` and zero times in the pinned rust grammar,
because it is a method call, not an operator spelling. The probe
generator reads three buckets — prefix, postfix, binary — and a method
call's only home in the grammar is the structural bucket, which the
generator excludes by an explicit written reason.

They should not yet be merged because of what the extraction actually
produced. rust's `algebraic_add` on two 64-bit floats compiles to
`addsd %xmm1,%xmm0` then `ret`, five bytes, `f2 0f 58 c1 c3`. rust's
ordinary `+` on two 64-bit floats compiles to exactly the same five
bytes. Their canonical texts would be the same string, their operand
types are the same, their result types are the same — so the class key
is the same, and the pipeline would put them in one class and record
no divergence at all. But log 076 measured that they are NOT the same
operation: at optimization the algebraic one can be rearranged and the
ordinary one cannot. The difference does not show up here because a
two-operand probe has nothing to rearrange; rearrangement needs three
or more operands, and every probe in this branch has at most two by
construction ("a probe applies ONE operator to PARAMETERS only").

So the measured stopping point is not a missing feature. It is a probe
SHAPE that cannot see the property the new operators exist to have.

---

## 2. The stage map

The pipeline end to end, from an operator in a language to a proved
canonical arch-unit and its place in the tables. Times are wall times
measured today unless the cell says otherwise. "Person must touch"
means a human has to type something for the stage to produce a correct
answer, not merely start it.

| # | stage | script, full path | inputs | outputs | time | person must touch |
|---|---|---|---|---|---|---|
| 0 | operator inventory | `PseudoCoupHQ/Research/kind_fuzz_clustering/operator_arity.py` (1,464 lines) | the pinned grammar sources in `grammar_cache/`, plus the file's own hand-typed table | `operator_arity.json` (5,859 lines; 13 languages) | not re-run today (unverified) | YES — 136 `G(rule, file, ops)` rows, 1,561 operator spellings hand-typed; rust's row set carries 97 |
| 1 | probe generation | `PseudoCoupHQ/Research/op_pipeline/probe_gen.py` (502 lines) | `operator_arity.json`; its own HOLDERS, result-type rules and five emitters | `probe_manifest_{c,cpp,go,rust,swift}.json` — 4,440 candidates (c 750, cpp 1,002, go 744, rust 858, swift 1,086) | 0.10 s, all five | YES — 30 holder rows, 58 lines of result-type rule, 5 source templates, 2 operator exclusions, 3 bucket exclusions |
| 2 | lane generation | `PseudoCoupHQ/Research/op_pipeline/lane_gen.py` (587 lines) | the five manifests | `op_pipeline/lanes/op_<lang>.sh`, optionally copied into `Airlock/agent/drop/` | 0.08 s, all five | YES, once per language — a 5-row tool check and a 5-language × 2-mode compile-flag table |
| 3 | extraction: compile-or-refuse, ANCHOR + SHIP, objdump, DWARF | the generated lane, run by the Airlock daemon | the lane's own embedded probe table | `Airlock/agent/out/op_<lang>.txt` | rust 29.8 s today (24.1 s on record); c 42.4 s; go 48.5 s; cpp 74.1 s; swift 159.8 s | NO — one file write starts it; the compiler is the acceptance oracle and no acceptance table is consulted |
| 4 | fold | `PseudoCoupHQ/Research/op_pipeline/fold.py` (184 lines) | the manifest and the lane output | `op_units_<lang>.json` | rust 0.05 s | NO |
| 5 | lift and normalize | `canon2.py` → `canon3.py` → `canon4.py`, with `expr_to_canon.py` (1,246 lines), `condition_table.py` (379), `condition_table2.py` (218) | `op_units_<lang>.json` | `canon{2,3,4}_units_<lang>.json` | not re-run today (unverified; needs pyvex + z3, both present in the container) | YES — 37 named refusal categories, a 6-entry register map, 5 arithmetic and 20 comparison rendering rows, a 28-row condition-suffix table |
| 6 | canonical rendering and the proof gate | `canon5.py` … `canon13.py` with `canon7_render.py` (970), `canon11_render.py` (489), `canon12_render.py` (124), `canon13_render.py` (160) | `canon4_units_<lang>.json`, `tree_units2.json` | `canon<N>_units_<lang>.json`, each unit carrying its canonical text and a gate verdict | not re-run today (unverified) | YES — every new machine shape needs a rendering rule; the file `PseudoCoupHQ/Research/op_pipeline/stage5_float_conditions_diagnosis.txt` is the current worked example of what that costs |
| 7 | reading form (the second column) | `PseudoCoupHQ/Research/op_pipeline/reading_form.py` (716 lines) | `op_units_<lang>.json`, `canon2_units_<lang>.json` | `reading_units_<lang>.json` (rust: 237 units), `reading_sample.txt` | not re-run today (unverified) | YES — about 35 mnemonic template arms, a 15-row flag-name table, and `SPEC_reading_form.md`'s 55 template rows plus 16 function-vocabulary rows |
| 8 | component mining (alphas) | `component_mine.py`, `component_mine2.py` | the erased forms of 1,731 units | `ALPHAS.md` — 275 level-0 components | not re-run today (unverified) | NO — mined, not authored |
| 9 | class table and dominant operators | `PseudoCoupHQ/Research/op_pipeline/dominant_table12.py` | `canon{4,7,8,9,10,11,12,13}_units_<lang>.json`, `result_types_<lang>.json` | `dominant_table12.json` (926 classes, 1,641 members), `dom_ops10.json` (135 nodes, 26 dom_ops, 23 edgeless) | 0.20 s | NO |
| 10 | verdicts (the solver stage) | `verdicts3.py` / the verdicts6 run | `dominant_table5.json` | `verdicts6.json` — 8,148 nominations, 4,370 distinct pairs, 4,240 fresh z3 verdicts | 15.62 s, recorded inside the file itself | NO |
| 11 | bridges and dominance | `dominance2.py`, `dominant_table_containment.py` | the class table | `bridges6.json`, `table_digest3b.md` (1,113 classes, 322 bridges) | not re-run today (unverified) | NO |
| 12 | the spelling guard | `PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py` | any grouping artifact plus the manifests | PASS/FAIL naming each offending path | 0.03 s | NO — its 78-token operator inventory is derived from the manifests, not declared |

### the two upstreams the brief named, and what they actually feed

**The acceptance and answers files do NOT feed this branch.** They are
`PseudoCoupHQ/Research/kind_fuzz_clustering/acceptance_rust_A2.json`
and `.../answers_rust.json`, from the layer-3 census campaign. The
branch says so in its own words, in `probe_gen.py`'s docstring:

> `PseudoCoupHQ/Research/op_pipeline/probe_gen.py`
> "This tool emits EVERY CANDIDATE. It consults no acceptance file.
> Whether a candidate is a real operation of the language is decided
> later, by the compiler's own type checker, in the lane
> (`lane_gen.py`) -- that is where overload resolution lives, and it
> is the acceptance oracle. A refusal is testimony, not a gap."

The only shared upstream is `operator_arity.json`.

**The compiler-graph tracing does not feed it either.**
`PseudoCoupHQ/Research/compiler_graph/build_graph.py`
parses the Go compiler's own source with tree-sitter and answers a
different question — which line of the compiler picks a physical
register. It shares no artifact with `op_pipeline`. It is a co-node
instrument, not a stage of this chain.

### where the hand-authored inputs are, counted

| what | file, full path | count |
|---|---|---|
| operator spellings, all 13 languages | `PseudoCoupHQ/Research/kind_fuzz_clustering/operator_arity.py` | 136 `G()` rows, 1,561 spellings |
| operator spellings, rust alone | same | 97 (33 of them reach this branch: 8 prefix, 3 postfix, 22 binary) |
| holder rows (which types are probed) | `PseudoCoupHQ/Research/op_pipeline/probe_gen.py`, lines 76–119 | 30 rows (5 languages × 6 types), 44 lines |
| result-type rules for go, rust, swift | same, lines 157–217 | 58 lines; `RUST_TRAIT` 10 entries, `CMP` 6, `LOGIC` 2 |
| per-language source templates | same, `emit_c` / `emit_cpp` / `emit_go` / `emit_rust` / `emit_swift` | 5 templates, `emit_rust` is 14 lines |
| operator exclusions | same, lines 127–136 | 2 |
| bucket exclusions | same, lines 55–67 | 3 |
| compile-flag table and tool checks | `PseudoCoupHQ/Research/op_pipeline/lane_gen.py` | 5 tool checks, 10 compile commands (5 languages × ANCHOR/SHIP) |
| named refusal categories in the lifter | `PseudoCoupHQ/Research/op_pipeline/expr_to_canon.py`, `REFUSAL_CATEGORY` | 37 |
| register map for rendering | same, `REGMAP` | 6 |
| arithmetic rendering rows | same, `ALU_OP` | 5 |
| comparison rendering rows | same, `CMP_OP_TO_SUFFIX` + `NEGATE_SUFFIX` | 10 + 10 |
| condition-suffix table | `PseudoCoupHQ/Research/op_pipeline/condition_table.py`, `SUFFIX_TO_COND` | 28 |
| standard register names | `PseudoCoupHQ/Research/op_pipeline/canon.py`, `GP_NAMES` | 8 families |
| temp register pool, ordered | `PseudoCoupHQ/Research/op_pipeline/canon7_render.py`, `TEMP_POOL_ORDER` | 9 |
| reading-form templates | `PseudoCoupHQ/Research/op_pipeline/reading_form.py` + `SPEC_reading_form.md` | ~35 dispatch arms; 55 spec template rows + 16 vocabulary rows; `FLAG_NAME` 15 |
| opcode glossary | `PseudoCoupHQ/Research/op_pipeline/GLOSSARY_arch_opcodes.md` | 93 mnemonics, 227 lines (prose authored; the occurrence counts are derived from the corpus) |

For contrast, the derived side of the same folder: 97 python files
totalling 39,637 lines, 181 JSON artifacts, 39 markdown artifacts,
189 MB.

---

## 3. The automation scorecard

One row per stage. Every cell carries a measured number.

| stage | runs with zero human input | runs after a config or table edit | requires new human authorship |
|---|---|---|---|
| 0 — operator inventory | 0. The file cannot discover an operator; `--verify` only asks whether each RECORDED spelling occurs in the grammar. On rust that is 44 of 44 confirmed, with 129 grammar anonymous kinds never checked in the other direction (measured in log 076, unchanged today) | a grammar pin bump plus re-fetch of `grammar_cache/` | 1 `G()` row per new rule; 1 spelling per new operator. rust's share of the table is 97 spellings |
| 1 — probe generation | 0.10 s for all five languages, and it is a FIXED POINT: regenerating all five manifests reproduces every one of the 4,440 probe records exactly (differing probe records: 0; keys present in only one: 0). The only top-level difference is a later-added `"role": "generator provenance"` key in `meta` | changing the holder list or a result rule regenerates everything below | a new language costs 1 holder row set (6 rows), 1 result-type rule (14–24 lines) and 1 emitter (14–19 lines). A new operator KIND — a method call, for instance — costs a new bucket read plus a new spelling function; measured in §5 |
| 2 — lane generation | 0.08 s, and BYTE-IDENTICAL to the five committed lanes (`cmp` clean on all five). No drift of the kind log 076 found in the census harness | a compiler-flag change is 1 line per mode | a new language costs 1 tool-check row and 2 compile commands |
| 3 — extraction | one file write. rust 29.8 s / 858 probes / 1,108 records; the compiler decides all 858 acceptances and writes all 733 refusal texts. 0 hand-maintained acceptance data anywhere in the stage | a toolchain change is 1 `PATH` line inserted after `set -u` — measured today, diff of exactly 1 functional line against a 469-line lane | 0 |
| 4 — fold | 0.05 s. Re-folding today's 1.96.1 output reproduces the committed `op_units_rust.json` at every one of the 858 probe records (0 differing) | 0 | 0 |
| 5 — lift and normalize | not run today (unverified). The stage is machine-driven, but it rests on a hand table: 37 named refusal categories, and the register map has 6 entries, all general-purpose | 0 | a machine shape with no rule refuses by name rather than guessing. `stage5_float_conditions_diagnosis.txt` measures one such gap at 260 units and names FOUR separate places that must agree before it closes |
| 6 — canonical rendering and gate | not run today (unverified). For rust the stored result is 98 converged of 125, gate tally 51 PROVED_EQUAL / 22 DISPROVED / 0 UNDECIDED on the units this generation attempted | 0 | one rendering rule per unseen shape. canon13's own record: 44 attempted, 12 accepted, 32 correctly disproved and refused |
| 7 — reading form | not run today (unverified); 237 rust units rendered on record | 0 | 1 template row per unseen mnemonic; an unknown opcode refuses by name rather than being guessed at |
| 8 — component mining | 275 alphas mined from 1,731 units, no authored list | 0 | 0 |
| 9 — class table and dom_ops | 0.20 s, and a FIXED POINT: the re-run reproduces the committed `dominant_table12.json` and `dom_ops10.json` exactly. 926 classes, 135 nodes, 26 dom_ops, 23 edgeless, 1,641 members | 0 | 0 |
| 10 — verdicts | 15.62 s for 4,240 fresh z3 verdicts, tally 1,812 UNMATCHED / 2,530 UNDECIDED / 22 DIFFERS-BY-DESIGN / 6 MATCHED | 0 | 0 — but the UNDECIDED bin is 58% of the pairs, and shrinking it is renderer work, which is authorship |
| 11 — bridges and dominance | 1,113 classes, 322 bridges, 756 different-live-result cases standing | 0 | 0 |
| 12 — spelling guard | 0.03 s; PASS on both of today's class tables. Inventory of 78 tokens derived from the manifests | 0 | 0 |

**Where a stage looks automated but rests on a hand table underneath,
stated plainly.** Three places.

- Stage 3 is the most automatic thing in the branch — the compiler
  decides everything — but it can only ever be handed probes that
  stage 1 could spell, and stage 1 can only spell what stage 0's typed
  table contains. The acceptance oracle is real; the QUESTION it
  answers is a person's list.
- Stages 5 and 6 are machine-driven and their refusals are honest, but
  their coverage is a hand table. A shape with no rule is refused, not
  guessed — which is correct, and which also means coverage grows only
  by authorship.
- Stage 9's class key contains the canonical text, so the class table
  inherits stage 6's coverage. 27 of rust's 125 units are not converged
  and therefore carry a weaker text into the key.

---

## 4. The blast radius of a compiler move — measured

### what was run

Two lanes, generated by the branch's own `lane_gen.py` called
directly, so nothing in the repository was written to:

| lane | file | compiler | elapsed | output |
|---|---|---|---|---|
| A | `Airlock/agent/drop/d78_rust196.sh` | `rustc 1.96.1 (31fca3adb 2026-06-26)`, the image default | 29.8 s | `Airlock/agent/out/d78_rust196.txt`, 104,927 bytes |
| B | `Airlock/agent/drop/d78_rust198.sh` | `rustc 1.98.0 (88d9e12ae 2026-08-18)`, from `/persist/rustup076/` | 23.8 s | `Airlock/agent/out/d78_rust198.txt`, 105,041 bytes |

Lane B is lane A with one line inserted after `set -u`:

```
export PATH=/persist/rustup076/toolchains/1.98.0-x86_64-unknown-linux-gnu/bin:$PATH
```

Both lanes printed their compiler's own version banner before doing
anything, so the toolchain in force is on the record rather than
assumed. The pin was not moved; `Airlock/Containerfile`
line 82 still says `--default-toolchain 1.96.1`.

### the control: is the pipeline reproducible at all?

`Airlock/agent/out/d78_rust196.txt` is **byte-identical**
to `Airlock/agent/out/op_rust.txt`, the extraction
recorded on 2026-08-25. Same 104,927 bytes, `diff` clean. Re-folding it
reproduces the committed `op_units_rust.json` at every one of the 858
probe records.

So any difference seen at 1.98.0 is the compiler's, not the day's.

### do the emitted instructions differ?

| measure | 1.96.1 | 1.98.0 | changed |
|---|---|---|---|
| candidate probes | 858 | 858 | 0 |
| refused by the compiler | 733 | 733 | 0 |
| accepted | 125 | 125 | 0 |
| accept/refuse verdicts that flipped | — | — | **0** |
| refusal texts that changed | — | — | **0** |
| SHIP byte strings that changed | — | — | **0 of 125** |
| ANCHOR byte strings that changed | — | — | **0 of 125** |
| DWARF parameter tables that changed | — | — | **0 of 125** |
| manifest meta that changed | — | — | 0 |
| total records written | 1,108 | 1,108 | — |
| records whose TEXT differs | — | — | **47 (4.2%)**: 41 ANCHOR, 6 SHIP |

Every one of the 47 has identical bytes. The difference is in the name
appended to a `call` instruction by the extractor, which reads it out
of the relocation entry because an object file's call displacement is
literally zero.

**Cause one, 41 records: the `core` library's build hash.** rust/op_642
is `a / b` on two 32-bit signed integers — the division-with-guards
shape. Its SHIP record, verbatim from the two lane outputs, with the
identical parts elided only where marked:

> `Airlock/agent/out/d78_rust196.txt`, record
> `op_642|SHIP|OK`, last two instructions:
>
> ```
> lea 0x0(%rip),%rdi !!reloc=R_X86_64_PC32:.data.rel.ro..Lanon.e999d8e928eeaaa2810ddee94f44a439.1-0x4
> call *0x0(%rip) !!reloc=R_X86_64_GOTPCREL:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow-0x4
> ```

> `Airlock/agent/out/d78_rust198.txt`, the same record:
>
> ```
> lea 0x0(%rip),%rdi !!reloc=R_X86_64_PC32:.data.rel.ro..Lanon.e999d8e928eeaaa2810ddee94f44a439.1-0x4
> call *0x0(%rip) !!reloc=R_X86_64_GOTPCREL:_RNvNtNtCsc36rpYXAlPq_4core9panicking11panic_const24panic_const_div_overflow-0x4
> ```

The byte strings for both records are the same 52 bytes, beginning
`50 85 f6 74 15 89 f0 f7 d0`. The eleven instructions that do the work
— `test`, `je`, `not`, `lea`, `or`, `je`, `mov`, `cltd`, `idiv`, `pop`,
`ret` — are character-for-character identical. What moved is
`Cs3BFokC4QLxY_` to `Csc36rpYXAlPq_`: rustc's disambiguator for the
`core` crate, which changes when `core` is rebuilt. The panic-location
constant's own hash, `.Lanon.e999d8e9…`, did NOT move, because it is a
hash of content we wrote.

Substituting a regular expression for that one token accounts for 41
of the 47 records exactly and leaves nothing over.

**Cause two, 6 records: the default symbol-mangling scheme changed.**
The six are rust's inclusive range operator `..=` at all six holder
types, ANCHOR build only.

> `Airlock/agent/out/d78_rust196.txt`,
> `op_786|ANCHOR|OK`, the call instruction:
>
> ```
> call *0x0(%rip) !!reloc=R_X86_64_GOTPCREL:_ZN4core3ops5range25RangeInclusive$LT$Idx$GT$3new17h873159e1f524bd14E-0x4
> ```

> `Airlock/agent/out/d78_rust198.txt`, the same record:
>
> ```
> call *0x0(%rip) !!reloc=R_X86_64_GOTPCREL:_RNvMs5_NtNtCsc36rpYXAlPq_4core3ops5rangeINtB5_14RangeInclusivelE3newCs2B1nOxgNFGD_4unit-0x4
> ```

Both records carry the same 36 bytes and the same nine instructions.
The 1.96.1 spelling is the legacy scheme (`_ZN…E`, with a
sixteen-hex-digit hash); the 1.98.0 spelling is the v0 scheme (`_RN…`,
with the crate names written out and our own crate's disambiguator
`Cs2B1nOxgNFGD_4unit` at the end). Note that at 1.96.1 the calls INTO
`core` were already v0 while the locally instantiated generic was
legacy; at 1.98.0 both are v0. That is a default flipping, and it is
the second and last cause.

### do unit identifiers stay stable?

**Perfectly stable across the compiler move, and not stable at all
across an inventory move.** Both facts are measured.

Across the compiler move: the two lane outputs contain the same 1,108
record keys, with 0 keys present in only one of them. `op_N` is
assigned by `probe_gen.py` while it walks the operator inventory
crossed with the holder list; no compiler is consulted, so no compiler
change can move it.

Across an inventory move, the number is large. One operator was added
to rust's binary bucket in a scratch copy and the manifests regenerated:

| where the new operator is inserted | candidates | probe identifiers that MOVED |
|---|---|---|
| appended at the END of rust's binary bucket | 858 → 894 | **0 of 858** (0.0%) |
| inserted at the HEAD of rust's binary bucket | 858 → 894 | **792 of 858** (92.3%) |

Identity was compared on `(operator, arity, position, left type, right
type)`, not on the number, so this measures real renumbering.

**This is the real identifier risk, and it is ours, not the
compiler's.** A language update that adds an operator will renumber
everything after it unless the new spelling is appended. Nothing in
the code enforces append-only ordering today.

### does the canonical rendering still converge, and does the proof still pass?

Yes, and the reason is forced by construction rather than argued.

The canonical lineage derives from the SHIP build. All 125 SHIP byte
strings are identical between the two compilers, and the SHIP mnemonic
text differs for exactly 6 units. Those 6 are
`op_642, op_649, op_656, op_678, op_685, op_692` — the guarded integer
divisions and remainders. Their recorded status in
`PseudoCoupHQ/Research/op_pipeline/canon13_units_rust.json`:

| unit | operator | status | branch kind | converged |
|---|---|---|---|---|
| op_642 | `/` i32 | `no_canon4_text` | — | no |
| op_649 | `/` i64 | `no_canon4_text` | — | no |
| op_656 | `/` u64 | `unchanged` | branching | no |
| op_678 | `%` i32 | `no_canon4_text` | — | no |
| op_685 | `%` i64 | `no_canon4_text` | — | no |
| op_692 | `%` u64 | `unchanged` | branching | no |

None of them is converged; none carries canonical text; none is in the
0-branch population the class table is built over. Checked directly:
of rust's 98 converged units, **0** have a SHIP record that changed.

Then the downstream stage was actually run, twice, rather than
reasoned about. A scratch tree was built holding
`dominant_table12.py`, its three imported co-modules, the eight canon
generations for all five languages and the three `result_types_*.json`
files. One copy was left alone; in the other, the six changed
mnemonic lists were substituted into `canon4_units_rust.json` from the
1.98.0 fold. Both were run:

| output | 1.96.1 input | 1.98.0 input | identical |
|---|---|---|---|
| `dominant_table12.json` | 926 classes, 1,641 members | 926 classes, 1,641 members | **yes, byte for byte** |
| `dom_ops10.json` | 135 nodes, 26 dom_ops, 23 edgeless | 135 nodes, 26 dom_ops, 23 edgeless | **yes, byte for byte** |
| `check_no_spelling_keys.py` on the class table | PASS | PASS | — |

The 1.96.1-input run also reproduces the committed
`PseudoCoupHQ/Research/op_pipeline/dominant_table12.json`
exactly, so the stage is a fixed point on its own output — the property
log 076 found MISSING in the census harness's generator.

The proof itself (the behaviour gate, z3 over the candidate text
against the real ship code) was not re-run — it needs the full canon
lineage and a lane, and it is unverified here. But its input for every
converged rust unit is identical at both compilers, so it has nothing
new to decide.

### how many stored artifacts would go stale if the pin moved?

Two questions, answered separately because they have very different
sizes.

**Artifacts that carry a version-sensitive STRING** — the thing that
would actually be wrong:

| measure | count |
|---|---|
| files under `PseudoCoupHQ/Research/` naming the 1.96.1 `core` disambiguator | **41** |
| — in `Research/op_pipeline/` | 33 |
| — in `Research/stage_asg/` | 7 |
| — in `Research/kind_fuzz_clustering/` (`arch_units_rust.json`) | 1 |
| total occurrences of that string | **3,668** |
| files carrying the legacy-mangled `RangeInclusive::new` name | 2, with 12 occurrences |
| of the 41 files, how many are hand-authored | **0** — all are `.json`, plus `verdicts.md`, `verdicts4.md` and `dominant_explorer.html`, every one written by a script in the same folder |
| canon generations 5 through 13 for rust that carry any symbol name | **0** — `reloc=`, `_ZN` and `_RN` all count zero in `canon5` … `canon13_units_rust.json` |
| canon generations 2 through 4 that do | 3 files, 24 `reloc=` lines, 10 v0-mangled names each |

The last two rows are the important pair: the HOME representation is
already free of compiler identity strings. Only the three generations
that store raw `objdump` text carry them.

**Artifacts that merely NAME a rust unit** — the scope a full
re-derivation would rewrite, whether or not anything in them is wrong:

| measure | count |
|---|---|
| JSON artifacts in `op_pipeline/` naming a rust unit | **88** |
| `rust/op_N` references across them | **20,747** |
| `"rust"` language tags across them | 27,957 |
| rust member rows in `dominant_table12.json` | 112 of 1,641 |
| classes containing a rust member | 109 of 926 |
| of those, classes where rust sits with at least one other language | 90 |

**Derivable by re-run versus hand-authored.** All 41 stale files and
all 88 rust-naming artifacts are derivable. The cost of re-deriving
everything from the compiler up to the fold is:

| stage | time |
|---|---|
| `probe_gen.py` (5 languages) | 0.10 s |
| `lane_gen.py` (5 languages) | 0.08 s |
| the rust extraction lane | 29.8 s |
| `fold.py rust` | 0.05 s |
| **total** | **30.0 s** |

Downstream of the fold the canon lineage and verdicts are the expense,
and they were not timed today (unverified); the two stages that were —
`dominant_table12.py` at 0.20 s and the verdicts6 run at 15.62 s on
record — are small.

Nothing hand-authored goes stale. The version move touches zero of the
tables counted in §2.

---

## 5. The new-feature path, and where it stops

### is the probe generator fed from a machine-readable source?

No. It is fed from `operator_arity.json`, which is generated from a
python table a person typed, verified in one direction against the
pinned grammar. The file is candid about this in its own header:

> `PseudoCoupHQ/Research/kind_fuzz_clustering/operator_arity.py`
> "Every row below is read out of a tree-sitter grammar source
> (`grammar.js`, …). … `--verify` re-reads the grammar source and
> checks that the spelling really does occur inside that rule".

Verification, not discovery. A spelling the table has that the grammar
lost is caught; a spelling the grammar GAINED is invisible. Log 076
measured that gap at 129 unchecked grammar kinds for rust; it is
unchanged.

### are the five new methods anywhere in that source?

Measured: `algebraic` appears **0 times** in
`PseudoCoupHQ/Research/kind_fuzz_clustering/operator_arity.json`
and **0 times** in
`PseudoCoupHQ/Research/kind_fuzz_clustering/grammar_cache/rust.js`.

That second zero is not a gap in the table — it is correct. A method is
not an operator spelling, so the grammar has nothing to say about it.
The grammar's rust inventory puts method access in the structural
bucket as `.`, and `probe_gen.py` reads three buckets only, excluding
structural by a written reason:

> `PseudoCoupHQ/Research/op_pipeline/probe_gen.py`,
> `EXCLUDED_BUCKETS`:
> "structural": "indexing, calls, member access and the like operate
> on aggregates, not on the scalar core; out of scope for this first
> run"

**Stopping point one: the probe generator cannot spell a method call.**
There is no bucket to read it from and no spelling function for it.
`spell_binary(op)` returns `"a %s b"`; a method call needs
`"a.%s(b)"`. That is new authorship, and it is small: one bucket read,
one spelling function, one result rule, one manifest field — about 35
lines against `probe_gen.py`'s 502.

### do the emitters need a new spelling row?

The result-type rule does NOT need one, and the reason is worth
stating because it is luck rather than design. `probe_gen.result_rust`
was called, unmodified, on each of the five method names. All ten
calls returned the left operand's type with the rule name
`fallback_lhs`. That answer is correct — `f64::algebraic_add` returns
`f64` — but the manifest's own note says a `fallback_lhs` probe is not
to be trusted:

> `PseudoCoupHQ/Research/op_pipeline/probe_gen.py`,
> `result_rule_note`:
> "`fallback_lhs` means no rule was known and the left operand's type
> was used, so a refusal there may be the fallback's and not the
> operator's"

So the emitter needs a spelling row; the result rule happens not to,
and would be recorded as unreliable if left as is.

### would the arch-unit extraction handle a method-call spelling? — tested

Yes, with no tool edit at all. Twelve probes were hand-written — the
five methods at `f32` and `f64`, plus the ordinary `+` at both widths
as a control, the control emitted by `probe_gen.emit_rust` itself —
and handed to `lane_gen.lane()` unmodified. Two lanes were run.

| lane | compiler | elapsed | result |
|---|---|---|---|
| `Airlock/agent/drop/d78_alg196.sh` | 1.96.1 | 0.4 s | 10 of 10 algebraic probes REFUSED; 2 of 2 controls extracted |
| `Airlock/agent/drop/d78_alg198.sh` | 1.98.0 | 0.6 s | 10 of 10 algebraic probes accepted, SHIP and ANCHOR units extracted, DWARF read for all |

The refusal, verbatim, ten identical lines:

```
op_900|REFUSED|error[E0658]: use of unstable library feature `float_algebraic`
```

**That is the compile-or-refuse rule detecting a language version
difference, for free, with zero tool changes and zero hand-maintained
data — in four tenths of a second.** It is the same signal log 076
found, reproduced here inside this branch's own lane rather than a
census one.

The 1.98.0 units came out clean. Two examples, verbatim from
`Airlock/agent/out/d78_alg198.txt`:

```
op_901|SHIP|OK|f2 0f 58 c1 c3|addsd %xmm1,%xmm0;ret
op_901|ANCHOR|OK|48 83 ec 18 f2 0f 11 44 24 08 f2 0f 11 4c 24 10 e8 00 00 00 00 48 83 c4 18 c3|sub $0x18,%rsp;movsd %xmm0,0x8(%rsp);movsd %xmm1,0x10(%rsp);call 15 <op_901+0x15> !!reloc=R_X86_64_PLT32:.text._RNvMNtCsc36rpYXAlPq_4core3f64d13algebraic_addCs2B1nOxgNFGD_4unit-0x4;add $0x18,%rsp;ret
op_901|ANCHOR|DWARF|a=2 byte block: 91 8 (DW_OP_fbreg: 8);b=2 byte block: 91 10 (DW_OP_fbreg: 16)
```

### stopping point two — the one that matters

Here is the control, from the same file, the ordinary `+` on two
64-bit floats emitted by the branch's own `emit_rust`:

```
op_911|SHIP|OK|f2 0f 58 c1 c3|addsd %xmm1,%xmm0;ret
```

The two SHIP records are the same five bytes and the same two
instructions. Now the class key, which is (operand type pair, result
type, canonical text). The stored canonical text of rust's ordinary
float add:

> `PseudoCoupHQ/Research/op_pipeline/canon13_units_rust.json`,
> unit 562 (`+`, f64, f64), field `canon10_text`:
>
> ```
> addsd %xmm1,%xmm0; ret
> ```

And the class that text sits in:

> `PseudoCoupHQ/Research/op_pipeline/dominant_table12.json`,
> class C0338, type pair `f64,f64`, result `f64`:
> members `c/op_130`, `cpp/op_130`, `go/op_340`, `rust/op_562`,
> `swift/op_250`

An `algebraic_add` unit would render to the same string, carry the
same operand types and the same result type, and become the sixth
member of C0338. The pipeline would call it MATCHED and record no
divergence.

**It is not the same operation.** Log 076 measured, on this same
compiler, that `algebraic_add` gives 1.0 at one optimization setting
and 2.0 at another on the same expression, while ordinary `+` gives
1.0 at every setting. The probe shape cannot see that, by
construction: a probe applies one operator to at most two parameters,
and there is nothing to rearrange in `a + b`. Rearrangement is a
property of `((a + b) + c) + d`.

So the measured stopping point is a probe-shape limit, not a missing
table row. Three sentences: **the five methods extract cleanly and
would converge to canonical text that already exists in the table;
they would therefore merge silently into the ordinary float-add class
and the branch would record that rust's algebraic add and rust's `+`
are one operation; they are not, and the two-operand probe cannot tell
them apart because reassociation needs three operands or more.**

### stopping point three, smaller

`algebraic_rem` at the SHIP build is not an instruction at all:

```
op_909|SHIP|OK|ff 25 00 00 00 00|jmp *0x0(%rip) !!reloc=R_X86_64_GOTPCREL:fmod-0x4
```

The whole unit is a tail jump into libc's `fmod`. Whatever the branch
decides about library calls as units applies here; today there is no
rule, so it would be a unit whose body is one unresolved call.

---

## 6. The update handler — what "rust moved to 1.98" should do

Ranked by measured cost against measured benefit. Nothing below is
decided; the naming and scope questions are named in §7.

### the free change-detectors that already exist

Before proposing anything, three detectors are already in hand and
cost nothing to wire.

| detector | what it is | measured cost today |
|---|---|---|
| compile-or-refuse against the OLD toolchain | build the new candidate probes at the previous compiler and read the refusals | 0.4 s for 12 probes; 10 of 10 named `E0658 float_algebraic` by name. Already ratified as first-class evidence |
| the machine-readable stabilized-API list | the release notes' "Stabilized APIs" section plus the standard library's own `since = "1.98.0"` attributes, two independent sources that agree | ~40 lines, 2.1 s, 2 network fetches — written and run in log 076 |
| the grammar's own enumeration | `operator_arity.py --verify` against `grammar_cache/`, plus the set difference in the direction it does not yet take | the reverse difference is a few lines inside a function that already computes both sets |

### the ranked list

| rank | build this | measured cost | measured benefit |
|---|---|---|---|
| 1 | **the re-extract-and-diff command.** One script that: stamps the toolchain into the manifest `meta`; regenerates the lane with a toolchain `PATH` line; runs it under a scratch output name; folds it beside the stored fold; and classifies the record-level difference by cause | every stage it calls already exists and every one is a fixed point. The four together are **30.0 s for rust** (0.10 + 0.08 + 29.8 + 0.05). The genuinely new code is the cause classifier, about 40 lines, written and run today, plus a `--toolchain` argument on `lane_gen.py` and an `--out` on `fold.py` (which already has one) | today the branch cannot say whether a compiler move changed anything. With this it says, in half a minute: **47 of 1,108 records, two named causes, 0 bytes, 0 verdicts, 0 classes.** It is also the regression test the branch does not have — today's control run proved the 2026-08-25 extraction reproduces byte for byte, which nothing was checking |
| 2 | **take the compiler's identity strings out of the instruction column.** Keep the relocation, but split the callee name into its own field, or normalize the crate disambiguator to a placeholder and record the real one once per run | 3 lines in `lane_gen.py`'s embedded driver, at the point where `!!reloc=` is appended to the instruction, plus one re-extraction per language | collapses **47 of 47** measured differences to zero, and retires **3,668** version-carrying strings across **41** machine-written files. After it, a rust point release produces a genuinely empty diff and the diff itself becomes trustworthy |
| 3 | **append-only operator identifiers.** A rule, plus a check, that a new spelling is appended to its bucket rather than inserted, and that `op_N` for an existing `(operator, arity, position, left type, right type)` never moves | the check is a set comparison between the old and new manifests; the measured facts it protects are already computed | measured: inserting one operator at the head of rust's binary bucket moves **792 of 858** identifiers (92.3%); appending it moves **0**. Without the rule, the first language update that adds an operator invalidates every `rust/op_N` reference in **88** artifacts and **20,747** places |
| 4 | **the reverse set difference on the operator inventory**, and a method-call probe kind behind it | the reverse difference is a few lines in `crosscheck_compiled()`, which already builds both sets (this is log 076's item 2, still open). The probe kind is ~35 lines in `probe_gen.py` against its 502 | today **0 of 5** of rust 1.98.0's new operations can enter the branch, and **129** grammar anonymous kinds for rust are never checked back. This is the difference between a language update being visible and being invisible |
| 5 | **a divergence probe shape for build-sensitive operations.** A second probe family with three or more operands, built at both ANCHOR and SHIP, whose finding is the DIFFERENCE between the two builds rather than the units themselves | a new emitter shape per language; the ANCHOR/SHIP two-build discipline it needs already exists and already runs on every probe | this is the only thing that stops rust's algebraic add merging silently into ordinary add — measured today as identical five-byte units in the same class key. Without it the branch would record a false MATCHED for the first genuinely new arithmetic mode in the line |
| 6 | **a per-language update manifest** — see below | one JSON file per language, roughly 20 fields; the values for rust are all measured in this log and log 076 | makes rank 1 mechanical instead of remembered, and makes a twelve-language sweep a loop rather than twelve sessions |

### what a per-language update manifest would hold

Proposed contents, each field with rust's measured value so the shape
is inspectable rather than described:

| field | rust's value today |
|---|---|
| language | `rust` |
| pinned version and where the pin lives | `1.96.1`, `Airlock/Containerfile` line 82 |
| how to reach an alternative toolchain | `PATH` prefix `/persist/rustup076/toolchains/<version>-x86_64-unknown-linux-gnu/bin` |
| version banner command and expected shape | `rustc --version` → `rustc 1.98.0 (88d9e12ae 2026-08-18)` |
| release-notes source | the project's `RELEASES.md`, section per version |
| stabilized-API source, independent of the notes | `library/core/src/num/f64.rs` and `f32.rs`, `since = "<version>"` attributes |
| grammar pin and its cache | tree-sitter-rust 0.24.2; `Research/kind_fuzz_clustering/grammar_cache/rust.js` |
| operator inventory rows owned | 97 spellings; 33 reach this branch |
| holders | 6 (`i32 i64 u64 f32 f64 bool`) |
| candidate probes | 858 |
| ANCHOR and SHIP commands | `rustc -C opt-level=0 -g` / `rustc -C opt-level=1 -C debug-assertions=off` |
| extraction lane and its recorded time | `op_pipeline/lanes/op_rust.sh`, 24–30 s |
| stored extraction to diff against | `Airlock/agent/out/op_rust.txt`, 104,927 bytes |
| known version-sensitive text patterns | the crate disambiguator `Cs[A-Za-z0-9]+_`; the mangling scheme prefix `_ZN` versus `_RN` |
| artifacts naming this language's units | 88 JSON files, 20,747 references |
| units accepted / converged | 125 / 98 |
| identifier-ordering rule | append-only within a bucket |

---

## 7. What must remain human, and open items for the owner

### what cannot be automated

Four things, each with the measured place it bites.

- **Naming.** Log 076 already put one name in front of the owner — a fourth
  guaranteed arithmetic mode, candidate `rearranging` against rust's
  own word `algebraic`. Nothing in this branch can choose it, and this
  audit adds no new argument, only a new consequence: whichever name
  is chosen has to reach the class key, or the merge measured in §5
  happens silently.
- **Ontology.** Is a library method an operator of the language? The
  standing ruling is that builtins are out of scope until the owner opens
  them. `algebraic_add` is a method on a primitive type; it is
  arithmetic; and the developer chose it by name. Whether that makes
  it an operator for this branch is not a measurement.
- **Mode classification.** Whether rust's algebraic add is a
  guarantee, an anti-guarantee, a compile-time refusal or something
  new is the owner's, and log 076 §4 already lays out the four measured
  facts. This audit contributes one more: **at the arch-unit grain the
  algebraic and ordinary adds are indistinguishable**, so the
  classification cannot come from this branch's evidence at all — it
  has to come from the build-difference measurement, which is a
  different probe shape.
- **Scope of an update.** Whether a release's new items enter at all,
  and in which order, is a work-planning decision. The detectors can
  produce the list; they cannot decide the list is worth doing.

### open items

- **The pin was not moved and the image was not rebuilt.** rust 1.98.0
  lives at `/persist/rustup076/`, which survives a container restart
  but is not part of the image. Bumping
  `Airlock/Containerfile` line 82 would REPLACE 1.96.1
  rather than co-install beside it. the owner's call; unchanged from log 076.
- **Append-only ordering is not ruled.** The 92.3% renumbering measured
  in §4 is a real hazard the moment any language gains an operator.
  Whether identifiers must be stable across inventory edits, or whether
  a renumbering is acceptable with a re-derivation, is a ruling this
  audit cannot make.
- **The relocation-name question is a design question, not just a
  cleanup.** Taking the callee name out of the instruction column
  removes the version sensitivity, but the name is also the only
  evidence of WHICH guard a unit calls — `panic_const_div_by_zero`
  versus `panic_const_div_overflow` is the divergence condition for
  rust's guarded division. It must move to a field, not be discarded.
- **The five methods were extracted but nothing was installed.** No
  manifest, no census page, no canon artifact and no table was edited.
  The twelve probes exist only inside
  `Airlock/agent/drop/d78_alg196.sh` and
  `d78_alg198.sh`, from which they can be lifted verbatim.
- **The canon lineage was not re-run at 1.98.0** (unverified). It needs
  pyvex and z3, both confirmed present in the container today
  (`pyvex 9.2.213`, `archinfo 9.2.213`, `capstone 5.0.7`, z3 importable),
  so the run is possible; it was not attempted because the converged
  population's input is byte-identical and the class table was measured
  directly instead.
- **`result_types_go.json` and `result_types_swift.json` do not
  exist.** Only c, cpp and rust have one. This shows up as
  `dominant_table12.py`'s own line "unknown result type (excluded from
  a scalar family) 37". Noticed while building the scratch tree;
  flagged, not chased.
- **`bash PseudoCoupHQ/hq.sh check` ends at 0 errors**
  (9 warnings, all pre-existing conformance gaps in PseudoCoup_v6 and
  PseudoIR that the sweep names itself). Unchanged from log 076.

---

## Artifacts this log left behind

Lanes, in `Airlock/agent/drop/` and archived by the
daemon into `.done/`:

| lane | what it measured | elapsed |
|---|---|---|
| `d78_rust196.sh` | the full rust extraction at the image compiler | 29.8 s |
| `d78_rust198.sh` | the same, one `PATH` line different, at 1.98.0 | 23.8 s |
| `d78_alg196.sh` | the five algebraic methods at 1.96.1 — the refusal detector | 0.4 s |
| `d78_alg198.sh` | the same twelve probes at 1.98.0 — extraction to arch-units | 0.6 s |
| `d78_mods.sh` | which python modules the container carries | 0.5 s |

Outputs, in `Airlock/agent/out/`: `d78_rust196.txt`
(104,927 bytes), `d78_rust198.txt` (105,041 bytes),
`d78_alg196.txt`, `d78_alg198.txt`.

Logs, in `Airlock/agent/logs/`, stamped `20260829T21*`
and `20260829T22*`.

Nothing under `PseudoCoupHQ/Research/`,
`PseudoCoupHQ/Planning/` or any census page was edited.
Every re-run of a repository tool was done into a scratch tree.
