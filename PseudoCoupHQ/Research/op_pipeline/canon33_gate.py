#!/usr/bin/env python3
"""canon33_gate.py -- the gate, extended for designated locations.

Four table gaps, each fixed here in a SUBCLASS or in a text
transform applied identically to both sides, with
canon10_behaviour_check.py and everything below it imported and
UNCHANGED.  AgentMemory's standing instruction for exactly this
situation: "The lifter was measured NOT to be the limiting factor ...
the limit was our own name->z3 translation table. Fix tables, not
tools."

GAP 1 -- DESIGNATED LOCATIONS ARE NOT MODELLED.  Sim10 reads and
writes register families only; a designated location
(`-0x8(%rsp)`, designated_memory.py) reaches
`width_of_operand` and is refused as an unknown register spelling.
Sim33 adds a slot store.  It is EXACT, not uninterpreted: a slot is a
64-bit value written by a store and read back by a load, keyed by the
slot's own text.

  The model is sound because of a property the RENDERER guarantees,
  not because of an assumption: parkload_derive.py emits a designated
  location in exactly two shapes, `mov <reg>,<slot>` and
  `mov <slot>,<reg>` (with `movd`/`movq` for the vector file).  No
  other instruction ever names a slot.  So there is no aliasing
  question to answer: two different slot texts are two different
  8-byte homes, and nothing else in the text can reach them.  Sim33
  REFUSES BY NAME (`NotModeled`) if a slot appears anywhere else.

  A slot read before it is written takes a shared symbolic seed keyed
  by the slot text, exactly as an unwritten register family does, so
  both texts being compared start from the same unconstrained value.

GAP 2 -- `lea` WITH A DISPLACEMENT.  canon5's Sim models only the
plain `(base,index,scale)` form and refuses `-0x41(%rsi)` by name.
The displacement form is ordinary exact arithmetic
(`base + index*scale + displacement`); it is modelled here.  Nothing
about it is approximate.

GAP 3 -- THE RIP GUARD IS WIDER THAN ITS OWN ARGUMENT.  The guard
refuses whenever the ordered list of rip-relative-operand mnemonics
differs between the two texts, because positional keying of constants
would otherwise be unsound.  A path-duplicating canonical text can
render one trap block twice, which changes that list without changing
any constant.  The NARROWED guard drops the lines whose constant is
never read as data by this checker:

  * a `call` through a rip-relative operand -- the walker raises Trap
    on every `call`, so no value from it reaches an answer;
  * a `lea <rip>,<reg>` IMMEDIATELY FOLLOWED by a `call` -- the
    address is the trapping call's own argument.

GAP 4 -- THE TRAPPING CALL'S ARGUMENT.  `neutralize_trap_arguments`
below; its soundness argument is in its own docstring.

Everything else is still compared, in order, exactly as before.
canon33_controls.py exercises this narrowing in both directions: a
text differing only by a duplicated trap path is accepted, and a text
whose non-trap rip constants differ is still refused.

THE SPELLING BAN.  No operator token appears in this file.
"""

import os
import sys

import z3

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon  # noqa: E402
import canon5_behaviour_check as BC5  # noqa: E402
import canon8_behaviour_check as BC8  # noqa: E402
import canon10_behaviour_check as BC10  # noqa: E402
import designated_memory as DM  # noqa: E402
import real_blocks  # noqa: E402

NotModeled = BC5.NotModeled
Trap = BC10.Trap
split_operands = BC5.split_operands

SLOT_MNEMONICS = ("mov", "movd", "movq")


def is_slot_text(text):
    if not text.endswith("(%rsp)"):
        return False
    return text.startswith("-0x")


