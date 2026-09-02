#!/usr/bin/env python3
"""l3_construct_value.py -- the construct pass at the VALUE grain.

Log 037 measured the nine statically checked languages at the HOLDER
grain: every holder at its BASE value class, 21,342 probes.  It left
open (CHECK 5t) whether a construct's domain MOVES when the value
varies.  This file runs the full value matrix of `construct_design.md`
§h for those nine, so the question is measured rather than assumed.

WHY THE HOLDER GRAIN IS NOT ENOUGH -- measured, not argued.
`construct_space.py` says in words that "in a statically checked
language the verdict is a function of the holder pair and not of the
value".  That reading is FALSE for 79 of the 226 holders of the nine.
A holder's declaration text is not fixed across its value classes:
java's `List.of(...)` holder declares `List<Long>`, `List<String>` and
`List<Object>` at three different value classes, and those are three
different types.  A verdict measured at the base value is therefore not
a verdict for the holder.  `verdict_moves.py` prints the 79.

WHAT IS GENERATED.  The same scaffolds, the same recorders, the same
lane machinery.  Only the slot filling changes: where log 037 wrote
`base_value(h)`, this writes every value class of h, and the probe id
carries the value class exactly as decision 14 specifies:

    one slot     K<construct>_<i>_<x>
    two slots    K<construct>_<i>_<j>_<x>_<y>
    three slots  K<construct>_<i>_<x>_<b1>_<b2>

WHAT IS NOT GENERATED.  `flow.break` and `flow.continue` open no
operand slot (decision 8), so they have no value grain at all.  Their
five k-probes stand as log 037 measured them.

SHARDS.  The daemon kills a script at 3600 s.  A language's probes are
cut into contiguous shards small enough to finish well inside that, and
each shard freezes its own manifest and writes its own pair of raw
files.  A shard is a unit of SCHEDULING and never of measurement: the
gate reads them added together.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from l3_accept import holders, rename                      # noqa: E402
from construct_space import (space, AUG_OPS,               # noqa: E402
                             WHOLE_BOUNDS)
import l3_construct_lang as L                              # noqa: E402
import l3_construct_go as G                                # noqa: E402

LANES = os.path.join(HERE, "lanes")
NINE = ["typescript", "csharp", "java", "dart", "rust", "go",
        "cpp", "swift", "kotlin"]          # cost order, kotlin last

# probes per shard, per language.  Chosen from log 037's MEASURED
# per-probe cost so that no shard approaches the daemon's 3600 s kill:
#   typescript 2.8 ms   csharp 6.8 ms   java 6.7 ms   dart 3.4 ms
#   rust 14.8 ms        go 15.7 ms      cpp 60.0 ms   swift 68.1 ms
#   kotlin 71.7 ms
SHARD = dict(typescript=8000, csharp=8000, java=6000, dart=8000,
             rust=12000, go=10000, cpp=6000, swift=6000, kotlin=8000)

TWO = ("access.subscript", "binding.augassign")
NO_SLOT = ("flow.break", "flow.continue")

# 68 shards run back to back on the serial lane, and each one makes its
# own directory under /work.  /work is memory backed and 2 GB.  A shard
# therefore removes its own scratch when it is finished and prints what
# is left, so that the shards do not add up the way log 030's run did.
CLEANUP = ('rm -rf "$ROOT" /work/.gocache /work/.gopath\n'
           "df -Pm /work | awk 'NR==2{print \"scratch after: free /work \""
           " $4 \" MB\"}'\n")

# a SMOKE run writes lanes named `kw_*` and raw files named `wx_/wy_`,
# so it can never overwrite a measured lane's script or its output.
# Set by VALUE_CAP being non-zero.  This is the log 037 lesson: the
# smoke run there caught a typescript fault that would otherwise have
# published a language refusing every probe.
PFX = "kv"
RAWP = "v"


# ----------------------------------------------------------------------
# CHECK 5u -- rust's harness refusals, repaired rather than recorded.
#
# Rust's recorder is a TRAIT, `DB`, and not a function over a dynamic
# value.  A type with no `impl DB` cannot be recorded at all, and rustc
# refuses the probe with a message naming the recorder's own method
# `db`.  Log 037 counted 4 such refusals apart and repaired none.
#
# Reading the four messages rather than guessing at them shows they are
# TWO different things:
#
#   `Kbinding.assign_19` and `Kbinding.assign_21` say "the method `db`
#   exists for reference `&R3` / `&Node`, but its trait bounds were not
#   satisfied".  `R3` and `Node` are types the HOLDER's own declaration
#   text declares, inside the probe, so no impl in the shared recorder
#   can ever reach them.  These two are genuine harness refusals.
#
#   `Kaccess.subscript_17_14` and `_18_14` say "the trait bound
#   `String: Borrow<[i64]>` is not satisfied".  That names `Borrow`,
#   which is rust's own trait and not the recorder.  It is rust
#   refusing to index a `HashMap<String, _>` with a slice of whole
#   numbers, which is a FINDING about rust.  Log 037's classifier
#   matched the bare token "trait bound" and swept them in by mistake.
#
# The repair for the first two: a locally declared type gets a locally
# declared impl, appended to the declaration that declares it, encoding
# by `OPAQUE` -- which `answers_encoding.md` defines for exactly this
# case, "nothing better was available".  Harness machinery, surfaced
# here and reversible by deleting this function.
#
# The repair for the other two is in `l3_construct_read.py`: the
# classifier no longer matches a bare "trait bound".
RUST_LOCAL_TYPE = __import__("re").compile(
    r"\b(?:struct|enum)\s+([A-Za-z_]\w*)")
RUST_OPAQUE = (' impl DB for %s { fn db(&self) -> String {'
               ' format!("OPAQUE:{}", _hx(format!("{:?}", self)'
               '.as_bytes())) } }')


# A THIRD harness fault, found by the verification lane that proved the
# repair above and not by any run before it.  Four of rust's value-class
# declarations carry their own `use std::collections::BTreeMap;` inside
# the declaration text, and rust refuses a name imported twice in one
# scope: "error[E0252]: the name `BTreeMap` is defined multiple times".
# When both slots are filled from such a holder the probe scores REFUSE
# and it is the harness importing twice, not rust refusing the
# construct.  HARVEST_constructs.md already names this fault shape --
# "a duplicate import is a refusal" -- for go.  It is rust's too.
#
# Only rust carries an import inside a declaration; the other eight
# carry none *(measured)*.  So the remedy is rust-only: an import the
# LEFT declaration already made is dropped from the RIGHT one.
RUST_USE = __import__("re").compile(r"use\s+[^;]+;")


def drop_duplicate_uses(left, right):
    have = set(m.group(0) for m in RUST_USE.finditer(left))
    out = right
    for u in have:
        out = out.replace(u, "", 1) if u in out else out
    return out


def rust_local_impls(decl):
    """append an `impl DB` for every type this declaration declares."""
    out = decl
    for name in sorted(set(RUST_LOCAL_TYPE.findall(decl))):
        out += RUST_OPAQUE % name
    return out


# ----------------------------------------------------------------------
# the php recovery's fix, carried to the three languages that need it.
#
# Log 037 recovered php's twenty fatals by suffixing a declared class
# name per SLOT as well as per probe: when one probe's two slots are
# filled by two holders whose declaration text declares the SAME name,
# the second declaration redeclares the first.
#
# The same fault is present, unrecovered, in three of the nine, and the
# holder grain shows it: rust 8 rows, c++ 4 rows and swift 1 row score
# REFUSE with a redeclaration message.  Thirteen rows read as the
# language refusing the construct when they are the harness declaring a
# name twice.  At the value grain the same pairs recur once per value
# class pair, so the fault multiplies rather than staying at thirteen.
#
# The remedy is php's, unchanged in shape: only the RIGHT-hand slot's
# declaration is suffixed, so the left slot's type names read exactly
# as log 037 wrote them and only a collision is broken.
DECLARES = {
    "rust":   r"\b(?:struct|enum|union|trait)\s+([A-Za-z_]\w*)",
    "cpp":    r"\b(?:struct|class|enum|union)\s+([A-Za-z_]\w*)",
    "swift":  r"\b(?:struct|class|enum|protocol|actor)\s+([A-Za-z_]\w*)",
    "java":   r"\b(?:record|class|interface|enum)\s+([A-Za-z_]\w*)",
    "csharp": r"\b(?:record|class|interface|enum|struct)\s+([A-Za-z_]\w*)",
    "kotlin": r"\b(?:class|interface|enum|object)\s+([A-Za-z_]\w*)",
    "dart":   r"\b(?:class|mixin|enum|extension)\s+([A-Za-z_]\w*)",
    "typescript": r"\b(?:class|interface|enum)\s+([A-Za-z_]\w*)",
    "go":     r"\btype\s+([A-Za-z_]\w*)",
}


def side_suffix(lang, decl, suffix="_B"):
    """suffix every type name this declaration DECLARES, mechanically,
    by regular expression over the literal text."""
    import re as _re
    pat = DECLARES.get(lang)
    if not pat:
        return decl
    names = set(_re.findall(pat, decl))
    for n in sorted(names, key=len, reverse=True):
        decl = _re.sub(r"\b%s\b" % _re.escape(n), n + suffix, decl)
    return decl


def whole_index(hs):
    return next((n for n, h in enumerate(hs) if h["form"] == "whole"), None)


def bound_classes(hs):
    """decision 6 -- slice bounds come from the canonical whole-number
    holder only, capped at six value classes."""
    wi = whole_index(hs)
    if wi is None:
        return None, []
    return wi, sorted(hs[wi]["values"])[:WHOLE_BOUNDS]


def gen_value(lang):
    """[(pid, cons, holder_list, decls, body)] at the FULL value grain."""
    hs, _ = holders(lang)
    sp = space(lang)
    present = [r["construct"] for r in sp["constructs"] if r["present"]]
    na = (L.NOT_APPLICABLE.get(lang, {}) if lang != "go"
          else G.NOT_APPLICABLE)
    scaf = L.SCAF[lang] if lang != "go" else G.SCAF
    wi, bcs = bound_classes(hs)
    out = []
    for cons in present:
        if cons in na or cons in NO_SLOT or cons not in scaf:
            continue
        sc = scaf[cons]
        three = cons == "access.slice"
        two = cons in TWO
        for i, ha in enumerate(hs):
            for x in sorted(ha["values"]):
                da = rename(ha["values"][x], "a")
                if lang == "rust":
                    da = rust_local_impls(da)
                if three:
                    if wi is None:
                        continue
                    for b1 in bcs:
                        for b2 in bcs:
                            db = rename(hs[wi]["values"][b1], "b")
                            dc = rename(hs[wi]["values"][b2], "c")
                            pid = "K%s_%d_%s_%s_%s" % (cons, i, x, b1, b2)
                            out.append((pid, cons, [ha, hs[wi]],
                                        [da, db, dc], sc))
                    continue
                if not two:
                    pid = "K%s_%d_%s" % (cons, i, x)
                    out.append((pid, cons, [ha], [da], sc))
                    continue
                for j, hb in enumerate(hs):
                    for y in sorted(hb["values"]):
                        db = rename(side_suffix(lang, hb["values"][y]), "b")
                        if lang == "rust":
                            db = drop_duplicate_uses(da, db)
                            db = rust_local_impls(db)
                        ops = AUG_OPS if cons == "binding.augassign" else [""]
                        for op in ops:
                            body = sc.replace("{OP}", op)
                            pid = "K%s%s_%d_%d_%s_%s" % (cons, op, i, j, x, y)
                            out.append((pid, cons, [ha, hb], [da, db], body))
    return out


# ----------------------------------------------------------------------
# the eight that run through l3_construct_lang's lane machinery
# ----------------------------------------------------------------------
def emit_lang(lang, shard, nsh, probes):
    tag = "%s_%02d" % (lang, shard)
    rows = []
    for pid, cons, hl, decls, body in probes:
        used = "".join(decls) + body
        rows.append(dict(id=pid, cons=cons,
                         pres=L.pres_for(lang, hl, used),
                         decls=decls, body=body))
    jl = "\n".join(json.dumps(r) for r in rows)
    drv = (L.DRV.replace("{SRCGEN}", L.SRCGEN)
                .replace("{LANG}", lang)
                .replace("{EXT}", L.EXT[lang])
                .replace("{CH}", str(L.CHUNK[lang]))
                .replace("{ROUTE}", L.ROUTE[lang])
                .replace("{AMODE}", L.AMODE[lang]))
    # the raw files are per SHARD, so two shards never overwrite each
    # other, and the stage-B time cap leaves the daemon's 3600 s kill
    # a margin rather than racing it.
    drv = (drv.replace('/out/kx_%s.txt' % lang, '/out/%sx_%s.txt' % (RAWP, tag))
              .replace('/out/ky_%s.txt' % lang, '/out/%sy_%s.txt' % (RAWP, tag))
              .replace('/out/ky_%s.compilefail' % lang,
                       '/out/%sy_%s.compilefail' % (RAWP, tag))
              .replace("CAP = 3000.0", "CAP = 1500.0"))
    aux = ""
    if lang in L.AUXDRV:
        aux = ("base64 -d <<'B64_EOF' | gunzip > \"$ROOT/aux.txt\"\n%s\n"
               "B64_EOF" % L.gz64(L.AUXDRV[lang]))
    sh = L.LANE % dict(LANG=lang, N=len(rows), CH=L.CHUNK[lang],
                       ROUTE=L.ROUTE[lang], PROBES=L.gz64(jl),
                       RT=L.gz64(L.RT[lang]), TR=L.gz64(L.TRACE[lang]),
                       AUX=aux, DRV=L.gz64(drv))
    sh = sh.replace("ROOT=/work/kx_%s" % lang, "ROOT=/work/%s_%s" % (PFX, tag))
    sh += CLEANUP
    p = os.path.join(LANES, "%s_%s.sh" % (PFX, tag))
    open(p, "w").write(sh)
    os.chmod(p, 0o755)
    return p


# ----------------------------------------------------------------------
# go, which has its own simpler driver: build AND run, one file each
# ----------------------------------------------------------------------
def emit_go(shard, nsh, probes):
    tag = "go_%02d" % shard
    srcs = []
    for pid, cons, hl, decls, body in probes:
        pre = G.go_pre(hl, "".join(decls) + body)
        imps = [l for l in pre.splitlines() if l.strip()]
        srcs.append((pid, G.probe_src(cons, decls, body, pid, imps)))
    jl = "\n".join(json.dumps(dict(id=a, src=b)) for a, b in srcs)
    drv = G.DRV.replace('/out/kg_go.txt', '/out/%sg_%s.txt' % (RAWP, tag))
    # A FOURTH harness fault, and this one voided a run before it was
    # caught.  go's driver builds each probe into its own directory and
    # KEEPS the binary.  At log 037's 1,710 probes that cost 255 MB and
    # nobody noticed.  At 39,104 it filled the 4 GB /work part way
    # through, and from there `go build` failed with "write /work/...:
    # no space left" -- which the driver recorded as the probe being
    # REFUSED.  1,031 rows of go's first value run say that *(measured)*.
    #
    # The rows were written, so the completeness gate read COMPLETE.
    # That is the sharpest form of "exit 0 is not evidence" this node
    # has hit: the gate counts rows and cannot tell a refusal from a
    # full disk.  A message check now sits beside the gate, and the
    # driver deletes each probe's directory as soon as it has read the
    # result.
    drv = drv.replace(
        "import json, os, subprocess, sys, time",
        "import json, os, shutil, subprocess, sys, time")
    drv = drv.replace(
        "    done[0] += 1\n",
        "    shutil.rmtree(d, ignore_errors=True)\n    done[0] += 1\n")
    assert "shutil.rmtree(d" in drv and "os, shutil," in drv
    # go's lane gzips its probe file and does NOT gzip its driver.
    sh = G.LANE % dict(N=len(srcs), PROBES=L.gz64(jl), DRV=L.b64(drv))
    sh = sh.replace("ROOT=/work/kag", "ROOT=/work/%sg_%02d" % (PFX, shard))
    sh += CLEANUP
    p = os.path.join(LANES, "%s_%s.sh" % (PFX, tag))
    open(p, "w").write(sh)
    os.chmod(p, 0o755)
    return p


def freeze(lang, shard, nsh, probes, lo, hi, total):
    hs, _ = holders(lang)
    per = {}
    for p in probes:
        per[p[1]] = per.get(p[1], 0) + 1
    mp = os.path.join(HERE, "manifest_value_%s_%02d.json" % (lang, shard))
    json.dump(dict(language=lang, grain="value", frozen="2026-08-19",
                   design="construct_design.md",
                   log="log_038",
                   shard=shard, shards=nsh,
                   probe_range=[lo, hi], language_total=total,
                   route_acceptance=(L.ROUTE.get(lang)
                                     or "A2 `go build` per file"),
                   holders=[dict(i=n, form=h["form"], rep=h["rep"],
                                 value_classes=sorted(h["values"]))
                            for n, h in enumerate(hs)],
                   not_applicable=(L.NOT_APPLICABLE.get(lang, {})
                                   if lang != "go" else G.NOT_APPLICABLE),
                   constructs_probed=per,
                   scaffolds=(L.SCAF[lang] if lang != "go" else G.SCAF),
                   aug_ops=AUG_OPS,
                   no_slot_constructs_excluded=list(NO_SLOT),
                   slice_bound_classes=bound_classes(hs)[1],
                   probes=len(probes)),
              open(mp, "w"), indent=1)
    return mp


def main():
    which = [a for a in sys.argv[1:] if not a.startswith("-")] or NINE
    cap = int(os.environ.get("VALUE_CAP", "0"))
    if cap:
        globals()["PFX"], globals()["RAWP"] = "kw", "w"
        print("  SMOKE run: cap %d per language, lanes kw_*, "
              "raw w*_ -- never a measured run" % cap)
    print("layer-3 CONSTRUCTS at the VALUE grain -- derived counts,")
    print("printed before anything runs.")
    print("")
    print("  language     probes   shards   design answers col")
    tot = 0
    for lang in which:
        ps = gen_value(lang)
        sp = space(lang)
        design = sp["answer_probes"]
        if cap:
            # a SMOKE subset: a spread across every construct, so a cheap
            # run proves the value-grain scaffolds compile before the
            # full lane pays for them.  NEVER a measured run.
            byc = {}
            for p in ps:
                byc.setdefault(p[1], []).append(p)
            ps = []
            for c in sorted(byc):
                xs = byc[c]
                step = max(1, len(xs) // max(1, cap // max(1, len(byc))))
                ps += xs[::step][:cap]
        n = len(ps)
        tot += n
        sz = cap if cap else SHARD[lang]
        shards = [ps[i:i + sz] for i in range(0, n, sz)]
        print("  %-11s %7d %8d   %7d" % (lang, n, len(shards), design))
        for si, sub in enumerate(shards):
            lo = si * sz
            p = (emit_go(si, len(shards), sub) if lang == "go"
                 else emit_lang(lang, si, len(shards), sub))
            freeze(lang, si, len(shards), sub, lo, lo + len(sub), n)
            print("      shard %02d  %6d probes  ->  %s"
                  % (si, len(sub), os.path.basename(p)))
    print("")
    print("  TOTAL %d value-grain probes over %d languages"
          % (tot, len(which)))


if __name__ == "__main__":
    main()
