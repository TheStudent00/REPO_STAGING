#!/usr/bin/env python3
"""l3_matrix_extended.py -- the EXTENDED CLUSTERING MATRIX, assembly only.

the owner ruled the design 2026-08-20 (settled, not proposed); the spec is
Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/
SUPPORT_conversion_spec.md.  The governing rule, quoted from there:

    never compare raw answers, compare their decompositions, and let
    WHICH coordinate disagrees be the feature.

No probe runs here.  Everything is assembly over the layer-3 answer
data already on disk, loaded through `l3_answers12.py`'s own loaders
(load_three / load_nine) so the canonical token space is the one the
clusters stand on -- the `inx` grain, key `form|vc|form|vc` -> set of
canonical tokens.

Emits:
  matrix_extended_base.csv   the base form-level matrix.  Rows = the 64
                             `form|form` pairs, columns = every lang.op
                             signature, cell = sorted set of answer
                             FORMS joined by "+", with RAISE and ABORT
                             as first-class elements; REFUSE for a probed-
                             and-declined cell, UNPROBED for a never-probed
                             cell with nothing at all.  Rectangular,
                             never sparse, spelling-blind.
  matrix_extended.json       the extension coordinates.  Interned:
                             `token_decompositions` maps each canonical
                             token to its coordinate set ONCE;
                             `cells` maps column -> input cell ->
                             token list at the value-pair grain;
                             `congruences` lists every detected
                             wrap relation ("=== mod 2^w").

Extension coordinates that do not apply to a token read
`not-applicable`, which is DISTINCT from refuse (spec, applicability
rule).

Numeric cast is unbounded EXACT -- python int / fractions.Fraction --
never floating.  A print-grain decimal token is cast exactly AS
PRINTED; what the printer already destroyed stays destroyed and is not
re-invented here.

Graphemes: no grapheme library is assumed present.  The fallback is a
simple extended-grapheme-cluster approximation: a new cluster starts at
every codepoint that is not a combining mark (category M*), not a ZWJ
(U+200D), not preceded by a ZWJ, and not the second of a regional-
indicator pair.  Documented here and in the spec; it is exact for the
probe alphabet in use (e-acute both composed and decomposed) and
approximate in general.

Wrap relations: when two exact integer values in the same input cell
(same column or different columns) differ by exactly 2^w with w >= 8,
the congruence is recorded as a FEATURE instead of a mismatch.  The
floor w >= 8 is mechanical noise control (a difference of 2 or 4 is
arithmetic, not wrapping) and is overturnable.
"""

import ast
import csv
import re
import itertools
import json
import os
import sys
import time
import unicodedata
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from l3_cluster import FORMS                                  # noqa
from l3_answers import NINE, THREE                            # noqa
from l3_answers12 import load_three, load_nine                # noqa

ROWS = ["%s|%s" % (a, b) for a in FORMS for b in FORMS]

NA = "not-applicable"


# --------------------------------------------------------------------
# numeric decomposition -- [sign | mantissa | exponent | special]
# --------------------------------------------------------------------

SPECIALS = {"inf": "inf", "+inf": "inf", "-inf": "-inf",
            "infinity": "inf", "-infinity": "-inf",
            "nan": "nan", "-nan": "nan"}


def exact_number(text):
    """Unbounded exact cast of a decimal token payload.  int for
    integers, Fraction for anything with a point or exponent.  Never a
    float."""
    t = text.strip()
    try:
        return int(t)
    except ValueError:
        pass
    return Fraction(t)          # Fraction parses '2.25', '9.2e+18' exactly


def numeric_coords(payload):
    low = payload.lower()
    if low in SPECIALS:
        return dict(sign=NA, mantissa=NA, exponent=NA,
                    special=SPECIALS[low])
    if payload == "-0.0" or payload == "-0":
        return dict(sign=NA, mantissa=NA, exponent=NA, special="negzero")
    try:
        v = exact_number(payload)
    except (ValueError, ZeroDivisionError):
        return dict(sign=NA, mantissa=NA, exponent=NA,
                    special="unparsed:%s" % payload[:40])
    if v == 0:
        return dict(sign=0, mantissa="0", exponent=NA, special=NA)
    sign = 1 if v > 0 else -1
    a = abs(Fraction(v))
    # |v| = m * 2^e with 1 <= m < 2, m exact
    e = a.numerator.bit_length() - a.denominator.bit_length()
    if Fraction(2) ** e > a:
        e -= 1
    m = a / Fraction(2) ** e
    return dict(sign=sign,
                mantissa=str(m.numerator) if m.denominator == 1
                else "%d/%d" % (m.numerator, m.denominator),
                exponent=e,
                special=NA,
                exact=str(a.numerator) if a.denominator == 1
                else "%d/%d" % (a.numerator, a.denominator))


