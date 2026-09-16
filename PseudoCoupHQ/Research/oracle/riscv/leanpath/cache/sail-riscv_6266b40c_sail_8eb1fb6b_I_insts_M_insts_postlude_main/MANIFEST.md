# the cached emit: Sail's Lean output for the RISC-V model (third emit: the last pair the model's own Lean CI built green)

- model: `sail-riscv` commit 6266b40c (2026-08-20 15:26:43 +0000), the clone
  `/persist/sail-riscv-6266b40c` on the tower instance `lp1`'s persistent
  volume (lane `lp1_l10_clone_last_green_model_and_build_sail_8eb1fb6b.sh`),
  the model's last commit whose Lean workflow (`compile-lean.yml`) ran
  green (2026-08-20T16:29Z, measured through the GitHub API on
  2026-09-13 by the coordinator); config
  `build/config/rv64d_v256_e64.json` produced by that clone's own
  `config/CMakeLists.txt` (lane `lp1_l10b_cmake_configure_without_asio.sh`,
  cmake with the model's own `-DDOWNLOAD_ASIO=OFF`; sha256 a3b545eb174247f5552a27dbb60f32c4ee95af85bdc8ea92ce0661254fbff674)
- sail: Sail 0.20.2 (HEAD @ 8eb1fb6b5bf9f18c0f89f71e94ff0c5894acd7c1), built from source in lane
  `lp1_l10_clone_last_green_model_and_build_sail_8eb1fb6b.sh` (branch
  `sail2`, the head on 2026-08-20; the model's CI builds its Lean with
  sail "latest" by this recipe), Lean backend; the opam root is the copy
  `/persist/opam` on the tower instance `lp1`'s persistent volume
- modules handed to sail (LEAF names): `I_insts M_insts postlude main`,
  resolved to 89 source files, `base_insts.sail` and `mext_insts.sail`
  among them
- lane: `lp1_l11_emit_6266b40c_with_sail_8eb1fb6b.sh`, tower instance
  `lp1`, 2026-09-14, 20 GB cap; the lane's own output is beside this file
  as `emit_lane.log`; the invocation is in log 274 §3, verbatim but for
  the clone's two paths
- product: `LeanIM/*.lean`, 57270 lines; `execute_DIV` at
  `LeanIM/InstsEnd.lean:4325`; the lake project requires [[require]] name = "Sail" git = "https://github.com/rems-project/lean-sail" rev = "v5"  and toolchain
  `leanprover/lean4:v4.29.0` (`lean-toolchain`)
- the two earlier emits are the co-folders
  `sail-riscv_3243f93_I_insts_M_insts_postlude_main/` (sail 0.20.2 from
  opam; log 275 §4.2) and
  `sail-riscv_3243f93_sail_5745ea9e_I_insts_M_insts_postlude_main/` (sail
  built at 5745ea9e; log 276 §4.1), kept as the records of the two build
  failures; nothing in them is edited
- this folder is a BUILD PRODUCT, cached by the model commit, the sail
  commit and the module list in its name; the regeneration test deletes
  it and gets it back by running lanes 10, 10b and 11. Nobody edits a
  file in it.
