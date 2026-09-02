#!/usr/bin/env python3
"""log070_dominant_operators.py -- the dominant-operator construction run
over EVERY probed operator in `matrices_full_v2/`, discovery-first.

PRELIMINARY.  Nothing structural is decided here; everything is measured
and flagged.  Written for `DevComms/log_070_dominant_operators_all.md`,
generalising `log067_dominant_plus.py` (the worked example, log_068).

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree; the
OS-stopped outcome is ABORT.

the owner REJECTED grouping by operator spelling.  Families are DISCOVERED from
measured structure; spelling is used only POST-HOC as a check.  The
NAMING step is discovery-first too: every whole|whole family is tested
against EVERY census guarantee of EVERY arithmetic intention (add,
subtract, multiply, divide, modulo), so a family's name comes from what
it DOES, never from what it is spelled.

The pipeline:
  GATE      same (form_pair, level) -- which under full grids also fixes
            profile cardinality -- plus the output FORM SIGNATURE, run
            BOTH as a hard gate and as a signal only.
  IDENTITY  identical full-grid vectors contract (the settled CONTRACT
            rule).  Equality is transitive, so components and cliques
            coincide and there is no chaining hazard.  These are the
            DEFINITE families and they are what gets named.
  RELAX     every non-identical pair classified by the disagreement-kind
            classifier ruled by the owner 2026-08-23 (log_069): WINDOW-only /
            VALUE-only / MIXED.  A WINDOW-only pair is a merge candidate.
            The settled decline rule still applies: zero comparable keys
            means NO connector, so an edge needs at least one cell where
            BOTH sides answer a value.  Reported as components AND as
            maximal cliques; neither is chosen.
  NAME      `+`/`-`/`*` -> wrapping / growing / approximating; `/` ->
            F-i3 float / truncating / flooring; `%` -> F-i4 divisor-sign
            / dividend-sign / Euclidean.  No fit -> UNCLASSIFIED.
  SPELLING  post-hoc only.
"""

import collections
import csv
import datetime
import decimal
import hashlib
import json
import os
import sys
from fractions import Fraction

import numpy as np

csv.field_size_limit(10 ** 9)
decimal.getcontext().prec = 120
MANT_DIGITS = 31

HERE = os.path.dirname(os.path.abspath(__file__))
FULL = os.path.join(HERE, "matrices_full_v2")
SEP = ";"
OUT_JSON = os.path.join(HERE, "dominant_operators_v1.json")
CLIQUE_CAP = 400000

DECLINE_EXACT = {"REFUSE", "ABORT"}
NOT_ASKED = "UNREPRESENTABLE"


# ------------------------------------------------------------------
# cell reading
# ------------------------------------------------------------------

def is_value(c):
    return not (c in DECLINE_EXACT or c == NOT_ASKED or c.startswith("RAISE:"))


def out_form(c):
    """the FORM of an answered cell, at the grain the canon actually
    carries.  LIMIT, stated not hidden: the canon does NOT record the
    output holder, so whole and fractional are one `number` here."""
    if c.startswith("[") or c == "nan":
        return "number"
    if c in ("true", "false"):
        return "truth"
    if c == "null":
        return "nothing"
    if c.startswith("t|"):
        return "text"
    if c.startswith("c|"):
        return "container"
    if c.startswith("opaque:"):
        return "opaque"
    return "UNKNOWN-FORM"


def out_shape(c):
    """the ontology's own coarser notion -- ruby `&` on TrueFalse yields
    five SHAPES: true, false, a number and two different raises."""
    return out_form(c) if is_value(c) else c


# ------------------------------------------------------------------
# canon, reimplemented (no project canon code imported)
# ------------------------------------------------------------------

def canon(fr):
    if fr == 0:
        return "[1, 0.0, 0]"
    sign = 1 if fr > 0 else -1
    a = abs(fr)
    e = a.numerator.bit_length() - a.denominator.bit_length()
    if Fraction(2) ** e > a:
        e -= 1
    mant = a / (Fraction(2) ** e)
    d = decimal.Decimal(mant.numerator) / decimal.Decimal(mant.denominator)
    q = d.quantize(decimal.Decimal(1).scaleb(-MANT_DIGITS))
    s = format(q, "f").rstrip("0")
    if s.endswith("."):
        s += "0"
    return "[%d, %s, %d]" % (sign, s, e)


def parse_spelling(s):
    s = s.strip()
    neg = s.startswith("-")
    if neg:
        s = s[1:]
    if "^" in s:
        base, rest = s.split("^", 1)
        assert base == "2"
        k, tail = rest, ""
        for i, ch in enumerate(rest):
            if ch in "+-":
                k, tail = rest[:i], rest[i:]
                break
        v = 1 << int(k)
        if neg:
            v = -v
        if tail:
            v = v + int(tail)
        return v
    return -int(s) if neg else int(s)


# ------------------------------------------------------------------
# the census vocabulary, as predictions -- INTENTION x GUARANTEE
# ------------------------------------------------------------------

# WIDTH IS A HOLDER PROPERTY, NOT A GUARANTEE (census F-i1), so every
# declared width in the twelve languages rides under the ONE name
# `wrapping`.  128 is here because cpp's `__int128` and rust's `i128`
# are declared holders in this run.
WIDTHS = (8, 16, 32, 64, 128)
INT64_LO, INT64_HI = -(1 << 63), (1 << 63) - 1
INTENTIONS = {"add": "+", "sub": "-", "mul": "*", "div": "/", "mod": "%"}


def wrap(v, w, signed):
    m = 1 << w
    v = v % m
    if signed and v >= (m >> 1):
        v -= m
    return v


