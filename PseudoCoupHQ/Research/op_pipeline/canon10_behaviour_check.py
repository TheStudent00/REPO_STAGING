#!/usr/bin/env python3
"""canon10_behaviour_check.py -- TASK 26 (log_109 round 5): the
FLOAT-FAMILY gate.

WHAT WAS ACTUALLY BLOCKING THESE UNITS, read off the records rather
than carried from a prior report. log_105 named the float family's
root cause as "the float-operand classifier (_operand_xmm) only knows
a/b/zero ... needing fresh register-allocation logic" in
canon17_float.py. That reading does not survive contact with the
current records: canon4_units_<lang>.json ALREADY carries a rendered
candidate for 116 of the 120 float units (a `derived_text` list for
74, `derived_blocks` for 42). The rendering is not missing. What is
missing is on the GATE side, and every one of these units says so in
its own words:

  c/op_141 reason: "no return path: expression contains an
  uninterpreted atom for VEX op 'Sub32F0x4' -- SIMD packed-float sub
  (not modeled)"

That is the name->z3 translation table, exactly the limit AgentMemory
records ("The lifter was measured NOT to be the limiting factor ...
the limit was our own name->z3 translation table. Fix tables, not
tools."). So this file extends the SIMULATOR's table, in the same
wrapper lineage every prior lap used: Sim10 subclasses
canon9_behaviour_check.Sim9, which subclasses Sim8/Sim7/ExtSim/Sim.
canon5..canon9_behaviour_check.py are UNCHANGED and imported by
reference only.

HOW FLOAT IS MODELED, and why the model is sound for THIS question.
The question asked here is never "what does this float program
compute" -- it is "do these two instruction texts compute THE SAME
value". So every genuinely floating-point operation is modeled as an
UNINTERPRETED FUNCTION over bitvectors: `addss` is a function
FADD32(x, y) -> 32 bits, about which nothing is assumed. Two texts
prove equal only if they agree for EVERY interpretation of those
functions, and IEEE-754's actual behaviour is one such interpretation
-- so a proof here holds of the real machine. This direction is the
sound one; it is deliberately incomplete (no float algebra is
available to the solver, and none is wanted -- float addition is not
associative, so an "optimization" resting on that would be a bug we
must not prove away).

Everything that is NOT float arithmetic is modeled EXACTLY, as
bitvectors: lane structure (`punpckldq`, `unpckhpd`), full-width
copies (`movaps`/`movapd`), the low-lane merge rules, the zero-
extension rules of `movq`/`movd`, and the stack spill/reload forms.
That exactness is the point -- the corpus's real difficulty is where
values are parked and which lane they occupy, and that is precisely
what an uninterpreted-function model leaves fully visible.

THE FLOAT FLAG RULE (`ucomiss`/`ucomisd` + `seta`/`setae`/`setne`/
`setp`). condition_table.py already lists `ucomisd`/`ucomiss` in its
FLAGSETTER_MNEMONICS, but cond_to_z3 would read the operands as
integers. So Sim10 tracks a float compare separately and derives the
three flags by the hardware's own rule, over three uninterpreted
predicates FUNORD / FLT / FEQ of the two operands:

    ZF = FUNORD(x,y) or FEQ(x,y)
    PF = FUNORD(x,y)
    CF = FUNORD(x,y) or FLT(x,y)

and then `seta` = not CF and not ZF, `setae` = not CF, `setne` = not
ZF, `setp` = PF -- the documented flag consumption, with the float
relation itself left uninterpreted. No constraint tying the three
predicates together is asserted; omitting such constraints can only
make the solver WEAKER (fewer things provable), never unsound.

WHERE THE ANSWER LIVES -- read off the GROUND TRUTH, never guessed.
canon4's own `entry_contract["result"]` field is NOT usable here: it
was measured wrong on this population (c/op_117, c/op_118, c/op_189
all declare "rax" while the real ship code's last write is plainly
`addss`/`addsd`/`mulss` into %xmm0). So the answer home is taken from
the unit's OWN REAL SHIP CODE: the last instruction of the real text
whose destination is %xmm0 or an rax-family register wins, and the
answer WIDTH comes from that instruction's own operand-size suffix
(`ss`/`aps`/`movd` -> 32, `sd`/`apd`/`pd`/`movq` -> 64). Both the
real and the candidate simulation are then read at that one home and
width. This is the ground-truth-anchored rule the standing
requirement demands, and it is what makes a candidate's extra dead
write (c/op_117's candidate ends `... addss %xmm2,%xmm0; mov
%edi,%eax; ret`, a write the real code never makes) harmless rather
than answer-changing.

RIP-RELATIVE CONSTANTS. The real text spells a constant pool load as
`punpckldq 0x0(%rip),%xmm1 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4`; the
candidate spells the same load as `punpckldq 0x0(%rip),%xmm2` with no
reloc annotation. The two texts must therefore agree on WHICH
constant by position, not by name. Sim10 gives the k-th rip-relative
READ in a text the k-th fresh constant symbol, and the driver runs a
MECHANICAL GUARD first: the ordered list of mnemonics carrying a
rip-relative operand must be identical in the two texts, or the unit
is refused UNDECIDED rather than gated on an assumption. The guard's
outcome is recorded per unit.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

Nothing in this file reads an operator token. Unit selection is by
VEX lifter name (census27.names_from_raw over tree_units3.json's own
`normal_path_raw`), a machine-form name; each unit is gated ALONE
against its own ship code, so no pairing of units against each other
happens here at all.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                # noqa: E402
import canon5_behaviour_check as BC5                        # noqa: E402
import canon8_behaviour_check as BC8                        # noqa: E402
import canon9_behaviour_check as BC9                        # noqa: E402
import real_blocks                                          # noqa: E402
import z3                                                 # noqa: E402

NotModeled = BC5.NotModeled
split_operands = BC5.split_operands
Trap = BC9.Trap

XMM_NAMES = frozenset(["xmm%d" % i for i in range(16)])

# ---------------------------------------------------------------
# the uninterpreted float vocabulary. One z3 Function per (operation,
# width). Built once at import so every unit and every simulation
# shares the SAME function symbols -- two texts using `addss` are
# talking about one function, which is what makes them comparable.
# ---------------------------------------------------------------

def _bin_fn(name, width):
    dom = z3.BitVecSort(width)
    return z3.Function(name, dom, dom, dom)


FADD = {32: _bin_fn("FADD32", 32), 64: _bin_fn("FADD64", 64)}
FSUB = {32: _bin_fn("FSUB32", 32), 64: _bin_fn("FSUB64", 64)}
FMUL = {32: _bin_fn("FMUL32", 32), 64: _bin_fn("FMUL64", 64)}
FDIV = {32: _bin_fn("FDIV32", 32), 64: _bin_fn("FDIV64", 64)}

# integer -> float conversion, one function per (source width,
# destination width) so a 32-bit source and a 64-bit source are never
# silently the same function.
FCVT_I2F = {}
for _sw in (32, 64):
    for _dw in (32, 64):
        FCVT_I2F[(_sw, _dw)] = z3.Function(
            "FCVT_I%d_TO_F%d" % (_sw, _dw),
            z3.BitVecSort(_sw), z3.BitVecSort(_dw))

FCVT_F32_F64 = z3.Function(
    "FCVT_F32_TO_F64", z3.BitVecSort(32), z3.BitVecSort(64))

# the three ordering predicates behind ucomiss/ucomisd and behind the
# cmpeqss/cmpneqss lane masks.
FUNORD = {}
FLT = {}
FEQ = {}
for _w in (32, 64):
    _s = z3.BitVecSort(_w)
    FUNORD[_w] = z3.Function("FUNORD%d" % _w, _s, _s, z3.BoolSort())
    FLT[_w] = z3.Function("FLT%d" % _w, _s, _s, z3.BoolSort())
    FEQ[_w] = z3.Function("FEQ%d" % _w, _s, _s, z3.BoolSort())


# widths implied by an instruction's own operand-size spelling.
SS_MNEM = ("ss", "aps", "ps")
SD_MNEM = ("sd", "apd", "pd")

ARITH_FN = {
    "add": FADD,
    "sub": FSUB,
    "mul": FMUL,
    "div": FDIV,
}


def width_of_float_mnem(mnem):
    """32 or 64, from the mnemonic's own operand-size spelling, or
    None when the mnemonic states no float width."""
    if mnem == "movd":
        return 32
    if mnem == "movq":
        return 64
    if mnem.endswith("ss"):
        return 32
    if mnem.endswith("sd"):
        return 64
    if mnem.endswith("aps") or mnem.endswith("ps"):
        return 32
    if mnem.endswith("apd") or mnem.endswith("pd"):
        return 64
    return None


class Sim10(BC9.Sim9):
    """canon9_behaviour_check.Sim9, plus 128-bit XMM state, the
    scalar/packed float vocabulary as uninterpreted functions, a
    literal-keyed memory for stack spills, positionally-keyed
    rip-relative constants, and the float flag rule.

    XMM families are stored in the SAME `self.regs` dict the inherited
    branch walker already saves and restores, and memory cells are
    stored there too under a "MEM:" key prefix, so no walker change is
    needed for state rollback across a conditional branch."""

    def __init__(self, shared_seed, tag):
        BC9.Sim9.__init__(self, shared_seed, tag)
        self.last_fcmp = None
        self.rip_reads = 0
        self.rip_mnem_order = []
        self.answer_family = None
        self.answer_width = None

    # -- register plumbing -------------------------------------------

    def family_of(self, operand):
        name = operand[1:]
        fam = canon.FAMILY_OF.get(name)
        if fam is None:
            raise NotModeled(
                "register spelling %r not in canon.py's FAMILY_OF "
                "table" % operand)
        return fam

    def is_xmm(self, operand):
        if not operand.startswith("%"):
            return False
        return operand[1:] in XMM_NAMES

    def get_family(self, fam):
        """128-bit symbols for xmm families, 64-bit for everything
        else (the inherited rule)."""
        if fam not in XMM_NAMES:
            return BC9.Sim9.get_family(self, fam)
        if fam in self.regs:
            return self.regs[fam]
        if fam not in self.shared_seed:
            self.shared_seed[fam] = z3.BitVec("seed_%s" % fam, 128)
        v = self.shared_seed[fam]
        self.regs[fam] = v
        return v

    def read_xmm(self, operand):
        fam = self.family_of(operand)
        return self.get_family(fam)

    def write_xmm(self, operand, value128):
        if value128.size() != 128:
            raise NotModeled(
                "internal: an xmm write of %d bits, not 128"
                % value128.size())
        fam = self.family_of(operand)
        self.regs[fam] = value128

    def lane(self, value128, index, width):
        low = index * width
        return z3.Extract(low + width - 1, low, value128)

    def set_low_lane(self, old128, value, width):
        """the low `width` bits replaced, the rest of the register
        preserved -- the merge rule every scalar (`ss`/`sd`) form
        follows."""
        if width == 128:
            return value
        high = z3.Extract(127, width, old128)
        return z3.Concat(high, value)

    def zero_extend_to_128(self, value):
        pad = 128 - value.size()
        return z3.ZeroExt(pad, value)

    # -- memory -------------------------------------------------------

    def mem_key(self, operand):
        return "MEM:" + operand

    def read_mem(self, operand, width):
        """a memory read at a LITERAL operand spelling. Stack operands
        (`-0x8(%rsp)`) read back whatever this same text stored there;
        an unwritten cell gets one fresh symbol shared through
        `shared_seed`, so both texts start from the same state."""
        key = self.mem_key(operand)
        if key in self.regs:
            cell = self.regs[key]
        else:
            if key not in self.shared_seed:
                self.shared_seed[key] = z3.BitVec(
                    "seed_%s" % key.replace("%", "").replace("(", "_")
                    .replace(")", "_").replace(",", "_")
                    .replace("-", "m").replace(":", "_"), 128)
            cell = self.shared_seed[key]
            self.regs[key] = cell
        return z3.Extract(width - 1, 0, cell)

    def write_mem(self, operand, value):
        key = self.mem_key(operand)
        if value.size() == 128:
            self.regs[key] = value
            return
        pad = 128 - value.size()
        self.regs[key] = z3.ZeroExt(pad, value)

    def rip_constant(self, mnem, width):
        """the k-th rip-relative READ in this text gets the k-th fresh
        constant symbol. The driver's mnemonic-order guard is what
        makes the two texts' k-th reads the same constant; without
        that guard passing, the unit is never gated."""
        idx = self.rip_reads
        self.rip_reads = self.rip_reads + 1
        self.rip_mnem_order.append(mnem)
        name = "ripconst_%d" % idx
        if name not in self.shared_seed:
            self.shared_seed[name] = z3.BitVec(name, 128)
        full = self.shared_seed[name]
        if width == 128:
            return full
        return z3.Extract(width - 1, 0, full)

    def is_memory_operand(self, operand):
        if operand.startswith("%"):
            return False
        if operand.startswith("$"):
            return False
        return operand.endswith(")")

    def is_rip_operand(self, operand):
        return "(%rip)" in operand

    # -- reading either kind of source --------------------------------

    def read_src(self, operand, width, mnem):
        """one source operand of a float instruction, at `width` bits:
        an xmm register's low lane, a rip constant, a memory cell, or
        a plain general register."""
        if self.is_xmm(operand):
            return self.lane(self.read_xmm(operand), 0, width)
        if self.is_rip_operand(operand):
            return self.rip_constant(mnem, width)
        if self.is_memory_operand(operand):
            return self.read_mem(operand, width)
        return self.read_at(operand, width)

    def read_src_128(self, operand, mnem):
        if self.is_xmm(operand):
            return self.read_xmm(operand)
        if self.is_rip_operand(operand):
            return self.rip_constant(mnem, 128)
        if self.is_memory_operand(operand):
            key = self.mem_key(operand)
            if key in self.regs:
                return self.regs[key]
            return self.zero_extend_to_128(self.read_mem(operand, 64))
        raise NotModeled(
            "a 128-bit read of operand %r is not modeled" % operand)

    # -- the answer home ----------------------------------------------

    def current_answer(self):
        """the answer, read at the home the GROUND TRUTH names (set by
        the driver from the real ship text). Falls back to Sim9's
        rax-tracking rule when no home was set."""
        if self.answer_family is None:
            return BC9.Sim9.current_answer(self)
        fam_val = self.get_family(self.answer_family)
        width = self.answer_width
        return z3.Extract(width - 1, 0, fam_val), width

    def answer_value(self, text_lines):
        """the straight-line entry point, overriding Sim's linear
        end-of-text rax scan with the same ground-truth-named home."""
        if self.answer_family is None:
            return BC5.Sim.answer_value(self, text_lines)
        for line in text_lines:
            if line.strip() == "":
                continue
            if line.strip() == "ret":
                continue
            self.exec_line(line)
        return self.current_answer()

    # -- the float flag rule ------------------------------------------

    def cond_bool(self, suffix):
        """float flags win when the most recent flag-setter was a
        `ucomiss`/`ucomisd`; otherwise the inherited integer path."""
        if self.last_fcmp is None:
            return BC9.Sim9.cond_bool(self, suffix)
        width, left, right = self.last_fcmp
        unord = FUNORD[width](left, right)
        lt = FLT[width](left, right)
        eq = FEQ[width](left, right)
        zf = z3.Or(unord, eq)
        pf = unord
        cf = z3.Or(unord, lt)
        if suffix in ("a", "nbe"):
            return z3.And(z3.Not(cf), z3.Not(zf))
        if suffix in ("ae", "nb", "nc"):
            return z3.Not(cf)
        if suffix in ("b", "c", "nae"):
            return cf
        if suffix in ("be", "na"):
            return z3.Or(cf, zf)
        if suffix in ("e", "z"):
            return zf
        if suffix in ("ne", "nz"):
            return z3.Not(zf)
        if suffix in ("p", "pe"):
            return pf
        if suffix in ("np", "po"):
            return z3.Not(pf)
        raise NotModeled(
            "branch/set suffix %r has no float-flag model" % suffix)

    # -- the instruction table ----------------------------------------

    def exec_line(self, line):
        line = line.strip()
        if "!!" in line:
            line = line.split("!!", 1)[0].strip()
        if line == "":
            return
        parts = line.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        handled = self.exec_float_line(mnem, rest)
        if handled:
            return
        BC9.Sim9.exec_line(self, line)

    def exec_float_line(self, mnem, rest):
        """True when this file's own table handled the instruction."""
        operands = split_operands(rest)

        # --- full-width and lane-merging copies ---------------------
        if mnem in ("movaps", "movapd", "movups", "movupd"):
            src, dst = operands
            value = self.read_src_128(src, mnem)
            if self.is_xmm(dst):
                self.write_xmm(dst, value)
                return True
            self.write_mem(dst, value)
            return True

        if mnem in ("movss", "movsd"):
            src, dst = operands
            width = width_of_float_mnem(mnem)
            value = self.read_src(src, width, mnem)
            if self.is_xmm(dst):
                if self.is_xmm(src):
                    old = self.read_xmm(dst)
                    self.write_xmm(
                        dst, self.set_low_lane(old, value, width))
                    return True
                self.write_xmm(
                    dst, self.zero_extend_to_128(value))
                return True
            self.write_mem(dst, value)
            return True

        if mnem in ("movd", "movq"):
            src, dst = operands
            width = width_of_float_mnem(mnem)
            src_is_x = self.is_xmm(src)
            dst_is_x = self.is_xmm(dst)
            if not src_is_x and not dst_is_x:
                return False
            value = self.read_src(src, width, mnem)
            if dst_is_x:
                self.write_xmm(dst, self.zero_extend_to_128(value))
                return True
            if self.is_memory_operand(dst):
                self.write_mem(dst, value)
                return True
            self.write(dst, value)
            return True

        # --- scalar float arithmetic --------------------------------
        if len(mnem) > 2 and mnem[:-2] in ARITH_FN:
            suffix = mnem[-2:]
            if suffix in ("ss", "sd"):
                width = 32 if suffix == "ss" else 64
                fn = ARITH_FN[mnem[:-2]][width]
                src, dst = operands
                a = self.lane(self.read_xmm(dst), 0, width)
                b = self.read_src(src, width, mnem)
                r = fn(a, b)
                old = self.read_xmm(dst)
                self.write_xmm(dst, self.set_low_lane(old, r, width))
                return True
            if suffix in ("ps", "pd"):
                width = 32 if suffix == "ps" else 64
                fn = ARITH_FN[mnem[:-2]][width]
                src, dst = operands
                dst_v = self.read_xmm(dst)
                src_v = self.read_src_128(src, mnem)
                lanes = []
                count = 128 // width
                for i in range(count):
                    a = self.lane(dst_v, i, width)
                    b = self.lane(src_v, i, width)
                    lanes.append(fn(a, b))
                lanes.reverse()
                self.write_xmm(dst, z3.Concat(*lanes))
                return True
            return False

        # --- lane comparison masks ----------------------------------
        if mnem in ("cmpeqss", "cmpeqsd", "cmpneqss", "cmpneqsd"):
            width = 32 if mnem.endswith("ss") else 64
            src, dst = operands
            a = self.lane(self.read_xmm(dst), 0, width)
            b = self.read_src(src, width, mnem)
            eq = FEQ[width](a, b)
            unord = FUNORD[width](a, b)
            if mnem.startswith("cmpeq"):
                taken = z3.And(eq, z3.Not(unord))
            else:
                taken = z3.Not(z3.And(eq, z3.Not(unord)))
            ones = z3.BitVecVal(-1, width)
            zero = z3.BitVecVal(0, width)
            mask = z3.If(taken, ones, zero)
            old = self.read_xmm(dst)
            self.write_xmm(dst, self.set_low_lane(old, mask, width))
            return True

        # --- conversions ---------------------------------------------
        if mnem in ("cvtsi2ss", "cvtsi2sd", "cvtsi2ssl", "cvtsi2sdl",
                    "cvtsi2ssq", "cvtsi2sdq"):
            dst_width = 32 if "ss" in mnem else 64
            src, dst = operands
            if self.is_memory_operand(src):
                raise NotModeled(
                    "cvtsi2* from memory operand %r is not modeled"
                    % src)
            src_width = BC5.Sim.width_of_operand(self, src)
            if src_width not in (32, 64):
                raise NotModeled(
                    "cvtsi2* from a %d-bit source is not modeled"
                    % src_width)
            a = self.read_at(src, src_width)
            r = FCVT_I2F[(src_width, dst_width)](a)
            old = self.read_xmm(dst)
            self.write_xmm(
                dst, self.set_low_lane(old, r, dst_width))
            return True

        if mnem == "cvtss2sd":
            src, dst = operands
            a = self.read_src(src, 32, mnem)
            r = FCVT_F32_F64(a)
            old = self.read_xmm(dst)
            self.write_xmm(dst, self.set_low_lane(old, r, 64))
            return True

        # --- lane shuffles -------------------------------------------
        if mnem == "punpckldq":
            src, dst = operands
            dst_v = self.read_xmm(dst)
            src_v = self.read_src_128(src, mnem)
            d0 = self.lane(dst_v, 0, 32)
            s0 = self.lane(src_v, 0, 32)
            d1 = self.lane(dst_v, 1, 32)
            s1 = self.lane(src_v, 1, 32)
            self.write_xmm(dst, z3.Concat(s1, d1, s0, d0))
            return True

        if mnem == "unpckhpd":
            src, dst = operands
            dst_v = self.read_xmm(dst)
            src_v = self.read_src_128(src, mnem)
            d1 = self.lane(dst_v, 1, 64)
            s1 = self.lane(src_v, 1, 64)
            self.write_xmm(dst, z3.Concat(s1, d1))
            return True

        if mnem == "unpcklpd":
            src, dst = operands
            dst_v = self.read_xmm(dst)
            src_v = self.read_src_128(src, mnem)
            d0 = self.lane(dst_v, 0, 64)
            s0 = self.lane(src_v, 0, 64)
            self.write_xmm(dst, z3.Concat(s0, d0))
            return True

        if mnem in ("xorps", "xorpd", "pxor"):
            src, dst = operands
            dst_v = self.read_xmm(dst)
            src_v = self.read_src_128(src, mnem)
            self.write_xmm(dst, dst_v ^ src_v)
            return True

        # --- float flag CONSUMERS -------------------------------------
        # setcc/cmovcc after a ucomiss/ucomisd. The inherited ExtSim
        # handlers refuse ("setcc with no preceding cmp/test") because
        # they look only at the INTEGER `last_cmp`; when a float
        # compare is the live flag setter, the flags come from the
        # float rule in cond_bool instead. Measured cause: all 32
        # units this file left UNDECIDED on its first run reported
        # exactly that one refusal.
        if self.last_fcmp is not None:
            if mnem.startswith("set") and len(mnem) > 3:
                (dst,) = operands
                pred = self.cond_bool(mnem[3:])
                one = z3.BitVecVal(1, 8)
                zero = z3.BitVecVal(0, 8)
                self.write(dst, z3.If(pred, one, zero))
                return True
            if mnem.startswith("cmov") and len(mnem) > 4:
                src, dst = operands
                pred = self.cond_bool(mnem[4:])
                width = self.width_of_operand(dst)
                old_v = self.read_at(dst, width)
                new_v = self.read_at(src, width)
                self.write(dst, z3.If(pred, new_v, old_v))
                return True

        # --- float flag setters ---------------------------------------
        if mnem in ("ucomiss", "ucomisd", "comiss", "comisd"):
            width = 32 if mnem.endswith("ss") else 64
            src, dst = operands
            left = self.lane(self.read_xmm(dst), 0, width)
            right = self.read_src(src, width, mnem)
            self.last_fcmp = (width, left, right)
            self.last_cmp = None
            return True

        # an integer flag setter clears any float compare, so the
        # inherited integer path is used again from here.
        if mnem in ("cmp", "test"):
            self.last_fcmp = None
            return False

        return False


