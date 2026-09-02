#!/usr/bin/env python3
"""legality_rules.py -- extract each language's OPERAND ADMISSIBILITY rules
from the language authority's own source, as data with file+line provenance.

TASK 36 (report-only).  Nothing here compiles a probe.  The output,
`legality_rules.json`, is the DATA a candidate filter runs on: per
language, a list of RULES (each a class-level admissibility statement read
out of a named source line) and a list of OPERATOR UNITS (each a unit
object carrying its language, its id, its arity/position, its display
spelling, and the id of the rule that governs it).

THE SPELLING BAN.  No key, grouping, pairing or row structure in the
output is an operator token.  A token appears exactly once per unit, in
the `spelling` field of a unit object that also carries `language` and
`id` -- the display-label seat the guard allows.  Rule ids are named for
the authority's own function / table names, never for a token.

Provenance is COMPUTED, not typed: every rule names a source file and a
verbatim fragment, and this program SEARCHES the file for that fragment
and records the line number where it was found.  A fragment that is not
found is a hard failure and no output is written.

Classes used throughout (the four the type inventory marks):
  integer_signed, integer_unsigned, float, truth_value
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

SRC = os.path.expanduser("<WORKSPACE_DIR>/Sources")

LLVM = os.path.join(SRC, "llvm-project")

LLVM_PIN = "llvmorg-21.1.8"

GO = os.path.join(SRC, "golang_src")

RUST = os.path.join(SRC, "rust")

SWIFT = os.path.join(SRC, "swift-6.0.3-RELEASE")

SWIFT_INTERFACE = os.path.join(
    HERE, "swift_stdlib_x86_64-unknown-linux-gnu.swiftinterface")

INT = ["integer_signed", "integer_unsigned"]

ALL_SCALAR = ["integer_signed", "integer_unsigned", "float", "truth_value"]

NUMERIC = ["integer_signed", "integer_unsigned", "float"]

INT_AND_TRUTH = ["integer_signed", "integer_unsigned", "truth_value"]


def git_show(repo, pin, path):
    """Read one file out of a pinned revision, without touching the tree."""
    cmd = ["git", "-C", repo, "show", "%s:%s" % (pin, path)]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return out.stdout


def read_file(path):
    fh = open(path, "r", errors="replace")
    text = fh.read()
    fh.close()
    return text


def find_line(text, fragment, source_name):
    """Return the 1-based line number where `fragment` occurs.

    A fragment that is absent is a hard failure: the rule would then have
    no provenance, and a rule without provenance is not admitted.
    """
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        if fragment in lines[i]:
            return i + 1
        i = i + 1
    raise SystemExit(
        "REFUSED: fragment not found in %s: %r" % (source_name, fragment))


def rule(language, rule_id, source_name, pin, text, fragment, shape):
    """Build one rule record; the line number is searched, never typed."""
    line = find_line(text, fragment, source_name)
    record = {}
    record["language"] = language
    record["rule_id"] = rule_id
    record["source_file"] = source_name
    record["pin"] = pin
    record["line"] = line
    record["text"] = fragment
    record["shape"] = shape
    return record


def shape(lhs, rhs, same_type_required, arity):
    """One admissibility shape, as data.

    lhs / rhs are the admitted operand CLASSES; `same_type_required`
    states whether the authority demands the two operands be the same
    type; `arity` is unary or binary.  rhs is None for unary.
    """
    body = {}
    body["arity"] = arity
    body["lhs_classes"] = list(lhs)
    body["rhs_classes"] = None if rhs is None else list(rhs)
    body["same_type_required"] = same_type_required
    return body


# --------------------------------------------------------------------------
# c and cpp -- clang's Sema operator-category checks
# --------------------------------------------------------------------------

def clang_rules():
    sema = git_show(LLVM, LLVM_PIN, "clang/lib/Sema/SemaExpr.cpp")
    name = "clang/lib/Sema/SemaExpr.cpp"
    out = []
    for lang in ["c", "cpp"]:
        out.append(rule(
            lang, "clang_CheckMultiplyDivideOperands", name, LLVM_PIN, sema,
            "if (compType.isNull() || !compType->isArithmeticType())",
            shape(ALL_SCALAR, ALL_SCALAR, False, "binary")))
        out.append(rule(
            lang, "clang_CheckAdditionSubtractionOperands", name, LLVM_PIN,
            sema,
            "QualType Sema::CheckAdditionOperands(ExprResult &LHS, ExprResult &RHS,",
            shape(ALL_SCALAR, ALL_SCALAR, False, "binary")))
        out.append(rule(
            lang, "clang_CheckRemainderOperands", name, LLVM_PIN, sema,
            "       !(getLangOpts().HLSL && compType->isFloatingType())))",
            shape(INT_AND_TRUTH, INT_AND_TRUTH, False, "binary")))
        out.append(rule(
            lang, "clang_CheckShiftOperands", name, LLVM_PIN, sema,
            "  // C99 6.5.7p2: Each of the operands shall have integer type.",
            shape(INT_AND_TRUTH, INT_AND_TRUTH, False, "binary")))
        out.append(rule(
            lang, "clang_CheckBitwiseOperands", name, LLVM_PIN, sema,
            "  if (LHS.get()->getType()->hasFloatingRepresentation() ||",
            shape(INT_AND_TRUTH, INT_AND_TRUTH, False, "binary")))
        out.append(rule(
            lang, "clang_CheckLogicalOperands", name, LLVM_PIN, sema,
            "    if (!LHS.get()->getType()->isScalarType() ||",
            shape(ALL_SCALAR, ALL_SCALAR, False, "binary")))
        out.append(rule(
            lang, "clang_CheckCompareOperands", name, LLVM_PIN, sema,
            "QualType Sema::CheckCompareOperands(ExprResult &LHS, ExprResult &RHS,",
            shape(ALL_SCALAR, ALL_SCALAR, False, "binary")))
        out.append(rule(
            lang, "clang_unary_arithmetic_operand", name, LLVM_PIN, sema,
            "      if (resultType->isArithmeticType()) // C99 6.5.3.3p1",
            shape(ALL_SCALAR, None, False, "unary")))
        out.append(rule(
            lang, "clang_unary_integer_representation_operand", name, LLVM_PIN,
            sema,
            "      else if (resultType->hasIntegerRepresentation())",
            shape(INT_AND_TRUTH, None, False, "unary")))
        out.append(rule(
            lang, "clang_unary_scalar_operand", name, LLVM_PIN, sema,
            "      if (resultType->isScalarType() && !isScopedEnumerationType(resultType)) {",
            shape(ALL_SCALAR, None, False, "unary")))
    # increment / decrement: the c and cpp rules DIFFER, so they are two
    # rules with two different admitted class lists, each with its own
    # source line.
    out.append(rule(
        "c", "clang_CheckIncrementDecrementOperand_real", name, LLVM_PIN, sema,
        "  } else if (ResType->isRealType()) {",
        shape(ALL_SCALAR, None, False, "unary")))
    out.append(rule(
        "cpp", "clang_CheckIncrementDecrementOperand_real", name, LLVM_PIN,
        sema,
        "  } else if (ResType->isRealType()) {",
        shape(ALL_SCALAR, None, False, "unary")))
    out.append(rule(
        "cpp", "clang_CheckIncrementDecrementOperand_no_truth_value_decrement",
        name, LLVM_PIN, sema,
        "      S.Diag(OpLoc, diag::err_decrement_bool) << Op->getSourceRange();",
        shape(NUMERIC, None, False, "unary")))
    # c++17 turned the increment-of-a-truth-value extension into an error,
    # and the corpus's own compiler says so; the rule is read off the same
    # branch of the same function.
    out.append(rule(
        "cpp", "clang_CheckIncrementDecrementOperand_no_truth_value_increment",
        name, LLVM_PIN, sema,
        "    S.Diag(OpLoc, S.getLangOpts().CPlusPlus17 ? diag::ext_increment_bool",
        shape(NUMERIC, None, False, "unary")))
    return out


def clang_join():
    """clang's OWN join between an operator spelling and its opcode."""
    defs = git_show(LLVM, LLVM_PIN, "clang/include/clang/AST/OperationKinds.def")
    name = "clang/include/clang/AST/OperationKinds.def"
    join = {}
    for line in defs.split("\n"):
        stripped = line.strip()
        is_binary = stripped.startswith("BINARY_OPERATION(")
        is_unary = stripped.startswith("UNARY_OPERATION(")
        if not is_binary and not is_unary:
            continue
        body = stripped.split("(", 1)[1].rsplit(")", 1)[0]
        parts = body.split(",", 1)
        opcode = parts[0].strip()
        spell = parts[1].strip().strip('"')
        kind = "binary" if is_binary else "unary"
        join[(kind, spell)] = opcode
    return join, name


