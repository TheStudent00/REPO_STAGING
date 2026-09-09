#!/usr/bin/env python3
"""runtime_callee_run.py -- TASK 59 (b), executed and printed.

Locates each toolchain's own runtime archive, extracts the four
routines' bodies, attaches each as an arch unit the caller references,
and writes:

    runtime_callee_units.json              the callee arch units
    runtime_callee_attachments.json        the 308 callers, attached
    out_of_scope_library_calls_superseded.json
    runtime_callee_printed.txt             this run's transcript

Nothing recorded is edited: `out_of_scope_library_calls.json` and the
canon38 stores are READ, and every product is a new file.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation).  No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns.  The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label
on the member.  HISTORY OF VIOLATIONS, so the pattern is visible: (1)
the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25
-- the fix brief itself reintroduced it as "same-operator pairs").
MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste
this paragraph verbatim."

Coding discipline: no compound one-liner statements.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                     # noqa: E402
import runtime_callee as RC                                      # noqa: E402


def family_of(token):
    return canon.FAMILY_OF.get(token)


def say(out, text):
    print(text)
    out.append(text)


def main():
    transcript = []
    engine = RC.RuntimeCallee(family_of=family_of)

    say(transcript, "== THE TOOLCHAINS, ASKED WHERE THEIR OWN "
                    "ARCHIVE IS ==")
    for probe in engine.probes:
        say(transcript, "$ %s" % " ".join(probe.argv))
        if probe.stdout:
            say(transcript, "  %s" % probe.stdout.splitlines()[0])
        if probe.exit_code != 0:
            first = ""
            if probe.stderr:
                first = probe.stderr.splitlines()[0]
            say(transcript, "  exit %d  %s" % (probe.exit_code, first))
    say(transcript, "")
    say(transcript, "archives located, per toolchain:")
    for toolchain in sorted(engine.archive_paths):
        say(transcript, "  %-8s %s"
            % (toolchain, engine.archive_paths[toolchain]))
    for toolchain in sorted(engine.not_located):
        record = engine.not_located[toolchain]
        say(transcript, "  %-8s NOT LOCATED on this machine (%s)"
            % (toolchain, record.get("command",
                                     record.get("archive", ""))))
    say(transcript, "")

    doc = RC.recorded_callers(HERE)
    callers = doc["units"]
    wanted = sorted(set(one["callee"] for one in callers))
    say(transcript, "the recorded list names %d callers over the "
                    "routines %s" % (len(callers), ", ".join(wanted)))
    say(transcript, "")

    say(transcript, "== IS EACH NAME A ROUTINE OF THE COMPILER'S OWN "
                    "RUNTIME? (the archives' own symbol index) ==")
    for callee in wanted:
        yes, where = engine.is_runtime_routine(callee)
        say(transcript, "  %-10s %s   defined in: %s"
            % (callee, "yes" if yes else "no", ", ".join(where)))
    say(transcript, "")

    say(transcript, "== THE BODIES, EXTRACTED ==")
    units = {}
    trouble_by_key = {}
    toolchains_wanted = set()
    for one in callers:
        name = RC.TOOLCHAIN_OF_LANGUAGE.get(one["lang"])
        if name is not None:
            toolchains_wanted.add(name)
    for toolchain in sorted(toolchains_wanted):
        for callee in wanted:
            unit, trouble = engine.extract_callee(callee, toolchain)
            key = "%s/%s" % (toolchain, callee)
            if unit is None:
                trouble_by_key[key] = trouble
                say(transcript, "  %-18s could not be extracted: %s"
                    % (key, trouble))
                continue
            units[key] = unit
            say(transcript, "  %-18s %4d instructions, %5d bytes of "
                            "text, arrival %s"
                % (key, unit["instruction_count"],
                   len(unit["body_bytes"] or ""),
                   ",".join(unit["arrival_families"])))
    say(transcript, "")

    literal_key = None
    for candidate in ("clang/__divti3", "gcc/__divti3"):
        if candidate in units:
            literal_key = candidate
            break
    if literal_key is not None:
        one = units[literal_key]
        say(transcript, "== LITERAL -- one body in full: %s ==" % literal_key)
        say(transcript, "archive: %s" % one["archive"])
        say(transcript, "member:  %s" % one["archive_member"])
        say(transcript, "arrival families (read before written): %s"
            % ", ".join(one["arrival_families"]))
        for index, line in enumerate(one["body_as_read"]):
            say(transcript, "  %3d  %s" % (index, line))
        say(transcript, "")

    say(transcript, "== ATTACHING EACH CALLER ==")
    attachments = {}
    stores = {}
    attached = 0
    no_ledger = 0
    missing = 0
    by_language = {}
    for one in callers:
        language = one["lang"]
        toolchain = RC.TOOLCHAIN_OF_LANGUAGE.get(language)
        key = "%s/%s" % (toolchain, one["callee"])
        callee_unit = units.get(key)
        if callee_unit is None:
            missing = missing + 1
            attachments[one["unit"]] = {
                "unit": one["unit"],
                "lang": language,
                "callee": one["callee"],
                "attached": False,
                "why_not": "no archive for toolchain %r on this "
                           "machine, so the callee's body cannot come "
                           "from the compiler that built the caller"
                           % toolchain,
            }
            continue
        store_path = os.path.join(HERE, one["store"])
        if store_path not in stores:
            stores[store_path] = json.load(open(store_path))
        record = stores[store_path]["units"].get(one["unit"])
        if record is None:
            no_ledger = no_ledger + 1
            attachments[one["unit"]] = {
                "unit": one["unit"],
                "lang": language,
                "callee": one["callee"],
                "attached": False,
                "why_not": "the recorded store carries no unit under "
                           "this name",
            }
            continue
        joined, trouble = engine.attach(record, callee_unit)
        answer_row = None
        for row in joined.get("ledger") or []:
            if row.get("row") == (joined.get("out_row") or "OUT-0"):
                answer_row = row
        attachments[one["unit"]] = {
            "unit": one["unit"],
            "lang": language,
            "callee": one["callee"],
            "attached": trouble == "",
            "why_not": trouble,
            "references": joined.get("runtime_callees"),
            "answer_row": answer_row,
        }
        if trouble == "":
            attached = attached + 1
            by_language[language] = by_language.get(language, 0) + 1
    say(transcript, "callers in the recorded list: %d" % len(callers))
    say(transcript, "attached (answer row now produced by the "
                    "runtime callee): %d" % attached)
    say(transcript, "  by language: %s"
        % json.dumps(by_language, sort_keys=True))
    say(transcript, "not attached, no archive for the caller's own "
                    "toolchain: %d" % missing)
    say(transcript, "not attached, the store carries no such unit: %d"
        % no_ledger)
    say(transcript, "")

    shown = 0
    for name in sorted(attachments):
        record = attachments[name]
        if not record["attached"]:
            continue
        if shown >= 2:
            break
        say(transcript, "LITERAL -- attached caller %s (%s)"
            % (name, record["callee"]))
        say(transcript, "  answer row produced_by: %s"
            % json.dumps(record["answer_row"]["produced_by"],
                         sort_keys=True))
        say(transcript, "  it was:                 %s"
            % json.dumps(record["answer_row"].get("produced_by_was"),
                         sort_keys=True))
        say(transcript, "  references: %s"
            % json.dumps([one["unit"] for one in record["references"]]))
        shown = shown + 1
    say(transcript, "")

    out_units = {
        "meta": {
            "generator": "runtime_callee_run.py",
            "node": "hq.research.compiler_graph.arch_unit."
                    "runtime_callee",
            "what_this_is": "the compiler-runtime routines this "
                            "machine's toolchains ship, extracted "
                            "from their own archives as further arch "
                            "units the callers reference",
            "location_record": engine.location_record(),
            "could_not_extract": trouble_by_key,
        },
        "units": units,
    }
    path = os.path.join(HERE, "runtime_callee_units.json")
    json.dump(out_units, open(path, "w"), indent=1, sort_keys=True)

    out_attach = {
        "meta": {
            "generator": "runtime_callee_run.py",
            "what_this_is": "one entry per caller of the recorded "
                            "list, saying whether its answer row is "
                            "now produced by the runtime callee and "
                            "which callee arch unit it references",
            "source_list": RC.RECORDED_LIST,
            "callers": len(callers),
            "attached": attached,
            "attached_by_language": by_language,
            "not_attached_no_archive": missing,
            "not_attached_no_such_unit": no_ledger,
        },
        "units": attachments,
    }
    path = os.path.join(HERE, "runtime_callee_attachments.json")
    json.dump(out_attach, open(path, "w"), indent=1, sort_keys=True)

    note = RC.supersession_note(doc)
    path = os.path.join(HERE, RC.SUPERSESSION)
    json.dump(note, open(path, "w"), indent=1, sort_keys=True)

    say(transcript, "written: runtime_callee_units.json, "
                    "runtime_callee_attachments.json, %s"
        % RC.SUPERSESSION)
    path = os.path.join(HERE, "runtime_callee_printed.txt")
    open(path, "w").write("\n".join(transcript) + "\n")


main()
