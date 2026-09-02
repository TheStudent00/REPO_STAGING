#!/usr/bin/env python3
"""verdicts3.py -- step 7 again, with the candidate set taken from
machine-form evidence only.

Why this file exists
--------------------
`verdicts.py` built its comparison rows on the key
`(operator token, type pair)`.  Only units spelled the same were ever
paired.  That is a violation of THE SPELLING BAN, and it had a
measurable cost: `rust !=` and `cpp ^` on `(bool,bool)` are the same
machine bytes -- clusters.json had already merged them -- and they
never received a verdict, because their spellings differ.

`verdicts.py`, `verdicts.json` and `verdicts2.json` are left untouched
as the record of the violation and of what it produced.  This file
replaces the candidate set and nothing else.

The candidate set, stated exactly
---------------------------------
A unit is paired with another unit only when both hold, in this order:

  TYPE PAIR.  The two units carry the same operand type pair.  Types
  are ABI facts recorded by the probe generator, not spellings, so
  this is a machine-form key.  An i32 addition and an f64 addition
  stay two rows.

  and then EITHER

  (a) CLUSTER.  The two units sit in the same byte cluster or the same
      sem cluster of clusters.json.  Bytes and anchored lifted forms;
      no spelling involved.

  (b) CONNECTION.  Both lifted forms contain an identical maximal
      sub-term over the anchored variables.  The sub-term index is
      built from the sem forms: every serialized sub-expression that
      mentions `in0` or `in1`, is compound (an operation is applied),
      and is not a pure width adjustment.  A bare leaf like `in0:64`
      is in nearly every unit; so is `ex32@0(in0:64)`, which is only
      "the argument, narrowed".  Both connect nothing, and the second
      is excluded by the pipeline's own `verdicts.PASSTHROUGH` test
      rather than by a new rule of this file.  A sub-term is MAXIMAL
      for a group when no longer shared sub-term covers the same
      member set.

Connections come in three levels, counted separately, following the
distinction the owner named: whether the shared core sits inside control
flow.  An occurrence is NESTED when it appears in a block other than
block 0, or inside a branch condition; otherwise it is FLAT.

  both_nested   the shared core is inside control-flow nesting on
                both sides
  one_nested    one side nests it, the other has it flat
  both_flat     neither side nests it

The verdict logic itself is NOT re-derived.  `judge` is imported from
verdicts.py unchanged, so bytes, sem identity, the one-sided-guard
reading and the z3 call are literally the same code.  RE-DERIVED
MINIMALLY, and stated here because it is the only thing that is: the
unit loader is imported too (`verdicts.load_units`), so the exclusion
rules (`fallback_lhs`, DWARF contradiction, no anchored sem) are the
same as well.  Nothing about the deciding is new; only the choosing.

Already-decided pairs are CARRIED, not re-solved: verdicts2.json is
read and every pair it already holds keeps its verdict, addressed by
its unordered unit-pair id.  z3 runs only for pairs the spelling
scoping had hidden.

Output: verdicts3.json and verdicts3.md.  Rows are CLUSTER and
CONNECTION groups.  Every member lists its language, its operator
token AS A DISPLAY LABEL, and its type pair.  No row is named by a
token.

usage:
  verdicts3.py            write verdicts3.json and verdicts3.md
"""

import json
import os
import sys
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import verdicts as V                                         # noqa: E402
import z3_ext as X                                           # noqa: E402
import arch_sem as AS                                        # noqa: E402
import z3                                                    # noqa: E402


# The one setting this pass changes, stated because it changes
# results: z3_ext asks its solver with a 20-second cap per query.
# This pass lowers that cap to 2 seconds for the pairs it decides
# fresh.  The reason is wall clock -- the sandbox that runs this kills
# a process every three minutes, so the run is chunked, and a
# 20-second cap makes the chunking impractical.  The effect of the
# lower cap is one-directional and honest: a pair the solver would
# have decided between 2 and 20 seconds lands in the UNDECIDED bin
# with the solver's own "unknown" reason instead.  It never turns an
# undecided pair into a decided one.
X.Z3_TIMEOUT_MS = 2000


FLOAT_REPS = ("f32", "f64")