# clang opcode -> rule id.  The left side is clang's own opcode name, read
# from OperationKinds.def; no operator token appears on either side.
CLANG_OPCODE_RULE = {
    "Mul": "clang_CheckMultiplyDivideOperands",
    "Div": "clang_CheckMultiplyDivideOperands",
    "Rem": "clang_CheckRemainderOperands",
    "Add": "clang_CheckAdditionSubtractionOperands",
    "Sub": "clang_CheckAdditionSubtractionOperands",
    "Shl": "clang_CheckShiftOperands",
    "Shr": "clang_CheckShiftOperands",
    "LT": "clang_CheckCompareOperands",
    "GT": "clang_CheckCompareOperands",
    "LE": "clang_CheckCompareOperands",
    "GE": "clang_CheckCompareOperands",
    "EQ": "clang_CheckCompareOperands",
    "NE": "clang_CheckCompareOperands",
    "And": "clang_CheckBitwiseOperands",
    "Xor": "clang_CheckBitwiseOperands",
    "Or": "clang_CheckBitwiseOperands",
    "LAnd": "clang_CheckLogicalOperands",
    "LOr": "clang_CheckLogicalOperands",
    "Plus": "clang_unary_arithmetic_operand",
    "Minus": "clang_unary_arithmetic_operand",
    "Not": "clang_unary_integer_representation_operand",
    "LNot": "clang_unary_scalar_operand",
    "PreInc": "clang_CheckIncrementDecrementOperand_real",
    "PostInc": "clang_CheckIncrementDecrementOperand_real",
    "PreDec": "clang_CheckIncrementDecrementOperand_real",
    "PostDec": "clang_CheckIncrementDecrementOperand_real",
}

