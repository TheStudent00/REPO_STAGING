# log 252 — task hub1: Hub v1, first form — the dictionary read off the polyfill-complete set, one typed go file lowered as source composition of proved emulations, and the measure over the corpus's own go units

Node: `hq.research.arch_unit_oracle.hub_compiler`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_1_hub_compiler/`),
its CORE's "definition" of 2026-09-07 (SOURCE COMPOSITION) and its four
sub-nodes front_end, dictionary, joiner, oracle_test. Line: steps 4 and 5
of the master order,
`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/CORE_0_3_research.md`
§4.2. Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, read in full
including its tower section. Brief:
`PRIVATE/PseudoCoupHQ/Research/briefs/task_hub1_brief.md`.
Date: 2026-09-10. Instance `hub1`, on the tower guest.

Artifact folder: `PRIVATE/PseudoCoupHQ/Research/oracle/hub/`. Lane
scripts: `PRIVATE/PseudoCoupHQ/Research/oracle/hub/lanes_hub1/`,
sixteen of them, each kept in the repo as the standing rule of 2026-09-07
requires. Every lane log named below is on the TOWER
(`<user>@<tower>`) under
`<runs>/hub1/agent/logs/`.

Paths inside a pasted command are the ones the lane sees:
`PseudoCoupHQ` IS `PRIVATE/PseudoCoupHQ`, mounted into the
instance. Every rendering is labelled per the protocol's
`object.literal-gloss-analogy`: **LITERAL** is the object itself, quoted;
**GLOSS** is a plain-words reading beside a literal.

---

# 1. What this is, one sentence per object in relation

* A **CELL** is one (`mnem`, operand shape, `key_width`) row of the
  arch-opcode model table — the machine-form key ruled 2026-09-08.
* The **DICTIONARY** is, per (target, cell), the emulation SOURCE the
  AutoPoly loop rendered for that cell on that target, the route it took
  (primitive / primitive+setup / term), the gate's verdict on it, and the
  ledger rows the cell is attested by. Task ap5's store
  (`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5_runs.jsonl`,
  1,012 runs, log 249) holds every one; this task writes them out as one
  lookup and names, per target, the cells that have no proved entry and
  why.
* The **GO SIDE** of the lookup is the corpus's own attestation: a go
  unit whose WHOLE body is one arch-opcode instruction plus chaff (task
  o2's narrow rule,
  `PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.json`)
  says which cell go's compiler produces for the construct that unit's
  own source holds at the operand holders that unit's own probe record
  names.
* The **FRONT END** parses the file to be lowered with tree-sitter-go and
  types every operator node's operands with go's own type checker
  (`PRIVATE/PseudoCoupHQ/Research/oracle/compiler_units/go_types_oracle.go`,
  task o6's program, READ and never edited), joining the two by POSITION.
* **SOURCE COMPOSITION** is the egress the CORE ruled on 2026-09-07: the
  tree walked post-order, each operator node replaced by a CALL of its
  cell's emulation function, the emulation emitted once per cell into the
  composed file verbatim, and the target's own compiler left to lower and
  optimise across the calls.
* The **ORACLE TEST** is the gate over two bodies: body A, go's own build
  of one function of the file, carved; body B, the target's build of the
  composed function, carved; the two aligned by IN row.
* **THIS TASK** is the first form of all six, run end to end.

**THE ANSWER, in three numbers.** The dictionary holds **151 proved
entries on c, 151 on rust and 161 on go**, over the 253 cells of task
ap5's outer set. Of the handful's **eight** functions, **four prove on c,
five on rust, and five prove on go** once one directive is dropped (§6).
Over the corpus's own go units the dictionary composes **100 of 134 to c
(100 proved, 0 disproved) and 114 of 134 to rust (114 proved, 0
disproved)** — 56,830 and 62,745 attested ledger rows.

Three things are said before the numbers so the numbers are not misread.

* **A HOLE IS A RESULT, and every one of them carries its cause off the
  record.** Three of the eight handful functions do not compose, and each
  says why in go's own terms: `<<` and `>>` on `uint64` and `/` on
  `int32` are constructs go lowers to SIX and EIGHT cells, not one, and
  the cause quotes go's own body for them; `a != b` lowers to a cell that
  writes only flags. Nothing was hand-written to fill a hole.
* **THE MEASURE'S FIRST PASS WAS WRONG AND WAS RE-RUN.** Lane `hub1_l12`
  measured 21 DISPROVED on c and 14 rust units that would not build, and
  both were ONE cause: the primitive route can match a corpus body whose
  own probe was written over TRUTH holders, so the entry's parameters are
  declared `bool`. The composition now refuses such an entry by cause
  instead of calling it, and the first pass's numbers are kept in this
  log beside the second (§7).
* **THE GO IDENTITY CHECK NEEDED A RE-POSE, and both verdicts are
  recorded.** `//go:noinline`, which the corpus's own probe shape puts on
  every rendered emulation, forbids exactly the cross-operator lowering
  source composition exists to obtain. The strict composed file is
  UNDECIDED on all five; the same file with that one line dropped from
  each emulation proves all five, and go's own instructions come back
  (§6).

