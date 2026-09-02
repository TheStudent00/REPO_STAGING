#!/usr/bin/env python3
"""l3_answers12.py -- layer 3 phase 4, the ANSWER GRAIN for ALL TWELVE.

Log 031 clustered the three print-grain languages (python, ruby, php)
on their computed values.  Log 032 executed the nine statically checked
languages and recorded their answers as BITS.  This pass joins the two:
one canonical token space, one distance rule, one dendrogram, twelve
languages, domains AND computed values together.

The bridge between the two encodings is decisions 31 to 42 and it lives
in `l3_answers.py' beside decisions 18 to 30, so that the canonicalizing
rules of the three and the bridging rules of the nine are read in one
place and overturned in one place.

Run:  python3 l3_answers12.py     -> clusters_all12.json
      python3 make_dendrogram_all12.py  -> dendrogram_all12.html

`l3_answers.py' run as a script is untouched and still reproduces
log 031's three-language result.
"""

import itertools
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from l3_final import merge_history, count_at, clusters_at, plateaus   # noqa
from l3_cluster import bar, FORMS                                     # noqa
from l3_answers import (DECISIONS, BRIDGE_DECISIONS, NINE, THREE,     # noqa
                        LANGS12, VOID, bridge_row, canon_pair)
from l3_wordops import ADMIT as WORD_ADMIT               # decision 43

SHARED = [(a, b) for a in FORMS for b in FORMS]


# --------------------------------------------------------------------
# loading -- one record shape for both encodings
# --------------------------------------------------------------------
#
# per operation:
#   dom       set of (form_a, form_b) with at least one VALUE answer
#             (decision 32)
#   pairs     set of (form_a, form_b) probed at all
#   inx       input cell -> set of EXACT tokens
#   ins       input cell -> set of SHADOW tokens   (decision 34)
#   raws      input cell -> [(token, holder_a, holder_b), ...]
#   n_value   value answers, n_raise, n_death, n_refuse
#
# an input cell is the string "form_a|vc_a|form_b|vc_b" (decision 18).

VALUE_KINDS = ("nothing", "truth", "whole", "fractional", "text",
               "sequence", "keyed", "ord", "enum", "range", "opaque")


def _blank():
    return dict(dom=set(), pairs=set(), inx={}, ins={}, raws={},
                n_value=0, n_raise=0, n_death=0, n_refuse=0)


def load_three(lang):
    man = json.load(open(os.path.join(HERE, "manifest_%s.json" % lang)))
    beh = json.load(open(os.path.join(HERE, "behavior_%s_C.json" % lang)))
    assert beh.get("complete"), "%s route-C table not complete" % lang
    hs = man["holders"]
    cells = beh["cells"]
    # DECISION 43, log 035.  The manifests are FROZEN, and they were
    # frozen before the word-spelled operations were admitted, so
    # `man["operations"]' does not carry ruby's `and'/`or' or php's
    # `instanceof' even though `rc_ruby2'/`rc_php2' measured them and
    # `behavior_<lang>_C.json' holds their cells.  Iterating the frozen
    # list alone silently dropped three leaves on the first re-fold.
    #
    # The admitted list is APPENDED here rather than the manifests
    # rebuilt: a manifest is a frozen record of what was probed under a
    # given plan, and re-freezing it to fix a reader would destroy the
    # thing it exists to preserve.  Holders and value classes are not
    # affected by the operation list, so the append is sound.
    ops3 = list(man["operations"]) + [
        o for o in WORD_ADMIT.get(lang, []) if o not in man["operations"]]
    per = {}
    alphabet = {}
    vocab = {}
    t0 = time.time()
    for n, ha in enumerate(hs):
        for h in (ha,):
            vocab.setdefault(h["form"], set()).update(
                x[0] for x in h["value_classes"])
        for hb in hs:
            i, j = ha["i"], hb["i"]
            for vca, _ in ha["value_classes"]:
                for vcb, _ in hb["value_classes"]:
                    for op in ops3:
                        c = cells.get("P%d_%d_%s_%s_%s"
                                      % (i, j, vca, vcb, op))
                        if c is None:
                            continue
                        rec = per.setdefault(op, _blank())
                        fp = (ha["form"], hb["form"])
                        rec["pairs"].add(fp)
                        if c[0] == "ANSWER":
                            tok, sh = canon_pair(c[1])
                            raw = c[1]
                            rec["dom"].add(fp)
                            rec["n_value"] += 1
                        elif c[0] == "RAISE":            # DECISION 31
                            tok = sh = "raise:" + str(c[1])
                            raw = "RAISE:" + str(c[1])
                            rec["n_raise"] += 1
                        else:
                            continue                    # BUDGET, not an answer
                        alphabet.setdefault(tok, {})
                        alphabet[tok][raw] = alphabet[tok].get(raw, 0) + 1
                        key = "%s|%s|%s|%s" % (ha["form"], vca,
                                               hb["form"], vcb)
                        rec["inx"].setdefault(key, set()).add(tok)
                        rec["ins"].setdefault(key, set()).add(sh)
                        rec["raws"].setdefault(key, []).append(
                            (tok, ha["holder"], hb["holder"]))
        bar(n + 1, len(hs), t0, "%s (print grain)" % lang)
    print()
    return dict(language=lang, per=per, alphabet=alphabet,
                vocab={f: sorted(s) for f, s in sorted(vocab.items())},
                grain="print", probes=beh["probes"])


