#!/usr/bin/env python3
"""points.py -- the level-0 points: edge values first, then random.

For every operation in ops.json (gen.py), in each of the five rounding
modes the model encodes (000 RNE, 001 RTZ, 010 RDN, 011 RUP, 100 RMM)
when the operation takes one; a comparison takes none and is run once.

  edge    every ordered pair over the edge values of the operation's
          format: both zeros; both infinities; quiet and signalling NaNs,
          with and without payload and sign; the smallest and largest
          subnormal and normal; 1 and its two neighbours; and the halfway
          cases built in:
            2^(m+1) with 1 and with 3          a tie in the sum
            3 with 2^m + 1                     a tie in the product
            the smallest normal plus one ulp
              with 1/2 and with 2              a tie at the subnormal quantum
            the largest normal with half an
              ulp of it                        a tie at overflow
            a pair whose exact product lies    tininess: rounding at the
              just below the smallest normal     format's precision and at
              with its first m+1 bits all ones   the subnormal quantum part
  random  (full mode) per operation and mode: uniform bit patterns;
          pairs of close exponent; subnormal operands; exponents whose sum
          or difference sits at overflow or underflow; sums built to tie.

The format parameters are the IEEE 754 binary formats' own (exponent
bits, significand bits): 16 -> (5, 10), 32 -> (8, 23), 64 -> (11, 52).
"""
import argparse
import json
import random

FORMATS = {16: (5, 10), 32: (8, 23), 64: (11, 52)}
MODES = [0, 1, 2, 3, 4]
GATE = {"pos_zero", "neg_zero", "pos_inf", "qnan", "snan", "min_sub", "max_normal", "one",
        "three", "tie_base", "succ_min_normal", "half", "two", "tiny_boundary_a", "tiny_boundary_b"}


def fmt(w):
    e, m = FORMATS[w]
    return e, m, (1 << (e - 1)) - 1


def enc(w, s, E, M):
    e, m, _ = fmt(w)
    return (s << (e + m)) | (E << m) | M


def exact(w, s, n, k):
    """the encoding of (-1)^s * n * 2^k when exactly representable, else None"""
    e, m, bias = fmt(w)
    if n == 0:
        return enc(w, s, 0, 0)
    while n % 2 == 0:
        n //= 2
        k += 1
    L = n.bit_length()
    if L > m + 1:
        return None
    emin, emax, qmin = 1 - bias, bias, 1 - bias - m
    top = k + L - 1
    if top > emax:
        return None
    if top >= emin:
        return enc(w, s, top + bias, (n << (m + 1 - L)) - (1 << m))
    if k < qmin:
        return None
    return enc(w, s, 0, n << (k - qmin))


