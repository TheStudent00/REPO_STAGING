# log_112 — TASK 26, the two-unit new bucket and the corrected remainder

**Role:** Claude Code implementer, TASK 26 of
`log_109_claude_code_task_briefs_round5.md`. Date: 2026-09-01. No
sub-agents used — every artifact below was built and run directly in
this session with `/tmp/reconnect_venv/bin/python3`.

**Evidence class is stated per claim.** Every "I verified X" sentence
below pastes the command and its output, per the round-5 rule.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line — not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention — never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 — the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

---

## 0. the headline, in plain words

Three things happened this lap, and the third is the important one.

- **The 2-unit bucket is diagnosed and is really a 5-unit family.**
  "The answer value never entered a tracked register" means the
  answer is a byte image at an address the CALLER passed in; the
  register the canonical form calls `a` is carrying that address
  instead. Three units in the neighbouring "read before defined"
  bucket have the same cause with a different symptom. Rendering
  these needs an exit contract the ratified canonical form does not
  have — **named, evidenced, and left to the owner.**
- **The float family was worked, and 74 units converged.** The cause
  was NOT what log_105 recorded (a canon17_float register-allocation
  gap): the candidate text already exists on the records. The gate
  was the blocker — no name→z3 entry for the SIMD float ops. Fixed
  by table, in a wrapper, exactly as AgentMemory says.
- **A CIRCULAR GATE was found and is the most consequential finding
  of the lap.** `canon4.py` assigns the same list object to `blocks`
  and to `derived_blocks`. Every gate that treated `blocks` as ground
  truth compared a text with itself. That includes round 4's
  branching acceptances. Re-gated honestly against blocks cut from
  the units' own ship BYTES: **13 of the 1,561 baseline are
  withdrawn** (11 swift, 2 go, all DISPROVED with counterexamples),
  and 42 float branching units that would otherwise have been
  reported as converged are honestly DISPROVED instead.

**Converged: recorded 1,635 (+74 from 1,561); honest standing 1,622
(+61) after the 13 withdrawals.** Both numbers are computed from disk
and pasted in §5.

---

## 1. what I read first

`~/Programming/PseudoCoupHQ/AgentMemory.md` in full;
`~/Programming/DevComms/LLM_communication_protocol.md` (this is the
v2 refactor — its own first line reads "# Communication Protocol, v2";
**named honestly: the path `LLM_communication_protocol_v2.md` that the
brief and AgentMemory both give DOES NOT EXIST on disk**, verified:

```
$ ls ~/Programming/DevComms/ | grep -i protocol
LLM_communication_protocol.md
proposal_2026-08-01_communication_protocol.md
```

so the v2 content lives at the unsuffixed path and AgentMemory's
pointer is stale by one filename); `log_109` (TASK 26);
`log_105` including its appended 2026-09-01 correction note;
`log_110`; `log_099`; `PseudoCoupHQ/CLAUDE.md`.

---

## 2. PART ONE — the 2-unit bucket, diagnosed

### 2.1 the two units, read off disk

Evidence class: **tool testimony, reproducible.**

```
$ /tmp/reconnect_venv/bin/python3 -c "
import json
d4=json.load(open('canon4_units_rust.json'))['units']
for k in ['807','814']:
    r=d4[k]
    print('=====',k)
    for f,v in r.items(): print('  ',f,'=',json.dumps(v)[:2000])
"
===== 807
   unit = "rust/op_807"
   meta = {..., "lhs_type": "f32", "rhs_type": "f32",
           "result_type": "core::ops::RangeInclusive<f32>", ...}
   mnem = ["mov %rdi,%rax", "movss %xmm0,(%rdi)",
           "movss %xmm1,0x4(%rdi)", "movb $0x0,0x8(%rdi)", "ret"]
   bytes = "48 89 f8 f3 0f 11 07 f3 0f 11 4f 04 c6 47 08 00 c3"
   erasure = "ok"
   entry_contract = {"a": "xmm0", "b": "xmm1", "result": "rax"}
   erased_form = ["mem = movss(a)", "mem = movss(b)", "mem = movb(_)"]
   derive_refused = "erasure_refused: the answer value never entered
       a tracked register (a passthrough this builder does not model)"
===== 814
   mnem = ["mov %rdi,%rax", "movsd %xmm0,(%rdi)",
           "movsd %xmm1,0x8(%rdi)", "movb $0x0,0x10(%rdi)", "ret"]
   entry_contract = {"a": "xmm0", "b": "xmm1", "result": "rax"}
   derive_refused = (same text)
```

### 2.2 what it means mechanically

The unit never computes anything into a register. It writes three
fields — the two operands and a one-byte flag — through a pointer
that arrives in `%rdi`, and returns that same pointer in `%rax`. That
is the x86-64 System V **memory-return** rule: an answer too large
for the return registers is written into space the CALLER allocated,
whose address arrives as a hidden first argument, and the declared
arguments shift one register to the right.

