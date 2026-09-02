# dominant table, rebuilt -- flat digest

Multi-language classes (>=3 languages), one plain table each.
`canonical mnem` = the unit's instructions after the rename into the canonical runnable form (first 6); `(rename refused)` where the canonicaliser refused, with the reason under the table.

## K0001 &middot; types (f32,None) &middot; result f32 &middot; 9 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `+` | `ret` |
| c | `__extension__` | `ret` |
| c | `++` | `ret` |
| c | `--` | `ret` |
| cpp | `+` | `ret` |
| cpp | `++` | `ret` |
| cpp | `--` | `ret` |
| go | `+` | `ret` |
| swift | `+` | `ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0002 &middot; types (f64,None) &middot; result f64 &middot; 9 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `--` | `ret` |
| c | `+` | `ret` |
| c | `__extension__` | `ret` |
| c | `++` | `ret` |
| cpp | `+` | `ret` |
| cpp | `++` | `ret` |
| cpp | `--` | `ret` |
| go | `+` | `ret` |
| swift | `+` | `ret` |

- weakest evidence: canonical byte identity (after the rename into the canonical runnable form, the two units assemble to the same machine bytes)

## K0003 &middot; types (i32,None) &middot; result i32 &middot; 8 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `+` | `mov %edi,%eax; ret` |
| c | `__extension__` | `mov %edi,%eax; ret` |
| c | `++` | `mov %edi,%eax; ret` |
| c | `--` | `mov %edi,%eax; ret` |
| cpp | `+` | `mov %edi,%eax; ret` |
| cpp | `++` | `mov %edi,%eax; ret` |
| cpp | `--` | `mov %edi,%eax; ret` |
| swift | `+` | `mov %edi,%eax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0004 &middot; types (i64,None) &middot; result i64 &middot; 8 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `+` | `mov %rdi,%rax; ret` |
| c | `__extension__` | `mov %rdi,%rax; ret` |
| c | `++` | `mov %rdi,%rax; ret` |
| c | `--` | `mov %rdi,%rax; ret` |
| cpp | `+` | `mov %rdi,%rax; ret` |
| cpp | `++` | `mov %rdi,%rax; ret` |
| cpp | `--` | `mov %rdi,%rax; ret` |
| swift | `+` | `mov %rdi,%rax; ret` |

- weakest evidence: canonical byte identity (after the rename into the canonical runnable form, the two units assemble to the same machine bytes)