class Sim33(BC10.Sim10):
    """Sim10 plus the designated-location store and the displacement
    `lea` form.  Nothing else differs."""

    def __init__(self, shared_seed, tag):
        BC10.Sim10.__init__(self, shared_seed, tag)
        self.slots = {}

    def slot_value(self, slot_text, width):
        if slot_text in self.slots:
            value, stored_width = self.slots[slot_text]
            if stored_width != width:
                raise NotModeled(
                    "designated location %s was parked at %d bits and "
                    "is read back at %d -- a width-mixing form this "
                    "checker does not model"
                    % (slot_text, stored_width, width))
            return value
        key = "slot_%s" % slot_text
        if key not in self.shared_seed:
            self.shared_seed[key] = z3.BitVec(key, 64)
        return z3.Extract(width - 1, 0, self.shared_seed[key])

    def exec_line(self, line):
        text = line.strip()
        if "!!" in text:
            text = text.split("!!", 1)[0].strip()
        parts = text.split(" ", 1)
        mnemonic = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        operands = split_operands(rest)
        if mnemonic == "lea" and operands:
            # A `lea` READS NO MEMORY -- its memory-shaped operand is
            # an address computation.  So it is handled before the
            # slot check, and a stack-relative operand inside a `lea`
            # is never mistaken for a designated location.  (Measured:
            # six own-frame units, c/op_31 c/op_32 c/op_35 and
            # cpp/op_43 cpp/op_44 cpp/op_47, were refused by name for
            # exactly that mistake.)
            handled = self.try_displacement_lea(operands)
            if handled:
                return
        touching = []
        for operand in operands:
            if is_slot_text(operand):
                touching.append(operand)
        if not touching:
            return BC10.Sim10.exec_line(self, line)
        if mnemonic not in SLOT_MNEMONICS:
            raise NotModeled(
                "a designated location appears as an operand of %r, "
                "which is outside the two shapes the renderer emits "
                "(a load into a register and a store from one)"
                % mnemonic)
        if len(operands) != 2:
            raise NotModeled(
                "a designated location appears in a %r with %d "
                "operands" % (mnemonic, len(operands)))
        source, destination = operands
        if len(touching) == 2:
            raise NotModeled(
                "both operands of %r are designated locations, which "
                "x86-64 does not encode and the renderer never emits"
                % mnemonic)
        if is_slot_text(destination):
            width = self.width_of_operand(source)
            value = self.read_at(source, width)
            self.slots[destination] = (value, width)
            return
        width = self.width_of_operand(destination)
        value = self.slot_value(source, width)
        self.write(destination, value)
        return

    def try_displacement_lea(self, operands):
        """the displacement forms of `lea`.  Returns True when it
        handled the line, False to let the base class see it."""
        if len(operands) != 2:
            return False
        source, destination = operands
        parsed = parse_address(source)
        if parsed is None:
            return False
        base, index, scale, displacement = parsed
        if displacement == 0 and index is not None:
            return False
        total = None
        if base is not None:
            total = self.get_family(canon.FAMILY_OF[base[1:]])
        if index is not None:
            index_value = self.get_family(canon.FAMILY_OF[index[1:]])
            term = index_value * scale
            total = term if total is None else total + term
        if total is None:
            return False
        total = total + z3.BitVecVal(displacement, 64)
        width = self.width_of_operand(destination)
        self.write(destination, z3.Extract(width - 1, 0, total))
        return True


def parse_address(text):
    """(base, index, scale, displacement) for the AT&T memory forms
    this checker models, or None.  Only fully explicit forms are
    accepted; anything else returns None so the caller refuses by
    name rather than guessing."""
    if not text.endswith(")"):
        return None
    head, _, tail = text.partition("(")
    inner = tail[:-1]
    displacement = 0
    if head != "":
        try:
            displacement = int(head, 0)
        except ValueError:
            return None
    fields = inner.split(",")
    base = None
    index = None
    scale = 1
    if len(fields) == 1:
        base = fields[0].strip()
    elif len(fields) == 3:
        base = fields[0].strip()
        index = fields[1].strip()
        try:
            scale = int(fields[2].strip(), 0)
        except ValueError:
            return None
    else:
        return None
    if base == "":
        base = None
    if index == "":
        index = None
    for register in (base, index):
        if register is None:
            continue
        if not register.startswith("%"):
            return None
        if canon.FAMILY_OF.get(register[1:]) is None:
            return None
    if base is None and index is None:
        return None
    return base, index, scale, displacement


# ------------------------------------------------------ the rip guard

def rip_order_data_only(lines):
    """canon10's rip_mnemonic_order, narrowed to the lines whose
    rip-relative operand can actually reach an answer -- see GAP 3 in
    this file's header."""
    cleaned = []
    for raw in lines:
        line = raw.strip()
        if "!!" in line:
            line = line.split("!!", 1)[0].strip()
        if line == "":
            continue
        if line.endswith(":"):
            continue
        cleaned.append(line)
    out = []
    for position, line in enumerate(cleaned):
        if "(%rip)" not in line:
            continue
        mnemonic = line.split(" ", 1)[0]
        if mnemonic == "call":
            continue
        if mnemonic == "lea":
            following = ""
            if position + 1 < len(cleaned):
                following = cleaned[position + 1].split(" ", 1)[0]
            if following == "call":
                continue
        out.append(mnemonic)
    return out


# ------------------------------------------- the trapping-call argument

def neutralize_trap_arguments(block_list):
    """rewrite `lea <rip-relative>,<register>` when the VERY NEXT line
    of the same block is a `call`, to `mov $0x0,<register>`.

    WHY THIS IS SOUND, and not a convenience.  The walker raises Trap
    on every `call`, so execution of that block stops at the next
    line and the register just written is never read by anything.  Any
    value at all may be written there without changing a single
    answer.  The rewrite is applied IDENTICALLY to the real text and
    to the candidate, so it cannot make two texts agree that would
    otherwise disagree anywhere the answer can see.

    WHAT IT BUYS.  These lines are the address of a panic message --
    the argument of the call that traps.  Without the rewrite the
    checker refuses the whole unit by name ("lea addressing form
    '0x0(%rip)' is not the plain (base,index,scale) shape"), which is
    an honest refusal about a value that provably cannot matter.
    """
    out = []
    for block in block_list:
        steps = list(block["steps"])
        for index, raw in enumerate(steps):
            line = raw.strip()
            if "!!" in line:
                line = line.split("!!", 1)[0].strip()
            if not line.startswith("lea "):
                continue
            if "(%rip)" not in line:
                continue
            if index + 1 >= len(steps):
                continue
            following = steps[index + 1].strip()
            if not following.startswith("call"):
                continue
            operands = split_operands(line.split(" ", 1)[1])
            if len(operands) != 2:
                continue
            if not operands[1].startswith("%"):
                continue
            steps[index] = "mov $0x0,%s" % operands[1]
        copy = dict(block)
        copy["steps"] = steps
        out.append(copy)
    return out


