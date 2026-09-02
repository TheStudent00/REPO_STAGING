#!/usr/bin/env python3
"""l3_manifest.py -- FREEZE the probe manifests.

Layer 3 phase 4, job 1.  A raw line is `P{i}_{j}_{x}_{y}_{k}|VERDICT|detail`
for the value matrix and `P{i}_{j}_{vca}_{vcb}_{op}|KIND|detail` for route C.
Those ids are POSITIONAL: they mean nothing without the holder list, the
value-class list and the operation list that the generator walked.  This
file writes that walk down, once, so a raw file stays decodable after the
generator changes, after the container is rebuilt, and after everyone who
remembers has stopped remembering.

the owner's condition is satisfied because the generator is DETERMINISTIC: the
manifest is a replay of `l3_matrix.matrix()` / `l3_routec`'s enumeration
loop.  No probe is run, no compiler is invoked, nothing is executed.  This
script is a pure read of `l3_accept.holders/ops` plus two nested loops.

It runs as an ORDINARY PROCESS, not as a lane.  Nothing is written into
the sandbox agent's `drop/`, so the running value-matrix shards are not
perturbed and nothing queues behind them.

Usage:
    python3 l3_manifest.py            # write every manifest + verify
    python3 l3_manifest.py --verify   # verify only, write no manifest
"""

import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
sys.path.insert(0, HERE)
from l3_accept import holders, ops, LANG            # noqa: E402
from l3_matrix import ORDER, MS, SHARD_SECONDS, SHARD_PROBES  # noqa: E402

ROUTE_C = ["python", "ruby", "php"]
FROZEN = "2026-08-18"


def bar(done, total, t0, what):
    el = time.time() - t0
    eta = (el / done * (total - done)) if done else 0.0
    sys.stdout.write("\r  [%d/%d] %s  elapsed %.1fs  ETA %.1fs   "
                     % (done, total, what, el, eta))
    sys.stdout.flush()


def holder_block(hs):
    """the holder table, with each value class's LITERAL declaration text.

    `x` in a probe id indexes this list's `value_classes`, which is sorted
    by class name -- exactly what l3_matrix.matrix() sorts by.
    """
    out = []
    for i, h in enumerate(hs):
        out.append(dict(i=i, form=h["form"], holder=h["rep"],
                        pre=h.get("pre", "") or "",
                        value_classes=[[k, h["values"][k]]
                                       for k in sorted(h["values"])]))
    return out


