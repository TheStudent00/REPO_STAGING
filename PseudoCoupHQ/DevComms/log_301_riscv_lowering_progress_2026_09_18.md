# log 301 --- riscv64 lowering, working notes, 2026-09-18

The counts live in `log_287_project_communication_template.md`, which stays in
its own form. This is where the reasoning behind them goes, so that one does
not fill with prose.

### THE INTERPRETER ROUTE, PROVED ON php (2026-09-18)

php's `+` is a full-body Lean arch-unit, typechecked by Lean. It is the fifth
language. the owner's ruling: a branch-full arch-unit is context-sliced like the GMP
slices, not modelled with a program counter.

| step | | blocks | br | call | instructions |
|---|---|---|---|---|---|
| carved from the built .o | machine code, already through the backend | - | 18 transfers | - | 117 |
| `add_function` sliced raw | internalize, inline, globaldce | 729 | 715 | 170 | 3000 |
| pinned to the arrival | both operands IS_LONG, zvals built locally | 3 | 3 | 1 | 8 |
| flattened | flatten_dag.py, if-converted | 1 | 0 | 1 | 13 |
| compiled for riscv64 | | 1 | **0** | 0 | **14** |

- the pin is the store's own `arrival_annotation`, nothing new
  - php `zval*`; ruby `VALUE (tagged word)`; cpython `i32`
  - built LOCALLY so sroa makes the type tag a constant, which is what
    deletes the dispatch --- exactly what pinning the rounding mode did to
    SoftFloat's switch
- what survives is php's real semantics: add, and if it overflows redo it as
  a double --- both arms computed, masked, or'd
- the flattened body uses fcvt.d.l, fadd.d, fmv.x.d
  - those have Lean bodies ONLY because 1.2 gave the 67 float axioms bodies
  - the interpreted route lands on the float layer and the float layer is no
    longer a hole
- the slicer eats BITCODE; a carved .o has already been through the backend
  and has nothing left to if-convert

### WHICH RUNTIMES HAVE A PURE ARCH-UNIT FOR `+`, AND WHY

The pin is the same for all three. What differs is how the runtime represents
an integer, and that alone decides whether the operator is arithmetic.

| runtime | how an operand arrives | what the result path does | pure |
|---|---|---|---|
| php | `zval`, a value struct the caller builds | overflow promotes to a double | **yes** |
| ruby | `VALUE`, a tagged word | overflow allocates a Bignum | no |
| cpython | `PyObject *`, a heap object throughout | allocates, refcounts, may raise | no |

| runtime | blocks | br | call | instructions |
|---|---|---|---|---|
| php, pinned and flattened | 1 | 0 | 0 | 14 |
| ruby, pinned | 6 | 6 | 5 | 42 |
| cpython, pinned | 2460 | 2186 | 951 | 7054 |

- what survives in cpython: `_PyLong_New`, `_Py_Dealloc`, `_Py_NewReference`,
  `PyErr_SetString`, `PyErr_NoMemory`, `__assert_fail`
  - allocation, reference counting and exception raising
  - all of them effects on interpreter state, none of them arithmetic
- php reduces because its operands are a VALUE STRUCT the caller builds on the
  stack, so sroa makes the type tag a constant
- cpython cannot: a `PyObject *` is a pointer, and the optimiser knows nothing
  about what it points at
- this is a property of each runtime's value representation, NOT of the
  pipeline

*this decides the shape of the remaining eight languages*

- .NET's `int` is unboxed, like php's long --- expect php's answer
- V8's Smi is a tagged word, like ruby's VALUE --- expect ruby's
- the question to ask of each runtime FIRST is how it represents the operand,
  because that is what decides whether the operator is arithmetic at all

### ruby DOES NOT COLLAPSE, AND THE REASON IS THE LANGUAGE

| | blocks | br | call | instructions |
|---|---|---|---|---|
| php `+`, pinned and flattened | 1 | 0 | 0 | 14 |
| ruby `+`, pinned the same way | 6 | 6 | 5 | 42 |

- the calls that survive in ruby are `rb_wb_protected_newobj_of` and
  `rb_obj_freeze_inline` --- the GC allocator
- php's overflow arm promotes to a double, which is arithmetic and flattens
- ruby's integers are arbitrary precision, so its overflow arm ALLOCATES a
  Bignum: a heap side effect, not arithmetic
- that is a property of ruby, not a limit of the pipeline
- stating the bound in the wrapper (`__builtin_unreachable` on overflow)
  became an `llvm.assume` the optimiser did not carry into the tagged
  domain; the Bignum arm stayed
