# log 150 — audit of round 10's completion logs (143–149)

Date: 2026-09-02. Auditor: the coordinating session, not a sub-agent.
Every number below was recomputed from the artifacts in
`PRIVATE/PseudoCoupHQ/Research/op_pipeline/` this session; the
commands and outputs are pasted. Renderings are labelled per protocol
§5.1a.

# 1. Verdict

- Round 10 delivered what the briefs asked, and the counts in the
  logs match the artifacts on disk. Details in §2.
- One finding of my own that no log reports: task 47's ledger
  artifacts (`canon37_wrapped_*.json`, `canon37_regen_store/`) pass
  the spelling guard ONLY by a file-level exemption. With that
  exemption removed they fail with 579 places in the c file alone —
  bare `produced_by: "xor"` strings. This is the exact defect log 147
  §13 confessed and repaired for task 48's files, and it was not
  carried back to task 47's. Details and the repair in §3.
- One inherited "open point" is not open: log 149 §1.2 and §2.3(7)
  report the 826-vs-827 withdrawal gap as unresolved; log 147 §13.5
  already resolved it (a 3,000 ms solver timeout moves one unit at the
  margin between runs). Details in §4.
- The round leaves five calls for the owner, listed with their instances in
  §5. Three are new this round; two are the Airlock calls carried from
  log 145.

# 2. What was checked, and the values

## 2.1 The counts on disk agree with the logs

LITERAL — recomputed this session over `canon37_wrapped_*.json`,
`canon37_interp.json`, `canon37_regen_store/*.json`, `the_pool2.json`,
`name_census3.json`:

```
orig+interp {'WRAPPED_TEXT_PROVED': 1772, 'REFUSED': 18}
regen       {'WRAPPED_TEXT_PROVED': 28664, 'REFUSED': 624}
pool2 summary: entries 5274, multi-language 423,
   compiled+interpreted 3, brief-strict 8140,
   distinct layer-3 texts 6277
E00029 members 158  rep go/op_319  l5 ['v0 + v1']
c/op_109 v0 + v1 True      go/op_319 v0 + v1 True
php/add_function v0 + v1 True   ruby/rb_fix_plus v0 + v1 True
cpython/long_add_fastpath v0 + v1 True
census3 entries 47; tally: DISPROVED 826, PROVED ship 17072,
   PROVED textorder 23414, no OUT-0 term 4142, population 30436
```

GLOSS: 1,772 + 28,664 = 30,436 proved, 18 + 624 = 642 refused —
log 146 §1.2's line. The pool's five headline figures are log 148
§1.2's. The census tally is log 147 §13.5's. The five members of the
integer-addition entry all carry the same eight-character layer-5
text and all are merge-eligible, which is the acceptance instance
both log 147 §8.2 and log 148 §2.2 print.

## 2.2 The idiv defect is real, as stated

LITERAL — `canon37_wrapped_c.json`, unit `c/op_210`, body and ledger
rows (row, produced_by, operands):

```
['mov %edi,%eax', 'cltd', 'idiv %esi', 'ret']
IN-0   arrival  []
IN-1   arrival  []
TEMP-0 mov      ['IN-0']
TEMP-1 idiv     ['IN-1']
OUT-0  mov      ['TEMP-0']
```

GLOSS: OUT-0 claims the answer came from `mov` reading IN-0 — the
dividend — because `idiv`'s row is attached to the divisor and `cltd`
made no row. Log 147 §5 reports exactly this; confirmed.

## 2.3 The version control system

LITERAL — `git status --porcelain | wc -l` and `git log --oneline -4`
in `PRIVATE/PseudoCoupHQ`:

```
0
225c6a6 auto: 1 file (PROGRESS.md)
73c6c0e Round 10 banked: task 47 wrapped 30,436 units (memory form), …
2755e42 Round 10 banked: task 47 wrapped 30,436 units (memory form), …
b1548a9 auto: 1 file (PROGRESS.md)
```

GLOSS: tree clean; the banking message was committed (twice — the
daemon picked the file up on two consecutive ticks; harmless).
`next_commit_message.txt` is now empty, as the daemon leaves it.

# 3. THE FINDING — task 47's ledgers are guarded only by exemption

## 3.1 The instance

LITERAL — the unmodified guard on task 47's c artifact as it sits on
disk:

```
PASS canon37_wrapped_c.json -- exempt: top-level meta declares role
'generator provenance', so this file is generator provenance and
never participates in matching
```

