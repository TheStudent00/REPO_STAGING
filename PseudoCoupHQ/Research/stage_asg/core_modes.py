#!/usr/bin/env python3
"""core_modes.py -- every accepted ship unit re-emitted as a CORE and a
list of MODES.

The shape, in the owner's words
------------------------
  core     the normal-path lifted form: the dataflow term(s) of the
           path that reaches `ret` without passing a trap or a panic
           response.
  modes[]  the ways the unit leaves that path, each one
           {condition, response, detection}.

Why the split is worth making: `verdicts.py` already had both halves and
kept them apart only inside one verdict.  `DIFFERS-BY-DESIGN` means
"the cores are equal and one side has a mode the other has not".  This
file makes that the STANDING SHAPE of a unit rather than a thing the
comparison discovers, so a relation can be computed as a column
(verdicts4.py) instead of decided by a cascade.

THE SPELLING BAN (AgentMemory, restated by the owner 2026-08-25).  No operator
token appears in any key, grouping, pairing, row structure, candidate
selection or comparison scope here.  The candidate set for the solver
route is verdicts3.py's own machine-form groups, imported.  The token
appears exactly once per unit: as the display label `operator` on the
unit record, beside `lang` and `n`.  `check_no_spelling_keys.py` is run
on the output of this file and a FAIL means the output is refused.

--------------------------------------------------------------------
THE CORE
--------------------------------------------------------------------
`verdicts.core_values` is imported unchanged.  It already computes
exactly the thing named above: every value computed in a block that is
NOT a trap/panic block, minus three kinds of value it names and argues
for (a pass-through, a value mentioning no operand, and the guard's own
branch machinery).  Nothing is re-derived here.

One limit, stated rather than hidden: `core_values` walks every
non-response block, not only the blocks a path to `ret` can reach.  In
this corpus every non-response block does reach `ret`; that is an
observation over these units, not a proof, and it is marked UNVERIFIED
on the output.

--------------------------------------------------------------------
MODES, ROUTE 1 -- branch-to-response
--------------------------------------------------------------------
The existing guard machinery, imported: `verdicts.guard_blocks` finds
each block that traps or calls a panic-like callee, and
`verdicts.divergence_conditions` reads the conditional branch that lands
in it and decodes the condition into words with `verdicts.describe`.

  condition   the decoded words where the decoder can read the form,
              the serialized lifted form where it cannot -- never a
              guess.  `lifted` is carried beside it always.
  response    `trap` for a trap event; `panic-call:<callee>` for a call
              to a panic-like callee, the callee named.
  detection   `branch-to-response`.

A SECOND, DERIVED mode of this route, and the one place a mode is read
off another unit: where a unit has NO response block, and a unit
CONNECTED to it by machine-form evidence has one whose decoded
condition says the operation OVERFLOWS, the bare unit is recorded as
carrying a mode with that same condition and the response
`wrap-continue`.  What is this unit's own evidence and what is not:
that this unit has no branch to a response is its own fact; the
CONDITION is read from the other unit's lifted guard and the mode
records `read_from` naming that unit.  The mode is never claimed as
this unit's own branch.

--------------------------------------------------------------------
MODES, ROUTE 2 -- solver-localized (the branchless case)
--------------------------------------------------------------------
go's shift clamps without branching:

    mov %rbx,%rcx ; shl %cl,%eax ; cmp $0x20,%rcx ; sbb %edx,%edx ;
    and %edx,%eax

`sbb %edx,%edx` after `cmp` is minus-the-borrow: all ones when the
shift amount is below 32, zero otherwise.  The `and` therefore zeroes
the answer for every shift amount of 32 or more.  There is no branch,
so route 1 sees nothing at all, and c's bare `shl` for the same types
differs from it -- but only in a REGION.

So: when two units that machine-form evidence has already CONNECTED
have different cores, z3 is asked where they disagree, and the
disagreement is offered a small set of simple predicates over the
anchored inputs.  A predicate P is accepted only when BOTH of these
come back inside the budget:

  (a) z3 proves  NOT P  =>  the two results are equal        (unsat)
  (b) z3 finds a model of  P  AND  the two results differ    (sat)

that is: outside P they agree, inside P they really do disagree.  P is
then recorded as a MODE DIFFERENCE on the unit, with the response
worked out by one further query:

  clamp-continue   z3 proves that inside P this unit's result is 0
  continue-with-a-different-answer   otherwise

THE PREDICATE TEMPLATES TRIED, in this order, and there are no others:

  T1  unsigned threshold on one input:  in_i >=u k
      for i in (0, 1) and k in (64, 32, 16, 8) -- LARGEST FIRST, so the
      region accepted is the tightest one the template can state
  T2  sign test on one input:           in_i <s 0
      for i in (0, 1)
  T3  equality with a constant:         in_i == c
      for i in (0, 1) and c in (0, 1, -1, -2147483648,
      -9223372036854775808)

BUDGET.  At most 40 solver queries per pair, each capped at 2000 ms,
and at most 90 seconds of wall clock per pair.  When the budget is
spent with nothing accepted, NO MODE IS CLAIMED: the difference stays a
core difference and the unit records why the attempt failed.  A
template that was never reached because the budget ran out is recorded
as such rather than as a template that failed.

SCOPE.  Route 2 is not asked about a pair whose operands are IEEE
floats.  Every template above is an INTEGER predicate; asked about a
float operand, `in1 >= 32 (unsigned)` names an interval of BIT PATTERNS
and not an interval of numbers, so an accepted region would read as a
statement about the value when it is a statement about the encoding.
Measured beside that reason: a floating-point pair spends the whole wall
budget and answers nothing.  Those pairs keep a core difference and the
skip is recorded on both units.

Only pairs where BOTH units are single-block pure dataflow are asked --
the translation z3_ext gives is defined on those and nothing else.  A
connected pair that is not of that shape is recorded as not asked, with
that reason.

RESUMABLE.  The sandbox this was developed in kills a process after
about two minutes, so route 2's answers are cached in
`core_modes_cache.json` and `--budget=SECONDS` stops the pass cleanly
and asks to be run again.  The cache is a resume point and changes no
answer.

usage:
  core_modes.py                write core_modes_<lang>.json
  core_modes.py --no-solver    route 1 only (fast; route 2 recorded as
                               not run)
  core_modes.py --budget=90    stop asking after 90 seconds, cache, and
                               exit 3 to say "run me again"
"""

