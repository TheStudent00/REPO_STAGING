#!/usr/bin/env python3
"""cross_unit_prover_bucket1.py -- TASK 4's sweep of the unbudgeted
bucket: bucket 1 from cross_unit_prover.py's own priority_bucket
(cross-language, non-float class key) -- 6,401 pairs, named but
never attempted by cross_unit_prover.py (--limit stopped in bucket
0) or by cross_unit_prover_extend.py (that file's own docstring:
"Bucket 1 ... is NOT touched by this run").

Reuses cross_unit_prover.py's population builder, candidate-pair
builder, priority_bucket, and prove_pair() UNCHANGED (imported, not
reimplemented) -- the SAME machinery already used for the float
slice (14 proved) and the widened same-language/cross-float sweep
(0 new proofs in 5,285 pairs).

Skips any (a,b) pair already attempted in proved_edges.json or
proved_edges2.json (any verdict), so no pair is proved twice.
Transitivity shortcut: before calling the solver, checks whether a
and b are already connected via a union-find over every PROVED edge
seen so far (both prior files + this run's own new edges so far).
If connected, records PROVED-by-transitivity, no solver call.

CHECKPOINTING: the sandbox caps a single command's wall-clock at
~170s. SWEEP_BUDGET_SECONDS (env, default 150) bounds one process's
run; re-running this same command resumes from proved_edges3.json's
own contents (already-attempted set includes this file's own prior
pairs), so several short chunks accumulate into one sweep -- same
resume pattern as cross_unit_prover_extend.py's OUT_FILE handling.

Writes proved_edges3.json -- ADDITIVE to proved_edges.json AND
proved_edges2.json (a third file, same schema; the three are meant
to be merged by unioning their `pairs` lists; this file never
overwrites either prior file).

usage:
  SWEEP_BUDGET_SECONDS=150 python3 cross_unit_prover_bucket1.py
"""
import json
import os
import sys
import time
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cross_unit_prover as CUP  # noqa: E402

TIME_BUDGET_SECONDS = float(os.environ.get("SWEEP_BUDGET_SECONDS", "150"))
OLD_FILE_1 = os.path.join(HERE, "proved_edges.json")
OLD_FILE_2 = os.path.join(HERE, "proved_edges2.json")
OUT_FILE = os.path.join(HERE, "proved_edges3.json")


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


def find_chain(a, b, all_proved_edges):
    adj = {}
    for src_name, e in all_proved_edges:
        adj.setdefault(e["a"], []).append((e["b"], src_name))
        adj.setdefault(e["b"], []).append((e["a"], src_name))
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


def main():
    old1 = json.load(open(OLD_FILE_1))
    old2 = json.load(open(OLD_FILE_2))
    old_pairs = list(old1["pairs"]) + list(old2["pairs"])

    prior_new = []
    if os.path.exists(OUT_FILE):
        prior_doc = json.load(open(OUT_FILE))
        prior_new = list(prior_doc.get("pairs", []))

    already_attempted = set()
    uf = UF()
    all_proved_edges = []  # (source_name, edge) for chain reconstruction
    for e in old_pairs:
        already_attempted.add((e["a"], e["b"]))
        if e["verdict"] == "PROVED":
            uf.union(e["a"], e["b"])
            all_proved_edges.append(("proved_edges.json/proved_edges2.json", e))
    for e in prior_new:
        already_attempted.add((e["a"], e["b"]))
        if e["verdict"] == "PROVED":
            uf.union(e["a"], e["b"])
            all_proved_edges.append(("proved_edges3.json", e))

    text_of, meta_of, class_of = CUP.build_population()
    all_pairs = CUP.build_candidate_pairs(text_of, class_of)

    bucket1 = [p for p in all_pairs
               if CUP.priority_bucket(p[0], p[1], p[2], class_of) == 1]
    bucket1.sort()

    bucket1_remaining = [p for p in bucket1
                          if (p[0], p[1]) not in already_attempted]

    print("bucket1 total (cross-language, non-float): %d" % len(bucket1))
    print("bucket1 remaining before this chunk: %d" % len(bucket1_remaining))

    new_edges = list(prior_new)
    tally = {"PROVED": 0, "PROVED_TRANSITIVE": 0, "DISPROVED": 0,
             "UNDECIDED": 0, "REFUSED": 0}
    for e in prior_new:
        v = e["verdict"]
        if v == "PROVED" and e.get("proof_method") == "transitive":
            tally["PROVED_TRANSITIVE"] += 1
        else:
            tally[v] = tally.get(v, 0) + 1

    t0 = time.time()
    stopped_reason = "completed the full bucket1 remaining set"
    attempted_n = 0
    for i, (a, b, key) in enumerate(bucket1_remaining):
        elapsed = time.time() - t0
        if elapsed > TIME_BUDGET_SECONDS:
            stopped_reason = ("wall-clock budget of %ds reached after "
                               "%d pairs this chunk" % (TIME_BUDGET_SECONDS, i))
            break
        attempted_n = i + 1
        cross_lang = a.split("/op_")[0] != b.split("/op_")[0]

        if uf.connected(a, b):
            chain = find_chain(a, b, all_proved_edges)
            edge = {
                "a": a, "b": b,
                "class_key_type_pair": key[0],
                "class_key_result_family": key[1],
                "cross_language": cross_lang,
                "verdict": "PROVED",
                "detail": ("proved by transitivity (union-find over "
                           "already-PROVED edges), no solver call "
                           "made -- supporting chain: %s" % chain),
                "proof_method": "transitive",
            }
            new_edges.append(edge)
            all_proved_edges.append(("proved_edges3.json", edge))
            tally["PROVED_TRANSITIVE"] += 1
            continue

        verdict, detail = CUP.prove_pair(a, b, text_of, class_of)
        tally[verdict] += 1
        edge = {
            "a": a, "b": b,
            "class_key_type_pair": key[0],
            "class_key_result_family": key[1],
            "cross_language": cross_lang,
            "verdict": verdict,
            "detail": detail,
            "proof_method": "solver",
        }
        new_edges.append(edge)
        if verdict == "PROVED":
            uf.union(a, b)
            all_proved_edges.append(("proved_edges3.json", edge))

        if (i + 1) % 10 == 0:
            print("  [%d/%d this chunk] elapsed=%.1fs tally=%r"
                  % (i + 1, len(bucket1_remaining), elapsed, tally))

    doc = {
        "meta": {
            "role_note": "this file IS a GROUPING/matching artifact -- "
                        "checked by check_no_spelling_keys.py IN FULL.",
            "generator": "cross_unit_prover_bucket1.py",
            "merge_with": "proved_edges.json and proved_edges2.json "
                          "(union the `pairs` lists of all three; this "
                          "file is additive, never a replacement)",
            "population": len(text_of),
            "bucket1_total": len(bucket1),
            "bucket1_remaining_after_this_chunk":
                len(bucket1) - len(new_edges),
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
    print("cumulative attempted: %d / %d" % (len(new_edges), len(bucket1)))


if __name__ == "__main__":
    main()
