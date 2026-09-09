#!/bin/bash
# TASK 96 round 19, lane 9.  The %r15 count, re-run after lane 8's own
# format-string fault (a literal %r15 inside a python format string).
set -x
cd PseudoCoupHQ/Research/op_pipeline
echo "[1/2] the compiled population and its %r15 count"
python3 -c "
import json
total = 0
hits = 0
seen = 0
for lang in ('c', 'cpp', 'go', 'rust', 'swift'):
    units = json.load(open('canon40_wrapped_%s.json' % lang))['units']
    total = total + len(units)
    for label in units:
        text = units[label].get('wrapped_text')
        if text is None:
            continue
        seen = seen + 1
        if '%r15' in text:
            hits = hits + 1
print('compiled units in the canon40 render : %d' % total)
print('of those, carrying a wrapped text    : %d' % seen)
print('wrapped texts containing the r15 name: %d' % hits)
"
echo "[2/2] the same, as a grep that does not go through a loader"
grep -o '\"wrapped_text\": \"[^\"]*%r15[^\"]*\"' canon40_wrapped_c.json canon40_wrapped_cpp.json canon40_wrapped_go.json canon40_wrapped_rust.json canon40_wrapped_swift.json | wc -l
echo done
