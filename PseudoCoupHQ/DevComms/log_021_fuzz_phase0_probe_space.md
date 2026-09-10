# log 021 — kind_fuzz_clustering phase 0: the probe space and its size

date: 2026-08-15
node: `PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`
artifacts: `PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/`
status: phase 0 complete — measurement only; no probe was generated and
nothing was executed in any of the eleven languages.

---

## §1 — what phase 0 did, in plain words

Four words in this log have been away long enough to need a line each
before they are used.

- A **kind** is one entry in a language's tree-sitter grammar
  vocabulary: `binary_expression`, `for_statement`, `integer_literal`
  are kinds, and so are the bare operators and keywords such as `+` and
  `fn`. The whole point of this research line is to group kinds across
  languages by what they DO.
- **`node-types.json`** is a file each tree-sitter grammar ships. It
  lists every kind, and for each kind it lists the slots it has and
  which kinds may legally stand in each slot. All 411 of them were
  downloaded on 2026-08-12 by the co-node `kind_signature_clustering`
  and sit in
  `PRIVATE/PseudoCoupHQ/Research/kind_signature_clustering/raw_all/`.
- The **six dominants** are boolean, float, integer, string, list and
  dict. They are the data structures whose behaviour was verified by
  execution across the eleven languages on 2026-08-14 (467 confirmed, 7
  refuted, empty residue), recorded in
  `PRIVATE/PseudoCoupHQ/Research/dominant_intentions/verified/`.
  They are the calibrated inputs: a probe's answer is only readable
  because what went in is known exactly.
- A **probe** is one small generated script that puts a known input
  into one kind and records what comes back — an answer, a raise, or a
  compile refusal. No probe exists yet. Phase 0 only counted how many
  there will be.

The work was three passes over the grammar files, and nothing else.

The first pass pulled each target language's vocabulary out of its
grammar file: the named kinds, and the anonymous tokens, which are the
operators and keywords. Across the eleven target languages that is
1,776 named kinds and 1,422 anonymous tokens. Rust's named count came
out at 163, which is the number the CORE already carried, so the
extraction agrees with the figure the plan was written against.

The second pass built the table the CORE said would replace blind
enumeration. For every kind, the grammar states which kinds may stand
in each of its slots. Written out, that is 8,371 statements as the
grammar spells them, and 36,236 once every abstract grouping the
grammar uses — such as python's `expression`, which stands for 32
concrete kinds, or python's `_simple_statement`, which stands for 51 —
is expanded into the concrete kinds it covers.

The third pass asked, of every slot, whether one of the six dominants
could legally stand in it, and counted one probe for each dominant that
can. **The answer is 3,556 probes for the eleven languages, between 168
and 445 per language.** That is the first number the plan asked for.

That number rests on one choice worth stating in the walkthrough rather
than burying in the rule: it counts a kind once per dominant, so
`binary_expression` is a handful of probes whether the operator in it
is `+` or `*`. The eleven grammars declare menus of operators for those
slots — thirteen for python's `binary_operator`, thirty for php's
`binary_expression` — and `1 + 2` and `1 * 2` are plainly not the same
measurement. Counting each operator on the menu separately raises the
total to 7,140. Both readings are given below; which one the owner wants is
decision 2 in §2.

Two things were found that the plan did not anticipate, and both change
what phase 1 has to do.

- **The grammar prunes even harder than the CORE hoped.** For rust the
  CORE's blind figure was 163 x 163 = 26,569 pairs. The grammar's own
  legality cuts that to 3,289, and the dominant-typed slots cut it to
  311 probes — one and a quarter percent of the blind number.
