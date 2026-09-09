#!/usr/bin/env bash
# t91_l1_populations_and_sample.sh -- TASK 91, lane 1 of the round-17
# re-gate: the two populations named unit by unit, then a SAMPLE of the
# re-gate run before the full pass.
#
# WHAT IS MEASURED HERE, and why a sample comes first.  Task 91 re-gates
# the 415 withdrawn disproofs and the 5,602 undecided verdicts of
# log 153 through the ONE reference (`reference.py`).  Before the whole
# population runs, this lane measures seconds-per-unit and peak resident
# size on 200 units drawn from those two buckets, so the full pass is
# planned against a measurement and not a guess.
#
# THE MEMORY BOUND, stated before the run.
#   what is held:  ONE canon38 source document at a time (the biggest is
#                  `canon38_wrapped_cpp.json`), its units transcribed one
#                  at a time; no store of terms is kept across units.
#   lane cap:      6000 MB, abort named T91_MEMORY_ABORT, checked after
#                  every source document and every 25 sampled units.
#   nothing is held across the two configurations: each is a fresh Gate.
#
# THE TWO CONFIGURATIONS, both of the ONE reference:
#   (a) no attached runtime callees -- a `call` is a transfer out of the
#       unit.  This is the configuration `gate58_run.py` ran under.
#   (b) the attached callee bodies of `canon39_callee_units.json` -- the
#       reference steps into the callee's own body (reference CORE,
#       "A `call` WITH AN ATTACHED CALLEE IS NOT A TRANSFER").
#
# Products: PseudoCoupHQ/Research/op_pipeline/t91_populations.json
#           /out/t91_sample.json
set -uo pipefail

cd PseudoCoupHQ/Research/op_pipeline || exit 2
mkdir -p /out

echo "[1/2] the two populations, named unit by unit"
python3 t91_populations.py || exit 3

echo ""
echo "[2/2] the sample: 200 units of the two populations, both configurations"
python3 - <<'PY'
import glob
import json
import os
import resource
import sys
import time

HERE = "PseudoCoupHQ/Research/op_pipeline"
sys.path.insert(0, HERE)

import gate as GATE
import layer4c
import reference as REF

LANE_CAP_MB = 6000
LANE_ABORT = "T91_MEMORY_ABORT"
SAMPLE_SIZE = 200


def peak():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def check(stage):
    now = peak()
    if now > LANE_CAP_MB:
        raise SystemExit("%s: peak resident size %.1f MB passed the "
                         "lane's stated cap of %d MB during %s"
                         % (LANE_ABORT, now, LANE_CAP_MB, stage))
    return now


populations = json.load(open(os.path.join(HERE, "t91_populations.json")))
wanted = {}
for name in populations["buckets"]["withdrawn"]:
    wanted[name] = "withdrawn"
for name in populations["buckets"]["undecided"]:
    wanted[name] = "undecided"
print("    the two buckets hold %d units in all" % len(wanted))


def sources():
    out = []
    for lang in ("c", "cpp", "go", "rust", "swift"):
        out.append(os.path.join(HERE, "canon38_wrapped_%s.json" % lang))
    out.append(os.path.join(HERE, "canon38_interp.json"))
    out.extend(sorted(glob.glob(os.path.join(HERE, "canon38_regen_store",
                                             "*.json"))))
    return [p for p in out if os.path.exists(p)]


def callee_units():
    path = os.path.join(HERE, "canon39_callee_units.json")
    if not os.path.exists(path):
        return {}
    document = json.load(open(path))
    out = {}
    for key, unit in document.get("units", {}).items():
        toolchain = unit.get("toolchain") or key.split("/", 1)[0]
        name = unit.get("callee") or key.split("/", 1)[-1]
        out.setdefault(toolchain, {})
        out[toolchain][name] = unit
    return out


