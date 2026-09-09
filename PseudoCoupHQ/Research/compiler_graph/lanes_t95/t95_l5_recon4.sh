#!/usr/bin/env bash
# t95 lane 5 -- RECONNAISSANCE, the last two facts.  Nothing is written.
#
# Node: hq.research.compiler_graph.graph, heading "the arch-opcode-node".
#
# Lane 4 turned up ONE genuine surprise: the swift region does spell a
# machine instruction, in an inline-assembly template it writes itself --
# `llvm::InlineAsm::get(AsmFnTy, "nop", "", true)` at
# lib/IRGen/IRGenSIL.cpp:5578.  Three other sites hand over an EMPTY
# template (a barrier, no instruction), and one hands over a variable
# `asmString` whose value has to be read before it can be graded.  This
# lane prints those bodies.
#
# It also answers whether the pseudo-opcode table LLVM shares across all
# targets (TargetOpcodes.def) is readable at the region's own pin, so
# X86::COPY and X86::PHI can be separated from real machine instructions
# by READING a table rather than by recognising names.
#
# THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
# second violation). No operator token may appear in ANY key, grouping,
# pairing, row structure, candidate selection, or comparison scope,
# anywhere in this line -- not in matching, not in "which pairs get
# compared", not in report rows, not in dropdowns. The candidate set for
# comparison comes from machine-form evidence (clusters, connections,
# type pairs) or from ratified intention -- never from the token. The
# token appears exactly once per unit: as a display label on the member.
# HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
# campaign's cross-language matrix (caught by the owner 2026-08-24);
# (2) verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix
# brief itself reintroduced it as "same-operator pairs"). MECHANICAL
# GUARD REQUIRED: every pipeline stage that groups or pairs units must
# run the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
# refuse its own output on failure.
set -u
say() { echo; echo "======== $* ========"; }
export HOME=/work/t95home
mkdir -p "$HOME/Programming"
ln -sfn /sources "$HOME/Programming/Sources"
cd /projects/PseudoCoupHQ/Research/compiler_graph

say "[1/4] swift -- the five inline-asm sites, printed with their context"
python3 - <<'PY'
import sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graph as G
region = G.REGIONS["swift"]
for rel, a, b in (("lib/IRGen/GenObjC.cpp", 100, 150),
                  ("lib/IRGen/IRGenSIL.cpp", 5565, 5585),
                  ("lib/IRGen/IRGenSIL.cpp", 745, 760),
                  ("lib/IRGen/GenDecl.cpp", 2018, 2038),
                  ("lib/IRGen/IRGenFunction.cpp", 450, 470)):
    text = G.show_file(region.repository, region.pin, rel).splitlines()
    print("   ---- %s:%d-%d ----" % (rel, a, b))
    for n in range(a, min(b, len(text)) + 1):
        print("   %6d  %s" % (n, text[n - 1]))
PY

say "[2/4] swift -- where does GenObjC's asmString come from"
python3 - <<'PY'
import re, sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graph as G
region = G.REGIONS["swift"]
for rel in ("lib/IRGen/GenObjC.cpp",):
    text = G.show_file(region.repository, region.pin, rel)
    for n, line in enumerate(text.splitlines(), 1):
        if re.search(r"asmString|markerKey|Triple|getArch", line):
            print("   %s:%d  %s" % (rel, n, line.strip()[:140]))
PY

say "[3/4] llvm -- is the shared pseudo-opcode table readable at the region pin"
python3 - <<'PY'
import re, sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graph as G
region = G.REGIONS["cpp"]
for rel in ("llvm/include/llvm/CodeGen/TargetOpcodes.def",
            "llvm/include/llvm/Support/TargetOpcodes.def"):
    try:
        text = G.show_file(region.repository, region.pin, rel)
    except Exception as exc:
        print("   %s  ABSENT (%s)" % (rel, type(exc).__name__))
        continue
    names = re.findall(r"^HANDLE_TARGET_OPCODE\w*\(\s*([A-Za-z_][A-Za-z0-9_]*)",
                       text, re.M)
    print("   %s  PRESENT, %d pseudo-opcode names" % (rel, len(names)))
    print("   the first 30: %s" % " ".join(names[:30]))
PY

say "[4/4] cpp -- the in-region opcode-returning helpers the hop must follow"
python3 - <<'PY'
import re, sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graph as G
region = G.REGIONS["cpp"]
files = [f for f in G.list_region_files(region) if not f.endswith(".td")]
wanted = ("getMOVriOpcode", "getPUSHOpcode", "getPOPOpcode", "getSubOpcode",
          "getLEArOpcode", "getSUBrrOpcode", "getPUSH2Opcode",
          "getPOP2Opcode", "getSUBriOpcode", "getConcreteOpcode",
          "GET_EGPR_IF_ENABLED")
for rel in files:
    text = G.show_file(region.repository, region.pin, rel)
    lines = text.splitlines()
    for n, line in enumerate(lines, 1):
        for w in wanted:
            if re.search(r"(^|[^A-Za-z0-9_])%s\s*\(" % w, line) and \
               (re.match(r"^\s*(static\s+|inline\s+|unsigned|#define)", line)
                    or "static unsigned" in line):
                print("   ---- %s  %s:%d ----" % (w, rel, n))
                for k in range(n - 1, min(n + 24, len(lines))):
                    print("   %6d  %s" % (k + 1, lines[k]))
                break
PY

say "lane 5 done"
