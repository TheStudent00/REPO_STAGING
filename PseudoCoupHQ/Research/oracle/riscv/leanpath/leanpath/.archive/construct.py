"""construct -- the construction stage, no proofs: for every Sail clause
that `propose_all` reads, every value of its enumerated parameters, and
every place it writes, the term D as z3, printed in every language both
ways by the printer that already exists (task t4's `render_general`,
with its constructions proved once), written to files, and listed as
units for the walk (which lowers them, decodes them with Sail's own
decoder and composes L; certification off).

  python3 -m leanpath construct <emit lean dir> <out dir> [langs csv] [only csv]

Writes <out dir>/emulations/<clause>__<variant>__<place>__<lang>__<policy>.<ext>,
<out dir>/construct.json (every row: D as Lean text and as z3 text, the
files, the printer's refusals), and <out dir>/units.json for the walk.

Nothing here names an instruction: the clauses come from the emit, the
enumerated values from the emit's own types, the places from the
clause's own writes.
"""
import itertools
import json
import os
import re
import sys

from . import strip as ST
from . import propose_all as PA
from . import lean_to_z3 as LZ
from .equals import enum_values

HQ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", ".."))
EMU = os.path.join(HQ, "Research", "oracle", "cross_construction", "emulation")
NAT_DOMAIN = {"width": [1, 2, 4, 8]}     # a Nat parameter that is a byte width; the decoder's own values
POLICIES = ("native_first", "all_constructed")
EXT = {"c": "c", "cpp": "cpp", "rust": "rs", "go": "go"}


def the_printer():
    """the old printer's modules, on the path the earlier drivers used"""
    for p in (os.path.join(EMU, "construct", "general"), os.path.join(EMU, "construct"), EMU,
              os.path.join(EMU, "handful"), os.path.join(HQ, "Research", "oracle", "riscv"),
              os.path.join(HQ, "Research", "oracle")):
        if p not in sys.path:
            sys.path.insert(0, p)
    import z3  # noqa
    import render_general as RG
    import handful as H
    import rv_loop as RL
    import construct as CONS
    import term  # noqa: the module `rv_loop.in_parameter_slots` is handed
    return RG, H, RL, CONS


def variants_of(clause, proposal, lean_dir):
    """every choice of the enumerated parameters; the inputs of each"""
    inputs = list(proposal["inputs"])
    domains = {}
    enums = {}
    for pname, ptype in proposal.get("others", []):
        pt = ptype.strip("() ")
        m = re.match(r"^BitVec (\d+)$", pt)
        if m:
            inputs.append((pname, "bv", int(m.group(1))))
            continue
        if pt == "Bool":
            inputs.append((pname, "bool", None))
            domains[pname] = [False, True]
            continue
        if pt == "Nat":
            if pname not in NAT_DOMAIN:
                return None, "a Nat parameter %s with no known domain" % pname
            inputs.append((pname, "nat", None))
            domains[pname] = NAT_DOMAIN[pname]
            continue
        ev = enum_values(lean_dir, pt)
        if ev is None:
            return None, "a parameter %s : %s that is not enumerable" % (pname, pt)
        inputs.append((pname, "enum", None))
        domains[pname] = [v if v.startswith("{") else v.split(".")[-1] for v in ev]
        if not ev[0].startswith("{"):
            enums[pt] = [v.split(".")[-1] for v in ev]
    keys = list(domains)
    combos = list(itertools.product(*[domains[k] for k in keys])) if keys else [()]
    return [(dict(zip(keys, c)), inputs, enums) for c in combos], None


def resolved_inputs(inputs, choice):
    """`8*width` widths resolved by the choice"""
    out = []
    for name, kind, width in inputs:
        if isinstance(width, str):
            m = re.match(r"^8\*(\w+)$", width)
            width = 8 * choice[m.group(1)] if m and m.group(1) in choice else None
            if width is None:
                raise LZ.Unknown("width %s unresolved" % width)
        out.append((name, kind, width))
    return out


