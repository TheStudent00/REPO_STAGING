#!/usr/bin/env python3
"""log067_dominant_plus.py -- the first dominant operator, as a worked
example: dominant `+` over whole numbers, built from `matrices_full_v2/`.

PRELIMINARY.  Nothing structural is decided here.  The script
ACCUMULATES by intention (every language's add on whole|whole),
PARTITIONS by behaviour under BOTH readings, and NAMES the parts
against the census's three guaranteed adds -- `wrapping`, `growing`,
`approximating` -- leaving anything that matches none of them
UNCLASSIFIED.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree; the
OS-stopped outcome is ABORT.

Readings (log_065's operationalisation, unchanged):
  VALUE      -- a cell where either side holds an outcome token is
                dropped from numerator AND denominator.
  ALL-CELLS  -- outcome tokens ride as literal answers; containment
                collapses to full-vector equality.
"""

import collections
import csv
import decimal
import json
import os
import sys
from fractions import Fraction

csv.field_size_limit(10 ** 9)
decimal.getcontext().prec = 80
MANT_DIGITS = 31

HERE = os.path.dirname(os.path.abspath(__file__))
FULL = os.path.join(HERE, "matrices_full_v2")
SEP = ";"
UNREP = "UNREPRESENTABLE"

# the accumulation set: every spelling of the add INTENTION.  `swift`'s
# `&+` is swift's own wrapping add (log_066); dart carries no add row at
# L1 at all (log_064 section 2) and is therefore absent, not excluded.
ADD_FILES = [("cpp", "cpp.plus.L1.csv", "+"),
             ("csharp", "csharp.plus.L1.csv", "+"),
             ("go", "go.plus.L1.csv", "+"),
             ("java", "java.plus.L1.csv", "+"),
             ("kotlin", "kotlin.plus.L1.csv", "+"),
             ("php", "php.plus.L1.csv", "+"),
             ("python", "python.plus.L1.csv", "+"),
             ("ruby", "ruby.plus.L1.csv", "+"),
             ("rust", "rust.plus.L1.csv", "+"),
             ("rust_release", "rust_release.plus.L1.csv", "+"),
             ("typescript", "typescript.plus.L1.csv", "+"),
             ("swift", "swift.ampplus.L1.csv", "&+")]


# ------------------------------------------------------------------
# canon -> exact number, reimplemented here (no project canon code)
# ------------------------------------------------------------------

def canon(fr):
    """exact Fraction -> the canon string, per the CLAUDE.md rule:
    `[sign, mant, expo]`, mant a DECIMAL string in [1,2) with up to 31
    fractional digits, trailing zeros stripped, one kept minimum.
    Reimplemented here; no project canon code is imported."""
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


def decode(cell):
    """`[sign, mant, expo]` -> a Fraction (ROUNDED at 31 digits, so only
    ever used for reading, never for equality)."""
    if not cell.startswith("["):
        return None
    body = cell[1:-1].split(", ")
    if len(body) != 3:
        return None
    s, mant, expo = body
    if mant in ("inf", "nan"):
        return None
    return int(s) * Fraction(mant) * (Fraction(2) ** int(expo))


def is_token(cell):
    return not cell.startswith("[")


# ------------------------------------------------------------------
# the X set, decoded once
# ------------------------------------------------------------------

def parse_spelling(s):
    """`-2^53-1`, `2^31`, `1000` -> the EXACT integer.  The X-set values
    must never be read back out of their canon strings: the canon
    mantissa is rounded at 31 digits, so `2^63-1` decoded from canon is
    not `2^63-1` and every prediction built on it would be wrong."""
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
        # the leading sign binds to the POWER, the tail is added after:
        # `-2^63+1` is -(2^63) + 1, never -(2^63 + 1)
        v = 1 << int(k)
        if neg:
            v = -v
        if tail:
            v = v + int(tail)
        return v
    return -int(s) if neg else int(s)


def whole_points(idx):
    sid = idx["full_sets"]["whole/L1"]
    spell = idx["x_sets"][sid]["spellings"]
    pts = [Fraction(parse_spelling(s)) for s in spell]
    # cross-check: every parsed point must canonise to the canon string
    # the index already records for it
    for s, v, c in zip(spell, pts, idx["x_sets"][sid]["canon"]):
        assert canon(v) == c, (s, canon(v), c)
    return spell, pts


# ------------------------------------------------------------------
# the predictions -- the three guaranteed adds, plus one unnamed
# candidate kept OUT of the vocabulary on purpose
# ------------------------------------------------------------------

def wrap(v, w, signed):
    m = 1 << w
    v = v % m
    if signed and v >= (m >> 1):
        v -= m
    return v


def nearest_double(v):
    """exact value of the binary64 nearest to v (correctly rounded)."""
    f = float(v)
    if f in (float("inf"), float("-inf")):
        return None
    return Fraction(f)


