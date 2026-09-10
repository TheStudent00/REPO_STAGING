#!/usr/bin/env python3
"""interp_render.py -- task ex1: the ONE renderer for an INTERPRETED
target, and the seven dialects it prints through.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly, with
`node_0_3_1_operator_equivalence/node_0_3_1_12_remaining_languages`.

WHAT AN INTERPRETED EMULATION IS, and how it differs from a compiled
one.  For c, cpp, rust, go and swift the emulation is a translation
unit: it is compiled at the corpus's ship flags, CARVED, put on the
canonical form and handed to z3, and the verdict is a proof over every
input.  None of that exists here.  An interpreted target's operator has
no lowered body of its own that our probe can name -- the machine code
that runs is the interpreter's handler, which is a different unit
(`node_0_3_1_12_remaining_languages` section 1, "the interpreter
shape") -- so:
  * THE EMULATION IS SOURCE.  The cell's mapping, written in the
    target's own operators over the target's own value model.  The
    value model is not assumed: `dialects.py` holds one prelude per
    language, every rule of it measured by a probe, and this file
    emits CALLS into that prelude.
  * THE CHECK IS A FUZZ CENSUS, not a proof.  `interp_check.py` holds
    it, and its own header states the sample rule LITERAL before it
    runs.

THE OBJECTS, one sentence each, in relation.
  * A TERM is one place of one arch-opcode written as a z3 expression
    over `seed_<register family>` symbols -- the same object the
    compiled targets render.
  * A DIALECT is one interpreted language's value model, written once
    as a prelude of named functions (`dialects.py`).
  * AN EMULATION is one source file: that prelude, one function whose
    body is the term written as calls into it, and a main that reads
    arrival tuples from standard input and writes one answer per line.
  * A POINT is one arrival tuple; the SAMPLE is the stated set of them.

THE VALUE CONVENTION, which is stated because it is a convention and
not a measurement:
  * every value is carried as a non-negative integer in [0, 2^w) (the
    unbounded dialects) or in the low w bits of the language's 64-bit
    integer (the fixed ones);
  * A FLOAT ARRIVAL REACHES THE EMULATION AS ITS BIT PATTERN, and a
    float answer leaves as its bit pattern.  This is c's own shape and
    not an invention: `emulate.Renderer.emit_symbol` takes a float
    parameter and immediately applies `f32_to_bits`, and
    `emulate.Renderer.answer` applies `bits_to_f32` on the way out.
    What differs is only that the conversion sits at the edge of the
    process here rather than at the edge of the function.
  * `fp.to_ieee_bv` and the one-argument `fpToFP` are therefore the
    IDENTITY in every dialect, so no rendering ever round-trips a
    value through a float wider than the one the term names.

WHAT IS REUSED RATHER THAN COPIED, said out loud.  `emulate.Renderer`
is DERIVED FROM: `plan_parameters` (which decides each arrival's
width), `collect_uses` and `check_symbols` are inherited unchanged and
are the same functions the compiled targets' widths come from.  The
refusal causes are `emulate`'s own (`CAUSE_OP`, `CAUSE_WIDTH`,
`CAUSE_STATE`, `CAUSE_LANE`, `CAUSE_X87`), so a cause on an
interpreted run reads the same as a cause on a compiled one.  Nothing
under `Research/op_pipeline/` is edited.

WHAT IS REFUSED RATHER THAN GUESSED.  The handful's ten cells ask for
exactly this vocabulary, measured by lane
`ex1_l3_the_ten_cells_and_what_they_ask_for.sh` over the cells
themselves: `bv`, `bvadd`, `bvand`, `bvashr`, `bvlshr`, `bvmul`,
`bvsdiv`, `bvsrem`, `bvsub`, `concat`, `distinct`, `extract`,
`fp.add`, `fp.to_ieee_bv`, `if`, `roundNearestTiesToEven`, `to_fp` and
the seed symbols.  This file spells those and the ones that come with
them for free; every other z3 declaration is `CAUSE_OP`, by name, and
the report counts them.  That is the handful-first rule applied to a
printer: what the handful asks for is written and measured, and what
it does not ask for is a named refusal rather than untested text.

MEMORY: this file allocates nothing of its own and runs inside the
driver's one collecting process, bound 6 GB, named abort
ABORT_MEMORY_EX1.

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

Nothing here keys, groups, pairs or selects anything: a z3 declaration
kind goes in and source text comes out.

Coding discipline: no compound one-liner statements.

usage:
  interp_render.py runners   what each language's runner answers, LITERAL
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EMULATION = os.path.normpath(os.path.join(HERE, ".."))
CROSS = os.path.normpath(os.path.join(HERE, "..", ".."))
OP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                   "op_pipeline"))
sys.path.insert(0, OP)
sys.path.insert(0, CROSS)
sys.path.insert(0, EMULATION)
sys.path.insert(0, HERE)

import z3                                                        # noqa: E402
import emulate as E                                              # noqa: E402
import dialects as D                                             # noqa: E402

# THE SEVEN, in the brief's own order: its four, then the three whose
# runners this task found and named.
LANGUAGES = ["cpython", "php", "ruby", "java", "javascript", "dart",
             "csharp"]

CAUSE_WIDE = ("a width %s has no holder for: its integer is 64 bits "
              "and this place is %d")


class Dialect(object):
    """one interpreted language's spellings.  Every field is either the
    text of that language's own syntax or a measured fact about its
    value model; the arithmetic itself is in `dialects.py`."""

    name = None
    suffix = None
    unbounded = False
    prefix = ""
    """what every helper name of this dialect's prelude carries in
    front of it.  Only php has one: `fdiv` is a php BUILT-IN function
    (php 8), and a prelude that declares it answers, LITERAL, `PHP
    Fatal error:  Cannot redeclare function fdiv()` -- measured on the
    first smoke run of lane ex1_l6, and the reason every php helper is
    `ex_`-prefixed rather than only that one."""
    prelude = None
    main = None
    logic_and = "&&"
    logic_or = "||"
    logic_not = "!"
    true_text = "true"
    false_text = "false"
    version_command = None

    def param(self, name):
        return name

    def lit(self, value, width):
        """a literal of the value, non-negative and less than 2^width."""
        if self.unbounded:
            return "%d" % value
        if width > 64:
            raise E.Refused(E.CAUSE_WIDTH,
                            CAUSE_WIDE % (self.name, width))
        if value >= (1 << 63):
            return "%d" % (value - (1 << 64))
        return "%d" % value

    def call(self, name, args):
        parts = []
        for one in args:
            parts.append("%s" % one)
        return "%s(%s)" % (name, ", ".join(parts))

    def width_text(self, width):
        return "%d" % width

    def ite(self, cond, left, right):
        return "((%s) ? (%s) : (%s))" % (cond, left, right)

    def function(self, symbol, params, body):
        raise NotImplementedError

    def command(self, folder, path, symbol):
        raise NotImplementedError

    def prepare(self, folder, path, symbol, environment):
        """what to RUN, once the source is on disk.  Every dialect but
        one just runs its own runner over the file; c# has to build a
        project first, and its build writes to standard output, so the
        build is done here and the BINARY is what the measurement
        runs -- otherwise the build's own lines would be read as
        answers, which is exactly what the first smoke run of lane
        ex1_l6 recorded (`the runner answered 9 lines for 900
        points`)."""
        return self.command(folder, path, symbol), None

    def check_width(self, width):
        if self.unbounded:
            return
        if width > 64:
            raise E.Refused(E.CAUSE_WIDTH,
                            CAUSE_WIDE % (self.name, width))


class Cpython(Dialect):
    name = "cpython"
    suffix = ".py"
    unbounded = True
    prelude = D.CPYTHON_PRELUDE
    main = D.CPYTHON_MAIN
    logic_and = "and"
    logic_or = "or"
    logic_not = "not "
    true_text = "True"
    false_text = "False"
    version_command = ["python3", "--version"]

    def ite(self, cond, left, right):
        return "((%s) if (%s) else (%s))" % (left, cond, right)

    def function(self, symbol, params, body):
        head = "def %s(%s):" % (symbol, ", ".join(params))
        return "%s\n    return %s\n" % (head, body)

    def command(self, folder, path, symbol):
        return ["python3", path]


class Ruby(Dialect):
    name = "ruby"
    suffix = ".rb"
    unbounded = True
    prelude = D.RUBY_PRELUDE
    main = D.RUBY_MAIN
    version_command = ["ruby", "--version"]

    def function(self, symbol, params, body):
        head = "def %s(%s)" % (symbol, ", ".join(params))
        return "%s\n  %s\nend\n" % (head, body)

    def command(self, folder, path, symbol):
        return ["ruby", path]


class Javascript(Dialect):
    name = "javascript"
    suffix = ".js"
    unbounded = True
    prelude = D.JAVASCRIPT_PRELUDE
    main = D.JAVASCRIPT_MAIN
    version_command = ["node", "--version"]

    def lit(self, value, width):
        return "%dn" % value

    def function(self, symbol, params, body):
        head = "function %s(%s)" % (symbol, ", ".join(params))
        return "%s {\n    return %s;\n}\n" % (head, body)

    def command(self, folder, path, symbol):
        return ["node", path]


class Php(Dialect):
    name = "php"
    suffix = ".php"
    unbounded = False
    prelude = D.PHP_PRELUDE
    main = D.PHP_MAIN
    prefix = "ex_"
    version_command = ["php", "--version"]

    def param(self, name):
        return "$%s" % name

    def function(self, symbol, params, body):
        head = "function %s(%s)" % (symbol, ", ".join(params))
        return "%s {\n    return %s;\n}\n" % (head, body)

    def command(self, folder, path, symbol):
        return ["php", path]


class Java(Dialect):
    name = "java"
    suffix = ".java"
    unbounded = False
    prelude = D.JAVA_PRELUDE
    main = D.JAVA_MAIN
    version_command = ["java", "--version"]

    def lit(self, value, width):
        return "%sL" % Dialect.lit(self, value, width)

    def function(self, symbol, params, body):
        typed = []
        for one in params:
            typed.append("long %s" % one)
        head = "    static long %s(%s)" % (symbol, ", ".join(typed))
        return "%s {\n        return %s;\n    }\n" % (head, body)

    def command(self, folder, path, symbol):
        return ["java", path]


class Dart(Dialect):
    name = "dart"
    suffix = ".dart"
    unbounded = False
    prelude = D.DART_PRELUDE
    main = D.DART_MAIN
    version_command = ["/persist/dart-sdk/bin/dart", "--version"]

    def function(self, symbol, params, body):
        typed = []
        for one in params:
            typed.append("int %s" % one)
        head = "int %s(%s)" % (symbol, ", ".join(typed))
        return "%s {\n  return %s;\n}\n" % (head, body)

    def command(self, folder, path, symbol):
        return ["/persist/dart-sdk/bin/dart", "run", path]


class Csharp(Dialect):
    name = "csharp"
    suffix = ".cs"
    unbounded = False
    prelude = D.CSHARP_PRELUDE
    main = D.CSHARP_MAIN
    version_command = ["/persist/dotnet/dotnet", "--version"]

    def lit(self, value, width):
        return "%sL" % Dialect.lit(self, value, width)

    def function(self, symbol, params, body):
        typed = []
        for one in params:
            typed.append("long %s" % one)
        head = "    public static long %s(%s)" % (symbol,
                                                  ", ".join(typed))
        return "%s {\n        return %s;\n    }\n" % (head, body)

    def command(self, folder, path, symbol):
        # THE DLL THROUGH THE HOST, not the framework-dependent
        # launcher: the launcher answers `You must install .NET to run
        # this application` when the runtime is in the persist volume
        # rather than on the machine's own path, which is what lane
        # ex1_l8's first pass recorded (exit 131).
        return ["/persist/dotnet/dotnet", "exec",
                os.path.join(folder, "bin", "Release", "net10.0",
                             "emu.dll")]

    def prepare(self, folder, path, symbol, environment):
        """THE ONE RUNNER THAT IS A BUILD."""
        done = subprocess.run(
            ["/persist/dotnet/dotnet", "build", "-c", "Release",
             "--nologo", "-v", "quiet"],
            cwd=folder, capture_output=True, text=True, timeout=1800,
            env=environment)
        binary = os.path.join(folder, "bin", "Release", "net10.0",
                              "emu.dll")
        if not os.path.exists(binary):
            first = "(no diagnostic)"
            text = (done.stdout or done.stderr).strip()
            for line in text.splitlines():
                if "error" in line:
                    first = line.strip()[:300]
                    break
            if first == "(no diagnostic)" and text:
                first = text.splitlines()[0][:300]
            return None, ("the c# build exited %d and left no binary: %s"
                          % (done.returncode, first))
        return self.command(folder, path, symbol), None


DIALECTS = {
    "cpython": Cpython(),
    "ruby": Ruby(),
    "javascript": Javascript(),
    "php": Php(),
    "java": Java(),
    "dart": Dart(),
    "csharp": Csharp(),
}


def runner_answer(lang):
    """what running this language's runner actually does on the machine
    this runs on: the literal answer, whatever it is.  Re-read at run
    time rather than pasted from a previous lane, so an absent runner
    is a FLAG carried on the run record and never a workaround."""
    dialect = DIALECTS[lang]
    try:
        done = subprocess.run(dialect.version_command,
                              capture_output=True, text=True,
                              timeout=180)
    except OSError as problem:
        return "%s: %s" % (dialect.version_command[0], problem.strerror)
    text = (done.stdout or done.stderr).strip()
    first = "(no output)"
    if text:
        first = text.splitlines()[0]
    if done.returncode != 0:
        return "%s exited %d: %s" % (dialect.version_command[0],
                                     done.returncode, first)
    return first


# ==================================================================
# section 2: THE RENDERER   z3 term -> one interpreted source file
# ==================================================================

class InterpRenderer(E.Renderer):
    """the ONE interpreted renderer: a z3 term over `seed_<family>`
    symbols -> one source file in the target language.

    DERIVES from task o7's `emulate.Renderer`; `plan_parameters`,
    `collect_uses` and `check_symbols` are inherited unchanged, so an
    arrival's width here is the width the compiled targets plan for the
    same term.  Every `emit` method is this file's own, because the
    compiled renderer's are c expressions with c casts in them.

    attributes:
        dialect         the target's own spellings
        families        the term's arrival families, IN order
        result_family   the answer home
        result_width    its width in bits
        params          per family: name, holder text, kind, bits
    methods:
        render          -> (source text, function symbol)
        emit            one node -> (text, kind, width)
    """

    def __init__(self, lang, families, result_family, result_width,
                 label):
        E.Renderer.__init__(self, families, result_family, result_width,
                            label)
        self.lang = lang
        self.dialect = DIALECTS[lang]

    # -- the parameter plan -------------------------------------------

    def plan_parameters(self, term):
        """`emulate.Renderer.plan_parameters`, then the holder names
        replaced by this language's own.  The WIDTHS are not touched:
        they are what the compiled targets plan for the same term."""
        E.Renderer.plan_parameters(self, term)
        for param in self.params:
            self.dialect.check_width(param["bits"])
            if param["kind"] == "fp":
                param["holder"] = ("the %d-bit float's IEEE bit "
                                   "pattern, in %s's own integer"
                                   % (param["bits"], self.lang))
                continue
            param["holder"] = ("a %d-bit value, in %s's own integer"
                               % (param["bits"], self.lang))

    # -- the file -----------------------------------------------------

    def render(self, term, text):
        self.plan_parameters(term)
        self.check_symbols(term)
        self.dialect.check_width(self.result_width)
        root_text, root_kind, root_width = self.emit(term)
        body = self.answer(root_text, root_kind, root_width)
        symbol = "emu_%s" % self.label
        names = []
        for param in self.params:
            names.append(self.dialect.param(param["name"]))
        comment = self.comment_lines(text)
        pieces = []
        pieces.append(self.dialect.prelude)
        pieces.append("\n")
        pieces.append(comment)
        pieces.append(self.dialect.function(symbol, names, body))
        call = "%s(%s)" % (symbol, self.argument_text(len(names)))
        pieces.append(self.dialect.main % {"symbol": symbol,
                                           "call": call})
        return "".join(pieces), symbol

    def comment_lines(self, text):
        """the term's own layer-5 text over the emulation, in the
        target's own comment spelling."""
        marks = {"cpython": "#", "ruby": "#", "javascript": "//",
                 "php": "//", "java": "    //", "dart": "//",
                 "csharp": "    //"}
        mark = marks[self.lang]
        lines = []
        lines.append("%s task ex1 emulation -- rendered by "
                     "interp_render.py" % mark)
        lines.append("%s InterpRenderer from the layer-4 term of %s."
                     % (mark, self.label))
        lines.append("%s The term's layer-5 text, LITERAL:" % mark)
        lines.append("%s   %s" % (mark, " ".join(text.split())))
        return "\n".join(lines) + "\n"

    def argument_text(self, count):
        """how the main hands the parsed arrivals to the emulation.
        The three fixed dialects parse into an array; the four others
        splat a list, which their own main already does."""
        if self.lang in ("java", "csharp"):
            parts = []
            for index in range(count):
                parts.append("values[%d]" % index)
            return ", ".join(parts)
        if self.lang == "dart":
            parts = []
            for index in range(count):
                parts.append("values[%d]" % index)
            return ", ".join(parts)
        return ""

    def answer(self, root_text, root_kind, root_width):
        width = self.result_width
        if width is None:
            raise E.Refused(E.CAUSE_STATE, "no answer home")
        self.dialect.check_width(width)
        if root_kind == "bool":
            return self.dialect.ite(root_text,
                                    self.dialect.lit(1, width),
                                    self.dialect.lit(0, width))
        if root_kind == "rm":
            raise E.Refused(E.CAUSE_OP, "a rounding mode as an answer")
        return self.helper("m", [root_text, width])

    # -- the helper call ----------------------------------------------

    def helper(self, name, args):
        parts = []
        for one in args:
            if isinstance(one, int):
                parts.append(self.dialect.width_text(one))
                continue
            parts.append(one)
        return self.dialect.call(self.dialect.prefix + name, parts)

    # -- one node -----------------------------------------------------

    def emit(self, node):
        """-> (text, kind, width).  `bv` is a non-negative value of
        `width` bits in the dialect's own integer, `fp` is the IEEE bit
        pattern of a float of `width` bits (which is the same carrier),
        `bool` is the dialect's own truth value, `rm` is a rounding
        mode and carries no text."""
        decl = node.decl()
        kind = decl.kind()
        if z3.is_const(node) and kind == z3.Z3_OP_UNINTERPRETED:
            return self.emit_symbol(node, None)
        if kind == z3.Z3_OP_BNUM:
            width = node.size()
            self.dialect.check_width(width)
            return self.dialect.lit(node.as_long(), width), "bv", width
        if kind == z3.Z3_OP_TRUE:
            return self.dialect.true_text, "bool", 1
        if kind == z3.Z3_OP_FALSE:
            return self.dialect.false_text, "bool", 1
        if kind == z3.Z3_OP_EXTRACT:
            return self.emit_extract(node)
        if kind == z3.Z3_OP_CONCAT:
            return self.emit_concat(node)
        if kind in (z3.Z3_OP_ZERO_EXT, z3.Z3_OP_SIGN_EXT):
            return self.emit_extend(node, kind == z3.Z3_OP_SIGN_EXT)
        if kind == z3.Z3_OP_ITE:
            return self.emit_ite(node)
        if kind in (z3.Z3_OP_AND, z3.Z3_OP_OR, z3.Z3_OP_NOT,
                    z3.Z3_OP_XOR, z3.Z3_OP_IMPLIES, z3.Z3_OP_IFF):
            return self.emit_logic(node, kind)
        if kind in (z3.Z3_OP_EQ, z3.Z3_OP_DISTINCT):
            return self.emit_equality(node, kind)
        if kind in (z3.Z3_OP_SLEQ, z3.Z3_OP_SLT, z3.Z3_OP_SGEQ,
                    z3.Z3_OP_SGT, z3.Z3_OP_ULEQ, z3.Z3_OP_ULT,
                    z3.Z3_OP_UGEQ, z3.Z3_OP_UGT):
            return self.emit_compare(node, kind)
        if kind in (z3.Z3_OP_BADD, z3.Z3_OP_BSUB, z3.Z3_OP_BMUL,
                    z3.Z3_OP_BAND, z3.Z3_OP_BOR, z3.Z3_OP_BXOR):
            return self.emit_arith(node, kind)
        if kind in (z3.Z3_OP_BNOT, z3.Z3_OP_BNEG):
            return self.emit_unary(node, kind)
        if kind in (z3.Z3_OP_BSHL, z3.Z3_OP_BLSHR, z3.Z3_OP_BASHR):
            return self.emit_shift(node, kind)
        if kind in (z3.Z3_OP_BUDIV, z3.Z3_OP_BUDIV_I, z3.Z3_OP_BUREM,
                    z3.Z3_OP_BUREM_I, z3.Z3_OP_BSDIV, z3.Z3_OP_BSDIV_I,
                    z3.Z3_OP_BSREM, z3.Z3_OP_BSREM_I):
            return self.emit_division(node, kind)
        if z3.is_fp(node) or z3.is_fprm(node) or \
                str(decl.name()).startswith("fp"):
            return self.emit_fp(node, kind)
        raise E.Refused(E.CAUSE_OP, "%s (kind %d)" % (decl.name(), kind))

    def emit_symbol(self, node, extract):
        name = node.decl().name()
        param = self.params[self.seed_names[name]]
        text = self.dialect.param(param["name"])
        width = param["bits"]
        if param["kind"] == "fp":
            # the arrival is the float's bits; c's own renderer takes
            # them with `f32_to_bits` at exactly this point.
            if extract is None:
                raise E.Refused(E.CAUSE_LANE, name)
            high, low = extract
            if low == 0 and high + 1 == width:
                return text, "bv", width
            return self.helper("ext", [text, high, low]), "bv", \
                high - low + 1
        if param["bits"] == E.X87_BITS:
            raise E.Refused(E.CAUSE_X87, name)
        if extract is None:
            if node.size() != 64:
                raise E.Refused(E.CAUSE_WIDTH,
                                "general arrival of %d bits"
                                % node.size())
            if width < 64:
                raise E.Refused(E.CAUSE_STATE,
                                "%s read at 64 bits but planned at %d"
                                % (name, width))
            return text, "bv", 64
        high, low = extract
        if low == 0 and high + 1 == width:
            return text, "bv", width
        return self.helper("ext", [text, high, low]), "bv", \
            high - low + 1

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
        return self.helper("ext", [text, high, low]), "bv", out

    def emit_concat(self, node):
        parts = []
        for index in range(node.num_args()):
            text, kind, width = self.emit(node.arg(index))
            self.expect(kind, "bv", node)
            parts.append((text, width))
        text, total = parts[0]
        for other, width in parts[1:]:
            text = self.helper("cat", [text, other, width])
            total = total + width
            self.dialect.check_width(total)
        return text, "bv", total

    def emit_extend(self, node, signed):
        extra = node.params()[0]
        text, kind, width = self.emit(node.arg(0))
        self.expect(kind, "bv", node)
        total = width + extra
        self.dialect.check_width(total)
        if not signed:
            # THE VALUE IS ALREADY NON-NEGATIVE, so a zero extension is
            # the identity on the carrier and only the width changes.
            return text, "bv", total
        return self.helper("sext", [text, width, total]), "bv", total

    def emit_ite(self, node):
        cond, ckind, _ = self.emit(node.arg(0))
        self.expect(ckind, "bool", node)
        left, lkind, lwidth = self.emit(node.arg(1))
        right, rkind, rwidth = self.emit(node.arg(2))
        if lkind != rkind or lwidth != rwidth:
            raise E.Refused(E.CAUSE_OP, "If with arms of different sorts")
        return self.dialect.ite(cond, left, right), lkind, lwidth

    def emit_logic(self, node, kind):
        args = []
        for index in range(node.num_args()):
            text, akind, _ = self.emit(node.arg(index))
            self.expect(akind, "bool", node)
            args.append("(%s)" % text)
        dialect = self.dialect
        if kind == z3.Z3_OP_NOT:
            return "(%s%s)" % (dialect.logic_not, args[0]), "bool", 1
        if kind == z3.Z3_OP_AND:
            joined = (" %s " % dialect.logic_and).join(args)
            return "(%s)" % joined, "bool", 1
        if kind == z3.Z3_OP_OR:
            joined = (" %s " % dialect.logic_or).join(args)
            return "(%s)" % joined, "bool", 1
        if kind == z3.Z3_OP_XOR:
            return "((%s) != (%s))" % (args[0], args[1]), "bool", 1
        if kind == z3.Z3_OP_IMPLIES:
            return "((%s%s) %s (%s))" % (dialect.logic_not, args[0],
                                         dialect.logic_or, args[1]), \
                "bool", 1
        return "((%s) == (%s))" % (args[0], args[1]), "bool", 1

    def emit_equality(self, node, kind):
        left, lkind, lwidth = self.emit(node.arg(0))
        right, rkind, rwidth = self.emit(node.arg(1))
        if lkind != rkind or lwidth != rwidth:
            raise E.Refused(E.CAUSE_OP, "equality across sorts")
        if lkind == "bool":
            if kind == z3.Z3_OP_EQ:
                return "((%s) == (%s))" % (left, right), "bool", 1
            return "((%s) != (%s))" % (left, right), "bool", 1
        if lkind == "rm":
            raise E.Refused(E.CAUSE_OP, "equality on rounding modes")
        name = "eq"
        if kind == z3.Z3_OP_DISTINCT:
            name = "ne"
        return self.helper(name, [left, right, lwidth]), "bool", 1

    NAMES = {z3.Z3_OP_SLEQ: "sle", z3.Z3_OP_SLT: "slt",
             z3.Z3_OP_SGEQ: "sge", z3.Z3_OP_SGT: "sgt",
             z3.Z3_OP_ULEQ: "ule", z3.Z3_OP_ULT: "ult",
             z3.Z3_OP_UGEQ: "uge", z3.Z3_OP_UGT: "ugt",
             z3.Z3_OP_BADD: "add", z3.Z3_OP_BSUB: "sub",
             z3.Z3_OP_BMUL: "mul", z3.Z3_OP_BAND: "band",
             z3.Z3_OP_BOR: "bor", z3.Z3_OP_BXOR: "bxor",
             z3.Z3_OP_BNOT: "bnot", z3.Z3_OP_BNEG: "bneg",
             z3.Z3_OP_BSHL: "shl", z3.Z3_OP_BLSHR: "lshr",
             z3.Z3_OP_BASHR: "ashr"}

    def emit_compare(self, node, kind):
        left, lkind, lwidth = self.emit(node.arg(0))
        right, rkind, rwidth = self.emit(node.arg(1))
        self.expect(lkind, "bv", node)
        self.expect(rkind, "bv", node)
        if lwidth != rwidth:
            raise E.Refused(E.CAUSE_OP, "comparison across widths")
        return self.helper(self.NAMES[kind], [left, right, lwidth]), \
            "bool", 1

    def emit_arith(self, node, kind):
        args = []
        width = None
        for index in range(node.num_args()):
            text, akind, awidth = self.emit(node.arg(index))
            self.expect(akind, "bv", node)
            if width is None:
                width = awidth
            elif width != awidth:
                raise E.Refused(E.CAUSE_OP, "arithmetic across widths")
            args.append(text)
        text = args[0]
        for other in args[1:]:
            text = self.helper(self.NAMES[kind], [text, other, width])
        return text, "bv", width

    def emit_unary(self, node, kind):
        text, akind, width = self.emit(node.arg(0))
        self.expect(akind, "bv", node)
        return self.helper(self.NAMES[kind], [text, width]), "bv", width

    def emit_shift(self, node, kind):
        value, vkind, width = self.emit(node.arg(0))
        amount, akind, awidth = self.emit(node.arg(1))
        self.expect(vkind, "bv", node)
        self.expect(akind, "bv", node)
        return self.helper(self.NAMES[kind], [value, amount, width]), \
            "bv", width

    def emit_division(self, node, kind):
        left, lkind, lwidth = self.emit(node.arg(0))
        right, rkind, rwidth = self.emit(node.arg(1))
        self.expect(lkind, "bv", node)
        self.expect(rkind, "bv", node)
        if lwidth != rwidth:
            raise E.Refused(E.CAUSE_OP, "division across widths")
        signed = kind in (z3.Z3_OP_BSDIV, z3.Z3_OP_BSDIV_I,
                          z3.Z3_OP_BSREM, z3.Z3_OP_BSREM_I)
        remainder = kind in (z3.Z3_OP_BUREM, z3.Z3_OP_BUREM_I,
                             z3.Z3_OP_BSREM, z3.Z3_OP_BSREM_I)
        name = "udiv"
        if signed and remainder:
            name = "srem"
        elif signed:
            name = "sdiv"
        elif remainder:
            name = "urem"
        return self.helper(name, [left, right, lwidth]), "bv", lwidth

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
            self.dialect.check_width(width)
            bits_value = z3.simplify(z3.fpToIEEEBV(node)).as_long()
            return self.dialect.lit(bits_value, width), "fp", width
        if kind == z3.Z3_OP_FPA_TO_FP:
            return self.emit_to_fp(node)
        if kind == z3.Z3_OP_FPA_TO_FP_UNSIGNED:
            self.expect_rne(node.arg(0))
            text, akind, awidth = self.emit(node.arg(1))
            self.expect(akind, "bv", node)
            width = E.fp_width(node.sort())
            self.dialect.check_width(width)
            return self.helper("u2f", [text, awidth, width]), "fp", width
        if kind == z3.Z3_OP_FPA_TO_IEEE_BV:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            if awidth == E.X87_BITS:
                raise E.Refused(E.CAUSE_X87,
                                "this term reads an x87 value's bits")
            # THE IDENTITY, and it is the whole point of carrying a
            # float as its bits: this node asks for the bits of a value
            # that is already being carried as its bits.
            return text, "bv", awidth
        if kind in (z3.Z3_OP_FPA_ADD, z3.Z3_OP_FPA_SUB,
                    z3.Z3_OP_FPA_MUL, z3.Z3_OP_FPA_DIV):
            names = {z3.Z3_OP_FPA_ADD: "fadd", z3.Z3_OP_FPA_SUB: "fsub",
                     z3.Z3_OP_FPA_MUL: "fmul", z3.Z3_OP_FPA_DIV: "fdiv"}
            self.expect_rne(node.arg(0))
            left, lkind, lwidth = self.emit(node.arg(1))
            right, rkind, rwidth = self.emit(node.arg(2))
            self.expect(lkind, "fp", node)
            self.expect(rkind, "fp", node)
            if lwidth != rwidth:
                raise E.Refused(E.CAUSE_OP,
                                "float arithmetic across widths")
            return self.helper(names[kind], [left, right, lwidth]), \
                "fp", lwidth
        raise E.Refused(E.CAUSE_OP, "%s (kind %d)" % (name, kind))

    def emit_to_fp(self, node):
        width = E.fp_width(node.sort())
        self.dialect.check_width(width)
        if node.num_args() == 1:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "bv", node)
            if awidth != width:
                raise E.Refused(E.CAUSE_WIDTH,
                                "%d bits reinterpreted as a %d-bit "
                                "float" % (awidth, width))
            # THE IDENTITY: a bit pattern read as a float, and a float
            # is carried here as its bit pattern.
            return text, "fp", width
        if node.num_args() == 2:
            self.expect_rne(node.arg(0))
            text, akind, awidth = self.emit(node.arg(1))
            if akind == "fp":
                return self.helper("fwiden", [text, awidth, width]), \
                    "fp", width
            if akind == "bv":
                return self.helper("i2f", [text, awidth, width]), \
                    "fp", width
        raise E.Refused(E.CAUSE_OP, "fpToFP with %d arguments"
                        % node.num_args())


def runners_command():
    for lang in LANGUAGES:
        sys.stdout.write("   %-12s %s\n" % (lang, runner_answer(lang)))
    sys.stdout.flush()
    return 0


def main(argv):
    if not argv:
        sys.stdout.write(__doc__ + "\n")
        return 2
    if argv[0] == "runners":
        return runners_command()
    sys.stdout.write(__doc__ + "\n")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
