#!/usr/bin/env bash
# rv3 lane 8 -- the counts section 1 row 3 produces, the union with task
# rv2's own loop so the cells-proved figure can be read beside its 116 of
# 255, the bank's count BEFORE anything is appended (row 4 waits for task
# ref2), and the spelling guard over every json and jsonl this task wrote.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
AP=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
export HOME=/work
total=6

echo "[1/$total] the per-target table, rv2's run beside this one"
python3 - <<'EOF'
import json, collections
RV = "PseudoCoupHQ/Research/oracle/riscv"

def read(path):
    rows = []
    for line in open(path):
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows

old = read(RV + "/certificates_riscv64.jsonl")
new = read(RV + "/certificates_riscv64_rv3.jsonl")

def tally(rows):
    out = {}
    for r in rows:
        held = out.setdefault(r["target"], collections.Counter())
        held[(r["verdict"] or {}).get("outcome")] += 1
    return out

o, n = tally(old), tally(new)
print("%-12s %-34s %-34s" % ("target", "rv2 (log_259)", "rv3 (this task)"))
for t in sorted(set(o) | set(n)):
    print("%-12s %-34s %-34s"
          % (t, json.dumps(dict(o.get(t, {})), sort_keys=True),
             json.dumps(dict(n.get(t, {})), sort_keys=True)))
print()
print("rv2 kinds", json.dumps(dict(collections.Counter(
    r["kind"] for r in old)), sort_keys=True))
print("rv3 kinds", json.dumps(dict(collections.Counter(
    r["kind"] for r in new)), sort_keys=True))
EOF

echo "[2/$total] the width readings on the proved rows"
python3 - <<'EOF'
import json, collections
RV = "PseudoCoupHQ/Research/oracle/riscv"
rows = []
for line in open(RV + "/certificates_riscv64_rv3.jsonl"):
    line = line.strip()
    if line:
        rows.append(json.loads(line))
proved = [r for r in rows if r["kind"] == "proved"]
whole = collections.Counter(
    (r.get("verdict_at_the_whole_place") or {}).get("outcome")
    for r in proved)
print("proved at the cell's own key_width:", len(proved))
print("of those, at the WHOLE written place:", json.dumps(dict(whole),
                                                          sort_keys=True))
EOF

echo "[3/$total] the cells, and the union with rv2's own loop"
python3 - <<'EOF'
import json
RV = "PseudoCoupHQ/Research/oracle/riscv"

def cells(path, kinds):
    out = set()
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        if r["kind"] not in kinds:
            continue
        c = r["cell"]
        out.add((c.get("mnem"), c.get("shape"), c.get("key_width")))
    return out

inherited_rv2 = cells(RV + "/certificates_riscv64.jsonl", ("proved",))
inherited_rv3 = cells(RV + "/certificates_riscv64_rv3.jsonl", ("proved",))
loop_rv2 = cells(RV + "/rv_loop.jsonl", ("proved",))
table = json.load(open(RV + "/model_table_rv.json"))
allcells = set()
for r in table["rows"]:
    if r.get("outcome") == "TRANSLATED" and r.get("mapping"):
        allcells.add((r["mnem"], r["shape"], r["key_width"]))
print("RISC-V cells in the model table:", len(allcells))
print("inherited PROVED cells, rv2:", len(inherited_rv2))
print("inherited PROVED cells, rv3:", len(inherited_rv3))
print("gained by the re-run:",
      sorted(inherited_rv3 - inherited_rv2))
print("lost by the re-run:", sorted(inherited_rv2 - inherited_rv3))
print("loop PROVED cells, rv2:", len(loop_rv2))
print("union rv2 (log_259 headline):", len(inherited_rv2 | loop_rv2))
print("union rv3 inheritance + rv2 loop:", len(inherited_rv3 | loop_rv2))
EOF

echo "[4/$total] the bank's count BEFORE anything is appended"
wc -l "$AP/certificates.jsonl"
python3 -c "
import json, collections
n = 0
arch = collections.Counter()
for line in open('$AP/certificates.jsonl'):
    line = line.strip()
    if not line:
        continue
    n = n + 1
    arch[json.loads(line).get('arch')] += 1
print('records', n, 'by arch', json.dumps(dict(arch), sort_keys=True))
"

echo "[5/$total] the spelling guard, over every json and jsonl this task wrote"
python3 -c "
import json
for name in ['certificates_riscv64_rv3', 'certificates_riscv64_rv3_sample']:
    rows = []
    for line in open('$RV/%s.jsonl' % name):
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    fh = open('$RV/%s.jsonl.as_one.json' % name, 'w')
    json.dump({'rows': rows}, fh, indent=1, sort_keys=True)
    fh.write('\n')
    fh.close()
    print('wrote %s.jsonl.as_one.json with %d rows' % (name, len(rows)))
"
python3 "$OP/check_no_spelling_keys.py" \
  "$RV/census_rv3.json" \
  "$RV/census_rv3_sample.json" \
  "$RV/level0_points_rv3.json" \
  "$RV/level0_points_rv3_sample.json" \
  "$RV/certificates_riscv64_rv3.json" \
  "$RV/certificates_riscv64_rv3_sample.json" \
  "$RV/certificates_riscv64_rv3.jsonl.as_one.json" \
  "$RV/certificates_riscv64_rv3_sample.jsonl.as_one.json"
echo "guard rc=$?"

echo "[6/$total] the word the guard hunts for, over every file this task added"
python3 - <<'EOF'
import os
RV = "PseudoCoupHQ/Research/oracle/riscv"
added = ["inherit_rv3.py", "census_rv3.json", "census_rv3_sample.json",
         "level0_points_rv3.json", "level0_points_rv3_sample.json",
         "certificates_riscv64_rv3.json",
         "certificates_riscv64_rv3_sample.json",
         "certificates_riscv64_rv3.jsonl",
         "certificates_riscv64_rv3_sample.jsonl",
         "certificates_riscv64_rv3.jsonl.as_one.json",
         "certificates_riscv64_rv3_sample.jsonl.as_one.json",
         "riscv_reference.py", "sail_points.py"]
word = "ex" + "empt"
total_files = 0
carrying = 0
for name in added:
    path = os.path.join(RV, name)
    if not os.path.isfile(path):
        print("NOT ON DISK", name)
        continue
    total_files = total_files + 1
    text = open(path, "r", errors="replace").read()
    count = text.count(word)
    if count:
        carrying = carrying + 1
        print("NONZERO %d %s" % (count, name))
print("deliverable files scanned: %d" % total_files)
print("deliverable files containing the word: %d" % carrying)
EOF
echo "lane rv3_l8 done"
