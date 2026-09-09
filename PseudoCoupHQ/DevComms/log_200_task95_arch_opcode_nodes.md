# log 200 — task 95: the arch-opcode-node, detected from compiler source alone

Date: 2026-09-05. Instance `sandbox` (default). Node:
`hq.research.compiler_graph.graph`, the heading **"the arch-opcode-node —
a shape this node lacks, added 2026-09-05"** in
`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_9_graph/CORE_0_3_5_9_graph.md`.
the owner, 2026-09-05: *"is there a way to know which parts of the compiler
produces arch-opcodes (arch-units)? … i mean just by analyzing the
compiler source code. like if the compiler produces an arch opcode, its
an arch-opcode-node."*

Every rendering in this log is labelled per the protocol's §5.1a:
**LITERAL** is the object itself quoted from a file or a lane log,
**GLOSS** is a plain-words reading sitting beside a literal, and
**ANALOGY** is something that resembles the thing and is not it. No gloss
appears without its literal.

---

# 1. What was done, in plain words

## 1.1 The one-line account

`Graph.arch_opcode_nodes` was added to `Research/compiler_graph/graph.py`
beside `coverage` and `variant_connections`; it reads each region's
compiler source AT ITS PIN, finds every call site of that region's
instruction emitter, grades the opcode argument in four states, and
marks every definition node of the graph with one of them — **with no run
of the compiler and no diary**, which is why it reaches rust and swift,
the two this machine cannot instrument.

## 1.2 The numbers that matter, each with its population

**LITERAL**, lane `t95_l10_own_evidence.sh` §[1/8]:

```
$ python3 -c "import json;d={l:json.load(open('PseudoCoupGraphs/arch_opcode_nodes_%s.json'%l)) for l in ('go','cpp','rust','swift')};[print(l, d[l]['by_state'], 'sum', sum(d[l]['by_state'].values()), 'population', d[l]['populations']['definitions']) for l in d]"
go {'names_its_opcode': 13, 'one_static_hop': 39, 'emits_opcode_dynamic': 5, 'emits_nothing': 1802} sum 1859 population 1859
cpp {'names_its_opcode': 174, 'one_static_hop': 8, 'emits_opcode_dynamic': 69, 'emits_nothing': 10538} sum 10789 population 10789
rust {'names_its_opcode': 0, 'one_static_hop': 0, 'emits_opcode_dynamic': 1, 'emits_nothing': 3312} sum 3313 population 3313
swift {'names_its_opcode': 1, 'one_static_hop': 0, 'emits_opcode_dynamic': 1, 'emits_nothing': 10086} sum 10088 population 10088
```

**GLOSS.** Four states, and they PARTITION the definition population in
every region — the sums are 1,859 / 10,789 / 3,313 / 10,088 against
populations of exactly those sizes. The method asserts the partition
itself and would raise rather than print a marking that does not close.

- **57 of 1,859** go definitions produce a machine instruction; **1,802
  of 1,859** produce none.
- **251 of 10,789** clang definitions produce one; **10,538 of 10,789**
  produce none.
- **1 of 3,313** rust definitions reaches an instruction-shaped emitter
  at all, and it names no opcode; **3,312 of 3,313** produce none.
- **2 of 10,088** swift definitions; exactly **1** of them NAMES its
  instruction, and that one is real.
- The coordinator's own go measurement is reproduced exactly from this
  task's artifact: **50** `Prog` call sites pass an x86 constant,
  **24** distinct opcodes. See §6.1.

## 1.3 What is NOT claimed

- **Not** that these definitions are the only ones that matter to opcode
  production. They are the ones whose OWN SOURCE names or reaches an
  instruction. A definition that computes the operand of an instruction
  emitted three frames away is in `emits_nothing`, correctly, and the
  caller closure in §5 is how that reach is measured.
- **Not** that a `one_static_hop` definition emits ONE opcode. go's hop
  through `Op.Asm()` resolves to the whole amd64 opcode table — **564**
  distinct opcodes at every such site. The hop BOUNDS the set; it does
  not pin a member. §4.2 says so with the number.
- **Not** that entering is emitting. §6 keeps the two apart in both
  directions and reports each side's exclusive part.
- **Not** that rust and swift were run. Nothing was compiled in this
  task. Their rows for `diary`, `coverage` and `variant_connections`
  stay **planned**, exactly as log_175 §6.3–6.4 left them.
- **Not** that the `.td` files served as the instruction table the CORE
  expected them to be. They could not, for a measured reason. §8.1.

---

# 2. The instrument

## 2.1 The four states, and where they come from

The CORE names three grades and says everything else emits nothing. The
method implements exactly that, and the third is a CATEGORY, never a
failure:

| state | meaning |
|---|---|
| `names_its_opcode` | a call site of the emitter passes a CONSTANT; the opcodes are recorded |
| `one_static_hop` | the opcode argument reads a STATIC TABLE; the hop is followed and the opcodes it yields recorded |
| `emits_opcode_dynamic` | an emitter whose opcode cannot be named from source. Never guessed |
| `emits_nothing` | no emitter call site — the droppable set |

A definition takes the FIRST of these that any of its call sites reaches.

## 2.2 Language-agnostic by construction, the way `build` already is

**LITERAL**, `Research/compiler_graph/graph.py`, the block above
`class Graph`:

```
ARCH_OPCODE_RULES = {
    "go": {
        "extensions": (".go",),
        "arch_token": r"\bx86\.A([A-Z][A-Za-z0-9_]*)\b",
        "pseudo_token": r"\bobj\.A([A-Z][A-Za-z0-9_]*)\b",
        "emitter_parameter_type": r"\bobj\.As\b",
        ...
```

**GLOSS.** Everything per-language is DATA — the arch-opcode namespace,
the pseudo-opcode namespace, the emitter openers and which argument of
each carries the opcode. The walk itself never names a language. This is
the `LanguagePack` pattern `build` already uses, applied again.

## 2.3 Where each region's emitter was LOCATED, not assumed

go's shape was NOT carried over. Each region was searched from its own
source first.

### go — the machine-form rule finds it

An emitter is a function that TAKES the arch opcode type; a table is one
that RETURNS it. Both are read off the declaration.

**LITERAL**, lane `t95_l13_own_evidence3.sh` §[1/8]:

```
$ python3 PseudoCoupHQ/Research/compiler_graph/lanes_t95/t95_show.py declarations go
go: 7 declarations of the arch opcode type
  src/cmd/compile/internal/amd64/ssa.go:67  returns the arch opcode type -- a TABLE
     func loadByRegWidth(r int16, width int64) obj.As {
  src/cmd/compile/internal/amd64/ssa.go:83  returns the arch opcode type -- a TABLE
     func storeByRegWidth(r int16, width int64) obj.As {
  src/cmd/compile/internal/amd64/ssa.go:121  returns the arch opcode type -- a TABLE
     func moveByRegsWidth(dest, src int16, width int64) obj.As {
  src/cmd/compile/internal/amd64/ssa.go:175  takes the arch opcode type -- an EMITTER
     func opregreg(s *ssagen.State, op obj.As, dest, src int16) *obj.Prog {
  src/cmd/compile/internal/ssa/opGen.go:115435  returns the arch opcode type -- a TABLE
     func (o Op) Asm() obj.As          { return opcodeTable[o].asm }
  src/cmd/compile/internal/ssagen/ssa.go:6742  takes the arch opcode type -- an EMITTER
     func (s *State) Prog(as obj.As) *obj.Prog {
  src/cmd/compile/internal/ssagen/ssa.go:6771  takes the arch opcode type -- an EMITTER
     func (s *State) Br(op obj.As, target *ssa.Block) *obj.Prog {
```

And the two of those the CORE names, read straight from the pin -- lane
`t95_l13_own_evidence3.sh` §[4/8]:

```
$ git -C /sources/golang_src show 9f1012d9a1aa0831ff44ac9c767e96f9943d13fe:src/cmd/compile/internal/ssagen/ssa.go | sed -n '6742,6743p'
func (s *State) Prog(as obj.As) *obj.Prog {
	p := s.pp.Prog(as)

$ git -C /sources/golang_src show 9f1012d9a1aa0831ff44ac9c767e96f9943d13fe:src/cmd/compile/internal/ssa/opGen.go | sed -n '115435p'
func (o Op) Asm() obj.As          { return opcodeTable[o].asm }
```

**GLOSS.** Three emitters and four tables, and the CORE's own hop —
`Op.Asm()` reading `opcodeTable` in the generated `ssa/opGen.go` — falls
out of the same rule rather than being named by hand.

### cpp — the four instruction-building openers

**LITERAL**, lane `t95_l10_own_evidence.sh` §[2/8]:

```
$ python3 -c "import json;[print(l, json.load(open('PseudoCoupGraphs/arch_opcode_nodes_%s.json'%l))['emitter_census']) for l in ('go','cpp','rust','swift')]"
go {'Prog': 206, 'Br': 9, 'opregreg': 23}
cpp {'BuildMI': 724, 'setDesc': 57, 'MCInstBuilder': 53, 'setOpcode': 36}
rust {'InlineAsmCall': 0, 'LLVMRustInlineAsm': 0, 'inline_asm_call': 2}
swift {'InlineAsm': 5}
```

**GLOSS.** `BuildMI` and `setDesc` carry the opcode inside their
`get(...)`; `MCInstBuilder` and `setOpcode` carry it first. The argument
is taken from its POSITION in the call, which is why `X86::EAX` and
`X86::RAX` — registers, not instructions — never reach the grader. A
first cut that keyed on "any `X86::` token anywhere in the call" did
count them, and lane `t95_l3_recon2.sh` §[3/6] holds that wrong reading
as the record.

### rust — LOCATED, and it is OUTSIDE the region

**LITERAL**, lane `t95_l13_own_evidence3.sh` §[2/8] -- and the swift
line is printed here too, because the two answers are the same:

```
$ grep -rl --include='*.rs' --include='*.cpp' --include='*.h' -e 'BuildMI(' -e 'MCInst' -e 'MachineInstr' -e 'X86::' /sources/rust | wc -l
0

$ grep -rl --include='*.cpp' --include='*.h' -e 'BuildMI(' -e 'MCInst' -e 'MachineInstr' -e 'X86::' /sources/swift-6.0.3-RELEASE | wc -l
0
```

**GLOSS.** Not "we could not find one". Zero files in the WHOLE rust
checkout — not merely the region — name any instruction-building
construct. rustc's region emits LLVM IR; LLVM emits the instruction; and
LLVM's source IS the cpp region, where it is measured. This is written
onto the rust artifact as a named frontier, quoted in §7.1.

