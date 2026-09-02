#!/usr/bin/env python3
"""l3_cart_gen.py -- emit the CARTESIAN lanes for the two languages of
this run (rust, static; ruby, open dispatch / route C).

Scope, the owner 2026-08-21: rust and ruby ONLY.  The other ten wait.

This is the settled probe design of `SUPPORT_conversion_spec.md`,
section "the probe design settled 2026-08-21".  It supersedes the
ladder-plus-shift design of logs 049/051 for all future runs.  Rejected
and NOT re-emitted here: the geometric ladder (never an interval sweep),
the constant-offset shifted pairing (`y - x` constant makes every
difference-only operator answer a constant vector), and comp1 with equal
operands (degenerate).

  LEVEL 1   `y = op(x0, x1)`, ALL ordered pairs from the shared set X.
  LEVEL 2   `z = op(op(x0, x1), op(x2, x3))`, all four operands from X'.

The two intermediates of level 2 are never enumerated, deduped, capped
or unioned -- they exist inside the expression.  Both languages evaluate
identical expressions on identical inputs, so rows compare position by
position with no alignment step.

LANE MECHANICS are the ones log_027 section 3 settled and every campaign
since has used -- reused, not reinvented:

  - a lane is a self-contained `/bin/sh` script dropped into
    `SandboxDesign/agent/drop/`; the daemon runs it and writes
    `agent/status/<name>.status`; products land in `/out`.
  - the payload travels gzip+base64 INSIDE the script.
  - rust: one rustc compile per chunk, `-C debug-assertions=on
    -C opt-level=0`, with `unconditional_panic` and `arithmetic_overflow`
    allowed so an accepted probe still compiles; the panic happens at run
    time, is caught by `catch_unwind` and recorded `RAISE:panic`.  A
    failing chunk is BISECTED to the individual probe rather than
    condemning the whole chunk to BUILDFAIL.
  - ruby: an `eval` per probe under begin/rescue, address space capped,
    and a runner that restarts the driver past any probe that stopped it,
    recording that probe as an ABORT.

THE RUBY STALL BUDGET IS 2 SECONDS (was 10).  Recorded change, the owner
2026-08-21: the previous run spent 550 s of its 557 s wall clock waiting
on `**` with BigDecimal.  A stall is recorded as ABORT and an ABORT is
excluded from scoring, in the numerator and the denominator both, so
shortening the budget loses no measurement -- only wall clock.

RUBY OPERATOR MENU.  `and` and `or` are added to the ruby menu for this
run.  They are required by the design's own sanity check: ruby's
`&&`/`||`/`and`/`or` RETURN AN OPERAND rather than a truth value, and
`&&` against `and` is the positive control that says the harness is
measuring what it claims to.

RUBY PARALLELISM.  Level 2 is millions of probes and the daemon runs one
script at a time with an hour's timeout, so the ruby level-2 lane shards
its probe list across W worker processes inside the one script.  Each
worker is the SAME driver with the SAME restart-past-a-stall discipline;
sharding replicates the runner, it does not replace it.

RUST LEVEL-2 TYPE VALIDITY.  `op(y, y)` has to typecheck.  `y`'s type is
read out of the level-1 lane output (whose answered lines carry
`std::any::type_name`) and the level-2 probe is emitted only where
`(op, ty, ty)` is an ACCEPT cell in `acceptance_rust_A2.json`.  No
cast-and-catch and no speculative compile.  ruby is route C and has no
such question -- everything is eval'd.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.
"""

import base64
import collections
import gzip
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

LANES = os.path.join(HERE, "lanes")
DROP = os.path.abspath(os.path.join(HERE, "..", "..", "..",
                                    "SandboxDesign", "agent", "drop"))
RAW = os.path.join(HERE, "raw")
LANE_OUT = os.path.abspath(os.path.join(HERE, "..", "..", "..",
                                        "SandboxDesign", "agent", "out"))
# The sandbox became Airlock on 2026-08-22 (log_060).  The 480 products
# of the runs of record still live under SandboxDesign and repointing
# this line wholesale is the owner's call, so `LANE_OUT` is UNCHANGED and
# Airlock's own `agent/out` is added as a further search directory --
# additive, so no earlier product moves or is re-read from a new place.
AIRLOCK_OUT = os.environ.get(
    "AIRLOCK_OUT",
    os.path.abspath(os.path.join(HERE, "..", "..", "..",
                                 "Airlock", "agent", "out")))
AIRLOCK_DROP = os.environ.get(
    "AIRLOCK_DROP",
    os.path.abspath(os.path.join(HERE, "..", "..", "..",
                                 "Airlock", "agent", "drop")))

from l3_accept import holders as _holders, ops as _ops        # noqa: E402
from l3_exec import RT_RUST, RT_GO                            # noqa: E402
# log_062, 2026-08-22 -- the remaining eight.  The seven statically
# checked ones reuse the SETTLED runtimes of the execution campaign
# (log_032) unmodified: every one of them already emits a binary float as
# BITS (`Double.doubleToRawLongBits`, `bitPattern`, `setFloat64`,
# `BitConverter.GetBytes`, `memcpy`), which is the log_057 hazard closed
# by construction rather than by promise.
from l3_exec import (RT_CPP, RT_SWIFT, RT_DART, RT_CSHARP,    # noqa: E402
                     RT_JAVA, RT_KOTLIN, RT_TS, CHUNK as EXEC_CHUNK)
import l3_cart_values as CV                                   # noqa: E402

CHUNK = 1500                 # rust probes per compiled file
RUBY_STALL_S = 2.0           # recorded change: was 10.0
RUBY_WORKERS = 5             # 6 cores in the runner; one left for the shell
RUBY_L2_SHARDS = 1           # ONE lane script.  Level 2 measured 2,335.7 s
                             # wall on the run of record -- inside the
                             # daemon's one-hour ceiling -- so it does not
                             # need splitting.  Raise this constant to cut
                             # the cells across N lane scripts if the menu
                             # or the sets grow; each worker also writes its
                             # answers to its OWN part file AS THEY ARRIVE,
                             # so a run that is stopped still leaves
                             # everything it measured.

# ------------------------------------------------------------------
# log_061, 2026-08-22 -- python (the interpreted shape) and go (the
# compiled shape).  NOTHING about the design changes: same X sets, same
# canonical form, same probe-index rule, same outcome vocabulary, same
# two levels.  Only two emitters are added, one on each existing
# pattern.
# ------------------------------------------------------------------

GO_CHUNK = 1500              # go probes per compiled file.  Starts at
                             # rust's cap and is MEASURED, not assumed --
                             # see log_061 for the build-time table that
                             # settled it.
PYTHON_STALL_S = 0.5         # MEASURED, not inherited.  The principle is
                             # the owner's recorded one (log_052 section 2): a
                             # stall is an ABORT, an ABORT leaves the
                             # numerator AND the denominator both, so the
                             # budget costs WALL CLOCK AND NO MEASUREMENT.
                             # The number is python's own, because python
                             # stalls where ruby does not: ruby's
                             # `Integer#**` REFUSES an oversized exponent
                             # (it warns "in a**b, b may be too big" and
                             # answers Infinity), while python's just
                             # tries.  Measured at level 2, sampled:
                             #
                             #   `**` int      x int       59.3% ABORT
                             #   `**` c_int64  x c_int64   59.6% ABORT
                             #   `**` Fraction x Fraction  75.7% ABORT
                             #   `**` Fraction x int       75.1% ABORT
                             #   `**` Decimal  x Decimal    0.0% (10,000
                             #   `**` int      x Decimal    0.0%  probes)
                             #
                             # ~74,300 of python's 12,852,225 level-2
                             # probes (0.58%) stall.  At ruby's 2.0 s they
                             # would cost 29,720 s of wall clock -- 90% of
                             # the run -- for cells that are excluded from
                             # every score anyway.  CONTROL, so the budget
                             # is not merely assumed safe: `Decimal **
                             # Decimal` ran all 10,000 of its level-2
                             # probes at a 0.10 s budget with ZERO aborts,
                             # so a budget five times shorter than this one
                             # already produces no false stop.
PYTHON_WORKERS = 5           # 6 cores in the runner; one left for the shell
PYTHON_L2_SHARDS = 8         # RE-DERIVED 2026-08-23 (log_061 addendum) now
                             # that python L1 has an actual measured wall
                             # clock: 360,000 probes in 171.5 s = 2,100
                             # probes/s -- SLOWER than the ruby-derived
                             # `MEASURED_RATE["interpreted"]` (4,003/s) this
                             # constant used to be sized against, because
                             # L1's own worker log shows stall recovery is
                             # already a real share of that wall clock
                             # (740 s of 855.5 s worker-time, 1,480 restarts
                             # at the 0.5 s budget).  Unsharded projection,
                             # rate PLUS the measured L2 stall bill divided
                             # across PYTHON_WORKERS:
                             #   12,852,225/2,100 + 74,300*0.5/5 = 13,550 s
                             #   = 225.8 min = 3.76 h
                             # Four shards would be ~56.5 min each -- past
                             # the ~30 min target this run set for restart
                             # granularity.  Eight puts each shard at
                             # 13,550/8 = 1,694 s = ~28.2 min.
# the measured stall bill, carried so the projection is honest rather
# than a bare throughput number.  (aborting probes, seconds each)
PYTHON_L2_STALL_PROBES = 74300

EXTRA_RUBY_OPS = ["and", "or"]


def ops(lang):
    """the operator menu, per language.  Taken from the GRAMMAR's own
    positioned anonymous tokens (`l3_accept.ops`), intersected with the
    candidate binary vocabulary -- nothing is added that a grammar does
    not declare, with the one recorded exception below.

      rust    19    ruby  22 + `and`/`or` = 24
      python  25    go    19

    `and`/`or` are added to RUBY ONLY, and only because the design's own
    sanity check needs them (`&&` against `and` is the positive control).
    python's grammar declares `and`/`or` itself, so they arrive through
    `_ops` with no extension; go declares neither."""
    base = list(_ops(lang))
    if lang == "ruby":
        base = base + EXTRA_RUBY_OPS
    return base


def b64gz(text):
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as g:
        g.write(text.encode("utf-8"))
    return base64.b64encode(buf.getvalue()).decode("ascii")


def wrap(s, width=76):
    return "\n".join(s[i:i + width] for i in range(0, len(s), width))


# ------------------------------------------------------------------
# the holder table, per language and per level
# ------------------------------------------------------------------

def table(lang, level):
    """[{i, form, holder, set_id, kept spellings, absent spellings,
         decls for x0/x2 (`a`,`c`) and x1/x3 (`b`,`d`)}]"""
    hs, _ = _holders(lang)
    out = []
    for i, h in enumerate(hs):
        key = (lang, h.get("form"), h.get("rep"))
        if key not in CV.HOLDERS:
            continue
        holder = CV.HOLDERS[key]
        keep, absent = CV.points(lang, h["form"], holder, level)
        out.append(dict(
            i=i, form=h["form"], holder=holder, rep=h["rep"],
            set_id=CV.set_id(lang, h["form"], holder, level),
            spellings=[s for s, _ in keep], absent=absent,
            n=len(keep),
            a=[CV.decl(lang, h["form"], holder, "a", v) for _, v in keep],
            b=[CV.decl(lang, h["form"], holder, "b", v) for _, v in keep],
            c=[CV.decl(lang, h["form"], holder, "c", v) for _, v in keep],
            d=[CV.decl(lang, h["form"], holder, "d", v) for _, v in keep],
            pre=(h.get("pre") or "")))
    return out


def accepted_rust():
    """{(op, lhs rep, rhs rep): verdict} from the acceptance run."""
    acc = json.load(open(os.path.join(HERE, "acceptance_rust_A2.json")))
    v = {}
    for cell in acc["cells"].values():
        v[(cell["operation"], cell["lhs"]["holder"],
           cell["rhs"]["holder"])] = cell["verdict"]
    return v


def rust_cells_l1():
    """the ACCEPTED (op, lhs index, rhs index) cells over our holders."""
    verdict = accepted_rust()
    tab = {t["rep"]: t for t in table("rust", 1)}
    cells = []
    for (op, lh, rh), vd in verdict.items():
        if vd != "ACCEPT" or lh not in tab or rh not in tab:
            continue
        cells.append((op, tab[lh]["i"], tab[rh]["i"]))
    return sorted(set(cells))


RUST_TYPE_REP = {"bool": "bool", "i32": "i32", "i64": "i64", "u64": "u64",
                 "i128": "i128", "f64": "f64", "f32": "f32"}


def rust_l1_output_types():
    """(op index, lhs index, rhs index) -> rust type_name of the answer,
    read out of the level-1 lane output.  No new measurement, no guess."""
    p = None
    for d in (LANE_OUT, RAW):
        q = os.path.join(d, "ct_rust_l1.txt")
        if os.path.exists(q):
            p = q
            break
    if p is None:
        raise SystemExit("level-1 rust lane output not found; run "
                         "lanes/ct_rust_l1.sh first")
    ty = {}
    for line in open(p):
        line = line.rstrip("\n")
        if line.startswith("__") or not line:
            continue
        pid, _, rest = line.partition("|")
        tn = rest.partition("|")[0]
        if tn == "-":
            continue
        k, i, j, _s = pid[1:].split("_")
        ty.setdefault((int(k), int(i), int(j)), tn)
    return ty


def rust_cells_l2():
    """(cells, why-skipped counter).  Composition must typecheck."""
    op_list = ops("rust")
    verdict = accepted_rust()
    ty = rust_l1_output_types()
    cells, skipped = [], collections.Counter()
    for (op, i, j) in rust_cells_l1():
        k = op_list.index(op)
        tn = ty.get((k, i, j))
        if tn is None:
            skipped["no answered probe at level 1"] += 1
            continue
        rep = RUST_TYPE_REP.get(tn)
        if rep is None:
            skipped["output type is not a holder in the table (%s)"
                    % tn.split("<")[0]] += 1
            continue
        if verdict.get((op, rep, rep)) != "ACCEPT":
            skipped["`%s %s %s` is not an ACCEPT cell" % (rep, op, rep)] += 1
            continue
        cells.append((op, i, j))
    return cells, skipped


# ==================================================================
# go -- the SAME static discipline as rust, on go's own acceptance run
# ==================================================================
# go is statically typed AND refuses every implicit conversion, so most
# cross-holder pairs do not compile at all.  That pruning is REAL DATA,
# not a shortcut: it is the acceptance grain of `acceptance_go_A2.json`,
# measured in the census, and it is the reason go's profile count is
# small next to a dynamically dispatched language's.

def accepted_go():
    """{(op, lhs rep, rhs rep): verdict} from go's acceptance run."""
    acc = json.load(open(os.path.join(HERE, "acceptance_go_A2.json")))
    v = {}
    for cell in acc["cells"].values():
        v[(cell["operation"], cell["lhs"]["holder"],
           cell["rhs"]["holder"])] = cell["verdict"]
    return v


def go_cells_l1():
    """the ACCEPTED (op, lhs index, rhs index) cells over our holders."""
    verdict = accepted_go()
    tab = {t["rep"]: t for t in table("go", 1)}
    cells = []
    for (op, lh, rh), vd in verdict.items():
        if vd != "ACCEPT" or lh not in tab or rh not in tab:
            continue
        cells.append((op, tab[lh]["i"], tab[rh]["i"]))
    return sorted(set(cells))


# `reflect.TypeOf(v).String()` -> the holder rep in our table.  go's
# reflect names ARE the type names, so this map is an identity over the
# holders that take part and a filter over everything else.
GO_TYPE_REP = {"bool": "bool", "int32": "int32", "int64": "int64",
               "uint64": "uint64", "int": "int",
               "float64": "float64", "float32": "float32"}


def go_l1_output_types():
    """(op index, lhs index, rhs index) -> go type name of the answer,
    read out of the level-1 lane output.  No new measurement, no guess --
    exactly the discipline `rust_l1_output_types` applies."""
    p = None
    for d in (LANE_OUT, RAW, AIRLOCK_OUT):
        q = os.path.join(d, "ct_go_l1.txt")
        if os.path.exists(q):
            p = q
            break
    if p is None:
        raise SystemExit("level-1 go lane output not found; run "
                         "lanes/ct_go_l1.sh first")
    ty = {}
    for line in open(p):
        line = line.rstrip("\n")
        if line.startswith("__") or not line:
            continue
        pid, _, rest = line.partition("|")
        tn = rest.partition("|")[0]
        if tn == "-":
            continue
        k, i, j, _s = pid[1:].split("_")
        ty.setdefault((int(k), int(i), int(j)), tn)
    return ty


def go_cells_l2():
    """(cells, why-skipped counter).  `op(y, y)` has to typecheck, so the
    level-1 answer's own type has to be an ACCEPT cell against itself."""
    op_list = ops("go")
    verdict = accepted_go()
    ty = go_l1_output_types()
    cells, skipped = [], collections.Counter()
    for (op, i, j) in go_cells_l1():
        k = op_list.index(op)
        tn = ty.get((k, i, j))
        if tn is None:
            skipped["no answered probe at level 1"] += 1
            continue
        rep = GO_TYPE_REP.get(tn)
        if rep is None:
            skipped["output type is not a holder in the table (%s)"
                    % tn.split("[")[0]] += 1
            continue
        if verdict.get((op, rep, rep)) != "ACCEPT":
            skipped["`%s %s %s` is not an ACCEPT cell" % (rep, op, rep)] += 1
            continue
        cells.append((op, i, j))
    return cells, skipped


# ==================================================================
# rust lane
# ==================================================================

RUST_SH = r'''#!/bin/sh
# layer-3 CARTESIAN lane -- __LABEL__ -- level __LVL__ -- generated by
# Research/kind_fuzz_clustering/l3_cart_gen.py .  Do not hand-edit.
# Static path: the ACCEPTED holder pairs only.  A value the holder
# cannot represent is ABSENT from the row, never coerced.
set -u
export HOME=/work
ROOT=/work/__NAME__
rm -rf "$ROOT"; mkdir -p "$ROOT"
echo "=== layer-3 CARTESIAN -- __LABEL__ -- level __LVL__ -- __NP__ probes ==="
date -u +%Y-%m-%dT%H:%M:%SZ
df -Pm /work | awk 'NR==2{print "free /work: " $4 " MB"}'
base64 -d <<'T_EOF' | gunzip > "$ROOT/table.json"
__TABLE__
T_EOF
base64 -d <<'X_EOF' | gunzip > "$ROOT/rt.txt"
__RT__
X_EOF
python3 - "$ROOT" <<'PY_EOF'
__DRIVER__
PY_EOF
rm -rf "$ROOT"
echo "swept $ROOT; /work free: $(df -Pm /work | awk 'NR==2{print $4}') MB"
date -u +%Y-%m-%dT%H:%M:%SZ
echo "=== cartesian __LABEL__ level __LVL__ done ==="
'''