# ---------------------------------------------------------------
# the answer home, read off the real ship text
# ---------------------------------------------------------------

def answer_home_from_real(real_lines):
    """(family, width) -- the register the unit's OWN REAL SHIP CODE
    leaves its answer in, and the width its own last answer-writing
    instruction used. Returns (None, None) when the real text never
    writes either candidate home."""
    home = None
    width = None
    for raw in real_lines:
        line = raw.strip()
        if "!!" in line:
            line = line.split("!!", 1)[0].strip()
        if line == "":
            continue
        if line.endswith(":"):
            continue
        parts = line.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        if mnem in ("ret", "jmp", "ud2", "call"):
            continue
        if mnem.startswith("j") and len(mnem) > 1:
            continue
        operands = split_operands(rest)
        if not operands:
            continue
        dst = operands[-1]
        if not dst.startswith("%"):
            continue
        name = dst[1:]
        fam = canon.FAMILY_OF.get(name)
        if fam is None:
            continue
        if fam == "xmm0":
            home = "xmm0"
            w = width_of_float_mnem(mnem)
            if w is None:
                w = 64
            width = w
            continue
        if fam == "rax":
            home = "rax"
            code = canon.WIDTH_OF.get(name)
            if code is None:
                continue
            width = BC5.WIDTH_BITS[code]
            continue
    return home, width


