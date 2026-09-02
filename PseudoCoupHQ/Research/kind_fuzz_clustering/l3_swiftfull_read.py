#!/usr/bin/env python3
"""l3_swiftfull_read.py -- fold the swift REDO shards and diff them
against the superseded -typecheck matrix.

Writes valuematrix_swift_full.json (the new measurement) and
swiftfull_diff.json (what moved).  It does NOT overwrite
valuematrix_swift.json: that file is the -typecheck measurement and is
kept, marked superseded-with-reason, because a wrong instrument that
produced a published number belongs on the record.

Carries the same completeness gate as l3_matrix_read.py: expected
probes from swiftfull_plan.json, one __SUMMARY__ line per shard, and
`complete`/`completeness` written into the result.
"""
import json, os, sys
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
sys.path.insert(0, HERE)
from progress import Progress          # noqa: E402


def main():
    plan = json.load(open(os.path.join(HERE, "swiftfull_plan.json")))
    space = json.load(open(os.path.join(HERE, "space_swift.json")))
    hs, ops = space["holders"], space["operations"]
    vclass = [h["value_classes"] for h in hs]
    files = sorted(f for f in os.listdir(RAW)
                   if f.startswith("vs_swift_") and f.endswith(".txt"))
    print("shards present: %s" % (", ".join(files) or "(none)"))
    cells, summaries, rows = defaultdict(dict), [], 0
    probe_verdict = {}
    for fn in files:
        lines = open(os.path.join(RAW, fn), errors="replace").read().splitlines()
        pg = Progress(len(lines), "vs:swift:%s" % fn, every=20000)
        for line in lines:
            pg.tick()
            if line.startswith("__SUMMARY__"):
                summaries.append(line.split("|")[1:]); continue
            p = line.split("|", 2)
            if len(p) < 2 or not p[0].startswith("P"):
                continue
            try:
                i, j, x, y, k = (int(v) for v in p[0][1:].split("_"))
            except ValueError:
                continue
            cells["%s|%d|%d" % (ops[k], i, j)][(x, y)] = p[1]
            probe_verdict[p[0]] = p[1]
            rows += 1
        pg.close()

    uniform = split = 0
    out = {}
    for key, tab in cells.items():
        vs = set(tab.values())
        op, i, j = key.rsplit("|", 2); i, j = int(i), int(j)
        rec = dict(operation=op,
                   lhs=dict(form=hs[i]["form"], holder=hs[i]["rep"]),
                   rhs=dict(form=hs[j]["form"], holder=hs[j]["rep"]),
                   probes=len(tab))
        if len(vs) == 1:
            uniform += 1; rec["shape"] = "uniform"
            rec["verdict"] = next(iter(vs))
        else:
            split += 1; rec["shape"] = "split"
            rec["verdicts"] = sorted(vs)
            rec["by_value_class"] = [
                dict(lhs_value_class=vclass[i][x],
                     rhs_value_class=vclass[j][y], verdict=v)
                for (x, y), v in sorted(tab.items())]
        out[key] = rec

    expect, shards = plan["probes"], plan["shards"]
    complete = (rows == expect) and (len(summaries) == shards)
    note = "COMPLETE" if complete else (
        "TRUNCATED -- %d of %d probes over %d of %d shard summary lines; "
        "do not read as a measurement" % (rows, expect, len(summaries), shards))
    if not complete:
        print("  !! swift REDO INCOMPLETE: %s" % note)
    res = dict(language="swift", route="A2r full swiftc -c value matrix",
               instrument="swiftc -c (SILGen and IRGen run)",
               supersedes="valuematrix_swift.json (swiftc -typecheck)",
               grain="(operation, lhs holder, rhs holder) x full value "
                     "cross product",
               probes=rows, expected_probes=expect,
               shards_present=len(files), shards_expected=shards,
               shard_summaries=summaries, pair_cells=len(out),
               uniform_cells=uniform, split_cells=split,
               complete=complete, completeness=note, cells=out)
    json.dump(res, open(os.path.join(HERE, "valuematrix_swift_full.json"), "w"))

    # ---- the diff against the superseded instrument
    old = json.load(open(os.path.join(HERE, "valuematrix_swift.json")))
    oc = old["cells"]
    moved, same = [], 0
    for key, rec in out.items():
        o = oc.get(key)
        if o is None:
            moved.append(dict(cell=key, was=None, now=rec.get("shape")))
            continue
        ov = o.get("verdict") if o["shape"] == "uniform" else "SPLIT:" + \
            ",".join(o.get("verdicts", []))
        nv = rec.get("verdict") if rec["shape"] == "uniform" else "SPLIT:" + \
            ",".join(rec.get("verdicts", []))
        if ov == nv:
            same += 1
        else:
            moved.append(dict(cell=key, was=ov, now=nv))
    n_acc_old = sum(1 for r in oc.values()
                    if r["shape"] == "uniform" and r.get("verdict") == "ACCEPT")
    n_acc_new = sum(1 for r in out.values()
                    if r["shape"] == "uniform" and r.get("verdict") == "ACCEPT")
    p_acc_old = None
    p_acc_new = sum(1 for v in probe_verdict.values() if v == "ACCEPT")
    diff = dict(cells_compared=len(out), cells_unchanged=same,
                cells_moved=len(moved),
                pair_cells_all_accept_typecheck=n_acc_old,
                pair_cells_all_accept_fullc=n_acc_new,
                probes_accept_fullc=p_acc_new,
                probes_accept_typecheck=sum(
                    int(s[1]) for s in old["shard_summaries"]),
                moved=moved[:4000], moved_truncated=len(moved) > 4000)
    json.dump(diff, open(os.path.join(HERE, "swiftfull_diff.json"), "w"),
              indent=1)
    json.dump(sorted(k for k, v in probe_verdict.items() if v == "ACCEPT"),
              open(os.path.join(HERE, "swiftfull_accepts.json"), "w"))
    print("| measure | -typecheck | full swiftc |")
    print("|---|---|---|")
    print("| probes | %d | %d |" % (diff["probes_accept_typecheck"], p_acc_new))
    print("| all-ACCEPT pair cells | %d | %d |" % (n_acc_old, n_acc_new))
    print("| uniform / split cells | %d / %d | %d / %d |"
          % (old["uniform_cells"], old["split_cells"], uniform, split))
    print("| pair cells moved | - | %d of %d |" % (len(moved), len(out)))
    print("gate: %s" % note)


if __name__ == "__main__":
    main()