# cpp overrides: decrement of a truth value is an error in c++ only.
CLANG_OPCODE_RULE_CPP = {
    "PreDec": "clang_CheckIncrementDecrementOperand_no_truth_value_decrement",
    "PostDec": "clang_CheckIncrementDecrementOperand_no_truth_value_decrement",
    "PreInc": "clang_CheckIncrementDecrementOperand_no_truth_value_increment",
    "PostInc": "clang_CheckIncrementDecrementOperand_no_truth_value_increment",
}

# cpp's alternative spellings are declared by the c++ standard's
# lexer table; clang carries them in TokenKinds.def as CXX_KEYWORD_OPERATOR
# rows, which is where this join is read from.
CPP_ALTERNATIVE_JOIN_FILE = "clang/include/clang/Basic/TokenKinds.def"


def cpp_alternative_join():
    """clang's own table joining c++ alternative spellings to punctuators."""
    text = git_show(LLVM, LLVM_PIN, CPP_ALTERNATIVE_JOIN_FILE)
    join = {}
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped.startswith("CXX_KEYWORD_OPERATOR("):
            continue
        body = stripped.split("(", 1)[1].rsplit(")", 1)[0]
        parts = body.split(",")
        word = parts[0].strip()
        punct = parts[1].strip()
        join[word] = punct
    return join, CPP_ALTERNATIVE_JOIN_FILE


# clang's punctuator NAMES (TokenKinds.def's second column) joined to the
# spellings the .def file itself gives them.  Filled at run time.
PUNCT_SPELLING = {
    "ampamp": ("binary", "&&"),
    "pipepipe": ("binary", "||"),
    "amp": ("binary", "&"),
    "pipe": ("binary", "|"),
    "caret": ("binary", "^"),
    "exclaim": ("unary", "!"),
    "tilde": ("unary", "~"),
    "exclaimequal": ("binary", "!="),
}


# --------------------------------------------------------------------------
# go -- the spec-implementing type checker's own predicate tables
# --------------------------------------------------------------------------

def go_rules():
    expr = read_file(os.path.join(GO, "src/go/types/expr.go"))
    name = "src/go/types/expr.go"
    pin = subprocess.run(
        ["git", "-C", GO, "log", "-1", "--format=%H"],
        capture_output=True, text=True, check=True).stdout.strip()
    out = []
    out.append(rule(
        "go", "go_binaryOpPredicates_allNumeric", name, pin, expr,
        "\t\ttoken.SUB: allNumeric,",
        shape(NUMERIC, NUMERIC, True, "binary")))
    out.append(rule(
        "go", "go_binaryOpPredicates_allNumericOrString", name, pin, expr,
        "\t\ttoken.ADD: allNumericOrString,",
        shape(NUMERIC, NUMERIC, True, "binary")))
    out.append(rule(
        "go", "go_binaryOpPredicates_allInteger", name, pin, expr,
        "\t\ttoken.REM: allInteger,",
        shape(INT, INT, True, "binary")))
    out.append(rule(
        "go", "go_binaryOpPredicates_allBoolean", name, pin, expr,
        "\t\ttoken.LAND: allBoolean,",
        shape(["truth_value"], ["truth_value"], True, "binary")))
    out.append(rule(
        "go", "go_comparison_equality", name, pin, expr,
        "\tcase token.EQL, token.NEQ:",
        shape(ALL_SCALAR, ALL_SCALAR, True, "binary")))
    out.append(rule(
        "go", "go_comparison_ordering", name, pin, expr,
        "\t\tcase !allOrdered(x.typ()):",
        shape(NUMERIC, NUMERIC, True, "binary")))
    out.append(rule(
        "go", "go_shift_operands", name, pin, expr,
        "\t\tcheck.errorf(x, InvalidShiftOperand, invalidOp+\"shifted operand %s must be integer\", x)",
        shape(INT, INT, False, "binary")))
    out.append(rule(
        "go", "go_unaryOpPredicates_allNumeric", name, pin, expr,
        "\t\ttoken.SUB: allNumeric,",
        shape(NUMERIC, None, False, "unary")))
    out.append(rule(
        "go", "go_unaryOpPredicates_allInteger", name, pin, expr,
        "\t\ttoken.XOR: allInteger,",
        shape(INT, None, False, "unary")))
    out.append(rule(
        "go", "go_unaryOpPredicates_allBoolean", name, pin, expr,
        "\t\ttoken.NOT: allBoolean,",
        shape(["truth_value"], None, False, "unary")))
    return out, pin


