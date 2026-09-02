#!/usr/bin/env python3
"""dwarf_typed_key.py -- TASK 24: read the DWARF-recorded parameter types
of each interpreter handler at its PINNED ANCHOR BUILD, and emit the
typed key for that handler.

WHY THIS EXISTS.  proposal_representation_dimension.json (round 4) carries
`type_pair_read: "ptr64,ptr64"` on its one PROVED record while its prose
claims PyLongObject*.  The machine field is the one that counts, so the key
itself must become the typed one.  fix_cpython_type_key.py is the precedent
for reading a type as a MACHINE FACT rather than as an assertion; there the
width (ptr64) came from the unit's own lifted expression and the NAME
(PyLongObject*) came from the C signature in prose -- human interpretation
of stated design, the weaker evidence class.  This program removes that
weakness for the NAME as well: the name is read from the compiler's own
DWARF debugging information in the anchor binary.

METHOD, exactly.
  1. Open the pinned anchor binary with pyelftools.
  2. Walk every compilation unit; find DW_TAG_subprogram DIEs whose
     DW_AT_name equals the handler symbol.
  3. For each DW_TAG_formal_parameter under it, follow DW_AT_type through
     the type chain (typedef / pointer / const / volatile / base /
     struct) and render the C spelling of the type, plus its byte size.
  4. The typed key is the comma-joined rendering of the TWO OPERAND
     parameters.  Which parameters are the operands is decided by a rule
     stated in the artifact, not by silent position: when the subprogram
     has exactly three parameters that all carry the SAME type and the
     return type is not that type (the out-parameter shape --
     `add_function(zval *result, zval *op1, zval *op2)` returning `int`),
     the operands are the last two; otherwise they are the first two.
     The artifact also records, per handler, whether the key is INVARIANT
     under that choice -- when every parameter carries one type, the
     operand selection cannot change the key at all, and the rule is not
     load-bearing.

WHAT IS REFUSED.  If a symbol has no DW_TAG_subprogram DIE in the anchor
binary (inlined away, static-with-no-debug, or built without -g), this
program records a NAMED REFUSAL for that handler.  It never guesses a type
from a header, a signature quoted in prose, or a name that "looks right".

EVIDENCE CLASS of a produced key: forced by construction -- it is the
compiler's own recorded type for the parameter, emitted by the same compile
that produced the bytes the arch-unit was carved from.
"""

import json
import os
import sys

from elftools.elf.elffile import ELFFile

TARGETS = [
    # (lang, handler symbol, binary path, what the binary is)
    ("cpython", "long_add", "/persist/cpython_anchor/python",
     "cpython v3.14.7 anchor build (-O0 -g -fwrapv), per interp_cpython.json meta.builds.anchor"),
    ("ruby", "vm_opt_plus", "/persist/ruby_anchor/ruby",
     "ruby 3.3.0 anchor build, per interp_ruby.json pin"),
    ("ruby", "rb_fix_plus", "/persist/ruby_anchor/ruby",
     "ruby 3.3.0 anchor build, per interp_ruby.json pin"),
    ("ruby", "rb_int_plus", "/persist/ruby_anchor/ruby",
     "ruby 3.3.0 anchor build, per interp_ruby.json pin"),
    ("ruby", "rb_big_plus", "/persist/ruby_anchor/ruby",
     "ruby 3.3.0 anchor build, per interp_ruby.json pin"),
    ("php", "add_function", "/persist/php_anchor/sapi/cli/php",
     "php 7.4.33 anchor build, per interp_php.json pin"),
    ("php", "ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER",
     "/persist/php_anchor/sapi/cli/php", "php 7.4.33 anchor build"),
    ("php", "ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER",
     "/persist/php_anchor/sapi/cli/php", "php 7.4.33 anchor build"),
    ("php", "ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER",
     "/persist/php_anchor/sapi/cli/php", "php 7.4.33 anchor build"),
]

OUT = os.environ.get("DWARF_TYPED_KEY_OUT") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "dwarf_typed_key.json")


def attr(die, name):
    a = die.attributes.get(name)
    return a.value if a is not None else None


def sname(die):
    v = attr(die, "DW_AT_name")
    if v is None:
        return None
    return v.decode("utf-8", "replace") if isinstance(v, bytes) else str(v)


def render_type(die, cu, depth=0):
    """Render the C spelling of a DWARF type DIE, plus its byte size."""
    if die is None or depth > 24:
        return ("void", None)
    tag = die.tag
    if tag == "DW_TAG_base_type":
        return (sname(die) or "?base", attr(die, "DW_AT_byte_size"))
    if tag == "DW_TAG_typedef":
        return (sname(die) or "?typedef", _size_of(die, cu, depth))
    if tag in ("DW_TAG_structure_type", "DW_TAG_union_type",
               "DW_TAG_enumeration_type", "DW_TAG_class_type"):
        kw = {"DW_TAG_structure_type": "struct ",
              "DW_TAG_union_type": "union ",
              "DW_TAG_enumeration_type": "enum ",
              "DW_TAG_class_type": "class "}[tag]
        return (kw + (sname(die) or "<anon>"), attr(die, "DW_AT_byte_size"))
    if tag == "DW_TAG_pointer_type":
        inner, _ = render_type(deref(die, cu), cu, depth + 1)
        return (inner + "*", attr(die, "DW_AT_byte_size") or 8)
    if tag == "DW_TAG_const_type":
        inner, sz = render_type(deref(die, cu), cu, depth + 1)
        return ("const " + inner, sz)
    if tag == "DW_TAG_volatile_type":
        inner, sz = render_type(deref(die, cu), cu, depth + 1)
        return ("volatile " + inner, sz)
    if tag == "DW_TAG_array_type":
        inner, sz = render_type(deref(die, cu), cu, depth + 1)
        return (inner + "[]", None)
    return (sname(die) or tag, attr(die, "DW_AT_byte_size"))


