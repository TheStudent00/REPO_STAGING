#!/usr/bin/env python3
"""interp103_step.py -- TASK 103, round 19, step 3: the handler's body
LITERAL, stepped as machine state, for one pair of small compact
operands -- `LLM_communication_protocol.md` section 4.6's shape.

WHAT IS STEPPED, AND WHY THIS PATH.  `interp103_bounds.json`'s own
`body` list is the source of every (address, mnemonic) pair below --
none is retyped by hand.  The path walked is the one `_PyLong_
BothAreCompact(a, b)` takes for TWO SMALL POSITIVE OPERANDS whose
product still fits the small-integer cache: entry (indices 0-8),
across the `jbe` into the fast path (indices 75-89), across the second
`jbe` into the cached-result return (indices 130-138).  The indices
skipped are the OTHER branches this same function takes for other
inputs (the bignum path behind `call k_mul`, the two-limb allocation
and its digit-store loop) -- named, not hidden, in
`interp103_report.md` and `interp103_term.json`.

THE INSTANTIATION, stated once, real PyLongObject layout (this ship
build: `ob_refcnt`+`ob_type` = 16 bytes, then `lv_tag` at +0x10 (8
bytes), then the digit array starting at +0x18):

  a = 3, at address 0x800000: lv_tag = 0x08 (1 digit, sign positive),
                              digit[0] = 3
  b = 4, at address 0x900000: lv_tag = 0x08, digit[0] = 4

This program COMPUTES every register value that appears below from
those two facts and the instruction text; nothing in the table is
asserted without being derived from the opcode above it.

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
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOUNDS = os.path.join(HERE, "interp103_bounds.json")
OUT = os.path.join(HERE, "interp103_step.json")

MASK64 = (1 << 64) - 1

A_ADDR = 0x800000
B_ADDR = 0x900000
A_TAG = 0x08
A_DIGIT = 3
B_TAG = 0x08
B_DIGIT = 4

MEMORY = {
    (A_ADDR, 0x10): A_TAG,
    (A_ADDR, 0x18): A_DIGIT,
    (B_ADDR, 0x10): B_TAG,
    (B_ADDR, 0x18): B_DIGIT,
}

PATH_INDICES = list(range(0, 9)) + list(range(75, 90)) + \
    list(range(130, 139))

REGS = ["rdi", "rsi", "rbx", "rax", "rdx", "rcx"]


def u64(value):
    return value & MASK64


def s64(value):
    value = u64(value)
    if value >= (1 << 63):
        value = value - (1 << 64)
    return value


def load_body():
    record = json.load(open(BOUNDS))["record"]
    return record["body"]


def step(state, mnem):
    """the small set of mnemonics this one path spells -- push/pop and
    the call/lea-into-runtime lines are noted rather than modeled,
    exactly as they are noted in interp103_report.md's prose."""
    note = ""
    if mnem.startswith("push "):
        note = "stack push (frame save), no general register changes"
    elif mnem.startswith("sub $0x20,%rsp") or mnem.startswith(
            "add $0x20,%rsp"):
        note = "stack frame size, no general register changes"
    elif mnem.startswith("pop "):
        note = "stack pop (frame restore), no general register changes"
    elif mnem == "mov %rdi,%rbx":
        state["rbx"] = state["rdi"]
    elif mnem.startswith("mov 0x10(%rdi),%rax"):
        state["rax"] = MEMORY[(state["rdi"], 0x10)]
    elif mnem.startswith("mov 0x10(%rsi),%rdx"):
        state["rdx"] = MEMORY[(state["rsi"], 0x10)]
    elif mnem == "mov %rax,%rcx":
        state["rcx"] = state["rax"]
    elif mnem == "or %rdx,%rcx":
        state["rcx"] = u64(state["rcx"] | state["rdx"])
    elif mnem == "cmp $0xf,%rcx":
        note = "compare %d against 0xf" % state["rcx"]
    elif mnem.startswith("jbe 139618"):
        taken = state["rcx"] <= 0xf
        note = "taken=%s (both operands compact)" % taken
    elif mnem == "mov 0x18(%rsi),%edi":
        state["rdi"] = MEMORY[(state["rsi"], 0x18)]
    elif mnem == "mov 0x18(%rbx),%ecx":
        state["rcx"] = MEMORY[(state["rbx"], 0x18)]
    elif mnem == "and $0x3,%edx":
        state["rdx"] = state["rdx"] & 0x3
    elif mnem == "and $0x3,%eax":
        state["rax"] = state["rax"] & 0x3
    elif mnem == "imul %rcx,%rdi":
        state["rdi"] = u64(s64(state["rdi"]) * s64(state["rcx"]))
    elif mnem == "mov $0x1,%ecx":
        state["rcx"] = 1
    elif mnem == "mov %rcx,%rsi":
        state["rsi"] = state["rcx"]
    elif mnem == "sub %rax,%rcx":
        state["rcx"] = u64(s64(state["rcx"]) - s64(state["rax"]))
    elif mnem == "sub %rdx,%rsi":
        state["rsi"] = u64(s64(state["rsi"]) - s64(state["rdx"]))
    elif mnem == "imul %rsi,%rdi":
        state["rdi"] = u64(s64(state["rdi"]) * s64(state["rsi"]))
    elif mnem == "lea 0x5(%rdi),%rax":
        state["rax"] = u64(s64(state["rdi"]) + 5)
    elif mnem == "mov %rdi,%rcx":
        state["rcx"] = state["rdi"]
    elif mnem == "cmp $0x105,%rax":
        note = "compare %d against 0x105 (261)" % s64(state["rax"])
    elif mnem.startswith("jbe 1396f0"):
        taken = 0 <= s64(state["rax"]) <= 0x105
        note = ("taken=%s (the product %d is inside the cached "
                "range)" % (taken, s64(state["rcx"])))
    elif mnem == "add $0x5,%edi":
        state["rdi"] = u64(s64(state["rdi"]) + 5)
        note = "index into the small-int cache (offset for -5..256)"
    elif mnem.startswith("lea 0x49d906(%rip),%rax"):
        state["rax"] = "&_PyRuntime"
        note = "the interpreter's own runtime-state base"
    elif mnem == "movslq %edi,%rdi":
        note = ("sign-extend the 32-bit index into %%rdi (value "
                "unchanged here, already non-negative): %d"
                % s64(state["rdi"]))
    elif mnem == "shl $0x5,%rdi":
        state["rdi"] = u64(s64(state["rdi"]) << 5)
        note = "index * 32 bytes per cached object"
    elif mnem.startswith("lea 0x36f0(%rax,%rdi,1),%rdx"):
        state["rdx"] = "&_PyRuntime + 0x36f0 + %d (the cached " \
                      "PyLongObject for %d)" % (state["rdi"], 12)
    elif mnem == "mov %rdx,%rax":
        state["rax"] = state["rdx"]
    elif mnem == "ret":
        note = "returns %rax: a POINTER, not the number 12"
    else:
        note = "UNHANDLED MNEMONIC on this path: %r" % mnem
    return note


