#!/usr/bin/env python3
"""construct_catalogue.py -- derive the layer-3 CONSTRUCT list per language.

the owner blessed three construct families on 2026-08-19: access, flow,
binding.  This file does NOT hand-list which constructs each language
has.  It states a ROLE (what the construct is for), gives that role a
set of candidate kind NAMES, and then asks each grammar's own kinds
file (kinds_<lang>.json, phase 0) which of those names it declares.

  * a role RESOLVED  -- the grammar declares a kind for it; the name it
    resolved to is recorded, because the name differs per grammar
    (`subscript` in python, `index_expression` in go and rust,
    `subscript_expression` in c++, php and typescript).
  * a role ABSENT    -- no candidate name is declared.  Absence is a
    FINDING and is written down as one, never patched over.

Emits construct_catalogue.json and prints the per-language table.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

LANGS = ["go", "rust", "cpp", "swift", "dart", "csharp", "kotlin",
         "java", "typescript", "python", "ruby", "php"]

# family -> role -> the candidate kind names.  Candidates are spellings
# the twelve grammars are known to use for the SAME job.  A candidate
# list is not a claim that a language has the construct; the grammar
# answers that.
ROLES = {
    "access": {
        "subscript": ["subscript_expression", "subscript",
                      "index_expression", "index_selector",
                      "element_reference", "element_access_expression",
                      "array_access"],
        "slice": ["slice_expression", "slice", "range_expression"],
        "member": ["member_access_expression", "member_expression",
                   "field_expression", "selector_expression",
                   "attribute", "navigation_expression",
                   "field_access", "unconditional_assignable_selector",
                   "qualified_identifier", "call"],
    },
    "flow": {
        "if": ["if_statement", "if_expression", "if"],
        "for": ["for_statement", "for_expression", "for",
                "enhanced_for_statement", "foreach_statement",
                "for_in_statement"],
        "while": ["while_statement", "while_expression", "while",
                  "while_modifier"],
        "break": ["break_statement", "break_expression", "break"],
        "continue": ["continue_statement", "continue_expression",
                     "next", "continue"],
        "try": ["try_statement", "try_expression", "try_block",
                "begin_block", "begin", "do_block", "rescue"],
    },
    "binding": {
        "assign": ["assignment", "assignment_expression",
                   "assignment_statement", "short_var_declaration",
                   "variable_declaration", "let_declaration",
                   "local_variable_declaration", "property_declaration",
                   "lexical_declaration", "constant_declaration",
                   "local_variable_declaration_statement",
                   "declaration"],
        "augassign": ["augmented_assignment",
                      "augmented_assignment_expression",
                      "compound_assignment_expr", "operator_assignment",
                      "assignment_statement", "assignment_expression",
                      "assignment"],
        "unpack": ["pattern_list", "tuple_pattern", "array_pattern",
                   "object_pattern", "destructured_left_assignment",
                   "multi_variable_declaration", "left_assignment_list",
                   "expression_list", "structured_binding_declarator",
                   "assignment_statement", "record_pattern",
                   "pattern_assignment", "list_pattern",
                   "list_literal", "tuple"],
    },
}


def declared(lang):
    d = json.load(open(os.path.join(HERE, "kinds_%s.json" % lang)))
    return (set(d.get("named_concrete", []))
            | set(d.get("anonymous", []))
            | set(d.get("anonymous_positioned", []))
            | set(d.get("hidden", []))
            | set(d.get("supertypes", [])))


def main():
    out = {}
    for lang in LANGS:
        have = declared(lang)
        fam = {}
        for family, roles in ROLES.items():
            fam[family] = {}
            for role, cands in roles.items():
                hits = [c for c in cands if c in have]
                fam[family][role] = dict(
                    present=bool(hits),
                    kind=hits[0] if hits else None,
                    all_matches=hits,
                )
        out[lang] = fam

    path = os.path.join(HERE, "construct_catalogue.json")
    json.dump(out, open(path, "w"), indent=1, sort_keys=True)

    order = [(f, r) for f in ("access", "flow", "binding")
             for r in sorted(ROLES[f])]
    print("construct catalogue -- role resolved to the grammar's own "
          "kind name, or ABSENT")
    for lang in LANGS:
        print("")
        print("  %s" % lang)
        for f, r in order:
            c = out[lang][f][r]
            print("    %-8s %-10s %s"
                  % (f, r, c["kind"] if c["present"] else "ABSENT"))
    n_abs = sum(1 for l in LANGS for f, r in order
                if not out[l][f][r]["present"])
    print("")
    print("resolved %d of %d role slots; %d ABSENT"
          % (len(LANGS) * len(order) - n_abs, len(LANGS) * len(order),
             n_abs))
    print("wrote %s" % path)


if __name__ == "__main__":
    main()