def variant_label(choice):
    parts = []
    for k, v in choice.items():
        s = str(v)
        if s.startswith("{"):
            s = "_".join(re.findall(r":=\s*[\w.]*?(\w+)\s*[,}]", s))   # the value after the last dot of each field
        parts.append("%s_%s" % (k, re.sub(r"\W", "", s)))
    return "__".join(parts) if parts else "one"


SLOT_WIDTH = 64      # an emulation receives every input in a register: a narrower value is its low bits


def term_of(place_text, inputs, lets, enums, choice):
    v = LZ.read_pure_form(inputs, lets, place_text, enums, choice, slot_width=SLOT_WIDTH)
    import z3
    if v[0] == "bool":
        return z3.If(v[1], z3.BitVecVal(1, 64), z3.BitVecVal(0, 64))
    if v[0] == "int":
        return z3.Extract(63, 0, v[1])
    if v[0] == "nat":
        return z3.BitVecVal(v[1], 64)
    return v[1]


TREE_BOUND = int(os.environ.get("CONSTRUCT_TREE_BOUND", "100000"))   # the printer walks a term as a tree: one statement per tree node


def sizes_of(term):
    """(shared nodes, tree nodes) of a z3 term; the tree count is memoized by node, so it costs the graph"""
    memo = {}

    def walk(e):
        k = e.get_id()
        if k in memo:
            return memo[k]
        s = 1 + sum(walk(ch) for ch in e.children())
        memo[k] = s
        return s
    tree = walk(term)
    return len(memo), tree


def render_both(RG, H, RL, CONS, term, label, lang, text):
    """the printer both ways: {policy: {"source", "symbol", ...} or {"refused": why}}"""
    import z3
    out = {}
    slotted, refusal = RL.in_parameter_slots(sys.modules["term"], term)
    if slotted is None:
        return {p: {"refused": refusal} for p in POLICIES}
    record = H.place_record("reg_rdi", slotted)
    if record.get("families") is None:
        why = record.get("not_rendered_detail") or record.get("not_rendered") or "no families"
        return {p: {"refused": str(why)} for p in POLICIES}
    word = CONS.word_of(lang)
    if word is None:
        return {p: {"refused": "no word for %s" % lang} for p in POLICIES}
    ordered = H.renderer_input(record["term"])
    for policy in POLICIES:
        try:
            made = RG.render(ordered, lang, record["families"], record["home"]["family"], record["bits"],
                             "%s__%s__%s" % (label, lang, policy), word, policy, text)
            out[policy] = {"source": made["source"], "symbol": made["symbol"], "statements": made["statements"],
                           "native_nodes": made["native_nodes"], "constructed_nodes": made["constructed_nodes"],
                           "constructed_kinds": made["constructed_kinds"]}
        except Exception as problem:
            out[policy] = {"refused": "%s: %s" % (getattr(problem, "cause", type(problem).__name__), str(getattr(problem, "detail", problem))[:160])}
    return out


FLAGS = {"c": "clang -std=c17 -O1 --target=riscv64-linux-gnu --gcc-toolchain=/usr",
         "cpp": "clang++ -std=c++20 -O1 --target=riscv64-linux-gnu --gcc-toolchain=/usr",
         "rust": "rustc --target riscv64gc-unknown-linux-gnu --crate-type lib --emit obj -C opt-level=1",
         "go": "GOARCH=riscv64 GOOS=linux go build"}


