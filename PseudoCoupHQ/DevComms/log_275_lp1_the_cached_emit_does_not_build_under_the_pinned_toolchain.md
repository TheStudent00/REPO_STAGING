# log 275 — lp1: the Lean proof path, the handful — the cached emit does not build under the toolchain it pins, so the line is blocked at its foundation and flagged for the coordinator

Node: `hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/`).

Task lp1. Brief:
`PRIVATE/PseudoCoupHQ/Research/briefs/task_lp1_brief.md`.
Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, all of it.
It implements log 274
(`PRIVATE/PseudoCoupHQ/DevComms/log_274_the_lean_proof_path_resistant_to_churn.md`).

Date: 2026-09-13. Instance `lp1`
(`PUBLIC/Airlock/instances/lp1.conf`). Every lane ran on
the tower guest through
`bash PUBLIC/Airlock/remote_lane.sh`; nothing but file
editing and git ran on the laptop. A lane log's host path on the tower
is
`<runs>/lp1/agent/logs/<stamp>__<lane>.sh.log`,
and every attribution below names its file. Paths inside a pasted
command are the ones the lane sees: `PseudoCoupHQ` IS
`PRIVATE/PseudoCoupHQ`. Every rendering is labelled
**LITERAL** (the object, quoted) or **GLOSS** (a plain reading beside a
literal).

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

The Lean proof path takes the RISC-V model's own Lean — what the sail
compiler's Lean backend writes for each instruction — as the definition
of every arch-opcode, lifts each compiled unit's meaning by composing
that same Lean, and asks Lean's kernel to prove the two equal. The
whole line therefore stands on one thing being true: the model's Lean,
as cached on disk, must build under the toolchain and support library
it pins. This task's first lane was to build it once, and then the
handful (ten units, `mulh` on c among them) and pass A would follow.

It does not build. The cached emit at
`Research/oracle/riscv/leanpath/cache/sail-riscv_3243f93_I_insts_M_insts_postlude_main/`
was produced by the image's sail 0.20.2. Its `lakefile.toml` pins the
Lean toolchain `leanprover/lean4:v4.29.0` and requires `lean-sail` rev
`v4`. I installed exactly that toolchain and fetched exactly that
library; the library itself builds in six seconds. But the first
module of the model, `LeanIM/Defs.lean`, fails to compile with twelve
errors, and the cause is in the emitted text itself: sail 0.20.2's Lean
backend wrote Sail function-call syntax — `is_sv32_mode(k_v)` — inside a
Lean type abbreviation, and left the type variable `k_v` unbound. Those
are the virtual-memory page-table type abbreviations in the model's
`core`, which everything else imports, so nothing downstream compiles.

This is not a module-selection problem and not something a re-emit with
the same sail would change: the emit is deterministic and the sail that
made it is the version the model pins for its C build
(`cmake/sail_required_version.txt` is `0.20.2`, and the image carries
0.20.2). What is different is that the RISC-V model's own continuous
integration builds its Lean with sail `"latest"`, not with 0.20.2 — the
Lean backend has moved on since the pinned release, and 0.20.2's Lean
backend emits Lean this model commit's virtual-memory types can no
longer be expressed in. Fixing it means re-emitting with a newer sail,
which is a fetch/install outside the one lane the brief gives a network
to, and therefore a stop-line for the coordinator, not something this
task works around.

So this log carries: the one measurement that needs no build — the
definitions, listed and keyed straight from the emitted text, which is
what `SailModel.definitions` reads before it ever calls Lean — and two
flags with their literal output and counts. The handful's ten rows, the
`mulh` headline, pass A over the corpus, and the per-stage Lean speed
are all downstream of the build and are unreached; each is reported as
blocked with its cause, none is faked. Along the way a second, smaller
flag: the toolchain the cache pins is fetched by `elan` from
`release.lean-lang.org`, which the proxy allowlist does not carry and
refuses; the identical archive is on `github.com`, which the allowlist
does carry and which the brief itself names as the toolchain's source,
so the toolchain step got past its refused host and let the real
blocker surface.

The churn reading is not incidental to this failure — it is the
failure. the owner's test is `written once` against `never written`: the emit
is a `never written` artifact, produced per model commit by a specific
sail version, and this is exactly a case where that per-version artifact
and the tool that consumes it have drifted apart. The system did what
it is supposed to do on churn — it tried to regenerate and stopped
loudly at a build that fails, rather than drifting — and the repair is
mechanical and nameable (a newer sail), not a hand edit anywhere.

