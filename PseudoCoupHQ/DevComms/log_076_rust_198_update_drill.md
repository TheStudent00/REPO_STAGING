# log 076 — the rust 1.98 update drill: how automated are we when a target language moves?

Date: 2026-08-29. A MEASUREMENT exercise, not a build. Every number
below was printed by a run; nothing here is asserted from reading
code. Where something could not be run it is marked unverified with
its reason.

Layer named, per the three-layer anchor: this drill serves **layer 3
(OPERATION)** — what the compiler can do to a representation — with
one excursion into the shape machinery that sits under layers 1 and 2.

---

## 1. Plain-words walkthrough

### what the drill is

One of the twelve target languages shipped a new version. The
question is not "is the new version interesting" — it is "when a
language moves, how much of our pipeline notices, and how much needs
a person to type something". So the whole pipeline was pointed at
rust twice, once at the old compiler and once at the new one, with no
hand edits, and the difference was counted.

Four things were measured, in this order. **The shape layer** — the
machinery that reads a language's grammar and produces its token
alphabet and its kind map (the table saying which of the grammar's
named node kinds becomes which of our fifteen objects). **The
toolchain layer** — what it actually cost, in steps and minutes, to
get the new compiler into the container. **The behaviour layer** —
the census harness, which is the generator that turns a census page's
claims into one shell script per page, runs it in the sandbox, and
compares what came back against what the page promised. And
**classification** — where rust's new operations belong in the
vocabulary the census already uses.

Two words that have been away and need re-warming before they appear
below. A **lane** is one shell script dropped into the sandbox's
`drop/` directory, which the sandbox daemon runs on its own and whose
output lands in `out/`. A **vector** is one census claim written out
as a tiny runnable probe, living in `vectors_<object>.json`; the
generator pastes each vector into each language's runner template.

### what the release actually contains — verified, not summarised

rust 1.98.0 exists, it shipped on 2026-08-20, and the stable channel
manifest names that date. The dist server answers 200 for 1.98.0 and
for 1.97.0 and 404 for 1.99.0, so 1.98.0 is the current stable and
nothing newer is out. The compiler identifies itself as
`rustc 1.98.0 (88d9e12ae 2026-08-18)`.

The release notes' "Stabilized APIs" section lists twenty-three
items, five of which are the float methods the brief named:
`algebraic_add`, `algebraic_sub`, `algebraic_mul`, `algebraic_div`,
`algebraic_rem`. The standard library source agrees independently:
`library/core/src/num/f64.rs` and `f32.rs` each carry ten attributes
saying `since = "1.98.0"`, and reading the method names straight out
of those attributes gives exactly those five names in both files. Two
sources, agreeing, both machine-readable.

The brief's claim that the methods also arrive on `f16`/`f128` is
**only half true on stable rust**, and this is the first finding. The
methods exist for those types, but the TYPES themselves are still
unstable at 1.98.0: a program writing `let a: f16 = 1.0;` is refused
with `error[E0658]: the type f16 is unstable`, pointing at issue
#116909. On stable rust the five methods are reachable on `f32` and
`f64` only.

The claim that they are non-deterministic is **confirmed, with a
correction to its shape**. The same source file, compiled four times
by the same compiler at four optimisation settings, produced four
different answers on one probe and three on another. But the
variation is between BUILDS, not between runs of one build: a probe
that computes the same expression twice inside one program got the
same bits both times, in every build. So "the same expression may
give different results depending on optimization" is exactly right,
and the stronger reading some people hear in the word
non-deterministic — that one compiled binary might answer differently
on two runs — was not observed. Not refuted either; a sample refutes,
it never proves.

Two further things the runs established that the brief did not claim.
The special-value contract does not move: NaN, both infinities and
negative zero came back bit-identical to the ordinary operators at
every optimisation level — twelve special-value probes, zero of them
build-sensitive. And the methods ARE usable in a constant:
`const K: f64 = (1.0f64).algebraic_add(2.0f64);` compiles and gives
3, because constant evaluation has nothing to rearrange.

### what happened at each layer

The shape layer did nothing, and that is the correct answer. The
grammar pin check passed 12 of 12, the kind map for rust came out
byte-identical, and the token-alphabet staleness check printed the
same five lines it printed before. Algebraic methods are library
additions, not syntax, so there was nothing there for the shape layer
to see. The honest complication is that these three checks could not
have seen a syntax change either, because none of them asks the
compiler anything — they read a pinned grammar package and a constant
that was typed out of rustc's source by hand on 2026-08-12. That
constant was re-fetched and checked during this drill and it is still
correct, but its correctness today is luck, not machinery.

The toolchain layer was cheap: eighty-six seconds, one command, no
blockers. The allowlist already permitted the download site and no
sync is needed. Exactly one file in the whole estate pins rust's
version, and nothing broke.

