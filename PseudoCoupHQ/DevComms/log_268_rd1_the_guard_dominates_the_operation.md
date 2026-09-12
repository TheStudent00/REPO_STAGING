# log 268 — task rd1: a conditional whose branch can trap is written as an `if` that dominates the operation, and go's divide family is proved

Node: `hq.research.arch_unit_oracle.cross_construction.autopoly`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/PROGRESS.md`).
It also touches the riscv64 architecture node
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/PROGRESS.md`),
whose queue of 2026-09-12 this task is the first item of.

Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_rd1_brief.md`.
Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, all of it.
It follows rv6 (`PRIVATE/PseudoCoupHQ/DevComms/log_265_rv6_every_riscv_arch_opcode_four_languages.md`)
and t4 (`PRIVATE/PseudoCoupHQ/DevComms/log_262_t4_the_general_construction_tier.md`).

Date: 2026-09-12. Instance `rd1`
(`PUBLIC/Airlock/instances/rd1.conf`). Every lane ran on the
tower guest through `bash $HOME/Programming/PUBLIC/Airlock/remote_lane.sh`;
nothing but file editing and git ran on the laptop. A lane log's host path on
the tower is
`<runs>/rd1/agent/logs/<stamp>__<lane>.sh.log`, and
every attribution below names its file. Paths inside a pasted command are the
ones the lane sees: `PseudoCoupHQ` IS
`PRIVATE/PseudoCoupHQ`. Every rendering is labelled **LITERAL**
(the object, quoted) or **GLOSS** (a plain-words reading beside a literal).

THE SPELLING BAN, pasted verbatim as required:

> **THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25
> after a second violation).** No operator token may appear in ANY
> key, grouping, pairing, row structure, candidate selection, or
> comparison scope, anywhere in this line — not in matching, not in
> "which pairs get compared", not in report rows, not in dropdowns.
> The candidate set for comparison comes from machine-form evidence
> (clusters, connections, type pairs) or from ratified intention —
> never from the token. The token appears exactly once per unit: as
> a display label on the member. HISTORY OF VIOLATIONS, so the
> pattern is visible: (1) the arch campaign's cross-language matrix
> (caught by the owner 2026-08-24); (2) verdicts.py's row pairing (caught
> by the owner 2026-08-25 — the fix brief itself reintroduced it as
> "same-operator pairs"). MECHANICAL GUARD REQUIRED: every pipeline
> stage that groups or pairs units must run the spelling-key check
> (op_pipeline/check_no_spelling_keys.py) and refuse its own output
> on failure. A brief handed to any subagent for this line MUST
> paste this paragraph verbatim.

---

## 1. What the objects are, one sentence each, in relation

- **A trapping node** is a node of a term whose operator, in ONE target, can
  stop the program instead of answering it: division and remainder on go and
  on swift, and the float-to-integer conversion on swift.
- **A guarded conditional** is a conditional of the term written as CONTROL
  FLOW — `if cond { … } else { … }` — rather than as a select over values
  already computed, so the guard DOMINATES the operation under it.
- **A region** is one nested scope of the rendered body: region 0 is the
  function body, and each arm of a guarded conditional opens one region whose
  super-region is the region the conditional itself is written in.
- **The general render** is `render_general.render`, which writes one term
  into one target as one named local variable per node of the term; it is the
  ONE file this task changed.
- **The defect** was that every node was evaluated eagerly, so a division the
  term GUARDS was executed before the guard was tested, and on go that traps
  where the cell answers.

---

## 2. The defect, as the object shows it

The riscv64 node's PROGRESS recorded it at 2026-09-12 05:20Z, with the file
`construct/general/emulations_riscv64/div_gpr_gpr_gpr_64__reg_a0__go__native_first.go`.
The term the cell states, **LITERAL**, is that file's own comment line:

```
If(v0 == 0, 18446744073709551615, If(And(v0 == 18446744073709551615, v1 == 9223372036854775808), 9223372036854775808, bvsdiv_i(v1, v0)))
```

**GLOSS.** Where the divisor is zero the cell answers all ones; where the
dividend is the most negative value and the divisor is minus one it answers
the most negative value; otherwise it answers the signed quotient. RISC-V
DEFINES an answer at the zero divisor, which is why the cell's term carries a
conditional at all.

What the render wrote for go before this task, **LITERAL** — lane
`rd1_l4_where_the_rule_fires_the_causes_and_the_guard.sh` step [2/5], the
left side of its diff:

```go
func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_div_gpr_gpr_gpr_64__reg_a0__go__native_first(a uint64, b uint64) uint64 {
	var v0 uint64 = (uint64(uint64((int64(uint64(b))) / (int64(uint64(a))))))
	var v1 bool = ((uint64(uint64(b))) == (uint64(uint64(0x8000000000000000))))
	var v2 bool = ((uint64(uint64(a))) == (uint64(uint64(0xffffffffffffffff))))
	var v3 bool = ((v2) && (v1))
	var v4 uint64 = sel64(v3, uint64(uint64(0x8000000000000000)), uint64(v0))
	var v5 bool = ((uint64(uint64(a))) == (uint64(uint64(0x0))))
	var v6 uint64 = sel64(v5, uint64(uint64(0xffffffffffffffff)), uint64(v4))
	return uint64(v6)
}
```

**GLOSS, values in motion.** Call it with `a = 0` and `b = 7`. Line 1
computes `7 / 0`, and go's own specification says the program stops there
with a run-time panic. Lines 2 to 5 never run. Line 6 would have answered all
ones, which is what the cell says, and the body never reaches it. The guard
is written AFTER the operation it guards, which is not a guard.

---

## 3. The change: one rule, on the node's kind and on the target's trapping operators

### 3.1 The rule as it is written

`render_general.py` gained one rule and nothing else. In the file's own words
(its module docstring), **LITERAL**:

```
    when a conditional's branch (transitively) contains a trapping
    node, the conditional is written as CONTROL FLOW --
    `if cond { <the then arm's nodes> } else { <the else arm's
    nodes> }`, each arm's nodes computed INSIDE its arm -- so the guard
    DOMINATES the operation.  Otherwise the conditional stays a select
    over values already computed.  A node whose readers are not all
    inside one arm stays hoisted above the conditional.
