# task t4 -- the general construction tier, measured

store: `PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/t4_general_runs.jsonl`
proof table: `PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/construction_proofs.json`
store lines: 970; of them, general-tier runs: 304

## 1. per operation kind: constructed, and how each is proved

| operation kind | width | target | places constructed | nodes | proved | by lemma | by z3 | undecided | refused |
|---|---|---|---|---|---|---|---|---|---|
| add | 64 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| add | 64 | swift | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| add | 65 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| add | 65 | swift | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| multiply | 64 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| multiply | 64 | swift | 1 | 2 | 0 | 0 | 0 | 0 | 1 |
| divide unsigned | 128 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| remainder unsigned | 128 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| divide signed | 128 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| remainder signed | 128 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| bitwise over the word | 8 | c | 12 | 12 | 12 | 12 | 0 | 0 | 0 |
| bitwise over the word | 8 | cpp | 12 | 12 | 12 | 12 | 0 | 0 | 0 |
| bitwise over the word | 8 | rust | 12 | 12 | 12 | 12 | 0 | 0 | 0 |
| complement | 8 | c | 6 | 18 | 6 | 6 | 0 | 0 | 0 |
| complement | 8 | cpp | 6 | 18 | 6 | 6 | 0 | 0 | 0 |
| complement | 8 | rust | 6 | 18 | 6 | 6 | 0 | 0 | 0 |
| equality | 1 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| equality | 1 | swift | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| equality | 8 | c | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| equality | 8 | cpp | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| equality | 8 | rust | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| conditional | 8 | c | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| conditional | 8 | cpp | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| conditional | 8 | rust | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| conditional | 64 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| conditional | 64 | swift | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| wiring: widen, narrow, spread the sign, join | 1 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| wiring: widen, narrow, spread the sign, join | 1 | swift | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| wiring: widen, narrow, spread the sign, join | 8 | c | 20 | 32 | 20 | 20 | 0 | 0 | 0 |
| wiring: widen, narrow, spread the sign, join | 8 | cpp | 20 | 32 | 20 | 20 | 0 | 0 | 0 |
| wiring: widen, narrow, spread the sign, join | 8 | rust | 20 | 32 | 20 | 20 | 0 | 0 | 0 |
| wiring: widen, narrow, spread the sign, join | 56 | c | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| wiring: widen, narrow, spread the sign, join | 56 | cpp | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| wiring: widen, narrow, spread the sign, join | 56 | rust | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| wiring: widen, narrow, spread the sign, join | 64 | c | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| wiring: widen, narrow, spread the sign, join | 64 | cpp | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| wiring: widen, narrow, spread the sign, join | 64 | go | 4 | 4 | 0 | 0 | 0 | 0 | 4 |
| wiring: widen, narrow, spread the sign, join | 64 | rust | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| wiring: widen, narrow, spread the sign, join | 65 | go | 1 | 2 | 0 | 0 | 0 | 0 | 1 |
| wiring: widen, narrow, spread the sign, join | 65 | swift | 1 | 2 | 0 | 0 | 0 | 0 | 1 |
| wiring: widen, narrow, spread the sign, join | 128 | go | 4 | 8 | 0 | 0 | 0 | 0 | 4 |

### 1a. the cause on every row that is not proved, LITERAL

