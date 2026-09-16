"""render -- Language.render (plan node
hq.research.lean_proof_path_resistant_to_churn.language.render): an
emulation of a Sail definition written from `operator_for` and nothing
else.

  python3 -m leanpath render <emit lean dir> <strip.json> <operator_for.json> <corpus units.json> <out dir> [lang] [limit]

For every certified straight pure form (the strip), every arm of its
`match` over an enumerated parameter is one definition D over its
register reads. The tree of D is matched, largest node first, against
the KEYS of operator_for (subterms of the definitions over the unknowns
a, b, ...): a key is a pattern whose unknowns bind the node's children.
A match writes a call to the corpus unit the key holds (its probe
source copied verbatim into the output, byte for byte); the bound
children are rendered the same way; a read renders as the emulation's
parameter; a numeral as a literal. A node no key matches is a refusal
naming the subterm. Nothing here knows an operator's spelling: the
keys come from the definitions, the units from the proofs.

Plumbing, written once per language: the function syntax of the
composition and the spelling of a call and a literal.
"""
import json
import os
import re

from . import strip as ST
from . import lean_tree as LZ
from .operator_for import (to_lean, substitute, subterms, ids_of, UNKNOWNS,
                           settings_of, field_values, as_term, fold, operand_widths)

EXT = {"c": "c", "cpp": "cpp", "rust": "rs", "go": "go"}


def size(n):
    k = n[0]
    if k in ("num", "id"):
        return 1
    if k == "app":
        return 1 + size(n[1]) + sum(size(x) for x in n[2])
    if k == "bin":
        return 1 + size(n[2]) + size(n[3])
    if k in ("un", "named"):
        return 1 + size(n[2])
    if k == "ascribe":
        return 1 + size(n[1])
    if k == "if":
        return 1 + size(n[1]) + size(n[2]) + size(n[3])
    return 1


def match(pat, node, b):
    """pat over the unknowns; node any tree; b the bindings (unknown -> node), consistent"""
    k = pat[0]
    if k == "id" and pat[1] in UNKNOWNS:
        if pat[1] in b:
            return to_lean(b[pat[1]]) == to_lean(node)
        b[pat[1]] = node
        return True
    if k != node[0]:
        return False
    if k in ("num", "id"):
        return pat[1] == node[1]
    if k == "app":
        return match(pat[1], node[1], b) and len(pat[2]) == len(node[2]) and all(match(p, q, b) for p, q in zip(pat[2], node[2]))
    if k == "bin":
        return pat[1] == node[1] and match(pat[2], node[2], b) and match(pat[3], node[3], b)
    if k == "un":
        return pat[1] == node[1] and match(pat[2], node[2], b)
    if k == "named":
        return pat[1] == node[1] and match(pat[2], node[2], b)
    if k == "ascribe":
        return pat[2] == node[2] and match(pat[1], node[1], b)
    if k == "if":
        return all(match(pat[i], node[i], b) for i in (1, 2, 3))
    return False


class Refusal(Exception):
    pass


# --- plumbing, once per language: how a unit's function is carried into the output (verbatim), how a call, a
# literal and the composition function are spelled. The unit's own parameter types come from its probe record
# (the manifest's `lhs_type`, `rhs_type`), never from a table here.
def _func_block(src, marker):
    """the function that begins at `marker` in the probe source, to its closing brace, byte for byte"""
    i = src.find(marker)
    if i < 0:
        raise Refusal("the probe source has no %s" % marker.strip())
    j = src.find("{", i)
    depth = 0
    for k in range(j, len(src)):
        if src[k] == "{":
            depth += 1
        elif src[k] == "}":
            depth -= 1
            if depth == 0:
                return src[i:k + 1]
    raise Refusal("unbalanced braces after %s" % marker.strip())


def _go_returns_bool(unit):
    src = open(unit["source"]).read()
    m = re.search(r"func %s\([^)]*\)\s+(\w+)\s*\{" % re.escape(unit["symbol"]), src)
    return bool(m and m.group(1) == "bool")


def _types_of(unit):
    pr = unit.get("probe", {})
    return [t for t in (pr.get("lhs_type"), pr.get("rhs_type")) if t]


