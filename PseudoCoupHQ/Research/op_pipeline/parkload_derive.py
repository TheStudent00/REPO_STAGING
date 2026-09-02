#!/usr/bin/env python3
"""parkload_derive.py -- THE PARK-RELOAD IDIOM.  MACHINE-GENERATED.

DO NOT EDIT BY HAND.  This file is written by parkload_make.py, which
copies canon4.py's `derive_runnable3` and `derive_block_body`
verbatim and applies exactly two literal edits.  Re-run
`parkload_make.py` after any change to canon4.py; it refuses to write
if its edits no longer match.

WHAT WAS WRONG, in plain words.  canon4.py assigns each erased value a
home: a temp register while the pool lasts, then a stack slot.  When
it then prints an instruction whose operands include two homes that
are not plain registers, it refuses the whole unit:

    "erasure_refused: two stack-spilled operands in one instruction"

Two separate faults hide in that one line.

  FAULT ONE -- THE COUNT IS WRONG.  The test counts pieces that do not
  begin with "%".  An IMMEDIATE does not begin with "%".  So
  `and $0x1,-0x8(%rsp)` -- a perfectly legal x86-64 instruction with
  ONE memory operand -- was counted as two and refused.  Measured: of
  the 22 corpus units carrying this refusal, several reach it this
  way, with no second memory operand anywhere in the instruction.

  FAULT TWO -- A REAL PAIR HAS A KNOWN IDIOM.  x86-64 permits at most
  one memory operand per instruction, so two really do have to be
  resolved.  The compilers in this corpus resolve it the same way
  every time: load one operand into a register first, then use it.
  That is the PARK-RELOAD IDIOM -- the value was PARKED in its
  designated location, and is RELOADED for the length of one
  instruction.  It is a canonicalization step, not a computation: the
  reload register holds the value that the designated location holds,
  and nothing else changes.

WHY A DEDICATED RELOAD REGISTER.  designated_memory.py holds %r11 and
%xmm15 out of the value pools for exactly this.  A reload register
drawn from the pool would need an eviction, and an eviction changes
which register holds which value -- which would make two units with
the same shape render differently, defeating the point of a
standardized selection (AgentMemory, 2026-08-28: temps are
STANDARDIZED, not limited).

FOUR MORE CAUSES, FOUND WHILE GATING THE UNITS THIS RULE UNBLOCKED,
FIXED AT FIRST OBSERVATION.  None could be seen before, because every
unit that exposes them was refused earlier and never reached a gate.
Two live in canon33_fixes.py (the block fall-through and the
alias-blind dead-mov cleanup); three live here:

  CAUSE 3 -- THE ANSWER MOVE WAS ALWAYS 32 BITS.  canon4.py landed the
  finished value in the answer register with `ensure(..., 1)`, the
  32-bit alias, whatever the answer's width.  A 64-bit answer was
  truncated: the unit computed the right value and returned the wrong
  one.  MEASURED on `swift/op_703`, DISPROVED by the gate with
  `b = 11`, `a = 4914318053212165`.  Fixed by rendering that move at
  the 64-bit alias, which is never worse (a value written by a 32-bit
  instruction already has zeroes above bit 31 on x86-64).

  CAUSE 4 -- AN IN-PLACE WRITE CLOBBERED A STILL-LIVE VALUE.  An
  instruction that reads and writes one operand was rendered on top of
  the value it reads, even when a later step still reads that value.
  MEASURED on `cpp/op_765`: `shr $1,%rdi` destroyed `a`, and the very
  next step's `and $0x1,%edi` then read the shifted value instead of
  `a`.  Fixed by `preserve_if_live`: when the old value is read by a
  later step -- or is a contract value (`a`/`b`), which a later BLOCK
  this function cannot see may read -- it is copied to a fresh home
  first and the instruction writes there.  This is the same shape the
  compiler itself emitted (`mov %rdi,%rax ; shr $1,%rax`).

  CAUSE 5 -- THE DIVIDE FAMILY'S WIDTHS WERE FIXED AT 32 BITS.  The
  dividend was moved into the answer register with a 32-bit move
  before every sign-extend, and the two dividend halves were ensured
  at 32 bits before every divide.  For a 64-bit divide (`cqto` +
  `idiv %rsi`) that truncates the dividend.  MEASURED on
  `rust/op_649`, DISPROVED with `b = 1`,
  `a = 10990797176293339890`.  Fixed by reading the width from the
  sign-extend mnemonic and from the step's own recorded divisor
  width.

WHEN IT STILL REFUSES, by name:
  * `two memory operands and neither is a designated location` -- the
    instruction's own source text carries a memory operand this pass
    did not create (a rip-relative constant, an address computation);
    reloading it would change what the instruction does.
  * `more than two memory operands` -- never observed; refused rather
    than guessed.
  * `RedZoneExhausted` from designated_memory.py.

Every refusal text produced here NAMES THE BUILD it was derived from,
which the canon4.py texts did not: the corpus record these units are
derived from is `sem_anchored_<lang>.json`'s `mnem`, and that text was
verified line-identical to `op_units_<lang>.json`'s own `ship` mnem
for every unit of all five compiled languages (canon33_designated.py
prints the check).  So the refusals fire against the SHIP build.

THE SPELLING BAN.  No operator token appears here; this file handles
registers, offsets and value names only.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon  # noqa: E402
import canon2  # noqa: E402
import canon4  # noqa: E402
import designated_memory as DM  # noqa: E402

FAMILY_OF = canon.FAMILY_OF
WIDTH_OF = canon.WIDTH_OF
Erasure = canon2.Erasure

is_mem = canon4.is_mem
loc_text = canon4.loc_text
render = canon4.render


# ------------------------------------------------------ the classifier

def piece_kind(text, bench):
    """what one rendered operand piece IS.  Four kinds, and the
    difference between the last two is the whole point: a designated
    location is ours and may be reloaded; any other memory operand
    came from the unit's own source text and may not."""
    if text.startswith("%"):
        return "register"
    if text.startswith("$"):
        return "immediate"
    if bench.designation_of_text(text) is not None:
        return "designated"
    return "source-memory"


