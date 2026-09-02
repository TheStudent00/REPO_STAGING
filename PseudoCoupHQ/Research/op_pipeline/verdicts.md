# the three verdicts

Every row is one operator intention on one operand type pair.  Every cell is one cross-language pair of ship units.

**What each verdict is evidence of.**

- `MATCHED (byte)` is a FACT about these two artifacts: the same machine bytes.  It needs no lifter and no solver.
- `MATCHED (sem)` and `MATCHED (z3)` are bounds over ALL RUNS: the lifted forms are equal as expressions, or z3 proved them equal for every input.  They rest on the lifter being right about what the instructions do.
- `DIFFERS-BY-DESIGN` is an all-runs bound too, and the divergence condition printed with it is read out of the guard's own lifted comparison.
- `UNMATCHED` carries a counterexample: an assignment of the arguments on which the two units disagree.
- `UNDECIDED` carries the reason, in the tool's own words.

**One limit on `UNMATCHED`, stated rather than hidden.** z3 is asked about every bit pattern the registers can hold.  A language's ABI promises less than that -- a `bool` arrives as 0 or 1 and never as 0xFFFFFF00 -- and this pass does NOT put the ABI's promise into the query as a precondition.  A counterexample that only exists outside what the ABI can produce is therefore a real difference between the two BIT FUNCTIONS and not necessarily a difference between the two OPERATORS.  Read the counterexample before reading the verdict.

The OPERAND ANCHOR under all of it -- which register carried `a` -- rests on the ABI rule, on the anchor build's DWARF table (per-artifact testimony, checked probe by probe), and on the forced `a - b` probe.  See `sem_anchored.py --anchor-report`.

lifter: pyvex 9.2.213 / archinfo 9.2.213 / libVEX via ArchAMD64   solver: z3 5.1.0

## excluded

- `dwarf_contradicts_the_anchor`: 3 units
- `fallback_lhs`: 18 units

## tally

| verdict | pairs |
| --- | --- |
| MATCHED | 972 |
| DIFFERS-BY-DESIGN | 60 |
| UNMATCHED | 137 |
| UNDECIDED | 351 |

## the table

