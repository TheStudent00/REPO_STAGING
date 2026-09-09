# log 023 — layer 2: the representations, enumerated and audited

Date: 2026-08-17. Node:
`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_4_data_representation/CORE_0_3_4_data_representation.md`.
Artifacts: `PseudoCoupHQ/Research/data_representation/`.

---

## §1 — walkthrough, in plain words

Three cold words first, because they have been away for a while and a
definition does not survive a gap.

- **Layer 1** is the DATA: fixed content, no language, no dynamics —
  nothing, truth, whole number, fractional number, text, sequence,
  keyed grouping, nesting, identity marks. It was ruled on 2026-08-15
  and written down as one shared file,
  [data_layer1.json](file://PseudoCoupHQ/Research/data_representation/data_layer1.json).
- **Layer 2** is the REPRESENTATIONS: for each language, the ways a
  running program can HOLD that content — python's list and tuple and
  dict, rust's `Vec` and `[T; N]` and `HashMap`, go's slice and map and
  struct. That is what this log reports.
- **Layer 3** is the OPERATIONS: what a compiler can DO to a
  representation. It belongs to the co-node `kind_fuzz_clustering` and
  nothing here touches it.

What was done, in order.

First, the enumeration. For each of the twelve languages I wrote one
file listing, per layer-1 form, the shapes that language offers for
holding it — spelled as the compiler knows them, with the literal or the
constructor that builds one. Where a language offers several holders for
one form, all of them are listed, because that plurality is the point of
layer 2. Things whose content is behaviour — a function, a channel —
are excluded, as the node's definition requires.

Second, the audit. The question layer 2 has to answer is not "what
shapes exist" but "can this shape actually take the data". So a
generator reads the layer-1 data file, bakes its values into each
language as literals, and emits one tiny program per cell — a cell being
one (form, representation) pair. Each program builds the representation
holding that form's values and prints the content back out, one line per
probe, in the `FACT_ID|RESULT` convention the census harness already
uses. No probe parses the data file at run time; the values arrive as
source text, so a language needs no parser to take part.

Third, the ruling. Every cell was classified from what its programs
actually printed:

- **LOADS** — every probe built, ran, and gave the content back.
- **PARTIAL** — the base values loaded and some EDGE did not. The edge
  is named. A whole number that came back CHANGED counts here too:
  python's `ctypes.c_int64` accepted 9223372036854775808 without a word
  of complaint and returned -9223372036854775808. That is a loss, not a
  load.
- **REFUSES-behavioral** — the representation cannot hold that content
  by its own nature, and the refusal is what the representation IS: a
  32-bit whole number has no room for a 64-bit edge; a container with
  one declared element kind has no room for the mixed row; a holder that
  owns its elements cannot put one node in two positions.
- **REFUSES-gap** — content layer 1 says is loadable that NO
  representation of that form in that language could hold. This is the
  only verdict that would make layer 1 grow, so it is decided across a
  whole form rather than per cell.

The headline. **328 (form, representation) cells across the twelve
languages. 1,324 probes ran. 211 cells LOAD, 66 are PARTIAL, 18
REFUSE-behaviorally, and 33 could not be run at all — every one of those
33 is c#, whose toolchain is unreachable from our sandbox.** The audit
verdict on layer-1 completeness: **no REFUSES-gap was found anywhere.
Every form is held by at least one representation in every language that
ran. Layer 1 stands audited, unchanged.**

Two things are worth saying before the tables, because both are
mechanism rather than result.

- **Three defects in my own harness were found and fixed, and they were
  found because they produced results too good or too bad to believe.**
  Go refused its own `float64` base values — the cause was an unused
  `import "math"`, carried in for the NaN spelling, which go treats as a
  compile error; the generator now keeps only the imports a probe uses.
  Dart refused an entire keyed cell — the cause was that dart forbids
  declaring a class inside a function body, so all five of a cell's
  shapes sat in one shared block and the two deliberately unspellable
  field names poisoned the other three; the generator now gives each
  probe only the shape it names. And every representation whose name
  contains a bracket — rust's `[T; N]`, go's `[]T`, java's `long[]` —
  had its results silently replaced by the lane's fallback word, because
  the lane matched probe ids as patterns and `[...]` is a character
  class; matching is now by fixed string. Each fix is recorded in the
  generator's own docstring.
- **A refusal is only a finding if the spelling was fair.** Where a
  refusal turned out to be my spelling rather than the language's limit
  — tsc reporting a duplicate `Node` because the DOM library already
  owns that name; `Float.NaNf` produced by appending an `f` suffix to a
  spelling that already carried its own — the spelling was corrected and
  the lane re-run. Where the spelling was fair, the refusal stands and
  is reported below.

---

## §2 — how many ways each language can hold the data

Representation counts per layer-1 form. One row per language; the number
is how many distinct shapes that language offers for holding that form.

| language | nothing | truth | whole | fractional | text | sequence | keyed | nesting | identity | total |
|---|---|---|---|---|---|---|---|---|---|---|
| java | 3 | 2 | 6 | 3 | 4 | 6 | 5 | 3 | 4 | **36** |
| csharp | 3 | 1 | 5 | 3 | 4 | 6 | 5 | 3 | 3 | **33** |
| kotlin | 3 | 1 | 4 | 3 | 4 | 5 | 4 | 2 | 3 | **29** |
| dart | 3 | 1 | 3 | 2 | 4 | 5 | 4 | 3 | 3 | **28** |
| cpp | 3 | 1 | 4 | 2 | 3 | 6 | 3 | 2 | 3 | **27** |
| python | 1 | 1 | 4 | 3 | 3 | 5 | 4 | 3 | 3 | **27** |
| swift | 2 | 1 | 4 | 2 | 4 | 5 | 3 | 3 | 3 | **27** |
| typescript | 3 | 1 | 2 | 1 | 3 | 5 | 5 | 3 | 3 | **26** |
| ruby | 1 | 1 | 3 | 3 | 4 | 4 | 4 | 2 | 3 | **25** |
| rust | 2 | 1 | 4 | 2 | 3 | 5 | 3 | 2 | 3 | **25** |
| go | 2 | 1 | 4 | 2 | 3 | 4 | 2 | 2 | 3 | **23** |
| php | 1 | 1 | 3 | 1 | 3 | 4 | 4 | 2 | 3 | **22** |
| **all 12** | 27 | 13 | 46 | 27 | 42 | 60 | 46 | 30 | 37 | **328** |

Full detail — every representation's spelling, kind (literal or
constructor) and one-line note — is in
`PseudoCoupHQ/Research/data_representation/representations_<language>.json`.

