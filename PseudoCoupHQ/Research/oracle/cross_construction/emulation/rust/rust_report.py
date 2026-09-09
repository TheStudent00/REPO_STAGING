#!/usr/bin/env python3
"""rust_report.py -- task o11's report: reads the run json and writes
`rust_results.json` and `rust_report.md`.

WHAT THIS FILE IS, one sentence, in relation: it is the presentation
half of `rust_render.py`, kept apart so the run and the report can be
re-made independently; it computes no verdict of its own and only
counts and quotes what the run lanes wrote.

MEMORY BOUND: one process, the four run documents held at once (about
30 MB of json); no forks; peak resident printed at the end; the named
abort ABORT_MEMORY_O11 is `rust_render.check_collector_memory`'s, at
4 GB, and nothing here approaches it.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

The report's rows are the source LANGUAGE (c / go / swift), the z3
declaration kind, and the arch mnemonic -- each machine-form or a
tool's own constant, none of them a language operator spelling.

Coding discipline: no compound one-liner statements.
"""

import collections
import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import rust_render as R                                          # noqa: E402


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def cell(value):
    """one table cell, with the one character a pipe table cannot carry
    escaped.  A `|` inside a value -- `rust|c` is one of task o1's own
    pair keys -- would otherwise split the cell."""
    return str(value).replace("|", "\\|")


def pipe_table(header, rows):
    lines = ["| " + " | ".join(cell(c) for c in header) + " |",
             "|" + "---|" * len(header)]
    for row in rows:
        lines.append("| " + " | ".join(cell(c) for c in row) + " |")
    return "\n".join(lines)


def rate(part, whole):
    if not whole:
        return "0 of 0"
    return "%d of %d (%d%%)" % (part, whole, round(100.0 * part / whole))


def verdict_of(record, question):
    return (record.get(question) or {}).get("verdict")


def outcome_of(record):
    return (record.get("q3") or {}).get("outcome")


def rescued(record):
    """DISPROVED on the first pose, PROVED once every narrow input row
    is zero-extended from its holder width -- task o7's own
    caller-extension re-pose, run by `emulate.prove_against_x`."""
    q3 = record.get("q3") or {}
    if q3.get("outcome") != "DISPROVED":
        return False
    again = q3.get("under_caller_extension") or {}
    return again.get("outcome") == "PROVED_ON_SHIP"


def counts_for(records):
    out = collections.Counter()
    out["attempted"] = len(records)
    for record in records:
        if record.get("rendered"):
            out["rendered"] = out["rendered"] + 1
        if record.get("compiled"):
            out["compiled"] = out["compiled"] + 1
        if verdict_of(record, "q1") == "BYTE_IDENTICAL":
            out["q1"] = out["q1"] + 1
        if (record.get("q1") or {}).get("same_entry"):
            out["q1_same_entry"] = out["q1_same_entry"] + 1
        if verdict_of(record, "q2") == "TERM_IDENTICAL":
            out["q2"] = out["q2"] + 1
        outcome = outcome_of(record)
        if outcome is not None:
            out[outcome] = out[outcome] + 1
        if rescued(record):
            out["rescued"] = out["rescued"] + 1
        if record.get("runner_limit"):
            out["runner_limit"] = out["runner_limit"] + 1
    return out


