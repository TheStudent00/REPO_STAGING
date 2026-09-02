# dominant_table6 -- classes after the widened third candidate rule

- source table: dominant_table5.json
- source verdicts: verdicts6.json
- classes: 1019 (was 1025)
- classes of size 1: 578 (was 578)
- rows that are a merge of two or more source classes: 6
- weakest evidence: {'byte': 321, 'canon-byte': 57, 'sem': 26, 'z3': 35, 'core-text': 2, 'None': 578}

## the edges this table added

| pair | left class | right class | ground | joined two classes |
|---|---|---|---|---|
| cpp/op_606|go/op_564 | K0358 | K0372 | z3 over the two lifted forms | True |
| cpp/op_613|go/op_571 | K0359 | K0373 | z3 over the two lifted forms | True |
| cpp/op_620|go/op_578 | K0360 | K0374 | z3 over the two lifted forms | True |
| cpp/op_534|go/op_600 | K0362 | K0369 | z3 over the two lifted forms | True |
| cpp/op_541|go/op_607 | K0363 | K0370 | z3 over the two lifted forms | True |
| cpp/op_548|go/op_614 | K0364 | K0371 | z3 over the two lifted forms | True |

## the rows that merged

| class | merged from | operand types | result | languages | members | weakest evidence |
|---|---|---|---|---|---|---|
| K0358 | K0358, K0372 | i32,i32 | bool | cpp, go, rust, swift | cpp `<=`; go `<=`; rust `<=`; swift `<=` | z3 |
| K0359 | K0359, K0373 | i64,i64 | bool | cpp, go, rust, swift | cpp `<=`; go `<=`; rust `<=`; swift `<=` | z3 |
| K0360 | K0360, K0374 | u64,u64 | bool | cpp, go, rust, swift | cpp `<=`; go `<=`; rust `<=`; swift `<=` | z3 |
| K0362 | K0362, K0369 | i32,i32 | bool | cpp, go, rust, swift | cpp `>`; go `>`; rust `>`; swift `>` | z3 |
| K0363 | K0363, K0370 | i64,i64 | bool | cpp, go, rust, swift | cpp `>`; go `>`; rust `>`; swift `>` | z3 |
| K0364 | K0364, K0371 | u64,u64 | bool | cpp, go, rust, swift | cpp `>`; go `>`; rust `>`; swift `>` | z3 |
