#!/usr/bin/env python3
"""canon38_wrapped.py -- TASK 52 (round 11): the memory-wrapped form over the
ORIGINAL population (the 1,779 compiled units).

THE FORM is ledger48.py's and THE GATE is canon38_gate.py's; read
those headers first.  This file is the driver.

WHICH TEXT IS THE BODY, stated rather than assumed.  Ruling 1 says
the compiler's body is kept verbatim, so the body is THE UNIT'S OWN
SHIP TEXT wherever the corpus records one -- that is literally what
the compiler emitted.  Where no ship text is recorded, the body is the
unit's newest canonical text, and the record says which was used in
`body_source`.

WHAT IS DONE PER UNIT

 1. Read the ARRIVAL CONTRACT: which register the compiler expects
    each input in.  It is taken from the recorded contract, then
    RECONCILED against the body's own text (the text outranks the
    record; the disagreement is recorded, never smoothed over).
 2. Read the ANSWER HOME off the unit's own ship text.
 3. Wrap: prelude (ledger -> those registers), body verbatim,
    epilogue (result register -> OUT-0).
 4. Build the PROVENANCE LEDGER by walking the body's dataflow.
 5. Gate.  GATE 2, the direct ship gate, is the admission gate: the
    value the wrapped text leaves in OUT-0 against the value the
    unit's own ship code leaves in its answer home, for every value of
    every input row.  GATE 1, against the unit's own prior canonical
    text, is run as a cross-check where such a text exists.
 6. Where the solver has no model for a mnemonic the body spells, the
    STRUCTURAL ROUTE decides -- a proof by construction that the body
    is present character-for-character and the plumbing cannot disturb
    it.

CHECKPOINTING.  Each language writes its own artifact every
CHECKPOINT_EVERY units; a re-run skips units already present, so an
interrupted lap resumes without redoing finished work.

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

The selection here is the corpus files on disk.  The operator token is
carried once per record as a display label and is read by nothing.

usage:
  canon38_wrapped.py --lang c [--limit N] [--fresh]
  canon38_wrapped.py --all
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon8_behaviour_check as BC8                             # noqa: E402
import canon10_behaviour_check as BC10                           # noqa: E402
import canon33_gate as G33                                       # noqa: E402
import canon36_universal as U36                                  # noqa: E402
import canon38_gate as GATE                                      # noqa: E402
import ledger48 as L48                                           # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]
CHECKPOINT_EVERY = 25


def out_path(lang):
    return os.path.join(HERE, "canon38_wrapped_%s.json" % lang)


def read_checkpoint(lang, fresh):
    path = out_path(lang)
    if fresh:
        return {}
    if not os.path.exists(path):
        return {}
    return json.load(open(path))["units"]


def tally_of(units):
    out = {}
    for record in units.values():
        key = record.get("outcome")
        out[key] = out.get(key, 0) + 1
    return out


def write_checkpoint(lang, units, tally):
    document = {
        "meta": {
            "generated_by": "canon38_wrapped.py",
            "form": "ledger48: the memory-wrapped form -- prelude from "
                    "the ledger into the compiler's own registers, "
                    "body verbatim, epilogue into OUT-0",
            "population": "the original corpus, %s" % lang,
            "note": "the operator field is a display label on the "
                    "member and is read by nothing",
        },
        "tally": tally,
        "units": units,
    }
    handle = open(out_path(lang), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()


def body_of(lang, n, canon4_docs, prior_text):
    """the compiler's own body: the ship text where one is recorded."""
    real_text = BC8.real_text_of(lang, n, canon4_docs)
    if real_text is not None:
        return real_text, "the unit's own real ship text"
    if prior_text:
        return prior_text, ("the unit's newest canonical text (no ship "
                            "text is recorded for it)")
    return None, None


