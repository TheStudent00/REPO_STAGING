#!/usr/bin/env python3
"""t94_recarve.py -- TASK 94, round 18, steps 2-4: the eleven interpreter
units RE-CARVED to their handler function's body, put through the
universal canonical form (region36's virtual memory), and gated against
each unit's OWN ship code.

THE RULING THIS IMPLEMENTS (the owner, 2026-09-05, recorded under the heading
"the unit's boundary -- RULED by the owner 2026-09-05" in
CORE_0_3_5_1_arch_unit.md): "everything is wrapped in a function.  it
should be just after the wrapper-function call to just before the
return statement."  A unit is a FUNCTION BODY.  For an interpreter
there is no wrapper of ours, so the interpreter's OWN handler function
is the wrapper and the unit is that function's body, with bounds READ
from the symbol table and DWARF (t94_read_bounds.py), never computed by
taint propagation.

AND, ruled in the same breath, what carries the cost: "canonical form
should reduce unnecessary clutter with the reference to a virtual memory
system, and the super-op miner should be able to fill in the missing
stuff for z3."  So the form used here is region36's -- the ruled virtual
region, its six allocation kinds and its block allocator -- rendered by
canon36_universal.render, both imported UNMODIFIED.  No new memory model
is invented; where the existing one does not reach, this file says so by
name and stops.

A VERDICT THAT MOVES FROM PROVED TO UNDECIDED IS A CORRECT RESULT HERE,
not a regression: the old proof rested on a boundary someone chose.  No
body is narrowed to keep a proof.

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

MEMORY BOUND, stated: this program holds eleven function bodies (the
largest is 190 instructions) and one z3 solver at a time.  Expected peak
resident size is well under 1 GB; the abort name if it climbs past 6 GB
is `T94_RECARVE_MEMORY_ABORT`, and the run prints its own peak.

SOLVER TIME.  Each gate is asked twice where the first answer is
UNDECIDED FOR TIME: once at 20,000 ms (canon36_universal.compare's own
figure) and once at 120,000 ms, which is task 91's measured longer run.
Both answers are recorded, and whether the answer changed is stated.
"""

import json
import os
import re
import resource
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                   # noqa: E402
import canon2                                                  # noqa: E402
import region36 as R36                                         # noqa: E402
import canon36_universal as CU                                 # noqa: E402
import block_cutter                                            # noqa: E402
import z3                                                      # noqa: E402

OUT = os.path.join(HERE, "t94_recarve.json")
MEMORY_ABORT_KB = 6 * 1024 * 1024
LONG_TIMEOUT_MS = 120000


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def memory_guard(where):
    now = peak_kb()
    if now > MEMORY_ABORT_KB:
        raise SystemExit("T94_RECARVE_MEMORY_ABORT at %s: peak resident "
                         "%d kB is past the stated 6 GB bound"
                         % (where, now))
    return now


def load(name):
    with open(os.path.join(HERE, name)) as handle:
        return json.load(handle)


# ------------------------------------------------------------------
# per-unit arrival contract, DECLARED with its evidence class.
# `label` is the display label, once, on the member.  Nothing in
# this file keys, groups, pairs or selects on it.
# ------------------------------------------------------------------

