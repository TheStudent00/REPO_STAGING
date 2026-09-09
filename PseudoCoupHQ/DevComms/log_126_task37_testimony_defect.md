# log 126 — TASK 37, the verbatim-testimony defect

Date: 2026-09-01. Round 7, task 37 of log_123. Nothing existing was
modified; every file named below is new. No probe was re-captured —
that decision is reserved for the owner and §5 is the proposal.

---

## 0. What was asked, and what is here

(a) fix the capture path in a new module so future captures are
verbatim, having first found the reason the substitution existed and
solved THAT; (b) audit the damage, with counts and carriers; (c) put
the remediation proposal in front of the owner without acting on it.

All three are here. §5 is the part that needs the owner.

---

## 1. The defect, stated in mechanism

**The store.** `Research/op_pipeline/lane_gen.py` writes a shell lane
that carries a Python program (its `DRIVER` string) into the Airlock
container. Inside the container that program compiles each probe and
writes ONE LINE PER PROBE into a text file whose fields are separated
by `|`:

```
op_178|REFUSED|error[E0277]: no implementation for `i32 / f64`
```

`Research/op_pipeline/fold.py` reads that file back with
`ln.split("|")` (its `read_lanes`) and folds it into
`op_units_<lang>.json`.

**The alteration.** A `|` inside the compiler's own words would split
into extra fields and corrupt the parse. The author's answer was to
substitute the character before storing it:

- `lane_gen.py:192`, in `clean()` — `text.replace("|", "/")` and
  `text.replace(";", ",")`
- `lane_gen.py:365, 368, 371, 373`, in `firstline()` —
  `ln.replace("|", "/")[:200]`

So wherever a compiler quoted `|`, the store holds a `/` the compiler
never emitted. Evidence class for this paragraph: **read of the code
on disk**, quoted above.

**The named instance.** rust probe 178 asked about `a | b`; the store
holds ``error[E0277]: no implementation for `i32 / f64` ``.

```
$ /tmp/reconnect_venv/bin/python3 -c "import json;d=json.load(open('op_units_rust.json'));print(d['probes']['178'])"
 "expression": "a | b",
 "refused": "error[E0277]: no implementation for `i32 / f64`"
```

**Where it was first recorded.** The brief cites "log 121". **There is
no log 121 in this repository.** Verified:

```
$ ls PseudoCoupHQ/DevComms/ | grep -E "log_1(1[5-9]|2[0-6])"
log_115_claude_code_task_briefs_round6.md
log_116_task29_type_inventory.md
log_117_task31_result_destination_seat.md
log_118_task30_designated_memory.md
log_119_task32_interp_table_union.md
log_120_task33_bank_round6.md
log_122_swift_source_obtained.md
log_123_claude_code_task_briefs_round7.md

$ find ~/Programming -name "*log_121*"
StressBot/RelevantProjects/PseudoCoup_v0/DevComms/log_121_reactivity_model.md
```

The one file with that number anywhere under `~/Programming` is in an
unrelated old repository (`PseudoCoup_v0`) and is about a reactivity
model. The numbering skips 121 in this line. **The actual source of
record is log_116 §5, finding F5**, which states the defect in the
same words and explicitly leaves it open:

> **F5 — the stored refusal text has one systematic alteration.
> OPEN, not fixed this round.** `lane_gen.py :: firstline()` applies
> `text.replace("|", "/")` to every stored diagnostic (lines 192, 365,
> 368, 371, 373). … rust probe 178 is stored as ``error[E0277]: no
> implementation for `i32 / f64` `` when the expression is `a | b`.

Log_123 also cites "log 121" for three other things (the swift stdlib
cross-witness routes, the "intelligent way" §3 direction, the
container-wall lesson). Those citations point at a file that does not
exist and are flagged here so a later session does not hunt for it.

---

## 2. (a) The fix — why the substitution existed, and the proper solve

### 2.1 The reason, found rather than assumed

The reason is a **delimiter collision**, and it is real. Two
delimiters are load-bearing in the lane record format, and BOTH have
named consumers:

