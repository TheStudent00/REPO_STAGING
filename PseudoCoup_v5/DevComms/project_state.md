# Project State

One page. Update at the end of every working session.

## As of 2026-07-24

**Where we are:** theory phase complete enough to formalize. The
two-layer program (basis vs derived) is the organizing frame; 20
policies consolidated; divergence suite built and passing in the hub.

**Settled:**

- 8 divergence classes, membership final: 1+8 machine-model (Wrap),
  2-6 language-model (Forbid/legislate), 7 demoted to performance
  → DevComms/language_divergence_study_log.md
- minimum intention set: 11 objects; audit found no 12th
  → Designing/minimum_intention_set.md
- row satisfiers: 7 of 10 intent rows have one; B/E/J solved in-hub
  → Designing/intention_row_satisfiers.md, BEJ_expansion.md
- restriction-egresses-trivially rule; proofs live in hub only
- two-layer program: egress difficulty concentrates in the basis
  → Designing/two_layer_program.md
- 20 policies → Designing/PCv7_policy_decisions.md

**Formalization queue (from two_layer_program.md): COMPLETE**

1. ~~divergence script suite~~ DONE → Research/divergence_suite/
2. ~~basis audit as probes~~ 12/12 DONE → Research/basis_audit/
   (basis layer GREEN, no unsolved work cells; Swift via podman;
    all pre-registered predictions confirmed)
3. ~~verdict tables as data~~ DONE → Designing/pc_verdicts.json
   (built + validated by Designing/build_verdicts.py; 45 t2 pairs,
    108 basis cells, 11 border-lattice entries; tables generator
    now importable as the single data source)
4. ~~int64-on-JS evaluation~~ DONE → Research/int64_js/
   (verdict: BigInt asIntN — correct AND faster than Long emulation)

**Open questions held by the owner:**

- ~~dominance vs primitiveness~~ SETTLED (was a stale carry-over in
  the handoff draft, corrected 2026-07-25). two_layer_program.md
  §1/§6: dominance selects semantics, primitiveness orders egress
  work — different questions. Decisive reason (the owner): the hub must
  DOMINATE intentions because that is what makes ingress trivial;
  a dominating canon means any of the 12 maps in with no semantic
  distance to cross. Tables 3/4 stay frozen as-is.
- performance-primitive completeness (candidates: tail calls,
  string builder)

**Session log:**

- 2026-07-24: docs migrated from PseudoIR/DevComms into this repo;
  structure DevComms/Designing/Research established; suite verified.
- 2026-07-24 (later): git_commit_push.sh added (the owner runs it to push);
  int64-on-JS probe run under Node 22 — BigInt wins on correctness
  and speed; basis audit int64 cell now solved.
- 2026-07-24 (later still): basis audit probes built and run for
  Python/JS/C++/Ruby with results matrix; probe protocol documented
  for the remaining 8 targets.
- 2026-07-24 (evening): the owner ran toolchain setup + run_all.sh on
  host; 11/12 targets probed. All four pre-registered predictions
  confirmed (Go slice alias/detach, PHP array value-copy, PHP int
  float-drift, Rust moves). Trap canon nearly free everywhere;
  executor withheld on exactly JS/Dart/PHP.
- 2026-07-24 (night): Swift probed via podman container after
  swiftly cleanup; 12/12 complete. Only item 3 (verdict tables as
  machine-readable data) remains in the formalization queue.
- 2026-07-24 (night, cont.): item 3 done — pc_verdicts.json is the
  machine-readable single source (categories, t2 verdicts, P/O
  canons, basis audit, border lattice), validated on build. The
  formalization queue is complete; next frontier is the open
  questions the owner holds + first egress tooling consuming the JSON.
- 2026-07-24 (late): dev plan logged (DevComms/dev_plan_log.md);
  interp-insertion PoC scaffolded (Research/interp_insertion/):
  hand-sliced rust div_euclid chain, PCv3-mapped Python version
  (verified: Euclid properties pass on full grid), C insertion via
  int's empty @ slot in longobject.c, host build+verify script.
  Awaiting the owner's host run of build_and_verify.sh.
