#!/usr/bin/env python3
"""canon32_sret_controls.py -- TASK 31: the three controls that make
canon32_sret.py's PROVED_EQUAL verdicts load-bearing.

WHY CONTROLS ARE NOT OPTIONAL HERE. log_112 found a gate that proved
everything it was shown because `canon4.py` handed it the same list
object twice (`blocks` and `derived_blocks`), so a text was compared
with itself. A gate that accepts everything is indistinguishable from
a gate that is not looking. These three controls distinguish them.

  CONTROL 1 -- NEGATIVE (mutation). Each accepted canonical text is
  mutated in a way that MUST change what the caller reads, and the
  identical gate is re-run. Every mutation must be rejected. The five
  mutations, each stated as what it breaks:
     swap-values     -- the two field values are exchanged, so the
                        image holds b where a belongs
     drop-write      -- one field write is deleted, so a cell of the
                        image is never written
     flip-immediate  -- the immediate byte $0x0 becomes $0x1
     wrong-exit      -- the exit adapter returns a different register,
                        so the caller is handed the wrong address
     narrow-write    -- a 64-bit field write becomes 32-bit, so half
                        the cell is left unwritten

  CONTROL 2 -- POSITIVE (real against real). Each unit's own ship
  text is gated against ITSELF. If this failed, a DISPROVED verdict
  would be a statement about the checker rather than about the
  candidate.

  CONTROL 3 -- HARMLESS DIFFERENCE. The canonical text's field writes
  are reordered (reversed). The writes are disjoint, so the answer is
  unchanged and the gate must still prove equality. This shows the
  gate is comparing MEANING, not text: if it were comparing text it
  would reject this.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

Coding discipline: no complex/compound one-liner statements.

usage:
  canon32_sret_controls.py
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sret_gate                        # noqa: E402

STORE_LINE_RE = re.compile(
    r"^(mov|movb|movw|movl|movq|movss|movsd)\s+(\S+),(.*)$")


def mutate_swap_values(lines):
    """the two field writes whose sources are registers exchange their
    destinations."""
    indexes = []
    for i, line in enumerate(lines):
        m = STORE_LINE_RE.match(line)
        if m is None:
            continue
        if not m.group(2).startswith("%"):
            continue
        if "(" not in m.group(3):
            continue
        indexes.append(i)
    if len(indexes) < 2:
        return None
    i = indexes[0]
    j = indexes[1]
    mi = STORE_LINE_RE.match(lines[i])
    mj = STORE_LINE_RE.match(lines[j])
    if mi.group(1) != mj.group(1):
        return None
    out = list(lines)
    out[i] = "%s %s,%s" % (mi.group(1), mj.group(2), mi.group(3))
    out[j] = "%s %s,%s" % (mj.group(1), mi.group(2), mj.group(3))
    return out


def mutate_drop_write(lines):
    for i, line in enumerate(lines):
        m = STORE_LINE_RE.match(line)
        if m is None:
            continue
        if "(" not in m.group(3):
            continue
        out = list(lines)
        del out[i]
        return out
    return None


def mutate_flip_immediate(lines):
    for i, line in enumerate(lines):
        m = STORE_LINE_RE.match(line)
        if m is None:
            continue
        if not m.group(2).startswith("$"):
            continue
        out = list(lines)
        out[i] = "%s $0x1,%s" % (m.group(1), m.group(3))
        return out
    return None


def mutate_wrong_exit(lines):
    for i, line in enumerate(lines):
        if not line.endswith(",%rax"):
            continue
        if "(" in line:
            continue
        out = list(lines)
        out[i] = "mov %rsi,%rax"
        if out[i] == line:
            out[i] = "mov %rdx,%rax"
        return out
    return None


def mutate_narrow_write(lines):
    narrow = {"%rsi": "%esi", "%rdx": "%edx", "%rdi": "%edi"}
    for i, line in enumerate(lines):
        m = STORE_LINE_RE.match(line)
        if m is None:
            continue
        if m.group(2) not in narrow:
            continue
        if "(" not in m.group(3):
            continue
        out = list(lines)
        out[i] = "%s %s,%s" % (m.group(1), narrow[m.group(2)],
                               m.group(3))
        return out
    return None


MUTATIONS = [
    ("swap-values", mutate_swap_values),
    ("drop-write", mutate_drop_write),
    ("flip-immediate", mutate_flip_immediate),
    ("wrong-exit", mutate_wrong_exit),
    ("narrow-write", mutate_narrow_write),
]


def reorder_writes(lines):
    """the field writes reversed, everything else left in place."""
    positions = []
    for i, line in enumerate(lines):
        m = STORE_LINE_RE.match(line)
        if m is None:
            continue
        if "(" not in m.group(3):
            continue
        positions.append(i)
    if len(positions) < 2:
        return None
    out = list(lines)
    values = []
    for i in positions:
        values.append(lines[i])
    values.reverse()
    for k, i in enumerate(positions):
        out[i] = values[k]
    return out


def main():
    path = os.path.join(HERE, "canon32_sret_units.json")
    fh = open(path)
    doc = json.load(fh)
    fh.close()
    rows = doc["members"]
    control1 = {"applied": 0, "rejected": 0, "still_proved": 0,
                "not_applicable": 0}
    control2 = {"tested": 0, "proved": 0, "not_proved": 0}
    control3 = {"tested": 0, "proved": 0, "not_proved": 0,
                "not_applicable": 0}
    detail = {}
    for key in sorted(rows):
        row = rows[key]
        if row.get("verdict") != "PROVED_EQUAL":
            continue
        ship = row["ship_mnem"]
        canonical = row["canonical_text"]
        per_unit = {"mutations": {}}
        for name, fn in MUTATIONS:
            mutated = fn(canonical)
            if mutated is None:
                control1["not_applicable"] = \
                    control1["not_applicable"] + 1
                per_unit["mutations"][name] = "not applicable"
                continue
            control1["applied"] = control1["applied"] + 1
            verdict, note = sret_gate.check(ship, mutated)
            per_unit["mutations"][name] = {
                "text": mutated,
                "verdict": verdict,
                "detail": note,
            }
            if verdict == "PROVED_EQUAL":
                control1["still_proved"] = control1["still_proved"] + 1
                continue
            control1["rejected"] = control1["rejected"] + 1
        control2["tested"] = control2["tested"] + 1
        verdict, note = sret_gate.check(ship, ship)
        per_unit["real_against_real"] = verdict
        if verdict == "PROVED_EQUAL":
            control2["proved"] = control2["proved"] + 1
        else:
            control2["not_proved"] = control2["not_proved"] + 1
        reordered = reorder_writes(canonical)
        if reordered is None:
            control3["not_applicable"] = control3["not_applicable"] + 1
            per_unit["reordered_writes"] = "not applicable"
        else:
            control3["tested"] = control3["tested"] + 1
            verdict, note = sret_gate.check(ship, reordered)
            per_unit["reordered_writes"] = {
                "text": reordered,
                "verdict": verdict,
            }
            if verdict == "PROVED_EQUAL":
                control3["proved"] = control3["proved"] + 1
            else:
                control3["not_proved"] = control3["not_proved"] + 1
        detail[key] = per_unit
    print("CONTROL 1 (negative, mutation): %r" % control1)
    if control1["still_proved"] == 0:
        print("   PASS -- every applied mutation was rejected")
    else:
        print("   FAIL -- %d mutations were still proved equal"
              % control1["still_proved"])
    print("CONTROL 2 (positive, real against real): %r" % control2)
    if control2["not_proved"] == 0:
        print("   PASS -- every unit's own ship text proves equal to "
              "itself, so a DISPROVED verdict is about the candidate, "
              "not about this checker")
    else:
        print("   FAIL")
    print("CONTROL 3 (harmless difference, writes reordered): %r"
          % control3)
    if control3["not_proved"] == 0:
        print("   PASS -- reordering disjoint field writes does not "
              "change the answer and the gate still proves equality, "
              "so the gate compares meaning rather than text")
    else:
        print("   FAIL")
    out_doc = {
        "meta": {
            "produced_by": "canon32_sret_controls.py",
            "role": "generator provenance",
            "what": "the three controls on the displaced-ABI gate",
            "control_1_negative_mutation": control1,
            "control_2_positive_real_against_real": control2,
            "control_3_harmless_reorder": control3,
        },
        "per_unit": detail,
    }
    out = os.path.join(HERE, "canon32_sret_controls.json")
    fh = open(out, "w")
    json.dump(out_doc, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()
    print("wrote canon32_sret_controls.json")


if __name__ == "__main__":
    main()