def piece_shape(operands, slot, bench, piece_text):
    """the width index and file of one piece, read off the ORIGINAL
    operand of the instruction rather than guessed from the rendered
    text."""
    kind = piece_kind(piece_text, bench)
    width_index = 0
    is_vector = False
    operand = operands[slot] if slot < len(operands) else ""
    if canon.is_plain_register(operand):
        regname = canon.registers_in(operand)[0]
        width_index = WIDTH_OF.get(regname, 1)
        family = FAMILY_OF.get(regname)
        if family is not None:
            is_vector = canon.is_vector(family)
    return kind, width_index, is_vector


def park_reload(step, pieces, operands, role, write_slot, write_kind,
                bench, report):
    """resolve the memory operands of ONE instruction.

    Returns (pieces, before_lines, after_lines).  `report` is a list
    this function appends one record to per park-reload it performs,
    so the driver can show what happened without re-deriving it.

    TWO CASES, and they are different:

      THE DESTINATION IS A DESIGNATED LOCATION.  x86-64 has no
      `cmov` into memory at all, and an immediate written to memory
      needs an explicit size suffix the erased form does not carry.
      Both are avoided the same way the compilers themselves avoid
      them: do the work in the reload register and re-park the result.
      When the instruction READS its destination as well as writing it
      (`write_kind == "rw"`, e.g. a conditional move, which leaves the
      destination untouched when its condition is false) the location
      is loaded into the reload register FIRST, so the untouched case
      still carries the parked value.

      A SOURCE IS A DESIGNATED LOCATION and some other operand is also
      memory.  Load that source into the reload register and read it
      from there.

    FLAGS ARE SAFE.  Every line this function adds is a `mov`-family
    load or store, and no x86-64 `mov` writes the flags -- so an
    instruction that sets flags for a later branch is not separated
    from that branch by anything that changes them.

    REFUSALS, by name, never a guess:
      * both the destination and a source of one instruction are
        designated locations -- one reload register, two demands;
      * more than two memory operands;
      * two memory operands of which the reloadable one is not ours
        (a rip-relative constant or an address computation from the
        unit's own source text: reloading it would change what the
        instruction does).
    """
    kinds = []
    widths = []
    vectors = []
    for slot in range(len(pieces)):
        kind, width_index, is_vector = piece_shape(operands, slot,
                                                   bench, pieces[slot])
        kinds.append(kind)
        widths.append(width_index)
        vectors.append(is_vector)
    memory_slots = []
    for slot in range(len(pieces)):
        if kinds[slot] in ("designated", "source-memory"):
            memory_slots.append(slot)
    if not memory_slots:
        return pieces, [], []
    destination_parked = False
    if write_slot is not None and write_slot < len(kinds):
        destination_parked = (kinds[write_slot] == "designated")
    source_memory_slots = []
    for slot in memory_slots:
        if slot == write_slot and destination_parked:
            continue
        source_memory_slots.append(slot)
    if not destination_parked and len(source_memory_slots) <= 1:
        return pieces, [], []
    if destination_parked and not source_memory_slots:
        return park_destination(step, pieces, kinds, widths, vectors,
                                write_slot, write_kind, bench, report)
    if destination_parked and source_memory_slots:
        return park_both(step, pieces, kinds, widths, vectors,
                         write_slot, write_kind, source_memory_slots,
                         bench, report)
    if len(source_memory_slots) > 2:
        raise Erasure(
            "erasure_refused: more than two memory operands in one "
            "instruction of the unit's own SHIP build -- never "
            "observed in this corpus, refused rather than guessed")
    reloadable = []
    for slot in source_memory_slots:
        if kinds[slot] == "designated":
            reloadable.append(slot)
    if not reloadable:
        raise Erasure(
            "erasure_refused: two memory operands meet in one "
            "instruction of the unit's own SHIP build and neither is "
            "a designated location, so the park-reload idiom does not "
            "apply")
    slot = reloadable[0]
    register_text = DM.render_location(
        DM.reload_register(vectors[slot], 1), widths[slot])
    mnemonic = DM.reload_mnemonic(vectors[slot], widths[slot])
    line = "%s %s,%s" % (mnemonic, pieces[slot], register_text)
    record = {}
    record["shape"] = "source-reload"
    record["mnem"] = step["mnem"]
    record["designation"] = bench.designation_of_text(pieces[slot])
    record["slot_text"] = pieces[slot]
    record["reload_register"] = register_text
    record["lines_before"] = [line]
    record["lines_after"] = []
    report.append(record)
    new_pieces = list(pieces)
    new_pieces[slot] = register_text
    return new_pieces, [line], []


