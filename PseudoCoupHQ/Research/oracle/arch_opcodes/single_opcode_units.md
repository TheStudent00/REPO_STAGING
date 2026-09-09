# single_opcode_units -- task o2 deliverable 1

## Population

| language | units read | units with body | units without body |
|---|---|---|---|
| c | 10620 | 10367 | 253 |
| cpp | 17840 | 17569 | 271 |
| cpython | 1 | 1 | 0 |
| go | 590 | 577 | 13 |
| java | 2 | 2 | 0 |
| php | 4 | 4 | 0 |
| ruby | 4 | 2 | 2 |
| rust | 695 | 685 | 10 |
| swift | 1322 | 1229 | 93 |

## c

### narrow chaff -- 83 distinct single-opcode bodies

| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |
|---|---|---|---|---|
| add | `mov %esi,%eax; add %rdi,%rax; ret` | 32 | + | c/op_113 |
| add | `mov %edi,%eax; add %rsi,%rax; ret` | 32 | + | c/op_133 |
| addsd | `addsd %xmm1,%xmm0; ret` | 2 | + | c/op_130 |
| addsd | `addsd 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` | 4 | ++, -- | c/op_40 |
| addss | `addss %xmm1,%xmm0; ret` | 2 | + | c/op_123 |
| addss | `addss 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` | 4 | ++, -- | c/op_39 |
| and | `mov %edi,%eax; and %esi,%eax; ret` | 135 | &, &&, * | c/op_209 |
| and | `mov %rdi,%rax; and %rsi,%rax; ret` | 40 | & | c/op_433 |
| and | `mov %rdi,%rax; and %esi,%eax; ret` | 32 | & | c/op_437 |
| and | `mov %rsi,%rax; and %edi,%eax; ret` | 32 | & | c/op_457 |
| call | `push %rax; call 6 <op_11491+0x6> !!reloc=R_X86_64_PLT32:__divti3-0x4; pop %rcx; ret` | 1 | / | c/regen_11491 |
| call | `push %rax; call 6 <op_11492+0x6> !!reloc=R_X86_64_PLT32:__udivti3-0x4; pop %rcx; ret` | 1 | / | c/regen_11492 |
| call | `push %rax; call 6 <op_11547+0x6> !!reloc=R_X86_64_PLT32:__udivti3-0x4; pop %rcx; ret` | 1 | / | c/regen_11547 |
| call | `push %rax; call 6 <op_11548+0x6> !!reloc=R_X86_64_PLT32:__udivti3-0x4; pop %rcx; ret` | 1 | / | c/regen_11548 |
| call | `push %rax; call 6 <op_14207+0x6> !!reloc=R_X86_64_PLT32:__modti3-0x4; pop %rcx; ret` | 1 | % | c/regen_14207 |
| call | `push %rax; call 6 <op_14208+0x6> !!reloc=R_X86_64_PLT32:__umodti3-0x4; pop %rcx; ret` | 1 | % | c/regen_14208 |
| call | `push %rax; call 6 <op_14254+0x6> !!reloc=R_X86_64_PLT32:__umodti3-0x4; pop %rcx; ret` | 1 | % | c/regen_14254 |
| call | `push %rax; call 6 <op_14255+0x6> !!reloc=R_X86_64_PLT32:__umodti3-0x4; pop %rcx; ret` | 1 | % | c/regen_14255 |
| divsd | `divsd %xmm1,%xmm0; ret` | 2 | / | c/op_238 |
| divss | `divss %xmm1,%xmm0; ret` | 2 | / | c/op_231 |
| imul | `mov %edi,%eax; imul %esi,%eax; ret` | 82 | * | c/op_174 |
| imul | `mov %rdi,%rax; imul %rsi,%rax; ret` | 40 | * | c/op_181 |
| imul | `mov %esi,%eax; imul %rdi,%rax; ret` | 18 | * | c/regen_8997 |
| imul | `mov %edi,%eax; imul %rsi,%rax; ret` | 18 | * | c/regen_9822 |
| lea | `lea (%rdi,%rsi,1),%eax; ret` | 125 | + | c/op_102 |
| lea | `lea (%rdi,%rsi,1),%rax; ret` | 40 | + | c/op_109 |
| lea | `mov %edi,-0x4(%rsp); lea -0x4(%rsp),%rax; ret` | 4 | & | c/op_30 |
| lea | `mov %rdi,-0x8(%rsp); lea -0x8(%rsp),%rax; ret` | 8 | & | c/op_31 |
| lea | `movss %xmm0,-0x4(%rsp); lea -0x4(%rsp),%rax; ret` | 2 | & | c/op_33 |
| lea | `movsd %xmm0,-0x8(%rsp); lea -0x8(%rsp),%rax; ret` | 2 | & | c/op_34 |
| lea | `mov %dil,-0x1(%rsp); lea -0x1(%rsp),%rax; ret` | 6 | & | c/op_35 |
| lea | `lea 0x1(%rdi),%eax; ret` | 10 | ++ | c/op_36 |
| lea | `lea 0x1(%rdi),%rax; ret` | 8 | ++ | c/op_37 |
| lea | `lea -0x1(%rdi),%eax; ret` | 10 | -- | c/op_42 |
| lea | `lea -0x1(%rdi),%rax; ret` | 8 | -- | c/op_43 |
| lea | `movaps %xmm0,-0x18(%rsp); lea -0x18(%rsp),%rax; ret` | 1 | & | c/regen_288 |
| lea | `mov %rsi,-0x10(%rsp); mov %rdi,-0x18(%rsp); lea -0x18(%rsp),%rax; ret` | 2 | & | c/regen_291 |
| lea | `mov %di,-0x2(%rsp); lea -0x2(%rsp),%rax; ret` | 3 | & | c/regen_307 |
| mov | `mov $0x1,%al; ret` | 3 | ++ | c/op_41 |
| mov | `mov $0x4,%eax; ret` | 24 | _Alignof, __alignof, __alignof__, sizeof | c/op_48 |
| mov | `mov $0x8,%eax; ret` | 40 | _Alignof, __alignof, __alignof__, sizeof | c/op_49 |
| mov | `mov $0x1,%eax; ret` | 24 | _Alignof, __alignof, __alignof__, sizeof | c/op_53 |
| mov | `mov $0x2,%eax; ret` | 20 | _Alignof, __alignof, __alignof__, sizeof | c/regen_441 |
| mov | `mov $0x10,%eax; ret` | 16 | _Alignof, __alignof, __alignof__, sizeof | c/regen_456 |
| mulsd | `mulsd %xmm1,%xmm0; ret` | 2 | * | c/op_202 |
| mulss | `mulss %xmm1,%xmm0; ret` | 2 | * | c/op_195 |
| neg | `mov %edi,%eax; neg %eax; ret` | 13 | - | c/op_12 |
| neg | `mov %rdi,%rax; neg %rax; ret` | 8 | - | c/op_13 |
| not | `mov %edi,%eax; not %eax; ret` | 11 | ~ | c/op_11 |
| not | `mov %rdi,%rax; not %rax; ret` | 8 | ~ | c/op_7 |
| or | `mov %edi,%eax; or %esi,%eax; ret` | 130 | |, || | c/op_317 |
| or | `mov %rdi,%rax; or %rsi,%rax; ret` | 44 | | | c/op_361 |
| or | `mov %esi,%eax; or %rdi,%rax; ret` | 32 | | | c/op_365 |
| or | `mov %edi,%eax; or %rsi,%rax; ret` | 42 | | | c/op_385 |
| or | `mov %edx,%eax; or %rdi,%rax; mov %rsi,%rdx; ret` | 10 | | | c/regen_22674 |
| or | `mov %rdi,%rax; or %rdx,%rax; mov %rsi,%rdx; ret` | 4 | | | c/regen_22712 |
| sar | `mov %esi,%ecx; mov %edi,%eax; sar %cl,%eax; ret` | 68 | >> | c/op_714 |
| sar | `mov %rsi,%rcx; mov %edi,%eax; sar %cl,%eax; ret` | 50 | >> | c/op_715 |
| sar | `mov %esi,%ecx; mov %rdi,%rax; sar %cl,%rax; ret` | 46 | >> | c/op_720 |
| sar | `mov %rsi,%rcx; mov %rdi,%rax; sar %cl,%rax; ret` | 34 | >> | c/op_721 |
| shl | `mov %esi,%ecx; mov %edi,%eax; shl %cl,%eax; ret` | 125 | << | c/op_678 |
| shl | `mov %rsi,%rcx; mov %edi,%eax; shl %cl,%eax; ret` | 92 | << | c/op_679 |
| shl | `mov %esi,%ecx; mov %rdi,%rax; shl %cl,%rax; ret` | 70 | << | c/op_684 |
| shl | `mov %rsi,%rcx; mov %rdi,%rax; shl %cl,%rax; ret` | 52 | << | c/op_685 |
| shr | `mov %esi,%ecx; mov %rdi,%rax; shr %cl,%rax; ret` | 24 | >> | c/op_726 |
| shr | `mov %rsi,%rcx; mov %rdi,%rax; shr %cl,%rax; ret` | 18 | >> | c/op_727 |
| shr | `mov %esi,%ecx; mov %edi,%eax; shr %cl,%eax; ret` | 57 | >> | c/op_744 |
| shr | `mov %rsi,%rcx; mov %edi,%eax; shr %cl,%eax; ret` | 42 | >> | c/op_745 |
| sub | `mov %edi,%eax; sub %esi,%eax; ret` | 125 | - | c/op_138 |
| sub | `mov %rdi,%rax; sub %rsi,%rax; ret` | 40 | - | c/op_145 |
| sub | `mov %rdi,%rax; mov %esi,%ecx; sub %rcx,%rax; ret` | 32 | - | c/op_149 |
| sub | `mov %edi,%eax; sub %rsi,%rax; ret` | 32 | - | c/op_169 |
| subsd | `subsd %xmm1,%xmm0; ret` | 2 | - | c/op_166 |
| subss | `subss %xmm1,%xmm0; ret` | 2 | - | c/op_159 |
| xor | `xor %eax,%eax; ret` | 38 | % | c/op_251 |
| xor | `mov %edi,%eax; xor %esi,%eax; ret` | 130 | !=, ^ | c/op_390 |
| xor | `mov %rdi,%rax; xor %rsi,%rax; ret` | 44 | ^ | c/op_397 |
| xor | `mov %esi,%eax; xor %rdi,%rax; ret` | 32 | ^ | c/op_401 |
| xor | `mov %edi,%eax; xor %rsi,%rax; ret` | 42 | ^ | c/op_421 |
| xor | `mov %edi,%eax; xor $0x1,%al; ret` | 3 | -- | c/op_47 |
| xor | `mov %edx,%eax; xor %rdi,%rax; mov %rsi,%rdx; ret` | 10 | ^ | c/regen_24883 |
| xor | `mov %rdi,%rax; xor %rdx,%rax; mov %rsi,%rdx; ret` | 4 | ^ | c/regen_24921 |
| xorps | `xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` | 6 | - | c/op_15 |

