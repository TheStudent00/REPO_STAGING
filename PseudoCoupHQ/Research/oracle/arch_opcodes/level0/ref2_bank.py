#!/usr/bin/env python3
"""ref2_bank.py -- the polyfill bank against a corrected reference: every
certificate stamped with the reference it was produced under, every
certificate whose cell's term text moved MARKED and never deleted, and the
loop's own re-attempt rule widened to include the reference.

WHAT THE OBJECTS ARE, one sentence each, in relation.
  * THE BANK is
    `emulation/autopoly/certificates.jsonl`: one certificate per (cell,
    target, written place, setter cell), carrying the term text it was posed
    on, the rendered source and its sha256, the compiler and its flags, the
    carved body, and the gate's verdict.
  * A CELL is one (`mnem`, operand shape, `key_width`) row of the arch-opcode
    model table, and its TERM is what `reference.py`'s builder puts in each
    place the opcode writes.
  * `reference_version` is the new field this task adds, authorised by its
    brief: the sha256 of `reference.py` and of `condition_table.py`, so a
    certificate says which reading of the machine it was produced under.
  * `reference_superseded` is the second field the brief names: true where
    the cell's term text under the corrected reference is not the text the
    certificate was posed on.  The certificate is KEPT: it is still the true
    record of what was proved about the old reading.
  * THE CODE VERSION is the loop's own re-attempt rule -- the sha256 of the
    driver, the loop and the target's renderer -- and an uncertified key is
    attempted again only when it moved.  This file widens that tuple with the
    reference's own two shas, by patching `autopoly.version_key` and
    `autopoly.code_version_of` IN THIS PROCESS.  Neither shared file is
    edited; making the widening permanent is one line in
    `autopoly.code_version_of` and is a flag for the coordinator, not a change
    this task makes.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope, anywhere in
this line -- not in matching, not in "which pairs get compared", not in report
rows, not in dropdowns.  The candidate set for comparison comes from
machine-form evidence (clusters, connections, type pairs) or from ratified
intention -- never from the token.  The token appears exactly once per unit:
as a display label on the member.  HISTORY OF VIOLATIONS, so the pattern is
visible: (1) the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25 -- the
fix brief itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse its own
output on failure.  A brief handed to any subagent for this line MUST paste
this paragraph verbatim."

Every key below is (mnem, operand shape, key_width, written place, setter
mnem) -- machine form, with the mnemonic in the field `mnem`, which the guard
reads as machine form under the ruling of 2026-09-08.

Coding discipline: no compound one-liner statements.

usage:
  ref2_bank.py mark          certificates.jsonl -> certificates_ref2.jsonl
  ref2_bank.py plan          the delta the widened rule would run, nothing run
  ref2_bank.py audit [<n>]   the bank-mode pass: every certificate re-derived
  ref2_bank.py readings      the three readings, before and after
"""

import hashlib
import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = os.path.abspath(os.path.join(HERE, "..", "..", "..",
                                        "op_pipeline"))
EMULATION = os.path.abspath(os.path.join(HERE, "..", "..",
                                         "cross_construction",
                                         "emulation"))
AUTOPOLY = os.path.join(EMULATION, "autopoly")
MODEL = os.path.abspath(os.path.join(HERE, "..", "model"))
ORIGINALS = os.path.join(HERE, "ref2_originals")

