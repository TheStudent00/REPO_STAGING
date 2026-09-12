# Task rv4 — the round the owner timed: every RISC-V arch-opcode without a proof, the logic filled in from primitives, compiled with optimization OFF, checked; the lane finishes inside ten minutes

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it.
Then `Research/GLOSSARY.md`, `log_262` (t4: `render_general.py`,
`build.py`, `rv_general.py` — the RISC-V driver that ran 188 runs in
168 s at ship flags; REUSE it, do not rewrite it), `log_260` and
`log_259` (rv3, rv2: the RISC-V cells, `twins.json`, the riscv64
compilers and flags, `riscv_reference.py` the lifter), `task_rv3b_brief.md`
(not run; not needed here). Instance `rv4.conf` (copy `rv3.conf`; cpus
8). Artifact folder: `Research/oracle/riscv/`; lanes under `lanes_rv4/`.

## 0. the owner's ruling, 2026-09-11, that this task carries out
"we have the RISC-V official arch-opcode logical definitions. we have
the behavioral mappings of primitive operations in all the languages.
it doesn't take an optimizer. it requires a system to fill in the
logic." And the cause t4 measured for the misses: the compiled body is
checked at SHIPPING optimization, where the compiler rewrites a
gate-level multiplier into another multiplier and z3 cannot decide the
two are equal. The fix is a flag: compile the backstop with optimization
OFF, so the body follows the source one statement at a time and the
check closes by structure. the owner: slower code is fine to start with.

## 1. The round
```
population = every RISC-V cell whose term the lifter states,           # from twins.json / model_table_rv.json
             for each target in (c, go, rust), with NO proved certificate on that target  # rv2, rv3, t4 union
for (cell, target) in population, 8 workers, wall clock 9 minutes hard:
    source = render_general(cell.term, target)          # native operator first, the backstop where the target has none
    body   = carve(compile(source, target, OPTIMIZATION_OFF))
              # clang -O0 --target=riscv64-linux-gnu --gcc-toolchain=/usr
              # go build -gcflags='all=-N -l' GOARCH=riscv64
              # rustc -C opt-level=0 --target riscv64gc-unknown-linux-gnu --emit=obj
    t_body = riscv_reference.walk(body)                  # the lifter, on the register the convention answers in
    if Term.normalize(t_body) == Term.normalize(cell.term): verdict = PROVED_IDENTICAL   # no z3
    else: verdict = z3(t_body == cell.term, 3,000 ms)    # PROVED / DISPROVED / UNDECIDED
    record(cell, target, verdict, instructions(body), seconds)
rows not reached when the clock ends: NOT_REACHED_IN_BUDGET, counted, never silent
```
The lane's own wall clock is the driver's: it reads the clock per run
and stops cleanly at 9 minutes; the lane must show `state=done` inside
10 minutes of its submit. Sample 5 (cell, target) pairs FIRST in a
separate lane, paste peak RSS and seconds per pair, then submit the
round. Memory bound 6g, abort `ABORT_MEMORY_RV4`.

## 2. What to report, and nothing else
1. the population: cells × targets, by the cause they were unproved
   before (refused by name in the lifter: loads/stores/branches/auipc
   are NOT in the population, say how many; floats; integer kinds).
2. per target: proved before → after; PROVED_IDENTICAL / PROVED by z3 /
   DISPROVED / UNDECIDED / REFUSED (cause) / NOT_REACHED; seconds per
   pair, mean and max; instructions per body, mean and max.
3. the union of cells with a proved riscv64 emulation on any target,
   beside 119 of 255; and per target beside rv3's.
4. every DISPROVED with its counterexample (a defect in the lifter or
   the construction; named, not fixed here).
Guard over the json; log (next free number); verifier lane; PROGRESS on
the riscv64 node; sync-back; instance down. `riscv_reference.py`,
`render_general.py`, `build.py` are READ. Never delete anything under
`<runs>/` or `PUBLIC/Airlock/`. Reply with tables
1–4, the lane's submit and done timestamps, every flag LITERAL.