### swift — the same, with one measured exception

**LITERAL**, lane `t95_l13_own_evidence3.sh` §[3/8], read from the pin:

```
$ git -C /sources/swift-6.0.3-RELEASE show 6a862d2eb7128ff1f317b07e8ad1a6da939775f3:lib/IRGen/IRGenSIL.cpp | sed -n '5571,5580p'
void IRGenSILFunction::visitDebugStepInst(DebugStepInst *i) {
  // Unfortunately there is no LLVM-equivalent of a debug_step instruction.
  // Also LLVM doesn't provide a plain NOP instruction.
  // Therefore we have to solve this with inline assembly.
  // Strictly speaking, this is not architecture independent. But there are
  // probably few assembly languages which don't use "nop" for nop instructions.
  auto *AsmFnTy = llvm::FunctionType::get(IGM.VoidTy, {}, false);
  auto *InlineAsm = llvm::InlineAsm::get(AsmFnTy, "nop", "", true);
  Builder.CreateAsmCall(InlineAsm, {});
}
```

**GLOSS.** The swift compiler spells a machine instruction itself, once,
in an inline-assembly template, and its own comment says the line is
"not architecture independent". So swift's emitter is the inline-assembly
constructor and its opcode argument is the template string.

---

# 3. The four-state marking, per region

## 3.1 go — 1,859 definitions

| state | definitions | of population | call sites |
|---|---|---|---|
| names_its_opcode | 13 | 1,859 | 84 |
| one_static_hop | 39 | 1,859 | 129 |
| emits_opcode_dynamic | 5 | 1,859 | 25 |
| emits_nothing | 1,802 | 1,859 | — |
| **emitters, all three states** | **57** | **1,859** | **238** |

Of the 13 state-1 definitions, **6** name at least one ARCH opcode and
**7** name only PSEUDO opcodes (`obj.ACALL`, `obj.AFUNCDATA`,
`obj.APCDATA`, `obj.ARET`, `obj.AJMP`, `obj.APCALIGNMAX`). A pseudo-op
still NAMES its opcode, so the state is right; it is not a machine
instruction, so the inverse index carries only the arch ones and the
split is reported rather than blurred.

The 57 sit in **4 files**: `amd64/ssa.go` 46, `ssagen/ssa.go` 9,
`amd64/ggen.go` 1, `ssagen/abi.go` 1 (lane `t95_l8_split_and_guard.sh`
§[2/5]).

## 3.2 cpp, serving c and cpp — 10,789 definitions

| state | definitions | of population | call sites |
|---|---|---|---|
| names_its_opcode | 174 | 10,789 | 578 |
| one_static_hop | 8 | 10,789 | 27 |
| emits_opcode_dynamic | 69 | 10,789 | 265 |
| emits_nothing | 10,538 | 10,789 | — |
| **emitters** | **251** | **10,789** | **870** |

Of the 174 state-1 definitions, **138** name at least one arch opcode and
**36** name only pseudo opcodes. 15 of the 870 call sites sit outside any
definition node of the graph and are reported as such. The 251 sit in
**45 files**, headed by `X86InstrInfo.cpp` 38, `X86FastISel.cpp` 30,
`GISel/X86InstructionSelector.cpp` 23, `X86FrameLowering.cpp` 22,
`X86ISelLowering.cpp` 20, `X86MCInstLower.cpp` 14.

## 3.3 rust — 3,313 definitions, and swift — 10,088

| region | names_its_opcode | one_static_hop | emits_opcode_dynamic | emits_nothing | population |
|---|---|---|---|---|---|
| rust | 0 | 0 | 1 | 3,312 | 3,313 |
| swift | 1 | 0 | 1 | 10,086 | 10,088 |

**LITERAL**, lane `t95_l10_own_evidence.sh` §[5/8] — swift's five sites,
whole:

```
$ python3 -c "import json;d=json.load(open('PseudoCoupGraphs/arch_opcode_nodes_swift.json'));[print(c['file']+':'+str(c['line']), c['state'], c['argument']['text'], [k['text'] for k in c['opcodes']]) for c in d['call_sites']]"
lib/IRGen/GenDecl.cpp:2030 emits_nothing "" []
lib/IRGen/GenObjC.cpp:144 emits_opcode_dynamic asmString []
lib/IRGen/IRGenFunction.cpp:461 emits_nothing "" []
lib/IRGen/IRGenSIL.cpp:755 emits_nothing "" []
lib/IRGen/IRGenSIL.cpp:5578 names_its_opcode "nop" ['nop']
```

**GLOSS.** Three sites hand over an EMPTY template — an optimisation
barrier that emits no instruction, so they are `emits_nothing` and their
definitions are not emitters. One hands over `asmString`, read from
`TargetInfo.ObjCRetainAutoreleasedReturnValueMarker`, which is outside
the region: `emits_opcode_dynamic`, named, never guessed. One names
`nop`.

---

# 4. The inverse index — per arch opcode, which definitions emit it

## 4.1 The sizes

**LITERAL**, lane `t95_l10_own_evidence.sh` §[4/8]:

```
$ python3 -c "import json;[print(l, json.load(open('PseudoCoupGraphs/arch_opcode_nodes_%s.json'%l))['distinct_arch_opcodes'], json.load(open('PseudoCoupGraphs/arch_opcode_nodes_%s.json'%l))['distinct_pseudo_opcodes']) for l in ('go','cpp','rust','swift')]"
go 578 6
cpp 400 9
rust 0 0
swift 1 0
```

