# Task lp1 — the Lean proof path, the handful: Sail's Lean output as the definitions, Sail's `execute` composed as the walk, Lean as the prover, on ten units first

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it
(waits in short calls; the spelling ban; sync args in the flat form).
Then `Research/GLOSSARY.md` (the last six entries are this path's
words). Then the log this task implements,
`PRIVATE/PseudoCoupHQ/DevComms/log_274_the_lean_proof_path_resistant_to_churn.md`,
ALL of it: §2.3 is the object, §4 is the code you are writing, §5.3 is
the expectation you measure, §6 is the test every line you write is
held to. Then the plan, which IS the code at a coarser depth
(`plan_and_code.md` §1): every CORE under
`Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/`,
one class per sub-node, one method per leaf, under the names the code
uses. Then logs 258 (rv1, the handful of ten carved units), 273 (rv9,
§3.6: the multiply-high cause named) and 262 (t4, §"Lean": how the
line already calls `bv_decide`). Instance `lp1.conf`
(`PUBLIC/Airlock/instances/lp1.conf`; proxy on, for the
one fetch lane only; its own empty persist volume). Artifact folder:
`Research/oracle/riscv/leanpath/`; the module the plan names; lanes
under `Research/oracle/riscv/leanpath/lanes_lp1/`.

## 0. the owner's criterion, 2026-09-13, that this task exists for
"if i stop making updates to the repo and things that it processes
churn, the system will still be able to re-generate essentially all
the proofs, Hub, and whatever else downstream by running the system."
And: "no human intelligence (LLM or biological) is pointing to a
spelling and saying 'that's div!'". And, the same day, the test of
every line: `written once` (the algorithm; it names no opcode, no
compiler, no language version) against `never written` (anything per
opcode, per compiler, per release). A change you are about to make
that would differ for `mulh` and for `add` is refused by this rule;
say so in the log and stop that line. `riscv_reference.py` is READ
for the ABI facts only and is never the definition of anything here.

## 1. What is already on disk, and what you build
`the cached emit`
- `Research/oracle/riscv/leanpath/cache/sail-riscv_3243f93_I_insts_M_insts_postlude_main/`:
  Sail's Lean output for the model at that commit, the lake project
  the backend wrote (`lakefile.toml`, `lean-toolchain` pinning
  `leanprover/lean4:v4.29.0`, a `require` of `Sail` from
  `https://github.com/rems-project/lean-sail` rev `v4`), `LeanIM/*.lean`
  (62,893 lines), `MANIFEST.md`, and the emit lane's log. A build
  product; nobody edits a file in it. If you need a different module
  selection, re-run the emit (log 274 §3, the invocation verbatim; leaf
  module names; `sail --list-files` first; the tower; 20g) into a new
  cache folder named the same way.
`the image`
- `sail` 0.20.2 at `/opt/opam/default/bin`; Lean 4.24.0 and lake at
  `/opt/elan/bin`; z3; core `grind` proves
  `(a + b) * (a + b) = a*a + 2*a*b + b*b` over `Int` in one line
  (measured 2026-09-13); NO Mathlib. clang 21, go 1.26, rust with
  `riscv64gc-unknown-linux-gnu`, riscv64 headers at
  `/usr/riscv64-linux-gnu`; `llvm-objdump --mattr=+m,+a,+f,+d,+c,+zba,+zbb,+zbs -M no-aliases`.
`what you build`, under `Research/oracle/riscv/leanpath/`
- the module `leanpath/` with the classes and methods of the plan,
  under their names: `SailModel.definitions/key_of/strip`,
  `LeanExpr.equals/widen/normalize_integer_level/decide_fixed_width/primitives`,
  `ArchUnit.meaning/decode/compose/branch_rule/memory_and_calls`,
  `Language.compile/render/compose_at_width` with `operator_for`,
  `Emulation`, `Dictionary`, `System.run/pass_a_find/pass_b_build`.
  Methods do not need the instance unless they genuinely do
  (`plan_and_code.md` §7). Python drives; every semantic step is a
  Lean file Lean checks: the definitions are Sail's Lean, a unit's
  meaning is Sail's `execute` composed IN LEAN (unfolded by `simp`, not
  re-parsed into a Python expression), and every equality is a theorem
  whose proof Lean's kernel accepts. Python may parse the emitted Lean
  text only to LIST the clauses and their keys (`key_of`), never to
  rewrite a definition.
- pass C is out of scope here; leave its method a stub that says so.

## 2. The lanes, in order, each sampled before it is run whole
1. `lp1_l1_fetch_and_build_lean_sail.sh` — the ONE lane with the
   network: `elan` installs the toolchain the cache pins; `lake build`
   of the cached project fetches `lean-sail` v4 and builds the model's
   Lean once, into `/persist`; paste the toolchain and library versions
   and the build's wall time and peak resident. A host the proxy refuses
   is a FLAG with the literal refusal (the coordinator adds it; do not
   work around). Every later lane states that it fetched nothing.
