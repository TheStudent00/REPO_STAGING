# log 286 — the walk: how an arch-unit is expressed in Lean

2026-09-15. the owner, on the paragraph that began "What the walk does: it
reads an arch-unit one arch-opcode at a time, in address order,
applying Sail's definition of each to a set of registers that starts
as the argument registers": "idu what youre saying. try again please.
please read comms protocol and verify that youve read it."

This is the second try, written after reading the comms protocol in
full (`PRIVATE/DevComms/comms_protocol.md`, until today
named `LLM_communication_protocol.md`). The first try broke five of its
cards:

| card | what it asks | where the first try broke it |
|---|---|---|
| `names.what-is-it-first` | the first sentence places the thing between the things it sits between | it said what the walk does, never that it sits between an arch-unit and its Lean expression |
| `object.instance-before-mechanism` | real rows of real data before the rule | no arch-unit was shown |
| `object.machine-state-stepped` | the registers on the page, values changing per instruction | no register had a value |
| `names.sets-and-loops` | a process is a loop in a code block over declared names | the process was a paragraph |
| `shape.plain-words-loudly-defined` | every word declared before it is used | "our reader", "argument registers", "register number" were used cold |

## 1. walkthrough

The walk is how an arch-unit gets expressed in Lean. It takes the
arch-unit's arch-opcodes in the order the compiler wrote them. For each
one, it writes Sail's definition of that arch-opcode over what the
registers held just before it, and stores the result in the register
the arch-opcode writes. At the return, the register that carries a
function's answer holds one Lean expression made only of Sail's
definitions: the arch-unit expressed in Lean. Lean then checks that
expression by running Sail's own `execute` over the same instructions.
The walk stops, with no expression, at three places. All three are
limits of our code, not of Sail.

## 2. names

`register table`
- for each register, what it holds, written as a Lean expression over the function's inputs.
- if we take an empty table and write the letter a in x10 (where a function receives its first input), b in x11 (its second), c in x12, d in x13, and 0 in x0 (the register that is always zero), that is the table every walk starts from.

`pure form`
- Sail's definition of one arch-opcode, with each register it reads turned into an input: `pure_RTYPE a b XOR` is Sail's definition RTYPE, with operation XOR, applied to the values a and b.
- built by `strip` (below).

`strip`
- our code that turns Sail's Lean text for one arch-opcode into its pure form.
- it knows one shape: read some registers, compute one value, write one register, retire. A definition in any other shape gets no pure form.

`the walk`
- if we take the register table at its start, then for each arch-opcode of the arch-unit (the return excepted) look up its pure form, fill the pure form's inputs from the table, and write the result into the table under the register the arch-opcode writes, then what x10 holds at the return is the arch-unit expressed in Lean.
- code: `compose` in `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/leanpath/walk.py`.

## 3. one arch-unit, walked

Block A — LITERAL, the compiler-operator: c's `==` on `int64_t` and
`uint64_t`, `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/handful_c/corpus/c__op_470.c`

```c
__typeof__((int64_t){0} == (uint64_t){0})
op_470(int64_t a, uint64_t b)
{
    return a == b;
}
```

Table 1 — LITERAL, its arch-unit, as the disassembler printed it (row
`c__op_470` of `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/handful_c/walk_2/walk.json`)

| word | arch-opcode |
|---|---|
| `8d2d` | `c.xor a0, a1` |
| `00153513` | `sltiu a0, a0, 0x1` |
| `8082` | `c.jr ra` (the return) |

Block B — LITERAL, Sail's definitions of the two arch-opcodes, as
`strip` reads them from Sail's Lean emit
(`PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/LeanIM/`);
`v_rs1` and `v_rs2` are the values read from the two registers

```
RTYPE   | .XOR   => (v_rs1 ^^^ v_rs2)
ITYPE   let immext : xlenbits := (sign_extend (m := 64) imm)
        | .SLTIU => (zero_extend (m := 64) (bool_to_bit (zopz0zI_u v_rs1 immext)))
```