| delimiter | what it separates | the consumer that depends on it |
| --- | --- | --- |
| `\|` | the record's fields | `fold.py :: read_lanes` — `parts = ln.split("\|")` |
| `;` | items inside a list field | `fold.py :: fold` — `parts[4].split(";")` for the mnemonic list |
| `;` | rows inside the DWARF field | `fold.py :: dwarf_rows` — `text.split(";")` |

Every consumer of the two delimiters, named. Dropping the replacement
without replacing the mechanism would corrupt `fold.py`'s parse — so
the substitution was not gratuitous, it was the wrong solution to a
genuine problem.

The `;` substitution reaches a narrower surface than the `|` one:
`clean()` is called from the DWARF attribute reader and nowhere else.

```
$ grep -n "clean(" lane_gen.py
190:def clean(text):
263:            nm = clean(dwname(at.get("DW_AT_name", "(unnamed)")))
264:            loc = clean(at.get("DW_AT_location", "(no location)"))
```

### 2.2 The proper solve: escape, do not substitute

Escaping is reversible; substitution is not. Codec v1, in
`verbatim_diag.py`:

```
\   -> \\      (the escape character itself, first)
|   -> \p
;   -> \s
LF  -> \n      CR -> \r
```

`decode` is the exact inverse. A lane written by the verbatim path
opens its output file with the line `#verbatim-escape v1`, so a
reader can tell an escaped capture from a legacy one — and the reader
**refuses** a legacy file rather than decoding it, because decoding a
legacy line would rewrite a backslash the compiler really emitted,
which is the same class of mistake as the defect itself.

### 2.3 lane_gen.py is not edited — the wrapper, and how it is checked

`lane_gen_verbatim.py` imports `lane_gen`, takes its `DRIVER` text,
and applies a named list of eight text edits, each asserted to apply
an exact number of times; if any edit does not apply the expected
number of times the program raises and writes no lane. After the
edits it asserts that neither `replace("|", "/")` nor
`replace(";", ",")` survives anywhere in the driver.

Why a text edit and not a function call: the driver does not run on
this machine. It is serialised into the lane shell script and executed
inside Airlock, where this directory does not exist. The fix has to
travel inside the lane text. The codec body is COPIED from
`verbatim_diag.py` at generation time (`inspect.getsource`), so the
two cannot drift.

```
$ /tmp/reconnect_venv/bin/python3 lane_gen_verbatim.py rust --check
driver edits applied:
  clean(): drop the two substitutions                  x1
  firstline(): drop the substitution, keep the truncation x4
  REFUSED field escaped                                x1
  ANCHOR BUILDFAIL field escaped                       x1
  ANCHOR NODWARF field escaped                         x1
  DWARF rows escaped per item, so `;` still separates  x1
  NOSYM field escaped                                  x1
  OK row: bytes and mnemonics escaped per item         x1
  driver bytes: 12070 -> 12431
```

List fields are escaped **per item**, not as a whole field, so `;`
still separates the items it is supposed to separate.

### 2.4 The reader half, and its refusal

`fold_verbatim.py` calls `fold.fold()` (fold.py untouched), then
decodes the escaped fields and writes
`op_units_<lang>_verbatim.json` — a NEW file beside the original. It
refuses any lane file without the marker, by name:

```
$ /tmp/reconnect_venv/bin/python3 fold_verbatim.py rust
rust   REFUSED: these lane files carry no '#verbatim-escape v1' marker, so they are legacy captures and must not be decoded: Airlock/agent/out/op_rust.txt
rc=1
```

### 2.5 Proof the fix stores what the compiler said

`test_verbatim_roundtrip.py` runs the real rustc refusal text through
BOTH drivers' own `firstline` (each driver's head is executed, because
`firstline` exists only inside the driver text, not as a module
attribute) and compares:

```
$ /tmp/reconnect_venv/bin/python3 test_verbatim_roundtrip.py
ok   codec identity                     'error[E0277]: no implementation for `i32 | f64`'
ok   codec removes delimiters           'error[E0277]: no implementation for `i32 \\p f64`'
ok   codec identity                     'a || b'
ok   codec removes delimiters           'a \\p\\p b'
ok   codec identity                     'a |= b; c'
ok   codec removes delimiters           'a \\p= b\\s c'
ok   codec identity                     'back\\slash | ; end'
ok   codec removes delimiters           'back\\\\slash \\p \\s end'
ok   codec identity                     ''
ok   codec removes delimiters           ''
ok   driver parses as Python            12431 bytes
ok   no substitution survives
ok   driver announces the marker
ok   record has the right field count   'op_178|REFUSED|error[E0277]: no implementation for `i32 \\p f64`\n'
ok   decodes to the compiler's words    'error[E0277]: no implementation for `i32 | f64`'
ok   legacy path reproduces defect      'error[E0277]: no implementation for `i32 / f64`'
ok   legacy text is not verbatim

0 failures
```

The fix is measured against a **demonstrated** defect (the legacy line
in that transcript), not against a description of one.

A real lane was generated to prove generation works end to end. It was
NOT submitted:

```
$ /tmp/reconnect_venv/bin/python3 lane_gen_verbatim.py rust
rust   op_rust_vb            858 probes    32337 bytes  .../lanes/op_rust_vb.sh
$ sh -n lanes/op_rust_vb.sh && echo "shell syntax OK"
shell syntax OK
```

Verbatim lanes are named `<base>_vb`, so a verbatim lane can never
overwrite a legacy one and `fold.py`'s shard glob (`_s` + DIGITS)
cannot pick one up by accident.

---

## 3. (b) The audit — how much testimony is altered

### 3.1 How a record is judged, and why not by the spelling

Nothing in the audit selects, groups, keys or pairs records by an
operator token. The population is EVERY stored string that holds
compiler words, in EVERY `op_units_*.json` on disk. Two machine-form
tests decide each field:

- **Test 1, on the stored text alone.** Is there a `/` in TOKEN
  POSITION? A file path always puts a word character on the RIGHT of
  its separator (`/work/op_c/u/n9/unit.c`, including the leading one).
  So a `/` followed by a word character is path-like and ignored;
  a `/` beside a space, quote, backtick, `=`, bracket or another `/`
  is in token position, which is where a substituted character lands.
- **Test 2, on the probe's OWN expression** (the manifest's record of
  what was handed to the compiler; reading it is covered by the
  generator-provenance exemption already written into
  `check_no_spelling_keys.py`). Does that expression contain a `|`
  character at all? If yes and it contains no `/` → **ALTERED**. If
  it contains no `|` → **GENUINE** (nothing could have been
  substituted). Both → **UNDECIDABLE**, counted, never guessed.

A correction made during the work, recorded because the first numbers
were wrong: the adjudication scope was first the whole probe FILE,
which carries includes and comments with their own slashes, and that
made every record UNDECIDABLE and measured nothing. The scope must be
the expression — the text the diagnostic quotes.

### 3.2 The counts, per store

