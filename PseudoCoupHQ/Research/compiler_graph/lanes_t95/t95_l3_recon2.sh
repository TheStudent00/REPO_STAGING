#!/usr/bin/env bash
# t95 lane 3 -- RECONNAISSANCE, second pass.  Nothing is written.
#
# Node: hq.research.compiler_graph.graph, heading "the arch-opcode-node".
#
# Lane 2 established:
#   go   -- 7 functions in the region take the ARCH OPCODE TYPE obj.As;
#           205 `.Prog(` call sites; 67 pass a package-qualified constant
#           (50 of them x86.A*, 24 distinct -- which is the coordinator's
#           own count exactly, the other 17 being obj.A* pseudo-ops).
#   cpp  -- 724 BuildMI(, 395 TII->get(, 334 TII.get(, 53 MCInstBuilder(,
#           36 .setOpcode(, 14,331 X86:: tokens, 61 .td files carrying
#           7,227 `def <name>` records.
#   rust -- 0 BuildMI, 0 X86::.  Only LLVM builder calls and inline-asm
#           handling.
#   swift-- 0 BuildMI, 0 X86::.  Only llvm IRBuilder calls.
#
# This lane asks the three questions those counts raise:
#   A. cpp: for each instruction-building call site, WHAT is the opcode
#      argument, and does it carry a token that is a `def` in the region's
#      own .td instruction table?
#   B. rust and swift: is there an arch-opcode emitter ANYWHERE in the
#      repository, and if so, is it inside the region or outside it?  A
#      negative has to be measured over the whole checkout, not assumed
#      from a region grep.
#   C. go: what do the non-constant call sites hand over, exactly, so the
#      static hop can be defined instead of guessed.
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
#
# An ARCH OPCODE (MOVQ, ADDQ) is machine form and a legitimate key.  An
# OPERATOR TOKEN is not.  This lane keys by arch opcodes and by file
# coordinates only.
set -u
say() { echo; echo "======== $* ========"; }
CG=/projects/PseudoCoupHQ/Research/compiler_graph
export HOME=/work/t95home
mkdir -p "$HOME/Programming"
ln -sfn /sources "$HOME/Programming/Sources"
cd "$CG"

say "[1/6] go -- the seven obj.As functions, printed whole, so the hop is read not guessed"
python3 - <<'PY'
import sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graph as G
region = G.REGIONS["go"]
wanted = {
    "src/cmd/compile/internal/amd64/ssa.go": [(67, 100), (83, 116), (121, 172), (175, 182)],
    "src/cmd/compile/internal/ssagen/ssa.go": [(6742, 6790)],
    "src/cmd/compile/internal/ssa/opGen.go": [(115430, 115440)],
}
for rel, spans in wanted.items():
    text = G.show_file(region.repository, region.pin, rel).splitlines()
    for a, b in spans:
        print("   ---- %s:%d-%d ----" % (rel, a, b))
        for n in range(a, min(b, len(text)) + 1):
            print("   %6d  %s" % (n, text[n - 1]))
PY

say "[2/6] go -- what opGen.go's opcodeTable actually holds for the amd64 ops"
python3 - <<'PY'
import re, sys, collections
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graph as G
region = G.REGIONS["go"]
text = G.show_file(region.repository, region.pin,
                   "src/cmd/compile/internal/ssa/opGen.go")
rows = re.findall(r"\{\s*name:\s*\"([A-Za-z0-9_]+)\",(.*?)\n\t\},", text, re.S)
print("   opcodeTable rows parsed: %d" % len(rows))
amd = collections.Counter()
allasm = collections.Counter()
for name, body in rows:
    m = re.search(r"asm:\s+([a-z0-9]+)\.A([A-Za-z0-9_]+)", body)
    if not m:
        continue
    allasm[m.group(1)] += 1
    if m.group(1) == "x86":
        amd[m.group(2)] += 1
print("   rows with an asm field, by opcode package: %s" % dict(allasm))
print("   distinct x86 arch opcodes reachable through .Asm(): %d" % len(amd))
print("   the first 24 of them, alphabetically: %s"
      % " ".join(sorted(amd)[:24]))
PY

say "[3/6] cpp -- every instruction-building call site, and its opcode argument"
python3 - <<'PY'
import re, sys, collections
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graph as G

region = G.REGIONS["cpp"]
files = G.list_region_files(region)
td = [f for f in files if f.endswith(".td")]
code = [f for f in files if not f.endswith(".td")]

DEF = re.compile(r"^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*[:<]")
table = set()
for rel in td:
    for line in G.show_file(region.repository, region.pin, rel).splitlines():
        m = DEF.match(line)
        if m:
            table.add(m.group(1))
print("   .td instruction-table records: %d" % len(table))

OPENERS = ("BuildMI", "MCInstBuilder")
TOKEN = re.compile(r"\bX86::([A-Za-z_][A-Za-z0-9_]*)")

def call_text(text, start):
    """the balanced (...) that follows position `start`."""
    i = text.find("(", start)
    if i < 0:
        return None, start + 1
    depth = 0
    j = i
    while j < len(text):
        if text[j] == "(":
            depth += 1
        elif text[j] == ")":
            depth -= 1
            if depth == 0:
                return text[i + 1:j], j
        j += 1
    return None, len(text)