```

THE TERM IS UNCHANGED and only the printed ORDER is, so the Lean statement
(`lean_general.py`) is untouched: it states the term, not the order.

### 3.2 What "trapping" is read off, and it is never a token

The set is `TRAPPING_KINDS` in `render_general.py`, keyed by z3's own
DECLARATION KINDS and by the target. Every row of it is a reading of that
target's own renderer, and the two rows that say NOT are readings too:

| target | the kinds | the reading, from the target's own renderer |
|---|---|---|
| go | the ten division and remainder kinds | `go_render.emit_division`, measured: "go checks the zero divisor and branches into runtime.panicdivide -- the EDGE REGION, rendered rather than hidden" |
| swift | the same ten | `swift_render.emit_division`: "swift's `/` and `%` on a fixed-width integer trap on a zero divisor and on the signed extreme by the language's own definition" |
| swift | the two float-to-integer conversions | `swift_render.emit_fp`: "swift's `Int64(_: Double)` TRAPS when the value does not fit … That is an edge region like division's, recorded, not hidden" |
| swift | its plain arithmetic is NOT in the set | `swift_render.emit_arith` never writes plain arithmetic: the three arithmetic kinds are written `&+ &- &*`, swift's own wrapping forms, which do not trap |
| rust | NOT in the set | `rust_render.emit_division` writes the divide under `core::hint::unreachable_unchecked`, which it measured (lanes o11_l1, o11_l3, o11_l4) removes both of rust's checks and the panic route with them |
| c, c++ | NOT in the set | neither renderer marks an edge region and neither language defines a trap for the divide — clang emits the bare instruction |

There is no case per opcode name anywhere in the rule. The question asked of
a node is its z3 declaration kind; the question asked of a target is which
kinds its own renderer writes with an operator that can trap.

### 3.3 How a node is placed in an arm, mechanically

`plan_the_regions` runs before one statement is written, and answers two
things about the term:

1. Every node is visited leaves first, and `traps_below[node]` is true when
   the node itself will be written with a trapping operator, or any node it
   reads will be.
2. A conditional is BRANCHING when `traps_below` holds of either arm.
3. Regions are then assigned readers-first: a node is written in the
   INNERMOST region that encloses every place it is read, computed as the
   join of its readers' regions in the region tree. A value read through the
   then-edge of a branching conditional is demanded in that conditional's
   then-region; a value read anywhere else is demanded in its reader's own
   region.

Step 3 is why "nodes shared by both arms and by the rest stay hoisted" needs
no rule of its own: the join of two arms IS the region the conditional itself
is written in.

Under `all_constructed` the rule never fires, and that is not a special case
either: a constructed divide is built from `& | ^ ~`, constant shifts and a
conditional, so it holds no trapping node at all. §7.2 measures exactly that.

---

## 4. What the object looks like now, and what the compiler did with it

### 4.1 The rendered source, after

Lane `rd1_l1_the_guard_dominates_and_the_six_cell_sample.sh` step [3/5],
**LITERAL**, the whole file:

```go
// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of div_gpr_gpr_gpr_64__reg_a0__go__native_first.
//   If(v0 == 0, 18446744073709551615, If(And(v0 == 18446744073709551615, v1 == 9223372036854775808), 9223372036854775808, bvsdiv_i(v1, v0)))
package main

