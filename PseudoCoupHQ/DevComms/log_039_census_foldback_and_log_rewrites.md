# log 039 — the census fold-back, and seven logs rewritten for readability

Date: 2026-08-19. Nodes:
`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_dominant_intentions/CORE_0_3_1_dominant_intentions.md`
and
`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`.
Artifacts: `~/Programming/PseudoCoupHQ/Research/dominant_intentions/`
and `~/Programming/PseudoCoupHQ/DevComms/`.

This log records two housekeeping jobs. Neither ran a probe and neither
measured anything new. Both move findings that already existed into
places where they can be found and read.

Every claim carries its level. **Measured** means a number a run
printed. **Derived** means a number worked out from measured numbers.
**Estimate** means a guess with a reason. **Unverified** means nobody
has checked it.

---

## words used in this log

Every short word this log leans on is defined here, with an example
taken from this log's own content.

```
census page
    one hand-written reference page describing
    what one data structure does across the
    eleven target languages.  there are five
    files covering six objects.
    example tied to context:
        `census_integer.md` is the census page
        for the integer.

fold-back
    adding what a later run PROVED to a page
    written before that run, without
    rewriting the page's own claims.
    example tied to context:
        the shift mixed-holder table is folded
        back into the integer page; the page's
        own F-i6 rows are left untouched.

the layer-3 campaign
    logs 024 through 037: the runs that took
    the census pages as a work order and
    measured them by executing generated
    programs.
    example tied to context:
        log 032 is the campaign's execution
        pass, and four of its eight surprises
        are folded back below.

readable register
    the way of writing set out in
    `~/Programming/DevComms/LLM_communication_protocol.md`
    — every term defined at first use, no
    sentence depending on an unread file,
    contrasts built into the structure.
    example tied to context:
        logs 034 and 035 were rewritten into
        it first, and are the models the seven
        rewrites below copied.

the rewrite note
    the bolded line placed at the top of a
    rewritten log stating that the prose was
    rebuilt and the content was not.
    example tied to context:
        all seven rewritten logs carry it, and
        it was checked by counting the line in
        each file.

frozen heading
    a section heading that other files point
    at by number, so it cannot move or change
    text.
    example tied to context:
        `### 5.1 integer overflow — the clean
        one` in log 031 is pointed at from the
        integer census page.

provenance
    the log and section a folded-back claim
    came from, written beside the claim.
    example tied to context:
        `(measured, log_032 §5 surprise four)`
        is the provenance on the pi + pi
        finding.
```

---

## what came before this log, restated

Each fact this log leans on is stated in full here, so no sentence
below depends on opening another file.

- **The census pages predate the campaign that tested them.** The five
  files in `~/Programming/PseudoCoupHQ/Research/dominant_intentions/`
  were hand-drafted on 2026-08-13. Each one says at the top that every
  fact on it is UNVERIFIED, and that the page is the harness's work
  order. They cover six objects in five files: boolean and float share
  `census_boolean_float.md`, and integer, string, list and dict have
  one each.
- **The campaign then ran and answered them.** Logs 024 through 037
  built generated programs, ran them across twelve languages, and
  recorded both what each language ACCEPTS and what it RETURNS. The
  pages were never updated with the results.
- **Logs 034 and 035 were already rewritten into the readable
  register.** Both carry a glossary block, a restatement block for
  prior-log facts, and a note saying the content is identical and only
  the prose was rebuilt. They were the models for this pass.
- **Section numbers in these logs are load-bearing.** Other logs, and
  the planning files
  `CHECK_0_3_2_kind_fuzz_clustering.md` and `PROGRESS.md` under
  `~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/`,
  point at these logs by section and by numbered item — "log 027
  finding 11", "log 030 §4.4", "log 031 §5.1", "log 033 decision 40".
  A rewrite that renumbered a section would break those pointers
  silently.

---

## §1 walkthrough, in plain words

Two jobs, both reading work that was already done.

- **Job one was the census fold-back.** Each of the five census pages
  got one new section at its end, dated today, carrying what the
  campaign proved that the page does not say. Nothing above the new
  section was edited. Every claim in the new sections names the log and
  section it came from, and says whether it is measured or derived.
- **Job two was the readable-register rewrite of seven logs**, 027
  through 033. Each was rebuilt in the same shape as logs 034 and 035:
  a glossary of the log's own words first, then a restatement of every
  prior-log fact the log leans on, then the body. The facts, the
  numbers and the section numbers are unchanged.
