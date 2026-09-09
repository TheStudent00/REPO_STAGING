#!/usr/bin/env python3
"""recapture_asg.py -- re-run the THREE ASSIGNMENT lanes (go, rust, swift)
through the verbatim path, so the 118 out-of-scope findings from log 126 /
log 131 §7.7 / log 140 §8 can actually be superseded.

TASK 50(b).  Log 140 §8.2 named exactly what was left undone: round 8's
regeneration and re-capture went through `probe_gen.py`, which EXCLUDES the
assignment bucket by its own `EXCLUDED_BUCKETS`; the assignment lanes'
probes come from a different generator (`asg_stage.py`), so no plain-run
re-capture ever touched them.  This program gives the three `op_asg_*`
lanes (go, rust, swift; c and cpp are not run here because log 126 §3.2
measured them at 0 ALTERED fields each) the SAME verbatim treatment
`recapture_original.py` gave the three plain lanes -- but through
`trickle2.py`'s route (Airlock's front door, `airlock submit`), because
`trickle.py`'s `podman exec` route against the copied container is
superseded (`TRICKLE_SUPERSEDED.md`, 2026-09-02).

WHAT THIS RUNS

`probe_manifest_asg_<lang>.json` for go, rust and swift -- 432 + 396 + 216
= 1,044 candidates, unfiltered, exactly as `op_asg_go.sh` / `op_asg_rust.sh`
/ `op_asg_swift.sh` ran them on 2026-08-25 (confirmed below: same probe
count as log 126 §3.2's table for `op_pipeline/op_units_asg_<lang>.json`).
Every probe is rendered by `lane_gen_verbatim.lane_verbatim`, submitted to
the `trickle` Airlock instance, and folded WITHOUT decoding unless the
product carries the `#verbatim-escape v1` marker.

WHAT THIS DOES NOT TOUCH

No existing store is opened for writing.  `op_units_asg_<lang>.json`,
`probe_manifest_asg_<lang>.json`, and every `stage_asg/*` copy are read
only by `check_no_spelling_keys.py`'s companion audit script, never by
this program.  This program's own output lives under `trickle_store/` as
`op_units_asgrecap_<lang>_c<k>.json`, and the merged product (built by
`recapture_asg.py --merge`) is a NEW file,
`op_units_asg_<lang>_verbatim.json`, beside the originals.

THE SPELLING BAN, pasted verbatim as required: "THE SPELLING BAN,
ABSOLUTE (the owner, restated in anger 2026-08-25 after a second violation). No
operator token may appear in ANY key, grouping, pairing, row structure,
candidate selection, or comparison scope, anywhere in this line -- not in
matching, not in "which pairs get compared", not in report rows, not in
dropdowns. The candidate set for comparison comes from machine-form
evidence (clusters, connections, type pairs) or from ratified intention
-- never from the token. The token appears exactly once per unit: as a
display label on the member. HISTORY OF VIOLATIONS, so the pattern is
visible: (1) the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25 --
the fix brief itself reintroduced it as "same-operator pairs").
MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
units must run the spelling-key check (op_pipeline/check_no_spelling_keys.py)
and refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim." Chunks and merged stores
are slices of a manifest in probe-number order; nothing here keys,
groups, or selects by an operator token. Every output is walked by
`check_no_spelling_keys.py`, and this program deletes its own output on
a failure.

usage:
    python3 recapture_asg.py --plan
    python3 recapture_asg.py --run
    python3 recapture_asg.py --status
    python3 recapture_asg.py --merge
"""

import argparse
import json
import os
import sys

import trickle
import trickle2

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["go", "rust", "swift"]
STATE = os.path.join(HERE, "recapture_asg_state.json")
CHUNK = 400
STORE_DIR = trickle2.STORE_DIR


def plan(chunk_size):
    if os.path.exists(STATE):
        raise SystemExit(
            "REFUSE: %s already exists. Delete it by hand to start over."
            % STATE)
    chunks = []
    for lang in LANGS:
        path = os.path.join(HERE, "probe_manifest_asg_%s.json" % lang)
        doc = json.load(open(path))
        keys = sorted(int(k) for k in doc["probes"])
        k = 0
        idx = 0
        while k < len(keys):
            part = keys[k:k + chunk_size]
            chunks.append({
                "chunk_id": "asgrecap_%s_c%04d" % (lang, idx),
                "language": lang,
                "first_probe": part[0],
                "last_probe": part[-1],
                "probes": len(part),
                "state": "pending",
                "manifest_prefix": "probe_manifest_asg",
                "lane_prefix": "asgrecap",
                "store_prefix": "op_units_asgrecap",
            })
            k = k + chunk_size
            idx = idx + 1
    state = {}
    state["generated_by"] = "recapture_asg.py"
    state["what_this_is"] = (
        "resume state for the ASSIGNMENT-lane re-capture (task 50(b)). "
        "A chunk marked done is never rerun.")
    state["population"] = (
        "probe_manifest_asg_<lang>.json for go, rust, swift -- the same "
        "1,044 candidates the 2026-08-25 op_asg_* lanes ran, unfiltered")
    state["chunks"] = chunks
    state["totals"] = {"chunks": len(chunks),
                       "probes": sum(c["probes"] for c in chunks)}
    save(state)
    return state


