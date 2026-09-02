#!/usr/bin/env python3
"""l3_interval_read.py -- fold the interval lanes into the TENSOR
matrices: `matrices_interval/<lang>.<op>.csv`.

the owner's row shape, his words (2026-08-21): "each set of interval inputs
and outputs to be contained within in their own respective row."  So
the 32 samples of one (operator, lhs holder, rhs holder, interval spec)
are ONE row carrying three vectors, not 32 rows.  the owner calls the result
a tensor: a per-operator matrix, with the sample axis inside each row.

Columns, identical on every row of every file:

  probe_id, lhs_holder, rhs_holder, interval_id, n_samples,
  lhs_canon_vector, rhs_canon_vector, output_canon_vector,
  n_values, n_declines

Vectors are semicolon-separated canonical strings under the SAME v2
canon rules as `matrices/`: numeric `[sign, mant, expo]`, zero
`[1, 0.0, 0]` / `[-1, 0.0, 0]`, infinities `[1, inf]` / `[-1, inf]`,
`nan`, ascii minus, no fractions, no `~`, no annotations.  A slot with
no value carries its outcome token -- REFUSE, RAISE:<kind>, ABORT --
never an empty.  Nothing is padded and nothing is dropped: every vector
in a row has exactly n_samples entries.

The existing edge-value matrices in `matrices/` are NOT touched.

Oversized ruby answers arrive as declared tokens rather than truncated
literals (see l3_interval_ruby.py): BIGNUM / BIGRAT / BIGDEC carry a
sign, an exact bit length and the leading 512 bits.  512 bits is 154
decimal digits against the 31 the canonical mant shows, so the printed
canon is the true one; the reader counts how many cells took that path
so the reliance is visible rather than assumed.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.
"""

import csv
import decimal
import json
import os
import sys
import time
from fractions import Fraction

csv.field_size_limit(sys.maxsize)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

OUT_DIR = os.path.join(HERE, "matrices_interval")
LANE_OUT = os.path.abspath(os.path.join(HERE, "..", "..", "..",
                                        "SandboxDesign", "agent", "out"))
RAW = os.path.join(HERE, "raw")

import l3_per_op_matrices as m                                # noqa: E402
import l3_per_op_matrices_v2 as v2                            # noqa: E402
import l3_interval_values as IV                               # noqa: E402
import l3_interval_gen as G                                   # noqa: E402

COLUMNS = ["probe_id", "lhs_holder", "rhs_holder", "interval_id",
           "n_samples", "lhs_canon_vector", "rhs_canon_vector",
           "output_canon_vector", "n_values", "n_declines"]

SEP = ";"
N = IV.N_SAMPLES

TOPBITS_USED = {"n": 0}


# ------------------------------------------------------------------
# outcome tokens
# ------------------------------------------------------------------

def is_decline(s):
    return s == "REFUSE" or s == "ABORT" or s.startswith("RAISE:")


# ------------------------------------------------------------------
# ruby: the bounded serializer's tokens -> canon
# ------------------------------------------------------------------

def _from_top(sign, bits, hexdigits):
    """sign * (leading bits) * 2**(bits - len(leading bits))."""
    top = int(hexdigits, 16)
    if top == 0:
        return Fraction(0)
    shift = bits - top.bit_length()
    TOPBITS_USED["n"] += 1
    return Fraction(sign * top) * (Fraction(2) ** shift)


# ------------------------------------------------------------------
# log_057 self-check: a ruby `Float:` payload's canon must be the canon
# of the SAME double the payload printed.  This is the exact fault
# diagnosed 2026-08-22 -- reading the printed decimal AS an exact
# decimal names a different real number than the double it came from.
#
# NOTE on what "round-trip" has to mean here.  A weak check -- read the
# canon mantissa back to a double at double precision (52 bits) and
# compare -- DOES NOT catch this fault: the buggy and the fixed
# mantissa for -DBL_MAX both round-trip to `ffefffffffffffff` (proven
# below), because they differ by ~9e-18, far under the ~2e-16 half-ULP
# a double's own round-to-nearest tolerates.  The fault lives entirely
# in digits past the 17th, which the CANON keeps (31 fractional
# digits) and a double-precision round-trip cannot see.  So the check
# has to compare the canon AT ITS OWN PRECISION, independently
# recomputed from the double via `Fraction(float(text))` -- the same
# path the fix takes -- not merely confirm the double survives.
#
#   >>> old = "[-1, 1.9999999999999997688934766870555, 1023]"  # bug
#   >>> new = "[-1, 1.9999999999999997779553950749687, 1023]"  # fix
#   >>> both parse back to the double ffefffffffffffff -- identical
#   >>> only `new` is v2.canon_num(Fraction(float(text)))
#
# The fix lives in `canon_output_printed` (l3_per_op_matrices.py); this
# is the instrument that would have caught it, kept so it keeps
# catching it.
# ------------------------------------------------------------------

