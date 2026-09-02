#!/usr/bin/env python3
"""probe_generate.py -- layer 3, phase 2: generate the python probes.

Plain words first. Layer 1 is the DATA (fixed content, no language). Layer 2 is
the set of ways a language can HOLD that content -- one (form, representation)
CELL per way, audited for whether it loads. Layer 3, which this script serves,
is what the COMPILER can DO to a loaded cell: operators, indexing, comparison,
iteration, arithmetic. Never builtins, never stdlib calls.

A PROBE is one measurement: one probed kind (or one anonymous token off a
grammar menu), one operand assignment drawn from the layer-2 cells, one
SPELLING MODE. It is a source snippet that ends by binding `_r`; the driver
compiles it, runs it, and prints `PROBE_ID|RESULT`.

The rules are written out for review in `probe_design.md`; this file is their
executable form. Products:

  probes_python.json   every probe: id, source, operands, family, provenance
  lanes/l3_python.sh   the SandboxDesign lane that compiles and runs them

Inherited defects, already fixed here because the layer-2 generator recorded
them (see ../data_representation/audit_generate.py docstring):

  * lane id matching is by FIXED STRING (`grep -F`): a representation's own
    name goes into its FACT_ID and `array.array` / `[T; N]` read as patterns.
  * imports are PRUNED per emitted file: only the `pre` lines of the atoms a
    file actually uses are written, so an unused import cannot refuse a file
    that would otherwise have run.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DR = os.path.join(os.path.dirname(HERE), "data_representation")

# ---------------------------------------------------------------- layer-2 in

def load_cells():
    reps = json.load(open(os.path.join(DR, "representations_python.json")))
    audit = json.load(open(os.path.join(DR, "audit", "audit_python.json")))
    verdict = {(c["form"], c["rep"]): c for c in audit["cells"]}
    spell = reps["spell"]
    cells = []
    for form, entries in reps["forms"].items():
        for entry in entries:
            cell = verdict[(form, entry["rep"])]
            if cell["verdict"] not in ("LOADS", "PARTIAL"):
                continue                      # decision 3: REFUSES-* is not an input
            cells.append((form, entry, cell))
    return cells, spell


IDENTITY_BUILD = {
    # hand-written (decision 9): the layer-2 identity probes end in a verdict
    # word, not in the object; layer 3 needs the OBJECT, so its three shapes
    # are spelled here, once per representation.
    ("list", "shared"): "_s = [1, 2, 3]\n{N} = [_s, _s]",
    ("list", "diamond"): "_t = {'payload': 7}\n{N} = [_t, _t]",
    ("list", "cycle"): "{N} = [1]\n{N}.append({N})",
    ("dict", "shared"): "_s = [1, 2, 3]\n{N} = {'left': _s, 'right': _s}",
    ("dict", "diamond"): "_t = {'payload': 7}\n{N} = {'via_a': _t, 'via_b': _t}",
    ("dict", "cycle"): "{N} = {'name': 'loop'}\n{N}['self'] = {N}",
    ("tuple", "shared"): "_s = [1, 2, 3]\n{N} = (_s, _s)",
    ("tuple", "diamond"): "_t = {'payload': 7}\n{N} = (_t, _t)",
    ("tuple", "cycle"): "_box = []\n{N} = (_box,)\n_box.append({N})",
}

BASE_CLASS = {
    "nothing": "null", "truth": "true", "whole": "base_42",
    "fractional": "base_1_5", "text": "base_hello", "sequence": "base",
    "keyed": "flat", "nesting": "seq_in_seq", "identity": "shared",
}

CANONICAL = [("nothing", "NoneType"), ("truth", "bool"), ("whole", "int"),
             ("fractional", "float"), ("text", "str"),
             ("sequence", "list"), ("keyed", "dict")]

LITERAL_RE = re.compile(r"^[-+]?[0-9][0-9_.]*$|^\"|^'|^\[|^\(|^\{|^True$|^False$|^None$")


def build_atoms():
    """Every operand a probe may use: one per loaded (form, rep, value class)."""
    cells, spell = load_cells()
    atoms = []
    for form, entry, cell in cells:
        rep = entry["rep"]
        pre = entry.get("pre") or ""
        for cls, probe in cell["probes"].items():
            if probe["judgement"] == "refused":
                continue                       # decision 3: refused edges drop out
            if form == "identity":
                build = IDENTITY_BUILD[(rep, cls)]
                expr = None
                hand = True
            elif "decl" in entry and entry["decl"]:
                rhs = entry["decl"].split(" = ", 1)[1]
                rhs = rhs.replace("{V}", spell[form][cls])
                build = "{N} = " + rhs
                expr = rhs
                hand = False
            else:
                rhs = entry["probes"][cls].split(" = ", 1)[1]
                build = "{N} = " + rhs
                expr = rhs
                hand = False
            literal = bool(expr) and entry.get("kind") == "literal" \
                and "(" not in expr.replace("(", "(", 1)[0:0] + expr \
                if False else bool(expr) and entry.get("kind") == "literal"
            if literal and not LITERAL_RE.match(expr.strip()):
                literal = False
            atoms.append({
                "id": "%s.%s.%s" % (form, rep, cls),
                "form": form, "rep": rep, "cls": cls,
                "pre": pre, "build": build, "expr": expr,
                "literal": literal, "hand_written": hand,
                "loaded_as": probe["result"], "judgement": probe["judgement"],
            })
    return atoms


# --------------------------------------------------------- operand selection

def operand_sets(atoms):
    by_id = {a["id"]: a for a in atoms}
    by_cell = {}
    for a in atoms:
        by_cell.setdefault((a["form"], a["rep"]), []).append(a)

    singles = list(atoms)                       # U: every atom

    base = {}
    for (form, rep), members in by_cell.items():
        want = BASE_CLASS[form]
        pick = [m for m in members if m["cls"] == want] or members[:1]
        base[(form, rep)] = pick[0]

    pairs, why = [], {}

    def add(a, b, reason):
        key = (a["id"], b["id"])
        if key not in why:
            why[key] = reason
            pairs.append((a, b))

    for cellkey, atom in sorted(base.items()):
        add(atom, atom, "same-cell")            # (a) X op X
    forms = {}
    for (form, rep), atom in base.items():
        forms.setdefault(form, []).append(atom)
    for form, members in sorted(forms.items()):
        for a in members:                       # (b) same form, other holder
            for b in members:
                if a["rep"] != b["rep"]:
                    add(a, b, "cross-representation")
    canon = [base[c] for c in CANONICAL]
    for a in canon:                             # (c) cross form, canonical reps
        for b in canon:
            if a["form"] != b["form"]:
                add(a, b, "cross-form")
    pivot = base[("whole", "int")]
    for cell in CANONICAL:                      # (d) the edge lane
        for atom in by_cell[cell]:
            if atom["id"] == base[cell]["id"]:
                continue
            add(atom, atom, "edge-self")
            add(atom, pivot, "edge-left")
            add(pivot, atom, "edge-right")
    return singles, pairs, why, base, by_id


# ------------------------------------------------------------------ templates
# Every template is a snippet that binds `_r`. `{X}` and `{Y}` are replaced by
# SUBSTITUTION, never by str.format, so a template may hold braces freely.
# `wrap` says how the enclosing context was obtained: "none" (depth 1),
# "generated" (depth 2 -- the else/break case: the wrapper falls out of the
# rule), "hand" (depth 3+ -- the nine written out by hand).

TIER_B = {
    # (host, slot): (template, wrap, restriction)
    ("module", "*"): ("{X}\n_r = 'stmt-ok'", "none", None),
    ("as_pattern", "*"): ("match {X}:\n    case _ as _q:\n        _r = _q", "generated", None),
    ("assert_statement", "*"): ("assert {X}\n_r = 'assert-passed'", "none", None),
    ("assignment", "right"): ("_q = {X}\n_r = _q", "none", None),
    ("attribute", "object"): ("_r = ({X}).__class__.__name__", "none", None),
    ("call", "function"): ("_r = ({X})()", "none", None),
    ("delete_statement", "*"): ("_q = {X}\ndel _q\n_r = 'deleted'", "none", None),
    ("exec_statement", "*"): ("exec {X}\n_r = 'ok'", "none", None),
    ("exec_statement", "code"): ("exec {X} in {}\n_r = 'ok'", "none", "text"),
    ("generator_expression", "body"): ("_g = ({X} for _i in [0])\n_r = [_x for _x in _g]", "none", None),
    ("lambda", "body"): ("_f = lambda: {X}\n_r = _f()", "none", None),
    ("list", "*"): ("_r = [{X}]", "none", None),
    ("list_comprehension", "body"): ("_r = [{X} for _i in [0]]", "none", None),
    ("list_splat", "*"): ("_r = [*{X}]", "none", None),
    ("match_statement", "subject"): ("match {X}:\n    case _:\n        _r = 'matched'", "none", None),
    ("named_expression", "value"): ("_r = (_q := {X})", "none", None),
    ("parenthesized_expression", "*"): ("_r = ({X})", "none", None),
    ("print_statement", "argument"): ("print {X}\n_r = 'ok'", "none", None),
    ("raise_statement", "*"): ("try:\n    raise {X}\nexcept BaseException as _e:\n    _r = 'raise-took:' + type(_e).__name__", "none", None),
    ("raise_statement", "cause"): ("try:\n    raise ValueError('x') from {X}\nexcept BaseException as _e:\n    _r = 'cause-took:' + type(_e).__name__", "none", None),
    ("return_statement", "*"): ("def _f():\n    return {X}\n_r = _f()", "none", None),
    ("set", "*"): ("_r = {{X}}", "none", None),
    ("set_comprehension", "body"): ("_r = {{X} for _i in [0]}", "none", None),
    ("tuple", "*"): ("_r = ({X},)", "none", None),
    ("tuple_expression", "*"): ("_q = {X}, {X}\n_r = _q", "none", None),
    ("yield", "*"): ("def _g():\n    yield {X}\n_r = [_x for _x in _g()]", "none", None),
    # depth 2 -- the enclosing context is GENERATED by the rule
    ("argument_list", "*"): ("def _f(_a):\n    return _a\n_r = _f({X})", "generated", None),
    ("block", "*"): ("if True:\n    _q = {X}\n_r = _q", "generated", None),
    ("case_pattern", "*"): ("match {X}:\n    case {X}:\n        _r = 'match'\n    case _:\n        _r = 'no-match'", "generated", "literal"),
    ("chevron", "*"): ("print >>{X}, 'x'\n_r = 'ok'", "generated", None),
    ("decorator", "*"): ("@{X}\ndef _g():\n    pass\n_r = 'decorated'", "generated", None),
    ("dictionary_splat", "*"): ("_r = {**{X}}", "generated", None),
    ("elif_clause", "condition"): ("if False:\n    _r = 'if'\nelif {X}:\n    _r = 'elif-true'\nelse:\n    _r = 'elif-false'", "generated", None),
    ("except_clause", "value"): ("try:\n    raise ValueError('x')\nexcept {X} as _e:\n    _r = 'caught'", "generated", None),
    ("except_clause", "alias"): ("try:\n    raise ValueError('x')\nexcept ValueError as _e:\n    _q = ({X}, _e)\n    _r = 'aliased'", "generated", None),
    ("expression_list", "*"): ("for _q in [({X}, {X})]:\n    _r = _q", "generated", None),
    ("for_in_clause", "right"): ("_r = [_i for _i in {X}]", "generated", None),
    ("if_clause", "*"): ("_r = [_i for _i in [0] if {X}]", "generated", None),
    ("interpolation", "expression"): ('_r = f"{{X}}"', "generated", None),
    ("pair", "key"): ("_r = {{X}: 1}", "generated", None),
    ("pair", "value"): ("_r = {'k': {X}}", "generated", None),
    ("type", "*"): ("def _f() -> {X}:\n    return None\n_r = 'annotated'", "generated", None),
    # depth 3+ -- the nine HAND-WRITTEN wrappers (decision 8)
    ("complex_pattern", "*"): ("match 1 + 2j:\n    case 1 + {X}j:\n        _r = 'match'\n    case _:\n        _r = 'no-match'", "hand", "number-raw"),
    ("default_parameter", "value"): ("def _f(_a={X}):\n    return _a\n_r = _f()", "hand", None),
    ("dict_pattern", "key"): ("match {'a': 1}:\n    case {{X}: _v}:\n        _r = 'match'\n    case _:\n        _r = 'no-match'", "hand", "literal-raw"),
    ("format_expression", "expression"): ('_r = f"{{X}:>7}"', "hand", None),
    ("keyword_argument", "value"): ("def _f(_k=None):\n    return _k\n_r = _f(_k={X})", "hand", None),
    ("keyword_pattern", "*"): ("class _C:\n    __match_args__ = ()\n    def __init__(self):\n        self.k = {X}\nmatch _C():\n    case _C(k={X}):\n        _r = 'match'\n    case _:\n        _r = 'no-match'", "hand", "literal"),
    ("typed_default_parameter", "value"): ("def _f(_a: object = {X}):\n    return _a\n_r = _f()", "hand", None),
    ("union_pattern", "*"): ("match {X}:\n    case {X} | 'never-this':\n        _r = 'match'\n    case _:\n        _r = 'no-match'", "hand", "literal"),
    ("with_item", "value"): ("with {X} as _w:\n    _r = 'entered'", "hand", None),
}

# slots consumed by the tier-A operation families instead of tier B
TIER_A_SLOTS = {
    ("binary_operator", "left"), ("binary_operator", "right"),
    ("comparison_operator", "*"), ("boolean_operator", "left"),
    ("boolean_operator", "right"), ("augmented_assignment", "right"),
    ("unary_operator", "argument"), ("not_operator", "argument"),
    ("subscript", "value"), ("subscript", "subscript"), ("slice", "*"),
    ("for_statement", "right"), ("if_statement", "condition"),
    ("while_statement", "condition"), ("conditional_expression", "*"),
    ("concatenated_string", "*"),
}
DEFERRED_SLOTS = {("await", "*"): "needs an event driver; no stdlib call allowed"}

BINARY_TOKENS = ["%", "&", "*", "**", "+", "-", "/", "//", "<<", ">>", "@", "^", "|"]
COMPARISON_TOKENS = ["!=", "<", "<=", "<>", "==", ">", ">=", "in", "is",
                     "is not", "not in"]
BOOLEAN_TOKENS = ["and", "or"]
UNARY_TOKENS = ["+", "-", "~"]
AUG_TOKENS = ["%=", "&=", "**=", "*=", "+=", "-=", "//=", "/=", "<<=", ">>=",
              "@=", "^=", "|="]

INDEX_SPECS = [
    ("i0", "0"), ("i1", "1"), ("ineg", "-1"), ("ibig", "9223372036854775807"),
    ("key_a", "'a'"), ("key_absent", "'absent'"), ("ifloat", "1.5"),
    ("itrue", "True"), ("inone", "None"), ("ikeytuple", "(1, 2)"),
]
SLICE_SPECS = [("s02", "0:2"), ("sall", ":"), ("srev", "::-1"),
               ("sstep2", "::2"), ("soob", "5:99"), ("sfloat", "0:1.5")]

TOKEN_SAFE = {"%": "mod", "&": "and_", "*": "mul", "**": "pow", "+": "add",
              "-": "sub", "/": "div", "//": "floordiv", "<<": "lshift",
              ">>": "rshift", "@": "matmul", "^": "xor", "|": "or_",
              "!=": "ne", "<": "lt", "<=": "le", "<>": "ne_py2", "==": "eq",
              ">": "gt", ">=": "ge", "in": "in_", "is": "is_",
              "is not": "is_not", "not in": "not_in", "and": "and_",
              "or": "or_", "~": "invert"}


def safe(token):
    """A probe id must never hold the `|` the FACT_ID|RESULT line splits on."""
    if token in TOKEN_SAFE:
        return TOKEN_SAFE[token]
    if token.endswith("=") and token[:-1] in TOKEN_SAFE:
        return TOKEN_SAFE[token[:-1]] + "_eq"
    raise ValueError("no safe spelling for token %r" % token)


# ------------------------------------------------------------------ assembly

def restricted(atom, rule):
    if rule is None:
        return True
    if rule in ("literal", "literal-raw"):
        return atom["literal"]
    if rule == "text":
        return atom["form"] == "text"
    if rule == "number-raw":
        return atom["literal"] and atom["form"] in ("whole", "fractional")
    raise ValueError(rule)


def emit(probes, pid, family, kind, token, template, operands, mode, wrap,
         note=None, raw=False):
    """Bind operands into the template and record one probe."""
    pre, build, holes = [], [], {}
    for slotname, atom in operands.items():
        if atom["pre"]:
            pre.append(atom["pre"])
        if mode == "direct" and atom["expr"] and atom["literal"]:
            holes[slotname] = atom["expr"] if raw else "(" + atom["expr"] + ")"
        else:
            name = "_a_" + slotname
            build.append(atom["build"].replace("{N}", name))
            holes[slotname] = name
    src = template
    for slotname in sorted(holes, key=len, reverse=True):
        src = src.replace("{" + slotname + "}", holes[slotname])
    body = "\n".join(dict.fromkeys(pre)) + ("\n" if pre else "")
    body += "\n".join(build) + ("\n" if build else "")
    body += src
    probes.append({
        "id": pid, "family": family, "kind": kind, "token": token,
        "mode": mode, "wrap": wrap, "src": body,
        "operands": {k: v["id"] for k, v in operands.items()},
        "operand_forms": {k: v["form"] for k, v in operands.items()},
        "operand_reps": {k: v["rep"] for k, v in operands.items()},
        "operand_classes": {k: v["cls"] for k, v in operands.items()},
        "note": note,
    })


def modes(*atoms):
    out = ["opaque"]
    if all(a["literal"] for a in atoms):
        out.append("direct")
    return out


def generate():
    atoms = build_atoms()
    singles, pairs, why, base, by_id = operand_sets(atoms)
    probes = []

    # ---- family: binary arithmetic / bitwise (R2: one probe per menu token)
    for token in BINARY_TOKENS:
        for a, b in pairs:
            tmpl = "_r = ({X}) " + token + " ({Y})"
            for mode in modes(a, b):
                pid = "bin.%s.%s.%s.%s" % (safe(token), a["id"], b["id"], mode)
                emit(probes, pid, "binary_operator", "binary_operator", token,
                     tmpl, {"X": a, "Y": b}, mode, "none")
    # ---- family: comparison (the menu carries in / is / not in / is not)
    for token in COMPARISON_TOKENS:
        for a, b in pairs:
            tmpl = "_r = ({X}) " + token + " ({Y})"
            for mode in modes(a, b):
                pid = "cmp.%s.%s.%s.%s" % (safe(token), a["id"], b["id"], mode)
                emit(probes, pid, "comparison_operator", "comparison_operator",
                     token, tmpl, {"X": a, "Y": b}, mode, "none")
    # ---- family: boolean operators
    for token in BOOLEAN_TOKENS:
        for a, b in pairs:
            tmpl = "_r = ({X}) " + token + " ({Y})"
            for mode in modes(a, b):
                pid = "bool.%s.%s.%s.%s" % (safe(token), a["id"], b["id"], mode)
                emit(probes, pid, "boolean_operator", "boolean_operator",
                     token, tmpl, {"X": a, "Y": b}, mode, "none")
    # ---- family: augmented assignment (target must be a name: opaque target)
    for token in AUG_TOKENS:
        for a, b in pairs:
            tmpl = "_t = {X}\n_t " + token + " ({Y})\n_r = _t"
            for mode in modes(b):
                pid = "aug.%s.%s.%s.%s" % (safe(token), a["id"], b["id"], mode)
                emit(probes, pid, "augmented_assignment", "augmented_assignment",
                     token, tmpl, {"X": a, "Y": b}, mode, "none",
                     note="target is always a name; mode names the right side")
    # ---- family: unary operators, and `not`
    for token in UNARY_TOKENS:
        for a in singles:
            tmpl = "_r = " + token + " ({X})"
            for mode in modes(a):
                pid = "un.%s.%s.%s" % (safe(token), a["id"], mode)
                emit(probes, pid, "unary_operator", "unary_operator", token,
                     tmpl, {"X": a}, mode, "none")
    for a in singles:
        for mode in modes(a):
            emit(probes, "not.%s.%s" % (a["id"], mode), "not_operator",
                 "not_operator", "not", "_r = not ({X})", {"X": a}, mode, "none")
    # ---- family: indexing
    for a in singles:
        for iname, ispec in INDEX_SPECS:
            tmpl = "_r = ({X})[" + ispec + "]"
            for mode in modes(a):
                pid = "idx.%s.%s.%s" % (iname, a["id"], mode)
                emit(probes, pid, "subscript", "subscript", "[", tmpl,
                     {"X": a}, mode, "none")
        for sname, sspec in SLICE_SPECS:
            tmpl = "_r = ({X})[" + sspec + "]"
            for mode in modes(a):
                pid = "slice.%s.%s.%s" % (sname, a["id"], mode)
                emit(probes, pid, "slice", "slice", ":", tmpl, {"X": a},
                     mode, "generated")
    # ---- family: iteration
    ITER = {
        "for_statement": ("_o = []\nfor _i in {X}:\n    _o = _o + [_i]\n_r = _o", "none"),
        "list_comprehension": ("_r = [_i for _i in {X}]", "none"),
        "set_comprehension": ("_r = {_i for _i in {X}}", "none"),
        "dictionary_comprehension": ("_r = {_i: 1 for _i in {X}}", "none"),
        "generator_expression": ("_g = (_i for _i in {X})\n_r = [_x for _x in _g]", "none"),
        "unpacking": ("_p, _q = {X}\n_r = (_p, _q)", "generated"),
    }
    for kind, (tmpl, wrap) in sorted(ITER.items()):
        for a in singles:
            for mode in modes(a):
                emit(probes, "iter.%s.%s.%s" % (kind, a["id"], mode),
                     "iteration", kind, None, tmpl, {"X": a}, mode, wrap)
    # ---- family: truth testing
    TRUTH = {
        "if_statement": ("if {X}:\n    _r = 'true-branch'\nelse:\n    _r = 'false-branch'", "none"),
        "while_statement": ("_n = 0\nwhile {X}:\n    _n = 1\n    break\n_r = _n", "none"),
        "conditional_expression": ("_r = 'yes' if {X} else 'no'", "none"),
    }
    for kind, (tmpl, wrap) in sorted(TRUTH.items()):
        for a in singles:
            for mode in modes(a):
                emit(probes, "truth.%s.%s.%s" % (kind, a["id"], mode),
                     "truth_test", kind, None, tmpl, {"X": a}, mode, wrap)
    # ---- family: adjacent-literal concatenation (text only, literal only)
    for a in singles:
        if a["form"] != "text" or not a["literal"]:
            continue
        emit(probes, "concat.%s.direct" % a["id"], "concatenated_string",
             "concatenated_string", None, "_r = {X} 'TAIL'", {"X": a},
             "direct", "none", raw=True)
    # ---- family: element deletion
    for a in singles:
        for iname, ispec in INDEX_SPECS[:6]:
            tmpl = "_q = {X}\ndel _q[" + ispec + "]\n_r = _q"
            emit(probes, "del.%s.%s.opaque" % (iname, a["id"]),
                 "delete_statement", "delete_statement", "del", tmpl,
                 {"X": a}, "opaque", "none")
    # ---- tier B: every remaining dominant-typed slot, one base atom per cell
    bases = [base[k] for k in sorted(base)]
    for (host, slot), (tmpl, wrap, rule) in sorted(TIER_B.items()):
        for a in bases:
            if not restricted(a, rule):
                continue
            # A pattern slot takes a LITERAL, not a name: substituting a
            # variable there spells a capture pattern, which is a different
            # probe, not the same probe opaquely spelled (decision 7).
            allowed = (["direct"] if rule in ("literal", "literal-raw",
                                              "number-raw")
                       else modes(a))
            for mode in allowed:
                pid = "place.%s.%s.%s.%s" % (host, slot.replace("*", "star"),
                                             a["id"], mode)
                emit(probes, pid, "placement", host, None, tmpl, {"X": a},
                     mode, wrap,
                     raw=rule in ("number-raw", "literal-raw"))
    return atoms, probes, pairs, why


def main():
    atoms, probes, pairs, why = generate()
    seen = {}
    for p in probes:
        if p["id"] in seen:
            raise SystemExit("duplicate probe id: " + p["id"])
        seen[p["id"]] = 1
    families = {}
    for p in probes:
        families[p["family"]] = families.get(p["family"], 0) + 1
    out = {
        "language": "python", "layer": 3,
        "rules": "probe_design.md",
        "counts": {
            "atoms": len(atoms), "operand_pairs": len(pairs),
            "probes": len(probes), "by_family": families,
            "by_mode": {m: sum(1 for p in probes if p["mode"] == m)
                        for m in ("opaque", "direct")},
            "by_wrap": {w: sum(1 for p in probes if p["wrap"] == w)
                        for w in ("none", "generated", "hand")},
        },
        "deferred": {"%s.%s" % k: v for k, v in DEFERRED_SLOTS.items()},
        "atoms": atoms,
        "operand_pairs": [{"left": a["id"], "right": b["id"],
                           "reason": why[(a["id"], b["id"])]} for a, b in pairs],
        "probes": probes,
    }
    with open(os.path.join(HERE, "probes_python.json"), "w") as h:
        json.dump(out, h, indent=1, sort_keys=True)
    print("atoms=%d pairs=%d probes=%d" % (len(atoms), len(pairs), len(probes)))
    for f, n in sorted(families.items(), key=lambda kv: -kv[1]):
        print("  %-22s %6d" % (f, n))
    print("  modes:", out["counts"]["by_mode"], "wrap:", out["counts"]["by_wrap"])


if __name__ == "__main__":
    main()
