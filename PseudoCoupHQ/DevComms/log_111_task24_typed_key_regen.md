# log 111 — task 24: the representation-dimension proof, regenerated with the DWARF-typed key

Date: 2026-09-01. Round 5, task 24. Gates the owner's ratification of
option B / option B-with-A.

---

## Walkthrough — what was wrong, what was read, what it now says

- **The defect, in the artifact it damaged.**
  `proposal_representation_dimension.json` (round 4) carries nine
  handler records. Its ONE proved record, `cpython/long_add`, reads
  in its machine field:

  ```
  "type_pair_read": "ptr64,ptr64"
  ```

  while its prose beside it reads `typed-pointer(PyLongObject*)`.
  The machine field is the one that counts, and `ptr64` is the bare
  pointer key log_103 task 19 forbade. Eight further records carry
  the same shape of bare width (`tagged64`, `ptr64,tagged64`,
  `opaque_VALUE_dispatch`, `ptr64,ptr64`).

- **Why the round-4 field could not have been better at the time.**
  The precedent, `fix_cpython_type_key.py`, split the read in two:
  the WIDTH came from the unit's own lifted expression (forced by
  construction), the NAME came from `long_add`'s C signature quoted
  in `interp_cpython.md` — that program's own words: "human
  interpretation of stated design, the weaker class, marked as
  such". So the strong half was a width and the weak half was the
  name. Only the width reached the key.

- **What was read this session.** The compiler's own DWARF, out of
  the pinned anchor binaries, with pyelftools: for each handler
  symbol, the `DW_TAG_subprogram` DIE, then each
  `DW_TAG_formal_parameter` under it, then the `DW_AT_type` chain
  followed through typedef / pointer / const / struct and rendered
  as the C spelling. This is the same class of fact as the bytes:
  it was emitted by the same compile that produced the bytes the
  arch-unit was carved from.

- **The load-bearing check that the DIE is the right function.**
  `interp_cpython.json`'s `handler_arch_units.anchor.long_add`
  records `load_address 0x0000000000170a1b`. The DWARF subprogram
  DIE this session read carries `DW_AT_low_pc 0x170a1b`. Same
  address, so the type read is the type of the function whose bytes
  the unit is, not a same-named function somewhere else.

- **A second check, because the proof used a different build.**
  The carve and the z3 proof were taken from the SHIP build
  (`interp_fastpath.json`'s boundary address `1373f4` sits inside
  ship `long_add` at `0x137370`), while the typed key above is read
  from the ANCHOR build. So the same symbol's DWARF was read out of
  the ship binary as well and compared, rather than assuming the
  declared type survives the change of optimisation level:

  ```
  {
   "unit": "cpython/long_add",
   "binary": "/persist/cpython_ship/python",
   "compilation_unit": "Objects/longobject.c",
   "dwarf_low_pc": null,
   "formal_parameters": [
    {"param_name": "a", "dwarf_type": "PyLongObject*", "byte_size": 8},
    {"param_name": "b", "dwarf_type": "PyLongObject*", "byte_size": 8}
   ],
   "typed_key_at_this_build": "PyLongObject*,PyLongObject*",
   "typed_key_at_anchor_build": "PyLongObject*,PyLongObject*",
   "agrees": true
  }
  ```

  Stated honestly: the ship DIE carries no `DW_AT_low_pc`, so the
  address identity check that succeeded at the anchor build does NOT
  succeed here — what agrees at the ship build is the declared
  parameter type and the compilation unit, nothing more.

- **Where the read had to refuse.** Three php records —
  `ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER` and its two LONG
  variants. The DIEs exist in `Zend/zend_execute.c` and carry ZERO
  formal parameters and no `DW_AT_low_pc`. That is not a tooling
  failure, it is the measured fact: php's specialized executor
  handlers do not receive their operands as parameters at all, they
  reach them through the `execute_data` frame. A two-operand typed
  key is therefore not expressible for them from parameter types,
  and the field is null with the refusal named. Round 4 had written
  `"ptr64,ptr64"` on all three; that key had no measured basis, so
  removing it strengthens the record.

- **One disagreement, stated rather than smoothed.**
  `ruby/rb_big_plus`. Round 4's prose read "mixed:
  typed-pointer(RBignum*) + tagged-value(Fixnum)" and its machine
  field read `ptr64,tagged64`. The anchor build's DWARF declares
  BOTH parameters as `VALUE` (bignum.c, 8 bytes each). Both readings
  are true of different things: the DECLARED type is one single type
  for both operands; the REPRESENTATION the handler discriminates at
  run time inside that one declared type is Fixnum-tagged on one
  side and an RBignum object pointer on the other. The machine field
  now carries the declared type, because that is what DWARF
  measures; the run-time discrimination stays in the representation
  field, where it belongs, and is not passed off as a type key.