FLOAT_ROUNDTRIP_CHECKED = {"n": 0}


def _check_float_roundtrip(text, canon):
    """fail loudly -- SystemExit, not a warning -- if a `Float:` payload's
    canon is not the canon of the double the payload printed, recomputed
    independently via `float()` rather than re-run through the same code
    path that produced `canon`."""
    try:
        d = float(text)
    except ValueError:
        return
    FLOAT_ROUNDTRIP_CHECKED["n"] += 1
    if d != d:                                    # nan
        expected = "nan"
    elif d == float("inf"):
        expected = "[1, inf]"
    elif d == float("-inf"):
        expected = "[-1, inf]"
    elif d == 0.0:
        import struct
        expected = ("[-1, 0.0, 0]" if struct.pack(">d", d)[0] & 0x80
                    else "[1, 0.0, 0]")
    else:
        expected = v2.canon_num(Fraction(d))
    if canon != expected:
        raise SystemExit(
            "FLOAT CANON ROUND-TRIP FAILURE (the log_057 fault, "
            "unfixed): ruby Float:%r canonicalised to %s, but the "
            "double it names (float(text) = %r) canonicalises to %s "
            "independently -- these must be the same object"
            % (text, canon, d, expected))


def ruby_canon(payload):
    """`<Class>:<text>` or a declared oversized token -> canon."""
    tname, _, text = payload.partition(":")
    if tname == "BIGNUM":
        s, bits, hx = text.split(":", 2)
        return v2.canon_num(_from_top(int(s), int(bits), hx))
    if tname == "BIGRAT":
        s, nb, nh, db, dh = text.split(":", 4)
        num = _from_top(int(s), int(nb), nh)
        den = _from_top(1, int(db), dh)
        if den == 0:
            return "opaque:BIGRAT-zero-denominator"
        return v2.canon_num(num / den)
    if tname == "BIGDEC":
        s, expo, head = text.split(":", 2)
        TOPBITS_USED["n"] += 1
        try:
            return v2.canon_num(Fraction(head))
        except (ValueError, ZeroDivisionError):
            return "opaque:BIGDEC"
    c, _ = m.canon_output_printed(tname, text)
    c = v2.fix_special(c)
    if tname == "Float":
        _check_float_roundtrip(text, c)
    return c


# ------------------------------------------------------------------
# rust: the bit-grain encodings (l3_exec RT_RUST) -> canon
# ------------------------------------------------------------------

def rust_canon(payload):
    """`<type_name>|<encoding>` -> canon."""
    tname, _, enc = payload.partition("|")
    v = m.decode_enc(enc)
    c, _ = m.canon_output_value(v, enc)
    return v2.fix_special(c)


# ------------------------------------------------------------------
# lane output -> {probe id: canon-or-token}
# ------------------------------------------------------------------

def find_lane(name):
    for d in (LANE_OUT, RAW):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    raise SystemExit("lane output not found: %s (looked in %s, %s)"
                     % (name, LANE_OUT, RAW))


def read_rust():
    p = find_lane("iv_rust_00.txt")
    out, summary = {}, None
    for line in open(p):
        line = line.rstrip("\n")
        if line.startswith("__SUMMARY__"):
            summary = line
            continue
        pid, _, rest = line.partition("|")
        if not pid:
            continue
        if rest.startswith("-|RAISE:"):
            out[pid] = "RAISE:" + v2.norm_kind(rest[len("-|RAISE:"):])
        elif rest.startswith("-|ABORT"):
            out[pid] = "ABORT"
        elif rest.startswith("-|BUILDFAIL"):
            out[pid] = "REFUSE"      # the compiler would not take it
        elif rest.startswith("-|MISSING"):
            out[pid] = "ABORT"       # the process never answered for it
        else:
            out[pid] = rust_canon(rest)
    return out, summary, p