# --------------------------------------------------------------------
# text decomposition -- [utf-8 bytes | codepoints | graphemes | NFC]
# --------------------------------------------------------------------

def grapheme_count(s):
    """Fallback extended-grapheme-cluster count; see module docstring."""
    n = 0
    prev = None
    ri_run = 0
    for ch in s:
        cat = unicodedata.category(ch)
        is_ri = 0x1F1E6 <= ord(ch) <= 0x1F1FF
        if is_ri:
            ri_run += 1
        else:
            ri_run = 0
        joined = (cat.startswith("M") or ch == "‍" or
                  prev == "‍" or (is_ri and ri_run % 2 == 0))
        if prev is None or not joined:
            n += 1
        prev = ch
    return n


def text_coords(hexpayload):
    try:
        raw = bytes.fromhex(hexpayload)
        s = raw.decode("utf-8")
    except ValueError:
        return dict(utf8_bytes=hexpayload, codepoints=NA,
                    graphemes=NA, nfc=NA)
    return dict(utf8_bytes=hexpayload,
                codepoints=len(s),
                graphemes=grapheme_count(s),
                nfc=unicodedata.normalize("NFC", s).encode("utf-8").hex())


# --------------------------------------------------------------------
# container canonicalization -- [sorted values | key format | order flag]
# --------------------------------------------------------------------

def _canon_value(v):
    """Recursive canonical repr with the exact numeric cast applied to
    numeric leaves (spec: numeric cast applies recursively to keys and
    values)."""
    if isinstance(v, bool):
        return "truth:%s" % str(v).lower()
    if isinstance(v, (int, float)):
        try:
            f = Fraction(str(v))
        except (ValueError, ZeroDivisionError):
            return "num:%r" % v
        return "num:%s" % (str(f.numerator) if f.denominator == 1
                           else "%d/%d" % (f.numerator, f.denominator))
    if v is None:
        return "nothing:null"
    if isinstance(v, str):
        return "text:%s" % v.encode("utf-8").hex()
    if isinstance(v, (list, tuple, set, frozenset)):
        return "seq:[%s]" % ",".join(_canon_value(x) for x in v)
    if isinstance(v, dict):
        return "map:{%s}" % ",".join(
            "%s=>%s" % (_canon_value(k), _canon_value(x))
            for k, x in sorted(v.items(), key=lambda kv: _canon_value(kv[0])))
    return "opaque:%r" % (v,)


def container_coords(payload):
    # normalise the print-grain spellings the python literal parser
    # cannot read: ruby's Set inspect form becomes a set literal, and
    # the word spellings of truth and nothing become python's.  ruby
    # Struct/data inspect forms are LEFT unparsed on purpose -- their
    # coordinates read the unparsed marker and the resistance is
    # reported rather than papered over.
    p = payload
    m = re.fullmatch(r"\{#<Set:\{(.*)\}>\}", p)
    if m:
        p = "{%s}" % m.group(1) if m.group(1) else "set()"
    p = re.sub(r"\btrue\b", "True", p)
    p = re.sub(r"\bfalse\b", "False", p)
    p = re.sub(r"\b(?:nil|null)\b", "None", p)
    try:
        obj = ast.literal_eval(p)
    except (ValueError, SyntaxError, TypeError, MemoryError,
            RecursionError):
        return dict(sorted_values=NA, key_format=NA, order_flag=NA,
                    unparsed=payload[:60])
    if isinstance(obj, dict):
        d = obj
        src_order = list(obj.values())
        order_flag = NA          # a keyed container carries no order claim
    elif isinstance(obj, (list, tuple)):
        d = {i: v for i, v in enumerate(obj)}
        src_order = list(obj)
        order_flag = None        # filled below
    elif isinstance(obj, (set, frozenset)):
        d = {i: v for i, v in enumerate(sorted(obj, key=_canon_value))}
        src_order = None
        order_flag = "unordered"
    else:
        return dict(sorted_values=NA, key_format=NA, order_flag=NA,
                    unparsed=payload[:60])
    kinds = set()
    for k in d:
        kinds.add("integer" if isinstance(k, (int, bool)) else
                  "text" if isinstance(k, str) else "other")
    key_format = kinds.pop() if len(kinds) == 1 else \
        ("mixed" if kinds else "empty")
    sv = sorted(_canon_value(v) for v in d.values())
    if order_flag is None:
        order_flag = ("as-sorted"
                      if [_canon_value(v) for v in src_order] == sv
                      else "reordered")
    return dict(sorted_values=sv, key_format=key_format,
                order_flag=order_flag)