ARRIVAL = {
    "cpython/long_add_fastpath": {
        "a": "rdi", "b": "rsi", "result": "rax", "result_width": 64,
        "evidence": "read off the body: `mov 0x10(%rdi),%rax` and "
                    "`mov 0x10(%rsi),%rdx` are the first touches of "
                    "either family and are both reads, which is the "
                    "arrival-contract rule (log_146 5.4); the SysV "
                    "convention agrees.",
    },
    "ruby/rb_fix_plus": {
        "a": "rdi", "b": "rsi", "result": "rax", "result_width": 64,
        "evidence": "read off the body, cross-read against DWARF: the "
                    "symbol's DW_TAG_subprogram carries two formal "
                    "parameters of one type.",
    },
    "ruby/rb_int_plus": {
        "a": "rdi", "b": "rsi", "result": "rax", "result_width": 64,
        "evidence": "read off the body, cross-read against DWARF.",
    },
    "ruby/rb_big_plus": {
        "a": "rdi", "b": "rsi", "result": "rax", "result_width": 64,
        "evidence": "read off the body, cross-read against DWARF.",
    },
    "php/add_function": {
        "a": "rsi", "b": "rdx", "result": "rax", "result_width": 32,
        "evidence": "DWARF: add_function(zval *result, zval *op1, "
                    "zval *op2) -- dwarf_typed_key_t27.json.  The FIRST "
                    "parameter is where the answer is written, so the "
                    "two operand lineages arrive in %rsi and %rdx.  "
                    "lineage_carve.py recorded the same policy.",
    },
    "php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER": {
        "a": None, "b": None, "result": "rax", "result_width": 64,
        "evidence": "DWARF records ZERO formal parameters "
                    "(dwarf_typed_key_t27.json).  The operands are read "
                    "out of the VM frame through %r15 and %r14.",
    },
    "php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER": {
        "a": None, "b": None, "result": "rax", "result_width": 64,
        "evidence": "DWARF records ZERO formal parameters.",
    },
    "php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER": {
        "a": None, "b": None, "result": "rax", "result_width": 64,
        "evidence": "DWARF records ZERO formal parameters.",
    },
    "java/op_1": {
        "a": "rsi", "b": "rdx", "result": "rax", "result_width": 32,
        "evidence": "the JVM's own printed parameter comments on this "
                    "nmethod, quoted verbatim from interp_jvm.json: "
                    "'# parm0:    rsi       = int' and "
                    "'# parm1:    rdx       = int'.",
    },
    "java/op_2": {
        "a": "rsi", "b": "rdx", "result": "rax", "result_width": 32,
        "evidence": "the JVM's own printed parameter comments, as above.",
    },
    "ruby/vm_opt_plus": {
        "a": "rdi", "b": "rsi", "result": "rax", "result_width": 64,
        "evidence": "not reached: this symbol has no ship body.",
    },
}