def rip_mnemonic_order(lines):
    """the ordered list of mnemonics carrying a rip-relative operand
    -- the guard the two texts must agree on before any positional
    constant keying is allowed."""
    out = []
    for raw in lines:
        line = raw.strip()
        if "!!" in line:
            line = line.split("!!", 1)[0].strip()
        if line == "" or line.endswith(":"):
            continue
        if "(%rip)" not in line:
            continue
        out.append(line.split(" ", 1)[0])
    return out


def all_lines_of_blocks(block_list):
    out = []
    for b in block_list:
        for s in b["steps"]:
            out.append(s)
    return out


# ---------------------------------------------------------------
# the two gates -- straight-line and branching
# ---------------------------------------------------------------

def _prepare_seed(lang, n, sem_docs):
    a_fam, b_fam = BC8.real_arg_families(lang, n, sem_docs)
    shared_seed = {}
    if a_fam is not None and a_fam != "rdi":
        shared_seed[a_fam] = BC8.seed_family(shared_seed, "rdi")
    if b_fam is not None and b_fam != "rsi":
        shared_seed[b_fam] = BC8.seed_family(shared_seed, "rsi")
    return shared_seed


def anchored_check_straight(lang, n, canon4_docs, sem_docs,
                            candidate_text):
    real_text = BC8.real_text_of(lang, n, canon4_docs)
    if real_text is None:
        return "UNDECIDED", "no real ship mnem recorded for this " \
            "unit (canon4_units's own `mnem` field is empty/missing)"
    lines_real = [ln.strip() for ln in real_text.split(";")]
    lines_cand = [ln.strip() for ln in candidate_text.split(";")]
    order_real = rip_mnemonic_order(lines_real)
    order_cand = rip_mnemonic_order(lines_cand)
    if order_real != order_cand:
        return "UNDECIDED", "the rip-relative constant guard " \
            "refused: real text loads constants at %r, candidate at " \
            "%r -- positional constant keying is not sound here" \
            % (order_real, order_cand)
    home, width = answer_home_from_real(lines_real)
    if home is None:
        return "UNDECIDED", "the unit's own real ship code never " \
            "writes %xmm0 or an rax-family register, so no answer " \
            "home can be read off the ground truth"
    shared_seed = _prepare_seed(lang, n, sem_docs)
    sim_real = Sim10(shared_seed, "real")
    sim_cand = Sim10(shared_seed, "cand")
    sim_real.answer_family = home
    sim_real.answer_width = width
    sim_cand.answer_family = home
    sim_cand.answer_width = width
    try:
        val_real, w_real = sim_real.answer_value(lines_real)
        val_cand, w_cand = sim_cand.answer_value(lines_cand)
    except NotModeled as exc:
        return "UNDECIDED", str(exc)
    return _finish(val_real, w_real, val_cand, w_cand, home, width)


