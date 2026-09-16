"""operator_for -- System.pass_a_find step 2 (plan node
hq.research.lean_proof_path_resistant_to_churn.language.operator_for):
the swap table of a language, filled by proof and by nothing else.

  python3 -m leanpath operator_for <proof project> <lib> <strip.json> <walk.json[,walk.json...]> <out dir> [budget_s]

The candidates are the subterms of Sail's own definitions: every
certified pure form (the strip) is parsed, its lets inlined, its `match`
over an enumerated parameter split into arms, and every subterm whose
free variables are register reads (no immediate, no enumerated
parameter) becomes a candidate over the ABI unknowns, reads renamed in
order of first occurrence (a, b, ...). Lean types them (one run; a
subterm that is not a 64-bit vector over the unknowns is dropped). Then
for every certified unit of the walk, every candidate of its arity goes
through the same stages as `equals` (evaluation at sample inputs, which
only removes; the same text; the integer level; the fixed width), and
EVERY proved candidate is an entry: operator_for[candidate] += unit.

Nothing here names an operator or an instruction: the candidates come
from the definitions, the units from the corpus, the entries from Lean.
"""
import json
import os
import re
import time

from . import strip as ST
from . import lean_tree as LZ
from .equals import evaluate_batch, equals_batch, enum_values, SAMPLES
from .strip import emitted_defs, reachable, library_refs
from .walk import ABI_ARGS, lean_run

UNKNOWNS = [ABI_ARGS[k] for k in sorted(ABI_ARGS)]      # a b c d
MAX_SETTINGS = int(os.environ.get("OPFOR_MAX_SETTINGS", "64"))     # a resource bound on one clause, not a selection
BOOL_LIT = ("false", "true")
REGISTER_WIDTH = 64                 # the width of a read: a definition's operands are register reads
SLICE = "extractLsb"                # Sail's own name for a slice of a vector; a library function, not an operator


def to_lean(n):
    k = n[0]
    if k == "num":
        return n[1]
    if k == "id":
        return n[1]
    if k == "app":
        return "(%s %s)" % (to_lean(n[1]), " ".join(to_lean(x) for x in n[2]))
    if k == "bin":
        return "(%s %s %s)" % (to_lean(n[2]), n[1], to_lean(n[3]))
    if k == "un":
        return "(%s %s)" % (n[1], to_lean(n[2]))
    if k == "named":
        return "(%s := %s)" % (n[1], to_lean(n[2]))
    if k == "ascribe":
        return "(%s : %s)" % (to_lean(n[1]), n[2])
    if k == "if":
        return "(if %s then %s else %s)" % (to_lean(n[1]), to_lean(n[2]), to_lean(n[3]))
    if k == "match":
        return "(match %s with %s)" % (to_lean(n[1]), " ".join("| .%s => %s" % (c, to_lean(e)) for c, e in n[2]))
    if k == "let":
        return "(%s)" % to_lean(n[2])
    raise ValueError("node %r" % (k,))


def substitute(n, env):
    """let names replaced by their trees"""
    k = n[0]
    if k == "id":
        return env.get(n[1], n)
    if k == "num":
        return n
    if k == "app":
        return ("app", substitute(n[1], env), [substitute(x, env) for x in n[2]])
    if k == "bin":
        return ("bin", n[1], substitute(n[2], env), substitute(n[3], env))
    if k == "un":
        return ("un", n[1], substitute(n[2], env))
    if k == "named":
        return ("named", n[1], substitute(n[2], env))
    if k == "ascribe":
        return ("ascribe", substitute(n[1], env), n[2])
    if k == "if":
        return ("if", substitute(n[1], env), substitute(n[2], env), substitute(n[3], env))
    if k == "match":
        return ("match", substitute(n[1], env), [(c, substitute(e, env)) for c, e in n[2]])
    if k == "let":
        return substitute(n[2], env)
    return n


def ids_of(n, out):
    k = n[0]
    if k == "id":
        out.add(n[1])
    elif k == "app":
        ids_of(n[1], out)
        for x in n[2]:
            ids_of(x, out)
    elif k in ("bin",):
        ids_of(n[2], out); ids_of(n[3], out)
    elif k in ("un", "named"):
        ids_of(n[2], out)
    elif k == "ascribe":
        ids_of(n[1], out)
    elif k == "if":
        ids_of(n[1], out); ids_of(n[2], out); ids_of(n[3], out)
    elif k == "match":
        ids_of(n[1], out)
        for _, e in n[2]:
            ids_of(e, out)
    return out