- 2026-07-25: routing-logic design settled and logged (supersedes
  the @-slot PoC layer). Scaffold started in Research/rust_routing/:
  RustI64 cell + output ring (mmap/mprotect/ctypes) BUILT AND
  PASSING — machine code produced in-process, mounted, called from
  stock CPython; rust truncating idiv observed (-7/2 = -3 vs
  Python's -4); i64 wrap confirmed; border refusal enforced.
  Next: cut the Cranelift slices per Research/rust_routing/
  slice_notes.md (needs rust source on host).
- 2026-07-25 (cont.): slice 1 (MIR routing) cut and verified.
  Slice 2 blocked on a finding: in cranelift 0.134 byte encoding
  moved out of emit.rs into the generated crate
  cranelift-assembler-x64. vendor_encoder.sh updated to fetch it;
  awaiting host rerun. emit.rs still owns the CheckedDivOrRemSeq
  routing (divisor==-1 branch + size selection), which IS worth
  slicing.
- 2026-07-25 (breakthrough): END TO END PASSES. slice 2 (encoder)
  cut from cranelift-assembler-x64 generated Rust (rex.rs, mem.rs,
  idivq_m/cqto_zo encode fns). Transpiled encoder produced bytes
  BYTE-IDENTICAL to the hand-verified idiv sequence — nothing
  hand-written. Chain: hub expr -> rust routing -> CLIF -> ISLE
  lowering -> rust encoder -> x86-64 bytes -> mmap -> executed in
  stock CPython, result in a RustI64 cell. Full i64 grid passes
  incl. MAX/MIN. Cornerstone established.
  Next: input ring (Ledger as TyCtxt) + invocation ring (import
  hook) to reach `a r./ b` surface spelling.
- 2026-07-25 (rings closed): input ring (ledger.py) + invocation
  ring (pc_import.py meta-path finder for .pc modules) + backend
  cache built. demo.pc executes REAL qualified spellings
  (a r./ b, a r.% b, chained r.*) with zero parser surgery, all
  driven by transpiled Rust routing/lowering/encoding. Added
  slice 1.5 (ISLE lowering: Sdiv/Srem arms + iadd/isub/imul) and
  three more encoders (addq_rm/subq_rm/imulq_rm). Srem differs from
  Sdiv only by `mov rax, rdx` — a distinction that came from Rust's
  own lowering table. Not cut: CheckedDivOrRemSeq guard (backend
  refuses those inputs), udiv/urem. verify_all.sh diffs an 81-row
  grid vs native rustc (host); sandbox ran an independent semantic
  check: ALL PASS.
- 2026-07-25 (subsequence check): our generated bytes vs native
  compiler output. Div/Rem/Mul appear VERBATIM inside gcc -O2's
  functions (only endbr64/ret around them), incl. the Rem
  `mov rdx,rax` tail from ISLE's lowering. Add/Sub are EQUIV:
  gcc chose lea (peephole) and the 0x29 encoding form of the same
  `sub rax,rsi` — proven equivalent by mounting gcc's OWN bytes and
  diffing results on a grid. test_subsequence.py picks up rustc
  automatically on the host for ground-truth rows.
- 2026-07-25 (GROUND TRUTH): the owner ran verify_all.sh on host with
  rustc present. All four test files pass AND the 81-row arithmetic
  grid is BYTE-IDENTICAL to native rustc output. The transpiled
  Rust routing/lowering/encoding pipeline is now verified against
  the compiler whose logic it extracts, not merely against our own
  semantic reasoning. Cornerstone fully validated.
  Also: assembler.rs grammar survey done — 1071 encode() functions,
  14876 lines, ZERO unclassified; ~12 node kinds total (let, method
  call, if-let x2 variants, brace; RHS: self.field.enc(), bool/int
  literal, name, assoc fn call, self.field.method()). The arch
  vocabulary's transpiler grammar is closed and tiny. Second,
  richer grammar in the hand-written support layer (rex.rs/mem.rs,
  ~1000 lines) is where polyfill wrappers matter.
  Open (the owner's calls): emit .py vs in-memory; whole vocabulary vs
  on-demand (survey argues whole); generated output vs meta-generator
  (survey argues generated).
- 2026-07-25 (TIER A TRANSPILER): Research/vocab_transpiler/ built.
  Decisions taken (the owner): emit .py files (stability layer, versioned
  against source compiler — churn guard); whole vocabulary; generated
  output not meta-generator.
  Result: assembler.rs (9.3 MB, 1071 instructions) -> pc_vocab/
  (1.3 MB, 19 modules), ZERO unsupported nodes, regeneration is
  byte-identical (no timestamps -> real diffs only).
  Acceptance chain: rustc == hand transpile == auto transpile, on all
  9 gate checks incl. REX.B path. Breadth over all 1071: 756 encode
  cleanly, 315 hit MARKED cuts (VEX/EVEX SIMD), 0 transpiler faults.
  Two grammars confirmed: generated (12 node kinds, no arithmetic) vs
  hand-written support layer (rex/mem/gpr/xmm/custom.rs) where the
  uniform u8() polyfill policy is applied.
  Cuts carry reachability invariants, asserted at the cut site.
  Discovered en route: generated code has an escape hatch
  (crate::custom::encode::nop_*) into hand-written custom.rs — those
  nop encoders transpiled into the support layer.
- 2026-07-25 (LLVM investigation, the owner's push): traced the LLVM
  chain in real source rather than characterizing it. Read set
  fetched (Research/llvm_trace/, sparse llvm-project pinned to
  llvmorg-21.1.8 to match system llvm-tblgen-21).
  CHAIN CONFIRMED (file:line):
    sdiv -> ISD::SDIV   SelectionDAGBuilder.cpp:3794 (visitSDiv)
    ISD::SDIVREM -> IDIV64r + CQO   X86ISelDAGToDAG.cpp:6002
    IDIV64r = 0xF7 / MRM7r          X86InstrArithmetic.td:207
    REX byte                        X86MCCodeEmitter.cpp:306
  FABLE CORRECTION: earlier claim that LLVM selection is "compressed
  tables with no readable per-instruction code" was OVERSTATED —
  IDIV64r has an empty .td pattern list and is hand-selected in a
  plain C++ switch. Retracted and re-measured (below).
  NOTABLE: LLVM's REX line `0x40 | W<<3 | R<<2 | X<<1 | B` is
  character-identical to Cranelift's — our transpiled polyfill is
  faithful to both compilers.
- 2026-07-25 (SONNET SURVEY, measured): Research/llvm_trace/
  survey_results.md + survey_inc.py.
    X86GenDAGISel.inc   375,884 lines, 357 unclassified (0.095%)
    X86GenInstrInfo.inc 162,160 lines,  92 unclassified (0.057%)
    Cranelift baseline   14,876 lines,   0 unclassified
  DAGISel is ~99.5% ONE opaque MatcherTable[] byte array interpreted
  by a hand-written bytecode VM (SelectionDAGISel.cpp:3240
  SelectCodeCommon), NOT per-instruction functions — so the table
  claim holds for the generated matcher, while X86ISelDAGToDAG.cpp
  Select() has 210 hand-matched cases as escape hatch (IDIV64r among
  them). Both were true; each of us had half.
  X86 never runs -gen-emitter at all: X86MCCodeEmitter.cpp (2033
  lines) is 100% hand-written — architecturally opposite to
  Cranelift's 1071 generated readable encode() fns.
  VERDICT: LLVM's generated code is NOT transpilable by the 1:1
  function strategy that worked for Cranelift. Cranelift decision
  stands, now on measured grounds.
- 2026-07-25 (POINTER MEASUREMENT + PLAN): measured pointer usage in
  LLVM's three key files. Across all three: ZERO pointer-expression
  derefs, ZERO memcpy/memset/reinterpret_cast/new[]. Every flagged
  "pointer arithmetic" site is an integer counter (CurOp++); every
  -> is object navigation (free in Python). So PseudoMemory is NOT
  needed for LLVM's encoder — the residue Fable hedged about does
  not exist. Correction #3 this session (after the matcher-table
  claim and the C++-discipline claim): characterize only after
  reading the lines.
  Also settled: x++ in argument position transpiles to two
  statements, faithful because the param is by-value and there are
  zero multi-increment expressions — both verified, and the
  transpiler must ASSERT these rather than assume (divergence
  class 3 inside our own tooling).
  PLAN WRITTEN: DevComms/plan_2026-07-25.md
    Phase 1 close Cranelift work (differential test at full scale;
            machine-transpile the support layer; cut the two marked
            gaps) — no new dependencies
    Phase 2 C++ ingress transpiler targeting X86MCCodeEmitter.cpp
            (smallest real C++ artifact with a verifiable output;
            acceptance = bytes match the Rust-transpiled vocabulary)
    Phase 3 decision point, deliberately unplanned: aarch64 vs the
            selector vs return to language-side work
  Strategic framing recorded: Cranelift was a quarry not a
  dependency; pc_vocab encodes the ISA (LLVM's REX line is
  character-identical, gcc's bytes match verbatim), so there is
  nothing to abandon. LLVM buys architectures + optimization +
  alignment, and its cost splits: encoder ~= rex.rs difficulty,
  selector expensive.
- 2026-07-25 (PHASE 1.1 differential harness): built in
  Research/vocab_transpiler/differential/ (Sonnet).
  Rust harness GENERATED but NOT COMPILED (no cargo in sandbox):
  covers 973/1071 (90.8%); 98 skipped are Amode-only lock/RMW
  instructions with no register-based fallback (listed in
  SKIPPED_RUST.txt).
  Python side RAN CLEAN: 1946 lines (973 instrs x 2 operand keys —
  RAX/RSI and R14 for the REX.B path), 1328 clean encodes, 618 CUT
  (all VEX/EVEX AVX — the marked SIMD cut), 0 errors, 0 missing.
  No suspected transpiler bugs found.
  AWAITING DEE: run ./run.sh in that folder (needs cargo) to perform
  the actual Rust-vs-Python byte comparison. Residual risk: the
  generated harness/src/main.rs has never been compiled, so expect
  possible Rust type/syntax errors on first build.
- 2026-07-25 (DIFFERENTIAL TEST RAN — the owner, host): 1328 (instr,key)
  pairs compared. 1318 exact, 10 MISMATCH, 0 errors.
  THE TEST FOUND A REAL BUG, exactly as intended. All 10 were
  nop_5b..nop_9b — the custom.rs escape-hatch encoders, which Fable
  had extracted with a HAND-ROLLED script matching only
  `buf.put1(...)`. It silently dropped `buf.put2(0x00_00)` and
  `buf.put4(...)`, so those nops emitted 2-4 bytes short.
  Root cause is a policy violation by Fable: hand-rolling an
  extraction instead of using the transpiler is precisely the
  "mixed depth" failure the uniform-no-exemptions rule forbids.
  FIXED: custom.rs re-extracted handling put1/put2/put4/put8
  uniformly plus underscore-separated literals (0x00_00). 34 emit
  calls extracted. All five nops now byte-identical to rust.
  test_vocab.py still ALL PASS; python side of differential
  re-run clean (1946 lines, 0 CUT/ERROR after the AVX stubs were
  exercised differently — see below).
  Coverage recorded honestly: rust harness constructs 973/1071
  (98 Amode-only lock/RMW instructions skipped, listed in
  SKIPPED_RUST.txt); 618 pairs are the marked VEX/EVEX cut.
  AWAITING: the owner re-runs ./run.sh to confirm 1328/1328.
- 2026-07-25 (PHASE 1.1 COMPLETE): differential test PASS after the
  custom.rs fix. 1328/1328 exact byte matches, 0 mismatches,
  0 errors. Coverage honestly bounded: 973/1071 instructions
  constructible by the harness (98 Amode-only skipped), 618 pairs
  behind the marked VEX/EVEX cut.
  The transpiled x86-64 vocabulary is now verified against Cranelift
  itself at scale, not just on 9 sample instructions.
  Remaining in Phase 1: (2) machine-transpile the support layer,
  (3) cut CheckedDivOrRemSeq + udiv/urem.
- 2026-07-25 (PHASE 1.2 COMPLETE): support layer is now MACHINE
  TRANSPILED. Research/vocab_transpiler/transpile_support.py ->
  vocab_support_gen.py (419 lines). Second grammar built: brace-
  balanced block extraction + recursive-descent expression parser
  implementing Rust's precedence chain, statement transpiler for
  let / if-else / ternary / field assign / assert / struct literal
  (incl. multi-line folding) / calls / implicit-return bare exprs.
  Sources: rex.rs gpr.rs xmm.rs mem.rs custom.rs imm.rs fixed.rs
  api.rs — reachable surface only; Display/fmt/visit/Amode/VEX cut
  with asserted reachability invariants.
  Mechanical reductions each carry a citation AND a programmatic
  precondition check that fails loudly if source shape changes
  (e.g. the Imm8/16/32/64+Simm merge asserts all 7 encode() bodies
  match the expected text before collapsing).
  GATES (re-verified independently by Fable, not taken on report):
    1. test_vocab.py with vocab_support_gen substituted:
       VOCABULARY: ALL PASS (756 clean, 315 expected cuts, 0 faults)
    2. differential/run_python_side.py with gen substituted:
       1946 lines BYTE-IDENTICAL to the rustc-verified python_out.txt
       (1328 clean, 618 cut, 0 errors)
    3. regeneration deterministic: PASS (byte-identical)
  NOTE: Fable's first re-verification of gate 2 reported 0 lines —
  that was a harness bug on Fable's side (lost __name__/path in a
  -c exec), not a failure. Corrected before reporting.
  The hand-written vocab_support.py is retained as the reference;
  vocab_support_gen.py is its verified machine-produced twin. The
  uniform-automation-reach hole is closed.
  Remaining in Phase 1: item 3 — cut CheckedDivOrRemSeq + udiv/urem.
- 2026-07-25 (PHASE 1.3 COMPLETE — PHASE 1 DONE): both marked gaps cut.
  * CheckedDivOrRemSeq guard (emit.rs:215) transpiled for srem:
    cmp rsi,-1 / jne / xor edx,edx / jmp / cqto+idiv, with
    displacements resolved by a two-pass measure-then-emit (no
    hand-written offsets). srem(MIN,-1) now returns 0 instead of
    being refused.
  * udiv/urem cut using divq_m pulled from the machine-transpiled
    pc_vocab rather than the hand slice — new encoders now come from
    the verified source by default.
  BUG FOUND AND FIXED BY THE EXTENDED GRID: the -1 guard was
  initially applied to urem as well, returning 0 for
  urem(a, u64::MAX) because that pattern reads as -1 when signed.
  The guard is signed-only. Only sdiv still refuses one input
  (i64::MIN/-1, a genuine overflow trap).
  Verification: extended 130-row grid (signed incl. -1 divisors +
  unsigned incl. u64::MAX) passes an independent semantic check;
  verify_all.sh all four suites ALL PASS; test_vocab.py ALL PASS.
  ground_truth.rs + verify_vs_rustc.py extended to cover the new
  paths — the owner can diff against native rustc.
  PHASE 1 COMPLETE (differential test, support-layer transpiler,
  both cuts). Next per plan_2026-07-25.md: Phase 2, C++ ingress
  transpiler targeting X86MCCodeEmitter.cpp.
- 2026-07-25 (PHASE 2 COMPLETE): C++ ingress transpiler built.
  Research/cpp_ingress/ — transpile_cpp.py (~1030 lines) ->
  llvm_encoder_gen.py, from LLVM's X86MCCodeEmitter.cpp
  (pinned llvmorg-21.1.8). Regeneration byte-identical.
  Scope: modRMByte, emitRegModRMByte, emitSIBByte, the REX prefix
  helper (setR/setX/setB/setW + emit's None/REX arms), emitByte.
  Cut with asserted invariants: REX2/VEX2/VEX3/XOP/EVEX arms and
  all non-REX fields — test verifies all five cut arms raise.
  ACCEPTANCE (diverse double compiling — two compilers, two
  transpilers, one answer):
    modRMByte  vs encode_modrm   256/256    exact
    REX byte   vs RexPrefix      131072/131072 exact
    SIB byte   vs encode_sib     256/256    exact
  REAL FINDING (out-of-domain): LLVM's modRMByte does NO masking and
  relies on assert(); Cranelift masks (& 3, & 7) and uses
  debug_assert!. In RELEASE both guards vanish — so out of domain
  LLVM's raw formula can exceed a byte (Mod=255,Reg=255,RM=255 ->
  0x3fff) while Cranelift silently wraps to 0xff. Inside the
  asserted domain they are identical. This is a genuine
  source-language difference, not a transpiler artifact; both
  transpiles reproduce their source's guard faithfully.
  Judgment call recorded: emitRegModRMByte calls getX86RegNum()
  (needs MCContext/MCRegisterInfo, out of scope) — the transpiler
  asserts that exact substring then substitutes a resolved-register
  parameter, mirroring how vocab_support treats Gpr.enc().
  Measured: 111 x++/++x in the file, all outside the transpiled
  slice; the split rule never fires but still asserts.
  PHASE 2 COMPLETE. Next per plan: Phase 3 decision point
  (aarch64 vs the ISel selector vs return to language-side work) —
  deliberately unplanned, to be decided on the evidence now in hand.
- 2026-07-25 (HAND-OFF): DevComms/HANDOFF_2026-07-25.md written —
  detailed hand-off covering what is built/verified, all measured
  findings, decisions and who made them, an explicit error record,
  how to run everything, and the forward plan.
  DIRECTION SET BY DEE: complete solution for the RUST LANGUAGE
  first (dominant intentions), mapped to ALL architectures via LLVM.
  CRANELIFT IS RETIRED — proof of concept and partial oracle only.
  It is NOT in any forward plan. pc_vocab remains as a frozen,
  version-pinned x86-64 oracle with no run-time dependency.
  Fable misread "complete solution for Rust" as "all of Cranelift's
  architectures" — corrected; the hand-off states the retirement
  explicitly so it cannot recur.
  Forward sequence (HANDOFF s7): (1) aarch64 encoder via the
  existing transpile_cpp.py, survey its grammar first; (2) the
  MIR->LLVM-IR front half in rustc_codegen_ssa/llvm (Rust, small,
  located); (3) price the ISel gap only after 1-2 — options are
  hand-map the few opcodes the hub emits / transpile SelectCodeCommon
  with the table as data / use llvmlite as oracle; (4) repeat per
  architecture.
  [SUPERSEDED 2026-07-27 — see next entry: LLVM x86-64 first,
  aarch64 after; HANDOFF s7.2 rewritten.]
- 2026-07-27 (corrections + plan): three corrections from the owner,
  documents updated to match.
  * ORDERING: Fable had put the aarch64 encoder first. Wrong — the
    Cranelift-derived pc_vocab is an x86-64 oracle, so the LLVM
    chain is established on x86-64 FIRST, where every piece is
    byte-checkable against an independent extraction. aarch64 only
    after the chain stands. HANDOFF s7.2 rewritten (6 steps).
  * LEDGER: neither Research/rust_routing/ledger.py (57-line PoC
    stand-in) nor PseudoCoup/pseudocoup/core/ledger.py is "the"
    hub ledger — the owner's intent is that the hub ledger STARTS from
    the most advanced existing ledger and grows past it. Survey of
    all ledger*.py under ~/Programming: PCv3 origin 45 lines; most
    advanced type ledger 289 lines (identical in PseudoCoup/,
    PseudoCoup_v4/, WFL_PseudoCoup/); separate structural lineage
    in PseudoCoup_v0 pseudokotlin (ledger.py 370, ledger_unified.py
    323 — id-keyed one-record-per-node superset). Seed choice is
    the owner's; carried as a workstream in the new plan.
  * VOCABULARY: "egress language" rejected as a category name —
    egress/ingress are directions relative to a perspective,
    source/target are roles relative to a perspective. Settled:
    "target language" (one of the 12) vs "architecture"
    (instruction set); slice/stub kept. HANDOFF s8.1 and
    open_issues.md corrected; dev_plan_log.md, this file's older
    entries, and Research READMEs still carry old words.
  PLAN WRITTEN: DevComms/plan_llvm_rust_2026-07-27.md — the Rust
  LLVM compiler path: 6 stages (complete LLVM x86-64 encoder vs
  oracle; MIR front half vs --emit=llvm-ir; IR->ISD slice; price
  the selector; all-LLVM chain then slice dominant intentions;
  aarch64+) plus the ledger workstream and a proposed
  Research/llvm_rust/ layout. First action: node-kind census of
  X86MCCodeEmitter.cpp's full emission path + the
  X86GenInstrInfo.inc row format.