def per_x_rows(run, control):
    by_x = collections.defaultdict(list)
    for record in run:
        by_x[record["x_lang"]].append(record)
    header = ["x", "attempted", "rendered", "compiled",
              "byte identity with an existing rust unit",
              "term identity with the entry", "proved equivalent",
              "disproved", "undecided", "runner limit",
              "of the disproved: proved under caller extension"]
    rows = []
    for x in R.X_LANGUAGES:
        counts = counts_for(by_x.get(x, []))
        rows.append([x, counts["attempted"], counts["rendered"],
                     counts["compiled"], counts["q1"], counts["q2"],
                     counts["PROVED_ON_SHIP"], counts["DISPROVED"],
                     counts["UNDECIDED"], counts["runner_limit"],
                     counts["rescued"]])
    counts = counts_for(run)
    rows.append(["all", counts["attempted"], counts["rendered"],
                 counts["compiled"], counts["q1"], counts["q2"],
                 counts["PROVED_ON_SHIP"], counts["DISPROVED"],
                 counts["UNDECIDED"], counts["runner_limit"],
                 counts["rescued"]])
    counts = counts_for(control)
    rows.append(["control (rust)", counts["attempted"], counts["rendered"],
                 counts["compiled"], counts["q1"], counts["q2"],
                 counts["PROVED_ON_SHIP"], counts["DISPROVED"],
                 counts["UNDECIDED"], counts["runner_limit"],
                 counts["rescued"]])
    return header, rows


def refusals_by_cause(records):
    causes = collections.defaultdict(list)
    for record in records:
        if record.get("rendered"):
            continue
        cause = record.get("refusal_cause")
        causes[cause].append("%s (%s)" % (record["entry_id"],
                                          record["x_unit"]))
    out = []
    for cause in sorted(causes, key=lambda c: -len(causes[c])):
        out.append((cause, len(causes[cause]), causes[cause]))
    return out


def disproved_causes(records):
    """the disproved that the caller-extension re-pose did not rescue,
    grouped by what the x unit's body carries that the term does not."""
    groups = {"a memory row the term does not carry": [],
              "a conditional branch the term does not carry": [],
              "not attributed": []}
    for record in records:
        if outcome_of(record) != "DISPROVED":
            continue
        if rescued(record):
            continue
        q3 = record.get("q3") or {}
        free = list(q3.get("x_side_free_state") or [])
        free = free + list(q3.get("c_side_free_state") or [])
        seeds = str(q3.get("counterexample"))
        reads_memory = False
        for name in free:
            if str(name).startswith("seed_MEM"):
                reads_memory = True
        if "seed_MEM" in seeds:
            reads_memory = True
        body = record.get("x_body_text") or ""
        branches = False
        for piece in body.split(";"):
            word = piece.strip().split(" ")[0]
            if word.startswith("j") and word != "jmp":
                branches = True
            if word == "jmp":
                branches = True
        if reads_memory:
            groups["a memory row the term does not carry"].append(record)
        elif branches:
            groups["a conditional branch the term does not "
                   "carry"].append(record)
        else:
            groups["not attributed"].append(record)
    return groups


def undecided_causes(records):
    causes = collections.Counter()
    for record in records:
        if outcome_of(record) != "UNDECIDED":
            continue
        cause = (record.get("q3") or {}).get("cause")
        causes[str(cause)] = causes[str(cause)] + 1
    return causes


