#!/usr/bin/env python3
"""l3_final.py -- layer 3 phase 4, the FINAL clustering and threshold sweep.

This supersedes `l3_cluster.py`, whose every artifact said PRELIMINARY in
its first field.  Three things changed underneath it and each one is a
numbered decision below:

  * ALL NINE value matrices are complete (2,221,643 probes), so decision
    9's planned promotion fires: the value matrix BECOMES the primary
    domain for the nine statically checked languages.  The acceptance
    grids are kept only as the thing the promotion is measured against.
  * the dart `||` instrument fault of log 029 is FIXED, not flagged --
    `dart analyze` was scraped at every severity, so a `dead_code`
    WARNING on `true || b` was read as a type refusal.  Decision 12.
  * the owner's ruling: no chosen cut.  The full merge history is computed and
    the whole threshold range is reported -- the cluster-count curve, the
    stability plateaus, and where the named stories form and dissolve.
    Decision 14.

Decisions 1 through 11 are carried over from `l3_cluster.py` verbatim
except where a numbered successor replaces them, and they are reproduced
in the output so that overturning any one of them remains a one-line
instruction rather than a rejection of the pass.
"""

import itertools
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from l3_accept import holders, ops                    # noqa: E402
from l3_cluster import (STATIC, DYNAMIC, ALL, FORMS, SHARED,   # noqa: E402
                        DECISIONS as PRELIM_DECISIONS,
                        load_static, load_dynamic, signature,
                        jaccard, relate, bar)

