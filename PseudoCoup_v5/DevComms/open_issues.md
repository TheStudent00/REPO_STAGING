# Open Issues

Each issue carries a **provenance** line so it is verifiable at a
glance whether it concerns future development (the LLVM path) or the
retired Cranelift artifact. Retired items are not work; they are
recorded so they are not mistaken for work.

**As of 2026-07-27 there is one open item — Issue 2's scheduling —
and it blocks nothing.** Issues 1 and 3 are kept as closed records
rather than deleted, because in both cases the reasoning fell and the
reason it fell is worth preserving.

Settled elsewhere, listed only so they are not re-opened:

- **The basis layer is not defined by egress.** The hub dominates intentions; a destination language's shortfall is recorded as a shortfall. See Issue 1 and [HANDOFF_2026-07-25.md](file://PseudoCoup_v5/DevComms/HANDOFF_2026-07-25.md) §8.1.
- **Dominance vs primitiveness** — closed. See [two_layer_program.md](file://PseudoCoup_v5/Designing/two_layer_program.md) §1. Dominance selects semantics, primitiveness orders egress work; they answer different questions. Decisive reason: the hub must dominate intentions because that is what makes ingress trivial.
- **Ingress memory model** — closed, measured. The C++ pulled into the hub needs none. See Issue 3 below for the three memory questions kept apart.
- **Parser-level qualifiers** — closed as a decision, reduced to scheduling. See Issue 2.

**Word note (corrected 2026-07-27, the owner):** "**target language**"
means one of the 12 languages the hub renders to; "**architecture**"
means an instruction set such as x86-64 or aarch64 (earlier drafts
used "target" for both). **Egress/ingress are directions relative to
a perspective, never category names** — transpiling Rust into Python
is an egress from Rust (source) and an ingress to the hub (target).
An earlier draft of this document used "egress language" as a
category; those uses are corrected below except inside the
historical-record block of Issue 1, which preserves the old wording
as part of the record.

---

# Issue 1 — Performance-primitive completeness — CLOSED 2026-07-27

- **Provenance: FUTURE, and dissolved rather than answered.**
- **Status: CLOSED by the dominance rule.** The question only existed under a destination-first definition of the basis layer, which contradicts a decision already recorded.

- **Why it dissolves (the owner, 2026-07-27).** Intent is captured at ingress and lives in the Ledger; a source declaring a hash map records that type, a source declaring a list of pairs records a different one. The hub satisfies the intent by feature insertion — the mechanism already proven by inserting Rust's routing into CPython. A target language without fast retrieval renders a program without fast retrieval, which is a **recorded shortfall of the destination**, not a loss in the hub. Improving destinations later by feature insertion is possible and unscheduled. Ingress is the current priority.
  - This applies identically to hashing, the string builder, and the executor. None of them needs adjudicating.
  - The type identity is Ledger data. **Corrected 2026-07-27:** an earlier version of this bullet called [PseudoCoup/pseudocoup/core/ledger.py](file://PseudoCoup/pseudocoup/core/ledger.py) "the Ledger" — it is the most advanced ledger in the PCv3 type-ledger lineage (289 lines, fed by the tree-sitter ingressors), but the hub's ledger does not exist yet. the owner's intent: the hub ledger starts from the most advanced existing ledger and grows past it. Survey and the choice it leaves open are recorded in [HANDOFF_2026-07-25.md](file://PseudoCoup_v5/DevComms/HANDOFF_2026-07-25.md) §5 case 7 and [plan_llvm_rust_2026-07-27.md](file://PseudoCoup_v5/DevComms/plan_llvm_rust_2026-07-27.md).

- **Tail calls are resolved separately and need no category.** The hub performs the transformation itself, so every target language gets constant stack regardless of its own compiler. Self-recursion rewrites to a `while` loop at no cost; mutual recursion uses a wrapper that returns a description of the next call to a driver loop, at one allocation per step. Both preconditions — every call in tail position, and one step leading to at most one next step — are visible in the source, so the hub chooses without asking. Full mechanism with code in [HANDOFF_2026-07-25.md](file://PseudoCoup_v5/DevComms/HANDOFF_2026-07-25.md) §8.1.

- **Historical record of the closed argument, kept because the reasoning fell rather than merely ending.**

- **The basis layer is the set of things every egress language must supply natively or cheaply, and most of its members are there because of what they mean.** bool, int64, list, record are in the basis because no combination of the other members constructs them.
  - Two members — hashing and the executor — are there for a different reason, and my original phrasing for that reason was wrong.
    - I wrote "meaning preserved, intent destroyed" and leaned on "a program doing a million lookups". The threshold was doing work the argument should not need, and the owner rejected it.
  - The corrected reason needs no threshold: **the choice of data structure IS a choice of complexity class.**
    - A developer writing `d[key]` did not merely intend "retrieve the value associated with this key" — a list of pairs does that too. They intended *associate-with-fast-retrieval*.
    - That is exactly why `map` and `list` are separate objects in the minimum intention set rather than one object with two spellings. If the complexity were not part of the intention, one object would suffice.
    - So the failure of a derived map is not that it becomes slow at some workload size. It is that we silently substituted a different data structure than the one the developer selected, while the values coming out stay correct.

- **Working definition, section 4 form:**

```
performance-primitive
    a basis member whose COMPLEXITY CLASS is
    part of the intention it expresses.
    Deriving it preserves the values and
    substitutes a different complexity class
    -- i.e. substitutes a different intention.
    example tied to context:
        PC.map derived as a list of pairs
        returns the same value for every key
        and turns O(1) lookup into O(n). The
        program is correct and is no longer
        the program that was written.
```

- **Confirmed member: hashing.** Clean fit under the definition — O(1) versus O(n), values identical.

- **Possible mis-fit: the executor.** It may belong in the basis for a different reason than hashing does, which would mean it is not a performance-primitive at all.
  - Concurrency (divergence class 7) was demoted precisely because outputs are identical and only speed varies; simultaneity was established as a *resource*, not a semantic.
  - That is a different argument from the complexity-class one. The executor is plausibly a basis member under policy 7 (platform capability: exposed or withheld per egress language) rather than under this definition.
  - **Needs a decision: same category, or its own.**

- **Candidate: tail calls — probably the wrong category entirely.** Under the sharpened definition this looks like a correctness matter, not a performance one.
  - Without tail-call elimination, deep recursion overflows the stack. The program does not return a correct answer more slowly; it fails to return at all.
  - A crash is a meaning difference. That would put tail calls with the divergence classes rather than the performance-primitives.
  - **Needs classification before it can be accepted or rejected.**

- **Candidate: string builder — looks like a clean fit.** Same shape as hashing.
  - Repeated concatenation over immutable strings is O(n²) where a builder is O(n). Values identical, complexity class substituted.
  - Every egress language has a builder idiom: `StringBuilder`, `Vec<u8>`, `[]byte`, `strings.Builder`.
  - **Needs confirming, not investigating.**

- **The four questions this argument produced, all now moot.** Whether the executor was a performance-primitive or a platform capability; whether tail calls were a performance or a correctness matter; whether the string builder was in; whether anything else was missing. None of them needs an answer, because none of them constrains the hub.

---

# Issue 2 — Parser-level qualifiers

- **Provenance: FUTURE.** This concerns the hub's surface syntax and a forked CPython. It is independent of which compiler supplies the target semantics, so Cranelift's retirement does not touch it.
- **Status: DECIDED. The fork is the plan and always was. What remains is scheduling only; the first draft wrongly presented the decision itself as open.**

- **The record, since the first draft misrepresented it.** the owner asked "why wouldn't we be inserting into the interpreter?"; the answer given was that insertion is where this road ends on purpose, and the import hook was explicitly framed as measuring everything except the fork. the owner accepted that sequencing. The direction was never in question.

- **What exists now is a text rewrite, not grammar — a deliberate stepping stone.** [pc_import.py](file://PseudoCoup_v5/Research/rust_routing/pc_import.py) is a meta-path finder: it reads the `.pc` file, rewrites `r./` into `|_r_div|` before Python parses it, then compiles normally.
  - This runs on stock CPython with no fork, which is why it was cheap and why it shipped first.

- **It costs three things, all real, and all three are what the fork buys back.**
  - Precedence is wrong: `|` binds much lower than division, so `a r./ b + c` does not group the way a reader expects.
  - Error messages point at code nobody wrote — the rewritten text, not the source.
  - Qualifiers cannot appear everywhere; only in positions where the `|x|` infix trick is syntactically legal.

- **The fork makes `r./` a genuine token with genuine precedence.** Its cost is a forked interpreter, rebuilt per Python release, installed by every hub user — the maintenance bill the ABI-freeze analysis mapped earlier in the project. That bill is accepted, not under review.

- **The only open part is when.** Pencilled at PCv6. It is not a prerequisite for any current work, and nothing is blocked by it today.

---

# Issue 3 — Memory: three separate questions, kept apart

- **Provenance: MIXED, and that is the point of this entry.** The first draft filed one memory question under the retired vocabulary and thereby reopened a question that had already been measured and closed. There are three, and they belong to different parts of the project.
- **Status: two closed, one dormant. No open work here.**

- **Question A — ingress. Does the C++ we pull into the hub need a memory model? CLOSED, measured: no.**
  - Across `X86MCCodeEmitter.cpp`, `SelectionDAGISel.cpp`, `X86ISelDAGToDAG.cpp`: zero pointer-expression dereferences, and zero `memcpy` / `memset` / `reinterpret_cast` / `new[]`.
  - Every `->` is object navigation, free in Python because Python objects are already references. Every site flagged as pointer arithmetic is an integer counter (`CurOp++`), which is what an earlier 0.2–5% estimate was actually counting before it was retracted.
  - Recorded in [HANDOFF_2026-07-25.md](file://PseudoCoup_v5/DevComms/HANDOFF_2026-07-25.md) §3.3 and [plan_2026-07-25.md](file://PseudoCoup_v5/DevComms/plan_2026-07-25.md).

- **Question B — egress. Can pointer infrastructure be rendered into a language that has no addresses? CLOSED in principle, priced, dormant in practice.**
  - Answer: yes. Simulate the address space rather than mapping pointers to references — one large byte array in the target language, a pointer becomes an integer index into it, `*p` becomes a read at that index, `p + 4` stays integer addition. Arena allocators transpile untouched, because an arena is pointer arithmetic over a region and that is now honest integer arithmetic over the array. Emscripten is the existence proof.
  - The price: output stops being idiomatic and becomes a machine simulation written in the target language, with every struct field access an offset computation. **Idiomatic rendering and pointer fidelity pull in opposite directions.**
  - Dormant because nothing currently egresses pointer-bearing compiler source. It becomes live only if compiler guts are rendered to a target language, which is not in any current phase.

- **Question C — the emitted instructions. Will we emit x86 memory operands? Not yet; unreachable by caller invariant, and asserted.**
  - `Amode` means a memory operand: `add rax, [rbx+8]` rather than `add rax, rcx`. 98 of the 1071 encoders take only memory operands (lock and read-modify-write forms). `GprMem` handles the register form and raises on the memory arm.
  - The pipeline constructs `GprMem(reg)` and never a memory operand, so the arm is unreachable. That is a property of the callers, not of the encoder, which is why the stub asserts its reachability condition instead of assuming it.
  - It becomes reachable the moment register allocation spills. Register allocation is not scoped, so this is a consequence to track, not an issue to resolve.

- **The retired part, so it is not mistaken for work.** The VEX/EVEX stubs (618 differential pairs, the AVX and AVX-512 prefix encodings) sit in the Cranelift-derived vocabulary, which is kept only as a frozen oracle for cross-checking the LLVM-derived encoder. The oracle does not need to cover instructions we never ask it about. Completing them is work on a retired artifact.

---

# Terminology fix, pending the owner

- **The word "cut" has been used for two opposite things across the project docs**, which is the ambiguity §1 of the protocol warns about.
  - "cut from generated Rust" means *extracted*.
  - "marked cut" means *excluded*.
- **Proposed:** **slice** for extracted, **stub** for excluded. This document already uses the proposed terms.
- **Also in the sweep:** "target" split into **target language** and **architecture**, per the corrected word note at the top ("egress language" was the first proposal and was rejected — egress is a direction, not a category).
- **If agreed, the sweep covers** the handoff, the plan, `dev_plan_log.md`, `project_state.md`, and the four `Research/*/README.md` files.
