# TASK 53 resume state (written before the work, updated as it lands)

READ FIRST: log 151 (task 53 brief), log 152 (canon38), log 147 sec 13
then 4.1 and 13.5, AgentMemory "ROUND 10 RULINGS".

## the files this task writes (all new; nothing reused is edited)
- layer4c.py            the transcription over canon38 ledgers
- census53.py           the driver (chunked, resumable)
- name_census4.py       the census builder
- audit53.py            the per-population figures
- acceptance53.py       the literal instances
- zero_regression53.py  canon38 and prior artifacts untouched
- guard53.py            the unmodified guard, one process

## state
- step 0 reading: DONE
- step 1 layer4c: IN PROGRESS

## state, updated
- layer4c.py: DONE (replay exact on 1,763 original units; 0 disagreements)
- census53.py: RUNNING (chunked; resume by re-running it -- it skips
  chunks already listed in layer4c_state.json)
- name_census4.py / audit53.py / acceptance53.py / guard53.py /
  zero_regression53.py: WRITTEN
- acceptance53_printed.txt: produced

## order to finish
1. census53.py  (until it prints "finished")
2. name_census4.py > name_census4_printed.txt
3. audit53.py    > audit53_printed.txt
4. acceptance53.py > acceptance53_printed.txt
5. zero_regression53.py > zero_regression53_printed.txt
6. guard53.py    LAST (it walks name_census4.json)

## the two corrections made mid-lap (recorded so they are not redone)
1. THE ARRIVAL BINDING.  ledger48's prelude emits vector arrivals
   first, so IN-0 is loaded into the first VECTOR family; its dataflow
   walk and canon38's own `arrival_contract_bindings` bind IN-i to
   arrival_families[i].  The two differ for a unit with both vector and
   general arrivals.  layer4c follows the WALK's binding, which is the
   ledger it transcribes.  Reported as a canon38 disagreement, not
   fixed here.
2. THE FLAG STATE LINK.  A flag-reading row takes its flags ONLY from
   the row ledger48 put first in its operand list.  An earlier fallback
   that searched the rest of the operand list was removed: a reader's
   own destination operand can resolve to an unrelated row carrying a
   flag state (c/regen_36623 answered from a shift's flags).

## FINISHED 2026-09-03
All six steps ran; log written to
`PRIVATE/PseudoCoupHQ/DevComms/log_153_task53_layer4_canon38_census.md`
and a dated entry appended under PROGRESS.md's single `# PROGRESS` heading.
Census: 54 producers / 1,719 rows / 1,668 units.
Guard: 334 PASS, 0 FAIL, 0 exempt, exit 0.
