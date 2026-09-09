# Project Plan

the owner's high-level draft, 2026-07-27. The high level (Level 1) is the
frame; Level 2 below expands each component one step deeper without
changing the frame. Depth grows by adding levels, not by editing
Level 1 without the owner.

---

# Level 1 — components and goals (the owner's draft)

### core components

**transpiler**:

* PCvX (whatever the most advanced transpiler is)

**intentions**:

* json of language assessments -- intention dominance as data
  (exists already but requires validating)

**lessons**:

* info that is useful from the current (erroneous) project state
  (requires validating also)

**polyfill**:

* wrappers from transpilation that the required filling to match
  source behavior

**slicer**:

* the system that uses intentions (json) to extract the slice of the
  source compiler and inserting it into the hub interpreter.

### project goals

#### ultimate

greatest amount of automation of transpiling and slicing of
languages (in particular the 12 languages)

#### intermediate

Rust (LLVM) transpiling and slicing

---

# Level 2 — one step deeper per component

Each component: what exists now, what needs validating, what is
missing. Claims marked (measured) come from commands run this
project; claims marked (unverified) have not been checked this
session.

## transpiler

- One lineage, evolving through versions. There is one PseudoCoup
  transpiler; X in PCvX is a variable over its version-states.
  Transpiling Kotlin into Dart and transpiling rustc's routing into
  Python are the same job — a source language into a target
  language — exercised on different pairs. PCvX may be PCv5.
- "Most advanced" means most sophisticated at ACCURATELY
  transpiling — not most advanced with respect to any particular
  source/target pair (the owner). The current version can hold advanced
  tools despite being misaligned in other respects.
- Version-states known so far, each exercised on different pairs
  (capability inventory across versions is the survey's job):
  - v0–v4 lineage states carry tree-sitter ingress, the ledger,
    and emitters, exercised on application code between two of the
    12 (Kotlin→Dart, Kotlin→Python).
  - the v5 state added three source grammars (generated Rust:
    `transpile_vocab.py`; hand-written Rust: `transpile_support.py`;
    hand-written C++: `transpile_cpp.py`), the polyfill layer, and
    differential verification, exercised on compiler code
    ingressing to the hub (measured, all acceptance tests passing).
- The survey's output is a capability inventory per version, not a
  single winner: nothing says the most advanced state lives in one
  place. The expected move is to combine the best components from
  each version, or at minimum harvest lessons, to find or build the
  most advanced version.
- Survey DONE 2026-07-27: `transpiler_survey_2026-07-27.md`.
  Headline: "most advanced" is distributed — no version-state holds
  the best of more than two capabilities; a best-in-class-per-
  capability harvest map exists; two IR philosophies (tagged-tree +
  registry vs flat-opcode mining) coexist un-unified, and their
  relationship is the first design decision of the combined
  transpiler.

## intentions

- What exists now: `Designing/pc_verdicts.json` — 45 compat pairs,
  108 basis cells, 11 border-lattice entries; `build_verdicts.py`
  refuses to emit if anything is incomplete (measured at build
  time).
- Needs validating (the owner's requirement):
  - whether dominance is actually IN the JSON as data, or still only
    in the markdown analyses (`minimum_intention_set.md`,
    `intention_row_satisfiers.md`, `two_layer_program.md`)
    (unverified);
  - whether the slicer can drive from this JSON as-is — i.e. does a
    verdict row carry enough to select WHAT to slice from a source
    compiler, or only whether a pair is compatible (unverified).

## lessons

- What exists now, worth keeping regardless of the misalignment that
  surrounded it — all (measured):
  - Extraction works: compiler routing logic can be transpiled and
    executed inside CPython, verified byte-identical against native
    rustc (the 130-row grid; 1328/1328 differential).
  - Insertion works: machine code produced in-process, mounted
    (mmap/mprotect/ctypes), called from stock CPython, results in
    typed cells.
  - Generated compiler code is transpilable; hand-written tables are
    not (grammar censuses: Cranelift 0 unclassified vs LLVM's
    MatcherTable).
  - The C++ needed has no memory model requirement (zero pointer
    derefs across the three LLVM files).
  - The ISA is the ISA: three compilers agree byte-for-byte because
    all transcribe Intel's manual — so an extracted vocabulary is
    version-pinnable, not compiler-hostage.
  - The 12-language basis audit (12/12 probed, predictions
    confirmed) and the 8 divergence classes with runnable suite.
  - The error record: every error was caught by a mechanical test
    with a falsifiable acceptance criterion; characterize-only-
    after-reading-the-lines.
- Needs validating: a pass separating measured-fact from
  characterization in the PCv5 documents, because the conversation
  that produced them was drifting. Not yet scheduled.

## polyfill

- What exists now (measured, passing): the fixed-width wrappers
  (`u8()`, `u32()`) matching source arithmetic behavior; applied
  uniformly, no exemptions — mixed depth is forbidden because an
  unwrapped node becomes ambiguous between "proven safe" and "tool
  missed it".
- The uniform rule earned its keep: the one hand-rolled exemption
  (custom.rs nops) produced the one silent wrong-bytes bug, caught
  by the differential test.
- Missing: nothing known for the grammars met so far. New grammars
  (new source files) may demand new wrappers; the census-first rule
  finds them.

## slicer

- What exists now: nothing, as a system. Every slice so far (MIR
  routing, ISLE lowering, encoders) was chosen and cut by hand, per
  experiment.
- What the experiments proved for it: both halves of its job are
  feasible — extraction (the transpilers) and insertion (the output
  ring into the hub interpreter). What no code does yet: consume the
  intentions JSON to DECIDE what to slice.
- This is the novel component and the direct path to the ultimate
  goal: automation lives here.
- Depends on: intentions validation (the JSON must carry enough to
  drive selection), transpiler survey (what the slicer calls to do
  extraction).

## goals

- ultimate — greatest automation of transpiling and slicing of the
  12 languages:
  - served by: the slicer (unbuilt), the intentions JSON as its
    steering data, the transpilers as its extraction arm.
  - measure of progress, proposed for later levels: how much of a
    new language/compiler pair is handled without hand-written
    slices.
- intermediate — Rust (LLVM) transpiling and slicing:
  - the first full exercise of the system, on the architecture where
    an independent oracle exists (the Cranelift-derived x86-64
    vocabulary — measured, frozen, version-pinned).
  - the LLVM chain detail (which files, which stages, acceptance per
    stage) belongs at Level 3, not here. Current draft of that
    detail: `plan_llvm_rust_2026-07-27.md`, to be subordinated to
    this document.
