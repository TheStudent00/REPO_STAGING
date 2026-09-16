### 1. RISC-V instructions in Lean, from Sail

```python
arch_opcode_leans = {}
for arch_opcode in sail_riscv_model:
 arch_opcode_leans[arch_opcode] = get_sail_def(arch_opcode, output="Lean")
 # every number inside is the universal type (sign, mant, expo),
 # constrained to a kind: unsigned n, signed n, bool, float (e, m), fixed
```

### 2. every language's compiler-operators, lowered to arch-units, in Lean

```python
for lang in langs:
 for compiler_operator in lang.compiler_operators:
 arch_unit = lower(compiler_operator) # compile for RISC-V
 arch_unit.lean = build_unit_lean(arch_unit, arch_opcode_leans)
 arch_unit.kinds = discover_kinds(arch_unit.lean) # kinds read off the Lean, not written by hand
```

### 3. the primitives: which arch-units equal which pieces of Sail's definitions

```python
sail_lean_primitives = pieces_of(arch_opcode_leans) # a + b, a xor b, the 32-bit add, ...
for lang in langs:
 for primitive in sail_lean_primitives:
 for arch_unit in lang.arch_units:
 if prove_lean_equivalence(primitive, arch_unit.lean):
 lang.arch_unit_lean_primitives[primitive] = arch_unit
```

### 4. every arch-opcode emulated in every language, from those primitives only

```python
for lang in langs:
 for arch_opcode, definition in arch_opcode_leans.items():
 emulation = build_emulation(definition, lang.arch_unit_lean_primitives)
 arch_unit = lower(emulation)
 arch_unit.lean = build_unit_lean(arch_unit, arch_opcode_leans)
 emulation.proven = prove_lean_equivalence(definition, arch_unit.lean)
```

### 5. any language's arch-unit expressed in any other language's

```python
for lang_i in langs:
 for lang_j in langs:
 for arch_unit_i in lang_i.arch_units:
 for arch_unit_j in lang_j.arch_units:
 if prove_lean_equivalence(arch_unit_i.lean, arch_unit_j.lean):
 equivalents.add(arch_unit_i, arch_unit_j)
```