# --------------------------------------------------------------------
# one token -> one coordinate set
# --------------------------------------------------------------------

def decompose(tok):
    kind, _, payload = tok.partition(":")
    out = dict(kind=kind)
    if kind in ("whole", "fractional"):
        out["numeric"] = numeric_coords(payload)
        out["container"] = NA
        out["text"] = NA
    elif kind == "text":
        out["numeric"] = NA
        out["container"] = NA
        out["text"] = text_coords(payload)
    elif kind in ("sequence", "keyed"):
        out["numeric"] = NA
        out["container"] = container_coords(payload)
        out["text"] = NA
    elif kind == "raise":
        out.update(numeric=NA, container=NA, text=NA, outcome="raise")
    elif kind == "death":
        out.update(numeric=NA, container=NA, text=NA, outcome="abort")
    else:                       # truth, nothing, ord, range, opaque, ...
        out.update(numeric=NA, container=NA, text=NA)
    return out




ACCEPT_FILES = dict(cpp="acceptance_cpp_A2.json", dart="acceptance_dart_A2.json",
                    go="acceptance_go_A2.json", rust="acceptance_rust_A2.json",
                    swift="acceptance_swift_A2.json", csharp="acceptance_csharp_A1.json",
                    java="acceptance_java_A1.json", kotlin="acceptance_kotlin_A1.json",
                    typescript="acceptance_typescript_A1.json")


def load_probed_pairs():
    """(lang.op, form-pair) combinations the acceptance stage PROBED,
    whatever the verdict. An empty matrix cell whose pair is in here
    was probed and declined (REFUSE); otherwise never probed
    (UNPROBED). The answers files cannot supply this: they hold only
    the accepted subset."""
    probed = {}
    for lang, fn in ACCEPT_FILES.items():
        path = os.path.join(HERE, fn)
        if not os.path.exists(path):
            continue
        d = json.load(open(path))
        for cell in d["cells"].values():
            k = "%s.%s" % (lang, cell["operation"])
            probed.setdefault(k, set()).add(
                (cell["lhs"]["form"], cell["rhs"]["form"]))
    return probed


# --------------------------------------------------------------------
# assembly
# --------------------------------------------------------------------

def cell_elements(rec, fa, fb):
    els = set()
    for key, toks in rec["inx"].items():
        ka, _, kb, _ = key.split("|")
        if (ka, kb) != (fa, fb):
            continue
        for t in toks:
            p = t.split(":", 1)[0]
            els.add("RAISE" if p == "raise" else
                    "ABORT" if p == "death" else p)
    return els