def anchored_check_branching(lang, n, canon4_docs, sem_docs):
    rec = canon4_docs[lang].get(n)
    if rec is None:
        return "UNDECIDED", "no canon4_units record for this unit"
    real_block_list = rec.get("blocks")
    cand_block_list = rec.get("derived_blocks")
    if not real_block_list or not cand_block_list:
        return "UNDECIDED", "no block-structured real/derived text " \
            "recorded for this unit"
    lines_real = all_lines_of_blocks(real_block_list)
    lines_cand = all_lines_of_blocks(cand_block_list)
    order_real = rip_mnemonic_order(lines_real)
    order_cand = rip_mnemonic_order(lines_cand)
    if order_real != order_cand:
        return "UNDECIDED", "the rip-relative constant guard " \
            "refused: real text loads constants at %r, candidate at " \
            "%r" % (order_real, order_cand)
    home, width = answer_home_from_real(lines_real)
    if home is None:
        return "UNDECIDED", "the unit's own real ship code never " \
            "writes %xmm0 or an rax-family register"
    shared_seed = _prepare_seed(lang, n, sem_docs)
    real_blocks = {}
    for b in real_block_list:
        real_blocks[b["label"]] = b["steps"]
    cand_blocks = {}
    for b in cand_block_list:
        cand_blocks[b["label"]] = b["steps"]
    real_order = [b["label"] for b in real_block_list]
    cand_order = [b["label"] for b in cand_block_list]
    sim_real = Sim10(shared_seed, "real")
    sim_cand = Sim10(shared_seed, "cand")
    sim_real.answer_family = home
    sim_real.answer_width = width
    sim_cand.answer_family = home
    sim_cand.answer_width = width
    try:
        val_real = BC9.run_flow(sim_real, real_blocks,
                                real_block_list[0]["label"],
                                order=real_order)
        val_cand = BC9.run_flow(sim_cand, cand_blocks,
                                cand_block_list[0]["label"],
                                order=cand_order)
    except Trap:
        return "UNDECIDED", "both control-flow walks trapped " \
            "unconditionally -- no answer value on either side"
    except NotModeled as exc:
        return "UNDECIDED", str(exc)
    v_r, w_r = val_real
    v_c, w_c = val_cand
    return _finish(v_r, w_r, v_c, w_c, home, width)


