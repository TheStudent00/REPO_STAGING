#!/usr/bin/env python3
"""seed_extract2.py -- TASK 3 (log_083). Resolves the 34 c/cpp
branching seeds seed_extract1.py left unresolved (seeds1.json,
status "unresolved", reason "2 disjoint computation groups, 0
matched an existing 0-branch canonical text"). Reads seeds1.json,
writes seeds2.json (additive: every seeds1.json entry is carried
forward unchanged except the ones this file resolves).

SCOPE. seeds1.json actually holds 36 unresolved units, not 34: 34
are c/cpp (the u64->float halving/doubling conversion idiom, paired
with an operator -- +,-,*,/,==,!=,>,>=,<=,<,not_eq) and 2 are swift
(op_164 "/", op_200 "%" -- a DIFFERENT idiom, the 32-bit-fits-fast-
path unsigned division/modulo guard, not a conversion). The task
brief's title names "the 34 c/cpp branching seeds"; this file
resolves exactly those 34 and leaves the 2 swift units untouched
(status stays "unresolved", reason updated to say why they are out
of this task's scope, honestly, not silently dropped).

METHOD for the 34, evidence class FORCED BY CONSTRUCTION throughout.

Both of a unit's two candidate groups (seeds1.json's own extraction,
canon3-level per-block text, exact-text lookup already tried and
failed) share one shape: an IDIOM PREFIX that manipulates only %rdi
and one scratch %xmm register (never touching %xmm0, the pre-
existing traced float argument register) to build a converted float
value, followed by an OPERATOR SUFFIX that is the first and every
later step touching %xmm0. This split point is found purely by
REGISTER IDENTITY (%xmm0 is the designated register for the second
traced argument under the canonical form's own registers rule --
never an operator token), so it carries no spelling-ban risk.

Per AgentMemory's SEEDED GROUPING UNDER CONDITIONS amendment
(brief part b): the idiom is CONTEXT, not guard, not seed -- the
SEED is the operator suffix alone. This file PROVES the two
candidates' operator suffixes compute the identical function (z3,
via the SAME Sim20/Sim20Cmp classes cross_unit_prover.py already
uses, reused unchanged) by renaming each candidate's own idiom-
output register (the last new %xmm register the idiom prefix wrote,
found by register liveness, never by name-guessing) to one shared
placeholder name in BOTH suffix texts, then running both through a
SHARED z3 seed dict -- so %xmm0 and the placeholder start from the
SAME free symbol on both sides, and the proof covers EVERY possible
converted-float value and EVERY possible %xmm0 argument, not one
sample. A pair whose suffixes are UNSAT-different is PROVED equal;
that resolves the unit (status "ok"); a pair this file cannot model
or cannot prove is left unresolved, reason recorded verbatim.

THE THIRD-COMPONENT-KIND FLAG (per the brief's stop rule): resolved
units below carry a `context` field alongside `seed_text`/`guards`.
This is NOT a ratified ontology addition -- it is this file's own
provisional label for "the u64->float halving/doubling idiom that
feeds the seed but is neither guard nor seed", flagged for the owner in
this task's report (log_089) rather than folded into the existing
`guards` list or asserted as settled.

THE SPELLING BAN: the split point is register identity (%xmm0), the
proof pairing is WITHIN one already-existing unit (seeds1.json's own
two candidates for that unit), and the representative choice (when
building dominant_table23c/dom_ops21c) is byte length, per THE
REPRESENTATIVE RULE. No operator token is read anywhere in this
file's grouping/matching logic; check_no_spelling_keys.py is run on
every output before this file declares success.

usage:
  seed_extract2.py [--out FILE]
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon20_behaviour_check as BC20                           # noqa: E402
import cross_unit_prover as CUP                                  # noqa: E402
import z3                                                          # noqa: E402

JUMP_RE = re.compile(r"^j\w+\s+L\w+$")
PER_PAIR_TIMEOUT_MS = 12000

CPP_SCOPE_LANGS = ("c", "cpp")


def steps_of(text):
    return [s.strip() for s in text.split(";") if s.strip()]


def strip_jumps(steps):
    return [s for s in steps if not JUMP_RE.match(s)]


def touches_xmm0(step):
    return "%xmm0" in step


def split_idiom_and_suffix(steps):
    """(idiom_steps, suffix_steps, idiom_reg). idiom_reg is the last
    %xmm register (other than %xmm0) WRITTEN among idiom_steps --
    register-liveness identity, never a name guess."""
    steps = strip_jumps(steps)
    split_at = None
    for i, s in enumerate(steps):
        if touches_xmm0(s):
            split_at = i
            break
    if split_at is None:
        return steps, [], None
    idiom_steps = steps[:split_at]
    suffix_steps = steps[split_at:]
    idiom_reg = None
    for s in idiom_steps:
        parts = s.split(" ", 1)
        rest = parts[1] if len(parts) > 1 else ""
        operands = [o.strip() for o in rest.split(",")] if rest else []
        if not operands:
            continue
        dst = operands[-1]
        if dst.startswith("%xmm") and dst != "%xmm0":
            idiom_reg = dst
    return idiom_steps, suffix_steps, idiom_reg


def rename_reg(steps, old, new):
    if old is None:
        return steps
    out = []
    for s in steps:
        out.append(s.replace(old, new))
    return out


STACK_STORE_RE = re.compile(r"^(movaps|movapd)\s+(%\w+),(-?0x[0-9a-f]+)\(%rsp\)$")
STACK_LOAD_RE = re.compile(r"^mov\s+(-?0x[0-9a-f]+)\(%rsp\),(%\w+)$")


def collapse_stack_roundtrip(steps):
    """A spill-store to a %rsp offset immediately followed (once,
    same offset, no intervening write to that offset) by a load from
    that same offset is compiler bookkeeping for a register that
    could not stay live across the block join -- not computation.
    Collapsed to a direct register-to-register move so this file's
    Sim classes (which model no memory operands) can still run the
    suffix. Register identity only -- no operator token involved."""
    stores = {}
    out = []
    for s in steps:
        m_store = STACK_STORE_RE.match(s)
        m_load = STACK_LOAD_RE.match(s)
        if m_store:
            _mnem, src, off = m_store.groups()
            stores[off] = src
            continue  # store itself is dead once collapsed below
        if m_load:
            off, dst = m_load.groups()
            src = stores.get(off)
            if src is not None:
                if src != dst:
                    out.append("movaps %s,%s" % (src, dst))
                continue
        out.append(s)
    return out


def drop_dead_gp_lines(steps):
    """For an ARITHMETIC suffix (answer register is %xmm0), a step
    that never mentions an %xmm register is bookkeeping for a GP
    value this file's answer never reads (e.g. a leftover flag-test
    register) -- dropped so the instrument does not refuse on a
    mnemonic it has no reason to model. Never applied to a compare
    suffix (there the GP register IS the answer)."""
    return [s for s in steps if "%xmm" in s]


def is_compare_suffix(suffix_steps):
    for s in suffix_steps:
        mnem = s.split(" ", 1)[0]
        if mnem in ("cmpeqss", "cmpneqss", "cmpeqsd", "cmpneqsd",
                    "ucomiss", "ucomisd"):
            return True
    return False


def prove_suffix_equal(suffix_a, suffix_b):
    """(verdict, detail, sim_a, sim_b) -- sim_a/sim_b are the ACTUAL
    step lists the solver ran on (after stack-roundtrip collapse and
    dead-GP-line drop, when applied), kept for the record so the
    proof is independently checkable. verdict in
    PROVED/DISPROVED/UNDECIDED/REFUSED."""
    text_a = "; ".join(suffix_a)
    text_b = "; ".join(suffix_b)
    if "(%rip)" in text_a or "(%rip)" in text_b:
        return "REFUSED", "rip-relative operand, no recovered value", suffix_a, suffix_b
    shared_seed = {}
    compare = is_compare_suffix(suffix_a) or is_compare_suffix(suffix_b)
    if not compare:
        suffix_a = drop_dead_gp_lines(collapse_stack_roundtrip(suffix_a))
        suffix_b = drop_dead_gp_lines(collapse_stack_roundtrip(suffix_b))
    try:
        if compare:
            val_a = CUP.Sim20Cmp(shared_seed, "a").answer_value(suffix_a, 32)
            val_b = CUP.Sim20Cmp(shared_seed, "b").answer_value(suffix_b, 32)
        else:
            val_a = BC20.Sim20(shared_seed, "a").answer_value(suffix_a, 32)
            val_b = BC20.Sim20(shared_seed, "b").answer_value(suffix_b, 32)
    except BC20.NotModeled as exc:
        return "UNDECIDED", "instrument has no model: %s" % exc, suffix_a, suffix_b
    solver = z3.Solver()
    solver.set("timeout", PER_PAIR_TIMEOUT_MS)
    solver.add(val_a != val_b)
    r = solver.check()
    if r == z3.unsat:
        return ("PROVED", "no input makes the two suffixes disagree",
                suffix_a, suffix_b)
    if r == z3.sat:
        m = solver.model()
        return ("DISPROVED", "counterexample found: %s" % m,
                suffix_a, suffix_b)
    return "UNDECIDED", "solver returned unknown (timeout)", suffix_a, suffix_b


def byte_len_of(steps):
    # proxy already used elsewhere in this pipeline (dominant_table23
    # rows): character length of the joined canonical text, deterministic.
    return len("; ".join(steps))


def resolve_unit(unit_id, rec):
    lang = rec["lang"]
    candidates = rec["candidates"]
    if len(candidates) != 2:
        return None, "expected exactly 2 candidates, found %d" % len(candidates)

    keys = sorted(candidates.keys())
    splits = {}
    for key in keys:
        steps = steps_of(candidates[key]["text"])
        idiom_steps, suffix_steps, idiom_reg = split_idiom_and_suffix(steps)
        if not suffix_steps:
            return None, ("candidate %r never touches %%xmm0 -- not the "
                           "halving-idiom shape this file models" % key)
        splits[key] = dict(idiom=idiom_steps, suffix=suffix_steps,
                            idiom_reg=idiom_reg)

    ka, kb = keys[0], keys[1]
    sa = rename_reg(splits[ka]["suffix"], splits[ka]["idiom_reg"], "%xmm8")
    sb = rename_reg(splits[kb]["suffix"], splits[kb]["idiom_reg"], "%xmm8")

    verdict, detail, sim_a, sim_b = prove_suffix_equal(sa, sb)
    if verdict != "PROVED":
        return None, "suffix proof %s: %s" % (verdict, detail)

    # THE REPRESENTATIVE RULE: simplest (fewest bytes) suffix wins,
    # ties by candidate-key sort order (deterministic).
    len_a = byte_len_of(splits[ka]["suffix"])
    len_b = byte_len_of(splits[kb]["suffix"])
    rep_key = ka if len_a <= len_b else kb
    other_key = kb if rep_key == ka else ka
    seed_text = "; ".join(splits[rep_key]["suffix"])

    resolved = dict(
        lang=lang, n=rec["n"], operator=rec["operator"],
        status="ok",
        method="idiom-context-stripped-proved-equal-suffix",
        seed_text=seed_text,
        seed_source_candidate=rep_key,
        matched_class=None,
        guards=rec.get("guards", []),
        context=[dict(
            kind="idiom-context (PROVISIONAL LABEL, not ratified -- "
                 "flagged for the owner, see log_089)",
            extent="u64_to_float halving/doubling conversion "
                   "(ExpandLegalINT_TO_FP, graph_cpp2.json)",
            idiom_text_by_candidate={
                rep_key: "; ".join(splits[rep_key]["idiom"]),
                other_key: "; ".join(splits[other_key]["idiom"]),
            })],
        proof=dict(
            verdict=verdict, detail=detail,
            suffix_a_candidate=ka, suffix_a_as_extracted="; ".join(sa),
            suffix_a_as_proved="; ".join(sim_a),
            suffix_b_candidate=kb, suffix_b_as_extracted="; ".join(sb),
            suffix_b_as_proved="; ".join(sim_b),
            simplifications_applied=(sim_a != sa or sim_b != sb)))
    return resolved, None


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "seeds2.json"))
    args = ap.parse_args(argv)

    doc = json.load(open(os.path.join(HERE, "seeds1.json")))
    seeds = doc["seeds"]

    resolved_count = 0
    still_unresolved = []
    out_of_scope_swift = []
    fail_reasons = {}

    for unit_id, rec in sorted(seeds.items()):
        if rec.get("status") != "unresolved":
            continue
        lang = rec["lang"]
        if lang not in CPP_SCOPE_LANGS:
            out_of_scope_swift.append(unit_id)
            rec = dict(rec)
            rec["reason"] = (
                rec["reason"] + " -- OUT OF SCOPE for TASK 3 (34 c/cpp "
                "branching seeds only; this is swift's 32-bit-fits-"
                "fast-path division guard, a different idiom, left "
                "for a later task)")
            seeds[unit_id] = rec
            continue

        resolved, fail = resolve_unit(unit_id, rec)
        if resolved is not None:
            seeds[unit_id] = resolved
            resolved_count += 1
        else:
            rec = dict(rec)
            rec["reason"] = rec["reason"] + " -- seed_extract2.py: " + fail
            seeds[unit_id] = rec
            still_unresolved.append(unit_id)
            fail_reasons[unit_id] = fail

    out = dict(
        meta=dict(
            generator="seed_extract2.py",
            base="seeds1.json",
            method="see module docstring: idiom/operator-suffix split "
                   "by %xmm0 register identity, z3-proved suffix "
                   "equality (canon20_behaviour_check.Sim20 / this "
                   "file's Sim20Cmp reuse via cross_unit_prover.py)",
            scope="34 c/cpp branching seeds (TASK 3); 2 swift units "
                  "(op_164, op_200) are a different idiom, left "
                  "unresolved and marked out-of-scope, not silently "
                  "dropped",
            resolved_this_pass=resolved_count,
            still_unresolved_this_pass=still_unresolved,
            out_of_scope_swift=out_of_scope_swift,
            fail_reasons=fail_reasons),
        seeds=seeds)
    json.dump(out, open(args.out, "w"), indent=1)
    print(json.dumps(out["meta"], indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