for _path in (PIPELINE, os.path.join(PIPELINE, "lean"), MODEL,
              AUTOPOLY, EMULATION, os.path.join(EMULATION, "handful"),
              os.path.join(EMULATION, "interp")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

BANK = os.path.join(AUTOPOLY, "certificates.jsonl")
NEW_BANK = os.path.join(AUTOPOLY, "certificates_ref2.jsonl")
SUMMARY = os.path.join(HERE, "ref2_bank_summary.json")
ROWS_BEFORE = os.path.join(HERE, "model_table_rows_ref2_before.json")
ROWS_AFTER = os.path.join(HERE, "model_table_rows_ref2_c4.json")

MEMORY_CEILING_KB = 12 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_REF2"


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    peak = peak_kb()
    if peak > MEMORY_CEILING_KB:
        raise SystemExit("%s: %d kB at %s, past the stated %d kB"
                         % (ABORT_NAME, peak, where, MEMORY_CEILING_KB))
    return peak


def digest_of(path):
    handle = open(path, "rb")
    text = handle.read()
    handle.close()
    return hashlib.sha256(text).hexdigest()


def reference_version(before=False):
    """the two shas that say which reading of the machine produced a
    certificate."""
    if before:
        return {"reference_py": digest_of(os.path.join(ORIGINALS,
                                                       "reference.py")),
                "condition_table_py":
                    digest_of(os.path.join(ORIGINALS,
                                           "condition_table.py"))}
    return {"reference_py": digest_of(os.path.join(PIPELINE,
                                                   "reference.py")),
            "condition_table_py":
                digest_of(os.path.join(PIPELINE, "condition_table.py"))}


def texts_of(path):
    """(mnem, shape, key_width, written place, setter mnem) -> the set of
    term texts that sweep gave it."""
    handle = open(path)
    document = json.load(handle)
    handle.close()
    out = {}
    for row in document["rows"]:
        setter = row.get("flags_in_setter")
        for entry in row.get("mapping") or []:
            key = (row["mnem"], row["shape"], row["key_width"],
                   entry["writes"], setter)
            out.setdefault(key, set()).add(entry.get("text"))
    document = None
    return out


def stream(path):
    handle = open(path)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        yield json.loads(text)
    handle.close()


def key_of(cert):
    cell = cert.get("cell") or {}
    setter = cert.get("setter") or {}
    return (cell.get("mnem"), cell.get("shape"), cell.get("key_width"),
            cert.get("place"), setter.get("mnem") or None)


def mark():
    """every certificate stamped, and the moved ones marked."""
    before = texts_of(ROWS_BEFORE)
    print("  the sweep before this task: %d (cell, place, setter) keys"
          % len(before))
    after = texts_of(ROWS_AFTER)
    print("  the sweep after it:         %d keys" % len(after))
    print("  peak resident so far: %d kB" % check_memory("the two sweeps"))
    old_version = reference_version(True)
    new_version = reference_version(False)
    counts = {}
    by_target = {}
    by_place = {}
    moved_keys = {}
    handle = open(NEW_BANK, "w")
    total = 0
    for cert in stream(BANK):
        total = total + 1
        cert["reference_version"] = old_version
        cert["reference_superseded"] = False
        text = cert.get("term_text")
        key = key_of(cert)
        if text is None:
            reading = "no term text: the run reached no place"
        elif key not in before and key not in after:
            reading = "the sweep holds no row at this key"
        elif text in after.get(key, set()):
            reading = "the cell's term text is unchanged"
        elif text in before.get(key, set()):
            reading = "the cell's term text MOVED"
            cert["reference_superseded"] = True
            moved_keys[key] = sorted(after.get(key, set()))
        else:
            reading = ("the certificate's term text is in neither "
                       "sweep at this key")
        counts[reading] = counts.get(reading, 0) + 1
        # THE BREAKDOWN IS NOT DECORATION.  Six certificates in ten
        # land in a bucket that is not a verdict about the correction,
        # and a count with no shape behind it cannot be read.  Both
        # keys below are machine form: a target's own name and a
        # written place.
        row = by_target.setdefault(cert.get("target"), {})
        row[reading] = row.get(reading, 0) + 1
        row = by_place.setdefault(cert.get("place"), {})
        row[reading] = row.get(reading, 0) + 1
        handle.write(json.dumps(cert, sort_keys=True) + "\n")
        if total % 5000 == 0:
            print("  [%d] %d kB" % (total, check_memory("marking")))
    handle.close()
    superseded = counts.get("the cell's term text MOVED", 0)
    document = {
        "what": ("every certificate of the bank stamped with the "
                 "reference version it was produced under, and marked "
                 "where the cell's term text moved under task ref2's "
                 "four corrections"),
        "bank_read": BANK,
        "bank_written": NEW_BANK,
        "certificates": total,
        "reference_version_before": old_version,
        "reference_version_after": new_version,
        "by_reading": counts,
        "by_target": by_target,
        "by_place": by_place,
        "certificates_marked_reference_superseded": superseded,
        "moved_keys": len(moved_keys),
        "moved_key_list": [{"mnem": k[0], "shape": k[1],
                            "key_width": k[2], "place": k[3],
                            "setter_mnem": k[4],
                            "term_text_after": moved_keys[k]}
                           for k in sorted(moved_keys, key=str)],
        "peak_resident_kb": peak_kb(),
        "memory_ceiling_kb": MEMORY_CEILING_KB,
        "named_abort": ABORT_NAME,
    }
    handle = open(SUMMARY, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    print("")
    print("| the certificate against the corrected sweep | certificates |")
    print("|---|---|")
    for reading in sorted(counts):
        print("| %s | %d |" % (reading, counts[reading]))
    print("")
    print("| target | %s |" % " | ".join(sorted(counts)))
    print("|---|%s" % ("---|" * len(counts)))
    for name in sorted(by_target, key=str):
        cells = []
        for reading in sorted(counts):
            cells.append("%d" % by_target[name].get(reading, 0))
        print("| `%s` | %s |" % (name, " | ".join(cells)))
    print("")
    print("| written place | %s |" % " | ".join(sorted(counts)))
    print("|---|%s" % ("---|" * len(counts)))
    for name in sorted(by_place, key=str):
        cells = []
        for reading in sorted(counts):
            cells.append("%d" % by_place[name].get(reading, 0))
        print("| `%s` | %s |" % (name, " | ".join(cells)))
    print("")
    print("certificates read %d, written %d, marked "
          "`reference_superseded` %d over %d distinct keys"
          % (total, total, superseded, len(moved_keys)))
    print("peak resident %d kB, ceiling %d kB, named abort %s"
          % (peak_kb(), MEMORY_CEILING_KB, ABORT_NAME))
    return 0


# ==================================================================
# the loop, with the reference in its re-attempt rule
# ==================================================================

def widen_the_code_version():
    """the loop's own version tuple, plus the reference's two shas.

    PATCHED IN THIS PROCESS AND NOWHERE ELSE.  `autopoly.code_version_of`
    answers the driver's, the loop's and the renderer's sha256, and
    `autopoly.version_key` compares exactly those three.  A correction to
    the REFERENCE moves neither, so without this the loop would hold back
    every key whose term this task changed.  Making it permanent is one
    line in `autopoly.code_version_of`, which this task is not authorised
    to write."""
    import autopoly as AP
    version = reference_version(False)
    original_of = AP.code_version_of
    original_key = AP.version_key

    def code_version_of(lang):
        out = dict(original_of(lang))
        out["reference_py"] = version["reference_py"]
        out["condition_table_py"] = version["condition_table_py"]
        return out

    def version_key(carried):
        base = original_key(carried)
        if base is None:
            return None
        return base + (carried.get("reference_py"),
                       carried.get("condition_table_py"))

    AP.code_version_of = code_version_of
    AP.version_key = version_key
    return AP


def plan():
    AP = widen_the_code_version()
    return AP.main(["--pass", "ref2", "--audit-share", "1",
                    "--bank", "preflight"])


def audit(limit):
    AP = widen_the_code_version()
    argv = ["--pass", "ref2", "--audit-share", "1", "--bank", "run"]
    if limit is not None:
        argv.append(str(limit))
    return AP.main(argv)


STANDING = os.path.join(AUTOPOLY, "certificates_ref2_standing.jsonl")


def standing():
    """the marked bank with every superseded certificate LEFT OUT.

    IT IS A VIEW, NOT A DELETION.  `certificates_ref2.jsonl` keeps every
    certificate the bank ever held, superseded ones included, and this
    file is that file minus the rows whose cell's term text moved -- so
    the three readings can be asked of what the bank still certifies
    ABOUT THE CORRECTED CELLS.  Nothing is removed from any bank."""
    kept = 0
    dropped = 0
    handle = open(STANDING, "w")
    for cert in stream(NEW_BANK):
        if cert.get("reference_superseded"):
            dropped = dropped + 1
            continue
        kept = kept + 1
        handle.write(json.dumps(cert, sort_keys=True) + "\n")
    handle.close()
    print("the standing view: %d certificates kept, %d left out "
          "because the cell's term text moved" % (kept, dropped))
    return 0


def readings(path):
    import bank as BK
    BK.BANK = path
    print("the three readings over %s" % os.path.basename(path))
    return BK.readings_command()


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    command = argv[1]
    if command == "mark":
        return mark()
    if command == "plan":
        return plan()
    if command == "audit":
        limit = None
        if len(argv) > 2:
            limit = int(argv[2])
        return audit(limit)
    if command == "standing":
        return standing()
    if command == "readings":
        path = BANK
        if len(argv) > 2:
            path = argv[2]
        return readings(path)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
