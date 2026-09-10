# log 179 — task 70: the selector and the arch opcode index over the whole population

Node: `hq.research.compiler_graph.dashboard`
(`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_10_dashboard/CORE_0_3_5_10_dashboard.md`),
methods `selector` and `opcode_index`.
Brief: log_172 task 70. Date: 2026-09-03.

---

# 1. What was done, in plain words

Two of the six things the owner numbered on the dashboard are a SELECTOR and an
ARCH OPCODE INDEX. Both terms first, because everything below rests on
them.

- The **selector** is the panel on pane 1 that narrows 31,078 arch-units
  down to the one you want: a random button, then three menus —
  language, then operator, then TYPE SIGNATURE — then a box to type a
  unit id into.
- A **type signature** is the shape of the thing the probe asked the
  compiler to compile: `(a: uint16, b: int32) -> uint16` means one probe
  took an unsigned 16-bit integer and a signed 32-bit integer and gave
  back an unsigned 16-bit integer. It is the probe's DECLARED types,
  with the result read off the unit's own OUT row when the compiler
  stated no result type.
- The **arch opcode index** is pane 2: every machine instruction
  mnemonic that appears in any unit's body — `ret`, `mov`, `movss` —
  and, under each, which groups of units it turns up in.

Task 68 built both, and named the hole it left. A unit's signature is
not in the unit; it is in the probe manifest, and the manifests are big,
so the live page filled a signature in only when a unit was clicked. The
signature menu was therefore empty, and the arch opcode index grouped
everything under "no signature recorded". Task 70 closes that.

What it now costs and what it now shows, measured:

- **31,067 of 31,078** index rows carry a type signature. The **11**
  that do not are the interpreter handlers, which have no probe at all
  (cpython 1, java 2, php 4, ruby 4).
- The signature menu lists **3,390** signatures, the operator menu
  **131** operator groups, the language menu **9** languages.
- The arch opcode index runs over **162** arch opcodes and **151,279**
  (language, operator group, signature) groups.
- Getting there costs **398 ms of wall clock** to read 94.2 MB of probe
  manifest and **668 ms** in total from the unit index landing to both
  panes being ready — in an interactive Chrome, with real timers.
- The spelling ban was RUN, not asserted: with every operator label
  replaced by a glyph, a script clicked **5 panes, 10 language entries,
  272 operator-group entries, 3,391 type-signature entries, 162 arch
  opcode entries, 37,483 opcode narrowing-menu entries, 9 unit rows and
  63 viewer modes — 0 errors**.

Two defects were found by running it rather than by reasoning about it,
and both are stated in section 6 rather than quietly fixed.

---

# 2. The signature, with values in motion

## 2.1 The rule, and where it already lived

The rule is `DashboardJoin.signatureOf`, written in task 68 and ported
from `viewer_build.py`. This work CALLS it; it does not restate it.
LITERAL, `Research/op_pipeline/dashboard_join.js` lines 169–191:

```javascript
  function signatureOf(probe, unit) {
    if (!probe) { return null; }
    var lhs = probe.lhs_type;
    var rhs = probe.rhs_type;
    var res = probe.result_type;
    if (!res) {
      var ledger = unit.ledger || [];
      var out = ledger.filter(function (r) {
        return String(r.row).indexOf("OUT") === 0;
      });
      if (out.length) { res = String(out[0].size * 8) + "-bit"; }
      else { res = "compiler-stated"; }
    }
    if (rhs) { return "(a: " + lhs + ", b: " + rhs + ") -> " + res; }
    return "(a: " + lhs + ") -> " + res;
  }
```

GLOSS: the declared types come from the probe; the result comes from the
probe too, unless the compiler was asked to state it itself, in which
case the width of the unit's own OUT row is the answer.

## 2.2 One unit, walked through

Take `c/op_0`, the first unit in the corpus.

**Step 1 — the unit's own record.** LITERAL, from
`canon39_wrapped_c.json`, the fields that matter here:

```
  "unit": "c/op_0",  "lang": "c",  "n": "0",
  "population": "original",  "operator": "!",
  "ledger": [ … , { "row": "OUT-0", "size": 1, … } ]
```

So the probe number is `0`, the population is `original`, and the OUT
row is 1 byte wide.

**Step 2 — the manifest row that probe number names.** `population`
picks the file: `original` means `probe_manifest_c.json`, `regenerated`
means `probe_manifest2_c.json`. LITERAL, `probe_manifest_c.json`,
probe 0:

```
  "n": 0, "operator": "!", "lhs_type": "int32_t",
  "rhs_type": null, "result_type": null,
  "result_rule": "compiler_states_it_typeof"
```

**Step 3 — the two joined.** `result_type` is null, so the result is
read off OUT-0: `1 * 8 = 8`. `rhs_type` is null, so the signature is
unary:

```
  (a: int32_t) -> 8-bit
```

That string is what the third menu lists, what the opcode index groups
by, and what the unit header prints. The operator token `!` is nowhere
in it.

## 2.3 The same walk over 31,078 units, and the 11 that stop

The join above needs the probe number and the OUT row's width for every
unit. Both are in the shard document that the background index pass
already has open, so `dashboard_pane23.js` wraps
`LiveSource.prototype.absorb` and keeps them on the index row as it goes
by. Reading them later would mean re-reading 233 MB of shards.

The 11 that get no signature are not a failure and are not hidden. They
are the interpreter handlers — `cpython/long_add_fastpath`, `java/op_1`,
and so on — which were not produced by a probe, so there is no declared
type to read. LITERAL, the page's own console line:

```
[pane23] signatures filled: 31067 of 31078 rows; 31067 rows now carry
one; 11 do not (cpython, population interpreter: 1; java, population
interpreter: 2; php, population interpreter: 4; ruby, population
interpreter: 4); 3390 distinct signatures; 131 operator groups;
9 languages
```

---

# 3. Reading 94 MB of manifest without parsing it

## 3.1 Why a shortcut was needed

The ten probe manifests total **94,162,163 bytes**, of which
`probe_manifest2_cpp.json` alone is 50 MB and `probe_manifest2_c.json`
is 37 MB. They are that size because every probe carries its whole
source text. Three fields per probe are wanted — `lhs_type`,
`rhs_type`, `result_type` — and all three are written before `source`
in every one of them.

## 3.2 The shortcut, and the proof that it is exact

`dashboard_pane23.js` reads each manifest as TEXT and runs one regular
expression over it, keeping the three fields and dropping the text. A
match that runs longer than 2,000 characters would mean it had crossed
out of one probe object into the next, so such a match is counted and
refused rather than kept.

The shortcut is not asserted. `pane23_manifest_regex_check.py` runs THE
SAME expression in python over all ten manifests and compares its result,
probe for probe, with `json.load`:

```
$ /tmp/reconnect_venv/bin/python3 pane23_manifest_regex_check.py
PASS probe_manifest_c.json         750 probes, identical to json.load (0 spans over the 2000-character ceiling, skipped)
PASS probe_manifest2_c.json      51829 probes, identical to json.load (0 spans over the 2000-character ceiling, skipped)
PASS probe_manifest_cpp.json      1002 probes, identical to json.load (0 spans over the 2000-character ceiling, skipped)
PASS probe_manifest2_cpp.json    70991 probes, identical to json.load (0 spans over the 2000-character ceiling, skipped)
PASS probe_manifest_go.json        744 probes, identical to json.load (0 spans over the 2000-character ceiling, skipped)
PASS probe_manifest2_go.json       553 probes, identical to json.load (0 spans over the 2000-character ceiling, skipped)
PASS probe_manifest_rust.json      858 probes, identical to json.load (0 spans over the 2000-character ceiling, skipped)
PASS probe_manifest2_rust.json    1993 probes, identical to json.load (0 spans over the 2000-character ceiling, skipped)
PASS probe_manifest_swift.json    1086 probes, identical to json.load (0 spans over the 2000-character ceiling, skipped)
PASS probe_manifest2_swift.json   4187 probes, identical to json.load (0 spans over the 2000-character ceiling, skipped)
exit=0
```

- **LITERAL:** ten PASS lines, exit 0.
- **GLOSS:** over 133,993 probes the regular expression and `json.load`
  return the same three values for every probe, and no match ever ran
  past the end of a probe object.

## 3.3 What it costs, in real time

