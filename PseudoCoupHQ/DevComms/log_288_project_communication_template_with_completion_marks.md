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

Complete: True

#### 1.2 Opaque Lean types to Universal Types

```python
for arch_opcode in arch_opcode_leans:
    arch_opcode_lean = arch_opcode_leans[arch_opcode]
    arch_opcode_leans[arch_opcode] = map_to_universal_types(arch_opcode_lean)
```

Complete: False
Why incomplete?

- no Lean type in Sail's output is opaque; 75 OPERATIONS are (declared with no body)
- of those, 67 are float: 27 have a body from the universal type, 40 do not
- the other 8 are platform (terminal read and write, the atomic reservation, random bits, an experimental-extensions flag)
- no proved bridge yet from Sail's own operations to the universal type: 1 proved (truncation = the kinds' wrap)
- containers (vectors, memory) are not covered: the universal type is one element

### 2. every language's compiler-operators, lowered to arch-units, in Lean

```python
for lang in langs:
 for compiler_operator in lang.compiler_operators:
 arch_unit = lower(compiler_operator) # compile for RISC-V
 arch_unit.lean = build_unit_lean(arch_unit, arch_opcode_leans)
 arch_unit.kinds = discover_kinds(arch_unit.lean) # kinds read off the Lean, not written by hand
```

Complete: False

### 3. the primitives: which arch-units equal which pieces of Sail's definitions

```python
sail_lean_primitives = pieces_of(arch_opcode_leans) # a + b, a xor b, the 32-bit add, ...
for lang in langs:
 for primitive in sail_lean_primitives:
 for arch_unit in lang.arch_units:
 if prove_lean_equivalence(primitive, arch_unit.lean):
 lang.arch_unit_lean_primitives[primitive] = arch_unit
```

Complete: False

### 4. every arch-opcode emulated in every language, from those primitives only

```python
for lang in langs:
 for arch_opcode, definition in arch_opcode_leans.items():
 emulation = build_emulation(definition, lang.arch_unit_lean_primitives)
 arch_unit = lower(emulation)
 arch_unit.lean = build_unit_lean(arch_unit, arch_opcode_leans)
 emulation.proven = prove_lean_equivalence(definition, arch_unit.lean)
```

Complete: False

### 5. any language's arch-unit expressed in any other language's

```python
for lang_i in langs:
 for lang_j in langs:
 for arch_unit_i in lang_i.arch_units:
 for arch_unit_j in lang_j.arch_units:
 if prove_lean_equivalence(arch_unit_i.lean, arch_unit_j.lean):
 equivalents.add(arch_unit_i, arch_unit_j)
```

Complete: False
