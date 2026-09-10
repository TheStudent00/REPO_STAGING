#!/bin/bash
# l3 lane 2 -- VERIFY the coordinator's reading of the 19 DISCREPANCY rows on
# the rows themselves, BEFORE anything is changed.  Nothing is written: this
# lane only reads check_L2.json, the canon40 store and the term66 store, and
# prints, per row, WHICH SIDE HOLDS WHICH BINDER under each of the two naming
# rules that are in play.
#
#   rule S (the STORED text's own rule) -- term.Term.normalize:
#       order_commutative -> z3.simplify -> order_commutative -> ordered_symbols
#   rule C (the CHECK's composer rule) -- model_translate.bound_variables:
#       z3.simplify -> layer5.ordered_symbols
#
# Memory bound: 6 GB, named abort ABORT_MEMORY_L3.  The stores are streamed one
# shard at a time by model_translate.stream_store, which is what holds the
# bound; this lane prints its own peak RSS as a second reading.
set -u
TOTAL=4
LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/l3home
mkdir -p "$HOME"
cd "$LEANDIR" || exit 1

python3 - <<'PY'
import json, os, resource, sys
sys.path.insert(0, 'PseudoCoupHQ/Research/op_pipeline/lean')
sys.path.insert(0, 'PseudoCoupHQ/Research/op_pipeline')
import z3
import model_translate as M
import layer5
import term as T
import term97_walk as TW

CEIL = 6 * 1024 * 1024
def guard(where):
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > CEIL:
        raise SystemExit("ABORT_MEMORY_L3: peak %d kB passed the stated "
                         "ceiling %d kB at %s" % (peak, CEIL, where))
    return peak

check = json.load(open('PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json'))
rows = check['rows']
disc = [r for r in rows if r.get('outcome') == 'DISCREPANCY']
stated_ok = [r for r in rows if r.get('closed_by')]
print("[1/4] the population this lane reads")
print("   check_L2.json rows: %d" % len(rows))
print("   DISCREPANCY rows:   %d" % len(disc))
print("   proved rows:        %d" % len(stated_ok))
print("   peak RSS %d kB" % guard('after loading check_L2.json'))

maker, _gate, _attached, _readings = TW.build()
print("   peak RSS %d kB after term97_walk.build()" % guard('build'))

# the control set: 12 proved rows, taken by position over the proved list so
# the sample is not chosen by mnemonic or by any operator token.
control = stated_ok[::max(1, len(stated_ok)//12)][:12]
wanted = set(r['unit'] for r in disc) | set(r['unit'] for r in control)
held, terms = M.stream_store(wanted)
print("   peak RSS %d kB after streaming the two stores" % guard('stream'))

def naming(symbols):
    return dict((s.decl().name(), "v%d" % i) for i, s in enumerate(symbols))

def rule_S(t):
    """the stored text's own rule, term.Term.normalize's prefix."""
    x = T.order_commutative(t)
    x = z3.simplify(x)
    x = T.order_commutative(x)
    return T.ordered_symbols(x)

def rule_C(t):
    """the check composer's rule, model_translate.bound_variables."""
    return layer5.ordered_symbols(z3.simplify(t))

def report(tag, rowlist):
    agree = 0
    differ = 0
    for r in rowlist:
        unit = r['unit']
        record = held.get(unit)
        term_record = terms.get(unit)
        if record is None or term_record is None:
            print("   %-22s NO STORE RECORD" % unit)
            continue
        u = dict(record); u['unit'] = unit
        walked = maker.transcribe(u)
        if walked.out_term is None:
            print("   %-22s NO TERM" % unit)
            continue
        t = walked.out_term
        S = naming(rule_S(t))
        C = naming(rule_C(t))
        same = (S == C)
        agree += 1 if same else 0
        differ += 0 if same else 1
        print("")
        print("   ---- %s   %s  row %s  mnem %r  %s"
              % (r.get('theorem_name') or r.get('outcome'), unit,
                 r.get('row_index'), r.get('mnem'),
                 "SAME NAMING" if same else "NAMING DIFFERS"))
        print("      body_verbatim:")
        body = record.get('body_verbatim') or []
        if not isinstance(body, list):
            body = body.splitlines()
        for line in [str(l) for l in body if str(l).strip()]:
            print("         %s" % str(line).strip())
        print("      arrival_contract_bindings (the LEDGER's own arrival rows):")
        print("         %r" % (record.get('arrival_contract_bindings'),))
        print("      result_family %r  result_width %r"
              % (record.get('result_family'), record.get('result_width')))
        print("      stored layer-5 text (LEFT of the theorem, LITERAL):")
        print("         %s" % term_record.get('layer5_normalized_text'))
        print("      rule S (the stored text's rule)  : %s"
              % sorted(S.items(), key=lambda kv: kv[1]))
        print("      rule C (the check's composer)    : %s"
              % sorted(C.items(), key=lambda kv: kv[1]))
        if r.get('left'):
            print("      check_L2 left  : %s" % r['left'])
            print("      check_L2 right : %s" % r['right'])
        guard(unit)
    print("")
    print("   %s: %d row(s) with the SAME naming, %d with DIFFERENT naming"
          % (tag, agree, differ))
    return agree, differ

print("")
print("[2/4] every DISCREPANCY row, both naming rules, LITERAL")
report("the 19", disc)

print("")
print("[3/4] a control sample of PROVED rows, same two rules")
report("the control sample", control)

print("")
print("[4/4] the two rules over EVERY row that has a proved term")
same = 0
diff = 0
skipped = 0
allunits = set(r['unit'] for r in rows)
held2, terms2 = M.stream_store(allunits)
print("   peak RSS %d kB after streaming for all rows" % guard('stream all'))
per_outcome = {}
for r in rows:
    unit = r['unit']
    record = held2.get(unit)
    term_record = terms2.get(unit)
    if record is None or term_record is None or \
       term_record.get('outcome') != 'PROVED_ON_SHIP':
        skipped += 1
        continue
    u = dict(record); u['unit'] = unit
    walked = maker.transcribe(u)
    if walked.out_term is None:
        skipped += 1
        continue
    t = walked.out_term
    agreed = naming(rule_S(t)) == naming(rule_C(t))
    key = (r.get('outcome'), r.get('closed_by'), agreed)
    per_outcome[key] = per_outcome.get(key, 0) + 1
    if agreed:
        same += 1
    else:
        diff += 1
    guard(unit)
print("   rows with a proved term: %d" % (same + diff))
print("   same naming under both rules : %d" % same)
print("   different naming             : %d" % diff)
print("   skipped (no store record / no proved term / no term): %d" % skipped)
print("   by (outcome, closed_by, naming agrees):")
for key in sorted(per_outcome, key=str):
    print("      %-40s %d" % (str(key), per_outcome[key]))
print("   peak RSS %d kB" % guard('end'))
PY
echo "--- exit $?"