---

# 2. The dictionary (step 4 of the master order)

`PRIVATE/PseudoCoupHQ/Research/oracle/hub/dictionary.json` and its
reading `PRIVATE/PseudoCoupHQ/Research/oracle/hub/dictionary.md`,
both written by
`python3 PseudoCoupHQ/Research/oracle/hub/hub.py dictionary`
(lane `hub1_l7`).

An entry exists for (target, cell) when the loop rendered, compiled and
PROVED the place that cell writes its own ANSWER into — the place whose
name begins `reg_`. A flags place is not a value a composition can pass
on, so a cell that writes only flags is a hole and says so.

Table 1 — entries and holes per target, and the attested ledger rows each
covers, out of the outer set's 133,044.

```
$ sed -n '5,11p' PseudoCoupHQ/Research/oracle/hub/dictionary.md
## 1. Entries and holes per target

| target | entries | ledger rows the entries cover | holes | ledger rows the holes cover |
|---|---|---|---|---|
| c | 151 | 82175 | 102 | 50869 |
| rust | 151 | 81294 | 102 | 51750 |
| go | 161 | 98458 | 92 | 34586 |
```

Table 2 — the same entries by the route the loop took to them.

```
$ sed -n '13,20p' PseudoCoupHQ/Research/oracle/hub/dictionary.md
## 2. Entries per target by route

| target | primitive | primitive+setup | term |
|---|---|---|---|
| c | 23 | 0 | 128 |
| rust | 21 | 0 | 130 |
| go | 16 | 0 | 145 |

```

Table 3 — the holes on c, by cause. The other two targets' tables are in
`dictionary.md` §3.

```
$ sed -n '21,33p' PseudoCoupHQ/Research/oracle/hub/dictionary.md
## 3. Holes per target, by cause

### c

| cells | ledger rows | cause |
|---|---|---|
| 61 | 26348 | the cell writes no register place: every place it writes is a flag place, which is not a value a composition can pass on |
| 35 | 22416 | z3 found a starting state under which the two sides differ |
| 4 | 1097 | seed_MEM__rsi_ is 128 bits, and an arriving value is 64 |
| 1 | 624 | the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either |
| 1 | 384 | the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |

### rust
```

**GLOSS.** The dominant hole is not a failure of the loop: 61 of the 253
cells write only flags, and a source composition passes VALUES between
nodes. Those cells are reachable by a Hub that carries a flag state
across nodes, which Hub v1 does not.

**THE GO SIDE.** 134 corpus go units whose whole body is one arch-opcode
instruction each name exactly one cell; 4 more that the narrow rule holds
name no single cell and are listed separately. Every one of the corpus's
590 go units is carried beside them (`go_units_every`), with the cells its
own body produced, so that a construct the narrow rule does not hold is a
hole with go's OWN body as its cause rather than an absence. The unit-by-
unit table is `dictionary.md` §5.

---

# 3. The front end

`hub.py front_end` does two things and joins them by position.

* tree-sitter-go parses the file. Lane `hub1_l6` printed the installed
  grammar's real nesting before the walk was written against it, and it
  is `block -> statement_list -> return_statement -> expression_list ->
  the expression`; a `binary_expression` carries fields `left`,
  `operator`, `right`.
* `go_types_oracle.go` is run over the file ALONE, in a directory of its
  own, and its `sites` array gives each operator node's operand type
  spellings and its result. The join key is the node's (line, column, end
  line, end column) — never the token.

**TWO CORRECTIONS THE FIRST PASS NEEDED, both named.**

1. **The node key is the whole SPAN.** `a + b - c` gives the outer node
   and its own left sub-node the SAME start position, so a key on the
   start alone lost one of the two (lane `hub1_l5`: "13 operator nodes"
   but only 11 resolutions). Table 4 below shows both `20:9` rows.
2. **go's default type for an untyped boolean value.** go/types spells a
   comparison's type `untyped bool`; the go specification makes that an
   untyped boolean value whose DEFAULT TYPE is `bool`, which is the
   holder the corpus's own probe records spell. The two are joined on the
   default type. Without it, `a != b` resolved to nothing and the cause
   would have said "no go unit of the corpus carries this construct",
   which is false.

Table 4 — every operator node of the handful, with what go's own type
checker says about it and the corpus go unit — and so the cell — it
resolves to.

