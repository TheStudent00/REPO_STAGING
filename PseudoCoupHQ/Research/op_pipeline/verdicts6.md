# verdicts6 -- the third candidate rule, widened to classes of three or fewer

The representative of a class of at most three members,
nominated against the representative of every other
class carrying the same class key (same operand types,
same result type).  No operator token takes part in the
nomination; each member carries its token as a display
label only.

- source table: dominant_table5.json
- classes read: 1025
- classes of size <= 3: 949
- nominations: 8148
- pairs already in one class (not nominated): 0
- distinct unit pairs judged: 4370
- verdicts reused from cache: 234
- verdicts freshly decided: 4240
- tally: {'UNMATCHED': 1812, 'UNDECIDED': 2530, 'DIFFERS-BY-DESIGN': 22, 'MATCHED': 6}

## the MATCHED pairs

| left | right | left label | right label | left class size | right class size | operand types | result | ground |
|---|---|---|---|---|---|---|---|---|
| cpp/op_606 | go/op_564 | `<=` | `<=` | 2 | 2 | i32,i32 | bool | z3 over the two lifted forms |
| cpp/op_613 | go/op_571 | `<=` | `<=` | 2 | 2 | i64,i64 | bool | z3 over the two lifted forms |
| cpp/op_620 | go/op_578 | `<=` | `<=` | 2 | 2 | u64,u64 | bool | z3 over the two lifted forms |
| cpp/op_534 | go/op_600 | `>` | `>` | 2 | 2 | i32,i32 | bool | z3 over the two lifted forms |
| cpp/op_541 | go/op_607 | `>` | `>` | 2 | 2 | i64,i64 | bool | z3 over the two lifted forms |
| cpp/op_548 | go/op_614 | `>` | `>` | 2 | 2 | u64,u64 | bool | z3 over the two lifted forms |