| operator | arity | type pair | MATCHED | DIFFERS-BY-DESIGN | UNMATCHED | UNDECIDED |
| --- | --- | --- | --- | --- | --- | --- |
| `!` | unary | bool,None | cpp~go cpp~rust cpp~swift go~rust go~swift rust~swift | - | c~cpp c~go c~rust c~swift | - |
| `!` | unary | f32,None | c~cpp | - | - | - |
| `!` | unary | f64,None | c~cpp | - | - | - |
| `!` | unary | i32,None | c~cpp | - | cpp~rust c~rust | - |
| `!` | unary | i64,None | c~cpp | - | cpp~rust c~rust | - |
| `!` | unary | u64,None | c~cpp | - | cpp~rust c~rust | - |
| `!=` | binary | bool,bool | cpp~rust cpp~swift c~cpp c~rust c~swift rust~swift | - | cpp~go c~go go~rust go~swift | - |
| `!=` | binary | bool,f32 | c~cpp | - | - | - |
| `!=` | binary | bool,f64 | c~cpp | - | - | - |
| `!=` | binary | bool,i32 | c~cpp | - | - | - |
| `!=` | binary | bool,i64 | - | - | c~cpp | - |
| `!=` | binary | bool,u64 | - | - | c~cpp | - |
| `!=` | binary | f32,bool | c~cpp | - | - | - |
| `!=` | binary | f32,f32 | cpp~rust cpp~swift c~cpp c~rust c~swift rust~swift | - | - | cpp~go c~go go~rust go~swift |
| `!=` | binary | f32,f64 | c~cpp | - | - | - |
| `!=` | binary | f32,i32 | c~cpp | - | - | - |
| `!=` | binary | f32,i64 | c~cpp | - | - | - |
| `!=` | binary | f32,u64 | c~cpp | - | - | - |
| `!=` | binary | f64,bool | c~cpp | - | - | - |
| `!=` | binary | f64,f32 | c~cpp | - | - | - |
| `!=` | binary | f64,f64 | cpp~rust cpp~swift c~cpp c~rust c~swift rust~swift | - | - | cpp~go c~go go~rust go~swift |
| `!=` | binary | f64,i32 | c~cpp | - | - | - |
| `!=` | binary | f64,i64 | c~cpp | - | - | - |
| `!=` | binary | f64,u64 | c~cpp | - | - | - |
| `!=` | binary | i32,bool | c~cpp | - | - | - |
| `!=` | binary | i32,f32 | c~cpp | - | - | - |
| `!=` | binary | i32,f64 | c~cpp | - | - | - |
| `!=` | binary | i32,i32 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `!=` | binary | i32,i64 | cpp~swift | - | c~cpp c~swift | - |
| `!=` | binary | i32,u64 | - | - | cpp~swift c~cpp c~swift | - |
| `!=` | binary | i64,bool | - | - | c~cpp | - |
| `!=` | binary | i64,f32 | c~cpp | - | - | - |
| `!=` | binary | i64,f64 | c~cpp | - | - | - |
| `!=` | binary | i64,i32 | cpp~swift | - | c~cpp c~swift | - |
| `!=` | binary | i64,i64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `!=` | binary | i64,u64 | c~cpp | - | cpp~swift c~swift | - |
| `!=` | binary | u64,bool | - | - | c~cpp | - |
| `!=` | binary | u64,f32 | c~cpp | - | - | - |
| `!=` | binary | u64,f64 | c~cpp | - | - | - |
| `!=` | binary | u64,i32 | - | - | cpp~swift c~cpp c~swift | - |
| `!=` | binary | u64,i64 | c~cpp | - | cpp~swift c~swift | - |
| `!=` | binary | u64,u64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `%` | binary | bool,bool | c~cpp | - | - | - |
| `%` | binary | bool,i32 | c~cpp | - | - | - |
| `%` | binary | bool,i64 | c~cpp | - | - | - |
| `%` | binary | bool,u64 | c~cpp | - | - | - |
| `%` | binary | i32,bool | c~cpp | - | - | - |
| `%` | binary | i32,i32 | c~cpp | cpp~rust cpp~swift c~rust c~swift | - | cpp~go c~go go~rust go~swift rust~swift |
| `%` | binary | i32,i64 | c~cpp | - | - | - |
| `%` | binary | i32,u64 | c~cpp | - | - | - |
| `%` | binary | i64,bool | c~cpp | - | - | - |
| `%` | binary | i64,i32 | c~cpp | - | - | - |
| `%` | binary | i64,i64 | c~cpp | cpp~rust c~rust | - | cpp~go cpp~swift c~go c~swift go~rust go~swift rust~swift |
| `%` | binary | i64,u64 | c~cpp | - | - | - |
| `%` | binary | u64,bool | c~cpp | - | - | - |
| `%` | binary | u64,i32 | c~cpp | - | - | - |
| `%` | binary | u64,i64 | c~cpp | - | - | - |
| `%` | binary | u64,u64 | c~cpp | cpp~go cpp~rust c~go c~rust | - | cpp~swift c~swift go~rust go~swift rust~swift |
| `&&` | binary | bool,bool | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `&&` | binary | bool,f32 | - | - | - | c~cpp |
| `&&` | binary | bool,f64 | - | - | - | c~cpp |
| `&&` | binary | bool,i32 | c~cpp | - | - | - |
| `&&` | binary | bool,i64 | c~cpp | - | - | - |
| `&&` | binary | bool,u64 | c~cpp | - | - | - |
| `&&` | binary | f32,bool | - | - | - | c~cpp |
| `&&` | binary | f32,f32 | - | - | - | c~cpp |
| `&&` | binary | f32,f64 | - | - | - | c~cpp |
| `&&` | binary | f32,i32 | - | - | - | c~cpp |
| `&&` | binary | f32,i64 | - | - | - | c~cpp |
| `&&` | binary | f32,u64 | - | - | - | c~cpp |
| `&&` | binary | f64,bool | - | - | - | c~cpp |
| `&&` | binary | f64,f32 | - | - | - | c~cpp |
| `&&` | binary | f64,f64 | - | - | - | c~cpp |
| `&&` | binary | f64,i32 | - | - | - | c~cpp |
| `&&` | binary | f64,i64 | - | - | - | c~cpp |
| `&&` | binary | f64,u64 | - | - | - | c~cpp |
| `&&` | binary | i32,bool | c~cpp | - | - | - |
| `&&` | binary | i32,f32 | - | - | - | c~cpp |
| `&&` | binary | i32,f64 | - | - | - | c~cpp |
| `&&` | binary | i32,i32 | c~cpp | - | - | - |
| `&&` | binary | i32,i64 | c~cpp | - | - | - |
| `&&` | binary | i32,u64 | c~cpp | - | - | - |
| `&&` | binary | i64,bool | c~cpp | - | - | - |
| `&&` | binary | i64,f32 | - | - | - | c~cpp |
| `&&` | binary | i64,f64 | - | - | - | c~cpp |
| `&&` | binary | i64,i32 | c~cpp | - | - | - |
| `&&` | binary | i64,i64 | c~cpp | - | - | - |
| `&&` | binary | i64,u64 | c~cpp | - | - | - |
| `&&` | binary | u64,bool | c~cpp | - | - | - |
| `&&` | binary | u64,f32 | - | - | - | c~cpp |
| `&&` | binary | u64,f64 | - | - | - | c~cpp |
| `&&` | binary | u64,i32 | c~cpp | - | - | - |
| `&&` | binary | u64,i64 | c~cpp | - | - | - |
| `&&` | binary | u64,u64 | c~cpp | - | - | - |
| `&` | binary | bool,bool | cpp~rust c~cpp c~rust | - | - | - |
| `&` | binary | bool,i32 | c~cpp | - | - | - |
| `&` | binary | bool,i64 | c~cpp | - | - | - |
| `&` | binary | bool,u64 | c~cpp | - | - | - |
| `&` | binary | i32,bool | c~cpp | - | - | - |
| `&` | binary | i32,i32 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `&` | binary | i32,i64 | c~cpp | - | - | - |
| `&` | binary | i32,u64 | c~cpp | - | - | - |
| `&` | binary | i64,bool | c~cpp | - | - | - |
| `&` | binary | i64,i32 | c~cpp | - | - | - |
| `&` | binary | i64,i64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `&` | binary | i64,u64 | c~cpp | - | - | - |
| `&` | binary | u64,bool | c~cpp | - | - | - |
| `&` | binary | u64,i32 | c~cpp | - | - | - |
| `&` | binary | u64,i64 | c~cpp | - | - | - |
| `&` | binary | u64,u64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `&` | unary | bool,None | c~cpp | - | - | cpp~go c~go |
| `&` | unary | f32,None | c~cpp | - | - | cpp~go c~go |
| `&` | unary | f64,None | c~cpp | - | - | cpp~go c~go |
| `&` | unary | i32,None | c~cpp | - | - | cpp~go c~go |
| `&` | unary | i64,None | c~cpp | - | - | cpp~go c~go |
| `&` | unary | u64,None | c~cpp | - | - | cpp~go c~go |
| `*` | binary | bool,bool | c~cpp | - | - | - |
| `*` | binary | bool,f32 | c~cpp | - | - | - |
| `*` | binary | bool,f64 | c~cpp | - | - | - |
| `*` | binary | bool,i32 | c~cpp | - | - | - |
| `*` | binary | bool,i64 | c~cpp | - | - | - |
| `*` | binary | bool,u64 | c~cpp | - | - | - |
| `*` | binary | f32,bool | c~cpp | - | - | - |
| `*` | binary | f32,f32 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `*` | binary | f32,f64 | c~cpp | - | - | - |
| `*` | binary | f32,i32 | c~cpp | - | - | - |
| `*` | binary | f32,i64 | c~cpp | - | - | - |
| `*` | binary | f32,u64 | c~cpp | - | - | - |
| `*` | binary | f64,bool | c~cpp | - | - | - |
| `*` | binary | f64,f32 | c~cpp | - | - | - |
| `*` | binary | f64,f64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `*` | binary | f64,i32 | c~cpp | - | - | - |
| `*` | binary | f64,i64 | c~cpp | - | - | - |
| `*` | binary | f64,u64 | c~cpp | - | - | - |
| `*` | binary | i32,bool | c~cpp | - | - | - |
| `*` | binary | i32,f32 | c~cpp | - | - | - |
| `*` | binary | i32,f64 | c~cpp | - | - | - |
| `*` | binary | i32,i32 | cpp~go cpp~rust c~cpp c~go c~rust go~rust | cpp~swift c~swift go~swift rust~swift | - | - |
| `*` | binary | i32,i64 | c~cpp | - | - | - |
| `*` | binary | i32,u64 | c~cpp | - | - | - |
| `*` | binary | i64,bool | c~cpp | - | - | - |
| `*` | binary | i64,f32 | c~cpp | - | - | - |
| `*` | binary | i64,f64 | c~cpp | - | - | - |
| `*` | binary | i64,i32 | c~cpp | - | - | - |
| `*` | binary | i64,i64 | cpp~go cpp~rust c~cpp c~go c~rust go~rust | cpp~swift c~swift go~swift rust~swift | - | - |
| `*` | binary | i64,u64 | c~cpp | - | - | - |
| `*` | binary | u64,bool | c~cpp | - | - | - |
| `*` | binary | u64,f32 | c~cpp | - | - | - |
| `*` | binary | u64,f64 | c~cpp | - | - | - |
| `*` | binary | u64,i32 | c~cpp | - | - | - |
| `*` | binary | u64,i64 | c~cpp | - | - | - |
| `*` | binary | u64,u64 | cpp~go cpp~rust c~cpp c~go c~rust go~rust | - | - | cpp~swift c~swift go~swift rust~swift |
| `+` | binary | bool,bool | c~cpp | - | - | - |
| `+` | binary | bool,f32 | c~cpp | - | - | - |
| `+` | binary | bool,f64 | c~cpp | - | - | - |
| `+` | binary | bool,i32 | c~cpp | - | - | - |
| `+` | binary | bool,i64 | c~cpp | - | - | - |
| `+` | binary | bool,u64 | c~cpp | - | - | - |
| `+` | binary | f32,bool | c~cpp | - | - | - |
| `+` | binary | f32,f32 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `+` | binary | f32,f64 | c~cpp | - | - | - |
| `+` | binary | f32,i32 | c~cpp | - | - | - |
| `+` | binary | f32,i64 | c~cpp | - | - | - |
| `+` | binary | f32,u64 | c~cpp | - | - | - |
| `+` | binary | f64,bool | c~cpp | - | - | - |
| `+` | binary | f64,f32 | c~cpp | - | - | - |
| `+` | binary | f64,f64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `+` | binary | f64,i32 | c~cpp | - | - | - |
| `+` | binary | f64,i64 | c~cpp | - | - | - |
| `+` | binary | f64,u64 | c~cpp | - | - | - |
| `+` | binary | i32,bool | c~cpp | - | - | - |
| `+` | binary | i32,f32 | c~cpp | - | - | - |
| `+` | binary | i32,f64 | c~cpp | - | - | - |
| `+` | binary | i32,i32 | cpp~go cpp~rust c~cpp c~go c~rust go~rust | cpp~swift c~swift go~swift rust~swift | - | - |
| `+` | binary | i32,i64 | c~cpp | - | - | - |
| `+` | binary | i32,u64 | c~cpp | - | - | - |
| `+` | binary | i64,bool | c~cpp | - | - | - |
| `+` | binary | i64,f32 | c~cpp | - | - | - |
| `+` | binary | i64,f64 | c~cpp | - | - | - |
| `+` | binary | i64,i32 | c~cpp | - | - | - |
| `+` | binary | i64,i64 | cpp~go cpp~rust c~cpp c~go c~rust go~rust | cpp~swift c~swift go~swift rust~swift | - | - |
| `+` | binary | i64,u64 | c~cpp | - | - | - |
| `+` | binary | u64,bool | c~cpp | - | - | - |
| `+` | binary | u64,f32 | c~cpp | - | - | - |
| `+` | binary | u64,f64 | c~cpp | - | - | - |
| `+` | binary | u64,i32 | c~cpp | - | - | - |
| `+` | binary | u64,i64 | c~cpp | - | - | - |
| `+` | binary | u64,u64 | cpp~go cpp~rust c~cpp c~go c~rust go~rust | cpp~swift c~swift go~swift rust~swift | - | - |
| `+` | unary | bool,None | c~cpp | - | - | - |
| `+` | unary | f32,None | cpp~go cpp~swift c~cpp c~go c~swift go~swift | - | - | - |
| `+` | unary | f64,None | cpp~go cpp~swift c~cpp c~go c~swift go~swift | - | - | - |
| `+` | unary | i32,None | cpp~swift c~cpp c~swift | - | - | cpp~go c~go go~swift |
| `+` | unary | i64,None | cpp~swift c~cpp c~swift | - | - | cpp~go c~go go~swift |
| `+` | unary | u64,None | cpp~swift c~cpp c~swift | - | - | cpp~go c~go go~swift |
| `++` | unary | f32,None | c~cpp | - | - | - |
| `++` | unary | f64,None | c~cpp | - | - | - |
| `++` | unary | i32,None | c~cpp | - | - | - |
| `++` | unary | i64,None | c~cpp | - | - | - |
| `++` | unary | u64,None | c~cpp | - | - | - |
| `++` | unary | f32,None | c~cpp | - | - | - |
| `++` | unary | f64,None | c~cpp | - | - | - |
| `++` | unary | i32,None | c~cpp | - | - | - |
| `++` | unary | i64,None | c~cpp | - | - | - |
| `++` | unary | u64,None | c~cpp | - | - | - |
| `-` | binary | bool,bool | c~cpp | - | - | - |
| `-` | binary | bool,f32 | c~cpp | - | - | - |
| `-` | binary | bool,f64 | c~cpp | - | - | - |
| `-` | binary | bool,i32 | c~cpp | - | - | - |
| `-` | binary | bool,i64 | c~cpp | - | - | - |
| `-` | binary | bool,u64 | c~cpp | - | - | - |
| `-` | binary | f32,bool | c~cpp | - | - | - |
| `-` | binary | f32,f32 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `-` | binary | f32,f64 | c~cpp | - | - | - |
| `-` | binary | f32,i32 | c~cpp | - | - | - |
| `-` | binary | f32,i64 | c~cpp | - | - | - |
| `-` | binary | f32,u64 | c~cpp | - | - | - |
| `-` | binary | f64,bool | c~cpp | - | - | - |
| `-` | binary | f64,f32 | c~cpp | - | - | - |
| `-` | binary | f64,f64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `-` | binary | f64,i32 | c~cpp | - | - | - |
| `-` | binary | f64,i64 | c~cpp | - | - | - |
| `-` | binary | f64,u64 | c~cpp | - | - | - |
| `-` | binary | i32,bool | c~cpp | - | - | - |
| `-` | binary | i32,f32 | c~cpp | - | - | - |
| `-` | binary | i32,f64 | c~cpp | - | - | - |
| `-` | binary | i32,i32 | cpp~go cpp~rust c~cpp c~go c~rust go~rust | cpp~swift c~swift go~swift rust~swift | - | - |
| `-` | binary | i32,i64 | c~cpp | - | - | - |
| `-` | binary | i32,u64 | c~cpp | - | - | - |
| `-` | binary | i64,bool | c~cpp | - | - | - |
| `-` | binary | i64,f32 | c~cpp | - | - | - |
| `-` | binary | i64,f64 | c~cpp | - | - | - |
| `-` | binary | i64,i32 | c~cpp | - | - | - |
| `-` | binary | i64,i64 | cpp~go cpp~rust c~cpp c~go c~rust go~rust | cpp~swift c~swift go~swift rust~swift | - | - |
| `-` | binary | i64,u64 | c~cpp | - | - | - |
| `-` | binary | u64,bool | c~cpp | - | - | - |
| `-` | binary | u64,f32 | c~cpp | - | - | - |
| `-` | binary | u64,f64 | c~cpp | - | - | - |
| `-` | binary | u64,i32 | c~cpp | - | - | - |
| `-` | binary | u64,i64 | c~cpp | - | - | - |
| `-` | binary | u64,u64 | cpp~go cpp~rust c~cpp c~go c~rust go~rust | cpp~swift c~swift go~swift rust~swift | - | - |
| `-` | unary | bool,None | c~cpp | - | - | - |
| `-` | unary | f32,None | cpp~rust cpp~swift c~cpp c~rust c~swift rust~swift | - | - | cpp~go c~go go~rust go~swift |
| `-` | unary | f64,None | cpp~rust cpp~swift c~cpp c~rust c~swift rust~swift | - | - | cpp~go c~go go~rust go~swift |
| `-` | unary | i32,None | cpp~go cpp~rust c~cpp c~go c~rust go~rust | cpp~swift c~swift go~swift rust~swift | - | - |
| `-` | unary | i64,None | cpp~go cpp~rust c~cpp c~go c~rust go~rust | cpp~swift c~swift go~swift rust~swift | - | - |
| `-` | unary | u64,None | cpp~go c~cpp c~go | - | - | - |
| `--` | unary | f32,None | c~cpp | - | - | - |
| `--` | unary | f64,None | c~cpp | - | - | - |
| `--` | unary | i32,None | c~cpp | - | - | - |
| `--` | unary | i64,None | c~cpp | - | - | - |
| `--` | unary | u64,None | c~cpp | - | - | - |
| `--` | unary | f32,None | c~cpp | - | - | - |
| `--` | unary | f64,None | c~cpp | - | - | - |
| `--` | unary | i32,None | c~cpp | - | - | - |
| `--` | unary | i64,None | c~cpp | - | - | - |
| `--` | unary | u64,None | c~cpp | - | - | - |
| `/` | binary | bool,bool | c~cpp | - | - | - |
| `/` | binary | bool,f32 | c~cpp | - | - | - |
| `/` | binary | bool,f64 | c~cpp | - | - | - |
| `/` | binary | bool,i32 | c~cpp | - | - | - |
| `/` | binary | bool,i64 | c~cpp | - | - | - |
| `/` | binary | bool,u64 | c~cpp | - | - | - |
| `/` | binary | f32,bool | c~cpp | - | - | - |
| `/` | binary | f32,f32 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `/` | binary | f32,f64 | c~cpp | - | - | - |
| `/` | binary | f32,i32 | c~cpp | - | - | - |
| `/` | binary | f32,i64 | c~cpp | - | - | - |
| `/` | binary | f32,u64 | c~cpp | - | - | - |
| `/` | binary | f64,bool | c~cpp | - | - | - |
| `/` | binary | f64,f32 | c~cpp | - | - | - |
| `/` | binary | f64,f64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `/` | binary | f64,i32 | c~cpp | - | - | - |
| `/` | binary | f64,i64 | c~cpp | - | - | - |
| `/` | binary | f64,u64 | c~cpp | - | - | - |
| `/` | binary | i32,bool | c~cpp | - | - | - |
| `/` | binary | i32,f32 | c~cpp | - | - | - |
| `/` | binary | i32,f64 | c~cpp | - | - | - |
| `/` | binary | i32,i32 | c~cpp | cpp~rust cpp~swift c~rust c~swift | - | cpp~go c~go go~rust go~swift rust~swift |
| `/` | binary | i32,i64 | c~cpp | - | - | - |
| `/` | binary | i32,u64 | c~cpp | - | - | - |
| `/` | binary | i64,bool | c~cpp | - | - | - |
| `/` | binary | i64,f32 | c~cpp | - | - | - |
| `/` | binary | i64,f64 | c~cpp | - | - | - |
| `/` | binary | i64,i32 | c~cpp | - | - | - |
| `/` | binary | i64,i64 | c~cpp | cpp~rust c~rust | - | cpp~go cpp~swift c~go c~swift go~rust go~swift rust~swift |
| `/` | binary | i64,u64 | c~cpp | - | - | - |
| `/` | binary | u64,bool | c~cpp | - | - | - |
| `/` | binary | u64,f32 | c~cpp | - | - | - |
| `/` | binary | u64,f64 | c~cpp | - | - | - |
| `/` | binary | u64,i32 | c~cpp | - | - | - |
| `/` | binary | u64,i64 | c~cpp | - | - | - |
| `/` | binary | u64,u64 | c~cpp | cpp~go cpp~rust c~go c~rust | - | cpp~swift c~swift go~rust go~swift rust~swift |
| `<` | binary | bool,bool | cpp~rust | - | c~cpp c~rust | - |
| `<` | binary | bool,f32 | - | - | - | c~cpp |
| `<` | binary | bool,f64 | - | - | - | c~cpp |
| `<` | binary | bool,i32 | c~cpp | - | - | - |
| `<` | binary | bool,i64 | - | - | c~cpp | - |
| `<` | binary | bool,u64 | - | - | c~cpp | - |
| `<` | binary | f32,bool | - | - | - | c~cpp |
| `<` | binary | f32,f32 | cpp~go cpp~rust cpp~swift go~rust go~swift rust~swift | - | - | c~cpp c~go c~rust c~swift |
| `<` | binary | f32,f64 | - | - | - | c~cpp |
| `<` | binary | f32,i32 | - | - | - | c~cpp |
| `<` | binary | f32,i64 | - | - | - | c~cpp |
| `<` | binary | f32,u64 | - | - | - | c~cpp |
| `<` | binary | f64,bool | - | - | - | c~cpp |
| `<` | binary | f64,f32 | - | - | - | c~cpp |
| `<` | binary | f64,f64 | cpp~go cpp~rust cpp~swift go~rust go~swift rust~swift | - | - | c~cpp c~go c~rust c~swift |
| `<` | binary | f64,i32 | - | - | - | c~cpp |
| `<` | binary | f64,i64 | - | - | - | c~cpp |
| `<` | binary | f64,u64 | - | - | - | c~cpp |
| `<` | binary | i32,bool | c~cpp | - | - | - |
| `<` | binary | i32,f32 | - | - | - | c~cpp |
| `<` | binary | i32,f64 | - | - | - | c~cpp |
| `<` | binary | i32,i32 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `<` | binary | i32,i64 | cpp~swift | - | c~cpp c~swift | - |
| `<` | binary | i32,u64 | - | - | cpp~swift c~cpp c~swift | - |
| `<` | binary | i64,bool | - | - | c~cpp | - |
| `<` | binary | i64,f32 | - | - | - | c~cpp |
| `<` | binary | i64,f64 | - | - | - | c~cpp |
| `<` | binary | i64,i32 | cpp~swift | - | c~cpp c~swift | - |
| `<` | binary | i64,i64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `<` | binary | i64,u64 | c~cpp | - | cpp~swift c~swift | - |
| `<` | binary | u64,bool | c~cpp | - | - | - |
| `<` | binary | u64,f32 | - | - | - | c~cpp |
| `<` | binary | u64,f64 | - | - | - | c~cpp |
| `<` | binary | u64,i32 | - | - | cpp~swift c~cpp c~swift | - |
| `<` | binary | u64,i64 | c~cpp | - | cpp~swift c~swift | - |
| `<` | binary | u64,u64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `<<` | binary | bool,bool | c~cpp | - | - | - |
| `<<` | binary | bool,i32 | c~cpp | - | - | - |
| `<<` | binary | bool,i64 | c~cpp | - | - | - |
| `<<` | binary | bool,u64 | c~cpp | - | - | - |
| `<<` | binary | i32,bool | c~cpp | - | - | - |
| `<<` | binary | i32,i32 | cpp~rust c~cpp c~rust | - | - | cpp~go cpp~swift c~go c~swift go~rust go~swift rust~swift |
| `<<` | binary | i32,i64 | cpp~rust c~cpp c~rust | - | - | cpp~go cpp~swift c~go c~swift go~rust go~swift rust~swift |
| `<<` | binary | i32,u64 | cpp~rust c~cpp c~rust | - | - | cpp~go cpp~swift c~go c~swift go~rust go~swift rust~swift |
| `<<` | binary | i64,bool | c~cpp | - | - | - |
| `<<` | binary | i64,i32 | cpp~rust c~cpp c~rust | - | - | cpp~go cpp~swift c~go c~swift go~rust go~swift rust~swift |
| `<<` | binary | i64,i64 | cpp~rust c~cpp c~rust | - | - | cpp~go cpp~swift c~go c~swift go~rust go~swift rust~swift |
| `<<` | binary | i64,u64 | cpp~rust c~cpp c~rust | - | - | cpp~go cpp~swift c~go c~swift go~rust go~swift rust~swift |
| `<<` | binary | u64,bool | c~cpp | - | - | - |
| `<<` | binary | u64,i32 | cpp~rust c~cpp c~rust | - | - | cpp~go cpp~swift c~go c~swift go~rust go~swift rust~swift |
| `<<` | binary | u64,i64 | cpp~rust c~cpp c~rust | - | - | cpp~go cpp~swift c~go c~swift go~rust go~swift rust~swift |
| `<<` | binary | u64,u64 | cpp~rust c~cpp c~rust | - | cpp~swift c~swift rust~swift | cpp~go c~go go~rust go~swift |
| `<=` | binary | bool,bool | cpp~rust | - | c~cpp c~rust | - |
| `<=` | binary | bool,f32 | - | - | - | c~cpp |
| `<=` | binary | bool,f64 | - | - | - | c~cpp |
| `<=` | binary | bool,i32 | c~cpp | - | - | - |
| `<=` | binary | bool,i64 | - | - | c~cpp | - |
| `<=` | binary | bool,u64 | - | - | c~cpp | - |
| `<=` | binary | f32,bool | - | - | - | c~cpp |
| `<=` | binary | f32,f32 | cpp~go cpp~rust cpp~swift go~rust go~swift rust~swift | - | - | c~cpp c~go c~rust c~swift |
| `<=` | binary | f32,f64 | - | - | - | c~cpp |
| `<=` | binary | f32,i32 | - | - | - | c~cpp |
| `<=` | binary | f32,i64 | - | - | - | c~cpp |
| `<=` | binary | f32,u64 | - | - | - | c~cpp |
| `<=` | binary | f64,bool | - | - | - | c~cpp |
| `<=` | binary | f64,f32 | - | - | - | c~cpp |
| `<=` | binary | f64,f64 | cpp~go cpp~rust cpp~swift go~rust go~swift rust~swift | - | - | c~cpp c~go c~rust c~swift |
| `<=` | binary | f64,i32 | - | - | - | c~cpp |
| `<=` | binary | f64,i64 | - | - | - | c~cpp |
| `<=` | binary | f64,u64 | - | - | - | c~cpp |
| `<=` | binary | i32,bool | c~cpp | - | - | - |
| `<=` | binary | i32,f32 | - | - | - | c~cpp |
| `<=` | binary | i32,f64 | - | - | - | c~cpp |
| `<=` | binary | i32,i32 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `<=` | binary | i32,i64 | cpp~swift | - | c~cpp c~swift | - |
| `<=` | binary | i32,u64 | - | - | cpp~swift c~cpp c~swift | - |
| `<=` | binary | i64,bool | - | - | c~cpp | - |
| `<=` | binary | i64,f32 | - | - | - | c~cpp |
| `<=` | binary | i64,f64 | - | - | - | c~cpp |
| `<=` | binary | i64,i32 | cpp~swift | - | c~cpp c~swift | - |
| `<=` | binary | i64,i64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `<=` | binary | i64,u64 | c~cpp | - | cpp~swift c~swift | - |
| `<=` | binary | u64,bool | - | - | c~cpp | - |
| `<=` | binary | u64,f32 | - | - | - | c~cpp |
| `<=` | binary | u64,f64 | - | - | - | c~cpp |
| `<=` | binary | u64,i32 | - | - | cpp~swift c~cpp c~swift | - |
| `<=` | binary | u64,i64 | c~cpp | - | cpp~swift c~swift | - |
| `<=` | binary | u64,u64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `==` | binary | bool,bool | cpp~rust cpp~swift rust~swift | - | cpp~go go~rust go~swift | c~cpp c~go c~rust c~swift |
| `==` | binary | bool,f32 | c~cpp | - | - | - |
| `==` | binary | bool,f64 | c~cpp | - | - | - |
| `==` | binary | bool,i32 | c~cpp | - | - | - |
| `==` | binary | bool,i64 | - | - | c~cpp | - |
| `==` | binary | bool,u64 | - | - | c~cpp | - |
| `==` | binary | f32,bool | c~cpp | - | - | - |
| `==` | binary | f32,f32 | cpp~rust cpp~swift c~cpp c~rust c~swift rust~swift | - | - | cpp~go c~go go~rust go~swift |
| `==` | binary | f32,f64 | c~cpp | - | - | - |
| `==` | binary | f32,i32 | c~cpp | - | - | - |
| `==` | binary | f32,i64 | c~cpp | - | - | - |
| `==` | binary | f32,u64 | c~cpp | - | - | - |
| `==` | binary | f64,bool | c~cpp | - | - | - |
| `==` | binary | f64,f32 | c~cpp | - | - | - |
| `==` | binary | f64,f64 | cpp~rust cpp~swift c~cpp c~rust c~swift rust~swift | - | - | cpp~go c~go go~rust go~swift |
| `==` | binary | f64,i32 | c~cpp | - | - | - |
| `==` | binary | f64,i64 | c~cpp | - | - | - |
| `==` | binary | f64,u64 | c~cpp | - | - | - |
| `==` | binary | i32,bool | c~cpp | - | - | - |
| `==` | binary | i32,f32 | c~cpp | - | - | - |
| `==` | binary | i32,f64 | c~cpp | - | - | - |
| `==` | binary | i32,i32 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `==` | binary | i32,i64 | cpp~swift | - | c~cpp c~swift | - |
| `==` | binary | i32,u64 | - | - | cpp~swift c~cpp c~swift | - |
| `==` | binary | i64,bool | - | - | c~cpp | - |
| `==` | binary | i64,f32 | c~cpp | - | - | - |
| `==` | binary | i64,f64 | c~cpp | - | - | - |
| `==` | binary | i64,i32 | cpp~swift | - | c~cpp c~swift | - |
| `==` | binary | i64,i64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `==` | binary | i64,u64 | c~cpp | - | cpp~swift c~swift | - |
| `==` | binary | u64,bool | - | - | c~cpp | - |
| `==` | binary | u64,f32 | c~cpp | - | - | - |
| `==` | binary | u64,f64 | c~cpp | - | - | - |
| `==` | binary | u64,i32 | - | - | cpp~swift c~cpp c~swift | - |
| `==` | binary | u64,i64 | c~cpp | - | cpp~swift c~swift | - |
| `==` | binary | u64,u64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `>` | binary | bool,bool | cpp~rust | - | c~cpp c~rust | - |
| `>` | binary | bool,f32 | - | - | - | c~cpp |
| `>` | binary | bool,f64 | - | - | - | c~cpp |
| `>` | binary | bool,i32 | c~cpp | - | - | - |
| `>` | binary | bool,i64 | - | - | c~cpp | - |
| `>` | binary | bool,u64 | c~cpp | - | - | - |
| `>` | binary | f32,bool | - | - | - | c~cpp |
| `>` | binary | f32,f32 | cpp~go cpp~rust cpp~swift go~rust go~swift rust~swift | - | - | c~cpp c~go c~rust c~swift |
| `>` | binary | f32,f64 | - | - | - | c~cpp |
| `>` | binary | f32,i32 | - | - | - | c~cpp |
| `>` | binary | f32,i64 | - | - | - | c~cpp |
| `>` | binary | f32,u64 | - | - | - | c~cpp |
| `>` | binary | f64,bool | - | - | - | c~cpp |
| `>` | binary | f64,f32 | - | - | - | c~cpp |
| `>` | binary | f64,f64 | cpp~go cpp~rust cpp~swift go~rust go~swift rust~swift | - | - | c~cpp c~go c~rust c~swift |
| `>` | binary | f64,i32 | - | - | - | c~cpp |
| `>` | binary | f64,i64 | - | - | - | c~cpp |
| `>` | binary | f64,u64 | - | - | - | c~cpp |
| `>` | binary | i32,bool | c~cpp | - | - | - |
| `>` | binary | i32,f32 | - | - | - | c~cpp |
| `>` | binary | i32,f64 | - | - | - | c~cpp |
| `>` | binary | i32,i32 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `>` | binary | i32,i64 | cpp~swift | - | c~cpp c~swift | - |
| `>` | binary | i32,u64 | - | - | cpp~swift c~cpp c~swift | - |
| `>` | binary | i64,bool | - | - | c~cpp | - |
| `>` | binary | i64,f32 | - | - | - | c~cpp |
| `>` | binary | i64,f64 | - | - | - | c~cpp |
| `>` | binary | i64,i32 | cpp~swift | - | c~cpp c~swift | - |
| `>` | binary | i64,i64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `>` | binary | i64,u64 | c~cpp | - | cpp~swift c~swift | - |
| `>` | binary | u64,bool | - | - | c~cpp | - |
| `>` | binary | u64,f32 | - | - | - | c~cpp |
| `>` | binary | u64,f64 | - | - | - | c~cpp |
| `>` | binary | u64,i32 | - | - | cpp~swift c~cpp c~swift | - |
| `>` | binary | u64,i64 | c~cpp | - | cpp~swift c~swift | - |
| `>` | binary | u64,u64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `>=` | binary | bool,bool | cpp~rust | - | c~cpp c~rust | - |
| `>=` | binary | bool,f32 | - | - | - | c~cpp |
| `>=` | binary | bool,f64 | - | - | - | c~cpp |
| `>=` | binary | bool,i32 | c~cpp | - | - | - |
| `>=` | binary | bool,i64 | - | - | c~cpp | - |
| `>=` | binary | bool,u64 | - | - | c~cpp | - |
| `>=` | binary | f32,bool | - | - | - | c~cpp |
| `>=` | binary | f32,f32 | cpp~go cpp~rust cpp~swift go~rust go~swift rust~swift | - | - | c~cpp c~go c~rust c~swift |
| `>=` | binary | f32,f64 | - | - | - | c~cpp |
| `>=` | binary | f32,i32 | - | - | - | c~cpp |
| `>=` | binary | f32,i64 | - | - | - | c~cpp |
| `>=` | binary | f32,u64 | - | - | - | c~cpp |
| `>=` | binary | f64,bool | - | - | - | c~cpp |
| `>=` | binary | f64,f32 | - | - | - | c~cpp |
| `>=` | binary | f64,f64 | cpp~go cpp~rust cpp~swift go~rust go~swift rust~swift | - | - | c~cpp c~go c~rust c~swift |
| `>=` | binary | f64,i32 | - | - | - | c~cpp |
| `>=` | binary | f64,i64 | - | - | - | c~cpp |
| `>=` | binary | f64,u64 | - | - | - | c~cpp |
| `>=` | binary | i32,bool | c~cpp | - | - | - |
| `>=` | binary | i32,f32 | - | - | - | c~cpp |
| `>=` | binary | i32,f64 | - | - | - | c~cpp |
| `>=` | binary | i32,i32 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `>=` | binary | i32,i64 | cpp~swift | - | c~cpp c~swift | - |
| `>=` | binary | i32,u64 | - | - | cpp~swift c~cpp c~swift | - |
| `>=` | binary | i64,bool | - | - | c~cpp | - |
| `>=` | binary | i64,f32 | - | - | - | c~cpp |
| `>=` | binary | i64,f64 | - | - | - | c~cpp |
| `>=` | binary | i64,i32 | cpp~swift | - | c~cpp c~swift | - |
| `>=` | binary | i64,i64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `>=` | binary | i64,u64 | c~cpp | - | cpp~swift c~swift | - |
| `>=` | binary | u64,bool | - | - | c~cpp | - |
| `>=` | binary | u64,f32 | - | - | - | c~cpp |
| `>=` | binary | u64,f64 | - | - | - | c~cpp |
| `>=` | binary | u64,i32 | - | - | cpp~swift c~cpp c~swift | - |
| `>=` | binary | u64,i64 | c~cpp | - | cpp~swift c~swift | - |
| `>=` | binary | u64,u64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `>>` | binary | bool,bool | c~cpp | - | - | - |
| `>>` | binary | bool,i32 | c~cpp | - | - | - |
| `>>` | binary | bool,i64 | c~cpp | - | - | - |
| `>>` | binary | bool,u64 | c~cpp | - | - | - |
| `>>` | binary | i32,bool | c~cpp | - | - | - |
| `>>` | binary | i32,i32 | cpp~rust c~cpp c~rust | - | - | cpp~go cpp~swift c~go c~swift go~rust go~swift rust~swift |
| `>>` | binary | i32,i64 | cpp~rust c~cpp c~rust | - | - | cpp~go cpp~swift c~go c~swift go~rust go~swift rust~swift |
| `>>` | binary | i32,u64 | cpp~rust c~cpp c~rust | - | - | cpp~go cpp~swift c~go c~swift go~rust go~swift rust~swift |
| `>>` | binary | i64,bool | c~cpp | - | - | - |
| `>>` | binary | i64,i32 | cpp~rust c~cpp c~rust | - | - | cpp~go cpp~swift c~go c~swift go~rust go~swift rust~swift |
| `>>` | binary | i64,i64 | cpp~rust c~cpp c~rust | - | - | cpp~go cpp~swift c~go c~swift go~rust go~swift rust~swift |
| `>>` | binary | i64,u64 | cpp~rust c~cpp c~rust | - | - | cpp~go cpp~swift c~go c~swift go~rust go~swift rust~swift |
| `>>` | binary | u64,bool | c~cpp | - | - | - |
| `>>` | binary | u64,i32 | cpp~rust c~cpp c~rust | - | - | cpp~go cpp~swift c~go c~swift go~rust go~swift rust~swift |
| `>>` | binary | u64,i64 | cpp~rust c~cpp c~rust | - | - | cpp~go cpp~swift c~go c~swift go~rust go~swift rust~swift |
| `>>` | binary | u64,u64 | cpp~rust c~cpp c~rust | - | cpp~swift c~swift rust~swift | cpp~go c~go go~rust go~swift |
| `^` | binary | bool,bool | cpp~rust c~cpp c~rust | - | - | - |
| `^` | binary | bool,i32 | c~cpp | - | - | - |
| `^` | binary | bool,i64 | c~cpp | - | - | - |
| `^` | binary | bool,u64 | c~cpp | - | - | - |
| `^` | binary | i32,bool | c~cpp | - | - | - |
| `^` | binary | i32,i32 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `^` | binary | i32,i64 | c~cpp | - | - | - |
| `^` | binary | i32,u64 | c~cpp | - | - | - |
| `^` | binary | i64,bool | c~cpp | - | - | - |
| `^` | binary | i64,i32 | c~cpp | - | - | - |
| `^` | binary | i64,i64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `^` | binary | i64,u64 | c~cpp | - | - | - |
| `^` | binary | u64,bool | c~cpp | - | - | - |
| `^` | binary | u64,i32 | c~cpp | - | - | - |
| `^` | binary | u64,i64 | c~cpp | - | - | - |
| `^` | binary | u64,u64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `sizeof` | unary | bool,None | c~cpp | - | - | - |
| `sizeof` | unary | f32,None | c~cpp | - | - | - |
| `sizeof` | unary | f64,None | c~cpp | - | - | - |
| `sizeof` | unary | i32,None | c~cpp | - | - | - |
| `sizeof` | unary | i64,None | c~cpp | - | - | - |
| `sizeof` | unary | u64,None | c~cpp | - | - | - |
| `|` | binary | bool,bool | cpp~rust c~cpp c~rust | - | - | - |
| `|` | binary | bool,i32 | c~cpp | - | - | - |
| `|` | binary | bool,i64 | c~cpp | - | - | - |
| `|` | binary | bool,u64 | c~cpp | - | - | - |
| `|` | binary | i32,bool | c~cpp | - | - | - |
| `|` | binary | i32,i32 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `|` | binary | i32,i64 | c~cpp | - | - | - |
| `|` | binary | i32,u64 | c~cpp | - | - | - |
| `|` | binary | i64,bool | c~cpp | - | - | - |
| `|` | binary | i64,i32 | c~cpp | - | - | - |
| `|` | binary | i64,i64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `|` | binary | i64,u64 | c~cpp | - | - | - |
| `|` | binary | u64,bool | c~cpp | - | - | - |
| `|` | binary | u64,i32 | c~cpp | - | - | - |
| `|` | binary | u64,i64 | c~cpp | - | - | - |
| `|` | binary | u64,u64 | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `||` | binary | bool,bool | cpp~go cpp~rust cpp~swift c~cpp c~go c~rust c~swift go~rust go~swift rust~swift | - | - | - |
| `||` | binary | bool,f32 | - | - | - | c~cpp |
| `||` | binary | bool,f64 | - | - | - | c~cpp |
| `||` | binary | bool,i32 | c~cpp | - | - | - |
| `||` | binary | bool,i64 | c~cpp | - | - | - |
| `||` | binary | bool,u64 | c~cpp | - | - | - |
| `||` | binary | f32,bool | - | - | - | c~cpp |
| `||` | binary | f32,f32 | - | - | - | c~cpp |
| `||` | binary | f32,f64 | - | - | - | c~cpp |
| `||` | binary | f32,i32 | - | - | - | c~cpp |
| `||` | binary | f32,i64 | - | - | - | c~cpp |
| `||` | binary | f32,u64 | - | - | - | c~cpp |
| `||` | binary | f64,bool | - | - | - | c~cpp |
| `||` | binary | f64,f32 | - | - | - | c~cpp |
| `||` | binary | f64,f64 | - | - | - | c~cpp |
| `||` | binary | f64,i32 | - | - | - | c~cpp |
| `||` | binary | f64,i64 | - | - | - | c~cpp |
| `||` | binary | f64,u64 | - | - | - | c~cpp |
| `||` | binary | i32,bool | c~cpp | - | - | - |
| `||` | binary | i32,f32 | - | - | - | c~cpp |
| `||` | binary | i32,f64 | - | - | - | c~cpp |
| `||` | binary | i32,i32 | c~cpp | - | - | - |
| `||` | binary | i32,i64 | c~cpp | - | - | - |
| `||` | binary | i32,u64 | c~cpp | - | - | - |
| `||` | binary | i64,bool | c~cpp | - | - | - |
| `||` | binary | i64,f32 | - | - | - | c~cpp |
| `||` | binary | i64,f64 | - | - | - | c~cpp |
| `||` | binary | i64,i32 | c~cpp | - | - | - |
| `||` | binary | i64,i64 | c~cpp | - | - | - |
| `||` | binary | i64,u64 | c~cpp | - | - | - |
| `||` | binary | u64,bool | c~cpp | - | - | - |
| `||` | binary | u64,f32 | - | - | - | c~cpp |
| `||` | binary | u64,f64 | - | - | - | c~cpp |
| `||` | binary | u64,i32 | c~cpp | - | - | - |
| `||` | binary | u64,i64 | c~cpp | - | - | - |
| `||` | binary | u64,u64 | c~cpp | - | - | - |
| `~` | unary | bool,None | c~cpp | - | - | - |
| `~` | unary | i32,None | cpp~swift c~cpp c~swift | - | - | - |
| `~` | unary | i64,None | cpp~swift c~cpp c~swift | - | - | - |
| `~` | unary | u64,None | cpp~swift c~cpp c~swift | - | - | - |

