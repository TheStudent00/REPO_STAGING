#!/usr/bin/env python3
"""l3_cart_full.py -- FULL GRIDS by construction: re-fold matrices_cart/
into matrices_full/ under the owner's ruling of 2026-08-21 (log 054).

NO PROBE IS RUN.  matrices_cart/ recorded absence as a shorter row (its
index.json absence_rule: a value a holder cannot represent is simply
ABSENT from that holder's x_set).  The ruling replaces absence with a
distinct STATIC outcome token:

    UNREPRESENTABLE -- the holder cannot represent this operand, known
    statically, zero machine cost.  It is NOT a decline (the language
    was never asked); it is its own cell class.

Every profile of a form pair and level is inflated to the FULL X set of
its form and level -- the form-level sets already recorded in
matrices_cart/index.json (the entries with n_absent == 0):

    truth       L1 6    L2 6
    whole       L1 17   L2 10
    fractional  L1 16   L2 10

so every profile of one (form_pair, level) carries the SAME key set,
always.  A cell whose key involves an operand the holder cannot
represent is filled with UNREPRESENTABLE; every other cell is copied
byte-for-byte from matrices_cart/ through the probe-index rule applied
verbatim:

    level 1   p = i0 * |Xb| + i1
    level 2   p = ((i0*|Xb| + i1)*|Xa| + i2)*|Xb| + i3

matrices_cart/ is NOT touched -- it stays on disk unchanged as the audit
trail of the measured run (log 052).

COLUMNS.  The matrices_cart pattern, kept, with three added columns
documented in matrices_full/index.json:

    probe_id, level, form_pair, lhs_holder, rhs_holder,
    x_set_a, x_set_b            (now the FULL form-level set ids),
    n_probes                    (the full grid size),
    output_canon_vector, n_values, n_declines,
    n_unrepresentable           (ADDED: the static fills in this row),
    src_x_set_a, src_x_set_b    (ADDED: the measured run's own set ids,
                                 so every cell traces to its source)

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree; the
OS-stopped outcome is ABORT.
"""

import csv
import json
import os
import sys
import time

csv.field_size_limit(sys.maxsize)

HERE = os.path.dirname(os.path.abspath(__file__))
CART = os.path.join(HERE, "matrices_cart")
OUT = os.path.join(HERE, "matrices_full")
SEP = ";"
UNREP = "UNREPRESENTABLE"

COLUMNS = ["probe_id", "level", "form_pair", "lhs_holder", "rhs_holder",
           "x_set_a", "x_set_b", "n_probes", "output_canon_vector",
           "n_values", "n_declines", "n_unrepresentable",
           "src_x_set_a", "src_x_set_b"]


def is_decline(c):
    return c == "REFUSE" or c == "ABORT" or c.startswith("RAISE:")


def full_sets(xs):
    """the FULL X set per (form, level): the recorded set with no absent
    spelling.  Asserted unique, and asserted to be the superset of every
    other set of its form and level."""
    full = {}
    for sid, v in xs.items():
        if v["n_absent"] == 0:
            k = (v["form"], v["level"])
            assert k not in full or full[k] == sid, (
                "two full sets for %s" % (k,))
            full[k] = sid
    for sid, v in xs.items():
        k = (v["form"], v["level"])
        assert k in full, "no full set for %s" % (k,)
        fs = xs[full[k]]
        assert set(v["spellings"]) | set(v["absent_spellings"]) == \
            set(fs["spellings"]), (
            "set %s + its absences is not the full set %s" % (sid, full[k]))
        assert set(v["spellings"]) <= set(fs["spellings"])
    return full


def map_positions(xs, full, level, sa, sb):
    """full-grid position -> source position, or -1 for UNREPRESENTABLE.
    Returns a plain list of length |XaF|*|XbF| (level 1) or its square
    (level 2), following the probe-index rule verbatim."""
    fa = xs[full[(xs[sa]["form"], level)]]["spellings"]
    fb = xs[full[(xs[sb]["form"], level)]]["spellings"]
    pa = {s: i for i, s in enumerate(xs[sa]["spellings"])}
    pb = {s: i for i, s in enumerate(xs[sb]["spellings"])}
    na, nb = len(pa), len(pb)
    # level-1 map over the full (I0, I1) grid
    q = []
    for s0 in fa:
        i0 = pa.get(s0, -1)
        for s1 in fb:
            i1 = pb.get(s1, -1)
            q.append(-1 if (i0 < 0 or i1 < 0) else i0 * nb + i1)
    if level == 1:
        return q
    # level 2 is the outer product of level 1 with itself:
    # P_full = Q01 * (|XaF|*|XbF|) + Q23  maps to  p = q01*(na*nb) + q23
    block = na * nb
    out = []
    for q01 in q:
        if q01 < 0:
            out.extend([-1] * len(q))
        else:
            base = q01 * block
            out.extend([-1 if q23 < 0 else base + q23 for q23 in q])
    return out


