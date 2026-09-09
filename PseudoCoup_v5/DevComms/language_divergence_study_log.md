# Language Divergence Study — Log

A running log. Central query: if languages are stylized into one unified surface style
(Python-style, PseudoCoup discipline enforced), the *explicit* uniquenesses are easily
wrappable. What are the *implicit* uniquenesses — the ones that produce different outputs
(or different intermediate results, which could theoretically produce different outputs)
from identically-styled code? Classify them.

---

## Entry 2026-07-22 — Terminology and the paradigm-form

### Terminology

- **script**: the code that is input for the compiler to compile.
- **compiler**: unchanged.
- **layers**: the objects code exists as: `[script]`, `[IR opcodes]`, `[arch opcodes]`, `VM`, `CPU`.
- **phases**: dev-time; compile-time; run-time. Run-time sub-phases: interp-time, jit-time, arch-time. Phases are wall-clock; compile-time is a stage that paradigms may park before run-time or inside it.
- Rejected: `IR-time` (IR is an object, not a phase; compile-time is when IR is made).

### The paradigm-form

```
assumption: PseudoCoup discipline enforced on [script]

layers:
	[script]         high level code
	[IR opcodes]     virtual instruction set
	[arch opcodes]   machine instruction set
	VM               software executor of [IR opcodes]
	CPU              hardware executor of [arch opcodes]

phases:
	dev-time:        [script]
	compile-time:    [script] --> [IR opcodes]
	run-time:
		interp-time:     [IR opcodes] --> VM
		jit-time:        [IR opcodes] --> [arch opcodes]
		arch-time:       [arch opcodes] --> CPU
```

Paradigms are phase-placement rules over this one form:

| Paradigm | Placement rule |
|---|---|
| Java | compile-time before run-time; all run-time sub-phases present |
| CPython | compile-time inside run-time; jit-time deleted (pre-3.13) |
| V8 / PyPy | compile-time inside run-time; all sub-phases present |
| C-type | VM row deleted; compile-time goes straight to `[arch opcodes]`; run-time is only arch-time |

### Commentary conventions

Reference objects per-aspect: ask *which aspect survives into which phase, hosted by which layer*. Example:

- `var_a.name` dies at compile-time (resolved to a slot); exists only in `[script]`.
- `var_a.storage` is paradigm-dependent: a VM-managed frame slot (VM rows) or a stack offset (C-type). VM-dependence at run-time follows from which one.

Pointers as the extreme case: `pointer.type` dies at compile-time (governs stride and byte interpretation); `pointer.storage` IS the meaning — an index into a flat byte array — so wrapping the pointer object without providing the array it indexes wraps the key without the dictionary it looks into.

---

## Entry 2026-07-22 — The central query: explicit vs implicit uniqueness

```
explicit uniqueness
    a difference visible in the surface form
    of the language. unified styling +
    wrapping handles it.
    example tied to context:
        C++ `uint64_t` vs Dart `int` —
        the Ledger sees the declared type,
        PseudoUint64 wraps it.
        (compiler_transpilation_experiment.md)

implicit uniqueness
    a difference in what identical-looking
    code MEANS. no surface signal. produces
    divergent outputs, or divergent
    intermediate results, from code that
    styles identically.
    example tied to context:
        `-7 // 2` is -4 in Python (floor)
        and -3 in C/Java/Go (truncation).
        same expression, same style,
        different value. nothing in the
        script warns.
```

### Initial classification of implicit uniquenesses

Each class lists what diverges, a minimal divergent expression, and its disposition under Map / Wrap / Fail.

**1. value-model** — the arithmetic of primitive values.

- Division/modulo sign convention: `-7 // 2` → −4 (Python floor) vs −3 (C/Java/Go truncation).
- Integer overflow policy: `INT_MAX + 1` → wrap (C unsigned) / trap / arbitrary precision (Python).
- Shift semantics: `x >> n` → arithmetic vs logical (established: RyuJIT experiment).
- Width and signedness (established: PseudoUint64).
- Float edges: NaN payloads, x87/FMA intermediate precision.
- Disposition: **Wrap** — bit-exact simulators at Ledger-declared width/policy. Best understood class; partially proven.

**2. copy-model** — whether `a = b` and argument passing alias or copy.

