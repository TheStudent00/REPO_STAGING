# Plan — the Rust LLVM compiler path — 2026-07-27

The goal in one sentence (the owner's): construct the tools to transpile
and polyfill the Rust compiler (LLVM) into CPython, then slice the
dominant intentions from that transpiled compiler.

Ordering rule (the owner, 2026-07-27): **LLVM x86-64 first.** The
Cranelift-derived `pc_vocab/` is an x86-64 oracle; x86-64 is the one
architecture where every LLVM-derived piece can be byte-checked
against an independent extraction of the same ISA. Other
architectures only after the chain stands there.

All file names and directory names below are **proposals** for the owner
to accept or rename.

---

## 1. The chain being transpiled

What rustc actually runs, in order. Each row's output is the next
row's input:

| stage | produces | lives in | language |
|---|---|---|---|
| MIR routing | MIR ops from source constructs | `rustc_codegen_ssa/src/mir/rvalue.rs` | Rust |
| LLVM IR building | LLVM IR opcode (macro-generated: sdiv → `LLVMBuildSDiv`) | `rustc_codegen_llvm/src/builder.rs` | Rust |
| FFI wall | the Rust→C++ crossing | `rustc_codegen_llvm/src/llvm/ffi.rs` | Rust decl |
| IR→ISD | ISD nodes | `llvm/.../SelectionDAGBuilder.cpp` | C++ |
| instruction selection | machine instructions | `X86ISelDAGToDAG.cpp` + MatcherTable VM | C++ |
| encoding | bytes | `X86MCCodeEmitter.cpp` | C++ |

Status per stage, measured this project:

| stage | state | evidence |
|---|---|---|
| MIR routing (`rvalue.rs`) | located, not transpiled | HANDOFF §7.1 |
| LLVM IR building (`builder.rs`) | located, not transpiled | macro table read |
| IR→ISD (`SelectionDAGBuilder.cpp`) | traced for sdiv (:3794), not transpiled | HANDOFF, project_state 07-25 |
| ISel selector | measured, not transpiled, choice unpriced | 1,145-line VM, 173 opcodes, 210 hand cases |
| encoder (`X86MCCodeEmitter.cpp`) | slice transpiled + verified | modRM 256/256, REX 131,072/131,072, SIB 256/256 vs the Rust-side encoder |

Tools already built and reusable: `transpile_vocab.py` (generated
Rust), `transpile_support.py` (hand-written Rust), `transpile_cpp.py`
(hand-written C++), the `u8()`/`u32()` polyfill layer,
`output_ring.py`, `rust_cell.py`, `pc_import.py`. Sources are pinned
(`llvmorg-21.1.8` in `Research/llvm_trace/`).

---

## 2. Stages

### Stage 1 — complete the LLVM x86-64 encoder

Extend the Phase 2 slice to the full per-instruction path of
`X86MCCodeEmitter.cpp`: `encodeInstruction`, opcode byte emission,
immediate emission, and the operand walk (`CurOp`). The grammar is
already measured as tractable (0 templates, 0 pointer derefs; the
one node rule is the `f(x++)` split, asserted).

- Inputs the encoder needs that are NOT in the .cpp: per-instruction
  data from `X86GenInstrInfo.inc` (opcode, TSFlags, operand layout).
  That file is ~87% struct/enum/string tables — carried as **data**,
  not transpiled as code. A reader script extracts the rows for the
  instructions in scope.
- Acceptance: bytes identical to the `pc_vocab` oracle for every
  instruction both sides cover; the existing 130-row grid vs native
  rustc stays green.

### Stage 2 — the MIR→LLVM IR front half

Transpile `rvalue.rs`'s `BinOp` routing and the
`math_builder_methods!` expansion in `builder.rs`. Rust source,
grammars already handled by `transpile_vocab.py`/`transpile_support.py`.

- Acceptance: for each hub operator, the LLVM IR opcode our
  transpiled routing selects equals what `rustc --emit=llvm-ir`
  produces for the same construct.

### Stage 3 — the IR→ISD slice

Transpile the `SelectionDAGBuilder.cpp` visit arms for exactly the
opcodes the hub emits (`visitSDiv`, `visitMul`, …). Per-opcode,
small, same C++ grammar as stage 1.

- Acceptance: ISD node sequence matches what `llc -debug` prints for
  the same IR (unverified that `llc -debug` output is stable enough
  to diff mechanically — check before relying on it).

### Stage 4 — price the selector, then decide

Between stage 3 (ISD node) and stage 1 (machine instruction) sits
the ISel gap. Three options, cost order, no pre-commitment:

- (a) hand-map the opcodes the hub actually emits — integer
  arithmetic is a handful; honest if recorded as a stub with an
  asserted reachability invariant.
- (b) transpile `SelectCodeCommon` (1,145-line VM) and carry
  `MatcherTable[]` as data — full solution, expensive.
- (c) llvmlite as a reference oracle rather than an extraction.

Decision input from stages 1–3: how much of the chain's behavior the
hub actually exercises.

### Stage 5 — all-LLVM chain; slice dominant intentions

Swap the running `demo.pc` chain to LLVM-derived stages end to end;
`pc_vocab` and the Cranelift slices leave the running path and remain
the oracle. Then slice the next dominant intentions from the
transpiled compiler — per the satisfier rows (suspension, optionals,
pattern matching, scoped cleanup), each intention gets its routing
sliced the way integer arithmetic was.

### Stage 6 — aarch64, then further architectures

`transpile_cpp.py` on `AArch64MCCodeEmitter.cpp`, grammar survey
first. No oracle exists there; native
`rustc --target aarch64-unknown-linux-gnu` is the only ground truth.
Front half (stages 2–3) is shared; only encoder/selector work is
per-architecture.

---

## 3. Ledger workstream (parallel, not blocking stages 1–4)

the owner's intent on record: the hub ledger for this path **starts from
the most advanced existing ledger and grows past it**. Survey of
2026-07-27 (every `ledger*.py` under `~/Programming`):

| lineage | file | lines | records |
|---|---|---|---|
| type ledger origin | `0_Archive/PseudoCoup_v3/pseudocoup/core/ledger.py` | 45 | FQDN types, wrappers, memory_erasure, JSON dump/load |
| type ledger, most advanced | `PseudoCoup/pseudocoup/core/ledger.py` (= v4 = WFL copy, md5-identical) | 289 | + param shapes (bare + scoped), method returns, suspend, symbol owners, singletons, enums, async-required |
| structural fidelity | `StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/ledger.py` | 370 | per-object shape + 1-degree wiring, source side vs introspected output side |
| unification | same dir, `ledger_unified.py` | 323 | ONE id-keyed record per source node, whole corpus, superset schema |
| PCv5 stand-in | `Research/rust_routing/ledger.py` | 57 | declared types for r.i64/r.u64; answers `type_of`/`binop_types` only |

- The stand-in derives from none of the lineages. It stays until the
  hub ledger exists, then is replaced behind the same two calls
  (`type_of`, `binop_types`) so the routing slices do not change.
- **Open, the owner's call:** which seed — the 289-line type ledger
  (role match: it answers the TyCtxt-style questions) or
  `ledger_unified`'s id-keyed one-record-per-node schema (the more
  advanced structure). A workable line: 289-line as the base, adopt
  unified's id keying when ingress work starts, since id generation
  is defined against a source tree and the hub's tree-sitter ingress
  provides one.