GLOSS, beside Block B: XOR gives the first value xor the second. SLTIU
gives 1 when the value is below the sign-extended constant, compared as
unsigned numbers (`zopz0zI_u` is Sail's unsigned less-than), and 0
otherwise.

Table 2 — the register table after each arch-opcode. The two right
columns put illustrative values into a and b, to watch them move.

| step | arch-opcode | x10 holds, as a Lean expression | x11 holds | x10 with a = 5, b = 5 | x10 with a = 5, b = 7 |
|---|---|---|---|---|---|
| start | | `a` | `b` | 5 | 5 |
| 1 | `c.xor a0, a1` | `pure_RTYPE a b XOR` | `b` | 0 | 2 |
| 2 | `sltiu a0, a0, 0x1` | `pure_ITYPE (pure_RTYPE a b XOR) 1 SLTIU` | `b` | 1 | 0 |
| return | `c.jr ra` | the answer | | 1: equal | 0: not equal |

- Step 1 read x10 and x11 from the table and wrote Sail's XOR over what they held into x10.
- Step 2 read x10, which now holds step 1's expression, and wrote Sail's SLTIU over that whole expression into x10.
- At the return, x10 holds the arch-unit expressed in Lean.

Block C — LITERAL, what the walk stored for this arch-unit

```
(pure_ITYPE ((pure_RTYPE (a) (b) (XOR))) (0x001#12) (LeanIM.iop.SLTIU))
```

GLOSS: 1 when (a xor b) is below 1, which is when a xor b is 0, which is
when a equals b.

Then Lean checks it: Lean runs Sail's own `execute` over the same two
instruction words, from a state where x10 holds a and x11 holds b, and
proves x10 ends up holding Block C. The walk wrote the expression; Lean
certifies it.

## 4. the walk, as code

Block D — the loop `compose` runs (the real code is in `walk.py`; this
is its shape, with the three places it stops marked)

```python
def walk(arch_unit):
    table = {x0: 0, x10: a, x11: b, x12: c, x13: d}      # the inputs, as letters
    for word in arch_unit.words[:-1]:                    # the last word is the return
        instruction = sail_decoder(word)                 # Sail's own decoder: which arch-opcode, which registers
        pure_form = strip(instruction)                   # Sail's definition, reads turned into inputs
        if pure_form is None:
            stop("no pure form")                         # stop 1
        values = []
        for register in instruction.reads:
            if register.number cannot be worked out:
                stop("register number unknown")          # stop 2
            if register.number not in table:
                stop("reads a register that holds no input")   # stop 3
            values.append(table[register.number])
        table[instruction.writes] = pure_form(values)
    return table[x10]                                    # the arch-unit expressed in Lean
```

No search and no guessing: one expression per arch-unit, then Lean's
check.

Block E — LITERAL, the three stops in
`PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/leanpath/walk.py`

```
329:            return {"refused": "no certified pure form for %s (%s)" % (
342:                return {"refused": "register of read %s not resolved" % rtext}
344:                return {"refused": "reads x%d, outside the ABI arguments" % k}
```

## 5. where it stops, in c's arch-units

Population: c's 610 compiler-operators, lowered to 610 arch-units and
walked on 2026-09-15 (lane l52). 346 were expressed in Lean. 248 stop
at stop 1 because Sail's decoder, as we run it, names their float
instruction words ILLEGAL, which has no pure form; why it does (the
float instructions left out of the decoder we built, or switched off in
the machine state it starts from) is unverified. The other 16:

Table 3 — the 16, by where they stop

| stop | c arch-units | one of them | why it stops there | status |
|---|---|---|---|---|
| 1. no pure form | 6 | c's `*` on `bool, int32_t`: `czero.eqz a0, a1, a0` (x10 becomes 0 when x10 is 0, else x11) | Sail defines it, but its definition computes the condition on a line of its own before the write, a shape `strip` does not know | open, ours |
| 2. register number unknown | 4 | c's `~` on `uint64_t`: `c.not a0` | Sail's definition names its register through a conversion on a line of its own, `let r := (creg2reg_idx rsdc)`; the walk works out a conversion written into the instruction's fields, not one Sail names first | open, ours |
| 3. reads a register that holds no input | 6 | c's unary `&` on `uint64_t`, the address of the input: `c.addi sp, -0x10; c.mv a1, a0; c.addi4spn a0, sp, 0x8; c.sdsp a1, 0x8(sp); c.addi sp, 0x10; c.jr ra` | its first arch-opcode reads x2, the stack pointer, which is not in the table; it also writes into memory, which the table does not hold | open, ours: the plan's `memory_and_calls` leaf |

The contrast for stop 2, both sides with an instance:

- Worked out: `c.xor a0, a1` in Table 1 names its registers in its fields as `creg2reg_idx (Cregidx 0x2#3)`, and Lean evaluated that to x10.
- Not worked out: `c.not a0` names its register through `let r := (creg2reg_idx rsdc)`, and the walk looks for `r` among the fields and does not find it.

## 6. decided, recorded for audit

- this log changes nothing in code, plan or runs.

## 7. awaiting the owner

- nothing from this log.

## 8. pointers

- the walk: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/leanpath/walk.py`, function `compose`
- the corpus walk rows: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/handful_c/walk_0/walk.json` to `walk_3/walk.json`
- the arch-unit sources: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/handful_c/corpus/`
- Sail's Lean emit: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/LeanIM/`
- the comms protocol: `PRIVATE/DevComms/comms_protocol.md`
