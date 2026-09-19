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

Number of php arch-units: not measured

Number of ruby arch-units: not measured

Number of java arch-units: not measured

Number of cpython arch-units: not measured

Number of x86-64 arch-units, all languages measured: 2356

*notes:*

* an arch-unit is one hi-op with its holders, lowered and sliced to context
* the counts above are hi-op x holder, from each language's probe manifest
* php, ruby, java and cpython have NO probe manifest
  * what was recorded for them is a handful of hand-named interpreter symbols
    (add_function, vm_opt_plus, _PyLong_Add), which is not a population
  * a manifest has to be generated for each before they have a number
* these twelve are not the ratified twelve
* c, javascript and cpython are here and are not on that list
* python, typescript and kotlin are on that list and have no probes
* they are x86-64 arch-units; section 2 lowers the same hi-ops for riscv64,
  which is a different count

### 1. RISC-V instructions in Lean, from Sail

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

*notes:*

- 1038 arch-opcodes are full-body Lean expressions via Sail model
- 0 are body-less
- 0 `sorry`
- 354 Sail clauses cover the 1038; one clause per dispatch enum
  - execute_ITYPE is 1 clause and 6 arch-opcodes: ADDI SLTI SLTIU ANDI ORI XORI

#### 1.2 GMP Slice Insertion

```python
for arch_opcode in arch_opcode_leans:
    arch_opcode_lean = arch_opcode_leans[arch_opcode]
    arch_opcode_leans[arch_opcode] = gmp_slice_insertion(arch_opcode_lean)
```

Complete: 100% (67 of 67 axioms)

*notes:*

- the 67 `axiom` in LeanIM/RiscvExtras.lean were the only body-less thing in
  the model; all 67 now have a body
- each body is the slice, walked to Lean over the 24 GMP primitives
- 5 rounding modes per axiom, dispatched on in the body
- 111562 IR instructions walked; 114713 lines of Lean; 68 modules
- lake build: 204 jobs, 0 errors
- `#print axioms riscv_f64Add` -> [propext, Quot.sound]; no sorry, no riscv_*
- 8 `axiom` left, all platform hooks, none float

### 2. every language's compiler-operators, lowered to arch-units, in Lean with full-body

```python
for lang in langs:
 for compiler_operator in lang.compiler_operators:
 arch_unit = lower(compiler_operator) # compile for RISC-V
 arch_unit.lean = build_unit_lean(arch_unit, arch_opcode_leans)
 arch_unit.kinds = discover_kinds(arch_unit.lean) # kinds read off the Lean, not written by hand
```

Complete: 86% (2023 of 2356 total arch-units)

*notes:*

- 2023 arch-units lowered for riscv64; 2023 of 2023 in Lean, 0 refused
- lake build Units + UnitsCs + UnitsSw: 6 of 6 modules, 0 errors
- 1956 are straight line; 67 branch before the end and are the fall-through
  trace, each marked as such in its own Lean
- a branch's operand is now the encoded offset, not the printed target
  - a disassembler prints the target address; the encoding holds target - addr
  - the addresses come from the word lengths, so nothing was re-carved
- csharp needed a riscv64 code generator, which no released package ships
  - RyuJIT's RISC-V backend is behind CLR_CMAKE_BUILD_COMMUNITY_ALTJITS
  - built from /sources/runtime with crossgen2 from the same tree

* cpp arch-units in Lean: 770 of 770
* c arch-units in Lean: 610 of 610
* rust arch-units in Lean: 125 of 125
* go arch-units in Lean: 107 of 107
* php arch-units in Lean: 1 --- `+` on (long, long); no manifest, no denominator
* csharp arch-units in Lean: 253 of 253 --- 942 in the manifest, 253 the compiler accepts
* javascript arch-units in Lean: 0 of 240
* swift arch-units in Lean: 157 of 167 --- 1086 in the manifest, 167 swiftc accepts
* dart arch-units in Lean: 0 of 82
* ruby arch-units in Lean: 0 --- `+` not pure, the overflow arm allocates
* java arch-units in Lean: 0
* cpython arch-units in Lean: 0 --- `+` not pure, allocates and refcounts

- the working notes are log_301

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
- what is proved is arch_unit = emulation (542 arch-units), not
  definition = arch_unit.lean

### 5. any language's arch-unit expressed in any other language's

```python
for lang_i in langs:
 for lang_j in langs:
 for arch_unit_i in lang_i.arch_units:
 for arch_unit_j in lang_j.arch_units:
 if prove_lean_equivalence(arch_unit_i.lean, arch_unit_j.lean):
 equivalents.add(arch_unit_i, arch_unit_j)
```

Complete: 0% (0 of 1612 arch-units proved equal to another language's)

*notes:*

- 979 arch-units in classes spanning more than one language
- c/cpp 880, cpp/rust 303, c/rust 204; go shares none
- related by identical body and arrival shape, not by prove_lean_equivalence