### wide chaff -- 109 distinct single-opcode bodies

| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |
|---|---|---|---|---|
| add | `movslq %edi,%rax; add %rsi,%rax; ret` | 38 | + | c/op_103 |
| add | `movslq %esi,%rax; add %rdi,%rax; ret` | 38 | + | c/op_108 |
| add | `mov %esi,%eax; add %rdi,%rax; ret` | 32 | + | c/op_113 |
| add | `mov %edi,%eax; add %rsi,%rax; ret` | 32 | + | c/op_133 |
| addsd | `addsd %xmm1,%xmm0; ret` | 2 | + | c/op_130 |
| addsd | `addsd 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` | 4 | ++, -- | c/op_40 |
| addss | `addss %xmm1,%xmm0; ret` | 2 | + | c/op_123 |
| addss | `addss 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` | 4 | ++, -- | c/op_39 |
| and | `mov %edi,%eax; and %esi,%eax; ret` | 135 | &, &&, * | c/op_209 |
| and | `movslq %edi,%rax; and %rsi,%rax; ret` | 38 | & | c/op_427 |
| and | `movslq %esi,%rax; and %rdi,%rax; ret` | 38 | & | c/op_432 |
| and | `mov %rdi,%rax; and %rsi,%rax; ret` | 40 | & | c/op_433 |
| and | `mov %rdi,%rax; and %esi,%eax; ret` | 32 | & | c/op_437 |
| and | `mov %rsi,%rax; and %edi,%eax; ret` | 32 | & | c/op_457 |
| call | `push %rax; call 6 <op_11491+0x6> !!reloc=R_X86_64_PLT32:__divti3-0x4; pop %rcx; ret` | 1 | / | c/regen_11491 |
| call | `push %rax; call 6 <op_11492+0x6> !!reloc=R_X86_64_PLT32:__udivti3-0x4; pop %rcx; ret` | 1 | / | c/regen_11492 |
| call | `push %rax; call 6 <op_11547+0x6> !!reloc=R_X86_64_PLT32:__udivti3-0x4; pop %rcx; ret` | 1 | / | c/regen_11547 |
| call | `push %rax; call 6 <op_11548+0x6> !!reloc=R_X86_64_PLT32:__udivti3-0x4; pop %rcx; ret` | 1 | / | c/regen_11548 |
| call | `push %rax; call 6 <op_14207+0x6> !!reloc=R_X86_64_PLT32:__modti3-0x4; pop %rcx; ret` | 1 | % | c/regen_14207 |
| call | `push %rax; call 6 <op_14208+0x6> !!reloc=R_X86_64_PLT32:__umodti3-0x4; pop %rcx; ret` | 1 | % | c/regen_14208 |
| call | `push %rax; call 6 <op_14254+0x6> !!reloc=R_X86_64_PLT32:__umodti3-0x4; pop %rcx; ret` | 1 | % | c/regen_14254 |
| call | `push %rax; call 6 <op_14255+0x6> !!reloc=R_X86_64_PLT32:__umodti3-0x4; pop %rcx; ret` | 1 | % | c/regen_14255 |
| div | `movzbl %dil,%eax; div %sil; movzbl %al,%eax; ret` | 1 | / | c/regen_12973 |
| div | `movzbl %dil,%eax; div %sil; movzbl %ah,%eax; ret` | 1 | % | c/regen_15263 |
| divsd | `divsd %xmm1,%xmm0; ret` | 2 | / | c/op_238 |
| divss | `divss %xmm1,%xmm0; ret` | 2 | / | c/op_231 |
| idiv | `mov %edi,%eax; cltd; idiv %esi; ret` | 49 | / | c/op_210 |
| idiv | `movslq %edi,%rax; cqto; idiv %rsi; ret` | 25 | / | c/op_211 |
| idiv | `mov %rdi,%rax; movslq %esi,%rcx; cqto; idiv %rcx; ret` | 25 | / | c/op_216 |
| idiv | `mov %rdi,%rax; cqto; idiv %rsi; ret` | 17 | / | c/op_217 |
| idiv | `mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret` | 49 | % | c/op_246 |
| idiv | `movslq %edi,%rax; cqto; idiv %rsi; mov %rdx,%rax; ret` | 25 | % | c/op_247 |
| idiv | `mov %rdi,%rax; movslq %esi,%rcx; cqto; idiv %rcx; mov %rdx,%rax; ret` | 25 | % | c/op_252 |
| idiv | `mov %rdi,%rax; cqto; idiv %rsi; mov %rdx,%rax; ret` | 17 | % | c/op_253 |
| idiv | `mov %rdi,%rax; mov %esi,%ecx; cqto; idiv %rcx; ret` | 12 | / | c/regen_12133 |
| idiv | `mov %rdi,%rax; mov %esi,%ecx; cqto; idiv %rcx; mov %rdx,%rax; ret` | 12 | % | c/regen_14605 |
| imul | `mov %edi,%eax; imul %esi,%eax; ret` | 82 | * | c/op_174 |
| imul | `movslq %edi,%rax; imul %rsi,%rax; ret` | 38 | * | c/op_175 |
| imul | `movslq %esi,%rax; imul %rdi,%rax; ret` | 38 | * | c/op_180 |
| imul | `mov %rdi,%rax; imul %rsi,%rax; ret` | 40 | * | c/op_181 |
| imul | `mov %esi,%eax; imul %rdi,%rax; ret` | 18 | * | c/regen_8997 |
| imul | `mov %edi,%eax; imul %rsi,%rax; ret` | 18 | * | c/regen_9822 |
| lea | `lea (%rdi,%rsi,1),%eax; ret` | 125 | + | c/op_102 |
| lea | `lea (%rdi,%rsi,1),%rax; ret` | 40 | + | c/op_109 |
| lea | `mov %edi,-0x4(%rsp); lea -0x4(%rsp),%rax; ret` | 4 | & | c/op_30 |
| lea | `mov %rdi,-0x8(%rsp); lea -0x8(%rsp),%rax; ret` | 8 | & | c/op_31 |
| lea | `movss %xmm0,-0x4(%rsp); lea -0x4(%rsp),%rax; ret` | 2 | & | c/op_33 |
| lea | `movsd %xmm0,-0x8(%rsp); lea -0x8(%rsp),%rax; ret` | 2 | & | c/op_34 |
| lea | `mov %dil,-0x1(%rsp); lea -0x1(%rsp),%rax; ret` | 6 | & | c/op_35 |
| lea | `lea 0x1(%rdi),%eax; ret` | 10 | ++ | c/op_36 |
| lea | `lea 0x1(%rdi),%rax; ret` | 8 | ++ | c/op_37 |
| lea | `lea -0x1(%rdi),%eax; ret` | 10 | -- | c/op_42 |
| lea | `lea -0x1(%rdi),%rax; ret` | 8 | -- | c/op_43 |
| lea | `movaps %xmm0,-0x18(%rsp); lea -0x18(%rsp),%rax; ret` | 1 | & | c/regen_288 |
| lea | `mov %rsi,-0x10(%rsp); mov %rdi,-0x18(%rsp); lea -0x18(%rsp),%rax; ret` | 2 | & | c/regen_291 |
| lea | `mov %di,-0x2(%rsp); lea -0x2(%rsp),%rax; ret` | 3 | & | c/regen_307 |
| mov | `mov $0x1,%al; ret` | 3 | ++ | c/op_41 |
| mov | `mov $0x4,%eax; ret` | 24 | _Alignof, __alignof, __alignof__, sizeof | c/op_48 |
| mov | `mov $0x8,%eax; ret` | 40 | _Alignof, __alignof, __alignof__, sizeof | c/op_49 |
| mov | `mov $0x1,%eax; ret` | 24 | _Alignof, __alignof, __alignof__, sizeof | c/op_53 |
| mov | `mov $0x2,%eax; ret` | 20 | _Alignof, __alignof, __alignof__, sizeof | c/regen_441 |
| mov | `mov $0x10,%eax; ret` | 16 | _Alignof, __alignof, __alignof__, sizeof | c/regen_456 |
| mulsd | `mulsd %xmm1,%xmm0; ret` | 2 | * | c/op_202 |
| mulss | `mulss %xmm1,%xmm0; ret` | 2 | * | c/op_195 |
| neg | `mov %edi,%eax; neg %eax; ret` | 13 | - | c/op_12 |
| neg | `mov %rdi,%rax; neg %rax; ret` | 8 | - | c/op_13 |
| not | `mov %edi,%eax; not %eax; ret` | 11 | ~ | c/op_11 |
| not | `mov %rdi,%rax; not %rax; ret` | 8 | ~ | c/op_7 |
| not | `not %dil; movsbl %dil,%eax; ret` | 2 | ~ | c/regen_74 |
| or | `mov %edi,%eax; or %esi,%eax; ret` | 130 | |, || | c/op_317 |
| or | `movslq %edi,%rax; or %rsi,%rax; ret` | 38 | | | c/op_355 |
| or | `movslq %esi,%rax; or %rdi,%rax; ret` | 38 | | | c/op_360 |
| or | `mov %rdi,%rax; or %rsi,%rax; ret` | 44 | | | c/op_361 |
| or | `mov %esi,%eax; or %rdi,%rax; ret` | 32 | | | c/op_365 |
| or | `mov %edi,%eax; or %rsi,%rax; ret` | 42 | | | c/op_385 |
| or | `mov %edx,%eax; or %rdi,%rax; mov %rsi,%rdx; ret` | 10 | | | c/regen_22674 |
| or | `mov %rdi,%rax; or %rdx,%rax; mov %rsi,%rdx; ret` | 4 | | | c/regen_22712 |
| sar | `mov %esi,%ecx; mov %edi,%eax; sar %cl,%eax; ret` | 68 | >> | c/op_714 |
| sar | `mov %rsi,%rcx; mov %edi,%eax; sar %cl,%eax; ret` | 50 | >> | c/op_715 |
| sar | `mov %esi,%ecx; mov %rdi,%rax; sar %cl,%rax; ret` | 46 | >> | c/op_720 |
| sar | `mov %rsi,%rcx; mov %rdi,%rax; sar %cl,%rax; ret` | 34 | >> | c/op_721 |
| shl | `mov %esi,%ecx; mov %edi,%eax; shl %cl,%eax; ret` | 125 | << | c/op_678 |
| shl | `mov %rsi,%rcx; mov %edi,%eax; shl %cl,%eax; ret` | 92 | << | c/op_679 |
| shl | `mov %esi,%ecx; mov %rdi,%rax; shl %cl,%rax; ret` | 70 | << | c/op_684 |
| shl | `mov %rsi,%rcx; mov %rdi,%rax; shl %cl,%rax; ret` | 52 | << | c/op_685 |
| shr | `mov %esi,%ecx; mov %rdi,%rax; shr %cl,%rax; ret` | 24 | >> | c/op_726 |
| shr | `mov %rsi,%rcx; mov %rdi,%rax; shr %cl,%rax; ret` | 18 | >> | c/op_727 |
| shr | `mov %esi,%ecx; mov %edi,%eax; shr %cl,%eax; ret` | 57 | >> | c/op_744 |
| shr | `mov %rsi,%rcx; mov %edi,%eax; shr %cl,%eax; ret` | 42 | >> | c/op_745 |
| sub | `mov %edi,%eax; sub %esi,%eax; ret` | 125 | - | c/op_138 |
| sub | `movslq %edi,%rax; sub %rsi,%rax; ret` | 38 | - | c/op_139 |
| sub | `mov %rdi,%rax; movslq %esi,%rcx; sub %rcx,%rax; ret` | 38 | - | c/op_144 |
| sub | `mov %rdi,%rax; sub %rsi,%rax; ret` | 40 | - | c/op_145 |
| sub | `mov %rdi,%rax; mov %esi,%ecx; sub %rcx,%rax; ret` | 32 | - | c/op_149 |
| sub | `mov %edi,%eax; sub %rsi,%rax; ret` | 32 | - | c/op_169 |
| subsd | `subsd %xmm1,%xmm0; ret` | 2 | - | c/op_166 |
| subss | `subss %xmm1,%xmm0; ret` | 2 | - | c/op_159 |
| xor | `xor %eax,%eax; ret` | 38 | % | c/op_251 |
| xor | `mov %edi,%eax; xor %esi,%eax; ret` | 130 | !=, ^ | c/op_390 |
| xor | `movslq %edi,%rax; xor %rsi,%rax; ret` | 38 | ^ | c/op_391 |
| xor | `movslq %esi,%rax; xor %rdi,%rax; ret` | 38 | ^ | c/op_396 |
| xor | `mov %rdi,%rax; xor %rsi,%rax; ret` | 44 | ^ | c/op_397 |
| xor | `mov %esi,%eax; xor %rdi,%rax; ret` | 32 | ^ | c/op_401 |
| xor | `mov %edi,%eax; xor %rsi,%rax; ret` | 42 | ^ | c/op_421 |
| xor | `mov %edi,%eax; xor $0x1,%al; ret` | 3 | -- | c/op_47 |
| xor | `xor $0x1,%dil; movzbl %dil,%eax; ret` | 3 | ! | c/op_5 |
| xor | `mov %edx,%eax; xor %rdi,%rax; mov %rsi,%rdx; ret` | 10 | ^ | c/regen_24883 |
| xor | `mov %rdi,%rax; xor %rdx,%rax; mov %rsi,%rdx; ret` | 4 | ^ | c/regen_24921 |
| xorps | `xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` | 6 | - | c/op_15 |