- **The check passes and nothing broke.** `bash
  ~/Programming/PseudoCoupHQ/hq.sh check` reports 0 errors both before
  and after this session's edits. Every heading in all seven logs
  survives, verified by comparing the heading list taken before the
  rewrites against the list taken after — zero headings missing.

The two jobs share one purpose. A finding that lives only in a log is
findable only by someone who already knows which log to open. The
census pages are the reference surface for the data structures, so
that is where the campaign's answers belong; and a log nobody can read
without three other logs open is a log that will not be re-read.

---

## §2 job one — what was folded into which census page

Every page received one new section titled `## layer-3 findings,
folded back 2026-08-19`, and each of those sections opens with its own
small glossary of the words it uses. Below is what each page gained.

### `census_integer.md`

- **The wrap camp agrees BIT FOR BIT**, not merely in behaviour: go
  `int64`, c++ `int64_t`, java `long`, c-sharp `long` and kotlin `Long`
  all return `INT:64:8000000000000029` on `i64max + 42`, and rust's
  panic is a property of the debug build, with `-O` wrapping like the
  rest. *(from log 032 §5 surprise two)*
- **Php's fall to float, with the tokens**: `whole:9223372036854775849`
  in python and ruby against `fractional:9.2233720368548e+18` in php,
  and the cell-level agreement of 1.000 python-with-ruby against 0.306
  for php. *(from log 031 §5.1)*
- **Python contradicts itself by holder**: `u64max + 42` answers
  `whole:18446744073709551657` from its ordinary integer and
  `whole:41` from its `ctypes.c_int64` holder. *(from log 031 §5.1)*
- **Wrapping alike does not make languages alike**: `go.+` sits nearest
  the panicking `rust.+` at 0.907 while `go.+` against `java.+` is
  0.094 with agreement exactly 1.000, because the domains barely meet.
  *(from log 033 §4.1 and §4.2)*
- **C++ division by zero is a DEATH**, `SIGFPE` and uncatchable, and
  dart's `/` answers positive infinity because it is not integer
  division at all. *(from log 032 §5 surprise three)*
- **The shift mixed-holder exemption**, with log 030's nine-language
  table reproduced: total in go and rust only, barely measurable in
  java, inverted in typescript, two sharp against four blunt — and
  closed by kotlin being ruled OUT on two measured tests rather than by
  a language being let in. *(from log 030 §4.4, log 034 §1, log 035
  §6.4)*
- **`42 << 42` gives seven acceptances and five answers**, which adds a
  camp the page had no row for: whether the shift COUNT is masked, a
  separate question from what width the shift operates on. *(from log
  032 §5 surprise one)*

### `census_boolean_float.md`

- **The full twelve-language truthiness table**, with its codes, turning
  the page's border fact about which values `if` accepts into a
  measurement. It adds swift to the bool-only camp, states that the
  refuse/coerce line is NOT the static-against-open line, separates
  c++'s per-form coercion from typescript's total coercion, and carries
  the caveat that a **T** for a statically checked language means the
  holder was accepted rather than that every value goes to the then
  arm. *(from log 037 §4)*
- **`pi + pi` is bit-identical across seven languages**,
  `FLOAT:64:401921fb54442d18`, which promotes the page's "same inputs,
  same bits" candidate to measured — and the method half, that
  recording bits rather than printed decimals is what makes the
  statement possible at all. *(from log 032 §5 surprise four)*
- **The −0.0 sign-read lesson**: php prints negative zero as `-0`, and
  parsing that back as a number first would have manufactured a
  fracture that belonged to the reader rather than to php. *(from log
  031 §5.6, decision 23)*
- **The known fractures that did not fracture**, as a table: 2^53+1,
  −0.0, NaN arithmetic, NaN equality and inf-against-NaN all agree
  across python, ruby and php. *(from log 031 §5.6)*
- **NaN read through the operators**, including that `if nan:` takes
  the true branch and `if -0.0:` takes the false one. *(from log 024 §4
  item 8)*

### `census_string.md`

- **The e-acute concatenation is a HOLDER story**: python's and ruby's
  string holders return identical bytes `text:c3a968656c6c6f` and score
  1.000 on the `text|text` cell, while the disagreeing tokens are the
  codepoint-array holders — ruby's carrying codepoint 233 and php's
  carrying the utf-8 bytes 195 and 169. So F-s1's camps are a property
  of the holder the program chose, not only of the language. *(from log
  031 §5.6)*
- **Php's row is not evidence about php's text**, because php drops a
  byte there — its `+` on an array is the key union, not a
  concatenation. *(from log 031 §5.4 and §5.6)*