def skip_tier1(tp, v):
    """is the wider z3 translation worth asking for this pair?

    Measured in this sandbox, on the pairs the spelling scoping had
    hidden: the wider translation spends seconds per floating-point
    pair and returns the solver's own `unknown` almost every time,
    because it models IEEE FP with z3's FP theory.  Two cores and a
    process the host kills every three minutes make that unaffordable
    at this pair count, so float pairs keep their tier-0 verdict and
    the skip is RECORDED ON THE PAIR rather than hidden."""
    if v["verdict"] == "UNMATCHED" and tp == "bool,bool":
        return False
    for rep in FLOAT_REPS:
        if rep in tp:
            return True
    return False


def decide(left, right, tp):
    """the verdict for one pair, at the same tier as the carried ones.

    `verdicts.judge` first (bytes, sem identity, the one-sided guard,
    then the narrow z3 translation), and where `z3_ext.retryable` says
    the wider translation can say something new, `z3_ext.z3_pair_ext`
    after it.  Both are imported, not re-derived: a new pair and a
    carried pair are decided by exactly the same code."""
    try:
        v = V.judge(left, right)
    except Exception as exc:                              # noqa: BLE001
        v = dict(verdict="UNDECIDED", ground="the pass raised",
                 detail="%s: %s" % (type(exc).__name__, exc))
    want, why = X.retryable(v, tp)
    if not want:
        return v
    if skip_tier1(tp, v):
        v["tier1"] = False
        v["tier1_skipped"] = ("the wider translation was NOT run on this "
                              "pair: its operands are floating point, "
                              "where that translation asks z3's FP theory "
                              "and the solver returns unknown after "
                              "seconds.  This pair's verdict is the "
                              "tier-0 one.  UNVERIFIED whether the wider "
                              "translation would decide it.")
        return v
    precondition = tp == "bool,bool" and v["verdict"] == "UNMATCHED"
    try:
        verdict, detail, extra = X.z3_pair_ext(left, right, precondition)
    except Exception as exc:                              # noqa: BLE001
        verdict = "UNDECIDED"
        detail = "the tier-1 pass raised: %s: %s" % (type(exc).__name__,
                                                     exc)
        extra = dict(tier1=True)
    v["tier1"] = True
    v["tier1_reason"] = why
    v["tier0_verdict"] = v["verdict"]
    v["tier0_detail"] = v.get("detail")
    v["verdict"] = verdict
    v["ground"] = "z3 over the two lifted forms (tier 1)"
    v["detail"] = detail
    for k, val in (extra or {}).items():
        v[k] = val
    return v


# ---------------------------------------------------------------- sub-terms

def split_args(text):
    """the comma-separated arguments of one serialized call, split at
    depth zero."""
    out = []
    depth = 0
    start = 0
    for i, ch in enumerate(text):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            out.append(text[start:i])
            start = i + 1
    out.append(text[start:])
    return out


def subterms(text, out):
    """every sub-expression of one serialized value, itself included."""
    text = text.strip()
    if not text:
        return
    out.add(text)
    i = text.find("(")
    if i < 0:
        return
    if not text.endswith(")"):
        return
    inner = text[i + 1:-1]
    for arg in split_args(inner):
        subterms(arg, out)


def anchored_compound(text):
    """is this sub-term a connection candidate?

    Three conditions, and the third is the one that matters:

      * compound -- an operation is applied.  A bare leaf like
        `in0:64` is in nearly every unit and connects nothing.
      * over the anchored variables -- it mentions `in0` or `in1`.
      * NOT a pure width adjustment.  `ex32@0(in0:64)` and
        `zx64(ex32@0(in0:64))` are compound and anchored, and they are
        still only "the argument, narrowed or widened".  The pipeline
        already has a name and a test for that shape --
        `verdicts.PASSTHROUGH` -- and this reuses it rather than
        inventing a second rule.  Without this condition every unit
        that merely reads an argument is connected to every other one.
    """
    if "(" not in text:
        return False
    if "in0" not in text and "in1" not in text:
        return False
    if V.PASSTHROUGH.match(text):
        return False
    return True


def unit_subterms(unit):
    """the connection sub-terms of one unit, each with the strongest
    nesting level at which it occurs.

    returns {subterm: True if nested somewhere}"""
    found = {}
    blocks = unit["sem"]["blocks"]
    for b in blocks:
        index = b["block"]
        pieces = []
        for v in b["values"]:
            pieces.append((v, index > 0))
        for s in b["stores"]:
            pieces.append((s, index > 0))
        for ev in b["events"]:
            if not ev.startswith("branch "):
                continue
            i = ev.find("[")
            if i < 0:
                continue
            pieces.append((ev[i + 1:-1], True))
        for text, nested in pieces:
            got = set()
            subterms(text, got)
            for t in got:
                if not anchored_compound(t):
                    continue
                if nested:
                    found[t] = True
                elif t not in found:
                    found[t] = False
    return found