# ---- collect the sample bodies, one source document at a time -------
chosen = []
for path in sources():
    if len(chosen) >= SAMPLE_SIZE:
        break
    document = json.load(open(path))
    for name in sorted(document.get("units", {})):
        if len(chosen) >= SAMPLE_SIZE:
            break
        if name not in wanted:
            continue
        unit = document["units"][name]
        if "ledger" not in unit:
            continue
        unit = dict(unit)
        unit["unit"] = name
        chosen.append((name, wanted[name], unit))
    del document
    check("collecting from %s" % os.path.basename(path))

print("    sampled %d units" % len(chosen))

attached = callee_units()
print("    attached callee archives: %s"
      % ", ".join("%s=%d" % (k, len(v)) for k, v in sorted(attached.items())))

rows = []
for tag, runtime_units in (("no_attached_callees", None),
                           ("attached_callees", attached)):
    reference = REF.Reference(runtime_units=runtime_units)
    gate = GATE.Gate(reference=reference)
    started = time.time()
    for index, (name, bucket, unit) in enumerate(chosen):
        one = time.time()
        record = {"unit": name, "bucket": bucket, "configuration": tag}
        try:
            transcription = layer4c.transcribe(unit)
        except Exception as problem:
            record["outcome"] = "TRANSCRIPTION_REFUSED"
            record["reason"] = "%s: %s" % (type(problem).__name__, problem)
            record["seconds"] = round(time.time() - one, 3)
            rows.append(record)
            continue
        term = transcription.out_term
        ship = gate.prove_term_against_ship(term, unit)
        record["ship_outcome"] = ship.outcome
        record["ship_reason"] = ship.reason
        if ship.proved():
            record["outcome"] = ship.outcome
        else:
            text = gate.prove_term_against_text(term, unit)
            record["text_outcome"] = text.outcome
            record["text_reason"] = text.reason
            if text.proved():
                record["outcome"] = text.outcome
            elif "DISPROVED" in (ship.outcome, text.outcome):
                record["outcome"] = "DISPROVED"
            else:
                record["outcome"] = ship.outcome
        record["seconds"] = round(time.time() - one, 3)
        rows.append(record)
        if index % 25 == 0:
            rss = check("%s unit %d" % (tag, index))
            print("      [%d/%d] %s %-22s %-14s %.2fs peak %.0f MB"
                  % (index + 1, len(chosen), tag, name,
                     record.get("outcome"), record["seconds"], rss))
            sys.stdout.flush()
    spent = time.time() - started
    print("    %s: %d units in %.1fs -- %.3f s/unit, peak %.0f MB"
          % (tag, len(chosen), spent, spent / max(1, len(chosen)), peak()))

by_configuration = {}
for row in rows:
    tag = row["configuration"]
    by_configuration.setdefault(tag, {})
    outcome = row.get("outcome")
    by_configuration[tag][outcome] = by_configuration[tag].get(outcome, 0) + 1

seconds = {}
for row in rows:
    seconds.setdefault(row["configuration"], []).append(row["seconds"])

summary = {}
for tag in seconds:
    values = sorted(seconds[tag])
    summary[tag] = {
        "units": len(values),
        "total_seconds": round(sum(values), 1),
        "mean_seconds": round(sum(values) / len(values), 3),
        "slowest_seconds": values[-1],
        "outcomes": by_configuration[tag],
    }

with open("/out/t91_sample.json", "w") as handle:
    json.dump({"sample_size": len(chosen),
               "lane_cap_mb": LANE_CAP_MB,
               "lane_abort": LANE_ABORT,
               "peak_rss_mb": round(peak(), 1),
               "per_configuration": summary,
               "rows": rows}, handle, indent=1, sort_keys=True)

print("")
for tag in sorted(summary):
    print("  %s: %s" % (tag, json.dumps(summary[tag], sort_keys=True)))
print("SAMPLE PEAK RESIDENT SIZE: %.1f MB, cap %d MB"
      % (peak(), LANE_CAP_MB))
PY
