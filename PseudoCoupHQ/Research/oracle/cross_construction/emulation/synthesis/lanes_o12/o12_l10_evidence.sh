#!/usr/bin/env bash
# o12 lane 10 -- closing evidence: every command this closing log
# (log_230) pastes, run fresh inside the sandbox against the mounted
# repo, so the log's LITERAL blocks are real reproducing commands
# rather than citations of host-only artifacts (the AirlockRuns log
# tree is not mounted into this sandbox, so a lane log cannot be
# re-read from inside a lane -- everything here reads only mounted
# repo files).  Guard re-run at the end, unmodified checker.
set -u
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/synthesis
TOTAL=9

echo "[1/$TOTAL] the fix commit, in the file's own history"
git -C /projects/PseudoCoupHQ log --format="COMMIT %H %ad" --date=iso \
  -- Research/oracle/cross_construction/emulation/synthesis/synthesize.py \
  | grep -A0 -B0 "^COMMIT b7abda67" || echo "NOT FOUND"
echo "-- the last commit to touch the file before the full run (o12_l7, 2026-09-07T04:21:32Z / 00:21:32 -0400)"
git -C /projects/PseudoCoupHQ log --format="COMMIT %H %ad" --date=iso \
  -- Research/oracle/cross_construction/emulation/synthesis/synthesize.py | head -1

echo "[2/$TOTAL] the corrected admissibility functions, as they stand now"
sed -n '/^def leaf_admissible/,/^def root_admissible/p; /^def root_admissible/,/^# ====/p' synthesize.py | sed -n '1,40p'

echo "[3/$TOTAL] synthesis_report.md sections 1-3"
sed -n '/^## 1\. The population/,/^## 3a\./p' synthesis_report.md | sed '/^## 3a\./d'

echo "[4/$TOTAL] synthesis_report.md section 5, in full"
sed -n '/^## 5\. The compositions found/,$p' synthesis_report.md

echo "[5/$TOTAL] the 30-sample, entry_ids grouped by type_key"
python3 -c "
import json
d = json.load(open('synthesis_sample_guess30000ms.json'))
tks = {}
for r in d['results']:
    tk = r.get('type_key')
    tks[tk] = tks.get(tk, 0) + 1
for k in sorted(tks):
    print('%s: %d targets' % (k, tks[k]))
print('total', d['count'])
"

echo "[6/$TOTAL] synthesis_report.md section 3a, in full"
sed -n '/^## 3a\./,/^## 4\./p' synthesis_report.md | sed '/^## 4\./d'

echo "[7/$TOTAL] synthesis_report.md section 4, in full"
sed -n '/^## 4\. Agreement/,/^## 5\./p' synthesis_report.md | sed '/^## 5\./d'

echo "[8/$TOTAL] synthesis_results.json, the 4 both_proved agreement rows"
python3 -c "
import json
d = json.load(open('synthesis_results.json'))
for r in d['agreement']:
    if r['both_proved']:
        print(r['entry_id'], r['x_lang'], r['x_unit'],
              'length=%s' % r['composition_length'],
              'composition_entry_ids=%s' % r['composition_entry_ids'],
              'same_pool_entry_as_a_component=%s' % r['same_pool_entry_as_a_component'],
              'compiler_route_body_opcode_count=%s' % r['compiler_route_body_opcode_count'])
"

echo "[9/$TOTAL] the memory bound, stated in synthesize.py, and the guard re-run"
sed -n '/named abort ABORT_MEMORY_O12/,+1p' synthesize.py
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  synthesis_plan.json \
  synthesis_sample_guess3000ms.json \
  synthesis_sample_guess30000ms.json \
  synthesis_run_guess30000ms.json \
  synthesis_results.json
echo "-- guard exit $?"
grep -c exempt synthesize.py synthesis_report.md \
  synthesis_plan.json synthesis_sample_guess3000ms.json \
  synthesis_sample_guess30000ms.json synthesis_run_guess30000ms.json \
  synthesis_results.json
