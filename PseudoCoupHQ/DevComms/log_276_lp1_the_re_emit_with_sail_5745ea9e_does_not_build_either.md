# log 276 — lp1, second launch: sail built from source at 5745ea9e re-emits the model in 217 s, but its Lean backend still prints the model's type-level function `is_sv32_mode(k_v)` as Sail syntax, so the build fails at the same file and the line stops at the same flag

Node: `hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/`).

Task lp1, SECOND launch (brief §4). Brief:
`PRIVATE/PseudoCoupHQ/Research/briefs/task_lp1_brief.md`.
Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, all of it. It
continues log 275
(`PRIVATE/PseudoCoupHQ/DevComms/log_275_lp1_the_cached_emit_does_not_build_under_the_pinned_toolchain.md`)
and implements log 274
(`PRIVATE/PseudoCoupHQ/DevComms/log_274_the_lean_proof_path_resistant_to_churn.md`).

Date: 2026-09-13 evening to 2026-09-14 (UTC stamps below). Instance
`lp1` (`PUBLIC/Airlock/instances/lp1.conf`, 8 cpus, 20g,
proxy on). Every lane ran on the tower guest through
`bash PUBLIC/Airlock/remote_lane.sh`; nothing but file
editing and git ran on the laptop. A lane log's host path on the tower
is `<runs>/lp1/agent/logs/<stamp>__<lane>.sh.log`
(a TOWER path), and every attribution below names its stamp. Paths
inside a pasted command are the ones the lane sees: `PseudoCoupHQ`
IS `PRIVATE/PseudoCoupHQ`; `/sources/sail-riscv` IS
`SOURCES/sail-riscv` (commit `3243f93`); `/persist` is the
instance's own volume `lp1-persist`. Every rendering is labelled
**LITERAL** (the object, quoted) or **GLOSS** (a plain reading beside a
literal). Every raw block is wrapped inside 72 columns; where a literal
line was longer, it is broken at a space with a two-space continuation
and the block says so.

THE SPELLING BAN, pasted verbatim as required:

> **THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25
> after a second violation).** No operator token may appear in ANY
> key, grouping, pairing, row structure, candidate selection, or
> comparison scope, anywhere in this line — not in matching, not in
> "which pairs get compared", not in report rows, not in dropdowns.
> The candidate set for comparison comes from machine-form evidence
> (clusters, connections, type pairs) or from ratified intention —
> never from the token. The token appears exactly once per unit: as
> a display label on the member. HISTORY OF VIOLATIONS, so the
> pattern is visible: (1) the arch campaign's cross-language matrix
> (caught by the owner 2026-08-24); (2) verdicts.py's row pairing (caught
> by the owner 2026-08-25 — the fix brief itself reintroduced it as
> "same-operator pairs"). MECHANICAL GUARD REQUIRED: every pipeline
> stage that groups or pairs units must run the spelling-key check
> (op_pipeline/check_no_spelling_keys.py) and refuse its own output
> on failure. A brief handed to any subagent for this line MUST
> paste this paragraph verbatim.

---

## 1. In plain words, before any table

The first launch (log 275) stopped because the Lean that the sail
compiler wrote for the RISC-V model does not compile: three type
abbreviations in `LeanIM/Defs.lean` carry `is_sv32_mode(k_v)`, which is
Sail's way of applying a function and not Lean's. The coordinator's
reading was that the image's sail (the 0.20.2 release) was behind the
model, because the model's own continuous integration builds its Lean
with sail "latest" — a build from the source's default branch. So this
launch was told to do what that CI does: build sail from source at the
last commit before the model's own commit, re-emit the Lean with it,
build the result, and then run the handful and pass A.

The sail build worked, in 85 seconds, by the CI's own recipe. The
re-emit worked too, and it is a different animal from the first: 217
seconds and 552 megabytes where the release took 45 minutes and 17
gigabytes for the same 91 source files. The new emit pins a newer
support library (`lean-sail` rev `v5` instead of `v4`), which was
fetched as the brief allowed. Then the build failed in the same file at
the same construct: the same three `is_sv32_mode(k_v)` lines are in the
new `Defs.lean`, character for character, plus the abbreviation
`root_level` above them that uses `k_v` without binding it. Fourteen
error lines; zero of 118 modules build. The brief says the task stops at
that flag, and it does.

Why the same failure, when the CI's recipe was followed: `is_sv32_mode`
is not an ordinary Sail function. In the model's source it is a
TYPE-LEVEL function — `type is_sv32_mode('v : Int) -> Bool = ...` — a
function that computes a boolean at the type level to size other
types, and it entered the model in `core/vmem_types.sail` at commit
`3243f93`, the very commit the image carries (2026-09-09). The sail
commit this launch built, `5745ea9e`, is from 2026-08-26. Its Lean
backend prints type-level function applications in Sail's own
spelling, `f(x)`, which Lean 4 rejects; it has no rule for them. So the
sail head as of the model commit does not lower a construct the model
commit introduced. Either the model's Lean CI was red at that commit,
or its "latest" clone happened after a sail fix; I cannot check either
without the network, so it is a flag with the literals, not a guess.

Two more things happened along the way. The proxy refused
`opam.ocaml.org` and `ocaml.org` although the coordinator added them
to the allowlist at 23:39: the `lp1-proxy` container that `up` started
at 23:44 serves the allowlist baked into the proxy image on 2026-08-22,
and the host file is pushed into a running proxy by `allow.sh`, which
runs against the proxy that exists at that moment. The refusal did not
block anything, because the copied opam root already held every
dependency the new sail wanted ("Nothing to do."). And my first emit
lane pre-made the memo-z3 path as a directory where this sail writes a
file, so that run ended with an error after writing the whole tree; it
was re-run clean, and both logs are kept beside the cache.

