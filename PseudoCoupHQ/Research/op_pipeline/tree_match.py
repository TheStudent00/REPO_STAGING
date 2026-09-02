#!/usr/bin/env python3
"""tree_match.py -- compositional matching over the LIFTED EXPRESSION TREE.

the owner's direction (2026-08-26): the matching material is the lifted
expression tree pyvex already produces (moves already absorbed by the
sem layer's substitution-form values; register parking does not exist
in this tree at all).  Matching is SUB-TREE CONTAINMENT: unit X
contains unit Y when Y's value-expression tree appears as a sub-tree
(or block sub-structure) of X's.  Priority is intrinsic tree position:
sub-exp-1 = the root transformation producing the returned value;
sub-exp-2 = the transformations the inputs pass through on the way in.

Normalization tool: z3 (see TOOL SURVEY in the report this script's
caller filed).  A SMALL ratified rewrite set only -- z3's own
`simplify()` over bit-vector terms gives commutativity/associativity
for the hardware-commutative ops (And/Or/Xor/Add on fixed widths) and
constant folding for free; opaque VEX helper calls (DivModS64to32,
32HLto64, CCall, loads) are represented as UNINTERPRETED atoms keyed
by their own sub-tree text, so z3 still normalizes the algebra around
them without inventing semantics for helpers it was not asked about.

THE SPELLING BAN: no operator token is a key, a grouping field, or a
comparison-scope field anywhere below.  Candidate pairs for exact/
containment comparison come from the recorded operand TYPE PAIR
(machine evidence -- lhs_rep/rhs_rep), never from `operator`.  The
`operator` field appears exactly once per unit, as a display label.
"""

import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sem_anchored as SA                                    # noqa: E402

LANGS = SA.LANGS

try:
    import z3
    HAVE_Z3 = True
except Exception:
    HAVE_Z3 = False


# --------------------------------------------------------------------
# 1. parser for the prefix notation `_ser` in arch_sem.py writes.
#    leaves: "name:width" or "value:width" or "opaque[...]:width"
#            (no top-level parenthesis).
#    nodes:  "funcname(arg,arg,...)" -- funcname may itself contain
#            digits and an "@" (ex32@0, ld64/g0, ins@3).
# --------------------------------------------------------------------

def split_args(inner):
    """split a comma-joined argument list respecting nested parens."""
    out, depth, start = [], 0, 0
    for i, c in enumerate(inner):
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif c == "," and depth == 0:
            out.append(inner[start:i])
            start = i + 1
    out.append(inner[start:])
    return out


def parse_expr(s):
    """returns ("leaf", text) or ("node", name, [subtrees...])."""
    s = s.strip()
    p = s.find("(")
    if p == -1:
        return ("leaf", s)
    if not s.endswith(")"):
        return ("leaf", s)          # defensive: malformed, treat as opaque
    name = s[:p]
    inner = s[p + 1:-1]
    args = [parse_expr(a) for a in split_args(inner)] if inner else []
    return ("node", name, args)


LEAF_RE = re.compile(r"^(?P<tok>.+):(?P<width>\d+)$")

COMMUTATIVE = {"And32", "And64", "And8", "And16",
               "Or32", "Or64", "Or8", "Or16",
               "Xor32", "Xor64", "Xor8", "Xor16",
               "Add32", "Add64", "Add8", "Add16"}

# node-name -> (kind, width) for the small ratified rewrite set.
WIDTH_OF_OP = {
    "And32": 32, "And64": 64, "Or32": 32, "Or64": 64,
    "Xor32": 32, "Xor64": 64, "Add32": 32, "Add64": 64,
    "Sub32": 32, "Sub64": 64, "Not32": 32, "Not64": 64,
    "Sar32": 32, "Sar64": 64, "Shr32": 32, "Shr64": 64,
    "Shl32": 32, "Shl64": 64,
}