Two shapes of the table worth naming. **Sequence is the most crowded
form (60 of the 328 cells)**, because every language offers several
ordered runs that differ in whether the length is fixed, whether the
element kind is declared, and whether the run owns its elements. **Truth
is the emptiest (13)**, because nearly every language has exactly one
way to hold two values.

---

## §3 — the audit, per language

| language | cells | LOADS | PARTIAL | REFUSES-behavioral | NOT-RUN | probes |
|---|---|---|---|---|---|---|
| java | 36 | 24 | 10 | 2 | 0 | 161 |
| python | 27 | 23 | 3 | 1 | 0 | 126 |
| typescript | 26 | 23 | 1 | 2 | 0 | 109 |
| ruby | 25 | 22 | 2 | 1 | 0 | 118 |
| dart | 28 | 19 | 8 | 1 | 0 | 122 |
| kotlin | 29 | 19 | 8 | 2 | 0 | 131 |
| cpp | 27 | 18 | 8 | 1 | 0 | 119 |
| php | 22 | 17 | 1 | 4 | 0 | 100 |
| rust | 25 | 16 | 7 | 2 | 0 | 113 |
| swift | 27 | 16 | 10 | 1 | 0 | 122 |
| go | 23 | 14 | 8 | 1 | 0 | 103 |
| csharp | 33 | 0 | 0 | 0 | 33 | 0 |
| **all 12** | 328 | 211 | 66 | 18 | 33 | 1,324 |

Per-cell detail with the printed result of every probe is in
`PseudoCoupHQ/Research/data_representation/audit/audit_<language>.json`;
the raw `FACT_ID|RESULT` lines are in `audit/raw/l2_<language>.txt`, and
the scripts that produced them in `audit/lanes/`.