What was reached without a build: the module the plan names,
`Research/oracle/riscv/leanpath/leanpath/`, written in the plan's shape
(one class per sub-node, one method per leaf, under the plan's names),
with logic only where it can run today — `SailModel.definitions` and
`key_of` — and every Lean-dependent method a signature with its
refusal. Run over the new cache, it lists 29 `execute` clauses and reads
74 keys from the model's own assembly clause and `instruction`
inductive, with no typed list of mnemonics anywhere; the spelling guard
passes on the merits. The handful, the `mulh` headline, pass A, and the
per-stage Lean speed remain downstream of a build that fails, and each
is reported as unreached with its cause.

---

## 2. The lanes, in order, and what each reached

Table 1 — the lanes of this launch on instance `lp1`, every one
`state=done exit=0` at the lane level (the step-level rc is in the
"reached" column where it differs). "of" is stated where a loop ran.

| lane | tower log stamp | lane wall | reached |
|---|---|---|---|
| `lp1_l6_build_sail_from_source.sh` | `20260913T234554Z` | 85.2 s | sail built at `5745ea9e`; two hosts refused (flag 2), nothing needed from them |
| `lp1_l7_emit_with_sail_5745ea9e.sh` | `20260913T234916Z` | 216.9 s | the emit written (117 files), sail rc=2 at exit: `/work/smtcache: Is a directory` (mine; §4.3) |
| `lp1_l7b_emit_again_without_the_smtcache_directory.sh` | `20260914T000319Z` | 217.1 s | the emit, rc=0, 117 files / 63,066 lines, into the new cache |
| `lp1_l8_lake_build_of_the_new_emit.sh` | `20260914T000722Z` | 39.3 s | `lean-sail` v5 fetched and built; `LeanIM.Defs` FAILED, 14 error lines (flag 1); 0 of 118 modules |
| `lp1_l9_definitions_through_the_module.sh` | `20260914T001255Z` | 0.3 s | 29 clauses, 19 keys: the map reader missed 13 clauses (a regex of mine) |
| `lp1_l9b_definitions_through_the_module_again.sh` | `20260914T001347Z` | 0.3 s | 74 keys; the guard REFUSED the json (a per-clause list of mnemonics) |
| `lp1_l9c_definitions_through_the_module_third.sh` | `20260914T001436Z` | 0.3 s | the last constructor's operand form read; the guard still refused |
| `lp1_l9d_definitions_through_the_module_fourth.sh` | `20260914T001554Z` | 0.3 s | 29 clauses, 74 keys, guard PASS on the merits |
| `lp1_l10_verifier.sh` | `20260914T002118Z` | 0.2 s | the conventions verifier over this log: 1 DIFFERS (the wrapped §6 grep, re-run as typed) |
| `lp1_l10b_verifier_again.sh` | `20260914T002245Z` | 0.2 s | the verifier again after the log's §6 fix: 7 MATCHES, 0 DIFFERS (§9.2) |

Lane names are used once; the first launch used `lp1_l1` to `lp1_l3b`.
Every lane script is under
`PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/lanes_lp1/`
(`lp1_l6` to `lp1_l10b`) and was submitted from there. Lanes 6 and 8 fetched (the brief's two
network lanes); every other lane unset the proxy variables and says so
in its log.

---

## 3. What the second launch built and measured before the wall

### 3.1 The sail compiler from source — brief §4 lane 6

Lane `lp1_l6_build_sail_from_source.sh` (`20260913T234554Z`). The
recipe is the model's own `.github/actions/sail-setup/action.yml` for
`sail-version: "latest"`: clone, `opam install sail --deps-only --yes`,
`make install`, in a copy of the image's opam root so the result
survives `down`.

**LITERAL**, step [3/9], the copy and its relocation (the image's
`findlib.conf` names `/opt/opam` absolutely; the copy's was rewritten
to `/persist/opam` so new libraries install where they are looked up):

```
  rc=0 wall=32.0s largest-descendant peak resident=14208 kB
    2.4G	/persist/opam
  opam var prefix: /persist/opam/default
  findlib.conf AFTER relocation (LITERAL):
    destdir="/persist/opam/default/lib"
    path="/persist/opam/default/lib/ocaml:/persist/opam/default/lib"
```

**LITERAL**, step [4/9], the clone and the commit:

```
  rc=0 wall=18.3s largest-descendant peak resident=101900 kB
  5745ea9e5369ab4fc51de6f8b773dd8ebc323357 2026-08-26 14:57:51 +0100
    Lean: use more generic term for initial state
  branch containing it:   origin/HEAD -> origin/sail2   origin/sail2
```

**LITERAL**, step [5/9], the dependencies (the copied root already
satisfied every constraint of `sail.opam` at this commit):

```
[WARNING] Running as root is not recommended
Nothing to do.
  rc=0 wall=3.9s largest-descendant peak resident=400812 kB
```

**LITERAL**, steps [6/9] and [7/9], the build and the result:

```
dune build --release
(cd _build/default/src/lib && /persist/opam/default/bin/ott
  -sort false -generate_aux_rules true -o ./jib.ml
  -picky_multiple_parses true ../../language/jib.ott)
Ott version 0.34   distribution of Mon Dec 30 10:12:45 GMT 2024
dune install
  rc=0 wall=26.1s largest-descendant peak resident=1206728 kB
  make install rc=0
  which sail: /persist/opam/default/bin/sail
  sail --version: Sail 0.20.2 (HEAD @
    5745ea9e5369ab4fc51de6f8b773dd8ebc323357)
  sail --dir: /persist/opam/default/bin/../share/sail
```

(the two long lines above are broken at a space with a two-space
continuation.) **GLOSS.** The version string still says 0.20.2 because
the source's `dune-project` carries that number; the `HEAD @ 5745ea9e`
part is what tells the two apart. Every flag of log 274 §3's invocation
is in this sail's `--help` (step [8/9] checked twelve of them, all
`accepted`), and `sail --list-files` resolves the leaf modules to the
same 91 files in 0.2 s.