RUST_DRIVER = r'''
import json, os, shutil, subprocess, sys, time

ROOT = sys.argv[1]
T = json.load(open(os.path.join(ROOT, "table.json")))
OUT = T["out"]
CH = T["chunk"]
LVL = T["level"]
LANG = T.get("language", "rust")     # "rust" (debug) or "rust_release"
RUSTC_FLAGS = T.get("rustc_flags", ["-C", "debug-assertions=on",
                                    "-C", "opt-level=0"])
TAG = "A" if LVL == 1 else "B"

RTX = open(os.path.join(ROOT, "rt.txt")).read()
HOLD = {h["i"]: h for h in T["holders"]}
OPS = T["ops"]

ALLOW = ("#![allow(unused, non_snake_case, non_camel_case_types, "
         "unused_parens, unused_mut, unused_variables, dead_code, "
         "unconditional_panic, arithmetic_overflow)]\n")

# ---- the probe list.  A probe is (id, fn name, [body lines]).
probes = []
for (op, i, j) in T["cells"]:
    k = OPS.index(op)
    ha, hb = HOLD[i], HOLD[j]
    na, nb = ha["n"], hb["n"]
    if LVL == 1:
        for i0 in range(na):
            for i1 in range(nb):
                p = i0 * nb + i1
                probes.append(("A%d_%d_%d_%d" % (k, i, j, p),
                               "a_%d_%d_%d_%d" % (k, i, j, p),
                               [ha["a"][i0], hb["b"][i1],
                                "let _r = (a) %s (b);" % op]))
    else:
        for i0 in range(na):
            for i1 in range(nb):
                for i2 in range(na):
                    for i3 in range(nb):
                        p = ((i0 * nb + i1) * na + i2) * nb + i3
                        probes.append((
                            "B%d_%d_%d_%d" % (k, i, j, p),
                            "b_%d_%d_%d_%d" % (k, i, j, p),
                            [ha["a"][i0], hb["b"][i1],
                             ha["c"][i2], hb["d"][i3],
                             "let _r = ((a) %s (b)) %s ((c) %s (d));"
                             % (op, op, op)]))

print("cartesian %s level %d: %d cells -> %d probes"
      % (LANG, LVL, len(T["cells"]), len(probes)))
sys.stdout.flush()

COMPILES = {"n": 0, "s": 0.0}


def build_src(ps):
    src = ALLOW + RTX + "\n"
    for p in ps:
        src += "// __PROBE__ %s\nfn %s() {\n" % (p[0], p[1])
        for ln in p[2]:
            src += "    %s\n" % ln
        src += '    _emit("%s", &_r);\n}\n' % p[0]
    src += "// __PROBE__ -\n"
    src += "\nfn main() {\n    std::panic::set_hook(Box::new(|_| {}));\n"
    src += "    let ps: Vec<(&str, fn())> = vec![\n"
    for p in ps:
        src += '        ("%s", %s),\n' % (p[0], p[1])
    src += "    ];\n"
    src += "    let av: Vec<String> = std::env::args().collect();\n"
    src += ("    let s: usize = if av.len() > 1 "
            "{ av[1].parse().unwrap_or(0) } else { 0 };\n")
    src += "    for i in s..ps.len() {\n        let (id, f) = ps[i];\n"
    src += ("        if std::panic::catch_unwind(f).is_err() "
            '{ println!("{}|-|RAISE:panic", id); }\n    }\n')
    src += '    println!("__END__");\n}\n'
    return src


def compile_chunk(d, ps):
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    open(os.path.join(d, "chunk.rs"), "w").write(build_src(ps))
    t = time.time()
    r = subprocess.run(["rustc"] + RUSTC_FLAGS +
                       ["-o", d + "/bin", d + "/chunk.rs"],
                       capture_output=True, text=True, cwd=d, timeout=3000)
    el = time.time() - t
    COMPILES["n"] += 1
    COMPILES["s"] += el
    return (r.returncode == 0), el, ((r.stderr or "") + (r.stdout or ""))


def run_binary(d, ps, out):
    ids = [p[0] for p in ps]
    pos = dict((p, k) for k, p in enumerate(ids))
    got = {}
    start = 0
    restarts = 0
    t = time.time()
    while start < len(ids) and restarts < 500:
        pr = subprocess.Popen([d + "/bin", str(start)],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True,
                              cwd=d, bufsize=1)
        last = start - 1
        ended = False
        for line in pr.stdout:
            line = line.rstrip("\n")
            if line == "__END__":
                ended = True
                continue
            if "|" not in line:
                continue
            pid = line.split("|", 1)[0]
            k = pos.get(pid)
            if k is None:
                continue
            got[pid] = line
            if k > last:
                last = k
        pr.wait()
        if ended or last >= len(ids) - 1:
            break
        nxt = last + 1
        got[ids[nxt]] = "%s|-|ABORT:rc%s" % (ids[nxt], pr.returncode)
        start = nxt + 1
        restarts += 1
    el = time.time() - t
    a = r_ = ab = 0
    for pid in ids:
        line = got.get(pid, "%s|-|MISSING" % pid)
        out.write(line + "\n")
        if "|-|RAISE:" in line:
            r_ += 1
        elif "|-|ABORT:" in line:
            ab += 1
        elif "|-|MISSING" in line:
            pass
        else:
            a += 1
    out.flush()
    return a, r_, ab, restarts, el


def handle(d, ps, out, depth=0):
    """compile; on failure BISECT rather than condemning the chunk."""
    ok, tb, err = compile_chunk(d, ps)
    if ok:
        a, r_, ab, rs, tr = run_binary(d, ps, out)
        shutil.rmtree(d, ignore_errors=True)
        return a, r_, ab, 0, rs, tb, tr
    if len(ps) == 1:
        out.write("%s|-|BUILDFAIL\n" % ps[0][0])
        out.flush()
        open(OUT + ".compilefail." + ps[0][0] + ".txt", "w").write(err[:60000])
        shutil.rmtree(d, ignore_errors=True)
        print("   !! BUILDFAIL on a single probe: %s" % ps[0][0])
        sys.stdout.flush()
        return 0, 0, 0, 1, 0, tb, 0.0
    print("   !! chunk of %d failed to build; bisecting (depth %d)"
          % (len(ps), depth))
    sys.stdout.flush()
    shutil.rmtree(d, ignore_errors=True)
    h = len(ps) // 2
    acc = [0, 0, 0, 0, 0, tb, 0.0]
    for half, sub in enumerate((ps[:h], ps[h:])):
        got = handle(d + "_%d%d" % (depth, half), sub, out, depth + 1)
        for x in range(7):
            acc[x] += got[x]
    return tuple(acc)


chunks = [probes[x:x + CH] for x in range(0, len(probes), CH)]
print("chunking: %d probes -> %d chunk files, at most %d probes per file"
      % (len(probes), len(chunks), CH))
sys.stdout.flush()

out = open(OUT, "w")
t0 = time.time()
answers = raises = aborts = buildfail = restarts = 0
build_s = run_s = 0.0
for ci, ps in enumerate(chunks):
    d = os.path.join(ROOT, "c%05d" % ci)
    a, r_, ab, bf, rs, tb, tr = handle(d, ps, out)
    answers += a; raises += r_; aborts += ab
    buildfail += bf; restarts += rs
    build_s += tb; run_s += tr
    if ci % 25 == 0 or ci == len(chunks) - 1:
        print("[progress] rust L%d chunk %d/%d  build %.2fs  run %.2fs  "
              "elapsed %.1fs" % (LVL, ci + 1, len(chunks), tb, tr,
                                 time.time() - t0))
        sys.stdout.flush()

el = time.time() - t0
out.write("__SUMMARY__|%s|%d|%d|%d|%d|%d|%.3f\n"
          % (LANG, len(probes), answers, raises, aborts, buildfail, el))
out.write("__TIMING__|%s|level=%d|chunk_files=%d|probes=%d|chunk_cap=%d|"
          "compile_invocations=%d|compile_s=%.3f|execute_s=%.3f|"
          "other_s=%.3f|total_s=%.3f|restarts=%d|stall_s=0.000\n"
          % (LANG, LVL, len(chunks), len(probes), CH, COMPILES["n"],
             COMPILES["s"], run_s, el - COMPILES["s"] - run_s, el, restarts))
out.close()
print("== cartesian %s L%d: %d probes, %d answers, %d raises, %d aborts, "
      "%d buildfail, %.2f s" % (LANG, LVL, len(probes), answers, raises,
                                aborts, buildfail, el))
print("== TIMING %s L%d: %d chunk FILES (cap %d probes each), %d compile "
      "invocations totalling %.2f s; execution %.2f s; driver overhead "
      "%.2f s; wall %.2f s"
      % (LANG, LVL, len(chunks), CH, COMPILES["n"], COMPILES["s"], run_s,
         el - COMPILES["s"] - run_s, el))
'''


# Job B (log_057, 2026-08-22): rust's overflow behaviour is
# build-mode dependent -- debug PANICS (the only mode this line has
# ever measured), release WRAPS.  the owner's ruling: record BOTH modes as
# DISTINCT language columns that never silently merge, rather than
# replace one with the other.  `-O` alone is rustc's shorthand for
# `-C opt-level=2`; with no `-C debug-assertions=on` / `-C
# overflow-checks=on` it leaves both off, which is exactly the
# wrapping-add guarantee release mode is chosen to exercise.
RUST_DEBUG_FLAGS = ["-C", "debug-assertions=on", "-C", "opt-level=0"]
RUST_RELEASE_FLAGS = ["-O"]


def emit_rust(level, smoke=False, release=False):
    tab = table("rust", level)
    if level == 1:
        cells = rust_cells_l1()
        skipped = collections.Counter()
    else:
        cells, skipped = rust_cells_l2()
    if smoke:
        cells = cells[:3]
    name = "ct_rust_release_l%d" % level if release else "ct_rust_l%d" % level
    if smoke:
        name += "_smoke"
    hold = {t["i"]: t for t in tab}
    nprobe = 0
    for (op, i, j) in cells:
        na, nb = hold[i]["n"], hold[j]["n"]
        nprobe += na * nb if level == 1 else (na * nb) ** 2
    language = "rust_release" if release else "rust"
    payload = dict(language=language, ops=ops("rust"), holders=tab,
                   cells=cells, level=level, chunk=CHUNK,
                   rustc_flags=(RUST_RELEASE_FLAGS if release
                                else RUST_DEBUG_FLAGS),
                   out="/out/%s.txt" % name)
    sh = (RUST_SH
          .replace("__TABLE__", wrap(b64gz(json.dumps(payload))))
          .replace("__RT__", wrap(b64gz(RT_RUST)))
          .replace("__DRIVER__", RUST_DRIVER)
          .replace("__NAME__", name)
          .replace("__LVL__", str(level))
          .replace("__LABEL__", "rust-release" if release else "rust")
          .replace("__NP__", str(nprobe)))
    return name + ".sh", sh, len(cells), nprobe, skipped


# ==================================================================
# go lane -- the COMPILED shape (log_061, 2026-08-22)
# ==================================================================
# Built on `emit_rust`'s pattern, point for point:
#
#   - probes are CHUNKED per build, `GO_CHUNK` per file, so one compiler
#     invocation covers many probes;
#   - the compiled binary takes a START INDEX, and the driver restarts it
#     past any probe that stopped the process, recording that probe
#     ABORT.  An uncatchable stop therefore costs ONE probe, never a
#     chunk;
#   - a chunk that fails to BUILD is BISECTED down to the single probe
#     the compiler refused, which is recorded REFUSE, rather than
#     condemning 1,500 probes to BUILDFAIL;
#   - a catchable panic (integer divide by zero, negative shift count) is
#     taken by `recover()` in RT_GO's `_guard` and recorded RAISE:<kind>.
#
# GO's OWN BUILD REQUIREMENTS, each one a fault if forgotten:
#   * no network.  `GOTOOLCHAIN=local` stops go fetching a newer
#     toolchain for a `go` directive it does not have, and `GOPROXY=off`
#     stops any module fetch.  The sandbox has no route out, so either
#     omission turns into a build failure rather than a download.
#   * `GOCACHE` and `GOPATH` must be writable and are put under the
#     lane's own /work root.
#   * a `go.mod` is written per chunk directory so the build is a module
#     build and never falls back on GOPATH heuristics.
#   * an unused import is a COMPILE ERROR in go.  Every import in the
#     header is used by RT_GO itself (`bufio`, `fmt`, `math`, `os`,
#     `reflect`, `sort`, `strconv`, `strings`), so the header is
#     constant and needs no per-chunk pruning.
#
# THE FLOAT PATH IS BITS, NOT TEXT.  RT_GO's `_enc` emits
# `FLOAT:64:<hex of math.Float64bits>` and `FLOAT:32:<hex of
# math.Float32bits>`.  No printed decimal is ever produced, so the
# log_057 fault -- reading a shortest-round-tripping decimal AS an exact
# decimal -- has no path into go's canon at all.

GO_SH = r'''#!/bin/sh
# layer-3 CARTESIAN lane -- go -- level __LVL__ -- generated by
# Research/kind_fuzz_clustering/l3_cart_gen.py .  Do not hand-edit.
# Static path: the ACCEPTED holder pairs only, from the census's own
# acceptance_go_A2.json.  A value the holder cannot represent is ABSENT
# from the row, never coerced -- in go an out-of-range constant is a
# compile error, so absence is the only honest reading.
set -u
export HOME=/work
ROOT=/work/__NAME__
rm -rf "$ROOT"; mkdir -p "$ROOT"
export GOTOOLCHAIN=local
export GOPROXY=off
export GOFLAGS=-mod=mod
export GOCACHE="$ROOT/gocache"
export GOPATH="$ROOT/gopath"
mkdir -p "$GOCACHE" "$GOPATH"
echo "=== layer-3 CARTESIAN -- go -- level __LVL__ -- __NP__ probes ==="
date -u +%Y-%m-%dT%H:%M:%SZ
go version
df -Pm /work | awk 'NR==2{print "free /work: " $4 " MB"}'
base64 -d <<'T_EOF' | gunzip > "$ROOT/table.json"
__TABLE__
T_EOF
base64 -d <<'X_EOF' | gunzip > "$ROOT/rt.txt"
__RT__
X_EOF
python3 - "$ROOT" <<'PY_EOF'
__DRIVER__
PY_EOF
rm -rf "$ROOT"
echo "swept $ROOT; /work free: $(df -Pm /work | awk 'NR==2{print $4}') MB"
date -u +%Y-%m-%dT%H:%M:%SZ
echo "=== cartesian go level __LVL__ done ==="
'''

GO_DRIVER = r'''
import json, os, shutil, subprocess, sys, time

ROOT = sys.argv[1]
T = json.load(open(os.path.join(ROOT, "table.json")))
OUT = T["out"]
CH = T["chunk"]
LVL = T["level"]
LANG = T.get("language", "go")
TAG = "A" if LVL == 1 else "B"

RTX = open(os.path.join(ROOT, "rt.txt")).read()
HOLD = {h["i"]: h for h in T["holders"]}
OPS = T["ops"]

# every one of these is used by the runtime in rt.txt; go REFUSES an
# unused import, so the header is fixed rather than derived per chunk.
HEAD = ("package main\n\nimport (\n\t\"bufio\"\n\t\"fmt\"\n\t\"math\"\n"
        "\t\"os\"\n\t\"reflect\"\n\t\"sort\"\n\t\"strconv\"\n"
        "\t\"strings\"\n)\n\n")

GOMOD = "module chunk\n\ngo 1.26\n"

# ---- the probe list.  A probe is (id, fn name, [body lines]).
probes = []
for (op, i, j) in T["cells"]:
    k = OPS.index(op)
    ha, hb = HOLD[i], HOLD[j]
    na, nb = ha["n"], hb["n"]
    if LVL == 1:
        for i0 in range(na):
            for i1 in range(nb):
                p = i0 * nb + i1
                probes.append(("A%d_%d_%d_%d" % (k, i, j, p),
                               "a_%d_%d_%d_%d" % (k, i, j, p),
                               [ha["a"][i0], hb["b"][i1],
                                "_r := ((a) %s (b));" % op]))
    else:
        for i0 in range(na):
            for i1 in range(nb):
                for i2 in range(na):
                    for i3 in range(nb):
                        p = ((i0 * nb + i1) * na + i2) * nb + i3
                        probes.append((
                            "B%d_%d_%d_%d" % (k, i, j, p),
                            "b_%d_%d_%d_%d" % (k, i, j, p),
                            [ha["a"][i0], hb["b"][i1],
                             ha["c"][i2], hb["d"][i3],
                             "_r := (((a) %s (b)) %s ((c) %s (d)));"
                             % (op, op, op)]))

print("cartesian %s level %d: %d cells -> %d probes"
      % (LANG, LVL, len(T["cells"]), len(probes)))
sys.stdout.flush()

COMPILES = {"n": 0, "s": 0.0}


def build_src(ps):
    src = HEAD + RTX + "\n"
    for p in ps:
        src += "// __PROBE__ %s\nfunc %s() {\n" % (p[0], p[1])
        src += '\tdefer _guard("%s")\n' % p[0]
        for ln in p[2]:
            src += "\t%s\n" % ln
        src += '\t_emit("%s", _r)\n}\n' % p[0]
    src += "// __PROBE__ -\n"
    src += "\nfunc main() {\n"
    src += "\tps := []struct {\n\t\tid string\n\t\tf  func()\n\t}{\n"
    for p in ps:
        src += '\t\t{"%s", %s},\n' % (p[0], p[1])
    src += "\t}\n"
    src += "\ts := 0\n"
    src += "\tif len(os.Args) > 1 {\n"
    src += "\t\tif n, err := strconv.Atoi(os.Args[1]); err == nil {\n"
    src += "\t\t\ts = n\n\t\t}\n\t}\n"
    src += "\tfor i := s; i < len(ps); i++ {\n\t\tps[i].f()\n\t}\n"
    src += '\tfmt.Fprintln(_W, "__END__")\n\t_W.Flush()\n}\n'
    return src


def compile_chunk(d, ps):
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    open(os.path.join(d, "go.mod"), "w").write(GOMOD)
    open(os.path.join(d, "chunk.go"), "w").write(build_src(ps))
    t = time.time()
    r = subprocess.run(["go", "build", "-o", os.path.join(d, "bin"),
                        "chunk.go"],
                       capture_output=True, text=True, cwd=d, timeout=3000)
    el = time.time() - t
    COMPILES["n"] += 1
    COMPILES["s"] += el
    return (r.returncode == 0), el, ((r.stderr or "") + (r.stdout or ""))


def run_binary(d, ps, out):
    """the START-INDEX discipline, identical to rust's: an uncatchable
    stop costs ONE probe, never the chunk."""
    ids = [p[0] for p in ps]
    pos = dict((p, k) for k, p in enumerate(ids))
    got = {}
    start = 0
    restarts = 0
    t = time.time()
    while start < len(ids) and restarts < 500:
        pr = subprocess.Popen([os.path.join(d, "bin"), str(start)],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True,
                              cwd=d, bufsize=1)
        last = start - 1
        ended = False
        for line in pr.stdout:
            line = line.rstrip("\n")
            if line == "__END__":
                ended = True
                continue
            if "|" not in line:
                continue
            pid = line.split("|", 1)[0]
            k = pos.get(pid)
            if k is None:
                continue
            got[pid] = line
            if k > last:
                last = k
        pr.wait()
        if ended or last >= len(ids) - 1:
            break
        nxt = last + 1
        got[ids[nxt]] = "%s|-|ABORT:rc%s" % (ids[nxt], pr.returncode)
        start = nxt + 1
        restarts += 1
    el = time.time() - t
    a = r_ = ab = 0
    for pid in ids:
        line = got.get(pid, "%s|-|MISSING" % pid)
        out.write(line + "\n")
        if "|-|RAISE:" in line:
            r_ += 1
        elif "|-|ABORT:" in line:
            ab += 1
        elif "|-|MISSING" in line:
            pass
        else:
            a += 1
    out.flush()
    return a, r_, ab, restarts, el


def handle(d, ps, out, depth=0):
    """compile; on failure BISECT rather than condemning the chunk."""
    ok, tb, err = compile_chunk(d, ps)
    if ok:
        a, r_, ab, rs, tr = run_binary(d, ps, out)
        shutil.rmtree(d, ignore_errors=True)
        return a, r_, ab, 0, rs, tb, tr
    if len(ps) == 1:
        out.write("%s|-|BUILDFAIL\n" % ps[0][0])
        out.flush()
        open(OUT + ".compilefail." + ps[0][0] + ".txt", "w").write(err[:60000])
        shutil.rmtree(d, ignore_errors=True)
        print("   !! BUILDFAIL on a single probe: %s" % ps[0][0])
        sys.stdout.flush()
        return 0, 0, 0, 1, 0, tb, 0.0
    print("   !! chunk of %d failed to build; bisecting (depth %d)"
          % (len(ps), depth))
    sys.stdout.flush()
    shutil.rmtree(d, ignore_errors=True)
    h = len(ps) // 2
    acc = [0, 0, 0, 0, 0, tb, 0.0]
    for half, sub in enumerate((ps[:h], ps[h:])):
        got = handle(d + "_%d%d" % (depth, half), sub, out, depth + 1)
        for x in range(7):
            acc[x] += got[x]
    return tuple(acc)


chunks = [probes[x:x + CH] for x in range(0, len(probes), CH)]
print("chunking: %d probes -> %d chunk files, at most %d probes per file"
      % (len(probes), len(chunks), CH))
sys.stdout.flush()

out = open(OUT, "w")
t0 = time.time()
answers = raises = aborts = buildfail = restarts = 0
build_s = run_s = 0.0
for ci, ps in enumerate(chunks):
    d = os.path.join(ROOT, "c%05d" % ci)
    a, r_, ab, bf, rs, tb, tr = handle(d, ps, out)
    answers += a; raises += r_; aborts += ab
    buildfail += bf; restarts += rs
    build_s += tb; run_s += tr
    if ci % 25 == 0 or ci == len(chunks) - 1:
        print("[progress] go L%d chunk [%d/%d]  build %.2fs  run %.2fs  "
              "elapsed %.1fs" % (LVL, ci + 1, len(chunks), tb, tr,
                                 time.time() - t0))
        sys.stdout.flush()

el = time.time() - t0
out.write("__SUMMARY__|%s|%d|%d|%d|%d|%d|%.3f\n"
          % (LANG, len(probes), answers, raises, aborts, buildfail, el))
out.write("__TIMING__|%s|level=%d|chunk_files=%d|probes=%d|chunk_cap=%d|"
          "compile_invocations=%d|compile_s=%.3f|execute_s=%.3f|"
          "other_s=%.3f|total_s=%.3f|restarts=%d|stall_s=0.000\n"
          % (LANG, LVL, len(chunks), len(probes), CH, COMPILES["n"],
             COMPILES["s"], run_s, el - COMPILES["s"] - run_s, el, restarts))
out.close()
print("== cartesian %s L%d: %d probes, %d answers, %d raises, %d aborts, "
      "%d buildfail, %.2f s" % (LANG, LVL, len(probes), answers, raises,
                                aborts, buildfail, el))
print("== TIMING %s L%d: %d chunk FILES (cap %d probes each), %d compile "
      "invocations totalling %.2f s; execution %.2f s; driver overhead "
      "%.2f s; wall %.2f s"
      % (LANG, LVL, len(chunks), CH, COMPILES["n"], COMPILES["s"], run_s,
         el - COMPILES["s"] - run_s, el))
'''


