#!/usr/bin/env python3
"""trickle_report.py -- the per-chunk tallies of the regeneration trickle,
read straight out of the resume state.

Writes the full per-chunk table (one row per chunk, in the order the plan
lists them) and the per-language roll-up. Nothing is recomputed from the
stores: the state file is what the trickle banked, so this page and the
resume mechanism cannot disagree.

usage:
    /tmp/reconnect_venv/bin/python3 trickle_report.py
writes:
    trickle_tallies.md
    trickle_tallies.json
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]
FIELDS = ["submitted", "accepted", "refused", "extracted_ship",
          "extracted_anchor", "extracted_dwarf", "no_line"]


def build():
    state = json.load(open(os.path.join(HERE, "trickle_state.json")))
    per_lang = {}
    for lang in LANGS:
        per_lang[lang] = dict((f, 0) for f in FIELDS)
        per_lang[lang]["chunks_done"] = 0
        per_lang[lang]["chunks_planned"] = 0
        per_lang[lang]["probes_planned"] = 0
        per_lang[lang]["seconds"] = 0.0
    rows = []
    for chunk in state["chunks"]:
        lang = chunk["language"]
        per_lang[lang]["chunks_planned"] += 1
        per_lang[lang]["probes_planned"] += chunk["probes"]
        row = {"chunk_id": chunk["chunk_id"], "language": lang,
               "state": chunk["state"], "probes": chunk["probes"]}
        if chunk["state"] == "done":
            per_lang[lang]["chunks_done"] += 1
            per_lang[lang]["seconds"] += chunk.get("seconds") or 0.0
            for f in FIELDS:
                per_lang[lang][f] += chunk["tally"][f]
            row.update(chunk["tally"])
            row["seconds"] = chunk.get("seconds")
        rows.append(row)
    totals = dict((f, 0) for f in FIELDS)
    totals["chunks_done"] = 0
    totals["chunks_planned"] = 0
    totals["probes_planned"] = 0
    totals["seconds"] = 0.0
    for lang in LANGS:
        for key in totals:
            totals[key] += per_lang[lang][key]
    return state, rows, per_lang, totals


def markdown(state, rows, per_lang, totals):
    out = []
    out.append("# the regeneration trickle -- per-chunk tallies")
    out.append("")
    out.append("Read from `trickle_state.json`, which is also the resume "
               "state: a chunk marked done here is a chunk the trickle "
               "will not rerun.")
    out.append("")
    out.append("## per language")
    out.append("")
    out.append("| language | chunks done / planned | probes planned | "
               "submitted | accepted | refused | extracted (ship/anchor/"
               "dwarf) | lane seconds |")
    out.append("|---|---|---:|---:|---:|---:|---|---:|")
    for lang in LANGS:
        r = per_lang[lang]
        out.append("| %s | %d / %d | %d | %d | %d | %d | %d / %d / %d | "
                   "%.0f |"
                   % (lang, r["chunks_done"], r["chunks_planned"],
                      r["probes_planned"], r["submitted"], r["accepted"],
                      r["refused"], r["extracted_ship"],
                      r["extracted_anchor"], r["extracted_dwarf"],
                      r["seconds"]))
    out.append("| **total** | **%d / %d** | **%d** | **%d** | **%d** | "
               "**%d** | **%d / %d / %d** | **%.0f** |"
               % (totals["chunks_done"], totals["chunks_planned"],
                  totals["probes_planned"], totals["submitted"],
                  totals["accepted"], totals["refused"],
                  totals["extracted_ship"], totals["extracted_anchor"],
                  totals["extracted_dwarf"], totals["seconds"]))
    out.append("")
    out.append("## per chunk")
    out.append("")
    out.append("| chunk | state | probes | submitted | accepted | refused | "
               "extracted ship | seconds |")
    out.append("|---|---|---:|---:|---:|---:|---:|---:|")
    for row in rows:
        if row["state"] != "done":
            out.append("| `%s` | %s | %d | | | | | |"
                       % (row["chunk_id"], row["state"], row["probes"]))
            continue
        out.append("| `%s` | done | %d | %d | %d | %d | %d | %.1f |"
                   % (row["chunk_id"], row["probes"], row["submitted"],
                      row["accepted"], row["refused"],
                      row["extracted_ship"], row["seconds"] or 0.0))
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
    state, rows, per_lang, totals = build()
    doc = {"generated_by": "trickle_report.py",
           "reads": ["trickle_state.json"],
           "per_language": per_lang, "totals": totals, "per_chunk": rows}
    p1 = os.path.join(HERE, "trickle_tallies.json")
    fh = open(p1, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()
    p2 = os.path.join(HERE, "trickle_tallies.md")
    text = markdown(state, rows, per_lang, totals)
    open(p2, "w").write(text)
    print("\n".join(text.split("\n")[:20]))
    print("wrote %s" % p1)
    print("wrote %s" % p2)
    refuse_own_output_on_spelling_failure([p1])


if __name__ == "__main__":
    main()