## K0005 &middot; types (u64,None) &middot; result u64 &middot; 8 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `+` | `mov %rdi,%rax; ret` |
| c | `__extension__` | `mov %rdi,%rax; ret` |
| c | `++` | `mov %rdi,%rax; ret` |
| c | `--` | `mov %rdi,%rax; ret` |
| cpp | `+` | `mov %rdi,%rax; ret` |
| cpp | `++` | `mov %rdi,%rax; ret` |
| cpp | `--` | `mov %rdi,%rax; ret` |
| swift | `+` | `mov %rdi,%rax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0007 &middot; types (i32,None) &middot; result i32 &middot; 6 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `~` | `mov %edi,%eax; not %eax; ret` |
| cpp | `compl` | `mov %edi,%eax; not %eax; ret` |
| cpp | `~` | `mov %edi,%eax; not %eax; ret` |
| go | `^` | `(rename refused)` |
| rust | `!` | `mov %edi,%eax; not %eax; ret` |
| swift | `~` | `mov %edi,%eax; not %eax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0008 &middot; types (i64,None) &middot; result i64 &middot; 6 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `~` | `mov %rdi,%rax; not %rax; ret` |
| cpp | `compl` | `mov %rdi,%rax; not %rax; ret` |
| cpp | `~` | `mov %rdi,%rax; not %rax; ret` |
| go | `^` | `(rename refused)` |
| rust | `!` | `mov %rdi,%rax; not %rax; ret` |
| swift | `~` | `mov %rdi,%rax; not %rax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0009 &middot; types (u64,None) &middot; result u64 &middot; 6 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `~` | `mov %rdi,%rax; not %rax; ret` |
| cpp | `compl` | `mov %rdi,%rax; not %rax; ret` |
| cpp | `~` | `mov %rdi,%rax; not %rax; ret` |
| go | `^` | `(rename refused)` |
| rust | `!` | `mov %rdi,%rax; not %rax; ret` |
| swift | `~` | `mov %rdi,%rax; not %rax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0010 &middot; types (i32,i32) &middot; result i32 &middot; 6 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `&` | `mov %edi,%eax; and %esi,%eax; ret` |
| cpp | `&` | `mov %edi,%eax; and %esi,%eax; ret` |
| cpp | `bitand` | `mov %edi,%eax; and %esi,%eax; ret` |
| go | `&` | `(rename refused)` |
| rust | `&` | `mov %edi,%eax; and %esi,%eax; ret` |
| swift | `&` | `mov %edi,%eax; and %esi,%eax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0011 &middot; types (i64,i64) &middot; result i64 &middot; 6 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `&` | `mov %rdi,%rax; and %rsi,%rax; ret` |
| cpp | `&` | `mov %rdi,%rax; and %rsi,%rax; ret` |
| cpp | `bitand` | `mov %rdi,%rax; and %rsi,%rax; ret` |
| go | `&` | `(rename refused)` |
| rust | `&` | `mov %rdi,%rax; and %rsi,%rax; ret` |
| swift | `&` | `mov %rdi,%rax; and %rsi,%rax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0012 &middot; types (u64,u64) &middot; result u64 &middot; 6 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `&` | `mov %rdi,%rax; and %rsi,%rax; ret` |
| cpp | `&` | `mov %rdi,%rax; and %rsi,%rax; ret` |
| cpp | `bitand` | `mov %rdi,%rax; and %rsi,%rax; ret` |
| go | `&` | `(rename refused)` |
| rust | `&` | `mov %rdi,%rax; and %rsi,%rax; ret` |
| swift | `&` | `mov %rdi,%rax; and %rsi,%rax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0013 &middot; types (i32,i32) &middot; result i32 &middot; 6 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `|` | `mov %edi,%eax; or %esi,%eax; ret` |
| cpp | `|` | `mov %edi,%eax; or %esi,%eax; ret` |
| cpp | `bitor` | `mov %edi,%eax; or %esi,%eax; ret` |
| go | `|` | `(rename refused)` |
| rust | `|` | `mov %edi,%eax; or %esi,%eax; ret` |
| swift | `|` | `mov %edi,%eax; or %esi,%eax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0014 &middot; types (i64,i64) &middot; result i64 &middot; 6 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `|` | `mov %rdi,%rax; or %rsi,%rax; ret` |
| cpp | `|` | `mov %rdi,%rax; or %rsi,%rax; ret` |
| cpp | `bitor` | `mov %rdi,%rax; or %rsi,%rax; ret` |
| go | `|` | `(rename refused)` |
| rust | `|` | `mov %rdi,%rax; or %rsi,%rax; ret` |
| swift | `|` | `mov %rdi,%rax; or %rsi,%rax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0015 &middot; types (u64,u64) &middot; result u64 &middot; 6 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `|` | `mov %rdi,%rax; or %rsi,%rax; ret` |
| cpp | `|` | `mov %rdi,%rax; or %rsi,%rax; ret` |
| cpp | `bitor` | `mov %rdi,%rax; or %rsi,%rax; ret` |
| go | `|` | `(rename refused)` |
| rust | `|` | `mov %rdi,%rax; or %rsi,%rax; ret` |
| swift | `|` | `mov %rdi,%rax; or %rsi,%rax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0016 &middot; types (i32,i32) &middot; result i32 &middot; 6 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `^` | `mov %edi,%eax; xor %esi,%eax; ret` |
| cpp | `^` | `mov %edi,%eax; xor %esi,%eax; ret` |
| cpp | `xor` | `mov %edi,%eax; xor %esi,%eax; ret` |
| go | `^` | `(rename refused)` |
| rust | `^` | `mov %edi,%eax; xor %esi,%eax; ret` |
| swift | `^` | `mov %edi,%eax; xor %esi,%eax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0017 &middot; types (i64,i64) &middot; result i64 &middot; 6 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `^` | `mov %rdi,%rax; xor %rsi,%rax; ret` |
| cpp | `^` | `mov %rdi,%rax; xor %rsi,%rax; ret` |
| cpp | `xor` | `mov %rdi,%rax; xor %rsi,%rax; ret` |
| go | `^` | `(rename refused)` |
| rust | `^` | `mov %rdi,%rax; xor %rsi,%rax; ret` |
| swift | `^` | `mov %rdi,%rax; xor %rsi,%rax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0018 &middot; types (u64,u64) &middot; result u64 &middot; 6 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `^` | `mov %rdi,%rax; xor %rsi,%rax; ret` |
| cpp | `^` | `mov %rdi,%rax; xor %rsi,%rax; ret` |
| cpp | `xor` | `mov %rdi,%rax; xor %rsi,%rax; ret` |
| go | `^` | `(rename refused)` |
| rust | `^` | `mov %rdi,%rax; xor %rsi,%rax; ret` |
| swift | `^` | `mov %rdi,%rax; xor %rsi,%rax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0019 &middot; types (bool,bool) &middot; result bool &middot; 6 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `&&` | `mov %edi,%eax; and %esi,%eax; ret` |
| cpp | `and` | `mov %edi,%eax; and %esi,%eax; ret` |
| go | `&&` | `(rename refused)` |
| rust | `&&` | `mov %edi,%eax; and %esi,%eax; ret` |
| rust | `&` | `mov %edi,%eax; and %esi,%eax; ret` |
| swift | `&&` | `mov %edi,%eax; and %esi,%eax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0020 &middot; types (bool,bool) &middot; result bool &middot; 6 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `||` | `mov %edi,%eax; or %esi,%eax; ret` |
| cpp | `or` | `mov %edi,%eax; or %esi,%eax; ret` |
| go | `||` | `(rename refused)` |
| rust | `||` | `mov %edi,%eax; or %esi,%eax; ret` |
| rust | `|` | `mov %edi,%eax; or %esi,%eax; ret` |
| swift | `||` | `mov %edi,%eax; or %esi,%eax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0027 &middot; types (f32,f32) &middot; result f32 &middot; 5 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `*` | `mulss %xmm1,%xmm0; ret` |
| cpp | `*` | `mulss %xmm1,%xmm0; ret` |
| go | `*` | `mulss %xmm1,%xmm0; ret` |
| rust | `*` | `mulss %xmm1,%xmm0; ret` |
| swift | `*` | `mulss %xmm1,%xmm0; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0028 &middot; types (f64,f64) &middot; result f64 &middot; 5 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `*` | `mulsd %xmm1,%xmm0; ret` |
| cpp | `*` | `mulsd %xmm1,%xmm0; ret` |
| go | `*` | `mulsd %xmm1,%xmm0; ret` |
| rust | `*` | `mulsd %xmm1,%xmm0; ret` |
| swift | `*` | `mulsd %xmm1,%xmm0; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0029 &middot; types (f32,f32) &middot; result f32 &middot; 5 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `/` | `divss %xmm1,%xmm0; ret` |
| cpp | `/` | `divss %xmm1,%xmm0; ret` |
| go | `/` | `divss %xmm1,%xmm0; ret` |
| rust | `/` | `divss %xmm1,%xmm0; ret` |
| swift | `/` | `divss %xmm1,%xmm0; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0030 &middot; types (f64,f64) &middot; result f64 &middot; 5 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `/` | `divsd %xmm1,%xmm0; ret` |
| cpp | `/` | `divsd %xmm1,%xmm0; ret` |
| go | `/` | `divsd %xmm1,%xmm0; ret` |
| rust | `/` | `divsd %xmm1,%xmm0; ret` |
| swift | `/` | `divsd %xmm1,%xmm0; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0031 &middot; types (f32,f32) &middot; result f32 &middot; 5 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `+` | `addss %xmm1,%xmm0; ret` |
| cpp | `+` | `addss %xmm1,%xmm0; ret` |
| go | `+` | `addss %xmm1,%xmm0; ret` |
| rust | `+` | `addss %xmm1,%xmm0; ret` |
| swift | `+` | `addss %xmm1,%xmm0; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0032 &middot; types (f64,f64) &middot; result f64 &middot; 5 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `+` | `addsd %xmm1,%xmm0; ret` |
| cpp | `+` | `addsd %xmm1,%xmm0; ret` |
| go | `+` | `addsd %xmm1,%xmm0; ret` |
| rust | `+` | `addsd %xmm1,%xmm0; ret` |
| swift | `+` | `addsd %xmm1,%xmm0; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0033 &middot; types (f32,f32) &middot; result f32 &middot; 5 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `-` | `subss %xmm1,%xmm0; ret` |
| cpp | `-` | `subss %xmm1,%xmm0; ret` |
| go | `-` | `subss %xmm1,%xmm0; ret` |
| rust | `-` | `subss %xmm1,%xmm0; ret` |
| swift | `-` | `subss %xmm1,%xmm0; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0034 &middot; types (f64,f64) &middot; result f64 &middot; 5 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `-` | `subsd %xmm1,%xmm0; ret` |
| cpp | `-` | `subsd %xmm1,%xmm0; ret` |
| go | `-` | `subsd %xmm1,%xmm0; ret` |
| rust | `-` | `subsd %xmm1,%xmm0; ret` |
| swift | `-` | `subsd %xmm1,%xmm0; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0035 &middot; types (bool,None) &middot; result bool &middot; 5 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `--` | `mov %edi,%eax; xor $0x1,%al; ret` |
| cpp | `not` | `mov %edi,%eax; xor $0x1,%al; ret` |
| cpp | `!` | `mov %edi,%eax; xor $0x1,%al; ret` |
| rust | `!` | `mov %edi,%eax; xor $0x1,%al; ret` |
| swift | `!` | `mov %edi,%eax; xor $0x1,%al; ret` |

- weakest evidence: canonical byte identity (after the rename into the canonical runnable form, the two units assemble to the same machine bytes)

## K0036 &middot; types (bool,bool) &middot; result bool &middot; 5 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `not_eq` | `mov %edi,%eax; xor %esi,%eax; ret` |
| cpp | `!=` | `mov %edi,%eax; xor %esi,%eax; ret` |
| rust | `^` | `mov %edi,%eax; xor %esi,%eax; ret` |
| rust | `!=` | `mov %edi,%eax; xor %esi,%eax; ret` |
| swift | `!=` | `mov %edi,%eax; xor %esi,%eax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0041 &middot; types (i32,None) &middot; result i32 &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `-` | `mov %edi,%eax; neg %eax; ret` |
| cpp | `-` | `mov %edi,%eax; neg %eax; ret` |
| go | `-` | `(rename refused)` |
| rust | `-` | `mov %edi,%eax; neg %eax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0042 &middot; types (i64,None) &middot; result i64 &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `-` | `mov %rdi,%rax; neg %rax; ret` |
| cpp | `-` | `mov %rdi,%rax; neg %rax; ret` |
| go | `-` | `(rename refused)` |
| rust | `-` | `mov %rdi,%rax; neg %rax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0043 &middot; types (i32,i32) &middot; result i32 &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `+` | `lea (%rdi,%rsi,1),%eax; ret` |
| cpp | `+` | `lea (%rdi,%rsi,1),%eax; ret` |
| go | `+` | `(rename refused)` |
| rust | `+` | `lea (%rdi,%rsi,1),%eax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0044 &middot; types (i64,i64) &middot; result i64 &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `+` | `lea (%rdi,%rsi,1),%rax; ret` |
| cpp | `+` | `lea (%rdi,%rsi,1),%rax; ret` |
| go | `+` | `(rename refused)` |
| rust | `+` | `lea (%rdi,%rsi,1),%rax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0045 &middot; types (u64,u64) &middot; result u64 &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `+` | `lea (%rdi,%rsi,1),%rax; ret` |
| cpp | `+` | `lea (%rdi,%rsi,1),%rax; ret` |
| go | `+` | `(rename refused)` |
| rust | `+` | `lea (%rdi,%rsi,1),%rax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0046 &middot; types (i32,i32) &middot; result i32 &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `-` | `mov %edi,%eax; sub %esi,%eax; ret` |
| cpp | `-` | `mov %edi,%eax; sub %esi,%eax; ret` |
| go | `-` | `(rename refused)` |
| rust | `-` | `mov %edi,%eax; sub %esi,%eax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0047 &middot; types (i64,i64) &middot; result i64 &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `-` | `mov %rdi,%rax; sub %rsi,%rax; ret` |
| cpp | `-` | `mov %rdi,%rax; sub %rsi,%rax; ret` |
| go | `-` | `(rename refused)` |
| rust | `-` | `mov %rdi,%rax; sub %rsi,%rax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0048 &middot; types (u64,u64) &middot; result u64 &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `-` | `mov %rdi,%rax; sub %rsi,%rax; ret` |
| cpp | `-` | `mov %rdi,%rax; sub %rsi,%rax; ret` |
| go | `-` | `(rename refused)` |
| rust | `-` | `mov %rdi,%rax; sub %rsi,%rax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0049 &middot; types (i32,i32) &middot; result i32 &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `*` | `mov %edi,%eax; imul %esi,%eax; ret` |
| cpp | `*` | `mov %edi,%eax; imul %esi,%eax; ret` |
| go | `*` | `(rename refused)` |
| rust | `*` | `mov %edi,%eax; imul %esi,%eax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0050 &middot; types (i64,i64) &middot; result i64 &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `*` | `mov %rdi,%rax; imul %rsi,%rax; ret` |
| cpp | `*` | `mov %rdi,%rax; imul %rsi,%rax; ret` |
| go | `*` | `(rename refused)` |
| rust | `*` | `mov %rdi,%rax; imul %rsi,%rax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0051 &middot; types (u64,u64) &middot; result u64 &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `*` | `mov %rdi,%rax; imul %rsi,%rax; ret` |
| cpp | `*` | `mov %rdi,%rax; imul %rsi,%rax; ret` |
| go | `*` | `(rename refused)` |
| rust | `*` | `mov %rdi,%rax; imul %rsi,%rax; ret` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0052 &middot; types (f32,None) &middot; result f32 &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `-` | `xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` |
| cpp | `-` | `xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` |
| rust | `-` | `xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` |
| swift | `-` | `xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI1_0-0x4; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0053 &middot; types (f64,None) &middot; result f64 &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `-` | `xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` |
| cpp | `-` | `xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` |
| rust | `-` | `xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` |
| swift | `-` | `xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI1_0-0x4; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0054 &middot; types (f32,f32) &middot; result bool &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `<` | `ucomiss %xmm0,%xmm1; seta %al; ret` |
| go | `<` | `ucomiss %xmm0,%xmm1; seta %al; ret` |
| rust | `<` | `ucomiss %xmm0,%xmm1; seta %al; ret` |
| swift | `<` | `ucomiss %xmm0,%xmm1; seta %al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0055 &middot; types (f64,f64) &middot; result bool &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `<` | `ucomisd %xmm0,%xmm1; seta %al; ret` |
| go | `<` | `ucomisd %xmm0,%xmm1; seta %al; ret` |
| rust | `<` | `ucomisd %xmm0,%xmm1; seta %al; ret` |
| swift | `<` | `ucomisd %xmm0,%xmm1; seta %al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0056 &middot; types (f32,f32) &middot; result bool &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `>` | `ucomiss %xmm1,%xmm0; seta %al; ret` |
| go | `>` | `ucomiss %xmm1,%xmm0; seta %al; ret` |
| rust | `>` | `ucomiss %xmm1,%xmm0; seta %al; ret` |
| swift | `>` | `ucomiss %xmm1,%xmm0; seta %al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0057 &middot; types (f64,f64) &middot; result bool &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `>` | `ucomisd %xmm1,%xmm0; seta %al; ret` |
| go | `>` | `ucomisd %xmm1,%xmm0; seta %al; ret` |
| rust | `>` | `ucomisd %xmm1,%xmm0; seta %al; ret` |
| swift | `>` | `ucomisd %xmm1,%xmm0; seta %al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0058 &middot; types (f32,f32) &middot; result bool &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `<=` | `ucomiss %xmm0,%xmm1; setae %al; ret` |
| go | `<=` | `ucomiss %xmm0,%xmm1; setae %al; ret` |
| rust | `<=` | `ucomiss %xmm0,%xmm1; setae %al; ret` |
| swift | `<=` | `ucomiss %xmm0,%xmm1; setae %al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0059 &middot; types (f64,f64) &middot; result bool &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `<=` | `ucomisd %xmm0,%xmm1; setae %al; ret` |
| go | `<=` | `ucomisd %xmm0,%xmm1; setae %al; ret` |
| rust | `<=` | `ucomisd %xmm0,%xmm1; setae %al; ret` |
| swift | `<=` | `ucomisd %xmm0,%xmm1; setae %al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0060 &middot; types (f32,f32) &middot; result bool &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `>=` | `ucomiss %xmm1,%xmm0; setae %al; ret` |
| go | `>=` | `ucomiss %xmm1,%xmm0; setae %al; ret` |
| rust | `>=` | `ucomiss %xmm1,%xmm0; setae %al; ret` |
| swift | `>=` | `ucomiss %xmm1,%xmm0; setae %al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0061 &middot; types (f64,f64) &middot; result bool &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `>=` | `ucomisd %xmm1,%xmm0; setae %al; ret` |
| go | `>=` | `ucomisd %xmm1,%xmm0; setae %al; ret` |
| rust | `>=` | `ucomisd %xmm1,%xmm0; setae %al; ret` |
| swift | `>=` | `ucomisd %xmm1,%xmm0; setae %al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0062 &middot; types (i32,i32) &middot; result bool &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `!=` | `cmp %esi,%edi; setne %al; ret` |
| cpp | `not_eq` | `cmp %esi,%edi; setne %al; ret` |
| rust | `!=` | `cmp %esi,%edi; setne %al; ret` |
| swift | `!=` | `cmp %esi,%edi; setne %al; ret` |