# ---------------------------------------------------------------
# a state-complete branch walker
# ---------------------------------------------------------------
#
# canon9_behaviour_check.run_from saves and restores exactly four
# pieces of simulator state across a conditional branch: `regs`,
# `last_flags`, `last_cmp` and `rax_write_width`. Two more exist and
# were not saved: Sim7's `push_stack` and this file's `last_fcmp` and
# `rip_reads`. Measured effect (go/op_96, go/op_132): after the taken
# side runs to a `pop`, the fall-through side finds the push stack
# already emptied and the whole unit is refused "pop with an empty
# symbolic push stack". This walker saves EVERY instance attribute
# instead of a hand-listed four, so a state addition can never again
# leak across a branch.


def snapshot(sim):
    state = {}
    for key, value in vars(sim).items():
        if isinstance(value, dict):
            state[key] = dict(value)
            continue
        if isinstance(value, list):
            state[key] = list(value)
            continue
        state[key] = value
    return state


def restore(sim, state):
    for key, value in state.items():
        setattr(sim, key, value)


def walk(sim, blocks, label, depth=0, order=None):
    if depth > 60:
        raise NotModeled(
            "control flow recursion exceeded 60 -- possible loop, "
            "not modeled by this straight-DAG-only walker")
    steps = blocks.get(label)
    if steps is None:
        raise NotModeled(
            "branch target label %r has no block recorded" % label)
    return walk_from(sim, blocks, label, steps, 0, depth, order)