The behaviour layer split in two. Re-running the existing float
vectors under the new compiler changed nothing at all: twenty
fact-by-language cells across the two rust build modes, seventy-eight
probes, every previously confirmed cell still confirmed, byte-identical
result files. Adding the new methods, on the other hand, took real
authorship — and the interesting part is WHY. The first attempt,
written in the census's existing style, produced the same answer in
both build modes and so measured nothing. Isolating the cause took
three more sandbox runs and found that two conditions must BOTH hold
before the optimiser can move anything: the operands must be bound to
a name once and reused, and they must be hidden from constant
evaluation. The census's vectors format can express neither, because
a vector is a single expression and its helper functions are
transparent identity functions. The preamble mechanism the harness
already has — a per-language file of named functions holding
statements — can express both. So the addition cost two files and
193 lines and zero changes to any tool.

Finally, the one thing in the entire drill that DID detect that the
language had moved was the old compiler itself: building the new
program at 1.96.1 produced thirty-nine instances of
`error[E0658]: use of unstable library feature 'float_algebraic'`.
That is compile-or-refuse working exactly as ratified — but nothing
in the repo runs it, because nothing holds a list of names to try.
That list turns out to be machine-readable in two seconds.

---

## 2. The automation scorecard

Counts are of things measured in this drill, not estimates.

| layer | fired automatically, zero hand edits | needed a config or pin bump only | needed new human authorship |
|---|---|---|---|
| A — shape (grammar pin, token alphabet, kind map) | 3 tools run, 3 clean: pin check 12/12 pass; differential alphabet identical output (111 grammar tokens, 53 rustc punctuation names, 51 agreed, 2+4 known residue); pack generator over rust byte-identical (163 kinds, 106 proposed, 57 residue). 0 signals — and 0 signals were POSSIBLE, since none of the three consults a compiler | 0 | 0 lines written. But: 1 transcribed constant (53 entries, fetch-dated 2026-08-12) has no refresh path; and `operator_arity.py` verifies table→grammar only, never grammar→table (rust: 44 recorded spellings all found, 129 grammar anonymous kinds never checked back, 19 of them punctuation-shaped) |
| B — toolchain | 0 | 1 command, 86 s, 0 blockers; `.rust-lang.org` already on the allowlist, dist reachable HTTP 200. Exactly 1 version pin in the estate: `Airlock/Containerfile` line 82, `--default-toolchain 1.96.1`. 0 breakage: no `Cargo.toml`, no `rust-toolchain` file, no version string in PseudoCoupHQ | 0 |
| C1 — behaviour, regression | Full boolean/float lane re-run twice, unchanged script at 1.96.1 (14.5 s) and 1 inserted PATH line at 1.98.0 (10.3 s). 11 result files byte-identical between the two compilers; rust and rust-release byte-identical to the 2026-08-14 records. 20 rust cells, 78 probes, 100 CONFIRMED / 0 REFUTED at both versions | 1 line (a `PATH` prefix inserted after `set -u`; diff = 1 line against a 2,584-line lane) | 0 |
| C2 — behaviour, new content | The "what is new" inventory is fully derivable: 23 stabilised APIs and the 5 float method names extracted from two independent machine-readable sources in 2.1 s by a ~40-line script. The old compiler's 39 `E0658` refusals are a free change-detector already ratified as compile-or-refuse | 0 | 2 files, 193 lines: 128 added to `vectors_boolean_float.json`, 65 in a new `templates/rust.boolean_float.pre`. 0 changes to `generate_run.py`, `compare.py`, `rust.tmpl`, `rust.probe`. Plus 4 sandbox iterations to isolate the two conditions a probe needs. Expected values: not derivable, measured |
| D — classification | 0 | 0 | 1 proposal, 0 decisions. Existing camps do not fit; a fourth guaranteed add is proposed in §4 for the owner's ruling |

Incidental drift found while running the above, unrelated to the
release:

| finding | measure |
|---|---|
| `generate_run.py` is not a fixed point on its own committed lane | regenerating `lane_bf.sh` from the UNCHANGED vectors differs from the committed file by 126 lines (63 removed, 63 added): 24 lines of a `<compile-error>` verdict refinement that the generator no longer emits, and 39 c++ probe lines whose template shape changed |
| the container lost a toolchain since the census was recorded | typescript ran on 2026-08-14 and is ABSENT today; the census's one recorded REFUTED cell (bool-U4, typescript, TS2367) could not be re-measured |

---

## 3. Layer by layer, with the evidence

### 3.1 Layer A — the shape layer

Three tools were run unchanged. Level: this is the SHAPE layer
(grammar evidence), not the intention layer.

**The grammar pin check.** `PseudoCoup_v6/Tools/ledgerer/tree_sitter/test_tree_sitter_base.py`,
which parses a pinned fixture per grammar and demands the rendered
census equal the frozen file byte for byte.

```
12 passed in 0.04s
```

Pins unchanged: tree-sitter 0.26.0, tree-sitter-rust 0.24.2,
tree-sitter-python 0.25.0, tree-sitter-cpp 0.23.4.

**The differential alphabet.** `PseudoCoup_v5/Research/differential_alphabet.py`.
Note the path: the brief named it under `PseudoCoupHQ/Research/kind_clustering/`;
that folder does not exist and the file lives in PseudoCoup_v5.
Output, unchanged:

```
grammar anonymous tokens : 111 (55 punctuation, 56 word-like)
rustc TokenKind punctuation: 53
AGREE on 51 punctuation tokens
in rustc, not in the pinned grammar: '<-' (LArrow), '~' (Tilde)
in the pinned grammar, not in rustc's list: '"', '*/', '/*', '//'
```

**The specific point the brief asked to be tested honestly, answered
plainly: yes, the rustc side is a transcribed constant and it cannot
notice a change by itself.** The file says so in its own docstring —
"TRANSCRIBED, not fetched at run time: the constant below is typed
from the source and is therefore only as current as its fetch date"
— and the fetch date is 2026-08-12. Both of its two authorities are
frozen: authority A is a pinned pip package, authority B is a python
dict. The script would print the same five lines if rust released
fifty versions.

What a refresh costs was then measured rather than guessed. Fetching
`compiler/rustc_ast/src/token.rs` at both tags and diffing them:

| measure | 1.96.1 | 1.98.0 |
|---|---|---|
| file size | 41,032 bytes | 40,737 bytes |
| `TokenKind` variants | 62 | 62 |

The diff is 109 lines and every substantive hunk is one rename of a
derive macro (`HashStable_Generic` becoming `StableHash`). Checked
against the transcribed constant directly: all 53 transcribed
punctuation names are still present at 1.98.0, and the 9 variants not
transcribed (`Eof`, `Ident`, `Literal`, `Lifetime`, `NtIdent`,
`NtLifetime`, `DocComment`, `OpenInvisible`, `CloseInvisible`) are
the non-punctuation ones the file deliberately excludes. **The
constant did not go stale.** The refresh is two `curl` calls and a
diff, and it should be the mechanism rather than a person's memory.

**The pack generator.** `Research/kind_signature_clustering/pack_generator.py rust`,
run into a scratch copy so the repo was untouched:

| measure | before | after |
|---|---|---|
| `proposed_kind_map_rust.json` md5 | a180636645f63e9ace021bd1802d711d | unchanged |
| `proposed_kind_map_rust.md` md5 | 65569d9872698d762e24816d3d0aa63d | unchanged |
| named kinds | 163 | 163 |
| proposed | 106 | 106 |
| residue | 57 | 57 |

**The rust kind map did not change at all, and that is a correct
non-event.** Algebraic methods are method calls; a method call is
already `call_expression` in the grammar, which the map already
carries. A library addition cannot move a grammar-derived map, and it
did not.

**The operation inventory: DISCOVERED or HAND-LISTED? Hand-listed,
with a machine verifier.** This is the single fact the brief said
would largely decide the verdict, so here is the evidence by name.

`Research/kind_fuzz_clustering/operator_arity.py` is the per-language
operator inventory, and `Research/op_pipeline/probe_gen.py` reads it
— its docstring calls it "the grammar-authored operator inventory,
per language, in arity buckets." The inventory itself is a python
literal. Every row is a call to a helper, `G(rule, file, ops)`, whose
docstring reads: `"""One fact: 'ops' are admitted by 'rule' in grammar
file 'file'."""` Rust's binary row, verbatim:

```
G("binary_expression", "rust.js",
  ["&&", "||", "&", "|", "^", "==", "!=", "<", "<=", ">", ">=",
   "<<", ">>", "+", "-", "*", "/", "%"]),
```

The file is candid about this. Its header says the authority is the
grammar and that "`--verify` re-reads the grammar source and checks
that the spelling really does occur inside that rule". So the flow is
person types a spelling, machine confirms the grammar admits it. That
is verification, not discovery, and the direction matters: a spelling
in the table that the grammar has lost is caught, a spelling the
grammar has GAINED is invisible.

Measured, on rust:

| measure | count |
|---|---|
| anonymous node kinds in the compiled pinned grammar | 166 |
| spellings recorded in the hand table | 44 |
| recorded spellings confirmed present in the grammar | 44 of 44 |
| grammar anonymous kinds never checked against the table | 129 |
| of those, punctuation-shaped | 19 |

The 19 are delimiters and structural marks (`(`, `{`, `;`, `->`,
`=>`, `::`-adjacent forms, comment markers), so the table is complete
in practice for this grammar version. But nothing in the code
establishes that; `crosscheck_compiled()` computes the grammar's
anonymous-kind set and then only asks whether each RECORDED spelling
is in it. The set difference in the other direction is never taken.

The census side is hand-authored too, and says so: `census_integer.md`
opens "2026-08-13, hand-drafted", and `vectors_boolean_float.json`
is written from that page. So at both the operator grain and the
census grain, WHAT TO PROBE is a person's list; only WHETHER THE
PROBE IS LEGAL is machine-decided, by the compiler's own type checker
in the lane.

**Verdict for layer A: a correct non-event, and a blind spot.** The
shape layer was right to stay silent, and it would also have stayed
silent if the release had changed the grammar, because it never asks.

### 3.2 Layer B — the toolchain layer

