#!/usr/bin/env python3
"""l3_interval_c_read.py -- fold the ruling-C lanes into ADDITIONAL
interval rows: `matrices_interval_c/<lang>.<op>.csv`.

Same ten columns as `matrices_interval/`, same canon rules, same vector
separator.  The diagonal rows are NOT overwritten -- `matrices_interval/`
is not opened for writing anywhere in this file, and the log-049/050
products stand exactly as they were.  The two directories are read
TOGETHER by `l3_row_graph_v2.py`.

Two new interval_id spellings mark the variants (ruling C):

  `IV32:<a>|<b>:shift`   C1.  lhs sample k against rhs sample
                         (k+1) mod 32.  No new values: the ladder
                         already carries every point, only the pairing
                         moved.  So lhs_canon_vector is the ladder in
                         order and rhs_canon_vector is the ladder
                         rotated by one.

  `IV32:<a>|<b>:comp1`   C2.  `op(op(x_k, x_k'), op(x_k, x_k'))`.  The
                         composed operands are the operator's OWN
                         diagonal outputs, so lhs_canon_vector and
                         rhs_canon_vector are BOTH the diagonal row's
                         output_canon_vector, read out of
                         `matrices_interval/`.  That is what makes a
                         comp1 row comparable to another comp1 row: two
                         operators compose over the same operands only
                         when their diagonal outputs coincide.

  On a comp1 row `lhs_holder` and `rhs_holder` still name the holders of
  the SOURCE operands x, so the row can be traced back to the diagonal
  row it composes; the composed operands themselves are in the two input
  vectors, where the scoring reads them.

Where an operand of the composition DECLINED, the composed probe was not
run and the position carries a decline token -- so ruling B excludes it
from every comparison, in the numerator and the denominator both.  The
reader cross-checks that claim against the diagonal rows and prints the
count rather than asserting it silently.

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
sys.path.insert(0, HERE)

IV_DIR = os.path.join(HERE, "matrices_interval")          # READ ONLY here
OUT_DIR = os.path.join(HERE, "matrices_interval_c")
LANE_OUT = os.path.abspath(os.path.join(HERE, "..", "..", "..",
                                        "SandboxDesign", "agent", "out"))
RAW = os.path.join(HERE, "raw")

import l3_per_op_matrices as m                              # noqa: E402
import l3_per_op_matrices_v2 as v2                          # noqa: E402
import l3_interval_values as IV                             # noqa: E402
import l3_interval_gen as G                                 # noqa: E402
import l3_interval_read as IR                               # noqa: E402
import l3_interval_c as C                                   # noqa: E402

COLUMNS = IR.COLUMNS
SEP = IR.SEP
N = IV.N_SAMPLES


def find_lane(name):
    for d in (LANE_OUT, RAW):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    raise SystemExit("lane output not found: %s (looked in %s, %s)"
                     % (name, LANE_OUT, RAW))


# ------------------------------------------------------------------
# lane output -> {probe id: canon-or-token}
# ------------------------------------------------------------------

def read_rust():
    p = find_lane("iv_rust_c0.txt")
    out, summary, timing = {}, None, None
    for line in open(p):
        line = line.rstrip("\n")
        if line.startswith("__SUMMARY__"):
            summary = line
            continue
        if line.startswith("__TIMING__"):
            timing = line
            continue
        pid, _, rest = line.partition("|")
        if not pid:
            continue
        if rest.startswith("-|RAISE:"):
            out[pid] = "RAISE:" + v2.norm_kind(rest[len("-|RAISE:"):])
        elif rest.startswith("-|ABORT"):
            out[pid] = "ABORT"
        elif rest.startswith("-|BUILDFAIL"):
            out[pid] = "REFUSE"
        elif rest.startswith("-|MISSING"):
            out[pid] = "ABORT"
        else:
            out[pid] = IR.rust_canon(rest)
    return out, summary, timing, p


def read_ruby():
    p = find_lane("iv_ruby_c0.txt")
    out, summary, timing = {}, None, None
    opdecl = set()
    for line in open(p):
        line = line.rstrip("\n")
        if line.startswith("__SUMMARY__"):
            summary = line
            continue
        if line.startswith("__TIMING__"):
            timing = line
            continue
        parts = line.split("|", 2)
        if len(parts) < 3:
            continue
        pid, kind, payload = parts
        if kind == "ANSWER":
            out[pid] = IR.ruby_canon(payload)
        elif kind == "RAISE":
            out[pid] = "RAISE:" + v2.norm_kind(payload)
        elif kind == "RAISEOP":
            # the OPERAND declined, so the composed probe was not run
            out[pid] = "RAISE:" + v2.norm_kind(payload)
            opdecl.add(pid)
        elif kind == "REFUSE":
            out[pid] = "REFUSE"
        elif kind == "REFUSEOP":
            out[pid] = "REFUSE"
            opdecl.add(pid)
        elif kind == "ABORT":
            out[pid] = "ABORT"
        else:
            out[pid] = "ABORT"
    return out, summary, timing, p, opdecl


# ------------------------------------------------------------------
# the diagonal rows, read (never written) for the comp1 operands
# ------------------------------------------------------------------

def diagonal_outputs(lang):
    """{probe_id V<k>_<i>_<j>: [32 output canon cells]}"""
    idx = json.load(open(os.path.join(IV_DIR, "index.json")))
    out = {}
    for key, meta in idx["matrices"].items():
        if not key.startswith(lang + "."):
            continue
        for r in csv.DictReader(open(os.path.join(IV_DIR, meta["file"]))):
            out[r["probe_id"]] = r["output_canon_vector"].split(SEP)
    return out


# ------------------------------------------------------------------
# row assembly
# ------------------------------------------------------------------

def build(lang, results, diag):
    tab = {t["i"]: t for t in G.numeric_table(lang)}
    op_list = G.ops(lang)
    if lang == "rust":
        shift_cells, comp_cells, _ = C.rust_plan()
    else:
        cells = [(op, i, j) for i in sorted(tab) for j in sorted(tab)
                 for op in op_list]
        shift_cells, comp_cells = cells, cells

    per = {}
    stats = dict(shift_rows=0, comp_rows=0, comp_operand_declines=0,
                 comp_positions_checked=0, comp_mismatch=0,
                 comp_missing_diagonal=0)

    for op, i, j in shift_cells:
        k = op_list.index(op)
        ha, hb = tab[i], tab[j]
        lidA, ruleA, sampA = IV.samples_for(lang, ha["form"], ha["holder"])
        lidB, ruleB, sampB = IV.samples_for(lang, hb["form"], hb["holder"])
        lvec, rvec, ovec = [], [], []
        for s in range(N):
            t = C.shift_index(s)
            lvec.append(IV.canon_sample(ruleA, sampA[s], v2.canon_num))
            rvec.append(IV.canon_sample(ruleB, sampB[t], v2.canon_num))
            ovec.append(results.get("S%d_%d_%d_%d" % (k, i, j, s), "ABORT"))
        per.setdefault(op, []).append(_row(
            "S%d_%d_%d" % (k, i, j), ha, hb,
            "IV%d:%s|%s:shift" % (N, lidA, lidB), lvec, rvec, ovec))
        stats["shift_rows"] += 1

    for op, i, j in comp_cells:
        k = op_list.index(op)
        ha, hb = tab[i], tab[j]
        lidA, _, _ = IV.samples_for(lang, ha["form"], ha["holder"])
        lidB, _, _ = IV.samples_for(lang, hb["form"], hb["holder"])
        dv = diag.get("V%d_%d_%d" % (k, i, j))
        if dv is None:
            stats["comp_missing_diagonal"] += 1
            continue
        ovec = [results.get("C%d_%d_%d_%d" % (k, i, j, s), "ABORT")
                for s in range(N)]
        # the operands ARE the diagonal outputs; a declined operand means
        # the composed probe was not run, and the position must therefore
        # carry a decline of its own.  Checked, not assumed.
        for s in range(N):
            stats["comp_positions_checked"] += 1
            if IR.is_decline(dv[s]):
                stats["comp_operand_declines"] += 1
                if not IR.is_decline(ovec[s]):
                    stats["comp_mismatch"] += 1
        per.setdefault(op, []).append(_row(
            "C%d_%d_%d" % (k, i, j), ha, hb,
            "IV%d:%s|%s:comp1" % (N, lidA, lidB), list(dv), list(dv), ovec))
        stats["comp_rows"] += 1

    return per, stats


def _row(pid, ha, hb, iv_id, lvec, rvec, ovec):
    nd = sum(1 for c in ovec if IR.is_decline(c))
    return {"probe_id": pid, "lhs_holder": ha["holder"],
            "rhs_holder": hb["holder"], "interval_id": iv_id,
            "n_samples": N,
            "lhs_canon_vector": SEP.join(lvec),
            "rhs_canon_vector": SEP.join(rvec),
            "output_canon_vector": SEP.join(ovec),
            "n_values": N - nd, "n_declines": nd}


# ------------------------------------------------------------------
# format verification -- the same ground log 049 section 4 checked
# ------------------------------------------------------------------

def verify(d):
    print("FORMAT VERIFICATION -- %s" % os.path.basename(d))
    files = sorted(f for f in os.listdir(d) if f.endswith(".csv"))
    ncols_bad = veclen_bad = empty_slot = dirty = rows = samples = 0
    ok_tokens = 0
    for fn in files:
        p = os.path.join(d, fn)
        for line in csv.reader(open(p)):
            if len(line) != len(COLUMNS):
                ncols_bad += 1
        for r in csv.DictReader(open(p)):
            rows += 1
            n = int(r["n_samples"])
            samples += n
            vs = [r["lhs_canon_vector"].split(SEP),
                  r["rhs_canon_vector"].split(SEP),
                  r["output_canon_vector"].split(SEP)]
            if any(len(v) != n for v in vs):
                veclen_bad += 1
            for v in vs:
                for cell in v:
                    if cell == "":
                        empty_slot += 1
                        continue
                    if cell.startswith("[") and ("/" in cell or "~" in cell):
                        dirty += 1
                    if cell in ("negzero", "inf", "-inf"):
                        dirty += 1
                    if "−" in cell:
                        dirty += 1
                    if IR.is_decline(cell):
                        ok_tokens += 1
    print("  files                        %d" % len(files))
    print("  rows                         %d" % rows)
    print("  samples inside those rows    %d" % samples)
    print("  non-rectangular lines        %d  (column count %d everywhere "
          "else)" % (ncols_bad, len(COLUMNS)))
    print("  rows with a wrong vector len %d" % veclen_bad)
    print("  empty vector slots           %d  (padding NOTHING)" % empty_slot)
    print("  dirty canon cells            %d" % dirty)
    print("  outcome tokens in vectors    %d" % ok_tokens)
    return dict(files=len(files), rows=rows, samples=samples,
                non_rectangular=ncols_bad, wrong_vector_len=veclen_bad,
                empty_slots=empty_slot, dirty_cells=dirty,
                outcome_tokens=ok_tokens)


# ------------------------------------------------------------------

def main():
    print("interval ruling-C matrices -- ADDITIONAL rows (C1 shifted, "
          "C2 one-level composition); matrices_interval/ is read, never "
          "written")
    os.makedirs(OUT_DIR, exist_ok=True)
    t0 = time.time()
    index, lane_timing = {}, {}
    for lang in ("rust", "ruby"):
        if lang == "rust":
            results, summary, timing, path = read_rust()
            opdecl = set()
        else:
            results, summary, timing, path, opdecl = read_ruby()
        print("  %s: %d sample results from %s" % (lang, len(results), path))
        if summary:
            print("      lane summary: %s" % summary)
        if timing:
            print("      lane timing:  %s" % timing)
            lane_timing[lang] = timing
        diag = diagonal_outputs(lang)
        per, stats = build(lang, results, diag)
        print("      %d shifted rows + %d composed rows; %d composed "
              "positions where the OPERAND declined so the composed probe "
              "was not run (%d of those disagree with the diagonal -- must "
              "be 0); %d composed cells had no diagonal row"
              % (stats["shift_rows"], stats["comp_rows"],
                 stats["comp_operand_declines"], stats["comp_mismatch"],
                 stats["comp_missing_diagonal"]))
        if opdecl:
            print("      ruby reported %d operand declines itself "
                  "(RAISEOP / REFUSEOP)" % len(opdecl))
        assert stats["comp_mismatch"] == 0, "composed probe ran on a " \
            "declined operand"
        for op, rows in sorted(per.items()):
            fn = "%s.%s.csv" % (lang, m.op_filename(op))
            with open(os.path.join(OUT_DIR, fn), "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=COLUMNS)
                w.writeheader()
                for r in rows:
                    w.writerow(r)
            index["%s.%s" % (lang, op)] = dict(
                file=fn, rows=len(rows), n_samples=N,
                samples=len(rows) * N,
                variants=sorted({r["interval_id"].rsplit(":", 1)[1]
                                 for r in rows}),
                holders=sorted({r["lhs_holder"] for r in rows}
                               | {r["rhs_holder"] for r in rows}),
                n_values=sum(r["n_values"] for r in rows),
                n_declines=sum(r["n_declines"] for r in rows))
        index.setdefault("_stats", {})[lang] = stats

    stats = verify(OUT_DIR)
    json.dump(dict(
        status="INTERVAL RULING-C MATRICES -- ADDITIONAL rows breaking "
               "the diagonal: C1 SHIFTED (x_k OP x_{(k+1) mod 32}) and "
               "C2 ONE-LEVEL COMPOSITION (op(op(x,x'), op(x,x'))).  The "
               "diagonal rows in matrices_interval/ are untouched.",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        pilot="rust (static) + ruby (route C) only; the other ten wait",
        columns=COLUMNS, vector_separator=SEP, n_samples=N,
        shift=C.SHIFT,
        comp1_operands="the operator's own diagonal outputs; a comp1 "
                       "row's lhs_canon_vector and rhs_canon_vector are "
                       "both the diagonal row's output_canon_vector, and "
                       "lhs_holder/rhs_holder still name the SOURCE "
                       "operand holders so the row traces back",
        lane_timing=lane_timing,
        oversized_cells_reconstructed_from_leading_bits=(
            IR.TOPBITS_USED["n"]),
        verification=stats,
        vocabulary="super-node / sub-node / co-node / sub-tree; the "
                   "OS-stopped outcome is ABORT",
        matrices={k: v for k, v in index.items() if k != "_stats"},
        build_stats=index.get("_stats", {})),
        open(os.path.join(OUT_DIR, "index.json"), "w"), indent=1)

    with open(os.path.join(OUT_DIR, "README.md"), "w") as f:
        f.write("# interval matrices -- ruling C (breaking the diagonal)"
                "\n\nADDITIONAL rows on top of `../matrices_interval/`, "
                "which is not modified.  Same ten columns, same canon "
                "rules, same `%s` vector separator.\n\n"
                "- `IV%d:<a>|<b>:shift` -- C1, `x_k OP x_{(k+%d) mod %d}`."
                "  No new values; the pairing moved.\n"
                "- `IV%d:<a>|<b>:comp1` -- C2, "
                "`op(op(x,x'), op(x,x'))`.  The composed operands are the "
                "operator's own diagonal outputs and appear in the two "
                "input vectors; `lhs_holder`/`rhs_holder` still name the "
                "SOURCE operand holders.\n\n"
                "A position whose composed OPERAND declined was not run "
                "and carries a decline token, so ruling B excludes it "
                "from every comparison.\n"
                % (SEP, N, C.SHIFT, N, N))
    print("  wrote %s (%d matrices, %.1f s)"
          % (OUT_DIR, len([k for k in index if k != "_stats"]),
             time.time() - t0))


if __name__ == "__main__":
    main()
