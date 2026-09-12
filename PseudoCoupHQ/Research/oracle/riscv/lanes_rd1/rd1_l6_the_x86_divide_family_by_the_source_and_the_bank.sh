#!/bin/bash
# rd1 lane 6 -- the x86 bank's delta on go and swift for the divide family,
# taken from the SOURCE first and the verdict second.
#
# WHY THIS SHAPE. Lane rd1_l5 offered every cell of the family to the whole
# tier and did not come back inside its ceiling: five of the eight cells have
# NO row in task t4's store at all -- t4's pass runs "every place the native
# route did not prove", so it never posed them -- and posing one now means the
# printed-term equality task t4's log_262 section 3.2 measured at 900 s a lane.
# So: every (cell, place, language, policy) of the family is RENDERED and its
# source compared with the one task t4 saved, which decides the delta exactly;
# and the tier is re-run only where the source CHANGED and t4 has a row to put
# the new verdict beside.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/rd1gocache GOPATH=/work/rd1gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rd1x3

cat > /work/rd1x3/x86.py <<'PYEOF'
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
T4_SOURCES = os.path.join(AUTOPOLY, "src_t4_general")
TARGETS = ("go", "swift")
POLICIES = ("native_first", "all_constructed")


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def dividing(term):
    """MACHINE FORM: the term holds a node of z3's own division or
    remainder declaration kinds."""
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
        "outcome": ("%s" % outcome)[:60].replace("\n", " "),
        "landing": landing.get("verdict") or "NO LANDING RECORDED",
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
    import emulate as E
    import handful as H
    import model_table as MTAB
    MTAB._install_gpr_widths()
    shared = H.build_shared()
    cells = AP.read_json(AP.CELLS)
    say("[1/3] the divide family, machine form, narrow widths first")
    family = the_family(H, cells)
    say("   %d x86 cells whose term holds a division or remainder node"
        % len(family))
    for key in family:
        say("     %s %s %d" % key)
        continue
    before = before_rows()

    say("")
    say("[2/3] every (cell, place, language, policy) rendered again, "
        "against the source task t4 saved")
    say("| cell | place | language | policy | t4 source | rd1 source | "
        "guarded conditionals | statements |")
    say("|---|---|---|---|---|---|---|---|")
    changed = set()
    shown = []
    for key in family:
        for held in H.cell_inputs(cells, key):
            for lang in TARGETS:
                word = GEN.word_of(lang)
                for place in held.get("places") or []:
                    term = place.get("term")
                    if term is None:
                        continue
                    for policy in POLICIES:
                        label = E.sanitize(
                            "%s_%s_%d__%s__%s__%s"
                            % (held["mnem"], held["shape"],
                               held["key_width"],
                               place["writes"].replace(".", "_"), lang,
                               policy))
                        ordered = H.renderer_input(term)
                        try:
                            made = RGEN.render(
                                ordered, lang, place.get("families"),
                                (place.get("home") or {}).get("family"),
                                place.get("bits"), label, word, policy,
                                place.get("text") or "")
                        except Exception as raised:           # noqa: BLE001
                            say("| `%s` `%s` %d | %s | %s | %s | -- | "
                                "the render refused: %s | -- | -- |"
                                % (key[0], key[1], key[2],
                                   place["writes"], lang, policy,
                                   ("%s" % raised)[:60]))
                            continue
                        old = os.path.join(T4_SOURCES,
                                           label + H.suffix_of(lang))
                        if not os.path.exists(old):
                            state = "not saved by t4"
                            same = None
                        else:
                            same = (open(old).read() == made["source"])
                            state = "saved"
                        if same is True:
                            verdict = "byte-identical"
                        elif same is False:
                            verdict = "CHANGED"
                            changed.add((key, lang))
                            shown.append((label, lang, old,
                                          made["source"]))
                        else:
                            verdict = "--"
                        say("| `%s` `%s` %d | %s | %s | %s | %s | %s | "
                            "%d | %d |"
                            % (key[0], key[1], key[2], place["writes"],
                               lang, policy, state, verdict,
                               made["guards"], made["statements"]))
                        continue
                    continue
                continue
            break
        continue

    say("")
    say("[3/3] the verdict beside t4's, for every changed (cell, "
        "language) task t4 has a row for")
    say("| cell | place | language | policy | t4 outcome | rd1 outcome "
        "| t4 collapse | rd1 collapse | t4 instructions | rd1 "
        "instructions |")
    say("|---|---|---|---|---|---|---|---|---|---|")
    for key, lang in sorted(changed, key=lambda one: (one[0][2],
                                                      one[0][0],
                                                      one[1])):
        was = before.get((key[0], key[1], key[2], lang))
        if was is None:
            say("| `%s` `%s` %d | -- | %s | -- | (no t4 row: t4's pass "
                "never posed this cell, the native route proved it) | "
                "not re-gated here | -- | -- | -- | -- |"
                % (key[0], key[1], key[2], lang))
            continue
        old_by = before_by_policy(was)
        started = time.time()
        made = None
        problem = None
        try:
            for held in H.cell_inputs(cells, key):
                record = H.the_native_route(shared, held, lang)
                made = GEN.general_tier(shared, held, lang, record)
                break
        except Exception as raised:                           # noqa: BLE001
            problem = "%s: %s" % (type(raised).__name__,
                                  ("%s" % raised)[:200])
        if problem is not None:
            say("| `%s` `%s` %d | -- | %s | -- | %s | THE DRIVER RAISED "
                "| -- | -- | -- | -- |"
                % (key[0], key[1], key[2], lang,
                   ("%s" % (was or {}).get("refusal_cause"))[:40]))
            say("   rd1, LITERAL: %s" % problem)
            say("   t4,  LITERAL: %s"
                % ("%s" % (was or {}).get("refusal_detail"))[:200])
            continue
        for place in (made or {}).get("places") or []:
            for attempt in place.get("attempts") or []:
                now = attempt_reading(attempt)
                old = old_by.get((place.get("writes"),
                                  now["policy"])) or {}
                say("| `%s` `%s` %d | %s | %s | %s | %s | %s | %s | %s "
                    "| %s | %s |"
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
        say("   %s %s %d on %s: %.0f s"
            % (key[0], key[1], key[2], lang, time.time() - started))
        continue

    say("")
    say("the changed sources, LITERAL (the first two)")
    for label, lang, old, source in shown[:2]:
        say("   ==== %s (%s), as task t4 wrote it:" % (label, lang))
        for line in open(old).read().splitlines()[:40]:
            say("      %s" % line)
            continue
        say("   ==== the same, under the guarded render:")
        for line in source.splitlines()[:40]:
            say("      %s" % line)
            continue
        continue
    say("")
    say("peak resident: %d kB" % GEN.peak_kb())
    return 0


if __name__ == "__main__":
    sys.exit(main())
PYEOF

echo "[1/1] the x86 divide family, by the source and then by the bank"
timeout 5400 python3 /work/rd1x3/x86.py
echo "  exit: $?"
