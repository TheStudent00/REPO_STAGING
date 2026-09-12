#!/usr/bin/env python3
"""rv4: task t4's RISC-V driver, unchanged, with ONE difference — the
emulation is compiled with optimization OFF (the owner, 2026-09-11: "it doesn't
take an optimizer. it requires a system to fill in the logic"), so the
machine code follows the source statement by statement and the check
closes by structure. Same population, same render, same lifter, same gate
(the identical-text shortcut is rv_general's own).

    python3 rv4_o0.py run <ref_dir> <op_dir> <emulation_dir> <twins.json> <model_table_rv.json> <prefix> <src> <work> [limit]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rv_general as RG                                          # noqa: E402

RV_DIR = os.path.dirname(os.path.abspath(sys.argv[5]))            # the riscv folder
sys.path.insert(0, RV_DIR)
import inherit as INH                                            # noqa: E402  (the same module rv_general imports)

# c: -O1 -> -O0 ; rust: opt-level=1 -> 0 ; go: -gcflags=all=-N -l
INH.CARVE.SHIP["c"] = ["-O0" if f == "-O1" else f for f in INH.CARVE.SHIP["c"]]
INH.RUST_SHIP = ["opt-level=0" if f == "opt-level=1" else f for f in INH.RUST_SHIP]
_sh = INH.CARVE.sh
def _sh_o0(command, *a, **k):
    if command[:2] == ["go", "build"]:
        command = command[:2] + ["-gcflags=all=-N -l"] + command[2:]
    return _sh(command, *a, **k)
INH.CARVE.sh = _sh_o0
print("rv4: optimization OFF — c %s | rust %s | go build -gcflags=all=-N -l"
      % (" ".join(INH.CARVE.SHIP["c"]), " ".join(INH.RUST_SHIP)), flush=True)

if __name__ == "__main__":
    sys.exit(RG.main())
