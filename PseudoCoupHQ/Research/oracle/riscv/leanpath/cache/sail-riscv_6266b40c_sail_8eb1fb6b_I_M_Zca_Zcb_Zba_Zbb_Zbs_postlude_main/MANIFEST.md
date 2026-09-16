# the cached emit: Sail's Lean output for the RISC-V model, the green pair, with C and Zb

- model: `sail-riscv` commit `6266b40c1c` (2026-08-20, the last commit whose own Lean CI passed), clone at /persist/sail-riscv-6266b40c, config `build/config/rv64d_v256_e64.json`
- sail: built from source at `8eb1fb6b5b` (branch sail2, 2026-08-18, the head on that date), Lean backend
- modules handed to sail (LEAF names): `I_insts M_insts Zca Zcb Zba Zbb Zbs postlude main`, resolved to 96 source files
- lane: `lp1_l15_emit_with_zc_zb_and_build.sh`, tower instance `lp1`, 2026-09-14; the lane's log is beside this file as `emit_lane.log`
- product: `LeanIMZ/*.lean`; the lake project the backend wrote (`lakefile.toml`, `lean-toolchain`)
- a BUILD PRODUCT cached by the model commit, the sail commit and the module list in its name; nobody edits a file in it
