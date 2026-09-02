# Vocabulary Transpiler (Tier A)

Mechanically transpiles Cranelift's **generated** x86-64 encoder into
Python. The emitted `pc_vocab/` is PseudoCoup's **stability layer**:
versioned against the source compiler, changing only when we choose to
re-run this tool.

## Result

```
input     assembler.rs           9.3 MB, 1071 instructions
output    pc_vocab/              1.3 MB, 19 modules, 1071 classes
faults    0 unsupported nodes
determinism  regenerate -> byte-identical (no timestamps in output)
```

## Acceptance: the chain of trust

`python3 test_vocab.py`

```
rustc  ==  hand transpile  ==  auto transpile
```

The nine gate checks compare auto-transpiled encoders against the
hand-transpiled ones in `../rust_routing/slice_encoder.py`, which are
themselves byte-identical to native rustc (81-row grid, host run
2026-07-25). Both operand encodings tested (RSI and R14, i.e. the
REX.B path).

```
PASS  idivq_m rm=6 / rm=14      48 f7 fe / 49 f7 fe
PASS  cqto_zo                   48 99
PASS  addq_rm  rm=6 / rm=14     48 03 c6 / 49 03 c6
PASS  subq_rm  rm=6 / rm=14     48 2b c6 / 49 2b c6
PASS  imulq_rm rm=6 / rm=14     48 0f af c6 / 49 0f af c6

breadth over all 1071 encoders:
  encoded cleanly    756
  hit a marked cut   315   (VEX/EVEX SIMD — expected)
  transpiler faults    0
```

## The two grammars

| Layer | Source | Character |
|---|---|---|
| `pc_vocab/*.py` | generated `assembler.rs` | 12 node kinds, no arithmetic — mechanically transpiled |
| `vocab_support.py` | hand-written `rex.rs`, `mem.rs`, `gpr.rs`, `xmm.rs`, `custom.rs` | real arithmetic — **this is where polyfills live** |

Uniform-wrapping policy is applied in the support layer: every
arithmetic node in a u8-typed Rust expression is wrapped in `u8()`,
with no exemptions even where overflow is provably impossible. An
unwrapped node is therefore unambiguously a bug rather than possibly
a proof-based omission.

## Cuts, with reachability invariants

Cuts are not "not implemented" — each carries the invariant that makes
it unreachable, asserted at the cut site so a violation fails loudly
instead of emitting wrong bytes.

- `GprMem::Mem` (Amode encoding) — unreachable while all callers
  construct register operands (true until register allocation with
  spills is cut).
- `VexPrefix` / `EvexPrefix` — reachable only from AVX/AVX-512
  instructions; no current slice emits those.

## Decision 3, explained (why generated output, not the generator)

`assembler.rs` is not in Cranelift's repo — it is written at build
time by `cranelift-assembler-x64-meta` from instruction descriptions.
Two candidates to transpile:

- **the generator**: ordinary hand-written Rust (traits, iterators,
  string building, file IO). Would let our Python regenerate the
  vocabulary for any future Cranelift — but needs a large transpiler
  grammar, and large grammars are where inference creeps back in.
- **the output**: 12 node kinds, because the generator already
  flattened every decision into longhand.

We take the output — the same rule ISLE taught us: cut from generated
code, never from the DSL. The cost is being pinned to one Cranelift
version, which is the point rather than a defect: the emitted Python
changes when we re-run this tool, not when upstream moves.

## Regenerate

```
python3 transpile_vocab.py <path>/assembler.rs [outdir]
```

Each emitted module carries provenance: source filename, source
sha256, Cranelift version, transpiler version. No timestamps, so
regeneration is deterministic and `git diff` shows real changes only.