def park_both(step, pieces, kinds, widths, vectors, write_slot,
              write_kind, source_memory_slots, bench, report):
    """the destination AND one source are designated locations.  The
    destination takes reload register 0, the source reload register 1;
    the order is fixed so two units of the same shape render the same
    text."""
    if len(source_memory_slots) != 1:
        raise Erasure(
            "erasure_refused: a parked destination meets %d memory "
            "sources in one instruction of the unit's own SHIP build "
            "-- refused rather than guessed"
            % len(source_memory_slots))
    slot = source_memory_slots[0]
    if kinds[slot] != "designated":
        raise Erasure(
            "erasure_refused: a parked destination meets a memory "
            "operand that came from the unit's own SHIP source text, "
            "not from a designated location -- reloading it would "
            "change what the instruction does")
    pieces, before, after = park_destination(
        step, pieces, kinds, widths, vectors, write_slot, write_kind,
        bench, report)
    register_text = DM.render_location(
        DM.reload_register(vectors[slot], 1), widths[slot])
    mnemonic = DM.reload_mnemonic(vectors[slot], widths[slot])
    line = "%s %s,%s" % (mnemonic, pieces[slot], register_text)
    record = {}
    record["shape"] = "source-reload-beside-destination"
    record["mnem"] = step["mnem"]
    record["designation"] = bench.designation_of_text(pieces[slot])
    record["slot_text"] = pieces[slot]
    record["reload_register"] = register_text
    record["lines_before"] = [line]
    record["lines_after"] = []
    report.append(record)
    new_pieces = list(pieces)
    new_pieces[slot] = register_text
    return new_pieces, [line] + before, after


