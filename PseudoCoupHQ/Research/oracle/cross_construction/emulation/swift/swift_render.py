#!/usr/bin/env python3
"""swift_render.py -- task g1: AutoPoly with SWIFT as the target.

Node: hq.research.arch_unit_oracle.cross_construction
(`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/CORE_0_3_2_2_cross_construction.md`).

READ THIS FIRST -- WHAT IS AND IS NOT ATTESTED IN THIS FILE.
There is NO swift toolchain in the image this task ran under.  Lane
`g1_l1_toolchains.sh` asked `/persist/swift/usr/bin/swiftc --version`
-- the path `lane_gen.py` names for every swift unit of the corpus --
and the shell answered, LITERAL:

    /drop/g1_l1_toolchains.sh: line 28: /persist/swift/usr/bin/swiftc:
    No such file or directory

and lane `g1_l2_swift_where.sh` then found `/persist` empty, no
`swiftc` anywhere on the image's own filesystem, and no
`libncurses.so.6` (only `libncursesw.so.6`).  So:

  * EVERY SWIFT ROW OF THIS TASK'S DELIVERABLE IS REFUSED, with that
    literal text as its cause.  No workaround was attempted -- no
    LD_LIBRARY_PATH, no copied library, no substitute compiler -- as
    the brief requires.
  * EVERY SPELLING IN THIS FILE IS UNMEASURED.  Task o11 section 3.1's
    rule is that a target's behaviour is read off its own emission
    before a spelling is written, and three of task o11's twenty rust
    spellings changed when it was.  Nothing here has been through that,
    so each rule below carries the marker UNMEASURED and cites the
    language reference rather than a probe.  Under the evidence
    doctrine that is the WEAKEST class -- "human interpretation of
    stated design" -- and it is labelled as such on every row rather
    than presented as a measurement.
  * The file exists because the brief asks for it: "the swift renderer
    is written and probed as far as compile-free checks allow".  The
    compile-free check it does get is that it RENDERS: every place of
    every cell this task runs is put through it, and whether it writes
    source or refuses by cause is on the record.  What that record does
    NOT establish is that the source it writes compiles, or that what
    swiftc would emit for it is what these comments say.

THE OBJECTS, one sentence each, in relation.
  * A TERM is one place of one arch-opcode written as a z3 expression
    over `seed_<register family>` symbols.
  * AN EMULATION is a swift file whose one exported function's body is
    that term written in swift's own operations over swift's holders,
    produced by the ONE renderer below (`SwiftRenderer`, which DERIVES
    from task o7's `emulate.Renderer`).
  * THE SHIP BUILD would be `swiftc -O -c`, read off `lane_gen.py`'s
    swift branch, with the symbol exported by `@_cdecl` -- which is
    also the corpus's own shape (`probe_gen.emit_swift`).  It is not
    run by this task, because there is no swiftc to run it.

WHAT IS REUSED RATHER THAN COPIED, said out loud.  Nothing under
`Research/op_pipeline/` is edited and `emulate.py` is imported, never
forked: `emulate.Renderer` is DERIVED FROM, and the width planning, the
free-symbol check and the refusal causes are inherited unchanged.
Swift's arrival contract is the SysV one (`canon37_gate.sequences_for`
answers with the SysV sequence for every language except go), so
`emulate.recorded_facts` and `emulate.expected_c_families` apply
unchanged and are called rather than restated -- the one place this
target is simpler than go.

MEMORY BOUND: this file allocates nothing of its own and runs inside
the driver's one collecting process under its stated 4 GB resident
bound and named abort ABORT_MEMORY_G1.

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

Nothing here keys, groups, pairs or selects anything.  This file is a
printer: a z3 declaration kind goes in and swift source comes out.  The
swift operator tokens in the strings below are the OUTPUT TEXT of that
printer and are read by no machinery of this line.

Coding discipline: no compound one-liner statements.

usage:
  swift_render.py flags    the ship flags and their source, LITERAL
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
EMULATION = os.path.normpath(os.path.join(HERE, ".."))
CROSS = os.path.normpath(os.path.join(HERE, "..", ".."))
OP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                   "op_pipeline"))
sys.path.insert(0, OP)
sys.path.insert(0, CROSS)
sys.path.insert(0, EMULATION)

import z3                                                        # noqa: E402
import emulate as E                                              # noqa: E402

SRC_DIR = os.path.join(HERE, "src")
HOST_FOLDER = ("~/Programming/PseudoCoupHQ/Research/oracle/"
               "cross_construction/emulation/swift")

TARGET = "swift"
# `lane_gen.py` line 290, LITERAL: SWIFTC = "/persist/swift/usr/bin/swiftc"
SWIFTC = "/persist/swift/usr/bin/swiftc"
SHIP_FLAGS = ["-O", "-c"]
SHIP_FLAGS_SOURCE = ("lane_gen.py compile_probe, swift branch: "
                     "`opt = [\"-Onone\", \"-g\"] if mode == \"anchor\" "
                     "else [\"-O\"]`; `cmd = [SWIFTC] + opt + [\"-c\", "
                     "src, \"-o\", obj]` -- the ship build of every "
                     "swift unit in the corpus")

# swift's holders.  UNMEASURED, every row: the language reference, not
# a probe, because there is no swiftc in this image.  `Float16` and the
# 128-bit holders are refused rather than spelled, because whether this
# toolchain has them is exactly the sort of thing task o11's rust
# probes settled by measurement (rustc 1.96.1 refuses `f16` as
# unstable) and nothing here can settle it.
SU = {8: "UInt8", 16: "UInt16", 32: "UInt32", 64: "UInt64"}
SI = {8: "Int8", 16: "Int16", 32: "Int32", 64: "Int64"}
SF = {32: "Float", 64: "Double"}
PARAM_NAMES = E.PARAM_NAMES

NO_WIDE = ("swift's %d-bit integer holder is not spelled by this "
           "renderer: whether this toolchain has Int128/UInt128 is "
           "UNMEASURED, there being no swiftc in the image")
NO_F16 = ("swift's %d-bit float holder is not spelled by this "
          "renderer: whether this toolchain has Float16 on x86-64 "
          "linux is UNMEASURED, there being no swiftc in the image")


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def swiftc_answer():
    """what running swiftc actually does, on the machine this runs on:
    the literal answer, whatever it is.  This is the cause every swift
    row of the deliverable carries, and it is re-read at run time rather
    than pasted from a previous lane."""
    try:
        done = subprocess.run([SWIFTC, "--version"],
                              capture_output=True, text=True,
                              timeout=120)
    except OSError as problem:
        return "%s: %s" % (SWIFTC, problem.strerror)
    except Exception as problem:                             # noqa: BLE001
        return "%s raised %s: %s" % (SWIFTC, type(problem).__name__,
                                     problem)
    if done.returncode != 0:
        text = (done.stderr or done.stdout).strip()
        return "%s exited %d: %s" % (SWIFTC, done.returncode,
                                     text.splitlines()[0] if text
                                     else "(no diagnostic)")
    return (done.stdout or done.stderr).strip().splitlines()[0]


# ==================================================================
# section 1: SWIFT SOURCE PIECES   holders, literals, masks, sign
# ==================================================================

def su(bits):
    if bits not in SU:
        raise E.Refused(E.CAUSE_WIDTH, NO_WIDE % bits)
    return SU[bits]


def si(bits):
    if bits not in SI:
        raise E.Refused(E.CAUSE_WIDTH, NO_WIDE % bits)
    return SI[bits]


def sf(bits):
    if bits not in SF:
        raise E.Refused(E.CAUSE_WIDTH, NO_F16 % bits)
    return SF[bits]


def slit(value, bits):
    return "%s(0x%x)" % (su(bits), value & ((1 << bits) - 1))


def smask(text, width):
    """`text`, of the promoted unsigned holder of `width`, with the
    bits above `width` cleared.

    UNMEASURED.  `UInt64(truncatingIfNeeded:)` is swift's own
    non-trapping conversion between fixed-width holders; the plain
    `UInt64(_:)` TRAPS when the value does not fit, which would put a
    trap in every intermediate step of a rendered term rather than only
    where the opcode itself has one."""
    bits = E.promoted_bits(width)
    if width == bits:
        return "(%s(truncatingIfNeeded: %s))" % (su(bits), text)
    return "((%s(truncatingIfNeeded: %s)) & %s)" % (
        su(bits), text, slit((1 << width) - 1, bits))


def ssign(text, width, bits):
    """`text` (the low `width` bits of the promoted unsigned holder) as
    a SIGNED value of the holder of `bits`, sign bit `width - 1`
    propagated.

    UNMEASURED.  `&<<` and `&>>` are swift's MASKING shift operators,
    which mask the count to the width rather than trapping on an
    out-of-range one; `>>` on a signed holder is arithmetic."""
    if width == bits:
        return "(%s(bitPattern: %s))" % (si(bits), text)
    shift = bits - width
    return "(((%s(bitPattern: %s)) &<< %d) &>> %d)" % (
        si(bits), text, shift, shift)


# ==================================================================
# section 2: THE RENDERER   z3 term -> swift source
# ==================================================================

class SwiftRenderer(E.Renderer):
    """the ONE swift renderer: a z3 term over `seed_<family>` symbols ->
    one swift file.  DERIVES from task o7's `emulate.Renderer`; the
    width planning, the free-symbol check and the refusal causes are
    inherited unchanged.

    EVERY SPELLING IS UNMEASURED -- see this file's own header.

    attributes:
        families        the term's arrival families, IN order
        result_family   the answer home
        result_width    its width in bits
        params          per family: name, holder text, kind, bits
    methods:
        render          -> (source text, function symbol)
        emit            one node -> (text, kind, width)
    """

    def __init__(self, families, result_family, result_width, label):
        E.Renderer.__init__(self, families, result_family, result_width,
                            label)

    def plan_parameters(self, term):
        E.Renderer.plan_parameters(self, term)
        for param in self.params:
            if param["kind"] == "fp":
                param["holder"] = sf(param["bits"])
                continue
            param["holder"] = su(param["bits"])

    def render(self, term, text):
        """the whole swift file.  `@_cdecl` gives the function the C
        symbol the carve would ask objdump for, which is the corpus's
        own shape (`probe_gen.emit_swift`)."""
        self.plan_parameters(term)
        self.check_symbols(term)
        root_text, root_kind, root_width = self.emit(term)
        return_type, body = self.answer(root_text, root_kind, root_width)
        symbol = "emu_%s" % self.label
        params = []
        for param in self.params:
            params.append("_ %s: %s" % (param["name"], param["holder"]))
        lines = []
        lines.append("// task g1 emulation -- rendered by "
                     "swift_render.py")
        lines.append("// SwiftRenderer from the layer-4 term of %s."
                     % self.label)
        lines.append("// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: "
                     "there is no swiftc in")
        lines.append("// the image, so nothing here has been compiled "
                     "or carved.")
        lines.append("// The term's layer-5 text, LITERAL:")
        lines.append("//   %s" % " ".join(text.split()))
        lines.append("@_cdecl(\"%s\")" % symbol)
        lines.append("public func %s(%s) -> %s"
                     % (symbol, ", ".join(params), return_type))
        lines.append("{")
        lines.append("    return %s" % body)
        lines.append("}")
        lines.append("")
        return "\n".join(lines), symbol

    def answer(self, root_text, root_kind, root_width):
        import reference as R
        family = self.result_family
        width = self.result_width
        if family is None or width is None:
            raise E.Refused(E.CAUSE_STATE, "no answer home")
        if family in R.XMM_NAMES:
            return_type = sf(width)
            if root_kind == "fp":
                if root_width != width:
                    raise E.Refused(E.CAUSE_WIDTH,
                                    "fp answer %d bits, home %d"
                                    % (root_width, width))
                return return_type, root_text
            if root_kind == "bool":
                raise E.Refused(E.CAUSE_OP,
                                "a truth value in a float answer home")
            return return_type, "%s(bitPattern: %s(truncatingIfNeeded" \
                                ": %s))" % (return_type, su(width),
                                            root_text)
        if family.startswith("st") or family.startswith("x87"):
            raise E.Refused(E.CAUSE_X87, family)
        return_type = su(width)
        if root_kind == "fp":
            return return_type, "%s(truncatingIfNeeded: (%s).bitPattern)" \
                                % (return_type, root_text)
        if root_kind == "bool":
            return return_type, "((%s) ? %s(1) : %s(0))" % (
                root_text, return_type, return_type)
        return return_type, "%s(truncatingIfNeeded: %s)" % (return_type,
                                                            root_text)

    # -- one node -----------------------------------------------------

    def emit(self, node):
        decl = node.decl()
        kind = decl.kind()
        if z3.is_const(node) and kind == z3.Z3_OP_UNINTERPRETED:
            return self.emit_symbol(node, None)
        if kind == z3.Z3_OP_BNUM:
            width = node.size()
            bits = E.promoted_bits(width)
            return slit(node.as_long(), bits), "bv", width
        if kind == z3.Z3_OP_TRUE:
            return "true", "bool", 1
        if kind == z3.Z3_OP_FALSE:
            return "false", "bool", 1
        return E.Renderer.emit(self, node)

    def emit_symbol(self, node, extract):
        name = node.decl().name()
        param = self.params[self.seed_names[name]]
        if param["kind"] == "bv":
            bits = E.promoted_bits(param["bits"])
            text = "(%s(%s))" % (su(bits), param["name"])
            width = param["bits"]
            if extract is None:
                if node.size() != 64:
                    raise E.Refused(E.CAUSE_WIDTH,
                                    "general arrival of %d bits"
                                    % node.size())
                if width < 64:
                    raise E.Refused(E.CAUSE_STATE,
                                    "%s read at 64 bits but planned as "
                                    "%s" % (name, param["holder"]))
                return text, "bv", 64
            high, low = extract
            if low == 0 and high + 1 == width:
                return text, "bv", width
            return smask("(%s) &>> %d" % (text, low), high - low + 1), \
                "bv", high - low + 1
        # a vector arrival planned as a float holder: its bits.
        # UNMEASURED: `bitPattern` is swift's own name for the bits of a
        # float, so no helper of the kind c's renderer writes is needed.
        bits = E.promoted_bits(param["bits"])
        text = "(%s((%s).bitPattern))" % (su(bits), param["name"])
        if extract is None:
            raise E.Refused(E.CAUSE_LANE, name)
        high, low = extract
        if low == 0 and high + 1 == param["bits"]:
            return text, "bv", param["bits"]
        return smask("(%s) &>> %d" % (text, low), high - low + 1), \
            "bv", high - low + 1

    def emit_extract(self, node):
        high, low = node.params()
        child = node.arg(0)
        if z3.is_const(child) and \
                child.decl().kind() == z3.Z3_OP_UNINTERPRETED:
            return self.emit_symbol(child, (high, low))
        text, kind, width = self.emit(child)
        self.expect(kind, "bv", node)
        out = high - low + 1
        if low == 0 and out == width:
            return text, "bv", width
        inner_bits = E.promoted_bits(width)
        shifted = "(%s(truncatingIfNeeded: %s)) &>> %d" % (
            su(inner_bits), text, low)
        return smask(shifted, out), "bv", out

    def emit_concat(self, node):
        parts = []
        total = 0
        for index in range(node.num_args()):
            text, kind, width = self.emit(node.arg(index))
            self.expect(kind, "bv", node)
            parts.append((text, width))
            total = total + width
        bits = E.promoted_bits(total)
        pieces = []
        shift = total
        for text, width in parts:
            shift = shift - width
            piece = "((%s(truncatingIfNeeded: %s)) &<< %d)" % (
                su(bits), text, shift)
            if shift == 0:
                piece = "(%s(truncatingIfNeeded: %s))" % (su(bits), text)
            pieces.append(piece)
        return smask(" | ".join(pieces), total), "bv", total

    def emit_extend(self, node, signed):
        extra = node.params()[0]
        text, kind, width = self.emit(node.arg(0))
        self.expect(kind, "bv", node)
        total = width + extra
        bits = E.promoted_bits(total)
        if not signed:
            return "(%s(truncatingIfNeeded: %s))" % (su(bits), text), \
                "bv", total
        return smask(self.sign_extended(text, width, bits), total), \
            "bv", total

    def sign_extended(self, text, width, bits):
        return ssign(text, width, bits)

    def emit_ite(self, node):
        """swift HAS a conditional expression, so unlike go this needs
        no helper.  UNMEASURED."""
        cond, ckind, _ = self.emit(node.arg(0))
        self.expect(ckind, "bool", node)
        left, lkind, lwidth = self.emit(node.arg(1))
        right, rkind, rwidth = self.emit(node.arg(2))
        if lkind != rkind or lwidth != rwidth:
            raise E.Refused(E.CAUSE_OP, "If with arms of different sorts")
        return "((%s) ? (%s) : (%s))" % (cond, left, right), lkind, \
            lwidth

    def emit_logic(self, node, kind):
        args = []
        for index in range(node.num_args()):
            text, akind, _ = self.emit(node.arg(index))
            self.expect(akind, "bool", node)
            args.append("(%s)" % text)
        if kind == z3.Z3_OP_NOT:
            return "(!%s)" % args[0], "bool", 1
        if kind == z3.Z3_OP_AND:
            return "(%s)" % " && ".join(args), "bool", 1
        if kind == z3.Z3_OP_OR:
            return "(%s)" % " || ".join(args), "bool", 1
        if kind == z3.Z3_OP_XOR:
            return "(%s != %s)" % (args[0], args[1]), "bool", 1
        if kind == z3.Z3_OP_IMPLIES:
            return "(!%s || %s)" % (args[0], args[1]), "bool", 1
        return "(%s == %s)" % (args[0], args[1]), "bool", 1

    def emit_equality(self, node, kind):
        left, lkind, lwidth = self.emit(node.arg(0))
        right, rkind, rwidth = self.emit(node.arg(1))
        if lkind == "fp" or rkind == "fp":
            raise E.Refused(E.CAUSE_OP, "structural equality on floats")
        if lkind != rkind or lwidth != rwidth:
            raise E.Refused(E.CAUSE_OP, "equality across sorts")
        if kind == z3.Z3_OP_EQ:
            sign = "=="
        else:
            sign = "!="
        if lkind == "bool":
            return "((%s) %s (%s))" % (left, sign, right), "bool", 1
        bits = E.promoted_bits(lwidth)
        return "((%s(truncatingIfNeeded: %s)) %s (%s(truncatingIfNeeded" \
               ": %s)))" % (su(bits), left, sign, su(bits), right), \
            "bool", 1

    def emit_compare(self, node, kind, signed):
        signs = {
            z3.Z3_OP_SLEQ: "<=", z3.Z3_OP_SLT: "<", z3.Z3_OP_SGEQ: ">=",
            z3.Z3_OP_SGT: ">", z3.Z3_OP_ULEQ: "<=", z3.Z3_OP_ULT: "<",
            z3.Z3_OP_UGEQ: ">=", z3.Z3_OP_UGT: ">",
        }
        left, lkind, lwidth = self.emit(node.arg(0))
        right, rkind, rwidth = self.emit(node.arg(1))
        self.expect(lkind, "bv", node)
        self.expect(rkind, "bv", node)
        if lwidth != rwidth:
            raise E.Refused(E.CAUSE_OP, "comparison across widths")
        bits = E.promoted_bits(lwidth)
        if signed:
            left = ssign(left, lwidth, bits)
            right = ssign(right, rwidth, bits)
        else:
            left = "(%s(truncatingIfNeeded: %s))" % (su(bits), left)
            right = "(%s(truncatingIfNeeded: %s))" % (su(bits), right)
        return "((%s) %s (%s))" % (left, signs[kind], right), "bool", 1

    def emit_arith(self, node, kind):
        """THE MASKING (wrapping) operators `&+ &- &*`.  UNMEASURED.
        Swift's plain `+ - *` TRAP on overflow by the language's own
        definition, which is not the term's meaning; the `&`-prefixed
        forms are swift's own name for the wrapping ones."""
        signs = {
            z3.Z3_OP_BADD: "&+", z3.Z3_OP_BSUB: "&-",
            z3.Z3_OP_BMUL: "&*", z3.Z3_OP_BAND: "&",
            z3.Z3_OP_BOR: "|", z3.Z3_OP_BXOR: "^",
        }
        args = []
        width = None
        for index in range(node.num_args()):
            text, akind, awidth = self.emit(node.arg(index))
            self.expect(akind, "bv", node)
            if width is None:
                width = awidth
            if awidth != width:
                raise E.Refused(E.CAUSE_OP, "arithmetic across widths")
            args.append(text)
        bits = E.promoted_bits(width)
        cast = []
        for text in args:
            cast.append("(%s(truncatingIfNeeded: %s))" % (su(bits), text))
        joined = (" %s " % signs[kind]).join(cast)
        return smask(joined, width), "bv", width

    def emit_unary(self, node, kind):
        """`~x` is swift's bitwise complement; `0 &- x` is the wrapping
        negation, because swift's unary `-` is not defined on an
        unsigned holder at all.  UNMEASURED."""
        text, akind, width = self.emit(node.arg(0))
        self.expect(akind, "bv", node)
        bits = E.promoted_bits(width)
        cast = "(%s(truncatingIfNeeded: %s))" % (su(bits), text)
        if kind == z3.Z3_OP_BNOT:
            return smask("~%s" % cast, width), "bv", width
        return smask("(%s(0) &- %s)" % (su(bits), cast), width), \
            "bv", width

    def emit_shift(self, node, kind):
        """THE MASKING SHIFTS `&<<` and `&>>`.  UNMEASURED.  Swift's
        plain `<<` and `>>` are the "smart" shifts, defined for every
        count (an over-large count answers with the fill) and swift's
        `&<<`/`&>>` mask the count to the width, which is the MACHINE's
        rule.  So, as in c and rust, where the term's count is not
        already bounded the term's own guard is written out, and where
        it is bounded (the model table's own shape) the masking operator
        is the bare instruction.  `emulate.upper_bound` is the same
        bound reader the c and rust renderers use."""
        value, vkind, width = self.emit(node.arg(0))
        amount, akind, awidth = self.emit(node.arg(1))
        self.expect(vkind, "bv", node)
        self.expect(akind, "bv", node)
        bits = E.promoted_bits(width)
        abits = E.promoted_bits(awidth)
        count = "(%s(truncatingIfNeeded: %s))" % (su(abits), amount)
        bound = E.upper_bound(node.arg(1))
        if kind == z3.Z3_OP_BSHL:
            plain = smask("(%s(truncatingIfNeeded: %s)) &<< %s"
                          % (su(bits), value, count), width)
            fill = "%s(0)" % su(bits)
        elif kind == z3.Z3_OP_BLSHR:
            plain = smask("(%s(truncatingIfNeeded: %s)) &>> %s"
                          % (su(bits), value, count), width)
            fill = "%s(0)" % su(bits)
        else:
            signed_value = ssign(value, width, bits)
            plain = smask("%s(bitPattern: (%s) &>> %s)"
                          % (su(bits), signed_value, count), width)
            fill = "(((%s) < 0) ? %s : %s(0))" % (
                signed_value, slit((1 << width) - 1, bits), su(bits))
        if bound is not None and bound < width:
            return plain, "bv", width
        guard = "((%s) < %s)" % (count, slit(width, abits))
        return "((%s) ? (%s) : (%s))" % (guard, plain, fill), "bv", width

    def emit_division(self, node, kind):
        """THE PLAIN DIVIDE, and the EDGE REGION left visible.
        UNMEASURED.  Swift's `/` and `%` on a fixed-width integer trap
        on a zero divisor and on the signed extreme by the language's
        own definition; the brief's rule for this target is to render
        the plain operator and let the gate report the region, so
        neither trap is hidden."""
        left, lkind, lwidth = self.emit(node.arg(0))
        right, rkind, rwidth = self.emit(node.arg(1))
        self.expect(lkind, "bv", node)
        self.expect(rkind, "bv", node)
        if lwidth != rwidth:
            raise E.Refused(E.CAUSE_OP, "division across widths")
        bits = E.promoted_bits(lwidth)
        signed = kind in (z3.Z3_OP_BSDIV, z3.Z3_OP_BSDIV_I,
                          z3.Z3_OP_BSREM, z3.Z3_OP_BSREM_I)
        remainder = kind in (z3.Z3_OP_BUREM, z3.Z3_OP_BUREM_I,
                             z3.Z3_OP_BSREM, z3.Z3_OP_BSREM_I)
        if remainder:
            sign = "%"
        else:
            sign = "/"
        if signed:
            numerator = ssign(left, lwidth, bits)
            divisor = ssign(right, rwidth, bits)
            body = "%s(bitPattern: (%s) %s (%s))" % (su(bits), numerator,
                                                     sign, divisor)
            return smask(body, lwidth), "bv", lwidth
        numerator = "(%s(truncatingIfNeeded: %s))" % (su(bits), left)
        divisor = "(%s(truncatingIfNeeded: %s))" % (su(bits), right)
        return smask("(%s) %s (%s)" % (numerator, sign, divisor),
                     lwidth), "bv", lwidth

    # -- the float family ---------------------------------------------

    def emit_fp(self, node, kind):
        name = node.decl().name()
        if kind == z3.Z3_OP_FPA_RM_NEAREST_TIES_TO_EVEN:
            return "RNE", "rm", 0
        if z3.is_fprm(node):
            raise E.Refused(E.CAUSE_RM, name)
        if z3.is_fp_value(node) or kind in (
                z3.Z3_OP_FPA_PLUS_ZERO, z3.Z3_OP_FPA_MINUS_ZERO,
                z3.Z3_OP_FPA_PLUS_INF, z3.Z3_OP_FPA_MINUS_INF,
                z3.Z3_OP_FPA_NAN, z3.Z3_OP_FPA_NUM):
            width = E.fp_width(node.sort())
            holder = sf(width)
            bits_value = z3.simplify(z3.fpToIEEEBV(node)).as_long()
            return "%s(bitPattern: %s)" % (holder,
                                           slit(bits_value, width)), \
                "fp", width
        if kind == z3.Z3_OP_FPA_TO_FP:
            return self.emit_to_fp(node)
        if kind == z3.Z3_OP_FPA_TO_FP_UNSIGNED:
            self.expect_rne(node.arg(0))
            text, akind, awidth = self.emit(node.arg(1))
            self.expect(akind, "bv", node)
            width = E.fp_width(node.sort())
            bits = E.promoted_bits(awidth)
            return "%s(%s(truncatingIfNeeded: %s))" % (sf(width),
                                                       su(bits), text), \
                "fp", width
        if kind == z3.Z3_OP_FPA_TO_IEEE_BV:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            bits = E.promoted_bits(awidth)
            return "(%s((%s).bitPattern))" % (su(bits), text), \
                "bv", awidth
        if kind in (z3.Z3_OP_FPA_TO_SBV, z3.Z3_OP_FPA_TO_UBV):
            rm = node.arg(0)
            if rm.decl().kind() != z3.Z3_OP_FPA_RM_TOWARD_ZERO:
                raise E.Refused(E.CAUSE_RM,
                                "%s under %s" % (name, rm.decl().name()))
            text, akind, awidth = self.emit(node.arg(1))
            self.expect(akind, "fp", node)
            width = node.size()
            if kind == z3.Z3_OP_FPA_TO_SBV:
                holder = si(width)
            else:
                holder = su(width)
            # UNMEASURED, and the one row where this renderer knows it
            # is on thin ice: swift's `Int64(_: Double)` TRAPS when the
            # value does not fit, where the machine's `cvttsd2si`
            # answers with the "integer indefinite" pattern.  That is an
            # edge region like division's, recorded, not hidden.
            return smask("%s(truncatingIfNeeded: %s(%s))"
                         % (su(E.promoted_bits(width)), holder, text),
                         width), "bv", width
        if kind in (z3.Z3_OP_FPA_ADD, z3.Z3_OP_FPA_SUB,
                    z3.Z3_OP_FPA_MUL, z3.Z3_OP_FPA_DIV):
            signs = {z3.Z3_OP_FPA_ADD: "+", z3.Z3_OP_FPA_SUB: "-",
                     z3.Z3_OP_FPA_MUL: "*", z3.Z3_OP_FPA_DIV: "/"}
            self.expect_rne(node.arg(0))
            left, lkind, lwidth = self.emit(node.arg(1))
            right, rkind, rwidth = self.emit(node.arg(2))
            self.expect(lkind, "fp", node)
            self.expect(rkind, "fp", node)
            if lwidth != rwidth:
                raise E.Refused(E.CAUSE_OP,
                                "float arithmetic across widths")
            return "((%s) %s (%s))" % (left, signs[kind], right), \
                "fp", lwidth
        if kind == z3.Z3_OP_FPA_NEG:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            return "(-(%s))" % text, "fp", awidth
        if kind == z3.Z3_OP_FPA_ABS:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            mask = (1 << (awidth - 1)) - 1
            return "%s(bitPattern: ((%s).bitPattern & %s))" % (
                sf(awidth), text, slit(mask, awidth)), "fp", awidth
        if kind in (z3.Z3_OP_FPA_EQ, z3.Z3_OP_FPA_LT, z3.Z3_OP_FPA_GT,
                    z3.Z3_OP_FPA_LE, z3.Z3_OP_FPA_GE):
            signs = {z3.Z3_OP_FPA_EQ: "==", z3.Z3_OP_FPA_LT: "<",
                     z3.Z3_OP_FPA_GT: ">", z3.Z3_OP_FPA_LE: "<=",
                     z3.Z3_OP_FPA_GE: ">="}
            left, lkind, lwidth = self.emit(node.arg(0))
            right, rkind, rwidth = self.emit(node.arg(1))
            self.expect(lkind, "fp", node)
            self.expect(rkind, "fp", node)
            if lwidth != rwidth:
                raise E.Refused(E.CAUSE_OP,
                                "float comparison across widths")
            return "((%s) %s (%s))" % (left, signs[kind], right), \
                "bool", 1
        if kind == z3.Z3_OP_FPA_IS_NAN:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            return "((%s) != (%s))" % (text, text), "bool", 1
        if kind == z3.Z3_OP_FPA_IS_ZERO:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            return "((%s) == %s(0))" % (text, sf(awidth)), "bool", 1
        if kind == z3.Z3_OP_FPA_IS_INF:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            sort = node.arg(0).sort()
            mask = (1 << (awidth - 1)) - 1
            infinity = ((1 << sort.ebits()) - 1) << (sort.sbits() - 1)
            return "(((%s).bitPattern & %s) == %s)" % (
                text, slit(mask, awidth), slit(infinity, awidth)), \
                "bool", 1
        if kind == z3.Z3_OP_FPA_IS_NEGATIVE:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            return "(((%s).bitPattern &>> %d) != 0)" % (text,
                                                        awidth - 1), \
                "bool", 1
        if kind == z3.Z3_OP_FPA_IS_POSITIVE:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            return "(((%s).bitPattern &>> %d) == 0)" % (text,
                                                        awidth - 1), \
                "bool", 1
        raise E.Refused(E.CAUSE_OP, "%s (kind %d)" % (name, kind))

    def emit_to_fp(self, node):
        width = E.fp_width(node.sort())
        holder = sf(width)
        if node.num_args() == 1:
            child = node.arg(0)
            if child.decl().kind() == z3.Z3_OP_EXTRACT:
                grand = child.arg(0)
                high, low = child.params()
                if z3.is_const(grand) and \
                        grand.decl().kind() == z3.Z3_OP_UNINTERPRETED:
                    param = self.params[self.seed_names[
                        grand.decl().name()]]
                    if param["kind"] == "fp" and low == 0 and \
                            high + 1 == param["bits"] and \
                            param["bits"] == width:
                        return param["name"], "fp", width
            text, akind, awidth = self.emit(child)
            self.expect(akind, "bv", node)
            if awidth != width:
                raise E.Refused(E.CAUSE_WIDTH,
                                "%d bits reinterpreted as a %d-bit float"
                                % (awidth, width))
            return "%s(bitPattern: %s(truncatingIfNeeded: %s))" % (
                holder, su(width), text), "fp", width
        if node.num_args() == 2:
            self.expect_rne(node.arg(0))
            text, akind, awidth = self.emit(node.arg(1))
            if akind == "fp":
                return "%s(%s)" % (holder, text), "fp", width
            if akind == "bv":
                bits = E.promoted_bits(awidth)
                return "%s(%s)" % (holder, ssign(text, awidth, bits)), \
                    "fp", width
        raise E.Refused(E.CAUSE_OP, "fpToFP with %d arguments"
                        % node.num_args())