| step | measure |
|---|---|
| is `.rust-lang.org` allowlisted | yes, already present in both `SandboxDesign/proxy/allowlist.txt` and `Airlock/proxy/allowlist.txt`. **No sync needed** |
| reachability | `curl` to `static.rust-lang.org` returned HTTP 200 before anything was installed |
| install command | `rustup toolchain install 1.98.0 --profile minimal --no-self-update` |
| install time | 86 seconds; 3 components |
| blockers | none |
| 1.96.1 kept | yes — installed into a separate `RUSTUP_HOME=/persist/rustup076`, so `/opt/cargo/bin/rustc` still answers 1.96.1 with the environment left alone |

Proof both are reachable, printed in one run:

```
with the inserted line, rustc --version  = rustc 1.98.0 (88d9e12ae 2026-08-18)
plain rustc = /opt/cargo/bin/rustc -> rustc 1.96.1 (31fca3adb 2026-06-26)
```

**What pins rust's version in the estate: exactly one line.**
`Airlock/Containerfile` line 82,
`| sh -s -- -y --no-modify-path --default-toolchain 1.96.1`. Searched
for and not found anywhere: a `rust-toolchain` file, a `Cargo.toml`,
a `rust-version` key, or a rust version string in any research script
under PseudoCoupHQ. **Nothing broke** — every python tool, every lane,
every check ran.

The image was NOT rebuilt and the pin was NOT bumped; that is
recorded as an open item in §6, because a co-installed toolchain
under `/persist` is outside the image.

### 3.3 Layer C1 — regression

The boolean/float lane was run twice today. The first run used
`harness/lane_bf.sh` copied byte for byte, at the container's default
compiler. The second used the same file with ONE line inserted after
`set -u` putting the 1.98.0 toolchain first on `PATH` — a 1-line diff
against a 2,584-line script.

| result file | 1.96.1 today vs the 2026-08-14 record | 1.96.1 today vs 1.98.0 today |
|---|---|---|
| `bf_rust.txt` | identical | identical |
| `bf_rust-release.txt` | identical | identical |
| the other 9 language files | not compared to record | identical |

Comparing against the census's claims with `compare.py`, unedited:

| run | CONFIRMED | REFUTED | SKIPPED |
|---|---|---|---|
| recorded 2026-08-14 | 109 | 1 | 20 |
| 1.96.1, today | 100 | 0 | 30 |
| 1.98.0, today | 100 | 0 | 30 |

The drop from 110 live cells to 100 is entirely typescript leaving
the container — 10 facts times 1 language — and the single recorded
REFUTED cell was typescript's `bool-U4` (TS2367, comparing two bool
literals), so it left with it. **No rust cell moved.** Cell by cell,
across all ten facts and both rust build modes:

| measure | recorded | 1.96.1 today | 1.98.0 today |
|---|---|---|---|
| rust + rust-release cells | 20 | 20 | 20 |
| all CONFIRMED | yes | yes | yes |
| probes checked | 78 | 78 | 78 |
| evidence values identical | — | yes | yes |

**Zero drift. F-f1 (division by zero) still answers `inf`, `-inf`,
`nan`, `inf` in both build modes.**

### 3.4 Layer C2 — the new content, measured

**(a) do they compile and run.** At 1.98.0, yes, at all four
settings tried. At 1.96.1, no: 39 errors, all
`error[E0658]: use of unstable library feature 'float_algebraic'`,
each pointing at issue #136469. That refusal is a first-class camp
answer under the 2026-08-14 ruling, and it is also the only automatic
signal in this whole drill that the language moved.

**(b) do they agree with the ordinary operators on simple values.**
Yes, on every value tried, at every optimisation setting, in both
widths. Bits, not printed decimals, per the census's own method rule.
The two columns are ordinary operator then algebraic method:

```
agree64.add|4013000000000000|4013000000000000
agree64.sub|4002000000000000|4002000000000000
agree64.mul|4011800000000000|4011800000000000
agree64.div|4006666666666666|4006666666666666
agree64.rem|3ff0000000000000|3ff0000000000000
agree32.add|40980000|40980000
agree32.sub|40100000|40100000
agree32.mul|408c0000|408c0000
agree32.div|40333333|40333333
agree32.rem|3f800000|3f800000
agree64.tenth|3fd3333333333334|3fd3333333333334
```

**(c) the interesting one — does the optimiser change the answer.**
One source file, one compiler (1.98.0), four builds. Only the lines
that differ between builds are shown; each cell is
`printed value | 64-bit pattern`. This table is the run's own output,
verbatim:

| probe | O0 | O1 | O3 | O3native |
|---|---|---|---|---|
| reassoc4.algebraic | 1\|3ff0000000000000 | 2\|4000000000000000 | 2\|4000000000000000 | 2\|4000000000000000 |
| loopsum.algebraic | 1\|3ff0000000000000 | 1\|3ff0000000000000 | 512\|4080000000000000 | 512\|4080000000000000 |
| loopsum2.algebraic | 10000000000000000\|4341c37937e08000 | 10000000000000000\|4341c37937e08000 | 10000000000000768\|4341c37937e08180 | 10000000000000992\|4341c37937e081f0 |
| loopmul.algebraic | 4611686018427388000\|43d0000000000000 | 4611686018427388000\|43d0000000000000 | inf\|7ff0000000000000 | inf\|7ff0000000000000 |
| twice.same_build | 3ff0000000000000\|3ff0000000000000 | 4000000000000000\|4000000000000000 | 4000000000000000\|4000000000000000 | 4000000000000000\|4000000000000000 |

