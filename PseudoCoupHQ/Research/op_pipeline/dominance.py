#!/usr/bin/env python3
"""dominance.py -- THE DIRECTIONAL BRIDGE / DOMINANCE RULING, run.

the owner's ruling of 2026-08-26, in his own words:

    X dominates Y on projection P when: at every reading Y's callers
    may perform (P = the bits/outputs Y's result type promises), X
    answers identically -- and X additionally answers readings Y
    cannot.

The relation is DIRECTIONAL.  It never merges two classes.  The
result-type split stands; a bridge is laid across it, carrying three
things and no more: the projection, the proof scope, and the adapter.

The worked example, measured this session and reproduced by this file:
C's int-returning comparison dominates C++'s bool-returning comparison
on the low 8 bits.  The adapter that lets the dominated form stand
where the dominant one is expected is `movzbl %al, %eax`.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25).  No
operator token may appear in ANY key, grouping, pairing, row structure,
candidate selection, or comparison scope, anywhere in this line.  The
token appears exactly once per unit: as a display label on the member.
Nothing in this file selects, groups or pairs by a token.  Candidates
come from the class key (operand types and result type) and from the
existing connection index in verdicts3b.  Every product this file
writes is handed to check_no_spelling_keys.py before it is published.

BANNED VOCABULARY.  parent/child/sibling and their relatives are not
used here; a sub-term is a sub-term.

What this file reads
--------------------
dominant_table2.json    the 1,113 classes, result type in the class key
verdicts3b.json         the pair record, including the scope-limited z3
                        proofs and the undecided bin
sem_anchored_*.json     the units themselves (bytes, mnem, meta), or a
                        slim `units.json` when the lane embedded one

What this file writes
---------------------
bridges.json            every bridge, every skip and its reason, and
                        the residue run
dominant_table3.json    dominant_table2 with `bridges_out` and
dominant_table3.md      `bridges_in` on every class row
table_digest3.md        the short read

usage:
  dominance.py --in DIR --out DIR [--every 100] [--cap-seconds N]
"""

import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# In the lane the lifter travels beside this file.  On the host it lives
# in the co-node folder, so that folder is added when it is not here.
_KFC = os.path.join(os.path.dirname(HERE), "kind_fuzz_clustering")
if not os.path.exists(os.path.join(HERE, "arch_sem.py")):
    sys.path.insert(0, _KFC)

import arch_read as AR                                     # noqa: E402
import arch_sem as AS                                        # noqa: E402
import sem_anchored as SA                                    # noqa: E402
import z3_ext as X                                           # noqa: E402

import z3                                                    # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]

SOLVER_CAP_MS = 20000


# ===================================================================
# THE PROJECTION DERIVATION TABLE
# ===================================================================
#
# The projection is derived from the DOMINATED side's RESULT TYPE, and
# from nothing else.  It is the promise the dominated form's callers
# are entitled to read -- not the bits the machine happens to leave
# lying around, which is exactly the distinction the result-type split
# of 2026-08-25 was made to keep.
#
# Each entry is (bits, result register, what the promise is).  The
# result register is the ABI's, in the lifter's own naming: an integer
# or boolean answer comes back in %rax, a floating point answer in
# %xmm0, which libVEX models as the low half of `ymm0`.
#
# THE EXTRA-LIVE-OUTPUTS CASE is not in this table because it is not a
# width at all.  When one side leaves more live results than the other
# -- a go unit that leaves a scratch value beside the answer -- the
# projection is THE ABI RESULT REGISTER ONLY, and the width inside that
# register is still taken from this table.  See `project_outputs`.
#
# A result type this table does not name gets NO projection.  The pair
# is recorded with the reason and no bridge is claimed.  Reading, say,
# `partial_ordering` as "some number of bits" would be human
# interpretation of stated design, the weakest evidence class, and this
# file does not do it.

RESULT_PROJECTION = {
    "bool": (8, "rax",
             "the low 8 bits, holding the value 0 or 1 -- what the "
             "ABI promises a bool return is"),
    "i32": (32, "rax", "the low 32 bits, all of them valid"),
    "u32": (32, "rax", "the low 32 bits, all of them valid"),
    "i64": (64, "rax", "all 64 bits"),
    "u64": (64, "rax", "all 64 bits"),
    "f32": (32, "ymm0",
            "the low 32 bits of the result register -- one IEEE single"),
    "f64": (64, "ymm0",
            "the low 64 bits of the result register -- one IEEE double"),
}


PROJECTION_KIND = {
    8: "low-8",
    32: "low-32",
    64: "low-64",
}


def projection_of(result_type):
    """(bits, register, prose, None) or (None, None, None, reason)."""
    got = RESULT_PROJECTION.get(result_type)
    if got is None:
        reason = ("this result type has no derived projection: the "
                  "projection table does not name %r, and reading it "
                  "as a bit width would be interpretation of stated "
                  "design" % result_type)
        return None, None, None, reason
    bits, reg, prose = got
    return bits, reg, prose, None


