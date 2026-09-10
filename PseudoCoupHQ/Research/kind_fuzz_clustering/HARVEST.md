# HARVEST — what is running, what is done, how to collect

**STATUS 2026-08-19, after the log-035 session: NOTHING PENDING.**
Every lane this file listed has finished, been harvested through the
completeness gate, and been folded. The re-fold is built and validated.
The one thing still generated-but-unrun is the kotlin aside, which is
DEFERRED on purpose and must never be folded into the default
clustering.

The reporting logs are, newest first,
`DevComms/log_035_refold_all_twelve.md` (the harvest and the re-fold),
`DevComms/log_034_swift_redo_and_word_operators.md` (the swift redo and
decision 43), and `log_033`/`log_032` beneath them.

## what log 035 did, in one paragraph

Collected every lane below, executed the ONE thing log 034 had not
built — c++'s six word spellings had a domain from `vw_cpp_*` but no
answers, because c++ is a route-A language — and re-folded. Result:
**238 leaves against log 033's 226, zero codegen-refusal exclusions
against 1,066, and both positive controls passing at similarity
1.000.** Decision 44 lifts decision 30's voiding of php's word
logicals. Details, worked cells and the two faults the pass found in
its own code are in log 035.

## the lane queue — ALL DONE

| lane | what it is | probes | state |
|---|---|---|---|
| `vs_swift_00/01` | swift matrix REDO, full swiftc | 76,614 | DONE, gate COMPLETE, 1,552 accept |
| `lr_words1..5` | leg R, five passes | 91 | DONE, folded; `lr_words5` closed python's two UNREAD cells |
| `rc_ruby2` | ruby route C, repaired, +`and` +`or` | 285,144 | DONE, folded |
| `rc_php2` | php route C, repaired, +`instanceof` | 223,587 | DONE, folded |
| `vw_typescript_00` | ts matrix, +`instanceof` | 10,000 | DONE — **0 accepts, EMPTY DOMAIN, no leaf** |
| `vw_cpp_00..02` | cpp matrix, six word operations | 72,600 | DONE, 8,526 accept |
| `xr_swift_00` | swift EXECUTION redo | 1,552 | DONE, **0 codegen refusals — the check passed** |
| `xw_cpp_00` | cpp word-operation EXECUTION | 8,526 | DONE (log 035), 8,526 answers |
| `ka_kotlin_00..03` | **STUBBED OUT, DEFERRED, never fold by default** | 89,304 | 78 min when re-dropped |

## if you need to rebuild from raw

```
A=SandboxDesign/agent
K=PRIVATE/PseudoCoupHQ/Research/\
kind_fuzz_clustering
cd $K
python3 l3_swiftfull_read.py   # swift matrix
python3 wordop_survey.py       # leg G
python3 wordop_criterion.py    # legs G and R
python3 l3_refold.py           # the three folds
python3 l3_answers12.py        # clusters_all12
python3 make_dendrogram_all12.py
node domstub.js dendrogram_all12.html
```

`l3_refold.py` is RE-RUNNABLE: each fold reads its `SUPERSEDED_` copy
as the base, so running it twice gives the same file rather than
folding twice. `l3_wordexec.py` re-emits `lanes/xw_cpp_00.sh` if that
lane ever has to be run again.

## the two traps log 035 fell into, so the next reader does not

1. **`l3_wordops.with_ops` does not reach `l3_exec`.** That module does
   `from l3_accept import ..., ops` at line 51, binding the function
   object at import time. Use `l3_wordexec.with_ops`, which patches
   `l3_exec.ops` as well. The failure is silent: the lane compiles the
   WRONG operator, exits 0, and writes a full `__SUMMARY__`. The tell
   is a non-zero `CODEGEN_REFUSE` count on a set the compiler accepted.
2. **the manifests are FROZEN and predate decision 43.**
   `manifest_ruby.json` has no `and`/`or` and `manifest_php.json` has no
   `instanceof`, so a reader that iterates `man["operations"]` drops
   those leaves without a word. `l3_answers12.load_three` appends the
   admitted list at read time. **Do not re-freeze a manifest to fix a
   reader.**

## the criterion, in one place — decision 43

A word-spelled binary operation is FIRST CLASS iff BOTH legs hold.

| leg | what it asks | evidence |
|---|---|---|
| G | does the grammar declare the word in the operator slot of a binary-shaped expression node | `wordop_survey.py` over `raw_all/<L>.node-types.json` and `kinds_<L>.json` |
| R | does the language's own checker REFUSE an ordinary variable named with the word | lanes `lr_words*.sh` -> `raw/lr_words*.txt` |

A leg-R verdict is readable only if that pass's CONTROL word `zzfoo`
came back ACCEPT. Two passes failed their own control and were re-run;
`wordop_criterion.py` drops unreadable verdicts rather than reading
them.

## the route-C parenthesis repair

`l3_routec.py`'s php and ruby drivers both wrote
`__r = (a) <op> (b)`. In BOTH languages the word-spelled logicals bind
LOOSER than assignment, so that parses as `(__r = a) <op> b` and the
recorded answer is the LEFT OPERAND. This is log 033 item 4u's php
fault; it is the same fault in ruby and was invisible there only
because ruby had no word-spelled operation in its menu until this pass
admitted one. `l3_wordops.py` applies the repair and re-emits
`lanes/rc_ruby.sh` and `lanes/rc_php.sh` as well as the new
`rc_ruby2`/`rc_php2`. **`behavior_ruby_C.json` and `behavior_php_C.json`
are pre-repair products**; the post-repair ones are `rc_ruby2.txt` and
`rc_php2.txt` and they supersede them for every operation, not only for
the word-spelled ones, because the repair changes no symbol-spelled
cell and that is worth confirming rather than assuming.

