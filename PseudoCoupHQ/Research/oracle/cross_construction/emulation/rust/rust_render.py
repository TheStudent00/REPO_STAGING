#!/usr/bin/env python3
"""rust_render.py -- task o11: AutoPoly with RUST as the target.

Node: hq.research.arch_unit_oracle.cross_construction
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/CORE_0_3_2_2_cross_construction.md`,
FROZEN for term-level composition; task o7 opened the emulation route
with c as the target and this task adds a second target, which asks
the same question of a different compiler and does not unfreeze the
node).

THE OBJECTS, one sentence each, in relation.
  * An X UNIT is a pool member (`the_pool5.json`) in language x of
    {c, go, swift} whose entry has NO rust member, together with its
    canon40 record (the body verbatim, the arrival contract, the
    answer home) and its proved layer-4 term (the body as a z3
    expression).
  * An EMULATION is a rust function whose body is that term written
    in rust's own operations over rust's holders, produced by the ONE
    renderer below (`RustRenderer`, which DERIVES from task o7's
    `emulate.Renderer` and overrides one method per rule) from the z3
    term; a term the renderer cannot render is refused by cause and no
    source is written for it.
  * THE COLLAPSE TEST compiles the emulation at the rust corpus's own
    ship flags (`rustc --crate-type=lib --emit=obj -C opt-level=1
    -C debug-assertions=off`, read off `lane_gen.py` `compile_probe`'s
    rust branch), carves the function with the pipeline's own objdump
    reader (`lane_gen.extract`, through `emulate.pipeline_extractor`),
    puts it on the canonical form (`canonical_form.render_one`), builds
    its term (`term66_run.one_unit`), and asks three questions:
      Q1 BYTE identity: is the emulation's body byte-identical to some
         RUST unit of the corpus (and to one in the same entry, for
         the control)?
      Q2 TERM identity: is its layer-5 text the entry's?
      Q3 PROOF: does the gate prove it equal to the x unit's body?
    and, on the single-opcode rows of task o2, one more:
      Q0 does the chaff-stripped body come back as exactly the row's
         own arch opcode (LANDED), one other opcode
         (LANDED_ELSEWHERE), or more than one (NOT_COLLAPSED)?

WHAT IS REUSED RATHER THAN COPIED, said out loud.  Nothing under
`Research/op_pipeline/` is edited, and task o7's `emulate.py` is
imported, never forked:
  `emulate.Renderer`             -- DERIVED FROM; `RustRenderer` below
                                    overrides one method per row of
                                    the coverage table and inherits
                                    the width planning, the symbol
                                    check and the refusal causes.
  `emulate.pipeline_extractor`   -- the carve, unchanged.
  `emulate.prove_against_x`      -- Q3, unchanged, including its
                                    caller-extension re-pose.
  `emulate.recorded_facts`       -- the arch-unit facts off the ship
                                    text; `canon37_gate.sequences_for`
                                    returns the SysV sequence for both
                                    "c" and "rust", so the contract it
                                    reads is the same object, and this
                                    file only relabels the record's
                                    `lang` to "rust" afterwards so the
                                    runtime-callee bodies come from
                                    rustc's archive and not clang's.
  `emulate.collect` / `fork_one` -- the collector, its worker bound
                                    through the one assignment in
                                    `install_worker()` below, which is
                                    stated in the report.
  `emulate.Population`           -- DERIVED FROM; `RustPopulation`
                                    changes only which language is the
                                    target.
  `per_opcode.load_rows`         -- task o8's single-opcode rows.
  `single_opcode_units.strip_chaff` / `parse_insn` -- task o2's own
                                    narrow rule, unchanged.
  `cross2_length_two.parse_text` / `print_node` -- task o1's parser.

MEMORY BOUND, stated as the law requires: one collecting process,
peak checked after every emulation, named abort ABORT_MEMORY_O11 at
4 GB resident (this file's own `check_collector_memory`, bound into
`emulate` so the imported collector raises this task's name); one
forked sub-process per emulation under RLIMIT_AS 2,048 MB and a wall
clock of 240 s (a sub-process that passes either is recorded as a
runner limit, never as a verdict); at most 3 sub-processes at once.
The canon40 shards are streamed one at a time and dropped.

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

No operator token appears in this file as a key.  The population is a
set of pool entry ids read from task o1's length-one map (machine
form: pool membership by language); the coverage table's rows are
keyed by the z3 DECLARATION KIND NAME (`Z3_OP_BADD`) or by a z3 call
name (`Extract`), never by a language's operator spelling; the
per-opcode rows are keyed by arch mnemonic, task o2's own key; a
member's `operator` field rides onto a record as a DISPLAY LABEL and
is read by nothing.

Coding discipline: no compound one-liner statements.

usage:
  rust_render.py optable                the coverage table, from the corpus
  rust_render.py census                 population, indexes, held records
  rust_render.py sample <count>         the first stratified sample
  rust_render.py run                    every entry that passed the filters
  rust_render.py control <count>        entries WITH a rust member
  rust_render.py peropcode              task o8's question, rust as target
  rust_render.py report                 rust_results.json + rust_report.md
"""

import json
import os
import random
import resource
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
EMULATION = os.path.normpath(os.path.join(HERE, ".."))
CROSS = os.path.normpath(os.path.join(HERE, "..", ".."))
OP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                   "op_pipeline"))
ARCH_OPCODES = os.path.normpath(os.path.join(HERE, "..", "..", "..",
                                             "arch_opcodes"))
PER_OPCODE = os.path.join(EMULATION, "per_opcode")
sys.path.insert(0, OP)
sys.path.insert(0, CROSS)
sys.path.insert(0, EMULATION)
sys.path.insert(0, ARCH_OPCODES)
sys.path.insert(0, PER_OPCODE)

import z3                                                        # noqa: E402
import emulate as E                                              # noqa: E402

SRC_DIR = os.path.join(HERE, "src")
OPTABLE = os.path.join(HERE, "coverage_table.json")
POPULATION = os.path.join(HERE, "rust_population.json")
HELD = os.path.join(HERE, "rust_held.json")
INDEXES = os.path.join(HERE, "rust_indexes.json")
SAMPLE = os.path.join(HERE, "rust_sample.json")
RUN = os.path.join(HERE, "rust_run.json")
CONTROL = os.path.join(HERE, "rust_control.json")
PEROPCODE = os.path.join(HERE, "rust_peropcode.json")
RESULTS = os.path.join(HERE, "rust_results.json")
REPORT = os.path.join(HERE, "rust_report.md")
HOST_FOLDER = ("PseudoCoupHQ/Research/oracle/"
               "cross_construction/emulation/rust")

TARGET = "rust"
X_LANGUAGES = ["c", "go", "swift"]
# task o8's per-opcode question, asked of the same three source
# languages with rust as the target.
PER_OPCODE_LANGS = ["c", "go", "swift"]

RUSTC = "rustc"
# read off `lane_gen.py` compile_probe, the rust branch: the SHIP mode
# is `opt-level=1` with debug assertions OFF.
SHIP_FLAGS = ["--crate-type=lib", "--emit=obj", "-C", "opt-level=1",
              "-C", "debug-assertions=off"]
SHIP_FLAGS_SOURCE = ("lane_gen.py compile_probe, rust branch: "
                     "`opt = [\"-C\", \"opt-level=1\", \"-C\", "
                     "\"debug-assertions=off\"]` then "
                     "`[\"rustc\", \"--crate-type=lib\", \"--emit=obj\"] "
                     "+ opt + [\"-o\", obj, src]` -- the ship build of "
                     "every rust unit in the corpus")

COLLECTOR_CAP_KB = 4 * 1024 * 1024
SEED = 20260907
RUN_CEILING = 400

# ---------------------------------------------------------------------
# rust's holders, MEASURED rather than recalled: `rust_facts.json` /
# `rust_facts2.json` (lanes o11_l1, o11_l2) carry the emitted body of
# one probe per row.  f16 and f128 are refused by rustc 1.96.1 with
# "the type `f16` is unstable", so there is NO 16-bit float holder --
# the one place c's renderer has a holder and rust's has none.
# ---------------------------------------------------------------------

RU = {8: "u8", 16: "u16", 32: "u32", 64: "u64", 128: "u128"}
RI = {8: "i8", 16: "i16", 32: "i32", 64: "i64", 128: "i128"}
RF = {32: "f32", 64: "f64"}
PARAM_NAMES = E.PARAM_NAMES

RUST_PRELUDE = ("#![allow(dead_code, unused_parens, unused_unsafe, "
                "unconditional_panic, non_snake_case, "
                "overflowing_literals)]")

NO_F16 = ("rust has no %d-bit float holder: rustc 1.96.1 refuses f16 "
          "and f128 with \"the type is unstable\" (measured, lane "
          "o11_l2)")


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_collector_memory():
    """this task's own ceiling and its own named abort; bound into
    `emulate` by `install_worker()` so the imported collector raises
    ABORT_MEMORY_O11 and not o7's name."""
    used = peak_kb()
    if used > COLLECTOR_CAP_KB:
        raise SystemExit(
            "ABORT_MEMORY_O11: the collecting process's peak resident "
            "%d kB passed the stated bound of %d kB"
            % (used, COLLECTOR_CAP_KB))
    return used


def write_json(path, document):
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()


def read_json(path):
    handle = open(path)
    document = json.load(handle)
    handle.close()
    return document


# ==================================================================
# section 1: RUST SOURCE PIECES   literals, masks, sign extension
# ==================================================================