# ===================================================================
# THE ADAPTER DERIVATION TABLE
# ===================================================================
#
# The adapter is the glue an emitter inserts so the DOMINATED form can
# stand where the DOMINANT one is expected.  It is keyed by the pair
# (dominated result type, dominant result type) and by nothing else.
#
# Entries are stated, not guessed.  A pair outside this table is
# recorded with `adapter: null` and the note "none derived"; it is a
# real bridge with an unstated adapter, which is a different fact from
# a bridge with a wrong one.
#
# `movzbl %al, %eax` is the worked example the owner measured this session.
# It is also the whole of the bool cases: on amd64, writing a 32-bit
# register zeroes the upper 32 bits of the 64-bit register, so the same
# one instruction serves bool -> i32, bool -> i64 and bool -> u64.
#
# i32 -> i64 is DELIBERATELY ABSENT.  Whether the widening is `movslq`
# or `movl` depends on the signedness the caller reads with, and the
# result types alone do not settle it.  It is recorded as none derived.

ADAPTER = {
    ("bool", "i32"): "movzbl %al, %eax",
    ("bool", "i64"): ("movzbl %al, %eax   -- writing %eax zeroes the "
                      "upper 32 bits of %rax, so no second instruction "
                      "is needed"),
    ("bool", "u64"): ("movzbl %al, %eax   -- writing %eax zeroes the "
                      "upper 32 bits of %rax, so no second instruction "
                      "is needed"),
    ("u32", "u64"): "movl %eax, %eax",
}

# The extra-live-outputs case has one adapter and it is not an
# instruction: the emitter reads the result register and ignores what
# the dominated form left elsewhere.
ADAPTER_OUTPUTS = {
    "rax": "read only %rax; the extra live register is not the answer",
    "ymm0": "read only %xmm0; the extra live register is not the answer",
}


def adapter_for(dominated_type, dominant_type):
    """(adapter text, note)."""
    key = (dominated_type, dominant_type)
    got = ADAPTER.get(key)
    if got is not None:
        return got, "derived from the adapter table"
    note = ("none derived: the adapter table does not state a "
            "conversion from this result type to that one, and this "
            "file records the gap rather than guessing an instruction")
    return None, note


# ===================================================================
# the units, and their live results WITH the register kept
# ===================================================================
#
# arch_sem.summarize drops the register name: it answers "these are the
# values the unit leaves", not "this value is in %rax".  For dominance
# the register is load-bearing -- the projection names one register --
# so the same filtering is repeated here with the name kept.  The
# FILTER IS arch_sem's, rule for rule; only the name survives that
# would otherwise be thrown away.

class LiftRefused(Exception):
    pass


def live_results(unit):
    """[(register name, value expression), ...] for the unit's single
    block, plus the anchored name map.  Raises LiftRefused with the
    tool's own words when the unit cannot be read this way."""
    names = SA.anchor_names(unit["lang"], unit["meta"])
    if names is None:
        raise LiftRefused("no ABI classification for the parameter types")
    lay, reason = SA.layout(dict(bytes=unit["bytes"].split(),
                                 mnem=unit["mnem"]))
    if lay is None:
        raise LiftRefused(reason)
    rec = dict(state="OK", bytes=unit["bytes"].split(),
               mnem=unit["mnem"], layout=lay)
    insns = AR.instructions(rec)
    if insns is None:
        raise LiftRefused("arch_read refused the recovered layout")
    insns, _endbr = AR.strip_entry_endbr64(insns)
    insns, _go, _unmatched = AR.strip_go_stack_growth(insns)
    texts, _masked = AR.normalize_addresses(insns)
    index = dict((ins["addr"], k) for k, ins in enumerate(insns))
    spans, block_index = AS.blocks_of(insns, texts, index)
    if len(spans) != 1:
        raise LiftRefused("%s op_%s is not straight-line: %d blocks"
                          % (unit["lang"], unit["n"], len(spans)))
    lo, hi = spans[0]
    st = AS._sweep(insns, texts, index, block_index, lo, hi)
    if st.stores:
        raise LiftRefused("%s op_%s writes memory"
                          % (unit["lang"], unit["n"]))
    kept = []
    for name in sorted(st.written):
        if name in AS.PSEUDO:
            continue
        if name == "*":
            continue
        if name == "rsp":
            continue
        value = st.reg.get(name)
        if value is None:
            continue
        if value[0] == "r" and value[2] == name:
            continue
        value = AS._untouched_slice(value, name)
        value = AS._map(value, AS._riprel_mask)
        kept.append((name, value))
    inner = set()
    for _name, value in kept:
        seen = set()
        AS._subexprs(value, seen)
        inner |= (seen - set([value]))
    kept = [(n, v) for n, v in kept if v not in inner]

    # THE NAMING STEP, exactly sem_anchored.render_anchored's.  Without
    # it every register that is not an argument register is unnamed, and
    # z3_ext.Side refuses a register with no name -- which would read as
    # "the solver could not settle it" when in truth the pass never
    # asked.  The argument registers keep their anchored `inN` tokens;
    # everything else is named `uN` in a separate namespace, so nothing
    # that is not an operand can be read as one.
    ordered = sorted([v for _n, v in kept], key=AS._key)
    order = []
    for value in ordered:
        AS._leaves(value, order)
    names = dict(names)
    k = 0
    for reg in order:
        if reg in names:
            continue
        names[reg] = "u%d" % k
        k = k + 1
    return kept, names