def cmd_construct(argv, say, write_json):
    lean_dir, out_dir = argv[0], argv[1]
    langs = argv[2].split(",") if len(argv) > 2 else ["c", "cpp", "rust", "go"]
    only = set(argv[3].split(",")) if len(argv) > 3 and argv[3] else None
    os.makedirs(os.path.join(out_dir, "emulations"), exist_ok=True)
    RG, H, RL, CONS = the_printer()
    import z3
    clauses = ST.clauses_of(lean_dir)
    rows = []
    units = []
    counts = {"clauses": 0, "proposed": 0, "deferred": 0, "variants": 0, "terms": 0, "term_failures": 0, "files": 0, "printer_refusals": 0}
    for c in clauses:
        name = c["name"][len("execute_"):]
        if only and name not in only:
            continue
        counts["clauses"] += 1
        p = PA.propose_any(c)
        if "deferred" in p:
            counts["deferred"] += 1
            rows.append({"clause": name, "deferred": p["deferred"], "notes": p.get("notes", [])})
            continue
        counts["proposed"] += 1
        vs, why = variants_of(c, p, lean_dir)
        if vs is None:
            rows.append({"clause": name, "deferred": why, "notes": p.get("notes", [])})
            counts["deferred"] += 1
            continue
        for choice, inputs, enums in vs:
            counts["variants"] += 1
            vlabel = variant_label(choice)
            try:
                ins = resolved_inputs(inputs, choice)
            except LZ.Unknown as ex:
                rows.append({"clause": name, "variant": choice, "deferred": str(ex)})
                continue
            for place, ptext in p["outputs"].items():
                row = {"clause": name, "variant": choice, "place": place, "D_lean": ptext, "lets": p["lets"],
                       "inputs": [(n, k, w) for n, k, w in ins if n not in choice], "notes": p.get("notes", []), "files": {},
                       "slotted": ["%s (%d bits, in a %d-bit slot)" % (n, w, SLOT_WIDTH) for n, k, w in ins
                                   if n not in choice and k == "bv" and isinstance(w, int) and w < SLOT_WIDTH]}
                try:
                    term = term_of(ptext, ins, p["lets"], enums, choice)
                    counts["terms"] += 1
                except Exception as ex:
                    counts["term_failures"] += 1
                    row["term_failure"] = "%s: %s" % (type(ex).__name__, str(ex)[:160])
                    rows.append(row)
                    continue
                row["dag_nodes"], row["tree_nodes"] = sizes_of(term)
                if row["tree_nodes"] > TREE_BOUND:
                    counts["term_failures"] += 1
                    row["term_failure"] = "the term as a tree has %d nodes (%d shared): beyond the printer's tree bound %d" % (
                        row["tree_nodes"], row["dag_nodes"], TREE_BOUND)
                    rows.append(row)
                    continue
                row["D_z3"] = str(z3.simplify(term))[:2000]
                label = "%s__%s__%s" % (name, vlabel, place)
                for lang in langs:
                    made = render_both(RG, H, RL, CONS, term, label, lang, "")
                    for policy, r in made.items():
                        key = "%s__%s" % (lang, policy)
                        if "refused" in r:
                            counts["printer_refusals"] += 1
                            row["files"][key] = {"refused": r["refused"]}
                            continue
                        fname = "%s__%s__%s.%s" % (label, lang, policy, EXT[lang])
                        path = os.path.join(out_dir, "emulations", fname)
                        open(path, "w").write(r["source"])
                        counts["files"] += 1
                        row["files"][key] = {"path": path, "symbol": r["symbol"], "statements": r["statements"],
                                             "native_nodes": r["native_nodes"], "constructed_nodes": r["constructed_nodes"]}
                        units.append({"name": "%s__%s__%s" % (label, lang, policy), "lang": lang, "source": path,
                                      "symbol": r["symbol"], "flags": FLAGS[lang],
                                      "cell_display": "%s %s %s (%s, %s)" % (name, vlabel, place, lang, policy)})
                rows.append(row)
        say("  %-16s %2d variants, %d places" % (name, len(vs), len(p["outputs"])))
    write_json(os.path.join(out_dir, "construct.json"), {"counts": counts, "rows": rows})
    write_json(os.path.join(out_dir, "units.json"), units)
    say("  construct: %s" % json.dumps(counts))
    return 0
