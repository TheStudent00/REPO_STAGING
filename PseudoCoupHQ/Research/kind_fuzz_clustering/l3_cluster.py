#!/usr/bin/env python3
"""l3_cluster.py -- PRELIMINARY phase-4 clustering.

Layer 3 phase 4, job 2.  Everything this file emits is PRELIMINARY: it
runs over the data that is ALREADY COMPLETE -- the nine acceptance grids
and the three route-C behavior tables -- and not over the full value
matrix, whose kotlin, cpp, go and swift shards are still running.

The CORE's phase 4 asks for comparison by RELATION over the pair
{domain accepted, answer per input}, with the trichotomy nests /
overlaps / contradicts.  That is what this builds.

Every methodological choice is NUMBERED in DECISIONS below and every one
is overturnable; they are stated so the owner can overturn them individually
rather than having to reject the whole pass.
"""

import itertools
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from l3_accept import holders, ops                    # noqa: E402

STATIC = ["go", "rust", "cpp", "swift", "dart", "csharp", "kotlin",
          "java", "typescript"]
DYNAMIC = ["python", "ruby", "php"]
ALL = STATIC + DYNAMIC
FORMS = ["nothing", "truth", "whole", "fractional", "text", "sequence",
         "keyed", "nesting"]
SHARED = [(a, b) for a in FORMS for b in FORMS]      # 64 ordered form pairs