sites = 0
with_table_token = 0
with_other_token = 0
without_token = 0
opcodes = collections.Counter()
non_table = collections.Counter()
argshape = collections.Counter()
per_opener = collections.Counter()
for rel in code:
    text = G.show_file(region.repository, region.pin, rel)
    for opener in OPENERS:
        for m in re.finditer(r"\b%s\s*\(" % opener, text):
            body, _ = call_text(text, m.start())
            if body is None:
                continue
            sites += 1
            per_opener[opener] += 1
            names = TOKEN.findall(body)
            intable = [n for n in names if n in table]
            if intable:
                with_table_token += 1
                for n in intable:
                    opcodes[n] += 1
            elif names:
                with_other_token += 1
                for n in names:
                    non_table[n] += 1
            else:
                without_token += 1
                inner = re.search(r"(?:TII[.>-]*get|get)\s*\(([^()]*)\)", body)
                argshape[(inner.group(1).strip() if inner else body.strip()[:38])[:38]] += 1
    for m in re.finditer(r"\.setOpcode\s*\(", text):
        body, _ = call_text(text, m.start())
        if body is None:
            continue
        sites += 1
        per_opener["setOpcode"] += 1
        names = TOKEN.findall(body)
        intable = [n for n in names if n in table]
        if intable:
            with_table_token += 1
            for n in intable:
                opcodes[n] += 1
        elif names:
            with_other_token += 1
            for n in names:
                non_table[n] += 1
        else:
            without_token += 1
            argshape[body.strip()[:38]] += 1

print("   instruction-building call sites: %d  %s" % (sites, dict(per_opener)))
print("   sites naming at least one token that IS a .td record:   %d" % with_table_token)
print("   sites naming an X86:: token that is NOT a .td record:    %d" % with_other_token)
print("   sites naming no X86:: token at all:                      %d" % without_token)
print("   distinct .td-backed opcodes named at those sites: %d" % len(opcodes))
print("   the twenty most frequent: %s"
      % " ".join("%s(%d)" % (k, v) for k, v in opcodes.most_common(20)))
print("   the twenty most frequent NON-table X86:: tokens: %s"
      % " ".join("%s(%d)" % (k, v) for k, v in non_table.most_common(20)))
print("   the thirty most frequent opcode-argument spellings where no token appears:")
for k, v in argshape.most_common(30):
    print("      %-40s %d" % (k, v))
PY

say "[4/6] rust -- is there an arch-opcode emitter anywhere in the checkout"
echo "   --- what of the repository is materialised at all (promisor clone) ---"
ls /sources/rust 2>&1 | sed 's/^/   /'
ls /sources/rust/compiler 2>&1 | sed 's/^/   compiler\//'
echo "   --- BuildMI / MCInst / an instruction-table namespace, WHOLE checkout ---"
for pat in 'BuildMI(' 'MCInst' 'X86::' 'MachineInstr'; do
  n=$(grep -rl --include='*.rs' --include='*.cpp' --include='*.h' -F "$pat" /sources/rust 2>/dev/null | wc -l)
  echo "   files containing $pat : $n"
done
echo "   --- does an alternative backend that DOES emit machine code exist here ---"
ls -d /sources/rust/compiler/rustc_codegen_cranelift 2>&1 | sed 's/^/   /'
grep -rl --include='*.rs' -E '\bIns\b|MachInst|emit_inst|isa::x64' /sources/rust/compiler/rustc_codegen_cranelift 2>/dev/null | head -5 | sed 's/^/   /'
echo "   --- and is that backend inside the region? ---"
python3 -c "
import sys; sys.path.insert(0,'/projects/PseudoCoupHQ/Research/compiler_graph')
import graph as G
print('   region directories:', list(G.REGIONS['rust'].directories))
"

say "[5/6] swift -- is there an arch-opcode emitter anywhere in the checkout"
for pat in 'BuildMI(' 'MCInst' 'X86::' 'MachineInstr'; do
  n=$(grep -rl --include='*.cpp' --include='*.h' -F "$pat" /sources/swift-6.0.3-RELEASE 2>/dev/null | wc -l)
  echo "   files containing $pat : $n"
done
echo "   --- what the swift checkout contains at top level ---"
ls /sources/swift-6.0.3-RELEASE 2>&1 | head -30 | sed 's/^/   /'
echo "   --- the two swift trees on this disk ---"
ls -d /sources/swift /sources/swift-6.0.3-RELEASE 2>&1 | sed 's/^/   /'

say "[6/6] the graph's own def nodes -- do they carry an end line, in every region"
python3 - <<'PY'
import json, sys, collections
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graphs_home
for lang in ("go", "cpp", "rust", "swift"):
    doc = json.load(open(graphs_home.path("graph_%s.json" % lang)))
    schemas = doc["sections"]["nodes"]["schemas"]
    strings = [row["text"] for row in doc["strings"]]
    kinds = collections.Counter()
    withspan = collections.Counter()
    for row in doc["nodes"]:
        sch = schemas[row[0]]
        rec = {}
        for name, code, value in zip(sch["fields"], sch["codes"], row[1:]):
            rec[name] = strings[value] if (code == "s" and value is not None) else value
        kinds[rec.get("kind")] += 1
        if rec.get("kind") == "def":
            withspan["has end_line" if rec.get("end_line") is not None
                     else "no end_line"] += 1
    print("   %-6s nodes by kind %s   def spans %s"
          % (lang, dict(kinds), dict(withspan)))
    del doc
PY

say "lane 3 done"
