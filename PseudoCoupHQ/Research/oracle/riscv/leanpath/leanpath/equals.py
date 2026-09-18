"""LeanExpr.equals -- are a unit's certified meaning and a definition's pure
form the same function of their unknowns, in the plan's order.

Plan leaves hq.research.lean_proof_path_resistant_to_churn.lean_expr.{equals,normalize_integer_level,
decide_fixed_width} (log 274 §4, §5.3):

  1. the same text            `rfl`: the two pure forms are one term.
  2. the integer level        `simp only [the pure forms]` then `grind`:
                              Lean's own algebra over Int and BitVec, no
                              circuit. This is where log 273's multiply-high
                              wall is expected to fall (log 274 §5.3).
  3. fixed width              `simp only [the pure forms, the Sail helpers]`
                              then `bv_decide`: bit-blast to a circuit with
                              a budget. Sail's Int-level helpers must have
                              been rewritten to BitVec operations for this
                              to apply (the widening leaf; here only what
                              `simp` already knows).
  4. undecided                the stage reached is the row.

The definition side: for a clause with an enumerated operation parameter
(rop, mul_op, ...), every value of that parameter is a candidate, and the
row records which candidate proved. Nothing is keyed by a name: the
candidate set is the clause's parameter type, enumerated.
"""
import json
import os
import re
import time

from .walk import lean_run
from .strip import emitted_defs, reachable, library_refs

STAGES = [
    ("same_text", ["  with_reducible rfl"]),
    # `all_goals`: when the unfolding alone closes the goal (`a &&& b = a &&& b` after `pure_RTYPE` opens),
    # a bare `grind`/`bv_decide` fails with "no goals" and the proof is lost; on zero goals `all_goals` succeeds
    ("integer_level", ["  try simp only [%(defs)s]", "  all_goals grind"]),
    ("fixed_width", ["  try simp only [%(defs)s]", "  all_goals bv_decide"]),
]


# ---------------------------------------------------------------- core level
# Unfolding the emitted definitions and the lean-sail helpers is not the whole
# rule. Under both of those sits LEAN'S OWN library, and three of its terms are
# outside `bv_decide`'s BitVec fragment in the spelling the emit produces. Each
# entry here is (the term that calls for it, the lemmas that answer it).
#
# NOT A GUESS LIST. Every name was put to the toolchain on its own `#check`
# line first, and every lemma was then put to `bv_decide` one at a time against
# the shape the gate's own residuals named (lane lp3_l101, and on the host at
# v4.30.0 and v4.34.0 before it). A name that is merely plausible is worse here
# than no name at all: `try simp only [...]` SWALLOWS the elaboration error of
# an unknown identifier -- measured, not assumed -- and then skips the ENTIRE
# simp set, so one bad name leaves every definition folded and `bv_decide`
# answers with a spurious counterexample that reads exactly like hard
# mathematics. `equals` guards against that by emitting a `#check` for each
# lemma it injects, which fails loudly instead.
#
#   BitVec.zero n     `zeros` (Prelude) is `BitVec.zero n`, and `bv_decide`
#                     abstracts it. `BitVec.zero_eq` rewrites it to `0#n`.
#   an Int-derived    Sail's shift helpers hand `BitVec.sshiftRight` a Nat
#   shift             coerced out of an Int. `bv_decide` takes the shift when
#                     it is a plain `BitVec.toNat`, and abstracts the whole
#                     shift when the Int round-trip is still in the term;
#                     `Int.toNat_natCast` removes the round-trip.
#   an Int comparison Sail's unsigned comparisons leave a decidable `<` over
#                     two Ints. The bridge must go TOWARDS BitVec, never away:
#                     unfolding `BitVec.ult` into Nat breaks goals `bv_decide`
#                     proves natively (measured), while `Int.ofNat_lt` then
#                     `← BitVec.lt_def` then `BitVec.ult_iff_lt` puts the
#                     comparison back inside the fragment and harms nothing.
CORE_NORMALISE = (
    ("BitVec.zero", ("BitVec.zero_eq",)),
    ("sshiftRight", ("Int.toNat_natCast",)),
    ("toNatInt", ("Int.ofNat_lt", "← BitVec.lt_def", "BitVec.ult_iff_lt")),
)