NEW_DECISIONS = [
    ("12", "THE DART HARNESS IS FIXED, NOT FLAGGED.  log 029 found seven "
     "`contradicts' edges, all of them dart's `||', and chased them to a "
     "grid cell recording `bool || bool' REFUSE with an EMPTY error "
     "detail.  Diagnosed here: the dart lane ran `dart analyze <dir>` and "
     "marked a probe REFUSE if its filename appeared ANYWHERE in the "
     "output, at ANY severity, and recorded no detail at all.  dart "
     "reports `dead_code' on the right operand of `true || b' and of "
     "`false && b', which is a WARNING.  So a short-circuit lint was "
     "being read as a type refusal, and the acceptance grid -- which "
     "probes ONE value per holder -- happened to draw `true' for the "
     "truth holder, which is the dead-code case for `||' and the live "
     "case for `&&'.  One value, opposite luck, and a language-level "
     "contradiction reported.  The fix reads `dart analyze "
     "--format=machine' and counts ONLY severity ERROR as a refusal, "
     "which is what the other eight harnesses already measure -- g++, "
     "javac and rustc do not fail on warnings either -- so the fix makes "
     "dart CONSISTENT rather than special.  It also restores the detail "
     "field.  Dart's whole value matrix and its acceptance grid were "
     "re-run under the fix (217,073 + 10,625 probes, 176 s).  Verified "
     "for regressions: of 217,073 matrix probes, 50,381 moved REFUSE to "
     "ACCEPT and ZERO moved ACCEPT to REFUSE.  The superseded raw files "
     "are kept as `raw/SUPERSEDED_*_lintbug.txt'."),
    ("13", "THE LOAD-CHECK LANES ARE THEMSELVES INSTRUMENTS AND TWO OF "
     "THE NINE WERE FAULTY.  A load check declares a holder and stops, "
     "with no use of the declared name.  go punishes exactly that: "
     "`declared and not used: a' and `\"fmt\" imported and not used' are "
     "HARD ERRORS in go, so all 94 of go's load-check probes refused and "
     "the lane measured go's unused-variable rule rather than whether the "
     "holder can hold the value.  dart refused all 113 for the decision "
     "12 reason, `unused_local_variable' being an INFO.  Both were "
     "re-run: go with a single `_ = fmt.Sprint(a)' that consumes the "
     "variable and the import together, dart under the severity fix.  go "
     "now refuses 21 of 94 and dart 12 of 113, and dart's refusals read "
     "`INTEGER_LITERAL_OUT_OF_RANGE', which is precisely the layer-2 leak "
     "HARVEST predicted.  A load check that refuses everything cannot "
     "separate anything, so the preliminary pass's go and dart split "
     "classifications were void and are replaced, not adjusted."),
    ("14", "NO CHOSEN CUT -- THE SWEEP IS THE DELIVERABLE.  Decision 5 "
     "picked 0.70 and reported 0.85 beside it, and log 029 already "
     "conceded that nothing in the data picks either.  This pass computes "
     "the FULL MERGE HISTORY instead: average linkage run to a single "
     "root, every merge recorded with the similarity at which it "
     "happened.  The dendrogram IS the sweep.  From that history the "
     "cluster count at any threshold t is exact and needs no re-run -- "
     "it is the leaf count minus the number of merges at similarity >= "
     "t -- so the whole curve is reported rather than two points on it.  "
     "STABILITY PLATEAUS are the reading: a maximal run of t over which "
     "the cluster count does not change is a range where the picture "
     "does not move, and a WIDE plateau is a natural reading of the data "
     "in a way that a chosen number never is.  Average linkage is "
     "monotone, so the history has no inversions and the identity holds "
     "exactly."),
    ("15", "SPLIT CELLS ARE CLASSIFIED, NOT COUNTED.  A `split' cell is "
     "one whose verdict moved with the VALUE rather than the holder pair, "
     "and log 024 decision 3's territory is that there are two reasons "
     "and they are not the same finding.  Against the load-check lanes "
     "each split is classified: `layer2_only' when every refusing value "
     "pair has a side whose DECLARATION ALONE also refuses (the holder "
     "could not hold the value, so the operation was never judged -- "
     "layer 2 leaking in); `layer3_moving' when at least one refusing "
     "value pair has both sides loading perfectly well (the finding "
     "proper); `mixed' when one cell carries both.  A TRUE VALUE-LEVEL "
     "ACCEPTANCE SPLIT is `layer3_moving' plus the layer-3 half of "
     "`mixed'; a `layer2_only' cell is a layer-2 fact wearing a layer-3 "
     "costume and is reported separately everywhere."),
    ("16", "THE PROMOTION IS MEASURED, NOT ASSUMED.  Decision 9 is now "
     "spent: the nine statically checked languages take their domain from "
     "the value matrix under decision 10's existential-over-values rule, "
     "and python, ruby and php stay on route C behavior (decision 3) "
     "because no matrix exists or can exist for them.  Because the "
     "objection decision 9 raised was that a partial promotion would move "
     "similarities for a reason about WHICH LANE FINISHED, the delta "
     "against the preliminary pass is computed per signature and per "
     "cluster and reported in full -- every domain that changed, and by "
     "which cells.  The promotion is only defensible because it is now "
     "ALL nine, and the delta is the evidence for what it cost."),
    ("17", "A LANE THAT RUNS OUT OF SCRATCH SCORES EVERY MISSING PROBE "
     "ACCEPT, AND STILL EXITS 0.  Found here, not looked for.  The first "
     "re-run of `vm_dartfix_01` produced 49,827 accepts where the same "
     "shard had produced 4,675 before, and the value matrix then claimed "
     "dart accepted `Map<String,int> && String` for some values of the "
     "map and not others -- which is not a rule any type checker could "
     "be following.  Chased: `/work` is a 4 GB tmpfs and it was holding "
     "3.7 GB of phase-3 leftovers, so the lane could not write its probe "
     "sources; 44,268 `OSError: [Errno 28] No space left on device' lines "
     "are in its log.  The harness scores `no diagnostic' as ACCEPT, and "
     "a file that was never written draws no diagnostic, so ENOSPC reads "
     "as universal acceptance.  The lane still exited 0 and still printed "
     "its `__SUMMARY__' line, so the completeness gate -- which counts "
     "probes and summary lines -- passed it.  THE GATE CANNOT SEE THIS "
     "FAULT.  /work was swept, the shard re-run clean (0 ENOSPC, 9,350 "
     "accepts), and `vm_dartfix_00' was re-run on clean scratch as a "
     "control and reproduced its 17,101 accepts EXACTLY.  Every other "
     "value-matrix, acceptance and load-check lane log in the node was "
     "then scanned: ZERO further ENOSPC lines, so no other measurement in "
     "this node is implicated.  The void file is kept as "
     "`raw/VOID_vm_dart_01_enospc.txt'.  Standing rule proposed for the "
     "next agent: a lane's log must be grepped for ENOSPC before its "
     "product is folded, because neither the exit code nor the summary "
     "line nor the probe count can detect it."),
]
DECISIONS = PRELIM_DECISIONS + NEW_DECISIONS