def emit_go(level, smoke=False):
    tab = table("go", level)
    if level == 1:
        cells = go_cells_l1()
        skipped = collections.Counter()
    else:
        cells, skipped = go_cells_l2()
    if smoke:
        cells = cells[:3]
    name = "ct_go_l%d" % level
    if smoke:
        name += "_smoke"
    hold = {t["i"]: t for t in tab}
    nprobe = 0
    for (op, i, j) in cells:
        na, nb = hold[i]["n"], hold[j]["n"]
        nprobe += na * nb if level == 1 else (na * nb) ** 2
    payload = dict(language="go", ops=ops("go"), holders=tab,
                   cells=cells, level=level, chunk=GO_CHUNK,
                   out="/out/%s.txt" % name)
    sh = (GO_SH
          .replace("__TABLE__", wrap(b64gz(json.dumps(payload))))
          .replace("__RT__", wrap(b64gz(RT_GO)))
          .replace("__DRIVER__", GO_DRIVER)
          .replace("__NAME__", name)
          .replace("__LVL__", str(level))
          .replace("__NP__", str(nprobe)))
    return name + ".sh", sh, len(cells), nprobe, skipped


# ==================================================================
# ruby lane
# ==================================================================

RUBY_SH = """#!/bin/sh
# layer-3 CARTESIAN lane -- ruby -- level __LVL__ __SHARDNOTE__ --
# generated by Research/kind_fuzz_clustering/l3_cart_gen.py .
# Do not hand-edit.  Route C: execution is the only acceptance evidence
# ruby has, so every ordered holder pair times the operator menu runs.
set -u
export HOME=/work
ROOT=/work/__NAME__
rm -rf "$ROOT"; mkdir -p "$ROOT"
echo "=== layer-3 CARTESIAN -- ruby -- level __LVL__ -- __NP__ probes ==="
date -u +%Y-%m-%dT%H:%M:%SZ
base64 -d <<'T_EOF' | gunzip > "$ROOT/table.json"
__TABLE__
T_EOF
base64 -d <<'DRV_EOF' > "$ROOT/drv.rb"
__DRIVER__
DRV_EOF
python3 - "$ROOT" <<'PY_EOF'
__RUNNER__
PY_EOF
rm -rf "$ROOT"
date -u +%Y-%m-%dT%H:%M:%SZ
echo "=== cartesian ruby level __LVL__ done ==="
"""

RUBY_DRIVER = r"""ROOT = ARGV[0]
SHARD = (ARGV[1] || "0").to_i
START = (ARGV[2] || "0").to_i
require 'json'
require 'bigdecimal'
$VERBOSE = nil            # ruby's "in a**b, b may be too big" warning
begin
  Process.setrlimit(Process::RLIMIT_AS, 2 * 1024 * 1024 * 1024)
rescue StandardError
end
T = JSON.parse(File.read(File.join(ROOT, "table.json")))
HS = T["holders"]; OPS = T["ops"]; LVL = T["level"]; CELLS = T["cells"]
NW = T["workers"]
TAG = LVL == 1 ? "A" : "B"

BIGBITS = 4096
TOPBITS = 512

def _top(a)
  bl = a.bit_length
  [bl, (bl > TOPBITS ? (a >> (bl - TOPBITS)) : a).to_s(16)]
end

def ser(r)
  case r
  when Integer
    a = r.abs
    if a.bit_length > BIGBITS
      bl, hx = _top(a)
      "BIGNUM:#{r < 0 ? -1 : 1}:#{bl}:#{hx}"
    else
      "Integer:#{r}"
    end
  when Rational
    n = r.numerator; d = r.denominator
    if n.abs.bit_length > BIGBITS || d.bit_length > BIGBITS
      nb, nh = _top(n.abs); db, dh = _top(d)
      "BIGRAT:#{n < 0 ? -1 : 1}:#{nb}:#{nh}:#{db}:#{dh}"
    else
      "Rational:#{n}/#{d}"
    end
  when Float
    "Float:#{r.inspect}"
  when BigDecimal
    s = r.to_s
    s.length > 4000 ? "BIGDEC:#{r.sign}:#{r.exponent}:#{s[0, 200]}" : "BigDecimal:#{s}"
  when String
    "String:#{r.length > 2000 ? r[0, 2000] : r}"
  when NilClass
    "NilClass:nil"
  when TrueClass, FalseClass
    "#{r.class}:#{r}"
  else
    "#{r.class}:#{r.inspect[0, 400]}"
  end
end

HB = {}
HS.each { |h| HB[h["i"]] = h }

# The probe list is NEVER materialised.  Building millions of source
# strings up front cost more than the whole stall budget and more than
# the 2 GB address-space cap, so the enumeration is arithmetic instead:
# a small per-cell plan with prefix sums, and an O(1) decode from a
# global probe index to the four operand indices.  A restart therefore
# resumes in constant time instead of replaying the run so far.
PLAN = []
TOTAL = 0
CELLS.each do |cell|
  op, i, j = cell
  k = OPS.index(op)
  ha = HB[i]; hb = HB[j]
  na = ha["n"]; nb = hb["n"]
  n = LVL == 1 ? na * nb : (na * nb) * (na * nb)
  PLAN << [TOTAL, n, k, i, j, op, ha, hb, na, nb]
  TOTAL += n
end

$stdout.sync = true
puts "__READY__"

def locate(g)
  lo = 0; hi = PLAN.size - 1
  while lo < hi
    mid = (lo + hi + 1) / 2
    if PLAN[mid][0] <= g then lo = mid else hi = mid - 1 end
  end
  PLAN[lo]
end

l = START
loop do
  g = l * NW + SHARD
  break if g >= TOTAL
  base, n, k, i, j, op, ha, hb, na, nb = locate(g)
  p = g - base
  if LVL == 1
    i1 = p % nb; i0 = p / nb
    pid = "A#{k}_#{i}_#{j}_#{p}"
    src = ha["a"][i0] + "\n" + hb["b"][i1] +
          "\n__r = ((a) #{op} (b))\n__r"
  else
    i3 = p % nb; t = p / nb
    i2 = t % na; t2 = t / na
    i1 = t2 % nb; i0 = t2 / nb
    pid = "B#{k}_#{i}_#{j}_#{p}"
    src = ha["a"][i0] + "\n" + hb["b"][i1] + "\n" +
          ha["c"][i2] + "\n" + hb["d"][i3] +
          "\n__r = (((a) #{op} (b)) #{op} ((c) #{op} (d)))\n__r"
  end
  begin
    r = eval(src, TOPLEVEL_BINDING.dup)
    puts "#{pid}|ANSWER|#{ser(r)}"
  rescue SyntaxError
    puts "#{pid}|REFUSE|SyntaxError"
  rescue Exception => e
    puts "#{pid}|RAISE|#{e.class}"
  end
  l += 1
end
puts "__END__"
"""

RUBY_RUNNER = r"""
import json
import os
import queue
import subprocess
import sys
import threading
import time

ROOT = sys.argv[1]
T = json.load(open(os.path.join(ROOT, "table.json")))
OUT = T["out"]
STALL = T["stall_s"]        # RECORDED CHANGE: 2 s, was 10 s.  A stall is
                            # an ABORT and an ABORT is excluded from
                            # scoring, so a shorter budget loses no
                            # measurement -- only wall clock.
STARTUP = 120.0             # a driver's setup grace, separate from the
                            # per-probe stall budget
NW = T["workers"]
LVL = T["level"]
HS, OPS, CELLS = T["holders"], T["ops"], T["cells"]
HB = dict((h["i"], h) for h in HS)

ids = []
for (op, i, j) in CELLS:
    k = OPS.index(op)
    na, nb = HB[i]["n"], HB[j]["n"]
    n = na * nb if LVL == 1 else (na * nb) ** 2
    tag = "A" if LVL == 1 else "B"
    for p in range(n):
        ids.append("%s%d_%d_%d_%d" % (tag, k, i, j, p))

shards = [ids[w::NW] for w in range(NW)]
print("cartesian ruby level %d: %d cells -> %d probes, sharded across %d "
      "worker processes; stall budget %.1f s (was 10.0)"
      % (LVL, len(CELLS), len(ids), NW, STALL))
sys.stdout.flush()


def pump(fh, q):
    for line in fh:
        q.put(line.rstrip("\n"))
    q.put(None)


RES = {}
STATS = {}
LOCK = threading.Lock()


def work(w):
    mine = shards[w]
    pos = dict((p, k) for k, p in enumerate(mine))
    got = {}
    # every worker writes its own PART FILE as the answers arrive.  A run
    # the daemon stops at its ceiling therefore still leaves on disk
    # everything it actually measured, instead of nothing.
    part = open(OUT[:-4] + ".w%d.txt" % w, "w")
    written = 0
    start = 0
    restarts = 0
    stall_s = 0.0
    t0 = time.time()
    while start < len(mine) and restarts < 20000:
        pr = subprocess.Popen(["ruby", os.path.join(ROOT, "drv.rb"), ROOT,
                               str(w), str(start)],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True,
                              bufsize=1)
        q = queue.Queue()
        threading.Thread(target=pump, args=(pr.stdout, q),
                         daemon=True).start()
        last = start - 1
        ended = stalled = False
        ready = False
        while True:
            # STARTUP grace: the driver announces `__READY__` once its
            # per-cell plan is built.  Until then the stall budget does not
            # apply -- a slow start is not a stuck probe, and conflating
            # the two is what made the first attempt at this lane spin.
            try:
                line = q.get(timeout=(STARTUP if not ready else STALL))
            except queue.Empty:
                stalled = True
                stall_s += STALL
                break
            if line is None:
                break
            if line == "__READY__":
                ready = True
                continue
            if line == "__END__":
                ended = True
                continue
            if "|" not in line:
                continue
            pid = line.split("|", 1)[0]
            k = pos.get(pid)
            if k is None:
                continue
            got[pid] = line
            part.write(line + "\n")
            written += 1
            if written % 5000 == 0:
                part.flush()
            if k > last:
                last = k
        if stalled:
            try:
                pr.kill()      # the subprocess API's own name; the OUTCOME
                               # this produces is ABORT
            except OSError:
                pass
        pr.wait()
        if ended or last >= len(mine) - 1:
            break
        nxt = last + 1
        why = ("stalled>%.0fs" % STALL) if stalled else ("rc%s"
                                                         % pr.returncode)
        got[mine[nxt]] = "%s|ABORT|%s" % (mine[nxt], why)
        part.write(got[mine[nxt]] + "\n")
        part.flush()
        start = nxt + 1
        restarts += 1
        if restarts % 25 == 0:
            print("[worker %d] %d restarts, at %d/%d after %.1f s"
                  % (w, restarts, start, len(mine), time.time() - t0))
            sys.stdout.flush()
    part.close()
    with LOCK:
        RES.update(got)
        STATS[w] = dict(restarts=restarts, stall_s=stall_s,
                        wall_s=time.time() - t0, probes=len(mine))
    print("[worker %d] done: %d probes, %d restarts, %.1f s stalled, "
          "%.1f s wall" % (w, len(mine), restarts, stall_s,
                           time.time() - t0))
    sys.stdout.flush()


t0 = time.time()
ths = [threading.Thread(target=work, args=(w,)) for w in range(NW)]
for t in ths:
    t.start()
for t in ths:
    t.join()
el = time.time() - t0

ans = raises = aborts = refused = missing = 0
with open(OUT, "w") as f:
    for pid in ids:
        line = RES.get(pid, "%s|MISSING|" % pid)
        f.write(line + "\n")
        kind = line.split("|")[1]
        if kind == "ANSWER":
            ans += 1
        elif kind == "RAISE":
            raises += 1
        elif kind == "ABORT":
            aborts += 1
        elif kind == "REFUSE":
            refused += 1
        else:
            missing += 1
    restarts = sum(s["restarts"] for s in STATS.values())
    stall_s = sum(s["stall_s"] for s in STATS.values())
    f.write("__SUMMARY__|ruby|%d|%d|%d|%d|%d|%.3f\n"
            % (len(ids), ans, raises, aborts, refused, el))
    f.write("__TIMING__|ruby|level=%d|workers=%d|processes=%d|probes=%d|"
            "compile_invocations=0|compile_s=0.000|stall_budget_s=%.1f|"
            "stall_s=%.3f|execute_s=%.3f|total_s=%.3f|restarts=%d\n"
            % (LVL, NW, restarts + NW, len(ids), STALL, stall_s,
               max(0.0, el - stall_s / max(1, NW)), el, restarts))
print("== cartesian ruby L%d: %d probes, %d answers, %d raises, %d aborts, "
      "%d refusals, %d missing, %d restarts, %.2f s wall"
      % (LVL, len(ids), ans, raises, aborts, refused, missing, restarts, el))
print("== TIMING ruby L%d: 0 files compiled (route C is eval, nothing is "
      "compiled); %d ruby process(es) across %d workers -- %d workers plus "
      "%d restarts past a probe that stopped one; wall %.2f s; %.2f s of "
      "worker-time spent inside the %.1f s inactivity budget on stalls"
      % (LVL, restarts + NW, NW, NW, restarts, el, stall_s, STALL))
for w in sorted(STATS):
    s = STATS[w]
    print("   worker %d: %d probes, %d restarts, %.1f s stalled, %.1f s wall"
          % (w, s["probes"], s["restarts"], s["stall_s"], s["wall_s"]))
"""


def ruby_cells(level):
    tab = table("ruby", level)
    idx = sorted(t["i"] for t in tab)
    return [(op, i, j) for i in idx for j in idx for op in ops("ruby")]


def emit_ruby(level, shard=None, nshard=1, smoke=False):
    tab = table("ruby", level)
    hold = {t["i"]: t for t in tab}
    cells = ruby_cells(level)
    if smoke:
        cells = cells[:4]
    if shard is not None:
        cells = [c for n, c in enumerate(cells) if n % nshard == shard]
    name = "ct_ruby_l%d" % level
    if shard is not None:
        name += "_s%d" % shard
    if smoke:
        name += "_smoke"
    nprobe = 0
    for (op, i, j) in cells:
        na, nb = hold[i]["n"], hold[j]["n"]
        nprobe += na * nb if level == 1 else (na * nb) ** 2
    payload = dict(language="ruby", ops=ops("ruby"), holders=tab,
                   cells=cells, level=level, workers=RUBY_WORKERS,
                   stall_s=RUBY_STALL_S, out="/out/%s.txt" % name)
    sh = (RUBY_SH
          .replace("__TABLE__", wrap(b64gz(json.dumps(payload))))
          .replace("__DRIVER__", wrap(base64.b64encode(
              RUBY_DRIVER.encode("utf-8")).decode("ascii")))
          .replace("__RUNNER__", RUBY_RUNNER)
          .replace("__NAME__", name)
          .replace("__LVL__", str(level))
          .replace("__SHARDNOTE__",
                   "shard %d of %d" % (shard, nshard) if shard is not None
                   else "")
          .replace("__NP__", str(nprobe)))
    return name + ".sh", sh, len(cells), nprobe


# ==================================================================
# python lane -- the INTERPRETED shape (log_061, 2026-08-22)
# ==================================================================
# Built on `emit_ruby`'s pattern, point for point: route C, nothing is
# compiled ahead of time, every ordered holder pair times the operator
# menu runs, the probe list is NEVER materialised (arithmetic
# enumeration from a small per-cell plan with prefix sums and an O(1)
# decode, so a restart resumes in constant time), the driver announces
# `__READY__` so a slow start is not mistaken for a stuck probe, each
# worker writes its own part file as answers arrive, and a probe that
# stops a worker is recorded ABORT and stepped past.
#
# THE STALL BUDGET IS THE RUNNER'S INACTIVITY TIMEOUT, not an in-process
# alarm, and that is deliberate.  The operation that stalls is `**` on
# unbounded integers, which is a SINGLE bytecode: a `signal.setitimer`
# alarm cannot interrupt it, because the interpreter never reaches a
# bytecode boundary to deliver the signal.  Only an outside observer
# with the power to stop the process can bound it -- which is exactly
# what the ruby runner already does.
#
# THE FLOAT PATH IS BITS, NOT TEXT.  `ser` emits a `float` as
# `FLOAT:64:<hex of struct.pack(">d", r)>` -- the same token shape rust
# and go emit from `to_bits()` / `math.Float64bits`, decoded by the same
# `decode_enc` -- so python's binary floats never travel as printed
# decimals and the log_057 fault has no path into python's canon.
# `Decimal` and `Fraction` keep the printed grain, because a decimal
# type's printed text already IS its exact value and a rational's
# `n/d` is exact by construction.

PYTHON_SH = """#!/bin/sh
# layer-3 CARTESIAN lane -- python -- level __LVL__ __SHARDNOTE__ --
# generated by Research/kind_fuzz_clustering/l3_cart_gen.py .
# Do not hand-edit.  Route C: execution is the only acceptance evidence
# python has, so every ordered holder pair times the operator menu runs.
set -u
export HOME=/work
ROOT=/work/__NAME__
rm -rf "$ROOT"; mkdir -p "$ROOT"
echo "=== layer-3 CARTESIAN -- python -- level __LVL__ -- __NP__ probes ==="
date -u +%Y-%m-%dT%H:%M:%SZ
python3 --version
base64 -d <<'T_EOF' | gunzip > "$ROOT/table.json"
__TABLE__
T_EOF
base64 -d <<'DRV_EOF' > "$ROOT/drv.py"
__DRIVER__
DRV_EOF
python3 - "$ROOT" <<'PY_EOF'
__RUNNER__
PY_EOF
rm -rf "$ROOT"
date -u +%Y-%m-%dT%H:%M:%SZ
echo "=== cartesian python level __LVL__ done ==="
"""