def result_value(kept, register):
    """the value the unit leaves in the ABI result register, or None.

    libVEX models %xmm0 as the low half of `ymm0`, so a floating point
    answer is looked for under `ymm0`."""
    for name, value in kept:
        if name == register:
            return value
    return None


# ===================================================================
# the proof, on the projection
# ===================================================================
#
# This is the machinery the scope_bits ladder in z3_ext already runs.
# The one change is what is being recorded: not a weak MATCHED at a
# narrow width, but a DIRECTIONAL EDGE at a width the reader's own
# result type named in advance.
#
# The translation is z3_ext's, imported unchanged.  Nothing about the
# bit arithmetic is re-implemented here.

def prove_on_projection(left, right, register, bits, bool_precondition):
    """(True/False/None, detail).  None means the solver did not
    settle it; the detail is the tool's own words either way."""
    try:
        lkept, lnames = live_results(left)
        rkept, rnames = live_results(right)
    except LiftRefused as exc:
        return None, "the lift was refused: %s" % exc

    lval = result_value(lkept, register)
    rval = result_value(rkept, register)
    if lval is None:
        return None, ("%s op_%s leaves no live value in the result "
                      "register the projection names"
                      % (left["lang"], left["n"]))
    if rval is None:
        return None, ("%s op_%s leaves no live value in the result "
                      "register the projection names"
                      % (right["lang"], right["n"]))

    lside = X.Side(lnames, "L")
    rside = X.Side(rnames, "R")
    env = {}
    try:
        a = X.bv(lval, lside, env)
        b = X.bv(rval, rside, env)
    except X.Unsupported as exc:
        return None, "z3 was not asked: %s" % exc
    except Exception as exc:                                 # noqa: BLE001
        return None, ("the translation raised: %s: %s"
                      % (type(exc).__name__, exc))

    pre = []
    if bool_precondition:
        # THE ABI'S PROMISE, EXACTLY, and only where a bool operand
        # arrives: the value is 0 or 1 in the low byte.  Nothing is
        # asserted about the bits above it.
        for key in sorted(env.keys()):
            if not key.startswith("in"):
                continue
            low = X.fit(env[key], 8)
            pre.append(z3.ULE(low, z3.BitVecVal(1, 8)))

    claim = X.fit(a, bits) == X.fit(b, bits)
    solver = z3.Solver()
    solver.set("timeout", SOLVER_CAP_MS)
    for p in pre:
        solver.add(p)
    solver.add(z3.Not(claim))
    got = solver.check()

    scratch = sorted(set(lside.scratch + rside.scratch))
    if got == z3.unsat:
        detail = ("z3 proved the two canonical forms equal on the "
                  "projection -- the low %d bits of the result register "
                  "-- for every input (negation unsat)" % bits)
        if scratch:
            detail += ("; the proof holds for every value of the "
                       "unanchored scratch registers %s"
                       % ", ".join(scratch))
        if bool_precondition:
            detail += ("; under the ABI precondition that each bool "
                       "operand arrives as 0 or 1 in the low byte of "
                       "its register")
        return True, detail
    if got == z3.sat:
        model = solver.model()
        shown = ", ".join("%s = %s" % (d.name(), model[d])
                          for d in sorted(model.decls(),
                                          key=lambda d: d.name()))
        return False, ("z3 counterexample on the projection (low %d "
                       "bits): %s" % (bits, shown))
    return None, ("z3 returned %s on the projection (low %d bits, "
                  "timeout %d ms)" % (got, bits, SOLVER_CAP_MS))


# ===================================================================
# the direction rule
# ===================================================================
#
# the owner's rule, stated once: "the side whose form defines MORE than the
# projection dominates.  If both define exactly the projection, that is
# symmetric equality and belongs to class merging, not a bridge."
#
# Two shapes of "more", and they are kept apart on the row:
#
#   MORE BITS.  The two result types promise different widths in the
#   same register.  The wider promise dominates; the projection is the
#   narrower one.  This is the C-int-against-C++-bool case.
#
#   MORE OUTPUTS.  The two units leave a different number of live
#   results.  The side with more outputs answers everything the other
#   answers, in the same register, and leaves something else besides.
#   The projection is THE ABI RESULT REGISTER ONLY.  This is the
#   different-live-result-count residue the owner named.

def direction_by_bits(type_a, type_b):
    """(dominant type, dominated type, projection bits, register,
    prose) or (None, None, None, None, reason)."""
    bits_a, reg_a, prose_a, why_a = projection_of(type_a)
    if why_a is not None:
        return None, None, None, None, why_a
    bits_b, reg_b, prose_b, why_b = projection_of(type_b)
    if why_b is not None:
        return None, None, None, None, why_b
    if reg_a != reg_b:
        reason = ("the two result types are answered in different "
                  "registers (%s and %s), so there is no common "
                  "projection to compare them on" % (reg_a, reg_b))
        return None, None, None, None, reason
    if bits_a == bits_b:
        reason = ("both sides define exactly the projection (%d bits "
                  "each), so neither answers a reading the other "
                  "cannot; this is symmetric equality and belongs to "
                  "class merging, not to a bridge" % bits_a)
        return None, None, None, None, reason
    if bits_a > bits_b:
        return type_a, type_b, bits_b, reg_b, prose_b
    return type_b, type_a, bits_a, reg_a, prose_a


