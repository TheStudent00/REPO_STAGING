#!/usr/bin/env python3
"""go_render.py -- task g1: AutoPoly with GO as the target.

Node: hq.research.arch_unit_oracle.cross_construction
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/CORE_0_3_2_2_cross_construction.md`,
FROZEN for term-level composition; task o7 opened the emulation route
with c as the target and task o11 added rust.  This file adds a third
target, which asks the same question of a third compiler and does not
unfreeze the node).

THE OBJECTS, one sentence each, in relation.
  * A TERM is one place of one arch-opcode written as a z3 expression
    over `seed_<register family>` symbols -- for this task, one place
    of one cell of the arch-opcode model table.
  * AN EMULATION is a go program whose one exported function's body is
    that term written in go's own operations over go's holders,
    produced by the ONE renderer below (`GoRenderer`, which DERIVES
    from task o7's `emulate.Renderer` and overrides one method per rule
    whose SPELLING differs from c).  A term the renderer cannot write
    is refused by cause and no source is written for it.
  * THE SHIP BUILD is a plain `go build` of a `package main` program in
    a module directory, which is what `lane_gen.py`'s go branch does
    for every go unit of the corpus; the artifact is a linked
    EXECUTABLE rather than an object file, and the symbol carved out of
    it is `main.<name>`, the corpus's own symbol shape
    (`probe_gen.emit_go`).

EVERY SPELLING BELOW WAS MEASURED BEFORE IT WAS WRITTEN, task o11
section 3.1's rule.  The evidence is `go_facts.json` beside this file,
written by `go_facts.py probe` in lane `g1_l5_go_facts3.sh`: one small
go function per question, built at the same flags, carved with the same
objdump reader.  Each rule below names its probe.  THE FIVE THAT
CHANGED WHAT HAD TO BE WRITTEN:

  1. `plain_sum_u32` emits `add %ebx,%eax` and `plain_negate_u32` emits
     `neg %eax`: go's plain `+ - *` and unary `-` WRAP at the ship
     flags and carry no check at all, so -- unlike rust, whose renderer
     must write `wrapping_add` -- go's plain operator IS the term's own
     meaning and the renderer writes it.
  2. `plain_left_shift_u32` emits `shl %cl,%eax` FOLLOWED BY go's own
     out-of-range guard (`cmp $0x20,%ecx; sbb %edx,%edx; and %edx,%eax`)
     because go defines a count at or above the width as answering
     zero, where the machine's own shift masks the count.
     `masked_left_shift_u32`, whose source masks the count itself,
     emits the bare `shl %cl,%eax`.  So the CELL'S MASK MUST BE SPELLED
     in the source: the renderer writes the count masked to the width,
     and go then emits no guard of its own.
  3. `select_u64` shows that go has no conditional EXPRESSION at all,
     so a conditional is written as a call to a small helper function
     in the same file; the helper inlines to `test %al,%al; cmovne
     %rbx,%rcx`, a conditional move and no call.  `select_f64` shows
     the same helper with FLOAT arms inlines to a BRANCH rather than a
     move, which is recorded rather than worked around.
  4. `f64_bits_math` emits `nop; movq %xmm0,%rax` and `f64_bits_unsafe`
     emits `movq %xmm0,%rax`: on a BARE FLOAT ARRIVAL the pointer cast
     is one instruction and the standard library's own function is the
     same instruction behind an inlining marker.  A parameter is
     already a variable, so `emit_symbol` writes the pointer cast; a
     sub-expression and the answer are not, so `answer` writes the
     library function.
     AND THE PART THAT WAS MEASURED WRONG THE FIRST TIME, recorded
     here rather than quietly corrected.  This renderer first spelled
     the ANSWER's reinterpretation with the pointer cast over a bound
     local, and the emulation of `addss` came back with a stack frame
     around it.  The reading was that binding the local caused the
     frame; the spelling was changed to the library function, the forty
     runs were run again (lane `g1_l9_run_of_record.sh`), and THE BODY
     WAS THE SAME:

         push %rbp; mov %rsp,%rbp; sub $0x8,%rsp;
         addss %xmm1,%xmm0;
         movss %xmm0,0x4(%rsp); movss 0x4(%rsp),%xmm0;
         add $0x8,%rsp; pop %rbp; ret

     Go's own `math.Float32bits` IS a pointer cast over a local, so
     both spellings put the value through memory and go folds neither
     -- where clang folds its `memcpy` helper pair to nothing and rustc
     folds `to_bits`/`from_bits` to nothing, and both land on
     `addss %xmm1,%xmm0; ret`.  That is a fact about go, not about the
     spelling.  The library function is kept because it is ONE rule
     wherever there is no variable, and because the rendered source
     then needs no `unsafe` import; the round trip is reported as this
     target's own cost.
  5. `wide_holder_128` and `float16_holder` are refused by the compiler
     itself -- `undefined: uint128`, `undefined: float16` -- so go has
     NO 128-bit integer holder and NO 16-bit float holder.  That is
     this target's hole, the way the missing `f16` is rust's, and a
     term needing either is refused by cause.

TWO MORE MEASURED FACTS THE DRIVER NEEDS, not spellings:
  * `arrival_registers_six` reads `%rax %rbx %rcx %rdi %rsi %r8` in
    declaration order, and `arrival_registers_float` reads `%xmm0
    %xmm1 %xmm2`: go's own argument sequence, which is
    `canon37_gate.GENERAL_SEQUENCE_GO` / `VECTOR_SEQUENCE_GO`.  That is
    why `expected_go_families` below exists beside
    `emulate.expected_c_families` and why `recorded_facts` reads the
    arrival contract with go's own order.
  * `narrow_arrival_u8` emits `movzbl %al,%ecx`: the go callee
    RE-EXTENDS a narrow arrival itself rather than assuming the caller
    widened it, which is the opposite of c's and rust's rule
    (`emulate.expected_c_families`'s note and task o7's
    caller-extension re-pose).  So a go emulation needs no such
    re-pose; the re-pose is left in the driver unchanged and simply
    does not fire.

WHAT IS REUSED RATHER THAN COPIED, said out loud.  Nothing under
`Research/op_pipeline/` is edited, and `emulate.py` is imported, never
forked:
  `emulate.Renderer`           -- DERIVED FROM; `GoRenderer` overrides
                                  one method per rule whose spelling
                                  differs from c and inherits the width
                                  planning, the free-symbol check and
                                  the refusal causes.
  `emulate.pipeline_extractor` -- the carve, unchanged.
  `emulate.promoted_bits`, `.upper_bound`, `.fp_width`, `.PARAM_NAMES`,
  `.Refused` and its causes -- unchanged.
  `single_opcode_units.strip_chaff` / `parse_insn` -- task o2's narrow
                                  rule, unchanged, through the driver.

ONE THING IS RESTATED RATHER THAN CALLED, and here is why.
`emulate.recorded_facts` reads the arrival contract with
`canon38_gate.arrival_contract("c", body_text)`, and
`canon37_gate.sequences_for` answers with the SysV sequence for every
language EXCEPT go.  Task o11's rust file could therefore call it and
relabel afterwards; go cannot, because the ORDER ITSELF differs.
`recorded_facts` below is that function with `"go"` in place of `"c"`
and nothing else changed.

MEMORY BOUND, stated as the law requires: this file allocates nothing
of its own -- it renders text and shells out to `go build` and
`objdump` -- and runs inside the driver's one collecting process under
its stated 4 GB resident bound and named abort ABORT_MEMORY_G1.

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
printer: a z3 declaration kind goes in and go source comes out.  The go
operator tokens in the strings below are the OUTPUT TEXT of that
printer -- the program being written -- and are read by the go
compiler, never by this line's own machinery.

Coding discipline: no compound one-liner statements.

usage:
  go_render.py flags     the ship flags and their source, LITERAL
"""

