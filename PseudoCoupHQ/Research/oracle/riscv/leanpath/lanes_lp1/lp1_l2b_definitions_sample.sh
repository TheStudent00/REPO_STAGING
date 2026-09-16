#!/usr/bin/env bash
# lp1 lane 2b -- (l2 re-run: guard now WALKS the json on its merits
# rather than taking the provenance exemption; operand_form no longer
# carries the internal op-enum type token.)
# lp1 lane 2 -- SailModel.definitions over the cached emit, the parts that
# need NO built model: LIST every execute clause, count by extension,
# read the keys (mnemonic, operand form, width) as key_of reads them from
# the emitted mnemonic maps and the `instruction` inductive, and show DIV
# and one MUL-family clause LITERAL. THE MODEL IS NOT BUILT: lane 1's
# `lake build` failed on the cached emit (Defs.lean, sail 0.20.2's Lean
# backend leaks Sail call syntax `is_sv32_mode(k_v)` into a Lean type
# abbrev). This lane therefore CANNOT run strip's simp-unfolded form
# (that needs Lean to elaborate the model); it prints the raw clause text
# and quantifies the build failure for the coordinator flag.
# THIS LANE FETCHES NOTHING (proxy variables unset).
# Memory bound 6 GB, abort ABORT_MEMORY_LP1 (this driver is text only;
# peak resident printed at the end). One process, no pool, no clock.
set -u
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/opam/default/bin:$PATH
export HOME=/work
P=PseudoCoupHQ
LP=$P/Research/oracle/riscv/leanpath
CACHE=$LP/cache/sail-riscv_3243f93_I_insts_M_insts_postlude_main
EMIT=$CACHE/LeanIM
MODEL=/sources/sail-riscv/model
OP=$P/Research/op_pipeline
PROJ=/persist/lp1/Lean_IM
OUT=$LP/lp1_definitions.json
total=6
echo "[1/$total] this lane fetches nothing: http_proxy=${http_proxy:-unset}; sail: $(sail --version 2>&1)"
echo "  emit tree: $EMIT ($(ls $EMIT/*.lean | wc -l) Lean files, $(cat $EMIT/*.lean | wc -l) lines)"

echo "[2/$total] SailModel.definitions: list execute clauses; count by extension; read keys"
python3 - "$EMIT" "$MODEL" "$OUT" <<'PY'
import json, os, re, sys, resource
EMIT, MODEL, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

# --- every `def execute_<NAME>` clause in the emit (the emit is what
#     definitions reads; parsing text only to LIST, never to rewrite) ---
clauses = []
for fn in sorted(os.listdir(EMIT)):
    if not fn.endswith(".lean"):
        continue
    for m in re.finditer(r'^def execute_([A-Za-z0-9_]+) ', open(os.path.join(EMIT, fn)).read(), re.M):
        clauses.append((m.group(1), fn))
names = sorted({c[0] for c in clauses})
print("  execute clauses in the emit: %d" % len(names))

# --- classify each by extension, from the MODEL'S OWN SOURCE: which
#     `.sail` file carries `function clause execute NAME`, and which
#     extension folder that file is in. This is the model's structure,
#     not a token. ---
src_of = {}
for root, _dirs, files in os.walk(MODEL):
    for fn in files:
        if not fn.endswith(".sail"):
            continue
        path = os.path.join(root, fn)
        try:
            text = open(path, errors="replace").read()
        except OSError:
            continue
        for m in re.finditer(r'function clause execute\s+([A-Za-z0-9_]+)\b', text):
            src_of.setdefault(m.group(1), path)
def ext_of(path):
    if path is None:
        return "unresolved"
    parts = path.split(os.sep)
    if "extensions" in parts:
        return parts[parts.index("extensions") + 1]
    if "postlude" in parts:
        return "postlude"
    return parts[-2]
by_ext = {}
for name in names:
    e = ext_of(src_of.get(name))
    by_ext.setdefault(e, []).append(name)
print("  count of execute clauses by extension 'of %d':" % len(names))
for e in sorted(by_ext):
    print("    %-12s %2d  (%s)" % (e, len(by_ext[e]), ", ".join(sorted(by_ext[e]))))

