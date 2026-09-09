#!/usr/bin/env python3
"""per_opcode.py -- task o8: for every single-arch-opcode unit (task
o2's NARROW rule), render ITS OWN proved term back to c with task o7's
renderer, compile at the corpus's ship flags, carve the body, and ask
Q0: does the chaff-stripped emulation body come back as exactly one
arch opcode, and is it the SAME mnemonic the unit was chosen for
(LANDED), one opcode but a DIFFERENT mnemonic (LANDED_ELSEWHERE,
named), or more than one opcode (NOT_COLLAPSED, counted)?  Alongside
Q0, task o7's own Q1 (byte identity, here against the ROW's own body
rather than the whole c corpus) and Q3 (the gate's proof against the
row's example unit) are asked exactly as o7 asks them.

Node: hq.research.arch_unit_oracle.cross_construction
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/CORE_0_3_2_2_cross_construction.md`,
FROZEN for term-level composition; this task, like o7, asks a
different question and does not unfreeze it).

the owner's question, verbatim (2026-09-06): "im curious if we could
auto-polyfill for each unique arch opcode at a high level. and im
curious is the compiler will optimally lower it to the correct arch
opcode."

THE OBJECTS, one sentence each, in relation.
  * A SINGLE-OPCODE UNIT is one row of task o2's
    `single_opcode_groups.<lang>.narrow` -- a group of arch-units
    whose chaff-stripped body is exactly one mnemonic, holding one
    `example_unit_id` and the group's own machine body bytes.
  * A PROVED TERM is that example unit's `layer5_normalized_text` from
    `Research/op_pipeline/term66_store`, read only where
    `outcome == "PROVED_ON_SHIP"`; a row whose unit carries no such
    term is listed and skipped, never emulated.
  * A POLYFILL is a c function whose body is that term written in c's
    own operators, produced by task o7's ONE renderer
    (`emulate.Renderer`, imported, never forked) from the z3 term; a
    term the renderer cannot render is refused by cause.
  * THE COLLAPSE TEST reuses o7's own steps by import: `emulate.
    compile_and_carve` (clang at the corpus's ship flags, carved by
    the pipeline's own objdump reader) and `emulate.prove_against_x`
    (the gate, 3,000 ms, `Q3`).  Q0 is NEW: the carved body's chaff
    stripped by task o2's own `single_opcode_units.strip_chaff(...,
    "narrow")` (imported, never forked), then its remaining mnemonic
    count and identity read off directly.  Q1 here is BYTE identity
    against the ROW's OWN body (not the whole c corpus, which is o7's
    question) -- both are `emulate.compile_and_carve`'s raw bytes,
    compared as strings.

WHAT IS REUSED RATHER THAN COPIED, said out loud.
  `emulate.Renderer`, `emulate.compile_and_carve`, `emulate.
  pipeline_extractor` (inside compile_and_carve), `emulate.
  families_the_term_reads`, `emulate.recorded_facts`, `emulate.
  prove_against_x`, `emulate.commutative_canonical`, `emulate.sanitize`,
  `emulate.read_json` / `write_json` / `say` / `peak_kb` / `check_
  collector_memory`, `emulate.pipe_table` -- all imported from
  `../emulate.py`, none forked.  `single_opcode_units.strip_chaff` /
  `parse_insn` / `is_label_line` -- imported from
  `Research/oracle/arch_opcodes/single_opcode_units.py`, none forked.
  `term97_walk.build`, `canonical_form.new_form` / `render_one`,
  `term66_run.one_unit` / `shards`, `pool100_entry_equivalence.*`,
  `gate.Gate`, `reference.answer_for_unit` -- the same op_pipeline
  modules o7 imports, used the same way.  Nothing under
  `Research/op_pipeline/` or `Research/oracle/arch_opcodes/` is
  edited; nothing under `emulate.py` is edited beyond what this
  docstring reads as already import-safe (its `main` sits behind
  `if __name__ == "__main__"`; no change was needed or made).

WHY NO FORKED WORKERS, unlike o7.  o7's population was 244
emulations, each needing a fresh process because the collector held
~450 canon40 records plus a corpus-wide byte index and ran up to 3
workers at once; a runaway z3 call under RLIMIT_AS was the risk being
bounded.  This task's population is at most 259 rows (task o2's own
counts: c 83, cpp 82, rust 48, go 27, swift 19), roughly the same
order of magnitude as o7's SAMPLE, not its full run, and each row's
own compile already carries a 180 s subprocess timeout
(`emulate.compile_and_carve`) and each gate call its own 3,000 ms
solver ceiling (`gate.Gate.decide`), so the per-row worst case is
already bounded without a fork.  What a fork buys beyond that -- an
outer kill on a runaway PYTHON loop rather than a bounded subprocess
call -- is accepted as a gap here and stated, not hidden: the lane's
own `script_timeout` (21,600 s, `o8.conf`) is the outer bound, and the
collecting process's own peak RSS is checked after every row against
a named abort (`ABORT_MEMORY_O8`, below).

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

This task's grouping key is `mnemonic` -- an ARCH-OPCODE MNEMONIC, the
same permitted key task o2's brief named ("Keys in this task are:
language, arch-opcode mnemonic, machine body bytes, unit id").  Task
o2 (log_208) already found and left OPEN, awaiting the owner, that four
mnemonics -- `and`, `or`, `xor`, `not` -- are also banned operator
spellings (c++'s alternative tokens) and trip the guard on the
`mnemonic` key for that reason alone; this task inherits that same
open question rather than re-litigating it (see the report's own
`decided` / `awaiting the owner` lists). No new key is invented to route
around it.

MEMORY BOUND, stated as the law requires: one collecting process, no
forked workers (see above), peak checked after every row, named abort
ABORT_MEMORY_O8 at 2 GB resident (half o7's 4 GB, o7's own margin
ratio against this task's tenth-scale population). The canon40 and
term66_store shards are streamed one at a time and dropped.

Coding discipline: no compound one-liner statements.

usage:
  per_opcode.py population     the population, held records, guard
  per_opcode.py run            every valid row's polyfill
  per_opcode.py report         per_opcode_results.json + .md
"""