```
$ sed -n '5,24p' PseudoCoupHQ/Research/oracle/hub/oracle_test.md
## 1. The handful, node by node

One row per operator node of `Research/oracle/hub/handful/handful.go`: where it is, what go's own type checker says its operands and its result are, and which corpus go unit -- and so which cell -- the corpus attests for it.

| function | line:col | the node, LITERAL | lhs holder | rhs holder | result holder | corpus unit | cell |
|---|---|---|---|---|---|---|---|
| f1_i32_add_sub | 20:9 | `a + b` | int32 | int32 | int32 | go/op_312 | `add gpr_gpr 32` |
| f1_i32_add_sub | 20:9 | `a + b - c` | int32 | int32 | int32 | go/op_348 | `sub gpr_gpr 32` |
| f2_i32_add_mul | 25:9 | `(a + b) * c` | int32 | int32 | int32 | go/op_60 | `imul gpr_gpr 32` |
| f2_i32_add_mul | 25:10 | `a + b` | int32 | int32 | int32 | go/op_312 | `add gpr_gpr 32` |
| f3_i64_add_sub | 30:9 | `a + b` | int64 | int64 | int64 | go/op_319 | `add gpr_gpr 64` |
| f3_i64_add_sub | 30:9 | `a + b - c` | int64 | int64 | int64 | go/op_355 | `sub gpr_gpr 64` |
| f4_i64_mul | 35:9 | `a * b` | int64 | int64 | int64 | go/op_67 | `imul gpr_gpr 64` |
| f5_u64_shift | 40:9 | `(a << n) >> n` | uint64 | uint64 | uint64 | -- | -- |
| f5_u64_shift | 40:10 | `a << n` | uint64 | uint64 | uint64 | -- | -- |
| f6_i32_div | 45:9 | `a / b` | int32 | int32 | int32 | -- | -- |
| f7_f64_add_mul | 50:9 | `(a + b) * c` | float64 | float64 | float64 | go/op_88 | `mulsd xmm_xmm 64` |
| f7_f64_add_mul | 50:10 | `a + b` | float64 | float64 | float64 | go/op_340 | `addsd xmm_xmm 64` |
| f8_i32_select | 55:5 | `a != b` | int32 | int32 | bool | -- | -- |

```

**GLOSS.** 13 operator nodes, all 13 typed by go/types, 9 of them
resolved to a corpus-attested cell. The four that do not are `<<`, `>>`,
`/` and `!=`, and §5 gives each one's cause in go's own body text.

**HOW THE RESOLUTION OBEYS THE SPELLING BAN, said mechanically.** The
CANDIDATE SET for a node is the TYPE TUPLE (arity, lhs holder, rhs
holder, result holder) — "type pairs", which the ban names as
machine-form evidence. Within that candidate set the front end reads
SOURCE: the candidate corpus unit's own go source is parsed by the same
tree-sitter grammar and the two operator nodes' own operator children are
compared as source text, between two source files, exactly as a parser
reads. The answer is a NAMED CORPUS UNIT whose body go's own compiler
produced. No key, no grouping, no pairing and no row structure in
anything this task writes carries an operator token — the guard is §8.

---

# 4. The join at source level, and it is not the identity

The joiner sub-node's row traffic, at source level, is the ARGUMENT PLAN:
which of the emulation's parameters each operand of the node is passed
as. It is read off three machine-form objects and nothing else
(`hub.py argument_plan`):

| the object | what it gives |
|---|---|
| the corpus go unit's `arrival_families` on its canon40 record | which register each of ITS parameters arrives in |
| the same unit's own body LINE, through `model_table.operand_texts` and `ledger.family_of_operand` | which register each operand SLOT of that one instruction reads |
| the cell's own line beside the emulation's parameter families (`params[i]["family"]`, or the gate's own `aligned_rows` where the primitive route recorded none) | which of the emulation's parameters stands for each slot |

Operand position → the unit's parameter index → its arrival family → the
slot that family sits in → the cell's family in the same slot → the
emulation's parameter.

**IT IS NOT ALWAYS THE IDENTITY, and that is why it is read rather than
assumed.** For the float64 `+` node on c, the entry
`emu_addsd_xmm_xmm_64__reg_xmm0__c` declares its parameters in the order
the renderer met them in the term — `a` is `xmm1` and `b` is `xmm0` — so
the composition emits the call with the node's operands the other way
round. **LITERAL**, the composed c function:

```
$ sed -n '82,88p' PseudoCoupHQ/Research/oracle/hub/handful/composed_c.c
double
f7_f64_add_mul(double a, double b, double c)
{
    double hub_t0 = (double)(emu_addsd_xmm_xmm_64__reg_xmm0__c((double)(b), (double)(a)));
    double hub_t1 = (double)(emu_mulsd_xmm_xmm_64__reg_xmm0__c((double)(hub_t0), (double)(c)));
    return hub_t1;
}
```

**THE COMPOSED FILE'S OWN FURNITURE.** The emulation is carried in
VERBATIM; only what a file needs once is taken off it — `#include` lines
and the renderer's `static inline` helpers (deduplicated by their own
text) for c, the `#![allow(...)]` line for rust, and `package main`, the
globals and the `main` a go probe file carries for go. Nothing inside a
proved function is touched. **LITERAL**, the two composed c functions
whose result holder is `int32`:

```
$ sed -n '59,73p' PseudoCoupHQ/Research/oracle/hub/handful/composed_c.c
int32_t
f1_i32_add_sub(int32_t a, int32_t b, int32_t c)
{
    int32_t hub_t0 = (int32_t)((uint32_t)(emu_add_gpr_gpr_32__reg_rdi__c((uint32_t)(a), (uint32_t)(b))));
    int32_t hub_t1 = (int32_t)((uint32_t)(emu_sub_gpr_gpr_32__primitive__c((int32_t)(hub_t0), (int32_t)(c))));
    return hub_t1;
}

int32_t
f2_i32_add_mul(int32_t a, int32_t b, int32_t c)
{
    int32_t hub_t0 = (int32_t)((uint32_t)(emu_add_gpr_gpr_32__reg_rdi__c((uint32_t)(a), (uint32_t)(b))));
    int32_t hub_t1 = (int32_t)((uint32_t)(emu_imul_gpr_gpr_32__primitive__c((int32_t)(hub_t0), (int32_t)(c))));
    return hub_t1;
}
```

**GLOSS.** The node's value is the LOW `key_width` bits of the place the
cell writes, in the node's own holder, and the two casts are how it is
taken: the emulation's own return holder never has to be named, because
an integer answer of any width lands in the node's holder through its
unsigned counterpart and a float answer is already the value.

---

# 5. The handful (step 5 of the master order)

The file is
`PRIVATE/PseudoCoupHQ/Research/oracle/hub/handful/handful.go`,
written for this task: eight explicitly typed functions, each one or two
operators, in the corpus's own probe shape (`//go:noinline`, package
main, globals fed from `main`) so that go's build of it is carved exactly
as every go unit of the corpus was carved. It covers the brief's list:
`+ - *` on `int32` and on `int64`, `<<` and `>>` on `uint64` with a
count, `/` on `int32`, float64 `+` and `*`, one comparison feeding a
select, and one two-operator expression `(a + b) * c`.

Table 5 — the eight functions, per target: the gate's verdict, the
re-pose of §6 where there is one, and the hole's cause where it is a
hole. The cause column is cut here because its go rows are paragraphs;
the whole of it is `oracle_test.md` §2.

```
$ sed -n '29,52p' PseudoCoupHQ/Research/oracle/hub/oracle_test.md | cut -d'|' -f2,3,4,5
 f1_i32_add_sub | c | PROVED | -- 
 f2_i32_add_mul | c | PROVED | -- 
 f3_i64_add_sub | c | HOLE | -- 
 f4_i64_mul | c | PROVED | -- 
 f5_u64_shift | c | HOLE | -- 
 f6_i32_div | c | HOLE | -- 
 f7_f64_add_mul | c | PROVED | -- 
 f8_i32_select | c | HOLE | -- 
 f1_i32_add_sub | rust | PROVED | -- 
 f2_i32_add_mul | rust | PROVED | -- 
 f3_i64_add_sub | rust | PROVED | -- 
 f4_i64_mul | rust | PROVED | -- 
 f5_u64_shift | rust | HOLE | -- 
 f6_i32_div | rust | HOLE | -- 
 f7_f64_add_mul | rust | PROVED | -- 
 f8_i32_select | rust | HOLE | -- 
 f1_i32_add_sub | go | UNDECIDED | PROVED 
 f2_i32_add_mul | go | UNDECIDED | PROVED 
 f3_i64_add_sub | go | UNDECIDED | PROVED 
 f4_i64_mul | go | UNDECIDED | PROVED 
 f5_u64_shift | go | HOLE | -- 
 f6_i32_div | go | HOLE | -- 
 f7_f64_add_mul | go | UNDECIDED | PROVED 
 f8_i32_select | go | HOLE | -- 
```

**THE FOUR HOLES, BY CAUSE, each off the record and none of them an
absence.**

| function | cause, as `oracle_test.md` §2 states it |
|---|---|
| `f3_i64_add_sub`, c only | the dictionary has no proved entry for the cell `add gpr_gpr 64` on c: the loop's own verdict there is "z3 found a starting state under which the two sides differ". rust and go have the entry and prove the function. |
| `f5_u64_shift` | go's own build of `a << n` at `uint64` is the corpus unit `go/op_182`, whose body `mov %rbx,%rcx; shl %cl,%rax; cmp $0x40,%rcx; sbb %rdx,%rdx; and %rdx,%rax; ret` produced SIX arch-opcode ledger rows (`mov gpr_gpr 64`, `shl cl_gpr 64`, `cmp imm_gpr 64`, `sbb gpr_same 64`, `sbb gpr_same 64`, `and gpr_gpr 64`) and not one; `>>` is `go/op_218` and the same six with `shr` |
| `f6_i32_div` | go's own build of `a / b` at `int32` is `go/op_96`, whose body carries the divide-by-zero guard and the overflow branch and produced EIGHT arch-opcode ledger rows (`push gpr_one 64`, `test gpr_same 32`, `cmp imm_gpr 32`, `neg gpr_one 32`, `xor gpr_same 32`, `cltd none 64`, `idiv gpr_one 32`, `idiv gpr_one 32`) |
| `f8_i32_select` | go's own build of `a != b` at `int32` is `go/op_492`, whose body `cmp %eax,%ebx; setne %al; ret` is not one arch-opcode instruction plus chaff; its own ledger holds one arch-opcode row, `cmp gpr_gpr 32`, and that cell writes only flags |