def core_normalise(texts):
    """The Lean-core lemmas the given texts call for, by the rule above.

    Nothing is added unconditionally: a lemma rides only when the term it
    answers actually occurs in the closure being unfolded, so a theorem that
    never leaves the BitVec fragment carries none of them."""
    joined = "\n".join(t for t in texts if t)
    out = []
    for term, lemmas in CORE_NORMALISE:
        # whole token, not substring: `Sail.BitVec.zeroExtend` contains the
        # letters of `BitVec.zero` and is a different function entirely
        if re.search(r"\b%s\b" % re.escape(term), joined):
            out += [lm for lm in lemmas if lm not in out]
    return out


# --------------------------------------------------------- the Sail bridge --
# Layer four, and it is not a library lemma: Sail's Lean backend defines every
# comparison over Int (`zopz0zI_u x y = toNatInt x <b toNatInt y`), `bv_decide`
# cannot bitblast `Int.blt`, and Sail ships NO lemma to `BitVec.ult` -- which
# is the same predicate, inside the fragment. Lane lp3_l104 measured that no
# library lemma closes it; lp3_l105 sized it at 35 of 186 classes UNDECIDED.
#
# `leanpath/sail_bridge.py` GENERATES the lemmas by reading each definition out
# of the Prelude, and lane lp3_l107 put all eight to Lean: the four signed ones
# hold by `rfl` (they are definitionally the BitVec predicate) and the four
# unsigned by `simp`. They are emitted INTO the theorem file rather than
# imported, so a file carries its own proof of every rewrite it uses.
_BRIDGE_CACHE = {}


def bridge_lemmas(project, module):
    """(lemma text lines, the names they define) for this project's Prelude.

    Generated, never typed: a definition whose shape sail_bridge does not
    recognise is skipped there and simply has no lemma here, so a rename in
    Sail becomes a missing rewrite and never a wrong one."""
    key = (project, module)
    if key in _BRIDGE_CACHE:
        return _BRIDGE_CACHE[key]
    try:
        from .sail_bridge import (read_defs, lemma_for,
                                  read_bool_defs, bool_lemma_for)
        prelude = os.path.join(project, module, "Prelude.lean")
        text = open(prelude).read()
    except Exception:
        _BRIDGE_CACHE[key] = ([], [])
        return _BRIDGE_CACHE[key]
    lines, names = [], []
    # two families: the comparisons, and the Bool-to-bit wrapper around them.
    # lane lp3_l109 moved two classes with the comparisons alone and its
    # residuals named the wrapper as what stayed opaque, so both ride.
    found = [(n, b, y, lemma_for) for n, b, y in read_defs(text)]
    found += [(n, b, y, bool_lemma_for) for n, b, y in read_bool_defs(text)]
    for name, binder, body, maker in found:
        got, _why = maker(name, binder, body)
        if got is None:
            continue
        lemma, meta = got
        lines += lemma.split("\n") + [""]
        names.append(("sail_bridge_" + name, meta["definition"]))
    _BRIDGE_CACHE[key] = (lines, names)
    return _BRIDGE_CACHE[key]


def bridge_for(project, module, texts):
    """(lemma text, the lemma names, the definitions that must be DROPPED).

    A lemma rides only when the Sail definition it bridges occurs in the
    closure being unfolded, exactly as core_normalise does it.

    THE THIRD RETURN IS NOT OPTIONAL. A simp set cannot both UNFOLD a
    definition and REWRITE it: `simp only [zopz0zI_s, sail_bridge_zopz0zI_s]`
    unfolds first, and the bridge then has nothing left to match. Lane
    lp3_l108 ran exactly that and moved nothing -- every residual showed the
    comparison already spelled `(...).toInt <b (...).toInt`, which is the
    unfolded form. The definition a bridge covers must leave the set with it,
    which is why this returns them together and the caller is given no way to
    take one without the other."""
    lines, names = bridge_lemmas(project, module)
    joined = "\n".join(t for t in texts if t)
    wanted = [n for n, defined in names
              if re.search(r"\b%s\b" % re.escape(defined), joined)]
    bridged = {n: d for n, d in names}
    drop = [bridged[n] for n in wanted]
    if not wanted:
        return [], [], []
    keep, emit = set(wanted), []
    block = []
    for line in lines:
        block.append(line)
        if line == "":
            head = "\n".join(block)
            m = re.search(r"^theorem (sail_bridge_\w+)", head, re.M)
            if m and m.group(1) in keep:
                emit += block
            block = []
    return emit, wanted, drop