import glob
import json
import os
import re
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EMU_DIR = os.path.normpath(os.path.join(HERE, ".."))
ARCH_OPCODES = os.path.normpath(os.path.join(HERE, "..", "..", "..", "arch_opcodes"))
OP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "op_pipeline"))
sys.path.insert(0, EMU_DIR)
sys.path.insert(0, ARCH_OPCODES)
sys.path.insert(0, OP)

import z3                                                        # noqa: E402
import emulate as E                                              # noqa: E402
import single_opcode_units as SOU                                # noqa: E402

SOURCE_JSON = os.path.join(ARCH_OPCODES, "single_opcode_units.json")
SRC_DIR = os.path.join(HERE, "src")
POPULATION = os.path.join(HERE, "per_opcode_population.json")
HELD = os.path.join(HERE, "per_opcode_held.json")
RESULTS = os.path.join(HERE, "per_opcode_results.json")
REPORT = os.path.join(HERE, "per_opcode_report.md")
HOST_FOLDER = ("PseudoCoupHQ/Research/oracle/cross_construction/"
              "emulation/per_opcode")

LANGS = ["c", "cpp", "go", "rust", "swift"]
RULE = "narrow"
ABORT_MEMORY_O8_KB = 2 * 1024 * 1024

say = E.say
peak_kb = E.peak_kb
write_json = E.write_json
read_json = E.read_json
pipe_table = E.pipe_table


def check_collector_memory():
    peak = peak_kb()
    if peak > ABORT_MEMORY_O8_KB:
        raise SystemExit("ABORT_MEMORY_O8: collector peak %d kB exceeds "
                         "the stated 2 GB bound" % peak)


# ==================================================================
# section 1: THE POPULATION   single_opcode_units.json -> jobs
# ==================================================================

def load_rows():
    """every row of `single_opcode_groups.<lang>.narrow`, for the five
    compiled languages the population object names."""
    doc = read_json(SOURCE_JSON)
    rows = []
    for lang in LANGS:
        group = doc["single_opcode_groups"][lang][RULE]
        for index, row in enumerate(group):
            rows.append({
                "lang": lang,
                "row_index": index,
                "mnem": row["mnem"],
                "row_body_text": row["body_text"],
                "example_unit_id": row["example_unit_id"],
                "member_count": row["member_count"],
            })
    return rows


def term66_shard_path(canon40_path):
    """the term66_store counterpart of one canon40 shard path: the
    same basename for a root wrapped/interp shard, prefixed
    `canon40_regen_store__` for a shard that sits under the
    `canon40_regen_store/` sub-folder -- read directly off the two
    directory listings (332 files, one-to-one, checked before this
    task wrote a line of code)."""
    base = os.path.basename(canon40_path)
    parent = os.path.basename(os.path.dirname(canon40_path))
    if parent == "canon40_regen_store":
        base = "canon40_regen_store__" + base
    return os.path.join(OP, "term66_store", base)