# --------------------------------------------------------------------
# 2. normalization.  z3 bitvector simplify with opaque atoms for
#    anything outside the small ratified rewrite set.
# --------------------------------------------------------------------

def leaf_width(text):
    m = LEAF_RE.match(text)
    return int(m.group(2)) if m else 64


def to_z3(tree, atoms):
    """tree -> z3 BitVec expression.  `atoms` maps a sub-tree's own
    canonical text to the z3 Const standing for it, so the SAME
    sub-tree (same characters) always gets the SAME atom -- this is
    what lets containment be read off the z3 term afterward."""
    kind = tree[0]
    if kind == "leaf":
        text = tree[1]
        w = leaf_width(text)
        key = text
        if key not in atoms:
            atoms[key] = z3.BitVec("atom_%d" % len(atoms), w)
        return atoms[key]

    name, args = tree[1], tree[2]
    kids = [to_z3(a, atoms) for a in args]

    if name in ("And32", "And64"):
        return kids[0] & kids[1]
    if name in ("Or32", "Or64"):
        return kids[0] | kids[1]
    if name in ("Xor32", "Xor64"):
        return kids[0] ^ kids[1]
    if name in ("Add32", "Add64"):
        return kids[0] + kids[1]
    if name in ("Sub32", "Sub64"):
        return kids[0] - kids[1]
    if name in ("Not32", "Not64"):
        return ~kids[0]
    if name in ("Sar32", "Sar64"):
        return kids[0] >> kids[1]        # arithmetic shift (signed BitVec)
    if name in ("Shr32", "Shr64"):
        return z3.LShR(kids[0], kids[1])
    if name in ("Shl32", "Shl64"):
        return kids[0] << kids[1]
    if name.startswith("zx"):
        outw = int(name[2:])
        inw = kids[0].size()
        return z3.ZeroExt(outw - inw, kids[0]) if outw > inw else kids[0]
    if name.startswith("sx"):
        outw = int(name[2:])
        inw = kids[0].size()
        return z3.SignExt(outw - inw, kids[0]) if outw > inw else kids[0]
    if name.startswith("ex"):
        # "ex32@0" / "ex32@32" -- extract `width` bits at bit-offset off.
        m = re.match(r"ex(\d+)@(\d+)$", name)
        width, off = int(m.group(1)), int(m.group(2))
        return z3.Extract(off + width - 1, off, kids[0])
    if name == "32HLto64":
        hi, lo = kids
        return z3.Concat(z3.ZeroExt(32, hi) if hi.size() < 32 else hi,
                          z3.ZeroExt(32, lo) if lo.size() < 32 else lo) \
            if False else z3.Concat(hi, lo)

    # everything else (DivModS64to32, ite, CCall/"cc", loads, opaque
    # calls, condition helpers) is OUTSIDE the small ratified rewrite
    # set: represent it as a single uninterpreted atom keyed by its
    # own full canonical text, so surrounding algebra still normalizes
    # but no semantics is invented for it.
    text = serialize(tree)
    w = 64
    if text not in atoms:
        atoms[text] = z3.BitVec("op_%d" % len(atoms), w)
    return atoms[text]


def serialize(tree):
    if tree[0] == "leaf":
        return tree[1]
    name, args = tree[1], tree[2]
    return "%s(%s)" % (name, ",".join(serialize(a) for a in args))


def normalize(expr_text):
    """returns (normalized_text, ok, note)."""
    tree = parse_expr(expr_text)
    if not HAVE_Z3:
        return expr_text, False, "z3 unavailable"
    try:
        atoms = {}
        e = to_z3(tree, atoms)
        simplified = z3.simplify(e)
        return str(simplified).replace("\n", " ").strip(), True, "z3 simplify"
    except Exception as exc:
        return expr_text, False, "z3 failed: %r" % exc


# --------------------------------------------------------------------
# 3. load every unit's blocks from the recorded sem_anchored strings.
# --------------------------------------------------------------------