def main():
    print("FULL GRIDS -- re-fold matrices_cart/ into matrices_full/; the "
          "static token %s fills every cell a holder cannot represent.  "
          "NO probe is run and matrices_cart/ is not touched." % UNREP)
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    idx = json.load(open(os.path.join(CART, "index.json")))
    xs = idx["x_sets"]
    full = full_sets(xs)
    print("  full form-level sets: %s"
          % ", ".join("%s/L%d -> %s (n=%d)" % (f, l, sid, xs[sid]["n"])
                      for (f, l), sid in sorted(full.items())))

    map_cache = {}
    out_index = {}
    tot = dict(rows=0, cells=0, unrep=0, values=0, declines=0,
               copied=0)
    for key in sorted(idx["matrices"]):
        meta = idx["matrices"][key]
        rows_out = []
        p = os.path.join(CART, meta["file"])
        for r in csv.DictReader(open(p)):
            level = int(r["level"])
            sa, sb = r["x_set_a"], r["x_set_b"]
            mk = (level, sa, sb)
            mp = map_cache.get(mk)
            if mp is None:
                mp = map_cache[mk] = map_positions(xs, full, level, sa, sb)
            src = r["output_canon_vector"].split(SEP)
            assert len(src) == int(r["n_probes"])
            vec = [UNREP if q < 0 else src[q] for q in mp]
            n_unrep = sum(1 for q in mp if q < 0)
            n_decl = sum(1 for c in vec if is_decline(c))
            n_val = len(vec) - n_unrep - n_decl
            fa = full[(xs[sa]["form"], level)]
            fb = full[(xs[sb]["form"], level)]
            rows_out.append({
                "probe_id": r["probe_id"], "level": level,
                "form_pair": r["form_pair"],
                "lhs_holder": r["lhs_holder"],
                "rhs_holder": r["rhs_holder"],
                "x_set_a": fa, "x_set_b": fb, "n_probes": len(vec),
                "output_canon_vector": SEP.join(vec),
                "n_values": n_val, "n_declines": n_decl,
                "n_unrepresentable": n_unrep,
                "src_x_set_a": sa, "src_x_set_b": sb})
            tot["rows"] += 1
            tot["cells"] += len(vec)
            tot["unrep"] += n_unrep
            tot["values"] += n_val
            tot["declines"] += n_decl
            tot["copied"] += len(src)
            # every measured cell must appear exactly once in the full grid
            assert len(vec) - n_unrep == len(src), (key, r["probe_id"])
        fn = meta["file"]
        with open(os.path.join(OUT, fn), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLUMNS)
            w.writeheader()
            for rr in rows_out:
                w.writerow(rr)
        out_index[key] = dict(
            file=fn, language=meta["language"], operator=meta["operator"],
            level=meta["level"], rows=len(rows_out),
            cells=sum(rr["n_probes"] for rr in rows_out),
            n_values=sum(rr["n_values"] for rr in rows_out),
            n_declines=sum(rr["n_declines"] for rr in rows_out),
            n_unrepresentable=sum(rr["n_unrepresentable"]
                                  for rr in rows_out))
    print("  %d rows re-folded; %d cells in the full grids; %d measured "
          "cells copied byte-for-byte; %d cells filled %s statically; "
          "%d value cells, %d decline cells  (%.1f s)"
          % (tot["rows"], tot["cells"], tot["copied"], tot["unrep"], UNREP,
             tot["values"], tot["declines"], time.time() - t0))
    assert tot["copied"] + tot["unrep"] == tot["cells"]

    # ---- format verification, the l3_cart_read pattern
    files = sorted(f for f in os.listdir(OUT) if f.endswith(".csv"))
    ncols_bad = veclen_bad = empty_slot = rows = cells = 0
    gridsize = {}
    for fn in files:
        pth = os.path.join(OUT, fn)
        for line in csv.reader(open(pth)):
            if len(line) != len(COLUMNS):
                ncols_bad += 1
        for r in csv.DictReader(open(pth)):
            rows += 1
            n = int(r["n_probes"])
            cells += n
            v = r["output_canon_vector"].split(SEP)
            if len(v) != n:
                veclen_bad += 1
            if any(c == "" for c in v):
                empty_slot += 1
            k = (r["form_pair"], r["level"])
            assert gridsize.setdefault(k, n) == n, (
                "two grid sizes inside one (form_pair, level)")
    print("  FORMAT: %d files, %d rows, %d cells; non-rectangular lines "
          "%d; wrong vector lengths %d; empty slots %d; ONE grid size per "
          "(form_pair, level) across all %d of them"
          % (len(files), rows, cells, ncols_bad, veclen_bad, empty_slot,
             len(gridsize)))
    assert ncols_bad == veclen_bad == empty_slot == 0

    json.dump(dict(
        status="FULL GRIDS -- the owner's ruling of 2026-08-21 (log 054).  "
               "Every profile is inflated to the FULL X set of its form "
               "and level; a cell whose key involves an operand the "
               "holder cannot represent carries the static token "
               "UNREPRESENTABLE.  Assembly over matrices_cart/ -- no "
               "probe was run, and matrices_cart/ is unchanged on disk "
               "as the audit trail.",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        scope=idx["scope"],
        columns=COLUMNS, vector_separator=SEP,
        probe_index_rule=idx["probe_index_rule"],
        comparability="every profile of one (form_pair, level) carries "
                      "the SAME key set by construction, so profiles "
                      "compare position by position inside their "
                      "compatibility gate with no alignment step and no "
                      "partial overlap",
        unrepresentable_rule="a value a holder cannot represent fills "
                             "its cell with the distinct outcome token "
                             "UNREPRESENTABLE -- statically, zero "
                             "probes.  It is NOT a decline: the "
                             "language was never asked.  Whether it is "
                             "scored is the scoring's choice, recorded "
                             "on the scoring, never destroyed here.",
        added_columns=dict(
            n_unrepresentable="count of static UNREPRESENTABLE fills in "
                              "this row",
            src_x_set_a="the measured run's own lhs operand-set id in "
                        "matrices_cart/, so every cell traces to its "
                        "source",
            src_x_set_b="same for rhs"),
        full_sets={"%s/L%d" % k: sid for k, sid in sorted(full.items())},
        x_sets=xs,
        totals=tot,
        grid_sizes={"%s/L%s" % k: n for k, n in sorted(gridsize.items())},
        vocabulary=idx["vocabulary"],
        matrices=out_index),
        open(os.path.join(OUT, "index.json"), "w"), indent=1)

    with open(os.path.join(OUT, "README.md"), "w") as f:
        f.write(
            "# full-grid matrices\n\n"
            "the owner's ruling of 2026-08-21 (log 054): every profile is "
            "inflated to the FULL X set of its form and level, so every "
            "profile of one (form_pair, level) carries the SAME key set, "
            "always.  A cell whose key involves an operand the holder "
            "cannot represent carries the distinct static token "
            "`UNREPRESENTABLE` -- no probe was run for it, none was "
            "needed, and it is NOT a decline (the language was never "
            "asked).\n\n"
            "Assembly over `matrices_cart/` through the probe-index rule "
            "applied verbatim (level 1 `p = i0*|Xb| + i1`, level 2 "
            "`p = ((i0*|Xb| + i1)*|Xa| + i2)*|Xb| + i3`); every measured "
            "cell is copied byte-for-byte and `matrices_cart/` stays on "
            "disk unchanged for the audit.\n\n"
            "Columns are the matrices_cart pattern plus three: "
            "`n_unrepresentable` (the static fills in the row) and "
            "`src_x_set_a` / `src_x_set_b` (the measured run's own set "
            "ids, so every cell traces to its source).  `x_set_a` / "
            "`x_set_b` now name the FULL form-level sets recorded in "
            "`index.json`.\n")
    print("  wrote %s (%d matrices, %.1f s)"
          % (OUT, len(out_index), time.time() - t0))


if __name__ == "__main__":
    main()
