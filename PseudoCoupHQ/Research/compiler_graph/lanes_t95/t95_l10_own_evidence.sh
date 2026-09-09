#!/usr/bin/env bash
# t95 lane 10 -- THE LOG'S OWN EVIDENCE, printed as `$ command` followed by
# its output, so every claim log_200 makes carries something that re-runs.
#
# Node: hq.research.compiler_graph.graph, heading "the arch-opcode-node".
# Convention: hq.conventions, and the shape task 90's
# check_conventions_log_claims.py can actually re-run -- a shell
# transcript, read-only, every path a container path.
#
# THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
# second violation). No operator token may appear in ANY key, grouping,
# pairing, row structure, candidate selection, or comparison scope,
# anywhere in this line -- not in matching, not in "which pairs get
# compared", not in report rows, not in dropdowns. The candidate set for
# comparison comes from machine-form evidence (clusters, connections,
# type pairs) or from ratified intention -- never from the token. The
# token appears exactly once per unit: as a display label on the member.
# HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
# campaign's cross-language matrix (caught by the owner 2026-08-24);
# (2) verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix
# brief itself reintroduced it as "same-operator pairs"). MECHANICAL
# GUARD REQUIRED: every pipeline stage that groups or pairs units must
# run the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
# refuse its own output on failure.
set -u
run() { echo; echo "\$ $*"; eval "$@" 2>&1; }
say() { echo; echo "======== $* ========"; }

say "[1/8] the four-state marking, and that the four states partition"
run "python3 -c \"import json;d={l:json.load(open('/projects/PseudoCoupGraphs/arch_opcode_nodes_%s.json'%l)) for l in ('go','cpp','rust','swift')};[print(l, d[l]['by_state'], 'sum', sum(d[l]['by_state'].values()), 'population', d[l]['populations']['definitions']) for l in d]\""

say "[2/8] the emitter census and the call sites, per region"
run "python3 -c \"import json;[print(l, json.load(open('/projects/PseudoCoupGraphs/arch_opcode_nodes_%s.json'%l))['emitter_census']) for l in ('go','cpp','rust','swift')]\""
run "python3 -c \"import json;[print(l, json.load(open('/projects/PseudoCoupGraphs/arch_opcode_nodes_%s.json'%l))['by_state_of_call_sites']) for l in ('go','cpp','rust','swift')]\""

say "[3/8] the shrink"
run "python3 -c \"import json;[print(l, json.load(open('/projects/PseudoCoupGraphs/arch_opcode_nodes_%s.json'%l))['shrink']) for l in ('go','cpp','rust','swift')]\""

say "[4/8] the inverse index, and go's 24 x86 constants recounted from the artifact"
run "python3 -c \"import json;[print(l, json.load(open('/projects/PseudoCoupGraphs/arch_opcode_nodes_%s.json'%l))['distinct_arch_opcodes'], json.load(open('/projects/PseudoCoupGraphs/arch_opcode_nodes_%s.json'%l))['distinct_pseudo_opcodes']) for l in ('go','cpp','rust','swift')]\""
run "python3 -c \"import json;d=json.load(open('/projects/PseudoCoupGraphs/arch_opcode_nodes_go.json'));s=[c for c in d['call_sites'] if c['emitter']=='Prog' and c['state']=='names_its_opcode' and c['opcodes']];o=sorted({k['text'] for c in s for k in c['opcodes']});print(len(s),'Prog sites name an arch constant;',len(o),'distinct:');print(' '.join(o))\""

say "[5/8] swift -- the one call site where the compiler spells an instruction"
run "python3 -c \"import json;d=json.load(open('/projects/PseudoCoupGraphs/arch_opcode_nodes_swift.json'));[print(c['file']+':'+str(c['line']), c['state'], c['argument']['text'], [k['text'] for k in c['opcodes']]) for c in d['call_sites']]\""

say "[6/8] rust -- the named frontier, quoted from the artifact"
run "python3 -c \"import json;d=json.load(open('/projects/PseudoCoupGraphs/arch_opcode_nodes_rust.json'));print(d['unmeasured_by_absence_of_an_emitter'])\""

say "[7/8] the static emitter set against what running the compiler showed"
run "python3 -c \"import json;a=json.load(open('/projects/PseudoCoupGraphs/arch_opcode_nodes_go.json'));c=json.load(open('/projects/PseudoCoupHQ/Research/compiler_graph/coverage_go_files.json'));e={r['id'] for r in a['definitions_marked'] if r['state']!='emits_nothing'};v=set(c['per_def_visitors']);n={r['id'] for r in c['never_visited_rows']};print('go emitters',len(e),'entered',len(v),'both',len(e\\&v),'emitters instrumented but entered by none',len(e\\&n),'emitters never instrumented',len(e-v-n),'entered emitting nothing',len(v-e))\""
run "python3 -c \"import json;a=json.load(open('/projects/PseudoCoupGraphs/arch_opcode_nodes_cpp.json'));c=json.load(open('/projects/PseudoCoupHQ/Research/compiler_graph/coverage_cpp_files.json'));e={r['id'] for r in a['definitions_marked'] if r['state']!='emits_nothing'};v=set(c['per_def_visitors']);n={r['id'] for r in c['never_visited_rows']};print('cpp emitters',len(e),'entered',len(v),'both',len(e\\&v),'emitters instrumented but entered by none',len(e\\&n),'emitters never instrumented',len(e-v-n),'entered emitting nothing',len(v-e))\""

say "[8/8] the guard transcript, and the guard's own md5"
run "md5sum /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py"
run "cat /projects/PseudoCoupHQ/Research/compiler_graph/guard_task95.txt"
run "grep -c exempt /projects/PseudoCoupHQ/Research/compiler_graph/guard_task95.txt"
run "md5sum /projects/PseudoCoupGraphs/arch_opcode_nodes_go.json /projects/PseudoCoupGraphs/arch_opcode_nodes_cpp.json /projects/PseudoCoupGraphs/arch_opcode_nodes_rust.json /projects/PseudoCoupGraphs/arch_opcode_nodes_swift.json"

say "lane 10 done"