**c# is NOT-RUN, and the reason is ours, not the language's.** The
sandbox's package proxy refuses `dot.net` (`CONNECT tunnel failed,
response 403`) and `apt-get update` dies against it, so no mono and no
dotnet SDK could be installed. Its 33 cells are enumerated and its
programs are generated and waiting; only the running is missing.

### every non-LOADS cell, by cause

**Cause 1 — a fixed-width whole number meeting a wider edge.** The
representation states its width; the data file's edges are chosen to
cross it. Two different manners of refusal, and the difference matters:

- the compiler REFUSES the literal — go `int32`, `int64`, `int`; java
  `short`, `int`, `long`, `Integer`, `Long`; kotlin `Int`, `Long`; rust
  `i32`, `i64`; swift `Int`, `Int32`, `Int64`; dart `int`. All PARTIAL:
  base values load, the named edges do not.
- the value is TAKEN and silently CHANGED — cpp `int32_t` (i64max came
  back as `-1`) and `int64_t` (i64max_plus1 came back as
  `-9223372036854775808`); python `ctypes.c_int64` (same wrap); php
  `int` (i64max_plus1 came back as the float `9.2233720368548E+18`);
  typescript `number` and dart `double (whole number)` (both eroded
  every edge past 2^53). All PARTIAL, and the more dangerous half of the
  cause, since nothing announces the loss.

**Cause 2 — a container with one declared element kind meeting the
mixed row or the big-integer element.** cpp `std::vector`, C array,
`std::array`, `std::deque`, `std::list`; go `[]T`, `[N]T`, `[]any`,
`container/list.List`; rust `Vec<T>`, `[T; N]`, `&[T]`, `VecDeque<T>`;
swift `Array`, `ArraySlice`, `ContiguousArray`, `Set`, tuple; dart
`List<T>`, fixed-length `List`, `Set<T>`, `List.unmodifiable`, record;
kotlin `List`, `MutableList`, `Array<T>`, `ArrayDeque`; java `long[]`,
`List.of(...)`, `ArrayDeque<T>`. All PARTIAL. Two in this group refuse
outright rather than partially, because the base row already breaks
them: kotlin `IntArray` and python `array.array` — both are REFUSES-
behavioral, since they cannot even hold `["a", "b"]`.

**Cause 3 — a shape whose field names are fixed when the shape is
written, meeting the odd keys.** The data file's keyed edges include the
key `"1"` and the empty key `""`, and neither is spellable as a field
name. cpp `struct`, go `struct`, rust `struct`, swift `struct` and
`class`, dart `class with fields`, java `local class with fields`,
python `collections.namedtuple`, ruby `Struct`, kotlin `data class`. All
PARTIAL — the flat and nested groupings load; the two odd keys do not.

**Cause 4 — an exact holder meeting the non-finite fractional values.**
An exact ratio or exact decimal has no room for NaN or infinity: python
`fractions.Fraction`, ruby `Rational`, java `BigDecimal`, kotlin
`BigDecimal`. All PARTIAL.

**Cause 5 — a run-time refusal of a typed binary run.** typescript
`BigInt64Array` refuses strings and the mixed row at run time
(`TypeError: Cannot convert ... to a BigInt`) — REFUSES-behavioral.

**Cause 6 — an extension that is not installed.** php `GMP`, php
`BCMath` and php's mbstring codepoint array all threw `Error` on every
probe, including the base values — REFUSES-behavioral, but the honest
reading is that these three representations exist in php and not in this
container. Their cells should be re-run wherever those extensions are
present before anything is concluded about php's whole-number reach.

**Cause 7 — identity.** Nine cells refuse to hold one node in two
positions. They are §4's subject and are not repeated here.

---

## §4 — the identity findings

This is new measured ground: which representations can hold a shared
node — two positions, one object — and which can hold a cycle.

Reading the table: **shared node** says what happened when one object
was placed in two positions and changed through the first — `shared`
means the change was visible through the second and the two positions
were one object; `shared-read-only` means the two positions were one
object but nothing could be changed through them; `copied` means the
second position held its own object. **diamond** says whether two
positions naming one id were one object. **cycle** says whether a node
ended up containing itself.

| language | representation | shared node | diamond | cycle |
|---|---|---|---|---|
| cpp | `std::vector<T> (owned elements)` | copied | distinct | compile-error |
| cpp | `std::shared_ptr<T>` | shared | same | cycle |
| cpp | `T* (raw pointer)` | shared | same | cycle |
| csharp | `struct value holder` | not run | not run | not run |
| csharp | `class reference holder` | not run | not run | not run |
| csharp | `array of references` | not run | not run | not run |
| dart | `List of object references` | shared | same | cycle |
| dart | `copying holder (List.from)` | copied | distinct | no-cycle |
| dart | `class instance holder` | shared | same | cycle |
| go | `[]T (slice value, owned)` | copied | same | no-cycle |
| go | `*T (pointer)` | shared | same | cycle |
| go | `[]*Node (slice of pointers)` | shared | same | cycle |
| java | `Object[] of references` | shared | same | cycle |
| java | `record holding a reference` | shared | same | cycle |
| java | `value-copying record (primitives)` | copied | distinct | no-cycle |
| java | `long[] value array` | copied | distinct | no-cycle |
| kotlin | `MutableList<MutableList<T>> (shared reference)` | shared | same | cycle |
| kotlin | `data class holding a reference` | shared | same | cycle |
| kotlin | `data class of primitives (value holder)` | copied | distinct | aborted |
| php | `array holder (value semantics)` | copied | distinct | cycle |
| php | `object holder (reference semantics)` | shared | same | cycle |
| php | `ArrayObject holder` | shared | same | cycle |
| python | `list` | shared | same | cycle |
| python | `dict` | shared | same | cycle |
| python | `tuple` | shared | same | cycle |
| ruby | `Array (object references)` | shared | same | cycle |
| ruby | `dup / Marshal round trip (copying holder)` | copied | distinct | cycle |
| ruby | `Hash (object held under two names)` | shared | same | cycle |
| rust | `Vec<T> (owned elements)` | copied | distinct | compile-error |
| rust | `Rc<T>` | shared-read-only | same | compile-error |
| rust | `Rc<RefCell<T>>` | shared | same | cycle |
| swift | `struct value holder` | copied | distinct | compile-error |
| swift | `class reference holder` | shared | same | cycle |
| swift | `array of class references` | shared | same | cycle |
| typescript | `object references in an array` | shared | same | cycle |
| typescript | `spread-copy holder` | copied | distinct | no-cycle |
| typescript | `Map holding one object twice` | shared | same | cycle |

**Counted: of the 34 identity cells that ran, 23 hold a shared node and
24 hold a cycle.** Every one of the eleven languages that ran has at
least one representation for each, so identity marks are held everywhere
— but never by every representation, which is the finding.

The five things this table shows that a type table could not.

- **The split is between holders that OWN their elements and holders
  that REFER to them, and it is the same split in every language.** An
  owning holder answered `copied` in every case: cpp `std::vector`, rust
  `Vec`, go's slice value, java's primitive record and `long[]`, swift's
  struct, kotlin's data class of primitives. A referring holder answered
  `shared` in every case: pointers, `shared_ptr`, `Rc<RefCell<T>>`,
  object references, `*T`.
- **Rust's `Rc<T>` is the one representation that holds sharing but not
  editing.** It answered `shared-read-only`: two positions genuinely
  name one object, and nothing can be changed through them, so the data
  file's shared-node note ("edit through left, read through right") can
  only be half-answered. `Rc<RefCell<T>>` answers it whole. This is the
  clearest evidence in the whole audit that "can it hold the shape" and
  "can the shape be observed" are two questions.
- **A cycle costs strictly more than sharing, and rust prices it
  visibly.** `Rc<T>` holds sharing and its cycle attempt is refused by
  the compiler; only `Rc<RefCell<T>>` — counted sharing plus permission
  to change what is shared at run time — holds a cycle. cpp and swift
  show the same order in a coarser form: the owning holder's cycle
  attempt does not compile, the reference holder's does.
- **php's array is the odd one and it is genuinely odd.** It answered
  `copied` for the shared node (php arrays copy on assignment) and
  `cycle` for the cycle, because a php array can be made to contain
  itself through a reference (`$v["self"] = &$v`). It is the only
  representation measured that holds a cycle while refusing a shared
  node. That is not a mistake in the probe; it is what php's two kinds
  of assignment do.
- **go's slice value answered `copied` for the shared node but `same`
  for the diamond.** Two slice values copied from one slice are distinct
  values that point at one backing store, so the sharing question has
  two different answers depending on whether you ask about the holder or
  what it holds. Layer 3 will have to keep those apart.

Two entries in the table are weaker evidence than the rest and are
marked here rather than buried: java's `value-copying record` and
`long[]` answer `no-cycle` by assertion in the probe rather than by an
attempt the compiler refused, and ruby's `dup / Marshal round trip`
answers `cycle` because `Marshal` preserves a self-reference through the
copy — true, and a different fact from the others in that column.

---

## §5 — the layer-1 audit verdict

**No REFUSES-gap was found. Layer 1 stands audited and does not grow.**

The rule the node set was that every "no" is either behavioral —
expected from what the representation IS, and filed to layer 3 — or a
genuine gap, meaning content the model says is loadable that nothing can
hold. All 84 non-loading cells (66 PARTIAL + 18 REFUSES-behavioral) are
of the first kind, and each one's cause is named in §3. For every one of
the nine layer-1 forms, in each of the eleven languages that ran, at
least one representation LOADS it outright.

One boundary on that verdict, stated rather than left implied: c#'s 33
cells did not run, so the verdict covers eleven languages of twelve. C#
is unlikely to change it — every form it enumerates has several holders
— but it has not been measured, and this log does not claim it has.

---

## §6 — what layer 3 inherits

`kind_fuzz_clustering` fuzzes layer-3 operations over (data,
representation) pairs. The audit says which pairs are real.

- **211 cells LOAD outright.** That is the clean input space: a
  representation, a form, and evidence that it holds the content.
- **66 more are PARTIAL**, which means they hold the BASE values and
  refuse a named edge. They are usable inputs as long as the edge that
  refused is excluded per cell — the exclusion is written into each
  cell's `why` field in `audit/audit_<language>.json`. **Counting these,
  layer 3 inherits 277 (form, representation) pairs.**
- **18 cells REFUSE-behaviorally** and are not layer-3 inputs at all;
  they are the boundary of the input space, and three of them (php's
  GMP, BCMath and mbstring codepoint array) should be re-measured
  wherever those php extensions are installed before being written off.
- **33 c# cells are pending a toolchain**, generated and unrun.

The pairs are not a new artifact: layer 3 reads them from the twelve
`audit_<language>.json` files, where each cell carries its form, its
representation, its verdict, and the printed result of every probe.

---

## Postscript — 2026-08-17, gap-closing follow-up

Two measurement gaps stood after the audit above: php's three
extension-gated representations (Cause 6), and c#'s 33 unrun cells
(§3). Both were checked, not assumed.

**c# — still blocked; verified, not fixed.** Before touching anything,
a one-shot probe from the agent lane tried `https://dot.net`,
`https://dotnet.microsoft.com`, and
`https://dotnetcli.blob.core.windows.net` through the proxy; all three
came back `000` (no connection), so dot.net is still refused after
the owner's `allow.sh` + `allow.sh sync`. `proxy/allowlist.txt` (instance
state, not committed) now has a `.NET SDK` block appended: `.dot.net`,
`.microsoft.com`, `.azureedge.net`, `.dotnetcli.blob.core.windows.net`,
`.builds.dotnet.microsoft.com`, `.download.visualstudio.microsoft.com`
— `dotnet-install.sh` and the runtime/SDK payloads it fetches pull from
several of these, not just `dot.net` itself. **the owner needs to run
`bash SandboxDesign/allow.sh sync` again before the SDK
install can be retried.** No install was attempted against a blocked
proxy, and this session did not loop waiting on the sync — c#'s 33
cells remain generated and unrun.

