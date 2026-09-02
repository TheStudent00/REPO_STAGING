#!/usr/bin/env python3
"""generate_run.py -- turn a census page's vectors into one SandboxDesign lane
script.

Plain words first: this reads a `vectors_<object>.json` file (every census fact
on one page, written out as tiny probes), pastes each probe into the matching
per-language runner template, and writes ONE shell script that compiles and
runs every language's program inside the sandbox container, dropping
`FACT.PROBE|RESULT` lines into /out. The lane is serial, so one script is the
honest shape: languages run one after another and a failure in a late one
cannot lose the earlier results.

Three things every probe may carry:

* PROGRAM. `main` holds everything safe to compile; any other name gets its
  own tiny program, so a probe a compiler is expected to REFUSE, or a probe
  that may kill the process, cannot take the rest of the batch down with it.
* EXPR. Either one shared C-ish string (the boolean/float style) or a mapping
  from language to that language's own text. The heavy census pages need the
  mapping: there is no single expression that means "add one to the largest
  integer" in eleven languages.
* ONLY / SKIP. Language lists, for probes that exist in one camp alone.

Where a probe's body needs statements rather than an expression, the body
lives in a PREAMBLE file, `templates/<lang>.<object>.pre`, as a named function
returning this run's shared string type, and the probe's expr is just the call.
That keeps the vectors file readable as a work order and keeps real code in
real source files where a compiler can see it.

Build and run are separate steps, so the lane can tell the two failures apart:
a program the compiler REFUSED records `<compile-error>` for its probes; a
program that built and then died records `<aborted>`. Both are results.

Usage:  python3 generate_run.py --vectors vectors_integer.json
"""

import argparse
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

DEFAULT_RUN_ORDER = [
    "python", "ruby", "php", "typescript", "go",
    "cpp", "java", "rust", "rust-release", "kotlin", "dart", "dart-web",
    "swift",
]

# which template (and therefore which source text) a run mode uses
TEMPLATE_OF = {"rust-release": "rust", "dart-web": "dart"}

SRC_NAME = {
    "python": "main.py", "ruby": "main.rb", "php": "main.php",
    "typescript": "main.ts", "go": "main.go", "cpp": "main.cpp",
    "java": "Main.java", "rust": "main.rs", "kotlin": "main.kt",
    "swift": "main.swift", "dart": "main.dart",
}


def dialect(lang, expr):
    """The only places a SHARED C-ish expression has to bend. Per-language
    expressions never pass through here -- they are already that language."""
    if lang == "python":
        expr = re.sub(r"\btrue\b", "True", expr)
        expr = re.sub(r"\bfalse\b", "False", expr)
        expr = expr.replace("||", " or ").replace("&&", " and ")
    if lang == "cpp":
        # <cmath> already owns the name nan(); the template spells it nan_()
        expr = re.sub(r"\bnan\(\)", "nan_()", expr)
    return expr


def base_of(lang):
    return TEMPLATE_OF.get(lang, lang)


def load_templates(lang, object_key, program="main"):
    """Body, probe pattern, preamble. The preamble is the base file for this
    language and object, plus -- if it exists -- a file for THIS program only.
    The per-program file exists because a preamble is pasted into every program
    a language runs, and one compiler (dart's web compiler) refuses a source
    text merely for CONTAINING a literal it cannot represent. Parking such a
    body in the program that needs it keeps the refusal where the finding is."""
    base = base_of(lang)
    with open(os.path.join(HERE, "templates", base + ".tmpl")) as fh:
        body = fh.read()
    with open(os.path.join(HERE, "templates", base + ".probe")) as fh:
        probe = fh.read().rstrip("\n")
    pre = ""
    if object_key:
        for name in ("%s.%s.pre" % (base, object_key),
                     "%s.%s.%s.pre" % (base, object_key, program)):
            path = os.path.join(HERE, "templates", name)
            if os.path.exists(path):
                pre += open(path).read()
    return body, probe, pre


