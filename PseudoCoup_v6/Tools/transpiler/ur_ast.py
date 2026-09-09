"""Define the Universal Rich AST node vocabulary (the hub-side program representation).

Provenance: transplanted 2026-07-28 from
~/Programming/PseudoCoup/pseudocoup/core/ur_ast.py (the v3-born,
v4-current UR-AST; R3-verified suite green). Kept: URNode with a
metadata dict, and the general-purpose node set. Adapted for PCv6:
UI-specific nodes (ModifierNode, DeclarativeNode) are NOT carried —
they arrive with their writers per the growth gate; every node
built by the ingress framework records its LEDGER ID in
metadata["ledger_id"] (id-keyed from the start, the settled T2
keying).
"""
from typing import Any, List, Optional


class URNode:
    """Base class for all Universal Rich AST nodes."""
    def __init__(self):
        self.metadata: dict = {}   # holds ledger_id + Ledger-hydrated facts


class ModuleNode(URNode):
    def __init__(self, body: List["URNode"]):
        super().__init__()
        self.body = body


class FunctionDefNode(URNode):
    def __init__(self, name: str, args: List["IdentifierNode"],
                 body: List["URNode"], return_type: Optional[str] = None):
        super().__init__()
        self.name = name
        self.args = args
        self.body = body
        self.return_type = return_type


class ClassDefNode(URNode):
    def __init__(self, name: str, bases: List[str],
                 methods: List["FunctionDefNode"],
                 fields: List["AssignmentNode"]):
        super().__init__()
        self.name = name
        self.bases = bases
        self.methods = methods
        self.fields = fields


class AssignmentNode(URNode):
    def __init__(self, left: "URNode", right: "URNode"):
        super().__init__()
        self.left = left
        self.right = right


class BinaryOpNode(URNode):
    def __init__(self, left: "URNode", right: "URNode", operator: str):
        super().__init__()
        self.left = left
        self.right = right
        self.operator = operator


class UnaryOpNode(URNode):
    def __init__(self, operator: str, operand: "URNode"):
        super().__init__()
        self.operator = operator
        self.operand = operand


class CastNode(URNode):
    def __init__(self, target_type: str, value: "URNode"):
        super().__init__()
        self.target_type = target_type
        self.value = value


class CallNode(URNode):
    def __init__(self, func_name: str, args: List["URNode"]):
        super().__init__()
        self.func_name = func_name
        self.args = args


class IdentifierNode(URNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = name


class LiteralNode(URNode):
    def __init__(self, value: Any, raw: bool = False):
        super().__init__()
        self.value = value
        self.raw = raw


class ReturnNode(URNode):
    def __init__(self, value: Optional["URNode"]):
        super().__init__()
        self.value = value


class IfNode(URNode):
    def __init__(self, condition: "URNode", body: List["URNode"],
                 orelse: Optional["URNode"] = None):
        super().__init__()
        self.condition = condition
        self.body = body
        self.orelse = orelse


class WhileNode(URNode):
    def __init__(self, condition: "URNode", body: List["URNode"]):
        super().__init__()
        self.condition = condition
        self.body = body


class ForNode(URNode):
    def __init__(self, target: "URNode", iter_: "URNode",
                 body: List["URNode"]):
        super().__init__()
        self.target = target
        self.iter = iter_
        self.body = body


class ListNode(URNode):
    def __init__(self, elements: List["URNode"]):
        super().__init__()
        self.elements = elements


class SubscriptNode(URNode):
    def __init__(self, value: "URNode", slice_: "URNode"):
        super().__init__()
        self.value = value
        self.slice = slice_


class AttributeNode(URNode):
    def __init__(self, value: "URNode", attr: str):
        super().__init__()
        self.value = value
        self.attr = attr