def build_held(needed_units):
    """stream every canon40 shard once, and its term66_store
    counterpart once, holding only the records this task needs: the
    canon40 record (ledger, body_bytes -- for transcribing the term
    and for Q1) and the term66 record (layer5_normalized_text,
    outcome -- the proved term itself)."""
    held = {}
    terms = {}
    shard_of = {}
    for path in E.canon40_shards():
        document = read_json(path)
        for name, record in document["units"].items():
            if name in needed_units:
                held[name] = record
                shard_of[name] = os.path.basename(path)
        del document
        term_path = term66_shard_path(path)
        if os.path.exists(term_path):
            term_document = read_json(term_path)
            for name, record in term_document["units"].items():
                if name in needed_units:
                    terms[name] = record
            del term_document
        check_collector_memory()
    return held, terms, shard_of


def population_command():
    say("-- POPULATION: single_opcode_units.json narrow rows, five languages")
    rows = load_rows()
    counts_by_lang = {}
    for row in rows:
        counts_by_lang[row["lang"]] = counts_by_lang.get(row["lang"], 0) + 1
    say("   rows per language: %s" % counts_by_lang)
    needed = set(row["example_unit_id"] for row in rows)
    say("   distinct example unit ids needed: %d" % len(needed))
    held, terms, shard_of = build_held(needed)
    say("   canon40 records held: %d; term66 records held: %d"
        % (len(held), len(terms)))
    valid = []
    no_proved_term = []
    for row in rows:
        uid = row["example_unit_id"]
        term_record = terms.get(uid)
        if term_record is None:
            entry = dict(row)
            entry["reason"] = "no term66_store record for this unit"
            no_proved_term.append(entry)
            continue
        if not term_record.get("proved") or \
                term_record.get("outcome") != "PROVED_ON_SHIP":
            entry = dict(row)
            entry["reason"] = ("term66_store outcome is %r, not "
                               "PROVED_ON_SHIP" % term_record.get("outcome"))
            no_proved_term.append(entry)
            continue
        text = term_record.get("layer5_normalized_text")
        if not text:
            entry = dict(row)
            entry["reason"] = "term66_store record carries no layer5 text"
            no_proved_term.append(entry)
            continue
        job = dict(row)
        job["term_text"] = text
        job["term_outcome"] = term_record.get("outcome")
        valid.append(job)
    say("   valid (proved term held): %d; no proved term, listed and "
        "skipped: %d" % (len(valid), len(no_proved_term)))
    write_json(POPULATION, {
        "task": "o8 -- for each single-arch-opcode unit, does clang "
                "land the polyfill on the SAME opcode",
        "source_json": SOURCE_JSON,
        "languages": LANGS,
        "rule": RULE,
        "rows_per_language": counts_by_lang,
        "rows_total": len(rows),
        "needed_units": sorted(needed),
        "valid": valid,
        "no_proved_term": no_proved_term,
        "ship_flags": " ".join([E.CLANG] + E.SHIP_FLAGS),
        "ship_flags_source": E.SHIP_FLAGS_SOURCE,
    })
    write_json(HELD, {"held": held, "shard_of": shard_of})
    say("   wrote %s, %s" % (POPULATION, HELD))
    say("   collector peak %d kB" % peak_kb())


# ==================================================================
# section 2: ONE POLYFILL   term -> c source -> compiled -> Q0/Q1/Q3
# ==================================================================

def build_shared():
    import term97_walk as TW
    import canonical_form as CF
    maker, gate, _attached, _readings = TW.build()
    form = CF.new_form()
    held_doc = read_json(HELD)
    return {
        "maker": maker,
        "gate": gate,
        "form": form,
        "reference": maker.reference,
        "held": held_doc["held"],
    }


