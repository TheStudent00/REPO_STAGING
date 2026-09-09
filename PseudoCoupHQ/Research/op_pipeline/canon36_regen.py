#!/usr/bin/env python3
"""canon36_regen.py -- TASK 43, the REGENERATED population (the 29,288
accepted probes of log_131) rendered into the region form.

THE FORM is region36.py's; THE RENDERER and THE GATE are
canon36_universal.py's, imported rather than copied so they cannot
drift between populations.

WHAT IS DIFFERENT ABOUT THIS POPULATION, stated rather than assumed.
These units have never been canonicalized: `trickle_store/
op_units2_<lang>_<chunk>.json` carries, per accepted probe, the SHIP
mnemonics, the ANCHOR mnemonics and the DWARF parameter table, and
nothing else.  So:

  * the text rendered is the unit's OWN SHIP TEXT, not a canonical
    text (there is none);
  * the entry contract is INFERRED from that text -- the arrival
    lineages are the families the text reads before it writes them;
  * the answer home is read off the same ship text by
    canon10_behaviour_check.answer_home_from_real, which is the
    ground truth this population has;
  * there is therefore ONE gate, and it is the direct ship gate: the
    value the region form leaves in the RESULT BLOCK against the value
    the unit's own ship code leaves in its answer home, for every
    value of every input block.  That is exactly the brief's
    obligation ("gate-prove against each unit's OWN ship code under
    the arrival contract").

CHECKPOINTING AND RESUME.  Work is per CHUNK FILE, which is the unit
the trickle itself used.  `canon36_regen_state.json` records, per
chunk, `done` with its tally; a re-run skips every chunk marked done,
so an interrupted lap resumes at a chunk boundary and never redoes
finished work.  Per-chunk results are written to
`canon36_regen_store/<chunk file name>`, one file per chunk, so no
single artifact has to be rewritten as the population grows.

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
  canon36_regen.py --run [--chunks N]
  canon36_regen.py --status
"""

import argparse
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon10_behaviour_check as BC10                           # noqa: E402
import canon33_gate as G33                                       # noqa: E402
import canon36_universal as U36                                  # noqa: E402
import region36 as R36                                           # noqa: E402

STORE = os.path.join(HERE, "trickle_store")
OUT_DIR = os.path.join(HERE, "canon36_regen_store")
STATE = os.path.join(HERE, "canon36_regen_state.json")


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


def gate_ship(ship_lines, region_lines, directory, families,
              entry_contract):
    """the one gate for this population."""
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
    order_cand = G33.rip_order_data_only(region_lines)
    if order_real != order_cand:
        return ("UNDECIDED",
                "the narrowed rip-relative constant guard refused: the "
                "ship text loads data constants at %r, the region text "
                "at %r" % (order_real, order_cand))
    seed = {}
    U36.bind_region(seed, directory, families)
    return U36.compare(ship_lines, region_lines, seed, home, width,
                       "the unit's own ship code")