def _step(guarantee, op, x, y):
    if x is None or y is None:
        return None
    tx, a = x
    ty, b = y
    if tx == "f" or ty == "f":
        fa = a if tx == "f" else _tofloat(a)
        fb = b if ty == "f" else _tofloat(b)
        if fa is None or fb is None:
            return None
        try:
            if op == "+":
                return ("f", fa + fb)
            if op == "-":
                return ("f", fa - fb)
            if op == "*":
                return ("f", fa * fb)
            if op == "/":
                return None if fb == 0 else ("f", fa / fb)
        except (OverflowError, ZeroDivisionError):
            return None
        return None
    if op in ("+", "-", "*"):
        s = a + b if op == "+" else (a - b if op == "-" else a * b)
        fam = guarantee.split("/")[0]
        if fam == "growing":
            return ("i", s)
        if fam == "wrapping":
            _, w, sg = guarantee.split("/")
            return ("i", wrap(s, int(w), sg == "signed"))
        if fam == "approximating":
            if INT64_LO <= s <= INT64_HI:
                return ("i", s)
            fa, fb = _tofloat(a), _tofloat(b)
            if fa is None or fb is None:
                return None
            try:
                return ("f", fa + fb if op == "+"
                        else (fa - fb if op == "-" else fa * fb))
            except OverflowError:
                return None
        return None
    if op == "/":
        if b == 0:
            return None
        fam = guarantee.split("/")[0]
        if fam == "float":
            fa, fb = _tofloat(a), _tofloat(b)
            if fa is None or fb is None:
                return None
            try:
                return ("f", fa / fb)
            except (OverflowError, ZeroDivisionError):
                return None
        if fam == "truncating":
            q = abs(a) // abs(b)
            q = -q if (a < 0) != (b < 0) else q
        elif fam == "flooring":
            q = a // b
        else:
            return None
        parts = guarantee.split("/")
        if len(parts) == 3:
            return ("i", wrap(q, int(parts[1]), parts[2] == "signed"))
        return ("i", q)
    if op == "%":
        if b == 0:
            return None
        fam = guarantee.split("/")[0]
        if fam == "dividend-sign":
            q = abs(a) // abs(b)
            q = -q if (a < 0) != (b < 0) else q
            return ("i", a - q * b)
        if fam == "divisor-sign":
            return ("i", a - (a // b) * b)
        if fam == "euclidean":
            return ("i", a - abs(b) * (a // abs(b)))
        return None
    return None


def _tofloat(v):
    try:
        return float(v)
    except OverflowError:
        return None


def guarantees_for(op):
    if op in ("+", "-", "*"):
        out = ["growing", "approximating/64"]
        for w in WIDTHS:
            out.append("wrapping/%d/signed" % w)
            out.append("wrapping/%d/unsigned" % w)
        return out
    if op == "/":
        out = ["float", "truncating", "flooring"]
        for w in WIDTHS:
            for sg in ("signed", "unsigned"):
                out.append("truncating/%d/%s" % (w, sg))
                out.append("flooring/%d/%s" % (w, sg))
        return out
    if op == "%":
        return ["dividend-sign", "divisor-sign", "euclidean"]
    return []


CENSUS_NAME = {
    "growing": "growing", "approximating": "approximating",
    "wrapping": "wrapping",
    "float": "float (F-i3)", "truncating": "truncating (F-i3)",
    "flooring": "flooring (F-i3)",
    "dividend-sign": "dividend-sign (F-i4)",
    "divisor-sign": "divisor-sign (F-i4)",
    "euclidean": "Euclidean (F-i4)",
}


def census_name(tag):
    """`add/wrapping/64/signed` -> `add wrapping`.  Width and signedness
    are HOLDER properties, not guarantees (census F-i1)."""
    intent, guarantee = tag.split("/", 1)
    return "%s %s" % (intent, CENSUS_NAME.get(guarantee.split("/")[0],
                                              guarantee))


def named_region_masks(pts, n):
    """whole|whole L1 only: name -> a boolean mask over the 289 keys.  The
    catalogue the region test draws on -- `one operand negative`,
    `magnitude past a limit`, `the exact result outside a width`.  A pair
    whose disagreement mask IS one of these has a describable boundary."""
    out = collections.OrderedDict()

    def build(name, fn):
        m = np.zeros(n * n, dtype=bool)
        for i, a in enumerate(pts):
            for j, b in enumerate(pts):
                try:
                    m[i * n + j] = bool(fn(a, b))
                except Exception:
                    pass
        if m.any() and not m.all():
            out[name] = m

    build("one operand negative", lambda a, b: a < 0 or b < 0)
    build("both operands negative", lambda a, b: a < 0 and b < 0)
    build("the left operand negative", lambda a, b: a < 0)
    build("the right operand negative", lambda a, b: b < 0)
    build("exactly one operand negative", lambda a, b: (a < 0) != (b < 0))
    build("the right operand zero", lambda a, b: b == 0)
    build("the left operand zero", lambda a, b: a == 0)
    build("either operand zero", lambda a, b: a == 0 or b == 0)
    for k in (31, 32, 53, 63):
        build("an operand at or past 2^%d in magnitude" % k,
              lambda a, b, k=k: abs(a) >= (1 << k) or abs(b) >= (1 << k))
        build("the right operand at or past 2^%d in magnitude" % k,
              lambda a, b, k=k: abs(b) >= (1 << k))
        build("the left operand at or past 2^%d in magnitude" % k,
              lambda a, b, k=k: abs(a) >= (1 << k))
    for intent, op in INTENTIONS.items():
        for w in WIDTHS:
            build("the exact `%s` result outside signed %d" % (op, w),
                  lambda a, b, op=op, w=w: not (
                      -(1 << (w - 1)) <= _exact(op, a, b) <= (1 << (w - 1)) - 1))
            build("the exact `%s` result outside unsigned %d" % (op, w),
                  lambda a, b, op=op, w=w: not (
                      0 <= _exact(op, a, b) <= (1 << w) - 1))
    return out


def _exact(op, a, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        return 0 if b == 0 else abs(a) // abs(b) * (-1 if (a < 0) != (b < 0) else 1)
    if op == "%":
        return 0 if b == 0 else a - b * (a // b)
    return 0


def _canon_of(v):
    t, x = v
    if t == "i":
        return canon(Fraction(x))
    if x != x:
        return "nan"
    if x in (float("inf"), float("-inf")):
        return "[1, inf]" if x > 0 else "[-1, inf]"
    return canon(Fraction(x))


def all_predictions(pts, level):
    """tag -> list of predicted canon strings (None where the guarantee
    leaves the key undefined, e.g. a zero divisor)."""
    out = collections.OrderedDict()
    for intent, op in INTENTIONS.items():
        for g in guarantees_for(op):
            tag = "%s/%s" % (intent, g)
            vec = []
            if level == 1:
                for a in pts:
                    for b in pts:
                        r = _step(g, op, ("i", a), ("i", b))
                        vec.append(None if r is None else _canon_of(r))
            else:
                for a in pts:
                    for b in pts:
                        left = _step(g, op, ("i", a), ("i", b))
                        for c in pts:
                            for d in pts:
                                right = _step(g, op, ("i", c), ("i", d))
                                r = _step(g, op, left, right)
                                vec.append(None if r is None
                                           else _canon_of(r))
            out[tag] = vec
    return out


# ------------------------------------------------------------------
# load
# ------------------------------------------------------------------

def load():
    idx = json.load(open(os.path.join(FULL, "index.json")))
    grid = idx["grid_sizes"]
    spell_of = {}
    for k, v in idx["matrices"].items():
        spell_of[(v["language"], v["file"].split(".")[1],
                  v["level"])] = v["operator"]

    blocks = collections.defaultdict(lambda: collections.OrderedDict())
    profiles = []
    card_violations = 0
    for fn in sorted(os.listdir(FULL)):
        if not fn.endswith(".csv"):
            continue
        parts = fn[:-4].split(".")
        lang, tok, lvl = parts[0], parts[1], int(parts[2][1:])
        sp = spell_of.get((lang, tok, lvl), tok)
        for r in csv.DictReader(open(os.path.join(FULL, fn))):
            block = (r["form_pair"], int(r["level"]))
            if int(r["n_probes"]) != grid["%s/L%d" % block]:
                card_violations += 1
            vs = r["output_canon_vector"]
            h = hashlib.blake2b(vs.encode(), digest_size=16).digest()
            slot = blocks[block].setdefault(h, dict(vec=vs, members=[]))
            pid = len(profiles)
            profiles.append(dict(
                idx=pid, lang=lang, tok=tok, sp=sp, level=lvl, block=block,
                lhs=r["lhs_holder"], rhs=r["rhs_holder"],
                probe_id=r["probe_id"], n_values=int(r["n_values"]),
                n_declines=int(r["n_declines"]),
                n_unrep=int(r["n_unrepresentable"]),
                win_a=r["src_x_set_a"].split(":")[0],
                win_b=r["src_x_set_b"].split(":")[0],
                range_a=r["src_x_set_a"].split(":", 1)[1],
                range_b=r["src_x_set_b"].split(":", 1)[1],
                vhash=h,
                key="%s.%s %s x %s" % (lang, sp, r["lhs_holder"],
                                       r["rhs_holder"])))
            slot["members"].append(pid)
    return idx, blocks, profiles, card_violations


# ------------------------------------------------------------------
# graph helpers
# ------------------------------------------------------------------

def _describe(mask, ground, named, gshape):
    """THE REGION TEST.  `mask` is the set of keys that disagree; `ground`
    is the set of keys where the question could be asked at all (for a
    value clash, the keys where BOTH sides answer a value).  Returns the
    region's description, or None for UNDESCRIBABLE -- which is FLAGGED
    for the owner, never decided."""
    if not mask.any():
        return "empty"
    if np.array_equal(mask, ground):
        return "EVERY key where the question could be asked (no boundary)"
    for nm, m in named:
        if np.array_equal(mask, m & ground):
            return nm
    g = mask.reshape(gshape)
    axes = list(range(g.ndim))
    projs = [g.any(axis=tuple(a for a in axes if a != k)) for k in axes]
    prod = projs[0]
    for pr in projs[1:]:
        prod = np.multiply.outer(prod, pr)
    if np.array_equal(prod, g):
        return ("a product region over operand subsets (%s)"
                % " x ".join(str(int(p.sum())) for p in projs))
    return None


def _keyname(p, spell, n, level):
    if level == 1:
        return "(%s, %s)" % (spell[p // n], spell[p % n])
    return "(%s, %s, %s, %s)" % (spell[(p // n ** 3) % n], spell[(p // n ** 2) % n],
                                 spell[(p // n) % n], spell[p % n])


def _bucket(v):
    if v is None:
        return "UNDESCRIBABLE -- flagged for the owner"
    if v.startswith("a product region"):
        return "a product region over operand subsets"
    return v


def components(n, adj):
    seen, out = set(), []
    for v in range(n):
        if v in seen:
            continue
        stack, comp = [v], []
        seen.add(v)
        while stack:
            u = stack.pop()
            comp.append(u)
            for w in adj[u]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        out.append(sorted(comp))
    return out


def bron_kerbosch(R, P, X, adj, out, cap):
    if len(out) > cap:
        return
    if not P and not X:
        out.append(sorted(R))
        return
    pivot = max(P | X, key=lambda u: len(adj[u] & P))
    for v in list(P - adj[pivot]):
        bron_kerbosch(R | {v}, P & adj[v], X & adj[v], adj, out, cap)
        P = P - {v}
        X = X | {v}
        if len(out) > cap:
            return


def is_clique(comp, adj):
    s = set(comp)
    return all((s - {v}) <= adj[v] for v in comp)


# ------------------------------------------------------------------
# main
# ------------------------------------------------------------------

def main():
    idx, blocks, profiles, card_violations = load()
    print("GATE -- same (form_pair, level).  Under FULL GRIDS this already")
    print("        fixes profile cardinality; VERIFIED: %d of %d profiles"
          % (card_violations, len(profiles)))
    print("        carry an n_probes different from their block's grid size.")
    print("        Input FORM, never holder.  Output form signature measured")
    print("        BOTH as a hard gate and as a signal.")
    print("  profiles %d   gate blocks %d" % (len(profiles), len(blocks)))

    whole_pts, whole_spell = {}, {}
    for lvl in (1, 2):
        sid = idx["full_sets"]["whole/L%d" % lvl]
        sp = idx["x_sets"][sid]["spellings"]
        whole_spell[lvl] = sp
        whole_pts[lvl] = [parse_spelling(s) for s in sp]
        for s, v, c in zip(sp, whole_pts[lvl], idx["x_sets"][sid]["canon"]):
            assert canon(Fraction(v)) == c, (s, canon(Fraction(v)), c)

    print("\nPREDICTIONS -- every census guarantee of every arithmetic")
    print("               intention, on whole|whole, both levels")
    PRED = {}
    for lvl in (1, 2):
        PRED[lvl] = all_predictions(whole_pts[lvl], lvl)
        print("   L%d: %d candidate tags x %d cells"
              % (lvl, len(PRED[lvl]), len(next(iter(PRED[lvl].values())))))

    report = dict(
        built=datetime.datetime.now().isoformat(timespec="seconds"),
        source="Research/kind_fuzz_clustering/matrices_full_v2/",
        status="PRELIMINARY -- measured; nothing structural decided",
        vocabulary="super-node / sub-node / co-node / sub-tree; "
                   "the OS-stopped outcome is ABORT",
        gate=dict(
            keys=["form_pair", "level"],
            cardinality_implied=True,
            cardinality_violations=card_violations,
            input_gate="FORM, never holder (the owner's ruling)",
            output_form_signature="measured BOTH as hard gate and as signal",
            output_form_grain="the canon does not carry the output holder, "
                              "so whole and fractional are one `number`"),
        blocks={}, families=[], relaxation={}, operators={},
        vocabulary_gap={}, spelling_check={}, residue=[])

    all_fams = []
    block_stats = []
    pk_total = collections.Counter()
    pk_sigcross = collections.Counter()
    relax_rows = []
    region_stats = collections.Counter()
    region_examples = []
    fam_by_hash = {}

    for block in sorted(blocks):
        fp, lvl = block
        slots = blocks[block]
        hashes = list(slots)
        d = len(hashes)
        cells = slots[hashes[0]]["vec"].count(SEP) + 1
        fa, fb = fp.split("|")
        na = len(idx["x_sets"][idx["full_sets"]["%s/L%d" % (fa, lvl)]]["spellings"])
        nb = len(idx["x_sets"][idx["full_sets"]["%s/L%d" % (fb, lvl)]]["spellings"])
        # probe_index_rule: L1 p = i0*|Xb| + i1;
        #                   L2 p = ((i0*|Xb| + i1)*|Xa| + i2)*|Xb| + i3
        gshape = (na, nb) if lvl == 1 else (na, nb, na, nb)
        assert int(np.prod(gshape)) == cells, (fp, lvl, gshape, cells)
        # the named-predicate half of the region test, keyed by packed mask
        # so a lookup is O(1) instead of a scan over the catalogue
        rlookup = []
        if fp == "whole|whole" and lvl == 1:
            rlookup = list(named_region_masks(whole_pts[1], na).items())
        allcells = np.ones(cells, dtype=bool)

        codes = np.zeros((d, cells), dtype=np.int32)
        vmask = np.zeros((d, cells), dtype=bool)
        interned = {}
        sigs, shapes = [], []
        for i, h in enumerate(hashes):
            v = slots[h]["vec"].split(SEP)
            row = codes[i]
            mrow = vmask[i]
            f, sh = set(), set()
            for p, c in enumerate(v):
                cc = interned.get(c)
                if cc is None:
                    cc = interned[c] = len(interned)
                row[p] = cc
                iv = is_value(c)
                mrow[p] = iv
                (f.add(out_form(c)) if iv else None)
                sh.add(out_shape(c))
            sigs.append(frozenset(f))
            shapes.append(frozenset(sh))

        # ---- pairwise classification --------------------------------
        adj_sig = {i: set() for i in range(d)}
        adj_hard = {i: set() for i in range(d)}
        kinds = collections.Counter()
        no_connector = 0
        samples = collections.defaultdict(list)
        for i in range(d):
            ci, mi = codes[i], vmask[i]
            for j in range(i + 1, d):
                neq = ci != codes[j]
                nd = int(np.count_nonzero(neq))
                if nd == 0:
                    continue
                mj = vmask[j]
                both = mi & mj
                comparable = int(np.count_nonzero(both))
                vv = int(np.count_nonzero(neq & both))
                wi = int(np.count_nonzero(neq & (mi ^ mj)))
                tt = nd - vv - wi
                if vv and wi:
                    k = "MIXED"
                elif vv:
                    k = "VALUE"
                elif wi:
                    k = "WINDOW"
                else:
                    k = "DECLINE-KIND"
                kinds[k] += 1
                pk_total[k] += 1
                same_sig = sigs[i] == sigs[j]
                if not same_sig:
                    pk_sigcross[k] += 1
                if len(samples[k]) < 8:
                    samples[k].append((i, j, nd, vv, wi, tt, comparable))
                if k == "WINDOW":
                    # settled decline rule: zero comparable keys means NO
                    # connector, not a zero-weight one (CLAUDE.md)
                    if comparable == 0:
                        no_connector += 1
                        continue
                    adj_sig[i].add(j)
                    adj_sig[j].add(i)
                    if same_sig:
                        adj_hard[i].add(j)
                        adj_hard[j].add(i)
                elif k == "MIXED":
                    # THE REGION TEST.  A fracture has a boundary; noise
                    # does not.  Two tests, neither a threshold:
                    #   named    -- the disagreement set IS one of the
                    #               catalogue's named regions
                    #   product  -- the set equals the product of its own
                    #               per-operand-axis projections
                    vclash = neq & both
                    va = _describe(neq, allcells, rlookup, gshape)
                    vf = _describe(vclash, both, rlookup, gshape)
                    region_stats["whole disagreement set: " +
                                 _bucket(va)] += 1
                    region_stats["value-clash set only: " + _bucket(vf)] += 1
                    if (vf and not vf.startswith(("a product", "EVERY"))
                            and len(region_examples) < 60):
                        region_examples.append(dict(
                            block="%s/L%d" % (fp, lvl),
                            a=sorted(profiles[x]["key"]
                                     for x in slots[hashes[i]]["members"])[0],
                            b=sorted(profiles[x]["key"]
                                     for x in slots[hashes[j]]["members"])[0],
                            n_disagree=nd, n_value_clash=vv, n_window=wi,
                            whole_set=va or "UNDESCRIBABLE",
                            value_clash_set=vf))

        comp_sig = components(d, adj_sig)
        comp_hard = components(d, adj_hard)
        big = [c for c in comp_sig if len(c) > 1]
        nonclique = sum(1 for c in big if len(c) > 2 and not is_clique(c, adj_sig))
        cl = []
        bron_kerbosch(set(), set(range(d)), set(), adj_sig, cl, CLIQUE_CAP)
        clique_overflow = len(cl) > CLIQUE_CAP

        # ---- the definite families = identity classes ----------------
        codes_pred = None
        predmask = None
        if fp == "whole|whole":
            tags = list(PRED[lvl])
            codes_pred = np.zeros((len(tags), cells), dtype=np.int32)
            predmask = np.zeros((len(tags), cells), dtype=bool)
            for ti, t in enumerate(tags):
                for p, s in enumerate(PRED[lvl][t]):
                    if s is None:
                        predmask[ti, p] = False
                        codes_pred[ti, p] = -1
                    else:
                        predmask[ti, p] = True
                        codes_pred[ti, p] = interned.get(s, -2)

        for i, h in enumerate(hashes):
            mem = slots[h]["members"]
            fam = dict(
                id="%s/L%d#%d" % (fp, lvl, i),
                block="%s/L%d" % (fp, lvl),
                n_profiles=len(mem),
                output_form_signature=sorted(sigs[i]) or ["(declines only)"],
                output_shape_signature=sorted(shapes[i]),
                n_value_cells=int(np.count_nonzero(vmask[i])),
                n_cells=cells,
                members=sorted(profiles[m]["key"] for m in mem),
                spellings=sorted({profiles[m]["sp"] for m in mem}),
                spelling_counts=dict(collections.Counter(
                    profiles[m]["sp"] for m in mem)),
                languages=sorted({profiles[m]["lang"] for m in mem}),
                member_windows=sorted({
                    "%s: %s x %s" % (profiles[m]["key"], profiles[m]["win_a"],
                                     profiles[m]["win_b"]) for m in mem}),
                name="NO-VOCABULARY", fits=[])
            if fp == "whole|whole":
                mi = vmask[i]
                fits = []
                for ti, t in enumerate(tags):
                    chk = mi & predmask[ti]
                    if not chk.any():
                        continue
                    if np.array_equal(codes[i][chk], codes_pred[ti][chk]):
                        fits.append(t)
                fam["fits"] = fits
                cn = sorted({census_name(t) for t in fits})
                if not fits:
                    fam["name"] = "UNCLASSIFIED"
                    # the work order: WHICH census guarantee comes closest,
                    # and at which keys does it fail?  A gap is only a work
                    # order if it names the cells that broke it.
                    best = None
                    for ti, t in enumerate(tags):
                        chk = mi & predmask[ti]
                        nchk = int(np.count_nonzero(chk))
                        if not nchk:
                            continue
                        bad = np.zeros(cells, dtype=bool)
                        bad[chk] = codes[i][chk] != codes_pred[ti][chk]
                        nbad = int(np.count_nonzero(bad))
                        if best is None or nbad < best[1]:
                            best = (t, nbad, nchk, np.flatnonzero(bad)[:3])
                    if best:
                        t, nbad, nchk, wit = best
                        vtxt = slots[h]["vec"].split(SEP)
                        fam["nearest_census_guarantee"] = dict(
                            tag=t, census_name=census_name(t),
                            mismatching_value_cells=nbad,
                            of_value_cells_checked=nchk,
                            witnesses=[dict(
                                key=_keyname(int(p), whole_spell[lvl], na, lvl),
                                answered=vtxt[int(p)],
                                predicted=PRED[lvl][t][int(p)])
                                for p in wit])
                elif len(cn) == 1:
                    fam["name"] = cn[0]
                else:
                    fam["name"] = "NON-DISCRIMINATING"
                    fam["consistent_with"] = cn
            fam["_i"] = i
            fam["_block"] = block
            all_fams.append(fam)
            fam_by_hash[(block, i)] = fam

        # ---- what the WINDOW-only relaxation merges -------------------
        merged_named = 0
        merged_conflict = []
        comp_detail = []
        for c in big:
            names = {fam_by_hash[(block, i)]["name"] for i in c}
            real = {n for n in names
                    if n not in ("NON-DISCRIMINATING", "UNCLASSIFIED",
                                 "NO-VOCABULARY")}
            det = dict(size=len(c),
                       n_profiles=sum(fam_by_hash[(block, i)]["n_profiles"]
                                      for i in c),
                       names=sorted(names),
                       census_names=sorted(real),
                       is_clique=is_clique(c, adj_sig),
                       spellings=sorted(set().union(
                           *[set(fam_by_hash[(block, i)]["spellings"])
                             for i in c])),
                       languages=sorted(set().union(
                           *[set(fam_by_hash[(block, i)]["languages"])
                             for i in c])),
                       sample_members=[fam_by_hash[(block, i)]["members"][0]
                                       for i in c[:14]])
            comp_detail.append(det)
            if len(real) > 1:
                merged_conflict.append(dict(det, block="%s/L%d" % (fp, lvl)))
            elif len(real) == 1:
                merged_named += 1
        relax_rows.append(dict(
            block="%s/L%d" % (fp, lvl),
            identity_families=d,
            window_edges=sum(len(a) for a in adj_sig.values()) // 2,
            window_edges_refused_no_comparable_cell=no_connector,
            components=len(comp_sig),
            components_larger_than_one=len(big),
            largest_component=max((len(c) for c in comp_sig), default=0),
            components_that_are_not_cliques=nonclique,
            maximal_cliques=("> %d" % CLIQUE_CAP) if clique_overflow else len(cl),
            hard_gate_components=len(comp_hard),
            hard_gate_largest=max((len(c) for c in comp_hard), default=0),
            merged_groups_keeping_one_name=merged_named,
            merged_groups_mixing_TWO_names=len(merged_conflict),
            conflicts=merged_conflict[:20],
            component_detail=comp_detail))

        block_stats.append(dict(
            block="%s/L%d" % (fp, lvl), cells=cells,
            profiles=sum(len(slots[h]["members"]) for h in hashes),
            identity_families=d,
            distinct_output_form_signatures=len(set(sigs)),
            distinct_output_shape_signatures=len(set(shapes)),
            pairs=sum(kinds.values()),
            WINDOW=kinds["WINDOW"], VALUE=kinds["VALUE"],
            MIXED=kinds["MIXED"], DECLINE_KIND=kinds["DECLINE-KIND"]))
        report["blocks"]["%s/L%d" % (fp, lvl)] = dict(
            block_stats[-1],
            sample_pairs={
                k: [dict(a=sorted(profiles[x]["key"]
                                  for x in slots[hashes[t[0]]]["members"])[0],
                         b=sorted(profiles[x]["key"]
                                  for x in slots[hashes[t[1]]]["members"])[0],
                         n_disagree=t[2], value_clash=t[3], window=t[4],
                         decline_kind=t[5], comparable_cells=t[6])
                    for t in v] for k, v in samples.items()})
        print("  %-24s cells=%-5d prof=%-5d identity=%-4d  W=%-6d V=%-5d "
              "M=%-7d D=%-4d | comps=%-4d (max %-4d) cliques=%-8s hardgate=%d"
              % ("%s/L%d" % (fp, lvl), cells, block_stats[-1]["profiles"], d,
                 kinds["WINDOW"], kinds["VALUE"], kinds["MIXED"],
                 kinds["DECLINE-KIND"], len(comp_sig),
                 relax_rows[-1]["largest_component"],
                 relax_rows[-1]["maximal_cliques"], len(comp_hard)))
        del codes, vmask, codes_pred, predmask

    # ---- naming tally ----------------------------------------------
    print("\nNAME -- discovery-first: every whole|whole family tested against")
    print("        every census guarantee of every arithmetic intention")
    tally = collections.Counter(f["name"] for f in all_fams)
    for k, v in tally.most_common(30):
        print("   %-34s %5d families" % (k, v))

    ww = [f for f in all_fams if f["block"].startswith("whole|whole")]
    print("   whole|whole families: %d   named %d   NON-DISCRIMINATING %d"
          "   UNCLASSIFIED %d"
          % (len(ww),
             sum(1 for f in ww if f["name"] not in
                 ("UNCLASSIFIED", "NON-DISCRIMINATING")),
             sum(1 for f in ww if f["name"] == "NON-DISCRIMINATING"),
             sum(1 for f in ww if f["name"] == "UNCLASSIFIED")))

    # ---- post-hoc spelling check ------------------------------------
    span = [f for f in all_fams if len(f["spellings"]) > 1]
    byspell = collections.defaultdict(lambda: collections.defaultdict(list))
    for f in all_fams:
        for s in f["spellings"]:
            byspell[s][f["block"]].append(f["id"])
    splits = {}
    for s, dd in byspell.items():
        bad = {b: v for b, v in dd.items() if len(v) > 1}
        if bad:
            splits[s] = bad
    span_real = [f for f in span if f["n_value_cells"] > 0]
    span_vac = [f for f in span if f["n_value_cells"] == 0]
    print("\nPOST-HOC SPELLING CHECK")
    print("   families holding MORE THAN ONE spelling: %d of %d" % (len(span),
                                                                    len(all_fams)))
    print("     of those, VACUOUS -- the shared vector holds no value cell at")
    print("     all, so the spellings contracted on declines only: %d"
          % len(span_vac))
    print("     of those, carrying real evidence (>=1 value cell): %d"
          % len(span_real))
    print("   spellings split across families inside one gate block: %d of %d"
          % (len(splits), len(byspell)))
    pairs = collections.Counter()
    pairs_vac = collections.Counter()
    for f in span:
        sps = f["spellings"]
        tgt = pairs if f["n_value_cells"] > 0 else pairs_vac
        for a in range(len(sps)):
            for b in range(a + 1, len(sps)):
                tgt[(sps[a], sps[b])] += 1
    print("   spelling pairs sharing a family that carries REAL evidence:")
    for (a, b), c in pairs.most_common(25):
        print("      `%s` + `%s`  in %d families" % (a, b, c))

    # a spelling FRACTURES when its families carry more than one census name
    spname = collections.defaultdict(set)
    for f in ww:
        if f["name"] in ("UNCLASSIFIED", "NO-VOCABULARY", "NON-DISCRIMINATING"):
            continue
        for s in f["spellings"]:
            spname[s].add(f["name"])
    frac = {s: sorted(v) for s, v in spname.items() if len(v) > 1}
    print("   SPELLINGS THAT FRACTURE -- one spelling, families carrying more")
    print("   than one census name:")
    for s, v in sorted(frac.items()):
        print("      `%s` -> %s" % (s, ", ".join(v)))
    print("   spellings that carry exactly one census name:")
    for s, v in sorted(spname.items()):
        if len(v) == 1:
            print("      `%s` -> %s" % (s, list(v)[0]))

    report["spelling_check"] = dict(
        n_families_spanning_spellings=len(span),
        n_vacuous_spanning_families=len(span_vac),
        n_real_evidence_spanning_families=len(span_real),
        spelling_pairs_sharing_a_family_real={"%s + %s" % k: v
                                              for k, v in pairs.most_common()},
        spelling_pairs_sharing_a_family_vacuous={
            "%s + %s" % k: v for k, v in pairs_vac.most_common()},
        spellings_that_fracture=frac,
        spellings_with_one_census_name={s: sorted(v)[0]
                                        for s, v in spname.items()
                                        if len(v) == 1},
        families_spanning_spellings=[
            dict(id=f["id"], block=f["block"], spellings=f["spellings"],
                 languages=f["languages"], n_profiles=f["n_profiles"],
                 name=f["name"], n_value_cells=f["n_value_cells"],
                 n_cells=f["n_cells"],
                 output_form_signature=f["output_form_signature"],
                 members=f["members"][:60]) for f in span],
        spellings_split_across_families={
            s: {b: dict(n_families=len(v), families=v[:60])
                for b, v in dd.items()} for s, dd in splits.items()})

    # ---- residue -----------------------------------------------------
    single = [f for f in all_fams if f["n_profiles"] == 1]
    report["residue"] = [dict(id=f["id"], block=f["block"],
                              member=f["members"][0], name=f["name"],
                              window=f["member_windows"][0],
                              n_value_cells=f["n_value_cells"],
                              n_cells=f["n_cells"],
                              output_form_signature=f["output_form_signature"])
                         for f in single]
    print("\nRESIDUE -- families of exactly one profile: %d of %d"
          % (len(single), len(all_fams)))
    bylang = collections.Counter(f["languages"][0] for f in single)
    print("   by language: %s" % dict(bylang.most_common()))

    # ---- the vocabulary gap map --------------------------------------
    # tiered STRUCTURALLY (by output form signature), never by spelling
    gap = [f for f in ww if f["name"] == "UNCLASSIFIED"]
    tierA = [f for f in gap if f["output_form_signature"] == ["number"]]
    tierB = [f for f in gap if f["output_form_signature"] != ["number"]]
    novoc = collections.Counter()
    for f in all_fams:
        if f["name"] == "NO-VOCABULARY":
            novoc[(f["block"], "|".join(f["spellings"]))] += 1
    print("\nVOCABULARY GAP MAP -- tiered by OUTPUT FORM SIGNATURE, not by")
    print("                      spelling; spelling is quoted post-hoc only")
    print("  TIER A -- whole|whole, answers NUMBERS, matches no census")
    print("            guarantee.  A real arithmetic-vocabulary gap: %d families"
          % len(tierA))
    ca = collections.Counter("|".join(f["spellings"]) for f in tierA)
    for s, c in ca.most_common(40):
        print("      %-22s %4d families   %d profiles"
              % (s, c, sum(f["n_profiles"] for f in tierA
                           if "|".join(f["spellings"]) == s)))
    print("  TIER B -- whole|whole, answers something OTHER than a number,")
    print("            so the arithmetic vocabulary was never applicable:"
          " %d families" % len(tierB))
    cb = collections.Counter("|".join(sorted(f["output_form_signature"]))
                             for f in tierB)
    for s, c in cb.most_common(10):
        print("      output %-22s %4d families" % (s, c))
    print("  TIER C -- outside whole|whole; the census states no guarantee")
    print("            vocabulary for these form pairs at all: %d families"
          " over %d operator x form-pair regions"
          % (sum(novoc.values()), len(novoc)))

    def famrec(f):
        return dict(id=f["id"], block=f["block"], spellings=f["spellings"],
                    languages=f["languages"], n_profiles=f["n_profiles"],
                    n_value_cells=f["n_value_cells"], n_cells=f["n_cells"],
                    members=f["members"],
                    output_form_signature=f["output_form_signature"],
                    output_shape_signature=f["output_shape_signature"],
                    member_windows=f["member_windows"],
                    nearest_census_guarantee=f.get("nearest_census_guarantee"))

    report["vocabulary_gap"] = dict(
        tier_A_arithmetic_vocabulary_gap=[famrec(f) for f in tierA],
        tier_A_by_spelling=dict(ca.most_common()),
        tier_B_not_a_number_output=[famrec(f) for f in tierB],
        tier_B_by_output_form=dict(cb.most_common()),
        tier_C_no_vocabulary_regions=[dict(block=b, spelling=s, families=c)
                                      for (b, s), c in
                                      sorted(novoc.items(),
                                             key=lambda kv: -kv[1])])

    # ---- highlights the log quotes -----------------------------------
    print("\nHIGHLIGHTS -- discovered families by census name, with the")
    print("              spellings that landed in each (POST-HOC)")
    byname = collections.defaultdict(lambda: dict(
        fams=0, profiles=0, sp=collections.Counter(),
        langs=set(), members=[]))
    for f in ww:
        if f["name"] in ("UNCLASSIFIED", "NO-VOCABULARY"):
            continue
        e = byname[f["name"] if f["name"] != "NON-DISCRIMINATING"
                   else "NON-DISCRIMINATING"]
        e["fams"] += 1
        e["profiles"] += f["n_profiles"]
        for s, c in f["spelling_counts"].items():
            e["sp"][s] += c
        e["langs"] |= set(f["languages"])
        e["members"].extend(f["members"])
    print("| census name | families | profiles | languages | spellings that landed here |")
    print("|---|---|---|---|---|")
    for nm in sorted(byname):
        e = byname[nm]
        print("| %s | %d | %d | %s | %s |"
              % (nm, e["fams"], e["profiles"], len(e["langs"]),
                 " ".join("`%s`x%d" % (s, c) for s, c in e["sp"].most_common())))
    nd = collections.defaultdict(lambda: dict(fams=0, profiles=0,
                                              sp=collections.Counter(),
                                              members=[]))
    for f in ww:
        if f["name"] != "NON-DISCRIMINATING":
            continue
        k = " | ".join(f.get("consistent_with", []))
        nd[k]["fams"] += 1
        nd[k]["profiles"] += f["n_profiles"]
        for s, c in f["spelling_counts"].items():
            nd[k]["sp"][s] += c
        nd[k]["members"].extend(f["members"])
    print("\nNON-DISCRIMINATING -- the profiles that never reach their own")
    print("   fracture inside this X set.  The EVIDENCE LIMIT, not a fault.")
    print("| consistent with | families | profiles | spellings |")
    print("|---|---|---|---|")
    for k in sorted(nd, key=lambda k: -nd[k]["profiles"]):
        e = nd[k]
        print("| %s | %d | %d | %s |"
              % (k, e["fams"], e["profiles"],
                 " ".join("`%s`" % s for s in e["sp"])))
    report["non_discriminating_rollup"] = {
        k: dict(families=e["fams"], profiles=e["profiles"],
                spellings=dict(e["sp"]), sample_members=sorted(e["members"])[:40])
        for k, e in nd.items()}

    report["census_name_rollup"] = {
        nm: dict(families=e["fams"], profiles=e["profiles"],
                 languages=sorted(e["langs"]),
                 spellings={s: c for s, c in e["sp"].most_common()},
                 sample_members=sorted(e["members"])[:60])
        for nm, e in byname.items()}

    report["families"] = [{k: v for k, v in f.items()
                           if not k.startswith("_")} for f in all_fams]
    report["block_stats"] = block_stats
    report["relaxation"] = relax_rows
    report["pair_kinds"] = dict(pk_total)
    report["pair_kinds_crossing_an_output_form_signature"] = dict(pk_sigcross)
    report["region_test"] = dict(counts=dict(region_stats),
                                 examples=region_examples)

    ops = collections.defaultdict(lambda: dict(languages=set(), fams=[],
                                               names=collections.Counter(),
                                               blocks=set()))
    for f in all_fams:
        for s in f["spellings"]:
            ops[s]["languages"] |= set(f["languages"])
            ops[s]["fams"].append(f["id"])
            ops[s]["names"][f["name"]] += 1
            ops[s]["blocks"].add(f["block"])
    report["operators"] = {
        s: dict(languages=sorted(v["languages"]), n_families=len(v["fams"]),
                blocks=sorted(v["blocks"]), names=dict(v["names"]))
        for s, v in ops.items()}

    json.dump(report, open(OUT_JSON, "w"), indent=1)
    print("\nwrote %s (%.1f MB)" % (OUT_JSON, os.path.getsize(OUT_JSON) / 1e6))

    print("\nRELAXATION -- what WINDOW-only admission merges")
    for r in relax_rows:
        print("  %-24s edges=%-6d refused(no comparable cell)=%-5d "
              "comps=%-4d >1=%-4d largest=%-4d not-cliques=%-3d "
              "one-name=%-3d TWO-names=%d"
              % (r["block"], r["window_edges"],
                 r["window_edges_refused_no_comparable_cell"],
                 r["components"], r["components_larger_than_one"],
                 r["largest_component"], r["components_that_are_not_cliques"],
                 r["merged_groups_keeping_one_name"],
                 r["merged_groups_mixing_TWO_names"]))

    print("\nSUMMARY")
    print("  distinct operator spellings processed: %d" % len(ops))
    print("  gate blocks: %d" % len(blocks))
    print("  DEFINITE families (identity / CONTRACT): %d" % len(all_fams))
    print("  pair kinds over every gate block: %s" % dict(pk_total))
    print("  of those, crossing an output-form-signature boundary: %s"
          % dict(pk_sigcross))
    print("  region test on MIXED pairs: %s" % dict(region_stats))


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    main()
