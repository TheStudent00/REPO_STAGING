#!/usr/bin/env python3
"""timing_build.py -- measure the WORST-CASE cost of one layer-3 probe.

Purpose. the owner has ruled full enumeration of operand pairs for layer 3 and is
deciding whether to also brute-force the full value matrix. Before ruling he
wants MEASUREMENTS rather than guesses: what does ONE probe cost, in its own
file, in its own process, with no batching and no daemon -- the worst case.

What this builds. One SandboxDesign lane script per language. Each script
writes N probe programs, one per directory, then times each one twice over:
the COMPILE step (where the language has one) and the RUN step, wall clock,
recorded separately in nanoseconds. Every lane prints [done/total], elapsed
and an ETA from the running mean as it goes.

A probe here is the shape layer 3 actually uses: one operation -- a binary
operator, a subscript, a comparison, a unary operator -- applied to literal
operands spelled in that language, drawn from the layer-1 forms. Half the
sample is predicted-accepting and half predicted-refusing, because refusals
are the majority under enumeration and a refusal may cost differently. The
prediction only balances the sample; the MEASURED exit codes are what the
report classifies on.

Products: lanes/tm_<language>.sh, dropped into SandboxDesign/agent/drop/.
Each lane writes /out/tm_<language>.txt, one line per probe:

    <probe id>|<predicted label>|<compile rc>|<compile ns>|<run rc>|<run ns>

plus a final BATCH line: one file holding 100 accepting probes, compiled and
run once, so the amortisation of batching can be read off the same run.
"""

import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.join(HERE, "lanes")

CAP_SECONDS = 400          # per-lane wall-clock cap; a lane stops early and
N_TARGET = 100             # reports the count it actually reached

# --------------------------------------------------------------- the operands
# Seventeen atoms per language: the layer-1 forms in that language's own
# spellings. Ids are shared across languages so the sample is comparable.

ATOM_FORMS = {
    "nil": "nothing",
    "true": "truth", "false": "truth",
    "i0": "whole", "i42": "whole", "ibig": "whole",
    "f15": "fractional", "f01": "fractional", "fpi": "fractional",
    "sempty": "text", "shello": "text", "sworld": "text",
    "l123": "sequence", "l7": "sequence",
    "m1": "keyed", "m2": "keyed",
}

OPS = ["+", "-", "*", "<", "=="]

# --------------------------------------------------------------- the languages


def L(**kw):
    kw.setdefault("decl_over", {})
    kw.setdefault("compile", "")
    kw.setdefault("block", ("{", "}"))
    return kw


LANGS = {}

LANGS["python"] = L(
    file="main.py", ext="py",
    check='command -v python3 >/dev/null 2>&1',
    run="python3 main.py",
    head="", tail="", indent="",
    atoms={"nil": "None", "true": "True", "false": "False",
           "i0": "0", "i42": "42", "ibig": "1000000",
           "f15": "1.5", "f01": "0.1", "fpi": "3.14",
           "sempty": '""', "shello": '"hello"', "sworld": '"world"',
           "l123": "[1, 2, 3]", "l7": "[7]",
           "m1": '{"a": 1}', "m2": '{"a": 1, "b": 2}'},
    decl=lambda n, e: "%s = %s" % (n, e),
    res=lambda x: 'r = %s\nprint("r=", type(r).__name__)' % x,
    notop="not ", block=("if True:", ""), pyblock=True,
)

LANGS["ruby"] = L(
    file="main.rb", ext="rb",
    check='command -v ruby >/dev/null 2>&1',
    run="ruby main.rb",
    head="", tail="", indent="",
    atoms={"nil": "nil", "true": "true", "false": "false",
           "i0": "0", "i42": "42", "ibig": "1000000",
           "f15": "1.5", "f01": "0.1", "fpi": "3.14",
           "sempty": '""', "shello": '"hello"', "sworld": '"world"',
           "l123": "[1, 2, 3]", "l7": "[7]",
           "m1": '{"a" => 1}', "m2": '{"a" => 1, "b" => 2}'},
    decl=lambda n, e: "%s = %s" % (n, e),
    res=lambda x: 'r = %s\nputs "r=" + r.class.to_s' % x,
    notop="!", block=("begin", "end"),
)