def predictions(a, b):
    """name -> exact predicted answer (or None where undefined)."""
    s = a + b
    out = {"growing": s}
    for w in (8, 16, 32, 64):
        out["wrapping/%d/signed" % w] = wrap(int(s), w, True)
        out["wrapping/%d/unsigned" % w] = wrap(int(s), w, False)
    # php's rule: exact while it fits the holder's signed range, the
    # nearest double once it does not
    lo, hi = -(1 << 63), (1 << 63) - 1
    out["approximating/64"] = s if lo <= s <= hi else nearest_double(s)
    # NOT one of the three guaranteed adds -- carried only so a part
    # that matches it can be reported as UNCLASSIFIED with a reason
    out["(double-rounded, unnamed)"] = nearest_double(s)
    return out


# ------------------------------------------------------------------
# load
# ------------------------------------------------------------------

def load():
    idx = json.load(open(os.path.join(FULL, "index.json")))
    spell, pts = whole_points(idx)
    n = len(pts)
    profiles = []
    for lang, fn, opname in ADD_FILES:
        p = os.path.join(FULL, fn)
        if not os.path.exists(p):
            print("  !! MISSING %s" % fn)
            continue
        for r in csv.DictReader(open(p)):
            if r["form_pair"] != "whole|whole" or r["level"] != "1":
                continue
            vec = r["output_canon_vector"].split(SEP)
            assert len(vec) == n * n == int(r["n_probes"])
            profiles.append(dict(
                lang=lang, op=opname, probe_id=r["probe_id"],
                lhs=r["lhs_holder"], rhs=r["rhs_holder"], vec=vec,
                key="%s.%s %s x %s" % (lang, opname, r["lhs_holder"],
                                       r["rhs_holder"]),
                n_values=int(r["n_values"]),
                n_declines=int(r["n_declines"]),
                n_unrep=int(r["n_unrepresentable"])))
    return idx, spell, pts, profiles


# ------------------------------------------------------------------
# classification against the guaranteed adds
# ------------------------------------------------------------------

def classify(profiles, pts):
    n = len(pts)
    pred = {}
    for i, a in enumerate(pts):
        for j, b in enumerate(pts):
            pred[i * n + j] = predictions(a, b)
    names = sorted(next(iter(pred.values())).keys())
    # predictions are compared as CANON STRINGS -- the canon mantissa is
    # a 31-digit decimal, so decoding it back is lossy and an exact
    # numeric comparison would be wrong
    cpred = {p: {nm: (None if q is None else canon(Fraction(q)))
                 for nm, q in d.items()} for p, d in pred.items()}
    for pr in profiles:
        fits = set(names)
        seen = 0
        for p, cell in enumerate(pr["vec"]):
            if is_token(cell):
                continue
            seen += 1
            for nm in list(fits):
                if cpred[p][nm] != cell:
                    fits.discard(nm)
        pr["fits"] = fits
        pr["n_value_cells"] = seen
    return pred, names


# ------------------------------------------------------------------
# the two readings
# ------------------------------------------------------------------

def allcells_parts(profiles):
    parts = collections.OrderedDict()
    for pr in profiles:
        parts.setdefault(SEP.join(pr["vec"]), []).append(pr)
    return list(parts.values())


def value_compatible(a, b):
    """no conflict at any cell where BOTH hold a value, and at least
    one such cell exists."""
    shared = 0
    for x, y in zip(a["vec"], b["vec"]):
        if is_token(x) or is_token(y):
            continue
        shared += 1
        if x != y:
            return False, shared
    return shared > 0, shared


def components(nodes, adj):
    seen, out = set(), []
    for v in nodes:
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


def bron_kerbosch(R, P, X, adj, out):
    if not P and not X:
        out.append(sorted(R))
        return
    pivot = max(P | X, key=lambda u: len(adj[u] & P))
    for v in list(P - adj[pivot]):
        bron_kerbosch(R | {v}, P & adj[v], X & adj[v], adj, out)
        P = P - {v}
        X = X | {v}


# ------------------------------------------------------------------
# report
# ------------------------------------------------------------------

def name_part(members):
    """the guaranteed-add name(s) every member of the part fits."""
    fits = set.intersection(*[m["fits"] for m in members]) if members else set()
    return fits


def langs(ms):
    return sorted({m["lang"] for m in ms})


