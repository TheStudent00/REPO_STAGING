#!/usr/bin/env python3
"""task50a_recompile1.py -- compile the regenerated source of every probe
the corrected emitter changes, and tally accept/refuse verbatim.

WHAT IS COMPILED, AND WHAT IS NOT
---------------------------------
Only the probes whose GENERATED TEXT the fix changes, as
`task50a_diff1.json` lists them: 516 whose `@_cdecl` line the fix
removes (a superset of the 276 counted in log 137's F45-4, exactly the
516 the compiler refused with that diagnostic) and 891 whose `@_cdecl`
line the fix adds.  The full regeneration is NOT re-run: this task
compiles 1,407 sources, not 129,553.

The `attribute_added` half is compiled for a reason worth stating: the
fix widens the set as well as narrowing it, and a widening can only be
trusted if the compiler is asked.  A probe that the old emitter left
unexported and that now refuses would be a REGRESSION, and this is the
measurement that would show it.

The flags are the probe lanes' own, anchor mode, copied from
`lane_gen.py :: compile_probe`:

    /persist/swift/usr/bin/swiftc -Onone -g -c

so a verdict here is comparable with the store's verdict for the same
probe.  The full diagnostic is captured verbatim through the codec of
record (`verbatim_diag`), and the product is refused rather than
decoded if it does not open with the marker.

WHERE IT RUNS
-------------
Generation and fold on the host; the 1,407 compilations inside
Airlock's `trickle` instance, submitted through `airlock submit`.
Nothing here runs podman.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim.

The set compiled here is selected by PROBE ID, from a diff computed on
generated TEXT.  Rows are grouped by the direction of the text change
and by the compiler's own message shape.  No token is a key or a
selector.

usage:
    /tmp/reconnect_venv/bin/python3 task50a_recompile1.py --emit
    /tmp/reconnect_venv/bin/python3 task50a_recompile1.py --run
writes:
    task50a_lanes/recompile_swift.sh
    task50a_recompile1.json
"""

import argparse
import collections
import glob
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import declare_lane                                        # noqa: E402
import regen_validate1                                     # noqa: E402
import swift_cdecl_witness1 as witness                     # noqa: E402
import trickle2                                            # noqa: E402

DIFF = os.path.join(HERE, "task50a_diff1.json")
BANKED = os.path.join(HERE, "regen_witness_validation1.json")
LANE_DIR = os.path.join(HERE, "task50a_lanes")
OUTBOX = os.path.join(HERE, "task50a_outbox")
RAW_DIR = os.path.join(HERE, "task50a_raw")
PRODUCT = os.path.join(HERE, "task50a_recompile1.json")

LANE_NAME = "recompile_swift.sh"
OUT_NAME = "recompile_swift"


def changed_rows():
    doc = json.load(open(DIFF))
    rows = [c for c in doc["changed"] if c["manifest"] == "regeneration"]
    rows.sort(key=lambda c: c["n"])
    return rows


def items():
    """One compile per changed probe, carrying the CORRECTED source."""
    out = []
    for row in changed_rows():
        out.append({"language": "swift", "id": row["id"],
                    "form": row["direction"],
                    "source": row["source_after"]})
    return out


def emit():
    rows = items()
    if not os.path.isdir(LANE_DIR):
        os.makedirs(LANE_DIR)
    text = declare_lane.lane("swift", rows, OUT_NAME)
    path = os.path.join(LANE_DIR, LANE_NAME)
    fh = open(path, "w")
    fh.write(text)
    fh.close()
    counts = collections.Counter(r["form"] for r in rows)
    print("swift %5d compilations -> %s" % (len(rows), path))
    print("  by direction of the text change: %s" % dict(counts))
    return path


def run():
    path = emit()
    for folder in (OUTBOX, RAW_DIR):
        if not os.path.isdir(folder):
            os.makedirs(folder)
    lane_copy = os.path.join(OUTBOX, LANE_NAME)
    shutil.copyfile(path, lane_copy)
    inst = trickle2.Instance()
    print(inst.describe())
    ok, said = inst.submit(lane_copy)
    print(said.strip()[-600:])
    if not ok:
        raise SystemExit("REFUSE: airlock submit did not accept the lane")
    fields = inst.wait(LANE_NAME, 7200)
    print("status: %s" % json.dumps(fields))
    if fields.get("state") != "done":
        raise SystemExit("REFUSE: lane did not finish (state=%s)"
                         % fields.get("state"))
    product = os.path.join(inst.out, "%s.txt" % OUT_NAME)
    if not os.path.isfile(product):
        raise SystemExit("REFUSE: no product at %s" % product)
    raw = os.path.join(RAW_DIR, "%s.txt" % OUT_NAME)
    shutil.copyfile(product, raw)
    fold(witness.parse_product(open(raw).read()), raw)


def store_verdicts():
    """What the banked regeneration recorded for each swift probe."""
    out = {}
    for path in glob.glob(os.path.join(HERE, "trickle_store",
                                       "op_units2_swift_*.json")):
        doc = json.load(open(path))
        for key in doc["probes"]:
            probe = doc["probes"][key]
            accepted = ("ship" in probe) and (
                probe.get("refused") in (None, "", False))
            out["swift/probe_%s" % key] = {
                "verdict": "ACCEPT" if accepted else "REFUSE",
                "refusal": probe.get("refused") or "",
                "filter_verdict": probe["meta"].get("filter_verdict"),
            }
    return out