PYTHON_DRIVER = r'''import json
import os
import resource
import struct
import sys
from decimal import Decimal
from fractions import Fraction

ROOT = sys.argv[1]
SHARD = int(sys.argv[2] if len(sys.argv) > 2 else "0")
START = int(sys.argv[3] if len(sys.argv) > 3 else "0")

try:
    _CAP = 2 * 1024 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (_CAP, _CAP))
except Exception:
    pass

T = json.load(open(os.path.join(ROOT, "table.json")))
HS = T["holders"]; OPS = T["ops"]; LVL = T["level"]; CELLS = T["cells"]
NW = T["workers"]
TAG = "A" if LVL == 1 else "B"

BIGBITS = 4096
TOPBITS = 512


def _top(a):
    bl = a.bit_length()
    return bl, format((a >> (bl - TOPBITS)) if bl > TOPBITS else a, "x")


def ser(r):
    """the payload grain.  Binary floats travel as BITS -- the same
    `FLOAT:<width>:<hex>` token rust and go emit -- so no printed decimal
    is ever read back as an exact decimal (the log_057 fault).  Decimal
    and Fraction keep the printed grain, where the text IS the value."""
    if r is None:
        return "NULL"
    if r is True:
        return "bool:True"
    if r is False:
        return "bool:False"
    t = type(r)
    if t is int:
        a = -r if r < 0 else r
        if a.bit_length() > BIGBITS:
            bl, hx = _top(a)
            return "BIGNUM:%d:%d:%s" % (-1 if r < 0 else 1, bl, hx)
        return "Integer:%d" % r
    if t is float:
        return "FLOAT:64:" + struct.pack(">d", r).hex()
    if t is Fraction:
        n = r.numerator
        d = r.denominator
        an = -n if n < 0 else n
        if an.bit_length() > BIGBITS or d.bit_length() > BIGBITS:
            nb, nh = _top(an)
            db, dh = _top(d)
            return "BIGRAT:%d:%d:%s:%d:%s" % (-1 if n < 0 else 1,
                                              nb, nh, db, dh)
        return "Rational:%d/%d" % (n, d)
    if t is Decimal:
        s = str(r)
        if len(s) > 4000:
            sg, _dg, ex = r.as_tuple()
            return "BIGDEC:%d:%s:%s" % (-1 if sg else 1, ex, s[:200])
        return "Decimal:%s" % s
    if t is str:
        return "String:%s" % (r if len(r) <= 2000 else r[:2000])
    if t is complex:
        return "opaque:complex"
    try:
        return "%s:%s" % (t.__name__, repr(r)[:400])
    except Exception:
        return "opaque:%s" % t.__name__


HB = {}
for h in HS:
    HB[h["i"]] = h

# The probe list is NEVER materialised -- the ruby lane's defect A
# (log_052 section 10) applies word for word to python: building millions
# of source strings up front costs more than the whole stall budget and
# more than the address-space cap.  The enumeration is arithmetic: a
# small per-cell plan with prefix sums and an O(1) decode from a global
# probe index to the four operand indices, so a restart resumes in
# constant time instead of replaying the run so far.
PLAN = []
TOTAL = 0
for cell in CELLS:
    op, i, j = cell
    k = OPS.index(op)
    ha = HB[i]
    hb = HB[j]
    na = ha["n"]
    nb = hb["n"]
    n = (na * nb) if LVL == 1 else (na * nb) * (na * nb)
    PLAN.append((TOTAL, n, k, i, j, op, ha, hb, na, nb))
    TOTAL += n

# the holder declarations name Decimal, Fraction and ctypes; they are
# bound ONCE here and copied into each probe's namespace, so no probe
# pays an import.
import ctypes                                            # noqa: E402
BASE = {"Decimal": Decimal, "Fraction": Fraction, "ctypes": ctypes}

sys.stdout.reconfigure(line_buffering=True)
print("__READY__")


def locate(g):
    lo = 0
    hi = len(PLAN) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if PLAN[mid][0] <= g:
            lo = mid
        else:
            hi = mid - 1
    return PLAN[lo]


l = START
while True:
    g = l * NW + SHARD
    if g >= TOTAL:
        break
    base, n, k, i, j, op, ha, hb, na, nb = locate(g)
    p = g - base
    if LVL == 1:
        i1 = p % nb
        i0 = p // nb
        pid = "A%d_%d_%d_%d" % (k, i, j, p)
        src = (ha["a"][i0] + "\n" + hb["b"][i1] +
               "\n__r = ((a) %s (b))\n" % op)
    else:
        i3 = p % nb
        t = p // nb
        i2 = t % na
        t2 = t // na
        i1 = t2 % nb
        i0 = t2 // nb
        pid = "B%d_%d_%d_%d" % (k, i, j, p)
        src = (ha["a"][i0] + "\n" + hb["b"][i1] + "\n" +
               ha["c"][i2] + "\n" + hb["d"][i3] +
               "\n__r = (((a) %s (b)) %s ((c) %s (d)))\n" % (op, op, op))
    try:
        code = compile(src, "<probe>", "exec")
    except SyntaxError:
        print("%s|REFUSE|SyntaxError" % pid)
        l += 1
        continue
    ns = dict(BASE)
    try:
        exec(code, ns)
        print("%s|ANSWER|%s" % (pid, ser(ns.get("__r"))))
    except BaseException as e:
        print("%s|RAISE|%s" % (pid, type(e).__name__))
    l += 1
print("__END__")
'''

# The runner is the ruby runner's machinery with python's interpreter and
# driver file.  It is a SEPARATE constant rather than a parameterisation
# of `RUBY_RUNNER`, deliberately: `ct_ruby_l1.sh` / `ct_ruby_l2.sh` are
# the scripts of the run of record (log_052) and their generated bytes
# are left untouchable by anything added here.
PYTHON_RUNNER = r"""
import json
import os
import queue
import subprocess
import sys
import threading
import time

ROOT = sys.argv[1]
T = json.load(open(os.path.join(ROOT, "table.json")))
OUT = T["out"]
STALL = T["stall_s"]        # a stall is an ABORT and an ABORT is excluded
                            # from scoring in the numerator AND the
                            # denominator, so this budget costs wall clock
                            # and no measurement.
STARTUP = 120.0             # a driver's setup grace, separate from the
                            # per-probe stall budget
NW = T["workers"]
LVL = T["level"]
HS, OPS, CELLS = T["holders"], T["ops"], T["cells"]
HB = dict((h["i"], h) for h in HS)

ids = []
for (op, i, j) in CELLS:
    k = OPS.index(op)
    na, nb = HB[i]["n"], HB[j]["n"]
    n = na * nb if LVL == 1 else (na * nb) ** 2
    tag = "A" if LVL == 1 else "B"
    for p in range(n):
        ids.append("%s%d_%d_%d_%d" % (tag, k, i, j, p))

shards = [ids[w::NW] for w in range(NW)]
print("cartesian python level %d: %d cells -> %d probes, sharded across %d "
      "worker processes; stall budget %.1f s"
      % (LVL, len(CELLS), len(ids), NW, STALL))
sys.stdout.flush()


def pump(fh, q):
    for line in fh:
        q.put(line.rstrip("\n"))
    q.put(None)


RES = {}
STATS = {}
LOCK = threading.Lock()


def work(w):
    mine = shards[w]
    pos = dict((p, k) for k, p in enumerate(mine))
    got = {}
    # every worker writes its own PART FILE as the answers arrive, so a
    # run the daemon stops at its ceiling still leaves on disk everything
    # it actually measured instead of nothing.
    part = open(OUT[:-4] + ".w%d.txt" % w, "w")
    written = 0
    start = 0
    restarts = 0
    stall_s = 0.0
    t0 = time.time()
    while start < len(mine) and restarts < 20000:
        pr = subprocess.Popen(["python3", os.path.join(ROOT, "drv.py"), ROOT,
                               str(w), str(start)],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True,
                              bufsize=1)
        q = queue.Queue()
        threading.Thread(target=pump, args=(pr.stdout, q),
                         daemon=True).start()
        last = start - 1
        ended = stalled = False
        ready = False
        while True:
            # STARTUP grace: the driver announces `__READY__` once its
            # per-cell plan is built.  Until then the stall budget does not
            # apply -- a slow start is not a stuck probe.
            try:
                line = q.get(timeout=(STARTUP if not ready else STALL))
            except queue.Empty:
                stalled = True
                stall_s += STALL
                break
            if line is None:
                break
            if line == "__READY__":
                ready = True
                continue
            if line == "__END__":
                ended = True
                continue
            if "|" not in line:
                continue
            pid = line.split("|", 1)[0]
            k = pos.get(pid)
            if k is None:
                continue
            got[pid] = line
            part.write(line + "\n")
            written += 1
            if written % 5000 == 0:
                part.flush()
            if k > last:
                last = k
        if stalled:
            try:
                pr.kill()      # the subprocess API's own name; the OUTCOME
                               # this produces is ABORT
            except OSError:
                pass
        pr.wait()
        if ended or last >= len(mine) - 1:
            break
        nxt = last + 1
        why = ("stalled>%.0fs" % STALL) if stalled else ("rc%s"
                                                         % pr.returncode)
        got[mine[nxt]] = "%s|ABORT|%s" % (mine[nxt], why)
        part.write(got[mine[nxt]] + "\n")
        part.flush()
        start = nxt + 1
        restarts += 1
        if restarts % 25 == 0:
            print("[worker %d] %d restarts, at %d/%d after %.1f s"
                  % (w, restarts, start, len(mine), time.time() - t0))
            sys.stdout.flush()
    part.close()
    with LOCK:
        RES.update(got)
        STATS[w] = dict(restarts=restarts, stall_s=stall_s,
                        wall_s=time.time() - t0, probes=len(mine))
    print("[worker %d] done: %d probes, %d restarts, %.1f s stalled, "
          "%.1f s wall" % (w, len(mine), restarts, stall_s,
                           time.time() - t0))
    sys.stdout.flush()


t0 = time.time()
ths = [threading.Thread(target=work, args=(w,)) for w in range(NW)]
for t in ths:
    t.start()


def progress():
    # the standing `[n/total]` progress line, so `airlock status` and
    # progress.sh have something to read.  `RES` only fills as a worker
    # FINISHES, so the live count is taken off the part files instead --
    # they are written as the answers arrive.
    while any(t.is_alive() for t in ths):
        time.sleep(15.0)
        with LOCK:
            done = len(RES)
        live = 0
        for w in range(NW):
            try:
                with open(OUT[:-4] + ".w%d.txt" % w, "rb") as fh:
                    live += sum(1 for _ in fh)
            except OSError:
                pass
        n = max(done, live)
        el = time.time() - t0
        rate = n / el if el > 0 else 0.0
        eta = ((len(ids) - n) / rate) if rate > 0 else -1.0
        print("[progress] python L%d [%d/%d] %5.1f%%  elapsed %.0fs  "
              "ETA %s  %.0f probes/s"
              % (LVL, n, len(ids), 100.0 * n / max(1, len(ids)), el,
                 ("%.0fs" % eta) if eta >= 0 else "--", rate))
        sys.stdout.flush()


pth = threading.Thread(target=progress, daemon=True)
pth.start()
for t in ths:
    t.join()
el = time.time() - t0
print("[progress] python L%d [%d/%d] 100.0%%  elapsed %.0fs"
      % (LVL, len(ids), len(ids), el))
sys.stdout.flush()

ans = raises = aborts = refused = missing = 0
with open(OUT, "w") as f:
    for pid in ids:
        line = RES.get(pid, "%s|MISSING|" % pid)
        f.write(line + "\n")
        kind = line.split("|")[1]
        if kind == "ANSWER":
            ans += 1
        elif kind == "RAISE":
            raises += 1
        elif kind == "ABORT":
            aborts += 1
        elif kind == "REFUSE":
            refused += 1
        else:
            missing += 1
    restarts = sum(s["restarts"] for s in STATS.values())
    stall_s = sum(s["stall_s"] for s in STATS.values())
    f.write("__SUMMARY__|python|%d|%d|%d|%d|%d|%.3f\n"
            % (len(ids), ans, raises, aborts, refused, el))
    f.write("__TIMING__|python|level=%d|workers=%d|processes=%d|probes=%d|"
            "compile_invocations=0|compile_s=0.000|stall_budget_s=%.1f|"
            "stall_s=%.3f|execute_s=%.3f|total_s=%.3f|restarts=%d\n"
            % (LVL, NW, restarts + NW, len(ids), STALL, stall_s,
               max(0.0, el - stall_s / max(1, NW)), el, restarts))
print("== cartesian python L%d: %d probes, %d answers, %d raises, %d aborts, "
      "%d refusals, %d missing, %d restarts, %.2f s wall"
      % (LVL, len(ids), ans, raises, aborts, refused, missing, restarts, el))
print("== TIMING python L%d: 0 files compiled (route C is exec, nothing is "
      "compiled ahead of time); %d python process(es) across %d workers -- "
      "%d workers plus %d restarts past a probe that stopped one; wall "
      "%.2f s; %.2f s of worker-time spent inside the %.1f s inactivity "
      "budget on stalls"
      % (LVL, restarts + NW, NW, NW, restarts, el, stall_s, STALL))
for w in sorted(STATS):
    s = STATS[w]
    print("   worker %d: %d probes, %d restarts, %.1f s stalled, %.1f s wall"
          % (w, s["probes"], s["restarts"], s["stall_s"], s["wall_s"]))
"""


def python_cells(level):
    tab = table("python", level)
    idx = sorted(t["i"] for t in tab)
    return [(op, i, j) for i in idx for j in idx for op in ops("python")]


def emit_python(level, shard=None, nshard=1, smoke=False):
    tab = table("python", level)
    hold = {t["i"]: t for t in tab}
    cells = python_cells(level)
    if smoke:
        cells = cells[:4]
    if shard is not None:
        cells = [c for n, c in enumerate(cells) if n % nshard == shard]
    name = "ct_python_l%d" % level
    if shard is not None:
        name += "_s%d" % shard
    if smoke:
        name += "_smoke"
    nprobe = 0
    for (op, i, j) in cells:
        na, nb = hold[i]["n"], hold[j]["n"]
        nprobe += na * nb if level == 1 else (na * nb) ** 2
    payload = dict(language="python", ops=ops("python"), holders=tab,
                   cells=cells, level=level, workers=PYTHON_WORKERS,
                   stall_s=PYTHON_STALL_S, out="/out/%s.txt" % name)
    sh = (PYTHON_SH
          .replace("__TABLE__", wrap(b64gz(json.dumps(payload))))
          .replace("__DRIVER__", wrap(base64.b64encode(
              PYTHON_DRIVER.encode("utf-8")).decode("ascii")))
          .replace("__RUNNER__", PYTHON_RUNNER)
          .replace("__NAME__", name)
          .replace("__LVL__", str(level))
          .replace("__SHARDNOTE__",
                   "shard %d of %d" % (shard, nshard) if shard is not None
                   else "")
          .replace("__NP__", str(nprobe)))
    return name + ".sh", sh, len(cells), nprobe


# ==================================================================
# log_062, 2026-08-22 -- THE REMAINING EIGHT
# ==================================================================
# Nothing about the design changes.  Same X / X' sets, same canonical
# form, same probe-index rule, same outcome vocabulary (REFUSE,
# RAISE:<kind>, ABORT, UNREPRESENTABLE), level 1 `y = op(x0,x1)` over all
# ordered pairs of X, level 2 `z = op(op(x0,x1), op(x2,x3))` over X'.
#
# Two patterns, exactly the two log_061 established:
#
#   INTERPRETED (ruby / python) -- php.  Worker processes, a stall
#   budget, nothing compiled ahead of time, the probe list never
#   materialised, a restart past any probe that stopped a worker.
#
#   COMPILED (rust / go) -- typescript, java, kotlin, c++, swift, dart,
#   c#.  Probes chunked per build; the built artefact takes a START
#   INDEX so an uncatchable ABORT costs ONE probe and not a chunk; a
#   chunk the compiler refuses is REPAIRED by mapping the compiler's own
#   error lines back to probes through `// __PROBE__` markers, and only
#   BISECTED when the compiler names no line at all.
#
# EVERY LANE'S OUTPUT LINE IS THE RUST SHAPE -- `pid|<type>|<ENCODING>`,
# `pid|-|RAISE:<kind>`, `pid|-|ABORT:<why>`, `pid|-|BUILDFAIL` -- so all
# eight fold through `l3_cart_read.read_rust` with NO reader change.
# php's driver emits the same shape rather than ruby's `pid|KIND|payload`
# for exactly that reason.
#
# THE FLOAT PATH IS BITS IN ALL EIGHT.  Not one of them prints a float
# and lets the reader parse the digits -- that is the log_057 fault and
# it has no path in here:
#
#   c++          memcpy of the object's bytes, byte-reversed  -> FLOAT:<w>:<hex>
#   java         Double.doubleToRawLongBits / Float.floatToRawIntBits
#   kotlin       the same two JDK calls
#   swift        Double.bitPattern / Float.bitPattern
#   dart         ByteData.setFloat64
#   c#           BitConverter.GetBytes(double), byte-reversed
#   typescript   DataView.setFloat64(0, v, false)
#   php          bin2hex(pack("E", $v))   -- big-endian IEEE-754 double
#
# The first seven are the settled `l3_exec.RT_*` runtimes, unmodified.
# php's is written here because php has no RT of its own, and it is the
# only new float path in this log; its round trip is proved in log_062.

# probes per compiled file.  MEASURED, not guessed: these are
# `l3_exec.CHUNK`, chosen in log_032 against each compiler's own habits
# (swift's type checker is superlinear in a file's size; java, kotlin and
# c# carry a 64 KB method limit that the two-level dispatch respects).
STATIC8_CHUNK = dict(EXEC_CHUNK)

# cpp RAISED from 2,000, log_063: g++ compiling this lane's own dispatch
# shape (plain function-pointer table, no method-size limit) measured
# NEAR-LINEAR from 500 to 32,000 probes/file on the host toolchain --
# 0.35s/500, 0.69s/2,000, 1.24s/4,000, 2.37s/8,000, 4.78s/16,000,
# 9.75s/32,000 -- no superlinear knee anywhere in that range.  8,000 cuts
# cpp's file count from 49 to 13 (a 4x reduction in g++ start-up
# amortised) while staying an order of magnitude under any figure that
# was actually measured.  The other six STATIC8 languages are UNCHANGED:
# no toolchain for java, kotlin, swift, dart, csharp or typescript exists
# in this sandbox, and l3_exec.CHUNK's own comment names two real,
# language-specific risks (swift's superlinear type checker, the 64 KB
# method limit) that make raising those caps a guess, not a measurement.
STATIC8_CHUNK["cpp"] = 8000

# the execution-side stall budget, log_063.  Missing entirely before this
# log: `run_binary`'s read loop blocked on `for line in pr.stdout` with
# NO timeout of any kind, so one probe that never writes a line (or a
# process that never exits) froze the whole lane forever -- this is what
# stalled `ct_cpp_l1.sh` at chunk 5/49, undetected, after chunk 4 had
# already shown an 18x jump in run time (10.88s vs 0.00s for 2,000
# probes).  Both numbers below are chosen, not measured -- no java,
# kotlin, swift, dart or csharp toolchain exists in this sandbox to time
# a cold start against -- but both are wide margins over every number
# any log in this line has actually recorded: STARTUP covers a JVM/.NET
# process's first line; STALL covers every later probe, at roughly
# 1,400x the 5.4 ms/probe the one anomalous cpp chunk actually showed.
STATIC8_STARTUP_S = 60.0
STATIC8_STALL_S = 15.0

# MEASURED milliseconds per probe, log_032 section "smoke lanes", one
# compile plus one run of a real chunk inside this very container image.
# rust measures 0.30 ms here against log_052's 0.25 ms on the cartesian
# run, so the two instruments agree and these numbers are usable as
# projections for the other languages.  php has no entry -- it is route C
# and is projected at ruby's measured interpreted rate instead.
MS_PER_PROBE = dict(go=0.29, rust=0.30, java=0.60, csharp=0.76,
                    typescript=0.24, swift=3.02, dart=0.72, cpp=1.63,
                    kotlin=5.60)

# `_emit`-side type name -> the holder rep in our table, per language.
# Used ONLY to decide level-2 cells: `op(y, y)` has to typecheck, and
# `y`'s type is READ OUT of the level-1 lane output, never guessed.
STATIC8_TYPE_REP = {
    "typescript": {"number": "number", "bigint": "bigint",
                   "boolean": "boolean"},
    "java": {"boolean": "boolean", "short": "short", "int": "int",
             "long": "long", "double": "double", "float": "float",
             "java.lang.Boolean": "Boolean", "java.lang.Integer": "Integer",
             "java.lang.Long": "Long", "java.lang.Short": "short",
             "java.lang.Double": "double", "java.lang.Float": "float"},
    "kotlin": {"kotlin.Boolean": "Boolean", "kotlin.Int": "Int",
               "kotlin.Long": "Long",
               "kotlin.Double": "Double", "kotlin.Float": "Float"},
    # c++ reports the DEMANGLED type, so `int32_t` arrives as `int` and
    # `uint64_t` as `unsigned long` on this platform.  The map is the
    # translation, not a rename of the holder.
    "cpp": {"bool": "bool", "int": "int32_t", "long": "int64_t",
            "unsigned long": "uint64_t", "__int128": "__int128",
            "double": "double", "float": "float"},
    "swift": {"Bool": "Bool", "Int": "Int", "Int32": "Int32",
              "Int64": "Int64", "UInt64": "UInt64", "Double": "Double",
              "Float": "Float"},
    "dart": {"bool": "bool", "int": "int", "BigInt": "BigInt",
             "double": "double", "num": "num"},
    "csharp": {"System.Boolean": "bool", "System.Int16": "short",
               "System.Int32": "int", "System.Int64": "long",
               "System.UInt64": "ulong", "System.Double": "double",
               "System.Single": "float"},
}

# which acceptance product each language's cells come from.  These are
# the census's own measured files; nothing here re-decides acceptance.
STATIC8_ACC = {"typescript": "acceptance_typescript_A1.json",
               "java": "acceptance_java_A1.json",
               "kotlin": "acceptance_kotlin_A1.json",
               "cpp": "acceptance_cpp_A2.json",
               "swift": "acceptance_swift_A2.json",
               "dart": "acceptance_dart_A2.json",
               "csharp": "acceptance_csharp_A1.json"}

STATIC8 = ["typescript", "java", "kotlin", "cpp", "swift", "dart", "csharp"]
EIGHT = ["php"] + STATIC8