**GLOSS, and it is the shape of Hub v1's reach.** Hub v1 resolves a node
where go's own compiler lowers that construct at those holders to ONE
cell. Where go lowers it to a guarded sequence — a shift's count clamp, a
divide's two traps, a comparison's flag consumer — the node is a hole and
the cause names the sequence. That is the frontier the next form has to
cross, and it is a property of the lowering, not of the dictionary.

Table 6 — the two bodies, per function and target, for every function
that composed and carved. The go rows are §6.

```
$ sed -n '54,66p' PseudoCoupHQ/Research/oracle/hub/oracle_test.md
## 3. Body A and body B, per function and target

| function | target | body A, go's own, LITERAL | body B, the composition, LITERAL |
|---|---|---|---|
| f1_i32_add_sub | c | `add %ebx,%eax; sub %ecx,%eax; ret` | `lea (%rdi,%rsi,1),%eax; sub %edx,%eax; ret` |
| f2_i32_add_mul | c | `add %ebx,%eax; imul %ecx,%eax; ret` | `lea (%rdi,%rsi,1),%eax; imul %edx,%eax; ret` |
| f4_i64_mul | c | `imul %rbx,%rax; ret` | `mov %rdi,%rax; imul %rsi,%rax; ret` |
| f7_f64_add_mul | c | `addsd %xmm1,%xmm0; mulsd %xmm2,%xmm0; ret` | `addsd %xmm1,%xmm0; mulsd %xmm2,%xmm0; ret` |
| f1_i32_add_sub | rust | `add %ebx,%eax; sub %ecx,%eax; ret` | `lea (%rdi,%rsi,1),%eax; sub %edx,%eax; ret` |
| f2_i32_add_mul | rust | `add %ebx,%eax; imul %ecx,%eax; ret` | `lea (%rdi,%rsi,1),%eax; imul %edx,%eax; ret` |
| f3_i64_add_sub | rust | `add %rbx,%rax; sub %rcx,%rax; ret` | `lea (%rdi,%rsi,1),%rax; sub %rdx,%rax; ret` |
| f4_i64_mul | rust | `imul %rbx,%rax; ret` | `mov %rdi,%rax; imul %rsi,%rax; ret` |
| f7_f64_add_mul | rust | `addsd %xmm1,%xmm0; mulsd %xmm2,%xmm0; ret` | `addsd %xmm1,%xmm0; mulsd %xmm2,%xmm0; ret` |
```

**GLOSS, and this is the CORE's own claim measured.** Body B for
`f1_i32_add_sub` on c is three instructions — the two emulation calls are
gone and the add became a `lea`. The target's compiler lowered and
optimised ACROSS the calls, which is the reason source composition
replaced the memory-row join. And on the float64 function body B is
`addsd %xmm1,%xmm0; mulsd %xmm2,%xmm0; ret` — the same instruction TEXT
go's own compiler left for the same source, reached through two proved
emulations of two arch-opcode cells.

---

# 6. The go identity check, and the one directive that stood in the way

The brief asks go itself as an identity check: composing go from go must
round-trip to a proved-equal body. **It does not, as the emulations
stand, and the cause is exact.** Every emulation the corpus's renderers
write carries `//go:noinline`, which is the directive that makes a probe
its own carvable function. In a COMPOSED file the emulation is not the
unit being carved — the composed function is — and the directive forbids
the inlining the whole method rests on. go then gives the composed
function its stack-growth preamble, and the reference refuses to read a
body every path of which leaves the unit.

**LITERAL**, body B for `f1_i32_add_sub` on go, strict:

```
cmp 0x10(%r14),%rsp; jbe 47a80b <main.f1_i32_add_sub+0x2b>; push %rbp; mov %rsp,%rbp; sub $0x8,%rsp; mov %ecx,0x20(%rsp); call 47a6e0 <main.emu_add_gpr_gpr_32__primitive__go>; mov 0x20(%rsp),%ebx; nopl 0x0(%rax,%rax,1); call 47a700 <main.emu_sub_gpr_gpr_32__primitive__go>; add $0x8,%rsp; pop %rbp; ret; mov %eax,0x8(%rsp); mov %ebx,0xc(%rsp); mov %ecx,0x10(%rsp); call 475be0 <runtime.morestack_noctxt.abi0>; mov 0x8(%rsp),%eax; mov 0xc(%rsp),%ebx; mov 0x10(%rsp),%ecx; jmp 47a7e0 <main.f1_i32_add_sub>
```
*(attribution: `oracle_test.md` §3, the `f1_i32_add_sub | go` row.)*

