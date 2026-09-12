# Task bb2 — the bit-blast route on x86-64: every attested arch-opcode, all five compiled languages, beside the native route and the backstop; then the interpreted seven by agreement

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it.
Then `Research/GLOSSARY.md`, `log_267` (bb1: the route on RISC-V, its
sizes and costs, `bitblast.py`, `bb1_run.py`), `log_262` (t4:
`general.py`, the x86 pass over the bank, the arrival contract, the
readings), `log_255` (ap6: the bank's delta and audit), and the
interpreted check (`emulation/interp/interp_check.py`, log of task ex2:
agreement at points, edge values first, ≤20,000 points). Instance
`bb2.conf` (copy `t4.conf`; persist volume for swift). Lanes under
`construct/general/lanes_bb2/`.

## 1. What this is (the owner, 2026-09-12: "then after we can go through the rest of the languages covered by PCHQ")
The bit-blast render of bb1 (`bitblast.py`: z3's circuit, one named
boolean per gate) driven by t4's x86 pass instead of the RISC-V one:
every attested x86 cell (the model table's 253, the population stated
on every row), on c, cpp, rust, go, swift, both the term's own places
and the flags places the bank tracks; the bank's delta and audit as
ever; the three readings.

Then the interpreted seven (cpython, php, ruby, java, javascript, dart,
csharp): no machine body exists, so the route is AGREEMENT — the gate
source rendered in each interpreter's language and run beside the
definition at points (edge values first, ≤20,000), recorded as
`agreed`, never as proved; the count beside ex2's.

## 2. Report
1. x86, population 253 on every row: per language, native / backstop /
   bit-blast / any route, destination-only and strict.
2. the three readings on all four (c rust go swift) beside t4's 96 /
   154 / 141 of 205, and the bank before → after.
3. the interpreted seven: agreed / disagreed / refused, of 253.
4. sizes and seconds as bb1 reported them; NOT_GATED by size counted.
5. swift on riscv64: whether a Swift SDK for riscv64 Linux exists to
   install (a probe, LITERAL), not a guess.
Guard; log; verifier; PROGRESS on the autopoly node and the x86_64
node; sync-back; instance down. Memory bound 6g, abort
`ABORT_MEMORY_BB2`. Nothing under `Research/op_pipeline/`; `bank.py`
only through its existing pass registration.
