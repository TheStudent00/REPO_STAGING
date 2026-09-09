#!/usr/bin/env python3
"""ledger_signatures.py -- task o10: the opcode signature census from
LEDGER rows -- signatures for the 137 mnemonics task o9's
single-opcode population had no row for.

Node: hq.research.arch_unit_oracle.cross_construction.single_opcode_units
(`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/
node_0_3_2_2_cross_construction/node_0_3_2_2_2_single_opcode_units/`).
Framing: `DevComms/log_221_opcode_signature_algebra.md`. Population and
join method: `DevComms/log_223_task_o9_opcode_signature_census.md` and
its script `signatures/opcode_signatures.py` -- IMPORTED here (as
`OS`), never forked, for every piece of logic that is shape-compatible
with this task's own table.

THE OBJECT, one sentence, in relation to o9's. o9's population was
`single_opcode_units.json`'s 259 NARROW rows (a unit whose WHOLE body
is exactly one arch-opcode instruction) for 5 compiled languages --
25 of 162 mnemonics ever appear that way. o10's population is every
ledger row of every canon40 unit, of ANY body length, across all 9
languages and the interpreters -- every row with
`produced_by.kind == "arch_opcode"` is one occurrence of its mnemonic,
whatever else that unit's body also does. This is why o10 can carry
signatures for the other 137 mnemonics: `cmp`/`test` (a value-producing
row of type "flags only" inside a larger body), `idiv`/`div`, the x87
stack, the SIMD compares, `call` -- none of them ever survive o2's
"chaff-strip to one instruction" rule alone, but every one of them
still writes a ledger row when it runs.

THE HOLDER RULE (the brief's own words, generalized once, stated
here). "Holder class comes from `types101_entry_holders.json` for IN
rows (the unit's pool entry's input holders) and from the row's own
`type` for TEMP rows (width only; class 'unknown' unless the row's
type says it)." The brief names two block kinds; canon40's ledger has
eight (`IN TEMP OUT CONST GUARD OWN STACK X87`, measured in this
task's own exploration lane, `lanes_o10/o10_l1_explore.sh`). DECIDED,
recorded for audit (not asked, because it is mechanical, not
structural): every block OTHER than IN is given TEMP's own rule --
width from its own `size`, class "unknown" unless the `type` STRING
itself names one (`flag`, `vector`, `stack address`, `x87 stack
value`, `literal`). This is a generalization of the stated TEMP rule
to the six block kinds the brief did not name individually, not a new
rule: OUT/CONST/OWN/STACK/X87 rows carry the exact same generic,
width-only `type` strings TEMP rows do (`"8-byte general value"`,
never `"8-byte SIGNED value"`) -- there is no richer source for them
the way `types101_entry_holders.json` is a richer source for IN. The
one place this reads differently from o9: o9 additionally read a
unit's OWN `result_holder` (a DWARF-classed answer type) onto its
OUT-0 row, because o9's population was single-instruction bodies where
the produced row's DWARF answer type was already the thing being
censused. o10 does not carry that enrichment onto OUT here, following
the brief's literal two-block wording; every produced value from an
arch-opcode row (TEMP or OUT) is classed by its own ledger `type`
alone. Where this changes what is visible relative to o9, it is named
in the report, never silently.

MEMORY BOUND: one process, no forked workers. `types101_entry_holders
.json` (14 MB) and `the_families5.json` (0.2 MB) are held whole; the
~332 canon40 shards (259 MB total) are streamed one at a time via
`term66_run.shards()` (imported, never forked) and dropped after each
-- only per-mnemonic-signature counters, small evidence dicts, and
per-mnemonic unit-id sets survive across shards. Named abort
`ABORT_MEMORY_O10` at 2 GB resident (`resource.getrusage`), checked
after every shard.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
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
line MUST paste this paragraph verbatim."

This task's grouping key is `mnemonic` -- the same permitted key task
o2, o8 and o9 used, inheriting the same open item (the four mnemonics
`and`/`or`/`xor`/`not` are ALSO banned operator spellings and trip the
guard on this key for that reason alone; not re-litigated here, see
the report's two-list rule).

Coding discipline: no compound one-liner statements.

usage:
  ledger_signatures.py census    the whole census -> ledger_signatures.json
  ledger_signatures.py report    ledger_signatures.json -> .md
"""