def subterms(n, out):
    """every operation node, in post-order; a match splits into its arms"""
    k = n[0]
    if k == "match":
        for _, e in n[2]:
            subterms(e, out)
        return out
    if k == "app":
        for x in n[2]:
            subterms(x, out)
        out.append(n)
    elif k == "bin":
        subterms(n[2], out); subterms(n[3], out); out.append(n)
    elif k == "un":
        subterms(n[2], out); out.append(n)
    elif k in ("named", "ascribe"):
        subterms(n[2] if k == "named" else n[1], out)
    elif k == "if":
        subterms(n[1], out); subterms(n[2], out); subterms(n[3], out); out.append(n)
    elif k == "let":
        subterms(n[2], out)
    return out


def rename_reads(n, order, reg_of):
    """reads -> unknowns by the order of first occurrence of their REGISTER in the
    subterm (the strip hoists a repeated read of one register into several names:
    v_rs1, v_rs1_2, ... are one unknown)"""
    env = {name: ("id", UNKNOWNS[order.index(reg)]) for name, reg in reg_of.items() if reg in order}
    return substitute(n, env)


def first_occurrence(n, reg_of, reads_order=None):
    """The registers the subterm reads, in the order the PURE FORM reads them when that
    order is given -- not in the order the subterm happens to mention them. A guard tests
    the second operand first (`if rs2 == 0 then -1 else rs1 / rs2`), and under first
    occurrence that subterm would be renamed with the divisor as `a`, the mirror of the
    function the unit's meaning names (a meaning always names the registers in the pure
    form's own parameter order). Registers the subterm does not read are dropped, so the
    unknowns stay a prefix a, b, ..."""
    seen = []

    def walk(m):
        k = m[0]
        if k == "id":
            if m[1] in reg_of and reg_of[m[1]] not in seen:
                seen.append(reg_of[m[1]])
        elif k == "app":
            walk(m[1])
            for x in m[2]:
                walk(x)
        elif k == "bin":
            walk(m[2]); walk(m[3])
        elif k in ("un", "named"):
            walk(m[2])
        elif k == "ascribe":
            walk(m[1])
        elif k == "if":
            walk(m[1]); walk(m[2]); walk(m[3])
        elif k == "match":
            walk(m[1])
            for _, e in m[2]:
                walk(e)
    walk(n)
    if reads_order is None:
        return seen
    return [r for r in reads_order if r in seen]


def literal_num(n):
    """the value of a node that IS a decimal numeral, None otherwise"""
    if n[0] == "num" and re.match(r"^\d+$", n[1]):
        return int(n[1])
    return None


def read_slice(n):
    """(unknown, width) when `n` is a slice of a READ taken from bit 0 with LITERAL bounds
    -- `extractLsb x k 0`, whose width is k + 1 -- and (None, None) for anything else.

    The bounds must be numerals. A slice whose high bound is written in the architecture's
    own parameters (`extractLsb b (log2_xlen -i 1) 0`, the masking a shift applies to its
    amount) is NOT a width read off the expression: it scales with the register, it is the
    operation's own use of a whole register, and the read keeps the register's width."""
    f = n[1]
    if f[0] != "id" or f[1].split(".")[-1] != SLICE:
        return None, None
    args = n[2]
    if len(args) != 3 or args[0][0] != "id" or args[0][1] not in UNKNOWNS:
        return None, None
    hi, lo = literal_num(args[1]), literal_num(args[2])
    if hi is None or lo != 0:
        return None, None
    return args[0][1], hi + 1


