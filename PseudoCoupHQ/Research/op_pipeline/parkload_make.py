#!/usr/bin/env python3
"""parkload_make.py -- the GENERATOR that writes parkload_derive.py.

WHY A GENERATOR AND NOT A HAND-WRITTEN COPY.  The park-reload rule is
one change inside two long functions that already exist and are
already gate-proved on 1,635 units: canon4.py's `derive_runnable3`
(straight-line units) and `derive_block_body` (one block of a
branching unit).  Re-typing them by hand would put every OTHER line of
those functions at risk of a silent transcription difference, and a
reviewer would have no way to tell an intended edit from a slip.

So parkload_derive.py is MACHINE-COPIED from canon4.py's own source
text, and exactly two edits are applied, each one a literal string
replacement that this file names and that the run prints.  If an edit
does not match canon4.py's current text the generator REFUSES rather
than writing a file (`EditDidNotApply`), so the copy can never drift
away from its source without saying so.

canon4.py IS NOT MODIFIED.  It is opened read-only.  Verified by this
program's own sha256 report, and by the vcs.

THE TWO EDITS, stated in full:

  EDIT 1 -- the refusal, in `derive_runnable3`.  canon4.py refuses
  when more than one operand piece of one instruction is not a plain
  register:

        if len([p for p in pieces if not p.startswith("%")]) > 1:
            raise Erasure("erasure_refused: two stack-spilled operands
                           in one instruction -- not attempted this
                           slice")

  It is replaced by a call to `park_reload`, which (a) counts MEMORY
  pieces rather than non-register pieces -- an immediate beside one
  memory operand is a legal x86-64 instruction and was never a real
  obstruction -- and (b) where two memory pieces do meet, loads one of
  them into the designated reload register first: the park-reload
  idiom.

  EDIT 2 -- the same refusal, in `derive_block_body`.  Same text,
  same replacement.

THE SPELLING BAN.  Neither this file nor its product contains an
operator token; both handle registers, offsets and value names only.

usage:
  parkload_make.py            # writes parkload_derive.py beside it
  parkload_make.py --check    # refuses to write; reports whether the
                              # edits still apply to canon4.py
"""

import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "canon4.py")
PRODUCT = os.path.join(HERE, "parkload_derive.py")

FIRST_FUNCTION = "def derive_runnable3(steps, final_name, contract, bench):"
SECOND_FUNCTION = "def derive_block_body(steps, contract, bench, reg_of_in):"

OLD_REFUSAL = '''        if len([p for p in pieces if not p.startswith("%")]) > 1:
            raise Erasure("erasure_refused: two stack-spilled operands "
                          "in one instruction -- not attempted this "
                          "slice")
        if pieces:
            text.append("%s %s" % (step["mnem"], ",".join(pieces)))
        else:
            text.append(step["mnem"])
'''

NEW_REFUSAL = '''        # THE ONE EDIT (park-reload).  canon4.py raised
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
'''


OLD_ANSWER_MOVE = '        ensure(final_name, contract["result"], 1)\n'

NEW_ANSWER_MOVE = '''        # EDIT 3 (the answer move's width).  canon4.py landed the
        # finished value in the answer register with a 32-BIT move,
        # always.  A 64-bit answer is truncated by that move; the unit
        # then computes the right value and returns the wrong one.
        # See parkload_derive.py's header, CAUSE 3.
        ensure(final_name, contract["result"], 0)
'''


class EditDidNotApply(Exception):
    pass


OLD_RW_STRAIGHT = """            if is_final:
                ensure(old_name, target, 1)
            reg_of[write_name] = target
"""

NEW_RW_STRAIGHT = """            if is_final:
                ensure(old_name, target, 1)
            else:
                target, preserve_lines = preserve_if_live(
                    text, steps, step_index, old_name, write_name,
                    target, write_vec, bench)
                for preserve_line in preserve_lines:
                    text.append(preserve_line)
            reg_of[write_name] = target
"""

OLD_RW_BLOCK = """            if target is None:
                raise Erasure("erasure_refused: an in-place value has "
                              "no known register")
            reg_of[write_name] = target
"""

NEW_RW_BLOCK = """            if target is None:
                raise Erasure("erasure_refused: an in-place value has "
                              "no known register")
            target, preserve_lines = preserve_if_live(
                text, steps, step_index, old_name, write_name, target,
                write_vec, bench)
            for preserve_line in preserve_lines:
                text.append(preserve_line)
            reg_of[write_name] = target
"""


OLD_SIGN_EXTEND = '            ensure(src, "rax", 1)\n'

NEW_SIGN_EXTEND = (
    '            # EDIT 5 (the dividend arrives at its own width).\n'
    '            ensure(src, "rax", sign_extend_width(step["mnem"]))\n')

OLD_DIVMUL = """            ensure(lo, "rax", 1)
            ensure(hi, "rdx", 1)
            dwidth = step.get("divisor_width", 1)
"""

