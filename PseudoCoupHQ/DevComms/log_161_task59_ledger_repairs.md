# log 161 — TASK 59, the ledger repairs

Date: 2026-09-03. Node `hq.research.compiler_graph.ledger` (0_3_5_3)
and `hq.research.compiler_graph.arch_unit.runtime_callee` (0_3_5_1_8).
Round 12, first run under the plan tree (log_158).

---

# 1. What was asked and what stands now

Three things were asked, and all three landed. Each is stated here at
top level, and each has its own section below with the values moving.

- **(a)** `sbb` and `adc` had no model as flag SETTERS. They have one
  now, written into the tree first and then coded: each one writes TWO
  rows, a value row and a `flags only` row, and a following flag
  reader links to the flags row. **728 units of the 31,067 walked**
  carry a flag pair whose setter is one of the two.
- **(b)** A transfer into the compiler's own runtime had no producing
  row. The four routines' bodies are now extracted from the archive
  each toolchain names as its own and attached as further arch units
  the caller references. **304 of the 308 recorded callers** are
  attached; the 4 that are not are swift's, whose toolchain is not on
  this machine.
- **(c)** `ledger.py` exists, carrying `Ledger`, `Row`, `Producer`,
  `DESTINATION_RULES` and `FLAG_RULES`, importing nothing from
  `ledger47.py` or `ledger48.py`. Its unit test walks a **computed**
  sample of 241 units and prints the rows: 241 walked, 0 refused,
  2,189 rows, 0 producer holes.

## 1.1 What this task did NOT do, said plainly

- It did not re-render a population. `canon39_*` is task 60's
  (`canonical_form.py`, node 0_3_5_2), which consumes
  `ledger.wrap_unit`. This log carries no proved/disproved figure,
  because proving is the gate's job (node 0_3_5_5, task 58) and no
  claim about it can be made from here.
- It did not edit `ledger47.py`, `ledger48.py` or
  `out_of_scope_library_calls.json`. `git status --porcelain` over the
  three is empty; the supersession is a NEW file beside the recorded
  one.

---

# 2. The tree was corrected before any code was written

Round 12's binding rule 2: a shape the tree lacks is added to the tree
first. Three COREs said "planned" where this task needed a shape, so
three COREs were written before the code that realizes them.

## 2.1 flag_rules — `## design` rule 7, rewritten

It said: "`sbb` and `adc` set flags from their own arithmetic. As
SETTERS they have no model yet, which is what 699 units are waiting
on." That is a gap named, not a shape. It now states the two-row
model (section 3), and adds a rule 8 saying that whether EVERY
arithmetic setter should carry its own flags row is not decided here
and not invented here.

Provenance written into the CORE: log_158 TASK 59 (a), closing the gap
log_153 §4.2 named. The superseded sentence is quoted in the settled
rules rather than deleted.

## 2.2 destination_rules — `## design` rule 4, rewritten

It said: "Planned: a `call` into the compiler's own runtime writes the
accumulator, naming the callee as the producer. Not added until
ruled." the owner ruled on 2026-09-03 and log_158 states the producer shape,
so the rule is now written, with the condition that decides when it
fires (section 4.2).

## 2.3 producer — a THIRD field

The CORE said a producer is "a typed object with two fields — `kind`
and `mnem`". The brief specifies
`{"kind": "runtime_callee", "callee": "__divti3"}`, which has no
`mnem`. The CORE now states `callee` as the second field of that one
kind, because what produced the value is a ROUTINE and not an
instruction. Provenance: log_158 TASK 59 (b).

## 2.4 runtime_callee and ledger — realization tables

Both nodes' realization tables now say what is on disk. `runtime_callee`
also gains one settled rule this task's own evidence forced: a
toolchain that is not on this machine is recorded as not located and
its callers are NOT attached, because attaching another compiler's
archive is exactly the "two toolchains stitched together" that CORE
already forbids.

---

# 3. (a) `sbb` and `adc` as flag setters, with the values moving

## 3.1 The instruction, and why one row was not enough

`sbb %rsi,%rcx` is, on the machine: `rcx = rcx − rsi − carry`. Two
facts about it:

- it READS the carry the previous flag-setting instruction left, so
  its answer depends on the flag state and not only on its operands;
