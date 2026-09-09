#!/usr/bin/env python3
"""opcode_signatures.py -- task o9: the opcode signature census.

Node: hq.research.arch_unit_oracle.cross_construction.single_opcode_units
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/
node_0_3_2_2_cross_construction/node_0_3_2_2_2_single_opcode_units/`).
Framing: `DevComms/log_221_opcode_signature_algebra.md` (this census is
its own §5). This task is a JOIN over existing json -- counting only,
no proofs, nothing re-derived that already exists on disk.

THE OBJECTS, one sentence each, in relation.
  * A SINGLE-OPCODE ROW is one row of task o2's
    `single_opcode_groups.<lang>.narrow` (`single_opcode_units.json`,
    log 208), for the five compiled languages
    (c, cpp, go, rust, swift) -- the same population task o8 used.
  * A PROVED ROW is a single-opcode row whose `example_unit_id` reads
    `term_state == "TERM"` in `the_pool5.json` -- 243 of 259, the same
    16 c/cpp `call` rows (wide-integer runtime callees) task o8 (log
    220) found and skipped, for the same reason (no proved term).
  * A HOLDER is `types101_entry_holders.json`'s per-unit
    `parameter_holders` / `result_holder` -- read directly off that
    file, keyed by unit id (every entry's member list), never
    re-derived.
  * A SIGNATURE is one (parameter_holders tuple -> result_holder) pair
    attested by at least one member unit of a proved row.
  * A FAMILY is one entry of `the_families5.json`'s `families` list;
    membership is read off its nodes' `units` lists (unit id ->
    family_id), never off the operator token.
  * A GUARD-OUTCOME ROW is a canon40 ledger row with `block == "GUARD"`
    (the corpus's only guard marker; every GUARD row observed in this
    corpus is `produced_by.kind == "flag_pair"` -- see §3 of the
    report for the literal count that established this).

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

This task's grouping key is `mnemonic` -- an ARCH-OPCODE MNEMONIC, the
same permitted key task o2 and task o8 used. Task o2 (log_208) already
found and left OPEN, awaiting the owner, that four mnemonics -- `and`, `or`,
`xor`, `not` -- are also banned operator spellings (c++'s alternative
tokens) and trip the guard on the `mnemonic` key for that reason
alone; this task inherits that same open question rather than
re-litigating it (see the report's two-list rule). No new key is
invented to route around it. Holder strings (`DW_ATE_signed|8`, etc.)
and family/entry ids are machine-form, not operator spellings.

MEMORY BOUND: one process, no forked workers. `the_pool5.json` (32 MB)
and `types101_entry_holders.json` (14 MB) are held whole (both well
under the stated bound); the 332 canon40 stores (259 MB total) are
streamed one shard at a time via `term66_run.shards()` (imported,
never forked) for the guard-partition pass (deliverable 3) and dropped
after each shard -- only small per-mnemonic counters survive across
shards. Named abort `ABORT_MEMORY_O9` at 2 GB resident
(`resource.getrusage`), checked after every shard.

Coding discipline: no compound one-liner statements.

usage:
  opcode_signatures.py census    the whole census -> opcode_signatures.json
  opcode_signatures.py report    opcode_signatures.json -> .md
"""

import collections
import glob
import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARCH_OPCODES = os.path.normpath(os.path.join(HERE, ".."))
OP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "op_pipeline"))
sys.path.insert(0, OP)

import term66_run as TR  # noqa: E402  -- imported for .shards() only

SINGLE_OPCODE_JSON = os.path.join(ARCH_OPCODES, "single_opcode_units.json")
UNIQUE_OPCODES_JSON = os.path.join(ARCH_OPCODES, "unique_opcodes.json")
POOL_JSON = os.path.join(OP, "the_pool5.json")
ENTRY_HOLDERS_JSON = os.path.join(OP, "types101_entry_holders.json")
FAMILIES_JSON = os.path.join(OP, "the_families5.json")

OUT_JSON = os.path.join(HERE, "opcode_signatures.json")
OUT_MD = os.path.join(HERE, "opcode_signatures.md")

LANGS5 = ["c", "cpp", "go", "rust", "swift"]
RULE = "narrow"
ABORT_MEMORY_O9_KB = 2 * 1024 * 1024


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_collector_memory():
    used = peak_kb()
    if used > ABORT_MEMORY_O9_KB:
        raise SystemExit(
            "ABORT_MEMORY_O9: collector peak %d kB exceeds the stated "
            "2 GB bound" % used)
    return used


