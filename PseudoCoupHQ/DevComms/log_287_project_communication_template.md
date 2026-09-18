*notes*:

* DO NOT INSERT PARAGRAPHS OF PROSE

### 0. Basic Numbers

Number of RISCV arch-opcodes: 1038

Number of GMP primitives: 24

* add, and, ashr, freeze, lshr, mul, or, sext, shl, sub, trunc, udiv, xor, zext
* eq, ne, sgt, slt, ugt, ult
* abs, ctlz, fshl, usub.sat

Number of cpp arch-units: 770

Number of c arch-units: 610

Number of csharp arch-units: 253

Number of javascript arch-units: 240

Number of swift arch-units: 167

Number of rust arch-units: 125

Number of go arch-units: 107

Number of dart arch-units: 82

Number of php arch-units: 4

Number of ruby arch-units: 3

Number of java arch-units: 2

Number of cpython arch-units: 1

Number of x86-64 arch-units, all languages measured: 2364

*notes:*

* these twelve are not the ratified twelve
  * c, javascript and cpython are here and are not on that list
  * python, typescript and kotlin are on that list and have no probes
* they are x86-64 arch-units; section 2 lowers the same compiler-operators
  for riscv64, and that is a different count

*notes:*

* all 1038 RISCV arch-opcodes have Lean expressions

### 1. RISC-V instructions in Lean, from Sail

*notes:*

- 1038 RISCV arch-opcodes are full-body Lean expressions via Sail model
- 0 RISCV arch-opcodes are body-less Lean expressions
- 0 `sorry`
- 354 Sail clauses cover the 1038; one clause per dispatch enum
  - execute_ITYPE is 1 clause and 6 arch-opcodes: ADDI SLTI SLTIU ANDI ORI XORI
- 685 of the 1038 the flattener cannot reduce to a standalone expression
  - that is the flattener, not the body
  - 262 vector: the element width is machine state, not a parameter
  - 218 match on a tuple of the parameters
  - 90 read the rounding mode out of fcsr
  - 70 not measured
  - 21 assert on xlen/width
  - 13 CSR, traps, barriers, memory
  - 11 the body is the retire

#### 1.1 Sail to Lean

```python
arch_opcode_leans = {}
for arch_opcode in sail_riscv_model:
 arch_opcode_leans[arch_opcode] = get_sail_def(arch_opcode, output="Lean")
 # every primitive value inside is the universal type (sign, mant, expo),
 # constrained to a kind: bool, unsigned n, signed n, float (e, m), fixed;
 # a composite (text, a sequence, a keyed thing) is an address, a length
 # and bytes in memory, each of those a universal value again
```

Complete: 100% (1038 of 1038 arch_opcodes)

#### 1.2 GMP Slice Insertion

```python
for arch_opcode in arch_opcode_leans:
    arch_opcode_lean = arch_opcode_leans[arch_opcode]
    arch_opcode_leans[arch_opcode] = gmp_slice_insertion(arch_opcode_lean)
```

Complete: 100% (67 of 67 axioms)

*notes:*

- the 67 `axiom` in LeanIM/RiscvExtras.lean were the only body-less thing in
  the whole model; all 67 now have a body and the declarations are gone
- each body is the slice, walked to Lean over the 24 GMP primitives
- 5 rounding modes per axiom, the mode dispatched on in the body
- 111562 IR instructions walked; 114713 lines of Lean; 68 modules
- lake build: 68 of 68 modules, 0 failed, 60s (lp3_l130)
- `#print axioms riscv_f64Add` -> [propext, Quot.sound]
  - Lean's own two; no sorry, no riscv_*
- 8 `axiom` left in RiscvExtras, none of them float:
  - plat_term_read, plat_term_write, get_16_random_bits
  - load_reservation, match_reservation, cancel_reservation, valid_reservation
  - sys_enable_experimental_extensions

### 2. every language's compiler-operators, lowered to arch-units, in Lean with full-body

```python
for lang in langs:
 for compiler_operator in lang.compiler_operators:
 arch_unit = lower(compiler_operator) # compile for RISC-V
 arch_unit.lean = build_unit_lean(arch_unit, arch_opcode_leans)
 arch_unit.kinds = discover_kinds(arch_unit.lean) # kinds read off the Lean, not written by hand
```

Complete: 68% (1612 of 2364 total arch-units)

*notes:*

