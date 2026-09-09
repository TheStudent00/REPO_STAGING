# log 073 — the optimizer probed, and the O0 anchor ruled in

2026-08-24, conversation with the owner, following log_072's instrument
build. Airlock outputs of record: `ce_routes.txt`,
`ce_opt_form.txt`, `ce_rec_and_o0.txt`, `ce_o0_go.txt` (in
`Airlock/agent/out/`; lane scripts in `drop/.done`).

## 1. the route probes (the owner's idea): vary HOW a value reaches the
operator, read what survives

Five routes to one add, C (clang -O1) and Go (default), measured:

- local copy (`t := a; t + b`) — ERASED, both languages;
  byte-identical to the direct add.
- inlinable identity function — ERASED, both.
- literals (`2 + 3`) — folded to `mov $5`, both. (the owner's suspicion
  about literal sums confirmed.)
- no-inline identity function — SURVIVES in Go (`//go:noinline`
  honored: b parked to stack, fetched back, the operand's arrival
  visibly changed). DEFEATED in C: clang honors noinline but
  separately proves the function returns its argument, substitutes
  the result, deletes the dead call, and drops the function body.
- Conclusion: the route is a real knob, but only where the detour
  survives; which detours survive is itself a per-compiler
  measurement.

## 2. what form the optimizer works on (measured, not asserted)

Same `a + b`, clang, two settings:

- `-O0` IR: two `alloca`s, two `store`s, two `load`s, one `add` —
  every variable has a MEMORY HOME; a dumb, faithful transcription.
- `-O1` IR: one `add`, one `ret`.

So the optimizer does not work on arch opcodes; it works on the
middle form, whose one-definition-per-value shape makes who-uses-
what an explicit graph — it optimizes by graph rewriting, the same
edge-walking our map does. Arch-level work is a final touch-up.

## 3. the arms race, tested on the owner's recursive carrier

The construct: `carry(x, n)` counts n down through recursive calls
and delivers x untouched.

- clang -O2 ERASED it — even with n UNKNOWN at compile time
  (`use_param` compiles to the bare `lea`). Mechanism: tail
  recursion becomes a loop; loop analysis proves x unchanged each
  iteration; the loop collapses to x. The optimizer does not need
  general proof, only induction patterns, and this is one of its
  oldest.
- Go KEPT the call chain (shallower optimizer).
- Standing conclusion: outsmarting the rule library is fragile per
  compiler and per version — a losing foundation, though the rule
  inventory is measurable if ever wanted as data.

## 4. the contract barrier (inert logic for ANY operand type)

Empty inline assembly, `__asm__ volatile("" : "+r"(a))`:

- INERT, verified: fenced add is byte-identical to the direct add —
  the barrier contributes zero instructions.
- UNSIMPLIFIABLE, verified: `2 + 3` folds to `mov $5`; with the
  barrier on the 2, the output is `mov $2; add $3` — the add is
  forced to exist. Not by outsmarting: the compiler's own contract
  says "this value may have changed in a way you cannot see".
- Generality: `"+r"` pins anything register-sized; `"+m"` pins
  anything addressable. Go analogs: `//go:noinline` (held, §1),
  `runtime.KeepAlive`.

## 5. THE FINDING BANKED: the optimizer off switch is the identity
anchor

Every AOT compiler in the line already ships the off switch —
built for debuggers, supported by contract, no compiler
modification needed:

    clang -O0        rustc -C opt-level=0
    go build -gcflags="-N -l"        swiftc -Onone

Measured at -O0 (C):

    mov %edi,-0x4(%rbp)     ; a stored to its own slot
    mov %esi,-0x8(%rbp)     ; b stored to its own slot
    mov -0x4(%rbp),%eax     ; a fetched back
    add -0x8(%rbp),%eax     ; b arrives at the add FROM ITS SLOT

and the compiler's own table names the slots:

    DW_AT_name: a   DW_AT_location: fbreg -4
    DW_AT_name: b   DW_AT_location: fbreg -8

Go `-N -l` shows the same shape (parameters parked to stack slots,
add, result stored). Rust at level 0 keeps its overflow check
visible (`add; seto; jo -> panic`) — the semantics before polish.

**The layering ruled in (the owner: "weve found our solution"):**

- **anchor**: the un-optimized build — every named variable has a
  memory home, every operand arrives from its home, name->home
  stated by the compiler's own debug table. The high-level-name to
  low-level-operand identity is OBSERVABLE BY CONTRACT here.
- **ship**: the optimized build — what the arch campaign measures.
- **diff**: route probes and the anchor/ship pair measure exactly
  what the optimizer changed between the two states.

Scope caveat, stated so the finding is not over-read: identity
proven at the anchor is a fact about the anchor mode's own code;
it carries to the optimized build through the diff or the pinning
kit, not automatically.

## 6. what this closes and what it feeds

- Closes the "how do we observe the variable's arrival" question
  without an arms race and without compiler modification.
- Feeds the allocator question from log_072: at the anchor, the
  allocator's choice is trivial (operands live in memory homes),
  so the anchor + the forced probe bracket the choice from both
  sides.
- The diary, the map, the arch-units, the route probes and the
  anchor are now five instruments of one kit, each with its
  evidence class stated.
