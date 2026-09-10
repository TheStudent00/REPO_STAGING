# log_258 — task rv1: RISC-V as a second architecture, on a handful of ten units

Project node: **arch_unit_oracle**
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`).
Written 2026-09-10 by the implementer of task rv1, brief
`PRIVATE/PseudoCoupHQ/Research/briefs/task_rv1_brief.md`. the owner,
2026-09-10: *"explore it as an option"*, not a pivot.

Deliverable: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/README.md`
(§2–§5 in full, with every table). Lanes:
`PRIVATE/PseudoCoupHQ/Research/oracle/riscv/lanes_rv1/`. Lane logs on
the tower at
`<runs>/rv1/agent/logs/<stamp>__<lane>.log` — that
is a TOWER path, not a path on this laptop.

---

## 1. What was done and what came of it — the walkthrough, before any figures

The task asked three things of a new architecture. First, whether the ten
units the handful names can be compiled for riscv64 at all and their bodies
read back. Second, whether a RISC-V reference written in our own
reference's shape agrees with the architecture's own published semantics.
Third, how much of the pipeline had to be written again to do it.

I brought up the `rv1` instance on the tower and verified every install the
coordinator had made, each with a one-line probe. The rust riscv64 target
is installed; clang 21 compiles for riscv64; go 1.26 builds for riscv64;
Sail 0.20.2 and the model simulator `sail_riscv_sim` are both there; the
Sail model's own source is mounted. Three tools behaved differently from
the way the brief supposed, and each became a flag rather than a
workaround: `llvm-objdump` has no `--no-aliases` flag, a go riscv64 binary
declares no architecture attributes so its compressed instructions decode
as unknown, and the image carries no riscv64 C library headers so every
probe's `#include <stdint.h>` refused. The third was the only one that
stopped the work, and the remedy — send the include to clang's own
per-target headers — leaves the optimisation level untouched.

With that, all ten units compiled and carved. The bodies are short: nine of
the ten are one computing instruction and a return. That by itself is the
first result — clang and go both reach a single RISC-V instruction where
x86 needed two or three, because x86 has to move a value into the register
its instruction is pinned to and RISC-V does not.

I then wrote the RISC-V reference in the x86 reference's own shape, section
for section, and checked it against the Sail model by running the model's
own simulator over bare-metal programs. Each program loads two inputs from
a table, executes exactly one instruction, stores the result, and loops.
The simulator's signature file gives the results back; the reference's own
term is evaluated at the same inputs by z3. Forty-four instructions,
860,304 points, and the two readings agreed at every point. Nothing had to
be fixed in the reference, because nothing disagreed.

Last, the claim itself: the term read off each unit's riscv64 body against
the term read off its own x86-64 body, at the unit's own answer width.
Seven of the ten pairs are the same term after normalisation. Three differ,
and the three rest on two causes, both of which are real facts about the
two machines rather than errors: the two application binary interfaces
disagree about whether a narrow argument arrives extended to the full
register, and x86's division traps where RISC-V's is defined everywhere.

The surface came to 2,644 lines over five files, of which the reference
alone is 1,174. Nothing outside the task's own folder was written; the term
store, the model table, the attestation, the probe corpus and
`Term.normalize` were all read unchanged, and z3 compared the two
architectures' terms with no new machinery at all.

---

## 2. The installs, verified

Lane `rv1_l1_installs.sh`. Each line below is LITERAL from that lane's log.