---

## 4. Proposed file system

New root: `Research/llvm_rust/` — one directory per chain stage,
each self-contained with its own test, matching the repo's existing
one-experiment-one-directory shape.

- `Research/llvm_rust/`
  - `README.md` — scope, how to run, provenance.
  - `sources/`
    - `vendor.sh` — pinned fetch: llvmorg-21.1.8 + the rustc tag.
    - `PINS.md` — exact tags and paths of every vendored file.
  - `encoder_x86/` — Stage 1.
    - `transpile_encoder.py` — driver over `transpile_cpp.py`.
    - `instrinfo_reader.py` — `X86GenInstrInfo.inc` rows → data.
    - `llvm_encoder_x86_gen.py` — OUTPUT (deterministic, provenance header).
    - `test_vs_oracle.py` — bytes vs `pc_vocab`, per instruction.
    - `test_vs_rustc.py` — grid vs native rustc (host).
  - `mir_front/` — Stage 2.
    - `transpile_mir.py` — driver over the Rust transpilers.
    - `mir_binop_gen.py` — OUTPUT.
    - `test_vs_llvm_ir.py` — vs `rustc --emit=llvm-ir`.
  - `isd_build/` — Stage 3.
    - `transpile_isd.py` — driver.
    - `isd_gen.py` — OUTPUT.
    - `test_vs_llc.py` — vs `llc -debug` (stability unverified, §2 Stage 3).
  - `selector/` — Stage 4. `PRICING.md` first; code only after the decision.
  - `chain/` — Stage 5.
    - `demo.pc` — the hub module.
    - `run_chain.py` — hub expression → … → bytes → output ring.
    - `test_all_llvm.py` — asserts no Cranelift import in the running path.
  - `ledger/` — the §3 workstream.
    - `ledger.py` — seeded per the owner's choice.
    - `test_ledger.py` — the gate.

Conventions carried over unchanged: generated files are the
stability layer (deterministic, no timestamps, provenance header);
stubs assert reachability invariants; every directory's test is
runnable alone; `verify_all.sh`-style aggregation at the root once
two or more stages exist.

Not in scope anywhere above: register allocation (spill paths stay
stubbed), VEX/EVEX SIMD, the Amode/memory-operand path — each
remains a stub with an asserted invariant until an intention needs
it.

---

## 5. First action

Stage 1: survey the full `X86MCCodeEmitter.cpp` emission path the
way `assembler.rs` was surveyed (node-kind census before transpiling),
plus the `X86GenInstrInfo.inc` row format for the in-scope
instructions. Measure first; the census decides how much
`transpile_cpp.py` must grow.
