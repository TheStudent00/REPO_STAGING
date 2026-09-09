#!/usr/bin/env bash
# m1_l1_explore.sh -- task m1, the survey lane: everything the model
# table's shape depends on, measured before any of it is written.
# MEMORY BOUND: this lane holds one canon40 shard and a ten-mnemonic
# sweep sample; the stated ceiling for the task is 16g (inside the
# instance's 20g), named abort ABORT_MEMORY_M1. Peak RSS is printed at
# the end from resource.getrusage.
set -euo pipefail
echo "[1/6] task m1: the reference's opcode table, counted"
cd PseudoCoupHQ/Research/op_pipeline
python3 - <<'PY'
import json
import os
import resource
import sys
import time

sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline")
sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline/lean")
import z3
import reference as R
import layer5
import term as T
import model_translate as MT

ABORT_MEMORY_M1_KB = 16 * 1024 * 1024


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    now = peak_kb()
    if now > ABORT_MEMORY_M1_KB:
        raise SystemExit("ABORT_MEMORY_M1: %d kB at %s" % (now, where))


table = R.REFERENCE.opcode_table
entries = table.entries
print("table mnemonics: %d" % len(entries))
no_builder = sorted(m for m in entries if entries[m].build is None)
print("no builder (%d): %s" % (len(no_builder), " ".join(no_builder)))

print("")
print("[2/6] same-builder groups (entry.build is other.build)")
by_id = {}
for m in sorted(entries):
    entry = entries[m]
    if entry.build is None:
        continue
    by_id.setdefault(id(entry.build), []).append(m)
groups = [g for g in by_id.values() if len(g) > 1]
groups.sort(key=lambda g: (-len(g), g[0]))
pairs = 0
for g in groups:
    pairs += len(g) * (len(g) - 1) // 2
print("groups of size > 1: %d, pairs: %d" % (len(groups), pairs))
for g in groups:
    print("   %2d  %s" % (len(g), " ".join(g)))

print("")
print("[3/6] the table's mnemonics beside the corpus's 162")
corpus = json.load(open(
    "PseudoCoupHQ/Research/oracle/arch_opcodes/"
    "unique_opcodes.json"))
corpus_mnems = sorted(r["mnem"] for r in corpus["cross_language_rows"])
print("corpus mnemonics: %d" % len(corpus_mnems))
in_both = sorted(set(corpus_mnems) & set(entries))
table_only = sorted(set(entries) - set(corpus_mnems))
corpus_only = sorted(set(corpus_mnems) - set(entries))
print("in both: %d" % len(in_both))
print("table only (%d): %s" % (len(table_only), " ".join(table_only)))
print("corpus only (%d): %s" % (len(corpus_only), " ".join(corpus_only)))

print("")
print("[4/6] a ten-mnemonic sweep sample, with the terms kept")
sample = ["add", "lea", "imul", "sar", "idiv", "sub", "shl", "sal",
          "movzbl", "cmp"]
start = time.time()
model = MT.Model()
kept = 0
example = None
for mnem in sample:
    entry = entries.get(mnem)
    if entry is None or entry.build is None:
        continue
    for shape_name, width, texts in MT.attempts_for(mnem):
        try:
            written, flags, _state, line = MT.run_line(mnem, texts)
        except Exception:
            continue
        if not written and flags is None:
            continue
        for place in sorted(written):
            text = T.Term.normalize(None, written[place])
            kept += 1
            if mnem == "add" and shape_name == "gpr_gpr" and width == 32:
                if example is None:
                    example = (line, place, text)
print("sample: %d place-terms normalized in %.1f s"
      % (kept, time.time() - start))
if example is not None:
    print("   line     : %s" % example[0])
    print("   place    : %s" % example[1])
    print("   layer-5  : %s" % example[2])
check_memory("after the sweep sample")

print("")
print("[5/6] does Term.normalize apply to a bare z3 expr, and does a "
      "Term instance cost anything")
start = time.time()
try:
    holder = T.Term()
    print("   Term() constructed in %.1f s" % (time.time() - start))
    v = z3.BitVec("some_register", 32)
    print("   holder.normalize(v + v) = %s" % holder.normalize(v + v))
except Exception as problem:
    print("   Term() raised %s: %s" % (type(problem).__name__, problem))
v = z3.BitVec("some_register", 32)
print("   T.Term.normalize(None, v + v) = %s"
      % T.Term.normalize(None, v + v))
print("   layer5.normalize(v + v)       = %s" % layer5.normalize(v + v))

print("")
print("[6/6] one canon40 shard: the ledger rows, and how a row reaches "
      "its body line")
import term66_run as TR
shard_paths = TR.shards()
print("shards: %d" % len(shard_paths))
path = shard_paths[0]
document = json.load(open(path))
unit_ids = list(document["units"])
print("shard %s: %d units" % (os.path.basename(path), len(unit_ids)))
start = time.time()
relinked = 0
refused = 0
first_refusal = None
sample_ids = unit_ids[:25]
for unit_id in sample_ids:
    unit = document["units"][unit_id]
    try:
        rows, line_of_row, _occ = T.relink(unit)
        relinked += 1
        if relinked == 1:
            for row in rows:
                producer = row.get("produced_by") or {}
                if producer.get("kind") == "arch_opcode":
                    print("   %s  %-8s  line %r"
                          % (row["row"], producer.get("mnem"),
                             line_of_row.get(row["row"])))
    except Exception as problem:
        refused += 1
        if first_refusal is None:
            first_refusal = "%s: %s" % (type(problem).__name__, problem)
took = time.time() - start
print("   relink over %d units: %d ok, %d refused, %.2f s (%.3f s/unit)"
      % (len(sample_ids), relinked, refused, took, took / len(sample_ids)))
if first_refusal is not None:
    print("   first refusal: %s" % first_refusal[:200])
total_units = 0
for p in shard_paths:
    total_units += 1
print("   at that rate, 31k units would take %.0f s"
      % (31000 * took / len(sample_ids)))
check_memory("after the shard sample")
print("")
print("peak RSS: %d kB" % peak_kb())
PY
echo "[6/6] done"