| operation kind | width | target | the cause | places |
|---|---|---|---|---|
| add | 64 | go | no cause | 1 |
| add | 64 | swift | the carved body is proved equal to the term the render wrote, and that term's equality with the CELL's own is not discharged by any of the three forms | 1 |
| add | 65 | go | no cause | 1 |
| add | 65 | swift | the carved body is proved equal to the term the render wrote, and that term's equality with the CELL's own is not discharged by any of the three forms | 1 |
| multiply | 64 | go | no cause | 1 |
| multiply | 64 | swift | the carved body is proved equal to the term the render wrote, and that term's equality with the CELL's own is not discharged by any of the three forms | 1 |
| divide unsigned | 128 | go | the carved body is larger than the number of instructions this task's gate is offered: the lift builds one term per instruction and a body of this siz | 1 |
| remainder unsigned | 128 | go | the carved body is larger than the number of instructions this task's gate is offered: the lift builds one term per instruction and a body of this siz | 1 |
| divide signed | 128 | go | the carved body is larger than the number of instructions this task's gate is offered: the lift builds one term per instruction and a body of this siz | 1 |
| remainder signed | 128 | go | the carved body is larger than the number of instructions this task's gate is offered: the lift builds one term per instruction and a body of this siz | 1 |
| equality | 1 | go | no cause | 1 |
| equality | 1 | swift | the carved body is proved equal to the term the render wrote, and that term's equality with the CELL's own is not discharged by any of the three forms | 1 |
| conditional | 64 | go | no cause | 1 |
| conditional | 64 | swift | the carved body is proved equal to the term the render wrote, and that term's equality with the CELL's own is not discharged by any of the three forms | 1 |
| wiring: widen, narrow, spread the sign, join | 1 | go | no cause | 1 |
| wiring: widen, narrow, spread the sign, join | 1 | swift | the carved body is proved equal to the term the render wrote, and that term's equality with the CELL's own is not discharged by any of the three forms | 1 |
| wiring: widen, narrow, spread the sign, join | 64 | go | the carved body is larger than the number of instructions this task's gate is offered: the lift builds one term per instruction and a body of this siz | 4 |
| wiring: widen, narrow, spread the sign, join | 65 | go | no cause | 1 |
| wiring: widen, narrow, spread the sign, join | 65 | swift | the carved body is proved equal to the term the render wrote, and that term's equality with the CELL's own is not discharged by any of the three forms | 1 |
| wiring: widen, narrow, spread the sign, join | 128 | go | the carved body is larger than the number of instructions this task's gate is offered: the lift builds one term per instruction and a body of this siz | 4 |

### 1b. the construction's OWN proof, per (kind, width, word)