import collections
import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARCH_OPCODES = os.path.normpath(os.path.join(HERE, ".."))
OP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "op_pipeline"))
sys.path.insert(0, OP)
sys.path.insert(0, HERE)

import term66_run as TR  # noqa: E402  -- imported for .shards() only
import opcode_signatures as OS  # noqa: E402  -- imported, not forked

UNIQUE_OPCODES_JSON = os.path.join(ARCH_OPCODES, "unique_opcodes.json")
ENTRY_HOLDERS_JSON = os.path.join(OP, "types101_entry_holders.json")
FAMILIES_JSON = os.path.join(OP, "the_families5.json")

OUT_JSON = os.path.join(HERE, "ledger_signatures.json")
OUT_MD = os.path.join(HERE, "ledger_signatures.md")

ABORT_MEMORY_O10_KB = 2 * 1024 * 1024

# the class words a non-IN row's own `type` string can state, read off
# this task's own exploration lane (o10_l1_explore.sh): 12 distinct
# `type` strings over the whole corpus, none of them a DW_ATE_* class.
TYPE_CLASS_WORDS = [
    ("flag", "flag"),
    ("vector", "vector"),
    ("stack address", "pointer"),
    ("x87 stack value", "x87"),
]


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_collector_memory():
    used = peak_kb()
    if used > ABORT_MEMORY_O10_KB:
        raise SystemExit(
            "ABORT_MEMORY_O10: collector peak %d kB exceeds the stated "
            "2 GB bound" % used)
    return used


def class_from_type_string(type_string):
    """the class a non-IN row's own `type` field states, "unknown"
    unless one of the words in TYPE_CLASS_WORDS appears in it. Exact
    match for "literal" (the CONST block's own `type`, stated whole,
    not a substring of anything else in the 12-string inventory)."""
    if type_string is None:
        return "unknown"
    if type_string == "literal":
        return "literal"
    for word, label in TYPE_CLASS_WORDS:
        if word in type_string:
            return label
    return "unknown"


def holder_for_row(row, parameter_holders):
    """this task's own holder string for one ledger row: an IN row
    with an in-range position in the unit's DWARF parameter list reads
    that holder verbatim (a `DW_ATE_*|width` string, task o9's own
    format, comparable to it); every other row (including an IN row
    past that range -- a machine-level register read with no DWARF
    parameter behind it, see the report's op_105 walkthrough) reads
    `class_from_type_string(type) + "|" + size`."""
    if row["block"] == "IN" and parameter_holders is not None:
        index = row["index"]
        if index < len(parameter_holders):
            return parameter_holders[index]
    return "%s|%d" % (class_from_type_string(row.get("type")), row["size"])


def build_unit_row_info(record, parameter_holders):
    row_info = {}
    for row in record.get("ledger") or []:
        row_info[row["row"]] = holder_for_row(row, parameter_holders)
    return row_info


# ==================================================================
# section 1: the stream -- every ledger row of every canon40 unit
# ==================================================================