def one_polyfill(shared, job):
    """one row's whole work: transcribe its own term, render, compile,
    carve, strip chaff (Q0), compare bytes against the row's own body
    (Q1), wrap+gate+term (kept for diagnosis), and prove against the
    row's own example unit (Q3)."""
    import term as T
    import term66_run as TR
    import canonical_form as CF
    import pool100_entry_equivalence as P100
    import gate as G
    maker = shared["maker"]
    gate = shared["gate"]
    form = shared["form"]
    reference = shared["reference"]
    held = shared["held"]
    uid = job["example_unit_id"]
    record = {
        "lang": job["lang"],
        "mnem": job["mnem"],
        "example_unit_id": uid,
        "row_body_text": job["row_body_text"],
        "member_count": job["member_count"],
        "term_text": job["term_text"],
    }
    x_record = held.get(uid)
    if x_record is None:
        record["rendered"] = False
        record["refusal_cause"] = E.CAUSE_NO_TERM
        record["refusal_detail"] = "no canon40 record held for %s" % uid
        return record
    record["row_body_bytes"] = x_record.get("body_bytes")
    record["x_arrival_families"] = list(x_record.get("arrival_families")
                                        or [])
    record["x_result_family"] = x_record.get("result_family")
    record["x_result_width"] = x_record.get("result_width")
    unit = dict(x_record)
    unit["unit"] = uid
    walked = maker.transcribe(unit)
    if walked.refused is not None or walked.out_term is None:
        record["rendered"] = False
        record["refusal_cause"] = E.CAUSE_NO_TERM
        if walked.refused is not None:
            record["refusal_detail"] = "the relink refused: %s" % \
                walked.refused
        else:
            import regate64_run as RG
            record["refusal_detail"] = RG.why_no_term(walked)
        return record
    x_term = walked.out_term
    reprinted = maker.normalize(x_term)
    record["reprinted_text"] = reprinted
    record["reprint_exact"] = reprinted == job["term_text"]
    if not record["reprint_exact"]:
        same = E.commutative_canonical(reprinted) == \
            E.commutative_canonical(job["term_text"])
        record["reprint_same_up_to_commutative_order_and_variable_index"] = \
            same
        if not same:
            record["rendered"] = False
            record["refusal_cause"] = E.CAUSE_REPRINT
            record["refusal_detail"] = reprinted
            return record
    ordered = T.order_commutative(z3.simplify(x_term))
    label = "%s_%d__%s" % (job["lang"], job["row_index"], E.sanitize(uid))
    families, omitted = E.families_the_term_reads(x_record, x_term)
    record["arrival_families"] = families
    record["contract_omits"] = omitted
    renderer = E.Renderer(families, x_record.get("result_family"),
                          x_record.get("result_width"), label)
    try:
        source, symbol = renderer.render(ordered, job["term_text"])
    except E.Refused as refusal:
        record["rendered"] = False
        record["refusal_cause"] = refusal.cause
        record["refusal_detail"] = refusal.detail
        return record
    record["rendered"] = True
    record["params"] = renderer.params
    record["source_path"] = os.path.join("src", label + ".c")
    record["source"] = source
    handle = open(os.path.join(SRC_DIR, label + ".c"), "w")
    handle.write(source)
    handle.close()
    got, refusal = E.compile_and_carve(source, symbol)
    if got is None:
        record["compiled"] = False
        record["compile_refusal"] = refusal
        return record
    record["compiled"] = True
    raw_bytes, mnem = got
    record["body_bytes"] = " ".join(raw_bytes)
    record["body_text"] = "; ".join(mnem)
    record["body_byte_count"] = len(raw_bytes)
    # Q0: chaff-stripped opcode collapse, task o2's own narrow rule
    stripped = SOU.strip_chaff(mnem, "narrow")
    record["stripped_remaining"] = list(stripped)
    record["stripped_count"] = len(stripped)
    if len(stripped) == 1:
        # THE FIELD NAME, renamed 2026-09-08 by task m1b: task mn1's
        # rename (log_235) moved this task's own `mnemonic` field to
        # `mnem`, the machine-form name the ruling of 2026-09-08 gives
        # it, and left `landed_mnemonic` -- the opcode a polyfill
        # actually compiled to -- behind as a compound field, which is
        # cause C of log_235's guard findings.
        landed_mnemonic, _operands = SOU.parse_insn(stripped[0])
        record["landed_mnem"] = landed_mnemonic
        if landed_mnemonic == job["mnem"]:
            record["q0"] = {"verdict": "LANDED"}
        else:
            record["q0"] = {"verdict": "LANDED_ELSEWHERE",
                            "landed_mnem": landed_mnemonic}
    else:
        record["q0"] = {"verdict": "NOT_COLLAPSED",
                        "opcode_count": len(stripped)}
    # Q1: byte identity against the ROW's OWN body (o7 asked this
    # against the whole c corpus; here the comparison scope is the one
    # body this row was drawn from)
    row_bytes = record["row_body_bytes"]
    identical = row_bytes is not None and record["body_bytes"] == row_bytes
    record["q1"] = {
        "verdict": "BYTE_IDENTICAL" if identical else "BYTES_DIFFER",
        "row_body_bytes": row_bytes,
    }
    # canonical form + term, the pipeline's own way (kept for
    # diagnosis; not one of the brief's three questions but needed by
    # Q3's own machinery below)
    emu_label = "c/" + label
    recorded = E.recorded_facts(emu_label, label, raw_bytes, mnem)
    record["c_arrival_families"] = recorded["arrival_families"]
    record["c_result_family"] = recorded["result_family"]
    record["c_result_width"] = recorded["result_width"]
    canon = CF.render_one(form, gate, recorded)
    canon["unit"] = emu_label
    record["canon40_outcome"] = canon.get("outcome")
    record["canon40_detail"] = canon.get("verdict_detail")
    term_record = TR.one_unit(maker, gate, emu_label, canon)
    record["term_state"] = term_record.get("term_state")
    record["term_outcome"] = term_record.get("outcome")
    record["layer5_text"] = term_record.get("layer5_normalized_text")
    # Q3: the gate over the two bodies, inputs aligned by IN row --
    # against the row's OWN example unit, reused unchanged from o7
    record["q3"] = E.prove_against_x(reference, gate, maker, canon,
                                     x_record, renderer.params, x_term,
                                     walked, P100, G, families)
    return record