//go:noinline
func emu_div_gpr_gpr_gpr_64__reg_a0__go__native_first(a uint64, b uint64) uint64 {
	var v5 bool = ((uint64(uint64(a))) == (uint64(uint64(0x0))))
	var v6 uint64 = 0
	if v5 {
		v6 = uint64(0xffffffffffffffff)
	} else {
		var v1 bool = ((uint64(uint64(b))) == (uint64(uint64(0x8000000000000000))))
		var v2 bool = ((uint64(uint64(a))) == (uint64(uint64(0xffffffffffffffff))))
		var v3 bool = ((v2) && (v1))
		var v4 uint64 = 0
		if v3 {
			v4 = uint64(0x8000000000000000)
		} else {
			var v0 uint64 = (uint64(uint64((int64(uint64(b))) / (int64(uint64(a))))))
			v4 = v0
		}
		v6 = v4
	}
	return uint64(v6)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_div_gpr_gpr_gpr_64__reg_a0__go__native_first(g0, g1)
	_ = sink
}
```

**GLOSS, the same values in motion.** Call it with `a = 0`, `b = 7`. `v5` is
true, the then-arm answers all ones, and the divide is never reached — it is
written inside the else-arm of the conditional that excludes zero. The helper
`sel64` is gone from the file because no select is written any more.

### 4.2 The compiled body

Compiled for riscv64 at the corpus's ship flags and carved at its symbol.
Lane `rd1_l1_the_guard_dominates_and_the_six_cell_sample.sh` step [4/5],
**LITERAL**:

```
the compile command: GOARCH=riscv64 GOOS=linux go build -o /work/rd1body/bin_rv .
14 instructions
 0  bne a0, zero, 0x6c72a <main.emu_div_gpr_gpr_gpr_64__reg_a0__go__native_first+0xa>
 1  c.li t0, -0x1
 2  jal zero, 0x6c746 <main.emu_div_gpr_gpr_gpr_64__reg_a0__go__native_first+0x26>
 3  addi t0, a0, 0x1
 4  bne t0, zero, 0x6c742 <main.emu_div_gpr_gpr_gpr_64__reg_a0__go__native_first+0x22>
 5  c.li t0, -0x1
 6  c.slli t0, 0x3f
 7  bne t0, a1, 0x6c742 <main.emu_div_gpr_gpr_gpr_64__reg_a0__go__native_first+0x22>
 8  c.li t0, -0x1
 9  c.slli t0, 0x3f
10  jal zero, 0x6c746 <main.emu_div_gpr_gpr_gpr_64__reg_a0__go__native_first+0x26>
11  div t0, a1, a0
12  c.mv a0, t0
13  jalr zero, 0x0(ra)
```

**GLOSS.** One `div`; no call to `runtime.panicdivide`; and no check of go's
own beyond the two the term itself states. The compiler saw that the zero
case and the extreme case are already excluded on the path that reaches the
divide, and dropped its own. This is the shape the owner's question of 2026-09-12
predicted and lane `rv7_l1_go_div_body.sh` measured by hand (12 instructions
there, for a body written without the named intermediates).

---

## 5. The six-cell sample

Lane `rd1_l1_the_guard_dominates_and_the_six_cell_sample.sh`, tower log
`<runs>/rd1/agent/logs/20260912T065240Z__rd1_l1_the_guard_dominates_and_the_six_cell_sample.sh.log`,
`state=done exit=0` in 162.1 s.

The population is ordered by a MACHINE-FORM filter and never by a name: a
cell is in the divide family when its own term holds a node of z3's own
division or remainder declaration kinds. **LITERAL**:

```
   the filter: a cell whose term holds a node of z3's own division or remainder kinds
   16 of 255 cells are in that family; the sample takes the first 6 cells of the family-first order
     div gpr_gpr_gpr 64, places reg_a0
     div gpr_gpr_same 64, places reg_a0
     divu gpr_gpr_gpr 64, places reg_a0
     divu gpr_gpr_same 64, places reg_a0
     divuw gpr_gpr_gpr 32, places reg_a0
     divuw gpr_gpr_same 32, places reg_a0
```

Six cells on four languages, both routes each: 24 runs in 161 s, peak RSS
363,652 kB. **LITERAL**, step [5/5]:

```
   census:      {'proved': 17, 'sat': 5, 'undecided': 2}
   per target:  {'c': {'proved': 4, 'sat': 1, 'undecided': 1}, 'cpp': {'proved': 4, 'sat': 1, 'undecided': 1}, 'go': {'proved': 6}, 'rust': {'proved': 3, 'sat': 3}}