- **The grammar does not encode the dependency chains the owner described,
  as opposed to encoding them where they are written as slots.** `else`
  after `if` IS in the file: python declares `else_clause` as a filler
  of `if_statement`'s `alternative` slot, so it measures at depth 2.
  `break` inside `for` is NOT in the file: python declares
  `break_statement` as a legal top-level statement of a file, so it
  measures at depth 1, even though CPython rejects `break` outside a
  loop. Grammar depth is therefore a LOWER BOUND on the enclosing
  context a probe really needs, not the answer. The evidence for both
  halves is quoted in §4.

Feasibility, plainly: the count is small. 3,556 probes across eleven
languages, 974 of which are a single top-level line needing no
enclosing kind at all, is a run that fits inside the bisect-batching
scheme the CORE already designed. The expensive part of this line was
never going to be the number of probes; it is the 1,150 kinds that take
no dominant input and so cannot be probed by this rule at all (§5), and
the hand-written tail for kinds buried three or more levels deep (§4).

---

## §2 — the counting rule, and the decisions inside it

The rule is stated first; its number was given in §1 and is tabled in
§3.

> **R1, the base rule.** One probe is one triple — a host kind, one
> declared slot of that host kind, and one of the six dominants —
> where `node-types.json` declares that a literal of that dominant may
> legally stand in that slot. A slot no dominant can fill contributes
> nothing. A host kind with no such slot contributes nothing and is
> counted separately as unprobeable.

> **R2, the operator extension, offered beside R1 and not folded into
> it.** A slot whose declared fillers are all anonymous tokens and
> number two or more is a token-choice slot: the grammar is saying this
> host holds one operator from a fixed menu. Under R2 a host's R1
> probes are multiplied by the size of its menu.

All claims in this log are at the GRAMMAR level — what
`node-types.json` declares — unless marked LANGUAGE level, which means
what the compiler or interpreter actually accepts. Phase 0 produced no
claim at the measured-behaviour level, because nothing was run.

The judgment calls, numbered, each one a decision the owner can overturn
without re-running anything but the third script.

1. **R1 is the unit.** Adopted as the task proposed. The alternative
   considered was counting one probe per (host, slot) pair regardless
   of how many dominants fit, which would give 739 probes rather than
   3,556; it was rejected because feeding a string where an integer was
   fed is exactly the measurement this line exists to take.
2. **R2 is offered, not adopted.** This is the one decision that moves
   the headline number: 3,556 under R1, 7,140 under R2. R2 has one
   visible flaw — it multiplies by menus that are not operator menus at
   all, such as c-sharp's `operator_declaration` (34 tokens) and cpp's
   `fold_expression` (38 tokens), which are declarations of operators
   rather than uses of them. If R2 is adopted, those two hosts want
   excluding by hand.
3. **The dominant-to-kind map is hand-written, one entry per language,
   and lives at the top of
   `PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/probe_space.py`.**
   It says which kind of each grammar IS a literal of each dominant —
   python's `dictionary` for dict, rust's `boolean_literal` for
   boolean. It names 74 kinds across the eleven languages, 70 of them
   distinct; every one was checked against its own grammar's kind list
   and none is missing. Three consequences are
   measured facts about the grammars, not gaps in the method:
   java, c-sharp, rust, cpp and kotlin declare **no dict literal**, so
   dict is unreachable in five of eleven languages; kotlin declares
   **no boolean literal at all** — its grammar has neither a named
   boolean kind nor `true`/`false` as tokens; cpp and typescript fuse
   integer and float into one kind (`number_literal`, `number`), which
   costs nothing here because R1 counts the dominant, not the kind.
4. **Dialects were chosen where a language ships more than one grammar
   file.** typescript reads `typescript__typescript.node-types.json`,
   not the `tsx` dialect. php reads `php__php.node-types.json`, the
   grammar that also handles the surrounding text, not
   `php__php_only.node-types.json`; the two differ by 2 named entries
   (162 against 160). csharp reads `c-sharp.node-types.json`.
5. **A slot is a key of the entry's `fields` map, plus one further slot
   for tree-sitter's `children` key**, which carries no role name and
   is written in our tables under the role label `*`.