| tool | probe | output |
|---|---|---|
| rust riscv64 target | `rustup target list --installed` | `riscv64gc-unknown-none-elf` and `x86_64-unknown-linux-gnu` |
| clang | `clang --version \| head -1` | `Ubuntu clang version 21.1.8 (6ubuntu1)` |
| clang for riscv64 | `clang --target=riscv64-unknown-linux-gnu -O1 -c` on a two-line c function | `rc=0` |
| llvm-objdump | `llvm-objdump --version \| head -2` | `Ubuntu LLVM version 21.1.8` / `Optimized build.` |
| go | `go version` | `go version go1.26.0 linux/amd64` |
| go for riscv64 | `GOARCH=riscv64 GOOS=linux go build` | `rc=0` |
| Sail | `sail --version` | `Sail 0.20.2 (sail @ opam-v2.5.0 0.20.2)` |
| the model simulator | `which sail_riscv_sim` | `/usr/local/bin/sail_riscv_sim` |
| the model's source | `ls /sources/sail-riscv` | `CMakeLists.txt … model … c_emulator … lean_emulator` |
| z3 | `python3 -c 'import z3; print(z3.get_version_string())'` | `z3 5.1.0` |

The simulator's default configuration gives the reset address `0x80000000`
and locates HTIF by the `tohost` symbol; its ISA string begins
`rv64imafdcbvh_zic64b_…_zicond_…` (lane `rv1_l2_sim_shape.sh`), which is
why the Zicond instruction the handful needed is in the model.

Absent, and named rather than worked around: `file`, `llvm-nm`,
`riscv64-linux-gnu-gcc`, `ld.lld` as a standalone binary (clang's
`-fuse-ld=lld` works). None was needed.

---

## 3. The handful — §2 of the brief

Every figure here is in
`PRIVATE/PseudoCoupHQ/Research/oracle/riscv/README.md` §2 as a table,
with the full x86 body beside the full riscv64 body per unit; the artifacts
are `units.json` and `carved.json`. The summary:

- **Ten bodies carved of ten attempted** (lane `rv1_l14_regenerate.sh`).
  Nine are c units through `clang -std=c17 -O1
  --target=riscv64-unknown-linux-gnu -nostdlibinc -c`; one is a go unit
  through `GOARCH=riscv64 GOOS=linux go build`. The optimisation levels are
  the corpus's own.
- **Nine of the brief's ten cells carry a corpus unit.** The `sub`
  immediate-form cell attests none (§6 flag 2), so the tenth compiled body
  is `c/op_102`, the c reading of the same int32 addition the go unit
  carries, on a row of its own.
- **The calling convention, stated:** integer arguments in `a0 .. a7`, the
  integer answer in `a0`; floating-point arguments in `fa0 .. fa7`, the
  floating-point answer in `fa0`; **no flags register**.
- **The instruction vocabulary the ten bodies spell: 15 mnemonics**, of
  which `c.jr` (the return) is 9 of the 24 lines.

The one instance worth putting on this page, because it is the whole result
in three lines — `c/op_210`, source `a / b` on `int32_t`:

> x86-64 ship body: `mov %edi,%eax ; cltd ; idiv %esi ; ret`
> riscv64 ship body: `divw a0, a0, a1 ; c.jr ra`

x86 must park the dividend in the accumulator, spread its sign into the
data register, and then divide the pair; RISC-V's divide reads the two
registers it names.

---

## 4. Level 0 for RISC-V — §3 of the brief

**The headline carries its reading: this is a CHECK AT POINTS, NOT AN
EQUALITY.** 44 instructions, 858 program variants, **860,304 points**, and
the RISC-V reference agreed with the ratified Sail model at every point.
Agreement at 860,304 points is evidence that the two readings compute the
same mapping; it is not a proof.

Lanes `rv1_l7_sail_smoke.sh` (200 points each, 19 instructions, to show the
harness worked), `rv1_l9_sail_full.sh` (42 instructions at 20,000 points)
and `rv1_l10_czero.sh` (the two Zicond instructions). Artifacts
`level0_points.json`, `level0_points_zicond.json`, `sail_smoke.json`. The
per-family table is README §3, Table 2.

**Zero disagreements, so zero defects were found in the reference and no
row had to be fixed.** The brief's instruction — "a disagreement is a
defect in (a), fixed with the row shown" — had nothing to act on.

