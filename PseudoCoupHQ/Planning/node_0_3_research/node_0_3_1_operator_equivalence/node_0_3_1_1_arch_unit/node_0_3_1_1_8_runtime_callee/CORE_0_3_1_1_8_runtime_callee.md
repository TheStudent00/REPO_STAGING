---
id: hq.research.compiler_graph.arch_unit.runtime_callee
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method), work
node:
    name: runtime_callee
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_1_arch_unit/node_0_3_1_1_8_runtime_callee/CORE_0_3_1_1_8_runtime_callee.md
super_node:
    name: arch_unit
    path: ../CORE_0_3_1_1_arch_unit.md
sub_nodes: []
---

# CORE 0_3_1_1_8 — runtime_callee

## metadata

- **id:** hq.research.compiler_graph.arch_unit.runtime_callee
- **level:** 4
- **status:** draft
- **designation:** code (method), work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [arch_unit](../CORE_0_3_1_1_arch_unit.md)

## sub_nodes

*(none yet)*

## definition

For a body that `call`s a routine of the compiler's OWN runtime, the
step that extracts that routine's body out of the runtime archive on
this machine and attaches it as a further arch-unit the caller
references. The routines in question are the compiler's lowering of
operations the hardware has no single instruction for — `__divti3`,
`__udivti3`, `__modti3`, `__umodti3` for 128-bit division and
remainder — shipped in libgcc or compiler-rt and built by the same
compiler. 308 units carry such a call. As of 2026-09-03 (task 59) 304 of them
have a producing row again; the remaining 4 are swift's, whose
toolchain is not on this machine.

## design

```
ArchUnit.runtime_callee
	attributes:
		archive_paths
			"""
			the libgcc / compiler-rt archives on
			this machine, per toolchain, so the
			callee comes from the same compiler
			that built the caller
			"""
	methods:
		is_runtime_routine
			"""
			callee name -> yes when the routine
			is shipped with the compiler as part
			of its own lowering; no when it is
			an outside library
			"""
		extract_callee
			"""
			archive + callee name -> a further
			ArchUnit: its own bytes, text and
			arrival contract.  the body is read
			RELOCATION-AWARE (objdump -dr), and
			the symbol is located by its ADDRESS
			AND SIZE in the member, because one
			address in an archive member carries
			several names
			"""
		extract_closure
			"""
			archive + callee name -> that callee
			and every callee ITS body names
			through a relocation, followed the
			same way, with a cycle guard so a
			routine that reaches itself is
			extracted once
			"""
		attach
			"""
			caller ArchUnit + callee ArchUnit ->
			the caller's record references the
			callee; the caller's answer row is
			produced by the callee
			"""
```

## settled rules

- **A `call` into the compiler's own runtime is followed.** the owner,
  2026-09-03: "if its within the compiler, its not a library call. if
  the compiler is importing something as a standard feature, also not
  a library call." Decision: [arch_unit](../CORE_0_3_1_1_arch_unit.md) settled rules.
- **That ruling SUPERSEDES the "out of scope" verdict** recorded the
  same day in
  `~/Programming/PseudoCoupHQ/Research/op_pipeline/out_of_scope_library_calls.json`.
  The file's LIST of 308 units stands as a list; its verdict does not.
  Decision: the owner, 2026-09-03; carried in [arch_unit](../CORE_0_3_1_1_arch_unit.md) and in
  [probes](../../node_0_3_1_0_probes/CORE_0_3_1_0_probes.md).
- **The callee comes from the archive on THIS machine**, produced by
  the same compiler as the caller, so the two are one compiler's
  answer and not two toolchains stitched together. Decision: this
  CORE, 2026-09-03, refining the ruling above.
- **The transfer into the runtime IS in the destination table now**,
  and it writes WHAT THE ATTACHED CALLEE'S OWN BODY SAYS IT WRITES —
  one row per register family that body changes, read off the body.
  Decision:
  [destination_rules](../../node_0_3_1_3_ledger/node_0_3_1_3_3_destination_rules/CORE_0_3_1_3_3_destination_rules.md)
  rule 4, 2026-09-03; log_158 TASK 59 (b) for the rule's existence,
  task 78 for what it writes. It answers what log_152 §9.2 put to the owner
  and log_153 §3.4 left as a census row.
  - Superseded, and named so the change is visible: "and it writes the
    accumulator". That was wrong for every float lowering (they answer
    in `%xmm0`) and wrong in a second way for all of them (one row
    where the body writes several places) — log_168 §5.3.