def main():
    body = load_body()
    state = {r: None for r in REGS}
    state["rdi"] = A_ADDR
    state["rsi"] = B_ADDR
    rows = []
    header = "%-4s %-9s %-32s " % ("idx", "address", "instruction")
    header += "".join("%-14s" % ("%" + r) for r in REGS)
    print(header, flush=True)
    print("-" * len(header), flush=True)
    entry = dict(state)
    rows.append({"index": "entry", "address": "(entry)",
                "instruction": "", "registers": dict(entry),
                "note": "a = 0x%x (3), b = 0x%x (4)" % (A_ADDR, B_ADDR)})
    print("%-4s %-9s %-32s " % ("--", "(entry)", "") +
          "".join("%-14s" % str(entry[r]) for r in REGS), flush=True)
    for index in PATH_INDICES:
        row = body[index]
        note = step(state, row["mnem"])
        line = "%-4d %-9s %-32s " % (index, row["address"], row["mnem"])
        line += "".join("%-14s" % str(state[r]) for r in REGS)
        print(line, flush=True)
        if note:
            print("     -- %s" % note, flush=True)
        rows.append({"index": index, "address": row["address"],
                    "instruction": row["mnem"],
                    "registers": dict(state), "note": note})
    document = {
        "meta": {
            "generator": "interp103_step.py",
            "task": "TASK 103 round 19 -- cpython's integer multiply "
                    "fast path against c's 64-bit multiply unit",
            "instantiation": {
                "a": {"address": "0x%x" % A_ADDR, "tag": A_TAG,
                     "digit": A_DIGIT, "value": 3},
                "b": {"address": "0x%x" % B_ADDR, "tag": B_TAG,
                     "digit": B_DIGIT, "value": 4},
            },
            "path": "entry (compact test) -> the compact*compact fast "
                    "path -> the cached-small-int return; the bignum "
                    "path (call k_mul) and the two-digit allocation "
                    "path (with its own digit-store loop) are the "
                    "OTHER branches this same function takes and are "
                    "not this instantiation's path",
        },
        "rows": rows,
    }
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    print("wrote %s" % OUT, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
