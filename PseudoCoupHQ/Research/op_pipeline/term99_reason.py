#!/usr/bin/env python3
"""term99_reason.py -- record a `reason` on every NO_TERM record in
term66_store, derived from that record's OWN holes, grouped by CAUSE.

Node: hq.conventions / the operator-equivalence term walk (task 97/98
built the store; task 99 closes the recording gap the coordinator
found in log_204 -- every NO_TERM record has "outcome": null and
"reason": null, though its holes already carry a `why` string).

WHAT A NO_TERM RECORD IS
------------------------
A record in `term66_store/*.json` (`{"shard":..., "units": {id: rec}}`)
whose `term_state` is `"NO_TERM"`: the walk could not put this
arch-unit into z3 form.  It carries `holes` (each hole names a `block`,
a `row`, a `producer` and a `why` string) and often `cascades`
(secondary rows blocked by an earlier hole -- never a cause on their
own, so they are not read here).

WHAT "BY CAUSE, NOT BY SIGHTING" MEANS HERE
--------------------------------------------
The 485 NO_TERM records carry 3,259 holes.  Their `why` strings are
not 3,259 different sentences -- stripped of the callee name and the
row they name, they collapse onto a SMALL number of shared shapes.
This program strips exactly those two variable parts (never anything
else) and matches what remains against the shapes actually present in
the store, listing every shape it finds -- it does not assume the two
the coordinator's count happened to show first (cyclic callee body;
non-opcode phrase).  A `why` that matches none of the known shapes is
its own cause, named from its own text, and printed so a human sees a
shape this program did not anticipate -- it never guesses.

WHAT IS WRITTEN
----------------
For each NO_TERM record with `reason is None`:
  - "reason": "no term: <cause phrase[s]>; <k> hole(s) in <blocks>,
    producers <names>"
  - "reason_source": "term99_reason.py over the record's own holes"
No other field is read for writing, no other field is written, and no
record whose term_state != "NO_TERM" is touched.  Running twice changes
zero records on the second run (the `reason is None` guard).

MEMORY BOUND
------------
Streams shard by shard -- one shard's json loaded, reasoned over,
optionally rewritten, then dropped -- never the whole 99 MB store at
once.  Named abort `ABORT_MEMORY_T99` at 2,048 MB peak RSS, checked
after every shard with resource.getrusage (ru_maxrss is already a
running peak, not per-shard, but the check still fires promptly since
shards are processed one at a time and the bound is well above what
one shard plus the interpreter costs).

USAGE
-----
  python3 term99_reason.py --dry-run   # compute, print, write nothing
  python3 term99_reason.py --write     # compute, then rewrite shards
Both modes print `[i/total]` per shard and the final cause table, and
write term99_reason.json next to this file (the --dry-run run's table
is the one pasted in the log BEFORE any --write run happens).
"""

import argparse
import glob
import json
import os
import re
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STORE_GLOB = os.path.join(HERE, "term66_store", "*.json")
OUT_JSON = os.path.join(HERE, "term99_reason.json")

MEMORY_CEILING_MB = 2048
REASON_SOURCE = "term99_reason.py over the record's own holes"

# ---------------------------------------------------------------------------
# cause derivation
# ---------------------------------------------------------------------------

# Each entry: (cause_key, cause_phrase, a regex matched against the hole's
# `why` string after stripping quoted names).  Checked in order; first
# match wins.  `why` strings are stripped of `'...'` quoted names (callee
# spellings, register names) before matching, so the regex never has to
# name a specific callee -- that is exactly the strip §2.2 of the brief
# asks for ("what the why strings share once the callee name and row are
# stripped").
CAUSE_RULES = [
    ("cyclic_callee_body",
     "a cyclic callee body (its control flow transfers back to a block "
     "already on the walk, with no loop invariant invented)",
     re.compile(r"control flow has a cycle")),
    ("callee_no_reachable_return",
     "a callee body where every path leaves the unit or is unreachable, "
     "so the body leaves no answer to read",
     re.compile(r"leaves the unit or is unreachable")),
    ("callee_stack_depth_mismatch",
     "a callee body whose branches leave the machine stack at different "
     "depths",
     re.compile(r"different depths")),
    ("callee_no_attached_body",
     "a runtime callee with no attached body on this machine",
     re.compile(r"has no attached body on this machine")),
    ("hole_no_value_residence",
     "a hole row that names no place its value resides, so nothing "
     "downstream can read it",
     re.compile(r"names no place (its|no destination register)"
                 r"|no place its value resides")),
    ("non_opcode_phrase",
     "no arch opcode in the body writes the answer register (a "
     "non-opcode phrase stands in the OUT block)",
     re.compile(r"no arch opcode in this body writes the answer register")),
]


def strip_quoted(why):
    """Strip `'...'` quoted names -- callee spellings, register names --
    the two variable parts the brief says to strip before comparing
    `why` strings.  Nothing else is touched."""
    return re.sub(r"'[^']*'", "''", why)


def cause_of(why):
    stripped = strip_quoted(why)
    for key, phrase, rx in CAUSE_RULES:
        if rx.search(stripped):
            return key, phrase
    # Not one of the shapes seen so far in the store: its own cause,
    # named from its own (stripped) text so it is visible, never folded
    # into an existing one.
    key = "unclassified: " + stripped[:80]
    return key, "an unclassified hole shape: %r" % stripped


