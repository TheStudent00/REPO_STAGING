#!/usr/bin/env bash
# t95 lane 2 -- RECONNAISSANCE ONLY, the rerun of lane 1.
#
# Node: hq.research.compiler_graph.graph, the heading "the
# arch-opcode-node -- a shape this node lacks, added 2026-09-05".
#
# The question this lane answers, and ONLY this question: WHERE, in each
# of the four regions we have a graph for, does the compiler's own source
# emit a machine instruction?  The heading names go's emitter and gives
# clang's neighbourhood; rust and swift must be LOCATED from source, and
# if one cannot be located the region is reported UNMEASURED rather than
# approximated.
#
# Every file is read FROM THE PIN with `git show`, never from the working
# tree, exactly as graph.py's own build does -- all four checkouts sit at
# a different commit than their region pin.
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
# An ARCH OPCODE (MOVQ, ADDQ) is machine form and is a legitimate key.
# An OPERATOR TOKEN is not.  This lane keys by nothing at all: it counts
# lines and prints them.
set -u
say() { echo; echo "======== $* ========"; }
CG=PseudoCoupHQ/Research/compiler_graph
GR=PseudoCoupGraphs
GO=/sources/golang_src
LLVM=/sources/llvm-project
RUST=/sources/rust
SWIFT=/sources/swift-6.0.3-RELEASE
# WHY HOME IS REDIRECTED.  graph.py resolves its source checkouts as
# `Path.home() / "Programming" / "Sources"` (graph.py line 124), which on
# the host is the folder Airlock mounts at /sources.  Inside the container
# HOME is /root, so that path does not exist and lane 1 raised
# FileNotFoundError on every region.  graph.py is NOT edited for this: a
# lane-local HOME with one symlink makes the SAME path resolve to the SAME
# read-only mount, so the region rule and the pin reads are unchanged.
export HOME=/work/t95home
mkdir -p "$HOME/Programming"
ln -sfn /sources "$HOME/Programming/Sources"
cd "$CG"

say "[1/9] the instance, the mounts, and the memory bound"
python3 -c "import sys;print('   python',sys.version.split()[0])"
echo "   MEMORY BOUND for task 95: 6144 MB, refusal named MemoryCeilingReached."
ls -d "$GR" "$GO" "$LLVM" "$RUST" "$SWIFT" 2>&1 | sed 's/^/   /'
touch "$GR/.t95_write_probe" && echo "   graphs mount write probe OK" && rm -f "$GR/.t95_write_probe"
for r in "$GO" "$LLVM" "$RUST" "$SWIFT"; do
  echo "   $r head: $(git -C "$r" rev-parse HEAD 2>&1 | head -c 40)"
done

say "[2/9] MEMORY SAMPLE -- holding each compact graph whole"
python3 - <<'PY'
import json, os, resource, sys
sys.path.insert(0, "PseudoCoupHQ/Research/compiler_graph")
import graphs_home
CEILING_MB = 6144
for name in ("graph_go.json", "graph_cpp.json", "graph_rust.json",
             "graph_swift.json"):
    p = graphs_home.path(name)
    doc = json.load(open(p))
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    print("   %-18s %11d bytes on disk  nodes %7d  strings %7d  peak RSS %8.1f MB"
          % (name, os.path.getsize(p), doc["counts"]["nodes"],
             len(doc["strings"]), peak))
    if peak > CEILING_MB:
        raise SystemExit("MemoryCeilingReached")
    del doc