# the OLD boundary of every unit, quoted from the artifact that holds
# it rather than from notes.
OLD = {
    "cpython/long_add_fastpath": {
        "artifact": "interp_fastpath.json + canon_interp_units_cpython.json",
        "old_low": "0x1373d8",
        "old_high": "(reachability closure, not a contiguous range)",
        "old_region_instruction_count": 48,
        "old_body_instruction_count": 1,
        "old_body_verbatim": ["lea (%rax,%rdx,1),%rdi"],
        "old_canonical_text": "mov %rdi,%rax; mov %rsi,%r10; "
                              "add %r10,%rax; ret",
        "old_verdict": "PROVED",
        "old_boundary_rule": "lineage confluence, computed by taint "
                             "propagation from an entry the fast-path "
                             "branch chose",
    },
    "java/op_1": {
        "artifact": "canon_interp_units_java.json + interp_jvm.json",
        "old_low": "0x7f99346aa41a",
        "old_high": "0x7f99346aa41d",
        "old_region_instruction_count": 27,
        "old_body_instruction_count": 1,
        "old_body_verbatim": ["lea (%rdi,%rsi,1),%eax"],
        "old_canonical_text": "mov %rdi,%rax; and $-1,%eax; "
                              "mov %rsi,%r10; and $-1,%r10d; "
                              "add %r10d,%eax; ret",
        "old_verdict": "PROVED",
        "old_boundary_rule": "jvm_canon.strip()'s residual core -- the "
                             "nmethod stripped of prologue, entry "
                             "barrier, safepoint poll and stubs",
    },
    "java/op_2": {
        "artifact": "interp_canon34.json",
        "old_low": "0x7f99346a9b33",
        "old_high": "0x7f99346a9b36",
        "old_region_instruction_count": 43,
        "old_body_instruction_count": 1,
        "old_body_verbatim": ["idiv %r11d"],
        "old_canonical_text": "mov %edi,%eax; cltd; idiv %esi; ret",
        "old_verdict": "PROVED",
        "old_boundary_rule": "lineage confluence, computed by taint "
                             "propagation",
    },
    "ruby/vm_opt_plus": {
        "artifact": "interp_canon35.json units_with_no_universal_text",
        "old_low": None,
        "old_high": None,
        "old_region_instruction_count": 0,
        "old_body_instruction_count": 0,
        "old_body_verbatim": [],
        "old_canonical_text": None,
        "old_verdict": "NO_CANONICAL_TEXT",
        "old_boundary_rule": "no ship body exists for this symbol",
    },
    "ruby/rb_fix_plus": {
        "artifact": "interp_canon34.json",
        "old_low": "0x104834",
        "old_high": "0x104837",
        "old_region_instruction_count": 126,
        "old_body_instruction_count": 1,
        "old_body_verbatim": ["add %rdi,%rax"],
        "old_canonical_text": "mov %rsi,%rax; add %rdi,%rax; ret",
        "old_verdict": "PROVED",
        "old_boundary_rule": "lineage confluence, computed by taint "
                             "propagation",
    },
    "ruby/rb_int_plus": {
        "artifact": "interp_canon34.json",
        "old_low": "0xfac1f",
        "old_high": "0xfac22",
        "old_region_instruction_count": 190,
        "old_body_instruction_count": 1,
        "old_body_verbatim": ["add %rbx,%rax"],
        "old_canonical_text": "mov %rdi,%rax; add %rsi,%rax; ret",
        "old_verdict": "PROVED",
        "old_boundary_rule": "lineage confluence, computed by taint "
                             "propagation",
    },
    "ruby/rb_big_plus": {
        "artifact": "interp_canon35.json units_with_no_universal_text",
        "old_low": None,
        "old_high": None,
        "old_region_instruction_count": 132,
        "old_body_instruction_count": 0,
        "old_body_verbatim": [],
        "old_canonical_text": None,
        "old_verdict": "NO_CANONICAL_TEXT",
        "old_boundary_rule": "the taint propagation refused: the "
                             "lineages leave through a call",
    },
    "php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER": {
        "artifact": "interp_canon34.json",
        "old_low": "0x228ca1",
        "old_high": "0x228ca4",
        "old_region_instruction_count": 48,
        "old_body_instruction_count": 1,
        "old_body_verbatim": ["add (%rsi),%rax"],
        "old_canonical_text": "mov %rdi,%rax; mov -0x8(%rsp),%r11; "
                              "add %r11,%rax; ret",
        "old_verdict": "PROVED",
        "old_boundary_rule": "lineage confluence, computed by taint "
                             "propagation from frame-slot seeds",
    },
    "php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER": {
        "artifact": "interp_canon34.json",
        "old_low": "0x2257fc",
        "old_high": "0x2257ff",
        "old_region_instruction_count": 20,
        "old_body_instruction_count": 1,
        "old_body_verbatim": ["add (%rcx),%rax"],
        "old_canonical_text": "mov %rdi,%rax; mov -0x8(%rsp),%r11; "
                              "add %r11,%rax; ret",
        "old_verdict": "PROVED",
        "old_boundary_rule": "lineage confluence, computed by taint "
                             "propagation from frame-slot seeds",
    },
    "php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER": {
        "artifact": "interp_canon34.json",
        "old_low": "0x2257ce",
        "old_high": "0x2257d3",
        "old_region_instruction_count": 10,
        "old_body_instruction_count": 1,
        "old_body_verbatim": ["add (%r14,%rcx,1),%rax"],
        "old_canonical_text": "mov %rsi,%rax; mov -0x8(%rsp),%r11; "
                              "add %r11,%rax; ret",
        "old_verdict": "PROVED",
        "old_boundary_rule": "lineage confluence, computed by taint "
                             "propagation from frame-slot seeds",
    },
    "php/add_function": {
        "artifact": "interp_canon35.json (the arrival-aware re-carve)",
        "old_low": "0x40c065",
        "old_high": "0x40c068",
        "old_region_instruction_count": 55,
        "old_body_instruction_count": 2,
        "old_body_verbatim": ["mov (%rsi),%rax", "add (%rdx),%rax"],
        "old_canonical_text": "mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; "
                              "mov %rdi,%rax; add %rsi,%rax; ret",
        "old_verdict": "PROVED",
        "old_boundary_rule": "arrival-aware lineage confluence, computed "
                             "by taint propagation",
    },
}


