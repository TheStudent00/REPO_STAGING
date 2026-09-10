"""Ingest LLVM's X86 encoder slice via tree-sitter and render the Python encoder module.

The C++ half of the T3 ingestor work, and the first LLVM-facing
tool in PCv6 (plan node:
PRIVATE/PseudoIR/Planning/node_0_2_hub/node_0_2_0_construction/node_0_2_0_0_rust_llvm/node_0_2_0_0_0_transpile/,
whose scope covers the C++ ingestor as its co-node increment).

Division of labor, same as the Rust vocabulary ingestor:
- STRUCTURE from tree-sitter (T1): the functions, the enum, the
  class body, its one-line setters, and the emit() switch arms are
  located as CST nodes — replacing the regex/brace-scanning
  extractors (`find_fn_block`, `find_header_block`,
  `EMIT_BYTE_RE`, `ONE_LINE_METHOD_RE`, `parse_switch_arms`).
- RENDERING + ASSEMBLY reused verbatim from render_cpp.py (the
  copied PCv5 transpiler): the expression grammar with uniform
  u8() wrapping, the statement transpiler, the header/section
  emission. Byte-equality with the recorded artifact is the
  acceptance, so the rendering layer must not drift.

Census gate: the 94-kind census of X86MCCodeEmitter.cpp (frozen by
R2) is partitioned; a 95th kind fails ingestion.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_T1 = os.path.normpath(os.path.join(HERE, "..", "ledgerer", "tree_sitter"))
for p in (HERE, _T1):
    if p not in sys.path:
        sys.path.insert(0, p)

from parse_source import parse_file            # noqa: E402
from record_coverage import census, partition  # noqa: E402
from ingest_source import GateFailure          # noqa: E402
import render_cpp as R                         # noqa: E402

# ---- census gate --------------------------------------------------
# Structural kinds the CST walk itself uses:
HANDLED_STRUCTURAL = {
    "translation_unit", "function_definition", "function_declarator",
    "parameter_list", "parameter_declaration", "compound_statement",
    "class_specifier", "enum_specifier", "enumerator_list", "enumerator",
    "field_declaration_list", "field_declaration", "field_identifier",
    "identifier", "qualified_identifier", "switch_statement",
    "case_statement", "type_identifier", "primitive_type",
}

# Every OTHER kind in the R2-frozen 94-kind census of
# X86MCCodeEmitter.cpp — present in the file but outside the named
# slice, or consumed as leaf text by the rendering layer. Frozen so a
# 95th kind (grammar or source drift) FAILS the gate.
BASELINE_R2 = {
    "abstract_function_declarator", "abstract_pointer_declarator",
    "abstract_reference_declarator", "access_specifier", "argument_list",
    "array_declarator", "assignment_expression", "attribute",
    "attribute_declaration", "attributed_statement", "auto",
    "base_class_clause", "binary_expression", "bitfield_clause",
    "break_statement", "call_expression", "char_literal", "comment",
    "condition_clause", "conditional_expression", "continue_statement",
    "declaration", "declaration_list", "default_method_clause",
    "delete_method_clause", "destructor_name", "else_clause",
    "escape_sequence", "expression_statement", "false",
    "field_expression", "field_initializer", "field_initializer_list",
    "for_statement", "if_statement", "init_declarator",
    "initializer_list", "lambda_capture_specifier",
    "lambda_default_capture", "lambda_expression", "namespace_definition",
    "namespace_identifier", "new_expression", "null", "number_literal",
    "operator_name", "optional_parameter_declaration",
    "parenthesized_expression", "placeholder_type_specifier",
    "pointer_declarator", "pointer_expression", "preproc_arg",
    "preproc_def", "preproc_ifdef", "preproc_include",
    "reference_declarator", "return_statement", "sized_type_specifier",
    "storage_class_specifier", "string_content", "string_literal",
    "subscript_argument_list", "subscript_expression",
    "system_lib_string", "template_argument_list", "template_function",
    "template_type", "true", "type_descriptor", "type_qualifier",
    "unary_expression", "update_expression", "using_declaration",
    "virtual_specifier", "while_statement",
}


def _text(n):
    return n.text.decode("utf-8", "replace")


def _walk(node):
    yield node
    for c in node.children:
        yield from _walk(c)


def _fn_name(node):
    """Declarator name of a function_definition (plain or qualified)."""
    d = node.child_by_field_name("declarator")
    while d is not None and d.type != "function_declarator":
        d = d.child_by_field_name("declarator")
    if d is None:
        return None, None
    name_node = d.child_by_field_name("declarator")
    return (_text(name_node) if name_node is not None else None), d


def find_functions(root):
    """-> {name: (params_text, body_text)} for every function_definition."""
    out = {}
    for n in _walk(root):
        if n.type != "function_definition":
            continue
        name, decl = _fn_name(n)
        if name is None:
            continue
        params = decl.child_by_field_name("parameters")
        body = n.child_by_field_name("body")
        if params is None or body is None:
            continue
        out[name] = (_text(params)[1:-1], _text(body)[1:-1])
    return out


def find_class_body(root, class_name):
    for n in _walk(root):
        if n.type == "class_specifier":
            nm = n.child_by_field_name("name")
            if nm is not None and _text(nm) == class_name:
                body = n.child_by_field_name("body")
                return _text(body)[1:-1] if body is not None else None
    return None


def find_enum(root, enum_name):
    for n in _walk(root):
        if n.type == "enum_specifier":
            nm = n.child_by_field_name("name")
            if nm is not None and _text(nm) == enum_name:
                lst = n.child_by_field_name("body")
                return [_text(e.child_by_field_name("name") or e)
                        for e in lst.named_children
                        if e.type == "enumerator"]
    return None


# ---- CST-based replacements for render_cpp's extractors ---------

def make_extractors(root):
    """Build extractor functions closed over the parsed CST, matching
    render_cpp's extractor signatures exactly (they take `src`, which
    is ignored here — the CST is the source of structure)."""
    fns = find_functions(root)

    def extract_emit_byte(src):
        if "emitByte" not in fns:
            raise R.Unsupported("emitByte not found in the CST")
        params, body = fns["emitByte"]
        names = [R.param_name(p) for p in R.split_top_level(params) if p.strip()]
        if names != ["C", "CB"]:
            raise R.Unsupported(f"emitByte signature changed: {names!r}")
        stmts = R.split_statements(body)
        if stmts != ["CB.push_back(C)"]:
            raise R.Unsupported(f"emitByte body changed: {stmts!r}")
        ctx = {"params": {"C": "c", "CB": "cb"},
               "methods": {"push_back": "append"}}
        line = R.pyexpr("CB.push_back(C)", ctx)
        return line.replace("cb.append(c)", "cb.append(u8(c))")

    def extract_mod_rm_byte(src):
        params, body = fns["modRMByte"]
        names = [R.param_name(p) for p in R.split_top_level(params) if p.strip()]
        if names != ["Mod", "RegOpcode", "RM"]:
            raise R.Unsupported(f"modRMByte signature changed: {names!r}")
        ctx = {"params": {"Mod": "mod_", "RegOpcode": "reg_opcode", "RM": "rm"},
               "funcs": {}}
        return R.transpile_body(body, ctx)

    def extract_emit_reg_modrm_byte(src):
        key = next((k for k in fns if k.endswith("emitRegModRMByte")), None)
        if key is None:
            raise R.Unsupported("emitRegModRMByte not found in the CST")
        params, body = fns[key]
        names = [R.param_name(p) for p in R.split_top_level(params) if p.strip()]
        if names != ["ModRMReg", "RegOpcodeFld", "CB"]:
            raise R.Unsupported(f"emitRegModRMByte signature changed: {names!r}")
        if not R.GET_X86_REGNUM_CALL.search(body):
            raise R.Unsupported(
                "emitRegModRMByte body no longer calls getX86RegNum(ModRMReg)")
        sub = R.GET_X86_REGNUM_CALL.sub("ModRMRegNum", body)
        ctx = {"params": {"ModRMRegNum": "modrm_reg_num",
                          "RegOpcodeFld": "reg_opcode_fld", "CB": "cb"},
               "funcs": {"emitByte": "emit_byte", "modRMByte": "mod_rm_byte"}}
        return R.transpile_body(sub, ctx)

    def extract_emit_sib_byte(src):
        key = next((k for k in fns if k.endswith("emitSIBByte")), None)
        if key is None:
            raise R.Unsupported("emitSIBByte not found in the CST")
        params, body = fns[key]
        names = [R.param_name(p) for p in R.split_top_level(params) if p.strip()]
        if names != ["SS", "Index", "Base", "CB"]:
            raise R.Unsupported(f"emitSIBByte signature changed: {names!r}")
        ctx = {"params": {"SS": "ss", "Index": "index", "Base": "base",
                          "CB": "cb"},
               "funcs": {"emitByte": "emit_byte", "modRMByte": "mod_rm_byte"}}
        return R.transpile_body(body, ctx)

    def extract_prefix_kind_enum(src):
        names = find_enum(root, "PrefixKind")
        if not names:
            raise R.Unsupported("enum PrefixKind not found in the CST")
        import keyword
        return names, {n: (n.upper() if keyword.iskeyword(n) else n)
                       for n in names}

    # The class body is located by the CST; the WITHIN-class shapes
    # (field default, one-line setters, emit()'s switch arms) keep the
    # copied text-level readers, which operate on that body text. So
    # instead of replacing extract_prefix_helper wholesale, its one
    # structural call — find_header_block for the class — is answered
    # from the CST.
    def find_header_block(src, header_re, start=0):
        if "X86OpcodePrefixHelper" in header_re:
            body = find_class_body(root, "X86OpcodePrefixHelper")
            if body is None:
                raise R.Unsupported(
                    "class X86OpcodePrefixHelper not found in the CST")
            return body, 0
        return _orig_find_header_block(src, header_re, start)

    return dict(
        extract_emit_byte=extract_emit_byte,
        extract_mod_rm_byte=extract_mod_rm_byte,
        extract_emit_reg_modrm_byte=extract_emit_reg_modrm_byte,
        extract_emit_sib_byte=extract_emit_sib_byte,
        extract_prefix_kind_enum=extract_prefix_kind_enum,
        find_header_block=find_header_block,
    )


_orig_find_header_block = R.find_header_block


def build_encoder(src_path, outfile):
    """Parse with T1, gate the census, then render via render_cpp with
    CST-based extractors substituted in."""
    tree = parse_file(src_path, "cpp")
    root = tree.root_node

    c = census(root)
    part = partition(set(c["named"]), handled=HANDLED_STRUCTURAL,
                     baseline=BASELINE_R2)
    if part["leftover"]:
        raise GateFailure(part["leftover"], os.path.basename(src_path))

    saved = {}
    try:
        for name, fn in make_extractors(root).items():
            saved[name] = getattr(R, name)
            setattr(R, name, fn)
        R.main(src_path, outfile)
    finally:
        for name, fn in saved.items():
            setattr(R, name, fn)
    return outfile


if __name__ == "__main__":
    build_encoder(sys.argv[1],
                  sys.argv[2] if len(sys.argv) > 2 else "llvm_encoder_gen.py")