def walk_from(sim, blocks, label, steps, idx, depth, order):
    while idx < len(steps):
        line = steps[idx].strip()
        if line == "":
            idx = idx + 1
            continue
        if line.endswith(":"):
            idx = idx + 1
            continue
        parts = line.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        if mnem == "ud2":
            raise Trap()
        if mnem == "call":
            raise Trap()
        if mnem == "ret":
            return sim.current_answer()
        if mnem == "jmp":
            target = rest.strip()
            return walk(sim, blocks, target, depth + 1, order)
        if mnem.startswith("j") and len(mnem) > 1:
            suffix = mnem[1:]
            target = rest.strip()
            pred = sim.cond_bool(suffix)
            saved = snapshot(sim)
            trapped_taken = False
            val_taken = None
            try:
                val_taken = walk(sim, blocks, target, depth + 1,
                                 order)
            except Trap:
                trapped_taken = True
            restore(sim, saved)
            trapped_fall = False
            val_fall = None
            try:
                val_fall = walk_from(sim, blocks, label, steps,
                                     idx + 1, depth + 1, order)
            except Trap:
                trapped_fall = True
            if trapped_taken and trapped_fall:
                raise Trap()
            if trapped_taken:
                return val_fall
            if trapped_fall:
                return val_taken
            v_t, w_t = val_taken
            v_f, w_f = val_fall
            w = min(w_t, w_f)
            if w_t != w_f:
                v_t = z3.Extract(w - 1, 0, v_t)
                v_f = z3.Extract(w - 1, 0, v_f)
            merged = z3.If(pred, v_t, v_f)
            return merged, w
        sim.exec_line(line)
        idx = idx + 1
    if order and label in order:
        pos = order.index(label)
        if pos + 1 < len(order):
            return walk(sim, blocks, order[pos + 1], depth + 1,
                        order)
    raise NotModeled(
        "block %r fell off its own end without ret/jmp/trap and has "
        "no next block in compiled order to fall through to" % label)


