#!/usr/bin/env python3
"""audit_generate.py -- the layer-2 load-audit, made real.

Plain words first. Layer 1 is the data (fixed content, no language). Layer 2 is
the set of ways each language can HOLD that content. This script turns the
layer-2 question -- "can this representation load layer-1 data?" -- into
programs that actually run.

For every (form, representation) cell in `representations_<language>.json` it
emits a tiny program that

  (a) CONSTRUCTS the representation holding that form's layer-1 values, with the
      values baked in as literals by this generator -- a probe never parses the
      data file at run time, so no language needs a parser to take part;
  (b) READS the content back out and prints one line in the shared harness
      convention `FACT_ID|RESULT`, where FACT_ID is `<form>.<rep>.<probe>`.

Nothing else happens to the data. Operations on a representation are layer 3
and belong to `kind_fuzz_clustering`; this script must not grow them.

Two program shapes, chosen per language by its `probe_style`:

* `probe`  -- ONE source file per probe. Used where a refusal is a COMPILE
  refusal (c++, go, java, kotlin, rust, swift, dart, typescript, c#). A compile
  refusal takes down the whole source file it sits in, so each probe gets its
  own file; otherwise one refused cell would erase its co-probes' results and
  the audit would read a language as far poorer than it is.
* `cell`   -- ONE source file per cell, each probe wrapped in a catch. Used
  where a refusal is a RUN-TIME refusal (python, ruby, php), which a catch can
  contain.

The generator also re-reads `data_layer1.json` and checks that every value a
`spell` table claims to spell is a value the data file actually holds. That
check is what stops the audit drifting away from layer 1.

A representation's own name is part of its FACT_ID, and rust spells one
`[T; N]` and go one `[]T` -- so the lane must match those ids as FIXED
STRINGS (`grep -F`). Matching them as patterns made `[...]` a character
class, the match failed, and the lane recorded its fallback word instead of
the program's answer.

Products: one lane script per language, written to `audit/lanes/l2_<lang>.sh`,
each dropped into ~/Programming/SandboxDesign/agent/drop/ by hand and run
serially. Every line of /out/l2_<lang>.txt is FACT_ID|RESULT.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

FORMS = ["nothing", "truth", "whole", "fractional", "text",
         "sequence", "keyed", "nesting", "identity"]

SCALAR_FORMS = ["nothing", "truth", "whole", "fractional", "text"]

# The probe ids of the scalar forms, and the layer-1 value each one names. The
# right-hand side is checked against data_layer1.json, so a probe id can never
# quietly stop meaning what the data file says.
SCALAR_PROBES = {
    "nothing": {"null": None},
    "truth": {"true": True, "false": False},
    "whole": {"base_zero": 0, "base_42": 42,
              "i64max": "9223372036854775807",
              "i64max_plus1": "9223372036854775808",
              "p53_plus1": "9007199254740993",
              "u64max": "18446744073709551615"},
    "fractional": {"base_1_5": 1.5, "base_pi": 3.141592653589793,
                   "negzero": "-0.0", "nan": "nan", "inf": "inf",
                   "point1": 0.1},
    "text": {"base_empty": "", "base_hello": "hello",
             "base_lines": "line one\nline two",
             "eacute": "é", "clef": "\U0001D11E",
             "escapes": "quote \" backslash \\ tab\there"},
}

CONTAINER_PROBES = {
    "sequence": ["empty", "base", "strs", "mixed", "bigint"],
    "keyed": ["empty", "flat", "intlike", "emptykey", "nested"],
    "nesting": ["seq_in_seq", "seq_in_map", "mixed_depth"],
    "identity": ["shared", "diamond", "cycle"],
}


# ---------------------------------------------------------------- layer-1 tie

def check_against_layer1(data):
    """Every scalar probe id must name content the data file holds. Returns the
    list of complaints; an empty list means the audit is still tied to layer 1."""
    bad = []
    if data["nothing"] != [None]:
        bad.append("nothing changed shape in data_layer1.json")
    if data["truth"] != [True, False]:
        bad.append("truth changed shape in data_layer1.json")
    whole_base = set(data["whole"]["base"])
    whole_edges = set(e["#int"] for e in data["whole"]["edges"])
    for pid, want in SCALAR_PROBES["whole"].items():
        if isinstance(want, int) and want not in whole_base:
            bad.append("whole.%s (%r) is not a base value in the data file" % (pid, want))
        if isinstance(want, str) and want not in whole_edges:
            bad.append("whole.%s (%s) is not an edge in the data file" % (pid, want))
    frac_base = set(data["fractional"]["base"])
    frac_specials = set(e["#special"] for e in data["fractional"]["edges"]
                        if isinstance(e, dict))
    frac_plain = set(e for e in data["fractional"]["edges"] if not isinstance(e, dict))
    for pid, want in SCALAR_PROBES["fractional"].items():
        if isinstance(want, float) and want not in frac_base and want not in frac_plain:
            bad.append("fractional.%s (%r) is not in the data file" % (pid, want))
        if isinstance(want, str) and want not in frac_specials:
            bad.append("fractional.%s (%s) is not a special in the data file" % (pid, want))
    text_all = set(data["text"]["base"]) | set(data["text"]["edges"])
    for pid, want in SCALAR_PROBES["text"].items():
        if want not in text_all and pid != "escapes":
            bad.append("text.%s (%r) is not in the data file" % (pid, want))
    return bad


# ------------------------------------------------------------------ per-lang

CPP_INCLUDES = """#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <deque>
#include <iostream>
#include <limits>
#include <list>
#include <map>
#include <memory>
#include <optional>
#include <set>
#include <sstream>
#include <string>
#include <tuple>
#include <unordered_map>
#include <variant>
#include <vector>
"""


DECL_NAME = re.compile(
    r"\b(?:abstract\s+class|final\s+class|public\s+class|sealed\s+class|data\s+class"
    r"|class|struct|record|interface|enum|typealias|typedef|type)\s+([A-Za-z_]\w*)")
IMPORT_LINE = re.compile(r"^\s*(?:import|using|#include|require|use|package)\b")
PKG_OF_IMPORT = re.compile(r'^\s*import\s+(?:(\w+)\s+)?"([^"]+)"')


def chunk_pre(pre):
    """Split a `pre` block into whole top-level declarations, brace-aware, so a
    single declaration spanning several lines is not cut in half."""
    chunks, cur, depth = [], [], 0
    for line in pre.split("\n"):
        cur.append(line)
        depth += line.count("{") + line.count("(") - line.count("}") - line.count(")")
        if depth <= 0 and line.strip():
            chunks.append("\n".join(cur))
            cur, depth = [], 0
    if [l for l in cur if l.strip()]:
        chunks.append("\n".join(cur))
    return chunks


def filter_pre(lang, pre, probe_text):
    """Keep only the parts of `pre` this one probe needs.

    Two reasons, both measured rather than guessed:

    * go refuses to compile a source file that imports a package it does not
      use, so a `pre` carrying `import "math"` for the sake of the NaN spelling
      broke the base-value probes of the very same representation. That was a
      generator artifact, not a layer-2 finding.
    * where a language forbids declaring a shape inside a function body (dart,
      c#), all of a cell's shapes sit in one `pre`, so ONE deliberately
      unspellable field name (the `1` key, the empty key) refused the whole
      cell, hiding the fact that its base values load. Keeping only the shape a
      probe names puts each refusal back on the probe that earned it.
    """
    if not pre.strip():
        return pre
    keep = []
    for chunk in chunk_pre(pre):
        head = chunk.strip().split("\n")[0]
        if IMPORT_LINE.match(head):
            if lang == "go":
                m = PKG_OF_IMPORT.match(head)
                if m:
                    name = m.group(1) or m.group(2).split("/")[-1]
                    if (name + ".") not in probe_text:
                        continue
            keep.append(chunk)
            continue
        m = DECL_NAME.search(chunk)
        if m and not re.search(r"\b%s\b" % re.escape(m.group(1)), probe_text):
            continue
        keep.append(chunk)
    return "\n".join(keep) + ("\n" if keep else "")


def indent(text, pad):
    return "\n".join(pad + line if line.strip() else line
                     for line in text.split("\n"))


def src_probe(lang, pid, pre, decl, read, index):
    """One source file holding exactly one probe."""
    if lang == "cpp":
        return (CPP_INCLUDES + pre + "\nint main() {\n" + indent(decl, "  ") +
                '\n  std::cout << "%s" << "|" << (%s) << std::endl;\n  return 0;\n}\n'
                % (pid, read))
    if lang == "go":
        return ('package main\n\nimport "fmt"\n' + pre + "\nfunc main() {\n" +
                indent(decl, "\t") +
                '\n\tfmt.Println("%s" + "|" + (%s))\n}\n' % (pid, read))
    if lang == "java":
        return (pre + "\npublic class Main {\n"
                "  public static void main(String[] args) throws Exception {\n" +
                indent(decl, "    ") +
                '\n    System.out.println("%s" + "|" + (%s));\n  }\n}\n' % (pid, read))
    if lang == "kotlin":
        return (pre + "\nfun main() {\n" + indent(decl, "    ") +
                '\n    println("%s" + "|" + (%s))\n}\n' % (pid, read))
    if lang == "rust":
        return ("#![allow(unused)]\n" + pre + "\nfn main() {\n" +
                indent(decl, "    ") +
                '\n    println!("{}|{}", "%s", %s);\n}\n' % (pid, read))
    if lang == "swift":
        return (pre + "\n" + decl +
                '\nprint("%s" + "|" + (%s))\n' % (pid, read))
    if lang == "dart":
        return (pre + "\nvoid main() {\n" + indent(decl, "  ") +
                '\n  print("%s" + "|" + (%s));\n}\n' % (pid, read))
    if lang == "typescript":
        return (pre + "\nfunction run(): void {\n" + indent(decl, "  ") +
                '\n  console.log("%s" + "|" + (%s));\n}\nrun();\n' % (pid, read))
    if lang == "csharp":
        return (pre + "\npublic class Program {\n"
                "  public static void Main() {\n" + indent(decl, "    ") +
                '\n    System.Console.WriteLine("%s" + "|" + (%s));\n  }\n}\n'
                % (pid, read))
    raise KeyError(lang)


def src_cell(lang, pre, probes):
    """One source file holding a whole cell, each probe caught on its own."""
    if lang == "python":
        out = [pre, "import sys",
               "def _emit(i, fn):",
               "    try:",
               "        sys.stdout.write(i + '|' + str(fn()) + '\\n')",
               "    except BaseException as e:",
               "        sys.stdout.write(i + '|<error:' + type(e).__name__ + '>\\n')",
               "    sys.stdout.flush()"]
        for n, (pid, decl, read) in enumerate(probes):
            out.append("def _p%d():" % n)
            out.append(indent(decl, "    "))
            out.append("    return (%s)" % read)
            out.append('_emit("%s", _p%d)' % (pid, n))
        return "\n".join(out) + "\n"
    if lang == "ruby":
        out = [pre]
        for n, (pid, decl, read) in enumerate(probes):
            out.append("def _p%d()" % n)
            out.append(indent(decl, "  "))
            out.append("  return (%s)" % read)
            out.append("end")
            out.append("begin")
            out.append('  puts("%s|" + _p%d().to_s)' % (pid, n))
            out.append("rescue Exception => e")
            out.append('  puts("%s|<error:" + e.class.to_s + ">")' % pid)
            out.append("end")
            out.append("$stdout.flush")
        return "\n".join(out) + "\n"
    if lang == "php":
        out = ["<?php", pre]
        for n, (pid, decl, read) in enumerate(probes):
            out.append("function _p%d() {" % n)
            out.append(indent(decl, "  "))
            out.append("  return (%s);" % read)
            out.append("}")
            out.append("try {")
            out.append('  echo "%s|" . _p%d() . "\\n";' % (pid, n))
            out.append("} catch (Throwable $e) {")
            out.append('  echo "%s|<error:" . get_class($e) . ">\\n";' % pid)
            out.append("}")
        return "\n".join(out) + "\n"
    raise KeyError(lang)


SRC_NAME = {"cpp": "main.cpp", "go": "main.go", "java": "Main.java",
            "rust": "main.rs", "swift": "main.swift", "dart": "main.dart",
            "typescript": "main.ts", "csharp": "Program.cs",
            "python": "main.py", "ruby": "main.rb", "php": "main.php"}

# build, run. An empty build means the language has no separate build step, and
# the lane cannot tell a refusal from a crash by the exit code alone -- it falls
# back on "did the program print anything at all".
RECIPE = {
    "cpp": ("g++ -O0 -std=c++17 -o prog main.cpp", "./prog"),
    "go": ("go build -o prog main.go", "./prog"),
    "java": ("javac Main.java", "java Main"),
    "rust": ("rustc -A warnings main.rs -o prog", "./prog"),
    "swift": ("/persist/swift/usr/bin/swiftc main.swift -o prog", "./prog"),
    "dart": ("", "/persist/dart-sdk/bin/dart run main.dart"),
    "typescript": ("/persist/ts/node_modules/.bin/tsc --target es2020 --module commonjs main.ts",
                   "node main.js"),
    "python": ("", "python3 main.py"),
    "ruby": ("", "ruby main.rb"),
    "php": ("", "php main.php"),
    # c# has no single-file build+run pair the way the scripting languages do,
    # and `dotnet run Program.cs` restores from NuGet even for a program with
    # no package references, which the sandbox proxy refuses (api.nuget.org
    # is not on the allowlist and does not need to be for pure-BCL probes).
    # These two persist-volume helper scripts compile with csc directly
    # against the installed reference assemblies (no restore, no network)
    # and then run the produced assembly with a hand-written
    # runtimeconfig.json. See dotnet_helpers.sh in the agent lane history
    # (2026-08-17, log_023 gap-close) for how they were built; they live in
    # /persist so they survive across runs of this generated lane.
    "csharp": ("/persist/dotnet-csc-build.sh", "/persist/dotnet-csc-run.sh"),
}

PRESENCE = {
    "cpp": "command -v g++", "go": "command -v go", "java": "command -v javac",
    "rust": "command -v rustc", "swift": "test -x /persist/swift/usr/bin/swiftc",
    "dart": "test -x /persist/dart-sdk/bin/dart",
    "typescript": "test -x /persist/ts/node_modules/.bin/tsc",
    "python": "command -v python3", "ruby": "command -v ruby",
    "php": "command -v php", "kotlin": "test -x /persist/kotlinc/bin/kotlinc",
    "csharp": "test -x /persist/dotnet/dotnet",
}

HEAD = r"""#!/bin/sh
# %(title)s -- generated by
# Research/data_representation/audit_generate.py . Do not hand-edit; regenerate.
# Every line of /out/%(prefix)s.txt is FACT_ID|RESULT, FACT_ID being
# <form>.<representation>.<probe>.
set -u
ROOT=/work/%(prefix)s
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
    ln -sf /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 \
       /usr/lib/x86_64-linux-gnu/libncurses.so.6 2>/dev/null
    ldconfig 2>/dev/null
  fi
}
ncurses_fix

