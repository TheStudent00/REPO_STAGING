#!/usr/bin/env python3
"""canon2.py -- MOVES ARE ERASED BY SUBSTITUTION (the owner, 2026-08-26).

This is THIS SLICE's generator.  It reuses canon.py's parsing,
role model (use/def/rw per operand), and register tables, but
replaces canon.py's approach (rename the compiler's own registers in
place) with the ruled one: erase every pure move by substitution,
keep only genuine computation steps named over VALUES (a, b, answer,
u0, u1, ...), record the entry contract separately, and DERIVE
runnable text on demand by inserting adapter movs by rule.

Per unit this program tries to build four things:

  erased_form   -- the ordered list of computation steps left after
                   every pure register-to-register move has been
                   deleted and every downstream read of its
                   destination rewritten to the source value's name.
                   This is the canonical RECORD (AgentMemory's
                   ruling).  Steps never carry a physical register --
                   only value names.
  entry_contract -- where each value must arrive for the derivation
                   below: default a -> %rdi (%xmm0 float), b -> %rsi
                   (%xmm1 float), answer -> %rax (%xmm0 float); plus
                   any instruction-encoding pin the unit's own code
                   uses (cltd/cqto need the dividend in %rax; a shift
                   count needs %cl).
  derived_text  -- runnable AT&T text rebuilt from the erased form
                   under the default contract, inserting adapter
                   movs exactly where the contract demands them.
  roundtrip     -- `as` then `objdump -d` run for real on the
                   derived text, in this sandbox; the resulting bytes
                   are recorded.

Two cases canon.py refused are exactly what this slice is for:
  * a traced value pinned by cltd/cqto/idiv/div/mul/a shift count --
    the erased form does not tie a value to a register at all, so the
    "conflict" canon.py hit dissolves; derive_runnable inserts the
    adapter the pin needs.
  * an argument modified in place and returned (go's 48) -- the
    erasure treats the post-mutation value as a NEW name (the
    mutating instruction is a genuine computation, not a move), so
    "a" and "answer" are simply two different names that may share a
    physical register at derive time; derive_runnable adapts.

Branching units are SKIPPED outright with an honest per-unit record
`{"erasure": "deferred: branching"}` -- this program does not attempt
cross-block value naming.  canon.py's own `Walk` (imported, unmodified)
still supplies the branch detector and the per-instruction role list;
nothing about its role model is re-derived here.

THE SPELLING BAN.  No operator token participates in any key,
grouping, pairing or comparison scope here.  The token is copied once
per unit as the display label `operator`.  This file's OUTPUT ROOT
declares `"meta": {"role": "generator provenance"}` per
check_no_spelling_keys.py's generator-provenance exemption, because
every unit-shaped record here is itself provenance of one generator
run, not a matching/grouping artifact -- there are no `members`,
`pairs`, `rows`, `groups`, or `entries` at the top level, so the
exemption's own refusal condition does not apply.  Run
check_no_spelling_keys.py on the output; it must pass.

usage:
  canon2.py [--in DIR] [--out DIR] [--asm-lang c]
"""

import json
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon  # noqa: E402  (reuse parsing, register tables, Walk)

LANGS = ["c", "cpp", "go", "rust", "swift"]

FAMILY_OF = canon.FAMILY_OF
WIDTH_OF = canon.WIDTH_OF
NEVER_RENAME = canon.NEVER_RENAME
TEMPS = list(canon.TEMPS)
VECTOR_TEMPS = list(canon.VECTOR_TEMPS)

PURE_MOV_MNEMS = set([
    "mov", "movl", "movq", "movb", "movw",
])

DIVMUL_MNEMS = set([
    "idiv", "idivl", "idivq", "idivb",
    "div", "divl", "divq",
    "mul", "mull", "mulq",
])

SIGN_EXTEND_MNEMS = set(["cltd", "cqto"])

SHIFT_MNEMS = set([
    "shl", "shll", "shlq", "shr", "shrl", "shrq",
    "sar", "sarl", "sarq", "rol", "ror",
])


class Erasure(Exception):

    def __init__(self, reason):
        Exception.__init__(self, reason)
        self.reason = reason


def strip_reloc(line):
    """sem_anchored's mnem text sometimes carries a trailing objdump
    relocation annotation (`!!reloc=R_X86_64_PC32:...`) glued onto the
    last operand by a space, not a comma -- canon.py's own parse()
    tolerates it (the register regex still finds the register inside
    the garbage), but this program re-emits operand text verbatim into
    DERIVED, runnable AT&T, where the garbage would not assemble.  Cut
    it before parsing so the stored operand text is clean."""
    idx = line.find("!!")
    if idx >= 0:
        return line[:idx].rstrip()
    return line


# ------------------------------------------------------- erasure pass

