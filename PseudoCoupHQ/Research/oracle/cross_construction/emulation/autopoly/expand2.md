# expand2 -- task ex2: the interpreted loop

Node: hq.research.arch_unit_oracle.cross_construction.autopoly; also serves node_0_3_1_12_remaining_languages.

Written by `expand2.py report`. Every table is the output of a command of this program, captured: `tables`, `all_seven`, `disagreements`, `declines`, `refusals`, `handful_check`.

Nothing new in method: the emulation is task ex1's own -- the cell's mapping rendered in the target's own operators over its own value model -- and the check is task ex1's own sample rule, pasted below LITERAL, exactly as it ran.

## 1. the per-target table

Table 1 -- one row per target. `cells` counts runs; `rows` is the attested ledger rows those cells cover and `share` that as a percentage of 133044. A run whose first pass TIMED OUT and whose 600 s retry answered is counted by the retry's own outcome; a run that timed out on both passes is counted `timed out`.

| step | cpython | php | ruby | java | javascript | dart | csharp |
|---|---|---|---|---|---|---|---|
| `attempted` | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% |
| `rendered` | 175 cells, 110004 rows, 82.68% | 166 cells, 105628 rows, 79.39% | 175 cells, 110004 rows, 82.68% | 166 cells, 105628 rows, 79.39% | 175 cells, 110004 rows, 82.68% | 166 cells, 105628 rows, 79.39% | 184 cells, 116057 rows, 87.23% |
| `whole sample agrees` | 175 cells, 110004 rows, 82.68% | 166 cells, 105628 rows, 79.39% | 175 cells, 110004 rows, 82.68% | 166 cells, 105628 rows, 79.39% | 175 cells, 110004 rows, 82.68% | 166 cells, 105628 rows, 79.39% | 167 cells, 105760 rows, 79.49% |
| `any disagreement` | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 11 cells, 8611 rows, 6.47% |
| `refused` | 78 cells, 23040 rows, 17.32% | 87 cells, 27416 rows, 20.61% | 78 cells, 23040 rows, 17.32% | 87 cells, 27416 rows, 20.61% | 78 cells, 23040 rows, 17.32% | 87 cells, 27416 rows, 20.61% | 69 cells, 16987 rows, 12.77% |
| `timed out` | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% |

## 2. all seven, all twelve

Table 2 -- the widths this line has proved or checked, side by side, neither redefining the other.

| width | targets | cells | ledger rows | share |
|---|---|---|---|---|
| all four | c, rust, go, swift | 165 | 106773 | 80.25% |
| all five | c, cpp, rust, go, swift | 163 | 105877 | 79.58% |
| all seven | cpython, php, ruby, java, javascript, dart, csharp | 166 | 105628 | 79.39% |
| all twelve | the five compiled proved + the seven agreeing | 143 | 94052 | 70.69% |

cells agreeing on all seven interpreted targets but NOT proved on all five compiled targets: 23
cells proved on all five compiled targets but not agreeing on all seven interpreted targets: 20

## 3. every disagreement

disagreements found: 11 of 1771 runs

| cell | target | the point, the reference's answer, the interpreter's answer, LITERAL |
|---|---|---|
| `cmp` gpr_gpr 64 | csharp | {"point": [1], "the interpreter's answer": 0, "the reference's answer": 1} |
| `push` gpr_one 64 | csharp | {"point": [1], "the interpreter's answer": 4294967296, "the reference's answer": 1} |
| `ucomisd` xmm_xmm 64 | csharp | {"point": [9223372036854775808], "the interpreter's answer": 0, "the reference's answer": 9223372036854775808} |
| `punpckldq` mem_xmm 128 | csharp | {"point": [0, 2147483648], "the interpreter's answer": 0, "the reference's answer": 2147483648} |
| `andpd` xmm_xmm 128 | csharp | {"point": [9223372036854775808, 9223372036854775808], "the interpreter's answer": 0, "the reference's answer": 9223372036854775808} |
| `andps` xmm_xmm 128 | csharp | {"point": [9223372036854775808, 9223372036854775808], "the interpreter's answer": 0, "the reference's answer": 9223372036854775808} |
| `orpd` xmm_xmm 128 | csharp | {"point": [0, 9223372036854775808], "the interpreter's answer": 0, "the reference's answer": 9223372036854775808} |
| `orps` xmm_xmm 128 | csharp | {"point": [0, 9223372036854775808], "the interpreter's answer": 0, "the reference's answer": 9223372036854775808} |
| `punpcklqdq` xmm_xmm 128 | csharp | {"point": [9223372036854775808], "the interpreter's answer": 0, "the reference's answer": 9223372036854775808} |
| `pxor` xmm_xmm 128 | csharp | {"point": [0, 9223372036854775808], "the interpreter's answer": 0, "the reference's answer": 9223372036854775808} |
| `pand` xmm_xmm 128 | csharp | {"point": [0, 1], "the interpreter's answer": 1, "the reference's answer": 0} |

