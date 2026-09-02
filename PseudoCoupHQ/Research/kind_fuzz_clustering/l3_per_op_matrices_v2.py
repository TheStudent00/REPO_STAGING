#!/usr/bin/env python3
"""l3_per_op_matrices_v2.py -- the per-operator matrices RE-EMITTED
under the owner's FINAL canonical-form rulings (2026-08-20, settled; they
overrode the earlier forms after repeated miscommunication).  Recorded
verbatim in Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/
SUPPORT_conversion_spec.md, dated section "final canonical-form
rulings".  Assembly only; no probe runs.

The rulings, in force here:

  1  numeric canon is `[sign, mant, expo]`, sign in {-1, 1} (0 unused;
     see the zero rule), mant a DECIMAL floating-point string in [1,2)
     rounded to 31 significant fractional digits (a knob; never
     fewer -- trailing zeros are stripped for readability, one
     fractional digit minimum), expo an integer.  NO fractions or
     rationals in any visible column; NO `~` markers; NO arrows or
     annotations inside cells.  Exact rationals go to the SIDE file
     matrices/exact_sidecar.json, never the CSVs.
  2  zero: +0.0 = [1, 0.0, 0]; -0.0 = [-1, 0.0, 0]; the word negzero
     is retired.  Infinities: [1, inf] / [-1, inf].  `nan` is the only
     special word kept.  Ascii `-` everywhere.
  3  bytes columns are exactly as the language holds them (fixed-width
     holders keep leading zeros; unbounded minimal).  Never annotated,
     never transformed.
  4  columns (one CSV per lang.op, one PROBE per row): probe_id,
     lhs_holder, lhs_value_class, lhs_bytes, lhs_canon, rhs_holder,
     rhs_value_class, rhs_bytes, rhs_canon, output_bytes,
     output_canon.  The old indicator columns are RETIRED: outcome
     tokens travel IN output_canon as `REFUSE`, `RAISE:<kind>`,
     `ABORT` (universal vocabulary, never language message text).
     output_bytes is empty when there is no value.
  5  lhs/rhs_canon include the rep read-rule (ctypes.c_int64 holding
     bytes 8000000000000000 canonicalizes [-1, 1.0, 63]).
  6  text canon: t|<NFC utf-8 hex>|byte_len|codepoint_len|grapheme_len.
     container canon: c|<sorted member canons>|key_format|order_flag.
  7  REFUSE rows from the acceptance files stay as rows (inputs
     filled, output_canon = REFUSE).

RAISE kinds: the recorded raise KIND with the language's package
prefix stripped (java.lang.X -> X, System.X -> X, _TypeError ->
TypeError, Encoding::CompatibilityError -> CompatibilityError); go's
message-text raise `runtime error: integer divide by zero` becomes the
kind token IntegerDivideByZero.  A kind token, never a message.

Implementation: imports l3_per_op_matrices (the v1 generator) for its
data loading, rep read-rules and row assembly, and PATCHES its
canonical spellings to the final rulings before running.  The v1
module stays on disk unchanged for the audit trail.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.
"""

import csv
import decimal
import json
import os
import re
import sys
import time
import unicodedata
from fractions import Fraction

csv.field_size_limit(sys.maxsize)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l3_per_op_matrices as m                                     # noqa

OUT_DIR = os.path.join(HERE, "matrices")

COLUMNS = ["probe_id",
           "lhs_holder", "lhs_value_class", "lhs_bytes", "lhs_canon",
           "rhs_holder", "rhs_value_class", "rhs_bytes", "rhs_canon",
           "output_bytes", "output_canon"]

decimal.getcontext().prec = 60

MANT_DIGITS = 31          # the knob: significant fractional digits

EXACT = {}                # canon string -> exact rational mant (side file)


# ------------------------------------------------------------------
# ruling 1 + 2: numeric canon
# ------------------------------------------------------------------