**php — closed.** `apt-get install -y php8.5-gmp php8.5-bcmath
php8.5-mbstring` (package names adjusted for the container's php 8.5,
`php-gmp` etc. unversioned aren't resolvable) needed two workarounds
to run at all: `-o APT::Sandbox::User=root`, because apt's privilege
drop to the `_apt` user fails under this rootless container's user
namespace (`setgroups`/`setegid`/`seteuid` all `EPERM`); and
`-o Dir::Cache::Archives=/work/apt-cache/archives`, because the image's
own `/var/cache/apt/archives/partial` is owned by a uid outside the
container's mapped range and even root here cannot chown or write into
it. Neither is a php problem; both are sandbox-container quirks worth
folding into `SandboxDesign` generally if apt keeps coming up this way.
`php -m` confirmed `bcmath`, `gmp`, and `mbstring` all present after
install. The `l2_php.sh` lane was re-run whole (all 100 probes, not
just the three affected cells — the lane has no finer grain) and
`audit_classify.py` re-run over the refreshed raw output.

**php's three verdicts, before -> after:**
- `whole.GMP (ext-gmp)`: REFUSES-behavioral -> **LOADS** (base values
  and both edges — `i64max_plus1`, `u64max` — all held exactly).
- `whole.BCMath string-carried number (ext-bcmath)`: REFUSES-behavioral
  -> **LOADS** (same edges, held as exact decimal strings).
- `text.array of codepoints (mbstring)`: REFUSES-behavioral -> **LOADS**
  (all five text probes, including the astral codepoint `𝄞` and the
  escape-heavy string, printed back cleanly).

No new PARTIAL edges were named by this re-run — the three cells moved
straight to LOADS. php's `whole.int` PARTIAL (float erosion past
2^53) and its `identity.array holder (value semantics)`
REFUSES-behavioral (copies on assignment, so it cannot hold a shared
node or a diamond) are unchanged and are genuine language findings,
not extension gaps.