Wall time of the lane: 85.2 s; the largest single process 1.21 GB
(`dune build`); cgroup peak 7.17 GB (that figure is the container's
cgroup since `up`, which also counts the 5.9 GB the earlier lanes'
page cache holds; it is pasted because the brief asks for it, and it
is not the build's own resident set).

### 3.2 The re-emit — brief §4 lane 7

Lane `lp1_l7b_emit_again_without_the_smtcache_directory.sh`
(`20260914T000319Z`), the invocation of log 274 §3 verbatim, working
directory `/opt/sail-riscv-src/model`, config
`/opt/sail-riscv-src/build/config/rv64d_v256_e64.json`, leaf modules
`I_insts M_insts postlude main`. Its product is
`PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/cache/sail-riscv_3243f93_sail_5745ea9e_I_insts_M_insts_postlude_main/`
with `MANIFEST.md` in the shape of the first cache's, the lane's own
output beside it as `emit_lane.log`, and the rc=2 run's output as
`emit_lane_l7_rc2.log`.

**LITERAL**, step [3/9] and [4/9]:

```
  rc=0 wall=216.5s largest-descendant peak resident=552432 kB
  emit rc=0
  Lean files: 117; lines: 63066; bytes: 2346480
  lean-toolchain (LITERAL): leanprover/lean4:v4.29.0
  occurrences of 'is_sv32_mode(' (the first emit's leak, 3 sites in
    Defs.lean): 3
  execute clauses: 29
  execute_DIV at: /work/leanout/Lean_IM/LeanIM/InstsEnd.lean:4386
```

**LITERAL**, the new `lakefile.toml`'s require (the first cache pinned
`v4`):

```
[[require]]
name = "Sail"
git = "https://github.com/rems-project/lean-sail"
rev = "v5"
```

Table 2 — the two emits side by side, the same model commit, the same
91 source files, the same invocation.

| | sail 0.20.2 (opam), log 274 l5 | sail `5745ea9e` (source), lane 7b |
|---|---|---|
| wall | 45.5 min (2728 s) | 216.5 s |
| peak resident of the sail process | about 17 GB (log 274 §3) | 552 MB |
| Lean files / lines | 116 / 62,893 | 117 / 63,066 |
| `lean-sail` rev pinned | `v4` | `v5` |
| `is_sv32_mode(` sites in `Defs.lean` | 3 | 3 |
| `execute` clauses | 29 | 29 |

**GLOSS.** What changed in the text, read with `diff` over the 117
files on the laptop: every file differs, and the differences are the
backend's new namespacing (`namespace LeanIM` and `namespace Functions`
in place of `namespace LeanIM.Functions`; `open Sail.ConcurrencyInterfaceV1`;
`import LeanIM.LeanIM`), the renumbered type-quantifier comments
(`k_ex553288_`), and `main_of_sail_main default` in place of an explicit
state tuple (the "more generic term for initial state" the sail commit
names). The instruction clauses are the same text. The virtual-memory
abbreviations are the same text.

### 3.3 The build — brief §4 lane 8

Lane `lp1_l8_lake_build_of_the_new_emit.sh` (`20260914T000722Z`). The
working copy is `/persist/lp1/Lean_IM_5745ea9e`; the toolchain is the
4.29.0 the first launch cached under `/persist/lp1/elan` (from
github.com); the new pin `v5` differs from the first launch's built
`v4`, so this lane fetched it, as the brief authorises for this lane,
and said so.

**LITERAL**, step [2/9]:

```
  DIFFERENT rev: the new emit pins lean-sail rev 'v5' (the first
    pinned 'v4'); this lane FETCHES it with lake update from
    github.com (authorised by brief §4 for this lane, and said so
    here); http_proxy=http://lp1-proxy:3128
info: Sail: cloning https://github.com/rems-project/lean-sail
info: Sail: checking out revision
  '079463134b9c50450b8393e1566a09fc492a34d9'
info: toolchain not updated; already up-to-date
  rc=0 wall=0.9s largest-descendant peak resident=106792 kB
  079463134b9c50450b8393e1566a09fc492a34d9 2026-07-20 16:26:29 +0200
    Add support for archsem (#10)
    lean-toolchain: leanprover/lean4:v4.29.0
```

**LITERAL**, step [4/9], the library builds:

```
✔ [9/10] Built Sail (885ms)
Build completed successfully (10 jobs).
  rc=0 wall=7.4s largest-descendant peak resident=1495620 kB
```

**LITERAL**, step [5/9], the model's first module does not — the
fourteen error lines' first twelve, exactly as the lane printed them
(line-numbered by the lane's `grep -n`; the two longest broken at a
space with a two-space continuation):

```
3:error: LeanIM/Defs.lean:621:8: Unknown identifier `k_v`
4:error: LeanIM/Defs.lean:621:19: Unknown identifier `k_v`
5:error: LeanIM/Defs.lean:621:55: Unknown identifier `k_v`
6:error: LeanIM/Defs.lean:621:66: Unknown identifier `k_v`
7:error: LeanIM/Defs.lean:621:102: Unknown identifier `k_v`
8:error: LeanIM/Defs.lean:622:9: Unknown identifier `k_v`
9:error: LeanIM/Defs.lean:626:54: unexpected token '(';
  expected ')', ',' or ':'
10:error: LeanIM/Defs.lean:628:49: unexpected token '(';
  expected ')', ',' or ':'
11:error: LeanIM/Defs.lean:630:49: unexpected token '(';
  expected ')', ',' or ':'
12:error: LeanIM/Defs.lean:1181:9: Function expected at
21:error: LeanIM/Defs.lean:1182:9: Function expected at
30:error: LeanIM/Defs.lean:1189:35: Unknown identifier `PTW_Output`
```

```
  rc=1 wall=30.2s largest-descendant peak resident=1924208 kB
  LeanIM.Defs rc=1; error lines: 14
  modules built: 0 of 118 (LeanIM/*.lean plus LeanIM.lean)
```

count: 14 `error` lines from `lake build LeanIM.Defs`; `LeanIM.Defs`
is imported by every model module, so 0 of 118 modules build. This is
the flag the task stops at (§4.1).

### 3.4 The definitions, through the module — brief §2 lane 2, §3 item 1

Lane `lp1_l9d_definitions_through_the_module_fourth.sh`
(`20260914T001554Z`); artifact
`PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/lp1_definitions_sail_5745ea9e.json`;
peak resident 22,716 kB (bound 6 GB, abort `ABORT_MEMORY_LP1`, never
raised); the reader runs in 0.3 s.

`SailModel.definitions` reads the emitted Lean to LIST the `execute`
clauses; `key_of` reads each clause's key from the model's own
`assembly_forwards` clause (the literal parts before the first
`spc_forwards ()`, and the `*_forwards` maps those parts call, expanded
to the strings the maps' own clauses give) and the operand form from
the `instruction` inductive's tuple; the width is 64 (`xlen` as
instantiated) unless the clause writes a 32-bit value sign-extended
into the register. No list of mnemonics is typed anywhere; the first
launch's lane `lp1_l2b` had typed the M-family and W-family mnemonics
by hand, and this reader retires that.