LANGS["php"] = L(
    file="main.php", ext="php",
    check='command -v php >/dev/null 2>&1',
    run="php main.php",
    head="<?php", tail="", indent="",
    atoms={"nil": "null", "true": "true", "false": "false",
           "i0": "0", "i42": "42", "ibig": "1000000",
           "f15": "1.5", "f01": "0.1", "fpi": "3.14",
           "sempty": '""', "shello": '"hello"', "sworld": '"world"',
           "l123": "array(1, 2, 3)", "l7": "array(7)",
           "m1": 'array("a" => 1)', "m2": 'array("a" => 1, "b" => 2)'},
    decl=lambda n, e: "$%s = %s;" % (n, e),
    res=lambda x: '$r = %s;\necho "r=" . gettype($r) . "\\n";' % x,
    notop="!", var="$",
)

LANGS["typescript"] = L(
    file="main.ts", ext="ts",
    check='test -x /persist/ts/node_modules/.bin/tsc',
    compile="/persist/ts/node_modules/.bin/tsc --target es2020 --module commonjs main.ts",
    run="node main.js",
    head="", tail="", indent="",
    atoms={"nil": "null", "true": "true", "false": "false",
           "i0": "0", "i42": "42", "ibig": "1000000",
           "f15": "1.5", "f01": "0.1", "fpi": "3.14",
           "sempty": '""', "shello": '"hello"', "sworld": '"world"',
           "l123": "[1, 2, 3]", "l7": "[7]",
           "m1": '{a: 1}', "m2": '{a: 1, b: 2}'},
    decl=lambda n, e: "const %s = %s;" % (n, e),
    res=lambda x: 'const r = %s;\nconsole.log("r=" + typeof r);' % x,
    notop="!",
)

LANGS["java"] = L(
    file="Main.java", ext="java",
    check='command -v javac >/dev/null 2>&1',
    compile="javac Main.java",
    run="java Main",
    head="public class Main {\n  public static void main(String[] args) {",
    tail="  }\n}", indent="    ",
    atoms={"nil": "(String) null", "true": "true", "false": "false",
           "i0": "0", "i42": "42", "ibig": "1000000",
           "f15": "1.5", "f01": "0.1", "fpi": "3.14",
           "sempty": '""', "shello": '"hello"', "sworld": '"world"',
           "l123": "new int[]{1, 2, 3}", "l7": "new int[]{7}",
           "m1": 'java.util.Map.of("a", 1)',
           "m2": 'java.util.Map.of("a", 1, "b", 2)'},
    decl=lambda n, e: "var %s = %s;" % (n, e),
    res=lambda x: 'var r = %s;\nSystem.out.println("r=" + r);' % x,
    notop="!",
)

LANGS["csharp"] = L(
    file="Program.cs", ext="cs",
    check='test -x /persist/dotnet/dotnet',
    compile="/persist/dotnet-csc-build.sh",
    run="/persist/dotnet-csc-run.sh",
    head="public class Program {\n  public static void Main() {",
    tail="  }\n}", indent="    ",
    atoms={"nil": "(string) null", "true": "true", "false": "false",
           "i0": "0", "i42": "42", "ibig": "1000000",
           "f15": "1.5", "f01": "0.1", "fpi": "3.14",
           "sempty": '""', "shello": '"hello"', "sworld": '"world"',
           "l123": "new int[]{1, 2, 3}", "l7": "new int[]{7}",
           "m1": 'new System.Collections.Generic.Dictionary<string,int>{{"a",1}}',
           "m2": 'new System.Collections.Generic.Dictionary<string,int>{{"a",1},{"b",2}}'},
    decl=lambda n, e: "var %s = %s;" % (n, e),
    res=lambda x: 'var r = %s;\nSystem.Console.WriteLine("r=" + r);' % x,
    notop="!",
)

LANGS["go"] = L(
    file="main.go", ext="go",
    check='command -v go >/dev/null 2>&1',
    compile="go build -o prog main.go",
    run="./prog",
    head='package main\n\nimport "fmt"\n\nfunc main() {', tail="}", indent="\t",
    atoms={"nil": "nil", "true": "true", "false": "false",
           "i0": "0", "i42": "42", "ibig": "1000000",
           "f15": "1.5", "f01": "0.1", "fpi": "3.14",
           "sempty": '""', "shello": '"hello"', "sworld": '"world"',
           "l123": "[]int{1, 2, 3}", "l7": "[]int{7}",
           "m1": 'map[string]int{"a": 1}',
           "m2": 'map[string]int{"a": 1, "b": 2}'},
    decl=lambda n, e: "%s := %s" % (n, e),
    decl_over={"nil": "var %s interface{} = nil"},
    res=lambda x: 'r := %s\nfmt.Printf("r=%%T\\n", r)' % x,
    notop="!",
)

