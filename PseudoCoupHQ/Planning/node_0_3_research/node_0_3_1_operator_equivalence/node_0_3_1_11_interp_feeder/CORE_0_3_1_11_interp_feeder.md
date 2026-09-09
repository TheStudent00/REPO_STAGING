---
id: hq.research.interp_feeder
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: interp_feeder
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_11_interp_feeder/CORE_0_3_1_11_interp_feeder.md
super_node:
    name: operator_equivalence
    path: ../CORE_0_3_1_operator_equivalence.md
sub_nodes:
    - name: feeder_config
      path: node_0_3_1_11_0_feeder_config/CORE_0_3_1_11_0_feeder_config.md
    - name: parse_interp
      path: node_0_3_1_11_1_parse_interp/CORE_0_3_1_11_1_parse_interp.md
    - name: format_canon
      path: node_0_3_1_11_2_format_canon/CORE_0_3_1_11_2_format_canon.md
    - name: invoke_normalizer
      path: node_0_3_1_11_3_invoke_normalizer/CORE_0_3_1_11_3_invoke_normalizer.md
    - name: run_pipeline
      path: node_0_3_1_11_4_run_pipeline/CORE_0_3_1_11_4_run_pipeline.md
    - name: run_jvm
      path: node_0_3_1_11_5_run_jvm/CORE_0_3_1_11_5_run_jvm.md
    - name: target
      path: node_0_3_1_11_6_target/CORE_0_3_1_11_6_target.md
    - name: output
      path: node_0_3_1_11_7_output/CORE_0_3_1_11_7_output.md
---

# CORE 0_3_1_11 — interp_feeder

## metadata

- **id:** hq.research.interp_feeder
- **level:** 3
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [operator_equivalence](../CORE_0_3_1_operator_equivalence.md)

## sub_nodes

- [feeder_config](node_0_3_1_11_0_feeder_config/CORE_0_3_1_11_0_feeder_config.md) — The configuration object of the feeder: which interpreter dump files are read and which directory the op_units-shaped records are written to.
- [parse_interp](node_0_3_1_11_1_parse_interp/CORE_0_3_1_11_1_parse_interp.md) — The reader of one interpreter pilot's dump: `parse_interp_log(path)` loads the JSON an interpreter or JIT pilot wrote (for java, `interp_jvm.json`: per unit an id, a label, the objdump lines and hex bytes of the emitted code, and the operand types the pilot probed).
- [format_canon](node_0_3_1_11_2_format_canon/CORE_0_3_1_11_2_format_canon.md) — The mapping from a pilot's own dump schema onto the op_units record the compiled probes have: `format_jvm(interp_data)` turns each dump unit into a probe record with the operator label, the instruction list (the last tab field of each objdump line), the bytes, and the holder representations of the operands (`int32` → `i32`).
- [invoke_normalizer](node_0_3_1_11_3_invoke_normalizer/CORE_0_3_1_11_3_invoke_normalizer.md) — The hand-off from the feeder's records to the canonical-form stage: the written op_units records are given to the same normalizer the compiled units go through (today `canon40_interp.py`, producing `canon40_interp.json`).
- [run_pipeline](node_0_3_1_11_4_run_pipeline/CORE_0_3_1_11_4_run_pipeline.md) — The lane that runs one interpreted language end to end: parse the pilot's dump, format it to op_units, invoke the normalizer, and leave the canonical records where the gate reads them.
- [run_jvm](node_0_3_1_11_5_run_jvm/CORE_0_3_1_11_5_run_jvm.md) — The java route, the one where the unit does not exist in any binary until run time: the probe method is warmed until HotSpot's C2 tier compiles it, the emitted machine code is dumped, and the method's body is carved as the unit.
- [target](node_0_3_1_11_6_target/CORE_0_3_1_11_6_target.md) — Which build of each interpreter is read, so a unit is attributed to a named binary and not to "php": the instrumented php builds (`Airlock/php-{7.4.33,8.2.13,8.3.0}.tar.gz`), the instrumented ruby 3.3.0 build, the image's cpython and openjdk 25.
- [output](node_0_3_1_11_7_output/CORE_0_3_1_11_7_output.md) — The records the feeder writes and where: per pilot, `canon_interp_units_{java,cpython}.json` and `canon_interp_units_ruby_php.json`; after the normalizer, `canon40_interp.json` (eleven units, ten with bodies), all under `PseudoCoupHQ/Research/op_pipeline/`.

## definition

The retrofit that lets an interpreted or JIT-compiled language enter
the operator-equivalence pipeline at the arch-unit step: it reads
what the interpreter or its JIT itself produced for an operator (a
handler function's body, or the JIT's emitted machine code with its
own dump of what it did) and writes it in the record shape the
compiled probes already have, so everything after
[arch_unit](../node_0_3_1_1_arch_unit/CORE_0_3_1_1_arch_unit.md)
runs unchanged.

Written 2026-08-26 to 2026-09-05 across tasks 12, 17, 21, 27, 32,
34, 94 and 96 (logs 095, 101, 107, 113, 119, 124, 199, 201). Moved
under operator_equivalence 2026-09-06; it was the research node's
sixth co-node.