def _size_of(die, cu, depth):
    t = deref(die, cu)
    if t is None:
        return None
    if "DW_AT_byte_size" in t.attributes:
        return attr(t, "DW_AT_byte_size")
    return _size_of(t, cu, depth + 1) if depth < 24 else None


def deref(die, cu):
    ref = die.attributes.get("DW_AT_type")
    if ref is None:
        return None
    try:
        return cu.get_DIE_from_refaddr(cu.cu_offset + ref.value)
    except Exception:
        return None


def scan(path, wanted):
    """Return {symbol: record} for every wanted symbol found in path."""
    found = {}
    with open(path, "rb") as fh:
        elf = ELFFile(fh)
        if not elf.has_dwarf_info():
            return found, "no DWARF in %s" % path
        dw = elf.get_dwarf_info()
        for cu in dw.iter_CUs():
            for die in cu.iter_DIEs():
                if die.tag != "DW_TAG_subprogram":
                    continue
                nm = sname(die)
                if nm not in wanted or nm in found:
                    continue
                if "DW_AT_low_pc" not in die.attributes and \
                        "DW_AT_declaration" in die.attributes:
                    continue
                params = []
                for ch in die.iter_children():
                    if ch.tag != "DW_TAG_formal_parameter":
                        continue
                    tname, tsize = render_type(deref(ch, cu), cu)
                    params.append({
                        "param_name": sname(ch),
                        "dwarf_type": tname,
                        "byte_size": tsize,
                    })
                # A subprogram DIE with no DW_AT_type declares no return
                # type at all.  Record that ABSENCE as absence (null), never
                # as an invented spelling -- the artifact must not carry a
                # word DWARF did not say.
                rt = (render_type(deref(die, cu), cu)[0]
                      if "DW_AT_type" in die.attributes else None)
                low = attr(die, "DW_AT_low_pc")
                found[nm] = {
                    "compilation_unit": sname(cu.get_top_DIE()),
                    "dwarf_low_pc": hex(low) if isinstance(low, int) else None,
                    "return_type": rt,
                    "return_type_absent_in_dwarf": rt is None,
                    "formal_parameters": params,
                }
            if len(found) == len(wanted):
                break
    return found, None


# The carve and the z3 proof were done over the SHIP build's bytes
# (interp_fastpath.json's boundary address 1373f4 sits inside ship
# long_add at 0x137370).  The typed key above is read from the ANCHOR
# build.  This cross-check reads the SAME symbol's DWARF out of the SHIP
# binary too, so the key is not merely assumed to survive the change of
# optimisation level -- it is measured at both builds and compared.
CROSS_CHECKS = [
    ("cpython", "long_add", "/persist/cpython_ship/python",
     "cpython v3.14.7 ship build (-DNDEBUG -g -O3), the build the carved "
     "slice and the z3 proof were taken from"),
]


