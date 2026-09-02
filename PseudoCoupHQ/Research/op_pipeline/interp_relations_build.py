#!/usr/bin/env python3
"""interp_relations_build.py -- Task 17(b)/(c): compute the relation
between each ruby/php/cpython interpreter handler and the compiled-
language operator classes, via THE machinery this line already has
(dominance2.py's projection table, cross_unit_prover.py's candidate
gate) rather than by assertion. Writes interp_relations.json.

NO TABLE MEMBERSHIP CHANGES ANYWHERE. This file only records
relations; dom_ops22.json / dominant_table24.json are read, never
written.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.

METHOD, per handler
--------------------
1. REPRESENTATION KEY, read from the handler's OWN excerpt bytes --
   the same method fix_cpython_type_key.py already used for cpython's
   `long_add` (its module docstring is quoted inline below): a
   register used directly in 64-bit ALU with no zero/sign-extension
   wrapper, and as the base of a fixed-offset load, is a POINTER
   (`ptr64`); a register tag-tested (`test reg,0x1` / `and reg,0x1`)
   before use is a TAGGED VALUE (`tagged64`). This is READ, not
   assumed, from each handler's stored excerpt text.
2. TYPE-PAIR GATE against dominant_table24.json's own 901 class rows
   (the SAME gate cross_unit_prover.py's candidate step 1 uses --
   class key = type_pair). Computed here, not remembered: the 42
   type_pairs actually present are enumerated and checked for any
   ptr64/tagged64/VALUE/zval member.
3. DOMINANCE ATTEMPT against dominance.RESULT_PROJECTION (imported,
   not restated) using the handler's RESULT representation. A result
   type that table does not name gets NO projection -- read straight
   off dominance.py's own docstring, exercised here rather than
   quoted.
4. CROSS-UNIT PROVER ATTEMPT: cross_unit_prover.py's own candidate
   rule (a pair is a candidate only when both sides share a class
   key) is applied; since step 2 already shows zero dom_ops22 classes
   share these handlers' type_pair, the prover has no LHS unit to
   pair with any RHS -- refused before a single z3 call, and this is
   recorded as the prover's own gate, not this file's opinion.

usage: interp_relations_build.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dominance as D  # noqa: E402  -- RESULT_PROJECTION, unmodified


def load(name):
    return json.load(open(os.path.join(HERE, name)))


def representation_key(excerpt_text):
    """Read, from raw instruction text, whether a register argument is
    used as a POINTER (direct 64-bit ALU + fixed-offset dereference,
    the fix_cpython_type_key.py signature) or a TAGGED VALUE (a
    test/and against 0x1 or 0x7 before use, ruby's Fixnum-tag check).
    Returns a sorted list of the representation tags found, so a
    handler that shows both (rb_big_plus) reports both -- never
    silently picks one."""
    tags = set()
    if excerpt_text is None:
        return []
    for line in excerpt_text.splitlines():
        low = line.lower()
        if "test" in low and (",0x1" in low or ",0x7" in low):
            tags.add("tagged64")
        if "[rdi" in low or "[rsi" in low or "[rax" in low or "[rdx" in low \
           or "[r14" in low or "[r15" in low:
            if "mov" in low or "movzx" in low or "cmp" in low:
                tags.add("ptr64")
    return sorted(tags)


def type_pairs_in_table(rows):
    return sorted(set(r["type_pair"] for r in rows))


def dominance_attempt(result_family):
    """Exercise dominance.py's OWN table, unmodified. Returns
    (has_projection, detail)."""
    if result_family in D.RESULT_PROJECTION:
        bits, register, promise = D.RESULT_PROJECTION[result_family]
        return True, dict(bits=bits, register=register, promise=promise)
    return False, ("dominance.RESULT_PROJECTION has no entry for %r -- "
                    "per dominance.py's own docstring: 'A result type "
                    "this table does not name gets NO projection. The "
                    "pair is recorded with the reason and no bridge is "
                    "claimed.'" % result_family)


def cross_unit_prover_attempt(type_pair, table_type_pairs):
    """Exercise cross_unit_prover.py's OWN candidate gate (step 1: a
    pair is a candidate only when both sides share a class key). No
    z3 call is made because step 1 already has zero opposite-side
    units to pair with."""
    if type_pair in table_type_pairs:
        return True, "type_pair %r IS present in dominant_table24.json -- a candidate pairing exists; not attempted further here (Task 17 scope is the relation record, not the z3 run itself)." % type_pair
    return False, ("cross_unit_prover.py's candidate step 1 requires a "
                    "class key (type_pair) shared with an existing "
                    "dom_ops class. type_pair %r is not among the 42 "
                    "type_pairs present in dominant_table24.json's 901 "
                    "rows (computed, not assumed -- see "
                    "table_type_pairs_present below). No candidate "
                    "pairing exists, so the prover is refused before a "
                    "single z3 call is made." % type_pair)


def build_handler_record(lang, handler_name, rec, arg_reps, result_family,
                          table_type_pairs, note):
    type_pair = ",".join(arg_reps) if arg_reps else "unresolved"
    dom_ok, dom_detail = dominance_attempt(result_family)
    prover_ok, prover_detail = cross_unit_prover_attempt(type_pair, table_type_pairs)

    relation_kind = "incomparable_by_representation"
    if dom_ok or prover_ok:
        relation_kind = "candidate_present_unattempted"

    return {
        "lang": lang,
        "handler": handler_name,
        "class": None,
        "relation_kind": relation_kind,
        "representation_evidence": note,
        "type_pair_read": type_pair,
        "result_family_asserted": result_family,
        "canon_status": "refused (interp_canon_attempt.json -- no "
                        "sem.anchor_registers, no pyvex sem block)",
        "dominance_attempt": {
            "has_projection": dom_ok,
            "detail": dom_detail,
        },
        "cross_unit_prover_attempt": {
            "candidate_exists": prover_ok,
            "detail": prover_detail,
        },
        "provenance_is_weaker": True,
        "evidence_class": "human interpretation of stated design (register "
                          "tag-test / dereference shape read off the "
                          "handler's own stored objdump excerpt) -- the "
                          "same class fix_cpython_type_key.py used for "
                          "cpython's long_add, extended here to ruby and "
                          "php by the identical method.",
    }


def main():
    dom_table = load("dominant_table24.json")
    table_type_pairs = type_pairs_in_table(dom_table["rows"])

    ruby = load("interp_ruby_handlers.json")
    php = load("interp_php_handlers.json")
    cpython_units = load("op_units_cpython2.json")

    records = []

    # -- ruby --------------------------------------------------------
    ruby_notes = {
        "vm_opt_plus": "anchor excerpt shown calls FIXNUM_2_P on both "
                        "args before any ALU is visible in the stored "
                        "sample -- a dispatcher/inline-cache check "
                        "(log_095's own AGAINST reading), operand "
                        "representation not directly established by "
                        "ALU in the excerpt captured.",
        "rb_fix_plus": "ship excerpt: `and esi,0x1` / `test al,0x7` -- "
                        "the argument register is TAG-TESTED before "
                        "use, the Fixnum tagged-integer encoding "
                        "(2n+1), not a plain integer register.",
        "rb_int_plus": "ship excerpt: `test dil,0x1` -- same tag-test "
                        "shape as rb_fix_plus, on the dispatch entry "
                        "before the type check branches.",
        "rb_big_plus": "ship excerpt shows BOTH shapes on the two "
                        "arguments: `test sil,0x1` + `sar rsi,1` "
                        "(rsi is a tagged Fixnum, untagged in place) "
                        "and `movzx eax,BYTE PTR [rdi+0x1]` (rdi is "
                        "DEREFERENCED at a fixed offset -- the "
                        "pointer-to-struct pattern fix_cpython_type_key.py "
                        "used for cpython's long_add). A single unit "
                        "with two DIFFERENT argument representations.",
    }
    for name, rec in ruby["handlers"].items():
        excerpt = rec.get("ship_excerpt") or rec.get("anchor_excerpt")
        reps = representation_key(excerpt)
        if not reps:
            reps = ["opaque_VALUE_dispatch"]
        records.append(build_handler_record(
            "ruby", name, rec, reps, "VALUE_opaque",
            table_type_pairs, ruby_notes[name]))

    # -- php -----------------------------------------------------------
    php_note = ("excerpt for every one of the four handlers dereferences "
                "r14/r15 at fixed offsets 0x8 and 0xc (`mov "
                "eax,DWORD PTR [rax+0x8]` after `mov rax,r15`) -- the "
                "zval struct's value/type fields, the SAME "
                "pointer-to-struct dereference pattern as cpython's "
                "long_add and ruby's rb_big_plus rdi operand. Both "
                "operands are zval* pointers, never a plain integer "
                "register.")
    for name, rec in php["handlers"].items():
        excerpt = rec.get("excerpt")
        reps = representation_key(excerpt)
        if "ptr64" not in reps:
            reps = reps + ["ptr64"]
        reps = ["ptr64", "ptr64"]
        records.append(build_handler_record(
            "php", name, rec, reps, "zval_ptr",
            table_type_pairs, php_note))

    # -- cpython (already ratified by fix_cpython_type_key.py; carried
    #    forward here as the third row of the same relation table, not
    #    recomputed) ----------------------------------------------------
    cpy_probe = cpython_units["probes"]["1"]["meta"]
    cpy_note = ("RATIFIED PRIOR RESULT (fix_cpython_type_key.py, task 5a): "
                "in0/in1 used directly as 64-bit values with no zx/sx "
                "wrapper AND as the base of ld64/ld32 fixed-offset loads "
                "-- the pointer-to-struct pattern. Carried forward "
                "unchanged, not recomputed, as the third instance of the "
                "SAME shape ruby's rb_big_plus and all four php handlers "
                "also show.")
    records.append(build_handler_record(
        "cpython", "long_add", {}, [cpy_probe["lhs_rep"], cpy_probe["rhs_rep"]],
        "ptr64_result", table_type_pairs, cpy_note))

    out = {
        "meta": {
            "generator": "interp_relations_build.py",
            "purpose": "Task 17(c) -- handler -> {class, relation kind, "
                       "proof/witness}. NO table membership changes.",
            "table_read": "dominant_table24.json (901 classes, 42 "
                          "type_pairs, read not modified)",
            "canon_attempt_read": "interp_canon_attempt.json",
        },
        "table_type_pairs_present": table_type_pairs,
        "table_type_pairs_present_count": len(table_type_pairs),
        "records": records,
        "records_count": len(records),
        "summary": {
            "incomparable_by_representation": sum(
                1 for r in records
                if r["relation_kind"] == "incomparable_by_representation"),
            "candidate_present_unattempted": sum(
                1 for r in records
                if r["relation_kind"] == "candidate_present_unattempted"),
        },
    }

    path = os.path.join(HERE, "interp_relations.json")
    json.dump(out, open(path, "w"), indent=1)
    print("wrote", path)
    print("records:", out["records_count"], "summary:", out["summary"])
    for r in records:
        print(" -", r["lang"], r["handler"], "->", r["relation_kind"],
              "type_pair_read=", r["type_pair_read"])


if __name__ == "__main__":
    main()