def census_pass(unit_to_holders, all_mnemonics):
    """one stream over every canon40 shard. Per mnemonic, per
    signature: occurrence count (every arch_opcode row), unit count
    (units contributing at least one occurrence, deduped per unit as
    it streams -- no unit id list is kept past its own shard except
    up to 3 examples per signature). Also: which units ever produce
    the mnemonic at all (`mnem_to_units`, for the family join in
    section 3) and which mnemonics are ever seen ANYWHERE in a
    ledger row (`seen_anywhere`, `seen_as_flag_pair_element`) -- both
    needed for the "never produces its own ledger row" category
    (deliverable 1's last part)."""
    wanted = set(all_mnemonics)
    table = collections.defaultdict(
        lambda: collections.defaultdict(
            lambda: {"occurrence_count": 0, "unit_count": 0,
                     "example_units": []}))
    mnem_to_units = collections.defaultdict(set)
    seen_anywhere = set()
    seen_as_flag_pair_element = set()
    unresolved_operand_refs = collections.Counter()
    units_seen = 0
    shard_count = 0
    shard_paths = TR.shards()
    total_shards = len(shard_paths)

    for path in shard_paths:
        shard_count += 1
        document = OS.read_json(path)
        for unit_id, record in document["units"].items():
            units_seen += 1
            holders = unit_to_holders.get(unit_id)
            parameter_holders = (holders["parameter_holders"]
                                  if holders is not None else None)
            row_info = build_unit_row_info(record, parameter_holders)
            local_signatures_seen = set()
            for row in record.get("ledger") or []:
                produced_by = row.get("produced_by") or {}
                kind = produced_by.get("kind")
                mnem = produced_by.get("mnem")
                if isinstance(mnem, list):
                    for element in mnem:
                        seen_anywhere.add(element)
                    if kind == "flag_pair" and len(mnem) == 2:
                        seen_as_flag_pair_element.add(mnem[1])
                    continue
                if mnem is None:
                    continue
                seen_anywhere.add(mnem)
                if kind != "arch_opcode":
                    continue
                if mnem not in wanted:
                    continue
                operand_holders = []
                for operand_name in row.get("operands") or []:
                    holder = row_info.get(operand_name)
                    if holder is None:
                        unresolved_operand_refs[mnem] += 1
                        holder = "unresolved|0"
                    operand_holders.append(holder)
                produced_holder = row_info[row["row"]]
                signature = (tuple(operand_holders), produced_holder)
                cell = table[mnem][signature]
                cell["occurrence_count"] += 1
                if len(cell["example_units"]) < 3 and \
                        unit_id not in cell["example_units"]:
                    cell["example_units"].append(unit_id)
                pair_key = (mnem, signature)
                if pair_key not in local_signatures_seen:
                    local_signatures_seen.add(pair_key)
                    cell["unit_count"] += 1
                    mnem_to_units[mnem].add(unit_id)
        del document
        check_collector_memory()
        if shard_count % 50 == 0 or shard_count == total_shards:
            say("   [%d/%d] shards read, %d units streamed"
                % (shard_count, total_shards, units_seen))

    return {
        "table": table,
        "mnem_to_units": mnem_to_units,
        "seen_anywhere": seen_anywhere,
        "seen_as_flag_pair_element": seen_as_flag_pair_element,
        "unresolved_operand_refs": unresolved_operand_refs,
        "shard_count": shard_count,
        "units_seen": units_seen,
    }


# ==================================================================
# section 2: the never-produces-a-row category (deliverable 1, last part)
# ==================================================================

def classify_never_produced(all_mnemonics, table, seen_anywhere,
                             seen_as_flag_pair_element):
    """a mnemonic with zero rows in `table` never produced its own
    arch_opcode ledger row anywhere in the corpus. Read further, by
    cause, off the same two sets rather than left as one flat list:
    a flag READER (seen only as the second element of a flag_pair,
    e.g. `sete`/`jne`) is one cause; a mnemonic never seen in any
    ledger row at all (a move folded away by canonicalization, or a
    pure control transfer -- the ledger only models the
    value-producing straight-line path, per log 223 section 4) is the
    other."""
    never = []
    for mnem in all_mnemonics:
        if mnem in table:
            continue
        if mnem in seen_as_flag_pair_element:
            cause = "flag reader (seen only as a flag_pair's reading element)"
        elif mnem in seen_anywhere:
            cause = "seen in a ledger row, never as its own arch_opcode producer"
        else:
            cause = "never seen in any ledger row (move or control transfer)"
        never.append({"mnem": mnem, "cause": cause})
    return never


# ==================================================================
# section 3: reading kind, collapse, sign-sensitive pairs -- reusing
# o9's own generic table functions (`OS.*`), never forked
# ==================================================================

