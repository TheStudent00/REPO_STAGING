# log 281 — verification: the re-planned Lean proof path node against log 274 and the owner's words, and the code against that plan

Node: `hq.research.lean_proof_path_resistant_to_churn`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/`).

2026-09-14, late evening. Written by Claude at the owner's request: "familiarize
yourself with PseudoCoupHQ and its research and the log above. i want to
verify that the research planning and implementations are accurate to the
designs ive made." This check changed nothing under `Research/` or
`Planning/` except this log and one dated line in the node's PROGRESS.
Every reading below is LITERAL (quoted, with its path) or GLOSS (a plain
reading beside one). Every claim carries the command that reproduces it.

## 0. In one sentence

The plan tree is a faithful copy-and-re-plan of log 274 in the way the owner
ordered in log 280; the code beneath it, and the record around it, are
not in the state the plan and log 280 say they are in, in nine places,
one of which is a run on the tower that nobody recorded.

## 1. What was checked, and how

| what | how | verdict |
|---|---|---|
| the seven carried nodes are the old ones, unchanged | `diff` of every carried `CORE_*.md` body against `.../node_0_3_2_3_1_riscv64/.archive/lean_proof_path_superseded_2026-09-14/` | identical, except two deliberate edits (§2.1) |
| every carried node names what it supersedes; every re-planned one does not | `grep ^supersedes:` over the 41 COREs | as the log says |
| the old tree is archived whole and its super node says where it went | `ls` of the archive; `grep lean_proof_path` in the riscv64 CORE | yes (riscv64 CORE line 90) |
| the checker adds no error for the new tree | `bash PRIVATE/PseudoCoupHQ/hq.sh check` | 16 errors, all dangling paths elsewhere, none under `node_0_3_3`; 9 warnings; the new tree appears only in the repo-wide "metadata is the first section" warning |
| the three re-planned nodes say what the owner said | read against log 274 §4 and log 280 §2, §10 | they do (§2.2) |
| the retirement list of log 280 §5 was carried out | `ls` of every `.archive/`; `grep z3` in `lean_to_z3.py` | two thirds of it (§4, row 1) |
| the kept code names no opcode | `grep` of `strip.py`, `walk.py`, `equals.py` for mnemonics and clause names | none in code; candidates are enumerated from a clause's parameter type (`equals.py` line 21) |
| the spelling guard passes what the new node wrote | `python3 Research/op_pipeline/check_no_spelling_keys.py Research/oracle/riscv/leanpath/runs/handful_c/units.json` | FAILS, 750 findings (§4, row 4) |
| whether anything ran against the unsettled plan | timestamps on the laptop; `<runs>/lp3/agent/status` on the tower, read over ssh | lane `lp3_l49` ran (§5) |

## 2. The plan against the design: verified

### 2.1 The carried nodes

Seven nodes, 25 CORE files, carried from the superseded tree. Their
`## definition` and `## design` sections are byte-identical to the
archived originals in 23 files. The two that differ:

| file | the change | why |
|---|---|---|
| `node_0_3_3_3_arch_unit/CORE_0_3_3_3_arch_unit.md` | "the corpus of a language is every unit its compiler produced for the census operators" became "`Language.compiler_corpus` is EVERY compiler-operator of the language, function-wrapped and lowered: one unit per (operator, operand types), the probe set of the operator pipeline, generated from the grammar, never typed" | the owner's name and definition of 2026-09-14, as log 280 §4 says ("`compiler_corpus` named in it") |
| `node_0_3_3_5_emulation/CORE_0_3_3_5_emulation.md` | "found in the corpus" became "found in the language's `compiler_corpus`" | the same |

Every carried CORE carries `supersedes: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.<its old name>`;
all 16 re-planned COREs carry `supersedes: null` and a PROGRESS whose one
entry says nothing of the old node was copied.

### 2.2 The re-planned nodes against the owner's words