PLUMBING = {
    "c": {
        "unit_source": lambda unit, src: src,                                    # the whole probe file: includes and the function
        "call": lambda unit, args: "%s(%s)" % (unit["symbol"], ", ".join(args)),
        "literal": lambda v, w: "((uint64_t)%dULL)" % v,
        "function": lambda name, params, body, units_src: "%s\n\nuint64_t\n%s(%s)\n{\n    return (uint64_t)(%s);\n}\n" % (
            units_src, name, ", ".join("uint64_t %s" % p for p in params) or "void", body),
    },
    "cpp": {
        "unit_source": lambda unit, src: src,
        "call": lambda unit, args: "%s(%s)" % (unit["symbol"], ", ".join(args)),
        "literal": lambda v, w: "((uint64_t)%dULL)" % v,
        "function": lambda name, params, body, units_src: "%s\n\nextern \"C\" uint64_t\n%s(%s)\n{\n    return (uint64_t)(%s);\n}\n" % (
            units_src, name, ", ".join("uint64_t %s" % p for p in params) or "void", body),
    },
    "rust": {
        "unit_source": lambda unit, src: src,                                    # the probe file is the function and its attribute
        # a call casts each argument to the unit's own parameter type and the result back to u64
        "call": lambda unit, args: "((%s(%s)) as u64)" % (unit["symbol"], ", ".join("(%s) as %s" % (a, t) for a, t in zip(args, _types_of(unit)))),
        "literal": lambda v, w: "(%du64)" % v,
        "function": lambda name, params, body, units_src: "%s\n\n#[no_mangle]\npub extern \"C\" fn %s(%s) -> u64 {\n    %s\n}\n" % (
            units_src, name, ", ".join("%s: u64" % p for p in params), body),
    },
    "go": {
        # the probe file carries a package line, the function, sinks and a main: only the function is carried, byte for byte
        "unit_source": lambda unit, src: _func_block(src, "func %s(" % unit["symbol"]),
        # go has no conversion from bool to an integer: a unit whose function returns `bool` (read off its own
        # signature in the probe source: `func op_N(...) bool {`) goes through b2u
        "call": lambda unit, args: ("b2u(%s(%s))" if _go_returns_bool(unit) else "uint64(%s(%s))") % (
            unit["symbol"], ", ".join("%s(%s)" % (t, a) for a, t in zip(args, _types_of(unit)))),
        "literal": lambda v, w: "uint64(%d)" % v,
        "function": lambda name, params, body, units_src: "package main\n\n%s\n\nfunc b2u(x bool) uint64 {\n\tif x {\n\t\treturn 1\n\t}\n\treturn 0\n}\n\n//go:noinline\nfunc %s(%s) uint64 {\n\treturn %s\n}\n\nvar sink interface{}\n\nfunc main() {\n\tsink = %s(%s)\n\t_ = sink\n}\n" % (
            units_src, name, ", ".join("%s uint64" % p for p in params), body, name, ", ".join("0" for _ in params)),
    },
}


def numeral_value(text):
    m = re.match(r"^(0x[0-9a-fA-F]+|\d+)#(\d+)$", text)
    if m:
        return int(m.group(1), 0), int(m.group(2))
    if re.match(r"^\d+$", text):
        return int(text), None
    raise Refusal("a numeral the plumbing does not spell: %s" % text)