DECISIONS = [
    ("1", "HOLDER-TO-FORM PROJECTION.  A language's acceptance grid is at "
     "holder grain, and two languages do not share holders, so nothing can "
     "be compared until both are projected onto the layer-1 forms they DO "
     "share.  Every holder is replaced by its form and a domain becomes a "
     "set of ordered FORM pairs.  All twelve languages carry all eight "
     "forms, so the shared space is the same 64 ordered pairs for every "
     "language pair -- no pair-specific restriction is needed.  Overturnable: "
     "the projection is lossy exactly where CORE ruling 1 said it would be "
     "(Decimal(42) + Fraction(42) raises though both hold one form), so a "
     "holder-grain comparison remains available for language pairs that "
     "have a holder correspondence."),
    ("2", "EXISTENTIAL PROJECTION RULE.  A projected form-pair cell counts "
     "as ACCEPTED if AT LEAST ONE holder pair with those forms was accepted. "
     "Rationale: the question a domain answers is `can this operation take "
     "these forms at all', which is existential.  The alternatives -- "
     "universal (all holder pairs accept) and majority -- are computed and "
     "stored alongside as `density` so overturning this costs a re-read and "
     "not a re-run."),
    ("3", "ROUTE-C DOMAIN RULE.  For python, ruby and php acceptance does "
     "not exist as a separate verdict; execution is the only evidence "
     "(CORE ruling 5, route C).  A cell counts as ACCEPTED there if at "
     "least one probe returned ANSWER.  RAISE, REFUSE and BUDGET all count "
     "as not-accepted.  Overturnable: RAISE is arguably `accepted then "
     "failed', which would widen these three domains."),
    ("4", "SIMILARITY MEASURE.  Jaccard on the ACCEPT sets over the 64 "
     "shared form pairs: |A and B| / |A or B|.  Chosen because it ignores "
     "the enormous agreed-REFUSE background that would make every pair of "
     "operations look ~90 percent alike under plain agreement.  An "
     "operation with an EMPTY domain is excluded from clustering entirely "
     "rather than being scored 0 against everything."),
    ("5", "CLUSTER CUT.  Average-linkage agglomerative over 1 - Jaccard, "
     "cut at similarity 0.70.  The 0.85 cut is computed too and reported "
     "beside it, because the honest thing to show is how much the picture "
     "moves with the threshold.  Nothing in the data picks 0.70; it is a "
     "reading choice."),
    ("6", "RELATIONS.  Over the shared space: NESTS if one accept set "
     "strictly contains the other and the contained one is non-empty; "
     "OVERLAPS if they intersect and neither contains the other; "
     "CONTRADICTS is reserved for the SAME SPELLED operation in two "
     "languages whose accept sets are disjoint while both are non-empty. "
     "Overturnable: `contradicts' in the CORE is defined at the answer "
     "grain (same input, different answer) and only three languages have "
     "answers, so this is the acceptance-grain reading of it and is "
     "labelled as such."),
    ("7", "THE MIXED-HOLDER STATISTIC IS COMPUTED, NEVER ASSERTED.  The "
     "shift exemption is a claim about HOLDERS, which the form projection "
     "destroys, so a second statistic is measured at holder grain: among "
     "accepted probes whose two holders share one form, the fraction whose "
     "holders DIFFER.  No operation and no language is named in the code "
     "that computes it.  Whether the shifts separate out is then an "
     "observation about the data, not a restatement of the input."),
    ("8", "PRELIMINARY SCOPE, AND THE COMPLETENESS GATE.  Only completed "
     "artifacts are read.  The nine acceptance grids and the three route-C "
     "behavior tables are complete and are read in full.  A value matrix is "
     "read ONLY if its own `complete` field is true -- the gate, not the "
     "file's existence, decides.  Reading a part-finished lane would produce "
     "a domain that shrinks for a reason that is not a fact about the "
     "language, which is the error this gate exists to prevent.  At this "
     "pass SEVEN matrices pass the gate (typescript, csharp, java, rust, "
     "go, swift, kotlin -- kotlin's sixth and last shard landed during "
     "this session) and two do not: cpp, which had not started, and dart, "
     "whose second shard was never queued at all, a gap rather than a "
     "wait."),
    ("9", "THE VALUE MATRIX IS AN OVERLAY, NOT THE PRIMARY DOMAIN.  The "
     "clustering proper runs on the acceptance grids for ALL TWELVE "
     "languages.  It would be a measurement artifact to widen six languages' "
     "domains with value-matrix evidence and not the other six: every "
     "cross-language similarity involving a gated language would then move "
     "for a reason about WHICH LANE FINISHED rather than about the "
     "languages.  So the matrices are read as a separate overlay and "
     "reported as a delta.  Overturnable when all nine matrices land, at "
     "which point the overlay should simply BECOME the primary domain for "
     "the nine statically checked languages."),
    ("10", "OVERLAY RULE, EXISTENTIAL OVER VALUES.  In an admitted matrix a "
     "(operation, lhs holder, rhs holder) cell counts as accepted if AT "
     "LEAST ONE value combination accepted -- the same existential posture "
     "as decision 2, one layer down.  A `split` cell (verdict moved with the "
     "VALUE, not the holder pair) therefore counts as accepted.  This is the "
     "widest reading and it is chosen deliberately, because the overlay's "
     "job here is to BOUND how wrong the one-value-per-holder acceptance "
     "grid could be, and a bound wants the extreme."),
    ("11", "THE OVERLAY MEASURES THE GRID'S ERROR.  For each admitted "
     "language the count of cells where the grid and the existential "
     "overlay disagree is reported.  That number is the honest error bar on "
     "every domain in this pass, including the domains of the six languages "
     "that have no matrix yet -- there is no reason to think their grids are "
     "better behaved than the measured ones."),
]


def bar(done, total, t0, what):
    el = time.time() - t0
    eta = (el / done * (total - done)) if done else 0.0
    sys.stdout.write("\r  [%d/%d] %-38s elapsed %.1fs ETA %.1fs   "
                     % (done, total, what[:38], el, eta))
    sys.stdout.flush()


# ------------------------------------------------------------ load

def load_static(lang):
    """acceptance grid -> per-op holder-grain accept set."""
    for suf in ("A1", "A2"):
        p = os.path.join(HERE, "acceptance_%s_%s.json" % (lang, suf))
        if os.path.exists(p):
            d = json.load(open(p))
            break
    else:
        raise SystemExit("no acceptance grid for %s" % lang)
    assert d.get("complete"), "%s grid not complete" % lang
    hs = d["holders"]
    form = [h["form"] for h in hs]
    rep = [h["rep"] for h in hs]
    per = {}
    for key, c in d["cells"].items():
        op, i, j = c["operation"], key.rsplit("|", 2)[1], key.rsplit("|", 2)[2]
        i, j = int(i), int(j)
        per.setdefault(op, dict(accept=set(), total=set()))
        per[op]["total"].add((i, j))
        if c["verdict"] == "ACCEPT":
            per[op]["accept"].add((i, j))
    return dict(language=lang, route=d["route"], form=form, rep=rep,
                ops=d["operations"], per=per, answers=None)


