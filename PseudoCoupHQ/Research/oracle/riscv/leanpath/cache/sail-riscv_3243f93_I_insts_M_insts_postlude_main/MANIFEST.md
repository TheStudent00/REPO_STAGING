# the cached emit: Sail's Lean output for the RISC-V model

- model: `sail-riscv` commit `3243f93` (2026-09-09 21:47:21 +0000), the
  image's clone `/opt/sail-riscv-src`, config
  `build/config/rv64d_v256_e64.json`
- sail: 0.20.2 (opam), Lean backend
- modules handed to sail (LEAF names): `I_insts M_insts postlude main`,
  resolved to 91 source files, `base_insts.sail` and `mext_insts.sail`
  among them
- lane: `sail0_l5_lean_I_insts_M_insts.sh`, tower instance `sail0`,
  2026-09-13, 45.5 minutes, 20 GB cap; the lane's log is beside this
  file as `emit_lane.log`; the invocation is in log 274 §3
- product: `LeanIM/*.lean`, 62,893 lines; `execute_DIV` at
  `LeanIM/InstsEnd.lean:4362`; the lake project requires `Sail` from
  `https://github.com/rems-project/lean-sail` rev `v4` and toolchain
  `leanprover/lean4:v4.29.0` (`lean-toolchain`)
- this folder is a BUILD PRODUCT, cached by the model commit and the
  module list in its name; the regeneration test deletes it and gets it
  back by running the emit lane. Nobody edits a file in it.
