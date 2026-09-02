# dom_ops digest -- one table

Rows are dominant operators: connected components of the mutual-best graph.  A language cell carries that language's display label and arity, or `--` with the reason it is absent.

Absence reasons: `no mutual` = the language has units in these classes but no node of it was chosen back; `bridge only` = a directional bridge reaches these classes, membership does not; `refused/absent` = no accepted unit of the language sits in any class this dominant operator spans.

| dom_op | c | cpp | go | rust | swift | java | classes | bridges | fences | weakest evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D0001 | `+` unary_prefix + `++` unary_postfix + `--` unary_postfix + `__extension__` unary_prefix | `+` unary_prefix + `++` unary_postfix + `--` unary_postfix | `+` unary_prefix | -- refused/absent | `+` unary_prefix | -- refused/absent | 7 | 1 | 0 | canon-byte |
| D0002 | `&` binary | `&` binary + `bitand` binary | `&` binary | `&` binary | `&` binary | -- refused/absent | 16 | 1 | 0 | sem |
| D0003 | `+` binary | `+` binary | `+` binary | `+` binary | `+` binary | `+` binary | 36 | 0 | 15 | sem |
| D0004 | `--` unary_prefix | `!` unary_prefix + `--` unary_prefix + `not` unary_prefix | `!` unary_prefix | -- no mutual | `!` unary_prefix | -- refused/absent | 11 | 9 | 3 | z3 |
| D0005 | `^` binary | `^` binary + `xor` binary | `^` binary | `^` binary | `^` binary | -- refused/absent | 16 | 1 | 0 | sem |
| D0006 | `\|` binary | `bitor` binary + `\|` binary | `\|` binary | `\|` binary | `\|` binary | -- refused/absent | 16 | 1 | 0 | sem |
| D0007 | `~` unary_prefix | `compl` unary_prefix + `~` unary_prefix | `^` unary_prefix | `!` unary_prefix | `~` unary_prefix | -- refused/absent | 4 | 0 | 1 | sem |
| D0008 | `*` binary | `*` binary | `*` binary | `*` binary | `*` binary | -- refused/absent | 36 | 1 | 11 | sem |
| D0009 | `-` binary | `-` binary | `-` binary | `-` binary | `-` binary | -- refused/absent | 36 | 0 | 11 | sem |
| D0010 | `-` unary_prefix | `-` unary_prefix | `-` unary_prefix | `-` unary_prefix | `-` unary_prefix | -- refused/absent | 6 | 0 | 10 | sem |
| D0011 | `/` binary | `/` binary | `/` binary | `/` binary | `/` binary | -- refused/absent | 37 | 1 | 13 | core-text |
| D0012 | `_Alignof` unary_prefix + `__alignof` unary_prefix + `__alignof__` unary_prefix + `sizeof` unary_prefix | `sizeof` unary_prefix | -- refused/absent | -- refused/absent | -- refused/absent | -- refused/absent | 6 | 0 | 0 | canon-byte |
| D0013 | -- bridge only | `!=` binary + `not_eq` binary | `!=` binary | `!=` binary | `!=` binary | -- refused/absent | 36 | 53 | 26 | z3 |
| D0014 | -- bridge only | `&&` binary + `and` binary | `&&` binary | `&&` binary | `&&` binary | -- refused/absent | 36 | 49 | 0 | sem |
| D0015 | -- bridge only | `or` binary + `\|\|` binary | `\|\|` binary | `\|\|` binary | `\|\|` binary | -- refused/absent | 36 | 49 | 0 | sem |
| D0016 | -- bridge only | `<` binary | `<` binary | `<` binary | `<` binary | -- refused/absent | 8 | 8 | 15 | z3 |
| D0017 | -- bridge only | `<=` binary | `<=` binary | `<=` binary | `<=` binary | -- refused/absent | 11 | 8 | 10 | z3 |
| D0018 | -- bridge only | `==` binary | `==` binary | `==` binary | `==` binary | -- refused/absent | 8 | 8 | 14 | z3 |
| D0019 | -- bridge only | `>` binary | `>` binary | `>` binary | `>` binary | -- refused/absent | 11 | 8 | 9 | z3 |
| D0020 | -- bridge only | `>=` binary | `>=` binary | `>=` binary | `>=` binary | -- refused/absent | 8 | 8 | 16 | z3 |
| D0021 | `<<` binary | `<<` binary | -- refused/absent | `<<` binary | -- refused/absent | -- refused/absent | 16 | 0 | 12 | byte |
| D0022 | `>>` binary | `>>` binary | -- refused/absent | `>>` binary | -- refused/absent | -- refused/absent | 16 | 0 | 6 | byte |
| D0023 | `%` binary | `%` binary | -- refused/absent | -- refused/absent | -- refused/absent | -- refused/absent | 16 | 0 | 0 | byte |
| D0024 | `&` unary_prefix | `&` unary_prefix | -- refused/absent | -- refused/absent | -- refused/absent | -- refused/absent | 6 | 0 | 0 | byte |
| D0025 | `++` unary_prefix | `++` unary_prefix | -- refused/absent | -- refused/absent | -- refused/absent | -- refused/absent | 5 | 0 | 0 | byte |
| D0026 | -- refused/absent | -- refused/absent | `%` binary | `%` binary | -- refused/absent | -- refused/absent | 1 | 0 | 8 | core-text |
| D0027 | -- refused/absent | -- refused/absent | `<<` binary | -- refused/absent | `<<` binary | -- refused/absent | 1 | 0 | 18 | z3 |
| D0028 | -- refused/absent | -- refused/absent | `>>` binary | -- refused/absent | `>>` binary | -- refused/absent | 1 | 0 | 12 | z3 |

A cell holding two labels joined by `+` is a same-language collision: the component chained back into a language it had already visited.  Recorded, not resolved -- the owner settles the rule.

nodes 143; edges 248 before the mutual filter, 210 after; dom_ops 28.