def rlit(value, bits):
    """a rust literal of the unsigned type of `bits` holding `value`."""
    value = value & ((1 << bits) - 1)
    return "0x%x%s" % (value, RU[bits])


def rmask(text, width):
    """`text`, of the promoted unsigned type of `width`, with the bits
    above `width` cleared."""
    bits = E.promoted_bits(width)
    if width == bits:
        return "((%s) as %s)" % (text, RU[bits])
    return "(((%s) as %s) & %s)" % (text, RU[bits],
                                    rlit((1 << width) - 1, bits))


def rsign(text, width, bits):
    """`text` (width bits, promoted unsigned type) as a SIGNED value of
    the promoted type `bits`, sign bit `width - 1` propagated.  Rust
    has no implicit widening, so every step is an explicit `as`."""
    if width == bits:
        return "((%s) as %s)" % (text, RI[bits])
    shift = bits - width
    return "(((((%s) as %s) << %d) as %s) >> %d)" % (
        text, RU[bits], shift, RI[bits], shift)


# ==================================================================
# section 2: THE RENDERER   z3 term -> rust source
# ==================================================================

class RustRenderer(E.Renderer):
    """the ONE rust renderer: a z3 term over `seed_<family>` symbols ->
    one rust translation unit.  DERIVES from task o7's
    `emulate.Renderer` and overrides one method per row of the
    coverage table; the width planning, the free-symbol check and the
    refusal causes are inherited unchanged.

    attributes:
        families        the x unit's arrival families, IN order
        result_family   the x unit's answer home
        result_width    its width in bits
        params          per family: name, holder text, kind, bits
        blocks          a counter, so each division's block names its
                        two bindings uniquely
    methods:
        render          -> (source text, function symbol)
        emit            one node -> (text, kind, width)
    """

    def __init__(self, families, result_family, result_width, label):
        E.Renderer.__init__(self, families, result_family, result_width,
                            label)
        self.blocks = 0

    # -- the parameter plan -------------------------------------------

    def plan_parameters(self, term):
        """the base class plans the WIDTH of every arrival from how the
        term reads it; only the holder text is rust's."""
        E.Renderer.plan_parameters(self, term)
        for param in self.params:
            if param["kind"] == "fp":
                if param["bits"] not in RF:
                    raise E.Refused(E.CAUSE_WIDTH, NO_F16 % param["bits"])
                param["holder"] = RF[param["bits"]]
                continue
            if param["bits"] not in RU:
                raise E.Refused(E.CAUSE_WIDTH, "%d bits" % param["bits"])
            param["holder"] = RU[param["bits"]]

    # -- the source ---------------------------------------------------

    def render(self, term, text):
        self.plan_parameters(term)
        self.check_symbols(term)
        root_text, root_kind, root_width = self.emit(term)
        return_type, body = self.answer(root_text, root_kind, root_width)
        symbol = "emu_%s" % self.label
        params = []
        for param in self.params:
            params.append("%s: %s" % (param["name"], param["holder"]))
        lines = []
        lines.append(RUST_PRELUDE)
        lines.append("")
        lines.append("// task o11 emulation -- rendered by rust_render.py")
        lines.append("// RustRenderer from the layer-4 term of %s."
                     % self.label)
        lines.append("// The term's layer-5 text, LITERAL:")
        lines.append("//   %s" % " ".join(text.split()))
        lines.append("#[no_mangle]")
        lines.append("pub extern \"C\" fn %s(%s) -> %s"
                     % (symbol, ", ".join(params), return_type))
        lines.append("{")
        lines.append("    %s" % body)
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
            if width not in RF:
                raise E.Refused(E.CAUSE_WIDTH, NO_F16 % width)
            return_type = RF[width]
            if root_kind == "fp":
                if root_width != width:
                    raise E.Refused(E.CAUSE_WIDTH,
                                    "fp answer %d bits, home %d"
                                    % (root_width, width))
                return return_type, root_text
            return return_type, "%s::from_bits((%s) as %s)" % (
                return_type, root_text, RU[width])
        if family.startswith("st") or family.startswith("x87"):
            raise E.Refused(E.CAUSE_X87, family)
        if width not in RU:
            raise E.Refused(E.CAUSE_WIDTH, "answer %d bits" % width)
        return_type = RU[width]
        if root_kind == "fp":
            return return_type, "((%s).to_bits() as %s)" % (root_text,
                                                            return_type)
        return return_type, "((%s) as %s)" % (root_text, return_type)

    # -- one node -----------------------------------------------------

    def emit(self, node):
        """-> (rust text, kind, width).  kind is bv (text of the
        promoted unsigned type, bits above `width` zero), fp (f32/f64
        of `width` bits) or bool (a rust `bool`).  The three cases
        below are the ones whose SPELLING differs from c; everything
        else goes through the base class's dispatch, which calls this
        object's own `emit_*` overrides."""
        decl = node.decl()
        kind = decl.kind()
        if z3.is_const(node) and kind == z3.Z3_OP_UNINTERPRETED:
            return self.emit_symbol(node, None)
        if kind == z3.Z3_OP_BNUM:
            width = node.size()
            bits = E.promoted_bits(width)
            return rlit(node.as_long(), bits), "bv", width
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
            text = "(%s as %s)" % (param["name"], RU[bits])
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
            return rmask("(%s) >> %d" % (text, low), high - low + 1), \
                "bv", high - low + 1
        # a vector arrival planned as a float holder: its bits.  Rust
        # reads them with `to_bits`, so the memcpy helper c needs has
        # no counterpart here and `self.helpers` stays empty.
        bits = E.promoted_bits(param["bits"])
        text = "((%s).to_bits() as %s)" % (param["name"], RU[bits])
        if extract is None:
            raise E.Refused(E.CAUSE_LANE, name)
        high, low = extract
        if low == 0 and high + 1 == param["bits"]:
            return text, "bv", param["bits"]
        return rmask("(%s) >> %d" % (text, low), high - low + 1), \
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
        shifted = "((%s) as %s) >> %d" % (text, RU[inner_bits], low)
        return rmask(shifted, out), "bv", out

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
            piece = "(((%s) as %s) << %d)" % (text, RU[bits], shift)
            if shift == 0:
                piece = "((%s) as %s)" % (text, RU[bits])
            pieces.append(piece)
        return rmask(" | ".join(pieces), total), "bv", total

    def emit_extend(self, node, signed):
        extra = node.params()[0]
        text, kind, width = self.emit(node.arg(0))
        self.expect(kind, "bv", node)
        total = width + extra
        bits = E.promoted_bits(total)
        if not signed:
            return "((%s) as %s)" % (text, RU[bits]), "bv", total
        return rmask(self.sign_extended(text, width, bits), total), \
            "bv", total

    def sign_extended(self, text, width, bits):
        return rsign(text, width, bits)

    def emit_ite(self, node):
        cond, ckind, _ = self.emit(node.arg(0))
        self.expect(ckind, "bool", node)
        left, lkind, lwidth = self.emit(node.arg(1))
        right, rkind, rwidth = self.emit(node.arg(2))
        if lkind != rkind or lwidth != rwidth:
            raise E.Refused(E.CAUSE_OP, "If with arms of different sorts")
        if lkind == "bv":
            bits = E.promoted_bits(lwidth)
            return "(if (%s) { ((%s) as %s) } else { ((%s) as %s) })" % (
                cond, left, RU[bits], right, RU[bits]), "bv", lwidth
        return "(if (%s) { (%s) } else { (%s) })" % (cond, left, right), \
            lkind, lwidth

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
        sign = "==" if kind == z3.Z3_OP_EQ else "!="
        if lkind == "bool":
            return "((%s) %s (%s))" % (left, sign, right), "bool", 1
        bits = E.promoted_bits(lwidth)
        return "(((%s) as %s) %s ((%s) as %s))" % (
            left, RU[bits], sign, right, RU[bits]), "bool", 1

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
            left = rsign(left, lwidth, bits)
            right = rsign(right, rwidth, bits)
        else:
            left = "((%s) as %s)" % (left, RU[bits])
            right = "((%s) as %s)" % (right, RU[bits])
        return "((%s) %s (%s))" % (left, signs[kind], right), "bool", 1

    def emit_arith(self, node, kind):
        """the WRAPPING method, never the plain operator.  Measured
        (lane o11_l1): at the corpus's ship flags -- which carry
        `-C debug-assertions=off` -- plain `+` and `a.wrapping_add(b)`
        emit the same body; at `debug-assertions=on` the plain form
        emits a branch to `panic_const_add_overflow`.  The renderer
        must not depend on a flag, so it always writes the wrapping
        form, which is the term's own meaning."""
        methods = {
            z3.Z3_OP_BADD: "wrapping_add",
            z3.Z3_OP_BSUB: "wrapping_sub",
            z3.Z3_OP_BMUL: "wrapping_mul",
        }
        bitwise = {
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
            cast.append("((%s) as %s)" % (text, RU[bits]))
        if kind in bitwise:
            joined = (" %s " % bitwise[kind]).join(cast)
            return rmask(joined, width), "bv", width
        joined = cast[0]
        for text in cast[1:]:
            joined = "(%s).%s(%s)" % (joined, methods[kind], text)
        return rmask(joined, width), "bv", width

    def emit_unary(self, node, kind):
        text, akind, width = self.emit(node.arg(0))
        self.expect(akind, "bv", node)
        bits = E.promoted_bits(width)
        cast = "((%s) as %s)" % (text, RU[bits])
        if kind == z3.Z3_OP_BNOT:
            return rmask("!%s" % cast, width), "bv", width
        return rmask("(%s).wrapping_neg()" % cast, width), "bv", width

    def emit_shift(self, node, kind):
        """the WRAPPING shift inside the term's own out-of-range guard.
        Measured (lane o11_l1): at ship flags plain `a << b` and
        `a.wrapping_shl(b)` emit the same `shl %cl,%eax`; at
        `debug-assertions=on` the plain form branches to
        `panic_const_shl_overflow`.  Neither spells the TERM's rule,
        which is that a count at or above the width answers with the
        fill, so the guard is written out -- exactly as the c renderer
        writes it."""
        value, vkind, width = self.emit(node.arg(0))
        amount, akind, awidth = self.emit(node.arg(1))
        self.expect(vkind, "bv", node)
        self.expect(akind, "bv", node)
        bits = E.promoted_bits(width)
        abits = E.promoted_bits(awidth)
        count = "(((%s) as %s) as u32)" % (amount, RU[abits])
        bound = E.upper_bound(node.arg(1))
        if kind == z3.Z3_OP_BSHL:
            plain = rmask("((%s) as %s).wrapping_shl(%s)"
                          % (value, RU[bits], count), width)
            fill = "(0 as %s)" % RU[bits]
        elif kind == z3.Z3_OP_BLSHR:
            plain = rmask("((%s) as %s).wrapping_shr(%s)"
                          % (value, RU[bits], count), width)
            fill = "(0 as %s)" % RU[bits]
        else:
            signed_value = rsign(value, width, bits)
            plain = rmask("(%s).wrapping_shr(%s)" % (signed_value, count),
                          width)
            fill = "(if (%s) < 0 { %s } else { 0 as %s })" % (
                signed_value, rlit((1 << width) - 1, bits), RU[bits])
        if bound is not None and bound < width:
            return plain, "bv", width
        guard = "(((%s) as %s) < (%s))" % (amount, RU[abits],
                                           rlit(width, abits))
        return "(if %s { %s } else { %s })" % (guard, plain, fill), \
            "bv", width

    def emit_division(self, node, kind):
        """the divide under an UNREACHABLE hint.  Measured (lanes
        o11_l1, o11_l3, o11_l4): rust's `/` and `%` check for a zero
        divisor in BOTH builds -- the check is not a debug assertion --
        and the signed forms check the extreme (the most negative value
        over minus one) as well; each check is a branch to a panic
        routine, which is not in the term.  `core::hint::
        unreachable_unchecked` under the exact conditions the machine's
        own divide leaves undefined removes both, and the emitted body
        is the bare `div` / `idiv` the c renderer's plain `/` gets from
        clang."""
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
        sign = "%" if remainder else "/"
        self.blocks = self.blocks + 1
        tag = self.blocks
        if signed:
            if lwidth not in RI:
                raise E.Refused(E.CAUSE_WIDTH,
                                "signed division at %d bits" % lwidth)
            holder = RI[lwidth]
            numerator = "((%s) as %s)" % (rsign(left, lwidth, bits),
                                          holder)
            divisor = "((%s) as %s)" % (rsign(right, rwidth, bits),
                                        holder)
            block = ("{ let n%d: %s = %s; let d%d: %s = %s; "
                     "unsafe { if d%d == 0 || (n%d == %s::MIN && "
                     "d%d == -1) { core::hint::unreachable_unchecked(); "
                     "} } n%d %s d%d }"
                     % (tag, holder, numerator, tag, holder, divisor,
                        tag, tag, holder, tag, tag, sign, tag))
            return rmask("(%s)" % block, lwidth), "bv", lwidth
        holder = RU[bits]
        numerator = "((%s) as %s)" % (left, holder)
        divisor = "((%s) as %s)" % (right, holder)
        block = ("{ let n%d: %s = %s; let d%d: %s = %s; "
                 "unsafe { if d%d == 0 { "
                 "core::hint::unreachable_unchecked(); } } n%d %s d%d }"
                 % (tag, holder, numerator, tag, holder, divisor, tag,
                    tag, sign, tag))
        return rmask("(%s)" % block, lwidth), "bv", lwidth

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
            if width not in RF:
                raise E.Refused(E.CAUSE_WIDTH, NO_F16 % width)
            bits_value = z3.simplify(z3.fpToIEEEBV(node)).as_long()
            if bits_value == 0:
                zero = {32: "(0.0f32)", 64: "(0.0f64)"}
                return zero[width], "fp", width
            return "%s::from_bits(%s)" % (RF[width],
                                          rlit(bits_value, width)), \
                "fp", width
        if kind == z3.Z3_OP_FPA_TO_FP:
            return self.emit_to_fp(node)
        if kind == z3.Z3_OP_FPA_TO_FP_UNSIGNED:
            self.expect_rne(node.arg(0))
            text, akind, awidth = self.emit(node.arg(1))
            self.expect(akind, "bv", node)
            width = E.fp_width(node.sort())
            if width not in RF:
                raise E.Refused(E.CAUSE_WIDTH, NO_F16 % width)
            bits = E.promoted_bits(awidth)
            return "(((%s) as %s) as %s)" % (text, RU[bits], RF[width]), \
                "fp", width
        if kind == z3.Z3_OP_FPA_TO_IEEE_BV:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            bits = E.promoted_bits(awidth)
            return "((%s).to_bits() as %s)" % (text, RU[bits]), \
                "bv", awidth
        if kind in (z3.Z3_OP_FPA_TO_SBV, z3.Z3_OP_FPA_TO_UBV):
            rm = node.arg(0)
            if rm.decl().kind() != z3.Z3_OP_FPA_RM_TOWARD_ZERO:
                raise E.Refused(E.CAUSE_RM,
                                "%s under %s (rust's to_int_unchecked "
                                "truncates)" % (name, rm.decl().name()))
            text, akind, awidth = self.emit(node.arg(1))
            self.expect(akind, "fp", node)
            width = node.size()
            if width not in RI:
                raise E.Refused(E.CAUSE_WIDTH, "%s to %d bits"
                                % (name, width))
            table = RI if kind == z3.Z3_OP_FPA_TO_SBV else RU
            # `as` SATURATES in rust (measured, lane o11_l1: seven
            # instructions with a NaN case); `to_int_unchecked` is the
            # truncating cast the machine's own cvtt* does, and is the
            # rule c's plain cast gets for free.
            return rmask("unsafe { (%s).to_int_unchecked::<%s>() }"
                         % (text, table[width]), width), "bv", width
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
            if awidth not in RF:
                raise E.Refused(E.CAUSE_WIDTH, NO_F16 % awidth)
            mask = (1 << (awidth - 1)) - 1
            return "%s::from_bits((%s).to_bits() & %s)" % (
                RF[awidth], text, rlit(mask, awidth)), "fp", awidth
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
            zero = {32: "(0.0f32)", 64: "(0.0f64)"}
            if awidth not in zero:
                raise E.Refused(E.CAUSE_WIDTH, NO_F16 % awidth)
            return "((%s) == %s)" % (text, zero[awidth]), "bool", 1
        if kind == z3.Z3_OP_FPA_IS_INF:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            sort = node.arg(0).sort()
            mask = (1 << (awidth - 1)) - 1
            infinity = ((1 << sort.ebits()) - 1) << (sort.sbits() - 1)
            return "(((%s).to_bits() & %s) == %s)" % (
                text, rlit(mask, awidth), rlit(infinity, awidth)), \
                "bool", 1
        if kind == z3.Z3_OP_FPA_IS_NEGATIVE:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            return "(((%s).to_bits() >> %d) != 0)" % (text, awidth - 1), \
                "bool", 1
        if kind == z3.Z3_OP_FPA_IS_POSITIVE:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            return "(((%s).to_bits() >> %d) == 0)" % (text, awidth - 1), \
                "bool", 1
        raise E.Refused(E.CAUSE_OP, "%s (kind %d)" % (name, kind))

    def emit_to_fp(self, node):
        width = E.fp_width(node.sort())
        if width not in RF:
            raise E.Refused(E.CAUSE_WIDTH, NO_F16 % width)
        if node.num_args() == 1:
            child = node.arg(0)
            # the shortcut: the bits of a float arrival, read whole
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
            return "%s::from_bits((%s) as %s)" % (RF[width], text,
                                                  RU[width]), "fp", width
        if node.num_args() == 2:
            self.expect_rne(node.arg(0))
            text, akind, awidth = self.emit(node.arg(1))
            if akind == "fp":
                return "((%s) as %s)" % (text, RF[width]), "fp", width
            if akind == "bv":
                bits = E.promoted_bits(awidth)
                return "((%s) as %s)" % (rsign(text, awidth, bits),
                                         RF[width]), "fp", width
        raise E.Refused(E.CAUSE_OP, "fpToFP with %d arguments"
                        % node.num_args())


# ==================================================================
# section 3: COMPILE AND CARVE   rustc at the corpus's ship flags
# ==================================================================

def compile_and_carve(source, symbol):
    """the rust corpus's own ship compile and carve: rustc at
    SHIP_FLAGS, objdump read by `emulate.pipeline_extractor()`, which
    is `lane_gen.DRIVER`'s own `extract`."""
    extract = E.pipeline_extractor()
    work = tempfile.mkdtemp(prefix="o11_", dir=os.environ.get("TMPDIR"))
    src = os.path.join(work, "unit.rs")
    obj = os.path.join(work, "unit_ship.o")
    handle = open(src, "w")
    handle.write(source)
    handle.close()
    command = [RUSTC] + SHIP_FLAGS + ["-o", obj, src]
    done = subprocess.run(command, capture_output=True, text=True,
                          timeout=180)
    if done.returncode != 0 or not os.path.exists(obj):
        E.cleanup(work)
        return None, E.firstline(done.stderr or done.stdout)
    done = subprocess.run(["objdump", "-dr", "--disassemble=" + symbol,
                           obj], capture_output=True, text=True,
                          timeout=180)
    got = extract(done.stdout, symbol, True)
    E.cleanup(work)
    if got is None:
        return None, "objdump found no symbol %s" % symbol
    return got, None


def recorded_facts(label, key, raw_bytes, mnem):
    """task o7's `emulate.recorded_facts`, unchanged, then relabelled.
    `canon37_gate.sequences_for` returns the SysV sequence for both
    "c" and "rust", so the arrival contract it reads is the same
    object; the `lang` field is set to rust afterwards because
    `term.py` reads it to pick the toolchain whose runtime-callee
    bodies a `call` resolves to, and rustc's archive is the one this
    emulation was linked against."""
    recorded = E.recorded_facts(label, key, raw_bytes, mnem)
    recorded["lang"] = TARGET
    return recorded


# ==================================================================
# section 4: THE POPULATION   rust as the target
# ==================================================================

class RustPopulation(E.Population):
    """task o7's `emulate.Population` with rust as the target: the same
    three filters, the same member choice, over the entries that have
    a c, go or swift member and NO rust member."""

    def select(self):
        candidates = {}
        for x in X_LANGUAGES:
            cell = self.cross1["pairs"]["%s|%s" % (TARGET, x)]
            for entry_id in cell["not_built_entry_ids"]:
                candidates.setdefault(entry_id, set()).add(x)
        self.count_filter("P1 an x member and no rust member (o1's "
                          "rust|x not-built sets)", candidates)
        with_text = {}
        for entry_id, xs in candidates.items():
            entry = self.entry_by_id[entry_id]
            if entry.get("layer5_normalized_texts"):
                with_text[entry_id] = xs
        self.count_filter("P2 the entry carries a layer-5 text",
                          with_text)
        import cross2_length_two as C2
        round_trips = {}
        chosen = {}
        for entry_id, xs in with_text.items():
            entry = self.entry_by_id[entry_id]
            member = self.choose_member(entry, xs)
            if member is None:
                continue
            text = member["layer5_normalized_text"]
            try:
                node = C2.parse_text(text)
                ok = C2.print_node(node) == text
            except Exception:                              # noqa: BLE001
                ok = False
            chosen[entry_id] = (member, ok)
            if ok:
                round_trips[entry_id] = xs
        self.count_filter("P3 task o1's parser round-trips the chosen "
                          "member's text", round_trips)
        for entry_id, xs in with_text.items():
            member, ok = chosen.get(entry_id, (None, False))
            if member is None:
                continue
            entry = self.entry_by_id[entry_id]
            self.entries[entry_id] = {
                "entry_id": entry_id,
                "x_langs": sorted(xs),
                "x_lang": member["lang"],
                "x_unit": member["unit"],
                "text": member["layer5_normalized_text"],
                "entry_texts": list(entry["layer5_normalized_texts"]),
                "type_key": entry.get("type_key"),
                "round_trips": ok,
                "result_width": member.get("result_width"),
                "target_units_in_entry": [],
            }
        return self.entries

    def select_control(self, count):
        """`count` entries that DO have a rust member and a text, drawn
        uniformly with a stated seed; the rust member is the
        representative when it is rust, else the first rust member."""
        eligible = []
        for entry in self.pool["entries"]:
            if not entry.get("layer5_normalized_texts"):
                continue
            members = []
            for member in entry["members"]:
                if member["lang"] != TARGET:
                    continue
                if not member.get("layer5_normalized_text"):
                    continue
                if not member.get("layer5_merge_eligible"):
                    continue
                members.append(member)
            if not members:
                continue
            chosen = members[0]
            for member in members:
                if member["unit"] == entry.get("representative"):
                    chosen = member
            eligible.append((entry["entry_id"], chosen, members))
        eligible.sort(key=lambda item: item[0])
        rng = random.Random(SEED)
        drawn = rng.sample(eligible, min(count, len(eligible)))
        drawn.sort(key=lambda item: item[0])
        for entry_id, chosen, members in drawn:
            self.control[entry_id] = {
                "entry_id": entry_id,
                "x_langs": [TARGET],
                "x_lang": TARGET,
                "x_unit": chosen["unit"],
                "text": chosen["layer5_normalized_text"],
                "entry_texts": list(
                    self.entry_by_id[entry_id]["layer5_normalized_texts"]),
                "type_key": self.entry_by_id[entry_id].get("type_key"),
                "round_trips": True,
                "result_width": chosen.get("result_width"),
                "target_units_in_entry": [m["unit"] for m in members],
            }
        return len(eligible)

    def count_filter(self, label, mapping):
        row = {"filter": label, "distinct": len(mapping)}
        for x in X_LANGUAGES:
            row[x] = 0
        for entry_id, xs in mapping.items():
            for x in xs:
                row[x] = row[x] + 1
        self.filters.append(row)
        say("   %-64s c %4d  go %4d  swift %4d  distinct %4d"
            % (label, row["c"], row["go"], row["swift"], row["distinct"]))

    def stratified_sample(self, count):
        by_x = {}
        for x in X_LANGUAGES:
            by_x[x] = []
        for entry_id in sorted(self.entries):
            if not self.entries[entry_id]["round_trips"]:
                continue
            by_x[self.entries[entry_id]["x_lang"]].append(entry_id)
        want = {}
        share = count // len(X_LANGUAGES)
        for x in X_LANGUAGES:
            want[x] = share
        want[X_LANGUAGES[0]] = count - share * (len(X_LANGUAGES) - 1)
        rng = random.Random(SEED)
        picked = []
        shortfall = 0
        for x in X_LANGUAGES:
            have = by_x[x]
            take = min(want[x], len(have))
            shortfall = shortfall + want[x] - take
            picked.extend(rng.sample(have, take))
        if shortfall:
            largest = max(X_LANGUAGES, key=lambda x: len(by_x[x]))
            rest = [e for e in by_x[largest] if e not in picked]
            picked.extend(rng.sample(rest, min(shortfall, len(rest))))
        return sorted(picked)


def build_indexes(needed_units):
    """stream every canon40 shard once: the RUST body-bytes index (the
    corpus Q1 is asked against), and the canon40 record of every unit
    this task needs."""
    bytes_index = {}
    held = {}
    shard_of = {}
    target_units = 0
    for path in E.canon40_shards():
        document = read_json(path)
        for name, record in document["units"].items():
            lang = record.get("lang")
            if lang == TARGET and record.get("body_bytes"):
                key = record["body_bytes"]
                bytes_index.setdefault(key, []).append(name)
                target_units = target_units + 1
            if name in needed_units:
                held[name] = record
                shard_of[name] = os.path.basename(path)
        del document
        check_collector_memory()
    return bytes_index, held, shard_of, target_units


# ==================================================================
# section 5: THE WORKER   one entry's whole work, inside the fork
# ==================================================================

def install_worker():
    """bind this task's worker and its memory ceiling into task o7's
    collector.  `emulate.fork_one` calls the module-global
    `one_emulation`, and `emulate.collect` calls the module-global
    `check_collector_memory`; these two assignments are the ONLY way
    the imported collector is changed, and nothing in emulate.py is
    edited on disk."""
    E.one_emulation = one_job
    E.check_collector_memory = check_collector_memory


def one_job(shared, job):
    if job.get("job_kind") == "per_opcode":
        return one_polyfill(shared, job)
    return one_emulation(shared, job)


def transcribe_x(shared, job, record):
    """the x unit's canon40 record and its term, with the reprint
    check task o7 added; -> (x_record, x_term, walked) or None with the
    refusal already written onto `record`."""
    maker = shared["maker"]
    held = shared["held"]
    x_unit = job["x_unit"]
    x_record = held.get(x_unit)
    if x_record is None:
        record["rendered"] = False
        record["refusal_cause"] = E.CAUSE_NO_TERM
        record["refusal_detail"] = "no canon40 record held for %s" % x_unit
        return None
    record["x_arrival_families"] = list(x_record.get("arrival_families")
                                        or [])
    record["x_result_family"] = x_record.get("result_family")
    record["x_result_width"] = x_record.get("result_width")
    record["x_body_text"] = x_record.get("body_text")
    record["x_body_bytes"] = x_record.get("body_bytes")
    unit = dict(x_record)
    unit["unit"] = x_unit
    walked = maker.transcribe(unit)
    if walked.refused is not None or walked.out_term is None:
        record["rendered"] = False
        record["refusal_cause"] = E.CAUSE_NO_TERM
        if walked.refused is not None:
            record["refusal_detail"] = "the relink refused: %s" % \
                walked.refused
        else:
            import regate64_run as RG
            record["refusal_detail"] = RG.why_no_term(walked)
        return None
    x_term = walked.out_term
    reprinted = maker.normalize(x_term)
    record["x_reprinted_text"] = reprinted
    record["reprint_exact"] = reprinted == job["text"]
    if not record["reprint_exact"]:
        same = E.commutative_canonical(reprinted) == \
            E.commutative_canonical(job["text"])
        record["reprint_same_up_to_commutative_order_and_variable_index"] \
            = same
        if not same:
            record["rendered"] = False
            record["refusal_cause"] = E.CAUSE_REPRINT
            record["refusal_detail"] = reprinted
            return None
    return x_record, x_term, walked


def render_compile_carve(job, record, x_record, x_term, label):
    """render the term into rust, write the source, compile at the ship
    flags, carve; -> (renderer, raw_bytes, mnem) or None with the
    refusal already written onto `record`."""
    import term as T
    ordered = T.order_commutative(z3.simplify(x_term))
    families, omitted = E.families_the_term_reads(x_record, x_term)
    record["x_in_rows"] = families
    record["x_contract_omits"] = omitted
    renderer = RustRenderer(families, x_record.get("result_family"),
                            x_record.get("result_width"), label)
    try:
        source, symbol = renderer.render(ordered, job["text"])
    except E.Refused as refusal:
        record["rendered"] = False
        record["refusal_cause"] = refusal.cause
        record["refusal_detail"] = refusal.detail
        return None
    record["rendered"] = True
    record["params"] = renderer.params
    record["source_path"] = os.path.join("src", label + ".rs")
    record["source"] = source
    handle = open(os.path.join(SRC_DIR, label + ".rs"), "w")
    handle.write(source)
    handle.close()
    got, refusal = compile_and_carve(source, symbol)
    if got is None:
        record["compiled"] = False
        record["compile_refusal"] = refusal
        return None
    record["compiled"] = True
    raw_bytes, mnem = got
    record["body_bytes"] = " ".join(raw_bytes)
    record["body_text"] = "; ".join(mnem)
    record["body_byte_count"] = len(raw_bytes)
    return renderer, raw_bytes, mnem


def one_emulation(shared, job):
    """the whole of one entry's work: transcribe x, render, compile,
    carve, wrap, gate, term, Q1, Q2, Q3.  Runs inside the fork."""
    import term66_run as TR
    import canonical_form as CF
    import pool100_entry_equivalence as P100
    import gate as G
    maker = shared["maker"]
    gate = shared["gate"]
    form = shared["form"]
    reference = shared["reference"]
    bytes_index = shared["bytes_index"]
    text_to_entries = shared["text_to_entries"]
    unit_to_entry = shared["unit_to_entry"]
    entry_id = job["entry_id"]
    record = {
        "entry_id": entry_id,
        "x_lang": job["x_lang"],
        "x_unit": job["x_unit"],
        "x_text": job["text"],
        "entry_texts": job["entry_texts"],
        "type_key": job["type_key"],
        "control": job.get("control", False),
    }
    walked_all = transcribe_x(shared, job, record)
    if walked_all is None:
        return record
    x_record, x_term, walked = walked_all
    label = "%s__%s" % (entry_id, E.sanitize(job["x_unit"]))
    if job.get("control"):
        label = "control__" + label
    built = render_compile_carve(job, record, x_record, x_term, label)
    if built is None:
        return record
    renderer, raw_bytes, mnem = built
    # Q1: byte identity against the rust corpus, and against the entry
    matched = list(bytes_index.get(record["body_bytes"], []))
    matched_entries = sorted(set(unit_to_entry.get(name, "not in pool")
                                 for name in matched))
    record["q1"] = {
        "verdict": "BYTE_IDENTICAL" if matched
                   else "NO_RUST_UNIT_WITH_THESE_BYTES",
        "matched_target_units": matched,
        "matched_entries": matched_entries,
        "same_entry": entry_id in matched_entries,
    }
    # the canonical form and the term, the pipeline's own way
    emu_label = "rust/" + label
    recorded = recorded_facts(emu_label, label, raw_bytes, mnem)
    record["target_arrival_families"] = recorded["arrival_families"]
    record["target_result_family"] = recorded["result_family"]
    record["target_result_width"] = recorded["result_width"]
    canon = CF.render_one(form, gate, recorded)
    canon["unit"] = emu_label
    record["canon40_outcome"] = canon.get("outcome")
    record["canon40_detail"] = canon.get("verdict_detail")
    term_record = TR.one_unit(maker, gate, emu_label, canon)
    record["term_state"] = term_record.get("term_state")
    record["term_outcome"] = term_record.get("outcome")
    record["term_reason"] = term_record.get("reason") or \
        term_record.get("why_no_term")
    layer5 = term_record.get("layer5_normalized_text")
    record["layer5_text"] = layer5
    lands = []
    if layer5 is not None:
        lands = list(text_to_entries.get(layer5, []))
    if layer5 is None:
        q2 = "NO_LAYER5_TEXT"
    elif layer5 in job["entry_texts"]:
        q2 = "TERM_IDENTICAL"
    else:
        q2 = "TERM_DIFFERS"
    record["q2"] = {"verdict": q2, "lands_in_entries": lands,
                    "result_width_differs":
                        recorded["result_width"] != x_record.get(
                            "result_width")}
    # Q3: the gate over the two bodies, o7's own routine unchanged
    record["q3"] = E.prove_against_x(reference, gate, maker, canon,
                                     x_record, renderer.params, x_term,
                                     walked, P100, G, record["x_in_rows"])
    return record


def one_polyfill(shared, job):
    """task o8's question with rust as the target: one single-opcode row
    rendered to rust, compiled, chaff-stripped by task o2's own narrow
    rule, and asked whether exactly the row's own arch opcode remains."""
    import single_opcode_units as SOU
    import canonical_form as CF
    import pool100_entry_equivalence as P100
    import gate as G
    gate = shared["gate"]
    form = shared["form"]
    maker = shared["maker"]
    reference = shared["reference"]
    record = {
        "entry_id": job["entry_id"],
        "x_lang": job["x_lang"],
        "x_unit": job["x_unit"],
        "x_text": job["text"],
        "mnem": job["mnem"],
        "row_body_text": job["row_body_text"],
        "member_count": job["member_count"],
        "job_kind": "per_opcode",
    }
    walked_all = transcribe_x(shared, job, record)
    if walked_all is None:
        return record
    x_record, x_term, walked = walked_all
    label = "opcode_%s" % E.sanitize(job["entry_id"])
    built = render_compile_carve(job, record, x_record, x_term, label)
    if built is None:
        return record
    renderer, raw_bytes, mnem = built
    stripped = SOU.strip_chaff(mnem, "narrow")
    record["stripped_remaining"] = list(stripped)
    record["stripped_count"] = len(stripped)
    if len(stripped) == 1:
        landed, _operands = SOU.parse_insn(stripped[0])
        record["landed"] = {"mnem": landed}
        if landed == job["mnem"]:
            record["q0"] = {"verdict": "LANDED"}
        else:
            record["q0"] = {"verdict": "LANDED_ELSEWHERE",
                            "landed": {"mnem": landed}}
    else:
        record["q0"] = {"verdict": "NOT_COLLAPSED",
                        "opcode_count": len(stripped)}
    row_bytes = record.get("x_body_bytes")
    identical = row_bytes is not None and record["body_bytes"] == row_bytes
    record["q1"] = {
        "verdict": "BYTE_IDENTICAL" if identical else "BYTES_DIFFER",
        "row_body_bytes": row_bytes,
    }
    emu_label = "rust/" + label
    recorded = recorded_facts(emu_label, label, raw_bytes, mnem)
    canon = CF.render_one(form, gate, recorded)
    canon["unit"] = emu_label
    record["canon40_outcome"] = canon.get("outcome")
    record["q3"] = E.prove_against_x(reference, gate, maker, canon,
                                     x_record, renderer.params, x_term,
                                     walked, P100, G, record["x_in_rows"])
    return record


def build_shared():
    import term97_walk as TW
    import canonical_form as CF
    maker, gate, _attached, _readings = TW.build()
    form = CF.new_form()
    pool = read_json(E.POOL5)
    text_to_entries, unit_to_entry = E.pool_indexes(pool)
    del pool
    indexes = read_json(INDEXES)
    held = read_json(HELD)["held"]
    return {
        "maker": maker,
        "gate": gate,
        "form": form,
        "reference": maker.reference,
        "held": held,
        "bytes_index": indexes["bytes_index"],
        "text_to_entries": text_to_entries,
        "unit_to_entry": unit_to_entry,
    }


# ==================================================================
# section 6: THE COVERAGE TABLE   sorts x operators, measured
# ==================================================================

# the print form of each z3 declaration kind the renderer dispatches
# on, so the report can show the reader what the row looks like inside
# a layer-5 text.  A DISPLAY column only: the rows are keyed by the
# kind NAME below and by nothing else.
KIND_ROWS = [
    ("Z3_OP_UNINTERPRETED", "v0", "an arrival, read whole or through "
     "one Extract"),
    ("Z3_OP_BNUM", "1", "a bit-vector numeral"),
    ("Z3_OP_TRUE", "True", "the truth constant"),
    ("Z3_OP_FALSE", "False", "the falsehood constant"),
    ("Z3_OP_EXTRACT", "Extract(hi, lo, x)", "a bit field"),
    ("Z3_OP_CONCAT", "Concat(x, y)", "two fields joined"),
    ("Z3_OP_ZERO_EXT", "ZeroExt(k, x)", "widened, zero fill"),
    ("Z3_OP_SIGN_EXT", "SignExt(k, x)", "widened, sign fill"),
    ("Z3_OP_ITE", "If(c, x, y)", "a choice"),
    ("Z3_OP_AND", "And(p, q)", "truth conjunction"),
    ("Z3_OP_OR", "Or(p, q)", "truth disjunction"),
    ("Z3_OP_NOT", "Not(p)", "truth negation"),
    ("Z3_OP_XOR", "Xor(p, q)", "truth difference"),
    ("Z3_OP_IMPLIES", "Implies(p, q)", "truth implication"),
    ("Z3_OP_IFF", "p == q", "truth equality"),
    ("Z3_OP_EQ", "x == y", "bit-vector equality"),
    ("Z3_OP_DISTINCT", "x != y", "bit-vector difference"),
    ("Z3_OP_SLT", "x < y", "signed order"),
    ("Z3_OP_SLEQ", "x <= y", "signed order"),
    ("Z3_OP_SGT", "x > y", "signed order"),
    ("Z3_OP_SGEQ", "x >= y", "signed order"),
    ("Z3_OP_ULT", "ULT(x, y)", "unsigned order"),
    ("Z3_OP_ULEQ", "ULE(x, y)", "unsigned order"),
    ("Z3_OP_UGT", "UGT(x, y)", "unsigned order"),
    ("Z3_OP_UGEQ", "UGE(x, y)", "unsigned order"),
    ("Z3_OP_BADD", "x + y", "bit-vector sum"),
    ("Z3_OP_BSUB", "x - y", "bit-vector difference"),
    ("Z3_OP_BMUL", "x * y", "bit-vector product"),
    ("Z3_OP_BAND", "x & y", "bitwise meet"),
    ("Z3_OP_BOR", "x | y", "bitwise join"),
    ("Z3_OP_BXOR", "x ^ y", "bitwise difference"),
    ("Z3_OP_BNOT", "~x", "bitwise complement"),
    ("Z3_OP_BNEG", "-x", "two's-complement negation"),
    ("Z3_OP_BSHL", "x << y", "left shift"),
    ("Z3_OP_BLSHR", "LShR(x, y)", "logical right shift"),
    ("Z3_OP_BASHR", "x >> y", "arithmetic right shift"),
    ("Z3_OP_BUDIV_I", "bvudiv_i(x, y)", "unsigned quotient"),
    ("Z3_OP_BUREM_I", "bvurem_i(x, y)", "unsigned remainder"),
    ("Z3_OP_BSDIV_I", "bvsdiv_i(x, y)", "signed quotient"),
    ("Z3_OP_BSREM_I", "bvsrem_i(x, y)", "signed remainder"),
    ("Z3_OP_FPA_ADD", "fpAdd(RNE, x, y)", "float sum"),
    ("Z3_OP_FPA_SUB", "fpSub(RNE, x, y)", "float difference"),
    ("Z3_OP_FPA_MUL", "fpMul(RNE, x, y)", "float product"),
    ("Z3_OP_FPA_DIV", "fpDiv(RNE, x, y)", "float quotient"),
    ("Z3_OP_FPA_NEG", "fpNeg(x)", "float negation"),
    ("Z3_OP_FPA_ABS", "fpAbs(x)", "float magnitude"),
    ("Z3_OP_FPA_EQ", "fpEQ(x, y)", "float equality"),
    ("Z3_OP_FPA_LT", "fpLT(x, y)", "float order"),
    ("Z3_OP_FPA_LEQ", "fpLEQ(x, y)", "float order"),
    ("Z3_OP_FPA_GT", "fpGT(x, y)", "float order"),
    ("Z3_OP_FPA_GEQ", "fpGEQ(x, y)", "float order"),
    ("Z3_OP_FPA_IS_NAN", "fpIsNaN(x)", "float class test"),
    ("Z3_OP_FPA_IS_ZERO", "fpIsZero(x)", "float class test"),
    ("Z3_OP_FPA_IS_INF", "fpIsInf(x)", "float class test"),
    ("Z3_OP_FPA_IS_NEGATIVE", "fpIsNegative(x)", "float class test"),
    ("Z3_OP_FPA_IS_POSITIVE", "fpIsPositive(x)", "float class test"),
    ("Z3_OP_FPA_TO_FP", "fpToFP(RNE, x)", "to a float holder"),
    ("Z3_OP_FPA_TO_FP_UNSIGNED", "fpToFPUnsigned(RNE, x)",
     "unsigned to a float holder"),
    ("Z3_OP_FPA_TO_IEEE_BV", "fpToIEEEBV(x)", "a float's bits"),
    ("Z3_OP_FPA_TO_SBV", "fpToSBV(RTZ, x)", "float to signed holder"),
    ("Z3_OP_FPA_TO_UBV", "fpToUBV(RTZ, x)", "float to unsigned holder"),
    ("Z3_OP_FPA_RM_NEAREST_TIES_TO_EVEN", "RNE", "the rounding mode"),
]

# the c cell and the rust cell of each row: how the renderer for that
# target writes it, and the class of the cell -- "direct" (the
# target's own operator, one for one), "idiom" (a named construction
# the target needs where the other does not), or "none" (no holder or
# no operation, a hole).
CELLS = {
    "Z3_OP_UNINTERPRETED": (
        "direct", "a parameter of the holder of the width the term "
        "reads, cast with a C cast",
        "direct", "a parameter of the holder of the width the term "
        "reads, cast with `as`"),
    "Z3_OP_BNUM": (
        "direct", "`UINT32_C(0x..)` / `UINT64_C(0x..)`; a 128-bit "
        "numeral is built from two 64-bit halves shifted and joined",
        "direct", "`0x..u32` / `0x..u64` / `0x..u128` -- rust writes a "
        "128-bit numeral directly, with no halves"),
    "Z3_OP_TRUE": ("direct", "`1`", "direct", "`true`"),
    "Z3_OP_FALSE": ("direct", "`0`", "direct", "`false`"),
    "Z3_OP_EXTRACT": (
        "direct", "shift right, then mask with `&`",
        "direct", "shift right, then mask with `&`; every step carries "
        "an explicit `as` because rust never widens on its own"),
    "Z3_OP_CONCAT": (
        "direct", "each part cast to the promoted type, shifted into "
        "place, joined with `|`",
        "direct", "the same, with `as` at each part"),
    "Z3_OP_ZERO_EXT": (
        "direct", "a cast to the wider unsigned type",
        "direct", "`as` to the wider unsigned type"),
    "Z3_OP_SIGN_EXT": (
        "idiom", "shift left into the sign position, cast to the "
        "signed type, shift right -- c has no sign-extend from an "
        "arbitrary field width",
        "idiom", "the same three steps; `((x as u32) << k) as i32 >> k`"),
    "Z3_OP_ITE": ("direct", "`c ? x : y`", "direct", "`if c { x } else { y }`"),
    "Z3_OP_AND": ("direct", "`&&`", "direct", "`&&`"),
    "Z3_OP_OR": ("direct", "`||`", "direct", "`||`"),
    "Z3_OP_NOT": ("direct", "`!`", "direct", "`!`"),
    "Z3_OP_XOR": ("direct", "`!=` on truth values", "direct", "`!=` on `bool`"),
    "Z3_OP_IMPLIES": ("direct", "`!p || q`", "direct", "`!p || q`"),
    "Z3_OP_IFF": ("direct", "`==` on truth values", "direct", "`==` on `bool`"),
    "Z3_OP_EQ": ("direct", "`==`", "direct", "`==`"),
    "Z3_OP_DISTINCT": ("direct", "`!=`", "direct", "`!=`"),
    "Z3_OP_SLT": ("direct", "`<` on the signed holder",
                  "direct", "`<` on the signed holder"),
    "Z3_OP_SLEQ": ("direct", "`<=` on the signed holder",
                   "direct", "`<=` on the signed holder"),
    "Z3_OP_SGT": ("direct", "`>` on the signed holder",
                  "direct", "`>` on the signed holder"),
    "Z3_OP_SGEQ": ("direct", "`>=` on the signed holder",
                   "direct", "`>=` on the signed holder"),
    "Z3_OP_ULT": ("direct", "`<` on the unsigned holder",
                  "direct", "`<` on the unsigned holder"),
    "Z3_OP_ULEQ": ("direct", "`<=` on the unsigned holder",
                   "direct", "`<=` on the unsigned holder"),
    "Z3_OP_UGT": ("direct", "`>` on the unsigned holder",
                  "direct", "`>` on the unsigned holder"),
    "Z3_OP_UGEQ": ("direct", "`>=` on the unsigned holder",
                   "direct", "`>=` on the unsigned holder"),
    "Z3_OP_BADD": (
        "direct", "`+` on the unsigned holder, which wraps by the "
        "standard",
        "idiom", "`wrapping_add`. At the corpus's ship flags "
        "(`-C debug-assertions=off`) plain `+` emits the same body, "
        "but at `debug-assertions=on` it branches to "
        "`panic_const_add_overflow`, so the plain operator is "
        "flag-dependent and the wrapping method is not"),
    "Z3_OP_BSUB": (
        "direct", "`-` on the unsigned holder",
        "idiom", "`wrapping_sub`, for the same reason as the sum"),
    "Z3_OP_BMUL": (
        "direct", "`*` on the unsigned holder",
        "idiom", "`wrapping_mul`; plain `*` branches to "
        "`panic_const_mul_overflow` at `debug-assertions=on`"),
    "Z3_OP_BAND": ("direct", "`&`", "direct", "`&`"),
    "Z3_OP_BOR": ("direct", "`|`", "direct", "`|`"),
    "Z3_OP_BXOR": ("direct", "`^`", "direct", "`^`"),
    "Z3_OP_BNOT": ("direct", "`~`", "direct", "`!` on an integer holder"),
    "Z3_OP_BNEG": (
        "direct", "unary `-` on the unsigned holder",
        "idiom", "`wrapping_neg`; plain `-` branches to "
        "`panic_const_neg_overflow` at `debug-assertions=on`"),
    "Z3_OP_BSHL": (
        "idiom", "`<<` inside the term's out-of-range guard "
        "`(count < width) ? shifted : 0` -- c leaves an out-of-range "
        "count undefined",
        "idiom", "`wrapping_shl` inside the same guard. Plain `<<` "
        "branches to `panic_const_shl_overflow` at "
        "`debug-assertions=on`; `wrapping_shl` masks the count to the "
        "width, which is the machine's rule and not the term's, so "
        "the guard is still needed"),
    "Z3_OP_BLSHR": (
        "idiom", "`>>` on the unsigned holder inside the same guard",
        "idiom", "`wrapping_shr` on the unsigned holder inside the "
        "same guard"),
    "Z3_OP_BASHR": (
        "idiom", "`>>` on the signed holder inside the same guard, "
        "with the sign-fill arm",
        "idiom", "`wrapping_shr` on the signed holder inside the same "
        "guard, with the sign-fill arm"),
    "Z3_OP_BUDIV_I": (
        "direct", "`/` on the unsigned holder; c leaves a zero "
        "divisor undefined and clang emits a bare `div`",
        "idiom", "`unsafe { if d == 0 { unreachable_unchecked() } } "
        "n / d`. Rust checks a zero divisor in BOTH builds -- the "
        "check is not a debug assertion -- and emits a branch to "
        "`panic_const_div_by_zero`; the hint removes it and the body "
        "is the bare `div`"),
    "Z3_OP_BUREM_I": (
        "direct", "`%` on the unsigned holder",
        "idiom", "the same hint, then `%`"),
    "Z3_OP_BSDIV_I": (
        "direct", "`/` on the signed holder; clang emits a bare `idiv`",
        "idiom", "the hint must ALSO exclude the signed extreme "
        "(`n == MIN && d == -1`), because rust checks that case too "
        "and branches to `panic_const_div_overflow`. "
        "`core::hint::assert_unchecked` on its own does NOT remove "
        "that second check (measured, lane o11_l3); the `if ... { "
        "unreachable_unchecked() }` spelling does (lane o11_l4)"),
    "Z3_OP_BSREM_I": (
        "direct", "`%` on the signed holder",
        "idiom", "the same two-condition hint, then `%`"),
    "Z3_OP_FPA_ADD": ("direct", "`+` on float / double",
                      "direct", "`+` on f32 / f64; floats never check"),
    "Z3_OP_FPA_SUB": ("direct", "`-`", "direct", "`-`"),
    "Z3_OP_FPA_MUL": ("direct", "`*`", "direct", "`*`"),
    "Z3_OP_FPA_DIV": ("direct", "`/`", "direct", "`/`"),
    "Z3_OP_FPA_NEG": ("direct", "unary `-`", "direct", "unary `-`"),
    "Z3_OP_FPA_ABS": (
        "direct", "`__builtin_fabs` / `__builtin_fabsf`",
        "idiom", "`f64::from_bits(x.to_bits() & 0x7fff_ffff_ffff_ffff)` "
        "-- the sign bit cleared, which emits one `andps` (measured, "
        "lane o11_l2); `f64::abs` would reach the standard library"),
    "Z3_OP_FPA_EQ": ("direct", "`==`", "direct", "`==`"),
    "Z3_OP_FPA_LT": ("direct", "`<`", "direct", "`<`"),
    "Z3_OP_FPA_LEQ": ("direct", "`<=`", "direct", "`<=`"),
    "Z3_OP_FPA_GT": ("direct", "`>`", "direct", "`>`"),
    "Z3_OP_FPA_GEQ": ("direct", "`>=`", "direct", "`>=`"),
    "Z3_OP_FPA_IS_NAN": ("idiom", "`x != x`", "idiom", "`x != x`"),
    "Z3_OP_FPA_IS_ZERO": ("idiom", "`x == 0`", "idiom", "`x == 0.0`"),
    "Z3_OP_FPA_IS_INF": (
        "direct", "`__builtin_isinf`",
        "idiom", "the exponent field all ones and the significand "
        "zero, read off `to_bits`; `f64::is_infinite` would reach the "
        "standard library"),
    "Z3_OP_FPA_IS_NEGATIVE": (
        "direct", "`__builtin_signbit`",
        "idiom", "`(x.to_bits() >> 63) != 0`"),
    "Z3_OP_FPA_IS_POSITIVE": (
        "direct", "`__builtin_signbit(x) == 0`",
        "idiom", "`(x.to_bits() >> 63) == 0`"),
    "Z3_OP_FPA_TO_FP": (
        "idiom", "a `memcpy` helper for the bit reinterpretation; a "
        "plain cast for the value conversion",
        "direct", "`f64::from_bits` for the bit reinterpretation, "
        "`as` for the value conversion -- rust needs no helper"),
    "Z3_OP_FPA_TO_FP_UNSIGNED": ("direct", "a cast from the unsigned "
                                 "holder", "direct", "`as` from the "
                                 "unsigned holder"),
    "Z3_OP_FPA_TO_IEEE_BV": (
        "idiom", "a `memcpy` helper",
        "direct", "`x.to_bits()`"),
    "Z3_OP_FPA_TO_SBV": (
        "direct", "a cast to the signed holder, which truncates",
        "idiom", "`unsafe { x.to_int_unchecked::<i64>() }`. Plain `as` "
        "SATURATES in rust and emits seven instructions with a "
        "not-a-number case (measured, lane o11_l1); "
        "`to_int_unchecked` emits the bare `cvttsd2si`"),
    "Z3_OP_FPA_TO_UBV": (
        "direct", "a cast to the unsigned holder",
        "idiom", "the same `to_int_unchecked`"),
    "Z3_OP_FPA_RM_NEAREST_TIES_TO_EVEN": (
        "direct", "the default rounding mode of both languages; any "
        "other mode is refused",
        "direct", "the same"),
}

# the 32 holders task t101b measured, as the two targets spell them.
# The one hole is the 16-bit float: rustc 1.96.1 refuses `f16`.
SORT_ROWS = [
    ("signed 8", "int8_t", "i8"), ("signed 16", "int16_t", "i16"),
    ("signed 32", "int32_t", "i32"), ("signed 64", "int64_t", "i64"),
    ("signed 128", "__int128", "i128"),
    ("unsigned 8", "uint8_t", "u8"), ("unsigned 16", "uint16_t", "u16"),
    ("unsigned 32", "uint32_t", "u32"),
    ("unsigned 64", "uint64_t", "u64"),
    ("unsigned 128", "unsigned __int128", "u128"),
    ("float 16", "_Float16", "NONE -- f16 is unstable on rustc 1.96.1"),
    ("float 32", "float", "f32"), ("float 64", "double", "f64"),
    ("truth 1", "the promoted int, 0 or 1", "bool"),
]


def optable_command():
    """the coverage table: every operator of the term language, with
    the c cell and the rust cell, and the count of pool entries whose
    layer-5 text contains that operator's print form.  The count makes
    the table finite in the sense log 221 section 3 means: the rows
    are the operation symbols the corpus actually attests."""
    say("-- COVERAGE TABLE: the term language's operators x the two "
        "targets")
    pool = read_json(E.POOL5)
    counts = {}
    for kind, print_form, _reading in KIND_ROWS:
        counts[kind] = 0
    entries_with_text = 0
    for entry in pool["entries"]:
        texts = entry.get("layer5_normalized_texts") or []
        if not texts:
            continue
        entries_with_text = entries_with_text + 1
        joined = " ".join(texts)
        for kind, print_form, _reading in KIND_ROWS:
            if occurrence(joined, kind, print_form):
                counts[kind] = counts[kind] + 1
    del pool
    rows = []
    for kind, print_form, reading in KIND_ROWS:
        c_class, c_rule, rust_class, rust_rule = CELLS[kind]
        rows.append({
            "kind": kind,
            "print_form": print_form,
            "reading": reading,
            "entries_attesting": counts[kind],
            "c_class": c_class,
            "c_rule": c_rule,
            "rust_class": rust_class,
            "rust_rule": rust_rule,
        })
    document = {
        "task": "o11",
        "what_this_is": (
            "the coverage table log 221 section 3 names: the term "
            "language's operators (rows) against the two target "
            "languages (columns), each cell saying whether the target "
            "has a direct operator, needs a named idiom, or has no "
            "construction at all.  The sorts table beside it is the "
            "32 holders task t101b measured, as the two targets spell "
            "them."),
        "kind_source": (
            "the dispatch of emulate.Renderer.emit -- the z3 "
            "declaration kinds task o7's renderer names, which are the "
            "kinds reference.Reference.opcode_table's builders "
            "produce"),
        "pool_source": E.POOL5,
        "pool_entries_with_a_layer5_text": entries_with_text,
        "coverage": rows,
        "sorts": [{"holder": h, "c": c, "rust": r}
                  for h, c, r in SORT_ROWS],
        "rust_facts": [os.path.join(HOST_FOLDER, "rust_facts.json"),
                       os.path.join(HOST_FOLDER, "rust_facts2.json"),
                       os.path.join(HOST_FOLDER, "rust_facts3.json"),
                       os.path.join(HOST_FOLDER, "rust_facts4.json")],
        "rustc": rustc_version(),
        "ship_flags": " ".join([RUSTC] + SHIP_FLAGS),
        "ship_flags_source": SHIP_FLAGS_SOURCE,
    }
    write_json(OPTABLE, document)
    say("   %d operator rows; %d entries carry a layer-5 text"
        % (len(rows), entries_with_text))
    holes = [row for row in rows if row["rust_class"] == "none"]
    idioms = [row for row in rows if row["rust_class"] == "idiom"]
    say("   rust: %d direct, %d idiom, %d none"
        % (len(rows) - len(idioms) - len(holes), len(idioms), len(holes)))
    say("   wrote %s" % OPTABLE)
    return 0


def occurrence(joined, kind, print_form):
    """does this operator's print form appear in the joined texts of one
    entry?  A structural test on the print form, never a key: the
    result is a COUNT on the coverage row, and no unit is grouped or
    paired by it."""
    if kind == "Z3_OP_UNINTERPRETED":
        return "v0" in joined
    if kind == "Z3_OP_BNUM":
        return True
    if print_form.endswith(")") and "(" in print_form:
        return print_form.split("(")[0] + "(" in joined
    if print_form in ("True", "False", "RNE"):
        return print_form in joined
    marker = print_form.replace("x", "").replace("y", "")
    marker = marker.replace("p", "").replace("q", "").strip()
    if not marker:
        return False
    return (" %s " % marker) in joined


def rustc_version():
    try:
        done = subprocess.run([RUSTC, "--version"], capture_output=True,
                              text=True, timeout=120)
        return done.stdout.strip() or done.stderr.strip()
    except Exception as problem:                           # noqa: BLE001
        return "rustc --version raised %s" % problem


# ==================================================================
# section 7: THE COMMANDS
# ==================================================================

def census():
    say("-- CENSUS: the population, its filters, the indexes")
    pool = read_json(E.POOL5)
    cross1 = read_json(E.CROSS1)
    population = RustPopulation(pool, cross1)
    entries = population.select()
    eligible_controls = population.select_control(40)
    needed = set()
    for entry_id, plan in entries.items():
        needed.add(plan["x_unit"])
    for entry_id, plan in population.control.items():
        needed.add(plan["x_unit"])
        for name in plan["target_units_in_entry"]:
            needed.add(name)
    per_opcode_rows = per_opcode_population()
    for row in per_opcode_rows:
        needed.add(row["x_unit"])
    say("   units whose canon40 records are held: %d" % len(needed))
    bytes_index, held, shard_of, target_units = build_indexes(needed)
    missing = sorted(name for name in needed if name not in held)
    say("   rust units indexed by body bytes: %d (%d distinct byte "
        "strings)" % (target_units, len(bytes_index)))
    say("   held records: %d; missing: %d %s" % (len(held), len(missing),
                                                 missing[:5]))
    sample = population.stratified_sample(40)
    # the run set: every entry that round-trips, capped at RUN_CEILING
    # and drawn uniformly with the stated seed when it is larger.
    passing = sorted(entry_id for entry_id in entries
                     if entries[entry_id]["round_trips"])
    if len(passing) > RUN_CEILING:
        rng = random.Random(SEED)
        run_set = sorted(rng.sample(passing, RUN_CEILING))
        drawn_note = ("%d of %d drawn uniformly, seed %d"
                      % (RUN_CEILING, len(passing), SEED))
    else:
        run_set = passing
        drawn_note = "all %d, under the ceiling of %d" % (len(passing),
                                                          RUN_CEILING)
    say("   the run set: %s" % drawn_note)
    write_json(POPULATION, {
        "task": "o11 -- does rustc collapse an emulation to the unit it "
                "emulates",
        "pool_source": E.POOL5,
        "cross1_source": E.CROSS1,
        "pool_entry_count": len(pool["entries"]),
        "target": TARGET,
        "x_languages": X_LANGUAGES,
        "filters": population.filters,
        "entries": entries,
        "control": population.control,
        "control_eligible_entries": eligible_controls,
        "sample_40": sample,
        "run_set": run_set,
        "run_set_note": drawn_note,
        "per_opcode": per_opcode_rows,
        "seed": SEED,
        "ship_flags": " ".join([RUSTC] + SHIP_FLAGS),
        "ship_flags_source": SHIP_FLAGS_SOURCE,
        "rustc": rustc_version(),
        "held_missing": missing,
    })
    write_json(HELD, {"held": held, "shard_of": shard_of})
    write_json(INDEXES, {"bytes_index": bytes_index,
                         "target_units": target_units})
    say("   wrote %s, %s, %s" % (POPULATION, HELD, INDEXES))
    say("   collector peak %d kB" % peak_kb())


def per_opcode_population():
    """task o8's single-opcode rows for the three source languages, each
    with its example unit's proved layer-5 text; a row whose unit has
    no proved term is carried with `text` None and skipped."""
    import per_opcode as P8
    import term66_run as TR
    rows = []
    wanted = {}
    for row in P8.load_rows():
        if row["lang"] not in PER_OPCODE_LANGS:
            continue
        rows.append(row)
        wanted[row["example_unit_id"]] = None
    for path in E.canon40_shards():
        term_path = P8.term66_shard_path(path)
        if not os.path.exists(term_path):
            continue
        document = read_json(term_path)
        for name, record in document["units"].items():
            if name not in wanted:
                continue
            if record.get("outcome") != "PROVED_ON_SHIP":
                continue
            wanted[name] = record.get("layer5_normalized_text")
        del document
        check_collector_memory()
    out = []
    for index, row in enumerate(rows):
        text = wanted.get(row["example_unit_id"])
        out.append({
            "entry_id": "%s_%d" % (row["lang"], row["row_index"]),
            "job_kind": "per_opcode",
            "x_lang": row["lang"],
            "x_unit": row["example_unit_id"],
            "text": text,
            "entry_texts": [text] if text else [],
            "type_key": None,
            "mnem": row["mnemonic"],
            "row_body_text": row["row_body_text"],
            "member_count": row["member_count"],
            "has_proved_term": text is not None,
        })
    say("   per-opcode rows for %s: %d, of which %d carry a proved term"
        % (", ".join(PER_OPCODE_LANGS), len(out),
           sum(1 for row in out if row["has_proved_term"])))
    return out


def jobs_for(entry_ids, plans, control=False):
    jobs = []
    for entry_id in entry_ids:
        job = dict(plans[entry_id])
        job["control"] = control
        jobs.append(job)
    return jobs


def sample_command(count):
    say("-- SAMPLE: %d entries across the three x, seed %d"
        % (count, SEED))
    install_worker()
    population = read_json(POPULATION)
    entry_ids = population["sample_40"][:count]
    shared = build_shared()
    say("   shared objects built; collector peak %d kB" % peak_kb())
    results = E.collect(shared, jobs_for(entry_ids,
                                         population["entries"]), "sample")
    write_json(SAMPLE, {"count": count, "entry_ids": entry_ids,
                        "results": results,
                        "collector_peak_kb": peak_kb()})
    say("   wrote %s" % SAMPLE)


def run_command():
    say("-- RUN: the run set")
    install_worker()
    population = read_json(POPULATION)
    entry_ids = population["run_set"]
    say("   %s" % population["run_set_note"])
    shared = build_shared()
    results = E.collect(shared, jobs_for(entry_ids,
                                         population["entries"]), "run")
    write_json(RUN, {"entry_ids": entry_ids, "results": results,
                     "collector_peak_kb": peak_kb()})
    say("   wrote %s" % RUN)


def control_command(count):
    say("-- CONTROL: %d entries WITH a rust member, seed %d"
        % (count, SEED))
    install_worker()
    population = read_json(POPULATION)
    entry_ids = sorted(population["control"])[:count]
    shared = build_shared()
    results = E.collect(shared, jobs_for(entry_ids, population["control"],
                                         control=True), "control")
    write_json(CONTROL, {"count": count, "entry_ids": entry_ids,
                         "results": results,
                         "collector_peak_kb": peak_kb()})
    say("   wrote %s" % CONTROL)


def peropcode_command():
    say("-- PER OPCODE: task o8's question with rust as the target")
    install_worker()
    population = read_json(POPULATION)
    jobs = [row for row in population["per_opcode"]
            if row["has_proved_term"]]
    skipped = [row for row in population["per_opcode"]
               if not row["has_proved_term"]]
    say("   %d rows with a proved term; %d skipped"
        % (len(jobs), len(skipped)))
    shared = build_shared()
    results = E.collect(shared, jobs, "peropcode")
    write_json(PEROPCODE, {"results": results, "skipped": skipped,
                           "collector_peak_kb": peak_kb()})
    say("   wrote %s" % PEROPCODE)


def main(argv):
    if len(argv) < 2:
        say(__doc__)
        return 2
    command = argv[1]
    if command == "optable":
        return optable_command()
    if command == "census":
        census()
        return 0
    if command == "sample":
        sample_command(int(argv[2]))
        return 0
    if command == "run":
        run_command()
        return 0
    if command == "control":
        control_command(int(argv[2]))
        return 0
    if command == "peropcode":
        peropcode_command()
        return 0
    if command == "report":
        import rust_report
        return rust_report.report()
    say("unknown command %s" % command)
    return 2


if __name__ == "__main__":
    if not os.path.isdir(SRC_DIR):
        os.makedirs(SRC_DIR)
    sys.exit(main(sys.argv))