def park_destination(step, pieces, kinds, widths, vectors, write_slot,
                     write_kind, bench, report):
    """the read-modify-write half of the idiom: the instruction's
    destination is a designated location, so the work happens in the
    reload register and the result is re-parked."""
    is_vector = vectors[write_slot]
    width_index = widths[write_slot]
    register_text = DM.render_location(
        DM.reload_register(is_vector, 0), width_index)
    mnemonic = DM.reload_mnemonic(is_vector, width_index)
    slot_text = pieces[write_slot]
    before = []
    if write_kind == "rw":
        before.append("%s %s,%s" % (mnemonic, slot_text, register_text))
    after = ["%s %s,%s" % (mnemonic, register_text, slot_text)]
    record = {}
    record["shape"] = "destination-repark"
    record["mnem"] = step["mnem"]
    record["write_kind"] = write_kind
    record["designation"] = bench.designation_of_text(slot_text)
    record["slot_text"] = slot_text
    record["reload_register"] = register_text
    record["lines_before"] = list(before)
    record["lines_after"] = list(after)
    report.append(record)
    new_pieces = list(pieces)
    new_pieces[write_slot] = register_text
    return new_pieces, before, after




# --------------------------------------------- the divide-family widths

SIGN_EXTEND_WIDTH = {
    "cltd": 1,   # 32-bit dividend: %eax -> %edx:%eax
    "cwtl": 1,
    "cqto": 0,   # 64-bit dividend: %rax -> %rdx:%rax
    "cqo": 0,
    "cltq": 0,
}


def sign_extend_width(mnemonic):
    """CAUSE 5 (see the header): the width index at which the dividend
    must arrive in the answer register, read off the sign-extend
    instruction's own mnemonic instead of being fixed at 32 bits."""
    if mnemonic not in SIGN_EXTEND_WIDTH:
        raise Erasure(
            "erasure_refused: sign-extend mnemonic %r has no recorded "
            "dividend width -- refused rather than guessed" % mnemonic)
    return SIGN_EXTEND_WIDTH[mnemonic]


# ------------------------------------- the in-place-clobber guard

def value_read_later(steps, index, name):
    """does any LATER step of this list read `name`?  Reads are taken
    from the step record's own fields -- `reads`, `slot_names` and the
    hardware pin -- never inferred from text."""
    for step in steps[index + 1:]:
        for read in step.get("reads") or []:
            if read == name:
                return True
        for slot_name in step.get("slot_names") or []:
            if slot_name == name:
                return True
        if step.get("pin_cl") == name:
            return True
    return False


def preserve_copy_line(current, fresh):
    """the instruction that copies a whole value from one location to
    another, at full width.  Refuses by name rather than emitting
    something that would not assemble."""
    current_vector = (not is_mem(current)) and canon.is_vector(current)
    fresh_vector = (not is_mem(fresh)) and canon.is_vector(fresh)
    current_text = DM.render_location(current, 0)
    fresh_text = DM.render_location(fresh, 0)
    if current_vector and fresh_vector:
        return "movaps %s,%s" % (current_text, fresh_text)
    if current_vector != fresh_vector:
        return "movq %s,%s" % (current_text, fresh_text)
    return "mov %s,%s" % (current_text, fresh_text)


def preserve_if_live(text, steps, index, old_name, write_name, target,
                     write_vec, bench):
    """THE IN-PLACE-CLOBBER GUARD (CAUSE 4, see the header).  An
    instruction that reads and writes one operand would otherwise be
    rendered ON TOP of the value it reads.  That is only sound when
    the old value is dead afterwards.  When it is still read later --
    or when it is a contract value (`a`/`b`), which a LATER BLOCK this
    function cannot see may still read -- the value is copied into a
    fresh home first and the instruction writes there instead."""
    if old_name is None:
        return target, []
    still_live = value_read_later(steps, index, old_name)
    if not still_live and old_name not in ("a", "b"):
        return target, []
    fresh = bench.location_for(write_name, write_vec)
    if fresh == target:
        return target, []
    return fresh, [preserve_copy_line(target, fresh)]



# ------------------------------------------- copied from canon4.py
# Everything below this line is canon4.py's own source text, with the
# two edits parkload_make.py names in its header.  Do not edit here.