- it SETS the flags from its own subtraction, so a following `setl`
  answers from `sbb`'s flags, not from the earlier `cmp`'s.

The old walk gave it ONE row, typed `8-byte general value`, and then
pointed the "row that set the flags" at that value row. A following
`setl` therefore linked to a row that carries no flag state at all.

## 3.2 The unit, and what the ledger said before

LITERAL — `c/regen_34943`, its recorded ledger in
`canon38_regen_store/`, as log_153 §4.2 printed the hole:

```
   hole GUARD-0 {'kind': 'flag_pair', 'mnem': ['sbb', 'setl']}
        the flag-setting arch opcode 'sbb' left flags this file could not build
```

## 3.3 The unit, and what the ledger says now

LITERAL — `ledger_sample_walk_printed.txt`, the carry-in section:

```
  c/regen_34943   [population: carry-in]
    body: mov IN-0,%rdi; mov IN-1,%rsi; mov IN-2,%rdx; mov %edi,%eax;
          cmp %rax,%rsi; sbb $0x0,%rdx; setl %al; movzbl %al,%eax;
          mov %eax,OUT-0; ret
    row      type                 produced by            operands
    IN-0     8-byte general value arrival
    IN-1     8-byte general value arrival
    IN-2     8-byte general value arrival
    TEMP-0   8-byte general value mov                    IN-0
    TEMP-1   flags only           cmp                    TEMP-0,IN-1
    CONST-0  literal              the body's own immediate operand
    TEMP-2   8-byte general value sbb [the difference]   TEMP-1,CONST-0,IN-2
    TEMP-3   flags only           sbb [the flags]        TEMP-1,CONST-0,IN-2
    GUARD-0  flag-derived value   sbb + setl             TEMP-3,TEMP-0
    TEMP-4   8-byte general value movzbl                 GUARD-0
    OUT-0    4-byte general value movzbl                 TEMP-4
```

(Line-wrapped here for width; the file has each row on one line.)

GLOSS, with values. Take the three arrivals `IN-0 = 5`,
`IN-1 = 5`, `IN-2 = 0` — a 128-bit comparison whose low halves are
equal.

- `TEMP-0` is `5`: the body copies `IN-0` into the accumulator.
- `TEMP-1` is the flag state `cmp %rax,%rsi` leaves comparing
  `IN-1 = 5` against `TEMP-0 = 5`. Equal, so the carry it leaves is
  0. The row is typed `flags only` and repoints no register.
- `TEMP-2` is `sbb`'s VALUE half: `IN-2 − CONST-0 − carry`, that is
  `0 − 0 − 0 = 0`. Its first operand is `TEMP-1`, the row the carry
  came out of.
- `TEMP-3` is `sbb`'s FLAGS half, from the same three operands. This
  is the row that did not exist before.
- `GUARD-0` is the pair `(sbb, setl)`, and its FIRST operand is
  `TEMP-3` — `sbb`'s own flags, not `cmp`'s. With the subtraction
  giving 0 and no borrow, `setl` is 0.
- `OUT-0` is that widened: `0`.

The mechanism, stated: the ledger now carries the LINEAGE the
reference needs. Whether `c/regen_34943` proves is task 58's answer
from `reference.py`'s term for `sbb`'s flags; this node does not claim
it.

## 3.4 The population, counted from canon38

Counted by walking every recorded unit and looking for a flag pair
whose setter mnemonic stems to `sbb` or `adc`:

```
units walked (population): 31067      (canon38_regen_store 29,288
                                       + canon38_wrapped_* 1,779)
units with a flag_pair whose SETTER stems to sbb or adc: 728
by stem (a unit may carry both): {'sbb': 726, 'adc': 2}
by language: {'c': 284, 'cpp': 390, 'rust': 8, 'swift': 46}
```

Reconciliation with log_153 §4.2's **699**: that figure is the subset
that MOVED from proved to no-term when the flag link was made honest.
**728** is the ledger-side population — every unit whose recorded
ledger carries such a pair, whatever its verdict was. The two count
different things over the same evidence, and both are stated with
their population.

---

# 4. (b) The compiler's own runtime, followed

## 4.1 The archives, quoted from each toolchain's own output

No path below was typed. Each is the first line the named command
printed. LITERAL — `runtime_callee_printed.txt`:

```
$ gcc -print-libgcc-file-name
  /usr/lib/gcc/x86_64-linux-gnu/15/libgcc.a
$ clang -print-file-name=libclang_rt.builtins-x86_64.a
  /usr/lib/llvm-21/lib/clang/21/lib/linux/libclang_rt.builtins-x86_64.a
$ clang++ -print-file-name=libclang_rt.builtins-x86_64.a
  /usr/lib/llvm-21/lib/clang/21/lib/linux/libclang_rt.builtins-x86_64.a
$ rustc --print sysroot
  ~/.rustup/toolchains/stable-x86_64-unknown-linux-gnu
$ swiftc -print-target-info
  exit 127  no such executable: swiftc

archives located, per toolchain:
  clang    /usr/lib/llvm-21/lib/clang/21/lib/linux/libclang_rt.builtins-x86_64.a
  clang++  /usr/lib/llvm-21/lib/clang/21/lib/linux/libclang_rt.builtins-x86_64.a
  gcc      /usr/lib/gcc/x86_64-linux-gnu/15/libgcc.a
  rustc    ~/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/rustlib/x86_64-unknown-linux-gnu/lib/libcompiler_builtins-17bce873ebfac7f5.rlib
  swiftc   NOT LOCATED on this machine (swiftc -print-target-info)
```

Which toolchain built which language is read off `lane_gen.py`'s own
`compile_probe`, not assumed: c is `/usr/bin/clang`, cpp is
`/usr/bin/clang++`, rust is `rustc`, swift is
`/persist/swift/usr/bin/swiftc`.

### 4.1.1 swift, and the path check that proves which side of the wall

`lane_gen.py` names swift's compiler under `/persist/`, which is a
container path. Two checks were run, in the brief's order:

- HOST: `ls /persist` — "No such file or directory". Swift is not on
  the host.
- SANDBOX: a fresh Airlock instance `t59` was brought up
  (`bash up.sh --instance t59`), a probe lane submitted, and it
  reported `ls: cannot access '/persist/swift/usr/bin/swiftc': No such
  file or directory` and found no `libclang_rt.builtins*` anywhere
  under `/persist/swift`. The instance was taken down
  (`bash down.sh --instance t59`).

So swift's runtime archive is reachable from neither side within this
task's own instance, and the 4 swift callers are recorded as not
attached rather than given another compiler's archive. That refusal is
now a settled rule in the runtime_callee CORE.

## 4.2 What counts as a runtime routine — machine-form evidence

`is_runtime_routine` does not consult a list of names. It reads each
archive's own symbol index with `nm --print-armap` and answers from
that. LITERAL — the same transcript:

```
== IS EACH NAME A ROUTINE OF THE COMPILER'S OWN RUNTIME? (the archives' own symbol index) ==
  __divti3   yes   defined in: gcc, clang, clang++, rustc
  __modti3   yes   defined in: gcc, clang, clang++, rustc
  __udivti3  yes   defined in: gcc, clang, clang++, rustc
  __umodti3  yes   defined in: gcc, clang, clang++, rustc
```

That is also what makes the destination rule safe to add: the rule
fires on the archive's answer, never on how the callee's name is
spelled.

## 4.3 One body, literally

`ar x` extracts the member the index names; `objdump -d
--disassemble=__divti3` prints it; the address and byte columns are
dropped, which is the shape every other body in this pipeline is
stored in. LITERAL — `runtime_callee_printed.txt`:

```
== LITERAL -- one body in full: clang/__divti3 ==
archive: /usr/lib/llvm-21/lib/clang/21/lib/linux/libclang_rt.builtins-x86_64.a
member:  divti3.c.o
arrival families (read before written): rbx, rsi, rcx, rdi, rdx
    0  endbr64
    1  push %rbx
    2  mov %rsi,%rax
    3  shr $0x3f,%rax
    4  mov %rsi,%r8
    5  sar $0x3f,%r8
    6  mov %rcx,%r9
    7  shr $0x3f,%r9
    8  mov %rcx,%rbx
    9  sar $0x3f,%rbx
   10  xor %r8,%rsi
   11  xor %r8,%rdi
   12  add %rax,%rdi
   13  adc $0x0,%rsi
   14  xor %rbx,%rcx
   15  xor %rbx,%rdx
   16  add %r9,%rdx
   17  adc $0x0,%rcx
   18  xor %r8,%rbx
   19  xor %r8d,%r8d
   20  call 46 <__divti3+0x46>
   21  xor %rbx,%rdx
   22  xor %rbx,%rax
   23  sub %rbx,%rax
   24  sbb %rbx,%rdx
   25  pop %rbx
   26  ret
```

