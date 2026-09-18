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

### THE PATH FROM 1612 TO 2364

752 units, eight languages, one cause: `riscv_carve.py COMPILE` holds a
compile rule for c, cpp, rust and go and nothing else.

| language | units | toolchain | state |
|---|---|---|---|
| csharp | 253 | dotnet 9.0.318 | installed, riscv64 being probed |
| javascript | 240 | V8, /sources/chromium_src | interpreter binary route |
| swift | 167 | swiftc | no <os> build; 24.04 tarball being tried |
| dart | 82 | dart 3.13.4 | installed, gen_snapshot is target-locked |
| php | 4 | php-src | interpreter binary route |
| ruby | 3 | ruby | interpreter binary route |
| java | 2 | /sources/jdk | interpreter binary route |
| cpython | 1 | cpython | interpreter binary route |

- riscv64-linux-gnu-gcc is in the image, so the C interpreters (cpython,
  ruby, php) cross-compile directly
- the route is the one already proven on Berkeley SoftFloat: compile for
  riscv64, link transitive helpers, internalize, inline, dead-code
  eliminate, one function per operation
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