- Minimal case: `a = b; b.x = 1; print(a.x)` → 0 in C++ (value struct), 1 in Python/Java/Dart (reference).
- Disposition: **Wrap or Forbid** — discipline could mandate reference semantics plus explicit `.copy()` at borders (the Python rule: rebinding is frame-local, mutation is global, no exceptions). Candidate for a discipline rule rather than a polyfill.

**3. evaluation-order** — the order sub-expressions execute.

- Minimal case: `f(g(), h())` → g/h order unspecified in C++ (pre-17), left-to-right in Python/Java. Observable only when sub-expressions have side effects.
- Disposition: **Forbid** (no side effects in argument position) or **Map** (emit explicit temporaries fixing the order). Cheap to fix at egress.

**4. lifetime / observation** — WHEN cleanup side effects run.

- C++ RAII destructor: deterministic, at scope exit. GC finalizer: nondeterministic, maybe never. Observable when destructors/finalizers have effects (files, locks).
- Disposition: **Wrap** (explicit try/finally-style scopes at egress) or **Forbid** (no effectful destructors). Unexplored.

**5. dispatch** — which function a call site selects.

- Overload resolution (static, by declared type) vs single dynamic dispatch; method resolution order in multiple inheritance.
- Disposition: discipline likely already forbids the divergent forms (Concrete Constructs) — verify. Unexplored; suspected forbidden-by-discipline.

**6. collection-order** — iteration order of unordered containers.

- Hashmap iteration: Python dict insertion-ordered; Go map deliberately randomized; C++ `unordered_map` unspecified. Observable whenever iteration order reaches output.
- Disposition: **Wrap** (canonical ordered container in the semantic registry) or **Forbid** (no iteration over unordered containers). Unexplored; silent-divergence risk high.

**7. concurrency / memory-ordering** — visibility order of writes between threads.

- Established in the transpilation experiment: shared-memory vs isolate models, atomics ordering.
- Disposition: **Wrap** at high cost, or **Fail**. Hardest class.

**8. encoding** — the unit of string indexing/length.

- `s[i]` → byte (C) / UTF-16 code unit (Dart, Java) / code point (Python).
- Disposition: **Wrap** (byte-array strings in the semantic registry). Established in the transpilation experiment.

### Observations

The classes sort by where the divergence hides:

| Hiding place | Classes |
|---|---|
| in the values (what a primitive operation returns) | 1, 8 |
| in the object graph (what aliases what, when it dies) | 2, 4 |
| in the sequencing (what order things happen) | 3, 6, 7 |
| in the selection (which code runs at all) | 5 |

```
machine-model dependence
    the language defines a construct by
    promising a machine abstraction —
    flat byte-addressed memory, shared
    address space, fixed-width registers.
    the semantics are "whatever that
    machine does." note: this is still a
    property of the LANGUAGE, not the
    machine; the machine does not care
    what language instructs it. the
    language delegates meaning to a
    machine abstraction.
    example tied to context:
        C++ pointer arithmetic — `p + 4`
        means what flat memory makes it
        mean. no convention to consult.

language-model dependence
    the language legislates meaning
    directly, by convention, with no
    machine referent.
    example tied to context:
        `-7 // 2`: floor vs truncation is
        somebody's choice. no machine
        settles it.
