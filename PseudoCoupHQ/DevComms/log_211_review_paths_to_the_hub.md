# log_211 — review: the research paths to the Hub, and what task o4's numbers are

This log belongs to the arch_unit_oracle line but reviews the whole
PCHQ research node. Written 2026-09-06 by the coordinator (Fable) at
the owner's request: "have a review of whatever you need and let me know
your expert thoughts", with the objective stated as "create dominant
operators and types for constructing the Hub." Numbers are as of
2026-09-06 with populations named; opinions are marked as such.

## 1. First, the surprise: why task o4 found thousands of variants

### 1.1 What was measured, and what the owner had in mind

- **Measured (task o4, log_210):** every operator site in the WHOLE
  source tree of each compiler. go's `cmd/compile` is 734 files:
  the parser, the type checker, escape analysis, SSA construction,
  every optimisation pass, register allocation, the object writer.
  103,475 sites of the twenty lowered operators.
- **the owner's picture:** the lowering route for one operator — the path
  the compiler walks from `a + b` in the source to the `add`
  instruction. That is the DIARY slice (compiler_graph line, task
  81 and after), and it is tens of functions, mostly `switch` on an
  opcode and string or enum comparison. The transpile-to-Python
  result was that slice, and its simplicity is real.
- These are different populations by three orders of magnitude,
  and I set the wrong one. The o4 number is not odd; it is the
  ordinary arithmetic of a 100,000-line program: loop indices,
  byte offsets, bit flags, size comparisons.

### 1.2 What the "variants" are made of

- A variant is (operator, written left type, written right type).
  The written types in a compiler's source are its OWN data
  structures: `*ir.Node`, `ssa.ID`, `int64`, `unsigned`, `SDValue`,
  plus literal kinds. Of go compiler's 1,050 resolved variants, 248
  have both operand types in go's scalar core; the other 802 are
  compiler-internal types. So most of the variety is the compiler's
  type vocabulary, not the operator's.
- The three largest resolved variants in go's compiler, literal
  from `operator_variants_by_search.json`: unary `-` on an integer
  literal (7,214 sites), `!=` on `int64` against an integer literal
  (433), `!` on `bool` (372). That is index and flag arithmetic.

### 1.3 The number that answers the owner's question, not yet cut

- Task 95 already names the emitter definitions: 57 in go, 251 in
  clang (the functions whose source produces machine instructions).
  Task 81's diaries name the functions visited per operator probe.
- Cutting o4's per-site records to those functions gives "variants
  used by the lowering route" — expected to be tens, in a handful of
  types. This is a filter over an existing json, one lane. Proposed
  as the first step in §6.

## 2. What the Hub is, in the terms that already exist

**The Hub is a dictionary: key = (operator intention, input types,
output type), value = one canonical arch-unit body; tree-sitter
supplies the nesting that turns a source tree into a sequence of
lookups joined through memory rows.**

- the owner's words for it today: "the dictionary key could be generated
  from high level operator, types (input, output) and return the
  arch-unit with everything being coordinated by the tree-sitter."
