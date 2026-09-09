# log 072 — the compiler graph: tracing the transformer itself

2026-08-24, at the owner's request, recording an understanding reached in
conversation before the machinery is built. Per protocol §18a: the
chat carried the conclusions; this is the working record. The
operand-identity question (which register holds parameter `a`) was
the driving example throughout; the captures behind it are
`Airlock/agent/out/ce_trace_walk.txt` and
`ce_trace_all.txt`, and the interactive walkthrough is
`PseudoCoupHQ/Research/kind_fuzz_clustering/operand_walk.html`.

## 1. the correction that produced this log

- Three prior attempts answered the wrong question, each one level
  closer:
  - showing the compiler's PRODUCTS (MIR, LLVM IR, asm, DWARF) —
    testimony about outputs, not the machinery;
  - quoting the compiler's SOURCE by hand (four nodes:
    `args_iter().enumerate()` in rustc_codegen_ssa,
    `AnalyzeFormalArguments`'s ascending loop,
    `CCAssignToReg<[EDI, ESI, ...]>` in X86CallingConv.td,
    `AllocateReg`'s first-free rule) — correct nodes, but composed
    by human reading. A TRACE: proof by citation, interpretation
    still in the loop.
- the owner's requirement, now understood: **the actual graph as data,
  and the proof as a mechanical path query over it.** Nodes are
  declarations/references in the compiler's own source; edges are
  resolution and dataflow; "high-level variable connects to
  low-level variable" is answered by edge-following, or the query
  names the exact node where the path dies. No interpretation
  anywhere in the loop.
- Vocabulary settled in passing: **trace** (weak form — machinery
  stays in place, walked and cited) vs **slice** (strong form —
  logic extracted into the hub as usable parts). The trace proves a
  fact; the slice makes it infrastructure.

## 2. the "defined in" / "does" distinction (the owner's, load-bearing)

- The graph is over what the compiler is WRITTEN IN, never over
  what it DOES. A lowering function whose subject is arch opcodes
  may itself be ordinary Go — it sits in the Go-parseable region.
  The tree-sitter horizon is set by the implementation language of
  each file, not by the abstraction level of its content.
- Components defined AT the assembly/machine level are MORE
  automatically traceable, not less: closed vocabulary, one
  operation per line, explicit operands, no scope machinery. The
  hard resolution problems (interfaces, dispatch, closures) live in
  the high-level region.

## 3. implementation languages of the 13 compilers/runtimes

Measured from `Sources` where vendored (file-extension
census, 2026-08-24); marked unverified otherwise.

| compiler/runtime — written in |
| --- |
| go (gc): Go — 734 `.go` vs 2 `.s` and 27 `.rules` in cmd/compile. Self-hosted almost totally. MEASURED |
| rustc: Rust front/middle, hand-off to LLVM (C++). MEASURED (vendored crates pure .rs) |
| clang (c/cpp): C++ — 449 `.cpp` + 65 `.td` data files in llvm/lib. MEASURED |
| swiftc: C++ core, some Swift; lowers into LLVM. unverified |
| java/kotlin (HotSpot): C++ — 3,801 hpp/cpp + 25 `.ad` data + 19 `.S`. javac is Java, kotlinc is Kotlin (bytecode front ends). MEASURED |
| c# (.NET coreclr): C# 2,026 + C++ 1,403 + 190 `.S`. A genuine split. MEASURED |
| dart (VM): C++ — 438 `.cc` in runtime/vm. MEASURED |
| python (CPython): C. unverified |
| ruby (CRuby): C. unverified |
| php (Zend): C. unverified |
| typescript (tsc): TypeScript, self-hosted, type-erasure only; executor is V8 (C++). unverified |

