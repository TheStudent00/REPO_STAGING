#!/usr/bin/env python3
"""log064_independent_verify.py -- INDEPENDENT re-derivation of a sample
of matrices_cart_v2 cells straight from the raw lane text, per the
log_055 verifier pattern. Written fresh: does NOT import l3_cart_read,
l3_interval_read, l3_per_op_matrices, or l3_per_op_matrices_v2. Only the
documented canon rule (CLAUDE.md / log_055/056/057) is used:

  [sign, mant, expo], sign in {-1,1}, mant a DECIMAL string in [1,2)
  with up to 31 fractional digits (trailing zeros stripped, one kept
  minimum), expo an integer. Zero: [1, 0.0, 0] / [-1, 0.0, 0].
  Infinities: [1, inf] / [-1, inf]. nan is the only special word.

No probes are run. Pure re-derivation and comparison; read-only.
"""
import csv
import decimal
import os
import struct
import sys
from fractions import Fraction

csv.field_size_limit(sys.maxsize)

decimal.getcontext().prec = 80
MANT_DIGITS = 31

_BASES = ["<USER_HOME>/Programming", "/sessions/bold-relaxed-tesla/mnt/Programming"]
_BASE = next((b for b in _BASES if os.path.isdir(b)), _BASES[0])
HERE = os.path.join(_BASE, "PseudoCoupHQ/Research/kind_fuzz_clustering")
CART = os.path.join(HERE, "matrices_cart_v2")
AIRLOCK = os.path.join(_BASE, "Airlock/agent/out")
SANDBOX = os.path.join(_BASE, "SandboxDesign/agent/out")


def canon_num_independent(fr):
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


def decode_int(bits, hx):
    v = int(hx, 16)
    if v >= (1 << (bits - 1)):
        v -= (1 << bits)
    return v


def decode_uint(hx):
    return int(hx, 16)


def decode_float(bits, hx):
    raw = bytes.fromhex(hx)
    fmt = ">d" if bits == 64 else ">f"
    return struct.unpack(fmt, raw)[0]


def canon_of_payload(type_name, enc):
    """independent decode+canon for INT / UINT / BIGINT / FLOAT / BOOL
    payloads -- the numeric/bool subset needed for spot verification."""
    if enc.startswith("BOOL:"):
        return "true" if enc[5:] == "true" else "false"
    if enc.startswith("INT:"):
        _, bits, hx = enc.split(":", 2)
        return canon_num_independent(Fraction(decode_int(int(bits), hx)))
    if enc.startswith("UINT:"):
        _, bits, hx = enc.split(":", 2)
        return canon_num_independent(Fraction(decode_uint(hx)))
    if enc.startswith("BIGINT:"):
        p = enc[7:]
        neg = p.startswith("-")
        p = p.lstrip("-")
        v = int(p, 16) if p else 0
        if neg:
            v = -v
        return canon_num_independent(Fraction(v))
    if enc.startswith("FLOAT:"):
        _, bits, hx = enc.split(":", 2)
        v = decode_float(int(bits), hx)
        if v != v:
            return "nan"
        if v == float("inf"):
            return "[1, inf]"
        if v == float("-inf"):
            return "[-1, inf]"
        if v == 0.0:
            neg = struct.pack(">d", v)[0] & 0x80
            return "[-1, 0.0, 0]" if neg else "[1, 0.0, 0]"
        return canon_num_independent(Fraction(v))
    return None   # not a type this spot-checker independently decodes


_INDEX_CACHE = {}


def index_for(files):
    key = tuple(files)
    idx = _INDEX_CACHE.get(key)
    if idx is not None:
        return idx
    idx = {}
    for fn in files:
        if not os.path.exists(fn):
            continue
        with open(fn, "r", errors="replace") as fh:
            for line in fh:
                p, _, rest = line.rstrip("\n").partition("|")
                if p:
                    idx[p] = rest          # later files override earlier
    _INDEX_CACHE[key] = idx
    return idx


def find_raw_line(pid, files):
    """indexed lookup; last file in the given order wins on a
    duplicate pid (worker-shard override semantics)."""
    return index_for(files).get(pid)


def raw_files_for(lang, level):
    tag = "l1" if level == 1 else "l2"
    cands = {
        "go": [f"{AIRLOCK}/ct_go_{tag}.txt"],
        "typescript": [f"{AIRLOCK}/ct_typescript_{tag}.txt"],
        "java": [f"{AIRLOCK}/ct_java_{tag}.txt"],
        "csharp": [f"{AIRLOCK}/ct_csharp_{tag}.txt"],
        "swift": [f"{AIRLOCK}/ct_swift_{tag}.txt"],
        "dart": [f"{AIRLOCK}/ct_dart_{tag}.txt"],
        "cpp": [f"{AIRLOCK}/ct_cpp_{tag}.txt"] if level == 1 else
               sorted(f"{AIRLOCK}/ct_cpp_l2_s{i}.txt" for i in range(2)),
        "kotlin": [f"{AIRLOCK}/ct_kotlin_{tag}.txt"] if level == 1 else
               sorted(f"{AIRLOCK}/ct_kotlin_l2_s{i}.txt" for i in range(2)),
        "php": [f"{AIRLOCK}/ct_php_{tag}.txt"] +
               sorted(f"{AIRLOCK}/ct_php_{tag}.w{i}.txt" for i in range(5)),
        "rust_release": [f"{SANDBOX}/ct_rust_release_{tag}.txt"],
    }
    return cands[lang]