- so ruby's `+` is NOT a pure arch-unit
  - the bounded arm is, and it is visible in the slice as
    shl / or / sadd.with.overflow --- `LONG2FIX(FIX2LONG(x) + FIX2LONG(y))`
  - naming it as a separate bounded unit is a decision for the owner, not one to
    take quietly

### THE PATH FROM 1612 TO 2364, MEASURED

752 units, eight languages. Their x86-64 bodies are already in the store, so
what each one needs can be read off those bodies rather than guessed.

| language | units | median instructions | branch or call before the end | what it needs |
|---|---|---|---|---|
| csharp | 253 | 20 | **0 of 253** | **UNBLOCKED** --- compiles to riscv64 |
| javascript | 240 | 173 | **240 of 240** | riscv64 codegen AND slicing |
| swift | 167 | 3 | 29 of 167 | riscv64 stdlib only |
| dart | 82 | 42 | **82 of 82** | riscv64 codegen AND slicing |
| php | 4 | --- | --- | **1 done**; the route is proved |
| ruby | 3 | --- | --- | not pure: the overflow arm allocates |
| java | 2 | --- | --- | riscv64 codegen |
| cpython | 1 | --- | --- | not pure: allocates, refcounts, may raise |

- csharp and swift are NOT an interpreter problem at all
  - their bodies are unboxed machine values, already straight line
  - 420 units blocked on one thing each: a riscv64 code generator
- javascript and dart carry type guards and deoptimisation paths in every
  body, so they need the pin and the flattener as well
### csharp COMPILES TO RISC-V (2026-09-18)

```
=== cs7_Ops__op_0   34 bytes      // public static int op_0(int a, int b) => a + b;
   0: ff010113   addi sp,sp,-16
   4: 00813023   sd   s0,0(sp)
   8: 00113423   sd   ra,8(sp)
   c: 00010413   addi s0,sp,0
  10: 9d2d       c.addw a0,a1
  12: 00813083   ld   ra,8(sp)
  16: 00013403   ld   s0,0(sp)
  1a: 01010113   addi sp,sp,16
  1e: 00008067   jalr zero,0(ra)
```

- straight line, no branch --- as the x86 bodies said all 253 would be
- crossgen2 writes a per-method map, which is what makes a body addressable:
  `0x000109B0,34,0,.text,cs7_Ops__op_0,MethodWithGCInfo`
- the R2R PE machine is 0x2b1d = 0x5064 (RISCV64) XOR 0x7b79, ReadyToRun's
  Linux override
- the five things it took, each one measured not guessed
  1. `CLR_CMAKE_BUILD_COMMUNITY_ALTJITS` gates the riscv64 cross-JIT; the
     subset that sets it is `clr.alljitscommunity`
  2. crossgen2 is in `clr.tools` --- `clr.crossgen2` is not a subset
  3. both must come from the SAME tree: the shipped 9.0.20 crossgen2 with a
     JIT off main refuses every method, the JIT/EE interface GUID must match
  4. run crossgen2 with the TREE's own dotnet; it targets 11.0-preview and
     the installed 9.0.20 cannot host it
  5. use the published crossgen2 under `bin/.../crossgen2/`, not the
     intermediate one under `obj/crossgen2_publish/`

- csharp: the riscv64 cross-JIT is BUILT (lp1_l83)
  - `libclrjit_unix_riscv64_x64.so`, 15M, from /sources/runtime
  - jit/CMakeLists.txt gates it on `CLR_CMAKE_BUILD_COMMUNITY_ALTJITS`, and
    `clr.alljitscommunity` is the subset that sets it
  - `clr.crossgen2` is NOT a subset; crossgen2 is in `clr.tools`
  - paired with the SHIPPED 9.0.20 crossgen2 the JIT refuses every method
    (`CodeGenerationFailedException`): the JIT/EE interface GUID has to match,
    so both must come from the same tree
- three tower unblocks found on the way
  - apt needs BOTH `APT::Sandbox::User=root` (for `Failed to setgroups`) and a
    writable `Dir::Cache::archives` (for `/var/cache/apt/.../partial: Permission
    denied`); with those it reaches the ubuntu repos and installs
  - dotnet's build feeds are `pkgs.dev.azure.com`, now allowlisted
  - CoreCLR's Linux prerequisites are libkrb5-dev, liblttng-ust-dev,
    libunwind-dev, libicu-dev, libssl-dev