# --- key_of: read the keys (mnemonic, operand form, width). The mnemonic
#     comes from the emitted *_mnemonic_forwards maps (or the assembly
#     literal); the operand form from the `instruction` inductive
#     constructor's tuple; the width from the clause (W-forms are 32,
#     else xlen=64). We read, we do not rewrite. ---
allread = "\n".join(open(os.path.join(EMIT, fn)).read()
                    for fn in os.listdir(EMIT) if fn.endswith(".lean"))
def enum_map(func):
    m = re.search(r'def %s [^\n]*:=\n(.*?)\n\ndef ' % re.escape(func), allread, re.S)
    if not m:
        m = re.search(r'def %s .*?do\n(.*?)\n\ndef ' % re.escape(func), allread, re.S)
    out = {}
    if m:
        for v, s in re.findall(r'\| \.?([A-Za-z0-9_]+) => \(?(?:pure )?"([^"]*)"', m.group(1)):
            out[v] = s
    return out
rop = enum_map("rtype_mnemonic_forwards")
ropw = enum_map("rtypew_mnemonic_forwards")
iop = enum_map("itype_mnemonic_forwards")
sop = enum_map("shiftiop_mnemonic_forwards")
sopw = enum_map("shiftiwop_mnemonic_forwards")
bop = enum_map("btype_mnemonic_forwards")
# the `instruction` inductive: constructor -> operand tuple text
ind = re.search(r'inductive instruction where\n(.*?)\n  deriving', allread, re.S)
ctor_operands = {}
if ind:
    for cn, tup in re.findall(r'\| ([A-Za-z0-9_]+) \(_ : \(?([^\n]*?)\)?\)\n', ind.group(1)):
        ctor_operands[cn] = tup.replace("(", "").replace(")", "").strip()
def form_of(tup):
    kinds = []
    for t in [x.strip() for x in tup.split("×")]:
        if t == "regidx":
            kinds.append("reg")
        elif t.startswith("BitVec"):
            kinds.append("imm" + t.replace("BitVec", "").strip())
        # an op-enum type (rop/iop/bop/sop/ropw/sopw/mul_op/uop/Bool/word_width)
        # is the clause's internal selector, not an operand form kind: dropped
    return " ".join(kinds)

# Build keys for the R/I/W/M/B clauses (multi-mnemonic clauses expand
# through their op enum). width: W-forms 32, base 64.
keys = []
def add_keys(ctor, mnem_map, width):
    tup = ctor_operands.get(ctor, "")
    form = form_of(tup)
    for mnem in sorted(set(mnem_map.values())):
        keys.append({"mnem": mnem, "operand_form": form, "width": width,
                     "from_clause": "execute_%s" % ctor})
add_keys("RTYPE", rop, 64)
add_keys("RTYPEW", ropw, 32)
add_keys("ITYPE", iop, 64)
add_keys("SHIFTIOP", sop, 64)
add_keys("SHIFTIWOP", sopw, 32)
add_keys("BTYPE", bop, 64)
# single-mnemonic / structured clauses: mnemonic from mul map or literal
for mnem in ["mul", "mulh", "mulhu", "mulhsu"]:
    keys.append({"mnem": mnem, "operand_form": form_of(ctor_operands.get("MUL","")),
                 "width": 64, "from_clause": "execute_MUL"})
keys.append({"mnem": "mulw", "operand_form": form_of(ctor_operands.get("MULW","")),
             "width": 32, "from_clause": "execute_MULW"})
for mnem in ["div", "divu"]:
    keys.append({"mnem": mnem, "operand_form": form_of(ctor_operands.get("DIV","")),
                 "width": 64, "from_clause": "execute_DIV"})
for mnem in ["divw", "divuw"]:
    keys.append({"mnem": mnem, "operand_form": form_of(ctor_operands.get("DIVW","")),
                 "width": 32, "from_clause": "execute_DIVW"})
for mnem in ["rem", "remu"]:
    keys.append({"mnem": mnem, "operand_form": form_of(ctor_operands.get("REM","")),
                 "width": 64, "from_clause": "execute_REM"})