def main():
    print("extended matrix -- assembly over the layer-3 answers, no runs")
    Ls = {}
    for lang in THREE:
        Ls[lang] = load_three(lang)
    for lang in NINE:
        Ls[lang] = load_nine(lang)

    cols = []
    recs = {}
    for lang, L in Ls.items():
        for op, rec in L["per"].items():
            k = "%s.%s" % (lang, op)
            cols.append(k)
            recs[k] = rec
    cols.sort()

    probed_pairs = load_probed_pairs()

    # ------------------------------------------------- base CSV
    csv_path = os.path.join(HERE, "matrix_extended_base.csv")
    n_refuse = n_filled = 0
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["form_pair"] + cols)
        for row in ROWS:
            fa, fb = row.split("|")
            line = [row]
            for c in cols:
                els = cell_elements(recs[c], fa, fb)
                if not els:
                    probed = ((fa, fb) in recs[c]["pairs"]
                              or (fa, fb) in probed_pairs.get(c, ()))
                    line.append("REFUSE" if probed else "UNPROBED")
                    n_refuse += 1
                else:
                    line.append("+".join(sorted(els)))
                    n_filled += 1
            w.writerow(line)
    print("  base matrix: %d rows x %d columns -> %s"
          % (len(ROWS), len(cols), csv_path))
    print("  cells: %d filled, %d REFUSE/UNPROBED, %d total"
          % (n_filled, n_refuse, n_filled + n_refuse))

    # ------------------------------------------------- decompositions
    tokens = set()
    cells = {}
    for c in cols:
        cc = {}
        for key, toks in recs[c]["inx"].items():
            cc[key] = sorted(toks)
            tokens.update(toks)
        cells[c] = cc
    t0 = time.time()
    dec = {}
    for i, t in enumerate(sorted(tokens)):
        dec[t] = decompose(t)
    print("  %d distinct canonical tokens decomposed in %.1f s"
          % (len(dec), time.time() - t0))

    # ------------------------------------------------- congruences
    # group exact integer values by input cell across all columns
    by_key = {}
    for c in cols:
        for key, toks in cells[c].items():
            for t in toks:
                d = dec[t]
                if d["numeric"] is NA or not isinstance(d["numeric"], dict):
                    continue
                nm = d["numeric"]
                if nm.get("special") != NA or nm.get("sign") is NA:
                    continue
                ex = nm.get("exact")
                if nm.get("sign") == 0:
                    v = 0
                elif ex is not None and "/" not in ex:
                    v = int(ex) * nm["sign"]
                else:
                    continue                       # not an integer
                by_key.setdefault(key, []).append((c, t, v))
    congr = []
    seen = set()
    # the owner's coordinates (2026-08-20): a wrap is NOT a raw distance.
    # In [sign, mant, expo] space it is a SIGN FLIP plus mantissas
    # that are complements of the modulus: |a| + |b| == 2^w.  The
    # raw-difference spelling compared un-decomposed values, which
    # the governing rule forbids; this one never leaves the
    # decomposition.  The sharper signature also retires most of the
    # old w >= 8 floor's job; kept as a guard.
    for key, entries in by_key.items():
        for (ca, ta, va), (cb, tb, vb) in itertools.combinations(entries, 2):
            if va == vb:
                continue
            sa, sb = (va > 0) - (va < 0), (vb > 0) - (vb < 0)
            rel = None
            if sa != 0 and sa == -sb:
                # signed wrap: sign flip, mants are complements
                m = abs(va) + abs(vb)
                w = m.bit_length() - 1
                if m == (1 << w) and w >= 8:
                    rel = ("sign flip, mant sum = 2^%d"
                           " (=== mod 2^%d)" % (w, w))
            elif sa == sb:
                # unsigned wrap: same sign, mants offset by the
                # modulus (uint64 41 vs python 2^64+41)
                m = abs(abs(va) - abs(vb))
                w = m.bit_length() - 1
                if m == (1 << w) and w >= 8:
                    rel = ("same sign, mant difference = 2^%d"
                           " (=== mod 2^%d)" % (w, w))
            if rel:
                sig = (key, min(ca, cb), max(ca, cb), min(va, vb),
                       max(va, vb))
                if sig in seen:
                    continue
                seen.add(sig)
                congr.append(dict(input_cell=key, a=ca, b=cb,
                                  token_a=ta, token_b=tb,
                                  relation=rel, w=w))
    congr.sort(key=lambda r: (-r["w"], r["input_cell"]))
    print("  %d congruences (wrap relations) recorded" % len(congr))

    # ------------------------------------------------- sanity checks
    print("SANITY CHECKS")
    print("  [1] matrix dimensions: %d rows x %d columns"
          % (len(ROWS), len(cols)))
    go_cells = {r: cell_elements(recs["go.+"], *r.split("|"))
                for r in ROWS}
    nz = sorted(r for r, e in go_cells.items() if e)
    print("  [2] go.+ non-REFUSE cells: %d -> %s" % (len(nz), nz))
    hits = [r for r in congr
            if r["input_cell"] == "whole|i64max|whole|base_42"
            and r["w"] == 64 and "go.+" in (r["a"], r["b"])]
    print("  [3] 2^64 congruence on (i64max, base_42) touching go.+: "
          "%d pairs" % len(hits))
    for h in hits[:6]:
        print("      %s ~ %s : %s vs %s  %s"
              % (h["a"], h["b"], h["token_a"], h["token_b"], h["relation"]))

    out = dict(
        status="EXTENDED MATRIX, ASSEMBLY ONLY",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        spec="Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/"
             "SUPPORT_conversion_spec.md",
        governing_rule="never compare raw answers, compare their "
                       "decompositions, and let WHICH coordinate "
                       "disagrees be the feature",
        forms=FORMS, rows=ROWS, columns=cols,
        n_rows=len(ROWS), n_columns=len(cols),
        base_csv="matrix_extended_base.csv",
        applicability_rule="a coordinate that does not apply reads "
                           "'not-applicable', which is DISTINCT from "
                           "refuse",
        grapheme_note="fallback extended-grapheme-cluster count, see "
                      "l3_matrix_extended.py docstring",
        congruence_floor="w >= 8, mechanical, overturnable",
        token_decompositions=dec,
        cells=cells,
        congruences=congr,
        n_congruences=len(congr),
    )
    jp = os.path.join(HERE, "matrix_extended.json")
    json.dump(out, open(jp, "w"), indent=1, default=str)
    print("  wrote %s (%.1f MB)" % (jp, os.path.getsize(jp) / 1e6))


if __name__ == "__main__":
    main()
