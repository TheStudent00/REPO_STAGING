# log 130 — TASK 39: the universal-form migration, every compiled unit

Date: 2026-09-02. Author: Claude Code (implementer), no sub-agents.
Working directory: `PRIVATE/PseudoCoupHQ/Research/op_pipeline`.
Python: `/tmp/reconnect_venv/bin/python3`.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line — not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention — never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 — the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim.

---

# 1. What the lap did, at the top resolution

## 1.1 The one sentence

Every compiled unit that has a canonical text now carries a
UNIVERSAL-FORM text — its argument values originate at designated
virtual-memory locations, standardized loads bring them to their
standardized registers, the unit's own computation runs unchanged, and
the answer is stored to its designated location and left in its
register — and 1,744 of the 1,779 units in the corpus are in that form
with a gate proof behind each one.

## 1.2 The headline counts, each recomputed from disk this lap

| measure | before (register-first) | after (universal form) |
|---|---|---|
| units carrying a canonical text with a gate proof | 1,663 converged | 1,744 carry an admitted universal text |
| of those, converged in the ruled sense (a standing proof against the unit's own ship code) | 1,663 | **1,655** |
| classes | 901 | **898** |
| nodes | 137 | **137** |
| families | 26 | **26** |
| edgeless nodes | 20 | **20** |
| join rows / proved relations | 23 / 18 | 23 / 18 |
| union components | 2 | 2 |

- The brief's handoff figure was "converged 1,676 of 1,779". That
  number is not what the disk says; §7.1 recomputes it and names the
  difference rather than adopting either figure on trust.

## 1.3 The expectation the brief set, and what was measured

- The brief asked this to be TESTED, not assumed: "the universal form
  removes register-idiosyncrasy … so cross-language classes may MERGE
  further."
- **Measured: it does not merge. It splits.** Zero merges anywhere in
  the corpus; 77 register-first texts each split into more than one
  universal text; the distinct-text count rises from 527 to 606 over
  the same units. §6 walks the cause with values in motion.

---

# 2. The universal-form rendering for a compiled unit, stated
# mechanically

This is the definition, and it is documented in the module header of
`canon35_universal.py` as the brief requires. Every term is
introduced before it is used.

## 2.1 The directory: which location holds which designation

- A DESIGNATED LOCATION is a named stack address. The names and
  addresses come from `designated_memory.slot_text(i)`, unchanged
  since log_118: slot `i` sits at `-0x%x(%rsp)` for `8*(i+1)`.
- The directory is FIXED for every unit in the corpus:

```
S0   -0x8(%rsp)    holds  a        (argument 1)
S1   -0x10(%rsp)   holds  b        (argument 2, when the unit has one)
S2   -0x18(%rsp)   holds  answer
```

- `S2` is reserved for the answer even in a one-argument unit. The
  directory is a STANDARD; "the answer lives at S2" must not depend on
  how many arguments a unit happens to take.
- The three addresses sit inside the System V 128-byte red zone, so
  the form still needs no prologue — the same property log_118
  established for the slot series.

## 2.2 The standardized load: one pattern for everyone

- An ARRIVAL is an argument value reaching the unit. Its designated
  register is the one the unit's own recorded entry contract names
  (`canon4_units_<lang>.json`, field `entry_contract`, produced by
  `canon.designated()`): `a` takes `%rdi`, or `%xmm0` when the first
  argument is a floating-point value; `b` takes `%rsi`, `%xmm1` when
  `a` is also floating point, `%xmm0` otherwise.
- The load is one line per arrival, in designation order:

```
integer-file arrival    mov  <slot>,%<64-bit designated register>
vector-file arrival     movq <slot>,%xmm<k>
```

- It is always full width. A core that reads `%edi` or `%dil` reads
  the low lanes of the same loaded value, so the load pattern does not
  vary with a declared width. The registers are the standardized
  VEHICLES; the locations are the definition.

## 2.3 The computation core, and the answer

- The core is the unit's own newest canonical text with its trailing
  `ret` removed. Nothing inside it is rewritten. It already reads the
  designated registers, which the loads have just filled.
- The answer is stored AND kept:

```
integer result   mov  %rax,-0x18(%rsp)
vector result    movq %xmm0,-0x18(%rsp)
```

- Both homes are recorded per unit in `answer_seats`
  (`designated_location` and `designated_register`), which is the
  brief's "record both".
- Each record also carries `universal_text_no_answer_store` — the same
  text without that one line — because the interpreter side's
  universal form (`interp_canon35.py`, log_124) emits no store. That
  field lets the two views be compared on identical ground without
  re-rendering either. **Open for the owner: the two sides differ by that
  one line, and one of them should eventually move.**

## 2.4 The arrival annotation: read, never invented

- The annotation is read from `canon33_arrival_modes.json`'s
  `compiled` map. Its whole compiled tally, pasted:
  `{"plain": 1776, "typed-pointer(i32)": 1, "typed-pointer(i64)": 1,
  "typed-pointer(u64)": 1}`.
- The three typed-pointer units are `rust/op_786`, `rust/op_793`,
  `rust/op_800`. Every other compiled unit is `plain`, which is what
  the brief expected for compiled scalar units.
- The annotation rides BESIDE the text and never inside it. That is
  precisely what lets a pointer-arriving unit and a plain-arriving one
  meet on the same memory-based form.

## 2.5 The displaced-ABI units get a four-designation directory

- `canon32_sret_units.json` measured a three-seat entry contract for
  five rust units: a RESULT-DESTINATION pointer arrives first, then
  `a`, then `b`, and the answer is a nine-byte image at the
  destination with the destination address returned in `%rax`.
- Those five take the directory their own ABI hands them, in arrival
  order, with the answer one slot further down:

```
S0  -0x8(%rsp)   result-destination -> %rdi
S1  -0x10(%rsp)  a                  -> %rsi
S2  -0x18(%rsp)  b                  -> %rdx
S3  -0x20(%rsp)  answer            <-  %rax
```

- `rust/op_786`, verbatim from `canon35_universal_rust.json`:

```
prior:  mov %esi,(%rdi); mov %edx,0x4(%rdi); movb $0x0,0x8(%rdi); mov %rdi,%rax; ret
univ :  mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov -0x18(%rsp),%rdx;
        mov %esi,(%rdi); mov %edx,0x4(%rdi); movb $0x0,0x8(%rdi);
        mov %rdi,%rax; mov %rax,-0x20(%rsp); ret
```

- All five are admitted. This is the case the register-first form
  could not state at all without a second dialect.

## 2.6 The private region, and the one bias

- Some units already spell stack-relative scratch of their own. Where
  such an address IS one of S0/S1/S2 it would collide with the
  directory.
- Only then is a bias applied, and then to EVERY stack displacement in
  that unit at once: `PRIVATE_BIAS = 0x20`, so `-0x1(%rsp)` becomes
  `-0x21(%rsp)` and `-0x8(%rsp)` becomes `-0x28(%rsp)`, clear of the
  whole directory. The same constant is added everywhere, so the
  unit's own scratch keeps its exact relative structure and only
  moves.
- A unit whose displacements do not collide is left untouched. This is
  the smallest change that makes the directory sound.

## 2.7 The preconditions, each refusing by name

- **P1** — the core must not write a designated location. Checked, and
  reported, rather than assumed.
- **P2** — for a VECTOR arrival, every core line that reads the arrival
  register must be LANE-WISE: a scalar-float operation, a bit-parallel
  packed one, or a lane-preserving copy, so its low lane depends only
  on the operands' low lanes. A designated location holds a VALUE,
  eight bytes; the standardized load fills the low lane and zeroes the
  rest. A unit whose answer depended on the upper lanes would depend
  on something that is not the value — a finding, recorded by name.
  Measured this lap: no unit fails P2 after the lane-wise set was
  completed (§7.3 names the one correction that made that true).
- **P3** — the unit must present an entry contract naming its arguments
  and its result. Where no `canon4` record exists at all, the contract
  is INFERRED from the unit's own text (the arrival families are the
  ones the text reads before it writes them, seated by
  `canon.designated()`'s own rule) and the record says so in
  `entry_contract_source`.

## 2.8 A precondition this render does NOT need, named so its absence
## is not read as an oversight

- The interpreter lap had to check that the core does not write a
  designated operand register before its last read of it. That lap
  REWROTE register names inside the core (it deleted park-reloads and
  substituted the designated register downstream), so a clobber was
  real.
- This lap copies the core VERBATIM and only prepends loads. A core
  that overwrites an arrival register does exactly what it did before;
  there is nothing to clobber.
- The first-mention shape is still measured and recorded per unit as
  `first_mention_of_each_arrival`, as information, never as a refusal.
- This was caught by measurement: carrying the interpreter lap's
  precondition across refused 21 units for a hazard that cannot occur
  here (§7.3).

---

# 3. The gate — what makes the new texts admissible

## 3.1 Two gates run on every unit, and both verdicts are recorded

Both bind THE ARRIVAL CONTRACT before anything is proved:
`slot_-0x8(%rsp)` is bound to the same symbol as the canonical
a-register, `slot_-0x10(%rsp)` to the b-register. So the proof
obligation is exactly the ruled one: **for all values in the
designated locations, the universal text computes what the original
computes on those values.**

- **GATE 1, the admission gate** — the universal text against the
  unit's OWN PRIOR CANONICAL TEXT, z3, under `Sim35`. This is the
  interpreter lap's gate shape (log_124 §3). The prior text is itself
  already gate-proved against the unit's own ship code by the
  generation that converged it, so `universal == prior == ship` is a
  proof against the ship code that does not re-litigate gate quirks
  this lap did not touch. A unit that does not prove here keeps NO
  universal text.
- **GATE 1b, the structural route** — used only where gate 1 returns
  UNDECIDED (the simulator has no model for some mnemonic the unit
  spells, or the text is a block list a straight-line walk must not
  be asked about). Five checks, each mechanical and each recorded:
  (i) the core is character-identical to the prior core; (ii) the
  loads write only the arrival registers, one line each, from their
  own locations; (iii) no core line names a designated location;
  (iv) the answer store reads the answer register and writes S2, and
  every `ret` is immediately preceded by it; (v) P2's lane safety
  holds. Under (i)–(v) the universal text executes the prior text's
  instruction sequence on the register state the loads establish, and
  the store touches a location nothing else reads — equivalence is
  forced by construction.
- **GATE 2, the direct ship gate** — the universal text against the
  unit's own ship code, `canon33_gate`'s own straight-line checker
  with the arrival contract bound. Recorded per unit whether it proves
  or refuses.

## 3.2 The measured verdicts

```
$ /tmp/reconnect_venv/bin/python3 canon35_universal.py --lang c --fresh
c       610 units  {"GATE_DISPROVED": 3, "GATE_UNDECIDED": 2, "UNIVERSAL_TEXT_PROVED": 605}
cpp     770 units  {"GATE_DISPROVED": 3, "GATE_UNDECIDED": 4, "UNIVERSAL_TEXT_PROVED": 763}
go      107 units  {"REFUSED": 6, "UNIVERSAL_TEXT_PROVED": 101}
rust    125 units  {"REFUSED": 2, "UNIVERSAL_TEXT_PROVED": 123}
swift   167 units  {"REFUSED": 15, "UNIVERSAL_TEXT_PROVED": 152}
```

- Total: **1,744 admitted of 1,779**. The five per-language runs sum
  to 610 + 770 + 107 + 125 + 167 = 1,779, which is the corpus.
- How the 1,744 were admitted, per language, computed from the
  artifacts:

```
('c',     'PROVED_EQUAL') 571   ('c',     'PROVED_BY_CONSTRUCTION') 34
('cpp',   'PROVED_EQUAL') 722   ('cpp',   'PROVED_BY_CONSTRUCTION') 41
('go',    'PROVED_EQUAL')  77   ('go',    'PROVED_BY_CONSTRUCTION') 24
('rust',  'PROVED_EQUAL') 112   ('rust',  'PROVED_BY_CONSTRUCTION') 11
('swift', 'PROVED_EQUAL') 124   ('swift', 'PROVED_BY_CONSTRUCTION') 28
```

  1,606 by solver, 138 by construction; 1,606 + 138 = 1,744.

- The direct ship gate on those 1,744:
  `{"PROVED_EQUAL": 1537, "UNDECIDED": 117, "NOT_APPLICABLE": 90}`.
  So **1,537 universal texts stand directly on their own ship code
  with no chain at all**; 117 rest on gate 1's chain because the
  straight-line ship checker refused for a reason this lap did not
  create (its narrowed rip-relative constant guard, or a mnemonic it
  does not model); 90 are block-list units, where the direct gate here
  is the straight-line checker and is therefore not applicable.

## 3.3 The 35 units with no universal text, every one named with its
## cause

```
23  no canonical text exists for this unit in any generation
     go/op_30 go/op_31 go/op_32 go/op_33 go/op_34 go/op_35
     rust/op_699 rust/op_706
     swift/op_128 swift/op_690 swift/op_691 swift/op_692 swift/op_696
     swift/op_697 swift/op_698 swift/op_702 swift/op_726 swift/op_727
     swift/op_728 swift/op_732 swift/op_733 swift/op_734 swift/op_738
 6  the answer is the ADDRESS of one of the unit's own private stack
    locations, and that location collides with the directory, so the
    universal form must move it -- which moves the answer
     c/op_31 c/op_32 c/op_34 cpp/op_43 cpp/op_44 cpp/op_46
 6  the canonical form is a block list AND the private region was
    biased, so the structural route's check (i) (core character-
    identical) cannot hold
     c/op_153 c/op_225 cpp/op_153 cpp/op_225 cpp/op_765 cpp/op_770
```

- The six address-answer units are a real finding, not a defect of
  this lap: their answer is not invariant under ANY designated-location
  directory placed in the red zone. **What would change it, named:** a
  ruled directory base other than `%rsp` for units whose answer is an
  address. Not taken here — it is the owner's call.

---

# 4. The texts assemble, and they run

## 4.1 Assembly — all 1,744, `as` + `objdump`, on disk

```
$ /tmp/reconnect_venv/bin/python3 canon35_assemble.py
offered 1744  assembled 1744  failed 0
```

- Each text is written into a real `.s` file as its own symbol,
  assembled with `as --64`, and read back with `objdump -d`; a unit
  passes only when its symbol disassembles to at least as many
  instructions as the text spells. Batches of 60; a failing batch is
  re-run one unit at a time so a failure is never smeared.
- Two normalizations, both recorded per unit and neither of them a
  cheat: the `!!…` reading annotations the pipeline's renderers attach
  are stripped (they are comments), and `0x0(%rip)` data references are
  bound to a real local constant pool emitted in the same file, so the
  instruction encoded is the real instruction. Block labels are emitted
  as LOCAL labels (`.L<symbol>_<name>`), which is what keeps a whole
  block-list unit attributed to its own symbol in the disassembly.

## 4.2 Real runs — the arrival contract executed, not argued

```
$ /tmp/reconnect_venv/bin/python3 canon35_realrun.py
eligible {"two floating-point values": 58, "two integers": 873}
sampled 80 units
pairs 10400  differing 0
```

- Each sampled universal unit is called through a wrapper that parks
  the arguments in the red zone and TAIL-JUMPS into the unit:

```
w_u_<unit>:
    mov %rdi,-0x8(%rsp)      a -> S0
    mov %rsi,-0x10(%rsp)     b -> S1
    jmp u_<unit>
```

  The jump pushes no return address, so `%rsp` is the same inside the
  unit as in the wrapper — S0 and S1 are the same two addresses on
  both sides. That is why it is a tail jump and not a call.
- The prior text is emitted beside it and called with the ordinary
  register contract. Over 14 integer values (0, 1, 2, 3, 7, 20, 255,
  4096, and the four sign boundaries at 32 and 64 bits, plus the two
  all-ones patterns) and 8 floating-point values, every ordered pair,
  **10,400 comparisons, zero differences.**
- The sample is 80 of 931 eligible units and is named as a sample. A
  unit is eligible only when the harness can honestly call it: no
  rip-relative constant (this harness carries no constant pool), no
  call, no trap.

---

# 5. Values in motion: one unit walked end to end

Take `c/op_109`, whose type pair is two 64-bit integers, with
`a = 20` and `b = 3`.

## 5.1 Its register-first text, before this lap

```
mov %rdi,%rax     %rax = 20     a is read from the register it arrived in
mov %rsi,%r10     %r10 = 3      b is read from the register it arrived in
add %r10,%rax     %rax = 23
ret                             the answer is in %rax and nowhere else
```

- Two facts are IMPLICIT here and cannot be read off the text: that the
  values arrived at all (the text simply finds them in registers), and
  where the answer lives besides `%rax`.

## 5.2 Its universal text, after this lap

```
mov -0x8(%rsp),%rdi     %rdi = 20    S0 holds a; the standardized load
mov -0x10(%rsp),%rsi    %rsi = 3     S1 holds b; the standardized load
mov %rdi,%rax           %rax = 20    the core, unchanged
mov %rsi,%r10           %r10 = 3     the core, unchanged
add %r10,%rax           %rax = 23    the core, unchanged
mov %rax,-0x18(%rsp)    S2   = 23    the answer reaches its location
ret                                  and stays in %rax as well
```

- The value 20 now has a stated ORIGIN (`S0`) and travels a stated
  ROUTE (the load into `%rdi`). The value 23 has two stated homes.
- Arrival annotation, riding beside the text: `plain`.
- Gate 1 proved this equal to the text in §5.1 at 64 bits with `S0`
  bound to the same symbol as `%rdi` and `S1` to `%rsi`. Gate 2 proved
  it equal to `c/op_109`'s own ship code under the same binding. The
  harness of §4.2 then ran both and got 23 from both.

---

# 6. The class table, rebuilt — and the expectation refuted

## 6.1 The build

```
$ /tmp/reconnect_venv/bin/python3 build_table25.py
PASS dominant_table25.json -- no operator token in any key, grouping, pairing or row structure
PASS dom_ops23.json -- no operator token in any key, grouping, pairing or row structure
{
 "0branch_offered": 1641,
 "0branch_keyed": 1635,
 "0branch_left_out": 6,
 "classes": 898,
 "nodes": 137,
 "families": 26,
 "edgeless_nodes": 20,
 "branching_joined": 4,
 "rows_with_more_than_one_arrival": 0
}
```

- Exactly one thing changed from `build_table24.py`: the TEXT. The
  population rule, the representative rule and its three grounds, the
  class-key shape and dom_ops7's family rule are IMPORTED from
  `build_table24.py` / `dom_ops.py`, not copied, so they cannot drift.
- The arrival annotation is carried on every row as recorded data
  (`arrival_annotations`) and is deliberately NOT in the key — the same
  choice `interp_table2.json` made and the owner accepted (log_124 §4.1).
  Putting it back in the key would re-create the separate dialects the
  ruling dissolves.

## 6.2 The counts against the baseline, with the change decomposed

```
$ /tmp/reconnect_venv/bin/python3 canon35_table_diff.py
classes   24=901   25=898
nodes     22=137   23=137
families  22=26    23=26
edgeless  22=20    23=20

MERGES (a table25 class holding units from more than one table24 class): 0

TABLE24 CLASSES THAT LOST MEMBERS (a member has no universal text): 3
  C0282  left out c/op_34, cpp/op_46  remaining 0  disappeared=True
  C0583  left out c/op_31, cpp/op_43  remaining 0  disappeared=True
  C0751  left out c/op_32, cpp/op_44  remaining 0  disappeared=True
```

- 901 − 898 = 3, and all three are accounted for: each of the three
  vanished classes had exactly two members, and both members are among
  the six address-answer refusals of §3.3. **No class lost a member to
  anything but a named, proved cause.**

## 6.3 EVERY family change, verbatim, with its cause

```
FAMILY CHANGES: 1 changed, 1 vanished
  D0024  units: c/op_30, c/op_33, c/op_35, cpp/op_42, cpp/op_45, cpp/op_47
      dom_ops22 D0024: c/op_30, c/op_31, c/op_32, c/op_33, c/op_34,
                       c/op_35, cpp/op_42, cpp/op_43, cpp/op_44,
                       cpp/op_45, cpp/op_46, cpp/op_47
  VANISHED D0024  units: c/op_30, c/op_31, c/op_32, c/op_33, c/op_34,
                         c/op_35, cpp/op_42, cpp/op_43, cpp/op_44,
                         cpp/op_45, cpp/op_46, cpp/op_47
```

- That is one family, printed twice by the diff (once as the new node
  set, once as the old one it replaces). It went from 12 units to 6.
- **The cause, named:** the six units it lost are exactly
  `c/op_31 c/op_32 c/op_34 cpp/op_43 cpp/op_44 cpp/op_46` — the six
  address-answer refusals. No other family changed at all: the family
  count, the node count and the edgeless count are identical.

## 6.4 The expectation tested — the universal form is a REFINEMENT

The brief asked whether cross-language classes merge further. Measured
over the 1,744 units carrying both texts:

```
distinct texts: universal 606, register-first 527
distinct texts carried by more than one language: universal 304, register-first 264
universal texts covering more than one prior text (a MERGE): 0
prior texts that split into more than one universal text: 77
```

- **Zero merges. 77 splits.** The universal form is a strict refinement
  of the register-first form on this corpus.
- The rise from 264 to 304 in cross-language texts is NOT new merging:
  no universal text is shared across languages whose members did not
  already share a cross-language prior text (measured, count 0). It is
  the splits doing it — a prior text shared by three languages splits
  into two universal texts each still shared by two.
- **The cause, with values in motion.** Take the prior text
  `mov %rdi,%rax; and $-1,%eax; ret`. Read it and you cannot tell
  whether the unit takes one argument or two, because the second one,
  if it exists, is never touched. Under the universal form the
  arrivals are stated, so the same core splits in two:

```
prior:  mov %rdi,%rax; and $-1,%eax; ret
  ->  mov -0x8(%rsp),%rdi; mov %rdi,%rax; and $-1,%eax; mov %rax,-0x18(%rsp); ret
  ->  mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rdi,%rax; and $-1,%eax; mov %rax,-0x18(%rsp); ret
```

  The first takes one argument; the second takes two and discards the
  second. That distinction was invisible in the register-first text and
  is visible now.

- The sharpest instance is the prior text `ret` — the units whose
  canonical form is the identity on their arriving value. One text
  before; four after, one per arrival-and-answer shape:

```
prior:  ret
  ->  movq -0x8(%rsp),%xmm0; mov %rax,-0x18(%rsp); ret
  ->  movq -0x8(%rsp),%xmm0; movq %xmm0,-0x18(%rsp); ret
  ->  movq -0x8(%rsp),%xmm0; movq -0x10(%rsp),%xmm1; mov %rax,-0x18(%rsp); ret
  ->  movq -0x8(%rsp),%xmm0; movq -0x10(%rsp),%xmm1; movq %xmm0,-0x18(%rsp); ret
```

- **The finding, stated plainly for the owner:** go's ABI differences were
  already normalized away by the entry contract long before this lap
  (every compiled unit's canonical text already read `%rdi`/`%rsi`),
  so the universal form had no register idiosyncrasy left to remove.
  What it adds instead is the arrival and answer plumbing as EXPLICIT
  text, and that plumbing carries real information the core text was
  hiding. The class count moved only because six units left; the
  refinement did not split a single class, because a class key is
  (type pair, result type, text) and the units the text now separates
  already differed in their type pair.

---

# 7. Zero regression, in the ruled sense

The binding definition, quoted from log_129 because it is not the
usual one: "the universal-form texts REPLACE the register-first texts
as the canonical column, so 'zero regressions' there means no unit
loses its PROVED status and no class loses members without a named,
proved cause — text change is the point, not a regression."

## 7.1 The standing count before, recomputed from disk

```
$ /tmp/reconnect_venv/bin/python3 canon35_zero_regression.py
population 1779
standing before: {"converged": 1658, "converged (displaced ABI)": 5,
                  "no_canon4_text": 23, "not_yet_converged": 10,
                  "unchanged": 70, "withdrawn": 13}
universal after: {"GATE_DISPROVED": 6, "GATE_UNDECIDED": 6,
                  "REFUSED": 23, "UNIVERSAL_TEXT_PROVED": 1744}
```

- 1,658 + 5 + 23 + 10 + 70 + 13 = 1,779. The converged population
  before this lap is **1,663**, not 1,676.
- The brief's 1,676 is 1,663 + 13, i.e. it counts the 13 units the
  canon31 branching audit WITHDREW as still converged. The
  withdrawal is recorded on those units' own canon31 records
  (`job8_branching_audit_verdict` present and not `PROVED_EQUAL`) and
  `canon33_zero_regression.json` already carries
  `"honest_standing_converged": 1622` beside `"recorded_converged":
  1635` for exactly this reason. This log uses 1,663 and shows its
  arithmetic; **the record should be corrected to 1,663, and the
  "90 unchanged" of the handoff is 70 unchanged + 23 with no canon4
  text = 93.**

## 7.2 The cross-tab, every cell

```
  converged (displaced ABI) -> UNIVERSAL_TEXT_PROVED   5
  converged -> GATE_DISPROVED                          6
  converged -> GATE_UNDECIDED                          2
  converged -> UNIVERSAL_TEXT_PROVED                   1650
  no_canon4_text -> REFUSED                            23
  not_yet_converged -> UNIVERSAL_TEXT_PROVED           10
  unchanged -> GATE_UNDECIDED                          4
  unchanged -> UNIVERSAL_TEXT_PROVED                   66
  withdrawn -> UNIVERSAL_TEXT_PROVED                   13
```

```
units that were converged and now carry no universal text: 8
  c/op_31    converged   the answer of this unit is the ADDRESS of one of its own private stack locations…
  c/op_32    converged   the answer of this unit is the ADDRESS of one of its own private stack locations…
  c/op_34    converged   the answer of this unit is the ADDRESS of one of its own private stack locations…
  cpp/op_43  converged   the answer of this unit is the ADDRESS of one of its own private stack locations…
  cpp/op_44  converged   the answer of this unit is the ADDRESS of one of its own private stack locations…
  cpp/op_46  converged   the answer of this unit is the ADDRESS of one of its own private stack locations…
  cpp/op_765 converged   the canonical form is a block list, and gate 1's simulator walks a straight line…
  cpp/op_770 converged   the canonical form is a block list, and gate 1's simulator walks a straight line…
converged UNDER THE UNIVERSAL FORM: 1655 of 1779
carry a universal text but are NOT converged: 89
```

- **8 units lose their proved status, each with a named cause.** Six
  are the address-answer finding of §3.3 — a property of the unit, not
  a defect of the render. Two are block-list units whose private
  region also had to be biased, so the structural route's
  character-identity check cannot hold.
- **1,663 − 8 = 1,655 converged under the universal form.**
- The 89 that gained a universal text without gaining convergence are
  counted SEPARATELY and never folded into the headline: 66 were
  `unchanged`, 13 were `withdrawn`, 10 were `not_yet_converged`. A
  universal text admitted by gate 1 inherits its standing from the
  prior text it was proved equal to, so a unit whose prior text has no
  standing ship proof does not become converged by gaining one. Zero
  of the 89 proved on the direct ship gate (measured, not assumed).

## 7.3 The three causes fixed at first observation, named

- **The interpreter lap's clobber precondition, carried across
  wrongly.** It refused 21 units for a hazard that cannot occur when
  the core is copied verbatim (§2.8). Removed; replaced by the
  lane-safety precondition, which is the real one.
- **The lane-wise set was incomplete.** With it half-written, 76+40
  units refused on `cmpeqsd`/`cmpneqsd`/`cmpeqss`/`cmpneqss` (scalar
  compares — low lane only) and `movaps`/`movapd` (lane-preserving
  copies). All six are lane-wise; adding them was a correction to the
  set, not a loosening of the rule.
- **The private bias was too small.** At `0x18` a biased `-0x8(%rsp)`
  landed on `-0x20(%rsp)`, which is S3 in the four-designation
  directory — six units failed P1 on their own relocated scratch.
  Raised to `0x20`.

## 7.4 The artifacts that had to stay untouched, proved untouched

```
$ sha256sum dominant_table24.json dom_ops22.json interp_table2.json \
            interp_join2.json union_table2.json interp_canon35.json
2f31942d54a7f531b99755261402c5759b16a1ef97ffb353e7e166aa096221b7  dominant_table24.json
e2577cf37558c8ef9e046f1157d8425860cccd44660cfc2bb0884188c8243421  dom_ops22.json
8cad91fca374991f100af88da3b1f2ff0b1571a20fdfbc787783d0c8c2abbc73  interp_table2.json
ee9d73de08d73c9d4145b19d79cdc745aabd91284e50c1b32adbc38cfbb0e1b1  interp_join2.json
c46b5da71b7574790156fb6432d37b92b950e99548f9c546cc3bd759a897090a  union_table2.json
3e5d8441a4c78c76cafc6b33701e28f178d5da635fe527add144cded7341561d  interp_canon35.json
```

- The VCS is checked before any write-claim, as the standing rule
  requires:

```
$ git status --porcelain Research/op_pipeline/dominant_table24.json \
    Research/op_pipeline/dom_ops22.json Research/op_pipeline/interp_table2.json \
    Research/op_pipeline/interp_join2.json Research/op_pipeline/union_table2.json \
    Research/op_pipeline/interp_canon35.json
exit=0  (no lines above means all six are unmodified in the working tree)
$ git log --oneline -1 -- Research/op_pipeline/dominant_table24.json
3405fe9 auto: 2 files (build_table24.py, dominant_table24.json)
```

  Six files, six with no working-tree modification, and
  `dominant_table24.json`'s last commit is still the one
  `build_table24.py` made. New files only, throughout.
- The same sha256 set is stored inside
  `canon35_zero_regression.json` under `watched_artifact_sha256`, so a
  later reader can recompute rather than trust.

---

# 8. The three views, rebuilt

## 8.1 The join, re-run — `interp_join3.json`

```
$ /tmp/reconnect_venv/bin/python3 build_interp_join3.py
…
ruby/rb_int_plus   PROVED_EQUAL   rust/op_548
java/op_2          TYPE_INCOMPARABLE   no measured declared operand type: there is no ELF file for
php/add_function   TYPE_INCOMPARABLE   the declared operand type is a POINTER pair (zval*,zval*); t
interp<->interp IU0007 IU0008 PROVED_EQUAL
summary: {"join_row_count": 23, "by_relation": {"PROVED_EQUAL": 18, "TYPE_INCOMPARABLE": 5},
          "interpreter_to_interpreter_edge_count": 1, "guard_join_row_count": 6,
          "guard_join_by_relation": {"UNDECIDED_CONDITION_NOT_COMPARABLE": 6}}
PASS interp_join3.json -- no operator token in any key, grouping, pairing or row structure
```

- **Identical to `interp_join2.json`: 23 rows, 18 proved, 5 type-
  incomparable.** Every relation survives the change of the compiled
  side's text column.
- Two inputs changed and nothing else: the compiled class index now
  reads `dominant_table25.json`, and the compiled candidate
  population's text is now the universal text. Both are monkeypatched
  seams on `build_interp_join2.py`'s own code, so the candidate rule,
  the relation vocabulary, the prover and the row shape cannot drift.
- One consequence worth naming: both sides now spell their values as
  designated locations, so the binding convention is ONE convention.
  Under the register form the compiled side named registers and the
  interpreter side named locations, and the binding had to bridge them.

## 8.2 The union — `union_table3.json`

```
$ /tmp/reconnect_venv/bin/python3 build_union_table3.py
U0001  interpreter=['IU0002']  compiled=['C0504']  edges=1
U0002  interpreter=['IU0001', 'IU0007', 'IU0008']  compiled=['C0698', 'C0886']  edges=18
summary: {'compiled_classes': 898, 'interpreter_classes': 8,
          'union_components': 2, 'proved_edges': 19, 'units_indexed': 1648}
PASS union_table3.json -- no operator token in any key, grouping, pairing or row structure
```

- Against `union_table2.json`: `{"compiled_classes": 901,
  "interpreter_classes": 8, "proved_edges": 19, "union_components": 2,
  "units_indexed": 1654}`.
- Both components survive with the same edge count. The compiled class
  count drops by the 3 vanished classes of §6.2 and the indexed-unit
  count by the 6 units of §3.3. Nothing else moved.
- Three views preserved, nothing merged, nothing destroyed.

## 8.3 The five displaced-ABI units sit in no class table, before or
## after

- `rust/op_786`, `793`, `800`, `807`, `814` are absent from
  `dominant_table24.json` AND from `dominant_table25.json`. Verified:

```
sret in table24: []
sret in table25: []
canon4_units_rust.json['786']: erasure=ok, derived_text is a list = False
```

  `load_0branch_units` requires `derived_text` to be a list, and theirs
  is not, so both tables skip them by the same rule. This is not a
  regression; it is the same population on both sides. They DO carry
  universal texts (§2.5).

---

# 9. The guards

## 9.1 Every new artifact, checked

```
PASS dominant_table25.json -- no operator token in any key, grouping, pairing or row structure
PASS dom_ops23.json        -- no operator token in any key, grouping, pairing or row structure
PASS representatives25.json-- no operator token in any key, grouping, pairing or row structure
PASS interp_join3.json     -- no operator token in any key, grouping, pairing or row structure
PASS union_table3.json     -- no operator token in any key, grouping, pairing or row structure
PASS canon35_universal_c.json    -- exempt: top-level meta declares role 'generator provenance'
PASS canon35_universal_cpp.json  -- exempt: …
PASS canon35_universal_go.json   -- exempt: …
PASS canon35_universal_rust.json -- exempt: …
PASS canon35_universal_swift.json-- exempt: …
PASS canon35_assemble.json       -- exempt: …
PASS canon35_realrun.json        -- exempt: …
PASS canon35_zero_regression.json-- exempt: …
PASS canon35_table_diff.json     -- exempt: …
```

- The matching-shaped artifacts — `dominant_table25.json`,
  `dom_ops23.json`, `interp_join3.json`, `union_table3.json`,
  `representatives25.json` — pass IN FULL, with NO exemption claimed.
  `dom_ops23.json` was entitled to the ratified generator-provenance
  exemption its predecessors use and did not need it.
- `build_table25.py` runs the check on its own two outputs and raises
  `REFUSING OWN OUTPUT` on failure, which is the mechanical guard the
  ban requires.

## 9.2 The exemption the nine provenance files claim is not load-bearing

Rather than assert that, it was tested: each was copied with its
`meta.role` declaration REMOVED and re-checked, so the checker had no
exemption to grant.

```
$ for f in …; do strip meta.role; check_no_spelling_keys.py /tmp/c35_strip/$f; done
PASS canon35_universal_c.json     -- no operator token in any key, grouping, pairing or row structure
PASS canon35_universal_cpp.json   -- no operator token in any key, grouping, pairing or row structure
PASS canon35_universal_go.json    -- no operator token in any key, grouping, pairing or row structure
PASS canon35_universal_rust.json  -- no operator token in any key, grouping, pairing or row structure
PASS canon35_universal_swift.json -- no operator token in any key, grouping, pairing or row structure
PASS canon35_assemble.json        -- no operator token in any key, grouping, pairing or row structure
PASS canon35_realrun.json         -- no operator token in any key, grouping, pairing or row structure
PASS canon35_zero_regression.json -- no operator token in any key, grouping, pairing or row structure
PASS canon35_table_diff.json      -- no operator token in any key, grouping, pairing or row structure
```

- All nine pass without any exemption. The operator token appears in
  those files exactly once per unit, as the `operator` display label,
  and is read by nothing.
- Selection and grouping throughout this lap are machine-form: the
  corpus of `canon31_units_<lang>.json`, the recorded
  `entry_contract`, the recorded branch shape, the class key
  (type pair, result type, text), and `seeds2.json`'s seed-text
  equality. No token participates anywhere.

---

# 10. Complete file inventory

## 10.1 Programs written (8)

| file | what it is |
|---|---|
| `Research/op_pipeline/canon35_universal.py` | the render + both gates + the structural route; the mechanical definition of the form lives in its header |
| `Research/op_pipeline/canon35_assemble.py` | `as` + `objdump` over every universal text |
| `Research/op_pipeline/canon35_realrun.py` | the tail-jump harness; real execution through the designated locations |
| `Research/op_pipeline/canon35_zero_regression.py` | the standing counts, the cross-tab, the watched sha256 set |
| `Research/op_pipeline/canon35_table_diff.py` | class/node/family/edgeless diff with the change decomposed by cause |
| `Research/op_pipeline/build_table25.py` | the class table on the universal text |
| `Research/op_pipeline/build_interp_join3.py` | the join re-run against the new compiled table |
| `Research/op_pipeline/build_union_table3.py` | the union rebuilt (derived from `build_union_table2.py`, three inputs changed) |

## 10.2 Artifacts written (14)

| file | bytes |
|---|---|
| `Research/op_pipeline/canon35_universal_c.json` | 2,482,058 |
| `Research/op_pipeline/canon35_universal_cpp.json` | 3,533,482 |
| `Research/op_pipeline/canon35_universal_go.json` | 305,465 |
| `Research/op_pipeline/canon35_universal_rust.json` | 406,173 |
| `Research/op_pipeline/canon35_universal_swift.json` | 815,724 |
| `Research/op_pipeline/canon35_assemble.json` | 279,165 |
| `Research/op_pipeline/canon35_realrun.json` | 2,063 |
| `Research/op_pipeline/canon35_zero_regression.json` | 59,622 |
| `Research/op_pipeline/canon35_table_diff.json` | 1,804 |
| `Research/op_pipeline/dominant_table25.json` | 2,330,152 |
| `Research/op_pipeline/dom_ops23.json` | 47,514 |
| `Research/op_pipeline/representatives25.json` | 1,695,740 |
| `Research/op_pipeline/interp_join3.json` | 32,511 |
| `Research/op_pipeline/union_table3.json` | 889,443 |

## 10.3 Caches created (2)

- `Research/op_pipeline/__pycache__/build_interp_join2.cpython-313.pyc`
- `Research/op_pipeline/__pycache__/canon35_zero_regression.cpython-313.pyc`

Named because the rule says to name EVERY file created including
caches. The other three `__pycache__` entries with today's date
(`core_rule2`, `legality_filter`, `probe_gen`) belong to the
concurrently running task-40 trickle, not to this lap. No other
`__pycache__` entry was rewritten: the modules this lap imported
(`build_table24`, `dominant_table17`, `cross_unit_prover`,
`build_interp_join1`, `canon33_gate`, `designated_memory`) all still
carry their pre-existing mtimes.

## 10.4 Work directories outside the repo (5)

- `/tmp/canon35_assemble_work/` — 60 files, the batch `.s`/`.o` pairs
- `/tmp/canon35_realrun_work/` — `units.s`, `driver.c`, `harness`
- `/tmp/c35_strip/` — 9 role-stripped copies for the §9.2 test
- `/tmp/c35_c.log`, `/tmp/c35_cpp.log`, `/tmp/c35_go.log`,
  `/tmp/c35_rust.log`, `/tmp/c35_swift.log` — the per-language run logs
- `/tmp/final_status.json` — a scratch status map from the audit of §7.1

## 10.5 Nothing was overwritten

New files only. §7.4 proves the six artifacts that had to stay
untouched are byte-identical and unmodified in the VCS.

---

# 11. Two lists

## 11.1 Decided, recorded for audit

- The admission gate is the universal text against the unit's own
  PRIOR canonical text, with the direct ship gate recorded beside it
  per unit. Reason: the prior text already carries a ship proof, so the
  chain is a ship proof, and it does not re-litigate gate quirks this
  lap did not touch. 1,537 of 1,744 also prove directly on ship.
- The interpreter lap's clobber precondition was DROPPED for this
  render, with the reason stated in the module header: this lap copies
  the core verbatim, so nothing can be clobbered.
- The private-region bias is applied only on collision, and at `0x20`.
- The arrival annotation is recorded data on every class row, not part
  of the class key.
- The branching seeds are matched against a pool that includes each
  member's prior register-form text, with `matched_against` recorded
  per join, because no seed text has ever been rendered into the
  universal form and gated.
- The five displaced-ABI units take a four-designation directory in
  their own ABI's arrival order.

## 11.2 Awaiting the owner

- **The answer store.** The compiled universal form emits
  `mov %rax,-0x18(%rsp)`; the interpreter universal form (log_124)
  emits nothing. Both are on disk and both are recorded (the compiled
  records carry `universal_text_no_answer_store`). One of the two
  should become the form.
- **The six address-answer units.** Their answer is the address of
  their own stack scratch, so no red-zone directory can hold them. The
  named remedy is a ruled directory base other than `%rsp` for such
  units.
- **The converged figure of record.** This lap measures 1,663 before
  and 1,655 after; the handoff said 1,676. The difference is the 13
  withdrawn units. The record should be corrected.
