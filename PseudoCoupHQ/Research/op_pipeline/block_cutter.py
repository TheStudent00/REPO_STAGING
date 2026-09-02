#!/usr/bin/env python3
"""block_cutter.py -- Task 20 wrapper for canon2's block cutter, fixing
two named defects found while carving CPython's long_add fast path
(interp_fastpath.json, carve.defects_found_reusing_cut_blocks).

THIS FILE DOES NOT EDIT canon2.py.  It imports canon2's parsing
(canon.parse, canon.JUMP) and canon2's own JUMP_TARGET regex, and
supplies a REPLACEMENT walk built at INSTRUCTION granularity, per the
wrapper precedent already used across this pipeline (new module wraps
a shared module; the shared module stays untouched).

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the
member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim.
[N/A here -- this module does not group or pair units; it walks
control flow inside ONE unit. No spelling-key check applies.]

TWO DEFECTS FIXED (verbatim record, matching
interp_fastpath.json's carve.defects_found_reusing_cut_blocks):

DEFECT A -- alignment padding after ret/jmp becomes a block leader.
    canon2.cut_blocks() derives a block's successors from
    edges.get(LAST_INSTRUCTION_INDEX) only, i.e. from the block's
    nominal LAST index under the textbook leader/leader cut. Every
    unit that machinery was built for is a tightly captured probe
    slice where a ret is always the unit's own last instruction. A
    real ship binary instead has compiler alignment nopl/nopw padding
    AFTER a ret/jmp that lands mid-function, so the true
    control-transfer instruction sits inside the nominal block rather
    than at its end, and the naive fallthrough rule invents an edge
    into whatever block happens to sit next in memory.
    FIX: classify() below marks every ret/unconditional-jmp/trap
    instruction as a walk-terminating LEADER in its own right --
    reachability is computed one instruction at a time, and a
    ret/jmp/trap instruction's successor set is read off ITS OWN
    index, never inherited from a nominal block's last index. Padding
    after such an instruction is reachable only if something else
    (a branch target) also lands on it.

DEFECT B -- a bare "<symbol>" jump target resolves as offset 0 into
    THIS unit.
    canon2.find_jump_target_offset() returns 0 for any bare "<sym>"
    match with no "+0xNN" suffix, correct for a self-contained probe
    (the only symbol its own disassembly can name is the unit itself,
    at its own start), wrong for a real binary slice that tail-jumps
    to OTHER, external, named functions.
    FIX: find_jump_target_offset_checked() below takes the unit's own
    symbol name and only resolves an in-unit offset when the bracketed
    name MATCHES that symbol; a different name is recorded as an
    EXTERNAL exit with no successor inside the unit.
"""

import re

import canon


BARE_OR_OFFSET = re.compile(
    r"<([^+>]*)\+0x([0-9a-fA-F]+)>|<([^+>]*)>")


def find_jump_target_offset_checked(operand_text, own_symbol):
    """like canon2.find_jump_target_offset, but a bare '<sym>' (no
    '+0xNN') is only resolved to offset 0 when sym == own_symbol.  A
    bare '<other_sym>' names a DIFFERENT function (defect B) and
    returns None with is_external=True."""
    m = BARE_OR_OFFSET.search(operand_text)
    if m is None:
        return None, False
    if m.group(2) is not None:
        # "<sym+0xNN>" -- offset given explicitly.  This slice's own
        # walk only ever uses such offsets against its own unit, so
        # no symbol-name check is needed for this branch.
        return int(m.group(2), 16), False
    sym = m.group(3)
    if sym == own_symbol:
        return 0, False
    return None, True


def classify(mnem):
    """-> one of 'jump' (conditional or unconditional), 'ret', 'trap',
    'call', 'other'."""
    bare = mnem
    if canon.JUMP.match(bare):
        return "jump"
    if bare in ("ret", "retq"):
        return "ret"
    if bare in ("ud2",):
        return "trap"
    if bare in ("call", "callq"):
        return "call"
    return "other"