LANGS["rust"] = L(
    file="main.rs", ext="rs",
    check='command -v rustc >/dev/null 2>&1',
    compile="rustc -A warnings main.rs -o prog",
    run="./prog",
    head="#![allow(unused)]\nfn main() {", tail="}", indent="    ",
    atoms={"nil": "None::<i32>", "true": "true", "false": "false",
           "i0": "0", "i42": "42", "ibig": "1000000",
           "f15": "1.5", "f01": "0.1", "fpi": "3.14",
           "sempty": 'String::from("")', "shello": 'String::from("hello")',
           "sworld": 'String::from("world")',
           "l123": "vec![1, 2, 3]", "l7": "vec![7]",
           "m1": 'std::collections::HashMap::from([("a", 1)])',
           "m2": 'std::collections::HashMap::from([("a", 1), ("b", 2)])'},
    decl=lambda n, e: "let %s = %s;" % (n, e),
    res=lambda x: 'let r = %s;\nprintln!("r={}", std::mem::size_of_val(&r));' % x,
    notop="!",
)

LANGS["cpp"] = L(
    file="main.cpp", ext="cpp",
    check='command -v g++ >/dev/null 2>&1',
    compile="g++ -w -std=c++17 main.cpp -o prog",
    run="./prog",
    head=("#include <iostream>\n#include <map>\n#include <string>\n"
          "#include <vector>\nint main() {"),
    tail="  return 0;\n}", indent="  ",
    atoms={"nil": "nullptr", "true": "true", "false": "false",
           "i0": "0", "i42": "42", "ibig": "1000000",
           "f15": "1.5", "f01": "0.1", "fpi": "3.14",
           "sempty": 'std::string("")', "shello": 'std::string("hello")',
           "sworld": 'std::string("world")',
           "l123": "std::vector<int>{1, 2, 3}", "l7": "std::vector<int>{7}",
           "m1": 'std::map<std::string,int>{{"a", 1}}',
           "m2": 'std::map<std::string,int>{{"a", 1}, {"b", 2}}'},
    decl=lambda n, e: "auto %s = %s;" % (n, e),
    res=lambda x: 'auto r = %s;\nstd::cout << "r=" << sizeof(r) << "\\n";' % x,
    notop="!",
)

LANGS["kotlin"] = L(
    file="main.kt", ext="kt",
    check='test -x /persist/kotlinc/bin/kotlinc',
    compile="/persist/kotlinc/bin/kotlinc main.kt -d out",
    run="/persist/kotlinc/bin/kotlin -classpath out MainKt",
    head="fun main() {", tail="}", indent="    ",
    atoms={"nil": "null", "true": "true", "false": "false",
           "i0": "0", "i42": "42", "ibig": "1000000",
           "f15": "1.5", "f01": "0.1", "fpi": "3.14",
           "sempty": '""', "shello": '"hello"', "sworld": '"world"',
           "l123": "listOf(1, 2, 3)", "l7": "listOf(7)",
           "m1": 'mapOf("a" to 1)', "m2": 'mapOf("a" to 1, "b" to 2)'},
    decl=lambda n, e: "val %s = %s" % (n, e),
    res=lambda x: 'val r = %s\nprintln("r=" + r)' % x,
    notop="!", block=("run {", "}"),
)

LANGS["swift"] = L(
    file="main.swift", ext="swift",
    check='test -x /persist/swift/usr/bin/swiftc',
    compile="/persist/swift/usr/bin/swiftc main.swift -o prog",
    run="./prog",
    head="", tail="", indent="",
    atoms={"nil": "nil", "true": "true", "false": "false",
           "i0": "0", "i42": "42", "ibig": "1000000",
           "f15": "1.5", "f01": "0.1", "fpi": "3.14",
           "sempty": '""', "shello": '"hello"', "sworld": '"world"',
           "l123": "[1, 2, 3]", "l7": "[7]",
           "m1": '["a": 1]', "m2": '["a": 1, "b": 2]'},
    decl=lambda n, e: "let %s = %s" % (n, e),
    decl_over={"nil": "let %s: Int? = nil"},
    res=lambda x: 'let r = %s\nprint("r=", type(of: r))' % x,
    notop="!", block=("do {", "}"),
)

