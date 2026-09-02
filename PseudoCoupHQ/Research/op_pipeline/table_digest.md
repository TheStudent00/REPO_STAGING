# dominant table — flat digest

Multi-language classes (>=3 languages), one plain table each.
`ship mnem` = the optimized build's instructions (first 6).

## K0001 · types (bool,bool) · 12 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `&` | `mov %edi,%eax; and %esi,%eax; ret` |
| c | `&&` | `mov %edi,%eax; and %esi,%eax; ret` |
| c | `*` | `mov %edi,%eax; and %esi,%eax; ret` |
| cpp | `&` | `mov %edi,%eax; and %esi,%eax; ret` |
| cpp | `&&` | `mov %edi,%eax; and %esi,%eax; ret` |
| cpp | `*` | `mov %edi,%eax; and %esi,%eax; ret` |
| cpp | `and` | `mov %edi,%eax; and %esi,%eax; ret` |
| cpp | `bitand` | `mov %edi,%eax; and %esi,%eax; ret` |
| go | `&&` | `and %ebx,%eax; ret` |
| rust | `&` | `mov %edi,%eax; and %esi,%eax; ret` |
| rust | `&&` | `mov %edi,%eax; and %esi,%eax; ret` |
| swift | `&&` | `mov %edi,%eax; and %esi,%eax; ret` |

## K0004 · types (bool,bool) · 10 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `|` | `mov %edi,%eax; or %esi,%eax; ret` |
| c | `||` | `mov %edi,%eax; or %esi,%eax; ret` |
| cpp | `bitor` | `mov %edi,%eax; or %esi,%eax; ret` |
| cpp | `or` | `mov %edi,%eax; or %esi,%eax; ret` |
| cpp | `|` | `mov %edi,%eax; or %esi,%eax; ret` |
| cpp | `||` | `mov %edi,%eax; or %esi,%eax; ret` |
| go | `||` | `or %ebx,%eax; ret` |
| rust | `|` | `mov %edi,%eax; or %esi,%eax; ret` |
| rust | `||` | `mov %edi,%eax; or %esi,%eax; ret` |
| swift | `||` | `mov %edi,%eax; or %esi,%eax; ret` |

## K0008 · types (bool,bool) · 9 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `!=` | `mov %edi,%eax; xor %esi,%eax; ret` |
| c | `^` | `mov %edi,%eax; xor %esi,%eax; ret` |
| cpp | `!=` | `mov %edi,%eax; xor %esi,%eax; ret` |
| cpp | `^` | `mov %edi,%eax; xor %esi,%eax; ret` |
| cpp | `not_eq` | `mov %edi,%eax; xor %esi,%eax; ret` |
| cpp | `xor` | `mov %edi,%eax; xor %esi,%eax; ret` |
| rust | `!=` | `mov %edi,%eax; xor %esi,%eax; ret` |
| rust | `^` | `mov %edi,%eax; xor %esi,%eax; ret` |
| swift | `!=` | `mov %edi,%eax; xor %esi,%eax; ret` |

## K0010 · types (i32,None) · 6 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `~` | `mov %edi,%eax; not %eax; ret` |
| cpp | `compl` | `mov %edi,%eax; not %eax; ret` |
| cpp | `~` | `mov %edi,%eax; not %eax; ret` |
| go | `^` | `not %eax; ret` |
| rust | `!` | `mov %edi,%eax; not %eax; ret` |
| swift | `~` | `mov %edi,%eax; not %eax; ret` |

## K0011 · types (i64,None) · 6 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `~` | `mov %rdi,%rax; not %rax; ret` |
| cpp | `compl` | `mov %rdi,%rax; not %rax; ret` |
| cpp | `~` | `mov %rdi,%rax; not %rax; ret` |
| go | `^` | `not %rax; ret` |
| rust | `!` | `mov %rdi,%rax; not %rax; ret` |
| swift | `~` | `mov %rdi,%rax; not %rax; ret` |

## K0012 · types (u64,None) · 6 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `~` | `mov %rdi,%rax; not %rax; ret` |
| cpp | `compl` | `mov %rdi,%rax; not %rax; ret` |
| cpp | `~` | `mov %rdi,%rax; not %rax; ret` |
| go | `^` | `not %rax; ret` |
| rust | `!` | `mov %rdi,%rax; not %rax; ret` |
| swift | `~` | `mov %rdi,%rax; not %rax; ret` |

## K0013 · types (i32,i32) · 6 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `&` | `mov %edi,%eax; and %esi,%eax; ret` |
| cpp | `&` | `mov %edi,%eax; and %esi,%eax; ret` |
| cpp | `bitand` | `mov %edi,%eax; and %esi,%eax; ret` |
| go | `&` | `and %ebx,%eax; ret` |
| rust | `&` | `mov %edi,%eax; and %esi,%eax; ret` |
| swift | `&` | `mov %edi,%eax; and %esi,%eax; ret` |