def summary_word(record):
    if not record.get("rendered"):
        return "REFUSED(%s)" % record.get("refusal_cause")
    if not record.get("compiled"):
        return "NOT_COMPILED"
    return "compiled %d bytes" % record.get("body_byte_count", 0)


def run_command():
    say("-- RUN: every valid row's polyfill (sequential, see docstring "
        "for why no forked workers)")
    population = read_json(POPULATION)
    jobs = population["valid"]
    shared = build_shared()
    say("   shared objects built; collector peak %d kB" % peak_kb())
    total = len(jobs)
    results = []
    for index, job in enumerate(jobs, 1):
        try:
            record = one_polyfill(shared, job)
            record["word"] = "walked"
        except SystemExit:
            raise
        except BaseException as problem:                    # noqa: BLE001
            record = dict(job)
            record["word"] = "RAISED"
            record["raised"] = "%s: %s" % (type(problem).__name__, problem)
        results.append(record)
        say("[%d/%d] %s/%s %s -> %s  q0=%s q1=%s q3=%s"
            % (index, total, job["lang"], job["mnem"],
               job["example_unit_id"], summary_word(record),
               (record.get("q0") or {}).get("verdict", "-"),
               (record.get("q1") or {}).get("verdict", "-"),
               (record.get("q3") or {}).get("outcome", "-")))
        check_collector_memory()
    write_json(RESULTS, {"jobs_total": total, "results": results,
                         "collector_peak_kb": peak_kb()})
    say("   wrote %s" % RESULTS)
    say("   collector peak %d kB" % peak_kb())


# ==================================================================
# section 3: THE REPORT
# ==================================================================

def per_x_mnemonic_table(results):
    """the brief's deliverable 1 table: per source language x and per
    mnemonic, rows | rendered | compiled | LANDED | LANDED_ELSEWHERE |
    NOT_COLLAPSED | byte-identical | proved | disproved | undecided."""
    groups = {}
    order = []
    for record in results:
        key = (record["lang"], record["mnem"])
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(record)
    rows = []
    for key in order:
        lang, mnemonic = key
        members = groups[key]
        rendered = sum(1 for r in members if r.get("rendered"))
        compiled = sum(1 for r in members if r.get("compiled"))
        landed = sum(1 for r in members
                    if (r.get("q0") or {}).get("verdict") == "LANDED")
        elsewhere = sum(1 for r in members
                       if (r.get("q0") or {}).get("verdict") ==
                       "LANDED_ELSEWHERE")
        not_collapsed = sum(1 for r in members
                           if (r.get("q0") or {}).get("verdict") ==
                           "NOT_COLLAPSED")
        byte_identical = sum(1 for r in members
                            if (r.get("q1") or {}).get("verdict") ==
                            "BYTE_IDENTICAL")
        proved = sum(1 for r in members
                    if (r.get("q3") or {}).get("outcome") ==
                    "PROVED_ON_SHIP")
        disproved = sum(1 for r in members
                       if (r.get("q3") or {}).get("outcome") ==
                       "DISPROVED")
        undecided = sum(1 for r in members
                       if (r.get("q3") or {}).get("outcome") ==
                       "UNDECIDED")
        rows.append([lang, mnemonic, len(members), rendered, compiled,
                    landed, elsewhere, not_collapsed, byte_identical,
                    proved, disproved, undecided])
    return rows


