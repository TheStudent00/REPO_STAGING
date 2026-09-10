#!/usr/bin/env bash
# hub1_l1_toolchain_probe.sh -- task hub1, lane 1 of the hub node.
# WHAT IT ASKS: which of the pieces Hub v1 needs are already in the image --
# tree-sitter's go grammar, the go toolchain (for the type oracle and for
# body A), clang and rustc (for body B), and z3 (for the gate). It writes
# nothing; it prints. A missing piece is a STOP for the brief, not an install.
set -uo pipefail
total=6
echo "[1/$total] python, z3, resource"
python3 - <<'PY'
import sys, resource
print("python", sys.version.split()[0])
try:
    import z3
    print("z3", z3.get_version_string())
except Exception as exc:
    print("z3 ABSENT:", exc)
print("peak kB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

echo "[2/$total] tree-sitter runtime and the grammars installed"
python3 - <<'PY'
import importlib
try:
    import tree_sitter
    print("tree_sitter", getattr(tree_sitter, "__version__", "?"))
except Exception as exc:
    print("tree_sitter ABSENT:", exc)
for name in ["tree_sitter_go", "tree_sitter_c", "tree_sitter_rust",
             "tree_sitter_cpp", "tree_sitter_python"]:
    try:
        mod = importlib.import_module(name)
        print(name, "PRESENT", getattr(mod, "__version__", "?"))
    except Exception as exc:
        print(name, "ABSENT:", type(exc).__name__)
PY

echo "[3/$total] the go toolchain"
which go && go version || echo "go ABSENT"
echo "GOROOT: $(go env GOROOT 2>/dev/null || echo none)"

echo "[4/$total] clang and rustc, and the ship flags of record"
which clang && clang --version | head -1 || echo "clang ABSENT"
which rustc && rustc --version || echo "rustc ABSENT"
ls -d /persist/swift 2>/dev/null && echo "persist swift present" || echo "no /persist/swift"

echo "[5/$total] the artifact folder and the stores this task reads"
ls -d PseudoCoupHQ/Research/oracle/hub || echo "no hub folder"
for f in PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5_runs.jsonl \
         PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.json \
         PseudoCoupHQ/Research/op_pipeline/probe_manifest_go.json \
         PseudoCoupHQ/Research/op_pipeline/probe_manifest2_go.json \
         PseudoCoupHQ/Research/op_pipeline/canon40_wrapped_go.json ; do
    if [ -f "$f" ]; then echo "OK   $f"; else echo "MISS $f"; fi
done
ls PseudoCoupHQ/Research/op_pipeline/canon40_regen_store/op_units2_go_*.json | wc -l

echo "[6/$total] a go build of one probe source, end to end, at the corpus ship flags"
grep -n "compile_probe" -A 30 PseudoCoupHQ/Research/op_pipeline/lane_gen.py | sed -n '1,60p'