def core_guards(defs):
    """The injected core lemmas, as bare names, for the `#check` guard."""
    named = {lm for _, lemmas in CORE_NORMALISE for lm in lemmas}
    return [d.replace("←", "").strip() for d in defs if d in named]


def simp_set(defs_index, heads, name, bodies, F, G):
    """Every definition `simp only` must unfold for one theorem, in order.

    ONE place, deliberately. This was three copies -- two here and a third in
    a lane's heredoc -- and on 2026-09-16 a fix landed in one of them while the
    gate ran another, so the run reported UNDECIDED against code that had not
    changed. A caller that assembles its own set will drift the same way.

    Seeded from the pure bodies AND from the theorem STATEMENT. The statement
    names helpers no body mentions: a candidate carries constants in its
    operand list (`pure_ZBA_RTYPEUW a zero_reg 0b00#2`), and `zero_reg` is an
    emitted definition nothing else would reach. Without it `bv_decide`
    abstracts the constant as an opaque variable and answers with a spurious
    counterexample.

    Three layers, in this order: the emitted definitions the text reaches, the
    lean-sail helpers those call, and Lean's own normalisations for whatever
    the first two leave outside `bv_decide`'s fragment. The third layer is read
    off the TEXT OF THE UNFOLDED CLOSURE, not off the statement: `BitVec.zero`
    is never written by the emit at the call site -- it is the body of `zeros`,
    which is the body of `zero_reg`, which is what the statement carries.
    """
    # A `pure_` name rides only if the bodies handed in actually DEFINE it.
    # The rule used to take every head and the name on faith, which is safe for
    # the corpus driver (its `name` is a clause) and a trap for any caller whose
    # `name` is a unit tag or whose head was refused a body: the definition does
    # not exist, `simp only` cannot elaborate the list, `try` eats the error
    # without a word, and the WHOLE set -- every emitted definition, every
    # library helper -- is skipped. The run then reports UNDECIDED for a
    # spelling. Measured on this toolchain as candidate u0 of lane lp3_l101.
    body_text = "\n".join(bodies)
    defined = lambda nm: re.search(r"^def pure_%s\b" % re.escape(nm), body_text, re.M) is not None
    defs = []
    for nm in list(heads) + [name]:
        if defined(nm) and ("pure_%s" % nm) not in defs:
            defs.append("pure_%s" % nm)
    pure_text = "\n".join(re.findall(r"^def pure_.*?(?=^theorem|\Z)", body_text, re.S | re.M))
    seed = "\n".join([pure_text, F, G])
    defs += [d for d in reachable(defs_index, seed) if d not in defs]
    defs += [d for d in library_refs(defs_index, defs, extra_texts=[seed]) if d not in defs]
    closure = [seed] + [defs_index.get(d, "") for d in defs]
    defs += [d for d in core_normalise(closure) if d not in defs]
    return defs

def simp_set_with_bridge(defs_index, heads, name, bodies, F, G,
                        project, module):
    """(the simp set, the lemma text to emit) -- `simp_set` plus the bridge.

    ONE PLACE, and it exists because getting the bridge right by hand is two
    mistakes deep. Lane lp3_l108 added the bridge lemmas and left the Sail
    definitions in the set: simp unfolded first and nothing moved. Lane
    lp3_l109 dropped the definitions and moved two of thirty-five. Lane
    lp3_l110 added the second family -- the Bool-to-bit wrapper around the
    comparison -- and moved thirty-one.

    A caller that assembles this itself will get one of those three, and two
    of them look like hard mathematics. So the drop and the emit come back
    together from here or not at all."""
    defs = simp_set(defs_index, heads, name, bodies, F, G)
    closure = [F, G] + list(bodies) + [defs_index.get(d, "") for d in defs]
    emit, names, drop = bridge_for(project, module, closure)
    if not names:
        return defs, []
    dropped = set(drop)
    defs = [d for d in defs if d not in dropped] + names
    return defs, emit