def per_x_collapsed(rows):
    """the brief's "collapsed table per x (sums)": one row per
    language, summing the per-mnemonic table's numeric columns."""
    sums = {}
    order = []
    for row in rows:
        lang = row[0]
        if lang not in sums:
            sums[lang] = [0] * 10
            order.append(lang)
        for index in range(10):
            sums[lang][index] = sums[lang][index] + row[2 + index]
    out = []
    for lang in order:
        out.append([lang] + sums[lang])
    totals = [0] * 10
    for lang in order:
        for index in range(10):
            totals[index] = totals[index] + sums[lang][index]
    out.append(["all"] + totals)
    return out


def never_landed(results):
    """mnemonics that never got Q0 LANDED from ANY language's
    polyfill, across the whole run -- read off `mnemonic` and `q0`
    only, never off the operator token (there is none in this
    record)."""
    seen = {}
    for record in results:
        mnemonic = record["mnem"]
        landed = (record.get("q0") or {}).get("verdict") == "LANDED"
        seen.setdefault(mnemonic, False)
        if landed:
            seen[mnemonic] = True
    return sorted(name for name, was_landed in seen.items()
                 if not was_landed)


def zero_opcode_not_collapsed(results):
    """the NOT_COLLAPSED rows whose chaff-stripped body is EMPTY (0
    opcodes, not >1) -- named separately because the cause differs:
    the row's own body writes through a pointer (a store), which the
    term machinery's OUT-0 register answer does not carry, so the
    proved term is the pointer argument itself and the polyfill
    compiles to nothing but its own return."""
    out = []
    for record in results:
        q0 = record.get("q0") or {}
        if q0.get("verdict") == "NOT_COLLAPSED" and \
                q0.get("opcode_count") == 0:
            out.append(record)
    return out


def refusals_by_cause(results):
    causes = {}
    for record in results:
        if record.get("rendered"):
            continue
        cause = record.get("refusal_cause") or "(no cause recorded)"
        causes.setdefault(cause, []).append(record)
    return causes


def pick_examples(results):
    landed = None
    elsewhere = None
    not_collapsed = None
    for record in results:
        verdict = (record.get("q0") or {}).get("verdict")
        if verdict == "LANDED" and landed is None:
            landed = record
        if verdict == "LANDED_ELSEWHERE" and elsewhere is None:
            elsewhere = record
        if verdict == "NOT_COLLAPSED" and not_collapsed is None:
            not_collapsed = record
    return landed, elsewhere, not_collapsed


def report_command():
    say("-- REPORT: per_opcode_results.json + per_opcode_report.md")
    population = read_json(POPULATION)
    results_document = read_json(RESULTS)
    results = results_document["results"]
    mnemonic_rows = per_x_mnemonic_table(results)
    collapsed_rows = per_x_collapsed(mnemonic_rows)
    never = never_landed(results)
    causes = refusals_by_cause(results)
    zero_opcode = zero_opcode_not_collapsed(results)
    landed, elsewhere, not_collapsed = pick_examples(results)
    write_report_md(population, results_document, mnemonic_rows,
                    collapsed_rows, never, causes, landed, elsewhere,
                    not_collapsed, zero_opcode)
    say("   wrote %s" % REPORT)


def source_text(record):
    path = os.path.join(HERE, record.get("source_path", ""))
    if not os.path.exists(path):
        return "(source file not found: %s)" % path
    handle = open(path)
    text = handle.read()
    handle.close()
    return text