**Counts, whole audit, before -> after this postscript:**

| verdict | before | after |
|---|---|---|
| LOADS | 211 | **214** |
| PARTIAL | 66 | 66 |
| REFUSES-behavioral | 18 | **15** |
| NOT-RUN (c#) | 33 | 33 |
| **total cells** | 328 | 328 |

php's own row: 22 cells, was 17 LOADS / 1 PARTIAL / 4
REFUSES-behavioral, now **20 LOADS / 1 PARTIAL / 1 REFUSES-behavioral**.

**The §5 layer-1 verdict, restated plainly: it does NOT yet cover
twelve languages of twelve.** php's extension re-run changes php's own
row but does not touch coverage, because php had already run and
contributed to the verdict before this postscript — closing its
extension gap firms up php's PARTIAL/REFUSES-behavioral detail, it does
not add a language. c# is still the one language that has not run at
all. **The verdict remains: no REFUSES-gap was found in the eleven
languages of twelve that ran; c#'s 33 cells are generated and waiting
on the sandbox proxy sync above.** Layer 1 stands audited and
unchanged either way, since c#'s enumeration offers several holders for
every form and is not expected to change the verdict — but, as before,
this log does not claim what has not been measured.

---

## Postscript 2 — 2026-08-17, c#'s gap closed

the owner ran `allow.sh sync` after the first postscript. This entry verifies
the sync, installs the toolchain, runs c#'s 33 waiting cells, and folds
them into the whole-audit count.

**dot.net — reachable now.** A one-shot lane probe (`curl -sSI --max-time
15`) hit `https://dot.net` (301), `https://dotnetcli.blob.core.windows.net`
(400), `https://dotnet.microsoft.com` (302), and
`https://builds.dotnet.microsoft.com` (400). None of these is a clean
200, but none is `000` either — every one is a real HTTP response from
the far end, which is the only thing this step needed to know. The
proxy sync worked; the earlier `CONNECT tunnel failed` block is gone.

**Install — succeeded, with one sandbox-container quirk, same shape as
php's.** `dotnet-install.sh --install-dir /persist/dotnet --channel LTS`
downloaded a 240 MB SDK payload cleanly, but its own `tar` extraction
reported `Cannot change ownership to uid 2001, gid 2001: Operation not
permitted` on every entry under `sdk-manifests/` — the mono, emscripten
and iOS/Android/macOS/tvOS workload manifests, none of which this audit
needs — and exited nonzero. The core SDK (`dotnet`, the Roslyn compiler,
the `Microsoft.NETCore.App` runtime and reference-assembly pack)
extracted before the failing entries and is intact: `dotnet --version`
reports `10.0.400`, `dotnet --list-sdks` shows `10.0.400
[/persist/dotnet/sdk]`. This is the same rootless-container ownership
quirk `SandboxDesign` already carries a note about from the php
extension install — worth generalizing there rather than re-discovering
per language.

**A second, real gap and how it was closed.** `dotnet run Program.cs`
(the SDK's single-file run path) does not just compile and run — it
restores from NuGet first, even for a program with zero package
references, and `api.nuget.org` is not on the allowlist (and does not
need to be, for probes that touch nothing but the base class library).
That path was abandoned rather than requesting another allowlist entry
for a dependency the probes do not have. Instead, two small persistent
helper scripts were written to `/persist/dotnet-csc-build.sh` and
`/persist/dotnet-csc-run.sh`: the build script invokes the SDK's own
Roslyn compiler directly (`dotnet exec .../Roslyn/bincore/csc.dll
-target:exe -reference:<every dll in the installed
Microsoft.NETCore.App.Ref pack> Program.cs`), and the run script writes
a hand-built `prog.runtimeconfig.json` naming the installed runtime
version and then runs the produced assembly with `dotnet prog.dll`.
Neither step touches the network. `audit_generate.py`'s `RECIPE["csharp"]`
and `PRESENCE["csharp"]` were updated to call these two scripts instead
of the placeholder `mcs`/`__ABSENT__` pair, and `l2_csharp.sh` was
regenerated from the updated generator before running — it carries the
three inherited defect fixes (pruned imports, per-probe shape isolation,
fixed-string lane matching) unchanged, since none of those live in the
recipe.

**The run.** `l2_csharp.sh`, 33 cells / 150 probes, ran whole in the
agent lane (73s). `audit_classify.py csharp` ruled: **20 LOADS, 11
PARTIAL, 2 REFUSES-behavioral, 0 NOT-RUN.** Full detail in
`Research/data_representation/audit/audit_csharp.json`; raw output in
`audit/raw/l2_csharp.txt`.

The two REFUSES-behavioral cells: `sequence.ValueTuple` (refuses its own
`empty` probe — `ValueTuple.Create()` with zero elements is not valid
c# syntax for the zero-arity case this probe spells — and refuses
`bigint`, since a tuple element typed for the base row's `int` cannot
also hold a beyond-i64 value without every position being re-typed
`object`) and `identity.struct value holder` (a value type has no
reference identity at all — no shared node, no diamond, no cycle are
even expressible; this is the same "owning holder answers `copied`"
family every other language's value-typed holders fell into in §4, not
a new kind of finding).

**Identity, c#'s contribution.** `class reference holder` and `array of
references` both answered `shared` / `same` / `cycle` on all three
probes — c# joins the "referring holder shares" side of §4's split with
no surprises. `struct value holder` is REFUSES-behavioral rather than
`copied`-with-an-answer, because none of the three probes could even be
spelled (three `<compile-error>`, not three printed judgements) —
weaker evidence than java's and kotlin's value-copying holders, which
at least ran and printed `copied`; noted here rather than smoothed into
the same row as those.

**form_verdicts for c#: all nine held.** No REFUSES-gap. c#'s 33 cells
close out exactly as the eleven already-run languages did — every
layer-1 form has at least one c# representation that loads it outright.

**Whole-audit totals, before -> after this postscript:**

| verdict | before (postscript 1) | after (postscript 2) |
|---|---|---|
| LOADS | 214 | **234** |
| PARTIAL | 66 | **77** |
| REFUSES-behavioral | 15 | **17** |
| NOT-RUN | 33 | **0** |
| **total cells** | 328 | 328 |

**The §5 layer-1 verdict, now stated as closed: coverage is twelve
languages of twelve. No REFUSES-gap was found in any of them. Layer 1
stands audited, complete, and unchanged.** This is the first point in
the whole audit where that sentence can be written without a boundary
attached — c# was the last of the twelve, and it is measured now, not
generated-and-waiting.