**GLOSS.** go's index holds **578** arch opcodes over 1,859 definitions;
cpp's holds **400** over 10,789. The index lives in each artifact at
`inverse_index`, one row per opcode carrying the definition ids that emit
it. A sample, lane `t95_l8_split_and_guard.sh` §[3/5]: `JCC_1` from 20
cpp definitions, `LEA64r` from 17, `MOV64ri` from 14, `CALL64pcrel32`
from 10.

## 4.2 Why go's index is LARGER than clang's, and what that costs

**LITERAL**, lane `t95_l11_own_evidence2.sh` §[3/3], the first rows:

```
57 emitter definitions
names_its_opcode       ginsnop src/cmd/compile/internal/amd64/ggen.go:28 1 opcodes
emits_opcode_dynamic   opregreg src/cmd/compile/internal/amd64/ssa.go:175 0 opcodes
names_its_opcode       getgFromTLS src/cmd/compile/internal/amd64/ssa.go:199 1 opcodes
names_its_opcode       ssaGenValue src/cmd/compile/internal/amd64/ssa.go:227 578 opcodes
names_its_opcode       zeroX15 src/cmd/compile/internal/amd64/ssa.go:1911 1 opcodes
one_static_hop         simdV11 src/cmd/compile/internal/amd64/ssa.go:1916 564 opcodes
one_static_hop         simdV21 src/cmd/compile/internal/amd64/ssa.go:1926 564 opcodes
```

**GLOSS, and it is a limit not a result.** The 39 `simd*` helpers each
carry **564 opcodes** because the hop `s.Prog(v.Op.Asm())` resolves to
the WHOLE amd64 row of `opcodeTable` — the source says which TABLE is
read, never which ROW. So a `one_static_hop` definition is bounded by 564
opcodes, not pinned to one. clang's `BuildMI(..., TII->get(X86::MOV64rr),
...)` names one, which is why cpp's index is sharper on 10,789
definitions than go's is on 1,859. Narrowing the go hop would need to
know which `Op` reaches the site, which is a run-time fact and therefore
`coverage`'s question, not this one's.

---

# 5. The emits-nothing set, and how much smaller each graph gets

**LITERAL**, lane `t95_l13_own_evidence3.sh` §[5/8] -- `kept` is the
share of the definition population that survives restriction to the
emitters and their callers:

```
$ python3 PseudoCoupHQ/Research/compiler_graph/lanes_t95/t95_show.py shrink
region  definitions  emitters  +direct  +all  emits_nothing  kept
go             1859        57       66    66           1802  3.6%
cpp           10789       251      319   356          10538  3.3%
rust           3313         1        2     6           3312  0.2%
swift         10088         2        3     4          10086  0.0%
```

**GLOSS.** Restricting each graph to its emitters and their callers keeps
**3.6%** of go's definitions and **3.3%** of clang's, and **0.2%** and
**0.0%** of rust's and swift's. That is the answer to the owner's "perhaps that
would shrink the graph size to only the relevant parts to opcode
production": for the two compilers that emit instructions, roughly
one definition in thirty; for the two that do not, effectively none.

**A BOUND ON THAT CLOSURE, stated rather than hidden.** The caller sets
are computed over the graph's own RESOLVED `calls` edges. Every
unresolved call is already a named frontier OF THE GRAPH, and it is
large — go 6,374 unresolved and 2,094 ambiguous calls, cpp 94,656 and
26,124 (lane `t95_l9_guard_fix_rerun.sh` §[5/7]). So the closure is a
LOWER BOUND on who reaches an emitter, and the number to quote is the
emitter set itself, which needs no edges at all.

---

# 6. The static emitter set against what RUNNING the compiler showed

## 6.1 First, the coordinator's own go numbers, recounted

**LITERAL**, lane `t95_l10_own_evidence.sh` §[4/8]:

```
$ python3 -c "import json;d=json.load(open('PseudoCoupGraphs/arch_opcode_nodes_go.json'));s=[c for c in d['call_sites'] if c['emitter']=='Prog' and c['state']=='names_its_opcode' and c['opcodes']];o=sorted({k['text'] for c in s for k in c['opcodes']});print(len(s),'Prog sites name an arch constant;',len(o),'distinct:');print(' '.join(o))"
50 Prog sites name an arch constant; 24 distinct:
ADDQ CMOVLPC CMOVLPS CMOVQPC CMOVQPS CMOVWPC CMOVWPS DECL JNE LOCK MOVB MOVBLZX MOVL MOVQ MOVSQ MOVUPS RCRQ REP SETEQ SETPC SETPS STOSQ TESTB XCHGL
```

**GLOSS.** `206` call sites, `50` constant, `24` distinct opcodes, and
the same 24 names — the coordinator's measurement reproduces exactly from
this task's own artifact. Two differences worth naming, because they are
differences in COUNTING and not in the source:

- **the 118.** The coordinator's "118 pass a computed opcode" is the
  count of three spellings — `v.Op.Asm()` 114, `op` 3, `as` 1 — measured
  in lane `t95_l2_recon.sh` §[4/9]. It is not all the non-constant
  sites: 206 − 50 − 17 pseudo-op constants = 139 are non-constant, and
  the remaining 21 carry other spellings (`asm` 8, `mov` 3, `opCMP`,
  `opNEG`, `opSXD`, `op.Asm()`, `cmpxchg`, and four calls into
  `loadByRegWidth` / `storeByRegWidth`).
- **the 50 versus 67.** Lane `t95_l2_recon.sh` counts **67** sites
  passing a package-qualified constant; **50** of those are `x86.A*` arch
  opcodes and **17** are `obj.A*` pseudo-ops. The coordinator counted the
  arch half. This task reports both, separately.

## 6.2 The comparison, three ways because the CORE's rule requires three

**LITERAL**, lane `t95_l11_own_evidence2.sh` §[1/3] and §[2/3]:

```
$ python3 PseudoCoupHQ/Research/compiler_graph/lanes_t95/t95_compare.py go
go: 1859 definitions, 1534 instrumented bodies, 590 probes
  entered by at least one probe             724 of 1859 definitions
  instrumented, entered by none             810 of 1859 definitions
  never instrumented, a NAMED FRONTIER      325 of 1859 definitions
  statically detected emitters               57 of 1859 definitions
  in BOTH sets                               12
  emitters instrumented, entered by none     45 of 57 emitters
  emitters never instrumented                 0 of 57 emitters
  entered but emitting nothing              712 of 724 entered

