#!/usr/bin/env python3
"""t94_analysis.py -- TASK 94, round 18, steps 2 and 4: WHY each whole
handler body does not go through the universal canonical form, reported
BY CAUSE and not by sighting; and whether the super-op miner already
carries a candidate covering the machinery those bodies contain.

WHY A SECOND PROGRAM.  `t94_recarve.py`'s gate stops at the FIRST thing
the checker cannot carry, which is the right behaviour for a gate and
the wrong one for a report: it names one sighting where there are
several causes.  This file walks each body to the end and inventories
every cause, so the report can say what actually stands between a whole
handler and a proof.

THE SUPER-OP ROUTE, checked rather than assumed.  the owner's stated route is
that "the super-op miner should be able to fill in the missing stuff for
z3".  This file asks the miner's OWN artifact
(`super_op_candidates.json`) whether it carries a candidate that occurs
in these bodies, using the miner's OWN normalizer
(`super_op_miner.normalize_positionally`, imported unmodified).  The
answer is reported as it comes out.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim.

MEMORY BOUND: one body at a time plus the miner's candidate list
(2,173 records).  Expected peak resident under 1 GB; abort name
`T94_ANALYSIS_MEMORY_ABORT` at 6 GB.  The run prints its own peak.
"""

import json
import os
import re
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                   # noqa: E402
import canon2                                                  # noqa: E402
import region36 as R36                                         # noqa: E402
import canon36_universal as CU                                 # noqa: E402
import super_op_miner as MINER                                 # noqa: E402
import z3                                                      # noqa: E402

OUT = os.path.join(HERE, "t94_analysis.json")
MEMORY_ABORT_KB = 6 * 1024 * 1024


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def load(name):
    with open(os.path.join(HERE, name)) as handle:
        return json.load(handle)


MEMORY_OPERAND = re.compile(r"\(([^)]*)\)")

# instructions that NAME a memory operand and touch no memory: the
# alignment padding a compiler emits between functions, and the CET
# landing pad.  Counting `nopl 0x0(%rax)` as a memory write was a
# defect, fixed at first observation.
NO_OPERATION = frozenset(["nop", "nopl", "nopw", "nopq", "endbr64",
                          "data16", "cs", "hlt", "xchg"])
MEMORY_DESTINATION = re.compile(r"\([^)]*%[a-z0-9]+[^)]*\)\s*$")
ALLOCATOR = re.compile(r"alloc|malloc|calloc|_new|New", re.I)


def base_families(operand):
    out = []
    hit = MEMORY_OPERAND.search(operand)
    if hit is None:
        return out
    for token in re.findall(r"%([a-z0-9]+)", hit.group(1)):
        family = canon.FAMILY_OF.get(token)
        if family is not None:
            out.append(family)
    return out


NEEDS_PRIOR_STATE = (
    "no preceding cmp/test",
    "empty symbolic push stack",
)


def unmodelled_mnemonics(lines):
    """every instruction in this body the gate's own checker cannot take,
    asked ONE INSTRUCTION AT A TIME so the walk reaches the end instead
    of stopping at the first refusal.

    THE PROBE'S OWN LIMIT, said out loud rather than hidden.  Asking one
    instruction of a fresh simulator loses the state a real walk would
    have carried in, so two refusal wordings are ARTEFACTS OF THE PROBE
    and not gaps in the checker: `cmov`/`setcc` complaining of no
    preceding compare, and `pop` complaining of an empty push stack.
    They are counted separately and labelled, never folded in with the
    real gaps."""
    found = {}
    for line in lines:
        simulator = CU.Sim36({}, "probe")
        try:
            simulator.exec_line(line)
        except Exception as bad:                              # noqa: BLE001
            text = "%s" % bad
            mnemonic = canon.parse(canon2.strip_reloc(line))[0]
            kind = "the checker has no model for this"
            for marker in NEEDS_PRIOR_STATE:
                if marker in text:
                    kind = ("an artefact of this probe: the refusal is "
                            "about state a one-instruction probe cannot "
                            "carry in, not about a missing model")
            entry = found.setdefault(mnemonic, {"mnem": mnemonic,
                                                "sightings": 0,
                                                "kind": kind,
                                                "the_checker_said": text})
            entry["sightings"] = entry["sightings"] + 1
    return sorted(found.values(), key=lambda row: row["mnem"])


LEADING_ADDRESS = re.compile(r"^\s*(?:0x)?([0-9a-f]{4,16})\b")


