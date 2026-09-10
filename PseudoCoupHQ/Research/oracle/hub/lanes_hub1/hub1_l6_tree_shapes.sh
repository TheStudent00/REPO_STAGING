#!/usr/bin/env bash
# hub1_l6_tree_shapes.sh -- task hub1, lane 6. Writes nothing.
# WHAT IT ASKS: the exact shape the installed tree-sitter-go grammar gives
# the handful's own functions -- every node with its type, its field name
# under its super-node, and its span -- so the front end's walk is written
# against the grammar as it IS and not as it is assumed to be.
set -uo pipefail
cd PseudoCoupHQ/Research/oracle/hub
python3 - <<'PY'
import tree_sitter, tree_sitter_go
print("tree_sitter", getattr(tree_sitter, "__version__", "?"))
language = tree_sitter.Language(tree_sitter_go.language())
parser = tree_sitter.Parser(language)
data = open("handful/handful.go", "rb").read()
tree = parser.parse(data)

def show(node, depth, field):
    if depth > 9:
        return
    text = data[node.start_byte:node.end_byte].decode("utf-8")
    text = text.replace("\n", "\\n")
    if len(text) > 44:
        text = text[:44] + "..."
    print("%s%-26s field=%-12s %s..%s  %r"
          % ("  " * depth, node.type, field,
             node.start_point, node.end_point, text))
    for index, child in enumerate(node.children):
        name = node.field_name_for_child(index)
        show(child, depth + 1, name)

count = 0
for child in tree.root_node.children:
    if child.type != "function_declaration":
        continue
    name = child.child_by_field_name("name")
    if data[name.start_byte:name.end_byte].decode() == "main":
        continue
    count += 1
    if count > 3:
        continue
    print("==== %s" % data[name.start_byte:name.end_byte].decode())
    show(child, 0, "-")
PY