# ==================================================================
# section 3: COMPILE AND CARVE   the step that cannot run here
# ==================================================================

def compile_and_carve(source, symbol):
    """`swiftc -O -c` at the corpus's own ship flags, then the
    pipeline's own objdump reader.

    IT IS NOT DISABLED AND NOT SHORT-CIRCUITED: it runs, and what comes
    back is whatever the machine says.  On the image this task ran under
    that is the absence of `/persist/swift/usr/bin/swiftc`, and the
    refusal every swift row of the deliverable carries is that answer,
    LITERAL, read at run time rather than pasted."""
    extract = E.pipeline_extractor()
    work = tempfile.mkdtemp(prefix="g1_", dir=os.environ.get("TMPDIR"))
    src = os.path.join(work, "unit.swift")
    obj = os.path.join(work, "unit_ship.o")
    handle = open(src, "w")
    handle.write(source)
    handle.close()
    command = [SWIFTC] + SHIP_FLAGS + [src, "-o", obj]
    try:
        done = subprocess.run(command, capture_output=True, text=True,
                              timeout=600)
    except OSError as problem:
        E.cleanup(work)
        return None, "%s: %s" % (SWIFTC, problem.strerror)
    if done.returncode != 0 or not os.path.exists(obj):
        refusal = E.firstline(done.stderr or done.stdout)
        E.cleanup(work)
        return None, refusal
    done = subprocess.run(["objdump", "-dr", "--disassemble=" + symbol,
                           obj], capture_output=True, text=True,
                          timeout=300)
    got = extract(done.stdout, symbol, True)
    E.cleanup(work)
    if got is None:
        return None, "objdump found no symbol %s" % symbol
    return got, None