def build_flags_only_producer(table):
    """a mnemonic is flag-producing here directly off this task's own
    class label: at least one attested signature's produced holder is
    class "flag" (a GUARD-block flag_pair setter's own value-producing
    row, e.g. `cmp`/`test`, read straight off the ledger's `type`
    field -- no DWARF boolean check needed, unlike o9's population,
    where the flag-setting mnemonic never survived to be a
    single-opcode row on its own)."""
    producers = set()
    for mnem, signatures in table.items():
        for signature in signatures:
            if OS.holder_class(signature[1]) == "flag":
                producers.add(mnem)
                break
    return producers


def classify_reading_kinds_o10(table, row_blind_evidence, width_changing,
                                reading_changing, flags_only_producer,
                                sign_sensitive_pairs):
    """o9's `OS.classify_reading_kinds` gates flag-producing on a
    DWARF boolean OUTPUT holder (`has_truth_output`), which never
    fires under this task's own holder rule (a produced TEMP/OUT row
    is never classed `DW_ATE_boolean` here -- see the module
    docstring). This task's own version drops that gate: flag-
    producing is exactly `mnem in flags_only_producer`, the direct
    signal `build_flags_only_producer` reads off the ledger's own
    `type` field. Every other kind is `OS`'s own check, unchanged."""
    sign_sensitive_of = collections.defaultdict(set)
    for pair in sign_sensitive_pairs:
        sign_sensitive_of[pair["mnemonic_a"]].add(pair["mnemonic_b"])
        sign_sensitive_of[pair["mnemonic_b"]].add(pair["mnemonic_a"])

    kinds = {}
    for mnem in table:
        found = []
        if mnem in flags_only_producer:
            found.append("flag-producing")
        if mnem in reading_changing:
            found.append("reading-changing")
        if mnem in width_changing:
            found.append("width-changing")
        if mnem in row_blind_evidence:
            found.append("reading-blind")
        if mnem in sign_sensitive_of:
            found.append("sign-sensitive")
        if not found:
            found.append("none of the read kinds")
        kinds[mnem] = found
    return kinds


def build_family_shim_rows(mnem_to_units):
    """the shape `OS.find_sign_sensitive_pairs` expects for its third
    argument (`valid_rows`): one pseudo-row per mnemonic, its
    `members` the units that ever produced it. `OS`'s own function
    reads only `row["mnem"]` and `member["unit"]` off this list --
    nothing else -- so this shim carries no meaning beyond satisfying
    that shape, and no field `OS` does not already read."""
    rows = []
    for mnem, units in mnem_to_units.items():
        rows.append({
            "mnem": mnem,
            "members": [{"unit": unit} for unit in sorted(units)],
        })
    return rows


# ==================================================================
# section 4: census command
# ==================================================================