def load_nine(lang):
    d = json.load(open(os.path.join(HERE, "answers_%s.json" % lang)))
    assert d.get("complete"), "%s execution table not complete" % lang
    per = {}
    alphabet = {}
    vocab = {}
    t0 = time.time()
    rows = d["rows"]
    for n, r in enumerate(rows):
        la, rb = r["lhs"], r["rhs"]
        vocab.setdefault(la["form"], set()).add(la["value"])
        vocab.setdefault(rb["form"], set()).add(rb["value"])
        rec = per.setdefault(r["operation"], _blank())
        fp = (la["form"], rb["form"])
        rec["pairs"].add(fp)
        b = bridge_row(r)
        if b is None:                                    # DECISION 40
            rec["n_refuse"] += 1
            continue
        tok, sh, raw = b
        if r["outcome"] == "answer":
            rec["dom"].add(fp)                           # DECISION 32
            rec["n_value"] += 1
        elif r["outcome"] == "raise":
            rec["n_raise"] += 1
        else:
            rec["n_death"] += 1
        alphabet.setdefault(tok, {})
        alphabet[tok][raw] = alphabet[tok].get(raw, 0) + 1
        key = "%s|%s|%s|%s" % (la["form"], la["value"],
                               rb["form"], rb["value"])
        rec["inx"].setdefault(key, set()).add(tok)
        rec["ins"].setdefault(key, set()).add(sh)
        rec["raws"].setdefault(key, []).append(
            (tok, la["holder"], rb["holder"]))
        if (n + 1) % 4000 == 0:
            bar(n + 1, len(rows), t0, "%s (bit grain)" % lang)
    bar(len(rows), len(rows), t0, "%s (bit grain)" % lang)
    print()
    return dict(language=lang, per=per, alphabet=alphabet,
                vocab={f: sorted(s) for f, s in sorted(vocab.items())},
                grain="bit", probes=d["probes"])


# --------------------------------------------------------------------
# signatures
# --------------------------------------------------------------------