**What is refused by name rather than counted as agreement: 54 mnemonics.**
`auipc` (its second input is the program counter); the 19 loads, stores,
branches and jumps (their effect is not a value the harness can store from
a register); the 34 floating-point instructions (the brief's §3 names the
base integer set; they are in the reference because the handful's two float
bodies spell them). Each is listed with its cause in `level0_points.json`
under `refused_by_name`.

**The reference's four departures from the x86 file**, each a fact of the
architecture: there is no flags register; every register write is the full
64 bits and the 32-bit forms sign-extend; register `x0` is the constant
zero; division does not trap and every case is defined. README §3(a)
states each with the x86 machinery it replaces.

**Memory.** Bound 6 GB, abort named `ABORT_MEMORY_RV1`, raised by the
driver itself. Peak RSS of the full sweep: **56.4 MB**. The abort was never
raised.

---

## 5. The claim, measured — §4 of the brief

z3 at 3,000 ms, per written place, at the unit's own answer width. Lane
`rv1_l14_regenerate.sh`, artifact `claim.json`. README §4, Table 3 is the
full table; the counts:

| outcome | rows |
|---|---|
| terms identical after `Term.normalize` | 7 |
| equal by z3 but not identical | 0 |
| differ, with a counterexample | 3 |
| undecided at 3,000 ms | 0 |
| no corpus unit at the cell | 1 |

**The three differences, by cause. Two causes, not three.**

**Cause A — the two ABIs disagree about a narrow argument (2 rows, open;
this is a finding, not a defect).** System V on x86-64 leaves the bits above
a narrow argument unspecified, so clang reads only the argument's own
width; the RISC-V psABI requires a narrow argument to arrive extended to
the full register, so clang reads all 64 bits.

- `c/op_498`, `a != b` on `int32_t`, answer width 8.
  x86: `If(Extract(31, 0, v0) == Extract(31, 0, v1), 0, 1)`.
  riscv64: `If(v0 ^ v1 == 0, 0, 1)`.
  Counterexample: `arg0 = 16500306186977935360, arg1 = 0`.
- `c/op_185`, `int64_t * bool`, answer width 64.
  x86: `If(Extract(31, 0, v0) == 0, 0, v1)` — `test %esi,%esi` reads 32
  bits of the `bool` argument's register.
  riscv64: `If(v0 == 0, 0, v1)` — `czero.eqz` reads all 64.
  Counterexample: `arg0 = 18446744073709551607,
  arg1 = 16390304541154738176`.

**Cause B — x86's division is a partial mapping and RISC-V's is total (1
row, open; also a finding).** `c/op_210`, `a / b` on `int32_t`, answer
width 32. `idiv` raises on a zero divisor, so the x86 term says nothing
about that region; `divw` defines the zero divisor as all ones and the
most-negative-over-minus-one overflow as the most negative value.
Counterexample: `arg0 = 2147483648, arg1 = 0`. Both terms are quoted in
full in README §4.

**Two things that look like differences and are not**, each named in
README §4 because they will be asked about: go's int32 addition lowers to a
64-bit `c.add` while clang's lowers to a 32-bit `c.addw`, and at the unit's
own answer width both are the same function; and x86's `cvtsi2ss` writes
one lane of a vector register and keeps the bits above it — so `xmm1` is
recorded as an ARRIVING register on `c/op_105` and `c/op_106` — where
RISC-V has no lanes and `fcvt.s.w` writes the whole register.

**Where the x86 term came from, said plainly.** It is RE-DERIVED by walking
the unit's own recorded ship body with
`PRIVATE/PseudoCoupHQ/Research/op_pipeline/reference.py`, because the
term store holds the term as TEXT and this line has no reader that turns
text back into a z3 object. The store's recorded text is on every row of
`claim.json` as `x86_term_from_the_store` and matched the re-derivation on
9 of the 10 rows; the tenth is §7 flag 3 and is the answer-width reading,
not a disagreement.

---

## 6. The surface, counted — §5 of the brief

Lane `rv1_l14_regenerate.sh`, artifact `surface.json`, counted with
python's own `ast`. README §5 holds Tables 4, 5 and 6.