Table 3 — `execute` clauses in the new emit, by extension (the
extension is the folder of the `.sail` file under
`/sources/sail-riscv/model` that carries `function clause execute
<NAME>`). **LITERAL** (lane step [2/6]).

| extension | clauses | of 29 |
|---|---|---|
| I | 20 | 29 |
| M | 6 | 29 |
| cfi (`LPAD`) | 1 | 29 |
| postlude (`C_ILLEGAL`, `ILLEGAL`) | 2 | 29 |

Table 4 — the keys as `key_of` reads them, ten of 74, in the order the
lane printed them. **LITERAL** (lane step [2/6]).

| mnem | operand form | width | from clause | of 74 |
|---|---|---|---|---|
| wfi | (none) | 64 | execute_WFI | 74 |
| auipc | imm20 reg | 64 | execute_UTYPE | 74 |
| lui | imm20 reg | 64 | execute_UTYPE | 74 |
| sb | imm12 reg reg | 64 | execute_STORE | 74 |
| sd | imm12 reg reg | 64 | execute_STORE | 74 |
| sh | imm12 reg reg | 64 | execute_STORE | 74 |
| sw | imm12 reg reg | 64 | execute_STORE | 74 |
| sret | (none) | 64 | execute_SRET | 74 |
| slliw | imm5 reg reg | 32 | execute_SHIFTIWOP | 74 |
| sraiw | imm5 reg reg | 32 | execute_SHIFTIWOP | 74 |

Table 5 — the 74 keys by width and by operand form (read from the
artifact on the laptop with python's `json`; the guard's exempt field
`mnem` holds the mnemonic). **LITERAL** counts.

| width | keys | of 74 |
|---|---|---|
| 64 | 60 | 74 |
| 32 | 14 | 74 |

| operand form | keys | of 74 |
|---|---|---|
| reg reg reg | 28 | 74 |
| imm12 reg reg | 20 | 74 |
| (none) | 9 | 74 |
| imm13 reg reg | 6 | 74 |
| imm5 reg reg | 3 | 74 |
| imm6 reg reg | 3 | 74 |
| imm20 reg | 2 | 74 |
| reg reg | 1 | 74 |
| imm21 reg | 1 | 74 |
| imm4 imm4 imm4 reg reg | 1 | 74 |

**GLOSS.** 74 against the first launch's 49: the first launch typed
keys only for the arithmetic families; this reader takes every clause
the assembly clause spells, so the loads, stores, branches, jumps,
fences and system instructions are keys too. One reading to record: the
`LOAD` clause's mnemonic is the free product `"l"` × width map × `maybe_u`,
which yields `ldu` beside `lb lbu lh lhu lw lwu ld`; the encoder never
produces `ldu`, and pruning the free product by the model's own
`encdec` is a later step of `key_of`, not done here. Every clause read
at least one key (the lane's "clauses with no key: []").

### 3.5 `strip` on DIV and on the MUL family — RAW, and why RAW again

`strip`'s own output needs Lean to elaborate the model (§3.3 fails), so
what follows is the RAW clause as this sail wrote it, quoted from the
new cache. **LITERAL**,
`…/cache/sail-riscv_3243f93_sail_5745ea9e_I_insts_M_insts_postlude_main/LeanIM/InstsEnd.lean:4386`,
the quotient logic (the reads and the write around it are the lines
`let rs1_bits ← do (rX_bits rs1)`, the `rs2` read, and
`(wX_bits rd (to_bits_truncate (l := 64) quotient))`):

```
  let quotient :=
    if ((rs2_int == 0) : Bool)
    then (Neg.neg 1)
    else (Int.tdiv rs1_int rs2_int)
  let quotient :=
    if (((not is_unsigned) && (quotient ≥b (2 ^i (xlen -i 1)))) :
        Bool)
    then (Neg.neg (2 ^i (xlen -i 1)))
    else quotient
  (wX_bits rd (to_bits_truncate (l := 64) quotient))
```

**LITERAL**, `…/LeanIM/Arithmetic.lean`, the helper `execute_MUL`
calls (`mult_to_bits_half (l := xlen) mul_op.signed_rs1
mul_op.signed_rs2 rs1_bits rs2_bits mul_op.result_part`):

```
  let result_wide :=
    (to_bits_truncate (l := (2 *i l)) (rs1_int *i rs2_int))
  match result_part with
  | .High => (Sail.BitVec.extractLsb result_wide ((2 *i l) -i 1) l)
  | .Low => (Sail.BitVec.extractLsb result_wide (l -i 1) 0)
```

**GLOSS.** Identical to the first emit's text (log 275 §3.1): the new
backend changed nothing in the instruction clauses.

---

## 4. The flags for the coordinator, each LITERAL

### 4.1 FLAG 1 — the blocker: the re-emit with sail `5745ea9e` does not build either, and the construct is a type-level function the model commit itself introduced

The first twelve error lines are in §3.3. The cause, in the emitted
text. **LITERAL**, the new
`…/cache/sail-riscv_3243f93_sail_5745ea9e_I_insts_M_insts_postlude_main/LeanIM/Defs.lean`
lines 620 to 630 (the `root_level` line is broken at a space with a
two-space continuation; the three abbrevs are whole lines):

```
abbrev root_level : Int :=
  (if ( k_v = 32 ∨ k_v = 34  : Bool) then 1 else (if ( k_v = 39 ∨
  k_v = 41  : Bool) then 2 else (if ( k_v
  = 48 ∨ k_v = 50  : Bool) then 3 else 4)))

abbrev level_range (k_v : Nat) := Nat

abbrev vpn_level_size : Int := (12 - if ( is_sv32_mode(k_v)  : Bool)
  then 2 else 3)

abbrev pte_bits k_v := (BitVec (if ( is_sv32_mode(k_v)  : Bool)
  then 32 else 64))

abbrev ppn_bits k_v := (BitVec (if ( is_sv32_mode(k_v)  : Bool)
  then 22 else 44))
```

The cause, in the model's source. **LITERAL**,
`/sources/sail-riscv/model/core/vmem_types.sail` (commit `3243f93`),
lines 13, 38, 44 and 47 (line 38 broken at a space with a two-space
continuation):

```
type is_sv32_mode('v : Int) -> Bool = 'v == 32 | 'v == 34
type vpn_level_size('v : Int), is_sv_or_svx4_mode('v) =
  pagesize_bits - (if is_sv32_mode('v) then 2 else 3)
type pte_bits('v), is_sv_or_svx4_mode('v) =
  bits(if is_sv32_mode('v) then 32 else 64)
type ppn_bits('v), is_sv_or_svx4_mode('v) =
  bits(if is_sv32_mode('v) then 22 else 44)
```

**GLOSS.** `type is_sv32_mode('v : Int) -> Bool` declares a function
at the TYPE level: it takes a type-level integer and gives a type-level
boolean, and the model uses it to choose the width of `pte_bits` and
`ppn_bits`. The Lean backend at `5745ea9e` writes `is_sv32_mode(k_v)`
into Lean exactly as Sail spells an application, `f(x)`; Lean 4's
application is `f x` and it reads `f(x)` as `f` followed by a stray
`(`, which is the `unexpected token '('` above. `root_level` and
`vpn_level_size` lose their parameter altogether (`k_v` free). These
abbreviations are the virtual-memory page-table types, required by
`PTW_Output` (line 1181, `Function expected` — `pte_bits` and
`ppn_bits` never got defined) and so by every module.

The file is NEW at the model commit: **LITERAL**, on the laptop,
`git -C SOURCES/sail-riscv show 3243f93 --stat` lists
`model/core/vmem_types.sail | 164 +` as an added file (that clone is a
single-commit snapshot, so nothing older is in it to compare). So the
construct entered the model at the commit the image carries
(2026-09-09), and the sail commit the brief names is from 2026-08-26.

Why this is a stop-line and not a workaround, again:

- the emit is a build product; a file under
  `Research/oracle/riscv/leanpath/cache/` is never edited (brief and
  launch). Hand-fixing the abbreviations would be a per-model hand edit.
- the brief §4 lane 8 says a build error here is a FLAG and the task
  stops at it.
- the model's own Lean CI recipe was followed exactly (`sail-setup`
  with `sail-version: "latest"`: clone, `opam install sail --deps-only
  --yes`, `make install`; then `lake update`, `lake build`). With the
  sail head as of the model commit, the CI's own recipe reproduces the
  failure. Whether the CI was red at `3243f93`, or a later sail commit
  lowers type-level functions, needs the network to see and is the
  coordinator's to check.