def producer_name(hole):
    p = hole.get("producer") or {}
    kind = p.get("kind", "?")
    if kind == "runtime_callee":
        return p.get("callee", "?")
    if kind == "flag_pair":
        return "flag_pair:" + "/".join(p.get("mnem") or [])
    if kind == "arch_opcode":
        return "arch_opcode:" + str(p.get("mnem", "?"))
    return kind


def reason_for(record):
    """(reason_text, cause_keys, cause_phrases) for one NO_TERM record,
    built only from its own `holes` -- cascades are never a cause, only
    a hole's own `why` is read."""
    holes = record.get("holes") or []
    if not holes:
        # No hole at all recorded -- the record's own `why_no_term` is
        # the only material left, read as one cause of its own text.
        why = record.get("why_no_term") or "no holes recorded"
        key, phrase = cause_of(why)
        return ("no term: %s; 0 hole(s) recorded on the record itself, "
                "producers (none)" % phrase, [key], [phrase])

    causes = []  # ordered, de-duplicated cause keys
    phrase_by_key = {}
    blocks = []
    producers = []
    for h in holes:
        why = h.get("why", "")
        key, phrase = cause_of(why)
        if key not in phrase_by_key:
            causes.append(key)
            phrase_by_key[key] = phrase
        blk = h.get("block")
        if blk and blk not in blocks:
            blocks.append(blk)
        prod = producer_name(h)
        if prod not in producers:
            producers.append(prod)

    cause_phrase = " and ".join(phrase_by_key[k] for k in causes)
    reason = ("no term: %s; %d hole(s) in %s, producers %s"
              % (cause_phrase, len(holes),
                 ", ".join(sorted(blocks)) or "(none named)",
                 ", ".join(sorted(producers))))
    return reason, causes, [phrase_by_key[k] for k in causes]


# ---------------------------------------------------------------------------
# store walk
# ---------------------------------------------------------------------------

def peak_rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def run(write, dry_run_note):
    shards = sorted(glob.glob(STORE_GLOB))
    total = len(shards)
    if total == 0:
        print("ABORT: no shards found at %s" % STORE_GLOB)
        sys.exit(2)

    cause_units = {}   # cause_phrase -> set of unit ids
    cause_example = {} # cause_phrase -> one unit id
    touched = 0
    already_had_reason = 0
    n_no_term = 0

    for i, path in enumerate(shards, 1):
        with open(path) as f:
            doc = json.load(f)
        units = doc.get("units", {})
        shard_touched = 0
        for uid, rec in units.items():
            if rec.get("term_state") != "NO_TERM":
                continue
            n_no_term += 1
            if rec.get("reason") is not None:
                already_had_reason += 1
                continue
            reason, cause_keys, cause_phrases = reason_for(rec)
            for phrase in dict.fromkeys(cause_phrases):
                cause_units.setdefault(phrase, set()).add(uid)
                cause_example.setdefault(phrase, uid)
            if write:
                rec["reason"] = reason
                rec["reason_source"] = REASON_SOURCE
            touched += 1
            shard_touched += 1

        if write and shard_touched:
            with open(path, "w") as f:
                json.dump(doc, f, indent=2, sort_keys=True)
                f.write("\n")

        rss = peak_rss_mb()
        print("[%d/%d] %s -- %d NO_TERM record(s) touched this shard "
              "(peak RSS so far %.1f MB)"
              % (i, total, os.path.basename(path), shard_touched, rss))
        sys.stdout.flush()
        if rss > MEMORY_CEILING_MB:
            print("ABORT_MEMORY_T99: peak RSS %.1f MB over the %d MB "
                  "ceiling, at shard %d/%d" % (rss, MEMORY_CEILING_MB, i, total))
            sys.exit(3)
        del doc, units

    print()
    print("mode: %s" % dry_run_note)
    print("NO_TERM records seen: %d" % n_no_term)
    print("already had a reason (skipped, idempotent): %d" % already_had_reason)
    print("records given a reason this run: %d" % touched)
    print()
    print("| cause | units | example unit |")
    print("|---|---:|---|")
    table_rows = []
    for phrase in sorted(cause_units, key=lambda p: -len(cause_units[p])):
        n = len(cause_units[phrase])
        ex = cause_example[phrase]
        print("| %s | %d | %s |" % (phrase, n, ex))
        table_rows.append({"cause": phrase, "units": n, "example_unit": ex})

    out_doc = {
        "generated_by": "term99_reason.py",
        "mode": dry_run_note,
        "no_term_total": n_no_term,
        "already_had_reason": already_had_reason,
        "touched_this_run": touched,
        "cause_table": table_rows,
    }
    with open(OUT_JSON, "w") as f:
        json.dump(out_doc, f, indent=2, sort_keys=True)
        f.write("\n")
    print()
    print("wrote %s" % OUT_JSON)
    return out_doc


def main(argv):
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true",
                    help="compute and print the table; write nothing to "
                         "the store (term99_reason.json is still written)")
    g.add_argument("--write", action="store_true",
                    help="compute AND rewrite each touched shard in place")
    args = ap.parse_args(argv)
    run(write=args.write, dry_run_note=("DRY-RUN, no shard written" if
                                         args.dry_run else "WRITE"))


if __name__ == "__main__":
    main(sys.argv[1:])