class Erased(object):
    """the ordered computation-step record for one straight-line
    unit, plus the running family->value-name map used to build it.
    Values are named a / b / w<k> (an untraced incoming value the
    unit itself never defined) / u<k> (a computed temp) / answer
    (whichever value the calling rule hands back)."""

    def __init__(self, anchor, lines, role_log, result_family,
                 live=None, ctx=None):
        self.anchor = anchor
        self.lines = lines
        self.role_log = role_log
        self.result_family = result_family
        self.live = {} if live is None else live
        self.steps = []
        # `ctx` lets a branching unit share ONE numbering sequence
        # across all of its blocks (see BlockErased below) so u17 in
        # block 2 is never reused as a different value's name in
        # block 5.  A straight-line unit gets its own private counters.
        self.ctx = ctx if ctx is not None else {"u": 0, "w": 0, "k": 0}
        self.entry_pins = []
        self.mem_park = {}
        self.store_fate = {}
        self.consumed_reload = set()

    def new_u(self):
        name = "u%d" % self.ctx["u"]
        self.ctx["u"] = self.ctx["u"] + 1
        return name

    def new_w(self):
        name = "w%d" % self.ctx["w"]
        self.ctx["w"] = self.ctx["w"] + 1
        return name

    def new_k(self):
        name = "k%d" % self.ctx["k"]
        self.ctx["k"] = self.ctx["k"] + 1
        return name

    def occupant(self, fam):
        if fam in self.live:
            return self.live[fam]
        name = self.new_w()
        self.live[fam] = name
        return name

    def start(self):
        first = self.anchor.get("in0")
        second = self.anchor.get("in1")
        if first is not None and FAMILY_OF[first] not in self.live:
            self.live[FAMILY_OF[first]] = "a"
        if second is not None and FAMILY_OF[second] not in self.live:
            self.live[FAMILY_OF[second]] = "b"

    def run(self):
        self.start()
        self.precompute_store_fates()
        for index, line in enumerate(self.lines):
            self.one(index, line)
        final_name = self.live.get(self.result_family)
        return self.steps, final_name

    def precompute_store_fates(self):
        """REFUSAL CAUSE (b): a store to memory that is reloaded later
        (nothing else touching that slot in between) is a PARK -- the
        same bookkeeping as a register-to-register move, erased by
        substitution.  A store that is never reloaded before the unit
        ends (it is the unit's real output, taken by address, or the
        slot is simply dead) is kept as a genuine computation step.
        This is decided by lookahead over the whole unit, once, before
        the per-instruction walk, so `one()` can just look up the
        verdict for each index."""
        parsed = []
        for line in self.lines:
            parsed.append(canon.parse(strip_reloc(line)))
        for i, (mnem, operands) in enumerate(parsed):
            role = self.role_log.get(i)
            if role is None:
                continue
            for slot, operand in enumerate(operands):
                if slot >= len(role):
                    continue
                kind = role[slot]
                if kind not in ("def", "rw"):
                    continue
                if canon.is_plain_register(operand):
                    continue
                if "(%rip)" in operand:
                    continue
                addr_key = operand
                found = None
                for j in range(i + 1, len(parsed)):
                    mnem2, operands2 = parsed[j]
                    role2 = self.role_log.get(j)
                    if role2 is None:
                        break
                    rewritten = False
                    reload_slot = None
                    for slot2, operand2 in enumerate(operands2):
                        if slot2 >= len(role2):
                            continue
                        kind2 = role2[slot2]
                        if operand2 != addr_key:
                            continue
                        if kind2 in ("def", "rw"):
                            rewritten = True
                        if kind2 in ("use", "rw"):
                            reload_slot = slot2
                    if reload_slot is not None:
                        if (mnem2 in PURE_MOV_MNEMS
                                and len(operands2) == 2
                                and reload_slot == 0
                                and canon.is_plain_register(operands2[1])):
                            found = j
                        break
                    if rewritten:
                        break
                if found is not None:
                    self.store_fate[i] = ("park", found)
                    self.consumed_reload.add(found)
                else:
                    self.store_fate[i] = ("keep", None)

    def one(self, index, line):
        line = strip_reloc(line)
        mnem, operands = canon.parse(line)
        if mnem in ("ret", "retq", "nop", "nopl", "nopw", "cld",
                    "leave", "push", "pushq", "pop", "popq",
                    "call", "callq"):
            return
        if canon.JUMP.match(mnem) or mnem == "ud2":
            # branch/jump/trap instructions are computation STRUCTURE,
            # kept as an explicit control step by the caller (a
            # straight-line unit never reaches here since canon.py's
            # own Walk would have set `branches`; a branching unit's
            # canon2_branching appends the control step itself after
            # this block's per-instruction walk finishes) -- they are
            # never themselves erased-form compute steps.
            return
        role = self.role_log[index]
        fate = self.store_fate.get(index)
        if fate is not None and fate[0] == "park":
            self.park_store_step(operands, role)
            return
        if index in self.consumed_reload:
            self.park_reload_step(operands, role)
            return
        if mnem in SIGN_EXTEND_MNEMS:
            self.sign_extend_step(mnem)
            return
        if mnem in DIVMUL_MNEMS:
            self.divmul_step(mnem, operands, role)
            return
        if (mnem in PURE_MOV_MNEMS and len(operands) == 2
                and role == ["use", "def"]
                and canon.is_plain_register(operands[0])
                and canon.is_plain_register(operands[1])):
            self.alias_step(operands)
            return
        self.compute_step(mnem, operands, role)

    def park_store_step(self, operands, role):
        src_val = None
        addr = None
        for slot, operand in enumerate(operands):
            kind = role[slot]
            if kind == "use" and canon.is_plain_register(operand):
                name = canon.registers_in(operand)[0]
                fam = FAMILY_OF.get(name)
                if fam is not None:
                    src_val = self.occupant(fam)
            if kind in ("def", "rw") and not canon.is_plain_register(
                    operand):
                addr = operand
        if addr is None or src_val is None:
            raise Erasure("erasure_refused: a parked store could not "
                          "be matched to a source value")
        self.mem_park[addr] = src_val
        # no step recorded: this is the erased park, the memory
        # analogue of alias_step's erased register move.

    def park_reload_step(self, operands, role):
        addr = None
        dst_operand = None
        for slot, operand in enumerate(operands):
            kind = role[slot]
            if kind == "use" and not canon.is_plain_register(operand):
                addr = operand
            if kind == "def" and canon.is_plain_register(operand):
                dst_operand = operand
        val = self.mem_park.get(addr)
        if val is None or dst_operand is None:
            raise Erasure("erasure_refused: a memory reload could not "
                          "be matched to its park")
        name = canon.registers_in(dst_operand)[0]
        fam = FAMILY_OF.get(name)
        self.live[fam] = val
        # no step recorded: the park and this reload cancel out
        # exactly like a register-to-register move.

    def memory_write_step(self, mnem, slot_names, operand):
        reads = [n for n in slot_names if n is not None]
        self.steps.append({
            "mnem": mnem,
            "kind": "store",
            "reads": reads,
            "dest_text": operand,
        })

    def alias_step(self, operands):
        src_name = canon.registers_in(operands[0])[0]
        src_fam = FAMILY_OF.get(src_name)
        dst_name = canon.registers_in(operands[1])[0]
        dst_fam = FAMILY_OF.get(dst_name)
        if src_fam is None or dst_fam is None:
            raise Erasure("erasure_refused: a move names a register "
                          "this builder does not track")
        val = self.occupant(src_fam)
        self.live[dst_fam] = val
        # no step recorded: this is the ERASED move itself.

    def sign_extend_step(self, mnem):
        read_val = self.occupant("rax")
        new_val = self.new_u()
        self.live["rdx"] = new_val
        self.steps.append({
            "mnem": mnem,
            "kind": "sign_extend",
            "reads": [read_val],
            "writes": [new_val],
            "pin": {"read_family": "rax"},
        })

    def divmul_step(self, mnem, operands, role):
        if len(operands) != 1 or not canon.is_plain_register(operands[0]):
            raise Erasure("erasure_refused: a divide/multiply operand "
                          "this builder does not track (memory or "
                          "immediate divisor)")
        divisor_name = canon.registers_in(operands[0])[0]
        divisor_fam = FAMILY_OF.get(divisor_name)
        if divisor_fam is None:
            raise Erasure("erasure_refused: unknown divisor register")
        divisor_val = self.occupant(divisor_fam)
        lo_val = self.occupant("rax")
        hi_val = self.occupant("rdx")
        q = self.new_u()
        r = self.new_u()
        self.live["rax"] = q
        self.live["rdx"] = r
        self.steps.append({
            "mnem": mnem,
            "kind": "divmul",
            "reads": [lo_val, hi_val, divisor_val],
            "divisor_width": WIDTH_OF.get(divisor_name),
            "writes": [q, r],
            "pin": {"lo_family": "rax", "hi_family": "rdx"},
        })

    def compute_step(self, mnem, operands, role):
        # generic instruction: some operand slots are read, at most
        # one (the LAST, per canon.py's role tables) is written, and
        # a "rw" slot is read-then-written in the SAME register --
        # the x86 two-operand encoding this whole corpus uses.
        slot_names = []
        pin_cl = None
        rip_names = {}
        for slot, operand in enumerate(operands):
            kind = role[slot]
            if not canon.is_plain_register(operand):
                # REFUSAL CAUSE (a): a rip-relative operand is a VALUE
                # BIRTH -- a constant arriving -- not an undefined
                # read.  Name it k0, k1, ... for DISPLAY only (via
                # `rip_names`, keyed by slot); `slot_names` itself
                # stays None here so derive_runnable keeps copying the
                # literal `const(%rip)` operand text verbatim (it is
                # not a register-resident value -- nothing to `ensure`
                # into a register).
                slot_names.append(None)
                if kind in ("use", "rw") and "(%rip)" in operand:
                    rip_names[slot] = self.new_k()
                continue
            name = canon.registers_in(operand)[0]
            fam = FAMILY_OF.get(name)
            if fam is None or fam in NEVER_RENAME:
                slot_names.append(None)
                continue
            if kind in ("use", "rw"):
                val = self.occupant(fam)
                slot_names.append(val)
                if operand == "%cl" and mnem in SHIFT_MNEMS:
                    pin_cl = val
            else:
                slot_names.append(None)
        writes = []
        written_this_instr = {}
        for slot, operand in enumerate(operands):
            kind = role[slot]
            if kind not in ("def", "rw"):
                continue
            if not canon.is_plain_register(operand):
                self.memory_write_step(mnem, slot_names, operand)
                return
            name = canon.registers_in(operand)[0]
            fam = FAMILY_OF.get(name)
            if fam is None or fam in NEVER_RENAME:
                continue
            # BUGFIX (this slice): `xor %eax,%eax` gets role
            # ["def","def"] from canon.py's self_zeroing rule -- both
            # operand mentions name the SAME destination home, so this
            # instruction defines ONE new value, not two.  canon.py's
            # own Walk.redefine() dedups by family for exactly this
            # reason; this builder must too, or the second phantom
            # def (never entered into any register at derive time)
            # gets read downstream and the unit is wrongly refused
            # ("u1 is read before it is defined").
            if fam in written_this_instr:
                self.live[fam] = written_this_instr[fam]
                continue
            new_val = self.new_u()
            written_this_instr[fam] = new_val
            self.live[fam] = new_val
            writes.append((slot, new_val, kind, canon.is_vector(fam)))
        self.steps.append({
            "mnem": mnem,
            "kind": "generic",
            "operand_texts": operands,
            "role": role,
            "slot_names": slot_names,
            "writes": writes,
            "pin_cl": pin_cl,
            "rip_names": rip_names,
        })