def process(lang, key, probe):
    label = "%s/regen_%s" % (lang, key)
    ship = probe.get("ship") or {}
    mnem = ship.get("mnem")
    record = {
        "unit": label,
        "lang": lang,
        "n": key,
        "population": "regenerated",
        "operator": (probe.get("meta") or {}).get("operator"),
        "operator_unit_id": (probe.get("meta") or {}).get(
            "operator_unit_id"),
        "ship_text": None if not mnem else "; ".join(mnem),
    }
    if not mnem:
        record["outcome"] = "REFUSED"
        record["refusal_cause"] = "no ship text"
        record["refusal"] = ("this accepted probe carries no ship "
                             "mnemonics, so there is nothing to render")
        return record
    ship_text = "; ".join(mnem)
    entry_contract = U36.infer_entry_contract(ship_text)
    source = ("inferred from the unit's own ship text: this population "
              "has no canonical record, so the arrival lineages are "
              "the families the text reads before it writes them")
    if entry_contract.get("a") is None:
        # THE READ-BEFORE-WRITE TEST FINDS NOTHING.  Measured at first
        # observation: 122 of one chunk's 130 units, all of them wide
        # float forms whose ship code loads a constant into %xmm1 and
        # tail-jumps into a runtime routine, so no argument register is
        # ever read in this text at all.  The fallback seats the
        # arrivals by the recorded ARITY of the probe -- machine-form
        # provenance from the generator, never a token -- on the
        # ordinary System V seats, choosing the register file by which
        # file the text uses.  It is a FALLBACK and it is recorded as
        # one; the gate still has to prove it.
        arity = (probe.get("meta") or {}).get("arity")
        vector = "%xmm" in ship_text
        entry_contract = dict(entry_contract)
        entry_contract["a"] = "xmm0" if vector else "rdi"
        if arity == "binary":
            entry_contract["b"] = "xmm1" if vector else "rsi"
        source = ("seated by the recorded arity on the ordinary System "
                  "V seats: this unit's own ship text reads no argument "
                  "register before writing one, so the read-before-"
                  "write test names no arrival")
    record["entry_contract"] = entry_contract
    record["entry_contract_source"] = source
    ship_lines = [line.strip() for line in mnem]
    home, home_width = BC10.answer_home_from_real(ship_lines)
    if home is None:
        home = entry_contract.get("a")
        home_width = 64
    attempts = []
    chosen = None
    for materialize in (True, False):
        fields, refusal = U36.render(entry_contract, ship_text, [],
                                     materialize, home, home_width)
        if refusal is not None:
            record["outcome"] = "REFUSED"
            record["refusal_cause"] = refusal[0]
            record["refusal"] = refusal[1]
            return record
        region_lines = U36.split_lines(fields["universal_text"])
        families = U36.arrival_family_list(entry_contract)
        verdict, detail = gate_ship(ship_lines, region_lines,
                                    fields["block_directory"], families,
                                    entry_contract)
        if verdict == "UNDECIDED":
            ok, note = U36.structural_route(fields, ship_text)
            if ok:
                verdict = "PROVED_BY_CONSTRUCTION"
                detail = ("equivalence is forced by construction: the "
                          "region text executes this unit's own ship "
                          "instruction sequence under an injective "
                          "register permutation, on the register state "
                          "the standardized loads establish from the "
                          "input blocks")
                fields["structural_route_checks"] = note
            else:
                fields["structural_route_refusal"] = note
        attempts.append({
            "constant_materialization":
                fields["constant_materialization"],
            "verdict": verdict,
            "detail": detail,
        })
        if verdict in ("PROVED_EQUAL", "PROVED_BY_CONSTRUCTION"):
            chosen = (fields, verdict, detail)
            break
        if chosen is None:
            chosen = (fields, verdict, detail)
        if fields["constant_materialization"] == "reduced":
            break
    fields, verdict, detail = chosen
    record.update(fields)
    record["gate_attempts"] = attempts
    record["gate_ship_verdict"] = verdict
    record["gate_ship_detail"] = detail
    if verdict in ("PROVED_EQUAL", "PROVED_BY_CONSTRUCTION"):
        record["outcome"] = "REGION_TEXT_PROVED"
    elif verdict == "DISPROVED":
        record["outcome"] = "GATE_DISPROVED"
        record["universal_text"] = None
    else:
        record["outcome"] = "GATE_UNDECIDED"
        record["universal_text"] = None
    return record


def run_chunk(path):
    document = json.load(open(path))
    lang = document.get("language")
    units = {}
    tally = {}
    for key, probe in document.get("probes", {}).items():
        if "refused" in probe:
            continue
        if not probe.get("ship"):
            continue
        try:
            record = process(lang, key, probe)
        except Exception as bad:                   # noqa: BLE001
            record = {
                "unit": "%s/regen_%s" % (lang, key),
                "lang": lang,
                "n": key,
                "population": "regenerated",
                "outcome": "REFUSED",
                "refusal_cause": "renderer fault",
                "refusal": "%s: %s" % (type(bad).__name__, bad),
            }
        units[record["unit"]] = record
        outcome = record["outcome"]
        tally[outcome] = tally.get(outcome, 0) + 1
    out = {
        "meta": {
            "role": "generator provenance",
            "generated_by": "canon36_regen.py",
            "source_chunk": os.path.basename(path),
            "form": "region36: the ruled virtual region, typed blocks "
                    "per lineage, no designated registers",
            "population": "regenerated",
            "note": "the operator field is a display label on the "
                    "member and is read by nothing",
        },
        "tally": tally,
        "units": units,
    }
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    target = os.path.join(OUT_DIR, os.path.basename(path))
    handle = open(target, "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    return tally, len(units)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--chunks", type=int)
    args = parser.parse_args(argv[1:])
    state = read_state()
    files = chunk_files()
    if args.status:
        total = {}
        done = 0
        units = 0
        for path in files:
            name = os.path.basename(path)
            record = state["chunks"].get(name)
            if record is None:
                continue
            done = done + 1
            units = units + record["units"]
            for key, value in record["tally"].items():
                total[key] = total.get(key, 0) + value
        print("chunks %d/%d  units %d  %s"
              % (done, len(files), units, json.dumps(total,
                                                     sort_keys=True)))
        return 0
    processed = 0
    for path in files:
        name = os.path.basename(path)
        if name in state["chunks"]:
            continue
        if args.chunks is not None:
            if processed >= args.chunks:
                break
        tally, count = run_chunk(path)
        state["chunks"][name] = {"tally": tally, "units": count}
        write_state(state)
        processed = processed + 1
        sys.stderr.write("%s  %d units  %s\n"
                         % (name, count, json.dumps(tally,
                                                    sort_keys=True)))
        sys.stderr.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