# ------------------------------------------------------------------
# the body, as text
# ------------------------------------------------------------------

TARGET = re.compile(r"\b([0-9a-f]{4,16})\s*<([^>]*)>")


def body_lines(record):
    """the handler function's own instructions, objdump's text, with the
    `<symbol+0xNN>` annotation kept -- canon2's cutter reads it."""
    return [row["mnem"] for row in record["body"]]


def body_addresses(record):
    return [int(row["address"], 16) for row in record["body"]]


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


def block_form_text(lines, addrs):
    """the whole body as a BLOCK LIST -- labels L0, L1, ... in ADDRESS
    order, which is canon2_branching's own convention (canon2.py line
    1085), and every in-body transfer rewritten onto its label.  A
    transfer whose target is OUTSIDE these bounds is left exactly as
    the compiler wrote it and is counted as an exit."""
    low = addrs[0]
    index_of_address = {}
    for index, address in enumerate(addrs):
        index_of_address[address] = index
    leaders = set([0])
    target_of_index = {}
    for index, line in enumerate(lines):
        mnemonic, _operands = canon.parse(canon2.strip_reloc(line))
        if canon.JUMP.match(mnemonic):
            address = target_address(line, low)
            landing = index_of_address.get(address)
            if landing is not None:
                leaders.add(landing)
                target_of_index[index] = landing
            if mnemonic != "jmp" and index + 1 < len(lines):
                leaders.add(index + 1)
            continue
        if mnemonic in ("ret", "retq", "ud2", "call", "callq"):
            if index + 1 < len(lines):
                leaders.add(index + 1)
    label_of_index = {}
    for order, index in enumerate(sorted(leaders)):
        label_of_index[index] = "L%d" % order
    start_of_index = {}
    current = None
    for index in range(len(lines)):
        if index in label_of_index:
            current = index
        start_of_index[index] = current
    out = []
    exits = []
    for index, line in enumerate(lines):
        if index in label_of_index:
            out.append("%s:" % label_of_index[index])
        text = line
        mnemonic, _operands = canon.parse(canon2.strip_reloc(line))
        if canon.JUMP.match(mnemonic):
            landing = target_of_index.get(index)
            if landing is not None:
                text = "%s %s" % (mnemonic,
                                  label_of_index[start_of_index[landing]])
            else:
                exits.append({"at_index": index, "instruction": line})
        if mnemonic in ("call", "callq"):
            exits.append({"at_index": index, "instruction": line})
        out.append(text)
    return out, exits, len(label_of_index)


REFCOUNT = re.compile(r"lock\s+(add|sub|inc|dec)|"
                      r"(add|sub|inc|dec)[a-z]*\s+\$0x1,0x0\(")
MEMORY_DESTINATION = re.compile(r"\([^)]*%[a-z0-9]+[^)]*\)\s*$")