---

## 2. What is on disk, what was reached, and where it stopped

Table 1 — the five lanes of this task, in order, each on instance
`lp1`. Every lane `state=done exit=0`. "reached" is what the lane
established; "of" is stated where a loop ran.

| lane | tower log stamp | elapsed | reached |
|---|---|---|---|
| `lp1_l1_fetch_and_build_lean_sail.sh` | `20260913T231339Z` | 16.1 s | elan's toolchain fetch REFUSED by the proxy (flag 1) |
| `lp1_l1b_elans_download_sources.sh` | `20260913T231504Z` | 1.5 s | named the refused host and elan's download source, LITERAL |
| `lp1_l1d_fetch_from_github_and_build.sh` | `20260913T231702Z` | 62.2 s | toolchain from github.com; lean-sail v4 built; model build FAILED (flag 2) |
| `lp1_l1e_the_first_build_error_in_full.sh` | `20260913T231908Z` | 55.2 s | the build errors in full, LITERAL |
| `lp1_l2b_definitions_sample.sh` | `20260913T232708Z` | 27.8 s | definitions listed and keyed from the emit text (needs no build) |

(Lane `lp1_l1c` at `20260913T231619Z` is between l1b and l1d; it named
the toolchain asset with a stray `v` and met the image's missing
`zstd`, both fixed in l1d; it is kept, not removed, per the standing
rule.)

The one measurement that needs no built model is §3. Everything from §4
on is downstream of the build and is blocked; each is stated with its
cause and nothing is fabricated.

---

## 3. The definitions, from the emit text — brief §3 item 1

`SailModel.definitions` reads the emitted Lean to LIST the `execute`
clauses and their keys (`key_of`); the brief permits parsing the text
"only to LIST the clauses and their keys, never to rewrite a
definition." That listing needs no built model and is the one thing
this task measured end to end. Lane `lp1_l2b_definitions_sample.sh`,
tower log `20260913T232708Z`; artifact
`PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/lp1_definitions.json`;
peak resident 23,752 kB (bound 6 GB, abort `ABORT_MEMORY_LP1`, never
raised).

Table 2 — `execute` clauses in the emit, counted by extension. The
extension is read from the model's OWN source: which `.sail` file under
`/sources/sail-riscv/model` carries `function clause execute <NAME>`,
and which extension folder that file sits in. Machine structure, no
token. **LITERAL** (lane step [2/6]).

| extension | clauses | of 29 |
|---|---|---|
| I | 20 | 29 |
| M | 6 | 29 |
| cfi (Zicfilp, `LPAD`) | 1 | 29 |
| postlude (`C_ILLEGAL`, `ILLEGAL`) | 2 | 29 |

**GLOSS.** A `def execute_<NAME>` is one clause; a clause may cover many
cells (e.g. `execute_RTYPE` covers `add sub and or xor sll srl sra slt
sltu` through its `rop` selector). The 29 clauses expand to 49 keys
below.

Table 3 — the keys as `key_of` reads them (mnemonic, operand form,
width): the mnemonic from the emitted `*_mnemonic_forwards` maps (or the
assembly literal), the operand form from the `instruction` inductive
constructor's tuple, the width from the clause (the W-forms are 32,
the base forms 64). Ten of 49. **LITERAL** (lane step [2/6]).

| mnemonic | operand form | width | from clause | of 49 |
|---|---|---|---|---|
| add | reg reg reg | 64 | execute_RTYPE | 49 |
| and | reg reg reg | 64 | execute_RTYPE | 49 |
| or | reg reg reg | 64 | execute_RTYPE | 49 |
| sll | reg reg reg | 64 | execute_RTYPE | 49 |
| slt | reg reg reg | 64 | execute_RTYPE | 49 |
| sltu | reg reg reg | 64 | execute_RTYPE | 49 |
| sra | reg reg reg | 64 | execute_RTYPE | 49 |
| srl | reg reg reg | 64 | execute_RTYPE | 49 |
| sub | reg reg reg | 64 | execute_RTYPE | 49 |
| xor | reg reg reg | 64 | execute_RTYPE | 49 |

**GLOSS.** The mnemonic sits in the field `mnem`, the guard's exempt
machine-form field; the operand form and width are read, never a token.
The full 49 include `mul mulh mulhu mulhsu` (execute_MUL, 64), `div
divu` (execute_DIV, 64), `divw divuw` (execute_DIVW, 32), `rem remu`
(execute_REM, 64), `mulw` (execute_MULW, 32), and the I-type and W-type
families.