# decisions superseded by a later numbered one
SUPERSEDED = {"5": "14", "8": "16", "9": "16"}


# ------------------------------------------------------- primary domain

def load_matrix_primary(lang):
    """DECISION 16 + 10: the value matrix AS THE PRIMARY DOMAIN.

    Returns the same shape `load_static` returns, so `signature` cannot
    tell the difference -- which is the point: the promotion changes the
    input, not the method.  Refuses anything the completeness gate
    refuses; a refusal here is a hard stop, because this pass exists on
    the premise that all nine are complete.
    """
    p = os.path.join(HERE, "valuematrix_%s.json" % lang)
    d = json.load(open(p))
    if not d.get("complete"):
        raise SystemExit("%s value matrix INCOMPLETE (%s) -- the promotion "
                         "of decision 16 requires all nine"
                         % (lang, d.get("completeness")))
    space = json.load(open(os.path.join(HERE, "space_%s.json" % lang)))
    hs = space["holders"]
    form = [h["form"] for h in hs]
    rep = [h["rep"] for h in hs]
    per = {}
    for key, c in d["cells"].items():
        op = c["operation"]
        i, j = (int(v) for v in key.rsplit("|", 2)[1:])
        if c["shape"] == "uniform":
            acc = c["verdict"] == "ACCEPT"
        else:
            acc = "ACCEPT" in c["verdicts"]     # DECISION 10
        per.setdefault(op, dict(accept=set(), total=set()))
        per[op]["total"].add((i, j))
        if acc:
            per[op]["accept"].add((i, j))
    return dict(language=lang, route=d["route"] + " (PRIMARY)", form=form,
                rep=rep, ops=space["operations"], per=per, answers=None,
                probes=d["probes"], pair_cells=d["pair_cells"],
                split_cells=d["split_cells"])


# ------------------------------------------------- full merge history

def merge_history(keys, sim):
    """average linkage (UPGMA) run to a single root, exactly.

    Lance-Williams update for average linkage:
        d(k, i+j) = (ni*d(k,i) + nj*d(k,j)) / (ni+nj)
    which is exact for UPGMA, so this is the same tree `l3_cluster.cluster`
    produced, computed once instead of once per threshold.

    Returns the merge list, each entry carrying the similarity at which
    the merge happened and the two member sets joined.
    """
    n = len(keys)
    idx = {k: i for i, k in enumerate(keys)}
    dist = [[0.0] * n for _ in range(n)]
    for a, b in itertools.combinations(keys, 2):
        d = 1.0 - sim[(a, b)]
        dist[idx[a]][idx[b]] = dist[idx[b]][idx[a]] = d
    active = list(range(n))
    size = {i: 1 for i in range(n)}
    members = {i: [keys[i]] for i in range(n)}
    node = {i: i for i in range(n)}
    merges = []
    t0 = time.time()
    nxt = n
    while len(active) > 1:
        best, bi, bj = None, None, None
        for x in range(len(active)):
            for y in range(x + 1, len(active)):
                d = dist[active[x]][active[y]]
                if best is None or d < best:
                    best, bi, bj = d, x, y
        a, b = active[bi], active[bj]
        newid = nxt
        nxt += 1
        na, nb = size[a], size[b]
        row = [0.0] * (nxt)
        for c in active:
            if c in (a, b):
                continue
            v = (na * dist[a][c] + nb * dist[b][c]) / (na + nb)
            while len(dist[c]) <= newid:
                dist[c].append(0.0)
            dist[c][newid] = v
            row[c] = v
        dist.append(row)
        for c in active:
            if c not in (a, b):
                while len(dist[newid]) <= c:
                    dist[newid].append(0.0)
                dist[newid][c] = dist[c][newid]
        size[newid] = na + nb
        members[newid] = members[a] + members[b]
        active = [c for c in active if c not in (a, b)] + [newid]
        merges.append(dict(
            node=newid, similarity=round(1.0 - best, 6),
            distance=round(best, 6), size=na + nb,
            left=dict(id=a, size=na), right=dict(id=b, size=nb),
            members=sorted(members[newid])))
        if len(merges) % 25 == 0:
            bar(len(merges), n - 1, t0, "merging")
    bar(n - 1, n - 1, t0, "merge history complete")
    print()
    return merges, members