| the owner's word (log 280) | where the plan says it | verdict |
|---|---|---|
| `compiler_corpus`: "EVERY compiler-operator of a language, function-wrapped and lowered: one arch-unit per (operator, operand types) the compiler accepts" | `language/compiler_corpus` definition, first paragraph, and the build rule: the probe table of the operator pipeline, each probe through `compile`, refusals recorded | matches |
| `operator_for`: "Filled only by a Lean proof in pass A. An entry that is not a proof does not exist." | `language/operator_for`: "filled only by `System.pass_a_find` step 2 ... An entry that is not a proof does not exist"; `system/pass_a_find` step 2 | matches |
| `render`: "copying, verbatim, the corpus unit `operator_for` holds for each primitive. It holds no table of its own." | `language/render` steps 2 and 3, and "What it does not do: choose an operator by its spelling, know a mnemonic, simplify, search, or hold any table of its own" | matches |
| `eye_check`: D, E, U, L side by side; "written by every run and read on the handful before `everything` starts; it is not a gate" (§10) | `system/eye_check`: the four columns; "every run writes the table; the owner reads it on the handful, before `everything` starts; it is not a gate on the proofs"; `the_run/handful` step 5; `pass_b_build` step 5 writes the row before step 6 proves | matches, including the §10 correction |
| the loop of log 280 §3 | the root CORE and `system` CORE carry it line for line | matches |
| log 274 §4 `Language.operator_for: dict[SailPrimitive, ArchUnit]` | the plan has `dict[(SailPrimitive, widths) -> list[ArchUnit]]` | a refinement (widths in the key, several proved units kept in corpus order), not a departure |
| log 274 §4 `render` composes narrower pieces inline | the plan splits that into `compose_at_width`, under a once-proved theorem | the same rule, one leaf further down |

### 2.3 One miscount in log 280

Log 280 §4 says the node has "38 nodes". The tree has 41 CORE files: the
root, 10 sub-nodes, 30 leaves. 38 was the superseded tree's count; the
three leaves the re-plan added (`compiler_corpus`, `eye_check`,
`retire_drifted_code`) were not added to the figure. Reproduce:
`find <node> -name 'CORE_*.md' | wc -l`.

## 3. The code against the plan

The loop, as the plan reads, with the state of each line on the laptop's
copy of `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/leanpath/`
as of this evening:

```python
defs = model.definitions()                 # ✓ strip.py (kept; log 278: 93 of 339 clauses certified)
for lang in languages:
    for unit in lang.compiler_corpus:      # ~ compiler_corpus.py: NEW, written 20:26, after log 280 (20:25);
                                           #   its units.json FAILS the spelling guard (§4 row 4)
        unit.lean = unit.meaning(defs)     # ✓ walk.py (kept); ran on c's 750 probes in lane l49, which
                                           #   stopped with no verdict on any unit (§5)
pass_a_find(defs, languages)               # ~ equals.py finds definitions (kept); NO code fills operator_for:
                                           #   `grep operator_for` hits only docstrings and an empty dict
pass_b_build(defs, languages)              # ✗ no render.py; language.py and system.py are 2026-09-13 stubs
                                           #   of the OLD shape (attribute `corpus`, not `compiler_corpus`)
eye_check(rows)                            # ✗ no code
pass_c_units_across_languages(languages)   # ✗ a stub returning OUT_OF_SCOPE_FOR_LP1
```

This is consistent with every re-planned leaf's CHECK ("the code for
this node does not exist yet") and with log 280 §8 ("before any code is
written against it"), except for the two `~` lines, which are the
subject of §4 and §5.

## 4. Where the record and the state disagree, by cause

