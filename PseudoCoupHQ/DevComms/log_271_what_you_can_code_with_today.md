# log 271 — what you can code with today, in every language, and what guarantee each line carries

Written 2026-09-12 by the coordinator (Fable) for the owner, on request:
"what one could code with in every language ... with actual code
examples ... pseudo-code". Read from the bank's per-cell verdicts
(cov1, 2026-09-12, x86, destination reading) and from the
twelve-language round-trip program; both by full path in §8.

## §0. The answer, in one paragraph
Fixed-width integers and floats; every arithmetic, logic, shift and
compare operator in §3; assignment; a compare stored as a value; a
select (`a if c else b`); if / elif / else; while and counted for
loops; functions with calls, early return and recursion; records with
fixed-width fields. The expressions are proved on all five compiled
languages. The control constructs are the same construct in every
language and round-trip today, but their branches are not yet proved
on the machine body. Not yet at all: signed divide and remainder
outside c and c++, float subtraction and float equality on go, sign
extension into swift, 80-bit floats outside c and c++, closures,
generators, virtual dispatch, growing containers.

## §1. The words, declared before use
`PROVED, N of 5`
- the line's operator lowers to arch-opcodes whose emulation in N of
  the five compiled languages (c, c++, rust, go, swift) z3 confirmed
  equal to the machine definition for every input. The round trip
  closes on the certificates alone.
`STRUCTURAL`
- the construct is the same construct in every target: an if is an if,
  a while a while, a call a call. The target's own compiler emits its
  branch and call instructions. Verified by the twelve-language round
  trip on the quick-fox program (identical output through every
  language); NOT yet proved by z3 on the machine body, because the walk
  reads a body in text order and does not follow branches, and because
  a compare feeding a branch writes flags only. Both are owed (§6).
`NOT YET`
- refused at some language; the cause and the opener are in §4.
`arrival contract`
- what a call's argument or answer must satisfy to cross a frame: for
  values of 64 bits or fewer the verdict is identical or convertible
  (proved); 128-bit and 80-bit values are refused today.
`hub notation`
- the disciplined Python the hub reads: typed names, fixed-width int
  and float, no growing container inside the proved part.

## §2. A program you can write today, every line marked
```python
def mix(h: int, x: int) -> int:         # STRUCTURAL: call, return
    h = (h ^ x) & 0xFFFFFFFF            # PROVED 5 of 5: xor, and
    h = (h + (h << 5)) & 0xFFFFFFFF     # PROVED 5 of 5: shl, add
    return h                            # STRUCTURAL: return

def checksum(xs: list[int], n: int) -> int:
    h: int = 2166136261                 # PROVED 5 of 5: constant
    for i in range(n):                  # STRUCTURAL: counted loop
        v: int = xs[i]                  # PROVED 5 of 5: load
        v = -v if v < 0 else v          # PROVED 5 of 5: compare as a
                                        #   value, negate, select
        h = mix(h, v)                   # STRUCTURAL: call; arguments
                                        #   arrive under the contract
    return h

def sign(v: int) -> int:
    if v < 0:                           # STRUCTURAL: if / elif / else
        return -1                       #   with three early returns
    elif v == 0:
        return 0
    else:
        return 1

def fact(n: int) -> int:
    if n <= 1:                          # STRUCTURAL: if, early return
        return 1
    return n * fact(n - 1)              # PROVED 5 of 5: sub, signed
                                        #   mul; STRUCTURAL: recursion

def mean(xs: list[float], n: int) -> float:
    s: float = 0.0                      # PROVED 5 of 5: constant
    i: int = 0
    while i < n:                        # STRUCTURAL: while; its test
        s = s + xs[i]                   #   feeds a branch (§4)
        i = i + 1                       # PROVED 5 of 5: fadd, add
    return s / float(n)                 # PROVED 5 of 5: cvt, fdiv
```
Lines you would have to change today:
```python
q = a // b            # 2 of 5 (c, c++), and only in the machine's
                      #   truncating form; Python's floor form is
                      #   one compare and adjust on top, both proved
r = a % b             # 2 of 5 (c, c++): the same cell as divide
d = fa - fb           # 4 of 5: go refused
e = fa == fb          # 4 of 5: go refused
y = int64(int32(x))   # 4 of 5: swift refused (sign-extend 32 -> 64)
```

