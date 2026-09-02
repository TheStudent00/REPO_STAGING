#!/usr/bin/env python3
"""timing_read.py -- read the tm_* lanes and cost out brute force.

Three things, in order.

1. MEASURED. Per language, mean and standard deviation of the wall clock a
   single probe costs in its own file and its own process: compile step and
   run step separately, then combined; and the same split by whether the
   probe was ACCEPTED (both steps exited clean) or REFUSED (either step did
   not). The instrument's own cost -- two `date` forks per timed step, which
   each lane measures for itself -- is subtracted.

2. DERIVED. Python's probe count under the owner's ruling: full enumeration of
   ORDERED operand pairs in place of the 200 chosen by rule, with and without
   the full value matrix in tier B. Computed by re-running the real generator
   with those two rules replaced, so it is arithmetic on the generator, not
   an estimate.

3. ESTIMATE. Every other language's count, scaled from python by its phase-0
   probe space (R2 count, which carries the kinds and the menu tokens) and by
   the square of its layer-2 atom count (which carries the operand pairs).
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DR = os.path.join(os.path.dirname(HERE), "data_representation")

ORDER = ["python", "ruby", "php", "typescript", "dart", "go", "java",
         "csharp", "rust", "cpp", "swift", "kotlin"]
COMPILED = {"typescript", "java", "csharp", "go", "rust", "cpp", "swift",
            "kotlin"}


def stats(xs):
    if not xs:
        return (0.0, 0.0)
    m = sum(xs) / len(xs)
    if len(xs) < 2:
        return (m, 0.0)
    v = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return (m, math.sqrt(v))


def read_lane(lang):
    path = os.path.join(HERE, "raw", "tm_%s.txt" % lang)
    rows, gap, batch = [], 0, None
    for line in open(path):
        b = line.strip().split("|")
        if len(b) != 6:
            continue
        if b[0] == "__GAP__":
            gap = int(b[3])
            continue
        if b[0].startswith("__BATCH"):
            batch = {"n": int(b[0].strip("_").replace("BATCH", "")),
                     "compile_ns": int(b[3]), "run_ns": int(b[5]),
                     "compile_rc": int(b[2]), "run_rc": int(b[4])}
            continue
        rows.append({"id": b[0], "predicted": b[1], "crc": int(b[2]),
                     "cns": int(b[3]), "rrc": int(b[4]), "rns": int(b[5])})
    for r in rows:                       # take the instrument out
        r["cns"] = max(0, r["cns"] - gap) if r["cns"] else 0
        r["rns"] = max(0, r["rns"] - gap) if r["rns"] else 0
        r["total"] = r["cns"] + r["rns"]
        r["accepted"] = (r["crc"] == 0 and r["rrc"] == 0)
    if batch:
        batch["compile_ns"] = max(0, batch["compile_ns"] - gap)
        batch["run_ns"] = max(0, batch["run_ns"] - gap)
    return rows, gap, batch


def ms(ns):
    return ns / 1e6


# ------------------------------------------------------ python, DERIVED count

def python_full_counts():
    """Re-run the real generator with (a) full ordered pair enumeration and
    (b) optionally the full value matrix in tier B, and count what falls out."""
    import probe_generate as pg

    atoms = pg.build_atoms()
    base_singles, base_pairs, why, base, by_id = pg.operand_sets(atoms)

    def patched(full_tier_b):
        def operand_sets(a):
            singles = list(a)
            pairs = [(x, y) for x in a for y in a]
            w = {(x["id"], y["id"]): "full-enumeration" for x, y in pairs}
            if full_tier_b:
                b = {(t["form"], t["rep"], t["cls"]): t for t in a}
            else:
                b = base
            return singles, pairs, w, b, {t["id"]: t for t in a}
        return operand_sets

    out = {}
    for name, full_b in (("pairs_only", False), ("pairs_and_values", True)):
        saved = pg.operand_sets
        pg.operand_sets = patched(full_b)
        try:
            _a, probes, pairs, _w = pg.generate()
        finally:
            pg.operand_sets = saved
        out[name] = {"probes": len(probes), "pairs": len(pairs),
                     "atoms": len(atoms)}
    out["as_run"] = {"probes": 20024, "pairs": len(base_pairs),
                     "atoms": len(atoms)}
    return out


# --------------------------------------------------- per-language scale terms

def atom_count(lang):
    """Layer-2 (cell, value class) entries that LOADED -- the operand pool the
    full value matrix would draw on."""
    path = os.path.join(DR, "audit", "audit_%s.json" % lang)
    if not os.path.exists(path):
        return None
    d = json.load(open(path))
    n = 0
    for cell in d["cells"]:
        if cell["verdict"] not in ("LOADS", "PARTIAL"):
            continue
        for _cls, probe in cell["probes"].items():
            if probe["judgement"] != "refused":
                n += 1
    return n


def holder_count(lang):
    d = json.load(open(os.path.join(DR, "representations_%s.json" % lang)))
    return sum(len(v) for v in d["forms"].values())


def r2_count(lang):
    d = json.load(open(os.path.join(HERE, "probe_space.json")))
    return d[lang]["counts"]["probes_R2"]


def main():
    full = python_full_counts()
    py_atoms = full["as_run"]["atoms"]
    py_full = full["pairs_and_values"]["probes"]
    py_r2 = r2_count("python")

    report = {"python_derived": full, "languages": {}}
    for lang in ORDER:
        rows, gap, batch = read_lane(lang)
        acc = [r for r in rows if r["accepted"]]
        ref = [r for r in rows if not r["accepted"]]
        cm, cs = stats([r["cns"] for r in rows])
        rm, rs = stats([r["rns"] for r in rows])
        tm, ts = stats([r["total"] for r in rows])
        am, _ = stats([r["total"] for r in acc])
        fm, _ = stats([r["total"] for r in ref])
        na, nh, nr2 = atom_count(lang), holder_count(lang), r2_count(lang)
        if lang == "python":
            count, level = py_full, "DERIVED"
        else:
            count = int(round(py_full * (nr2 / py_r2) * (na / py_atoms) ** 2))
            level = "ESTIMATE"
        per_batch = ((batch["compile_ns"] + batch["run_ns"]) / batch["n"]
                     if batch else None)
        report["languages"][lang] = {
            "N": len(rows), "gap_ns": gap,
            "compile_mean_ms": ms(cm), "compile_sd_ms": ms(cs),
            "run_mean_ms": ms(rm), "run_sd_ms": ms(rs),
            "total_mean_ms": ms(tm), "total_sd_ms": ms(ts),
            "n_accept": len(acc), "n_refuse": len(ref),
            "accept_mean_ms": ms(am), "refuse_mean_ms": ms(fm),
            "atoms": na, "holders": nh, "r2": nr2,
            "count": count, "count_level": level,
            "worst_case_hours": count * tm / 1e9 / 3600,
            "batch_n": batch["n"] if batch else None,
            "batch_compile_ms": ms(batch["compile_ns"]) if batch else None,
            "batch_run_ms": ms(batch["run_ns"]) if batch else None,
            "batch_per_probe_ms": ms(per_batch) if batch else None,
            "batched_hours": count * per_batch / 1e9 / 3600 if batch else None,
            "has_compile_step": lang in COMPILED,
        }
    with open(os.path.join(HERE, "timing_results.json"), "w") as h:
        json.dump(report, h, indent=1, sort_keys=True)

    print("python DERIVED: %s" % json.dumps(full))
    hdr = ("lang", "N", "compile", "run", "total", "acc", "ref", "atoms",
           "count", "worst h", "batch/probe", "batched h")
    print("%-11s %4s %10s %10s %10s %9s %9s %6s %12s %9s %11s %10s" % hdr)
    for lang in ORDER:
        r = report["languages"][lang]
        print("%-11s %4d %5.1f+-%4.1f %5.1f+-%4.1f %5.1f+-%4.1f "
              "%9.1f %9.1f %6d %12d %9.2f %11.2f %10.2f"
              % (lang, r["N"], r["compile_mean_ms"], r["compile_sd_ms"],
                 r["run_mean_ms"], r["run_sd_ms"], r["total_mean_ms"],
                 r["total_sd_ms"], r["accept_mean_ms"], r["refuse_mean_ms"],
                 r["atoms"], r["count"], r["worst_case_hours"],
                 r["batch_per_probe_ms"], r["batched_hours"]))


if __name__ == "__main__":
    main()