def signatures(L):
    out = {}
    for op, rec in L["per"].items():
        if not rec["pairs"]:
            continue
        dom = sorted(rec["dom"])
        per_cell = {}
        for key, toks in rec["inx"].items():
            fa, _, fb, _ = key.split("|")
            per_cell.setdefault((fa, fb), {})
            for t in toks:
                per_cell[(fa, fb)][t] = per_cell[(fa, fb)].get(t, 0) + 1
        answer_classes = {}
        for k in dom:
            dd = per_cell.get(k, {})
            kinds = {}
            for t, c in dd.items():
                kinds[t.split(":", 1)[0]] = kinds.get(
                    t.split(":", 1)[0], 0) + c
            answer_classes["%s|%s" % k] = dict(
                tokens=len(dd),
                shape="uniform" if len(dd) == 1 else "split",
                kinds=sorted(kinds, key=lambda x: -kinds[x]),
                top=sorted(dd, key=lambda t: -dd[t])[:4])
        n_split = sum(1 for v in rec["inx"].values() if len(v) > 1)
        out["%s.%s" % (L["language"], op)] = dict(
            language=L["language"], operation=op,
            route="C answers (%s grain)" % L["grain"],
            grain=L["grain"],
            domain=["%s|%s" % k for k in dom],
            form_pairs_probed=len(rec["pairs"]),
            input_cells=len(rec["inx"]),
            input_cells_split=n_split,
            split_rate=(round(n_split / len(rec["inx"]), 4)
                        if rec["inx"] else None),
            value_answers=rec["n_value"], raises=rec["n_raise"],
            deaths=rec["n_death"], codegen_refuse=rec["n_refuse"],
            answer_classes=answer_classes)
    return out


# --------------------------------------------------------------------
# distance -- DECISION 27, with DECISION 34's precision rule
# --------------------------------------------------------------------

def sim_pair(ia, ib, da, db, exact):
    A, B = set(da), set(db)
    u = A | B
    j = (len(A & B) / len(u)) if u else 0.0
    shared = set(ia) & set(ib)
    if not shared:
        return j, j, None, 0, 0
    agree = 0
    for k in shared:
        if ia[k] & ib[k]:
            agree += 1
    a = agree / len(shared)
    return j * a, j, a, len(shared), agree