Ten stores hold lane-captured diagnostics (five in `Research/op_pipeline`
for the plain run, three more there for the assignment run, and
`Research/stage_asg`'s copies). The `stage_asg` copies were found by
the carrier scan, not assumed.

| store file | records | with diagnostic | records with a token-position `/` | ALTERED fields | GENUINE fields | UNDECIDABLE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| op_pipeline/op_units_asg_c.json | 396 | 120 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_asg_cpp.json | 504 | 180 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_asg_go.json | 432 | 373 | 64 | 33 | 31 | 0 |
| op_pipeline/op_units_asg_rust.json | 396 | 335 | 32 | 26 | 6 | 0 |
| op_pipeline/op_units_asg_swift.json | 216 | 187 | 6 | 0 | 6 | 0 |
| op_pipeline/op_units_c.json | 750 | 140 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_cpp.json | 1002 | 232 | 0 | 0 | 0 | 0 |
| op_pipeline/op_units_go.json | 744 | 637 | 99 | 68 | 31 | 0 |
| op_pipeline/op_units_rust.json | 858 | 733 | 32 | 32 | 0 | 0 |
| op_pipeline/op_units_swift.json | 1086 | 919 | 14 | 9 | 5 | 0 |
| stage_asg/op_units_c.json | 1146 | 260 | 0 | 0 | 0 | 0 |
| stage_asg/op_units_cpp.json | 1506 | 412 | 0 | 0 | 0 | 0 |
| stage_asg/op_units_go.json | 1176 | 1010 | 163 | 101 | 62 | 0 |
| stage_asg/op_units_rust.json | 1254 | 1068 | 64 | 58 | 6 | 0 |
| stage_asg/op_units_swift.json | 1302 | 1106 | 20 | 9 | 11 | 0 |
| **total** | **13,412** | **7,712** | **494** | **336** | **158** | **0** |

The interpreter-track and JIT-track stores (`cpython*`, `java*`,
`javascript`, `csharp`, `dart`, `php`, `ruby` — 644 records between
them, breakdown: cpython 1+1+1+1, csharp 253, dart 82, java 2+2,
javascript 291, php 4, ruby 6) carry **no** stored diagnostic at all, so nothing in them can be
altered. That is a verified exclusion, not an assumption: their
`with diagnostic` count is 0 in the run above, and they are not
lane_gen products.

**The 336 is 168 captures counted twice.** `Research/stage_asg`'s
`go`/`rust`/`swift` stores are the union of the plain and assignment
runs, so each altered field appears in exactly two files on disk:

```
$ per store: {'op_pipeline/op_units_asg_go.json': 33, 'op_pipeline/op_units_asg_rust.json': 26,
   'op_pipeline/op_units_go.json': 68, 'op_pipeline/op_units_rust.json': 32,
   'op_pipeline/op_units_swift.json': 9, 'stage_asg/op_units_go.json': 101,
   'stage_asg/op_units_rust.json': 58, 'stage_asg/op_units_swift.json': 9}
op_pipeline set 168 stage_asg set 168 ; distinct stored strings 158
```

Breakdown of the **168 distinct altered captures** by language:
go 101 (68 plain + 33 assignment), rust 58 (32 + 26), swift 9.
101 + 58 + 9 = 168. c 0, cpp 0.

### 3.3 The reconstructions, shown so they can be judged

| store | record | stored (altered) | suspected original |
| --- | ---: | --- | --- |
| op_units_rust | 175 | ``error[E0277]: no implementation for `i32 / i64` `` | ``error[E0277]: no implementation for `i32 \| i64` `` |
| op_units_rust | 178 | ``error[E0277]: no implementation for `i32 / f64` `` | ``error[E0277]: no implementation for `i32 \| f64` `` |
| op_units_asg_go | 325 | `./main.go:6:2: invalid operation: a /= b (mismatched types int32 and int64)` | `./main.go:6:2: invalid operation: a \|= b (mismatched types int32 and int64)` |
| op_units_swift | 639 | `…unit.swift:4:14: error: binary operator '/' cannot be applied to two 'Float' operands` | `…unit.swift:4:14: error: binary operator '\|' cannot be applied to two 'Float' operands` |

And the detector's other side, GENUINE — the same message shapes where
the `/` really is the compiler's, because the expression is a division:

```
asg_go   37  ./main.go:6:2: invalid operation: a /= b (mismatched types int32 and int64)
swift   180  …unit.swift:4:14: error: binary operator '/' cannot be applied to operands of type 'Bool'
```

Identical stored text, opposite verdicts, decided by the probe's own
expression. That pair is the detector's validation.

### 3.4 Detection limits, stated honestly

1. **c and cpp are undetectable AND show no evidence of harm.** clang's
   messages here do not echo the operator token at all — they say
   "invalid operands to binary expression ('int32_t' (aka 'int') and
   'float')". With no token in the text there is nothing for the
   substitution to have hit, and equally no fingerprint to find. The
   honest statement is: **0 detected, and the message grammar gives no
   place for an alteration to hide** — not "0 proved".
2. **A bar followed by a word character is invisible.** A substituted
   `|` that happened to be preceded by a space and followed by a word
   character is indistinguishable from the start of an absolute path.
   No such case is expected in these four compilers' grammars (they
   space or quote the operator), but the limit is real.
