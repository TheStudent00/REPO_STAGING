# log 167 — task 63: runtime_callee, generalized

Date: 2026-09-03. Round 13, TASK 63 of
`~/Programming/PseudoCoupHQ/DevComms/log_166_claude_code_task_briefs_round13.md`.
Node: `hq.research.compiler_graph.arch_unit.runtime_callee`, at
`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_1_arch_unit/node_0_3_5_1_8_runtime_callee/`.
Appendix-B shape; §5.1a LITERAL / GLOSS labels throughout; every
number carries its population.

---

# 1. What was done, in plain words before any figure

A body of machine code sometimes hands its answer to a routine the
compiler shipped with itself. `__extendhfsf2` is one such routine: it
takes a 16-bit half float and returns the same number as a 32-bit
float, because no single hardware instruction does that. Round 12
attached FOUR such routines — the 128-bit division family — for the
308 units a recorded list named. The round-12 audit found the real
population is far larger, and this task attached the rest.

Three things happened.

- **The census replaced the list.** Instead of reading a recorded list
  of 308 units, this task counted canon39 itself: which of its 30,432
  proved units carry a `call`, and which name each one's relocation
  spells. That is 4,119 units over 36 distinct routine names.
- **The extraction was made relocation-aware and recursive.** A
  routine's body is unlinked, so a `call` inside it disassembles as a
  jump to an address in the same file and the callee's name survives
  only in the relocation. Reading `objdump -dr` and following those
  names found six routines nobody calls directly — they are only ever
  reached from inside another routine's body.
- **Swift was extracted where swift lives.** Task 59 asked `swiftc` on
  the host, got nothing, and recorded swift's callers as not attached.
  Swift is installed inside the `trickle` sandbox instance, so the
  extraction ran there as a lane.

One correction fell out of the work that had nothing to do with the
plan: `objdump --disassemble=<name>` prints an EMPTY body for a name
that shares its address with another name, which clang's
128-bit-float comparison routines all do. The fix is to disassemble
the symbol's address range instead of asking for it by name.

---

# 2. The population, and the names in it

## 2.1 What was counted, and over what

LITERAL — `~/Programming/PseudoCoupHQ/Research/op_pipeline/canon39_callee_printed.txt`,
part 1:

```
canon39 proved units walked: 30432
  by language: {"c": 10367, "cpp": 17569, "cpython": 1, "go": 577,
                "java": 2, "php": 4, "ruby": 2, "rust": 685,
                "swift": 1225}
call-bearing units: 4119
  by language: {"c": 1579, "cpp": 2327, "go": 170, "rust": 30,
                "swift": 13}
```

GLOSS: the population is canon39's PROVED units, 30,432 of them —
the same figure log_165 §2 recomputed. 4,119 of those bodies carry at
least one `call`.

**4,119 is not the 3,419 of log_160 §1.7, and the difference is not a
disagreement.** 3,419 counts units whose TERM ROUTE stopped at the
`call`. A unit whose body has a conditional transfer BEFORE its
`call` stopped earlier, at the branch, and was counted under that
cause instead. So 3,419 is a subset of 4,119, and task 64's branch
following is what will draw the rest of them through.

## 2.2 The full list of names, computed

LITERAL — the same transcript, part 1. The count is UNITS that spell
the name, not lines:

| name | units | name | units |
|---|---|---|---|
| `__extendhfsf2` | 1,398 | `__extendsftf2` | 56 |
| `__truncsfbf2` | 920 | `__floatunditf` | 56 |
| `__truncsfhf2` | 911 | `__floattihf` | 44 |
| `__netf2` | 530 | `__floatuntihf` | 44 |
| `__floatsitf` | 310 | `__floattidf` | 44 |
| `__lttf2` | 157 | `__floatuntidf` | 44 |
| `__gttf2` | 157 | `__floatunsitf` | 44 |
| `__floatditf` | 112 | `__extendhftf2` | 28 |
| `__eqtf2` | 107 | `__extendhfxf2` | 28 |
| `__letf2` | 104 | `__floattitf` | 28 |
| `__getf2` | 104 | `__floatuntitf` | 28 |
| `__floattisf` | 88 | `__extenddftf2` | 28 |
| `__floatuntisf` | 88 | `__extendxftf2` | 28 |
| `__udivti3` | 78 | `__floattixf` | 28 |
| `__umodti3` | 78 | `__floatuntixf` | 28 |
| `__divti3` | 74 | rust's four `panic_const` names | 15, 15, 8, 8 |
| `__modti3` | 74 | go's four unrelocated transfers | 122, 28, 20, 20 (lines) |