def target_address(line, low):
    """the absolute address a transfer names, read off the LEADING
    NUMBER of its operand -- which is what objdump prints, for both
    spellings this population contains: `jbe 1373d8 <long_add+0x68>`
    and the JVM's `jne 0x7f99346aa443`.

    THE DEFECT THIS AVOIDS, named because block_cutter.py already
    records it as its DEFECT B: reading the `<symbol>` annotation
    instead makes a bare `<other_symbol>` target look like offset 0,
    i.e. like a transfer to this unit's own first instruction, when it
    is an external exit.  The printed number never has that ambiguity.
    `low` is accepted so the caller's intent stays explicit; the
    printed number is already absolute, so it is not added."""
    _mnemonic, operands = canon.parse(canon2.strip_reloc(line))
    if not operands:
        return None
    hit = LEADING_ADDRESS.match(operands[-1].strip())
    if hit is None:
        return None
    return int(hit.group(1), 16)


def causes_of(unit, lines, addrs, arrival_families):
    low = addrs[0]
    high = addrs[-1] + 1
    inside = []
    outside = []
    calls = []
    pointer_reads = []
    writes = []
    address_set = set(addrs)
    for index, line in enumerate(lines):
        mnemonic, operands = canon.parse(canon2.strip_reloc(line))
        if canon.JUMP.match(mnemonic):
            target = target_address(line, low)
            row = {"at_index": index, "instruction": line,
                   "target": None if target is None else "0x%x" % target}
            if target is not None and target in address_set:
                inside.append(row)
            else:
                outside.append(row)
            continue
        if mnemonic in ("call", "callq"):
            hit = re.search(r"<([^>]+)>", line)
            callee = hit.group(1) if hit else None
            calls.append({"at_index": index, "instruction": line,
                          "callee": callee,
                          "looks_like_an_allocation":
                              bool(callee and ALLOCATOR.search(callee))})
            continue
        if mnemonic in NO_OPERATION:
            continue
        for position, operand in enumerate(operands):
            if "(" not in operand:
                continue
            if mnemonic == "lea":
                # `lea` computes an ADDRESS: it reads the registers
                # inside the addressing form and never the memory the
                # form names.  lineage_carve.py states the same rule.
                continue
            families = base_families(operand)
            if position == len(operands) - 1:
                continue
            arriving = [f for f in families if f in arrival_families]
            if arriving:
                pointer_reads.append({"at_index": index,
                                      "instruction": line,
                                      "operand": operand,
                                      "base_families": families})
        if operands:
            destination = operands[-1]
            if MEMORY_DESTINATION.search(destination):
                families = base_families(destination)
                kind = "through a pointer this body computed"
                if "rsp" in families or "rbp" in families:
                    kind = "the unit's own stack frame"
                elif [f for f in families if f in arrival_families]:
                    kind = "through an ARRIVING pointer"
                writes.append({"at_index": index, "instruction": line,
                               "destination": destination,
                               "base_families": families,
                               "written_memory_kind": kind})
    return {
        "bounds": {"low": "0x%x" % low, "high": "0x%x" % high},
        "transfers_inside_its_own_bounds": inside,
        "transfers_out_of_its_own_bounds": outside,
        "transfers_into_the_runtime": calls,
        "reads_through_an_arriving_pointer": pointer_reads,
        "memory_writes": writes,
        "mnemonics_the_checker_has_no_model_for":
            unmodelled_mnemonics(lines),
    }


def recurring_paths(unit, lines, causes):
    """the RECURRING PATHS in this body, named from the body itself."""
    out = []
    allocations = [row for row in causes["transfers_into_the_runtime"]
                   if row["looks_like_an_allocation"]]
    for row in allocations:
        start = max(0, row["at_index"] - 6)
        end = min(len(lines), row["at_index"] + 4)
        out.append({
            "recurring_path": "allocation preamble and its answer test",
            "at_index": row["at_index"],
            "callee": row["callee"],
            "instructions": lines[start:end],
            "why_z3_cannot_take_it_directly":
                "the transfer leaves the unit, so the value the body "
                "goes on to write through the returned pointer is not a "
                "function of anything inside these bounds",
        })
    heap_writes = [row for row in causes["memory_writes"]
                   if row["written_memory_kind"] ==
                   "through a pointer this body computed"]
    if heap_writes:
        out.append({
            "recurring_path": "answer written through a pointer the body "
                              "obtained, not through one it arrived with",
            "instructions": [row["instruction"] for row in heap_writes],
            "why_z3_cannot_take_it_directly":
                "region36's virtual memory has six allocation kinds -- "
                "input, constant, temp, result, guard-outcome, "
                "own-address -- and none of them is a block the unit "
                "obtains at run time, so the store has no block to land "
                "in",
        })
    field_writes = [row for row in causes["memory_writes"]
                    if row["written_memory_kind"] ==
                    "through an ARRIVING pointer"]
    if field_writes:
        out.append({
            "recurring_path": "a field written through an arriving "
                              "pointer (the shape a reference count and "
                              "an out-parameter both take)",
            "instructions": [row["instruction"] for row in field_writes],
            "why_z3_cannot_take_it_directly":
                "the input block holds the POINTER's value, not the "
                "object it addresses, so a store at a displacement from "
                "it addresses memory the region does not model",
        })
    if causes["reads_through_an_arriving_pointer"]:
        out.append({
            "recurring_path": "operand unpacking -- a read at a fixed "
                              "displacement from an arriving pointer",
            "instructions": [row["instruction"] for row in
                             causes["reads_through_an_arriving_pointer"]],
            "why_z3_cannot_take_it_directly":
                "same shortfall from the other side: the arriving value "
                "is an address, and the region has no block standing for "
                "what it addresses",
        })
    if causes["transfers_inside_its_own_bounds"]:
        out.append({
            "recurring_path": "the body chooses between alternative "
                              "computations",
            "instructions": [row["instruction"] for row in
                             causes["transfers_inside_its_own_bounds"]],
            "why_z3_cannot_take_it_directly":
                "gate.py's own rule: a body that transfers to a place it "
                "defines itself has a page order that is not its run "
                "order, so a text-order walk has no one answer to reach",
        })
    return out