def theorem_text(name, unknowns, lhs, rhs, stage, defs):
    unk = " ".join("(%s : BitVec 64)" % v for v in unknowns)
    # the same text is instant when it holds; a cap keeps `rfl` from unfolding a composite for minutes
    caps = {"same_text": 10000, "integer_level": 40000}      # `grind` on a false goal must fail in a second, not twenty
    body = (["set_option maxHeartbeats %d in" % caps[stage]] if stage in caps else []) + ["theorem %s_%s %s :" % (name, stage, unk),
            "    (%s) = (%s) := by" % (lhs, rhs)]
    for ln in STAGES[[s for s, _ in STAGES].index(stage)][1]:
        body.append(ln % {"defs": ", ".join(defs)})
    return "\n".join(body)


def equals(proof_project, header, closers, bodies, name, unknowns, lhs, rhs, defs, out_dir, timeout_s=120, stages=None):
    """Try the stages in order; return the first that proves, with times."""
    tried = []
    # The guard for the churn this path has already been bitten by. A lemma
    # name that no longer exists does NOT announce itself inside
    # `try simp only [...]`: the `try` eats the elaboration error, the whole
    # set is skipped, and the run reports UNDECIDED for a vanished name. One
    # `#check` per injected core lemma turns that into an error on its own
    # line, which `rc` and `errors` below both carry.
    guard = ["#check @%s" % g for g in core_guards(defs)]
    for stage, _ in STAGES:
        if stages is not None and stage not in stages:
            continue
        text = "\n".join(header + ["set_option linter.unusedVariables false", ""] + guard + [""] + bodies +
                         ["", theorem_text(name, unknowns, lhs, rhs, stage, defs), ""] + closers + [""])
        path = os.path.join(out_dir, "Equals_%s_%s.lean" % (name, stage))
        open(path, "w").write(text)
        rc, secs, out = lean_run(proof_project, path, timeout_s)
        errs = [ln for ln in out.split("\n") if "error" in ln][:4]
        tried.append({"stage": stage, "rc": rc, "seconds": round(secs, 1), "errors": errs, "lean_file": path})
        if rc == 0:
            return {"verdict": "PROVED", "stage": stage, "tried": tried}
    return {"verdict": "UNDECIDED", "stage": "none", "tried": tried}


def equals_batch(proof_project, header, closers, bodies, unit_tag, unknowns, lhs, cands_G_defs, out_dir, stage, idx, timeout_s=120):
    """One stage over a subset of candidates in ONE Lean run: a theorem per
    candidate; Lean reports every failing theorem and stays silent on the
    proved ones; the errors are read back by line. Returns {k: proved?}
    for k in idx, or None on a timeout of the whole file."""
    lines = header + ["set_option linter.unusedVariables false", ""] + bodies + [""]
    spans = []
    count = lambda: sum(x.count("\n") + 1 for x in lines)     # items may hold several lines
    for k in idx:
        G, defs = cands_G_defs[k]
        start = count() + 1
        lines += theorem_text("%s_%02d" % (unit_tag, k), unknowns, lhs, G, stage, defs).split("\n") + [""]
        spans.append((k, start, count()))
    lines += closers + [""]
    tag = "%s_%s_%02d_%02d" % (unit_tag, stage, idx[0], idx[-1]) if idx else unit_tag
    path = os.path.join(out_dir, "Equals_%s.lean" % tag)
    open(path, "w").write("\n".join(lines))
    rc, secs, out = lean_run(proof_project, path, timeout_s)
    if rc == -1:
        return None, secs, path
    bad = set()
    for m in re.finditer(r"^[^\n]*?:(\d+):\d+: error", out, re.M):
        ln = int(m.group(1))
        for k, a, b in spans:
            if a <= ln <= b:
                bad.add(k)
    return {k: (k not in bad) for k in idx}, secs, path