def anchored_check_branching_real(lang, n, canon4_docs, op_docs,
                                  sem_docs):
    """the branching gate against the unit's REAL control-flow blocks,
    cut from its own ship bytes by real_blocks.build.

    This replaces anchored_check_branching, which reads
    canon4_units's `blocks` field as if it were ground truth. It is
    not: canon4.py assigns `blocks` and `derived_blocks` the same list
    object, so that gate compares a text with itself. See
    real_blocks.py's header for the measured evidence."""
    rec = canon4_docs[lang].get(n)
    if rec is None:
        return "UNDECIDED", "no canon4_units record for this unit"
    cand_block_list = rec.get("derived_blocks")
    if not cand_block_list:
        return "UNDECIDED", "no derived_blocks candidate on this " \
            "unit's record"
    probe = op_docs[lang].get(n)
    if probe is None:
        return "UNDECIDED", "no op_units probe record for this unit"
    ship = probe.get("ship") or {}
    ship_bytes = ship.get("bytes")
    ship_mnem = ship.get("mnem")
    if not ship_bytes or not ship_mnem:
        return "UNDECIDED", "the op_units probe record carries no " \
            "ship bytes/mnem for this unit"
    try:
        real_block_list = real_blocks.build(ship_bytes, ship_mnem)
    except real_blocks.NotCuttable as exc:
        return "UNDECIDED", "real control-flow blocks could not be " \
            "cut from this unit's own ship bytes: %s" % exc
    lines_real = all_lines_of_blocks(real_block_list)
    lines_cand = all_lines_of_blocks(cand_block_list)
    order_real = rip_mnemonic_order(lines_real)
    order_cand = rip_mnemonic_order(lines_cand)
    if order_real != order_cand:
        return "UNDECIDED", "the rip-relative constant guard " \
            "refused: real text loads constants at %r, candidate at " \
            "%r" % (order_real, order_cand)
    home, width = answer_home_from_real(lines_real)
    if home is None:
        return "UNDECIDED", "the unit's own real ship code never " \
            "writes %xmm0 or an rax-family register"
    shared_seed = _prepare_seed(lang, n, sem_docs)
    real_map = {}
    for b in real_block_list:
        real_map[b["label"]] = b["steps"]
    cand_map = {}
    for b in cand_block_list:
        cand_map[b["label"]] = b["steps"]
    real_order = [b["label"] for b in real_block_list]
    cand_order = [b["label"] for b in cand_block_list]
    sim_real = Sim10(shared_seed, "real")
    sim_cand = Sim10(shared_seed, "cand")
    sim_real.answer_family = home
    sim_real.answer_width = width
    sim_cand.answer_family = home
    sim_cand.answer_width = width
    try:
        val_real = walk(sim_real, real_map,
                        real_block_list[0]["label"],
                        order=real_order)
        val_cand = walk(sim_cand, cand_map,
                        cand_block_list[0]["label"],
                        order=cand_order)
    except Trap:
        return "UNDECIDED", "both control-flow walks trapped " \
            "unconditionally -- no answer value on either side"
    except NotModeled as exc:
        return "UNDECIDED", str(exc)
    v_r, w_r = val_real
    v_c, w_c = val_cand
    return _finish(v_r, w_r, v_c, w_c, home, width)


def _finish(val_real, w_real, val_cand, w_cand, home, width):
    if w_real != w_cand:
        w = min(w_real, w_cand)
        val_real = z3.Extract(w - 1, 0, val_real)
        val_cand = z3.Extract(w - 1, 0, val_cand)
    solver = z3.Solver()
    solver.add(val_real != val_cand)
    result = solver.check()
    if result == z3.unsat:
        return "PROVED_EQUAL", (
            "z3 proved this text equal to the unit's own real ship "
            "code in the ground-truth-named answer home %%%s at %d "
            "bits, for every value of every register either text "
            "reads before writing and for EVERY interpretation of "
            "the uninterpreted float operations"
            % (home, width))
    if result == z3.sat:
        model = solver.model()
        return "DISPROVED", (
            "z3 found a counterexample under which this text and the "
            "unit's own real ship code compute DIFFERENT answers in "
            "%%%s: %s" % (home, model))
    return "UNDECIDED", "z3 returned %r" % result