3. **The reconstruction is a SUSPECTED original.** The raw compiler
   output is retained NOWHERE. The driver writes only the folded
   record, and the Airlock lane log holds the banner and the tally:

```
$ grep -c "" logs/20260825T055504Z__op_rust.sh.log
26
$ grep -n "implementation" logs/20260825T055504Z__op_rust.sh.log
(no output)
```

   So no unaltered copy exists to compare against on this machine.
   Re-capture is the only route to true verbatim text. This is the
   single most important input to §5.
4. **The `;` → `,` substitution.** It reaches DWARF attribute text
   only (§2.1). 20,020 DWARF fields were examined across the ten
   stores; **0** carry a comma, so no DWARF field shows the
   fingerprint. Detection there is weak in principle (a comma is
   ordinary text), but the parameter names and locations in this
   corpus are `a`, `b` and `fbreg -N` shapes, where a semicolon has no
   business appearing.
5. **Truncation at 200 characters is not alteration** and is not
   counted: it removes tail, it does not change words.

### 3.5 Which artifacts carry the altered text

Found by searching the whole `PseudoCoupHQ` tree for the 158 distinct
altered strings as fixed substrings — a carrier is a file that HAS the
words written into it, not one that merely reads a store at run time.

```
$ /tmp/reconnect_venv/bin/python3 audit_altered_consumers.py
ALTERED findings: 336 ; distinct stored strings: 158
carrier                        28784  DevComms/log_116_task29_type_inventory.md
origin store                  302999  Research/op_pipeline/op_units_asg_go.json
origin store                  270410  Research/op_pipeline/op_units_asg_rust.json
origin store                  503243  Research/op_pipeline/op_units_go.json
origin store                  518918  Research/op_pipeline/op_units_rust.json
origin store                  708263  Research/op_pipeline/op_units_swift.json
origin store                  818226  Research/stage_asg/op_units_go.json
origin store                  800551  Research/stage_asg/op_units_rust.json
origin store                  849577  Research/stage_asg/op_units_swift.json
the fix's own test, quotes the defect on purpose      3786  Research/op_pipeline/test_verbatim_roundtrip.py
this audit's own output       197714  Research/op_pipeline/audit_altered_testimony.json
this audit's own output         4587  Research/op_pipeline/audit_altered_testimony.md
```

**The full carrier list is: eight origin stores, and exactly one other
document — `DevComms/log_116_task29_type_inventory.md`**, which quotes
rust 178 in its finding F5. That quotation is the defect being
REPORTED, not consumed, so it needs no repair; if anything it is the
one place the altered text belongs.

Notably absent, checked rather than assumed:
`type_inventory_validation.json` and `type_inventory.json` do NOT
carry any altered string (`grep -c "i32 / " …validation.json` → 0).
The type-inventory work read the refusal records but stored its own
derived verdicts, not the compiler's words. **No derived artifact's
conclusions rest on an altered character.**

---

## 4. Zero regressions

- Nothing existing was modified. `lane_gen.py` and `fold.py` are
  untouched, verified against the version-control system rather than
  against the file's current look:

```
$ git status --porcelain Research/op_pipeline/lane_gen.py Research/op_pipeline/fold.py
(no output — untouched)
$ git log -1 --format="%h %ad %s" --date=short -- lane_gen.py
8dda5af 2026-08-25 update
$ git log -1 --format="%h %ad %s" --date=short -- fold.py
8dda5af 2026-08-25 update
```

  Both last changed 2026-08-25, six days before this task.
- No existing store was rewritten. `fold_verbatim.py` writes to a NEW
  name (`op_units_<lang>_verbatim.json`), never over `op_units_<lang>.json`.
- No probe was re-captured; no lane was submitted to Airlock.
- The spelling guard, on both audit artifacts:

```
$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py audit_altered_testimony.json audit_altered_consumers.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS audit_altered_testimony.json -- no operator token in any key, grouping, pairing or row structure
PASS audit_altered_consumers.json -- no operator token in any key, grouping, pairing or row structure
rc=0
```

