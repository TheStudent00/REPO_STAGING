"""task o3b, correction lane 7. Parses one tiny snippet per swift
operator recorded in operator_arity.json (every rule under the
`binary` bucket, plus the two equality/comparison rules the defect
was found in) with the SAME tree_sitter_swift binding
compiler_operators_used.py uses, and prints every non-leaf node.type
seen, so the node kind that wraps each operator is READ, not guessed.
No token is special-cased; this is a one-shot inspection script, not
part of the measured pipeline.
"""
from tree_sitter import Language, Parser
import tree_sitter_swift as ts_swift

lang = Language(ts_swift.language())
parser = Parser(lang)

SNIPPETS = [
    ("!=",  "let x = a != b"),
    ("<=",  "let x = a <= b"),
    (">=",  "let x = a >= b"),
    ("==",  "let x = a == b"),
    ("<",   "let x = a < b"),
    (">",   "let x = a > b"),
    ("===", "let x = a === b"),
    ("+",   "let x = a + b"),
    ("-",   "let x = a - b"),
    ("*",   "let x = a * b"),
    ("/",   "let x = a / b"),
    ("%",   "let x = a % b"),
    ("&",   "let x = a & b"),
    ("|",   "let x = a | b"),
    ("^",   "let x = a ^ b"),
    ("<<",  "let x = a << b"),
    (">>",  "let x = a >> b"),
    ("&&",  "let x = a && b"),
    ("||",  "let x = a || b"),
    ("??",  "let x = a ?? b"),
    ("...", "let x = a...b"),
    ("..<", "let x = a..<b"),
    ("+=",  "a += b"),
    ("-=",  "a -= b"),
    ("=",   "a = b"),
    ("as",  "let x = a as Int"),
    ("as?", "let x = a as? Int"),
    ("as!", "let x = a as! Int"),
    ("is",  "let x = a is Int"),
]

for name, code in SNIPPETS:
    src = code.encode("utf-8")
    tree = parser.parse(src)
    kinds = []

    def walk(node):
        if node.child_count > 0:
            kinds.append((node.type, src[node.start_byte:node.end_byte].decode()))
        for c in node.children:
            walk(c)

    walk(tree.root_node)
    wrapping = [k for k in kinds if k[0] not in ("source_file", "property_declaration",
                                                  "value_binding_pattern", "pattern",
                                                  "assignment") or k[0] == "assignment"]
    print(f"{name!r} -> " + ", ".join(f"{t}={txt!r}" for t, txt in wrapping if t != "source_file"))