def expr_for(p, lang):
    """Resolve a probe's text for one language, or None if it has none."""
    e = p["expr"]
    if isinstance(e, str):
        return dialect(lang, e), True
    base = base_of(lang)
    for key in (lang, base, "default"):
        if key in e:
            return e[key], False
    return None, False


def probes_for(vectors, lang, program):
    """Every probe of every fact that belongs in this language's `program`."""
    out = []
    base = base_of(lang)
    for fact in vectors["facts"]:
        for p in fact["probes"]:
            if p.get("program", "main") != program:
                continue
            only = p.get("only")
            if only and base not in only and lang not in only:
                continue
            skip = p.get("skip")
            if skip and (base in skip or lang in skip):
                continue
            text, _shared = expr_for(p, lang)
            if text is None:
                continue
            out.append((fact["fact_id"] + "." + p["probe_id"],
                        p.get("type", "str"), text))
    return out


FMT_OF = {"bool": "fmtb", "float": "fmtf", "str": "fmts", "int": "fmts"}


def render(lang, vectors, program, object_key):
    body, probe_pat, pre = load_templates(lang, object_key, program)
    lines = []
    for pid, ptype, expr in probes_for(vectors, lang, program):
        stmt = probe_pat.replace("{ID}", pid)
        stmt = stmt.replace("{FMT}", FMT_OF.get(ptype, "fmts"))
        stmt = stmt.replace("{EXPR}", expr)
        lines.append(stmt)
    body = body.replace("{{PREAMBLE}}", pre)
    return body.replace("{{PROBES}}", "\n".join(lines))


# per-language recipe, split so the lane can tell a REFUSAL from a CRASH.
# An empty build means the language has no separate build step.
RECIPE = {
    "python": ("", "python3 main.py"),
    "ruby":   ("", "ruby main.rb"),
    "php":    ("", "php main.php"),
    "typescript": ("tsc --target es2020 --module commonjs main.ts", "node main.js"),
    "go":     ("go mod init probe >/dev/null 2>&1; go build -o prog main.go", "./prog"),
    "cpp":    ("g++ -O2 -std=c++17 -o prog main.cpp", "./prog"),
    "java":   ("javac Main.java", "java Main"),
    "rust":   ("rustc main.rs -o prog", "./prog"),
    "rust-release": ("rustc -O main.rs -o prog", "./prog"),
    "kotlin": ("/persist/kotlinc/bin/kotlinc main.kt -d classes",
               "java -cp classes:/persist/kotlinc/lib/kotlin-stdlib.jar MainKt"),
    "dart":   ("", "/persist/dart-sdk/bin/dart run main.dart"),
    "dart-web": ("/persist/dart-sdk/bin/dart compile js -O0 -o main.js main.dart",
                 "node main.js"),
    "swift":  ("/persist/swift/usr/bin/swiftc main.swift -o prog", "./prog"),
}

PRESENCE = {
    "python": "command -v python3", "ruby": "command -v ruby",
    "php": "command -v php", "typescript": "command -v tsc",
    "go": "command -v go", "cpp": "command -v g++",
    "java": "command -v javac", "rust": "command -v rustc",
    "rust-release": "command -v rustc",
    "kotlin": "test -x /persist/kotlinc/bin/kotlinc",
    "dart": "test -x /persist/dart-sdk/bin/dart",
    "dart-web": "test -x /persist/dart-sdk/bin/dart",
    "swift": "test -x /persist/swift/usr/bin/swiftc",
}

HEAD = r"""#!/bin/sh
# %(title)s -- generated by
# Research/dominant_intentions/harness/generate_run.py . Do not hand-edit;
# regenerate. Every line printed to /out/%(prefix)s_<lang>.txt is
# FACT.PROBE|RESULT.
set -u
ROOT=/work/%(prefix)s
rm -rf "$ROOT"; mkdir -p "$ROOT"
export HOME=/work
export GOFLAGS=-mod=mod
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

echo "=== %(title)s ==="
date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ
"""