Measured in an interactive Chrome (the Browser pane, real timers, not
the headless harness's virtual clock), reading the ten manifests over
the byte-range test server:

```
> await window.__pane23   // the page's own console, verbatim
[pane23] declared types read: 133993 probes from 10 manifest files,
         94.2 MB of text, 0 spans over the ceiling, 0 files missing,
         in 398 ms
[pane23] signatures filled: 31067 of 31078 rows; … 3390 distinct
         signatures; 131 operator groups; 9 languages
[pane23] PANES 2 AND 3 READY over the full population in 668 ms
```

- **LITERAL:** 398 ms and 668 ms are `performance.now()` differences the
  page logged itself.
- **GLOSS:** the manifest read is 398 ms; filling 31,067 signatures and
  repainting both panes takes the rest, 668 ms in all. This work happens
  AFTER the background unit index lands (6.7 s, task 68's figure), so it
  changes nothing about first paint.

The per-file breakdown the page kept, read out of `window.__pane23`, is
the same as python's, file for file:

| manifest | probes, browser | probes, python |
|---|---:|---:|
| `probe_manifest_c.json` | 750 | 750 |
| `probe_manifest2_c.json` | 51,829 | 51,829 |
| `probe_manifest_cpp.json` | 1,002 | 1,002 |
| `probe_manifest2_cpp.json` | 70,991 | 70,991 |
| `probe_manifest_go.json` | 744 | 744 |
| `probe_manifest2_go.json` | 553 | 553 |
| `probe_manifest_rust.json` | 858 | 858 |
| `probe_manifest2_rust.json` | 1,993 | 1,993 |
| `probe_manifest_swift.json` | 1,086 | 1,086 |
| `probe_manifest2_swift.json` | 4,187 | 4,187 |
| **total** | **133,993** | **133,993** |

---

# 4. The two panes at full size

## 4.1 The selector

Screenshot: `DevComms/screens/log_179/selector_full_population.png`.

Its scope line, read off the image, is the mechanical-update rule
applied to this pane specifically — the shell's population line says
what was READ, this one says what the pane HOLDS:

> selector: 31,078 rows in the index · 9 languages · 131 operator groups
> · 3,390 type signatures over 31,067 of 31,078 units · 11 units have no
> signature (cpython, population interpreter: 1; java, population
> interpreter: 2; php, population interpreter: 4; ruby, population
> interpreter: 4) · 133,993 probes read from 10 manifest files

The menus, counted in the live page:

| menu | options | what they are |
|---|---:|---|
| language | 10 | 9 languages plus "every language" |
| operator | 132 | 131 opaque operator group ids plus "every operator" |
| type signature | 3,391 | 3,390 signatures plus "every signature" |

**Narrowing, with values in motion.** Screenshot
`DevComms/screens/log_179/selector_language_cpp.png`: language `cpp`,
signature `(a: _Float16) -> 32-bit`. The list falls to

```
  3 of 31,078 shown
    cpp/regen_2      !
    cpp/regen_217    not
    cpp/regen_544    sizeof
```

That is worth reading twice. Three units, one signature, THREE DIFFERENT
operator spellings — `!`, `not`, `sizeof`. They are together because
their types match, not because their tokens do. The tokens in the right
column are labels; nothing selected on them.

## 4.2 The arch opcode index

Screenshot: `DevComms/screens/log_179/opcode_index_ret.png`, on `ret`,
the opcode that appears in the most units.

Its scope line:

> arch opcode index: 162 arch opcodes over 31,078 units · 151,279
> (language, operator group, signature) groups · the token is a label on
> the member, never a key

And its per-language summary, read off the image:

| language | units | operator groups | type signatures |
|---|---:|---:|---:|
| c | 10,367 | 27 | 1,795 |
| cpp | 17,569 | 32 | 2,123 |
| cpython | 1 | 1 | 1 |
| go | 577 | 20 | 165 |
| java | 2 | 2 | 1 |
| php | 4 | 1 | 1 |
| ruby | 2 | 1 | 1 |
| rust | 685 | 21 | 491 |
| swift | 1,225 | 26 | 268 |

## 4.3 The ceiling this pane needs, stated on the page

`ret` is in **30,432 units** and in **29,653** (language, operator group,
signature) groups. Drawing 29,653 collapsible sections is not a pane, it
is a hang. So the pane draws 200 and says so, in these words, on screen:

> Drawing 200 of 29,653 groups that match the menus above, out of 29,653
> groups this arch opcode appears in. Narrow by language or signature to
> see the rest.

and offers two menus — language and signature — to narrow them with. A
ceiling that is not printed beside the number it cut down from would be
a hidden sample; this one is printed with its population every time.

A narrower opcode shows the other end of the same behaviour:
`DevComms/screens/log_179/opcode_index_movss.png`.

---

# 5. THE SPELLING BAN

> THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
> second violation). No operator token may appear in ANY key, grouping,
> pairing, row structure, candidate selection, or comparison scope,
> anywhere in this line — not in matching, not in "which pairs get
> compared", not in report rows, not in dropdowns. The candidate set for
> comparison comes from machine-form evidence (clusters, connections,
> type pairs) or from ratified intention — never from the token. The
> token appears exactly once per unit: as a display label on the member.
> HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
> campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
> verdicts.py's row pairing (caught by the owner 2026-08-25 — the fix brief
> itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
> REQUIRED: every pipeline stage that groups or pairs units must run the
> spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
> its own output on failure. A brief handed to any subagent for this
> line MUST paste this paragraph verbatim.

## 5.1 What this work groups by

Every grouping, menu value and comparison added here is

```
  lang + "#" + opGroup + "#" + sig
```

`opGroup` is the opaque per-language id task 68 minted (`c#g07`); `sig`
is a type signature. Neither is a token. Values in motion, for
`cpp/regen_2` from section 4.1:

```
  u.lang    = "cpp"
  u.opGroup = "cpp#g11"                     <- the key
  u.label   = "!"                           <- printed, read by nothing
  u.sig     = "(a: _Float16) -> 32-bit"     <- the key
  k = "cpp#cpp#g11#(a: _Float16) -> 32-bit"
```

## 5.2 The test, RUN

`?labels=glyph` replaces every operator label with `◆`.
`pane23_clickthrough.py` then drives a real Chrome through every pane,
every menu entry and every arch opcode entry, counting what breaks.
LITERAL, the transcript:

```
========================================================================
RUN 1 -- the spelling-ban click-through, every label a glyph
========================================================================
[walk] first paint at 92 ms; 31078 units counted from 336 summary reads
[pane23] declared types read: 133993 probes from 10 manifest files, 94.2 MB of text, 0 spans over the ceiling, 0 files missing, in 30 ms
[pane23] signatures filled: 31067 of 31078 rows; 31067 rows now carry one; 11 do not (cpython, population interpreter: 1; java, population interpreter: 2; php, population interpreter: 4; ruby, population interpreter: 4); 3390 distinct signatures; 131 operator groups; 9 languages
[pane23] PANES 2 AND 3 READY over the full population in 30 ms
[walk] index complete at 6772 ms; 31078 units, 162 arch opcodes
[walk] glyph mode is ON (every operator label is a glyph)
[walk] panes on the page: 5
[walk] arch opcode entries in the index: 162
[walk] narrowing the biggest arch opcode by each of 10 language entries
[walk] selector language entries: 10
[walk] selector type signature entries: 3391
[walk] DONE {
 "counts": {
  "panes_clicked": 5,
  "language_entries": 10,
  "operator_group_entries": 272,
  "signature_entries": 3391,
  "unit_rows_clicked": 9,
  "opcode_entries": 162,
  "opcode_group_menu_entries": 37483,
  "unit_modes_clicked": 63,
  "text_filters": 1,
  "labels_checked": 600,
  "labels_not_a_glyph": 0,
  "non_label_tags_in_the_list": 1
 },
 "errors": 0,
 "error_list": [],
 "glyph_mode": true,
 "elapsed_ms": 9162
}
```

- **LITERAL:** the counts above are what the page counted as it clicked.
  `errors` counts every `window.onerror`, every unhandled promise
  rejection, every `console.error`, and every pane, menu or list that
  drew nothing when it was clicked. It is 0.
- **GLOSS:** every one of the 162 arch opcode entries was clicked and
  drew its pane; every one of the 3,391 type-signature entries, 272
  operator-group entries and 10 language entries was selected and the
  list redrew; all 5 panes opened; 9 units were opened and all 63 of
  their viewer modes clicked. 600 labels were checked and every one of
  them was `◆`. The one element in the list that is NOT a glyph is
  counted separately and named: it is the list's overflow notice
  ("…30,478 more, narrow the filter"), which is not a label.

Screenshots of the same state: `glyph_selector.png`,
`glyph_opcode_index.png`. The second is worth comparing with
`opcode_index_ret.png` — the counts, the groups and the signatures are
identical; only the labels changed.

## 5.3 The seeded sampler, and the reload

A sample is only reproducible if BOTH halves of it are in the address:
the seed, and the scope the seed indexes into. So the address carries
`seed=` and `scope=`, the scope being the four selector controls.

Values in motion, for the seed in the transcript below: the filtered
list is all 31,078 rows, and `20260903 mod 31078 = 29,125`, so row
29,125 of the index is the sample — `go/regen_348`. Load the same
address again and the same arithmetic runs on the same list.

```
========================================================================
RUN 2 -- the seeded sampler: the SAME address loaded twice
         seed=20260903, carried in the address hash
========================================================================
load 1: [pane23] seed 20260903 over 31078 filtered rows -> go/regen_348 (address bar on load)
load 2: [pane23] seed 20260903 over 31078 filtered rows -> go/regen_348 (address bar on load)

RELOAD DETERMINISM: SAME unit on both loads
```

Screenshot `DevComms/screens/log_179/seeded_sample.png` is that unit as
the address alone opened it: `go/regen_348`, signature
`(a: uint16, b: int32) -> uint16`, population regenerated, verdict
`PROVED_ON_SHIP`, with its go source beside it.

## 5.4 The guards, unmodified, one process each

**Over the data this work emits.** `pane23_ground_truth.json` is the
whole index recomputed in python (section 6.1) and is walked by the
guard:

```
$ git -C PRIVATE/PseudoCoupHQ status --porcelain \
      Research/op_pipeline/check_no_spelling_keys.py
(no output: unmodified)
$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py pane23_ground_truth.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS pane23_ground_truth.json -- no operator token in any key, grouping, pairing or row structure
exit=0
```

**Over this work's own code:**

```
$ /tmp/reconnect_venv/bin/python3 check_dashboard_js_no_spelling.py dashboard_pane23.js
operator inventory: 91 tokens read from probe_manifest_*.json
PASS dashboard_pane23.js -- no operator token is written as a literal, so none can be a key (0 named coincidences above)
exit=0
```

Note the `0` in that line. Task 68's files needed three named
coincidences (`&`, `<`, `/`); this file needs none — it contains no
string literal that is an operator token at all.

## 5.5 The guard caught something real, and the shape moved, not the guard

The first emission of `pane23_ground_truth.json` FAILED:

```
$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py pane23_ground_truth.json
FAIL pane23_ground_truth.json -- 8 spelling-keyed place(s)
     $.opcode_groups.and
         dict key is the operator token 'and'
     $.opcode_groups.not
         dict key is the operator token 'not'
     $.opcode_groups.or
         dict key is the operator token 'or'
     $.opcode_groups.xor
         dict key is the operator token 'xor'
     $.opcode_units.and
         dict key is the operator token 'and'
     …
```

- **LITERAL:** eight findings, all on four names.
- **GLOSS:** `and`, `or`, `xor` and `not` are x86 instruction mnemonics,
  read out of objdump — machine-form evidence, which is exactly what the
  ban says a candidate set MAY come from. They are ALSO C++'s
  alternative spellings for operators, so they are in the 91-token
  inventory. A json dict key cannot carry that distinction, and the
  guard is right to refuse it.

The fix was not to widen the guard and not to name an exception. The
emitted shape moved: the arch opcode index is now a LIST OF ROWS keyed
by an opaque arch id, with the mnemonic carried as `mnem`, a value:

```json
  "arch_opcodes": [
   { "arch_id": "arch#000", "mnem": "adc", "units": 178, "groups": 178 },
   …
   { "arch_id": "arch#128", "mnem": "ret", "units": 30432, "groups": 29653 },
```

No exception was named anywhere. Counted: over all seven code and
rig files this task wrote, the word that would name one appears 0
times — `dashboard_pane23.js` 0, `pane23_ground_truth.py` 0,
`pane23_manifest_regex_check.py` 0, `pane23_clickthrough.html` 0,
`pane23_clickthrough.py` 0, `pane23_shot.html` 0, `pane23_shot.py` 0.
(It appears once in this log: in this sentence.)

---

# 6. The numbers were checked against python, not trusted

## 6.1 The off-page arithmetic

`pane23_ground_truth.py` recomputes the whole index in python, over the
same files on disk, with the same rule. It is not part of the dashboard
and the dashboard does not know it exists.

```
$ /tmp/reconnect_venv/bin/python3 pane23_ground_truth.py
manifests: 10 files, c/original=750 probes, c/regenerated=51829 probes, cpp/original=1002 probes, cpp/regenerated=70991 probes, go/original=744 probes, go/regenerated=553 probes, rust/original=858 probes, rust/regenerated=1993 probes, swift/original=1086 probes, swift/regenerated=4187 probes

POPULATION: 31078 arch-units, from 332 files
  units with a signature      31067 of 31078
  units with no signature     11 of 31078
      cpython / population interpreter   1
      java / population interpreter      2
      php / population interpreter       4
      ruby / population interpreter      4
  distinct signatures         3390 over 31067 units
  distinct operator groups    131 over 31078 units
  languages in the selector   9
  units with no ledger        646 of 31078

  language      units with sig   groups     sigs
  cpp           17840    17840       32     2191
  c             10620    10620       27     1857
  swift          1322     1322       26      296
  rust            695      695       21      493
  go              590      590       20      165
  php               4        0        1        0
  ruby              4        0        1        0
  java              2        0        2        0
  cpython           1        0        1        0

OPCODE INDEX: 162 distinct arch opcodes over 31078 units
  opcode          units     groups
  ret             30432      29653
  mov             14437      14192
  cmp              7020       6886
  xor              6775       6681
  setne            6691       6633
  or               6107       6011
  test             5799       5743
  and              5687       5546
  call             4119       4089
  movslq           3728       3704
  push             3356       3326
  pop              3344       3316
  total (lang, operator-group, signature) groups over all opcodes: 151279

wrote pane23_ground_truth.json
```

## 6.2 The comparison

| figure | python, off the files | the browser, its own console |
|---|---:|---:|
| index rows | 31,078 | 31,078 |
| rows with a type signature | 31,067 | 31,067 |
| rows with none | 11 | 11 |
| distinct type signatures | 3,390 | 3,390 |
| operator groups | 131 | 131 |
| languages | 9 | 9 |
| arch opcodes | 162 | 162 |
| probes read | 133,993 | 133,993 |
| manifest files read | 10 | 10 |

Every figure agrees. Population for all of them: every arch-unit on disk
as of 2026-09-03 — 31,078 units read from 332 corpus files, joined to 10
probe manifests.

## 6.3 Two defects the running found

**Defect 1 — the live page's language menu was empty.** The shell fills
`#f-lang` once, in `mount`, from `state.index`. On the live page the
index is EMPTY at that moment (it arrives in the background 6.7 s
later), so the menu was filled with nothing and `refreshMenus` never
refills it — it only refills the operator and signature menus. Anyone
opening the live page had a language menu with one entry in it.
`dashboard_pane23.js` refills it on every repaint, from the index as it
stands. It now carries 10 options.

**Defect 2 — this module's own first cut broke the arch opcode index.**
The hardening in section 7.2 originally replaced the source's opcode map
with a fresh object. `DashboardJoin.mount` had already read
`source.opcodeIndex()` and kept THAT object, so every opcode absorbed
afterwards landed in a map nothing drew. The click-through said so, in
one line:

```
[walk] arch opcode entries in the index: 0
```

The fix strips the prototype in place (`Object.setPrototypeOf(map,
null)`) and keeps the identity the panes hold. The same line now reads
`162`. This is written down because it is the whole argument for running
the click-through rather than asserting it: the module looked right and
was wrong, and one counted number said so.

---

# 7. What was written, and what it touches

## 7.1 One new module, three shared files touched by one line each

Task 76 and task 69 were editing the dashboard at the same time, so all
of this work is in a new module and the shared files gain the minimum.

**`dashboard.html`** — one script line. Every script tag it now holds:

```
$ grep -n "<script" dashboard.html
27:<script src="dashboard_join.js"></script>
28:<script src="dashboard_loader.js"></script>
29:<script src="dashboard_pane1.js"></script>     <- task 69
30:<script src="dashboard_pane6.js"></script>     <- task 76
31:<script src="dashboard_pane23.js"></script>    <- this work
32:<script>
```

**`dashboard_join.js`** — two properties on the object `mount` returns,
and the comment saying why:

```
$ grep -n "task 70" -A6 dashboard_join.js
1112:      /* task 70: the two selector functions a module beside this file
1113-       * needs and cannot reach, because both are closed over `state`.
1114-       * `filtered` is the list the seeded sampler indexes into and
1115-       * `selectUnit` is how a unit anywhere in the population is opened
1116-       * without depending on it being one of the 600 rows drawn. */
1117-      filtered: filtered,
1118-      selectUnit: selectUnit
```

Nothing else in that file changed. It was unavoidable: a seeded sampler
that can only reach the 600 rows currently drawn is not a sampler over
31,078 units.

**`viewer_build.py`** — the module is embedded VERBATIM, at the one seam
where it must be parsed before the snapshot's own script (it wraps
`DashboardJoin.mount`, and the snapshot calls `mount` at parse time).
The `/*JOIN*/` substitution is untouched, so log_176 section 2.2's
byte-for-byte join proof still holds. The builder REFUSES to write a
page if the seam is not found. Its build line:

```
$ /tmp/reconnect_venv/bin/python3 viewer_build.py
operator inventory: 91 tokens read from probe_manifest_*.json
PASS dashboard_snapshot_data.json -- no operator token in any key, grouping, pairing or row structure
wrote …/dashboard_snapshot.html  (19.7 MB, 2456 unit bodies carried, 31078 units counted, 1019 files read)
the join embedded above is dashboard_join.js, verbatim (43902 bytes)
panes 2 and 3 embedded verbatim from dashboard_pane23.js (32169 bytes), before the snapshot script
pane 1's modes embedded verbatim from dashboard_pane1.js (15373 bytes), before the snapshot script
pane 6 embedded verbatim from dashboard_pane6.js (15891 bytes) with chronology.json (56904 bytes)
```

and the embedded copy is the file:

```
$ (extract the pane23 block out of dashboard_snapshot.html and compare)
embedded chars: 32169   file chars: 32169
IDENTICAL
```

## 7.2 How the module attaches without changing anything

Three wraps, each calling the original first:

| wrapped | why |
|---|---|
| `DashboardJoin.mount` | to attach after the panes exist |
| `LiveSource.prototype.absorb` | to keep each unit's probe number and OUT row width while the shard is open |
| `LiveSource.prototype.indexAll` | to know when the index is complete, without watching a note string |

