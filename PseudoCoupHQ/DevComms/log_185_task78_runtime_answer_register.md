# log 185 — task 78: the runtime answer register, and the panic-path callees

Date: 2026-09-03. Round 15, TASK 78 of
`~/Programming/PseudoCoupHQ/DevComms/log_183_claude_code_task_briefs_round15.md`
(whose header says the round's briefs were written by the coordinator,
not by the owner; nothing in them is a ruling).

Nodes: `hq.research.compiler_graph.ledger.destination_rules`
(`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_3_ledger/node_0_3_5_3_3_destination_rules/`)
and `hq.research.compiler_graph.arch_unit.runtime_callee`
(`.../node_0_3_5_1_arch_unit/node_0_3_5_1_8_runtime_callee/`).

Appendix-B shape; §5.1a LITERAL / GLOSS labels throughout; every number
carries its population.

Python: `/tmp/reconnect_venv/bin/python3` (pyvex 9.3.4, z3 5.1.0,
capstone 5.0.7). **The venv was gone from `/tmp` at session start and
was rebuilt** — see §9.

---

# 1. What was done, in plain words before any figure

A body of machine code sometimes hands a value to a routine the
compiler ships with itself, and then reads the answer back out of a
register. The ledger has to say which register that is. Until today it
said "the accumulator", `%rax`, for every such routine. That is wrong
for every float lowering — they answer in `%xmm0` — and it is wrong a
second time for all of them, because the routine changes several
registers and the rule wrote down one.

This task replaced the assertion with a READING. Each attached
callee's own body is walked, and the registers it changes are read off
it. The caller's ledger then gets one row per register that routine
changes, each produced by that routine.

Second, the 196 callers whose target no archive index defines were
named. They are not one thing, and the callers' own text separates
them into two: transfers that never come back (go's and rust's panic
paths), and transfers that do come back but whose routine has no body
on this machine. **Which of the three available shapes is right is
the owner's, and it is flagged in §7.**

Third, everything was re-rendered into `canon40_*` and re-gated.

---

# 2. The corrected rule, and where it was written

## 2.1 The order was kept: CORE first, then PROGRESS, then code

LITERAL — `CORE_0_3_5_3_3_destination_rules.md`, `## design` rule 4 as
it now stands:

```
4. A transfer into the compiler's OWN runtime writes EVERY REGISTER
   FAMILY THE ATTACHED CALLEE'S OWN BODY CHANGES, one row per family,
   each produced by {"kind": "runtime_callee", "callee": ...}.  The
   families are READ OFF THE CALLEE'S BODY ...
   - SUPERSEDED WORDING, kept so the change is visible: "writes the
     accumulator, and the row it writes is ..." (one row, on %rax).
     That was wrong twice over ...
```

and the settled rule beside it states the reading as six numbered
steps: a token per family; move-like opcodes propagate their source's
token; the machine stack tracked so a save-and-restore ends unchanged;
`%rsp`/`%rbp`/`%rip` excluded as everywhere else; a tail transfer
followed with a cycle guard; an x87 answer named; and **an unreadable
callee refused BY NAME rather than guessed**.

GLOSS: the rule was written into the CORE before the code, under round
12's binding rule 2. One refinement went in AFTER its measurement and
says so on its own line — the save-and-restore clause needed a second
sentence, §3.3.

## 2.2 What "the callee's own answer" turned out to mean