So `%rax` at return holds an ADDRESS, not the answer; and `%rdi`,
which the canonical form reserves for `a`, is holding the
destination.

### 2.3 the proof is forced by construction, not read off a manual

The corpus contains the same intention at four answer sizes, from one
compiler in one run. The register roles change with the SIZE and
nothing else (evidence class: **forced by construction** — the only
assumption is the standing one, that the compiler compiled the
program we wrote):

| unit | answer size | ship code | status |
|---|---|---|---|
| rust/op_821 | 3 bytes | `shl $0x8,%esi ; lea (%rsi,%rdi,1),%eax ; ret` | converged |
| rust/op_721 | 16 bytes | `mov %rsi,%rdx ; mov %rdi,%rax ; ret` | converged |
| rust/op_793 | 24 bytes | `mov %rdi,%rax ; mov %rsi,(%rdi) ; mov %rdx,0x8(%rdi) ; movb $0x0,0x10(%rdi) ; ret` | refused |
| rust/op_814 | 24 bytes, float operands | `mov %rdi,%rax ; movsd %xmm0,(%rdi) ; movsd %xmm1,0x8(%rdi) ; movb $0x0,0x10(%rdi) ; ret` | refused |

op_721 and op_793 differ in nothing but how many bytes the answer
occupies, and op_721 keeps `a` in `%rdi` while op_793 does not.

### 2.4 the second symptom is the same cause — the bucket is 5, not 2

Three of the four units in the "value w0 is read before it is defined
or before the unit's entry contract names it" bucket are op_786,
op_793 and op_800 — the integer members of this same family:

```
$ /tmp/reconnect_venv/bin/python3 -c "
import json
d4=json.load(open('canon4_units_rust.json'))['units']
for k,r in d4.items():
    if 'read before it is defined' in str(r.get('derive_refused')):
        print(k, r.get('meta',{}).get('result_type'), '|',
              r.get('entry_contract'), '|', r.get('erased_form'))
"
786 core::ops::RangeInclusive<i32> | {'a': 'rdi', 'b': 'rsi', 'result': 'rax'} | ['mem = mov(b)', 'mem = mov(w0)', 'mem = movb(_)']
793 core::ops::RangeInclusive<i64> | {'a': 'rdi', 'b': 'rsi', 'result': 'rax'} | ['mem = mov(b)', 'mem = mov(w0)', 'mem = movb(_)']
800 core::ops::RangeInclusive<u64> | {'a': 'rdi', 'b': 'rsi', 'result': 'rax'} | ['mem = mov(b)', 'mem = mov(w0)', 'mem = movb(_)']
```

**A machine-fact defect, named:** the `entry_contract` on these three
records says `a` is in `%rdi`. That is FACTUALLY WRONG for these
units — `%rdi` holds the destination address, `a` is in `%rsi` and
`b` is in `%rdx`. The builder then read `%rdx`, which its own wrong
contract never named, and refused "read before defined". One cause,
two refusal texts, five units.

### 2.5 the family, recovered by a machine-form shape test

`diag_caller_destination.py` (new) joins a unit to this family when
its own ship text satisfies both: the first instruction copies an
incoming register into `%rax`, AND every store writes through that
same register as base. No operator token, no result-type name, no
source expression takes part. Run (evidence class: **tool testimony,
reproducible**):

```
$ /tmp/reconnect_venv/bin/python3 diag_caller_destination.py
wrote diag_caller_destination.json -- 5 members
   rust/786     dest=%rdi  offsets=[0, 4, 8]  refusal="erasure_refused: value w0 is read before it is defined or before the unit's entry contract names it"
   rust/793     dest=%rdi  offsets=[0, 8, 16]  refusal="erasure_refused: value w0 is read before it is defined or before the unit's entry contract names it"
   rust/800     dest=%rdi  offsets=[0, 8, 16]  refusal="erasure_refused: value w0 is read before it is defined or before the unit's entry contract names it"
   rust/807     dest=%rdi  offsets=[0, 4, 8]  refusal='erasure_refused: the answer value never entered a tracked register (a passthrough this builder does not model)'
   rust/814     dest=%rdi  offsets=[0, 8, 16]  refusal='erasure_refused: the answer value never entered a tracked register (a passthrough this builder does not model)'
```

The shape test is discriminating, not vacuous: c has 52 units and cpp
66 whose first instruction is also `mov %rdi,%rax`, and none of them
joins, because none stores through `%rdi`.

### 2.6 the disposition — DEE-RESERVED, with the question named

The ratified canonical runnable form names three homes (`a` → `%rdi`,
`b` → `%rsi`, answer → `%rax` / `%xmm0`) and the canonical record is
the move-erased form PLUS the **entry contract** — where each value
must arrive. These five units have an answer that never occupies a
register. Rendering them needs two things that form does not have:

1. **a name and a designated register for the incoming DESTINATION
   ADDRESS**, which also displaces `a` and `b` from their designated
   registers whenever it is present; and
2. **an EXIT CONTRACT** — the dual of the entry contract — stating
   that the answer is the N-byte image at that address, at stated
   offsets, rather than a value in a register.

Both are ontology: a new traced name, a new register-assignment rule,
and a new half of the canonical record. AgentMemory's standing ruling
is "the owner decides architecture, ontology, naming. Flag, don't decide."
**So it is flagged, with the evidence above, and not invented.** The
artifact `diag_caller_destination.json` carries the five members,
their destination register, their store offsets, their declared
(wrong) entry contracts and their ship text.

---

## 3. PART TWO — re-deriving the plan from the CORRECTED accounting

log_105's "model next round" recommendation attached to the void
19-unit row is dead. Re-derived from the corrected counts, the
buckets recommended "model" and their sizes:

| bucket | corrected size | tractability judged this lap |
|---|---|---|
| float family (`*F0x*` lifter names) | **120** | largest; and the blocker turned out to be a table, not surgery |
| `no_canon4_text`: two stack-spilled operands | 22 | canon4 erasure stage, shared file, deferred |
| `no_canon4_text`: branch target unresolved | 16 | canon4 erasure stage, deferred |
| `no_canon4_text`: too many join paths | 6 | blocker unchanged, deferred |
| `no_canon4_text`: read before defined | 4 | 3 of 4 are §2's family → the owner-reserved |
| `no_canon4_text`: answer never in a tracked register | 2 | §2's family → the owner-reserved |

**Choice, stated: the float family**, by size and because the honest
diagnosis (below) showed it was a table gap, not the shared-file
surgery log_105 predicted.

The population is 120, counted from disk by machine-form key — the
pipeline's own `status`, and the VEX lifter names in each unit's own
`normal_path_raw` (no operator token participates):

```
$ /tmp/reconnect_venv/bin/python3 -c "... census27.names_from_raw over tree_units3.json ..."
float pop 120
```

### 3.1 log_105's stated root cause does not survive contact with the records

log_105 recorded: "the float-operand classifier (`_operand_xmm`) only
knows a/b/zero; every blocked unit carries a NESTED EXPRESSION as one
operand, needing fresh register-allocation logic ... in
`canon17_float.py`". Measured this lap:

```
$ ... counting candidate availability over the 120 ...
Counter({('cpp','derived_text'): 38, ('c','derived_text'): 36,
         ('cpp','derived_blocks'): 22, ('c','derived_blocks'): 20,
         ('cpp','NONE'): 4})
```

**116 of the 120 already carry a rendered candidate.** The rendering
is not missing. And each unit says what IS missing, in its own words
— e.g. c/op_141:

```
   u.reason = "no return path: expression contains an uninterpreted
               atom for VEX op 'Sub32F0x4' -- SIMD packed-float sub
               (not modeled)"
```

That is the name→z3 translation table, which is exactly the limit
AgentMemory already records: *"The lifter was measured NOT to be the
limiting factor ... the limit was our own name->z3 translation table.
Fix tables, not tools."*

### 3.2 the fix — `canon10_behaviour_check.Sim10`, a wrapper

`Sim10` subclasses `canon9_behaviour_check.Sim9` (→ Sim8 → Sim7 →
ExtSim → Sim). `canon5..canon9_behaviour_check.py` are UNCHANGED and
imported by reference only. What it adds:

- **128-bit XMM state**, seeded through the same `shared_seed` both
  simulations share.
- **Float operations as UNINTERPRETED FUNCTIONS over bitvectors.**
  `addss` is `FADD32(x,y) -> 32 bits`, about which nothing is
  assumed. Two texts prove equal only if they agree for EVERY
  interpretation, and IEEE-754 is one such interpretation — so a
  proof here holds of the real machine. Deliberately incomplete: no
  float algebra is available, and none is wanted (float addition is
  not associative; an "optimization" resting on that would be a bug
  we must not prove away).
- **Everything that is not float arithmetic modeled exactly**: lane
  structure (`punpckldq`, `unpckhpd`), 128-bit copies
  (`movaps`/`movapd`), the low-lane merge rule of the `ss`/`sd`
  forms, the zero-extension rules of `movq`/`movd`, packed `subpd`,
  the `cmpeqss`/`cmpneqss` lane masks, and literal-keyed stack spill
  and reload.
- **The float flag rule.** `ucomiss`/`ucomisd` set three
  uninterpreted predicates and the flags follow the hardware's own
  rule: `ZF = FUNORD ∨ FEQ`, `PF = FUNORD`, `CF = FUNORD ∨ FLT`; then
  `seta = ¬CF ∧ ¬ZF`, `setae = ¬CF`, `setne = ¬ZF`, `setp = PF`. No
  constraint tying the three predicates together is asserted —
  omitting them can only make the solver weaker, never unsound.