def project_outputs(type_dominated, type_dominant):
    """the extra-live-outputs case: the projection is the ABI result
    register only, and the width inside it is still the dominated
    side's promise.  (bits, register, prose) or (None, None, reason)."""
    bits, reg, prose, why = projection_of(type_dominated)
    if why is not None:
        return None, None, why
    other_bits, other_reg, _p, other_why = projection_of(type_dominant)
    if other_why is not None:
        return None, None, other_why
    if reg != other_reg:
        reason = ("the two result types are answered in different "
                  "registers (%s and %s), so the result register is "
                  "not one projection" % (reg, other_reg))
        return None, None, reason
    if other_bits < bits:
        bits = other_bits
    prose = ("the ABI result register only (%s), read at %d bits; the "
             "extra live results the other side leaves are outside the "
             "projection" % (reg, bits))
    return bits, reg, prose


# ===================================================================
# the candidate set -- machine-form evidence only
# ===================================================================
#
# A candidate is a pair of CLASSES, not of units.  Two rules, both
# stated by the owner, and no operator token takes part in either:
#
#  1. the two classes carry the SAME operand types and DIFFERENT result
#     types (the class key, straight off the row); and
#  2. their canonical cores are CONNECTED -- which here means some
#     member of one and some member of the other already sit together
#     in a verdicts3b pair record.  That index was itself built from
#     "type pair, then cluster identity or shared maximal sub-term",
#     which is the existing connection index and is machine form only;
#     OR some member pair of theirs carries a scope-limited z3 proof
#     (`scope_bits` recorded, `full_width` false).

def build_candidates(table, verdicts):
    by_class = {}
    for row in table["rows"]:
        by_class[row["class_id"]] = row
    of_unit = {}
    for row in table["rows"]:
        for member in row["members"]:
            of_unit[member["unit"]] = row["class_id"]

    linked = {}
    scope_limited = set()
    live_result_gap = set()
    for row in verdicts["rows"]:
        for pair in row["pairs"]:
            left = of_unit.get(pair["left"])
            right = of_unit.get(pair["right"])
            if left is None:
                continue
            if right is None:
                continue
            if left == right:
                continue
            key = tuple(sorted([left, right]))
            if key not in linked:
                linked[key] = []
            linked[key].append(pair)
            if pair.get("scope_bits") is not None:
                if pair.get("full_width") is False:
                    scope_limited.add(key)
            detail = str(pair.get("detail") or "")
            if "different number of live results" in detail:
                live_result_gap.add(key)

    candidates = []
    for key in sorted(linked.keys()):
        a = by_class[key[0]]
        b = by_class[key[1]]
        if a["class_key"]["operand_types"] != b["class_key"]["operand_types"]:
            continue
        if a["result_type"] == b["result_type"]:
            continue
        candidates.append(dict(
            classes=list(key),
            operand_types=a["class_key"]["operand_types"],
            result_types=[a["result_type"], b["result_type"]],
            connection=("a scope-limited z3 proof between two members"
                        if key in scope_limited
                        else "the existing connection index: two members "
                             "already sit together in a pair record"),
            scope_limited_proof=(key in scope_limited),
            live_result_gap=(key in live_result_gap),
            evidence_pairs=len(linked[key]),
        ))
    return candidates, by_class, of_unit, linked


def representative(row, units):
    """the class member the proof is run on.  A class is the closure of
    equality edges, so any member stands for it; the one the table
    already named as the source of the canonical core is preferred, and
    the rest are tried in the table's own order when it will not lift."""
    order = []
    wanted = row.get("canonical_core_from")
    for member in row["members"]:
        if member["unit"] == wanted:
            order.append(member["unit"])
    for member in row["members"]:
        if member["unit"] not in order:
            order.append(member["unit"])
    for label in order:
        unit = units.get(label)
        if unit is None:
            continue
        try:
            live_results(unit)
        except LiftRefused:
            continue
        except Exception:                                    # noqa: BLE001
            continue
        return label, unit
    return None, None


# ===================================================================
# the pass
# ===================================================================