So the proof is RE-POSED against the same composed file with that ONE
line dropped from each emulation and nothing else changed —
`PRIVATE/PseudoCoupHQ/Research/oracle/hub/handful/composed_go_inlinable.go`
beside
`PRIVATE/PseudoCoupHQ/Research/oracle/hub/handful/composed_go.go`.
Both files are kept, both verdicts are recorded, and the re-pose is
recorded BESIDE the strict verdict and never in place of it; task o7's
caller-extension re-pose is the precedent.

**LITERAL**, the same function's body B on the re-pose, and the four
others, off `oracle_test.json`:

| function | body B, go, without the directive |
|---|---|
| `f1_i32_add_sub` | `nop; add %ebx,%eax; sub %ecx,%eax; nop; nop; ret` |
| `f2_i32_add_mul` | `nop; add %ebx,%eax; imul %ecx,%eax; nop; nop; ret` |
| `f3_i64_add_sub` | `nop; add %rbx,%rax; sub %rcx,%rax; nop; nop; ret` |
| `f4_i64_mul` | `nop; imul %rbx,%rax; nop; ret` |
| `f7_f64_add_mul` | `push %rbp; mov %rsp,%rbp; sub $0x10,%rsp; addsd %xmm1,%xmm0; nop; movsd %xmm0,0x8(%rsp); movsd 0x8(%rsp),%xmm1; mulsd %xmm2,%xmm1; nop; movsd %xmm1,(%rsp); movsd (%rsp),%xmm0; add $0x10,%rsp; pop %rbp; ret` |

*(attribution: `PRIVATE/PseudoCoupHQ/Research/oracle/hub/oracle_test.json`,
`results[*].re_posed_without_the_noinline_directive.body_b_text`.)*

**GLOSS.** All five prove. `f1_i32_add_sub` comes back as
`add %ebx,%eax; sub %ecx,%eax` between two `nop`s — go's own two
instructions in go's own registers. The identity check holds; what it
needed was for the emulation to be allowed to inline.

---

# 7. The measure over the corpus's own go units (the brief's §3)

Body A here is not rebuilt: the corpus's own canon40 record for the unit
IS go's own carved body, and it is the object every proof of this line has
been posed against. Body B is the composition of that unit's one construct
for the target, built and carved at the target's own ship flags.

Table 7 — the measure, per target.

```
$ sed -n '73,82p' PseudoCoupHQ/Research/oracle/hub/oracle_test.md
## 4. The measure over the corpus's own go units

The corpus holds 590 go units. 138 of them are held by task o2's NARROW rule (the whole body is one arch-opcode instruction plus chaff) and 134 of those name exactly one cell; those are the units the dictionary can be asked about. The other go units of the corpus are the constructs go lowers to several cells, and they are named as such in the handful's own hole causes.

| target | units asked | composed | ledger rows the composed cells cover | built and carved | proved | proved under caller extension | disproved | undecided | ledger rows the proved cells cover | re-posed without `//go:noinline` | proved on that re-pose | ledger rows that re-pose proves |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c | 134 | 100 | 56830 | 100 | 98 | 2 | 0 | 0 | 56830 | 0 | 0 | 0 |
| rust | 134 | 114 | 62745 | 114 | 112 | 2 | 0 | 0 | 62745 | 0 | 0 | 0 |
| go | 134 | 124 | 74677 | 124 | 0 | 0 | 0 | 124 | 0 | 124 | 108 | 68399 |

