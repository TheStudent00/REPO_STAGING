#!/usr/bin/env python3
"""declare_lane.py -- the DECLARATION lane: one tiny compile per type.

WHAT THIS ASKS THE COMPILER
---------------------------
`type_inventory2.json` records, per language, every type spelling an
AUTHORITY admits -- the compiler's own type table, the grammar, the
stdlib source, the installed module interface.  That is the witness
"this toolchain KNOWS the spelling".  It is not the witness "this
toolchain ACCEPTS the spelling on this target, with the flags the probe
lanes use".  Correction 3 of round 9 measured the gap: about 91,000 of
the regeneration's 100,265 refusals are the compiler rejecting the
probe's TYPE DECLARATION, not its operator.

This program asks the second question, once per type per language, with
NO operator in the source at all:

    form `variable`   -- a variable declaration of that type, nothing else
    form `parameter`  -- the type in the position a probe puts it in
                         (a function parameter), nothing else

Both forms are recorded.  `parameter` is the load-bearing one, because a
probe holder IS a parameter; `__fp16` is the type for which the two
answers differ, and recording both is what makes that visible rather
than assumed.

THE FLAGS ARE THE PROBE LANES' OWN
----------------------------------
Copied from `lane_gen.py :: compile_probe`, anchor mode:

    c      /usr/bin/clang   -std=c17    -O0 -g -c
    cpp    /usr/bin/clang++ -std=c++20  -O0 -g -c
    rust   rustc --crate-type=lib --emit=obj -C opt-level=0 -g
    go     go build -gcflags="-N -l"
    swift  /persist/swift/usr/bin/swiftc -Onone -g -c

The headers and the function shape are copied from `probe_gen.py`'s
emitters, so the declaration sits in the same dialect the probe sits in.

VERBATIM CAPTURE
----------------
The lane writes pipe-delimited records and escapes every field with the
codec of record (`verbatim_diag.encode`, copied into the driver at
generation time, exactly as `lane_gen_verbatim.py` does it), so a `|` or
a `;` in the compiler's words survives.  The FULL diagnostic text is
stored, not only its first line.  The product opens with the marker
`#verbatim-escape v1`; a product without the marker is refused rather
than decoded.

THE SPELLING BAN
----------------
No operator token appears anywhere in this program or in what it writes.
Its subject is TYPES; every type spelling rides on an object carrying
`language` and `id`, with the spelling in a `spelling` display field.

usage:
    /tmp/reconnect_venv/bin/python3 declare_lane.py c cpp go rust swift
writes:
    declare_lanes/declare_<lang>.sh
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import lane_gen                                            # noqa: E402
import verbatim_diag                                       # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]
LANE_DIR = os.path.join(HERE, "declare_lanes")

C_HEAD = ["#include <stdint.h>", "#include <stdbool.h>"]
CPP_HEAD = ["#include <cstdint>", "#include <compare>", "#include <new>"]


def source_variable(lang, spelling):
    """a variable declaration of the type, and nothing else."""
    if lang == "c":
        lines = list(C_HEAD)
        lines.append("")
        lines.append("static %s declared_value;" % spelling)
        return "\n".join(lines) + "\n"
    if lang == "cpp":
        lines = list(CPP_HEAD)
        lines.append("")
        lines.append("static %s declared_value;" % spelling)
        return "\n".join(lines) + "\n"
    if lang == "go":
        lines = ["package main", "",
                 "var declaredValue %s" % spelling,
                 "",
                 "func main() {",
                 "\t_ = declaredValue",
                 "}"]
        return "\n".join(lines) + "\n"
    if lang == "rust":
        lines = ["#[no_mangle]",
                 "pub fn declared_value() {",
                 "    let _v: %s;" % spelling,
                 "}"]
        return "\n".join(lines) + "\n"
    if lang == "swift":
        lines = ["public func declaredValue() {",
                 "    let _v: %s? = nil" % spelling,
                 "    _ = _v",
                 "}"]
        return "\n".join(lines) + "\n"
    raise KeyError(lang)


def source_parameter(lang, spelling):
    """the type in the position a probe puts it in: a parameter."""
    if lang == "c":
        lines = list(C_HEAD)
        lines.append("")
        lines.append("void declared_holder(%s a)" % spelling)
        lines.append("{")
        lines.append("    (void)0;")
        lines.append("}")
        return "\n".join(lines) + "\n"
    if lang == "cpp":
        lines = list(CPP_HEAD)
        lines.append("")
        lines.append('extern "C" void')
        lines.append("declared_holder(%s a)" % spelling)
        lines.append("{")
        lines.append("    (void)0;")
        lines.append("}")
        return "\n".join(lines) + "\n"
    if lang == "go":
        lines = ["package main", "",
                 "//go:noinline",
                 "func declaredHolder(a %s) {" % spelling,
                 "\t_ = a",
                 "}",
                 "",
                 "var declaredValue %s" % spelling,
                 "",
                 "func main() {",
                 "\tdeclaredHolder(declaredValue)",
                 "}"]
        return "\n".join(lines) + "\n"
    if lang == "rust":
        lines = ["#[no_mangle]",
                 "pub fn declared_holder(a: %s) {" % spelling,
                 "    let _ = a;",
                 "}"]
        return "\n".join(lines) + "\n"
    if lang == "swift":
        lines = ["public func declaredHolder(_ a: %s) {" % spelling,
                 "    _ = a",
                 "}"]
        return "\n".join(lines) + "\n"
    raise KeyError(lang)


DRIVER = r'''
import json
import os
import subprocess
import sys

ROOT = sys.argv[1]
TABLE = json.load(open(os.path.join(ROOT, "table.json")))
LANG = TABLE["language"]
OUT = TABLE["out"]
WORK = os.path.join(ROOT, "u")

CLANG = "/usr/bin/clang"
CLANGXX = "/usr/bin/clang++"
SWIFTC = "/persist/swift/usr/bin/swiftc"
GOMOD = "module declprobe\n\ngo 1.26\n"


def sh(cmd, cwd=None, timeout=300):
    try:
        p = subprocess.run(cmd, cwd=cwd, timeout=timeout,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT after %ds" % timeout
    so = p.stdout.decode("utf-8", "replace")
    se = p.stderr.decode("utf-8", "replace")
    return p.returncode, so, se


def compile_one(source, d):
    if LANG == "c":
        src = os.path.join(d, "decl.c")
        open(src, "w").write(source)
        cmd = [CLANG, "-std=c17", "-O0", "-g", "-c", src,
               "-o", os.path.join(d, "decl.o")]
        rc, so, se = sh(cmd)
        return rc, (se or so)
    if LANG == "cpp":
        src = os.path.join(d, "decl.cpp")
        open(src, "w").write(source)
        cmd = [CLANGXX, "-std=c++20", "-O0", "-g", "-c", src,
               "-o", os.path.join(d, "decl.o")]
        rc, so, se = sh(cmd)
        return rc, (se or so)
    if LANG == "rust":
        src = os.path.join(d, "decl.rs")
        open(src, "w").write(source)
        cmd = ["rustc", "--crate-type=lib", "--emit=obj",
               "-C", "opt-level=0", "-g",
               "-o", os.path.join(d, "decl.o"), src]
        rc, so, se = sh(cmd)
        return rc, (se or so)
    if LANG == "go":
        open(os.path.join(d, "go.mod"), "w").write(GOMOD)
        open(os.path.join(d, "main.go"), "w").write(source)
        cmd = ["go", "build", "-gcflags=-N -l", "-o",
               os.path.join(d, "decl_bin"), "."]
        rc, so, se = sh(cmd, cwd=d)
        return rc, (se or so)
    if LANG == "swift":
        src = os.path.join(d, "decl.swift")
        open(src, "w").write(source)
        cmd = [SWIFTC, "-Onone", "-g", "-c", src,
               "-o", os.path.join(d, "decl.o")]
        rc, so, se = sh(cmd)
        return rc, (se or so)
    raise KeyError(LANG)


out = open(OUT, "w")
tally = {"submitted": 0, "accept": 0, "refuse": 0}
n = 0
for item in TABLE["items"]:
    n = n + 1
    d = os.path.join(WORK, "d%05d" % n)
    subprocess.run(["rm", "-rf", d])
    os.makedirs(d)
    rc, diag = compile_one(item["source"], d)
    tally["submitted"] = tally["submitted"] + 1
    if rc == 0:
        tally["accept"] = tally["accept"] + 1
        verdict = "ACCEPT"
    else:
        tally["refuse"] = tally["refuse"] + 1
        verdict = "REFUSE"
    out.write("%s|%s|%s|%s\n" % (esc(item["id"]), esc(item["form"]),
                                 verdict, esc(diag.strip())))
    out.flush()
    subprocess.run(["rm", "-rf", d])
    if n % 25 == 0:
        print("  %d of %d" % (n, len(TABLE["items"])))
        sys.stdout.flush()

out.close()
print("done: %s -> %s" % (json.dumps(tally), OUT))
'''


def driver_text():
    """the driver with the verbatim codec copied in, marker written first."""
    head = ("\n# --- verbatim delimiter codec, copied from verbatim_diag.py "
            "---\n")
    import inspect
    body = inspect.getsource(verbatim_diag.encode).replace("def encode(",
                                                           "def esc(")
    codec = head + body + "\n_ENC = " + repr(verbatim_diag._ENC) + "\n"
    codec = codec + "MARKER = " + repr(verbatim_diag.MARKER) + "\n"
    text = DRIVER
    marker_line = 'out = open(OUT, "w")\n'
    if text.count(marker_line) != 1:
        raise SystemExit("declare_lane: driver anchor not found once")
    text = text.replace(marker_line,
                        marker_line + "out.write(MARKER + '\\n')\n")
    return codec + text


TOOLCHECK = lane_gen.TOOLCHECK


def lane(lang, items, outname):
    check, why = TOOLCHECK[lang]
    table = dict(language=lang, out="/out/%s.txt" % outname, items=items)
    name = "decl_%s" % lang
    body = []
    body.append("#!/bin/sh")
    body.append("# declaration lane -- %s -- generated by" % lang)
    body.append("# Research/op_pipeline/declare_lane.py .  Do not hand-edit.")
    body.append("# one tiny compile per type per form; no operator anywhere.")
    body.append("set -u")
    body.append("export HOME=/work")
    body.append("export PATH=/persist/swift/usr/bin:$PATH")
    body.append("export GOTOOLCHAIN=local")
    body.append("export GOPROXY=off")
    body.append("export GOFLAGS=-mod=mod")
    body.append("ROOT=/work/%s" % name)
    body.append("export GOCACHE=\"$ROOT/gocache\"")
    body.append("export GOPATH=\"$ROOT/gopath\"")
    body.append("# swift's binaries want libncurses.so.6 and the image ships")
    body.append("# only libncursesw.so.6.6; the symlink lives in the image's")
    body.append("# own /usr/lib and does NOT survive a container restart.")
    body.append("if [ -f /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 ]; then")
    body.append("  ln -sf /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 \\")
    body.append("     /usr/lib/x86_64-linux-gnu/libncurses.so.6 2>/dev/null")
    body.append("  ldconfig 2>/dev/null")
    body.append("fi")
    body.append("echo \"=== declaration lane -- %s -- %d declarations ===\""
                % (lang, len(items)))
    body.append("date -u +%Y-%m-%dT%H:%M:%SZ")
    body.append("if ! %s >/dev/null 2>&1; then" % check)
    body.append("  echo \"!! REFUSING TO START: %s.\"" % why)
    body.append("  exit 4")
    body.append("fi")
    body.append("%s 2>&1 | head -2" % check)
    body.append("rm -rf \"$ROOT\"; mkdir -p \"$ROOT\" \"$GOCACHE\" \"$GOPATH\"")
    body.append("mkdir -p \"$ROOT/u\"")
    body.append("base64 -d <<'T_EOF' | gunzip > \"$ROOT/table.json\"")
    body.append(lane_gen.payload(table))
    body.append("T_EOF")
    body.append("echo \"payload bytes: $(wc -c < \"$ROOT/table.json\")\"")
    body.append("python3 - \"$ROOT\" <<'PY_EOF'")
    body.append(driver_text())
    body.append("PY_EOF")
    body.append("echo \"--- lane finished, rc=$?\"")
    body.append("date -u +%Y-%m-%dT%H:%M:%SZ")
    return "\n".join(body) + "\n"


def items_for(lang, inv):
    """one item per (type, form).  Compiler-table ids carrying `::` are
    excluded: they are not source spellings, so no declaration can be
    written with them.  `core_rule2.scalar_core` excludes them by the same
    test, which is where this exclusion is copied from."""
    out = []
    excluded = []
    for entry in inv["languages"][lang]["types"]:
        spelling = entry["spelling"]
        if "::" in spelling:
            excluded.append(entry["id"])
            continue
        out.append({"language": lang, "id": entry["id"],
                    "spelling": spelling, "form": "variable",
                    "source": source_variable(lang, spelling)})
        out.append({"language": lang, "id": entry["id"],
                    "spelling": spelling, "form": "parameter",
                    "source": source_parameter(lang, spelling)})
    return out, excluded


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("langs", nargs="+")
    args = ap.parse_args()
    inv = json.load(open(os.path.join(HERE, "type_inventory2.json")))
    if not os.path.isdir(LANE_DIR):
        os.makedirs(LANE_DIR)
    for lang in args.langs:
        items, excluded = items_for(lang, inv)
        text = lane(lang, items, "decl_%s" % lang)
        path = os.path.join(LANE_DIR, "declare_%s.sh" % lang)
        fh = open(path, "w")
        fh.write(text)
        fh.close()
        print("%-6s %4d declarations (%d types x 2 forms), "
              "%d table ids excluded -> %s"
              % (lang, len(items), len(items) // 2, len(excluded), path))


if __name__ == "__main__":
    main()