| operation kind | width | word | the form of record | outcome | shapes posed | s |
|---|---|---|---|---|---|---|
| add | 8 | 64 | lemma | PROVED | 1 | 0.011 |
| add | 8 | 128 | lemma | PROVED | 1 | 0.011 |
| add | 9 | 64 | lemma | PROVED | 0 | 0.0 |
| add | 9 | 128 | lemma | PROVED | 0 | 0.0 |
| add | 16 | 64 | lemma | PROVED | 0 | 0.0 |
| add | 16 | 128 | lemma | PROVED | 0 | 0.0 |
| add | 32 | 64 | lemma | PROVED | 0 | 0.0 |
| add | 32 | 128 | lemma | PROVED | 0 | 0.0 |
| add | 33 | 64 | lemma | PROVED | 0 | 0.0 |
| add | 33 | 128 | lemma | PROVED | 0 | 0.0 |
| add | 64 | 64 | lemma | PROVED | 0 | 0.0 |
| add | 64 | 128 | lemma | PROVED | 0 | 0.0 |
| add | 65 | 64 | lemma | PROVED | 0 | 0.0 |
| add | 65 | 128 | lemma | PROVED | 0 | 0.0 |
| subtract | 8 | 64 | lemma | PROVED | 0 | 0.0 |
| subtract | 8 | 128 | lemma | PROVED | 0 | 0.0 |
| subtract | 9 | 64 | lemma | PROVED | 0 | 0.0 |
| subtract | 9 | 128 | lemma | PROVED | 0 | 0.0 |
| subtract | 16 | 64 | lemma | PROVED | 0 | 0.0 |
| subtract | 16 | 128 | lemma | PROVED | 0 | 0.0 |
| subtract | 32 | 64 | lemma | PROVED | 0 | 0.0 |
| subtract | 32 | 128 | lemma | PROVED | 0 | 0.0 |
| subtract | 33 | 64 | lemma | PROVED | 0 | 0.0 |
| subtract | 33 | 128 | lemma | PROVED | 0 | 0.0 |
| subtract | 64 | 64 | lemma | PROVED | 0 | 0.0 |
| subtract | 64 | 128 | lemma | PROVED | 0 | 0.0 |
| subtract | 65 | 64 | lemma | PROVED | 0 | 0.0 |
| subtract | 65 | 128 | lemma | PROVED | 0 | 0.0 |
| negate | 8 | 64 | lemma | PROVED | 0 | 0.0 |
| negate | 8 | 128 | lemma | PROVED | 0 | 0.0 |
| negate | 16 | 64 | lemma | PROVED | 0 | 0.0 |
| negate | 16 | 128 | lemma | PROVED | 0 | 0.0 |
| negate | 32 | 64 | lemma | PROVED | 0 | 0.0 |
| negate | 32 | 128 | lemma | PROVED | 0 | 0.0 |
| negate | 64 | 64 | lemma | PROVED | 0 | 0.0 |
| negate | 64 | 128 | lemma | PROVED | 0 | 0.0 |
| multiply | 16 | 64 | -- | UNDECIDED | 1 | 30.051 |
| multiply | 16 | 128 | -- | UNDECIDED | 1 | 30.051 |
| multiply | 32 | 64 | -- | UNDECIDED | 1 | 30.423 |
| multiply | 32 | 128 | -- | UNDECIDED | 1 | 30.423 |
| multiply | 64 | 64 | -- | UNDECIDED | 1 | 32.461 |
| multiply | 64 | 128 | -- | UNDECIDED | 1 | 32.461 |
| multiply | 128 | 64 | -- | UNDECIDED | 1 | 129.975 |
| multiply | 128 | 128 | -- | UNDECIDED | 2 | 439.573 |
| divide unsigned | 16 | 64 | -- | UNDECIDED | 1 | 31.137 |
| divide unsigned | 16 | 128 | -- | UNDECIDED | 1 | 31.137 |
| divide unsigned | 32 | 64 | -- | UNDECIDED | 1 | 106.638 |
| divide unsigned | 32 | 128 | -- | UNDECIDED | 1 | 106.638 |
| divide unsigned | 64 | 64 | -- | UNDECIDED | 1 | 1542.784 |
| divide unsigned | 64 | 128 | -- | UNDECIDED | 1 | 1542.784 |
| divide unsigned | 128 | 64 | -- | UNDECIDED | 1 | 1474.09 |
| divide unsigned | 128 | 128 | -- | UNDECIDED | 1 | 1556.813 |
| remainder unsigned | 16 | 64 | -- | UNDECIDED | 1 | 30.996 |
| remainder unsigned | 16 | 128 | -- | UNDECIDED | 1 | 30.996 |
| remainder unsigned | 32 | 64 | -- | UNDECIDED | 1 | 261.364 |
| remainder unsigned | 32 | 128 | -- | UNDECIDED | 1 | 261.364 |
| remainder unsigned | 64 | 64 | -- | UNDECIDED | 1 | 1047.892 |
| remainder unsigned | 64 | 128 | -- | UNDECIDED | 1 | 1047.892 |
| remainder unsigned | 128 | 64 | -- | UNDECIDED | 1 | 937.37 |
| remainder unsigned | 128 | 128 | -- | UNDECIDED | 1 | 1345.92 |
| divide signed | 16 | 64 | -- | UNDECIDED | 1 | 30.857 |
| divide signed | 16 | 128 | -- | UNDECIDED | 1 | 30.857 |
| divide signed | 32 | 64 | -- | UNDECIDED | 1 | 97.601 |
| divide signed | 32 | 128 | -- | UNDECIDED | 1 | 97.601 |
| divide signed | 64 | 64 | -- | LEAN_REFUSED | 0 | 0.0 |
| divide signed | 64 | 128 | -- | LEAN_REFUSED | 0 | 0.0 |
| divide signed | 128 | 64 | -- | LEAN_REFUSED | 0 | 0.0 |
| divide signed | 128 | 128 | -- | LEAN_REFUSED | 0 | 0.0 |
| remainder signed | 16 | 64 | -- | UNDECIDED | 1 | 30.935 |
| remainder signed | 16 | 128 | -- | UNDECIDED | 1 | 30.935 |
| remainder signed | 32 | 64 | -- | UNDECIDED | 1 | 221.306 |
| remainder signed | 32 | 128 | -- | UNDECIDED | 1 | 221.306 |
| remainder signed | 64 | 64 | -- | LEAN_REFUSED | 0 | 0.0 |
| remainder signed | 64 | 128 | -- | LEAN_REFUSED | 0 | 0.0 |
| remainder signed | 128 | 64 | -- | LEAN_REFUSED | 0 | 0.0 |
| remainder signed | 128 | 128 | -- | LEAN_REFUSED | 0 | 0.0 |
| shift left | 8 | 64 | lemma | PROVED | 0 | 0.0 |
| shift left | 8 | 128 | lemma | PROVED | 0 | 0.0 |
| shift left | 32 | 64 | lemma | PROVED | 0 | 0.0 |
| shift left | 32 | 128 | lemma | PROVED | 0 | 0.0 |
| shift left | 64 | 64 | lemma | PROVED | 0 | 0.0 |
| shift left | 64 | 128 | lemma | PROVED | 0 | 0.0 |
| shift left | 128 | 64 | lemma | PROVED | 1 | 2.045 |
| shift left | 128 | 128 | lemma | PROVED | 0 | 0.0 |
| shift right logical | 8 | 64 | lemma | PROVED | 0 | 0.0 |
| shift right logical | 8 | 128 | lemma | PROVED | 0 | 0.0 |
| shift right logical | 16 | 64 | lemma | PROVED | 0 | 0.0 |
| shift right logical | 16 | 128 | lemma | PROVED | 0 | 0.0 |
| shift right logical | 32 | 64 | lemma | PROVED | 0 | 0.0 |
| shift right logical | 32 | 128 | lemma | PROVED | 0 | 0.0 |
| shift right logical | 64 | 64 | lemma | PROVED | 0 | 0.0 |
| shift right logical | 64 | 128 | lemma | PROVED | 0 | 0.0 |
| shift right logical | 128 | 64 | lemma | PROVED | 0 | 0.0 |
| shift right logical | 128 | 128 | lemma | PROVED | 0 | 0.0 |
| shift right arithmetic | 8 | 64 | lemma | PROVED | 0 | 0.0 |
| shift right arithmetic | 8 | 128 | lemma | PROVED | 0 | 0.0 |
| shift right arithmetic | 16 | 64 | lemma | PROVED | 0 | 0.0 |
| shift right arithmetic | 16 | 128 | lemma | PROVED | 0 | 0.0 |
| shift right arithmetic | 32 | 64 | lemma | PROVED | 0 | 0.0 |
| shift right arithmetic | 32 | 128 | lemma | PROVED | 0 | 0.0 |
| shift right arithmetic | 64 | 64 | lemma | PROVED | 0 | 0.0 |
| shift right arithmetic | 64 | 128 | lemma | PROVED | 0 | 0.0 |
| bitwise over the word | 1 | 64 | lemma | PROVED | 0 | 0.0 |
| bitwise over the word | 1 | 128 | lemma | PROVED | 0 | 0.0 |
| bitwise over the word | 8 | 64 | lemma | PROVED | 0 | 0.0 |
| bitwise over the word | 8 | 128 | lemma | PROVED | 0 | 0.0 |
| bitwise over the word | 16 | 64 | lemma | PROVED | 0 | 0.0 |
| bitwise over the word | 16 | 128 | lemma | PROVED | 0 | 0.0 |
| bitwise over the word | 32 | 64 | lemma | PROVED | 0 | 0.0 |
| bitwise over the word | 32 | 128 | lemma | PROVED | 0 | 0.0 |
| bitwise over the word | 64 | 64 | lemma | PROVED | 0 | 0.0 |
| bitwise over the word | 64 | 128 | lemma | PROVED | 0 | 0.0 |
| complement | 1 | 64 | lemma | PROVED | 0 | 0.0 |
| complement | 1 | 128 | lemma | PROVED | 0 | 0.0 |
| complement | 8 | 64 | lemma | PROVED | 0 | 0.0 |
| complement | 8 | 128 | lemma | PROVED | 0 | 0.0 |
| complement | 32 | 64 | lemma | PROVED | 0 | 0.0 |
| complement | 32 | 128 | lemma | PROVED | 0 | 0.0 |
| complement | 64 | 64 | lemma | PROVED | 0 | 0.0 |
| complement | 64 | 128 | lemma | PROVED | 0 | 0.0 |
| compare unsigned | 8 | 64 | lemma | PROVED | 0 | 0.0 |
| compare unsigned | 8 | 128 | lemma | PROVED | 0 | 0.0 |
| compare unsigned | 32 | 64 | lemma | PROVED | 0 | 0.0 |
| compare unsigned | 32 | 128 | lemma | PROVED | 0 | 0.0 |
| compare unsigned | 64 | 64 | lemma | PROVED | 0 | 0.0 |
| compare unsigned | 64 | 128 | lemma | PROVED | 0 | 0.0 |
| compare signed | 64 | 64 | lemma | PROVED | 4 | 0.447 |
| compare signed | 64 | 128 | lemma | PROVED | 4 | 0.447 |
| equality | 1 | 64 | lemma | PROVED | 0 | 0.0 |
| equality | 1 | 128 | lemma | PROVED | 0 | 0.0 |
| equality | 8 | 64 | lemma | PROVED | 0 | 0.0 |
| equality | 8 | 128 | lemma | PROVED | 0 | 0.0 |
| equality | 32 | 64 | lemma | PROVED | 0 | 0.0 |
| equality | 32 | 128 | lemma | PROVED | 0 | 0.0 |
| equality | 64 | 64 | lemma | PROVED | 0 | 0.0 |
| equality | 64 | 128 | lemma | PROVED | 0 | 0.0 |
| conditional | 8 | 64 | lemma | PROVED | 0 | 0.0 |
| conditional | 8 | 128 | lemma | PROVED | 0 | 0.0 |
| conditional | 32 | 64 | lemma | PROVED | 0 | 0.0 |
| conditional | 32 | 128 | lemma | PROVED | 0 | 0.0 |
| conditional | 64 | 64 | lemma | PROVED | 0 | 0.0 |
| conditional | 64 | 128 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 1 | 64 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 1 | 128 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 2 | 64 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 2 | 128 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 8 | 64 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 8 | 128 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 9 | 64 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 9 | 128 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 15 | 64 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 15 | 128 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 16 | 64 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 16 | 128 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 32 | 64 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 32 | 128 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 33 | 64 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 33 | 128 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 48 | 64 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 48 | 128 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 56 | 64 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 56 | 128 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 64 | 64 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 64 | 128 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 65 | 64 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 65 | 128 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 94 | 64 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 94 | 128 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 96 | 64 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 96 | 128 | lemma | PROVED | 6 | 0.004 |
| wiring: widen, narrow, spread the sign, join | 128 | 64 | lemma | PROVED | 0 | 0.0 |
| wiring: widen, narrow, spread the sign, join | 128 | 128 | lemma | PROVED | 0 | 0.0 |
| float arithmetic | 32 | 64 | -- | UNDECIDED | 4 | 2977.221 |
| float arithmetic | 32 | 128 | -- | UNDECIDED | 4 | 2977.221 |
| float arithmetic | 64 | 64 | -- | UNDECIDED | 4 | 1790.416 |
| float arithmetic | 64 | 128 | -- | UNDECIDED | 4 | 1790.416 |
| float arithmetic | 79 | 64 | -- | REFUSED_BEFORE_LEAN | 0 | 0.0 |
| float arithmetic | 79 | 128 | -- | REFUSED_BEFORE_LEAN | 0 | 0.0 |
| float compare | 32 | 64 | -- | REFUSED_BEFORE_LEAN | 0 | 0.0 |
| float compare | 32 | 128 | -- | REFUSED_BEFORE_LEAN | 0 | 0.0 |
| float compare | 64 | 64 | sat | PROVED | 5 | 0.235 |
| float compare | 64 | 128 | sat | PROVED | 5 | 0.235 |
| float class | 32 | 64 | sat | PROVED | 5 | 0.028 |
| float class | 32 | 128 | sat | PROVED | 5 | 0.028 |
| float class | 64 | 64 | -- | REFUSED_BEFORE_LEAN | 0 | 0.0 |
| float class | 64 | 128 | -- | REFUSED_BEFORE_LEAN | 0 | 0.0 |
| float convert | 32 | 64 | -- | REFUSED_BEFORE_LEAN | 0 | 0.0 |
| float convert | 32 | 128 | -- | REFUSED_BEFORE_LEAN | 0 | 0.0 |
| float convert | 64 | 64 | -- | REFUSED_BEFORE_LEAN | 0 | 0.0 |
| float convert | 64 | 128 | -- | REFUSED_BEFORE_LEAN | 0 | 0.0 |
| float wiring | 32 | 64 | sat | PROVED | 2 | 0.01 |
| float wiring | 32 | 128 | sat | PROVED | 2 | 0.01 |
| float wiring | 64 | 64 | sat | PROVED | 2 | 0.01 |
| float wiring | 64 | 128 | sat | PROVED | 2 | 0.01 |
| float wiring | 79 | 64 | -- | REFUSED_BEFORE_LEAN | 0 | 0.0 |
| float wiring | 79 | 128 | -- | REFUSED_BEFORE_LEAN | 0 | 0.0 |