$ python3 PseudoCoupHQ/Research/compiler_graph/lanes_t95/t95_compare.py cpp
cpp: 10789 definitions, 8871 instrumented bodies, 1380 probes
  entered by at least one probe            1331 of 10789 definitions
  instrumented, entered by none            7540 of 10789 definitions
  never instrumented, a NAMED FRONTIER     1918 of 10789 definitions
  statically detected emitters              251 of 10789 definitions
  in BOTH sets                               45
  emitters instrumented, entered by none    203 of 251 emitters
  emitters never instrumented                 3 of 251 emitters
  entered but emitting nothing             1286 of 1331 entered
```

**GLOSS — and ENTERING IS NOT EMITTING, in both directions.**

- The two sets **barely overlap**: 12 of go's 57 emitters and 45 of
  clang's 251 were entered by any probe. **712 of the 724** go
  definitions a probe entered, and **1,286 of the 1,331** clang bodies,
  emit no machine instruction at all — they are parsing, typing, ABI
  classification, rewriting, everything that happens before an
  instruction exists.
- The other exclusive part has a CAUSE, and it is readable. Of go's 45
  emitters that no probe entered, **39** are the `simd*` helpers in
  `amd64/ssa.go:1916-2411` (lane `t95_l8_split_and_guard.sh` §[2/5]) —
  SIMD lowering the 590 scalar probes never reach. Not a measurement
  failure: a statement about what the corpus exercises.
- **The third bucket is not "never entered".** The CORE already settled
  that an uninstrumented node is a frontier, never a never-visited node.
  0 of go's 57 emitters and 3 of clang's 251 are outside the instrumented
  population; those 3 are frontiers, not evidence of anything.
- A first cut of this comparison asked `per_def_visitors` whether an
  emitter was "in the coverage join's population" — but that map holds
  only the ENTERED definitions, so it merely repeated "never entered"
  under a second name. Lane `t95_l7_rerun_and_compare.sh` §[6/6] holds
  that wrong reading; lane `t95_l8_split_and_guard.sh` §[1/5] corrected
  it against `never_visited_rows`.

**GLOSS, the plain relation.** The static pass and the dynamic join
answer different questions and their answers should not be expected to
agree. The static pass says WHICH DEFINITIONS CAN PRODUCE AN
INSTRUCTION — 57 and 251, from source, with no probe. `coverage` says
WHICH DEFINITIONS THIS CORPUS WALKED — 724 and 1,331, with no statement
about what they emit. Their intersection, 12 and 45, is the set the
corpus is known to have driven to an instruction; each side's exclusive
part is a fact about the other measurement, not an error in either.

---

# 7. What rust and swift gained

Both are blocked from instrumentation on this machine — rust a promisor
clone with no route out and the corpus's rustc commit absent, swift
missing three of the five repositories a build needs (log_175 §6.3–6.4).
Both have graphs. A static pass needs only source, so both got marked.

## 7.1 rust gained a MEASURED negative, and its cause

**LITERAL**, lane `t95_l10_own_evidence.sh` §[6/8]:

```
$ python3 -c "import json;d=json.load(open('PseudoCoupGraphs/arch_opcode_nodes_rust.json'));print(d['unmeasured_by_absence_of_an_emitter'])"
arch_opcode_emitter_outside_the_region -- measured, not assumed: 0 files of the whole rust checkout name BuildMI(, MCInst, MachineInstr or an X86 instruction namespace (lane t95_l3_recon2.sh step 4). rustc's region emits LLVM IR; the machine instruction is emitted by LLVM, whose source IS the cpp region, where it is measured. The inline-assembly path carries a template the COMPILED PROGRAM supplies, which is not the compiler naming an opcode.
```

**GLOSS.** Before this task, rust's row said "0 diaries, planned". It now
says something positive: **no node of the rust region is an
arch-opcode-node, and the reason is structural, not a limit of this
machine.** Instruction selection for rust happens in LLVM, which this
line already has a graph of, already instrumented, already covered. The
only thing the rust region spells that looks like assembly is
DIRECTIVES — lane `t95_l6_run_the_pass.sh` §[2/8] lists every string
literal of `naked_asm.rs`: `.globl`, `.align`, `.section`, `.att_syntax`,
`.balign`, `.popsection`, `.functype`. Directives are not instructions.

## 7.2 swift gained one real arch-opcode-node

`lib/IRGen/IRGenSIL.cpp:5571`, `IRGenSILFunction::visitDebugStepInst`,
state `names_its_opcode`, opcode `nop` (§2.3 and §3.3). One definition of
10,088. And swift gained the same structural statement rust did for the
other 10,086.

**GLOSS.** Small, and it is the point. Two compilers that could not be
run on this machine now carry a marking that says exactly where opcode
production is and is not, derived from source, re-runnable by anyone,
and it says the honest thing rather than nothing.

---

# 8. The frontiers, named

## 8.1 The `.td` files are not a complete instruction table

The CORE names LLVM's `.td` as the static table the cpp hop should read,
and the region does keep all 61 of them. It could not serve.

**LITERAL**, lane `t95_l13_own_evidence3.sh` §[8/8], the frontier as it
rides on the cpp artifact:

```
$ python3 PseudoCoupHQ/Research/compiler_graph/lanes_t95/t95_show.py frontier
the_td_files_are_not_a_complete_instruction_table -- the CORE names LLVM's .td as the static table the hop reads, and the region does keep all 61 of them, but a plain `def <name>` scan of them answers 7,227 records and MISSES the instructions X86 defines through `defm` multiclasses: 100 call sites naming a real instruction (CMP64rr, ADD32ri, XOR32rr and so on) were read as `not a .td record` when the table was used that way (lane t95_l3_recon2.sh step 3). The complete enumeration lives in X86GenInstrInfo.inc, which TableGen writes at BUILD time and which is not on this disk. So the arch-opcode namespace X86:: is what identifies an instruction here, taken from the argument's POSITION in the call, and the hop reads the in-region static helpers and `static const TableEntry[]` arrays instead. The .td shortfall is written down, not worked around.
```

**GLOSS.** So the arch-opcode namespace `X86::`, read from the argument's
POSITION in the call, is what identifies an instruction in the cpp
region, and the hop reads the in-region static helpers and
`static const TableEntry[]` arrays instead. The shortfall is written
down, not worked around.

## 8.2 The sites whose hop does not resolve, per reason

**LITERAL**, lane `t95_l13_own_evidence3.sh` §[6/8]:

```
$ python3 PseudoCoupHQ/Research/compiler_graph/lanes_t95/t95_show.py reasons
go {"argument_is_not_a_named_constant": 24, "argument_named_nothing": 1}
cpp {"argument_is_not_a_named_constant": 243, "callee_body_has_no_return": 8, "callee_not_declared_inside_the_region": 1, "the_call_carries_no_instruction_descriptor_argument": 13, "token_pasting_suffix_not_readable_from_source": 6}
rust {"empty_template_emits_no_instruction": 1, "template_is_not_a_string_literal_in_this_region": 1}
swift {"empty_template_emits_no_instruction": 3, "template_is_not_a_string_literal_in_this_region": 1}
```

**GLOSS.** `token_pasting_suffix_not_readable_from_source` is the one
worth naming out loud. The X86 backend defines
`#define GET_EGPR_IF_ENABLED(OPC) STI->hasEGPR() ? OPC##_EVEX : OPC`. The
pass-through branch is literal and IS resolved from the call's own
argument; the `##`-pasted name cannot be READ as a constant from source
and so is NOT recorded. Never infer an opcode you cannot read.

## 8.3 Co-location is measured and is NOT a promotion

**46** of clang's 69 `emits_opcode_dynamic` definitions name arch opcodes
elsewhere in their own body — a switch that fills a local, which the
emitter then hands over. The source does not say which of them THAT call
site emits, so the state does not change and no opcode is recorded
against it. The number rides on the artifact under
`state_three_definitions_that_name_arch_opcodes_elsewhere_in_their_own_body`
with the field `what_that_number_is_not` beside it. go's count is 0.

---

# 9. The guard, and the real violation it caught

**LITERAL**, lane `t95_l8_split_and_guard.sh` §[5/5]:

```
FAIL arch_opcode_nodes_go.json -- 1 spelling-keyed place(s)
     $.call_sites[223].argument
         operator token 'as' on a structure field -- this is a grouping/row key, not a per-unit label
```

**GLOSS.** go's own emitter is `func (s *State) Prog(as obj.As)`, and the
call sites that hand the parameter straight through write `s.Prog(as)`.
The argument's TEXT is therefore the string `as`, one of the 91 operator
tokens the corpus probes — exactly the hazard the brief for this task
named in advance and exactly the one task 93 hit with `new` and `not`.
**THE RULED REMEDY WAS APPLIED: the typed shape, no whitelist, no
rename.** The argument, and the name of every table a hop read, now ride
as `{"text": "..."}` — a value on a row, the shape the opcodes already
had.

And the pass now REFUSES ITS OWN OUTPUT: `Graph.arch_opcode_nodes` runs
the unmodified guard over the file it just wrote and raises
`SpellingKeyRefused` rather than returning. Each artifact carries the
verdict at `spelling_guard`.

**LITERAL**, lane `t95_l10_own_evidence.sh` §[8/8]:

```
$ md5sum PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
1d6aba67cbcdb021c3bdfd7f40fd2020  PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py

$ cat PseudoCoupHQ/Research/compiler_graph/guard_task95.txt
operator inventory: 91 tokens read from probe_manifest_*.json
PASS arch_opcode_nodes_go.json -- no operator token in any key, grouping, pairing or row structure
PASS arch_opcode_nodes_cpp.json -- no operator token in any key, grouping, pairing or row structure
PASS arch_opcode_nodes_rust.json -- no operator token in any key, grouping, pairing or row structure
PASS arch_opcode_nodes_swift.json -- no operator token in any key, grouping, pairing or row structure
PASS arch_opcode_nodes_go_summary.json -- no operator token in any key, grouping, pairing or row structure
PASS arch_opcode_nodes_cpp_summary.json -- no operator token in any key, grouping, pairing or row structure
PASS arch_opcode_nodes_rust_summary.json -- no operator token in any key, grouping, pairing or row structure
PASS arch_opcode_nodes_swift_summary.json -- no operator token in any key, grouping, pairing or row structure

$ grep -c exempt PseudoCoupHQ/Research/compiler_graph/guard_task95.txt
0
```

**GLOSS.** The guard is UNMODIFIED (md5 `1d6aba67cbcdb021c3bdfd7f40fd2020`,
the same md5 task 87 and task 93 recorded; `git status` reports no
change). ONE process, all 8 artifacts, exit 0, `grep -c exempt` = 0.

---

# 10. Memory

Stated bound **6,144 MB**, refusal named `MemoryCeilingReached`, raised by
the method itself. Sampled BEFORE any pass was written, lane
`t95_l2_recon.sh` §[2/9]:

```
   graph_go.json          4839116 bytes on disk  nodes   10393  strings   18028  peak RSS     52.2 MB
   graph_cpp.json        39788093 bytes on disk  nodes  112364  strings  194627  peak RSS    324.1 MB
   graph_rust.json        6297219 bytes on disk  nodes   13446  strings   28979  peak RSS    324.1 MB
   graph_swift.json      21263773 bytes on disk  nodes   71106  strings  115219  peak RSS    319.9 MB
   peak resident set, all four held one after another: 324.1 MB
```

Measured peaks of the pass itself, each written onto its own artifact —
**LITERAL**, lane `t95_l13_own_evidence3.sh` §[7/8]:

```
$ python3 PseudoCoupHQ/Research/compiler_graph/lanes_t95/t95_show.py cost
go     wall  0.5 s  peak  120.9 MB  ceiling 6144 MB  refusal MemoryCeilingReached  files 112  co-located 0
cpp    wall  2.9 s  peak  566.9 MB  ceiling 6144 MB  refusal MemoryCeilingReached  files 269  co-located 46
rust   wall  0.3 s  peak  117.1 MB  ceiling 6144 MB  refusal MemoryCeilingReached  files 134  co-located 0
swift  wall  0.5 s  peak  319.5 MB  ceiling 6144 MB  refusal MemoryCeilingReached  files 230  co-located 0
```

**GLOSS.** No limit was approached and nothing was reduced to fit. The
compact graphs are read whole, which the CORE permits; the 515 MB and
416 MB coverage joins were NOT read — the comparison uses the small
`coverage_<lang>_files.json` summaries task 73 built for exactly this.
The `co-located` column is §8.3's number, and it is not a promotion.

---

# 11. Every artifact this task touched, named

## 11.1 Written

| path | bytes | md5 |
|---|---|---|
| `PseudoCoupGraphs/arch_opcode_nodes_go.json` | 4,830,504 | `9d90753f9d2b432db55624a2426b8bc1` |
| `PseudoCoupGraphs/arch_opcode_nodes_cpp.json` | 1,254,695 | `2890bd8edb8ba2c1c64cde6fca976f57` |
| `PseudoCoupGraphs/arch_opcode_nodes_rust.json` | 210,756 | `8efc2836ebaf707928c1065bce484b36` |
| `PseudoCoupGraphs/arch_opcode_nodes_swift.json` | 419,946 | `58c6a32341fbd9b56dbab32586a8eda0` |
| `Research/compiler_graph/arch_opcode_nodes_go_summary.json` | 6,325 | `396f1910ddcb0ba4328bdcafd84df8e3` |
| `Research/compiler_graph/arch_opcode_nodes_cpp_summary.json` | 4,959 | `a1245dfeeaddf4575429bd1c040bc955` |
| `Research/compiler_graph/arch_opcode_nodes_rust_summary.json` | 4,744 | `54570ae06fef23276b00f07ba5755180` |
| `Research/compiler_graph/arch_opcode_nodes_swift_summary.json` | 3,657 | `639a1cd17c9b9785b4762eb6ac7bc35d` |
| `Research/compiler_graph/guard_task95.txt` | — | the guard transcript above |

## 11.2 Changed

- `Research/compiler_graph/graph.py` — new module-level
  `ARCH_OPCODE_RULES` and `arch_text_row`; new exception
  `SpellingKeyRefused`; new methods `Graph.arch_opcode_nodes`,
  `_arch_balanced`, `_arch_split`, `_arch_branches`, `_arch_read_region`,
  `_arch_pseudo_names`, `_arch_hop`, `_arch_hop_uncached`, `_arch_grade`,
  `_arch_template_grade`; new `command_arch_opcode_nodes` and the
  `arch-opcode-nodes` subcommand. Nothing existing was altered.
- The node's `CORE_0_3_5_9_graph.md` realization table and `PROGRESS.md`.

## 11.3 New, and kept as the record

- `Research/compiler_graph/lanes_t95/t95_l1_recon.sh` — ran before the
  graphs mount existed; kept because it is what proved it was missing.
- `t95_l2_recon.sh`, `t95_l3_recon2.sh`, `t95_l4_recon3.sh`,
  `t95_l5_recon4.sh` — the four reconnaissance lanes that LOCATED each
  region's emitter.
- `t95_l6_run_the_pass.sh` — the first run; it exposed three defects.
- `t95_l7_rerun_and_compare.sh` — the fix, and a wrong first comparison.
- `t95_l8_split_and_guard.sh` — the corrected comparison, and the guard
  refusal.
- `t95_l9_guard_fix_rerun.sh` — the run of record.
- `t95_l10_own_evidence.sh`, `t95_l11_own_evidence2.sh`,
  `t95_compare.py` — this log's own evidence.

Lane logs, in `Airlock/agent/logs/`:
`20260905T053851Z__t95_l1_recon.sh.log`,
`20260905T054126Z__t95_l2_recon.sh.log`,
`20260905T054346Z__t95_l3_recon2.sh.log`,
`20260905T054554Z__t95_l4_recon3.sh.log`,
`20260905T054730Z__t95_l5_recon4.sh.log`,
`20260905T055435Z__t95_l6_run_the_pass.sh.log`,
`20260905T055803Z__t95_l7_rerun_and_compare.sh.log`,
`20260905T055933Z__t95_l8_split_and_guard.sh.log`,
`20260905T060204Z__t95_l9_guard_fix_rerun.sh.log`,
`20260905T060334Z__t95_l10_own_evidence.sh.log`,
`20260905T060426Z__t95_l11_own_evidence2.sh.log`.

## 11.4 One operational fact, recorded because it changed the sandbox

`mounts.conf` DID name `PseudoCoupGraphs:PseudoCoupGraphs:rw`
and `PseudoCoupHQ:PseudoCoupHQ:rw`, but the
running `sandbox-runner` had neither: it is a systemd quadlet, and the
quadlet unit had been rendered before those lines were added. `./down.sh`
plus `./up.sh` could not fix it — the unit restarts the container from
the stale file. `./install_quadlet.sh` re-renders it from `mounts.conf`,
which is Airlock's own provided way to do this. No workaround was
written and nothing was copied out of the mount.

---

# 11.5 What task 90's verifier says about this log

Run over this file, lane `t95_l15_verify_this_log3.sh`: **28 claims, 18
MATCHES, 0 DIFFERS, 7 UNVERIFIABLE, 3 REFUSED, 0 NOT_RERUNNABLE.** (Two
earlier runs are kept as the record: `t95_l12_verify_this_log.sh` scored
24 / 11 / 0 / 13 / 0 / 0 on the first draft, and
`t95_l14_verify_this_log2.sh` 27 / 16 / 0 / 8 / 3 / 0 after the
attributions here were turned into commands. This paragraph is itself a
claim, so the total moves by one each time it is written down.) The 3
REFUSED are the three `git -C /sources/... show <pin>:<file>` reads in
§2.3 — the verifier's allowlist does not carry `git show`, and its rule
is named (`git_subcommand_not_read_only`). They are kept as they are,
because reading a file AT ITS PIN is the whole point of quoting it and
`/sources` is mounted read-only. The 8 UNVERIFIABLE are quotations of
`graph.py`'s own text, of a lane log outside the sandbox, and prose
summarising numbers that appear with their command elsewhere in this log.

---

# 12. The two lists

## 12.1 Decided, recorded for audit — no answer needed

1. **The pass is a method of the graph**, `Graph.arch_opcode_nodes`,
   beside `coverage` and `variant_connections`, with the per-language
   rules as DATA — the pattern `build` already uses.
2. **An emitter is found by machine form, not by name.** In go, a
   function that TAKES `obj.As` emits and one that RETURNS it is a table;
   both are read off the declaration.
3. **State 1 covers pseudo opcodes as well as arch ones**, because a
   site naming `obj.ACALL` or `TargetOpcode::COPY` does name its opcode.
   The two are counted separately and only arch opcodes enter the inverse
   index.
4. **A conditional between named constants is state 1**, with both
   branches recorded; the condition is not a value the instruction can
   take.
5. **The opcode argument is taken from its POSITION in the call**, which
   is what keeps `X86::EAX` out of an opcode index.
6. **Co-location is reported and never promotes a state** (§8.3).
7. **The `.td` shortfall is a named frontier**, not a workaround (§8.1).
8. **Artifacts live in `PseudoCoupGraphs`, summaries in `PseudoCoupHQ`**,
   the split `graphs_home.py` already states.
9. **`install_quadlet.sh` was re-run** to apply `mounts.conf` (§11.4).

## 12.2 Awaiting the owner

1. **Should the go hop be reported as a bound rather than a set?** A
   `one_static_hop` definition in go carries all 564 amd64 opcodes,
   because `Op.Asm()` says which table is read and never which row
   (§4.2). It is correct and it is coarse. Narrowing it needs a run-time
   fact, which is `coverage`'s question. The marking stands either way;
   what is open is whether the inverse index should carry those 564 per
   site at all, or carry only the constants and name the table.