def operand_widths(n, arity):
    """THE WIDTH RULE (the owner, 2026-09-15): a definition's operand width, PER READ, is the
    width the definition's own subterm uses of that read, read off the subterm's own text.

    A read the subterm slices from bit 0 by literal bounds is used at the slice's width
    (`extractLsb a 31 0` is a use of 32 bits of a); a read used whole is used at the
    register's width; a read used both ways is used whole. So the W-form definitions --
    whose text reads only the low 32 bits of each register and sign-extends a 32-bit
    result -- have operand widths (32, 32), and their equivalents are the arch-units held
    at 32-bit holders; every other key keeps 64. `render` takes an arch-unit for a key when
    the arch-unit's holder widths EQUAL these. Result widths need no rule: a definition's
    result is the register.

    Nothing here is keyed by a name: the widths come from the key's own text."""
    whole, sliced = set(), {}

    def walk(m):
        k = m[0]
        if k == "id":
            if m[1] in UNKNOWNS:
                whole.add(m[1])
        elif k == "app":
            v, w = read_slice(m)
            if v is not None:
                sliced[v] = max(sliced.get(v, 0), w)
                return
            walk(m[1])
            for x in m[2]:
                walk(x)
        elif k == "bin":
            walk(m[2]); walk(m[3])
        elif k in ("un", "named"):
            walk(m[2])
        elif k == "ascribe":
            walk(m[1])
        elif k == "if":
            walk(m[1]); walk(m[2]); walk(m[3])
        elif k == "match":
            walk(m[1])
            for _, e in m[2]:
                walk(e)
        elif k == "let":
            walk(m[2])
    walk(n)
    return [REGISTER_WIDTH if v in whole or v not in sliced else sliced[v]
            for v in UNKNOWNS[:arity]]


def field_values(text):
    """a structure literal `{ f := v, ... }` read back as {field: value}; {} when the text
    is not one. The literal is the emit's own structure, written by `enum_values`."""
    m = re.match(r"^\s*\{(.*)\}\s*$", text, re.S)
    if not m:
        return {}
    out = {}
    for part in m.group(1).split(","):
        if ":=" in part:
            f, v = part.split(":=", 1)
            out[f.strip()] = v.strip()
    return out


def settings_of(lean_dir, others):
    """Every assignment of a pure form's NON-REGISTER parameters to a value of its own
    emitted type -- the same rule `equals` already uses for the definition side: an
    `inductive` of nullary constructors is its constructors, a `structure` of such fields
    is their product, `Bool` is false/true. A parameter whose type is not enumerated (an
    immediate, a register index) is left free, and the subterm filter drops what still
    mentions it, exactly as before. The empty assignment is always the first, so no
    candidate that existed before this rule stops existing.

    Each assignment maps identifiers to Lean text: the parameter itself, and -- because a
    field of a structure parameter is read in the emit as the single identifier `p.f` --
    every projection `p.f` to that field's value."""
    out = [{}]
    for n, t in others:
        vals = enum_values(lean_dir, t.strip("() "))
        if not vals or len(out) * (1 + len(vals)) > MAX_SETTINGS:
            continue                          # not enumerated, or past this clause's bound: leave it free
        grown = []
        for env in out:
            for v in vals:
                e = dict(env)
                e[n] = v
                for f, fv in field_values(v).items():
                    e["%s.%s" % (n, f)] = fv
                grown.append(e)
        out = out + grown
    return out


def free_params(ids, params):
    """the parameters a subterm still mentions. The emit writes a field of a structure
    parameter as ONE identifier `p.f`, so a dotted identifier whose head is a parameter is
    a mention of that parameter -- without this rule a field read hides the parameter from
    the filter and Lean rejects the candidate ("the argument p.f has type p -> T")."""
    out = set()
    for x in ids:
        if x in params:
            out.add(x)
        elif x.split(".")[0] in params:
            out.add(x.split(".")[0])
    return out


def as_term(text):
    """a setting's value as a term node: parenthesised unless it is already one name"""
    return ("id", text if re.match(r"^[\w.]+$", text.strip()) else "(%s)" % text.strip())