```

| language | proved | disproved | undecided | of the six sampled cells |
|---|---|---|---|---|
| c | 4 | 1 | 1 | 6 |
| c++ | 4 | 1 | 1 | 6 |
| rust | 3 | 3 | 0 | 6 |
| go | 6 | 0 | 0 | 6 |

**GLOSS.** go proves all six. The c, c++ and rust disproofs on this sample
are not this task's: those three targets' sources did not change at all
(§7.1), and the cells they fail on are the `gpr_gpr_same` forms — the queue's
second item (a compiled `if` walked in text order), not the render's order.

---

## 6. rv6 again, under the guarded render

Lane `rd1_l2_rv6_again_every_cell_four_languages.sh`, tower log
`<runs>/rd1/agent/logs/20260912T065642Z__rd1_l2_rv6_again_every_cell_four_languages.sh.log`,
`state=done exit=0` in 2,590.0 s. The driver is `rv6_all_langs.py` itself,
imported so the run is its own, ONE process and no pool. The bound it
printed, **LITERAL**: `the memory bound: 6291456 kB, abort
ABORT_MEMORY_RD1`. 1,020 runs in 2,589 s, peak RSS 1,165,012 kB. Store:
`construct/general/rd1_all.jsonl` — log_265's `rv6_all.jsonl` is untouched,
so the two are read side by side.

### 6.1 The table, population 255 on every row

Lane `rd1_l2` step [3/3]. Both tables are computed from the two stores by the
SAME reader in the same run, which is why they can be set against each other.
**LITERAL**, log_265's rv6, the eager render:

| language | proved | disproved | undecided | refused | of |
|---|---|---|---|---|---|
| c | 242 | 3 | 8 | 2 | 255 |
| c++ | 242 | 3 | 8 | 2 | 255 |
| rust | 246 | 5 | 4 | 0 | 255 |
| go | 238 | 7 | 2 | 8 | 255 |
| proved on at least one of the four | 251 | | | | 255 |
| proved on all four | 231 | | | | 255 |

It reproduces log_265's own table row for row, which is the check that the
two readings are one reading. **LITERAL**, rd1, the guarded render:

| language | proved | disproved | undecided | refused | of |
|---|---|---|---|---|---|
| c | 242 | 3 | 8 | 2 | 255 |
| c++ | 242 | 3 | 8 | 2 | 255 |
| rust | 246 | 5 | 4 | 0 | 255 |
| go | 240 | 5 | 2 | 8 | 255 |
| proved on at least one of the four | 251 | | | | 255 |
| proved on all four | 231 | | | | 255 |

### 6.2 The disproved column, before → after

| language | disproved, rv6 | disproved, rd1 | of |
|---|---|---|---|
| c | 3 | 3 | 255 |
| c++ | 3 | 3 | 255 |
| rust | 5 | 5 | 255 |
| go | 7 | 5 | 255 |

Every verdict that moved, and there are exactly two. **LITERAL**:

| mnem | shape | width | language | rv6 | rd1 |
|---|---|---|---|---|---|
| `div` | `gpr_gpr_gpr` | 64 | go | sat | proved |
| `rem` | `gpr_gpr_gpr` | 64 | go | sat | proved |

**GLOSS.** `sat` is the pipeline's own token for DISPROVED: z3 found an input
at which the body and the cell differ. The census beside it, **LITERAL**: rv6
`proved 968, refused 12, sat 18, undecided 22`; rd1 `proved 970, refused 12,
sat 16, undecided 22`, over the 1,020 (cell, target) runs before the two
policies collapse into one verdict per cell.

The same two numbers, re-derivable from the two stores:

```
$ python3 -c "import json; p='PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/'; f=lambda n:[json.loads(l) for l in open(p+n)]; g=lambda rs:{(r['cell']['mnem'],r['cell']['shape'],r['cell']['key_width'],r['target']):r['kind'] for r in rs}; h=lambda d,k:sum(1 for x in d if x[3]=='go' and d[x]==k); a=g(f('rv6_all.jsonl')); b=g(f('rd1_all.jsonl')); print(h(a,'proved'), h(a,'sat'), h(b,'proved'), h(b,'sat'))"
238 7 240 5
```

### 6.3 The count beside rv3's 117 of 255

Lane `rd1_l2` step [2/3], **LITERAL**:

| what | cells | share of the 255 |
|---|---|---|
| RISC-V cells `twins.json` holds | 255 | 100% |
| reached by an INHERITED proved certificate, rv3 | 35 | 13.7% |
| PROVED by task rv2's own loop | 82 | 32.2% |
| union, rv3's headline | 117 | 45.9% |
| PROVED by THIS task's general tier | 251 | 98.4% |
| **union, the inheritance with rv2's loop and this tier** | **251** | **98.4%** |

The four never proved on any language are unchanged and are the multiply-high
family, exactly as log_265 left them.

---

## 7. Where the rule fires, and where nothing moved

Lane `rd1_l4_where_the_rule_fires_the_causes_and_the_guard.sh`, tower log
`<runs>/rd1/agent/logs/20260912T075318Z__rd1_l4_where_the_rule_fires_the_causes_and_the_guard.sh.log`,
`state=done exit=0` in 66.2 s.

### 7.1 c, c++ and rust are untouched, byte for byte

Step [1/5], the sample's 48 rendered sources against the pre-rd1 render saved
in `emulations_riscv64/`. **LITERAL**:

| language | sources byte-identical to the pre-rd1 render | sources that differ |
|---|---|---|
| c | 12 | 0 |
| cpp | 12 | 0 |
| rust | 12 | 0 |
| go | 6 | 6 |

**GLOSS.** Twelve sources per language is six cells under two policies. On go
the six that differ are the `native_first` ones and the six that do not are
the `all_constructed` ones, which is what §3.3's last paragraph says must
happen.

### 7.2 The rule fires on 16 cells of 255, all on go, all on one route

Step [3/5], a render-only pass (no compile, no gate) over every cell.
**LITERAL**:

| language | policy | cells rendered | cells with a guarded conditional | guarded conditionals |
|---|---|---|---|---|
| go | native_first | 255 | 16 | 34 |
| go | all_constructed | 235 | 0 | 0 |
| c | native_first | 255 | 0 | 0 |
| c | all_constructed | 235 | 0 | 0 |

The sixteen, **LITERAL**, each with the number of guarded conditionals its
render carries:

| mnem | shape | width | guarded conditionals |
|---|---|---|---|
| `div` | `gpr_gpr_gpr` | 64 | 2 |
| `div` | `gpr_gpr_same` | 64 | 2 |
| `divu` | `gpr_gpr_gpr` | 64 | 1 |
| `divu` | `gpr_gpr_same` | 64 | 1 |
| `divuw` | `gpr_gpr_gpr` | 32 | 2 |
| `divuw` | `gpr_gpr_same` | 32 | 2 |
| `divw` | `gpr_gpr_gpr` | 32 | 3 |
| `divw` | `gpr_gpr_same` | 32 | 3 |
| `rem` | `gpr_gpr_gpr` | 64 | 2 |
| `rem` | `gpr_gpr_same` | 64 | 2 |
| `remu` | `gpr_gpr_gpr` | 64 | 1 |
| `remu` | `gpr_gpr_same` | 64 | 1 |
| `remuw` | `gpr_gpr_gpr` | 32 | 2 |
| `remuw` | `gpr_gpr_same` | 32 | 2 |
| `remw` | `gpr_gpr_gpr` | 32 | 4 |
| `remw` | `gpr_gpr_same` | 32 | 4 |

**GLOSS.** Sixteen cells is exactly the divide family the machine-form filter
found in §5, and 34 guarded conditionals over them. The 235 rendered under
`all_constructed` against 255 under `native_first` is that policy's own
refusals, unchanged by this task.

### 7.3 What is left disproved, by cause

Step [4/5], every `sat` row of `rd1_all.jsonl` with its counterexample.
**LITERAL**:

| mnem | shape | width | language | outcome | the counterexample |
|---|---|---|---|---|---|
| `czero.eqz` | `gpr_gpr_gpr` | 64 | go | DISPROVED | {'seed_x11': '18446744073709551615', 'seed_x12': '18446744073709551615'} |
| `czero.eqz` | `gpr_gpr_same` | 64 | go | DISPROVED | {'seed_x11': '18446744073709551615'} |
| `czero.nez` | `gpr_gpr_gpr` | 64 | go | DISPROVED | {'seed_x11': '18446744073709551615', 'seed_x12': '0'} |
| `div` | `gpr_gpr_same` | 64 | rust | DISPROVED | {'seed_x11': '0'} |
| `divu` | `gpr_gpr_same` | 64 | rust | DISPROVED | {'seed_x11': '0'} |
| `divuw` | `gpr_gpr_same` | 32 | c | DISPROVED | {'seed_x11': '16826030897479286784'} |
| `divuw` | `gpr_gpr_same` | 32 | c++ | DISPROVED | {'seed_x11': '17803084061229449216'} |
| `divuw` | `gpr_gpr_same` | 32 | rust | DISPROVED | {'seed_x11': '0'} |
| `divw` | `gpr_gpr_same` | 32 | c | DISPROVED | {'seed_x11': '4611686018427387904'} |
| `divw` | `gpr_gpr_same` | 32 | c++ | DISPROVED | {'seed_x11': '2305843009213693952'} |
| `divw` | `gpr_gpr_same` | 32 | rust | DISPROVED | {'seed_x11': '0'} |
| `fcvt.d.lu` | `fpr_gpr` | 64 | go | DISPROVED | {'fp.to_ieee_bv': '[else -> fp.to_ieee_bv(Var(0))]', 'seed_x11': '8557692487'} |
| `fcvt.s.lu` | `fpr_gpr` | 32 | go | DISPROVED | {'fp.to_ieee_bv': '[else -> fp.to_ieee_bv(Var(0))]', 'seed_x11': '29360127'} |
| `sraiw` | `gpr_gpr_imm` | 32 | c | DISPROVED | {'seed_x11': '2147483648'} |
| `sraiw` | `gpr_gpr_imm` | 32 | c++ | DISPROVED | {'seed_x11': '2147483648'} |
| `sraiw` | `gpr_gpr_imm` | 32 | rust | DISPROVED | {'seed_x11': '2147483648'} |

Read by cause, and the two classes are named against each other:

- **On go, not a divide any more (5 of 5).** go's five remaining disproofs
  are the two conditional-zero cells, the conditional-zero-if-nonzero cell,
  and the two unsigned-64-to-float conversions. NO divide and NO remainder
  cell is disproved on go.
- **On c, c++ and rust, still the `gpr_gpr_same` divides (8 of 13).** Those
  three targets' sources did not change at all (§7.1), so these are the
  queue's second item — a compiled `if` walked in text order — and not the
  render's order. `sraiw` on the same three is the same shape of reading.

### 7.4 What is refused, unchanged

Step [4/5], **LITERAL** in cause only: six `mulh` / `mulhsu` / `mulhu` rows on
go with "the carved body is larger than the number of instructions this
task's gate is offered", and six `remu gpr_gpr_gpr 64` / `remu gpr_gpr_same
64` rows on c, c++ and go with the bare cause `BUILD_REFUSED` and no message
— which is the queue's fourth item, unchanged and still owed.

---

## 8. The x86 leg: the rule has nothing to fire on there

Lane `rd1_l6_the_x86_divide_family_by_the_source_and_the_bank.sh`, tower log
`<runs>/rd1/agent/logs/20260912T102428Z__rd1_l6_the_x86_divide_family_by_the_source_and_the_bank.sh.log`,
`state=done exit=0` in 65.3 s. Peak resident 292,180 kB.

### 8.1 The family, in machine form

The same filter as §5, over the x86 cells: **LITERAL**,

```
   8 x86 cells whose term holds a division or remainder node
     div gpr_one 8
     idiv gpr_one 8
     div gpr_one 16
     idiv gpr_one 16
     div gpr_one 32
     idiv gpr_one 32
     div gpr_one 64
     idiv gpr_one 64