def read_ruby():
    p = find_lane("iv_ruby_00.txt")
    out, summary = {}, None
    for line in open(p):
        line = line.rstrip("\n")
        if line.startswith("__SUMMARY__"):
            summary = line
            continue
        parts = line.split("|", 2)
        if len(parts) < 3:
            continue
        pid, kind, payload = parts
        if kind == "ANSWER":
            out[pid] = ruby_canon(payload)
        elif kind == "RAISE":
            out[pid] = "RAISE:" + v2.norm_kind(payload)
        elif kind == "REFUSE":
            out[pid] = "REFUSE"
        elif kind == "ABORT":
            out[pid] = "ABORT"
        else:
            out[pid] = "ABORT"       # MISSING: the process never answered
    return out, summary, p


# ------------------------------------------------------------------
# row assembly
# ------------------------------------------------------------------

def cells_for(lang):
    """[(operation, op index, lhs table entry, rhs table entry)]"""
    tab = {t["i"]: t for t in G.numeric_table(lang)}
    op_list = G.ops(lang)
    if lang == "rust":
        cells = [(op, i, j) for (op, i, j) in G.rust_cells()]
    else:
        cells = [(op, i, j) for i in sorted(tab) for j in sorted(tab)
                 for op in op_list]
    return [(op, op_list.index(op), tab[i], tab[j]) for (op, i, j) in cells]


def build(lang, results):
    per = {}
    holders_seen = set()
    for op, k, ha, hb in cells_for(lang):
        lidA, ruleA, sampA = IV.samples_for(lang, ha["form"], ha["holder"])
        lidB, ruleB, sampB = IV.samples_for(lang, hb["form"], hb["holder"])
        lvec, rvec, ovec = [], [], []
        for s in range(N):
            pid = "V%d_%d_%d_%d" % (k, ha["i"], hb["i"], s)
            lvec.append(IV.canon_sample(ruleA, sampA[s], v2.canon_num))
            rvec.append(IV.canon_sample(ruleB, sampB[s], v2.canon_num))
            ovec.append(results.get(pid, "ABORT"))
        nd = sum(1 for c in ovec if is_decline(c))
        per.setdefault(op, []).append({
            "probe_id": "V%d_%d_%d" % (k, ha["i"], hb["i"]),
            "lhs_holder": ha["holder"], "rhs_holder": hb["holder"],
            "interval_id": "IV%d:%s|%s" % (N, lidA, lidB),
            "n_samples": N,
            "lhs_canon_vector": SEP.join(lvec),
            "rhs_canon_vector": SEP.join(rvec),
            "output_canon_vector": SEP.join(ovec),
            "n_values": N - nd, "n_declines": nd})
        holders_seen.add(ha["holder"])
        holders_seen.add(hb["holder"])
    return per, holders_seen


# ------------------------------------------------------------------
# verification -- rectangularity, vector lengths, canon hygiene
# ------------------------------------------------------------------

def verify():
    print("FORMAT VERIFICATION")
    files = sorted(f for f in os.listdir(OUT_DIR) if f.endswith(".csv"))
    ncols_bad = veclen_bad = empty_slot = dirty = rows = 0
    vocab_bad = {}
    ok_tokens = 0
    for fn in files:
        p = os.path.join(OUT_DIR, fn)
        for line in csv.reader(open(p)):
            if len(line) != len(COLUMNS):
                ncols_bad += 1
        for r in csv.DictReader(open(p)):
            rows += 1
            n = int(r["n_samples"])
            vs = [r["lhs_canon_vector"].split(SEP),
                  r["rhs_canon_vector"].split(SEP),
                  r["output_canon_vector"].split(SEP)]
            if any(len(v) != n for v in vs):
                veclen_bad += 1
            for v in vs:
                for cell in v:
                    if cell == "":
                        empty_slot += 1
                        continue
                    if cell.startswith("[") and ("/" in cell
                                                 or "~" in cell):
                        dirty += 1
                    if cell in ("negzero", "inf", "-inf"):
                        dirty += 1
                    if "−" in cell:          # unicode minus
                        dirty += 1
                    if is_decline(cell):
                        ok_tokens += 1
                        if cell.startswith("RAISE:") and not cell[6:]:
                            vocab_bad[cell] = vocab_bad.get(cell, 0) + 1
    print("  files                        %d" % len(files))
    print("  rows                         %d" % rows)
    print("  non-rectangular lines        %d  (column count %d "
          "everywhere else)" % (ncols_bad, len(COLUMNS)))
    print("  rows with a wrong vector len %d  (all three vectors must "
          "be n_samples long)" % veclen_bad)
    print("  empty vector slots           %d  (padding NOTHING: a slot "
          "with no value carries its outcome token)" % empty_slot)
    print("  dirty canon cells            %d  (fractions, `~`, retired "
          "words, non-ascii minus)" % dirty)
    print("  outcome tokens in vectors    %d  (REFUSE / RAISE:<kind> / "
          "ABORT only)" % ok_tokens)
    if vocab_bad:
        print("  OUT-OF-VOCABULARY TOKENS     %s" % vocab_bad)
    return dict(files=len(files), rows=rows, non_rectangular=ncols_bad,
                wrong_vector_len=veclen_bad, empty_slots=empty_slot,
                dirty_cells=dirty, outcome_tokens=ok_tokens)