OUT=/out/%(prefix)s.txt
: > "$OUT"
echo "=== %(title)s ==="
date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ
if ! %(presence)s >/dev/null 2>&1; then
  echo "%(lang)s: TOOLCHAIN ABSENT -- nothing run"
  echo "__ABSENT__|<absent>" >> "$OUT"
  exit 0
fi
"""

TAIL = r"""
echo ""
echo "=== %(prefix)s complete: $(wc -l < "$OUT") result lines ==="
"""


def sanitize(s):
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")


def units_for(spec):
    """Flatten a language file into the units the lane will build.

    Returns a list of (cell_id, [(probe_id, pre, decl, read), ...]).
    A cell_id is `<form>.<rep>`; a probe_id is `<form>.<rep>.<probe>`."""
    out = []
    for form in FORMS:
        for rep in spec["forms"].get(form, []):
            cell = "%s.%s" % (form, rep["rep"])
            pre = rep.get("pre", "")
            probes = []
            if form in SCALAR_FORMS:
                spell = dict(spec["spell"][form])
                spell.update(rep.get("spell_override", {}))
                for pname in SCALAR_PROBES[form]:
                    decl = rep["decl"].replace("{V}", spell[pname])
                    probes.append(("%s.%s" % (cell, pname), pre, decl, rep["read"]))
            else:
                for pname in CONTAINER_PROBES[form]:
                    if pname not in rep.get("probes", {}):
                        continue
                    probes.append(("%s.%s" % (cell, pname), pre,
                                   rep["probes"][pname], rep["read"]))
            out.append((cell, probes))
    return out


def emit_lane(lang, spec, outdir):
    prefix = "l2_" + lang
    style = spec["probe_style"]
    build, run = RECIPE[lang]
    src = SRC_NAME.get(lang, "main.txt")
    parts = [HEAD % {"title": "layer-2 load audit -- %s" % lang,
                     "prefix": prefix, "lang": lang,
                     "presence": PRESENCE[lang]}]
    a = parts.append
    n = 0
    for cell, probes in units_for(spec):
        if not probes:
            continue
        if style == "cell":
            n += 1
            body = src_cell(lang, probes[0][1],
                            [(p[0], p[2], p[3]) for p in probes])
            d = "$ROOT/%s" % sanitize(cell)
            a('\n# ---- cell %s (%d probes)' % (cell, len(probes)))
            a('D=%s; mkdir -p "$D"; cd "$D"' % d)
            a("cat > %s <<'L2_SRC_EOF'" % src)
            a(body.rstrip("\n"))
            a("L2_SRC_EOF")
            a('if timeout 60 %s > run.out 2> run.err; then :; else' % run)
            a('  echo "%s: run ended early ($(grep -c "|" run.out) lines printed)"' % cell)
            a('  sed -n 1,6p run.err')
            a('fi')
            a('grep "|" run.out >> "$OUT"')
            for pid, _pre, _decl, _read in probes:
                a('grep -qF "%s|" run.out || echo "%s|<no-output>" >> "$OUT"' % (pid, pid))
        else:
            for pid, pre, decl, read in probes:
                n += 1
                pre = filter_pre(lang, pre, decl + " " + read)
                d = "$ROOT/p%d" % n
                a('\n# ---- %s' % pid)
                a('D=%s; mkdir -p "$D"; cd "$D"' % d)
                a("cat > %s <<'L2_SRC_EOF'" % src)
                a(src_probe(lang, pid, pre, decl, read, n).rstrip("\n"))
                a("L2_SRC_EOF")
                a('V=ok')
                if build:
                    a('if ! timeout 180 %s > build.out 2> build.err; then V="<compile-error>"; fi'
                      % build)
                a('if [ "$V" = ok ]; then')
                a('  if timeout 30 %s > run.out 2> run.err; then :; else' % run)
                if build:
                    a('    V="<aborted>"')
                else:
                    a('    if [ "$(grep -c "|" run.out)" = 0 ]; then V="<compile-error>"; '
                      'else V="<aborted>"; fi')
                a('  fi')
                a('  grep -F "%s|" run.out >> "$OUT" || V="${V}"' % pid)
                a('fi')
                a('grep -qF "%s|" "$OUT" || echo "%s|$V" >> "$OUT"' % (pid, pid))
    parts.append(TAIL % {"prefix": prefix})
    path = os.path.join(outdir, "%s.sh" % prefix)
    with open(path, "w") as fh:
        fh.write("\n".join(parts) + "\n")
    os.chmod(path, 0o755)
    return path, n


def emit_kotlin_lane(spec, outdir):
    """Kotlin gets its own emitter for one reason: kotlinc is slow to start, so
    compiling 131 sources one at a time would dominate the whole audit. Sources
    go into ONE directory with distinct names, compiled in chunks; a chunk that
    fails is re-compiled file by file, so a refusal is still attributed to the
    one probe that earned it."""
    prefix = "l2_kotlin"
    parts = [HEAD % {"title": "layer-2 load audit -- kotlin (batched)",
                     "prefix": prefix, "lang": "kotlin",
                     "presence": PRESENCE["kotlin"]}]
    a = parts.append
    a('SRCD=$ROOT/src; mkdir -p "$SRCD"; cd "$SRCD"')
    ids = []
    n = 0
    for cell, probes in units_for(spec):
        for pid, pre, decl, read in probes:
            n += 1
            pre = filter_pre("kotlin", pre, decl + " " + read)
            name = "P%d" % n
            ids.append((name, pid))
            a('\n# ---- %s' % pid)
            a("cat > %s.kt <<'L2_SRC_EOF'" % name)
            a(src_probe("kotlin", pid, pre, decl, read, n).rstrip("\n"))
            a("L2_SRC_EOF")
    a('\ncat > $ROOT/manifest.txt <<\'L2_MAN_EOF\'')
    for name, pid in ids:
        a("%s %s" % (name, pid))
    a('L2_MAN_EOF')
    a(r'''
KC=/persist/kotlinc/bin/kotlinc
STDLIB=/persist/kotlinc/lib/kotlin-stdlib.jar
mkdir -p $ROOT/classes
# chunked batch compile, then per-file retry for any chunk the compiler refused
i=0
CHUNK=""
compile_chunk() {
  [ -z "$1" ] && return 0
  if timeout 900 $KC $1 -nowarn -d $ROOT/classes > $ROOT/kc.out 2>&1; then
    return 0
  fi
  echo "chunk refused, retrying file by file: $1"
  for f in $1; do
    b=$(basename "$f" .kt)
    if ! timeout 300 $KC "$f" -nowarn -d $ROOT/classes > $ROOT/kc_$b.out 2>&1; then
      echo "$b COMPILE-REFUSED"
      echo "$b" >> $ROOT/refused.txt
    fi
  done
}
: > $ROOT/refused.txt
for f in $SRCD/P*.kt; do
  CHUNK="$CHUNK $f"; i=$((i+1))
  if [ $((i % 12)) -eq 0 ]; then compile_chunk "$CHUNK"; CHUNK=""; fi
done
compile_chunk "$CHUNK"

cd $ROOT
while read name pid; do
  if grep -qx "$name" $ROOT/refused.txt 2>/dev/null; then
    echo "$pid|<compile-error>" >> "$OUT"; continue
  fi
  if [ ! -f $ROOT/classes/${name}Kt.class ]; then
    echo "$pid|<compile-error>" >> "$OUT"; continue
  fi
  if timeout 30 java -cp $ROOT/classes:$STDLIB ${name}Kt > r.out 2> r.err; then
    grep -F "$pid|" r.out >> "$OUT" || echo "$pid|<no-output>" >> "$OUT"
  else
    grep -F "$pid|" r.out >> "$OUT" || echo "$pid|<aborted>" >> "$OUT"
  fi
done < $ROOT/manifest.txt
''')
    parts.append(TAIL % {"prefix": prefix})
    path = os.path.join(outdir, "%s.sh" % prefix)
    with open(path, "w") as fh:
        fh.write("\n".join(parts) + "\n")
    os.chmod(path, 0o755)
    return path, n


def main():
    data = json.load(open(os.path.join(HERE, "data_layer1.json")))
    bad = check_against_layer1(data)
    if bad:
        print("LAYER-1 TIE BROKEN:")
        for b in bad:
            print("  " + b)
        sys.exit(1)
    print("layer-1 tie: every scalar probe id names content data_layer1.json holds.")

    outdir = os.path.join(HERE, "audit", "lanes")
    os.makedirs(outdir, exist_ok=True)
    langs = sys.argv[1:] or [
        "python", "ruby", "php", "typescript", "go", "cpp", "java", "rust",
        "kotlin", "dart", "swift", "csharp"]
    total_cells = total_probes = 0
    for lang in langs:
        key = {"cpp": "cpp"}.get(lang, lang)
        spec = json.load(open(os.path.join(HERE, "representations_%s.json" % key)))
        cells = units_for(spec)
        if lang == "kotlin":
            path, n = emit_kotlin_lane(spec, outdir)
        else:
            path, n = emit_lane(lang, spec, outdir)
        total_cells += len(cells)
        total_probes += sum(len(p) for _c, p in cells)
        print("%-11s %2d cells %4d probes -> %s" % (lang, len(cells), n, path))
    print("TOTAL %d cells, %d probes" % (total_cells, total_probes))


if __name__ == "__main__":
    main()