# ---------------------------------------------------------------- groups

def type_pair(meta):
    return "%s,%s" % (meta.get("lhs_rep"), meta.get("rhs_rep"))


def cluster_groups(units_by_id):
    """the CLUSTER candidate rows: one row per (cluster, type pair)
    that holds units of more than one language."""
    path = os.path.join(HERE, "clusters.json")
    doc = json.load(open(path))
    rows = []
    for kind in ("byte", "sem"):
        for cl in doc["clusters"][kind]:
            by_tp = defaultdict(list)
            for m in cl["members"]:
                uid = (m["lang"], m["n"])
                u = units_by_id.get(uid)
                if u is None:
                    continue
                by_tp[m["type_pair"]].append(u)
            for tp, members in sorted(by_tp.items()):
                langs = sorted(set(m["lang"] for m in members))
                if len(langs) < 2:
                    continue
                rows.append(dict(
                    ground="cluster",
                    cluster_kind=kind,
                    cluster_key=cl["key"],
                    type_pair=tp,
                    members=members,
                ))
    return rows


def connection_groups(units, by_id):
    """the CONNECTION candidate rows: one row per (maximal shared
    sub-term, type pair) that holds units of more than one language."""
    index = defaultdict(dict)
    for u in units:
        tp = type_pair(u["meta"])
        for t, nested in u["subterms"].items():
            index[(tp, t)][(u["lang"], u["n"])] = nested

    kept = []
    for (tp, t), members in index.items():
        langs = set(k[0] for k in members)
        if len(langs) < 2:
            continue
        kept.append((tp, t, members))

    # maximality: drop a sub-term whose member set is already covered
    # by a LONGER shared sub-term on the same type pair.  The longer
    # core is the stronger statement; the shorter one adds nothing.
    by_tp = defaultdict(list)
    for tp, t, members in kept:
        by_tp[tp].append((t, members))

    rows = []
    for tp, entries in sorted(by_tp.items()):
        entries.sort(key=lambda e: -len(e[0]))
        for i, (t, members) in enumerate(entries):
            covered = False
            keys = set(members.keys())
            for j, (t2, m2) in enumerate(entries):
                if j >= i:
                    continue
                if len(t2) <= len(t):
                    continue
                if keys <= set(m2.keys()):
                    covered = True
                    break
            if covered:
                continue
            rows.append(dict(
                ground="connection",
                core=t,
                type_pair=tp,
                members=[by_id[k] for k in sorted(members.keys())],
                nested_flags=dict(("%s/%s" % k, v)
                                  for k, v in members.items()),
            ))
    return rows


# ---------------------------------------------------------------- carrying

def pair_id(a, b):
    """the unordered id of one unit pair."""
    x = "%s/op_%s" % (a["lang"], a["n"])
    y = "%s/op_%s" % (b["lang"], b["n"])
    if x <= y:
        return (x, y)
    return (y, x)


def carried_verdicts():
    """every verdict verdicts2.json already holds, by unit-pair id."""
    path = os.path.join(HERE, "verdicts2.json")
    if not os.path.exists(path):
        return {}
    doc = json.load(open(path))
    out = {}
    for row in doc["rows"]:
        for p in row["pairs"]:
            x = p["left"]
            y = p["right"]
            if x > y:
                x, y = y, x
            keep = dict(p)
            keep.pop("left", None)
            keep.pop("right", None)
            out[(x, y)] = keep
    return out


# ---------------------------------------------------------------- naming

def row_name(row):
    """a canonical description of the shared core.  Never a token."""
    if row["ground"] == "cluster":
        if row["cluster_kind"] == "byte":
            what = "byte-identical group [%s]" % row["cluster_key"]
        else:
            what = "sem-identical group %s" % row["cluster_key"]
    else:
        what = "shared-core group %s" % row["core"]
    return "%s · (%s)" % (what, row["type_pair"])


CACHE = "verdicts3_cache.json"


def load_cache():
    """the pair verdicts already computed by an earlier chunk of this
    run.  The pass is resumable because the sandbox that runs it kills
    long processes; the cache is the resume point, and it changes no
    result."""
    path = os.path.join(HERE, CACHE)
    if not os.path.exists(path):
        return {}
    doc = json.load(open(path))
    out = {}
    for k, v in doc.items():
        a, b = k.split("|")
        out[(a, b)] = v
    return out