GLOSS: `__extendhfsf2` widens a half float to a float; `__truncsfbf2`
narrows a float to bfloat16; `__netf2` and `__gttf2` compare two
128-bit floats; `__floatsitf` turns a 32-bit integer into a 128-bit
float. Every one of them is the compiler's own lowering of an
operation the hardware has no instruction for.

The last two rows are the ones that are NOT that, and §4 says why.

---

# 3. The mechanism, with one unit's values in motion

## 3.1 The unit

`cpp/regen_12920` divides a half-float by a half-float. `/` is c++'s
division operator; the probe's two arguments arrive as half floats, so
the compiler has to widen them, divide as ordinary floats, and narrow
the answer back.

## 3.2 What its stored body says

LITERAL — `canon39_callee_printed.txt`, part 6, the unit's own
`body_verbatim` as canon39 stores it:

```
    0  push %rax
    1  cvtsi2ss %edi,%xmm1
    2  movss %xmm1,0x4(%rsp)
    3  call L0 !!reloc=R_X86_64_PLT32:__extendhfsf2-0x4
    4  L0:
    5  movss 0x4(%rsp),%xmm1
    6  divss %xmm0,%xmm1
    7  movaps %xmm1,%xmm0
    8  call L1 !!reloc=R_X86_64_PLT32:__truncsfhf2-0x4
    9  L1:
   10  pop %rax
   11  ret
```

GLOSS, following the values: an argument arrives in `%edi`, line 1
turns it into a float in `%xmm1`, line 2 parks it, line 3 transfers
into `__extendhfsf2` — and the transfer's own text says `call L0`,
the very next instruction. That is the log_161 finding: the object
file is not linked, so the displacement is zero and the disassembler
reads the transfer as going one instruction forward. The name
`__extendhfsf2` exists ONLY in the relocation stapled to the line.
Line 6 divides, line 8 transfers into `__truncsfhf2` to narrow the
result, and line 11 returns it.

## 3.3 The body that was attached to line 3

LITERAL — the same transcript, the callee arch unit
`runtime/clang++/__extendhfsf2`:

```
  archive: /usr/lib/llvm-21/lib/clang/21/lib/linux/libclang_rt.builtins-x86_64.a
  member:  extendhfsf2.c.o
  symbol at 0x0, size 0x77
  arrival families (read before written): xmm0, rax
    0  endbr64
    1  pextrw $0x0,%xmm0,%eax
    2  mov %eax,%edx
    3  shr $0xa,%edx
    4  and $0x1f,%edx
    5  mov %eax,%ecx
    6  and $0x3ff,%ecx
    7  test %edx,%edx
    8  je 2f <__extendhfsf2+0x2f>
    9  cmp $0x1f,%edx
   10  jne 51 <__extendhfsf2+0x51>
   11  movzwl %cx,%edx
   12  shl $0xd,%edx
   13  mov $0xff,%esi
   14  jmp 63 <__extendhfsf2+0x63>
   15  test %cx,%cx
   16  je 5f <__extendhfsf2+0x5f>
   17  movzwl %cx,%edx
   18  bsr %edx,%ecx
   19  xor $0x1f,%ecx
   20  mov $0x86,%esi
   21  sub %ecx,%esi
   22  add $0xf8,%cl
   23  shl %cl,%edx
   24  xor $0x800000,%edx
   25  jmp 63 <__extendhfsf2+0x63>
   26  movzwl %dx,%esi
   27  add $0x70,%esi
   28  movzwl %cx,%edx
   29  shl $0xd,%edx
   30  jmp 63 <__extendhfsf2+0x63>
   31  xor %edx,%edx
   32  xor %esi,%esi
   33  shl $0x10,%eax
   34  and $0x80000000,%eax
   35  shl $0x17,%esi
   36  or %eax,%esi
   37  or %edx,%esi
   38  movd %esi,%xmm0
   39  ret
```