The hardening the wraps also do, and why:

- The source's opcode map and shard map have their prototypes stripped.
  A plain `{}` answers truthily for the key `constructor`, so an arch
  opcode of that spelling would make `if (!map[m]) { map[m] = [] }` skip
  the assignment and then throw on push. Nothing in the corpus spells
  one today; the map is made this way so that nothing can.
- Every map this module builds is prototype-free for the same reason.

## 7.3 The snapshot gets it too

The snapshot carries a 2,456-unit sample rather than the population, and
has no folder to read manifests from, so it fills its signatures by
running the ONE join over the bodies it already carries. Its own scope
line says exactly that, and says what it does NOT have — screenshot
`DevComms/screens/log_179/snapshot_selector.png`:

> selector: 2,456 rows in the index · 9 languages · 131 operator groups
> · 829 type signatures over 2,445 of 2,456 units · 11 units have no
> signature (…) · 0 probes read from 0 manifest files

The 11 with no signature are the same 11 interpreter handlers. A pane
never claims a population it has not got.

## 7.4 The four modules coexist, checked

Tasks 69, 70 and 76 each added a module to the same page in the same
round, and `dashboard_pane6.js` also wraps `DashboardJoin.mount`, so the
wraps chain. The built snapshot carries all of them and was opened in
Chrome:

```
> ({panes: …, sigOptions: …, opcodeEntries: …, scopeSelector: …})
{ "panes": 6,
  "tabs": ["units","opcodes","coverage","stats","spec","chrono"],
  "langOptions": 10,
  "sigOptions": 830,
  "opcodeEntries": 122,
  "scopeSelector": true,
  "scopeOpcode": true }
> read_console_messages(onlyErrors: true)
No console logs.
```

- **LITERAL:** six panes including task 76's `chrono`, both of this
  work's scope lines present, the signature menu carrying 830 options,
  and no console error of any kind.
- **GLOSS:** 830 is 829 signatures plus "every signature", and 122 arch
  opcodes is the snapshot's own smaller population, not the live page's
  162 — the snapshot carries a 2,456-unit sample.

---

# 8. Complete file inventory

New:

| bytes | file | what |
|---|---|---|
| 32,184 | `Research/op_pipeline/dashboard_pane23.js` | the module: the signature index over the full population, the rebuilt arch opcode index, the scope lines, the seeded sampler |
| 10,361 | `Research/op_pipeline/pane23_ground_truth.py` | the off-page arithmetic; emits the json the guard walks |
| 7,176,776 | `Research/op_pipeline/pane23_ground_truth.json` | what it emits; PASSes `check_no_spelling_keys.py` |
| 3,084 | `Research/op_pipeline/pane23_manifest_regex_check.py` | TEST RIG ONLY — the regex proved identical to `json.load` over 133,993 probes |
| 12,310 | `Research/op_pipeline/pane23_clickthrough.html` | TEST RIG ONLY — clicks every pane, menu entry and arch opcode entry |
| 4,412 | `Research/op_pipeline/pane23_clickthrough.py` | TEST RIG ONLY — drives it headless and prints the transcript |
| 2,868 | `Research/op_pipeline/pane23_shot.html` | TEST RIG ONLY — opens one view for a screenshot |
| 2,714 | `Research/op_pipeline/pane23_shot.py` | TEST RIG ONLY — takes the screenshots below |
| — | `DevComms/screens/log_179/*.png` | 8 screenshots, named in sections 4, 5 and 7 |
| — | `DevComms/log_179_task70_panes23_full_population.md` | this file |