SAMPLES = [("0x0123456789abcdef#64", "0xfedcba9876543210#64"), ("0xffffffffffffffff#64", "0x1#64"),
           ("0x8000000000000000#64", "0x7fffffffffffffff#64"), ("0x5#64", "0x3#64")]


def evaluate_batch(proof_project, header, closers, bodies, unit_tag, unknowns, lhs, Gs, out_dir, timeout_s=120):
    """Test before proving: one Lean run evaluates the proposal and every
    candidate on the sample inputs (one `#eval` per sample over a list, so
    the interpreter compiles once per sample); a candidate that differs
    anywhere is refuted by evaluation and never sent to a prover. Returns
    the surviving candidate indices, or None if the emit cannot be evaluated."""
    lam = lambda body: "(fun %s => (%s))" % (" ".join("(%s : BitVec 64)" % v for v in unknowns), body)
    args = lambda s: " ".join("(%s)" % s[i] for i in range(len(unknowns)))
    lines = header + [""] + bodies + [""]
    for j, s in enumerate(SAMPLES):
        items = ", ".join("%s %s" % (lam(body), args(s)) for body in [lhs] + list(Gs))
        # a plain string of the values, never a `Format` (which wraps a long list over several lines)
        lines.append('#eval IO.println s!"E {%d} [{String.intercalate ", " (([%s] : List (BitVec 64)).map (fun x => toString x.toNat))}]"' % (j, items))
    lines += closers + [""]
    path = os.path.join(out_dir, "Eval_%s.lean" % unit_tag)
    open(path, "w").write("\n".join(lines))
    rc, secs, out = lean_run(proof_project, path, timeout_s)
    rows = {}
    for m in re.finditer(r"^E (\d+) \[(.*)\]\s*$", out, re.M):
        rows[int(m.group(1))] = [x.strip() for x in m.group(2).split(",")]
    if rc != 0 or any(j not in rows or len(rows[j]) != len(Gs) + 1 for j in range(len(SAMPLES))):
        why = [ln for ln in out.split("\n") if "error" in ln][:1] or ["rc=%d, %d sample rows parsed" % (rc, len(rows))]
        return None, secs, path + " | " + why[0][-160:]
    survivors = [k for k in range(len(Gs)) if all(rows[j][k + 1] == rows[j][0] for j in range(len(SAMPLES)))]
    return survivors, secs, path


# ------------------------------------------------------------- candidates
def enum_values(lean_dir, type_name):
    """Every value of an emitted enumerated type, as Lean terms; a structure
    of enumerated fields gives the product. None if the type is not one."""
    if type_name == "Bool":
        return ["false", "true"]
    t = open(os.path.join(lean_dir, "Defs.lean")).read()
    m = re.search(r"^inductive %s(?:\s*:\s*Type)?\s+where(.*?)(?=^\s*deriving|^\S)" % re.escape(type_name), t, re.S | re.M)
    if m:
        ctors = [x.strip().split()[0] for x in m.group(1).split("|") if x.strip() and re.match(r"^[A-Za-z_]\w*(\s|$)", x.strip())]
        if all(len(x.strip().split()) == 1 for x in m.group(1).split("|") if x.strip()):
            return ["%s.%s" % (type_name, c) for c in ctors]
        return None
    m = re.search(r"^structure %s where(.*?)(?=^\s*deriving|^\S)" % re.escape(type_name), t, re.S | re.M)
    if m:
        fields = re.findall(r"^\s+(\w+)\s*:\s*(\w+)", m.group(1), re.M)
        options = []
        for fname, ftype in fields:
            vals = enum_values(lean_dir, ftype)
            if vals is None:
                return None
            options.append([(fname, v) for v in vals])
        import itertools
        return ["{ " + ", ".join("%s := %s" % (f, v) for f, v in combo) + " }" for combo in itertools.product(*options)]
    return None