GLOSS, with a value moving: take the half float `0x3C00`, which is
1.0. Line 1 lifts the sixteen bits into `%eax`. Lines 3–4 shift the
exponent field down and mask it: `0x3C00 >> 10 = 0xF`, and `0xF & 0x1F`
is 15. Lines 5–6 mask out the fraction field: `0x3C00 & 0x3FF` is 0.
Line 7 tests the exponent — 15 is not zero, so line 8's branch is not
taken. Line 9 compares it against 31 — 15 is not 31, so line 10's
branch IS taken, to line 26. There the exponent is rebiased,
`15 + 0x70 = 0x7F`, the fraction is shifted up thirteen places, and
lines 33–38 reassemble sign, exponent and fraction into `%xmm0`:
`0x7F << 23` is `0x3F800000`, which is 1.0 as a 32-bit float.

That walk is exactly what the reference cannot yet do on its own,
because it walks a body in text order and refuses at line 8. Following
those branches is task 64's work; what this task delivers is the body
being there to follow.

## 3.4 The caller's answer row after attachment

LITERAL — the same transcript:

```
  produced_by: {"callee": "__truncsfhf2", "kind": "runtime_callee"}
  it was:      {"kind": "arch_opcode", "mnem": "push"}
```

GLOSS: the answer row now names the routine that produced it. What it
named before is kept beside it: an `arch_opcode` producer, the stack
opcode the ledger had traced the result register back to — which is
this unit's bookkeeping, not the thing that computed the answer. A
body
that transfers into the runtime more than once — this one does,
twice — leaves the LAST transfer in its own text order standing on
the answer row, and `produced_by_was` keeps the ORIGINAL producer, not
the previous attachment's.

---

# 4. Attached and not attached, by cause, per language

## 4.1 The tallies

LITERAL — `canon39_callee_attachments.json`, its `meta`:

```
"call_bearing": 4119,
"attached": 3923,
"attached_by_language": {"c": 1579, "cpp": 2327, "rust": 4,
                         "swift": 13}
```

| language | call-bearing | attached | not attached |
|---|---|---|---|
| c | 1,579 | 1,579 | 0 |
| cpp | 2,327 | 2,327 | 0 |
| rust | 30 | 4 | 26 |
| go | 170 | 0 | 170 |
| swift | 13 | 13 | 0 |
| **total** | **4,119** | **3,923** | **196** |

## 4.2 The two causes, and why neither is a gap

LITERAL — the same file, `not_attached_by_cause_per_language`,
shortened here to the cause text and the counts:

```
go   170  this body's transfer carries no relocation and no archive
          index defines its target: it is the language's own runtime
          panic path, not the compiler's lowering of an operation the
          hardware lacks
rust  26  no builtins archive of the caller's own toolchain (rustc)
          defines the names this body transfers to:
          ..._panic_const_div_by_zero / _rem_by_zero /
          _div_overflow / _rem_overflow
```

GLOSS: go's transfers are to `x_runtime_panicshift`,
`x_runtime_panicdivide`, `x_runtime_newobject` and
`x_runtime_morestack_noctxt_abi0`; rust's are to four
`core::panicking::panic_const` routines. `is_runtime_routine` answers
NO for every one of them, from the archive index, not from a list of
names this code believes in. They are the language's own runtime
reacting to a condition, not the compiler computing an answer — the
same distinction log_153 §3.4 drew for five go units, now measured
over the whole population.

## 4.3 The four swift callers of the recorded 308-unit list

LITERAL — `canon39_callee_printed.txt`, part 5:

```
  swift/regen_315    __divti3     outcome in canon39: REFUSED
      callee body referenced: True   answer row repointed: this
      caller record carries no ledger
  swift/regen_321    __udivti3    outcome in canon39: REFUSED   ...
  swift/regen_327    __modti3     outcome in canon39: REFUSED   ...
  swift/regen_333    __umodti3    outcome in canon39: REFUSED   ...
```

GLOSS: these four are not in the 4,119, because canon39 REFUSED their
wrapped text and the census walks proved units only. Their callee
bodies are now extracted from swift's own archive and referenced on
the caller's record; their answer row is not repointed because a
refused unit was never given a ledger to hold rows in. That is a
statement about those four units' outcome, not about the attachment.

---

# 5. The three mechanism changes, each with its evidence

## 5.1 A callee is located by address and size, not by name

LITERAL — run on this machine this session:

```
$ nm -S --defined-only /tmp/rcx/comparetf2.c.o | head -4
0000000000000000 00000000000000b9 T __cmptf2
0000000000000000 00000000000000b9 T __eqtf2
00000000000000c0 00000000000000b4 T __getf2
00000000000000c0 00000000000000b4 T __gttf2

$ objdump -dr --disassemble=__netf2 /tmp/rcx/comparetf2.c.o
comparetf2.c.o:     file format elf64-x86-64
Disassembly of section .text:
```

