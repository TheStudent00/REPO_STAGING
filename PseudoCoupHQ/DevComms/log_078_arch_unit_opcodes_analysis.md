# Log 078: Arch-Unit Opcodes Analysis

**Date:** 2026-08-29
**Subject:** Accounting of Unique Opcodes and Traced-Arguments within Canonical Arch-Units

## Overview
An analysis was run across all canonical texts (extracted via `canon4` to capture the raw compiler-operator before normalization) for all target languages (C, C++, Go, Rust, Swift). The goal was to identify how many unique architectural opcodes directly operate on high-level "traced-arguments" (the standard ABI input registers).

### Summary Counts
- **Total Unique Opcodes (Any):** 83
- **Unique Opcodes Using Traced-Arguments:** 68

---

### Opcodes Using Traced-Arguments (68)
These are the opcodes where at least one of the high-level input arguments (traced-arguments) is directly used as an operand (e.g., `%rdi`, `%xmm0`, `%rax` in Go):

`add`, `addsd`, `addss`, `and`, `andpd`, `andps`, `cmovb`, `cmove`, `cmovne`, `cmp`, `cmpeqsd`, `cmpeqss`, `cmpneqsd`, `cmpneqss`, `cvtsi2sd`, `cvtsi2ss`, `cvtss2sd`, `div`, `divsd`, `divss`, `idiv`, `imul`, `lea`, `mov`, `movapd`, `movaps`, `movd`, `movq`, `movsd`, `movslq`, `movss`, `movzbl`, `mulsd`, `mulss`, `neg`, `not`, `or`, `orpd`, `orps`, `punpckldq`, `pxor`, `sar`, `sbb`, `seta`, `setae`, `setb`, `setbe`, `sete`, `setg`, `setge`, `setl`, `setle`, `setne`, `setnp`, `setp`, `shl`, `shr`, `sub`, `subpd`, `subsd`, `subss`, `test`, `ucomisd`, `ucomiss`, `unpckhpd`, `xor`, `xorpd`, `xorps`

---

### The Rest (15)
These are the remaining opcodes that appear in the arch-units but *do not* directly take a traced-argument as an operand (usually operating on return registers, internal state, flags, or managing control flow):

`call`, `cltd`, `cqto`, `jb`, `je`, `jl`, `jmp`, `jne`, `jo`, `js`, `movabs`, `ret`, `setns`, `sets`, `ud2`

*(Note: Jump labels like `L0:` were filtered out from the final count.)*