print("   peak resident set, all four held one after another: %.1f MB"
      % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
print("   graphs home: %s (%s)" % (graphs_home.home(), graphs_home.where_from()))
PY

say "[3/9] go -- every function in the region with a parameter of the ARCH OPCODE TYPE obj.As"
python3 - <<'PY'
import re, sys
sys.path.insert(0, "PseudoCoupHQ/Research/compiler_graph")
import graph as G
region = G.REGIONS["go"]
files = G.list_region_files(region)
print("   region files: %d" % len(files))
hits = 0
for rel in files:
    if not rel.endswith(".go"):
        continue
    text = G.show_file(region.repository, region.pin, rel)
    for n, line in enumerate(text.splitlines(), 1):
        if re.search(r"^func .*\bobj\.As\b", line):
            hits += 1
            print("   %s:%d  %s" % (rel, n, line.strip()))
print("   functions taking obj.As, declared inside the region: %d" % hits)
PY

say "[4/9] go -- call sites of the emitter, and the shape of the first argument"
python3 - <<'PY'
import re, sys, collections
sys.path.insert(0, "PseudoCoupHQ/Research/compiler_graph")
import graph as G
region = G.REGIONS["go"]
files = [f for f in G.list_region_files(region) if f.endswith(".go")]
CALL = re.compile(r"\b([A-Za-z_][A-Za-z0-9_.]*)\.Prog\(")
per_receiver = collections.Counter()
sites = []
for rel in files:
    text = G.show_file(region.repository, region.pin, rel)
    for n, line in enumerate(text.splitlines(), 1):
        for m in CALL.finditer(line):
            per_receiver[m.group(1)] += 1
            arg = line[m.end():]
            sites.append((rel, n, m.group(1), arg.split(")")[0].strip()))
print("   .Prog( call sites in the region, by receiver expression:")
for k, v in per_receiver.most_common():
    print("      %-24s %d" % (k, v))
print("   total .Prog( call sites: %d" % len(sites))
const = [s for s in sites if re.match(r"^[a-z0-9]+\.A[A-Z0-9_]+$", s[3])]
print("   first argument is a package-qualified opcode constant: %d" % len(const))
names = collections.Counter(s[3] for s in const)
print("   distinct such constants: %d" % len(names))
for k, v in sorted(names.items()):
    print("      %-22s %d" % (k, v))
other = collections.Counter(s[3] for s in sites if s not in const)
print("   every OTHER first-argument spelling, with its count:")
for k, v in other.most_common():
    print("      %-40s %d" % (k[:40], v))
PY

say "[5/9] go -- the static hop: the generated op table"
git -C "$GO" ls-tree -r --name-only 9f1012d9a1aa0831ff44ac9c767e96f9943d13fe src/cmd/compile/internal/ssa | grep -E "opGen|op\.go$" | sed 's/^/   /'
echo "   --- func (op Op) Asm() ---"
git -C "$GO" show 9f1012d9a1aa0831ff44ac9c767e96f9943d13fe:src/cmd/compile/internal/ssa/op.go | grep -n "Asm()" | head -20 | sed 's/^/   /'
echo "   --- opGen.go: how many rows carry an asm field, and how many distinct ---"
git -C "$GO" show 9f1012d9a1aa0831ff44ac9c767e96f9943d13fe:src/cmd/compile/internal/ssa/opGen.go \
  | grep -cE "^\s+asm:\s+" | sed 's/^/   rows with an asm field: /'
git -C "$GO" show 9f1012d9a1aa0831ff44ac9c767e96f9943d13fe:src/cmd/compile/internal/ssa/opGen.go \
  | grep -oE "^\s+asm:\s+[a-z0-9]+\.A[A-Za-z0-9_]+" | awk '{print $2}' | sort -u | wc -l \
  | sed 's/^/   distinct asm values: /'
git -C "$GO" show 9f1012d9a1aa0831ff44ac9c767e96f9943d13fe:src/cmd/compile/internal/ssa/opGen.go \
  | grep -oE "^\s+asm:\s+x86\.A[A-Za-z0-9_]+" | awk '{print $2}' | sort -u | wc -l \
  | sed 's/^/   distinct x86 asm values: /'
echo "   --- is opGen.go inside the graph region? ---"
git -C "$GO" show 9f1012d9a1aa0831ff44ac9c767e96f9943d13fe:src/cmd/compile/internal/ssa/opGen.go | head -3 | sed 's/^/   /'

say "[6/9] cpp -- where the X86 backend actually builds a machine instruction"
python3 - <<'PY'
import re, sys, collections
sys.path.insert(0, "PseudoCoupHQ/Research/compiler_graph")
import graph as G
region = G.REGIONS["cpp"]
files = G.list_region_files(region)
by_ext = collections.Counter(f.rsplit(".", 1)[-1] for f in files)
print("   region files: %d  %s" % (len(files), dict(by_ext)))
pats = {
    "BuildMI(": re.compile(r"\bBuildMI\s*\("),
    "TII->get(": re.compile(r"\bTII->get\s*\("),
    "TII.get(": re.compile(r"\bTII\.get\s*\("),
    "setOpcode(": re.compile(r"\.setOpcode\s*\("),
    "MCInstBuilder(": re.compile(r"\bMCInstBuilder\s*\("),
    "X86:: token": re.compile(r"\bX86::[A-Z][A-Za-z0-9_]*"),
}
counts = collections.Counter()
per_file = collections.defaultdict(collections.Counter)
for rel in files:
    if rel.endswith(".td"):
        continue
    text = G.show_file(region.repository, region.pin, rel)
    for name, pat in pats.items():
        n = len(pat.findall(text))
        if n:
            counts[name] += n
            per_file[name][rel] += n
for name, n in counts.most_common():
    print("   %-18s %6d occurrences, in %d files" % (name, n, len(per_file[name])))
for name in ("BuildMI(", "TII->get("):
    print("   top files for %s:" % name)
    for f, n in per_file[name].most_common(12):
        print("      %-70s %d" % (f, n))
PY

say "[7/9] cpp -- the instruction table the region already keeps (.td)"
python3 - <<'PY'
import re, sys, collections
sys.path.insert(0, "PseudoCoupHQ/Research/compiler_graph")
import graph as G
region = G.REGIONS["cpp"]
files = [f for f in G.list_region_files(region) if f.endswith(".td")]
print("   .td files in the region: %d" % len(files))
DEF = re.compile(r"^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*[:<]")
names = set()
for rel in files:
    text = G.show_file(region.repository, region.pin, rel)
    for line in text.splitlines():
        m = DEF.match(line)
        if m:
            names.add(m.group(1))
print("   distinct `def <name>` records across those .td files: %d" % len(names))
PY

say "[8/9] rust -- LOCATE the emitter, or report there is none in the region"
python3 - <<'PY'
import re, sys, collections
sys.path.insert(0, "PseudoCoupHQ/Research/compiler_graph")
import graph as G
region = G.REGIONS["rust"]
files = G.list_region_files(region)
print("   region files: %d  directories declared: %s" % (len(files), list(region.directories)))
pats = {
    "an x86 mnemonic spelled in source": re.compile(r"\"(mov|add|sub|lea|push|pop|ret|call|jmp|xor|cmp|test)[a-z]{0,2}\b"),
    "inline asm template": re.compile(r"\basm!|InlineAsm|inline_asm|InlineAsmOperand"),
    "llvm builder": re.compile(r"\bllvm::|LLVMBuild[A-Za-z]+"),
    "codegen_llvm builder method": re.compile(r"\bself\.(call|add|sub|mul|load|store)\b"),
    "naked asm": re.compile(r"naked_asm|global_asm"),
}
counts = collections.Counter(); per_file = collections.defaultdict(collections.Counter)
for rel in files:
    text = G.show_file(region.repository, region.pin, rel)
    for name, pat in pats.items():
        n = len(pat.findall(text))
        if n:
            counts[name] += n; per_file[name][rel] += n
for name, n in counts.most_common():
    print("   %-38s %6d occurrences in %d files" % (name, n, len(per_file[name])))
    for f, k in per_file[name].most_common(6):
        print("        %-64s %d" % (f, k))
PY

say "[9/9] swift -- LOCATE the emitter, or report there is none in the region"
python3 - <<'PY'
import re, sys, collections
sys.path.insert(0, "PseudoCoupHQ/Research/compiler_graph")
import graph as G
region = G.REGIONS["swift"]
files = G.list_region_files(region)
print("   region files: %d  directories declared: %s" % (len(files), list(region.directories)))
pats = {
    "BuildMI(": re.compile(r"\bBuildMI\s*\("),
    "X86:: token": re.compile(r"\bX86::[A-Z][A-Za-z0-9_]*"),
    "MCInst": re.compile(r"\bMCInst\b"),
    "llvm IRBuilder": re.compile(r"\bIRBuilder\b|\bBuilder\.Create[A-Za-z]+"),
    "inline asm": re.compile(r"\bInlineAsm\b|createInlineAsm|asm_"),
}
counts = collections.Counter(); per_file = collections.defaultdict(collections.Counter)
for rel in files:
    text = G.show_file(region.repository, region.pin, rel)
    for name, pat in pats.items():
        n = len(pat.findall(text))
        if n:
            counts[name] += n; per_file[name][rel] += n
for name, n in counts.most_common():
    print("   %-38s %6d occurrences in %d files" % (name, n, len(per_file[name])))
    for f, k in per_file[name].most_common(6):
        print("        %-64s %d" % (f, k))
PY

say "lane 1 done"
