#!/usr/bin/env python3
"""canon38_regen.py -- TASK 52 (round 11), the REGENERATED population (the 29,288
accepted probes of log_131) put through the memory-wrapped form.

THE FORM is ledger48.py's and THE GATE is canon38_gate.py's, imported
rather than copied so they cannot drift between populations.

WHAT IS DIFFERENT ABOUT THIS POPULATION, stated rather than assumed.
These units have never been canonicalized.  `trickle_store/
op_units2_<lang>_<chunk>.json` carries, per accepted probe, the SHIP
mnemonics, the ANCHOR mnemonics and the DWARF parameter table, and
nothing else.  So:

  * the body is the unit's OWN SHIP TEXT, which is exactly what
    ruling 1 asks for -- the compiler's own instructions, verbatim;
  * the arrival contract is INFERRED from that text: the arrival
    lineages are the families the text reads before it writes them;
  * the answer home is read off the same ship text by
    canon10_behaviour_check.answer_home_from_real;
  * there is therefore ONE gate, and it is the direct ship gate.

CHECKPOINTING AND RESUME.  Work is per CHUNK FILE, the unit the
trickle itself used.  `canon38_regen_state.json` records, per chunk,
`done` with its tally; a re-run skips every chunk marked done, so an
interrupted lap resumes at a chunk boundary and never redoes finished
work.  Per-chunk results are written to `canon38_regen_store/<chunk
file name>`, one file per chunk.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation).  No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns.  The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label
on the member.  HISTORY OF VIOLATIONS, so the pattern is visible: (1)
the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25
-- the fix brief itself reintroduced it as "same-operator pairs").
MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste
this paragraph verbatim."

The selection here is the chunk files on disk; the operator token is
carried once per record as a display label and is read by nothing.

usage:
  canon38_regen.py --run [--chunks N] [--seconds S]
  canon38_regen.py --status
"""

import argparse
import glob
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon10_behaviour_check as BC10                           # noqa: E402
import canon33_gate as G33                                       # noqa: E402
import canon36_universal as U36                                  # noqa: E402
import canon38_gate as GATE                                      # noqa: E402
import ledger48 as L48                                           # noqa: E402

STORE = os.path.join(HERE, "trickle_store")
OUT_DIR = os.path.join(HERE, "canon38_regen_store")
STATE = os.path.join(HERE, "canon38_regen_state.json")


def read_state():
    if not os.path.exists(STATE):
        return {"chunks": {}}
    return json.load(open(STATE))