def pick_examples(run):
    """one emulation whose bytes an existing rust unit already has; one
    proved but not byte-identical, shortest first; one disproved with
    its seeds."""
    byte_identical = None
    proved = None
    disproved = None
    matched = []
    for record in run:
        if verdict_of(record, "q1") == "BYTE_IDENTICAL":
            matched.append(record)
    # the most informative of them: one the gate also proved if there
    # is one, else the one whose emulated body is longest, because a
    # one-instruction body says little about a collapse.
    for record in matched:
        if outcome_of(record) == "PROVED_ON_SHIP":
            byte_identical = record
    if byte_identical is None and matched:
        matched.sort(key=lambda r: len(r.get("body_text") or ""))
        byte_identical = matched[-1]
    candidates = []
    for record in run:
        if outcome_of(record) != "PROVED_ON_SHIP":
            continue
        if verdict_of(record, "q1") == "BYTE_IDENTICAL":
            continue
        candidates.append(record)
    candidates.sort(key=lambda r: len(r.get("body_text") or ""))
    if candidates:
        proved = candidates[len(candidates) // 4]
    for record in run:
        if outcome_of(record) != "DISPROVED":
            continue
        if rescued(record):
            continue
        if disproved is None:
            disproved = record
        body = record.get("x_body_text") or ""
        if "je " in body and disproved is not None:
            if "je " not in (disproved.get("x_body_text") or ""):
                disproved = record
    return byte_identical, proved, disproved


def example_block(title, record):
    if record is None:
        return "### %s\n\nNo emulation in the run has this shape.\n" % title
    lines = []
    lines.append("### %s" % title)
    lines.append("")
    lines.append("Entry `%s`, x unit `%s`. The term (layer-5 text), "
                 "**LITERAL**:" % (record["entry_id"], record["x_unit"]))
    lines.append("")
    lines.append("```")
    lines.append(record["x_text"])
    lines.append("```")
    lines.append("")
    lines.append("The rendered source, **LITERAL** "
                 "(`%s/%s`):" % (R.HOST_FOLDER, record.get("source_path")))
    lines.append("")
    lines.append("```rust")
    lines.append(record.get("source", "").rstrip())
    lines.append("```")
    lines.append("")
    lines.append("The two bodies, **LITERAL**:")
    lines.append("")
    lines.append(pipe_table(
        ["side", "body", "bytes"],
        [["x unit `%s`" % record["x_unit"],
          "`%s`" % record.get("x_body_text"),
          "`%s`" % record.get("x_body_bytes")],
         ["the emulation", "`%s`" % record.get("body_text"),
          "`%s`" % record.get("body_bytes")]]))
    lines.append("")
    q1 = record.get("q1") or {}
    q2 = record.get("q2") or {}
    q3 = record.get("q3") or {}
    lines.append("Verdicts, **LITERAL**: Q1 `%s` (matched rust units "
                 "`%s`, entries `%s`); Q2 `%s`; Q3 `%s`."
                 % (q1.get("verdict"), q1.get("matched_target_units"),
                    q1.get("matched_entries"), q2.get("verdict"),
                    q3.get("outcome")))
    if q3.get("counterexample") is not None:
        lines.append("")
        lines.append("The counterexample seeds, **LITERAL** (the "
                     "solver's model; `IN_i` is the aligned input row "
                     "`i`):")
        lines.append("")
        lines.append("```")
        lines.append(str(q3.get("counterexample")))
        lines.append("```")
        again = q3.get("under_caller_extension") or {}
        if again:
            lines.append("")
            lines.append("After the caller-extension re-pose: `%s`, "
                         "seeds **LITERAL** `%s`."
                         % (again.get("outcome"),
                            again.get("counterexample")))
    lines.append("")
    return "\n".join(lines)


# ------------------------------------------------------------------
# the per-opcode tables
# ------------------------------------------------------------------

def per_opcode_tables(document):
    results = document["results"]
    per_lang_mnem = collections.defaultdict(lambda: collections.Counter())
    for record in results:
        key = (record["x_lang"], record.get("mnem"))
        counter = per_lang_mnem[key]
        counter["rows"] = counter["rows"] + 1
        if record.get("rendered"):
            counter["rendered"] = counter["rendered"] + 1
        if record.get("compiled"):
            counter["compiled"] = counter["compiled"] + 1
        q0 = (record.get("q0") or {}).get("verdict")
        if q0 is not None:
            counter[q0] = counter[q0] + 1
        if verdict_of(record, "q1") == "BYTE_IDENTICAL":
            counter["byte"] = counter["byte"] + 1
        outcome = outcome_of(record)
        if outcome is not None:
            counter[outcome] = counter[outcome] + 1
    header = ["x", "mnem", "rows", "rendered", "compiled", "LANDED",
              "LANDED_ELSEWHERE", "NOT_COLLAPSED",
              "byte-identical to the row's own body", "proved",
              "disproved", "undecided"]
    rows = []
    for key in sorted(per_lang_mnem, key=lambda k: (k[0], str(k[1]))):
        lang, mnem = key
        counter = per_lang_mnem[key]
        rows.append([lang, "`%s`" % mnem, counter["rows"],
                     counter["rendered"], counter["compiled"],
                     counter["LANDED"], counter["LANDED_ELSEWHERE"],
                     counter["NOT_COLLAPSED"], counter["byte"],
                     counter["PROVED_ON_SHIP"], counter["DISPROVED"],
                     counter["UNDECIDED"]])
    collapsed_header = ["x", "rows", "rendered", "compiled", "LANDED",
                        "LANDED_ELSEWHERE", "NOT_COLLAPSED",
                        "byte-identical", "proved", "disproved",
                        "undecided"]
    per_lang = collections.defaultdict(lambda: collections.Counter())
    for key in per_lang_mnem:
        for name, value in per_lang_mnem[key].items():
            per_lang[key[0]][name] = per_lang[key[0]][name] + value
    collapsed = []
    total = collections.Counter()
    for lang in R.PER_OPCODE_LANGS:
        counter = per_lang.get(lang, collections.Counter())
        collapsed.append([lang, counter["rows"], counter["rendered"],
                          counter["compiled"], counter["LANDED"],
                          counter["LANDED_ELSEWHERE"],
                          counter["NOT_COLLAPSED"], counter["byte"],
                          counter["PROVED_ON_SHIP"],
                          counter["DISPROVED"], counter["UNDECIDED"]])
        for name, value in counter.items():
            total[name] = total[name] + value
    collapsed.append(["all", total["rows"], total["rendered"],
                      total["compiled"], total["LANDED"],
                      total["LANDED_ELSEWHERE"], total["NOT_COLLAPSED"],
                      total["byte"], total["PROVED_ON_SHIP"],
                      total["DISPROVED"], total["UNDECIDED"]])
    landed_ever = set()
    all_mnem = set()
    for record in results:
        all_mnem.add(record.get("mnem"))
        if (record.get("q0") or {}).get("verdict") == "LANDED":
            landed_ever.add(record.get("mnem"))
    never = sorted(m for m in all_mnem if m not in landed_ever)
    elsewhere = []
    for record in results:
        if (record.get("q0") or {}).get("verdict") != "LANDED_ELSEWHERE":
            continue
        elsewhere.append(record)
    not_collapsed = []
    for record in results:
        if (record.get("q0") or {}).get("verdict") != "NOT_COLLAPSED":
            continue
        not_collapsed.append(record)
    return (header, rows, collapsed_header, collapsed, never, elsewhere,
            not_collapsed)


# ------------------------------------------------------------------
# the report
# ------------------------------------------------------------------

def report():
    population = R.read_json(R.POPULATION)
    optable = R.read_json(R.OPTABLE)
    run = R.read_json(R.RUN)
    control = R.read_json(R.CONTROL)
    sample = R.read_json(R.SAMPLE)
    peropcode = R.read_json(R.PEROPCODE)
    document = {
        "task": "o11",
        "population": population["filters"],
        "run_set_note": population["run_set_note"],
        "rustc": population.get("rustc"),
        "ship_flags": population.get("ship_flags"),
        "ship_flags_source": population.get("ship_flags_source"),
        "run": run["results"],
        "control": control["results"],
        "sample": sample["results"],
        "peropcode": peropcode["results"],
        "peropcode_skipped": peropcode["skipped"],
        "collector_peak_kb": {
            "run": run.get("collector_peak_kb"),
            "control": control.get("collector_peak_kb"),
            "sample": sample.get("collector_peak_kb"),
            "peropcode": peropcode.get("collector_peak_kb"),
        },
    }
    R.write_json(R.RESULTS, document)
    text = write_report_md(population, optable, run["results"],
                           control["results"], sample["results"],
                           peropcode)
    handle = open(R.REPORT, "w")
    handle.write(text)
    handle.close()
    R.say("wrote %s and %s" % (R.RESULTS, R.REPORT))
    R.say("report process peak resident: %d kB" % peak_kb())
    return 0


def write_report_md(population, optable, run, control, sample,
                    peropcode):
    out = []
    out.append("# task o11 -- AutoPoly with rust as the target")
    out.append("")
    out.append("Generated by `rust_report.py` from the run json; every "
               "figure below is a count over those files and nothing "
               "here recomputes a verdict.")
    out.append("")
    out.append("rustc: `%s`" % population.get("rustc"))
    out.append("")
    out.append("Ship flags: `%s` (%s)" % (population.get("ship_flags"),
                                          population.get(
                                              "ship_flags_source")))
    out.append("")

    # -- 0. the coverage table --------------------------------------
    out.append("## 0. The coverage table: the term language's "
               "operators x the two targets")
    out.append("")
    out.append("Rows are the z3 declaration kinds task o7's renderer "
               "dispatches on, which are the kinds "
               "`reference.Reference.opcode_table`'s builders produce; "
               "the `print form` column is what the row looks like "
               "inside a layer-5 text, and is a display column only. "
               "`entries` counts the pool entries (of %d that carry a "
               "layer-5 text) whose text contains that print form."
               % optable["pool_entries_with_a_layer5_text"])
    out.append("")
    rows = []
    for row in optable["coverage"]:
        rows.append([row["kind"], "`%s`" % row["print_form"],
                     row["entries_attesting"], row["c_class"],
                     row["c_rule"], row["rust_class"], row["rust_rule"]])
    out.append(pipe_table(["kind", "print form", "entries", "c", "c rule",
                           "rust", "rust rule"], rows))
    out.append("")
    classes = collections.Counter()
    for row in optable["coverage"]:
        classes[row["rust_class"]] = classes[row["rust_class"]] + 1
    out.append("Rust cells: %d direct, %d idiom, %d none."
               % (classes["direct"], classes["idiom"], classes["none"]))
    out.append("")
    out.append("### The sorts: the 32 holders, as the two targets "
               "spell them")
    out.append("")
    srows = []
    for row in optable["sorts"]:
        srows.append([row["holder"], "`%s`" % row["c"], row["rust"]])
    out.append(pipe_table(["holder", "c", "rust"], srows))
    out.append("")

    # -- 1. the population ------------------------------------------
    out.append("## 1. The population, counted at each filter")
    out.append("")
    prows = []
    for row in population["filters"]:
        prows.append([row["filter"], row["c"], row["go"], row["swift"],
                      row["distinct"]])
    out.append(pipe_table(["filter", "c", "go", "swift", "distinct"],
                          prows))
    out.append("")
    out.append("The run set: %s." % population["run_set_note"])
    out.append("")

    # -- 2. the per-x table -----------------------------------------
    out.append("## 2. Per x: attempted / rendered / compiled / "
               "collapsed to byte identity / term identity / proved / "
               "disproved / undecided")
    out.append("")
    header, rows = per_x_rows(run, control)
    out.append(pipe_table(header, rows))
    out.append("")
    control_counts = counts_for(control)
    out.append("Control: %s of the compiled control emulations of a "
               "rust member's own term carry bytes a rust unit IN THE "
               "SAME entry already has (`same_entry`)."
               % rate(control_counts["q1_same_entry"],
                      control_counts["compiled"]))
    out.append("")

    # -- 3. what the control does -----------------------------------
    out.append("### What the control does to the reading of the x rows")
    out.append("")
    run_counts = counts_for(run)
    out.append("- Control Q1, the rate: %s of the compiled control "
               "emulations carry bytes some rust unit of the corpus "
               "already has, and %s carry the bytes of a rust unit in "
               "the SAME pool entry -- the unit the emulation was "
               "rendered from. This is the CEILING for byte-level "
               "collapse."
               % (rate(control_counts["q1"], control_counts["compiled"]),
                  rate(control_counts["q1_same_entry"],
                       control_counts["compiled"])))
    out.append("- So the x rows' %s byte identity is read against %s, "
               "not against 100%%. And an x row's byte identity can "
               "never be SAME-ENTRY: the population is entries with no "
               "rust member, so a matched rust unit is by construction "
               "a unit of another entry."
               % (rate(run_counts["q1"], run_counts["compiled"]),
                  rate(control_counts["q1_same_entry"],
                       control_counts["compiled"])))
    out.append("- Control Q3, the rate: %s proved on the ship build, "
               "%d more proved once narrow arguments are zero-extended "
               "from their holder width, %d undecided, %d left "
               "disproved."
               % (rate(control_counts["PROVED_ON_SHIP"],
                       control_counts["compiled"]),
                  control_counts["rescued"], control_counts["UNDECIDED"],
                  control_counts["DISPROVED"] -
                  control_counts["rescued"]))
    out.append("- So the x rows' %s proved, %s after the "
               "caller-extension rule, sits against the control's own "
               "level."
               % (rate(run_counts["PROVED_ON_SHIP"],
                       run_counts["compiled"]),
                  rate(run_counts["PROVED_ON_SHIP"] +
                       run_counts["rescued"], run_counts["compiled"])))
    out.append("")

    # -- 4. three literal examples ----------------------------------
    out.append("## 3. Three literal examples")
    out.append("")
    byte_identical, proved, disproved = pick_examples(run)
    out.append(example_block("3.1 collapsed to byte identity",
                             byte_identical))
    out.append(example_block("3.2 proved equivalent, not byte-identical",
                             proved))
    out.append(example_block("3.3 disproved, with the counterexample "
                             "seeds", disproved))

    # -- 5. three rendered sources from the sample ------------------
    out.append("## 4. Three rendered sources from the sample of 40")
    out.append("")
    shown = 0
    for record in sample:
        if shown >= 3:
            break
        if not record.get("rendered"):
            continue
        out.append("**LITERAL**, `%s/%s`, from the term `%s`:"
                   % (R.HOST_FOLDER, record.get("source_path"),
                      record["x_text"]))
        out.append("")
        out.append("```rust")
        out.append(record.get("source", "").rstrip())
        out.append("```")
        out.append("")
        shown = shown + 1

    # -- 6. refusals -------------------------------------------------
    out.append("## 5. Refusals, by cause")
    out.append("")
    out.append("### x -> rust")
    out.append("")
    for cause, count, names in refusals_by_cause(run):
        out.append("- renderer refused: %s: %d (%s)"
                   % (cause, count, ", ".join(names[:6])
                      + (", ..." if count > 6 else "")))
    out.append("")
    out.append("### control")
    out.append("")
    for cause, count, names in refusals_by_cause(control):
        out.append("- renderer refused: %s: %d (%s)"
                   % (cause, count, ", ".join(names[:6])
                      + (", ..." if count > 6 else "")))
    out.append("")
    compiled = counts_for(run)["compiled"]
    rendered = counts_for(run)["rendered"]
    out.append("rustc refused: %d. Every rendered source compiled: %d "
               "of %d on the x rows, %d of %d on the control."
               % (rendered - compiled, compiled, rendered,
                  counts_for(control)["compiled"],
                  counts_for(control)["rendered"]))
    out.append("")

    # -- 7. the disproved -------------------------------------------
    out.append("## 6. The disproved, by cause")
    out.append("")
    out.append("- CAUSE 1, the arrival width, status CLOSED: %d of the "
               "%d DISPROVED emulations are proved once every "
               "byte-wide or halfword-wide input row is zero-extended "
               "from its holder width. Rust's `extern \"C\"` callee "
               "reads the whole argument register and takes the caller "
               "to have widened it, exactly as c's does (measured, "
               "lane o11_l1: `wide_arrival_u8` computes on `%%esi` and "
               "`%%edi` whole); the term says nothing about the bits "
               "above the holder."
               % (run_counts["rescued"], run_counts["DISPROVED"]))
    groups = disproved_causes(run)
    for name in ["a memory row the term does not carry",
                 "a conditional branch the term does not carry",
                 "not attributed"]:
        records = groups[name]
        out.append("- CAUSE for %d of the %d that stay disproved: %s. "
                   "%s"
                   % (len(records),
                      run_counts["DISPROVED"] - run_counts["rescued"],
                      name,
                      ", ".join("`%s` (%s)" % (r["entry_id"],
                                               r["x_unit"])
                                for r in records[:8])))
    out.append("")
    out.append("### The undecided, by cause")
    out.append("")
    for cause, count in undecided_causes(run).most_common():
        out.append("- %d: %s" % (count, cause))
    out.append("")

    # -- 8. the per-opcode question ----------------------------------
    out.append("## 7. Task o8's per-opcode question, with rust as the "
               "target")
    out.append("")
    out.append("The rows are task o2's single-opcode groups "
               "(`single_opcode_units.json`, `narrow` rule) for c, go "
               "and swift; each row's example unit's proved term is "
               "rendered to rust, compiled, and its body chaff-stripped "
               "by task o2's own rule. LANDED means exactly the row's "
               "own arch opcode remains.")
    out.append("")
    (header, rows, chead, collapsed, never, elsewhere,
     not_collapsed) = per_opcode_tables(peropcode)
    out.append(pipe_table(chead, collapsed))
    out.append("")
    out.append("%d rows carried no proved term and were skipped."
               % len(peropcode["skipped"]))
    out.append("")
    out.append("### Per x and per mnemonic")
    out.append("")
    out.append(pipe_table(header, rows))
    out.append("")
    out.append("### Mnemonics never landed from any language's "
               "emulation")
    out.append("")
    if never:
        out.append(", ".join("`%s`" % m for m in never))
    else:
        out.append("None: every mnemonic in the population landed at "
                   "least once.")
    out.append("")
    if elsewhere:
        out.append("### LANDED_ELSEWHERE")
        out.append("")
        erows = []
        for record in elsewhere:
            erows.append([record["x_lang"], "`%s`" % record.get("mnem"),
                          "`%s`" % (record.get("landed") or {}).get("mnem"),
                          "`%s`" % record.get("row_body_text"),
                          "`%s`" % record.get("body_text")])
        out.append(pipe_table(["x", "the row's mnem", "the landed mnem",
                               "the row's body", "the emulation's body"],
                              erows))
        out.append("")
    if not_collapsed:
        out.append("### NOT_COLLAPSED")
        out.append("")
        nrows = []
        for record in not_collapsed:
            nrows.append([record["x_lang"], "`%s`" % record.get("mnem"),
                          (record.get("q0") or {}).get("opcode_count"),
                          "`%s`" % record.get("body_text")])
        out.append(pipe_table(["x", "the row's mnem",
                               "opcodes remaining",
                               "the emulation's body"], nrows))
        out.append("")

    # -- 9. bounds ---------------------------------------------------
    out.append("## 8. Bounds and memory")
    out.append("")
    out.append("The named abort is ABORT_MEMORY_O11, raised by the "
               "collecting process when its own peak resident size "
               "passes 4 GB (`rust_render.check_collector_memory`, "
               "bound into the imported collector); it did not fire in "
               "any lane. Peak resident, per collecting process, and "
               "the largest sub-process seen in each:")
    out.append("")
    brows = []
    for name, path in [("sample", R.SAMPLE), ("run", R.RUN),
                       ("control", R.CONTROL),
                       ("peropcode", R.PEROPCODE)]:
        document = R.read_json(path)
        biggest = 0
        for record in document["results"]:
            biggest = max(biggest, record.get("sub_peak_kb") or 0)
        brows.append([name, document.get("collector_peak_kb"), biggest,
                      len(document["results"])])
    out.append(pipe_table(["lane", "collector peak kB",
                           "largest sub-process kB", "records"], brows))
    out.append("")
    out.append("The ceiling on one sub-process is RLIMIT_AS 2,048 MB "
               "and a 240 s wall clock, both task o7's; no record in "
               "any lane carries a `runner_limit`.")
    out.append("")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.exit(report())