def tree_size(tree):
    if tree[0] == "leaf":
        return 1
    return 1 + sum(tree_size(a) for a in tree[2])


def normal_path_block(blocks):
    """the block that actually returns the value.

    First candidate: the block whose events include 'ret' (machine
    evidence: the VEX-recorded control event).  BUT a spilled return
    (go/rust: the computed value is stored to the stack in one block
    and reloaded, via a bare tmp reference "u1", in the ret-tagged
    block) makes the ret block's OWN value tree a trivial one-node
    wrapper around an unresolved tmp -- not the computation.  In that
    case the actual computation lives in an earlier straight-line
    block (no branch away from the unit's return path), and that
    block's value tree is larger.  The selection rule is TREE SIZE,
    read off the block structure -- never the operator token."""
    ret_block = None
    for b in blocks:
        if any(ev == "ret" or (isinstance(ev, str) and ev.startswith("ret"))
               for ev in b.get("events", [])):
            ret_block = b
            break
    if ret_block is None:
        return None, "none"
    vals = ret_block.get("values", [])
    ret_size = tree_size(parse_expr(vals[0])) if vals else 0
    if ret_size > 2:
        return ret_block, "ret-tagged block"
    # fall back: the largest-tree value among blocks that are not
    # trap/panic-only tails (i.e. blocks with no 'trap' event and
    # not ending only in a call to a panic routine) -- machine
    # evidence (events list), never the operator token.
    best, best_size, best_reason = ret_block, ret_size, "ret-tagged block"
    for b in blocks:
        if b is ret_block:
            continue
        evs = b.get("events", [])
        if any(e == "trap" or (isinstance(e, str) and e.startswith("trap"))
               for e in evs):
            continue
        if any(isinstance(e, str) and e.startswith("call") for e in evs):
            continue
        for v in b.get("values", []):
            sz = tree_size(parse_expr(v))
            if sz > best_size:
                best_size, best, best_reason = sz, {"values": [v],
                                                      "events": evs}, \
                    "largest-tree fallback block %d" % b.get("block", -1)
    return best, best_reason


def load_all_units():
    out = []
    for lang in LANGS:
        path = os.path.join(HERE, "sem_anchored_%s.json" % lang)
        if not os.path.exists(path):
            print("!! missing %s" % path)
            continue
        doc = json.load(open(path))
        for n, u in doc["units"].items():
            meta = u["meta"]
            sem = u["sem"]
            rec = dict(lang=lang, n=n, operator=meta.get("operator"),
                       arity=meta.get("arity"),
                       lhs_rep=meta.get("lhs_rep"), rhs_rep=meta.get("rhs_rep"),
                       symbol=meta.get("symbol"), sem_ok=sem.get("ok"))
            if not sem.get("ok"):
                rec["refused"] = sem.get("reason", "sem not ok")
                out.append(rec)
                continue
            blocks = sem.get("blocks", [])
            npb, block_rule = normal_path_block(blocks)
            rec["block_count"] = len(blocks)
            rec["all_block_values"] = [b.get("values", []) for b in blocks]
            rec["all_block_events"] = [b.get("events", []) for b in blocks]
            rec["normal_path_block_rule"] = block_rule
            if npb is None or not npb.get("values"):
                rec["normal_path_root"] = None
                rec["note"] = "no return-bearing block with a value"
            else:
                root_text = npb["values"][0]
                norm, ok, note = normalize(root_text)
                rec["normal_path_raw"] = root_text
                rec["normal_path_root"] = norm
                rec["normalize_ok"] = ok
                rec["normalize_note"] = note
                # sub-exp-2: the input transformations, i.e. the
                # immediate children of the root node in the parsed
                # tree (intrinsic tree position, not register-derived).
                tree = parse_expr(root_text)
                if tree[0] == "node":
                    rec["subexp1_root_op"] = tree[1]
                    rec["subexp2_children"] = [serialize(a) for a in tree[2]]
                else:
                    rec["subexp1_root_op"] = None
                    rec["subexp2_children"] = []
            out.append(rec)
    return out