#### zero-opcode units (pure move, chaff-stripped body is empty)
- narrow: 3 example(s) shown of the histogram's n=0 count
  - `c/op_100` operator `--`: `ret`
  - `c/op_101` operator `--`: `mov %edi,%eax; ret`
  - `c/op_18` operator `+`: `mov %edi,%eax; ret`
- wide: 3 example(s) shown of the histogram's n=0 count
  - `c/op_100` operator `--`: `ret`
  - `c/op_101` operator `--`: `mov %edi,%eax; ret`
  - `c/op_18` operator `+`: `mov %edi,%eax; ret`

## cpp

### narrow chaff -- 82 distinct single-opcode bodies

| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |
|---|---|---|---|---|
| add | `mov %esi,%eax; add %rdi,%rax; ret` | 44 | + | cpp/op_113 |
| add | `mov %edi,%eax; add %rsi,%rax; ret` | 44 | + | cpp/op_133 |
| addsd | `addsd %xmm1,%xmm0; ret` | 2 | + | cpp/op_130 |
| addsd | `addsd 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` | 4 | ++, -- | cpp/op_52 |
| addss | `addss %xmm1,%xmm0; ret` | 2 | + | cpp/op_123 |
| addss | `addss 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` | 4 | ++, -- | cpp/op_51 |
| and | `mov %edi,%eax; and %esi,%eax; ret` | 406 | &, &&, *, and, bitand | cpp/op_209 |
| and | `mov %rdi,%rax; and %rsi,%rax; ret` | 80 | &, bitand | cpp/op_433 |
| and | `mov %rdi,%rax; and %esi,%eax; ret` | 88 | &, bitand | cpp/op_437 |
| and | `mov %rsi,%rax; and %edi,%eax; ret` | 88 | &, bitand | cpp/op_457 |
| call | `push %rax; call 6 <op_11482+0x6> !!reloc=R_X86_64_PLT32:__divti3-0x4; pop %rcx; ret` | 1 | / | cpp/regen_11482 |
| call | `push %rax; call 6 <op_11483+0x6> !!reloc=R_X86_64_PLT32:__udivti3-0x4; pop %rcx; ret` | 1 | / | cpp/regen_11483 |
| call | `push %rax; call 6 <op_11538+0x6> !!reloc=R_X86_64_PLT32:__udivti3-0x4; pop %rcx; ret` | 1 | / | cpp/regen_11538 |
| call | `push %rax; call 6 <op_11539+0x6> !!reloc=R_X86_64_PLT32:__udivti3-0x4; pop %rcx; ret` | 1 | / | cpp/regen_11539 |
| call | `push %rax; call 6 <op_14198+0x6> !!reloc=R_X86_64_PLT32:__modti3-0x4; pop %rcx; ret` | 1 | % | cpp/regen_14198 |
| call | `push %rax; call 6 <op_14199+0x6> !!reloc=R_X86_64_PLT32:__umodti3-0x4; pop %rcx; ret` | 1 | % | cpp/regen_14199 |
| call | `push %rax; call 6 <op_14245+0x6> !!reloc=R_X86_64_PLT32:__umodti3-0x4; pop %rcx; ret` | 1 | % | cpp/regen_14245 |
| call | `push %rax; call 6 <op_14246+0x6> !!reloc=R_X86_64_PLT32:__umodti3-0x4; pop %rcx; ret` | 1 | % | cpp/regen_14246 |
| divsd | `divsd %xmm1,%xmm0; ret` | 2 | / | cpp/op_238 |
| divss | `divss %xmm1,%xmm0; ret` | 2 | / | cpp/op_231 |
| imul | `mov %edi,%eax; imul %esi,%eax; ret` | 170 | * | cpp/op_174 |
| imul | `mov %rdi,%rax; imul %rsi,%rax; ret` | 40 | * | cpp/op_181 |
| imul | `mov %edi,%eax; imul %rsi,%rax; ret` | 36 | * | cpp/regen_8581 |
| imul | `mov %esi,%eax; imul %rdi,%rax; ret` | 36 | * | cpp/regen_8966 |
| lea | `lea (%rdi,%rsi,1),%eax; ret` | 200 | + | cpp/op_102 |
| lea | `lea (%rdi,%rsi,1),%rax; ret` | 40 | + | cpp/op_109 |
| lea | `mov %edi,-0x4(%rsp); lea -0x4(%rsp),%rax; ret` | 6 | & | cpp/op_42 |
| lea | `mov %rdi,-0x8(%rsp); lea -0x8(%rsp),%rax; ret` | 8 | & | cpp/op_43 |
| lea | `movss %xmm0,-0x4(%rsp); lea -0x4(%rsp),%rax; ret` | 2 | & | cpp/op_45 |
| lea | `movsd %xmm0,-0x8(%rsp); lea -0x8(%rsp),%rax; ret` | 2 | & | cpp/op_46 |
| lea | `mov %dil,-0x1(%rsp); lea -0x1(%rsp),%rax; ret` | 6 | & | cpp/op_47 |
| lea | `lea 0x1(%rdi),%eax; ret` | 14 | ++ | cpp/op_48 |
| lea | `lea 0x1(%rdi),%rax; ret` | 8 | ++ | cpp/op_49 |
| lea | `lea -0x1(%rdi),%eax; ret` | 14 | -- | cpp/op_54 |
| lea | `lea -0x1(%rdi),%rax; ret` | 8 | -- | cpp/op_55 |
| lea | `movaps %xmm0,-0x18(%rsp); lea -0x18(%rsp),%rax; ret` | 1 | & | cpp/regen_391 |
| lea | `mov %rsi,-0x10(%rsp); mov %rdi,-0x18(%rsp); lea -0x18(%rsp),%rax; ret` | 2 | & | cpp/regen_394 |
| lea | `mov %di,-0x2(%rsp); lea -0x2(%rsp),%rax; ret` | 4 | & | cpp/regen_398 |
| mov | `mov $0x4,%eax; ret` | 8 | sizeof | cpp/op_60 |
| mov | `mov $0x8,%eax; ret` | 10 | sizeof | cpp/op_61 |
| mov | `mov $0x1,%eax; ret` | 6 | sizeof | cpp/op_65 |
| mov | `mov $0x2,%eax; ret` | 6 | sizeof | cpp/regen_544 |
| mov | `mov $0x10,%eax; ret` | 4 | sizeof | cpp/regen_559 |
| mulsd | `mulsd %xmm1,%xmm0; ret` | 2 | * | cpp/op_202 |
| mulss | `mulss %xmm1,%xmm0; ret` | 2 | * | cpp/op_195 |
| neg | `mov %edi,%eax; neg %eax; ret` | 16 | - | cpp/op_12 |
| neg | `mov %rdi,%rax; neg %rax; ret` | 8 | - | cpp/op_13 |
| not | `mov %edi,%eax; not %eax; ret` | 28 | compl, ~ | cpp/op_11 |
| not | `mov %rdi,%rax; not %rax; ret` | 16 | compl, ~ | cpp/op_31 |
| or | `mov %edi,%eax; or %esi,%eax; ret` | 404 | bitor, or, |, || | cpp/op_317 |
| or | `mov %rdi,%rax; or %rsi,%rax; ret` | 88 | bitor, | | cpp/op_361 |
| or | `mov %esi,%eax; or %rdi,%rax; ret` | 88 | bitor, | | cpp/op_365 |
| or | `mov %edi,%eax; or %rsi,%rax; ret` | 116 | bitor, | | cpp/op_385 |
| or | `mov %edx,%eax; or %rdi,%rax; mov %rsi,%rdx; ret` | 28 | bitor, | | cpp/regen_22681 |
| or | `mov %rdi,%rax; or %rdx,%rax; mov %rsi,%rdx; ret` | 8 | bitor, | | cpp/regen_22703 |
| sar | `mov %esi,%ecx; mov %edi,%eax; sar %cl,%eax; ret` | 100 | >> | cpp/op_714 |
| sar | `mov %rsi,%rcx; mov %edi,%eax; sar %cl,%eax; ret` | 58 | >> | cpp/op_715 |
| sar | `mov %esi,%ecx; mov %rdi,%rax; sar %cl,%rax; ret` | 58 | >> | cpp/op_720 |
| sar | `mov %rsi,%rcx; mov %rdi,%rax; sar %cl,%rax; ret` | 34 | >> | cpp/op_721 |
| shl | `mov %esi,%ecx; mov %edi,%eax; shl %cl,%eax; ret` | 200 | << | cpp/op_678 |
| shl | `mov %rsi,%rcx; mov %edi,%eax; shl %cl,%eax; ret` | 116 | << | cpp/op_679 |
| shl | `mov %esi,%ecx; mov %rdi,%rax; shl %cl,%rax; ret` | 88 | << | cpp/op_684 |
| shl | `mov %rsi,%rcx; mov %rdi,%rax; shl %cl,%rax; ret` | 52 | << | cpp/op_685 |
| shr | `mov %esi,%ecx; mov %rdi,%rax; shr %cl,%rax; ret` | 30 | >> | cpp/op_726 |
| shr | `mov %rsi,%rcx; mov %rdi,%rax; shr %cl,%rax; ret` | 18 | >> | cpp/op_727 |
| shr | `mov %esi,%ecx; mov %edi,%eax; shr %cl,%eax; ret` | 100 | >> | cpp/op_744 |
| shr | `mov %rsi,%rcx; mov %edi,%eax; shr %cl,%eax; ret` | 58 | >> | cpp/op_745 |
| sub | `mov %edi,%eax; sub %esi,%eax; ret` | 200 | - | cpp/op_138 |
| sub | `mov %rdi,%rax; sub %rsi,%rax; ret` | 40 | - | cpp/op_145 |
| sub | `mov %rdi,%rax; mov %esi,%ecx; sub %rcx,%rax; ret` | 44 | - | cpp/op_149 |
| sub | `mov %edi,%eax; sub %rsi,%rax; ret` | 44 | - | cpp/op_169 |
| subsd | `subsd %xmm1,%xmm0; ret` | 2 | - | cpp/op_166 |
| subss | `subss %xmm1,%xmm0; ret` | 2 | - | cpp/op_159 |
| xor | `mov %edi,%eax; xor %esi,%eax; ret` | 404 | !=, ^, not_eq, xor | cpp/op_1001 |
| xor | `xor %eax,%eax; ret` | 24 | % | cpp/op_251 |
| xor | `mov %edi,%eax; xor $0x1,%al; ret` | 4 | !, not | cpp/op_29 |
| xor | `mov %rdi,%rax; xor %rsi,%rax; ret` | 88 | ^, xor | cpp/op_397 |
| xor | `mov %esi,%eax; xor %rdi,%rax; ret` | 88 | ^, xor | cpp/op_401 |
| xor | `mov %edi,%eax; xor %rsi,%rax; ret` | 116 | ^, xor | cpp/op_421 |
| xor | `mov %edx,%eax; xor %rdi,%rax; mov %rsi,%rdx; ret` | 28 | ^, xor | cpp/regen_24890 |
| xor | `mov %rdi,%rax; xor %rdx,%rax; mov %rsi,%rdx; ret` | 8 | ^, xor | cpp/regen_24912 |
| xorps | `xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` | 6 | - | cpp/op_15 |