## K0014 · types (i64,i64) · 6 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `&` | `mov %rdi,%rax; and %rsi,%rax; ret` |
| cpp | `&` | `mov %rdi,%rax; and %rsi,%rax; ret` |
| cpp | `bitand` | `mov %rdi,%rax; and %rsi,%rax; ret` |
| go | `&` | `and %rbx,%rax; ret` |
| rust | `&` | `mov %rdi,%rax; and %rsi,%rax; ret` |
| swift | `&` | `mov %rdi,%rax; and %rsi,%rax; ret` |

## K0015 · types (u64,u64) · 6 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `&` | `mov %rdi,%rax; and %rsi,%rax; ret` |
| cpp | `&` | `mov %rdi,%rax; and %rsi,%rax; ret` |
| cpp | `bitand` | `mov %rdi,%rax; and %rsi,%rax; ret` |
| go | `&` | `and %rbx,%rax; ret` |
| rust | `&` | `mov %rdi,%rax; and %rsi,%rax; ret` |
| swift | `&` | `mov %rdi,%rax; and %rsi,%rax; ret` |

## K0016 · types (i32,i32) · 6 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `|` | `mov %edi,%eax; or %esi,%eax; ret` |
| cpp | `bitor` | `mov %edi,%eax; or %esi,%eax; ret` |
| cpp | `|` | `mov %edi,%eax; or %esi,%eax; ret` |
| go | `|` | `or %ebx,%eax; ret` |
| rust | `|` | `mov %edi,%eax; or %esi,%eax; ret` |
| swift | `|` | `mov %edi,%eax; or %esi,%eax; ret` |

## K0017 · types (i64,i64) · 6 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `|` | `mov %rdi,%rax; or %rsi,%rax; ret` |
| cpp | `bitor` | `mov %rdi,%rax; or %rsi,%rax; ret` |
| cpp | `|` | `mov %rdi,%rax; or %rsi,%rax; ret` |
| go | `|` | `or %rbx,%rax; ret` |
| rust | `|` | `mov %rdi,%rax; or %rsi,%rax; ret` |
| swift | `|` | `mov %rdi,%rax; or %rsi,%rax; ret` |

## K0018 · types (u64,u64) · 6 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `|` | `mov %rdi,%rax; or %rsi,%rax; ret` |
| cpp | `bitor` | `mov %rdi,%rax; or %rsi,%rax; ret` |
| cpp | `|` | `mov %rdi,%rax; or %rsi,%rax; ret` |
| go | `|` | `or %rbx,%rax; ret` |
| rust | `|` | `mov %rdi,%rax; or %rsi,%rax; ret` |
| swift | `|` | `mov %rdi,%rax; or %rsi,%rax; ret` |

## K0019 · types (i32,i32) · 6 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `^` | `mov %edi,%eax; xor %esi,%eax; ret` |
| cpp | `^` | `mov %edi,%eax; xor %esi,%eax; ret` |
| cpp | `xor` | `mov %edi,%eax; xor %esi,%eax; ret` |
| go | `^` | `xor %ebx,%eax; ret` |
| rust | `^` | `mov %edi,%eax; xor %esi,%eax; ret` |
| swift | `^` | `mov %edi,%eax; xor %esi,%eax; ret` |

## K0020 · types (i64,i64) · 6 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `^` | `mov %rdi,%rax; xor %rsi,%rax; ret` |
| cpp | `^` | `mov %rdi,%rax; xor %rsi,%rax; ret` |
| cpp | `xor` | `mov %rdi,%rax; xor %rsi,%rax; ret` |
| go | `^` | `xor %rbx,%rax; ret` |
| rust | `^` | `mov %rdi,%rax; xor %rsi,%rax; ret` |
| swift | `^` | `mov %rdi,%rax; xor %rsi,%rax; ret` |

## K0021 · types (u64,u64) · 6 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `^` | `mov %rdi,%rax; xor %rsi,%rax; ret` |
| cpp | `^` | `mov %rdi,%rax; xor %rsi,%rax; ret` |
| cpp | `xor` | `mov %rdi,%rax; xor %rsi,%rax; ret` |
| go | `^` | `xor %rbx,%rax; ret` |
| rust | `^` | `mov %rdi,%rax; xor %rsi,%rax; ret` |
| swift | `^` | `mov %rdi,%rax; xor %rsi,%rax; ret` |