- Files changed in the working tree that are NOT mine, named so they
  are not mistaken for this task's: `Research/op_pipeline/interp_table2.json`,
  `Research/op_pipeline/build_interp_table2.py`,
  `Research/compiler_graph/graph_cpp2.json`, `graph_cpp3.json` —
  those belong to the interpreter-table task running in parallel.

---

## 5. (c) FOR DEE — the remediation proposal, no action taken

The damage is **168 distinct altered captures**, in three languages
(go 101, rust 58, swift 9), living in 8 store files, consumed by 0
derived artifacts.

### Route A — re-capture the affected lanes with the verbatim path

Six lanes carry altered captures: `op_go`, `op_rust`, `op_swift`,
`op_asg_go`, `op_asg_rust`, `op_asg_swift`. Their measured runtimes
from the original runs (Airlock lane logs, `# exit 0 in Xs`):

| lane | probes | measured runtime |
| --- | ---: | ---: |
| op_go | 744 | 48.5s |
| op_rust | 858 | 24.1s |
| op_swift | 1086 | 159.8s |
| op_asg_go | 432 | 23.0s |
| op_asg_rust | 396 | 8.9s |
| op_asg_swift | 216 | 31.1s |
| **six lanes** | **3,732** | **295.4s** |

48.5 + 24.1 + 159.8 + 23.0 + 8.9 + 31.1 = 295.4 seconds — **under five
minutes of sandbox time**, serial, all six. Adding `op_c` (42.4s),
`op_cpp` (74.1s), `op_asg_c` (12.0s) and `op_asg_cpp` (27.4s) to
re-capture all ten for uniformity costs 451.3s — **under eight
minutes**.

  - Gets: true verbatim testimony, not a reconstruction.
  - Costs: the eight stores are rewritten, so every downstream product
    of the compiled five would want its provenance line updated to the
    new capture date; the toolchain in the container must be the same
    pins, or the diagnostics may differ for reasons unrelated to this
    defect (that is a re-capture risk, and it is the only one that is
    not cheap to dismiss).

### Route B — annotate in place

Mark each of the 168 records with an `altered_testimony` annotation
carrying the substitution, the suspected original, and the fact that
the true original is not retained anywhere.

  - Gets: zero sandbox time, zero re-capture risk, every record
    honestly labelled.
  - Costs: the store still does not hold what the compiler said. It
    holds a **reconstruction**, and §3.4 limit 3 is decisive here —
    there is no retained copy to check the reconstruction against.
    Under the evidence doctrine that is testimony-shaped, not
    testimony.

### What the numbers say

Re-capture costs about five minutes and yields real testimony; annotate
costs nothing and yields a labelled guess. The cost asymmetry is
large enough that the question is not really cost — it is whether
re-running the compilers is acceptable given the toolchain-pin risk,
and that is the owner's call, not mine. **Nothing was re-captured.**

A third, smaller thing that needs no ruling and was also not done: the
verbatim path is built and proved but is not yet the default. Making
it the default means either editing `lane_gen.py` (which this task was
told not to do) or routing lane generation through
`lane_gen_verbatim.py`. That routing decision belongs with the
re-capture ruling, so it waits here with it.

---

## 6. File inventory — every file created by this task

New, in `PseudoCoupHQ/Research/op_pipeline/`:

| file | what it is |
| --- | --- |
| `verbatim_diag.py` | the codec of record (escape/decode) plus `firstline_verbatim` and `clean_verbatim`; carries the defect's full statement and a self-test |
| `lane_gen_verbatim.py` | the wrapper; produces lanes whose driver escapes instead of substituting; eight asserted edits, refuses to write on any mismatch |
| `fold_verbatim.py` | the reader half; folds via `fold.py`, decodes, writes `op_units_<lang>_verbatim.json`; refuses unmarked legacy lane files |
| `test_verbatim_roundtrip.py` | the proof: codec identity, driver parses, verbatim record decodes to the compiler's words, and the legacy path reproducing the defect |
| `audit_altered_testimony.py` | the audit; writes the two files below |
| `audit_altered_testimony.json` | per-record findings (336 fields judged, with stored text and suspected original) and the counts |
| `audit_altered_testimony.md` | the same counts as a reading table |
| `audit_altered_consumers.py` | the carrier scan over the whole PseudoCoupHQ tree |
| `audit_altered_consumers.json` | the carrier list |
| `lanes/op_rust_vb.sh` | one generated verbatim lane, 858 probes, 32,337 bytes — generated as proof, NOT submitted |