import json
import os
import re
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import verdicts as V                                          # noqa: E402
import verdicts3 as V3                                        # noqa: E402
import z3_ext as X                                            # noqa: E402
import sem_anchored as SA                                     # noqa: E402
import arch_sem as AS                                         # noqa: E402
import z3                                                     # noqa: E402


# MEASURED, and the reason the numbers are what they are.  A first
# Airlock run with a 2000 ms cap and a 90-second wall budget per pair
# did not reach its first 500-pair checkpoint in 21 minutes: a
# floating-point pair can spend the whole wall budget and answer
# nothing.  The caps below are the ones the pass actually runs with.
# The effect is one-directional and honest: a region a slower query
# would have localized is not localized, and the pair keeps a core
# difference with the budget note on it.  It never invents a mode.
SOLVER_CAP_MS = 1000
QUERIES_PER_PAIR = 40
SECONDS_PER_PAIR = 20


# ---------------------------------------------------------------- route 1

def response_of(event):
    """the name of what a response block does."""
    if event.startswith("trap "):
        return "trap"
    if event.startswith("call "):
        callee = event.split(None, 1)[1]
        callee = callee.strip("*")
        callee = callee.split("(")[0]
        return "panic-call:%s" % callee
    return "response-block"


OVERFLOW_WORDS = re.compile(r"overflow|carries out of")


def branch_modes(unit):
    """the modes route 1 finds on one unit."""
    blocks = unit["sem"]["blocks"]
    gmap = V.guard_blocks(blocks)
    if not gmap:
        return [], gmap
    conds = V.divergence_conditions(unit, gmap)
    out = []
    for c in conds:
        lands = c.get("lands_in")
        if isinstance(lands, list):
            lands = "; ".join(lands)
        response = response_of(str(lands or ""))
        out.append(dict(
            condition=c.get("condition", c.get("text", "?")),
            lifted=c.get("lifted", "?"),
            response=response,
            detection="branch-to-response",
            branch=c.get("branch", "?"),
            lands_in=lands,
        ))
    return out, gmap


