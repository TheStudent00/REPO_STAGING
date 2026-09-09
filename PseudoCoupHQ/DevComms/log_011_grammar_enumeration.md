# log_011 — grammar enumeration survey (kind_clustering step 1)

Date: 2026-08-12. Author: enumeration agent, for the owner.
Node: `Planning/node_0_3_research/node_0_3_0_kind_clustering/` — plan of record step 1 (measurement only, no clustering).
Artifacts: `Research/kind_signature_clustering/grammar_inventory.json`, `Research/kind_signature_clustering/raw_all/` (411 node-types.json files; the original `raw/` five untouched).

## §1 headline numbers

- **415** unique grammars (deduplicated by language name) enumerated across three sources.
- **389** grammar repos ship `src/node-types.json` at HEAD (93.7% of the 412 reachable repos).
- **411** node-types.json files fetched — every one that exists, no bandwidth cap was needed (multi-dialect repos contribute more than one file, e.g. typescript/tsx, ocaml x3).
- **23** repos have no committed node-types.json; **3** repos are unreachable (deleted/renamed).
- **31,858** named kinds total across the fetched files (62,610 entries counting anonymous).

## §2 sources used and overlap

All three planned sources were used. The GitHub API was blocked by the sandbox proxy, so org enumeration fell back to the orgs' public repository HTML pages (paginated) plus the wiki — as the tasking permitted. Probing/fetching went through `git clone --depth 1 --filter=blob:none --no-checkout` + `git ls-tree`/selective checkout per repo (github.com was reachable), which is strictly more reliable than raw HEAD fetches: it finds node-types.json at any path in the tree.

| source combination | grammars |
|---|---|
| wiki only | 301 |
| tree-sitter-grammars org + wiki | 76 |
| tree-sitter org + wiki | 26 |
| tree-sitter-grammars org only | 5 |
| tree-sitter org only | 4 |
| both orgs + wiki | 3 |

The wiki is near-complete (406/415); the two orgs contribute only 9 grammars the wiki misses. Six wiki grammars live in repos not named `tree-sitter-*` (RubixDev/ebnf, kristoff-it/superhtml, kristoff-it/ziggy, slint-ui/slint, vlang/v-analyzer, winglang/wing) and were caught by hand.

## §3 category breakdown

Tags are MINE (provisional, keyword/judgment-based; the owner may re-rule). Rules used: general-purpose = languages whose programs are arbitrary computation (incl. shells, hardware description); query = languages whose programs are questions against a store (SQL family, GraphQL, datalog); markup = document/template structure (HTML, markdown, template engines, doc-comment grammars); config = declarative settings/build/data files (yaml, dockerfile, muttrc); notation = formal notations that are neither programs nor documents (regex, grammars-of-grammars, assembly, diffs, proof-adjacent syntax); dsl = domain-restricted programming (shaders, smart contracts, IDLs, workflow languages); other = non-grammar repos that leaked through enumeration or unclassifiable.

| category | count | with node-types.json | example languages |
|---|---|---|---|
| general-purpose | 120 | 116 | rust, python, ada, hoon |
| config | 97 | 91 | yaml, dockerfile, nix, muttrc |
| dsl | 63 | 60 | glsl, solidity, bicep, typespec |
| notation | 57 | 55 | regex, ebnf, x86asm, diff |
| markup | 51 | 47 | html, markdown, latex, jinja |
| query | 23 | 19 | sql, graphql, sparql, kusto |
| other | 4 | 1 | cyberchef, eventrule |

## §4 quality-signal distribution

Per fetched grammar file (n = 411). Role coverage = fraction of named non-supertype kinds that have sub-node slots (`fields` or `children` present) and carry at least one `fields` role.

| signal | distribution |
|---|---|
| role coverage | zero: 104 · (0, 0.25): 107 · [0.25, 0.5): 86 · [0.5, 0.75): 94 · [0.75, 1]: 20 — median 0.234 |
| supertype presence | absent: 293 (71.3%) · 1–3: 46 · 4–8: 58 · 9+: 14 (max 33) |
| arity discipline | **100% everywhere** — all 411 files carry `multiple` + `required` on every slot; zero exceptions, format guarantee confirmed |
| named kinds per grammar | median 52, min 3 (sxhkdrc-class), max 614 (systemverilog) |