def gate_one_unit(lang, n, canon4_docs, sem_docs, entry_contract,
                  fields, prior_text, body_text):
    home, width, home_source = GATE.answer_home_of(
        lang, n, canon4_docs, entry_contract, prior_text)
    families = fields["arrival_families"]
    wrapped_lines = L48.split_lines(fields["wrapped_text_resolved"])
    out_row = fields["out_row"]

    gate_ship = ("UNDECIDED",
                 "no real ship text is recorded for this unit")
    real_text = BC8.real_text_of(lang, n, canon4_docs)
    if real_text is not None:
        lines_real = [ln.strip() for ln in real_text.split(";")]
        order_real = G33.rip_order_data_only(lines_real)
        order_cand = G33.rip_order_data_only(wrapped_lines)
        if order_real != order_cand:
            gate_ship = ("UNDECIDED",
                         "the narrowed rip-relative constant guard "
                         "refused: the ship text loads data constants "
                         "at %r, the wrapped text at %r"
                         % (order_real, order_cand))
        else:
            home2, width2 = BC10.answer_home_from_real(lines_real)
            if home2 is None:
                home2 = home
                width2 = width
            if home2 is None:
                gate_ship = ("UNDECIDED",
                             "the unit's own ship code never writes an "
                             "answer home this checker can name")
            else:
                seed = BC10._prepare_seed(lang, n, sem_docs)
                GATE.bind_arrival(seed, fields["ledger"], families)
                gate_ship = GATE.compare(
                    lines_real, wrapped_lines, seed, home2, width2,
                    out_row, "the unit's own ship code")

    gate_prior = ("NOT_APPLICABLE",
                  "this unit has no prior canonical text to cross-check "
                  "against")
    if prior_text:
        if prior_text != body_text:
            seed = BC10._prepare_seed(lang, n, sem_docs)
            GATE.bind_arrival(seed, fields["ledger"], families)
            gate_prior = GATE.compare(
                L48.split_lines(prior_text), wrapped_lines, seed, home,
                width, out_row, "the unit's own prior canonical text")
        else:
            gate_prior = ("NOT_APPLICABLE",
                          "the prior canonical text is the body, so the "
                          "cross-check would be the ship gate again")

    seed_shape = {}
    bindings = GATE.bind_arrival(seed_shape, fields["ledger"], families)

    if gate_ship[0] == "PROVED_EQUAL":
        return ("PROVED_ON_SHIP", gate_ship[1], gate_prior, gate_ship,
                bindings, home_source)
    if gate_prior[0] == "PROVED_EQUAL":
        return ("PROVED_ON_PRIOR", gate_prior[1], gate_prior, gate_ship,
                bindings, home_source)
    if "DISPROVED" in (gate_ship[0], gate_prior[0]):
        which = gate_ship if gate_ship[0] == "DISPROVED" else gate_prior
        return ("DISPROVED", which[1], gate_prior, gate_ship, bindings,
                home_source)
    return ("UNDECIDED", "%s | %s" % (gate_ship[1], gate_prior[1]),
            gate_prior, gate_ship, bindings, home_source)