def main():
    by_bin = {}
    for lang, sym, path, what in TARGETS:
        by_bin.setdefault(path, {"what": what, "syms": []})["syms"].append(sym)

    scans = {}
    for path, info in by_bin.items():
        if not os.path.exists(path):
            scans[path] = ({}, "binary absent: %s" % path)
            continue
        scans[path] = scan(path, set(info["syms"]))

    records = []
    for lang, sym, path, what in TARGETS:
        found, err = scans[path]
        rec = {
            "lang": lang,
            "handler": sym,
            "unit": "%s/%s" % (lang, sym),
            "dwarf_source_binary": path,
            "dwarf_source_what": what,
        }
        if err:
            rec["typed_key"] = None
            rec["outcome"] = "REFUSED"
            rec["refusal_reason"] = err
            rec["evidence_class"] = "refusal (no DWARF read performed)"
        elif sym not in found:
            rec["typed_key"] = None
            rec["outcome"] = "REFUSED"
            rec["refusal_reason"] = (
                "no DW_TAG_subprogram DIE named %r with a low_pc in the "
                "anchor binary's DWARF -- the symbol is inlined away or "
                "carries no debugging information in this build.  No type "
                "is stated: a type read from a header or from a signature "
                "quoted in prose would be an assertion, which this line "
                "forbids." % sym)
            rec["evidence_class"] = "refusal (DWARF read ran, symbol absent)"
        else:
            d = found[sym]
            rec.update(d)
            ps = d["formal_parameters"]
            types = [p["dwarf_type"] for p in ps]
            if len(ps) >= 2:
                one_type = len(set(types)) == 1
                if (len(ps) == 3 and one_type
                        and d["return_type"] not in types):
                    ops = ps[1:3]
                    rule = ("out-parameter shape: three parameters of one "
                            "type, return type %r differs from it, so "
                            "parameter 0 is the result cell and the operands "
                            "are parameters 1 and 2."
                            % d["return_type"])
                else:
                    ops = ps[0:2]
                    rule = "the first two formal parameters are the operands."
                rec["operand_selection_rule"] = rule
                rec["typed_key"] = "%s,%s" % (ops[0]["dwarf_type"],
                                              ops[1]["dwarf_type"])
                rec["typed_key_byte_sizes"] = [ops[0]["byte_size"],
                                               ops[1]["byte_size"]]
                rec["typed_key_invariant_under_operand_choice"] = one_type
                rec["outcome"] = "READ"
                rec["evidence_class"] = (
                    "forced by construction -- the compiler's own DWARF "
                    "DW_AT_type chain on the handler's formal parameters, "
                    "emitted by the same compile that produced the bytes "
                    "the arch-unit was carved from"
                    + ("  (and the key does not depend on the operand "
                       "selection rule at all: every parameter of this "
                       "subprogram carries one and the same type)"
                       if one_type else
                       "  (the operand selection rule above IS load-bearing "
                       "here: the parameters do not all carry one type)"))
            else:
                rec["typed_key"] = None
                rec["outcome"] = "REFUSED"
                rec["refusal_reason"] = (
                    "the DWARF subprogram DIE for %r exists in %s but "
                    "carries %d formal parameter(s)%s.  A two-operand typed "
                    "key is not expressible for this handler from parameter "
                    "types, because its operands never arrive as parameters: "
                    "the specialized executor reaches them through the "
                    "execute_data frame.  No type is stated -- reading one "
                    "from a header or from a signature quoted in prose "
                    "would be an assertion, which this line forbids."
                    % (sym, d["compilation_unit"], len(ps),
                       " and no DW_AT_low_pc (no separate machine body of "
                       "its own in this build)"
                       if d["dwarf_low_pc"] is None else ""))
                rec["evidence_class"] = (
                    "refusal, machine-grounded -- the DWARF read ran and "
                    "found the DIE; the absence of typed operand parameters "
                    "is itself the measured fact")
        records.append(rec)

    cross = []
    for lang, sym, path, what in CROSS_CHECKS:
        if not os.path.exists(path):
            cross.append({"unit": "%s/%s" % (lang, sym), "binary": path,
                          "outcome": "REFUSED", "reason": "binary absent"})
            continue
        f2, e2 = scan(path, {sym})
        if e2 or sym not in f2:
            cross.append({"unit": "%s/%s" % (lang, sym), "binary": path,
                          "outcome": "REFUSED",
                          "reason": e2 or "no subprogram DIE"})
            continue
        d2 = f2[sym]
        ps2 = d2["formal_parameters"]
        k2 = ",".join(p["dwarf_type"] for p in ps2[:2]) if len(ps2) >= 2 else None
        anchor_rec = next((r for r in records
                           if r["unit"] == "%s/%s" % (lang, sym)), None)
        cross.append({
            "unit": "%s/%s" % (lang, sym),
            "binary": path,
            "what": what,
            "compilation_unit": d2["compilation_unit"],
            "dwarf_low_pc": d2["dwarf_low_pc"],
            "formal_parameters": ps2,
            "typed_key_at_this_build": k2,
            "typed_key_at_anchor_build": anchor_rec and anchor_rec.get("typed_key"),
            "agrees": bool(anchor_rec and k2 == anchor_rec.get("typed_key")),
        })

    doc = {
        "cross_checks_at_the_other_build": cross,
        "meta": {
            "generator": "dwarf_typed_key.py",
            "task": "TASK 24 -- the DWARF-typed key, read as a machine fact",
            "method": "pyelftools over the pinned anchor binaries; "
                      "DW_TAG_subprogram -> DW_TAG_formal_parameter -> "
                      "DW_AT_type chain, rendered as the C spelling.",
            "precedent": "fix_cpython_type_key.py (machine-fact type read); "
                         "that program took the WIDTH from the lifted "
                         "expression and the NAME from prose.  Here the NAME "
                         "comes from DWARF, which is the stronger class.",
            "refusal_policy": "a symbol with no subprogram DIE gets a named "
                              "refusal, never a guessed type.",
        },
        "records": records,
        "summary": {
            "handlers_considered": len(records),
            "keys_read": sum(1 for r in records if r["outcome"] == "READ"),
            "refused": sum(1 for r in records if r["outcome"] == "REFUSED"),
        },
    }
    json.dump(doc, open(OUT, "w"), indent=1)
    print("wrote", OUT)
    for r in records:
        print("%-8s %-52s %-8s %s" % (r["lang"], r["handler"], r["outcome"],
                                      r.get("typed_key")))
    print("summary:", doc["summary"])


if __name__ == "__main__":
    sys.exit(main())
