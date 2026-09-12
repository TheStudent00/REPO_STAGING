#!/bin/bash
# rd1 lane 3 -- the x86 bank's delta on go and swift for the divide family.
# The same render serves x86 (general.py's pass), so the guarded conditional
# must be measured there too: t4's own rows are the BEFORE, this lane's run of
# the same cells is the AFTER, and the collapse column is reported beside t4's.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/rd1gocache GOPATH=/work/rd1gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rd1x

echo "[1/2] the swift and go toolchains this lane compiles with"
ls -d /persist/swift 2>/dev/null || echo "  (no /persist/swift)"
(swiftc --version 2>&1 | head -2) || true
(PATH=/persist/swift/usr/bin:$PATH swiftc --version 2>&1 | head -2) || true
go version || true

cat > /work/rd1x/x86.py <<'PYEOF'
"""the x86 divide family on go and swift, before (t4's store) and after
(this run), with the collapse column."""
import json
import os
import sys

G = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general"
AUTOPOLY = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly"
sys.path.insert(0, G)

import general as GEN
import render_general as RGEN
import z3

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
    """every x86 cell whose own term holds a division or remainder
    node.  The population walked is the cells file's own `asked` list,
    which is the 253 attested cells."""
    out = []
    for entry in cells["asked"]:
        key = (entry["asked"]["mnem"], entry["asked"]["shape"],
               entry["asked"]["key_width"])
        try:
            held = H.cell_input(cells, key)
        except Exception as problem:                          # noqa: BLE001
            continue
        found = False
        for place in held.get("places") or []:
            term = place.get("term")
            if term is None:
                continue
            if dividing(term):
                found = True
                break
            continue
        if found:
            out.append(key)
        continue
    return out


def before_rows():
    held = {}
    for line in open(STORE):
        text = line.strip()
        if not text:
            continue
        row = json.loads(text)
        if row.get("route") != "general":
            continue
        key = (row.get("mnem"), row.get("shape"), row.get("key_width"),
               row.get("lang"))
        held[key] = row
        continue
    return held


def attempt_reading(attempt):
    check = attempt.get("check") or {}
    gate = attempt.get("gate_on_the_written_term") or {}
    landing = attempt.get("landing") or {}
    outcome = check.get("outcome") or gate.get("outcome")
    if outcome is None:
        outcome = (attempt.get("refusal_cause") or "no verdict")[:60]
    return {
        "policy": attempt.get("policy"),
        "statements": attempt.get("statements"),
        "instructions": attempt.get("instructions"),
        "outcome": outcome,
        "landing": landing.get("verdict") or "NO LANDING RECORDED",
        "equality": (attempt.get("equality") or {}).get("outcome"),
    }


def main():
    AP = GEN.configure_pass()
    GEN.SRC_DIR = os.path.join(AUTOPOLY, "src_rd1_x86")
    AP.SRC_DIR = GEN.SRC_DIR
    import handful as H
    import model_table as MTAB
    MTAB._install_gpr_widths()
    shared = H.build_shared()
    cells = AP.read_json(AP.CELLS)
    say("[2/2] the divide family, machine form, then before and after")
    family = the_family(H, cells)
    say("   the family: %d x86 cells whose term holds a division or "
        "remainder node" % len(family))
    for key in family:
        say("     %s %s %d" % key)
        continue
    before = before_rows()
    say("")
    say("| cell | language | route | rv6/t4 outcome | rd1 outcome | "
        "t4 collapse | rd1 collapse | t4 instructions | rd1 instructions |")
    say("|---|---|---|---|---|---|---|---|---|")
    lines = []
    for key in family:
        for lang in TARGETS:
            was = before.get((key[0], key[1], key[2], lang))
            was_by_policy = {}
            if was is not None:
                for place in was.get("places") or []:
                    for attempt in place.get("attempts") or []:
                        reading = attempt_reading(attempt)
                        was_by_policy.setdefault(
                            (place.get("writes"), reading["policy"]),
                            reading)
                        continue
                    continue
            made = None
            for held in H.cell_inputs(cells, key):
                record = H.the_native_route(shared, held, lang)
                made = GEN.general_tier(shared, held, lang, record)
                break
            if made is None:
                say("| `%s` `%s` %d | %s | -- | -- | the tier declined "
                    "every place | -- | -- | -- | -- |"
                    % (key[0], key[1], key[2], lang))
                continue
            for place in made.get("places") or []:
                for attempt in place.get("attempts") or []:
                    now = attempt_reading(attempt)
                    old = was_by_policy.get((place.get("writes"),
                                             now["policy"])) or {}
                    say("| `%s` `%s` %d %s | %s | %s | %s | %s | %s | "
                        "%s | %s | %s |"
                        % (key[0], key[1], key[2], place.get("writes"),
                           lang, now["policy"],
                           old.get("outcome", "(no t4 row)"),
                           now["outcome"],
                           old.get("landing", "(no t4 row)"),
                           now["landing"],
                           old.get("instructions", "--"),
                           now["instructions"]))
                    continue
                continue
            continue
        continue
    say("")
    say("the guarded conditionals the render wrote for these cells:")
    for key in family:
        for lang in TARGETS:
            for held in H.cell_inputs(cells, key):
                for place in held.get("places") or []:
                    say("   %s %s %d %s / %s: (see the sources under "
                        "%s)" % (key[0], key[1], key[2],
                                 place.get("writes"), lang,
                                 GEN.SRC_DIR))
                    break
                break
            break
        break
    say("peak resident: %d kB" % GEN.peak_kb())
    return 0


if __name__ == "__main__":
    sys.exit(main())
PYEOF

timeout 5400 python3 /work/rd1x/x86.py
echo "  exit: $?"