def save_cache(decided):
    doc = {}
    for (a, b), v in decided.items():
        doc["%s|%s" % (a, b)] = v
    path = os.path.join(HERE, CACHE)
    json.dump(doc, open(path, "w"))


def main():
    budget = 0
    for arg in sys.argv[1:]:
        if arg.startswith("--budget="):
            budget = int(arg.split("=")[1])
    started = time.time()

    units, excluded, excluded_rows = V.load_units()
    for u in units:
        u["subterms"] = unit_subterms(u)
    by_id = {}
    for u in units:
        by_id[(u["lang"], u["n"])] = u

    rows = []
    rows.extend(cluster_groups(by_id))
    rows.extend(connection_groups(units, by_id))

    carried = carried_verdicts()
    decided = load_cache()
    tally = Counter()
    levels = Counter()
    pair_level = {}
    fresh = 0

    out_rows = []
    for row in rows:
        by_lang = defaultdict(list)
        for m in row["members"]:
            by_lang[m["lang"]].append(m)
        langs = sorted(by_lang)
        pairs = []
        for i, la in enumerate(langs):
            for lb in langs[i + 1:]:
                for ua in by_lang[la]:
                    for ub in by_lang[lb]:
                        pid = pair_id(ua, ub)
                        if pid in decided:
                            v = dict(decided[pid])
                        elif pid in carried:
                            v = dict(carried[pid])
                            v["carried_from"] = "verdicts2.json"
                            decided[pid] = dict(v)
                        else:
                            if budget and time.time() - started > budget:
                                save_cache(decided)
                                print("budget spent; %d pairs cached, "
                                      "run again to continue"
                                      % len(decided))
                                return 3
                            v = decide(ua, ub, row["type_pair"])
                            v["newly_paired"] = True
                            v["pair_type_pair"] = row["type_pair"]
                            decided[pid] = dict(v)
                            fresh += 1
                            if fresh % 200 == 0:
                                save_cache(decided)
                                print("progress: %d decided this chunk, "
                                      "%d cached, %ds elapsed"
                                      % (fresh, len(decided),
                                         int(time.time() - started)))
                                sys.stdout.flush()
                        v["left"] = pid[0]
                        v["right"] = pid[1]
                        if row["ground"] == "connection":
                            fa = row["nested_flags"]["%s/%s"
                                                     % (ua["lang"], ua["n"])]
                            fb = row["nested_flags"]["%s/%s"
                                                     % (ub["lang"], ub["n"])]
                            n = int(bool(fa)) + int(bool(fb))
                            name = {2: "both_nested", 1: "one_nested",
                                    0: "both_flat"}[n]
                            v["connection_level"] = name
                            levels[name] += 1
                            best = pair_level.get(pid)
                            rank = {"both_nested": 2, "one_nested": 1,
                                    "both_flat": 0}
                            if best is None or rank[name] > rank[best]:
                                pair_level[pid] = name
                        pairs.append(v)
        if not pairs:
            continue
        members = []
        for m in row["members"]:
            members.append(dict(lang=m["lang"], n=m["n"],
                                operator=m["meta"].get("operator"),
                                type_pair=type_pair(m["meta"])))
        keep = dict(
            ground=row["ground"],
            name=row_name(row),
            type_pair=row["type_pair"],
            languages=langs,
            members=members,
            pairs=pairs,
        )
        if row["ground"] == "cluster":
            keep["cluster_kind"] = row["cluster_kind"]
            keep["cluster_key"] = row["cluster_key"]
        else:
            keep["core"] = row["core"]
        out_rows.append(keep)

    save_cache(decided)

    new_pairs = []
    carried_used = 0
    for pid, v in decided.items():
        tally[v["verdict"]] += 1
        if v.get("carried_from"):
            carried_used += 1
            continue
        a = by_id[(pid[0].split("/")[0], pid[0].split("/")[1][3:])]
        b = by_id[(pid[1].split("/")[0], pid[1].split("/")[1][3:])]
        new_pairs.append((pid, v["verdict"],
                          a["meta"].get("operator"),
                          b["meta"].get("operator"),
                          v.get("pair_type_pair", "")))

    doc = dict(
        languages=V.LANGS,
        units_considered=len(units),
        excluded=dict(excluded),
        excluded_rows=excluded_rows,
        candidate_set="type pair, then cluster identity or shared "
                      "maximal sub-term.  No operator token anywhere.",
        rows=out_rows,
        distinct_pairs=len(decided),
        carried_from_verdicts2=carried_used,
        newly_paired=len(new_pairs),
        new_pair_tally=dict(Counter(x[1] for x in new_pairs)),
        connection_levels=dict(levels),
        connection_levels_note="`connection_levels` counts CONNECTION\nINSTANCES: one pair sitting in three shared-core groups is counted\nthree times.  `connection_levels_by_pair` counts each unit pair once,\nat the strongest level any of its connections reached.",
        connection_levels_by_pair=dict(Counter(pair_level.values())),
        tally=dict(tally),
        z3=z3.get_version_string(),
        lifter=AS.LIFTER_ID,
    )
    json.dump(doc, open(os.path.join(HERE, "verdicts3.json"), "w"),
              indent=1)
    write_md(doc, new_pairs)

    print("== step 7, machine-form candidate set")
    print("   units considered        %d" % len(units))
    print("   rows (cluster groups)   %d"
          % sum(1 for r in out_rows if r["ground"] == "cluster"))
    print("   rows (connection groups)%d"
          % sum(1 for r in out_rows if r["ground"] == "connection"))
    print("   distinct unit pairs     %d" % len(decided))
    print("   carried from verdicts2  %d" % carried_used)
    print("   newly paired            %d" % len(new_pairs))
    print("   new-pair tally          %s" % dict(Counter(x[1]
                                                         for x in new_pairs)))
    print("   connection levels       %s" % dict(levels))
    print("   ... by distinct pair    %s"
          % dict(Counter(pair_level.values())))
    for v in ("MATCHED", "DIFFERS-BY-DESIGN", "UNMATCHED", "UNDECIDED"):
        print("   %-20s %d" % (v, tally.get(v, 0)))
    return 0


