#!/usr/bin/env python3
"""designated_memory.py -- MEMORY IS DESIGNATED, LIKE REGISTERS.

the owner's ruling, log_115 (2026-09-01): "the canonical form gains
designated LOCATIONS (standardized virtual slots with a directory:
which location holds which designation), alongside the designated
registers.  Runnable because slots are real stack offsets mapped at
run time."

THE SCHEME, stated completely, so a reader can rebuild it from this
header alone.

1.  THE DESIGNATIONS.  A designated location is named `S0`, `S1`,
    `S2`, ...  The name is a DESIGNATION, not an address -- exactly as
    `a` is a designation and `%rdi` is the register that designation
    is mapped to.  Designations are handed out in FIRST-NEEDED ORDER,
    the same order rule the temp-register pool already uses ("the
    order is what makes units match", canon7_render.py).

2.  THE DIRECTORY.  `Directory.directory()` returns the map
    designation -> slot record:

        "S0": {"slot_index": 0,
               "offset": -8,
               "text": "-0x8(%rsp)",
               "file": "general" | "vector",
               "holds": "u4"}

    `holds` is the erased-form value name that owns the designation
    for the whole unit.  A designation is assigned EXACTLY ONCE and
    never reassigned, which is the same rule the register bench
    already obeys.

3.  THE SLOTS ARE REAL STACK OFFSETS.  Slot `i` is at
    `-0x%x(%%rsp)` for 8*(i+1) -- `-0x8(%rsp)`, `-0x10(%rsp)`,
    `-0x18(%rsp)`, ...  This is the offset series canon3.py/canon4.py
    already overflow to; nothing about the addresses is new here.
    What is new is that they are NAMED and DIRECTORIED rather than
    being anonymous overflow.  Every slot is 8 bytes and 8-byte
    aligned, and the series grows downward from the stack pointer,
    so it lands inside the System V 128-byte red zone for the first
    16 slots -- which is why these units stay runnable with no
    prologue.  A unit needing a 17th slot is REFUSED BY NAME
    (`RedZoneExhausted`) rather than silently emitting text that
    would need a frame the canonical form does not carry.

4.  THE VALUE POOLS, and the registers held back.  Registers are
    still preferred over designated memory; memory is where a value
    goes when the register pool is spent.  The pool order is
    canon7_render.py's ratified order, with `%r10` and `%r11`
    REMOVED:

        general value pool: r9, r8, rbx, r12, r13, r14, r15
        vector  value pool: xmm2 .. xmm13

    `%r11`/`%r10` and `%xmm15`/`%xmm14` are RESERVED as the two
    designated reload registers per file (5).  Reserving them is a
    standardization choice, not a
    limit: AgentMemory's 2026-08-28 ruling ("TEMP REGISTERS ARE
    STANDARDIZED, NOT LIMITED") requires the SELECTION to be
    standardized so two units' texts can match, and a reload register
    that is sometimes %r11 and sometimes %r9 would defeat exactly
    that.

5.  THE RELOAD REGISTERS.  `%r11` (general) and `%xmm15` (vector)
    hold a value for the length of ONE instruction and are dead
    immediately after it.  They are never in the value pool, so no
    live value can occupy them, so the park-reload idiom
    (parkload_derive.py) can always use them without eviction.

WHAT THIS FILE DOES NOT DO.  It does not decide when a reload is
emitted -- that is parkload_derive.py's job.  It only owns the pools,
the designations, the slot addresses and the directory.

THE SPELLING BAN.  No operator token appears in this file at all: it
holds registers, offsets and value names only.  Any JSON a caller
builds from `directory()` carries designations and slot text, never a
token.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon  # noqa: E402  (is_vector, GP_NAMES)


# ------------------------------------------------------------ the pools

# canon7_render.py's ratified pool order, minus the two reserved
# reload registers.  Quoted from that file's header:
#   pool_order ["r10","r11","r9","r8","rbx","r12","r13","r14","r15"]
GENERAL_VALUE_POOL = ["r9", "r8", "rbx", "r12", "r13", "r14", "r15"]

# canon16_xmm.py's XMM_TEMP_POOL_ORDER is xmm2..xmm15; the top two are
# held back here for the same reason %r10/%r11 are.
VECTOR_VALUE_POOL = ["xmm%d" % i for i in range(2, 14)]

# TWO reload registers per file, not one.  One is enough for a source
# reload; an instruction whose DESTINATION is a designated location
# and whose source is another designated location needs two at once
# (measured on cpp/op_765 once the in-place-clobber guard raised that
# unit's register pressure).  Index 0 serves a destination re-park,
# index 1 a source reload, always in that order, so the selection is
# standardized.
GENERAL_RELOAD_REGISTERS = ["r11", "r10"]
VECTOR_RELOAD_REGISTERS = ["xmm15", "xmm14"]

# the System V red zone is 128 bytes below %rsp; 8-byte slots means 16
# of them fit.
RED_ZONE_SLOTS = 16


class RedZoneExhausted(Exception):
    pass


def slot_offset(slot_index):
    return -8 * (slot_index + 1)


def slot_text(slot_index):
    return "-0x%x(%%rsp)" % (8 * (slot_index + 1))


def designation_name(slot_index):
    return "S%d" % slot_index


def is_designated_location(loc):
    """a location is either a register family name (a string) or a
    designated location, which is the pair ("mem", <slot text>) --
    the same pair shape canon3.py/canon4.py already use, so a
    Directory can stand in for their Bench without any other change
    to the deriving code."""
    if not isinstance(loc, tuple):
        return False
    if len(loc) != 2:
        return False
    return loc[0] == "mem"


class Directory(object):
    """the canonical register/designated-location assignment for one
    unit.  Drop-in replacement for canon4.Bench: it answers the same
    `location_for(name, is_vec)` call and returns the same two shapes
    (a register family string, or ("mem", text)).  Two things are
    added: the pools are the ratified ORDER rather than a pair, and
    every memory assignment is recorded in a directory."""

    def __init__(self):
        self.general_bench = list(GENERAL_VALUE_POOL)
        self.vector_bench = list(VECTOR_VALUE_POOL)
        self.assigned = {}
        self.slots = []
        self.overflow_count = 0

    def location_for(self, name, is_vec):
        if name in self.assigned:
            return self.assigned[name]
        bench = self.vector_bench if is_vec else self.general_bench
        if bench:
            loc = bench.pop(0)
            self.assigned[name] = loc
            return loc
        return self._designate(name, is_vec)

    def _designate(self, name, is_vec):
        slot_index = len(self.slots)
        if slot_index >= RED_ZONE_SLOTS:
            raise RedZoneExhausted(
                "erasure_refused: this unit needs designated location "
                "S%d, which is below the System V red zone this "
                "canonical form relies on (%d slots)"
                % (slot_index, RED_ZONE_SLOTS))
        text = slot_text(slot_index)
        record = {}
        record["designation"] = designation_name(slot_index)
        record["slot_index"] = slot_index
        record["offset"] = slot_offset(slot_index)
        record["text"] = text
        record["file"] = "vector" if is_vec else "general"
        record["holds"] = name
        self.slots.append(record)
        self.overflow_count = self.overflow_count + 1
        loc = ("mem", text)
        self.assigned[name] = loc
        return loc

    def directory(self):
        out = {}
        for record in self.slots:
            out[record["designation"]] = dict(record)
        return out

    def register_map(self):
        out = {}
        for name in sorted(self.assigned):
            loc = self.assigned[name]
            if is_designated_location(loc):
                continue
            out[name] = loc
        return out

    def designation_of_text(self, text):
        for record in self.slots:
            if record["text"] == text:
                return record["designation"]
        return None


def reload_register(is_vec, index=0):
    if is_vec:
        return VECTOR_RELOAD_REGISTERS[index]
    return GENERAL_RELOAD_REGISTERS[index]


def reload_mnemonic(is_vec, width_index):
    """the instruction that brings a designated location's value into
    the reload register.  `width_index` is canon.py's own index into
    GP_NAMES (0 = 64-bit, 1 = 32-bit, 2 = 16-bit, 3 = 8-bit), which is
    what canon4.loc_text/render already pass around.  Within the
    general file a plain `mov` at the operand's own width; into the
    vector file `movd` at 32 bits and `movq` at 64 -- both real
    x86-64 loads that `as` accepts."""
    if not is_vec:
        return "mov"
    if width_index == 1:
        return "movd"
    return "movq"


def render_location(loc, width):
    """the AT&T text for a location at a register-name-table width
    index.  Identical in behaviour to canon4.loc_text/render, kept
    here so a caller can render a Directory location without importing
    the deriving module."""
    if is_designated_location(loc):
        return loc[1]
    if canon.is_vector(loc):
        return "%" + loc
    return "%" + canon.GP_NAMES[loc][width]
