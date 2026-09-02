#!/usr/bin/env python3
"""l3_accept.py -- phase 3 generator: the ACCEPTANCE space, fully enumerated.

Ruled design, CORE_0_3_2 "the layer-3 design -- RULED 2026-08-18":

  ruling 1  the probe operand is a layer-2 HOLDER; every row carries
            (form, holder, value class)
  ruling 2  FULL enumeration of ORDERED operand pairs -- no pruning rule
  ruling 3  full value matrix (that is the ANSWER grain, route C; this
            file builds the ACCEPTANCE grain, where a static language's
            verdict is a function of the holder pair and not of the
            value, so the value matrix multiplies answers and not
            verdicts)
  ruling 4  progress print-outs everywhere -- see progress.py
  ruling 5  routes A1/A2/B/C, per compiler assignment

What it emits
-------------
  space_<lang>.json      the enumerated probe space + its SIZE, printed
                         before anything runs
  lanes/ac_<lang>.sh     a self-contained lane carrying its own probes
                         and its own driver, because the runner cannot
                         see this repo

The operator menu is taken from the GRAMMAR's own positioned anonymous
tokens (kinds_<lang>.json), intersected with a candidate layer-3 binary
operation vocabulary.  Intersection is mechanical; nothing is added that
the grammar does not declare.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPS = os.path.join(HERE, "..", "data_representation")
sys.path.insert(0, HERE)
from progress import Progress, SH_PROGRESS      # noqa: E402

LANGS = ["go", "rust", "cpp", "swift", "dart", "csharp", "kotlin",
         "java", "typescript", "python", "ruby", "php"]

# candidate binary operations, intersected with each grammar's own
# positioned anonymous tokens.  Nothing here that a grammar does not
# declare survives the intersection.
COMMON = ["+", "-", "*", "/", "%", "<", "<=", ">", ">=", "==", "!=",
          "&", "|", "^", "<<", ">>", "&&", "||"]
EXTRA = {
    "python": ["//", "**", "and", "or", "in", "not in", "is", "is not", "@"],
    "ruby": ["**", "<=>", "=~", "==="],
    "php": [".", "**", "<=>", "===", "!==", "and", "or", "xor"],
    "dart": ["~/", "??"],
    "swift": ["??", "...", "..<"],
    "kotlin": ["..", "in", "?:"],
    "typescript": ["===", "!==", "**", "??", "in"],
    "csharp": ["??", "is"],
    "java": [">>>", "instanceof"],
    "go": ["&^"],
    "rust": [".."],
    "cpp": ["<=>"],
}

# per-language: how a probe program is spelled, and the CHECK route.
# route names are the CORE's: A1 in-process, A2 check-only invocation,
# C execution.
LANG = {
    "go": dict(ext="go", route="A2", cmd="go_build",
               head="package main\n\nimport \"fmt\"\n{PRE}\n\nfunc main() {\n",
               decl="\t{D}\n", body="\t_ = fmt.Sprint({A} {OP} {B})\n",
               tail="}\n"),
    "rust": dict(ext="rs", route="A2", cmd="rustc_metadata",
                 head="{PRE}\nfn main() {\n",
                 decl="    {D}\n",
                 body="    let _r = {A} {OP} {B};\n", tail="}\n"),
    "cpp": dict(ext="cpp", route="A2", cmd="gpp_syntax",
                head="{PRE}\nint main() {\n", decl="    {D}\n",
                body="    auto _r = ({A}) {OP} ({B}); (void)_r;\n",
                tail="    return 0;\n}\n"),
    "swift": dict(ext="swift", route="A2", cmd="swiftc_typecheck",
                  head="{PRE}\nfunc probe() {\n", decl="    {D}\n",
                  body="    let _r = ({A}) {OP} ({B})\n    _ = _r\n",
                  tail="}\n"),
    "dart": dict(ext="dart", route="A2", cmd="dart_analyze_dir",
                 head="{PRE}\nvoid probe{ID}() {\n", decl="  {D}\n",
                 body="  var _r = ({A}) {OP} ({B});\n  print(_r);\n",
                 tail="}\n"),
    "csharp": dict(ext="cs", route="A1", cmd="roslyn_inproc",
                   head="{PRE}\nclass C{ID} { void f() {\n",
                   decl="    {D}\n",
                   body="    var _r = ({A}) {OP} ({B});\n"
                        "    System.Console.WriteLine(_r);\n",
                   tail="} }\n"),
    "kotlin": dict(ext="kt", route="A1", cmd="kotlin_inproc",
                   head="{PRE}\nfun probe{ID}() {\n", decl="    {D}\n",
                   body="    val _r = ({A}) {OP} ({B})\n    println(_r)\n",
                   tail="}\n"),
    # java -- route A1, javax.tools / com.sun.source.util.JavacTask in
    # process.  The class is NOT public, so the in-memory file object's
    # name need not match; imports must precede the class, which is why
    # {PRE} sits at the head as it does everywhere else.
    "java": dict(ext="java", route="A1", cmd="javac_inproc",
                 head="{PRE}\nclass C{ID} { void f() {\n",
                 decl="    {D}\n",
                 body="    var _r = ({A}) {OP} ({B});\n"
                      "    System.out.println(_r);\n",
                 tail="} }\n"),
    # typescript -- route A1, the require-able checker inside the
    # shipped typescript.js.  Each probe is its own function in its own
    # file; the file is a script, not a module, so the function name
    # carries {ID} to keep the global scope collision-free.
    "typescript": dict(ext="ts", route="A1", cmd="ts_inproc",
                       head="{PRE}\nfunction probe{ID}() {\n",
                       decl="  {D}\n",
                       body="  let _r = ({A}) {OP} ({B});\n  return _r;\n",
                       # `export {};` makes every probe file a MODULE, so
                       # its top-level holder types are file-scoped.  All
                       # probes of a chunk live in ONE ts Program (that is
                       # what makes the checker cheap), and in a script
                       # file their `class Empty0` declarations would
                       # collide across files.  Mechanical, one line, and
                       # it changes no operand.
                       tail="}\nexport {};\n"),
}


# The layer-2 file carries holders in two shapes and both are used:
#   * SCALAR shape -- "decl" with a {V} hole, values from spell[form]
#     (with the holder's own spell_override on top)
#   * BUILT shape  -- "probes", a map from value class to a complete
#     declaration statement; the keys ARE the value classes
# Both are unified below into (value class -> declaration text).
#
# STATED DECISION, surfaced not buried (2026-08-18): the `identity`
# form's holders are EXCLUDED from the operand pairs.  Their probes are
# not operand builders -- each ends in a verdict word (log_024 decision
# 9, "identity atoms are hand-built").  Feeding them to an operator
# would measure the harness, not the operator.  This is a decision, it
# is not a ruling, and it is the cheapest one on this file to overturn.
EXCLUDE_FORMS = {"identity"}

BASE_ORDER = ("base_42", "base_hello", "base_1_5", "true", "null",
              "base_zero", "base_empty", "base", "flat", "seq_in_seq")


def holders(lang):
    """layer-2 holders, unified: each carries value class -> decl text."""
    p = os.path.join(REPS, "representations_%s.json" % lang)
    d = json.load(open(p))
    spell = d.get("spell", {})
    out = []
    for form, reps in d["forms"].items():
        if form in EXCLUDE_FORMS:
            continue
        for r in reps:
            vals = {}
            if "decl" in r:
                tab = dict(spell.get(form, {}))
                tab.update(r.get("spell_override", {}) or {})
                if not tab:
                    tab = {"spelling": r["spelling"]}
                for vc, txt in tab.items():
                    vals[vc] = r["decl"].replace("{V}", txt)
            elif "probes" in r:
                for vc, txt in r["probes"].items():
                    vals[vc] = txt
            if not vals:
                continue
            out.append(dict(form=form, rep=r["rep"], pre=r.get("pre", ""),
                            values=vals))
    return out, spell


def base_value(h, spell=None):
    """the value class a VERDICT probe carries.  In a statically checked
    language the verdict is a function of the holder pair; the value
    class multiplies ANSWERS (route C), not verdicts."""
    for k in BASE_ORDER:
        if k in h["values"]:
            return k, h["values"][k]
    k = sorted(h["values"])[0]
    return k, h["values"][k]


def ops(lang):
    p = os.path.join(HERE, "kinds_%s.json" % lang)
    k = json.load(open(p))
    have = set(k.get("anonymous", [])) | set(k.get("anonymous_positioned", []))
    cand = COMMON + EXTRA.get(lang, [])
    return [o for o in cand if o in have]


def rename(decl, new):
    return re.sub(r"\bv\b", new, decl)


# java carries two holders whose DECLARATION text declares a local type
# (`record R0() {} R0 v = new R0();`).  When such a holder is paired
# with ITSELF the same local type is declared twice in one method body,
# which java refuses -- a harness artifact, not a measurement, and the
# same shape as the php `Cannot redeclare class` fatal of log_027 5.1.
# The right-hand declaration's own declared type names are therefore
# suffixed, mechanically, by regular expression over the literal text.
# SURFACED, not buried: this is a harness decision, it touches java
# only, and it is reversible by deleting this function.
DECL_TYPE = re.compile(r"\b(?:record|class|interface|enum)\s+([A-Za-z_]\w*)")


def side_rename_types(decl, suffix):
    names = set(DECL_TYPE.findall(decl))
    for n in sorted(names, key=len, reverse=True):
        decl = re.sub(r"\b%s\b" % re.escape(n), n + suffix, decl)
    return decl


def build_space(lang):
    hs, spell = holders(lang)
    os_ = ops(lang)
    pairs = [(i, j) for i in range(len(hs)) for j in range(len(hs))]
    space = dict(
        language=lang,
        holders=[dict(i=n, form=h["form"], rep=h["rep"],
                      value_classes=sorted(h["values"]))
                 for n, h in enumerate(hs)],
        holder_count=len(hs),
        value_count=sum(len(h["values"]) for h in hs),
        operations=os_,
        operation_count=len(os_),
        ordered_pairs=len(pairs),
        acceptance_probes=len(pairs) * len(os_),
        value_matrix_answer_probes=sum(
            len(hs[i]["values"]) * len(hs[j]["values"]) for i, j in pairs
        ) * len(os_),
    )
    return hs, spell, os_, pairs, space


def gen_sources(lang, hs, spell, os_, pairs):
    """(probe id, source text) for every ordered pair x operation."""
    tpl = LANG[lang]
    out = []
    pg = Progress(len(pairs) * len(os_), "gen:%s" % lang, every=2000)
    n = 0
    for (i, j) in pairs:
        ha, hb = hs[i], hs[j]
        va = base_value(ha)
        vb = base_value(hb)
        da = rename(va[1], "a")
        db = rename(vb[1], "b")
        if lang == "java":
            db = side_rename_types(db, "_b")
        pres = []
        for h, dtext in ((ha, da), (hb, db)):
            pre = h.get("pre") or ""
            for line in pre.splitlines():
                line = line.strip()
                if not line:
                    continue
                m = re.findall(r"[A-Za-z_][A-Za-z_0-9]*", line)
                tok = m[-1] if m else ""
                if lang in ("go", "rust") and tok and tok not in dtext:
                    continue        # unused import is a refusal in go
                if line not in pres:
                    pres.append(line)
        for op in os_:
            pid = "P%d_%d_%d" % (i, j, os_.index(op))
            src = (tpl["head"].replace("{PRE}", "\n".join(pres))
                   .replace("{ID}", "%d_%d_%d" % (i, j, os_.index(op)))
                   + tpl["decl"].replace("{D}", da)
                   + tpl["decl"].replace("{D}", db)
                   + tpl["body"].replace("{A}", "a").replace("{B}", "b")
                                .replace("{OP}", op)
                   + tpl["tail"])
            out.append((pid, i, j, op, va[0], vb[0], src))
            n += 1
            pg.tick()
    pg.close()
    return out


def main():
    which = sys.argv[1:] or list(LANG)
    summary = {}
    for lang in which:
        if lang not in LANG:
            print("skip %s -- no acceptance template yet (route C only)" % lang)
            continue
        hs, spell, os_, pairs, space = build_space(lang)
        print("== %s: %d holders, %d operations, %d ordered pairs, "
              "%d acceptance probes; full value matrix would be "
              "%d answer probes"
              % (lang, space["holder_count"], space["operation_count"],
                 space["ordered_pairs"], space["acceptance_probes"],
                 space["value_matrix_answer_probes"]))
        json.dump(space, open(os.path.join(HERE, "space_%s.json" % lang), "w"),
                  indent=1)
        srcs = gen_sources(lang, hs, spell, os_, pairs)
        with open(os.path.join(HERE, "probes_ac_%s.jsonl" % lang), "w") as f:
            for pid, i, j, op, vca, vcb, src in srcs:
                f.write(json.dumps(dict(id=pid, lhs=i, rhs=j, op=op,
                                        vclass_lhs=vca, vclass_rhs=vcb,
                                        src=src)) + "\n")
        summary[lang] = space
    json.dump(summary, open(os.path.join(HERE, "space_summary.json"), "w"),
              indent=1)
    print("\n| language | holders | operations | ordered pairs | "
          "acceptance probes | full value-matrix answer probes |")
    print("|---|---|---|---|---|---|")
    for lang, s in summary.items():
        print("| %s | %d | %d | %d | %d | %d |"
              % (lang, s["holder_count"], s["operation_count"],
                 s["ordered_pairs"], s["acceptance_probes"],
                 s["value_matrix_answer_probes"]))


if __name__ == "__main__":
    main()