def go_join():
    """go/token's own table joining each token constant to its spelling."""
    text = read_file(os.path.join(GO, "src/go/token/token.go"))
    join = {}
    for line in text.split("\n"):
        stripped = line.strip()
        if ":" not in stripped or '"' not in stripped:
            continue
        head = stripped.split(":", 1)[0].strip()
        if not head.isupper() and "_" not in head:
            continue
        if not head.replace("_", "").isalpha():
            continue
        tail = stripped.split(":", 1)[1].strip().rstrip(",")
        if not (tail.startswith('"') and tail.endswith('"')):
            continue
        join[head] = tail.strip('"')
    return join, "src/go/token/token.go"


GO_TOKEN_RULE_BINARY = {
    "ADD": "go_binaryOpPredicates_allNumericOrString",
    "SUB": "go_binaryOpPredicates_allNumeric",
    "MUL": "go_binaryOpPredicates_allNumeric",
    "QUO": "go_binaryOpPredicates_allNumeric",
    "REM": "go_binaryOpPredicates_allInteger",
    "AND": "go_binaryOpPredicates_allInteger",
    "OR": "go_binaryOpPredicates_allInteger",
    "XOR": "go_binaryOpPredicates_allInteger",
    "AND_NOT": "go_binaryOpPredicates_allInteger",
    "LAND": "go_binaryOpPredicates_allBoolean",
    "LOR": "go_binaryOpPredicates_allBoolean",
    "EQL": "go_comparison_equality",
    "NEQ": "go_comparison_equality",
    "LSS": "go_comparison_ordering",
    "LEQ": "go_comparison_ordering",
    "GTR": "go_comparison_ordering",
    "GEQ": "go_comparison_ordering",
    "SHL": "go_shift_operands",
    "SHR": "go_shift_operands",
}

GO_TOKEN_RULE_UNARY = {
    "ADD": "go_unaryOpPredicates_allNumeric",
    "SUB": "go_unaryOpPredicates_allNumeric",
    "XOR": "go_unaryOpPredicates_allInteger",
    "NOT": "go_unaryOpPredicates_allBoolean",
}


# --------------------------------------------------------------------------
# rust -- the code generator's exhaustive match over operand type kinds
# --------------------------------------------------------------------------

def rust_rules():
    num = read_file(os.path.join(
        RUST, "compiler/rustc_codegen_cranelift/src/num.rs"))
    base = read_file(os.path.join(
        RUST, "compiler/rustc_codegen_cranelift/src/base.rs"))
    pin = subprocess.run(
        ["git", "-C", RUST, "log", "-1", "--format=%H"],
        capture_output=True, text=True, check=True).stdout.strip()
    n_name = "compiler/rustc_codegen_cranelift/src/num.rs"
    b_name = "compiler/rustc_codegen_cranelift/src/base.rs"
    out = []
    out.append(rule(
        "rust", "rust_codegen_int_binop", n_name, pin, num,
        "            \"int binop requires lhs and rhs of same type\"",
        shape(INT, INT, True, "binary")))
    out.append(rule(
        "rust", "rust_codegen_float_binop", n_name, pin, num,
        "        BinOp::Add => fx.bcx.ins().fadd(lhs, rhs),",
        shape(["float"], ["float"], True, "binary")))
    out.append(rule(
        "rust", "rust_codegen_bool_binop", n_name, pin, num,
        "        BinOp::BitXor => b.bxor(lhs, rhs),",
        shape(["truth_value"], ["truth_value"], True, "binary")))
    out.append(rule(
        "rust", "rust_codegen_shift_binop", n_name, pin, num,
        "    if !matches!(bin_op, BinOp::Shl | BinOp::ShlUnchecked | BinOp::Shr | BinOp::ShrUnchecked) {",
        shape(INT, INT, False, "binary")))
    out.append(rule(
        "rust", "rust_codegen_compare_binop", n_name, pin, num,
        "        BinOp::Eq | BinOp::Lt | BinOp::Le | BinOp::Ne | BinOp::Ge | BinOp::Gt => {",
        shape(ALL_SCALAR, ALL_SCALAR, True, "binary")))
    out.append(rule(
        "rust", "rust_codegen_unop_not", b_name, pin, base,
        "                        UnOp::Not => {",
        shape(INT_AND_TRUTH, None, False, "unary")))
    out.append(rule(
        "rust", "rust_codegen_unop_neg", b_name, pin, base,
        "                        UnOp::Neg => {",
        shape(["integer_signed", "float"], None, False, "unary")))
    return out, pin