def census_command():
    say("-- ledger_signatures.py census")
    unit_to_holders = OS.load_holder_lookup()
    say("   types101_entry_holders.json: %d units carry holders"
        % len(unit_to_holders))
    unit_to_family, family_conflicts = OS.load_family_lookup()
    say("   the_families5.json: %d units carry a family; %d conflicts"
        % (len(unit_to_family), len(family_conflicts)))

    all_mnemonics_doc = OS.read_json(UNIQUE_OPCODES_JSON)
    all_mnemonics = sorted(
        r["mnem"] for r in all_mnemonics_doc["cross_language_rows"])
    say("   unique_opcodes.json: %d mnemonics total" % len(all_mnemonics))

    pass_result = census_pass(unit_to_holders, all_mnemonics)
    table = pass_result["table"]
    say("   streamed %d shards, %d units; mnemonics with at least one "
        "signature: %d" % (pass_result["shard_count"],
                           pass_result["units_seen"], len(table)))
    if pass_result["unresolved_operand_refs"]:
        say("   WARNING unresolved operand refs: %s"
            % dict(pass_result["unresolved_operand_refs"]))

    never_produced = classify_never_produced(
        all_mnemonics, table, pass_result["seen_anywhere"],
        pass_result["seen_as_flag_pair_element"])
    say("   mnemonics with zero arch_opcode rows in the census: %d"
        % len(never_produced))

    flags_only_producer = build_flags_only_producer(table)
    row_blind_evidence = OS.find_reading_blind_evidence(table)
    width_changing = OS.find_width_changing(table)
    reading_changing = OS.find_reading_changing(table)
    family_shim_rows = build_family_shim_rows(pass_result["mnem_to_units"])
    sign_sensitive_pairs = OS.find_sign_sensitive_pairs(
        table, unit_to_family, family_shim_rows)
    say("   reading-blind: %d mnemonics; width-changing: %d; "
        "reading-changing: %d; flag-producing: %d; "
        "sign-sensitive pairs: %d"
        % (len(row_blind_evidence), len(width_changing),
           len(reading_changing), len(flags_only_producer),
           len(sign_sensitive_pairs)))

    kinds = classify_reading_kinds_o10(
        table, row_blind_evidence, width_changing, reading_changing,
        flags_only_producer, sign_sensitive_pairs)
    idea_count, merges = OS.collapse_count(table, sign_sensitive_pairs)
    say("   collapse: %d mnemonics with signature data -> %d ideas "
        "(%d sign-sensitive merges)" % (len(table), idea_count, merges))

    o9_pairs = [("imul", "mul"), ("sar", "shr"), ("add", "lea"),
                ("lea", "mov"), ("lea", "xor")]
    found_pair_set = set(
        frozenset([p["mnemonic_a"], p["mnemonic_b"]])
        for p in sign_sensitive_pairs)
    o9_reexamined = []
    for mnem_a, mnem_b in o9_pairs:
        confirmed = frozenset([mnem_a, mnem_b]) in found_pair_set
        o9_reexamined.append({
            "mnemonic_a": mnem_a,
            "mnemonic_b": mnem_b,
            "status": "confirmed" if confirmed else "suspect",
            "reason": ("still a signed/unsigned swap pair over the "
                       "fuller data" if confirmed else
                       "no signed/unsigned swap pair found over the "
                       "fuller data at any shared width"),
        })

    document = {
        "task": "o10 -- the opcode signature census from ledger rows",
        "population": {
            "source": "term66_run.shards() -- canon40_wrapped_*, "
                      "canon40_interp, canon40_regen_store",
            "shards": pass_result["shard_count"],
            "units_streamed": pass_result["units_seen"],
        },
        "signatures": {
            mnem: [
                {
                    "operand_holders": list(signature[0]),
                    "produced_holder": signature[1],
                    "occurrence_count": cell["occurrence_count"],
                    "unit_count": cell["unit_count"],
                    "example_units": cell["example_units"],
                }
                for signature, cell in table[mnem].items()
            ]
            for mnem in table
        },
        "never_produced": never_produced,
        "reading_kinds": {
            "row_scoped_reading_blind_evidence": {},
            "mnemonic_scoped_reading_blind_evidence": row_blind_evidence,
            "width_changing_evidence": width_changing,
            "reading_changing_evidence": reading_changing,
            "sign_sensitive_pairs": sign_sensitive_pairs,
            "flags_only_producer_mnemonics": sorted(flags_only_producer),
            "per_mnemonic_kinds": kinds,
        },
        "collapse": {
            "mnemonics_with_signature_data": len(table),
            "ideas_remaining": idea_count,
            "sign_sensitive_merges": merges,
        },
        "o9_pairings_reexamined": o9_reexamined,
        "unresolved_operand_refs": dict(pass_result["unresolved_operand_refs"]),
        "collector_peak_kb": peak_kb(),
    }
    OS.write_json(OUT_JSON, document)
    say("   wrote %s" % OUT_JSON)
    say("   collector peak %d kB" % peak_kb())
    return document


# ==================================================================
# section 5: report command
# ==================================================================