LANGS["dart"] = L(
    file="main.dart", ext="dart",
    check='test -x /persist/dart-sdk/bin/dart',
    run="/persist/dart-sdk/bin/dart run main.dart",
    head="void main() {", tail="}", indent="  ",
    atoms={"nil": "null", "true": "true", "false": "false",
           "i0": "0", "i42": "42", "ibig": "1000000",
           "f15": "1.5", "f01": "0.1", "fpi": "3.14",
           "sempty": '""', "shello": '"hello"', "sworld": '"world"',
           "l123": "[1, 2, 3]", "l7": "[7]",
           "m1": '{"a": 1}', "m2": '{"a": 1, "b": 2}'},
    decl=lambda n, e: "var %s = %s;" % (n, e),
    res=lambda x: 'var r = %s;\nprint("r=" + r.runtimeType.toString());' % x,
    notop="!",
)

ORDER = ["python", "ruby", "php", "typescript", "dart", "go", "java",
         "csharp", "rust", "cpp", "swift", "kotlin"]

# ------------------------------------------------------- predicted acceptance

NUM = ("whole", "fractional")


def predict(shape, op, fa, fb):
    """A rough accept/refuse label. It BALANCES the sample; it is not the
    measurement. The lane records real exit codes and the report classifies
    on those."""
    if shape == "bin":
        if op == "+":
            return (fa in NUM and fb in NUM) or (fa == fb == "text") \
                or (fa == fb == "sequence")
        if op in ("-", "*"):
            return fa in NUM and fb in NUM
        if op == "<":
            return (fa in NUM and fb in NUM) or (fa == fb == "text")
        if op == "==":
            return fa == fb
    if shape == "idx":
        return fa in ("sequence", "text")
    if shape == "neg":
        return fa in NUM
    if shape == "not":
        return fa == "truth"
    return False


def sample(seed):
    """Half accepting, half refusing, drawn at random from the whole space."""
    rng = random.Random(seed)
    ids = sorted(ATOM_FORMS)
    space = []
    for op in OPS:
        for a in ids:
            for b in ids:
                space.append(("bin", op, a, b))
    for a in ids:
        space.append(("idx", "[", a, None))
        space.append(("neg", "-", a, None))
        space.append(("not", "!", a, None))
    acc = [s for s in space if predict(s[0], s[1], ATOM_FORMS[s[2]],
                                       ATOM_FORMS[s[3]] if s[3] else None)]
    ref = [s for s in space if s not in acc]
    rng.shuffle(acc)
    rng.shuffle(ref)
    half = N_TARGET // 2
    out = acc[:half] + ref[:half]
    rng.shuffle(out)
    return out, acc


def body(lang, probe, va="a", vb="b"):
    """The source lines of one probe, without the language's head and tail."""
    cfg = LANGS[lang]
    shape, op, a, b = probe
    pre = cfg.get("var", "")
    lines = []

    def declare(name, atom):
        over = cfg["decl_over"].get(atom)
        if over:
            return over % name
        return cfg["decl"](name, cfg["atoms"][atom])

    lines.append(declare(va, a))
    if shape == "bin":
        lines.append(declare(vb, b))
        expr = "(%s%s) %s (%s%s)" % (pre, va, op, pre, vb)
    elif shape == "idx":
        expr = "(%s%s)[0]" % (pre, va)
    elif shape == "neg":
        expr = "-(%s%s)" % (pre, va)
    else:
        expr = "%s(%s%s)" % (cfg["notop"], pre, va)
    lines.append(cfg["res"](expr))
    return "\n".join(lines).split("\n")


def program(lang, probe):
    cfg = LANGS[lang]
    ind = cfg["indent"]
    out = []
    if cfg["head"]:
        out.append(cfg["head"])
    out += [ind + line for line in body(lang, probe)]
    if cfg["tail"]:
        out.append(cfg["tail"])
    return "\n".join(out) + "\n"


def batch_program(lang, probes):
    """One file holding many accepting probes, each in its own scope, so the
    amortisation of a batched compile can be read from the same run."""
    cfg = LANGS[lang]
    ind = cfg["indent"]
    bo, bc = cfg["block"]
    out = []
    if cfg["head"]:
        out.append(cfg["head"])
    for i, probe in enumerate(probes):
        out.append(ind + bo)
        for line in body(lang, probe, "a%d" % i, "b%d" % i):
            out.append(ind + ("    " if not cfg.get("pyblock") else "    ")
                       + line)
        if bc:
            out.append(ind + bc)
    if cfg["tail"]:
        out.append(cfg["tail"])
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------ lane text