# ---------------------------------------------------------------- route 2

class Budget(object):
    def __init__(self):
        self.queries = 0
        self.started = time.time()
        self.spent = False

    def take(self):
        if self.queries >= QUERIES_PER_PAIR:
            self.spent = True
            return False
        if time.time() - self.started > SECONDS_PER_PAIR:
            self.spent = True
            return False
        self.queries += 1
        return True


def single_block_form(unit):
    """(results, names) for a unit that is one block of pure dataflow,
    or (None, reason)."""
    blocks = unit["sem"]["blocks"]
    if len(blocks) != 1:
        return None, ("%s op_%s is not straight-line: %d blocks"
                      % (unit["lang"], unit["n"], len(blocks)))
    events = blocks[0]["events"]
    bad = []
    for ev in events:
        if not V.PURE_EVENT.match(ev):
            bad.append(ev)
    if bad:
        return None, ("%s op_%s is not pure scalar dataflow: %s"
                      % (unit["lang"], unit["n"], "; ".join(bad)))
    if blocks[0]["stores"]:
        return None, "%s op_%s writes memory" % (unit["lang"], unit["n"])
    summaries, names, reason = SA.raw_summaries(
        dict(bytes=unit["bytes"].split(), mnem=unit["mnem"]),
        unit["lang"], unit["meta"])
    if summaries is None:
        return None, "the lift was refused: %s" % reason
    _parts, names = SA.render_anchored(summaries, names)
    return (summaries[0][0], names), None


FLOAT_REPS = ("f32", "f64")


def float_operands(record):
    """does either operand of this unit arrive as an IEEE float?"""
    for f in FLOAT_REPS:
        if f in str(record["type_pair"]):
            return True
    return False

RESULT_REGISTERS_INT = ["rax"]

RESULT_REGISTERS_FLOAT = ["xmm0", "ymm0", "zmm0"]


def lifted_state(unit):
    """arch_sem's sweep of block 0, with the register names still on it.

    `sem_anchored.raw_summaries` throws the names away -- `summarize`
    returns a list of values and not a map -- and for one job here the
    name is exactly what is needed.  Every step below is copied from
    `raw_summaries` and stops one line earlier."""
    import arch_read as AR                                    # noqa: E402
    payload = dict(bytes=unit["bytes"].split(), mnem=unit["mnem"])
    names = SA.anchor_names(unit["lang"], unit["meta"])
    if names is None:
        return None, None, "no ABI classification for the parameter types"
    lay, reason = SA.layout(payload)
    if lay is None:
        return None, names, reason
    rec = dict(state="OK", bytes=payload["bytes"], mnem=payload["mnem"],
               layout=lay)
    insns = AR.instructions(rec)
    if insns is None:
        return None, names, "arch_read refused the recovered layout"
    insns, _endbr = AR.strip_entry_endbr64(insns)
    insns, _go, _unmatched = AR.strip_go_stack_growth(insns)
    texts, _masked = AR.normalize_addresses(insns)
    index = {}
    for k, ins in enumerate(insns):
        index[ins["addr"]] = k
    spans, block_index = AS.blocks_of(insns, texts, index)
    lo, hi = spans[0]
    st = AS._sweep(insns, texts, index, block_index, lo, hi)
    return st, names, None


def abi_result(unit):
    """(expression, names, reason) -- the value the ABI's RESULT
    REGISTER holds when the unit returns.

    EVIDENCE CLASS, stated because it is the weakest one this file
    uses: human interpretation of stated design.  That an integer
    result comes back in %rax and a floating-point result in %xmm0 is
    the SysV and go conventions, not something these artifacts prove.
    It is used ONLY as a fallback, when the two units leave different
    numbers of live results and the question cannot be asked at all
    otherwise, and every claim built on it is marked
    `result_register_by_convention: UNVERIFIED`."""
    st, names, reason = lifted_state(unit)
    if st is None:
        return None, None, reason
    rep = unit["meta"].get("result_type") or ""
    wanted = RESULT_REGISTERS_INT
    for f in FLOAT_REPS:
        if f in str(unit["meta"].get("lhs_rep")) \
                or f in str(unit["meta"].get("rhs_rep")):
            wanted = RESULT_REGISTERS_FLOAT + RESULT_REGISTERS_INT
    for name in wanted:
        got = st.reg.get(name)
        if got is None:
            continue
        if got[0] == "r" and got[2] == name:
            continue
        return got, names, None
    return None, None, ("the unit writes no ABI result register (%s); "
                        "result type %r" % (", ".join(wanted), rep))