- every compiled language is complete; 1612 = 770 + 610 + 125 + 107
- 1612 of 1612 are full-body Lean expressions, 0 refused
  - lake build Units: 4 of 4 modules, 0 errors (lp1_l57)
- 1582 of the 1612 are straight line: the only jump is the final return
  - for those, the clauses in program order ARE the body
- 30 branch before the end (go 24, rust 6)
  - for those the same sequence is the fall-through trace, not the whole
    body; each carries that line as a comment in its Lean

* cpp arch-units: 770 of 770 --- in Lean: 770
* c arch-units: 610 of 610 --- in Lean: 610
* rust arch-units: 125 of 125 --- in Lean: 125
* go arch-units: 107 of 107 --- in Lean: 107
* csharp 253, javascript 240, swift 167, dart 82, php 4, ruby 3, java 2,
  cpython 1: 0 lowered, 0 in Lean

- how the Lean is built
  - an arch-unit is a sequence of arch-opcodes; each is a full-body
    `execute_<CLAUSE>` in the model; the unit is those in order
  - which clause, and which operands, is read off the model's own
    `assembly_forwards` clause (leanpath/from_asm.py); nothing hand-written
  - 352 of 354 assembly clauses readable; every instruction line read
  - the rounding mode objdump does not print is read from the encoding
  - fli's constant is read from the model's own FLI table
  - Sail's decoder is not used: it is `noncomputable` in the proof emit

- what the last three gaps actually were, all of them flags
  - 22 cpp: the ship flags said -std=c++17 and `<=>` is C++20
  - 36 assembler refusals: the lifter's march string had no zcb, no zfa
  - 8 fli.s/fli.d: objdump prints the value, the model spells the index

- 81 arch-units rv_attest calls WALK_REFUSED are in Lean
  - that gate is rv_attest's own term walker, not Sail; build_unit_lean
    does not use it

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
| csharp | 253 | 20 | **0 of 253** | riscv64 codegen only |
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
- the toolchain answers, measured in lp1_l58
  - swift: the toolchain ships only x86_64 swiftmodules; no riscv64 stdlib
  - dart: gen_snapshot is built per target; the SDK's is linux_x64
  - dotnet: `NETSDK1203`, and nuget has no linux-riscv64 runtime pack at all
- the sources to build each are already staged: `/sources/runtime` (CoreCLR),
  `/sources/sdk` (Dart), `/sources/chromium_src` (V8), `/sources/jdk`
- python, typescript and kotlin are ratified and have no probe manifest

### 3. the primitives: which arch-units equal which pieces of Sail's definitions

```python
sail_lean_primitives = pieces_of(arch_opcode_leans) # a + b, a xor b, the 32-bit add, ...
for lang in langs:
 for primitive in sail_lean_primitives:
 for arch_unit in lang.arch_units:
 if prove_lean_equivalence(primitive, arch_unit.lean):
 lang.arch_unit_lean_primitives[primitive] = arch_unit
```

Complete: 0%

*notes:*

- pieces_of() exists: 459 primitives, 392 atoms
- arch_unit_lean_primitives per language does not exist

### 4. every arch-opcode emulated in every language, from those primitives only

```python
for lang in langs:
 for arch_opcode, definition in arch_opcode_leans.items():
 emulation = build_emulation(definition, lang.arch_unit_lean_primitives)
 arch_unit = lower(emulation)
 arch_unit.lean = build_unit_lean(arch_unit, arch_opcode_leans)
 emulation.proven = prove_lean_equivalence(definition, arch_unit.lean)
```

Complete: 0%

*notes:*

- 34 integer arch-opcodes + 67 float ops emulated in 8 languages, bit-exact
- built without step 3
- what is proved is arch_unit = emulation (542 arch-units), not definition = arch_unit.lean

### 5. any language's arch-unit expressed in any other language's

```python
for lang_i in langs:
 for lang_j in langs:
 for arch_unit_i in lang_i.arch_units:
 for arch_unit_j in lang_j.arch_units:
 if prove_lean_equivalence(arch_unit_i.lean, arch_unit_j.lean):
 equivalents.add(arch_unit_i, arch_unit_j)
```

Complete: 0% (0 of 1312 arch-units proved equal to another language's)

*notes:*

- 979 arch-units in classes spanning more than one language
- c/cpp 880, cpp/rust 303, c/rust 204; go shares none
- related by identical body and arrival shape, not by prove_lean_equivalence