## 2. where the tier declined, by cause, LITERAL

| target | the cause | places |
|---|---|---|
| c | the native route did not reach this place's term at all, so the tier has nothing to render | 72 |
| cpp | the native route did not reach this place's term at all, so the tier has nothing to render | 72 |
| rust | the native route did not reach this place's term at all, so the tier has nothing to render | 58 |
| swift | the native route did not reach this place's term at all, so the tier has nothing to render | 37 |
| c | the native route proved this place, so there is nothing the general tier can add | 9 |
| swift | the native route proved this place, so there is nothing the general tier can add | 9 |
| cpp | the native route proved this place, so there is nothing the general tier can add | 9 |
| rust | the native route proved this place, so there is nothing the general tier can add | 7 |
| go | the native route proved this place, so there is nothing the general tier can add | 7 |

| target | the gate's own outcome | places |
|---|---|---|
| c | DISPROVED | 58 |
| cpp | DISPROVED | 58 |
| rust | DISPROVED | 47 |
| c | PROVED_ON_SHIP | 28 |
| cpp | PROVED_ON_SHIP | 28 |
| rust | PROVED_ON_SHIP | 28 |
| swift | UNDECIDED | 27 |
| swift | DISPROVED | 16 |
| swift | PROVED_ON_SHIP | 10 |
| go | PROVED_ON_SHIP | 8 |
| c | UNDECIDED | 8 |
| cpp | UNDECIDED | 5 |
| go | UNDECIDED | 5 |
| go | the carved body is larger than the number of instructions this task's gate is offered: the lift builds one term per inst | 4 |
| rust | UNDECIDED | 4 |
| go | no verdict | 1 |
| swift | the carved body is proved equal to the term the render wrote, and that term's equality with the CELL's own is not discha | 1 |