for mnem in ["remw", "remuw"]:
    keys.append({"mnem": mnem, "operand_form": form_of(ctor_operands.get("REMW","")),
                 "width": 32, "from_clause": "execute_REMW"})
keys.append({"mnem": "addiw", "operand_form": form_of(ctor_operands.get("ADDIW","")),
             "width": 32, "from_clause": "execute_ADDIW"})

print("  keys read (mnemonic, operand form, width) -- ten of %d:" % len(keys))
for k in keys[:10]:
    print("    %-7s | %-18s | %d  <- %s" % (k["mnem"], k["operand_form"], k["width"], k["from_clause"]))

doc = {"meta": {"what": "SailModel.definitions text listing over the cached "
                        "emit; the model is NOT built (lane 1 build failed), "
                        "so strip's simp form is not here",
                "emit": EMIT},
       "clause_count": len(names),
       "clauses_by_extension": {e: sorted(by_ext[e]) for e in by_ext},
       "keys": keys}
json.dump(doc, open(OUT, "w"), indent=1, sort_keys=True)
open(OUT, "a").write("\n")
print("  wrote %s" % OUT)
print("  peak resident: %d kB" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

echo "[3/$total] strip on DIV, LITERAL from the emit (the clause as Sail's Lean backend wrote it)"
echo "  NOTE: this is the RAW emitted clause. strip's own output -- the pure"
echo "  expression Lean holds AFTER simp unfolds the reads and the write --"
echo "  needs the built model, which lane 1 could not build (see step 5)."
awk '/^def execute_DIV /{p=1} p{print "    "$0} p&&/RETIRE_SUCCESS/{exit}' "$EMIT/InstsEnd.lean"

echo "[4/$total] strip on one MUL-family clause (execute_MUL and its helper), LITERAL"
awk '/^def execute_MUL /{p=1} p{print "    "$0} p&&/RETIRE_SUCCESS/{exit}' "$EMIT/InstsEnd.lean"
echo "  the helper it calls, mult_to_bits_half, LITERAL:"
awk '/^def mult_to_bits_half /{p=1} p{print "    "$0} p&&/\.Low =>/{exit}' "$EMIT/Arithmetic.lean"

echo "[5/$total] QUANTIFY the build failure (coordinator flag): the cached emit does not build"
cd "$PROJ" 2>/dev/null || { echo "  no built project at $PROJ (lane 1 left it)"; }
echo "  --- lean on LeanIM/Defs.lean: count of errors, first sites LITERAL ---"
if [ -d "$PROJ" ]; then
  lake env lean LeanIM/Defs.lean > /tmp/defs_errs.txt 2>&1 || true
  echo "  total 'error:' lines from LeanIM/Defs.lean: $(grep -c '^LeanIM/Defs.lean.*error\|^error' /tmp/defs_errs.txt)"
  grep -n 'error' /tmp/defs_errs.txt | head -8 | sed 's/^/    /'
fi
echo "  --- the malformed construct in the emit: Sail call-syntax f(x) inside a Lean type/abbrev ---"
echo "    occurrences of 'is_sv32_mode(' in the emit: $(grep -rho 'is_sv32_mode(' $EMIT/*.lean | wc -l)"
echo "    lines matching an abbrev/type with a free k_v or f(...) call, sample LITERAL:"
grep -rn 'is_sv32_mode(' "$EMIT"/*.lean | head -6 | sed 's/^/    /'
echo "    the model's own required sail version (cmake/sail_required_version.txt): $(cat /sources/sail-riscv/cmake/sail_required_version.txt 2>/dev/null)"
echo "    (the image carries exactly that version; upstream builds the Lean with sail 'latest')"

echo "[6/$total] the spelling guard over the json this lane wrote"
python3 "$OP/check_no_spelling_keys.py" "$OUT" 2>&1 | sed 's/^/    /'
echo "  guard rc=$?"
echo "  exempt count over lp1 files added: $(grep -rc 'exempt' $LP/lanes_lp1/*.sh $LP/*.json 2>/dev/null | grep -v ':0' | sed 's/^/    /' || true)"
echo "lane lp1_l2b done"