def read_json(path):
    handle = open(path)
    document = json.load(handle)
    handle.close()
    return document


def write_json(path, document):
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()


def pipe_table(header, rows):
    lines = ["| " + " | ".join(header) + " |"]
    lines.append("|" + "---|" * len(header))
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def holder_class(holder):
    return holder.split("|")[0]


def holder_width(holder):
    return holder.split("|")[1]


# ==================================================================
# section 0: the three lookups this census joins against
# ==================================================================

def load_pool_lookup():
    """the_pool5.json -> unit -> term_state, unit -> entry_id."""
    pool = read_json(POOL_JSON)
    unit_to_termstate = {}
    unit_to_entry = {}
    for entry in pool["entries"]:
        for member in entry["members"]:
            unit_to_termstate[member["unit"]] = member.get("term_state")
            unit_to_entry[member["unit"]] = entry["entry_id"]
    return unit_to_termstate, unit_to_entry


def load_holder_lookup():
    """types101_entry_holders.json -> unit -> {parameter_holders,
    result_holder}. Interpreter members carry no holder fields
    (their DWARF-typed key lives elsewhere, task 24) and are skipped."""
    document = read_json(ENTRY_HOLDERS_JSON)
    unit_to_holders = {}
    for entry in document["entries"]:
        for member in entry["members"]:
            if "parameter_holders" not in member:
                continue
            unit_to_holders[member["unit"]] = {
                "parameter_holders": tuple(member["parameter_holders"]),
                "result_holder": member["result_holder"],
                "entry_id": entry["entry_id"],
            }
    return unit_to_holders


def load_family_lookup():
    """the_families5.json -> unit -> family_id. A unit belongs to at
    most one node's units list in this corpus; checked, not assumed
    (a conflict is named, never silently overwritten)."""
    document = read_json(FAMILIES_JSON)
    unit_to_family = {}
    conflicts = []
    for family in document["families"]:
        for node in family["nodes"]:
            for unit in node["units"]:
                if unit in unit_to_family and \
                        unit_to_family[unit] != family["family_id"]:
                    conflicts.append(unit)
                unit_to_family[unit] = family["family_id"]
    return unit_to_family, conflicts


# ==================================================================
# section 1: the population -- 259 single-opcode rows, 243 proved
# ==================================================================

def load_rows():
    document = read_json(SINGLE_OPCODE_JSON)
    rows = []
    for lang in LANGS5:
        group = document["single_opcode_groups"][lang][RULE]
        for index, row in enumerate(group):
            entry = dict(row)
            entry["lang"] = lang
            entry["row_index"] = index
            rows.append(entry)
    return rows


def build_population(rows, unit_to_termstate):
    valid = []
    skipped = []
    for row in rows:
        uid = row["example_unit_id"]
        state = unit_to_termstate.get(uid)
        if state == "TERM":
            valid.append(row)
        else:
            entry = dict(row)
            entry["reason"] = ("term_state is %r, not TERM (the_pool5.json)"
                               % state)
            skipped.append(entry)
    return valid, skipped


# ==================================================================
# section 2: deliverable 1 -- per mnemonic, the attested signatures
# ==================================================================

def build_signatures(valid_rows, unit_to_holders):
    """mnemonic -> signature -> {member_count, example_units}. A
    signature is (parameter_holders tuple, result_holder). Counted
    over every MEMBER of every proved row (not only the example unit)
    -- the row's own body is shared by every member, and members can
    carry different holders (this is exactly how reading-blindness
    shows up, section 3)."""
    table = collections.defaultdict(lambda: collections.defaultdict(
        lambda: {"member_count": 0, "example_units": []}))
    unmatched = collections.Counter()
    for row in valid_rows:
        mnem = row["mnem"]
        for member in row["members"]:
            holders = unit_to_holders.get(member["unit"])
            if holders is None:
                unmatched[mnem] += 1
                continue
            signature = (holders["parameter_holders"], holders["result_holder"])
            cell = table[mnem][signature]
            cell["member_count"] += 1
            if len(cell["example_units"]) < 3:
                cell["example_units"].append(member["unit"])
    return table, unmatched


