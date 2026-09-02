#!/usr/bin/env python3
"""operator_arity.py -- complete operator inventory per language, split by arity.

AUTHORITY
---------
Every row below is read out of a tree-sitter grammar source (`grammar.js`, or
`common/define-grammar.js` for the grammars that use the two-dialect pattern).
The grammar is a closed, human-written enumeration: an operator spelling can
only be parsed if some rule admits it as a literal token, so reading the rules
gives an inventory that is complete by construction for that grammar version.

Nothing here is filled in from memory or from language tutorials.  Each entry
records the rule that admits it, and `--verify` re-reads the grammar source and
checks that the spelling really does occur inside that rule (transitively
through helper rules and module-level const tables).

BUCKETS
-------
  unary_prefix     -x, !x, ~x, &x, *p, ++x, sizeof x
  unary_postfix    x++, x? (Rust), x! (Swift/TS), x!! (Kotlin)
  binary           arithmetic / comparison / bitwise / logical, plus the
                   two-operand keyword operators (`is`, `as`, `instanceof`,
                   `in`) and the two-operand range forms
  assignment       `=` and the compound stores (`+=`, ...).  These are binary
                   in shape but carry a store, so they are counted separately.
  ternary          c ? a : b  (and the language-specific spellings of it)
  structural       call, index, member access, slice, cast, spread, cascade --
                   the n-ary / fixed-shape operators

USAGE
-----
  python3 operator_arity.py                 # emit JSON + markdown from the table
  python3 operator_arity.py --fetch         # (re)download grammar sources to cache
  python3 operator_arity.py --verify        # check every spelling against the cache
  python3 operator_arity.py --census        # only print the census-coverage report

Outputs, written next to this script:
  operator_arity.json
  operator_arity.md

The grammar sources are cached in `grammar_cache/` next to this script so that
`--verify` is reproducible offline and the inventory is diffable when a grammar
version is bumped (the vendoring pattern named in
PseudoCoup_v6/Tools/ledgerer/tree_sitter/pins/MANIFEST.md).
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "grammar_cache")

BUCKETS = [
    "unary_prefix",
    "unary_postfix",
    "binary",
    "assignment",
    "ternary",
    "structural",
]

# --------------------------------------------------------------------------
# Grammar provenance.  `indent` is the column at which top-level rule keys sit
# in that file, which is all the slicer needs to cut a rule out of the source.
# --------------------------------------------------------------------------

GRAMMARS = OrderedDict([
    ("c.js", dict(owner="tree-sitter", repo="tree-sitter-c", ref="v0.24.2",
                  path="grammar.js", indent=4)),
    # tree-sitter-cpp v0.23.4 declares `tree-sitter-c: ^0.23.1`; grammar.js is
    # byte-identical between tree-sitter-c v0.23.6 and v0.24.2 (checked), so the
    # C base used by the C++ rows is the same text as the C rows.
    ("c_for_cpp.js", dict(owner="tree-sitter", repo="tree-sitter-c", ref="v0.23.6",
                          path="grammar.js", indent=4)),
    ("cpp.js", dict(owner="tree-sitter", repo="tree-sitter-cpp", ref="v0.23.4",
                    path="grammar.js", indent=4)),
    ("rust.js", dict(owner="tree-sitter", repo="tree-sitter-rust", ref="v0.24.2",
                     path="grammar.js", indent=4)),
    ("go.js", dict(owner="tree-sitter", repo="tree-sitter-go", ref="v0.25.0",
                   path="grammar.js", indent=4)),
    ("swift.js", dict(owner="alex-pinkus", repo="tree-sitter-swift", ref="0.7.3",
                      path="grammar.js", indent=4)),
    ("csharp.js", dict(owner="tree-sitter", repo="tree-sitter-c-sharp", ref="v0.23.5",
                       path="grammar.js", indent=4)),
    ("java.js", dict(owner="tree-sitter", repo="tree-sitter-java", ref="v0.23.5",
                     path="grammar.js", indent=4)),
    ("kotlin.js", dict(owner="fwcd", repo="tree-sitter-kotlin", ref="0.3.8",
                       path="grammar.js", indent=4)),
    # tree-sitter-dart publishes no release tags; pinned to an exact commit.
    ("dart.js", dict(owner="UserNobody14", repo="tree-sitter-dart",
                     ref="be07cf7118d3dba06236a3f19541685a68209934",
                     path="grammar.js", indent=8)),
    ("javascript.js", dict(owner="tree-sitter", repo="tree-sitter-javascript", ref="v0.23.1",
                           path="grammar.js", indent=4)),
    ("typescript.js", dict(owner="tree-sitter", repo="tree-sitter-typescript", ref="v0.23.2",
                           path="common/define-grammar.js", indent=6)),
    ("php.js", dict(owner="tree-sitter", repo="tree-sitter-php", ref="v0.24.2",
                    path="common/define-grammar.js", indent=6)),
    ("python.js", dict(owner="tree-sitter", repo="tree-sitter-python", ref="v0.25.0",
                       path="grammar.js", indent=4)),
    ("ruby.js", dict(owner="tree-sitter", repo="tree-sitter-ruby", ref="v0.23.1",
                     path="grammar.js", indent=4)),
])

# Which grammar files back each language row, in the order they are consulted.
LANG_FILES = {
    "c":          ["c.js"],
    "cpp":        ["cpp.js", "c_for_cpp.js"],
    "rust":       ["rust.js"],
    "go":         ["go.js"],
    "swift":      ["swift.js"],
    "csharp":     ["csharp.js"],
    "java":       ["java.js"],
    "kotlin":     ["kotlin.js"],
    "dart":       ["dart.js"],
    "typescript": ["typescript.js", "javascript.js"],
    "php":        ["php.js"],
    "python":     ["python.js"],
    "ruby":       ["ruby.js"],
}

LANG_ORDER = ["cpp", "rust", "go", "swift",
              "c", "csharp", "java", "kotlin", "dart", "typescript",
              "php", "python", "ruby"]


def is_open_set(op):
    """`<custom_operator>` / `<simple_identifier>` are placeholders for rules
    that admit an unbounded set of spellings, not operators themselves.  The
    pattern is deliberately narrow: `<`, `<=`, `<<` and `<=>` are real
    operators and must not be swallowed."""
    return re.fullmatch(r"<[a-z_]+>", op) is not None


def G(rule, file, ops, note=None, verify="literal"):
    """One fact: `ops` are admitted by `rule` in grammar file `file`."""
    return dict(rule=rule, file=file, ops=list(ops), note=note, verify=verify)


# --------------------------------------------------------------------------
# The inventory.
# --------------------------------------------------------------------------

FACTS = {

    # ---------------------------------------------------------------- C ----
    "c": {
        "unary_prefix": [
            G("unary_expression", "c.js", ["!", "~", "-", "+"]),
            G("pointer_expression", "c.js", ["*", "&"]),
            G("update_expression", "c.js", ["++", "--"],
              note="prefix arm of the choice(seq(op, arg), seq(arg, op))"),
            G("sizeof_expression", "c.js", ["sizeof"]),
            G("alignof_expression", "c.js",
              ["__alignof__", "__alignof", "_alignof", "alignof", "_Alignof"]),
            G("extension_expression", "c.js", ["__extension__"],
              note="GNU extension marker"),
        ],
        "unary_postfix": [
            G("update_expression", "c.js", ["++", "--"], note="postfix arm"),
        ],
        "binary": [
            G("binary_expression", "c.js",
              ["+", "-", "*", "/", "%", "||", "&&", "|", "^", "&",
               "==", "!=", ">", ">=", "<=", "<", "<<", ">>"]),
        ],
        "assignment": [
            G("assignment_expression", "c.js",
              ["=", "*=", "/=", "%=", "+=", "-=", "<<=", ">>=", "&=", "^=", "|="]),
        ],
        "ternary": [
            G("conditional_expression", "c.js", ["?:"], verify="shape",
              note="seq(condition, '?', optional(consequence), ':', alternative); "
                   "the optional consequence also admits the GNU `a ?: b`"),
        ],
        "structural": [
            G("call_expression", "c.js", ["f(...)"], verify="shape"),
            G("subscript_expression", "c.js", ["a[i]"], verify="shape"),
            G("field_expression", "c.js", [".", "->"]),
            G("cast_expression", "c.js", ["(T)x"], verify="shape"),
            G("compound_literal_expression", "c.js", ["(T){...}"], verify="shape"),
            G("comma_expression", "c.js", [","]),
            G("generic_expression", "c.js", ["_Generic"]),
            G("offsetof_expression", "c.js", ["offsetof"]),
        ],
    },

    # -------------------------------------------------------------- C++ ----
    "cpp": {
        "unary_prefix": [
            G("unary_expression", "c_for_cpp.js", ["!", "~", "-", "+"],
              note="inherited from the C base grammar"),
            G("unary_expression", "cpp.js", ["not", "compl"],
              note="C++ override adds the alternative-token spellings"),
            G("pointer_expression", "c_for_cpp.js", ["*", "&"]),
            G("update_expression", "c_for_cpp.js", ["++", "--"], note="prefix arm"),
            G("sizeof_expression", "c_for_cpp.js", ["sizeof"],
              note="the C++ override widens it: `($, original) => choice("
                   "original, seq('sizeof','...','(',identifier,')'))`, adding "
                   "`sizeof...(pack)`"),
            G("co_await_expression", "cpp.js", ["co_await"]),
            G("new_expression", "cpp.js", ["new"]),
            G("delete_expression", "cpp.js", ["delete"]),
        ],
        "unary_postfix": [
            G("update_expression", "c_for_cpp.js", ["++", "--"], note="postfix arm"),
            G("parameter_pack_expansion", "cpp.js", ["..."]),
        ],
        "binary": [
            G("binary_expression", "c_for_cpp.js",
              ["+", "-", "*", "/", "%", "||", "&&", "|", "^", "&",
               "==", "!=", ">", ">=", "<=", "<", "<<", ">>"],
              note="reached through `original` in the C++ override"),
            G("binary_expression", "cpp.js",
              ["<=>", "or", "and", "bitor", "xor", "bitand", "not_eq"],
              note="C++ adds three-way comparison and the alternative tokens"),
        ],
        "assignment": [
            G("assignment_expression", "cpp.js",
              ["=", "*=", "/=", "%=", "+=", "-=", "<<=", ">>=", "&=", "^=", "|=",
               "and_eq", "or_eq", "xor_eq"],
              note="ASSIGNMENT_OPERATORS module const"),
        ],
        "ternary": [
            G("conditional_expression", "c_for_cpp.js", ["?:"], verify="shape"),
        ],
        "structural": [
            G("call_expression", "c_for_cpp.js", ["f(...)"], verify="shape"),
            G("subscript_expression", "cpp.js", ["a[i]"], verify="shape",
              note="C++ widens the index to a subscript_argument_list (a[i, j])"),
            G("field_expression", "cpp.js", [".", ".*", "->"]),
            G("cast_expression", "c_for_cpp.js", ["(T)x"], verify="shape"),
            G("comma_expression", "c_for_cpp.js", [","]),
            G("fold_expression", "cpp.js", ["(pack op ...)"], verify="shape",
              note="_unary_left_fold / _unary_right_fold / _binary_fold over "
                   "FOLD_OPERATORS"),
        ],
        "annex": [
            G("_fold_operator", "cpp.js",
              ["+", "-", "*", "/", "%", "^", "&", "|", "=", "<", ">", "<<", ">>",
               "+=", "-=", "*=", "/=", "%=", "^=", "&=", "|=", ">>=", "<<=",
               "==", "!=", "<=", ">=", "&&", "||", ",", ".*", "->*",
               "or", "and", "bitor", "xor", "bitand", "not_eq"],
              note="the FOLD_OPERATORS table -- the operators that may appear "
                   "inside a C++17 fold, not standalone expression operators"),
            G("operator_name", "cpp.js",
              ["co_await", "+", "-", "*", "/", "%", "^", "&", "|", "~", "!", "=",
               "<", ">", "+=", "-=", "*=", "/=", "%=", "^=", "&=", "|=",
               "<<", ">>", ">>=", "<<=", "==", "!=", "<=", ">=", "<=>",
               "&&", "||", "++", "--", ",", "->*", "->", "()", "[]",
               "xor", "bitand", "bitor", "compl", "not", "xor_eq", "and_eq",
               "or_eq", "not_eq", "and", "or"],
              note="the spellings that may follow the `operator` keyword in an "
                   "overload declarator -- a declaration-side inventory, not an "
                   "expression-side one. `->*` appears HERE and in the fold "
                   "table but in NO expression rule of tree-sitter-cpp v0.23.4, "
                   "so `a->*p` has no dedicated node kind in this grammar."),
        ],
    },

    # ------------------------------------------------------------- Rust ----
    "rust": {
        "unary_prefix": [
            G("unary_expression", "rust.js", ["-", "*", "!"]),
            G("reference_expression", "rust.js", ["&"]),
            G("reference_expression", "rust.js", ["&raw const", "&raw mut"],
              verify="shape",
              note="seq('&', choice(seq('raw', choice('const', mutable_specifier)), "
                   "optional(mutable_specifier)), value) -- the raw-reference "
                   "forms are assembled from separate tokens"),
            G("range_expression", "rust.js", ["..", "..="], verify="derived",
              note="prefix arm seq(choice('..','...','..='), expr) -- the "
                   "grammar writes the choice once and reuses it in three arms"),
        ],
        "unary_postfix": [
            G("try_expression", "rust.js", ["?"]),
            G("range_expression", "rust.js", [".."], note="postfix arm seq(expr, '..')"),
            G("await_expression", "rust.js", [".await"], verify="shape",
              note="prec(PREC.field, seq(expr, '.', 'await')) -- two tokens"),
        ],
        "binary": [
            G("binary_expression", "rust.js",
              ["&&", "||", "&", "|", "^", "==", "!=", "<", "<=", ">", ">=",
               "<<", ">>", "+", "-", "*", "/", "%"]),
            G("range_expression", "rust.js", ["..", "...", "..="],
              note="two-operand arm seq(expr, choice('..','...','..='), expr)"),
            G("type_cast_expression", "rust.js", ["as"]),
        ],
        "assignment": [
            G("assignment_expression", "rust.js", ["="]),
            G("compound_assignment_expr", "rust.js",
              ["+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>="]),
        ],
        "ternary": [],
        "structural": [
            G("call_expression", "rust.js", ["f(...)"], verify="shape"),
            G("index_expression", "rust.js", ["a[i]"], verify="shape"),
            G("field_expression", "rust.js", ["."]),
            G("macro_invocation", "rust.js", ["!"], note="m!(...) -- macro call"),
            G("scoped_identifier", "rust.js", ["::"]),
            G("generic_function", "rust.js", ["::<>"], verify="shape",
              note="turbofish"),
            G("closure_expression", "rust.js", ["|...|"], verify="shape",
              note="closure parameter list, delimited by '|'"),
        ],
    },

    # --------------------------------------------------------------- Go ----
    "go": {
        "unary_prefix": [
            G("unary_expression", "go.js", ["+", "-", "!", "^", "*", "&", "<-"]),
        ],
        "unary_postfix": [
            G("inc_statement", "go.js", ["++"]),
            G("dec_statement", "go.js", ["--"]),
            G("variadic_argument", "go.js", ["..."]),
        ],
        "binary": [
            G("binary_expression", "go.js",
              ["*", "/", "%", "<<", ">>", "&", "&^",
               "+", "-", "|", "^",
               "==", "!=", "<", "<=", ">", ">=",
               "&&", "||"],
              verify="derived",
              note="table over the module consts multiplicativeOperators, "
                   "additiveOperators, comparativeOperators plus '&&' and '||'"),
        ],
        "assignment": [
            G("assignment_statement", "go.js",
              ["*=", "/=", "%=", "<<=", ">>=", "&=", "&^=",
               "+=", "-=", "|=", "^=", "="],
              verify="computed",
              note="assignmentOperators = multiplicative.concat(additive)"
                   ".map(o => o + '=').concat('=') -- built by string "
                   "concatenation, so the compound spellings never appear as "
                   "literals in the source"),
            G("short_var_declaration", "go.js", [":="],
              note="declare-and-store"),
            G("send_statement", "go.js", ["<-"], note="channel send; a store"),
        ],
        "ternary": [],
        "structural": [
            G("call_expression", "go.js", ["f(...)"], verify="shape"),
            G("index_expression", "go.js", ["a[i]"], verify="shape"),
            G("slice_expression", "go.js", ["a[i:j]", "a[i:j:k]"], verify="shape"),
            G("selector_expression", "go.js", ["."]),
            G("type_assertion_expression", "go.js", ["x.(T)"], verify="shape"),
            G("type_conversion_expression", "go.js", ["T(x)"], verify="shape"),
            G("type_instantiation_expression", "go.js", ["T[A]"], verify="shape",
              note="generic instantiation"),
        ],
    },

    # ------------------------------------------------------------ Swift ----
    "swift": {
        "unary_prefix": [
            G("_prefix_unary_operator", "swift.js",
              ["++", "--", "-", "+", "!", "&", "~", "."],
              verify="derived",
              note="'!' arrives as $.bang and '.' as $._dot, both external "
                   "scanner tokens aliased back to their text form"),
            G("_prefix_unary_operator", "swift.js", ["<custom_operator>"],
              verify="shape",
              note="OPEN SET: $.custom_operator is a scanner-produced token, so "
                   "user-defined prefix operators are admitted without being "
                   "enumerated"),
            G("try_operator", "swift.js", ["try", "try?", "try!"], verify="derived",
              note="seq('try', choice(optional($._try_operator_type), ...)) where "
                   "_try_operator_type is token.immediate('!')|token.immediate('?')"),
            G("await_expression", "swift.js", ["await"]),
            G("consume_expression", "swift.js", ["consume"]),
            G("open_start_range_expression", "swift.js", ["..<", "..."],
              verify="derived", note="_range_operator in prefix position"),
        ],
        "unary_postfix": [
            G("_postfix_unary_operator", "swift.js", ["++", "--", "!"],
              verify="derived", note="'!' is $.bang, an external scanner token"),
            G("_expression", "swift.js", ["?"], verify="derived",
              note="seq($._expression, alias($._immediate_quest, '?')) -- optional "
                   "unwrap/chain suffix"),
            G("open_end_range_expression", "swift.js", ["..."], verify="derived"),
        ],
        "binary": [
            G("_multiplicative_operator", "swift.js", ["*", "/", "%"]),
            G("_additive_operator", "swift.js", ["+", "-"]),
            G("_comparison_operator", "swift.js", ["<", ">", "<=", ">="]),
            G("_equality_operator", "swift.js", ["!=", "!==", "==", "==="],
              verify="derived", note="'==' arrives as $._eq_eq (scanner token)"),
            G("_bitwise_binary_operator", "swift.js", ["&", "|", "^", "<<", ">>"]),
            G("_conjunction_operator", "swift.js", ["&&"]),
            G("_disjunction_operator", "swift.js", ["||"]),
            G("_nil_coalescing_operator", "swift.js", ["??"]),
            G("_range_operator", "swift.js", ["..<", "..."], verify="derived"),
            G("check_expression", "swift.js", ["is"], verify="derived",
              note="$._is_operator"),
            G("as_operator", "swift.js", ["as", "as?", "as!"], verify="derived",
              note="choice($._as, $._as_quest, $._as_bang), scanner tokens "
                   "aliased to 'as' / 'as?' / 'as!'"),
            G("infix_expression", "swift.js", ["<custom_operator>"], verify="shape",
              note="OPEN SET: seq(lhs, $.custom_operator, rhs). Swift's overflow "
                   "operators &+ &- &* and every user-defined infix operator go "
                   "through here; the grammar does NOT enumerate them."),
        ],
        "assignment": [
            G("_assignment_and_operator", "swift.js",
              ["+=", "-=", "*=", "/=", "%=", "="], verify="derived",
              note="'=' arrives as $._equal_sign -> alias($._eq_custom, '='). "
                   "NOTE the grammar admits no &=, |=, ^=, <<=, >>=, &&=, ||=, ??="),
        ],
        "ternary": [
            G("ternary_expression", "swift.js", ["?:"], verify="shape",
              note="seq(condition, $._quest, if_true, ':', if_false)"),
        ],
        "structural": [
            G("value_arguments", "swift.js", ["f(...)", "a[i]"], verify="shape",
              note="one rule covers both paren call arguments and bracket "
                   "subscript arguments"),
            G("navigation_suffix", "swift.js", ["."], verify="derived",
              note="$._dot, scanner token aliased to '.'"),
            G("key_path_expression", "swift.js", ["\\\\."], verify="shape"),
            G("selector_expression", "swift.js", ["#selector(...)"], verify="shape"),
        ],
    },

    # --------------------------------------------------------------- C# ----
    "csharp": {
        "unary_prefix": [
            G("prefix_unary_expression", "csharp.js",
              ["++", "--", "+", "-", "!", "~", "&", "^"],
              note="'^' here is the index-from-end operator ^1"),
            G("_pointer_indirection_expression", "csharp.js", ["*"]),
            G("await_expression", "csharp.js", ["await"]),
        ],
        "unary_postfix": [
            G("postfix_unary_expression", "csharp.js", ["++", "--", "!"],
              note="'!' is the null-forgiving operator"),
        ],
        "binary": [
            G("binary_expression", "csharp.js",
              ["&&", "||", ">>", ">>>", "<<", "&", "^", "|", "+", "-", "*", "/",
               "%", "<", "<=", "==", "!=", ">=", ">", "??"]),
            G("as_expression", "csharp.js", ["as"]),
            G("is_expression", "csharp.js", ["is"]),
            G("range_expression", "csharp.js", [".."]),
            G("with_expression", "csharp.js", ["with"]),
        ],
        "assignment": [
            G("assignment_expression", "csharp.js",
              ["=", "+=", "-=", "*=", "/=", "%=", "&=", "^=", "|=",
               "<<=", ">>=", ">>>=", "??="]),
        ],
        "ternary": [
            G("conditional_expression", "csharp.js", ["?:"], verify="shape"),
        ],
        "structural": [
            G("invocation_expression", "csharp.js", ["f(...)"], verify="shape"),
            G("element_access_expression", "csharp.js", ["a[i]"], verify="shape"),
            G("member_access_expression", "csharp.js", [".", "->"]),
            G("conditional_access_expression", "csharp.js", ["?.", "?["],
              verify="shape",
              note="seq(expr, '?', choice(member_binding_expression, "
                   "element_binding_expression))"),
            G("cast_expression", "csharp.js", ["(T)x"], verify="shape"),
            G("switch_expression", "csharp.js", ["switch"]),
            G("sizeof_expression", "csharp.js", ["sizeof"]),
            G("default_expression", "csharp.js", ["default"]),
        ],
    },

    # ------------------------------------------------------------- Java ----
    "java": {
        "unary_prefix": [
            G("unary_expression", "java.js", ["+", "-", "!", "~"]),
            G("update_expression", "java.js", ["++", "--"], note="prefix arms"),
        ],
        "unary_postfix": [
            G("update_expression", "java.js", ["++", "--"], note="postfix arms"),
        ],
        "binary": [
            G("binary_expression", "java.js",
              [">", "<", ">=", "<=", "==", "!=", "&&", "||", "+", "-", "*", "/",
               "&", "|", "^", "%", "<<", ">>", ">>>"]),
            G("instanceof_expression", "java.js", ["instanceof"]),
        ],
        "assignment": [
            G("assignment_expression", "java.js",
              ["=", "+=", "-=", "*=", "/=", "&=", "|=", "^=", "%=",
               "<<=", ">>=", ">>>="]),
        ],
        "ternary": [
            G("ternary_expression", "java.js", ["?:"], verify="shape"),
        ],
        "structural": [
            G("method_invocation", "java.js", ["f(...)"], verify="shape"),
            G("array_access", "java.js", ["a[i]"], verify="shape"),
            G("field_access", "java.js", ["."]),
            G("cast_expression", "java.js", ["(T)x"], verify="shape"),
            G("method_reference", "java.js", ["::"]),
            G("lambda_expression", "java.js", ["->"]),
            G("object_creation_expression", "java.js", ["new"], verify="derived",
              note="literal 'new' sits in _unqualified_object_creation_expression"),
            G("switch_expression", "java.js", ["switch"]),
        ],
    },

    # ----------------------------------------------------------- Kotlin ----
    "kotlin": {
        "unary_prefix": [
            G("_prefix_unary_operator", "kotlin.js", ["++", "--", "-", "+", "!"]),
            G("spread_expression", "kotlin.js", ["*"]),
        ],
        "unary_postfix": [
            G("_postfix_unary_operator", "kotlin.js", ["++", "--", "!!"]),
        ],
        "binary": [
            G("_multiplicative_operator", "kotlin.js", ["*", "/", "%"]),
            G("_additive_operator", "kotlin.js", ["+", "-"]),
            G("_comparison_operator", "kotlin.js", ["<", ">", "<=", ">="]),
            G("_equality_operator", "kotlin.js", ["!=", "!==", "==", "==="]),
            G("conjunction_expression", "kotlin.js", ["&&"]),
            G("disjunction_expression", "kotlin.js", ["||"]),
            G("elvis_expression", "kotlin.js", ["?:"],
              note="binary elvis, NOT a ternary"),
            G("range_expression", "kotlin.js", [".."]),
            G("_in_operator", "kotlin.js", ["in", "!in"]),
            G("_is_operator", "kotlin.js", ["is", "!is"]),
            G("_as_operator", "kotlin.js", ["as", "as?"]),
            G("infix_expression", "kotlin.js", ["<simple_identifier>"], verify="shape",
              note="OPEN SET: seq(lhs, $.simple_identifier, rhs). Kotlin's bitwise "
                   "operations (and, or, xor, shl, shr, ushr, inv) are infix "
                   "FUNCTIONS and reach the tree through here -- the grammar "
                   "enumerates no bitwise operator tokens at all."),
        ],
        "assignment": [
            G("_assignment_and_operator", "kotlin.js", ["+=", "-=", "*=", "/=", "%="]),
            G("assignment", "kotlin.js", ["="]),
        ],
        "ternary": [],
        "structural": [
            G("call_suffix", "kotlin.js", ["f(...)"], verify="shape"),
            G("_indexing_suffix", "kotlin.js", ["a[i]"], verify="shape"),
            G("_member_access_operator", "kotlin.js", [".", "::", "?."],
              verify="derived", note="'?.' is alias($.safe_nav, '?.')"),
        ],
    },

    # ------------------------------------------------------------- Dart ----
    "dart": {
        "unary_prefix": [
            G("prefix_operator", "dart.js", ["-", "!", "~"], verify="derived",
              note="choice(minus_operator, negation_operator, tilde_operator)"),
            G("increment_operator", "dart.js", ["++", "--"],
              note="prefix arm of unary_expression"),
            G("await_expression", "dart.js", ["await"]),
            G("throw_expression", "dart.js", ["throw"]),
            G("spread_element", "dart.js", ["..."]),
            G("spread_element", "dart.js", ["...?"], verify="shape",
              note="seq('...', optional('?'), expr) -- two tokens"),
        ],
        "unary_postfix": [
            G("postfix_operator", "dart.js", ["++", "--"],
              note="postfix_operator => $.increment_operator"),
            G("_exclamation_operator", "dart.js", ["!"],
              note="null assertion, reached through `selector`"),
        ],
        "binary": [
            G("_multiplicative_operator", "dart.js", ["*", "/", "%", "~/"]),
            G("_additive_operator", "dart.js", ["+", "-"]),
            G("_shift_operator", "dart.js", ["<<", ">>", ">>>"]),
            G("_bitwise_operator", "dart.js", ["&", "^", "|"]),
            G("relational_operator", "dart.js", ["<", ">", "<=", ">="]),
            G("equality_operator", "dart.js", ["==", "!="]),
            G("logical_and_operator", "dart.js", ["&&"]),
            G("logical_or_operator", "dart.js", ["||"]),
            G("_if_null_expression", "dart.js", ["??"]),
            G("is_operator", "dart.js", ["is"]),
            G("is_operator", "dart.js", ["is!"], verify="shape",
              note="seq(token('is'), optional($._exclamation_operator)) -- "
                   "two tokens"),
            G("as_operator", "dart.js", ["as"]),
        ],
        "assignment": [
            G("_assignment_operator", "dart.js",
              ["=", "+=", "-=", "*=", "/=", "%=", "~/=", "<<=", ">>=", ">>>=",
               "&=", "^=", "|=", "??="]),
        ],
        "ternary": [
            G("conditional_expression", "dart.js", ["?:"], verify="shape"),
        ],
        "structural": [
            G("argument_part", "dart.js", ["f(...)"], verify="shape"),
            G("index_selector", "dart.js", ["a[i]"], verify="shape"),
            G("unconditional_assignable_selector", "dart.js", ["."]),
            G("conditional_assignable_selector", "dart.js", ["?."]),
            G("conditional_assignable_selector", "dart.js", ["?["],
              verify="shape",
              note="seq('?', $.index_selector) -- assembled from '?' and '['"),
            G("cascade_section", "dart.js", ["..", "?.."]),
            G("type_cast", "dart.js", ["as"], verify="derived"),
        ],
    },

    # ------------------------------------------------------- TypeScript ----
    "typescript": {
        "unary_prefix": [
            G("unary_expression", "javascript.js",
              ["!", "~", "-", "+", "typeof", "void", "delete"]),
            G("update_expression", "javascript.js", ["++", "--"], note="prefix arms"),
            G("await_expression", "javascript.js", ["await"]),
            G("new_expression", "javascript.js", ["new"]),
            G("spread_element", "javascript.js", ["..."]),
            G("type_assertion", "typescript.js", ["<T>x"], verify="shape",
              note="seq($.type_arguments, $.expression) -- the angle-bracket cast"),
        ],
        "unary_postfix": [
            G("update_expression", "javascript.js", ["++", "--"], note="postfix arms"),
            G("non_null_expression", "typescript.js", ["!"]),
        ],
        "binary": [
            G("binary_expression", "javascript.js",
              ["&&", "||", ">>", ">>>", "<<", "&", "^", "|", "+", "-", "*", "/",
               "%", "**", "<", "<=", "==", "===", "!=", "!==", ">=", ">", "??",
               "instanceof", "in"]),
            G("as_expression", "typescript.js", ["as"]),
            G("satisfies_expression", "typescript.js", ["satisfies"]),
        ],
        "assignment": [
            G("assignment_expression", "javascript.js", ["="]),
            G("augmented_assignment_expression", "javascript.js",
              ["+=", "-=", "*=", "/=", "%=", "^=", "&=", "|=", ">>=", ">>>=",
               "<<=", "**=", "&&=", "||=", "??="]),
        ],
        "ternary": [
            G("ternary_expression", "javascript.js", ["?:"], verify="shape",
              note="seq(condition, alias($._ternary_qmark, '?'), consequence, "
                   "':', alternative)"),
        ],
        "structural": [
            G("call_expression", "typescript.js", ["f(...)", "?.()"], verify="shape",
              note="TS override adds optional type_arguments to the call"),
            G("subscript_expression", "javascript.js", ["a[i]"], verify="shape"),
            G("member_expression", "javascript.js", ["."]),
            G("optional_chain", "javascript.js", ["?."]),
            G("instantiation_expression", "typescript.js", ["f<T>"], verify="shape"),
            G("sequence_expression", "javascript.js", [","], verify="shape",
              note="prec.right(commaSep1($.expression))"),
        ],
    },

    # -------------------------------------------------------------- PHP ----
    "php": {
        "unary_prefix": [
            G("unary_op_expression", "php.js", ["+", "-", "~", "!"]),
            G("update_expression", "php.js", ["++", "--"], note="prefix arm"),
            G("error_suppression_expression", "php.js", ["@"]),
            G("clone_expression", "php.js", ["clone"]),
            G("print_intrinsic", "php.js", ["print"]),
            G("include_expression", "php.js", ["include"]),
            G("include_once_expression", "php.js", ["include_once"]),
            G("require_expression", "php.js", ["require"]),
            G("require_once_expression", "php.js", ["require_once"]),
            G("yield_expression", "php.js", ["yield", "yield from"]),
            G("variadic_unpacking", "php.js", ["..."]),
        ],
        "unary_postfix": [
            G("update_expression", "php.js", ["++", "--"], note="postfix arm"),
        ],
        "binary": [
            G("binary_expression", "php.js",
              ["instanceof", "??", "**", "and", "or", "xor", "||", "&&", "|", "^",
               "&", "==", "!=", "<>", "===", "!==", "<", ">", "<=", ">=", "<=>",
               "|>", ".", "<<", ">>", "+", "-", "*", "/", "%"],
              note="'|>' is the PHP 8.5 pipe operator; '.' is string concatenation"),
        ],
        "assignment": [
            G("assignment_expression", "php.js", ["="]),
            G("reference_assignment_expression", "php.js", ["=&"], verify="shape",
              note="seq(left, '=', '&', right) -- two tokens"),
            G("augmented_assignment_expression", "php.js",
              ["**=", "*=", "/=", "%=", "+=", "-=", ".=", "<<=", ">>=",
               "&=", "^=", "|=", "??="]),
        ],
        "ternary": [
            G("conditional_expression", "php.js", ["?:"], verify="shape",
              note="seq(condition, '?', optional(body), ':', alternative) -- the "
                   "optional body is the short ternary `a ?: b`"),
        ],
        "structural": [
            G("function_call_expression", "php.js", ["f(...)"], verify="shape"),
            G("_dereferencable_subscript_expression", "php.js", ["a[i]"],
              verify="shape", note="aliased to `subscript_expression`"),
            G("member_access_expression", "php.js", ["->"]),
            G("nullsafe_member_access_expression", "php.js", ["?->"]),
            G("class_constant_access_expression", "php.js", ["::"]),
            G("cast_expression", "php.js", ["(int)x"], verify="shape",
              note="cast_type enumerates array/binary/bool/boolean/double/float/"
                   "int/integer/object/real/string/unset"),
            G("match_expression", "php.js", ["match"]),
        ],
    },

    # ----------------------------------------------------------- Python ----
    "python": {
        "unary_prefix": [
            G("unary_operator", "python.js", ["+", "-", "~"]),
            G("not_operator", "python.js", ["not"]),
            G("await", "python.js", ["await"]),
            G("list_splat", "python.js", ["*"]),
            G("dictionary_splat", "python.js", ["**"]),
            G("lambda", "python.js", ["lambda"]),
        ],
        "unary_postfix": [],
        "binary": [
            G("binary_operator", "python.js",
              ["+", "-", "*", "@", "/", "%", "//", "**", "|", "&", "^", "<<", ">>"],
              note="'@' is matrix multiplication"),
            G("boolean_operator", "python.js", ["and", "or"]),
            G("comparison_operator", "python.js",
              ["<", "<=", "==", "!=", ">=", ">", "<>", "in", "not in", "is", "is not"],
              note="'<>' is the Python-2 inequality; 'not in'/'is not' arrive as "
                   "aliased hidden tokens"),
            G("as_pattern", "python.js", ["as"]),
        ],
        "assignment": [
            G("assignment", "python.js", ["="],
              note="seq(left, choice(seq('=', right), seq(':', type), "
                   "seq(':', type, '=', right))) -- the ':' arm is the annotated "
                   "form"),
            G("augmented_assignment", "python.js",
              ["+=", "-=", "*=", "/=", "@=", "//=", "%=", "**=",
               ">>=", "<<=", "&=", "^=", "|="]),
            G("named_expression", "python.js", [":="], note="walrus"),
        ],
        "ternary": [
            G("conditional_expression", "python.js", ["if-else"], verify="shape",
              note="seq(expression, 'if', expression, 'else', expression) -- "
                   "Python spells its ternary with keywords, not ?:"),
        ],
        "structural": [
            G("call", "python.js", ["f(...)"], verify="shape"),
            G("subscript", "python.js", ["a[i]"], verify="shape"),
            G("attribute", "python.js", ["."]),
            G("slice", "python.js", ["a[i:j]", "a[i:j:k]"], verify="shape",
              note="seq(optional(expr), ':', optional(expr), "
                   "optional(seq(':', optional(expr))))"),
        ],
    },

    # ------------------------------------------------------------- Ruby ----
    "ruby": {
        "unary_prefix": [
            G("unary", "ruby.js", ["defined?", "not", "-", "+", "!", "~"],
              verify="derived", note="'-' arrives as _unary_minus / _binary_minus "
                                     "aliased back to '-'"),
            G("command_unary", "ruby.js", ["defined?", "not", "-", "+", "!", "~"],
              verify="derived", note="same operator set in command (paren-less) "
                                     "position"),
            G("splat_argument", "ruby.js", ["*"], verify="derived",
              note="alias($._splat_star, '*')"),
            G("hash_splat_argument", "ruby.js", ["**"], verify="derived"),
            G("block_argument", "ruby.js", ["&"], verify="derived"),
        ],
        "unary_postfix": [],
        "binary": [
            G("binary", "ruby.js",
              ["and", "or", "||", "&&", "<<", ">>", "<", "<=", ">", ">=", "&",
               "^", "|", "+", "-", "/", "%", "*", "==", "!=", "===", "<=>",
               "=~", "!~", "**"],
              verify="derived",
              note="'-', '*', '**' arrive as _binary_minus / _binary_star / "
                   "_binary_star_star aliased back to their text form"),
            G("range", "ruby.js", ["..", "..."]),
        ],
        "assignment": [
            G("assignment", "ruby.js", ["="]),
            G("operator_assignment", "ruby.js",
              ["+=", "-=", "*=", "**=", "/=", "||=", "|=", "&&=", "&=", "%=",
               ">>=", "<<=", "^="]),
            G("command_operator_assignment", "ruby.js",
              ["+=", "-=", "*=", "**=", "/=", "||=", "|=", "&&=", "&=", "%=",
               ">>=", "<<=", "^="], note="command (paren-less) position"),
        ],
        "ternary": [
            G("conditional", "ruby.js", ["?:"], verify="shape"),
        ],
        "structural": [
            G("call", "ruby.js", ["f(...)"], verify="shape"),
            G("_call_operator", "ruby.js", [".", "&.", "::"], verify="derived",
              note="choice('.', '&.', token.immediate('::'))"),
            G("element_reference", "ruby.js", ["a[i]"], verify="shape",
              note="alias($._element_reference_bracket, '[')"),
        ],
        "annex": [
            G("operator", "ruby.js",
              ["..", "|", "^", "&", "<=>", "==", "===", "=~", ">", ">=", "<", "<=",
               "+", "!=", "-", "*", "/", "%", "!", "!~", "**", "<<", ">>", "~",
               "+@", "-@", "~@", "[]", "[]=", "`"],
              note="the spellings that may be DEFINED as a method name "
                   "(`def <op>`) -- a declaration-side inventory, not an "
                   "expression-side one. `+@`/`-@`/`~@` are the unary forms and "
                   "`[]`/`[]=` the index read/write forms."),
        ],
    },
}


# --------------------------------------------------------------------------
# Operators with no counterpart elsewhere in the line.
# --------------------------------------------------------------------------

DISTINCTIVE = {
    "go": {"&^": "bit clear (AND NOT); also &^= in the assignment set",
           ":=": "declare-and-store",
           "<-": "channel receive (prefix) and channel send (statement)"},
    "cpp": {"<=>": "three-way comparison",
            ".*": "member-through-object-pointer",
            "and/or/xor/bitand/bitor/compl/not/not_eq/and_eq/or_eq/xor_eq":
                "alternative tokens for the punctuation operators",
            "co_await": "coroutine await"},
    "rust": {"..": "range (prefix, infix and postfix forms)",
             "..=": "inclusive range",
             "?": "postfix try",
             ".await": "postfix await",
             "&raw const / &raw mut": "raw reference"},
    "swift": {"..<": "half-open range",
              "as? / as!": "conditional and forced cast",
              "try? / try!": "optional and forced try",
              "??": "nil coalescing"},
    "php": {"<=>": "spaceship comparison",
            "??": "null coalescing; also ??=",
            "?->": "nullsafe member access",
            "|>": "pipe (PHP 8.5)",
            "<>": "legacy inequality",
            "@": "error suppression",
            ".": "string concatenation (binary), also .="},
    "dart": {"??": "if-null; also ??=",
             "?.": "conditional member access",
             "..": "cascade; '?..' is the null-aware cascade",
             "~/": "truncating division; also ~/=",
             "...?": "null-aware spread",
             "!": "postfix null assertion"},
    "kotlin": {"?:": "elvis (BINARY, not a ternary)",
               "!!": "postfix not-null assertion",
               "as?": "safe cast",
               "!in / !is": "negated containment / type test",
               "?.": "safe navigation"},
    "csharp": {">>>": "unsigned right shift; also >>>=",
               "??=": "null-coalescing assignment",
               "^": "index-from-end in prefix position",
               "?.": "null-conditional access",
               "..": "range",
               "with": "record copy-and-update"},
    "python": {"//": "floor division; also //=",
               "@": "matrix multiplication; also @=",
               ":=": "walrus",
               "<>": "Python-2 inequality, still admitted by the grammar",
               "if-else": "the ternary, spelled with keywords"},
    "ruby": {"=~": "regexp match", "!~": "negated regexp match",
             "<=>": "spaceship comparison",
             "&.": "safe navigation",
             "defined?": "definedness test",
             "===": "case-equality",
             "||= / &&=": "conditional stores"},
    "java": {">>>": "unsigned right shift; also >>>=",
             "::": "method reference"},
    "typescript": {"satisfies": "type-conformance check (TS only)",
                   "??=": "null-coalescing assignment",
                   "&&= / ||=": "logical assignment",
                   "?.": "optional chaining"},
    "c": {"_Generic": "type-generic selection",
          "?:": "the GNU elided-middle form is admitted (optional consequence)"},
}


# --------------------------------------------------------------------------
# Grammar fetching / caching
# --------------------------------------------------------------------------

def _curl(url, timeout=60):
    try:
        out = subprocess.run(["curl", "-sSL", "--max-time", str(timeout), url],
                             capture_output=True)
        return out.stdout.decode("utf-8", "replace")
    except FileNotFoundError:
        import urllib.request
        with urllib.request.urlopen(url, timeout=timeout) as fh:
            return fh.read().decode("utf-8", "replace")


def fetch_grammar(spec):
    """Return the text of one grammar file.

    Tries raw.githubusercontent first.  Where that host is unreachable (some
    sandboxes allow github.com but not the raw CDN) it falls back to scraping
    the `rawLines` payload embedded in the github.com blob page, which carries
    the identical bytes.
    """
    raw = ("https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}"
           .format(**spec))
    text = _curl(raw)
    if text and not text.lstrip().startswith("<") and "404" not in text[:16]:
        return text

    blob = ("https://github.com/{owner}/{repo}/blob/{ref}/{path}?plain=1"
            .format(**spec))
    page = _curl(blob)
    for m in re.findall(
            r'<script type="application/json" '
            r'data-target="react-app\.embeddedData">(.*?)</script>', page, re.S):
        try:
            payload = json.loads(html.unescape(m) if "&quot;" in m[:200] else m)
        except json.JSONDecodeError:
            continue
        found = []

        def walk(node):
            if isinstance(node, dict):
                if isinstance(node.get("rawLines"), list):
                    found.append(node["rawLines"])
                for v in node.values():
                    walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)

        walk(payload)
        if found:
            return "\n".join(found[0])
    return None


def cmd_fetch(force=False):
    os.makedirs(CACHE, exist_ok=True)
    for name, spec in GRAMMARS.items():
        dest = os.path.join(CACHE, name)
        if os.path.exists(dest) and not force:
            print("cached  %s" % name)
            continue
        text = fetch_grammar(spec)
        if text is None:
            print("FAILED  %s (%s/%s@%s)" % (name, spec["owner"], spec["repo"],
                                             spec["ref"]))
            continue
        with open(dest, "w") as fh:
            fh.write(text)
        print("fetched %s  %d lines  %s/%s@%s/%s"
              % (name, len(text.splitlines()), spec["owner"], spec["repo"],
                 spec["ref"], spec["path"]))


# --------------------------------------------------------------------------
# Rule slicing and verification
# --------------------------------------------------------------------------

_rule_cache = {}


def rule_slices(fname):
    if fname in _rule_cache:
        return _rule_cache[fname]
    path = os.path.join(CACHE, fname)
    if not os.path.exists(path):
        _rule_cache[fname] = None
        return None
    txt = open(path).read()
    ind = GRAMMARS[fname]["indent"]
    pat = r"^" + (" " * ind) + r"([A-Za-z_$][A-Za-z0-9_$]*)\s*:\s*"
    idx = [(m.start(), m.group(1)) for m in re.finditer(pat, txt, re.M)]
    out = {"__file__": txt}
    for i, (s, name) in enumerate(idx):
        e = idx[i + 1][0] if i + 1 < len(idx) else len(txt)
        out.setdefault(name, txt[s:e])
    _rule_cache[fname] = out
    return out


def _consts(fname):
    txt = rule_slices(fname)["__file__"]
    found = {}
    for m in re.finditer(r"^const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?);\s*$",
                         txt, re.M | re.S):
        found[m.group(1)] = m.group(2)
    return found


def expanded_rule_text(fname, rule, depth=3):
    """Rule body plus, transitively, the helper rules and const tables it names."""
    slices = rule_slices(fname)
    if slices is None or rule not in slices:
        return None
    consts = _consts(fname)
    seen = {rule}
    text = slices[rule]
    frontier = [text]
    for _ in range(depth):
        nxt = []
        for chunk in frontier:
            names = set(re.findall(r"\$\.([A-Za-z_][A-Za-z0-9_]*)", chunk))
            names |= set(re.findall(r"\$\[['\"]([A-Za-z_]+)['\"]\]", chunk))
            names |= set(re.findall(r"\b([A-Z][A-Z0-9_]{2,})\b", chunk))
            for n in names - seen:
                seen.add(n)
                body = slices.get(n) or consts.get(n)
                if body:
                    text += "\n" + body
                    nxt.append(body)
        frontier = nxt
        if not frontier:
            break
    return text


def _strip_comments(text):
    """Remove // and /* */ comments so stray apostrophes in prose do not
    desynchronise the quote scanner."""
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    text = re.sub(r"(?m)^\s*//.*$", " ", text)
    text = re.sub(r"(?m)\s//[^'\"]*$", " ", text)
    return text


def has_literal(text, op):
    """True if `op` appears as a quoted token literal in `text`.

    A plain substring test on the quoted form, rather than a full tokeniser:
    grammar sources are full of regex literals and escaped quotes that
    desynchronise a naive quote scanner, and no operator spelling contains a
    quote character.
    """
    st = _strip_comments(text)
    return ("'" + op + "'") in st or ('"' + op + '"') in st


def verify_all():
    """Check every 'literal' entry against the cached grammar source."""
    report = {"checked": 0, "ok": 0, "missing_file": [], "missing_rule": [],
              "missing_literal": [], "skipped_shape": 0,
              "derived_soft_checked": 0, "derived_soft_ok": 0,
              "derived_absent_from_file": [], "computed": 0}
    for lang in LANG_ORDER:
        for bucket, entries in FACTS[lang].items():
            for ent in entries:
                if ent["verify"] == "shape":
                    report["skipped_shape"] += 1
                    continue
                if ent["verify"] == "computed":
                    # Built by JS string arithmetic at grammar-load time, so the
                    # spelling exists in no form in the source text.  Recorded
                    # with the expression that produces it; see the entry note.
                    report["computed"] += len(ent["ops"])
                    continue
                if ent["verify"] == "derived":
                    # A derived spelling is assembled by the grammar (string
                    # concatenation, aliasing, or an optional suffix) so it need
                    # not occur verbatim inside its rule.  The weaker check is
                    # that it occurs as a literal SOMEWHERE in the grammar file,
                    # which still catches transcription slips.
                    slices = rule_slices(ent["file"])
                    if slices is None:
                        report["missing_file"].append((lang, ent["file"]))
                        continue
                    if ent["rule"] not in slices:
                        report["missing_rule"].append(
                            (lang, ent["file"], ent["rule"]))
                        continue
                    whole = slices["__file__"]
                    for op in ent["ops"]:
                        report["derived_soft_checked"] += 1
                        if is_open_set(op) or has_literal(whole, op):
                            report["derived_soft_ok"] += 1
                        else:
                            report["derived_absent_from_file"].append(
                                (lang, bucket, ent["rule"], ent["file"], op))
                    continue
                fname = ent["file"]
                if rule_slices(fname) is None:
                    report["missing_file"].append((lang, fname))
                    continue
                text = expanded_rule_text(fname, ent["rule"])
                if text is None:
                    report["missing_rule"].append((lang, fname, ent["rule"]))
                    continue
                for op in ent["ops"]:
                    report["checked"] += 1
                    if has_literal(text, op):
                        report["ok"] += 1
                    else:
                        report["missing_literal"].append(
                            (lang, bucket, ent["rule"], fname, op))
    return report


# --------------------------------------------------------------------------
# Independent cross-check against the COMPILED grammars
# --------------------------------------------------------------------------

# The pins of record (PseudoCoup_v6/Tools/ledgerer/tree_sitter/pins/MANIFEST.md)
# ship compiled grammars for three of these languages.  Their anonymous node
# kinds are the token alphabet, which does not say WHICH rule admits a token --
# so this is a cross-check on the spellings, not a substitute for reading the
# grammar source.
PINNED_MODULES = {
    "python": ("tree_sitter_python", "0.25.0"),
    "rust": ("tree_sitter_rust", "0.24.2"),
    "cpp": ("tree_sitter_cpp", "0.23.4"),
}

# Entries whose "spelling" is a syntactic shape rather than one token, so they
# cannot appear in a token alphabet.
_NOT_A_TOKEN = re.compile(r"[()\[\]{}]|^\.await$|^\.\.\.\?$|^is!$|^&raw |^=&$|"
                          r"^\?\[$|^if-else$|^\?:$|^::<>$|^\|\.\.\.\|$|^\\\\\.$")


def crosscheck_compiled():
    try:
        from tree_sitter import Language
    except ImportError:
        print("tree_sitter runtime not installed; skipping the compiled "
              "cross-check (pip install tree-sitter==0.26.0 "
              "tree-sitter-python==0.25.0 tree-sitter-rust==0.24.2 "
              "tree-sitter-cpp==0.23.4)")
        return None
    import importlib
    results = OrderedDict()
    for lang, (modname, want_ver) in PINNED_MODULES.items():
        try:
            mod = importlib.import_module(modname)
        except ImportError:
            print("%s not installed; skipped" % modname)
            continue
        L = Language(mod.language())
        anon = {L.node_kind_for_id(i) for i in range(L.node_kind_count)
                if L.node_kind_for_id(i) and not L.node_kind_is_named(i)}
        checked, missing = 0, []
        for bucket in BUCKETS:
            for op in bucket_ops(lang, bucket):
                if is_open_set(op) or _NOT_A_TOKEN.search(op):
                    continue
                checked += 1
                if op not in anon:
                    missing.append((bucket, op))
        results[lang] = dict(pinned_version=want_ver, checked=checked,
                             found=checked - len(missing), missing=missing,
                             anon_kind_count=len(anon))
        print("%-8s %d/%d recorded spellings are anonymous node kinds in the "
              "compiled grammar (%d anon kinds total)"
              % (lang, checked - len(missing), checked, len(anon)))
        for m in missing:
            print("    absent from the token alphabet: %s" % (m,))
    return results


# --------------------------------------------------------------------------
# Census cross-check
# --------------------------------------------------------------------------

def census_ops(lang):
    path = os.path.join(HERE, "space_%s.json" % lang)
    if not os.path.exists(path):
        return None
    with open(path) as fh:
        return json.load(fh).get("operations")


def census_report():
    rows = OrderedDict()
    for lang in LANG_ORDER:
        got = census_ops(lang)
        grammar_binary = []
        for ent in FACTS[lang]["binary"]:
            for op in ent["ops"]:
                if is_open_set(op):            # e.g. <custom_operator>
                    continue
                if op not in grammar_binary:
                    grammar_binary.append(op)
        if got is None:
            rows[lang] = dict(census_present=False, grammar_binary=grammar_binary,
                              covered=[], missed=grammar_binary,
                              not_in_grammar_binary=[])
            continue
        covered = [o for o in grammar_binary if o in got]
        missed = [o for o in grammar_binary if o not in got]
        extra = [o for o in got if o not in grammar_binary]
        rows[lang] = dict(
            census_present=True,
            census_count=len(got),
            census_ops=got,
            grammar_binary=grammar_binary,
            grammar_binary_count=len(grammar_binary),
            covered=covered,
            missed=missed,
            not_in_grammar_binary=extra,
            coverage_pct=round(100.0 * len(covered) / max(1, len(grammar_binary)), 1),
        )
    return rows


# --------------------------------------------------------------------------
# Emit
# --------------------------------------------------------------------------

def bucket_ops(lang, bucket, dedupe=True):
    ops = []
    for ent in FACTS[lang][bucket]:
        for op in ent["ops"]:
            if dedupe and op in ops:
                continue
            ops.append(op)
    return ops


def build():
    data = OrderedDict()
    data["generated_by"] = "operator_arity.py"
    data["authority"] = ("tree-sitter grammar sources; every operator is "
                         "attributed to the grammar rule that admits it")
    data["grammar_versions"] = OrderedDict(
        (name, "%s/%s@%s :: %s" % (s["owner"], s["repo"], s["ref"], s["path"]))
        for name, s in GRAMMARS.items())
    data["buckets"] = BUCKETS
    langs = OrderedDict()
    for lang in LANG_ORDER:
        entry = OrderedDict()
        entry["grammar_files"] = LANG_FILES[lang]
        entry["grammar_versions"] = [data["grammar_versions"][f]
                                     for f in LANG_FILES[lang]]
        counts = OrderedDict()
        buckets = OrderedDict()
        for b in BUCKETS:
            ops = bucket_ops(lang, b)
            counts[b] = len(ops)
            buckets[b] = OrderedDict()
            buckets[b]["operators"] = ops
            buckets[b]["sources"] = [
                OrderedDict([("rule", e["rule"]), ("grammar_file", e["file"]),
                             ("grammar_version", data["grammar_versions"][e["file"]]),
                             ("operators", e["ops"]),
                             ("verification", e["verify"]),
                             ("note", e["note"])])
                for e in FACTS[lang][b]]
        counts["total"] = sum(counts[b] for b in BUCKETS)
        entry["counts"] = counts
        entry["buckets"] = buckets
        if "annex" in FACTS[lang]:
            entry["annex"] = OrderedDict([
                ("note", "declaration-side operator inventories: spellings the "
                         "grammar admits when an operator is being DECLARED or "
                         "listed, not when an expression is being built. Not "
                         "counted in the arity buckets."),
                ("operators", bucket_ops(lang, "annex")),
                ("sources", [
                    OrderedDict([("rule", e["rule"]), ("grammar_file", e["file"]),
                                 ("operators", e["ops"]),
                                 ("verification", e["verify"]),
                                 ("note", e["note"])])
                    for e in FACTS[lang]["annex"]]),
            ])
        entry["distinctive"] = DISTINCTIVE.get(lang, {})
        langs[lang] = entry
    data["languages"] = langs
    data["census_coverage"] = census_report()
    return data


def md_escape(op):
    return "`" + op.replace("|", "\\|") + "`"


def to_markdown(data):
    L = []
    A = L.append
    A("# Operator inventory by arity")
    A("")
    A("Read out of tree-sitter grammar sources. Every operator below is "
      "attributed to the grammar rule that admits it; nothing is filled in "
      "from memory. Regenerate with `python3 operator_arity.py`.")
    A("")

    A("## Grammar versions used")
    A("")
    A("| grammar file | repository | ref | path |")
    A("|---|---|---|---|")
    for name, s in GRAMMARS.items():
        A("| `%s` | %s/%s | `%s` | `%s` |"
          % (name, s["owner"], s["repo"], s["ref"], s["path"]))
    A("")
    A("`c_for_cpp.js` is the C base that tree-sitter-cpp v0.23.4 builds on "
      "(it declares `tree-sitter-c: ^0.23.1`). tree-sitter-c `grammar.js` is "
      "byte-identical between v0.23.6 and v0.24.2, so the C and C++ rows rest "
      "on the same C text.")
    A("")

    A("## Counts per bucket")
    A("")
    header = "| language | " + " | ".join(BUCKETS) + " | total |"
    A(header)
    A("|" + "---|" * (len(BUCKETS) + 2))
    for lang in LANG_ORDER:
        c = data["languages"][lang]["counts"]
        A("| **%s** | %s | %d |"
          % (lang, " | ".join(str(c[b]) for b in BUCKETS), c["total"]))
    A("")
    A("Counts are distinct spellings per bucket. `++`/`--` appear in both the "
      "prefix and postfix rows where the grammar admits both. Open-set "
      "placeholders (`<custom_operator>`, `<simple_identifier>`) count as one "
      "each and are flagged in the per-language tables.")
    A("")

    A("## Full spellings")
    A("")
    for lang in LANG_ORDER:
        e = data["languages"][lang]
        A("### %s" % lang)
        A("")
        A("Grammar: %s" % "; ".join(e["grammar_versions"]))
        A("")
        A("| bucket | n | operators | admitting rule(s) |")
        A("|---|---|---|---|")
        for b in BUCKETS:
            ops = e["buckets"][b]["operators"]
            if not ops:
                A("| %s | 0 | _(none in this grammar)_ | - |" % b)
                continue
            rules = []
            for s in e["buckets"][b]["sources"]:
                tag = "%s (`%s`)" % (s["rule"], s["grammar_file"])
                if tag not in rules:
                    rules.append(tag)
            A("| %s | %d | %s | %s |"
              % (b, len(ops), " ".join(md_escape(o) for o in ops),
                 "<br>".join(rules)))
        A("")
        notes = [s for b in BUCKETS for s in e["buckets"][b]["sources"] if s["note"]]
        if notes:
            A("Notes:")
            A("")
            for s in notes:
                A("- `%s` (`%s`): %s" % (s["rule"], s["grammar_file"], s["note"]))
            A("")
        if "annex" in e:
            A("Declaration-side annex (not counted above):")
            A("")
            for src in e["annex"]["sources"]:
                A("- `%s` (`%s`), %d spellings: %s"
                  % (src["rule"], src["grammar_file"], len(src["operators"]),
                     " ".join(md_escape(o) for o in src["operators"])))
                A("  - %s" % src["note"])
            A("")
        if e["distinctive"]:
            A("Operators with no counterpart elsewhere in the line:")
            A("")
            for op, why in e["distinctive"].items():
                A("- `%s` -- %s" % (op, why))
            A("")

    A("## Census coverage (space_<lang>.json `operations`)")
    A("")
    A("| language | census n | grammar binary n | covered | missed | in census "
      "but not in the grammar binary bucket |")
    A("|---|---|---|---|---|---|")
    for lang, r in data["census_coverage"].items():
        if not r["census_present"]:
            A("| **%s** | _no space_%s.json_ | %d | 0 | %d | - |"
              % (lang, lang, len(r["grammar_binary"]), len(r["missed"])))
            continue
        A("| **%s** | %d | %d | %d (%.0f%%) | %s | %s |"
          % (lang, r["census_count"], r["grammar_binary_count"],
             len(r["covered"]), r["coverage_pct"],
             " ".join(md_escape(o) for o in r["missed"]) or "-",
             " ".join(md_escape(o) for o in r["not_in_grammar_binary"]) or "-"))
    A("")
    absent = [l for l, r in data["census_coverage"].items()
              if not r["census_present"]]
    if absent:
        A("No `space_<lang>.json` exists at all for: %s -- those languages have "
          "no behaviour census to compare against, so their whole binary "
          "bucket is unreached rather than partially reached."
          % ", ".join("`%s`" % l for l in absent))
        A("")
    A("The census `operations` lists are binary-operator lists, so they are "
      "compared against the `binary` bucket only. The last column is not an "
      "error in the census: it holds operators the census exercised that this "
      "table files under another bucket (or that the grammar admits only "
      "through an open-set rule).")
    A("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--fetch", action="store_true",
                    help="download grammar sources into grammar_cache/")
    ap.add_argument("--force", action="store_true",
                    help="with --fetch, re-download even if cached")
    ap.add_argument("--verify", action="store_true",
                    help="check every recorded spelling against the cache")
    ap.add_argument("--census", action="store_true",
                    help="print only the census-coverage report")
    ap.add_argument("--crosscheck", action="store_true",
                    help="cross-check the pinned languages against their "
                         "COMPILED grammars via the tree_sitter runtime")
    args = ap.parse_args()

    if args.fetch:
        cmd_fetch(force=args.force)

    if args.crosscheck:
        crosscheck_compiled()
        if not (args.verify or args.census):
            return 0

    if args.verify:
        rep = verify_all()
        print("verify: %d/%d literal spellings found in their admitting rule"
              % (rep["ok"], rep["checked"]))
        print("verify: %d/%d derived spellings present as literals somewhere in "
              "their grammar file (weaker check -- these are assembled by the "
              "grammar, see each entry's note)"
              % (rep["derived_soft_ok"], rep["derived_soft_checked"]))
        print("        %d shape entries skipped (they name a syntactic shape, "
              "not a token)" % rep["skipped_shape"])
        print("        %d computed spellings skipped (built by JS string "
              "arithmetic in the grammar, e.g. Go's compound assignments)"
              % rep["computed"])
        bad = False
        for key in ("missing_file", "missing_rule", "missing_literal",
                    "derived_absent_from_file"):
            for row in rep[key]:
                print("  %-24s %s" % (key, row))
                bad = True
        return 1 if bad else 0

    data = build()

    if args.census:
        print(json.dumps(data["census_coverage"], indent=2))
        return 0

    jpath = os.path.join(HERE, "operator_arity.json")
    mpath = os.path.join(HERE, "operator_arity.md")
    with open(jpath, "w") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")
    with open(mpath, "w") as fh:
        fh.write(to_markdown(data))
    print("wrote %s" % jpath)
    print("wrote %s" % mpath)
    for lang in LANG_ORDER:
        c = data["languages"][lang]["counts"]
        print("  %-11s " % lang + "  ".join("%s=%d" % (b, c[b]) for b in BUCKETS)
              + "  total=%d" % c["total"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