def count_at(merges, n_leaves, t):
    """clusters at similarity threshold t -- exact, from the history."""
    return n_leaves - sum(1 for m in merges if m["similarity"] >= t)


def clusters_at(keys, merges, members, t):
    """the actual cluster membership at threshold t."""
    joined = set()
    groups = []
    for m in reversed(merges):
        pass
    # walk merges in order; a merge at sim >= t joins, otherwise it does not
    parent = {}
    live = {k: [k] for k in keys}
    node_members = {}
    for i, k in enumerate(keys):
        node_members[i] = [k]
    cur = {i: [keys[i]] for i in range(len(keys))}
    alive = set(range(len(keys)))
    for m in merges:
        if m["similarity"] < t:
            continue
        a, b, nid = m["left"]["id"], m["right"]["id"], m["node"]
        if a in alive and b in alive:
            cur[nid] = cur[a] + cur[b]
            alive.discard(a)
            alive.discard(b)
            alive.add(nid)
    return sorted((sorted(cur[i]) for i in alive), key=lambda g: (-len(g), g[0]))


def plateaus(merges, n_leaves, lo=0.0, hi=1.0):
    """maximal threshold ranges over which the cluster count is constant.

    The count only changes at a merge similarity, so the breakpoints are
    exactly the distinct merge similarities.  A plateau [a, b) means every
    threshold in that range yields the same clustering -- not merely the
    same COUNT, because between two merge similarities no merge fires.
    """
    sims = sorted({m["similarity"] for m in merges})
    edges = sorted({lo, hi} | {s for s in sims if lo <= s <= hi})
    out = []
    for a, b in zip(edges, edges[1:]):
        if b <= a:
            continue
        mid = (a + b) / 2.0
        out.append(dict(low=round(a, 6), high=round(b, 6),
                        width=round(b - a, 6),
                        clusters=count_at(merges, n_leaves, mid)))
    out.sort(key=lambda d: -d["width"])
    return out


def story_track(keys, merges, members, sets):
    """where a named story FORMS and where it DISSOLVES, across the sweep.

    Asking "are all 21 shift signatures in one cluster" is the wrong
    question -- the answer is only ever yes at the root, which says
    nothing.  The readable question is how CONCENTRATED the story is at
    each threshold, and it is measured two ways at every breakpoint:

      PEAK  -- the largest cluster containing ONLY members of the story
               (size >= 2).  This is the story visible as its own group.
      COVER -- how many of the story's members sit in such a pure cluster
               at all.  A story can peak small and cover wide.

    A story FORMS at the highest threshold where PEAK first exceeds 1,
    and it DISSOLVES at the threshold below which PEAK stops growing
    because the group has been swallowed by a cluster that also contains
    non-members -- recorded as the threshold where COVER falls back to 0.
    Both are read off the same curve, which is reported in full so the
    reading is checkable rather than asserted.
    """
    sims = sorted({m["similarity"] for m in merges}, reverse=True)
    grid = [1.0] + sims
    out = {}
    for name, want in sets.items():
        want = sorted(w for w in want if w in keys)
        if len(want) < 2:
            out[name] = dict(members=want, n=len(want),
                             note="fewer than 2 signatures present")
            continue
        W = set(want)
        curve, forms_at, best = [], None, (0, None)
        dissolves_at = None
        prev_cover = 0
        for t in grid:
            gs = clusters_at(keys, merges, members, t)
            pure = [g for g in gs if len(g) >= 2 and set(g) <= W]
            peak = max((len(g) for g in pure), default=0)
            cover = sum(len(g) for g in pure)
            curve.append(dict(threshold=round(t, 6), peak=peak, cover=cover))
            if peak >= 2 and forms_at is None:
                forms_at = t
            if peak > best[0]:
                best = (peak, t,
                        sorted(max(pure, key=len)) if pure else None)
            if prev_cover > 0 and cover == 0 and dissolves_at is None:
                dissolves_at = t
            prev_cover = cover
        out[name] = dict(
            members=want, n=len(want),
            forms_at=forms_at,
            peak_size=best[0], peak_at=best[1],
            peak_cluster=(best[2] if len(best) > 2 else None),
            dissolves_below=dissolves_at,
            curve=curve)
    return out