# ------------------------------------------------------------------

def main():
    print("interval matrices -- fold the lane samples into ONE row per "
          "(operator, lhs holder, rhs holder, interval spec)")
    os.makedirs(OUT_DIR, exist_ok=True)
    t0 = time.time()
    index = {}
    for lang, reader in (("rust", read_rust), ("ruby", read_ruby)):
        results, summary, path = reader()
        print("  %s: %d sample results from %s" % (lang, len(results),
                                                   path))
        if summary:
            print("      lane summary: %s" % summary)
        per, holders_seen = build(lang, results)
        for op, rows in sorted(per.items()):
            fn = "%s.%s.csv" % (lang, m.op_filename(op))
            with open(os.path.join(OUT_DIR, fn), "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=COLUMNS)
                w.writeheader()
                for r in rows:
                    w.writerow(r)
            index["%s.%s" % (lang, op)] = dict(
                file=fn, rows=len(rows), n_samples=N,
                samples=len(rows) * N,
                holders=sorted({r["lhs_holder"] for r in rows}
                               | {r["rhs_holder"] for r in rows}),
                n_values=sum(r["n_values"] for r in rows),
                n_declines=sum(r["n_declines"] for r in rows))
        print("      %d operator matrices, %d rows, %d samples (%.1f s)"
              % (len(per), sum(len(v) for v in per.values()),
                 sum(len(v) for v in per.values()) * N,
                 time.time() - t0))

    stats = verify()
    json.dump(dict(
        status="INTERVAL MATRICES (TENSOR) -- one row per (operator, "
               "lhs holder, rhs holder, interval spec), the sample axis "
               "INSIDE the row",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        pilot="rust (static) + ruby (route C) only; the other ten wait",
        columns=COLUMNS, vector_separator=SEP, n_samples=N,
        ladders={k: dict(n=len(v),
                         first=str(v[0]), last=str(v[-1]))
                 for k, v in IV.LADDER_ID.items()},
        oversized_cells_reconstructed_from_leading_bits=TOPBITS_USED["n"],
        verification=stats,
        vocabulary="super-node / sub-node / co-node / sub-tree; the "
                   "OS-stopped outcome is ABORT",
        matrices=index),
        open(os.path.join(OUT_DIR, "index.json"), "w"), indent=1)

    with open(os.path.join(OUT_DIR, "README.md"), "w") as f:
        f.write("# interval matrices (the tensor)\n\n")
        f.write("One CSV per `language.operator`.  One row per "
                "(operator, lhs holder, rhs holder, interval spec); the "
                "%d samples live INSIDE the row as three "
                "semicolon-separated vectors of equal length.  Columns: "
                "%s.\n\n" % (N, ", ".join("`%s`" % c for c in COLUMNS)))
        f.write("Canon rules are the v2 rules unchanged.  A slot with "
                "no value carries `REFUSE`, `RAISE:<kind>` or `ABORT`; "
                "nothing is padded and no slot is ever empty.\n\n")
        f.write("The edge-value matrices in `../matrices/` are "
                "untouched -- interval sampling is IN ADDITION to the "
                "edge classes, never a replacement.\n\n")
        f.write("## ladders\n\n")
        for k, v in sorted(IV.LADDER_ID.items()):
            f.write("- `%s`: %d samples, %s .. %s\n"
                    % (k, len(v), v[0], v[-1]))
    print("  wrote %s (%d matrices)" % (OUT_DIR, len(index)))
    print("  oversized ruby cells rebuilt from leading bits: %d"
          % TOPBITS_USED["n"])


if __name__ == "__main__":
    main()
