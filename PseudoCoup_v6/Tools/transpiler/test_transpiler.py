"""Acceptance for the ingress framework: all four stages on a toy grammar; the gate refuses unknowns.

The settled acceptance of
<WORKSPACE_DIR>/PseudoCoup_v6/Planning/node_0_0_tools/node_0_0_1_transpiler/SUPPORT_ingress.md.
Run:
    python3 -m pytest <WORKSPACE_DIR>/PseudoCoup_v6/Tools/transpiler/ -q
"""
import json
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from ingest_source import Builder, GateFailure, Ingestor, ingest_file  # noqa: E402
from ur_ast import (BinaryOpNode, FunctionDefNode, IdentifierNode,     # noqa: E402
                    ModuleNode, ReturnNode)

_LEDGER = os.path.normpath(os.path.join(HERE, "..", "ledgerer"))
sys.path.insert(0, _LEDGER)
import check_ledger  # noqa: E402


class ToyPythonIngestor(Ingestor):
    """Minimal python-grammar ingestor: enough table for the toy fixture."""
    grammar = "python"

    def __init__(self):
        self.node_table = {
            "module": lambda b, n, i: ModuleNode(b.build_named_sub_nodes(n)),
            "function_definition": self._function,
            "parameters": lambda b, n, i: None,     # consumed by _function
            "identifier": lambda b, n, i: IdentifierNode(b.text(n)),
            "block": lambda b, n, i: None,          # consumed by _function
            "return_statement": lambda b, n, i: ReturnNode(
                b.build(n.named_children[0]) if n.named_children else None),
            "binary_operator": self._binop,
        }
        self.baseline = {
            "comment": "trivia; no build target",
        }

    @staticmethod
    def _function(b, n, i):
        name = b.text(n.child_by_field_name("name"))
        params = [IdentifierNode(b.text(p))
                  for p in n.child_by_field_name("parameters").named_children]
        body = b.build_named_sub_nodes(n.child_by_field_name("body"))
        return FunctionDefNode(name, params, body)

    @staticmethod
    def _binop(b, n, i):
        return BinaryOpNode(b.build(n.child_by_field_name("left")),
                            b.build(n.child_by_field_name("right")),
                            b.text(n.child_by_field_name("operator")))

    def resolve_type(self, node):
        if node is not None and node.type == "function_definition":
            n = node.child_by_field_name("parameters").named_children
            return f"fn/{len(n)}"
        return None


def test_all_four_stages():
    r = ingest_file(os.path.join(HERE, "fixtures", "toy_ok.py"),
                    ToyPythonIngestor())
    m = r["module"]
    assert isinstance(m, ModuleNode) and len(m.body) == 2
    fn = m.body[0]
    assert isinstance(fn, FunctionDefNode) and fn.name == "double"
    assert isinstance(fn.body[0], ReturnNode)
    assert isinstance(fn.body[0].value, BinaryOpNode)
    assert fn.body[0].value.operator == "+"
    assert r["partition"]["leftover"] == []


def test_ur_nodes_carry_ledger_ids_that_exist_in_ledger():
    r = ingest_file(os.path.join(HERE, "fixtures", "toy_ok.py"),
                    ToyPythonIngestor())
    ledger_ids = {rec["id"] for rec in r["ledger"]["records"]}
    fn = r["module"].body[0]
    assert fn.metadata["ledger_id"] in ledger_ids
    assert fn.metadata["ledger_id"].startswith("0:source_file/")


def test_types_resolved_replace_unresolvable():
    r = ingest_file(os.path.join(HERE, "fixtures", "toy_ok.py"),
                    ToyPythonIngestor())
    decls = [rec for rec in r["ledger"]["records"]
             if rec["node_kind"] == "function_definition"]
    assert decls and all(d["semantic"]["type"] == "fn/2" or
                         d["semantic"]["type"] == "fn/1"
                         for d in decls)
    assert r["ledger"]["meta"]["resolved_types"] == len(decls)


def test_ledger_still_checks_green():
    fixdir = os.path.join(HERE, "fixtures")
    r = ingest_file(os.path.join(fixdir, "toy_ok.py"), ToyPythonIngestor())
    report = check_ledger.check(r["ledger"], fixdir)
    assert report["ok"], report


def test_gate_refuses_unknown_kind():
    with pytest.raises(GateFailure) as e:
        ingest_file(os.path.join(HERE, "fixtures", "toy_unknown_kind.py"),
                    ToyPythonIngestor())
    assert "class_definition" in e.value.leftover


def test_ingest_deterministic():
    path = os.path.join(HERE, "fixtures", "toy_ok.py")
    a = ingest_file(path, ToyPythonIngestor())["ledger"]
    b = ingest_file(path, ToyPythonIngestor())["ledger"]
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