### wide chaff -- 107 distinct single-opcode bodies

| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |
|---|---|---|---|---|
| add | `movslq %edi,%rax; add %rsi,%rax; ret` | 44 | + | cpp/op_103 |
| add | `movslq %esi,%rax; add %rdi,%rax; ret` | 44 | + | cpp/op_108 |
| add | `mov %esi,%eax; add %rdi,%rax; ret` | 44 | + | cpp/op_113 |
| add | `mov %edi,%eax; add %rsi,%rax; ret` | 44 | + | cpp/op_133 |
| addsd | `addsd %xmm1,%xmm0; ret` | 2 | + | cpp/op_130 |
| addsd | `addsd 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` | 4 | ++, -- | cpp/op_52 |
| addss | `addss %xmm1,%xmm0; ret` | 2 | + | cpp/op_123 |
| addss | `addss 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` | 4 | ++, -- | cpp/op_51 |
| and | `mov %edi,%eax; and %esi,%eax; ret` | 406 | &, &&, *, and, bitand | cpp/op_209 |
| and | `movslq %edi,%rax; and %rsi,%rax; ret` | 88 | &, bitand | cpp/op_427 |
| and | `movslq %esi,%rax; and %rdi,%rax; ret` | 88 | &, bitand | cpp/op_432 |
| and | `mov %rdi,%rax; and %rsi,%rax; ret` | 80 | &, bitand | cpp/op_433 |
| and | `mov %rdi,%rax; and %esi,%eax; ret` | 88 | &, bitand | cpp/op_437 |
| and | `mov %rsi,%rax; and %edi,%eax; ret` | 88 | &, bitand | cpp/op_457 |
| call | `push %rax; call 6 <op_11482+0x6> !!reloc=R_X86_64_PLT32:__divti3-0x4; pop %rcx; ret` | 1 | / | cpp/regen_11482 |
| call | `push %rax; call 6 <op_11483+0x6> !!reloc=R_X86_64_PLT32:__udivti3-0x4; pop %rcx; ret` | 1 | / | cpp/regen_11483 |
| call | `push %rax; call 6 <op_11538+0x6> !!reloc=R_X86_64_PLT32:__udivti3-0x4; pop %rcx; ret` | 1 | / | cpp/regen_11538 |
| call | `push %rax; call 6 <op_11539+0x6> !!reloc=R_X86_64_PLT32:__udivti3-0x4; pop %rcx; ret` | 1 | / | cpp/regen_11539 |
| call | `push %rax; call 6 <op_14198+0x6> !!reloc=R_X86_64_PLT32:__modti3-0x4; pop %rcx; ret` | 1 | % | cpp/regen_14198 |
| call | `push %rax; call 6 <op_14199+0x6> !!reloc=R_X86_64_PLT32:__umodti3-0x4; pop %rcx; ret` | 1 | % | cpp/regen_14199 |
| call | `push %rax; call 6 <op_14245+0x6> !!reloc=R_X86_64_PLT32:__umodti3-0x4; pop %rcx; ret` | 1 | % | cpp/regen_14245 |
| call | `push %rax; call 6 <op_14246+0x6> !!reloc=R_X86_64_PLT32:__umodti3-0x4; pop %rcx; ret` | 1 | % | cpp/regen_14246 |
| div | `movzbl %dil,%eax; div %sil; movzbl %al,%eax; ret` | 4 | / | cpp/regen_11824 |
| div | `movzbl %dil,%eax; div %sil; movzbl %ah,%eax; ret` | 4 | % | cpp/regen_14486 |
| divsd | `divsd %xmm1,%xmm0; ret` | 2 | / | cpp/op_238 |
| divss | `divss %xmm1,%xmm0; ret` | 2 | / | cpp/op_231 |
| idiv | `mov %edi,%eax; cltd; idiv %esi; ret` | 78 | / | cpp/op_210 |
| idiv | `movslq %edi,%rax; cqto; idiv %rsi; ret` | 29 | / | cpp/op_211 |
| idiv | `mov %rdi,%rax; movslq %esi,%rcx; cqto; idiv %rcx; ret` | 29 | / | cpp/op_216 |
| idiv | `mov %rdi,%rax; cqto; idiv %rsi; ret` | 17 | / | cpp/op_217 |
| idiv | `mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret` | 78 | % | cpp/op_246 |
| idiv | `movslq %edi,%rax; cqto; idiv %rsi; mov %rdx,%rax; ret` | 29 | % | cpp/op_247 |
| idiv | `mov %rdi,%rax; movslq %esi,%rcx; cqto; idiv %rcx; mov %rdx,%rax; ret` | 29 | % | cpp/op_252 |
| idiv | `mov %rdi,%rax; cqto; idiv %rsi; mov %rdx,%rax; ret` | 17 | % | cpp/op_253 |
| idiv | `mov %rdi,%rax; mov %esi,%ecx; cqto; idiv %rcx; ret` | 24 | / | cpp/regen_12102 |
| idiv | `mov %rdi,%rax; mov %esi,%ecx; cqto; idiv %rcx; mov %rdx,%rax; ret` | 24 | % | cpp/regen_14578 |
| imul | `mov %edi,%eax; imul %esi,%eax; ret` | 170 | * | cpp/op_174 |
| imul | `movslq %edi,%rax; imul %rsi,%rax; ret` | 44 | * | cpp/op_175 |
| imul | `movslq %esi,%rax; imul %rdi,%rax; ret` | 44 | * | cpp/op_180 |
| imul | `mov %rdi,%rax; imul %rsi,%rax; ret` | 40 | * | cpp/op_181 |
| imul | `mov %edi,%eax; imul %rsi,%rax; ret` | 36 | * | cpp/regen_8581 |
| imul | `mov %esi,%eax; imul %rdi,%rax; ret` | 36 | * | cpp/regen_8966 |
| lea | `lea (%rdi,%rsi,1),%eax; ret` | 200 | + | cpp/op_102 |
| lea | `lea (%rdi,%rsi,1),%rax; ret` | 40 | + | cpp/op_109 |
| lea | `mov %edi,-0x4(%rsp); lea -0x4(%rsp),%rax; ret` | 6 | & | cpp/op_42 |
| lea | `mov %rdi,-0x8(%rsp); lea -0x8(%rsp),%rax; ret` | 8 | & | cpp/op_43 |
| lea | `movss %xmm0,-0x4(%rsp); lea -0x4(%rsp),%rax; ret` | 2 | & | cpp/op_45 |
| lea | `movsd %xmm0,-0x8(%rsp); lea -0x8(%rsp),%rax; ret` | 2 | & | cpp/op_46 |
| lea | `mov %dil,-0x1(%rsp); lea -0x1(%rsp),%rax; ret` | 6 | & | cpp/op_47 |
| lea | `lea 0x1(%rdi),%eax; ret` | 14 | ++ | cpp/op_48 |
| lea | `lea 0x1(%rdi),%rax; ret` | 8 | ++ | cpp/op_49 |
| lea | `lea -0x1(%rdi),%eax; ret` | 14 | -- | cpp/op_54 |
| lea | `lea -0x1(%rdi),%rax; ret` | 8 | -- | cpp/op_55 |
| lea | `movaps %xmm0,-0x18(%rsp); lea -0x18(%rsp),%rax; ret` | 1 | & | cpp/regen_391 |
| lea | `mov %rsi,-0x10(%rsp); mov %rdi,-0x18(%rsp); lea -0x18(%rsp),%rax; ret` | 2 | & | cpp/regen_394 |
| lea | `mov %di,-0x2(%rsp); lea -0x2(%rsp),%rax; ret` | 4 | & | cpp/regen_398 |
| mov | `mov $0x4,%eax; ret` | 8 | sizeof | cpp/op_60 |
| mov | `mov $0x8,%eax; ret` | 10 | sizeof | cpp/op_61 |
| mov | `mov $0x1,%eax; ret` | 6 | sizeof | cpp/op_65 |
| mov | `mov $0x2,%eax; ret` | 6 | sizeof | cpp/regen_544 |
| mov | `mov $0x10,%eax; ret` | 4 | sizeof | cpp/regen_559 |
| mulsd | `mulsd %xmm1,%xmm0; ret` | 2 | * | cpp/op_202 |
| mulss | `mulss %xmm1,%xmm0; ret` | 2 | * | cpp/op_195 |
| neg | `mov %edi,%eax; neg %eax; ret` | 16 | - | cpp/op_12 |
| neg | `mov %rdi,%rax; neg %rax; ret` | 8 | - | cpp/op_13 |
| not | `mov %edi,%eax; not %eax; ret` | 28 | compl, ~ | cpp/op_11 |
| not | `mov %rdi,%rax; not %rax; ret` | 16 | compl, ~ | cpp/op_31 |
| not | `not %dil; movsbl %dil,%eax; ret` | 4 | compl, ~ | cpp/regen_289 |
| or | `mov %edi,%eax; or %esi,%eax; ret` | 404 | bitor, or, |, || | cpp/op_317 |
| or | `movslq %edi,%rax; or %rsi,%rax; ret` | 88 | bitor, | | cpp/op_355 |
| or | `movslq %esi,%rax; or %rdi,%rax; ret` | 88 | bitor, | | cpp/op_360 |
| or | `mov %rdi,%rax; or %rsi,%rax; ret` | 88 | bitor, | | cpp/op_361 |
| or | `mov %esi,%eax; or %rdi,%rax; ret` | 88 | bitor, | | cpp/op_365 |
| or | `mov %edi,%eax; or %rsi,%rax; ret` | 116 | bitor, | | cpp/op_385 |
| or | `mov %edx,%eax; or %rdi,%rax; mov %rsi,%rdx; ret` | 28 | bitor, | | cpp/regen_22681 |
| or | `mov %rdi,%rax; or %rdx,%rax; mov %rsi,%rdx; ret` | 8 | bitor, | | cpp/regen_22703 |
| sar | `mov %esi,%ecx; mov %edi,%eax; sar %cl,%eax; ret` | 100 | >> | cpp/op_714 |
| sar | `mov %rsi,%rcx; mov %edi,%eax; sar %cl,%eax; ret` | 58 | >> | cpp/op_715 |
| sar | `mov %esi,%ecx; mov %rdi,%rax; sar %cl,%rax; ret` | 58 | >> | cpp/op_720 |
| sar | `mov %rsi,%rcx; mov %rdi,%rax; sar %cl,%rax; ret` | 34 | >> | cpp/op_721 |
| shl | `mov %esi,%ecx; mov %edi,%eax; shl %cl,%eax; ret` | 200 | << | cpp/op_678 |
| shl | `mov %rsi,%rcx; mov %edi,%eax; shl %cl,%eax; ret` | 116 | << | cpp/op_679 |
| shl | `mov %esi,%ecx; mov %rdi,%rax; shl %cl,%rax; ret` | 88 | << | cpp/op_684 |
| shl | `mov %rsi,%rcx; mov %rdi,%rax; shl %cl,%rax; ret` | 52 | << | cpp/op_685 |
| shr | `mov %esi,%ecx; mov %rdi,%rax; shr %cl,%rax; ret` | 30 | >> | cpp/op_726 |
| shr | `mov %rsi,%rcx; mov %rdi,%rax; shr %cl,%rax; ret` | 18 | >> | cpp/op_727 |
| shr | `mov %esi,%ecx; mov %edi,%eax; shr %cl,%eax; ret` | 100 | >> | cpp/op_744 |
| shr | `mov %rsi,%rcx; mov %edi,%eax; shr %cl,%eax; ret` | 58 | >> | cpp/op_745 |
| sub | `mov %edi,%eax; sub %esi,%eax; ret` | 200 | - | cpp/op_138 |
| sub | `movslq %edi,%rax; sub %rsi,%rax; ret` | 44 | - | cpp/op_139 |
| sub | `mov %rdi,%rax; movslq %esi,%rcx; sub %rcx,%rax; ret` | 44 | - | cpp/op_144 |
| sub | `mov %rdi,%rax; sub %rsi,%rax; ret` | 40 | - | cpp/op_145 |
| sub | `mov %rdi,%rax; mov %esi,%ecx; sub %rcx,%rax; ret` | 44 | - | cpp/op_149 |
| sub | `mov %edi,%eax; sub %rsi,%rax; ret` | 44 | - | cpp/op_169 |
| subsd | `subsd %xmm1,%xmm0; ret` | 2 | - | cpp/op_166 |
| subss | `subss %xmm1,%xmm0; ret` | 2 | - | cpp/op_159 |
| xor | `mov %edi,%eax; xor %esi,%eax; ret` | 404 | !=, ^, not_eq, xor | cpp/op_1001 |
| xor | `xor %eax,%eax; ret` | 24 | % | cpp/op_251 |
| xor | `mov %edi,%eax; xor $0x1,%al; ret` | 4 | !, not | cpp/op_29 |
| xor | `movslq %edi,%rax; xor %rsi,%rax; ret` | 88 | ^, xor | cpp/op_391 |
| xor | `movslq %esi,%rax; xor %rdi,%rax; ret` | 88 | ^, xor | cpp/op_396 |
| xor | `mov %rdi,%rax; xor %rsi,%rax; ret` | 88 | ^, xor | cpp/op_397 |
| xor | `mov %esi,%eax; xor %rdi,%rax; ret` | 88 | ^, xor | cpp/op_401 |
| xor | `mov %edi,%eax; xor %rsi,%rax; ret` | 116 | ^, xor | cpp/op_421 |
| xor | `mov %edx,%eax; xor %rdi,%rax; mov %rsi,%rdx; ret` | 28 | ^, xor | cpp/regen_24890 |
| xor | `mov %rdi,%rax; xor %rdx,%rax; mov %rsi,%rdx; ret` | 8 | ^, xor | cpp/regen_24912 |
| xorps | `xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` | 6 | - | cpp/op_15 |

