#!/usr/bin/env python3
"""l3_row_sim.py -- the owner's rulings A and B, settled 2026-08-21, as one
scoring module.  Imported by `l3_row_graph_v2.py`; `l3_row_graph.py`
(the log-050 byte-identity builder) is left on disk unchanged for the
audit trail.

RULING A -- similarity is PER ELEMENT and NUMERIC, not byte identity.

    A canonical numeric answer is `[sign, mant, expo]`.  Two of them are
    compared ELEMENT BY ELEMENT, AS NUMBERS:

      sign  distance |sign_0 - sign_1|, which is 0 or 2.  A sign flip
            costs real distance -- the owner's call: across a 32-point
            interval, closeness that survives a sign flip is
            coincidence, and the ladder makes it vanishingly rare.
            sign_sim = 1 - |d| / 2, so {1.0, 0.0}.
      mant  distance |mant_0 - mant_1|.  Mants live in [1,2), so the
            distance is already bounded by 1 and needs no scale
            constant: mant_sim = 1 - |d|, clamped at 0.  (The clamp is
            not decoration: zero canonicalizes to mant 0.0 and a mant
            that rounds up at the 31st digit spells 2.0, so |d| can
            reach 2.  Both are real distance and both floor at 0.)
      expo  distance |expo_0 - expo_1|, an unbounded integer, so it
            needs a DECAY to become a similarity.  The decay is the
            KNOB: EXPO_DECAY below.  Default `reciprocal`,
            expo_sim = 1 / (1 + |d|).

    The three element similarities are combined into ONE per-sample
    similarity by COMBINE, a single constant to change.  Default
    `euclidean`, the owner's sketch: the distance from the perfect point
    (1,1,1) in element-similarity space, normalised by sqrt(3) so the
    result lands in [0,1].

RULING A -- FORM CLASSIFIER, not cast-and-catch.  Every output_canon
    declares its form in its prefix:

      `[`            numeric        (`[sign, mant, expo]`, or the
                                     non-finite `[1, inf]` / `[-1, inf]`)
      `nan`          numeric        (the one special word the canon keeps)
      `t|`           text
      `c|`           container
      `true`/`false` truth
      `opaque:`      opaque         (a value the canon does not decompose:
                                     rust `Range`, ruby `Complex`)
      REFUSE / RAISE:<kind> / ABORT   an outcome token -- a DECLINE

    SAME form -> compare by that form's rule.  DIFFERENT form ->
    similarity 0.  No exceptions, no casting, no caught errors.

RULING B -- DECLINES ARE NOT SCORED AT ALL.  the owner: "lets only do matching
    on similarity of actual objects now.  lets avoid things like
    REFUSE/RAISE/whatever-else."

    A sample position where EITHER side's output is REFUSE, RAISE:* or
    ABORT is EXCLUDED from the comparison entirely -- out of the
    numerator AND out of the denominator.  If two rows share an input
    ladder but have ZERO comparable positions after exclusion there is
    NO connector between them at all, not a zero-weight one.

    Every comparison records `n_comparable`, `n_excluded_declines` and
    the weight.  The old byte-identity weight is kept as a SECONDARY
    recorded number (`weight_byte`, over all n_samples positions, so it
    is directly comparable with log 050); the PRIMARY weight is the
    ruling-A/B one.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree; the
OS-stopped outcome is ABORT.
"""

import decimal
import math

decimal.getcontext().prec = 60

# ---- the knobs, each a single constant ---------------------------
EXPO_DECAY = "reciprocal"     # expo_sim = 1 / (1 + |d|)
EXPO_DECAY_K = 1.0            # the 1 in 1/(1 + K*|d|)
COMBINE = "euclidean"         # or "weighted_mean"
COMBINE_WEIGHTS = (1.0, 1.0, 1.0)      # sign, mant, expo -- weighted_mean only
SIGN_MAX_DISTANCE = 2.0       # |1 - (-1)|
_R3 = math.sqrt(3.0)

KNOBS = dict(expo_decay=EXPO_DECAY, expo_decay_k=EXPO_DECAY_K,
             combine=COMBINE, combine_weights=list(COMBINE_WEIGHTS),
             sign_max_distance=SIGN_MAX_DISTANCE,
             mant_scale="none -- mants live in [1,2), distance already "
                        "bounded by 1; clamped at 0 for the zero mant "
                        "0.0 and a 31st-digit round-up to 2.0")


# ------------------------------------------------------------------
# the form classifier
# ------------------------------------------------------------------

DECLINE = "decline"


def is_decline(s):
    return s == "REFUSE" or s == "ABORT" or s.startswith("RAISE:")


def form_of(c):
    """The form a canon cell declares in its own prefix.  Total: every
    string lands in exactly one form and nothing raises."""
    if is_decline(c):
        return DECLINE
    if c.startswith("["):
        return "numeric"
    if c == "nan":
        return "numeric"
    if c.startswith("t|"):
        return "text"
    if c.startswith("c|"):
        return "container"
    if c == "true" or c == "false":
        return "truth"
    if c.startswith("opaque:"):
        return "opaque"
    return "other"


# ------------------------------------------------------------------
# numeric form
# ------------------------------------------------------------------

