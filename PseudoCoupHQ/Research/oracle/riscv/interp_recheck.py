#!/usr/bin/env python3
"""interp_recheck.py -- ONE INTERPRETER'S HANDFUL, RE-RUN, to show that an
`agreed` certificate transfers to riscv64 as it is.

Node: hq.research.arch_unit_oracle.  Task rv2, brief section 2 step 3's
last sentence, `PRIVATE/PseudoCoupHQ/Research/briefs/task_rv2_brief.md`.

WHAT THIS IS, one sentence, in relation: the evidence behind the claim
that an interpreted target's certificate needs no re-verification on a
second architecture -- a handful of cpython emulations run again, at
their own sample of values, against the term they are certified for.

THE CLAIM, stated plainly so it can be disagreed with: an `agreed`
certificate says "this SOURCE, run by this interpreter, answers what the
term says at every point of a sample".  The interpreter is a program; on
riscv64 it is the same program built for a different machine, and the
language's own arithmetic is defined by the language, not by the machine
underneath it.  So the certificate's claim does not mention the host
architecture and does not change with it.  What this file shows is the
weaker, checkable half: the same source, run again, still answers what
the term says.  It is a check at points, NOT a proof, exactly as the
original agreement was.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope, anywhere
in this line -- not in matching, not in "which pairs get compared", not in
report rows, not in dropdowns.  The candidate set for comparison comes from
machine-form evidence (clusters, connections, type pairs) or from ratified
intention -- never from the token.  The token appears exactly once per
unit: as a display label on the member.  HISTORY OF VIOLATIONS, so the
pattern is visible: (1) the arch campaign's cross-language matrix (caught
by the owner 2026-08-24); (2) verdicts.py's row pairing (caught by the owner
2026-08-25 -- the fix brief itself reintroduced it as "same-operator
pairs").  MECHANICAL GUARD REQUIRED: every pipeline stage that groups or
pairs units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste this
paragraph verbatim."

HOW THIS FILE OBEYS IT.  Which certificates are re-run is the first
`<n>` of the twinned cpython certificates in the bank's own order; the
sample points are built from the term's SYMBOL WIDTHS.  No token is read.

Coding discipline (the owner's ruling): no complex/compound one-liner statements.

usage:
  interp_recheck.py run <ref dir> <op dir> <x86 rows json> <twins.json>
                        <bank.jsonl> <src root> <out prefix> <n>
"""

import json
import os
import random
import resource
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import inherit as INH                                       # noqa: E402
import twins as TW                                          # noqa: E402
import z3                                                    # noqa: E402


ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_RV2"
POINTS = 200
SEED = "rv2"
TARGET = "cpython"


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def points_for(widths):
    """the edge values first, then points drawn by
    `random.Random("rv2")` -- the fuzz method's own shape, stated here
    rather than imported so this file's own claim is reproducible."""
    rng = random.Random(SEED)
    out = []
    for value in (0, 1, 2, 3):
        out.append(tuple([value % (1 << w) for w in widths]))
    for width in widths:
        top = (1 << width) - 1
        out.append(tuple([top % (1 << w) for w in widths]))
        out.append(tuple([(1 << (width - 1)) % (1 << w) for w in widths]))
        out.append(tuple([((1 << (width - 1)) - 1) % (1 << w)
                          for w in widths]))
    while len(out) < POINTS:
        out.append(tuple([rng.getrandbits(w) for w in widths]))
    return out[:POINTS]


def run_command(ref_dir, op_dir, rows_path, twins_path, bank_path,
                src_root, prefix, wanted):
    say("[0/3] the x86 reference this run uses")
    X86, TERMS, MT, MTAB, digest = TW.bring_in(ref_dir, op_dir)
    holder = TERMS.Term(X86.Reference())
    twinned = INH.twinned_cells(twins_path)
    records = INH.bank_lines(bank_path, twinned)
    chosen = []
    for record in records:
        if record["target"] != TARGET:
            continue
        chosen.append(record)
        if len(chosen) >= wanted:
            break
    say("[1/3] %d cpython certificates chosen of the twinned ones"
        % len(chosen))
    cells = TW.x86_cells(rows_path)
    rows = []
    say("[2/3] each one re-run at %d points" % POINTS)
    for record in chosen:
        rows.append(one(TERMS, MT, MTAB, holder, cells, record,
                        src_root))
        last = rows[-1]
        say("   %-10s %-14s %-4s %-10s  %s  %d/%d agree"
            % (last["cell"]["mnem"], last["cell"]["shape"],
               last["cell"]["key_width"], last["place"],
               last["outcome"], last["agreements"], last["points"]))
    say("[3/3] writing")
    total = 0
    agreed = 0
    for row in rows:
        total = total + row["points"]
        agreed = agreed + row["agreements"]
    document = {
        "meta": {
            "task": "rv2",
            "what": "a handful of cpython emulations run again at a "
                    "sample of points, against the term they are "
                    "certified for -- a check at points, not a proof",
            "target": TARGET,
            "points_per_certificate": POINTS,
            "point_seed": SEED,
            "certificates": len(rows),
            "points": total,
            "agreements": agreed,
            "disagreements": total - agreed,
            "peak_kb": peak_kb(),
            "memory_bound_kb": ABORT_KB,
            "memory_abort": ABORT_NAME,
        },
        "rows": rows,
    }
    INH.write_json(prefix + ".json", document)
    say("   %d certificates, %d points, %d agreements, %d disagreements"
        % (len(rows), total, agreed, total - agreed))
    return 0