def shard_plan(lang, nrows):
    """replay l3_matrix.main()'s sharding arithmetic, exactly."""
    secs = nrows * MS[lang] / 1000.0
    n = max(1,
            int(secs / SHARD_SECONDS) + (1 if secs % SHARD_SECONDS else 0),
            (nrows + SHARD_PROBES - 1) // SHARD_PROBES)
    per = (nrows + n - 1) // n
    sh = []
    for s in range(n):
        lo, hi = s * per, min((s + 1) * per, nrows)
        if lo >= hi:
            continue
        sh.append(dict(shard=s, lane="vm_%s_%02d" % (lang, s),
                       row_first=lo, row_last=hi - 1, rows=hi - lo))
    return sh


DECODE_A = ("id = P{i}_{j}_{x}_{y}_{k}.  i and j index `holders` and are "
            "the LEFT and RIGHT operand holders, in that order.  x indexes "
            "holders[i].value_classes, y indexes holders[j].value_classes.  "
            "k indexes `operations`.  Both operand orders are enumerated "
            "separately; the operator is never assumed commutative.")
DECODE_C = ("id = P{i}_{j}_{vca}_{vcb}_{op}.  i and j index `holders`; vca "
            "and vcb are value-class NAMES, not indices; op is the "
            "operation spelled literally.  Value-class names and operation "
            "spellings can both contain underscores and spaces, so an id is "
            "decoded by MATCHING against this manifest's enumeration, never "
            "by splitting the string on underscores.")


def manifest_a(lang):
    hs, _ = holders(lang)
    os_ = ops(lang)
    rows = []
    for i, ha in enumerate(hs):
        na = len(sorted(ha["values"]))
        for j, hb in enumerate(hs):
            nb = len(sorted(hb["values"]))
            for x in range(na):
                for y in range(nb):
                    for k in range(len(os_)):
                        rows.append([i, j, x, y, k])
    return dict(kind="value_matrix_manifest", language=lang, route="A",
                frozen=FROZEN, generator="l3_matrix.py::matrix()",
                id_grammar="P{i}_{j}_{x}_{y}_{k}", decode=DECODE_A,
                operations=os_, holders=holder_block(hs),
                probes=len(rows), shards=shard_plan(lang, len(rows)),
                enumeration_order=("i outer, then j, then x, then y, then k "
                                   "innermost"),
                rows=rows)


def manifest_c(lang):
    hs, _ = holders(lang)
    os_ = ops(lang)
    ids = []
    for i, ha in enumerate(hs):
        va = sorted(ha["values"])
        for j, hb in enumerate(hs):
            vb = sorted(hb["values"])
            for vca in va:
                for vcb in vb:
                    for op in os_:
                        ids.append([i, j, vca, vcb, op])
    return dict(kind="route_c_manifest", language=lang, route="C",
                frozen=FROZEN, generator="l3_routec.py",
                id_grammar="P{i}_{j}_{vca}_{vcb}_{op}", decode=DECODE_C,
                operations=os_, holders=holder_block(hs),
                probes=len(ids),
                enumeration_order=("i outer, then j, then value class of i, "
                                   "then value class of j, then operation"),
                rows=ids)


def expand(man, row):
    """one manifest row -> the full self-describing probe record."""
    if man["route"] == "A":
        i, j, x, y, k = row
        ha, hb = man["holders"][i], man["holders"][j]
        vca, da = ha["value_classes"][x]
        vcb, db = hb["value_classes"][y]
        op = man["operations"][k]
        pid = "P%d_%d_%d_%d_%d" % (i, j, x, y, k)
    else:
        i, j, vca, vcb, op = row
        ha, hb = man["holders"][i], man["holders"][j]
        da = dict(ha["value_classes"])[vca]
        db = dict(hb["value_classes"])[vcb]
        pid = "P%d_%d_%s_%s_%s" % (i, j, vca, vcb, op)
    return pid, dict(operation=op,
                     lhs=dict(form=ha["form"], holder=ha["holder"],
                              value_class=vca, value=da),
                     rhs=dict(form=hb["form"], holder=hb["holder"],
                              value_class=vcb, value=db))


# ---------------------------------------------------------------- verify

def read_raw(path):
    cells, summ = {}, None
    for line in open(path, errors="replace"):
        line = line.rstrip("\n")
        if line.startswith("__SUMMARY__"):
            summ = line.split("|")[1:]
            continue
        if not line.startswith("P"):
            continue
        f = line.split("|")
        cells[f[0]] = f[1]
    return cells, summ


def acceptance_grid(lang):
    for suf in ("A1", "A2"):
        p = os.path.join(HERE, "acceptance_%s_%s.json" % (lang, suf))
        if os.path.exists(p):
            d = json.load(open(p))
            return {k: v["verdict"] for k, v in d["cells"].items()}
    return None


def verify(man, rng):
    lang = man["language"]
    rep = dict(language=lang, route=man["route"], manifest_probes=man["probes"],
               shards=[], spot_checks=[], line_count_match=None)
    if man["route"] == "A":
        grid = acceptance_grid(lang)
        ok = True
        for sh in man["shards"]:
            p = os.path.join(RAW, sh["lane"] + ".txt")
            if not os.path.exists(p):
                rep["shards"].append(dict(lane=sh["lane"], state="IN FLIGHT",
                                          manifest_rows=sh["rows"]))
                continue
            cells, summ = read_raw(p)
            # a lane is FINISHED only if it printed __SUMMARY__.  A raw file
            # that exists without one is a lane still writing; its short line
            # count is progress, not a manifest fault.
            state = "LANDED" if summ else "IN FLIGHT (partial file)"
            match = len(cells) == sh["rows"]
            if summ:
                ok = ok and match
            rep["shards"].append(dict(lane=sh["lane"], state=state,
                                      manifest_rows=sh["rows"],
                                      raw_lines=len(cells),
                                      lines_match=match if summ else None,
                                      lane_summary=summ))
            # spot-check 20 random ids from the rows this file has reached
            hi = sh["row_last"] if summ else sh["row_first"] + len(cells) - 1
            if hi < sh["row_first"]:
                continue
            idx = rng.sample(range(sh["row_first"], hi + 1),
                             min(20, hi - sh["row_first"] + 1))
            for r in idx:
                pid, rec = expand(man, man["rows"][r])
                got = cells.get(pid)
                gkey = "%s|%d|%d" % (rec["operation"], man["rows"][r][0],
                                     man["rows"][r][1])
                exp = grid.get(gkey) if grid else None
                rep["spot_checks"].append(dict(
                    lane=sh["lane"], row=r, id=pid, decoded=rec,
                    matrix_verdict=got, acceptance_grid_verdict=exp,
                    id_present=got is not None,
                    agrees_with_grid=(exp is None or got == exp)))
        rep["line_count_match"] = ok
    else:
        p = {"python": "behavior_python_C.json", "ruby": "behavior_ruby_C.json",
             "php": "behavior_php_C.json"}[lang]
        d = json.load(open(os.path.join(HERE, p)))
        cells = d["cells"]
        rep["raw_cells"] = len(cells)
        rep["line_count_match"] = len(cells) == man["probes"]
        missing = 0
        for row in man["rows"]:
            pid, _ = expand(man, row)
            if pid not in cells:
                missing += 1
        rep["ids_missing_from_table"] = missing
        for r in rng.sample(range(man["probes"]), 20):
            pid, rec = expand(man, man["rows"][r])
            v = cells.get(pid)
            rep["spot_checks"].append(dict(row=r, id=pid, decoded=rec,
                                           cell=v, id_present=v is not None))
    return rep


def main():
    only_verify = "--verify" in sys.argv
    rng = random.Random(20260818)
    reports = []
    jobs = [(l, "A") for l in ORDER] + [(l, "C") for l in ROUTE_C]
    t0 = time.time()
    for n, (lang, route) in enumerate(jobs, 1):
        bar(n - 1, len(jobs), t0, "building %s (%s)" % (lang, route))
        man = manifest_a(lang) if route == "A" else manifest_c(lang)
        p = os.path.join(HERE, "manifest_%s.json" % lang)
        if not only_verify:
            with open(p, "w") as f:
                json.dump(man, f, separators=(",", ":"))
        reports.append(verify(man, rng))
        bar(n, len(jobs), t0, "%s done (%d probes, %.1f MB)"
            % (lang, man["probes"],
               os.path.getsize(p) / 1e6 if os.path.exists(p) else 0))
    print()
    out = dict(frozen=FROZEN, verified=time.strftime("%Y-%m-%d %H:%M:%S"),
               reports=reports)
    print("\n| language | route | manifest probes | shards landed | "
          "line counts match | spot checks | grid agreements |")
    print("|---|---|---|---|---|---|---|")
    for r in reports:
        sc = r["spot_checks"]
        land = sum(1 for s in r.get("shards", []) if s["state"] == "LANDED")
        r["shards_landed"] = land
        r["spot_ids_present"] = sum(1 for s in sc if s["id_present"])
        r["spot_grid_agreements"] = sum(1 for s in sc
                                        if s.get("agrees_with_grid", True))
        agree = sum(1 for s in sc if s.get("agrees_with_grid", True))
        pres = sum(1 for s in sc if s["id_present"])
        print("| %s | %s | %d | %d | %s | %d/%d present | %d/%d |"
              % (r["language"], r["route"], r["manifest_probes"], land,
                 r["line_count_match"], pres, len(sc), agree, len(sc)))
    json.dump(out, open(os.path.join(HERE, "manifest_verify.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