# --------------------------------------------------------------------
# 4. matching.  candidate set = shared operand type pair (machine
#    evidence), never the operator token.
# --------------------------------------------------------------------

def build_matches(units):
    ok_units = [u for u in units if u.get("normal_path_root")]

    # exact match: same normalized root text, restricted to units
    # sharing a type pair.
    by_typepair = defaultdict(list)
    for u in ok_units:
        by_typepair[(u["lhs_rep"], u["rhs_rep"])].append(u)

    exact = []
    for tp, members in by_typepair.items():
        groups = defaultdict(list)
        for u in members:
            groups[u["normal_path_root"]].append(u)
        for root, ms in groups.items():
            langs = sorted(set(m["lang"] for m in ms))
            if len(ms) < 2:
                continue
            exact.append(dict(
                type_pair="%s,%s" % tp,
                normalized_root=root,
                size=len(ms),
                languages=langs,
                cross_language=len(langs) > 1,
                members=[dict(lang=m["lang"], n=m["n"],
                               operator=m["operator"]) for m in ms],
            ))
    exact.sort(key=lambda c: (-c["size"], c["normalized_root"]))

    # containment: X's normal-path root CONTAINS Y's normal-path root
    # as a literal sub-string of the parsed tree (same characters,
    # a/b/uN naming) -- restricted to the same type pair as candidate
    # scope (machine evidence).
    containment = []
    for tp, members in by_typepair.items():
        for x in members:
            xt = x["normal_path_root"]
            for y in members:
                if x is y:
                    continue
                yt = y["normal_path_root"]
                if yt and xt != yt and yt in xt:
                    containment.append(dict(
                        type_pair="%s,%s" % tp,
                        container=dict(lang=x["lang"], n=x["n"],
                                        operator=x["operator"]),
                        contained=dict(lang=y["lang"], n=y["n"],
                                        operator=y["operator"]),
                    ))
    return exact, containment


# --------------------------------------------------------------------
# main
# --------------------------------------------------------------------

def main():
    units = load_all_units()
    exact, containment = build_matches(units)

    units_doc = dict(
        languages=LANGS,
        normalizer="z3 simplify (bitvector), opaque atoms for helper calls",
        total_units=len(units),
        units=[dict(
            lang=u["lang"], n=u["n"], operator=u["operator"],
            type_pair="%s,%s" % (u.get("lhs_rep"), u.get("rhs_rep")),
            sem_ok=u.get("sem_ok"),
            refused=u.get("refused"),
            block_count=u.get("block_count"),
            normal_path_block_rule=u.get("normal_path_block_rule"),
            normal_path_raw=u.get("normal_path_raw"),
            normal_path_root=u.get("normal_path_root"),
            normalize_ok=u.get("normalize_ok"),
            normalize_note=u.get("normalize_note"),
            subexp1_root_op=u.get("subexp1_root_op"),
            subexp2_children=u.get("subexp2_children"),
        ) for u in units],
    )
    matches_doc = dict(
        languages=LANGS,
        exact_normalized_root=exact,
        containment=containment,
    )

    json.dump(units_doc, open(os.path.join(HERE, "tree_units.json"), "w"),
               indent=1)
    json.dump(matches_doc, open(os.path.join(HERE, "tree_matches.json"), "w"),
               indent=1)

    print("units total:", len(units))
    print("units with normal-path root:", sum(1 for u in units
                                                if u.get("normal_path_root")))
    print("exact normalized-root clusters:", len(exact))
    print("  cross-language:", sum(1 for c in exact if c["cross_language"]))
    print("containment edges:", len(containment))
    return 0


if __name__ == "__main__":
    sys.exit(main())