def machinery_of(lines):
    """RECURRING PATHS in this body, found by looking at the body: a
    transfer into the runtime (allocation, warning, coercion), a
    read-modify-write of a word at a fixed displacement from an
    arriving pointer (the shape a reference count has), and a store
    into memory the unit did not arrive with."""
    calls = []
    memory_writes = []
    for index, line in enumerate(lines):
        mnem, operands = canon.parse(canon2.strip_reloc(line))
        if mnem in ("call", "callq"):
            hit = re.search(r"<([^>]+)>", line)
            calls.append({"at_index": index, "instruction": line,
                          "callee": hit.group(1) if hit else None})
            continue
        if not operands:
            continue
        destination = operands[-1]
        if MEMORY_DESTINATION.search(destination):
            memory_writes.append({"at_index": index, "instruction": line,
                                  "destination": destination})
    return {"transfers_into_the_runtime": calls,
            "memory_writes": memory_writes}


# ------------------------------------------------------------------
# the gate: the region text against the unit's OWN ship body
# ------------------------------------------------------------------

def gate_against_own_ship(reference_lines, region_lines, families,
                          directory, home, width, timeout_ms):
    seed = {}
    bindings = CU.bind_region(seed, directory, families)
    sim_ref = CU.Sim36(seed, "reference")
    sim_reg = CU.Sim36(seed, "region")
    sim_ref.answer_family = home
    sim_ref.answer_width = width
    sim_reg.answer_family = home
    sim_reg.answer_width = width
    try:
        val_ref, w_ref = sim_ref.answer_value(reference_lines)
    except Exception as bad:                                  # noqa: BLE001
        return ("UNDECIDED",
                "the unit's own ship body: %s: %s"
                % (type(bad).__name__, bad), bindings, False)
    try:
        sim_reg.run_lines(region_lines)
        val_reg, w_reg = sim_reg.result_block_value()
    except Exception as bad:                                  # noqa: BLE001
        return ("UNDECIDED",
                "the region text: %s: %s" % (type(bad).__name__, bad),
                bindings, False)
    bits = min(w_ref, w_reg)
    solver = z3.Solver()
    solver.set("timeout", timeout_ms)
    solver.add(z3.Extract(bits - 1, 0, val_ref) !=
               z3.Extract(bits - 1, 0, val_reg))
    outcome = solver.check()
    if outcome == z3.unsat:
        return ("PROVED_ON_SHIP",
                "z3 proved the region text's RESULT BLOCK equal to the "
                "value this unit's own ship body leaves in its own "
                "answer home at %d bits, at a %d ms limit"
                % (bits, timeout_ms), bindings, False)
    if outcome == z3.sat:
        return ("DISPROVED",
                "z3 found a counterexample against this unit's own ship "
                "body: %s" % solver.model(), bindings, False)
    return ("UNDECIDED",
            "the solver did not answer inside its %d ms limit"
            % timeout_ms, bindings, True)


JVM_ADDRESS = re.compile(r"^\s*([0-9a-f]{6,16}):$")


def jvm_bodies():
    """the two JIT-emitted nmethods, from the JVM's OWN printed dump.
    A JIT has no ELF symbol table and no DWARF, so the bounds READ here
    are the JVM's own nmethod base and length -- its own testimony,
    read rather than computed.  FLAGGED as the one place the ruling's
    named sources do not exist."""
    doc = load("interp_jvm.json")
    out = {}
    for unit in doc["units"]:
        name = "java/op_%s" % unit["id"][1:]
        rows = []
        for run in unit["arch_unit"]:
            base = int(run["base"], 16)
            length = run["length"]
            for raw in run["objdump"]:
                # objdump prints `address:\tbytes\tmnemonic`.  A line
                # with only TWO fields is the byte continuation of the
                # instruction above it, not an instruction of its own --
                # reading it as one was a defect, fixed at first
                # observation (it read the continuation `7f 00 00` of a
                # movabs as an instruction whose mnemonic was `00`).
                fields = raw.split("\t")
                if len(fields) < 3:
                    continue
                hit = JVM_ADDRESS.match(fields[0])
                if hit is None:
                    continue
                address = int(hit.group(1), 16)
                mnemonic = re.sub(r"\s+", " ", fields[2].strip())
                mnemonic = mnemonic.split("#")[0].strip()
                if mnemonic == "":
                    continue
                rows.append({"address": "0x%x" % address,
                             "bytes": fields[1].strip(),
                             "mnem": mnemonic})
        out[name] = {
            "rows": rows,
            "base": unit["arch_unit"][0]["base"],
            "length": unit["arch_unit"][0]["length"],
            "nmethod_header": unit["nmethod_header"],
        }
    return out