def main():
    print("layer 3 phase 4 -- ANSWER GRAIN, ALL TWELVE LANGUAGES")
    Ls = {}
    for lang in THREE:
        Ls[lang] = load_three(lang)
    for lang in NINE:
        Ls[lang] = load_nine(lang)

    # ---------------------------------------- DECISION 41, the vocabulary
    ref = Ls["python"]["vocab"]
    vocab_report = {}
    contained = True
    for lang, L in Ls.items():
        extra = {f: sorted(set(v) - set(ref.get(f, [])))
                 for f, v in L["vocab"].items()}
        extra = {f: v for f, v in extra.items() if v}
        missing = {f: sorted(set(ref.get(f, [])) - set(v))
                   for f, v in L["vocab"].items()}
        missing = {f: v for f, v in missing.items() if v}
        absent_forms = sorted(set(ref) - set(L["vocab"]))
        if extra:
            contained = False
        vocab_report[lang] = dict(vocab=L["vocab"], invents=extra,
                                  lacks=missing, forms_absent=absent_forms)

    sigs = {}
    inx = {}
    ins = {}
    langof = {}
    for lang, L in Ls.items():
        sigs.update(signatures(L))
        for op, rec in L["per"].items():
            k = "%s.%s" % (lang, op)
            inx[k] = rec["inx"]
            ins[k] = rec["ins"]
            langof[k] = lang

    for k, why in VOID.items():                          # DECISION 30
        if k in sigs:
            sigs[k]["void"] = why
    keys = sorted(k for k in sigs if sigs[k]["domain"] and k not in VOID)
    empty = sorted(k for k in sigs if not sigs[k]["domain"])
    print("  %d signatures, %d leaves with a non-empty domain, %d empty"
          % (len(sigs), len(keys), len(empty)))

    # ------------------------------------------------------------- edges
    sim = {}
    edge = {}
    fp_shadow_edges = 0
    fp_lost_cells = 0
    fp_lost_edges = 0
    t0 = time.time()
    n = 0
    total = len(keys) * (len(keys) - 1) // 2
    for a, b in itertools.combinations(keys, 2):
        exact = langof[a] in NINE and langof[b] in NINE   # DECISION 34
        ia, ib = (inx[a], inx[b]) if exact else (ins[a], ins[b])
        s, j, ag, sh, agn = sim_pair(ia, ib, sigs[a]["domain"],
                                     sigs[b]["domain"], exact)
        if not exact and sh:
            fp_shadow_edges += 1
        if exact and sh:
            # how many cells the 14-digit shadow would have merged
            shared = set(inx[a]) & set(inx[b])
            lost = sum(1 for k in shared
                       if not (inx[a][k] & inx[b][k])
                       and (ins[a][k] & ins[b][k]))
            if lost:
                fp_lost_cells += lost
                fp_lost_edges += 1
        sim[(a, b)] = sim[(b, a)] = s
        edge[(a, b)] = dict(similarity=round(s, 6), jaccard=round(j, 6),
                            agreement=(round(ag, 6) if ag is not None
                                       else None),
                            shared_inputs=sh,
                            precision="exact" if exact else "14-digit")
        n += 1
        if n % 2000 == 0:
            bar(n, total, t0, "pairs")
    bar(total, total, t0, "pairs")
    print()

    merges, members = merge_history(keys, sim)
    curve = [dict(threshold=round(t / 100.0, 2),
                  clusters=count_at(merges, len(keys), t / 100.0))
             for t in range(0, 101)]
    plat = plateaus(merges, len(keys))
    snaps = {}
    for p in plat[:8]:
        t = (p["low"] + p["high"]) / 2.0
        snaps["%.3f-%.3f" % (p["low"], p["high"])] = dict(
            clusters=clusters_at(keys, merges, members, t),
            count=p["clusters"], width=p["width"])

    # ------------------------- CONTROL: the same leaves, domain J alone
    simJ = {}
    for (a, b), e in edge.items():
        simJ[(a, b)] = simJ[(b, a)] = e["jaccard"]
    cmerges, cmembers = merge_history(keys, simJ)
    ccurve = [dict(threshold=round(t / 100.0, 2),
                   clusters=count_at(cmerges, len(keys), t / 100.0))
              for t in range(0, 101)]
    cplat = plateaus(cmerges, len(keys))
    ags = sorted(e["agreement"] for e in edge.values()
                 if e["agreement"] is not None)
    control = dict(
        cluster_count_curve=ccurve, stability_plateaus=cplat[:12],
        widest_plateau="[%.3f, %.3f)" % (cplat[0]["low"], cplat[0]["high"]),
        widest_plateau_clusters=clusters_at(
            keys, cmerges, cmembers,
            (cplat[0]["low"] + cplat[0]["high"]) / 2.0),
        edges_with_agreement=len(ags),
        edges_domain_only=sum(1 for e in edge.values()
                              if e["agreement"] is None),
        agreement_median=round(ags[len(ags) // 2], 4) if ags else None,
        agreement_is_1=sum(1 for a in ags if a == 1.0),
        agreement_is_0=sum(1 for a in ags if a == 0.0))

    coarse = {}
    for lo, hi in ((0.0, 0.1), (0.1, 0.2), (0.2, 0.4), (0.4, 0.6),
                   (0.6, 0.8)):
        cand = [p for p in plat if lo <= p["low"] < hi]
        if not cand:
            continue
        p = cand[0]
        gs = clusters_at(keys, merges, members,
                         (p["low"] + p["high"]) / 2.0)
        coarse["%.3f-%.3f" % (p["low"], p["high"])] = dict(
            count=p["clusters"], width=p["width"],
            clusters=[dict(size=len(g), members=g,
                           languages=sorted({m.split(".")[0] for m in g}),
                           spellings=sorted({m.split(".", 1)[1] for m in g}))
                      for g in sorted(gs, key=len, reverse=True)])

    # ------------------------------------ same spelling, and contradicts
    spell = {}
    contra = []
    partial = []
    agree_zero = []
    for a, b in itertools.combinations(keys, 2):
        la, oa = sigs[a]["language"], sigs[a]["operation"]
        lb, ob = sigs[b]["language"], sigs[b]["operation"]
        if la == lb or oa != ob:
            continue
        exact = la in NINE and lb in NINE
        ia, ib = (inx[a], inx[b]) if exact else (ins[a], ins[b])
        sh = sorted(set(ia) & set(ib))
        if not sh:
            continue
        dis = [k for k in sh if not (ia[k] & ib[k])]
        rate = round((len(sh) - len(dis)) / len(sh), 4)
        spell.setdefault(oa, {})["%s vs %s" % (la, lb)] = dict(
            shared_inputs=len(sh), agree=len(sh) - len(dis), rate=rate,
            divide=("open|open" if la in THREE and lb in THREE else
                    "static|static" if la in NINE and lb in NINE else
                    "static|open"))
        rec = dict(a=a, b=b, shared_inputs=len(sh), disagreeing=len(dis),
                   rate=round(len(dis) / len(sh), 4),
                   divide=spell[oa]["%s vs %s" % (la, lb)]["divide"],
                   examples=dis[:6])
        if dis and len(dis) == len(sh):
            rec["kind"] = "contradicts_total"
            contra.append(rec)
        elif dis:
            rec["kind"] = "contradicts_partial"
            partial.append(rec)
        else:
            agree_zero.append(dict(a=a, b=b, shared_inputs=len(sh),
                                   divide=rec["divide"]))
    contra.sort(key=lambda r: -r["shared_inputs"])
    partial.sort(key=lambda r: -r["disagreeing"])
    agree_zero.sort(key=lambda r: -r["shared_inputs"])

    by_divide = {}
    for r in contra + partial + [dict(divide=z["divide"], disagreeing=0,
                                      shared_inputs=z["shared_inputs"],
                                      rate=0.0) for z in agree_zero]:
        d = by_divide.setdefault(r["divide"], dict(pairs=0,
                                                  disagree_some=0,
                                                  disagree_all=0,
                                                  cells=0, dis_cells=0))
        d["pairs"] += 1
        d["cells"] += r["shared_inputs"]
        d["dis_cells"] += r["disagreeing"]
        if r["disagreeing"]:
            d["disagree_some"] += 1
        if r["disagreeing"] and r["disagreeing"] == r["shared_inputs"]:
            d["disagree_all"] += 1
    for d in by_divide.values():
        d["cell_disagreement_rate"] = (round(d["dis_cells"] / d["cells"], 4)
                                       if d["cells"] else None)

    # ---- two readable roll-ups of the 974 same-spelling pairs.  The
    # raw table is unreadable at twelve languages, so it is summarised
    # twice and the raw stays in `spelling_agreement'.
    smat = {}
    for op, pairs in spell.items():
        for name, v in pairs.items():
            la, lb = name.split(" vs ")
            for x, y in ((la, lb), (lb, la)):
                c = smat.setdefault(x, {}).setdefault(
                    y, dict(ops=0, cells=0, agree=0))
                c["ops"] += 1
                c["cells"] += v["shared_inputs"]
                c["agree"] += v["agree"]
    for x in smat:
        for y in smat[x]:
            c = smat[x][y]
            c["rate"] = round(c["agree"] / c["cells"], 4) if c["cells"] else None
    sops = {}
    for op, pairs in spell.items():
        rs = sorted((v["rate"], k) for k, v in pairs.items())
        cells = sum(v["shared_inputs"] for v in pairs.values())
        agree = sum(v["agree"] for v in pairs.values())
        sops[op] = dict(pairs=len(rs), cells=cells,
                        rate=round(agree / cells, 4) if cells else None,
                        lowest=rs[0][1], lowest_rate=rs[0][0],
                        highest=rs[-1][1], highest_rate=rs[-1][0],
                        median=rs[len(rs) // 2][0])

    # --------------------------------------------------- worked examples
    def raws(lang, op, key):
        rec = Ls[lang]["per"].get(op)
        if not rec:
            return None
        d = rec["raws"].get(key)
        if not d:
            return None
        seen = {}
        for tok, ha, hb in d:
            seen.setdefault(tok, []).append("%s %s %s" % (ha, op, hb))
        return [dict(token=t, holders=v[0], holder_pairs=len(v))
                for t, v in sorted(seen.items())]

    NAMED = [
        ("+", "whole|i64max|whole|base_42", "int overflow at 2^63-1"),
        ("+", "whole|u64max|whole|base_42", "int overflow at 2^64-1"),
        ("+", "whole|p53_plus1|whole|base_42", "2^53+1"),
        ("<<", "whole|base_42|whole|base_42", "42 << 42"),
        ("/", "whole|base_42|whole|base_zero", "42 / 0"),
        ("%", "whole|base_42|whole|base_zero", "42 % 0"),
        ("+", "fractional|base_pi|fractional|base_pi", "pi + pi"),
        ("+", "fractional|negzero|fractional|negzero", "-0.0 + -0.0"),
        ("+", "fractional|nan|fractional|nan", "nan + nan"),
        ("==", "fractional|nan|fractional|nan", "nan == nan"),
        ("+", "text|eacute|text|base_hello", "e-acute concatenation"),
        ("==", "text|eacute|text|eacute", "e-acute equality"),
        ("+", "sequence|base|sequence|strs", "sequence + sequence"),
        ("==", "truth|true|whole|base_42", "true == 42"),
        ("&", "truth|true|whole|base_42", "true & 42"),
        ("+", "truth|true|whole|base_42", "true + 42"),
        ("+", "whole|base_42|text|base_hello", "42 + 'hello'"),
        ("<", "fractional|inf|fractional|nan", "inf < nan"),
        ("*", "whole|i64max|whole|base_42", "i64max * 42"),
    ]
    worked = []
    for op, key, label in NAMED:
        row = dict(label=label, operation=op, input_cell=key,
                   per_language={})
        for lang in LANGS12:
            r = raws(lang, op, key)
            if r is not None:
                row["per_language"][lang] = r
        toks = {l: sorted(set(x["token"] for x in v))
                for l, v in row["per_language"].items()}
        row["tokens"] = toks
        ls = [l for l in toks if toks[l]]
        row["languages"] = len(ls)
        row["distinct_answers"] = len({tuple(toks[l]) for l in ls})
        row["all_agree"] = (len(ls) > 1 and bool(
            set.intersection(*[set(toks[l]) for l in ls])))
        worked.append(row)

    # ------------------------------------------------ the bridge merges
    allraw = {}
    for lang, L in Ls.items():
        for tok, d in L["alphabet"].items():
            for raw, c in d.items():
                allraw.setdefault(tok, {}).setdefault(lang, {})
                allraw[tok][lang][raw] = allraw[tok][lang].get(raw, 0) + c
    bridge_merges = []
    canon_merges = []
    for tok, per_l in allraw.items():
        pr = sorted({r for lang in per_l if lang in THREE
                     for r in per_l[lang]})
        bt = sorted({r for lang in per_l if lang in NINE
                     for r in per_l[lang]})
        n_probes = sum(sum(d.values()) for d in per_l.values())
        if pr and bt:
            bridge_merges.append(dict(
                token=tok, print_pre=pr[:4], bit_pre=bt[:4],
                n_print_pre=len(pr), n_bit_pre=len(bt),
                languages=sorted(per_l), probes=n_probes))
        if len(pr) + len(bt) > 1:
            canon_merges.append(dict(token=tok, n_pre=len(pr) + len(bt),
                                     pre_canonical=(pr + bt)[:8],
                                     languages=sorted(per_l),
                                     probes=n_probes))
    bridge_merges.sort(key=lambda r: -r["probes"])
    canon_merges.sort(key=lambda r: -r["probes"])

    container_meets = 0
    for r in bridge_merges:
        if r["token"].split(":", 1)[0] in ("sequence", "keyed"):
            container_meets += 1

    # ----------------------------------------------------- the stories
    def cluster_of(gs, leaf):
        for g in gs:
            if leaf in g:
                return g
        return []

    widest = plat[0]
    gs_widest = clusters_at(keys, merges, members,
                            (widest["low"] + widest["high"]) / 2.0)
    stories = {}
    for name, leaf in (("plus_python", "python.+"), ("plus_go", "go.+"),
                       ("plus_php", "php.+"), ("plus_ts", "typescript.+"),
                       ("div_dart", "dart./"), ("div_go", "go./"),
                       ("shl_go", "go.<<"), ("shl_java", "java.<<"),
                       ("add_rust", "rust.+")):
        if leaf in keys:
            stories[name] = dict(leaf=leaf,
                                 cluster=sorted(cluster_of(gs_widest, leaf)))

    # wrap-versus-panic: the i64max + 42 cell, token by token
    wrap = {}
    for lang in LANGS12:
        r = raws(lang, "+", "whole|i64max|whole|base_42")
        if r:
            wrap[lang] = sorted({x["token"] for x in r})

    out = dict(
        status="ANSWER-GRAIN, ALL TWELVE",
        extends=["clusters_answers.json", "clusters_final.json"],
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        scope="the answer half of phase 4 for all twelve languages: the "
              "three print-grain route-C languages of log 031 and the "
              "nine bit-grain execution languages of log 032, bridged "
              "into one canonical token space by decisions 31 to 42 and "
              "clustered on decision 27's combined distance.",
        languages={l: dict(probes=Ls[l]["probes"], grain=Ls[l]["grain"])
                   for l in LANGS12},
        value_class_vocabulary=vocab_report,
        value_class_vocabulary_contained=contained,
        forms=FORMS, shared_space_cells=len(SHARED),
        decisions=[dict(n=n_, text=t) for n_, t in
                   sorted(DECISIONS, key=lambda x: int(x[0]))],
        bridge_decisions=[dict(n=n_, text=t) for n_, t in
                          BRIDGE_DECISIONS],
        answer_alphabet={l: {t: d for t, d in
                             sorted(Ls[l]["alphabet"].items())}
                         for l in LANGS12},
        bridge_merges=bridge_merges[:200],
        bridge_merges_total=len(bridge_merges),
        bridge_container_meets=container_meets,
        canon_merges=canon_merges[:120],
        canon_merges_total=len(canon_merges),
        float_precision=dict(
            edges_using_14_digit_shadow=fp_shadow_edges,
            exact_edges_where_shadow_would_merge=fp_lost_edges,
            cells_shadow_would_merge=fp_lost_cells),
        signatures=sigs, empty_domain=empty, void_signatures=VOID,
        n_leaves=len(keys),
        edges={"%s :: %s" % k: v for k, v in sorted(edge.items())},
        merge_history=merges,
        cluster_count_curve=curve,
        stability_plateaus=plat,
        cluster_snapshots=snaps,
        coarse_readings=coarse,
        control_domain_only=control,
        spelling_agreement=spell,
        spelling_matrix=smat,
        spelling_by_operation=sops,
        contradicts=contra,
        contradicts_partial=partial,
        agrees_everywhere=agree_zero,
        contradicts_counts=dict(total=len(contra), partial=len(partial),
                                zero=len(agree_zero),
                                pairs=len(contra) + len(partial)
                                + len(agree_zero)),
        contradicts_by_divide=by_divide,
        worked_examples=worked,
        stories=stories,
        wrap_vs_panic=wrap,
    )
    p = os.path.join(HERE, "clusters_all12.json")
    json.dump(out, open(p, "w"), indent=1, default=str)
    print("  wrote %s (%.1f MB)" % (p, os.path.getsize(p) / 1e6))
    print("  leaves %d | contradicts total %d | partial %d | zero %d"
          % (len(keys), len(contra), len(partial), len(agree_zero)))
    print("  widest plateau [%.3f, %.3f) -> %d clusters"
          % (plat[0]["low"], plat[0]["high"], plat[0]["clusters"]))
    print("  control widest %s -> %d"
          % (control["widest_plateau"], cplat[0]["clusters"]))


if __name__ == "__main__":
    main()