# A dart holder's level-2 answer can be `double (whole number)` -- the
# census's own holder name carries a space, which no type name ever does,
# so the whole-form binary64 holder is reached through the `double` entry
# above and separated by FORM, exactly as `table()` already separates it.
STATIC8_TYPE_REP["dart"]["double"] = "double"


def accepted_static(lang):
    """{(op, lhs rep, rhs rep): verdict}, from the census's acceptance
    run.  Identical shape to `accepted_rust` / `accepted_go`; the file is
    the measurement and this function only reads it."""
    acc = json.load(open(os.path.join(HERE, STATIC8_ACC[lang])))
    v = {}
    for cell in acc["cells"].values():
        v[(cell["operation"], cell["lhs"]["holder"],
           cell["rhs"]["holder"])] = cell["verdict"]
    return v


def static_cells_l1(lang):
    """the ACCEPTED (op, lhs index, rhs index) cells over our holders."""
    verdict = accepted_static(lang)
    menu = set(ops(lang))
    tab = {t["rep"]: t for t in table(lang, 1)}
    cells = []
    for (op, lh, rh), vd in verdict.items():
        if vd != "ACCEPT" or op not in menu:
            continue
        if lh not in tab or rh not in tab:
            continue
        cells.append((op, tab[lh]["i"], tab[rh]["i"]))
    return sorted(set(cells))


def static_l1_output_types(lang):
    """(op index, lhs index, rhs index) -> the language's own name for the
    type of the level-1 answer, read out of the level-1 lane output.  No
    new measurement and no guess -- exactly the discipline
    `rust_l1_output_types` and `go_l1_output_types` apply."""
    p = None
    for d in (AIRLOCK_OUT, LANE_OUT, RAW):
        q = os.path.join(d, "ct_%s_l1.txt" % lang)
        if os.path.exists(q):
            p = q
            break
    if p is None:
        raise SystemExit("level-1 %s lane output not found (ct_%s_l1.txt); "
                         "run lanes/ct_%s_l1.sh first" % (lang, lang, lang))
    ty = {}
    for line in open(p):
        line = line.rstrip("\n")
        if line.startswith("__") or not line:
            continue
        pid, _, rest = line.partition("|")
        tn = rest.partition("|")[0]
        if tn == "-" or not pid.startswith("A"):
            continue
        try:
            k, i, j, _s = pid[1:].split("_")
        except ValueError:
            continue
        ty.setdefault((int(k), int(i), int(j)), tn)
    return ty


def static_cells_l2(lang):
    """(cells, why-skipped counter).  The composition has to typecheck, so
    the level-1 answer's OWN measured type has to be an ACCEPT cell
    against itself."""
    op_list = ops(lang)
    verdict = accepted_static(lang)
    rep_of = STATIC8_TYPE_REP[lang]
    ty = static_l1_output_types(lang)
    # rep -> the census holder name the acceptance file uses
    tab2 = {t["holder"]: t["rep"] for t in table(lang, 2)}
    cells, skipped = [], collections.Counter()
    for (op, i, j) in static_cells_l1(lang):
        k = op_list.index(op)
        tn = ty.get((k, i, j))
        if tn is None:
            skipped["no answered probe at level 1"] += 1
            continue
        holder = rep_of.get(tn)
        if holder is None or holder not in tab2:
            skipped["output type is not a holder in the table (%s)"
                    % tn.split("<")[0].split("[")[0]] += 1
            continue
        rep = tab2[holder]
        if verdict.get((op, rep, rep)) != "ACCEPT":
            skipped["`%s %s %s` is not an ACCEPT cell" % (rep, op, rep)] += 1
            continue
        cells.append((op, i, j))
    return cells, skipped


# ------------------------------------------------------------------
# the compiled lane -- one script shape for all seven
# ------------------------------------------------------------------
# THE TOOLCHAIN PREAMBLE IS NOT DECORATION.  Four of the seven live in
# the `sandbox-persist` named volume rather than in the image, and both
# Airlock's `up.sh` and SandboxDesign's mount that same volume at
# `/persist`, so they survive a container restart -- but the swift
# runtime's `libncurses.so.6` symlink does NOT, because it lives in the
# image's own `/usr/lib`.  It is therefore re-made at the top of every
# lane, exactly as `l3_exec_lanes.PRELUDE` has done since log_027.
#
# The lane REFUSES ITSELF, loudly and in two seconds, if its toolchain is
# missing, instead of burning an hour discovering it.

STATIC8_SH = r'''#!/bin/sh
# layer-3 CARTESIAN lane -- __LANG__ -- level __LVL__ __SHARDNOTE__ --
# generated by Research/kind_fuzz_clustering/l3_cart_gen.py (log_062).
# Do not hand-edit.  Static path: the ACCEPTED holder pairs only, from
# the census's own __ACC__.  A value the holder cannot represent is
# ABSENT from the row, never coerced.
set -u
export HOME=/work
export PATH=/persist/dart-sdk/bin:/persist/dotnet:/persist/kotlinc/bin:/persist/swift/usr/bin:$PATH
export DOTNET_CLI_TELEMETRY_OPTOUT=1
export DOTNET_NOLOGO=1
export DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1
# swift's binaries need libncurses.so.6 and the image ships only
# libncursesw.so.6.6.  The symlink lives in the image's own /usr/lib and
# therefore does NOT survive a container restart, so it is re-made here.
if [ -f /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 ]; then
  ln -sf /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 \
     /usr/lib/x86_64-linux-gnu/libncurses.so.6 2>/dev/null
  ldconfig 2>/dev/null
fi
echo "=== layer-3 CARTESIAN -- __LANG__ -- level __LVL__ -- __NP__ probes ==="
date -u +%Y-%m-%dT%H:%M:%SZ
# refuse in seconds rather than in an hour if the toolchain is not here
if ! __PROBECMD__ >/dev/null 2>&1; then
  echo "!! REFUSING TO START: __TOOLNAME__ is not runnable in this container."
  echo "!! tried: __PROBECMD__"
  echo "!! __TOOLNOTE__"
  exit 4
fi
__VERSIONCMD__ 2>&1 | head -2
ROOT=/work/__NAME__
rm -rf "$ROOT"; mkdir -p "$ROOT"
df -Pm /work | awk 'NR==2{print "free /work: " $4 " MB"}'
FREE=`df -Pm /work | awk 'NR==2{print $4}'`
if [ "$FREE" -lt 400 ]; then
  echo "!! REFUSING TO START: only $FREE MB free on /work, need 400"
  exit 3
fi
base64 -d <<'T_EOF' | gunzip > "$ROOT/table.json"
__TABLE__
T_EOF
base64 -d <<'X_EOF' | gunzip > "$ROOT/rt.txt"
__RT__
X_EOF
python3 - "$ROOT" <<'PY_EOF'
__DRIVER__
PY_EOF
rm -rf "$ROOT"
echo "swept $ROOT; /work free: $(df -Pm /work | awk 'NR==2{print $4}') MB"
date -u +%Y-%m-%dT%H:%M:%SZ
echo "=== cartesian __LANG__ level __LVL__ done ==="
'''

# per language: how to prove the toolchain is there, what to print, and
# what to say when it is not.  Verified 2026-08-22 against
# `Airlock/Containerfile` (c++, java, node) and against the contents of
# the `sandbox-persist` volume (kotlin, swift, dart, c#, the typescript
# checker) -- see log_062 section 1.
STATIC8_TOOL = {
    "cpp": ("g++ --version", "g++ --version", "g++",
            "gcc-15/g++-15 is installed by Airlock's own Containerfile"),
    "java": ("javac -version", "javac -version", "javac",
             "openjdk-25-jdk-headless is installed by Airlock's own "
             "Containerfile"),
    "typescript": ("node -e 'require(\"/persist/tv/ts5/node_modules/"
                   "typescript/lib/typescript.js\")'",
                   "node --version", "node + the typescript checker",
                   "node is in the image; the typescript checker lives in "
                   "the sandbox-persist volume at /persist/tv/ts5"),
    "kotlin": ("test -x /persist/kotlinc/bin/kotlinc",
               "/persist/kotlinc/bin/kotlinc -version", "kotlinc",
               "kotlinc lives in the sandbox-persist volume at "
               "/persist/kotlinc, not in the image"),
    "swift": ("/persist/swift/usr/bin/swiftc --version",
              "/persist/swift/usr/bin/swiftc --version", "swiftc",
              "swift lives in the sandbox-persist volume at /persist/swift "
              "and needs the libncurses symlink this lane re-makes"),
    "dart": ("/persist/dart-sdk/bin/dart --version",
             "/persist/dart-sdk/bin/dart --version", "dart",
             "the dart SDK lives in the sandbox-persist volume at "
             "/persist/dart-sdk, not in the image"),
    "csharp": ("/persist/dotnet/dotnet --version",
               "/persist/dotnet/dotnet --version", "dotnet",
               ".NET lives in the sandbox-persist volume at "
               "/persist/dotnet, not in the image -- Airlock's README "
               "records .NET absent from the IMAGE, which is true and is "
               "not the whole story"),
}