Screenshots by path, all under `DevComms/screens/log_179/`:

| file | what it shows |
|---|---|
| `selector_full_population.png` | the selector's scope line and its three filled menus over 31,078 rows |
| `selector_language_cpp.png` | cpp narrowed to one signature — three units, three different operator spellings |
| `opcode_index_ret.png` | the arch opcode in the most units: 30,432 units, 29,653 groups, the ceiling stated |
| `opcode_index_movss.png` | a narrower arch opcode, same pane |
| `glyph_selector.png` | the selector with every operator label replaced by ◆ |
| `glyph_opcode_index.png` | the arch opcode index with every label replaced by ◆, counts unchanged |
| `seeded_sample.png` | `go/regen_348`, opened by the seed in the address alone |
| `snapshot_selector.png` | the snapshot saying its own smaller population honestly |

Changed, one line or one block each (the three the brief allowed):

| file | what changed |
|---|---|
| `Research/op_pipeline/dashboard.html` | one `<script src="dashboard_pane23.js">` line, appended |
| `Research/op_pipeline/dashboard_join.js` | two properties (`filtered`, `selectUnit`) added to the object `mount` returns, with the comment saying why |
| `Research/op_pipeline/viewer_build.py` | `PANE23` constant, the verbatim embed at the seam, the refusal if the seam is absent, and one build-line print — all additive |

