# 01 — Vocabulary

Settled terms, the owner's §4 format. Check this file before reusing a
term. Add entries when a new term is introduced; never introduce a
term without one.

```
hub
    the disciplined-Python center. Applications are written once in
    it; the 12 target languages render from it. It dominates
    intentions.
    example tied to context:
        demo.pc executing `a r./ b` with Rust's truncating division
        semantics inside stock CPython — the hub computing a target
        language's exact semantics.

target language
    one of the 12 languages the hub renders to.
    example tied to context:
        Dart in the WFL work; Rust in the intermediate goal.
    note: earlier drafts used "target" for this AND for instruction
    sets; "egress language" was proposed and REJECTED (egress is a
    direction, not a category).

architecture
    an instruction set (x86-64, aarch64).
    example tied to context:
        an earlier generated-vocabulary artifact (since removed as
        mis-aimed) was an x86-64 oracle; LLVM x86-64 is established
        first because that is where byte-level disagreement is
        detectable.

ingress / egress
    directions, always relative to a stated perspective; never
    category names. source/target are roles, also relative.
    example tied to context:
        transpiling Rust compiler code into Python is an egress
        from Rust (source) and an ingress to the hub (target).

slice
    logic extracted from a compiler and executed in the hub.
    example tied to context:
        slice_mir_routing.py — rustc's operator routing to a
        backend intermediate op (a retired reference backend's;
        since removed as mis-aimed), transpiled and running inside
        CPython.

stub
    code deliberately excluded, carrying an asserted reachability
    invariant so it fails loudly at its site instead of emitting
    wrong output.
    example tied to context:
        the VEX/EVEX SIMD arms in an earlier generated-vocabulary
        artifact (since removed as mis-aimed): 618 differential
        pairs behind a stub that raises if reached.

ledger
    the per-program record: what type/shape/identity/divergence does
    THIS identifier have in THIS program. Populated at ingress
    (tree-sitter ingestors) and by defined overlays; read to drive
    emission and to verify.
    example tied to context:
        PseudoCoup/pseudocoup/core/ledger.py's method_returns
        answering "what does ProgramDao.getEnrolled return" so the
        Dart emitter can decide await.

registry
    class-level, program-independent steering data keyed
    (construct, target language): the confirmed lowering, its
    strategy, and its evidence. NOT a ledger.
    example tied to context:
        PseudoIR/pseudoir/registry/data/ops.json — null-coalescing
        per language, runtime-confirmed, with falsy-trap vectors
        that rejected `a or b`.

intention
    what the developer meant by choosing a construct — including
    complexity class. The choice of data structure IS a choice of
    complexity class.
    example tied to context:
        `d[key]` means associate-with-fast-retrieval; rendering it
        as a list of pairs returns the same values and is no longer
        the program that was written.

dominance
    the hub-canon property of covering every language's intentions
    so each maps in with no semantic distance. Selection tool:
    which semantics does the hub object get.
    example tied to context:
        Rust satisfies intention rows A/C/D/G (suspension,
        optionals, pattern matching, scoped cleanup) — the most
        dominant intentions; hence Rust first.

primitiveness
    ordering tool: where egress work bottoms out — which basis
    members cannot be constructed from the others. Answers a
    different question than dominance; they never competed.
    example tied to context:
        bool/int64/list/record are basis members because no
        combination of the others constructs them.

polyfill
    a wrapper filling target-behavior gaps so transpiled code
    matches source behavior exactly. Law: uniform, no exemptions.
    example tied to context:
        u8()/u32() fixed-width wrappers in the transpiled support
        layer of a retired reference backend; the one hand-rolled
        exemption (custom.rs nops) produced the one silent
        wrong-bytes bug.

oracle
    an independent ground truth used to catch disagreement.
    example tied to context:
        an earlier generated-vocabulary artifact (a retired
        reference backend's rustc-verified x86-64 encoders, since
        removed as mis-aimed) checking every LLVM-derived encoder
        byte for byte; native rustc grids; the v0 JVM-cross-checked
        behavior oracle.

PCvX
    the most advanced version-state of the one PseudoCoup
    transpiler lineage; X is a variable over versions, not a name
    for any specific old artifact. PCvX may be the current version.
    example tied to context:
        the 2026-07-27 survey found PCvX distributed: v0 holds
        behavioral verification, WFL the deepest emitter, PCv5 the
        compiler-source ingress.

tree-sitter
    the parsing foundation for every language in the project; the
    module producing the ASTs that connect the 12 languages and
    feed the ledger.
    example tied to context:
        idgen's node ids are positional paths over the tree-sitter
        tree; the WFL coverage gate partitions tree-sitter node
        kinds into handled/dropped/unvisited and drives the residue
        to zero.

MIR
    rustc's Mid-level Intermediate Representation (their term):
    the simplified internal form a Rust program becomes after
    parsing and type-checking — functions are flat sequences of
    primitive statements, sugar gone, control flow explicit.
    example tied to context:
        `codegen_int_binop` takes a MIR integer operation (like
        Div) and emits the backend's instruction for it — the
        seam PCv5 sliced.

seam
    the entry point in a source compiler where one pipeline stage
    meets the next — the function a slice starts at. Declared by a
    human, once per (language, intention); everything downstream
    of a declared seam is mechanically derivable (the automation
    boundary, R5 finding, pending the owner's ruling).
    example tied to context:
        `codegen_int_binop` in rustc's num.rs is the seam where
        MIR meets the backend's intermediate form; PCv5's
        slice_mir_routing.py starts there.

stand-in
    a transpiling-wrapper at a slice boundary: the hub object
    substituted where a call target was deliberately NOT followed.
    Every stand-in is a human-ruled wrapper point — pre-declared
    in the slicing request form (known compiler infrastructure) or
    created at a depth-truncation warning. Callees resolvable in
    the vendored compiler source are FOLLOWED (transpiled+sliced),
    not wrapped (the owner's follow-the-calls rule).
    example tied to context:
        the Ledger stands in for rustc's TyCtxt (answers "what
        type is this operand"); following TyCtxt instead would
        drag in half of rustc — the pre-declared wrapper case.

Frankenstein
    the owner's term (2026-07-31) for a tool built by composing the
    best-in-class parts already scattered across the PseudoCoup
    lineage, rather than written fresh or ported wholesale. The
    harvest maps in 03_lineage_and_harvest.md are the parts list.
    Two are named: the Frankenstein transpiler and the Frankenstein
    ledgerer.
    example tied to context:
        the combined ledger described in 03 — v0's idgen positional-
        path ids as the primary key, v0's ledger_unified record shape,
        the 289-line ledger's semantic registries re-keyed onto those
        ids — is a Frankenstein ledgerer described but not yet built.

PCv5-archived-research
    the owner's annotation (2026-07-31) marking a reference to something
    that lived in PseudoCoup_v5 BEFORE the gutting. It says: this
    exists in version control, not in the current tree. The
    annotation is why references to old PCv5 material do not all have
    to be deleted when PCv5 is rebuilt — annotate rather than remove.
    example tied to context:
        03_lineage_and_harvest.md's line "PCv5 | compiler-source
        ingress (Rust+C++ to Python), polyfill law, oracle-checked
        bytes" describes the pre-gutting repo, and once the rebuild
        happens that row is PCv5-archived-research, not a description
        of what is on disk.
```