def process_unit(lang, n, rec31, c4, prior_text, prior_source,
                 canon4_docs, sem_docs, arrival):
    label = "%s/op_%s" % (lang, n)
    record = {
        "unit": label,
        "lang": lang,
        "n": n,
        "operator": rec31.get("operator"),
        "population": "original",
        "recorded_status": rec31.get("status"),
        "branch_kind": rec31.get("branch_kind"),
        "prior_text": prior_text,
        "prior_text_source": prior_source,
        "arrival_annotation": (arrival.get(label) or {}).get("mode"),
    }
    body_text, body_source = body_of(lang, n, canon4_docs, prior_text)
    record["body_source"] = body_source
    if body_text is None:
        record["outcome"] = "REFUSED"
        record["refusal_cause"] = "no text"
        record["refusal"] = ("no ship text and no canonical text exist "
                             "for this unit, so there is no body to "
                             "wrap")
        return record
    record["body_text"] = body_text
    record["body_bytes"] = c4.get("bytes")

    recorded_contract = c4.get("entry_contract")
    entry_contract = GATE.arrival_contract(lang, body_text)
    record["recorded_entry_contract"] = recorded_contract
    record["entry_contract"] = entry_contract
    record["entry_contract_source"] = (
        "read off the unit's own body, in %s's own argument-register "
        "order: a family arrives when the body reads it before it "
        "writes it" % lang)
    disagreement = GATE.contract_disagreement(recorded_contract,
                                              entry_contract)
    if disagreement is not None:
        record["entry_contract_disagreement"] = disagreement

    home, width, home_source = GATE.answer_home_of(
        lang, n, canon4_docs, entry_contract, prior_text)
    record["result_family"] = home
    record["result_width"] = width
    record["answer_home_source"] = home_source

    families = GATE.arrival_family_list(entry_contract)
    try:
        fields = L48.wrap_unit(body_text, families, home, width,
                               c4.get("bytes"))
    except L48.Refusal as bad:
        record["outcome"] = "REFUSED"
        record["refusal_cause"] = bad.cause
        record["refusal"] = bad.detail
        return record

    result = gate_one_unit(lang, n, canon4_docs, sem_docs,
                           entry_contract, fields, prior_text, body_text)
    verdict = result[0]
    if verdict == "UNDECIDED":
        ok, note = GATE.structural_route(fields)
        if ok:
            verdict = "PROVED_BY_CONSTRUCTION"
            fields["structural_route_checks"] = note
            result = (verdict,
                      "equivalence is forced by construction: the "
                      "wrapped text carries this unit's own body "
                      "character-for-character, on the register state "
                      "the prelude establishes from the input rows, "
                      "and stores the compiler's own result register "
                      "into %s immediately before every return"
                      % fields["out_row"],
                      result[2], result[3], result[4], result[5])
        else:
            fields["structural_route_refusal"] = note
    record.update(fields)
    record["verdict"] = verdict
    record["verdict_detail"] = result[1]
    record["gate_prior_verdict"] = result[2][0]
    record["gate_prior_detail"] = result[2][1]
    record["gate_ship_verdict"] = result[3][0]
    record["gate_ship_detail"] = result[3][1]
    record["arrival_contract_bindings"] = result[4]
    if verdict in ("PROVED_ON_SHIP", "PROVED_ON_PRIOR",
                   "PROVED_BY_CONSTRUCTION"):
        record["outcome"] = "WRAPPED_TEXT_PROVED"
    elif verdict == "DISPROVED":
        record["outcome"] = "GATE_DISPROVED"
    else:
        record["outcome"] = "GATE_UNDECIDED"
    return record


def run_language(lang, limit, fresh, c33, c32, gen_docs, arrival):
    canon4_docs = {}
    sem_docs = {}
    for other in LANGS:
        canon4_docs[other] = U36.load(
            "canon4_units_%s.json" % other)["units"]
        sem_docs[other] = U36.load(
            "sem_anchored_%s.json" % other)["units"]
    canon31 = U36.load("canon31_units_%s.json" % lang)["units"]
    units = read_checkpoint(lang, fresh)
    done = 0
    for n in sorted(canon31, key=lambda x: int(x)):
        label = "%s/op_%s" % (lang, n)
        if label in units:
            continue
        if limit is not None and done >= limit:
            break
        rec31 = canon31[n]
        c4 = canon4_docs[lang].get(n) or {}
        prior_text, prior_source = U36.newest_text_of(lang, n, c33, c32,
                                                      gen_docs)
        try:
            record = process_unit(lang, n, rec31, c4, prior_text,
                                  prior_source, canon4_docs, sem_docs,
                                  arrival)
        except Exception as bad:                   # noqa: BLE001
            record = {
                "unit": label,
                "lang": lang,
                "n": n,
                "population": "original",
                "operator": rec31.get("operator"),
                "outcome": "REFUSED",
                "refusal_cause": "renderer fault",
                "refusal": "%s: %s" % (type(bad).__name__, bad),
            }
        units[label] = record
        done = done + 1
        if done % CHECKPOINT_EVERY == 0:
            write_checkpoint(lang, units, tally_of(units))
            sys.stderr.write("  %s: %d done\n" % (lang, len(units)))
            sys.stderr.flush()
    write_checkpoint(lang, units, tally_of(units))
    return tally_of(units), len(units)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--fresh", action="store_true")
    args = parser.parse_args(argv[1:])
    c33, c32, gen_docs = U36.newest_text_sources()
    arrival = U36.load("canon33_arrival_modes.json")["compiled"]
    langs = LANGS if args.all else [args.lang]
    for lang in langs:
        tally, total = run_language(lang, args.limit, args.fresh, c33,
                                    c32, gen_docs, arrival)
        print("%-6s %4d units  %s"
              % (lang, total, json.dumps(tally, sort_keys=True)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