- **A toolchain that is not on this machine is recorded as not
  located, and its callers are not attached.** swiftc answers no
  question here, so no swift caller is given a runtime producer from
  another compiler's archive — which would be exactly the "two
  toolchains stitched together" the rule above forbids. Decision: this
  CORE, 2026-09-03; evidence `runtime_callee_printed.txt`.
- **EVERY callee the toolchain's own builtins archive defines is a
  runtime routine, not only the four division names.** Measured
  2026-09-03 over canon39: 3,419 call-bearing units, of which the
  `__divti3` family is 308; the rest are `__extendhfsf2` (2,308
  sightings), `__truncsfbf2` (1,168), `__truncsfhf2` (1,143),
  `__netf2` (536), `__floatsitf` (310), `__gttf2`/`__lttf2` (157
  each), `__floatditf`, `__eqtf2`, `__getf2`, `__letf2`,
  `__floattisf`, `__floatuntisf`, … — half-float, bfloat16 and
  128-bit-float lowering, all defined in libgcc / compiler-rt.
  `is_runtime_routine` already answers from the archive's symbol
  index (`nm --print-armap`), so the rule is: attach whatever the
  index defines. Decision: coordinator, 2026-09-03 (log_165 §3),
  applying the owner's ruling above; no new ontology.
- **swift's toolchain lives in the `trickle` instance's persist
  volume** (`/persist/swift/usr/bin/swiftc`, per `lane_gen.py`), not
  on the host and not in a fresh instance's volume. The 4 swift
  callers are attached by running the extraction as a lane on the
  `trickle` instance. Decision: coordinator, 2026-09-03 (log_165 §3);
  the rule against stitching toolchains is unchanged.
- **A CALLEE IS LOCATED BY ADDRESS AND SIZE, NOT BY NAME.** One
  address in an archive member carries several names — clang's
  `comparetf2.c.o` defines `__cmptf2`, `__eqtf2`, `__netf2`, `__letf2`
  and `__lttf2` all at address 0 with size 0xb9 — and
  `objdump --disassemble=__netf2` prints NOTHING for such a name,
  because objdump labels the address with the first name it holds.
  So `extract_callee` reads `nm -S --defined-only` for the symbol's
  address and size and disassembles that RANGE. Decision: this CORE,
  2026-09-03 (task 63); evidence `canon39_callee_printed.txt`, the
  `nm -S` block.
- **NESTED CALLEES ARE FOLLOWED THE SAME WAY, RELOCATION-AWARE, WITH
  A CYCLE GUARD.** An archive body is not linked, so a `call` in it
  disassembles as a transfer to an address inside the same member and
  the callee's name exists only in the relocation — log_161's finding,
  now applied one level down. `extract_closure` reads `objdump -dr`,
  folds each relocation onto the instruction it belongs to as
  `!!reloc=<type>:<symbol>`, and extracts every symbol so named that
  the same archive's index defines, once per name. Decision: this
  CORE, 2026-09-03 (task 63), answering log_163 §7.1 item 3.
- **A CALLEE THE ARCHIVE INDEX DOES NOT DEFINE IS NOT ATTACHED, AND
  ITS CAUSE IS RECORDED.** go's `x_runtime_panicshift` and rust's
  `panic_const_div_by_zero` are their own runtimes' panic paths, not
  the compiler's lowering of an operation the hardware lacks; no
  builtins archive defines them, so `is_runtime_routine` answers no
  and the caller is recorded as not attached with that reason. This
  is the same distinction log_153 §3.4 drew for the five go units.
  Decision: this CORE, 2026-09-03 (task 63).
- **THE MNEMONICS THE ARCHIVE BODIES SPELL JOIN THE ONE OPCODE
  TABLE.** An attached body is an arch unit like any other, so the
  arch opcodes it spells — `endbr64`, `bsr`, `cmovle`, … — are
  entries in `Reference.opcode_table`, not a second table beside it.
  Decision: [opcode_table](../../node_0_3_1_4_reference/node_0_3_1_4_0_opcode_table/CORE_0_3_1_4_0_opcode_table.md)
  is the one table (AgentMemory, round-12 rulings); applied here
  2026-09-03 (task 63), answering log_163 §7.1 item 3's second half.

