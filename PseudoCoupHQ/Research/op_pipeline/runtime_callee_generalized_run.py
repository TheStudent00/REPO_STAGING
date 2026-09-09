#!/usr/bin/env python3
"""runtime_callee_generalized_run.py -- TASK 63 (a) and (b), executed
and printed.

Node: `hq.research.compiler_graph.arch_unit.runtime_callee`
CORE: Planning/node_0_3_research/node_0_3_5_compiler_graph/
      node_0_3_5_1_arch_unit/node_0_3_5_1_8_runtime_callee/
      CORE_0_3_5_1_8_runtime_callee.md

WHAT IS NEW HERE, against task 59's `runtime_callee_run.py`.  Task 59
attached FOUR names -- the 128-bit division family -- for the 308
units a recorded list named.  The round-12 audit (log_165 §3) found
the population is far larger: every call-bearing unit in canon39
transfers into a routine the toolchain's own builtins archive
defines, and the division family is 9% of it.  So this program:

  1. COUNTS the call-bearing units of canon39 itself, and the callee
     names their bodies spell, off the relocation each `call` line
     carries.  Nothing is typed in; the census is the input.
  2. Asks the archive index whether each name is a runtime routine,
     per toolchain.
  3. Extracts every name that is, WITH ITS NESTED CALLEES followed
     the same way (`extract_closure`), and attaches the caller.
  4. Merges swift's units, extracted inside the `trickle` Airlock
     instance by `runtime_callee_swift_lane.py` -- swift's toolchain
     is not on the host, and the CORE forbids taking a callee from
     another compiler's archive.
  5. Reports attached and NOT attached BY CAUSE, per language.

It re-walks the ledgers of the call-bearing units into NEW files.  It
does not re-gate; that is task 64's.

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

The candidate set here is machine form throughout: a unit is a
candidate because ITS OWN BODY carries a `call` whose relocation
names a symbol the archive index defines.  No operator token is read
by anything.

Coding discipline: no compound one-liner statements.
"""

import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                     # noqa: E402
import runtime_callee as RC                                      # noqa: E402


RELOCATION = re.compile(r"!!reloc=([A-Za-z0-9_]+):([A-Za-z0-9_.$]+)")

SWIFT_LANE_PRODUCT = "canon39_callee_swift_lane.json"

# The four swift callers of the recorded 308-unit list.  They are
# REFUSED in canon39 -- their wrapped text did not prove -- so the
# census over canon39's proved units cannot see them, and log_161
# left them unattached for want of the toolchain.  They are carried
# here so the swift row of the report is the whole swift row.
RECORDED_LIST = "out_of_scope_library_calls.json"


def family_of(token):
    return canon.FAMILY_OF.get(token)


def say(transcript, text):
    print(text)
    sys.stdout.flush()
    transcript.append(text)


# ------------------------------------------------------------------
# part 0 -- the census: which units carry a transfer, and to what
# ------------------------------------------------------------------

def store_paths():
    """every canon39 store, in one list."""
    out = []
    out.extend(sorted(glob.glob(os.path.join(HERE,
                                             "canon39_wrapped_*.json"))))
    out.extend(sorted(glob.glob(os.path.join(
        HERE, "canon39_regen_store", "*.json"))))
    interp = os.path.join(HERE, "canon39_interp.json")
    if os.path.exists(interp):
        out.append(interp)
    return out


def body_of(record):
    body = record.get("body_verbatim")
    if body is None:
        body = record.get("body_as_read")
    if body is None:
        return []
    if isinstance(body, str):
        return body.split(";")
    return list(body)


def callees_of(record):
    """[(callee name or None, the line)] for every transfer line."""
    out = []
    for line in body_of(record):
        text = line.strip()
        if not text.startswith("call"):
            continue
        hit = RELOCATION.search(text)
        if hit is None:
            out.append((None, text))
            continue
        out.append((hit.group(2), text))
    return out