- **The answer home read off the GROUND TRUTH.** canon4's own
  `entry_contract["result"]` is unusable here and this is measured,
  not assumed: c/op_117, c/op_118 and c/op_189 all declare `"rax"`
  while their real ship code's last write is plainly `addss`/`addsd`/
  `mulss` into `%xmm0`. So the home is the last instruction of the
  REAL text writing `%xmm0` or an rax-family register, and the width
  is that instruction's own operand-size spelling. This is what makes
  a candidate's extra dead write harmless (c/op_117's candidate ends
  `... addss %xmm2,%xmm0; mov %edi,%eax; ret`; the real code never
  writes `%eax`).
- **A mechanical guard on rip-relative constants.** The real text
  spells a constant-pool load `punpckldq 0x0(%rip),%xmm1
  !!reloc=R_X86_64_PC32:.LCPI0_0-0x4`; the candidate drops the reloc.
  So the k-th rip read in each text gets the k-th fresh constant
  symbol, and the unit is refused UNDECIDED unless the two texts'
  ordered lists of rip-bearing mnemonics are identical.

### 3.3 first run, and one cause fixed at first observation

```
$ /tmp/reconnect_venv/bin/python3 canon30.py
TOTAL: {'attempted': 116, 'accepted': 84, 'attempted_not_proved': 32,
        'disproved': 0, ...}
```

All 32 refusals were ONE cause, counted:

```
32 | setcc with no preceding cmp/test in this text -- flags carried in from outside this sequence, not modeled | ['c/549','c/550','c/554','c/560']
```

The inherited `ExtSim` `setcc`/`cmovcc` handlers look only at the
INTEGER `last_cmp`. A `setcc` after a `ucomiss` must read the float
flags. Fixed in `Sim10` at first observation (AgentMemory's rule), and
re-run:

```
$ /tmp/reconnect_venv/bin/python3 canon30.py
TOTAL: {'attempted': 116, 'accepted': 116, 'attempted_not_proved': 0,
        'disproved': 0, ...}
```

**116 of 116 — and that is exactly where I stopped believing it.**

---

## 4. THE CIRCULAR GATE — the finding of the lap

### 4.1 how it surfaced

A gate that proves everything it is shown is indistinguishable from a
gate that is not looking. `canon30_negative_control.py` (new) mutates
each accepted candidate in a way that must change the answer and
re-runs the identical gate:

```
$ /tmp/reconnect_venv/bin/python3 canon30_negative_control.py
negative control tally: {'mutations_applied': 322,
  'mutations_not_applicable': 26, 'mutations_rejected_by_gate': 270,
  'mutations_still_proved_equal': 52, 'units_tested': 116}
MUTATIONS THE GATE FAILED TO REJECT: ... 52 ...
```

52 undetected mutations, all on branching units. Following them found
the cause.

### 4.2 the cause, forced by canon4.py's own source

`canon4.py`, its own lines 772–777:

```
    out["erasure"] = "ok"
    out["entry_contract"] = contract
    out["blocks"] = block_records
    out["erased_form"] = erased_flat
    out["derived_blocks"] = block_records
```

`blocks` and `derived_blocks` are **the same list object** — both are
the DERIVED, register-renamed rendering. `blocks` is not ground truth
and never was. Confirmed across the whole corpus (evidence class:
**tool testimony, reproducible**):

```
$ /tmp/reconnect_venv/bin/python3 -c "
import json
same=diff=0
for L in ['c','cpp','go','rust','swift']:
    d=json.load(open('canon4_units_%s.json'%L))['units']
    for k,r in d.items():
        b=r.get('blocks'); db=r.get('derived_blocks')
        if not b or not db: continue
        if json.dumps(b)==json.dumps(db): same+=1
        else: diff+=1
print('identical blocks/derived_blocks:',same,'differing:',diff)"
identical blocks/derived_blocks: 88 differing: 0
```

**88 of 88 identical, 0 differ.** So
`canon9_behaviour_check.anchored_check_branching`, which reads
`blocks` as the real side and `derived_blocks` as the candidate,
compares a text with itself. Round 4's branching acceptances rest on
it, and so did canon30's branching half.

### 4.3 the repair — real blocks cut from the unit's own ship bytes

`real_blocks.py` (new) disassembles the unit's own ship bytes
(`op_units_<lang>.json`'s `probes[n]["ship"]["bytes"]`) with capstone
**only to learn each instruction's offset and length**; the block
step text is objdump's own AT&T strings, so no second spelling
convention enters the pipeline. Leaders are offset 0, every branch
target, and the instruction after every branch; block order is
ascending offset — the real compiled order the fall-through rule
needs. A target that is not the first byte of a decoded instruction
is a refusal by name, never a guess. Branch operands are resolved
through objdump's own symbol-relative form (`<op_549+0xc>`,
`<main.op_96+0x18>`), so a slice taken from a linked binary cuts
exactly like one based at zero.

Worked instance — c/op_549, real versus candidate:

```
REAL (cut from the unit's own ship bytes)
   R0  ['test %rdi,%rdi', 'js Rc']
   R5  ['cvtsi2ss %rdi,%xmm1', 'jmp R21']
   Rc  ['mov %rdi,%rax', 'shr $1,%rax', 'and $0x1,%edi',
        'or %rax,%rdi', 'cvtsi2ss %rdi,%xmm1', 'addss %xmm1,%xmm1']
   R21 ['xor %eax,%eax', 'ucomiss %xmm0,%xmm1', 'seta %al', 'ret']

CANDIDATE (canon4's derived_blocks)
   L0     ['test %rdi,%rdi', 'js L2', 'jmp L1']
   L2     ['shr $1,%rdi', 'and $0x1,%edi', 'or %rdi,%rdi',
           'cvtsi2ss %rdi,%xmm2', 'addss %xmm2,%xmm2']
   L1     ['cvtsi2ss %rdi,%xmm3', 'jmp L3_p1']
   L3     ['xor %r10d,%r10d', 'ucomiss %xmm0,%xmm2', 'seta %r10b',
           'mov %r10d,%eax', 'ret']
   L3_p1  ['xor %r11d,%r11d', 'ucomiss %xmm0,%xmm3', 'seta %r11b',
           'mov %r11d,%eax', 'ret']
```

Two defects visible in the candidate, both real: the real code keeps
the shifted value in `%rax` and ANDs into `%edi` separately, while the
candidate does `shr $1,%rdi` then `and $0x1,%edi` — the second
instruction destroys the first's result; and block `L2` falls through
to `L1` in the candidate's own order, so block `L3` (the only block
that reads `%xmm2`) is never reached at all.