### 3.1 `strip` on DIV and on a MUL-family clause — LITERAL, and why it is the RAW clause

`strip`'s own output is "the pure expression Lean holds AFTER `simp`
unfolds the reads and the write." That needs Lean to elaborate the
model, which is exactly what does not build (§4). So what follows is the
RAW emitted clause — the object `strip` would consume — quoted from the
cache with its path and line; the simp-normal form `strip` returns is
BLOCKED and is not shown, rather than a hand reading substituted for it.

**LITERAL**, `…/cache/sail-riscv_3243f93_I_insts_M_insts_postlude_main/LeanIM/InstsEnd.lean:4383`
(`execute_DIV`), the quotient logic, wrapped at 72 columns:

```
let quotient :=
  if ((rs2_int == 0) : Bool)
  then (Neg.neg 1)
  else (Int.tdiv rs1_int rs2_int)
let quotient :=
  if (((not is_unsigned) && (quotient >=b (2 ^i (xlen -i 1)))) :
      Bool)
  then (Neg.neg (2 ^i (xlen -i 1)))
  else quotient
(wX_bits rd (to_bits_truncate (l := 64) quotient))
```

(the reads stripped are `let rs1_bits <- (rX_bits rs1)` and the `rs2`
read and the signed/unsigned integer reads above; the write is the
`wX_bits rd ...` line. The whole clause is in the cache at that path and
in log 274 §2.3 verbatim.)

**LITERAL**, `…/LeanIM/Arithmetic.lean:240`, the helper every MUL-family
clause calls (`execute_MUL` is `(wX_bits rd (mult_to_bits_half (l :=
xlen) mul_op.signed_rs1 mul_op.signed_rs2 rs1_bits rs2_bits
mul_op.result_part))`), wrapped at 72 columns:

```
let result_wide :=
  (to_bits_truncate (l := (2 *i l)) (rs1_int *i rs2_int))
match result_part with
| .High => (Sail.BitVec.extractLsb result_wide ((2 *i l) -i 1) l)
| .Low  => (Sail.BitVec.extractLsb result_wide (l -i 1) 0)
```

**GLOSS.** This is the object log 274 §2.3 and log 273 §3.6 named as the
`mulh` cause: the definition's high half is an `extractLsb` of a
doubled-width integer product, general in the width `l`. The handful
was to feed this to `equals` at the integer level and see `ring` close
it against c's compiled `(__int128)a*b >> 64`. That measurement is
blocked (§5).

---

## 4. The flags for the coordinator, each LITERAL

Per LAW's stop rules: a build that fails and a fetch/install outside
lane 1 are stop-lines — flagged with literal output and count, never
worked around, never a hand edit. Two were met.

### 4.1 FLAG 1 — the pinned toolchain's download host is refused by the proxy

`elan` 4.2.4 downloads every toolchain from `release.lean-lang.org`.
The `lp1` allowlist does not carry that host, so the proxy refuses it.
**LITERAL**, lane `lp1_l1_fetch_and_build_lean_sail.sh`
(`20260913T231339Z`), step [2/9]:

```
elan 4.2.4 (227caca13 2026-08-25)
  toolchain the cache pins: leanprover/lean4:v4.29.0
error: error during download
info: caused by: [56] Failure when receiving data from the peer
      (CONNECT tunnel failed, response 403)
```

**LITERAL**, the proxy's own denied log, lane
`lp1_l1b_elans_download_sources.sh` (`20260913T231504Z`) and the
`lp1-proxy` access log, the refused host:

```
TCP_DENIED/403 3368 CONNECT release.lean-lang.org:443 - HIER_NONE/-
```

count: every toolchain fetch attempt refused (8 CONNECTs to that host
in the l1/l1b window, all `TCP_DENIED/403`).

How the line proceeded, transparently, rather than stopping here: the
brief's own words are "elan installs that toolchain … (its downloads
come from GitHub releases; if a host is refused, FLAG the literal
host)." `github.com` IS on the allowlist and IS where the release
archive lives, so lane `lp1_l1d` took the identical pinned archive
(`https://github.com/leanprover/lean4/releases/download/v4.29.0/lean-4.29.0-linux.zip`,
sha256 `e5cf6952…1663`) from github.com and unpacked it into elan's
toolchain directory. The proof that this is the same toolchain,
**LITERAL** (l1d step [3/10]):