- Its two halves in the planning tree: the dictionary is the pool's
  deliverable ("the dominant-operator table feeding `ur_kind` and the
  Hub", pool CORE); the tree-walk-and-join is the hub_compiler
  sub-node of this line.
- What this replaces: PCv5 → PseudoIR → PCv6 was "transpile the
  compiler, slice its lowering, insert the slice." The function-
  wrapping probes made the lowering's OUTPUT available directly, so
  the slice is no longer needed for the value side of the
  dictionary. §5 says what the transpile path was still carrying.

## 3. What exists toward it, piece by piece

### 3.1 Dominant operators — the pool and the families

- `the_pool5.json`: 1,831 entries over 30,432 members; 490 entries
  span more than one language; 3 span compiled and interpreted.
  Merge grounds: identical wrapped text (27,439 merges), identical
  layer-5 term text among proved terms (25,327), banked proved edges
  (118).
- `the_families5.json`: 34 families over 197 nodes, the dom_op rule
  over entries. `exception_families5.json`: 40 families over
  guards.
- Integer addition is entry E00029: 158 members across c, cpp, go,
  rust, php, ruby, cpython, one term text `v0 + v1`, representative
  `go/op_319` at 35 bytes. That row is what a Hub entry looks like.

### 3.2 The per-language routing table — already data

- Each language's compiler has ALREADY told us where every
  (operator, operand types) goes: the probe corpus. c/op_113 is c's
  `+` on (int32, int64) and it is a member of one entry. So the map
  (language, token, input types) → entry is 30,432 rows of existing
  data, produced by the compilers themselves, with no hand table.
  This is the owner's "dictionary key generated from high level operator,
  types" — the key side exists per language, keyed by the probe's
  holder types.

### 3.3 Dominant types — two vocabularies, not yet one

- **Language side:** `type_inventory2_core2.json`, the scalar core
  read from each compiler's own type markings: c 56, cpp 56, go 14,
  rust 15, swift 17 spellings, each with a class
  (integer_signed / integer_unsigned / float / truth).
- **Machine side:** the pool's `type_key` = arrival register
  families | answer width, 88 distinct values (`rdi,rsi|32`,
  `rcx,xmm0,xmm1|32`, `xmm0,xmm1|8`, …). This is the machine-form
  stand-in for the operand-type key, per the spelling ban.
- Task 40 extracted a DWARF parameter table for every one of the
  29,288 regenerated units. That table carries, per unit, the
  language spelling AND the machine width and encoding of each
  parameter. It is the join between the two vocabularies, and it
  is on disk, unjoined.

### 3.4 Modes

- A mode is the same intention with a different guard: swift's `+`
  traps on overflow (`jo` / `ud2`, 123 sites of `ud2` in swift's
  units), c's wraps, rust's checks in debug. The pipeline keeps them
  as separate entries (correctly: they compute different functions
  on the overflow inputs) and the exception families group the
  guards. The DIFFERS-BY-DESIGN verdict and the DIRECTIONAL BRIDGE
  ruling (AgentMemory, 2026-08-26) are the recorded design for
  relating a mode to its unguarded core: "X dominates Y on
  projection P", carrying the adapter.

## 4. The gaps, by cause, each with a status

### 4.1 Equivalence in the pool is finer than intention — open

- The pool merges on IDENTICAL term text. Two units computing the
  same function whose normalized texts differ stay separate. The
  evidence that this matters: 527 entries carry more than one
  wrapped text, and the brief-strict count (text identity and proved
  edges only) is 5,095 against 1,831 merged — text identity is doing
  most of the merging, and what text identity cannot see is not
  merged at all. Task o1's length-one matrix (c builds only 46% of
  cpp's entries, from the SAME clang) is the same fact from the
  other side: many of those 54% are equal computations with
  different texts.
- A dominant operator is the union of entries proved equal by the
  solver, term against term, within a type_key bucket. That is the
  gate's existing solver call applied between entries instead of
  between a term and its own body. 88 buckets bound the pair count.
- Status: open. Not started. It is the step that turns the pool
  into "dominant operators".

### 4.2 The type join is not built — open, data on disk

- §3.3: language spellings on one side, register-family|width on
  the other, DWARF tables in the middle. Building the join gives,
  per language, spelling → (class, width) → type_key, and its
  inverse gives, per pool entry, which language types it serves.
  That table IS "dominant types" at the scalar level: one row per
  (class, width) the machine distinguishes, with each language's
  spellings hanging off it.
- Status: open. One task, no new measurement.

### 4.3 The key needs input types at every tree node — open, the owner's

- Task o4 measured how far search alone gets at typing operator
  sites: fully resolved 17% (clang), 22% (go compiler), 20% (go
  stdlib), 6% (rustc), 11% (swiftc), 9% (swift stdlib). The
  remainder is call results, member access, inferred bindings, and
  declarations in other files.
- The Hub's tree-sitter front end has exactly this problem on the
  programs it lowers: a tree-sitter tree carries no types. So the
  dictionary's key cannot be built from tree-sitter alone on real
  code. Three routes:
    - **the language's own front end as a type oracle**: run
      `clang -ast-dump=json`, `go/types`, rustc's typed dump on the
      input file once, read the type at each operator node. Not
      transpiling; a dump. My recommendation.
    - **restrict Hub v1 to explicitly typed code** (or to code the
      Hub itself generated): search suffices; o4's resolver is that
      search.
    - **a type inference in the Hub per language**: the largest
      build, and it re-creates the compiler's front end.
- Status: the owner's to choose. Everything in §6 after step 4 waits on it.

### 4.4 Scope is scalar expressions only — open, largest

- Layer 1 of data_representation names nine forms: nothing, truth,
  whole, fractional, text, sequence, keyed grouping, nesting,
  identity marks. The arch-unit corpus covers whole, fractional and
  truth. Text, sequence, keyed, nesting and identity have NO
  arch-units: the probe generator excluded the structural buckets
  (indexing, member access, calls) by design, and task o3 shows
  those are exactly the "used, not lowered" operators in every
  compiler (`.`, `->`, `[]`, `:=`, `new`).
- A real program is mostly those. The Hub over scalars lowers
  arithmetic; the Hub over programs needs aggregate holders, and the
  unit boundary rule (function body) already admits them — a probe
  whose parameter is a slice or a struct is still a function body.
- Status: open, not started; the seed order in dominant_intentions
  (boolean, float, integer, string, list, dict) is the plan for it.

### 4.5 Coverage across the twelve — open

- Corpora exist for c, cpp, go, rust, swift. java, cpython, php,
  ruby have 11 hand-carved handler units between them (tasks 94,
  96), all `+` and one `/`. kotlin, dart, c#, typescript have
  grammar inventories only. The interpreter route (interp_feeder,
  remaining_languages nodes) is the plan; the seventh block kind
  ruling (an arriving addressable area) is what it was waiting on.
- Status: open; blocked on nothing but work.

### 4.6 The mode axis in the key — the owner's

- Whether the key carries a mode (wrap / trap / checked) or the Hub
  picks the target language's mode by policy. The exception
  families and the bridge ruling hold the data either way.

## 5. On vectorized lowering side-stepping transpile-slice-insert

Opinion, stated as such.

- **Agree on the value side.** Every operator node is an
  independent lookup; every tree edge is a memory row; the join is
  the canonical form's own prelude and epilogue. There is no
  dependence between lookups, so lowering a tree is a map over its
  operator nodes. That is a vector operation. The composed body is
  in canonical form, so the gate can prove it against the language
  compiler's output for the same file — the hub_compiler oracle —
  and a disagreement locates to one entry or one join.
- **The transpile path was carrying two things**, and arch-units
  replace only one. It carried the lowering ROUTE (replaced: the
  route's output is the arch-unit) and the compiler's TYPE CHECKER
  (not replaced: §4.3). So "side-step the transpile" reduces to
  "the compiler's front end runs once as a type oracle", which is a
  dump, not a slice, and needs no transpilation.
- **Cost of the vector form**, stated once: every value crosses
  between entries through memory, so the emitted code is slower
  than the compiler's. Correctness and provability are the
  objective; speed is not.

## 6. Order I would take — a proposal, not a decision

1. **Cut o4 to the lowering route** (emitter definitions from task
   95, diary functions from task 81): the variant count the owner
   expected, and the answer to §1 in numbers. One lane over an
   existing json.
2. **Dominant operators**: solver equivalence between entries within
   each type_key bucket; families rebuilt over the merged entries.
   Output: the dominant-operator table, with each entry's members
   and the counterexample for each refused merge.
3. **Dominant types**: the DWARF join, §4.2. Output: the (class,
   width) table with every language's spellings.
4. **Hub v1 dictionary**: (language, token, input types) → dominant
   operator → representative body, built from the corpus; report
   coverage per language over operator × core types, and the holes.
5. **hub_compiler on one explicitly typed go file**: lower by lookup
   and join, gate against go's own output. One PROVED or one located
   counterexample. Needs the owner's §4.3 choice only if the file is not
   explicitly typed.
6. Aggregate forms (§4.4), then the remaining languages (§4.5).

Steps 1–4 need no ruling and read only existing artifacts.

## 7. Awaiting the owner

- §4.3: the typing route for the Hub's front end.
- §4.6: whether the key carries a mode axis.
- Whether to proceed with steps 1–4 in that order.