def candidates_for(unit_row, strip_rows, lean_dir, arity):
    """The definition side: every certified straight clause whose pure form
    reads `arity` registers and whose other parameters are enumerated types,
    each value of each parameter. Nothing is chosen by a name."""
    out = []
    for name, r in strip_rows.items():
        if r.get("verdict") != "CERTIFIED" or r.get("shape") != "straight":
            continue
        if len(r.get("reads", [])) != arity:
            continue
        others = [(n, t) for n, t in r["params"] if t != "regidx"]
        combos = [[]]
        ok = True
        for n, t in others:
            vals = enum_values(lean_dir, t.strip("() "))
            if vals is None:
                ok = False
                break
            combos = [c + [v] for c in combos for v in vals]
        if not ok:
            continue
        for combo in combos:
            out.append((name, combo))
    return out


def cmd_equals(argv, say, write_json, check_memory):
    """python3 -m leanpath equals <proof project> <lib> <strip.json> <walk.json> <out dir> [budget_s] [max candidates per unit]"""
    from . import strip as ST
    from .walk import ABI_ARGS
    proof_project, lib, strip_json, walk_json, out_dir = argv[:5]
    budget_s = int(argv[5]) if len(argv) > 5 else 120
    max_cand = int(argv[6]) if len(argv) > 6 else 64
    every = os.environ.get("EQUALS_ALL") == "1"
    unit_budget_s = int(os.environ.get("EQUALS_UNIT_BUDGET_S", "150"))   # a resource bound per unit, not a selection
    jobs = int(os.environ.get("EQUALS_JOBS", "2"))
    from concurrent.futures import ThreadPoolExecutor
    pool = ThreadPoolExecutor(max_workers=jobs)
    os.makedirs(out_dir, exist_ok=True)
    lean_dir = os.path.join(proof_project, lib)
    header, closers = ST.header_of(lean_dir, lib)
    clauses = {c["name"][len("execute_"):]: c for c in ST.clauses_of(lean_dir)}
    defs_index = emitted_defs(lean_dir)
    lib_index = ST.library_index(proof_project)
    say("  emitted definitions scanned: %d; lean-sail definitions indexed: %d" % (len(defs_index), len(lib_index)))
    strip_rows = {r["clause"][len("execute_"):]: r for r in json.load(open(strip_json))["rows"]}
    walk = json.load(open(walk_json))
    rows = []
    for u in walk["rows"]:
        if u.get("verdict") != "CERTIFIED":
            continue
        F = u["proposal"]
        unknowns = [ABI_ARGS[k] for k in sorted(ABI_ARGS) if re.search(r"\b%s\b" % ABI_ARGS[k], F)]
        arity = len(unknowns)
        heads = set(re.findall(r"pure_(\w+)", F))
        cands = candidates_for(u, strip_rows, lean_dir, arity)
        # the clauses the unit itself walked come first, and among them the candidate whose text is the
        # proposal's own (the library prefix aside): its own instructions must prove by the same text
        norm = lambda s: re.sub(r"\b%s\." % re.escape(lib), "", re.sub(r"\s+", " ", s))
        G_of = lambda c: "pure_%s %s %s" % (c[0], " ".join("(%s)" % v for v in unknowns), " ".join("(%s)" % v for v in c[1]))
        cands.sort(key=lambda c: (c[0] not in heads, norm(G_of(c)) != norm(F), c[0]))
        cands = cands[:max_cand]
        say("  %-44s F over %s; %d candidates" % (u["unit"], unknowns, len(cands)))
        results = {}
        t_unit = time.time()
        def run_one(k, name, combo, stages):
            cl = clauses[name]
            bodies = ST.lean_body(cl, ST.propose(cl))
            for h in heads:
                if h != name and h in clauses:
                    bodies += ST.lean_body(clauses[h], ST.propose(clauses[h]))
            G = G_of((name, combo))
            tag = re.sub(r"\W", "_", "%s__%s_%02d" % (u["unit"], name, k))[:120]
            defs = simp_set(defs_index, heads, name, bodies, F, G)
            return k, equals(proof_project, header, closers, bodies, tag, unknowns, F, G, defs, out_dir, budget_s, stages)
        found = False
        # round 1, one Lean run: the same text and the integer level over every candidate
        prepared = []
        for k, (name, combo) in enumerate(cands):
            cl = clauses[name]
            bodies = ST.lean_body(cl, ST.propose(cl))
            G = G_of((name, combo))
            defs = simp_set(defs_index, heads, name, bodies, F, G)
            prepared.append((name, bodies, G, defs))
        shared, seen_clauses = [], set()
        for h in list(heads) + [nm for nm, _, _, _ in prepared]:
            if h in clauses and h not in seen_clauses:
                seen_clauses.add(h)
                shared += ST.lean_body(clauses[h], ST.propose(clauses[h]))
        utag = re.sub(r"\W", "_", u["unit"])[:100]
        GD = [(G, defs) for _, _, G, defs in prepared]
        for k, (name, combo) in enumerate(cands):
            results[k] = {"definition": name, "operation": combo, "verdict": "UNDECIDED", "stage": "none", "seconds": 0, "tried": []}
        live = list(range(len(cands)))
        eval_first = os.environ.get("EQUALS_EVAL_FIRST") == "1"     # a big composite: evaluate before any prover sees 52 copies of it
        if eval_first:
            surv, secs0, path0 = evaluate_batch(proof_project, header, closers, shared, utag, unknowns, F, [G for G, _ in GD], out_dir, budget_s)
            if surv is None:
                say("      evaluation: the emit did not evaluate (%.1fs); every candidate goes to the provers; %s" % (secs0, path0.split(" | ")[-1]))
            else:
                say("      evaluation over %d candidates on %d samples, one Lean run: %.1fs; %d survive" % (len(cands), len(SAMPLES), secs0, len(surv)))
                for k in range(len(cands)):
                    if k not in surv:
                        results[k].update({"verdict": "REFUTED_BY_EVALUATION", "stage": "evaluation", "tried": [{"stage": "evaluation", "rc": 1, "seconds": round(secs0 / len(cands), 2), "errors": [], "lean_file": path0}]})
                live = surv
        if not live:
            got, secs1, path1 = {}, 0.0, ""
        else:
            got, secs1, path1 = equals_batch(proof_project, header, closers, shared, utag, unknowns, F, GD, out_dir, "same_text", live, budget_s)
        if live:
            say("      %-14s over %2d candidates, one Lean run: %.1fs%s" % ("same_text", len(live), secs1, "" if got else "; TIMEOUT"))
        for k in live:
            r = results[k]
            ok = bool(got and got[k])
            r["tried"].append({"stage": "same_text", "rc": (-1 if got is None else (0 if ok else 1)), "seconds": round(secs1 / len(live), 2), "errors": ([] if got else ["TIMEOUT"]), "lean_file": path1, "batched": True})
            r["seconds"] = round(sum(x["seconds"] for x in r["tried"]), 1)
            if ok and r["verdict"] != "PROVED":
                r["verdict"], r["stage"] = "PROVED", "same_text"
                if not found:
                    say("      %-14s %-40s %-9s %s" % (r["definition"], " ".join(r["operation"])[:40], "PROVED", "same_text"))
                found = found or not every
        if not found and not eval_first and os.environ.get("EQUALS_NO_EVAL") != "1":
            surv, secs0, path0 = evaluate_batch(proof_project, header, closers, shared, utag, unknowns, F, [G for G, _ in GD], out_dir, budget_s)
            if surv is None:
                say("      evaluation: the emit did not evaluate (%.1fs); every candidate goes to the provers; %s" % (secs0, path0.split(" | ")[-1]))
            else:
                say("      evaluation over %d candidates on %d samples, one Lean run: %.1fs; %d survive" % (len(cands), len(SAMPLES), secs0, len(surv)))
                for k in range(len(cands)):
                    if k not in surv:
                        results[k].update({"verdict": "REFUTED_BY_EVALUATION", "stage": "evaluation", "tried": [{"stage": "evaluation", "rc": 1, "seconds": round(secs0 / len(cands), 2), "errors": [], "lean_file": path0}]})
                live = surv
        own = [k for k, (nm, _) in enumerate(cands) if nm in heads and k in live]
        rest = [k for k in live if k not in own]
        # the batched rounds: the same text over every candidate; the integer level over the unit's own
        # clauses, then over the rest; each one Lean run, within the unit's budget
        chunk = int(os.environ.get("EQUALS_CHUNK", "12"))     # candidates per Lean run: a run must not outlive the budget
        # the plan, within the unit's budget: the same text over every candidate (one run); the integer level
        # over the unit's own clauses (runs of `chunk`); the fixed width over the own clauses (a run each,
        # pooled); then the integer level and the fixed width over the rest
        plan = [("integer_level", own[i:i + chunk]) for i in range(0, len(own), chunk)]
        plan += [("fixed_width", own[i:i + jobs]) for i in range(0, len(own), jobs)]
        plan += [("integer_level", rest[i:i + chunk]) for i in range(0, len(rest), chunk)]
        plan += [("fixed_width", rest[i:i + jobs]) for i in range(0, len(rest), jobs)]
        for stage, idx in plan:
            if found or not idx or time.time() - t_unit > unit_budget_s:
                continue
            if stage == "fixed_width":
                batch = [(k, cands[k][0], cands[k][1]) for k in idx]
                for k, res in pool.map(lambda x: run_one(x[0], x[1], x[2], ["fixed_width"]), batch):
                    r = results[k]
                    r["tried"] += res["tried"]
                    r["seconds"] = round(sum(x["seconds"] for x in r["tried"]), 1)
                    if res["verdict"] == "PROVED":
                        r["verdict"], r["stage"] = "PROVED", res["stage"]
                        found = found or not every
                    say("      %-14s %-40s %-9s %s %.1fs" % (r["definition"], " ".join(r["operation"])[:40], res["verdict"], res["stage"], r["seconds"]))
                continue
            got, secs1, path1 = equals_batch(proof_project, header, closers, shared, utag, unknowns, F, GD, out_dir, stage, idx, budget_s)
            say("      %-14s over %2d candidates, one Lean run: %.1fs%s" % (stage, len(idx), secs1, "" if got else "; TIMEOUT"))
            for k in idx:
                r = results[k]
                ok = bool(got and got[k])
                r["tried"].append({"stage": stage, "rc": (-1 if got is None else (0 if ok else 1)), "seconds": round(secs1 / len(idx), 2), "errors": ([] if got else ["TIMEOUT"]), "lean_file": path1, "batched": True})
                r["seconds"] = round(sum(x["seconds"] for x in r["tried"]), 1)
                if ok and r["verdict"] != "PROVED":
                    r["verdict"], r["stage"] = "PROVED", stage
                    if not found:
                        say("      %-14s %-40s %-9s %s" % (r["definition"], " ".join(r["operation"])[:40], "PROVED", stage))
                    found = found or not every
        for k in results:
            if not results[k]["tried"]:
                results[k].update({"verdict": "NOT_TRIED", "stage": "the unit's budget of %ds, or a proof found first" % unit_budget_s})
        results = [results[k] for k in sorted(results)]
        proved = [r for r in results if r["verdict"] == "PROVED"]
        rows.append({"unit": u["unit"], "cell_display": u.get("cell_display"), "proposal": F, "unknowns": unknowns,
                     "candidates": len(cands), "proved": [(r["definition"], r["operation"], r["stage"]) for r in proved],
                     "results": results})
    summary = {"units": len(rows), "with_a_proved_definition": sum(1 for r in rows if r["proved"]),
               "driver_peak_resident_kB": check_memory("equals end")}
    write_json(os.path.join(out_dir, "equals.json"), {"summary": summary, "rows": rows})
    say("  equals: %d units, %d with a proved definition" % (summary["units"], summary["with_a_proved_definition"]))
    return 0