```

**GLOSS — Hub v1's first oracle number.** Everything the dictionary
composes, the gate proves: **100 of 100 on c and 114 of 114 on rust, zero
disproved**, over 56,830 and 62,745 attested ledger rows. On go every
strict verdict is UNDECIDED for §6's one reason, and the re-pose proves
108 of 124.

**THE FIRST PASS OF THIS MEASURE WAS WRONG.** Lane `hub1_l12` reported
**c: 121 composed, 98 proved, 21 DISPROVED; rust: 128 composed, 114
carved** — fourteen rust units would not build at all. Lane `hub1_l13`
re-ran it after ONE cause was closed, and the cause is on the record, not
guessed. **LITERAL**, the composition lane `hub1_l12` wrote for
`go/op_240` (`a & b` at `int32`) and the two bodies the gate compared:

```
#[no_mangle]
pub extern "C" fn hub_go_op_240(a: i32, b: i32) -> i32
{
    let hub_t0: i32 = ((((emu_and_gpr_gpr_32__primitive__rust(((a) as bool), ((b) as bool))) as u32)) as i32);
    return hub_t0;
}
```
```
body A: and %ebx,%eax; ret
body B: test %edi,%edi; setne %al; test %esi,%esi; setne %cl; and %al,%cl; movzbl %cl,%eax; ret
the gate: z3 found a starting state under which the two sides differ
the counterexample: [IN_1 = 4261396478, IN_0 = 4261396478]
```
*(attribution: `PRIVATE/PseudoCoupHQ/Research/oracle/hub/measure.json`
as lane `hub1_l12` left it, read in this session before lane `hub1_l13`
overwrote it.)*

**GLOSS.** The dictionary entry for `and gpr_gpr 32` on c and on rust was
reached by the PRIMITIVE route, and the corpus body it matched came from
a probe written over TRUTH holders — so the emulation's own parameters
are declared `bool`, and it computes a boolean and. The loop proved that
emulation against the cell under the cell's own arrival contract; passing
a 32-bit operand through a `bool` parameter is outside what was proved,
and in rust `(a) as bool` is not even legal, which is why fourteen units
would not build. The composition now REFUSES such an entry by cause, and
refuses any parameter narrower than the operand it would carry
(`hub.py check_parameters`). Nothing about the dictionary or about the
loop changed; the refusal is in the composition, where the question
belongs.

Table 8 — the measure's causes, c and rust, after that refusal.

```
| units | target | cause |
|---|---|---|
| 9 | c | the emulation `emu_and_gpr_gpr_32__primitive__c` declares its parameter 0 in c's truth holder `bool`, which collapses every non-zero value to one; the cell's own mapping is over 32 bits, so this entry cannot carry this node's operand |
| 9 | c | the emulation `emu_or_gpr_gpr_32__primitive__c` declares its parameter 0 in c's truth holder `bool` (the same, on the other cell) |
| 7 | c | the emulation `emu_not_gpr_one_32__primitive__c` declares its parameter 0 in c's truth holder `bool` (the same, on the other cell) |
| 7 | c | the dictionary has no proved entry for the cell `add gpr_gpr 64` on c |
| 2 | c | the unit's own body line `xor $0x1,%eax` carries an operand that is not a register, so no IN row stands for it |
| 9 | rust | the emulation `emu_and_gpr_gpr_32__primitive__rust` declares its parameter 0 in rust's truth holder `bool` |
| 9 | rust | the emulation `emu_or_gpr_gpr_32__primitive__rust` declares its parameter 0 in rust's truth holder `bool` |
| 2 | rust | the unit's own body line `xor $0x1,%eax` carries an operand that is not a register, so no IN row stands for it |
```
*(attribution: `oracle_test.md` §5, cut to one line per cause; the
verifier reads a paragraph-length cell as an annotation, so the repeated
sentence is abbreviated here and stands in full in the file.)*

**A FINDING FOR THE LOOP, stated and not patched.** Three c entries and
two rust entries that the loop PROVED are unusable by a composition
because their parameters are the target's truth holder. It is the same
family as task ap5's `add gpr_gpr 64` on c, whose primitive match took a
`bool` first parameter and was DISPROVED (log 249). The loop's primitive
lookup keys on the cell's triple, which carries no holder; that is where
the question lives, and it is in the second list.

---

# 8. The guards, the memory, and the lanes

**THE SPELLING GUARD**, over every json this task wrote:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/hub/dictionary.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS dictionary.json -- no operator token in any key, grouping, pairing or row structure
```

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/hub/oracle_test.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS oracle_test.json -- no operator token in any key, grouping, pairing or row structure
```

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/hub/measure.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS measure.json -- no operator token in any key, grouping, pairing or row structure
```

It did not pass first time and the failure is on the record: lane
`hub1_l8` FAILED with "13 spelling-keyed place(s)", every one of them a
field `site_operator_label` this task had put on the node record beside
the `operator` the guard allows on a unit object. The second label said
nothing the first did not and it was removed; the guard was not touched.

**NO EXEMPTION** anywhere in what this task wrote:

```
$ grep -c exempt PseudoCoupHQ/Research/oracle/hub/hub.py
0
```

`grep -c exempt` over `lanes_hub1/*.sh` returns 1 on exactly two lanes,
`hub1_l14` and `hub1_l17`, and both hits are those lanes' OWN
`grep -c exempt ...` line. Every other lane returns 0. It read 1 on
`hub.py` itself until the word was taken out of the docstring sentence
that describes what the guard does with a `meta` sub-object; the sentence
says the same thing in other words and nothing else in the file changed.

**MEMORY.** Bound 6 GB resident on the one collecting process, named
abort `ABORT_MEMORY_HUB1`, checked after every unit of work. The sample
ran first as the law requires — lane `hub1_l11`, the first 12 units, 36
runs in 54 s, peak **101,328 kB**. The whole population then ran at peak
**112,136 kB**, 1.8% of the bound, and never aborted. The handful lane
peaked at 78,376 kB and the dictionary lane at 86,984 kB. No lane hit a
time or memory limit, so nothing is re-run for room.