# ------------------------------------------------------- the two gates

def check_straight(lang, n, canon4_docs, sem_docs, candidate_text):
    real_text = BC8.real_text_of(lang, n, canon4_docs)
    if real_text is None:
        return "UNDECIDED", "no real ship mnem recorded for this unit"
    lines_real = [ln.strip() for ln in real_text.split(";")]
    lines_cand = [ln.strip() for ln in candidate_text.split(";")]
    order_real = rip_order_data_only(lines_real)
    order_cand = rip_order_data_only(lines_cand)
    if order_real != order_cand:
        return "UNDECIDED", "the narrowed rip-relative constant " \
            "guard refused: real text loads data constants at %r, " \
            "candidate at %r" % (order_real, order_cand)
    home, width = BC10.answer_home_from_real(lines_real)
    if home is None:
        return "UNDECIDED", "the unit's own real ship code never " \
            "writes %xmm0 or an rax-family register"
    shared_seed = BC10._prepare_seed(lang, n, sem_docs)
    sim_real = Sim33(shared_seed, "real")
    sim_cand = Sim33(shared_seed, "cand")
    for sim in (sim_real, sim_cand):
        sim.answer_family = home
        sim.answer_width = width
    try:
        val_real, w_real = sim_real.answer_value(lines_real)
        val_cand, w_cand = sim_cand.answer_value(lines_cand)
    except NotModeled as bad:
        return "UNDECIDED", str(bad)
    return BC10._finish(val_real, w_real, val_cand, w_cand, home, width)


def check_branching(lang, n, canon4_docs, op_docs, sem_docs):
    record = canon4_docs[lang].get(n)
    if record is None:
        return "UNDECIDED", "no canon4_units record for this unit"
    candidate_blocks = record.get("derived_blocks")
    if not candidate_blocks:
        return "UNDECIDED", "no derived_blocks candidate on this " \
            "unit's record"
    probe = op_docs[lang].get(n)
    if probe is None:
        return "UNDECIDED", "no op_units probe record for this unit"
    ship = probe.get("ship") or {}
    if not ship.get("bytes") or not ship.get("mnem"):
        return "UNDECIDED", "the op_units probe record carries no " \
            "ship bytes/mnem for this unit"
    try:
        real_block_list = real_blocks.build(ship["bytes"], ship["mnem"])
    except real_blocks.NotCuttable as bad:
        return "UNDECIDED", "real control-flow blocks could not be " \
            "cut from this unit's own ship bytes: %s" % bad
    real_block_list = neutralize_trap_arguments(real_block_list)
    candidate_blocks = neutralize_trap_arguments(candidate_blocks)
    lines_real = BC10.all_lines_of_blocks(real_block_list)
    lines_cand = BC10.all_lines_of_blocks(candidate_blocks)
    order_real = rip_order_data_only(lines_real)
    order_cand = rip_order_data_only(lines_cand)
    if order_real != order_cand:
        return "UNDECIDED", "the narrowed rip-relative constant " \
            "guard refused: real text loads data constants at %r, " \
            "candidate at %r" % (order_real, order_cand)
    home, width = BC10.answer_home_from_real(lines_real)
    if home is None:
        return "UNDECIDED", "the unit's own real ship code never " \
            "writes %xmm0 or an rax-family register"
    shared_seed = BC10._prepare_seed(lang, n, sem_docs)
    real_map = {}
    for block in real_block_list:
        real_map[block["label"]] = block["steps"]
    cand_map = {}
    for block in candidate_blocks:
        cand_map[block["label"]] = block["steps"]
    real_order = [b["label"] for b in real_block_list]
    cand_order = [b["label"] for b in candidate_blocks]
    sim_real = Sim33(shared_seed, "real")
    sim_cand = Sim33(shared_seed, "cand")
    for sim in (sim_real, sim_cand):
        sim.answer_family = home
        sim.answer_width = width
    try:
        val_real = BC10.walk(sim_real, real_map,
                             real_block_list[0]["label"],
                             order=real_order)
        val_cand = BC10.walk(sim_cand, cand_map,
                             candidate_blocks[0]["label"],
                             order=cand_order)
    except Trap:
        return "UNDECIDED", "both control-flow walks trapped " \
            "unconditionally -- no answer value on either side"
    except NotModeled as bad:
        return "UNDECIDED", str(bad)
    v_real, w_real = val_real
    v_cand, w_cand = val_cand
    return BC10._finish(v_real, w_real, v_cand, w_cand, home, width)