def signature_rows_for_md(table):
    rows = []
    for mnem in sorted(table):
        entries = sorted(table[mnem].items(),
                         key=lambda kv: -kv[1]["occurrence_count"])
        for signature, cell in entries:
            params_text = ", ".join(signature[0])
            sig_text = "%s -> %s" % (params_text, signature[1])
            rows.append([mnem, sig_text, cell["occurrence_count"],
                        cell["unit_count"]])
    return rows


def report_command():
    document = OS.read_json(OUT_JSON)
    lines = []
    lines.append("# ledger_signatures.md -- task o10, the opcode "
                 "signature census from ledger rows")
    lines.append("")
    lines.append("Generated by `ledger_signatures.py report` from "
                 "`ledger_signatures.json`. Counting only, no proofs.")
    lines.append("")

    lines.append("## 0. Population")
    lines.append("")
    population = document["population"]
    lines.append("%d shards, %d units streamed (`term66_run.shards()`)."
                 % (population["shards"], population["units_streamed"]))
    lines.append("")

    lines.append("## 1. Per mnemonic, the attested signatures")
    lines.append("")
    header = ["mnemonic", "signature (operand holders -> produced holder)",
              "occurrence count", "unit count"]
    table = {mnem: {tuple([tuple(s["operand_holders"]), s["produced_holder"]]):
                    {"occurrence_count": s["occurrence_count"],
                     "unit_count": s["unit_count"]}
                    for s in sigs}
             for mnem, sigs in document["signatures"].items()}
    rows = signature_rows_for_md(table)
    lines.append(OS.pipe_table(header, rows))
    lines.append("")

    lines.append("## 1b. Mnemonics with zero arch_opcode rows in the census")
    lines.append("")
    header = ["mnemonic", "cause"]
    rows = [[e["mnem"], e["cause"]]
            for e in document["never_produced"]]
    lines.append(OS.pipe_table(header, rows))
    lines.append("")

    lines.append("## 2. Reading kind per mnemonic (census-populated "
                 "mnemonics only)")
    lines.append("")
    per_mnemonic_kinds = document["reading_kinds"]["per_mnemonic_kinds"]
    header = ["mnemonic", "reading kind(s)"]
    rows = []
    for mnem in sorted(per_mnemonic_kinds):
        rows.append([mnem, ", ".join(per_mnemonic_kinds[mnem])])
    lines.append(OS.pipe_table(header, rows))
    lines.append("")
    lines.append("Sign-sensitive pairs (shared width signature, shared "
                 "family):")
    lines.append("")
    header = ["mnemonic_a", "mnemonic_b", "shared_width_signatures",
              "shared_families"]
    rows = []
    for pair in document["reading_kinds"]["sign_sensitive_pairs"]:
        rows.append([pair["mnemonic_a"], pair["mnemonic_b"],
                    pair["shared_width_signatures"],
                    pair["shared_families"]])
    lines.append(OS.pipe_table(header, rows))
    lines.append("")

    lines.append("## 3. Collapse count")
    lines.append("")
    collapse = document["collapse"]
    lines.append("%d mnemonics carry census signature data; %d "
                 "sign-sensitive merges; %d distinct arithmetic ideas "
                 "remain." % (collapse["mnemonics_with_signature_data"],
                              collapse["sign_sensitive_merges"],
                              collapse["ideas_remaining"]))
    lines.append("")

    lines.append("## 4. o9's lea-driven pairings, re-examined")
    lines.append("")
    header = ["mnemonic_a", "mnemonic_b", "status", "reason"]
    rows = [[e["mnemonic_a"], e["mnemonic_b"], e["status"], e["reason"]]
            for e in document["o9_pairings_reexamined"]]
    lines.append(OS.pipe_table(header, rows))
    lines.append("")

    handle = open(OUT_MD, "w")
    handle.write("\n".join(lines) + "\n")
    handle.close()
    say("wrote %s" % OUT_MD)


def main():
    if len(sys.argv) != 2:
        say(__doc__)
        return 1
    command = sys.argv[1]
    if command == "census":
        census_command()
        return 0
    if command == "report":
        report_command()
        return 0
    say(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
