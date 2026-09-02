#!/usr/bin/env python3
"""syn_shim — the slice of syn's API that rustc_macros needs, backed by
tree-sitter instead of a transpiled parser.

| syn item          | shim class                      |
| ----------------- | ------------------------------- |
| syn::DeriveInput  | DeriveInput (ident, data, attrs)|
| syn::Data::Struct | DataStruct  (fields)            |
| syn::Data::Enum   | DataEnum    (variants)          |
| syn::Field        | Field       (ident, ty)         |
| syn::Ident        | plain str (sufficient here)     |

Research spike, 2026-08-02 — see README.md beside this file.
Pins: tree-sitter==0.26.0, tree-sitter-rust==0.24.2.
"""
from tree_sitter import Language, Parser
import tree_sitter_rust as tsr

_L = Language(tsr.language())
_P = Parser(_L)


def _text(src, n):
    return src[n.start_byte:n.end_byte].decode()


class Field:
    def __init__(self, ident, ty):
        self.ident, self.ty = ident, ty


class Variant:
    def __init__(self, ident, discr):
        self.ident, self.discr = ident, discr


class DataStruct:
    def __init__(self, fields):
        self.fields = fields


class DataEnum:
    def __init__(self, variants):
        self.variants = variants


class DeriveInput:
    """What syn::parse_macro_input!(input as DeriveInput) yields."""

    def __init__(self, ident, data, attrs):
        self.ident, self.data, self.attrs = ident, data, attrs


def parse_derive_input(source: str) -> DeriveInput:
    tree = _P.parse(source.encode())
    src = source.encode()
    for item in tree.root_node.children:
        if item.type == "struct_item":
            name = _text(src, item.child_by_field_name("name"))
            fields = []
            body = item.child_by_field_name("body")
            if body:
                for f in body.children:
                    if f.type == "field_declaration":
                        fields.append(Field(
                            _text(src, f.child_by_field_name("name")),
                            _text(src, f.child_by_field_name("type"))))
            return DeriveInput(name, DataStruct(fields), [])
        if item.type == "enum_item":
            name = _text(src, item.child_by_field_name("name"))
            variants = []
            for v in item.child_by_field_name("body").children:
                if v.type == "enum_variant":
                    vi = _text(src, v.child_by_field_name("name"))
                    dv = v.child_by_field_name("value")
                    variants.append(
                        Variant(vi, _text(src, dv) if dv else None))
            return DeriveInput(name, DataEnum(variants), [])
    raise ValueError("no struct or enum item found")