```

Conjecture to test: every implicit uniqueness is **machine-model dependence** (classes 1, 7, 8 — the established pattern from the transpilation experiment) or **language-model dependence** (classes 2, 3, 4, 5, 6 — divergent choices languages made above the machine). Machine-model classes Wrap by simulating the machine slice; language-model classes look more amenable to Forbid — discipline rules that pick one convention — since they are conventions, not hardware facts.

### Open questions

- Which classes does the current Universal Discipline already forbid, and which leak through?
- Minimal divergent script per class: a test suite where each file styles identically across all 12 targets but outputs differently when naively transpiled. The class is proven implicit exactly when this file exists.
- Are there classes not yet listed? Candidates to investigate: exception semantics (what is catchable), recursion limits, integer hashing, default float formatting in print.

---

## Entry 2026-07-22 (later) — Protocol consolidation and formatting pass

- The communication protocol was consolidated: canonical now at [LLM_communication_protocol.md](file://DevComms/LLM_communication_protocol.md); live-project copies are symlinks; archive copies frozen.
- This log was reformatted to comply with the merged protocol's ban on whitespace-aligned tables in code blocks: tabular data now uses pipe tables or lists. The paradigm-form block is retained as-is — it is a definition form (tab-structured, short lines, per the Text diagrams conditions), not a data table.

---

## Entry 2026-07-22 (later still) — Self-hosted polyfills

Proposal: instead of hand-writing each simulator per target, write each simulator **once, in disciplined Python**, and transpile it through the PseudoCoup pipeline like any other script. The semantic registry becomes self-hosting.

- Candidates: `PseudoUint64` (and the width family), `PseudoMemory` (flat byte array + pointer arithmetic), `PseudoBytes` (encoding). Each is pure computation, expressible inside the discipline.
- Precedent: Emscripten does not hand-port libc to JavaScript; it compiles the machine model through the same pipeline as user code.
- Coverage: fully solves the machine-model Wrap classes whose meaning is a computation — value-model (1), encoding (8), and the memory slice of pointers. Language-model classes (2–6) are unaffected; they are solved by Forbid (discipline rules), not simulation.
- The boundary: a simulator can be transpiled only if its own source stays inside the discipline. Two residues fall outside:
	- Class 7 residue: "two executors racing on one buffer" is not a computation you can write down; it is a platform property the target grants (shared buffers + real threads) or does not (pure isolates). Where granted, wrap; where not, serialize (correct, not parallel) or Fail.
	- Intrinsics residue: the semantics transpile fine as loops; the performance intent is not a computable object and cannot ride along.
- Compressed: **everything whose meaning is a computation becomes write-once; what remains is meaning that is a platform property.**

---

## Entry 2026-07-22 — Class 7 demoted: the service itself is transpilable

Sequence of corrections, each narrowing the residue:

- First position (wrong): class 7 wraps at high cost or fails — the target must offer an equivalent threading API.
- Second position (still short): class 7 is platform-service dependence — the language holds a promise, the platform holds the fulfillment, the service interface binds them (the `DisplayModule` pattern from the communication protocol).
- Resolution (the owner's push: "the service is transpilable, not just the expectation"): the fulfillment is code too. A scheduler is an ordinary program — a loop holding paused executions, picking one, running to a switch point, saving state. Mutexes and condition variables are computation. Write the scheduler once in disciplined Python, transpile it: a green-thread scheduler in the semantic registry, self-hosted like PseudoUint64. Precedent: Go's runtime, Erlang's VM, QEMU — they carry their own concurrency service as ordinary code rather than wrapping the platform's.
- Consequence: class 7 *correctness* transpiles completely, even to pure-isolate targets. On one executor interleaved by your own scheduler, memory-visibility divergence disappears.
- The sole survivor: the count of physical executors. The scheduler distributes across cores; the number arrives as an input (`num_cpus`), never as a computation. Transpiling an allocator does not create RAM; transpiling a scheduler does not create cores. A service is code plus a resource — the code transpiles, the resource is what the platform has.
- Reclassification: styled identically and transpiled with its service, class 7 produces identical *outputs* everywhere, at different *speeds*. By this study's definition of implicit uniqueness (divergent outputs), class 7 is not a member — it is a performance concern. The conjecture's machine-model list shrinks to classes 1 and 8.
- Same demotion applies to the intrinsics residue: semantics transpile as loops; only speed diverges.

---

## Entry 2026-07-22 — Class 7 final resolution: the withholding runtime

Final correction (the owner's push: the OS service already exists and is agnostic to who requests it):

The run-time stack on any target:

```
hardware          cores exist
OS                scheduler exists, serves any caller
host runtime      the target language's VM/runtime
your program      the transpiled code
```

- The OS scheduler requires no transpilation. It exists on the target machine and serves any caller. The compiler's knowledge of how to invoke it is ordinary business logic and transpiles like everything else.
- The transpiled program does not sit on the OS; it sits on the **host runtime**, and can reach only the services the host runtime exposes.
- Egress to C, Rust, Go, Java: host runtime passes OS threading through. Class 7 is a non-problem — real threads, real cores, no simulation.
- Egress to Dart or browser JavaScript: the OS scheduler exists one layer down, but the host runtime **withholds** it (isolates / workers instead of shared-memory threads). Only here does the self-hosted green-thread scheduler (previous entry) enter — as a workaround for the withholding runtime, not as a replacement for the OS.
- Prior framings, corrected: "simultaneity is not a computation" — true but irrelevant; nobody computes it, the OS dispenses it. "The target must offer an equivalent API" — right shape, wrong party: the machine and OS always have the service; the variable is the host runtime's API surface.
- Final classification: class 7 is neither machine-level nor language-level in the abstract. It is a **per-egress-target capability flag**: does the host runtime expose OS threading or withhold it? Exposed --> Map. Withheld --> Wrap (self-hosted scheduler; correct outputs, single-executor speed).
- Sole remaining residue: `num_cpus` — throughput varies with physical core count. True of ordinary native programs too; not a transpilation concern.

Status: class 7 resolved. The implicit-uniqueness membership list stands at classes 1 and 8 (machine-model, Wrap via self-hosted simulators) and classes 2–6 (language-model, candidates for Forbid via discipline rules). Open frontier: which of 2–6 the Universal Discipline already forbids, and the minimal divergent script suite.

---

## Entry 2026-07-23 — Machine-model examples and the consolidated program

Machine-model classes are **1 and 8 only** (class 7 exited via demotion). Divergent specimens, each a Python-styled script:

**Class 1 — value-model.**

```python
q = -7 // 2
```

Python: `-4` (floor). Naive Go/C/Java egress: `-3` (truncation). Fix: egress emits `floor_div(-7, 2)`, a self-hosted polyfill.

```python
x = 9223372036854775807   # 2^63 - 1
y = x + 1
```

Python: grows (arbitrary precision). Naive Go `int64`: wraps to `-2^63`, silently. Fix: discipline declares the type; the canonical semantics is enforced by polyfill on whichever target lacks it natively (including Python, if the declared type is `int64`).

```python
z = x >> 60
```

With `x` negative: arithmetic vs logical shift (the RyuJIT split). Fix: `shift_right(x, 60, signed=False)` at declared width.

**Class 8 — encoding.**

```python
s = "h🙂i"
n = len(s)
c = s[1]
```

Python: `n = 3`, `c = "🙂"` (code points). Java/Dart naive: `n = 4`, `s[1]` is half a surrogate pair. C naive: `n = 6` (bytes). Fix: `PseudoString` in the registry; `len`/`[i]` route through it everywhere.

**The consolidated program** — target: *computational equivalence*: Python-styled source produces identical intermediate results and outputs on every target from the user's perspective, even where the underlying operation differs.

| Class | What it takes |
|---|---|
| 1 value-model | Self-hosted polyfills (`floor_div`, `PseudoInt64`, ...), canonical semantics per declared type |
| 8 encoding | Same mechanism: `PseudoString`, canonical unit chosen once |
| 2 copy-model | Discipline rule: one aliasing convention (Python's) + explicit `.copy()` at borders |
| 3 evaluation-order | Egress rule: temporaries fix left-to-right order |
| 4 lifetime | Discipline rule: no effectful destructors; explicit try/finally scopes |
| 5 dispatch | Suspected forbidden by Concrete Constructs; verify |
| 6 collection-order | Canonical container polyfill: insertion-ordered map everywhere |
| 7 concurrency | Capability flag: Map to OS threads where exposed; self-hosted scheduler where withheld |

Summary shape: two classes need self-hosted polyfills, five need legislation (discipline), one needs a per-target capability check. The program is complete on paper; unproven parts are coverage (classes 9+?) and the discipline audit for 2–6.

---

## Entry 2026-07-23 — Reframing: the CST ordering and origin-specified operators

### The CST ordering as an audit axis

the owner's surface inventory, arranged by where meaning attaches:

- named structure: modules, classes, methods, attributes, functions, variables
- operators and control flow: `=, +, -, *, /, **, ==, >, <, >>, ...`; `if, for-each, while, ...` (often lower to simple IR opcode complexity)
- implicit imports (builtins): `list, dict, sort, len` — the semantic registry's jurisdiction
- IR opcodes (often lower to simple arch opcode complexity)
- machine-model / services

The eight classes say *how* meaning diverges; this ordering says *where in the CST it can attach*. Crossing them gives a finite audit table: for each CST node kind, for each class, is behavior uniform across the 12? Filling it is mechanical. This converts "are there classes 9+?" from speculation into a checklist.

### Origin-specified operators

Notation: `j.+`, `p.//`, `c.>>` — an operator qualified by origin language. Native semantics needs no qualifier (in a Python-mode frame, `+` not `p.+`).

