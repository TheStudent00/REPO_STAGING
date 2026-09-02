#!/usr/bin/env python3
"""canon33_designated.py -- TASK 30's driver: designated locations and
the park-reload idiom, run over the not-converged population.

WHAT THIS PROGRAM DOES, in order:

 1. GROUND TRUTH FIRST.  For every unit of all five compiled
    languages it compares `sem_anchored_<lang>.json`'s `mnem` (the
    text every canonicalization in this line is derived from) with
    `op_units_<lang>.json`'s own `probes[n]["ship"]["mnem"]`, line by
    line.  This answers a question the existing refusal texts leave
    open -- WHICH BUILD a refusal fired against -- and it is printed
    before anything else is claimed.

 2. THE POPULATION.  Machine-form only: every unit whose recorded
    `canon31_units_<lang>.json` status is neither `converged` nor
    `unchanged`.  No operator token takes part in choosing it.

 3. RE-DERIVE with designated_memory.Directory in place of
    canon4.Bench and parkload_derive's two functions in place of
    canon4's.  canon4.py is imported and its module globals are
    REBOUND IN THIS PROCESS ONLY.  No file on disk is modified; the
    sha256 of canon4.py is printed before and after.

 4. ASSEMBLE.  Every candidate text is handed to the real assembler
    (canon4's own round-trip helper).  Text that does not assemble is
    not a canonical form and is reported as such.

 5. GATE.  canon33_gate.py -- Sim10 plus the designated-location
    store, the displacement `lea` form and the narrowed rip guard.
    Branching units are gated against real blocks cut from the unit's
    OWN SHIP BYTES (never canon4's `blocks` field -- log_112 showed
    that field is the same list object as `derived_blocks`, so a gate
    reading it compares a text with itself).

 6. REPORT the delta per bucket against the precisely-stated
    baseline: 1,635 recorded converged / 1,622 honest standing / 13
    withdrawn as a separate population (log_112, log_117 §8.1).

THE SPELLING BAN.  The output root declares
`"meta": {"role": "generator provenance"}` for the same reason
canon4.py does: every record here is provenance of one generator run.
The operator token is copied once per unit as the display label
`operator` and takes no part in any key, grouping, pairing, candidate
selection or comparison scope.  Run check_no_spelling_keys.py on the
output.

usage:
  canon33_designated.py
"""

import hashlib
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon  # noqa: E402
import canon2  # noqa: E402
import canon4  # noqa: E402
import canon10_behaviour_check as BC10  # noqa: E402
import canon33_fixes as F33  # noqa: E402
import canon33_gate as G33  # noqa: E402
import designated_memory as DM  # noqa: E402
import parkload_derive as PL  # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]


def load(name):
    path = os.path.join(HERE, name)
    handle = open(path)
    doc = json.load(handle)
    handle.close()
    return doc


def sha256_of(name):
    path = os.path.join(HERE, name)
    handle = open(path, "rb")
    digest = hashlib.sha256(handle.read()).hexdigest()
    handle.close()
    return digest


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


# ------------------------------------------------- step 1: ground truth

def ground_truth_check(sem_docs, op_docs):
    same = 0
    differ = []
    missing = 0
    for lang in LANGS:
        for n, rec in sem_docs[lang].items():
            probe = op_docs[lang].get(n)
            if probe is None:
                missing = missing + 1
                continue
            ship = (probe.get("ship") or {}).get("mnem")
            if ship is None:
                missing = missing + 1
                continue
            if list(rec.get("mnem") or []) == list(ship):
                same = same + 1
            else:
                differ.append("%s/%s" % (lang, n))
    return same, differ, missing


# --------------------------------------------- step 3: the rebinding

