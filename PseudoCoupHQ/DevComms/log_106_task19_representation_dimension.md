# log_106 -- TASK 19: the representation dimension, as a measured proposal

## Walkthrough (plain words first)

The question this task answers: when an interpreter (CPython, PHP,
Ruby) adds two numbers, its machine code looks nothing like a
compiled language's `add` -- it starts by dereferencing pointers or
testing tag bits. Does that mean the interpreter has a DIFFERENT
operator, or the SAME operator whose inputs just ARRIVE differently
(through a pointer, through a tag) before the real addition happens?

the owner's lean going in: it's mostly the second thing (his "option B with
a bit of A") -- the pointer changes how the value ARRIVES, not what
gets computed, so a typed-pointer interpreter unit should be able to
join the same family as the plain-integer compiled unit, carrying its
representation as an extra fact rather than a different membership.

This task does NOT decide that -- the owner ratifies, this task only builds
the evidence he ratifies FROM (log_101 sec4's own words, restated: "membership
is the owner's ruling, not yours"). Four pieces of evidence were built:

1. **Every compiled-language unit now carries an explicit ARRIVAL
   statement.** Before this task, canon7's per-unit record
   (`context_record`) said WHERE a value sits (which register, how
   wide) but never HOW it got there. Now every one of the 1,779
   compiled units across c/cpp/go/rust/swift carries an `arrival`
   block saying `representation: "plain"` and `unpacking_prefix: []`
   -- stated on paper, not left implicit. The reasoning: a compiled
   unit's two operands are already plain fixed-width register values
   the moment the unit starts, so there is nothing to unpack before
   the two operands' derivation lines (their "lineages") meet -- the
   meeting point (formally: LINEAGE CONFLUENCE, AgentMemory 2026-08-31)
   is the unit's very first instruction.

2. **One interpreter handler got the FULL treatment: carved, proved.**
   CPython's fast integer-add path (`long_add`, the "both operands
   are small enough" branch) was already carved in a prior session's
   `interp_fastpath.json`: 8 instructions unpack two pointers'
   `ob_digit[0]` fields into two plain 64-bit integers (that's the
   ARRIVAL prefix), one `lea` instruction adds them (that's the
   COMPUTATION), and everything after boxes the answer back into a
   pointer (irrelevant to the addition itself). This task reused that
   carve and its verdict: z3 PROVED the one add instruction computes
   the exact same function as c's plain 64-bit addition, for every
   possible input, not just the ones where CPython's fast path is
   taken. So for this ONE handler, the representation-dimension idea
   is not a guess -- it is measured and proved.

3. **The other eight handlers (four PHP, four Ruby) were REFUSED
   honestly, not forced.** A full carve needs a complete disassembled
   instruction slice cut into blocks; that re-extraction (Task 20's
   fixed cutter) was only run on CPython's slice this session. For
   the other eight, only a short excerpt exists (from a prior task,
   `interp_relations.json`) -- enough to say what REPRESENTATION each
   operand arrives in (pointer-to-struct, or a tagged integer, or a
   VALUE dispatcher check), not enough to carve a real boundary or run
   a proof. So this task states the representation for all nine and
   states, honestly, that eight of the nine have no computation-part
   proof this session -- rather than inventing one.

4. **CPython's `growing` mode row (from a separate, already-approved
   ruling) was added to the guard record, and it DOES form its own
   family.** Separately from the representation question: CPython's
   integer add, when its operands are NOT both "compact" (small
   enough), doesn't wrap or trap -- it branches into a different
   routine (the arbitrary-precision digit loop) and the answer grows
   as many digits as it needs. That's a third kind of "what happens on
   the edge of the domain," different from wrapping (like Go) or
   trapping (like Rust). This is its FIRST measured instance in the
   corpus. Run through the same family-building step every other
   guard row goes through, it forms its OWN one-member family
   (`EF0039`) -- meaning: nothing already in the corpus matches it, as
   expected, since it's the first of its kind.

## Instances (the real data, verbatim)

### Instance A -- CPython long_add's arrival prefix (carved this session, reused from interp_fastpath.json)

```
mov    $0x1,%edx               %edx = $0x1
mov    0x18(%rcx),%ecx         %ecx = 0x18(%rcx)   # b's ob_digit[0]
mov    %rdx,%rax               %rax = %rdx
sub    %r8,%rdx                %rdx = %rdx - %r8   # apply a's sign
sub    %rsi,%rax               %rax = %rax - %rsi  # apply b's sign
imul   %rcx,%rax               %rax = %rax * %rcx  # medium_value(b)
mov    0x18(%rdi),%ecx         %ecx = 0x18(%rdi)   # a's ob_digit[0]
imul   %rcx,%rdx               %rdx = %rdx * %rcx  # medium_value(a)
```
Boundary (lineage confluence, the first instruction that reads BOTH
unpacked values): `lea (%rax,%rdx,1),%rdi` -- the first place either
value COULD be summed, and where CPython's own source sums them.

### Instance B -- the proof (real z3 output, restated verbatim from interp_fastpath.json, reused not re-run)

```
z3_bounded_domain_check: unsat  (no a,b in the compact domain differ)
z3_unbounded_check_also_run: unsat  (no a,b AT ALL differ, ever)
verdict: PROVED
```
Reading: within (and beyond) the domain where CPython takes this
path, its add computes the IDENTICAL function of two integers that
c's `lea (%rdi,%rsi,1),%rax` computes. The representation differs
(pointer vs plain); the computation does not.

### Instance C -- the would-be table rows for CPython long_add (from proposal_representation_dimension.json)

Under option B (new representation-keyed family):
```json
{
  "family_kind": "NEW representation-keyed family (option B, log_101 sec4)",
  "family_key": "(representation='typed-pointer(PyLongObject*)')",
  "row": {
    "representation": "typed-pointer(PyLongObject*)",
    "members": "cpython/long_add"
  }
}
```
Under B-with-A (the owner's lean -- joins the same-seed family, representation as a dimension):
```json
{
  "family_kind": "JOINS the same-seed family (option B-with-A, the owner's lean): representation carried as a DIMENSION on the existing row, membership unchanged",
  "row": {
    "joins_class": "c/rust/go/swift/cpp/kotlin i64,i64 + (the seed lea/add family the compiled table already carries)",
    "representation_dimension": "typed-pointer(PyLongObject*)",
    "arrival_prefix_dimension": "8 instructions (medium_value(a)/medium_value(b) extraction), condition-gated: only reached under _PyLong_BothAreCompact(a,b)",
    "proof_basis": "PROVED (z3, both bounded and unbounded checks unsat)"
  }
}
```

### Instance D -- one of the eight honest refusals (php add_function, representative of the pattern)

```json
{
  "representation": "typed-pointer(zval*)",
  "arrival": {
    "status": "REFUSED -- no full instruction slice was re-extracted and block-cut for this handler in this session ...",
    "boundary": null
  },
  "proof": {
    "attempted": false,
    "verdict": "UNDECIDED (honest refusal, not forced)"
  },
  "would_be_row_option_b_with_a": {
    "family_kind": "CANNOT STATE -- proof against a candidate compiled class was not attempted ..."
  }
}
```
The other seven (php x3 more, ruby x4) carry the identical refusal
shape, each with its own representation:
- `php add_function`, `ZEND_ADD_SPEC_...`, `ZEND_ADD_LONG_SPEC_...`,
  `ZEND_ADD_LONG_NO_OVERFLOW_SPEC_...`: `typed-pointer(zval*)`
- `ruby rb_fix_plus`, `rb_int_plus`: `tagged-value(Fixnum, 2n+1 encoding)`
- `ruby rb_big_plus`: `mixed: typed-pointer(RBignum*) + tagged-value(Fixnum)`
- `ruby vm_opt_plus`: `tagged-value(VALUE, opaque-dispatch)`

### Instance E -- the growing mode row and its family (real output, `exception_families3.json`)

```
EF0039  [the operands are not both compact -- not _PyLong_BothAreCompact(a, b), i.e. at least one operand fails the cmp $0xf test at long_add+0x1f (the compact-fast-path unit carved in interp_fastpath.json is never entered) / grows]  langs=cpython  members=1
    cpython cpython/long_add_fastpath +          grows
```
This IS the first `growing` family (verbatim row above) -- confirmed
by re-running the exact family-clustering logic every other guard row
already goes through (`exception_families2.py`'s clustering, re-
pointed at the new `guards5.json` instead of `guards4.json`, logic
byte-for-byte unchanged). `growing` was not in the excluded-response-
head list, so it clustered on its own merit, same as every other row.

## Numbers

- Compiled units given an explicit ARRIVAL statement: **1,779** total
  (c 610, cpp 770, go 107, rust 125, swift 167) -- breakdown pasted
  from `entry_contract_arrival_index.json`'s own `per_lang_unit_counts`.
- Interpreter handlers considered: **9** (all `+`, per
  `interp_relations.json`'s own scope).
- Handlers with a full carve + z3 proof this session: **1**
  (cpython/long_add) -- verdict PROVED.
- Handlers refused honestly (no carve, no proof, stated why): **8**.
- Guard rows in the new guard record of record (`guards5.json`):
  **314** = guards4.json's 313 (unmodified, carried verbatim) + 1 new
  (`grows`, provenance-marked `provenance_is_weaker: true`).
- Exception families rebuilt (`exception_families3.json`): **40**
  families from guards5.json's rows (39 from guards4.json's data,
  unchanged in count/content, plus the new `EF0039` `growing`
  family). A `growing` family DOES form -- it is the first, exactly
  as the task asked to check.

## File inventory (every file created this task, all new, none pre-existing modified)

- `Research/op_pipeline/entry_contract_arrival_c.json` -- ARRIVAL
  extension, 610 c units.
- `Research/op_pipeline/entry_contract_arrival_cpp.json` -- 770 cpp
  units.
- `Research/op_pipeline/entry_contract_arrival_go.json` -- 107 go
  units.
- `Research/op_pipeline/entry_contract_arrival_rust.json` -- 125 rust
  units.
- `Research/op_pipeline/entry_contract_arrival_swift.json` -- 167
  swift units.
- `Research/op_pipeline/entry_contract_arrival_index.json` -- index
  over the five files above, per-language counts.
- `Research/op_pipeline/build_entry_contract_arrival.py` -- the
  generator for the six files above (step 1).
- `Research/op_pipeline/proposal_representation_dimension.json` --
  the step 2/3 deliverable: per-handler representation, arrival,
  computation, proof, both would-be rows.
- `Research/op_pipeline/build_proposal_representation_dimension.py`
  -- its generator.
- `Research/op_pipeline/guards5.json` -- the new guard record of
  record: guards4.json's 313 rows verbatim + 1 new `growing` row.
  `guards4.json` itself is UNMODIFIED (verified: `git diff --stat`
  empty on it).
- `Research/op_pipeline/build_guards5.py` -- its generator.
- `Research/op_pipeline/exception_families3.json` -- the rebuilt
  exception-family table (40 families, from guards5.json).
  `exception_families2.json` itself is UNMODIFIED (verified: `git
  diff --stat` empty on it).
- `Research/op_pipeline/exception_families3.py` -- its generator
  (`exception_families2.py`'s clustering logic, byte-identical, only
  its source/output filenames repointed).

## Gates run

```
$ python3 check_no_spelling_keys.py entry_contract_arrival_c.json entry_contract_arrival_cpp.json entry_contract_arrival_go.json entry_contract_arrival_rust.json entry_contract_arrival_swift.json entry_contract_arrival_index.json proposal_representation_dimension.json guards5.json exception_families3.json
```
All nine files: PASS (no operator token in any key, grouping, pairing
or row structure). `proposal_representation_dimension.json` failed on
its first run (the per-handler `operator` field sat on an object that
did not carry a unit-id field the checker recognizes) -- fixed by
adding a `unit` field (`"lang/handler"`) to each handler record, not
by removing the check or loosening it; re-run PASSED.

Zero-regressions check: `git diff --stat` against `guards4.json`,
`exception_families2.json`, `dominant_table24.json`, `dom_ops22.json`,
and all five `canon7_units_*.json` files -- empty on every one, before
and after this task's work. `dominant_table24.json` and
`dom_ops22.json` are never opened by `build_proposal_representation_
dimension.py` (verified by reading the script: no `open(...)` call
names either file).

Commit state: the repo-daemon had already committed every artifact
listed above by the time this log was written (`git log --oneline`
shows commit `549a955` for the proposal files and `37380df` for
`guards5.json`/its generator, both auto-commits) -- this is a message
for posterity, not a request to bank, per BANKING IS A MESSAGE, NOT A
COMMIT.

## What was refused, and why (restated, not buried)

- Eight of nine interpreter handlers' arrival/computation carve and
  proof: refused, because no full re-extracted+block-cut instruction
  slice exists for them this session (Task 20's re-extraction only
  covered CPython's `long_add`). Stated as `"UNDECIDED (honest
  refusal, not forced)"` in `proposal_representation_dimension.json`,
  never guessed at from the short representation-evidence excerpt
  alone.
- `dominant_table24.json`/`dom_ops22.json`: no changes attempted, no
  changes made -- membership is the owner's ratification.

## PROGRESS entry

Appended under the single `# PROGRESS` heading in
`Planning/node_0_3_research/node_0_3_5_compiler_graph/PROGRESS.md`.
