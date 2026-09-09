# log 242 — task g1b: swift on the rebuilt image, and the primitive lookup widened by one step

Node: `hq.research.arch_unit_oracle`
(`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`,
the "goal" section of 2026-09-07 and the ruling of 2026-09-08). The
PROGRESS entry is on the autopoly sub-node
(`.../node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/PROGRESS.md`),
beside tasks o12, o13, h1, h1b, h2 and g1.

Date: 2026-09-09. Instance `g1`, on the TOWER, brought down at the end
of this log. Artifact folder (the same one tasks h1, h1b, h2 and g1
wrote):
[`~/Programming/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/`](file://~/Programming/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/).

**WHAT THIS TASK IS.** Task g1b is the closer for task g1. Its first
job was to bank task g1's own record from what task g1 left on disk,
and that is
[`log_241`](file://~/Programming/PseudoCoupHQ/DevComms/log_241_task_g1_find_emulation_go_and_swift.md),
a separate log. This one carries task g1b's own two pieces of work: the
same forty runs re-run on a machine where a swift compiler exists, and
the primitive lookup widened by one step so that a divide can take the
primitive route.

The deliverables:

- [`handful/handful3b.json`](file://~/Programming/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3b.json)
  and
  [`handful/handful3b.md`](file://~/Programming/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3b.md)
  — the second run of record: the same forty runs, on the rebuilt image.
- [`handful/handful3c.json`](file://~/Programming/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3c.json)
  and
  [`handful/handful3c.md`](file://~/Programming/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3c.md)
  — the widened lookup, and the ONE run it changes.
- [`handful/handful.py`](file://~/Programming/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py)
  extended with section 2e (the widened rule) and the `*3b` / `*3c`
  commands, and with one defect fixed in `one_recheck` (§8).
- `~/Programming/Airlock/instances/g1.conf` — one change, stated with
  its reason in the file: the instance now mounts `sandbox-persist`
  READ-ONLY (§3). Airlock's own `.gitignore` line 35 excludes
  `instances/*.conf` as per-machine configuration, so this one lives on
  disk here and in the copy `remote_lane.sh conf` put on the tower, not
  in git; its reason is written into its header rather than into a
  commit message.

**Task g1's own `handful3.json` / `handful3.md` /
`handful3_primitive.json` / `handful3_spellings.json` were not written
by any lane of this task**; the new products sit beside them, and the
rendered sources are under `src3b/` and `src3c/` beside `src3/`.

Every rendering here is labelled per the protocol's
`object.literal-gloss-analogy`: **LITERAL** is the object itself,
quoted; **GLOSS** is a plain-words reading beside a literal. No gloss
appears without its literal.

Paths inside a pasted command are the ones the lane sees:
`/projects/PseudoCoupHQ` IS `~/Programming/PseudoCoupHQ`, mounted into
the instance. Prose names host paths. **The lane logs are on the
TOWER** (`<tower-user>@<host>`), under
`~/AirlockRuns/g1/agent/logs/`, and every attribution
below names one of them.

| lane | what it did | log, on the tower |
|---|---|---|
| `g1b_l1_evidence_g1.sh`, `g1b_l3_evidence_g1_2.sh` | task g1's own record, printed off the files task g1 left; log 241 | `...092132Z`, `...092546Z` |
| `g1b_l2_verify_241.sh`, `g1b_l4_verify_241_2.sh` | the conventions verifier over log 241; the second pass is 9 MATCHES, 0 DIFFERS, 0 REFUSED, 0 NOT_RERUNNABLE | `...092305Z`, `...092735Z` |
| `g1b_l5_swift_probe.sh` | after `down` then `up`: `/persist` as the container now sees it, `swiftc --version`, `ldd` over the driver, and one swift source through it at the corpus's own ship flags | `20260909T092938Z__g1b_l5_swift_probe.sh.log` |
| `g1b_l6_changes.sh` | the widened lookup's changed set, before anything was run | `20260909T093428Z__g1b_l6_changes.sh.log` |
| `g1b_l7_whynot.sh` | why the widened rule reaches the divide cell in c and in no other target | `20260909T093602Z__g1b_l7_whynot.sh.log` |
| `g1b_l8_run_of_record_b.sh` | **THE SECOND RUN OF RECORD**: the forty runs on the rebuilt image, the eight UNDECIDED gate calls re-posed at 300,000 ms, the composition column, the report and the spelling tables — one lane. 1,861.2 s, exit 0 | `20260909T093701Z__g1b_l8_run_of_record_b.sh.log` |
| `g1b_l9_bodies.sh` | what each target's own corpus holds at the divide's arch mnemonic | `20260909T100834Z__g1b_l9_bodies.sh.log` |
| `g1b_l10_run_of_record_c.sh` | the widened lookup's first run; its re-pose returned DISPROVED off a rebuilt parameter plan, which §8 is | `20260909T101000Z__g1b_l10_run_of_record_c.sh.log` |
| `g1b_l11_run_of_record_c2.sh` | **THE WIDENED LOOKUP'S RUN OF RECORD**, after the parameter-plan fix | `20260909T101144Z__g1b_l11_run_of_record_c2.sh.log` |
| `g1b_l12_evidence.sh` | the first pass of the transcripts below; its recheck audit asked whether a place records a parameter plan, which is not the question that decides anything, so §8's measurement is a later lane's | `20260909T101304Z__g1b_l12_evidence.sh.log` |
| `g1b_l13_evidence2.sh` | the second pass, with §8's measurement corrected; two of its transcripts end in the program's own `peak resident` line, which varies by a few kB between runs, so the conventions verifier scored them DIFFERS | `20260909T101437Z__g1b_l13_evidence2.sh.log` |
| `g1b_l14_verify_242.sh` | the conventions verifier over a first draft of this log: 11 MATCHES, 0 REFUSED on the transcripts that stayed, but 2 DIFFERS, both the varying memory line | `20260909T101759Z__g1b_l14_verify_242.sh.log` |
| `g1b_l15_evidence3.sh` | **the lane that printed every transcript this log pastes**, each with its own command printed above it; the two commands whose output carries the varying memory line now print it out of the transcript with `grep -v`, and the number itself is in §9 | `20260909T101905Z__g1b_l15_evidence3.sh.log` |
| `g1b_l16_verify_242_2.sh` | the verifier again, over this log as it stands: 13 MATCHES, 0 DIFFERS | `20260909T102006Z__g1b_l16_verify_242_2.sh.log` |

Every lane script is kept in the repo at
`~/Programming/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_g1b/`
and was submitted from there.

---

# 1. What the objects are

The first four are recaps; the last four are this task's own.

- **a cell** (recap, task h1) — one (`mnem`, operand shape, `key_width`)
  row of the arch-opcode model table, holding, per PLACE the opcode
  writes, the z3 term the reference simulator's own builder puts there.
- **a run** (recap, task h1) — one (cell, target) pair carried through
  render, compile at that corpus's own ship flags, carve, and one gate
  call per written place.
- **the primitive route** (recap, task g1) — the question asked before
  the term is rendered: does the target have an operator whose whole
  lowered body IS this cell? Task g1's rule accepted a row whose
  chaff-stripped body is exactly ONE instruction classifying to the
  cell.
- **a single-opcode row** (recap, task o2) — a group of corpus units
  whose body, with task o2's chaff rule applied, is exactly one
  instruction. Task o2 keeps two lists, one per chaff rule: NARROW
  drops `ret`, `nop`, `push`, `pop` and pure register-to-register moves;
  WIDE drops those plus width-changing moves and sign extensions
  (`movslq`, `cltd`, `cqto` and their like).
- **a zero-operand setup instruction** (this task) — a line with NO
  OPERAND AT ALL whose mnemonic is a key of `reference.SPREAD_SIGN`
  (`cltd`, `cqto`, `cqo`, `cwtd`) or of `reference.ACCUMULATOR_WIDEN`
  (`cltq`, `cwtl` and their like). Those two tables are the reference
  simulator's own, and they are the same two task h2's zero-operand
  width rule reads, so such a line classifies to a model-table cell like
  any other instruction.
- **the widened lookup** (this task) — the primitive rule with one step
  added: a row is accepted when its NARROW-stripped body is the cell's
  own instruction PLUS zero or more zero-operand setup instructions, and
  nothing else. §7 holds it, LITERAL.
- **`primitive+setup`** (this task) — the route name recorded when the
  accepted row carries setup. A row that carries none is still
  `primitive`, which is task g1's own answer unchanged.
- **a parameter plan** (recap, task o7, and §8's subject) — the list of
  declared parameters of a rendered function, each with its holder and
  its width. It is the ARRIVAL CONTRACT: `check_one_place` turns it into
  the register list the body reads (`expected_families(lang, params)`)
  and aligns that against the cell's own families, IN row by IN row.

---

# 2. What was done and what came back

Task g1 could not compile a single line of swift, and the reason turned
out to be two independent obstacles rather than the one the task was
told about. The first is the one the coordinator fixed: the old image
carried `libncursesw.so.6` and not `libncurses.so.6`, which the swift
driver loads. The second was in the instance's own configuration and
task g1 measured it without naming it: `g1.conf` declared no persist
volume, and Airlock has no "no volume" state, so the container got a
fresh EMPTY volume of its own at `/persist` — while the swift toolchain
lives at `/persist/swift` on the DEFAULT instance's volume. With the
container re-created on the rebuilt image and `sandbox-persist` mounted
read-only, `swiftc --version` answers and a probe compiles.

The forty runs were then run again, unchanged in every other respect.
All forty reach a compiled body where task g1 got thirty; every one of
the thirty non-swift rows returns exactly what task g1 got for it, which
is the check that the machine and not the method changed. Eight of
swift's ten cells are proved equal to the cell's term for every input,
a ninth once its narrow holder is zero-extended, and the tenth is the
divide, which no target decides.

The lookup was then widened by one step, and the honest result is
smaller than the brief expected. It changes ONE of the forty pairs, not
three: the divide in c. In rust, go and swift it changes nothing, and
the reason is not the rule — it is that those languages' corpora hold no
single-opcode row carrying the divide instruction at all, because their
divide bodies carry a GUARD. c's divide body is four instructions and no
guard; rust's shortest is seventeen and ends in two calls into
`core::panicking`; go's carries a branch into `runtime.panicdivide`;
swift's carries two `ud2` traps. That is the owner's own model of an opcode —
a primitive plus its edge regions — showing up as the reason the
primitive route reaches one target and not the others.

On c the widened rule does exactly what it was meant to. The route
becomes `primitive+setup`, the rendered source is one line, and the
compiled body is the cell's own opcode with its accumulator setup beside
it — five instructions where the term route produced seventy-six. The
gate still cannot answer, and this time the reason is not the solver's
clock: the emulation reads TWO inputs where the cell reads THREE,
because the third is the one `cltd` derives from the first. §7.4 is
that, and it is the sharpest statement of the edge-region question this
line has produced.

One defect was found and fixed on the way, and §8 is it: the re-pose
step rebuilt the term-route parameter plan even for a primitive-route
place, which aligned the wrong rows and produced a counterexample about
a comparison nobody posed.

---

# 3. Swift: the two obstacles, and the compiler that answered

Task g1's refusal text, which log 241 §9 carries in full, was
`/persist/swift/usr/bin/swiftc: No such file or directory` — a missing
FILE. Its lane `g1_l2_swift_where.sh` also measured that `/persist`
inside the `g1` container held two entries and nothing else.

**LITERAL**, `~/Programming/Airlock/instance.sh` lines 174-176, which is
where the empty volume comes from:

```
    AL_PERSIST="$(_airlock_pick "$(_airlock_conf_get "$AL_CONF" persist_volume)" "$AL_INSTANCE-persist")"
    AL_PERSIST_MODE="$(_airlock_pick "$(_airlock_conf_get "$AL_CONF" persist_mode)" "rw")"
    [ "$AL_PERSIST_MODE" = "ro" ] || AL_PERSIST_MODE="rw"
```

**GLOSS**, beside it: `persist_volume` is not optional. Naming none
means `<instance>-persist`, which podman creates empty on first use.
`g1.conf` said "WHY NO PERSIST VOLUME" and therefore got `g1-persist`,
an empty volume, mounted over the very path the swift toolchain lives
at on `sandbox-persist`. Two other instance configurations already
mount that volume read-only for the same toolchain — `t101b.conf` ("swift
lives at /persist/swift on the default instance's toolchain") and
`t103.conf` — so `g1.conf` now does the same, with the reason written
into its header.

The container was then re-created (`remote_lane.sh down --instance g1`,
then `up --instance g1`), which is what makes an instance pick up the
rebuilt image. Lane `g1b_l5_swift_probe.sh` asked the questions that
separate the two obstacles. **LITERAL**, printed by that lane, steps
[2/6] to [4/6], on the tower at
`~/AirlockRuns/g1/agent/logs/20260909T092938Z__g1b_l5_swift_probe.sh.log`:

```
$ ls -la /persist/swift/usr/bin/swiftc
lrwxrwxrwx 1 root root 12 Dec 11  2024 /persist/swift/usr/bin/swiftc -> swift-driver
[3/6] task g1b: is libncurses.so.6 present in the image now

$ ls -la /usr/lib/x86_64-linux-gnu/libncurses.so.6
lrwxrwxrwx 1 root root 17 Jan  3  2026 /usr/lib/x86_64-linux-gnu/libncurses.so.6 -> libncurses.so.6.6
[4/6] task g1b: swiftc --version, LITERAL

$ /persist/swift/usr/bin/swiftc --version
Swift version 6.0.3 (swift-6.0.3-RELEASE)
Target: x86_64-unknown-linux-gnu
```

This block is an ATTRIBUTION and not a re-runnable transcript on
purpose: `/persist/swift/usr/bin/swiftc` is an absolute path to a
compiler and not a program on the conventions verifier's read-only
allowlist, so a pasted `$` line naming it is REFUSED rather than run.
The lane log named above is where the machine answered.

**GLOSS**: a swift compiler exists at the path the whole swift corpus
was built at, and it answers. Both obstacles had to go: the same lane's
`ldd` step shows the driver resolving `libncurses.so.6` out of
`/usr/lib/x86_64-linux-gnu/`, which the old image did not carry, and
its last step compiles a probe at the corpus's own `-O` and produces an
object file. No workaround was used anywhere in this task: no
`LD_LIBRARY_PATH`, no copied library, no second path.

---

# 4. The forty runs on the rebuilt image

Table 1 — the second run of record, printed off `handful3b.json` by
`handful.py report3b` and never hand-edited. The columns are task g1's
own; `route` is `primitive` where the target has an operator whose whole
lowered body IS the cell and `term` where it has not; `rendered` and
`composition` are GLOSSES whose LITERALs sit in each run's own section
of `handful3b.md`.

```
$ sed -n \\%\^.\ cell\ .\ lang\ .\ route\ .\ rendered%\,\\%\^\$%p /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3b.md
| cell | lang | route | rendered (GLOSS) | landed | composition (GLOSS) | gate (verdict, and where it holds) | cause if refused |
|---|---|---|---|---|---|---|---|
| `add` gpr_gpr 32 | c | term | `((((UINT32_C(0x0)) << 32) \| (((a) + (b)))))` | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `add` gpr_gpr 32 | rust | term | `(((((((0x0u32)) << 32) \| ((((((((a)))).wrapping_add((((b))))))))))))` | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `add` gpr_gpr 32 | go | primitive | `a + b` | LANDED | `add` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `add` gpr_gpr 32 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) \| (UInt64(truncatingIfNeeded: (UInt32(truncatingIf...` | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sub` imm_gpr 64 | c | term | `(((a) + (UINT64_C(0xfffffffffffffffd))))` | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sub` imm_gpr 64 | rust | term | `((((((((a)))).wrapping_add(((0xfffffffffffffffdu64)))))))` | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sub` imm_gpr 64 | go | term | `uint64((uint64((uint64(uint64(a))) + (uint64(uint64(0xfffffffffffffffd))))))` | LANDED_ELSEWHERE on `add` | `add` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sub` imm_gpr 64 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(a)))) &+ (UInt64(truncatingIfNeeded: UInt64(0xfffffffffffffffd))))))` | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `imul` gpr_gpr 32 | c | primitive | `a * b` | LANDED | `imul` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `imul` gpr_gpr 32 | rust | primitive | `a * b` | LANDED | `imul` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `imul` gpr_gpr 32 | go | primitive | `a * b` | LANDED | `imul` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `imul` gpr_gpr 32 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) \| (UInt64(truncatingIfNeeded: (UInt32(truncatingIf...` | LANDED | `imul` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sar` cl_gpr 32 | c | primitive | `a >> b` | LANDED | `sar` (+3 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sar` cl_gpr 32 | rust | primitive | `a >> b` | LANDED | `sar` (+3 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sar` cl_gpr 32 | go | term | `uint64((uint64(((uint64(uint32(0x0))) << 32) \| (uint64((uint32(uint32((int32(uint32(a))) >> ((uint32((uint32(((uint32(uint32(0x0))) << 5) \| (uint32(((uint3...` | NOT_COLLAPSED (2) | `movzbl` `sar` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sar` cl_gpr 32 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) \| (UInt64(truncatingIfNeeded: (UInt32(truncatingIf...` | LANDED | `sar` (+3 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `shr` cl_gpr 64 | c | primitive | `a >> b` | LANDED | `shr` (+3 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `shr` cl_gpr 64 | rust | primitive | `a >> b` | LANDED | `shr` (+3 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `shr` cl_gpr 64 | go | term | `uint64((uint64((uint64(uint64(a))) >> ((uint64((uint64(((uint64(uint64(0x0))) << 6) \| (uint64(((uint32((uint32(b)) >> 0)) & uint32(0x3f)))))))) & uint64(0x3...` | NOT_COLLAPSED (2) | `movzbl` `shr` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `shr` cl_gpr 64 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(a)))) &>> (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ...` | LANDED | `shr` (+3 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `idiv` gpr_one 32 | c | term | `((((UINT32_C(0x0)) << 32) \| (((((((((a) << 32) \| (b)))) / (((((((c >> 31) & UINT32_C(0x1))) << 63) \| ((((c >> 31) & UINT32_C(0x1))) << 62) \| ((((c >> 31)...` | NOT_COLLAPSED (51) | `shl` `or` `shr` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `or` `shl` `shl` `or` `s... (+25 chaff) | UNDECIDED, UNDECIDED at 300000 ms -- not decided: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |  |
| `idiv` gpr_one 32 | rust | term | `(((((((0x0u32)) << 32) \| ((((((((({ let n1: i64 = ((((((((((a))) << 32) \| (((b))))))))); let d1: i64 = ((((((((((((((c)) >> 31)) & 0x1u32))) << 63) \| ((((...` | NOT_COLLAPSED (51) | `shl` `or` `shr` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `or` `shl` `shl` `or` `s... (+25 chaff) | UNDECIDED, UNDECIDED at 300000 ms -- not decided: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |  |
| `idiv` gpr_one 32 | go | term | `uint64((uint64(((uint64(uint32(0x0))) << 32) \| (uint64((uint32((uint64((uint64(uint64((int64((uint64(((uint64(uint32(a))) << 32) \| (uint64(uint32(b))))))) ...` | NOT_COLLAPSED (85) | `lea` `cmp` `sub` `shl` `shr` `and` `shl` `shl` `shl` `shl` `shl` `shl` `shl` `shl` `shl` `shl` `shl` `shl` ... -- maps to no cell: `jbe`\* `je`\* `jne`\* `jmp`\* `call`\* `call`\* `jmp`\* (+92 chaff) | UNDECIDED, UNDECIDED at 300000 ms -- not decided: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |  |
| `idiv` gpr_one 32 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) \| (UInt64(truncatingIfNeeded: (UInt32(truncatingIf...` | LANDED_ELSEWHERE on `jmp` |  -- maps to no cell: `jmp`\* | UNDECIDED, UNDECIDED at 300000 ms -- not decided: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |  |
| `cmovne` gpr_gpr 32 | c | term | `((((UINT32_C(0x0)) << 32) \| ((((((~((((~(b))) \| ((~(a))))))) == (UINT32_C(0x0)))) ? (d) : (c)))))` | NOT_COLLAPSED (2) | `test` `cmove` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cmovne` gpr_gpr 32 | rust | term | `(((((((0x0u32)) << 32) \| (((if ((((((!((((((((!(((b))))))) \| ((((!(((a))))))))))))))) == ((0x0u32)))) { (((d))) } else { (((c))) })))))))` | NOT_COLLAPSED (2) | `test` `cmove` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cmovne` gpr_gpr 32 | go | term | `uint64((uint64(((uint64(uint32(0x0))) << 32) \| (uint64(sel32(((uint32((uint32(^(uint32((uint32((uint32((uint32(^(uint32(uint32(b))))))) \| (uint32((uint32(^...` | NOT_COLLAPSED (2) | `test` `cmove` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cmovne` gpr_gpr 32 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) \| (UInt64(truncatingIfNeeded: ((((UInt32(truncatin...` | NOT_COLLAPSED (2) | `test` `cmove` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `setne` gpr_one 8 | c | term | `((((UINT64_C(0x0)) << 8) \| (((((((~((((((~(a)) & UINT32_C(0xff))) \| (((~(b)) & UINT32_C(0xff)))) & UINT32_C(0xff)))) & UINT32_C(0xff))) == (UINT32_C(0x0)))...` | NOT_COLLAPSED (3) | `xor` `test` `setne` (+1 chaff) | DISPROVED, PROVED_ON_SHIP under caller extension -- holds on every input once each narrow-holder row is zero-extended to the register |  |
| `setne` gpr_one 8 | rust | term | `(((((((0x0u64)) << 8) \| (((if (((((((!((((((((((!(((a))))) & 0xffu32))) \| (((((!(((b))))) & 0xffu32))))) & 0xffu32))))) & 0xffu32))) == ((0x0u32)))) { ((0x...` | NOT_COLLAPSED (3) | `xor` `test` `setne` (+1 chaff) | DISPROVED, PROVED_ON_SHIP under caller extension -- holds on every input once each narrow-holder row is zero-extended to the register |  |
| `setne` gpr_one 8 | go | term | `uint64((uint64(((uint64(uint64(0x0))) << 8) \| (uint64(sel32(((uint32(((uint32(^(uint32(((uint32((uint32(((uint32(^(uint32(uint32(a))))) & uint32(0xff)))) \|...` | NOT_COLLAPSED (13) | `movzbl` `not` `movzbl` `movzbl` `not` `movzbl` `or` `movzbl` `not` `movzbl` `test` `setne` `movzbl` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `setne` gpr_one 8 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt64(0x0))) &<< 8) \| (UInt64(truncatingIfNeeded: ((((UInt32(truncating...` | NOT_COLLAPSED (3) | `xor` `test` `setne` (+1 chaff) | DISPROVED, PROVED_ON_SHIP under caller extension -- holds on every input once each narrow-holder row is zero-extended to the register |  |
| `addss` xmm_xmm 32 | c | term | `bits_to_f32((f32_to_bits(((float)((b) + (a))))))` | LANDED |  -- maps to no cell: `addss`\* (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `addss` xmm_xmm 32 | rust | term | `f32::from_bits((((((b) + (a))).to_bits())))` | LANDED |  -- maps to no cell: `addss`\* (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `addss` xmm_xmm 32 | go | term | `math.Float32frombits(uint32(uint32(math.Float32bits(((b) + (a))))))` | NOT_COLLAPSED (3) | `sub` `add` -- maps to no cell: `addss`\* (+6 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `addss` xmm_xmm 32 | swift | term | `Float(bitPattern: UInt32(truncatingIfNeeded: (UInt32((((b) + (a))).bitPattern))))` | LANDED |  -- maps to no cell: `addss`\* (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cvtsi2sd` gpr_xmm 64 | c | term | `bits_to_f64((f64_to_bits(((double)(a)))))` | LANDED | `cvtsi2sd` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cvtsi2sd` gpr_xmm 64 | rust | term | `f64::from_bits(((((((((a)))))).to_bits())))` | LANDED | `cvtsi2sd` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cvtsi2sd` gpr_xmm 64 | go | term | `math.Float64frombits(uint64(uint64(math.Float64bits(float64((int64(uint64(a))))))))` | NOT_COLLAPSED (4) | `sub` `cvtsi2sd` `add` -- maps to no cell: `xorps`\* (+7 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cvtsi2sd` gpr_xmm 64 | swift | term | `Double(bitPattern: UInt64(truncatingIfNeeded: (UInt64((Double((Int64(bitPattern: (UInt64(a)))))).bitPattern))))` | LANDED | `cvtsi2sd` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
```

---

# 5. Every pair, task g1's answer beside this one

Table 2 — one row per (cell, target), with task g1's own verdict from
`handful3.json` beside this run's. **Ten rows moved and thirty did not**,
and both halves are the result: the ten are exactly the swift rows, and
the thirty are the check that re-creating the container changed the
machine and not the method.

```
$ sed -n \\%\^.\ cell\ .\ lang\ .\ g1\ route%\,\\%\^\$%p /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3b.md
| cell | lang | g1 route | g1 verdict | this route | this verdict | moved |
|---|---|---|---|---|---|---|
| `add` gpr_gpr 32 | c | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `add` gpr_gpr 32 | rust | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `add` gpr_gpr 32 | go | primitive | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP | no |
| `add` gpr_gpr 32 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | PROVED_ON_SHIP | **yes** |
| `sub` imm_gpr 64 | c | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `sub` imm_gpr 64 | rust | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `sub` imm_gpr 64 | go | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `sub` imm_gpr 64 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | PROVED_ON_SHIP | **yes** |
| `imul` gpr_gpr 32 | c | primitive | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP | no |
| `imul` gpr_gpr 32 | rust | primitive | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP | no |
| `imul` gpr_gpr 32 | go | primitive | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP | no |
| `imul` gpr_gpr 32 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | PROVED_ON_SHIP | **yes** |
| `sar` cl_gpr 32 | c | primitive | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP | no |
| `sar` cl_gpr 32 | rust | primitive | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP | no |
| `sar` cl_gpr 32 | go | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `sar` cl_gpr 32 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | PROVED_ON_SHIP | **yes** |
| `shr` cl_gpr 64 | c | primitive | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP | no |
| `shr` cl_gpr 64 | rust | primitive | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP | no |
| `shr` cl_gpr 64 | go | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `shr` cl_gpr 64 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | PROVED_ON_SHIP | **yes** |
| `idiv` gpr_one 32 | c | term | UNDECIDED, UNDECIDED at 300000 ms | term | UNDECIDED, UNDECIDED at 300000 ms | no |
| `idiv` gpr_one 32 | rust | term | UNDECIDED, UNDECIDED at 300000 ms | term | UNDECIDED, UNDECIDED at 300000 ms | no |
| `idiv` gpr_one 32 | go | term | UNDECIDED, UNDECIDED at 300000 ms | term | UNDECIDED, UNDECIDED at 300000 ms | no |
| `idiv` gpr_one 32 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | UNDECIDED, UNDECIDED at 300000 ms | **yes** |
| `cmovne` gpr_gpr 32 | c | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `cmovne` gpr_gpr 32 | rust | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `cmovne` gpr_gpr 32 | go | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `cmovne` gpr_gpr 32 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | PROVED_ON_SHIP | **yes** |
| `setne` gpr_one 8 | c | term | DISPROVED, PROVED_ON_SHIP under caller extension | term | DISPROVED, PROVED_ON_SHIP under caller extension | no |
| `setne` gpr_one 8 | rust | term | DISPROVED, PROVED_ON_SHIP under caller extension | term | DISPROVED, PROVED_ON_SHIP under caller extension | no |
| `setne` gpr_one 8 | go | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `setne` gpr_one 8 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | DISPROVED, PROVED_ON_SHIP under caller extension | **yes** |
| `addss` xmm_xmm 32 | c | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `addss` xmm_xmm 32 | rust | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `addss` xmm_xmm 32 | go | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `addss` xmm_xmm 32 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | PROVED_ON_SHIP | **yes** |
| `cvtsi2sd` gpr_xmm 64 | c | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `cvtsi2sd` gpr_xmm 64 | rust | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `cvtsi2sd` gpr_xmm 64 | go | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `cvtsi2sd` gpr_xmm 64 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | PROVED_ON_SHIP | **yes** |
```

Table 3 — the run counted.

```
$ python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py tally3b
add gpr_gpr 32               flags      SAME BYTES       c, rust, swift
add gpr_gpr 32               reg_rdi    DIFFERENT BYTES  c, go, rust, swift
addss xmm_xmm 32             reg_xmm0   DIFFERENT BYTES  c, go, rust, swift
cmovne gpr_gpr 32            reg_rdi    DIFFERENT BYTES  c, go, rust, swift
cvtsi2sd gpr_xmm 64          reg_xmm0   DIFFERENT BYTES  c, go, rust, swift
idiv gpr_one 32              reg_rax    DIFFERENT BYTES  c, go, rust, swift
idiv gpr_one 32              reg_rdx    DIFFERENT BYTES  c, go, rust, swift
imul gpr_gpr 32              reg_rdi    DIFFERENT BYTES  c, go, rust, swift
sar cl_gpr 32                reg_rdi    DIFFERENT BYTES  c, go, rust, swift
setne gpr_one 8              reg_rdi    DIFFERENT BYTES  c, go, rust, swift
shr cl_gpr 64                reg_rdi    DIFFERENT BYTES  c, go, rust, swift
sub imm_gpr 64               flags      SAME BYTES       c, rust
sub imm_gpr 64               reg_rdi    DIFFERENT BYTES  c, go, rust, swift
compiled places more than one target has a body for: 13
   every target that compiled it emitted the same bytes: 2
   they emitted different bytes: 11

runs                             40
runs refused before any compile  0
places compiled and carved       50
LANDED                           17
LANDED_ELSEWHERE                 11
NOT_COLLAPSED                    22
PROVED_ON_SHIP                   39
proved under caller extension    3
neither                          8

instructions                                                   462
table cells                                                    240
chaff: ret                                                     39
chaff: calling-convention move                                 162
maps to no table cell                                          21
LANDED runs whose composition is exactly one cell, the target  14
```

**GLOSS**, beside Table 3, with task g1's own numbers for the same
counts in brackets. Forty runs, none refused before a compile (was ten).
Fifty places compiled and were carved (was thirty-seven). Seventeen
LANDED (was twelve), eleven LANDED_ELSEWHERE (was seven), twenty-two did
not collapse to one instruction (was eighteen). Thirty-nine places were
PROVED_ON_SHIP (was twenty-nine), three more once each narrow-holder row
is zero-extended to the register (was two), and eight were neither (was
six) — the eight are the divide's places, now including swift's two. The
composition tally counts 462 raw carved instructions (was 434), of which
240 are table cells, 201 are chaff and 21 map to no table cell.

---

# 6. What did not work, by cause

## 6.1 Refusals and gate calls that did not prove

```
$ sed -n \\%\^###\ 3.1\ Refusals%\,\\%\^###\ 3.2%p /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3b.md
### 3.1 Refusals and gate calls that did not prove

- `a width c has no holder for`: 2 -- sub imm_gpr 64/go [flags], sub imm_gpr 64/swift [flags]
- `the flags place of a preseeded row is the flag state that ARRIVED, not a place this opcode writes`: 8 -- cmovne gpr_gpr 32/c [flags], cmovne gpr_gpr 32/rust [flags], cmovne gpr_gpr 32/go [flags], cmovne gpr_gpr 32/swift [flags], setne gpr_one 8/c [flags], setne gpr_one 8/rust [flags], setne gpr_one 8/go [flags], setne gpr_one 8/swift [flags]
- `the gate answered UNDECIDED at 3,000 ms and again at 300000 ms`: 8 -- idiv gpr_one 32/c [reg_rax], idiv gpr_one 32/c [reg_rdx], idiv gpr_one 32/rust [reg_rax], idiv gpr_one 32/rust [reg_rdx], idiv gpr_one 32/go [reg_rax], idiv gpr_one 32/go [reg_rdx], idiv gpr_one 32/swift [reg_rax], idiv gpr_one 32/swift [reg_rdx]
- `the primitive route renders the operator's own answer, and the flags place is not a value an operator answers with`: 4 -- add gpr_gpr 32/go [flags], imul gpr_gpr 32/c [flags], imul gpr_gpr 32/rust [flags], imul gpr_gpr 32/go [flags]

### 3.2 The landings that were not LANDED, by cause
```

Read as four causes, with status. **The whole "the compiler refused"
cause is gone**: it accounted for thirteen places in task g1's run and
accounts for none here.

- **the gate answered UNDECIDED at 3,000 ms and again at 300,000 ms
  (8)** — the divide's two places in all four targets. OPEN; §7 is the
  attempt on it.
- **the flags place of a preseeded row is the flag state that ARRIVED
  (8)** — `cmovne` and `setne`, all four targets. HISTORICAL, task h1's
  own cause: these two cells consume flags rather than write them.
- **the primitive route renders the operator's own answer, and the flags
  place is not a value an operator answers with (4)** — task g1's own
  cause, unchanged: an operator hands back one value.
- **a width c has no holder for (2)** — the 128-bit flags place of
  `sub imm_gpr 64`. HISTORICAL, task h1's own cause.

## 6.2 The landings that were not LANDED, by cause

```
$ sed -n \\%\^###\ 3.2\ The\ landings%\,\\%\^##\ 4%p /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3b.md
### 3.2 The landings that were not LANDED, by cause

- the cell's own arch opcode IS among the ones that remain; what sits beside it is what the term carries beyond the operation (2 remain): 2 -- sar cl_gpr 32/go [reg_rdi], shr cl_gpr 64/go [reg_rdi]
- the cell's own arch opcode IS among the ones that remain; what sits beside it is what the term carries beyond the operation (3 remain): 1 -- addss xmm_xmm 32/go [reg_xmm0]
- the cell's own arch opcode IS among the ones that remain; what sits beside it is what the term carries beyond the operation (4 remain): 1 -- cvtsi2sd gpr_xmm 64/go [reg_xmm0]
- the cell's own arch opcode IS among the ones that remain; what sits beside it is what the term carries beyond the operation (51 remain): 4 -- idiv gpr_one 32/c [reg_rax], idiv gpr_one 32/c [reg_rdx], idiv gpr_one 32/rust [reg_rax], idiv gpr_one 32/rust [reg_rdx]
- the cell's own arch opcode IS among the ones that remain; what sits beside it is what the term carries beyond the operation (85 remain): 2 -- idiv gpr_one 32/go [reg_rax], idiv gpr_one 32/go [reg_rdx]
- the compiler chose another arch opcode for the same computation (`add`): 1 -- sub imm_gpr 64/go [reg_rdi]
- the compiler chose another arch opcode for the same computation (`jmp`): 2 -- idiv gpr_one 32/swift [reg_rax], idiv gpr_one 32/swift [reg_rdx]
- the compiler chose another arch opcode for the same computation (`lea`): 6 -- add gpr_gpr 32/c [reg_rdi], add gpr_gpr 32/rust [reg_rdi], add gpr_gpr 32/swift [reg_rdi], sub imm_gpr 64/c [reg_rdi], sub imm_gpr 64/rust [reg_rdi], sub imm_gpr 64/swift [reg_rdi]
- the compiler chose another arch opcode for the same computation (`mov`): 2 -- sub imm_gpr 64/c [flags], sub imm_gpr 64/rust [flags]
- the emulation is a PAIR by construction (the setter's comparison, then the select), so more than one arch opcode was never possible (13 remain): 1 -- setne gpr_one 8/go [reg_rdi]
- the emulation is a PAIR by construction (the setter's comparison, then the select), so more than one arch opcode was never possible (2 remain): 4 -- cmovne gpr_gpr 32/c [reg_rdi], cmovne gpr_gpr 32/rust [reg_rdi], cmovne gpr_gpr 32/go [reg_rdi], cmovne gpr_gpr 32/swift [reg_rdi]
- the emulation is a PAIR by construction (the setter's comparison, then the select), so more than one arch opcode was never possible (3 remain): 3 -- setne gpr_one 8/c [reg_rdi], setne gpr_one 8/rust [reg_rdi], setne gpr_one 8/swift [reg_rdi]
- the flags place is the reference's flag model -- the two values the setter compared, repacked -- so it is not one operation and no single arch opcode is its landing (2 remain): 4 -- add gpr_gpr 32/c [flags], add gpr_gpr 32/rust [flags], add gpr_gpr 32/swift [flags], imul gpr_gpr 32/swift [flags]

## 4. Task g1's verdict beside this run's
```

Read as four causes, with status. One is new with swift and worth its
own line.

- **the term carries more than the operation (10)** — the cell's own
  arch opcode IS in the carved body; what sits beside it is what the
  term carries. OPEN, and it is the size question: the divide is the
  extreme (51 remaining in c and rust, 85 in go).
- **the compiler chose another arch opcode for the same computation
  (11)** — `lea` for `add` and `sub` in three targets, `add` for go's
  `sub`, `mov` for two flags places. Not a defect: LANDED_ELSEWHERE with
  a PROVED_ON_SHIP verdict is the compiler picking a different
  instruction for the same function.
- **swift's divide carved as a `jmp` (2), new in this run** — the two
  swift divide places landed on `jmp`, because `swiftc -O` emitted the
  `@_cdecl` entry point as a thunk that tail-jumps to the mangled swift
  function, and the carve reads the named symbol's own bytes. So what
  was carved is the thunk and not the computation, and the UNDECIDED
  verdict on those two places rests on a body that is one branch.
  OPEN, and named here rather than folded into the divide's other
  causes; it is a carve-boundary question, not a proof question.
- **the emulation is a PAIR by construction (8)** and **the flags place
  is the reference's flag model (4)** — `cmovne`, `setne`, and the two
  `add` flags places. HISTORICAL, task h1's own causes.

---

# 7. The lookup widened by one step

## 7.1 The rule, LITERAL

**LITERAL**,
`~/Programming/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py`,
section 2e, `is_setup_line` — what counts as setup:

```python
def is_setup_line(line):
    mnem, operands = SOU.parse_insn(line)
    if mnem is None:
        return False
    if mnem not in SETUP_MNEMONICS:
        return False
    return len(operands) == 0
```

**LITERAL**, the same file and section, `primitive_rows_with_setup` —
the acceptance itself:

```python
    for rule in ("narrow", "wide"):
        for row in (groups.get(rule) or []):
            if row["body_text"] in seen:
                continue
            seen.add(row["body_text"])
            body = row["body_text"].split("; ")
            stripped = SOU.strip_chaff(body, "narrow")
            setup, rest = split_setup(stripped)
            if len(rest) != 1:
                continue
            line = rest[0]
            mnem, _operands = SOU.parse_insn(line)
            shape, width, cause = MTAB.classify_line(mnem, line, 0)
```

**GLOSS**, beside both. `SETUP_MNEMONICS` is the union of the keys of
`reference.SPREAD_SIGN` and `reference.ACCUMULATOR_WIDEN` — a closed
list read from the reference simulator, not a judgement — and a line
counts as setup only if it also carries NO OPERAND, so the rule can
never widen past that list. Both of task o2's rule lists are read,
because the divide's row is a single-opcode row under the WIDE rule
only; each row's body is then stripped again under the NARROW rule,
because the wide rule counts `cltd` and `cqto` as chaff and would throw
away the very instructions this route must see. A row is accepted when
what remains is setup plus EXACTLY ONE other instruction and that one
classifies to the cell. The route is recorded as `primitive+setup` when
the accepted row carries setup and stays `primitive` when it carries
none, which is task g1's own answer unchanged.

## 7.2 Which pairs it changes: one of forty

```
$ python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py changes3c
the (cell, target) pairs the widened lookup changes
   [21/40] idiv gpr_one 32 -> c: term becomes primitive+setup, on `mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret`
   1 of 40 pair(s) change

   idiv gpr_one 32 -> c
peak resident: 83096 kB
```

**GLOSS**: both lookups are run for every one of the forty pairs and the
two answers compared, so "which pairs change" is a measurement. One
changes. The brief expected three — the divide in c, rust and go. (The
conventions verifier scores this transcript NOT_RERUNNABLE for the
cause `output_annotated`, because the program's own line carries `->`
and the verifier reads an arrow in a paste as a hand-written gloss. The
command runs and the output is its own; the cause is a heuristic
misfire on real output, and it is left rather than worked around.)

## 7.3 Why one and not three

```
$ python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py whynot3c idiv gpr_one 32 | grep -v 'peak resident'
cell idiv gpr_one 32

c: 2 row(s) accepted by the widened rule at this cell; 10 row(s) of 109 carry the mnemonic at all
   found under the wide rule, 49 member(s), e.g. c/op_210
      body:    mov %edi,%eax; cltd; idiv %esi; ret
      strip:   cltd; idiv %esi
      setup:   cltd
      rest:    idiv %esi
      ACCEPTED at this cell
   found under the wide rule, 25 member(s), e.g. c/op_211
      body:    movslq %edi,%rax; cqto; idiv %rsi; ret
      strip:   movslq %edi,%rax; cqto; idiv %rsi
      setup:   cqto
      rest:    movslq %edi,%rax; idiv %rsi
      REJECTED: the non-setup part is 2 instructions, not one
   found under the wide rule, 25 member(s), e.g. c/op_216
      body:    mov %rdi,%rax; movslq %esi,%rcx; cqto; idiv %rcx; ret
      strip:   movslq %esi,%rcx; cqto; idiv %rcx
      setup:   cqto
      rest:    movslq %esi,%rcx; idiv %rcx
      REJECTED: the non-setup part is 2 instructions, not one
   found under the wide rule, 17 member(s), e.g. c/op_217
      body:    mov %rdi,%rax; cqto; idiv %rsi; ret
      strip:   cqto; idiv %rsi
      setup:   cqto
      rest:    idiv %rsi
      REJECTED: classifies to (idiv, gpr_one, 64), not this cell
   found under the wide rule, 49 member(s), e.g. c/op_246
      body:    mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret
      strip:   cltd; idiv %esi
      setup:   cltd
      rest:    idiv %esi
      ACCEPTED at this cell
   found under the wide rule, 25 member(s), e.g. c/op_247
      body:    movslq %edi,%rax; cqto; idiv %rsi; mov %rdx,%rax; ret
      strip:   movslq %edi,%rax; cqto; idiv %rsi
      setup:   cqto
      rest:    movslq %edi,%rax; idiv %rsi
      REJECTED: the non-setup part is 2 instructions, not one
   found under the wide rule, 25 member(s), e.g. c/op_252
      body:    mov %rdi,%rax; movslq %esi,%rcx; cqto; idiv %rcx; mov %rdx,%rax; ret
      strip:   movslq %esi,%rcx; cqto; idiv %rcx
      setup:   cqto
      rest:    movslq %esi,%rcx; idiv %rcx
      REJECTED: the non-setup part is 2 instructions, not one
   found under the wide rule, 17 member(s), e.g. c/op_253
      body:    mov %rdi,%rax; cqto; idiv %rsi; mov %rdx,%rax; ret
      strip:   cqto; idiv %rsi
      setup:   cqto
      rest:    idiv %rsi
      REJECTED: classifies to (idiv, gpr_one, 64), not this cell
   found under the wide rule, 12 member(s), e.g. c/regen_12133
      body:    mov %rdi,%rax; mov %esi,%ecx; cqto; idiv %rcx; ret
      strip:   cqto; idiv %rcx
      setup:   cqto
      rest:    idiv %rcx
      REJECTED: classifies to (idiv, gpr_one, 64), not this cell
   found under the wide rule, 12 member(s), e.g. c/regen_14605
      body:    mov %rdi,%rax; mov %esi,%ecx; cqto; idiv %rcx; mov %rdx,%rax; ret
      strip:   cqto; idiv %rcx
      setup:   cqto
      rest:    idiv %rcx
      REJECTED: classifies to (idiv, gpr_one, 64), not this cell

rust: 0 row(s) accepted by the widened rule at this cell; 0 row(s) of 48 carry the mnemonic at all

go: 0 row(s) accepted by the widened rule at this cell; 0 row(s) of 27 carry the mnemonic at all

swift: 0 row(s) accepted by the widened rule at this cell; 0 row(s) of 19 carry the mnemonic at all
```

**GLOSS**, and this is the finding. In c, ten of the corpus's 109
single-opcode rows carry the divide instruction, two of them are the
cell's instruction plus `cltd` and nothing else, and those two are
accepted. In rust, go and swift, ZERO rows carry it — not zero accepted,
zero present, out of 48, 27 and 19 rows respectively. So no widening of
THIS rule could reach them; the limit is in task o2's input artifact,
and the reason is in the corpus underneath it:

```
$ python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py bodies3c idiv | grep -v 'peak resident'

c: 12 unit(s) of 610 carry `idiv`
   the shortest such body, 4 instruction(s), unit c/op_210 (display label `/`):
      mov %edi,%eax
      cltd
      idiv %esi
      ret
   the longest such body, 6 instruction(s), unit c/op_252 (display label `%`):
      mov %rdi,%rax
      movslq %esi,%rcx
      cqto
      idiv %rcx
      mov %rdx,%rax
      ret

rust: 4 unit(s) of 125 carry `idiv`
   the shortest such body, 17 instruction(s), unit rust/op_642 (display label `/`):
      push %rax
      test %esi,%esi
      je 1a <op_642+0x1a>
      mov %esi,%eax
      not %eax
      lea -0x80000000(%rdi),%ecx
      or %eax,%ecx
      je 27 <op_642+0x27>
      mov %edi,%eax
      cltd
      idiv %esi
      pop %rcx
      ret
      lea 0x0(%rip),%rdi !!reloc=R_X86_64_PC32:.data.rel.ro..Lanon.e999d8e928eeaaa2810ddee94f44a439.1-0x4
      call *0x0(%rip) !!reloc=R_X86_64_GOTPCREL:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero-0x4
      lea 0x0(%rip),%rdi !!reloc=R_X86_64_PC32:.data.rel.ro..Lanon.e999d8e928eeaaa2810ddee94f44a439.1-0x4
      call *0x0(%rip) !!reloc=R_X86_64_GOTPCREL:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow-0x4
   the longest such body, 19 instruction(s), unit rust/op_685 (display label `%`):
      push %rax
      test %rsi,%rsi
      je 2b <op_685+0x2b>
      mov %rsi,%rax
      not %rax
      movabs $0x8000000000000000,%rcx
      xor %rdi,%rcx
      or %rax,%rcx
      je 38 <op_685+0x38>
      mov %rdi,%rax
      cqto
      idiv %rsi
      mov %rdx,%rax
      pop %rcx
      ret
      lea 0x0(%rip),%rdi !!reloc=R_X86_64_PC32:.data.rel.ro..Lanon.59c7b7ded09d4d41cf4c16e5b51ce86c.1-0x4
      call *0x0(%rip) !!reloc=R_X86_64_GOTPCREL:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero-0x4
      lea 0x0(%rip),%rdi !!reloc=R_X86_64_PC32:.data.rel.ro..Lanon.59c7b7ded09d4d41cf4c16e5b51ce86c.1-0x4
      call *0x0(%rip) !!reloc=R_X86_64_GOTPCREL:_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow-0x4

go: 4 unit(s) of 107 carry `idiv`
   the shortest such body, 15 instruction(s), unit go/op_96 (display label `/`):
      push %rbp
      mov %rsp,%rbp
      test %ebx,%ebx
      je 47a658 <main.op_96+0x18>
      cmp $0xffffffff,%ebx
      jne 47a653 <main.op_96+0x13>
      neg %eax
      xor %edx,%edx
      jmp 47a656 <main.op_96+0x16>
      cltd
      idiv %ebx
      pop %rbp
      ret
      call 43f3c0 <runtime.panicdivide>
      nop
   the longest such body, 17 instruction(s), unit go/op_139 (display label `%`):
      push %rbp
      mov %rsp,%rbp
      test %rbx,%rbx
      je 47a681 <main.op_139+0x21>
      cmp $0xffffffffffffffff,%rbx
      jne 47a676 <main.op_139+0x16>
      neg %rax
      xor %edx,%edx
      jmp 47a67b <main.op_139+0x1b>
      cqto
      idiv %rbx
      mov %rdx,%rax
      pop %rbp
      nop
      ret
      call 43f360 <runtime.panicdivide>
      nop

swift: 4 unit(s) of 167 carry `idiv`
   the shortest such body, 12 instruction(s), unit swift/op_150 (display label `/`):
      test %esi,%esi
      je 17 <op_150+0x17>
      cmp $0x80000000,%edi
      jne 11 <op_150+0x11>
      cmp $0xffffffff,%esi
      je 19 <op_150+0x19>
      mov %edi,%eax
      cltd
      idiv %esi
      ret
      ud2
      ud2
   the longest such body, 23 instruction(s), unit swift/op_193 (display label `%`):
      test %rsi,%rsi
      je 3b <op_193+0x3b>
      movabs $0x8000000000000000,%rax
      cmp %rax,%rdi
      jne 1a <op_193+0x1a>
      cmp $0xffffffffffffffff,%rsi
      je 3d <op_193+0x3d>
      mov %rdi,%rax
      or %rsi,%rax
      shr $0x20,%rax
      je 32 <op_193+0x32>
      mov %rdi,%rax
      cqto
      idiv %rsi
      mov %rdx,%rax
      ret
      mov %edi,%eax
      xor %edx,%edx
      div %esi
      mov %edx,%eax
      ret
      ud2
      ud2
```

**GLOSS**, beside it. c's shortest divide body is four instructions and
carries no guard at all, because c leaves division by zero and
`INT_MIN / -1` undefined and clang emits nothing for them. Rust's
shortest is seventeen: a zero test, an overflow test, and two calls into
`core::panicking`. Go's carries a compare, a branch and a call into
`runtime.panicdivide`. Swift's carries a zero test, an overflow test and
two `ud2` traps. Those guards ARE the edge regions of the owner's model, and
because they sit inside the function body, the body is never one
instruction under either of task o2's chaff rules, so the language never
produces a single-opcode row for its divide. **The primitive route
reaches an operator exactly when the target leaves the edge region
undefined.**

## 7.4 What the one changed run answers

```
$ sed -n \\%\^.\ cell\ .\ lang\ .\ route\ .\ single-opcode\ rows%\,\\%\^\$%p /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3c.md
| cell | lang | route | single-opcode rows at this cell | chosen row's body, LITERAL | the setup cells the row carries | the operator and operand types the manifest records | cause if no primitive |
|---|---|---|---|---|---|---|---|
| `idiv` gpr_one 32 | c | primitive+setup | 2 | `mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret` | `cltd` = (`cltd`, none, 32) | `a % b on int32_t and int32_t` (probe c/op_246 of c) |  |
```

**GLOSS**: the chosen row is the corpus's own, attested by 49 members,
and the setup it carries is one instruction, `cltd`, which classifies to
the model-table cell (`cltd`, `none`, 32). What is rendered is the
member's own probe source, one line.

```
$ sed -n \\%\^.\ cell\ .\ lang\ .\ g1\ route%\,\\%\^\$%p /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3c.md
| cell | lang | g1 route | g1 verdict | this route | this verdict | moved |
|---|---|---|---|---|---|---|
| `idiv` gpr_one 32 | c | term | UNDECIDED, UNDECIDED at 300000 ms | primitive+setup | UNDECIDED, UNDECIDED at 300000 ms | **yes** |
```

**GLOSS**, and this is the result. The route moved from `term` to
`primitive+setup`, and the verdict did not move: UNDECIDED at 3,000 ms
and UNDECIDED again at 300,000 ms. **But the two UNDECIDEDs are not the
same UNDECIDED**, and the difference is the whole point.

- **Task g1's**, term route — the reason is the solver's clock. The
  emulation was 76 instructions, 51 after the strip, and z3 did not
  answer inside either ceiling.
- **This run's**, primitive+setup route — the reason is structural, and
  it is the same at any ceiling. The gate's own words, LITERAL from
  `handful3c.json`:

```
the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows
```

**GLOSS**: the cell `idiv %edi` reads THREE arriving values — the high
half of the dividend, its low half, and the divisor. The emulation, `a %
b` on two `int32_t`, reads TWO, and derives the third with `cltd`. So
the emulation is not the cell; it is the cell RESTRICTED to the region
where the arriving high half is the sign extension of the low half. The
gate aligns inputs IN row by IN row and has no way to say "this input is
a function of that one", so it declines rather than answers. **That is
the edge-region question in machine form, and it is the one this line
now has to answer.** The size problem the divide had is gone — five
instructions where there were seventy-six — and what is left underneath
it is a question about arrival contracts.

There is no `sat` here, so there is no counterexample and no region for
this log to name. The two regions the brief expected — division by zero,
and `INT_MIN / -1` — are not what the gate ran into; §7.3 shows where
they are instead, which is inside the other three targets' function
bodies as guards.

---

# 8. One defect, found and fixed: the re-posed parameter plan

Lane `g1b_l10_run_of_record_c.sh` — the widened lookup's FIRST run —
returned DISPROVED on both of the divide's places, with counterexamples.
That answer was wrong, and this section is why, because a wrong answer
that is not chased is worse than no answer.

**LITERAL**, `handful.py`, `one_recheck` as it stood before this task:

```python
    renderer = rebuilt_renderer(wanted, run["lang"], place["label"])
    raw_bytes = place["body_bytes"].split()
    mnem = place["body_text"].split("; ")
    return check_one_place(shared, wanted, renderer.params, raw_bytes,
                           mnem, place["label"], run["lang"])
```

**GLOSS**: `rebuilt_renderer` builds the TERM-ROUTE renderer for the
place and takes its parameter plan. The plan is the arrival contract —
`check_one_place` turns it into the register list the body reads and
aligns that against the cell's families, position by position. For a
term-route place the rebuilt plan is the one the run used. For a
PRIMITIVE-route place it is not: that plan comes from
`primitive_params(probe)`, the operand types the manifest records, which
for the divide in c is two rows where the term route's is three. Handed
three rows, the re-pose aligned the emulation's first argument against
the cell's HIGH DIVIDEND HALF and answered DISPROVED about a comparison
nobody posed. The first pass had already declined for exactly that
reason at its own ceiling.

The fix is the general one, in the shared step rather than at the call
site: use the plan the place RECORDS, and rebuild only where none is
recorded.

Whether that moves a results file already written is a question with a
mechanical answer, so it was measured rather than asserted — and the
first attempt at measuring it asked the wrong question (whether a place
records a plan at all; they all do). What matters is whether the two
plans give the same ARRIVAL CONTRACT:

```
$ python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py rechecked3b
idiv gpr_one 32/c [reg_rax]: run route term; the plan the place RECORDS gives ['rdi', 'rsi', 'rdx']; the plan the old code REBUILT gives ['rdi', 'rsi', 'rdx']; the same
idiv gpr_one 32/c [reg_rdx]: run route term; the plan the place RECORDS gives ['rdi', 'rsi', 'rdx']; the plan the old code REBUILT gives ['rdi', 'rsi', 'rdx']; the same
idiv gpr_one 32/rust [reg_rax]: run route term; the plan the place RECORDS gives ['rdi', 'rsi', 'rdx']; the plan the old code REBUILT gives ['rdi', 'rsi', 'rdx']; the same
idiv gpr_one 32/rust [reg_rdx]: run route term; the plan the place RECORDS gives ['rdi', 'rsi', 'rdx']; the plan the old code REBUILT gives ['rdi', 'rsi', 'rdx']; the same
idiv gpr_one 32/go [reg_rax]: run route term; the plan the place RECORDS gives ['rax', 'rbx', 'rcx']; the plan the old code REBUILT gives ['rax', 'rbx', 'rcx']; the same
idiv gpr_one 32/go [reg_rdx]: run route term; the plan the place RECORDS gives ['rax', 'rbx', 'rcx']; the plan the old code REBUILT gives ['rax', 'rbx', 'rcx']; the same
idiv gpr_one 32/swift [reg_rax]: run route term; the plan the place RECORDS gives ['rdi', 'rsi', 'rdx']; the plan the old code REBUILT gives ['rdi', 'rsi', 'rdx']; the same
idiv gpr_one 32/swift [reg_rdx]: run route term; the plan the place RECORDS gives ['rdi', 'rsi', 'rdx']; the plan the old code REBUILT gives ['rdi', 'rsi', 'rdx']; the same

re-posed places: 8
of those, the two plans give different arrival contracts: 0
so the parameter-plan fix moves: 0 of them
```

```
$ python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py rechecked3c
idiv gpr_one 32/c [reg_rax]: run route primitive+setup; the plan the place RECORDS gives ['rdi', 'rsi']; the plan the old code REBUILT gives ['rdi', 'rsi', 'rdx']; DIFFERS
idiv gpr_one 32/c [reg_rdx]: run route primitive+setup; the plan the place RECORDS gives ['rdi', 'rsi']; the plan the old code REBUILT gives ['rdi', 'rsi', 'rdx']; DIFFERS

re-posed places: 2
of those, the two plans give different arrival contracts: 2
so the parameter-plan fix moves: 2 of them
```

**GLOSS**: for all eight re-posed places of `handful3b.json` the
recorded plan and the rebuilt one give the same three registers, so the
fix moves none of them and the second run of record stands as it is. For
both re-posed places of `handful3c.json` they differ — two registers
against three — which is exactly the defect, and those two are the runs
§7.4 reports, re-run after the fix by lane
`g1b_l11_run_of_record_c2.sh`.

---

# 9. Memory

The bound stated in `g1.conf` and in every lane header is 4 GB resident
on the one collecting process, named aborts `ABORT_MEMORY_G1B` and
`ABORT_MEMORY_G1C`, checked after every run and every re-pose. The
peaks the programs printed: 89,976 kB through the forty runs before the
divide, 488,376 kB at the highest re-pose, 258,548 kB through the
composition step, 87,832 kB through the widened lookup's own run,
257,928 kB through its composition step, and 81,636 kB through the
corpus read of `bodies3c`, which reads one 4.9 MB file at a time. The
high-water mark, 488,376 kB, is 12% of the bound. No abort fired.

---

# 10. The guard, unmodified

The spelling-key check was run over every json this task's own programs
write, and `grep -c exempt` over every file this task added or changed.

```
$ python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3b.json /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3b_primitive.json /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3b_spellings.json /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3c.json /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3c_primitive.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS handful3b.json -- no operator token in any key, grouping, pairing or row structure
PASS handful3b_primitive.json -- no operator token in any key, grouping, pairing or row structure
PASS handful3b_spellings.json -- no operator token in any key, grouping, pairing or row structure
PASS handful3c.json -- no operator token in any key, grouping, pairing or row structure
PASS handful3c_primitive.json -- no operator token in any key, grouping, pairing or row structure
```

```
$ grep -c exempt /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3b.md /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3c.md /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_g1b/g1b_l8_run_of_record_b.sh /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_g1b/g1b_l11_run_of_record_c2.sh
/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py:0
/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3b.md:0
/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3c.md:0
/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_g1b/g1b_l8_run_of_record_b.sh:0
/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_g1b/g1b_l11_run_of_record_c2.sh:0
```

`grep -c` exits 1 when a count it prints is zero, which is why the lane
carries `|| true` on that step; the counts themselves are the answer,
and every one is 0.

**On the widened rule and the ban.** The rule reads a mnemonic and an
operand count and nothing else. `SETUP_MNEMONICS` is keyed by arch
mnemonic, which is machine form; the match against a cell is the
(`mnem`, shape, `key_width`) triple the ruling of 2026-09-08 states; and
the operator token is read afterwards, off the chosen row's member, as
the display label on a unit object. Nothing about the widening
introduces a token anywhere.

---

# 11. The conventions verifier over this log

**LITERAL**, printed by lane `g1b_l16_verify_242_2.sh`, on the tower at
`~/AirlockRuns/g1/agent/logs/20260909T102006Z__g1b_l16_verify_242_2.sh.log`.
It was run over this log AS IT STOOD BEFORE THIS SECTION WAS APPENDED
and before the note about Airlock's `.gitignore` was added to the
deliverables list above.  Between them those two additions add one
attribution claim and nothing that re-runs, and they move the line
numbers in the table below.  Lane `g1b_l17_verify_242_3.sh` is the pass
over the log as it now stands, and it returns 26 claims, 13 MATCHES,
**0 DIFFERS**, 9 UNVERIFIABLE, 1 REFUSED and 3 NOT_RERUNNABLE -- the
two additions are the two extra UNVERIFIABLE and change nothing else.

```
## log_242_task_g1b_swift_and_the_widened_lookup.md
   claims 24 | MATCHES 13 | DIFFERS 0 | UNVERIFIABLE 7 | REFUSED 1 | NOT_RERUNNABLE 3
   VERDICT: 13 of 24 claims reproduce; 7 (29%) carry nothing to re-run

   | line | shape | outcome | claim / reason |
   |---|---|---|---|
   | 138 | prose_verification | **UNVERIFIABLE** | `The forty runs were then run again, unchanged in every other respect. All forty reach a compiled` — prose_only -- a verification is asserted with nothing beside it |
   | 185 | attribution | **UNVERIFIABLE** | `**LITERAL**, `~/Programming/Airlock/instance.sh` lines 174-176, which is where the empty volume ` — attribution_only -- cites `~/Programming/Airlock/instance.sh`, carries no command |
   | 209 | shell_transcript | **NOT_RERUNNABLE** | `ls -la /persist/swift/usr/bin/swiftc` — output_annotated -- the paste carries an arrow gloss (`->`); an exact comparison is impossible |
   | 213 | shell_transcript | **NOT_RERUNNABLE** | `ls -la /usr/lib/x86_64-linux-gnu/libncurses.so.6` — output_annotated -- the paste carries an arrow gloss (`->`); an exact comparison is impossible |
   | 217 | shell_transcript | **REFUSED** | `/persist/swift/usr/bin/swiftc --version` — head_not_on_the_read_only_allowlist -- `/persist/swift/usr/bin/swiftc` |
   | 248 | shell_transcript | **MATCHES** | `sed -n \\%\^.\ cell\ .\ lang\ .\ route\ .\ rendered%\,\\%\^\$%p /projects/PseudoCoupHQ/Research/` |
   | 304 | shell_transcript | **MATCHES** | `sed -n \\%\^.\ cell\ .\ lang\ .\ g1\ route%\,\\%\^\$%p /projects/PseudoCoupHQ/Research/oracle/cr` |
   | 352 | shell_transcript | **MATCHES** | `python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py t` |
   | 406 | shell_transcript | **MATCHES** | `sed -n \\%\^###\ 3.1\ Refusals%\,\\%\^###\ 3.2%p /projects/PseudoCoupHQ/Research/oracle/cross_co` |
   | 436 | shell_transcript | **MATCHES** | `sed -n \\%\^###\ 3.2\ The\ landings%\,\\%\^##\ 4%p /projects/PseudoCoupHQ/Research/oracle/cross_` |
   | 490 | attribution | **UNVERIFIABLE** | `**LITERAL**, `~/Programming/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/ha` — attribution_only -- cites `~/Programming/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/han |
   | 503 | attribution | **UNVERIFIABLE** | `**LITERAL**, the same file and section, `primitive_rows_with_setup` — the acceptance itself:` — attribution_only -- cites `primitive_rows_with_setup`, carries no command |
   | 536 | shell_transcript | **NOT_RERUNNABLE** | `python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py c` — output_annotated -- the paste carries an arrow gloss (`->`); an exact comparison is impossible |
   | 557 | shell_transcript | **MATCHES** | `python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py w` |
   | 638 | shell_transcript | **MATCHES** | `python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py b` |
   | 786 | shell_transcript | **MATCHES** | `sed -n \\%\^.\ cell\ .\ lang\ .\ route\ .\ single-opcode\ rows%\,\\%\^\$%p /projects/PseudoCoupH` |
   | 798 | shell_transcript | **MATCHES** | `sed -n \\%\^.\ cell\ .\ lang\ .\ g1\ route%\,\\%\^\$%p /projects/PseudoCoupHQ/Research/oracle/cr` |
   | 816 | attribution | **UNVERIFIABLE** | `- **Task g1's**, term route — the reason is the solver's clock. The emulation was 76 instruction` — attribution_only -- cites `handful3c.json`, carries no command |
   | 849 | attribution | **UNVERIFIABLE** | `**LITERAL**, `handful.py`, `one_recheck` as it stood before this task:` — attribution_only -- cites `handful.py`, carries no command |
   | 881 | shell_transcript | **MATCHES** | `python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py r` |
   | 897 | shell_transcript | **MATCHES** | `python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py r` |
   | 936 | shell_transcript | **MATCHES** | `python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py /projects/PseudoCo` |
   | 946 | shell_transcript | **MATCHES** | `grep -c exempt /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handf` |
   | 972 | prose_verification | **UNVERIFIABLE** | `1. **`g1.conf` now mounts `sandbox-persist` read-only**, with the reason written into its header` — prose_only -- a verification is asserted with nothing beside it |
```

**GLOSS**, and the obligation the law states is the DIFFERS column:
**0 DIFFERS**. Every claim that carries a command and can be re-run
reproduces. The other four outcomes, each with its cause, so none of
them reads as a pass by omission:

- **REFUSED (1)** — `/persist/swift/usr/bin/swiftc --version`, in §3's
  attribution block. An absolute path to a compiler is not on the
  verifier's read-only allowlist, so the line is named and never run.
  The block is an attribution to lane `g1b_l5_swift_probe.sh`'s own log,
  which is where the machine answered; it is not offered as a
  re-runnable transcript.
- **NOT_RERUNNABLE (3), all for the cause `output_annotated`** — two
  `ls -la` lines in the same attribution block and one `changes3c`
  transcript. The verifier reads `->` in a paste as a hand-written
  gloss; here the arrow is real output, from a symlink in the two `ls`
  lines and from the program's own wording in `changes3c`. A heuristic
  misfire on genuine output, left as it is rather than worked around by
  rewording the program.
- **UNVERIFIABLE (7)** — five attributions (each naming the file or lane
  log it came from) and two prose paragraphs: §2's walkthrough, which
  the protocol requires to open a report, and §12's first decided item.
- **MATCHES (13)** — every transcript this log pastes from lane
  `g1b_l15_evidence3.sh`.

An earlier pass, lane `g1b_l14_verify_242.sh`, returned 2 DIFFERS, and
both were the same cause: two of the pasted commands end with the
program's own `peak resident` line, a real measurement that moves by a
few kB between runs. It was fixed in the CLAIM and never in the
verifier — lane `g1b_l15_evidence3.sh` prints those two commands with
`| grep -v 'peak resident'` on the pasted line itself, so what is
printed is what ran, and the memory figures are in §9 where they belong.

---

# 12. The two lists

## Decided, recorded for audit

1. **`g1.conf` now mounts `sandbox-persist` read-only**, with the reason
   written into its header. It is this task's own instance
   configuration, and the pattern is the one `t101b.conf` and
   `t103.conf` already use for the same toolchain. Without it the
   rebuilt image alone would not have made `swiftc` reachable, because
   the empty default volume sits over the path it lives at.
2. **Both obstacles to swift are recorded separately**, because they
   were independent and only one of them was the one this task was told
   about (§3).
3. **The second run of record re-ran all forty pairs, not the ten swift
   ones**, so the 40-row table comes from one run rather than from
   stitching two, and the thirty unchanged rows are a check rather than
   an assumption (§5, Table 2).
4. **The widened rule reads a closed list from the reference
   simulator** — the keys of `SPREAD_SIGN` and `ACCUMULATOR_WIDEN`, and
   only where the line carries no operand — so it cannot widen further
   by accident (§7.1).
5. **It changes one of forty pairs, and the other three targets' silence
   is a measurement, not an omission**: their corpora hold zero
   single-opcode rows carrying the divide instruction, because their
   divide bodies carry guards (§7.3).
6. **The defect in `one_recheck` was fixed in the shared step**, and its
   effect on both results files was measured per place rather than
   asserted: it moves 0 of `handful3b.json`'s eight re-posed places and
   both of `handful3c.json`'s (§8).
7. **No workaround was attempted for swift at any point** — no
   `LD_LIBRARY_PATH`, no copied library, no second path.
8. **Task g1's four products were not written by any lane of this
   task.**

## Awaiting the owner

1. **The divide's gate call is now an ARRIVAL-CONTRACT question, not a
   size question, and it needs a ruling.** On the primitive+setup route
   the emulation reads two inputs where the cell reads three, because
   `cltd` derives the third from the first; the gate aligns IN row by IN
   row and cannot express "this input is a function of that one", so it
   declines. Either the gate learns to pose a comparison over a
   CONSTRAINED region of the cell's inputs, or a cell whose arrival is
   partly derived is a different kind of entry in the Hub. Both are
   ontology, not implementation (§7.4).
2. **Swift's divide was carved from a thunk.** `swiftc -O` emitted the
   `@_cdecl` entry point as a tail-jump to the mangled swift function,
   so the carve read one `jmp` and the gate answered about that. This is
   the unit-boundary ruling of 2026-09-04 meeting a compiler that puts
   the body behind a second symbol; it is flagged, not worked around
   (§6.2).