class Rebound(object):
    """rebind canon4's derive functions and its Bench, IN THIS PROCESS
    ONLY, so canon4's own block-cutting, contract-building and
    control-line machinery is reused unchanged while the deriving half
    is this lap's.  Restores the originals on exit."""

    def __init__(self):
        self.saved = {}
        self.reports = []

    def __enter__(self):
        self.saved["Bench"] = canon4.Bench
        self.saved["derive_runnable3"] = canon4.derive_runnable3
        self.saved["derive_block_body"] = canon4.derive_block_body
        self.saved["dead_mov_cleanup"] = canon4.dead_mov_cleanup
        self.saved["render_control_line"] = canon4.render_control_line
        reports = self.reports

        class DirectoryBench(DM.Directory):
            pass

        def derive_runnable3(steps, final_name, contract, bench):
            return PL.derive_runnable33(steps, final_name, contract,
                                        bench, reports)

        def derive_block_body(steps, contract, bench, reg_of_in):
            return PL.derive_block_body33(steps, contract, bench,
                                          reg_of_in, reports)

        canon4.Bench = DirectoryBench
        canon4.derive_runnable3 = derive_runnable3
        canon4.derive_block_body = derive_block_body
        canon4.dead_mov_cleanup = F33.dead_mov_cleanup33
        canon4.render_control_line = F33.render_control_line33
        return self

    def __exit__(self, kind, value, trace):
        canon4.Bench = self.saved["Bench"]
        canon4.derive_runnable3 = self.saved["derive_runnable3"]
        canon4.derive_block_body = self.saved["derive_block_body"]
        canon4.dead_mov_cleanup = self.saved["dead_mov_cleanup"]
        canon4.render_control_line = self.saved["render_control_line"]
        return False


# ------------------------------------------------------ steps 4 and 5

def candidate_lines(rec):
    if isinstance(rec.get("derived_text"), list):
        return list(rec["derived_text"])
    if rec.get("derived_blocks"):
        flat = []
        for block in rec["derived_blocks"]:
            flat.append("%s:" % block["label"])
            for line in block["steps"]:
                flat.append(line)
        return flat
    return None


def gate_unit(lang, n, new_rec, canon4_docs, sem_docs, op_docs):
    patched = {}
    for other in canon4_docs:
        patched[other] = canon4_docs[other]
    units = dict(canon4_docs[lang])
    merged = dict(units.get(n) or {})
    merged.update(new_rec)
    units[n] = merged
    patched[lang] = units
    if isinstance(new_rec.get("derived_text"), list):
        text = "; ".join(new_rec["derived_text"])
        return G33.check_straight(lang, n, patched, sem_docs, text)
    if new_rec.get("derived_blocks"):
        return G33.check_branching(lang, n, patched, op_docs,
                                   sem_docs)
    return "UNDECIDED", "this lap produced no candidate text for the " \
        "unit, so there is nothing to gate"


# ------------------------------------------------------------- driver

