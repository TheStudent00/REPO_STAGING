# Native composition of tools across languages and operating systems — exploration

Date: 2026-09-10. Status: exploration, not a plan. No planning node yet.
Origin: the owner's question whether the Hub can pull tools from any open
source, any language, any OS, into one native application.

## 1. What the project is

- Input: a set of open-source tools (any language, written for any OS)
  plus a target (language, OS).
- Output: one native program in the target, composed from those tools,
  each piece carrying a stated guarantee.
- Not Wine, not a container: the foreign tool becomes native source in
  the target, not a foreign binary in a foreign environment.
- Working name in this document: "the composer". Placeholder only.

## 2. What the line is expected to deliver (design assumptions)

- A1. Proved per-operator emulations per target language (AutoPoly),
  ground truth = z3 verdict on machine-form terms.
- A2. Source composition (hub_compiler) that joins proved pieces into
  proved straight-line sequences.
- A3. Memory and loops are the frontier: for a long time those parts of
  a tool are NOT proved. Design must not wait for them.
- A4. Intentions: ratified per-operator semantics, keyed by machine
  form, never by name (the spelling ban).
- A5. Language front ends arrive in the line's order (Kotlin/Java,
  Python, Dart, Haxe first; C/C++/Rust/Go later). The composer's
  tool candidates are gated by which front ends exist.

## 3. The four floors of any tool, and the guarantee at each

| floor | what it is | what the composer does | guarantee |
|---|---|---|---|
| 1 pure computation | arithmetic, logic, data structures, algorithms | transpile via the Hub | proved (A1, A2) where straight-line; A3 parts: tested |
| 2 runtime model | memory management, threads, exceptions, strings, floats | map the tool's runtime model onto the target's | tested; proved later |
| 3 OS interface | files, sockets, processes, display, input, IPC | per-OS-pair table of correspondences | tested; hand-written where no source on one side |
| 4 hardware / closed | drivers, closed libraries | nothing | wall |

- Every composed program ships a profile: how many units sit at each
  guarantee level. Same shape as the sandbox-OS security graph: a
  graph of components labelled by guarantee strength, never one score.

## 4. The key design object: the OS seam table

- A tool's OS-facing surface = the calls that do not resolve inside its
  own source closure. Linkers already compute this: undefined symbols
  after closure. So the surface is mechanical and measurable BEFORE
  any transpilation.
- One table per OS pair, keyed by effect on state (resource kind,
  operation, parameter shape), never by name — open() vs CreateFileW
  vs openat is the spelling ban at OS level. Same intention mechanism
  as A4, applied to OS calls.
- Populated on demand: only the entries the chosen tools use. Wine
  must cover everything; the composer covers what is pulled in.
- Guarantee per entry: proved when both sides are pure enough source
  (rare); differential-tested (same call, same observable outcome)
  as the norm; hand-written when one side is closed.
- Cost model: the price of bringing a tool over = number of distinct
  seam calls NOT already in the pair's table. This is the number that
  sizes every decision.

## 5. Sequencing that isolates one problem at a time

1. Same language, cross OS. Compose a Linux C++ tool and an Android
   C++ tool natively on Linux. Transpiler ≈ identity; the seam table
   does all the work. Tests the table alone.
2. Cross language, same OS. Compose a Java tool and a Python tool into
   one target on Linux. Seam table ≈ identity; the Hub does all the
   work. Tests the Hub alone.
3. Both. The real product.
4. Target = the sandbox OS's own control plane (libvirt pieces in C,
   Kata shim in Go, egress proxy in C, Airlock daemon in Python, graph
   model in Python) — the composer's first customer, and the OS
   project's userland factory. Ordering between them is open.

## 6. The first experiment (runnable now, no Hub needed)

- The census: for ~10 candidate tools across languages and OSes,
  compute source closure + undefined symbols → distinct seam calls per
  tool, per OS. Output: the seam-count table and the overlap between
  tools (how much one pair's table serves the next tool).
- Runs as Airlock lanes; needs only build systems + nm/ldd/import
  analysis. Memory bound must be stated in the brief.
- Decides: which tools go first, which OS pair goes first, and whether
  the seam surface is small enough for the project to exist.

## 7. Where it dies

- D1. Front-end coverage. If C/C++ into the Hub is far off, the only
  composable tools are in the line's languages. Mitigation: Android's
  framework side is Java/Kotlin — the line's strongest language — so
  the first tools come from there, not from C.
- D2. Runtime-model mismatch. A manual-memory tool into a GC target
  (or the reverse) needs a memory model in the target; that is A3.
  Mitigation: first target is a language with explicit memory (Rust
  or C) so the translation is nearest identity.
- D3. Build-system extraction. Gradle/CMake/Cargo closures are
  laborious; the census automates and measures it.
- D4. License closure. GPL anywhere in the closure = GPL program.
  The census records licences alongside seam counts.
- D5. Performance after transpilation into a different runtime model.
  Gate: ratio vs the original on the same inputs, reported per tool.

## 8. Gates (measured, never a single score)

- seam calls per tool per OS pair; table coverage before/after
- proved fraction / tested fraction / hand-written fraction per program
- differential-test pass rate on real inputs vs the original tool
- performance ratio vs original

## 9. Redundancy via proved equivalence (the owner, 2026-09-11)

- Idea: run K proved-equivalent variants of a unit; disagreement = a
  tamper signal; an attacker must compromise all K consistently.
- Prior art: N-version programming (Avizienis 1985; failed on
  correlated bugs, Knight & Leveson 1986); N-Variant Systems (Cox et
  al. 2006) and Orchestra: artificially diversified variants run in
  lockstep, syscalls compared; ~2x cost for K=2. Byzantine voting for
  masking (K=3 tolerates 1).
- What the line adds: variants are PROVED equivalent, so a divergence
  cannot be a benign bug in the proved span; and AutoPoly emits the
  same unit per target language, i.e. diversity (different runtime,
  different exploit surface) for free with the proof attached.
- Unit of redundancy = a span with a comparable output: a floor-1
  pure function, or a seam-bounded unit compared at the seam table.
  Nondeterminism (time, random, interleaving) must be fed as input
  to all variants (record/replay) — the main engineering cost, as in
  MVEE work.
- Three failure points:
  F1. Common input. Tampering upstream of the span is invisible; the
      span boundary is the detection boundary.
  F2. The comparator. Single point; must be minimal, proved, in the
      outermost trusted layer, unreachable from variants; variants
      commit a hash before any reveal.
  F3. Fake diversity. Same binary, same layout = one exploit hits all.
      Real axes: target language, isolation tier (variant per sandbox
      layer), compiler. Shared kernel and shared hardware are NOT
      diversified.
- Modes and cost (p = sample rate):
  lockstep: latency = slowest variant, compute K.
  async audit: latency ~1, compute 1 + p(K-1); detection delayed.
  majority mask (K>=3): continue on majority; attacker needs 2 of 3.
- Detection probability: persistent compromise caught with
  1-(1-p)^n over n checks; one-shot compromise caught with p only.
  These are the first CALCULABLE edges on the security graph.
- Divergence triage: frontier bug (memory/loops, unproved) /
  nondeterminism leak / hardware fault / compromise. Early on mostly
  the first, which makes the harness the Hub's continuous
  differential tester at no extra cost.