PRELUDE = """#!/bin/sh
# layer-3 PROBE TIMING -- %(lang)s -- generated by
# Research/kind_fuzz_clustering/timing_build.py . Do not hand-edit; regenerate.
# One probe per file, fresh process per probe, no batching: the WORST CASE.
# Every line of /out/tm_%(lang)s.txt is
#   <probe id>|<predicted>|<compile rc>|<compile ns>|<run rc>|<run ns>
set -u
ROOT=/work/tm_%(lang)s
rm -rf "$ROOT"; mkdir -p "$ROOT"
export HOME=/work
export GOFLAGS=-mod=mod
export GO111MODULE=off
export GOCACHE=/work/.gocache
export GOPATH=/work/.gopath
export PATH=/persist/dart-sdk/bin:$PATH

# swift's binaries want an ncurses name the image does not ship under; the fix
# is per-container, so every script that may touch swift re-applies it.
ncurses_fix() {
  if [ -f /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 ]; then
    ln -sf /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 \\
       /usr/lib/x86_64-linux-gnu/libncurses.so.6 2>/dev/null
    ldconfig 2>/dev/null
  fi
}
ncurses_fix

OUT=/out/tm_%(lang)s.txt
: > "$OUT"
echo "=== layer-3 probe timing -- %(lang)s ==="
date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ
if ! %(check)s; then
  echo "%(lang)s: TOOLCHAIN ABSENT -- nothing run"
  echo "__ABSENT__|absent|-1|0|-1|0" >> "$OUT"
  exit 0
fi
"""

LOOP = """
CAP=%(cap)d
TOTAL=%(total)d
# The container's `timeout` is uutils coreutils 0.8.0, which polls at 100 ms
# and so quantises every wrapped step to a 100 ms bucket (measured: see
# raw/tm_diag.txt). It is therefore NOT used around a timed step. The residual
# instrument cost is the two `date` forks, measured here and reported so it
# can be subtracted.
GAP=0
for k in 1 2 3 4 5 6 7; do
  G0=$(date +%%s%%N); G1=$(date +%%s%%N); GAP=$((GAP+G1-G0))
done
GAP=$((GAP/7))
echo "__GAP__|instrument|0|$GAP|0|0" >> "$OUT"
echo "instrument overhead per timed step: ${GAP} ns"
LANE0=$(date +%%s)
i=0
SUM=0
while IFS=' ' read -r PID LABEL; do
  i=$((i+1))
  cd "$ROOT/$PID" || continue
  CRC=0; CNS=0
  %(compile_block)s
  RRC=-1; RNS=0
  if [ "$CRC" -eq 0 ]; then
    R0=$(date +%%s%%N)
    %(run)s > r.out 2> r.err
    RRC=$?
    R1=$(date +%%s%%N)
    RNS=$((R1-R0))
  fi
  echo "$PID|$LABEL|$CRC|$CNS|$RRC|$RNS" >> "$OUT"
  SUM=$((SUM+CNS+RNS))
  NOW=$(date +%%s)
  EL=$((NOW-LANE0))
  MEANMS=$((SUM/i/1000000))
  ETA=$(( (TOTAL-i) * (SUM/i) / 1000000000 ))
  echo "[$i/$TOTAL] elapsed=${EL}s mean=${MEANMS}ms eta=${ETA}s  ($PID $LABEL c=$CRC r=$RRC)"
  if [ "$EL" -ge "$CAP" ]; then
    echo "CAP REACHED at $i/$TOTAL after ${EL}s -- stopping early"
    break
  fi
done < "$ROOT/labels.txt"
echo "PROBES_DONE=$i of $TOTAL"
"""

COMPILE_BLOCK = """C0=$(date +%%s%%N)
  %(compile)s > b.out 2> b.err
  CRC=$?
  C1=$(date +%%s%%N)
  CNS=$((C1-C0))"""

BATCH = """
# ---- one batched file: %(nbatch)d accepting probes, compiled once, run once.
cd "$ROOT/batch" || exit 0
BC0=$(date +%%s%%N)
BCRC=0
%(bcompile)s
BC1=$(date +%%s%%N)
BRRC=-1; BR1=0; BR0=0
if [ "$BCRC" -eq 0 ]; then
  BR0=$(date +%%s%%N)
  %(run)s > r.out 2> r.err
  BRRC=$?
  BR1=$(date +%%s%%N)
fi
echo "__BATCH%(nbatch)d__|accept|$BCRC|$((BC1-BC0))|$BRRC|$((BR1-BR0))" >> "$OUT"
echo "batch: compile rc=$BCRC ns=$((BC1-BC0))  run rc=$BRRC ns=$((BR1-BR0))"
sed -n 1,3p b.err 2>/dev/null
echo "=== tm_%(lang)s complete: $(wc -l < "$OUT") result lines ==="
"""