def fold(rows, raw_path):
    diff = json.load(open(DIFF))
    banked = json.load(open(BANKED))
    counted_shape = banked["miss_shapes"][0]["text"]
    before = store_verdicts()
    store_meta = before
    by_id = {}
    for row in rows:
        by_id[row["id"]] = row
    directions = {}
    for row in changed_rows():
        directions[row["id"]] = row
    tally = collections.defaultdict(int)
    still_refusing = []
    regressions = []
    shapes = collections.defaultdict(int)
    for pid in sorted(directions, key=lambda p: directions[p]["n"]):
        if pid not in by_id:
            raise SystemExit("REFUSE: no compilation result for %s" % pid)
        after = by_id[pid]
        direction = directions[pid]["direction"]
        was = before.get(pid, {}).get("verdict", "(not in the store)")
        tally["%s_%s" % (direction, after["verdict"].lower())] += 1
        tally["total"] += 1
        if after["verdict"] == "REFUSE":
            shapes[regen_validate1.shape_of(after["diagnostic"])] += 1
            entry = {
                "language": "swift",
                "id": pid,
                "n": directions[pid]["n"],
                "lhs_type": directions[pid]["lhs_type"],
                "rhs_type": directions[pid]["rhs_type"],
                "result_type": directions[pid]["result_type"],
                "direction": direction,
                "verdict_in_the_banked_store": was,
                "refusal": after["diagnostic"],
            }
            still_refusing.append(entry)
            if was == "ACCEPT":
                regressions.append(entry)

    counted_276 = set()
    for pid, row in directions.items():
        if row["direction"] != "attribute_removed":
            continue
        was_text = before.get(pid, {}).get("refusal", "")
        if regen_validate1.shape_of(was_text) != counted_shape:
            continue
        # log 137 counted the misses INSIDE THE ORACLE'S SCOPE: a probe
        # the legality filter called `legal` that the compiler refused.
        # A `no_rule` candidate carries the same refusal and the same
        # cause, but the oracle never predicted anything about it, so it
        # was never a miss.  Both populations are reported; neither is
        # folded into the other.
        if store_meta.get(pid, {}).get("filter_verdict") != "legal":
            continue
        counted_276.add(pid)
    counted_now = collections.Counter(
        by_id[p]["verdict"] for p in counted_276)
    out_of_scope = sorted(
        pid for pid in directions
        if directions[pid]["direction"] == "attribute_removed"
        and pid not in counted_276)
    out_of_scope_now = collections.Counter(
        by_id[p]["verdict"] for p in out_of_scope)

    doc = {}
    doc["generated_by"] = "task50a_recompile1.py"
    doc["task"] = "50(a) -- the swift probe emitter's @_cdecl test"
    doc["reads"] = ["task50a_diff1.json", "regen_witness_validation1.json",
                    "trickle_store/op_units2_swift_*.json"]
    doc["population"] = (
        "the %d regeneration candidates whose generated text the "
        "corrected emitter changes.  The regeneration itself is NOT "
        "re-run; the banked 29,288 accepted probes predate this fix and "
        "are untouched." % tally["total"])
    doc["flags"] = ("/persist/swift/usr/bin/swiftc -Onone -g -c, copied "
                    "from lane_gen.py :: compile_probe, anchor mode")
    doc["spelling_ban"] = (
        "the compiled set is selected by probe id from a text diff; rows "
        "are grouped by the direction of the text change and by the "
        "compiler's own message shape; no key, grouping, pairing or row "
        "structure is an operator token")
    doc["raw_product"] = os.path.relpath(raw_path, HERE)
    doc["tally"] = dict(tally)
    doc["the_276_counted_in_log_137"] = {
        "how_they_are_identified": (
            "an attribute_removed candidate whose banked refusal has the "
            "message shape regen_witness_validation1.json banked as "
            "shape_0001, AND whose legality-oracle verdict was `legal` -- "
            "log 137 counted misses inside the oracle's scope"),
        "count": len(counted_276),
        "verdicts_now": dict(counted_now),
    }
    doc["same_cause_outside_the_oracle_scope"] = {
        "how_they_are_identified": (
            "an attribute_removed candidate the oracle called `no_rule`: "
            "the same refusal and the same cause, never a miss because "
            "nothing was predicted about it"),
        "count": len(out_of_scope),
        "verdicts_now": dict(out_of_scope_now),
    }
    doc["still_refusing"] = still_refusing
    doc["regressions_probes_that_were_accepted_and_now_refuse"] = regressions
    doc["refusal_shapes_after_the_fix"] = [
        {"count": n, "text": t} for t, n in
        sorted(shapes.items(), key=lambda kv: -kv[1])]
    fh = open(PRODUCT, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()
    print("tally: %s" % json.dumps(dict(tally), indent=1))
    print("the 276 counted in log 137: %d, now %s"
          % (len(counted_276), dict(counted_now)))
    print("same cause, outside the oracle scope: %d, now %s"
          % (len(out_of_scope), dict(out_of_scope_now)))
    print("still refusing: %d ; regressions: %d"
          % (len(still_refusing), len(regressions)))
    for t, n in sorted(shapes.items(), key=lambda kv: -kv[1]):
        print("  %5d  %s" % (n, t[:110]))
    print("wrote %s" % PRODUCT)
    witness.guard(PRODUCT)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--fold", metavar="RAWFILE")
    args = ap.parse_args()
    if args.emit:
        emit()
        return
    if args.fold:
        fold(witness.parse_product(open(args.fold).read()), args.fold)
        return
    if args.run:
        run()
        return
    ap.error("one of --emit, --run, --fold is required")


if __name__ == "__main__":
    main()
