#!/usr/bin/env python3
"""regen_cost.py -- what the probe regeneration costs, measured from the
lane runs that already happened.

NOTHING IS COMPILED BY THIS PROGRAM.  It reads two things off disk:

  - the Airlock lane logs' own footer line (`# exit 0 in 42.4s`), which is
    the sandbox daemon's measurement of the lane's wall clock;
  - each store's own accepted/refused tally.

THE MODEL, AND WHY IT HAS TWO RATES
-----------------------------------

A probe that the compiler REFUSES costs one compile and stops.  A probe
the compiler ACCEPTS costs the acceptance compile (which IS the ship
build), then the anchor build, then two objdump reads, then the debug
table read.  Those are not the same price, and the regeneration
population is almost entirely accepted probes, so a single blended rate
taken off today's refusal-heavy corpus would understate the cost.

Each language ran TWO lanes -- the plain run and the assignment run --
with different accepted/refused mixes.  Two lanes, two unknowns:

    t_plain = refused_rate * n_refused_plain + accepted_rate * n_accepted_plain
    t_asg   = refused_rate * n_refused_asg   + accepted_rate * n_accepted_asg

Solved per language, so no language's rate is borrowed from another's.
A solution with a negative rate is REFUSED, not clamped: it would mean
the two lanes' totals cannot be explained by the mix, and the honest
answer there is the blended rate with the fact stated.

WALL CLOCK AT THE CAP
---------------------

The trickle runs inside one container capped at half the machine's cores.
The lane daemon runs scripts SERIALLY, so the useful parallelism is
whatever the trickle driver itself creates.  Two wall-clock figures are
reported: serial (one probe at a time, the measured shape) and at the
core cap with the driver compiling several probes at once.

usage:
    /tmp/reconnect_venv/bin/python3 regen_cost.py
writes:
    regen_cost.json
    regen_cost.md
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.expanduser("PUBLIC/Airlock/agent/logs")
LANGS = ["c", "cpp", "go", "rust", "swift"]

# The two lanes each language ran.  `store` is the file the lane folded
# into; `lane` is the script name whose log carries the measured runtime.
LANE_PAIRS = {
    "c": [("op_c.sh", "op_units_c.json"),
          ("op_asg_c.sh", "op_units_asg_c.json")],
    "cpp": [("op_cpp.sh", "op_units_cpp.json"),
            ("op_asg_cpp.sh", "op_units_asg_cpp.json")],
    "go": [("op_go.sh", "op_units_go.json"),
           ("op_asg_go.sh", "op_units_asg_go.json")],
    "rust": [("op_rust.sh", "op_units_rust.json"),
             ("op_asg_rust.sh", "op_units_asg_rust.json")],
    "swift": [("op_swift.sh", "op_units_swift.json"),
              ("op_asg_swift.sh", "op_units_asg_swift.json")],
}

FOOTER = re.compile(r"^# exit (\d+) in ([0-9.]+)s\s*$")

TOTAL_CORES = os.cpu_count()
CAP_CORES = TOTAL_CORES // 2


def lane_runtime(lane):
    """The daemon's own footer measurement for the most recent run of a
    lane.  Returns (seconds, log path)."""
    names = []
    for name in os.listdir(LOGS):
        if name.endswith("__" + lane + ".log"):
            names.append(name)
    if not names:
        raise SystemExit("regen_cost: no log for lane %s in %s" % (lane, LOGS))
    names.sort()
    path = os.path.join(LOGS, names[-1])
    seconds = None
    exit_code = None
    for line in open(path):
        m = FOOTER.match(line)
        if m:
            exit_code = int(m.group(1))
            seconds = float(m.group(2))
    if seconds is None:
        raise SystemExit("regen_cost: no footer measurement in %s" % path)
    return seconds, exit_code, path


def store_tally(store):
    path = os.path.join(HERE, store)
    data = json.load(open(path))
    accepted = 0
    refused = 0
    for key in data["probes"]:
        probe = data["probes"][key]
        ok = ("ship" in probe) and (probe.get("refused") in (None, "", False))
        if ok:
            accepted = accepted + 1
        else:
            refused = refused + 1
    return accepted, refused, path


def solve(rows):
    """Two lanes, two rates.  rows = [(n_ref, n_acc, seconds), ...]"""
    (r1, a1, t1), (r2, a2, t2) = rows
    det = (r1 * a2) - (r2 * a1)
    if det == 0:
        return None
    refused_rate = ((t1 * a2) - (t2 * a1)) / float(det)
    accepted_rate = ((r1 * t2) - (r2 * t1)) / float(det)
    return refused_rate, accepted_rate


def build():
    red = json.load(open(os.path.join(HERE, "legality_reduction2.json")))
    residue = {}
    for record in red["languages"]:
        residue[record["language"]] = record["must_compile"]

    doc = {}
    doc["generated_by"] = "regen_cost.py"
    doc["compiles_nothing"] = True
    doc["machine"] = {"cores": TOTAL_CORES, "cap_cores": CAP_CORES,
                      "cap_rule": "half the machine's cores, per the "
                                  "overheating constraint"}
    doc["measurement_source"] = (
        "the Airlock lane logs' own footer line, written by the sandbox "
        "daemon: `# exit 0 in <seconds>s`")
    doc["languages"] = []
    total_serial = 0.0
    for lang in LANGS:
        rows = []
        lanes = []
        for lane, store in LANE_PAIRS[lang]:
            seconds, exit_code, log_path = lane_runtime(lane)
            accepted, refused, store_path = store_tally(store)
            rows.append((refused, accepted, seconds))
            lanes.append({
                "lane": lane,
                "log": log_path,
                "exit": exit_code,
                "seconds": seconds,
                "probes": accepted + refused,
                "accepted": accepted,
                "refused": refused,
                "store": store_path,
            })
        blended_probes = sum(r[0] + r[1] for r in rows)
        blended_seconds = sum(r[2] for r in rows)
        blended_rate = blended_seconds / blended_probes
        solved = solve(rows)
        note = None
        if solved is None:
            refused_rate = blended_rate
            accepted_rate = blended_rate
            note = ("the two lanes' mixes are linearly dependent, so the "
                    "split cannot be solved; the blended rate is used for "
                    "both and that is stated rather than hidden")
        else:
            refused_rate, accepted_rate = solved
            if refused_rate < 0 or accepted_rate < 0:
                note = ("the solved split has a negative rate, which means "
                        "the two lanes' totals are not explained by the "
                        "accepted/refused mix alone; the blended rate is "
                        "used instead and the solved pair is kept for the "
                        "record")
                refused_rate = blended_rate
                accepted_rate = blended_rate
        n = residue[lang]
        # The regeneration population is what the filter hands to a
        # compiler.  Its accepted/refused split is not known before the
        # run -- that is what the run measures -- so the ACCEPTED rate is
        # applied to all of it.  That is the upper bound of the two rates
        # for every language here, so the estimate errs long.
        serial = n * accepted_rate
        total_serial = total_serial + serial
        doc["languages"].append({
            "language": lang,
            "lanes": lanes,
            "solved_refused_rate_s": round(
                solved[0], 5) if solved else None,
            "solved_accepted_rate_s": round(
                solved[1], 5) if solved else None,
            "blended_rate_s": round(blended_rate, 5),
            "rate_used_s": round(accepted_rate, 5),
            "note": note,
            "residue_probes": n,
            "serial_seconds": round(serial, 1),
        })
    doc["totals"] = {
        "residue_probes": sum(residue[k] for k in LANGS),
        "serial_seconds": round(total_serial, 1),
        "serial_hours": round(total_serial / 3600.0, 2),
    }
    # At the cap the driver compiles CAP_CORES probes at once.  Compilation
    # of one small single-function probe is single-threaded, so the speedup
    # is close to the worker count; 0.8 is applied as an efficiency haircut
    # for the shared file system and the process churn, and it is a
    # DECLARED assumption, not a measurement.
    doc["at_the_cap"] = {
        "workers": CAP_CORES,
        "efficiency_assumed": 0.8,
        "evidence_class": "human interpretation -- the worker count is a "
                          "choice and the 0.8 haircut is declared, not "
                          "measured. The serial figure above is the "
                          "measured one.",
        "wall_clock_seconds": round(
            total_serial / (CAP_CORES * 0.8), 1),
        "wall_clock_hours": round(
            total_serial / (CAP_CORES * 0.8) / 3600.0, 2),
    }
    doc["cpu_seconds"] = {
        "value": round(total_serial, 1),
        "note": "CPU time is the serial figure: the work is the same "
                "compiles however they are spread across cores.",
    }
    return doc


def markdown(doc):
    out = []
    out.append("# regeneration cost, measured from the lane runs that "
               "already happened")
    out.append("")
    out.append("Nothing was compiled to produce this page. Every runtime is "
               "the Airlock daemon's own footer line.")
    out.append("")
    out.append("## the measured lanes")
    out.append("")
    out.append("| language | lane | probes | accepted | refused | measured |")
    out.append("|---|---|---:|---:|---:|---:|")
    for record in doc["languages"]:
        for lane in record["lanes"]:
            out.append("| %s | `%s` | %d | %d | %d | %.1fs |"
                       % (record["language"], lane["lane"], lane["probes"],
                          lane["accepted"], lane["refused"], lane["seconds"]))
    out.append("")
    out.append("## the two rates, solved per language")
    out.append("")
    out.append("| language | refused probe | accepted probe | rate used | "
               "residue | serial |")
    out.append("|---|---:|---:|---:|---:|---:|")
    for record in doc["languages"]:
        out.append("| %s | %s | %s | %.4fs | %d | %.0fs |"
                   % (record["language"],
                      ("%.4fs" % record["solved_refused_rate_s"])
                      if record["solved_refused_rate_s"] is not None else "-",
                      ("%.4fs" % record["solved_accepted_rate_s"])
                      if record["solved_accepted_rate_s"] is not None else "-",
                      record["rate_used_s"], record["residue_probes"],
                      record["serial_seconds"]))
    out.append("| **total** | | | | **%d** | **%.0fs** |"
               % (doc["totals"]["residue_probes"],
                  doc["totals"]["serial_seconds"]))
    out.append("")
    out.append("## where the two-rate solve failed, and what was used "
               "instead")
    out.append("")
    out.append("The two lanes are not only two mixes: the assignment lane "
               "compiles a DIFFERENT PROBE SHAPE, so its per-probe cost "
               "differs for reasons the accepted/refused split does not "
               "carry. Where that shows up, the solve returns a negative "
               "rate, and a negative rate is refused rather than clamped.")
    out.append("")
    for record in doc["languages"]:
        if record["note"]:
            out.append("- **%s** -- %s. Rate used: %.4fs (blended)."
                       % (record["language"], record["note"],
                          record["rate_used_s"]))
        else:
            out.append("- **%s** -- solved cleanly; the accepted rate "
                       "%.4fs is used."
                       % (record["language"], record["rate_used_s"]))
    out.append("")
    out.append("## the answer")
    out.append("")
    out.append("- serial, one probe at a time: **%.0f s = %.2f hours**"
               % (doc["totals"]["serial_seconds"],
                  doc["totals"]["serial_hours"]))
    out.append("- CPU time: the same %.0f s -- the work does not change "
               "when it is spread."
               % (doc["cpu_seconds"]["value"]))
    out.append("- at the cap (%d of %d cores, %d workers, 0.8 efficiency "
               "assumed): **%.2f hours** wall clock."
               % (doc["machine"]["cap_cores"], doc["machine"]["cores"],
                  doc["at_the_cap"]["workers"],
                  doc["at_the_cap"]["wall_clock_hours"]))
    out.append("")
    return "\n".join(out) + "\n"


def refuse_own_output_on_spelling_failure(paths):
    cmd = [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py")]
    cmd.extend(paths)
    done = subprocess.run(cmd, capture_output=True, text=True)
    print(done.stdout.strip())
    if done.returncode != 0:
        print(done.stderr.strip())
        for path in paths:
            if os.path.exists(path):
                os.remove(path)
        raise SystemExit("REFUSED OWN OUTPUT: spelling guard failed")


def main():
    doc = build()
    p1 = os.path.join(HERE, "regen_cost.json")
    fh = open(p1, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()
    p2 = os.path.join(HERE, "regen_cost.md")
    open(p2, "w").write(markdown(doc))
    print(markdown(doc))
    print("wrote %s" % p1)
    print("wrote %s" % p2)
    refuse_own_output_on_spelling_failure([p1])


if __name__ == "__main__":
    main()