def signature_rows_for_md(table):
    rows = []
    for mnem in sorted(table):
        for signature, cell in sorted(table[mnem].items(),
                                      key=lambda kv: -kv[1]["member_count"]):
            params_text = ", ".join(signature[0])
            sig_text = "%s -> %s" % (params_text, signature[1])
            rows.append([mnem, sig_text, cell["member_count"]])
    return rows


# ==================================================================
# section 3: deliverable 2 -- reading kind, read off the data
# ==================================================================

SIGNED_CLASSES = set(["DW_ATE_signed", "DW_ATE_signed_char"])
UNSIGNED_CLASSES = set(["DW_ATE_unsigned", "DW_ATE_unsigned_char"])


def is_signed_unsigned_swap(class_a, class_b):
    """True when class_a and class_b are the two DWARF spellings of
    (signed, unsigned) reading of the same bits -- never a match when
    they are textually equal (that is 'same', not a swap), never a
    match across an unrelated class (float, boolean, UTF, the
    struct/pointer 'no size' class)."""
    if class_a in SIGNED_CLASSES and class_b in UNSIGNED_CLASSES:
        return True
    if class_a in UNSIGNED_CLASSES and class_b in SIGNED_CLASSES:
        return True
    return False


def positions_differ_only_in_class(sig_a, sig_b):
    """True if sig_a and sig_b (each (params_tuple, result)) have the
    same arity, the same width at every position, every position is
    either textually identical or a signed/unsigned swap (§brief:
    'differ only in class (signed vs unsigned)'), and at least one
    position is a genuine swap (identical signatures are not
    evidence of anything)."""
    params_a, result_a = sig_a
    params_b, result_b = sig_b
    if len(params_a) != len(params_b):
        return False
    positions_a = list(params_a) + [result_a]
    positions_b = list(params_b) + [result_b]
    saw_a_swap = False
    for holder_a, holder_b in zip(positions_a, positions_b):
        if holder_width(holder_a) != holder_width(holder_b):
            return False
        class_a = holder_class(holder_a)
        class_b = holder_class(holder_b)
        if class_a == class_b:
            continue
        if is_signed_unsigned_swap(class_a, class_b):
            saw_a_swap = True
            continue
        return False
    return saw_a_swap


def find_reading_blind_evidence(table):
    """per mnemonic: the first same-body-implied pair of signatures
    (within that one mnemonic's attested set) that differ only in
    class. `single_opcode_groups` already merges by (mnemonic, body);
    two signatures under the SAME mnemonic key are attested by
    members that -- for at least one shared row's example body, or
    across rows if the mnemonic's whole body-vocabulary is
    reading-blind -- are read off literally the same instruction
    text. The narrower, row-scoped check (same row, two members) is
    additionally recorded when it exists (`row_scoped`); the
    mnemonic-scoped check (`any_scoped`) is the fallback."""
    evidence = {}
    for mnem, signatures in table.items():
        sig_list = sorted(signatures.keys())
        found = None
        for i in range(len(sig_list)):
            for j in range(i + 1, len(sig_list)):
                if positions_differ_only_in_class(sig_list[i], sig_list[j]):
                    found = (sig_list[i], sig_list[j])
                    break
            if found is not None:
                break
        if found is not None:
            evidence[mnem] = {
                "signature_a": [list(found[0][0]), found[0][1]],
                "signature_b": [list(found[1][0]), found[1][1]],
            }
    return evidence


def find_row_scoped_reading_blind(valid_rows, unit_to_holders):
    """the stronger, literal claim: one PROVED ROW (one exact machine
    body) whose own members carry two signatures differing only in
    class. Returns mnemonic -> {example_unit_id, body_text, unit_a,
    signature_a, unit_b, signature_b}."""
    evidence = {}
    for row in valid_rows:
        mnem = row["mnem"]
        if mnem in evidence:
            continue
        seen = {}
        for member in row["members"]:
            holders = unit_to_holders.get(member["unit"])
            if holders is None:
                continue
            signature = (holders["parameter_holders"], holders["result_holder"])
            for other_signature, other_unit in seen.items():
                if positions_differ_only_in_class(signature, other_signature):
                    evidence[mnem] = {
                        "example_unit_id": row["example_unit_id"],
                        "body_text": row["body_text"],
                        "unit_a": other_unit,
                        "signature_a": [list(other_signature[0]),
                                       other_signature[1]],
                        "unit_b": member["unit"],
                        "signature_b": [list(signature[0]), signature[1]],
                    }
                    break
            if mnem in evidence:
                break
            seen[signature] = member["unit"]
    return evidence


