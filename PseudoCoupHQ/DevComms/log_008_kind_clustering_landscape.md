# log_008 — kind-clustering landscape survey of six tree-sitter node-types.json files

Date: 2026-08-12. Author: survey agent for the owner's PseudoCoup research node.
Raw data: `PseudoCoupHQ/Research/kind_signature_clustering/raw/`.
Re-runnable measurement script: `PseudoCoupHQ/Research/kind_signature_clustering/survey.py`.

Vocabulary note: tree-sitter's JSON key `"children"` names the unnamed-slot
spec of a kind; in prose this log calls it the **sub-node spec**. Nodes that a
supertype covers are its **sub-nodes**; the kinds a slot admits are its
**input kinds**; the supertypes a kind belongs to are its **output supertypes**.

## §1 Verdict

Arity and input-type data are perfectly uniform (1232/1232 slots across all six grammars carry `multiple`, `required`, and a non-empty type list), but output-type data is not: kotlin (fwcd 0.3.8) declares 0 supertypes and 0 field slots, and dart declares only 3 supertypes, so cross-language clustering can consume arity + input types everywhere today, while output supertypes must be derived (not read) for kotlin and dart.

## §2 What was fetched

All files fetched 2026-08-12. Byte sizes are of the saved raw JSON.

| language | repo | tag / ref | bytes | route |
|---|---|---|---|---|
| rust | tree-sitter/tree-sitter-rust | v0.24.2 | 99,023 | raw.githubusercontent.com |
| python | tree-sitter/tree-sitter-python | v0.25.0 | 64,995 | raw.githubusercontent.com |
| kotlin | fwcd/tree-sitter-kotlin | 0.3.8 (npm `tree-sitter-kotlin@0.3.8`) | 189,208 | npm tarball |
| dart | UserNobody14/tree-sitter-dart (exists; ast-grep fork not needed) | npm `tree-sitter-dart@1.0.0`, gitHead `53485a8f301254e19c518aa20c80f1bcf7cf5c62` | 216,007 | npm tarball |
| c | tree-sitter/tree-sitter-c | v0.24.1 | 83,057 | raw.githubusercontent.com |
| cpp | tree-sitter/tree-sitter-cpp | v0.23.4 (exists) | 147,611 | npm tarball |

Fetch notes: the sandbox HTTP proxy returned 403 for raw.githubusercontent.com
from shell python/curl; the session fetch tool retrieved rust, python, and c
intact but truncated kotlin, dart, and cpp at ~100 KB, so those three were
pulled as npm registry tarballs (registry.npmjs.org was reachable) and
JSON-validated. All six files parse as valid JSON. The kotlin/cpp npm tags
match the git tags by version number; the dart npm release maps to the git
commit above (repo-tag correspondence for dart is otherwise unverified — the
repo publishes no version tags on npm metadata beyond 1.0.0).

## §3 Per-language feature availability

