"""Verification tests for ts_to_ur — the settling instrument (the owner,
2026-08-11: skeptical until the design is verified).

    python3 ~/Programming/PseudoCoup_v5/Tools/ledgerer/test_ts_to_ur.py

Each test states what would falsify the design if it failed. The
parser is constructed HERE, in one place, honouring the single-owner
rule until the frontend module exists. The kind map used is a small
EXPLICIT test map (q1's 163-row ratification is pending); unknown
kinds refusing is itself under test.
"""

import sys

from tree_sitter import Language, Parser
import tree_sitter_rust as tsr

import ledger
import ts_to_ur
import ur

GRAMMAR_VERSION = "0.24.2"          # the pin of record

SAMPLE = b"""\
use std::collections::HashMap;

pub struct Counter {
    counts: HashMap<String, u32>,
}

impl Counter {
    pub fn bump(&mut self, key: &str) -> u32 {
        let n = self.counts.entry(key.to_string()).or_insert(0);
        *n += 1;
        *n
    }
}
"""

# explicit test rows only — every named kind the sample produces.
TEST_KIND_MAP = {
    "source_file": "sequence", "use_declaration": "name",
    "scoped_identifier": "name", "identifier": "name",
    "struct_item": "record", "visibility_modifier": "declarative-form",
    "type_identifier": "type-form", "field_declaration_list": "record",
    "field_declaration": "record", "generic_type": "type-form",
    "type_arguments": "type-form", "primitive_type": "type-form",
    "impl_item": "record", "declaration_list": "sequence",
    "function_item": "function", "parameters": "function",
    "self_parameter": "name", "mutable_specifier": "declarative-form",
    "self": "name", "parameter": "name", "reference_type": "proof-form",
    "block": "sequence", "let_declaration": "name",
    "call_expression": "service call", "field_expression": "name",
    "arguments": "function", "string_literal": "value",
    "integer_literal": "value", "expression_statement": "sequence",
    "compound_assignment_expr": "mutation", "unary_expression": "operation",
    "field_identifier": "name", "string_content": "value",
    "token_tree": "value", "macro_invocation": "service call",
    "binary_expression": "operation",
}

VARIANT_ROLES = {"binary_expression": "operator",
                 "compound_assignment_expr": "operator"}
STENCILS = {"field_declaration": ("name", ":", "type"),
            "struct_item": (), "function_item": ()}


class Seq:
    """Minimal sequencer: one batch, ordinals in mint order."""
    def __init__(self, batch=0):
        self.batch, self.n = batch, -1
    def mint(self):
        self.n += 1
        return ur.Id(batch=self.batch, ordinal=self.n)


def build(source=SAMPLE, kind_map=None):
    parser = Parser(Language(tsr.language()))
    pack = ts_to_ur.LanguagePack(
        language="rust", grammar_version=GRAMMAR_VERSION,
        kind_map=kind_map or TEST_KIND_MAP,
        stencils=STENCILS, variant_roles=VARIANT_ROLES)
    mapper = ts_to_ur.Mapper(pack, Seq())
    tree = parser.parse(source)
    return mapper, tree, source


