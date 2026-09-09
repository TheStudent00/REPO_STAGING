# log 235 — task mn1: the `mnem` field rename across o2/o8/o9/o10

Node: `hq.research.arch_unit_oracle.cross_construction.single_opcode_units`
(`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_2_single_opcode_units/CORE_0_3_2_2_2_single_opcode_units.md`).

**One sentence.** The spelling guard
(`Research/op_pipeline/check_no_spelling_keys.py`) already exempts a
JSON field named `mnem` as a machine form; five generator scripts on
the oracle line wrote that same field under the name `mnemonic`
instead, so this task renamed the field to `mnem` in each generator
and regenerated the artifacts it writes — a rename, not a change of
anything measured.

Date: 2026-09-08. Instance `mn1`, copied from `t97.conf` (already on
the tower and up per the brief), brought down at the end of this log.
Every lane ran on the tower guest through
[`remote_lane.sh`](file://~/Programming/Airlock/remote_lane.sh)
(`~/Programming/Airlock/remote_lane.sh`), per LAW's last section — none
of the twelve compute lanes below ran on the laptop.

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

Every rendering below is labelled per `object.literal-gloss-analogy`:
**LITERAL** is the object itself, quoted; **GLOSS** is a plain-words
reading beside a literal. Paths inside a pasted command are the ones
the lane sees: `/projects/PseudoCoupHQ` IS `~/Programming/PseudoCoupHQ`,
mounted into the instance on the tower guest.

---

## §1. What the objects are, one sentence each, in relation

- The **guard** is
  [`Research/op_pipeline/check_no_spelling_keys.py`](file://~/Programming/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py),
  never modified this task; its `PROSE_FIELDS` set names `mnem` (not
  `mnemonic`) as exempt, on the stated ground "a byte/sem key is a
  machine form".
- The **field** is the JSON object key each of the five generators
  below used to carry one arch-opcode mnemonic string (e.g. `add`,
  `and`, `lea`) on a row, a signature-table entry, or a result record.
  Before this task every one of the five wrote and read it spelled
  `mnemonic`; after, `mnem`.
- The **five generators** are the scripts that write the field, each
  read and edited this task, in the dependency order they run (a
  later one reads an earlier one's json):
  1. [`single_opcode_units.py`](file://~/Programming/PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.py) (task o2)
  2. [`unique_opcodes.py`](file://~/Programming/PseudoCoupHQ/Research/oracle/arch_opcodes/unique_opcodes.py) (task o2)
  3. [`opcode_signatures.py`](file://~/Programming/PseudoCoupHQ/Research/oracle/arch_opcodes/signatures/opcode_signatures.py) (task o9) — reads o2's two jsons
  4. [`ledger_signatures.py`](file://~/Programming/PseudoCoupHQ/Research/oracle/arch_opcodes/signatures/ledger_signatures.py) (task o10) — reads `unique_opcodes.json` and imports o9's own module (`opcode_signatures.py`, as `OS`), never forked
  5. [`per_opcode.py`](file://~/Programming/PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode/per_opcode.py) (task o8) — reads `single_opcode_units.json`
- The **scope of the rename**, decided once and held for all five
  scripts: only the JSON object key spelled EXACTLY `mnemonic` — in
  what a script writes and in what it reads back off another script's
  json — became `mnem`. A *different*, compound field name that merely
  contains the word (`mnemonic_a`, `mnemonic_b`, `landed_mnemonic`) is
  a separate field, out of this rename's scope, and is named below
  (§5) as a distinct, still-open guard cause — not silently renamed,
  which would have been inventing a new record field the brief did
  not ask for.
- The **before artifacts** are each json's pre-regeneration copy, kept
  at `<name>.before.json` beside the live one until this log was
  written (per the brief), then deleted (§9).

## §2. Walkthrough

The five scripts' `mnemonic` occurrences were read first (LAW's
`grep -c` convention is not what applies here — every literal use had
to be classified by hand as one of: a JSON field WRITE, a JSON field
READ, a markdown column header or docstring/prose word, or a Python
local-variable name). Only the first two classes change. Column
headers, docstrings and variable names keep the word, per the brief.
One dependency, found while reading `ledger_signatures.py`, mattered
for correctness and not only for the guard: its `build_family_shim_rows`
builds pseudo-rows that it feeds into `opcode_signatures.py`'s own
`find_sign_sensitive_pairs` (imported as `OS`, never forked) — that
function was itself edited to read `row["mnem"]`, so the shim's own
output field had to become `mnem` too, or the two functions would no
longer agree on a key and the call would raise a `KeyError`. This was
caught by reading the call graph before editing, not by a failed run.

Each script was edited on the laptop, syntax-checked with
`python3 -m py_compile` (all five passed clean, no exception), then
the whole `Research/oracle/` folder was mirrored to the tower with
`sync-to` before any lane ran. Regeneration then followed the brief's
stated order — o2's two generators first, then o9 and o10 (both read
o2's `unique_opcodes.json`), then o8 (reads o2's
`single_opcode_units.json`) — with a `sync-back` after every stage so
the next stage's lane read the just-renamed json rather than a stale
copy still on the tower. Every regeneration command below is the
generator's own `census` / `population` / `run` / `report` sub-command,
run exactly as its own original lane ran it (confirmed against
`lane_logs/o2_l5_single_opcode.log`, `lane_logs/o2_l6_unique_opcodes.log`,
`signatures/lanes/o9_l1_census.sh`, `signatures/lanes_o10/o10_l2_census.sh`,
`cross_construction/emulation/per_opcode/lanes/o8_l1_population.sh` /
`o8_l3_run.sh` / `o8_l4_report.sh`) — nothing about HOW each generator
runs changed, only the field name inside it.

Every headline count came back identical to its `.before.json` value
(§4's table): 259 single-opcode narrow rows, 162 unique mnemonics,
o9's 243 valid / 16 skipped, o10's 31,078 units streamed over 332
shards, o8's 243 jobs with 197 LANDED / 155 byte-identical /
216 proved-on-ship. The guard, run over every regenerated json, PASSED
clean on three of the seven files it had never passed before this
rename (`unique_opcodes.json`, `per_opcode_population.json`,
`per_opcode_held.json`) and still FAILS on the other four, for causes
distinct from the one this task fixed (§5) — reported, not fixed,
per the brief's own instruction to stop and list by cause rather than
invent an exemption or a further rename.

## §3. The diff per script, LITERAL

Command run on the laptop, `~/Programming/PseudoCoupHQ` as the working
directory (the pre-session baseline commit is `f34a38a0`, the last
commit under `Research/oracle/` before this task's edits):

```
$ git diff f34a38a0 -- Research/oracle/arch_opcodes/single_opcode_units.py
diff --git a/Research/oracle/arch_opcodes/single_opcode_units.py b/Research/oracle/arch_opcodes/single_opcode_units.py
index a0b149d7..5940f98f 100644
--- a/Research/oracle/arch_opcodes/single_opcode_units.py
+++ b/Research/oracle/arch_opcodes/single_opcode_units.py
@@ -185,7 +185,7 @@ def main():
                 # display-label field -- never as a bare-token list on
                 # this grouping row (THE SPELLING BAN).
                 rows.append({
-                    "mnemonic": entry["mnem"],
+                    "mnem": entry["mnem"],
                     "body_text": entry["body_text"],
                     "member_count": len(entry["members"]),
                     "example_unit_id": entry["members"][0]["unit"],
@@ -221,7 +221,7 @@ def main():
             lines.append("|---|---|---|---|---|")
             for r in rows:
                 ops_seen = sorted(set(m["operator"] for m in r["members"]))
-                lines.append(f"| {r['mnemonic']} | `{r['body_text']}` | {r['member_count']} | "
+                lines.append(f"| {r['mnem']} | `{r['body_text']}` | {r['member_count']} | "
                               f"{', '.join(ops_seen)} | {r['example_unit_id']} |")
         lines.append("")
         lines.append("#### zero-opcode units (pure move, chaff-stripped body is empty)")
```

```
$ git diff f34a38a0 -- Research/oracle/arch_opcodes/unique_opcodes.py
diff --git a/Research/oracle/arch_opcodes/unique_opcodes.py b/Research/oracle/arch_opcodes/unique_opcodes.py
index efe340ef..ffe0aef9 100644
--- a/Research/oracle/arch_opcodes/unique_opcodes.py
+++ b/Research/oracle/arch_opcodes/unique_opcodes.py
@@ -102,7 +102,7 @@ def main():
         only_ledger = sorted(ledger_set - body_set)
         only_body_not_ledger = sorted(body_set - ledger_set)
         for m in only_ledger:
-            mismatches.append({"lang": lang, "mnemonic": m, "where": "in ledger produced_by, not in body_verbatim vocabulary"})
+            mismatches.append({"lang": lang, "mnem": m, "where": "in ledger produced_by, not in body_verbatim vocabulary"})
         # only_body_not_ledger is EXPECTED for chaff mnemonics (mov/ret/etc
         # that never directly produce a ledger row) -- report count only,
         # not as a mismatch, since the brief's cross-check direction is
@@ -118,8 +118,8 @@ def main():
     for lang in sorted(tally):
         rows = []
         for mnem, entry in tally[lang].items():
-            rows.append({"mnemonic": mnem, "occurrences": entry["occurrences"], "unit_count": len(entry["units"])})
-        rows.sort(key=lambda r: (-r["unit_count"], r["mnemonic"]))
+            rows.append({"mnem": mnem, "occurrences": entry["occurrences"], "unit_count": len(entry["units"])})
+        rows.sort(key=lambda r: (-r["unit_count"], r["mnem"]))
         out["per_language"][lang] = rows
 
     # Cross-language table.
@@ -129,7 +129,7 @@ def main():
     langs_sorted = sorted(tally.keys())
     cross_rows = []
     for mnem in sorted(all_mnems):
-        row = {"mnemonic": mnem}
+        row = {"mnem": mnem}
         langs_using = []
         for lang in langs_sorted:
             cnt = len(tally.get(lang, {}).get(mnem, {}).get("units", set()))
@@ -138,7 +138,7 @@ def main():
                 langs_using.append(lang)
         row["languages_using_it"] = langs_using
         cross_rows.append(row)
-    cross_rows.sort(key=lambda r: r["mnemonic"])
+    cross_rows.sort(key=lambda r: r["mnem"])
     out["cross_language_rows"] = cross_rows
     out["languages"] = langs_sorted
 
@@ -156,7 +156,7 @@ def main():
         lines.append("| mnemonic | occurrences | unit count |")
         lines.append("|---|---|---|")
         for r in rows:
-            lines.append(f"| {r['mnemonic']} | {r['occurrences']} | {r['unit_count']} |")
+            lines.append(f"| {r['mnem']} | {r['occurrences']} | {r['unit_count']} |")
         lines.append("")
 
     lines.append("## cross-language table")
@@ -167,7 +167,7 @@ def main():
     lines.append(sep)
     for row in cross_rows:
         cells = " | ".join(str(row[l]) for l in langs_sorted)
-        lines.append(f"| {row['mnemonic']} | {cells} | {', '.join(row['languages_using_it'])} |")
+        lines.append(f"| {row['mnem']} | {cells} | {', '.join(row['languages_using_it'])} |")
     lines.append("")
 
     lines.append("## cross-check")
@@ -175,7 +175,7 @@ def main():
     if mismatches:
         lines.append(f"{len(mismatches)} mismatch(es):")
         for m in mismatches:
-            lines.append(f"- {m['lang']}: `{m['mnemonic']}` -- {m['where']}")
+            lines.append(f"- {m['lang']}: `{m['mnem']}` -- {m['where']}")
     else:
         lines.append("0 mismatches: every ledger-row producing mnemonic is present in that "
                       "language's body_verbatim vocabulary.")
```

```
$ git diff f34a38a0 -- Research/oracle/arch_opcodes/signatures/opcode_signatures.py
diff --git a/Research/oracle/arch_opcodes/signatures/opcode_signatures.py b/Research/oracle/arch_opcodes/signatures/opcode_signatures.py
index f983c165..0ec8e167 100644
--- a/Research/oracle/arch_opcodes/signatures/opcode_signatures.py
+++ b/Research/oracle/arch_opcodes/signatures/opcode_signatures.py
@@ -251,7 +251,7 @@ def build_signatures(valid_rows, unit_to_holders):
         lambda: {"member_count": 0, "example_units": []}))
     unmatched = collections.Counter()
     for row in valid_rows:
-        mnem = row["mnemonic"]
+        mnem = row["mnem"]
         for member in row["members"]:
             holders = unit_to_holders.get(member["unit"])
             if holders is None:
@@ -362,7 +362,7 @@ def find_row_scoped_reading_blind(valid_rows, unit_to_holders):
     signature_a, unit_b, signature_b}."""
     evidence = {}
     for row in valid_rows:
-        mnem = row["mnemonic"]
+        mnem = row["mnem"]
         if mnem in evidence:
             continue
         seen = {}
@@ -445,7 +445,7 @@ def find_sign_sensitive_pairs(table, unit_to_family, valid_rows):
     the brief requires instead of the operator token."""
     mnem_families = collections.defaultdict(set)
     for row in valid_rows:
-        mnem = row["mnemonic"]
+        mnem = row["mnem"]
         for member in row["members"]:
             family = unit_to_family.get(member["unit"])
             if family is not None:
@@ -699,7 +699,7 @@ def census_command():
 
     all_mnemonics = read_json(UNIQUE_OPCODES_JSON)
     all_mnemonics = sorted(
-        r["mnemonic"] for r in all_mnemonics["cross_language_rows"])
+        r["mnem"] for r in all_mnemonics["cross_language_rows"])
     say("   unique_opcodes.json: %d mnemonics total" % len(all_mnemonics))
 
     guard = guard_partition_pass(all_mnemonics)
@@ -805,7 +805,7 @@ def report_command():
     header = ["lang", "mnemonic", "example_unit_id", "reason"]
     skip_rows = []
     for row in population["skipped"]:
-        skip_rows.append([row["lang"], row["mnemonic"],
+        skip_rows.append([row["lang"], row["mnem"],
                           row["example_unit_id"], row["reason"]])
     lines.append(pipe_table(header, skip_rows))
     lines.append("")
```

```
$ git diff f34a38a0 -- Research/oracle/arch_opcodes/signatures/ledger_signatures.py
diff --git a/Research/oracle/arch_opcodes/signatures/ledger_signatures.py b/Research/oracle/arch_opcodes/signatures/ledger_signatures.py
index 317462b3..78bf4ec2 100644
--- a/Research/oracle/arch_opcodes/signatures/ledger_signatures.py
+++ b/Research/oracle/arch_opcodes/signatures/ledger_signatures.py
@@ -301,7 +301,7 @@ def classify_never_produced(all_mnemonics, table, seen_anywhere,
             cause = "seen in a ledger row, never as its own arch_opcode producer"
         else:
             cause = "never seen in any ledger row (move or control transfer)"
-        never.append({"mnemonic": mnem, "cause": cause})
+        never.append({"mnem": mnem, "cause": cause})
     return never
 
 
@@ -366,13 +366,13 @@ def build_family_shim_rows(mnem_to_units):
     """the shape `OS.find_sign_sensitive_pairs` expects for its third
     argument (`valid_rows`): one pseudo-row per mnemonic, its
     `members` the units that ever produced it. `OS`'s own function
-    reads only `row["mnemonic"]` and `member["unit"]` off this list --
+    reads only `row["mnem"]` and `member["unit"]` off this list --
     nothing else -- so this shim carries no meaning beyond satisfying
     that shape, and no field `OS` does not already read."""
     rows = []
     for mnem, units in mnem_to_units.items():
         rows.append({
-            "mnemonic": mnem,
+            "mnem": mnem,
             "members": [{"unit": unit} for unit in sorted(units)],
         })
     return rows
@@ -393,7 +393,7 @@ def census_command():
 
     all_mnemonics_doc = OS.read_json(UNIQUE_OPCODES_JSON)
     all_mnemonics = sorted(
-        r["mnemonic"] for r in all_mnemonics_doc["cross_language_rows"])
+        r["mnem"] for r in all_mnemonics_doc["cross_language_rows"])
     say("   unique_opcodes.json: %d mnemonics total" % len(all_mnemonics))
 
     pass_result = census_pass(unit_to_holders, all_mnemonics)
@@ -546,7 +546,7 @@ def report_command():
     lines.append("## 1b. Mnemonics with zero arch_opcode rows in the census")
     lines.append("")
     header = ["mnemonic", "cause"]
-    rows = [[e["mnemonic"], e["cause"]]
+    rows = [[e["mnem"], e["cause"]]
             for e in document["never_produced"]]
     lines.append(OS.pipe_table(header, rows))
     lines.append("")
```

```
$ git diff f34a38a0 -- Research/oracle/cross_construction/emulation/per_opcode/per_opcode.py
diff --git a/Research/oracle/cross_construction/emulation/per_opcode/per_opcode.py b/Research/oracle/cross_construction/emulation/per_opcode/per_opcode.py
index f46fb7a9..cba9d5f2 100644
--- a/Research/oracle/cross_construction/emulation/per_opcode/per_opcode.py
+++ b/Research/oracle/cross_construction/emulation/per_opcode/per_opcode.py
@@ -185,7 +185,7 @@ def load_rows():
             rows.append({
                 "lang": lang,
                 "row_index": index,
-                "mnemonic": row["mnemonic"],
+                "mnem": row["mnem"],
                 "row_body_text": row["body_text"],
                 "example_unit_id": row["example_unit_id"],
                 "member_count": row["member_count"],
@@ -331,7 +331,7 @@ def one_polyfill(shared, job):
     uid = job["example_unit_id"]
     record = {
         "lang": job["lang"],
-        "mnemonic": job["mnemonic"],
+        "mnem": job["mnem"],
         "example_unit_id": uid,
         "row_body_text": job["row_body_text"],
         "member_count": job["member_count"],
@@ -413,7 +413,7 @@ def one_polyfill(shared, job):
     if len(stripped) == 1:
         landed_mnemonic, _operands = SOU.parse_insn(stripped[0])
         record["landed_mnemonic"] = landed_mnemonic
-        if landed_mnemonic == job["mnemonic"]:
+        if landed_mnemonic == job["mnem"]:
             record["q0"] = {"verdict": "LANDED"}
         else:
             record["q0"] = {"verdict": "LANDED_ELSEWHERE",
@@ -483,7 +483,7 @@ def run_command():
             record["raised"] = "%s: %s" % (type(problem).__name__, problem)
         results.append(record)
         say("[%d/%d] %s/%s %s -> %s  q0=%s q1=%s q3=%s"
-            % (index, total, job["lang"], job["mnemonic"],
+            % (index, total, job["lang"], job["mnem"],
                job["example_unit_id"], summary_word(record),
                (record.get("q0") or {}).get("verdict", "-"),
                (record.get("q1") or {}).get("verdict", "-"),
@@ -506,7 +506,7 @@ def per_x_mnemonic_table(results):
     groups = {}
     order = []
     for record in results:
-        key = (record["lang"], record["mnemonic"])
+        key = (record["lang"], record["mnem"])
         if key not in groups:
             groups[key] = []
             order.append(key)
@@ -573,7 +573,7 @@ def never_landed(results):
     record)."""
     seen = {}
     for record in results:
-        mnemonic = record["mnemonic"]
+        mnemonic = record["mnem"]
         landed = (record.get("q0") or {}).get("verdict") == "LANDED"
         seen.setdefault(mnemonic, False)
         if landed:
@@ -690,7 +690,7 @@ def write_report_md(population, results_document, mnemonic_rows,
         for entry in population["no_proved_term"]:
             lines.append("- `%s` (mnemonic `%s`): %s"
                          % (entry["example_unit_id"],
-                            entry["mnemonic"], entry["reason"]))
+                            entry["mnem"], entry["reason"]))
         lines.append("")
     lines.append("## 1. Per x and per mnemonic: rows | rendered | "
                  "compiled | LANDED | LANDED_ELSEWHERE | NOT_COLLAPSED "
@@ -732,7 +732,7 @@ def write_report_md(population, results_document, mnemonic_rows,
             lines.append("- `%s` (mnemonic `%s`): term `%s`, row "
                          "body `%s`, polyfill body `%s`"
                          % (record["example_unit_id"],
-                            record["mnemonic"], record["term_text"],
+                            record["mnem"], record["term_text"],
                             record["row_body_text"], record["body_text"]))
     else:
         lines.append("(none in this run)")
@@ -746,7 +746,7 @@ def write_report_md(population, results_document, mnemonic_rows,
             q3 = record["q3"]
             lines.append("`%s`, mnemonic `%s`. The term, LITERAL: "
                          "`%s`" % (record["example_unit_id"],
-                                   record["mnemonic"],
+                                   record["mnem"],
                                    record["term_text"]))
             lines.append("")
             lines.append(pipe_table(
@@ -774,7 +774,7 @@ def write_report_md(population, results_document, mnemonic_rows,
     if landed is not None:
         lines.append("`%s`, mnemonic `%s`. The term, LITERAL: `%s`"
                      % (landed["example_unit_id"],
-                        landed["mnemonic"], landed["term_text"]))
+                        landed["mnem"], landed["term_text"]))
         lines.append("")
         lines.append("The rendered source, LITERAL:")
         lines.append("")
@@ -796,13 +796,13 @@ def write_report_md(population, results_document, mnemonic_rows,
         lines.append("`%s`, drawn for mnemonic `%s`, landed on `%s`. "
                      "The term, LITERAL: `%s`"
                      % (elsewhere["example_unit_id"],
-                        elsewhere["mnemonic"],
+                        elsewhere["mnem"],
                         elsewhere["q0"]["landed_mnemonic"],
                         elsewhere["term_text"]))
         lines.append("")
         lines.append(pipe_table(["side", "body"],
                                 [["the row's own body (`%s`)"
-                                  % elsewhere["mnemonic"],
+                                  % elsewhere["mnem"],
                                   "`%s`" % elsewhere["row_body_text"]],
                                  ["the polyfill (`%s`)"
                                   % elsewhere["q0"]["landed_mnemonic"],
@@ -821,7 +821,7 @@ def write_report_md(population, results_document, mnemonic_rows,
         lines.append("`%s`, mnemonic `%s`, %d opcodes remaining after "
                      "the narrow chaff strip. The term, LITERAL: `%s`"
                      % (not_collapsed["example_unit_id"],
-                        not_collapsed["mnemonic"],
+                        not_collapsed["mnem"],
                         not_collapsed["q0"]["opcode_count"],
                         not_collapsed["term_text"]))
         lines.append("")
```

Every one of the five files above was also run through
`python3 -m py_compile` on the laptop before syncing to the tower;
all five compiled clean.

## §4. Regeneration, one lane per generator command, and the counts table

Every lane script is kept in the repo under
[`Research/oracle/arch_opcodes/lanes_mn1/`](file://~/Programming/PseudoCoupHQ/Research/oracle/arch_opcodes/lanes_mn1/),
submitted from there per LAW. Order: o2's two generators, then o9,
then o10 (both read o2's `unique_opcodes.json`), then o8 (reads o2's
`single_opcode_units.json`), a `sync-back` after every stage.

| lane script | generator command it runs | tower log |
|---|---|---|
| `mn1_l1_o2_single_opcode.sh` | `cd Research/oracle/arch_opcodes && python3 single_opcode_units.py` | `~/AirlockRuns/mn1/agent/logs/20260908T215807Z__mn1_l1_o2_single_opcode.sh.log` |
| `mn1_l2_o2_unique_opcodes.sh` | `cd Research/oracle/arch_opcodes && python3 unique_opcodes.py` | `.../20260908T215819Z__mn1_l2_o2_unique_opcodes.sh.log` |
| `mn1_l4_o9_census.sh` | `cd Research/oracle/arch_opcodes/signatures && python3 opcode_signatures.py census` | `.../20260908T215935Z__mn1_l4_o9_census.sh.log` |
| `mn1_l5_o9_report.sh` | `... python3 opcode_signatures.py report` | `.../20260908T215957Z__mn1_l5_o9_report.sh.log` |
| `mn1_l7_o10_census.sh` | `cd Research/oracle/arch_opcodes/signatures && python3 ledger_signatures.py census` | `.../20260908T220041Z__mn1_l7_o10_census.sh.log` |
| `mn1_l8_o10_report.sh` | `... python3 ledger_signatures.py report` | `.../20260908T220053Z__mn1_l8_o10_report.sh.log` |
| `mn1_l10_o8_population.sh` | `cd Research/oracle/cross_construction/emulation/per_opcode && python3 per_opcode.py population` | `.../20260908T220141Z__mn1_l10_o8_population.sh.log` |
| `mn1_l11_o8_run.sh` | `... python3 per_opcode.py run` | `.../20260908T220203Z__mn1_l11_o8_run.sh.log` |
| `mn1_l12_o8_report.sh` | `... python3 per_opcode.py report` | `.../20260908T220228Z__mn1_l12_o8_report.sh.log` |

**Table 1 — counts unchanged, before (from `<name>.before.json`) vs
after regeneration.**

| artifact | headline count | before | after |
|---|---|---|---|
| `single_opcode_units.json` | narrow rows, 5 compiled languages | 259 | 259 |
| `unique_opcodes.json` | cross-language rows (unique mnemonics) | 162 | 162 |
| `opcode_signatures.json` | o9 valid / skipped | 243 / 16 | 243 / 16 |
| `ledger_signatures.json` | o10 units streamed (332 shards) | 31,078 | 31,078 |
| `per_opcode_results.json` | o8 valid rows | 243 | 243 |
| `per_opcode_results.json` | o8 LANDED | 197 | 197 |
| `per_opcode_results.json` | o8 byte-identical (Q1) | 155 | 155 |
| `per_opcode_results.json` | o8 proved-on-ship (Q3) | 216 | 216 |

Every count is identical before/after. Reproducing commands, run from
`~/Programming/PseudoCoupHQ` (the verifier's own cwd) against the
synced-back copies on the laptop:

```
$ python3 -c "
import json
d = json.load(open('Research/oracle/arch_opcodes/single_opcode_units.json'))
langs5 = ['c','cpp','go','rust','swift']
print(sum(len(d['single_opcode_groups'][l]['narrow']) for l in langs5))
"
259
$ python3 -c "
import json
print(len(json.load(open('Research/oracle/arch_opcodes/unique_opcodes.json'))['cross_language_rows']))
"
162
$ python3 -c "
import json
d = json.load(open('Research/oracle/arch_opcodes/signatures/opcode_signatures.json'))
print(d['population']['valid'], len(d['population']['skipped']))
"
243 16
$ python3 -c "
import json
d = json.load(open('Research/oracle/arch_opcodes/signatures/ledger_signatures.json'))
print(d['population']['units_streamed'], d['population']['shards'])
"
31078 332
$ python3 -c "
import json
d = json.load(open('Research/oracle/cross_construction/emulation/per_opcode/per_opcode_results.json'))
r = d['results']
print(d['jobs_total'],
      sum(1 for x in r if (x.get('q0') or {}).get('verdict')=='LANDED'),
      sum(1 for x in r if (x.get('q1') or {}).get('verdict')=='BYTE_IDENTICAL'),
      sum(1 for x in r if (x.get('q3') or {}).get('outcome')=='PROVED_ON_SHIP'))
"
243 197 155 216
```

o10's own peak resident size, printed by `ledger_signatures.py`
itself (`resource.getrusage`), from the tower log
`.../20260908T220041Z__mn1_l7_o10_census.sh.log`: `collector peak
113608 kB` — about 111 MB, well inside the 2 GB named abort
(`ABORT_MEMORY_O10`) `ledger_signatures.py` states and checks after
every one of the 332 shards it streams, and inside the 12 g the
brief states the original o10 run held to. The abort never fired.

## §5. The guard, over every regenerated json, LITERAL

Guard command, run from `Research/op_pipeline` inside the instance
(`/projects/PseudoCoupHQ` mounted there):
`python3 check_no_spelling_keys.py <path>`. Lane
`mn1_l3_o2_guard.sh`, `mn1_l6_o9_guard.sh`, `mn1_l9_o10_guard.sh` and
`mn1_l13_o8_guard.sh` under
[`lanes_mn1/`](file://~/Programming/PseudoCoupHQ/Research/oracle/arch_opcodes/lanes_mn1/).

**PASS, three files that had never passed before this rename:**

```
$ python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/unique_opcodes.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS unique_opcodes.json -- no operator token in any key, grouping, pairing or row structure
```
(tower log `.../20260908T215841Z__mn1_l3_o2_guard.sh.log`, step [2/2])

```
$ python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode/per_opcode_population.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS per_opcode_population.json -- no operator token in any key, grouping, pairing or row structure
$ python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode/per_opcode_held.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS per_opcode_held.json -- no operator token in any key, grouping, pairing or row structure
```
(tower log `.../20260908T220248Z__mn1_l13_o8_guard.sh.log`, steps
[1/3] and [2/3])

**FAIL, four files — reported by cause, per protocol
`object.report-by-cause`, not fixed (stop rule: no new exemption, no
touching the guard, no further rename beyond the scope §1 fixed).**

- **Cause A — a mnemonic used as the DICT KEY itself** (e.g.
  `document["signatures"]["and"]`), not as the value of a field named
  `mnemonic`/`mnem`. The guard's field-name exemption cannot help
  here: it inspects every dict key unconditionally, before any
  exemption applies. This is the SAME open item task o2 (log 208) and
  task o9/o10 (logs 223, 225) already carried and left for the owner,
  unrelated to the field this task renamed — confirmed unchanged in
  count: o9's `opcode_signatures.json` still shows 33 findings (log
  223 recorded 33), o10's `ledger_signatures.json` still shows 58
  (log 225 recorded 58).

  ```
  $ python3 check_no_spelling_keys.py /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/signatures/opcode_signatures.json
  operator inventory: 91 tokens read from probe_manifest_*.json
  FAIL opcode_signatures.json -- 33 spelling-keyed place(s)
       $.guard_partition.all_mnemonics[4]
           list element is the bare operator token 'and'
       $.guard_partition.per_mnemonic.and
           dict key is the operator token 'and'
       $.reading_kinds.mnemonic_scoped_reading_blind_evidence.and
           dict key is the operator token 'and'
       $.reading_kinds.per_mnemonic_kinds.and
           dict key is the operator token 'and'
       $.reading_kinds.reading_changing_evidence.and
           dict key is the operator token 'and'
       ... and 13 more
  ```
  (tower log `.../20260908T220019Z__mn1_l6_o9_guard.sh.log`)

- **Cause B — the compound field `mnemonic_a`/`mnemonic_b`**
  (`opcode_signatures.py`'s `find_sign_sensitive_pairs`, unedited —
  a DIFFERENT field name from the one this task renamed, out of
  scope). One sighting in `opcode_signatures.json`
  (`$.reading_kinds.sign_sensitive_pairs[3].mnemonic_b`, token
  `'xor'`), folded into cause A's 33 above since the guard walks both
  under one run; `ledger_signatures.json` carries more of them since
  o10 found far more sign-sensitive pairs (88 vs o9's 5):

  ```
  $ python3 check_no_spelling_keys.py /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/signatures/ledger_signatures.json
  operator inventory: 91 tokens read from probe_manifest_*.json
  FAIL ledger_signatures.json -- 58 spelling-keyed place(s)
       $.o9_pairings_reexamined[4].mnemonic_b
           operator token 'xor' on a structure field -- this is a grouping/row key, not a per-unit label
       $.reading_kinds.mnemonic_scoped_reading_blind_evidence.and
           dict key is the operator token 'and'
       $.reading_kinds.sign_sensitive_pairs[0].mnemonic_b
           operator token 'and' on a structure field -- this is a grouping/row key, not a per-unit label
       $.reading_kinds.sign_sensitive_pairs[3].mnemonic_b
           operator token 'or' on a structure field -- this is a grouping/row key, not a per-unit label
       $.reading_kinds.sign_sensitive_pairs[5].mnemonic_b
           operator token 'xor' on a structure field -- this is a grouping/row key, not a per-unit label
       ... and 38 more
  ```
  (tower log `.../20260908T220115Z__mn1_l9_o10_guard.sh.log`)

- **Cause C — `per_opcode.py`'s compound field `landed_mnemonic`**
  (the observed opcode a polyfill actually compiled to, a different
  concept from the row's target `mnem` — also out of this rename's
  scope). 57 findings, ALL this one field, confirmed by a local,
  untruncated walk of the synced-back json (§ below); none share
  cause A or B, since `per_opcode_results.json` carries no dict keyed
  by a bare mnemonic:

  ```
  $ python3 check_no_spelling_keys.py /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode/per_opcode_results.json
  operator inventory: 91 tokens read from probe_manifest_*.json
  FAIL per_opcode_results.json -- 57 spelling-keyed place(s)
       $.results[6].landed_mnemonic
           operator token 'and' on a structure field -- this is a grouping/row key, not a per-unit label
       $.results[7].landed_mnemonic
           operator token 'and' on a structure field -- this is a grouping/row key, not a per-unit label
       $.results[40].landed_mnemonic
           operator token 'not' on a structure field -- this is a grouping/row key, not a per-unit label
       $.results[42].landed_mnemonic
           operator token 'or' on a structure field -- this is a grouping/row key, not a per-unit label
       $.results[66].landed_mnemonic
           operator token 'xor' on a structure field -- this is a grouping/row key, not a per-unit label
       ... and 37 more
  ```
  (tower log `.../20260908T220248Z__mn1_l13_o8_guard.sh.log`, step
  [3/3])

- **Cause D — `single_opcode_units.json`'s `zero_opcode_examples`
  records**. A pre-existing structural gap unrelated to §A-C: each
  example record is `{"unit": uid, "operator": operator, "body_text":
  body_text}` — it carries a UNIT ID (`unit`) but no `lang`/`language`
  field, so the guard's `is_unit_object()` check (which requires
  BOTH) never recognizes it as a per-unit label carrier, and its
  `operator` field is walked as an ordinary structure field. 30
  findings, all this one cause (confirmed by a local, untruncated
  walk):

  ```
  $ python3 check_no_spelling_keys.py /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.json
  operator inventory: 91 tokens read from probe_manifest_*.json
  FAIL single_opcode_units.json -- 30 spelling-keyed place(s)
       $.zero_opcode_examples.c.narrow[0].operator
           operator token '--' on a object that does not identify one unit -- this is a grouping/row key, not a per-unit label
       $.zero_opcode_examples.c.narrow[2].operator
           operator token '+' on a object that does not identify one unit -- this is a grouping/row key, not a per-unit label
       $.zero_opcode_examples.rust.narrow[0].operator
           operator token '..' on a object that does not identify one unit -- this is a grouping/row key, not a per-unit label
       ... and 10 more
  ```
  (tower log `.../20260908T215841Z__mn1_l3_o2_guard.sh.log`, step
  [1/2])

Untruncated local re-walks confirming causes C and D are each ONE
cause (run on the laptop, synced-back copies, using the guard's own
`inventory()`/`walk()` functions, never a fork of its logic):

```
$ python3 -c "
import json, sys
sys.path.insert(0,'Research/op_pipeline')
import check_no_spelling_keys as G
toks = G.inventory()
doc = json.load(open('Research/oracle/cross_construction/emulation/per_opcode/per_opcode_results.json'))
findings = []
G.walk(doc, toks, '\$', findings)
print(len(findings), 'findings, all landed_mnemonic:',
      all('landed_mnemonic' in w for w, _why in findings))
"
57 findings, all landed_mnemonic: True
$ python3 -c "
import json, sys
sys.path.insert(0,'Research/op_pipeline')
import check_no_spelling_keys as G
toks = G.inventory()
doc = json.load(open('Research/oracle/arch_opcodes/single_opcode_units.json'))
findings = []
G.walk(doc, toks, '\$', findings)
print(len(findings), 'findings, all zero_opcode_examples:',
      all('zero_opcode_examples' in w for w, _why in findings))
"
30 findings, all zero_opcode_examples: True
```
(run from `~/Programming/PseudoCoupHQ`)

`grep -c exempt` over every file this task added that DOES work (the
thirteen lanes that generate, guard, or regenerate something, and the
five edited generators) — the verify-only lanes (`mn1_l14_verify.sh`
onward) are excluded from this list because each one names itself,
so a glob over `lanes_mn1/*.sh` grows by one every time this exact
check is re-run to fix something else the same verify pass found,
which never converges; the guard itself is untouched:

```
$ grep -c exempt Research/oracle/arch_opcodes/lanes_mn1/mn1_l10_o8_population.sh Research/oracle/arch_opcodes/lanes_mn1/mn1_l11_o8_run.sh Research/oracle/arch_opcodes/lanes_mn1/mn1_l12_o8_report.sh Research/oracle/arch_opcodes/lanes_mn1/mn1_l13_o8_guard.sh Research/oracle/arch_opcodes/lanes_mn1/mn1_l1_o2_single_opcode.sh Research/oracle/arch_opcodes/lanes_mn1/mn1_l2_o2_unique_opcodes.sh Research/oracle/arch_opcodes/lanes_mn1/mn1_l3_o2_guard.sh Research/oracle/arch_opcodes/lanes_mn1/mn1_l4_o9_census.sh Research/oracle/arch_opcodes/lanes_mn1/mn1_l5_o9_report.sh Research/oracle/arch_opcodes/lanes_mn1/mn1_l6_o9_guard.sh Research/oracle/arch_opcodes/lanes_mn1/mn1_l7_o10_census.sh Research/oracle/arch_opcodes/lanes_mn1/mn1_l8_o10_report.sh Research/oracle/arch_opcodes/lanes_mn1/mn1_l9_o10_guard.sh Research/oracle/arch_opcodes/single_opcode_units.py Research/oracle/arch_opcodes/unique_opcodes.py Research/oracle/arch_opcodes/signatures/opcode_signatures.py Research/oracle/arch_opcodes/signatures/ledger_signatures.py Research/oracle/cross_construction/emulation/per_opcode/per_opcode.py | sort
Research/oracle/arch_opcodes/lanes_mn1/mn1_l10_o8_population.sh:0
Research/oracle/arch_opcodes/lanes_mn1/mn1_l11_o8_run.sh:0
Research/oracle/arch_opcodes/lanes_mn1/mn1_l12_o8_report.sh:0
Research/oracle/arch_opcodes/lanes_mn1/mn1_l13_o8_guard.sh:0
Research/oracle/arch_opcodes/lanes_mn1/mn1_l1_o2_single_opcode.sh:0
Research/oracle/arch_opcodes/lanes_mn1/mn1_l2_o2_unique_opcodes.sh:0
Research/oracle/arch_opcodes/lanes_mn1/mn1_l3_o2_guard.sh:0
Research/oracle/arch_opcodes/lanes_mn1/mn1_l4_o9_census.sh:0
Research/oracle/arch_opcodes/lanes_mn1/mn1_l5_o9_report.sh:0
Research/oracle/arch_opcodes/lanes_mn1/mn1_l6_o9_guard.sh:0
Research/oracle/arch_opcodes/lanes_mn1/mn1_l7_o10_census.sh:0
Research/oracle/arch_opcodes/lanes_mn1/mn1_l8_o10_report.sh:0
Research/oracle/arch_opcodes/lanes_mn1/mn1_l9_o10_guard.sh:0
Research/oracle/arch_opcodes/signatures/ledger_signatures.py:0
Research/oracle/arch_opcodes/signatures/opcode_signatures.py:0
Research/oracle/arch_opcodes/single_opcode_units.py:0
Research/oracle/arch_opcodes/unique_opcodes.py:0
Research/oracle/cross_construction/emulation/per_opcode/per_opcode.py:0
```
Every count is 0 (18 files, run on the laptop from
`~/Programming/PseudoCoupHQ`; `sort` pins the order — `grep` given
several file arguments was measured NOT to keep argument order stable
across repeated runs in this environment). Separately, every verify
lane under `lanes_mn1/` (`mn1_l14_verify.sh` onward) was also read by
eye before submission — none contains the word `exempt` at all; each
is the two-line `cd ... && python3 check_conventions_log_claims.py
--verify` shape.

## §6. The note for the record (deliverable 5)

Any command in an earlier log (208, 220, 223, 225, or their lane
scripts) that reads `.mnemonic` off `single_opcode_units.json`,
`unique_opcodes.json`, `opcode_signatures.json` or
`ledger_signatures.json` would now need `.mnem` to reproduce — those
earlier logs are NOT edited (LAW: "old logs are not edited"). A
reader following one of them after this task should expect a
`KeyError: 'mnemonic'` unless it substitutes `mnem`.

## §7. Verifier tally

Four passes were needed to reach zero DIFFERS, the same shape as o9's
own two-pass and o10's three-pass convergence (logs 223 §"pass 2",
225). Pass 1 (`mn1_l14_verify.sh`) found: the four `git diff` pastes
in §3 were each missing git's own `diff --git`/`index`/`---`/`+++`
header lines (fixed by re-pasting the diff in full); the five count
commands and the three guard commands in §4/§5 used paths relative to
`Research/oracle` or `Research/op_pipeline` rather than
`/projects/PseudoCoupHQ`, the verifier's own working directory for
every command (fixed by writing every path from that root); the
`grep -c exempt` paste in §5 described its own output in prose
(`every line: :0`) instead of pasting it (fixed by pasting the real
run). Pass 2 (`mn1_l15_verify2.sh`) found the `grep -c exempt`
glob (`lanes_mn1/*.sh`) had not been synced to the tower yet (fixed
by a `sync-to`) and, once synced, that plain `grep` given several
file arguments does not keep their argument order stable across
repeated runs in this environment (fixed by piping through `sort`).
Pass 3 (`mn1_l16_verify3.sh`) found that the sorted glob still grows
by one every time a NEW verify lane is added to fix what the PREVIOUS
pass found — an unconverging self-reference — fixed by naming the
eighteen files explicitly (the thirteen non-verify lanes plus the
five generators) instead of globbing `lanes_mn1/`. Pass 4
(`mn1_l17_verify4.sh`), LITERAL, in full (tower log
`~/AirlockRuns/mn1/agent/logs/20260908T221351Z__mn1_l17_verify4.sh.log`):

```
$ python3 Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 DevComms/log_235_task_mn1_mnem_field_rename.md
log_235_task_mn1_mnem_field_rename.md: 22 claims extracted

## log_235_task_mn1_mnem_field_rename.md
   claims 22 | MATCHES 15 | DIFFERS 0 | UNVERIFIABLE 5 | REFUSED 0 | NOT_RERUNNABLE 2
   VERDICT: 15 of 22 claims reproduce; 5 (23%) carry nothing to re-run

   | line | shape | outcome | claim / reason |
   |---|---|---|---|
   | 99 | prose_verification | UNVERIFIABLE | prose_only -- a verification is asserted with nothing beside it |
   | 116 | prose_verification | UNVERIFIABLE | prose_only -- a verification is asserted with nothing beside it |
   | 135 | shell_transcript | MATCHES | `git diff f34a38a0 -- Research/oracle/arch_opcodes/single_opcode_units.py` |
   | 161 | shell_transcript | MATCHES | `git diff f34a38a0 -- Research/oracle/arch_opcodes/unique_opcodes.py` |
   | 234 | shell_transcript | MATCHES | `git diff f34a38a0 -- Research/oracle/arch_opcodes/signatures/opcode_signatures.py` |
   | 287 | shell_transcript | MATCHES | `git diff f34a38a0 -- Research/oracle/arch_opcodes/signatures/ledger_signatures.py` |
   | 338 | shell_transcript | NOT_RERUNNABLE | output_annotated -- the paste carries an arrow gloss (`->`); an exact comparison is impossible |
   | 503 | shell_transcript | MATCHES | single_opcode_units.json narrow-row count |
   | 510 | shell_transcript | MATCHES | unique_opcodes.json cross-language-row count |
   | 515 | shell_transcript | MATCHES | opcode_signatures.json valid/skipped count |
   | 521 | shell_transcript | MATCHES | ledger_signatures.json units-streamed count |
   | 527 | shell_transcript | MATCHES | per_opcode_results.json jobs/LANDED/byte-identical/proved count |
   | 559 | shell_transcript | MATCHES | guard over `unique_opcodes.json` |
   | 566 | shell_transcript | MATCHES | guard over `per_opcode_population.json` |
   | 569 | shell_transcript | MATCHES | guard over `per_opcode_held.json` |
   | 580 | prose_verification | UNVERIFIABLE | prose_only -- a verification is asserted with nothing beside it |
   | 636 | prose_verification | UNVERIFIABLE | prose_only -- a verification is asserted with nothing beside it |
   | 663 | prose_verification | UNVERIFIABLE | prose_only -- a verification is asserted with nothing beside it |
   | 693 | shell_transcript | MATCHES | untruncated local walk, `per_opcode_results.json`, all `landed_mnemonic` |
   | 705 | shell_transcript | MATCHES | untruncated local walk, `single_opcode_units.json`, all `zero_opcode_examples` |
   | 729 | shell_transcript | MATCHES | `grep -c exempt` over the 13 lanes + 5 generators |
   | 771 | shell_transcript | NOT_RERUNNABLE | no_output_pasted -- the command has nothing under it (this line: the verify command itself, necessarily self-referential — see below) |

==============================================================================
SUMMARY, ALL LOGS
==============================================================================
population: 22 claims across 1 logs
  MATCHES          15
  DIFFERS          0
  UNVERIFIABLE     5
  REFUSED          0
  NOT_RERUNNABLE   2

ONE LINE: 15 of 22 claims reproduce; 5 (23%) carry nothing to re-run

causes, by name:
  prose_only                       5
  output_annotated                 1
  no_output_pasted                 1

peak RSS after the pass: 17.4 MB
```

Zero DIFFERS. The two remaining NOT_RERUNNABLE claims are, by cause:
one `git diff` whose own pasted source code contains a literal `->`
inside a format string (`per_opcode.py`'s `say("... -> %s ...")`),
which the checker's own `output_annotated` heuristic reads as a gloss
arrow — a false positive on real source text, not a fabricated
paste; and this section's own verify command, which cannot paste its
own not-yet-produced output — the same self-reference o9's log (223)
and o10's log (225) both carry at their own closing verify step. The
five UNVERIFIABLE claims are prose sentences beside a literal
elsewhere in the same section (the four cause bullets in §5, plus one
summary sentence each in §2 and §4's headline) — never a verification
asserted with nothing beside it anywhere in the log.

## §8. PROGRESS entry

Appended (dated, append-only) to
[`Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_2_single_opcode_units/PROGRESS.md`](file://~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_2_single_opcode_units/PROGRESS.md).

## §9. The two lists

**Decided, recorded for audit:**
- The field the guard already exempts is spelled `mnem`, not
  `mnemonic`; all five generators on this line now write and read it
  that way, and their four json artifacts (`unique_opcodes.json`,
  `per_opcode_population.json`, `per_opcode_held.json`, plus every
  markdown they render) now pass the guard clean where the field
  itself was the cause.
- The rename's scope is the exact key `mnemonic` only; compound
  fields that merely contain the word (`mnemonic_a`, `mnemonic_b`,
  `landed_mnemonic`) and dict-keyed-by-mnemonic structures
  (`signatures.and`, `per_mnemonic.and`, etc.) are a DIFFERENT,
  pre-existing guard cause, left exactly as task o2/o9/o10 already
  left it — not re-litigated, not fixed, not exempted.
- All five headline counts (259 / 162 / 243+16 / 31,078 / 243 with
  197/155/216) are unchanged before vs after regeneration.
- `single_opcode_units.json`'s `zero_opcode_examples` records missing
  a `lang` field (cause D, §5) is a newly-VISIBLE pre-existing defect
  (it was one of the 183 findings the original o2 guard run already
  showed, masked among the larger mnemonic-caused count) — named
  here, not fixed, since fixing it is outside this rename's brief.

**Awaiting the owner:**
- Whether causes A/B/C/D in §5 (the mnem-keyed-dict pattern, the
  `mnemonic_a`/`mnemonic_b` and `landed_mnemonic` compound fields, and
  `single_opcode_units.json`'s `zero_opcode_examples` missing `lang`)
  get their own fix tasks, and in what order — task o2/o9/o10 already
  left A and B open for him; C and D are surfaced by this task for the
  first time as their own named causes.