def read_rust_shape_line(rest):
    """`type|encoding` OR `-|RAISE:...` / `-|ABORT` / `-|BUILDFAIL` /
    `-|MISSING` -> independent canon-or-token, or None if not decodable
    by this spot-checker (containers/text/etc.)."""
    if rest is None:
        return "MISSING-FROM-RAW"
    if rest.startswith("-|RAISE:"):
        return ("RAISE", rest[len("-|RAISE:"):])
    if rest.startswith("-|ABORT"):
        return "ABORT"
    if rest.startswith("-|BUILDFAIL"):
        return "REFUSE"
    if rest.startswith("-|MISSING"):
        return "ABORT"
    tname, _, enc = rest.partition("|")
    c = canon_of_payload(tname, enc)
    return c


def check_language(lang, level, op, n_samples=8):
    csv_path = os.path.join(CART, f"{lang}.{op}.L{level}.csv")
    if not os.path.exists(csv_path):
        return None
    files = raw_files_for(lang, level)
    checked = matched = skipped = mismatched = 0
    mismatches = []
    with open(csv_path) as fh:
        for row in csv.DictReader(fh):
            pid_row = row["probe_id"]
            vec = row["output_canon_vector"].split(";")
            n = int(row["n_probes"])
            # sample evenly across the row rather than only position 0
            step = max(1, n // n_samples)
            for p in range(0, n, step):
                raw_pid = f"{pid_row}_{p}"
                rest = find_raw_line(raw_pid, files)
                indep = read_rust_shape_line(rest)
                got = vec[p]
                checked += 1
                if indep is None:
                    skipped += 1
                    continue
                if isinstance(indep, tuple) and indep[0] == "RAISE":
                    ok = got.startswith("RAISE:")
                elif indep == "MISSING-FROM-RAW":
                    ok = False
                else:
                    ok = (got == indep)
                if ok:
                    matched += 1
                else:
                    mismatched += 1
                    mismatches.append((raw_pid, rest, got, indep))
            if checked > 200:
                break
    return dict(lang=lang, op=op, level=level, checked=checked,
                matched=matched, skipped=skipped, mismatched=mismatched,
                mismatches=mismatches[:5])


if __name__ == "__main__":
    only_l2 = "--l2" in sys.argv
    plan_l1 = [
        ("go", 1, "plus"), ("go", 1, "star"),
        ("typescript", 1, "plus"), ("typescript", 1, "star"),
        ("java", 1, "plus"), ("java", 1, "slash"),
        ("csharp", 1, "plus"), ("csharp", 1, "percent"),
        ("swift", 1, "star"), ("swift", 1, "gt"),
        ("dart", 1, "star"), ("dart", 1, "slash"),
        ("cpp", 1, "plus"), ("cpp", 1, "star"),
        ("kotlin", 1, "plus"), ("kotlin", 1, "star"),
        ("php", 1, "plus"), ("php", 1, "star"),
        ("rust_release", 1, "plus"), ("rust_release", 1, "star"),
    ]
    plan_l2 = [
        ("go", 2, "plus"),
        ("cpp", 2, "plus"),
        ("php", 2, "plus"),
        ("kotlin", 2, "plus"),
        ("typescript", 2, "plus"),
        ("rust_release", 2, "plus"),
    ]
    plan = plan_l2 if only_l2 else plan_l1
    total_checked = total_matched = total_mismatched = total_skipped = 0
    for lang, level, op in plan:
        r = check_language(lang, level, op)
        if r is None:
            print(f"{lang}.{op}.L{level}: NO FILE")
            continue
        total_checked += r["checked"]
        total_matched += r["matched"]
        total_mismatched += r["mismatched"]
        total_skipped += r["skipped"]
        print(f"{lang}.{op}.L{level}: checked={r['checked']} "
              f"matched={r['matched']} mismatched={r['mismatched']} "
              f"skipped(non-numeric)={r['skipped']}")
        for mm in r["mismatches"]:
            print("   MISMATCH", mm)
    print("=====")
    print(f"TOTAL checked={total_checked} matched={total_matched} "
          f"mismatched={total_mismatched} skipped={total_skipped}")