def census(transcript):
    """the call-bearing units of canon39, and the names they spell."""
    units = {}
    counted = 0
    by_language = {}
    for path in store_paths():
        doc = json.load(open(path))
        for name, record in (doc.get("units") or {}).items():
            if not isinstance(record, dict):
                continue
            if record.get("outcome") != "WRAPPED_TEXT_PROVED":
                continue
            counted = counted + 1
            language = record.get("lang")
            by_language[language] = by_language.get(language, 0) + 1
            found = callees_of(record)
            if not found:
                continue
            names = []
            unnamed = []
            for callee, line in found:
                if callee is None:
                    unnamed.append(line)
                    continue
                if callee in names:
                    continue
                names.append(callee)
            units[name] = {
                "unit": name,
                "lang": language,
                "store": os.path.relpath(path, HERE),
                "callees": names,
                "transfers_without_a_relocation": unnamed,
            }
    return units, counted, by_language


def sightings(units):
    """{callee name -> how many units name it}, and the same by
    language."""
    by_name = {}
    by_name_language = {}
    for record in units.values():
        for callee in record["callees"]:
            by_name[callee] = by_name.get(callee, 0) + 1
            key = "%s/%s" % (record["lang"], callee)
            by_name_language[key] = by_name_language.get(key, 0) + 1
        for line in record["transfers_without_a_relocation"]:
            key = "<no relocation> %s" % line
            by_name[key] = by_name.get(key, 0) + 1
    return by_name, by_name_language


# ------------------------------------------------------------------
# part 4 -- the swift units, extracted inside the trickle instance
# ------------------------------------------------------------------

def swift_units(transcript):
    path = os.path.join(HERE, SWIFT_LANE_PRODUCT)
    if not os.path.exists(path):
        say(transcript, "swift: no lane product at %s -- the swift "
                        "callers cannot be attached" % SWIFT_LANE_PRODUCT)
        return {}, {"swiftc": "the lane product is not on disk"}
    doc = json.load(open(path))
    meta = doc.get("meta") or {}
    say(transcript, "swift: the lane ran inside %s"
        % meta.get("ran_inside"))
    say(transcript, "swift: archive, quoted from the toolchain's own "
                    "output: %s" % meta.get("archive"))
    units = doc.get("units") or {}
    say(transcript, "swift: %d callee units carried over" % len(units))
    return units, doc.get("could_not_extract") or {}


# ------------------------------------------------------------------
# the run
# ------------------------------------------------------------------