def main():
    idx, spell, pts, profiles = load()
    print("ACCUMULATION -- the add intention, whole|whole, L1")
    print("  profiles: %d" % len(profiles))
    by = collections.Counter(p["lang"] for p in profiles)
    for k in sorted(by):
        print("    %-14s %3d" % (k, by[k]))
    missing = [l for l, _, _ in ADD_FILES if l not in by]
    print("  languages with NO add row at L1: %s"
          % (", ".join(sorted(set(["dart"]) | set(missing))) or "none"))

    pred, names = classify(profiles, pts)

    print("\nPER-PROFILE FIT against the guaranteed adds")
    for pr in sorted(profiles, key=lambda p: p["key"]):
        f = sorted(pr["fits"])
        print("  %-52s values=%3d unrep=%3d decl=%3d  fits=%s"
              % (pr["key"], pr["n_value_cells"], pr["n_unrep"],
                 pr["n_declines"], ",".join(f) if f else "NONE"))

    # ---- ALL-CELLS -------------------------------------------------
    ac = allcells_parts(profiles)
    print("\nALL-CELLS reading -- full-vector equality, a true partition")
    print("  parts: %d   (cross-language: %d)"
          % (len(ac), sum(1 for p in ac if len(langs(p)) > 1)))
    for i, part in enumerate(sorted(ac, key=lambda p: (-len(p), p[0]["key"]))):
        print("  part %2d  n=%2d  langs=%s  values=%d  fits=%s"
              % (i, len(part), ",".join(langs(part)),
                 part[0]["n_value_cells"],
                 ",".join(sorted(name_part(part))) or "NONE"))
        for m in sorted(part, key=lambda x: x["key"]):
            print("           %s" % m["key"])

    # ---- VALUE -----------------------------------------------------
    ids = list(range(len(profiles)))
    adj = {i: set() for i in ids}
    overlap = {}
    for i in ids:
        for j in ids:
            if j <= i:
                continue
            ok, sh = value_compatible(profiles[i], profiles[j])
            overlap[(i, j)] = sh
            if ok:
                adj[i].add(j)
                adj[j].add(i)
    ne = sum(len(a) for a in adj.values()) // 2
    print("\nVALUE reading -- compatible where both answer a value")
    print("  profiles %d, compatible pairs %d of %d possible"
          % (len(ids), ne, len(ids) * (len(ids) - 1) // 2))
    comp = components(ids, adj)
    print("  connected components: %d  sizes=%s"
          % (len(comp), sorted((len(c) for c in comp), reverse=True)))
    cliq = []
    bron_kerbosch(set(), set(ids), set(), adj, cliq)
    cliq = [c for c in cliq]
    print("  maximal cliques:      %d  sizes=%s"
          % (len(cliq), sorted((len(c) for c in cliq), reverse=True)))
    for i, c in enumerate(sorted(cliq, key=lambda c: -len(c))):
        ms = [profiles[k] for k in c]
        print("  clique %2d  n=%2d  langs=%s  fits=%s"
              % (i, len(c), ",".join(langs(ms)),
                 ",".join(sorted(name_part(ms))) or "NONE"))
        for m in sorted(ms, key=lambda x: x["key"]):
            print("             %s" % m["key"])

    # membership count per profile under cliques
    inmany = collections.Counter()
    for c in cliq:
        for k in c:
            inmany[k] += 1
    print("\n  profiles appearing in MORE THAN ONE maximal clique:")
    for k, v in sorted(inmany.items(), key=lambda kv: (-kv[1],
                                                       profiles[kv[0]]["key"])):
        if v > 1:
            print("    %-52s in %d cliques  fits=%s"
                  % (profiles[k]["key"], v,
                     ",".join(sorted(profiles[k]["fits"])) or "NONE"))

    # ---- the discriminating key ------------------------------------
    ia = spell.index("2^63-1")
    ib = spell.index("42")
    p = ia * len(pts) + ib
    print("\nTHE DISCRIMINATING KEY  (2^63-1, 42)  position %d of %d"
          % (p, len(pts) ** 2))
    seen = collections.OrderedDict()
    for pr in sorted(profiles, key=lambda x: x["key"]):
        seen.setdefault(pr["vec"][p], []).append(pr["key"])
    for cell, who in seen.items():
        print("  %-52s %d profiles" % (cell, len(who)))
        for w in who:
            print("      %s" % w)

    # ---- residue ---------------------------------------------------
    print("\nRESIDUE -- ALL-CELLS parts of one")
    for part in ac:
        if len(part) == 1:
            pr = part[0]
            print("  %-52s values=%d unrep=%d decl=%d fits=%s"
                  % (pr["key"], pr["n_value_cells"], pr["n_unrep"],
                     pr["n_declines"], ",".join(sorted(pr["fits"])) or "NONE"))
    print("\nRESIDUE -- profiles with ZERO comparable value cells against"
          " every co-profile (VALUE reading isolates)")
    for i in ids:
        if not adj[i]:
            pr = profiles[i]
            print("  %-52s values=%d  fits=%s"
                  % (pr["key"], pr["n_value_cells"],
                     ",".join(sorted(pr["fits"])) or "NONE"))

    json.dump(dict(
        profiles=[dict(key=p["key"], lang=p["lang"], op=p["op"],
                       lhs=p["lhs"], rhs=p["rhs"],
                       n_value_cells=p["n_value_cells"],
                       n_unrepresentable=p["n_unrep"],
                       n_declines=p["n_declines"],
                       fits=sorted(p["fits"])) for p in profiles],
        allcells_parts=[[m["key"] for m in part] for part in ac],
        value_components=[[profiles[k]["key"] for k in c] for c in comp],
        value_cliques=[[profiles[k]["key"] for k in c] for c in cliq]),
        open(os.path.join(HERE, "log067_dominant_plus.json"), "w"), indent=1)
    print("\nwrote log067_dominant_plus.json")


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