def relabel_answer(steps, final_name):
    """the value the calling rule hands back is renamed `answer`
    everywhere it appears, in place, so the erased record reads the
    way the ruling describes it (values named a/b/answer, temps
    u0,u1,...)."""
    if final_name is None:
        return steps, None
    if not final_name.startswith("u"):
        # a pass-through (return a; / return b;) or an unresolved
        # incoming value -- name it answer at the point of use only.
        return steps, final_name

    def swap(name):
        if name == final_name:
            return "answer"
        return name

    out = []
    for step in steps:
        s = dict(step)
        if "reads" in s:
            s["reads"] = [swap(x) for x in s["reads"]]
        if "writes" in s and s["kind"] != "generic":
            s["writes"] = [swap(x) for x in s["writes"]]
        if s["kind"] == "generic":
            s["slot_names"] = [swap(x) if x is not None else None
                               for x in s["slot_names"]]
            s["writes"] = [(slot, swap(name), kind, is_vec)
                           for slot, name, kind, is_vec in s["writes"]]
        out.append(s)
    return out, "answer"


def step_text(step):
    """the display line for one erased step -- literal, no operator
    spelling, only value names and the real instruction mnemonic."""
    if step["kind"] == "sign_extend":
        return "%s = %s(%s)" % (step["writes"][0], step["mnem"],
                                step["reads"][0])
    if step["kind"] == "divmul":
        q, r = step["writes"]
        lo, hi, divisor = step["reads"]
        return "%s, %s = %s(%s:%s, %s)" % (q, r, step["mnem"], hi, lo,
                                           divisor)
    if step["kind"] == "store":
        return "mem = %s(%s)" % (step["mnem"],
                                 ",".join(step["reads"]) or "_")
    if step["kind"] == "control":
        return step["text"]
    names = []
    rip_names = step.get("rip_names") or {}
    for slot, n in enumerate(step["slot_names"]):
        if n is not None:
            names.append(n)
        elif slot in rip_names:
            names.append(rip_names[slot])
        else:
            names.append("_")
    write_names = ",".join(w for _s, w, _k, _v in step["writes"]) or "_"
    return "%s = %s(%s)" % (write_names, step["mnem"], ",".join(names))