```

### 8.2 The delta is EMPTY, and it is empty by the source

Every (cell, place, language, policy) of the family was rendered again on go
and on swift and compared with the source task t4 saved in
`autopoly/src_t4_general/`. **LITERAL**, the whole `guarded conditionals`
column is 0 and every comparison that had a t4 source to compare against says
`byte-identical`. The rows where t4 saved nothing are the (cell, language)
pairs t4's pass never posed — its pass runs "every place the native route did
not prove". A sample of the table, **LITERAL**:

| cell | place | language | policy | t4 source | rd1 source | guarded conditionals | statements |
|---|---|---|---|---|---|---|---|
| `idiv` `gpr_one` 32 | reg_rax | go | native_first | saved | byte-identical | 0 | 9 |
| `idiv` `gpr_one` 32 | reg_rax | go | all_constructed | saved | byte-identical | 0 | 8928 |
| `idiv` `gpr_one` 32 | reg_rax | swift | native_first | saved | byte-identical | 0 | 9 |
| `div` `gpr_one` 64 | reg_rax | go | native_first | saved | byte-identical | 0 | 27322 |
| `div` `gpr_one` 64 | reg_rax | swift | native_first | saved | byte-identical | 0 | 27322 |
| `idiv` `gpr_one` 64 | reg_rdx | go | native_first | saved | byte-identical | 0 | 27461 |

Because no source changed, step [3/3] — "the verdict beside t4's, for every
changed (cell, language) t4 has a row for" — printed its header and no rows,
and t4's collapse column stands exactly as log_262 §3 left it:

| target | landing | places | instructions, summed | instructions, mean | changed by rd1 |
|---|---|---|---|---|---|
| go | IDENTITY | 2 | 2 | 1.0 | no |
| go | LANDED | 5 | 10 | 2.0 | no |
| go | LANDED_ELSEWHERE | 2 | 4 | 2.0 | no |
| go | NO LANDING RECORDED | 1 | 0 | 0.0 | no |
| go | NOT_COLLAPSED | 8 | 154395 | 19299.4 | no |
| swift | LANDED | 4 | 11 | 2.8 | no |
| swift | LANDED_ELSEWHERE | 28 | 31 | 1.1 | no |
| swift | NOT_COLLAPSED | 22 | 130 | 5.9 | no |

### 8.3 WHY it is empty, and this is the interesting part

The rule fires on a CONDITIONAL whose branch holds a trapping node. The x86
divide cells have no conditional at all. The term of `div gpr_one 64`,
**LITERAL** (the comment line of
`autopoly/src_t4_general/div_gpr_one_64__reg_rax__go__native_first.go`):

```
Extract(63, 0, bvudiv_i(Concat(v0, v1), Concat(0, v2)))
```

and the whole of `idiv gpr_one 32` on go, **LITERAL**, where the divide IS
taken natively (a 64-bit node go has a holder for) and is still not under any
conditional:

```go
//go:noinline
func emu_idiv_gpr_one_32__reg_rax__go__native_first(a uint32, b uint32, c uint32) uint64 {
	var v0 uint32 = uint32(c)
	var v1 uint32 = ((uint32((uint32(c)) >> 31)) & uint32(0x1))
	var v2 uint64 = (uint64(((uint64(v1)) << 63) | ... | (uint64(v0))))
	var v3 uint32 = uint32(b)
	var v4 uint32 = uint32(a)
	var v5 uint64 = (uint64(((uint64(v4)) << 32) | (uint64(v3))))
	var v6 uint64 = (uint64(uint64((int64(v5)) / (int64(v2)))))
	var v7 uint32 = (uint32((uint64(v6)) >> 0))
	var v8 uint64 = (uint64(((uint64(uint32(0x0))) << 32) | (uint64(v7))))
	return uint64(v8)
}
```

(the elision in `v2` is 32 shifted terms of the same shape, cut here for
reading; the file itself is whole.)

**GLOSS, and the contrast with §2 named on both sides.** RISC-V DEFINES an
answer for the zero divisor, so its cell's term carries `If(divisor == 0, all
ones, …)` — a conditional, with the divide inside one arm, which is exactly
what the rule acts on. x86 RAISES on the zero divisor instead of answering,
so the reference's term for the same operation carries no conditional at all
— there is nothing above the divide to dominate it. The delta on x86 is
therefore empty for a reason about the two ARCHITECTURES and not about the
render: the render behaves identically, and on x86 there is no guard in the
term to hoist the operation under.

### 8.4 FLAG — the first shape of this lane did not come back

Lane `rd1_l5_the_x86_divide_family_before_and_after.sh`, tower log
`<runs>/rd1/agent/logs/20260912T075426Z__rd1_l5_the_x86_divide_family_before_and_after.sh.log`,
offered every cell of the family to the whole tier (native route, both
policies, compile, carve, gate). It printed its table header and then nothing
for 9,000 s, and its own `timeout` stopped it. **LITERAL**, the last lines of
that lane:

```
| cell | place | language | route | t4 outcome | rd1 outcome | t4 collapse | rd1 collapse | t4 statements | rd1 statements | t4 instructions | rd1 instructions |
|---|---|---|---|---|---|---|---|---|---|---|---|
  exit: 124