What would clear it, each mechanical and nameable, none decided here:

- a sail commit AFTER 2026-09-09 whose Lean backend lowers type-level
  function applications (if such a commit exists on `sail2`);
- a model commit BEFORE `vmem_types.sail` introduced `is_sv32_mode`
  (the emit cache is keyed by model commit, so that is a different
  `/sources` checkout, not a hand edit; it also moves the definitions
  to an older model text);
- upstream's fix, when it lands.

### 4.2 FLAG 2 — the `lp1-proxy` container serves the allowlist baked into the proxy image, not the tower's edited `proxy/allowlist.txt`

The coordinator added `.lean-lang.org`, `.ocaml.org` and
`.opam.ocaml.org` to `Airlock/proxy/allowlist.txt` on the
tower at 23:39 and reloaded the proxy. Lane 6's sample request to each
host it might need, **LITERAL** (step [2/9], `20260913T234554Z`):

```
  --- https://github.com/rems-project/sail.git/info/refs?...
      HTTP 405 in 0.128005s
  --- https://opam.ocaml.org/index.tar.gz
  curl: (7) CONNECT tunnel failed, response 403
      HTTP 000 in 0.001208s
  --- https://ocaml.org/
  curl: (7) CONNECT tunnel failed, response 403
      HTTP 000 in 0.001082s
```

(the github URL is shortened with `...` here; the lane has it whole.)
**LITERAL**, the proxy's own log (`podman logs lp1-proxy` on the tower,
read over ssh — not a lane; a read):

```
1789343155.227      0 10.89.38.5 TCP_DENIED/403 3354 CONNECT
  opam.ocaml.org:443 - HIER_NONE/- text/html
1789343155.237      0 10.89.38.5 TCP_DENIED/403 3344 CONNECT
  ocaml.org:443 - HIER_NONE/- text/html
```

count: 2 hosts refused, one CONNECT each (the lane asked once each).

The mechanism, **LITERAL**, on the tower: inside the container,
`/etc/squid/allowlist.txt` is 832 bytes, 39 lines, dated `Aug 22
18:45`, and `grep -n "ocaml\|lean-lang"` over it finds nothing; the
host's `Programming/Airlock/proxy/allowlist.txt` is 874 bytes, dated
`Sep 13 23:39`, and carries the three lines (46 to 48). The proxy image
bakes the file (`Programming/Airlock/proxy/Containerfile.proxy:17`:
`COPY proxy/allowlist.txt /etc/squid/allowlist.txt`), and `allow.sh`
pushes the host file into a RUNNING proxy (`podman cp` then
`squid -k reconfigure`). The `lp1-proxy` this launch's `up` started at
23:44 came from the image, after the 23:39 push. The push is the
coordinator's: `./allow.sh --instance lp1 sync` on the tower, after
`up`. Not worked around.

It did not block: `opam install --deps-only` answered "Nothing to
do." (§3.1) because the copied opam root already held every dependency
at a satisfying version, and the clone came from github.com, which is
in both files. `release.lean-lang.org` (log 275 flag 1) was not needed
either: the 4.29.0 toolchain was already cached from the github route.

### 4.3 Recorded, minor

- Lane `lp1_l7` pre-made `/work/smtcache` as a directory (a `mkdir` of
  mine, not in the verbatim invocation); this sail writes its
  `--memo-z3-path` as a FILE and ended `rc=2` with
  `Fatal error: exception Sys_error("/work/smtcache: Is a directory")`
  AFTER writing the whole tree (same 117 files / 63,066 lines). Lane
  `lp1_l7b` made no such directory and ended `rc=0`; its product is the
  cache, and lane 7's output is kept beside it as
  `emit_lane_l7_rc2.log`.