def write_state(state):
    handle = open(STATE, "w")
    json.dump(state, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()


def chunk_files():
    return sorted(glob.glob(os.path.join(STORE, "op_units2_*.json")))


def gate_ship(ship_lines, wrapped_lines, ledger_rows, families,
              entry_contract, out_row):
    home, width = BC10.answer_home_from_real(ship_lines)
    if home is None:
        if entry_contract.get("a") is not None:
            home = entry_contract.get("a")
            width = 64
    if home is None:
        return ("UNDECIDED",
                "the unit's own ship code writes no answer home this "
                "checker can name and its contract names no arrival")
    order_real = G33.rip_order_data_only(ship_lines)
    order_cand = G33.rip_order_data_only(wrapped_lines)
    if order_real != order_cand:
        return ("UNDECIDED",
                "the narrowed rip-relative constant guard refused: the "
                "ship text loads data constants at %r, the wrapped text "
                "at %r" % (order_real, order_cand))
    seed = {}
    GATE.bind_arrival(seed, ledger_rows, families)
    return GATE.compare(ship_lines, wrapped_lines, seed, home, width,
                        out_row, "the unit's own ship code")


def process_probe(lang, key, probe):
    label = "%s/regen_%s" % (lang, key)
    meta = probe.get("meta") or {}
    record = {
        "unit": label,
        "lang": lang,
        "n": key,
        "population": "regenerated",
        "operator": meta.get("operator"),
        "body_source": "the unit's own ship text",
    }
    ship = probe.get("ship") or {}
    mnem = ship.get("mnem")
    if not mnem:
        record["outcome"] = "REFUSED"
        record["refusal_cause"] = "no ship text"
        record["refusal"] = ("this probe's record carries no ship "
                             "mnemonics, so there is no body to wrap")
        return record
    body_text = "; ".join(mnem)
    record["body_text"] = body_text
    raw_bytes = ship.get("bytes")
    body_bytes = None
    if raw_bytes:
        body_bytes = " ".join(raw_bytes)
        record["body_bytes"] = body_bytes
    entry_contract = GATE.arrival_contract(lang, body_text)
    record["entry_contract"] = entry_contract
    record["entry_contract_source"] = (
        "read off the unit's own ship text, in %s's own "
        "argument-register order: a family arrives when the text reads "
        "it before it writes it" % lang)
    ship_lines = L48.split_lines(body_text)
    home, width = BC10.answer_home_from_real(ship_lines)
    if home is None:
        home = entry_contract.get("a")
        width = 64
    record["result_family"] = home
    record["result_width"] = width
    families = GATE.arrival_family_list(entry_contract)
    try:
        fields = L48.wrap_unit(body_text, families, home, width,
                               body_bytes)
    except L48.Refusal as bad:
        record["outcome"] = "REFUSED"
        record["refusal_cause"] = bad.cause
        record["refusal"] = bad.detail
        return record
    wrapped_lines = L48.split_lines(fields["wrapped_text_resolved"])
    verdict, detail = gate_ship(ship_lines, wrapped_lines,
                                fields["ledger"], families,
                                entry_contract, fields["out_row"])
    if verdict == "UNDECIDED":
        ok, note = GATE.structural_route(fields)
        if ok:
            verdict = "PROVED_BY_CONSTRUCTION"
            detail = ("equivalence is forced by construction: the "
                      "wrapped text carries this unit's own ship body "
                      "character-for-character, on the register state "
                      "the prelude establishes from the input rows")
            fields["structural_route_checks"] = note
        else:
            fields["structural_route_refusal"] = note
    record.update(fields)
    record["verdict"] = verdict
    record["verdict_detail"] = detail
    if verdict in ("PROVED_EQUAL", "PROVED_BY_CONSTRUCTION"):
        record["outcome"] = "WRAPPED_TEXT_PROVED"
    elif verdict == "DISPROVED":
        record["outcome"] = "GATE_DISPROVED"
    else:
        record["outcome"] = "GATE_UNDECIDED"
    return record


def run_chunk(path):
    document = json.load(open(path))
    lang = document["language"]
    units = {}
    for key in sorted(document["probes"], key=lambda x: int(x)):
        probe = document["probes"][key]
        if probe.get("refused") is not None:
            continue
        if probe.get("ship") is None:
            continue
        label = "%s/regen_%s" % (lang, key)
        try:
            record = process_probe(lang, key, probe)
        except Exception as bad:                   # noqa: BLE001
            record = {
                "unit": label,
                "lang": lang,
                "n": key,
                "population": "regenerated",
                "outcome": "REFUSED",
                "refusal_cause": "renderer fault",
                "refusal": "%s: %s" % (type(bad).__name__, bad),
            }
        units[label] = record
    tally = {}
    for record in units.values():
        tally[record["outcome"]] = tally.get(record["outcome"], 0) + 1
    out = {
        "meta": {
            "generated_by": "canon38_regen.py",
            "form": "ledger48: the memory-wrapped form",
            "population": "regenerated",
            "source_chunk": os.path.basename(path),
            "note": "the operator field is a display label on the "
                    "member and is read by nothing",
        },
        "tally": tally,
        "units": units,
    }
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    handle = open(os.path.join(OUT_DIR, os.path.basename(path)), "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    return tally, len(units)


def status():
    state = read_state()
    files = chunk_files()
    done = 0
    total_units = 0
    tally = {}
    for path in files:
        name = os.path.basename(path)
        entry = state["chunks"].get(name)
        if entry is None:
            continue
        done = done + 1
        total_units = total_units + entry["units"]
        for key, value in entry["tally"].items():
            tally[key] = tally.get(key, 0) + value
    print("chunks %d of %d done, %d units, %s"
          % (done, len(files), total_units, json.dumps(tally,
                                                       sort_keys=True)))
    return 0


def run(limit_chunks, seconds):
    state = read_state()
    files = chunk_files()
    started = time.time()
    done_now = 0
    for path in files:
        name = os.path.basename(path)
        if name in state["chunks"]:
            continue
        if limit_chunks is not None:
            if done_now >= limit_chunks:
                break
        if seconds is not None:
            if time.time() - started > seconds:
                break
        tally, count = run_chunk(path)
        state["chunks"][name] = {"tally": tally, "units": count}
        write_state(state)
        done_now = done_now + 1
        sys.stderr.write("  %s %d units %s\n"
                         % (name, count, json.dumps(tally,
                                                    sort_keys=True)))
        sys.stderr.flush()
    return status()


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--chunks", type=int)
    parser.add_argument("--seconds", type=int)
    args = parser.parse_args(argv[1:])
    if args.status:
        return status()
    if args.run:
        return run(args.chunks, args.seconds)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
