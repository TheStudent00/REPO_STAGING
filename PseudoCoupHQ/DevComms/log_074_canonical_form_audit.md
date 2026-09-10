# log_074 — forensic audit: is matching decided by THE CANONICAL RUNNABLE FORM

Scope: `PRIVATE/PseudoCoupHQ/Research/op_pipeline`. Method: direct
reads of the pipeline's own code and JSON artifacts, plus file mtimes —
no code was run, no artifact was regenerated, nothing was fixed.
Every number below is either quoted from a JSON artifact's own
recorded field, or computed by this audit directly from an artifact
using a rule quoted from the artifact's own producing code — the two
are labelled separately every time, per §5.1 of
`PRIVATE/DevComms/LLM_communication_protocol_v2.md`.

## Walkthrough

The canonical runnable form exists, is measured, and is verified
against a real assembler — but it is a MINORITY input to matching, not
the material matching runs on. The two matching passes that founded
the pipeline (`match_units.py`, step 6, and `verdicts.py`, step "the
judge") were written and run on 2026-08-25 at 06:36–06:44, comparing
raw pre-canonical compiler bytes and a non-runnable lifted-expression
string — nearly eighteen hours BEFORE `canon.py` (which builds THE
CANONICAL RUNNABLE FORM) was written at 23:28 the same day. Every
later layer added new comparison material — canonical bytes
(2026-08-25 23:30), the move-erased pseudo-step notation
(2026-08-26 21:56), a z3-normalized expression tree
(2026-08-27 11:26) — but none of them replaced the founding two, and
the newest, most complete runnable-text field the pipeline owns
(`canon2.py`'s `derived_text`, built 2026-08-26 21:49 under the owner's
own 2026-08-26 amendment) is never read by any matching or
class-forming code anywhere in the directory — confirmed by grep, not
inference. Counting every pair of arch-units that ended up in the same
class in the final table, `dominant_table9.json`: 75.1% were decided
by raw pre-canonical compiler bytes, 23.0% by a non-runnable notation,
and 1.8% by the canonical runnable form. A concrete case,
`swift/op_150` (division) and `swift/op_186` (modulo), shows exactly
why this matters: their canonical runnable text is visibly different
(`idiv %esi; ret` vs `idiv %esi; mov %edx,%eax; ret`) and would have
kept them apart, but the pseudo-step notation used instead erases the
one instruction that carries the distinction, and the two units were
merged — and, by transitive closure through that merge, C's own
division and modulo (which the pipeline DOES keep apart when
compared directly) were pulled into the same 20-member class as well.

---

## 1. Inventory of forms

Every distinct representation of one arch-unit that exists anywhere in
the pipeline, read off the SAME unit, `c/op_246` (`a % b`, C, `int32_t
% int32_t`), wherever it appears; two units that don't reach a given
stage are noted where relevant.

- **Raw ship bytes/mnem** — `op_units_c.json`, field `probes["246"]["ship"]`, produced by objdump reading the compiler's optimized output directly. 750 probe records in the file; 610 of them ("`units_read`", `canon_units_c.json`) go on to be usable arch-units. RUNNABLE machine text (it is literally what the compiler emitted), but PRE-canonical — no register rename has happened yet.
  > `"mnem": ["mov %edi,%eax", "cltd", "idiv %esi", "mov %edx,%eax", "ret"]`
- **`canon.py`'s `canon_text`** — `canon_units_c.json`, field `units["246"].canon_text`. 610 units read per language file; THE CANONICAL RUNNABLE FORM itself (registers renamed to `a`→`%rdi`, `b`→`%rsi`, `result`→`%rax`, temps→`%r10`/`%r11`, ratified 2026-08-25). RUNNABLE — it is real AT&T assembler text, and `canon_roundtrip.json` proves it assembles.
  > `"canon_text": "mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret"`
  Here it happens to equal the ship mnem (`"already_canonical": true`) because `int32_t % int32_t`'s C ABI registers already match the canonical assignment; this is not true for every unit (598/610 C units canonicalise at all — see §3).
- **`canon2.py`'s `erased_form`** — `canon2_units_c.json`, field `units["246"].erased_form`. 610 units read; 596 erase successfully (`"erased_ok": 596`). NON-runnable — it names values (`a`, `b`, `u0`, `answer`), never a register, and is not assembler text.
  > `["u0 = cltd(a)", "u1, answer = idiv(u0:a, b)"]`
- **`canon2.py`'s `derived_text`** — same file, field `units["246"].derived_text`. RUNNABLE — literally re-derived AT&T text from the erased form plus the entry contract; for this unit it round-trips through a real assembler (`"roundtrip": {"assembled": true, ...}`).
  > `["mov %edi,%eax", "cltd", "idiv %esi", "mov %edx,%eax", "ret"]`
  Only 574/610 C units reach this (branching units are refused outright — canon2.py's own docstring: *"Branching units are SKIPPED outright with an honest per-unit record"*, `canon2.py` line 45).
- **`sem_anchored.py`'s lifted `sem.key`** — `sem_anchored_c.json`, field `units["246"].sem.key`. NON-runnable — a pyvex-lifted symbolic expression string over anchored operand names (`in0`, `in1`), block-structured.
  > `"B0 V[zx64(ex32@32(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64)))) zx64(ex32@32(DivModS64to32(...)))] S[] E[ret]"`
- **`core_modes.py`'s `core`** — `core_modes_c.json`, field `units["246"].core`. NON-runnable — the same pyvex lift, stripped of the anchoring wrapper, plus a separate `modes` list for fence/guard behaviour.
  > `"zx64(ex32@32(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64))))"`
- **`tree_match2.py`'s `normal_path_root`** — `tree_units2.json`, one record per unit (list, not dict, keyed by scanning `lang`+`n`). NON-runnable — a z3-`simplify()`-normalized bitvector expression, with any VEX operation the normalizer does not model replaced by an opaque `op_N` placeholder atom (mechanism detailed in §6/§7).
  > `"Concat(0, Extract(63, 32, op_3))"` (raw pre-normalization text: `"normal_path_raw": "zx64(ex32@32(DivModS64to32(...)))"`)

Total count of unit representations that exist for `c/op_246` across the pipeline: **7**, of which **3 are runnable machine text** (ship mnem, `canon_text`, `derived_text`) and **4 are non-runnable notations** (`erased_form`, `sem.key`, `core`, `normal_path_root`). Producing programs, in file order: `probe_gen.py`/objdump → `canon.py` → `canon2.py` (two fields) → `sem_anchored.py` → `core_modes.py` → `tree_match2.py`.

---

## 2. Which form each matching ground actually compares

`dominant_table9.json`'s own `evidence_order` field:

> `["byte", "canon-byte", "erased-form", "tree-exact", "sem", "core-text", "z3", "unclassified"]`

Each ground, the code that decides it, the literal comparison line, and the representation from §1 it uses:

| ground | producing code | literal comparison | representation compared | runnable? |
|---|---|---|---|---|
| `byte` | `verdicts.py` line 628 | `if left["bytes"] == right["bytes"]:` | raw ship bytes (`sem_anchored_*.json`'s `bytes` field, itself copied from `op_units_*.json`'s `ship.bytes`) | runnable, but PRE-canonical |
| `canon-byte` | `dominant_table2.py` lines 188–208, `canon_byte_edges()` | `b = units[uid].get("canon_bytes")` ... `key = " ".join(b)` | `canon_roundtrip.json`'s `canon_bytes` — the assembled bytes of `canon.py`'s `canon_text` | THE canonical runnable form |
| `erased-form` | `dominant_table_erased.py` lines 289–309, `load_erased_forms()` | `form = tuple(rec.get("erased_form") or [])` | `canon2.py`'s `erased_form` pseudo-steps | non-runnable |
| `tree-exact` | `dominant_table_tree.py` lines 122–162 | groups keyed on `u.get("normal_path_root")` | `tree_units2.json`'s z3-normalized root | non-runnable |
| `sem` | `verdicts.py` line 631 | `if left["sem"]["key"] == right["sem"]["key"]:` | `sem_anchored.py`'s lifted `sem.key` | non-runnable |
| `core-text` | `verdicts4.py` line 105, `relate()` | `same_core = ra["core"] == rb["core"]` | `core_modes.py`'s pyvex `core` string | non-runnable |
| `z3` | `dominant_table2.py` lines 166–185, `z3_edges()` | pulls `verdicts3b`'s rows where `ground.startswith("z3")` — z3 deduction runs over the `core`/lifted expressions | pyvex lift, z3-normalized | non-runnable |

`dominant_table.py` lines 213–225, `classify_ground()`, is the router that sorts a `verdicts3b` pair's recorded `ground` text into these buckets:

> ```
> if ground.startswith("byte identity"): return "byte"
> if ground.startswith("sem identity"): return "sem"
> if ground.startswith("z3"): return "z3"
> # verdicts3b had no identity ground for this pair, yet verdicts4's
> # column read the two records as totally equal.
> return "core-text"
> ```

Measured pair counts, `dominant_table9.json`'s `stats.member_pairs_by_evidence_ground` (recorded field, evidence class: quoted artifact stat):

| ground | pairs | share |
|---|---:|---:|
| byte | 3,142 | 75.11% |
| sem | 410 | 9.80% |
| erased-form | 238 | 5.69% |
| tree-exact | 267 | 6.38% |
| canon-byte | 77 | 1.84% |
| z3 | 47 | 1.12% |
| core-text | 2 | 0.05% |
| unclassified | 0 | 0.00% |
| **total** | **4,183** | 100% |

---

## 3. The scorecard

Grouping §2's seven grounds into the three categories the audit was
asked to separate — computed directly from the table above (evidence
class: arithmetic on quoted artifact stats):

- **Decided by THE CANONICAL RUNNABLE FORM** (`canon-byte` — `canon_text`/its assembled bytes): **77 pairs, 1.84%**.
- **Decided by a NON-runnable notation** (`erased-form` + `tree-exact` + `sem` + `core-text` + `z3`): 238+267+410+2+47 = **964 pairs, 23.05%**.
- **Decided by raw, pre-canonical compiler bytes** (`byte`): **3,142 pairs, 75.11%**.

The same split at the CLASS level, not the pair level — `dominant_table9.json`'s own `stats.weakest_evidence_distribution` (a class's weakest edge is the one the owner's ruling says the class's evidence marker must report):

> `{"sem": 32, "byte": 325, "tree-exact": 103, "erased-form": 62, "canon-byte": 26, "z3": 35, "core-text": 1, "None": 484}`

Of 1,068 final classes, 484 are singletons (no internal edge, `None`); of the 584 classes that DO carry an internal edge, only **26 (4.5%)** have the canonical runnable form as their weakest — i.e. as the WORST evidence any member pair inside them can point to.

**Units that HAVE a canonical runnable form at all**, per language — recorded fields, `canon_units_*.json`'s `units[n].canon_ok` and `canon2_units_*.json`'s `units[n].derived_text` (present as a list, vs. as the refusal string canon2.py writes for branching units):

| lang | units read | `canon.py` `canon_ok` | `canon2.py` `derived_text` present |
|---|---:|---:|---:|
| c | 610 | 598 | 574 |
| cpp | 770 | 762 | 700 |
| go | 107 | 49 | 77 |
| rust | 125 | 119 | 112 |
| swift | 167 | 161 | 124 |
| **total** | **1,779** | **1,689** | **1,587** |

go's collapse (49/107 `canon_ok`, 58 refused) matches AgentMemory's own
2026-08-26 amendment note verbatim: *"90 of 1,779 units, 58 of go's
107, fall back to the lifted string today for want of exactly this"* —
confirmed directly against `canon_units_go.json`.

**How many of the units that DO have a canonical runnable form never took part in a canon-byte edge** — this number is NOT recorded anywhere in the artifacts; it is computed by this audit directly from `canon_roundtrip.json` (`canon.py`'s assembled bytes) and `canon_units_*.json` (for the operand-type-pair half of the class key), replicating `dominant_table2.py`'s own grouping rule quoted in §2 (`canon_byte_edges()`), gated on `(canon_bytes, type_pair)` — a slightly looser gate than the real class key, which also requires matching result type, so this UNDERCOUNTS the true "never-in-edge" figure:

| lang | units with `canon_bytes` (assembled) | never share their group with another unit |
|---|---:|---:|
| c | 564 | 234 |
| cpp | 716 | 134 |
| go | 45 | 21 |
| rust | 115 | 10 |
| swift | 122 | 41 |
| **total** | **1,562** | **440 (28.2%)** |

Nearly three in ten units that DO carry the canonical runnable form,
and DID assemble, never find a canon-byte partner at all — the ground
built from THE CANONICAL RUNNABLE FORM is not just rare in the final
table (§2), it is starved at the source.

---

## 4. Where the form is used for real

Three places do genuine, verifiable work with the canonical runnable
form; nowhere else in the matching pipeline touches it.

- **The canon-byte ground itself** (§2, 77 pairs) — the only class-forming ground built from it.
- **The assembler roundtrip**, `roundtrip.py` (called from `canon.py`'s pipeline) and `canon2.py`'s own roundtrip step (line 1126 on): both hand the canonical text to a REAL assembler and objdump, not a simulation.
  > `roundtrip.py` line 9: *"the object is assembled; the object is disassembled again; and the instructions that the assembler produced are the unit's CANONICAL BYTES"*
  > `canon2.py` line 1141: `proc2 = subprocess.run(["objdump", "-d", "--no-show-raw-insn", ...])`
  1,562 units reach this for `canon.py`'s form (`canon_roundtrip.json`, `units_assembled` count); `canon2.py`'s own roundtrip reaches 574/700/77/112/124 = 1,587 units (§3's `derived_text`-present column; all of these are `assembled_ok`, confirmed by `canon2_units_c.json`'s field `"assembled_ok": 574` matching the `derived_text`-present count exactly).
- **Exact-regeneration checking, C ONLY** — `canon2.py` line 840: `out["exact_regeneration"] = derived == list(lines)`, and line 1211: `if lang == "c" and rec.get("exact_regeneration"):`. This check — does the derived runnable text reproduce the compiler's OWN mnem, character for character — is gated to `lang == "c"` in the code; `canon2_units_cpp.json`, `_go.json`, `_rust.json`, `_swift.json` all lack the field `exact_regeneration_against_compiler_mnem` entirely (checked directly, all four files). 128/610 C units pass it.
- **One dead-end use of `derived_text` itself**: `component_mine2.py`, the compositional-matching (alpha/beta/gamma) miner, states in its own docstring: *"The material mined here is the RUNNABLE derived text (`derived_text`, ...), never the pseudo-step notation"* — the only file in the whole directory, besides `canon2.py` itself, that reads the field `derived_text` (confirmed by grep across every `.py` file). Its outputs, `components2.json` and `compositions2.json`, are read by NO OTHER program in the directory (confirmed by grep for both filenames across every `.py` file) — so this genuine, correctly-scoped use of the runnable form never reaches the matching pipeline that builds `dominant_table9.json`.

---

## 5. Drift timeline

Reconstructed from file mtimes (`stat`, this session) and each
program's own docstring/`PROGRESS.md` entry. All times 2026, `-0400`.

- **08-25 01:58** — `op_units_c.json` written: raw probe bytes exist; nothing canonical exists yet.
- **08-25 06:36–06:44** — `sem_anchored.py`, `match_units.py`, `verdicts.py` written and run. `match_units.py`'s own docstring: *"1. BYTE IDENTITY. ... 2. SEM IDENTITY. The anchored lifted form"* — matching is founded on raw bytes and the pyvex lift, with NO mention of a canonical form, because none exists yet.
- **08-25 17:41–19:09** — `verdicts3b.json`, `core_modes.py`, `verdicts4.json`, `dominant_table.py`/`.json` (the FIRST dominant table) all built. `dominant_table.py`'s `EVIDENCE_ORDER = ["byte", "sem", "core-text", "z3", "unclassified"]` — the founding table has no canon ground because THE CANONICAL RUNNABLE FORM does not exist for another four hours.
- **08-25 23:28–23:30** — `canon.py` and `dominant_table2.py` written together; `canon_units_c.json`, `canon_roundtrip.json`, `dominant_table2.json` built the same minute. This is the moment `canon-byte` enters `EVIDENCE_ORDER` — AgentMemory records the same date: *"THE CANONICAL RUNNABLE FORM (ratified by the owner, 2026-08-25)."* The founding byte/sem grounds from step 6/`verdicts.py` are carried forward unchanged, never re-run against the new form.
- **08-26 (same day, later)** — `PROGRESS.md`'s own entry: *"ruled direction — matching material is the lifted expression tree; sub-tree containment; priority = tree position"* — a SECOND, separate ruling on what "the matching material" is, naming the lifted expression tree rather than the canonical runnable form, recorded the day after the canonical-form ratification.
- **08-26 21:49–21:56** — `canon2.py` (the move-erasure amendment's generator, producing BOTH `erased_form` and `derived_text`) and `dominant_table_erased.py` written six minutes apart. `dominant_table_erased.py` line 306 reads `rec.get("erased_form")` — the NON-runnable field — never `rec.get("derived_text")`, the runnable one sitting right beside it in the same JSON record. `dominant_table8.json` built the same minute.
- **08-27 11:23–11:29** — `sem_anchored_spill.py`, `tree_match2.py`, `tree_units2.json`, `dominant_table_tree.py`, `dominant_table9.json`, `dom_ops7.py`/`.json` — the newest lap, all built within six minutes of each other. This is where `tree-exact` (a z3-normalized, non-runnable expression) enters `EVIDENCE_ORDER` for the first time; `dominant_table9.json` is the current final table.

Read in order: matching started on non-canonical material before the
canonical form existed (08-25 06:36 vs. 08-25 23:28); once the form
existed, a new ground was built from it (`canon-byte`) but the
founding grounds were never revisited; and every layer added after
that (08-26 21:56, 08-27 11:27) reached for a new NON-runnable
notation each time — the pseudo-step form, then the z3-normalized
tree — rather than extending or replacing anything with `canon_text`
or `derived_text`.

---

## 6. The swift division/modulo case, worked

`swift/op_150` = `a / b`, `swift/op_186` = `a % b`, both `Int32,Int32
-> Int32`. Every representation, side by side, and whether it tells
the two apart.

- **bytes / mnem** (`op_units_swift.json`, `ship`) — DISTINGUISHES. op_150 ends `idiv %esi; ret`; op_186 ends `idiv %esi; mov %edx,%eax; ret` — the extra `mov` is the whole difference between "hand back the quotient already sitting in `%eax`" and "hand back the remainder sitting in `%edx`."
- **`canon2.py`'s `derived_text`** — DOES NOT APPLY. Both units are branching (overflow/zero-divide guards), and canon2.py's own docstring says branching units are *"SKIPPED outright"* for this field; `canon2_units_swift.json` records, for both: `"derived_text": "not derived this slice: branching units are erased per-block; multi-block runnable derivation is future work"`. The canonical runnable form makes no statement about this pair at all.
- **`erased_form`/`blocks`** (`canon2_units_swift.json`) — DOES NOT DISTINGUISH. Both units erase to the IDENTICAL block sequence, character for character, including the control-flow block that contains the division:
  > `"L3:", "  u0 = cltd(a)", "  u1, u2 = idiv(u0:a, b)", "  return"`
  This is identical text for op_150 and op_186. The mechanical cause is `canon2.py`'s `control_step_text()`, lines 973–974:
  > ```
  > if mnem in ("ret", "retq"):
  >     return "return"
  > ```
  Every `ret` instruction becomes the bare string `"return"`, with no value name attached — unlike the SINGLE-block path (§1's `c/op_246` example, `"u1, answer = idiv(...)"`), which calls `relabel_answer()` (`canon2.py` lines 462–492) to rename the value the calling rule hands back to `answer`. `canon2_branching()` (the function that builds `blocks`/`erased_form` for branching units, lines 985–1107) never calls `relabel_answer` — confirmed by reading the function in full; it has no such call anywhere in its body. The information that distinguishes "return `u1`" from "return `u2`" is computed (both values are named, `u1` and `u2`) and then discarded at the one line that writes the return step.
- **lifted `sem.key`** (`sem_anchored_swift.json`) — DISTINGUISHES, though only by coincidence of listing order/content, not by an explicit "this is the answer" tag. Block B3's `V[...]` list differs: op_150 is `V[zx64(ex32@0(DivModS64to32(...))) zx64(ex32@32(DivModS64to32(...)))]` (one value at offset 0, one at offset 32); op_186 is `V[zx64(ex32@32(DivModS64to32(...))) zx64(ex32@32(DivModS64to32(...)))]` (both listed values at offset 32). The two full `sem.key` strings are NOT equal.
- **`tree_units2.json`'s `normal_path_root`** — DISTINGUISHES. op_150: `"Concat(0, Extract(31, 0, op_3))"`; op_186: `"Concat(0, Extract(63, 32, op_3))"` — the `Extract` bounds differ (`31,0` = low 32 bits = quotient, vs `63,32` = high 32 bits = remainder), even though the `DivModS64to32(...)` call inside both collapses to the same opaque `op_3` placeholder (§7 explains why).
- **`core_modes.py`'s `core`** — DISTINGUISHES (same `ex32@0` vs `ex32@32` distinction as `sem.key`, before z3 normalization).

**Which representations would have prevented the false merge**: bytes/mnem, `sem.key`, `normal_path_root`, and `core` all distinguish the pair — four of six. **Which one caused it**: `erased_form`/`blocks`, the ONLY representation among the six that is blind to the difference, because `control_step_text()`'s `ret`-handling branch (quoted above) drops the return-value name that every other representation in the pipeline still carries. `dominant_table8.json`'s class `A0735` (`swift/op_150`, `swift/op_186`, plus their `/=`/`%=` forms) records this exactly:
> `"weakest_evidence": "erased-form"`, `"weakest_evidence_text": "erased-form identity (the move-erased canonical records, ratified 2026-08-26, are line-for-line character-identical; entry-contract differences are ignored -- the adapter between them is derivable)"`, `"distinct_core_texts": 2`

`distinct_core_texts: 2` is the artifact's OWN field, on the OWN class it is flagging as merged, stating outright that two different `core` texts sit inside one class — and the merge went ahead regardless, because `core`-text disagreement is not, by the code in §2, a thing that blocks a merge; it only labels a weaker ground when nothing stronger disagrees either.

**The transitive consequence**: `dominant_table8.json` (before `tree-exact` existed) still kept C's own division and modulo apart — `c/op_210` in class `A0072`, `c/op_246` in class `A0108`, two different classes, confirmed by direct lookup. `dominant_table9.json`'s `tree-exact` pass then added two SEPARATELY CORRECT cross-language edges: `c/op_210` (division) ↔ `swift/op_150` (division), and `c/op_246` (modulo) ↔ `swift/op_186` (modulo) — both true, both backed by matching `normal_path_root` text for the matching operator. But because `A0735` already contained BOTH swift units (the erased-form bug above), landing one correct edge on each swift unit fuses `A0072` and `A0108` together THROUGH `A0735`, by ordinary transitive closure — no single edge anywhere claims "division equals modulo." The final class, `dominant_table9.json`'s `A0072`, has 20 members across all five languages, including `c/op_210` (`canonical_form`: `"mov %edi,%eax; cltd; idiv %esi; ret"`) and `c/op_246` (`canonical_form`: `"mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret"`) side by side — visibly different canonical runnable text, in the same class — and its own `divergence_inside_the_class` field, whose job is to record exactly this kind of internal disagreement, reads `[]`.

---

## 7. What would change if the canonical runnable text were primary

Three measured examples (the task asked for at least three).

**1. `dominant_table9.json` class `A0072` (§6) would split.** Comparing `canon_text`/`derived_text` directly, `c/op_210` (`"mov %edi,%eax; cltd; idiv %esi; ret"`) and `c/op_246` (`"mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret"`) are not equal — the class's 20 members would separate back into (at minimum) a division class and a modulo class, matching what `dominant_table8.json` already had correct for C, C++, Go, and Rust before `tree-exact` ran.

**2. `dominant_table9.json` class `A0057`** — 40 members, `class_key.operand_types = "f32,f32"`, spanning FOUR different operators: `['*', '*=', '+', '+=', '-', '-=', '/', '/=']`. `canonical_core` (the field recording distinct underlying representations found inside the class) lists 4 distinct entries: `Mul32F0x4(...)`, `Div32F0x4(...)`, `Add32F0x4(...)`, `Sub32F0x4(...)` — the class's own `distinct_core_texts: 4` says so. `divergence_inside_the_class` is `[]`. Mechanism, traced to `tree_match2.py`: `c/op_123` (`+`), `c/op_159` (`-`), `c/op_195` (`*`), `c/op_231` (`/`) each lift to a DIFFERENT raw VEX call — `Add32F0x4`, `Sub32F0x4`, `Mul32F0x4`, `Div32F0x4` — but `tree_units2.json` records the SAME `normal_path_root` for all four: `"op_2"`. The cause is `tree_match2.py` lines 131–135:
   > ```
   > text = serialize(tree)
   > w = 64
   > if text not in atoms:
   >     atoms[text] = _z3.BitVec("op_%d" % len(atoms), w)
   > return atoms[text]
   > ```
   None of the four SIMD float operations is in the recognized-operation list above this fallback (only scalar `Add32`/`Sub32`/etc. are handled, lines 95–101). Each falls through to this branch, and — because `atoms = {}` is a FRESH dictionary per unit (line 144, `normalize()`) — the first unrecognized node in ANY unit's expression becomes `op_0`, the second `op_2`, purely by its POSITION in that unit's own tree, never by its identity. Four structurally-similar, operator-different expressions each place their one unmodelled call at the same tree position, so all four get the identifier `op_2` regardless of which real operation it is. Comparing `canon_text` directly (`"mulss %xmm1,%xmm0; ret"` vs `"divss %xmm1,%xmm0; ret"` vs `"addss %xmm1,%xmm0; ret"` vs `"subss %xmm1,%xmm0; ret"`) would keep all four apart, because the opcode mnemonic — `mulss`/`divss`/`addss`/`subss` — is present in the runnable text and erased nowhere in the normalizer's placeholder substitution.

**3. `dominant_table9.json` class `A0124`** — a currently-correct merge that raw runnable-text equality alone would BREAK, needing a normalizer above it (the second half of the task's question). Members include `c/op_102` (`"add %esi,%edi; jo 7 <op_222+0x7>; mov %edi,%eax; ret; ud2"` — an overflow-checked add that traps) and `cpp/op_102`/others compiled to `"lea (%rdi,%rsi,1),%eax; ret"` — a plain unchecked add via the `lea` instruction. `canonical_core` for this class is a SINGLE entry, `"zx64(Add32(ex32@0(in0:64),ex32@0(in1:64)))"` — both forms genuinely compute `a + b`; `Add32` IS a recognized op in `tree_match2.py` (line 98), so this one normalizes correctly, unlike example 2. But the canonical runnable TEXT of the two forms is completely different — `lea` vs `add`+`jo`-guard+`mov` — an instruction-selection difference between compilers, not a naming difference register-renaming can fix. Rebuilding matching on `canon_text`/`derived_text` equality alone would split this currently-correct class; keeping it merged needs a normalizer that recognizes `lea (%rdi,%rsi,1),%eax` and `add %esi,%edi` as the same arithmetic op modulo instruction selection — exactly the "instruction-order/register-allocation" normalizer the task anticipated, except the actual gap measured here is instruction SELECTION, one level more specific.

**Contrast, stated once, structurally**: example 1 and 2 are classes where the runnable text, read directly, would have refused to merge what an opaque non-runnable placeholder merged — reading it would SPLIT a false class. Example 3 is a class where the runnable text, read directly and compared for raw equality, would have refused to merge what a real semantic equivalence (`Add32` in both, `lea` being an add-with-a-side-effect-free encoding) makes true — reading it naively would SPLIT a correct class, unless paired with a normalizer built for exactly this gap.