def decide_class_pair(cand, by_class, units):
    """one bridge row, or one skip row with its reason."""
    a_id, b_id = cand["classes"]
    a = by_class[a_id]
    b = by_class[b_id]
    type_a = a["result_type"]
    type_b = b["result_type"]

    a_label, a_unit = representative(a, units)
    b_label, b_unit = representative(b, units)
    if a_unit is None or b_unit is None:
        return None, dict(classes=[a_id, b_id],
                          result_types=[type_a, type_b],
                          skipped="no member of one class lifts, so "
                                  "there is nothing to prove on")

    try:
        a_live, _n = live_results(a_unit)
        b_live, _m = live_results(b_unit)
    except LiftRefused as exc:
        return None, dict(classes=[a_id, b_id],
                          result_types=[type_a, type_b],
                          skipped="the lift was refused: %s" % exc)

    outputs_case = (len(a_live) != len(b_live))

    if outputs_case:
        if len(a_live) > len(b_live):
            dom_id, dom_type, sub_id, sub_type = a_id, type_a, b_id, type_b
        else:
            dom_id, dom_type, sub_id, sub_type = b_id, type_b, a_id, type_a
        bits, reg, prose = project_outputs(sub_type, dom_type)
        if bits is None:
            return None, dict(classes=[a_id, b_id],
                              result_types=[type_a, type_b],
                              skipped=prose)
        kind = "result-register-only"
        why = ("more outputs: %d live results against %d, in the same "
               "result register" % (max(len(a_live), len(b_live)),
                                    min(len(a_live), len(b_live))))
    else:
        dom_type, sub_type, bits, reg, prose = direction_by_bits(type_a,
                                                                 type_b)
        if dom_type is None:
            return None, dict(classes=[a_id, b_id],
                              result_types=[type_a, type_b],
                              skipped=prose)
        if dom_type == type_a:
            dom_id, sub_id = a_id, b_id
        else:
            dom_id, sub_id = b_id, a_id
        kind = PROJECTION_KIND.get(bits, "low-%d" % bits)
        why = ("more bits: the dominant side's result type promises a "
               "wider answer than the projection")

    bool_pre = (cand["operand_types"] == "bool,bool")
    ok, detail = prove_on_projection(a_unit, b_unit, reg, bits, bool_pre)
    if ok is None:
        return None, dict(classes=[a_id, b_id],
                          result_types=[type_a, type_b],
                          projection_bits=bits,
                          skipped="the solver did not settle it: %s"
                                  % detail)
    if ok is False:
        return None, dict(classes=[a_id, b_id],
                          result_types=[type_a, type_b],
                          projection_bits=bits,
                          skipped="not equal on the projection: %s"
                                  % detail)

    adapter, adapter_note = adapter_for(sub_type, dom_type)
    if outputs_case:
        adapter = ADAPTER_OUTPUTS.get(reg)
        adapter_note = ("derived from the adapter table: the "
                        "extra-live-outputs case has one adapter and it "
                        "is a reading rule, not an instruction")
        if adapter is None:
            adapter_note = ("none derived: the adapter table names no "
                            "reading rule for this register")

    dom_row = by_class[dom_id]
    sub_row = by_class[sub_id]
    bridge = dict(
        dominant_class=dom_id,
        dominated_class=sub_id,
        operand_types=cand["operand_types"],
        dominant_result_type=dom_type,
        dominated_result_type=sub_type,
        projection_kind=kind,
        projection_bits=bits,
        projection_register=reg,
        projection=prose,
        direction_ground=why,
        proof_scope=("z3 over the two canonical forms, restricted to "
                     "the projection; solver cap %d ms" % SOLVER_CAP_MS),
        proof_detail=detail,
        adapter=adapter,
        adapter_note=adapter_note,
        abi_precondition=bool_pre,
        live_results_of_the_two_representatives=[len(a_live),
                                                 len(b_live)],
        evidence=dict(
            connection=cand["connection"],
            scope_limited_proof=cand["scope_limited_proof"],
            connecting_pair_records=cand["evidence_pairs"],
            proved_on=[a_label, b_label],
            dominant_languages=dom_row["languages"],
            dominated_languages=sub_row["languages"],
            evidence_class=("solver analysis over the lifted form: it "
                            "proves about the MODEL of the machine, "
                            "which is the lifter's testimony"),
        ),
        classes_stay_split=True,
    )
    return bridge, None


def run(table, verdicts, units, every, cap_seconds):
    started = time.time()
    candidates, by_class, of_unit, linked = build_candidates(table,
                                                             verdicts)
    total = len(candidates)
    print("candidate class pairs: %d" % total)
    print("   (same operand types, different result type, connected)")
    sys.stdout.flush()

    bridges = []
    skips = []
    done = 0
    for cand in candidates:
        bridge, skip = decide_class_pair(cand, by_class, units)
        if bridge is not None:
            bridges.append(bridge)
        if skip is not None:
            skips.append(skip)
        done += 1
        if done % every == 0 or done == total:
            print("[progress] %d/%d bridges=%d skipped=%d elapsed=%ds"
                  % (done, total, len(bridges), len(skips),
                     int(time.time() - started)))
            sys.stdout.flush()
        if cap_seconds and (time.time() - started) > cap_seconds:
            print("[progress] the wall-clock cap was reached at %d/%d"
                  % (done, total))
            break
    return bridges, skips, by_class, of_unit, started


# ===================================================================
# THE BIG TEST -- the different-live-results residue
# ===================================================================
#
# The solver left a bin of pairs with one reason: "the two units leave
# a different number of live results".  That is precisely the shape
# the owner named -- one side leaves extra outputs, same answer plus more --
# so every such pair is re-asked as a dominance question, at UNIT
# level, on the ABI result register only.