STATIC8_DRIVER = r'''
import json, os, queue, re, shutil, subprocess, sys, threading, time, glob

ROOT = sys.argv[1]
T = json.load(open(os.path.join(ROOT, "table.json")))
OUT = T["out"]
CH = T["chunk"]
LVL = T["level"]
LANG = T["language"]
# log_063: STALL used to be read here and never used again anywhere in
# this driver -- `run_binary`'s read loop had NO timeout at all, so one
# probe that never wrote a line froze the lane forever.  STARTUP is the
# grace before the first line (a JVM/.NET cold start is not a stall);
# STALL applies to every line after that, and a stall now COSTS ONE
# PROBE via the same START-INDEX restart discipline an uncatchable crash
# already used, never the whole lane.
STALL = T.get("stall_s", 15.0)
STARTUP = T.get("startup_s", 60.0)
RTX = open(os.path.join(ROOT, "rt.txt")).read()
HOLD = {h["i"]: h for h in T["holders"]}
OPS = T["ops"]
PRELINES = T.get("pre", [])
TAG = "A" if LVL == 1 else "B"
DOT = "/persist/dotnet"

# ---- the probe list.  A probe is (id, fn name, [decl lines], expr).
probes = []
for (op, i, j) in T["cells"]:
    k = OPS.index(op)
    ha, hb = HOLD[i], HOLD[j]
    na, nb = ha["n"], hb["n"]
    if LVL == 1:
        for i0 in range(na):
            for i1 in range(nb):
                p = i0 * nb + i1
                probes.append(("A%d_%d_%d_%d" % (k, i, j, p),
                               "p_%d_%d_%d_%d" % (k, i, j, p),
                               [ha["a"][i0], hb["b"][i1]],
                               "((a) %s (b))" % op))
    else:
        for i0 in range(na):
            for i1 in range(nb):
                for i2 in range(na):
                    for i3 in range(nb):
                        p = ((i0 * nb + i1) * na + i2) * nb + i3
                        probes.append((
                            "B%d_%d_%d_%d" % (k, i, j, p),
                            "p_%d_%d_%d_%d" % (k, i, j, p),
                            [ha["a"][i0], hb["b"][i1],
                             ha["c"][i2], hb["d"][i3]],
                            "(((a) %s (b)) %s ((c) %s (d)))" % (op, op, op)))

print("cartesian %s level %d: %d cells -> %d probes"
      % (LANG, LVL, len(T["cells"]), len(probes)))
sys.stdout.flush()

COMPILES = {"n": 0, "s": 0.0}


def _split_head(lines, kw):
    h, b = [], []
    for l in lines:
        (h if l.startswith(kw) else b).append(l)
    return h, b


def _dedup(seq):
    out = []
    for s in seq:
        if s not in out:
            out.append(s)
    return out


def _dispatch(ps, decl_fmt, case_fmt, close, group=100):
    """the two-level switch java, kotlin and c# need: a single method
    holding thousands of calls exceeds the 64 KB method limit."""
    n = len(ps)
    src = ""
    for g in range(0, n, group):
        src += decl_fmt % (g // group)
        for i in range(g, min(g + group, n)):
            src += case_fmt % (i, ps[i][1])
        src += close
    return src


def build_src(ps):
    """the whole chunk as ONE source file.  Every probe carries a
    `// __PROBE__ <id>` marker so a compiler error line maps back to the
    probe that caused it."""
    n = len(ps)

    def bodies(fmt):
        return "".join("// __PROBE__ %s\n%s" % (p[0], fmt(p))
                       for p in ps) + "// __PROBE__ -\n"

    if LANG == "cpp":
        src = RTX + "\n" + "\n".join(_dedup(PRELINES)) + "\n"
        src += bodies(lambda p:
                      "static void %s() {\n%s    auto _r = %s;\n"
                      '    _emit("%s", _r);\n}\n'
                      % (p[1], "".join("    %s\n" % d for d in p[2]),
                         p[3], p[0]))
        src += "\ntypedef void (*_FN)();\nstatic _FN _P[] = {\n"
        for p in ps:
            src += "  %s,\n" % p[1]
        src += "};\nstatic const char* _I[] = {\n"
        for p in ps:
            src += '  "%s",\n' % p[0]
        src += "};\n\nint main(int argc, char** argv) {\n"
        src += "  size_t n = %d;\n" % n
        src += "  size_t s = argc > 1 ? (size_t)atol(argv[1]) : 0;\n"
        src += ("  for (size_t i = s; i < n; i++) {\n"
                "    try { _P[i](); } catch (...) { _raise(_I[i], \"cxx\"); }\n"
                "  }\n")
        src += '  printf("__END__\\n");\n  return 0;\n}\n'
        return src, "chunk.cpp"

    if LANG == "swift":
        # swift cannot catch a trap IN LANGUAGE.  The START INDEX is the
        # whole defence: the driver restarts past the probe that stopped
        # the process, so an uncatchable stop costs ONE probe.
        src = RTX + "\n" + "\n".join(_dedup(PRELINES)) + "\n"
        src += bodies(lambda p:
                      "func %s() {\n%s    let _r = %s\n"
                      '    _emit("%s", _r)\n}\n'
                      % (p[1], "".join("    %s\n" % d for d in p[2]),
                         p[3], p[0]))
        src += "\nlet _I: [String] = [\n"
        for p in ps:
            src += '  "%s",\n' % p[0]
        src += "]\nlet _P: [() -> Void] = [\n"
        for p in ps:
            src += "  %s,\n" % p[1]
        src += "]\nsetvbuf(stdout, nil, _IONBF, 0)\nvar _s = 0\n"
        src += ("if CommandLine.arguments.count > 1 "
                "{ _s = Int(CommandLine.arguments[1]) ?? 0 }\n")
        src += "var _i = _s\nwhile _i < _P.count {\n  _P[_i]()\n  _i += 1\n}\n"
        src += 'print("__END__")\n'
        return src, "main.swift"

    if LANG == "dart":
        hdr, rest = _split_head(_dedup(PRELINES), "import ")
        src = "\n".join(hdr) + "\n" + RTX + "\n" + "\n".join(rest) + "\n"
        src += bodies(lambda p:
                      "void %s() {\n  try {\n%s    var _r = %s;\n"
                      "    _emit('%s', _r);\n  } catch (e) {\n"
                      "    stdout.writeln('%s|-|RAISE:' + "
                      "e.runtimeType.toString());\n  }\n}\n"
                      % (p[1], "".join("    %s\n" % d for d in p[2]),
                         p[3], p[0], p[0]))
        src += "\nfinal _P = <void Function()>[\n"
        for p in ps:
            src += "  %s,\n" % p[1]
        src += "];\n\nvoid main(List<String> args) {\n"
        src += "  var s = args.isNotEmpty ? int.parse(args[0]) : 0;\n"
        src += "  for (var i = s; i < _P.length; i++) { _P[i](); }\n"
        src += "  stdout.writeln('__END__');\n}\n"
        return src, "chunk.dart"

    if LANG == "typescript":
        src = "\n".join(_dedup(PRELINES)) + "\n" + RTX + "\n"
        src += bodies(lambda p:
                      "function %s(): void {\n  try {\n%s    let _r = %s;\n"
                      '    _emit("%s", _r);\n  } catch (e: any) {\n'
                      '    process.stdout.write("%s|-|RAISE:" + ((e && '
                      'e.constructor && e.constructor.name) || "error") + '
                      '"\\n");\n  }\n}\n'
                      % (p[1], "".join("    %s\n" % d for d in p[2]),
                         p[3], p[0], p[0]))
        src += "\nconst _P: Array<() => void> = [\n"
        for p in ps:
            src += "  %s,\n" % p[1]
        src += ("];\nconst _s: number = process.argv.length > 2 ? "
                "parseInt(process.argv[2]) : 0;\n")
        src += "for (let i = _s; i < _P.length; i++) { _P[i](); }\n"
        src += 'process.stdout.write("__END__\\n");\n'
        return src, "chunk.ts"

    if LANG == "java":
        rt_h, rt_b = _split_head(RTX.splitlines(), "import ")
        pr_h, pr_b = _split_head(_dedup(PRELINES), "import ")
        src = "\n".join(_dedup(pr_h + rt_h)) + "\n" + "\n".join(pr_b) + "\n"
        src += "\n".join(rt_b) + "\n\nclass Chunk {\n"
        src += bodies(lambda p:
                      "  static void %s() {\n    try {\n%s"
                      '      var _r = %s;\n      RT.emit("%s", _r);\n'
                      "    } catch (Throwable _t) {\n"
                      '      RT.raise("%s", _t);\n    }\n  }\n'
                      % (p[1], "".join("      %s\n" % d for d in p[2]),
                         p[3], p[0], p[0]))
        src += _dispatch(ps, "  static void d%d(int i) {\n    switch (i) {\n",
                         "      case %d: %s(); break;\n", "    }\n  }\n")
        src += "  static void run(int i) {\n    switch (i / 100) {\n"
        for g in range(0, n, 100):
            src += "      case %d: d%d(i); break;\n" % (g // 100, g // 100)
        src += "    }\n  }\n"
        src += ("  public static void main(String[] a) {\n    int s = "
                "a.length > 0 ? Integer.parseInt(a[0]) : 0;\n"
                "    for (int i = s; i < %d; i++) run(i);\n"
                '    System.out.println("__END__");\n  }\n}\n' % n)
        return src, "Chunk.java"

    if LANG == "kotlin":
        rt_h, rt_b = _split_head(RTX.splitlines(), "import ")
        pr_h, pr_b = _split_head(_dedup(PRELINES), "import ")
        src = "\n".join(_dedup(pr_h + rt_h)) + "\n" + "\n".join(pr_b) + "\n"
        src += "\n".join(rt_b) + "\n\n"
        src += bodies(lambda p:
                      "fun %s() {\n  try {\n%s    val _r = %s\n"
                      '    RT.emit("%s", _r)\n  } catch (_t: Throwable) {\n'
                      '    RT.raise("%s", _t)\n  }\n}\n'
                      % (p[1], "".join("    %s\n" % d for d in p[2]),
                         p[3], p[0], p[0]))
        src += _dispatch(ps, "fun d%d(i: Int) {\n  when (i) {\n",
                         "    %d -> %s()\n", "  }\n}\n")
        src += "fun run(i: Int) {\n  when (i / 100) {\n"
        for g in range(0, n, 100):
            src += "    %d -> d%d(i)\n" % (g // 100, g // 100)
        src += "  }\n}\n"
        src += ("fun main(args: Array<String>) {\n  val s = if "
                "(args.isNotEmpty()) args[0].toInt() else 0\n"
                "  for (i in s until %d) run(i)\n"
                '  println("__END__")\n}\n' % n)
        return src, "Chunk.kt"

    if LANG == "csharp":
        rt_h, rt_b = _split_head(RTX.splitlines(), "using ")
        pr_h, pr_b = _split_head(_dedup(PRELINES), "using ")
        src = "\n".join(_dedup(pr_h + rt_h)) + "\n" + "\n".join(pr_b) + "\n"
        src += "\n".join(rt_b) + "\n\nclass Chunk {\n"
        src += bodies(lambda p:
                      "  static void %s() {\n    try {\n%s"
                      '      var _r = %s;\n      RT.Emit("%s", _r);\n'
                      "    } catch (System.Exception _e) {\n"
                      '      RT.Raise("%s", _e.GetType().FullName);\n'
                      "    }\n  }\n"
                      % (p[1], "".join("      %s\n" % d for d in p[2]),
                         p[3], p[0], p[0]))
        src += _dispatch(ps, "  static void d%d(int i) {\n    switch (i) {\n",
                         "      case %d: %s(); break;\n", "    }\n  }\n")
        src += "  static void Run(int i) {\n    switch (i / 100) {\n"
        for g in range(0, n, 100):
            src += "      case %d: d%d(i); break;\n" % (g // 100, g // 100)
        src += "    }\n  }\n"
        src += ("  static void Main(string[] a) {\n    int s = a.Length > 0 "
                "? int.Parse(a[0]) : 0;\n"
                "    for (int i = s; i < %d; i++) Run(i);\n"
                '    System.Console.Out.Write("__END__\\n");\n'
                "    System.Console.Out.Flush();\n  }\n}\n" % n)
        return src, "Chunk.cs"

    raise SystemExit("no source builder for " + LANG)


def build_cmds(d, fname):
    """(compile argv list, run argv factory).  Copied unchanged from
    `l3_exec_lanes.build_cmds` -- these are the invocations the execution
    campaign of log_032 actually used inside this image."""
    if LANG == "cpp":
        return ([["g++", "-std=c++20", "-O0", "-w", "-o", d + "/bin",
                  d + "/" + fname]],
                lambda s: [d + "/bin", str(s)])
    if LANG == "swift":
        return ([["/persist/swift/usr/bin/swiftc", "-Onone",
                  "-suppress-warnings", "-o", d + "/bin", d + "/" + fname]],
                lambda s: [d + "/bin", str(s)])
    if LANG == "dart":
        return ([["/persist/dart-sdk/bin/dart", "compile", "exe",
                  d + "/" + fname, "-o", d + "/bin"]],
                lambda s: [d + "/bin", str(s)])
    if LANG == "java":
        return ([["javac", "-nowarn", "-d", d + "/cls", d + "/" + fname]],
                lambda s: ["java", "-cp", d + "/cls", "Chunk", str(s)])
    if LANG == "kotlin":
        std = "/persist/kotlinc/lib/kotlin-stdlib.jar"
        return ([["/persist/kotlinc/bin/kotlinc", "-nowarn", "-d", d + "/cls",
                  d + "/" + fname]],
                lambda s: ["java", "-cp", d + "/cls:" + std, "ChunkKt",
                           str(s)])
    if LANG == "csharp":
        refd = sorted(glob.glob(
            DOT + "/packs/Microsoft.NETCore.App.Ref/*/ref/net*"))[-1]
        csc = sorted(glob.glob(DOT + "/sdk/*/Roslyn/bincore/csc.dll"))[-1]
        ver = refd.split("/")[-3]
        tfm = refd.split("/")[-1]
        open(d + "/Chunk.runtimeconfig.json", "w").write(
            '{"runtimeOptions":{"tfm":"%s","framework":{"name":'
            '"Microsoft.NETCore.App","version":"%s"}}}' % (tfm, ver))
        refs = ["-reference:" + os.path.join(refd, f)
                for f in os.listdir(refd) if f.endswith(".dll")]
        return ([[DOT + "/dotnet", "exec", csc, "-nologo", "-nowarn:CS0168",
                  "-out:" + d + "/Chunk.dll", "-target:exe"] + refs
                 + [d + "/" + fname]],
                lambda s: [DOT + "/dotnet", d + "/Chunk.dll", str(s)])
    if LANG == "typescript":
        tsc = "/persist/tv/ts5/node_modules/typescript/lib/typescript.js"
        open(d + "/tr.js", "w").write(
            "const ts=require(%r);const fs=require('fs');"
            "const src=fs.readFileSync(process.argv[2],'utf8');"
            "const o=ts.transpileModule(src,{compilerOptions:"
            "{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS}});"
            "fs.writeFileSync(process.argv[3],o.outputText);" % tsc)
        return ([["node", d + "/tr.js", d + "/" + fname, d + "/chunk.js"]],
                lambda s: ["node", "--stack-size=4000", d + "/chunk.js",
                           str(s)])
    raise SystemExit("no toolchain for " + LANG)


_MARK = re.compile(r"^// __PROBE__ (\S+)\s*$")
_ERL = re.compile(r"(?:chunk|Chunk|main)\.[A-Za-z]+:(\d+)[:.]")
_ERC = re.compile(r"(?:chunk|Chunk|main)\.[A-Za-z]+\((\d+),\d+\)")


def probe_spans(src):
    marks = []
    for n, line in enumerate(src.splitlines(), 1):
        m = _MARK.match(line)
        if m:
            marks.append((n, m.group(1)))
    out = []
    for k, (n, pid) in enumerate(marks):
        end = marks[k + 1][0] - 1 if k + 1 < len(marks) else 10 ** 9
        out.append((n, end, pid))
    return out


def map_errors(msg, spans):
    """which probes did the compiler NAME?  {pid: short reason}.  This is
    the REPAIR step: the compiler points at its own line, so one refused
    probe costs one rebuild rather than a bisection."""
    hit = {}
    for ml in msg.splitlines():
        ms = _ERL.search(ml) or _ERC.search(ml)
        if not ms:
            continue
        ln = int(ms.group(1))
        for a, b, pid in spans:
            if a <= ln <= b:
                if pid != "-":
                    hit.setdefault(pid, ml.strip()[:120])
                break
    return hit


def compile_chunk(d, ps):
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    src, fname = build_src(ps)
    open(os.path.join(d, fname), "w").write(src)
    cmds, runf = build_cmds(d, fname)
    t = time.time()
    ok, msg = True, ""
    for c in cmds:
        r = subprocess.run(c, capture_output=True, text=True, cwd=d,
                           timeout=3000)
        if r.returncode != 0:
            ok = False
            msg = (r.stderr or "") + "\n" + (r.stdout or "")
            break
    el = time.time() - t
    COMPILES["n"] += 1
    COMPILES["s"] += el
    return ok, el, msg, src, runf


def _pump(fh, q):
    for line in fh:
        q.put(line.rstrip("\n"))
    q.put(None)


def run_binary(d, ps, runf, out):
    """the START-INDEX discipline, identical to rust's and go's: an
    uncatchable stop costs ONE probe, never the chunk.  log_063 adds the
    other half of that discipline -- a STALL (no line for STALL seconds
    once output has started, or none at all within STARTUP) is now also
    caught, `pr.kill()`-ed and restarted past, exactly like a crash, so
    it too costs one probe and not the lane's entire remaining budget."""
    ids = [p[0] for p in ps]
    pos = dict((p, k) for k, p in enumerate(ids))
    got = {}
    start = 0
    restarts = 0
    stall_s = 0.0
    t = time.time()
    while start < len(ids) and restarts < 2000:
        pr = subprocess.Popen(runf(start), stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True, cwd=d,
                              bufsize=1)
        q = queue.Queue()
        threading.Thread(target=_pump, args=(pr.stdout, q),
                         daemon=True).start()
        last = start - 1
        ended = stalled = False
        ready = False
        while True:
            try:
                line = q.get(timeout=(STARTUP if not ready else STALL))
            except queue.Empty:
                stalled = True
                stall_s += (STARTUP if not ready else STALL)
                break
            if line is None:
                break
            ready = True
            if line == "__END__":
                ended = True
                continue
            if "|" not in line:
                continue
            pid = line.split("|", 1)[0]
            k = pos.get(pid)
            if k is None:
                continue
            got[pid] = line
            if k > last:
                last = k
        if stalled:
            try:
                pr.kill()      # the subprocess API's own name; the
                               # OUTCOME this produces is ABORT
            except OSError:
                pass
        pr.wait()
        if ended or last >= len(ids) - 1:
            break
        nxt = last + 1
        why = ("stalled>%.0fs" % (STARTUP if not ready else STALL)) \
            if stalled else ("rc%s" % pr.returncode)
        got[ids[nxt]] = "%s|-|ABORT:%s" % (ids[nxt], why)
        start = nxt + 1
        restarts += 1
        if stalled:
            print("   .. probe %s stalled (%s); killed and restarting "
                  "at probe %d" % (ids[nxt], why, start))
            sys.stdout.flush()
    el = time.time() - t
    a = r_ = ab = 0
    for pid in ids:
        line = got.get(pid, "%s|-|MISSING" % pid)
        out.write(line + "\n")
        if "|-|RAISE:" in line:
            r_ += 1
        elif "|-|ABORT:" in line:
            ab += 1
        elif "|-|MISSING" in line:
            pass
        else:
            a += 1
    out.flush()
    return a, r_, ab, restarts, el, stall_s


def handle(d, ps, out, depth=0):
    """compile with REPAIR, then run.  Returns
    (answers, raises, aborts, buildfail, restarts, build_s, run_s,
    stall_s)."""
    refused = {}
    cur = list(ps)
    tb = 0.0
    ok = False
    runf = None
    for attempt in range(16):
        if not cur:
            ok = True
            break
        okc, el, msg, src, runf = compile_chunk(d, cur)
        tb += el
        if okc:
            ok = True
            break
        bad = map_errors(msg, probe_spans(src))
        if not bad:
            break
        print("   .. chunk of %d refused; the compiler named %d probe(s), "
              "dropping them and rebuilding (attempt %d)"
              % (len(cur), len(bad), attempt + 1))
        sys.stdout.flush()
        for pid, why in bad.items():
            refused[pid] = why
        cur = [p for p in cur if p[0] not in bad]
    if not ok:
        # the compiler refused and named no line at all -- BISECT, so a
        # nameless refusal still costs one probe and not a chunk.
        if len(cur) == 1:
            open(OUT + ".compilefail." + cur[0][0] + ".txt", "w").write(
                (msg or "")[:60000])
            refused[cur[0][0]] = "buildfail"
            for pid in refused:
                out.write("%s|-|BUILDFAIL\n" % pid)
            out.flush()
            return 0, 0, 0, len(refused), 0, tb, 0.0, 0.0
        print("   !! chunk of %d failed to build and named nothing; "
              "bisecting (depth %d)" % (len(cur), depth))
        sys.stdout.flush()
        h = len(cur) // 2
        acc = [0, 0, 0, 0, 0, tb, 0.0, 0.0]
        for half, sub in enumerate((cur[:h], cur[h:])):
            got = handle(d + "_%d%d" % (depth, half), sub, out, depth + 1)
            for x in range(8):
                acc[x] += got[x]
        for pid in refused:
            out.write("%s|-|BUILDFAIL\n" % pid)
            acc[3] += 1
        out.flush()
        return tuple(acc)
    a = r_ = ab = rs = 0
    tr = ss = 0.0
    if cur:
        a, r_, ab, rs, tr, ss = run_binary(d, cur, runf, out)
    for pid in refused:
        out.write("%s|-|BUILDFAIL\n" % pid)
    out.flush()
    shutil.rmtree(d, ignore_errors=True)
    return a, r_, ab, len(refused), rs, tb, tr, ss


chunks = [probes[x:x + CH] for x in range(0, len(probes), CH)]
print("chunking: %d probes -> %d chunk files, at most %d probes per file"
      % (len(probes), len(chunks), CH))
sys.stdout.flush()

out = open(OUT, "w")
t0 = time.time()
answers = raises = aborts = buildfail = restarts = 0
build_s = run_s = stall_s = 0.0
done = 0
for ci, ps in enumerate(chunks):
    d = os.path.join(ROOT, "c%05d" % ci)
    a, r_, ab, bf, rs, tb, tr, ss = handle(d, ps, out)
    answers += a; raises += r_; aborts += ab
    buildfail += bf; restarts += rs
    build_s += tb; run_s += tr; stall_s += ss
    done += len(ps)
    el = time.time() - t0
    eta = (el / done) * (len(probes) - done) if done else -1.0
    print("[progress] %s L%d chunk %d/%d [%d/%d] %5.1f%%  build %.2fs  "
          "run %.2fs  stall %.2fs  elapsed %.0fs  ETA %.0fs"
          % (LANG, LVL, ci + 1, len(chunks), done, len(probes),
             100.0 * done / max(1, len(probes)), tb, tr, ss, el, eta))
    sys.stdout.flush()

el = time.time() - t0
print("[progress] %s L%d [%d/%d] 100.0%%  elapsed %.0fs"
      % (LANG, LVL, len(probes), len(probes), el))
out.write("__SUMMARY__|%s|%d|%d|%d|%d|%d|%.3f\n"
          % (LANG, len(probes), answers, raises, aborts, buildfail, el))
out.write("__TIMING__|%s|level=%d|chunk_files=%d|probes=%d|chunk_cap=%d|"
          "compile_invocations=%d|compile_s=%.3f|execute_s=%.3f|"
          "other_s=%.3f|total_s=%.3f|restarts=%d|stall_s=%.3f\n"
          % (LANG, LVL, len(chunks), len(probes), CH, COMPILES["n"],
             COMPILES["s"], run_s, el - COMPILES["s"] - run_s, el, restarts,
             stall_s))
out.close()
print("== cartesian %s L%d: %d probes, %d answers, %d raises, %d aborts, "
      "%d buildfail, %.2f s" % (LANG, LVL, len(probes), answers, raises,
                                aborts, buildfail, el))
print("== TIMING %s L%d: %d chunk FILES (cap %d probes each), %d compile "
      "invocations totalling %.2f s; execution %.2f s; driver overhead "
      "%.2f s; wall %.2f s"
      % (LANG, LVL, len(chunks), CH, COMPILES["n"], COMPILES["s"], run_s,
         el - COMPILES["s"] - run_s, el))
'''

RT8 = dict(cpp=RT_CPP, swift=RT_SWIFT, dart=RT_DART, csharp=RT_CSHARP,
           java=RT_JAVA, kotlin=RT_KOTLIN, typescript=RT_TS)


def _pre_lines(tab):
    """the `pre` lines the participating holders declare, deduplicated.
    In practice only c++ carries any (`#include <cstdint>` and friends);
    every holder that carried an `import` is one of the excluded
    decimal/bignum holders, so the list is empty for the other six."""
    out = []
    for t in tab:
        for line in (t.get("pre") or "").splitlines():
            line = line.strip()
            if line and line not in out:
                out.append(line)
    return out


def emit_static8(lang, level, shard=None, nshard=1, smoke=False):
    tab = table(lang, level)
    if level == 1:
        cells = static_cells_l1(lang)
        skipped = collections.Counter()
    else:
        cells, skipped = static_cells_l2(lang)
    if smoke:
        cells = cells[:3]
    if shard is not None:
        cells = [c for n, c in enumerate(cells) if n % nshard == shard]
    name = "ct_%s_l%d" % (lang, level)
    if shard is not None:
        name += "_s%d" % shard
    if smoke:
        name += "_smoke"
    hold = {t["i"]: t for t in tab}
    nprobe = 0
    for (op, i, j) in cells:
        na, nb = hold[i]["n"], hold[j]["n"]
        nprobe += na * nb if level == 1 else (na * nb) ** 2
    payload = dict(language=lang, ops=ops(lang), holders=tab, cells=cells,
                   level=level, chunk=STATIC8_CHUNK[lang],
                   pre=_pre_lines(tab), out="/out/%s.txt" % name,
                   stall_s=STATIC8_STALL_S, startup_s=STATIC8_STARTUP_S)
    probecmd, vercmd, toolname, toolnote = STATIC8_TOOL[lang]
    sh = (STATIC8_SH
          .replace("__TABLE__", wrap(b64gz(json.dumps(payload))))
          .replace("__RT__", wrap(b64gz(RT8[lang])))
          .replace("__DRIVER__", STATIC8_DRIVER)
          .replace("__NAME__", name)
          .replace("__LVL__", str(level))
          .replace("__LANG__", lang)
          .replace("__ACC__", STATIC8_ACC[lang])
          .replace("__PROBECMD__", probecmd)
          .replace("__VERSIONCMD__", vercmd)
          .replace("__TOOLNAME__", toolname)
          .replace("__TOOLNOTE__", toolnote)
          .replace("__SHARDNOTE__",
                   "shard %d of %d" % (shard, nshard) if shard is not None
                   else "")
          .replace("__NP__", str(nprobe)))
    return name + ".sh", sh, len(cells), nprobe, skipped


# ==================================================================
# swift's &+ / &- / &* -- HAND-ADDED wrapping-arithmetic operators
# (log_065 diagnosed the gap; log_066 closes it; the owner greenlit running
# BOTH levels, 2026-08-23)
# ==================================================================
# WHY HAND-ADDED, NOT GRAMMAR-EXTRACTED.  Every operator anywhere else
# in this file arrives through `l3_accept.ops()`: the grammar's own
# positioned anonymous tokens (`kinds_<lang>.json`) intersected with a
# candidate vocabulary.  Swift's `&+`/`&-`/`&*` cannot arrive that way
# -- Swift lexes them as a REGEX-MATCHED `custom_operator` grammar node,
# not fixed anonymous string tokens, so `kinds_swift.json`'s 109-entry
# `anonymous` list contains exactly one `&`-token (`&&`) and structurally
# never will (confirmed against the archived tree-sitter grammar,
# `0_Archive/PseudoIR_(retired)/v2/grammars/swift/node-types.json`,
# whose `custom_operator` node type is the mechanism -- log_065).  They
# ARE real swift infix OPERATORS (Swift's `FixedWidthInteger` protocol),
# not method calls, so they belong in the operator data despite the
# extraction blindness -- the one genuine operator-spelling gap log_065
# found across all twelve languages.
#
# Kept in a SEPARATE namespace from `ops("swift")` / `accepted_static`
# / `static_cells_l1/l2` ON PURPOSE -- a mechanical choice, not a
# structural one, reversible by merging later.  `ops("swift")` and
# `acceptance_swift_A2.json` are the census's own MEASURED products;
# folding a hand-derived verdict into them would blur measured and
# hand-derived data in one file, and would also renumber or commingle
# probe ids with the ALREADY-RUN `ct_swift_l1.txt`/`ct_swift_l2.txt`
# lanes.  `SWIFT_WRAP_*` below, plus `emit_swift_wrap`, is the whole
# addition; nothing about `ops()`, `accepted_static()`,
# `static_cells_l1/l2()`, `STATIC8_*`, or any existing swift lane
# changes.
SWIFT_WRAP_OPS = ["&+", "&-", "&*"]

# ACCEPTANCE -- NOT measured by a fresh swiftc -typecheck pass (the
# census's own route for every other operator), DERIVED, and the
# derivation is stated so it can be checked or overturned.  `&+`/`&-`/
# `&*` are declared in the Swift standard library ONLY on types
# conforming to `FixedWidthInteger`
# (`static func &+ (Self, Self) -> Self` -- same type on both operands
# AND the result, no promotion).  This is a NARROWER version of a
# pattern already MEASURED for `*` in `acceptance_swift_A2.json`: read
# directly (log_065/log_066), `*` ACCEPTs on EXACTLY the 6 same-type
# pairs `Int Int, Int32 Int32, Int64 Int64, UInt64 UInt64,
# Double Double, Float Float` and REFUSEs every other one of swift's
# 576 candidate pairs -- so same-type-only is a MEASURED fact for this
# operator family, not an assumption reached for the first time here.
# `&+`/`&-`/`&*`'s domain is that same same-type rule, restricted to
# the four INTEGER holders (`Double`/`Float` do not conform to
# `FixedWidthInteger`, so they are taken REFUSE -- general Swift-
# language knowledge, UNVERIFIED by a swiftc acceptance measurement).
#
# SAFE IN BOTH DIRECTIONS BY CONSTRUCTION.  An over-included cell simply
# fails to compile; the STATIC8 driver's own repair-before-bisect
# discipline (reused UNMODIFIED here) bisects it down to the single
# probe and records BUILDFAIL, which `read_rust` already folds to
# REFUSE (log_062 section 7) -- wasted compile time, not a wrong
# answer. An under-included cell would be a true coverage gap; none is
# believed to exist (every non-`FixedWidthInteger` swift type in the
# census already REFUSEs `*` for the identical protocol-conformance
# reason), but this is flagged here, not asserted as closed.
SWIFT_WRAP_INT_REPS = ("Int", "Int32", "Int64", "UInt64")


def swift_wrap_cells_l1():
    """the hand-derived ACCEPT cells: same-type pairs only, over the
    four swift integer holders already in the census's own table."""
    tab = {t["rep"]: t for t in table("swift", 1)}
    cells = [(op, tab[rep]["i"], tab[rep]["i"])
             for op in SWIFT_WRAP_OPS for rep in SWIFT_WRAP_INT_REPS]
    return sorted(set(cells))