```

**GLOSS.** The first pair, `div gpr_one 8` on go, did not come back inside
9,000 s. Five of the eight family cells have NO row in t4's store, because
t4's pass poses only the places the native route did not prove; posing one
now means the printed-term equality task t4 measured at 900 s a lane
(log_262 §3.2). The answer was not made to fit: lane `rd1_l6` decides the
same delta from the SOURCE, which is exact, and would have re-gated any
(cell, language) whose source changed and for which t4 has a row — there were
none.

### 8.5 FLAG — swift on the 64-bit x86 divides, unchanged and still out of budget

Lane `rd1_l3_the_x86_divide_family_on_go_and_swift.sh`, tower log
`<runs>/rd1/agent/logs/20260912T074020Z__rd1_l3_the_x86_divide_family_on_go_and_swift.sh.log`,
ABORTed the run on the swift compile of `idiv gpr_one 64`. **LITERAL**:

```
subprocess.TimeoutExpired: Command '['/persist/swift/usr/bin/swiftc', '-O', '-c', '/tmp/g1_k3khwp6f/unit.swift', '-o', '/tmp/g1_k3khwp6f/unit_ship.o']' timed out after 600 seconds
```

Task t4's own store records the same three refusals for the same three pairs,
**LITERAL** from `autopoly/t4_general_runs.jsonl`:

```
idiv gpr_one 64 swift : TimeoutExpired: ... timed out after 600 seconds
idiv gpr_one 32 swift : Z3Exception: b'out of memory'
div  gpr_one 64 swift : TimeoutExpired: ... timed out after 600 seconds
```

**GLOSS.** The 600 s budget is `swift_render.compile_and_carve`'s own, and
that file is not one this brief authorises changing. The source for those
pairs is byte-identical before and after (§8.2), so the refusal is unchanged
by this task and is reported rather than worked around.

---

## 9. The guard, the count, and the verifier

### 9.1 The spelling-key guard

Lane `rd1_l4` step [5/5], over every json this task wrote. **LITERAL**:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/rd1_all.json PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/rd1_sample.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS rd1_all.json -- no operator token in any key, grouping, pairing or row structure
PASS rd1_sample.json -- no operator token in any key, grouping, pairing or row structure
```