GLOSS: `__netf2`, `__eqtf2`, `__letf2`, `__lttf2` and `__cmptf2` are
five names for one address, and objdump labels that address with the
first name it holds — so asking for `__netf2` by name prints a header
and no body at all. Task 59 never met this, because the four division
routines each own their address. `RuntimeCallee.extract_callee` now
reads the symbol's address and size out of `nm -S --defined-only` and
disassembles that RANGE, which answers for every name at that address.
The rule is written into the CORE's settled rules.

## 5.2 Nested callees, followed with a cycle guard

LITERAL — `canon39_callee_printed.txt`, part 3, four of the 76 rows:

```
  clang++/__divti3                 27 instructions   nested: __udivmodti4
  clang++/__floattisf              77 instructions   nested: __clzti2
  clang++/__modti3                 38 instructions   nested: __udivmodti4,__stack_chk_fail
  clang++/__udivmodti4             91 instructions   nested: -
```

and the summary line:

```
callee arch units extracted: 76
of those, reached ONLY as a nested callee of another body: 6
  (clang++/__clzti2, clang++/__udivmodti4, clang/__clzti2,
   clang/__udivmodti4,
   rustc/_RNvNtNtCsNDsy69z6bA_17compiler_builtins3int19specialized_div_rem12u128_div_rem,
   swiftc/__udivmodti4)
  NOT EXTRACTED clang++/__stack_chk_fail  the archive index of
      toolchain 'clang++' defines no symbol named __stack_chk_fail
  NOT EXTRACTED clang/__stack_chk_fail    (the same)
```

GLOSS: six routines are reached only from inside another routine.
`__udivmodti4` is where all four division routines actually do the
division; `__clzti2` counts leading zeros for the integer-to-float
conversions. `__stack_chk_fail` is refused BY THE SAME RULE that
admits the others — no builtins archive defines it, because it is
libc's, not the compiler's own lowering. The guard against a cycle is
a set of already-extracted names, so a routine that reaches itself is
extracted once.

## 5.3 Swift, extracted inside the instance where swift lives

LITERAL — `canon39_callee_swift_lane_printed.txt`, the lane's own log
from inside the `trickle` instance:

```
--- which side of the wall ---
uname:   Linux 4963c357a353 7.0.0-30-generic ...
lrwxrwxrwx 1 root root 12 Dec 11  2024 /persist/swift/usr/bin/swiftc -> swift-driver

== WHICH SIDE OF THE CONTAINER WALL IS THIS? ==
  /persist/swift/usr/bin/swiftc      exists: True
  /out                               exists: True

$ /persist/swift/usr/bin/swiftc --version
  Swift version 6.0.3 (swift-6.0.3-RELEASE)
  Target: x86_64-unknown-linux-gnu
$ /persist/swift/usr/bin/clang -print-file-name=libclang_rt.builtins-x86_64.a
  /persist/swift/usr/lib/clang/17/lib/linux/libclang_rt.builtins-x86_64.a

the archive's own symbol index names 155 defined symbols
```

and the bodies it extracted:

```
  swiftc/__divti3                26 instructions   nested: __udivmodti4
  swiftc/__extendhfsf2           33 instructions   nested: -
  swiftc/__modti3                31 instructions   nested: __udivmodti4
  swiftc/__truncsfhf2            79 instructions   nested: -
  swiftc/__udivmodti4            90 instructions   nested: -
  swiftc/__udivti3                2 instructions   nested: __udivmodti4
  swiftc/__umodti3                7 instructions   nested: __udivmodti4
```

GLOSS: the archive path is READ BACK from swift's own clang, never
typed. `/persist/swift` exists only inside the instance, which is what
the path check at the top proves. Swift's `__extendhfsf2` is 33
instructions where clang 21's is 40 — a different compiler version
lowering the same operation differently, which is exactly why the CORE
forbids taking a callee from another toolchain's archive.

The commands, exactly as run:

```
bash ~/Programming/Airlock/up.sh --instance trickle
python3 ~/Programming/Airlock/airlock --instance trickle submit \
    ~/Programming/PseudoCoupHQ/Research/op_pipeline/runtime_callee_swift_lane2.sh \
    --batch t63 --weight 1
AIRLOCK_INSTANCE=trickle bash ~/Programming/Airlock/progress.sh status
bash ~/Programming/Airlock/down.sh --instance trickle
```