def load_dynamic(lang):
    """route-C behavior table -> per-op holder-grain accept set + answers."""
    d = json.load(open(os.path.join(HERE, "behavior_%s_C.json" % lang)))
    assert d.get("complete"), "%s behavior table not complete" % lang
    hs, _ = holders(lang)
    form = [h["form"] for h in hs]
    rep = [h["rep"] for h in hs]
    os_ = ops(lang)
    per = {}
    ans = {}
    for i, ha in enumerate(hs):
        va = sorted(ha["values"])
        for j, hb in enumerate(hs):
            vb = sorted(hb["values"])
            for vca in va:
                for vcb in vb:
                    for op in os_:
                        pid = "P%d_%d_%s_%s_%s" % (i, j, vca, vcb, op)
                        cell = d["cells"].get(pid)
                        if cell is None:
                            continue
                        per.setdefault(op, dict(accept=set(), total=set()))
                        per[op]["total"].add((i, j))
                        if cell[0] == "ANSWER":
                            per[op]["accept"].add((i, j))
                            # answer CLASS, not the value: the text before
                            # the first colon is the runtime's own type name
                            cls = cell[1].split(":", 1)[0]
                            ans.setdefault(op, {}).setdefault(
                                (form[i], form[j]), {}).setdefault(cls, 0)
                            ans[op][(form[i], form[j])][cls] += 1
    return dict(language=lang, route="C", form=form, rep=rep, ops=os_,
                per=per, answers=ans)


# --------------------------------------------------- value overlay

def load_overlay(lang):
    """DECISIONS 8/9/10: read valuematrix_<lang>.json ONLY if it is complete.

    Returns None when the gate refuses the file.  Never raises on an
    unfinished matrix -- refusing it IS the correct outcome.
    """
    p = os.path.join(HERE, "valuematrix_%s.json" % lang)
    if not os.path.exists(p):
        return dict(admitted=False, reason="no matrix file")
    d = json.load(open(p))
    if not d.get("complete"):
        return dict(admitted=False,
                    reason="gate refused: %s, %d of %d probes"
                    % (d.get("completeness"), d.get("probes", 0),
                       d.get("expected_probes", 0)))
    per = {}
    agree = disagree = 0
    for key, c in d["cells"].items():
        op = c["operation"]
        i, j = key.rsplit("|", 2)[1], key.rsplit("|", 2)[2]
        i, j = int(i), int(j)
        if c["shape"] == "uniform":
            acc = c["verdict"] == "ACCEPT"
        else:
            # DECISION 10: existential over the value cross product
            acc = "ACCEPT" in c["verdicts"]
        per.setdefault(op, dict(accept=set(), total=set()))
        per[op]["total"].add((i, j))
        if acc:
            per[op]["accept"].add((i, j))
        # DECISION 11: how wrong was the one-value-per-holder grid
        g = c.get("acceptance_run_verdict")
        if g is not None:
            if (g == "ACCEPT") == acc:
                agree += 1
            else:
                disagree += 1
    return dict(admitted=True, per=per, probes=d["probes"],
                pair_cells=d["pair_cells"], uniform=d["uniform_cells"],
                split=d["split_cells"], grid_agree=agree,
                grid_disagree=disagree)


# ------------------------------------------------------- signatures