def parse_numeric(c):
    """`[sign, mant, expo]` -> (sign, Decimal mant, int expo).
    A non-finite (`[1, inf]`, `[-1, inf]`, `nan`) has no mant and no
    expo to difference, so it returns None and the form's rule falls
    back to identity."""
    if c == "nan":
        return None
    body = c[1:-1] if c.endswith("]") else c[1:]
    parts = [p.strip() for p in body.split(",")]
    if len(parts) != 3:
        return None                       # [1, inf] / [-1, inf]
    try:
        return (int(parts[0]), decimal.Decimal(parts[1]), int(parts[2]))
    except (ValueError, ArithmeticError, decimal.InvalidOperation):
        return None


def expo_sim(d):
    if EXPO_DECAY == "reciprocal":
        return 1.0 / (1.0 + EXPO_DECAY_K * float(d))
    raise ValueError("unknown EXPO_DECAY %r" % EXPO_DECAY)


def combine(sign_s, mant_s, exp_s):
    if COMBINE == "euclidean":
        d = math.sqrt((1.0 - sign_s) ** 2 + (1.0 - mant_s) ** 2 +
                      (1.0 - exp_s) ** 2) / _R3
        return max(0.0, min(1.0, 1.0 - d))
    if COMBINE == "weighted_mean":
        w = COMBINE_WEIGHTS
        return max(0.0, min(1.0, (w[0] * sign_s + w[1] * mant_s +
                                  w[2] * exp_s) / sum(w)))
    raise ValueError("unknown COMBINE %r" % COMBINE)


def numeric_sim(a, b):
    pa, pb = parse_numeric(a), parse_numeric(b)
    if pa is None or pb is None:
        # an infinity or a nan carries no mant and no expo; within the
        # numeric form it compares by identity, which is the honest
        # answer rather than an invented magnitude
        return 1.0 if a == b else 0.0
    s_s = 1.0 - abs(pa[0] - pb[0]) / SIGN_MAX_DISTANCE
    m_s = max(0.0, 1.0 - float(abs(pa[1] - pb[1])))
    e_s = expo_sim(abs(pa[2] - pb[2]))
    return combine(s_s, m_s, e_s)


def numeric_elements(a, b):
    """the three element similarities, for reporting a worked example."""
    pa, pb = parse_numeric(a), parse_numeric(b)
    if pa is None or pb is None:
        return None
    return dict(sign_sim=1.0 - abs(pa[0] - pb[0]) / SIGN_MAX_DISTANCE,
                mant_sim=max(0.0, 1.0 - float(abs(pa[1] - pb[1]))),
                expo_sim=expo_sim(abs(pa[2] - pb[2])),
                sign_distance=abs(pa[0] - pb[0]),
                mant_distance=str(abs(pa[1] - pb[1])),
                expo_distance=abs(pa[2] - pb[2]))


# ------------------------------------------------------------------
# text form -- NOT exercised by the interval pilot (numeric forms only);
# defined so the classifier is total rather than partial
# ------------------------------------------------------------------

def text_sim(a, b):
    if a == b:
        return 1.0
    fa, fb = a.split("|"), b.split("|")
    if len(fa) != 5 or len(fb) != 5:
        return 0.0
    if fa[1] == fb[1]:
        return 1.0                        # same NFC bytes
    try:
        s = [1.0 / (1.0 + abs(int(fa[k]) - int(fb[k]))) for k in (2, 3, 4)]
    except ValueError:
        return 0.0
    d = math.sqrt(sum((1.0 - x) ** 2 for x in s)) / _R3
    return max(0.0, min(1.0, 1.0 - d))


# ------------------------------------------------------------------
# one sample position
# ------------------------------------------------------------------

_SIM_CACHE = {}
_MISS = object()


def sample_sim(a, b):
    """similarity in [0,1], or None when the position is EXCLUDED
    because either side declined (ruling B).

    Memoised on the unordered pair: the same canon strings recur across
    tens of thousands of row pairs, and the function is symmetric and
    pure, so the cache changes speed and nothing else.
    """
    k = (a, b) if a <= b else (b, a)
    v = _SIM_CACHE.get(k, _MISS)
    if v is not _MISS:
        return v
    v = _sample_sim(a, b)
    _SIM_CACHE[k] = v
    return v


def _sample_sim(a, b):
    fa, fb = form_of(a), form_of(b)
    if fa == DECLINE or fb == DECLINE:
        return None                       # ruling B: not scored at all
    if fa != fb:
        return 0.0                        # ruling A: different form -> 0
    if fa == "numeric":
        return numeric_sim(a, b)
    if fa == "text":
        return text_sim(a, b)
    # truth, container, opaque, other: the form carries no numeric
    # elements to difference, so its rule is identity
    return 1.0 if a == b else 0.0


# ------------------------------------------------------------------
# one row pair
# ------------------------------------------------------------------

def row_sim(va, vb):
    """Two ladder-aligned output vectors -> the ruling A/B record.

    Returns None when there is NO comparable position -- ruling B says
    that is not a zero-weight connector, it is no connector.
    """
    n = len(va)
    total = 0.0
    n_cmp = 0
    n_exc = 0
    n_byte = 0
    for i in range(n):
        if va[i] == vb[i]:
            n_byte += 1
        s = sample_sim(va[i], vb[i])
        if s is None:
            n_exc += 1
            continue
        n_cmp += 1
        total += s
    if n_cmp == 0:
        return None
    return dict(n_samples=n, n_comparable=n_cmp,
                n_excluded_declines=n_exc,
                weight=round(total / n_cmp, 6),
                sum_similarity=round(total, 6),
                n_matched_byte=n_byte,
                weight_byte=round(n_byte / n, 6) if n else 0.0)