```
Lean (version 4.29.0, x86_64-unknown-linux-gnu,
      commit 98dc76e3c0a9b856c9b98726b713fb04fab16740, Release)
```

The coordinator's call: add `release.lean-lang.org` (and its asset
host) to the `lp1` allowlist so `elan` installs natively, OR keep the
github.com route. Either way flag 2 below is the blocker that matters;
this one only gates it. Recorded, not decided by me.

### 4.2 FLAG 2 — the cached emit does not build under the toolchain and library it pins

`lean-sail` rev `v4` resolves and builds fine on its own. **LITERAL**,
lane `lp1_l1d` step [5/10] and [7/10]:

```
info: Sail: checking out revision
      '79b4d08505af29d88b3918f32d29840fae1fa191'
...
Build completed successfully (7 jobs).
```

(that is the Sail support library — `lean-sail` v4, commit `79b4d08`,
"Update Lean version (#7)", its own `lean-toolchain` is `v4.29.0` —
built in 5.7 s, peak 1.56 GB. The library is not the problem.)

The model's first module fails. **LITERAL**, lane
`lp1_l1e_the_first_build_error_in_full.sh` (`20260913T231908Z`) and
`lp1_l2b` step [5/6]: twelve errors from `LeanIM/Defs.lean`, the first
eight:

```
LeanIM/Defs.lean:618:8: Unknown identifier `k_v`
LeanIM/Defs.lean:618:19: Unknown identifier `k_v`
LeanIM/Defs.lean:618:55: Unknown identifier `k_v`
LeanIM/Defs.lean:618:66: Unknown identifier `k_v`
LeanIM/Defs.lean:618:102: Unknown identifier `k_v`
LeanIM/Defs.lean:619:9: Unknown identifier `k_v`
LeanIM/Defs.lean:623:54: unexpected token '('; expected ')', ',' or ':'
LeanIM/Defs.lean:625:49: unexpected token '('; expected ')', ',' or ':'
```

count: 12 `error:` lines from `LeanIM/Defs.lean`; `LeanIM.Defs` is
imported by every model module, so 0 of 116 modules build.

The cause, in the emitted text. **LITERAL**, `LeanIM/Defs.lean:623,
625, 627`:

```
abbrev vpn_level_size : Int :=
  (12 - if ( is_sv32_mode(k_v)  : Bool) then 2 else 3)
abbrev pte_bits k_v := (BitVec (if ( is_sv32_mode(k_v) : Bool)
  then 32 else 64))
abbrev ppn_bits k_v := (BitVec (if ( is_sv32_mode(k_v) : Bool)
  then 22 else 44))
```

**GLOSS.** `is_sv32_mode(k_v)` is Sail's own call syntax `f(x)` leaked
verbatim into Lean, where it parses as `is_sv32_mode` applied to
`(k_v)` and `k_v` is unbound; `vpn_level_size` references `k_v` with no
parameter at all. In the Sail source
(`/sources/sail-riscv/model/core/vmem_types.sail`) these are parametric
type functions, `type pte_bits('v), is_sv_or_svx4_mode('v) = …`. sail
0.20.2's Lean backend did not lower them to well-formed Lean. These are
the virtual-memory (page-table) types in `core`, required transitively
by every selection, so no module — arithmetic included — compiles.
`is_sv32_mode(` occurs 3 times in the emit.

Why this is a stop-line and not a workaround:

- the emit is a build product; a file under
  `Research/oracle/riscv/leanpath/cache/` is never edited (brief and
  launch). Hand-fixing `Defs.lean` is forbidden and would be a per-model
  hand edit — the opposite of the line's whole point.
- re-emitting with the SAME sail (0.20.2, the only one in the image) is
  deterministic and reproduces the same text.
- the model requires 0.20.2 for its C build — **LITERAL**,
  `/sources/sail-riscv/cmake/sail_required_version.txt`:

  ```
  0.20.2
  ```

  but the model's own Lean CI builds with a NEWER sail — **LITERAL**,
  `/sources/sail-riscv/.github/workflows/compile-lean.yml`:

  ```
  - name: Common setup
    uses: ./.github/actions/sail-setup
    with:
      sail-version: "latest"
  ```