def swift_wrap_l1_output_types():
    """(op index, lhs index, rhs index) -> swift's own type name of the
    L1 answer, read out of `ct_swift_wrap_l1.txt` -- no guess, the same
    discipline `static_l1_output_types` applies, pointed at THIS lane's
    own output rather than the shared `ct_swift_l1.txt`."""
    p = None
    for d in (AIRLOCK_OUT, LANE_OUT, RAW):
        q = os.path.join(d, "ct_swift_wrap_l1.txt")
        if os.path.exists(q):
            p = q
            break
    if p is None:
        raise SystemExit("level-1 swift-wrap lane output not found "
                         "(ct_swift_wrap_l1.txt); run "
                         "lanes/ct_swift_wrap_l1.sh first")
    ty = {}
    for line in open(p):
        line = line.rstrip("\n")
        if line.startswith("__") or not line:
            continue
        pid, _, rest = line.partition("|")
        tn = rest.partition("|")[0]
        if tn == "-" or not pid.startswith("A"):
            continue
        try:
            k, i, j, _s = pid[1:].split("_")
        except ValueError:
            continue
        ty.setdefault((int(k), int(i), int(j)), tn)
    return ty


def swift_wrap_cells_l2():
    """(cells, why-skipped counter).  `op(y, y)` has to typecheck; y's
    type is read out of the REAL level-1 lane output (never guessed),
    exactly `static_cells_l2`'s discipline, checked against the
    hand-derived ACCEPT set above instead of `acceptance_swift_A2.json`
    (which has no entries at all for these three operators)."""
    ty = swift_wrap_l1_output_types()
    rep_of = STATIC8_TYPE_REP["swift"]
    tab2 = {t["holder"]: t["rep"] for t in table("swift", 2)}
    accept = set((op, rep) for op in SWIFT_WRAP_OPS
                for rep in SWIFT_WRAP_INT_REPS)
    cells, skipped = [], collections.Counter()
    for (op, i, j) in swift_wrap_cells_l1():
        k = SWIFT_WRAP_OPS.index(op)
        tn = ty.get((k, i, j))
        if tn is None:
            skipped["no answered probe at level 1"] += 1
            continue
        holder = rep_of.get(tn)
        if holder is None or holder not in tab2:
            skipped["output type is not a holder in the table (%s)"
                    % tn] += 1
            continue
        rep = tab2[holder]
        if (op, rep) not in accept:
            skipped["`%s %s %s` is not a hand-derived ACCEPT cell"
                    % (rep, op, rep)] += 1
            continue
        cells.append((op, i, j))
    return cells, skipped


def emit_swift_wrap(level, shard=None, nshard=1, smoke=False):
    """the SAME STATIC8_SH / STATIC8_DRIVER template swift's other six
    operators use -- nothing about the lane mechanics, the stall
    watchdog (log_063), the BITS float path, the START-INDEX restart
    discipline or the `[n/total]` progress line changes.  Only the
    operator list and the cell set are swapped for the hand-derived
    ones above, and the lane is named and filed separately
    (`ct_swift_wrap_l<N>`) so it can never be confused with, or
    re-submitted alongside, the already-run `ct_swift_l<N>` lane."""
    lang = "swift"
    tab = table(lang, level)
    if level == 1:
        cells = swift_wrap_cells_l1()
        skipped = collections.Counter()
    else:
        cells, skipped = swift_wrap_cells_l2()
    if smoke:
        cells = cells[:3]
    if shard is not None:
        cells = [c for n, c in enumerate(cells) if n % nshard == shard]
    name = "ct_swift_wrap_l%d" % level
    if shard is not None:
        name += "_s%d" % shard
    if smoke:
        name += "_smoke"
    hold = {t["i"]: t for t in tab}
    nprobe = 0
    for (op, i, j) in cells:
        na, nb = hold[i]["n"], hold[j]["n"]
        nprobe += na * nb if level == 1 else (na * nb) ** 2
    payload = dict(language=lang, ops=SWIFT_WRAP_OPS, holders=tab,
                   cells=cells, level=level, chunk=STATIC8_CHUNK[lang],
                   pre=_pre_lines(tab), out="/out/%s.txt" % name,
                   stall_s=STATIC8_STALL_S, startup_s=STATIC8_STARTUP_S)
    probecmd, vercmd, toolname, toolnote = STATIC8_TOOL[lang]
    sh = (STATIC8_SH
          .replace("__TABLE__", wrap(b64gz(json.dumps(payload))))
          .replace("__RT__", wrap(b64gz(RT8[lang])))
          .replace("__DRIVER__", STATIC8_DRIVER)
          .replace("__NAME__", name)
          .replace("__LVL__", str(level))
          .replace("__LANG__", "swift (&+/&-/&*, hand-added, log_066)")
          .replace("__ACC__", "hand-derived ACCEPT set, NOT "
                              + STATIC8_ACC[lang] + " -- see log_066")
          .replace("__PROBECMD__", probecmd)
          .replace("__VERSIONCMD__", vercmd)
          .replace("__TOOLNAME__", toolname)
          .replace("__TOOLNOTE__", toolnote)
          .replace("__SHARDNOTE__",
                   "shard %d of %d" % (shard, nshard) if shard is not None
                   else "")
          .replace("__NP__", str(nprobe)))
    return name + ".sh", sh, len(cells), nprobe, skipped


# ==================================================================
# php lane -- the INTERPRETED shape
# ==================================================================
# Built on `emit_ruby` / `emit_python`, point for point: route C, nothing
# compiled ahead of time, every ordered holder pair times the operator
# menu runs, the probe list is NEVER materialised (arithmetic enumeration
# from a per-cell plan with prefix sums and an O(1) decode from a global
# probe index to the four operand indices, so a restart resumes in
# constant time), the driver announces `__READY__` so a slow start is not
# mistaken for a stuck probe, each worker writes its own part file as
# answers arrive, and a probe that stops a worker is recorded ABORT and
# stepped past.
#
# THE FLOAT PATH IS BITS.  `_ser` emits a php float as
# `FLOAT:64:<bin2hex(pack("E", $v))>` -- `E` is php's own big-endian
# IEEE-754 double packing, the identical token rust, go, python and the
# other seven emit, decoded by the identical `decode_enc`.  php's
# `var_dump`/`(string)` grain is never used for a float, so the log_057
# fault has no path into php's canon.
#
# php's line shape is the RUST shape, not ruby's, so the fold reads it
# with `read_rust` and no reader branch is added anywhere.
#
# PHP HAS NO UNBOUNDED INTEGER.  `PHP_INT_MAX + 1` becomes a FLOAT rather
# than raising, so php's whole column is expected to answer `FLOAT:64:`
# where ruby answers an exact integer.  That is a measurement, and it is
# named here so the run confirms or refutes it rather than surprising a
# reader later.

PHP_STALL_S = 2.0            # ruby's number, carried deliberately and NOT
                             # measured for php.  php has no unbounded
                             # integer, so the `**` stall that forced
                             # python down to 0.5 s cannot arise -- an
                             # oversized power becomes INF at once.  The
                             # budget is therefore a safety net, not a
                             # throughput control, and it is left at the
                             # recorded ruling's value rather than
                             # invented.
PHP_WORKERS = 5              # 6 cores in the runner; one left for the shell
PHP_L2_SHARDS = 1            # set from the projection at emit time

PHP_SH = """#!/bin/sh
# layer-3 CARTESIAN lane -- php -- level __LVL__ __SHARDNOTE__ --
# generated by Research/kind_fuzz_clustering/l3_cart_gen.py (log_062).
# Do not hand-edit.  Route C: execution is the only acceptance evidence
# php has, so every ordered holder pair times the operator menu runs.
set -u
export HOME=/work
ROOT=/work/__NAME__
rm -rf "$ROOT"; mkdir -p "$ROOT"
echo "=== layer-3 CARTESIAN -- php -- level __LVL__ -- __NP__ probes ==="
date -u +%Y-%m-%dT%H:%M:%SZ
if ! php -v >/dev/null 2>&1; then
  echo "!! REFUSING TO START: php is not runnable in this container."
  echo "!! php-cli is installed by Airlock's own Containerfile."
  exit 4
fi
php -v | head -1
base64 -d <<'T_EOF' | gunzip > "$ROOT/table.json"
__TABLE__
T_EOF
base64 -d <<'DRV_EOF' > "$ROOT/drv.php"
__DRIVER__
DRV_EOF
python3 - "$ROOT" <<'PY_EOF'
__RUNNER__
PY_EOF
rm -rf "$ROOT"
date -u +%Y-%m-%dT%H:%M:%SZ
echo "=== cartesian php level __LVL__ done ==="
"""

PHP_DRIVER = r'''<?php
// the cartesian probe driver for php.  Route C: every probe is eval'd.
// Emits the RUST line shape -- `pid|<type>|<ENCODING>` -- so the fold
// reads php with `l3_cart_read.read_rust` and no new reader branch.
error_reporting(0);
ini_set("display_errors", "0");
ini_set("memory_limit", "2048M");
$ROOT = $argv[1];
$SHARD = isset($argv[2]) ? intval($argv[2]) : 0;
$START = isset($argv[3]) ? intval($argv[3]) : 0;

$T = json_decode(file_get_contents($ROOT . "/table.json"), true);
$HS = $T["holders"]; $OPS = $T["ops"]; $LVL = $T["level"];
$CELLS = $T["cells"]; $NW = $T["workers"];

function _hx($s) { return bin2hex($s); }

function _ser($r) {
    // THE FLOAT PATH IS BITS.  `pack("E", ...)` is php's own big-endian
    // IEEE-754 double; no printed decimal is ever produced.
    if ($r === null) return array("NULL", "NULL");
    if (is_bool($r)) return array("boolean", "BOOL:" . ($r ? "true" : "false"));
    if (is_int($r)) return array("integer", "INT:64:" . sprintf("%016x", $r));
    if (is_float($r)) return array("double", "FLOAT:64:" . _hx(pack("E", $r)));
    if (is_string($r)) {
        // php's OWN length notion for a string is BYTES -- `strlen` --
        // and both slots of the STR token are therefore bytes.  `mbstring`
        // is deliberately not called: `php-cli` is the only php package
        // in the image and the extension is not verified present, so a
        // lane that needed it would fail at run time for a reason that
        // has nothing to do with the measurement.
        $u = $r;
        if (strlen($u) > 2000) $u = substr($u, 0, 2000);
        return array("string", "STR:" . strlen($u) . ":" .
                     strlen($u) . ":" . _hx($u));
    }
    if (is_array($r)) {
        $ps = array();
        foreach ($r as $k => $v) {
            $kk = _ser($k); $vv = _ser($v);
            $ps[] = $kk[1] . "=>" . $vv[1];
        }
        sort($ps);
        return array("array", "MAP:" . count($ps) . "[" .
                     implode(",", $ps) . "]");
    }
    return array(gettype($r), "OPAQUE:");
}

$HB = array();
foreach ($HS as $h) { $HB[$h["i"]] = $h; }

// The probe list is NEVER materialised -- the ruby lane's defect A
// (log_052 section 10) applies word for word.  The enumeration is
// arithmetic: a per-cell plan with prefix sums and an O(1) decode from a
// global probe index to the four operand indices, so a restart resumes
// in constant time instead of replaying the run so far.
$PLAN = array(); $TOTAL = 0;
foreach ($CELLS as $cell) {
    list($op, $i, $j) = $cell;
    $k = array_search($op, $OPS, true);
    $ha = $HB[$i]; $hb = $HB[$j];
    $na = $ha["n"]; $nb = $hb["n"];
    $n = ($LVL == 1) ? ($na * $nb) : ($na * $nb) * ($na * $nb);
    $PLAN[] = array($TOTAL, $n, $k, $i, $j, $op, $ha, $hb, $na, $nb);
    $TOTAL += $n;
}

echo "__READY__\n";
flush();

function _locate($g) {
    global $PLAN;
    $lo = 0; $hi = count($PLAN) - 1;
    while ($lo < $hi) {
        $mid = intdiv($lo + $hi + 1, 2);
        if ($PLAN[$mid][0] <= $g) { $lo = $mid; } else { $hi = $mid - 1; }
    }
    return $PLAN[$lo];
}

$l = $START;
while (true) {
    $g = $l * $NW + $SHARD;
    if ($g >= $TOTAL) break;
    list($base, $n, $k, $i, $j, $op, $ha, $hb, $na, $nb) = _locate($g);
    $p = $g - $base;
    if ($LVL == 1) {
        $i1 = $p % $nb; $i0 = intdiv($p, $nb);
        $pid = "A{$k}_{$i}_{$j}_{$p}";
        $src = $ha["a"][$i0] . "\n" . $hb["b"][$i1] .
               "\n\$__r = ((\$a) {$op} (\$b));";
    } else {
        $i3 = $p % $nb; $t = intdiv($p, $nb);
        $i2 = $t % $na; $t2 = intdiv($t, $na);
        $i1 = $t2 % $nb; $i0 = intdiv($t2, $nb);
        $pid = "B{$k}_{$i}_{$j}_{$p}";
        $src = $ha["a"][$i0] . "\n" . $hb["b"][$i1] . "\n" .
               $ha["c"][$i2] . "\n" . $hb["d"][$i3] .
               "\n\$__r = (((\$a) {$op} (\$b)) {$op} ((\$c) {$op} (\$d)));";
    }
    $__r = null;
    try {
        $ok = @eval($src);
        if ($ok === false) {
            // php 7 returned false from eval on a parse error; php 8
            // throws ParseError.  Both are the language REFUSING the
            // source, not raising on a value, so both take the same
            // token -- `read_rust` folds `-|BUILDFAIL` to REFUSE.
            echo "{$pid}|-|BUILDFAIL\n";
        } else {
            $e = _ser($__r);
            echo "{$pid}|{$e[0]}|{$e[1]}\n";
        }
    } catch (ParseError $pe) {
        echo "{$pid}|-|BUILDFAIL\n";
    } catch (Throwable $ex) {
        echo "{$pid}|-|RAISE:" . get_class($ex) . "\n";
    }
    $l += 1;
}
echo "__END__\n";
'''

# The runner is the ruby/python runner's machinery with php's interpreter
# and driver file.  It is a SEPARATE constant rather than a
# parameterisation of either, deliberately: `ct_ruby_l{1,2}.sh` are the
# scripts of the run of record (log_052) and `ct_python_l*.sh` are
# already queued in Airlock (log_061), and neither one's generated bytes
# may move because something was added here.
PHP_RUNNER = r"""
import json
import os
import queue
import subprocess
import sys
import threading
import time

ROOT = sys.argv[1]
T = json.load(open(os.path.join(ROOT, "table.json")))
OUT = T["out"]
STALL = T["stall_s"]        # a stall is an ABORT and an ABORT is excluded
                            # from scoring in the numerator AND the
                            # denominator, so this budget costs wall clock
                            # and no measurement.
STARTUP = 120.0             # a driver's setup grace, separate from the
                            # per-probe stall budget
NW = T["workers"]
LVL = T["level"]
HS, OPS, CELLS = T["holders"], T["ops"], T["cells"]
HB = dict((h["i"], h) for h in HS)

ids = []
for (op, i, j) in CELLS:
    k = OPS.index(op)
    na, nb = HB[i]["n"], HB[j]["n"]
    n = na * nb if LVL == 1 else (na * nb) ** 2
    tag = "A" if LVL == 1 else "B"
    for p in range(n):
        ids.append("%s%d_%d_%d_%d" % (tag, k, i, j, p))

shards = [ids[w::NW] for w in range(NW)]
print("cartesian php level %d: %d cells -> %d probes, sharded across %d "
      "worker processes; stall budget %.1f s"
      % (LVL, len(CELLS), len(ids), NW, STALL))
sys.stdout.flush()


def pump(fh, q):
    for line in fh:
        q.put(line.rstrip("\n"))
    q.put(None)


RES = {}
STATS = {}
LOCK = threading.Lock()


def work(w):
    mine = shards[w]
    pos = dict((p, k) for k, p in enumerate(mine))
    got = {}
    part = open(OUT[:-4] + ".w%d.txt" % w, "w")
    written = 0
    start = 0
    restarts = 0
    stall_s = 0.0
    t0 = time.time()
    while start < len(mine) and restarts < 20000:
        pr = subprocess.Popen(["php", os.path.join(ROOT, "drv.php"), ROOT,
                               str(w), str(start)],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True,
                              bufsize=1)
        q = queue.Queue()
        threading.Thread(target=pump, args=(pr.stdout, q),
                         daemon=True).start()
        last = start - 1
        ended = stalled = False
        ready = False
        while True:
            try:
                line = q.get(timeout=(STARTUP if not ready else STALL))
            except queue.Empty:
                stalled = True
                stall_s += STALL
                break
            if line is None:
                break
            if line == "__READY__":
                ready = True
                continue
            if line == "__END__":
                ended = True
                continue
            if "|" not in line:
                continue
            pid = line.split("|", 1)[0]
            k = pos.get(pid)
            if k is None:
                continue
            got[pid] = line
            part.write(line + "\n")
            written += 1
            if written % 5000 == 0:
                part.flush()
            if k > last:
                last = k
        if stalled:
            try:
                pr.kill()      # the subprocess API's own name; the OUTCOME
                               # this produces is ABORT
            except OSError:
                pass
        pr.wait()
        if ended or last >= len(mine) - 1:
            break
        nxt = last + 1
        why = ("stalled>%.0fs" % STALL) if stalled else ("rc%s"
                                                         % pr.returncode)
        got[mine[nxt]] = "%s|-|ABORT:%s" % (mine[nxt], why)
        part.write(got[mine[nxt]] + "\n")
        part.flush()
        start = nxt + 1
        restarts += 1
        if restarts % 25 == 0:
            print("[worker %d] %d restarts, at %d/%d after %.1f s"
                  % (w, restarts, start, len(mine), time.time() - t0))
            sys.stdout.flush()
    part.close()
    with LOCK:
        RES.update(got)
        STATS[w] = dict(restarts=restarts, stall_s=stall_s,
                        wall_s=time.time() - t0, probes=len(mine))
    print("[worker %d] done: %d probes, %d restarts, %.1f s stalled, "
          "%.1f s wall" % (w, len(mine), restarts, stall_s,
                           time.time() - t0))
    sys.stdout.flush()


t0 = time.time()
ths = [threading.Thread(target=work, args=(w,)) for w in range(NW)]
for t in ths:
    t.start()


def progress():
    # the standing `[n/total]` progress line.  `RES` only fills as a
    # worker FINISHES, so the live count is taken off the part files.
    while any(t.is_alive() for t in ths):
        time.sleep(15.0)
        with LOCK:
            done = len(RES)
        live = 0
        for w in range(NW):
            try:
                with open(OUT[:-4] + ".w%d.txt" % w, "rb") as fh:
                    live += sum(1 for _ in fh)
            except OSError:
                pass
        n = max(done, live)
        el = time.time() - t0
        rate = n / el if el > 0 else 0.0
        eta = ((len(ids) - n) / rate) if rate > 0 else -1.0
        print("[progress] php L%d [%d/%d] %5.1f%%  elapsed %.0fs  "
              "ETA %s  %.0f probes/s"
              % (LVL, n, len(ids), 100.0 * n / max(1, len(ids)), el,
                 ("%.0fs" % eta) if eta >= 0 else "--", rate))
        sys.stdout.flush()


pth = threading.Thread(target=progress, daemon=True)
pth.start()
for t in ths:
    t.join()
el = time.time() - t0
print("[progress] php L%d [%d/%d] 100.0%%  elapsed %.0fs"
      % (LVL, len(ids), len(ids), el))
sys.stdout.flush()

ans = raises = aborts = refused = missing = 0
with open(OUT, "w") as f:
    for pid in ids:
        line = RES.get(pid, "%s|-|MISSING" % pid)
        f.write(line + "\n")
        if "|-|RAISE:" in line:
            raises += 1
        elif "|-|ABORT:" in line:
            aborts += 1
        elif "|-|BUILDFAIL" in line:
            refused += 1
        elif "|-|MISSING" in line:
            missing += 1
        else:
            ans += 1
    restarts = sum(s["restarts"] for s in STATS.values())
    stall_s = sum(s["stall_s"] for s in STATS.values())
    f.write("__SUMMARY__|php|%d|%d|%d|%d|%d|%.3f\n"
            % (len(ids), ans, raises, aborts, refused, el))
    f.write("__TIMING__|php|level=%d|workers=%d|processes=%d|probes=%d|"
            "compile_invocations=0|compile_s=0.000|stall_budget_s=%.1f|"
            "stall_s=%.3f|execute_s=%.3f|total_s=%.3f|restarts=%d\n"
            % (LVL, NW, restarts + NW, len(ids), STALL, stall_s,
               max(0.0, el - stall_s / max(1, NW)), el, restarts))
print("== cartesian php L%d: %d probes, %d answers, %d raises, %d aborts, "
      "%d refusals, %d missing, %d restarts, %.2f s wall"
      % (LVL, len(ids), ans, raises, aborts, refused, missing, restarts, el))
for w in sorted(STATS):
    s = STATS[w]
    print("   worker %d: %d probes, %d restarts, %.1f s stalled, %.1f s wall"
          % (w, s["probes"], s["restarts"], s["stall_s"], s["wall_s"]))
"""