"Slots" = field slots plus the sub-node spec (tree-sitter's `"children"` key), counted over named kinds.

| feature | rust | python | kotlin | dart | c | cpp |
|---|---|---|---|---|---|---|
| total entries | 280 | 217 | 262 | 316 | 275 | 407 |
| named entries | 169 | 128 | 134 | 187 | 132 | 213 |
| supertypes declared | 6 | 6 | **0** | 3 | 7 | 7 |
| named kinds with `fields` (role slots) | 73 | 49 | **0** | 30 | 64 | 98 |
| named kinds with a sub-node spec | 104 | 70 | 107 | 134 | 58 | 111 |
| leaf kinds (neither, no subtypes) | 26 | 21 | 27 | 32 | 27 | 39 |
| total slots | 262 | 165 | 107 | 199 | 187 | 312 |
| slots with both `multiple` + `required` | 262 (100%) | 165 (100%) | 107 (100%) | 199 (100%) | 187 (100%) | 312 (100%) |
| slots with non-empty input-kind list | 262 (100%) | 165 (100%) | 107 (100%) | 199 (100%) | 187 (100%) | 312 (100%) |
| distinct role names | 31 | 32 | **0** | 24 | 39 | 50 |

Supertype names per language:
- rust: `_declaration_statement`, `_expression`, `_literal`, `_literal_pattern`, `_pattern`, `_type`
- python: `_compound_statement`, `_simple_statement`, `expression`, `parameter`, `pattern`, `primary_expression`
- kotlin: none
- dart: `_declaration`, `_literal`, `_statement`
- c and cpp (identical sets): `_abstract_declarator`, `_declarator`, `_field_declarator`, `_type_declarator`, `expression`, `statement`, `type_specifier`

Top-10 role names (count = kinds using the role):
- rust: name 24, type 20, body 16, value 14, type_parameters 10, pattern 7, left 6, right 5, bounds 5, type_arguments 5
- python: body 13, name 10, value 9, left 7, right 7, operator 4, alternative 4, alias 3, type 3, consequence 3
- kotlin: (none — no field slots at all)
- dart: name 14, body 11, condition 6, alternative 3, consequence 3, parameters 3, value 3, arguments 2, left 2, operator 2
- c: declarator 13, type 13, value 12, body 12, name 10, condition 8, operator 6, alternative 6, argument 6, parameters 3
- cpp: declarator 21, name 19, type 19, body 18, value 14, operator 10, condition 9, right 8, parameters 7, left 7

## §4 Cross-language uniformity findings

1. **Arity and input types are 100% uniform.** Every one of the 1232 slots across all six grammars carries both `multiple` and `required` booleans and a non-empty allowed-kind list (per-language: 262/165/107/199/187/312, each 100%).
2. **Kotlin is the structural outlier: 0 supertypes and 0 field slots.** All 107 of its slots are anonymous sub-node specs, so it contributes no role names and no declared output supertypes at all.
3. **No role name is shared by all six grammars (intersection is empty, solely because kotlin has none), but 11 role names appear in ≥5 of 6:** alternative, arguments, body, condition, consequence, left, name, operator, parameters, right, value.
4. Supertype naming is not verbatim-uniform among the five grammars that have supertypes: `expression` recurs in 3 (python, c, cpp), `statement` and `type_specifier` in 2 (c, cpp), `_literal` in 2 (rust, dart); rust uses underscore-prefixed hidden names (`_expression`) where python/c/cpp use visible ones (`expression`). Semantic alignment (an "expression-like" supertype exists in rust `_expression`, python `expression`, dart — absent, c/cpp `expression`) needs a small manual alias table; dart notably has no expression supertype, only `_declaration`, `_literal`, `_statement`.
5. c and cpp declare byte-identical supertype name sets (7 each), confirming first-party family consistency.

## §5 Demo feature vectors (rust, python)

Format per kind: output supertypes; then per slot (role, `multiple`, `required`, input set collapsed to a shared supertype when every input kind belongs to one). Produced by `survey.py`; collapse note: a singleton input set is also collapsed when its one kind belongs to a supertype (e.g. rust `body: [block]` prints as `_expression` because `block` is an `_expression` sub-node) — the raw concrete set is retained in the data.

rust:
- `binary_expression` — out: [`_expression`]; slots=3: left (F,T, `_expression`), operator (F,T, 18 anonymous operator tokens), right (F,T, `_expression`)
- `if_expression` — out: [`_expression`]; slots=3: alternative (F,F, [else_clause]), condition (F,T, [`_expression`, let_chain, let_condition]), consequence (F,T, `_expression` ← concrete [block])
- `function_item` — out: [`_declaration_statement`]; slots=6: body (F,T, [block]→`_expression`), name (F,T, [identifier, metavariable]→`_expression`), parameters (F,T, [parameters]), return_type (F,F, [`_type`]), type_parameters (F,F, [type_parameters]), sub-node spec (T,F, [function_modifiers, visibility_modifier, where_clause])
- `call_expression` — out: [`_expression`]; slots=2: arguments (F,T, [arguments]), function (F,T, `_expression`)
- `identifier` — out: [`_expression`, `_pattern`]; slots=0 (leaf)

python:
- `binary_operator` — out: [`primary_expression`]; slots=3: left (F,T, `expression`), operator (F,T, 13 operator tokens), right (F,T, `expression`)
- `if_statement` — out: [`_compound_statement`]; slots=3: alternative (T,F, [elif_clause, else_clause]), condition (F,T, [`expression`]), consequence (F,T, [block])
- `function_definition` — out: [`_compound_statement`]; slots=5: body (F,T, [block]), name (F,T, [identifier]→`parameter`), parameters (F,T, [parameters]), return_type (F,F, [type]), type_parameters (F,F, [type_parameter])
- `call` — out: [`primary_expression`]; slots=2: arguments (F,T, [argument_list, generator_expression]), function (F,T, `expression`)
- `identifier` — out: [`parameter`, `pattern`, `primary_expression`]; slots=0 (leaf)

This is exactly the tuple the clustering machinery would consume: (slot count, per-slot (multiple, required), per-slot input-kind set collapsed to supertypes, output supertype memberships). Cross-language comparability of e.g. rust `binary_expression` vs python `binary_operator` is visibly strong: identical slot signature (3 slots, all F/T, left/operator/right).

## §6 Limitations and gaps

- Kotlin (fwcd, non-first-party) provides no supertypes and no field slots; role-based features are simply absent there, measured, not assumed.
- Dart (UserNobody14, non-first-party) has only 3 supertypes and 30 fielded kinds out of 187 named; most structure sits in anonymous sub-node specs (134 kinds).
- The dart npm 1.0.0 → git tag mapping is by commit hash only (`53485a8`); the repo's tagging practice is unverified. The ast-grep/tree-sitter-dart fork was not needed and was not fetched.
- Three files (kotlin, dart, cpp) came via npm tarballs rather than raw git because the fetch tool truncates at ~100 KB; version-string equality to git tags is asserted from npm metadata, byte-level identity to git is unverified.
- The supertype-collapse rule in the demo vectors over-collapses singleton sets (noted inline in §5).
- Counts treat the sub-node spec as one slot per kind; anonymous (unnamed) token types inside operator slots are counted as input kinds like any other.

## §7 Consumable today vs needs deriving

Consumable today, uniformly, from the shipped JSON:
- per-slot arity flags (`multiple`, `required`) — 100% coverage in all six;
- per-slot input-kind sets — 100% coverage in all six;
- output supertype memberships — directly for rust (6), python (6), c (7), cpp (7); partially for dart (3).

Needs deriving:
- kotlin output types entirely, and dart mostly: infer pseudo-supertypes by clustering input-kind co-occurrence (kinds that appear together in the same slots behave as one supertype) — the 100%-present input sets make this derivation well-posed;
- kotlin role names entirely: no field slots exist, so role-based features must come from positional/structural signatures instead;
- a cross-language supertype alias table (`_expression` ≈ `expression`, `_declaration_statement` ≈ `statement` ≈ `_statement`) — small, manual, five languages.
