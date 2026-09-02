#!/usr/bin/env python3
"""test_verbatim_roundtrip.py -- proof that the verbatim path stores the
compiler's words unaltered AND still parses.

Three checks, each printed with its verdict:

 1. CODEC        encode/decode is the identity on adversarial strings.
 2. DRIVER       the driver text produced by lane_gen_verbatim.py parses
                 as Python, contains no surviving substitution, and its
                 own `firstline`+`esc` pair turns a real rustc refusal
                 into a record line that (a) has the right field count
                 and (b) decodes back to the compiler's exact words.
 3. LEGACY       the same input through the CURRENT lane_gen.firstline
                 produces the altered text -- the defect reproduced, so
                 the fix is measured against a demonstrated defect and
                 not against a description of one.

Nothing existing is imported for modification; lane_gen is imported
read-only and its module-level DRIVER is restored by the wrapper.
"""

import ast
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import lane_gen                                            # noqa: E402
import lane_gen_verbatim                                   # noqa: E402
import verbatim_diag as V                                  # noqa: E402

RUSTC = (
    "error[E0277]: no implementation for `i32 | f64`\n"
    " --> unit.rs:5:13\n"
    "  |\n"
    "5 |     let c = a | b;\n"
    "  |             ^ no implementation for `i32 | f64`\n"
)
WANT = "error[E0277]: no implementation for `i32 | f64`"

fails = 0


def say(ok, what, detail=""):
    global fails
    if not ok:
        fails += 1
    print("%-4s %-34s %s" % ("ok" if ok else "FAIL", what, detail))


# 1 CODEC
for s in [WANT, "a || b", "a |= b; c", "back\\slash | ; end", ""]:
    say(V.decode(V.encode(s)) == s, "codec identity", repr(s)[:60])
    say("|" not in V.encode(s) and ";" not in V.encode(s),
        "codec removes delimiters", repr(V.encode(s))[:60])

# 2 DRIVER
driver, _ = lane_gen_verbatim.make_driver()
ast.parse(driver)
say(True, "driver parses as Python", "%d bytes" % len(driver))
say('replace("|", "/")' not in driver and 'replace(";", ",")' not in driver,
    "no substitution survives")
say(V.MARKER in driver, "driver announces the marker")

def driver_ns(text, tag):
    """run a driver's head (definitions only) and hand back its namespace.

    The driver is a program serialised into the lane script, not an
    importable module, so `firstline` exists only inside that text.
    Executing the head is how either version's own function is reached.
    """
    ns = {}
    head = text.split("t0 = time.time()")[0]
    head = head.replace(
        'T = json.load(open(os.path.join(ROOT, "table.json")))',
        'T = {"language": "x", "probes": [], "out": "/dev/null"}')
    head = head.replace('ROOT = sys.argv[1]', 'ROOT = "/tmp"')
    head = head.replace('out = open(OUT, "w")', 'import io\nout = io.StringIO()')
    exec(compile(head, tag, "exec"), ns)                   # noqa: S102
    return ns


ns = driver_ns(driver, "<driver-verbatim>")
line = "op_%d|REFUSED|%s\n" % (178, ns["esc"](ns["firstline"](RUSTC)))
say(line.count("|") == 2, "record has the right field count", repr(line))
parts = line.rstrip("\n").split("|")
say(V.decode(parts[2]) == WANT, "decodes to the compiler's words",
    repr(V.decode(parts[2])))

# 3 LEGACY -- the defect reproduced
legacy = driver_ns(lane_gen.DRIVER, "<driver-legacy>")["firstline"](RUSTC)
say(legacy == "error[E0277]: no implementation for `i32 / f64`",
    "legacy path reproduces defect", repr(legacy))
say(legacy != WANT, "legacy text is not verbatim")

print("\n%d failures" % fails)
sys.exit(1 if fails else 0)