def fold(n):
    """Constant folding of the Booleans an assignment made literal: `not`, `&&`, `||`, a
    `(_ : Bool)` ascription of a literal, and an `if` on a literal condition. A rewrite on
    the node's own shape, sound for any term and keyed by nothing."""
    k = n[0]
    lit = lambda m: m[0] == "id" and m[1] in BOOL_LIT
    if k == "app":
        f = fold(n[1])
        xs = [fold(x) for x in n[2]]
        if f[0] == "id" and f[1] == "not" and len(xs) == 1 and lit(xs[0]):
            return ("id", "true" if xs[0][1] == "false" else "false")
        return ("app", f, xs)
    if k == "bin":
        a, b = fold(n[2]), fold(n[3])
        if n[1] == "&&":
            if lit(a):
                return b if a[1] == "true" else a
            if lit(b):
                return a if b[1] == "true" else b
        if n[1] == "||":
            if lit(a):
                return a if a[1] == "true" else b
            if lit(b):
                return b if b[1] == "true" else a
        return ("bin", n[1], a, b)
    if k == "un":
        return ("un", n[1], fold(n[2]))
    if k == "named":
        return ("named", n[1], fold(n[2]))
    if k == "ascribe":
        a = fold(n[1])
        return a if lit(a) else ("ascribe", a, n[2])
    if k == "if":
        c, t, e = fold(n[1]), fold(n[2]), fold(n[3])
        if lit(c):
            return t if c[1] == "true" else e
        return ("if", c, t, e)
    if k == "match":
        s = fold(n[1])
        arms = [(c, fold(e)) for c, e in n[2]]
        if s[0] == "id":                      # the scrutinee is now a constructor: the match IS its arm
            for c, e in arms:
                if c == s[1].split(".")[-1]:
                    return e
        return ("match", s, arms)
    if k == "let":
        return ("let", n[1], fold(n[2]))
    return n


def candidates_of_definitions(lean_dir, strip_rows):
    """[{"G": text over a b, "arity": n, "from": [(clause, ...)]}], deduplicated by text"""
    clauses = {c["name"][len("execute_"):]: c for c in ST.clauses_of(lean_dir)}
    by_text = {}
    for name, r in strip_rows.items():
        if r.get("verdict") != "CERTIFIED" or r.get("shape") != "straight" or name not in clauses:
            continue
        p = ST.propose(clauses[name])
        reads = [v for v, _ in p["reads"]]
        reg_of = {v: reg for v, reg in p["reads"]}
        reads_order = []
        for _, reg in p["reads"]:                 # the pure form's own parameter order, deduplicated
            if reg not in reads_order:
                reads_order.append(reg)
        params = set(reads) | {n for n, _ in p.get("others", [])} | {n for n, _ in clauses[name]["params"]}
        env = {}
        try:
            for ln, text in p.get("lets", []):
                ln = ln.split(":")[0].strip()
                env[ln] = substitute(LZ.parse(text), env)
            root = substitute(LZ.parse(p["value"]), env)
        except Exception as ex:
            continue
        # the pure form at every value of its non-register parameters, the free form included
        for setting in settings_of(lean_dir, p.get("others", [])):
            here = fold(substitute(root, {k: as_term(v) for k, v in setting.items()})) if setting else root
            for st in subterms(here, []):
                ids = ids_of(st, set())
                frees = free_params(ids, params)
                if not frees or not frees <= set(reads):
                    continue                  # an immediate, a parameter still free, or no read at all
                order = first_occurrence(st, reg_of, reads_order)
                if len(order) > len(UNKNOWNS):
                    continue
                renamed = rename_reads(st, order, reg_of)
                G = to_lean(renamed)
                key = re.sub(r"\s+", " ", G)
                e = by_text.setdefault(key, {"G": G, "arity": len(order), "from": [],
                                             "operand_widths": operand_widths(renamed, len(order))})
                if name not in e["from"]:
                    e["from"].append(name)
    out = sorted(by_text.values(), key=lambda e: (e["arity"], len(e["G"]), e["G"]))
    return out


def bitvec_width(t):
    """the width of a `BitVec w` type: an int when w is literal arithmetic (`64`,
    `(63 - 0 + 1)`), the TEXT of w when it is a name the emit defines (`xlen`), None when
    the type is not a vector. A name is not a rejection: Lean evaluates it."""
    t = t.strip()
    if not t.startswith("BitVec"):
        return None
    w = t[len("BitVec"):].strip()
    if w.startswith("(") and w.endswith(")"):
        w = w[1:-1].strip()
    if re.match(r"^[\d\s()+\-*]+$", w):
        try:
            return int(eval(w, {"__builtins__": {}}, {}))       # digits, spaces, + - * ( ) only, checked by the regex
        except Exception:
            return None
    return w if re.match(r"^[A-Za-z_][\w.']*$", w) else None