def build_claims(left, right):
    """([(a, b)], env, reason, by_convention) -- the result pairs of two
    units as z3 bitvectors, sharing the anchored input variables."""
    lform, lwhy = single_block_form(left)
    if lform is None:
        return None, None, None, lwhy
    rform, rwhy = single_block_form(right)
    if rform is None:
        return None, None, None, rwhy
    lv, lnames = lform
    rv, rnames = rform
    convention = False
    if len(lv) != len(rv):
        # THE FALLBACK, and the only place this file leans on a
        # convention.  go's branchless shift clamp leaves two live
        # values -- the answer in %rax and the mask it built in %rdx --
        # while c's bare shift leaves one, so the whole-unit question
        # cannot be asked.  The ANSWER can still be asked about: the
        # value the ABI's result register holds.  The claim is marked.
        la, lnames2, lwhy2 = abi_result(left)
        ra, rnames2, rwhy2 = abi_result(right)
        if la is None or ra is None:
            return None, None, None, (
                "the two units leave a different number of live results "
                "(%d and %d), and the result register fallback did not "
                "apply: %s" % (len(lv), len(rv), lwhy2 or rwhy2))
        lv = [la]
        rv = [ra]
        lnames = lnames2
        rnames = rnames2
        convention = True
    lv = sorted(lv, key=lambda x: (AS.W(x), AS._ser(x, lnames)))
    rv = sorted(rv, key=lambda x: (AS.W(x), AS._ser(x, rnames)))
    lside = X.Side(lnames, "L")
    rside = X.Side(rnames, "R")
    env = {}
    pairs = []
    try:
        for a, b in zip(lv, rv):
            av = X.bv(a, lside, env)
            bvv = X.bv(b, rside, env)
            n = min(av.size(), bvv.size())
            pairs.append((X.fit(av, n), X.fit(bvv, n)))
    except X.Unsupported as exc:
        return None, None, None, "z3 was not asked: %s" % exc
    return pairs, env, convention, None


def anchored_vars(env):
    """{0: variable, 1: variable} for the anchored inputs, widest form
    of each."""
    out = {}
    for key, var in sorted(env.items()):
        m = re.match(r"^in(\d+)_(\d+)$", key)
        if not m:
            continue
        i = int(m.group(1))
        if i not in out or var.size() > out[i].size():
            out[i] = var
    return out


def templates(vars_):
    """the predicates tried, in order, each as (words, z3 formula)."""
    out = []
    for i in sorted(vars_):
        var = vars_[i]
        # LARGEST THRESHOLD FIRST, and this order is load-bearing.  A
        # predicate is accepted when the two units agree OUTSIDE it, so
        # a smaller threshold names a LARGER region and is easier to
        # satisfy: `in1 >= 8` passes for the shift clamp even though the
        # units agree all the way to 31.  Trying the largest first makes
        # the accepted region the TIGHTEST one the templates can state.
        for k in (64, 32, 16, 8):
            if k >= (1 << var.size()):
                continue
            out.append(("in%d >= %d (unsigned)" % (i, k),
                        z3.UGE(var, z3.BitVecVal(k, var.size()))))
    for i in sorted(vars_):
        var = vars_[i]
        out.append(("in%d < 0 (signed)" % i,
                    var < z3.BitVecVal(0, var.size())))
    for i in sorted(vars_):
        var = vars_[i]
        for c in (0, 1, -1, -2147483648, -9223372036854775808):
            out.append(("in%d == %d" % (i, c),
                        var == z3.BitVecVal(c, var.size())))
    return out