- weakest evidence: canonical byte identity (after the rename into the canonical runnable form, the two units assemble to the same machine bytes)

## K0063 &middot; types (i64,i64) &middot; result bool &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `!=` | `cmp %rsi,%rdi; setne %al; ret` |
| cpp | `not_eq` | `cmp %rsi,%rdi; setne %al; ret` |
| rust | `!=` | `cmp %rsi,%rdi; setne %al; ret` |
| swift | `!=` | `cmp %rsi,%rdi; setne %al; ret` |

- weakest evidence: canonical byte identity (after the rename into the canonical runnable form, the two units assemble to the same machine bytes)

## K0064 &middot; types (u64,u64) &middot; result bool &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `!=` | `cmp %rsi,%rdi; setne %al; ret` |
| cpp | `not_eq` | `cmp %rsi,%rdi; setne %al; ret` |
| rust | `!=` | `cmp %rsi,%rdi; setne %al; ret` |
| swift | `!=` | `cmp %rsi,%rdi; setne %al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0065 &middot; types (f32,f32) &middot; result bool &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `!=` | `cmpneqss %xmm1,%xmm0; movd %xmm0,%eax; and $0x1,%eax; ret` |
| cpp | `not_eq` | `cmpneqss %xmm1,%xmm0; movd %xmm0,%eax; and $0x1,%eax; ret` |
| rust | `!=` | `cmpneqss %xmm1,%xmm0; movd %xmm0,%eax; and $0x1,%eax; ret` |
| swift | `!=` | `cmpneqss %xmm1,%xmm0; movd %xmm0,%eax; and $0x1,%eax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0066 &middot; types (f64,f64) &middot; result bool &middot; 4 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `!=` | `cmpneqsd %xmm1,%xmm0; movq %xmm0,%rax; and $0x1,%eax; ret` |
| cpp | `not_eq` | `cmpneqsd %xmm1,%xmm0; movq %xmm0,%rax; and $0x1,%eax; ret` |
| rust | `!=` | `cmpneqsd %xmm1,%xmm0; movq %xmm0,%rax; and $0x1,%eax; ret` |
| swift | `!=` | `cmpneqsd %xmm1,%xmm0; movq %xmm0,%rax; and $0x1,%eax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0105 &middot; types (u64,None) &middot; result u64 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `-` | `mov %rdi,%rax; neg %rax; ret` |
| cpp | `-` | `mov %rdi,%rax; neg %rax; ret` |
| go | `-` | `(rename refused)` |

- canon_refused: the unit modifies an argument in place and returns it, which a rename cannot express (the argument's register %rdi is not the result's %rax)

- weakest evidence: anchored sem identity (the two lifted forms are identical)

## K0106 &middot; types (i32,i32) &middot; result i32 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `<<` | `mov %esi,%ecx; mov %edi,%eax; shl %cl,%eax; ret` |
| cpp | `<<` | `mov %esi,%ecx; mov %edi,%eax; shl %cl,%eax; ret` |
| rust | `<<` | `mov %esi,%ecx; mov %edi,%eax; shl %cl,%eax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0107 &middot; types (i32,i64) &middot; result i32 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `<<` | `mov %rsi,%rcx; mov %edi,%eax; shl %cl,%eax; ret` |
| cpp | `<<` | `mov %rsi,%rcx; mov %edi,%eax; shl %cl,%eax; ret` |
| rust | `<<` | `mov %rsi,%rcx; mov %edi,%eax; shl %cl,%eax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0108 &middot; types (i32,u64) &middot; result i32 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `<<` | `mov %rsi,%rcx; mov %edi,%eax; shl %cl,%eax; ret` |
| cpp | `<<` | `mov %rsi,%rcx; mov %edi,%eax; shl %cl,%eax; ret` |
| rust | `<<` | `mov %rsi,%rcx; mov %edi,%eax; shl %cl,%eax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0109 &middot; types (i64,i32) &middot; result i64 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `<<` | `mov %esi,%ecx; mov %rdi,%rax; shl %cl,%rax; ret` |
| cpp | `<<` | `mov %esi,%ecx; mov %rdi,%rax; shl %cl,%rax; ret` |
| rust | `<<` | `mov %esi,%ecx; mov %rdi,%rax; shl %cl,%rax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0110 &middot; types (i64,i64) &middot; result i64 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `<<` | `mov %rsi,%rcx; mov %rdi,%rax; shl %cl,%rax; ret` |
| cpp | `<<` | `mov %rsi,%rcx; mov %rdi,%rax; shl %cl,%rax; ret` |
| rust | `<<` | `mov %rsi,%rcx; mov %rdi,%rax; shl %cl,%rax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0111 &middot; types (i64,u64) &middot; result i64 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `<<` | `mov %rsi,%rcx; mov %rdi,%rax; shl %cl,%rax; ret` |
| cpp | `<<` | `mov %rsi,%rcx; mov %rdi,%rax; shl %cl,%rax; ret` |
| rust | `<<` | `mov %rsi,%rcx; mov %rdi,%rax; shl %cl,%rax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0112 &middot; types (u64,i32) &middot; result u64 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `<<` | `mov %esi,%ecx; mov %rdi,%rax; shl %cl,%rax; ret` |
| cpp | `<<` | `mov %esi,%ecx; mov %rdi,%rax; shl %cl,%rax; ret` |
| rust | `<<` | `mov %esi,%ecx; mov %rdi,%rax; shl %cl,%rax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0113 &middot; types (u64,i64) &middot; result u64 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `<<` | `mov %rsi,%rcx; mov %rdi,%rax; shl %cl,%rax; ret` |
| cpp | `<<` | `mov %rsi,%rcx; mov %rdi,%rax; shl %cl,%rax; ret` |
| rust | `<<` | `mov %rsi,%rcx; mov %rdi,%rax; shl %cl,%rax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0114 &middot; types (u64,u64) &middot; result u64 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `<<` | `mov %rsi,%rcx; mov %rdi,%rax; shl %cl,%rax; ret` |
| cpp | `<<` | `mov %rsi,%rcx; mov %rdi,%rax; shl %cl,%rax; ret` |
| rust | `<<` | `mov %rsi,%rcx; mov %rdi,%rax; shl %cl,%rax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0115 &middot; types (i32,i32) &middot; result i32 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `>>` | `mov %esi,%ecx; mov %edi,%eax; sar %cl,%eax; ret` |
| cpp | `>>` | `mov %esi,%ecx; mov %edi,%eax; sar %cl,%eax; ret` |
| rust | `>>` | `mov %esi,%ecx; mov %edi,%eax; sar %cl,%eax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0116 &middot; types (i32,i64) &middot; result i32 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `>>` | `mov %rsi,%rcx; mov %edi,%eax; sar %cl,%eax; ret` |
| cpp | `>>` | `mov %rsi,%rcx; mov %edi,%eax; sar %cl,%eax; ret` |
| rust | `>>` | `mov %rsi,%rcx; mov %edi,%eax; sar %cl,%eax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0117 &middot; types (i32,u64) &middot; result i32 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `>>` | `mov %rsi,%rcx; mov %edi,%eax; sar %cl,%eax; ret` |
| cpp | `>>` | `mov %rsi,%rcx; mov %edi,%eax; sar %cl,%eax; ret` |
| rust | `>>` | `mov %rsi,%rcx; mov %edi,%eax; sar %cl,%eax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0118 &middot; types (i64,i32) &middot; result i64 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `>>` | `mov %esi,%ecx; mov %rdi,%rax; sar %cl,%rax; ret` |
| cpp | `>>` | `mov %esi,%ecx; mov %rdi,%rax; sar %cl,%rax; ret` |
| rust | `>>` | `mov %esi,%ecx; mov %rdi,%rax; sar %cl,%rax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0119 &middot; types (i64,i64) &middot; result i64 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `>>` | `mov %rsi,%rcx; mov %rdi,%rax; sar %cl,%rax; ret` |
| cpp | `>>` | `mov %rsi,%rcx; mov %rdi,%rax; sar %cl,%rax; ret` |
| rust | `>>` | `mov %rsi,%rcx; mov %rdi,%rax; sar %cl,%rax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0120 &middot; types (i64,u64) &middot; result i64 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `>>` | `mov %rsi,%rcx; mov %rdi,%rax; sar %cl,%rax; ret` |
| cpp | `>>` | `mov %rsi,%rcx; mov %rdi,%rax; sar %cl,%rax; ret` |
| rust | `>>` | `mov %rsi,%rcx; mov %rdi,%rax; sar %cl,%rax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0121 &middot; types (u64,i32) &middot; result u64 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `>>` | `mov %esi,%ecx; mov %rdi,%rax; shr %cl,%rax; ret` |
| cpp | `>>` | `mov %esi,%ecx; mov %rdi,%rax; shr %cl,%rax; ret` |
| rust | `>>` | `mov %esi,%ecx; mov %rdi,%rax; shr %cl,%rax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0122 &middot; types (u64,i64) &middot; result u64 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `>>` | `mov %rsi,%rcx; mov %rdi,%rax; shr %cl,%rax; ret` |
| cpp | `>>` | `mov %rsi,%rcx; mov %rdi,%rax; shr %cl,%rax; ret` |
| rust | `>>` | `mov %rsi,%rcx; mov %rdi,%rax; shr %cl,%rax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0123 &middot; types (u64,u64) &middot; result u64 &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| c | `>>` | `mov %rsi,%rcx; mov %rdi,%rax; shr %cl,%rax; ret` |
| cpp | `>>` | `mov %rsi,%rcx; mov %rdi,%rax; shr %cl,%rax; ret` |
| rust | `>>` | `mov %rsi,%rcx; mov %rdi,%rax; shr %cl,%rax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0124 &middot; types (i32,i32) &middot; result bool &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `<` | `cmp %esi,%edi; setl %al; ret` |
| rust | `<` | `cmp %esi,%edi; setl %al; ret` |
| swift | `<` | `cmp %esi,%edi; setl %al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0125 &middot; types (i64,i64) &middot; result bool &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `<` | `cmp %rsi,%rdi; setl %al; ret` |
| rust | `<` | `cmp %rsi,%rdi; setl %al; ret` |
| swift | `<` | `cmp %rsi,%rdi; setl %al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0126 &middot; types (u64,u64) &middot; result bool &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `<` | `cmp %rsi,%rdi; setb %al; ret` |
| rust | `<` | `cmp %rsi,%rdi; setb %al; ret` |
| swift | `<` | `cmp %rsi,%rdi; setb %al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0127 &middot; types (i32,i32) &middot; result bool &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `>=` | `cmp %esi,%edi; setge %al; ret` |
| rust | `>=` | `cmp %esi,%edi; setge %al; ret` |
| swift | `>=` | `cmp %esi,%edi; setge %al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0128 &middot; types (i64,i64) &middot; result bool &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `>=` | `cmp %rsi,%rdi; setge %al; ret` |
| rust | `>=` | `cmp %rsi,%rdi; setge %al; ret` |
| swift | `>=` | `cmp %rsi,%rdi; setge %al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0129 &middot; types (u64,u64) &middot; result bool &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `>=` | `cmp %rsi,%rdi; setae %al; ret` |
| rust | `>=` | `cmp %rsi,%rdi; setae %al; ret` |
| swift | `>=` | `cmp %rsi,%rdi; setae %al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0130 &middot; types (i32,i32) &middot; result bool &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `==` | `cmp %esi,%edi; sete %al; ret` |
| rust | `==` | `cmp %esi,%edi; sete %al; ret` |
| swift | `==` | `cmp %esi,%edi; sete %al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0131 &middot; types (i64,i64) &middot; result bool &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `==` | `cmp %rsi,%rdi; sete %al; ret` |
| rust | `==` | `cmp %rsi,%rdi; sete %al; ret` |
| swift | `==` | `cmp %rsi,%rdi; sete %al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0132 &middot; types (u64,u64) &middot; result bool &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `==` | `cmp %rsi,%rdi; sete %al; ret` |
| rust | `==` | `cmp %rsi,%rdi; sete %al; ret` |
| swift | `==` | `cmp %rsi,%rdi; sete %al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0133 &middot; types (f32,f32) &middot; result bool &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `==` | `cmpeqss %xmm1,%xmm0; movd %xmm0,%eax; and $0x1,%eax; ret` |
| rust | `==` | `cmpeqss %xmm1,%xmm0; movd %xmm0,%eax; and $0x1,%eax; ret` |
| swift | `==` | `cmpeqss %xmm1,%xmm0; movd %xmm0,%eax; and $0x1,%eax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0134 &middot; types (f64,f64) &middot; result bool &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `==` | `cmpeqsd %xmm1,%xmm0; movq %xmm0,%rax; and $0x1,%eax; ret` |
| rust | `==` | `cmpeqsd %xmm1,%xmm0; movq %xmm0,%rax; and $0x1,%eax; ret` |
| swift | `==` | `cmpeqsd %xmm1,%xmm0; movq %xmm0,%rax; and $0x1,%eax; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

## K0135 &middot; types (bool,bool) &middot; result bool &middot; 3 members

| lang | label | canonical mnem |
| --- | --- | --- |
| cpp | `==` | `mov %edi,%eax; xor %esi,%eax; xor $0x1,%al; ret` |
| rust | `==` | `mov %edi,%eax; xor %esi,%eax; xor $0x1,%al; ret` |
| swift | `==` | `mov %edi,%eax; xor %esi,%eax; xor $0x1,%al; ret` |

- weakest evidence: byte identity (the two units are the same machine bytes)