| target | the equality's form | its outcome | places |
|---|---|---|---|
| c | canonical | PROVED | 74 |
| cpp | canonical | PROVED | 71 |
| rust | canonical | PROVED | 59 |
| swift | canonical | PROVED | 53 |
| c | kind | PROVED | 20 |
| cpp | kind | PROVED | 20 |
| rust | kind | PROVED | 20 |
| go | canonical | PROVED | 13 |
| go | -- | -- | 5 |
| swift | -- | UNDECIDED | 1 |

## 3. the collapse column per constructed certificate

| target | landing | places | instructions, summed | instructions, mean |
|---|---|---|---|---|
| c | LANDED | 6 | 17 | 2.8 |
| c | LANDED_ELSEWHERE | 3 | 6 | 2.0 |
| c | NOT_COLLAPSED | 85 | 1116 | 13.1 |
| cpp | LANDED | 6 | 17 | 2.8 |
| cpp | LANDED_ELSEWHERE | 2 | 4 | 2.0 |
| cpp | NOT_COLLAPSED | 83 | 1108 | 13.3 |
| go | IDENTITY | 2 | 2 | 1.0 |
| go | LANDED | 5 | 10 | 2.0 |
| go | LANDED_ELSEWHERE | 2 | 4 | 2.0 |
| go | NO LANDING RECORDED | 1 | 0 | 0.0 |
| go | NOT_COLLAPSED | 8 | 154395 | 19299.4 |
| rust | LANDED | 6 | 17 | 2.8 |
| rust | LANDED_ELSEWHERE | 2 | 4 | 2.0 |
| rust | NOT_COLLAPSED | 71 | 1118 | 15.7 |
| swift | LANDED | 4 | 11 | 2.8 |
| swift | LANDED_ELSEWHERE | 28 | 31 | 1.1 |
| swift | NOT_COLLAPSED | 22 | 130 | 5.9 |