| layer | file written | total lines | code lines |
|---|---|---|---|
| lifter (the reference) | `riscv_reference.py` | 1,174 | 921 |
| carve | `riscv_carve.py` | 291 | 253 |
| calling convention / canonical form | `claim_check.py` | 326 | 286 |
| attestation | `pick_units.py` | 303 | 263 |
| level 0 check (beside the four the brief names) | `sail_points.py` | 550 | 451 |
| **all five** | **5 files** | **2,644** | **2,174** |

**The answer to "does solving one architecture solve the rest".**

- **What did not transfer: the reading of a body.** 1,174 lines of 2,644 —
  44% of everything written — is the lifter alone. An architecture's
  instruction meanings are its own.
- **What did not transfer: the arrival contract.** The two ABIs' rules for
  a narrow argument differ, and that difference produced two of the three
  disagreements above.
- **What DID transfer, and it is the larger half:** the TERM itself (a z3
  expression over bit vectors is architecture-neutral by construction),
  `Term.normalize` (2,348 lines, called unchanged), the term store (332
  shards), the model table (71,778 rows), the attestation, the probe corpus
  (750 c probes, 744 go probes), and the comparison — z3 decided x86
  against riscv64 with no new machinery at all.

---

## 7. The flags

Each is a flag with its literal output, not a workaround and not a
redesign. Status is on every item.

1. **The image has no riscv64 glibc headers — FIXED, with the optimisation
   level untouched.** LITERAL, lane `rv1_l4_carve_diagnostics.sh`:
   `In file included from /usr/lib/llvm-21/lib/clang/21/include/stdint.h:56:`
   / `/usr/include/stdint.h:26:10: fatal error: 'bits/libc-header-start.h' file not found`
   / `1 error generated.` Ten of ten probes refused. `-nostdlibinc` sends
   the include to clang's own per-target resource headers; ten of ten then
   compiled.
2. **The `sub` immediate-form cell attests no corpus unit — OPEN, and it is
   the brief's own "where one exists".** The probe corpus is (operator ×
   holder pair) and never puts a literal on an operand, so no body spells
   an immediate-form subtract at 64.
3. **`c/op_105`'s store text and the re-derivation differ by the upper
   lane, not by the computation — EXPLAINED.** The store's recorded
   `layer5_normalized_text` is 64 bits (`Concat(Extract(63, 32, v1), <the
   32-bit sum>)`) while the unit's `result_width` is 32, and the comparison
   is at the unit's own answer width as the brief directs. The
   re-derivation is exactly the low 32 bits of the stored term.
4. **One instruction outside RV64I+M is in the reference — RECORDED.**
   `czero.eqz` of the Zicond extension, which clang 21 emits for the
   handful's select; its co-instruction `czero.nez` is beside it. The
   entry carries its cause. Both agree with the Sail model at 20,000
   points each.
5. **Three tool spellings the brief did not foresee — FIXED, each quoted.**
   LITERAL, lane `rv1_l4_carve_diagnostics.sh`:
   `llvm-objdump: error: unknown argument '--no-aliases'` (its own spelling
   is `-M no-aliases`); and `6c730: 952e <unknown>` for a go riscv64 binary
   until `--mattr=+m,+a,+f,+d,+c` names the extensions it does not declare,
   after which the same halfword reads `6c730: 952e c.add a0, a1`.
   `file` is absent from the image and was not needed.
6. **`grep -c exempt` is 0 over every deliverable file and nonzero over
   five lane scripts — REPORTED, not gamed.** LITERAL, lane
   `rv1_l20_final_count.sh`, the final pass:
   `NONZERO 3 rv1_l13_surface_and_guard.sh`, `NONZERO 2 rv1_l15_verify.sh`,
   `NONZERO 2 rv1_l18_verify2.sh`, `NONZERO 2 rv1_l19_verify3.sh`,
   `NONZERO 3 rv1_l20_final_count.sh`, then
   `deliverable files containing the word: 0` and
   `lane scripts containing the word: 5`. Every `.py`, `.json` and `.md`
   in `Research/oracle/riscv/` is 0. The five lanes carry the word because
   each one's job is to RUN that count or that guard, and the word is in
   the command they run. I did not assemble the word from parts to make
   the number read zero.