FAILURES = []
def check(name, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ") + name + (f"  [{detail}]" if detail and not cond else ""))
    if not cond:
        FAILURES.append(name)


def main():
    # 1 — one named ts node -> one ur node, none lost, none invented.
    mapper, tstree, src = build()
    urtree = mapper.map_file("sample.rs", src, tstree)
    def count_named(n):
        return (1 if n.is_named else 0) + sum(count_named(c) for c in n.children)
    ts_count = count_named(tstree.root_node)
    ur_count = sum(1 for _ in urtree.root.walk())
    check("node conservation (named ts == ur)", ts_count == ur_count,
          f"ts {ts_count} vs ur {ur_count}")

    # 2 — ids are unique and walk order == mint order (admission order).
    ids = [n.id for n in urtree.root.walk()]
    check("id uniqueness", len(ids) == len(set(ids)))
    check("walk order == mint order",
          [i.ordinal for i in ids] == sorted(i.ordinal for i in ids))

    # 3 — content leaves carry text; structural nodes carry none.
    leaves = [n for n in urtree.root.walk() if not n.sub_nodes]
    named_leaf_texts = {n.origin.ts_kind: n.text() for n in leaves}
    check("identifier leaf carries text",
          any(n.origin.ts_kind == "identifier" and n.text() for n in leaves))
    structural = [n for n in urtree.root.walk() if n.sub_nodes]
    check("structural nodes carry no text",
          all(n.text() is None for n in structural if n.origin.ts_kind != "token_tree"))

    # 4 — variant: the operator arrives by role, exactly as parsed.
    ops = [n.origin.variant for n in urtree.root.walk()
           if n.origin.ts_kind == "compound_assignment_expr"]
    check("variant by role (+=)", ops == ["+="], repr(ops))

    # 5 — roles: field() answers by the grammar's names.
    fns = [n for n in urtree.root.walk() if n.origin.ts_kind == "function_item"]
    check("role 'name' resolves on function_item",
          fns and fns[0].field("name") is not None
          and fns[0].field("name").text() == "bump")

    # 6 — no source retention: the tree object holds no bytes.
    check("Tree holds no source copy",
          not hasattr(urtree, "source_bytes"))

    # 7 — unknown kind refuses BY NAME (q1 posture).
    try:
        m2, t2, s2 = build(kind_map={"source_file": "sequence"})
        m2.map_file("x.rs", s2, t2)
        check("unknown ts_kind refuses", False)
    except ts_to_ur.Refused as e:
        check("unknown ts_kind refuses", "kind map" in str(e), str(e))

    # 8 — ERROR refuses, naming the pin (mirror-the-pin ruling).
    bad = b'unsafe extern "C" { safe fn f(); }'
    try:
        m3, t3, s3 = build(source=bad)
        m3.map_file("bad.rs", s3, t3)
        check("ERROR refuses naming the pin", False)
    except ts_to_ur.Refused as e:
        check("ERROR refuses naming the pin", "pin" in str(e), str(e))

    # 9 — opacity: token_tree is ONE node, marked, text kept.
    macro_src = b'fn f() { println!("hi {}", name); }'
    m4, t4, s4 = build(source=macro_src)
    tr4 = m4.map_file("m.rs", s4, t4)
    opaque = [n for n in tr4.root.walk() if n.semantic.get("opaque")]
    check("token_tree -> one opaque node", len(opaque) == 1, repr(len(opaque)))
    check("opaque node keeps its text",
          opaque and opaque[0].text() == '("hi {}", name)',
          repr(opaque and opaque[0].text()))
    check("opaque node has no sub-nodes (pre-injection)",
          opaque and not opaque[0].sub_nodes)

    # 10 — check_pin refuses on mismatch, passes on match.
    pack = m4.language_pack
    try:
        pack.check_pin("9.9.9"); check("check_pin refuses mismatch", False)
    except ts_to_ur.Refused as e:
        check("check_pin refuses mismatch", "pin" in str(e))
    pack.check_pin(GRAMMAR_VERSION)
    check("check_pin passes on match", True)

    # 11 — check_level: a reference token the grammar lacks is reported.
    missing = pack.check_level(grammar_tokens={"fn", "->", "=="},
                               reference_tokens={"fn", "->", "==", "safe"})
    check("check_level surfaces 'safe'", missing == {"safe"}, repr(missing))

    # 12 — the mapped tree admits into the ledger and survives a
    # dump/load round trip byte-identically (the store is downstream).
    table = ledger.Table(frame="test")
    ledger.admit(table, urtree.root)
    d1 = ledger.dump(table)
    d2 = ledger.dump(ledger.load(d1))
    check("ledger admit + dump/load fixed point", d1 == d2)

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURE(S): {FAILURES}")
        sys.exit(1)
    print("all tests pass")


if __name__ == "__main__":
    main()