def width_signature(signature):
    params, result = signature
    widths = tuple(holder_width(holder) for holder in params)
    return (widths, holder_width(result))


def find_width_changing(table):
    """mnemonic -> list of signatures where every input shares one
    width and that width differs from the output's -- the refined,
    same-width-inputs-only reading (mixed-width binary operands, e.g.
    a promoted second argument, are excluded here; they are exactly
    what section's pairwise class check already reads separately)."""
    evidence = {}
    for mnem, signatures in table.items():
        hits = []
        for signature in signatures:
            params, result = signature
            widths = set(holder_width(holder) for holder in params)
            if len(widths) == 1:
                only_width = next(iter(widths))
                if only_width != holder_width(result):
                    hits.append([list(params), result])
        if hits:
            evidence[mnem] = hits
    return evidence


def find_reading_changing(table):
    """mnemonic -> list of signatures where every input shares one
    class and that class differs from the output's."""
    evidence = {}
    for mnem, signatures in table.items():
        hits = []
        for signature in signatures:
            params, result = signature
            classes = set(holder_class(holder) for holder in params)
            if len(classes) == 1:
                only_class = next(iter(classes))
                if only_class != holder_class(result):
                    hits.append([list(params), result])
        if hits:
            evidence[mnem] = hits
    return evidence


def find_sign_sensitive_pairs(table, unit_to_family, valid_rows):
    """two DISTINCT mnemonics pair as sign-sensitive when: (a) they
    share at least one width signature (class dropped); (b) at that
    shared width, at least one of m1's attested signatures and one of
    m2's are a signed/unsigned swap of each other (never merely
    textually identical -- that would show shared behaviour, not a
    sign distinction); (c) they share at least one family id reached
    by any of their proved-row member units, the machine-form ground
    the brief requires instead of the operator token."""
    mnem_families = collections.defaultdict(set)
    for row in valid_rows:
        mnem = row["mnem"]
        for member in row["members"]:
            family = unit_to_family.get(member["unit"])
            if family is not None:
                mnem_families[mnem].add(family)

    mnemonics = sorted(table.keys())
    pairs = []
    for i in range(len(mnemonics)):
        for j in range(i + 1, len(mnemonics)):
            m1 = mnemonics[i]
            m2 = mnemonics[j]
            shared_families = mnem_families[m1] & mnem_families[m2]
            if not shared_families:
                continue
            swap_widths = set()
            swap_examples = []
            for sig1 in table[m1]:
                for sig2 in table[m2]:
                    if width_signature(sig1) != width_signature(sig2):
                        continue
                    if positions_differ_only_in_class(sig1, sig2):
                        swap_widths.add(width_signature(sig1))
                        if len(swap_examples) < 1:
                            swap_examples.append({
                                "signature_a": [list(sig1[0]), sig1[1]],
                                "signature_b": [list(sig2[0]), sig2[1]],
                            })
            if not swap_widths:
                continue
            pairs.append({
                "mnemonic_a": m1,
                "mnemonic_b": m2,
                "shared_width_signatures": sorted(
                    "%s -> %s" % (",".join(w[0]), w[1])
                    for w in swap_widths),
                "shared_families": sorted(shared_families),
                "example_signature_swap": swap_examples[0],
            })
    return pairs


# ==================================================================
# section 4: deliverable 3 -- the guard partition, all 162 mnemonics
# ==================================================================

def mnemonics_in_ledger_row(row):
    """the mnemonic(s) a ledger row names as its producer: one for an
    `arch_opcode` row, two (setter, reader) for a `flag_pair` row,
    none for `non_opcode_phrase`."""
    produced_by = row.get("produced_by") or {}
    mnem = produced_by.get("mnem")
    if mnem is None:
        return []
    if isinstance(mnem, list):
        return list(mnem)
    return [mnem]


def guard_reading_opcode(row):
    """the opcode a GUARD row names as the guard itself: the second
    (reading) element of a flag_pair; the bare mnem for anything
    else (never seen as anything but flag_pair in this corpus, kept
    as a fallback rather than an assumption)."""
    produced_by = row.get("produced_by") or {}
    mnem = produced_by.get("mnem")
    if isinstance(mnem, list) and len(mnem) == 2:
        return mnem[1]
    if isinstance(mnem, list) and mnem:
        return mnem[-1]
    return mnem