import json
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

FACTS = os.path.join(HERE, "go_facts.json")
SRC_DIR = os.path.join(HERE, "src")
HOST_FOLDER = ("PseudoCoupHQ/Research/oracle/"
               "cross_construction/emulation/go")

TARGET = "go"
GO = "go"

# read off `lane_gen.py` compile_probe, the go branch: the SHIP build is
# a plain `go build` with no gcflags, in a module directory holding
# `go.mod` and `main.go`.
SHIP_ARGS = ["build"]
SHIP_FLAGS_SOURCE = ("lane_gen.py compile_probe, go branch: "
                     "`open(go.mod).write(GOMOD)`; "
                     "`open(main.go).write(p[\"source\"])`; "
                     "`cmd = [\"go\", \"build\"]` with no gcflags in "
                     "the ship mode, then `cmd.extend([\"-o\", obj, "
                     "\".\"])` run with cwd=the module directory -- the "
                     "ship build of every go unit in the corpus")
GOMOD = "module opprobe\n\ngo 1.26\n"
# `proxy = no` in the instance conf: the module has no requirements, so
# nothing is fetched; these make that explicit rather than leaving it to
# a network timeout.
GO_ENV = {"GOFLAGS": "-mod=mod", "GOPROXY": "off", "GO111MODULE": "on"}

# go's holders, MEASURED rather than recalled (`go_facts.json`): every
# width below built and carved; `uint128` and `float16` are refused by
# the compiler itself with "undefined".
GU = {8: "uint8", 16: "uint16", 32: "uint32", 64: "uint64"}
GI = {8: "int8", 16: "int16", 32: "int32", 64: "int64"}
GF = {32: "float32", 64: "float64"}
PARAM_NAMES = E.PARAM_NAMES

NO_WIDE = ("go has no %d-bit integer holder: `go build` refuses "
           "`uint128` with \"undefined: uint128\" (measured, probe "
           "wide_holder_128)")
NO_F16 = ("go has no %d-bit float holder: `go build` refuses `float16` "
          "with \"undefined: float16\" (measured, probe "
          "float16_holder)")

# go's own argument sequence, measured by probe `arrival_registers_six`
# (`%rax %rbx %rcx %rdi %rsi %r8`, in declaration order) and probe
# `arrival_registers_float` (`%xmm0 %xmm1 %xmm2`).  It is the same
# sequence `canon37_gate.GENERAL_SEQUENCE_GO` holds, which is where the
# pipeline reads it, and this constant is checked against that one by
# `sequence_agrees()` rather than trusted.
GENERAL_ORDER_GO = ["rax", "rbx", "rcx", "rdi", "rsi", "r8", "r9",
                    "r10", "r11"]


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def sequence_agrees():
    """the measured sequence against the pipeline's own, so the two are
    never allowed to drift apart in silence."""
    import canon37_gate as G37
    general, vector = G37.sequences_for(TARGET)
    return {
        "measured": GENERAL_ORDER_GO,
        "the pipeline's own": list(general),
        "they agree": list(general) == GENERAL_ORDER_GO,
        "the pipeline's own vector sequence": list(vector),
    }


# ==================================================================
# section 1: GO SOURCE PIECES   holders, literals, masks, sign
# ==================================================================

def gu(bits):
    """the unsigned holder of `bits`, or the refusal that names go's
    hole."""
    if bits not in GU:
        raise E.Refused(E.CAUSE_WIDTH, NO_WIDE % bits)
    return GU[bits]


def gi(bits):
    if bits not in GI:
        raise E.Refused(E.CAUSE_WIDTH, NO_WIDE % bits)
    return GI[bits]


def gf(bits):
    if bits not in GF:
        raise E.Refused(E.CAUSE_WIDTH, NO_F16 % bits)
    return GF[bits]


def glit(value, bits):
    """a go literal of the unsigned holder of `bits`."""
    value = value & ((1 << bits) - 1)
    return "%s(0x%x)" % (gu(bits), value)


def gmask(text, width):
    """`text`, of the promoted unsigned holder of `width`, with the bits
    above `width` cleared.  Go converts explicitly and never
    implicitly, so every step names its holder."""
    bits = E.promoted_bits(width)
    if width == bits:
        return "(%s(%s))" % (gu(bits), text)
    return "((%s(%s)) & %s)" % (gu(bits), text, glit((1 << width) - 1,
                                                     bits))