def residue(verdicts, units, every, started, cap_seconds):
    wanted = {}
    for row in verdicts["rows"]:
        for pair in row["pairs"]:
            detail = str(pair.get("detail") or "")
            if "different number of live results" not in detail:
                continue
            key = tuple(sorted([pair["left"], pair["right"]]))
            if key in wanted:
                continue
            wanted[key] = dict(left=pair["left"], right=pair["right"],
                               type_pair=pair.get("pair_type_pair")
                               or row["type_pair"],
                               solver_reason=detail)
    keys = sorted(wanted.keys())
    total = len(keys)
    print("residue: %d distinct pairs whose reason is a different "
          "number of live results" % total)
    sys.stdout.flush()

    resolved = []
    remaining = []
    done = 0
    for key in keys:
        item = wanted[key]
        got = decide_unit_pair(item, units)
        if got.get("dominant") is not None:
            resolved.append(got)
        else:
            remaining.append(got)
        done += 1
        if done % every == 0 or done == total:
            print("[progress] residue %d/%d resolved=%d remaining=%d "
                  "elapsed=%ds" % (done, total, len(resolved),
                                   len(remaining),
                                   int(time.time() - started)))
            sys.stdout.flush()
        if cap_seconds and (time.time() - started) > cap_seconds:
            print("[progress] the wall-clock cap was reached at %d/%d "
                  "of the residue" % (done, total))
            break
    return resolved, remaining, total


def result_type_of(unit):
    """the unit's own normalised result type, as the table recorded it
    on its member row.  Carried on the slim unit record."""
    return unit.get("result_type")


def decide_unit_pair(item, units):
    left = units.get(item["left"])
    right = units.get(item["right"])
    out = dict(left=item["left"], right=item["right"],
               type_pair=item["type_pair"],
               solver_reason=item["solver_reason"],
               dominant=None, dominated=None)
    if left is None or right is None:
        out["reason"] = "a unit of the pair is not in the accepted set"
        return out
    try:
        l_live, _a = live_results(left)
        r_live, _b = live_results(right)
    except LiftRefused as exc:
        out["reason"] = "the lift was refused: %s" % exc
        return out
    except Exception as exc:                                 # noqa: BLE001
        out["reason"] = ("the lift raised: %s: %s"
                         % (type(exc).__name__, exc))
        return out
    if len(l_live) == len(r_live):
        out["reason"] = ("this pass reads the same number of live "
                         "results on both sides, so the solver's own "
                         "reason no longer applies and there is no "
                         "extra output to bridge")
        return out
    if len(l_live) > len(r_live):
        dom, sub = item["left"], item["right"]
        dom_type = result_type_of(left)
        sub_type = result_type_of(right)
    else:
        dom, sub = item["right"], item["left"]
        dom_type = result_type_of(right)
        sub_type = result_type_of(left)
    bits, reg, prose = project_outputs(sub_type, dom_type)
    if bits is None:
        out["reason"] = prose
        return out
    bool_pre = (item["type_pair"] == "bool,bool")
    ok, detail = prove_on_projection(left, right, reg, bits, bool_pre)
    if ok is None:
        out["reason"] = "the solver did not settle it: %s" % detail
        return out
    if ok is False:
        out["reason"] = ("not equal on the projection: %s" % detail)
        return out
    adapter = ADAPTER_OUTPUTS.get(reg)
    out["dominant"] = dom
    out["dominated"] = sub
    out["dominant_result_type"] = dom_type
    out["dominated_result_type"] = sub_type
    out["projection_kind"] = "result-register-only"
    out["projection_bits"] = bits
    out["projection_register"] = reg
    out["projection"] = prose
    out["proof_detail"] = detail
    out["adapter"] = adapter
    out["abi_precondition"] = bool_pre
    out["live_results"] = [len(l_live), len(r_live)]
    return out


# ===================================================================
# the products
# ===================================================================

def attach(table, bridges):
    """each class row gains bridges_out and bridges_in.  CLASSES STAY
    SPLIT: a bridge is written on both rows and merges nothing."""
    out = {}
    into = {}
    for b in bridges:
        d = b["dominant_class"]
        s = b["dominated_class"]
        if d not in out:
            out[d] = []
        if s not in into:
            into[s] = []
        entry = dict(
            to_class=s,
            projection_kind=b["projection_kind"],
            projection_bits=b["projection_bits"],
            projection=b["projection"],
            proof_scope=b["proof_scope"],
            adapter=b["adapter"],
            adapter_note=b["adapter_note"],
            evidence=b["evidence"],
        )
        out[d].append(entry)
        entry_in = dict(entry)
        entry_in.pop("to_class")
        entry_in["from_class"] = d
        into[s].append(entry_in)
    for row in table["rows"]:
        row["bridges_out"] = out.get(row["class_id"], [])
        row["bridges_in"] = into.get(row["class_id"], [])
    return table


def counts(bridges):
    by_kind = {}
    by_direction = {}
    for b in bridges:
        k = b["projection_kind"]
        by_kind[k] = by_kind.get(k, 0) + 1
        doms = ",".join(sorted(b["evidence"]["dominant_languages"]))
        subs = ",".join(sorted(b["evidence"]["dominated_languages"]))
        pattern = "%s dominates %s" % (doms, subs)
        by_direction[pattern] = by_direction.get(pattern, 0) + 1
    return by_kind, by_direction