7. **A new sub-node is WANTED and is the owner's to create, not this task's.**
   `Research/oracle/riscv/` is now a RISC-V line under `arch_unit_oracle`
   with its own reference, its own level-0 oracle and its own carve, and it
   has no planning node.

---

## 8. The guard, and where nothing was written

- **The spelling guard passes on every json this task wrote.** LITERAL,
  lane `rv1_l14_regenerate.sh`:
  `operator inventory: 91 tokens read from probe_manifest_*.json` then
  `PASS units.json`, `PASS carved.json`, `PASS claim.json`,
  `PASS level0_points.json`, `PASS level0_points_zicond.json`,
  `PASS sail_smoke.json`, `PASS surface.json`, `guard rc=0`.
- It did NOT pass on the first attempt: `units.json` and `claim.json` each
  carried 10 findings on a field I had named `display_label`, which is not
  one of the guard's allowed label names. LITERAL, lane
  `rv1_l13_surface_and_guard.sh`:
  `FAIL units.json -- 10 spelling-keyed place(s)` /
  `$.rows[0].display_label` /
  `operator token '+' on a structure field -- this is a grouping/row key, not a per-unit label`.
  The field was renamed to `operator`, which is the guard's own allowed
  name for a display label on a row that also carries `lang` and `unit`,
  and every artifact was regenerated. The guard was not modified.
- **Nothing was written outside `Research/oracle/riscv/`**, the log, and the
  two PROGRESS files the brief names. `reference.py` was READ.
- **Nothing under `PUBLIC/Airlock/` or `<runs>/` was
  deleted**, on either machine.

**The verifier's tally**, from lane `rv1_l18_verify2.sh`, run from this
task's own instance with
`python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_258_task_rv1_riscv_as_a_second_architecture.md`:

| outcome | claims |
|---|---|
| MATCHES | 7 |
| **DIFFERS** | **0** |
| UNVERIFIABLE | 2 |
| REFUSED | 0 |
| NOT_RERUNNABLE | 0 |
| population | 9 claims across 1 log |

Its one line: `7 of 9 claims reproduce; 2 (22%) carry nothing to re-run`.
The two are both prose paragraphs the protocol asks for and that carry no
figure by design: the walkthrough's opening paragraph (§1), which
`order.walkthrough-before-numbers` requires to be prose with no figures in
it, and the "awaiting the owner" bullet (§12), which is a request for a ruling
and not a measurement. Neither was changed to make the tally read better,
and the verifier was not touched.

---

## 9. How to re-run any of it

Every command below is exactly as typed. `$R` is
`bash PUBLIC/Airlock/remote_lane.sh` with
`AIRLOCK_REMOTE=<user>@<tower>` and
`AIRLOCK_REMOTE_ROOT=Programming/Airlock`.

| what | command |
|---|---|
| the instance | `bash PUBLIC/Airlock/remote_lane.sh conf PUBLIC/Airlock/instances/rv1.conf` then `bash PUBLIC/Airlock/remote_lane.sh up --instance rv1` |
| mirror the folder | `bash PUBLIC/Airlock/remote_lane.sh sync-to Programming/PseudoCoupHQ/Research/oracle/riscv` |
| any lane | `bash PUBLIC/Airlock/remote_lane.sh submit --instance rv1 --batch rv1 --weight 1 PRIVATE/PseudoCoupHQ/Research/oracle/riscv/lanes_rv1/<lane>.sh` |
| wait for it | `bash PUBLIC/Airlock/remote_lane.sh wait --instance rv1 <lane>.sh` — repeated, each call at most 100 s |
| bring it back | `bash PUBLIC/Airlock/remote_lane.sh sync-back Programming/PseudoCoupHQ/Research/oracle/riscv` |