def walk_reachable(lines, addrs, own_symbol, start_index=0,
                    unit_base_addr=None):
    """instruction-granularity reachability walk, fixing defects A and
    B above.  `lines` are objdump mnemonic strings (address-stripped,
    per this unit's own captured text); `addrs` are the matching real
    addresses (canon2.real_addresses).  Returns a dict:

      instructions   -- ordered list of {index, addr, mnem} reached
      address_ranges -- contiguous [start_addr, end_addr) runs over
                         the reached indices, merged when adjacent
                         instructions are contiguous in address
      external_exits -- [{at_index, instruction, target_symbol}]
                         for jumps/calls resolved as DEFECT-B cases
      unresolved_exits -- [{at_index, instruction}] for jump targets
                         this walk could not resolve at all

    `unit_base_addr` -- the unit's OWN real starting address, i.e.
    addrs[0] for a unit that starts at its own symbol's offset 0. A
    disassembler's "<sym+0xNN>" branch-target syntax names an offset
    from sym's start, NOT the absolute address directly -- so a
    target offset must be added to unit_base_addr before it is looked
    up in addrs, exactly as objdump itself computed it when it
    printed that operand. Defaults to addrs[0] when not given (true
    whenever start_index == 0; must be supplied explicitly otherwise,
    as this test does for long_add).
    """
    if unit_base_addr is None:
        unit_base_addr = addrs[0] if addrs else 0
    n = len(lines)
    addr_to_index = {}
    for i, a in enumerate(addrs):
        addr_to_index[a] = i

    parsed = []
    for line in lines:
        if line.strip() == "":
            # a stray/empty entry (e.g. the slice-extractor split-
            # instruction defect this task also fixes, see
            # slice_extractor_fix.py) carries no control-transfer
            # semantics: walk through it as an inert instruction
            # rather than crash canon.parse on empty text.
            parsed.append(("", []))
            continue
        mnem, operands = canon.parse(line)
        parsed.append((mnem, operands))

    reached = set()
    external_exits = []
    unresolved_exits = []
    stack = [start_index]
    while stack:
        i = stack.pop()
        if i in reached or i < 0 or i >= n:
            continue
        reached.add(i)
        mnem, operands = parsed[i]
        kind = classify(mnem)
        if kind == "ret" or kind == "trap":
            # DEFECT A: a ret/trap NEVER falls through, regardless of
            # whether alignment padding follows it in memory.
            continue
        if kind == "jump":
            resolved_any = False
            for operand in operands:
                off, is_external = find_jump_target_offset_checked(
                    operand, own_symbol)
                if is_external:
                    external_exits.append({
                        "at_index": i,
                        "instruction": mnem + " " + " ".join(operands),
                        "target_symbol": operand,
                    })
                    resolved_any = True
                    continue
                if off is None:
                    continue
                target_idx = addr_to_index.get(unit_base_addr + off)
                if target_idx is None:
                    unresolved_exits.append({
                        "at_index": i,
                        "instruction": mnem + " " + " ".join(operands),
                    })
                    continue
                stack.append(target_idx)
                resolved_any = True
            if mnem != "jmp" and i + 1 < n:
                # conditional jump: fallthrough is a real successor
                stack.append(i + 1)
            elif mnem == "jmp" and not resolved_any:
                unresolved_exits.append({
                    "at_index": i,
                    "instruction": mnem + " " + " ".join(operands),
                })
            # DEFECT A, unconditional-jmp case: no fallthrough is
            # pushed here even though i+1 exists in `lines` -- an
            # unconditional jmp's only successor is its resolved
            # target(s) (or an external exit), never the next
            # physical instruction.
            continue
        if kind == "call":
            if i + 1 < n:
                stack.append(i + 1)
            continue
        # 'other': ordinary fallthrough
        if i + 1 < n:
            stack.append(i + 1)

    ordered = sorted(reached)
    instructions = []
    for i in ordered:
        mnem, operands = parsed[i]
        text = mnem if not operands else mnem + " " + " ".join(operands)
        instructions.append({
            "index": i,
            "addr": addrs[i],
            "mnem": text,
        })

    address_ranges = []
    run_start = None
    run_end = None
    prev_addr = None
    prev_len = None
    for pos, i in enumerate(ordered):
        a = addrs[i]
        length = (addrs[i + 1] - a) if i + 1 < len(addrs) else None
        if run_start is None:
            run_start = a
            run_end = a
        elif prev_len is not None and prev_addr + prev_len == a:
            pass
        else:
            address_ranges.append((run_start, run_end))
            run_start = a
        run_end = a + (length if length is not None else 1)
        prev_addr = a
        prev_len = length
    if run_start is not None:
        address_ranges.append((run_start, run_end))

    return {
        "instructions": instructions,
        "address_ranges": address_ranges,
        "external_exits": external_exits,
        "unresolved_exits": unresolved_exits,
    }
