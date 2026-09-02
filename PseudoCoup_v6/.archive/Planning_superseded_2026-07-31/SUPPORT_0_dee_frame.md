---
id: pcv6.planning.dee_frame
level: 0
status: settled
settled_by: the owner
supersedes: null
---

# SUPPORT 0 — the owner's high-level frame (verbatim, 2026-07-27)

Provenance: the owner's draft, first placed in
`PseudoCoup_v5/DevComms/project_plan.md`. Changes only by the owner.

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
