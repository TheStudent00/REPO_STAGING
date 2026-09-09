#!/usr/bin/env bash
# o12 lane 12 -- closing evidence, corrected: every command uses an
# absolute path (the checker's own working directory is
# PseudoCoupHQ, not this folder) and sed uses the \%...%
# address form (a leading / in a /pattern/ address reads to the
# conventions checker as a file path -- task o7 hit the same thing,
# lane o7_l9, and fixed it the same way in o7_l11).  git is pinned to
# a single SHA per invocation (a plain `git log` with no revision is
# refused by the checker as a moving reference).
set -u
SYN=PseudoCoupHQ/Research/oracle/cross_construction/emulation/synthesis
TOTAL=9
echo "[1/$TOTAL] the fix commit, pinned"
git log -1 --format="COMMIT %H %ad" --date=iso b7abda67768b3833878d1a20dc306d97dd93e1ae
echo "[1b/$TOTAL] the last commit to synthesize.py before the full run, pinned"
git log -1 --format="COMMIT %H %ad" --date=iso 82765ca79a272801d1a3d6b9a6370d37792efaf3

echo "[2/$TOTAL] the corrected admissibility functions, as they stand now"
sed -n '394,412p' "$SYN/synthesize.py"

echo "[3/$TOTAL] synthesis_report.md sections 1-3"
sed -n '\%^## 1\. The population%,\%^## 3a\.%p' "$SYN/synthesis_report.md" | sed '\%^## 3a\.%d'

echo "[4/$TOTAL] synthesis_report.md section 5, in full"
sed -n '\%^## 5\. The compositions found%,$p' "$SYN/synthesis_report.md"

echo "[5/$TOTAL] the 30-sample, entry_ids grouped by type_key"
python3 -c "
import json
d = json.load(open('$SYN/synthesis_sample_guess30000ms.json'))
tks = {}
for r in d['results']:
    tk = r.get('type_key')
    tks[tk] = tks.get(tk, 0) + 1
for k in sorted(tks):
    print('%s: %d targets' % (k, tks[k]))
print('total', d['count'])
"

echo "[6/$TOTAL] synthesis_report.md section 3a, in full"
sed -n '\%^## 3a\.%,\%^## 4\.%p' "$SYN/synthesis_report.md" | sed '\%^## 4\.%d'

echo "[7/$TOTAL] synthesis_report.md section 4, in full"
sed -n '\%^## 4\. Agreement%,\%^## 5\.%p' "$SYN/synthesis_report.md" | sed '\%^## 5\.%d'

echo "[8/$TOTAL] synthesis_results.json, the 4 both_proved agreement rows"
python3 -c "
import json
d = json.load(open('$SYN/synthesis_results.json'))
for r in d['agreement']:
    if r['both_proved']:
        print(r['entry_id'], r['x_lang'], r['x_unit'],
              'length=%s' % r['composition_length'],
              'composition_entry_ids=%s' % r['composition_entry_ids'],
              'same_pool_entry_as_a_component=%s' % r['same_pool_entry_as_a_component'],
              'compiler_route_body_opcode_count=%s' % r['compiler_route_body_opcode_count'])
"

echo "[9/$TOTAL] the memory bound, the guard re-run, grep -c exempt"
sed -n '\%named abort ABORT_MEMORY_O12%,+1p' "$SYN/synthesize.py"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  "$SYN/synthesis_plan.json" \
  "$SYN/synthesis_sample_guess3000ms.json" \
  "$SYN/synthesis_sample_guess30000ms.json" \
  "$SYN/synthesis_run_guess30000ms.json" \
  "$SYN/synthesis_results.json"
echo "-- guard exit $?"
grep -c exempt "$SYN/synthesize.py" "$SYN/synthesis_report.md" \
  "$SYN/synthesis_plan.json" "$SYN/synthesis_sample_guess3000ms.json" \
  "$SYN/synthesis_sample_guess30000ms.json" "$SYN/synthesis_run_guess30000ms.json" \
  "$SYN/synthesis_results.json"
echo "-- done"