def gsign(text, width, bits):
    """`text` (the low `width` bits of the promoted unsigned holder) as
    a SIGNED value of the holder of `bits`, sign bit `width - 1`
    propagated.

    The shift pair is go's own arithmetic right shift on a signed
    holder, measured by probe `masked_arith_shift_i32`
    (`sar %cl,%eax`)."""
    if width == bits:
        return "(%s(%s))" % (gi(bits), text)
    shift = bits - width
    return "((%s(%s) << %d) >> %d)" % (gi(bits), text, shift, shift)


# ==================================================================
# section 2: THE RENDERER   z3 term -> go source
# ==================================================================

class GoRenderer(E.Renderer):
    """the ONE go renderer: a z3 term over `seed_<family>` symbols ->
    one go program.  DERIVES from task o7's `emulate.Renderer`; the
    width planning, the free-symbol check and the refusal causes are
    inherited unchanged.

    attributes:
        families        the term's arrival families, IN order
        result_family   the answer home
        result_width    its width in bits
        params          per family: name, holder text, kind, bits
        selectors       the (kind, bits) pairs the body's conditionals
                        need, so exactly those helper functions are
                        written
        needs_unsafe    whether any bit cast was written, so the
                        `unsafe` import is present only when used
    methods:
        render          -> (source text, function symbol)
        emit            one node -> (text, kind, width)
    """

    def __init__(self, families, result_family, result_width, label):
        E.Renderer.__init__(self, families, result_family, result_width,
                            label)
        self.selectors = []
        self.needs_unsafe = False
        self.needs_math = False

    # -- the parameter plan -------------------------------------------

    def plan_parameters(self, term):
        """the base class plans the WIDTH of every arrival from how the
        term reads it; only the holder text is go's."""
        E.Renderer.plan_parameters(self, term)
        for param in self.params:
            if param["kind"] == "fp":
                param["holder"] = gf(param["bits"])
                continue
            param["holder"] = gu(param["bits"])

    # -- the source ---------------------------------------------------

    def render(self, term, text):
        """the whole go program: the emulation function, the helper
        functions its body actually named, the package globals that keep
        it reachable, and `main`.

        THE PROGRAM SHAPE IS THE CORPUS'S OWN (`probe_gen.emit_go`):
        `package main`, `//go:noinline` on the function, package-level
        variables handed to it, and a `main` that calls it and parks the
        answer in a `sink`, so the linker cannot drop it.  The symbol
        the carve asks objdump for is `main.<name>`, also the corpus's
        own."""
        self.plan_parameters(term)
        self.check_symbols(term)
        root_text, root_kind, root_width = self.emit(term)
        return_type, statements = self.answer(root_text, root_kind,
                                              root_width)
        symbol = "emu_%s" % self.label
        params = []
        for param in self.params:
            params.append("%s %s" % (param["name"], param["holder"]))
        lines = []
        lines.append("// task g1 emulation -- rendered by go_render.py")
        lines.append("// GoRenderer from the layer-4 term of %s."
                     % self.label)
        lines.append("// The term's layer-5 text, LITERAL:")
        lines.append("//   %s" % " ".join(text.split()))
        lines.append("package main")
        lines.append("")
        # THE IMPORTS ARE KNOWN BY NOW because the body was emitted
        # above: `emit` and `answer` ran before this list was started,
        # and each of them records which of the two bit-cast spellings
        # it wrote.  Go refuses an unused import, so only the ones the
        # body named are written.
        if self.needs_math:
            lines.append("import \"math\"")
        if self.needs_unsafe:
            lines.append("import \"unsafe\"")
        if self.needs_math or self.needs_unsafe:
            lines.append("")
        for helper in self.selector_texts():
            lines.append(helper)
            lines.append("")
        lines.append("//go:noinline")
        lines.append("func %s(%s) %s {" % (symbol, ", ".join(params),
                                           return_type))
        for statement in statements:
            lines.append("\t%s" % statement)
        lines.append("}")
        lines.append("")
        names = []
        for index, param in enumerate(self.params):
            lines.append("var g%d %s" % (index, param["holder"]))
            names.append("g%d" % index)
        lines.append("var sink interface{}")
        lines.append("")
        lines.append("func main() {")
        lines.append("\tsink = %s(%s)" % (symbol, ", ".join(names)))
        lines.append("\t_ = sink")
        lines.append("}")
        lines.append("")
        return "\n".join(lines), "main.%s" % symbol

    def selector_name(self, kind, bits):
        """the helper the body will call for one conditional, recorded
        so exactly the helpers used are written."""
        if kind == "fp":
            name = "selfp%d" % bits
            holder = gf(bits)
        elif kind == "bool":
            name = "selbool"
            holder = "bool"
        else:
            name = "sel%d" % bits
            holder = gu(bits)
        if (name, holder) not in self.selectors:
            self.selectors.append((name, holder))
        return name

    def selector_texts(self):
        """GO HAS NO CONDITIONAL EXPRESSION, so a conditional is a call
        to one of these.  Measured (probe `select_u64`): the helper
        inlines to `test %al,%al; cmovne %rbx,%rcx` -- a conditional
        move, no call.  With FLOAT arms (probe `select_f64`) it inlines
        to a branch instead, which is recorded and not worked around."""
        out = []
        for name, holder in self.selectors:
            out.append("func %s(c bool, x %s, y %s) %s {\n"
                       "\tif c {\n\t\treturn x\n\t}\n\treturn y\n}"
                       % (name, holder, holder, holder))
        return out

    def answer(self, root_text, root_kind, root_width):
        """(return type, the statements of the function body).

        THE ANSWER'S BIT REINTERPRETATION IS THE STANDARD LIBRARY'S
        FUNCTION, and the header of this file records what was measured
        about that and what was first read wrong about it.  Go's
        pointer cast is `*(*T)(unsafe.Pointer(&v))` and `&` needs a
        VARIABLE, so spelling the answer that way means binding one;
        the library function is an EXPRESSION and needs none.  Both
        emit the SAME body -- go's own `math.Float32bits` is itself a
        pointer cast over a local, and go folds neither, so the value
        goes through memory either way (measured, lane
        `g1_l9_run_of_record.sh`).  The library function is kept
        because it is one rule wherever there is no variable to take
        the address of, and because the rendered source then needs no
        `unsafe` import.

        This method answers with a list of statements rather than one
        expression, because the pointer cast in `emit_symbol` may one
        day need a bound local here; today every list it returns has
        one entry."""
        import reference as R
        family = self.result_family
        width = self.result_width
        if family is None or width is None:
            raise E.Refused(E.CAUSE_STATE, "no answer home")
        if family in R.XMM_NAMES:
            return_type = gf(width)
            if root_kind == "fp":
                if root_width != width:
                    raise E.Refused(E.CAUSE_WIDTH,
                                    "fp answer %d bits, home %d"
                                    % (root_width, width))
                return return_type, ["return %s" % root_text]
            if root_kind == "bool":
                raise E.Refused(E.CAUSE_OP,
                                "a truth value in a float answer home")
            return return_type, [
                "return %s(%s(%s))"
                % (self.bits_to_float_call(width), gu(width), root_text),
            ]
        if family.startswith("st") or family.startswith("x87"):
            raise E.Refused(E.CAUSE_X87, family)
        return_type = gu(width)
        if root_kind == "fp":
            return return_type, [
                "return %s(%s)"
                % (return_type,
                   self.float_to_bits_call(root_text, root_width)),
            ]
        if root_kind == "bool":
            name = self.selector_name("bv", E.promoted_bits(width))
            promoted = E.promoted_bits(width)
            return return_type, [
                "return %s(%s(%s, %s, %s))"
                % (return_type, name, root_text, glit(1, promoted),
                   glit(0, promoted)),
            ]
        return return_type, ["return %s(%s)" % (return_type, root_text)]

    # -- one node -----------------------------------------------------

    def emit(self, node):
        """-> (go text, kind, width).  kind is bv (text of the promoted
        unsigned holder, bits above `width` zero), fp (float32/float64
        of `width` bits) or bool (a go `bool`).  The four cases below
        are the ones whose SPELLING differs from c; everything else goes
        through the base class's dispatch, which calls this object's own
        `emit_*` overrides."""
        decl = node.decl()
        kind = decl.kind()
        if z3.is_const(node) and kind == z3.Z3_OP_UNINTERPRETED:
            return self.emit_symbol(node, None)
        if kind == z3.Z3_OP_BNUM:
            width = node.size()
            bits = E.promoted_bits(width)
            return glit(node.as_long(), bits), "bv", width
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
            text = "%s(%s)" % (gu(bits), param["name"])
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
            return gmask("(%s) >> %d" % (text, low), high - low + 1), \
                "bv", high - low + 1
        # A VECTOR ARRIVAL planned as a float holder: its bits.
        # Measured (probes `f64_bits_unsafe`, `f32_bits_unsafe`): the
        # pointer cast emits one instruction (`movq %xmm0,%rax`,
        # `movd %xmm0,%eax`), where the standard library's own
        # `math.Float64bits` emits the same instruction with an inlining
        # marker `nop` in front of it.
        self.needs_unsafe = True
        bits = E.promoted_bits(param["bits"])
        text = "%s(*(*%s)(unsafe.Pointer(&%s)))" % (
            gu(bits), gu(param["bits"]), param["name"])
        if extract is None:
            raise E.Refused(E.CAUSE_LANE, name)
        high, low = extract
        if low == 0 and high + 1 == param["bits"]:
            return text, "bv", param["bits"]
        return gmask("(%s) >> %d" % (text, low), high - low + 1), \
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
        shifted = "(%s(%s)) >> %d" % (gu(inner_bits), text, low)
        return gmask(shifted, out), "bv", out

    def emit_concat(self, node):
        """the join, measured by probe `concat_shift_or_u64`:
        `mov %eax,%eax; shl $0x20,%rax; mov %ebx,%ecx; or %rcx,%rax`."""
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
            piece = "((%s(%s)) << %d)" % (gu(bits), text, shift)
            if shift == 0:
                piece = "(%s(%s))" % (gu(bits), text)
            pieces.append(piece)
        return gmask(" | ".join(pieces), total), "bv", total

    def emit_extend(self, node, signed):
        extra = node.params()[0]
        text, kind, width = self.emit(node.arg(0))
        self.expect(kind, "bv", node)
        total = width + extra
        bits = E.promoted_bits(total)
        if not signed:
            return "(%s(%s))" % (gu(bits), text), "bv", total
        return gmask(self.sign_extended(text, width, bits), total), \
            "bv", total

    def sign_extended(self, text, width, bits):
        return gsign(text, width, bits)

    def emit_ite(self, node):
        """the conditional, through the helper `selector_texts` writes,
        because go has no conditional expression."""
        cond, ckind, _ = self.emit(node.arg(0))
        self.expect(ckind, "bool", node)
        left, lkind, lwidth = self.emit(node.arg(1))
        right, rkind, rwidth = self.emit(node.arg(2))
        if lkind != rkind or lwidth != rwidth:
            raise E.Refused(E.CAUSE_OP, "If with arms of different sorts")
        if lkind == "bv":
            bits = E.promoted_bits(lwidth)
            name = self.selector_name("bv", bits)
            return "%s(%s, %s(%s), %s(%s))" % (name, cond, gu(bits),
                                               left, gu(bits), right), \
                "bv", lwidth
        if lkind == "fp":
            name = self.selector_name("fp", lwidth)
            return "%s(%s, %s, %s)" % (name, cond, left, right), \
                "fp", lwidth
        name = self.selector_name("bool", 1)
        return "%s(%s, %s, %s)" % (name, cond, left, right), "bool", 1

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
        return "((%s(%s)) %s (%s(%s)))" % (gu(bits), left, sign,
                                           gu(bits), right), "bool", 1

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
            left = gsign(left, lwidth, bits)
            right = gsign(right, rwidth, bits)
        else:
            left = "(%s(%s))" % (gu(bits), left)
            right = "(%s(%s))" % (gu(bits), right)
        return "((%s) %s (%s))" % (left, signs[kind], right), "bool", 1

    def emit_arith(self, node, kind):
        """THE PLAIN OPERATOR, and the measurement that says so:
        `plain_sum_u32` emits `add %ebx,%eax`, `plain_difference_u32`
        emits `sub %ebx,%eax`, `plain_product_u64` emits
        `imul %rbx,%rax` -- no check, no branch, at the corpus's own
        ship flags.  Go's arithmetic on an unsigned holder wraps by the
        language's own definition, which is the term's own meaning, so
        there is no wrapping method to reach for and none exists."""
        signs = {
            z3.Z3_OP_BADD: "+", z3.Z3_OP_BSUB: "-", z3.Z3_OP_BMUL: "*",
            z3.Z3_OP_BAND: "&", z3.Z3_OP_BOR: "|", z3.Z3_OP_BXOR: "^",
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
            cast.append("(%s(%s))" % (gu(bits), text))
        joined = (" %s " % signs[kind]).join(cast)
        return gmask(joined, width), "bv", width

    def emit_unary(self, node, kind):
        """`^x` is go's bitwise complement (probe `complement_u32`:
        `not %eax`) and unary `-` on an unsigned holder wraps (probe
        `plain_negate_u32`: `neg %eax`)."""
        text, akind, width = self.emit(node.arg(0))
        self.expect(akind, "bv", node)
        bits = E.promoted_bits(width)
        cast = "(%s(%s))" % (gu(bits), text)
        if kind == z3.Z3_OP_BNOT:
            return gmask("^%s" % cast, width), "bv", width
        return gmask("-%s" % cast, width), "bv", width

    def emit_shift(self, node, kind):
        """THE COUNT IS MASKED IN THE SOURCE, and the measurement that
        says so: `plain_left_shift_u32` emits `shl %cl,%eax` FOLLOWED BY
        go's own out-of-range guard (`cmp $0x20,%ecx; sbb %edx,%edx;
        and %edx,%eax`), because go defines a count at or above the
        width as answering zero where the machine's shift masks the
        count; `masked_left_shift_u32`, whose source masks the count
        itself, emits the bare `shl %cl,%eax`.

        THE TERM'S OWN RULE IS THE SAME AS GO'S (a count at or above the
        width answers with the fill), so where the term's count is NOT
        already bounded the plain operator is correct and the guard go
        emits is the term's own guard.  Where the count IS bounded --
        which is the model table's own shape, since the machine's own
        shift masks and the reference's builder spells that mask -- the
        mask is written out so no guard is emitted.  `emulate.
        upper_bound` is the same bound reader the c and rust renderers
        use."""
        value, vkind, width = self.emit(node.arg(0))
        amount, akind, awidth = self.emit(node.arg(1))
        self.expect(vkind, "bv", node)
        self.expect(akind, "bv", node)
        bits = E.promoted_bits(width)
        abits = E.promoted_bits(awidth)
        bound = E.upper_bound(node.arg(1))
        count = "(%s(%s))" % (gu(abits), amount)
        if bound is not None and bound < width:
            count = "((%s(%s)) & %s)" % (gu(abits), amount,
                                         glit(width - 1, abits))
        if kind == z3.Z3_OP_BSHL:
            body = "(%s(%s)) << %s" % (gu(bits), value, count)
            return gmask(body, width), "bv", width
        if kind == z3.Z3_OP_BLSHR:
            body = "(%s(%s)) >> %s" % (gu(bits), value, count)
            return gmask(body, width), "bv", width
        signed_value = gsign(value, width, bits)
        body = "%s(%s >> %s)" % (gu(bits), signed_value, count)
        return gmask(body, width), "bv", width

    def emit_division(self, node, kind):
        """THE PLAIN DIVIDE, and the EDGE REGION left visible.

        Measured: `plain_quotient_u32` carries `test %ebx,%ebx; je ...`
        into `runtime.panicdivide` at the ship flags, and
        `plain_quotient_i32` carries that check AND go's own handling of
        the extreme case (`cmp $0xffffffff,%ebx; jne ...; neg %eax`,
        because go's specification DEFINES the most negative value over
        minus one as wrapping rather than trapping).  The brief's rule
        for this target is to render the plain operator and let the gate
        report the region, so neither check is hidden: they are the edge
        regions of this opcode in this language, and the gate's verdict
        says whether the body answers as the cell does on all inputs or
        only on a region."""
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
            numerator = gsign(left, lwidth, bits)
            divisor = gsign(right, rwidth, bits)
            body = "%s(%s %s %s)" % (gu(bits), numerator, sign, divisor)
            return gmask(body, lwidth), "bv", lwidth
        numerator = "(%s(%s))" % (gu(bits), left)
        divisor = "(%s(%s))" % (gu(bits), right)
        body = "%s %s %s" % (numerator, sign, divisor)
        return gmask(body, lwidth), "bv", lwidth

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
            holder = gf(width)
            bits_value = z3.simplify(z3.fpToIEEEBV(node)).as_long()
            if bits_value == 0:
                return "(%s(0))" % holder, "fp", width
            return "%s(%s)" % (self.bits_to_float_call(width),
                               glit(bits_value, width)), "fp", width
        if kind == z3.Z3_OP_FPA_TO_FP:
            return self.emit_to_fp(node)
        if kind == z3.Z3_OP_FPA_TO_FP_UNSIGNED:
            self.expect_rne(node.arg(0))
            text, akind, awidth = self.emit(node.arg(1))
            self.expect(akind, "bv", node)
            width = E.fp_width(node.sort())
            bits = E.promoted_bits(awidth)
            return "%s(%s(%s))" % (gf(width), gu(bits), text), \
                "fp", width
        if kind == z3.Z3_OP_FPA_TO_IEEE_BV:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            bits = E.promoted_bits(awidth)
            return "%s(%s)" % (gu(bits),
                               self.float_to_bits_call(text, awidth)), \
                "bv", awidth
        if kind in (z3.Z3_OP_FPA_TO_SBV, z3.Z3_OP_FPA_TO_UBV):
            rm = node.arg(0)
            if rm.decl().kind() != z3.Z3_OP_FPA_RM_TOWARD_ZERO:
                raise E.Refused(E.CAUSE_RM,
                                "%s under %s (go's own conversion "
                                "truncates)" % (name, rm.decl().name()))
            text, akind, awidth = self.emit(node.arg(1))
            self.expect(akind, "fp", node)
            width = node.size()
            if kind == z3.Z3_OP_FPA_TO_SBV:
                holder = gi(width)
            else:
                holder = gu(width)
            # measured, probe `f64_to_int`: `cvttsd2si %xmm0,%rax`, the
            # bare truncating conversion, with no saturation sequence of
            # the kind rust's plain `as` emits.
            return gmask("%s(%s(%s))" % (gu(E.promoted_bits(width)),
                                         holder, text), width), \
                "bv", width
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
            cleared = "((%s) & %s)" % (
                self.float_to_bits_call(text, awidth),
                glit(mask, awidth))
            return "%s(%s)" % (self.bits_to_float_call(awidth),
                               cleared), "fp", awidth
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
            return "((%s) == %s(0))" % (text, gf(awidth)), "bool", 1
        if kind == z3.Z3_OP_FPA_IS_INF:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            sort = node.arg(0).sort()
            mask = (1 << (awidth - 1)) - 1
            infinity = ((1 << sort.ebits()) - 1) << (sort.sbits() - 1)
            return "(((%s) & %s) == %s)" % (
                self.float_to_bits_call(text, awidth),
                glit(mask, awidth), glit(infinity, awidth)), "bool", 1
        if kind == z3.Z3_OP_FPA_IS_NEGATIVE:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            return "(((%s) >> %d) != 0)" % (
                self.float_to_bits_call(text, awidth), awidth - 1), \
                "bool", 1
        if kind == z3.Z3_OP_FPA_IS_POSITIVE:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            return "(((%s) >> %d) == 0)" % (
                self.float_to_bits_call(text, awidth), awidth - 1), \
                "bool", 1
        raise E.Refused(E.CAUSE_OP, "%s (kind %d)" % (name, kind))

    def float_to_bits_call(self, text, width):
        """A BIT CAST IN THE MIDDLE OF AN EXPRESSION needs an
        addressable value, and go's pointer cast takes the address of a
        VARIABLE, so mid-expression the only spelling is the standard
        library's own function.  Measured (probe `f64_bits_math`):
        `nop; movq %xmm0,%rax` -- the same one instruction the pointer
        cast emits, with an inlining marker in front of it, which task
        o2's own narrow chaff rule strips.  Where the value IS a bare
        arrival or the answer, `emit_symbol` and `answer` above write
        the pointer cast instead and no marker is emitted."""
        self.needs_math = True
        return "math.Float%dbits(%s)" % (width, text)

    def bits_to_float_call(self, width):
        """the same the other way; see `float_to_bits_call`."""
        self.needs_math = True
        return "math.Float%dfrombits" % width

    def emit_to_fp(self, node):
        width = E.fp_width(node.sort())
        holder = gf(width)
        if node.num_args() == 1:
            child = node.arg(0)
            # the shortcut: the bits of a float arrival, read whole --
            # the arrival itself, with no cast at all
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
            return "%s(%s(%s))" % (self.bits_to_float_call(width),
                                   gu(width), text), "fp", width
        if node.num_args() == 2:
            self.expect_rne(node.arg(0))
            text, akind, awidth = self.emit(node.arg(1))
            if akind == "fp":
                return "%s(%s)" % (holder, text), "fp", width
            if akind == "bv":
                bits = E.promoted_bits(awidth)
                # measured, probes `int_to_f64` / `int32_to_f64`:
                # `xorps %xmm0,%xmm0; cvtsi2sd %rax,%xmm0` -- go breaks
                # the destination's dependency before the conversion, so
                # a go emulation of a convert opcode is TWO instructions
                # where c's and rust's is one.
                return "%s(%s)" % (holder,
                                   gsign(text, awidth, bits)), \
                    "fp", width
        raise E.Refused(E.CAUSE_OP, "fpToFP with %d arguments"
                        % node.num_args())


# ==================================================================
# section 3: BUILD AND CARVE   `go build` at the corpus's ship flags
# ==================================================================

def compile_and_carve(source, symbol):
    """the go corpus's own ship build and carve: a module directory
    holding `go.mod` and `main.go`, a plain `go build`, and objdump read
    by `emulate.pipeline_extractor()`, which is `lane_gen.DRIVER`'s own
    `extract`.

    THE ARTIFACT IS A LINKED EXECUTABLE, not an object file, because
    that is what `lane_gen.py`'s go branch builds and what every go unit
    of the corpus was carved out of.  `HOME`, `GOCACHE` and `GOPATH` are
    pointed inside the temporary directory so the build writes nothing
    outside it, and `GOPROXY=off` so nothing is fetched -- the instance
    has no route out at all (`proxy = no`) and the module has no
    requirements."""
    extract = E.pipeline_extractor()
    work = tempfile.mkdtemp(prefix="g1_", dir=os.environ.get("TMPDIR"))
    handle = open(os.path.join(work, "go.mod"), "w")
    handle.write(GOMOD)
    handle.close()
    handle = open(os.path.join(work, "main.go"), "w")
    handle.write(source)
    handle.close()
    binary = os.path.join(work, "bin_ship")
    environment = dict(os.environ)
    environment.update(GO_ENV)
    environment["HOME"] = work
    environment["GOCACHE"] = os.path.join(work, "gocache")
    environment["GOPATH"] = os.path.join(work, "gopath")
    command = [GO] + SHIP_ARGS + ["-o", binary, "."]
    done = subprocess.run(command, capture_output=True, text=True,
                          timeout=600, cwd=work, env=environment)
    if done.returncode != 0 or not os.path.exists(binary):
        refusal = go_refusal(done.stderr or done.stdout)
        cleanup(work)
        return None, refusal
    done = subprocess.run(["objdump", "-dr", "--disassemble=" + symbol,
                           binary], capture_output=True, text=True,
                          timeout=300)
    got = extract(done.stdout, symbol, True)
    cleanup(work)
    if got is None:
        return None, "objdump found no symbol %s" % symbol
    return got, None


REFUSAL_READER = {}


def go_refusal(text):
    """the PIPELINE's own reading of a go refusal, taken out of
    `lane_gen.DRIVER` rather than re-implemented.

    Its own docstring says why go needs it: go leads with a banner
    naming the package (`# opprobe`) and its diagnostics never contain
    the word `error`, so a rule that reads the first non-empty line
    records the banner and throws the compiler's testimony away.  It is
    defined inside that embedded text, not at module level, so it is
    sliced and compiled the same way `emulate.pipeline_extractor` slices
    `extract`."""
    import re
    import lane_gen as LG
    if "firstline" not in REFUSAL_READER:
        driver = LG.DRIVER
        start = driver.index("DIAG = re.compile")
        end = driver.index("def write_unit(")
        namespace = {"re": re}
        exec(compile(driver[start:end], "lane_gen.DRIVER[firstline]",
                     "exec"), namespace)
        REFUSAL_READER["firstline"] = namespace["firstline"]
    return REFUSAL_READER["firstline"](text)


def cleanup(work):
    """`go build` leaves a cache tree behind, so the whole directory is
    walked; `emulate.cleanup` unlinks one flat directory and would
    refuse this one."""
    for root, dirs, files in os.walk(work, topdown=False):
        for name in files:
            try:
                os.unlink(os.path.join(root, name))
            except OSError:
                pass
        for name in dirs:
            try:
                os.rmdir(os.path.join(root, name))
            except OSError:
                pass
    try:
        os.rmdir(work)
    except OSError:
        pass


def recorded_facts(label, key, raw_bytes, mnem):
    """`emulate.recorded_facts` with GO'S OWN ARGUMENT ORDER.

    RESTATED, NOT CALLED, and said out loud as the law requires.
    `emulate.recorded_facts` reads the arrival contract with
    `canon38_gate.arrival_contract("c", body_text)`, and
    `canon37_gate.sequences_for` answers with the SysV sequence for
    every language EXCEPT go -- which is why task o11's rust file could
    call it and relabel the record afterwards, and this one cannot: the
    ORDER ITSELF differs (`rax rbx rcx rdi rsi r8 ...` against
    `rdi rsi rdx rcx r8 r9`), and probe `arrival_registers_six` measured
    that order on this very toolchain.  Every other line here is that
    function's, unchanged."""
    import canon38_gate as G38
    import canon10_behaviour_check as BC10
    import ledger48 as L48
    body_text = "; ".join(mnem)
    body_bytes = " ".join(raw_bytes)
    entry_contract = G38.arrival_contract(TARGET, body_text)
    ship_lines = L48.split_lines(body_text)
    home, width = BC10.answer_home_from_real(ship_lines)
    if home is None:
        home = entry_contract.get("a")
        width = 64
    families = G38.arrival_family_list(entry_contract)
    return {
        "unit": label,
        "lang": TARGET,
        "n": key,
        "population": "emulation",
        "operator": None,
        "recorded_status": "emulation",
        "body_source": "the unit's own ship text",
        "body_text": body_text,
        "body_bytes": body_bytes,
        "entry_contract": entry_contract,
        "entry_contract_source": (
            "read off the unit's own ship text, in go's own "
            "argument-register order: a family arrives when the text "
            "reads it before it writes it"),
        "result_family": home,
        "result_width": width,
        "arrival_families": families,
    }


def expected_go_families(params):
    """the register each declared parameter arrives in under GO's own
    calling rule: general holders take rax, rbx, rcx, rdi, rsi, r8 in
    declaration order; float holders take xmm0 upwards.

    `emulate.expected_c_families` is the same function over the SysV
    sequence, and it cannot be reused because the sequence differs.
    Measured, probes `arrival_registers_six` and
    `arrival_registers_float`."""
    out = []
    general = 0
    vector = 0
    for param in params:
        if param["kind"] == "fp":
            out.append("xmm%d" % vector)
            vector = vector + 1
        else:
            if general >= len(GENERAL_ORDER_GO):
                raise E.Refused(E.CAUSE_ARITY,
                                "more general arrivals than go's own "
                                "argument sequence names")
            out.append(GENERAL_ORDER_GO[general])
            general = general + 1
    return out


# ==================================================================
# section 4: THE SPELLING TABLE   one row per rule, each with its probe
# ==================================================================
#
# Every row names the z3 DECLARATION KIND it is the spelling of (task
# o11's own key for its coverage table -- machine form, never a language
# operator token), the go text this renderer writes for it, the PROBE in
# `go_facts.json` that measured it, and that probe's carved body.  The
# body is not repeated here: `probe` is the key into that file, so the
# table cannot drift from the measurement.

SPELLINGS = [
    ("Z3_OP_BADD, Z3_OP_BSUB, Z3_OP_BMUL",
     "the plain operator on the unsigned holder",
     "plain_sum_u32, plain_difference_u32, plain_product_u64",
     "go's arithmetic on an unsigned holder wraps and carries no "
     "check at the ship flags, so the plain operator IS the term's "
     "meaning"),
    ("Z3_OP_BAND, Z3_OP_BOR, Z3_OP_BXOR",
     "the plain bitwise operator", "bitwise_three_u32",
     "one instruction each"),
    ("Z3_OP_BNEG", "unary minus on the unsigned holder",
     "plain_negate_u32", "wraps, one instruction"),
    ("Z3_OP_BNOT", "the caret prefix, go's own complement",
     "complement_u32", "one instruction"),
    ("Z3_OP_BSHL, Z3_OP_BLSHR",
     "the plain shift with the count MASKED to the width in the source",
     "plain_left_shift_u32, masked_left_shift_u32, "
     "masked_right_shift_u32",
     "unmasked, go emits its own out-of-range guard after the shift "
     "because it defines a count at or above the width as answering "
     "zero; masked, it emits the bare shift"),
    ("Z3_OP_BASHR",
     "the value converted to the signed holder, shifted, converted "
     "back", "masked_arith_shift_i32, masked_arith_shift_via_unsigned",
     "one instruction either way"),
    ("Z3_OP_BUDIV_I, Z3_OP_BUREM_I",
     "the plain operator on the unsigned holder",
     "plain_quotient_u32",
     "go checks the zero divisor and branches into runtime.panicdivide "
     "-- the EDGE REGION, rendered rather than hidden"),
    ("Z3_OP_BSDIV_I, Z3_OP_BSREM_I",
     "the plain operator on the signed holder",
     "plain_quotient_i32, plain_remainder_i32, plain_quotient_i64",
     "go checks the zero divisor AND the extreme case, which its own "
     "specification defines as wrapping -- both EDGE REGIONS"),
    ("Z3_OP_ITE", "a call to a helper function written into the same "
     "file", "select_u64, select_f64, nested_select_u64",
     "go has no conditional EXPRESSION; the helper inlines to a "
     "conditional move for integer arms and to a branch for float arms"),
    ("Z3_OP_EQ, Z3_OP_DISTINCT", "the plain comparison, through the "
     "conditional helper", "equality_u64", "one compare and one set"),
    ("Z3_OP_SLEQ .. Z3_OP_UGT", "the plain comparison on the converted "
     "holder", "compare_u32, signed_compare_i32",
     "one compare and one set"),
    ("Z3_OP_EXTRACT, Z3_OP_CONCAT",
     "the explicit conversion, and a shift joined by an or",
     "zero_extend_after_narrow, concat_shift_or_u64",
     "go converts explicitly and never implicitly"),
    ("Z3_OP_ZERO_EXT", "the explicit conversion to the wider holder",
     "widen_u8_to_u32", "one instruction"),
    ("Z3_OP_SIGN_EXT", "the conversion through the signed holder",
     "sign_extend_i8_to_i64", "one instruction"),
    ("Z3_OP_FPA_TO_IEEE_BV (a bare float arrival)",
     "the pointer cast", "f64_bits_unsafe, f32_bits_unsafe",
     "one instruction; a parameter is already a variable, so the "
     "pointer cast costs nothing here"),
    ("Z3_OP_FPA_TO_IEEE_BV (mid-expression or at the answer)",
     "the standard library's own function",
     "f64_bits_math, f32_bits_math",
     "go's pointer cast needs an addressable variable and a "
     "sub-expression is not one; both spellings put the value through "
     "memory in a rendered emulation, because the library function is "
     "itself a pointer cast over a local and go folds neither"),
    ("Z3_OP_FPA_TO_FP (bits reinterpreted)",
     "the standard library's own function",
     "bits_f64_math, bits_f64_unsafe, bits_f32_unsafe",
     "one instruction behind an inlining marker in isolation; in a "
     "rendered emulation the round trip costs a stack frame, which "
     "clang and rustc both fold away and go does not"),
    ("Z3_OP_FPA_TO_FP (value converted)",
     "the explicit conversion to the float holder",
     "int_to_f64, int32_to_f64, int32_to_f32, f32_to_f64, f64_to_f32",
     "go breaks the destination register's dependency with an `xorps` "
     "before an integer-to-float conversion, so that row is TWO "
     "instructions where c's and rust's is one"),
    ("Z3_OP_FPA_TO_FP_UNSIGNED",
     "the explicit conversion from the unsigned holder", "uint_to_f64",
     "eleven instructions: go's own unsigned-to-float sequence"),
    ("Z3_OP_FPA_TO_SBV, Z3_OP_FPA_TO_UBV",
     "the explicit conversion to the integer holder", "f64_to_int",
     "the bare truncating instruction, with none of the saturation "
     "sequence rust's plain conversion emits"),
    ("Z3_OP_FPA_ADD, Z3_OP_FPA_SUB, Z3_OP_FPA_MUL, Z3_OP_FPA_DIV",
     "the plain operator on the float holder", "sum_f32, sum_f64",
     "one instruction"),
    ("Z3_OP_FPA_ABS", "the sign bit cleared through the bit casts",
     "absolute_f64", "read, clear, write back"),
    ("the holders", "uint8..uint64, int8..int64, float32, float64",
     "wide_holder_128, float16_holder",
     "go has NO 128-bit integer holder and NO 16-bit float holder: the "
     "compiler answers \"undefined\" for both"),
    ("the arrival registers",
     "rax, rbx, rcx, rdi, rsi, r8 ... and xmm0 upwards",
     "arrival_registers_six, arrival_registers_float",
     "go's own argument sequence, which is why this target needs its "
     "own `expected_go_families` and its own `recorded_facts`"),
    ("the narrow arrival", "no assumption about the caller",
     "narrow_arrival_u8, narrow_arrival_u16, truth_arrival",
     "the go callee re-extends a narrow arrival itself, where c's and "
     "rust's assume the caller widened it"),
    ("the prologue", "none", "leaf_prologue",
     "a small leaf function carries no stack-growth prologue, so "
     "nothing of the kind sits in a carved emulation body"),
]


def spelling_rows():
    """the spelling table as records, each with the carved body of its
    own probe read out of `go_facts.json` -- so the table cannot drift
    from the measurement."""
    facts = {}
    if os.path.exists(FACTS):
        document = json.load(open(FACTS))
        for record in document.get("probes") or []:
            facts[record["name"]] = record
    out = []
    for kind, spelling, probes, note in SPELLINGS:
        bodies = []
        for name in probes.split(", "):
            record = facts.get(name)
            if record is None:
                bodies.append({"probe": name, "body": None})
                continue
            if record.get("built"):
                bodies.append({"probe": name,
                               "body": record["body_text"]})
                continue
            bodies.append({"probe": name,
                           "body": "NOT BUILT: %s"
                                   % (record.get("refusal") or {}).get(
                                       "the_pipelines_own_reading")})
        out.append({
            "z3_kind": kind,
            "spelling": spelling,
            "probes": probes,
            "what_it_emits": note,
            "measured": True,
            "bodies": bodies,
        })
    return out


def flags_command():
    say("the go ship flags this task compiles at: go %s"
        % " ".join(SHIP_ARGS))
    say("")
    say("their source, LITERAL:")
    say("   %s" % SHIP_FLAGS_SOURCE)
    say("")
    say("go.mod, LITERAL:")
    for line in GOMOD.splitlines():
        say("   %s" % line)
    say("")
    say("go's argument sequence, measured against the pipeline's own:")
    say("   %s" % json.dumps(sequence_agrees(), sort_keys=True))
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