#### zero-opcode units (pure move, chaff-stripped body is empty)
- narrow: 3 example(s) shown of the histogram's n=0 count
  - `cpp/op_18` operator `+`: `mov %edi,%eax; ret`
  - `cpp/op_19` operator `+`: `mov %rdi,%rax; ret`
  - `cpp/op_20` operator `+`: `mov %rdi,%rax; ret`
- wide: 3 example(s) shown of the histogram's n=0 count
  - `cpp/op_18` operator `+`: `mov %edi,%eax; ret`
  - `cpp/op_19` operator `+`: `mov %rdi,%rax; ret`
  - `cpp/op_20` operator `+`: `mov %rdi,%rax; ret`

## cpython

### narrow chaff -- 1 distinct single-opcode bodies

| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |
|---|---|---|---|---|
| add | `mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret` | 1 | + | cpython/long_add_fastpath |

### wide chaff -- 1 distinct single-opcode bodies

| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |
|---|---|---|---|---|
| add | `mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret` | 1 | + | cpython/long_add_fastpath |

#### zero-opcode units (pure move, chaff-stripped body is empty)
- narrow: 0 example(s) shown of the histogram's n=0 count
- wide: 0 example(s) shown of the histogram's n=0 count

## go

### narrow chaff -- 27 distinct single-opcode bodies

| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |
|---|---|---|---|---|
| add | `add %ebx,%eax; ret` | 7 | + | go/op_312 |
| add | `add %rbx,%rax; ret` | 7 | + | go/op_319 |
| addsd | `addsd %xmm1,%xmm0; ret` | 2 | + | go/op_340 |
| addss | `addss %xmm1,%xmm0; ret` | 2 | + | go/op_333 |
| and | `and %ebx,%eax; ret` | 9 | &, && | go/op_240 |
| and | `and %rbx,%rax; ret` | 7 | & | go/op_247 |
| divsd | `divsd %xmm1,%xmm0; ret` | 2 | / | go/op_124 |
| divss | `divss %xmm1,%xmm0; ret` | 2 | / | go/op_117 |
| imul | `imul %ebx,%eax; ret` | 7 | * | go/op_60 |
| imul | `imul %rbx,%rax; ret` | 7 | * | go/op_67 |
| mulsd | `mulsd %xmm1,%xmm0; ret` | 2 | * | go/op_88 |
| mulss | `mulss %xmm1,%xmm0; ret` | 2 | * | go/op_81 |
| neg | `neg %eax; ret` | 7 | - | go/op_6 |
| neg | `neg %rax; ret` | 7 | - | go/op_7 |
| not | `not %eax; ret` | 7 | ^ | go/op_18 |
| not | `not %rax; ret` | 7 | ^ | go/op_19 |
| or | `or %ebx,%eax; ret` | 9 | |, || | go/op_384 |
| or | `or %rbx,%rax; ret` | 7 | | | go/op_391 |
| pxor | `movsd 0x1d5c0(%rip),%xmm1; pxor %xmm1,%xmm0; ret` | 2 | - | go/op_10 |
| pxor | `movss 0x1d5dc(%rip),%xmm1; pxor %xmm1,%xmm0; ret` | 2 | - | go/op_9 |
| sub | `sub %ebx,%eax; ret` | 7 | - | go/op_348 |
| sub | `sub %rbx,%rax; ret` | 7 | - | go/op_355 |
| subsd | `subsd %xmm1,%xmm0; ret` | 2 | - | go/op_376 |
| subss | `subss %xmm1,%xmm0; ret` | 2 | - | go/op_369 |
| xor | `xor $0x1,%eax; ret` | 2 | ! | go/op_17 |
| xor | `xor %ebx,%eax; ret` | 7 | ^ | go/op_420 |
| xor | `xor %rbx,%rax; ret` | 7 | ^ | go/op_427 |

### wide chaff -- 27 distinct single-opcode bodies

| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |
|---|---|---|---|---|
| add | `add %ebx,%eax; ret` | 7 | + | go/op_312 |
| add | `add %rbx,%rax; ret` | 7 | + | go/op_319 |
| addsd | `addsd %xmm1,%xmm0; ret` | 2 | + | go/op_340 |
| addss | `addss %xmm1,%xmm0; ret` | 2 | + | go/op_333 |
| and | `and %ebx,%eax; ret` | 9 | &, && | go/op_240 |
| and | `and %rbx,%rax; ret` | 7 | & | go/op_247 |
| divsd | `divsd %xmm1,%xmm0; ret` | 2 | / | go/op_124 |
| divss | `divss %xmm1,%xmm0; ret` | 2 | / | go/op_117 |
| imul | `imul %ebx,%eax; ret` | 7 | * | go/op_60 |
| imul | `imul %rbx,%rax; ret` | 7 | * | go/op_67 |
| mulsd | `mulsd %xmm1,%xmm0; ret` | 2 | * | go/op_88 |
| mulss | `mulss %xmm1,%xmm0; ret` | 2 | * | go/op_81 |
| neg | `neg %eax; ret` | 7 | - | go/op_6 |
| neg | `neg %rax; ret` | 7 | - | go/op_7 |
| not | `not %eax; ret` | 7 | ^ | go/op_18 |
| not | `not %rax; ret` | 7 | ^ | go/op_19 |
| or | `or %ebx,%eax; ret` | 9 | |, || | go/op_384 |
| or | `or %rbx,%rax; ret` | 7 | | | go/op_391 |
| pxor | `movsd 0x1d5c0(%rip),%xmm1; pxor %xmm1,%xmm0; ret` | 2 | - | go/op_10 |
| pxor | `movss 0x1d5dc(%rip),%xmm1; pxor %xmm1,%xmm0; ret` | 2 | - | go/op_9 |
| sub | `sub %ebx,%eax; ret` | 7 | - | go/op_348 |
| sub | `sub %rbx,%rax; ret` | 7 | - | go/op_355 |
| subsd | `subsd %xmm1,%xmm0; ret` | 2 | - | go/op_376 |
| subss | `subss %xmm1,%xmm0; ret` | 2 | - | go/op_369 |
| xor | `xor $0x1,%eax; ret` | 2 | ! | go/op_17 |
| xor | `xor %ebx,%eax; ret` | 7 | ^ | go/op_420 |
| xor | `xor %rbx,%rax; ret` | 7 | ^ | go/op_427 |

#### zero-opcode units (pure move, chaff-stripped body is empty)
- narrow: 3 example(s) shown of the histogram's n=0 count
  - `go/op_0` operator `+`: `ret`
  - `go/op_1` operator `+`: `ret`
  - `go/op_2` operator `+`: `ret`
- wide: 3 example(s) shown of the histogram's n=0 count
  - `go/op_0` operator `+`: `ret`
  - `go/op_1` operator `+`: `ret`
  - `go/op_2` operator `+`: `ret`

## java

### narrow chaff -- 0 distinct single-opcode bodies

| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |
|---|---|---|---|---|

### wide chaff -- 1 distinct single-opcode bodies

| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |
|---|---|---|---|---|
| idiv | `mov %edi,%eax; cltd; idiv %esi; ret` | 1 | / | java/op_2 |

#### zero-opcode units (pure move, chaff-stripped body is empty)
- narrow: 0 example(s) shown of the histogram's n=0 count
- wide: 0 example(s) shown of the histogram's n=0 count

## php

### narrow chaff -- 3 distinct single-opcode bodies

| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |
|---|---|---|---|---|
| add | `mov %rsi,%rax; mov %rdi,%r11; add %r11,%rax; ret` | 1 | + | php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER |
| add | `mov %rdi,%rax; mov %rsi,%r11; add %r11,%rax; ret` | 2 | + | php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER |
| add | `mov %rdi,%rax; add %rsi,%rax; ret` | 1 | + | php/add_function |