def _ask(budget, *formulas):
    if not budget.take():
        return None, None
    s = z3.Solver()
    s.set("timeout", SOLVER_CAP_MS)
    for f in formulas:
        s.add(f)
    got = s.check()
    model = s.model() if got == z3.sat else None
    return got, model


def differ(pairs):
    claims = []
    for a, b in pairs:
        claims.append(a != b)
    if len(claims) == 1:
        return claims[0]
    return z3.Or(*claims)


def localize(left, right):
    """(mode, note).  The disagreement region of two connected units
    whose cores differ, when a template fits it."""
    pairs, env, convention, why = build_claims(left, right)
    if pairs is None:
        return None, why
    vars_ = anchored_vars(env)
    if not vars_:
        return None, ("no anchored operand reaches the results, so there "
                      "is nothing to state a predicate over")
    budget = Budget()
    D = differ(pairs)

    got, _model = _ask(budget, D)
    if got is None:
        return None, "the budget was spent before the first query"
    if got == z3.unsat:
        return None, ("the two units do not disagree on any input at the "
                      "common width, so the core difference is textual "
                      "only")
    if got != z3.sat:
        return None, "z3 returned %s on the disagreement query" % got

    tried = []
    for words, P in templates(vars_):
        outside, _m = _ask(budget, D, z3.Not(P))
        if outside is None:
            return None, ("the budget was spent after %d queries; %d "
                          "templates were tried and the rest were never "
                          "reached" % (budget.queries, len(tried)))
        if outside != z3.unsat:
            tried.append(words)
            continue
        inside, model = _ask(budget, D, P)
        if inside is None:
            return None, ("the budget was spent after %d queries"
                          % budget.queries)
        if inside != z3.sat:
            tried.append(words)
            continue
        response, rwhy = region_response(budget, pairs, P)
        shown = ""
        if model is not None:
            bits = []
            for d in sorted(model.decls(), key=lambda d: d.name()):
                bits.append("%s = %s" % (d.name(), model[d]))
            shown = ", ".join(bits)
        mode = dict(
            condition=words,
            lifted="(solver-localized; no branch carries this condition)",
            response=response,
            detection="solver-localized",
            templates_tried=len(tried) + 1,
            solver_queries=budget.queries,
            witness=shown,
            response_ground=rwhy,
        )
        if convention:
            mode["result_register_by_convention"] = "UNVERIFIED"
            mode["scope"] = ("the two units leave different numbers of "
                             "live values, so the claim is about the "
                             "value the ABI's result register holds and "
                             "not about every bit either unit writes")
        return mode, None
    return None, ("no template fitted the disagreement region after %d "
                  "queries; the templates tried were: %s"
                  % (budget.queries, "; ".join(tried)))


def region_response(budget, pairs, P):
    """what this unit does inside the region."""
    zeros = []
    for a, _b in pairs:
        zeros.append(a == z3.BitVecVal(0, a.size()))
    if len(zeros) == 1:
        claim = zeros[0]
    else:
        claim = z3.And(*zeros)
    got, _m = _ask(budget, P, z3.Not(claim))
    if got == z3.unsat:
        return ("clamp-continue",
                "z3 proved this unit's result is 0 throughout the region")
    if got is None:
        return ("continue-with-a-different-answer",
                "the budget was spent before the clamp query was answered")
    return ("continue-with-a-different-answer",
            "z3 found a point in the region where this unit's result is "
            "not 0, so the region is not a clamp to zero")


# --------------------------------------------------------- the vocabulary
#
# log_067: the three guaranteed adds are `wrapping`, `growing`,
# `approximating`.  They name what happens to the ANSWER, not the
# mechanism.  Only one of them fits a response this corpus produces.

MODE_NAMES = {"wrap-continue": "wrapping"}

VOCABULARY_NOTE = (
    "`wrapping`, `growing` and `approximating` are the interval-probe "
    "names (kind_fuzz_clustering, log_067).  A `wrap-continue` response "
    "IS `wrapping` and carries that name.  `clamp-continue` carries no "
    "name from that vocabulary: the three names describe what happens "
    "to the answer when the operation overflows, and clamping a shift "
    "to zero is not one of them.  `growing` and `approximating` do not "
    "occur here -- no unit in this corpus widens its result or returns "
    "an approximation -- and the tally says 0 rather than the name "
    "being left out.")