## 4. the gate's cost where it runs out

| operation kind | width | word | outcome | the form actually used | s |
|---|---|---|---|---|---|
| multiply | 16 | 64 | UNDECIDED | none | 30.051 |
| multiply | 16 | 128 | UNDECIDED | none | 30.051 |
| multiply | 32 | 64 | UNDECIDED | none | 30.423 |
| multiply | 32 | 128 | UNDECIDED | none | 30.423 |
| multiply | 64 | 64 | UNDECIDED | none | 32.461 |
| multiply | 64 | 128 | UNDECIDED | none | 32.461 |
| multiply | 128 | 64 | UNDECIDED | none | 129.975 |
| multiply | 128 | 128 | UNDECIDED | none | 439.573 |
| divide unsigned | 16 | 64 | UNDECIDED | none | 31.137 |
| divide unsigned | 16 | 128 | UNDECIDED | none | 31.137 |
| divide unsigned | 32 | 64 | UNDECIDED | none | 106.638 |
| divide unsigned | 32 | 128 | UNDECIDED | none | 106.638 |
| divide unsigned | 64 | 64 | UNDECIDED | none | 1542.784 |
| divide unsigned | 64 | 128 | UNDECIDED | none | 1542.784 |
| divide unsigned | 128 | 64 | UNDECIDED | none | 1474.09 |
| divide unsigned | 128 | 128 | UNDECIDED | none | 1556.813 |
| remainder unsigned | 16 | 64 | UNDECIDED | none | 30.996 |
| remainder unsigned | 16 | 128 | UNDECIDED | none | 30.996 |
| remainder unsigned | 32 | 64 | UNDECIDED | none | 261.364 |
| remainder unsigned | 32 | 128 | UNDECIDED | none | 261.364 |
| remainder unsigned | 64 | 64 | UNDECIDED | none | 1047.892 |
| remainder unsigned | 64 | 128 | UNDECIDED | none | 1047.892 |
| remainder unsigned | 128 | 64 | UNDECIDED | none | 937.37 |
| remainder unsigned | 128 | 128 | UNDECIDED | none | 1345.92 |
| divide signed | 16 | 64 | UNDECIDED | none | 30.857 |
| divide signed | 16 | 128 | UNDECIDED | none | 30.857 |
| divide signed | 32 | 64 | UNDECIDED | none | 97.601 |
| divide signed | 32 | 128 | UNDECIDED | none | 97.601 |
| divide signed | 64 | 64 | LEAN_REFUSED | none | 0.0 |
| divide signed | 64 | 128 | LEAN_REFUSED | none | 0.0 |
| divide signed | 128 | 64 | LEAN_REFUSED | none | 0.0 |
| divide signed | 128 | 128 | LEAN_REFUSED | none | 0.0 |
| remainder signed | 16 | 64 | UNDECIDED | none | 30.935 |
| remainder signed | 16 | 128 | UNDECIDED | none | 30.935 |
| remainder signed | 32 | 64 | UNDECIDED | none | 221.306 |
| remainder signed | 32 | 128 | UNDECIDED | none | 221.306 |
| remainder signed | 64 | 64 | LEAN_REFUSED | none | 0.0 |
| remainder signed | 64 | 128 | LEAN_REFUSED | none | 0.0 |
| remainder signed | 128 | 64 | LEAN_REFUSED | none | 0.0 |
| remainder signed | 128 | 128 | LEAN_REFUSED | none | 0.0 |
| float arithmetic | 32 | 64 | UNDECIDED | none | 2977.221 |
| float arithmetic | 32 | 128 | UNDECIDED | none | 2977.221 |
| float arithmetic | 64 | 64 | UNDECIDED | none | 1790.416 |
| float arithmetic | 64 | 128 | UNDECIDED | none | 1790.416 |
| float arithmetic | 79 | 64 | REFUSED_BEFORE_LEAN | none | 0.0 |
| float arithmetic | 79 | 128 | REFUSED_BEFORE_LEAN | none | 0.0 |
| float compare | 32 | 64 | REFUSED_BEFORE_LEAN | none | 0.0 |
| float compare | 32 | 128 | REFUSED_BEFORE_LEAN | none | 0.0 |
| float class | 64 | 64 | REFUSED_BEFORE_LEAN | none | 0.0 |
| float class | 64 | 128 | REFUSED_BEFORE_LEAN | none | 0.0 |
| float convert | 32 | 64 | REFUSED_BEFORE_LEAN | none | 0.0 |
| float convert | 32 | 128 | REFUSED_BEFORE_LEAN | none | 0.0 |
| float convert | 64 | 64 | REFUSED_BEFORE_LEAN | none | 0.0 |
| float convert | 64 | 128 | REFUSED_BEFORE_LEAN | none | 0.0 |
| float wiring | 79 | 64 | REFUSED_BEFORE_LEAN | none | 0.0 |
| float wiring | 79 | 128 | REFUSED_BEFORE_LEAN | none | 0.0 |