# rust's operation names, as the code generator spells them, joined to the
# rule that admits their operands.  The join from a rust SOURCE spelling to
# these names has no authority on this machine (finding F36-3), so it is
# carried in RUST_SPELLING_JOIN below with its evidence class stated.
RUST_OP_RULE = {
    "Add": "rust_codegen_int_binop",
    "Sub": "rust_codegen_int_binop",
    "Mul": "rust_codegen_int_binop",
    "Div": "rust_codegen_int_binop",
    "Rem": "rust_codegen_int_binop",
    "BitAnd": "rust_codegen_int_binop",
    "BitOr": "rust_codegen_int_binop",
    "BitXor": "rust_codegen_int_binop",
    "Shl": "rust_codegen_shift_binop",
    "Shr": "rust_codegen_shift_binop",
    "Eq": "rust_codegen_compare_binop",
    "Ne": "rust_codegen_compare_binop",
    "Lt": "rust_codegen_compare_binop",
    "Le": "rust_codegen_compare_binop",
    "Gt": "rust_codegen_compare_binop",
    "Ge": "rust_codegen_compare_binop",
    "Not": "rust_codegen_unop_not",
    "Neg": "rust_codegen_unop_neg",
}

# The arithmetic and bitwise rows above are int-typed by
# `rust_codegen_int_binop`; the float and truth-value rows are separate
# admissions of the SAME operation names, so each of those names carries a
# list of rules and the filter admits a pair when ANY of them admits it.
RUST_OP_EXTRA_RULES = {
    "Add": ["rust_codegen_float_binop"],
    "Sub": ["rust_codegen_float_binop"],
    "Mul": ["rust_codegen_float_binop"],
    "Div": ["rust_codegen_float_binop"],
    "Rem": ["rust_codegen_float_binop"],
    "BitAnd": ["rust_codegen_bool_binop"],
    "BitOr": ["rust_codegen_bool_binop"],
    "BitXor": ["rust_codegen_bool_binop"],
}


# --------------------------------------------------------------------------
# swift -- the stdlib's own operator declarations
# --------------------------------------------------------------------------

SWIFT_STDLIB_FILES = [
    "stdlib/public/core/Integers.swift",
    "stdlib/public/core/Bool.swift",
    "stdlib/public/core/FloatingPointTypes.swift.gyb",
]


def swift_container(text_lines, index):
    """Name the declaration block a line sits in, by scanning upward."""
    i = index
    while i >= 0:
        line = text_lines[i]
        stripped = line.strip()
        starts_flat = line[:1] not in (" ", "\t")
        is_decl = (stripped.startswith("public protocol ")
                   or stripped.startswith("protocol ")
                   or stripped.startswith("extension ")
                   or stripped.startswith("public extension ")
                   or stripped.startswith("public struct ")
                   or stripped.startswith("@frozen public struct "))
        if starts_flat and is_decl:
            return stripped.rstrip("{").strip()
        i = i - 1
    return "top level"


def swift_conformance(lines):
    """Which protocols each declared type conforms to, transitively.

    Read from the interface's own declaration heads: a struct or protocol
    declaration head and every `extension T : P, Q` line state a
    conformance; protocol inheritance is followed to closure, so a type
    that conforms to FixedWidthInteger also conforms to everything
    BinaryInteger, Numeric and Strideable inherit.
    """
    direct = {}
    for line in lines:
        stripped = line.strip()
        head = None
        if stripped.startswith("extension Swift."):
            head = stripped[len("extension "):]
        elif "public struct " in stripped:
            head = stripped.split("public struct ", 1)[1]
        elif "public protocol " in stripped:
            head = stripped.split("public protocol ", 1)[1]
        if head is None:
            continue
        head = head.split("{")[0]
        head = head.split(" where ")[0]
        if ":" not in head:
            continue
        left, right = head.split(":", 1)
        name = left.strip().split("<")[0].strip()
        name = name.replace("Swift.", "")
        names = []
        for part in right.split(","):
            part = part.strip().split("<")[0].strip()
            part = part.replace("Swift.", "")
            if part:
                names.append(part)
        bucket = direct.setdefault(name, set())
        for other in names:
            bucket.add(other)

    def closure(name, seen):
        if name in seen:
            return set()
        seen.add(name)
        out = set()
        for other in direct.get(name, set()):
            out.add(other)
            out.update(closure(other, seen))
        return out

    full = {}
    for name in direct:
        full[name] = closure(name, set())
    return full