def main():
    transcript = []
    engine = RC.RuntimeCallee(family_of=family_of)

    say(transcript, "== PART 0 -- THE TOOLCHAINS, ASKED WHERE THEIR "
                    "OWN ARCHIVE IS ==")
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
    for toolchain in sorted(engine.archive_paths):
        say(transcript, "  %-8s %s"
            % (toolchain, engine.archive_paths[toolchain]))
    say(transcript, "")

    say(transcript, "== PART 1 -- THE CENSUS, COMPUTED OFF canon39 ==")
    callers, counted, population = census(transcript)
    say(transcript, "canon39 proved units walked: %d" % counted)
    say(transcript, "  by language: %s"
        % json.dumps(population, sort_keys=True))
    say(transcript, "call-bearing units: %d" % len(callers))
    call_by_language = {}
    for record in callers.values():
        key = record["lang"]
        call_by_language[key] = call_by_language.get(key, 0) + 1
    say(transcript, "  by language: %s"
        % json.dumps(call_by_language, sort_keys=True))
    by_name, by_name_language = sightings(callers)
    say(transcript, "")
    say(transcript, "THE FULL LIST OF NAMES, by how many units spell "
                    "each (computed, not typed):")
    ordered = sorted(by_name.items(), key=lambda one: (-one[1], one[0]))
    for name, count in ordered:
        say(transcript, "  %-76s %5d" % (name, count))
    say(transcript, "")

    say(transcript, "== PART 2 -- IS EACH NAME A ROUTINE OF THE "
                    "COMPILER'S OWN RUNTIME? ==")
    say(transcript, "(machine-form evidence: the archive's own symbol "
                    "index, nm --print-armap)")
    swift, swift_trouble = swift_units(transcript)
    for key in sorted(swift):
        engine.symbol_tables.setdefault("swiftc", {})
    say(transcript, "")
    wanted_by_toolchain = {}
    verdicts = {}
    for record in callers.values():
        toolchain = RC.TOOLCHAIN_OF_LANGUAGE.get(record["lang"])
        for callee in record["callees"]:
            key = "%s/%s" % (toolchain, callee)
            if key in verdicts:
                continue
            if toolchain == "swiftc":
                verdicts[key] = "swiftc/%s" % callee in swift
            else:
                yes, where = engine.is_runtime_routine(callee, toolchain)
                verdicts[key] = yes
            if verdicts[key]:
                wanted_by_toolchain.setdefault(toolchain, [])
                if callee not in wanted_by_toolchain[toolchain]:
                    wanted_by_toolchain[toolchain].append(callee)
    for key in sorted(verdicts):
        say(transcript, "  %-84s %s"
            % (key, "yes" if verdicts[key] else "no"))
    say(transcript, "")

    say(transcript, "== PART 3 -- THE BODIES, EXTRACTED, NESTED "
                    "CALLEES FOLLOWED ==")
    units = {}
    could_not = {}
    seen = set()
    for toolchain in sorted(wanted_by_toolchain):
        if toolchain == "swiftc":
            continue
        for callee in sorted(wanted_by_toolchain[toolchain]):
            got, bad = engine.extract_closure(callee, toolchain, seen)
            units.update(got)
            could_not.update(bad)
    units.update(swift)
    could_not.update(swift_trouble)
    nested_only = []
    for key in sorted(units):
        one = units[key]
        named_by_a_caller = False
        for toolchain in wanted_by_toolchain:
            if one["callee"] in wanted_by_toolchain[toolchain]:
                named_by_a_caller = True
        if not named_by_a_caller:
            nested_only.append(key)
        say(transcript, "  %-30s %4d instructions   nested: %s"
            % (key, one["instruction_count"],
               ",".join(one["nested_callees"]) or "-"))
    say(transcript, "")
    say(transcript, "callee arch units extracted: %d" % len(units))
    say(transcript, "of those, reached ONLY as a nested callee of "
                    "another body: %d  (%s)"
        % (len(nested_only), ", ".join(nested_only) or "none"))
    for key in sorted(could_not):
        say(transcript, "  NOT EXTRACTED %-28s %s"
            % (key, could_not[key]))
    say(transcript, "")

    say(transcript, "== PART 4 -- ATTACHING EVERY CALL-BEARING "
                    "UNIT ==")
    stores = {}
    attachments = {}
    attached_by_language = {}
    refused_by_cause = {}
    for name in sorted(callers):
        record = callers[name]
        language = record["lang"]
        toolchain = RC.TOOLCHAIN_OF_LANGUAGE.get(language)
        chosen = []
        missing = []
        for callee in record["callees"]:
            key = "%s/%s" % (toolchain, callee)
            if key in units:
                chosen.append(units[key])
                continue
            missing.append(callee)
        cause = None
        if record["transfers_without_a_relocation"]:
            cause = ("this body's transfer carries no relocation and "
                     "no archive index defines its target: it is the "
                     "language's own runtime panic path, not the "
                     "compiler's lowering of an operation the "
                     "hardware lacks")
        elif not chosen:
            cause = ("no builtins archive of the caller's own "
                     "toolchain (%s) defines the names this body "
                     "transfers to: %s" % (toolchain,
                                           ", ".join(missing)))
        if cause is not None:
            attachments[name] = {
                "unit": name,
                "lang": language,
                "callees": record["callees"],
                "attached": False,
                "why_not": cause,
            }
            refused_by_cause.setdefault(language, {})
            refused_by_cause[language][cause] = \
                refused_by_cause[language].get(cause, 0) + 1
            continue
        store_path = os.path.join(HERE, record["store"])
        if store_path not in stores:
            stores[store_path] = json.load(open(store_path))
        stored = stores[store_path]["units"].get(name)
        # `record["callees"]` is in the body's own text order, so
        # `chosen` is too, and the LAST transfer is the one that
        # leaves the answer row pointing at it.
        joined = stored
        trouble = ""
        for callee_unit in chosen:
            joined, trouble = engine.attach(joined, callee_unit)
        answer_row = None
        rows = joined.get("ledger") or []
        for row in rows:
            if row.get("row") == (joined.get("out_row") or "OUT-0"):
                answer_row = row
        attachments[name] = {
            "unit": name,
            "lang": language,
            "callees": record["callees"],
            "attached": trouble == "",
            "why_not": trouble,
            "partially": missing,
            "references": joined.get("runtime_callees"),
            "answer_row": answer_row,
            "ledger_rows": len(rows),
        }
        if trouble == "":
            attached_by_language[language] = \
                attached_by_language.get(language, 0) + 1
        else:
            refused_by_cause.setdefault(language, {})
            refused_by_cause[language][trouble] = \
                refused_by_cause[language].get(trouble, 0) + 1

    total_attached = sum(attached_by_language.values())
    say(transcript, "call-bearing units: %d" % len(callers))
    say(transcript, "ATTACHED: %d" % total_attached)
    say(transcript, "  by language: %s"
        % json.dumps(attached_by_language, sort_keys=True))
    say(transcript, "NOT ATTACHED, BY CAUSE, PER LANGUAGE:")
    for language in sorted(refused_by_cause):
        for cause in sorted(refused_by_cause[language]):
            say(transcript, "  %-6s %5d  %s"
                % (language, refused_by_cause[language][cause], cause))
    say(transcript, "")

    say(transcript, "== PART 5 -- THE FOUR SWIFT CALLERS OF THE "
                    "RECORDED 308-UNIT LIST ==")
    say(transcript, "(they are REFUSED in canon39, so the census over "
                    "canon39's PROVED units cannot see them; log_161 "
                    "left them unattached for want of the toolchain)")
    recorded = json.load(open(os.path.join(HERE, RECORDED_LIST)))
    extra = {}
    for one in recorded["units"]:
        if one["lang"] != "swift":
            continue
        key = "swiftc/%s" % one["callee"]
        callee_unit = units.get(key)
        if callee_unit is None:
            extra[one["unit"]] = {
                "unit": one["unit"],
                "lang": "swift",
                "callees": [one["callee"]],
                "attached": False,
                "why_not": "the swift lane extracted no %s"
                           % one["callee"],
            }
            say(transcript, "  %-18s NOT ATTACHED" % one["unit"])
            continue
        store_path = os.path.join(HERE, one["store"].replace(
            "canon38_regen_store", "canon39_regen_store"))
        if not os.path.exists(store_path):
            store_path = os.path.join(HERE, one["store"])
        if store_path not in stores:
            stores[store_path] = json.load(open(store_path))
        stored = stores[store_path]["units"].get(one["unit"])
        if stored is None:
            extra[one["unit"]] = {
                "unit": one["unit"],
                "lang": "swift",
                "callees": [one["callee"]],
                "attached": False,
                "why_not": "the store carries no unit under this name",
            }
            say(transcript, "  %-18s NOT ATTACHED (no such unit)"
                % one["unit"])
            continue
        joined, trouble = engine.attach(stored, callee_unit)
        extra[one["unit"]] = {
            "unit": one["unit"],
            "lang": "swift",
            "callees": [one["callee"]],
            "attached": trouble == "",
            "why_not": trouble,
            "callee_body_referenced": bool(
                joined.get("runtime_callees")),
            "references": joined.get("runtime_callees"),
            "outcome_in_canon39": stored.get("outcome"),
        }
        say(transcript, "  %-18s %-12s outcome in canon39: %-9s  "
                        "callee body referenced: %s   answer row "
                        "repointed: %s"
            % (one["unit"], one["callee"], stored.get("outcome"),
               bool(joined.get("runtime_callees")),
               trouble == "" or trouble))
    say(transcript, "")

    say(transcript, "== PART 6 -- LITERAL: cpp/regen_12920 WITH ITS "
                    "CALLEE BODY ATTACHED ==")
    show = attachments.get("cpp/regen_12920")
    if show is not None:
        for line in printed_unit(stores, units, "cpp/regen_12920",
                                 show):
            say(transcript, line)
    say(transcript, "")

    out_units = {
        "meta": {
            "generator": "runtime_callee_generalized_run.py",
            "node": "hq.research.compiler_graph.arch_unit."
                    "runtime_callee",
            "what_this_is": "every routine of a toolchain's own "
                            "builtins archive that a canon39 body "
                            "transfers to, extracted as a further "
                            "arch unit, with the routines THOSE "
                            "bodies transfer to followed the same way",
            "location_record": engine.location_record(),
            "swift_lane_product": SWIFT_LANE_PRODUCT,
            "could_not_extract": could_not,
            "reached_only_as_a_nested_callee": nested_only,
        },
        "units": units,
    }
    write(os.path.join(HERE, "canon39_callee_units.json"), out_units)

    out_attach = {
        "meta": {
            "generator": "runtime_callee_generalized_run.py",
            "what_this_is": "one entry per call-bearing canon39 unit: "
                            "whether its answer row is now produced by "
                            "a runtime callee, which callee arch units "
                            "it references, and when not, the cause",
            "population": "canon39, the %d units whose wrapped text "
                          "proved" % counted,
            "call_bearing": len(callers),
            "attached": total_attached,
            "attached_by_language": attached_by_language,
            "not_attached_by_cause_per_language": refused_by_cause,
            "the_four_recorded_swift_callers": extra,
        },
        "units": attachments,
    }
    write(os.path.join(HERE, "canon39_callee_attachments.json"),
          out_attach)

    out_census = {
        "meta": {
            "generator": "runtime_callee_generalized_run.py",
            "what_this_is": "the census this run is driven by: which "
                            "canon39 units carry a transfer, and which "
                            "names their relocations spell",
            "population": counted,
            "population_by_language": population,
            "call_bearing": len(callers),
            "call_bearing_by_language": call_by_language,
            "sightings_by_name": by_name,
            "sightings_by_language_and_name": by_name_language,
        },
        "units": callers,
    }
    write(os.path.join(HERE, "canon39_callee_census.json"), out_census)

    path = os.path.join(HERE, "canon39_callee_printed.txt")
    open(path, "w").write("\n".join(transcript) + "\n")
    print("written: canon39_callee_units.json, "
          "canon39_callee_attachments.json, "
          "canon39_callee_census.json, canon39_callee_printed.txt")