## §3. The expression vocabulary, x86, destination reading
| operator, as written | widths | c | c++ | rust | go | swift | languages |
|---|---|---|---|---|---|---|---|
| integer + and - | 8, 16, 32, 64 | yes | yes | yes | yes | yes | 5 of 5 |
| + with carry, - with borrow | 64 (borrow also 8) | yes | yes | yes | yes | yes | 5 of 5; borrow at 32 is 4 of 5 (rust no) |
| negate | 8, 16, 32, 64 | yes | yes | yes | yes | yes | 5 of 5 |
| & \| ^ ~ | 8, 32, 64 (~ also 16) | yes | yes | yes | yes | yes | 5 of 5 |
| << >> arithmetic and logical, by constant and by count; double-word shifts | 8, 16, 32, 64; double-word 64 | yes | yes | yes | yes | yes | 5 of 5 |
| signed * | 16, 32, 64 | yes | yes | yes | yes | yes | 5 of 5; at 8 it is 1 of 5 (go) |
| unsigned widening * | 8, 16, 32, 64 | yes | yes | yes | yes | yes | 5 of 5 |
| select `a if c else b`, the attested conditions | 32, 64 | yes | yes | yes | yes | yes | 5 of 5 |
| compare stored as a value | 8-bit answer | yes | yes | yes | yes | 12 of 15 conditions | 5 of 5 on 12 conditions; overflow and parity 4 of 5 |
| constants, moves, loads | 8 to 64 | yes | yes | yes | yes | yes | 5 of 5 |
| address arithmetic | 64 | register form yes; memory form no | same | yes | yes | yes | 5 of 5 register form; 3 of 5 memory form |
| zero-extend 8, 16 -> 32 | 32 | yes | yes | yes | yes | yes | 5 of 5 |
| sign-extend 32 -> 64 and 8 -> 64 | 64 | yes | yes | yes | yes | no | 4 of 5 |
| sign-extend 8, 16 -> 32 | 32 | no | no | no | yes | no | 1 of 5 |
| float + * / | 32, 64 | yes | yes | yes | yes | yes | 5 of 5 |
| float - | 32, 64 | yes | yes | yes | no | yes | 4 of 5 |
| float == != stored as a value | 32, 64 | yes | yes | yes | no | yes | 4 of 5 |
| int -> float, float -> double, moves between int and float registers | 32, 64 | yes | yes | yes | yes | yes | 5 of 5 |
| 128-bit register logic, moves, unpack, extract | 128 | yes | yes | yes | yes | yes | 5 of 5 (register forms only) |
| signed / and % | 32, 64 | yes | yes | no | no | no | 2 of 5; at 8, 16 it is 0 of 5 |
| unsigned / and % | 8 to 64 | no | no | no | no | no | 0 of 5 |
| 80-bit long double | 80 | yes | yes | no | no | no | 2 of 5 |
| compare feeding a branch; float compare feeding a branch; push | | no | no | no | no | no | 0 of 5: flags or stack, no answer register; these are structural |

## §4. Outside today, with cause and opener
| you cannot write, or not yet | why | what opens it |
|---|---|---|
| a // b, a % b on rust, go, swift | the divide check runs out; go's own zero check | branch-following walk; divide lemma |
| fa - fb, fa == fb on go | undecided at the check | the same walk |
| int64(int32(x)) on swift | the widening move refused at arrival | arrival contract, the convertible verdict |
| long double outside c, c++ | no holder | the x87 arrival as two words |
| a condition proved as the branch it feeds | flags only, no answer register | the flags-consumer contract |
| try/except, classes with methods, lists, dicts, strings | carried by the round trip today (quick-fox); nothing proved at the machine level: runtime library and dispatch, not operators | runtime-callee extraction |
| closures, generators, virtual dispatch, side effects that depend on evaluation order | discipline Forbid rows 3 to 5 | nothing; write without them |
| a 128-bit value across a call | arrival refused | the calling convention as hub structure |

## §5. How a line is carried
```
for stmt in program:
    if stmt is an assignment:
        for node in stmt.expression, leaves first:
            cell = arch_opcode_of(node.operator, node.widths)
            cert = bank[cell][target]        # PROVED, or the cause
        # a compare stored as a value, or a select, is such a node
    elif stmt is if / elif / while / for / return:
        emit target's own construct          # STRUCTURAL
        # its test is a compare feeding a branch: flags only, no
        # answer register; the flags-consumer contract is owed
    elif stmt is a call:
        emit target's own call               # STRUCTURAL
        for arg in stmt.args:
            verdict = arrival(arg.width)     # <= 64: identical or
                                             # convertible; 128, 80:
                                             # refused
```

## §6. The four anchors
| anchor | one line |
|---|---|
| the research | at the code level the proved vocabulary is the whole fixed-width integer and float expression language less signed divide (3 languages), float subtract and float equality (go), sign extension (swift); the control constructs are structural and round-trip tested, not machine-proved |
| mine next | cov2: the exact operator vocabulary from the corpus manifests (a session with a shell); then the branch-following walk and the flags-consumer contract, each a brief |
| yours | the two plan rulings (pipeline in PseudoIR; the exchange node's clause); restoring `PRIVATE/PseudoCoup_v5/Designing/`; the daemon restart |
| theirs | the other conversation: the daemon restart that splits the two oversized files |

## §7. Decided, recorded for audit / awaiting the owner
Decided: a condition inside if or while is STRUCTURAL, never PROVED,
until the flags-consumer contract exists; a compare stored as a value
or used in a select is PROVED; every row carries N of 5; `//` is
reported in the machine's truncating form, with the floor adjust
named.

Awaiting the owner: nothing in this log; the plan rulings stand in log_270.

## §8. Pointers, by full path
- the per-cell verdicts this log reads:
  `PRIVATE/PseudoCoupHQ/Research/oracle/coverage/bank_x86.json`
- how they were joined, and the reach matrices:
  `PRIVATE/PseudoCoupHQ/DevComms/` logs 266 (cov1) and
  269 (bb2); each file name begins `log_<number>_`.
- the round-trip program the STRUCTURAL rows rest on:
  `PUBLIC/PseudoCoup/tests/roundtrip/00_quickfox.py`
- the progress report, with the disciplines matrix and the eight rows:
  `PRIVATE/PseudoCoupHQ/DevComms/log_270_autopoly_progress_report_2026-09-12.md`
- the brief that computes the exact vocabulary from the corpus:
  `PRIVATE/PseudoCoupHQ/Research/briefs/task_cov2_brief.md`
- the glossary (arch-unit, segment, backstop, walk):
  `PRIVATE/PseudoCoupHQ/Research/GLOSSARY.md`