# ------------------------------------------------------- derive pass

def default_contract(is_a_vector, is_b_present, is_b_vector,
                     is_result_vector):
    a_reg = "xmm0" if is_a_vector else "rdi"
    if is_b_present:
        if is_b_vector:
            b_reg = "xmm1" if is_a_vector else "xmm0"
        else:
            b_reg = "rdi" if is_a_vector else "rsi"
    else:
        b_reg = None
    result_reg = "xmm0" if is_result_vector else "rax"
    return {"a": a_reg, "b": b_reg, "result": result_reg}


def render(family, width):
    if canon.is_vector(family):
        return family
    return canon.GP_NAMES[family][width]


def derive_runnable(steps, final_name, contract):
    """rebuild AT&T text from the erased steps, inserting an adapter
    mov wherever the entry contract's registers do not already hold
    the value a step needs.  This is the rule the AMENDMENT names:
    value-here + needed-there produces the adapter mov."""
    reg_of = {}
    if contract["a"] is not None:
        reg_of["a"] = contract["a"]
    if contract["b"] is not None:
        reg_of["b"] = contract["b"]
    text = []
    temp_bench = list(TEMPS)
    vector_temp_bench = list(VECTOR_TEMPS)
    assigned_temp = {}

    def width_for(name, fallback=1):
        return fallback

    def ensure(name, target, width):
        cur = reg_of.get(name)
        if cur is None:
            raise Erasure("erasure_refused: value %s is read before it "
                          "is defined or before the unit's entry "
                          "contract names it" % name)
        if cur == target:
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

    def temp_for(name, is_vec):
        if name in assigned_temp:
            return assigned_temp[name]
        bench = vector_temp_bench if is_vec else temp_bench
        if not bench:
            raise Erasure("erasure_refused: temps exhausted deriving "
                          "runnable text")
        t = bench.pop(0)
        assigned_temp[name] = t
        return t

    for step in steps:
        kind = step["kind"]
        if kind == "sign_extend":
            src = step["reads"][0]
            ensure(src, "rax", 1)
            text.append(step["mnem"])
            dst = step["writes"][0]
            reg_of[dst] = "rdx"
            continue
        if kind == "store":
            # REFUSAL CAUSE (b), keep-case: this store IS the unit's
            # real output (or its slot is never reloaded) -- render it
            # as a genuine instruction, its source value put wherever
            # it currently lives.
            reads = list(step["reads"])
            if reads:
                src = reads[0]
                cur = reg_of.get(src)
                if cur is None:
                    raise Erasure("erasure_refused: value %s is read "
                                  "before it is defined or before the "
                                  "unit's entry contract names it"
                                  % src)
                text.append("%s %%%s,%s" % (step["mnem"],
                                            render(cur, 1),
                                            step["dest_text"]))
            else:
                text.append("%s %s" % (step["mnem"], step["dest_text"]))
            continue
        if kind == "divmul":
            lo, hi, divisor = step["reads"]
            ensure(lo, "rax", 1)
            ensure(hi, "rdx", 1)
            dwidth = step.get("divisor_width", 1)
            if reg_of.get(divisor) in ("rax", "rdx"):
                raise Erasure("erasure_refused: the divisor value would "
                              "have to share %rax/%rdx with the "
                              "dividend -- not attempted this slice")
            divisor_reg = reg_of.get(divisor)
            if divisor_reg is None:
                raise Erasure("erasure_refused: divisor value has no "
                              "known register")
            text.append("%s %%%s" % (step["mnem"], render(divisor_reg,
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
        # a value can cross from the general-purpose file to the
        # vector file (or back) between one instruction and the next
        # -- `movq %rdi,%xmm1` bit-reinterprets an integer argument
        # for a floating-point computation.  That crossing is real
        # bookkeeping the derivation must redo when the value's
        # CURRENT register is in the wrong file for this operand,
        # regardless of whether this step is the unit's last one.
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
            if cur is None or canon.is_vector(cur) == wanted_vec:
                continue
            is_final_write = (slot == write_slot and role[slot] == "rw"
                              and (name == final_name
                                   or name == "answer"))
            if is_final_write:
                target = contract["result"]
            else:
                target = temp_for(name, wanted_vec)
            ensure(name, target, 0)
        if write_kind == "rw":
            old_name = slot_names[write_slot]
            is_final = (write_name == final_name or write_name == "answer")
            target = contract["result"] if is_final else reg_of.get(
                old_name)
            if target is None:
                raise Erasure("erasure_refused: an in-place value has "
                              "no known register")
            if is_final:
                width = width_for(old_name)
                ensure(old_name, target, width)
            reg_of[write_name] = target
        elif write_kind == "def":
            is_final = (write_name == final_name or write_name == "answer")
            target = contract["result"] if is_final else temp_for(
                write_name, write_vec)
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
                # a pure "def" register slot (canon.py's role table
                # gave it no "use"/"rw" reading, e.g. BOTH mentions of
                # `xor %eax,%eax` -- self_zeroing marks both slots
                # "def") was never given a value name above -- there
                # is nothing to read there -- but its register WAS
                # just relocated to `write_name`'s target below.
                # Re-render EVERY def-only mention of that same
                # register family here, or the emitted instruction
                # keeps writing (part of) the compiler's original
                # register while every later reader is told the value
                # lives somewhere else.
                if (canon.is_plain_register(operand)
                        and FAMILY_OF.get(canon.registers_in(operand)[0])
                        == write_fam and write_fam is not None):
                    regname = canon.registers_in(operand)[0]
                    width = WIDTH_OF.get(regname, 1)
                    pieces.append("%" + render(reg_of[write_name],
                                               width))
                    continue
                pieces.append(operand)
                continue
            width = WIDTH_OF.get(canon.registers_in(operand)[0], 1)
            if slot == write_slot:
                target_family = reg_of[write_name]
            else:
                target_family = reg_of.get(name)
                if target_family is None:
                    raise Erasure("erasure_refused: value %s used "
                                  "before it is defined" % name)
            pieces.append("%" + render(target_family, width))
        if pieces:
            text.append("%s %s" % (step["mnem"], ",".join(pieces)))
        else:
            text.append(step["mnem"])
    if final_name is not None:
        width = 1
        if final_name not in reg_of:
            raise Erasure("erasure_refused: the answer value never "
                          "entered a tracked register (a passthrough "
                          "this builder does not model)")
        ensure(final_name, contract["result"], width)
    text.append("ret")
    return text


# --------------------------------------------------------- per unit

def is_vector_rep(rep):
    return rep in ("f32", "f64")


def build_contract(meta, anchor, actual_result_family):
    a_vec = is_vector_rep(meta.get("lhs_rep"))
    b_present = anchor.get("in1") is not None
    b_vec = is_vector_rep(meta.get("rhs_rep"))
    r_vec = canon.is_vector(actual_result_family)
    return default_contract(a_vec, b_present, b_vec, r_vec)


def canon2_one(lang, n, sem_rec, canon_rec):
    meta = sem_rec.get("meta", {})
    sem = sem_rec.get("sem", {})
    anchor = sem.get("anchor_registers")
    lines = sem_rec.get("mnem")
    out = {}
    out["lang"] = lang
    out["n"] = n
    out["unit"] = "%s/op_%s" % (lang, n)
    out["operator"] = meta.get("operator")
    out["meta"] = meta
    out["mnem"] = lines
    out["bytes"] = sem_rec.get("bytes")
    if anchor is None or not lines:
        out["erasure"] = "erasure_refused: no anchored register map or "\
                         "no instruction text"
        return out
    fam = canon.result_register_family(lang, meta, lines)
    walker = canon.Walk(lines, anchor, fam)
    try:
        walker.run()
    except canon.Refusal:
        # canon.py's OWN refusals (pinned traced value, argument
        # modified in place) are exactly the two cases this slice
        # exists to handle differently.  By the time run() raises,
        # it has already walked every line -- role_log and the
        # branch flag are fully populated -- so the refusal is
        # ignored here and this program does its own thing with
        # that same per-instruction role data.
        pass
    if walker.branches:
        return canon2_branching(lang, n, sem_rec, out, anchor, lines,
                                walker)
    # walker.result_family is canon.py's OWN determination of which
    # register the calling rule actually used at return -- read off
    # the unit's own code (whichever of %rax/%xmm0 the unit itself
    # last computed into), not the meta-derived guess `fam`, which
    # is only a priority hint canon.py's Walk may correct (e.g. an
    # int/float comparison whose C result_type is unstated: the
    # code visibly returns the bit in %rax even though both operands
    # are floating point).
    actual_result_family = walker.result_family
    contract = build_contract(meta, anchor, actual_result_family)
    try:
        eraser = Erased(anchor, lines, walker.role_log,
                        actual_result_family)
        steps, final_name = eraser.run()
        steps, final_name = relabel_answer(steps, final_name)
    except Erasure as bad:
        out["erasure"] = bad.reason
        return out
    # REFUSAL CAUSE (c): "temps exhausted" is a fact about DERIVING
    # runnable text under the default contract (only two temp
    # registers are on the bench) -- it is not a fact about the
    # erased form, which carries no register pressure at all (values
    # are just names).  A unit whose erasure succeeds but whose
    # derivation cannot find enough temps still has a real erased
    # form and takes part in erased-form matching; only its
    # `derived_text` is marked refused, separately.
    out["erasure"] = "ok"
    out["entry_contract"] = contract
    out["erased_form"] = [step_text(s) for s in steps]
    try:
        derived = derive_runnable(steps, final_name, contract)
    except Erasure as bad:
        out["derived_text"] = "refused: %s" % bad.reason
        out["derive_refused"] = bad.reason
        return out
    out["derived_text"] = derived
    out["derived_mnem_joined"] = "; ".join(derived)
    out["exact_regeneration"] = derived == list(lines)
    return out


# ------------------------------------------------ branching units

JUMP_TARGET = __import__("re").compile(
    r"<[^+>]*\+0x([0-9a-fA-F]+)>|<[^+>]*>")


def real_addresses(bytes_hex, expect_count):
    """disassemble the unit's OWN captured bytes with the system
    `objdump`, for real -- the same real-tool standard this whole
    program holds itself to elsewhere -- to get each instruction's
    real byte offset from the function's start.  This is how branch
    targets (`<sym+0x1a>`) are turned into instruction indices without
    guessing at instruction-length tables."""
    raw = bytes(int(tok, 16) for tok in bytes_hex.split())
    tmpdir = tempfile.mkdtemp(prefix="canon2_addr_")
    try:
        binpath = os.path.join(tmpdir, "u.bin")
        fh = open(binpath, "wb")
        fh.write(raw)
        fh.close()
        proc = subprocess.run(
            ["objdump", "-D", "-b", "binary", "-m", "i386:x86-64",
             "-M", "att", "--no-show-raw-insn", binpath],
            capture_output=True, text=True)
        addrs = []
        for line in proc.stdout.splitlines():
            line = line.rstrip()
            if not line or ":" not in line or not line[0:1].isspace():
                continue
            head = line.strip().split(":", 1)
            if len(head) != 2:
                continue
            try:
                addr = int(head[0], 16)
            except ValueError:
                continue
            addrs.append(addr)
        if len(addrs) != expect_count:
            return None
        return addrs
    finally:
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)


def find_jump_target_offset(operand_text):
    m = JUMP_TARGET.search(operand_text)
    if m is None:
        return None
    if m.group(1) is not None:
        return int(m.group(1), 16)
    return 0


def cut_blocks(lines, addrs):
    """leaders = entry, every branch target, and the instruction right
    after every branch/jmp/ret/call -- the textbook basic-block cut,
    reused from the same idea as arch_sem.py's `blocks_of` (VEX-block
    cutting) but done here directly over the real, addressed mnem
    text so branch targets land on exact instruction indices."""
    n = len(lines)
    addr_to_index = {}
    for i, a in enumerate(addrs):
        addr_to_index[a] = i
    leaders = set([0])
    edges = {}
    branch_target_index = {}
    for i, line in enumerate(lines):
        mnem, operands = canon.parse(strip_reloc(line))
        bare = mnem
        if canon.JUMP.match(bare):
            base_off = None
            for operand in operands:
                off = find_jump_target_offset(operand)
                if off is not None:
                    base_off = off
            target_idx = addr_to_index.get(base_off)
            succs = []
            if target_idx is not None:
                leaders.add(target_idx)
                succs.append(target_idx)
                branch_target_index[i] = target_idx
            if bare != "jmp" and i + 1 < n:
                leaders.add(i + 1)
                succs.append(i + 1)
            edges[i] = ("jump", succs)
        elif bare in ("ret", "retq"):
            edges[i] = ("ret", [])
        elif bare in ("ud2",):
            edges[i] = ("trap", [])
        elif bare in ("call", "callq"):
            if i + 1 < n:
                leaders.add(i + 1)
                edges[i] = ("call", [i + 1])
            else:
                edges[i] = ("call", [])
    ordered_leaders = sorted(leaders)
    block_of_index = {}
    blocks = []
    for bi, start in enumerate(ordered_leaders):
        end = n
        for later in ordered_leaders:
            if later > start:
                end = later
                break
        blocks.append((start, end))
        for i in range(start, end):
            block_of_index[i] = bi
    successors = {}
    for bi, (start, end) in enumerate(blocks):
        last = end - 1
        if last in edges:
            kind, succ_indices = edges[last]
            successors[bi] = [block_of_index[s] for s in succ_indices]
        else:
            if end < n:
                successors[bi] = [block_of_index[end]]
            else:
                successors[bi] = []
    return blocks, successors, edges, branch_target_index, block_of_index


def control_step_text(mnem, operands, target_label, last_desc):
    if canon.JUMP.match(mnem):
        label = target_label if target_label is not None else "L?"
        if mnem == "jmp":
            return "jump %s %s" % (mnem, label)
        cond = last_desc if last_desc is not None else "?"
        return "branch %s %s if %s" % (mnem, label, cond)
    if mnem in ("ret", "retq"):
        return "return"
    if mnem in ("call", "callq"):
        target = operands[0] if operands else ""
        m = __import__("re").search(r"<([^>]+)>", target)
        name = m.group(1) if m else target
        return "call %s" % name
    if mnem == "ud2":
        return "trap"
    return "%s %s" % (mnem, ",".join(operands))


def canon2_branching(lang, n, sem_rec, out, anchor, lines, walker):
    """Cut a branching unit into straight blocks at branch targets and
    branch instructions, then erase moves WITHIN each block, carrying
    the value->register map along every edge (fall-through and branch
    target) to the block it reaches.  Branch/jump/call/trap
    instructions are computation structure -- they are kept as steps,
    never erased.  Two paths reaching one block under different maps
    are an honest refusal (`conflicting value maps at join`), not a
    guess: nothing here invents a phi value.  Labels are L0, L1, ...
    in address order, so two units' block-erased forms can be
    character-compared."""
    bytes_hex = sem_rec.get("bytes")
    if not bytes_hex:
        out["erasure"] = "deferred: branching (no bytes to address)"
        return out
    addrs = real_addresses(bytes_hex, len(lines))
    if addrs is None:
        out["erasure"] = "deferred: branching (could not align real "\
                         "disassembly to instruction count)"
        return out
    blocks, successors, edges, branch_target_index, block_of_index = \
        cut_blocks(lines, addrs)
    block_labels = {}
    for bi in range(len(blocks)):
        block_labels[bi] = "L%d" % bi

    ctx = {"u": 0, "w": 0, "k": 0}
    incoming = {0: {}}
    if anchor.get("in0") is not None:
        incoming[0][FAMILY_OF[anchor["in0"]]] = "a"
    if anchor.get("in1") is not None:
        incoming[0][FAMILY_OF[anchor["in1"]]] = "b"
    visited = {}
    block_records_by_bi = {}
    conflict = None
    order = [0]
    seen_order = set([0])
    fam = walker.result_family
    while order:
        bi = order.pop(0)
        if bi in visited:
            continue
        live_in = incoming.get(bi)
        if live_in is None:
            continue
        start, end = blocks[bi]
        sub_lines = lines[start:end]
        sub_role_log = {}
        for j in range(start, end):
            sub_role_log[j - start] = walker.role_log.get(j, [])
        eraser = Erased(anchor, sub_lines, sub_role_log, fam,
                        live=dict(live_in), ctx=ctx)
        eraser.start = lambda: None  # entry values come from live_in
        try:
            for idx, ln in enumerate(sub_lines):
                eraser.one(idx, ln)
        except Erasure as bad:
            block_records_by_bi[bi] = {
                "label": block_labels[bi], "steps": [],
                "erasure": bad.reason,
            }
            visited[bi] = dict(eraser.live)
            continue
        last_i = end - 1
        last_desc = None
        for s in eraser.steps:
            txt = step_text(s)
            if " = " in txt:
                txt = txt.split(" = ", 1)[1]
            last_desc = txt
        if last_i in edges:
            emnem, eoperands = canon.parse(strip_reloc(lines[last_i]))
            target_label = None
            if last_i in branch_target_index:
                target_label = block_labels[
                    block_of_index[branch_target_index[last_i]]]
            ctext = control_step_text(emnem, eoperands, target_label,
                                      last_desc)
            eraser.steps.append({"kind": "control", "text": ctext})
        block_records_by_bi[bi] = {
            "label": block_labels[bi],
            "steps": [step_text(s) for s in eraser.steps],
        }
        visited[bi] = dict(eraser.live)
        for s in successors.get(bi, []):
            if s in incoming:
                for f, v in visited[bi].items():
                    if f in incoming[s] and incoming[s][f] != v:
                        conflict = ("conflicting value maps at join "
                                   "entering %s (family %%%s: %s vs "
                                   "%s)" % (block_labels[s], f,
                                            incoming[s][f], v))
                # merge in whatever this predecessor agrees with the
                # existing incoming map on; anything it disagrees on
                # is exactly the conflict flagged above.
            else:
                incoming[s] = dict(visited[bi])
            if s not in seen_order:
                order.append(s)
                seen_order.add(s)
    # labels are L0, L1, ... in ADDRESS order (`bi` is already assigned
    # that way); output the blocks in that same order regardless of
    # the traversal order the join-carrying walk used, so two units'
    # block-erased forms line up character-for-character.
    block_records = [block_records_by_bi[bi]
                     for bi in sorted(block_records_by_bi.keys())]
    out["blocks"] = block_records
    out["block_labels"] = block_labels
    flattened = []
    for rec in block_records:
        flattened.append("%s:" % rec["label"])
        for line in rec["steps"]:
            flattened.append("  " + line)
        if rec.get("erasure"):
            flattened.append("  refused: %s" % rec["erasure"])
    out["erased_form"] = flattened
    if conflict is not None:
        out["erasure"] = "erasure_refused: %s" % conflict
        return out
    any_block_refused = any(r.get("erasure") for r in block_records)
    if any_block_refused:
        reasons = [r["erasure"] for r in block_records if r.get("erasure")]
        out["erasure"] = "erasure_refused: %s" % reasons[0]
        return out
    out["erasure"] = "ok"
    out["derived_text"] = "not derived this slice: branching units "\
                          "are erased per-block; multi-block runnable "\
                          "derivation is future work"
    return out


# ---------------------------------------------------- assembler pass

ASM_PROLOGUE = {
    "c": ".text\n.globl op_unit\n.type op_unit,@function\nop_unit:\n",
    "default": ".text\n.globl op_unit\n.type op_unit,@function\nop_unit:\n",
}


def assemble_and_disassemble(lines, workdir):
    """a REAL roundtrip: write the derived text as a tiny function
    body, run the system `as`, then `objdump -d` the result, and
    record what came back.  This is the tool's own testimony that
    the derived text is valid, encodable x86-64."""
    src = ASM_PROLOGUE["default"]
    for line in lines:
        src = src + "\t" + line + "\n"
    src_path = os.path.join(workdir, "u.s")
    obj_path = os.path.join(workdir, "u.o")
    fh = open(src_path, "w")
    fh.write(src)
    fh.close()
    proc = subprocess.run(["as", "--64", "-o", obj_path, src_path],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        return {"assembled": False, "as_stderr": proc.stderr.strip()}
    proc2 = subprocess.run(["objdump", "-d", "--no-show-raw-insn",
                            obj_path],
                           capture_output=True, text=True)
    proc3 = subprocess.run(["objdump", "-d", obj_path],
                           capture_output=True, text=True)
    bytes_line = extract_bytes(proc3.stdout)
    return {
        "assembled": True,
        "objdump_text": proc2.stdout,
        "bytes": bytes_line,
    }


def extract_bytes(objdump_text):
    out = []
    for line in objdump_text.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        after_colon = line.split(":", 1)[1]
        parts = after_colon.strip().split("\t")
        hexpart = parts[0].strip()
        if not hexpart:
            continue
        toks = hexpart.split()
        ok = True
        for t in toks:
            if len(t) != 2:
                ok = False
        if ok:
            out.extend(toks)
    return " ".join(out)


# ------------------------------------------------------------ driver

def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def run_language(lang, indir, outdir, workdir):
    sem_path = os.path.join(indir, "sem_anchored_%s.json" % lang)
    canon_path = os.path.join(indir, "canon_units_%s.json" % lang)
    sem_doc = json.load(open(sem_path))
    canon_doc = json.load(open(canon_path))
    sem_units = sem_doc["units"]
    canon_units = canon_doc["units"]
    keys = sorted(sem_units.keys(), key=lambda x: int(x))
    rows = {}
    deferred_branching = 0
    erasure_refused = 0
    erased_ok = 0
    assembled_ok = 0
    assembled_failed = 0
    exact_regen = 0
    reasons = {}
    for n in keys:
        rec = canon2_one(lang, n, sem_units[n], canon_units.get(n, {}))
        if rec["erasure"].startswith("deferred:"):
            deferred_branching = deferred_branching + 1
        elif rec["erasure"] == "ok":
            erased_ok = erased_ok + 1
            if isinstance(rec.get("derived_text"), list):
                rt = assemble_and_disassemble(rec["derived_text"], workdir)
                rec["roundtrip"] = rt
                if rt["assembled"]:
                    assembled_ok = assembled_ok + 1
                else:
                    assembled_failed = assembled_failed + 1
                if lang == "c" and rec.get("exact_regeneration"):
                    exact_regen = exact_regen + 1
        else:
            erasure_refused = erasure_refused + 1
            reasons[rec["erasure"]] = reasons.get(rec["erasure"], 0) + 1
        rows[n] = rec
    out = {}
    out["language"] = lang
    out["meta"] = {
        "role": "generator provenance",
        "form": "erased-form + entry-contract canonical record "\
               "(AMENDMENT: moves are erased by substitution, "\
               "the owner 2026-08-26); runnable text is DERIVED from it "\
               "under the default contract",
        "spelling": "the operator token appears once per unit, as "\
                   "the display label `operator` on a unit object",
        "generator": "canon2.py",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                      time.gmtime()),
    }
    out["units_read"] = len(keys)
    out["deferred_branching"] = deferred_branching
    out["erasure_refused"] = erasure_refused
    out["erasure_refused_reasons"] = reasons
    out["erased_ok"] = erased_ok
    out["assembled_ok"] = assembled_ok
    out["assembled_failed"] = assembled_failed
    if lang == "c":
        out["exact_regeneration_against_compiler_mnem"] = exact_regen
    out["units"] = rows
    name = os.path.join(outdir, "canon2_units_%s.json" % lang)
    fh = open(name, "w")
    json.dump(out, fh, indent=1)
    fh.close()
    log("wrote %s (%d read, %d deferred-branching, %d erasure_refused, "
        "%d erased_ok, %d assembled_ok, %d assembled_failed)"
        % (name, len(keys), deferred_branching, erasure_refused,
           erased_ok, assembled_ok, assembled_failed))
    return out


def main(argv):
    indir = HERE
    outdir = HERE
    i = 1
    while i < len(argv):
        if argv[i] == "--in":
            indir = argv[i + 1]
            i = i + 2
            continue
        if argv[i] == "--out":
            outdir = argv[i + 1]
            i = i + 2
            continue
        print(__doc__)
        return 2
    started = time.time()
    log("canon2.py -- erased form + entry contract + derived text")
    workdir = tempfile.mkdtemp(prefix="canon2_asm_")
    for lang in LANGS:
        run_language(lang, indir, outdir, workdir)
    log("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