Unmodified, and checked to be:

- `Research/op_pipeline/check_no_spelling_keys.py` — `git status
  --porcelain` prints nothing for it.
- `Research/op_pipeline/check_dashboard_js_no_spelling.py` — the same.
- `Research/op_pipeline/dashboard_loader.js` — not edited; it is wrapped
  from outside.

Plan tree:

- `Planning/…/node_0_3_5_10_dashboard/CORE_0_3_5_10_dashboard.md` — the
  "panes 2 and 3 over the full population" row moved from **partly
  done** to **done**, with its numbers; a new section records the three
  measured constraints of sections 3, 4.3 and 5.5.
- `Planning/…/node_0_3_5_10_dashboard/PROGRESS.md` — six entries, at the
  moment of progress, with the evidence links.

---

# 9. Two lists

**Decided, recorded for audit.**

- The arch opcode index in EMITTED JSON is a list of rows keyed by an
  opaque `arch#NNN` id, with the mnemonic carried as `mnem`. The reason
  is section 5.5: four x86 mnemonics are homographs of C++ operator
  tokens and a dict key cannot carry the difference. In the page's own
  memory the map stays keyed by mnemonic, because an arch opcode
  mnemonic read out of objdump is machine-form evidence, which the ban's
  own sentence names as a permitted candidate source.
- The arch opcode pane draws at most 200 groups and at most 12 unit ids
  per group. Both ceilings are printed on screen beside the number they
  cut down from, and two menus are offered to narrow past them.
- The address carries `scope=` beside `seed=`, because a seed alone does
  not reproduce a sample — it indexes into a filtered list, and the
  filter has to travel with it.
- The signature is filled from the manifests by one regular expression
  rather than a json parse, proved equal to `json.load` on all 133,993
  probes rather than assumed.
- `dashboard_join.js` gained two properties. The alternative was to copy
  `selectUnit` and `filtered` into this module, which would have been a
  second implementation of the selector.

**Awaiting the owner.**

- Nothing.
