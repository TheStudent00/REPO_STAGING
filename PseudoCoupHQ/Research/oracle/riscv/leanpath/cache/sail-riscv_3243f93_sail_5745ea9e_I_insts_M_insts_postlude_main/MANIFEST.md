# the cached emit: Sail's Lean output for the RISC-V model (second emit, sail built from source)

- model: `sail-riscv` commit 3243f93 (2026-09-09 21:47:21 +0000), the
  image's clone `/opt/sail-riscv-src`, config
  `build/config/rv64d_v256_e64.json`
- sail: Sail 0.20.2 (HEAD @ 5745ea9e5369ab4fc51de6f8b773dd8ebc323357), built from source in lane
  `lp1_l6_build_sail_from_source.sh` (branch `sail2`, the head before the
  model's own commit of 2026-09-09; the model's CI builds its Lean with
  sail "latest" by this recipe), Lean backend; the opam root is the copy
  `/persist/opam` on the tower instance `lp1`'s persistent volume
- modules handed to sail (LEAF names): `I_insts M_insts postlude main`,
  resolved to 91 source files, `base_insts.sail` and `mext_insts.sail`
  among them
- lane: `lp1_l7_emit_with_sail_5745ea9e.sh`, tower instance `lp1`,
  2026-09-13/14, 20 GB cap; the lane's own output is beside this file as
  `emit_lane.log`; the invocation is in log 274 §3, verbatim
- product: `LeanIM/*.lean`, 63066 lines; `execute_DIV` at
  `LeanIM/InstsEnd.lean:4386`; the lake project requires [[require]] name = "Sail" git = "https://github.com/rems-project/lean-sail" rev = "v5"  and toolchain
  `leanprover/lean4:v4.29.0` (`lean-toolchain`)
- the first emit (sail 0.20.2 from opam) is the co-folder
  `sail-riscv_3243f93_I_insts_M_insts_postlude_main/`, kept as the record
  of the build failure log 275 §4.2 flags; nothing in it is edited
- this folder is a BUILD PRODUCT, cached by the model commit, the sail
  commit and the module list in its name; the regeneration test deletes
  it and gets it back by running lanes 6 and 7. Nobody edits a file in it.