Worked instance — swift/op_13, one of the units withdrawn from the
baseline:

```
REAL   R0 ['neg %rdi', 'jo R9']   R5 ['mov %rdi,%rax', 'ret']   R9 ['ud2']
CAND   L0 ['neg %rdi', 'jo L2', 'jmp L1']   L2 ['ud2']   L1 ['mov %edi,%eax', 'ret']
```

The real answer is 64-bit (`mov %rdi,%rax`); the candidate truncates
it to 32 (`mov %edi,%eax`). Its 32-bit counterpart swift/op_12 is
correct and still proves — so the defect is real and specific, not a
modelling artifact.

Worked instance — go/op_96:

```
REAL   R0 ['push %rbp','mov %rsp,%rbp','test %ebx,%ebx','je R18']
       R8 ['cmp $0xffffffff,%ebx','jne R13']
       Rd ['neg %eax','xor %edx,%edx','jmp R16']
       R13 ['cltd','idiv %ebx']
       R16 ['pop %rbp','ret']
       R18 ['call 43f3c0 <runtime.panicdivide>','nop']
CAND   L0 ['test %esi,%esi','je L5','jmp L1']   L5 ['call runtime.panicdivide']
       L1 ['cmp $0xffffffff,%esi','jne L3','jmp L2']   L6 []
       L3 ['mov %edi,%eax','cltd','idiv %esi']
       L2 ['neg %edi','xor %r10d,%r10d','jmp L4_p1']
       L4 ['ret']   L4_p1 ['mov %edi,%eax','ret']
```

The candidate's block `L3` has no terminator and falls through in the
candidate's own order into `L2`, so on the normal path it computes
`-a` instead of `a/b`. z3's counterexample:
`[seed_rdi = 335379663, seed_rsi = 2945578971]`.

One more latent defect fixed while doing this: `canon9`'s branch
walker saves and restores exactly four pieces of simulator state
across a conditional branch and does not save Sim7's `push_stack`.
Measured effect on go/op_96 and go/op_132: after one side ran to a
`pop`, the other side found the stack already emptied and the unit
was refused. `canon10`'s `walk`/`walk_from` snapshots EVERY instance
attribute instead of a hand-listed four, so a future state addition
cannot leak across a branch again.

### 4.4 the honest re-run