- Lane `lp1_l8` copied the first launch's `lake build -j 4` for its
  later steps; lake 5.0.0 answers `error: unknown short option '-j'`.
  No information was lost: `LeanIM.Defs` had already failed and every
  module imports it. A future build lane spells it `--jobs=4` or omits
  it.
- Lane `lp1_l9`'s reader missed every map whose `def` line ends in
  `: String :=` (13 of 29 clauses read no key); lane `lp1_l9c` read the
  `instruction` inductive's last constructor; lane `lp1_l9b`/`9c`'s json
  carried a per-clause LIST of mnemonics, which the guard read as bare
  operator tokens (`and`, `or`, `xor`) in a row structure — the guard was
  right, and lane `lp1_l9d`'s json carries the count instead, every
  mnemonic being one key row in the exempt field `mnem`. Four lanes for
  one listing; each kept.
- The cgroup `memory.peak` printed by every lane (7.17 GB) is the
  container's since `up` and includes page cache; the per-process
  peaks are the resident figures pasted beside each step.

---

## 5. The handful, pass A, and the speed — brief §3 items 2, 3, 4

None of these could run: they need the model built as a Lean library
(`meaning` composes Sail's `execute` and unfolds it with `simp`;
`equals` builds theorems Lean's kernel checks). The build is flag 1,
and brief §4 stops the task there. Nothing here is estimated or faked.

Table 6 — the handful, brief §3 item 2: the ten of rv1 (log 258) plus
`mulh` on c, eleven rows to run. Reached: 0 of 11.

| unit | stage reached | cause |
|---|---|---|
| the ten of rv1 (log 258 §3) | not started | BLOCKED by flag 1: no built model to compose `meaning` in, no kernel to check `equals` |
| `mulh` on c (the headline) | not started | same; the integer-level `grind` test of log 274 §5.3 is unmeasured |

Table 7 — pass A over the rv6 corpus, brief §3 item 3 (the population:
255 RISC-V cells on c, c++, rust, go; the sources under
`Research/oracle/cross_construction/emulation/construct/general/emulations_riscv64/`,
1,960 files, 490 per language). Reached: 0 of 255 per language.

| language | dictionary entries proved | swap table size | of 255 |
|---|---|---|---|
| c | not started | not started | 255 |
| c++ | not started | not started | 255 |
| rust | not started | not started | 255 |
| go | not started | not started | 255 |

(For reference, the z3-gate line stands at c 243, c++ 243, rust 247,
go 243 of 255 on some route; 251 on some language; 235 on all four —
log 273 §6.2.)

Table 8 — speed measured, brief §3 item 4, beside log 274 §7.1's
expectations. Only the steps that do not need the built model are
measured; the emit's figure is the launch's one new number.

| step | expected (log 274 §7.1) | measured here | of |
|---|---|---|---|
| sail from source at `5745ea9e` | not expected | 85.2 s lane; `make install` 26.1 s, peak 1.21 GB | 1 build |
| `definitions()` emit | 45 min, 17 GB, once/commit (sail 0.20.2) | 216.5 s, peak 552 MB (this sail) | 117 files / 63,066 lines |
| `lean-sail` v5 fetch + build | plumbing | 0.9 s + 7.4 s, peak 1.50 GB | 10 jobs |
| `lake build LeanIM.Defs` | plumbing | FAILED at 30.2 s, peak 1.92 GB | 0 of 118 modules |
| definitions listing (module) | seconds | 0.3 s, peak 22.7 MB | 29 clauses / 74 keys |
| `meaning` per unit | seconds expected | UNMEASURED | BLOCKED by flag 1 |
| `equals` integer level / bv_decide | under 1 s expected | UNMEASURED | BLOCKED by flag 1 |
| `equals` on `mulh` at integer level | the headline | UNMEASURED | BLOCKED by flag 1 |
| pass A over 255 × 4 | ~1 hour expected | UNMEASURED | BLOCKED by flag 1 |

The `speed_measured` node's PROGRESS carries this table.

---

## 6. The churn statement — brief §3 item 5

**What in this module names an opcode: nothing.** **LITERAL**, the
grep over every file this task added — the module and EVERY lane under
`lanes_lp1/` (both launches) — for any control construct followed on
its line by a quoted opcode spelling, counting the files that match
(run from the instance; the command is one line, past 72 columns, for
the reason §9.1 states):

```
$ grep -rlP '\b(if|elif|case|when|match)\b.*[\x27"](add|sub|mul|mulh|mulhu|mulhsu|div|divu|rem|remu|sll|srl|sra|and|or|xor|slt|sltu)[\x27"]' PseudoCoupHQ/Research/oracle/riscv/leanpath/leanpath PseudoCoupHQ/Research/oracle/riscv/leanpath/lanes_lp1 | wc -l
0
```

**GLOSS.** Zero files, of the ten module files and the nineteen lane
scripts, carry a branch, case or match keyed on an opcode spelling.
The only places a mnemonic appears are the
exempt `mnem` field of a key the module READ from the model's own
`assembly_forwards`, and the display columns of this log. The
mechanical proof is the guard's verdict on the one json this launch
wrote. **LITERAL**, lane `lp1_l9d` step [5/6]:

```
    operator inventory: 91 tokens read from probe_manifest_*.json
    PASS lp1_definitions_sail_5745ea9e.json -- no operator token in
      any key, grouping, pairing or row structure
  guard rc=0
```

`grep -c exempt` over the files this launch ADDED (lane `lp1_l9d`
step [6/6]): 0 on the json and on lanes 6, 7, 7b, 8, and on eight of
the ten module files; 1 each on `leanpath/__init__.py` and
`leanpath/arch_opcode.py`, where the word is in the sentence that says
the mnemonic sits in "the field `mnem` the guard exempts as machine
form" (the ban's own ruling of 2026-09-08, restated, not a `role:
exempt` marker; the guard walked the json on the merits); 3 on each of
the lanes `lp1_l9*.sh`, which RUN the guard and carry the word inside
the command and its caption, exactly as rv1, rv9 and log 275 reported.

**What happens on a new model commit:** the cache key is the model
commit and the sail commit (both in the folder name), so a new commit
misses the cache and the emit lane re-runs — in 217 s with this sail,
where the first launch expected 45 minutes. Nobody writes anything. And
THIS launch is the measured instance of the other half of that
sentence: the model commit `3243f93` introduced a construct
(`is_sv32_mode`, a type-level function) that the sail head as of the
same day does not lower, so the regenerated product fails loudly at its
first module rather than drifting. The repair is a version choice,
named in §4.1, not an edit.

**What happens on a new compiler release:** pass A re-proves; each
language's units are re-lifted by `meaning` and re-checked by `equals`;
`operator_for` is refilled by proof. Unverified here (downstream of the
build).

---

## 7. The module, written in the plan's shape

`PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/leanpath/`,
ten files, 717 lines: one class per `code (class)` sub-node, one method
per `code (method)` leaf, under the plan's names (`plan_and_code.md`
§1); written top-down with logic last (§2): a method carries logic only
where it can be reviewed by running it, and every other method is its
signature, the leaf's steps as its docstring, and a named refusal.

Table 9 — the classes and what each carries today.

| class (file) | methods | logic today | refusal otherwise |
|---|---|---|---|
| `SailModel` (`sail_model.py`) | `definitions`, `key_of`, `strip` | `definitions`, `key_of`: the text listing of §3.4 | `strip`: `AWAITS_BUILT_MODEL` |
| `ArchOpcode` (`arch_opcode.py`) | `as_row` | the key row (`mnem`, `operand_form`, `width`, `from_clause`) | — |
| `LeanExpr` (`lean_expr.py`) | `equals`, `widen`, `normalize_integer_level`, `decide_fixed_width`, `primitives` | none | `AWAITS_BUILT_MODEL` with the stage |
| `ArchUnit` (`arch_unit.py`) | `meaning`, `decode`, `compose`, `branch_rule`, `memory_and_calls` | none | `AWAITS_BUILT_MODEL` |
| `Language` (`language.py`) | `compile`, `render`, `compose_at_width`; attribute `operator_for` | none (`compile`'s command lines are in its docstring, from the brief) | `NOT_RUN_YET` / `AWAITS_BUILT_MODEL` |
| `Emulation`, `Dictionary` (`emulation.py`, `dictionary.py`) | `add`, `find`, `report` | the table shape | — |
| `System` (`system.py`) | `run`, `pass_a_find`, `pass_b_build`, `pass_c_units_across_languages` | none | `AWAITS_BUILT_MODEL`; pass C `OUT_OF_SCOPE_FOR_LP1` (brief §1) |

`python3 -m leanpath definitions <LeanIM dir> <model source> <out.json>`
is the entry lane 9d ran. Methods do not take the instance
(`plan_and_code.md` §7): every one is a `@staticmethod` over its
inputs.

Why the Lean-dependent methods carry no logic, restated from log 275
§8 and unchanged by this launch: each is defined only in terms of a
built model, and logic written against a foundation that does not
stand would be unrunnable and unreviewed. What this launch settled
about their shape, for the next one, from lane 8's reading of the
support library (`lean-sail` v5): the state is
`SequentialState RegisterType trivialChoiceSource` with an `Inhabited`
instance (`ConcurrencyInterfaceV1.lean:338`), `readReg`/`writeReg` at
`ConcurrencyInterfaceV1.lean:173/169`, the emitted decoder
`encdec_backwards : BitVec 32 → SailM instruction` is monadic (its
guards read `misa` through `currentlyEnabled`), and `rX_bits (Regidx
i)` dispatches on `BitVec.toNatInt i` to `readReg x<i>`. Recorded, not
decided.

---

## 8. The guard, the counts, the verifier

- The spelling guard passed on the merits over
  `lp1_definitions_sail_5745ea9e.json` (§6, LITERAL), after refusing two
  earlier shapes of it (§4.3). `check_no_spelling_keys.py` was not
  modified.
- `grep -c exempt` = 0 on the deliverable json (§6).
- The conventions verifier over this log: §9 (final lane).
- Nothing under `Research/op_pipeline/` was touched;
  `riscv_reference.py` was not touched; no file under either cache
  folder was edited by hand (lane 7b regenerated the second cache's
  product after lane 7's rc=2 run; the first cache is untouched).
  Nothing under `PUBLIC/Airlock/` or `<runs>/` was
  deleted, on either machine. The idle `sl1-runner` container was not
  touched. No host venv, no host compile.
- Shared files: none changed. The four PROGRESS files the launch names
  carry one dated entry each.

---

## 9. The verifier's tally, and the claims that reproduce

### 9.1 The load-bearing claims, each with the command that reproduces it

Each block is a transcript re-run inside the `lp1` instance, where this
repository is mounted at `PseudoCoupHQ` and the model source
at `/sources/sail-riscv`. These command lines, and the one in §6, are
the one exception to the 72-column wrap of this log's raw blocks: the
verifier re-runs each `$` line exactly as typed, and a command broken
over two lines is not the command (the first verifier pass scored the
wrapped §6 grep DIFFERS for exactly that reason); the cache folder's
name, set by the brief, is most of the width.

the leak is in the new emit, 3 sites (§3.2, §4.1):

```
$ grep -c 'is_sv32_mode(' PseudoCoupHQ/Research/oracle/riscv/leanpath/cache/sail-riscv_3243f93_sail_5745ea9e_I_insts_M_insts_postlude_main/LeanIM/Defs.lean
3
```

the construct in the model source is a type-level function (§4.1):

```
$ sed -n 13p /sources/sail-riscv/model/core/vmem_types.sail
type is_sv32_mode('v : Int) -> Bool = 'v == 32 | 'v == 34
```

the new emit pins `lean-sail` v5, the first v4 (§3.2):

```
$ grep rev PseudoCoupHQ/Research/oracle/riscv/leanpath/cache/sail-riscv_3243f93_sail_5745ea9e_I_insts_M_insts_postlude_main/lakefile.toml
rev = "v5"
```

```
$ grep rev PseudoCoupHQ/Research/oracle/riscv/leanpath/cache/sail-riscv_3243f93_I_insts_M_insts_postlude_main/lakefile.toml
rev = "v4"
```

29 clauses and 74 keys in the artifact (§3.4):

```
$ python3 -c "import json; d=json.load(open('PseudoCoupHQ/Research/oracle/riscv/leanpath/lp1_definitions_sail_5745ea9e.json')); print(d['clause_count'], d['key_count'])"
29 74
```

the spelling guard passes on the merits over the one json (§6):

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/riscv/leanpath/lp1_definitions_sail_5745ea9e.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS lp1_definitions_sail_5745ea9e.json -- no operator token in any key, grouping, pairing or row structure
```

the 117 Lean files of the new cache (§3.2):

```
$ python3 -c "import os; print(len([f for f in os.listdir('PseudoCoupHQ/Research/oracle/riscv/leanpath/cache/sail-riscv_3243f93_sail_5745ea9e_I_insts_M_insts_postlude_main/LeanIM') if f.endswith('.lean')]))"
117
```

### 9.2 The tally

Lane `lp1_l10_verifier.sh`, verifier
`check_conventions_log_claims.py --verify --timeout 20` over this log,
from the instance. The tally is pasted below as the lane printed it.

Two passes. The first, lane `lp1_l10_verifier.sh` (tower log stamp
`20260914T002118Z`), scored ONE claim DIFFERS: the §6 grep, wrapped
over lines for the 72-column rule, which the verifier re-ran as typed
(`grep: Unmatched ( or \(`). The log was fixed (the grep became one
line; §9.1's exception sentence), never the verifier, and lane
`lp1_l10b_verifier_again.sh` (`20260914T002245Z`) scored it again.
**LITERAL**, the second pass's summary:

```
population: 27 claims across 1 logs
  MATCHES          7
  DIFFERS          0
  UNVERIFIABLE     19
  REFUSED          0
  NOT_RERUNNABLE   1

ONE LINE: 7 of 27 claims reproduce; 19 (70%) carry nothing to re-run

causes, by name:
  attribution_only                 16
  prose_only                       2
  pasted_without_source            1
  output_annotated                 1
```

| outcome | claims |
|---|---|
| MATCHES | 7 |
| **DIFFERS** | **0** |
| UNVERIFIABLE | 19 |
| REFUSED | 0 |
| NOT_RERUNNABLE | 1 |
| population | 27 claims across 1 log |

Zero DIFFERS. The seven that reproduce are the six commands of §9.1
and the §6 grep. The 19 UNVERIFIABLE are LITERAL attributions to lane
logs (the record) and prose, none carrying an embedded `$ ` command —
the same shape logs 258 and 275 carried. The one NOT_RERUNNABLE is the
laptop-side `git show --stat` of §4.1 (`out_of_sandbox`). The verifier
was not modified.

---

## 10. Flag summary (LITERAL), for the coordinator

1. **FLAG 1 — the blocker, again.** The emit with sail built from
   source at `5745ea9e53` (the model's own CI recipe) still prints
   `is_sv32_mode(k_v)` at `LeanIM/Defs.lean:626, 628, 630` and leaves
   `k_v` unbound at 621 to 622; `lake build LeanIM.Defs` fails with 14
   error lines (the first twelve in §3.3), 0 of 118 modules build. The
   construct is `type is_sv32_mode('v : Int) -> Bool` in
   `model/core/vmem_types.sail`, a file the model commit `3243f93`
   (2026-09-09) added; the sail commit (2026-08-26) has no lowering for
   type-level function applications. The task stops here (brief §4).
   Coordinator: a sail commit after 2026-09-09 that lowers them, or a
   model commit before the file entered, or wait for upstream.

2. **FLAG 2 — the proxy's allowlist.** The `lp1-proxy` container serves
   the allowlist baked into the proxy image (2026-08-22, 39 lines,
   without the three hosts); the tower's `proxy/allowlist.txt` (23:39,
   with them) reaches a proxy only through `allow.sh` against the
   RUNNING proxy, and this launch's `up` started a fresh one at 23:44.
   `TCP_DENIED/403 CONNECT opam.ocaml.org:443` and `ocaml.org:443`.
   Nothing needed them this time ("Nothing to do."). Coordinator:
   `./allow.sh --instance lp1 sync` after the next `up`.

3. **Recorded, minor.** Lane 7's rc=2 from my `mkdir` of the memo-z3
   path (re-run clean as 7b, both logs kept); lake 5.0.0 refuses
   `-j 4`; four lanes for one listing (§4.3).

---

## 11. Two lists

### Decided, recorded for audit

- The sail compiler at `5745ea9e53` is built and cached at
  `/persist/opam/default/bin/sail` (a copy of the image's opam root,
  relocated: `findlib.conf` rewritten to `/persist/opam`), clone at
  `/persist/sail-src`; 85 s by the CI recipe; no fetch beyond github.com
  was needed.
- The second emit is cached at
  `Research/oracle/riscv/leanpath/cache/sail-riscv_3243f93_sail_5745ea9e_I_insts_M_insts_postlude_main/`
  with `MANIFEST.md`, `emit_lane.log` (rc=0) and `emit_lane_l7_rc2.log`
  (the rc=2 run); the first cache is untouched. The emit with this sail
  costs 217 s and 552 MB, not 45 min and 17 GB.
- `lean-sail` v5 (commit `0794631`) is fetched and built under
  `/persist/lp1/Lean_IM_5745ea9e/.lake`, beside the first launch's v4;
  the 4.29.0 toolchain under `/persist/lp1/elan` served both.
- The module `Research/oracle/riscv/leanpath/leanpath/` exists in the
  plan's shape (§7); `SailModel.definitions` and `key_of` run and read
  74 keys from the model's own assembly clause with no typed mnemonic
  list; guard PASS; artifact `lp1_definitions_sail_5745ea9e.json`.
- Lane scripts are kept under `Research/oracle/riscv/leanpath/lanes_lp1/`
  (`lp1_l6` to `lp1_l10`), submitted from there; nothing deleted; the
  `sl1-runner` container left alone.
- The free-product reading of `LOAD`'s mnemonic (`ldu` beside `ld`) is
  recorded in §3.4 as a later refinement of `key_of` by the model's own
  encoder, not done here.

### Awaiting the owner

- **The blocker (flag 1) is the coordinator's to clear:** which sail
  commit, or which model commit, the next emit uses; until then the
  Lean proof path is stopped at its foundation, by design, and the
  handful, `mulh`, pass A and the per-stage speed stay unmeasured.
- **The proxy allowlist (flag 2):** the push into the `lp1-proxy` after
  `up`, so a later lane that does need `opam.ocaml.org` is not refused.