- **WHAT A GO OR RUST PANIC PATH IS IN THE LEDGER'S VOCABULARY — A
  PROPOSAL PUT HERE BEFORE ANY CODE, AND FLAGGED FOR DEE.** The 196
  callers no archive index defines are NOT one thing; the bodies say
  so, and the reading is machine form:

  | what the caller's own text shows | proposed name |
  |---|---|
  | NOTHING follows the transfer on its own path — the body ends, or the next line defines a label that is NOT the transfer's own return point — so the compiler emitted no continuation and the routine does not come back | **guard exit** |
  | the transfer is followed by an instruction of the same block, OR by the label the transfer itself names, so the routine DOES come back | **unread runtime routine** |

  THE RETURN-POINT CLAUSE IS LOAD-BEARING AND WAS MISSED AT FIRST
  WRITING, so it is recorded here with how it was caught. An unlinked
  `call` disassembles as a transfer to its own next address, and
  ruling 4's positional-label pass then writes `call L0` with `L0:`
  defined on the very next instruction (log_161's finding). So "a
  label follows" is what a RETURNING call looks like in this corpus,
  not what a non-returning one looks like. The first criterion said
  only "the next line is a label definition or the body ends", and it
  put `c/regen_1075` — `call L0 !!reloc=…__floattihf-0x4` followed by
  `L0:` and four more instructions that use the answer — in the guard
  exits. Caught by reading the unit, 2026-09-03, before the rule was
  reported.

  Measured 2026-09-03 over canon40's 31,078 units. The guard exits are
  `x_runtime_panicshift` (122 call lines), `x_runtime_panicdivide`
  (28) and rust's four `core::panicking::panic_const` names, reached
  through `call *0x0(%rip)` with a `R_X86_64_GOTPCREL` relocation (46
  call lines). The unread runtime routines are go's
  `x_runtime_newobject` and `x_runtime_morestack_noctxt_abi0` (20
  units carrying both), and c's and cpp's `__floattihf` and
  `__floatuntihf` — half-float conversions the caller's own toolchain
  ARCHIVE DOES NOT DEFINE, which is why task 63 extracted no body for
  them. The exact tallies per language are in `audit78_printed.txt`,
  "THE 196, BY THE SHAPE THE CALLER'S OWN TEXT GIVES THEM".

  - **guard exit** — the transfer produces no value, because control
    never returns to the body. The ledger makes NO row for it and
    records a typed note `{"kind": "guard_exit", "callee": …}` naming
    the routine. It is the RESPONSE half of a guard in the ratified
    mode-row vocabulary ("a branch leading to a trap or a panic
    call", AgentMemory), not a producer.
  - **unread runtime routine** — the routine returns and may leave a
    value, but no archive index on this machine defines it, so the
    families it changes CANNOT BE READ. The ledger makes NO row and
    records a typed note `{"kind": "unread_runtime_routine",
    "callee": …}`. A guessed row is exactly the defect
    `destination_rules` rule 4 is being repaired for, so none is
    written. `go/op_30` is the printed instance: `call
    x_runtime_newobject` is followed by `mov 0x20(%rsp),%ecx; mov
    %ecx,(%rax)`, so the caller reads `%rax` and the ledger today says
    `%rax` still holds the `lea` before the call.

  FLAGGED FOR DEE, exactly as log_183's closing line reserves it.
  Three options were open and only the first is implemented:
  (1) the two named notes above, no row and no refusal — nothing that
  proves today stops proving; (2) a fifth producer KIND beside
  `arch_opcode` / `flag_pair` / `non_opcode_phrase` /
  `runtime_callee`, which would put a row on the ledger with no body
  behind it; (3) extracting go's and rust's own runtime the way the
  builtins archives are extracted — the owner's ruling "if the compiler is
  importing something as a standard feature, also not a library call"
  can be read as reaching these, and if it does, the 20 returning
  callers become ordinary attachments and the 176 stay guard exits.
  Decision: NOT TAKEN — this CORE records the proposal and the
  evidence, 2026-09-03 (task 78).

## realization (what exists on disk, 2026-09-03)

Home: `~/Programming/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| the list of affected units | `out_of_scope_library_calls.json` — 308 units | list stands; its verdict superseded 2026-09-03 |
| the census row for the cause | `name_census4.json`, `name_census4_printed.txt` — 300 units, `__udivti3` 77, `__umodti3` 77, `__divti3` 73, `__modti3` 73 | done as a census row (log_153 §3.4) |
| archive_paths, is_runtime_routine, extract_callee, attach | `runtime_callee.py` (`class RuntimeCallee`), driven by `runtime_callee_run.py` | done 2026-09-03 (task 59) |
| the archives, per toolchain, quoted from the toolchain's own output | `runtime_callee_printed.txt`, and `runtime_callee_units.json` `meta.location_record` | done: gcc, clang, clang++ and rustc answered; **swiftc is not on this machine** and is recorded as not located, so the 4 swift callers are not attached |
| the four bodies, extracted | `runtime_callee_units.json` — 12 callee arch units (4 routines x 3 toolchains that answered), each with its own bytes, text and arrival contract | done; `clang/__divti3`'s 27-instruction body printed in full in `runtime_callee_printed.txt` |
| the callers, attached | `runtime_callee_attachments.json` | done: **304 of the 308** recorded callers (c 136, cpp 164, rust 4); the 4 swift callers are not attached, for the reason above |
| the transfer in the destination table | `ledger.py` (`RUNTIME_TRANSFER_RULE`, `transfer_callee`) | done (see destination_rules rule 4) |

### what task 63 added, 2026-09-03

| part | current file | status |
|---|---|---|
| the census the attachment is driven by | `canon39_callee_census.json` — 4,119 call-bearing units of canon39's 30,432 proved, 36 distinct callee names | done |
| `extract_callee`, relocation-aware, symbol located by address and size; `extract_closure`, nested callees followed with a cycle guard | `runtime_callee.py` (`member_symbols`, `disassemble_range`, `fold_relocations`, `nested_callees`, `RuntimeCallee.extract_closure`) | done |
| the callee arch units, including the nested ones | `canon39_callee_units.json` — 76 units, from the clang, clang++, rustc and swiftc archives — one per toolchain that actually built a caller | done |
| the callers, attached | `canon39_callee_attachments.json` — 3,923 of 4,119; 196 not attached, by cause | done |
| swift, extracted where swift lives | `runtime_callee_swift_lane.py` + `runtime_callee_swift_lane.sh`, run on the `trickle` instance; product `canon39_callee_swift_lane.json`, transcript `canon39_callee_swift_lane_printed.txt` | done |
| the arch opcodes the attached bodies spell | `canon39_callee_opcodes.json`, `acceptance63_printed.txt` | done |
| the answers that already existed, unmoved | `regression63.json`, `regression63_printed.txt` — 3,000-unit sample, 0 changed | done |
| the guard | `guard63.py`, `guard63_transcript.txt`, `guard63.json` — 6 paths, PASS 6, exempt 0 | done |

### what task 78 added, 2026-09-03

| part | current file | status |
|---|---|---|
| the two named shapes for a transfer no archive index defines | `ledger.py` (`Ledger.record_transfer_shape`), carried on every unit as `transfer_shapes` | done, FLAGGED for the owner |
| the census | `audit78_printed.txt`, "THE 196, BY THE SHAPE THE CALLER'S OWN TEXT GIVES THEM": guard exit 180 units (go 150, rust 30), unread runtime routine 108 units (c 40, cpp 48, go 20) | done |
| the four swift callers task 59 left unattached | now wrapped and proved in canon40 (`swift/regen_315`, `321`, `327`, `333`), because task 63 extracted swift's archive inside the instance where swift lives | done |
| the callee bodies' own answers, read | `runtime_answers78.json` (see [destination_rules](../../node_0_3_1_3_ledger/node_0_3_1_3_3_destination_rules/CORE_0_3_1_3_3_destination_rules.md)) | done |

The 88 c and cpp units in the unread bucket are NEW against task 63's
196. Task 63 counted UNITS WITH NO ATTACHMENT AT ALL; a unit that
transfers into `__extendhfsf2` (attached) and into `__floattihf` (which
no archive index defines) counted as attached. Task 78 counts
TRANSFERS, so those 88 appear -- and all 88 carry attached runtime rows
beside the unread one, which is what makes them invisible to a per-unit
count.

The 308 and the 300 differ by five go units (`go/regen_142`, `143`,
`144`, `145`, `147`) whose transfer is to a panic routine, not to a
routine that computes the answer (log_153 §3.4).