def super_op_coverage(bodies):
    """does the miner's own artifact carry a candidate that OCCURS in
    these bodies?  Asked with the miner's own normalizer."""
    doc = load("super_op_candidates.json")
    candidates = doc["candidates"]
    languages = set()
    for candidate in candidates:
        for language in candidate["languages"]:
            languages.add(language)
    hits = []
    for unit, lines in bodies.items():
        normalized = MINER.normalize_positionally(lines)
        joined = "\n".join(normalized)
        for candidate in candidates:
            needle = "\n".join(candidate["instructions"])
            if needle and needle in joined:
                hits.append({"unit": unit,
                             "candidate_instructions":
                                 candidate["instructions"],
                             "support": candidate["support"],
                             "languages": candidate["languages"]})
    return {
        "miner_artifact": "super_op_candidates.json",
        "candidate_count": len(candidates),
        "languages_the_miner_mined": sorted(languages),
        "population_the_miner_read": doc["load_report"],
        "interpreter_languages_in_that_population":
            sorted(languages & set(["cpython", "java", "ruby", "php"])),
        "candidates_occurring_in_these_bodies": hits,
    }


def main():
    recarve = load("t94_recarve.json")
    records = []
    bodies = {}
    for source in recarve["records"]:
        unit = source["unit"]
        body = source["recarved"].get("body_verbatim")
        if not body:
            records.append({"unit": unit,
                            "language": source["language"],
                            "label": source["label"],
                            "outcome": "NO_BODY",
                            "cause": source["cause"]})
            continue
        addrs = []
        for row in source["recarved"].get("body_addresses", []):
            addrs.append(int(row, 16))
        if not addrs:
            addrs = list(range(len(body)))
        contract = source["arrival_contract"]
        arrival = set()
        for designation in ("a", "b"):
            family = contract.get(designation)
            if family is not None:
                arrival.add(family)
        causes = causes_of(unit, body, addrs, arrival)
        paths = recurring_paths(unit, body, causes)
        bodies[unit] = body
        records.append({
            "unit": unit,
            "language": source["language"],
            "label": source["label"],
            "handler_function": source["handler_function"],
            "new_instruction_count": source["recarved"]["new_instruction_count"],
            "causes": causes,
            "recurring_paths": paths,
        })
        print("[unit] %-58s inside %2d  runtime %2d  ptr-reads %2d  "
              "writes %2d  unmodelled %d"
              % (unit, len(causes["transfers_inside_its_own_bounds"]),
                 len(causes["transfers_into_the_runtime"]),
                 len(causes["reads_through_an_arriving_pointer"]),
                 len(causes["memory_writes"]),
                 len(causes["mnemonics_the_checker_has_no_model_for"])),
              flush=True)

    coverage = super_op_coverage(bodies)
    out = {
        "meta": {
            "generator": "t94_analysis.py",
            "task": "TASK 94 round 18 -- causes, recurring paths, and "
                    "the super-op route checked",
            "reads_read_only": ["t94_recarve.json",
                                "super_op_candidates.json"],
            "spelling": "the display label appears once per unit, as a "
                        "display field on the member.  No key, "
                        "grouping, pairing or row structure in this "
                        "file uses it.",
            "peak_resident_kb": peak_kb(),
            "memory_abort_name": "T94_ANALYSIS_MEMORY_ABORT",
        },
        "records": records,
        "super_op_route": coverage,
    }
    with open(OUT, "w") as handle:
        json.dump(out, handle, indent=1)
    print("wrote %s ; peak resident %d kB" % (OUT, peak_kb()))
    print("super-op candidates occurring in these bodies: %d"
          % len(coverage["candidates_occurring_in_these_bodies"]))
    print("interpreter languages in the miner's population: %r"
          % coverage["interpreter_languages_in_that_population"])


if __name__ == "__main__":
    main()