def signature(L):
    """project to forms; build the per-operation signature record."""
    sigs = {}
    for op, rec in L["per"].items():
        acc, tot = rec["accept"], rec["total"]
        if not tot:
            continue
        cells = {}
        for (i, j) in tot:
            k = (L["form"][i], L["form"][j])
            c = cells.setdefault(k, [0, 0])
            c[1] += 1
            if (i, j) in acc:
                c[0] += 1
        dom_any = sorted(k for k, c in cells.items() if c[0] > 0)
        dom_all = sorted(k for k, c in cells.items() if c[0] == c[1])
        dom_maj = sorted(k for k, c in cells.items() if c[0] * 2 >= c[1]
                         and c[0] > 0)
        # DECISION 7: mixed-holder statistic, holder grain, same-form only
        same_form_acc = [(i, j) for (i, j) in acc
                         if L["form"][i] == L["form"][j]]
        mixed = [(i, j) for (i, j) in same_form_acc if i != j]
        sigs[op] = dict(
            language=L["language"], operation=op, route=L["route"],
            holder_accepts=len(acc), holder_probes=len(tot),
            domain=["%s|%s" % k for k in dom_any],
            domain_universal=["%s|%s" % k for k in dom_all],
            domain_majority=["%s|%s" % k for k in dom_maj],
            density={"%s|%s" % k: round(c[0] / c[1], 4)
                     for k, c in sorted(cells.items()) if c[0]},
            same_form_accepts=len(same_form_acc),
            mixed_holder_accepts=len(mixed),
            mixed_holder_ratio=(round(len(mixed) / len(same_form_acc), 4)
                                if same_form_acc else None),
            answer_classes=None)
        if L["answers"] and op in L["answers"]:
            sigs[op]["answer_classes"] = {
                "%s|%s" % k: sorted(v, key=lambda c: -v[c])
                for k, v in sorted(L["answers"][op].items())}
    return sigs


# -------------------------------------------------------- relations

def jaccard(a, b):
    u = a | b
    return (len(a & b) / len(u)) if u else None


def relate(a, b, sa, sb):
    A, B = set(sa["domain"]), set(sb["domain"])
    if not A or not B:
        return None
    j = jaccard(A, B)
    if A == B:
        rel = "equals"
    elif A > B:
        rel = "nests"          # a's domain strictly contains b's
    elif B > A:
        rel = "nested_by"
    elif A & B:
        rel = "overlaps"
    else:
        rel = ("contradicts" if sa["operation"] == sb["operation"]
               else "disjoint")
    return dict(a=a, b=b, relation=rel, jaccard=round(j, 4),
                a_only=sorted(A - B), b_only=sorted(B - A),
                shared=sorted(A & B))


def cluster(keys, sim, cut):
    """average-linkage agglomerative, cut at `cut` similarity."""
    groups = [[k] for k in keys]
    while True:
        best, bi, bj = None, None, None
        for x in range(len(groups)):
            for y in range(x + 1, len(groups)):
                vals = [sim[(p, q)] for p in groups[x] for q in groups[y]]
                m = sum(vals) / len(vals)
                if best is None or m > best:
                    best, bi, bj = m, x, y
        if best is None or best < cut:
            break
        groups[bi] = groups[bi] + groups[bj]
        groups.pop(bj)
    return sorted((sorted(g) for g in groups), key=lambda g: (-len(g), g[0]))