def save(state):
    tmp = STATE + ".tmp"
    fh = open(tmp, "w")
    json.dump(state, fh, indent=1)
    fh.write("\n")
    fh.close()
    os.replace(tmp, STATE)


def load():
    if not os.path.exists(STATE):
        raise SystemExit("REFUSE: no plan yet. Run --plan first.")
    return json.load(open(STATE))


def refuse_own_output_on_spelling_failure(paths):
    import subprocess
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


def run():
    state = load()
    instance = trickle2.Instance()
    print(instance.describe())
    for chunk in state["chunks"]:
        if chunk.get("state") == "done":
            continue
        record = trickle2.run_chunk(instance, chunk)
        if not record.get("ok"):
            chunk["state"] = "failed"
            chunk["detail"] = record.get("reason")
            print("  %-20s FAILED: %s"
                  % (chunk["chunk_id"], record.get("reason")))
            save(state)
            continue
        rc, out, _err = trickle.guard([record["store"]])
        if rc != 0:
            os.remove(record["store"])
            chunk["state"] = "refused_by_the_spelling_guard"
            chunk["detail"] = out
            save(state)
            continue
        chunk["state"] = "done"
        chunk["tally"] = record["tally"]
        chunk["seconds"] = record["seconds"]
        chunk["store"] = record["store"]
        t = record["tally"]
        print("  %-20s %5d submitted  %5d accepted  %5d refused  %6.1fs"
              % (chunk["chunk_id"], t["submitted"], t["accepted"],
                 t["refused"], record["seconds"]))
        save(state)
    save(state)
    refuse_own_output_on_spelling_failure([STATE])


def status():
    state = load()
    by_lang = {}
    for c in state["chunks"]:
        row = by_lang.setdefault(c["language"], {"done": 0, "left": 0})
        if c.get("state") == "done":
            row["done"] += 1
        else:
            row["left"] += 1
    for lang in sorted(by_lang):
        row = by_lang[lang]
        print("  %-6s done %-3d not done %d" % (lang, row["done"], row["left"]))


def merge():
    """Merge each language's chunk stores into one
    op_units_asg_<lang>_verbatim.json, a NEW file beside the originals."""
    state = load()
    by_lang = {}
    for c in state["chunks"]:
        by_lang.setdefault(c["language"], []).append(c)
    written = []
    for lang, chunks in by_lang.items():
        not_done = [c for c in chunks if c.get("state") != "done"]
        if not_done:
            print("!! %s: %d chunk(s) not done, skipping merge"
                  % (lang, len(not_done)))
            continue
        probes = {}
        tally_sum = {}
        for c in sorted(chunks, key=lambda c: c["first_probe"]):
            doc = json.load(open(c["store"]))
            for k, v in doc["probes"].items():
                probes[k] = v
            for tk, tv in doc["tally"].items():
                tally_sum[tk] = tally_sum.get(tk, 0) + tv
        out = {}
        out["generated_by"] = "recapture_asg.py --merge"
        out["language"] = lang
        out["capture"] = ("verbatim -- every chunk's lane product carried "
                          "'#verbatim-escape v1' and every escaped field "
                          "was decoded back to the compiler's own "
                          "characters")
        out["manifest"] = "probe_manifest_asg_%s.json" % lang
        out["id_space"] = ("probe_manifest_asg_<lang>.json's own numbering "
                           "-- the assignment bucket, not the plain "
                           "probe_manifest_<lang>.json space")
        out["tally"] = tally_sum
        out["probes"] = probes
        path = os.path.join(HERE, "op_units_asg_%s_verbatim.json" % lang)
        tmp = path + ".tmp"
        fh = open(tmp, "w")
        json.dump(out, fh, indent=1)
        fh.write("\n")
        fh.close()
        os.replace(tmp, path)
        written.append(path)
        print("  %-6s %5d probes  tally %s -> %s"
              % (lang, len(probes), tally_sum, path))
    if written:
        refuse_own_output_on_spelling_failure(written)
    return written


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--merge", action="store_true")
    ap.add_argument("--chunk", type=int, default=CHUNK)
    args = ap.parse_args()
    if args.plan:
        state = plan(args.chunk)
        print("planned %d chunks over %d probes"
              % (state["totals"]["chunks"], state["totals"]["probes"]))
        return 0
    if args.run:
        run()
        return 0
    if args.status:
        status()
        return 0
    if args.merge:
        merge()
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