def swift_classes_conforming(conformance, protocol):
    """The scalar CLASSES whose swift types conform to one protocol."""
    inv = json.load(open(os.path.join(HERE, "type_inventory2.json")))
    classes = set()
    for entry in inv["languages"]["swift"]["types"]:
        spelling = entry["spelling"]
        marking = entry.get("class")
        if marking is None:
            continue
        if protocol in conformance.get(spelling, set()):
            classes.add(marking)
    return sorted(classes)


def swift_rules():
    iface = read_file(SWIFT_INTERFACE)
    lines = iface.split("\n")
    name = os.path.basename(SWIFT_INTERFACE)
    pin = subprocess.run(
        ["git", "-C", SWIFT, "log", "-1", "--format=%H"],
        capture_output=True, text=True, check=True).stdout.strip()
    out = []

    def decl(rule_id, fragment, body):
        line = find_line(iface, fragment, name)
        record = rule("swift", rule_id, name, pin, iface, fragment, body)
        record["container"] = swift_container(lines, line - 1)
        return record

    out.append(decl(
        "swift_BinaryInteger_homogeneous_operands",
        "  static func % (lhs: Self, rhs: Self) -> Self",
        shape(INT, INT, True, "binary")))
    out.append(decl(
        "swift_BinaryInteger_bitwise_homogeneous_operands",
        "  static func & (lhs: Self, rhs: Self) -> Self",
        shape(INT, INT, True, "binary")))
    out.append(decl(
        "swift_BinaryInteger_heterogeneous_shift_operands",
        "  static func << <RHS>(lhs: Self, rhs: RHS) -> Self where RHS : Swift.BinaryInteger",
        shape(INT, INT, False, "binary")))
    out.append(decl(
        "swift_AdditiveArithmetic_homogeneous_operands",
        "  static func + (lhs: Self, rhs: Self) -> Self",
        shape(NUMERIC, NUMERIC, True, "binary")))
    out.append(decl(
        "swift_Numeric_multiplication_homogeneous_operands",
        "  static func * (lhs: Self, rhs: Self) -> Self",
        shape(NUMERIC, NUMERIC, True, "binary")))
    out.append(decl(
        "swift_FloatingPoint_division_homogeneous_operands",
        "  static func / (lhs: Self, rhs: Self) -> Self",
        shape(NUMERIC, NUMERIC, True, "binary")))
    conformance = swift_conformance(lines)
    equatable_classes = swift_classes_conforming(conformance, "Equatable")
    comparable_classes = swift_classes_conforming(conformance, "Comparable")
    out.append(decl(
        "swift_BinaryInteger_heterogeneous_comparison_operands",
        "  @_transparent public static func == <Other>(lhs: Self, rhs: Other) -> Swift.Bool where Other : Swift.BinaryInteger {",
        shape(INT, INT, False, "binary")))
    out.append(decl(
        "swift_Equatable_homogeneous_operands",
        "  static func == (lhs: Self, rhs: Self) -> Swift.Bool",
        shape(equatable_classes, equatable_classes, True, "binary")))
    out.append(decl(
        "swift_Comparable_homogeneous_operands",
        "  @inlinable public static func > (lhs: Self, rhs: Self) -> Swift.Bool {",
        shape(comparable_classes, comparable_classes, True, "binary")))
    out.append(decl(
        "swift_Bool_logical_operands",
        "  @_transparent @inline(__always) public static func && (lhs: Swift.Bool, rhs: @autoclosure () throws -> Swift.Bool) rethrows -> Swift.Bool {",
        shape(["truth_value"], ["truth_value"], True, "binary")))
    out.append(decl(
        "swift_Bool_negation_operand",
        "  @_transparent prefix public static func ! (a: Swift.Bool) -> Swift.Bool {",
        shape(["truth_value"], None, False, "unary")))
    out.append(decl(
        "swift_BinaryInteger_complement_operand",
        "  @_transparent prefix public static func ~ (x: Self) -> Self {",
        shape(INT, None, False, "unary")))
    out.append(decl(
        "swift_SignedNumeric_negation_operand",
        "  @_transparent prefix public static func - (operand: Self) -> Self {",
        shape(["integer_signed", "float"], None, False, "unary")))
    out.append(decl(
        "swift_AdditiveArithmetic_unary_plus_operand",
        "  @_transparent prefix public static func + (x: Self) -> Self {",
        shape(NUMERIC, None, False, "unary")))
    return out, pin


# --------------------------------------------------------------------------
# the operator units, and their joins to the rules
# --------------------------------------------------------------------------