## divergence conditions

- **rust `%` on i32,i32** guards where **c** does not.  Branch `je -> B3` lands in `call *_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero(%rip)`.  Divergence condition: **in1 == 0**
  - lifted: `ex1@0(amd64g_calculate_condition(4:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64))`
- **rust `%` on i32,i32** guards where **c** does not.  Branch `je -> B4` lands in `call *_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow(%rip)`.  Divergence condition: **((-2147483648 + in0) | ~in1) == 0**
  - lifted: `ex1@0(amd64g_calculate_condition(4:64,19:64,zx64(Or32(Add32(2147483648:32,ex32@0(in0:64)),Not32(ex32@0(in1:64)))),0:64,u0:64))`
- **swift `%` on i32,i32** guards where **c** does not.  Branch `je -> B4` lands in `trap ud2`.  Divergence condition: **in1 == 0**
  - lifted: `ex1@0(amd64g_calculate_condition(4:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64))`
- **swift `%` on i32,i32** guards where **c** does not.  Branch `je -> B5` lands in `trap ud2`.  Divergence condition: **in1 == -1**
  - lifted: `ex1@0(amd64g_calculate_condition(4:64,7:64,zx64(ex32@0(in1:64)),4294967295:64,u0:64))`
- **rust `%` on i64,i64** guards where **c** does not.  Branch `je -> B3` lands in `call *_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero(%rip)`.  Divergence condition: **in1 == 0**
  - lifted: `ex1@0(amd64g_calculate_condition(4:64,20:64,in1:64,0:64,u0:64))`
- **rust `%` on i64,i64** guards where **c** does not.  Branch `je -> B4` lands in `call *_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_rem_overflow(%rip)`.  Divergence condition: **(~in1 | (-9223372036854775808 ^ in0)) == 0**
  - lifted: `ex1@0(amd64g_calculate_condition(4:64,20:64,Or64(Not64(in1:64),Xor64(9223372036854775808:64,in0:64)),0:64,u0:64))`
- **go `%` on u64,u64** guards where **c** does not.  Branch `je -> B2` lands in `call runtime.panicdivide`.  Divergence condition: **in1 == 0**
  - lifted: `ex1@0(amd64g_calculate_condition(4:64,20:64,in1:64,0:64,u0:64))`
- **rust `%` on u64,u64** guards where **c** does not.  Branch `je -> B2` lands in `call *_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_rem_by_zero(%rip)`.  Divergence condition: **in1 == 0**
  - lifted: `ex1@0(amd64g_calculate_condition(4:64,20:64,in1:64,0:64,u0:64))`
- **swift `*` on i32,i32** guards where **c** does not.  Branch `jo -> B2` lands in `trap ud2`.  Divergence condition: **in1 * in0 overflows 32 bits (signed)**
  - lifted: `ex1@0(amd64g_calculate_condition(0:64,51:64,zx64(ex32@0(in1:64)),zx64(ex32@0(in0:64)),u0:64))`
- **swift `*` on i64,i64** guards where **c** does not.  Branch `jo -> B2` lands in `trap ud2`.  Divergence condition: **in1 * in0 overflows 64 bits (signed)**
  - lifted: `ex1@0(amd64g_calculate_condition(0:64,52:64,in1:64,in0:64,u0:64))`
- **swift `+` on i32,i32** guards where **c** does not.  Branch `jo -> B2` lands in `trap ud2`.  Divergence condition: **in0 + in1 overflows 32 bits (signed)**
  - lifted: `ex1@0(amd64g_calculate_condition(0:64,3:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64))`
- **swift `+` on i64,i64** guards where **c** does not.  Branch `jo -> B2` lands in `trap ud2`.  Divergence condition: **in0 + in1 overflows 64 bits (signed)**
  - lifted: `ex1@0(amd64g_calculate_condition(0:64,4:64,in0:64,in1:64,u0:64))`
- **swift `+` on u64,u64** guards where **c** does not.  Branch `jb -> B2` lands in `trap ud2`.  Divergence condition: **in0 + in1 carries out of 64 bits (unsigned)**
  - lifted: `ex1@0(amd64g_calculate_condition(2:64,4:64,in0:64,in1:64,u0:64))`
- **swift `-` on i32,i32** guards where **c** does not.  Branch `jo -> B2` lands in `trap ud2`.  Divergence condition: **in0 - in1 overflows 32 bits (signed)**
  - lifted: `ex1@0(amd64g_calculate_condition(0:64,7:64,zx64(ex32@0(in0:64)),zx64(ex32@0(in1:64)),u0:64))`
- **swift `-` on i64,i64** guards where **c** does not.  Branch `jo -> B2` lands in `trap ud2`.  Divergence condition: **in0 - in1 overflows 64 bits (signed)**
  - lifted: `ex1@0(amd64g_calculate_condition(0:64,8:64,in0:64,in1:64,u0:64))`
- **swift `-` on u64,u64** guards where **c** does not.  Branch `jb -> B2` lands in `trap ud2`.  Divergence condition: **in0 < in1 (unsigned)**
  - lifted: `ex1@0(amd64g_calculate_condition(2:64,8:64,in0:64,in1:64,u0:64))`
- **swift `-` on i32,None** guards where **c** does not.  Branch `jo -> B2` lands in `trap ud2`.  Divergence condition: **0 - in0 overflows 32 bits (signed)**
  - lifted: `ex1@0(amd64g_calculate_condition(0:64,7:64,0:64,zx64(ex32@0(in0:64)),u0:64))`
- **swift `-` on i64,None** guards where **c** does not.  Branch `jo -> B2` lands in `trap ud2`.  Divergence condition: **0 - in0 overflows 64 bits (signed)**
  - lifted: `ex1@0(amd64g_calculate_condition(0:64,8:64,0:64,in0:64,u0:64))`
- **rust `/` on i32,i32** guards where **c** does not.  Branch `je -> B3` lands in `call *_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero(%rip)`.  Divergence condition: **in1 == 0**
  - lifted: `ex1@0(amd64g_calculate_condition(4:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64))`
- **rust `/` on i32,i32** guards where **c** does not.  Branch `je -> B4` lands in `call *_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow(%rip)`.  Divergence condition: **((-2147483648 + in0) | ~in1) == 0**
  - lifted: `ex1@0(amd64g_calculate_condition(4:64,19:64,zx64(Or32(Add32(2147483648:32,ex32@0(in0:64)),Not32(ex32@0(in1:64)))),0:64,u0:64))`
- **swift `/` on i32,i32** guards where **c** does not.  Branch `je -> B4` lands in `trap ud2`.  Divergence condition: **in1 == 0**
  - lifted: `ex1@0(amd64g_calculate_condition(4:64,19:64,zx64(ex32@0(in1:64)),0:64,u0:64))`
- **swift `/` on i32,i32** guards where **c** does not.  Branch `je -> B5` lands in `trap ud2`.  Divergence condition: **in1 == -1**
  - lifted: `ex1@0(amd64g_calculate_condition(4:64,7:64,zx64(ex32@0(in1:64)),4294967295:64,u0:64))`
- **rust `/` on i64,i64** guards where **c** does not.  Branch `je -> B3` lands in `call *_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero(%rip)`.  Divergence condition: **in1 == 0**
  - lifted: `ex1@0(amd64g_calculate_condition(4:64,20:64,in1:64,0:64,u0:64))`
- **rust `/` on i64,i64** guards where **c** does not.  Branch `je -> B4` lands in `call *_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const24panic_const_div_overflow(%rip)`.  Divergence condition: **(~in1 | (-9223372036854775808 ^ in0)) == 0**
  - lifted: `ex1@0(amd64g_calculate_condition(4:64,20:64,Or64(Not64(in1:64),Xor64(9223372036854775808:64,in0:64)),0:64,u0:64))`
- **go `/` on u64,u64** guards where **c** does not.  Branch `je -> B2` lands in `call runtime.panicdivide`.  Divergence condition: **in1 == 0**
  - lifted: `ex1@0(amd64g_calculate_condition(4:64,20:64,in1:64,0:64,u0:64))`
- **rust `/` on u64,u64** guards where **c** does not.  Branch `je -> B2` lands in `call *_RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero(%rip)`.  Divergence condition: **in1 == 0**
  - lifted: `ex1@0(amd64g_calculate_condition(4:64,20:64,in1:64,0:64,u0:64))`

## every pair

### `!` unary on (bool,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_5 | cpp/op_5 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| c/op_5 | go/op_17 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| c/op_5 | rust/op_17 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| c/op_5 | swift/op_29 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| cpp/op_5 | go/op_17 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_5 | rust/op_17 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_5 | swift/op_29 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_17 | rust/op_17 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_17 | swift/op_29 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| rust/op_17 | swift/op_29 | MATCHED | byte identity | the two units are the same machine bytes |

### `!` unary on (f32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_3 | cpp/op_3 | MATCHED | byte identity | the two units are the same machine bytes |

### `!` unary on (f64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_4 | cpp/op_4 | MATCHED | byte identity | the two units are the same machine bytes |

### `!` unary on (i32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_0 | cpp/op_0 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_0 | rust/op_12 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 2147483648 |
| cpp/op_0 | rust/op_12 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 906371808 |

### `!` unary on (i64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_1 | cpp/op_1 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_1 | rust/op_13 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4 |
| cpp/op_1 | rust/op_13 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 3891992918388001782 |

### `!` unary on (u64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_2 | cpp/op_2 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_2 | rust/op_14 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 9179137105570694002 |
| cpp/op_2 | rust/op_14 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 3891992918388001782 |