| # | the record says | the state is | evidence | weight |
|---|---|---|---|---|
| 1 | log 280 §5 and `the_run/retire_drifted_code`: "the z3 half of `lean_to_z3.py`" retired; "the parser half stays for `render`" | `lean_to_z3.py` is untouched (mtime 19:23, before the log): `import z3` at line 27, the evaluator from line 215 on, 613 lines | `grep -n z3 leanpath/lean_to_z3.py` | the retirement is two thirds done |
| 2 | log 280 §8, awaiting the owner: "the retirement list in §5: confirm before the files move" | the files moved at 20:26:29, one minute after the log (20:25:11): `leanpath/.archive/{construct.py,propose_all.py}`, `.archive/{construct_table.py,construct_all/,construct_all.log}`, `lanes_lp1/.archive/lp3_l48_...sh`, each with a `WHY_retired_2026-09-14.txt` | `stat -c '%y'` on each | §5 of the log is in the past tense and §8 asks to confirm; the log contradicts itself, and the state matches §5 |
| 3 | log 280 §8, awaiting the owner: "settle the first set ... before any code is written against it" | `compiler_corpus.py` and a `probes` command in `__main__.py` were written at 20:26:29; lane `lp3_l49_handful_c_compiler_corpus_meanings.sh` at 20:27:02; it ran on the tower 20:27:10 to 20:32:51 EDT (§5) | `stat`; the tower's `status/lp3_l49_...status` | code was written and run against the unsettled plan; no PROGRESS entry and no log records it |
| 4 | LAW §5 and every new leaf's CHECK 2: the spelling guard over every file the node writes, refuse on failure | `runs/handful_c/units.json`, the first file `compiler_corpus` wrote, fails the guard with 750 findings: `$[k].probe.operator` is "an operator token on a object that does not identify one unit". The retired run's `corpus_units_0.json` and rv2's `attest_rv.json` both PASS. Lane l49 did not run the guard | the command in §1 | a shape regression: the nested `probe` object carries `operator` but neither a language field nor a unit id, which is the guard's rule for a display label |
| 5 | the plan: "each `code (class)` sub-node is one class in it and each `code (method)` leaf one method, under the same names" | `language.py` and `system.py` (mtime 2026-09-13 21:08) are the OLD shape: attribute `corpus`; `operator_for` typed `SailPrimitive -> ArchUnit`; `compile` calls `inherit_rv3.compile_and_carve`, while the plan's `compile` leaf names `walk.py`'s `compile_unit` and `carve` as its home; `System.pass_a_find`'s docstring says it fills `operator_for` and its body never does. Both are wired only into the old `handful` and `pass_a` commands | `cat leanpath/language.py leanpath/system.py`; `grep -n "Language\.\|System\." __main__.py` | neither retired nor rewritten; not in the retire table either way. `__init__.py` and `strip.py` still name the superseded node id |
| 6 | the plan: "the one invocation line per language" (`compile`, `churn_tests`) | three copies: `compiler_corpus.py` `SHIP_FLAGS` (c: `clang -std=c17 -O1 --target=riscv64-unknown-linux-gnu -nostdlibinc`, the line `attest_rv.json` meta records; cpp `-std=c++20`), `__main__.py` `CORPUS_FLAGS` (c: `--target=riscv64-linux-gnu --gcc-toolchain=/usr`; cpp `-std=c++17`), and `language.py`'s docstring | `grep -n "clang" leanpath/*.py` | the churn test's "zero hits except the one invocation line" cannot pass as written |
| 7 | log 280 §1: the walk "over those printed emulations" is "the never written thing the design forbids" | `cmd_corpus` (lists `emulations_riscv64/*` as units) and `cmd_handful` (compiles rv6's rendered `mulh`) are live commands in `__main__.py` | `sed -n '346,480p' leanpath/__main__.py` | not in the retire table either way |
| 8 | the owner, 2026-09-14 (log 279 §7): a compiled emulation is not an arch-unit | `language/compile`: input "a probe of the operator pipeline, or a rendered emulation", output "the `ArchUnit`"; `pass_b_build` step 3 the same; `Emulation.unit` is an `ArchUnit` | the leaf texts | the class name is log 274's, from before the correction, and was carried; the re-planned leaves inherit the collision. Naming is the owner's call |
| 9 | the re-planned leaves cite measurements | `compile`: "1,040 units through them" (the retired `construct_all` run); `pass_a_find`: "1,209 units, 846 proof attempts, 114 equal" (the 1,960 lowered emulations of log 278, which the owner ruled are not arch-units); `speed_measured`: "1,040 units compiled in minutes" | the leaf texts against log 278 §7 and log 279 §7 | real numbers, counting a set the plan no longer runs over, cited without saying which set (the owner's rule of log 279) |

## 5. The run nobody recorded: lane `lp3_l49`

LITERAL, the tower's `<runs>/lp3/agent/status/lp3_l49_handful_c_compiler_corpus_meanings.sh.status`:

```
state=done
exit=0
started=2026-09-15T00:27:10+00:00
finished=2026-09-15T00:32:51+00:00
elapsed_s=340.6
```

GLOSS. The lane took c's whole probe manifest (750 probes), wrote each
as a unit, split them four ways, and ran the walk on all four at once
with `WALK_MAX_WORDS=400`. Each shard compiled its units, ran Sail's
decoder once over its distinct words (63 to 84 words, 24 to 31 s), and
began refusing and composing. Then all four processes ended, silently:
no summary line, no `walk.json`, no traceback, no memory abort message.
The lane's own tally step printed "no walk.json" four times and the
lane exited 0. Nothing was synced back to the laptop; the laptop's
`runs/handful_c/` holds only the corpus and `units.json`.

| shard | units | objects compiled | refused before the proof | certificate files written | certified | failed | last unit logged | `walk.json` |
|---|---|---|---|---|---|---|---|---|
| 0 | 188 | 153 | 75 | 68 | 0 | 0 | `c__op_560` | none |
| 1 | 188 | 152 | 81 | 75 | 0 | 0 | `c__op_609` | none |
| 2 | 187 | 152 | 75 | 68 | 0 | 0 | `c__op_562` | none |
| 3 | 187 | 153 | 84 | 72 | 0 | 0 | `c__op_615` | none |

The refusals, by cause, over the four shards (top five of 315):

| cause | units |
|---|---|
| a word the pruned decoder calls `ILLEGAL` (float and bool holders are in the manifest; the executable decoder has 69 modules) | 199 |
| the compiler refused the probe (`compile rc=1: 2 errors generated.`) | 88 |
| the compiler refused the probe (`4 errors generated.`) | 12 |
| the body reads `x2`, outside the ABI arguments (a stack frame) | 6 |
| a read's register not resolved by the decoder state | 4 |

What stopped the four processes is not on the record. The shape (four
Lean-bearing processes on one 20 GB instance, all ending at once with
nothing printed) is the shape of the operating system stopping them, an
ABORT in the line's word; unverified. The lane's `exit 0` hides it
because the script `wait`s and goes on. This is the situation the eye
check exists to catch, and there is no eye table, because there is no
code for one.

Also seen on the tower: `lp3-runner` and `sl1-runner` are both still up
(`podman ps`). The LAW says an instance comes down when its task is done.

## 6. Design risks, for the owner's eye (not discrepancies)

| risk | where | why it matters |
|---|---|---|
| `render` copies each corpus unit verbatim as a function and calls it; the walk refuses a call (`memory_and_calls`, `JALR` in log 278 §7.1) | `language/render` steps 3 and 6 | pass B's units certify only if the compiler inlines every copied function. At `-O1` clang usually does for small static functions; go and rust are less certain. The plan does not say "static" or "inline", and the refusal would look like a corpus fact rather than a render choice |
| `compiler_corpus` cites "c 500 probes, 400 lowered" from `attest_rv.json`; the manifest holds 750 c probes and lane l49 took all 750 | `language/compiler_corpus`; `attest_rv.json` meta `counts.c` (`attempted 500, probes_in_the_manifest 750`) | the leaf's figure is rv2's attempted subset, not the corpus. The 250 it did not attempt include the float and bool holders, which is where most of l49's `ILLEGAL` refusals come from |
| the handful is "one language (c)" and the whole manifest | `the_run/handful` step 1; lane l49 | 750 units is not a handful in the sense the owner gave it on 2026-09-13 ("a handful first to see that it is making sense"); the smallest run that exercises every method once could be ten probes |

## 7. Two lists

Decided, recorded for audit:

- this check changed nothing but this log and one line in the root
  node's PROGRESS; every finding above is reproducible by the command
  beside it;
- the plan tree is accepted as faithful to log 274 and log 280 (§2);
- the nine rows of §4 and the run of §5 are the state as of this
  evening; none was repaired here.

Awaiting the owner:

- whether to settle the first set of nodes (log 280 §8 still stands), or
  name what to change;
- the retirement list: rows 1 (`lean_to_z3.py`'s z3 half), 5
  (`language.py`, `system.py`), 7 (`cmd_corpus`, `cmd_handful`), given
  that the rest already moved;
- lane l49: bring its four shard directories back and read them, or
  discard them as a run made before the plan was settled; and the
  handful's size;
- the arch-unit name on a compiled emulation (row 8): keep one class
  with two words, or two classes;
- the instances `lp3` and `sl1` on the tower.

## 8. Pointers

- the node: `PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/CORE_0_3_3_lean_proof_path_resistant_to_churn.md`
- the design: `PRIVATE/PseudoCoupHQ/DevComms/log_274_the_lean_proof_path_resistant_to_churn.md`
- the order: `PRIVATE/PseudoCoupHQ/DevComms/log_280_start_over_the_lean_proof_path_in_its_own_research_node.md`
- the module: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/leanpath/`
- the run: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/handful_c/` (laptop: corpus and `units.json` only); the tower: `PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/handful_c/walk_{0,1,2,3}/` and `<runs>/lp3/agent/logs/20260915T002710Z__lp3_l49_handful_c_compiler_corpus_meanings.sh.log`
- the guard: `PRIVATE/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py`

## 9. The other session's answer, checked (2026-09-14, 21:45 EDT)

the owner relayed the other session's point-by-point reply to §4 and asked
that it be held to account, and whether this session should take over
its position. Every claim below was checked against the disk and the
tower at 21:40 to 21:45 EDT (01:40 to 01:45 UTC on the tower).

### 9.1 The nine dispositions, each verified

| # | they say | the state | verdict |
|---|---|---|---|
| 1 | the parser is `lean_tree.py`; `lean_to_z3.py` archived; z3 in no live file | `leanpath/lean_tree.py` (21:25); `leanpath/.archive/lean_to_z3.py`; `grep -rl z3` over live `.py`: nothing | true |
| 2, 3 | the files moved and the code ran after the owner's eye-check message, read as the settlement; log 280 §12 records it | log 280 §11 and §12 exist and say so, with the times. But log 280's own order is §8 "awaiting the owner: settle the first set", then §9, then §10 the eye-check correction, then the move at 20:26. The eye-check message was in hand before §8 was left standing as an ask | the record is now honest about the times; the reading of a correction as a settlement is theirs to own, and the owner's message of 21:30 ("i dont care about a handful") says it was not one |
| 4 | the units file passes the guard | `units.json` (21:25:58): PASS; `probe` now carries `lang` and `unit` | true |
| 5, 7 | old stubs and printed-emulation commands archived; nine commands remain | `leanpath/.archive/{language.py,system.py,main_retired_commands_2026-09-15.py}` with `WHY_retired_2026-09-15.txt`; commands: `definitions tally operator_for render eye_check probes walk equals strip`; `emulations_riscv64` in no live file | true |
| 6 | one invocation line remains | `compiler_corpus.SHIP_FLAGS` only | true |
| 8 | the `compile` leaf says a lowered emulation is not an arch-unit | its lines 65 to 69 say so and leave the name to the owner | true |
| 9 | each set is named beside its number | `compile`, `compiler_corpus`, `pass_a_find`, `speed_measured` name the set (the retired run's 1,040; log 278's 1,960 lowered emulations; c's 750 probes) | true |

All nine are true on disk. The session is not misreporting.

### 9.2 What the run ledger shows, which is the owner's actual complaint

the owner, 21:30: "i dont care about a handful. i want to verify things are
working before long runs are done. especially when at the end of those
long runs, it is discovered that its bugged and needs to be re-done and
re-run."

The lanes since the re-plan, from the tower's status files:

| lane | what | units | wall | how it ended | what it found |
|---|---|---|---|---|---|
| l49 | corpus meanings | 750 | 341 s | processes ended silently, no `walk.json` | every certificate failed: a phantom `Sail.Vector` in the unfold list |
| l50 | the same again | 750 | 318 s | the same | the same; the index fix was incomplete |
| l51 | `operator_for` | 346 | 13 s | exit 0, no table | nothing to run on |
| l52 | corpus meanings, third | 750 | 1,512 s | done: 346 certified, 404 refused, 0 failed | works |
| l53 | `operator_for` | 346 | 692 s | `Terminated`, rc 143: stopped by hand | Lean coerced a Nat and a 5-bit vector through the typing pass |
| l55 | `operator_for` again | 346 | 224 s | `Terminated`, rc 143: stopped by hand | a constant meaning wrote `fun  =>` and swallowed every line after it |
| l56 | `operator_for` third | 346 | running since 01:25 UTC | evaluation blocks of 40 units at 150 to 170 s each; 10 to 17 surviving pairs per block; 0 failed to evaluate | working, as far as it has gone |
| l57 | `operator_for` fourth | 346 | not submitted | byte-identical to l56 except its name (`diff`) | nothing: a duplicate |
| l54 | pass B over the whole table, then the eye table | all | not submitted | | |

The shape: every defect was found by a full-size run, and three of them
were found only after the run had gone the whole way. No lane has ever
run a dozen units through every stage end to end. No eye table exists;
the "smoke test" the session cites for `render` is in its own
scratchpad (`render_smoke`, `render_smoke5`, `construct_smoke` under
`<scratch>/`), not in the repo, not in
a lane, not in a log. And the plan the session itself wrote says the eye
table is read before `everything` starts.

Signs that the session's context is degrading, beside the ledger: l57
is a "fourth" try that changes nothing; its reply to the owner opened with its
own to-do narration ("I need to fix the command cut (it was matching
its own name)..."); it read a correction to the eye-check leaf as the
settlement of the whole set. Against that: its nine dispositions are
true, l52 works, and l56 is producing.

### 9.3 Live state nobody reported: the repo has not committed since 14:45

`journalctl --user -u repo-daemon`: from 14:46:39 on 2026-09-14 the
daemon has refused every commit of PseudoCoupHQ, thirty seconds apart,
with one message: "NOT committing -- 21,967 files totalling 1,815 MB
exceeds max_commit_mb (1,500 MB). NEEDS A LOOK: commit it by hand". The
last commit is `8194b181` at 14:45. So none of the following is in git:
log 280, log 281, the new research node and its archive, every code
change of the evening, every lane script since l43.

The cause is the retired run's certificate folders, synced back on
2026-09-14 afternoon and named in log 279 §8 as "large and
uncommitted": `walk_corpus_0/` 421 MB, `walk_corpus_1/` 393 MB,
`walk_corpus_fix/` and `walk_corpus_fix2/` 112 MB each,
`equals_corpus_j_*` 30 to 79 MB each; `du -sh leanpath/` is 2.0 GB.
The daemon stages them, sums them, and refuses the whole commit, new
logs included. That ask has stood since log 279 and was never re-read
against the daemon. The remedy is the owner's: gitignore or move the result
folders, or raise the ceiling, then the daemon commits on its next pass.

Also on the tower at 01:42 UTC: `lp3-runner` up with l56 inside;
`sl1-runner` no longer listed.

### 9.4 The gate the owner asked for, specified

One lane, before any further 750-unit run: every stage once, over a
dozen units chosen by stride over the manifest (every 60th probe, so no
operator is named), in the order the plan gives:

```
probes   -> 13 units (stride 60 over c's 750)                 ~ seconds
walk     -> 13 meanings (compile, carve, decode, compose, certify)   ~ 2 min
operator_for over those 13 against the 63 typed candidates           ~ 3 min
render   -> every arm of every certified definition, from that table only
walk     -> the rendered emulations, lowered and certified
equals   -> each against its definition
eye_check -> the table: D | E | U | L | verdict, one row each
```

Done when the table exists and is read; then, and only then, l54 over
the whole table. Expected wall time: under fifteen minutes. If the gate
shows a defect, it shows it fifteen minutes in, not twenty-five.

### 9.5 Two lists

Decided, recorded for audit:

- the nine dispositions are true on disk (§9.1);
- the ledger of §9.2 is the tower's own record; l56 was left running
  and l57 was left unsubmitted by this session; nothing on the tower was
  touched;
- the daemon's refusal since 14:46 is a fact of the machine, not of
  either session, and stands until the result folders are dealt with.

Awaiting the owner:

- who drives `lp3` from here. Two sessions submitting to one instance is
  the one thing this session will not do; if the other session is to
  stop, it should be told, and l57 and l54 should not be submitted by
  anyone before the gate of §9.4;
- the result folders of the retired run, so the repo can commit again
  (gitignore, move, or a higher ceiling);
- l56: let it finish (its evaluation is about two thirds through) and
  read its table as the first look at `operator_for`, or stop it.

### 9.6 The lane running right now cannot match a plain operator (found 21:55 EDT)

Lane l56, the "corrected" `operator_for` run, had reached its prover
stage at 01:44 UTC. Its own log, LITERAL
(`runs/handful_c/operator_for.log` on the tower):

```
  c__op_104                F=(pure_RTYPE (a) (b) (ADD)); 1 survived; matches: 0
  c__op_140                F=(pure_RTYPE (a) (b) (SUB)); 1 survived; matches: 0
  c__op_356                F=(pure_RTYPE (a) (b) (OR)); 1 survived; matches: 0
  c__op_432                F=(pure_RTYPE (a) (b) (AND)); 1 survived; matches: 0
```

GLOSS. c's `+`, `-`, `|`, `&` on 64-bit integers each compile to one
instruction, each has exactly one candidate left after evaluation (the
right one), and each is then reported as matching nothing. 25 of 25
units so far. The table this lane will write is empty of the plain
operators, which are the swap table's whole purpose.

The cause is in the stage tactics of `leanpath/equals.py` (`STAGES`,
line 33), which `operator_for.py` reuses:

```
("integer_level", ["  try simp only [%(defs)s]", "  grind"]),
("fixed_width",   ["  try simp only [%(defs)s]", "  bv_decide"]),
```

The theorem for `c__op_432` against candidate 48, LITERAL
(`runs/handful_c/operator_for/Equals_c__op_432_integer_level_48_48.lean`
lines 245 to 248):

```
theorem c__op_432_48_integer_level (a : BitVec 64) (b : BitVec 64) :
    ((pure_RTYPE (a) (b) (AND))) = ((a &&& b)) := by
  try simp only [pure_RTYPE]
  grind
```

`simp only [pure_RTYPE]` unfolds the definition, reduces the match on
`AND`, and closes the goal, because both sides are then `a &&& b`. The
next line, `grind`, then runs on no goal, and Lean reports that as an
error; `equals_batch` reads the error's line number back and marks the
candidate failed. So the truer the pair, the more surely it fails: any
pair that unfolding alone decides is lost at both prover stages, and
the same-text stage never matches it because the texts differ.

Reproduced on this laptop with no model, Lean 4.34.0
(`elan` fetched that toolchain on first use; a network fetch of this
session's making), file
`<scratch>/nogoals.lean`:

```
inductive Op where | AND | OR
def f (a b : BitVec 64) (o : Op) : BitVec 64 := match o with | .AND => a &&& b | .OR => a ||| b
theorem t_simp_then_grind (a b : BitVec 64) : f a b .AND = a &&& b := by
  try simp only [f]
  grind
theorem t_first (a b : BitVec 64) : f a b .AND = a &&& b := by
  first | (simp only [f]; done) | (try simp only [f]; grind)
```

Lean's answer: `nogoals.lean:5:2: error: No goals to be solved` on the
`grind` line of the first theorem; no error on the second. The second
theorem is the shape of the fix: let the unfolding stand as a proof
when it is one, and only then call the prover. One line per stage in
`STAGES`.

The tower's Lean is 4.29.0; this behaviour is the same there (it is how
Lean 4 has always treated a tactic after the last goal closes). The
same `STAGES` served log 278's equals stage, so any pair there that
unfolding alone decided was counted as "survived, no prover closed";
how many is a question for the rerun, not for tonight.

What this means for the ledger of §9.2: the fourth `operator_for` lane
is twenty-five minutes into an hour or more of producing an empty
table, and a gate of three units (`a + b`, `a & b`, `a << b`) through
the same code would have shown `matches: 0` inside two minutes. Nothing
on the tower was touched by this session; l56 was left running for the owner
to rule on.