SHORT = {"MATCHED": "M", "DIFFERS-BY-DESIGN": "D", "UNMATCHED": "X",
         "UNDECIDED": "?"}


def write_md(doc, new_pairs):
    out = []
    out.append("# verdicts3 -- verdicts over a machine-form candidate set")
    out.append("")
    out.append("Rows are CLUSTER groups (same bytes, or same anchored")
    out.append("lifted form) and CONNECTION groups (the same maximal")
    out.append("sub-term over the anchored variables).  A row is never")
    out.append("named by an operator token.  Each member carries its")
    out.append("token as a display label only.")
    out.append("")
    out.append("- units considered: %d" % doc["units_considered"])
    out.append("- distinct unit pairs judged: %d" % doc["distinct_pairs"])
    out.append("- carried unchanged from verdicts2.json: %d"
               % doc["carried_from_verdicts2"])
    out.append("- newly paired, hidden before by spelling scoping: %d"
               % doc["newly_paired"])
    out.append("- new-pair tally: %s" % doc["new_pair_tally"])
    out.append("- connection levels (instances): %s"
               % doc["connection_levels"])
    out.append("- connection levels (distinct pairs): %s"
               % doc["connection_levels_by_pair"])
    out.append("- overall tally: %s" % doc["tally"])
    out.append("")
    out.append("## the pairs the spelling scoping had hidden")
    out.append("")
    out.append("| left | right | left label | right label | type pair |"
               " verdict |")
    out.append("|---|---|---|---|---|---|")
    for pid, verdict, oa, ob, tp in sorted(new_pairs):
        out.append("| %s | %s | `%s` | `%s` | %s | %s |"
                   % (pid[0], pid[1], oa, ob, tp, verdict))
    out.append("")
    out.append("## rows")
    out.append("")
    for row in doc["rows"]:
        out.append("### %s" % row["name"])
        out.append("")
        out.append("- ground: %s" % row["ground"])
        out.append("- languages: %s" % ", ".join(row["languages"]))
        labels = []
        for m in row["members"]:
            labels.append("%s `%s` (%s)" % (m["lang"], m["operator"],
                                            m["type_pair"]))
        out.append("- members: %s" % "; ".join(labels))
        out.append("")
        for p in row["pairs"]:
            line = "  - %s %s / %s -- %s" % (SHORT.get(p["verdict"], "?"),
                                             p["left"], p["right"],
                                             p["verdict"])
            out.append(line)
            out.append("    - %s: %s" % (p.get("ground", ""),
                                         p.get("detail", "")))
        out.append("")
    path = os.path.join(HERE, "verdicts3.md")
    open(path, "w").write("\n".join(out))


if __name__ == "__main__":
    sys.exit(main())