```
$ /tmp/reconnect_venv/bin/python3 canon31.py
wrote canon31_units_c.json     -- {'attempted_straight': 36, 'accepted_straight': 36, 'attempted_branching': 20, 'accepted_branching': 0, 'disproved': 20, 'undecided': 0, 'skipped_not_float_family': 7, 'skipped_already_converged': 547, 'skipped_no_candidate': 0, 'audit_branching_rechecked': 0, 'audit_branching_still_proved': 0, 'audit_branching_withdrawn': 0}
wrote canon31_units_cpp.json   -- {'attempted_straight': 38, 'accepted_straight': 38, 'attempted_branching': 22, 'accepted_branching': 0, 'disproved': 22, 'undecided': 0, 'skipped_not_float_family': 16, 'skipped_already_converged': 690, 'skipped_no_candidate': 4, 'audit_branching_rechecked': 0, 'audit_branching_still_proved': 0, 'audit_branching_withdrawn': 0}
wrote canon31_units_go.json    -- {'attempted_straight': 0, ..., 'audit_branching_rechecked': 2, 'audit_branching_still_proved': 0, 'audit_branching_withdrawn': 2}
wrote canon31_units_rust.json  -- {'attempted_straight': 0, ..., 'audit_branching_rechecked': 0}
wrote canon31_units_swift.json -- {'attempted_straight': 0, ..., 'audit_branching_rechecked': 16, 'audit_branching_still_proved': 5, 'audit_branching_withdrawn': 11}
TOTAL: {'attempted_straight': 74, 'accepted_straight': 74,
        'attempted_branching': 42, 'accepted_branching': 0,
        'disproved': 42, 'undecided': 0,
        'skipped_not_float_family': 98,
        'skipped_already_converged': 1561, 'skipped_no_candidate': 4,
        'audit_branching_rechecked': 18,
        'audit_branching_still_proved': 5,
        'audit_branching_withdrawn': 13}
wrote canon31_branching_audit.json -- 18 rows
```

The 18 audited units, verbatim from `canon31_branching_audit.json`
(5 still proved, 11 DISPROVED, 2 that were UNDECIDED before the
push/pop fix are now DISPROVED):

| unit | recheck |
|---|---|
| go/96 | DISPROVED (`seed_rdi = 335379663, seed_rsi = 2945578971`) |
| go/132 | DISPROVED (`seed_rsi = 1713713797, seed_rdi = 2581253503`) |
| swift/12 | PROVED_EQUAL |
| swift/13 | DISPROVED |
| swift/150 | PROVED_EQUAL |
| swift/186 | PROVED_EQUAL |
| swift/222 | PROVED_EQUAL |
| swift/229 | DISPROVED |
| swift/236 | DISPROVED |
| swift/258 | PROVED_EQUAL |
| swift/265 | DISPROVED |
| swift/272 | DISPROVED |
| swift/870 | DISPROVED |
| swift/877 | DISPROVED |
| swift/884 | DISPROVED |
| swift/906 | DISPROVED |
| swift/913 | DISPROVED |
| swift/920 | DISPROVED |

`canon31.py` deliberately does NOT change the recorded status of an
audited unit — withdrawal is a reported finding this lap, and
rewriting 1,561 baselined records is not this task's scope. Both
totals are reported side by side.

### 4.5 both controls now PASS

```
$ /tmp/reconnect_venv/bin/python3 canon31_controls.py
CONTROL 1 (negative, mutation): {'units_tested': 74, 'mutations_applied': 222, 'mutations_rejected': 222, 'mutations_still_proved_equal': 0, 'mutations_not_applicable': 0}
   PASS -- every applied mutation was rejected
CONTROL 2 (positive, real against real): {'units_tested': 42, 'real_against_real_proved': 42, 'real_against_real_not_proved': 0}
   PASS -- every DISPROVED branching unit proves equal to itself, so the DISPROVED verdict is about the candidate text, not about this checker
wrote canon31_controls.json
```

Control 2 is what makes the 42 DISPROVED verdicts load-bearing: on
every one of those units the walker, the float model, the answer-home
rule and the constant guard prove the real text equal to itself, so
the disagreement is in the candidate, not in the checker.

---

## 5. zero regressions, and the two totals

Evidence class: **tool testimony, reproducible.** Every one of the
1,561 baseline converged records compared FIELD BY FIELD against its
canon31 record:

```
$ /tmp/reconnect_venv/bin/python3 canon31_zero_regression.py
baseline converged units compared field by field: 1561
differences found: 0
fields canon31 ADDED to baseline records: {'job8_branching_audit_detail': 18, 'job8_branching_audit_verdict': 18}
per-language converged, canon29 -> canon31:
   c       547 ->  583  (+36)
   cpp     690 ->  728  (+38)
   go       72 ->   72  (+0)
   rust    112 ->  112  (+0)
   swift   140 ->  140  (+0)
   TOTAL  1561 -> 1635  (+74)
branching-audit WITHDRAWN (recorded converged, re-gate against real ship blocks did not prove): 13
honest standing converged total: 1622
ZERO-REGRESSION CHECK: PASS
```

**Converged delta from 1,561: +74 recorded (1,635); +61 honest
(1,622) once the 13 withdrawals are subtracted.** The only fields
canon31 adds to a baseline record are the two audit fields, listed
and counted above.

`dominant_table24` / `dom_ops22` were **not opened** this lap. Open
item, carried forward unchanged from log_099 and log_105: round 3's
84, round 4's 20 and this lap's 74 all still await
`tree_units`/`clusters`/`dominant_table` incorporation, and the 13
withdrawals must be reflected there too whenever that step runs.