def named(mode):
    name = MODE_NAMES.get(mode["response"])
    if name is not None:
        mode["mode_name"] = name
    return mode


# ------------------------------------------------------------- the pass

def connected_pairs(units, by_id):
    """the unit pairs machine-form evidence connects.  verdicts3's own
    grouping, imported: cluster identity and the shared maximal
    sub-term, on the same operand type pair.  No token is involved."""
    rows = []
    rows.extend(V3.cluster_groups(by_id))
    rows.extend(V3.connection_groups(units, by_id))
    out = {}
    for row in rows:
        members = row["members"]
        for i, a in enumerate(members):
            for b in members[i + 1:]:
                if a["lang"] == b["lang"]:
                    continue
                key = tuple(sorted([(a["lang"], a["n"]),
                                    (b["lang"], b["n"])]))
                out[key] = row["type_pair"]
    return out


CACHE = "core_modes_cache.json"

# WHERE THE CACHE LIVES.  In Airlock the pass unpacks into a scratch
# directory that is wiped when the lane ends, so a lane that is killed
# at its timeout would lose its work.  `CORE_MODES_CACHE_DIR` points the
# cache at `/out` instead, which survives, and a re-dropped lane picks
# up where the killed one stopped.
CACHE_DIR = os.environ.get("CORE_MODES_CACHE_DIR") or HERE


def form_key(unit):
    """what route 2's answer actually depends on: the two anchored
    lifted forms and the operand type pair.  Two unit pairs with the
    same form key get the same answer, so the solver is asked once for
    all of them.  3436 core-differing unit pairs carry 2072 distinct
    form keys; the rest is repeated work and is skipped.  This is a
    machine form, not a spelling."""
    return "%s @@ %s" % (unit["sem"]["key"], V3.type_pair(unit["meta"]))


def cache_key(ua, ub):
    return "%s ||| %s" % (form_key(ua), form_key(ub))


def load_cache():
    path = os.path.join(CACHE_DIR, CACHE)
    if not os.path.exists(path):
        return {}
    return json.load(open(path))


def save_cache(cache):
    doc = cache
    path = os.path.join(CACHE_DIR, CACHE)
    tmp = path + ".tmp"
    fh = open(tmp, "w")
    json.dump(doc, fh)
    fh.close()
    os.replace(tmp, path)