LITERAL — the same file with the one `role` line removed from `meta`
(copy at `/tmp/c37c_norole.json`, nothing else changed), same guard:

```
FAIL c37c_norole.json -- 579 spelling-keyed place(s)
     $.units.c/op_0.ledger[1].produced_by
         operator token 'xor' on a structure field -- this is a
         grouping/row key, not a per-unit label
     $.units.c/op_11.ledger[2].produced_by
         operator token 'not' on a structure field -- …
```

## 3.2 Why it matters

- The ledger is the object task 48 reads to build terms and task 49
  reads to merge. A file that feeds grouping is a grouping artifact;
  the exemption's own text says the file "never participates in
  matching", which is false of it.
- Log 146 §6.1 claimed the guard ran "WITHOUT exemption". What
  `canon37_guard.py` did was strip the role from a scratch copy and
  then add `produced_by`/`operands` to the guard's prose-field set at
  run time (log 146 §10.2 says so). That is the "invented exemption"
  log 147 §13.2 named in task 48 — the stage under check quieting the
  checker about its own field.
- Log 147 §13.3 fixed task 48's files structurally: `produced_by`
  became `{"kind": "arch_opcode", "mnem": "xor"}`, and `mnem` is a
  ratified machine-form field the guard already treats as machine
  form. Task 47's files did not get the same repair.

## 3.3 The repair (one cause, one fix)

Regenerate task 47's ledger rows with the typed producer object
(`layer4.producer_object` already exists and is the shape to reuse),
remove the `role` declaration from every canon37 artifact, and paste
the unmodified guard's transcript over all 333 files with `grep -c
exempt` = 0. No change to the wrapper, the bodies, the proofs or the
counts — only the shape of one field. Task 48/49 read `produced_by`
by string today and must read `.mnem` after; that is a two-line
change in `layer4.py`'s intake.

# 4. The 826/827 "open point" is closed

- Log 149 §1.2 and §2.3 item 7 say the two sources disagree by one
  and leave it "surfaced, not resolved".
- Log 147 §13.5 already explains it. LITERAL:

> the gate sets a 3,000-millisecond per-unit solver timeout, and a
> solver that runs out of time returns `unknown`, which this lap
> counts honestly as UNDECIDED. So the withdrawal count is
> timing-dependent at the margin, by one unit across two runs.

- The authoritative figure is the one on the artifact task 49 read:
  826 (`name_census3.json`, confirmed in §2.1). The bank author did
  not read §13 of the log he was banking. Status: closed; the bank's
  posterity line "826-827 disputed" is one line of history, not a
  defect.

# 5. The calls for the owner, with their instances

1. **The idiv implicit destination** (log 147 §5): `idiv`, `div`,
   `mul`, one-operand `imul` write registers they do not name;
   `ledger47.py` attaches their row to the last NAMED operand. 1,558
   rows; 826 units' terms withdrawn (all three spellings of the divide
   idiom: `cqto+idiv` 349, `cltd+idiv` 255, bare `idiv` 222). Fix: a
   per-opcode destination rule, plus rows for `cltd`/`cqto`. This is
   the largest single hole and is mechanical.
2. **The machine stack and the x87 stack have no block** (log 147
   §4.1): `push`/`pop` 4,298 rows and `fucomip`/`fucomi` pairs 1,072
   rows have no row to be about. Fix: two more block kinds in the
   ledger (STACK, X87). Your ruling on the form said every lineage
   gets a block; these are two lineages the form does not yet have.
3. **Branch labels in the wrapped text** (log 148 §4.2.2): 4,499
   members carry `<main.op_174+0x18>`-style targets holding the
   unit's own name; positional labels (`L0..`, already ruled) would
   take distinct layer-3 texts from 6,277 to 2,999. Fix to task 47's
   renderer.
4. **The third merge ground** (log 148 §1.4): the pool merges on
   layer-3 text identity as well as layer-5 and proved edges; without
   it, 8,140 entries instead of 5,274. My read: keep it — identical
   machine code twice is a proof of equivalence by construction.
   Needs your yes or no.
5. **Airlock** (log 145 §1–3 and log 143 §7.4): the ten conf-key
   names; several lanes per instance; where an instance's run
   records live; and whether `down` should refuse while a lane runs
   (a co-agent cut a running lane short this round; it re-ran clean).
   Design calls, yours.

Items 1–3 and the §3 repair are the natural round 11; item 4 needs an
answer before the pool is rebuilt again; item 5 does not block
anything.