**The kotlin-like zero-role convention is common: 104 of 411 grammars (25.3%) declare no `fields` at all** — every sub-node slot is a bare `children` collection. It is concentrated outside general-purpose languages: markup 44.0% zero-role, query 42.1%, config 33.7%, notation 30.5%, dsl 16.1%, general-purpose 11.2%. Kotlin is not an outlier; it is the low end of a large convention band. Supertype declaration is even sparser (28.7% of grammars have any), which matters for the hold-out validation frame — only ~118 grammars can self-referee.

Per-category medians: general-purpose median role coverage 0.431 / supertype presence 45.6%; query is the worst-instrumented category (median role coverage 0.082).

## §5 clustering population size

31,858 named kinds across 411 grammar files (vs ~800 at 5 languages in log_010 — a ~40x scale-up). Non-named entries add another ~30k anonymous kinds but those are leaf punctuation/keywords and out of scope. The dense-matrix approach is dead at this size (31,858² ≈ 1.0e9 pairs); step 3's sparse per-kind top-k spectrum is mandatory, as the plan of record already says. Decision-6 (output positions as counts) becomes more urgent: the saturation measured at 5 languages will compound heavily among the 104 zero-role + low-coverage grammars, whose kinds expose very few distinguishing features.

## §6 gaps and caveats

- **Proxy fallback**: api.github.com and raw.githubusercontent.com were blocked; used org repo HTML pages + wiki for enumeration and git clones for content. No API rate-limit issues as a result; star/activity metadata was consequently NOT collected (the ~150 activity cap was moot — all 415 were probed).
- **Unreachable repos (3)**: dannylongeuay/tree-sitter-go-template, PasiSalenius/tree-sitter-http, amaanq/tree-sitter-rec — clone fails with not-found; likely deleted or renamed since the wiki was written.
- **No node-types.json (23)**: incl. groovy, wgsl, sql (m-novikov), cobol, scilab, pod, razor — some genuinely don't commit generated files; a scaled run could regenerate via `tree-sitter generate` if those languages matter.
- **Multi-dialect repos (15)** handled: asciidoc, cfml, chatito, csv, hcl, markdown, ocaml, php, sfapex, stan, typescript, wasm, xml, yaml, ziggy — each dialect stored as `<name>__<dialect>.node-types.json` and recorded as a separate grammar entry under one repo record.
- Dedup is by repo-name-derived language name; competing community grammars for the same language (wiki lists several) collapse to one canonical repo (org repos preferred). The inventory keeps `sources` so alternates can be revisited.
- Category tags are single-judgment; borderline cases abound (prolog→general-purpose, souffle→query, stan→dsl, zsh→general-purpose). Flagged as provisional throughout.

## §7 recommended probe list for the scaled run

Per the CORE, full population always: ingest **all 411 fetched files**, tagged by category, report per category. Within that, two tiers worth distinguishing when tiering-by-quality comes up for explicit ruling:

- **High-instrumentation tier (44 grammars)** — role coverage ≥ 0.5, supertypes present, ≥ 60 named kinds: apex, arduino, c, cedar, cfml(cfscript), cpp, cuda, enforce, erlang, gdscript, gdshader, glimmer-javascript/-typescript, glsl, go, haskell, hlsl, ispc, jakt, javadoc, javascript, kcl, modelica, nqc, ocaml (x3), qmljs, re2c, ruby, rust, scala, sdml, slang, sourcepawn, sway, systemtap, tact, templ, typescript + tsx, typst, wing, xquery. These are the natural hold-out referees (their own supertype declarations are rich) and should anchor the merge-tree spectrum.
- **Everything else** enters as population; the 104 zero-role grammars are exactly where decision-6 count-features must carry the load, so they double as the stress test for step 2.
- The 12 transpilation targets remain in regardless of tier.

All raw material is already local under `Research/kind_signature_clustering/raw_all/` — the scaled run needs no further network.