## 4. declines by target and word

| target | cause | points |
|---|---|---|
| cpython | the interpreter RAISE:ZeroDivisionError | 4586 |
| cpython | the reference's own term does not evaluate to a numeral at this point | 1535 |
| php | the interpreter RAISE:DivisionByZeroError | 3128 |
| php | the reference's own term does not evaluate to a numeral at this point | 1535 |
| php | the interpreter RAISE:ArithmeticError | 1 |
| ruby | the interpreter RAISE:ZeroDivisionError | 4434 |
| ruby | the reference's own term does not evaluate to a numeral at this point | 1535 |
| java | the interpreter RAISE:ArithmeticException | 2976 |
| java | the reference's own term does not evaluate to a numeral at this point | 1535 |
| javascript | the interpreter RAISE:RangeError | 4434 |
| javascript | the reference's own term does not evaluate to a numeral at this point | 1535 |
| dart | the interpreter RAISE:IntegerDivisionByZeroException | 2976 |
| dart | the reference's own term does not evaluate to a numeral at this point | 1535 |
| csharp | the interpreter RAISE:DivideByZeroException | 2976 |
| csharp | the reference's own term does not evaluate to a numeral at this point | 1540 |
| csharp | the interpreter RAISE:IndexOutOfRangeException | 156 |
| csharp | the interpreter RAISE:OverflowException | 1 |

declined points over every run: 36418

## 5. refusals by cause

| target | cause | runs | ledger rows |
|---|---|---|---|
| cpython | vector arrival used beyond its low lane | 28 | 3738 |
| cpython | the runner did not answer | 24 | 16604 |
| cpython | operator not covered by the renderer | 22 | 1601 |
| cpython | term reads state that is not an arrival register | 4 | 1097 |
| php | a width c has no holder for | 48 | 8521 |
| php | the runner did not answer | 23 | 16283 |
| php | operator not covered by the renderer | 12 | 1515 |
| php | term reads state that is not an arrival register | 4 | 1097 |
| ruby | vector arrival used beyond its low lane | 28 | 3738 |
| ruby | the runner did not answer | 24 | 16604 |
| ruby | operator not covered by the renderer | 22 | 1601 |
| ruby | term reads state that is not an arrival register | 4 | 1097 |
| java | a width c has no holder for | 48 | 8521 |
| java | the runner did not answer | 23 | 16283 |
| java | operator not covered by the renderer | 12 | 1515 |
| java | term reads state that is not an arrival register | 4 | 1097 |
| javascript | vector arrival used beyond its low lane | 28 | 3738 |
| javascript | the runner did not answer | 24 | 16604 |
| javascript | operator not covered by the renderer | 22 | 1601 |
| javascript | term reads state that is not an arrival register | 4 | 1097 |
| dart | a width c has no holder for | 48 | 8521 |
| dart | the runner did not answer | 23 | 16283 |
| dart | operator not covered by the renderer | 12 | 1515 |
| dart | term reads state that is not an arrival register | 4 | 1097 |
| csharp | a width c has no holder for | 48 | 8521 |
| csharp | operator not covered by the renderer | 12 | 1515 |
| csharp | the runner did not answer | 5 | 5854 |
| csharp | term reads state that is not an arrival register | 4 | 1097 |

refused runs over the whole loop: 564 of 1771

## 6. the handful's seventy, reproduced inside the loop