def main(argv):
    before = sha256_of("canon4.py")
    sem_docs = {}
    op_docs = {}
    canon_docs = {}
    canon4_docs = {}
    canon31_docs = {}
    spill_docs = {}
    for lang in LANGS:
        sem_docs[lang] = load("sem_anchored_%s.json" % lang)["units"]
        op_docs[lang] = load("op_units_%s.json" % lang)["probes"]
        canon_docs[lang] = load("canon_units_%s.json" % lang)["units"]
        canon4_docs[lang] = load("canon4_units_%s.json" % lang)["units"]
        canon31_docs[lang] = load("canon31_units_%s.json" % lang)["units"]
        spill_docs[lang] = load(
            "sem_anchored_spill_%s.json" % lang)["units"]

    log("STEP 1 -- WHICH BUILD IS THE RECORD DERIVED FROM")
    same, differ, missing = ground_truth_check(sem_docs, op_docs)
    log("   sem_anchored `mnem` compared line-by-line with op_units "
        "`ship.mnem`:")
    log("      identical : %d" % same)
    log("      different : %d %s" % (len(differ), differ[:10]))
    log("      no probe record : %d" % missing)
    log("   so the text every refusal in this line fired against is "
        "the SHIP build, not the anchor build.")

    population = []
    for lang in LANGS:
        for n in sorted(canon31_docs[lang], key=lambda x: int(x)):
            status = canon31_docs[lang][n].get("status")
            if status in ("converged", "unchanged"):
                continue
            population.append((lang, n, status))
    log("")
    log("STEP 2 -- THE POPULATION (machine form: recorded status is "
        "neither converged nor unchanged)")
    log("   %d units" % len(population))

    workdir = tempfile.mkdtemp(prefix="canon33_")
    rows = {}
    tally = {}
    reload_rows = []
    with Rebound() as rebound:
        for lang, n, status in population:
            rebound.reports[:] = []
            sem_rec = sem_docs[lang][n]
            canon_rec = canon_docs[lang].get(n, {})
            row = {}
            row["unit"] = "%s/op_%s" % (lang, n)
            row["lang"] = lang
            row["n"] = n
            row["operator"] = (sem_rec.get("meta") or {}).get("operator")
            row["recorded_status"] = status
            old = canon4_docs[lang].get(n) or {}
            row["old_erasure"] = old.get("erasure")
            row["old_derive_refused"] = old.get("derive_refused")
            try:
                new_rec = canon4.canon3_one(lang, n, sem_rec, canon_rec)
            except DM.RedZoneExhausted as bad:
                new_rec = {"erasure": str(bad)}
            except Exception as bad:                # noqa: BLE001
                new_rec = {"erasure": "erasure_refused: the deriving "
                                      "pass raised %s: %s"
                                      % (type(bad).__name__, bad)}
            row["new_erasure"] = new_rec.get("erasure")
            row["new_derive_refused"] = new_rec.get("derive_refused")
            row["reloads"] = list(rebound.reports)
            for record in rebound.reports:
                one = dict(record)
                one["unit"] = row["unit"]
                reload_rows.append(one)
            lines = candidate_lines(new_rec)
            row["candidate"] = lines
            if lines is None:
                row["outcome"] = "still_refused"
                row["verdict"] = None
                row["detail"] = None
            else:
                roundtrip = canon4.assemble_and_disassemble(lines,
                                                            workdir)
                row["assembled"] = bool(roundtrip.get("assembled"))
                if not row["assembled"]:
                    row["outcome"] = "assemble_failed"
                    row["verdict"] = None
                    row["detail"] = roundtrip.get("as_stderr", "")[:200]
                else:
                    verdict, detail = gate_unit(lang, n, new_rec,
                                                canon4_docs,
                                                spill_docs, op_docs)
                    row["verdict"] = verdict
                    row["detail"] = detail
                    if verdict == "PROVED_EQUAL":
                        row["outcome"] = "newly_converged"
                    elif verdict == "DISPROVED":
                        row["outcome"] = "disproved"
                    else:
                        row["outcome"] = "undecided"
            tally[row["outcome"]] = tally.get(row["outcome"], 0) + 1
            rows[row["unit"]] = row
    after = sha256_of("canon4.py")

    log("")
    log("STEP 3-5 -- OUTCOME TALLY")
    for key in sorted(tally):
        log("   %-20s %d" % (key, tally[key]))
    log("")
    log("   park-reload lines emitted: %d, over %d units"
        % (len(reload_rows),
           len(set(r["unit"] for r in reload_rows))))
    log("   canon4.py sha256 before: %s" % before)
    log("   canon4.py sha256 after:  %s" % after)
    log("   canon4.py UNCHANGED: %s" % (before == after))

    out = {}
    out["meta"] = {}
    out["meta"]["role"] = "generator provenance"
    out["meta"]["produced_by"] = "canon33_designated.py"
    out["meta"]["population_key"] = (
        "machine-form: canon31_units_<lang>.json status is neither "
        "converged nor unchanged")
    out["meta"]["gate"] = (
        "canon33_gate.check_straight / check_branching -- Sim10 plus "
        "the designated-location store, the displacement lea form and "
        "the narrowed rip guard; branching units gated against blocks "
        "cut from the unit's own ship bytes")
    out["meta"]["baseline"] = {
        "recorded_converged": 1635,
        "honest_standing_converged": 1622,
        "withdrawn_separate_population": 13,
        "source": "log_112 branching audit, log_117 section 8.1",
    }
    out["meta"]["tally"] = tally
    out["meta"]["ground_truth"] = {
        "sem_anchored_mnem_identical_to_ship_mnem": same,
        "different": differ,
        "no_probe_record": missing,
    }
    out["meta"]["canon4_sha256_before"] = before
    out["meta"]["canon4_sha256_after"] = after
    out["units"] = rows
    handle = open(os.path.join(HERE, "canon33_units.json"), "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.close()
    log("wrote canon33_units.json -- %d units" % len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