- **One evidence class raised.** `php/add_function`. Round 4
  recorded zval* as "human interpretation of stated design, PHP's
  zval ABI, not DWARF-verified this session". It is DWARF-verified
  now: `Zend/zend_operators.c` declares
  `add_function(zval *result, zval *op1, zval *op2)` returning
  `int`. That signature has an out-parameter first, so which
  parameters are the operands is a decision — the artifact states
  the rule it used, and also records that the rule is NOT
  load-bearing here, because all three parameters carry one and the
  same type and the key is the same either way.

- **The proof was re-run, not copied.** The z3 bounded and unbounded
  checks were executed again by the new builder rather than
  restating round 4's verdict.

---

## The old/new record diff, verbatim

The proved record, `cpython/long_add`. Old, changed field only
(from `proposal_representation_dimension.json`):

```
{
 "type_pair_read": "ptr64,ptr64"
}
```

New, changed and added fields only (from
`proposal_representation_dimension2.json`):

```
{
 "type_pair_read": "PyLongObject*,PyLongObject*",
 "type_pair_read_status": "READ",
 "type_pair_read_previous": "ptr64,ptr64",
 "type_pair_read_width": "ptr64,ptr64",
 "type_pair_read_evidence_class": "forced by construction -- the compiler's own DWARF DW_AT_type chain on the handler's formal parameters, emitted by the same compile that produced the bytes the arch-unit was carved from  (and the key does not depend on the operand selection rule at all: every parameter of this subprogram carries one and the same type)",
 "dwarf_type_read": {
  "binary": "/persist/cpython_anchor/python",
  "build": "cpython v3.14.7 anchor build (-O0 -g -fwrapv), per interp_cpython.json meta.builds.anchor",
  "compilation_unit": "Objects/longobject.c",
  "dwarf_low_pc": "0x170a1b",
  "return_type": "PyLongObject*",
  "formal_parameters": [
   {
    "param_name": "a",
    "dwarf_type": "PyLongObject*",
    "byte_size": 8
   },
   {
    "param_name": "b",
    "dwarf_type": "PyLongObject*",
    "byte_size": 8
   }
  ],
  "operand_selection_rule": "the first two formal parameters are the operands.",
  "key_invariant_under_operand_choice": true,
  "byte_sizes": [
   8,
   8
  ]
 }
}
```

The re-run proof block now carried on that same record:

```
{
 "rerun_by": "build_proposal_representation_dimension2.py (not copied from round 4 -- the checks were executed again)",
 "z3_version": "5.1.0",
 "bounded_domain_check": "unsat",
 "unbounded_check": "unsat",
 "verdict": "PROVED"
}
```

The width `ptr64,ptr64` is not deleted. It is true, and it is kept
under `type_pair_read_width` with its own evidence class. What
changed is that it is no longer the KEY, because a bare width is not
a type.

---

## Per-handler key table, with the evidence class of each key

Pasted from the builder's own run (`status`, `unit`, round-4 value,
round-5 value):

```
  READ           ruby/vm_opt_plus             'opaque_VALUE_dispatch' -> 'VALUE,VALUE'
  READ           ruby/rb_fix_plus             'tagged64' -> 'VALUE,VALUE'
  READ           ruby/rb_int_plus             'tagged64' -> 'VALUE,VALUE'
  READ           ruby/rb_big_plus             'ptr64,tagged64' -> 'VALUE,VALUE'
  READ           php/add_function             'ptr64,ptr64' -> 'zval*,zval*'
  REFUSED        php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER 'ptr64,ptr64' -> None
  REFUSED        php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER 'ptr64,ptr64' -> None
  REFUSED        php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER 'ptr64,ptr64' -> None
  READ           cpython/long_add             'ptr64,ptr64' -> 'PyLongObject*,PyLongObject*'
```

