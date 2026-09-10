#!/bin/bash
# l3 lane 10 -- run, exactly as the log pastes them, the eight commands of
# log_250 section 9, so every pasted transcript in that section is this
# lane's own output and not a hand-typed one.  Working directory is the
# checker's own: PseudoCoupHQ.
set -u
cd PseudoCoupHQ || exit 1

echo "===== [1/8] ====="
python3 -c 'import collections, json; d = json.load(open("PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json")); rows = d["rows"]; t = collections.Counter(r.get("closed_by") or r.get("outcome") for r in rows); print("rows", len(rows)); print("STATED", sum(1 for r in rows if r["outcome"] == "STATED")); print("REFUSED", sum(1 for r in rows if r["outcome"] == "REFUSED")); print("DISCREPANCY", sum(1 for r in rows if r["outcome"] == "DISCREPANCY")); [print(" ", k, t[k]) for k in sorted(t, key=str)]'
echo "----- exit $? -----"

echo "===== [2/8] ====="
python3 -c 'import collections, json; d = json.load(open("PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json.before_task_l3")); rows = d["rows"]; t = collections.Counter(r.get("closed_by") or r.get("outcome") for r in rows); print("rows", len(rows)); print("STATED", sum(1 for r in rows if r["outcome"] == "STATED")); print("REFUSED", sum(1 for r in rows if r["outcome"] == "REFUSED")); print("DISCREPANCY", sum(1 for r in rows if r["outcome"] == "DISCREPANCY")); [print(" ", k, t[k]) for k in sorted(t, key=str)]'
echo "----- exit $? -----"

echo "===== [3/8] ====="
python3 -c 'import json; d = json.load(open("PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json.before_task_l3")); was = sorted(r["unit"] for r in d["rows"] if r["outcome"] == "DISCREPANCY"); e = json.load(open("PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json")); by = dict((r["unit"], r) for r in e["rows"]); print(len(was)); [print(u, by[u]["theorem_name"], by[u]["outcome"], by[u]["closed_by"], "native" if "ofReduceBool" in (by[u]["axioms"] or "") else "kernel-only") for u in was]'
echo "----- exit $? -----"

echo "===== [4/8] ====="
python3 -c 'import collections, json, re; d = json.load(open("PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json")); p = [r for r in d["rows"] if r.get("closed_by")]; print("proved", len(p), "missing", sum(1 for r in p if not r.get("axioms")), "sorryAx", sum(1 for r in p if "sorryAx" in (r.get("axioms") or ""))); t = collections.Counter((r["closed_by"], re.sub(chr(39) + "[^" + chr(39) + "]+" + chr(39), "THEOREM", r["axioms"])) for r in p); [print(t[k], k) for k in sorted(t, key=str)]'
echo "----- exit $? -----"

echo "===== [5/8] ====="
python3 -c 'import json; d = json.load(open("PseudoCoupHQ/Research/op_pipeline/lean/l3_trust_classes.json")); a = d["attempts"]; print("before", len(d["rows_carrying_ofReduceBool_before"])); print("after", len(d["rows_carrying_ofReduceBool_after"])); print("attempted", len(a)); print("moved", sum(1 for r in a if r["moved_to_the_stronger_class"])); print("kept bv_decide", sum(1 for r in a if not r["moved_to_the_stronger_class"])); print("outcomes", sorted(set(r["bv_normalize_attempt"]["outcome"] for r in a)))'
echo "----- exit $? -----"

echo "===== [6/8] ====="
grep -c ofReduceBool /opt/elan/toolchains/leanprover--lean4---v4.24.0/src/lean/Lean/Elab/Tactic/BVDecide/Frontend/BVDecide.lean
echo "----- exit $? -----"

echo "===== [7/8] ====="
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json PseudoCoupHQ/Research/op_pipeline/lean/l3_trust_classes.json
echo "----- exit $? -----"

echo "===== [8/8] ====="
python3 -c 'import os; paths = sorted(os.path.join(r, f) for r, ds, fs in os.walk("PseudoCoupHQ/Research/op_pipeline/lean/archproof") for f in fs if f.endswith(".lean")); print("lean files", len(paths)); print("native_decide", sum(open(p).read().count("native_decide") for p in paths)); print("bv_decide", sum(open(p).read().count("bv_decide") for p in paths))'
echo "----- exit $? -----"