- csharp's blocker was ONE FILE, measured in lp1_l76
  - crossgen2 ACCEPTS `--targetarch riscv64`; it then fails on
    `Unable to load shared library 'clrjit_unix_riscv64_x64'`
  - the linux-x64 crossgen2 package does not ship the cross-targeting JIT
  - dotnet/runtime builds exactly it as the `clr.alljits` subset --- the JIT
    alone, not the runtime; lane lp1_l77 is building it
- swift genuinely needs a riscv64 stdlib, measured in lp1_l76
  - `-parse-stdlib` removes the stdlib, and then `Int32` does not exist
  - swift cannot compile even `a &+ b` without it
- the toolchain answers, measured in lp1_l58
  - swift: the toolchain ships only x86_64 swiftmodules; no riscv64 stdlib
  - dart: gen_snapshot is built per target; the SDK's is linux_x64
  - dotnet: `NETSDK1203`, and nuget has no linux-riscv64 runtime pack at all
- the sources to build each are already staged: `/sources/runtime` (CoreCLR),
  `/sources/sdk` (Dart), `/sources/chromium_src` (V8), `/sources/jdk`
- python, typescript and kotlin are ratified and have no probe manifest


### csharp ONLINE --- 253 of 253 in Lean (2026-09-18)

| | |
|---|---|
| hi-op x holder probes in the manifest | 942 |
| roslyn accepts | 253 |
| roslyn refuses | 689 |
| carved from the riscv64 R2R image | 253 |
| read back to arch-opcodes | 253 |
| full-body Lean, typechecked | **253** |

- the refused 689 are the generator's own invalid spellings, 36 of each:
  `a with b`, `a ?? b`, `a as b`, `a is b`, `a .. b`, `a && b` on non-bools
  - the same COMPILE-OR-REFUSE gate that refuses `!` on a float in c
  - 253 is exactly what the x86 store holds a body for, from the same gate
- 236 straight line, 17 branch before the end
- three spelling gaps between GNU objdump and the model, all named
  - the model calls x8 `fp`; objdump prints `s0`. The psABI defines the
    register as s0/fp, so both spellings are entered for it
  - objdump annotates a pc-relative line with the address it computes
    (`addi a0,a0,-1456 # 0x24a88`); the comment is not part of the instruction
  - crossgen2's map size covers the method AND the constant pool it loads:
    `++` on double ends at its return and is followed by the eight bytes of
    1.0, which objdump renders as `c.unimp` and a `c.fld`.  Every body here is
    straight line, so the first return is the end and what follows is data.
    10 bodies, 74 lines trimmed

### swift ONLINE --- 150 of 167 in Lean (2026-09-18)

swift.org publishes no riscv64 toolchain (404; aarch64 is 200) and the stdlib
swiftmodules are target-tagged, so the front end cannot be aimed at riscv64.
It does not need to be.

| | |
|---|---|
| hi-op x holder probes in the manifest | 1086 |
| swiftc accepts | 167 |
| swiftc refuses | 919 |
| carved from the riscv64 object | 157 |
| full-body Lean, typechecked | **150** |

- 167 is exactly what the x86 store holds a body for --- the same gate
- the 919 are mostly `++a` and `--a`, removed from swift in version 3
- the route: `-emit-ir` on x86_64, then retarget the module and drop
  - `target-cpu` / `target-features` --- how to codegen for x86, not what the
    function is
  - `swiftcc` --- LLVM's RISC-V backend has no lowering for it, and the
    corpus's probes are `@_cdecl`, which is ccc already
- THE ASSUMPTION, stated: x86-64 and riscv64 are both LP64 little-endian with
  the same scalar alignments, and these are leaf functions over fixed-width
  scalars touching no stdlib runtime, so the front end's output does not
  depend on which of the two it was told

```
@_cdecl("op_0") public func op_0(_ a: Int32, _ b: Int32) -> Int32 { a &+ b }
   0: 9d2d       c.addw a0,a1
   2: 8082       c.jr   ra
```

### A DEFECT TO FIX: the branch immediate comes from the text

`from_asm` reads a branch's immediate out of the disassembly, and GNU objdump
prints a branch TARGET (an address inside the function) where the encoding
holds a pc-relative OFFSET, in bare hex with no `0x`.  So for any unit with a
branch before the end, that operand is wrong.

- 60 units of 2016 are affected, and they are exactly the ones already marked
  as a fall-through trace rather than a whole body
- no straight-line unit carries a pc-relative immediate, so none of the 1956
  is affected
- the fix is to decode the immediate from the instruction WORD, which every
  row already carries; the model's own encdec clause gives the bit layout