---

## 6. the spelling guard, on every artifact this lap produced

```
$ for f in canon31_units_{c,cpp,go,rust,swift}.json canon31_branching_audit.json canon31_controls.json canon30_negative_control.json canon30_units_{c,cpp,go,rust,swift}.json diag_caller_destination.json; do
    printf '%-34s ' "$f"; /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py "$f" 2>&1 | tail -1; done
canon31_units_c.json               PASS canon31_units_c.json -- exempt: top-level meta declares role 'generator provenance', so this file is generator provenance and never participates in matching
canon31_units_cpp.json             PASS ...
canon31_units_go.json              PASS ...
canon31_units_rust.json            PASS ...
canon31_units_swift.json           PASS ...
canon31_branching_audit.json       PASS canon31_branching_audit.json -- exempt: top-level meta declares role 'generator provenance', ...
canon31_controls.json              PASS canon31_controls.json -- exempt: top-level meta declares role 'generator provenance', ...
canon30_negative_control.json      PASS ...
canon30_units_c.json               PASS ...
canon30_units_cpp.json             PASS ...
canon30_units_go.json              PASS ...
canon30_units_rust.json            PASS ...
canon30_units_swift.json           PASS ...
diag_caller_destination.json       PASS diag_caller_destination.json -- no operator token in any key, grouping, pairing or row structure
```

**The guard FAILED twice on the first build and both were repaired at
the source, not exempted:** `canon31_branching_audit.json` carried an
`operator_display_label_only` field on rows that had no `lang` field,
so the guard read it as a row key rather than a per-unit label — the
field was removed and `lang`/`n` added; and both audit files declared
`role: generator provenance` while carrying a top-level `rows` field,
which the guard correctly refuses as a grouping artifact wearing a
provenance exemption — the field was renamed `per_unit`.
`diag_caller_destination.json` claims **no exemption at all**: it
genuinely groups units, so it is checked in full and passes in full.

---

## 7. per-bucket accounting of the remaining 144

Recorded-converged 1,635 + 144 = 1,779. Counted from disk by
machine-form key (the pipeline's own `status`, canon4's own refusal
text, and VEX lifter names — no operator token participates):

