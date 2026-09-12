#!/bin/bash
# rd1 lane 5 -- the x86 bank's delta on go and swift for the divide family, the
# narrow widths first. Lane rd1_l3 ABORTED the whole run on the first swift
# compile that exceeded swift_render's own 600 s budget; here every (cell,
# language) pair is caught and its limit reported as a row, which is what task
# t4's own store already records for those same three pairs.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/rd1gocache GOPATH=/work/rd1gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rd1x2

cat > /work/rd1x2/x86.py <<'PYEOF'
"""the x86 divide family on go and swift: t4's store is the BEFORE, this
run is the AFTER, and the collapse column is beside t4's."""
import json
import os
import sys
import time

G = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general"
AUTOPOLY = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly"
sys.path.insert(0, G)

import general as GEN
import render_general as RGEN

STORE = os.path.join(AUTOPOLY, "t4_general_runs.jsonl")
TARGETS = ("go", "swift")


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def dividing(term):
    """MACHINE FORM: the term holds a node of z3's own division or
    remainder declaration kinds.  No mnemonic is read."""
    for node in RGEN.leaves_first(term):
        if node.decl().kind() in RGEN.DIVIDING_KINDS:
            return True
        continue
    return False


def the_family(H, cells):
    out = []
    for entry in cells["asked"]:
        key = (entry["asked"]["mnem"], entry["asked"]["shape"],
               entry["asked"]["key_width"])
        try:
            held = H.cell_input(cells, key)
        except Exception:                                     # noqa: BLE001
            continue
        for place in held.get("places") or []:
            term = place.get("term")
            if term is None:
                continue
            if dividing(term):
                out.append(key)
                break
            continue
        continue
    out.sort(key=lambda key: (key[2], key[0], key[1]))
    return out


def before_rows():
    held = {}
    for line in open(STORE):
        text = line.strip()
        if not text:
            continue
        row = json.loads(text)
        key = (row.get("mnem"), row.get("shape"), row.get("key_width"),
               row.get("lang"))
        if row.get("route") == "general":
            held[key] = row
            continue
        held.setdefault(key, row)
        continue
    return held


def attempt_reading(attempt):
    check = attempt.get("check") or {}
    gate = attempt.get("gate_on_the_written_term") or {}
    landing = attempt.get("landing") or {}
    outcome = check.get("outcome") or gate.get("outcome")
    if outcome is None:
        outcome = (attempt.get("refusal_cause")
                   or attempt.get("compile_refusal") or "no verdict")
    return {
        "policy": attempt.get("policy"),
        "statements": attempt.get("statements"),
        "instructions": attempt.get("instructions"),
        "outcome": ("%s" % outcome)[:70].replace("\n", " "),
        "landing": landing.get("verdict") or "NO LANDING RECORDED",
        "equality": (attempt.get("equality") or {}).get("outcome"),
    }


def before_by_policy(row):
    out = {}
    if row is None:
        return out
    for place in row.get("places") or []:
        for attempt in place.get("attempts") or []:
            reading = attempt_reading(attempt)
            out.setdefault((place.get("writes"), reading["policy"]),
                           reading)
            continue
        continue
    return out


def main():
    AP = GEN.configure_pass()
    GEN.SRC_DIR = os.path.join(AUTOPOLY, "src_rd1_x86")
    AP.SRC_DIR = GEN.SRC_DIR
    import handful as H
    import model_table as MTAB
    MTAB._install_gpr_widths()
    shared = H.build_shared()
    cells = AP.read_json(AP.CELLS)
    say("[2/2] the divide family, machine form, narrow widths first")
    family = the_family(H, cells)
    say("   the family: %d x86 cells whose term holds a division or "
        "remainder node" % len(family))
    for key in family:
        say("     %s %s %d" % key)
        continue
    before = before_rows()
    say("")
    say("| cell | place | language | route | t4 outcome | rd1 outcome "
        "| t4 collapse | rd1 collapse | t4 statements | rd1 statements "
        "| t4 instructions | rd1 instructions |")
    say("|---|---|---|---|---|---|---|---|---|---|---|---|")
    flags = []
    for key in family:
        for lang in TARGETS:
            was = before.get((key[0], key[1], key[2], lang))
            old_by = before_by_policy(was)
            started = time.time()
            made = None
            problem = None
            try:
                for held in H.cell_inputs(cells, key):
                    record = H.the_native_route(shared, held, lang)
                    made = GEN.general_tier(shared, held, lang, record)
                    break
            except Exception as raised:                       # noqa: BLE001
                problem = "%s: %s" % (type(raised).__name__,
                                      ("%s" % raised)[:200])
            if problem is not None:
                cause = (was or {}).get("refusal_detail")
                flags.append((key, lang, problem, cause))
                say("| `%s` `%s` %d | -- | %s | -- | %s | THE DRIVER "
                    "RAISED | -- | -- | -- | -- | -- | -- |"
                    % (key[0], key[1], key[2], lang,
                       ("%s" % (was or {}).get("refusal_cause"))[:50]))
                say("   the raise, LITERAL: %s   (%.0f s)"
                    % (problem, time.time() - started))
                continue
            if made is None:
                say("| `%s` `%s` %d | -- | %s | -- | %s | the tier "
                    "declined every place | -- | -- | -- | -- | -- | -- |"
                    % (key[0], key[1], key[2], lang,
                       ("%s" % (was or {}).get("refusal_cause"))[:50]))
                continue
            for place in made.get("places") or []:
                for attempt in place.get("attempts") or []:
                    now = attempt_reading(attempt)
                    old = old_by.get((place.get("writes"),
                                      now["policy"])) or {}
                    say("| `%s` `%s` %d | %s | %s | %s | %s | %s | %s | "
                        "%s | %s | %s | %s | %s |"
                        % (key[0], key[1], key[2], place.get("writes"),
                           lang, now["policy"],
                           old.get("outcome", "(no t4 row)"),
                           now["outcome"],
                           old.get("landing", "(no t4 row)"),
                           now["landing"],
                           old.get("statements", "--"),
                           now["statements"],
                           old.get("instructions", "--"),
                           now["instructions"]))
                    continue
                continue
            say("   %s %s %d on %s: %.0f s" % (key[0], key[1], key[2],
                                               lang,
                                               time.time() - started))
            continue
        continue
    say("")
    say("FLAGS -- every (cell, language) pair whose driver raised, with "
        "what task t4's own store records for the same pair")
    for key, lang, problem, cause in flags:
        say("   `%s` `%s` %d on %s" % (key[0], key[1], key[2], lang))
        say("      rd1, LITERAL: %s" % problem)
        say("      t4,  LITERAL: %s" % ("%s" % cause)[:200])
        continue
    say("")
    say("peak resident: %d kB" % GEN.peak_kb())
    return 0


if __name__ == "__main__":
    sys.exit(main())
PYEOF

echo "[1/2] the toolchains this lane compiles with"
(PATH=/persist/swift/usr/bin:$PATH swiftc --version 2>&1 | head -2) || true
go version || true

timeout 9000 python3 /work/rd1x2/x86.py
echo "  exit: $?"