def widths_by_lean(proof_project, header, closers, names, out_dir, timeout_s=300):
    """a width Lean printed as a NAME is a width Lean can evaluate: one short run,
    `#eval` per name. Returns {name: width}."""
    if not names:
        return {}, 0.0
    lines = header + [""]
    for i, w in enumerate(names):
        lines.append('#eval IO.println s!"W %d {(%s : Nat)}"' % (i, w))
    lines += closers + [""]
    path = os.path.join(out_dir, "Typed_widths.lean")
    open(path, "w").write("\n".join(lines))
    rc, secs, out = lean_run(proof_project, path, timeout_s)
    got = {}
    for m in re.finditer(r"^W (\d+) (\d+)\s*$", out, re.M):
        got[names[int(m.group(1))]] = int(m.group(2))
    return got, secs


def typed_by_lean(proof_project, header, closers, cands, out_dir, timeout_s=600):
    """one Lean run: `#check (fun (kNNN_a : BitVec 64) ... => G)` per candidate. Lean prints the
    INFERRED type with no expected type imposed, so no coercion can let a Nat or a narrower
    vector through (an `example ... : BitVec 64 := G` did: lean-sail coerces). A candidate
    survives when every result of its type is exactly `BitVec 64`."""
    lines = header + ["set_option linter.unusedVariables false", ""]
    for k, c in enumerate(cands):
        G = c["G"]
        for v in UNKNOWNS[:c["arity"]]:
            G = re.sub(r"\b%s\b" % v, "k%03d_%s" % (k, v), G)
        unk = " ".join("(k%03d_%s : BitVec 64)" % (k, v) for v in UNKNOWNS[:c["arity"]])
        lines += ["#check (fun %s => (%s))" % (unk, G), ""]
    lines += closers + [""]
    path = os.path.join(out_dir, "Typed_candidates.lean")
    open(path, "w").write("\n".join(lines))
    rc, secs, out = lean_run(proof_project, path, timeout_s)
    if rc == -1:
        return None, secs, path
    # Lean prints a long term over several lines, the continuation lines indented: join them first
    flat = re.sub(r"\n[ \t]+", " ", out)
    typ = {}
    for m in re.finditer(r"^fun k(\d+)_a[^\n]*? : (.+)$", flat, re.M):
        typ[int(m.group(1))] = m.group(2).strip()

    parts_of = lambda t: [bitvec_width(x) for x in t.split("→")]
    symbolic = sorted({w for k, c in enumerate(cands) if typ.get(k) is not None
                       for w in parts_of(typ[k]) if isinstance(w, str)})
    evaluated, secs2 = widths_by_lean(proof_project, header, closers, symbolic, out_dir)
    secs += secs2
    keep = []
    for k, c in enumerate(cands):
        t = typ.get(k)
        if t is None:
            continue
        ws = [evaluated.get(w, w) if isinstance(w, str) else w for w in parts_of(t)]
        if len(ws) == c["arity"] + 1 and all(w == 64 for w in ws):
            c = dict(c); c["type"] = t; keep.append(c)
    return keep, secs, path


def evaluate_units(proof_project, header, closers, units, GD_of, out_dir, tag, timeout_s=900):
    """the evaluation across MANY units in one Lean run: one `#eval` line per (unit, sample); a
    line that does not evaluate loses only its unit. Returns {unit index: survivors or None}."""
    lam = lambda unknowns, body: "(fun %s => (%s))" % (" ".join("(%s : BitVec 64)" % v for v in unknowns), body)
    args = lambda unknowns, s: " ".join("(%s)" % s[i] for i in range(len(unknowns)))
    lines = header + [""]
    shared_seen, shared = set(), []
    for i, (u, unknowns, F, GD, bodies_key, bodies) in enumerate(units):
        if bodies_key not in shared_seen:
            shared_seen.add(bodies_key); shared += bodies
    lines += shared + [""]
    for i, (u, unknowns, F, GD, _, _) in enumerate(units):
        for j, s in enumerate(SAMPLES):
            items = ", ".join("%s %s" % (lam(unknowns, body), args(unknowns, s)) for body in [F] + [G for G, _ in GD])
            lines.append('#eval IO.println s!"E %d %d [{String.intercalate ", " (([%s] : List (BitVec 64)).map (fun x => toString x.toNat))}]"' % (i, j, items))
    lines += closers + [""]
    path = os.path.join(out_dir, "Eval_%s.lean" % tag)
    open(path, "w").write("\n".join(lines))
    rc, secs, out = lean_run(proof_project, path, timeout_s)
    rows = {}
    for m in re.finditer(r"^E (\d+) (\d+) \[(.*)\]\s*$", out, re.M):
        rows.setdefault(int(m.group(1)), {})[int(m.group(2))] = [x.strip() for x in m.group(3).split(",")]
    result = {}
    for i, (u, unknowns, F, GD, _, _) in enumerate(units):
        r = rows.get(i, {})
        if any(j not in r or len(r[j]) != len(GD) + 1 for j in range(len(SAMPLES))):
            result[i] = None
        else:
            result[i] = [k for k in range(len(GD)) if all(r[j][k + 1] == r[j][0] for j in range(len(SAMPLES)))]
    return result, secs, path