2. `lp1_l2_definitions_sample.sh` — `SailModel.definitions` over the
   cache: the count of `execute` clauses by extension, the keys as
   `key_of` reads them from the assembly clauses (paste ten), and
   `strip` on `DIV` and on one `MUL` family clause, LITERAL: the pure
   expression Lean holds after `simp` unfolds the reads and the write.
   A clause `strip` refuses is a row with the construct named.
3. `lp1_l3_meaning_on_the_handful.sh` — `ArchUnit.meaning` on the ten
   carved units of rv1 (log 258; recompile them for riscv64 at ship
   flags with `Language.compile` if the objects are not on disk):
   `decode` by Sail's own `encdec_backwards` (paste one word and its
   constructor), `compose` in Lean, the branch rule where a body has
   one, the answering register's expression, LITERAL for three units,
   seconds and peak resident for all ten.
4. `lp1_l4_equals_on_the_handful.sh` — `LeanExpr.equals` of each unit's
   meaning against its cell's definition, in the plan's order: integer
   level (`grind`) first, then `widen` and `bv_decide` with the standing
   30 s budget, then undecided with the stage. Include `mulh` on c
   (`(__int128)a * b >> 64` and its compiled body) among the ten, so
   that log 274 §5.3's expectation is measured: does `grind` close it
   at the integer level where log 273 measured the wall. Paste the
   theorem file and Lean's verdict for every one of the ten, LITERAL.
5. `lp1_l5_pass_a_over_the_corpus.sh` — `System.pass_a_find` over the
   rv6 corpus (every RISC-V cell, c, c++, rust, go: the units and
   sources `construct/general/rv6_all_langs.py` and
   `emulations_riscv64/` hold), one process: the dictionary entries
   found, the swap table per language, and every `Differ` and
   `Undecided` as a row with its stage. This is the first population
   run; if the handful's timings say it exceeds the lane ceiling, run it
   over a stated fraction and say so, never a filter by bookkeeping.

## 3. What to measure and report
1. the definitions: clauses by extension "of N"; keys as read; the two
   stripped clauses LITERAL.
2. the handful: ten rows, each with the stage reached
   (decoded / composed / integer-level / fixed-width / theorem-kind /
   undecided), seconds per stage, peak resident, the proof file's path
   or the refusal LITERAL. The `mulh` row's verdict is the headline
   either way.
3. pass A: the table "of 255" per language beside log 273 §6.2's union
   of routes (c 243, c++ 243, rust 247, go 243; 251 on some language,
   235 on all four), the swap table's size per language, the refusals by
   cause.
4. speed, measured, per stage, beside log 274 §7.1's expectations.
5. the churn statement: what in this module names an opcode (the
   answer must be nothing, with the grep pasted), and what would happen
   on a new model commit (the cache misses; the emit re-runs) and on a
   new compiler release (pass A re-proves).
Guard (`check_no_spelling_keys.py`) over every json; `grep -c exempt`
over files you add = 0; log (next free number; check the folder);
verifier; PROGRESS on `the_run/handful` and on `lean_proof_path`;
sync-back; instance down. Memory bound 6g on your own drivers, abort
`ABORT_MEMORY_LP1`; the one Lean build of the model is bounded by the
instance and its peak is pasted. Shared files this brief authorises:
none. Nothing under `Research/op_pipeline/` touched;
`riscv_reference.py` untouched. Every table row "N of M" with M the
population the loop ran over; every raw block inside 72 columns; two
lists at the end, "decided, recorded for audit" and "awaiting the owner".

## 4. Second launch, 2026-09-13 evening: the emit is rebuilt with the sail the model's own CI uses
Read first `PRIVATE/PseudoCoupHQ/DevComms/log_275_lp1_the_cached_emit_does_not_build_under_the_pinned_toolchain.md`:
the first launch found that the cached emit (sail 0.20.2's Lean
backend) does not compile under the toolchain it pins, at three sites
in `LeanIM/Defs.lean` where the backend leaked Sail call syntax
(`is_sv32_mode(k_v)`) into type abbreviations. The model's CI
(`.github/workflows/compile-lean.yml`) builds its Lean with sail
"latest", which its `sail-setup` action defines as a build from
source: `git clone https://github.com/rems-project/sail.git; opam
install sail --deps-only --yes; make install`. The newest sail release
is still 0.20.2, so the fix exists only on sail's default branch
`sail2`. The coordinator authorises, for this task only:

`lane 6`, with the network (the second and last fetch lane)
- build sail from `https://github.com/rems-project/sail.git` at commit
  `5745ea9e53` (branch `sail2`, 2026-08-26, the head before the model's
  own commit of 2026-09-09), by the model's CI recipe above, using a
  COPY of the image's opam root so it survives `down`:
  `cp -a /opt/opam /persist/opam; export OPAMROOT=/persist/opam`, then
  `opam install sail --deps-only --yes` inside the clone and
  `make install`. The hosts `.ocaml.org`, `.opam.ocaml.org` and
  `.lean-lang.org` are on the allowlist as of 23:40 tonight; a host
  still refused is a FLAG with the literal line. Paste `sail --version`
  and the build's wall time and peak resident.
`lane 7`, no network
- re-emit with that sail, the invocation of log 274 §3 verbatim, into a
  NEW cache folder whose name carries BOTH commits:
  `Research/oracle/riscv/leanpath/cache/sail-riscv_3243f93_sail_5745ea9e_I_insts_M_insts_postlude_main/`,
  with its `MANIFEST.md` in the shape of the existing one and the lane
  log beside it. 20g, about 45 minutes; wait in short calls.
`lane 8`
- `lake build` of the new emit as lane 1 did (the toolchain and
  `lean-sail` it pins; the persistent volume already holds the 4.29.0
  toolchain from the github route and a built `lean-sail` v4; if the new
  emit pins a different `lean-sail` rev, fetching it is authorised in
  this lane, and said so), the built model cached in `/persist`; paste
  wall time, peak resident, and the count of modules built "of N". A
  build error here is a FLAG with the first twelve lines LITERAL, and
  the task stops at that flag.
Then lanes 2 to 5 of §2, unchanged, over the new cache. The first
cache folder stays on disk as the record of the failure; nothing in it
is edited. Report items of §3 unchanged; the log is the next free
number.

## 5. Third launch, 2026-09-14: the pair the model's own CI last built
Read first `PRIVATE/PseudoCoupHQ/DevComms/log_276_lp1_the_re_emit_with_sail_5745ea9e_does_not_build_either.md`.
The second launch reproduced the model's own failure: the model's Lean
workflow (`compile-lean.yml`) has been RED on every run since
2026-08-27 (measured through the GitHub API on 2026-09-13; last green
run 2026-08-20T16:29Z at model commit `6266b40c1c`), so no sail can
build the Lean of the model at `3243f93`; the Lean backend at every
sail commit up to `sail2` head `dba5f0078f` prints type-level Sail
functions (`is_sv32_mode(k_v)`) as Sail syntax. The coordinator
therefore pins the LAST GREEN PAIR and authorises, for this task only:

`lane 10`, with the network (github only)
- clone `https://github.com/riscv/sail-riscv.git` at `6266b40c1c`
  (2026-08-20, the model's last commit whose Lean CI passed) into
  `/persist/sail-riscv-6266b40c`; build sail at `8eb1fb6b5b` (`sail2`
  head on that date; `/persist/sail-src` already holds the clone at a
  later commit: `git checkout 8eb1fb6b5b`, then the CI recipe
  `opam install sail --deps-only --yes; make install` with
  `OPAMROOT=/persist/opam`); paste `sail --version`. Then, in the same
  lane, `cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
  -DFIRST_PARTY_TESTS=OFF` in that clone (its configure fetches CLI11
  from github; that is why this lane has the network) so that
  `build/config/rv64d_v256_e64.json` exists for that commit. That model
  commit names the same leaf modules (`I_insts`, `M_insts`, `postlude`,
  `main`: checked); confirm with `sail --list-files` before emitting.
`lane 11`, no network
- the emit with that sail over that model, the invocation of log 274 §3
  with that clone's config, into
  `Research/oracle/riscv/leanpath/cache/sail-riscv_6266b40c_sail_8eb1fb6b_I_insts_M_insts_postlude_main/`,
  `MANIFEST.md` in the existing shape, the lane log beside it. Expect
  minutes, not 45 (the second launch measured 217 s with a from-source
  sail).
`lane 12`
- `lake build` of that emit as before, into `/persist`; the toolchain
  and `lean-sail` rev it pins are fetched only if absent from
  `/persist` (github route; said so). A build error is a FLAG with the
  first twelve lines LITERAL and the task stops there; a build that
  passes is the first measured fact of this path and its modules "of
  N" are pasted.
Then lanes 2 to 5 of §2 over that cache. The definitions of I and M at
`6266b40c1c` are what the handful is measured against; the model's
later commits change nothing in those two extensions that this task
needs (unverified; the diff of `extensions/I` and `extensions/M`
between the two commits is pasted in the log, LITERAL, as a row).
Report items of §3 unchanged; the log is the next free number.