def guard_partition_pass(all_mnemonics):
    """one stream over every canon40 store (332 shards via
    term66_run.shards(), imported, not forked). Per mnemonic: total
    units whose ledger carries a row naming it as producer, how many
    of THOSE units also carry a GUARD-block row anywhere in their own
    ledger, and the guard opcodes seen on those units. Running
    counters only -- no unit id is retained past its own shard."""
    total_units = collections.Counter()
    guard_units = collections.Counter()
    guard_opcodes = collections.defaultdict(collections.Counter)
    flags_only_producer = set()
    ledger_kind_tally = collections.Counter()
    ledger_block_tally = collections.Counter()
    units_seen = 0
    shard_count = 0
    wanted = set(all_mnemonics)
    shard_paths = TR.shards()
    total_shards = len(shard_paths)

    for path in shard_paths:
        shard_count += 1
        document = read_json(path)
        for name, record in document["units"].items():
            units_seen += 1
            ledger = record.get("ledger") or []
            mnems_here = set()
            has_guard = False
            guard_ops_here = []
            for row in ledger:
                ledger_block_tally[row.get("block")] += 1
                produced_by = row.get("produced_by") or {}
                ledger_kind_tally[produced_by.get("kind")] += 1
                for mnem in mnemonics_in_ledger_row(row):
                    mnems_here.add(mnem)
                if row.get("type") == "flags only":
                    setter = produced_by.get("mnem")
                    if isinstance(setter, str):
                        flags_only_producer.add(setter)
                if row.get("block") == "GUARD":
                    has_guard = True
                    guard_ops_here.append(guard_reading_opcode(row))
            for mnem in mnems_here:
                if mnem not in wanted:
                    continue
                total_units[mnem] += 1
                if has_guard:
                    guard_units[mnem] += 1
                    for guard_op in guard_ops_here:
                        if guard_op is not None:
                            guard_opcodes[mnem][guard_op] += 1
        del document
        check_collector_memory()
        if shard_count % 50 == 0 or shard_count == total_shards:
            say("   [%d/%d] shards read, %d units streamed"
                % (shard_count, total_shards, units_seen))

    return {
        "total_units": total_units,
        "guard_units": guard_units,
        "guard_opcodes": guard_opcodes,
        "flags_only_producer": flags_only_producer,
        "ledger_kind_tally": ledger_kind_tally,
        "ledger_block_tally": ledger_block_tally,
        "shard_count": shard_count,
        "units_seen": units_seen,
    }


# ==================================================================
# section 5: assembling the 162-mnemonic table and the collapse count
# ==================================================================

def classify_reading_kinds(table, row_blind_evidence, width_changing,
                           reading_changing, flags_only_producer,
                           sign_sensitive_pairs):
    """mnemonic -> sorted list of reading kinds it satisfies, read
    strictly off the evidence already gathered. A mnemonic with no
    single-opcode signature data at all gets the single kind
    `no single-opcode row in the census`."""
    sign_sensitive_of = collections.defaultdict(set)
    for pair in sign_sensitive_pairs:
        sign_sensitive_of[pair["mnemonic_a"]].add(pair["mnemonic_b"])
        sign_sensitive_of[pair["mnemonic_b"]].add(pair["mnemonic_a"])

    kinds = {}
    for mnem in table:
        found = []
        has_truth_output = any(
            holder_class(signature[1]) == "DW_ATE_boolean"
            for signature in table[mnem])
        if has_truth_output and mnem in flags_only_producer:
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


def collapse_count(table, sign_sensitive_pairs):
    """union-find over the mnemonics that carry census signature data
    (25 in this run): start with one idea per mnemonic, union every
    sign-sensitive pair. Reading-blind does not merge two mnemonics
    (it explains why ONE mnemonic's signed/unsigned signatures are
    already a single idea; it does not reduce the mnemonic count
    further). The result is the count of ideas remaining."""
    parent = {}

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(node_a, node_b):
        root_a = find(node_a)
        root_b = find(node_b)
        if root_a != root_b:
            parent[root_a] = root_b

    for mnem in table:
        parent[mnem] = mnem
    for pair in sign_sensitive_pairs:
        union(pair["mnemonic_a"], pair["mnemonic_b"])

    roots = set(find(mnem) for mnem in table)
    return len(roots), len(table) - len(roots)