def main():
    run_solver = "--no-solver" not in sys.argv
    budget_s = 0
    for arg in sys.argv[1:]:
        if arg.startswith("--budget="):
            budget_s = int(arg.split("=")[1])
    started = time.time()

    units, excluded, excluded_rows = V.load_units()
    for u in units:
        u["subterms"] = V3.unit_subterms(u)
    by_id = {}
    for u in units:
        by_id[(u["lang"], u["n"])] = u

    records = {}
    tally = Counter()
    for u in units:
        modes, gmap = branch_modes(u)
        core = V.core_values(u["sem"]["blocks"], gmap)
        records[(u["lang"], u["n"])] = dict(
            lang=u["lang"], n=u["n"], operator=u["meta"].get("operator"),
            type_pair=V3.type_pair(u["meta"]), meta=u["meta"],
            bytes=u["bytes"], core=core, modes=modes,
            response_blocks=sorted(gmap.values()),
            solver_notes=[])
        tally["units"] += 1

    pairs = connected_pairs(units, by_id)
    print("units %d; connected unit pairs %d" % (len(units), len(pairs)))
    sys.stdout.flush()

    # ---- route 1's derived wrap-continue mode.
    derived = 0
    for (ka, kb) in pairs:
        for one, other in ((ka, kb), (kb, ka)):
            ra = records[one]
            rb = records[other]
            if ra["modes"]:
                continue
            if not rb["modes"]:
                continue
            for m in rb["modes"]:
                if m["detection"] != "branch-to-response":
                    continue
                if not OVERFLOW_WORDS.search(str(m["condition"])):
                    continue
                already = False
                for got in ra["modes"]:
                    if got["condition"] == m["condition"]:
                        already = True
                if already:
                    continue
                ra["modes"].append(named(dict(
                    condition=m["condition"],
                    lifted=m["lifted"],
                    response="wrap-continue",
                    detection="branch-to-response",
                    read_from=dict(lang=rb["lang"], n=rb["n"],
                                   operator=rb["operator"]),
                    note="this unit carries no branch to a response, and "
                         "a unit machine-form evidence connects it to "
                         "guards on this condition; the condition is read "
                         "from that unit's own lifted guard and never "
                         "from this one",
                )))
                derived += 1

    # ---- route 2.
    asked = 0
    localized = 0
    skipped_float = 0
    notes = Counter()
    if run_solver:
        todo = []
        for (ka, kb) in sorted(pairs):
            ra = records[ka]
            rb = records[kb]
            if ra["core"] == rb["core"]:
                continue
            if float_operands(ra) or float_operands(rb):
                # THE SCOPE LIMIT OF ROUTE 2, and why it is one.
                # Every template is an INTEGER predicate: a threshold, a
                # sign test, an equality with a small constant.  Asked
                # about an operand that is an IEEE bit pattern, `in1 >=
                # 32 (unsigned)` names an interval of bit patterns and
                # not an interval of numbers, so an accepted region
                # would read as a statement about the value when it is
                # a statement about the encoding.  Measured beside
                # that: a floating-point pair spends the whole wall
                # budget and answers nothing.  So these pairs are not
                # asked, and the skip is RECORDED on both units.
                skipped_float += 1
                note = ("route 2 was not run on this pair: an operand is "
                        "floating point, and every predicate template "
                        "here is an integer predicate, so an accepted "
                        "region would be a statement about the bit "
                        "pattern and not about the number.  The "
                        "difference stays a core difference.")
                ra["solver_notes"].append(note)
                rb["solver_notes"].append(note)
                continue
            todo.append((ka, kb))
        cache = load_cache()
        print("core-differing connected pairs to ask: %d (cached %d)"
              % (len(todo), len(cache)))
        sys.stdout.flush()
        for i, (ka, kb) in enumerate(todo):
            ra = records[ka]
            rb = records[kb]
            ck = cache_key(by_id[ka], by_id[kb])
            if ck in cache:
                got = cache[ck]
                mode = got.get("mode")
                why = got.get("why")
                back = got.get("back")
                bwhy = got.get("back_why")
            else:
                if budget_s and time.time() - started > budget_s:
                    save_cache(cache)
                    print("budget spent; %d pairs cached, run again to "
                          "continue" % len(cache))
                    return 3
                mode, why = localize(by_id[ka], by_id[kb])
                back = None
                bwhy = None
                if mode is not None:
                    back, bwhy = mirror(by_id[kb], by_id[ka], mode)
                cache[ck] = dict(mode=mode, why=why, back=back,
                                 back_why=bwhy)
            asked += 1
            if mode is not None:
                localized += 1
                a_mode = named(dict(mode))
                a_mode["contrast"] = dict(lang=rb["lang"], n=rb["n"],
                                          operator=rb["operator"])
                ra["modes"].append(a_mode)
                if back is not None:
                    back = dict(back)
                    back["contrast"] = dict(lang=ra["lang"], n=ra["n"],
                                            operator=ra["operator"])
                    rb["modes"].append(named(back))
                else:
                    rb["solver_notes"].append(bwhy)
            else:
                notes[str(why)[:110]] += 1
                ra["solver_notes"].append(why)
                rb["solver_notes"].append(why)
            if (i + 1) % 100 == 0:
                save_cache(cache)
                print("[progress] %d/%d asked, %d localized, %ds"
                      % (i + 1, len(todo), localized,
                         int(time.time() - started)))
                sys.stdout.flush()
        save_cache(cache)

    # ---- write.
    by_lang = {}
    for (lang, n), rec in records.items():
        by_lang.setdefault(lang, {})[n] = rec

    counts = Counter()
    responses = Counter()
    for rec in records.values():
        if rec["modes"]:
            counts["units_with_modes"] += 1
        else:
            counts["units_with_no_mode"] += 1
        for m in rec["modes"]:
            head = m["response"].split(":")[0]
            responses[head] += 1
            counts["modes"] += 1
    for name in ("wrapping", "growing", "approximating"):
        responses.setdefault("name:" + name, 0)
    named_count = Counter()
    for rec in records.values():
        for m in rec["modes"]:
            if m.get("mode_name"):
                named_count[m["mode_name"]] += 1
    for name in ("wrapping", "growing", "approximating"):
        if name not in named_count:
            named_count[name] = 0

    for lang, us in sorted(by_lang.items()):
        doc = dict(
            language=lang,
            shape="every accepted ship unit as a core and a list of modes",
            core_note="the normal-path lifted form: verdicts.core_values "
                      "over the blocks that are not trap/panic response "
                      "blocks.  UNVERIFIED that every such block reaches "
                      "`ret` -- in this corpus each one does, which is an "
                      "observation over these units and not a proof.",
            detection_routes=["branch-to-response", "solver-localized"],
            predicate_templates=[
                "T1 unsigned threshold on one input: in_i >=u k, "
                "k in (8, 16, 32, 64)",
                "T2 sign test on one input: in_i <s 0",
                "T3 equality with a constant: in_i == c, "
                "c in (0, 1, -1, -2147483648, -9223372036854775808)"],
            budget="at most %d solver queries per pair, %d ms each, at "
                   "most %d seconds of wall clock per pair; when the "
                   "budget is spent with nothing accepted no mode is "
                   "claimed and the difference stays a core difference"
                   % (QUERIES_PER_PAIR, SOLVER_CAP_MS, SECONDS_PER_PAIR),
            solver_scope="route 2 is not asked about a pair whose "
                         "operands are IEEE floats: every template is an "
                         "integer predicate, so an accepted region would "
                         "be a statement about the bit pattern and not "
                         "about the number.  Such a pair keeps a core "
                         "difference and each unit records the skip.",
            vocabulary=VOCABULARY_NOTE,
            spelling="the operator token appears once per unit, as the "
                     "display label `operator` beside `lang` and `n`.  "
                     "No key, grouping or selection uses it.",
            solver_run=run_solver,
            units=us,
            z3=z3.get_version_string(),
            lifter=AS.LIFTER_ID,
        )
        path = os.path.join(HERE, "core_modes_%s.json" % lang)
        json.dump(doc, open(path, "w"), indent=1)
        print("wrote %s (%d units)" % (os.path.basename(path), len(us)))

    print()
    print("== core+modes")
    print("   units                      %d" % len(records))
    print("   units with 0 modes         %d" % counts["units_with_no_mode"])
    print("   units with 1+ modes        %d" % counts["units_with_modes"])
    print("   modes total                %d" % counts["modes"])
    for head, count in sorted(responses.items()):
        if head.startswith("name:"):
            continue
        print("   response %-22s %d" % (head, count))
    for name, count in sorted(named_count.items()):
        print("   mode name %-21s %d" % (name, count))
    print("   derived wrap-continue      %d" % derived)
    print("   solver pairs asked         %d" % asked)
    print("   solver pairs skipped (fp)  %d" % skipped_float)
    print("   solver pairs localized     %d" % localized)
    for why, count in notes.most_common(8):
        print("     %4d  %s" % (count, why))
    print("   wall seconds               %d" % int(time.time() - started))
    print("   excluded units             %s" % dict(excluded))
    return 0


def mirror(unit, other, mode):
    """the same mode from the other unit's side: the region is the same
    predicate, the response is what THAT unit does inside it."""
    pairs, env, convention, why = build_claims(unit, other)
    if pairs is None:
        return None, why
    vars_ = anchored_vars(env)
    P = None
    for words, formula in templates(vars_):
        if words == mode["condition"]:
            P = formula
            break
    if P is None:
        return None, ("the region predicate could not be restated over "
                      "this unit's own variables")
    budget = Budget()
    response, rwhy = region_response(budget, pairs, P)
    if convention:
        rwhy = rwhy + "; the claim is about the ABI's result register " \
                      "only (result_register_by_convention: UNVERIFIED)"
    return dict(
        condition=mode["condition"],
        lifted="(solver-localized; no branch carries this condition)",
        response=response,
        detection="solver-localized",
        response_ground=rwhy,
        solver_queries=budget.queries,
    ), None


if __name__ == "__main__":
    sys.exit(main())