- **E-acute equality did not fracture** across the three. *(from log
  031 §5.6)*
- **The "concatenation is universal" candidate needs its spelling
  caveat**: php has no `+` on strings and spells it `.`. *(from log 031
  §5.4)*
- **Indexing splits by holder inside one language**: `"hello"[0]` is
  `str:'h'` and the same text as `bytes` is `int:104`. *(from log 024
  §4 item 4)*
- **Iteration reads the same holder choice a third time**, after length
  and indexing. *(from log 024 §4 item 9)*
- **Text in the if-condition slot across twelve languages**, where
  c++'s PART-refused row is the only place a static language splits
  within a form. *(from log 037 §4)*

### `census_list.md`

- **Php's `+` is a union by KEY, measured**: python and ruby answer
  `sequence:[1,2,3,'a','b']` and php answers `sequence:[1,2,3]`, the
  left operand, because every positional key collides. This promotes
  the page's "impostor" reading from an analogy to a measurement.
  *(from log 031 §5.4)*
- **Ruby's `Set` holder answers as a keyed grouping** where its list
  holder answers as a sequence. *(from log 031 §5.4)*
- **The two refusal KINDS differ and the difference means something**:
  a sequence given a name index raises `TypeError`, a keyed grouping
  given a position index raises `KeyError`, because a whole number is a
  good key that is simply absent. *(from log 024 §4 item 4)*
- **Index kinds that are not whole numbers**, including that
  `[1,2,3][9223372036854775807]` raises `IndexError` — a RANGE
  complaint, not a WIDTH complaint, because python's whole number has
  no width. *(from log 024 §4 item 5)*
- **Python's containers do not agree across holders though its numbers
  do**: `list == tuple` false, `list == deque` false, against `int 42
  == Decimal 42 == Fraction 42` all true. A third axis the page's F-l7
  does not have. *(from log 024 §4 item 7)*
- **Repetition is a fifth operation** the ordered container owns, spelled
  with an arithmetic token: `[1,2,3] * 42` is a 126-element list. *(from
  log 024 §4 item 10)*
- **What a `for` actually collects**, including the frozenset caveat
  that it iterates and has no index at all. *(from log 024 §4 item 9)*
- **Sequences in the if-condition slot across twelve languages.** *(from
  log 037 §4)*

### `census_dict.md`

- **The php impostor resolution, now measured** rather than argued: the
  operation php's array carries under `+` is the DICT's keyed union, so
  the object is a dict. The two readings are set against each other on
  the page. *(from log 031 §5.4)*
- **Keyed merge is an operation the dominant needs and python lacks**:
  python's `dict + dict` raises `TypeError` while php's `+` is the key
  union. Merge is not on the page's universals list and it is not
  universal. *(from log 024 §4 item 1, log 031 §5.4)*
- **F-d3's refusal kind is itself a finding**: `{'a':1}[0]` raises
  `KeyError` and not `TypeError`, which is the run showing why python
  belongs in F-d1's "anything hashable" camp. *(from log 024 §4 item
  4)*
- **Holders of one form do not all compare equal**: `dict ==
  OrderedDict` is true and `dict == SimpleNamespace` is false. *(from
  log 024 §4 item 7)*
- **A `for` over a keyed grouping visits the KEYS**, which is the prior
  question F-d2 assumes and the page never states. *(from log 024 §4
  item 9)*
- **Keyed values in the if-condition slot**, where c++ flatly refuses a
  `std::map` while accepting whole and fractional — the sharpest
  evidence that coercion-to-bool is a per-STRUCTURE decision inside a
  language rather than a per-language camp. *(from log 037 §4)*

---

## §3 job two — the seven logs rewritten

Logs 027 through 033 were rewritten in place, each into the shape logs
034 and 035 already had.

| log | subject | glossary entries | restatement bullets |
|---|---|---|---|
| 027 | phase 3, the builds proven and the runs launched | 27 | 17 |
| 028 | phase 3 close-out, certification, the value matrix | 27 | 19 |
| 029 | frozen manifests and a preliminary clustering | 27 | 8 |
| 030 | the promoted clustering and the threshold sweep | 33 | 34 |
| 031 | the answer-grain clusters | 26 | 13 |
| 032 | execution — what the accepted operations return | 25 | 9 |
| 033 | the answer grain, all twelve languages | 37 | 16 |

Every one of the seven carries the rewrite note at its top, stating
that the content is identical and only the prose was rebuilt.

---

## §4 what the self-checks caught