def one(TERMS, MT, MTAB, holder, cells, record, src_root):
    cell = record["cell"]
    row = {"cell": dict(cell), "place": record["place"],
           "target": record["target"],
           "term_text": record.get("term_text"),
           "source": dict(record.get("source") or {}),
           "points": 0, "agreements": 0, "disagreements": 0}
    key = (cell["mnem"], cell["shape"], cell["key_width"])
    held = cells.get(key)
    if held is None:
        row["outcome"] = "NO_CELL"
        return row
    places = TW.rebuild(MT, MTAB, held)
    if record["place"] not in places:
        row["outcome"] = "NO_PLACE"
        return row
    term = TW.positional(TERMS, places[record["place"]])
    widths = TW.ordered_widths(TERMS, term)
    if widths is None:
        row["outcome"] = "NO_WIDTHS"
        return row
    path = resolve(src_root, row["source"].get("path") or "")
    if path is None:
        row["outcome"] = "SOURCE_NOT_ON_DISK"
        return row
    row["term_rebuilt"] = holder.normalize(places[record["place"]])
    if row["term_rebuilt"] != (record.get("term_text") or ""):
        row["outcome"] = "THE_CERTIFICATE_IS_ABOUT_A_RE_POSED_TERM"
        row["why"] = ("the certificate's own term is not this place's "
                      "whole term: the pipeline's gate re-poses a "
                      "vector place onto the LANE the operation writes "
                      "(`handful.projected_lane`) and renders the "
                      "emulation from that, so the source takes fewer "
                      "arguments than the whole place reads. Re-posing "
                      "a vector place is the driver's job and this file "
                      "does not restate it; the row is named rather "
                      "than counted as a disagreement.")
        return row
    bits = term.size()
    if record["place"].startswith("reg_xmm"):
        bits = cell["key_width"] or 64
        if bits > term.size():
            bits = term.size()
    row["compared_on_bits"] = bits
    row["comparison_note"] = ("a vector place is the whole 128-bit "
                              "register and the operation writes one "
                              "LANE of it, so a vector place is "
                              "compared on the cell's own key_width -- "
                              "the projection the pipeline's own gate "
                              "makes (`handful.projected_lane`); a "
                              "general-register place is compared "
                              "whole")
    sample = points_for(widths)
    feed = []
    for point in sample:
        feed.append(" ".join([str(value) for value in point]))
    process = subprocess.run(["python3", path],
                             input="\n".join(feed).encode("utf-8"),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, timeout=300)
    answers = process.stdout.decode("utf-8", "replace").split()
    row["runner"] = "python3 %s" % path
    row["outcome"] = "AGREES_AT_EVERY_POINT"
    row["unevaluated_note"] = ("a point where z3's own simplifier does "
                               "not put the term at a single numeral -- "
                               "a NaN has no one IEEE bit pattern in "
                               "z3's float theory -- is UNEVALUATED and "
                               "is dropped from both the numerator and "
                               "the denominator, which is the fuzz "
                               "census's own rule for a declined key")
    disagreements = []
    for index, point in enumerate(sample):
        row["points"] = row["points"] + 1
        expected = value_at(term, widths, point)
        if expected is not None:
            expected = expected & ((1 << bits) - 1)
        if index >= len(answers):
            row["disagreements"] = row["disagreements"] + 1
            disagreements.append({"point": list(point),
                                  "expected": str(expected),
                                  "answer": "NO_ANSWER"})
            continue
        got = answers[index]
        if expected is None:
            row["points"] = row["points"] - 1
            row["unevaluated"] = row.get("unevaluated", 0) + 1
            continue
        if got.isdigit() and \
                (int(got) & ((1 << bits) - 1)) == expected:
            row["agreements"] = row["agreements"] + 1
            continue
        row["disagreements"] = row["disagreements"] + 1
        if len(disagreements) < 3:
            disagreements.append({"point": list(point),
                                  "expected": str(expected),
                                  "answer": got})
    if row["disagreements"]:
        row["outcome"] = "DISAGREES"
        row["disagreement_examples"] = disagreements
    return row


def resolve(src_root, path):
    """where a certificate's source actually sits.

    The bank records a compiled target's source relative to the
    `autopoly/` folder (`src/...`) and an interpreted target's relative
    to the `emulation/` folder above it (`interp/src_ex1/...`), so both
    roots are tried and the one that exists is used."""
    if not path:
        return None
    here = os.path.join(src_root, path)
    if os.path.isfile(here):
        return here
    above = os.path.join(os.path.dirname(src_root.rstrip("/")), path)
    if os.path.isfile(above):
        return above
    return None


def value_at(term, widths, point):
    substitution = []
    for index, value in enumerate(point):
        symbol = z3.BitVec("v%d" % index, widths[index])
        substitution.append((symbol, z3.BitVecVal(value, widths[index])))
    got = term
    if substitution:
        got = z3.substitute(term, *substitution)
    got = z3.simplify(got)
    if z3.is_bv_value(got):
        return got.as_long()
    return None


def main():
    command = sys.argv[1]
    if command == "run":
        return run_command(sys.argv[2], sys.argv[3], sys.argv[4],
                           sys.argv[5], sys.argv[6], sys.argv[7],
                           sys.argv[8], int(sys.argv[9]))
    raise SystemExit("unknown command %r" % command)


if __name__ == "__main__":
    sys.exit(main())