6. **Multiplicity is ignored.** A slot that may hold many sub-nodes
   counts once, not once per possible count. Whether a list-valued slot
   deserves a second probe at length two is a phase-1 question.
7. **Depth is counted raw** — see §4 for what that costs.
8. **swift is carried as a bonus row and excluded from every total.**
   Its grammar file predates the `root` key, so its root was inferred
   as the one kind that has slots and never stands in another kind's
   slot; that came out `program`, uniquely.

### what reading only `node-types.json` costs

The task asked plainly what the uniform method loses against reading a
compiled grammar. It was measured rather than guessed, on the two
grammars that are pip-installable (`tree_sitter` 0.26.0 with
`tree_sitter_rust` 0.24.2 and `tree_sitter_python`, installed in the
sandbox only, not on the owner's machine):

- **The anonymous token INVENTORY costs nothing.** rust: 111 anonymous
  tokens in the grammar file, 111 in the compiled grammar, the same set
  exactly. python: 89 and 89, the same set exactly. The named sets
  agree too, apart from python's `as_pattern_target`, which the
  compiled wheel has and the repository file fetched 2026-08-12 does
  not — a one-kind version skew.
- **The anonymous token POSITION is what is lost.** A token is only
  attached to a host when it appears in some slot's type list. Across
  the eleven targets, 438 of the 1,422 anonymous tokens (30.8%) have a
  declared host; 984 (69.2%) exist in the file with nothing saying
  where they may go. rust is 29 positioned of 111; python 42 of 89;
  dart, worst, 21 of 132.

So the invisible thing is not which operators exist. It is which host
kind two-thirds of them attach to — and that is exactly what a probe
generator needs. Phase 1 will have to recover those positions by
another route, and the cheapest one is the refusal channel the CORE
already treats as a first-class result: emit the probe, let the
compiler refuse it, record the refusal.

---

## §3 — per language

Named kinds exclude the grammar's abstract groupings and its hidden
entries; anonymous tokens are the operators and keywords. "Legal
triples declared" is the table as the grammar spells it; "resolved" is
the same table with every abstract grouping expanded into the concrete
kinds it stands for. "Dominant-typed slots" is how many slots admit at
least one of the six dominants.

| language | named kinds | anonymous tokens | slots | legal triples declared | legal triples resolved | dominant-typed slots | probes R1 | probes R2 | unprobeable kinds |
|---|---|---|---|---|---|---|---|---|---|
| python | 122 | 89 | 165 | 352 | 2281 | 68 | 386 | 686 | 61 |
| typescript | 176 | 141 | 300 | 566 | 2830 | 70 | 336 | 810 | 120 |
| java | 142 | 114 | 230 | 410 | 2074 | 43 | 168 | 368 | 106 |
| csharp | 219 | 188 | 326 | 733 | 5309 | 87 | 392 | 642 | 140 |
| go | 107 | 76 | 153 | 232 | 1392 | 35 | 200 | 452 | 78 |
| rust | 163 | 111 | 262 | 547 | 3289 | 70 | 311 | 571 | 104 |
| ruby | 134 | 104 | 168 | 340 | 4672 | 86 | 445 | 859 | 65 |
| php | 157 | 143 | 241 | 724 | 3649 | 68 | 377 | 818 | 100 |
| kotlin | 114 | 124 | 112 | 273 | 1835 | 44 | 176 | 356 | 77 |
| cpp | 223 | 200 | 338 | 1081 | 4919 | 89 | 326 | 983 | 149 |
| dart | 219 | 132 | 227 | 3113 | 3986 | 79 | 439 | 595 | 150 |
| **11 targets** | **1776** | **1422** | **2522** | **8371** | **36236** | **739** | **3556** | **7140** | **1150** |
| swift (bonus) | 72 | 109 | 66 | 932 | 932 | 34 | 128 | 128 | 41 |

### the sanity check against the CORE's estimate

The CORE's words are:

> Reading legal pairs off the grammar replaces blind enumeration:
> hundreds of probes per language rather than 163^2 ~ 26,000.

**The real number is in that range, at its lower half.** Under R1 the
per-language count runs 168 (java) to 445 (ruby), mean 323 — hundreds,
as predicted. Under R2 it runs 356 to 983 — still hundreds, and still
nowhere near 26,000.

Rust, the language the CORE's estimate was written about, in three
steps:

| stage | rust triples | share of the blind number |
|---|---|---|
| blind enumeration, 163^2 | 26,569 | 100% |
| declared legal by the grammar, resolved | 3,289 | 12.4% |
| probes under R1 | 311 | 1.17% |
| probes under R2 | 571 | 2.15% |

One caution against reading the middle row as the pruning: 36,236
resolved legal triples across eleven languages is larger than eleven
blind n^2 counts would be for the smaller grammars, because one triple
is a host-and-slot-and-filler, not a host-and-filler. The number that
matters is the last row, and it is smaller than the CORE guessed.

---

## §4 — the depth structure

Depth is the smallest number of enclosing named kinds needed before the
kind is legal, counted from the grammar's root. Depth 1 means the probe
is a single top-level line. Depth 2 is the owner's `break` inside `for`
shape: one enclosing kind must be written first. Depth 3+ is the tail
the CORE anticipated having to hand-write.

| language | probe hosts depth 1 | depth 2 | depth 3+ | probes depth 1 | probes depth 2 | probes depth 3+ | kinds needing an enclosing kind |
|---|---|---|---|---|---|---|---|
| python | 37 | 15 | 9 | 242 | 100 | 44 | 59 |
| typescript | 9 | 26 | 20 | 64 | 163 | 105 | 117 |
| java | 7 | 17 | 12 | 36 | 83 | 49 | 111 |
| csharp | 1 | 51 | 25 | 7 | 257 | 124 | 191 |
| go | 10 | 14 | 5 | 66 | 109 | 25 | 77 |
| rust | 4 | 38 | 17 | 24 | 202 | 85 | 134 |
| ruby | 35 | 23 | 11 | 268 | 127 | 50 | 60 |
| php | 8 | 36 | 13 | 60 | 239 | 78 | 122 |
| kotlin | 25 | 8 | 4 | 124 | 36 | 16 | 66 |
| cpp | 17 | 37 | 20 | 74 | 161 | 91 | 164 |
| dart | 4 | 26 | 39 | 9 | 169 | 261 | 188 |
| **11 targets** | **157** | **291** | **175** | **974** | **1646** | **928** | **1289** |
| swift (bonus) | 20 | 10 | 1 | 86 | 38 | 4 | 35 |

Read across the totals: 974 probes are a single top-level line, 1,646
need exactly one enclosing kind, 928 need two or more, and 8 sit on
hosts the grammar never connects to its root (typescript's
`literal_type`, c-sharp's `preproc_line` and `preproc_pragma`). Of the
1,776 named kinds, 1,289 are legal only inside some other kind.

### the two distortions in this measurement, both stated rather than corrected

**First: container kinds count as a level.** java's `block` is a kind,
so anything written inside a method body reads one deeper than a person
would say. A draft of the third script contracted such wrappers away;
the rule could not be written without also swallowing
`break_statement`, whose only sub-node is an optional label, so the
contraction was removed and the raw count kept. The code carries the
same note at `containment_edges` in
`PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/probe_space.py`.

**Second, and it is the one that matters: the grammar's legality is
looser than the language's.** The contrast, with both sides quoted from
`PRIVATE/PseudoCoupHQ/Research/kind_signature_clustering/raw_all/python.node-types.json`.

The chain the grammar DOES state — `else` after `if`:

> ```json
> {"type": "if_statement", "named": true, "fields": {
>   "alternative": {"multiple": true, "required": false,
>     "types": [{"type": "elif_clause", "named": true},
>               {"type": "else_clause", "named": true}]},
> ```

`else_clause` is declared only inside the statements that can carry one
— `if_statement`, `for_statement`, `while_statement`, `try_statement` —
and never at the top level of a file, so it measures at depth 2 by the
shortest of those paths (`else_clause` inside `for_statement` inside
`module`). The grammar level and the language level agree that one
enclosing kind must be written first.

The chain the grammar does NOT state — `break` inside `for`:

> ```json
> {"type": "module", "named": true, "root": true, "fields": {},
>  "children": {"multiple": true, "required": false,
>   "types": [{"type": "_compound_statement", "named": true},
>             {"type": "_simple_statement", "named": true}]}}
> ```

and `_simple_statement` lists sixteen sub-kinds directly — 51 once
those expand in turn — with `break_statement` among them:

> `['assert_statement', 'break_statement', 'continue_statement',
> 'delete_statement', 'exec_statement', 'expression_statement',
> 'future_import_statement', 'global_statement',
> 'import_from_statement', 'import_statement', 'nonlocal_statement',
> 'pass_statement', 'print_statement', 'raise_statement',
> 'return_statement', 'type_alias_statement']`

So at the GRAMMAR level `break_statement` is a legal top-level line and
measures at depth 1. At the LANGUAGE level CPython refuses it outside a
loop. Seven of the eleven grammars do the same thing — python, java,
php, typescript, cpp, go and ruby all put their break at depth 1,
straight under the root. Three bury it only under scaffolding that has
nothing to do with loops: c-sharp at depth 2 through `global_statement`,
rust at 2 through `const_item`, dart at 3 through `function_body` then
`block`. The eleventh, kotlin, has no break kind at all — neither named
nor as a token — so its grammar cannot state the chain even in
principle. Not one of the eleven grammars says that break needs a loop.

The consequence for phase 1 is one sentence: the depth table above
tells you which probes need scaffolding because the grammar says so,
and it will under-report, so the rest has to come from refusals.

### the depth-3+ tail, in full

175 probe hosts across the eleven, holding 928 probes. This is longer
than the CORE's "short tail" and the reason is visible in the list:
most entries are argument, parameter and initializer wrappers, which
are three levels down in the tree but one line to write
(`f(1)` reaches java's `argument_list`). The genuinely hand-written
subset is smaller than 175, and picking it out is a phase-1 job.

- **python (9)**: complex_pattern, default_parameter, dict_pattern,
  format_expression, keyword_argument, keyword_pattern,
  typed_default_parameter, union_pattern, with_item
- **typescript (20)**: abstract_method_signature, arguments,
  assignment_pattern, computed_property_name, enum_assignment,
  export_specifier, extends_clause, import_specifier,
  method_definition, method_signature, object_assignment_pattern,
  optional_parameter, pair, pair_pattern, property_signature,
  public_field_definition, required_parameter, spread_element,
  switch_case, template_substitution
- **java (12)**: annotation_argument_list,
  annotation_type_element_declaration, argument_list, array_initializer,
  dimensions_expr, element_value_array_initializer, element_value_pair,
  explicit_constructor_invocation, guard, resource,
  string_interpolation, switch_label
- **csharp (25)**: argument, array_rank_specifier,
  arrow_expression_clause, attribute_argument, catch_filter_clause,
  constant_pattern, expression_element, from_clause, group_clause,
  interpolation, interpolation_alignment_clause, join_clause,
  let_clause, order_by_clause, parameter, relational_pattern,
  select_clause, spread_element, subpattern, switch_expression_arm,
  switch_section, variable_declarator, when_clause, where_clause,
  with_initializer
- **go (5)**: argument_list, field_declaration, literal_element,
  receive_statement, variadic_argument
- **rust (17)**: arguments, base_field_initializer, closure_parameters,
  const_parameter, enum_variant, field_initializer, field_pattern,
  let_chain, let_condition, match_arm, match_pattern, parameter,
  token_repetition, token_repetition_pattern, token_tree_pattern,
  type_arguments, variadic_parameter
- **ruby (11)**: block_body, destructured_left_assignment,
  exception_variable, exceptions, if_guard, keyword_parameter,
  keyword_pattern, optional_parameter, pattern, rest_assignment,
  unless_guard
- **php (13)**: argument, array_element_initializer, case_statement,
  enum_case, heredoc_body, match_condition_list,
  match_conditional_expression, match_default_expression,
  property_element, property_hook, property_promotion_parameter,
  simple_parameter, variadic_unpacking
- **kotlin (4)**: class_parameter, explicit_delegation, range_test,
  value_argument
- **cpp (20)**: abstract_array_declarator, annotation, argument_list,
  bitfield_clause, compound_requirement, constraint_conjunction,
  constraint_disjunction, field_initializer, gnu_asm_clobber_list,
  gnu_asm_input_operand, gnu_asm_output_operand, initializer_pair,
  lambda_capture_initializer, new_declarator, noexcept,
  optional_parameter_declaration, simple_requirement,
  subscript_argument_list, subscript_designator,
  subscript_range_designator
- **dart (39)**: argument, assertion_arguments, assignable_expression,
  assignment_expression_without_cascade, await_expression, cast_pattern,
  constant_pattern, declaration, expression_statement, field_initializer,
  for_element, for_loop_parts, function_expression_body, if_element,
  if_statement, index_selector, initialized_variable_definition,
  list_pattern, map_pattern, named_argument, null_assert_pattern,
  null_check_pattern, object_pattern, operator_signature,
  optional_formal_parameters, pair, pattern_variable_declaration,
  record_field, record_pattern, rest_pattern, spread_element,
  switch_expression_case, switch_statement_case, template_substitution,
  throw_expression_without_cascade, uri_test, yield_each_statement,
  yield_statement
- **swift (1, bonus)**: value_argument

Five entries in that tail are genuine chains rather than wrappers, and
they are the ones the CORE predicted by hand. Each is given as its
measured shortest super-chain, read right to left from the root:

| kind | measured depth | shortest super-chain |
|---|---|---|
| php `case_statement` | 3 | program, switch_statement, switch_block |
| java `switch_label` | 4 | program, switch_expression, switch_block, switch_block_statement_group |
| rust `match_arm` | 4 | source_file, const_item, match_expression, match_block |
| java `explicit_constructor_invocation` | 5 | program, class_declaration, class_body, constructor_declaration, constructor_body |
| dart `switch_statement_case` | 5 | program, function_body, block, switch_statement, switch_block |

The java row is the CORE's own `super(...)` example, which it estimated
at four; measured, it is five, because the grammar counts `class_body`
as a level of its own. The rust row shows the second distortion at
work: the shortest path to `match_arm` runs through `const_item`, which
is not how anyone would write the probe — a `match` inside a function
is the natural form, and it is one step longer.

---

## §5 — the kinds that cannot be probed by this rule

1,150 of the 1,776 named kinds — 64.8% — have no slot into which a
dominant literal may go, so R1 generates nothing for them. This is an
honest exclusion and the population splits into four causes, not 1,150
sightings.

| cause | what it is | examples |
|---|---|---|
| the kind IS a dominant, or part of one | it is the input, not a host | rust `boolean_literal`, ruby `character`, java `binary_integer_literal` |
| a control-flow or jump statement with no data slot | it takes no value at all, so nothing can be fed to it | python `break_statement`, python `continue_statement`, ruby `break`, go `break_statement` |
| a declaration or a type | it names things; a literal cannot stand in it | python `class_definition`, rust `abstract_type`, java `annotated_type`, cpp `access_specifier`, php `abstract_modifier` |
| lexical and layout kinds | comments, modifiers, container braces | python `comment`, go `comment`, ruby `block`, java `block`, cpp `attribute` |

Two of these four are not really losses. A kind in the first row is
already fully measured, because it is one of the six instruments the
`dominant_intentions` census verified on 2026-08-14. A kind in the
fourth row has no behaviour to measure.

The second row is the real loss, and it is the interesting one: python
`break_statement` cannot be probed by feeding it a value, because it
takes none. Its behaviour only shows in what a surrounding loop does.
Measuring it needs a probe whose reading is the ORDER of what got
printed, not the value returned — a different probe shape, and a phase-1
design question rather than a phase-0 count.

Per-language counts are the last column of §3; the full lists are in
`PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/probe_space.json`
under each language's `unprobeable_kinds`.

---

## §6 — what phase 1 needs from the owner

Phase 1 is probe design: the rules that turn a triple into a script.
Six things are blocked on a ruling, each stated with the fact it rests
on so it can be answered from this page.

1. **R1 or R2 — does the operator menu multiply?** R1 counts
   `binary_expression` once per dominant and gives 3,556 probes. R2
   counts it once per operator on the grammar's menu and gives 7,140.
   php's `binary_expression` menu has 30 tokens, python's has 13. Under
   R1 the anonymous vocabulary — 1,422 tokens, which the CORE names as
   half of what gets fuzzed — is never measured separately at all.
2. **The dict gap in five languages, and the boolean gap in kotlin.**
   java, c-sharp, rust, cpp and kotlin declare no dict literal, and
   kotlin declares no boolean literal. Reaching them needs a library
   call — `HashMap::new`, `mapOf` — and the CORE ruled builtins out of
   scope until the owner opens them. Options: leave the cell empty and record
   it as unmeasurable at the grammar level; or open a narrow exception
   for one constructor per missing dominant per language.
3. **The depth-3+ tail: written up front, or grown from refusals?**
   This was already an open question in the CORE. The measured tail is
   175 hosts and 928 probes, listed in §4 — longer than "short", but
   most of it is argument and parameter wrappers that cost one line
   each. A middle course exists: hand-write only the chain cases, which
   are a handful per language, and let the wrappers fall out of ordinary
   generation.
4. **Confirm python as the first language, now with a number behind
   it.** Python has 386 probes, of which 242 (63%) are depth 1 — the
   highest depth-1 share of the eleven. c-sharp, for contrast, has 7 of
   392 at depth 1. Python is the cheapest loop to prove end to end,
   which is what the CORE proposed on other grounds.
5. **How a probe reads a kind that takes no input.** §5's second row:
   `break_statement` and its co-kinds take no value, so an input/answer
   probe cannot see them. They need a probe read by execution order
   instead. That is a second probe shape, and whether phase 1 builds it
   or defers it is the owner's call.
6. **Whether the missing token positions are recovered by refusal.**
   984 of 1,422 anonymous tokens have no declared host slot. The CORE
   already treats a compile refusal as a first-class result; using it
   as the discovery channel for token position costs nothing extra in
   design but does raise the refusal rate, which changes what the
   bisect batching is tuned for.

---

## record

Scripts, all three in
`PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/`, each
runnable on its own:

- `bash -c "cd PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering && python3 extract_kinds.py"`
  — writes `kinds_<language>.json` for the eleven targets and swift.
- `bash -c "cd PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering && python3 legal_pairs.py"`
  — writes `legal_pairs_<language>.json`, the declared triples plus the
  expansion map for the grammar's abstract groupings.
- `bash -c "cd PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering && python3 probe_space.py"`
  — writes `probe_space.json`, every number in §3, §4 and §5.

Nothing was executed in any of the eleven languages, and no probe was
generated. The only thing installed was in the sandbox container, for
the one comparison in §2: `pip install tree_sitter tree_sitter_rust
tree_sitter_python`.