def main():
    t0 = time.time()
    print("== l3_final: promotion (decision 16) + sweep (decision 14) ==\n")
    sigs, prelim_sigs, prov = {}, {}, {}
    for n, lang in enumerate(ALL, 1):
        bar(n - 1, len(ALL), t0, "loading %s" % lang)
        if lang in STATIC:
            G = load_static(lang)                  # the OLD primary
            M = load_matrix_primary(lang)          # the NEW primary
            for op, s in signature(G).items():
                prelim_sigs["%s.%s" % (lang, op)] = s
            for op, s in signature(M).items():
                sigs["%s.%s" % (lang, op)] = s
            prov[lang] = dict(source="value matrix (PRIMARY)",
                              probes=M["probes"], pair_cells=M["pair_cells"],
                              split_cells=M["split_cells"])
        else:
            L = load_dynamic(lang)                 # route C, unchanged
            for op, s in signature(L).items():
                sigs["%s.%s" % (lang, op)] = s
                prelim_sigs["%s.%s" % (lang, op)] = s
            prov[lang] = dict(source="route C behavior (unchanged)")
        bar(n, len(ALL), t0, "%s done" % lang)
    print()

    # ---------------------------------------------------- the delta
    delta = {}
    for k, s in sigs.items():
        p = prelim_sigs.get(k)
        if p is None:
            delta[k] = dict(kind="new signature", added=s["domain"], lost=[])
            continue
        a, b = set(p["domain"]), set(s["domain"])
        if a != b:
            delta[k] = dict(kind="domain moved",
                            was=len(a), now=len(b),
                            added=sorted(b - a), lost=sorted(a - b))
    gone = sorted(set(prelim_sigs) - set(sigs))
    print("  DELTA: %d of %d signatures moved domain under the promotion; "
          "%d disappeared" % (len(delta), len(sigs), len(gone)))

    keys = sorted(k for k, s in sigs.items() if s["domain"])
    empty = sorted(k for k, s in sigs.items() if not s["domain"])
    print("  %d operation signatures; %d non-empty, %d empty (decision 4)"
          % (len(sigs), len(keys), len(empty)))

    sim = {}
    pairs = list(itertools.combinations(keys, 2))
    t1 = time.time()
    for n, (a, b) in enumerate(pairs, 1):
        if n % 20000 == 0:
            bar(n, len(pairs), t1, "similarity")
        sim[(a, b)] = sim[(b, a)] = jaccard(set(sigs[a]["domain"]),
                                            set(sigs[b]["domain"])) or 0.0
    for k in keys:
        sim[(k, k)] = 1.0
    bar(len(pairs), len(pairs), t1, "similarity done")
    print()

    # ------------------------------------------------- DECISION 14
    merges, members = merge_history(keys, sim)
    n_leaves = len(keys)
    curve = []
    t = 0.0
    while t <= 1.0001:
        curve.append(dict(threshold=round(t, 3),
                          clusters=count_at(merges, n_leaves, round(t, 3))))
        t += 0.01
    pl = plateaus(merges, n_leaves)
    # a plateau that reports ONE cluster or ALL singletons is an artefact of
    # the ends of the range, not a reading of the data.  Marked, not dropped.
    for p in pl:
        p["degenerate"] = (p["clusters"] <= 1 or p["clusters"] >= n_leaves)
    print("  merge history: %d merges over %d leaves" % (len(merges), n_leaves))
    print("  widest plateaus (threshold range -> cluster count):")
    for p in pl[:10]:
        print("    [%.3f, %.3f)  width %.3f  ->  %3d clusters%s"
              % (p["low"], p["high"], p["width"], p["clusters"],
                 "   (degenerate)" if p["degenerate"] else ""))

    # snapshots people will ask for, reported as points ON the curve and
    # explicitly NOT as a chosen reading
    snaps = {}
    for t in (0.50, 0.60, 0.70, 0.80, 0.85, 0.90):
        snaps["%.2f" % t] = clusters_at(keys, merges, members, t)
    print("  points on the curve (NOT a chosen reading -- decision 14): "
          + ", ".join("%s->%d" % (k, len(v)) for k, v in sorted(snaps.items())))
    print("  the preliminary pass reported 46 clusters at 0.70 and 58 at "
          "0.85, over 229 leaves; this pass has %d and %d"
          % (len(snaps["0.70"]), len(snaps["0.85"])))

    # ------------------------------------------------- named stories
    def spelled(*sp):
        return [k for k in keys if sigs[k]["operation"] in sp]
    stories = story_track(keys, merges, members, dict(
        plus=spelled("+"),
        shifts=spelled("<<", ">>", ">>>"),
        shifts_and_bitwise=spelled("<<", ">>", ">>>", "&", "|", "^", "&^"),
        equality=spelled("=="),
        equality_all=spelled("==", "!=", "===", "!=="),
        logicals=spelled("&&", "||"),
        comparisons=spelled("<", "<=", ">", ">=", "<=>"),
        # log 029 named these twelve as its cluster 5 at the 0.70 cut --
        # tracked by name so the sweep says what happened to THAT group
        log029_cluster5=["go.%", "go.&", "go.&^", "go.<<", "go.>>", "go.^",
                         "go.|", "java.<<", "java.>>", "java.>>>",
                         "rust.<<", "rust.>>"],
        # log 029 cluster 6, the first cross-family cluster the node made
        log029_cluster6=["cpp.%", "cpp.&", "cpp.<<", "cpp.>>", "cpp.^",
                         "cpp.|", "python.&", "python.<<", "python.>>",
                         "python.^"],
    ))
    print("  named stories (peak = largest cluster of story members only):")
    for nm, d in stories.items():
        if "note" in d:
            continue
        print("    %-20s %2d members; forms at t=%.3f; peak %d at t=%.3f; "
              "dissolves below t=%s"
              % (nm, d["n"], d["forms_at"] or 0, d["peak_size"],
                 d["peak_at"] or 0,
                 ("%.3f" % d["dissolves_below"]) if d["dissolves_below"]
                 else "never"))

    # ---------------------------------------------------- relations
    edges = []
    for a, b in pairs:
        sa, sb = sigs[a], sigs[b]
        if sa["language"] == sb["language"]:
            continue
        same = sa["operation"] == sb["operation"]
        if not same and sim[(a, b)] < 0.5:
            continue
        e = relate(a, b, sa, sb)
        if e:
            e["same_spelling"] = same
            edges.append(e)
    kinds = {}
    for e in edges:
        kinds[e["relation"]] = kinds.get(e["relation"], 0) + 1
    print("  %d relation edges: %s" % (len(edges), kinds))
    contras = [e for e in edges if e["relation"] == "contradicts"]
    print("  CONTRADICTS: %d (preliminary pass had 7, all dart's `||')"
          % len(contras))

    # -------------------------------------------- mixed-holder, again
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
                      for op, v in by_op.items()), key=lambda t: -t[1])

    lc = json.load(open(os.path.join(HERE, "loadcheck_classified.json")))

    out = dict(
        status="FINAL",
        supersedes="clusters_preliminary.json",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        scope=("value matrix as PRIMARY domain for the nine statically "
               "checked languages (2,221,643 probes, all nine complete); "
               "route-C behavior for python, ruby and php; the dart "
               "harness fixed and re-run; no chosen cut -- the full merge "
               "history and the threshold sweep are the result"),
        forms=FORMS, shared_space_cells=len(SHARED),
        decisions=[dict(n=n, text=t,
                        superseded_by=SUPERSEDED.get(n)) for n, t in DECISIONS],
        domain_provenance=prov,
        signatures=sigs, empty_domain=empty,
        promotion_delta=delta, signatures_lost=gone,
        loadcheck=lc,
        merge_history=merges, n_leaves=n_leaves,
        cluster_count_curve=curve,
        stability_plateaus=pl,
        cluster_snapshots=snaps,
        named_stories=stories,
        mixed_holder_by_signature=mixed,
        mixed_holder_by_spelling=[dict(operation=o, mean_ratio=r,
                                       signatures=c) for o, r, c in op_rank],
        relation_counts=kinds, relations=edges,
        contradicts=contras)
    p = os.path.join(HERE, "clusters_final.json")
    json.dump(out, open(p, "w"), indent=1)
    print("\n  wrote clusters_final.json (%.1f MB) in %.1f s"
          % (os.path.getsize(p) / 1e6, time.time() - t0))
    return out


if __name__ == "__main__":
    main()