| unit | typed key | DWARF site | evidence class of the key |
|---|---|---|---|
| cpython/long_add | `PyLongObject*,PyLongObject*` | Objects/longobject.c, low_pc 0x170a1b, anchor build | forced by construction (DWARF DW_AT_type chain, at an address identical to the carved unit's recorded load address) |
| ruby/vm_opt_plus | `VALUE,VALUE` | vm.c, low_pc 0x25aa43, anchor build | forced by construction (DWARF DW_AT_type chain) |
| ruby/rb_fix_plus | `VALUE,VALUE` | numeric.c, low_pc 0xfedb1, anchor build | forced by construction (DWARF DW_AT_type chain) |
| ruby/rb_int_plus | `VALUE,VALUE` | numeric.c, low_pc 0xfedda, anchor build | forced by construction (DWARF DW_AT_type chain) |
| ruby/rb_big_plus | `VALUE,VALUE` | bignum.c, low_pc 0x3cfaa9, anchor build | forced by construction (DWARF DW_AT_type chain); the round-4 representation reading disagrees with it and the disagreement is recorded on the record, not resolved by preference |
| php/add_function | `zval*,zval*` | Zend/zend_operators.c, low_pc 0x7c4001, anchor build | forced by construction (DWARF DW_AT_type chain); the operand-selection rule is not load-bearing — all three parameters carry one type |
| php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER | none | Zend/zend_execute.c, no low_pc, zero formal parameters | refusal, machine-grounded — the read ran, the DIE was found, and the absence of typed operand parameters is itself the measured fact |
| php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER | none | as above | as above |
| php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER | none | as above | as above |

Breakdown behind the "6 read, 3 refused" count, so the count is not
taken on trust: cpython 1 read + ruby 4 read + php 1 read = 6 read;
php 3 refused = 3. 6 + 3 = 9, which is the handler count of the
round-4 artifact.

**The brief's "java's 2 units" — checked against disk, and refused.**
The brief named "java's 2 units, ruby's 4, php's 4" as the other
eight. The round-4 artifact's nine records are ruby 4, php 4,
cpython 1 — **zero java**. Java's two units live in
`interp_jvm.json` as ids `u1` and `u2`, and they were never handler
records in this proposal. No DWARF key is possible for them at all:
they are nmethods, machine code the JVM's c2 compiler emitted into
its own memory at run time and that the probe dumped from a live
process. There is no ELF file, so there is no DWARF. The type
evidence `interp_jvm.json` does hold for them is the JVM's printed
parameter comments, recorded there as "the tool's own testimony" — a
weaker class, and nothing this session did upgrades it. No java row
was added and no java type was guessed. This refusal is carried in
the new artifact under `java_units_not_included_and_why`.

---

## Commands and their output

Verified: the DWARF read ran, in the sandbox container, over the
pinned anchor binaries.

```
$ podman exec -e DWARF_TYPED_KEY_OUT=/persist/dwarf_typed_key.json sandbox-runner \
    bash -lc 'cd PseudoCoupHQ/Research/op_pipeline && timeout 900 python3 dwarf_typed_key.py'
wrote /persist/dwarf_typed_key.json
cpython  long_add                                             READ     PyLongObject*,PyLongObject*
ruby     vm_opt_plus                                          READ     VALUE,VALUE
ruby     rb_fix_plus                                          READ     VALUE,VALUE
ruby     rb_int_plus                                          READ     VALUE,VALUE
ruby     rb_big_plus                                          READ     VALUE,VALUE
php      add_function                                         READ     zval*,zval*
php      ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER              REFUSED  None
php      ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER         REFUSED  None
php      ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER REFUSED  None
summary: {'handlers_considered': 9, 'keys_read': 6, 'refused': 3}
```

Note on where that ran: `PseudoCoupHQ` is mounted into the
container READ-ONLY in practice (the first run stopped with
`OSError: [Errno 30] Read-only file system`), so the script writes to
`/persist` when `DWARF_TYPED_KEY_OUT` says so and the result is copied
to the repo with `podman cp`. The mounts.conf line asks for `:rw`; the
running container does not honour it. Recorded as a fact about this
machine, not fixed here.

Verified: the proposal was regenerated and the tally re-run.

```
$ /tmp/reconnect_venv/bin/python3 build_proposal_representation_dimension2.py
wrote PRIVATE/PseudoCoupHQ/Research/op_pipeline/proposal_representation_dimension2.json
proof re-run: {'rerun_by': 'build_proposal_representation_dimension2.py (not copied from round 4 -- the checks were executed again)', 'z3_version': '5.1.0', 'bounded_domain_check': 'unsat', 'unbounded_check': 'unsat', 'verdict': 'PROVED'}
summary: {
 "handlers_considered": 9,
 "typed_keys_read_from_dwarf": 6,
 "typed_keys_refused": 3,
 "handlers_with_full_carve_and_proof": 1,
 "handlers_refused_honestly": 8,
 "proved_computation_matches": 1,
 "machine_fields_changed": 9
}
```

Verified: the spelling guard passes on both new artifacts.

```
$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py proposal_representation_dimension2.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS proposal_representation_dimension2.json -- no operator token in any key, grouping, pairing or row structure
exit=0
$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py dwarf_typed_key.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS dwarf_typed_key.json -- no operator token in any key, grouping, pairing or row structure
exit=0
```

**The guard caught this session's own work once, and the fix was the
mechanism, not the threshold.** The first build FAILED with 12
findings:

```
FAIL proposal_representation_dimension2.json -- 12 spelling-keyed place(s)
     $.diff_against_round_4[0].new
         dict key is the operator token 'new'
     ...
     $.handlers[5].dwarf_type_read.return_type
         operator token 'void' on a structure field -- this is a grouping/row key, not a per-unit label
```

Both were repaired at the source, and neither by touching the guard:

- the diff rows were keyed `old` / `new`, and `new` is a C++
  operator token in the inventory. The fields are now
  `round_4_value` / `round_5_value`, which is also the more accurate
  naming.
- `"return_type": "void"` was **my program inventing a word DWARF
  did not say**: the three php handler DIEs carry no `DW_AT_type`
  attribute at all, and the renderer was turning that absence into
  the string `void`. The reader now records the absence as `null`
  plus `return_type_absent_in_dwarf: true`. This is the honest fix
  and it is also what removed the finding.

Verified: zero regressions — no existing artifact was modified.

```
$ git status --porcelain Research/op_pipeline/
 M Research/op_pipeline/dwarf_typed_key.json
 M Research/op_pipeline/proposal_representation_dimension2.json
$ git diff HEAD --stat -- Research/op_pipeline/proposal_representation_dimension.json
(no output)
$ md5sum Research/op_pipeline/proposal_representation_dimension.json
1c222af06f3eb5b8fb32b75c6396901e  Research/op_pipeline/proposal_representation_dimension.json
$ git show HEAD:Research/op_pipeline/proposal_representation_dimension.json | md5sum
1c222af06f3eb5b8fb32b75c6396901e  -
```

The two files shown as modified are this session's OWN new files,
already commit-pushed once by the daemon at an earlier state and then
rewritten. The round-4 artifact is byte-identical to its committed
form. `dominant_table24.json` and `dom_ops22.json` are not opened by
any program written here — table membership stays the owner's ratification.

---

## Complete file inventory

Created this session (all new; nothing existing was edited):

- `PRIVATE/PseudoCoupHQ/Research/op_pipeline/dwarf_typed_key.py`
  — the DWARF parameter-type reader, with its refusal policy in the
  module docstring. 16258 bytes.
- `PRIVATE/PseudoCoupHQ/Research/op_pipeline/dwarf_typed_key.json`
  — its output: nine per-handler records, the cross-check at the ship
  build, the tally. 12204 bytes.
- `PRIVATE/PseudoCoupHQ/Research/op_pipeline/build_proposal_representation_dimension2.py`
  — the regenerator. 15124 bytes.
- `PRIVATE/PseudoCoupHQ/Research/op_pipeline/proposal_representation_dimension2.json`
  — **the artifact for the owner's ratification.** 48669 bytes.
- `PRIVATE/PseudoCoupHQ/DevComms/log_111_task24_typed_key_regen.md`
  — this log.
- A dated entry appended to
  `PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/PROGRESS.md`.

Inside the sandbox container, not in any repo:
`/persist/dwarf_typed_key.json` (the write target, copied out).

Byte counts pasted from the run that produced them:

```
$ wc -c dwarf_typed_key.py dwarf_typed_key.json build_proposal_representation_dimension2.py proposal_representation_dimension2.json
16258 dwarf_typed_key.py
12204 dwarf_typed_key.json
15124 build_proposal_representation_dimension2.py
48669 proposal_representation_dimension2.json
92255 total
```

Read but never written: `proposal_representation_dimension.json`,
`interp_fastpath.json`, `interp_cpython.json`, `interp_jvm.json`,
`interp_relations.json`, `fix_cpython_type_key.py`,
`check_no_spelling_keys.py`, and the three pinned binaries
`/persist/cpython_anchor/python`, `/persist/ruby_anchor/ruby`,
`/persist/php_anchor/sapi/cli/php` (plus `/persist/cpython_ship/python`
for the cross-check).

---

## What this does and does not gate

- It DOES put a real type in the machine field of every record where
  a type is measurable, with the field and the prose saying the same
  thing, so option B and option B-with-A can be ratified from a
  record that means what it reads.
- It does NOT change any table membership, and it does not add the
  ruby/php carves — those are task 27. The eight non-cpython records
  remain honest refusals at the ARRIVAL/COMPUTATION carve, exactly as
  round 4 left them; what changed is their type key, not their
  verdict.