| bucket | count | disposition this lap | converged delta |
|---|---|---|---|
| float family, straight-line | 74 | **PROVED against each unit's own ship code** (Sim10) | **+74** |
| float family, branching | 42 | **DISPROVED** — canon4's branch renderer emits a candidate that computes a different answer (destroyed intermediate, wrong fall-through order). Newly proven, previously hidden by the circular gate. Next round: repair canon4's branch renderer, then re-gate. | 0 |
| `no_canon4_text`: two stack-spilled operands | 22 (18 + the 4 float-family units with no candidate at all) | defer, unchanged — canon4 erasure stage | 0 |
| `no_canon4_text`: branch target unresolved | 16 | defer, unchanged | 0 |
| `amd64g_calculate_rflags_c` (`CF_SUB`) | 18 (12 `unchanged` + 6 `not_yet_converged`) | out of scope, not reopened, no new evidence | 0 |
| `amd64g_calculate_condition` | 9 (8 + 1 mixed) | out of scope, not reopened | 0 |
| WIDTH_OF / stack-relative (`SP:64`) | 9 `not_yet_converged` with no named op (includes log_099's 6) | the owner-reserved, unchanged | 0 |
| `DivModS128to64` / `DivModU128to64` | 10 | defer, unchanged | 0 |
| `no_canon4_text`: too many join paths | 6 | defer stays deferred | 0 |
| `no_canon4_text`: caller-provided destination (§2) | 6 (4 "read before defined" + 2 "never entered a tracked register") | **the owner-reserved, newly diagnosed as ONE family; 5 of the 6 are that family, swift/128 is a separate `mul`-writes-`%rdx` case** | 0 |
| `unchanged`, no named op | 4 | unexplained, carried | 0 |
| `Mul32` / `Mul64` | 2 | defer, unchanged | 0 |
| **TOTAL not converged** | **144** | | |
| **withdrawn from the 1,561 baseline by the branching audit** | **13** | reported, records not rewritten | **−13 honest** |

---

## 8. complete file inventory — every file created this lap

All new. No existing artifact was modified or deleted, with one
deliberate exception named below.

| file | bytes | what it is |
|---|---|---|
| `op_pipeline/canon10_behaviour_check.py` | 41577 | `Sim10`: XMM state, the float vocabulary as uninterpreted functions, exact lane/copy/spill modelling, the float flag rule, the ground-truth answer home, the rip-constant guard, a state-complete branch walker, and the three gates |
| `op_pipeline/real_blocks.py` | 6493 | the REAL control-flow blocks of a unit, cut from its own ship bytes (capstone for offsets only) |
| `op_pipeline/canon30.py` | 8750 | first float-gate driver — straight-line half sound, branching half superseded |
| `op_pipeline/canon30_negative_control.py` | 8105 | the mutation control that exposed the circular gate |
| `op_pipeline/canon30_mark_superseded.py` | 2411 | stamps canon30's outputs so no circular verdict can be read as a result |
| `op_pipeline/canon31.py` | 10753 | the honest driver: float gate against real ground truth, plus the branching audit |
| `op_pipeline/canon31_controls.py` | 7603 | negative (mutation) and positive (real-against-real) controls |
| `op_pipeline/canon31_zero_regression.py` | 4180 | field-by-field baseline comparison and both converged totals |
| `op_pipeline/diag_caller_destination.py` | 9738 | the §2 diagnosis and its machine-form shape test |
| `op_pipeline/canon30_units_c.json` | 1948820 | canon30 output (branching verdicts stamped void) |
| `op_pipeline/canon30_units_cpp.json` | 2732290 | as above |
| `op_pipeline/canon30_units_go.json` | 217186 | as above |
| `op_pipeline/canon30_units_rust.json` | 278228 | as above |
| `op_pipeline/canon30_units_swift.json` | 779021 | as above |
| `op_pipeline/canon30_negative_control.json` | 15107 | the 52 undetected mutations, as found |
| `op_pipeline/canon31_units_c.json` | 1944173 | the current unit records |
| `op_pipeline/canon31_units_cpp.json` | 2727155 | as above |
| `op_pipeline/canon31_units_go.json` | 217408 | as above |
| `op_pipeline/canon31_units_rust.json` | 277953 | as above |
| `op_pipeline/canon31_units_swift.json` | 783130 | as above |
| `op_pipeline/canon31_branching_audit.json` | 6345 | the 18 re-gated branching verdicts |
| `op_pipeline/canon31_controls.json` | 11719 | both controls, per mutation and per unit |
| `op_pipeline/diag_caller_destination.json` | 3857 | the 5-member caller-destination family |
| `DevComms/log_112_task26_new_bucket_remainder.md` | this file | the report |

**The one deliberate modification:**
`canon30_mark_superseded.py` stamps `canon30_units_<lang>.json` —
files this same lap created — with a superseded notice and marks 42
branching verdicts void, rather than deleting the artifact that is
the evidence of how the defect was found:

```
$ /tmp/reconnect_venv/bin/python3 canon30_mark_superseded.py
stamped canon30_units_c.json -- 20 branching verdicts marked void
stamped canon30_units_cpp.json -- 22 branching verdicts marked void
stamped canon30_units_go.json -- 0 branching verdicts marked void
stamped canon30_units_rust.json -- 0 branching verdicts marked void
stamped canon30_units_swift.json -- 0 branching verdicts marked void
TOTAL branching verdicts marked void: 42
```

`canon4.py`, `canon5..canon9_behaviour_check.py`, `canon.py`,
`condition_table.py`, `census27.py`, `canon28_units_<lang>.json`,
`canon29_units_<lang>.json`, `canon4_units_<lang>.json`,
`op_units_<lang>.json`, `sem_anchored_spill_<lang>.json` and
`tree_units3.json` were opened READ-ONLY and are unchanged — the
zero-regression run above is the programmatic proof for the canon29
records, and the rest were never opened for writing by any file in
this lap's inventory.

---

## 9. two lists

**Decided, recorded for audit (mechanical):**

- float operations modeled as uninterpreted functions rather than z3
  FP theory — sound for the equality question, and it deliberately
  withholds float algebra the solver must not use;
- the answer home read off the real ship text rather than canon4's
  `entry_contract["result"]` field, because that field is measurably
  wrong on this population;
- rip-relative constants keyed positionally, behind a mnemonic-order
  guard that refuses rather than assumes;
- canon30's branching outputs stamped void rather than deleted;
- audited-but-withdrawn units keep their recorded status, with the
  audit verdict recorded beside it.

**Awaiting the owner (kept minimal):**

1. **The caller-provided-destination family (5 units).** Does the
   canonical form gain a name and designated register for an incoming
   DESTINATION ADDRESS, and an EXIT CONTRACT as the dual of the entry
   contract? Evidence in §2 and in
   `op_pipeline/diag_caller_destination.json`. Nothing was invented.
2. **The 13 withdrawn units.** They sit in the records as
   `status: converged` with a `job8_branching_audit_verdict` of
   DISPROVED beside them. Whether the baseline number is restated to
   1,622, and whether their records are rewritten, is a call about
   the record, not a mechanical detail.

---

## 10. banking

The daemon commits and pushes every 30 seconds; every artifact above
has already landed. This log is the message written for posterity,
per the 2026-08-31 ruling, not a claim of a staged-not-committed
state.