def derive_runnable33(steps, final_name, contract, bench,
                      report):
    """canon2.py's derive_runnable(), with the temps-exhausted refusal
    (gap b) replaced by a stack-slot overflow home.  `bench` is a
    Bench instance; passing the SAME instance across several calls (as
    the branching driver does, once per block) makes register/stack
    assignment consistent for a value that is read in one block and
    was defined in an earlier one."""
    reg_of = {}
    if contract["a"] is not None:
        reg_of["a"] = contract["a"]
    if contract["b"] is not None:
        reg_of["b"] = contract["b"]
    text = []

    # canon4 fix (in-place-no-known-register / passthrough causes): a
    # value named literally "a" or "b" is, BY THE ENTRY CONTRACT ITSELF,
    # already sitting in contract["a"]/contract["b"] the moment the unit
    # starts -- even if some relabeling step lost that register from
    # reg_of before this point.  This is not a guess: it is the entry
    # contract, read back, never a new register choice.
    def contract_fallback(name):
        if name == "a" and contract.get("a") is not None:
            return contract["a"]
        if name == "b" and contract.get("b") is not None:
            return contract["b"]
        return None

    def ensure(name, target, width):
        cur = reg_of.get(name)
        if cur is None:
            cur = contract_fallback(name)
            if cur is not None:
                reg_of[name] = cur
        if cur is None:
            raise Erasure("erasure_refused: value %s is read before it "
                          "is defined or before the unit's entry "
                          "contract names it" % name)
        if cur == target:
            return
        if is_mem(cur):
            text.append("mov %s,%%%s" % (cur[1], render(target, width)))
            reg_of[name] = target
            return
        cur_vec = canon.is_vector(cur)
        target_vec = canon.is_vector(target)
        if cur_vec and target_vec:
            mnem = "movaps"
        elif cur_vec != target_vec:
            mnem = "movq"
        else:
            mnem = "mov"
        text.append("%s %%%s,%%%s" % (mnem, render(cur, width),
                                      render(target, width)))
        reg_of[name] = target

    def loc_for(name, is_vec):
        return bench.location_for(name, is_vec)

    for step_index, step in enumerate(steps):
        kind = step["kind"]
        if kind == "sign_extend":
            src = step["reads"][0]
            # EDIT 5 (the dividend arrives at its own width).
            ensure(src, "rax", sign_extend_width(step["mnem"]))
            text.append(step["mnem"])
            dst = step["writes"][0]
            reg_of[dst] = "rdx"
            continue
        if kind == "store":
            reads = list(step["reads"])
            if reads:
                src = reads[0]
                cur = reg_of.get(src)
                if cur is None:
                    cur = contract_fallback(src)
                    if cur is not None:
                        reg_of[src] = cur
                if cur is None:
                    raise Erasure("erasure_refused: value %s is read "
                                  "before it is defined or before the "
                                  "unit's entry contract names it"
                                  % src)
                src_text = loc_text(cur, 1)
                text.append("%s %s,%s" % (step["mnem"], src_text,
                                          step["dest_text"]))
            else:
                text.append("%s %s" % (step["mnem"], step["dest_text"]))
            continue
        if kind == "divmul":
            lo, hi, divisor = step["reads"]
            # EDIT 5 (the dividend halves arrive at the divisor's
            # own width, not always 32 bits).
            dwidth = step.get("divisor_width", 1)
            ensure(lo, "rax", dwidth)
            ensure(hi, "rdx", dwidth)
            if reg_of.get(divisor) in ("rax", "rdx"):
                raise Erasure("erasure_refused: the divisor value would "
                              "have to share %rax/%rdx with the "
                              "dividend -- not attempted this slice")
            divisor_loc = reg_of.get(divisor)
            if divisor_loc is None:
                raise Erasure("erasure_refused: divisor value has no "
                              "known register")
            text.append("%s %s" % (step["mnem"], loc_text(divisor_loc,
                                                           dwidth)))
            q, r = step["writes"]
            reg_of[q] = "rax"
            reg_of[r] = "rdx"
            continue
        # generic
        operands = step["operand_texts"]
        role = step["role"]
        slot_names = step["slot_names"]
        writes = step["writes"]
        if step.get("pin_cl") is not None:
            ensure(step["pin_cl"], "rcx", 1)
        write_slot = None
        write_name = None
        write_kind = None
        write_vec = False
        if writes:
            write_slot, write_name, write_kind, write_vec = writes[0]
        for slot, operand in enumerate(operands):
            if role[slot] not in ("use", "rw"):
                continue
            name = slot_names[slot]
            if name is None or not canon.is_plain_register(operand):
                continue
            regname = canon.registers_in(operand)[0]
            fam = FAMILY_OF.get(regname)
            if fam is None:
                continue
            wanted_vec = canon.is_vector(fam)
            cur = reg_of.get(name)
            if cur is None or is_mem(cur):
                continue
            if canon.is_vector(cur) == wanted_vec:
                continue
            is_final_write = (slot == write_slot and role[slot] == "rw"
                              and (name == final_name
                                   or name == "answer"))
            if is_final_write:
                target = contract["result"]
            else:
                target = loc_for(name, wanted_vec)
                if is_mem(target):
                    # a file-crossing value cannot be spilled to plain
                    # memory mid-instruction (it needs a real vector or
                    # GP register to bit-reinterpret through) -- refuse
                    # this specific, rare case by name rather than emit
                    # something that will not assemble.
                    raise Erasure("erasure_refused: a file-crossing "
                                  "value overflowed to a stack home -- "
                                  "not attempted this slice")
            ensure(name, target, 0)
        if write_kind == "rw":
            old_name = slot_names[write_slot]
            is_final = (write_name == final_name or write_name == "answer")
            if is_final:
                target = contract["result"]
            else:
                target = reg_of.get(old_name)
                if target is None:
                    target = contract_fallback(old_name)
                    if target is not None:
                        reg_of[old_name] = target
                if target is None and (step["mnem"] in ("sbb", "sbc")
                                       or step["mnem"].startswith("set")):
                    # canon4 fix (in-place-no-known-register cause):
                    # two idioms the erasure engine tags "rw" (it reads
                    # AT&T's single-operand-with-implicit-dest form)
                    # that are actually pure writes of flag state --
                    # `sbb reg,reg` (0 or -1 from the carry flag) and
                    # every `setCC reg8` (0 or 1 from the flags) --
                    # neither ever reads the register's prior bits, so
                    # "old_name" never needed a home.  Give it a fresh
                    # one, exactly as a `def` would.
                    target = loc_for(old_name, write_vec)
                    reg_of[old_name] = target
            if target is None:
                raise Erasure("erasure_refused: an in-place value has "
                              "no known register")
            if is_final:
                ensure(old_name, target, 1)
            else:
                target, preserve_lines = preserve_if_live(
                    text, steps, step_index, old_name, write_name,
                    target, write_vec, bench)
                for preserve_line in preserve_lines:
                    text.append(preserve_line)
            reg_of[write_name] = target
        elif write_kind == "def":
            is_final = (write_name == final_name or write_name == "answer")
            if is_final:
                target = contract["result"]
            else:
                target = loc_for(write_name, write_vec)
            reg_of[write_name] = target
        write_fam = None
        if write_slot is not None and canon.is_plain_register(
                operands[write_slot]):
            write_fam = FAMILY_OF.get(
                canon.registers_in(operands[write_slot])[0])
        pieces = []
        for slot, operand in enumerate(operands):
            name = slot_names[slot]
            if name is None:
                if (canon.is_plain_register(operand)
                        and FAMILY_OF.get(canon.registers_in(operand)[0])
                        == write_fam and write_fam is not None):
                    regname = canon.registers_in(operand)[0]
                    width = WIDTH_OF.get(regname, 1)
                    pieces.append(loc_text(reg_of[write_name], width))
                    continue
                pieces.append(operand)
                continue
            width = WIDTH_OF.get(canon.registers_in(operand)[0], 1)
            if slot == write_slot:
                target_loc = reg_of[write_name]
            else:
                target_loc = reg_of.get(name)
                if target_loc is None:
                    target_loc = contract_fallback(name)
                    if target_loc is not None:
                        reg_of[name] = target_loc
                if target_loc is None:
                    raise Erasure("erasure_refused: value %s used "
                                  "before it is defined" % name)
            pieces.append(loc_text(target_loc, width))
        # THE ONE EDIT (park-reload).  canon4.py raised
        # "two stack-spilled operands in one instruction" here, then
        # emitted the instruction.  The replacement counts MEMORY
        # pieces (not merely non-register pieces) and resolves a
        # genuine pair with the park-reload idiom, which can put lines
        # both before and after the instruction.  See this file's
        # header.
        pieces, before_lines, after_lines = park_reload(
            step, pieces, operands, role, write_slot, write_kind,
            bench, report)
        for parked_line in before_lines:
            text.append(parked_line)
        if pieces:
            text.append("%s %s" % (step["mnem"], ",".join(pieces)))
        else:
            text.append(step["mnem"])
        for parked_line in after_lines:
            text.append(parked_line)
    if final_name is not None:
        # canon4 fix (passthrough cause): a unit that just returns its
        # argument untouched has final_name == "a" (or "b") and never
        # ran a step that would have put it in reg_of -- ensure()'s
        # contract_fallback now seeds it from the entry contract itself,
        # so this becomes the honest "mov home->rax (or nothing) + ret"
        # rather than a refusal.
        if final_name not in reg_of and contract_fallback(final_name) \
                is None:
            raise Erasure("erasure_refused: the answer value never "
                          "entered a tracked register (a passthrough "
                          "this builder does not model)")
        # EDIT 3 (the answer move's width).  canon4.py landed the
        # finished value in the answer register with a 32-BIT move,
        # always.  A 64-bit answer is truncated by that move; the unit
        # then computes the right value and returns the wrong one.
        # See parkload_derive.py's header, CAUSE 3.
        ensure(final_name, contract["result"], 0)
    text.append("ret")
    return text