- An implicit uniqueness is a divergence with no surface signal. An origin qualifier IS a surface signal. The notation does not work around implicit uniqueness — it **abolishes the category** by giving every divergent operator an explicit spelling.
- The defaulting rule keeps the common case clean and makes every borrow greppable: exotic semantics announce themselves in the source.
- Implementation cost is already paid: `j.//` resolves to the same self-hosted polyfill (`trunc_div` vs `floor_div`) the class-1 program requires anyway. Qualifiers are surface syntax over the existing registry.
- A frame-level machine-model annotation is the same mechanism at coarser grain: an origin qualifier applied to a whole scope instead of one operator.

---

## Entry 2026-07-23 — PCv7: the ingress-hub inversion

the owner's proposal: a Python-central language (working name PCv7) with selectable machine-model modes per scope. Any of the 12 languages maps trivially in; once in, other languages' semantics (and via egress, their tooling) become usable. Analogy: English absorbing loanwords, but with a checkable grammar.

### The inversion

- PseudoCoup as built: **egress hub** — write disciplined Python once, emit 12.
- PCv7: **ingress hub** — absorb 12, host centrally, egress retained.
- "Trivially mapped" holds for a precise reason: ingress into PCv7-java-mode crosses no semantic distance. Canonicalizing translation must polyfill or forbid every divergence; a mode *contains* the source language's semantics, so code enters carrying its own meaning, divergences preserved.

