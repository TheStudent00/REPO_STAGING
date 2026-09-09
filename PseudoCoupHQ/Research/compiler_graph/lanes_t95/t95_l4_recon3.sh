#!/usr/bin/env bash
# t95 lane 4 -- RECONNAISSANCE, third and last pass.  Nothing is written.
#
# Node: hq.research.compiler_graph.graph, heading "the arch-opcode-node".
#
# Lane 3 left exactly three things unsettled, and this lane settles each
# by MEASUREMENT so the pass can be written without a judgement call:
#
#   A. cpp -- lane 3 keyed on "any X86:: token anywhere in the call",
#      which is wrong twice over: it counted X86::EAX and X86::RAX, which
#      are REGISTERS, as opcodes; and it called 100 real instructions
#      "not a .td record" because X86's .td defines most instructions
#      through `defm` multiclasses, so a plain `def <name>` scan cannot
#      see them.  The fix is POSITIONAL: BuildMI's opcode argument is
#      whatever sits inside its `get(...)`, MCInstBuilder's is its first
#      argument, setOpcode's and setDesc's are their only argument.  This
#      lane extracts exactly that and reports what the argument IS.
#
#   B. rust and swift -- lane 3 measured ZERO occurrences of BuildMI,
#      MCInst, MachineInstr or an X86 namespace in either whole checkout.
#      Before that is reported as "no emitter in the region", the one
#      remaining way a compiler can put a named machine instruction into
#      its output has to be checked: an INLINE ASSEMBLY TEMPLATE the
#      compiler itself spells.  A template the USER's program supplies is
#      not the compiler producing an opcode; a fixed string the compiler
#      writes is.  This lane prints every string literal handed to an
#      inline-asm constructor in both regions so the difference is read
#      off the source rather than assumed.
#
#   C. the coverage summaries -- their shape, so the comparison against
#      what running the compiler showed can be made from the SMALL files
#      rather than from the 515 MB and 316 MB joins.
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
CG=PseudoCoupHQ/Research/compiler_graph
export HOME=/work/t95home
mkdir -p "$HOME/Programming"
ln -sfn /sources "$HOME/Programming/Sources"
cd "$CG"

say "[1/5] cpp -- the opcode argument, taken from its POSITION in the call"
python3 - <<'PY'
import re, sys, collections
sys.path.insert(0, "PseudoCoupHQ/Research/compiler_graph")
import graph as G

region = G.REGIONS["cpp"]
files = [f for f in G.list_region_files(region) if not f.endswith(".td")]

def balanced(text, i):
    """text[i] is '('; answer (inside, index of the matching ')')."""
    depth, j = 0, i
    while j < len(text):
        if text[j] == "(":
            depth += 1
        elif text[j] == ")":
            depth -= 1
            if depth == 0:
                return text[i + 1:j], j
        j += 1
    return None, len(text)

def top_level_split(body):
    out, depth, last = [], 0, 0
    for k, ch in enumerate(body):
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif ch == "," and depth == 0:
            out.append(body[last:k]); last = k + 1
    out.append(body[last:])
    return [p.strip() for p in out]

GETCALL = re.compile(r"(?:\bTII\s*(?:->|\.)\s*get|\bget)\s*\(")
opener_pats = {
    "BuildMI": re.compile(r"\bBuildMI\s*\("),
    "MCInstBuilder": re.compile(r"\bMCInstBuilder\s*\("),
    "setOpcode": re.compile(r"\.setOpcode\s*\("),
    "setDesc": re.compile(r"\.setDesc\s*\("),
}

shapes = collections.Counter()
per_opener = collections.Counter()
no_get = collections.Counter()
sites = 0
for rel in files:
    text = G.show_file(region.repository, region.pin, rel)
    for opener, pat in opener_pats.items():
        for m in pat.finditer(text):
            body, _ = balanced(text, text.index("(", m.start()))
            if body is None:
                continue
            sites += 1
            per_opener[opener] += 1
            if opener == "BuildMI" or opener == "setDesc":
                g = GETCALL.search(body)
                if not g:
                    no_get[opener] += 1
                    shapes["NO get(...) IN THE CALL"] += 1
                    continue
                arg, _ = balanced(body, body.index("(", g.start()))
                arg = " ".join((arg or "").split())
            else:
                arg = top_level_split(body)[0]
                arg = " ".join(arg.split())
            shapes[arg[:44]] += 1
print("   instruction-building call sites: %d  %s" % (sites, dict(per_opener)))
print("   BuildMI/setDesc calls carrying no get(...): %s" % dict(no_get))
arch = sum(v for k, v in shapes.items() if re.fullmatch(r"X86::[A-Za-z0-9_]+", k))
target = sum(v for k, v in shapes.items() if re.fullmatch(r"TargetOpcode::[A-Za-z0-9_]+", k))
call = sum(v for k, v in shapes.items() if ("(" in k and not k.startswith("X86::")))
print("   argument is exactly one X86:: token:            %d" % arch)
print("   argument is exactly one TargetOpcode:: token:   %d" % target)
print("   argument is a CALL (a hop is available):        %d" % call)
print("   everything else:                                %d"
      % (sites - arch - target - call))