| cell | target | this loop | task ex1's handful | agree |
|---|---|---|---|---|
| `add` gpr_gpr 32 | cpython | 900 points, 900 agree, 0 disagree, 0 declined | 900 points, 900 agree, 0 disagree, 0 declined | True |
| `add` gpr_gpr 32 | php | 900 points, 900 agree, 0 disagree, 0 declined | 900 points, 900 agree, 0 disagree, 0 declined | True |
| `add` gpr_gpr 32 | ruby | 900 points, 900 agree, 0 disagree, 0 declined | 900 points, 900 agree, 0 disagree, 0 declined | True |
| `add` gpr_gpr 32 | java | 900 points, 900 agree, 0 disagree, 0 declined | 900 points, 900 agree, 0 disagree, 0 declined | True |
| `add` gpr_gpr 32 | javascript | 900 points, 900 agree, 0 disagree, 0 declined | 900 points, 900 agree, 0 disagree, 0 declined | True |
| `add` gpr_gpr 32 | dart | 900 points, 900 agree, 0 disagree, 0 declined | 900 points, 900 agree, 0 disagree, 0 declined | True |
| `add` gpr_gpr 32 | csharp | 900 points, 900 agree, 0 disagree, 0 declined | 900 points, 900 agree, 0 disagree, 0 declined | True |
| `sub` imm_gpr 64 | cpython | not run | 30 points, 30 agree, 0 disagree, 0 declined | -- |
| `sub` imm_gpr 64 | php | not run | 30 points, 30 agree, 0 disagree, 0 declined | -- |
| `sub` imm_gpr 64 | ruby | not run | 30 points, 30 agree, 0 disagree, 0 declined | -- |
| `sub` imm_gpr 64 | java | not run | 30 points, 30 agree, 0 disagree, 0 declined | -- |
| `sub` imm_gpr 64 | javascript | not run | 30 points, 30 agree, 0 disagree, 0 declined | -- |
| `sub` imm_gpr 64 | dart | not run | 30 points, 30 agree, 0 disagree, 0 declined | -- |
| `sub` imm_gpr 64 | csharp | not run | 30 points, 30 agree, 0 disagree, 0 declined | -- |
| `imul` gpr_gpr 32 | cpython | 900 points, 900 agree, 0 disagree, 0 declined | 900 points, 900 agree, 0 disagree, 0 declined | True |
| `imul` gpr_gpr 32 | php | 900 points, 900 agree, 0 disagree, 0 declined | 900 points, 900 agree, 0 disagree, 0 declined | True |
| `imul` gpr_gpr 32 | ruby | 900 points, 900 agree, 0 disagree, 0 declined | 900 points, 900 agree, 0 disagree, 0 declined | True |
| `imul` gpr_gpr 32 | java | 900 points, 900 agree, 0 disagree, 0 declined | 900 points, 900 agree, 0 disagree, 0 declined | True |
| `imul` gpr_gpr 32 | javascript | 900 points, 900 agree, 0 disagree, 0 declined | 900 points, 900 agree, 0 disagree, 0 declined | True |
| `imul` gpr_gpr 32 | dart | 900 points, 900 agree, 0 disagree, 0 declined | 900 points, 900 agree, 0 disagree, 0 declined | True |
| `imul` gpr_gpr 32 | csharp | 900 points, 900 agree, 0 disagree, 0 declined | 900 points, 900 agree, 0 disagree, 0 declined | True |
| `sar` cl_gpr 32 | cpython | 810 points, 810 agree, 0 disagree, 0 declined | 810 points, 810 agree, 0 disagree, 0 declined | True |
| `sar` cl_gpr 32 | php | 810 points, 810 agree, 0 disagree, 0 declined | 810 points, 810 agree, 0 disagree, 0 declined | True |
| `sar` cl_gpr 32 | ruby | 810 points, 810 agree, 0 disagree, 0 declined | 810 points, 810 agree, 0 disagree, 0 declined | True |
| `sar` cl_gpr 32 | java | 810 points, 810 agree, 0 disagree, 0 declined | 810 points, 810 agree, 0 disagree, 0 declined | True |
| `sar` cl_gpr 32 | javascript | 810 points, 810 agree, 0 disagree, 0 declined | 810 points, 810 agree, 0 disagree, 0 declined | True |
| `sar` cl_gpr 32 | dart | 810 points, 810 agree, 0 disagree, 0 declined | 810 points, 810 agree, 0 disagree, 0 declined | True |
| `sar` cl_gpr 32 | csharp | 810 points, 810 agree, 0 disagree, 0 declined | 810 points, 810 agree, 0 disagree, 0 declined | True |
| `shr` cl_gpr 64 | cpython | 810 points, 810 agree, 0 disagree, 0 declined | 810 points, 810 agree, 0 disagree, 0 declined | True |
| `shr` cl_gpr 64 | php | 810 points, 810 agree, 0 disagree, 0 declined | 810 points, 810 agree, 0 disagree, 0 declined | True |
| `shr` cl_gpr 64 | ruby | 810 points, 810 agree, 0 disagree, 0 declined | 810 points, 810 agree, 0 disagree, 0 declined | True |
| `shr` cl_gpr 64 | java | 810 points, 810 agree, 0 disagree, 0 declined | 810 points, 810 agree, 0 disagree, 0 declined | True |
| `shr` cl_gpr 64 | javascript | 810 points, 810 agree, 0 disagree, 0 declined | 810 points, 810 agree, 0 disagree, 0 declined | True |
| `shr` cl_gpr 64 | dart | 810 points, 810 agree, 0 disagree, 0 declined | 810 points, 810 agree, 0 disagree, 0 declined | True |
| `shr` cl_gpr 64 | csharp | 810 points, 810 agree, 0 disagree, 0 declined | 810 points, 810 agree, 0 disagree, 0 declined | True |
| `idiv` gpr_one 32 | cpython | 19683 points, 18954 agree, 0 disagree, 729 declined | 19683 points, 18954 agree, 0 disagree, 729 declined | True |
| `idiv` gpr_one 32 | php | 19683 points, 18953 agree, 0 disagree, 730 declined | 19683 points, 18953 agree, 0 disagree, 730 declined | True |
| `idiv` gpr_one 32 | ruby | 19683 points, 18954 agree, 0 disagree, 729 declined | 19683 points, 18954 agree, 0 disagree, 729 declined | True |
| `idiv` gpr_one 32 | java | 19683 points, 18954 agree, 0 disagree, 729 declined | 19683 points, 18954 agree, 0 disagree, 729 declined | True |
| `idiv` gpr_one 32 | javascript | 19683 points, 18954 agree, 0 disagree, 729 declined | 19683 points, 18954 agree, 0 disagree, 729 declined | True |
| `idiv` gpr_one 32 | dart | 19683 points, 18954 agree, 0 disagree, 729 declined | 19683 points, 18954 agree, 0 disagree, 729 declined | True |
| `idiv` gpr_one 32 | csharp | 19683 points, 18953 agree, 0 disagree, 730 declined | 19683 points, 18953 agree, 0 disagree, 730 declined | True |
| `cmovne` gpr_gpr 32 | cpython | 14641 points, 14641 agree, 0 disagree, 0 declined | 14641 points, 14641 agree, 0 disagree, 0 declined | True |
| `cmovne` gpr_gpr 32 | php | 14641 points, 14641 agree, 0 disagree, 0 declined | 14641 points, 14641 agree, 0 disagree, 0 declined | True |
| `cmovne` gpr_gpr 32 | ruby | 14641 points, 14641 agree, 0 disagree, 0 declined | 14641 points, 14641 agree, 0 disagree, 0 declined | True |
| `cmovne` gpr_gpr 32 | java | 14641 points, 14641 agree, 0 disagree, 0 declined | 14641 points, 14641 agree, 0 disagree, 0 declined | True |
| `cmovne` gpr_gpr 32 | javascript | 14641 points, 14641 agree, 0 disagree, 0 declined | 14641 points, 14641 agree, 0 disagree, 0 declined | True |
| `cmovne` gpr_gpr 32 | dart | 14641 points, 14641 agree, 0 disagree, 0 declined | 14641 points, 14641 agree, 0 disagree, 0 declined | True |
| `cmovne` gpr_gpr 32 | csharp | 14641 points, 14641 agree, 0 disagree, 0 declined | 14641 points, 14641 agree, 0 disagree, 0 declined | True |
| `setne` gpr_one 8 | cpython | 729 points, 729 agree, 0 disagree, 0 declined | 729 points, 729 agree, 0 disagree, 0 declined | True |
| `setne` gpr_one 8 | php | 729 points, 729 agree, 0 disagree, 0 declined | 729 points, 729 agree, 0 disagree, 0 declined | True |
| `setne` gpr_one 8 | ruby | 729 points, 729 agree, 0 disagree, 0 declined | 729 points, 729 agree, 0 disagree, 0 declined | True |
| `setne` gpr_one 8 | java | 729 points, 729 agree, 0 disagree, 0 declined | 729 points, 729 agree, 0 disagree, 0 declined | True |
| `setne` gpr_one 8 | javascript | 729 points, 729 agree, 0 disagree, 0 declined | 729 points, 729 agree, 0 disagree, 0 declined | True |
| `setne` gpr_one 8 | dart | 729 points, 729 agree, 0 disagree, 0 declined | 729 points, 729 agree, 0 disagree, 0 declined | True |
| `setne` gpr_one 8 | csharp | 729 points, 729 agree, 0 disagree, 0 declined | 729 points, 729 agree, 0 disagree, 0 declined | True |
| `addss` xmm_xmm 32 | cpython | 529 points, 439 agree, 0 disagree, 90 declined | 529 points, 439 agree, 0 disagree, 90 declined | True |
| `addss` xmm_xmm 32 | php | 529 points, 439 agree, 0 disagree, 90 declined | 529 points, 439 agree, 0 disagree, 90 declined | True |
| `addss` xmm_xmm 32 | ruby | 529 points, 439 agree, 0 disagree, 90 declined | 529 points, 439 agree, 0 disagree, 90 declined | True |
| `addss` xmm_xmm 32 | java | 529 points, 439 agree, 0 disagree, 90 declined | 529 points, 439 agree, 0 disagree, 90 declined | True |
| `addss` xmm_xmm 32 | javascript | 529 points, 439 agree, 0 disagree, 90 declined | 529 points, 439 agree, 0 disagree, 90 declined | True |
| `addss` xmm_xmm 32 | dart | 529 points, 439 agree, 0 disagree, 90 declined | 529 points, 439 agree, 0 disagree, 90 declined | True |
| `addss` xmm_xmm 32 | csharp | 529 points, 439 agree, 0 disagree, 90 declined | 529 points, 439 agree, 0 disagree, 90 declined | True |
| `cvtsi2sd` gpr_xmm 64 | cpython | 30 points, 30 agree, 0 disagree, 0 declined | 30 points, 30 agree, 0 disagree, 0 declined | True |
| `cvtsi2sd` gpr_xmm 64 | php | 30 points, 30 agree, 0 disagree, 0 declined | 30 points, 30 agree, 0 disagree, 0 declined | True |
| `cvtsi2sd` gpr_xmm 64 | ruby | 30 points, 30 agree, 0 disagree, 0 declined | 30 points, 30 agree, 0 disagree, 0 declined | True |
| `cvtsi2sd` gpr_xmm 64 | java | 30 points, 30 agree, 0 disagree, 0 declined | 30 points, 30 agree, 0 disagree, 0 declined | True |
| `cvtsi2sd` gpr_xmm 64 | javascript | 30 points, 30 agree, 0 disagree, 0 declined | 30 points, 30 agree, 0 disagree, 0 declined | True |
| `cvtsi2sd` gpr_xmm 64 | dart | 30 points, 30 agree, 0 disagree, 0 declined | 30 points, 30 agree, 0 disagree, 0 declined | True |
| `cvtsi2sd` gpr_xmm 64 | csharp | 30 points, 30 agree, 0 disagree, 0 declined | 30 points, 30 agree, 0 disagree, 0 declined | True |