class Renderer(object):
    def __init__(self, table, corpus_units, lang):
        self.lang = lang
        self.plumb = PLUMBING[lang]
        self.units = {u["name"]: u for u in corpus_units}
        self.keys = []                                   # (size, pattern tree, key text, unit)
        self.narrow = {}                                 # key text -> (its operand widths, the holders it is held at)
        self.widths_of = {}                              # key text -> the widths the key reads its operands at
        for G, entries in table.items():
            mine = [e for e in entries if e["unit"] in self.units and self.units[e["unit"]]["lang"] == lang]
            if not mine:
                continue
            try:
                pat = LZ.parse(G)
            except Exception:
                continue
            arity = len([v for v in UNKNOWNS if re.search(r"\b%s\b" % v, G)])
            # THE WIDTH RULE (the owner, 2026-09-15): a definition's operand width, per read, is the width the
            # definition's own subterm uses of that read -- recorded beside the key by `operator_for`, and read
            # off the key's own text here when an older table does not carry it. A unit renders a key when its
            # holder widths EQUAL those operand widths: the W forms read 32 bits of each register, so the units
            # that render them are held at 32-bit holders; a key whose reads are used whole keeps 64.
            want = mine[0].get("operand_widths") or operand_widths(pat, arity)
            self.widths_of[G] = want
            fit = [e for e in mine if (e.get("holders") or self.units[e["unit"]].get("holders") or []) == want]
            if not fit:
                self.narrow[G] = (want, sorted({tuple(e.get("holders") or self.units[e["unit"]].get("holders") or []) for e in mine}))
                continue
            self.keys.append((size(pat), pat, G, fit[0]["unit"]))
        self.keys.sort(key=lambda t: -t[0])              # the largest pattern first
        self.used = []                                   # (subterm text, unit) in order of use

    def render(self, node, params):
        k = node[0]
        if k == "id":
            if node[1] in params:
                return params[node[1]]
            raise Refusal("a free name no key binds: %s" % node[1])
        if k == "num":
            v, w = numeral_value(node[1])
            return self.plumb["literal"](v, w)
        if k == "ascribe":
            return self.render(node[1], params)
        for _, pat, G, unit in self.keys:
            b = {}
            if match(pat, node, b):
                args = [self.render(b[v], params) for v in UNKNOWNS if v in b]
                self.used.append((G, unit))
                return self.plumb["call"](self.units[unit], args)
        text = to_lean(node)
        for G, (want, held) in self.narrow.items():     # a key exists, at holders that are not its operand widths: say so
            b = {}
            try:
                if match(LZ.parse(G), node, b):
                    raise Refusal("%s uses its reads at widths %s; the units that prove it are held at %s" % (
                        G, list(want), ", ".join(str(list(h)) for h in held)))
            except Refusal:
                raise
            except Exception:
                pass
        raise Refusal("no key of operator_for matches: %s" % text[:120])


def label_of(setting, others):
    """a name for a pure form specialized at an assignment of its non-register parameters:
    the values, each type prefix dropped. `one` when nothing was assigned."""
    parts = []
    for n, _ in others:
        v = setting.get(n)
        if v is None:
            continue
        parts += [x.split(".")[-1] for x in (list(field_values(v).values()) or [v])]
    return re.sub(r"\W+", "_", "_".join(parts)).strip("_")[:60] or "one"


def definitions_of(lean_dir, strip_rows):
    """[(clause, arm, tree over the reads, params [(name, kind)])]: every arm of every
    certified straight pure form, lets inlined.

    An arm is one value of an enumerated parameter. A `match` over that parameter gives the
    arms by its own branches; a pure form that instead READS the parameter (a Boolean flag,
    a field of a structure parameter) has exactly the same arms, one per value of the
    parameter's emitted type, and they are taken here by the same rule `operator_for` uses
    to build its candidates -- without it a definition whose operation is a flag has no arm
    at all and can never be rendered."""
    clauses = {c["name"][len("execute_"):]: c for c in ST.clauses_of(lean_dir)}
    out = []
    for name, r in strip_rows.items():
        if r.get("verdict") != "CERTIFIED" or r.get("shape") != "straight" or name not in clauses:
            continue
        p = ST.propose(clauses[name])
        reg_of = {v: reg for v, reg in p["reads"]}
        env = {}
        try:
            for ln, text in p.get("lets", []):
                env[ln.split(":")[0].strip()] = substitute(LZ.parse(text), env)
            root = substitute(LZ.parse(p["value"]), env)
        except Exception as ex:
            out.append((name, None, None, None, "the pure form did not parse: %s" % str(ex)[:80]))
            continue
        others = [(n, t) for n, t in p.get("others", [])]
        seen = set()
        settings = settings_of(lean_dir, others)
        if len(settings) > 1:
            settings = settings[1:]           # the free form is not an arm: its operation is unresolved
        for setting in settings:
            here = fold(substitute(root, {k: as_term(v) for k, v in setting.items()})) if setting else root
            left = [(n, t) for n, t in others if n not in setting]
            arms = here[2] if here[0] == "match" else [(label_of(setting, others), here)]
            for ctor, tree in arms:
                key = (ctor, re.sub(r"\s+", " ", to_lean(tree)))
                if key in seen:                 # a `match` gives the same arms at every assignment
                    continue
                seen.add(key)
                out.append((name, ctor, tree, {"reg_of": reg_of, "others": left}, None))
    return out