And the tallies the same run printed:

```
probes identical across all builds: 31
probes that DIFFER across builds  : 5
ordinary-operator probes  : 12, of which build-sensitive: 0 []
algebraic-method probes   : 12, of which build-sensitive: 4
  ['loopmul.algebraic', 'loopsum.algebraic', 'loopsum2.algebraic', 'reassoc4.algebraic']
```

Read the rows. `reassoc4` is `((big+1)+(-big))+1` with `big = 1e100`:
left to right the big values cancel first and the answer is 1;
rearranged, the two ones are added together and the answer is 2.
`loopsum` sums 1,024 values arranged so that grouping matters — 1 at
O0 and O1, 512 at O3. `loopsum2` sums 1e16 followed by a thousand
ones, and gives THREE different answers: the same number at O0 and
O1, 768 higher at O3, and 992 higher again once `-C target-cpu=native`
is allowed, so the target CPU is also part of what picks the answer.
`loopmul` is the sharpest: a product containing 1e300 and 1e-300 that
answers 4611686018427388000 at O0 and O1 and **`inf` at O3** —
rearrangement moved the huge factor next to another huge factor and
the intermediate overflowed. The answer is still a valid float, which
is the whole point of the design: non-deterministic, never undefined.

`twice.same_build` is the control for the other reading of
non-determinism. It computes the same expression twice in one program
and prints both. Both halves agree in every build. So the answer is
fixed once the binary exists; it is the BUILD that chooses.

The optimiser's own testimony confirms the mechanism: the compiler
emitted 9 packed (SIMD) double instructions at O3 and 0 at O0.

**Do they change NaN or infinity behaviour? No — measured, not
assumed.** Every special-value probe was bit-identical to its ordinary
operator, and none of them moved between builds:

```
spec.inf_plus_neginf.ordinary|NaN|fff8000000000000
spec.inf_plus_neginf.algebraic|NaN|fff8000000000000
spec.nan_plus_one.ordinary|NaN|7ff8000000000000
spec.nan_plus_one.algebraic|NaN|7ff8000000000000
spec.one_div_zero.ordinary|inf|7ff0000000000000
spec.one_div_zero.algebraic|inf|7ff0000000000000
spec.zero_div_zero.ordinary|NaN|fff8000000000000
spec.zero_div_zero.algebraic|NaN|fff8000000000000
spec.inf_rem_one.ordinary|NaN|fff8000000000000
spec.inf_rem_one.algebraic|NaN|fff8000000000000
spec.negzero_add_zero.ordinary|0|0000000000000000
spec.negzero_add_zero.algebraic|0|0000000000000000
spec.neg_times_zero.ordinary|-0|8000000000000000
spec.neg_times_zero.algebraic|-0|8000000000000000
spec.negzero_sub_zero.ordinary|-0|8000000000000000
spec.negzero_sub_zero.algebraic|-0|8000000000000000
```

Negative zero matters here because the census lists −0.0 as a
structure fact of float. It survives: `-1.0 * 0.0` and
`-0.0 - 0.0` both keep the sign bit through the algebraic method, at
every optimisation level.

Two edge probes. **Constant context: accepted.**
`const K: f64 = (1.0f64).algebraic_add(2.0f64);` compiles and prints
3 — the library source marks all five `rustc_const_stable` since
1.98.0. **f16: refused**, `error[E0658]: the type f16 is unstable`.

### 3.5 What a person must write to add these to the census

Measured by doing it as a spike, in a scratch copy. The spike is NOT
installed in the repo — census pages and vectors are the owner's to rule.

The first attempt was written in the census's existing house style, a
single expression per probe using the template's helpers
(`d(1.0e100).algebraic_add(one())...`). It ran clean at 1.98.0 and
answered **1.0 in BOTH build modes** — it measured nothing. Isolating
why took three more runs. The five candidate shapes, all in one
program, at four settings:

| probe shape | debug | -O | -O2 | -O3 |
|---|---|---|---|---|
| A — census expression only | 1.0 | 1.0 | 1.0 | 1.0 |
| B — opaque, but the big value written twice | 1.0 | 1.0 | 1.0 | 1.0 |
| C — bound once, but foldable | 1.0 | 1.0 | 1.0 | 1.0 |
| D — bound once AND opaque | 1.0 | **2.0** | **2.0** | **2.0** |
| E — ordinary `+`, in shape D (the control) | 1.0 | 1.0 | 1.0 | 1.0 |

So BOTH conditions are needed, and the census's vectors format can
express NEITHER: a vector is one expression, so it cannot bind a name
and reuse it, and the templates' helpers (`d(x)`, `one()`) are
transparent identity functions the compiler folds through. The
harness's preamble mechanism — `templates/<lang>.<object>.pre`, a
file of named functions holding statements — can express both, using
`std::hint::black_box` as the opacity barrier.

