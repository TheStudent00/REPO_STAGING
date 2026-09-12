# log 265 — rv6: every RISC-V arch-opcode, both routes, on c, c++, rust and go

Written 2026-09-12 by the coordinator (Fable), who ran it. Lane
`rv6_l2_every_cell_four_languages.sh`, submitted 01:56:32Z, done
02:38:28Z; 1,020 checks in 2,505 s, one process, peak 1,137 MB.
Population: the 255 RISC-V arch-opcodes of the model table, each on c,
cpp, go, rust, both routes (the language's own operator first; the
backstop with every node constructed). Compile routes: rv3's
(`inherit_rv3.install()`: c/cpp with `--gcc-toolchain=/usr`, rust on the
linux-gnu target). Store: `construct/general/rv6_all.jsonl`.

## the table, population 255 on every row
| language | proved | disproved | undecided | refused | of |
|---|---|---|---|---|---|
| c | 242 | 3 | 8 | 2 | 255 |
| c++ | 242 | 3 | 8 | 2 | 255 |
| rust | 246 | 5 | 4 | 0 | 255 |
| go | 238 | 7 | 2 | 8 | 255 |
| proved on at least one of the four | 251 | | | | 255 |
| proved on all four | 231 | | | | 255 |

The backstop route alone (every node built from primitives): c 143,
c++ 143, rust 196, go 183 of 255.

## the four with no proof on any language
`mulh` and `mulhsu` at 64 bits, two operand forms each: the high half of
a 64-by-64 product. c/c++/rust: z3 out of budget on the 128-bit product;
go: no 128-bit integer, the constructed body over the 4,000-instruction
ceiling. A Lean statement of the product's high half is the owed lemma
(`construct/lean/OWED.md` §2).

## beside the earlier rounds
| round | arch-opcodes proved, any language | of |
|---|---|---|
| rv2 + rv3 (untwinned only, c and go) | 117 | 255 |
| rv5 (every cell, c and go) | 244 | 255 |
| rv6 (every cell, four languages) | 251 | 255 |

## flags
- swift: no riscv64 SDK in the image (swift 6.0.3: "could not find
  module '_Concurrency' for target 'riscv64-unknown-linux-gnu'").
- the text-order walk (log_259) still reads a compiled `if` wrong; the
  disproved column is mostly that, per the divide bodies of log_264 and
  the compiled emulation printed in lane `rv7_l1_go_div_body.sh`
  (go dropped its own zero check and its panic call once the zero case
  was handled upstream: 12 instructions, one `div`, three branches).
- bodies are not stored as text in this store (counts only); bb1 stores
  them.