The brief asked for "the ATTACHED CALLEE's own answer register". The
bodies say the honest answer is a SET, not a register: log_168 §5.3's
own second bullet already said so ("the callee's body writes several
places; the rule records one"). So the rule writes one row per family
the body changes. A family the routine merely clobbers is in the set
on purpose: the callee did change it, and a row saying so is true
where the old silence was false.

---

# 3. The reading, shown working

## 3.1 One body, and what is read off it

LITERAL — `acceptance78_printed.txt`, part 1, the tail of
`clang/__extendhfsf2` as `canon39_callee_units.json` holds it:

```
    shl $0x10,%eax
    and $0x80000000,%eax
    shl $0x17,%esi
    or %eax,%esi
    or %edx,%esi
    movd %esi,%xmm0
    ret
```

LITERAL — `runtime_answers78.json`, the same key:

```
    families: rcx,rdx,rax,rsi,xmm0
    x87: False
```

GLOSS: the accumulator IS in the set, because the body changes it —
but the family the caller reads is `xmm0`, and the superseded rule
never put a row there.

## 3.2 All 76 bodies

LITERAL — `runtime_answers78_printed.txt`, its last lines:

```
readings made: 76   refused by name: 0   leaving a value on the x87 stack: 6

CROSS-CHECK, reported and never used: the reading names at least one of
the stated calling convention's answer homes
  bodies whose reading names none of ('rax', 'rdx', 'xmm0', 'xmm1'): 0
```

GLOSS, with its evidence class. The 76 readings are FORCED BY
CONSTRUCTION from the archive bodies. Two cross-checks were computed
and neither was used as a source:

- every reading names at least one of the homes the calling convention
  states (0 of 76 name none);
- LITERAL — `acceptance78_printed.txt`, part 5:

```
readings: 76
readings naming a callee-saved family ('rbx', 'r12', 'r13', 'r14', 'r15', 'rbp'): 0
```

  The reading was never told which families the convention preserves.
  It reproduces the caller-saved / callee-saved split from the bodies
  alone. That is the strongest evidence in this log that the reading
  reads what it claims to.

## 3.3 The one refinement that came after its measurement

`clang/__eqtf2` has ONE `push %rbx` and TWO `pop %rbx`, one per return
path. A reading that walks the text in one line, not one path, takes
the second `pop` from an empty slot and calls `rbx` changed. The rule
therefore says: a family whose ARRIVAL value the body was seen parking
is restored by a `pop` this reading cannot place. Written into the
CORE with "Written into this CORE after the measurement that produced
it, which is the reverse of the binding order and is said so here."

---

# 4. The rebuild, and the per-population tallies

## 4.1 The three populations

LITERAL — the three run logs, `canon40_wrapped_run.log`,
`canon40_interp_run.log`, `canon40_regen_run.log`:

```
c       610 units  {"WRAPPED_TEXT_PROVED": 610}
cpp     770 units  {"WRAPPED_TEXT_PROVED": 770}
go      107 units  {"WRAPPED_TEXT_PROVED": 107}
rust    125 units  {"REFUSED": 2, "WRAPPED_TEXT_PROVED": 123}
swift   167 units  {"GATE_DISPROVED": 2, "REFUSED": 14, "WRAPPED_TEXT_PROVED": 151}
interp   11 units  {"REFUSED": 2, "WRAPPED_TEXT_PROVED": 9}
regen shards 326 of 326  {"GATE_DISPROVED": 110, "REFUSED": 624, "WRAPPED_TEXT_PROVED": 28554}
```

LITERAL — `audit78_printed.txt`:

```
units recorded: canon39 31078, canon40 31078

population / outcome                                  canon39  canon40
interpreter / REFUSED                                       2        2
interpreter / WRAPPED_TEXT_PROVED                           9        9
original / GATE_DISPROVED                                   0        2
original / REFUSED                                         16       16
original / WRAPPED_TEXT_PROVED                           1763     1761
regenerated / GATE_DISPROVED                                0      110
regenerated / REFUSED                                     628      624
regenerated / WRAPPED_TEXT_PROVED                       28660    28554

proved: canon39 30432, canon40 30324   not proved: canon39 646, canon40 754
```

| population | size | canon39 proved | canon40 proved | canon40 refused | canon40 disproved |
|---|---|---|---|---|---|
| original | 1,779 | 1,763 | **1,761** | 16 | 2 |
| interpreter | 11 | 9 | **9** | 2 | 0 |
| regenerated | 29,288 | 28,660 | **28,554** | 624 | 110 |
| **all** | **31,078** | **30,432** | **30,324** | **642** | **112** |

## 4.2 Every movement, with its computed cause

LITERAL — computed over `audit78.json`'s movement list:

```
112 ('WRAPPED_TEXT_PROVED', 'GATE_DISPROVED', 'DISPROVED')
4 ('REFUSED', 'WRAPPED_TEXT_PROVED', None)
disproved by language: {'swift': 112}
```

The third element is each unit's outcome in `regate64_store` — the
SAME canon39 units re-gated by task 64 with the CURRENT `reference.py`.

- **112 units, all swift, proved → disproved. The cause is task 64's
  reference, not this task**, and the proof is that the text the gate
  read did not change. LITERAL — `canon40_wrapped_text_identity.txt`:

```
THE WRAPPED TEXT, canon39 AGAINST canon40, OVER ALL 31,078
  identical wrapped text: 30432
  different wrapped text: 0  []
  wrapped in canon40 only (canon39 refused them): 4
```

  GLOSS: every one of the 30,432 units that had a wrapped text in
  canon39 has the BYTE-IDENTICAL text in canon40. canon39's verdicts
  were recorded on 2026-09-03 at 03:11, before task 64 changed
  `reference.py` at 13:19; task 64 re-gated the same units and already
  recorded all 112 as DISPROVED. So no unit loses proved status
  because of task 78: **zero regressions in the ruled sense**, with
  the named, proved cause being the reference change of task 64 and
  its record being `regate64_store`.

- **4 units, refused → proved**: `swift/regen_315`, `321`, `327`,
  `333`. Task 59 could not attach their callee (no swift archive on
  the host) and `canonical_form.unattached_runtime_callers()` refused
  them BY NAME. Task 63 extracted swift's archive inside the instance
  where swift lives, so those callees now have bodies and the refusal
  is answered. LITERAL — `audit78_printed.txt`:

```
  swift/regen_315   REFUSED -> WRAPPED_TEXT_PROVED
      the reference has no model for something this body spells (arch
      opcode 'jmp' is a census row ...), and the form applies
```

## 4.2a The new refusal path never fired

The corrected rule refuses a unit BY NAME where the attached callee's
answer cannot be read. LITERAL — canon40's 642 refusals, by their own
recorded cause:

```
  never returns        424
  no answer home       216
  no canonical text      2
```

GLOSS: all three causes are canon39's, unchanged in count except for
the four swift units that stopped being refused. "the attached callee's
answer register cannot be read" appears **0 times**, which agrees with
the readings: 76 of 76 bodies were read and none was refused.

## 4.3 The assembly, real, with its tallies

LITERAL — `canon40_assemble_run.log`:

```
offered 2722  assembled 2722  failed 0  ledger relocations 8914
```

against canon39's `offered 2728  assembled 2728  failed 0  ledger
relocations 8948`, over the SAME sample rule (whole original and
interpreter proved sets, plus every 30th regenerated proved unit —
stride 30, 952 sampled of 28,554 where canon39 sampled 956 of 28,660).
The 6-unit difference is exactly the 2 original and 4 regenerated
proved units the reference change removed from the proved set.

LITERAL — the head of `canon40_assemble_transcripts.txt`, `as --64`
then `objdump -d`, verbatim:

```
==== c/op_0   (from /tmp/canon_assemble_work/batch_0000.s)
0000000000000000 <u_c_op_0>:
   0:	48 8b 3d 00 00 00 00 	mov    0x0(%rip),%rdi        # 7 <u_c_op_0+0x7>
   7:	48 8b 3f             	mov    (%rdi),%rdi
   a:	31 c0                	xor    %eax,%eax
   c:	85 ff                	test   %edi,%edi
   e:	0f 94 c0             	sete   %al
  11:	4c 8b 1d 00 00 00 00 	mov    0x0(%rip),%r11        # 18 <u_c_op_0+0x18>
  18:	41 88 03             	mov    %al,(%r11)
  1b:	c3                   	ret
```

---

# 5. THE 2,862 — the expectation, tested

## 5.1 What was measured

LITERAL — `audit78_printed.txt`:

```
THE 2,862, TESTED RATHER THAN ASSUMED
  the measurement of log_168 §5.3, recomputed: a unit whose body
  transfers into a routine one of this machine's archives DEFINES, and
  whose ledger carries NO row naming that routine.
  canon39  units transferring into an archive-defined routine:   3923
           of those with NO row naming it:   3619   runtime_callee rows:     608
  canon40  units transferring into an archive-defined routine:   3927
           of those with NO row naming it:      0   runtime_callee rows:   49362
  units that had NO runtime row in canon39 and carry one in canon40: 3623
```

GLOSS, and the number is not 2,862 for a reason worth stating.
log_168's 2,862 counted the units whose STORED TERM was disproved
because of the missing row (2,860 undecided→disproved plus 2
no-term→disproved). The population that CARRIES the defect is larger:
**3,619 of canon39's 31,078 units** transfer into a routine an archive
defines and carry no row naming it. The 2,862 are the subset that had
a term for the reference to disprove.

**In canon40 that population is 0.** Every unit that transfers into an
archive-defined routine now carries at least one row naming it, and
3,623 units gained a row that had none (3,619 plus the 4 swift units
canon39 refused outright). `runtime_callee` rows over the whole
31,078 go from **608 to 49,362**.

## 5.2 One unit, before and after

LITERAL — `acceptance78_printed.txt`, part 2, `c/regen_1056`, whose
answer home IS `%xmm0`:

```
LITERAL -- canon39, c/regen_1056
    outcome:        WRAPPED_TEXT_PROVED
    result_family:  xmm0
    runtime rows:   0
    OUT-0 produced_by: {"kind": "arch_opcode", "mnem": "addss"}

LITERAL -- canon40, c/regen_1056
    outcome:        WRAPPED_TEXT_PROVED
    result_family:  xmm0
    runtime rows:   13
      TEMP-5   __extendhfsf2   register %xmm0
      TEMP-9   __truncsfhf2    register %xmm0
      ...
    OUT-0 produced_by: {"callee": "__truncsfhf2", "kind": "runtime_callee"}
```

GLOSS: canon39 said this unit's answer was the `addss` BEFORE the
transfer — the transfer changed nothing. canon40 says it is what
`__truncsfhf2` left in `%xmm0`. That is exactly the assertion log_168
said the reference rightly disproves.

## 5.3 The term route belongs to task 83, and this is said plainly

**This task did not re-run the term route.** `term.relink` checks its
re-run against the stored ledger row for row, so the term store must
be rebuilt over canon40 rather than patched, and log_183 gives that to
TASK 83 by name ("term66 / name_census7 / the_pool6 … over the newest
canon"). What this log can say is the input side: the rows the term
route reads are now present for 3,927 units where 3,619 of them
carried none. **Whether the 2,862 stop being disproved is task 83's
measurement, not this one's**, and no claim is made about it here.

---

# 6. The 196 panic-path callers, named

## 6.1 The two shapes, and the criterion that separates them

Written into `CORE_0_3_5_1_8_runtime_callee.md` before the code:

| what the caller's own text shows | name |
|---|---|
| NOTHING follows the transfer on its own path — the body ends, or the next line defines a label that is NOT the transfer's own return point | **guard exit** |
| an instruction of the same block follows, OR the label the transfer itself names does | **unread runtime routine** |

Neither makes a ledger row. Each is recorded on the unit as a typed
object in `transfer_shapes`.

## 6.2 The criterion's first version was WRONG, and how it was caught

An unlinked `call` disassembles as a transfer to its own next address,
so ruling 4's label pass writes `call L0` with `L0:` on the very next
instruction. "A label follows" is therefore what a RETURNING call looks
like in this corpus. The first criterion said only "the next line is a
label definition or the body ends", and it filed `c/regen_1075` under
guard exits:

LITERAL — `c/regen_1075`, its body:

```
    push %rax
    movss %xmm0,0x4(%rsp)
    call L0 !!reloc=R_X86_64_PLT32:__floattihf-0x4
    L0:
    call L1 !!reloc=R_X86_64_PLT32:__extendhfsf2-0x4
    ...
```

GLOSS: the routine plainly comes back — four more instructions use the
answer. Caught by reading the unit before reporting the rule; the
return-point clause was added, the render redone, and the CORE
records the mistake rather than hiding it.

## 6.3 The census

LITERAL — `audit78_printed.txt`:

```
  guard_exit                     180 units
  unread_runtime_routine         108 units
     guard_exit                   go     150
     guard_exit                   rust   30
     unread_runtime_routine       c      40
     unread_runtime_routine       cpp    48
     unread_runtime_routine       go     20
  by routine name (call lines, not units):
     guard_exit    ...panic_const23panic_const_div_by_zero    15
     guard_exit    ...panic_const23panic_const_rem_by_zero    15
     guard_exit    ...panic_const24panic_const_div_overflow    8
     guard_exit    ...panic_const24panic_const_rem_overflow    8
     guard_exit    runtime_panicdivide                        28
     guard_exit    runtime_panicshift                        122
     unread_runtime_routine  __floattihf                      44
     unread_runtime_routine  __floatuntihf                    44
     unread_runtime_routine  runtime_morestack_noctxt_abi0    20
     unread_runtime_routine  runtime_newobject                20
```

GLOSS, on why 288 and not 196. Task 63 counted UNITS WITH NO
ATTACHMENT AT ALL (go 170, rust 26). Task 78 counts TRANSFERS, so 88
c and cpp units appear that task 63 counted as attached: they transfer
into `__extendhfsf2` (attached) AND into `__floattihf` or
`__floatuntihf`, which no builtins archive on this machine defines.
Measured: all 88 carry attached runtime rows beside the unread
transfer, which is precisely what made them invisible to a per-unit
count.

## 6.4 The instance of each shape

LITERAL — `acceptance78_printed.txt`, part 3, `go/op_103`:

```
    cmp $0xffffffffffffffff,%rbx
    jne L0
    ...
    L2:
    nopl (%rax)
    call x_runtime_panicdivide
    nop
```

and part 4, `go/op_30`:

```
    lea 0x6d27(%rip),%rax
    call x_runtime_newobject
    mov 0x20(%rsp),%ecx
    mov %ecx,(%rax)
```

GLOSS: the first transfer has nothing after it — no continuation was
emitted. The second is followed by two instructions that READ `%rax`,
so the routine comes back and leaves a value; no archive index defines
it, so the ledger names the shape and writes no row rather than
guessing one.

---

# 7. FLAGGED FOR DEE — what a go or rust panic path IS

log_183's closing line reserves this decision ("what a go or rust panic
path IS in the ledger's vocabulary (task 78 flags it)"). Three options
were open; the CORE records all three and the first is implemented, so
switching costs one place:

1. **IMPLEMENTED — the two named notes**, `guard_exit` and
   `unread_runtime_routine`, making no row and refusing no unit.
   Nothing that proves today stops proving. A guard exit is the
   RESPONSE half of a guard in the ratified mode-row vocabulary ("a
   branch leading to a trap or a panic call", AgentMemory), not a
   producer.
2. **A fifth producer KIND**, beside `arch_opcode`, `flag_pair`,
   `non_opcode_phrase` and `runtime_callee`. It would put a row on the
   ledger with no body behind it — for the 108 returning transfers
   that is at least truthful about "something changed here", and for
   the 180 guard exits it would name a value that never exists.
3. **Extract go's and rust's own runtime** the way the builtins
   archives are extracted. the owner's ruling "if the compiler is importing
   something as a standard feature, also not a library call" can be
   read as reaching these. If it does, the 108 returning callers
   become ordinary attachments and the 180 guard exits stay guard
   exits. This is the only option that would put a READ row where
   `go/op_30` today has silence, and `go/op_30`'s `%rax` answer is
   demonstrably the routine's, not the `lea` before it.

Not decided here. The names `guard_exit` and `unread_runtime_routine`
are working names and are changeable in `ledger.Ledger.record_transfer_shape`.

---

# 8. The guards

## 8.1 The spelling guard, unmodified, one process

LITERAL — the command and the transcript's ends
(`guard78_transcript.txt`):

```
$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py \
      canon40_wrapped_*.json canon40_interp.json canon40_assemble.json \
      canon40_regen_store/*.json runtime_answers78.json audit78.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS canon40_wrapped_c.json -- no operator token in any key, grouping, pairing or row structure
...
PASS audit78.json -- no operator token in any key, grouping, pairing or row structure

$ grep -c "^PASS" guard78_transcript.txt
335
$ grep -c FAIL guard78_transcript.txt
0
$ grep -c exempt guard78_transcript.txt
0
```

335 artifacts in ONE process, exit 0. The guard is unmodified:

```
$ sha256sum check_no_spelling_keys.py
a377462b38e8610d8bb60ac668f0a5adc72ee571d15efab85e40a9afdaa511f7
$ git status --porcelain Research/op_pipeline/check_no_spelling_keys.py
(no output)
```

## 8.2 No role keys, no field whitelists

The one shape added to an artifact is `transfer_shapes`, a list of
typed objects `{"kind": ..., "callee": ..., "why": ...}` — the same
shape the producer objects carry, which is why the guard reads it as
machine form. No key was exempted and no field was whitelisted.

## 8.3 The memory bound

STATED BEFORE THE RUN: 6 GB hard cap, named abort
`AUDIT78_MEMORY_ABORT` in `audit78.py` (checked after every file), and
the renders hold one shard at a time by construction. SAMPLED FIRST:
the original population (1,779 units) was rendered before the
regenerated one. MEASURED, `/usr/bin/time -v`:

```
canon40_wrapped_time.txt:  Maximum resident set size (kbytes): 96292
canon40_interp_time.txt:   Maximum resident set size (kbytes): 60160
canon40_regen_time.txt:    Maximum resident set size (kbytes): 94936
audit78_time.txt:          Maximum resident set size (kbytes): 160324
```

Peak across the task: **160 MB**, 2.6% of the stated cap. The abort
was never reached.

---

# 9. Two things about the machine, recorded because they affect reading

## 9.1 The venv was rebuilt

`/tmp/reconnect_venv` did not exist at session start (and vanished a
second time mid-session). It was rebuilt from the anaconda python with
`--system-site-packages`, and `pyvex` and `capstone` were installed:

```
$ /tmp/reconnect_venv/bin/python3 -c "import pyvex,z3,capstone; ..."
3.13.9 | packaged by Anaconda, Inc.
pyvex True z3 ok capstone 5.0.7
$ z3.get_version_string() -> 5.1.0
```

pyvex 9.3.4, z3 5.1.0, capstone 5.0.7 — the same versions log_146 and
log_147 recorded, so no version drift.

## 9.2 WHICH `ledger.py` canon40 WAS BUILT FROM

The coordinator noted that task 80's render_back run read `ledger.py`
mid-edit. For task 83's benefit, stated plainly:

```
$ sha256sum ledger.py
90d05e6b0b086b2125f8743684c4c67c1201e0c63cf78f6d1ceeb49031da2c6f
```

recorded on disk as `canon40_build_ledger_sha256.txt`. **Every canon40
artifact in this log was rendered from that exact file**, in one run
per population after the last edit; the two earlier renders (from
`45d27e4e…` and `12dae4dd…`) were discarded and re-run, not merged.
The three renders agreed on every outcome — the classifier fix of §6.2
changes only the recorded note, never a row and never a verdict — but
the artifacts on disk are the last render alone.

The other three live modules were NOT edited by this task:
`reference.py` `96414ecb…`, `gate.py` `c68090b9…` (both as task 64
left them, 13:19), `canonical_form.py` `a30c80c9…` (edited by this
task; §10 lists what changed).

---

# 10. File inventory

## 10.1 Plan tree — CORE and PROGRESS

| file | what changed |
|---|---|
| `Planning/.../node_0_3_5_3_ledger/node_0_3_5_3_3_destination_rules/CORE_0_3_5_3_3_destination_rules.md` | `## design` rule 4 rewritten with its superseded wording kept beside it; new settled rule "THE ANSWER REGISTERS ARE READ OFF THE ATTACHED CALLEE'S BODY" (six steps); new settled rule pointing the panic paths at the runtime_callee node; four realization rows |
| `Planning/.../node_0_3_5_3_ledger/node_0_3_5_3_3_destination_rules/PROGRESS.md` | two entries: the rule rewritten before the code, and the rule realized with its measurement |
| `Planning/.../node_0_3_5_1_arch_unit/node_0_3_5_1_8_runtime_callee/CORE_0_3_5_1_8_runtime_callee.md` | new settled rule "WHAT A GO OR RUST PANIC PATH IS IN THE LEDGER'S VOCABULARY" with the two shapes, the return-point clause and its own correction record, and the three options flagged for the owner; the "writes the accumulator" settled rule superseded in place; a "what task 78 added" realization table |
| `Planning/.../node_0_3_5_1_arch_unit/node_0_3_5_1_8_runtime_callee/PROGRESS.md` | two entries: the shapes named before the code, and the shapes realized with the census and the wrong-criterion record |

## 10.2 Code — the live modules extended

| file | what changed |
|---|---|
| `Research/op_pipeline/ledger.py` | `RUNTIME_TRANSFER_RULE` rewritten (with `superseded_wording`); `ANSWER_EXCLUDED`, `MOVE_LIKE`, `X87_PUSHERS`, `X87_POPPERS`, `RETURN_STEMS`, `POSITIONAL_LABEL`, `_memory_slot`, `answer_registers_of_body`, `answer_row_half` added; `Ledger.__init__` takes `runtime_answers` and `toolchain`; `Ledger.runtime_answer` and `Ledger.record_transfer_shape` added; the walk's runtime branch writes one row per family (plus an X87 row where the callee answers there) and refuses by name where a reading cannot be made; `wrap_unit` passes the new arguments through |
| `Research/op_pipeline/canonical_form.py` | `PREFIX` + `out_path` + `--prefix` (canon39 stays the default, canon40 is this task's render); `TOOLCHAIN_OF_LANGUAGE`; `runtime_answer_readings`; `runtime_routine_names` reads the 33 archive-defined names from the readings; `unattached_runtime_callers` no longer refuses a caller whose callee now has a body; `CanonicalForm.__init__`/`wrap` carry `runtime_answers` and `toolchain`; `transfer_shapes` carried on every record |
| `Research/op_pipeline/reference.py`, `gate.py` | **not edited** |

## 10.3 New files

| file | what it is |
|---|---|
| `Research/op_pipeline/runtime_answers78.py` | the driver that applies the reading to the 76 callee bodies |
| `Research/op_pipeline/runtime_answers78.json` | the 76 readings, per `toolchain/name` |
| `Research/op_pipeline/runtime_answers78_printed.txt` | its transcript, all 76 rows |
| `Research/op_pipeline/audit78.py`, `audit78.json`, `audit78_printed.txt`, `audit78_run.log`, `audit78_time.txt` | canon40 against canon39, the movements, the 2,862 tested, the 196 census |
| `Research/op_pipeline/acceptance78.py`, `acceptance78_printed.txt` | the five printed parts of §3, §5.2 and §6.4 |
| `Research/op_pipeline/guard78_transcript.txt` | the unmodified guard over 335 artifacts |
| `Research/op_pipeline/canon40_wrapped_{c,cpp,go,rust,swift}.json` | the original population, rendered and gated |
| `Research/op_pipeline/canon40_interp.json` | the interpreter population |
| `Research/op_pipeline/canon40_regen_store/` (326 shards), `canon40_regen_state.json` | the regenerated population |
| `Research/op_pipeline/canon40_assemble.json`, `canon40_assemble_transcripts.txt` | 2,722 assembled, 0 failed |
| `Research/op_pipeline/canon40_wrapped_text_identity.txt` | the byte-identity check of §4.2 |
| `Research/op_pipeline/canon40_build_ledger_sha256.txt` | which `ledger.py` built canon40 |
| `Research/op_pipeline/canon40_*_run.log`, `canon40_*_time.txt` | the run logs and `/usr/bin/time -v` reports |

Nothing superseded was edited or imported: `ledger47.py`, `ledger48.py`,
`canon3*_*.py`, `gate48.py` and `layer4*.py` are untouched, and
`canonical_form.py` imports only `ledger`, `gate`, `canon`.

---

# 11. Resume state

**Nothing is left half-done, and no checkpoint is owed.** All three
populations are complete on disk and were rendered from one
`ledger.py`:

| population | size | state | file |
|---|---|---|---|
| original | 1,779 | COMPLETE | `canon40_wrapped_{c,cpp,go,rust,swift}.json` |
| interpreter | 11 | COMPLETE | `canon40_interp.json` |
| regenerated | 29,288 | COMPLETE, 326 of 326 shards | `canon40_regen_store/`, `canon40_regen_state.json` |
| assembly sample | 2,722 | COMPLETE, 0 failed | `canon40_assemble.json` |
| audit, acceptance, guard | — | COMPLETE | `audit78_printed.txt`, `acceptance78_printed.txt`, `guard78_transcript.txt` |

If a later lap must resume a partial render, `canonical_form.py
--population regenerated --prefix canon40` (without `--fresh`) skips
every shard named in `canon40_regen_state.json`, and the original
population skips every label already in its language file.

WHAT IS OWED, and to whom:

- **TASK 83** re-runs the term route and the pool over canon40. Its
  input changed materially: 3,623 units gained runtime rows and there
  are 49,362 `runtime_callee` rows where there were 608. Read
  `canon40_*`, not `canon39_*`, and note that 112 swift units are
  disproved on the wrapped route (all 112 already disproved by task
  64's reference).
- **TASK 80** is owed a re-run of `render_back` against this
  `ledger.py` (`90d05e6b…`), per the coordinator's note.
- **DEE** is owed the naming decision of §7.