def cmd_operator_for(argv, say, write_json, check_memory=None):
    proof_project, lib, strip_json, walk_jsons, out_dir = argv[:5]
    budget_s = int(argv[5]) if len(argv) > 5 else 120
    unit_budget_s = int(os.environ.get("EQUALS_UNIT_BUDGET_S", "150"))
    chunk = int(os.environ.get("EQUALS_CHUNK", "12"))
    eval_units = int(os.environ.get("EVAL_UNITS", "40"))          # units per evaluation file
    os.makedirs(out_dir, exist_ok=True)
    lean_dir = os.path.join(proof_project, lib)
    header, closers = ST.header_of(lean_dir, lib)
    clauses = {c["name"][len("execute_"):]: c for c in ST.clauses_of(lean_dir)}
    defs_index = emitted_defs(lean_dir)
    ST.library_index(proof_project)
    strip_rows = {r["clause"][len("execute_"):]: r for r in json.load(open(strip_json))["rows"]}
    cands = candidates_of_definitions(lean_dir, strip_rows)
    say("  candidates: %d subterms of the certified pure forms" % len(cands))
    typed, secs, path = typed_by_lean(proof_project, header, closers, cands, out_dir)
    if typed is None:
        say("  Lean did not type the candidates within the budget (%s)" % path)
        return 1
    say("  typed by Lean, every argument and the result exactly BitVec 64: %d of %d (%.1fs)" % (len(typed), len(cands), secs))
    cands = typed
    write_json(os.path.join(out_dir, "candidates.json"), cands)
    units = []
    for wj in walk_jsons.split(","):
        units += [u for u in json.load(open(wj))["rows"] if u.get("verdict") == "CERTIFIED"]
    # the holders of each unit's parameters, from the corpus units file beside the walk (log 283 §3: the width is part of the key)
    holders_of = {}
    for wj in walk_jsons.split(","):
        cu = os.path.join(os.path.dirname(os.path.dirname(wj)), "units.json")
        if os.path.exists(cu):
            for x in json.load(open(cu)):
                if "holders" in x:
                    holders_of[x["name"]] = x["holders"]
    say("  units with a certified meaning: %d" % len(units))
    # each unit: its unknowns, its candidates of fitting arity, the defs each candidate unfolds, the pure bodies its meaning names
    prepared = []
    for u in units:
        F = u["proposal"]
        unknowns = [v for v in UNKNOWNS if re.search(r"\b%s\b" % v, F)]
        mine = [c for c in cands if c["arity"] <= len(unknowns) and all(v in unknowns for v in UNKNOWNS[:c["arity"]])]
        heads = sorted(set(re.findall(r"pure_(\w+)", F)))
        bodies = []
        for h in heads:
            if h in clauses:
                bodies += ST.lean_body(clauses[h], ST.propose(clauses[h]))
        # what the provers may unfold: the pure forms the unit's meaning names, everything those reach
        # (sign_extend, extractLsb, ... in an immediate-carrying meaning), and what the candidate names
        pure_text = "\n".join(re.findall(r"^def pure_.*?(?=^theorem|\Z)", "\n".join(bodies), re.S | re.M))
        base = ["pure_%s" % h for h in heads]
        base += [d for d in reachable(defs_index, pure_text) if d not in base]
        base += [d for d in library_refs(defs_index, base, extra_texts=[pure_text]) if d not in base]
        GD = []
        for c in mine:
            defs = list(base)
            defs += [d for d in reachable(defs_index, c["G"]) if d not in defs]
            defs += [d for d in library_refs(defs_index, defs, extra_texts=[c["G"]]) if d not in defs]
            GD.append((c["G"], defs))
        prepared.append((u, unknowns, F, GD, ",".join(heads), bodies, mine))
    # the evaluation, across units: files of eval_units units, one Lean run each
    survivors = {}
    t_eval = time.time()
    constant = [i for i, b in enumerate(prepared) if not b[1] or not b[6]]     # no unknown, or no candidate of its arity
    for i in constant:
        survivors[i] = []
    say("  units with a constant meaning or no candidate of their arity: %d (no evaluation, no proof)" % len(constant))
    evaluable = [i for i in range(len(prepared)) if i not in survivors]
    for start in range(0, len(evaluable), eval_units):
        idx = evaluable[start:start + eval_units]
        block = [prepared[i] for i in idx]
        res, secs0, path0 = evaluate_units(proof_project, header, closers, [b[:6] for b in block], None, out_dir, "%04d" % start)
        for j, i in enumerate(idx):
            survivors[i] = res.get(j)
        alive = sum(len(v) for v in res.values() if v)
        say("  evaluation of %d units (%d..%d): %.1fs; %d did not evaluate; %d (unit, candidate) pairs survive" % (
            len(block), idx[0], idx[-1], secs0, sum(1 for v in res.values() if v is None), alive))
    say("  evaluation over all units: %.1fs" % (time.time() - t_eval))
    # the provers, only where something survived (a unit that did not evaluate keeps every candidate)
    table = {}
    rows = []
    for i, (u, unknowns, F, GD, _, bodies, mine) in enumerate(prepared):
        live = survivors.get(i)
        if live is None:
            live = list(range(len(mine)))
        if not live:
            rows.append({"unit": u["unit"], "F": F, "matches": [], "tried": len(mine),
                         "survived_evaluation": 0, "evaluated": survivors.get(i) is not None})
            continue
        utag = re.sub(r"\W", "_", u["unit"])[:100]
        t0 = time.time()
        matches = {}
        for stage in ("same_text", "integer_level", "fixed_width"):
            if not live or time.time() - t0 > unit_budget_s:
                break
            step = len(live) if stage == "same_text" else chunk
            for j in range(0, len(live), step):
                idx = live[j:j + step]
                got, secs1, path1 = equals_batch(proof_project, header, closers, bodies, utag, unknowns, F, GD, out_dir, stage, idx, budget_s)
                if got is None:
                    continue
                for k in idx:
                    if got[k] and k not in matches:
                        matches[k] = stage
            live = [k for k in live if k not in matches]
        for k, stage in matches.items():
            table.setdefault(mine[k]["G"], []).append({"unit": u["unit"], "stage": stage, "from": mine[k]["from"],
                                                       "holders": holders_of.get(u["unit"]),
                                                       "operand_widths": mine[k].get("operand_widths")})
        rows.append({"unit": u["unit"], "F": F, "matches": [{"G": mine[k]["G"], "stage": st} for k, st in matches.items()],
                     "tried": len(mine), "survived_evaluation": len(survivors.get(i) or []),
                     "evaluated": survivors.get(i) is not None, "seconds": round(time.time() - t0, 1)})
        say("  %-24s F=%s; %d survived; matches: %d  %s" % (u["unit"], F[:50], rows[-1]["survived_evaluation"], len(matches), "; ".join(mine[k]["G"][:36] for k in list(matches)[:3])))
    # the width rule: each key's operand widths, read off the key's own text, beside the key
    widths = {G: (es[0].get("operand_widths") or []) for G, es in table.items()}
    usable = sum(1 for G, es in table.items()
                 if any((e.get("holders") or []) == widths[G] for e in es))
    write_json(os.path.join(out_dir, "operator_for.json"), {"table": table, "rows": rows, "operand_widths": widths,
               "summary": {"units": len(units), "candidates": len(cands), "entries": sum(len(v) for v in table.values()),
                           "keys_filled": len(table), "units_with_a_match": sum(1 for r in rows if r["matches"]),
                           "keys_narrower_than_the_register": sum(1 for w in widths.values() if any(x != REGISTER_WIDTH for x in w)),
                           "keys_with_a_unit_at_their_widths": usable}})
    say("  operator_for: %d keys filled, %d entries, %d of %d units matched; %d keys read narrower than the register, %d keys have a unit at their own widths" % (
        len(table), sum(len(v) for v in table.values()), sum(1 for r in rows if r["matches"]), len(units),
        sum(1 for w in widths.values() if any(x != REGISTER_WIDTH for x in w)), usable))
    return 0