## 1. Why the interpreted languages need a different step 1 and 2

- A compiled language's probe IS the unit: our wrapper function,
  compiled, carved at its body. There is nothing of ours to compile
  for python, ruby, php or java; the operator's machine code is the
  interpreter's own handler (`ZEND_ADD_LONG_SPEC_…` in php,
  `rb_int_plus` in ruby, `long_add` in cpython) or, for a JIT, code
  the JIT emits at run time (HotSpot C2 for java).
- the owner's ruling 2026-09-04 gives the boundary: the interpreter's OWN
  handler function is the wrapper, so the unit is that function's
  body, read from the symbol table and DWARF. Task 94 re-carved all
  eleven interpreter units to it; every verdict moved from PROVED to
  UNDECIDED and that is a CORRECTION, not a regression, because the
  old proofs rested on a boundary someone chose.
- A handler works through pointers into the interpreter's frame, so
  it is already in the virtual-memory form by default; the compiled
  units are the ones that need wrapping. That observation (the owner,
  2026-09-05) is why the canonical form needed a seventh block kind,
  an ARRIVING ADDRESSABLE AREA, beside the six that hold one value
  each.

## 2. What the feeder is, mechanically

`PseudoCoupHQ/Research/op_pipeline/interp_feeder.py`,
"Translates parsed interpreter/JIT output logs into the schema
expected by the active Z3 normalization pipeline." Its parts are the
sub-nodes, each a function or class of that file:

- [feeder_config](node_0_3_1_11_0_feeder_config/CORE_0_3_1_11_0_feeder_config.md)
  — `FeederConfig`: which dump files to read, where to write.
- [parse_interp](node_0_3_1_11_1_parse_interp/CORE_0_3_1_11_1_parse_interp.md)
  — `parse_interp_log`: read one interpreter pilot's JSON dump.
- [format_canon](node_0_3_1_11_2_format_canon/CORE_0_3_1_11_2_format_canon.md)
  — `format_jvm` and its siblings: map the dump's own schema (unit
  id, label, objdump lines, hex bytes, operand types) onto the
  op_units record (probe id, operator label, instruction list,
  bytes, holder representations).
- [invoke_normalizer](node_0_3_1_11_3_invoke_normalizer/CORE_0_3_1_11_3_invoke_normalizer.md)
  — hand the written records to the canonical-form stage
  (`canon40_interp.py` today).
- [run_pipeline](node_0_3_1_11_4_run_pipeline/CORE_0_3_1_11_4_run_pipeline.md)
  — the lane that runs parse → format → normalize for one language.
- [run_jvm](node_0_3_1_11_5_run_jvm/CORE_0_3_1_11_5_run_jvm.md)
  — the java route: warm the method until C2 compiles it, dump the
  emitted code, carve it; the one route where the unit is emitted at
  run time rather than found in a binary.
- [target](node_0_3_1_11_6_target/CORE_0_3_1_11_6_target.md)
  — which interpreter build is read: the instrumented php and ruby
  builds in Airlock, cpython, the jdk in the image.
- [output](node_0_3_1_11_7_output/CORE_0_3_1_11_7_output.md)
  — the written records: `canon_interp_units_{java,cpython}.json`,
  `canon_interp_units_ruby_php.json`, then `canon40_interp.json`.

## 3. State, 2026-09-06

| language | units | bodies | on canonical form | verdict |
|---|---:|---:|---|---|
| php | 4 | 4 | yes | PROVED_BY_CONSTRUCTION (wrapping faithful; z3 answered for none: the reference has no model for `movl`-style moves in these bodies) |
| ruby | 4 | 2 | 2 wrap; `rb_big_plus`, `vm_opt_plus` have no ship body, refused by name | as php |
| cpython | 1 | 1 | yes | as php |
| java | 2 | 2 | refused at the seventh block kind: they reach 0x538 past `own-address`'s 0x100 `AREA_SPAN` | UNDECIDED |

All eleven are `+` except one java `/`. They are members of the
pool's three compiled-and-interpreted entries (integer addition,
E00029, has php, ruby and cpython members). Population note: these
eleven are NOT those languages' operator sets; a census over them
says nothing about the language (learned the hard way, 2026-09-06,
task o2).

## 4. Open

- the owner's: `AREA_SPAN` 0x100 against the two java units (log_204 §4.4).
- Not a decision: the reference needs models for the move forms the
  handler bodies use so the nine PROVED_BY_CONSTRUCTION units become
  solver-proved (log_204 §6.3).
- The operator sets: each interpreted language's probes generated
  from `operator_arity.json` over its holders, handler located per
  probe by the diary, so the corpus grows past eleven. That is the
  remaining_languages plan per language.

## record

- artifacts: `PseudoCoupHQ/Research/op_pipeline/`
  (`interp_feeder.py`, `canon_interp_*.py`, `canon40_interp.json`,
  `build_interp_join*.py`, `interp_php.md`).
- logs: 095, 101, 107, 113, 119, 124, 199, 201.
