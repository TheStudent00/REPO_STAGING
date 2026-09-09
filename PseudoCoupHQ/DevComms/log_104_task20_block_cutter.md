# log 104 -- Task 20: block cutter fixes + slice extractor fix

Date: 2026-09-01. Protocol v2 (walkthrough, then instances, then
numbers, then file inventory).

## WALKTHROUGH

Task 20 named three defects, all found while carving CPython's
`long_add` fast path for `interp_fastpath.json`:

1. **Cutter defect A** -- `canon2.cut_blocks()` derives a block's
   successors from its NOMINAL LAST instruction index only. Real ship
   binaries carry compiler alignment padding (nopl/nopw) after a
   ret/jmp that lands mid-function, so the true control-transfer
   instruction sits inside the nominal block rather than at its end,
   and the naive rule invents a fallthrough edge into whatever block
   happens to follow in memory.
2. **Cutter defect B** -- a bare `<symbol>` jump target (no
   `+0xNN`) is resolved by `canon2.find_jump_target_offset()` as
   offset 0 INTO THE CURRENT UNIT. Right for a self-contained probe
   (the only symbol its own disassembly can name is itself); wrong
   for a real binary slice that tail-jumps to an OTHER, external,
   named function (`long_add`'s `jmp 131e70 <x_add>`).
3. **Extractor defect** -- the stored `long_add` slice
   (`op_units_cpython.json`, `probes["1"]["ship"]["mnem"]`) carries an
   EMPTY-STRING entry at index 88: the trailing displacement byte of
   the preceding 8-byte `lea` instruction, printed by whatever
   extractor produced this slice as its OWN zero-content "instruction"
   instead of being folded back into the `lea` it belongs to.

Fix approach, per the wrapper precedent (a NEW module wraps the
shared machinery; the shared module is not edited):

- `block_cutter.py` -- wraps `canon2` (imports `canon.parse`,
  `canon.JUMP`; reuses `canon2.real_addresses`). Computes reachability
  at INSTRUCTION granularity (`classify()` + `walk_reachable()`)
  instead of block granularity, so a ret/jmp/trap's successor set is
  always read off ITS OWN index, never inherited from a block's
  nominal last index (fixes defect A). `find_jump_target_offset_checked()`
  takes the unit's own symbol name and only resolves a bare `<sym>`
  as offset 0 when `sym == own_symbol`; any other name is recorded as
  an `external_exits` entry with no in-unit successor (fixes defect
  B). `canon2.py` itself is untouched (verified: `git diff` on it is
  empty below).
- `slice_extractor_fix.py` -- a replacement extractor to the same
  contract as `lane_gen.py`'s `extract()` (address-stripped
  byte/mnem columns from raw objdump text), plus the merge rule: a
  continuation line (bytes present, instruction text empty) is folded
  into the PRECEDING instruction's byte span, never emitted as its
  own entry. Also offers `repair_stored_slice()` for slices that were
  already extracted with the bug and have no surviving raw objdump
  text -- it re-disassembles the affected byte span for real via
  `objdump` rather than hand-typing the corrected mnemonic.
