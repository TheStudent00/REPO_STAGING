---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.language.compile
level: 7
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: compile
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_4_language/node_0_3_2_3_1_3_4_0_compile/CORE_0_3_2_3_1_3_4_0_compile.md
super_node:
    name: language
    path: ../CORE_0_3_2_3_1_3_4_language.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_4_0 — compile

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.language.compile
- **level:** 7
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [language](../CORE_0_3_2_3_1_3_4_language.md)

## sub_nodes

*(none yet)*

## definition

`compile(language, source) -> ArchUnit`

Input: source text of one function. Output: its `ArchUnit`, cut out of the binary at the function symbol.

Steps, in order:

1. write the source to a file; invoke the compiler for riscv64 at ship flags (c and c++: clang `--target=riscv64-linux-gnu --gcc-toolchain=/usr`; rust `--target riscv64gc-unknown-linux-gnu --emit=obj`; go `GOARCH=riscv64`)
2. cut the body out with `llvm-objdump --mattr=+m,+a,+f,+d,+c,+zba,+zbb,+zbs -M no-aliases` from the symbol to its return
3. return the unit with its encoded words; a compile failure is a refusal with the compiler's literal output