def main():
    t0 = time.time()
    sigs = {}
    overlay = {}
    for n, lang in enumerate(ALL, 1):
        bar(n - 1, len(ALL), t0, "loading %s" % lang)
        L = load_static(lang) if lang in STATIC else load_dynamic(lang)
        for op, s in signature(L).items():
            sigs["%s.%s" % (lang, op)] = s
        if lang in STATIC:
            ov = load_overlay(lang)
            if ov["admitted"]:
                O = dict(L)
                O["per"] = ov["per"]
                osig = signature(O)
                ov["domains"] = {op: s["domain"] for op, s in osig.items()}
                ov["widened"] = {}
                for op, s in osig.items():
                    g = set(sigs.get("%s.%s" % (lang, op), {})
                            .get("domain", []))
                    v = set(s["domain"])
                    if v - g or g - v:
                        ov["widened"][op] = dict(
                            added=sorted(v - g), lost=sorted(g - v))
                del ov["per"]
            overlay[lang] = ov
        bar(n, len(ALL), t0, "%s: %d operations" % (lang, len(L["per"])))
    print()
    adm = sorted(l for l, o in overlay.items() if o["admitted"])
    print("  value-matrix gate: %d admitted (%s); %d refused"
          % (len(adm), ", ".join(adm), len(overlay) - len(adm)))

    keys = sorted(k for k, s in sigs.items() if s["domain"])
    empty = sorted(k for k, s in sigs.items() if not s["domain"])
    print("  %d operation signatures; %d with a non-empty domain, "
          "%d empty (excluded per decision 4)"
          % (len(sigs), len(keys), len(empty)))

    sim = {}
    pairs = list(itertools.combinations(keys, 2))
    t1 = time.time()
    for n, (a, b) in enumerate(pairs, 1):
        if n % 20000 == 0:
            bar(n, len(pairs), t1, "similarity")
        v = jaccard(set(sigs[a]["domain"]), set(sigs[b]["domain"])) or 0.0
        sim[(a, b)] = sim[(b, a)] = v
    for k in keys:
        sim[(k, k)] = 1.0
    bar(len(pairs), len(pairs), t1, "similarity done")
    print()

    clusters = {}
    for cut in (0.70, 0.85):
        print("  clustering at %.2f ..." % cut)
        clusters["%.2f" % cut] = cluster(keys, sim, cut)

    # relations: only edges worth writing down -- same spelled operation
    # anywhere, plus any cross-language pair scoring >= 0.5
    edges = []
    for a, b in pairs:
        sa, sb = sigs[a], sigs[b]
        if sa["language"] == sb["language"]:
            continue
        same_spelling = sa["operation"] == sb["operation"]
        if not same_spelling and sim[(a, b)] < 0.5:
            continue
        e = relate(a, b, sa, sb)
        if e:
            e["same_spelling"] = same_spelling
            edges.append(e)
    kinds = {}
    for e in edges:
        kinds[e["relation"]] = kinds.get(e["relation"], 0) + 1
    print("  %d relation edges: %s" % (len(edges), kinds))

    # DECISION 7: the mixed-holder statistic, ranked.  No operation is
    # named here; the ranking is produced and then read.
    mixed = sorted(
        ({k: sigs[k][f] for f in ("language", "operation",
                                  "same_form_accepts",
                                  "mixed_holder_accepts",
                                  "mixed_holder_ratio")}
         for k in keys), key=lambda d: 0)
    mixed = [dict(key=k, language=sigs[k]["language"],
                  operation=sigs[k]["operation"],
                  same_form_accepts=sigs[k]["same_form_accepts"],
                  mixed_holder_accepts=sigs[k]["mixed_holder_accepts"],
                  mixed_holder_ratio=sigs[k]["mixed_holder_ratio"])
             for k in keys if sigs[k]["mixed_holder_ratio"] is not None]
    mixed.sort(key=lambda d: (-d["mixed_holder_ratio"], d["key"]))
    by_op = {}
    for m in mixed:
        by_op.setdefault(m["operation"], []).append(m["mixed_holder_ratio"])
    op_rank = sorted(((op, round(sum(v) / len(v), 4), len(v))
                      for op, v in by_op.items()),
                     key=lambda t: -t[1])
    print("  mixed-holder ranking: top spellings %s"
          % ", ".join("%s=%.2f" % (o, r) for o, r, _ in op_rank[:6]))

    out = dict(
        status="PRELIMINARY",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        scope=("nine acceptance grids (route A) + three route-C behavior "
               "tables, all complete; plus a value-matrix OVERLAY for the "
               "matrices that pass the completeness gate, decisions 8-11"),
        forms=FORMS, shared_space_cells=len(SHARED),
        decisions=[dict(n=n, text=t) for n, t in DECISIONS],
        signatures=sigs, empty_domain=empty,
        value_matrix_overlay=overlay,
        mixed_holder_by_signature=mixed,
        mixed_holder_by_spelling=[dict(operation=o, mean_ratio=r,
                                       signatures=c) for o, r, c in op_rank],
        clusters=clusters, relation_counts=kinds, relations=edges)
    json.dump(out, open(os.path.join(HERE, "clusters_preliminary.json"), "w"),
              indent=1)
    print("  wrote clusters_preliminary.json (%.1f MB)"
          % (os.path.getsize(os.path.join(HERE,
             "clusters_preliminary.json")) / 1e6))
    return out


if __name__ == "__main__":
    main()