# --------------------------------------------------------- straight line


def derive_block_body33(steps, contract, bench, reg_of_in,
                        report):
    """derive_runnable3, restricted to ONE block's steps (no trailing
    `ret` -- the branching driver's render_control_line() appends the
    real control instruction separately) and threading `reg_of` in and
    back out so the next block along this path starts where this one
    left off."""
    reg_of = dict(reg_of_in)
    text = []

    def contract_fallback(name):
        if name == "a" and contract.get("a") is not None:
            return contract["a"]
        if name == "b" and contract.get("b") is not None:
            return contract["b"]
        return None

    def ensure(name, target, width):
        cur = reg_of.get(name)
        if cur is None:
            cur = contract_fallback(name)
            if cur is not None:
                reg_of[name] = cur
        if cur is None:
            raise Erasure("erasure_refused: value %s is read before it "
                          "is defined or before the unit's entry "
                          "contract names it" % name)
        if cur == target:
            return
        if is_mem(cur):
            text.append("mov %s,%%%s" % (cur[1], render(target, width)))
            reg_of[name] = target
            return
        cur_vec = canon.is_vector(cur)
        target_vec = canon.is_vector(target)
        if cur_vec and target_vec:
            mnem = "movaps"
        elif cur_vec != target_vec:
            mnem = "movq"
        else:
            mnem = "mov"
        text.append("%s %%%s,%%%s" % (mnem, render(cur, width),
                                      render(target, width)))
        reg_of[name] = target

    def loc_for(name, is_vec):
        return bench.location_for(name, is_vec)

    for step_index, step in enumerate(steps):
        kind = step["kind"]
        if kind == "sign_extend":
            src = step["reads"][0]
            # EDIT 5 (the dividend arrives at its own width).
            ensure(src, "rax", sign_extend_width(step["mnem"]))
            text.append(step["mnem"])
            dst = step["writes"][0]
            reg_of[dst] = "rdx"
            continue
        if kind == "store":
            reads = list(step["reads"])
            if reads:
                src = reads[0]
                cur = reg_of.get(src)
                if cur is None:
                    cur = contract_fallback(src)
                    if cur is not None:
                        reg_of[src] = cur
                if cur is None:
                    raise Erasure("erasure_refused: value %s is read "
                                  "before it is defined or before the "
                                  "unit's entry contract names it"
                                  % src)
                text.append("%s %s,%s" % (step["mnem"], loc_text(cur, 1),
                                          step["dest_text"]))
            else:
                text.append("%s %s" % (step["mnem"], step["dest_text"]))
            continue
        if kind == "divmul":
            lo, hi, divisor = step["reads"]
            # EDIT 5 (the dividend halves arrive at the divisor's
            # own width, not always 32 bits).
            dwidth = step.get("divisor_width", 1)
            ensure(lo, "rax", dwidth)
            ensure(hi, "rdx", dwidth)
            if reg_of.get(divisor) in ("rax", "rdx"):
                raise Erasure("erasure_refused: the divisor value would "
                              "have to share %rax/%rdx with the "
                              "dividend -- not attempted this slice")
            divisor_loc = reg_of.get(divisor)
            if divisor_loc is None:
                raise Erasure("erasure_refused: divisor value has no "
                              "known register")
            text.append("%s %s" % (step["mnem"], loc_text(divisor_loc,
                                                           dwidth)))
            q, r = step["writes"]
            reg_of[q] = "rax"
            reg_of[r] = "rdx"
            continue
        operands = step["operand_texts"]
        role = step["role"]
        slot_names = step["slot_names"]
        writes = step["writes"]
        if step.get("pin_cl") is not None:
            ensure(step["pin_cl"], "rcx", 1)
        write_slot = None
        write_name = None
        write_kind = None
        write_vec = False
        if writes:
            write_slot, write_name, write_kind, write_vec = writes[0]
        for slot, operand in enumerate(operands):
            if role[slot] not in ("use", "rw"):
                continue
            name = slot_names[slot]
            if name is None or not canon.is_plain_register(operand):
                continue
            regname = canon.registers_in(operand)[0]
            fam = FAMILY_OF.get(regname)
            if fam is None:
                continue
            wanted_vec = canon.is_vector(fam)
            cur = reg_of.get(name)
            if cur is None or is_mem(cur):
                continue
            if canon.is_vector(cur) == wanted_vec:
                continue
            target = loc_for(name, wanted_vec)
            if is_mem(target):
                raise Erasure("erasure_refused: a file-crossing value "
                              "overflowed to a stack home -- not "
                              "attempted this slice")
            ensure(name, target, 0)
        if write_kind == "rw":
            old_name = slot_names[write_slot]
            target = reg_of.get(old_name)
            if target is None:
                target = contract_fallback(old_name)
                if target is not None:
                    reg_of[old_name] = target
            if target is None and (step["mnem"] in ("sbb", "sbc")
                                   or step["mnem"].startswith("set")):
                # canon4 fix (in-place-no-known-register cause) -- see
                # derive_runnable3 for why this is sound: neither idiom
                # ever reads old_name's prior bits.
                target = loc_for(old_name, write_vec)
                reg_of[old_name] = target
            if target is None:
                raise Erasure("erasure_refused: an in-place value has "
                              "no known register")
            target, preserve_lines = preserve_if_live(
                text, steps, step_index, old_name, write_name, target,
                write_vec, bench)
            for preserve_line in preserve_lines:
                text.append(preserve_line)
            reg_of[write_name] = target
        elif write_kind == "def":
            target = loc_for(write_name, write_vec)
            reg_of[write_name] = target
        write_fam = None
        if write_slot is not None and canon.is_plain_register(
                operands[write_slot]):
            write_fam = FAMILY_OF.get(
                canon.registers_in(operands[write_slot])[0])
        pieces = []
        for slot, operand in enumerate(operands):
            name = slot_names[slot]
            if name is None:
                if (canon.is_plain_register(operand)
                        and FAMILY_OF.get(canon.registers_in(operand)[0])
                        == write_fam and write_fam is not None):
                    regname = canon.registers_in(operand)[0]
                    width = WIDTH_OF.get(regname, 1)
                    pieces.append(loc_text(reg_of[write_name], width))
                    continue
                pieces.append(operand)
                continue
            width = WIDTH_OF.get(canon.registers_in(operand)[0], 1)
            if slot == write_slot:
                target_loc = reg_of[write_name]
            else:
                target_loc = reg_of.get(name)
                if target_loc is None:
                    target_loc = contract_fallback(name)
                    if target_loc is not None:
                        reg_of[name] = target_loc
                if target_loc is None:
                    raise Erasure("erasure_refused: value %s used "
                                  "before it is defined" % name)
            pieces.append(loc_text(target_loc, width))
        # THE ONE EDIT (park-reload).  canon4.py raised
        # "two stack-spilled operands in one instruction" here, then
        # emitted the instruction.  The replacement counts MEMORY
        # pieces (not merely non-register pieces) and resolves a
        # genuine pair with the park-reload idiom, which can put lines
        # both before and after the instruction.  See this file's
        # header.
        pieces, before_lines, after_lines = park_reload(
            step, pieces, operands, role, write_slot, write_kind,
            bench, report)
        for parked_line in before_lines:
            text.append(parked_line)
        if pieces:
            text.append("%s %s" % (step["mnem"], ",".join(pieces)))
        else:
            text.append(step["mnem"])
        for parked_line in after_lines:
            text.append(parked_line)
    return text, reg_of