**THE LANES**, sixteen, all kept in
`PRIVATE/PseudoCoupHQ/Research/oracle/hub/lanes_hub1/`: `l1`
toolchain probe, `l2` and `l3` the go side explored, `l4` and `l7` the
dictionary, `l5`, `l8`, `l9`, `l10` and `l13` the handful, `l6` the
grammar's real shape, `l11` the measure sampled, `l12` and `l13` the
measure whole, `l14` the pastes of this log, `l15` and `l16` the tables.
Nothing under `<runs>/` or `PUBLIC/Airlock/` was deleted,
and no shared file was changed: `emulate.py`, `go_render.py`,
`rust_render.py`, `handful.py`, `model_table.py`, `ledger.py`,
`pool100_entry_equivalence.py`, `gate.py`, `reference.py`,
`canonical_form.py`, `term97_walk.py`, `lane_gen.py` and
`go_types_oracle.go` are all IMPORTED or RUN, never edited.

---

# 9. The conventions verifier

Both passes ran FROM this task's own instance:

    python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_252_task_hub1_hub_v1_first_form.md

| pass | lane | claims | MATCHES | DIFFERS | UNVERIFIABLE | REFUSED | NOT_RERUNNABLE |
|---|---|---|---|---|---|---|---|
| 1 | `hub1_l18` | 27 | 6 | **0** | 14 | 7 | 0 |
| 2 | `hub1_l20` | 27 | 13 | **0** | 14 | 0 | 0 |
| 3 | `hub1_l21` | 28 | 13 | **0** | 15 | 0 | 0 |

**GLOSS**, and the obligation the law states is the DIFFERS column: **0
on every pass**. The first pass's seven REFUSED were defects in the
pasted COMMAND and never in the claim, and each was fixed in the command
and never in the verifier: a `sed` RANGE like `'/^## 3/,/^### rust/p'` is
a token beginning `/`, which the verifier reads as a path that does not
exist from the instance, so every one of the seven was re-spelled as a
LINE-NUMBER range over the same file. Lane `hub1_l19` re-ran the seven
rewritten commands and this log carries that output.

The 14 UNVERIFIABLE are 10 prose paragraphs, 2 attributions (a fenced
block whose lead-in names the artifact it came from, carrying no command)
and 2 bare pastes. They carry nothing to re-run BY DESIGN and each names
the file it quotes.

Pass 3 is this section itself measured: lane `hub1_l21` ran the verifier
again over the file WITH the table above in it, and the one extra claim
it counts is this section's own paste. The only thing added after pass 3
is the `hub1_l21` row and this paragraph, and they carry no command.

---

# 10. The two lists

## Decided, recorded for audit

1. **A node resolves where go's own compiler lowers that construct at
   those holders to ONE cell**, which is task o2's narrow rule over go's
   own corpus — the brief's own named source. Where go lowers it to a
   sequence, the node is a hole and the cause quotes go's own body and
   names the cells. No fallback was written for any of them.
2. **The candidate set for resolving a node is the TYPE TUPLE** (arity,
   lhs holder, rhs holder, result holder), which the ban names as
   machine-form evidence; within it the front end compares the two
   sources' own operator nodes as a parser does, and its answer is a
   named corpus unit. Every key of every artifact is machine form and the
   guard passes (§8).
3. **go's default type for an untyped boolean value is `bool`**, and that
   is how go/types' `untyped bool` at a comparison is joined to the
   corpus's own `bool`. Stated as a holder-spelling rule, in `hub.py`
   `DEFAULT_TYPE` and in §3.
4. **The go identity check is re-posed without `//go:noinline`**, both
   composed files are kept, and both verdicts are recorded. §6.
5. **A dictionary entry whose parameter is the target's truth holder, or
   is narrower than the operand it would carry, is refused BY THE
   COMPOSITION, by cause.** The dictionary and the loop are unchanged.
   §7.
6. **The value place is the only one composed from.** A cell that writes
   only flags is a hole, and it is the largest hole on every target (61
   cells, 26,348 ledger rows).
7. **The measure's body A is the corpus's own canon40 record**, not a
   rebuild, so the measure is posed against the same object every proof
   of this line has been posed against.

## Awaiting the owner

1. **The primitive route's lookup key carries no holder, and three c
   entries and two rust entries the loop PROVED are therefore unusable by
   a composition** — their parameters are the target's truth holder
   because the corpus body the lookup matched came from a truth-holder
   probe. It is the same family as task ap5's `add gpr_gpr 64` on c
   (log 249). Whether the loop's lookup should carry the matched body's
   holder widths, or whether the dictionary should record the entry as
   proved-but-not-composable, is a question about the LOOP and is not
   this task's to answer. §7.
2. **Whether Hub v2 carries a flag state across nodes.** 61 of the 253
   cells write only flags, and no comparison — the whole of `a != b`,
   `a < b` and their family — can be composed without one. It is the
   largest single hole and it is a design question, not an
   implementation one.