def main():
    bounds = load("t94_bounds.json")
    jvm = jvm_bodies()
    records = []
    for source in bounds["records"]:
        unit = source["unit"]
        print("[unit] %s" % unit, flush=True)
        record = {
            "unit": unit,
            "language": source["language"],
            "label": source["label"],
            "handler_function": source["handler_function"],
            "old": OLD[unit],
            "arrival_contract": ARRIVAL[unit],
        }
        record["recarved"] = {
            "bounds_source": source["bounds_source"],
            "symbol_table_rows": source.get("symbol_table_rows"),
            "dwarf_rows": source.get("dwarf_rows"),
            "symbol_table_and_dwarf_agree":
                source.get("symbol_table_and_dwarf_agree"),
            "new_low": source.get("new_low"),
            "new_high": source.get("new_high"),
            "new_byte_length": source.get("new_byte_length"),
            "new_instruction_count": source.get("new_instruction_count"),
        }
        if source.get("binary") is None and unit in jvm:
            found = jvm[unit]
            base = int(found["base"], 16)
            source = dict(source)
            source["body"] = found["rows"]
            source["new_low"] = found["base"]
            source["new_high"] = "0x%x" % (base + found["length"])
            source["new_byte_length"] = found["length"]
            source["new_instruction_count"] = len(found["rows"])
            source["bounds_source"] = (
                "the JVM's OWN printed nmethod base and length "
                "(interp_jvm.json, nmethod header %r).  FLAGGED: a JIT "
                "has no ELF symbol table and no DWARF, so the ruling's "
                "two named sources do not exist for this unit; the "
                "JIT's own testimony is the only READ boundary there "
                "is, and it is read rather than computed."
                % found["nmethod_header"])
            record["recarved"]["bounds_source"] = source["bounds_source"]
            record["recarved"]["new_low"] = source["new_low"]
            record["recarved"]["new_high"] = source["new_high"]
            record["recarved"]["new_byte_length"] = source["new_byte_length"]
            record["recarved"]["new_instruction_count"] = \
                source["new_instruction_count"]

        if source.get("body") is None:
            record["outcome"] = "NO_BODY"
            record["new_verdict"] = "NO_BODY"
            record["cause"] = source.get(
                "refusal",
                source.get("bounds_source"))
            records.append(record)
            continue

        lines = body_lines(source)
        addrs = body_addresses(source)
        record["recarved"]["body_verbatim"] = lines
        record["recarved"]["body_addresses"] = [row["address"]
                                           for row in source["body"]]
        block_lines, exits, block_count = block_form_text(lines, addrs)
        record["recarved"]["block_count"] = block_count
        record["recarved"]["block_form_text"] = block_lines
        record["recarved"]["exits_left_as_written"] = exits
        record["machinery"] = machinery_of(lines)

        contract = ARRIVAL[unit]
        if contract["a"] is None:
            record["outcome"] = "REFUSED_BY_NAME"
            record["new_verdict"] = "UNDECIDED"
            record["cause"] = (
                "this handler declares ZERO formal parameters and reads "
                "its operands out of the VM frame through %r15, which "
                "region36 rules to be the region base and therefore not "
                "available to any lineage.  The form refuses by name "
                "(region36 section 2) rather than rendering onto a base "
                "the unit also uses as a value.")
            records.append(record)
            continue

        entry_contract = {"a": contract["a"], "b": contract["b"],
                          "result": contract["result"]}
        prior_text = "; ".join(block_lines)
        fields, refusal = CU.render(entry_contract, prior_text, [], True,
                                    result_width=contract["result_width"])
        if fields is None:
            fields, refusal2 = CU.render(entry_contract, prior_text, [],
                                         False,
                                         result_width=contract[
                                             "result_width"])
            if fields is None:
                record["outcome"] = "REFUSED_BY_NAME"
                record["new_verdict"] = "UNDECIDED"
                record["cause"] = ("the universal form refused by name: "
                                   "%s -- %s" % (refusal[0], refusal[1]))
                records.append(record)
                continue
            record["constant_materialization"] = "reduced"
        record["universal_form"] = {
            "universal_text": fields["universal_text"],
            "block_form": fields["block_form"],
            "block_directory": fields["block_directory"],
            "block_counts": fields["block_counts"],
            "result_block": fields["result_block"],
            "region_base": fields["region_base"],
            "region_size": fields["region_size"],
        }

        families = CU.arrival_family_list(entry_contract)
        region_lines = CU.split_lines(fields["universal_text"])
        verdict, detail, bindings, timed_out = gate_against_own_ship(
            lines, region_lines, families, fields["block_directory"],
            contract["result"], contract["result_width"], 20000)
        record["gate_bindings"] = bindings
        record["gate_at_20000ms"] = {"verdict": verdict, "detail": detail}
        record["new_verdict"] = verdict
        record["cause"] = detail
        if timed_out:
            print("   FLAGGED: solver time limit hit; re-running at "
                  "%d ms" % LONG_TIMEOUT_MS, flush=True)
            v2, d2, _b2, _t2 = gate_against_own_ship(
                lines, region_lines, families, fields["block_directory"],
                contract["result"], contract["result_width"],
                LONG_TIMEOUT_MS)
            record["gate_at_120000ms"] = {"verdict": v2, "detail": d2}
            record["answer_changed_with_more_room"] = (v2 != verdict)
            record["new_verdict"] = v2
            record["cause"] = d2
        else:
            record["gate_at_120000ms"] = {
                "verdict": "NOT_RUN",
                "detail": "the 20,000 ms run did not hit its time limit, "
                          "so the longer run would ask the same question "
                          "of the same solver state"}
            record["answer_changed_with_more_room"] = False
        record["outcome"] = "GATED"
        print("   verdict %s" % record["new_verdict"], flush=True)
        memory_guard(unit)
        records.append(record)

    moved = []
    for record in records:
        before = record["old"]["old_verdict"]
        after = record["new_verdict"]
        if before != after:
            moved.append({"unit": record["unit"], "from": before,
                          "to": after, "cause": record["cause"]})

    out = {
        "meta": {
            "generator": "t94_recarve.py",
            "task": "TASK 94 round 18 -- the eleven interpreter units "
                    "re-carved to their handler function's body",
            "ruling": "the owner 2026-09-05, CORE_0_3_5_1_arch_unit.md, "
                      "'the unit's boundary -- RULED by the owner 2026-09-05'",
            "form": "region36.py's ruled virtual region, rendered by "
                    "canon36_universal.render; both imported unmodified",
            "reads_read_only": [
                "t94_bounds.json", "interp_canon35.json",
                "interp_canon34.json",
                "canon_interp_units_cpython.json",
                "canon_interp_units_java.json", "interp_fastpath.json",
                "interp_jvm.json"],
            "spelling": "the member label appears once per unit, as a "
                        "display field on the member.  No key, "
                        "grouping, pairing or row structure in this "
                        "file uses it.",
            "peak_resident_kb": peak_kb(),
            "memory_abort_name": "T94_RECARVE_MEMORY_ABORT",
            "solver_limits_ms": [20000, LONG_TIMEOUT_MS],
        },
        "records": records,
        "verdict_movements": moved,
        "summary": {
            "units": len(records),
            "moved": len(moved),
        },
    }
    with open(OUT, "w") as handle:
        json.dump(out, handle, indent=1)
    print("wrote %s ; %d of %d verdicts moved ; peak resident %d kB"
          % (OUT, len(moved), len(records), peak_kb()))


if __name__ == "__main__":
    main()