def recorded_facts(label, key, raw_bytes, mnem):
    """`emulate.recorded_facts`, CALLED unchanged and then relabelled.

    `canon37_gate.sequences_for` answers with the SysV sequence for
    every language except go, so the arrival contract swift's units are
    read with is the same object c's are read with; only the record's
    `lang` differs, which `term.py` reads to pick the toolchain whose
    runtime-callee bodies a `call` resolves to."""
    recorded = E.recorded_facts(label, key, raw_bytes, mnem)
    recorded["lang"] = TARGET
    return recorded


# ==================================================================
# section 4: THE SPELLING TABLE   one row per rule, NONE of them
#            measured, and each saying so
# ==================================================================
#
# Every row names the z3 DECLARATION KIND it is the spelling of, the
# swift text this renderer writes for it, and the reason -- from the
# language reference, which under the evidence doctrine is "human
# interpretation of stated design", the weakest class.  The `probe`
# column of go's own table is empty here on every row, because there is
# no swiftc in this image to run one.

SPELLINGS = [
    ("Z3_OP_BADD, Z3_OP_BSUB, Z3_OP_BMUL",
     "the masking operators &+ &- &*",
     "swift's plain arithmetic traps on overflow, which the term does "
     "not; the &-prefixed forms are swift's own wrapping ones"),
    ("Z3_OP_BAND, Z3_OP_BOR, Z3_OP_BXOR",
     "the plain bitwise operators",
     "no trap is defined for them"),
    ("Z3_OP_BNEG", "zero &- the value",
     "swift's unary minus is not defined on an unsigned holder at all"),
    ("Z3_OP_BNOT", "the tilde prefix", "swift's own complement"),
    ("Z3_OP_BSHL, Z3_OP_BLSHR, Z3_OP_BASHR",
     "the masking shifts &<< and &>>, inside the term's own guard "
     "where the count is not already bounded",
     "swift's plain shifts are defined for every count and its masking "
     "shifts mask to the width, which is the MACHINE's rule"),
    ("Z3_OP_BUDIV_I, Z3_OP_BUREM_I, Z3_OP_BSDIV_I, Z3_OP_BSREM_I",
     "the plain operator",
     "swift traps on a zero divisor and on the signed extreme; those "
     "are the EDGE REGIONS, rendered rather than hidden"),
    ("Z3_OP_ITE", "the conditional expression",
     "swift has one, so no helper of the kind go needs"),
    ("Z3_OP_EQ, Z3_OP_DISTINCT, Z3_OP_SLEQ .. Z3_OP_UGT",
     "the plain comparison on the converted holder",
     "the conversions are explicit and non-trapping"),
    ("Z3_OP_EXTRACT, Z3_OP_CONCAT, Z3_OP_ZERO_EXT, Z3_OP_SIGN_EXT",
     "the truncating initializer, and a masking shift joined by an or",
     "the plain initializer TRAPS when the value does not fit, which "
     "would put a trap in every intermediate step"),
    ("Z3_OP_FPA_TO_IEEE_BV", "the float's own bit pattern",
     "swift names the bits of a float directly, so no helper of the "
     "kind c's renderer writes is needed"),
    ("Z3_OP_FPA_TO_FP (bits reinterpreted)",
     "the float holder's bit-pattern initializer", "the same, inverted"),
    ("Z3_OP_FPA_TO_FP (value converted)",
     "the float holder's plain initializer",
     "the conversion from an integer holder is exact for the widths "
     "this task's cells use"),
    ("Z3_OP_FPA_TO_SBV, Z3_OP_FPA_TO_UBV",
     "the integer holder's plain initializer",
     "THE THINNEST ROW: swift's initializer traps when the value does "
     "not fit, where the machine answers with the integer-indefinite "
     "pattern -- an edge region, and one nothing here has measured"),
    ("Z3_OP_FPA_ADD, Z3_OP_FPA_SUB, Z3_OP_FPA_MUL, Z3_OP_FPA_DIV",
     "the plain operator on the float holder", "no trap is defined"),
    ("Z3_OP_FPA_ABS", "the sign bit cleared through the bit pattern",
     "the standard library's own absolute value would reach outside "
     "the file"),
    ("the holders", "Int8..Int64, UInt8..UInt64, Float, Double",
     "whether this toolchain has Float16 or the 128-bit holders is "
     "UNMEASURED, so both are refused rather than spelled"),
    ("the arrival registers", "the SysV sequence",
     "canon37_gate.sequences_for answers with the SysV sequence for "
     "every language except go, so emulate.recorded_facts and "
     "emulate.expected_c_families apply unchanged"),
]


def spelling_rows():
    """the spelling table as records.  `measured` is False on every one
    of them, and that is the point of the column."""
    out = []
    for kind, spelling, note in SPELLINGS:
        out.append({
            "z3_kind": kind,
            "spelling": spelling,
            "probes": "",
            "what_it_emits": "UNMEASURED -- %s" % note,
            "measured": False,
            "bodies": [],
        })
    return out


def flags_command():
    say("the swift ship flags this task would compile at: swiftc %s"
        % " ".join(SHIP_FLAGS))
    say("")
    say("their source, LITERAL:")
    say("   %s" % SHIP_FLAGS_SOURCE)
    say("")
    say("what running that swiftc answers on this machine, LITERAL:")
    say("   %s" % swiftc_answer())
    return 0


def main(argv):
    if not argv:
        say(__doc__)
        return 2
    if argv[0] == "flags":
        return flags_command()
    say("unknown command %r" % argv[0])
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
