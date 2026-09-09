"""Validates a slicing request form: path resolves, entry symbol found by tree-sitter, scope filter parses.

Schema: forms/FORM_SCHEMA.md. The root under which source_file
paths resolve is a parameter (default:
PseudoCoup_v5, the archived research tree whose
vendoring scripts pin the compiler sources), so the same form
validates on host and sandbox alike.

Symbol finding uses the T1 tool
PseudoCoup_v6/Tools/ledgerer/tree_sitter/parse_source.py
— the ONLY place in PCv6 that owns parsing. For generated sources
whose seam is a cited construct rather than a named definition
(a generated match arm, an enum variant), what IS checkable is verbatim
presence in the file; the validator checks exactly that for every
cited_constructs entry, and still requires a findable entry_symbol.

A broken form is REFUSED with the specific failure named.
Run:
    python3 PseudoIR/Tools/intentions/validate_form.py FORM.json --root PseudoCoup_v5
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# The parser lives in the OTHER project. PseudoIR borrows PseudoCoup's
# toolchain; this is one of the borrow points. Same env-var pattern the
# ledger and intentions suites used before their fixtures were vendored.
PSEUDOCOUP = os.environ.get(
    "PSEUDOCOUP_ROOT", os.path.expanduser("PseudoCoup_v6"))
T1_DIR = os.path.join(PSEUDOCOUP, "Tools", "ledgerer", "tree_sitter")
if not os.path.isdir(T1_DIR):
    raise RuntimeError(
        f"cannot find PseudoCoup's parser at {T1_DIR}. "
        "Set PSEUDOCOUP_ROOT to PseudoCoup's repo root.")
if T1_DIR not in sys.path:
    sys.path.insert(0, T1_DIR)

import parse_source  # noqa: E402  (the T1 tool)

REQUIRED = ("language", "intention", "stage", "source_file",
            "entry_symbol", "scope_filter", "stand_ins", "rule")

# language (form vocabulary) -> T1 grammar name
GRAMMAR_OF = {"rust": "rust", "python": "python", "cpp": "cpp"}

# symbol_kind -> definition node types per grammar
DEF_NODES = {
    "function": {"rust": ("function_item",),
                 "python": ("function_definition",),
                 "cpp": ("function_definition",)},
    "type": {"rust": ("struct_item", "enum_item", "union_item",
                      "trait_item", "type_item"),
             "python": ("class_definition",),
             "cpp": ("struct_specifier", "class_specifier",
                     "enum_specifier")},
}


class FormRefused(ValueError):
    """Raised with the specific failure named; the form is not accepted."""


def _definition_name(node, grammar):
    """Return the defined name of a definition node, or None."""
    name = node.child_by_field_name("name")
    if name is not None:
        return name.text.decode("utf-8", "replace")
    if grammar == "cpp":
        # cpp function names sit inside the declarator subtree
        decl = node.child_by_field_name("declarator")
        while decl is not None:
            inner = decl.child_by_field_name("declarator")
            if inner is None:
                break
            decl = inner
        if decl is not None and decl.type in ("identifier",
                                              "field_identifier"):
            return decl.text.decode("utf-8", "replace")
    return None


def _find_definition(root_node, kinds, symbol, grammar):
    """Iteratively search the tree for a definition node named symbol."""
    stack = [root_node]
    while stack:
        node = stack.pop()
        if node.type in kinds and _definition_name(node, grammar) == symbol:
            return node
        # push in reverse so earlier definitions are found first
        stack.extend(reversed(node.children))
    return None


def validate_form(form_path, root):
    """Validate one form against root; return report lines or raise FormRefused."""
    name = os.path.basename(form_path)
    lines = []

    # 1. the form parses and is complete
    try:
        with open(form_path, "r", encoding="utf-8") as f:
            form = json.load(f)
    except (OSError, ValueError) as exc:
        raise FormRefused(f"{name}: form does not parse as JSON ({exc})")
    for field in REQUIRED:
        if field not in form:
            raise FormRefused(f"{name}: missing required field {field}")

    # 2. source_file resolves under the declared root
    rel = form["source_file"]
    if os.path.isabs(rel) or ".." in rel.split("/"):
        raise FormRefused(
            f"{name}: source_file must be relative to the declared "
            f"root, without '..' (got {rel!r})")
    full = os.path.join(root, rel)
    if not os.path.isfile(full):
        raise FormRefused(
            f"{name}: source_file does not exist at its declared "
            f"path: {rel} (root {root})")
    lines.append(f"VALID {name}: source_file {rel} exists under root")

    # 3. scope_filter parses
    sf = form["scope_filter"]
    if (not isinstance(sf, dict)
            or set(sf) != {"include", "exclude"}
            or not all(isinstance(v, list) and v
                       and all(isinstance(s, str) and s for s in v)
                       for v in sf.values())):
        raise FormRefused(
            f"{name}: scope_filter does not parse — want "
            "{'include': [...], 'exclude': [...]} with non-empty "
            "string lists")
    lines.append(f"VALID {name}: scope_filter parses "
                 f"(include={len(sf['include'])}, "
                 f"exclude={len(sf['exclude'])})")

    # 4. entry_symbol findable by tree-sitter (the T1 tool)
    language = form["language"]
    if language not in GRAMMAR_OF:
        raise FormRefused(
            f"{name}: language {language!r} has no registered "
            f"tree-sitter grammar (registered: {sorted(GRAMMAR_OF)})")
    grammar = GRAMMAR_OF[language]
    kind = form.get("symbol_kind", "function")
    if kind not in DEF_NODES:
        raise FormRefused(
            f"{name}: symbol_kind {kind!r} unknown "
            f"(known: {sorted(DEF_NODES)})")
    tree = parse_source.parse_file(full, grammar)
    node = _find_definition(tree.root_node, DEF_NODES[kind][grammar],
                            form["entry_symbol"], grammar)
    if node is None:
        raise FormRefused(
            f"{name}: entry_symbol {form['entry_symbol']!r} not found "
            f"by tree-sitter as a {kind} definition in {rel}")
    lines.append(
        f"VALID {name}: entry_symbol {form['entry_symbol']} found as "
        f"{node.type} at line {node.start_point[0] + 1}")

    # 5. cited constructs: verbatim presence is what IS checkable
    cited = form.get("cited_constructs", [])
    if cited:
        with open(full, "rb") as f:
            src = f.read()
        for construct in cited:
            if construct.encode("utf-8") not in src:
                raise FormRefused(
                    f"{name}: cited construct {construct!r} not "
                    f"present verbatim in {rel}")
        lines.append(f"VALID {name}: {len(cited)} cited construct(s) "
                     f"present verbatim")

    return lines


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("forms", nargs="+", help="form JSON file(s)")
    ap.add_argument("--root", default=os.path.expanduser(
        "PseudoCoup_v5"),
        help="root that source_file paths are relative to")
    args = ap.parse_args(argv)
    ok = True
    for form_path in args.forms:
        try:
            for line in validate_form(form_path, args.root):
                print(line)
        except FormRefused as exc:
            print(f"REFUSED: {exc}")
            ok = False
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