## superseded, kept, not deleted

| file | why |
|---|---|
| `valuematrix_swift.json` | swift's matrix taken with `swiftc -typecheck`, the instrument log 032 measured wrong on 40.7 percent of the accepted set. Kept: a wrong instrument that produced a published number belongs on the record |
| `answers_swift.json` | swift's execution over the `-typecheck` accepted set, 1,066 of 2,618 refused at codegen |
| `behavior_ruby_C.json` | pre-parenthesis-repair |
| `behavior_php_C.json` | pre-parenthesis-repair; its `and`/`or`/`xor` rows are the VOID ones of decision 30 |

Log 035 folded all four of those, so the LIVE files now hold the new
measurements and the retired ones were copied aside under these names
before being overwritten:

| kept as | what it is |
|---|---|
| `SUPERSEDED_answers_swift_typecheck.json` | swift's execution over the `-typecheck` accepted set, 1,066 codegen refusals |
| `SUPERSEDED_answers_cpp_symbolsonly.json` | c++'s answers before the six word operations were merged in; the base `l3_refold.py` re-reads on every run |
| `SUPERSEDED_behavior_ruby_C_preparen.json` | ruby's route C, pre-parenthesis-repair |
| `SUPERSEDED_behavior_php_C_preparen.json` | php's route C, pre-parenthesis-repair |
| `SUPERSEDED_clusters_all12_log033.json` | log 033's 226-leaf clustering, kept for the diffs in log 035 §6 |
| `SUPERSEDED_dendrogram_all12_log033.html` | log 033's visual |

## QUARANTINED — never fold these

| file | what happened |
|---|---|
| `raw/VOID_ac_rust_ebusy.txt` | `rustc --emit=metadata -o /dev/null` answers EBUSY on every ACCEPTING probe |
| `raw/PARTIAL_rc_php_fatal.txt` | `Cannot redeclare class R0` FATAL at 2,001 of 215,306 |
| `raw/PARTIAL_rc_python_oomkill.txt` | SIGKILL, out of memory, at 19,829 of 342,225 |
| `raw/VOID_lift_b_rust_run1.txt` | a wrong expansion that would have CONFIRMED the assumption under test |
| `raw/SUPERSEDED_ex_kotlin_rangebug.txt` | the recorder walked a `LongRange` as an `Iterable` |
| `raw/SUPERSEDED_ex_kotlin_arrayhash.txt` | java arrays recorded through `toString`, identity hash inside |
| `raw/VOID_xw_cpp_00_wrongops.txt` | log 035: the op list did not reach `l3_exec`, so the lane compiled c++'s STANDING menu — `k=3` is `not_eq` in the word list and `/` in the standing one. 2,466 `CODEGEN_REFUSE` of 8,526 reading `no match for 'operator/'`. **The lane exited 0 and wrote a full, gate-passing `__SUMMARY__`** |
| `raw/SUPERSEDED_rc_ruby_preparen.txt` | ruby's route-C raw, pre-parenthesis-repair; renamed out of `rc_ruby.txt` so no reader folds it |

The reader folds every `raw/<prefix>_*.txt` it finds, so anything not
to be folded must carry a `SUPERSEDED_` or `VOID_` prefix. That is this
node's standing convention.

## the lane mechanics, unchanged

- lane scripts live in `lanes/`; drop them into
  `SandboxDesign/agent/drop/`
- poll `SandboxDesign/agent/status/<name>.sh.status`
- products land in `SandboxDesign/agent/out/<name>.txt`
- the daemon is SERIAL and kills a script at 3600 s, which is why every
  matrix is sharded
- `/work` is a 4 GB tmpfs and a tmpfs charges a whole block per file;
  every matrix lane sweeps its own directory on exit and prints the
  free space it leaves. **Check free scratch before queueing.** It was
  2,566 MB when this session started
- the toolchains are NOT all on the default PATH: swift is at
  `/persist/swift/usr/bin`, kotlin at `/persist/kotlinc/bin`, dart at
  `/persist/dart-sdk/bin`, dotnet at `/persist/dotnet`, the typescript
  checker at `/persist/tv/ts5/node_modules/typescript/lib/typescript.js`
- the `libncursesw` symlink survived this session's container restart;
  the `ncurses_fix` preamble every generated lane carries re-makes it
  anyway and is cheap

## the standing rules a later agent must not quietly drop

- Progress print-outs — [done/total], elapsed, ETA — on every
  generation and every run phase.
- Read `complete` before reading verdicts. Five lanes have now lied
  about finishing.
- Grep for ENOSPC before folding.
- A probe harness needs a CONTROL. Leg R above cost four passes because
  the first one had none for five of the twelve languages, and two of
  the harnesses were broken in a way that looked exactly like a
  measurement.
- Overlapping cells keep BOTH routes' verdicts; a disagreement is a
  finding and is never reconciled silently.
- `rust-src` installs to `/opt/rustup`, not `/persist`; a container
  rebuild loses it.