def cmd_render(argv, say, write_json):
    lean_dir, strip_json, table_json, corpus_json, out_dir = argv[:5]
    lang = argv[5] if len(argv) > 5 else "c"
    limit = int(argv[6]) if len(argv) > 6 else None
    os.makedirs(os.path.join(out_dir, "emulations"), exist_ok=True)
    strip_rows = {r["clause"][len("execute_"):]: r for r in json.load(open(strip_json))["rows"]}
    table = json.load(open(table_json))["table"]
    corpus = json.load(open(corpus_json))
    R = Renderer(table, corpus, lang)
    say("  operator_for keys usable in %s: %d (of %d filled; %d have no unit at the widths the key reads)" % (
        lang, len(R.keys), len(R.keys) + len(R.narrow), len(R.narrow)))
    for _, _, G, unit in sorted(R.keys, key=lambda t: t[2]):
        say("    at %-10s %s" % (str(R.widths_of.get(G)), G[:110]))
    rows, units = [], []
    for name, ctor, tree, info, problem in definitions_of(lean_dir, strip_rows):
        if problem:
            rows.append({"clause": name, "refused": problem}); continue
        label = "%s__%s" % (name, ctor)
        regs = []
        for v, reg in info["reg_of"].items():
            if reg not in regs:
                regs.append(reg)
        params = {v: UNKNOWNS[regs.index(reg)] for v, reg in info["reg_of"].items()}
        params.update({n: n for n, _ in info["others"]})           # an immediate or a flag arrives as a parameter too
        param_names = [UNKNOWNS[i] for i in range(len(regs))] + [n for n, _ in info["others"] if re.search(r"\b%s\b" % n, to_lean(tree))]
        R.used = []
        row = {"clause": name, "arm": ctor, "D": to_lean(tree), "params": param_names}
        try:
            body = R.render(tree, params)
        except Refusal as ex:
            row["refused"] = str(ex); rows.append(row)
            say("  %-28s REFUSED  %s" % (label, str(ex)[:80])); continue
        used_units = []
        for _, u in R.used:
            if u not in used_units:
                used_units.append(u)
        units_src = "\n".join(R.plumb["unit_source"](R.units[u], open(R.units[u]["source"]).read()) for u in used_units)
        symbol = "emu_%s" % re.sub(r"\W", "_", label)
        src = R.plumb["function"](symbol, param_names, body, units_src)
        path = os.path.join(out_dir, "emulations", "%s__%s.%s" % (label, lang, EXT[lang]))
        open(path, "w").write(src)
        row.update({"E": body, "path": path, "symbol": symbol,
                    "built_from": [{"subterm": G, "unit": u, "operand_widths": R.widths_of.get(G)} for G, u in R.used]})
        rows.append(row)
        units.append({"name": "%s__%s" % (label, lang), "lang": lang, "source": path, "symbol": symbol,
                      "flags": corpus[0]["flags"], "cell_display": "%s %s (%s)" % (name, ctor, lang), "definition": {"clause": name, "arm": ctor}})
        say("  %-28s %s" % (label, body[:90]))
        if limit and len(units) >= limit:
            break
    write_json(os.path.join(out_dir, "render.json"), {"rows": rows, "rendered": len(units), "refused": sum(1 for r in rows if "refused" in r)})
    write_json(os.path.join(out_dir, "units.json"), units)
    say("  render: %d emulations written, %d refused" % (len(units), sum(1 for r in rows if "refused" in r)))
    return 0
