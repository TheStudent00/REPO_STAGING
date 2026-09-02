#!/usr/bin/env python3
"""cross_unit_prover_extend.py -- mechanical, additive extension of
cross_unit_prover.py's sweep. Reuses that file's population builder,
candidate-pair builder, priority buckets, and prove_pair() UNCHANGED
(imported, not reimplemented). Adds exactly two things, per explicit
task instructions:

 1. Skips any (a,b) pair already attempted in the existing
    proved_edges.json (any verdict), so no pair is proved twice.
 2. A transitivity shortcut: before calling the solver on a pair,
    checks whether a and b are already connected via a union-find
    over every PROVED edge seen so far (old file + this run's new
    edges). If connected, records PROVED-by-transitivity with the
    supporting edge(s) named, and skips the solver call.

Ordering of the pairs actually attempted this run (task-specified):
  (a) the 348 not-yet-attempted pairs in bucket 0 (cross-language +
      float-arithmetic/integer bucket, cross_unit_prover.py's own
      bucket numbering)
  (b) then same-language pairs (buckets 2 and 3), ordered by
      cheaper-first = shorter combined canonical-text length.
Bucket 1 (cross-language, non-float, 6,401 pairs) is NOT touched by
this run -- the task's own framing of "348 remaining cross-language"
+ "same-language" pairs does not name bucket 1, so it is left
untouched and reported as still fully unattempted.

Writes proved_edges2.json -- ADDITIVE to proved_edges.json (a
different file, same schema, meant to be merged by unioning the
`pairs` lists of both files; never overwrites the original).
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cross_unit_prover as CUP  # noqa: E402

TIME_BUDGET_SECONDS = float(os.environ.get("SWEEP_BUDGET_SECONDS", "600"))
OLD_FILE = os.path.join(HERE, "proved_edges.json")
OUT_FILE = os.path.join(HERE, "proved_edges2.json")


class UF:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.parent[rx] = ry

    def connected(self, x, y):
        return self.find(x) == self.find(y)


def main():
    old = json.load(open(OLD_FILE))
    old_pairs = list(old["pairs"])
    # RESUME support: if a proved_edges2.json already exists from a
    # prior chunk of this same sweep (this process is run in several
    # time-boxed chunks because the calling harness caps a single
    # command's wall-clock), fold its pairs in as already-attempted
    # too, and carry them forward into the new output so each chunk's
    # output is cumulative, never a partial overwrite.
    prior_new = []
    if os.path.exists(OUT_FILE):
        prior_doc = json.load(open(OUT_FILE))
        prior_new = list(prior_doc.get("pairs", []))
    already_attempted = set()
    uf = UF()
    proved_edge_for = {}  # frozenset({a,b}) -> edge dict, for direct-proof lookup
    for e in old_pairs + prior_new:
        already_attempted.add((e["a"], e["b"]))
        if e["verdict"] == "PROVED":
            uf.union(e["a"], e["b"])
            proved_edge_for[frozenset((e["a"], e["b"]))] = e

    text_of, meta_of, class_of = CUP.build_population()
    all_pairs = CUP.build_candidate_pairs(text_of, class_of)
    print("full candidate set: %d pairs" % len(all_pairs))

    buckets = {0: [], 1: [], 2: [], 3: []}
    for a, b, key in all_pairs:
        buckets[CUP.priority_bucket(a, b, key, class_of)].append((a, b, key))

    bucket0_remaining = [p for p in buckets[0]
                          if (p[0], p[1]) not in already_attempted]
    same_lang_remaining = [p for p in (buckets[2] + buckets[3])
                            if (p[0], p[1]) not in already_attempted]
    # cheaper-first: sort by combined canonical-text length
    same_lang_remaining.sort(
        key=lambda p: len(text_of[p[0]]) + len(text_of[p[1]]))
    bucket0_remaining.sort()

    bucket1_remaining = [p for p in buckets[1]
                          if (p[0], p[1]) not in already_attempted]

    print("bucket0 remaining (cross-lang float-arith): %d"
          % len(bucket0_remaining))
    print("bucket2+3 remaining (same-language): %d"
          % len(same_lang_remaining))
    print("bucket1 remaining (cross-lang other, NOT attempted this run): %d"
          % len(bucket1_remaining))

    ordered = bucket0_remaining + same_lang_remaining

    new_edges = list(prior_new)  # cumulative across resumed chunks
    tally = {"PROVED": 0, "PROVED_TRANSITIVE": 0, "DISPROVED": 0,
             "UNDECIDED": 0, "REFUSED": 0}
    for e in prior_new:
        v = e["verdict"]
        if v == "PROVED" and e.get("proof_method") == "transitive":
            tally["PROVED_TRANSITIVE"] += 1
        else:
            tally[v] = tally.get(v, 0) + 1
    t0 = time.time()
    stopped_reason = "completed the full ordered remaining set"
    attempted_n = 0
    chunk_start_len = len(new_edges)
    for i, (a, b, key) in enumerate(ordered):
        elapsed = time.time() - t0
        if elapsed > TIME_BUDGET_SECONDS:
            stopped_reason = ("wall-clock budget of %ds reached after "
                               "%d pairs" % (TIME_BUDGET_SECONDS, i))
            break
        attempted_n = i + 1
        cross_lang = a.split("/op_")[0] != b.split("/op_")[0]
        bnum = CUP.priority_bucket(a, b, key, class_of)

        if uf.connected(a, b):
            # transitivity shortcut -- find a short supporting chain
            # by walking recorded PROVED edges via BFS on the fly.
            chain = find_chain(a, b, old_pairs, new_edges)
            new_edges.append({
                "a": a, "b": b,
                "class_key_type_pair": key[0],
                "class_key_result_family": key[1],
                "cross_language": cross_lang,
                "verdict": "PROVED",
                "detail": ("proved by transitivity (union-find over "
                           "already-PROVED edges), no solver call "
                           "made -- supporting chain: %s" % chain),
                "proof_method": "transitive",
            })
            tally["PROVED_TRANSITIVE"] += 1
            continue

        verdict, detail = CUP.prove_pair(a, b, text_of, class_of)
        tally[verdict] += 1
        new_edges.append({
            "a": a, "b": b,
            "class_key_type_pair": key[0],
            "class_key_result_family": key[1],
            "cross_language": cross_lang,
            "verdict": verdict,
            "detail": detail,
            "proof_method": "solver",
        })
        if verdict == "PROVED":
            uf.union(a, b)
        if (i + 1) % 25 == 0:
            print("  [%d/%d] elapsed=%.1fs tally=%r"
                  % (i + 1, len(ordered), elapsed, tally))
            json.dump({"partial": True, "done": i + 1,
                       "total": len(ordered), "edges_so_far": new_edges},
                      open(OUT_FILE + ".partial", "w"), indent=1)

    doc = {
        "meta": {
            "role_note": "this file IS a GROUPING/matching artifact -- "
                        "checked by check_no_spelling_keys.py IN FULL.",
            "generator": "cross_unit_prover_extend.py",
            "merge_with": "proved_edges.json (union the `pairs` lists "
                          "of both files; this file is additive, "
                          "not a replacement)",
            "population": len(text_of),
            "bucket0_remaining_before_this_run": len(bucket0_remaining),
            "same_language_remaining_before_this_run":
                len(same_lang_remaining),
            "bucket1_cross_language_other_untouched":
                len(bucket1_remaining),
            "attempted_count_this_chunk": attempted_n,
            "attempted_count_cumulative": len(new_edges),
            "stopped_reason": stopped_reason,
            "per_pair_timeout_ms": CUP.PER_PAIR_TIMEOUT_MS,
            "tally": tally,
            "note": "candidate set is machine-form only (type_pair, "
                   "result-type class family), never an operator "
                   "token -- see cross_unit_prover.py's own docstring.",
        },
        "pairs": new_edges,
    }
    json.dump(doc, open(OUT_FILE, "w"), indent=1)
    print("wrote %s" % OUT_FILE)
    print("tally: %r" % tally)
    print("stopped_reason: %s" % stopped_reason)


def find_chain(a, b, old_pairs, new_edges):
    """BFS over PROVED edges (old + new-so-far) to name a short
    supporting chain from a to b, for the evidence trail."""
    adj = {}
    for e in old_pairs:
        if e["verdict"] == "PROVED":
            adj.setdefault(e["a"], []).append((e["b"], "proved_edges.json"))
            adj.setdefault(e["b"], []).append((e["a"], "proved_edges.json"))
    for e in new_edges:
        if e["verdict"] == "PROVED":
            adj.setdefault(e["a"], []).append((e["b"], "proved_edges2.json"))
            adj.setdefault(e["b"], []).append((e["a"], "proved_edges2.json"))
    from collections import deque
    q = deque([(a, [a])])
    seen = {a}
    while q:
        node, path = q.popleft()
        if node == b:
            return path
        for nxt, src in adj.get(node, []):
            if nxt not in seen:
                seen.add(nxt)
                q.append((nxt, path + [nxt]))
    return ["<chain not found -- union-find said connected but BFS "
            "could not reconstruct; treat as a bug>"]


if __name__ == "__main__":
    main()