### `!=` binary on (bool,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_533 | cpp/op_533 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_533 | go/op_527 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 250, in1_64 = 4 |
| c/op_533 | rust/op_317 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_533 | swift/op_473 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_533 | go/op_527 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 3, in1_64 = 248 |
| cpp/op_533 | rust/op_317 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_533 | swift/op_473 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_527 | rust/op_317 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 0, in1_64 = 255 |
| go/op_527 | swift/op_473 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 0, in1_64 = 255 |
| rust/op_317 | swift/op_473 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (bool,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_531 | cpp/op_531 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (bool,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_532 | cpp/op_532 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (bool,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_528 | cpp/op_528 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `!=` binary on (bool,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_529 | cpp/op_529 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |

### `!=` binary on (bool,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_530 | cpp/op_530 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |

### `!=` binary on (f32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_521 | cpp/op_521 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (f32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_519 | cpp/op_519 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_519 | go/op_513 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: XorV128 |
| c/op_519 | rust/op_303 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_519 | swift/op_459 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_519 | go/op_513 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: XorV128 |
| cpp/op_519 | rust/op_303 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_519 | swift/op_459 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_513 | rust/op_303 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| go/op_513 | swift/op_459 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| rust/op_303 | swift/op_459 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (f32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_520 | cpp/op_520 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (f32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_516 | cpp/op_516 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (f32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_517 | cpp/op_517 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (f32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_518 | cpp/op_518 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (f64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_527 | cpp/op_527 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (f64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_525 | cpp/op_525 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (f64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_526 | cpp/op_526 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_526 | go/op_520 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: XorV128 |
| c/op_526 | rust/op_310 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_526 | swift/op_466 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_526 | go/op_520 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: XorV128 |
| cpp/op_526 | rust/op_310 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_526 | swift/op_466 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_520 | rust/op_310 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| go/op_520 | swift/op_466 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| rust/op_310 | swift/op_466 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (f64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_522 | cpp/op_522 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (f64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_523 | cpp/op_523 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (f64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_524 | cpp/op_524 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (i32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_503 | cpp/op_503 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `!=` binary on (i32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_501 | cpp/op_501 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (i32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_502 | cpp/op_502 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (i32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_498 | cpp/op_498 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_498 | go/op_492 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_498 | rust/op_282 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_498 | swift/op_438 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| cpp/op_498 | go/op_492 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_498 | rust/op_282 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_498 | swift/op_438 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_492 | rust/op_282 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_492 | swift/op_438 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| rust/op_282 | swift/op_438 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (i32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_499 | cpp/op_499 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| c/op_499 | swift/op_439 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4278189824, in1_64 = 16777471 |
| cpp/op_499 | swift/op_439 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |

### `!=` binary on (i32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_500 | cpp/op_500 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| c/op_500 | swift/op_440 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 2147483648, in1_64 = 0 |
| cpp/op_500 | swift/op_440 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 2147483648, in1_64 = 18446744071562067968 |

### `!=` binary on (i64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_509 | cpp/op_509 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |

### `!=` binary on (i64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_507 | cpp/op_507 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (i64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_508 | cpp/op_508 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (i64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_504 | cpp/op_504 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |
| c/op_504 | swift/op_444 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 61, in1_64 = 4294967234 |
| cpp/op_504 | swift/op_444 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |

### `!=` binary on (i64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_505 | cpp/op_505 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_505 | go/op_499 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_505 | rust/op_289 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_505 | swift/op_445 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| cpp/op_505 | go/op_499 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_505 | rust/op_289 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_505 | swift/op_445 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_499 | rust/op_289 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_499 | swift/op_445 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| rust/op_289 | swift/op_445 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (i64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_506 | cpp/op_506 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_506 | swift/op_446 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18446744073709551615, in1_64 = 18446744073709551615 |
| cpp/op_506 | swift/op_446 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18446744073709551615, in1_64 = 18446744073709551615 |

### `!=` binary on (u64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_515 | cpp/op_515 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |

### `!=` binary on (u64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_513 | cpp/op_513 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (u64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_514 | cpp/op_514 | MATCHED | byte identity | the two units are the same machine bytes |

### `!=` binary on (u64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_510 | cpp/op_510 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |
| c/op_510 | swift/op_450 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 0, in1_64 = 2147483648 |
| cpp/op_510 | swift/op_450 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18446744071562067968, in1_64 = 2147483648 |

### `!=` binary on (u64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_511 | cpp/op_511 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_511 | swift/op_451 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18446744073709551615, in1_64 = 18446744073709551615 |
| cpp/op_511 | swift/op_451 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18446744073709551615, in1_64 = 18446744073709551615 |

### `!=` binary on (u64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_512 | cpp/op_512 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_512 | go/op_506 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_512 | rust/op_296 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_512 | swift/op_452 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| cpp/op_512 | go/op_506 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_512 | rust/op_296 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_512 | swift/op_452 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_506 | rust/op_296 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_506 | swift/op_452 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| rust/op_296 | swift/op_452 | MATCHED | byte identity | the two units are the same machine bytes |

### `%` binary on (bool,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_281 | cpp/op_281 | MATCHED | byte identity | the two units are the same machine bytes |

### `%` binary on (bool,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_276 | cpp/op_276 | MATCHED | byte identity | the two units are the same machine bytes |

### `%` binary on (bool,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_277 | cpp/op_277 | MATCHED | byte identity | the two units are the same machine bytes |

### `%` binary on (bool,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_278 | cpp/op_278 | MATCHED | byte identity | the two units are the same machine bytes |

### `%` binary on (i32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_251 | cpp/op_251 | MATCHED | byte identity | the two units are the same machine bytes |

### `%` binary on (i32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_246 | cpp/op_246 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_246 | go/op_132 | UNDECIDED | one side guards but the cores are not equal | core of c op_246 is ['zx64(ex32@32(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64))))', 'zx64(ex32@32(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64))))']; core of go op_132 is ['zx64(Sub32(0:32,ex32@0(in0:64)))', 'zx64(ex32@0(DivModS |
| c/op_246 | rust/op_678 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | rust op_678 guards; c op_246 does not; the arithmetic core is sem-equal |
| c/op_246 | swift/op_186 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_186 guards; c op_246 does not; the arithmetic core is sem-equal |
| cpp/op_246 | go/op_132 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_246 is ['zx64(ex32@32(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64))))', 'zx64(ex32@32(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64))))']; core of go op_132 is ['zx64(Sub32(0:32,ex32@0(in0:64)))', 'zx64(ex32@0(DivMo |
| cpp/op_246 | rust/op_678 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | rust op_678 guards; cpp op_246 does not; the arithmetic core is sem-equal |
| cpp/op_246 | swift/op_186 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_186 guards; cpp op_246 does not; the arithmetic core is sem-equal |
| go/op_132 | rust/op_678 | UNDECIDED | both sides carry a guard | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |
| go/op_132 | swift/op_186 | UNDECIDED | both sides carry a guard | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |
| rust/op_678 | swift/op_186 | UNDECIDED | both sides carry a guard | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |

### `%` binary on (i32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_247 | cpp/op_247 | MATCHED | byte identity | the two units are the same machine bytes |

### `%` binary on (i32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_248 | cpp/op_248 | MATCHED | byte identity | the two units are the same machine bytes |

### `%` binary on (i64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_257 | cpp/op_257 | MATCHED | byte identity | the two units are the same machine bytes |

### `%` binary on (i64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_252 | cpp/op_252 | MATCHED | byte identity | the two units are the same machine bytes |

### `%` binary on (i64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_253 | cpp/op_253 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_253 | go/op_139 | UNDECIDED | one side guards but the cores are not equal | core of c op_253 is ['ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))']; core of go op_139 is ['Sub64(0:64,in0:64)', 'ex64@0(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'ex64@64(DivModS128 |
| c/op_253 | rust/op_685 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | rust op_685 guards; c op_253 does not; the arithmetic core is sem-equal |
| c/op_253 | swift/op_193 | UNDECIDED | one side guards but the cores are not equal | core of c op_253 is ['ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))']; core of swift op_193 is ['Shr64(Or64(in0:64,in1:64),32:8)', 'ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'e |
| cpp/op_253 | go/op_139 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_253 is ['ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))']; core of go op_139 is ['Sub64(0:64,in0:64)', 'ex64@0(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'ex64@64(DivModS1 |
| cpp/op_253 | rust/op_685 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | rust op_685 guards; cpp op_253 does not; the arithmetic core is sem-equal |
| cpp/op_253 | swift/op_193 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_253 is ['ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))']; core of swift op_193 is ['Shr64(Or64(in0:64,in1:64),32:8)', 'ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))',  |
| go/op_139 | rust/op_685 | UNDECIDED | both sides carry a guard | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |
| go/op_139 | swift/op_193 | UNDECIDED | both sides carry a guard | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |
| rust/op_685 | swift/op_193 | UNDECIDED | both sides carry a guard | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |

### `%` binary on (i64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_254 | cpp/op_254 | MATCHED | byte identity | the two units are the same machine bytes |

### `%` binary on (u64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_263 | cpp/op_263 | MATCHED | byte identity | the two units are the same machine bytes |

### `%` binary on (u64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_258 | cpp/op_258 | MATCHED | byte identity | the two units are the same machine bytes |

### `%` binary on (u64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_259 | cpp/op_259 | MATCHED | byte identity | the two units are the same machine bytes |

### `%` binary on (u64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_260 | cpp/op_260 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_260 | go/op_146 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | go op_146 guards; c op_260 does not; the arithmetic core is sem-equal |
| c/op_260 | rust/op_692 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | rust op_692 guards; c op_260 does not; the arithmetic core is sem-equal |
| c/op_260 | swift/op_200 | UNDECIDED | one side guards but the cores are not equal | core of c op_260 is ['ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64))', 'ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64))']; core of swift op_200 is ['Shr64(Or64(in0:64,in1:64),32:8)', 'ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64))', 'ex64@64(DivModU128to64(64HLto128(0:64,in0:6 |
| cpp/op_260 | go/op_146 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | go op_146 guards; cpp op_260 does not; the arithmetic core is sem-equal |
| cpp/op_260 | rust/op_692 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | rust op_692 guards; cpp op_260 does not; the arithmetic core is sem-equal |
| cpp/op_260 | swift/op_200 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_260 is ['ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64))', 'ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64))']; core of swift op_200 is ['Shr64(Or64(in0:64,in1:64),32:8)', 'ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64))', 'ex64@64(DivModU128to64(64HLto128(0:64,in0 |
| go/op_146 | rust/op_692 | UNDECIDED | both sides carry a guard | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |
| go/op_146 | swift/op_200 | UNDECIDED | both sides carry a guard | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |
| rust/op_692 | swift/op_200 | UNDECIDED | both sides carry a guard | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |

### `&&` binary on (bool,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_353 | cpp/op_353 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_353 | go/op_707 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_353 | rust/op_101 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_353 | swift/op_797 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_353 | go/op_707 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_353 | rust/op_101 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_353 | swift/op_797 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_707 | rust/op_101 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_707 | swift/op_797 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| rust/op_101 | swift/op_797 | MATCHED | byte identity | the two units are the same machine bytes |

### `&&` binary on (bool,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_351 | cpp/op_351 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `&&` binary on (bool,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_352 | cpp/op_352 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |

### `&&` binary on (bool,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_348 | cpp/op_348 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `&&` binary on (bool,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_349 | cpp/op_349 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `&&` binary on (bool,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_350 | cpp/op_350 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `&&` binary on (f32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_341 | cpp/op_341 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `&&` binary on (f32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_339 | cpp/op_339 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: XorV128 |

### `&&` binary on (f32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_340 | cpp/op_340 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `&&` binary on (f32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_336 | cpp/op_336 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `&&` binary on (f32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_337 | cpp/op_337 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `&&` binary on (f32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_338 | cpp/op_338 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `&&` binary on (f64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_347 | cpp/op_347 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |

### `&&` binary on (f64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_345 | cpp/op_345 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `&&` binary on (f64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_346 | cpp/op_346 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: XorV128 |

### `&&` binary on (f64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_342 | cpp/op_342 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |

### `&&` binary on (f64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_343 | cpp/op_343 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |

### `&&` binary on (f64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_344 | cpp/op_344 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |

### `&&` binary on (i32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_323 | cpp/op_323 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `&&` binary on (i32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_321 | cpp/op_321 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `&&` binary on (i32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_322 | cpp/op_322 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |

### `&&` binary on (i32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_318 | cpp/op_318 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `&&` binary on (i32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_319 | cpp/op_319 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `&&` binary on (i32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_320 | cpp/op_320 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `&&` binary on (i64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_329 | cpp/op_329 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `&&` binary on (i64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_327 | cpp/op_327 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `&&` binary on (i64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_328 | cpp/op_328 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |

### `&&` binary on (i64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_324 | cpp/op_324 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `&&` binary on (i64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_325 | cpp/op_325 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `&&` binary on (i64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_326 | cpp/op_326 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `&&` binary on (u64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_335 | cpp/op_335 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `&&` binary on (u64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_333 | cpp/op_333 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `&&` binary on (u64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_334 | cpp/op_334 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |

### `&&` binary on (u64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_330 | cpp/op_330 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `&&` binary on (u64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_331 | cpp/op_331 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `&&` binary on (u64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_332 | cpp/op_332 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `&` binary on (bool,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_461 | cpp/op_461 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_461 | rust/op_173 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_461 | rust/op_173 | MATCHED | byte identity | the two units are the same machine bytes |

### `&` binary on (bool,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_456 | cpp/op_456 | MATCHED | byte identity | the two units are the same machine bytes |

### `&` binary on (bool,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_457 | cpp/op_457 | MATCHED | byte identity | the two units are the same machine bytes |

### `&` binary on (bool,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_458 | cpp/op_458 | MATCHED | byte identity | the two units are the same machine bytes |

### `&` binary on (i32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_431 | cpp/op_431 | MATCHED | byte identity | the two units are the same machine bytes |

### `&` binary on (i32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_426 | cpp/op_426 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_426 | go/op_240 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_426 | rust/op_138 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_426 | swift/op_582 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_426 | go/op_240 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_426 | rust/op_138 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_426 | swift/op_582 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_240 | rust/op_138 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_240 | swift/op_582 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| rust/op_138 | swift/op_582 | MATCHED | byte identity | the two units are the same machine bytes |

### `&` binary on (i32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_427 | cpp/op_427 | MATCHED | byte identity | the two units are the same machine bytes |

### `&` binary on (i32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_428 | cpp/op_428 | MATCHED | byte identity | the two units are the same machine bytes |

### `&` binary on (i64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_437 | cpp/op_437 | MATCHED | byte identity | the two units are the same machine bytes |

### `&` binary on (i64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_432 | cpp/op_432 | MATCHED | byte identity | the two units are the same machine bytes |

### `&` binary on (i64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_433 | cpp/op_433 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_433 | go/op_247 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_433 | rust/op_145 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_433 | swift/op_589 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_433 | go/op_247 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_433 | rust/op_145 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_433 | swift/op_589 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_247 | rust/op_145 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_247 | swift/op_589 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| rust/op_145 | swift/op_589 | MATCHED | byte identity | the two units are the same machine bytes |

### `&` binary on (i64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_434 | cpp/op_434 | MATCHED | byte identity | the two units are the same machine bytes |

### `&` binary on (u64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_443 | cpp/op_443 | MATCHED | byte identity | the two units are the same machine bytes |

### `&` binary on (u64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_438 | cpp/op_438 | MATCHED | byte identity | the two units are the same machine bytes |

### `&` binary on (u64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_439 | cpp/op_439 | MATCHED | byte identity | the two units are the same machine bytes |

### `&` binary on (u64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_440 | cpp/op_440 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_440 | go/op_254 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_440 | rust/op_152 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_440 | swift/op_596 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_440 | go/op_254 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_440 | rust/op_152 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_440 | swift/op_596 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_254 | rust/op_152 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_254 | swift/op_596 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| rust/op_152 | swift/op_596 | MATCHED | byte identity | the two units are the same machine bytes |

### `&` unary on (bool,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_35 | cpp/op_47 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_35 | go/op_35 | UNDECIDED | z3 over the two lifted forms | c op_35 writes memory |
| cpp/op_47 | go/op_35 | UNDECIDED | z3 over the two lifted forms | cpp op_47 writes memory |

### `&` unary on (f32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_33 | cpp/op_45 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_33 | go/op_33 | UNDECIDED | z3 over the two lifted forms | c op_33 writes memory |
| cpp/op_45 | go/op_33 | UNDECIDED | z3 over the two lifted forms | cpp op_45 writes memory |

### `&` unary on (f64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_34 | cpp/op_46 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_34 | go/op_34 | UNDECIDED | z3 over the two lifted forms | c op_34 writes memory |
| cpp/op_46 | go/op_34 | UNDECIDED | z3 over the two lifted forms | cpp op_46 writes memory |

### `&` unary on (i32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_30 | cpp/op_42 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_30 | go/op_30 | UNDECIDED | z3 over the two lifted forms | c op_30 writes memory |
| cpp/op_42 | go/op_30 | UNDECIDED | z3 over the two lifted forms | cpp op_42 writes memory |

### `&` unary on (i64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_31 | cpp/op_43 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_31 | go/op_31 | UNDECIDED | z3 over the two lifted forms | c op_31 writes memory |
| cpp/op_43 | go/op_31 | UNDECIDED | z3 over the two lifted forms | cpp op_43 writes memory |

### `&` unary on (u64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_32 | cpp/op_44 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_32 | go/op_32 | UNDECIDED | z3 over the two lifted forms | c op_32 writes memory |
| cpp/op_44 | go/op_32 | UNDECIDED | z3 over the two lifted forms | cpp op_44 writes memory |

### `*` binary on (bool,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_209 | cpp/op_209 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (bool,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_207 | cpp/op_207 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (bool,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_208 | cpp/op_208 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (bool,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_204 | cpp/op_204 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (bool,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_205 | cpp/op_205 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (bool,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_206 | cpp/op_206 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (f32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_197 | cpp/op_197 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (f32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_195 | cpp/op_195 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_195 | go/op_81 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_195 | rust/op_627 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_195 | swift/op_135 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_195 | go/op_81 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_195 | rust/op_627 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_195 | swift/op_135 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_81 | rust/op_627 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_81 | swift/op_135 | MATCHED | byte identity | the two units are the same machine bytes |
| rust/op_627 | swift/op_135 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (f32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_196 | cpp/op_196 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (f32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_192 | cpp/op_192 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (f32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_193 | cpp/op_193 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (f32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_194 | cpp/op_194 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (f64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_203 | cpp/op_203 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (f64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_201 | cpp/op_201 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (f64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_202 | cpp/op_202 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_202 | go/op_88 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_202 | rust/op_634 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_202 | swift/op_142 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_202 | go/op_88 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_202 | rust/op_634 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_202 | swift/op_142 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_88 | rust/op_634 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_88 | swift/op_142 | MATCHED | byte identity | the two units are the same machine bytes |
| rust/op_634 | swift/op_142 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (f64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_198 | cpp/op_198 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (f64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_199 | cpp/op_199 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (f64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_200 | cpp/op_200 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (i32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_179 | cpp/op_179 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (i32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_177 | cpp/op_177 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (i32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_178 | cpp/op_178 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (i32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_174 | cpp/op_174 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_174 | go/op_60 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_174 | rust/op_606 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_174 | swift/op_114 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_114 guards; c op_174 does not; the arithmetic core is sem-equal |
| cpp/op_174 | go/op_60 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_174 | rust/op_606 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_174 | swift/op_114 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_114 guards; cpp op_174 does not; the arithmetic core is sem-equal |
| go/op_60 | rust/op_606 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_60 | swift/op_114 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_114 guards; go op_60 does not; the arithmetic core is sem-equal |
| rust/op_606 | swift/op_114 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_114 guards; rust op_606 does not; the arithmetic core is sem-equal |

### `*` binary on (i32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_175 | cpp/op_175 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (i32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_176 | cpp/op_176 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (i64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_185 | cpp/op_185 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (i64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_183 | cpp/op_183 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (i64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_184 | cpp/op_184 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (i64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_180 | cpp/op_180 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (i64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_181 | cpp/op_181 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_181 | go/op_67 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_181 | rust/op_613 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_181 | swift/op_121 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_121 guards; c op_181 does not; the arithmetic core is sem-equal |
| cpp/op_181 | go/op_67 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_181 | rust/op_613 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_181 | swift/op_121 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_121 guards; cpp op_181 does not; the arithmetic core is sem-equal |
| go/op_67 | rust/op_613 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_67 | swift/op_121 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_121 guards; go op_67 does not; the arithmetic core is sem-equal |
| rust/op_613 | swift/op_121 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_121 guards; rust op_613 does not; the arithmetic core is sem-equal |

### `*` binary on (i64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_182 | cpp/op_182 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (u64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_191 | cpp/op_191 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (u64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_189 | cpp/op_189 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (u64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_190 | cpp/op_190 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (u64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_186 | cpp/op_186 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (u64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_187 | cpp/op_187 | MATCHED | byte identity | the two units are the same machine bytes |

### `*` binary on (u64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_188 | cpp/op_188 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_188 | go/op_74 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_188 | rust/op_620 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_188 | swift/op_128 | UNDECIDED | one side guards but the cores are not equal | core of c op_188 is ['Mul64(in0:64,in1:64)']; core of swift op_128 is ['ex64@64(MullU64(in0:64,in1:64))'] |
| cpp/op_188 | go/op_74 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_188 | rust/op_620 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_188 | swift/op_128 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_188 is ['Mul64(in0:64,in1:64)']; core of swift op_128 is ['ex64@64(MullU64(in0:64,in1:64))'] |
| go/op_74 | rust/op_620 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_74 | swift/op_128 | UNDECIDED | one side guards but the cores are not equal | core of go op_74 is ['Mul64(in0:64,in1:64)']; core of swift op_128 is ['ex64@64(MullU64(in0:64,in1:64))'] |
| rust/op_620 | swift/op_128 | UNDECIDED | one side guards but the cores are not equal | core of rust op_620 is ['Mul64(in0:64,in1:64)']; core of swift op_128 is ['ex64@64(MullU64(in0:64,in1:64))'] |

### `+` binary on (bool,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_137 | cpp/op_137 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (bool,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_135 | cpp/op_135 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (bool,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_136 | cpp/op_136 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (bool,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_132 | cpp/op_132 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (bool,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_133 | cpp/op_133 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (bool,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_134 | cpp/op_134 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (f32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_125 | cpp/op_125 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (f32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_123 | cpp/op_123 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_123 | go/op_333 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_123 | rust/op_555 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_123 | swift/op_243 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_123 | go/op_333 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_123 | rust/op_555 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_123 | swift/op_243 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_333 | rust/op_555 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_333 | swift/op_243 | MATCHED | byte identity | the two units are the same machine bytes |
| rust/op_555 | swift/op_243 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (f32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_124 | cpp/op_124 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (f32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_120 | cpp/op_120 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (f32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_121 | cpp/op_121 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (f32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_122 | cpp/op_122 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (f64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_131 | cpp/op_131 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (f64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_129 | cpp/op_129 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (f64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_130 | cpp/op_130 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_130 | go/op_340 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_130 | rust/op_562 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_130 | swift/op_250 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_130 | go/op_340 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_130 | rust/op_562 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_130 | swift/op_250 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_340 | rust/op_562 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_340 | swift/op_250 | MATCHED | byte identity | the two units are the same machine bytes |
| rust/op_562 | swift/op_250 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (f64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_126 | cpp/op_126 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (f64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_127 | cpp/op_127 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (f64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_128 | cpp/op_128 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (i32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_107 | cpp/op_107 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (i32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_105 | cpp/op_105 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (i32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_106 | cpp/op_106 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (i32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_102 | cpp/op_102 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_102 | go/op_312 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_102 | rust/op_534 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_102 | swift/op_222 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_222 guards; c op_102 does not; the arithmetic core is sem-equal |
| cpp/op_102 | go/op_312 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_102 | rust/op_534 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_102 | swift/op_222 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_222 guards; cpp op_102 does not; the arithmetic core is sem-equal |
| go/op_312 | rust/op_534 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_312 | swift/op_222 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_222 guards; go op_312 does not; the arithmetic core is sem-equal |
| rust/op_534 | swift/op_222 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_222 guards; rust op_534 does not; the arithmetic core is sem-equal |

### `+` binary on (i32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_103 | cpp/op_103 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (i32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_104 | cpp/op_104 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (i64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_113 | cpp/op_113 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (i64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_111 | cpp/op_111 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (i64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_112 | cpp/op_112 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (i64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_108 | cpp/op_108 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (i64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_109 | cpp/op_109 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_109 | go/op_319 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_109 | rust/op_541 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_109 | swift/op_229 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_229 guards; c op_109 does not; the arithmetic core is sem-equal |
| cpp/op_109 | go/op_319 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_109 | rust/op_541 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_109 | swift/op_229 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_229 guards; cpp op_109 does not; the arithmetic core is sem-equal |
| go/op_319 | rust/op_541 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_319 | swift/op_229 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_229 guards; go op_319 does not; the arithmetic core is sem-equal |
| rust/op_541 | swift/op_229 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_229 guards; rust op_541 does not; the arithmetic core is sem-equal |

### `+` binary on (i64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_110 | cpp/op_110 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (u64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_119 | cpp/op_119 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (u64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_117 | cpp/op_117 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (u64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_118 | cpp/op_118 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (u64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_114 | cpp/op_114 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (u64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_115 | cpp/op_115 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` binary on (u64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_116 | cpp/op_116 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_116 | go/op_326 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_116 | rust/op_548 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_116 | swift/op_236 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_236 guards; c op_116 does not; the arithmetic core is sem-equal |
| cpp/op_116 | go/op_326 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_116 | rust/op_548 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_116 | swift/op_236 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_236 guards; cpp op_116 does not; the arithmetic core is sem-equal |
| go/op_326 | rust/op_548 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_326 | swift/op_236 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_236 guards; go op_326 does not; the arithmetic core is sem-equal |
| rust/op_548 | swift/op_236 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_236 guards; rust op_548 does not; the arithmetic core is sem-equal |

### `+` unary on (bool,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_23 | cpp/op_23 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` unary on (f32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_21 | cpp/op_21 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_21 | go/op_3 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_21 | swift/op_21 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_21 | go/op_3 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_21 | swift/op_21 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_3 | swift/op_21 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` unary on (f64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_22 | cpp/op_22 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_22 | go/op_4 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_22 | swift/op_22 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_22 | go/op_4 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_22 | swift/op_22 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_4 | swift/op_22 | MATCHED | byte identity | the two units are the same machine bytes |

### `+` unary on (i32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_18 | cpp/op_18 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_18 | go/op_0 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (1 and 0) |
| c/op_18 | swift/op_18 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_18 | go/op_0 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (1 and 0) |
| cpp/op_18 | swift/op_18 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_0 | swift/op_18 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (0 and 1) |

### `+` unary on (i64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_19 | cpp/op_19 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_19 | go/op_1 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (1 and 0) |
| c/op_19 | swift/op_19 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_19 | go/op_1 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (1 and 0) |
| cpp/op_19 | swift/op_19 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_1 | swift/op_19 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (0 and 1) |

### `+` unary on (u64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_20 | cpp/op_20 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_20 | go/op_2 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (1 and 0) |
| c/op_20 | swift/op_20 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_20 | go/op_2 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (1 and 0) |
| cpp/op_20 | swift/op_20 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_2 | swift/op_20 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (0 and 1) |

### `++` unary on (f32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_93 | cpp/op_87 | MATCHED | byte identity | the two units are the same machine bytes |

### `++` unary on (f64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_94 | cpp/op_88 | MATCHED | byte identity | the two units are the same machine bytes |

### `++` unary on (i32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_90 | cpp/op_84 | MATCHED | byte identity | the two units are the same machine bytes |

### `++` unary on (i64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_91 | cpp/op_85 | MATCHED | byte identity | the two units are the same machine bytes |

### `++` unary on (u64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_92 | cpp/op_86 | MATCHED | byte identity | the two units are the same machine bytes |

### `++` unary on (f32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_39 | cpp/op_51 | MATCHED | byte identity | the two units are the same machine bytes |

### `++` unary on (f64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_40 | cpp/op_52 | MATCHED | byte identity | the two units are the same machine bytes |

### `++` unary on (i32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_36 | cpp/op_48 | MATCHED | byte identity | the two units are the same machine bytes |

### `++` unary on (i64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_37 | cpp/op_49 | MATCHED | byte identity | the two units are the same machine bytes |

### `++` unary on (u64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_38 | cpp/op_50 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (bool,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_173 | cpp/op_173 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (bool,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_171 | cpp/op_171 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (bool,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_172 | cpp/op_172 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (bool,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_168 | cpp/op_168 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (bool,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_169 | cpp/op_169 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (bool,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_170 | cpp/op_170 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (f32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_161 | cpp/op_161 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (f32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_159 | cpp/op_159 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_159 | go/op_369 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_159 | rust/op_591 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_159 | swift/op_279 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_159 | go/op_369 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_159 | rust/op_591 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_159 | swift/op_279 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_369 | rust/op_591 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_369 | swift/op_279 | MATCHED | byte identity | the two units are the same machine bytes |
| rust/op_591 | swift/op_279 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (f32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_160 | cpp/op_160 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (f32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_156 | cpp/op_156 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (f32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_157 | cpp/op_157 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (f32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_158 | cpp/op_158 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (f64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_167 | cpp/op_167 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (f64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_165 | cpp/op_165 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (f64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_166 | cpp/op_166 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_166 | go/op_376 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_166 | rust/op_598 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_166 | swift/op_286 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_166 | go/op_376 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_166 | rust/op_598 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_166 | swift/op_286 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_376 | rust/op_598 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_376 | swift/op_286 | MATCHED | byte identity | the two units are the same machine bytes |
| rust/op_598 | swift/op_286 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (f64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_162 | cpp/op_162 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (f64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_163 | cpp/op_163 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (f64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_164 | cpp/op_164 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (i32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_143 | cpp/op_143 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (i32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_141 | cpp/op_141 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (i32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_142 | cpp/op_142 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (i32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_138 | cpp/op_138 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_138 | go/op_348 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_138 | rust/op_570 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_138 | swift/op_258 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_258 guards; c op_138 does not; the arithmetic core is sem-equal |
| cpp/op_138 | go/op_348 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_138 | rust/op_570 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_138 | swift/op_258 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_258 guards; cpp op_138 does not; the arithmetic core is sem-equal |
| go/op_348 | rust/op_570 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_348 | swift/op_258 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_258 guards; go op_348 does not; the arithmetic core is sem-equal |
| rust/op_570 | swift/op_258 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_258 guards; rust op_570 does not; the arithmetic core is sem-equal |

### `-` binary on (i32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_139 | cpp/op_139 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (i32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_140 | cpp/op_140 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (i64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_149 | cpp/op_149 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (i64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_147 | cpp/op_147 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (i64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_148 | cpp/op_148 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (i64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_144 | cpp/op_144 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (i64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_145 | cpp/op_145 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_145 | go/op_355 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_145 | rust/op_577 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_145 | swift/op_265 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_265 guards; c op_145 does not; the arithmetic core is sem-equal |
| cpp/op_145 | go/op_355 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_145 | rust/op_577 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_145 | swift/op_265 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_265 guards; cpp op_145 does not; the arithmetic core is sem-equal |
| go/op_355 | rust/op_577 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_355 | swift/op_265 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_265 guards; go op_355 does not; the arithmetic core is sem-equal |
| rust/op_577 | swift/op_265 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_265 guards; rust op_577 does not; the arithmetic core is sem-equal |

### `-` binary on (i64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_146 | cpp/op_146 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (u64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_155 | cpp/op_155 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (u64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_153 | cpp/op_153 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (u64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_154 | cpp/op_154 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (u64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_150 | cpp/op_150 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (u64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_151 | cpp/op_151 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` binary on (u64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_152 | cpp/op_152 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_152 | go/op_362 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_152 | rust/op_584 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_152 | swift/op_272 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_272 guards; c op_152 does not; the arithmetic core is sem-equal |
| cpp/op_152 | go/op_362 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_152 | rust/op_584 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_152 | swift/op_272 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_272 guards; cpp op_152 does not; the arithmetic core is sem-equal |
| go/op_362 | rust/op_584 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_362 | swift/op_272 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_272 guards; go op_362 does not; the arithmetic core is sem-equal |
| rust/op_584 | swift/op_272 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_272 guards; rust op_584 does not; the arithmetic core is sem-equal |

### `-` unary on (bool,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_17 | cpp/op_17 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` unary on (f32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_15 | cpp/op_15 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_15 | go/op_9 | UNDECIDED | z3 over the two lifted forms | c op_15 is not pure scalar dataflow: riprel xorps |
| c/op_15 | rust/op_3 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_15 | swift/op_15 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_15 | go/op_9 | UNDECIDED | z3 over the two lifted forms | cpp op_15 is not pure scalar dataflow: riprel xorps |
| cpp/op_15 | rust/op_3 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_15 | swift/op_15 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_9 | rust/op_3 | UNDECIDED | z3 over the two lifted forms | go op_9 is not pure scalar dataflow: riprel movss |
| go/op_9 | swift/op_15 | UNDECIDED | z3 over the two lifted forms | go op_9 is not pure scalar dataflow: riprel movss |
| rust/op_3 | swift/op_15 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` unary on (f64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_16 | cpp/op_16 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_16 | go/op_10 | UNDECIDED | z3 over the two lifted forms | c op_16 is not pure scalar dataflow: riprel xorps |
| c/op_16 | rust/op_4 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_16 | swift/op_16 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_16 | go/op_10 | UNDECIDED | z3 over the two lifted forms | cpp op_16 is not pure scalar dataflow: riprel xorps |
| cpp/op_16 | rust/op_4 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_16 | swift/op_16 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_10 | rust/op_4 | UNDECIDED | z3 over the two lifted forms | go op_10 is not pure scalar dataflow: riprel movsd |
| go/op_10 | swift/op_16 | UNDECIDED | z3 over the two lifted forms | go op_10 is not pure scalar dataflow: riprel movsd |
| rust/op_4 | swift/op_16 | MATCHED | byte identity | the two units are the same machine bytes |

### `-` unary on (i32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_12 | cpp/op_12 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_12 | go/op_6 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_12 | rust/op_0 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_12 | swift/op_12 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_12 guards; c op_12 does not; the arithmetic core is sem-equal |
| cpp/op_12 | go/op_6 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_12 | rust/op_0 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_12 | swift/op_12 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_12 guards; cpp op_12 does not; the arithmetic core is sem-equal |
| go/op_6 | rust/op_0 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_6 | swift/op_12 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_12 guards; go op_6 does not; the arithmetic core is sem-equal |
| rust/op_0 | swift/op_12 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_12 guards; rust op_0 does not; the arithmetic core is sem-equal |

### `-` unary on (i64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_13 | cpp/op_13 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_13 | go/op_7 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_13 | rust/op_1 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_13 | swift/op_13 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_13 guards; c op_13 does not; the arithmetic core is sem-equal |
| cpp/op_13 | go/op_7 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_13 | rust/op_1 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_13 | swift/op_13 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_13 guards; cpp op_13 does not; the arithmetic core is sem-equal |
| go/op_7 | rust/op_1 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_7 | swift/op_13 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_13 guards; go op_7 does not; the arithmetic core is sem-equal |
| rust/op_1 | swift/op_13 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_13 guards; rust op_1 does not; the arithmetic core is sem-equal |

### `-` unary on (u64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_14 | cpp/op_14 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_14 | go/op_8 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_14 | go/op_8 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |

### `--` unary on (f32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_99 | cpp/op_93 | MATCHED | byte identity | the two units are the same machine bytes |

### `--` unary on (f64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_100 | cpp/op_94 | MATCHED | byte identity | the two units are the same machine bytes |

### `--` unary on (i32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_96 | cpp/op_90 | MATCHED | byte identity | the two units are the same machine bytes |

### `--` unary on (i64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_97 | cpp/op_91 | MATCHED | byte identity | the two units are the same machine bytes |

### `--` unary on (u64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_98 | cpp/op_92 | MATCHED | byte identity | the two units are the same machine bytes |

### `--` unary on (f32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_45 | cpp/op_57 | MATCHED | byte identity | the two units are the same machine bytes |

### `--` unary on (f64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_46 | cpp/op_58 | MATCHED | byte identity | the two units are the same machine bytes |

### `--` unary on (i32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_42 | cpp/op_54 | MATCHED | byte identity | the two units are the same machine bytes |

### `--` unary on (i64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_43 | cpp/op_55 | MATCHED | byte identity | the two units are the same machine bytes |

### `--` unary on (u64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_44 | cpp/op_56 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (bool,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_245 | cpp/op_245 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (bool,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_243 | cpp/op_243 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (bool,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_244 | cpp/op_244 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (bool,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_240 | cpp/op_240 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (bool,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_241 | cpp/op_241 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (bool,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_242 | cpp/op_242 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (f32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_233 | cpp/op_233 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (f32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_231 | cpp/op_231 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_231 | go/op_117 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_231 | rust/op_663 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_231 | swift/op_171 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_231 | go/op_117 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_231 | rust/op_663 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_231 | swift/op_171 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_117 | rust/op_663 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_117 | swift/op_171 | MATCHED | byte identity | the two units are the same machine bytes |
| rust/op_663 | swift/op_171 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (f32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_232 | cpp/op_232 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (f32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_228 | cpp/op_228 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (f32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_229 | cpp/op_229 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (f32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_230 | cpp/op_230 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (f64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_239 | cpp/op_239 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (f64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_237 | cpp/op_237 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (f64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_238 | cpp/op_238 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_238 | go/op_124 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_238 | rust/op_670 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_238 | swift/op_178 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_238 | go/op_124 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_238 | rust/op_670 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_238 | swift/op_178 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_124 | rust/op_670 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_124 | swift/op_178 | MATCHED | byte identity | the two units are the same machine bytes |
| rust/op_670 | swift/op_178 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (f64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_234 | cpp/op_234 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (f64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_235 | cpp/op_235 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (f64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_236 | cpp/op_236 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (i32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_215 | cpp/op_215 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (i32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_213 | cpp/op_213 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (i32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_214 | cpp/op_214 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (i32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_210 | cpp/op_210 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_210 | go/op_96 | UNDECIDED | one side guards but the cores are not equal | core of c op_210 is ['zx64(ex32@0(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64))))', 'zx64(ex32@32(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64))))']; core of go op_96 is ['zx64(Sub32(0:32,ex32@0(in0:64)))', 'zx64(ex32@0(DivModS64 |
| c/op_210 | rust/op_642 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | rust op_642 guards; c op_210 does not; the arithmetic core is sem-equal |
| c/op_210 | swift/op_150 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_150 guards; c op_210 does not; the arithmetic core is sem-equal |
| cpp/op_210 | go/op_96 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_210 is ['zx64(ex32@0(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64))))', 'zx64(ex32@32(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64))))']; core of go op_96 is ['zx64(Sub32(0:32,ex32@0(in0:64)))', 'zx64(ex32@0(DivModS |
| cpp/op_210 | rust/op_642 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | rust op_642 guards; cpp op_210 does not; the arithmetic core is sem-equal |
| cpp/op_210 | swift/op_150 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | swift op_150 guards; cpp op_210 does not; the arithmetic core is sem-equal |
| go/op_96 | rust/op_642 | UNDECIDED | both sides carry a guard | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |
| go/op_96 | swift/op_150 | UNDECIDED | both sides carry a guard | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |
| rust/op_642 | swift/op_150 | UNDECIDED | both sides carry a guard | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |

### `/` binary on (i32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_211 | cpp/op_211 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (i32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_212 | cpp/op_212 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (i64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_221 | cpp/op_221 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (i64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_219 | cpp/op_219 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (i64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_220 | cpp/op_220 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (i64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_216 | cpp/op_216 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (i64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_217 | cpp/op_217 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_217 | go/op_103 | UNDECIDED | one side guards but the cores are not equal | core of c op_217 is ['ex64@0(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))']; core of go op_103 is ['Sub64(0:64,in0:64)', 'ex64@0(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'ex64@64(DivModS128t |
| c/op_217 | rust/op_649 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | rust op_649 guards; c op_217 does not; the arithmetic core is sem-equal |
| c/op_217 | swift/op_157 | UNDECIDED | one side guards but the cores are not equal | core of c op_217 is ['ex64@0(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))']; core of swift op_157 is ['Shr64(Or64(in0:64,in1:64),32:8)', 'ex64@0(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'ex6 |
| cpp/op_217 | go/op_103 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_217 is ['ex64@0(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))']; core of go op_103 is ['Sub64(0:64,in0:64)', 'ex64@0(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'ex64@64(DivModS12 |
| cpp/op_217 | rust/op_649 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | rust op_649 guards; cpp op_217 does not; the arithmetic core is sem-equal |
| cpp/op_217 | swift/op_157 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_217 is ['ex64@0(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))']; core of swift op_157 is ['Shr64(Or64(in0:64,in1:64),32:8)', 'ex64@0(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'e |
| go/op_103 | rust/op_649 | UNDECIDED | both sides carry a guard | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |
| go/op_103 | swift/op_157 | UNDECIDED | both sides carry a guard | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |
| rust/op_649 | swift/op_157 | UNDECIDED | both sides carry a guard | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |

### `/` binary on (i64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_218 | cpp/op_218 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (u64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_227 | cpp/op_227 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (u64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_225 | cpp/op_225 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (u64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_226 | cpp/op_226 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (u64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_222 | cpp/op_222 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (u64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_223 | cpp/op_223 | MATCHED | byte identity | the two units are the same machine bytes |

### `/` binary on (u64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_224 | cpp/op_224 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_224 | go/op_110 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | go op_110 guards; c op_224 does not; the arithmetic core is sem-equal |
| c/op_224 | rust/op_656 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | rust op_656 guards; c op_224 does not; the arithmetic core is sem-equal |
| c/op_224 | swift/op_164 | UNDECIDED | one side guards but the cores are not equal | core of c op_224 is ['ex64@0(DivModU128to64(64HLto128(0:64,in0:64),in1:64))', 'ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64))']; core of swift op_164 is ['Shr64(Or64(in0:64,in1:64),32:8)', 'ex64@0(DivModU128to64(64HLto128(0:64,in0:64),in1:64))', 'ex64@64(DivModU128to64(64HLto128(0:64,in0:64) |
| cpp/op_224 | go/op_110 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | go op_110 guards; cpp op_224 does not; the arithmetic core is sem-equal |
| cpp/op_224 | rust/op_656 | DIFFERS-BY-DESIGN | a guard on one side, the same core on both | rust op_656 guards; cpp op_224 does not; the arithmetic core is sem-equal |
| cpp/op_224 | swift/op_164 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_224 is ['ex64@0(DivModU128to64(64HLto128(0:64,in0:64),in1:64))', 'ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64))']; core of swift op_164 is ['Shr64(Or64(in0:64,in1:64),32:8)', 'ex64@0(DivModU128to64(64HLto128(0:64,in0:64),in1:64))', 'ex64@64(DivModU128to64(64HLto128(0:64,in0:6 |
| go/op_110 | rust/op_656 | UNDECIDED | both sides carry a guard | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |
| go/op_110 | swift/op_164 | UNDECIDED | both sides carry a guard | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |
| rust/op_656 | swift/op_164 | UNDECIDED | both sides carry a guard | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |

### `<` binary on (bool,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_677 | cpp/op_677 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| c/op_677 | rust/op_353 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| cpp/op_677 | rust/op_353 | MATCHED | byte identity | the two units are the same machine bytes |

### `<` binary on (bool,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_675 | cpp/op_675 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `<` binary on (bool,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_676 | cpp/op_676 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: I32StoF64 |

### `<` binary on (bool,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_672 | cpp/op_672 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `<` binary on (bool,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_673 | cpp/op_673 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |

### `<` binary on (bool,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_674 | cpp/op_674 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |

### `<` binary on (f32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_665 | cpp/op_665 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `<` binary on (f32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_663 | cpp/op_663 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| c/op_663 | go/op_549 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| c/op_663 | rust/op_339 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| c/op_663 | swift/op_315 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| cpp/op_663 | go/op_549 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_663 | rust/op_339 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_663 | swift/op_315 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_549 | rust/op_339 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_549 | swift/op_315 | MATCHED | byte identity | the two units are the same machine bytes |
| rust/op_339 | swift/op_315 | MATCHED | byte identity | the two units are the same machine bytes |

### `<` binary on (f32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_664 | cpp/op_664 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `<` binary on (f32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_660 | cpp/op_660 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `<` binary on (f32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_661 | cpp/op_661 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `<` binary on (f32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_662 | cpp/op_662 | UNDECIDED | z3 over the two lifted forms | c op_662 is not straight-line: 4 blocks |

### `<` binary on (f64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_671 | cpp/op_671 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: I32StoF64 |

### `<` binary on (f64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_669 | cpp/op_669 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `<` binary on (f64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_670 | cpp/op_670 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| c/op_670 | go/op_556 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| c/op_670 | rust/op_346 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| c/op_670 | swift/op_322 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| cpp/op_670 | go/op_556 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_670 | rust/op_346 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_670 | swift/op_322 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_556 | rust/op_346 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_556 | swift/op_322 | MATCHED | byte identity | the two units are the same machine bytes |
| rust/op_346 | swift/op_322 | MATCHED | byte identity | the two units are the same machine bytes |

### `<` binary on (f64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_666 | cpp/op_666 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: I32StoF64 |

### `<` binary on (f64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_667 | cpp/op_667 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: I64StoF64 |

### `<` binary on (f64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_668 | cpp/op_668 | UNDECIDED | z3 over the two lifted forms | c op_668 is not pure scalar dataflow: riprel punpckldq; riprel subpd |

### `<` binary on (i32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_647 | cpp/op_647 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `<` binary on (i32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_645 | cpp/op_645 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `<` binary on (i32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_646 | cpp/op_646 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: I32StoF64 |

### `<` binary on (i32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_642 | cpp/op_642 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_642 | go/op_528 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_642 | rust/op_318 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_642 | swift/op_294 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| cpp/op_642 | go/op_528 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_642 | rust/op_318 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_642 | swift/op_294 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_528 | rust/op_318 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_528 | swift/op_294 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| rust/op_318 | swift/op_294 | MATCHED | byte identity | the two units are the same machine bytes |

### `<` binary on (i32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_643 | cpp/op_643 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| c/op_643 | swift/op_295 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| cpp/op_643 | swift/op_295 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |

### `<` binary on (i32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_644 | cpp/op_644 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| c/op_644 | swift/op_296 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 2147483648, in1_64 = 18446744071562067969 |
| cpp/op_644 | swift/op_296 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 2147483648, in1_64 = 18446744071562067968 |

### `<` binary on (i64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_653 | cpp/op_653 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |

### `<` binary on (i64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_651 | cpp/op_651 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `<` binary on (i64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_652 | cpp/op_652 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: I64StoF64 |

### `<` binary on (i64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_648 | cpp/op_648 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |
| c/op_648 | swift/op_300 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |
| cpp/op_648 | swift/op_300 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |

### `<` binary on (i64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_649 | cpp/op_649 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_649 | go/op_535 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_649 | rust/op_325 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_649 | swift/op_301 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| cpp/op_649 | go/op_535 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_649 | rust/op_325 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_649 | swift/op_301 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_535 | rust/op_325 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_535 | swift/op_301 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| rust/op_325 | swift/op_301 | MATCHED | byte identity | the two units are the same machine bytes |

### `<` binary on (i64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_650 | cpp/op_650 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_650 | swift/op_302 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 9223372036854775808, in1_64 = 9223372036854775808 |
| cpp/op_650 | swift/op_302 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 9223372036854775808, in1_64 = 9223372036854775808 |

### `<` binary on (u64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_659 | cpp/op_659 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `<` binary on (u64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_657 | cpp/op_657 | UNDECIDED | z3 over the two lifted forms | c op_657 is not straight-line: 4 blocks |

### `<` binary on (u64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_658 | cpp/op_658 | UNDECIDED | z3 over the two lifted forms | c op_658 is not pure scalar dataflow: riprel punpckldq; riprel subpd |

### `<` binary on (u64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_654 | cpp/op_654 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |
| c/op_654 | swift/op_306 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18446744071562067967, in1_64 = 2147483648 |
| cpp/op_654 | swift/op_306 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18446744071562067967, in1_64 = 2147483648 |

### `<` binary on (u64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_655 | cpp/op_655 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_655 | swift/op_307 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 9223372036854775807, in1_64 = 9223372036854775808 |
| cpp/op_655 | swift/op_307 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 9223372036854775807, in1_64 = 9223372036854775808 |

### `<` binary on (u64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_656 | cpp/op_656 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_656 | go/op_542 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_656 | rust/op_332 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_656 | swift/op_308 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| cpp/op_656 | go/op_542 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_656 | rust/op_332 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_656 | swift/op_308 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_542 | rust/op_332 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_542 | swift/op_308 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| rust/op_332 | swift/op_308 | MATCHED | byte identity | the two units are the same machine bytes |

### `<<` binary on (bool,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_713 | cpp/op_713 | MATCHED | byte identity | the two units are the same machine bytes |

### `<<` binary on (bool,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_708 | cpp/op_708 | MATCHED | byte identity | the two units are the same machine bytes |

### `<<` binary on (bool,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_709 | cpp/op_709 | MATCHED | byte identity | the two units are the same machine bytes |

### `<<` binary on (bool,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_710 | cpp/op_710 | MATCHED | byte identity | the two units are the same machine bytes |

### `<<` binary on (i32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_683 | cpp/op_683 | MATCHED | byte identity | the two units are the same machine bytes |

### `<<` binary on (i32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_678 | cpp/op_678 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_678 | go/op_168 | UNDECIDED | one side guards but the cores are not equal | core of c op_678 is ['zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))']; core of go op_168 is ['zx64(And32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),32:64,u0:64)))),ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))))', 'zx64(Sub32( |
| c/op_678 | rust/op_462 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_678 | swift/op_690 | UNDECIDED | z3 over the two lifted forms | swift op_690 is not pure scalar dataflow: jmp $s9unit_ship6op_690ys5Int32VAD_ADtF |
| cpp/op_678 | go/op_168 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_678 is ['zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))']; core of go op_168 is ['zx64(And32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),32:64,u0:64)))),ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))))', 'zx64(Sub3 |
| cpp/op_678 | rust/op_462 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_678 | swift/op_690 | UNDECIDED | z3 over the two lifted forms | swift op_690 is not pure scalar dataflow: jmp $s9unit_ship6op_690ys5Int32VAD_ADtF |
| go/op_168 | rust/op_462 | UNDECIDED | one side guards but the cores are not equal | core of go op_168 is ['zx64(And32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),32:64,u0:64)))),ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))))', 'zx64(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),32:64,u0:64)))))' |
| go/op_168 | swift/op_690 | UNDECIDED | one side guards but the cores are not equal | core of go op_168 is ['zx64(And32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),32:64,u0:64)))),ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))))', 'zx64(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),32:64,u0:64)))))' |
| rust/op_462 | swift/op_690 | UNDECIDED | z3 over the two lifted forms | swift op_690 is not pure scalar dataflow: jmp $s9unit_ship6op_690ys5Int32VAD_ADtF |

### `<<` binary on (i32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_679 | cpp/op_679 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_679 | go/op_169 | UNDECIDED | one side guards but the cores are not equal | core of c op_679 is ['zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))']; core of go op_169 is ['zx64(And32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(8:64,in1:64,32:64,u0:64)))),ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))))', 'zx64(Sub32(0:32,And32(1:3 |
| c/op_679 | rust/op_463 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_679 | swift/op_691 | UNDECIDED | z3 over the two lifted forms | swift op_691 is not pure scalar dataflow: jmp $s9unit_ship6op_691ys5Int32VAD_s5Int64VtF |
| cpp/op_679 | go/op_169 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_679 is ['zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))']; core of go op_169 is ['zx64(And32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(8:64,in1:64,32:64,u0:64)))),ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))))', 'zx64(Sub32(0:32,And32(1 |
| cpp/op_679 | rust/op_463 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_679 | swift/op_691 | UNDECIDED | z3 over the two lifted forms | swift op_691 is not pure scalar dataflow: jmp $s9unit_ship6op_691ys5Int32VAD_s5Int64VtF |
| go/op_169 | rust/op_463 | UNDECIDED | one side guards but the cores are not equal | core of go op_169 is ['zx64(And32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(8:64,in1:64,32:64,u0:64)))),ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))))', 'zx64(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(8:64,in1:64,32:64,u0:64)))))']; core of rust op_463 is [' |
| go/op_169 | swift/op_691 | UNDECIDED | one side guards but the cores are not equal | core of go op_169 is ['zx64(And32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(8:64,in1:64,32:64,u0:64)))),ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64))))))', 'zx64(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(8:64,in1:64,32:64,u0:64)))))']; core of swift op_691 is [ |
| rust/op_463 | swift/op_691 | UNDECIDED | z3 over the two lifted forms | swift op_691 is not pure scalar dataflow: jmp $s9unit_ship6op_691ys5Int32VAD_s5Int64VtF |

### `<<` binary on (i32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_680 | cpp/op_680 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_680 | go/op_170 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (1 and 2) |
| c/op_680 | rust/op_464 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_680 | swift/op_692 | UNDECIDED | z3 over the two lifted forms | swift op_692 is not pure scalar dataflow: jmp $s9unit_ship6op_692ys5Int32VAD_s6UInt64VtF |
| cpp/op_680 | go/op_170 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (1 and 2) |
| cpp/op_680 | rust/op_464 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_680 | swift/op_692 | UNDECIDED | z3 over the two lifted forms | swift op_692 is not pure scalar dataflow: jmp $s9unit_ship6op_692ys5Int32VAD_s6UInt64VtF |
| go/op_170 | rust/op_464 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (2 and 1) |
| go/op_170 | swift/op_692 | UNDECIDED | z3 over the two lifted forms | swift op_692 is not pure scalar dataflow: jmp $s9unit_ship6op_692ys5Int32VAD_s6UInt64VtF |
| rust/op_464 | swift/op_692 | UNDECIDED | z3 over the two lifted forms | swift op_692 is not pure scalar dataflow: jmp $s9unit_ship6op_692ys5Int32VAD_s6UInt64VtF |

### `<<` binary on (i64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_689 | cpp/op_689 | MATCHED | byte identity | the two units are the same machine bytes |

### `<<` binary on (i64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_684 | cpp/op_684 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_684 | go/op_174 | UNDECIDED | one side guards but the cores are not equal | core of c op_684 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_174 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),64:64,u0:64))))'] |
| c/op_684 | rust/op_468 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_684 | swift/op_696 | UNDECIDED | z3 over the two lifted forms | swift op_696 is not pure scalar dataflow: jmp $s9unit_ship6op_696ys5Int64VAD_s5Int32VtF |
| cpp/op_684 | go/op_174 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_684 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_174 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),64:64,u0:64))))'] |
| cpp/op_684 | rust/op_468 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_684 | swift/op_696 | UNDECIDED | z3 over the two lifted forms | swift op_696 is not pure scalar dataflow: jmp $s9unit_ship6op_696ys5Int64VAD_s5Int32VtF |
| go/op_174 | rust/op_468 | UNDECIDED | one side guards but the cores are not equal | core of go op_174 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),64:64,u0:64))))']; core of rust op_468 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))'] |
| go/op_174 | swift/op_696 | UNDECIDED | one side guards but the cores are not equal | core of go op_174 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),64:64,u0:64))))']; core of swift op_696 is [] |
| rust/op_468 | swift/op_696 | UNDECIDED | z3 over the two lifted forms | swift op_696 is not pure scalar dataflow: jmp $s9unit_ship6op_696ys5Int64VAD_s5Int32VtF |

### `<<` binary on (i64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_685 | cpp/op_685 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_685 | go/op_175 | UNDECIDED | one side guards but the cores are not equal | core of c op_685 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_175 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))'] |
| c/op_685 | rust/op_469 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_685 | swift/op_697 | UNDECIDED | z3 over the two lifted forms | swift op_697 is not pure scalar dataflow: jmp $s9unit_ship6op_697ys5Int64VAD_ADtF |
| cpp/op_685 | go/op_175 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_685 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_175 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))'] |
| cpp/op_685 | rust/op_469 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_685 | swift/op_697 | UNDECIDED | z3 over the two lifted forms | swift op_697 is not pure scalar dataflow: jmp $s9unit_ship6op_697ys5Int64VAD_ADtF |
| go/op_175 | rust/op_469 | UNDECIDED | one side guards but the cores are not equal | core of go op_175 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))']; core of rust op_469 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))'] |
| go/op_175 | swift/op_697 | UNDECIDED | one side guards but the cores are not equal | core of go op_175 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))']; core of swift op_697 is [] |
| rust/op_469 | swift/op_697 | UNDECIDED | z3 over the two lifted forms | swift op_697 is not pure scalar dataflow: jmp $s9unit_ship6op_697ys5Int64VAD_ADtF |

### `<<` binary on (i64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_686 | cpp/op_686 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_686 | go/op_176 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: VEX helper call not modelled: amd64g_calculate_rflags_c |
| c/op_686 | rust/op_470 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_686 | swift/op_698 | UNDECIDED | z3 over the two lifted forms | swift op_698 is not pure scalar dataflow: jmp $s9unit_ship6op_698ys5Int64VAD_s6UInt64VtF |
| cpp/op_686 | go/op_176 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: VEX helper call not modelled: amd64g_calculate_rflags_c |
| cpp/op_686 | rust/op_470 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_686 | swift/op_698 | UNDECIDED | z3 over the two lifted forms | swift op_698 is not pure scalar dataflow: jmp $s9unit_ship6op_698ys5Int64VAD_s6UInt64VtF |
| go/op_176 | rust/op_470 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: VEX helper call not modelled: amd64g_calculate_rflags_c |
| go/op_176 | swift/op_698 | UNDECIDED | z3 over the two lifted forms | swift op_698 is not pure scalar dataflow: jmp $s9unit_ship6op_698ys5Int64VAD_s6UInt64VtF |
| rust/op_470 | swift/op_698 | UNDECIDED | z3 over the two lifted forms | swift op_698 is not pure scalar dataflow: jmp $s9unit_ship6op_698ys5Int64VAD_s6UInt64VtF |

### `<<` binary on (u64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_695 | cpp/op_695 | MATCHED | byte identity | the two units are the same machine bytes |

### `<<` binary on (u64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_690 | cpp/op_690 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_690 | go/op_180 | UNDECIDED | one side guards but the cores are not equal | core of c op_690 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_180 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),64:64,u0:64))))'] |
| c/op_690 | rust/op_474 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_690 | swift/op_702 | UNDECIDED | z3 over the two lifted forms | swift op_702 is not pure scalar dataflow: jmp $s9unit_ship6op_702ys6UInt64VAD_s5Int32VtF |
| cpp/op_690 | go/op_180 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_690 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_180 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),64:64,u0:64))))'] |
| cpp/op_690 | rust/op_474 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_690 | swift/op_702 | UNDECIDED | z3 over the two lifted forms | swift op_702 is not pure scalar dataflow: jmp $s9unit_ship6op_702ys6UInt64VAD_s5Int32VtF |
| go/op_180 | rust/op_474 | UNDECIDED | one side guards but the cores are not equal | core of go op_180 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),64:64,u0:64))))']; core of rust op_474 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))'] |
| go/op_180 | swift/op_702 | UNDECIDED | one side guards but the cores are not equal | core of go op_180 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),64:64,u0:64))))']; core of swift op_702 is [] |
| rust/op_474 | swift/op_702 | UNDECIDED | z3 over the two lifted forms | swift op_702 is not pure scalar dataflow: jmp $s9unit_ship6op_702ys6UInt64VAD_s5Int32VtF |

### `<<` binary on (u64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_691 | cpp/op_691 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_691 | go/op_181 | UNDECIDED | one side guards but the cores are not equal | core of c op_691 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_181 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))'] |
| c/op_691 | rust/op_475 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_691 | swift/op_703 | UNDECIDED | z3 over the two lifted forms | swift op_703 is not straight-line: 7 blocks |
| cpp/op_691 | go/op_181 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_691 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_181 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))'] |
| cpp/op_691 | rust/op_475 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_691 | swift/op_703 | UNDECIDED | z3 over the two lifted forms | swift op_703 is not straight-line: 7 blocks |
| go/op_181 | rust/op_475 | UNDECIDED | one side guards but the cores are not equal | core of go op_181 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))']; core of rust op_475 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))'] |
| go/op_181 | swift/op_703 | UNDECIDED | one side guards but the cores are not equal | core of go op_181 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))']; core of swift op_703 is ['Add64(18446744073709551551:64,in1:64)', 'Shl64(u1:64,And8(63:8,ex8@0(in1:64)))', 'Shr64(u1:64,And8(63:8,Sub8(0:8,ex8@0(in1:64)) |
| rust/op_475 | swift/op_703 | UNDECIDED | z3 over the two lifted forms | swift op_703 is not straight-line: 7 blocks |

### `<<` binary on (u64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_692 | cpp/op_692 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_692 | go/op_182 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: VEX helper call not modelled: amd64g_calculate_rflags_c |
| c/op_692 | rust/op_476 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_692 | swift/op_704 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 141733920751, in1_64 = 96 |
| cpp/op_692 | go/op_182 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: VEX helper call not modelled: amd64g_calculate_rflags_c |
| cpp/op_692 | rust/op_476 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_692 | swift/op_704 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967263, in1_64 = 96 |
| go/op_182 | rust/op_476 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: VEX helper call not modelled: amd64g_calculate_rflags_c |
| go/op_182 | swift/op_704 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: VEX helper call not modelled: amd64g_calculate_rflags_c |
| rust/op_476 | swift/op_704 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 1073741815, in1_64 = 1152921504606847010 |

### `<=` binary on (bool,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_641 | cpp/op_641 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| c/op_641 | rust/op_389 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| cpp/op_641 | rust/op_389 | MATCHED | byte identity | the two units are the same machine bytes |

### `<=` binary on (bool,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_639 | cpp/op_639 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `<=` binary on (bool,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_640 | cpp/op_640 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: I32StoF64 |

### `<=` binary on (bool,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_636 | cpp/op_636 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `<=` binary on (bool,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_637 | cpp/op_637 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |

### `<=` binary on (bool,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_638 | cpp/op_638 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |

### `<=` binary on (f32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_629 | cpp/op_629 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `<=` binary on (f32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_627 | cpp/op_627 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| c/op_627 | go/op_585 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| c/op_627 | rust/op_375 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| c/op_627 | swift/op_387 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| cpp/op_627 | go/op_585 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_627 | rust/op_375 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_627 | swift/op_387 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_585 | rust/op_375 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_585 | swift/op_387 | MATCHED | byte identity | the two units are the same machine bytes |
| rust/op_375 | swift/op_387 | MATCHED | byte identity | the two units are the same machine bytes |

### `<=` binary on (f32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_628 | cpp/op_628 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `<=` binary on (f32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_624 | cpp/op_624 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `<=` binary on (f32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_625 | cpp/op_625 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `<=` binary on (f32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_626 | cpp/op_626 | UNDECIDED | z3 over the two lifted forms | c op_626 is not straight-line: 4 blocks |

### `<=` binary on (f64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_635 | cpp/op_635 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: I32StoF64 |

### `<=` binary on (f64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_633 | cpp/op_633 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `<=` binary on (f64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_634 | cpp/op_634 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| c/op_634 | go/op_592 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| c/op_634 | rust/op_382 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| c/op_634 | swift/op_394 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| cpp/op_634 | go/op_592 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_634 | rust/op_382 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_634 | swift/op_394 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_592 | rust/op_382 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_592 | swift/op_394 | MATCHED | byte identity | the two units are the same machine bytes |
| rust/op_382 | swift/op_394 | MATCHED | byte identity | the two units are the same machine bytes |

### `<=` binary on (f64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_630 | cpp/op_630 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: I32StoF64 |

### `<=` binary on (f64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_631 | cpp/op_631 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: I64StoF64 |

### `<=` binary on (f64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_632 | cpp/op_632 | UNDECIDED | z3 over the two lifted forms | c op_632 is not pure scalar dataflow: riprel punpckldq; riprel subpd |

### `<=` binary on (i32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_611 | cpp/op_611 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `<=` binary on (i32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_609 | cpp/op_609 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `<=` binary on (i32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_610 | cpp/op_610 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: I32StoF64 |

### `<=` binary on (i32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_606 | cpp/op_606 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_606 | go/op_564 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_606 | rust/op_354 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_606 | swift/op_366 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| cpp/op_606 | go/op_564 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_606 | rust/op_354 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_606 | swift/op_366 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_564 | rust/op_354 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_564 | swift/op_366 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| rust/op_354 | swift/op_366 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |

### `<=` binary on (i32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_607 | cpp/op_607 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| c/op_607 | swift/op_367 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| cpp/op_607 | swift/op_367 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |

### `<=` binary on (i32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_608 | cpp/op_608 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| c/op_608 | swift/op_368 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 2147483648, in1_64 = 18446744071562067967 |
| cpp/op_608 | swift/op_368 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 2147483648, in1_64 = 18446744071562067967 |

### `<=` binary on (i64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_617 | cpp/op_617 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |

### `<=` binary on (i64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_615 | cpp/op_615 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `<=` binary on (i64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_616 | cpp/op_616 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: I64StoF64 |

### `<=` binary on (i64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_612 | cpp/op_612 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |
| c/op_612 | swift/op_372 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |
| cpp/op_612 | swift/op_372 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |

### `<=` binary on (i64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_613 | cpp/op_613 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_613 | go/op_571 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_613 | rust/op_361 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_613 | swift/op_373 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| cpp/op_613 | go/op_571 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_613 | rust/op_361 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_613 | swift/op_373 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_571 | rust/op_361 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_571 | swift/op_373 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| rust/op_361 | swift/op_373 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |

### `<=` binary on (i64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_614 | cpp/op_614 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_614 | swift/op_374 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 9223372036854775808, in1_64 = 9223372036854775807 |
| cpp/op_614 | swift/op_374 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 9223372036854775808, in1_64 = 9223372036854775807 |

### `<=` binary on (u64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_623 | cpp/op_623 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |

### `<=` binary on (u64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_621 | cpp/op_621 | UNDECIDED | z3 over the two lifted forms | c op_621 is not straight-line: 4 blocks |

### `<=` binary on (u64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_622 | cpp/op_622 | UNDECIDED | z3 over the two lifted forms | c op_622 is not pure scalar dataflow: riprel punpckldq; riprel subpd |

### `<=` binary on (u64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_618 | cpp/op_618 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4278189824 |
| c/op_618 | swift/op_378 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18446744071562067969, in1_64 = 2147483648 |
| cpp/op_618 | swift/op_378 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18446744071562067968, in1_64 = 2147483648 |

### `<=` binary on (u64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_619 | cpp/op_619 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_619 | swift/op_379 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 9223372036854775808, in1_64 = 9223372036854775808 |
| cpp/op_619 | swift/op_379 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 9223372036854775808, in1_64 = 9223372036854775808 |

### `<=` binary on (u64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_620 | cpp/op_620 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_620 | go/op_578 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_620 | rust/op_368 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_620 | swift/op_380 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| cpp/op_620 | go/op_578 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_620 | rust/op_368 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_620 | swift/op_380 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_578 | rust/op_368 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_578 | swift/op_380 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| rust/op_368 | swift/op_380 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |

### `==` binary on (bool,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_497 | cpp/op_497 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (2 and 1) |
| c/op_497 | go/op_491 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (2 and 1) |
| c/op_497 | rust/op_281 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (2 and 1) |
| c/op_497 | swift/op_545 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (2 and 1) |
| cpp/op_497 | go/op_491 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 2, in1_64 = 249 |
| cpp/op_497 | rust/op_281 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_497 | swift/op_545 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_491 | rust/op_281 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 96, in1_64 = 139 |
| go/op_491 | swift/op_545 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 32, in1_64 = 222 |
| rust/op_281 | swift/op_545 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (bool,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_495 | cpp/op_495 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (bool,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_496 | cpp/op_496 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (bool,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_492 | cpp/op_492 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `==` binary on (bool,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_493 | cpp/op_493 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |

### `==` binary on (bool,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_494 | cpp/op_494 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |

### `==` binary on (f32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_485 | cpp/op_485 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (f32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_483 | cpp/op_483 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_483 | go/op_477 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| c/op_483 | rust/op_267 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_483 | swift/op_531 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_483 | go/op_477 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| cpp/op_483 | rust/op_267 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_483 | swift/op_531 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_477 | rust/op_267 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| go/op_477 | swift/op_531 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| rust/op_267 | swift/op_531 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (f32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_484 | cpp/op_484 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (f32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_480 | cpp/op_480 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (f32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_481 | cpp/op_481 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (f32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_482 | cpp/op_482 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (f64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_491 | cpp/op_491 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (f64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_489 | cpp/op_489 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (f64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_490 | cpp/op_490 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_490 | go/op_484 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| c/op_490 | rust/op_274 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_490 | swift/op_538 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_490 | go/op_484 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| cpp/op_490 | rust/op_274 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_490 | swift/op_538 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_484 | rust/op_274 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| go/op_484 | swift/op_538 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| rust/op_274 | swift/op_538 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (f64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_486 | cpp/op_486 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (f64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_487 | cpp/op_487 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (f64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_488 | cpp/op_488 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (i32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_467 | cpp/op_467 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `==` binary on (i32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_465 | cpp/op_465 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (i32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_466 | cpp/op_466 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (i32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_462 | cpp/op_462 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_462 | go/op_456 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_462 | rust/op_246 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_462 | swift/op_510 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| cpp/op_462 | go/op_456 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_462 | rust/op_246 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_462 | swift/op_510 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_456 | rust/op_246 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_456 | swift/op_510 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| rust/op_246 | swift/op_510 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (i32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_463 | cpp/op_463 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| c/op_463 | swift/op_511 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967042, in1_64 = 253 |
| cpp/op_463 | swift/op_511 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |

### `==` binary on (i32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_464 | cpp/op_464 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| c/op_464 | swift/op_512 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 2147483648, in1_64 = 0 |
| cpp/op_464 | swift/op_512 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 2147483648, in1_64 = 18446744071562067968 |

### `==` binary on (i64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_473 | cpp/op_473 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |

### `==` binary on (i64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_471 | cpp/op_471 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (i64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_472 | cpp/op_472 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (i64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_468 | cpp/op_468 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |
| c/op_468 | swift/op_516 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 119, in1_64 = 4294967176 |
| cpp/op_468 | swift/op_516 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |

### `==` binary on (i64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_469 | cpp/op_469 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_469 | go/op_463 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_469 | rust/op_253 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_469 | swift/op_517 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| cpp/op_469 | go/op_463 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_469 | rust/op_253 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_469 | swift/op_517 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_463 | rust/op_253 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_463 | swift/op_517 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| rust/op_253 | swift/op_517 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (i64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_470 | cpp/op_470 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_470 | swift/op_518 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18446744073709551615, in1_64 = 18446744073709551615 |
| cpp/op_470 | swift/op_518 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18446744073709551615, in1_64 = 18446744073709551615 |

### `==` binary on (u64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_479 | cpp/op_479 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |

### `==` binary on (u64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_477 | cpp/op_477 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (u64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_478 | cpp/op_478 | MATCHED | byte identity | the two units are the same machine bytes |

### `==` binary on (u64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_474 | cpp/op_474 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 3221225216 |
| c/op_474 | swift/op_522 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 0, in1_64 = 2147483648 |
| cpp/op_474 | swift/op_522 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18446744071562067968, in1_64 = 2147483648 |

### `==` binary on (u64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_475 | cpp/op_475 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_475 | swift/op_523 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18446744073709551615, in1_64 = 18446744073709551615 |
| cpp/op_475 | swift/op_523 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18446744073709551615, in1_64 = 18446744073709551615 |

### `==` binary on (u64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_476 | cpp/op_476 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_476 | go/op_470 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_476 | rust/op_260 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_476 | swift/op_524 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| cpp/op_476 | go/op_470 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_476 | rust/op_260 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_476 | swift/op_524 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_470 | rust/op_260 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_470 | swift/op_524 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| rust/op_260 | swift/op_524 | MATCHED | byte identity | the two units are the same machine bytes |

### `>` binary on (bool,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_569 | cpp/op_569 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |
| c/op_569 | rust/op_425 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |
| cpp/op_569 | rust/op_425 | MATCHED | byte identity | the two units are the same machine bytes |

### `>` binary on (bool,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_567 | cpp/op_567 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `>` binary on (bool,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_568 | cpp/op_568 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: I32StoF64 |

### `>` binary on (bool,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_564 | cpp/op_564 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `>` binary on (bool,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_565 | cpp/op_565 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |

### `>` binary on (bool,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_566 | cpp/op_566 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `>` binary on (f32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_557 | cpp/op_557 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `>` binary on (f32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_555 | cpp/op_555 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| c/op_555 | go/op_621 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| c/op_555 | rust/op_411 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| c/op_555 | swift/op_351 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| cpp/op_555 | go/op_621 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_555 | rust/op_411 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_555 | swift/op_351 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_621 | rust/op_411 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_621 | swift/op_351 | MATCHED | byte identity | the two units are the same machine bytes |
| rust/op_411 | swift/op_351 | MATCHED | byte identity | the two units are the same machine bytes |

### `>` binary on (f32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_556 | cpp/op_556 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `>` binary on (f32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_552 | cpp/op_552 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `>` binary on (f32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_553 | cpp/op_553 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `>` binary on (f32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_554 | cpp/op_554 | UNDECIDED | z3 over the two lifted forms | c op_554 is not straight-line: 4 blocks |

### `>` binary on (f64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_563 | cpp/op_563 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: I32StoF64 |

### `>` binary on (f64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_561 | cpp/op_561 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `>` binary on (f64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_562 | cpp/op_562 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| c/op_562 | go/op_628 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| c/op_562 | rust/op_418 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| c/op_562 | swift/op_358 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| cpp/op_562 | go/op_628 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_562 | rust/op_418 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_562 | swift/op_358 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_628 | rust/op_418 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_628 | swift/op_358 | MATCHED | byte identity | the two units are the same machine bytes |
| rust/op_418 | swift/op_358 | MATCHED | byte identity | the two units are the same machine bytes |

### `>` binary on (f64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_558 | cpp/op_558 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: I32StoF64 |

### `>` binary on (f64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_559 | cpp/op_559 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: I64StoF64 |

### `>` binary on (f64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_560 | cpp/op_560 | UNDECIDED | z3 over the two lifted forms | c op_560 is not pure scalar dataflow: riprel punpckldq; riprel subpd |

### `>` binary on (i32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_539 | cpp/op_539 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `>` binary on (i32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_537 | cpp/op_537 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `>` binary on (i32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_538 | cpp/op_538 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: I32StoF64 |

### `>` binary on (i32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_534 | cpp/op_534 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_534 | go/op_600 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_534 | rust/op_390 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_534 | swift/op_330 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| cpp/op_534 | go/op_600 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_534 | rust/op_390 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_534 | swift/op_330 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_600 | rust/op_390 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_600 | swift/op_330 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| rust/op_390 | swift/op_330 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |

### `>` binary on (i32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_535 | cpp/op_535 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| c/op_535 | swift/op_331 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| cpp/op_535 | swift/op_331 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |

### `>` binary on (i32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_536 | cpp/op_536 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 3758096128 |
| c/op_536 | swift/op_332 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 2147483648, in1_64 = 18446744071562067967 |
| cpp/op_536 | swift/op_332 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 2147483648, in1_64 = 18446744071562067967 |

### `>` binary on (i64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_545 | cpp/op_545 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |

### `>` binary on (i64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_543 | cpp/op_543 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `>` binary on (i64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_544 | cpp/op_544 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: I64StoF64 |

### `>` binary on (i64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_540 | cpp/op_540 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |
| c/op_540 | swift/op_336 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |
| cpp/op_540 | swift/op_336 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |

### `>` binary on (i64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_541 | cpp/op_541 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_541 | go/op_607 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_541 | rust/op_397 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_541 | swift/op_337 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| cpp/op_541 | go/op_607 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_541 | rust/op_397 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_541 | swift/op_337 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_607 | rust/op_397 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_607 | swift/op_337 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| rust/op_397 | swift/op_337 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |

### `>` binary on (i64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_542 | cpp/op_542 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_542 | swift/op_338 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 9223372036854775808, in1_64 = 9223372036854775807 |
| cpp/op_542 | swift/op_338 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 9223372036854775808, in1_64 = 9223372036854775807 |

### `>` binary on (u64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_551 | cpp/op_551 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |

### `>` binary on (u64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_549 | cpp/op_549 | UNDECIDED | z3 over the two lifted forms | c op_549 is not straight-line: 4 blocks |

### `>` binary on (u64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_550 | cpp/op_550 | UNDECIDED | z3 over the two lifted forms | c op_550 is not pure scalar dataflow: riprel punpckldq; riprel subpd |

### `>` binary on (u64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_546 | cpp/op_546 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |
| c/op_546 | swift/op_342 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18446744071562067969, in1_64 = 2147483648 |
| cpp/op_546 | swift/op_342 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18446744071562067968, in1_64 = 2147483648 |

### `>` binary on (u64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_547 | cpp/op_547 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_547 | swift/op_343 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 9223372036854775808, in1_64 = 9223372036854775808 |
| cpp/op_547 | swift/op_343 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 9223372036854775808, in1_64 = 9223372036854775808 |

### `>` binary on (u64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_548 | cpp/op_548 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_548 | go/op_614 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_548 | rust/op_404 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_548 | swift/op_344 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| cpp/op_548 | go/op_614 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_548 | rust/op_404 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_548 | swift/op_344 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_614 | rust/op_404 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_614 | swift/op_344 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| rust/op_404 | swift/op_344 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |

### `>=` binary on (bool,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_605 | cpp/op_605 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |
| c/op_605 | rust/op_461 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |
| cpp/op_605 | rust/op_461 | MATCHED | byte identity | the two units are the same machine bytes |

### `>=` binary on (bool,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_603 | cpp/op_603 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `>=` binary on (bool,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_604 | cpp/op_604 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: I32StoF64 |

### `>=` binary on (bool,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_600 | cpp/op_600 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `>=` binary on (bool,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_601 | cpp/op_601 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |

### `>=` binary on (bool,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_602 | cpp/op_602 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |

### `>=` binary on (f32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_593 | cpp/op_593 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `>=` binary on (f32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_591 | cpp/op_591 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| c/op_591 | go/op_657 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| c/op_591 | rust/op_447 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| c/op_591 | swift/op_423 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |
| cpp/op_591 | go/op_657 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_591 | rust/op_447 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_591 | swift/op_423 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_657 | rust/op_447 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_657 | swift/op_423 | MATCHED | byte identity | the two units are the same machine bytes |
| rust/op_447 | swift/op_423 | MATCHED | byte identity | the two units are the same machine bytes |

### `>=` binary on (f32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_592 | cpp/op_592 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `>=` binary on (f32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_588 | cpp/op_588 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `>=` binary on (f32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_589 | cpp/op_589 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `>=` binary on (f32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_590 | cpp/op_590 | UNDECIDED | z3 over the two lifted forms | c op_590 is not straight-line: 4 blocks |

### `>=` binary on (f64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_599 | cpp/op_599 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: I32StoF64 |

### `>=` binary on (f64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_597 | cpp/op_597 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `>=` binary on (f64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_598 | cpp/op_598 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| c/op_598 | go/op_664 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| c/op_598 | rust/op_454 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| c/op_598 | swift/op_430 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |
| cpp/op_598 | go/op_664 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_598 | rust/op_454 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_598 | swift/op_430 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_664 | rust/op_454 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_664 | swift/op_430 | MATCHED | byte identity | the two units are the same machine bytes |
| rust/op_454 | swift/op_430 | MATCHED | byte identity | the two units are the same machine bytes |

### `>=` binary on (f64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_594 | cpp/op_594 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: I32StoF64 |

### `>=` binary on (f64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_595 | cpp/op_595 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: I64StoF64 |

### `>=` binary on (f64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_596 | cpp/op_596 | UNDECIDED | z3 over the two lifted forms | c op_596 is not pure scalar dataflow: riprel punpckldq; riprel subpd |

### `>=` binary on (i32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_575 | cpp/op_575 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `>=` binary on (i32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_573 | cpp/op_573 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `>=` binary on (i32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_574 | cpp/op_574 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: I32StoF64 |

### `>=` binary on (i32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_570 | cpp/op_570 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_570 | go/op_636 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_570 | rust/op_426 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_570 | swift/op_402 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| cpp/op_570 | go/op_636 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_570 | rust/op_426 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_570 | swift/op_402 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_636 | rust/op_426 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_636 | swift/op_402 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| rust/op_426 | swift/op_402 | MATCHED | byte identity | the two units are the same machine bytes |

### `>=` binary on (i32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_571 | cpp/op_571 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| c/op_571 | swift/op_403 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| cpp/op_571 | swift/op_403 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |

### `>=` binary on (i32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_572 | cpp/op_572 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 4294967040 |
| c/op_572 | swift/op_404 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 2147483648, in1_64 = 18446744071562067969 |
| cpp/op_572 | swift/op_404 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 2147483648, in1_64 = 18446744071562067968 |

### `>=` binary on (i64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_581 | cpp/op_581 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |

### `>=` binary on (i64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_579 | cpp/op_579 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `>=` binary on (i64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_580 | cpp/op_580 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: I64StoF64 |

### `>=` binary on (i64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_576 | cpp/op_576 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |
| c/op_576 | swift/op_408 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |
| cpp/op_576 | swift/op_408 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |

### `>=` binary on (i64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_577 | cpp/op_577 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_577 | go/op_643 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_577 | rust/op_433 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_577 | swift/op_409 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| cpp/op_577 | go/op_643 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_577 | rust/op_433 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_577 | swift/op_409 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_643 | rust/op_433 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_643 | swift/op_409 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| rust/op_433 | swift/op_409 | MATCHED | byte identity | the two units are the same machine bytes |

### `>=` binary on (i64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_578 | cpp/op_578 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_578 | swift/op_410 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 9223372036854775808, in1_64 = 9223372036854775808 |
| cpp/op_578 | swift/op_410 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 9223372036854775808, in1_64 = 9223372036854775808 |

### `>=` binary on (u64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_587 | cpp/op_587 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |

### `>=` binary on (u64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_585 | cpp/op_585 | UNDECIDED | z3 over the two lifted forms | c op_585 is not straight-line: 4 blocks |

### `>=` binary on (u64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_586 | cpp/op_586 | UNDECIDED | z3 over the two lifted forms | c op_586 is not pure scalar dataflow: riprel punpckldq; riprel subpd |

### `>=` binary on (u64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_582 | cpp/op_582 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in1_64 = 4294967040 |
| c/op_582 | swift/op_414 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 56648833, in1_64 = 56648833 |
| cpp/op_582 | swift/op_414 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18446744071562067967, in1_64 = 2147483648 |

### `>=` binary on (u64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_583 | cpp/op_583 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_583 | swift/op_415 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 9223372036854775807, in1_64 = 9223372036854775808 |
| cpp/op_583 | swift/op_415 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 9223372036854775807, in1_64 = 9223372036854775808 |

### `>=` binary on (u64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_584 | cpp/op_584 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_584 | go/op_650 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_584 | rust/op_440 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| c/op_584 | swift/op_416 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |
| cpp/op_584 | go/op_650 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| cpp/op_584 | rust/op_440 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_584 | swift/op_416 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_650 | rust/op_440 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| go/op_650 | swift/op_416 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat) |
| rust/op_440 | swift/op_416 | MATCHED | byte identity | the two units are the same machine bytes |

### `>>` binary on (bool,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_749 | cpp/op_749 | MATCHED | byte identity | the two units are the same machine bytes |

### `>>` binary on (bool,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_744 | cpp/op_744 | MATCHED | byte identity | the two units are the same machine bytes |

### `>>` binary on (bool,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_745 | cpp/op_745 | MATCHED | byte identity | the two units are the same machine bytes |

### `>>` binary on (bool,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_746 | cpp/op_746 | MATCHED | byte identity | the two units are the same machine bytes |

### `>>` binary on (i32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_719 | cpp/op_719 | MATCHED | byte identity | the two units are the same machine bytes |

### `>>` binary on (i32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_714 | cpp/op_714 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_714 | go/op_204 | UNDECIDED | one side guards but the cores are not equal | core of c op_714 is ['zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))']; core of go op_204 is ['zx64(Or32(Not32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),32:64,u0:64))))),ex32@0(in1:64)))', 'zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,Or |
| c/op_714 | rust/op_498 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_714 | swift/op_726 | UNDECIDED | z3 over the two lifted forms | swift op_726 is not pure scalar dataflow: jmp $s9unit_ship6op_726ys5Int32VAD_ADtF |
| cpp/op_714 | go/op_204 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_714 is ['zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))']; core of go op_204 is ['zx64(Or32(Not32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),32:64,u0:64))))),ex32@0(in1:64)))', 'zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8, |
| cpp/op_714 | rust/op_498 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_714 | swift/op_726 | UNDECIDED | z3 over the two lifted forms | swift op_726 is not pure scalar dataflow: jmp $s9unit_ship6op_726ys5Int32VAD_ADtF |
| go/op_204 | rust/op_498 | UNDECIDED | one side guards but the cores are not equal | core of go op_204 is ['zx64(Or32(Not32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),32:64,u0:64))))),ex32@0(in1:64)))', 'zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,Or8(Not8(Sub8(0:8,And8(1:8,ex8@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),32:64,u0: |
| go/op_204 | swift/op_726 | UNDECIDED | one side guards but the cores are not equal | core of go op_204 is ['zx64(Or32(Not32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),32:64,u0:64))))),ex32@0(in1:64)))', 'zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,Or8(Not8(Sub8(0:8,And8(1:8,ex8@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),32:64,u0: |
| rust/op_498 | swift/op_726 | UNDECIDED | z3 over the two lifted forms | swift op_726 is not pure scalar dataflow: jmp $s9unit_ship6op_726ys5Int32VAD_ADtF |

### `>>` binary on (i32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_715 | cpp/op_715 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_715 | go/op_205 | UNDECIDED | one side guards but the cores are not equal | core of c op_715 is ['zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))']; core of go op_205 is ['Or64(Not64(Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,32:64,u0:64)))),in1:64)', 'zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,Or8(Not8(Sub8(0:8,And8(1:8,ex8@0(amd64 |
| c/op_715 | rust/op_499 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_715 | swift/op_727 | UNDECIDED | z3 over the two lifted forms | swift op_727 is not pure scalar dataflow: jmp $s9unit_ship6op_727ys5Int32VAD_s5Int64VtF |
| cpp/op_715 | go/op_205 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_715 is ['zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))']; core of go op_205 is ['Or64(Not64(Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,32:64,u0:64)))),in1:64)', 'zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,Or8(Not8(Sub8(0:8,And8(1:8,ex8@0(amd |
| cpp/op_715 | rust/op_499 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_715 | swift/op_727 | UNDECIDED | z3 over the two lifted forms | swift op_727 is not pure scalar dataflow: jmp $s9unit_ship6op_727ys5Int32VAD_s5Int64VtF |
| go/op_205 | rust/op_499 | UNDECIDED | one side guards but the cores are not equal | core of go op_205 is ['Or64(Not64(Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,32:64,u0:64)))),in1:64)', 'zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,Or8(Not8(Sub8(0:8,And8(1:8,ex8@0(amd64g_calculate_rflags_c(8:64,in1:64,32:64,u0:64))))),ex8@0(in1:64))))))']; core of rust op_499  |
| go/op_205 | swift/op_727 | UNDECIDED | one side guards but the cores are not equal | core of go op_205 is ['Or64(Not64(Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,32:64,u0:64)))),in1:64)', 'zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,Or8(Not8(Sub8(0:8,And8(1:8,ex8@0(amd64g_calculate_rflags_c(8:64,in1:64,32:64,u0:64))))),ex8@0(in1:64))))))']; core of swift op_727 |
| rust/op_499 | swift/op_727 | UNDECIDED | z3 over the two lifted forms | swift op_727 is not pure scalar dataflow: jmp $s9unit_ship6op_727ys5Int32VAD_s5Int64VtF |

### `>>` binary on (i32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_716 | cpp/op_716 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_716 | go/op_206 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (1 and 2) |
| c/op_716 | rust/op_500 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_716 | swift/op_728 | UNDECIDED | z3 over the two lifted forms | swift op_728 is not pure scalar dataflow: jmp $s9unit_ship6op_728ys5Int32VAD_s6UInt64VtF |
| cpp/op_716 | go/op_206 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (1 and 2) |
| cpp/op_716 | rust/op_500 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_716 | swift/op_728 | UNDECIDED | z3 over the two lifted forms | swift op_728 is not pure scalar dataflow: jmp $s9unit_ship6op_728ys5Int32VAD_s6UInt64VtF |
| go/op_206 | rust/op_500 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (2 and 1) |
| go/op_206 | swift/op_728 | UNDECIDED | z3 over the two lifted forms | swift op_728 is not pure scalar dataflow: jmp $s9unit_ship6op_728ys5Int32VAD_s6UInt64VtF |
| rust/op_500 | swift/op_728 | UNDECIDED | z3 over the two lifted forms | swift op_728 is not pure scalar dataflow: jmp $s9unit_ship6op_728ys5Int32VAD_s6UInt64VtF |

### `>>` binary on (i64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_725 | cpp/op_725 | MATCHED | byte identity | the two units are the same machine bytes |

### `>>` binary on (i64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_720 | cpp/op_720 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_720 | go/op_210 | UNDECIDED | one side guards but the cores are not equal | core of c op_720 is ['Sar64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_210 is ['Sar64(in0:64,And8(63:8,Or8(Not8(Sub8(0:8,And8(1:8,ex8@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),64:64,u0:64))))),ex8@0(in1:64))))', 'zx64(Or32(Not32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags |
| c/op_720 | rust/op_504 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_720 | swift/op_732 | UNDECIDED | z3 over the two lifted forms | swift op_732 is not pure scalar dataflow: jmp $s9unit_ship6op_732ys5Int64VAD_s5Int32VtF |
| cpp/op_720 | go/op_210 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_720 is ['Sar64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_210 is ['Sar64(in0:64,And8(63:8,Or8(Not8(Sub8(0:8,And8(1:8,ex8@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),64:64,u0:64))))),ex8@0(in1:64))))', 'zx64(Or32(Not32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rfla |
| cpp/op_720 | rust/op_504 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_720 | swift/op_732 | UNDECIDED | z3 over the two lifted forms | swift op_732 is not pure scalar dataflow: jmp $s9unit_ship6op_732ys5Int64VAD_s5Int32VtF |
| go/op_210 | rust/op_504 | UNDECIDED | one side guards but the cores are not equal | core of go op_210 is ['Sar64(in0:64,And8(63:8,Or8(Not8(Sub8(0:8,And8(1:8,ex8@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),64:64,u0:64))))),ex8@0(in1:64))))', 'zx64(Or32(Not32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),64:64,u0:64))))),ex32@0(in1:64)))'] |
| go/op_210 | swift/op_732 | UNDECIDED | one side guards but the cores are not equal | core of go op_210 is ['Sar64(in0:64,And8(63:8,Or8(Not8(Sub8(0:8,And8(1:8,ex8@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),64:64,u0:64))))),ex8@0(in1:64))))', 'zx64(Or32(Not32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),64:64,u0:64))))),ex32@0(in1:64)))'] |
| rust/op_504 | swift/op_732 | UNDECIDED | z3 over the two lifted forms | swift op_732 is not pure scalar dataflow: jmp $s9unit_ship6op_732ys5Int64VAD_s5Int32VtF |

### `>>` binary on (i64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_721 | cpp/op_721 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_721 | go/op_211 | UNDECIDED | one side guards but the cores are not equal | core of c op_721 is ['Sar64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_211 is ['Or64(Not64(Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64)))),in1:64)', 'Sar64(in0:64,And8(63:8,Or8(Not8(Sub8(0:8,And8(1:8,ex8@0(amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))),ex8@ |
| c/op_721 | rust/op_505 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_721 | swift/op_733 | UNDECIDED | z3 over the two lifted forms | swift op_733 is not pure scalar dataflow: jmp $s9unit_ship6op_733ys5Int64VAD_ADtF |
| cpp/op_721 | go/op_211 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_721 is ['Sar64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_211 is ['Or64(Not64(Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64)))),in1:64)', 'Sar64(in0:64,And8(63:8,Or8(Not8(Sub8(0:8,And8(1:8,ex8@0(amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))),ex |
| cpp/op_721 | rust/op_505 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_721 | swift/op_733 | UNDECIDED | z3 over the two lifted forms | swift op_733 is not pure scalar dataflow: jmp $s9unit_ship6op_733ys5Int64VAD_ADtF |
| go/op_211 | rust/op_505 | UNDECIDED | one side guards but the cores are not equal | core of go op_211 is ['Or64(Not64(Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64)))),in1:64)', 'Sar64(in0:64,And8(63:8,Or8(Not8(Sub8(0:8,And8(1:8,ex8@0(amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))),ex8@0(in1:64))))']; core of rust op_505 is ['Sar64(in0:64,And8(63:8, |
| go/op_211 | swift/op_733 | UNDECIDED | one side guards but the cores are not equal | core of go op_211 is ['Or64(Not64(Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64)))),in1:64)', 'Sar64(in0:64,And8(63:8,Or8(Not8(Sub8(0:8,And8(1:8,ex8@0(amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))),ex8@0(in1:64))))']; core of swift op_733 is [] |
| rust/op_505 | swift/op_733 | UNDECIDED | z3 over the two lifted forms | swift op_733 is not pure scalar dataflow: jmp $s9unit_ship6op_733ys5Int64VAD_ADtF |

### `>>` binary on (i64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_722 | cpp/op_722 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_722 | go/op_212 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (1 and 2) |
| c/op_722 | rust/op_506 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_722 | swift/op_734 | UNDECIDED | z3 over the two lifted forms | swift op_734 is not pure scalar dataflow: jmp $s9unit_ship6op_734ys5Int64VAD_s6UInt64VtF |
| cpp/op_722 | go/op_212 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (1 and 2) |
| cpp/op_722 | rust/op_506 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_722 | swift/op_734 | UNDECIDED | z3 over the two lifted forms | swift op_734 is not pure scalar dataflow: jmp $s9unit_ship6op_734ys5Int64VAD_s6UInt64VtF |
| go/op_212 | rust/op_506 | UNDECIDED | z3 over the two lifted forms | the two units leave a different number of live results (2 and 1) |
| go/op_212 | swift/op_734 | UNDECIDED | z3 over the two lifted forms | swift op_734 is not pure scalar dataflow: jmp $s9unit_ship6op_734ys5Int64VAD_s6UInt64VtF |
| rust/op_506 | swift/op_734 | UNDECIDED | z3 over the two lifted forms | swift op_734 is not pure scalar dataflow: jmp $s9unit_ship6op_734ys5Int64VAD_s6UInt64VtF |

### `>>` binary on (u64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_731 | cpp/op_731 | MATCHED | byte identity | the two units are the same machine bytes |

### `>>` binary on (u64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_726 | cpp/op_726 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_726 | go/op_216 | UNDECIDED | one side guards but the cores are not equal | core of c op_726 is ['Shr64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_216 is ['And64(Shr64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),64:64,u0:64))))'] |
| c/op_726 | rust/op_510 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_726 | swift/op_738 | UNDECIDED | z3 over the two lifted forms | swift op_738 is not pure scalar dataflow: jmp $s9unit_ship6op_738ys6UInt64VAD_s5Int32VtF |
| cpp/op_726 | go/op_216 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_726 is ['Shr64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_216 is ['And64(Shr64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),64:64,u0:64))))'] |
| cpp/op_726 | rust/op_510 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_726 | swift/op_738 | UNDECIDED | z3 over the two lifted forms | swift op_738 is not pure scalar dataflow: jmp $s9unit_ship6op_738ys6UInt64VAD_s5Int32VtF |
| go/op_216 | rust/op_510 | UNDECIDED | one side guards but the cores are not equal | core of go op_216 is ['And64(Shr64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),64:64,u0:64))))']; core of rust op_510 is ['Shr64(in0:64,And8(63:8,ex8@0(in1:64)))'] |
| go/op_216 | swift/op_738 | UNDECIDED | one side guards but the cores are not equal | core of go op_216 is ['And64(Shr64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),64:64,u0:64))))']; core of swift op_738 is [] |
| rust/op_510 | swift/op_738 | UNDECIDED | z3 over the two lifted forms | swift op_738 is not pure scalar dataflow: jmp $s9unit_ship6op_738ys6UInt64VAD_s5Int32VtF |

### `>>` binary on (u64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_727 | cpp/op_727 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_727 | go/op_217 | UNDECIDED | one side guards but the cores are not equal | core of c op_727 is ['Shr64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_217 is ['And64(Shr64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))'] |
| c/op_727 | rust/op_511 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_727 | swift/op_739 | UNDECIDED | z3 over the two lifted forms | swift op_739 is not straight-line: 7 blocks |
| cpp/op_727 | go/op_217 | UNDECIDED | one side guards but the cores are not equal | core of cpp op_727 is ['Shr64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_217 is ['And64(Shr64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))'] |
| cpp/op_727 | rust/op_511 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_727 | swift/op_739 | UNDECIDED | z3 over the two lifted forms | swift op_739 is not straight-line: 7 blocks |
| go/op_217 | rust/op_511 | UNDECIDED | one side guards but the cores are not equal | core of go op_217 is ['And64(Shr64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))']; core of rust op_511 is ['Shr64(in0:64,And8(63:8,ex8@0(in1:64)))'] |
| go/op_217 | swift/op_739 | UNDECIDED | one side guards but the cores are not equal | core of go op_217 is ['And64(Shr64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))']; core of swift op_739 is ['Add64(18446744073709551551:64,in1:64)', 'Shl64(u1:64,And8(63:8,Sub8(0:8,ex8@0(in1:64))))', 'Shr64(u1:64,And8(63:8,ex8@0(in1:64) |
| rust/op_511 | swift/op_739 | UNDECIDED | z3 over the two lifted forms | swift op_739 is not straight-line: 7 blocks |

### `>>` binary on (u64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_728 | cpp/op_728 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_728 | go/op_218 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: VEX helper call not modelled: amd64g_calculate_rflags_c |
| c/op_728 | rust/op_512 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_728 | swift/op_740 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 17870283317111160831, in1_64 = 64 |
| cpp/op_728 | go/op_218 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: VEX helper call not modelled: amd64g_calculate_rflags_c |
| cpp/op_728 | rust/op_512 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_728 | swift/op_740 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18158513697555742718, in1_64 = 65 |
| go/op_218 | rust/op_512 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: VEX helper call not modelled: amd64g_calculate_rflags_c |
| go/op_218 | swift/op_740 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: VEX helper call not modelled: amd64g_calculate_rflags_c |
| rust/op_512 | swift/op_740 | UNMATCHED | z3 over the two lifted forms | z3 counterexample: in0_64 = 18158513693262872576, in1_64 = 96 |

### `^` binary on (bool,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_425 | cpp/op_425 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_425 | rust/op_245 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_425 | rust/op_245 | MATCHED | byte identity | the two units are the same machine bytes |

### `^` binary on (bool,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_420 | cpp/op_420 | MATCHED | byte identity | the two units are the same machine bytes |

### `^` binary on (bool,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_421 | cpp/op_421 | MATCHED | byte identity | the two units are the same machine bytes |

### `^` binary on (bool,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_422 | cpp/op_422 | MATCHED | byte identity | the two units are the same machine bytes |

### `^` binary on (i32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_395 | cpp/op_395 | MATCHED | byte identity | the two units are the same machine bytes |

### `^` binary on (i32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_390 | cpp/op_390 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_390 | go/op_420 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_390 | rust/op_210 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_390 | swift/op_654 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_390 | go/op_420 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_390 | rust/op_210 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_390 | swift/op_654 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_420 | rust/op_210 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_420 | swift/op_654 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| rust/op_210 | swift/op_654 | MATCHED | byte identity | the two units are the same machine bytes |

### `^` binary on (i32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_391 | cpp/op_391 | MATCHED | byte identity | the two units are the same machine bytes |

### `^` binary on (i32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_392 | cpp/op_392 | MATCHED | byte identity | the two units are the same machine bytes |

### `^` binary on (i64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_401 | cpp/op_401 | MATCHED | byte identity | the two units are the same machine bytes |

### `^` binary on (i64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_396 | cpp/op_396 | MATCHED | byte identity | the two units are the same machine bytes |

### `^` binary on (i64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_397 | cpp/op_397 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_397 | go/op_427 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_397 | rust/op_217 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_397 | swift/op_661 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_397 | go/op_427 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_397 | rust/op_217 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_397 | swift/op_661 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_427 | rust/op_217 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_427 | swift/op_661 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| rust/op_217 | swift/op_661 | MATCHED | byte identity | the two units are the same machine bytes |

### `^` binary on (i64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_398 | cpp/op_398 | MATCHED | byte identity | the two units are the same machine bytes |

### `^` binary on (u64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_407 | cpp/op_407 | MATCHED | byte identity | the two units are the same machine bytes |

### `^` binary on (u64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_402 | cpp/op_402 | MATCHED | byte identity | the two units are the same machine bytes |

### `^` binary on (u64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_403 | cpp/op_403 | MATCHED | byte identity | the two units are the same machine bytes |

### `^` binary on (u64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_404 | cpp/op_404 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_404 | go/op_434 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_404 | rust/op_224 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_404 | swift/op_668 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_404 | go/op_434 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_404 | rust/op_224 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_404 | swift/op_668 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_434 | rust/op_224 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_434 | swift/op_668 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| rust/op_224 | swift/op_668 | MATCHED | byte identity | the two units are the same machine bytes |

### `sizeof` unary on (bool,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_53 | cpp/op_65 | MATCHED | byte identity | the two units are the same machine bytes |

### `sizeof` unary on (f32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_51 | cpp/op_63 | MATCHED | byte identity | the two units are the same machine bytes |

### `sizeof` unary on (f64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_52 | cpp/op_64 | MATCHED | byte identity | the two units are the same machine bytes |

### `sizeof` unary on (i32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_48 | cpp/op_60 | MATCHED | byte identity | the two units are the same machine bytes |

### `sizeof` unary on (i64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_49 | cpp/op_61 | MATCHED | byte identity | the two units are the same machine bytes |

### `sizeof` unary on (u64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_50 | cpp/op_62 | MATCHED | byte identity | the two units are the same machine bytes |

### `|` binary on (bool,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_389 | cpp/op_389 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_389 | rust/op_209 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_389 | rust/op_209 | MATCHED | byte identity | the two units are the same machine bytes |

### `|` binary on (bool,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_384 | cpp/op_384 | MATCHED | byte identity | the two units are the same machine bytes |

### `|` binary on (bool,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_385 | cpp/op_385 | MATCHED | byte identity | the two units are the same machine bytes |

### `|` binary on (bool,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_386 | cpp/op_386 | MATCHED | byte identity | the two units are the same machine bytes |

### `|` binary on (i32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_359 | cpp/op_359 | MATCHED | byte identity | the two units are the same machine bytes |

### `|` binary on (i32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_354 | cpp/op_354 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_354 | go/op_384 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_354 | rust/op_174 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_354 | swift/op_618 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_354 | go/op_384 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_354 | rust/op_174 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_354 | swift/op_618 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_384 | rust/op_174 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_384 | swift/op_618 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| rust/op_174 | swift/op_618 | MATCHED | byte identity | the two units are the same machine bytes |

### `|` binary on (i32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_355 | cpp/op_355 | MATCHED | byte identity | the two units are the same machine bytes |

### `|` binary on (i32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_356 | cpp/op_356 | MATCHED | byte identity | the two units are the same machine bytes |

### `|` binary on (i64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_365 | cpp/op_365 | MATCHED | byte identity | the two units are the same machine bytes |

### `|` binary on (i64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_360 | cpp/op_360 | MATCHED | byte identity | the two units are the same machine bytes |

### `|` binary on (i64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_361 | cpp/op_361 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_361 | go/op_391 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_361 | rust/op_181 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_361 | swift/op_625 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_361 | go/op_391 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_361 | rust/op_181 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_361 | swift/op_625 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_391 | rust/op_181 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_391 | swift/op_625 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| rust/op_181 | swift/op_625 | MATCHED | byte identity | the two units are the same machine bytes |

### `|` binary on (i64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_362 | cpp/op_362 | MATCHED | byte identity | the two units are the same machine bytes |

### `|` binary on (u64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_371 | cpp/op_371 | MATCHED | byte identity | the two units are the same machine bytes |

### `|` binary on (u64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_366 | cpp/op_366 | MATCHED | byte identity | the two units are the same machine bytes |

### `|` binary on (u64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_367 | cpp/op_367 | MATCHED | byte identity | the two units are the same machine bytes |

### `|` binary on (u64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_368 | cpp/op_368 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_368 | go/op_398 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_368 | rust/op_188 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_368 | swift/op_632 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_368 | go/op_398 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_368 | rust/op_188 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_368 | swift/op_632 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_398 | rust/op_188 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_398 | swift/op_632 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| rust/op_188 | swift/op_632 | MATCHED | byte identity | the two units are the same machine bytes |

### `||` binary on (bool,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_317 | cpp/op_317 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_317 | go/op_743 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| c/op_317 | rust/op_137 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_317 | swift/op_833 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_317 | go/op_743 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| cpp/op_317 | rust/op_137 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_317 | swift/op_833 | MATCHED | byte identity | the two units are the same machine bytes |
| go/op_743 | rust/op_137 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| go/op_743 | swift/op_833 | MATCHED | sem identity (anchored) | the two anchored lifted forms are identical |
| rust/op_137 | swift/op_833 | MATCHED | byte identity | the two units are the same machine bytes |

### `||` binary on (bool,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_315 | cpp/op_315 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `||` binary on (bool,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_316 | cpp/op_316 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |

### `||` binary on (bool,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_312 | cpp/op_312 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `||` binary on (bool,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_313 | cpp/op_313 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `||` binary on (bool,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_314 | cpp/op_314 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `||` binary on (f32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_305 | cpp/op_305 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `||` binary on (f32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_303 | cpp/op_303 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: XorV128 |

### `||` binary on (f32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_304 | cpp/op_304 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `||` binary on (f32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_300 | cpp/op_300 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `||` binary on (f32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_301 | cpp/op_301 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `||` binary on (f32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_302 | cpp/op_302 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `||` binary on (f64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_311 | cpp/op_311 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |

### `||` binary on (f64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_309 | cpp/op_309 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `||` binary on (f64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_310 | cpp/op_310 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: XorV128 |

### `||` binary on (f64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_306 | cpp/op_306 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |

### `||` binary on (f64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_307 | cpp/op_307 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |

### `||` binary on (f64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_308 | cpp/op_308 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |

### `||` binary on (i32,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_287 | cpp/op_287 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `||` binary on (i32,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_285 | cpp/op_285 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `||` binary on (i32,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_286 | cpp/op_286 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |

### `||` binary on (i32,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_282 | cpp/op_282 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `||` binary on (i32,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_283 | cpp/op_283 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `||` binary on (i32,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_284 | cpp/op_284 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `||` binary on (i64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_293 | cpp/op_293 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `||` binary on (i64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_291 | cpp/op_291 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `||` binary on (i64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_292 | cpp/op_292 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |

### `||` binary on (i64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_288 | cpp/op_288 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `||` binary on (i64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_289 | cpp/op_289 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `||` binary on (i64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_290 | cpp/op_290 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `||` binary on (u64,bool)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_299 | cpp/op_299 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `||` binary on (u64,f32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_297 | cpp/op_297 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: unary VEX op not modelled: F32toF64 |

### `||` binary on (u64,f64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_298 | cpp/op_298 | UNDECIDED | z3 over the two lifted forms | z3 was not asked: binary VEX op not modelled: CmpF64 |

### `||` binary on (u64,i32)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_294 | cpp/op_294 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `||` binary on (u64,i64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_295 | cpp/op_295 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `||` binary on (u64,u64)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_296 | cpp/op_296 | MATCHED | z3 over the two lifted forms | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the two units define 64 and 8 bits of that result and only the low bits are common to both |

### `~` unary on (bool,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_11 | cpp/op_11 | MATCHED | byte identity | the two units are the same machine bytes |

### `~` unary on (i32,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_6 | cpp/op_6 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_6 | swift/op_36 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_6 | swift/op_36 | MATCHED | byte identity | the two units are the same machine bytes |

### `~` unary on (i64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_7 | cpp/op_7 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_7 | swift/op_37 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_7 | swift/op_37 | MATCHED | byte identity | the two units are the same machine bytes |

### `~` unary on (u64,None)

| left | right | verdict | ground | detail |
| --- | --- | --- | --- | --- |
| c/op_8 | cpp/op_8 | MATCHED | byte identity | the two units are the same machine bytes |
| c/op_8 | swift/op_38 | MATCHED | byte identity | the two units are the same machine bytes |
| cpp/op_8 | swift/op_38 | MATCHED | byte identity | the two units are the same machine bytes |