| target | places CONSTRUCTED, COMPILED and CARVED but not gated |
|---|---|
| go | 4 |
| swift | 1 |

## 5. the size of the constructed sources

| target | policy | places | statements, summed | statements, mean | the largest | instructions, summed |
|---|---|---|---|---|---|---|
| c | all_constructed | 20 | 362 | 18.1 | 21 | 290 |
| c | native_first | 74 | 671 | 9.1 | 22 | 849 |
| cpp | all_constructed | 20 | 362 | 18.1 | 21 | 290 |
| cpp | native_first | 71 | 667 | 9.4 | 22 | 839 |
| go | native_first | 18 | 112156 | 6230.9 | 27642 | 154411 |
| rust | all_constructed | 20 | 362 | 18.1 | 21 | 290 |
| rust | native_first | 59 | 429 | 7.3 | 19 | 849 |
| swift | all_constructed | 1 | 4727 | 4727.0 | 4727 | 1 |
| swift | native_first | 53 | 491 | 9.3 | 31 | 171 |

| operation kind | width | target | places | statements, summed | the largest |
|---|---|---|---|---|---|
| add | 64 | go | 1 | 2553 | 2553 |
| add | 64 | swift | 1 | 4727 | 4727 |
| add | 65 | go | 1 | 2553 | 2553 |
| add | 65 | swift | 1 | 4727 | 4727 |
| multiply | 64 | go | 1 | 2553 | 2553 |
| multiply | 64 | swift | 1 | 4727 | 4727 |
| divide unsigned | 128 | go | 1 | 27322 | 27322 |
| remainder unsigned | 128 | go | 1 | 27142 | 27142 |
| divide signed | 128 | go | 1 | 27642 | 27642 |
| remainder signed | 128 | go | 1 | 27461 | 27461 |
| bitwise over the word | 8 | c | 12 | 234 | 21 |
| bitwise over the word | 8 | cpp | 12 | 234 | 21 |
| bitwise over the word | 8 | rust | 12 | 234 | 21 |
| complement | 8 | c | 6 | 126 | 21 |
| complement | 8 | cpp | 6 | 126 | 21 |
| complement | 8 | rust | 6 | 126 | 21 |
| equality | 1 | go | 1 | 2553 | 2553 |
| equality | 1 | swift | 1 | 4727 | 4727 |
| equality | 8 | c | 20 | 362 | 21 |
| equality | 8 | cpp | 20 | 362 | 21 |
| equality | 8 | rust | 20 | 362 | 21 |
| conditional | 8 | c | 20 | 362 | 21 |
| conditional | 8 | cpp | 20 | 362 | 21 |
| conditional | 8 | rust | 20 | 362 | 21 |
| conditional | 64 | go | 1 | 2553 | 2553 |
| conditional | 64 | swift | 1 | 4727 | 4727 |
| wiring: widen, narrow, spread the sign, join | 1 | go | 1 | 2553 | 2553 |
| wiring: widen, narrow, spread the sign, join | 1 | swift | 1 | 4727 | 4727 |
| wiring: widen, narrow, spread the sign, join | 8 | c | 20 | 362 | 21 |
| wiring: widen, narrow, spread the sign, join | 8 | cpp | 20 | 362 | 21 |
| wiring: widen, narrow, spread the sign, join | 8 | rust | 20 | 362 | 21 |
| wiring: widen, narrow, spread the sign, join | 56 | c | 20 | 362 | 21 |
| wiring: widen, narrow, spread the sign, join | 56 | cpp | 20 | 362 | 21 |
| wiring: widen, narrow, spread the sign, join | 56 | rust | 20 | 362 | 21 |
| wiring: widen, narrow, spread the sign, join | 64 | c | 20 | 362 | 21 |
| wiring: widen, narrow, spread the sign, join | 64 | cpp | 20 | 362 | 21 |
| wiring: widen, narrow, spread the sign, join | 64 | go | 4 | 109567 | 27642 |
| wiring: widen, narrow, spread the sign, join | 64 | rust | 20 | 362 | 21 |
| wiring: widen, narrow, spread the sign, join | 65 | go | 1 | 2553 | 2553 |
| wiring: widen, narrow, spread the sign, join | 65 | swift | 1 | 4727 | 4727 |
| wiring: widen, narrow, spread the sign, join | 128 | go | 4 | 109567 | 27642 |

peak resident: 118544 kB