### The border grammar (the sole new content)

- The modes contain nothing new — they are the 12 languages, inherited. PCv7's entire new intellectual content is the **border grammar**: the dev-time check at every frame border, with a three-way verdict per crossing object:
	- **identical** — representation matches; passes free.
	- **convertible** — a defined coercion exists; the compiler inserts it, visibly. Note: dev-time checking makes crossings safe and explicit, not free — differing representations still cost a copy at run-time. The win is that the cost has a visible spelling instead of being ambient (contrast cpyext: hidden toll on every crossing forever).
	- **incompatible** — Fail loudly (the Golden Rule's third branch).
- Precedent: Rust's `Send`/`Sync` — a compile-time grammar for what may cross a concurrency border.
- The eight classes relocate here: they are the row-headers of the **conversion lattice**. Examples: class 1 border — int64-wrap value entering an arbitrary-precision frame: convertible (widen). Class 2 border — value-copy struct entering a reference-model frame: convertible via copy, or incompatible if aliasing is load-bearing. Class 7 border — shared-memory object entering an isolate-mode frame: incompatible; message-pass instead.
- Not 12×12: route conversions through a PCv7-canonical form — 12 mappings in, 12 out.
- Hybridization policy: one mode per project remains the safe default ("effectively language X with Python-style annotation" — the owner); mixed modes are governed, not forbidden — "use at own risk" becomes "use where the lattice says convertible."

### English, structured

Loanwords keep foreign spelling — *schadenfreude*, *déjà vu* — visibly marked borrows inside an absorbing host grammar. That is the origin-qualifier rule exactly: `j.+` is a loanword spelling; unqualified `+` is native vocabulary. PCv7 is English plus the property English lacks: a checkable border grammar deciding what a loanword may touch.

### Caution: "other language tools"

- Other languages' *semantics*: yes — the modes.
- Other languages' *tooling and packages*: they operate on that language's source, so using them requires egress into the language and ingress of results back. The roundtrip verification suite is therefore not a demo — it is the load-bearing wall of PCv7: the borrow-a-package workflow IS a roundtrip.

### Resolution of the derivative question

Translating out was never about functionality; it is about occupying runtimes you don't own (iOS/Swift, Flutter/Dart, browser/JS, teams maintaining output). Dropping egress would owe PCv7 a compiler, per-platform runtimes, and an ecosystem — language 13, inheriting the un-portability PseudoCoup is a coup against. The language is already built — defined by subtraction (discipline) and annotation (qualifiers, modes), borrowing Python's toolchain at dev-time, with the 12 targets as its runtimes.