def emit_lang(lang, vectors, programs, prefix, object_key):
    src = SRC_NAME[base_of(lang)]
    build, run = RECIPE[lang]
    parts = []
    a = parts.append
    a('\n# ---------------------------------------------------------------- %s' % lang)
    a('echo ""; echo "--- %s ---"' % lang)
    a('OUT=/out/%s_%s.txt' % (prefix, lang))
    a(': > "$OUT"')
    a('if %s >/dev/null 2>&1; then' % PRESENCE[lang])
    for program in programs:
        ids = [pid for pid, _t, _e in probes_for(vectors, lang, program)]
        if not ids:
            continue
        a('  D="$ROOT/%s/%s"; mkdir -p "$D"; cd "$D"' % (lang, program))
        a("  cat > %s <<'PROBE_SRC_EOF'" % src)
        a(render(lang, vectors, program, object_key).rstrip("\n"))
        a('PROBE_SRC_EOF')
        a('  VERDICT=ok')
        if build:
            a('  if ! (%s) > build.out 2> build.err; then' % build)
            a('    VERDICT="<compile-error>"')
            a('    echo "%s %s: BUILD REFUSED (may itself be the finding)"' % (lang, program))
            a('    sed -n 1,15p build.err; sed -n 1,15p build.out')
            a('  fi')
        a('  if [ "$VERDICT" = ok ]; then')
        a('    if ! (%s) > run.out 2> run.err; then' % run)
        if build:
            # the build already had its say; anything now is a crash
            a('      VERDICT="<aborted>"')
        else:
            # a build-less language has no separate refusal moment: if the
            # program printed nothing at all it never started, which IS a refusal
            a('      if [ "$(grep -c "|" run.out)" = 0 ]; then VERDICT="<compile-error>"; '
              'else VERDICT="<aborted>"; fi')
        a('      echo "%s %s: RUN ENDED $VERDICT (may itself be the finding)"' % (lang, program))
        a('      sed -n 1,15p run.err')
        a('    fi')
        # tsc reports type errors on STDOUT, so only lines carrying a pipe are
        # harvested; the first line for an id wins in compare.py.
        a('    grep "|" run.out >> "$OUT"')
        a('    echo "%s %s: $(grep -c "|" run.out) lines, verdict $VERDICT"' % (lang, program))
        a('  fi')
        a('  if [ "$VERDICT" != ok ]; then')
        for pid in ids:
            a('    echo "%s|$VERDICT" >> "$OUT"' % pid)
        a('  fi')
    a('else')
    a('  echo "%s: ABSENT -- skipped"' % lang)
    a('  echo "__ABSENT__|<absent>" >> "$OUT"')
    a('fi')
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vectors", default=os.path.join(HERE, "vectors_boolean_float.json"))
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    path = args.vectors
    if not os.path.isabs(path):
        path = os.path.join(HERE, path)
    with open(path) as fh:
        vectors = json.load(fh)

    prefix = vectors.get("run_prefix", "bf")
    object_key = vectors.get("object_key")
    order = vectors.get("run_order", DEFAULT_RUN_ORDER)
    out = args.out or os.path.join(HERE, "lane_%s.sh" % prefix)

    programs = ["main"]
    for fact in vectors["facts"]:
        for p in fact["probes"]:
            prog = p.get("program", "main")
            if prog not in programs:
                programs.append(prog)

    title = vectors.get("title", "%s run" % prefix)
    chunks = [HEAD % {"title": title, "prefix": prefix}]
    for lang in order:
        chunks.append(emit_lang(lang, vectors, programs, prefix, object_key))
    chunks.append('\necho ""\necho "=== run complete ==="\nls -l /out/%s_*.txt\n' % prefix)

    with open(out, "w") as fh:
        fh.write("\n".join(chunks) + "\n")
    os.chmod(out, 0o755)
    n = sum(len(f["probes"]) for f in vectors["facts"])
    print("wrote %s (%d facts, %d probe definitions, %d programs, %d language runs)"
          % (out, len(vectors["facts"]), n, len(programs), len(order)))


if __name__ == "__main__":
    main()