def canon_num(fr):
    """exact Fraction -> the final canon string; exact mant recorded
    to the sidecar, never the CSV."""
    if fr == 0:
        return "[1, 0.0, 0]"
    sign = 1 if fr > 0 else -1
    a = abs(fr)
    e = a.numerator.bit_length() - a.denominator.bit_length()
    if Fraction(2) ** e > a:
        e -= 1
    mant = a / (Fraction(2) ** e)
    d = (decimal.Decimal(mant.numerator)
         / decimal.Decimal(mant.denominator))
    q = d.quantize(decimal.Decimal(1).scaleb(-MANT_DIGITS))
    s = format(q, "f").rstrip("0")
    if s.endswith("."):
        s += "0"
    canon = "[%d, %s, %d]" % (sign, s, e)
    EXACT.setdefault(canon, str(mant.numerator) if mant.denominator == 1
                     else "%d/%d" % (mant.numerator, mant.denominator))
    return canon


def canon_from_fraction_v2(fr):
    """v1 call signature (canon, exact) -- exact column is retired, so
    the second slot is always empty; the sidecar carries it."""
    return canon_num(fr), ""


# the v1 special words, mapped to the final spellings at field grain
SPECIAL_MAP = {"inf": "[1, inf]", "-inf": "[-1, inf]",
               "negzero": "[-1, 0.0, 0]"}


def fix_special(s):
    return SPECIAL_MAP.get(s, s)


# ------------------------------------------------------------------
# ruling 6: text and container canon
# ------------------------------------------------------------------

def canon_text_v2(s):
    s = m._desurrogate(s)
    nfc = unicodedata.normalize("NFC", s)
    b = s.encode("utf-8")
    return "t|%s|%d|%d|%d" % (nfc.encode("utf-8").hex(), len(b),
                              len(s), m.grapheme_count(s))


def val_canon(v):
    """member canon inside a container -- the same final spellings."""
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "null"
    if isinstance(v, int):
        return canon_num(Fraction(v))
    if isinstance(v, float):
        if v != v:
            return "nan"
        if v == float("inf"):
            return "[1, inf]"
        if v == float("-inf"):
            return "[-1, inf]"
        import struct
        if v == 0.0 and struct.pack(">d", v)[0] & 0x80:
            return "[-1, 0.0, 0]"
        return canon_num(Fraction(v))
    if isinstance(v, str):
        return canon_text_v2(v)
    if isinstance(v, (list, tuple, dict, set, frozenset)):
        return canon_container_obj_v2(v)
    return "opaque:%r" % (v,)


def canon_container_obj_v2(obj):
    if isinstance(obj, dict):
        d, order_flag = obj, "not-applicable"
    elif isinstance(obj, (list, tuple)):
        d = {i: v for i, v in enumerate(obj)}
        sv0 = [m._canon_value(v) for v in obj]
        order_flag = "as-sorted" if sorted(sv0) == sv0 else "reordered"
    elif isinstance(obj, (set, frozenset)):
        d = {i: v for i, v in
             enumerate(sorted(obj, key=m._canon_value))}
        order_flag = "unordered"
    else:
        return "unparsed:%r" % (obj,)
    kinds = set()
    for k in d:
        kinds.add("integer" if isinstance(k, (int, bool)) else
                  "text" if isinstance(k, str) else "other")
    key_format = kinds.pop() if len(kinds) == 1 else \
        ("mixed" if kinds else "empty")
    mem = sorted(val_canon(v) for v in d.values())
    return "c|%s|%s|%s" % (",".join(mem), key_format, order_flag)


# print-grain containers travel as l3_matrix_extended token strings
# (num:…, text:<hex>, seq:[…], map:{k=>v}); translate token -> canon.