of the seventy, this loop's own outcome matches task ex1's handful: 63 of 63 compared

## 7. the sample rule, LITERAL, as it was run (task ex1's own, unchanged)

```
THE SAMPLE, for a place whose emulation takes k arrivals of widths
w_1 .. w_k.

  the per-arrival budget b = max(4, int(20000 ** (1.0 / k)))

  P(an INTEGER arrival of width w) is this list, in this order,
  deduplicated, every value taken modulo nothing and dropped when it
  is not less than 2^w, then cut to its first b entries:
      0, 1, 2, 3, 7, 100,
      2^(w-1) - 1, 2^(w-1), 2^(w-1) + 1,          the sign boundary
      2^w - 2, 2^w - 1,                           the top, and -1
      w - 1, w, w + 1,                            this width's shift counts
      7, 8, 9, 15, 16, 17, 31, 32, 33, 63, 64, 65, the other widths'
      then 8 values from random.Random(20260909).randrange(2^w)

  P(a FLOAT arrival of width w, which reaches the emulation as its
  IEEE bit pattern) is this list, in this order, deduplicated, cut to
  its first b entries:
      +0, -0, 1.0, -1.0, 2.0, 0.5, -0.5,
      the smallest subnormal, the largest subnormal,
      the smallest normal, the largest finite,
      +inf, -inf, a quiet NaN, a signalling NaN,
      then 8 values from random.Random(20260909).randrange(2^w)

  THE SAMPLE is the ordered cross product P(a_1) x ... x P(a_k), in
  that order.  Its size is at most 20,000 by the budget above, and the
  run record carries the exact count.

  WHY b IS A CEILING AND NOT A CHOICE OF POINTS: the edge values come
  FIRST in every list, so cutting to b drops ordinary values before it
  drops an edge.  A place with one or two arrivals is never cut at all
  (b is 20000 and 141), so the handful's edges are all present; a
  place with four is cut to 11 per arrival, and the run record says
  which values those were.
```