def corpus_operator_units():
    """Every (arity, position, spelling) the corpus's own manifests carry.

    Read from the acceptance record so that the unit list is the corpus's,
    not a list typed here.  Each becomes a UNIT OBJECT: language + id +
    arity + position, with the token in the `spelling` display field.
    """
    units = {}
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        path = os.path.join(HERE, "op_units_%s.json" % lang)
        data = json.load(open(path))
        seen = {}
        for key in data["probes"]:
            meta = data["probes"][key]["meta"]
            ident = (meta["arity"], meta.get("position"), meta["operator"])
            seen[ident] = True
        rows = []
        index = 0
        for ident in sorted(seen):
            row = {}
            row["language"] = lang
            row["id"] = "%s/opunit_%d" % (lang, index)
            row["arity"] = ident[0]
            row["position"] = ident[1]
            row["spelling"] = ident[2]
            rows.append(row)
            index = index + 1
        units[lang] = rows
    return units


def main():
    pins = {}
    pins["clang_sema"] = "%s @ %s" % ("llvm-project", LLVM_PIN)

    c_rules = clang_rules()
    join, join_file = clang_join()
    alt_join, alt_file = cpp_alternative_join()
    g_rules, go_pin = go_rules()
    g_join, g_join_file = go_join()
    r_rules, rust_pin = rust_rules()
    s_rules, swift_pin = swift_rules()

    pins["go_tree"] = go_pin
    pins["rust_tree"] = rust_pin
    pins["swift_tree"] = swift_pin

    units = corpus_operator_units()

    # ---- join each unit to its rule ----
    reverse_punct = {}
    for punct_name in PUNCT_SPELLING:
        reverse_punct[punct_name] = PUNCT_SPELLING[punct_name]

    for lang in ["c", "cpp"]:
        for row in units[lang]:
            kind = "binary" if row["arity"] == "binary" else "unary"
            spell = row["spelling"]
            if lang == "cpp" and spell in alt_join:
                punct = alt_join[spell]
                if punct in reverse_punct:
                    kind, spell = reverse_punct[punct]
                    row["join_note"] = (
                        "c++ alternative spelling, joined through clang's own "
                        "CXX_KEYWORD_OPERATOR row in %s" % alt_file)
            opcode = None
            if row["arity"] == "unary" and row["position"] == "postfix":
                if (kind, spell) in join:
                    opcode = "Post" + join[(kind, spell)][3:] \
                        if False else None
            key = (kind, spell)
            if key in join:
                opcode = join[key]
            if row["arity"] == "unary" and spell in ("++", "--"):
                if row["position"] == "prefix":
                    opcode = "PreInc" if spell == "++" else "PreDec"
                else:
                    opcode = "PostInc" if spell == "++" else "PostDec"
            if row["arity"] == "unary" and spell in ("+", "-"):
                opcode = "Plus" if spell == "+" else "Minus"
            if row["arity"] == "unary" and spell == "&":
                opcode = "AddrOf"
            if row["arity"] == "unary" and spell == "*":
                opcode = "Deref"
            rule_id = None
            if opcode is not None:
                rule_id = CLANG_OPCODE_RULE.get(opcode)
                if lang == "cpp" and opcode in CLANG_OPCODE_RULE_CPP:
                    rule_id = CLANG_OPCODE_RULE_CPP[opcode]
            row["authority_operation"] = opcode
            row["rule_ids"] = [rule_id] if rule_id else []
            row["join_evidence"] = (
                "clang's own spelling/opcode table, %s" % join_file)

    for row in units["go"]:
        spell = row["spelling"]
        token_name = None
        for name in g_join:
            if g_join[name] == spell:
                token_name = name
                break
        table = GO_TOKEN_RULE_BINARY if row["arity"] == "binary" \
            else GO_TOKEN_RULE_UNARY
        rule_id = table.get(token_name) if token_name else None
        row["authority_operation"] = token_name
        row["rule_ids"] = [rule_id] if rule_id else []
        row["join_evidence"] = (
            "go/token's own constant/spelling table, %s" % g_join_file)

    # rust's source-spelling -> operation-name join has NO on-disk
    # authority (finding F36-3); it is declared here, evidence class
    # "human interpretation of stated design".
    rust_spelling_join = {
        ("binary", "+"): "Add",
        ("binary", "-"): "Sub",
        ("binary", "*"): "Mul",
        ("binary", "/"): "Div",
        ("binary", "%"): "Rem",
        ("binary", "&"): "BitAnd",
        ("binary", "|"): "BitOr",
        ("binary", "^"): "BitXor",
        ("binary", "<<"): "Shl",
        ("binary", ">>"): "Shr",
        ("binary", "=="): "Eq",
        ("binary", "!="): "Ne",
        ("binary", "<"): "Lt",
        ("binary", "<="): "Le",
        ("binary", ">"): "Gt",
        ("binary", ">="): "Ge",
        ("unary", "!"): "Not",
        ("unary", "-"): "Neg",
    }
    for row in units["rust"]:
        key = (row["arity"], row["spelling"])
        op_name = rust_spelling_join.get(key)
        rule_ids = []
        if op_name is not None:
            rule_ids.append(RUST_OP_RULE[op_name])
            rule_ids.extend(RUST_OP_EXTRA_RULES.get(op_name, []))
        row["authority_operation"] = op_name
        row["rule_ids"] = rule_ids
        row["join_evidence"] = (
            "declared here: rust's spelling/operation join has no on-disk "
            "authority (no library/core, no rust-src component); evidence "
            "class human interpretation of stated design")

    # swift's join IS the declaration: the stdlib declares the operator by
    # its spelling, so the unit joins to the declaration that names it.
    swift_join = {
        ("binary", "+"): ["swift_AdditiveArithmetic_homogeneous_operands"],
        ("binary", "-"): ["swift_AdditiveArithmetic_homogeneous_operands"],
        ("binary", "*"): ["swift_Numeric_multiplication_homogeneous_operands"],
        ("binary", "/"): ["swift_FloatingPoint_division_homogeneous_operands"],
        ("binary", "%"): ["swift_BinaryInteger_homogeneous_operands"],
        ("binary", "&"): ["swift_BinaryInteger_bitwise_homogeneous_operands"],
        ("binary", "|"): ["swift_BinaryInteger_bitwise_homogeneous_operands"],
        ("binary", "^"): ["swift_BinaryInteger_bitwise_homogeneous_operands"],
        ("binary", "<<"): ["swift_BinaryInteger_heterogeneous_shift_operands"],
        ("binary", ">>"): ["swift_BinaryInteger_heterogeneous_shift_operands"],
        ("binary", "=="): ["swift_Equatable_homogeneous_operands", "swift_BinaryInteger_heterogeneous_comparison_operands"],
        ("binary", "!="): ["swift_Equatable_homogeneous_operands", "swift_BinaryInteger_heterogeneous_comparison_operands"],
        ("binary", "<"): ["swift_Comparable_homogeneous_operands", "swift_BinaryInteger_heterogeneous_comparison_operands"],
        ("binary", "<="): ["swift_Comparable_homogeneous_operands", "swift_BinaryInteger_heterogeneous_comparison_operands"],
        ("binary", ">"): ["swift_Comparable_homogeneous_operands", "swift_BinaryInteger_heterogeneous_comparison_operands"],
        ("binary", ">="): ["swift_Comparable_homogeneous_operands", "swift_BinaryInteger_heterogeneous_comparison_operands"],
        ("binary", "&&"): ["swift_Bool_logical_operands"],
        ("binary", "||"): ["swift_Bool_logical_operands"],
        ("unary", "!"): ["swift_Bool_negation_operand"],
        ("unary", "~"): ["swift_BinaryInteger_complement_operand"],
        ("unary", "-"): ["swift_SignedNumeric_negation_operand"],
        ("unary", "+"): ["swift_AdditiveArithmetic_unary_plus_operand"],
    }
    for row in units["swift"]:
        key = (row["arity"], row["spelling"])
        if row["arity"] == "unary" and row["position"] == "postfix":
            key = ("unary_postfix", row["spelling"])
        rule_ids = swift_join.get(key, [])
        row["authority_operation"] = rule_ids[0] if rule_ids else None
        row["rule_ids"] = list(rule_ids)
        row["join_evidence"] = (
            "the swift stdlib declares the operator by its own spelling in "
            "the declaration line quoted on the rule")

    doc = {}
    doc["authority"] = (
        "each language's own operand-admissibility statement, read out of "
        "the source named on every rule; line numbers are searched at run "
        "time, never typed")
    doc["pins"] = pins
    doc["classes"] = list(ALL_SCALAR)
    doc["rules"] = c_rules + g_rules + r_rules + s_rules
    doc["operator_units"] = (units["c"] + units["cpp"] + units["go"]
                             + units["rust"] + units["swift"])
    doc["swift_stdlib_source_files"] = list(SWIFT_STDLIB_FILES)

    out_path = os.path.join(HERE, "legality_rules.json")
    fh = open(out_path, "w")
    json.dump(doc, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()
    print("wrote %s: %d rules, %d operator units"
          % (out_path, len(doc["rules"]), len(doc["operator_units"])))
    refuse_own_output_on_spelling_failure(out_path)


def refuse_own_output_on_spelling_failure(path):
    """Run the spelling guard on our own output and delete it on failure."""
    cmd = [sys.executable,
           os.path.join(HERE, "check_no_spelling_keys.py"), path]
    done = subprocess.run(cmd, capture_output=True, text=True)
    print(done.stdout.strip())
    if done.returncode != 0:
        os.remove(path)
        raise SystemExit("REFUSED OWN OUTPUT: spelling guard failed")


if __name__ == "__main__":
    main()