The spike, redone that way and run for real in the sandbox at
1.98.0, produced this from the actual harness:

| probe | what it asks | rust (debug) | rust-release |
|---|---|---|---|
| F-f2.a–e | does each of the five agree with its ordinary operator | true, true, true, true, true | true, true, true, true, true |
| F-f2.f | add, rearrangeable | 1.0 | **2.0** |
| F-f2.g | sub, rearrangeable | 1.0 | **2.0** |
| F-f2.h | mul, rearrangeable | 2.0 | 2.0 |
| F-f2.i | div, rearrangeable | inf | inf |
| F-f2.j | rem, rearrangeable | 0.0 | 0.0 |
| F-f2.k | ordinary `+` in the same shape (control) | 1.0 | 1.0 |

`compare.py`, unedited, then scored it CONFIRMED on both rust rows
against per-mode expectations — the record-both-modes rule doing
exactly the job it was ruled for.

**The cost, counted:**

| item | count |
|---|---|
| files touched | 2 (1 new) |
| lines added to `vectors_boolean_float.json` | 128 |
| lines removed from it | 0 |
| lines in the new `templates/rust.boolean_float.pre` | 65 |
| total lines authored | 193 |
| changes to `generate_run.py` | 0 |
| changes to `compare.py` | 0 |
| changes to `templates/rust.tmpl` / `rust.probe` | 0 |
| sandbox iterations to find the right probe shape | 4 |

**Is any of it derivable from rustc's own data? The inventory is;
the probe bodies and the expected values are not.** A ~40-line
script, running in 2.1 seconds, pulled the complete list of what
changed from two independent machine-readable sources:

| source | what it yields |
|---|---|
| the project's `RELEASES.md`, 1.98.0 section (99 lines) | 3 Language items, 5 Libraries items, **23 Stabilized APIs**, 7 Platform Support, 18 Compatibility Notes — each a parsed bullet with its API name |
| `library/core/src/num/f64.rs` and `f32.rs` at tag 1.98.0 | 10 attributes each saying `since = "1.98.0"`; reading the method names off the attributes gives `algebraic_add`, `algebraic_div`, `algebraic_mul`, `algebraic_rem`, `algebraic_sub` in both files |

The two agree. What is NOT derivable: that a probe needs a bound-once
opaque operand, and what each probe should answer in each build mode.
Those were measured, and measuring them is the census's job.

---

## 4. Layer D — where do these belong, and what would it mean for the Hub

Proposal only. the owner rules naming and ontology; nothing below is
decided.

### the vocabulary as it stands

Four camp answers exist. A **guarantee** — the language promises one
behaviour, like rust's `wrapping_add`. An **anti-guarantee** — go's
deliberately randomised map iteration, a promise OF unpredictability,
where the language spends work at RUNTIME to make sure you cannot
rely on an order. **Compile-time refusal** — "it does not build" as a
first-class answer beside a value and a raise. And **`unspecified`**
— rust's bare `+` on integers, where the developer did not choose an
add guarantee at all and the ledger records that they did not.

### what the measurements say about which one fits

Four measured facts decide this, and no two of them point the same
way.

**The developer chose.** Typing `algebraic_add` instead of `+` is a
deliberate act with a name on it. That is the exact opposite of
`unspecified`, whose whole content is "the developer typed the
neutral spelling and made no choice". Whatever this is, it is not
`unspecified`.

**The variability lives in the build, not the run.** `twice.same_build`
agreed with itself in all four builds; the answer changed only when
the compiler flags changed, including `-C target-cpu=native` changing
it again on its own. Go's map iteration varies inside one binary, on
purpose, on every loop. These are different phenomena, so this is not
an anti-guarantee either — nothing here spends work to make you
unable to rely on an answer; the compiler is simply released from
having to preserve one.

**Something IS guaranteed, and it is a set.** The promise is not
"anything"; it is "a value obtainable by applying real-number algebra
to this expression, with each individual step still an IEEE
operation". `loopmul` reaching `inf` is inside that set; a NaN out of
`3.5 + 1.25` would not be. And the parts that are NOT released stayed
put: every NaN, infinity and negative-zero probe was bit-identical to
the ordinary operator at every optimisation level. So this is a
guarantee whose content is a permitted SET of answers rather than a
single answer.

**The census already has the machinery for it.** The record-both-modes
rule was made for rust's debug/release split, and the spike used it
untouched: F-f2.f is 1.0 in debug and 2.0 in release, and `compare.py`
scored both CONFIRMED without a code change.

### the proposal

None of the four fits, and the gap is narrow and nameable: a
guarantee that names a SET of acceptable answers, chosen deliberately
by the developer, with the pick inside that set made by the build
rather than by the run. Proposed, for the owner's ruling, as a **fourth
guaranteed arithmetic mode alongside `wrapping`, `growing` and
`approximating`** — and named by the same principle the owner used when he
named `approximating`, which is to say named for what happens to the
ANSWER rather than for the mechanism that produced it. On that
principle the candidate word is **`rearranging`**: the answer is one
of the answers a rearrangement of the expression can produce.

