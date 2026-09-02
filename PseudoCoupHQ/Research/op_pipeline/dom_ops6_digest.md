# dom_ops digest -- one table

Rows are dominant operators: connected components of the mutual-best graph.  A language cell carries that language's display label and arity, or `--` with the reason it is absent.

Absence reasons: `no mutual` = the language has units in these classes but no node of it was chosen back; `bridge only` = a directional bridge reaches these classes, membership does not; `refused/absent` = no accepted unit of the language sits in any class this dominant operator spans.

| dom_op | c | cpp | go | rust | swift | java | classes | bridges | fences | weakest evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D0001 | `&` binary + `&=` assignment | `&` binary + `&=` assignment + `and_eq` assignment + `bitand` binary | `&` binary + `&=` assignment | `&` binary + `&=` assignment | `&` binary | -- refused/absent | 23 | 1 | 0 | erased-form |
| D0002 | `+` binary + `+=` assignment | `+` binary + `+=` assignment | `+` binary + `+=` assignment | `+` binary + `+=` assignment | `+` binary + `+=` assignment | `+` binary | 55 | 0 | 15 | erased-form |
| D0003 | `^` binary + `^=` assignment | `^` binary + `^=` assignment + `xor` binary + `xor_eq` assignment | `^` binary + `^=` assignment | `^` binary + `^=` assignment | `^` binary | -- refused/absent | 23 | 1 | 0 | erased-form |
| D0004 | `\|` binary + `\|=` assignment | `bitor` binary + `or_eq` assignment + `\|` binary + `\|=` assignment | `\|` binary + `\|=` assignment | `\|` binary + `\|=` assignment | `\|` binary | -- refused/absent | 23 | 1 | 0 | erased-form |
| D0005 | `*` binary + `*=` assignment | `*` binary + `*=` assignment | `*` binary + `*=` assignment | `*` binary + `*=` assignment | `*` binary + `*=` assignment | -- refused/absent | 55 | 1 | 11 | erased-form |
| D0006 | `-` binary + `-=` assignment | `-` binary + `-=` assignment | `-` binary + `-=` assignment | `-` binary + `-=` assignment | `-` binary + `-=` assignment | -- refused/absent | 55 | 0 | 11 | erased-form |
| D0007 | `/` binary + `/=` assignment | `/` binary + `/=` assignment | `/` binary + `/=` assignment | `/` binary + `/=` assignment | `/` binary + `/=` assignment | -- refused/absent | 60 | 1 | 13 | erased-form |
| D0008 | `+` unary_prefix + `++` unary_postfix + `--` unary_postfix + `__extension__` unary_prefix | `+` unary_prefix + `++` unary_postfix + `--` unary_postfix | `+` unary_prefix | -- refused/absent | `+` unary_prefix | -- refused/absent | 7 | 1 | 0 | canon-byte |
| D0009 | `<<` binary + `<<=` assignment | `<<` binary + `<<=` assignment | -- refused/absent | `<<` binary + `<<=` assignment | `??` binary | -- refused/absent | 20 | 0 | 12 | erased-form |
| D0010 | `--` unary_prefix | `!` unary_prefix + `--` unary_prefix + `not` unary_prefix | `!` unary_prefix | -- no mutual | `!` unary_prefix | -- refused/absent | 11 | 9 | 3 | erased-form |
| D0011 | `>>` binary + `>>=` assignment | `>>` binary + `>>=` assignment | -- refused/absent | `>>` binary + `>>=` assignment | -- refused/absent | -- refused/absent | 20 | 0 | 6 | erased-form |
| D0012 | `~` unary_prefix | `compl` unary_prefix + `~` unary_prefix | `^` unary_prefix | `!` unary_prefix | `~` unary_prefix | -- refused/absent | 4 | 0 | 1 | erased-form |
| D0013 | `-` unary_prefix | `-` unary_prefix | `-` unary_prefix | `-` unary_prefix | `-` unary_prefix | -- refused/absent | 6 | 0 | 10 | erased-form |
| D0014 | `=` assignment | `=` assignment | `=` assignment | `=` assignment | `=` assignment | -- refused/absent | 36 | 0 | 0 | sem |
| D0015 | `_Alignof` unary_prefix + `__alignof` unary_prefix + `__alignof__` unary_prefix + `sizeof` unary_prefix | `sizeof` unary_prefix | -- refused/absent | -- refused/absent | -- refused/absent | -- refused/absent | 6 | 0 | 0 | canon-byte |
| D0016 | -- no mutual | `!=` binary + `not_eq` binary | `!=` binary | `!=` binary | `!=` binary | -- refused/absent | 36 | 44 | 26 | erased-form |
| D0017 | -- bridge only | `<` binary | `<` binary | `<` binary | `<` binary | -- refused/absent | 8 | 8 | 15 | erased-form |
| D0018 | -- bridge only | `<=` binary | `<=` binary | `<=` binary | `<=` binary | -- refused/absent | 8 | 8 | 10 | erased-form |
| D0019 | -- bridge only | `==` binary | `==` binary | `==` binary | `==` binary | -- refused/absent | 8 | 8 | 14 | z3 |
| D0020 | -- bridge only | `>` binary | `>` binary | `>` binary | `>` binary | -- refused/absent | 8 | 8 | 9 | erased-form |
| D0021 | -- bridge only | `>=` binary | `>=` binary | `>=` binary | `>=` binary | -- refused/absent | 8 | 8 | 16 | erased-form |
| D0022 | -- refused/absent | -- refused/absent | `%` binary + `%=` assignment | `%` binary + `%=` assignment | -- refused/absent | -- refused/absent | 7 | 0 | 8 | core-text |
| D0023 | -- no mutual | -- no mutual | `&&` binary | `&&` binary | `&&` binary | -- refused/absent | 1 | 0 | 0 | sem |
| D0024 | -- refused/absent | -- refused/absent | `<<` binary + `<<=` assignment | -- refused/absent | `<<` binary | -- refused/absent | 9 | 0 | 18 | z3 |
| D0025 | -- refused/absent | -- refused/absent | `>>` binary + `>>=` assignment | -- refused/absent | `>>` binary | -- refused/absent | 9 | 0 | 12 | z3 |
| D0026 | -- no mutual | -- no mutual | `\|\|` binary | `\|\|` binary | `\|\|` binary | -- refused/absent | 1 | 0 | 0 | sem |
| D0027 | `%` binary | `%` binary | -- refused/absent | -- refused/absent | -- refused/absent | -- refused/absent | 16 | 0 | 0 | erased-form |
| D0028 | `%=` assignment | `%=` assignment | -- refused/absent | -- refused/absent | -- refused/absent | -- refused/absent | 16 | 0 | 0 | erased-form |
| D0029 | `&` unary_prefix | `&` unary_prefix | -- refused/absent | -- refused/absent | -- refused/absent | -- refused/absent | 6 | 0 | 0 | erased-form |
| D0030 | `++` unary_prefix | `++` unary_prefix | -- refused/absent | -- refused/absent | -- refused/absent | -- refused/absent | 5 | 0 | 0 | erased-form |

A cell holding two labels joined by `+` is a same-language collision: the component chained back into a language it had already visited.  Recorded, not resolved -- the owner settles the rule.

nodes 197; edges 609 before the mutual filter, 412 after; dom_ops 30.