GLOSS, with values. The routine takes two 128-bit values, `a` in
`rdi:rsi` and `b` in `rdx:rcx`. Take `a = −7` and `b = 2`.

- Lines 2–3 put the SIGN of `a`'s high half in `rax` as 0 or 1:
  `a` is negative, so `rax = 1`.
- Lines 4–5 spread that sign through `r8`: `r8 = 0xFFFF…FF`.
- Lines 10–13 make `|a|`: exclusive-or both halves with `r8` (a
  one's complement when the sign is set) and then add `rax = 1`
  through both halves — `add` on the low, `adc` on the high, so the
  carry the low addition leaves reaches the high one. That is a
  128-bit two's complement negation done in two 64-bit steps, and it
  is the exact instruction pair section 3 gives a flag row to.
- Lines 6–9 and 14–17 do the same to `b`; `b` is positive, so nothing
  changes.
- Line 18 puts the SIGN OF THE ANSWER in `rbx`: the two signs
  exclusive-ored. One negative, one positive, so `rbx = 0xFFFF…FF`.
- Line 20 divides the two magnitudes: `7 / 2 = 3`.
- Lines 21–24 apply the sign back, again with `sub` on the low and
  `sbb` on the high so the borrow crosses. The answer is `−3`.

That the runtime's own body leans on `adc` and `sbb` in exactly the
carry-crossing way section 3 models is corroboration, not coincidence:
128-bit arithmetic on a 64-bit machine is what both are about.

## 4.4 The rule firing inside the walk

The callee's name reaches the ledger from the RELOCATION, not only
from the assembler identifier. An unlinked `call` disassembles as a
transfer to an address inside the unit, so the positional-label pass
writes `call L0` and only `!!reloc=R_X86_64_PLT32:__divti3-0x4` still
says where it goes. `transfer_callee` reads both.

LITERAL — `ledger_sample_walk_printed.txt`:

```
  c/regen_10427   [population: runtime]
    body: mov IN-0,%rdi; mov IN-1,%rsi; mov IN-2,%rdx; push %rax;
          mov %rdx,%rcx; mov %rsi,%rdx; mov %edi,%edi; xor %esi,%esi;
          call L0 !!reloc=R_X86_64_PLT32:__divti3-0x4; L0:; pop %rcx;
          mov %rax,OUT-0; ret
    row      type                 produced by                          operands
    IN-0     8-byte general value arrival
    IN-1     8-byte general value arrival
    IN-2     8-byte general value arrival
    STACK-0  8-byte value on the machine stack push
    TEMP-0   8-byte general value mov                                  IN-2
    TEMP-1   8-byte general value mov                                  IN-1
    TEMP-2   8-byte general value mov                                  IN-0
    TEMP-3   8-byte general value xor                                  IN-1,IN-1
    TEMP-4   8-byte general value runtime __divti3 [the runtime routine's answer]  TEMP-2,TEMP-3,TEMP-1,TEMP-0
    OUT-0    8-byte general value runtime __divti3                     TEMP-4
```

Before this lap `OUT-0`'s producer on this unit was
`{"kind": "non_opcode_phrase", "phrase": "the body's last write to
%rax"}` — a row saying no opcode wrote the answer. It now names the
routine that did, and `TEMP-4`'s operands are the four argument
registers the caller had set up.

## 4.5 The counts

LITERAL — `runtime_callee_printed.txt`:

```
callers in the recorded list: 308
attached (answer row now produced by the runtime callee): 304
  by language: {"c": 136, "cpp": 164, "rust": 4}
not attached, no archive for the caller's own toolchain: 4
not attached, the store carries no such unit: 0
```

The 4 not attached are swift's, per 4.1.1. `runtime_callee_units.json`
holds 12 callee arch units — 4 routines × the 3 toolchains that
answered — each with its own bytes, text and arrival contract.

## 4.6 The supersession, recorded without editing the record

`out_of_scope_library_calls.json` is READ and left exactly as it is
(`git status --porcelain` over it is empty). The new file
`out_of_scope_library_calls_superseded.json` states that its verdict
no longer holds while its list of 308 stands, quotes the verdict it
replaces, quotes the owner's ruling, and cites log_158 TASK 59 and the
runtime_callee CORE.

---

# 5. (c) `ledger.py`

## 5.1 What it carries, and what it does not import

One module, named for its node, carrying `Ledger` (attribute `rows`,
method `walk_dataflow`), `Row`, `Producer`, `DESTINATION_RULES` and
`FLAG_RULES` — the CORE's `## design`, sub-node for sub-node.

`grep -n "import ledger4" ledger.py` returns ONE line, and it is
inside the docstring:

```
91:  * ledger48's module-level `import ledger47 as L47` re-export block.
```

Its only imports are `canon`, `canon33_gate` and `region36`, none of
which is a superseded ledger record. Every part copied from `ledger47`
or `ledger48` carries a header line naming the file and saying it is
unchanged; the docstring also lists what is NOT copied and why.

## 5.2 The unit test walks a COMPUTED sample

The sample is not a list somebody typed. It is:

1. every acceptance unit of logs 152 and 153, read BY PATTERN out of
   the two logs' own text and out of `acceptance48.py` and
   `acceptance53.py` — 44 names found, all 44 present in the recorded
   populations;
2. 50 random units per population at a fixed seed (59), over four
   populations: regenerated (29,288), wrapped (1,779), carry-in (728 —
   the population repair (a) is about) and runtime (308 — the
   population repair (b) is about).

LITERAL — the tail of `ledger_sample_walk_printed.txt`:

```
== THE WHOLE SAMPLE, WALKED ==
units in the sample: 241
units walked without refusal: 241
units refused by name: 0
rows built over the sample: 2189
rows by producer kind, over the sample of 241 units:
  arch_opcode          1167
  flag_pair            229
  non_opcode_phrase    689
  runtime_callee       104
rows by type, over the same sample:
  1-byte general value               78
  16-byte vector value               139
  4-byte general value               64
  8-byte general value               1325
  8-byte value on the machine stack  62
  8-byte vector-held value           14
  flag-derived value                 170
  flags only                         219
  literal                            99
  the unit's own stack address       4
  x87 stack value                    15
producer holes recorded over the sample: 0
```

The acceptance units of both logs are printed row by row earlier in
the same file, including `c/op_210` (the destination table's two
halves) and `go/op_174`, which is one of the 44 and happens to carry a
`sbb`, so both new rows appear in a unit the acceptance set chose for
other reasons:

```
    TEMP-3   flags only           cmp                    CONST-0,TEMP-1
    TEMP-4   8-byte general value sbb [the difference]   TEMP-3
    TEMP-5   flags only           sbb [the flags]        TEMP-3
```

## 5.3 The guard

The unmodified `check_no_spelling_keys.py`, run as a separate process,
one process over every JSON this task wrote. LITERAL —
`ledger_guard_transcript.txt`:

```
# guard: check_no_spelling_keys.py, unmodified, one process, 3 artifacts
# exit 0
operator inventory: 91 tokens read from probe_manifest_*.json
PASS runtime_callee_units.json -- no operator token in any key, grouping, pairing or row structure
PASS runtime_callee_attachments.json -- no operator token in any key, grouping, pairing or row structure
PASS out_of_scope_library_calls_superseded.json -- no operator token in any key, grouping, pairing or row structure
```

`grep -c exempt ledger_guard_transcript.txt` = **0**. No field
whitelist was added, no role key declared, no guard file edited.

One guard finding was fixed rather than exempted: the supersession
note's `recorded_in` field originally began with a `~`, which is an
operator token in the inventory, so it was rewritten repo-relative —
which also removes a machine-specific path from a tracked artifact.

---

# 6. Coordination with the other tasks of this round

- **Task 60** (`canonical_form.py`, node 0_3_5_2) consumes
  `ledger.wrap_unit(body_text, arrival_families, result_family,
  result_width, body_bytes=None, runtime_routines=None)`. Handing it
  the four routine names (readable from
  `runtime_callee_units.json`) is what makes the runtime rule fire;
  handing nothing leaves a transfer exactly as it was.
- **Task 57** (`reference.py`, node 0_3_5_4) now has a `flags only`
  row for `sbb`/`adc` with named operands, which is what a term for
  those flags has to be built from.
- **Task 58** (`gate.py`) is where any movement in the 728 and the 304
  becomes a verdict. Nothing here claims one.

---

# 7. File inventory

## 7.1 Written, in `Research/op_pipeline/`

| file | what it is |
|---|---|
| `ledger.py` | the node's module: `Ledger`, `Row`, `Producer`, `DESTINATION_RULES`, `FLAG_RULES` |
| `runtime_callee.py` | `class RuntimeCallee`: `archive_paths`, `is_runtime_routine`, `extract_callee`, `attach` |
| `runtime_callee_run.py` | the driver that locates, extracts, attaches and prints |
| `ledger_sample_walk.py` | the unit test over the computed sample |
| `ledger_guard.py` | the unmodified guard, one process, over every JSON written here |
| `runtime_callee_units.json` | 12 callee arch units, plus the full location record |
| `runtime_callee_attachments.json` | one entry per recorded caller, attached or not, with the reason |
| `out_of_scope_library_calls_superseded.json` | the supersession note beside the untouched record |
| `runtime_callee_printed.txt` | the (b) transcript, including one body in full |
| `ledger_sample_walk_printed.txt` | the (c) transcript: rows printed for the sample |
| `ledger_guard_transcript.txt` | the guard transcript |

## 7.2 Planning files touched

| file | what changed |
|---|---|
| `…/node_0_3_5_3_ledger/CORE_0_3_5_3_ledger.md` | producer's second field; two settled rules added; realization table rewritten; next-lap line |
| `…/node_0_3_5_3_ledger/PROGRESS.md` | 5 entries |
| `…/node_0_3_5_3_1_row/PROGRESS.md` | 2 entries |
| `…/node_0_3_5_3_2_producer/CORE_0_3_5_3_2_producer.md` | the `callee` field; kind 4 no longer "planned"; settled rule answered; realization |
| `…/node_0_3_5_3_2_producer/PROGRESS.md` | 4 entries |
| `…/node_0_3_5_3_3_destination_rules/CORE_0_3_5_3_3_destination_rules.md` | rule 4 rewritten; settled rule answered; realization |
| `…/node_0_3_5_3_3_destination_rules/PROGRESS.md` | 3 entries |
| `…/node_0_3_5_3_4_flag_rules/CORE_0_3_5_3_4_flag_rules.md` | rule 7 rewritten, rule 8 added; design block extended; settled rule; realization |
| `…/node_0_3_5_3_4_flag_rules/PROGRESS.md` | 3 entries |
| `…/node_0_3_5_1_8_runtime_callee/CORE_0_3_5_1_8_runtime_callee.md` | definition count; two settled rules; realization table rewritten |
| `…/node_0_3_5_1_8_runtime_callee/PROGRESS.md` | 6 entries |

All under
`Planning/node_0_3_research/node_0_3_5_compiler_graph/`.

## 7.3 Read and NOT modified

`ledger47.py`, `ledger48.py`, `out_of_scope_library_calls.json`,
`canon38_regen_store/*.json`, `canon38_wrapped_*.json`,
`check_no_spelling_keys.py`, `acceptance48.py`, `acceptance53.py`,
`lane_gen.py`, and the Airlock installation. `git status --porcelain`
over the three superseded records is empty.

## 7.4 The tree check

`python3 PRIVATE/PlanPlan/framework/check_plans.py
PRIVATE/PseudoCoupHQ/Planning` reports the same 5 dangling-path
errors and 3 warnings it reported before this task; none of them names
a file this task wrote or a CORE this task edited.

---

# 8. Open, and deliberately not asked

Nothing here needs a ruling from the owner. Two things are recorded as NOT
decided, each in the tree rather than in a question:

- whether every arithmetic flag setter should carry its own `flags
  only` row, not only the two that read the carry (flag_rules rule 8);
- swift's runtime archive, which no side of the container wall on this
  machine holds today (runtime_callee realization). The 4 swift
  callers stay unattached until a swift toolchain is present, and the
  rule that keeps them unattached is the same one that forbids
  stitching two toolchains together.