New, in `PseudoCoupHQ/DevComms/`:

| file | what it is |
| --- | --- |
| `log_126_task37_testimony_defect.md` | this report |

Edited (append-only, one dated entry):
`Planning/node_0_3_research/node_0_3_5_compiler_graph/PROGRESS.md`.

Nothing else on disk was written by this task.

---

## 7. The two lists

**Decided, recorded for audit (mechanical, mine to decide):**

- escape rather than substitute; codec v1 with `\p` / `\s`; the
  `#verbatim-escape v1` marker; the reader refusing unmarked files.
- the wrapper edits the driver TEXT (the driver cannot be imported —
  it runs in another machine), with every edit count asserted.
- verbatim lanes are named `<base>_vb`; verbatim folds are written to
  `op_units_<lang>_verbatim.json`. No existing name is reused.
- the audit adjudicates on the probe's EXPRESSION, not the whole probe
  file; the token-position test ignores a `/` followed by a word
  character.

**Awaiting the owner (kept minimal):**

1. **Re-capture, or annotate in place?** 168 altered captures; six
   lanes; 295.4 seconds measured. §5 has both routes with their
   costs. Nothing done either way.
2. If re-capture: should the four c/cpp lanes be re-run too (adds
   155.9s, no known damage) so all ten stores share one capture date?
3. Should lane generation route through `lane_gen_verbatim.py` by
   default, or should `lane_gen.py` itself be edited (this task was
   told not to)?

---

## CORRECTION (2026-09-02, appended by task 41 — record hygiene, log_132)

§3.2's second statement ("The 336 is 168 captures counted twice" and
the breakdown "168 distinct altered captures... go 101, rust 58,
swift 9") and §5's opening line ("The damage is 168 distinct altered
captures, in three languages (go 101, rust 58, swift 9)") both carry
a wrong figure. The 168/336 halving assumed every altered field is
stored in EXACTLY two places (an op_pipeline copy and a stage_asg
copy) with no other duplication. That assumption is false for rust:
some of rust's 58 op_pipeline-side altered rows share IDENTICAL
stored text with each other, so the true count of distinct altered
CONTENT is lower than the per-store row count suggests.

Recomputed directly from `audit_altered_testimony.json` on this
machine, 2026-09-02:

```
$ python3 -c "
import json, collections
d = json.load(open('Research/op_pipeline/audit_altered_testimony.json'))
altered = [f for f in d['findings'] if f['verdict']=='ALTERED']
print('altered rows:', len(altered))
distinct = set(f['stored'] for f in altered)
print('distinct stored strings:', len(distinct))
lang_of = {}
for f in altered:
    stem = f['stem']
    lang = 'go' if 'go' in stem else 'rust' if 'rust' in stem else 'swift'
    lang_of[f['stored']] = lang
print(collections.Counter(lang_of.values()))
"
altered rows: 336
distinct stored strings: 158
Counter({'go': 101, 'rust': 48, 'swift': 9})
```

**The correct figure is 158 distinct altered captures: go 101, rust
48, swift 9** (101 + 48 + 9 = 158). The 168/336 halving over-counts
rust by 10 (58 vs the true 48) because it treated every op_pipeline
row as a unique capture instead of deduplicating identical stored
text. go and swift are unaffected (101 and 9 both hold under either
method, because none of their altered rows happen to share text).

This wrong 168/rust-58 figure reached `DevComms/log_128_task38_bank_round7.md`
§4.4 (posterity input) and the daemon-committed posterity message
built from it — see that log's own appended correction. Task 42
(bank round 8) is asked to carry the 158/rust-48 figure in the next
posterity message, per this task's brief (log_129, TASK 41 work
item a).

Nothing in §3.3's four shown reconstructions, §3.4's detection
limits, or §3.5's carrier list changes — the correction is scoped to
the summary count only, not to which records are ALTERED or what
they say.
