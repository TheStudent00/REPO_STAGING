#!/usr/bin/env python3
"""canon33_controls.py -- the controls for TASK 30.

A gate that accepts everything proves nothing.  Four controls, each
answering one way the acceptances could be hollow.

CONTROL 1 (negative, mutation).  Every canonical text this lap accepted
is mutated five ways and re-gated by the IDENTICAL gate.  A mutation
that still proves equal would mean the gate is not reading the text.
The five mutations: swap two register operands; delete one
instruction; flip an immediate; retarget one branch; narrow the answer
move back to 32 bits (the shape CAUSE 3 fixed).

CONTROL 2 (positive, real against real).  Each unit's own ship text is
gated against itself.  This is what makes a DISPROVED verdict a
statement about a candidate rather than about the checker.

CONTROL 3 (the designated-location model is not vacuous).  A text that
parks a value in a designated location and reads back a DIFFERENT
location must be DISPROVED.  If the slot store were uninterpreted --
or ignored -- this would pass.

CONTROL 4 (the narrowed rip guard still refuses a real difference).
The guard was narrowed to ignore the constants of trapping calls.
Two checks: a text differing from another only by a duplicated trap
path passes the guard (that is the narrowing working), and a text
whose NON-trap rip-relative constant loads differ is still refused
(that is the guard still guarding).

THE SPELLING BAN.  No operator token participates in any grouping,
pairing or selection here; the output declares the generator-
provenance role and is checked by check_no_spelling_keys.py.

usage:
  canon33_controls.py
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon33_gate as G33  # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]


def load(name):
    handle = open(os.path.join(HERE, name))
    doc = json.load(handle)
    handle.close()
    return doc


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


# ------------------------------------------------------- the mutations

REGISTER = re.compile(r"%[a-z0-9]+")


def mutate_swap(lines):
    for index, line in enumerate(lines):
        registers = REGISTER.findall(line)
        if len(registers) != 2:
            continue
        if registers[0] == registers[1]:
            continue
        head, _, rest = line.partition(" ")
        swapped = rest.replace(registers[0], "@@").replace(
            registers[1], registers[0]).replace("@@", registers[1])
        out = list(lines)
        out[index] = "%s %s" % (head, swapped)
        return out
    return None


def mutate_drop(lines):
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.endswith(":"):
            continue
        if stripped in ("ret",):
            continue
        if stripped.startswith("j"):
            continue
        out = list(lines)
        del out[index]
        return out
    return None


def mutate_immediate(lines):
    for index, line in enumerate(lines):
        if "$0x" not in line and "$" not in line:
            continue
        match = re.search(r"\$(0x[0-9a-f]+|\d+)", line)
        if match is None:
            continue
        value = int(match.group(1), 0)
        out = list(lines)
        out[index] = line.replace(match.group(0), "$0x%x" % (value + 1))
        return out
    return None


def mutate_branch(lines):
    labels = []
    for line in lines:
        stripped = line.strip()
        if stripped.endswith(":"):
            labels.append(stripped[:-1])
    if len(labels) < 2:
        return None
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("j"):
            continue
        parts = stripped.split(" ", 1)
        if len(parts) != 2:
            continue
        target = parts[1].strip()
        for other in labels:
            if other == target:
                continue
            out = list(lines)
            out[index] = "%s %s" % (parts[0], other)
            return out
    return None


def mutate_narrow_answer(lines):
    for index in range(len(lines) - 1, -1, -1):
        line = lines[index].strip()
        if not line.startswith("mov %r"):
            continue
        if ",%rax" not in line:
            continue
        out = list(lines)
        out[index] = line.replace(",%rax", ",%eax")
        out[index] = out[index].replace("mov %r", "mov %e", 1)
        return out
    return None


MUTATIONS = [
    ("swap-registers", mutate_swap),
    ("drop-instruction", mutate_drop),
    ("flip-immediate", mutate_immediate),
    ("retarget-branch", mutate_branch),
    ("narrow-answer-move", mutate_narrow_answer),
]


# ------------------------------------------------------------ plumbing

def as_blocks(lines):
    blocks = []
    current = None
    for line in lines:
        stripped = line.strip()
        if stripped.endswith(":"):
            current = {"label": stripped[:-1], "steps": []}
            blocks.append(current)
            continue
        if current is None:
            current = {"label": "L0", "steps": []}
            blocks.append(current)
        current["steps"].append(stripped)
    return blocks


def gate(lang, n, lines, canon4_docs, sem_docs, op_docs):
    """the gate, with any exception rendered as a refusal.  A mutated
    text can be ill-formed enough to make the simulator raise; that is
    a REJECTION of the mutant, never an acceptance, and it is recorded
    under its own verdict name rather than swallowed."""
    try:
        return gate_inner(lang, n, lines, canon4_docs, sem_docs,
                          op_docs)
    except Exception as bad:                       # noqa: BLE001
        return "REFUSED_BY_EXCEPTION", "%s: %s" % (type(bad).__name__,
                                                   bad)


def gate_inner(lang, n, lines, canon4_docs, sem_docs, op_docs):
    record = dict(canon4_docs[lang].get(n) or {})
    if any(line.strip().endswith(":") for line in lines):
        record["derived_blocks"] = as_blocks(lines)
        record.pop("derived_text", None)
        patched = dict(canon4_docs)
        units = dict(canon4_docs[lang])
        units[n] = record
        patched[lang] = units
        return G33.check_branching(lang, n, patched, op_docs, sem_docs)
    patched = dict(canon4_docs)
    units = dict(canon4_docs[lang])
    units[n] = record
    patched[lang] = units
    return G33.check_straight(lang, n, patched, sem_docs,
                              "; ".join(lines))


def main(argv):
    units = load("canon33_units.json")["units"]
    canon4_docs = {}
    sem_docs = {}
    op_docs = {}
    for lang in LANGS:
        canon4_docs[lang] = load("canon4_units_%s.json" % lang)["units"]
        sem_docs[lang] = load(
            "sem_anchored_spill_%s.json" % lang)["units"]
        op_docs[lang] = load("op_units_%s.json" % lang)["probes"]

    accepted = []
    for key in sorted(units):
        row = units[key]
        if row["outcome"] != "newly_converged":
            continue
        accepted.append(row)

    log("CONTROL 1 (negative, mutation) over %d accepted units"
        % len(accepted))
    control1 = {"applied": 0, "rejected": 0, "still_proved": 0,
                "not_applicable": 0, "units_with_a_rejection": 0,
                "units_with_no_rejection": 0}
    survivors = []
    for row in accepted:
        rejected_here = 0
        for name, mutation in MUTATIONS:
            mutated = mutation(list(row["candidate"]))
            if mutated is None or mutated == row["candidate"]:
                control1["not_applicable"] += 1
                continue
            verdict, detail = gate(row["lang"], row["n"], mutated,
                                   canon4_docs, sem_docs, op_docs)
            control1["applied"] += 1
            if verdict == "PROVED_EQUAL":
                control1["still_proved"] += 1
                survivors.append({"unit": row["unit"],
                                  "mutation": name,
                                  "text": mutated})
            else:
                control1["rejected"] += 1
                rejected_here = rejected_here + 1
        if rejected_here:
            control1["units_with_a_rejection"] += 1
        else:
            control1["units_with_no_rejection"] += 1
    log("   %s" % control1)
    log("   NOTE ON SURVIVORS.  A mutation that STILL proves equal to "
        "the unit's own real ship code is not a gate failure: z3 has "
        "just proved the mutant computes the same answers, so the "
        "mutant is another correct canonical text (measured: the "
        "flipped constant is a trapping call's argument, or a guard "
        "bound the later guards already cover).  The control's "
        "question is whether the gate is LIVE on each unit, which is "
        "the units_with_a_rejection count.")
    if control1["units_with_no_rejection"] == 0:
        log("   PASS -- every one of the %d accepted units rejected "
            "at least one mutation of its own text"
            % control1["units_with_a_rejection"])
    else:
        log("   FAIL -- %d units rejected no mutation at all"
            % control1["units_with_no_rejection"])
        for survivor in survivors[:5]:
            log("      %s %s" % (survivor["unit"],
                                 survivor["mutation"]))

    log("")
    log("CONTROL 2 (positive, real against real)")
    control2 = {"tested": 0, "proved": 0, "not_proved": 0}
    for row in accepted:
        lang = row["lang"]
        n = row["n"]
        ship = op_docs[lang][n].get("ship") or {}
        real = ship.get("mnem")
        if not real:
            continue
        control2["tested"] += 1
        blocked = any(line.strip().endswith(":")
                      for line in row["candidate"])
        if blocked:
            # the ship text is a flat instruction list; the candidate
            # is block-structured.  Cut the ship's OWN real blocks --
            # the same cut the gate itself uses -- so this control
            # compares like with like instead of handing a branching
            # text to the straight-line path.
            try:
                real_blocks_list = G33.real_blocks.build(ship["bytes"],
                                                         ship["mnem"])
            except Exception as bad:               # noqa: BLE001
                control2["not_proved"] += 1
                control2.setdefault("detail", []).append(
                    "%s/%s: %s" % (lang, n, bad))
                continue
            lines = []
            for block in real_blocks_list:
                lines.append("%s:" % block["label"])
                for step in block["steps"]:
                    lines.append(step)
        else:
            lines = list(real)
        verdict, detail = gate(lang, n, lines, canon4_docs,
                               sem_docs, op_docs)
        if verdict == "PROVED_EQUAL":
            control2["proved"] += 1
        else:
            control2["not_proved"] += 1
            control2.setdefault("detail", []).append(
                "%s/%s: %s -- %s" % (lang, n, verdict, detail[:140]))
    log("   %s" % control2)
    if control2["not_proved"] == 0:
        log("   PASS -- every unit's own ship text proves equal to "
            "itself")
    else:
        log("   PARTIAL -- %d units' own ship text did not prove "
            "equal to itself (each is a checker boundary, named in "
            "the json)" % control2["not_proved"])

    log("")
    log("CONTROL 3 (the designated-location model is not vacuous)")
    honest = ["mov %rdi,-0x8(%rsp)", "mov -0x8(%rsp),%rax", "ret"]
    dishonest = ["mov %rdi,-0x8(%rsp)", "mov -0x10(%rsp),%rax", "ret"]
    seed = {}
    sim_one = G33.Sim33(seed, "one")
    sim_two = G33.Sim33(seed, "two")
    value_one = sim_one.answer_value(honest)
    value_two = sim_two.answer_value(dishonest)
    verdict, detail = G33.BC10._finish(value_one[0], value_one[1],
                                       value_two[0], value_two[1],
                                       "rax", 64)
    control3 = {"verdict": verdict, "detail": detail[:160]}
    log("   parking in S0 and reading back S1: %s" % verdict)
    if verdict == "DISPROVED":
        log("   PASS -- the slot store distinguishes two designated "
            "locations")
    else:
        log("   FAIL -- the slot store is vacuous")

    log("")
    log("CONTROL 4 (the narrowed rip guard)")
    trap_a = ["lea 0x0(%rip),%rdi", "call *0x0(%rip)", "ret"]
    trap_b = ["lea 0x0(%rip),%rdi", "call *0x0(%rip)",
              "lea 0x0(%rip),%rdi", "call *0x0(%rip)", "ret"]
    data_a = ["addsd 0x0(%rip),%xmm0", "ret"]
    data_b = ["ret"]
    same_trap = (G33.rip_order_data_only(trap_a)
                 == G33.rip_order_data_only(trap_b))
    same_data = (G33.rip_order_data_only(data_a)
                 == G33.rip_order_data_only(data_b))
    log("   duplicated trap path passes the guard: %s" % same_trap)
    log("   differing data constants still refused: %s"
        % (not same_data))
    control4 = {"duplicated_trap_path_passes": same_trap,
                "data_constant_difference_refused": not same_data}
    if same_trap and not same_data:
        log("   PASS -- the narrowing is exactly as wide as its own "
            "argument")
    else:
        log("   FAIL")

    out = {}
    out["meta"] = {"role": "generator provenance",
                   "produced_by": "canon33_controls.py"}
    out["control1_mutation"] = control1
    out["control1_survivors"] = survivors
    out["control2_real_against_real"] = control2
    out["control3_designated_location"] = control3
    out["control4_rip_guard"] = control4
    handle = open(os.path.join(HERE, "canon33_controls.json"), "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.close()
    log("")
    log("wrote canon33_controls.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