BATCH_COMPILE = """BC0=$(date +%s%N)
timeout 900 %(compile)s > b.out 2> b.err
BCRC=$?"""


def measured_accepts(lang):
    """Probe numbers that pass 1 measured as ACCEPTING: compiled clean and ran
    clean. Empty when pass 1 has not been run."""
    path = os.path.join(HERE, "raw", "tm_pass1_%s.txt" % lang)
    if not os.path.exists(path):
        return []
    out = []
    for line in open(path):
        bits = line.strip().split("|")
        if len(bits) != 6 or not bits[0].startswith("p"):
            continue
        if bits[2] == "0" and bits[4] == "0":
            out.append(int(bits[0][1:]))
    return out


def heredoc(path, text, tag):
    return ("cat > %s <<'%s'\n%s%s\n" % (path, tag, text, tag))


def build(lang):
    cfg = LANGS[lang]
    # a deterministic per-language seed: python's own hash() is salted per
    # process, so the sample would not be reproducible if it were used.
    probes, accepting = sample(seed=sum(ord(c) for c in lang))
    parts = [PRELUDE % {"lang": lang, "check": cfg["check"]}]

    labels = []
    for n, probe in enumerate(probes, 1):
        pid = "p%d" % n
        shape, op, a, b = probe
        label = "accept" if predict(shape, op, ATOM_FORMS[a],
                                    ATOM_FORMS[b] if b else None) else "refuse"
        labels.append("%s %s" % (pid, label))
        parts.append('mkdir -p "$ROOT/%s"\n' % pid)
        parts.append(heredoc('"$ROOT/%s/%s"' % (pid, cfg["file"]),
                             program(lang, probe), "TM_SRC_EOF"))
    parts.append(heredoc('"$ROOT/labels.txt"', "\n".join(labels) + "\n",
                         "TM_LABELS_EOF"))

    # The batch file may hold only probes that ACTUALLY compile and run: one
    # refusal would refuse the whole file, which is the very reason a batched
    # enumeration needs bisecting. Pass 1's measured exit codes name them; if
    # pass 1 is absent the predicted labels stand in.
    winners = measured_accepts(lang)
    if winners:
        batch_probes = [probes[n - 1] for n in winners]
    else:
        batch_probes = accepting[:100]
    while len(batch_probes) < 100 and batch_probes:
        batch_probes += batch_probes[:100 - len(batch_probes)]
    nbatch = len(batch_probes)
    parts.append('mkdir -p "$ROOT/batch"\n')
    parts.append(heredoc('"$ROOT/batch/%s"' % cfg["file"],
                         batch_program(lang, batch_probes),
                         "TM_BATCH_EOF"))

    compile_block = (COMPILE_BLOCK % {"compile": cfg["compile"]}
                     if cfg["compile"] else 'CRC=0; CNS=0')
    parts.append(LOOP % {"cap": CAP_SECONDS, "total": len(probes),
                         "compile_block": compile_block, "run": cfg["run"]})
    bcompile = ("%s > b.out 2> b.err\nBCRC=$?" % cfg["compile"]
                if cfg["compile"] else "BCRC=0")
    parts.append(BATCH % {"nbatch": nbatch, "bcompile": bcompile,
                          "run": cfg["run"], "lang": lang})
    return "".join(parts)


def main():
    os.makedirs(LANES, exist_ok=True)
    drop = "/sessions/brave-optimistic-cannon/mnt/Programming/SandboxDesign/agent/drop"
    manifest = {}
    for lang in ORDER:
        text = build(lang)
        path = os.path.join(LANES, "tm_%s.sh" % lang)
        with open(path, "w") as h:
            h.write(text)
        manifest[lang] = {"lane": os.path.basename(path),
                          "bytes": len(text),
                          "probes": N_TARGET,
                          "has_compile_step": bool(LANGS[lang]["compile"])}
        print("wrote %s (%d bytes)" % (path, len(text)))
    with open(os.path.join(HERE, "timing_manifest.json"), "w") as h:
        json.dump(manifest, h, indent=1, sort_keys=True)
    print("drop with: cp %s/tm_<lang>.sh %s/" % (LANES, drop))


if __name__ == "__main__":
    main()
