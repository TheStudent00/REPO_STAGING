# log 241 — task g1: `find_emulation` for go and swift, primitive-first

Node: `hq.research.arch_unit_oracle`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`,
the "goal" section of 2026-09-07 and the ruling of 2026-09-08). The
PROGRESS entry is on the autopoly sub-node
(`.../node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/PROGRESS.md`),
beside tasks o12, o13, h1, h1b and h2.

Date: 2026-09-09. Instance `g1`, on the TOWER. Artifact folder (the same
one tasks h1, h1b and h2 wrote, plus two new sub-folders):
[`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/`](file://PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/).

**WHO WROTE THIS LOG, said plainly.** Task g1's own session ended on a
usage limit after its run of record (lane `g1_l12_run_of_record2.sh`)
and its guard (lane `g1_l15_guard4.sh`), before it wrote anything to
DevComms. This log is written by task g1b, the closer, from what task
g1 left on disk. **Nothing in it was re-run**: `handful3.json`,
`handful3.md`, `handful3_primitive.json` and `handful3_spellings.json`
are byte-identical on the laptop and on the tower, and every count
below is printed off those files by one read-only lane,
`g1b_l3_evidence_g1_2.sh`. Task g1b's own work — swift on the rebuilt
image, and the widened primitive lookup — is a separate log.

The deliverables:

- [`go/go_facts.py`](file://PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/go/go_facts.py)
  and
  [`go/go_facts.json`](file://PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/go/go_facts.json)
  — go's own compiler behaviour, MEASURED by probe before any spelling
  was written (task o11 §3.1's shape).
- [`go/go_render.py`](file://PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/go/go_render.py)
  — `GoRenderer(E.Renderer)`.
- [`swift/swift_render.py`](file://PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/swift/swift_render.py)
  — `SwiftRenderer(E.Renderer)`, written but UNMEASURED (§9).
- [`handful/handful.py`](file://PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py)
  extended with section 2d and the `*3` commands.
- [`handful/handful3.json`](file://PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3.json)
  and
  [`handful/handful3.md`](file://PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3.md)
  — the forty runs.
- [`handful/handful3_primitive.json`](file://PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3_primitive.json)
  — the primitive lookup's own evidence, before any run.
- [`handful/handful3_spellings.json`](file://PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3_spellings.json)
  — the two new targets' spelling tables.

**Tasks h1's, h1b's and h2's products were not written by any lane of
task g1**; the new products sit beside them, and the rendered sources
are under `src3/` beside `src/` and `src2/`.

Every rendering here is labelled per the protocol's
`object.literal-gloss-analogy`: **LITERAL** is the object itself,
quoted; **GLOSS** is a plain-words reading beside a literal. No gloss
appears without its literal.

Paths inside a pasted command are the ones the lane sees:
`PseudoCoupHQ` IS `PRIVATE/PseudoCoupHQ`, mounted into
the instance. Prose names host paths. **The lane logs are on the
TOWER** (`<user>@<tower>`), under
`<runs>/g1/agent/logs/`, and every attribution
below names one of them.

| lane | what it did | log, on the tower |
|---|---|---|
| `g1_l1_toolchains.sh` | the four compilers, each answering its own version flag; `swiftc` at the path `lane_gen.py` names does not exist | `20260909T065344Z__g1_l1_toolchains.sh.log` |
| `g1_l2_swift_where.sh` | where swift is NOT: `/persist` empty, `swiftc` not on PATH, no file named `swiftc` anywhere on the image, and the swift branch of `lane_gen.py` LITERAL | `20260909T065422Z__g1_l2_swift_where.sh.log` |
| `g1_l3_go_facts.sh`, `g1_l4_go_facts2.sh`, `g1_l5_go_facts3.sh` | go's own behaviour measured probe by probe, into `go_facts.json` | `...065722Z`, `...070047Z`, `...070249Z` |
| `g1_l6_primitive_lookup.sh` | the primitive lookup alone over the forty pairs | `20260909T072140Z__g1_l6_primitive_lookup.sh.log` |
| `g1_l7_lookup_and_run.sh` | the lookup joined to the run, on a subset | `20260909T072319Z__g1_l7_lookup_and_run.sh.log` |
| `g1_l8_compose_report.sh` | the composition column and the report | `20260909T072442Z__g1_l8_compose_report.sh.log` |
| `g1_l9_run_of_record.sh` | the first end-to-end run of the forty | `20260909T072631Z__g1_l9_run_of_record.sh.log` |
| `g1_l11_read_the_run.sh` | that run's tally, by-cause list and re-posed gate calls | `20260909T075916Z__g1_l11_read_the_run.sh.log` |
| `g1_l12_run_of_record2.sh` | **THE RUN OF RECORD**: lookup, forty runs, every UNDECIDED gate call re-posed at 300,000 ms, composition, report, spelling tables — one lane, so `handful3.json` is written end to end by one version of the program. 1,852.2 s, exit 0 | `20260909T080038Z__g1_l12_run_of_record2.sh.log` |
| `g1_l10_guard.sh`, `g1_l13_guard2.sh`, `g1_l14_guard3.sh`, `g1_l15_guard4.sh` | the unmodified spelling guard, four attempts; `g1_l15` is the one that passes on all four json | `20260909T083431Z__g1_l15_guard4.sh.log` |
| `g1b_l1_evidence_g1.sh` (task g1b's, read-only) | the first pass of the transcripts below; its one `python3 -c` step was REFUSED by the conventions verifier, which splits a pasted command on `;` and then reads the python source's own `;` as a stage separator | `20260909T092132Z__g1b_l1_evidence_g1.sh.log` |
| `g1b_l3_evidence_g1_2.sh` (task g1b's, read-only) | **the lane that printed every transcript this log pastes**, each with its own command printed above it by `printf %q`; lane `g1b_l1` unchanged but for that one step, which is now a `grep` over the json itself | `20260909T092546Z__g1b_l3_evidence_g1_2.sh.log` |

Every lane script is kept in the repo at
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_g1/`
(task g1b's at `.../lanes_g1b/`) and was submitted from there.

---

# 1. What the objects are

- **a cell** (recap, task h1) — one (`mnem`, operand shape, `key_width`)
  row of the arch-opcode model table
  (`PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json`,
  tasks m1/m1b), holding, per PLACE the opcode writes, the z3 term the
  reference simulator's own builder puts there.
- **a run** (recap, task h1) — `find_emulation(cell, lang)`: one
  (cell, target) pair carried through render, compile at that corpus's
  own ship flags, carve, and one gate call per written place.
- **the primitive route** (new, task g1) — the question asked BEFORE the
  term is rendered at all: does the target have an operator whose whole
  lowered body IS this cell? Where it has, that operator on holders of
  the operand types the corpus recorded for it is what gets rendered,
  and nothing else.
- **the term route** (recap, tasks h1/h2) — the fallback: the cell's own
  z3 term written in the target's operators by the existing renderer,
  with task h2's two printing fixes still on.
- **a single-opcode row** (task o2's own artifact,
  `PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.json`)
  — a group of corpus units whose body, with task o2's chaff rule
  applied, is exactly ONE instruction. It is the lookup the primitive
  route reads.
- **task o2's two chaff rules** — NARROW drops `ret`, `nop`, `push`,
  `pop` and a pure register-to-register move; WIDE drops those and, in
  addition, a width-changing move or sign extension (`movslq`, `cltd`,
  `cqto` and their like). Task g1's lookup reads the NARROW rows, which
  is what its brief instructed.

---

# 2. What was done and what came back

Task g1 extended the driver with one question in front of the term
route, wrote two new renderers, and ran the same ten cells tasks h1 and
h2 ran against four targets instead of two.

The primitive question was answered for all forty pairs before anything
was rendered. Eight of the forty have an operator in that language's own
corpus whose whole lowered body is the cell; thirty-two do not, and for
those the term route ran unchanged. Where the primitive route ran, what
is compiled is one line of the target's own source — `a + b`, `a * b`,
`a >> b` — rather than the cell's term spelled out in casts and shifts.

Go was the target the brief was aimed at, and go behaved. Every go
place that reached the compile step compiled; `add` and `imul` came back
as one instruction each and were proved equal to the cell for every
input. The shifts did not collapse to one instruction, because go's own
shift carries a `movzbl` of the count beside it and the landing question
counts that as a second instruction — the cell's opcode is still there,
and the gate still proved the body equal to the cell. Table 1 is where
each of those rows is.

Swift did not run at all. `/persist/swift/usr/bin/swiftc`, the path
`lane_gen.py` names and the path the whole swift corpus was built at,
does not exist inside the `g1` instance, so all thirteen swift places
that reached the compile step were refused there with the machine's own
answer. The swift renderer was written and its rendering is on the
record for every one of the ten cells — the `rendered` column of Table 1
holds real swift source — but not one of its seventeen spellings is
measured. §9 is what actually stopped it, which is not what the task was
told to expect.

`idiv` is the cell that motivated the primitive route, and the primitive
route did not reach it. No narrow single-opcode row classifies to `idiv`
`gpr_one` 32 in any of the four languages, because division in every one
of them lowers to the accumulator setup plus the divide — `cltd; idiv`
— which is two instructions under the narrow rule. So `idiv` went by the
term route in all four, its emulation is 51 instructions after the strip
in c and rust and 85 in go, and the gate answered UNDECIDED at 3,000 ms
and again at 300,000 ms on all six of its places. Task g1's own lookup
recorded that under task o2's WIDE rule there IS such a row in c
(`mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret`, unit `c/op_246`)
and recorded it as evidence about the cell rather than taking it as a
second route. That recorded fact is what task g1b's §3 acts on.

---

# 3. The primitive lookup, LITERAL

**LITERAL**, `PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py`,
`primitive_rows` -- the rule that decides whether a single-opcode row
is at a cell:

```python
    for row in (groups.get(rule) or []):
        body = row["body_text"].split("; ")
        stripped = SOU.strip_chaff(body, rule)
        if len(stripped) != 1:
            continue
        line = stripped[0]
        mnem, _operands = SOU.parse_insn(line)
        shape, width, cause = MTAB.classify_line(mnem, line, 0)
```

**LITERAL**, the same file, `primitive_lookup` -- the match itself:

```python
    key = [held["mnem"], held["shape"], held["key_width"]]
    rows = primitive_rows(lang)
    matched = []
    for row in rows:
        if row["cell"] == key:
            matched.append(row)
```

**GLOSS**, beside both: a language's single-opcode row is accepted for a
cell when its body, stripped again by task o2's own narrow rule, is
exactly one instruction, and that instruction classifies — by task m1b's
own `classify_line` and `key_width` — to the same (`mnem`, shape,
`key_width`) triple the cell is. Nothing in the match reads an operator
token. The token is read afterwards, off the chosen row's member, to
reach that member's own probe in the language's manifest, and it appears
in the record as a display label on a unit object (`lang`, `unit`, `n`,
`operator`) and nowhere else.

---

# 3a. The run of record, counted

**LITERAL**, printed by lane `g1b_l3_evidence_g1_2.sh` step [1/9] off
`handful3.json`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py tally3
add gpr_gpr 32               flags      SAME BYTES       c, rust
add gpr_gpr 32               reg_rdi    DIFFERENT BYTES  c, go, rust
addss xmm_xmm 32             reg_xmm0   DIFFERENT BYTES  c, go, rust
cmovne gpr_gpr 32            reg_rdi    DIFFERENT BYTES  c, go, rust
cvtsi2sd gpr_xmm 64          reg_xmm0   DIFFERENT BYTES  c, go, rust
idiv gpr_one 32              reg_rax    DIFFERENT BYTES  c, go, rust
idiv gpr_one 32              reg_rdx    DIFFERENT BYTES  c, go, rust
imul gpr_gpr 32              reg_rdi    DIFFERENT BYTES  c, go, rust
sar cl_gpr 32                reg_rdi    DIFFERENT BYTES  c, go, rust
setne gpr_one 8              reg_rdi    DIFFERENT BYTES  c, go, rust
shr cl_gpr 64                reg_rdi    DIFFERENT BYTES  c, go, rust
sub imm_gpr 64               flags      SAME BYTES       c, rust
sub imm_gpr 64               reg_rdi    DIFFERENT BYTES  c, go, rust
compiled places more than one target has a body for: 13
   every target that compiled it emitted the same bytes: 2
   they emitted different bytes: 11

runs                             40
runs refused before any compile  10
places compiled and carved       37
LANDED                           12
LANDED_ELSEWHERE                 7
NOT_COLLAPSED                    18
PROVED_ON_SHIP                   29
proved under caller extension    2
neither                          6

instructions                                                   434
table cells                                                    229
chaff: ret                                                     30
chaff: calling-convention move                                 156
maps to no table cell                                          19
LANDED runs whose composition is exactly one cell, the target  10
```

**GLOSS**, beside it. Forty runs. Ten were refused before any compile —
the ten swift rows whose place reached the compile step, plus the flags
places their cells also carry. Thirty-seven places compiled and were
carved. Of those, twelve LANDED (the chaff-stripped body is exactly the
cell's own arch opcode), seven LANDED_ELSEWHERE (exactly one instruction,
but a different one), and eighteen did not collapse to one instruction.
Twenty-nine places were PROVED_ON_SHIP outright, two more once each
narrow-holder row is zero-extended to the register, and six were neither
— the six `idiv` places. The composition tally underneath counts the raw
carved instructions: 434 in all, of which 229 are table cells, 186 are
chaff (30 `ret`, 156 calling-convention moves) and 19 map to no table
cell. All ten LANDED runs whose place has a composition have exactly one
cell in it, the target — checked rather than asserted.

---

# 4. The forty runs, one row each

Table 1 — the deliverable's own table, printed off `handful3.json` by
`handful.py report3` and never hand-edited. `route` is `primitive` where
the target has an operator whose whole lowered body IS the cell and
`term` where it has not. `rendered` is a GLOSS (the LITERAL source of
each run sits in that run's own section of `handful3.md`); `composition`
is a GLOSS of the raw carved body; `gate` carries the verdict and where
it holds.

```
$ sed -n \\%\^.\ cell\ .\ lang\ .\ route\ .\ rendered%\,\\%\^\$%p PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3.md
| cell | lang | route | rendered (GLOSS) | landed | composition (GLOSS) | gate (verdict, and where it holds) | cause if refused |
|---|---|---|---|---|---|---|---|
| `add` gpr_gpr 32 | c | term | `((((UINT32_C(0x0)) << 32) \| (((a) + (b)))))` | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `add` gpr_gpr 32 | rust | term | `(((((((0x0u32)) << 32) \| ((((((((a)))).wrapping_add((((b))))))))))))` | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `add` gpr_gpr 32 | go | primitive | `a + b` | LANDED | `add` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `add` gpr_gpr 32 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) \| (UInt64(truncatingIfNeeded: (UInt32(truncatingIf...` |  |  |  | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory |
| `sub` imm_gpr 64 | c | term | `(((a) + (UINT64_C(0xfffffffffffffffd))))` | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sub` imm_gpr 64 | rust | term | `((((((((a)))).wrapping_add(((0xfffffffffffffffdu64)))))))` | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sub` imm_gpr 64 | go | term | `uint64((uint64((uint64(uint64(a))) + (uint64(uint64(0xfffffffffffffffd))))))` | LANDED_ELSEWHERE on `add` | `add` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sub` imm_gpr 64 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(a)))) &+ (UInt64(truncatingIfNeeded: UInt64(0xfffffffffffffffd))))))` |  |  |  | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory |
| `imul` gpr_gpr 32 | c | primitive | `a * b` | LANDED | `imul` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `imul` gpr_gpr 32 | rust | primitive | `a * b` | LANDED | `imul` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `imul` gpr_gpr 32 | go | primitive | `a * b` | LANDED | `imul` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `imul` gpr_gpr 32 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) \| (UInt64(truncatingIfNeeded: (UInt32(truncatingIf...` |  |  |  | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory |
| `sar` cl_gpr 32 | c | primitive | `a >> b` | LANDED | `sar` (+3 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sar` cl_gpr 32 | rust | primitive | `a >> b` | LANDED | `sar` (+3 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sar` cl_gpr 32 | go | term | `uint64((uint64(((uint64(uint32(0x0))) << 32) \| (uint64((uint32(uint32((int32(uint32(a))) >> ((uint32((uint32(((uint32(uint32(0x0))) << 5) \| (uint32(((uint3...` | NOT_COLLAPSED (2) | `movzbl` `sar` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sar` cl_gpr 32 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) \| (UInt64(truncatingIfNeeded: (UInt32(truncatingIf...` |  |  |  | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory |
| `shr` cl_gpr 64 | c | primitive | `a >> b` | LANDED | `shr` (+3 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `shr` cl_gpr 64 | rust | primitive | `a >> b` | LANDED | `shr` (+3 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `shr` cl_gpr 64 | go | term | `uint64((uint64((uint64(uint64(a))) >> ((uint64((uint64(((uint64(uint64(0x0))) << 6) \| (uint64(((uint32((uint32(b)) >> 0)) & uint32(0x3f)))))))) & uint64(0x3...` | NOT_COLLAPSED (2) | `movzbl` `shr` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `shr` cl_gpr 64 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(a)))) &>> (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ...` |  |  |  | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory |
| `idiv` gpr_one 32 | c | term | `((((UINT32_C(0x0)) << 32) \| (((((((((a) << 32) \| (b)))) / (((((((c >> 31) & UINT32_C(0x1))) << 63) \| ((((c >> 31) & UINT32_C(0x1))) << 62) \| ((((c >> 31)...` | NOT_COLLAPSED (51) | `shl` `or` `shr` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `or` `shl` `shl` `or` `s... (+25 chaff) | UNDECIDED, UNDECIDED at 300000 ms -- not decided: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |  |
| `idiv` gpr_one 32 | rust | term | `(((((((0x0u32)) << 32) \| ((((((((({ let n1: i64 = ((((((((((a))) << 32) \| (((b))))))))); let d1: i64 = ((((((((((((((c)) >> 31)) & 0x1u32))) << 63) \| ((((...` | NOT_COLLAPSED (51) | `shl` `or` `shr` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `or` `shl` `shl` `or` `s... (+25 chaff) | UNDECIDED, UNDECIDED at 300000 ms -- not decided: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |  |
| `idiv` gpr_one 32 | go | term | `uint64((uint64(((uint64(uint32(0x0))) << 32) \| (uint64((uint32((uint64((uint64(uint64((int64((uint64(((uint64(uint32(a))) << 32) \| (uint64(uint32(b))))))) ...` | NOT_COLLAPSED (85) | `lea` `cmp` `sub` `shl` `shr` `and` `shl` `shl` `shl` `shl` `shl` `shl` `shl` `shl` `shl` `shl` `shl` `shl` ... -- maps to no cell: `jbe`\* `je`\* `jne`\* `jmp`\* `call`\* `call`\* `jmp`\* (+92 chaff) | UNDECIDED, UNDECIDED at 300000 ms -- not decided: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |  |
| `idiv` gpr_one 32 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) \| (UInt64(truncatingIfNeeded: (UInt32(truncatingIf...` |  |  |  | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory |
| `cmovne` gpr_gpr 32 | c | term | `((((UINT32_C(0x0)) << 32) \| ((((((~((((~(b))) \| ((~(a))))))) == (UINT32_C(0x0)))) ? (d) : (c)))))` | NOT_COLLAPSED (2) | `test` `cmove` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cmovne` gpr_gpr 32 | rust | term | `(((((((0x0u32)) << 32) \| (((if ((((((!((((((((!(((b))))))) \| ((((!(((a))))))))))))))) == ((0x0u32)))) { (((d))) } else { (((c))) })))))))` | NOT_COLLAPSED (2) | `test` `cmove` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cmovne` gpr_gpr 32 | go | term | `uint64((uint64(((uint64(uint32(0x0))) << 32) \| (uint64(sel32(((uint32((uint32(^(uint32((uint32((uint32((uint32(^(uint32(uint32(b))))))) \| (uint32((uint32(^...` | NOT_COLLAPSED (2) | `test` `cmove` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cmovne` gpr_gpr 32 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) \| (UInt64(truncatingIfNeeded: ((((UInt32(truncatin...` |  |  |  | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory |
| `setne` gpr_one 8 | c | term | `((((UINT64_C(0x0)) << 8) \| (((((((~((((((~(a)) & UINT32_C(0xff))) \| (((~(b)) & UINT32_C(0xff)))) & UINT32_C(0xff)))) & UINT32_C(0xff))) == (UINT32_C(0x0)))...` | NOT_COLLAPSED (3) | `xor` `test` `setne` (+1 chaff) | DISPROVED, PROVED_ON_SHIP under caller extension -- holds on every input once each narrow-holder row is zero-extended to the register |  |
| `setne` gpr_one 8 | rust | term | `(((((((0x0u64)) << 8) \| (((if (((((((!((((((((((!(((a))))) & 0xffu32))) \| (((((!(((b))))) & 0xffu32))))) & 0xffu32))))) & 0xffu32))) == ((0x0u32)))) { ((0x...` | NOT_COLLAPSED (3) | `xor` `test` `setne` (+1 chaff) | DISPROVED, PROVED_ON_SHIP under caller extension -- holds on every input once each narrow-holder row is zero-extended to the register |  |
| `setne` gpr_one 8 | go | term | `uint64((uint64(((uint64(uint64(0x0))) << 8) \| (uint64(sel32(((uint32(((uint32(^(uint32(((uint32((uint32(((uint32(^(uint32(uint32(a))))) & uint32(0xff)))) \|...` | NOT_COLLAPSED (13) | `movzbl` `not` `movzbl` `movzbl` `not` `movzbl` `or` `movzbl` `not` `movzbl` `test` `setne` `movzbl` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `setne` gpr_one 8 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt64(0x0))) &<< 8) \| (UInt64(truncatingIfNeeded: ((((UInt32(truncating...` |  |  |  | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory |
| `addss` xmm_xmm 32 | c | term | `bits_to_f32((f32_to_bits(((float)((a) + (b))))))` | LANDED |  -- maps to no cell: `addss`\* (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `addss` xmm_xmm 32 | rust | term | `f32::from_bits((((((a) + (b))).to_bits())))` | LANDED |  -- maps to no cell: `addss`\* (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `addss` xmm_xmm 32 | go | term | `math.Float32frombits(uint32(uint32(math.Float32bits(((a) + (b))))))` | NOT_COLLAPSED (3) | `sub` `add` -- maps to no cell: `addss`\* (+6 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `addss` xmm_xmm 32 | swift | term | `Float(bitPattern: UInt32(truncatingIfNeeded: (UInt32((((a) + (b))).bitPattern))))` |  |  |  | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory |
| `cvtsi2sd` gpr_xmm 64 | c | term | `bits_to_f64((f64_to_bits(((double)(a)))))` | LANDED | `cvtsi2sd` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cvtsi2sd` gpr_xmm 64 | rust | term | `f64::from_bits(((((((((a)))))).to_bits())))` | LANDED | `cvtsi2sd` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cvtsi2sd` gpr_xmm 64 | go | term | `math.Float64frombits(uint64(uint64(math.Float64bits(float64((int64(uint64(a))))))))` | NOT_COLLAPSED (4) | `sub` `cvtsi2sd` `add` -- maps to no cell: `xorps`\* (+7 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cvtsi2sd` gpr_xmm 64 | swift | term | `Double(bitPattern: UInt64(truncatingIfNeeded: (UInt64((Double((Int64(bitPattern: (UInt64(a)))))).bitPattern))))` |  |  |  | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory |
```

---

# 5. c and rust: task h2's verdict beside task g1's

Table 2 — the twenty runs task h2 also ran, so the primitive route's
effect on the two targets that already had a term-route verdict is one
comparison and not two documents. **Four cells moved from the term route
to the primitive route in both c and rust (`imul`, `sar`, `shr`, and
`imul` again in go), and not one verdict changed.** That is the result:
the primitive route reaches the same answer through a body that is one
instruction instead of a term spelled out.

```
$ sed -n \\%\^.\ cell\ .\ lang\ .\ h2\ route%\,\\%\^\$%p PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3.md
| cell | lang | h2 route | h2 verdict | g1 route | g1 verdict |
|---|---|---|---|---|---|
| `add` gpr_gpr 32 | c | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP |
| `add` gpr_gpr 32 | rust | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP |
| `sub` imm_gpr 64 | c | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP |
| `sub` imm_gpr 64 | rust | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP |
| `imul` gpr_gpr 32 | c | term | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP |
| `imul` gpr_gpr 32 | rust | term | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP |
| `sar` cl_gpr 32 | c | term | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP |
| `sar` cl_gpr 32 | rust | term | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP |
| `shr` cl_gpr 64 | c | term | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP |
| `shr` cl_gpr 64 | rust | term | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP |
| `idiv` gpr_one 32 | c | term | UNDECIDED, UNDECIDED at 300000 ms | term | UNDECIDED, UNDECIDED at 300000 ms |
| `idiv` gpr_one 32 | rust | term | UNDECIDED, UNDECIDED at 300000 ms | term | UNDECIDED, UNDECIDED at 300000 ms |
| `cmovne` gpr_gpr 32 | c | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP |
| `cmovne` gpr_gpr 32 | rust | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP |
| `setne` gpr_one 8 | c | term | DISPROVED, PROVED_ON_SHIP under caller extension | term | DISPROVED, PROVED_ON_SHIP under caller extension |
| `setne` gpr_one 8 | rust | term | DISPROVED, PROVED_ON_SHIP under caller extension | term | DISPROVED, PROVED_ON_SHIP under caller extension |
| `addss` xmm_xmm 32 | c | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP |
| `addss` xmm_xmm 32 | rust | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP |
| `cvtsi2sd` gpr_xmm 64 | c | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP |
| `cvtsi2sd` gpr_xmm 64 | rust | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP |
```

---

# 6. Which route ran, and why

Table 3 — the primitive lookup per (cell, target): how many of that
language's single-opcode rows classify to the cell, which row was chosen
and on what ground, and, where none did, the cause the term route ran
instead. The `idiv`/c row is the one that carries the wide-rule
evidence.

```
$ sed -n \\%\^.\ cell\ .\ lang\ .\ route\ .\ single-opcode\ rows%\,\\%\^\$%p PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3.md
| cell | lang | route | single-opcode rows at this cell | chosen row's body, LITERAL | the operator and operand types the manifest records | cause if no primitive |
|---|---|---|---|---|---|---|
| `add` gpr_gpr 32 | c | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `add` gpr_gpr 32 | rust | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `add` gpr_gpr 32 | go | primitive | 1 | `add %ebx,%eax; ret` | `a + b on int32 and int32` (probe go/op_312 of go) |  |
| `add` gpr_gpr 32 | swift | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `sub` imm_gpr 64 | c | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `sub` imm_gpr 64 | rust | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `sub` imm_gpr 64 | go | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `sub` imm_gpr 64 | swift | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `imul` gpr_gpr 32 | c | primitive | 1 | `mov %edi,%eax; imul %esi,%eax; ret` | `a * b on int32_t and int32_t` (probe c/op_174 of c) |  |
| `imul` gpr_gpr 32 | rust | primitive | 1 | `mov %edi,%eax; imul %esi,%eax; ret` | `a * b on i32 and i32` (probe rust/op_606 of rust) |  |
| `imul` gpr_gpr 32 | go | primitive | 1 | `imul %ebx,%eax; ret` | `a * b on int32 and int32` (probe go/op_60 of go) |  |
| `imul` gpr_gpr 32 | swift | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `sar` cl_gpr 32 | c | primitive | 2 | `mov %esi,%ecx; mov %edi,%eax; sar %cl,%eax; ret` | `a >> b on int32_t and int32_t` (probe c/op_714 of c) |  |
| `sar` cl_gpr 32 | rust | primitive | 2 | `mov %rsi,%rcx; mov %edi,%eax; sar %cl,%eax; ret` | `a >> b on i32 and i64` (probe rust/op_499 of rust) |  |
| `sar` cl_gpr 32 | go | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `sar` cl_gpr 32 | swift | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `shr` cl_gpr 64 | c | primitive | 2 | `mov %esi,%ecx; mov %rdi,%rax; shr %cl,%rax; ret` | `a >> b on uint64_t and int32_t` (probe c/op_726 of c) |  |
| `shr` cl_gpr 64 | rust | primitive | 2 | `mov %rsi,%rcx; mov %rdi,%rax; shr %cl,%rax; ret` | `a >> b on u64 and i64` (probe rust/op_511 of rust) |  |
| `shr` cl_gpr 64 | go | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `shr` cl_gpr 64 | swift | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `idiv` gpr_one 32 | c | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell -- though under task o2's WIDE chaff rule there is one, `mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret` (c/op_246), which is evidence about the cell and not a second route |
| `idiv` gpr_one 32 | rust | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `idiv` gpr_one 32 | go | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `idiv` gpr_one 32 | swift | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `cmovne` gpr_gpr 32 | c | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `cmovne` gpr_gpr 32 | rust | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `cmovne` gpr_gpr 32 | go | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `cmovne` gpr_gpr 32 | swift | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `setne` gpr_one 8 | c | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `setne` gpr_one 8 | rust | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `setne` gpr_one 8 | go | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `setne` gpr_one 8 | swift | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `addss` xmm_xmm 32 | c | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `addss` xmm_xmm 32 | rust | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `addss` xmm_xmm 32 | go | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `addss` xmm_xmm 32 | swift | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `cvtsi2sd` gpr_xmm 64 | c | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `cvtsi2sd` gpr_xmm 64 | rust | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `cvtsi2sd` gpr_xmm 64 | go | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `cvtsi2sd` gpr_xmm 64 | swift | term | 0 |  |  | no single-opcode row of this language's own corpus classifies to this cell |
```

The two counts, off `handful3_primitive.json` itself:

```
$ grep -A 2 \"counted\" PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3_primitive.json
  "counted": {
   "primitive": 8,
   "term": 32
```

---

# 7. What did not work, by cause

Task g1's own report groups every place that did not reach a proof by
its cause, which is the protocol's `object.report-by-cause`. Five causes
cover the thirty-three refusals and undecided calls, and twelve cover
the landings that were not LANDED.

## 7.1 Refusals and gate calls that did not prove

```
$ sed -n \\%\^###\ 3.1\ Refusals%\,\\%\^###\ 3.2%p PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3.md
### 3.1 Refusals and gate calls that did not prove

- `a width c has no holder for`: 2 -- sub imm_gpr 64/go [flags], sub imm_gpr 64/swift [flags]
- `the compiler refused`: 13 -- add gpr_gpr 32/swift [reg_rdi], add gpr_gpr 32/swift [flags], sub imm_gpr 64/swift [reg_rdi], imul gpr_gpr 32/swift [reg_rdi], imul gpr_gpr 32/swift [flags], sar cl_gpr 32/swift [reg_rdi], shr cl_gpr 64/swift [reg_rdi], idiv gpr_one 32/swift [reg_rax], idiv gpr_one 32/swift [reg_rdx], cmovne gpr_gpr 32/swift [reg_rdi], setne gpr_one 8/swift [reg_rdi], addss xmm_xmm 32/swift [reg_xmm0], cvtsi2sd gpr_xmm 64/swift [reg_xmm0]
- `the flags place of a preseeded row is the flag state that ARRIVED, not a place this opcode writes`: 8 -- cmovne gpr_gpr 32/c [flags], cmovne gpr_gpr 32/rust [flags], cmovne gpr_gpr 32/go [flags], cmovne gpr_gpr 32/swift [flags], setne gpr_one 8/c [flags], setne gpr_one 8/rust [flags], setne gpr_one 8/go [flags], setne gpr_one 8/swift [flags]
- `the gate answered UNDECIDED at 3,000 ms and again at 300000 ms`: 6 -- idiv gpr_one 32/c [reg_rax], idiv gpr_one 32/c [reg_rdx], idiv gpr_one 32/rust [reg_rax], idiv gpr_one 32/rust [reg_rdx], idiv gpr_one 32/go [reg_rax], idiv gpr_one 32/go [reg_rdx]
- `the primitive route renders the operator's own answer, and the flags place is not a value an operator answers with`: 4 -- add gpr_gpr 32/go [flags], imul gpr_gpr 32/c [flags], imul gpr_gpr 32/rust [flags], imul gpr_gpr 32/go [flags]

### 3.2 The landings that were not LANDED, by cause
```

Read as five causes, with status:

- **the compiler refused (13)** — swift, every place that reached the
  compile step. OPEN; §9, and task g1b's §2 is the re-run.
- **the gate answered UNDECIDED at 3,000 ms and again at 300,000 ms
  (6)** — `idiv`'s six places in c, rust and go. OPEN; the time limit is
  a FLAG and it was re-posed, and the answer did not change.
- **the flags place of a preseeded row is the flag state that ARRIVED
  (8)** — `cmovne` and `setne` in all four targets. Not a defect: these
  two cells consume flags rather than write them, so their `flags` place
  is the arrival. HISTORICAL, the same cause task h1 recorded.
- **the primitive route renders the operator's own answer, and the flags
  place is not a value an operator answers with (4)** — new with this
  route, and correct: an operator hands back one value, so a cell's
  second written place has nothing on the source side to compare.
- **a width c has no holder for (2)** — `sub imm_gpr 64`'s 128-bit flags
  place. HISTORICAL, task h1's own cause.

## 7.2 The landings that were not LANDED, by cause

```
$ sed -n \\%\^###\ 3.2\ The\ landings%\,\\%\^##\ 5%p PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3.md
### 3.2 The landings that were not LANDED, by cause

- the cell's own arch opcode IS among the ones that remain; what sits beside it is what the term carries beyond the operation (2 remain): 2 -- sar cl_gpr 32/go [reg_rdi], shr cl_gpr 64/go [reg_rdi]
- the cell's own arch opcode IS among the ones that remain; what sits beside it is what the term carries beyond the operation (3 remain): 1 -- addss xmm_xmm 32/go [reg_xmm0]
- the cell's own arch opcode IS among the ones that remain; what sits beside it is what the term carries beyond the operation (4 remain): 1 -- cvtsi2sd gpr_xmm 64/go [reg_xmm0]
- the cell's own arch opcode IS among the ones that remain; what sits beside it is what the term carries beyond the operation (51 remain): 4 -- idiv gpr_one 32/c [reg_rax], idiv gpr_one 32/c [reg_rdx], idiv gpr_one 32/rust [reg_rax], idiv gpr_one 32/rust [reg_rdx]
- the cell's own arch opcode IS among the ones that remain; what sits beside it is what the term carries beyond the operation (85 remain): 2 -- idiv gpr_one 32/go [reg_rax], idiv gpr_one 32/go [reg_rdx]
- the compiler chose another arch opcode for the same computation (`add`): 1 -- sub imm_gpr 64/go [reg_rdi]
- the compiler chose another arch opcode for the same computation (`lea`): 4 -- add gpr_gpr 32/c [reg_rdi], add gpr_gpr 32/rust [reg_rdi], sub imm_gpr 64/c [reg_rdi], sub imm_gpr 64/rust [reg_rdi]
- the compiler chose another arch opcode for the same computation (`mov`): 2 -- sub imm_gpr 64/c [flags], sub imm_gpr 64/rust [flags]
- the emulation is a PAIR by construction (the setter's comparison, then the select), so more than one arch opcode was never possible (13 remain): 1 -- setne gpr_one 8/go [reg_rdi]
- the emulation is a PAIR by construction (the setter's comparison, then the select), so more than one arch opcode was never possible (2 remain): 3 -- cmovne gpr_gpr 32/c [reg_rdi], cmovne gpr_gpr 32/rust [reg_rdi], cmovne gpr_gpr 32/go [reg_rdi]
- the emulation is a PAIR by construction (the setter's comparison, then the select), so more than one arch opcode was never possible (3 remain): 2 -- setne gpr_one 8/c [reg_rdi], setne gpr_one 8/rust [reg_rdi]
- the flags place is the reference's flag model -- the two values the setter compared, repacked -- so it is not one operation and no single arch opcode is its landing (2 remain): 2 -- add gpr_gpr 32/c [flags], add gpr_gpr 32/rust [flags]

## 5. Which route ran, and why
```

Read as four causes, with status:

- **the term carries more than the operation (10)** — the cell's own
  arch opcode IS in the carved body; what sits beside it is what the
  term carries. OPEN, and it is the size question, not a correctness
  one: `idiv` is the extreme (51 remaining in c and rust, 85 in go).
- **the compiler chose another arch opcode for the same computation
  (7)** — `lea` for `add` and `sub`, `add` for go's `sub`, `mov` for the
  flags place. Not a defect: LANDED_ELSEWHERE with a PROVED_ON_SHIP
  verdict is the compiler picking a different instruction for the same
  function.
- **the emulation is a PAIR by construction (6)** — `cmovne` and
  `setne`: a comparison then a select, so one arch opcode was never
  possible. HISTORICAL.
- **the flags place is the reference's flag model (2)** — two values
  repacked, so it is not one operation. HISTORICAL.

---

# 8. The two new targets' spelling tables

**LITERAL**, printed by lane `g1_l12_run_of_record2.sh` step [6/6], on
the tower at
`<runs>/g1/agent/logs/20260909T080038Z__g1_l12_run_of_record2.sh.log`:

```
go: 26 spelling rows, 26 measured by a probe of this task
   Z3_OP_BADD, Z3_OP_BSUB, Z3_OP_BMUL                         the plain operator on the unsigned holder
   Z3_OP_BAND, Z3_OP_BOR, Z3_OP_BXOR                          the plain bitwise operator
   Z3_OP_BNEG                                                 unary minus on the unsigned holder
   Z3_OP_BNOT                                                 the caret prefix, go's own complement
   Z3_OP_BSHL, Z3_OP_BLSHR                                    the plain shift with the count MASKED to the width in the source
   Z3_OP_BASHR                                                the value converted to the signed holder, shifted, converted back
   Z3_OP_BUDIV_I, Z3_OP_BUREM_I                               the plain operator on the unsigned holder
   Z3_OP_BSDIV_I, Z3_OP_BSREM_I                               the plain operator on the signed holder
   Z3_OP_ITE                                                  a call to a helper function written into the same file
   Z3_OP_EQ, Z3_OP_DISTINCT                                   the plain comparison, through the conditional helper
   Z3_OP_SLEQ .. Z3_OP_UGT                                    the plain comparison on the converted holder
   Z3_OP_EXTRACT, Z3_OP_CONCAT                                the explicit conversion, and a shift joined by an or
   Z3_OP_ZERO_EXT                                             the explicit conversion to the wider holder
   Z3_OP_SIGN_EXT                                             the conversion through the signed holder
   Z3_OP_FPA_TO_IEEE_BV (a bare float arrival)                the pointer cast
   Z3_OP_FPA_TO_IEEE_BV (mid-expression or at the answer)     the standard library's own function
   Z3_OP_FPA_TO_FP (bits reinterpreted)                       the standard library's own function
   Z3_OP_FPA_TO_FP (value converted)                          the explicit conversion to the float holder
   Z3_OP_FPA_TO_FP_UNSIGNED                                   the explicit conversion from the unsigned holder
   Z3_OP_FPA_TO_SBV, Z3_OP_FPA_TO_UBV                         the explicit conversion to the integer holder
   Z3_OP_FPA_ADD, Z3_OP_FPA_SUB, Z3_OP_FPA_MUL, Z3_OP_FPA_DIV the plain operator on the float holder
   Z3_OP_FPA_ABS                                              the sign bit cleared through the bit casts
   the holders                                                uint8..uint64, int8..int64, float32, float64
   the arrival registers                                      rax, rbx, rcx, rdi, rsi, r8 ... and xmm0 upwards
   the narrow arrival                                         no assumption about the caller
   the prologue                                               none

swift: 17 spelling rows, 0 measured by a probe of this task
```

**GLOSS**, beside it: go has 26 spelling rows and every one of them was
measured by a probe this task compiled and read back, which is task o11
§3.1's rule. Swift has 17 rows and NONE of them was measured, because no
swift compiler was reachable; each row says so in
`handful3_spellings.json` itself. The table is keyed by z3 declaration
kind — machine form — and never by a language operator token.

---

# 9. Swift: what actually stopped it, which is not what was expected

The task was told to expect a loader failure — `swiftc` present but
unable to load `libncurses.so.6`. That is not what the machine said.

**LITERAL**, printed by lane `g1_l1_toolchains.sh` step [4/5], on the
tower at
`<runs>/g1/agent/logs/20260909T065344Z__g1_l1_toolchains.sh.log`:

```
[4/5] task g1: swiftc at the path lane_gen.py names
/drop/g1_l1_toolchains.sh: line 28: /persist/swift/usr/bin/swiftc: No such file or directory
```

**LITERAL**, printed by lane `g1_l2_swift_where.sh` steps [1/6] to
[4/6], same folder, `20260909T065422Z__g1_l2_swift_where.sh.log`:

```
[1/6] task g1: /persist as this instance sees it
total 8
drwxr-xr-x 2 root root 4096 Sep  9 06:52 .
dr-xr-xr-x 1 root root 4096 Sep  9 06:52 ..
[2/6] task g1: swiftc on PATH
  (not on PATH)
[3/6] task g1: any file named swiftc on the image's own filesystem
[4/6] task g1: any directory named swift near the usual roots
ls: cannot access '/usr/lib/swift': No such file or directory
ls: cannot access '/usr/share/swift': No such file or directory
ls: cannot access '/opt/swift': No such file or directory
ls: cannot access '/usr/local/swift': No such file or directory
```

**GLOSS**, beside both: inside the `g1` instance `/persist` is an EMPTY
directory. There is no `swiftc` at the path `lane_gen.py` names, none on
PATH, and no file of that name anywhere on the image. The refusal
recorded against all thirteen swift places is therefore a missing FILE,
and its literal text — the one Table 1 carries — is:

```
the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory
```

Task g1 obeyed its brief and attempted no workaround: no
`LD_LIBRARY_PATH`, no copied library, no second path. The cause of the
empty `/persist` is a configuration fact task g1b located and states in
its own log; it is named here only so this record is not read as a
loader failure.

---

# 10. Memory

The bound stated in `g1.conf` and in every lane header is 4 GB resident
on the one collecting process, named abort `ABORT_MEMORY_G1`, checked
after every run. The run of record's own peaks, printed by the program
after each step: 82,744 kB through the primitive lookup, 466,868 kB
through the forty runs, 439,916 kB through the six re-posed gate calls,
257,372 kB through the composition step, 64,176 kB through the spelling
tables. The high-water mark, 466,868 kB, is 11% of the bound. No abort
fired.

---

# 11. The guard, unmodified

The spelling-key check was run over every json task g1's own programs
write, plus `go_facts.json`, and `grep -c exempt` over every file task
g1 added or changed.

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3.json PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3_primitive.json PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3_spellings.json PseudoCoupHQ/Research/oracle/cross_construction/emulation/go/go_facts.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS handful3.json -- no operator token in any key, grouping, pairing or row structure
PASS handful3_primitive.json -- no operator token in any key, grouping, pairing or row structure
PASS handful3_spellings.json -- no operator token in any key, grouping, pairing or row structure
PASS go_facts.json -- no operator token in any key, grouping, pairing or row structure
```

```
$ grep -c exempt PseudoCoupHQ/Research/oracle/cross_construction/emulation/go/go_facts.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/go/go_render.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/swift/swift_render.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3.md
PseudoCoupHQ/Research/oracle/cross_construction/emulation/go/go_facts.py:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/go/go_render.py:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/swift/swift_render.py:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3.md:0
```

`grep -c` exits 1 when a count it prints is zero, which is why the lane
carries `|| true` on that step; the counts themselves are the answer,
and every one is 0.

---

# 12. The two lists

## Decided, recorded for audit

1. **The primitive route reads task o2's NARROW rows**, which is task
   g1's brief's own instruction, and records what the WIDE rule would
   have found as EVIDENCE about the cell rather than taking it as a
   second route. Eight of forty pairs have a primitive; thirty-two do
   not (§6).
2. **The lookup key is machine form.** A row is matched to a cell by the
   (`mnem`, shape, `key_width`) triple its one instruction classifies
   to, by task m1b's own classifier. No operator token participates in
   the match; the token is read afterwards, off the chosen member, as a
   display label on a unit object (§3). The unmodified guard passes on
   all four json (§11).
3. **What the primitive route renders is the corpus's own program.** The
   chosen member's probe SOURCE, with its symbol renamed and nothing
   else changed — so what the compiler is handed here is what it was
   handed when the corpus was built (`render_primitive`).
4. **The primitive route does not answer a `flags` place**, and says so
   by its own cause word rather than by silence: an operator hands back
   one value (§7.1).
5. **The UNDECIDED verdict on `idiv` was re-posed at 300,000 ms**, a
   hundred times the pipeline's own ceiling, on all six places, and did
   not change. The verdict OF RECORD stays the one the 3,000 ms ceiling
   gave.
6. **The run of record is lane `g1_l12_run_of_record2.sh`**, and lane
   `g1_l9_run_of_record.sh` — an earlier end-to-end run of the same
   forty under the same program but for one record-shape change — agrees
   with it row for row on every count in §4 and §7.
7. **Swift produced no measurement.** Its renderer is written and its
   rendering is on the record; all seventeen of its spellings are marked
   UNMEASURED in `handful3_spellings.json`, and no workaround was
   attempted (§9).

## Awaiting the owner

1. **`idiv`'s emulation is 51 instructions in c and rust and 85 in go,
   and the gate cannot answer it.** The 32-copy sign extension is in the
   TABLE'S OWN TERM — this is the same flag task h2 raised (log 240) and
   it belongs to tasks m1/m1b, not to this driver. Task g1b's §3 widens
   the primitive lookup so that division can take the primitive route
   instead; if it does, this flag is answered by route rather than by
   term size.