def write_report_md(population, results_document, mnemonic_rows,
                    collapsed_rows, never, causes, landed, elsewhere,
                    not_collapsed, zero_opcode):
    lines = []
    lines.append("# per_opcode_report.md -- task o8: does clang land a "
                 "polyfill on the SAME arch opcode it was drawn from")
    lines.append("")
    lines.append("Generated by `per_opcode.py report`. Every row's own "
                 "source is under `src/`.")
    lines.append("")
    lines.append("## 0. Population, at each filter")
    lines.append("")
    header = ["language", "rows (narrow)", "no proved term, skipped",
             "valid"]
    counts_rows = []
    no_term_by_lang = {}
    for entry in population["no_proved_term"]:
        no_term_by_lang[entry["lang"]] = no_term_by_lang.get(
            entry["lang"], 0) + 1
    valid_by_lang = {}
    for job in population["valid"]:
        valid_by_lang[job["lang"]] = valid_by_lang.get(job["lang"], 0) + 1
    for lang in population["languages"]:
        counts_rows.append([lang, population["rows_per_language"].get(
            lang, 0), no_term_by_lang.get(lang, 0),
            valid_by_lang.get(lang, 0)])
    counts_rows.append(["all", population["rows_total"],
                        len(population["no_proved_term"]),
                        len(population["valid"])])
    lines.append(pipe_table(header, counts_rows))
    lines.append("")
    lines.append("Ship flags: `%s` (%s)" % (population["ship_flags"],
                                            population["ship_flags_source"]))
    lines.append("")
    if population["no_proved_term"]:
        lines.append("Rows with no proved term, listed and skipped:")
        lines.append("")
        for entry in population["no_proved_term"]:
            lines.append("- `%s` (mnemonic `%s`): %s"
                         % (entry["example_unit_id"],
                            entry["mnem"], entry["reason"]))
        lines.append("")
    lines.append("## 1. Per x and per mnemonic: rows | rendered | "
                 "compiled | LANDED | LANDED_ELSEWHERE | NOT_COLLAPSED "
                 "| byte-identical to the row's own body | proved | "
                 "disproved | undecided")
    lines.append("")
    header = ["x", "mnemonic", "rows", "rendered", "compiled", "LANDED",
             "LANDED_ELSEWHERE", "NOT_COLLAPSED", "byte identical",
             "proved", "disproved", "undecided"]
    lines.append(pipe_table(header, mnemonic_rows))
    lines.append("")
    lines.append("## 2. Per x, collapsed (sums)")
    lines.append("")
    lines.append(pipe_table(header[:1] + header[2:], collapsed_rows))
    lines.append("")
    lines.append("## 3. Mnemonics never LANDED, from any language's "
                 "polyfill")
    lines.append("")
    if never:
        lines.append(", ".join("`%s`" % name for name in never))
    else:
        lines.append("(none -- every mnemonic in the population landed "
                     "from at least one language)")
    lines.append("")
    lines.append("## 3b. NOT_COLLAPSED rows whose stripped body is "
                 "EMPTY (0 opcodes, not >1)")
    lines.append("")
    if zero_opcode:
        lines.append("%d row(s). The row's own body writes through a "
                     "pointer (a store); the term machinery's OUT-0 "
                     "register answer does not carry a store, so the "
                     "proved term is the pointer argument itself and "
                     "the polyfill compiles to nothing but its own "
                     "return -- a limit of the method's scalar-answer "
                     "reading, not a collapse in either direction:"
                     % len(zero_opcode))
        lines.append("")
        for record in zero_opcode:
            lines.append("- `%s` (mnemonic `%s`): term `%s`, row "
                         "body `%s`, polyfill body `%s`"
                         % (record["example_unit_id"],
                            record["mnem"], record["term_text"],
                            record["row_body_text"], record["body_text"]))
    else:
        lines.append("(none in this run)")
    lines.append("")
    lines.append("## 3c. The disproved row (Q3), with its counterexample")
    lines.append("")
    disproved = [r for r in results_document["results"]
                if (r.get("q3") or {}).get("outcome") == "DISPROVED"]
    if disproved:
        for record in disproved:
            q3 = record["q3"]
            lines.append("`%s`, mnemonic `%s`. The term, LITERAL: "
                         "`%s`" % (record["example_unit_id"],
                                   record["mnem"],
                                   record["term_text"]))
            lines.append("")
            lines.append(pipe_table(
                ["side", "body"],
                [["the row's own body", "`%s`" % record["row_body_text"]],
                 ["the polyfill", "`%s`" % record["body_text"]]]))
            lines.append("")
            lines.append("Counterexample seeds, LITERAL: `%s`"
                         % q3.get("counterexample"))
            rescue = q3.get("under_caller_extension")
            if rescue is not None:
                lines.append("")
                lines.append("Under the caller-extension re-posing "
                             "(every narrow-holder input row zero-"
                             "extended from its holder width, c's own "
                             "caller-extension rule), LITERAL: `%s`"
                             % rescue.get("outcome"))
    else:
        lines.append("(none in this run)")
    lines.append("")
    lines.append("## 4. Three literal examples")
    lines.append("")
    lines.append("### 4.1 LANDED")
    lines.append("")
    if landed is not None:
        lines.append("`%s`, mnemonic `%s`. The term, LITERAL: `%s`"
                     % (landed["example_unit_id"],
                        landed["mnem"], landed["term_text"]))
        lines.append("")
        lines.append("The rendered source, LITERAL:")
        lines.append("")
        lines.append("```c")
        lines.append(source_text(landed).rstrip("\n"))
        lines.append("```")
        lines.append("")
        lines.append(pipe_table(["side", "body"],
                                [["the row's own body",
                                  "`%s`" % landed["row_body_text"]],
                                 ["the polyfill",
                                  "`%s`" % landed["body_text"]]]))
    else:
        lines.append("(none in this run)")
    lines.append("")
    lines.append("### 4.2 LANDED_ELSEWHERE")
    lines.append("")
    if elsewhere is not None:
        lines.append("`%s`, drawn for mnemonic `%s`, landed on `%s`. "
                     "The term, LITERAL: `%s`"
                     % (elsewhere["example_unit_id"],
                        elsewhere["mnem"],
                        elsewhere["q0"]["landed_mnem"],
                        elsewhere["term_text"]))
        lines.append("")
        lines.append(pipe_table(["side", "body"],
                                [["the row's own body (`%s`)"
                                  % elsewhere["mnem"],
                                  "`%s`" % elsewhere["row_body_text"]],
                                 ["the polyfill (`%s`)"
                                  % elsewhere["q0"]["landed_mnem"],
                                  "`%s`" % elsewhere["body_text"]]]))
        lines.append("")
        lines.append("**GLOSS.** Both bodies answer the row's own term; "
                     "clang chose the instruction on the right for that "
                     "term's shape, not the one the row's own body used "
                     "-- read from the two bodies above, not asserted.")
    else:
        lines.append("(none in this run)")
    lines.append("")
    lines.append("### 4.3 NOT_COLLAPSED")
    lines.append("")
    if not_collapsed is not None:
        lines.append("`%s`, mnemonic `%s`, %d opcodes remaining after "
                     "the narrow chaff strip. The term, LITERAL: `%s`"
                     % (not_collapsed["example_unit_id"],
                        not_collapsed["mnem"],
                        not_collapsed["q0"]["opcode_count"],
                        not_collapsed["term_text"]))
        lines.append("")
        lines.append("The polyfill's carved body, LITERAL: `%s`"
                     % not_collapsed["body_text"])
        lines.append("")
        lines.append("Remaining after the narrow chaff strip, LITERAL: "
                     "`%s`" % "; ".join(not_collapsed["stripped_remaining"]))
    else:
        lines.append("(none in this run)")
    lines.append("")
    lines.append("## 5. Renderer refusals, by cause")
    lines.append("")
    if causes:
        for cause in sorted(causes):
            members = causes[cause]
            names = [r["example_unit_id"] for r in members[:5]]
            lines.append("- `%s`: %d (%s%s)"
                         % (cause, len(members), ", ".join(names),
                            ", ..." if len(members) > 5 else ""))
    else:
        lines.append("(none -- every valid row's term rendered)")
    lines.append("")
    lines.append("## 6. Bounds")
    lines.append("")
    lines.append("- The stated bound: one collecting process, sequential "
                 "(no forked workers -- see `per_opcode.py`'s own "
                 "docstring), peak resident size checked after every "
                 "row, named abort `ABORT_MEMORY_O8` at %d kB (2 GB). It "
                 "was never raised." % ABORT_MEMORY_O8_KB)
    lines.append("- Peak resident size of the collecting process, "
                 "`resource.getrusage(RUSAGE_SELF).ru_maxrss`: %d kB."
                 % results_document.get("collector_peak_kb", 0))
    lines.append("")
    handle = open(REPORT, "w")
    handle.write("\n".join(lines))
    handle.close()


def main(argv):
    if not argv:
        say(__doc__)
        return 2
    word = argv[0]
    if not os.path.isdir(SRC_DIR):
        os.makedirs(SRC_DIR)
    if word == "population":
        population_command()
        return 0
    if word == "run":
        run_command()
        return 0
    if word == "report":
        report_command()
        return 0
    say(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