- so the repair is: install a newer sail and re-emit into a new cache
  folder. That is a fetch/install outside the one fetch lane the brief
  names (lane 1's network is for the Lean toolchain and `lean-sail`
  only). Per LAW, this line stops and the coordinator decides.

### 4.3 Recorded, minor — the image has no `zstd`

`elan`'s native archive is `.tar.zst`; the image has neither the `zstd`
binary nor python's `zstandard`. **LITERAL**, lane `lp1_l1c` step [2]:
`zstd: ABSENT`, and `ModuleNotFoundError: No module named 'zstandard'`.
lane `lp1_l1d` took the `.zip` release asset instead and unpacked it
with python's `zipfile` (13,352 files). Not a blocker; recorded so a
future lane that lets `elan` install natively knows the `.tar.zst` path
needs `zstd` in the image.

---

## 5. The handful, pass A, and the speed — brief §3 items 2, 3, 4 — all blocked, with cause

None of these could run: they need the model built as a Lean library
(`meaning` composes Sail's `execute` and unfolds it with `simp`;
`equals` builds theorems Lean's kernel checks). The build is flag 2.
Nothing here is estimated or faked.

Table 4 — the handful, brief §3 item 2. Ten rows were to carry the
stage reached, seconds, peak, and the proof file or refusal, with the
`mulh` on c as the headline. Reached: 0 of 10.

| unit | stage reached | cause |
|---|---|---|
| the ten of rv1 (log 258) | not started | BLOCKED by flag 2: no built model to compose `meaning` in, no kernel to check `equals` |
| `mulh` on c (the headline) | not started | same; the integer-level `ring` test of log 274 §5.3 is unmeasured |

Table 5 — pass A over the rv6 corpus, brief §3 item 3. The population is
the 255 RISC-V cells on c, c++, rust, go. Reached: 0 of 255 per
language.

| language | dictionary entries proved | swap table size | of 255 |
|---|---|---|---|
| c | not started | not started | 255 |
| c++ | not started | not started | 255 |
| rust | not started | not started | 255 |
| go | not started | not started | 255 |

Cause: `System.pass_a_find` proves each unit's `meaning` against each
definition in Lean; both sides need the built model. BLOCKED by flag 2.
(For reference, the z3-gate line already reaches, per log 273 §6.2, of
255: c 243, c++ 243, rust 247, go 243 on some route; 251 on some
language; 235 on all four. The Lean path was to re-establish these as
kernel-checked theorems; that is what is blocked.)

Table 6 — speed measured, brief §3 item 4, beside log 274 §7.1's
expectations. Only the steps that do not need the built model are
measured.

| step | expected (log 274 §7.1) | measured here | of |
|---|---|---|---|
| `definitions()` emit | 45 min, 17 GB, once/commit | already cached (log 274 §3, l5); not re-run | — |
| toolchain fetch + unpack | plumbing | curl 11.1 s (839 MB zip) + unpack ~12 s (l1d) | — |
| `lean-sail` v4 library build | plumbing | 5.7 s, peak 1.56 GB (l1d) | 7 jobs |
| definitions text listing | seconds | 27.8 s wall, peak 23,752 kB (l2b) | 29 clauses / 49 keys |
| `meaning` per unit | seconds expected | UNMEASURED | BLOCKED by flag 2 |
| `equals` integer level / bv_decide | under 1 s expected | UNMEASURED | BLOCKED by flag 2 |
| `equals` on `mulh` at integer level | the headline | UNMEASURED | BLOCKED by flag 2 |
| pass A over 255 × 4 | ~1 hour expected | UNMEASURED | BLOCKED by flag 2 |

The speed_measured node's PROGRESS carries this table.

---

## 6. The churn statement — brief §3 item 5

**What in this module names an opcode: nothing.** This task wrote no
`leanpath/` class module (the classes are downstream of the build and
would be untested logic; §8). What it did write — five lane scripts and
one definitions listing — names no opcode as a case, key, branch or
comparison scope. **LITERAL**, the grep over the files lp1 added
(`PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/lanes_lp1/*.sh`
and `lp1_definitions.json`), looking for any control construct keyed on
an opcode spelling:

```
grep -nE '\b(if|elif|case|when|match)\b.*("|'\'')(add|sub|mul|mulh|
  div|rem|sll|srl|sra|and|or|xor|slt)("|'\'')' lanes_lp1/*.sh
  -> none: no branch keyed on an opcode spelling
```

The only place a mnemonic appears is as the exempt `mnem` display field
of a key read from the model, and where the driver reads the model's own
`*_mnemonic_forwards` maps and `execute_<NAME>` defs to LIST clauses —
never to select behaviour. The mechanical proof is the guard's own
verdict on the one json this task wrote. **LITERAL**, lane `lp1_l2b`
step [6/6]:

```
operator inventory: 91 tokens read from probe_manifest_*.json
PASS lp1_definitions.json -- no operator token in any key, grouping,
     pairing or row structure
  guard rc=0
```

`grep -c exempt` over the files lp1 ADDED: 0 on `lp1_definitions.json`;
nonzero only on the two lane scripts that RUN the guard (the word is
inside the command they run), exactly as rv1/rv9 reported — 1 on
`lp1_l2_definitions_sample.sh`, 2 on `lp1_l2b_definitions_sample.sh`.

**What happens on a new model commit:** the cache key is the commit, so
a new commit misses the cache and `SailModel.definitions` re-runs the
emit. Nobody writes anything — except that THIS is where flag 2 bites:
the emit's correctness is coupled to the sail version, a `never
written` per-release artifact, and the image's sail (0.20.2) is behind
what the model's Lean now needs. The system regenerated on churn and
stopped loudly at a build that fails, which is the designed behaviour;
the repair is a newer sail, named and mechanical, not a hand edit.

**What happens on a new compiler release:** pass A re-proves. Each
language's units are re-lifted by `meaning` and re-checked by `equals`;
`operator_for` is refilled by proof. Unverified here because it is
downstream of the build (flag 2).

---

## 7. The guard, the counts, the verifier

- The spelling guard passed on the merits over `lp1_definitions.json`
  (§6, LITERAL). `check_no_spelling_keys.py` was not modified; its role
  is unchanged.
- `grep -c exempt` = 0 on the deliverable json (§6).
- The conventions verifier over this log: §9 (final lane).
- Nothing under `Research/op_pipeline/` was touched;
  `riscv_reference.py` was not touched; no file under
  `Research/oracle/riscv/leanpath/cache/` was edited. Nothing under
  `PUBLIC/Airlock/` or `<runs>/` was deleted, on
  either machine. The idle `sl1-runner` container was not touched.

---

## 8. Why no `leanpath/` class module was written

The brief's "what you build" is the module `leanpath/` with the classes
`SailModel`, `LeanExpr`, `ArchUnit`, `Language`, `Emulation`,
`Dictionary`, `System`. Every method that carries the line's meaning —
`LeanExpr.equals`, `LeanExpr.decide_fixed_width`, `ArchUnit.meaning`,
`ArchUnit.compose`, `System.pass_a_find` — is defined only in terms of
a built model: it composes Sail's `execute` in Lean and asks the kernel
to check a theorem. With the model not building (flag 2), none of them
can be exercised, and `plan_and_code.md` §2 is explicit that logic is
written last, only where descending one level adds logic that can be
reviewed by running it. Writing those bodies now would be unrunnable
logic against a foundation that does not stand — the drift that file
exists to prevent. The one class behaviour that needs no build,
`SailModel.definitions`'s text listing and `key_of`, is demonstrated by
lane `lp1_l2b` and its json (§3); embodying it as a class is deferred
with the rest until the emit builds. This is recorded, not decided.

---

## 9. The verifier's tally, and the claims that reproduce

### 9.1 The load-bearing claims, each with the command that reproduces it

Each block is a transcript re-run inside the `lp1` instance, where this
repository is mounted at `PseudoCoupHQ` and the emit cache is
`$EMIT` =
`PseudoCoupHQ/Research/oracle/riscv/leanpath/cache/sail-riscv_3243f93_I_insts_M_insts_postlude_main/LeanIM`.

The model pins sail 0.20.2 for its C build (§4.2):

```
$ cat /sources/sail-riscv/cmake/sail_required_version.txt
0.20.2
```

29 `execute` clauses in the emit (§3, Table 2):

```
$ grep -rhoE '^def execute_[A-Za-z0-9_]+' PseudoCoupHQ/Research/oracle/riscv/leanpath/cache/sail-riscv_3243f93_I_insts_M_insts_postlude_main/LeanIM/*.lean | sort -u | wc -l
29
```

the Sail call-syntax leak, 3 sites, all in `Defs.lean` (§4.2):

```
$ grep -c 'is_sv32_mode(' PseudoCoupHQ/Research/oracle/riscv/leanpath/cache/sail-riscv_3243f93_I_insts_M_insts_postlude_main/LeanIM/Defs.lean
3
```

the spelling guard passes on the merits over the one json (§6):

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/riscv/leanpath/lp1_definitions.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS lp1_definitions.json -- no operator token in any key, grouping, pairing or row structure
```

### 9.2 The tally

Lane `lp1_l3b_verifier.sh`, tower log `20260913T233447Z`, verifier
`check_conventions_log_claims.py --verify --timeout 20` over this log:

| outcome | claims |
|---|---|
| MATCHES | 3 |
| **DIFFERS** | **0** |
| UNVERIFIABLE | 13 |
| REFUSED | 1 |
| NOT_RERUNNABLE | 0 |
| population | 17 claims across 1 log |

Zero DIFFERS. The three that reproduce are the required-version, the
`is_sv32_mode(` count, and the guard. The one REFUSED is the clause
count above: its command names the path `…/LeanIM/*.lean`, and a glob is
not a file the verifier can reach from the instance, so it is scored
`log_unreachable` (REFUSED), never DIFFERS. The 13 UNVERIFIABLE are
LITERAL attributions to lane logs (the record) and prose, none carrying
an embedded `$ ` command — the same shape log 258 carried. The verifier
was not modified.

---

## 10. Flag summary (LITERAL), for the coordinator

1. **FLAG 1 — pinned toolchain host refused.** `release.lean-lang.org`
   is not on the `lp1` allowlist; `elan` 4.2.4 downloads from it and the
   proxy answers `TCP_DENIED/403 3368 CONNECT release.lean-lang.org:443`.
   Worked past (not around) by taking the identical `v4.29.0` archive
   from the allowlisted, brief-named `github.com`. Coordinator: add the
   host, or keep the github route.

2. **FLAG 2 — the cached emit does not build (the blocker).** Under the
   pinned `leanprover/lean4:v4.29.0` and `lean-sail` v4, `LeanIM/Defs.lean`
   fails with 12 errors; `is_sv32_mode(k_v)` (Sail call syntax) and an
   unbound `k_v` in the virtual-memory type abbreviations, emitted by
   sail 0.20.2. 0 of 116 modules build. The model pins sail 0.20.2 for C
   (`cmake/sail_required_version.txt`) but builds its Lean with sail
   `"latest"` (`compile-lean.yml`). Repair: re-emit with a newer sail
   into a new cache folder — a fetch/install outside lane 1, so the
   coordinator's call. The whole handful, pass A, and per-stage Lean
   speed are blocked on this.

3. **Recorded, minor.** The image lacks `zstd` / python `zstandard`, so
   `elan`'s `.tar.zst` cannot be unpacked; the `.zip` release asset was
   used instead.

---

## 11. Two lists

### Decided, recorded for audit

- `SailModel.definitions` is demonstrated at the text level over the
  cached emit: 29 `execute` clauses (I 20, M 6, cfi 1, postlude 2 of
  29), 49 keys read as (mnem, operand form, width), the two clauses
  `strip` consumes quoted LITERAL from the cache. Artifact
  `Research/oracle/riscv/leanpath/lp1_definitions.json`; guard PASS on
  the merits.
- The toolchain the cache pins (`leanprover/lean4:v4.29.0`, Lean commit
  `98dc76e`, lake 5.0.0) was obtained from github.com and cached under
  `/persist/lp1/elan`; `lean-sail` v4 (commit `79b4d08`) was fetched and
  built (5.7 s, peak 1.56 GB) into `/persist/lp1/Lean_IM/.lake`. These
  are cached across lanes in the instance's own volume, per the conf.
- The `leanpath/` class module is deferred until the emit builds (§8);
  its text-level behaviour is shown by lane `lp1_l2b`.
- Lane scripts are kept under `Research/oracle/riscv/leanpath/lanes_lp1/`
  and submitted from there; nothing was deleted; the `sl1-runner`
  container was left alone.

### Awaiting the owner

- **The blocker is the coordinator's to clear (flag 2):** authorise a
  newer sail (the version the model's Lean CI uses, `latest`) and a
  re-emit into a new cache folder, so the model's Lean builds and the
  handful, `mulh`, and pass A can run. Until then this line is stopped
  at its foundation, by design.
- **The refused toolchain host (flag 1):** whether to add
  `release.lean-lang.org` to the `lp1` allowlist so `elan` installs
  natively, or keep the github.com route this task used.