The instance was brought down when the lane was done; the lane exited
0 in 1.2 seconds.

---

# 6. Task (c) — the arch opcodes the archive bodies spell

## 6.1 What was missing, computed

LITERAL — `~/Programming/PseudoCoupHQ/Research/op_pipeline/acceptance63_printed.txt`,
part 0:

```
attached bodies: 76   body lines: 4002   distinct arch opcodes: 73
in the table: 73   NOT in the table: 0

the opcodes THIS TASK ADDED, with their sighting counts:
  endbr64       64 lines   first seen: clang++/__clzti2 | endbr64
  bsr           30 lines   first seen: clang++/__clzti2 | bsr %rcx,%rcx
  inc           14 lines   first seen: clang++/__extendxftf2 | inc %rax
  bt             8 lines   first seen: clang++/__floattidf | bt $0x37,%rcx
  cmova          4 lines   first seen: clang++/__truncsfbf2 | cmova %esi,%edx
  pinsrw         4 lines   first seen: clang++/__truncsfbf2 | pinsrw $0x0,%edx,%xmm0
  cs             2 lines   first seen: clang++/__udivmodti4 | cs nopw 0x0(%rax,%rax,1)
  fld            2 lines   first seen: clang++/__extendxftf2 | fld %st(0)
  xchg           1 lines   first seen: swiftc/__udivmodti4 | xchg %ax,%ax

STILL MISSING: none -- every arch opcode the attached bodies spell has
an entry.
```

GLOSS: nine, not two. The brief named `endbr64` and `bsr`; the
computation found seven more. They are entries in the ONE table, with
reads, writes and a term builder — not a second table beside it. The
opcode_table CORE's rule is unchanged and now says explicitly that the
corpus it is built over includes the attached bodies.

## 6.2 Each one, on a real line, with values moving

LITERAL — `acceptance63_printed.txt`, part 1, three of the nine:

```
  LITERAL  bsr %edx,%ecx  (from clang++/__extendhfsf2)
  GLOSS    writes the position of the highest set bit of its source,
           counting from zero at the low end
  reads ('the operands the opcode names',)
  writes ('the last named operand', 'the flags')
  before   %edx = 0x140 = 0b1_0100_0000, %ecx = 0
  after    %ecx = 8
  note     0x140's highest set bit is bit 8, and 8 is what the machine
           writes

  LITERAL  inc %eax  (from clang++/__truncsfbf2)
  GLOSS    adds one to the place it names, and leaves the carry flag
           exactly as it found it
  before   %eax = 0x28 = 40
  after    %eax = 41
  note     the flag triple left behind is 'inc', so a later carry read
           REFUSES rather than inventing one

  LITERAL  bt $0x37,%rcx  (from clang++/__floattidf; run here with
           $0x3 over 0xff)
  GLOSS    copies one numbered bit of its second operand into the
           carry flag, and touches nothing else
  before   %rcx = 0xff, so bit 3 is 1
  after    %al = 1
  note     the carry, and only the carry: a zero or sign reading after
           `bt` is refused
```

GLOSS on the choice of model: `inc` and `bt` both leave part of the
flag state untouched or undefined, and in both cases the entry records
a flag triple that names ITSELF, so that a reading the machine does
not actually define is REFUSED rather than answered with something
plausible. That is the refusal posture the line already holds.

## 6.3 One further cause, fixed where it lives

Eight of the 76 bodies stopped on `%fs:0x28` — a read through a
segment base, which is where the stack-protector cookie is kept.
`__modti3`, `__umodti3`, `__floattixf` and `__floatuntixf` in both
clang's and clang++'s archives begin by loading it.

That is not an opcode gap and not a shape the tree lacks: it is a
memory operand, and every other memory operand in this reference is
read as an unconstrained cell keyed by its own text. `Operands.is_memory`
now recognizes `%fs:` and `%gs:`, which claims nothing about the value
and refuses nothing. Fixed at first observation, in the shared layer.

LITERAL — `acceptance63_printed.txt`, part 2, after the fix:

```
attached bodies: 76
walked to the end: 2
stopped at a transfer (TASK 64's branch following): 74
stopped on an opcode the table lacks: 0
stopped for another reason: 0
```