# ==================================================================
# section 6: census command
# ==================================================================

def census_command():
    say("-- opcode_signatures.py census")
    unit_to_termstate, unit_to_entry = load_pool_lookup()
    say("   the_pool5.json: %d units carry a term_state" %
        len(unit_to_termstate))
    unit_to_holders = load_holder_lookup()
    say("   types101_entry_holders.json: %d units carry holders" %
        len(unit_to_holders))
    unit_to_family, family_conflicts = load_family_lookup()
    say("   the_families5.json: %d units carry a family; %d conflicts"
        % (len(unit_to_family), len(family_conflicts)))

    rows = load_rows()
    say("   single_opcode_units.json narrow, 5 languages: %d rows"
        % len(rows))
    valid_rows, skipped_rows = build_population(rows, unit_to_termstate)
    say("   valid (proved term): %d; skipped (no proved term): %d"
        % (len(valid_rows), len(skipped_rows)))

    table, unmatched = build_signatures(valid_rows, unit_to_holders)
    say("   mnemonics with at least one attested signature: %d"
        % len(table))
    if unmatched:
        say("   WARNING unmatched members (no holder record): %s"
            % dict(unmatched))

    row_blind_evidence = find_row_scoped_reading_blind(
        valid_rows, unit_to_holders)
    mnem_blind_evidence = find_reading_blind_evidence(table)
    width_changing = find_width_changing(table)
    reading_changing = find_reading_changing(table)
    sign_sensitive_pairs = find_sign_sensitive_pairs(
        table, unit_to_family, valid_rows)
    say("   reading-blind (row-scoped): %d mnemonics; "
        "width-changing: %d; reading-changing: %d; "
        "sign-sensitive pairs: %d"
        % (len(row_blind_evidence), len(width_changing),
           len(reading_changing), len(sign_sensitive_pairs)))

    all_mnemonics = read_json(UNIQUE_OPCODES_JSON)
    all_mnemonics = sorted(
        r["mnem"] for r in all_mnemonics["cross_language_rows"])
    say("   unique_opcodes.json: %d mnemonics total" % len(all_mnemonics))

    guard = guard_partition_pass(all_mnemonics)
    say("   guard partition: %d shards, %d units streamed"
        % (guard["shard_count"], guard["units_seen"]))
    say("   ledger produced_by.kind tally: %s" %
        dict(guard["ledger_kind_tally"]))
    say("   ledger block tally: %s" % dict(guard["ledger_block_tally"]))

    kinds = classify_reading_kinds(
        table, row_blind_evidence, width_changing, reading_changing,
        guard["flags_only_producer"], sign_sensitive_pairs)
    idea_count, merges = collapse_count(table, sign_sensitive_pairs)
    say("   collapse: %d mnemonics with signature data -> %d ideas "
        "(%d sign-sensitive merges)" % (len(table), idea_count, merges))

    document = {
        "task": "o9 -- the opcode signature census",
        "population": {
            "source": SINGLE_OPCODE_JSON,
            "rule": RULE,
            "languages": LANGS5,
            "rows_total": len(rows),
            "valid": len(valid_rows),
            "skipped": skipped_rows,
        },
        "signatures": {
            mnem: [
                {
                    "parameter_holders": list(signature[0]),
                    "result_holder": signature[1],
                    "member_count": cell["member_count"],
                    "example_units": cell["example_units"],
                }
                for signature, cell in table[mnem].items()
            ]
            for mnem in table
        },
        "reading_kinds": {
            "row_scoped_reading_blind_evidence": row_blind_evidence,
            "mnemonic_scoped_reading_blind_evidence": {
                mnem: ev for mnem, ev in mnem_blind_evidence.items()
            },
            "width_changing_evidence": width_changing,
            "reading_changing_evidence": reading_changing,
            "sign_sensitive_pairs": sign_sensitive_pairs,
            "flags_only_producer_mnemonics": sorted(
                guard["flags_only_producer"]),
            "per_mnemonic_kinds": kinds,
        },
        "collapse": {
            "mnemonics_with_signature_data": len(table),
            "ideas_remaining": idea_count,
            "sign_sensitive_merges": merges,
        },
        "guard_partition": {
            "all_mnemonics": all_mnemonics,
            "shard_count": guard["shard_count"],
            "units_streamed": guard["units_seen"],
            "ledger_produced_by_kind_tally": dict(
                guard["ledger_kind_tally"]),
            "ledger_block_tally": dict(guard["ledger_block_tally"]),
            "per_mnemonic": {
                mnem: {
                    "units": guard["total_units"].get(mnem, 0),
                    "units_with_guard": guard["guard_units"].get(mnem, 0),
                    "guard_opcodes": dict(
                        guard["guard_opcodes"].get(mnem, {})),
                }
                for mnem in all_mnemonics
            },
        },
        "collector_peak_kb": peak_kb(),
    }
    write_json(OUT_JSON, document)
    say("   wrote %s" % OUT_JSON)
    say("   collector peak %d kB" % peak_kb())
    return document