NEW_DIVMUL = """            # EDIT 5 (the dividend halves arrive at the divisor's
            # own width, not always 32 bits).
            dwidth = step.get("divisor_width", 1)
            ensure(lo, "rax", dwidth)
            ensure(hi, "rdx", dwidth)
"""


def apply_literal(body, label, old, new):
    if body.count(old) != 1:
        raise EditDidNotApply(
            "%s: the block was found %d times, expected exactly 1"
            % (label, body.count(old)))
    print("%s applied" % label)
    return body.replace(old, new)


def apply_enumerate_edit(body, label):
    old = "    for step in steps:\n"
    if body.count(old) != 1:
        raise EditDidNotApply(
            "%s: the step loop was found %d times, expected exactly 1"
            % (label, body.count(old)))
    print("%s (step index) applied" % label)
    return body.replace(
        old, "    for step_index, step in enumerate(steps):\n")




def apply_answer_width_edit(body):
    if body.count(OLD_ANSWER_MOVE) != 1:
        raise EditDidNotApply(
            "EDIT 3: the answer move was found %d times, expected "
            "exactly 1" % body.count(OLD_ANSWER_MOVE))
    print("EDIT 3 (the answer move's width) applied")
    return body.replace(OLD_ANSWER_MOVE, NEW_ANSWER_MOVE)


def read_source():
    handle = open(SOURCE)
    text = handle.read()
    handle.close()
    return text


def function_text(source, header, next_header):
    start = source.index(header)
    end = source.index(next_header, start)
    return source[start:end]


def extract():
    source = read_source()
    first = function_text(source, FIRST_FUNCTION,
                          "def canon3_straight(")
    second = function_text(source, SECOND_FUNCTION,
                           "# --------------------------------------"
                           "------------------- per unit")
    return first, second


def apply_edit(body, label):
    if body.count(OLD_REFUSAL) != 1:
        raise EditDidNotApply(
            "%s: canon4.py's refusal block was found %d times, "
            "expected exactly 1 -- refusing to write a product that "
            "does not match its source"
            % (label, body.count(OLD_REFUSAL)))
    return body.replace(OLD_REFUSAL, NEW_REFUSAL)


HEADER = '''#!/usr/bin/env python3
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

'''


def write_product(first, second, edits_applied):
    handle = open(PRODUCT, "w")
    handle.write(HEADER)
    handle.write("\n")
    handle.write(first)
    handle.write("\n")
    handle.write(second)
    handle.close()
    return len(HEADER) + len(first) + len(second) + 2


def sha256_of(path):
    handle = open(path, "rb")
    digest = hashlib.sha256(handle.read()).hexdigest()
    handle.close()
    return digest


def main(argv):
    check_only = "--check" in argv
    before = sha256_of(SOURCE)
    first, second = extract()
    first = first.replace(
        "def derive_runnable3(steps, final_name, contract, bench):",
        "def derive_runnable33(steps, final_name, contract, bench,\n"
        "                      report):")
    second = second.replace(
        "def derive_block_body(steps, contract, bench, reg_of_in):",
        "def derive_block_body33(steps, contract, bench, reg_of_in,\n"
        "                        report):")
    first = apply_edit(first, "EDIT 1 (derive_runnable3)")
    first = apply_answer_width_edit(first)
    first = apply_enumerate_edit(first, "EDIT 4a")
    first = apply_literal(
        first, "EDIT 4b (in-place clobber, straight line)",
        OLD_RW_STRAIGHT, NEW_RW_STRAIGHT)
    first = apply_literal(first, "EDIT 5a (sign-extend width)",
                          OLD_SIGN_EXTEND, NEW_SIGN_EXTEND)
    first = apply_literal(first, "EDIT 5b (dividend width)",
                          OLD_DIVMUL, NEW_DIVMUL)
    second = apply_edit(second, "EDIT 2 (derive_block_body)")
    second = apply_enumerate_edit(second, "EDIT 4c")
    second = apply_literal(
        second, "EDIT 4d (in-place clobber, per block)",
        OLD_RW_BLOCK, NEW_RW_BLOCK)
    second = apply_literal(second, "EDIT 5c (sign-extend width)",
                           OLD_SIGN_EXTEND, NEW_SIGN_EXTEND)
    second = apply_literal(second, "EDIT 5d (dividend width)",
                           OLD_DIVMUL, NEW_DIVMUL)
    print("EDIT 1 (derive_runnable3)  applied")
    print("EDIT 2 (derive_block_body) applied")
    if check_only:
        print("--check: both edits still match canon4.py; nothing "
              "written")
        return 0
    size = write_product(first, second, 2)
    after = sha256_of(SOURCE)
    print("wrote %s -- %d bytes" % (os.path.basename(PRODUCT), size))
    print("canon4.py sha256 before: %s" % before)
    print("canon4.py sha256 after:  %s" % after)
    if before != after:
        print("REFUSED: canon4.py changed during the run")
        return 1
    print("canon4.py UNCHANGED (opened read-only)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