Consequence: the connective tissue of all 13 languages is written
in ~5 languages (C++, C, Go, Rust, C#) plus self-hosted front ends
— all with tree-sitter grammars — and the layer beneath them is
machine code, which the arch campaign already lifts.

## 4. the mixed-grammar graph: five frontier kinds

One graph, several grammars. Where the implementation language's
tree-sitter cannot follow, the region is a FRONTIER, recorded by
kind, never guessed across:

- **assembly source** (`.s`/`.S`) — parse directly; grammar is a
  page; a register write followed by a read IS the edge. Cheapest
  region in the system.
- **compiled machine code** — the pyvex lift already produces
  explicit read/write statements = edges (1,652 arch-units of
  precedent).
- **data tables** (`.rules`, `.td`, `.ad`) — not code; each node is
  a PAIR: the table (parsed as data) + its consuming loop (already
  in the tree-sitter region). The edge runs through the pair.
  Precedents: CCAssignToReg + AllocateReg; our own stencils +
  mapper.
- **generated code** — trace the generator, or take the checked-in
  artifact as source; either way it re-enters a parseable region.
- **indirect calls** (function pointers, interface dispatch) —
  REFINED 2026-08-24 after the owner's challenge ("in what sense not
  traceable?"): statics nearly always names the CANDIDATE SET —
  every function value stored where the pointer could have come
  from is itself in the program, so the edge is one-to-many, still
  built by edge-following. What statics cannot name is the
  SINGLETON — which member runs — whenever the selector crosses an
  input boundary (a config string, file contents, user input).
  Worked example: `f := handlers[name]; f(v)` over a two-entry map
  gives the set {double, square} statically; the pick depends on
  `name`'s runtime value. The edge therefore carries the set,
  marked one-to-many, with the selector's origin recorded; it
  degrades to a TRUE frontier node only when the set itself is
  uncomputable (plugin loading, foreign pointers, address
  arithmetic). The probe layer closes singletons where needed.
  This keeps "exceptionally tractable" honest: tractable, not
  total — and the graph says where, and how wide.

## 4a. tree-sitter coverage below the high-level languages

Grammars exist for the lower layers too (ALL UNVERIFIED as of this
log — verify and pin at build time, same discipline as the language
grammars):

- assembly: tree-sitter-asm (GAS/objdump-style syntax)
- LLVM IR: tree-sitter-llvm (`.ll`)
- TableGen: tree-sitter-tablegen (`.td` — LLVM's
  machinery-as-data layer has its own grammar)
- WebAssembly text: tree-sitter-wast/wat

Consequence: the mixed-grammar graph can be tree-sitter END TO END
— one parsing technology, one node/edge shape, per-region grammars
— with one exception (raw machine bytes with no source, where the
pyvex lift substitutes) and one small custom reader (gc's `.rules`
files, a private line-oriented rewrite-rule format, closer to a
table than a language).

## 5. evidence classes (recorded in AgentMemory the same day)

forced-by-construction > the tool's own testimony > human
interpretation of stated design. The graph path query is the
forced class applied to the transformer's source; DWARF and dump
formats are testimony (three live testimony failures captured in
ce_trace_all.txt: Go's SSA dump unanswered, Go's DWARF matching
runtime functions, Swift's DWARF contradicting its own assembly);
the calling-convention document alone is interpretation.

## 5a. the static-runtime join (the owner, 2026-08-24) — the ledger closes
the singletons

The v0 pattern (survey part 2.7: runtime observation joins the
static side on id equality) applied to the compiler itself:

- static layer: tree-sitter over the compiler's source; the ledger
  holds the graph; indirect edges carry candidate sets (§4).
- runtime layer: run that compiler on OUR probe file (the
  operator-wrapped-in-a-function script) and observe which nodes
  execute; each one-to-many edge that ran collapses to the member
  that ran, written as a runtime connector against the static
  node's id.
- the input-boundary objection dissolves BECAUSE WE AUTHOR THE
  INPUT: "data that doesn't exist until runtime" is unknown only
  when the input is unknown; ours is chosen.
- instrument for Go: the compiler built with Go's own coverage
  machinery emits per-block execution counts keyed to file:line —
  joins to tree-sitter spans mechanically. rustc equivalent: LLVM
  source-based coverage. (both unverified in the container as of
  this log.)
- evidence-class note: an observed path is fact FOR THE OBSERVED
  RUN — singletons proven per input; the static sets bound all
  inputs; every claim states which of the two it is.

## 6. first build (agreed)

Go first — self-hosted, so one grammar covers essentially the whole
transformer, no codebase hand-off:

- parse the argument-lowering region of
  `Sources/golang_src/src/cmd/compile` with
  tree-sitter-go (pin to be recorded at build time);
- emit the def-use graph AS A FILE: nodes = declarations and
  references (file, span, kind), edges = resolves-to and
  flows-into, frontier nodes by kind;
- run "parameter `a` → register" as a path query; the answer is a
  path or a named dead-end node;
- judges: the forced probe (a−b vs b−a, already run for all four
  AOT languages) and DWARF where recoverable.
- scope honesty: full Go name resolution (interfaces, methods) is
  not needed for lap one; def-use within the bounded lowering
  region, growing outward, every unresolved reference a frontier
  node rather than a guess.

## 7. lap one result (2026-08-24, built and run same day)

- static layer: 86 files of cmd/compile parsed (tree-sitter-go
  0.25.0, tree 9f1012d9, 1.28-dev), 182,935 nodes, 234,312 edges,
  0 parse errors. `Research/compiler_graph/{build_graph,query_path}.py`,
  graph as data in `graph_go.json`.
- runtime layer: the tree's own toolchain built via make.bash into
  Airlock `/persist/gosrc`; cmd/compile rebuilt with
  `-covermode=count -coverpkg=cmd/compile/...`; probe
  `af(a,b)=a-b` compiled by replaying the exact tool command line
  with the instrumented binary. 141,731 blocks total, 8,284
  visited, 3,492 in {ssagen, ssa, abi, amd64}. `coverage_go.txt`.
- the join: 8-hop static path (params loop -> assignParam ->
  tryAllocRegs -> allocateRegs, all in abi/abiutils.go) — EVERY
  hop executed during the probe compile (loop x18, chain x10).
  join granularity lesson: coverage counts STATEMENTS, so a
  function's opening line (the `func ...` header) never appears
  in coverage; a function node's count is read from its first
  body line. First join printed MISSED for the three method
  declaration hops for exactly this reason; corrected.
- the named frontier where lap one stops: from allocateRegs into
  amd64 emission, NO PATH — bounded by field-selector references
  (`state.rUsed`, `t.Size()`) that need the second resolution
  step: knowing WHICH declaration a variable is an instance of,
  then landing the edge on the slot inside it. Measured cost:
  20,216 unresolved selectors, led by `.Type` (1,234), `.Op`
  (1,159), `.Args` (1,124). Lap two = follow the dot.
- visualization: `Research/compiler_graph/graph_walk.html` — the
  90-node subgraph around the path, runtime counts overlaid,
  frontier nodes marked.
- RULED IN (the owner, this session): the machinery is language-
  agnostic — dispatch on file extension to the matching grammar,
  one multi-language graph. And the probe side automates from
  `operator_arity.json`: arity -> wrapper shape -> instrumented
  compile -> visited nodes. No hand-written probe per operator.