def php_cells(level):
    tab = table("php", level)
    idx = sorted(t["i"] for t in tab)
    return [(op, i, j) for i in idx for j in idx for op in ops("php")]


def emit_php(level, shard=None, nshard=1, smoke=False):
    tab = table("php", level)
    hold = {t["i"]: t for t in tab}
    cells = php_cells(level)
    if smoke:
        cells = cells[:4]
    if shard is not None:
        cells = [c for n, c in enumerate(cells) if n % nshard == shard]
    name = "ct_php_l%d" % level
    if shard is not None:
        name += "_s%d" % shard
    if smoke:
        name += "_smoke"
    nprobe = 0
    for (op, i, j) in cells:
        na, nb = hold[i]["n"], hold[j]["n"]
        nprobe += na * nb if level == 1 else (na * nb) ** 2
    payload = dict(language="php", ops=ops("php"), holders=tab, cells=cells,
                   level=level, workers=PHP_WORKERS, stall_s=PHP_STALL_S,
                   out="/out/%s.txt" % name)
    sh = (PHP_SH
          .replace("__TABLE__", wrap(b64gz(json.dumps(payload))))
          .replace("__DRIVER__", wrap(base64.b64encode(
              PHP_DRIVER.encode("utf-8")).decode("ascii")))
          .replace("__RUNNER__", PHP_RUNNER)
          .replace("__NAME__", name)
          .replace("__LVL__", str(level))
          .replace("__SHARDNOTE__",
                   "shard %d of %d" % (shard, nshard) if shard is not None
                   else "")
          .replace("__NP__", str(nprobe)))
    return name + ".sh", sh, len(cells), nprobe


# ==================================================================

def write(name, sh, drop=True):
    os.makedirs(LANES, exist_ok=True)
    p = os.path.join(LANES, name)
    with open(p, "w") as f:
        f.write(sh)
    os.chmod(p, 0o755)
    if drop and os.path.isdir(DROP):
        with open(os.path.join(DROP, name), "w") as f:
            f.write(sh)
    return p


# ------------------------------------------------------------------
# projected cost, from log_052's MEASURED rates.  Printed before any
# level-2 lane is dropped, as a standing requirement -- never as a
# substitute for the wall clock the run itself reports.
# ------------------------------------------------------------------
# rust  646,659 probes in 162.0 s  (98% of it rustc)   -> 3,992 probes/s
# ruby  9,396,120 probes in 2,347.3 s (route C, 5 workers) -> 4,003 /s
MEASURED_RATE = {
    "compiled": 646659.0 / 162.0,       # the rust cartesian run of record
    "interpreted": 9396120.0 / 2347.3,  # the ruby cartesian run of record
}
DAEMON_CEILING_S = 3600.0               # Airlock SCRIPT_TIMEOUT default
SHARD_LIMIT_S = 7200.0                  # "shard anything beyond ~2 hours"


def project(nprobe, shape, stall_probes=0, stall_s=0.0, workers=1):
    """throughput plus the MEASURED stall bill.  A bare probes-per-second
    number is not an honest projection for python: 0.58% of its level-2
    probes stall on `**`, and at a 2 s budget those alone would be 90% of
    the wall clock."""
    s = nprobe / MEASURED_RATE[shape]
    s += stall_probes * stall_s / max(1, workers)
    return s, "%dm %02ds" % (int(s) // 60, int(s) % 60)


def announce(name, nprobe, shape, stall_probes=0, stall_s=0.0, workers=1):
    s, hm = project(nprobe, shape, stall_probes, stall_s, workers)
    flag = ""
    if s > SHARD_LIMIT_S:
        flag = "  <-- BEYOND ~2 h, MUST BE SHARDED"
    elif s > DAEMON_CEILING_S:
        flag = "  <-- beyond the daemon's %.0f s ceiling" % DAEMON_CEILING_S
    extra = ""
    if stall_probes:
        extra = (" + %d measured stalls at %.2f s over %d workers"
                 % (stall_probes, stall_s, workers))
    print("        projection for %s: %d probes at the measured %s rate "
          "(%.0f probes/s)%s -> %s wall%s"
          % (name, nprobe, shape, MEASURED_RATE[shape], extra, hm, flag))
    return s


# ------------------------------------------------------------------
# log_062 -- projection and sharding for the eight
# ------------------------------------------------------------------
# The compiled languages are NOT projected at rust's rate.  rust compiles
# 1,500 probes in 0.31 s and kotlinc compiles 2,000 in about twenty
# seconds; using one number for both would be a fiction.  Each language
# is projected at ITS OWN measured ms-per-probe from log_032's smoke
# lanes, which were taken in this same container image.  rust appears in
# both instruments and agrees between them, which is what makes the table
# usable.

SHARD_TARGET_S = 2400.0        # aim each shard near 40 min, well inside
                               # the daemon's 3,600 s ceiling and well
                               # inside the ~2 h line


def project8(lang, nprobe):
    """(seconds, "Nm SSs") for one lane of one of the eight."""
    if lang in MS_PER_PROBE:
        s = nprobe * MS_PER_PROBE[lang] / 1000.0
    else:
        s = nprobe / MEASURED_RATE["interpreted"]
    return s, "%dm %02ds" % (int(s) // 60, int(s) % 60)


def shards_for(lang, nprobe):
    """how many lane scripts this family needs so no one lane projects
    past the ~2 h line.  Shard counts are DERIVED from the projection,
    never chosen by hand."""
    s, _ = project8(lang, nprobe)
    if s <= SHARD_TARGET_S:
        return 1
    return int(s // SHARD_TARGET_S) + 1


def announce8(name, lang, nprobe):
    s, hm = project8(lang, nprobe)
    rate = ("%.2f ms/probe, measured (log_032)" % MS_PER_PROBE[lang]
            if lang in MS_PER_PROBE
            else "%.0f probes/s, measured (log_052 ruby)"
                 % MEASURED_RATE["interpreted"])
    flag = ""
    if s > SHARD_LIMIT_S:
        flag = "  <-- BEYOND ~2 h, MUST BE SHARDED"
    elif s > DAEMON_CEILING_S:
        flag = "  <-- beyond the daemon's %.0f s ceiling" % DAEMON_CEILING_S
    print("        projection for %s: %d probes at %s -> %s wall%s"
          % (name, nprobe, rate, hm, flag))
    return s


def batch_manifest(label, lanes):
    """`agent/batch.json` in Airlock's own byte shape.  ONE lane object
    per line matters -- `progress.sh`'s parser is line-based, not a
    general JSON parser, so a manifest that wraps a lane across several
    lines is silently read as no lane at all."""
    import datetime
    now = datetime.datetime.now(datetime.timezone.utc)
    bid = "batch-" + now.strftime("%Y%m%dT%H%M%SZ")
    out = ['{',
           '  "batch_id": "%s",' % bid,
           '  "label": "%s",' % label,
           '  "created": "%s",' % now.isoformat(),
           '  "lanes": [']
    for n, (script, weight) in enumerate(lanes):
        comma = "," if n < len(lanes) - 1 else ""
        out.append('    { "script": "%s", "weight": %d }%s'
                   % (script, weight, comma))
    out.append('  ]')
    out.append('}')
    return "\n".join(out) + "\n", bid


def main_eight(want, smoke, drop):
    """`--eight`: php, typescript, java, kotlin, c++, swift, dart, c#.

    LEVEL ORDER IS A DEPENDENCY, NOT A PREFERENCE.  A level-2 cell for a
    statically checked language exists only where `op(y, y)` typechecks,
    and `y`'s type is READ OUT of that language's level-1 lane output --
    the discipline `rust_cells_l2` has applied since log_052 and
    `go_cells_l2` since log_061.  So every level-1 lane runs before any
    level-2 lane can even be emitted, and the generator says so by name
    instead of failing obscurely.  php is route C and has no such
    question, so its level-2 lanes are emitted now."""
    print("CARTESIAN lanes -- THE REMAINING EIGHT (log_062, 2026-08-22).  "
          "The settled design of 2026-08-21, unchanged: LEVEL 1 "
          "y = op(x0,x1) over all ordered pairs of X; LEVEL 2 "
          "z = op(op(x0,x1), op(x2,x3)) over X'.  php follows the "
          "ruby/python pattern (interpreted, worker processes, a stall "
          "budget, nothing compiled); the other seven follow the rust/go "
          "pattern (compiled, chunked per build, START-INDEX restart, a "
          "repairing/bisecting driver).%s\n"
          % ("  SMOKE." if smoke else ""))
    made = []
    if "l1" in want:
        print("  -- LEVEL 1 --")
        name, sh, nc, np_ = emit_php(1, smoke=smoke)
        print("  %-26s %5d cells, %9d probes, %d KB"
              % (name, nc, np_, len(sh) // 1024))
        announce8(name, "php", np_)
        write(name, sh, drop)
        made.append((name, np_))
        for lang in STATIC8:
            name, sh, nc, np_, _ = emit_static8(lang, 1, smoke=smoke)
            print("  %-26s %5d cells, %9d probes, %d KB"
                  % (name, nc, np_, len(sh) // 1024))
            announce8(name, lang, np_)
            write(name, sh, drop)
            made.append((name, np_))
    if "l2" in want:
        print("\n  -- LEVEL 2 --")
        whole = emit_php(2, smoke=smoke)[3]
        ns = shards_for("php", whole)
        for s in range(ns):
            name, sh, nc, np_ = emit_php(
                2, shard=(s if ns > 1 else None), nshard=ns, smoke=smoke)
            print("  %-26s %5d cells, %9d probes, %d KB"
                  % (name, nc, np_, len(sh) // 1024))
            announce8(name, "php", np_)
            write(name, sh, drop)
            made.append((name, np_))
        for lang in STATIC8:
            try:
                whole = emit_static8(lang, 2, smoke=smoke)[3]
            except SystemExit as exc:
                print("  ct_%s_l2.sh  NOT EMITTED -- %s" % (lang, exc))
                print("        %s's level-2 cells are derived from the "
                      "MEASURED TYPE of each level-1 answer, so "
                      "lanes/ct_%s_l1.sh must run first.  This is the "
                      "dependency that makes 'every level-1 lane before "
                      "any level-2 lane' a requirement rather than a "
                      "preference." % (lang, lang))
                continue
            ns = shards_for(lang, whole)
            for s in range(ns):
                name, sh, nc, np_, skipped = emit_static8(
                    lang, 2, shard=(s if ns > 1 else None), nshard=ns,
                    smoke=smoke)
                print("  %-26s %5d cells, %9d probes, %d KB"
                      % (name, nc, np_, len(sh) // 1024))
                if s == 0:
                    for why, n in skipped.most_common():
                        print("        %d level-1 cells get NO level-2 row "
                              "-- %s" % (n, why))
                announce8(name, lang, np_)
                write(name, sh, drop)
                made.append((name, np_))
    tot = sum(n for _, n in made)
    ts, thm = 0.0, ""
    print("\n  %d lane scripts, %d probes in total" % (len(made), tot))
    print("  lanes written to %s and NOT dropped.\n"
          "  Submit each with:\n"
          "    python3 %s/airlock submit %s/<lane.sh> --batch <label> "
          "--weight <probe count>"
          % (LANES, AIRLOCK_DROP.rsplit("/agent", 1)[0], LANES))
    return made


def main():
    argv = sys.argv[1:]
    smoke = "--smoke" in argv
    want = [a for a in argv if not a.startswith("--")] or ["l1", "l2"]
    drop = "--no-drop" not in argv
    release = "--release" in argv
    pygo = "--pygo" in argv
    eight = "--eight" in argv

    if eight:
        # `--manifest <label>` takes a value, and the value must not be
        # mistaken for a level selector.
        if "--manifest" in argv:
            k = argv.index("--manifest")
            if k + 1 < len(argv) and not argv[k + 1].startswith("--"):
                want = [a for a in want if a != argv[k + 1]]
        want = want or ["l1", "l2"]
        # These lanes go to AIRLOCK through `airlock submit`, which
        # validates a lane before it becomes a run.  `write()`'s
        # auto-drop targets SandboxDesign's tree (unchanged, log_060) and
        # is therefore forced OFF -- a drop into the wrong tree is never
        # seen by the running container and looks exactly like a hung
        # queue (log_061 section 0).
        made = main_eight(want, smoke, drop=False)
        if "--manifest" in argv:
            label = "eight-languages-log062"
            k = argv.index("--manifest")
            if k + 1 < len(argv) and not argv[k + 1].startswith("--"):
                label = argv[k + 1]
            text, bid = batch_manifest(label, made)
            p = os.path.join(LANES, "batch_%s.json" % label)
            open(p, "w").write(text)
            print("\n  batch manifest written: %s\n"
                  "    label %s, id %s, %d lanes, weight %d"
                  % (p, label, bid, len(made),
                     sum(n for _, n in made)))
        return

    if pygo:
        # These lanes go to AIRLOCK, not to SandboxDesign, and they go
        # through `airlock submit` so the lane is validated before it
        # becomes a run.  `write()`'s auto-drop targets SandboxDesign's
        # tree (unchanged, log_060) and is therefore forced OFF here --
        # a drop into the wrong tree is never seen by the running
        # container and would look exactly like a hung queue.
        drop = False
        # log_061, 2026-08-22: the python + go extension.  Emits ONLY the
        # two new languages' lanes -- rust and ruby already ran (log_052,
        # log_057) and are not touched.  ORDER IS ENFORCED BY THE CALLER:
        # both level-1 lanes run before either level-2 lane, because
        # go's level-2 cells are read out of go's level-1 answers.
        print("CARTESIAN lanes -- PYTHON + GO (log_061, 2026-08-22).  The "
              "settled design of 2026-08-21, unchanged: LEVEL 1 "
              "y = op(x0,x1) over all ordered pairs of X; LEVEL 2 "
              "z = op(op(x0,x1), op(x2,x3)) over X'.  python follows the "
              "ruby pattern (interpreted, worker processes, a stall "
              "budget, nothing compiled); go follows the rust pattern "
              "(compiled, chunked per build, START-INDEX restart).%s\n"
              % ("  SMOKE." if smoke else ""))
        if "l1" in want:
            name, sh, nc, np_, _ = emit_go(1, smoke)
            print("  %-24s %5d cells, %9d probes, %d KB"
                  % (name, nc, np_, len(sh) // 1024))
            announce(name, np_, "compiled")
            write(name, sh, drop)
            name, sh, nc, np_ = emit_python(1, smoke=smoke)
            print("  %-24s %5d cells, %9d probes, %d KB"
                  % (name, nc, np_, len(sh) // 1024))
            announce(name, np_, "interpreted")
            write(name, sh, drop)
        if "l2" in want:
            # go's level-2 cells are read out of go's level-1 ANSWERS --
            # `op(y, y)` has to typecheck and `y`'s type is measured, not
            # guessed.  So the order is not a convention, it is a
            # dependency: without ct_go_l1.txt there is nothing to emit,
            # and saying so is better than emitting a guess.
            try:
                name, sh, nc, np_, skipped = emit_go(2, smoke)
            except SystemExit as exc:
                print("  ct_go_l2.sh  NOT EMITTED -- %s" % exc)
                print("        go's level-2 cells are derived from the "
                      "TYPE of each level-1 answer, so ct_go_l1.sh must "
                      "run first.  This is the dependency that makes "
                      "'both level-1 lanes before either level-2 lane' a "
                      "requirement rather than a preference.")
            else:
                print("  %-24s %5d cells, %9d probes, %d KB"
                      % (name, nc, np_, len(sh) // 1024))
                for why, n in skipped.most_common():
                    print("        %d level-1 cells get NO level-2 row -- %s"
                          % (n, why))
                announce(name, np_, "compiled")
                write(name, sh, drop)
            allp = sum(emit_python(2, shard=s, nshard=PYTHON_L2_SHARDS,
                                   smoke=smoke)[3]
                       for s in range(PYTHON_L2_SHARDS))
            whole, _hm = project(allp, "interpreted",
                                 PYTHON_L2_STALL_PROBES, PYTHON_STALL_S,
                                 PYTHON_WORKERS)
            print("        python level 2 UNSHARDED would project %dm %02ds "
                  "-- past the %.0f s daemon ceiling, so it is cut across "
                  "%d lane scripts"
                  % (int(whole) // 60, int(whole) % 60, DAEMON_CEILING_S,
                     PYTHON_L2_SHARDS))
            tot = 0
            for s in range(PYTHON_L2_SHARDS):
                name, sh, nc, np_ = emit_python(
                    2, shard=(s if PYTHON_L2_SHARDS > 1 else None),
                    nshard=PYTHON_L2_SHARDS, smoke=smoke)
                tot += np_
                print("  %-24s %5d cells, %9d probes, %d KB"
                      % (name, nc, np_, len(sh) // 1024))
                announce(name, np_, "interpreted",
                         PYTHON_L2_STALL_PROBES // PYTHON_L2_SHARDS,
                         PYTHON_STALL_S, PYTHON_WORKERS)
                write(name, sh, drop)
            print("        python level 2 total: %d probes across %d lane "
                  "scripts, %d worker processes each"
                  % (tot, PYTHON_L2_SHARDS, PYTHON_WORKERS))
        print("\n  lanes written to %s and NOT dropped.  Submit each with:\n"
              "    python3 %s/airlock submit <lane.sh> --batch <label> "
              "--weight <probe count>"
              % (LANES, AIRLOCK_DROP.rsplit("/agent", 1)[0]))
        return

    if release:
        # Job B (log_057, 2026-08-22): the rust RELEASE column.  The
        # debug lanes already ran (log_052); this emits ONLY the
        # release-mode counterpart, tagged `rust_release` so it never
        # silently merges with the debug rows.  Ruby has no release
        # notion in this design and is not touched.
        print("CARTESIAN lanes -- RUST RELEASE COLUMN (log_057, "
              "2026-08-22).  Same cells as the debug lanes, built with "
              "%s instead of %s, tagged language=rust_release so the "
              "two never merge.%s\n"
              % (RUST_RELEASE_FLAGS, RUST_DEBUG_FLAGS,
                 "  SMOKE." if smoke else ""))
        if "l1" in want:
            name, sh, nc, np_, _ = emit_rust(1, smoke, release=True)
            print("  %-22s %5d cells, %8d probes, %d KB"
                  % (name, nc, np_, len(sh) // 1024))
            write(name, sh, drop)
        if "l2" in want:
            name, sh, nc, np_, skipped = emit_rust(2, smoke, release=True)
            print("  %-22s %5d cells, %8d probes, %d KB"
                  % (name, nc, np_, len(sh) // 1024))
            for why, n in skipped.most_common():
                print("        %d level-1 cells get NO level-2 row -- %s"
                      % (n, why))
            write(name, sh, drop)
        return

    print("CARTESIAN lanes -- the settled design of 2026-08-21.  "
          "LEVEL 1 y = op(x0,x1) over all ordered pairs of X; LEVEL 2 "
          "z = op(op(x0,x1), op(x2,x3)) over X'.  Scope: rust + ruby "
          "only.%s\n" % ("  SMOKE." if smoke else ""))

    if "l1" in want:
        name, sh, nc, np_, _ = emit_rust(1, smoke)
        print("  %-22s %5d cells, %8d probes, %d KB"
              % (name, nc, np_, len(sh) // 1024))
        write(name, sh, drop)
        name, sh, nc, np_ = emit_ruby(1, smoke=smoke)
        print("  %-22s %5d cells, %8d probes, %d KB"
              % (name, nc, np_, len(sh) // 1024))
        write(name, sh, drop)

    if "l2" in want:
        name, sh, nc, np_, skipped = emit_rust(2, smoke)
        print("  %-22s %5d cells, %8d probes, %d KB"
              % (name, nc, np_, len(sh) // 1024))
        for why, n in skipped.most_common():
            print("        %d level-1 cells get NO level-2 row -- %s"
                  % (n, why))
        write(name, sh, drop)
        tot = 0
        for s in range(RUBY_L2_SHARDS):
            name, sh, nc, np_ = emit_ruby(
                2, shard=(s if RUBY_L2_SHARDS > 1 else None),
                nshard=RUBY_L2_SHARDS, smoke=smoke)
            tot += np_
            print("  %-22s %5d cells, %8d probes, %d KB"
                  % (name, nc, np_, len(sh) // 1024))
            write(name, sh, drop)
        print("        ruby level 2 total: %d probes across %d lane "
              "scripts, %d worker processes each" % (tot, RUBY_L2_SHARDS,
                                                     RUBY_WORKERS))


if __name__ == "__main__":
    main()