Two things to note against it. The origin-naming rule would instead
take rust's own word, `algebraic`; that reads as the mechanism rather
than the answer, so the two rules pull apart here and the owner should
break the tie. And `approximating` was ruled onto integer's page for
php's float promotion; if `rearranging` is accepted, the float page
gains its first mode entry and the two pages start sharing a mode
vocabulary — which may be a feature or may be a sign the modes belong
somewhere above both pages.

### what it would mean for the Hub

**Can a dominant operation be non-deterministic? Yes, if the ledger
records the permitted SET rather than the answer.** The guarantees
rule already says the Hub models every fracture as the set of
guarantees the languages make. A guarantee that names a set of
answers is still a guarantee; it is just weaker. The dominant float
add would carry a mode whose contract is "any rearrangement", and a
probe judge for that mode checks membership in the set rather than
equality to one value. Nothing in the ratified pipeline forbids this
— the two-build ANCHOR/SHIP discipline (optimizer off, optimizer on)
already compiles every probe twice, so the pipeline is ALREADY set up
to see exactly this difference. What it does not yet have is a place
to record "these two differ and that is allowed".

**What ingress records when a source calls `algebraic_add`:** the
`rearranging` add (or whatever the owner names it), NOT `unspecified`, and
not the ordinary add. The developer chose, statically, by writing the
name; declared types are the context, and here the spelling is the
declaration. The `unspecified` flag stays reserved for rust's bare
`+` on integers, where no choice was made.

**What egress may then do, stated as a directional bridge.** An
ordinary `+` is one valid arrangement — the identity arrangement — so
an ordinary add always satisfies a `rearranging` caller. The bridge
runs one way: `rearranging` may be egressed to any target language's
ordinary `+` losslessly with respect to the contract, while an
ordinary `+` may NOT be egressed as `algebraic_add`, because that
would hand the compiler a permission the source never granted. That
is the same shape as the existing dominance relation — X answers
everything Y's callers ask, plus more — and it means the new mode
costs egress nothing in eleven languages.

**One consequence worth flagging.** If the Hub carries a mode whose
answer depends on the build, then the reconstruction oracle
(source → ledger → equivalent source → ledger → identical equivalent
source) must compare LEDGERS, not run outputs, on any program using
it. The ledger is stable; the numbers are not. That is fine, and it
is the objective as stated, but it is the first mode where the
distinction bites.

---

## 5. The payoff — what to automate so the next update is cheaper

Ranked by measured cost against measured value.

| rank | build this | measured cost | what it buys, measured |
|---|---|---|---|
| 1 | **a release watcher per language**: fetch the project's release notes and the standard library's stability attributes, diff against the last sweep, emit a named list | ~40 lines of python, 2.1 s per language per run, 2 network fetches. Already written and run in this drill | turns "nothing notices" into 23 named items for rust 1.98.0, of which the 5 float methods are found by name from two agreeing sources. This is the ONLY thing in the drill that closes the detection gap |
| 2 | **the reverse direction on `operator_arity.py`**: after `--crosscheck`, take the set difference grammar-minus-table and print it | a few lines inside a function that already computes both sets | today rust has 129 grammar anonymous kinds the table never sees; a grammar bump that ADDS an operator is currently silent |
| 3 | **make `generate_run.py` a fixed point on its own lane**, and add a check that regenerating a committed lane produces that lane | one regenerate-and-diff step in the check sweep | measured drift today is 126 lines on `lane_bf.sh` alone; regenerating right now would silently DROP a `<compile-error>` verdict refinement in 24 places |
| 4 | **replace the differential alphabet's transcribed constant with a fetched, cached, fetch-dated file** | 2 `curl` calls plus the diff already demonstrated here | the constant survived this release by luck (62 variants both versions, all 53 names still present). The next release may not be so kind, and nothing would say so |
| 5 | **write the opacity convention once, for all twelve**: a per-language "make this value opaque" helper in the runner templates, beside the existing `d(x)`/`one()` helpers | 1 line per language template, 12 lines total, plus a paragraph in the vectors conventions | without it the census cannot probe ANY optimiser-visible behaviour in ANY language. It cost 4 sandbox iterations to discover here; it should cost zero the next time |

### if all twelve languages update once a year, what does that cost us today, and what could it cost

**Today, the honest answer is that it costs nothing and buys nothing,
and that is the problem.** Zero of the shape-layer checks can see a
release, by construction: two read a pinned grammar package and one
reads a constant typed by hand on a stated date. The censuses are
hand-drafted work orders. So twelve releases a year produce twelve
silent events, and the censuses gradually describe last year's
languages while every check stays green. The drill's own evidence for
this is that the ONLY automatic detection that fired was rustc
refusing 39 times — and it only fired because a person had already
written the new names into a file by hand.

**With item 1 in place**, a full sweep of twelve languages costs
about 25 seconds of machine time and 24 network fetches, and produces
twelve named diffs. rust's diff was 23 items. Assuming the same order
for the others, that is roughly 250 candidate items a year, and the
census's six data structures touch a minority of them — for rust
1.98.0, 5 of 23 items, or 22%. So call it 25 to 55 items a year that
need a person's judgement.