GLOSS: every attached body now stops only where task 64 takes over.

## 6.4 Nothing that already answered was moved

LITERAL — `~/Programming/PseudoCoupHQ/Research/op_pipeline/regression63_printed.txt`:

```
population: canon39's proved units; SAMPLE of 3000 drawn from 40
stores, seed 63
the module before this task: 7a560e5:Research/op_pipeline/reference.py
identical outcome:            3000
refusal -> term (a gain):     0
CHANGED ANSWER (a regression): 0
```

GLOSS: `regression63.py` loads BOTH versions of `reference.py` side by
side — the working tree's and the one git holds at the commit before
this task's first edit — and asks each for the same unit's answer term.
Over a 3,000-unit sample the two agree character for character, every
time. Evidence class: sampled observation, which REFUTES rather than
proves; task 64 re-gates the whole population, and that is where the
proof is. The gain column is zero by construction: the nine added
opcodes appear only in the archive bodies, and stepping into an
attached body is task 64's, not this task's.

---

# 7. The guard, the tree, and what was and was not edited

## 7.1 The unmodified guard, one process

LITERAL — `~/Programming/PseudoCoupHQ/Research/op_pipeline/guard63_transcript.txt`:

```
guard63.py -- every artifact task 63 writes, unmodified guard, ONE
process.  Nothing was added to any field set, and no artifact was
declared out of the walk.
$ python3 check_no_spelling_keys.py <6 paths, one process>

operator inventory: 91 tokens read from probe_manifest_*.json
PASS canon39_callee_units.json -- no operator token in any key,
     grouping, pairing or row structure
PASS canon39_callee_attachments.json -- ...
PASS canon39_callee_census.json -- ...
PASS canon39_callee_opcodes.json -- ...
PASS canon39_callee_swift_lane.json -- ...
PASS regression63.json -- ...

GUARD EXIT CODE = 0
```

```
$ cd ~/Programming/PseudoCoupHQ/Research/op_pipeline && grep -c exempt guard63_transcript.txt
0
$ git -C ~/Programming/PseudoCoupHQ diff --stat Research/op_pipeline/check_no_spelling_keys.py
(no output — the checker is unmodified)
```

**The guard caught one of my own artifacts, and the fix was a shape,
not an exemption.** The first run of `canon39_callee_opcodes.json`
keyed two objects by the arch mnemonic, and four arch mnemonics —
`and`, `or`, `xor`, `not` — are spelled the same as operator tokens:

```
FAIL canon39_callee_opcodes.json -- 8 spelling-keyed place(s)
     $.first_seen.and       dict key is the operator token 'and'
     $.sightings_by_opcode.or   dict key is the operator token 'or'
     ...
```

The file now carries a LIST of typed objects with a `mnem` field, and
passes. No field was added to any set and no exemption was declared.

## 7.2 The tree was corrected before the code

Two COREs gained settled rules before any of this was written, per
log_158's binding rule 3:

- `CORE_0_3_5_1_8_runtime_callee.md` — four new settled rules
  (locate by address and size; nested callees followed relocation-aware
  with a cycle guard; a callee the archive index does not define is not
  attached and its cause is recorded; the mnemonics the archive bodies
  spell join the one opcode table), plus `extract_closure` in the
  `## design` block and a realization table for this task's files.
- `CORE_0_3_5_4_0_opcode_table.md` — one new settled rule: the corpus
  the table is built over includes the attached callee bodies.

LITERAL — `python3 ~/Programming/PlanPlan/framework/check_plans.py ~/Programming/PseudoCoupHQ/Planning`:

```
summary: 4 error(s), 3 warning(s)
[ERROR] dangling-path: ~/Programming/PseudoCoupHQ/DevComms/log_107_task21_interp_ does not exist
[ERROR] dangling-path: ~/Programming/PseudoCoupHQ/DevComms/log_110_task25_ does not exist
[ERROR] dangling-path: ~/Programming/SandboxDesign/allow.sh does not exist
[ERROR] dangling-path: ~/Programming/Sources/llvm- does not exist
```

GLOSS: all four are truncated paths in files this task did not touch,
and all four predate it. Dashboards were regenerated —
`wrote 67 dashboard(s)`.

## 7.3 Which files were edited rather than added

Two live modules were extended, and this is the reasoning, stated
rather than assumed. The brief allows editing `ledger.py` and
`reference.py`; `runtime_callee.py` is not named in either list.