def write_md(path, table, bridges, skips, resid, digest_path):
    by_kind, by_direction = counts(bridges)
    out = []
    out.append("# the dominant-operator table -- with directional bridges")
    out.append("")
    out.append("This is `dominant_table2.md` with one addition and no "
               "subtraction.  THE CLASSES ARE UNCHANGED: the result-type "
               "split stands, and a bridge merges nothing.  Every class "
               "row now also carries `bridges_out` and `bridges_in`.")
    out.append("")
    out.append("A bridge says: **X dominates Y on projection P**.  At "
               "every reading Y's callers may perform -- P being the "
               "bits the dominated side's own result type promises -- X "
               "answers identically, and X answers readings Y cannot.  "
               "The row carries the projection, the proof scope, and the "
               "adapter an emitter inserts to put the dominated form "
               "where the dominant one is expected.")
    out.append("")
    out.append("## the projection derivation table")
    out.append("")
    out.append("| result type of the dominated side | projection | "
               "result register |")
    out.append("| --- | --- | --- |")
    for name in sorted(RESULT_PROJECTION.keys()):
        bits, reg, prose = RESULT_PROJECTION[name]
        out.append("| `%s` | %d bits -- %s | `%%%s` |"
                   % (name, bits, prose, reg))
    out.append("| a result type this table does not name | none derived "
               "| -- |")
    out.append("| one side leaves extra live results | the ABI result "
               "register only | as above |")
    out.append("")
    out.append("## the adapter derivation table")
    out.append("")
    out.append("| dominated | dominant | adapter |")
    out.append("| --- | --- | --- |")
    for key in sorted(ADAPTER.keys()):
        out.append("| `%s` | `%s` | `%s` |"
                   % (key[0], key[1], ADAPTER[key]))
    for reg in sorted(ADAPTER_OUTPUTS.keys()):
        out.append("| extra live results | -- | %s |"
                   % ADAPTER_OUTPUTS[reg])
    out.append("| anything else | | none derived -- recorded, not "
               "guessed |")
    out.append("")
    out.append("## the counts")
    out.append("")
    out.append("- bridges: **%d**" % len(bridges))
    out.append("- class pairs looked at and not bridged: **%d**"
               % len(skips))
    out.append("")
    out.append("| projection kind | bridges |")
    out.append("| --- | --- |")
    for k in sorted(by_kind.keys()):
        out.append("| %s | %d |" % (k, by_kind[k]))
    out.append("")
    out.append("| direction | bridges |")
    out.append("| --- | --- |")
    ordered = sorted(by_direction.items(), key=lambda kv: -kv[1])
    for pattern, n in ordered[:40]:
        out.append("| %s | %d |" % (pattern, n))
    out.append("")
    out.append("## the different-live-results residue")
    out.append("")
    out.append("- distinct pairs the solver left with that reason: **%d**"
               % resid["asked"])
    out.append("- resolved by dominance (a direction proven): **%d**"
               % resid["resolved"])
    out.append("- still standing on the solver's own reason: **%d**"
               % resid["remaining"])
    out.append("")
    out.append("| pairs | why it still stands |")
    out.append("| --- | --- |")
    ordered = sorted(resid["remaining_reasons"].items(),
                     key=lambda kv: -kv[1])
    for reason, n in ordered[:30]:
        out.append("| %d | %s |" % (n, reason.replace("|", "/")))
    out.append("")
    out.append("## every bridge")
    out.append("")
    out.append("| dominant class | dominated class | operand types | "
               "dominant result | dominated result | projection | "
               "adapter |")
    out.append("| --- | --- | --- | --- | --- | --- | --- |")
    for b in bridges:
        out.append("| %s | %s | %s | `%s` | `%s` | %s (%d bits) | %s |"
                   % (b["dominant_class"], b["dominated_class"],
                      b["operand_types"], b["dominant_result_type"],
                      b["dominated_result_type"], b["projection_kind"],
                      b["projection_bits"],
                      str(b["adapter"] or "none derived").replace("|",
                                                                  "/")))
    out.append("")
    open(path, "w").write("\n".join(out))

    short = []
    short.append("# the bridge digest")
    short.append("")
    short.append("- classes: %d (unchanged -- bridges never merge)"
                 % len(table["rows"]))
    short.append("- bridges: %d" % len(bridges))
    for k in sorted(by_kind.keys()):
        short.append("  - %s: %d" % (k, by_kind[k]))
    short.append("- different-live-results residue: %d asked, %d "
                 "resolved, %d standing"
                 % (resid["asked"], resid["resolved"],
                    resid["remaining"]))
    short.append("")
    open(digest_path, "w").write("\n".join(short))


