# log_207 -- task o1, cross_construction map

This log belongs to the arch_unit_oracle line, node
`node_0_3_8_arch_unit_oracle/node_0_3_8_2_cross_construction`. It is
the FIRST measurement on that node, and does not touch
`Research/op_pipeline/` -- it only READS the pool and term store the
main line already wrote.

## 1. What a construction is, one sentence

A construction of y from x is a y arch-unit whose computation can be
written as a composition of x arch-units: length one when the same
pool entry already carries both an x member and a y member, length
two when y's layer-5 term equals an x term with its variables
replaced by other x terms (CORE_0_3_8_2_cross_construction.md,
"definition").

## 2. The length-one matrix, with quoted instances

Script: `Research/oracle/cross_construction/cross1_length_one.py`,
lane `o1_l2_cross1.sh`. It reads
`Research/op_pipeline/the_pool5.json` (1,831 entries) and, for every
ordered language pair (x, y), splits the entries carrying a y member
into BUILT (also carry an x member) and NOT_BUILT.

The pool holds nine language labels; five have enough entries to
form a matrix (the coordinator's corpus-five), the other four are
one or two entries each and are reported separately, not folded into
the matrix as zero:

- matrix languages, entry counts: c 921, cpp 1032, swift 351, go
  137, rust 109.
- low-count languages present, excluded from the matrix: java 2,
  cpython 1, php 1, ruby 1.
- all five matrix languages present together in one entry: 60
  entries (`all_five_language_entries.count` in
  `cross1_length_one.json`), confirming the coordinator's count.

```
$ python3 -c "
import json
d=json.load(open('Research/oracle/cross_construction/cross1_length_one.json'))
print(d['languages_pool_holds'])
print(d['matrix_languages'])
print(d['all_five_language_entries']['count'])
"
{'c': 921, 'cpp': 1032, 'cpython': 1, 'go': 137, 'java': 2, 'php': 1, 'ruby': 1, 'rust': 109, 'swift': 351}
['c', 'cpp', 'swift', 'go', 'rust']
60
```

The length-one matrix, cell = `built / total_y_entries (percent)`,
x down, y across:

| x \ y | c | cpp | swift | go | rust |
|---|---|---|---|---|---|
| c | -- | 474/1032 (45.9%) | 85/351 (24.2%) | 64/137 (46.7%) | 79/109 (72.5%) |
| cpp | 474/921 (51.5%) | -- | 92/351 (26.2%) | 64/137 (46.7%) | 84/109 (77.1%) |
| swift | 85/921 (9.2%) | 92/1032 (8.9%) | -- | 61/137 (44.5%) | 69/109 (63.3%) |
| go | 64/921 (6.9%) | 64/1032 (6.2%) | 61/351 (17.4%) | -- | 62/109 (56.9%) |
| rust | 79/921 (8.6%) | 84/1032 (8.1%) | 69/351 (19.7%) | 62/137 (45.3%) | -- |

One quoted example per direction (built entry + its layer-5 text,
not-built entry + its layer-5 text), from
`cross1_length_one.json.examples_per_pair`:

```
$ python3 -c "
import json
d=json.load(open('Research/oracle/cross_construction/cross1_length_one.json'))
for key in ['c|cpp','cpp|c','swift|go','go|rust','rust|cpp']:
    print(key, d['examples_per_pair'][key])
"
c|cpp {'built': {'entry_id': 'E00001', 'x_text': 'If(Extract(31, 0, v0) == 0, 1, 0)', 'y_text': 'If(Extract(31, 0, v0) == 0, 1, 0)'}, 'not_built': {'entry_id': 'E00240', 'y_text': 'If(v0 == 0, 0, 1) | If(Extract(31, 0, v1) == 0, 0, 1)'}}
cpp|c {'built': {'entry_id': 'E00001', 'x_text': 'If(Extract(31, 0, v0) == 0, 1, 0)', 'y_text': 'If(Extract(31, 0, v0) == 0, 1, 0)'}, 'not_built': {'entry_id': 'E00005', 'y_text': 'Concat(0, Extract(7, 1, v0), ~Extract(0, 0, v0))'}}
swift|go {'built': {'entry_id': 'E00006', 'x_text': '~Extract(31, 0, v0)', 'y_text': '~Extract(31, 0, v0)'}, 'not_built': {'entry_id': 'E00058', 'y_text': 'Extract(31, 0, v0)*Extract(31, 0, v1)'}}
go|rust {'built': {'entry_id': 'E00006', 'x_text': '~Extract(31, 0, v0)', 'y_text': '~Extract(31, 0, v0)'}, 'not_built': {'entry_id': 'E00074', 'y_text': 'Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, v0) >> 31, Extract(31, 0, v0)), Concat(Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 0, v1))))'}}
rust|cpp {'built': {'entry_id': 'E00006', 'x_text': '~Extract(31, 0, v0)', 'y_text': '~Extract(31, 0, v0)'}, 'not_built': {'entry_id': 'E00001', 'y_text': 'If(Extract(31, 0, v0) == 0, 1, 0)'}}
```

Attribution: `Research/oracle/cross_construction/cross1_length_one.py`, run as
lane `o1_l2_cross1.sh`, log
`~/AirlockRuns/o1/agent/logs/20260906T002436Z__o1_l2_cross1.sh.log`
(o1's own run dir -- the daemon writes there per instance, distinct
from the default instance's `~/Programming/Airlock/agent/logs/`).
Peak RSS (children, `resource.getrusage`) 95,620 KB = 93.4 MB,
against the 2 GB bound (`ABORT_MEMORY_O1`, not raised).

## 3. The parser round-trip result

Deliverable B needs the layer-5 texts parsed into trees (z3's python
print form: infix with precedence, `Name(args)` calls, integer
literals, `v<N>` variables). A hand-written recursive-descent parser
was written and tested by re-printing every parsed tree and
comparing to the original text, over all 1,267 distinct layer-5
texts in the pool.

First run found 297 failures, all one cause: the tokenizer's
operator-character set omitted `~` entirely, so every text
containing a bitwise-not raised `ValueError` before printing was
even reached. That is a parser defect, fixed once in the tokenizer
(added `~` to `ONE_CHAR_OPS`), not 297 per-text patches.

```
$ python3 Research/oracle/cross_construction/cross2_length_two.py 2>&1 | head -6
round-trip: 1267 distinct layer-5 texts, 22 failures
FAILURE text: Concat(0, fp.to_ieee_bv(fpToFP(Concat(Extract(15, 0, v0), 0)) * fpToFP(Extract(31, 0, v1))))
  reprinted: Concat(0, fp.to_ieee_bv(fpToFP(Concat(Extract(15, 0, v0), 0))*fpToFP(Extract(31, 0, v1))))
  error: None
FAILURE text: Concat(Extract(63, 32, v0), fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) * fpToFP(Concat(Extract(15, 0, v1), 0))))
  reprinted: Concat(Extract(63, 32, v0), fp.to_ieee_bv(fpToFP(Extract(31, 0, v0))*fpToFP(Concat(Extract(15, 0, v1), 0))))
```

The remaining 22 failures are one cause too, and a genuine ambiguity
in the source notation rather than a parser bug: integer
multiplication prints `*` with NO surrounding spaces
(`2*(If(...)`, `Extract(31, 0, v0)*Extract(31, 0, v1)` -- confirmed
by grepping all 1,267 texts for `.{3}\*.{3}` before writing the
printer), but floating-point multiplication inside `fp.to_ieee_bv`
prints `*` WITH spaces (`fpToFP(...) * fpToFP(...)`). The syntax
alone does not carry which case a given `*` is in without deeper
type context this task does not build (no z3 proving in this task,
section 5). Per the brief's stop rule, these 22 texts are reported
and EXCLUDED from length-two matching, not patched per text.

Attribution: same lane, `o1_l4_cross2.sh`, log
`~/AirlockRuns/o1/agent/logs/20260906T002905Z__o1_l4_cross2.sh.log`.
Peak RSS 96,324 KB = 94.1 MB.

## 4. The length-two matrix, with quoted constructions

For every ordered pair (x, y), every y entry NOT built at length one
was tested for length-two constructibility from x: y's tree matches
some x pattern at the root (x's tree with each `v<N>` a hole), and
every hole's bound subtree is either a variable/literal or itself
matches some x pattern whose own holes bind only to variables or
literals (depth 2 exactly, section 4 of the brief). The whole run
finished in 9.6s wall clock, well under the 30-minute-per-lane
sampling threshold, so no pair was sampled
(`lane_deadline_hit_any_pair: false` in `cross2_length_two.json`).

Cell = `built_len2 / not_built_len1 (percent)`:

| x \ y | c | cpp | swift | go | rust |
|---|---|---|---|---|---|
| c | -- | 7/558 (1.3%) | 4/266 (1.5%) | 0/73 (0.0%) | 0/30 (0.0%) |
| cpp | 0/447 (0.0%) | -- | 4/259 (1.5%) | 0/73 (0.0%) | 0/25 (0.0%) |
| swift | 24/836 (2.9%) | 29/940 (3.1%) | -- | 1/76 (1.3%) | 1/40 (2.5%) |
| go | 17/857 (2.0%) | 22/968 (2.3%) | 5/290 (1.7%) | -- | 0/47 (0.0%) |
| rust | 23/842 (2.7%) | 28/948 (3.0%) | 5/282 (1.8%) | 0/75 (0.0%) | -- |

Note the denominator here is `not_built_len1_count` read straight
from `cross1_length_one.json`, before the 22 round-trip-excluded y
texts are dropped from the numerator's search -- so the percentage
is a slight undercount of what a text-complete parser would find,
stated once here rather than re-derived per cell.

Three constructions in full, from
`cross2_length_two.json.quoted_constructions_sample`:

```
$ python3 -c "
import json
d=json.load(open('Research/oracle/cross_construction/cross2_length_two.json'))
for c in d['quoted_constructions_sample'][:3]:
    print(c['pair'], c['entry_id'])
    print(' y:', c['y_text'])
    print(' root x pattern:', c['construction']['root_x_pattern_text'], c['construction']['root_x_example_entry'])
    print(' bindings:', c['construction']['bindings'])
"
c|cpp E00240
 y: If(v0 == 0, 0, 1) | If(Extract(31, 0, v1) == 0, 0, 1)
 root x pattern: v0 | v1 E00141
 bindings: {'v0': {'bindings': {'v0': 'v0', 'v1': '0'}, 'kind': 'matched_x_pattern', 'text': 'If(v0 == 0, 0, 1)', 'x_example_entry': 'E00167', 'x_pattern_text': 'If(v0 == v1, 0, 1)'}, 'v1': {'bindings': {'v0': 'v1', 'v1': '1'}, 'kind': 'matched_x_pattern', 'text': 'If(Extract(31, 0, v1) == 0, 0, 1)', 'x_example_entry': 'E00066', 'x_pattern_text': 'If(Extract(31, 0, v0) == 0, 0, v1)'}}
c|cpp E01070
 y: If(Extract(31, 0, v0) == 0, 0, 1) | If(v1 | v2 == 0, 0, 1)
 root x pattern: v0 | v1 E00141
 bindings: {'v0': {'bindings': {'v0': 'v0', 'v1': '1'}, 'kind': 'matched_x_pattern', 'text': 'If(Extract(31, 0, v0) == 0, 0, 1)', 'x_example_entry': 'E00066', 'x_pattern_text': 'If(Extract(31, 0, v0) == 0, 0, v1)'}, 'v1': {'bindings': {'v0': 'v1', 'v1': 'v2'}, 'kind': 'matched_x_pattern', 'text': 'If(v1 | v2 == 0, 0, 1)', 'x_example_entry': 'E00116', 'x_pattern_text': 'If(v0 | v1 == 0, 0, 1)'}}
c|cpp E01268
 y: If(v0 <= 0, 0, 1)
 root x pattern: v0 E00011
 bindings: {'v0': {'bindings': {'v0': 'v0', 'v1': '0'}, 'kind': 'matched_x_pattern', 'text': 'If(v0 <= 0, 0, 1)', 'x_example_entry': 'E00182', 'x_pattern_text': 'If(v0 <= v1, 0, 1)'}}
```

Reading E00240: the y tree `A | B` matches x's root pattern
`v0 | v1` (a c entry, E00141) with hole v0 bound to the subtree
`If(v0 == 0, 0, 1)` and hole v1 bound to `If(Extract(31, 0, v1) == 0, 0, 1)`.
Neither bound subtree is a bare variable or literal, so each is
checked against x's patterns again: `If(v0 == 0, 0, 1)` matches c's
`If(v0 == v1, 0, 1)` (E00167) with v1 -> the literal `0`; the other
subtree matches c's `If(Extract(31, 0, v0) == 0, 0, v1)` (E00066)
with v1 -> the literal `1`. Both inner matches bind only to
variables/literals, so the depth-2 rule is satisfied and E00240 (a
cpp y-entry) is length-two-constructible from c.

Three y texts nothing matched, per the two largest cells (c|cpp,
cpp|c):

```
$ python3 -c "
import json
d=json.load(open('Research/oracle/cross_construction/cross2_length_two.json'))
for m in d['quoted_misses_sample'][:3]:
    print(m['pair'], m['entry_id'], m['y_text'])
"
c|cpp E00241 If(Extract(31, 0, v1) == 0, 0, 1) | If(fpIsNaN(fpToFP(Extract(31, 0, v0))), 1, 0) | If(Or(Not(fpEQ(fpToFP(Extract(31, 0, v0)), +0.0)), fpIsNaN(fpToFP(Extract(31, 0, v0)))), 1, 0)
c|cpp E00242 If(Extract(31, 0, v1) == 0, 0, 1) | If(fpIsNaN(fpToFP(Extract(63, 0, v0))), 1, 0) | If(Or(fpIsNaN(fpToFP(Extract(63, 0, v0))), Not(fpEQ(fpToFP(Extract(63, 0, v0)), +0.0))), 1, 0)
c|cpp E00243 Extract(7, 0, v0) | If(Extract(31, 0, v1) == 0, 0, 1)
```

All three misses share a cause visible in the text: the tree is a
3-way `|` chain (right-associative, so its root is `A | (B | C)`),
and no single x pattern's root shape is a 3-term `|`, so no root
match is even attempted -- a length-three (or a right-associated
partial) construction, out of this task's depth-2 scope (section 5).

Attribution: same lane and log as section 3.

## 5. What the two matrices say, in plain words

- **Most capable builder, length one: cpp**, built from cpp cell
  values row-wise (51.5% of c, 26.2% of swift, 46.7% of go, 77.1% of
  rust) -- cpp's row has the highest entry in three of its four
  cells, and c's row is close behind (cpp built 51.5% of c's
  entries; c built 45.9% of cpp's, the next-highest pair). This
  reads directly from the matrix in section 2: cpp and c are each
  built from the other at rates roughly 4-5x any row from
  swift/go/rust.
- **Hardest to build, length one: go**, whose row has the lowest
  values against c (6.9%) and cpp (6.2%) of any row -- go's own
  arch-units are the least reusable as building blocks for c/cpp,
  even though go itself gets built at moderate rates from every
  other language (44.5%-56.9% down its column).
- **Why, from the quoted texts:** the go|rust not-built example
  quoted in section 2 (E00074) is a 32-way `Concat` of the same
  `Extract(31, 31, v1)` repeated, the sign-extension idiom for a
  32-bit division -- a shape c/cpp's compiled units do not carry
  because c/cpp's div/mod arch-units use the `idiv` instruction
  directly rather than expanding sign-extension into the term, so
  their layer-5 texts stay short (compare `E00001`'s
  `If(Extract(31, 0, v0) == 0, 1, 0)`, four tokens deep). A
  building-block language's terms recur across other languages'
  entries because they are short and shape-generic (`v0 | v1`,
  `If(v0 == v1, 0, 1)`); go's div/mod terms are long and
  self-specific, so nothing else's pool entry matches them and go
  is rarely the x that builds another y either -- but the LENGTH-TWO
  matrix (section 4) shows the opposite question (what CAN be
  BUILT FROM go) sits in the 44-57% range at length one, meaning
  go's short terms (shifts, extracts, bitwise) are reused often; it
  is specifically go's own long division-idiom terms that make go a
  weak x.

## 6. Lane logs and the verifier tally

- lane `o1_l2_cross1.sh`: `~/AirlockRuns/o1/agent/logs/20260906T002436Z__o1_l2_cross1.sh.log`
- lane `o1_l4_cross2.sh`: `~/AirlockRuns/o1/agent/logs/20260906T002905Z__o1_l4_cross2.sh.log`
- guard: `check_no_spelling_keys.py` PASS on both
  `cross1_length_one.json` and `cross2_length_two.json` (section 0
  of the brief), re-run in lane `o1_l5_verify.sh`.
- verifier: `check_conventions_log_claims.py --verify` over this log,
  run FROM o1 in lane `o1_l5_verify.sh`. Tally pasted below once run.

Verifier tally, `check_conventions_log_claims.py --verify` over this
log, lane `o1_l8_verify.sh`, log
`~/AirlockRuns/o1/agent/logs/20260906T003609Z__o1_l8_verify.sh.log`:

```
claims 7 | MATCHES 5 | DIFFERS 0 | UNVERIFIABLE 2 | REFUSED 0 | NOT_RERUNNABLE 0
ONE LINE: 5 of 7 claims reproduce; 2 (29%) carry nothing to re-run
```

The 2 UNVERIFIABLE claims are both prose with no command beside
them (the `*`-spacing-ambiguity explanation in section 3, and the
decided/awaiting split in section 7) -- named honestly rather than
dressed up as re-run evidence. Zero DIFFERS.

## 7. Decided / awaiting the owner

- **Decided, recorded for audit:** the matrix languages are the
  pool's five (c, cpp, swift, go, rust); the four other language
  labels present (java, cpython, php, ruby, 1-2 entries each) are
  reported by count, not folded into a matrix cell; the 22
  round-trip-ambiguous `*`-spacing texts are excluded from
  length-two matching rather than patched; length-two search is
  exactly depth 2, no recursion further, per the brief.
- **Awaiting the owner:** nothing beyond what task o2 is already scheduled
  to confirm at the gate (body-level PROVED verdicts over the
  length-one and length-two compositions this task found at the
  term level only -- section 5 of the brief: "no z3 proving in this
  task").