The protocol's §8 list was run over each rewritten log. Reported by
CAUSE rather than by sighting, since the same few faults recur across
all seven.

- **No log had a glossary at all, and all seven used in-house words
  freely.** Status: fixed in all seven. Probe, lane, shard, holder,
  value class, cell, route A/B/C, the lift, the completeness gate and
  the grain vocabulary were used throughout without ever being defined.
  This was the single largest fault and it is what the glossary blocks
  exist to close.
- **Contrasts were carried by a clause rather than by the structure**
  (protocol §5a). Status: fixed in all seven, roughly thirty places
  in total. The two worth naming: log 032's overflow surprise, where
  five languages agreeing bit for bit and rust standing alone were one
  sentence and are now two labelled blocks; and log 033 §4.2, where the
  fact that says the wrap languages should cluster and the fact that
  decides they do not are now two named sides.
- **Whitespace-aligned pseudo-tables inside fenced blocks** (protocol
  §3). Status: fixed where found — three blocks in log 027, one in log
  031, and eight in log 033, all converted to real pipe tables with
  every token carried across. Genuine verbatim compiler output and
  measurement output stayed fenced, which is what §3 permits.
- **Lane names arriving bare.** Status: fixed in all seven. `vm_dart_01`
  and its co-lanes now read as "the dart value-matrix lane
  `vm_dart_01`" on first use in each section.
- **Sentences leaning on an unread log.** Status: fixed in all seven,
  and this is what the restatement blocks are for. Every "log 029 said"
  and "decision 10" in a body now has its content stated above it.
- **Commands written without the path that runs them** (protocol §14a).
  Status: fixed in logs 031 and 033, where the reproduce blocks were
  bare `python3` lines with the directory implied.
- **One banned socio-familial term** (protocol §1). Status: fixed. Log
  029 §5 read "next to a **sibling** operation that accepts it"; it now
  names the operation, `&&`, as a co-operation in the same menu.

### two things the pass found that it did NOT act on

Both are recorded rather than corrected, because the instruction was to
rebuild prose and change no content.

- **Small internal inconsistencies were found in five of the seven
  logs** and were left exactly as written. Examples: log 027 §1 states
  a landed total of 558,001 probes where its own three components sum
  to 548,001; log 027 §5.1 opens "Six more" above seven items; log 032
  §5's third surprise is headed "splits six ways" above a table whose
  rows do not obviously reduce to six; log 033 §6 attributes the float
  shadow loss to decision 22 where §2 makes it decision 34. Status:
  **open**, each one a candidate for a correction pass that is
  explicitly allowed to change content.
- **One genuine repair was made, in log 033, and it is the item most
  worth an eye.** The twelve-by-twelve agreement matrix's swift row
  carried fourteen cells against twelve columns, the last two being a
  duplication of the kotlin and dart cells, which stopped the row
  rendering. The duplicated pair was dropped; no value changed, and the
  symmetric entries elsewhere in the table confirm the surviving
  twelve. Status: **fixed**, and flagged here rather than buried,
  because it is the one place a rewrite touched content.

---

## §5 verification

- **`bash ~/Programming/PseudoCoupHQ/hq.sh check` reports 0 errors and
  8 warnings**, the same as before this session. *(measured)*
- **No cross-reference broke.** The full heading list of each of the
  seven logs was taken before the rewrites and again after, and
  compared. **Zero headings are missing from any of the seven**, at
  matching levels and with matching text. *(measured)*
- **The numbered items other files point at all survived**, checked by
  name: log 027's finding 11; log 029's eleven decisions, present at 1
  through 11 in its §3; log 031's decisions 18 through 30, present in
  its §2.2 table; log 032's eight numbered surprises, present in order;
  log 033's decisions 31 through 42, present in its §2 table.
  *(measured)*
- **One thing worth knowing about the item labels.** Several references
  of the form "log 030 item 4k" and "log 033 item 4u" point at labels
  that do not exist inside those logs. The labels live in
  `~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CHECK_0_3_2_kind_fuzz_clustering.md`,
  which numbers its own checklist items and attributes each to a log.
  So the citation names a CHECK item and its log, not a section of that
  log. Nothing was invented to satisfy those references, and the
  content each one points at is intact and unmoved. Level **measured**,
  by grepping the whole repository for the labels.

---

## §6 what this log did not do

- It measured nothing. No probe was generated, no lane was run, and no
  number in any file changed.
- It did not touch logs 024, 025, 026, 036 or 037. Those are still in
  their original register.
- It did not act on the internal inconsistencies listed in §4, which
  remain open.