def tiny_boundary(w):
    """a, b with a * b = N * 2^(qmin - 1 - k), N = (2^(m+1) - 1) * 2^k + r,
    0 < r < 2^(k-1): the exact product is below the smallest normal, its
    first m+1 bits are all ones and the next bit is zero. Found by a
    divisor search, None when none is found in the bound."""
    e, m, bias = fmt(w)
    qmin = 1 - bias - m
    for k in range(2, m + 2):
        for r in (1, 3, 5, 7):
            if r >= (1 << (k - 1)):
                continue
            N = (((1 << (m + 1)) - 1) << k) + r
            need = max(0, N.bit_length() - (m + 1))
            lo = max(3, 1 << max(0, need - 1)) | 1
            for d in range(lo, min(1 << (m + 1), lo + 400000), 2):
                if N % d == 0 and (N // d).bit_length() <= m + 1:
                    a, b = exact(w, 0, d, -1 - k), exact(w, 0, N // d, qmin)
                    if a is not None and b is not None:
                        return a, b
    return None, None


def edges(w):
    e, m, bias = fmt(w)
    X = (1 << e) - 1
    V = [
        ("pos_zero", enc(w, 0, 0, 0)), ("neg_zero", enc(w, 1, 0, 0)),
        ("pos_inf", enc(w, 0, X, 0)), ("neg_inf", enc(w, 1, X, 0)),
        ("qnan", enc(w, 0, X, 1 << (m - 1))), ("neg_qnan_payload", enc(w, 1, X, (1 << (m - 1)) | 1)),
        ("snan", enc(w, 0, X, 1)), ("neg_snan_max_payload", enc(w, 1, X, (1 << (m - 1)) - 1)),
        ("min_sub", enc(w, 0, 0, 1)), ("neg_min_sub", enc(w, 1, 0, 1)),
        ("three_min_sub", enc(w, 0, 0, 3)), ("five_min_sub", enc(w, 0, 0, 5)),
        ("max_sub", enc(w, 0, 0, (1 << m) - 1)), ("neg_max_sub", enc(w, 1, 0, (1 << m) - 1)),
        ("min_normal", enc(w, 0, 1, 0)), ("neg_min_normal", enc(w, 1, 1, 0)),
        ("succ_min_normal", enc(w, 0, 1, 1)), ("neg_succ_min_normal", enc(w, 1, 1, 1)),
        ("max_normal", enc(w, 0, X - 1, (1 << m) - 1)), ("neg_max_normal", enc(w, 1, X - 1, (1 << m) - 1)),
        ("half_ulp_of_max", enc(w, 0, 2 * bias - m - 1, 0)), ("neg_half_ulp_of_max", enc(w, 1, 2 * bias - m - 1, 0)),
        ("quarter_ulp_of_max", enc(w, 0, 2 * bias - m - 2, 0)),
        ("one", enc(w, 0, bias, 0)), ("neg_one", enc(w, 1, bias, 0)),
        ("succ_one", enc(w, 0, bias, 1)), ("pred_one", enc(w, 0, bias - 1, (1 << m) - 1)),
        ("two", enc(w, 0, bias + 1, 0)), ("three", enc(w, 0, bias + 1, 1 << (m - 1))),
        ("neg_three", enc(w, 1, bias + 1, 1 << (m - 1))),
        ("half", enc(w, 0, bias - 1, 0)), ("neg_half", enc(w, 1, bias - 1, 0)),
        ("tie_base", enc(w, 0, bias + m + 1, 0)), ("neg_tie_base", enc(w, 1, bias + m + 1, 0)),
        ("odd_m1_bits", enc(w, 0, bias + m, 1)),
    ]
    a, b = tiny_boundary(w)
    if a is not None:
        V += [("tiny_boundary_a", a), ("tiny_boundary_b", b), ("neg_tiny_boundary_a", a | (1 << (e + m)))]
    return V


def rand_points(w, rng, count):
    e, m, bias = fmt(w)
    X = (1 << e) - 1
    emin, emax = 1 - bias, bias
    out = []
    for _ in range(count // 4):
        out.append((rng.getrandbits(w), rng.getrandbits(w), "rand_bits"))
    for _ in range(count // 4):
        E = rng.randint(1, X - 1)
        E2 = min(X - 1, max(1, E + rng.randint(-2, 2)))
        out.append((enc(w, rng.getrandbits(1), E, rng.getrandbits(m)),
                    enc(w, rng.getrandbits(1), E2, rng.getrandbits(m)), "rand_close"))
    for _ in range(count * 3 // 20):
        a = enc(w, rng.getrandbits(1), 0, rng.randint(1, (1 << m) - 1))
        if rng.random() < 0.5:
            b = enc(w, rng.getrandbits(1), 0, rng.randint(1, (1 << m) - 1))
        else:
            b = enc(w, rng.getrandbits(1), rng.randint(1, min(X - 1, m + 2)), rng.getrandbits(m))
        if rng.random() < 0.5:
            a, b = b, a
        out.append((a, b, "rand_subnormal"))
    for _ in range(count * 7 // 40):
        t = rng.choice([emax, emax + 1, emin - 1, emin - m, emin - m - 1, emin])
        xa = rng.randint(emin, emax)
        xb = t - xa if rng.random() < 0.5 else xa - t
        xb = max(emin, min(emax, xb))
        out.append((enc(w, rng.getrandbits(1), xa + bias, rng.getrandbits(m)),
                    enc(w, rng.getrandbits(1), xb + bias, rng.getrandbits(m)), "rand_range_edge"))
    while len(out) < count:
        E = rng.randint(m + 2, X - 1)
        a = enc(w, rng.getrandbits(1), E, rng.getrandbits(m))
        b = enc(w, rng.getrandbits(1), E - m - 1, rng.choice([0, 0, 0, 1 << (m - 1), rng.getrandbits(m)]))
        out.append((a, b, "rand_tie"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ops", required=True)
    ap.add_argument("--mode", choices=["gate", "full"], required=True)
    ap.add_argument("--seed", type=int, default=20260915)
    ap.add_argument("--random", type=int, default=1000)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tags", required=True)
    args = ap.parse_args()
    ops = json.load(open(args.ops))["ops"]
    lines, tags = [], []
    edge_cache = {}
    for op in ops:
        w = op["width"]
        if w not in edge_cache:
            edge_cache[w] = edges(w)
            found = [n for n, _ in edge_cache[w] if n.startswith("tiny_boundary")]
            print("  binary%d: %d edge values%s" % (w, len(edge_cache[w]),
                  "" if found else "; NO tininess-boundary pair found in the search bound"))
        E = edge_cache[w] if args.mode == "full" else [v for v in edge_cache[w] if v[0] in GATE]
        for rm in (MODES if op["shape"] == "rm2" else [0]):
            for na, a in E:
                for nb, b in E:
                    lines.append("%s %x %x %x" % (op["name"], rm, a, b))
                    tags.append("edge %s %s" % (na, nb))
            if args.mode == "full":
                rng = random.Random("%d:%s:%d" % (args.seed, op["name"], rm))
                for a, b, kind in rand_points(w, rng, args.random):
                    lines.append("%s %x %x %x" % (op["name"], rm, a, b))
                    tags.append("random %s" % kind)
    open(args.out, "w").write("\n".join(lines) + "\n")
    open(args.tags, "w").write("\n".join(tags) + "\n")
    print("  points: %d (%s)" % (len(lines), args.mode))


if __name__ == "__main__":
    main()