def load_units(indir):
    """label -> the slim record the pass reads.  A `units.json` written
    by the lane builder is preferred; otherwise the sem_anchored files
    are read directly."""
    slim = os.path.join(indir, "units.json")
    if os.path.exists(slim):
        return json.load(open(slim))
    index = {}
    table = json.load(open(os.path.join(indir, "dominant_table2.json")))
    result_types = {}
    for row in table["rows"]:
        for member in row["members"]:
            result_types[member["unit"]] = member["result_type"]
    for lang in LANGS:
        path = os.path.join(indir, "sem_anchored_%s.json" % lang)
        if not os.path.exists(path):
            continue
        doc = json.load(open(path))
        for n, u in doc["units"].items():
            label = "%s/op_%s" % (lang, n)
            index[label] = dict(lang=lang, n=n, meta=u["meta"],
                                bytes=u["bytes"], mnem=u["mnem"],
                                result_type=result_types.get(label))
    return index


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="indir", default=HERE)
    ap.add_argument("--out", dest="outdir", default=HERE)
    ap.add_argument("--every", type=int, default=100)
    ap.add_argument("--cap-seconds", type=int, default=0)
    args = ap.parse_args(argv[1:])

    started = time.time()
    print("== dominance: the directional bridge")
    print("   z3      %s" % z3.get_version_string())
    print("   lifter  %s" % AS.LIFTER_ID)
    print("   solver cap %d ms" % SOLVER_CAP_MS)
    sys.stdout.flush()

    table = json.load(open(os.path.join(args.indir,
                                        "dominant_table2.json")))
    verdicts = json.load(open(os.path.join(args.indir,
                                           "verdicts3b.json")))
    units = load_units(args.indir)
    print("   classes %d   units %d" % (len(table["rows"]), len(units)))
    sys.stdout.flush()

    bridges, skips, by_class, _of_unit, _t = run(
        table, verdicts, units, args.every, args.cap_seconds)

    resolved, remaining, asked = residue(verdicts, units, args.every,
                                         started, args.cap_seconds)
    remaining_reasons = {}
    for item in remaining:
        key = str(item.get("reason") or "")[:120]
        remaining_reasons[key] = remaining_reasons.get(key, 0) + 1

    by_kind, by_direction = counts(bridges)
    skip_reasons = {}
    for s in skips:
        key = str(s.get("skipped") or "")[:120]
        skip_reasons[key] = skip_reasons.get(key, 0) + 1

    resid = dict(asked=asked, resolved=len(resolved),
                 remaining=len(remaining),
                 remaining_reasons=remaining_reasons)

    doc = dict(
        shape="one row per DIRECTIONAL BRIDGE between two classes",
        ruling=("the owner, 2026-08-26: X dominates Y on projection P when at "
                "every reading Y's callers may perform, X answers "
                "identically, and X answers readings Y cannot.  "
                "Directional.  Classes stay split; a bridge merges "
                "nothing."),
        candidate_set=("pairs of CLASSES carrying the same operand "
                       "types and different result types, whose members "
                       "are already connected in the pair record or by "
                       "a scope-limited z3 proof.  No operator token "
                       "takes part in any key, grouping, pairing or "
                       "selection here."),
        spelling=("the operator token appears once per unit, as the "
                  "display label `operator` on a member object beside "
                  "`lang` and `n`."),
        projection_derivation=dict(
            (name, dict(bits=RESULT_PROJECTION[name][0],
                        register=RESULT_PROJECTION[name][1],
                        promise=RESULT_PROJECTION[name][2]))
            for name in RESULT_PROJECTION),
        projection_extra_outputs=("when one side leaves more live "
                                  "results than the other, the "
                                  "projection is the ABI result "
                                  "register only"),
        adapter_derivation=dict(
            ("%s to %s" % (k[0], k[1]), ADAPTER[k]) for k in ADAPTER),
        adapter_extra_outputs=ADAPTER_OUTPUTS,
        adapter_gap_note=("a pair outside the adapter table is recorded "
                          "with a null adapter and the note `none "
                          "derived`; no instruction is guessed"),
        z3=z3.get_version_string(),
        lifter=AS.LIFTER_ID,
        solver_cap_ms=SOLVER_CAP_MS,
        wall_seconds=int(time.time() - started),
        bridge_count=len(bridges),
        bridges_by_projection_kind=by_kind,
        bridges_by_direction=by_direction,
        class_pairs_not_bridged=len(skips),
        not_bridged_reasons=skip_reasons,
        residue=dict(
            what=("the pairs the solver left UNDECIDED for one reason: "
                  "the two units leave a different number of live "
                  "results"),
            asked=asked,
            resolved_by_dominance=len(resolved),
            still_standing=len(remaining),
            still_standing_reasons=remaining_reasons,
            resolved_rows=resolved,
            still_standing_rows=remaining,
        ),
        bridges=bridges,
        not_bridged=skips,
    )
    path = os.path.join(args.outdir, "bridges.json")
    json.dump(doc, open(path, "w"), indent=1)
    print("wrote %s" % path)

    table = attach(table, bridges)
    table["bridges"] = dict(
        count=len(bridges),
        by_projection_kind=by_kind,
        note=("bridges are DIRECTIONAL and merge nothing.  The classes "
              "in this table are exactly the classes of "
              "dominant_table2.json."),
        source="bridges.json",
    )
    path3 = os.path.join(args.outdir, "dominant_table3.json")
    json.dump(table, open(path3, "w"), indent=1)
    print("wrote %s" % path3)

    write_md(os.path.join(args.outdir, "dominant_table3.md"),
             table, bridges, skips, resid,
             os.path.join(args.outdir, "table_digest3.md"))
    print("wrote %s" % os.path.join(args.outdir, "dominant_table3.md"))

    print()
    print("== dominance done in %ds" % int(time.time() - started))
    print("   bridges           %d" % len(bridges))
    for k in sorted(by_kind.keys()):
        print("     %-24s %d" % (k, by_kind[k]))
    print("   not bridged       %d" % len(skips))
    print("   residue asked     %d" % asked)
    print("   residue resolved  %d" % len(resolved))
    print("   residue standing  %d" % len(remaining))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