def printed_unit(stores, units, name, attachment):
    """the caller's own body, then the callee body attached to it,
    labelled LITERAL and GLOSS."""
    out = []
    stored = None
    for doc in stores.values():
        if name in doc.get("units", {}):
            stored = doc["units"][name]
    if stored is None:
        out.append("  (the store holding %s was not opened in this "
                   "run)" % name)
        return out
    out.append("LITERAL -- %s, the caller's own body as stored "
               "(`body_verbatim`):" % name)
    for index, line in enumerate(stored.get("body_verbatim") or []):
        out.append("  %3d  %s" % (index, line))
    out.append("")
    out.append("GLOSS -- line 3 transfers into the compiler's own "
               "half-float widening routine, and line 8 into its "
               "narrowing routine; the relocation is the only place "
               "either name survives, because an unlinked `call` "
               "disassembles as a transfer inside the unit.")
    out.append("")
    for reference in attachment.get("references") or []:
        key = reference["unit"]
        one = None
        for candidate in units.values():
            if candidate["unit"] == key:
                one = candidate
        if one is None:
            continue
        out.append("LITERAL -- the attached callee %s:" % key)
        out.append("  archive: %s" % one["archive"])
        out.append("  member:  %s" % one["archive_member"])
        out.append("  symbol at 0x%x, size 0x%x"
                   % (one["symbol_address"], one["symbol_size"]))
        out.append("  arrival families (read before written): %s"
                   % ", ".join(one["arrival_families"]))
        for index, line in enumerate(one["body_as_read"]):
            out.append("  %3d  %s" % (index, line))
        out.append("")
    row = attachment.get("answer_row")
    if row is not None:
        out.append("LITERAL -- the caller's answer row, after "
                   "attachment:")
        out.append("  produced_by: %s"
                   % json.dumps(row.get("produced_by"), sort_keys=True))
        out.append("  it was:      %s"
                   % json.dumps(row.get("produced_by_was"),
                                sort_keys=True))
    return out


def write(path, doc):
    json.dump(doc, open(path, "w"), indent=1, sort_keys=True)


main()
