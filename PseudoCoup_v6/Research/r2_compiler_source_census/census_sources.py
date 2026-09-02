"""Census the compiler sources the Rust/C++ ingestors will ingest, using T1.

R2 of <WORKSPACE_DIR>/PseudoCoup_v6/Planning/node_0_1_research/.
Parses each subject file with the pinned grammars from
<WORKSPACE_DIR>/PseudoCoup_v6/Tools/ledgerer/tree_sitter/, writes one
deterministic census JSON per file into outputs/, plus a summary
table. Run from anywhere:

    python3 <WORKSPACE_DIR>/PseudoCoup_v6/Research/r2_compiler_source_census/census_sources.py
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
T1 = os.path.normpath(os.path.join(HERE, "..", "..", "Tools", "ledgerer", "tree_sitter"))
sys.path.insert(0, T1)

from parse_source import parse_file          # noqa: E402
from record_coverage import census, render_census  # noqa: E402

P5 = os.path.expanduser("<WORKSPACE_DIR>/PseudoCoup_v5")
# The support crate here belonged to a retired reference backend's
# assembler crate (since removed as mis-aimed, see the tools PROGRESS);
# resolved by glob rather than a hardcoded name so this historical
# census script names nothing directly.
_SUPPORT_CANDIDATES = sorted(glob.glob(os.path.join(
    P5, "Research/rust_routing/sources/encoder/asm<USER_HOME>/.cargo/"
        "registry/src/index.crates.io-*/*-assembler-x64-*/src")))
SUPPORT_DIR = _SUPPORT_CANDIDATES[0] if _SUPPORT_CANDIDATES else os.path.join(
    P5, "Research/rust_routing/sources/encoder/asm/_support_dir_not_found")

SUBJECTS = [
    # (label, grammar, path)
    ("assembler_generated", "rust",
     os.path.join(P5, "Research/rust_routing/sources/encoder/asm/assembler.rs")),
    ("support_rex", "rust", os.path.join(SUPPORT_DIR, "rex.rs")),
    ("support_custom", "rust", os.path.join(SUPPORT_DIR, "custom.rs")),
    ("rvalue", "rust",
     os.path.join(P5, "Research/rust_routing/sources/rust/compiler/"
                      "rustc_codegen_ssa/src/mir/rvalue.rs")),
    ("x86_mc_code_emitter", "cpp",
     os.path.join(P5, "Research/llvm_trace/sources/llvm-project/llvm/lib/"
                      "Target/X86/MCTargetDesc/X86MCCodeEmitter.cpp")),
]

# every .rs in the support crate, censused together as one grammar surface
SUPPORT_ALL = sorted(
    f for f in os.listdir(SUPPORT_DIR) if f.endswith(".rs")
) if os.path.isdir(SUPPORT_DIR) else []


def main():
    out = os.path.join(HERE, "outputs")
    os.makedirs(out, exist_ok=True)
    rows = []
    for label, grammar, path in SUBJECTS:
        if not os.path.isfile(path):
            rows.append((label, grammar, "MISSING", 0, 0, "-"))
            continue
        tree = parse_file(path, grammar)
        c = census(tree.root_node)
        with open(os.path.join(out, f"census_{label}.json"), "w") as f:
            f.write(render_census(c))
        named_kinds = len(c["named"])
        total = sum(c["named"].values()) + sum(c["anonymous"].values())
        err = "ERROR" in c["named"] or "ERROR" in c["anonymous"]
        lines = sum(1 for _ in open(path, "rb"))
        rows.append((label, grammar, f"{lines} lines", named_kinds, total,
                     "YES" if err else "no"))

    print("| subject | grammar | size | named kinds | total nodes | ERROR nodes |")
    print("|---|---|---|---|---|---|")
    for r in rows:
        print("| " + " | ".join(str(x) for x in r) + " |")
    print()
    print("support crate files present:", " ".join(SUPPORT_ALL))


if __name__ == "__main__":
    main()