print("   the sixty most frequent argument spellings:")
for k, v in shapes.most_common(60):
    print("      %-46s %d" % (k, v))
PY

say "[2/5] cpp -- the callees the hop would follow, and whether they are in the region"
python3 - <<'PY'
import re, sys, collections
sys.path.insert(0, "PseudoCoupHQ/Research/compiler_graph")
import graph as G
region = G.REGIONS["cpp"]
files = [f for f in G.list_region_files(region) if not f.endswith(".td")]
texts = {rel: G.show_file(region.repository, region.pin, rel) for rel in files}

def balanced(text, i):
    depth, j = 0, i
    while j < len(text):
        if text[j] == "(":
            depth += 1
        elif text[j] == ")":
            depth -= 1
            if depth == 0:
                return text[i + 1:j], j
        j += 1
    return None, len(text)

GETCALL = re.compile(r"(?:\bTII\s*(?:->|\.)\s*get|\bget)\s*\(")
callees = collections.Counter()
for rel, text in texts.items():
    for m in re.finditer(r"\bBuildMI\s*\(", text):
        body, _ = balanced(text, text.index("(", m.start()))
        if body is None:
            continue
        g = GETCALL.search(body)
        if not g:
            continue
        arg, _ = balanced(body, body.index("(", g.start()))
        arg = " ".join((arg or "").split())
        n = re.match(r"^([A-Za-z_][A-Za-z0-9_:.>()\[\]-]*)\s*\(", arg)
        if n:
            callees[n.group(1)] += 1
print("   distinct callee spellings in an opcode argument: %d" % len(callees))
for k, v in callees.most_common(40):
    name = k.split("::")[-1].split(".")[-1].split(">")[-1]
    declared = sum(1 for t in texts.values()
                   if re.search(r"\b%s\s*\(" % re.escape(name), t))
    print("      %-40s %3d   files declaring or naming it: %d" % (k, v, declared))
PY

say "[3/5] rust -- every inline-asm template the COMPILER ITSELF spells"
python3 - <<'PY'
import re, sys, collections
sys.path.insert(0, "PseudoCoupHQ/Research/compiler_graph")
import graph as G
region = G.REGIONS["rust"]
files = G.list_region_files(region)
PAT = re.compile(r"(inline_asm|InlineAsm|asm_string|template|naked_asm|global_asm)")
LIT = re.compile(r"\"((?:[^\"\\\\]|\\\\.){2,120})\"")
found = 0
for rel in files:
    text = G.show_file(region.repository, region.pin, rel)
    for n, line in enumerate(text.splitlines(), 1):
        if not PAT.search(line):
            continue
        for lit in LIT.findall(line):
            if re.match(r"^[a-z][a-z0-9]{1,7}([ \t]|$)", lit):
                found += 1
                print("   %s:%d  %s" % (rel, n, lit[:90]))
print("   candidate compiler-spelled asm text lines in the rust region: %d" % found)
PY

say "[4/5] swift -- every inline-asm template the COMPILER ITSELF spells"
python3 - <<'PY'
import re, sys, collections
sys.path.insert(0, "PseudoCoupHQ/Research/compiler_graph")
import graph as G
region = G.REGIONS["swift"]
files = G.list_region_files(region)
PAT = re.compile(r"(InlineAsm|createInlineAsm|asm_|AsmString)")
LIT = re.compile(r"\"((?:[^\"\\\\]|\\\\.){0,200})\"")
found = 0
for rel in files:
    text = G.show_file(region.repository, region.pin, rel)
    for n, line in enumerate(text.splitlines(), 1):
        if not PAT.search(line):
            continue
        print("   %s:%d  %s" % (rel, n, line.strip()[:120]))
        found += 1
print("   inline-asm lines in the swift region: %d" % found)
PY

say "[5/5] the coverage summaries -- their shape, and the entered sets"
python3 - <<'PY'
import json, os, resource, sys
sys.path.insert(0, "PseudoCoupHQ/Research/compiler_graph")
HERE = "PseudoCoupHQ/Research/compiler_graph"
for name in ("coverage_go_files.json", "coverage_cpp_files.json",
             "coverage_go_summary.json", "coverage_cpp_summary.json"):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        print("   %-28s ABSENT" % name)
        continue
    doc = json.load(open(p))
    print("   %-28s %10d bytes   top-level keys: %s"
          % (name, os.path.getsize(p), list(doc)[:14]))
    for k in ("populations", "counts"):
        if k in doc:
            print("        %s: %s" % (k, json.dumps(doc[k])[:600]))
    for k in ("per_definition", "definitions", "per_definition_visitors"):
        if k in doc:
            v = doc[k]
            print("        %s: %s of them; one row: %s"
                  % (k, len(v),
                     json.dumps(v[0] if isinstance(v, list)
                                else next(iter(v.items())))[:300]))
    del doc
print("   peak RSS %.1f MB"
      % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
PY

say "lane 4 done"