- `reference.py` — allowed by the brief, and edited: the nine opcode
  entries, their builders, the segment-relative memory operand, and
  `ARCHIVE_MNEMONICS` extending the inventory the table prunes to.
- `runtime_callee.py` — edited, on the ground that it carries this
  node's own name, which log_158's binding rule 1 makes the node's
  live module in exactly the way `ledger.py` and `reference.py` are
  theirs. It is round-12 code, not a superseded record. The additions
  are additive — `member_symbols`, `disassemble_range`,
  `fold_relocations`, `nested_callees`, `extract_closure` — plus two
  changes inside `extract_callee` (address-range disassembly, and the
  unit name gaining its toolchain) and one inside `attach` (keep the
  ORIGINAL `produced_by_was` when a body transfers twice).
- `ledger.py` — READ, not edited. Its `positional_labels` is called to
  put an attached body into the same label form every other stored
  body has.
- Nothing under `ledger47`/`ledger48`, `canon*`, `gate48` or `layer4*`
  was touched, and `runtime_callee_run.py` — task 59's run script —
  was left exactly as it is.

---

# 8. File inventory

## 8.1 Written by this task

Under `~/Programming/PseudoCoupHQ/Research/op_pipeline/`:

| file | what it is |
|---|---|
| `runtime_callee_generalized_run.py` | the run: census, verdicts, extraction, attachment, the printed unit |
| `runtime_callee_swift_lane.py` | the swift half, run inside the `trickle` instance |
| `runtime_callee_swift_lane.sh` | the lane script (first run) |
| `runtime_callee_swift_lane2.sh` | the same lane rerun with the ncurses symlink, so `swiftc` itself answers |
| `acceptance63.py` | task (c): the opcode inventory, each new opcode on a real line, the walk |
| `regression63.py` | both versions of `reference.py` asked the same question |
| `guard63.py` | the unmodified guard, one process, over all six JSON artifacts |
| `canon39_callee_census.json` | which units carry a transfer, and to what |
| `canon39_callee_units.json` | the 76 callee arch units |
| `canon39_callee_attachments.json` | one row per call-bearing unit |
| `canon39_callee_opcodes.json` | the opcode inventory of the attached bodies |
| `canon39_callee_swift_lane.json` | the lane's product, copied back from the instance |
| `canon39_callee_printed.txt` | the run's transcript |
| `canon39_callee_swift_lane_printed.txt` | the lane's own log, copied back |
| `acceptance63_printed.txt` | task (c)'s transcript |
| `regression63_printed.txt`, `regression63.json` | the before/after check |
| `guard63_transcript.txt`, `guard63.json` | the guard's transcript and counts |

## 8.2 Edited

- `~/Programming/PseudoCoupHQ/Research/op_pipeline/runtime_callee.py`
- `~/Programming/PseudoCoupHQ/Research/op_pipeline/reference.py`

## 8.3 Plan files touched

- `~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_1_arch_unit/node_0_3_5_1_8_runtime_callee/CORE_0_3_5_1_8_runtime_callee.md`
- `~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_1_arch_unit/node_0_3_5_1_8_runtime_callee/PROGRESS.md`
- `~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_4_reference/node_0_3_5_4_0_opcode_table/CORE_0_3_5_4_0_opcode_table.md`
- `~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_4_reference/node_0_3_5_4_0_opcode_table/PROGRESS.md`
- 67 `DASHBOARD.md` files, regenerated by
  `python3 ~/Programming/PlanPlan/framework/generate_dashboards.py ~/Programming/PseudoCoupHQ/Planning`

---

# 9. What task 64 receives, and the one thing it should know

- 3,923 call-bearing units carry a `runtime_callees` reference and an
  answer row that names the routine producing it, in
  `canon39_callee_attachments.json`.
- 76 callee arch units are in `canon39_callee_units.json`, each with
  its own `body_verbatim` in the positional-label form, its bytes, its
  arrival families, and the names it itself transfers to.
- Every arch opcode those bodies spell has an entry in the one table,
  so nothing stops on a missing meaning: 74 of the 76 stop at a
  transfer, and 2 walk to the end.
- **The one thing to know:** an attached body BRANCHES, heavily —
  `__extendhfsf2` has five transfers in forty instructions. Stepping
  into a callee and following its branches are the same problem, not
  two, and the branch model has to exist before the step-in pays.