**What each of those costs, at the rate this drill measured:** 193
lines across 2 files for 5 methods on 1 page in 1 language, with zero
tool changes. That scales to roughly 1,000 to 2,000 lines of vector
and preamble authorship a year across the twelve — real work, but
bounded, reviewable, and entirely inside the two file types the
harness already reads. The pipeline code itself needed no change at
all, which is the strongest single result in this drill: the harness
absorbed a genuinely new kind of language behaviour without one line
of tool edit.

**And the toolchain cost is negligible**: 86 seconds and one command
per language per year, with one pin line per language to bump. Twelve
languages is under twenty minutes a year of installing.

The shape of the answer, then: the expensive part is not the code and
not the toolchain — it is NOTICING, which today costs infinity because
it never happens, and which item 1 makes cost two seconds.

---

## 6. Open items and what could not be verified

- **The lane used was Airlock, not SandboxDesign.** The brief named
  `SandboxDesign/agent/drop/`. A ping dropped there sat unrun for
  over a minute and its last recorded run is 2026-08-22; Airlock's
  last run is 2026-08-26 and it answered in 6 seconds. AgentMemory
  records the migration and warns the two share container names, so
  only one may run. Every script was authored into
  `SandboxDesign/agent/drop/` as the brief asked and copied to
  `Airlock/agent/drop/` to execute. **the owner's awareness needed: is
  SandboxDesign's daemon meant to be down?**
- **No allowlist change is required.** `.rust-lang.org` was already
  present in both allowlists and `static.rust-lang.org` answered 200.
  **No `allow.sh sync` is needed for this drill.**
- **The container image was not rebuilt and the pin was not bumped.**
  1.98.0 lives in `/persist/rustup076`, which survives container
  restarts but is not part of the image. If `/persist` is ever wiped
  the toolchain is gone. Bumping `Airlock/Containerfile` line 82 is
  the owner's call, and would replace 1.96.1 rather than co-install.
- **typescript could not be re-measured.** It ran on 2026-08-14 and
  is absent from the container today, taking the census's only
  recorded REFUTED cell (bool-U4, TS2367) with it. Unverified whether
  this is deliberate.
- **csharp and dart remain blocked** exactly as the recorded run
  says: csharp blocked-deliberate, dart blocked-on-allowlist-sync.
  Not pursued.
- **Within-one-binary non-determinism was not observed.** Every build
  answered the same expression identically twice. A sample refutes
  and never proves, so this is recorded as not-observed, not as
  refuted. It matters to layer D's argument and deserves a wider
  probe if the owner wants the classification to rest on it.
- **f16 and f128 could not be measured** because the types are still
  unstable at 1.98.0 (E0658, issue #116909). The methods presumably
  behave the same way there; unverified, and unverifiable on stable.
- **`mul`, `div` and `rem` were not shown to move.** Probes F-f2.h,
  .i and .j gave the same answer in both build modes; the C2
  standalone probe DID move `mul` to `inf` at O3, so the harness-shaped
  probe for it is simply not yet sharp enough. Two of five methods
  are demonstrated build-sensitive inside the harness; three are
  demonstrated build-sensitive only outside it, for `mul`, and not at
  all for `div` and `rem`.
- **The spike is not installed.** `vectors_boolean_float.json` and
  `templates/rust.boolean_float.pre` were written and run only in a
  scratch copy. No census page was edited. F-f2 is a proposed
  fact id, not a ruled one. The proposed text survives verbatim
  inside `SandboxDesign/agent/drop/d76_spike3_198.sh`, which is the
  generated lane, so it can be reviewed or lifted without anything
  having been installed.
- **`hq.sh check` ends at 0 errors** (9 warnings, all pre-existing
  conformance gaps in PseudoCoup_v6 and PseudoIR named by the sweep
  itself).

---

## Artifacts

Scripts authored, all in `SandboxDesign/agent/drop/`
and executed from `Airlock/agent/drop/`:

| script | what it measured |
|---|---|
| `d76_ping.sh` | lane liveness, toolchain present, allowlist reachability |
| `d76_install.sh` | layer B: the release is real, the install cost |
| `d76_c2.sh` | layer C2: the five methods at four optimisation settings, plus the token.rs refresh |
| `d76_c1a_196.sh` | layer C1: `lane_bf.sh` byte for byte at 1.96.1 |
| `d76_c1b_198.sh` | layer C1: the same lane, one `PATH` line inserted, at 1.98.0 |
| `d76_pathcheck.sh` | proof the inserted line moves the compiler |
| `d76_spike_why.sh`, `d76_spike_why2.sh` | isolating the two conditions a probe needs |
| `d76_spike3_198.sh` | the spike lane, run for real. This file EMBEDS the proposed preamble verbatim, so the 193 lines of spike authorship are recoverable from it without any census file having been edited. An earlier attempt was refused by the compiler for declaring the probes' result type as `float` where the preamble returns a formatted string; the fix was one word per probe |
| `d76_derivable.sh` | how much of "what is new" is machine-readable |

Logs are under `Airlock/agent/logs/`, stamped
`20260829T17*`.