def tok2canon(tok):
    kind, _, payload = tok.partition(":")
    if kind == "truth":
        return payload
    if kind == "nothing":
        return "null"
    if kind == "num":
        try:
            return canon_num(Fraction(payload))
        except (ValueError, ZeroDivisionError):
            return tok
    if kind == "text":
        try:
            return canon_text_v2(bytes.fromhex(payload).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return tok
    if kind == "seq" and payload.startswith("[") and payload.endswith("]"):
        toks = m._split_top(payload[1:-1]) if payload != "[]" else []
        mem = [tok2canon(t) for t in toks]
        order_flag = ("as-sorted" if sorted(toks) == toks else "reordered")
        return "c|%s|%s|%s" % (",".join(sorted(mem)),
                               "integer" if mem else "empty", order_flag)
    if kind == "map" and payload.startswith("{") and payload.endswith("}"):
        entries = m._split_top(payload[1:-1]) if payload != "{}" else []
        vals, kkinds = [], set()
        for e in entries:
            k, _, v = e.partition("=>")
            kk, _, _ = k.partition(":")
            kkinds.add("integer" if kk in ("num", "truth") else
                       "text" if kk == "text" else "other")
            vals.append(tok2canon(v))
        key_format = kkinds.pop() if len(kkinds) == 1 else \
            ("mixed" if kkinds else "empty")
        return "c|%s|%s|%s" % (",".join(sorted(vals)), key_format,
                               "not-applicable")
    return tok


def coords_str_v2(cc):
    if cc.get("unparsed") is not None:
        return "unparsed:%s" % cc["unparsed"]
    sv = cc["sorted_values"]
    if not isinstance(sv, list):
        return "unparsed:"
    mem = sorted(tok2canon(t) for t in sv)
    return "c|%s|%s|%s" % (",".join(mem), cc["key_format"],
                           cc["order_flag"])


# ------------------------------------------------------------------
# ruling 4: outcome tokens in output_canon; kind tokens, not messages
# ------------------------------------------------------------------

def norm_kind(k):
    k = k.strip()
    if k == "runtime error: integer divide by zero":
        return "IntegerDivideByZero"
    if k.startswith("java.lang."):
        return k[len("java.lang."):]
    if k.startswith("System."):
        return k[len("System."):]
    if "::" in k:
        k = k.split("::")[-1]
    if k.startswith("_"):
        k = k[1:]
    return k


# ------------------------------------------------------------------
# patch the v1 module, then assemble
# ------------------------------------------------------------------

m.canon_from_fraction = canon_from_fraction_v2
m.canon_text = canon_text_v2
m.canon_container_obj = canon_container_obj_v2
m.coords_str = coords_str_v2

# print-grain constructor spellings (Decimal('X'), Fraction(a, b))
# must canonicalize, not fall to opaque: strip the constructor before
# the numeric parse.
_orig_canon_output_printed = m.canon_output_printed

_RX_DECIMAL = re.compile(r"Decimal\('(-?[0-9][0-9.eE+-]*|-?Infinity|"
                         r"Infinity|NaN|-?0(\.0+)?)'\)")
_RX_FRACTION = re.compile(r"(?:Fraction|Rational)\((-?\d+),\s*(\d+)\)")


def canon_output_printed_v2(tname, text):
    t = text.strip()
    mm = _RX_DECIMAL.fullmatch(t)
    if mm:
        t = mm.group(1)
        if t in ("Infinity", "+Infinity"):
            t = "inf"
        elif t == "-Infinity":
            t = "-inf"
        elif t == "NaN":
            t = "nan"
        return _orig_canon_output_printed("decimal", t)
    mm = _RX_FRACTION.fullmatch(t)
    if mm:
        num, den = int(mm.group(1)), int(mm.group(2))
        if den != 0:
            return canon_num(Fraction(num, den)), ""
    return _orig_canon_output_printed(tname, text)


m.canon_output_printed = canon_output_printed_v2


def convert_row(r):
    lc = fix_special(r["lhs_canonical"])
    rc = fix_special(r["rhs_canonical"])
    if r["REFUSE"]:
        oc, ob = "REFUSE", ""
    elif r["RAISE"]:
        oc, ob = "RAISE:" + norm_kind(r["raise_kind"]), ""
    elif r["ABORT"]:
        oc, ob = "ABORT", ""
    else:
        oc = fix_special(r["output_canonical"])
        ob = r["output_literal"]
    return {"probe_id": r["probe_id"],
            "lhs_holder": r["lhs_holder"],
            "lhs_value_class": r["lhs_value_class"],
            "lhs_bytes": r["lhs_bytes"], "lhs_canon": lc,
            "rhs_holder": r["rhs_holder"],
            "rhs_value_class": r["rhs_value_class"],
            "rhs_bytes": r["rhs_bytes"], "rhs_canon": rc,
            "output_bytes": ob, "output_canon": oc}


def main():
    print("per-operator matrices v2 -- the owner's final canonical-form "
          "rulings; assembly only, no probe runs")
    os.makedirs(OUT_DIR, exist_ok=True)
    t0 = time.time()
    index = {}
    name_map = {}
    for lang in m.THREE + m.NINE:
        per = (m.rows_three if lang in m.THREE else m.rows_nine)(lang)
        for op, rows in sorted(per.items()):
            fn = "%s.%s.csv" % (lang, m.op_filename(op))
            name_map[fn] = "%s.%s" % (lang, op)
            out_rows = [convert_row(r) for r in rows]
            with open(os.path.join(OUT_DIR, fn), "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=COLUMNS)
                w.writeheader()
                for r in out_rows:
                    w.writerow({k: (v.replace("\0", "\\x00")
                                    if isinstance(v, str) and "\0" in v
                                    else v) for k, v in r.items()})
            oc = [r["output_canon"] for r in out_rows]
            index["%s.%s" % (lang, op)] = dict(
                file=fn, rows=len(out_rows),
                holders=len({r["lhs_holder"] for r in out_rows}
                            | {r["rhs_holder"] for r in out_rows}),
                value_rows=sum(1 for c in oc if c != "REFUSE"
                               and c != "ABORT"
                               and not c.startswith("RAISE:")),
                REFUSE=sum(1 for c in oc if c == "REFUSE"),
                RAISE=sum(1 for c in oc if c.startswith("RAISE:")),
                ABORT=sum(1 for c in oc if c == "ABORT"))
        print("  %s: %d matrices (%.1f s)"
              % (lang, len(per), time.time() - t0))

    json.dump(dict(
        status="PER-OPERATOR MATRICES v2, FINAL CANONICAL FORMS, "
               "ASSEMBLY ONLY",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        columns=COLUMNS, n_matrices=len(index),
        mant_digits=MANT_DIGITS,
        exact_sidecar="exact_sidecar.json",
        escaping="see README.md in this directory",
        matrices=index),
        open(os.path.join(OUT_DIR, "index.json"), "w"), indent=1)

    json.dump(dict(
        status="EXACT SIDECAR -- exact rational mants, keyed by the "
               "canon string they were rounded into; never a CSV "
               "column (the owner's ruling 1, 2026-08-20)",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        mant_digits=MANT_DIGITS,
        exact_mants=EXACT),
        open(os.path.join(OUT_DIR, "exact_sidecar.json"), "w"),
        indent=0)

    with open(os.path.join(OUT_DIR, "README.md"), "w") as f:
        f.write("# per-operator matrices (v2 -- final canonical "
                "forms)\n\n")
        f.write("One CSV per `language.operator`; one PROBE per row; "
                "columns identical on every row of every matrix: "
                "%s (see l3_per_op_matrices_v2.py).  Outcome tokens "
                "travel in `output_canon` as `REFUSE`, `RAISE:<kind>`, "
                "`ABORT`; exact rational mants live in "
                "`exact_sidecar.json`, never a CSV column.\n\n"
                % ", ".join("`%s`" % c for c in COLUMNS))
        f.write("## filename escaping\n\n")
        f.write("A word-spelled operator that is entirely letters "
                "keeps its spelling with spaces as underscores. Any "
                "other operator is spelled character by character: "
                "%s.\n\n" % ", ".join(
                    "`%s` -> `%s`" % (k, v)
                    for k, v in sorted(m.CHAR_NAMES.items())))
        f.write("## reverse mapping (filename -> language.operator)\n\n")
        for fn, k in sorted(name_map.items()):
            f.write("- `%s` -> `%s`\n" % (fn, k))
    print("  %d matrices -> %s" % (len(index), OUT_DIR))
    print("  exact sidecar: %d distinct canon strings" % len(EXACT))

    if m.UNRESOLVED:
        print("  UNRESOLVED holder/value-class combinations: %d"
              % len(m.UNRESOLVED))

    # ------------------------------------------- verification slice
    print("VERIFICATION SLICE -- python.+, base_42 + i64max_plus1 "
          "(ordered), 16 rows")
    rows = list(csv.DictReader(open(os.path.join(OUT_DIR,
                                                 "python.plus.csv"))))
    sl = [r for r in rows
          if (r["lhs_value_class"], r["rhs_value_class"])
          == ("base_42", "i64max_plus1")]
    for r in sl:
        print("  %-18s + %-18s | rhs_canon %-24s | output_canon %s"
              % (r["lhs_holder"], r["rhs_holder"], r["rhs_canon"],
                 r["output_canon"]))
    expected = {
        ("int", "int"):
            ("[1, 1.0000000000000000045536491244391, 63]", None),
        ("int", "ctypes.c_int64"):
            ("[-1, 1.9999999999999999908927017511218, 62]",
             "[-1, 1.0, 63]"),
        ("ctypes.c_int64", "ctypes.c_int64"):
            ("[-1, 1.0, 1]", None),
        ("decimal.Decimal", "fractions.Fraction"):
            ("RAISE:TypeError", None),
        ("fractions.Fraction", "decimal.Decimal"):
            ("RAISE:TypeError", None),
    }
    print("  DIFF against the owner's approved example:")
    ok = True
    for r in sl:
        key = (r["lhs_holder"], r["rhs_holder"])
        if key not in expected:
            continue
        eo, er = expected[key]
        good = r["output_canon"] == eo and (er is None
                                            or r["rhs_canon"] == er)
        if not good:
            ok = False
        print("    %s %s+%s: output_canon %s (expected %s)%s"
              % ("MATCH   " if good else "MISMATCH", key[0], key[1],
                 r["output_canon"], eo,
                 "" if er is None else " ; rhs_canon %s (expected %s)"
                 % (r["rhs_canon"], er)))
    print("  slice verdict: %s" % ("ALL MATCH" if ok
                                   else "MISMATCH PRESENT -- reported, "
                                        "not papered over"))

    # ------------------------------------------- rectangularity
    bad = 0
    for fn in sorted(os.listdir(OUT_DIR)):
        if not fn.endswith(".csv"):
            continue
        ncols = {len(line) for line
                 in csv.reader(open(os.path.join(OUT_DIR, fn)))}
        if ncols != {len(COLUMNS)}:
            bad += 1
            print("  NOT RECTANGULAR: %s -> %s" % (fn, ncols))
    print("  rectangularity: %d matrices, %d non-rectangular, column "
          "count %d everywhere else" % (len(index), bad, len(COLUMNS)))
    # no fraction, no tilde, no retired word in any visible canon cell
    dirty = 0
    for fn in sorted(os.listdir(OUT_DIR)):
        if not fn.endswith(".csv"):
            continue
        for r in csv.DictReader(open(os.path.join(OUT_DIR, fn))):
            for col in ("lhs_canon", "rhs_canon", "output_canon"):
                v = r[col]
                if v.startswith("[") and ("/" in v or "~" in v):
                    dirty += 1
                if v == "negzero" or v == "inf" or v == "-inf":
                    dirty += 1
    print("  canon hygiene: %d dirty cells (fractions/~/retired "
          "words in visible canon columns)" % dirty)


if __name__ == "__main__":
    main()