- `reextract_long_add.py` -- applies the repair to the two stored
  files that carry the `long_add` slice and writes NEW re-extracted
  files (originals untouched, per "defective artifacts stay on disk
  as records").
- `test_block_cutter_long_add.py` -- the regression test. It targets
  the ORIGINAL, still-buggy `op_units_cpython.json` slice ON PURPOSE:
  `interp_fastpath.json`'s own recorded 48-instruction baseline was
  itself carved from that same buggy extraction (its own instruction
  at address `0x1374d8` is `{"bytes": "00", "mnem": ""}` -- verified
  below), so reproducing that EXACT baseline means walking the SAME
  bytes it was recorded against. The cutter fix (defects A/B) and the
  extractor fix (defect 3) are independent lines of work and are
  tested independently; item 3's own regression is the diff in
  Instance 2 below, run over the NEW re-extracted files.

**Provenance note, honestly stated:** no script that WROTE
`op_units_cpython.json` (or `interp_fastpath.py`, named in
`interp_fastpath.json`'s own `meta.generator` field) exists on this
disk. Searched with `grep -rl "op_units_cpython.json" *.py` across
every `.py` file in `op_pipeline/`: only READERS were found
(`fold_interp_cpython.py`, `interp_relations_build.py`,
`interp_feeder.py`, `fix_cpython_type_key.py`), no writer. This is
recorded as a fact, not papered over: `slice_extractor_fix.py` is
built as the REPLACEMENT any future real-binary extraction should
call, to the same interface `lane_gen.py`'s `extract()` already uses
for compiled probes, not as a patch to a named-but-missing script.

## INSTANCES

### Instance 1 -- regression test, run for real

```
$ /tmp/reconnect_venv/bin/python3 test_block_cutter_long_add.py
instruction_count: got=48 expected=48
address_ranges:
  0x1373d8 .. 0x137479
  0x1374c0 .. 0x1374db
  0x1374e0 .. 0x1374e9
expected address_ranges:
  0x1373d8 .. 0x137479
  0x1374c0 .. 0x1374db
  0x1374e0 .. 0x1374e9
external_exits: 1
   {'at_index': 92, 'instruction': 'jmp 131fe0 <_PyLong_FromMedium>', 'target_symbol': '131fe0 <_PyLong_FromMedium>'}
unresolved_exits: 0
PASS: walk over the fixed cutter matches interp_fastpath.json exactly (48 instructions, 3 address ranges).
```

Exit code 0. The one `external_exits` entry is defect B's own fix
firing for real: `long_add`'s tail jump to `_PyLong_FromMedium` is
recognized as a NAMED OTHER FUNCTION and excluded from the walk's
successor set, rather than being misresolved as offset 0 back into
`long_add`.

`canon2.py` unmodified, verified:

```
$ git diff --stat -- canon2.py
```

(empty output -- no changes)

### Instance 2 -- extractor fix, diff at the defect site, run for real

```
$ /tmp/reconnect_venv/bin/python3 reextract_long_add.py
=== defect site diff (op_units_cpython.json, probes[1].ship.mnem) ===
index 87 before: 'lea    0x36f0(%rax,%rdi,1),%rax'
index 88 before: ''  (stray tail byte, empty mnemonic)
index 89 before: 'jmp    137474 <long_add+0x104>'
---
index 87 after:  'lea 0x36f0(%rax,%rdi,1),%rax'
index 88 after:  'jmp    137474 <long_add+0x104>'  (was index 89 before the merge)
total instructions before: 94, after: 93
wrote PseudoCoupHQ/Research/op_pipeline/op_units_cpython_reextracted.json
```

Same run against the sibling file:

```
$ /tmp/reconnect_venv/bin/python3 reextract_long_add.py op_units_cpython2.json op_units_cpython2_reextracted.json
... (identical diff at the same site) ...
wrote PseudoCoupHQ/Research/op_pipeline/op_units_cpython2_reextracted.json
```

The replacement mnemonic (`lea 0x36f0(%rax,%rdi,1),%rax`) is not
hand-typed: `repair_stored_slice()` re-disassembles the recorded
8-byte encoding (`48 8d 84 38 f0 36 00 00`, confirmed present intact
at flat-byte offset 353 of the slice's own `bytes` array) via a real
`objdump -D -b binary` call and reads the mnemonic back off that
output.

### Instance 3 -- verbatim confirmation that interp_fastpath.json's
own baseline still carries the pre-fix split (why the regression test
in Instance 1 targets the ORIGINAL slice, not the re-extracted one)

```
$ python3 -c "
import json
d = json.load(open('interp_fastpath.json'))
for x in d['carve']['instructions']:
    if x['addr'] == '1374d8':
        print(x)
"
{'addr': '1374d8', 'bytes': '00', 'mnem': ''}
```

## NUMBERS

- Affected stored slices, computed by scanning EVERY probe/side in
  both files for an empty-string `mnem` entry (not assumed, computed):
  `op_units_cpython.json` -- 1 probe (`"1"`, side `ship`), 1 empty
  entry (index 88). `op_units_cpython2.json` -- 1 probe (`"1"`, side
  `ship`), 1 empty entry (index 88), same site, same bytes. Both
  files have exactly 1 probe total, so "1 of 1" in each file, computed
  by the loop in the transcript above (not eyeballed).
- Regression test: 48/48 instructions, 3/3 address ranges, byte-exact
  against `interp_fastpath.json`'s `carve.instructions` /
  `carve.address_ranges`. 1 external exit correctly excluded (defect
  B), 0 unresolved exits.
- Extractor fix: 94 -> 93 instructions in both re-extracted files (one
  spurious entry removed per file, 2 total).

## DOWNSTREAM ARTIFACTS STILL BUILT ON PRE-FIX SLICES

Named by grepping for consumers of `op_units_cpython.json` /
`op_units_cpython2.json` across `.py` files in `op_pipeline/`:

- `interp_relations.json` (via `interp_relations_build.py`, which
  reads `op_units_cpython2.json`) -- built on the PRE-FIX slice.
- `interp_fastpath.json` itself -- its `carve.instructions` was
  carved from the PRE-FIX slice (Instance 3); the 48-instruction
  baseline this task's regression test targets is therefore ALSO
  pre-fix by construction, and stays that way on purpose (see
  walkthrough).
- `interp_cpython.json`, `sem_anchored_cpython2.json`,
  `sem_anchored_spill_cpython2.json`,
  `sem_anchored_spill_cpython_fixed.json`, and anything
  `fold_interp_cpython.py` / `interp_feeder.py` /
  `fix_cpython_type_key.py` produced from them -- all read the
  PRE-FIX files (`op_units_cpython.json` / `...2.json`), not the new
  `..._reextracted.json` files. NONE of these were regenerated by
  this task -- regenerating them was out of this task's scope
  (block cutter + extractor fix only) and is named here as the open
  remainder gating future branching work on ruby/php/jvm slices, per
  the task's own closing instruction.

## FILE INVENTORY (all new; nothing edited in canon2.py or any prior
## artifact)

- `op_pipeline/block_cutter.py` -- the cutter wrapper (defects A, B).
- `op_pipeline/slice_extractor_fix.py` -- the extractor fix
  (defect 3), general `parse_objdump_text()` plus
  `repair_stored_slice()` for already-extracted slices.
- `op_pipeline/reextract_long_add.py` -- driver: applies the repair
  to a named file, asserts the expected before-state, writes a new
  file, prints the defect-site diff.
- `op_pipeline/test_block_cutter_long_add.py` -- the regression test
  (Instance 1).
- `op_pipeline/op_units_cpython_reextracted.json` -- re-extracted
  output (93 instructions, defect-free).
- `op_pipeline/op_units_cpython2_reextracted.json` -- re-extracted
  output (93 instructions, defect-free), sibling file.
- `PseudoCoupHQ/DevComms/log_104_task20_block_cutter.md`
  -- this report.
- Dated entry appended to
  `PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/PROGRESS.md`
  (single `# PROGRESS` heading, unchanged).

No file was deleted or edited among prior artifacts; `op_units_cpython.json`
and `op_units_cpython2.json` are left exactly as found (defective
artifacts stay on disk as records, per standing requirements).

`check_no_spelling_keys.py` was not run against these files: none of
them groups or pairs UNITS (plural) -- `block_cutter.py` walks control
flow inside ONE unit, and the extractor fix operates on ONE unit's own
instruction stream. Stated explicitly in `block_cutter.py`'s own
docstring, per the mechanical-guard requirement.

THE SPELLING BAN, pasted verbatim as required (no sub-agent was used
on this task -- Task 20 was worked directly -- pasted here anyway per
the letter of the requirement, since this line's rule applies to any
report on this line):

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in \"which pairs
get compared\", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as \"same-operator pairs\"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

Evidence class on every claim above: forced by construction (the
regression test output, the diff output, the flat-byte-offset match,
the `git diff` on canon2.py) except the "no writer script exists"
claim, which is the tool's own testimony (a `grep` search of this
disk) -- stated as such, not as proof no such script ever existed
anywhere.