### wide chaff -- 3 distinct single-opcode bodies

| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |
|---|---|---|---|---|
| add | `mov %rsi,%rax; mov %rdi,%r11; add %r11,%rax; ret` | 1 | + | php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER |
| add | `mov %rdi,%rax; mov %rsi,%r11; add %r11,%rax; ret` | 2 | + | php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER |
| add | `mov %rdi,%rax; add %rsi,%rax; ret` | 1 | + | php/add_function |

#### zero-opcode units (pure move, chaff-stripped body is empty)
- narrow: 0 example(s) shown of the histogram's n=0 count
- wide: 0 example(s) shown of the histogram's n=0 count

## ruby

### narrow chaff -- 2 distinct single-opcode bodies

| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |
|---|---|---|---|---|
| add | `mov %rsi,%rax; add %rdi,%rax; ret` | 1 | + | ruby/rb_fix_plus |
| add | `mov %rdi,%rax; add %rsi,%rax; ret` | 1 | + | ruby/rb_int_plus |

### wide chaff -- 2 distinct single-opcode bodies

| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |
|---|---|---|---|---|
| add | `mov %rsi,%rax; add %rdi,%rax; ret` | 1 | + | ruby/rb_fix_plus |
| add | `mov %rdi,%rax; add %rsi,%rax; ret` | 1 | + | ruby/rb_int_plus |

#### zero-opcode units (pure move, chaff-stripped body is empty)
- narrow: 0 example(s) shown of the histogram's n=0 count
- wide: 0 example(s) shown of the histogram's n=0 count

## rust

### narrow chaff -- 48 distinct single-opcode bodies

| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |
|---|---|---|---|---|
| addsd | `addsd %xmm1,%xmm0; ret` | 2 | + | rust/op_562 |
| addss | `addss %xmm1,%xmm0; ret` | 2 | + | rust/op_555 |
| and | `mov %edi,%eax; and %esi,%eax; ret` | 11 | &, && | rust/op_101 |
| and | `mov %rdi,%rax; and %rsi,%rax; ret` | 6 | & | rust/op_145 |
| divsd | `divsd %xmm1,%xmm0; ret` | 2 | / | rust/op_670 |
| divss | `divss %xmm1,%xmm0; ret` | 2 | / | rust/op_663 |
| imul | `mov %edi,%eax; imul %esi,%eax; ret` | 5 | * | rust/op_606 |
| imul | `mov %rdi,%rax; imul %rsi,%rax; ret` | 6 | * | rust/op_613 |
| lea | `lea (%rdi,%rsi,1),%eax; ret` | 5 | + | rust/op_534 |
| lea | `lea (%rdi,%rsi,1),%rax; ret` | 6 | + | rust/op_541 |
| lea | `lea (%rsi,%rdi,1),%eax; ret` | 2 | + | rust/regen_1029 |
| movb | `mov %rdi,%rax; mov %esi,(%rdi); mov %edx,0x4(%rdi); movb $0x0,0x8(%rdi); ret` | 3 | ..= | rust/op_786 |
| movb | `mov %rdi,%rax; mov %rsi,(%rdi); mov %rdx,0x8(%rdi); movb $0x0,0x10(%rdi); ret` | 6 | ..= | rust/op_793 |
| movb | `mov %rdi,%rax; movss %xmm0,(%rdi); movss %xmm1,0x4(%rdi); movb $0x0,0x8(%rdi); ret` | 2 | ..= | rust/op_807 |
| movb | `mov %rdi,%rax; movsd %xmm0,(%rdi); movsd %xmm1,0x8(%rdi); movb $0x0,0x10(%rdi); ret` | 2 | ..= | rust/op_814 |
| movb | `mov %rdi,%rax; mov %rdx,0x8(%rdi); mov %rsi,(%rdi); mov %r8,0x18(%rdi); mov %rcx,0x10(%rdi); movb $0x0,0x20(%rdi); ret` | 2 | ..= | rust/regen_1591 |
| mul | `mov %esi,%eax; mul %dil; ret` | 2 | * | rust/regen_1057 |
| mulsd | `mulsd %xmm1,%xmm0; ret` | 2 | * | rust/op_634 |
| mulss | `mulss %xmm1,%xmm0; ret` | 2 | * | rust/op_627 |
| neg | `mov %edi,%eax; neg %eax; ret` | 3 | - | rust/op_0 |
| neg | `mov %rdi,%rax; neg %rax; ret` | 3 | - | rust/op_1 |
| neg | `mov %edi,%eax; neg %al; ret` | 1 | - | rust/regen_6 |
| not | `mov %edi,%eax; not %eax; ret` | 5 | ! | rust/op_12 |
| not | `mov %rdi,%rax; not %rax; ret` | 6 | ! | rust/op_13 |
| not | `mov %edi,%eax; not %al; ret` | 2 | ! | rust/regen_28 |
| or | `mov %edi,%eax; or %esi,%eax; ret` | 11 | |, || | rust/op_137 |
| or | `mov %rdi,%rax; or %rsi,%rax; ret` | 6 | | | rust/op_181 |
| sar | `mov %esi,%ecx; mov %edi,%eax; sar %cl,%eax; ret` | 7 | >> | rust/op_498 |
| sar | `mov %rsi,%rcx; mov %edi,%eax; sar %cl,%eax; ret` | 8 | >> | rust/op_499 |
| sar | `mov %esi,%ecx; mov %rdi,%rax; sar %cl,%rax; ret` | 13 | >> | rust/op_504 |
| sar | `mov %rsi,%rcx; mov %rdi,%rax; sar %cl,%rax; ret` | 14 | >> | rust/op_505 |
| shl | `mov %esi,%ecx; mov %edi,%eax; shl %cl,%eax; ret` | 13 | << | rust/op_462 |
| shl | `mov %rsi,%rcx; mov %edi,%eax; shl %cl,%eax; ret` | 14 | << | rust/op_463 |
| shl | `mov %esi,%ecx; mov %rdi,%rax; shl %cl,%rax; ret` | 26 | << | rust/op_468 |
| shl | `mov %rsi,%rcx; mov %rdi,%rax; shl %cl,%rax; ret` | 28 | << | rust/op_469 |
| shr | `mov %esi,%ecx; mov %rdi,%rax; shr %cl,%rax; ret` | 13 | >> | rust/op_510 |
| shr | `mov %rsi,%rcx; mov %rdi,%rax; shr %cl,%rax; ret` | 14 | >> | rust/op_511 |
| shr | `mov %rsi,%rcx; mov %edi,%eax; shr %cl,%eax; ret` | 6 | >> | rust/regen_975 |
| shr | `mov %esi,%ecx; mov %edi,%eax; shr %cl,%eax; ret` | 6 | >> | rust/regen_976 |
| sub | `mov %edi,%eax; sub %esi,%eax; ret` | 5 | - | rust/op_570 |
| sub | `mov %rdi,%rax; sub %rsi,%rax; ret` | 6 | - | rust/op_577 |
| sub | `mov %edi,%eax; sub %sil,%al; ret` | 2 | - | rust/regen_1043 |
| subsd | `subsd %xmm1,%xmm0; ret` | 2 | - | rust/op_598 |
| subss | `subss %xmm1,%xmm0; ret` | 2 | - | rust/op_591 |
| xor | `mov %edi,%eax; xor $0x1,%al; ret` | 2 | ! | rust/op_17 |
| xor | `mov %edi,%eax; xor %esi,%eax; ret` | 11 | !=, ^ | rust/op_210 |
| xor | `mov %rdi,%rax; xor %rsi,%rax; ret` | 6 | ^ | rust/op_217 |
| xorps | `xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` | 4 | - | rust/op_3 |

### wide chaff -- 48 distinct single-opcode bodies

| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |
|---|---|---|---|---|
| addsd | `addsd %xmm1,%xmm0; ret` | 2 | + | rust/op_562 |
| addss | `addss %xmm1,%xmm0; ret` | 2 | + | rust/op_555 |
| and | `mov %edi,%eax; and %esi,%eax; ret` | 11 | &, && | rust/op_101 |
| and | `mov %rdi,%rax; and %rsi,%rax; ret` | 6 | & | rust/op_145 |
| divsd | `divsd %xmm1,%xmm0; ret` | 2 | / | rust/op_670 |
| divss | `divss %xmm1,%xmm0; ret` | 2 | / | rust/op_663 |
| imul | `mov %edi,%eax; imul %esi,%eax; ret` | 5 | * | rust/op_606 |
| imul | `mov %rdi,%rax; imul %rsi,%rax; ret` | 6 | * | rust/op_613 |
| lea | `lea (%rdi,%rsi,1),%eax; ret` | 5 | + | rust/op_534 |
| lea | `lea (%rdi,%rsi,1),%rax; ret` | 6 | + | rust/op_541 |
| lea | `lea (%rsi,%rdi,1),%eax; ret` | 2 | + | rust/regen_1029 |
| movb | `mov %rdi,%rax; mov %esi,(%rdi); mov %edx,0x4(%rdi); movb $0x0,0x8(%rdi); ret` | 3 | ..= | rust/op_786 |
| movb | `mov %rdi,%rax; mov %rsi,(%rdi); mov %rdx,0x8(%rdi); movb $0x0,0x10(%rdi); ret` | 6 | ..= | rust/op_793 |
| movb | `mov %rdi,%rax; movss %xmm0,(%rdi); movss %xmm1,0x4(%rdi); movb $0x0,0x8(%rdi); ret` | 2 | ..= | rust/op_807 |
| movb | `mov %rdi,%rax; movsd %xmm0,(%rdi); movsd %xmm1,0x8(%rdi); movb $0x0,0x10(%rdi); ret` | 2 | ..= | rust/op_814 |
| movb | `mov %rdi,%rax; mov %rdx,0x8(%rdi); mov %rsi,(%rdi); mov %r8,0x18(%rdi); mov %rcx,0x10(%rdi); movb $0x0,0x20(%rdi); ret` | 2 | ..= | rust/regen_1591 |
| mul | `mov %esi,%eax; mul %dil; ret` | 2 | * | rust/regen_1057 |
| mulsd | `mulsd %xmm1,%xmm0; ret` | 2 | * | rust/op_634 |
| mulss | `mulss %xmm1,%xmm0; ret` | 2 | * | rust/op_627 |
| neg | `mov %edi,%eax; neg %eax; ret` | 3 | - | rust/op_0 |
| neg | `mov %rdi,%rax; neg %rax; ret` | 3 | - | rust/op_1 |
| neg | `mov %edi,%eax; neg %al; ret` | 1 | - | rust/regen_6 |
| not | `mov %edi,%eax; not %eax; ret` | 5 | ! | rust/op_12 |
| not | `mov %rdi,%rax; not %rax; ret` | 6 | ! | rust/op_13 |
| not | `mov %edi,%eax; not %al; ret` | 2 | ! | rust/regen_28 |
| or | `mov %edi,%eax; or %esi,%eax; ret` | 11 | |, || | rust/op_137 |
| or | `mov %rdi,%rax; or %rsi,%rax; ret` | 6 | | | rust/op_181 |
| sar | `mov %esi,%ecx; mov %edi,%eax; sar %cl,%eax; ret` | 7 | >> | rust/op_498 |
| sar | `mov %rsi,%rcx; mov %edi,%eax; sar %cl,%eax; ret` | 8 | >> | rust/op_499 |
| sar | `mov %esi,%ecx; mov %rdi,%rax; sar %cl,%rax; ret` | 13 | >> | rust/op_504 |
| sar | `mov %rsi,%rcx; mov %rdi,%rax; sar %cl,%rax; ret` | 14 | >> | rust/op_505 |
| shl | `mov %esi,%ecx; mov %edi,%eax; shl %cl,%eax; ret` | 13 | << | rust/op_462 |
| shl | `mov %rsi,%rcx; mov %edi,%eax; shl %cl,%eax; ret` | 14 | << | rust/op_463 |
| shl | `mov %esi,%ecx; mov %rdi,%rax; shl %cl,%rax; ret` | 26 | << | rust/op_468 |
| shl | `mov %rsi,%rcx; mov %rdi,%rax; shl %cl,%rax; ret` | 28 | << | rust/op_469 |
| shr | `mov %esi,%ecx; mov %rdi,%rax; shr %cl,%rax; ret` | 13 | >> | rust/op_510 |
| shr | `mov %rsi,%rcx; mov %rdi,%rax; shr %cl,%rax; ret` | 14 | >> | rust/op_511 |
| shr | `mov %rsi,%rcx; mov %edi,%eax; shr %cl,%eax; ret` | 6 | >> | rust/regen_975 |
| shr | `mov %esi,%ecx; mov %edi,%eax; shr %cl,%eax; ret` | 6 | >> | rust/regen_976 |
| sub | `mov %edi,%eax; sub %esi,%eax; ret` | 5 | - | rust/op_570 |
| sub | `mov %rdi,%rax; sub %rsi,%rax; ret` | 6 | - | rust/op_577 |
| sub | `mov %edi,%eax; sub %sil,%al; ret` | 2 | - | rust/regen_1043 |
| subsd | `subsd %xmm1,%xmm0; ret` | 2 | - | rust/op_598 |
| subss | `subss %xmm1,%xmm0; ret` | 2 | - | rust/op_591 |
| xor | `mov %edi,%eax; xor $0x1,%al; ret` | 2 | ! | rust/op_17 |
| xor | `mov %edi,%eax; xor %esi,%eax; ret` | 11 | !=, ^ | rust/op_210 |
| xor | `mov %rdi,%rax; xor %rsi,%rax; ret` | 6 | ^ | rust/op_217 |
| xorps | `xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret` | 4 | - | rust/op_3 |

#### zero-opcode units (pure move, chaff-stripped body is empty)
- narrow: 3 example(s) shown of the histogram's n=0 count
  - `rust/op_36` operator `..`: `mov %edi,%eax; ret`
  - `rust/op_37` operator `..`: `mov %rdi,%rax; ret`
  - `rust/op_38` operator `..`: `mov %rdi,%rax; ret`
- wide: 3 example(s) shown of the histogram's n=0 count
  - `rust/op_36` operator `..`: `mov %edi,%eax; ret`
  - `rust/op_37` operator `..`: `mov %rdi,%rax; ret`
  - `rust/op_38` operator `..`: `mov %rdi,%rax; ret`

## swift

### narrow chaff -- 19 distinct single-opcode bodies

| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |
|---|---|---|---|---|
| addsd | `addsd %xmm1,%xmm0; ret` | 2 | + | swift/op_250 |
| addss | `addss %xmm1,%xmm0; ret` | 2 | + | swift/op_243 |
| and | `mov %edi,%eax; and %esi,%eax; ret` | 9 | &, && | swift/op_582 |
| and | `mov %rdi,%rax; and %rsi,%rax; ret` | 6 | & | swift/op_589 |
| divsd | `divsd %xmm1,%xmm0; ret` | 2 | / | swift/op_178 |
| divss | `divss %xmm1,%xmm0; ret` | 2 | / | swift/op_171 |
| mulsd | `mulsd %xmm1,%xmm0; ret` | 2 | * | swift/op_142 |
| mulss | `mulss %xmm1,%xmm0; ret` | 2 | * | swift/op_135 |
| not | `mov %edi,%eax; not %eax; ret` | 5 | ~ | swift/op_36 |
| not | `mov %rdi,%rax; not %rax; ret` | 6 | ~ | swift/op_37 |
| not | `mov %edi,%eax; not %al; ret` | 2 | ~ | swift/regen_83 |
| or | `mov %edi,%eax; or %esi,%eax; ret` | 9 | |, || | swift/op_618 |
| or | `mov %rdi,%rax; or %rsi,%rax; ret` | 6 | | | swift/op_625 |
| subsd | `subsd %xmm1,%xmm0; ret` | 2 | - | swift/op_286 |
| subss | `subss %xmm1,%xmm0; ret` | 2 | - | swift/op_279 |
| xor | `mov %edi,%eax; xor $0x1,%al; ret` | 2 | ! | swift/op_29 |
| xor | `mov %edi,%eax; xor %esi,%eax; ret` | 9 | !=, ^ | swift/op_473 |
| xor | `mov %rdi,%rax; xor %rsi,%rax; ret` | 6 | ^ | swift/op_661 |
| xorps | `xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI1_0-0x4; ret` | 4 | - | swift/op_15 |

### wide chaff -- 19 distinct single-opcode bodies

| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |
|---|---|---|---|---|
| addsd | `addsd %xmm1,%xmm0; ret` | 2 | + | swift/op_250 |
| addss | `addss %xmm1,%xmm0; ret` | 2 | + | swift/op_243 |
| and | `mov %edi,%eax; and %esi,%eax; ret` | 9 | &, && | swift/op_582 |
| and | `mov %rdi,%rax; and %rsi,%rax; ret` | 6 | & | swift/op_589 |
| divsd | `divsd %xmm1,%xmm0; ret` | 2 | / | swift/op_178 |
| divss | `divss %xmm1,%xmm0; ret` | 2 | / | swift/op_171 |
| mulsd | `mulsd %xmm1,%xmm0; ret` | 2 | * | swift/op_142 |
| mulss | `mulss %xmm1,%xmm0; ret` | 2 | * | swift/op_135 |
| not | `mov %edi,%eax; not %eax; ret` | 5 | ~ | swift/op_36 |
| not | `mov %rdi,%rax; not %rax; ret` | 6 | ~ | swift/op_37 |
| not | `mov %edi,%eax; not %al; ret` | 2 | ~ | swift/regen_83 |
| or | `mov %edi,%eax; or %esi,%eax; ret` | 9 | |, || | swift/op_618 |
| or | `mov %rdi,%rax; or %rsi,%rax; ret` | 6 | | | swift/op_625 |
| subsd | `subsd %xmm1,%xmm0; ret` | 2 | - | swift/op_286 |
| subss | `subss %xmm1,%xmm0; ret` | 2 | - | swift/op_279 |
| xor | `mov %edi,%eax; xor $0x1,%al; ret` | 2 | ! | swift/op_29 |
| xor | `mov %edi,%eax; xor %esi,%eax; ret` | 9 | !=, ^ | swift/op_473 |
| xor | `mov %rdi,%rax; xor %rsi,%rax; ret` | 6 | ^ | swift/op_661 |
| xorps | `xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI1_0-0x4; ret` | 4 | - | swift/op_15 |

#### zero-opcode units (pure move, chaff-stripped body is empty)
- narrow: 3 example(s) shown of the histogram's n=0 count
  - `swift/op_18` operator `+`: `mov %edi,%eax; ret`
  - `swift/op_19` operator `+`: `mov %rdi,%rax; ret`
  - `swift/op_20` operator `+`: `mov %rdi,%rax; ret`
- wide: 3 example(s) shown of the histogram's n=0 count
  - `swift/op_18` operator `+`: `mov %edi,%eax; ret`
  - `swift/op_19` operator `+`: `mov %rdi,%rax; ret`
  - `swift/op_20` operator `+`: `mov %rdi,%rax; ret`

