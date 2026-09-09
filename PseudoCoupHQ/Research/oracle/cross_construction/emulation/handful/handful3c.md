# handful3c.md -- task g1c: the primitive lookup widened by one step, and the runs it changes

The same ten cells of the arch-opcode model table tasks h1 and h2 ran, on four targets (c, rust, go and swift) and by a route that is tried before the term route: does the target have an OPERATOR whose whole lowered body IS this cell? Where it does, that operator on holders of the operand types the corpus recorded is what is rendered, and nothing else; where it does not, the term route of tasks h1 and h2 runs unchanged, with task h2's two printing fixes still on. Never hand-edited. The products of tasks h1, h2 and the other runs of this family are not written by this task: they sit beside these as `handful.json` / `handful.md`, `handful2.json` / `handful2.md`, `handful3*` and `handful3b*`.

**A swift compiler is reachable in this run.** Task g1's `g1` instance mounted an EMPTY persist volume, so `/persist/swift/usr/bin/swiftc` -- the path the whole swift corpus was built at -- did not exist and every swift place was refused there. `g1.conf` now mounts `sandbox-persist` read-only, as `t101b.conf` and `t103.conf` already do for the same toolchain, and the container was re-created on the rebuilt image, which carries `libncurses6`. `swiftc --version` answers `Swift version 6.0.3 (swift-6.0.3-RELEASE)`. The swift spelling table is still UNMEASURED row by row: what these runs measure is the renderer's OUTPUT through the real compiler, not each spelling by its own probe.

**This report holds only the runs the widened lookup CHANGES**, which is its brief's own instruction; every other (cell, target) pair is unchanged from `handful3b.json` and is not re-run or re-printed here.

**What a run is, one sentence.** `find_emulation(cell, lang)` asks first whether `lang` has an operator whose whole lowered body IS this cell and, where it has, renders that operator on holders of the operand types the corpus recorded for it; where it has not, it takes the z3 term the reference simulator's own builder writes into each place the cell's opcode writes and has the existing renderer write that term in the target's own operators. Either way the source is compiled at that corpus's own ship flags, the body is carved back out, and z3 is asked whether it answers as the cell's term says for every input.

Table 0 -- what this run was.

| what | value |
|---|---|
| runs | 1 |
| c ship flags | lane_gen.py compile_probe: `[CLANG, "-std=c17"] + ["-O1"] + ["-c", src, "-o", obj]` -- the ship build of every c unit in the corpus |
| rust ship flags | lane_gen.py compile_probe, rust branch: `opt = ["-C", "opt-level=1", "-C", "debug-assertions=off"]` then `["rustc", "--crate-type=lib", "--emit=obj"] + opt + ["-o", obj, src]` -- the ship build of every rust unit in the corpus |
| go ship flags | lane_gen.py compile_probe, go branch: `open(go.mod).write(GOMOD)`; `open(main.go).write(p["source"])`; `cmd = ["go", "build"]` with no gcflags in the ship mode, then `cmd.extend(["-o", obj, "."])` run with cwd=the module directory -- the ship build of every go unit in the corpus |
| swift ship flags | lane_gen.py compile_probe, swift branch: `opt = ["-Onone", "-g"] if mode == "anchor" else ["-O"]`; `cmd = [SWIFTC] + opt + ["-c", src, "-o", obj]` -- the ship build of every swift unit in the corpus |
| swiftc, as this machine answers it | Swift version 6.0.3 (swift-6.0.3-RELEASE) |
| solver ceiling | 3000 ms |
| memory bound | 4194304 kB, named abort ABORT_MEMORY_G1C |
| peak resident | 87832 kB |

## 1. The runs, one section each

### 1.1 `idiv` gpr_one 32 -> c

The row, LITERAL: `idiv %edi` (`r07409`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 389 unit(s), 778 ledger row(s).

#### place `reg_rax`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
a % b
```

The source, LITERAL (`src3c/idiv_gpr_one_32__primitive__c.c`):

```
/* probe 246 -- binary % */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} % (int32_t){0})
emu_idiv_gpr_one_32__primitive__c(int32_t a, int32_t b)
{
    return a % b;
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
cltd; idiv %esi
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (2 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **UNDECIDED** -- the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows

Re-posed with more solver room (300000 ms instead of 3,000): **UNDECIDED** -- the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows

#### place `reg_rdx`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, bvsrem_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
a % b
```

The source, LITERAL (`src3c/idiv_gpr_one_32__primitive__c.c`):

```
/* probe 246 -- binary % */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} % (int32_t){0})
emu_idiv_gpr_one_32__primitive__c(int32_t a, int32_t b)
{
    return a % b;
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
cltd; idiv %esi
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (2 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **UNDECIDED** -- the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows

Re-posed with more solver room (300000 ms instead of 3,000): **UNDECIDED** -- the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows


## 2. The forty runs, one row each

Table 1 -- one row per (cell, target). `route` is `primitive` where the target has an operator whose whole lowered body IS this cell (task o2's own single-opcode rows, classified by task m1b's own classifier) and `term` where it has not. `rendered` is a GLOSS: the destination place's rendered expression on one line with the casts stripped for reading; the LITERAL source sits in that run's own section above. `gate` carries the verdict and, beside it, WHERE it holds -- every input, or a region with z3's own counterexample. `composition` is a GLOSS, task h1b's own: the RAW carved body of the destination place, each table-cell instruction by its mnemonic, `ret` and calling-convention moves counted as chaff, an instruction that maps to no table cell starred.

| cell | lang | route | rendered (GLOSS) | landed | composition (GLOSS) | gate (verdict, and where it holds) | cause if refused |
|---|---|---|---|---|---|---|---|
| `idiv` gpr_one 32 | c | primitive+setup | `a % b` | NOT_COLLAPSED (2) | `cltd` `idiv` (+3 chaff) | UNDECIDED, UNDECIDED at 300000 ms -- not decided: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows |  |

## 3. What did not work, by cause

### 3.1 Refusals and gate calls that did not prove

- `the gate answered UNDECIDED at 3,000 ms and again at 300000 ms`: 2 -- idiv gpr_one 32/c [reg_rax], idiv gpr_one 32/c [reg_rdx]

### 3.2 The landings that were not LANDED, by cause

- the cell's own arch opcode IS among the ones that remain; what sits beside it is what the term carries beyond the operation (2 remain): 2 -- idiv gpr_one 32/c [reg_rax], idiv gpr_one 32/c [reg_rdx]

## 4. Task g1's verdict beside this run's

Table 4 -- one row per (cell, target) THIS run holds, with task g1's own answer for the same pair from `handful3.json` beside it. A row whose two sides differ is a row the change moved; a row whose two sides agree is the check that nothing else did.

| cell | lang | g1 route | g1 verdict | this route | this verdict | moved |
|---|---|---|---|---|---|---|
| `idiv` gpr_one 32 | c | term | UNDECIDED, UNDECIDED at 300000 ms | primitive+setup | UNDECIDED, UNDECIDED at 300000 ms | **yes** |

## 5. Which route ran, and why

Table 3 -- the primitive lookup, per (cell, target): how many of that language's single-opcode rows classify to the cell, which row was chosen and on what ground, and -- where none did -- the cause the term route ran instead.

| cell | lang | route | single-opcode rows at this cell | chosen row's body, LITERAL | the setup cells the row carries | the operator and operand types the manifest records | cause if no primitive |
|---|---|---|---|---|---|---|---|
| `idiv` gpr_one 32 | c | primitive+setup | 2 | `mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret` | `cltd` = (`cltd`, none, 32) | `a % b on int32_t and int32_t` (probe c/op_246 of c) |  |