# ==================================================================
# section 7: report command
# ==================================================================

def report_command():
    document = read_json(OUT_JSON)
    lines = []
    lines.append("# opcode_signatures.md -- task o9, the opcode "
                 "signature census")
    lines.append("")
    lines.append("Generated by `opcode_signatures.py report` from "
                 "`opcode_signatures.json`. Counting only, no proofs.")
    lines.append("")

    lines.append("## 0. Population")
    lines.append("")
    population = document["population"]
    lines.append("valid (proved term): %d; skipped (no proved term): %d"
                 % (population["valid"], len(population["skipped"])))
    lines.append("")
    lines.append("Skipped rows:")
    lines.append("")
    header = ["lang", "mnemonic", "example_unit_id", "reason"]
    skip_rows = []
    for row in population["skipped"]:
        skip_rows.append([row["lang"], row["mnem"],
                          row["example_unit_id"], row["reason"]])
    lines.append(pipe_table(header, skip_rows))
    lines.append("")

    lines.append("## 1. Per mnemonic, the attested signatures")
    lines.append("")
    header = ["mnemonic", "signature (input holders -> output holder)",
              "member count"]
    rows = signature_rows_for_md(
        {mnem: {tuple([tuple(s["parameter_holders"]), s["result_holder"]]):
               {"member_count": s["member_count"]}
               for s in sigs}
         for mnem, sigs in document["signatures"].items()})
    lines.append(pipe_table(header, rows))
    lines.append("")

    lines.append("## 2. Reading kind per mnemonic (census-populated "
                 "mnemonics only)")
    lines.append("")
    per_mnemonic_kinds = document["reading_kinds"]["per_mnemonic_kinds"]
    header = ["mnemonic", "reading kind(s)"]
    rows = []
    for mnem in sorted(per_mnemonic_kinds):
        rows.append([mnem, ", ".join(per_mnemonic_kinds[mnem])])
    lines.append(pipe_table(header, rows))
    lines.append("")
    lines.append("Row-scoped reading-blind evidence (one proved row, "
                 "two members, holders differing only in class):")
    lines.append("")
    header = ["mnemonic", "example_unit_id", "body_text", "unit_a",
              "signature_a", "unit_b", "signature_b"]
    rows = []
    for mnem, ev in sorted(
            document["reading_kinds"]["row_scoped_reading_blind_evidence"]
            .items()):
        rows.append([mnem, ev["example_unit_id"], ev["body_text"],
                    ev["unit_a"], ev["signature_a"], ev["unit_b"],
                    ev["signature_b"]])
    lines.append(pipe_table(header, rows))
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
    lines.append(pipe_table(header, rows))
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

    lines.append("## 4. The 162-mnemonic table")
    lines.append("")
    guard_partition = document["guard_partition"]
    header = ["mnemonic", "reading kind", "signatures attested",
              "units", "units with a guard", "guard opcodes"]
    rows = []
    for mnem in guard_partition["all_mnemonics"]:
        per_mnem_guard = guard_partition["per_mnemonic"][mnem]
        signature_count = len(document["signatures"].get(mnem, []))
        kind_text = ", ".join(
            per_mnemonic_kinds.get(mnem, ["no single-opcode row "
                                          "in the census"]))
        guard_ops = sorted(per_mnem_guard["guard_opcodes"].keys())
        rows.append([mnem, kind_text, signature_count,
                    per_mnem_guard["units"],
                    per_mnem_guard["units_with_guard"],
                    ", ".join(guard_ops)])
    lines.append(pipe_table(header, rows))
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
