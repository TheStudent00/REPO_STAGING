# log_107 -- TASK 21: canonicalize the interpreter units (registers are NOT the issue)

**Role:** Claude Code implementer, TASK 21 of
`log_103_claude_code_task_briefs_round4.md`. Evidence class stated per
claim below, per the evidence doctrine. No sub-agents used, per this
task's own instruction -- every artifact below was built and run
directly in this session.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

## walkthrough (plain words first)

Read AgentMemory.md (the three 2026-08-31 rulings: branch-to-
alternate-computation, ARRIVAL/COMPUTATION BOUNDARY IS LINEAGE
CONFLUENCE, BANKING IS A MESSAGE NOT A COMMIT), the LLM communication
protocol, log_103's own TASK 21 brief, log_083's STANDING REQUIREMENTS
header, log_104 (the fixed block_cutter.py + re-extracted cpython
slices), and log_106 (Task 19's representation-dimension proposal:
cpython's fast path carved and PROVED, the other 8 handlers UNDECIDED
for want of a re-extracted slice).

The question this task answers: canonicalization (the newest
generation, canon9_behaviour_check.Sim9's z3 checker) has never been
RUN on an interpreter or JIT unit -- only on compiled units. Task 19
already established that CPython's fast-path arguments arrive plain
(the arrival prefix is representation, not computation) and already
proved the one add instruction equal to c's add, but that proof was
an AD HOC script, not a run of the pipeline's own newest checker. This
task runs the real checker, for real, on every interpreter/JIT unit
where a computation part can be isolated, and refuses honestly, per
unit, where it cannot.

**Result, in one line:** cpython's fast-path add and java's `+` unit
both independently re-proved PROVED_EQUAL through Sim9. Java's `/`
unit and all 8 ruby/php handlers are honest refusals, each with a
real mechanical reason reproduced verbatim below -- none forced, none
guessed.

## instances

### instance 1 -- cpython `long_add` fast path, PROVED_EQUAL

New file: `op_pipeline/canon_interp_cpython.py`. It takes the single
computation instruction interp_fastpath.json's own carve already
isolated (index 8 of 48, address `0x1373f4`):

```
lea    (%rax,%rdx,1),%rdi
```

(`%rax` holds medium_value(b), `%rdx` holds medium_value(a) -- read
directly off interp_fastpath.json's own instruction comments, forced
by construction: which arrival-prefix line writes which family, not
asserted). One relocating `mov %rdi,%rax` is appended so
`Sim.answer_value` (which only ever reads the `rax` family) can see
the result -- stated in the file's own header as a mechanical
relocation, not a new computation.

Gated, through `canon9_behaviour_check.Sim9` (imported by reference,
unmodified), against the c/i64,i64/+ class's own newest canonical
text, read live off `canon29_units_c.json` (unit `c/op_109`):

```
mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret
```

Real run:

```
$ /tmp/reconnect_venv/bin/python3 canon_interp_cpython.py
wrote PseudoCoupHQ/Research/op_pipeline/canon_interp_units_cpython.json
verdict: PROVED_EQUAL
canonical_text: mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret
```

Evidence class: forced by construction (the z3 unsat result, over a
register binding derived from interp_fastpath.json's own recorded
instruction semantics) -- an INDEPENDENT re-run of the SAME result
log_106's ad hoc proof already found (cited there, not silently
repeated as a new finding here). Output:
`op_pipeline/canon_interp_units_cpython.json`.

### instance 2 -- java, 2 units

New file: `op_pipeline/canon_interp_java.py`.

**Unit 1 (`+`, i32,i32).** Already carved by `jvm_canon.py` in a prior
session (`add_java.json`'s own `java_canonical_form`:
`lea (%rdi,%rsi,1),%eax; ret`). Independently re-gated through Sim9
against the c/i32,i32/+ class's own newest canonical text:

```
$ /tmp/reconnect_venv/bin/python3 canon_interp_java.py
unit 1 verdict: PROVED_EQUAL mov %rdi,%rax; and $-1,%eax; mov %rsi,%r10; and $-1,%r10d; add %r10d,%eax; ret
```

**Unit 2 (`/`, i32,i32).** Attempted the SAME straight-line carve
(`jvm_canon.py`'s own `strip()`, imported unmodified) on
`interp_jvm.json`'s second arity-2 (int32,int32)->int32 unit (selected
by machine fact -- the one `pick_unit()`'s own smallest-bytes rule did
NOT already pick for unit 1 -- never by the operator label). Real
refusal, reproduced verbatim:

```
unit 2 verdict: REFUSED honest refusal, not forced -- jvm_canon.py's
own strip() (imported unmodified) rejects unit 2's residual core with
rule CORE: the residual core branches; this file handles one straight
run only (at 'je 0x7f99346a9b46'). The core branches (an INT_MIN/-1
division-overflow guard) and strip() only handles one straight run;
carving a branching JVM unit needs a new multi-block stripper, out of
this task's scope.
```

Reading: java's JIT-compiled integer division inlines the x86-64
INT_MIN/-1 overflow guard (`idiv` traps on that one input pair) as a
real conditional branch in the method body -- not furniture,
computation with a guard, the same shape the compiled table's guard
families already carry, but `jvm_canon.py`'s existing stripper only
ever handled a single straight run. Evidence class: forced by
construction (the stripper's own exception, re-run this session, not
assumed from Task 19's prose). Output:
`op_pipeline/canon_interp_units_java.json`.

### instance 3 -- ruby (4) + php (4), all 8 honest refusals

New file: `op_pipeline/canon_interp_units_ruby_php.py`. Per this
task's own instruction, the lineage-confluence carve was attempted
with the fixed cutter (`block_cutter.py`, Task 20, imported
unmodified) first. Before attempting, this session re-checked --
fresh, not carried over from log_106's prose -- what instruction
slices exist on disk:

```
$ ls op_units_*.json
op_units_asg_c.json  op_units_asg_cpp.json  op_units_asg_go.json
op_units_asg_rust.json  op_units_asg_swift.json  op_units_c.json
op_units_cpp.json  op_units_cpython.json  op_units_cpython2.json
op_units_cpython2_reextracted.json  op_units_cpython_reextracted.json
op_units_csharp.json  op_units_dart.json  op_units_go.json
op_units_java.json  op_units_java2.json  op_units_javascript.json
op_units_rust.json  op_units_swift.json
```

No `op_units_ruby.json`, no `op_units_php.json`. `block_cutter.py`
(and the `canon2.cut_blocks` machinery it wraps) both require an
INPUT to cut -- a full disassembled instruction stream with addresses
and successors, the shape only `op_units_cpython*.json` and
`op_units_java*.json` carry. The only recorded evidence for the 8
ruby/php handlers is `interp_relations.json`'s own
`representation_evidence` field, a short prose excerpt (example, real
value, `rb_fix_plus`): `"ship excerpt: `and esi,0x1` / `test al,0x7`
-- the argument register is TAG-TESTED before use ..."` -- named
instructions, not a full slice. The fixed cutter fixes DEFECTS in how
an EXISTING slice is walked; it cannot manufacture a slice that was
never extracted. This is the SAME finding Task 19 already made
(log_106, Instance D), re-verified this session rather than assumed
carried over.

Real run:

```
$ /tmp/reconnect_venv/bin/python3 canon_interp_units_ruby_php.py
wrote .../canon_interp_units_ruby_php.json
ruby/vm_opt_plus REFUSED
ruby/rb_fix_plus REFUSED
ruby/rb_int_plus REFUSED
ruby/rb_big_plus REFUSED
php/add_function REFUSED
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER REFUSED
php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER REFUSED
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER REFUSED
```

`provenance_is_weaker: true` is carried on every record in this file,
matching the round-3 fix. Evidence class: tool testimony (a fresh
directory listing, reproducible).

## gates

```
$ python3 check_no_spelling_keys.py canon_interp_units_cpython.json canon_interp_units_java.json canon_interp_units_ruby_php.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS canon_interp_units_cpython.json -- no operator token in any key, grouping, pairing or row structure
PASS canon_interp_units_java.json -- no operator token in any key, grouping, pairing or row structure
PASS canon_interp_units_ruby_php.json -- no operator token in any key, grouping, pairing or row structure
exit=0
```

## numbers

- Interpreter/JIT units considered this task: **11** = cpython 1
  (long_add fast path) + java 2 + ruby 4 + php 4.
- PROVED_EQUAL, independently re-run through the newest checker
  (Sim9): **2** (cpython/long_add_fastpath, java unit 1).
- Honest refusals, each with a real mechanical reason: **9** (java
  unit 2: stripper rejects a branching core; ruby 4 + php 4: no
  instruction slice exists to carve).
- Zero regressions, computed programmatically:

```
$ python3 -c "
import json
langs=['c','cpp','go','rust','swift']
total=0
for lang in langs:
    d=json.load(open('canon29_units_%s.json'%lang))
    for n,u in d['units'].items():
        if u.get('status')=='converged':
            total+=1
print('converged total:', total)
"
converged total: 1561
```
1,561 -- unchanged from round 4's own count (log_105). `git diff
--stat` empty (before and after) on every pre-existing file this task
read: `canon29_units_c.json`, `canon29_units_cpp.json`,
`canon29_units_go.json`, `canon29_units_rust.json`,
`canon29_units_swift.json`, `interp_fastpath.json`, `add_java.json`,
`interp_relations.json`, `jvm_canon.py`, `block_cutter.py`,
`canon9_behaviour_check.py`, `canon8_behaviour_check.py`, `canon.py`,
`canon2.py`. No table (`dominant_table24.json`, `dom_ops22.json`,
`guards5.json`, `exception_families3.json`) was opened or changed --
this task canonicalizes units, it does not touch membership.

## file inventory (all new; nothing edited in any prior artifact)

- `op_pipeline/canon_interp_cpython.py` -- generator, instance 1.
- `op_pipeline/canon_interp_units_cpython.json` -- output, instance 1.
- `op_pipeline/canon_interp_java.py` -- generator, instance 2 (both
  java units).
- `op_pipeline/canon_interp_units_java.json` -- output, instance 2.
- `op_pipeline/canon_interp_units_ruby_php.py` -- generator, instance
  3 (all 8 ruby/php handlers).
- `op_pipeline/canon_interp_units_ruby_php.json` -- output, instance 3.
- `PseudoCoupHQ/DevComms/log_107_task21_interp_
  canonicalization.md` -- this report.
- Dated entry appended to `PseudoCoupHQ/Planning/
  node_0_3_research/node_0_3_5_compiler_graph/PROGRESS.md` (single
  `# PROGRESS` heading, unchanged).

## what was refused, and why (restated, not buried)

- Java unit 2 (`/`, i32,i32): the existing straight-line stripper
  (`jvm_canon.py`) rejects its core because it branches (INT_MIN/-1
  division-overflow guard). Building a multi-block JVM stripper was
  out of this task's scope.
- All 4 ruby handlers and all 4 php handlers: no full instruction
  slice exists on disk to hand the (fixed) cutter -- verified fresh
  this session by listing every `op_units_*.json` file, not assumed
  from a prior log. This is the same gap Task 19 already found; the
  cutter fix (Task 20) does not close it because it fixes how an
  EXISTING slice is walked, not the absence of one.

Commit state: the repo-daemon auto-commits every artifact listed
above as it is written (`git log --oneline` shows `90dfbe7` and
`46b7749` as auto-commits already covering the cpython and java
artifacts by the time this log was drafted) -- stated for posterity,
per BANKING IS A MESSAGE, NOT A COMMIT.