Inside a lane, each script is one command per step; the four that produce
the deliverable are, in order:

- `python3 PseudoCoupHQ/Research/oracle/riscv/pick_units.py PseudoCoupHQ/Research/op_pipeline PseudoCoupHQ/Research/oracle/riscv/units.json`
- `python3 PseudoCoupHQ/Research/oracle/riscv/riscv_carve.py PseudoCoupHQ/Research/oracle/riscv/units.json PseudoCoupHQ/Research/oracle/riscv/carved.json /work/rv1carve`
- `python3 PseudoCoupHQ/Research/oracle/riscv/claim_check.py PseudoCoupHQ/Research/op_pipeline PseudoCoupHQ/Research/oracle/riscv/units.json PseudoCoupHQ/Research/oracle/riscv/carved.json PseudoCoupHQ/Research/oracle/riscv/claim`
- `python3 PseudoCoupHQ/Research/oracle/riscv/sail_points.py PseudoCoupHQ/Research/oracle/riscv/level0_points /work/rv1sailfull --points 20000`

---

---

## 10. The claims, each with the command that reproduces it

Every block below is a transcript from lanes `rv1_l16_claim_transcripts.sh`
and `rv1_l17_claim_transcript_fix.sh`, pasted whole and not tidied. Each
command runs INSIDE the `rv1` instance, where this repository is mounted at
`PseudoCoupHQ`.

Level 0 at points — the counts of §4:

```
$ python3 -c "import json; d=json.load(open('PseudoCoupHQ/Research/oracle/riscv/level0_points.json')); e=json.load(open('PseudoCoupHQ/Research/oracle/riscv/level0_points_zicond.json')); r=d['rows']+e['rows']; print('mnemonics', len(r), 'variants', sum(x['variants'] for x in r), 'points', sum(x['points'] for x in r), 'agree', sum(x['agree'] for x in r), 'disagree', sum(x['disagree'] for x in r))"
mnemonics 44 variants 858 points 860304 agree 860304 disagree 0
```

Level 0 — every row's outcome, and the count refused by name:

```
$ python3 -c "import json; d=json.load(open('PseudoCoupHQ/Research/oracle/riscv/level0_points.json')); print('outcomes', sorted(set(x['outcome'] for x in d['rows'])), 'refused by name', len(d['refused_by_name']))"
outcomes ['AGREES_AT_EVERY_POINT'] refused by name 54
```

The claim's tally — the counts of §5:

```
$ python3 -c "import json, collections; d=json.load(open('PseudoCoupHQ/Research/oracle/riscv/claim.json')); print(sorted(collections.Counter(x['outcome'] for x in d['rows']).items()))"
[('DIFFER', 3), ('IDENTICAL_AFTER_NORMALIZE', 7), ('NO_CORPUS_UNIT', 1)]
```

The three counterexamples of §5, as the solver gave them:

```
$ python3 -c "import json; d=json.load(open('PseudoCoupHQ/Research/oracle/riscv/claim.json')); print([(x['unit'], x['answer_width'], sorted(x['counterexample'].items())) for x in d['rows'] if x['outcome']=='DIFFER'])"
[('c/op_210', 32, [('arg0', '2147483648'), ('arg1', '0')]), ('c/op_185', 64, [('arg0', '18446744073709551607'), ('arg1', '16390304541154738176')]), ('c/op_498', 8, [('arg0', '16500306186977935360'), ('arg1', '0')])]
```

The handful — the counts of §3:

```
$ python3 -c "import json; d=json.load(open('PseudoCoupHQ/Research/oracle/riscv/carved.json')); rows=d['rows']; v=set(l.split()[0] for r in rows for l in r.get('body',[])); print('carved', sum(1 for r in rows if r['outcome']=='CARVED'), 'of', len(rows), 'distinct riscv mnemonics', len(v))"
carved 10 of 10 distinct riscv mnemonics 15
```

The surface — the counts of §6:

```
$ python3 -c "import json; d=json.load(open('PseudoCoupHQ/Research/oracle/riscv/surface.json')); print([(r['layer'].split(' (')[0], r['total_lines'], r['code_lines']) for r in d['by_layer']]); print('total', sum(r['total_lines'] for r in d['by_layer']), sum(r['code_lines'] for r in d['by_layer']))"
[('lifter', 1174, 921), ('carve', 291, 253), ('calling convention / canonical form', 326, 286), ('attestation', 303, 263), ('level 0 check', 550, 451)]
total 2644 2174
```

The spelling guard over every json this task wrote — the claim of §8:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/riscv/units.json PseudoCoupHQ/Research/oracle/riscv/carved.json PseudoCoupHQ/Research/oracle/riscv/claim.json PseudoCoupHQ/Research/oracle/riscv/level0_points.json PseudoCoupHQ/Research/oracle/riscv/level0_points_zicond.json PseudoCoupHQ/Research/oracle/riscv/sail_smoke.json PseudoCoupHQ/Research/oracle/riscv/surface.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS units.json -- no operator token in any key, grouping, pairing or row structure
PASS carved.json -- no operator token in any key, grouping, pairing or row structure
PASS claim.json -- no operator token in any key, grouping, pairing or row structure
PASS level0_points.json -- no operator token in any key, grouping, pairing or row structure
PASS level0_points_zicond.json -- no operator token in any key, grouping, pairing or row structure
PASS sail_smoke.json -- no operator token in any key, grouping, pairing or row structure
PASS surface.json -- no operator token in any key, grouping, pairing or row structure
```

---

## 11. Decided, recorded for audit

- **The ten rows are keyed by the machine triple** (`mnem`, operand shape,
  `key_width`) read off the model table's attestation. The source operator
  token rides on the row as `operator`, on a row that also carries `lang`
  and `unit` — the guard's one allowed place — and nothing reads it.
- **Where a cell is attested only in a language with no riscv64 compiler**,
  the row takes the nearest attested c or go unit of the same mnemonic and
  records the cell it actually attests as `attests_cell`. One row does
  this: `cmovne`, whose 32-bit cell is swift-only and whose row carries
  `c/op_185`, a `cmovne` gpr_gpr **64** unit.
- **The tenth compiled body is `c/op_102`**, a row of its own labelled
  `beside_the_ten`, because the `sub` immediate cell attests none. It is
  never folded into a cell it does not attest.
- **The x86 term is re-derived rather than parsed**, and the store's
  recorded text sits beside it on every row (§5 above).
- **The comparison is at the unit's own answer width**, as the brief
  directs.
- **`czero.eqz` and `czero.nez` are in the reference** because a carved body
  spells one of them, which is the x86 table's own rule ("no entry is
  invented for an opcode no body contains"). Both are point-checked.
- **The rounding mode is round-to-nearest-even.** `llvm-objdump` prints
  RISC-V's rounding operand as `dyn`, which defers to `fcsr`, and `fcsr`
  holds round-to-nearest-even at reset; none of the ten bodies writes it.
- **`auipc`, the loads, the stores, the branches, the jumps and the float
  family are refused by name in the point check**, each with its cause, and
  are never counted as agreeing.
- **The instance configuration `rv1.conf`** states the reason for every
  number in its header and is at
  `PUBLIC/Airlock/instances/rv1.conf`.

## 12. Awaiting the owner

- **A planning sub-node for the RISC-V line is wanted.**
  `Research/oracle/riscv/` now holds a second architecture's reference, its
  own level-0 oracle and its own carve, and it has no node. Creating one is
  the owner's, not this task's (brief §6).
- **The two causes of §5 are findings, not defects, and nothing was decided
  about either.** Whether the Hub's dictionary key must carry the arrival
  contract's extension rule — so that a certificate proved on x86 can be
  inherited on riscv64 without re-proving — is the question task rv2 will
  put numbers against, and the ruling is the owner's.