`check_no_spelling_keys.py` was not modified; its sha256 is unchanged from
the one task t4 recorded.

### 9.2 `grep -c exempt` over the files this task added

Zero on four of the five lane scripts, and three on the fifth — which are the
check's OWN command and its label, not an exemption in anything. **LITERAL**:

```
$ grep -n exempt PseudoCoupHQ/Research/oracle/riscv/lanes_rd1/rd1_l4_where_the_rule_fires_the_causes_and_the_guard.sh
209:echo "[5/5] the spelling guard over every json this task wrote, and the exempt count"
213:echo -n "  grep -c exempt over the files this task added: "
214:grep -c exempt "$RV/lanes_rd1/"*.sh | tr '\n' ' '
```

`render_general.py`, the one file changed, carries no `exempt` at all:

```
$ grep -c exempt PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/render_general.py
0
```

### 9.3 The file this task changed

```
$ sha256sum PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/render_general.py
f5af7386ead5921926b2bd8294d0a5cfc556ac1f0395a5d67e0992ca0bd2f677  PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/render_general.py
```

### 9.4 The verifier

Lane `rd1_l8_the_verifier_over_the_final_log_268.sh`, from THIS task's
instance, tower log
`<runs>/rd1/agent/logs/20260912T103336Z__rd1_l8_the_verifier_over_the_final_log_268.sh.log`,
`state=done exit=0`. The tally, **LITERAL**:

```
## log_268_rd1_the_guard_dominates_the_operation.md
   claims 23 | MATCHES 5 | DIFFERS 0 | UNVERIFIABLE 18 | REFUSED 0 | NOT_RERUNNABLE 0
   VERDICT: 5 of 23 claims reproduce; 18 (78%) carry nothing to re-run

causes, by name:
  attribution_only                 14
  prose_only                       4
```

ZERO DIFFERS. The five that reproduce are the five shell transcripts of §6.2
and §9; the eighteen that carry nothing to re-run are attributions to a lane
log and glosses beside them, which is the shape this tool names
`attribution_only` and `prose_only` and counts rather than passes.

THE ONE THING THIS TALLY CANNOT COUNT IS ITSELF. It is the reading of this
log as lane `rd1_l8` read it, which is this text with the block above still
saying what lane `rd1_l7` found (22 claims, 5 MATCHES, 0 DIFFERS, 17
UNVERIFIABLE, over the same log before it carried any tally). Replacing those
numbers with these adds no claim and removes none: the block is one
attribution either way, so re-running the verifier once more would print
exactly the tally above.

---

## 10. The two lists

### 10.1 Decided, recorded for audit

1. **The trapping set is go and swift only**, and rust, c and c++ are out of
   it — each by a reading of that target's own renderer, pasted in §3.2.
2. **The rule is keyed on z3's declaration kinds**, never on a mnemonic or a
   source token; the divide family is selected the same way everywhere in
   this task (§5, §8.1).
3. **A new store rather than an overwrite.** The run wrote
   `construct/general/rd1_all.jsonl` and `rd1_sample.jsonl`; log_265's
   `rv6_all.jsonl` was not touched, so the before and the after are both on
   disk and §6.1's two tables are computed from them by one reader.
4. **`emulations_riscv64/` still holds the PRE-rd1 render**, deliberately:
   the riscv64 node's PROGRESS of 05:20Z names the go divide file there as
   the defect, and that evidence is left standing. The post-rd1 sources of
   the sample are in `construct/general/src_rd1_sample/`.
5. **One field added to the render's own returned record**, `guards`, read
   only by this task's lanes; no store row and no certificate gained a field.
6. **Lane `rd1_l5` was left to reach its own ceiling** rather than being
   stopped by hand, and `rd1_l6` answers the same question from the source.
   Both lanes are in the repo; neither was deleted.

### 10.2 Awaiting the owner

1. **The queue's second item is now the whole of the disproved column.**
   Eight of the thirteen remaining disproofs are the `gpr_gpr_same` divides
   on c, c++ and rust, whose sources this task did not touch; they are the
   text-order walk. Nothing else in the disproved column is a divide.
2. **Whether `emulations_riscv64/` should be re-rendered** now that the go
   sources there are one round old. It is 1,960 files and 59 MB; this task
   left it alone on the reasoning in 10.1(4).
