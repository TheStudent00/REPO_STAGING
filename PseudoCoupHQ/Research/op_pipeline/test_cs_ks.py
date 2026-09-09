import json
from fold_interp_cs import parse_ryujit
import os

HERE = "PseudoCoupHQ/Research/op_pipeline"
IN_FILE = os.path.join(HERE, "jit_out_csharp", "all_opt.txt")
with open(IN_FILE) as f:
    txt = f.read()

from keystone import Ks, KS_ARCH_X86, KS_MODE_64
ks = Ks(KS_ARCH_X86, KS_MODE_64)

for line in txt.split("\n"):
    if not line.strip() or line.startswith("G_M") or line.strip().startswith(";"):
        continue
    inst = line.strip()
    import re
    inst = re.sub(r"\[\(reloc\s+0x[0-9a-fA-F]+\)\]", "[0x0]", inst)
    try:
        ks.asm(inst)
    except Exception as e:
        print(f"Failed: {inst} -> {e}")