## K0028 · types (f32,f32) · 5 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `*` | `mulss %xmm1,%xmm0; ret` |
| cpp | `*` | `mulss %xmm1,%xmm0; ret` |
| go | `*` | `mulss %xmm1,%xmm0; ret` |
| rust | `*` | `mulss %xmm1,%xmm0; ret` |
| swift | `*` | `mulss %xmm1,%xmm0; ret` |

## K0029 · types (f64,f64) · 5 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `*` | `mulsd %xmm1,%xmm0; ret` |
| cpp | `*` | `mulsd %xmm1,%xmm0; ret` |
| go | `*` | `mulsd %xmm1,%xmm0; ret` |
| rust | `*` | `mulsd %xmm1,%xmm0; ret` |
| swift | `*` | `mulsd %xmm1,%xmm0; ret` |

## K0030 · types (f32,f32) · 5 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `/` | `divss %xmm1,%xmm0; ret` |
| cpp | `/` | `divss %xmm1,%xmm0; ret` |
| go | `/` | `divss %xmm1,%xmm0; ret` |
| rust | `/` | `divss %xmm1,%xmm0; ret` |
| swift | `/` | `divss %xmm1,%xmm0; ret` |

## K0031 · types (f64,f64) · 5 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `/` | `divsd %xmm1,%xmm0; ret` |
| cpp | `/` | `divsd %xmm1,%xmm0; ret` |
| go | `/` | `divsd %xmm1,%xmm0; ret` |
| rust | `/` | `divsd %xmm1,%xmm0; ret` |
| swift | `/` | `divsd %xmm1,%xmm0; ret` |

## K0032 · types (f32,f32) · 5 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `+` | `addss %xmm1,%xmm0; ret` |
| cpp | `+` | `addss %xmm1,%xmm0; ret` |
| go | `+` | `addss %xmm1,%xmm0; ret` |
| rust | `+` | `addss %xmm1,%xmm0; ret` |
| swift | `+` | `addss %xmm1,%xmm0; ret` |

## K0033 · types (f64,f64) · 5 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `+` | `addsd %xmm1,%xmm0; ret` |
| cpp | `+` | `addsd %xmm1,%xmm0; ret` |
| go | `+` | `addsd %xmm1,%xmm0; ret` |
| rust | `+` | `addsd %xmm1,%xmm0; ret` |
| swift | `+` | `addsd %xmm1,%xmm0; ret` |

## K0034 · types (f32,f32) · 5 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `-` | `subss %xmm1,%xmm0; ret` |
| cpp | `-` | `subss %xmm1,%xmm0; ret` |
| go | `-` | `subss %xmm1,%xmm0; ret` |
| rust | `-` | `subss %xmm1,%xmm0; ret` |
| swift | `-` | `subss %xmm1,%xmm0; ret` |

## K0035 · types (f64,f64) · 5 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `-` | `subsd %xmm1,%xmm0; ret` |
| cpp | `-` | `subsd %xmm1,%xmm0; ret` |
| go | `-` | `subsd %xmm1,%xmm0; ret` |
| rust | `-` | `subsd %xmm1,%xmm0; ret` |
| swift | `-` | `subsd %xmm1,%xmm0; ret` |

## K0036 · types (f32,f32) · 5 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `!=` | `cmpneqss %xmm1,%xmm0; movd %xmm0,%eax; and $0x1,%eax; ret` |
| cpp | `!=` | `cmpneqss %xmm1,%xmm0; movd %xmm0,%eax; and $0x1,%eax; ret` |
| cpp | `not_eq` | `cmpneqss %xmm1,%xmm0; movd %xmm0,%eax; and $0x1,%eax; ret` |
| rust | `!=` | `cmpneqss %xmm1,%xmm0; movd %xmm0,%eax; and $0x1,%eax; ret` |
| swift | `!=` | `cmpneqss %xmm1,%xmm0; movd %xmm0,%eax; and $0x1,%eax; ret` |

## K0037 · types (f64,f64) · 5 members

| lang | label | ship mnem |
| --- | --- | --- |
| c | `!=` | `cmpneqsd %xmm1,%xmm0; movq %xmm0,%rax; and $0x1,%eax; ret` |
| cpp | `!=` | `cmpneqsd %xmm1,%xmm0; movq %xmm0,%rax; and $0x1,%eax; ret` |
| cpp | `not_eq` | `cmpneqsd %xmm1,%xmm0; movq %xmm0,%rax; and $0x1,%eax; ret` |
| rust | `!=` | `cmpneqsd %xmm1,%xmm0; movq %xmm0,%rax; and $0x1,%eax; ret` |
| swift | `!=` | `cmpneqsd %xmm1,%xmm0; movq %xmm0,%rax; and $0x1,%eax; ret` |
