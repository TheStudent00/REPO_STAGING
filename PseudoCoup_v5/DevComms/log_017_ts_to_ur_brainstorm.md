The `ts_to_ur` open questions, in weight order. Everything else in the ledgerer was settled by walking; this node has six genuinely open ones — some with rulings nearby, some untouched.

**1 — The rust map itself.** The mapper's heart is the ts_kind → ur_kind table for rust: 163 rows. log_008 drafted it, and your later rulings (coupled, the three constructs, the three form buckets) resolved the five uncertain families — but *nobody has applied those rulings back to the 163 rows*. The table needs one ratification pass to become the mapper's data. Related, mostly settled: the map is *data* (a table the census can check for totality against the grammar), with thin code executing it — your log_002 §8.2 lean, never formally ruled.

* is this related to (6)?
  * **answer (Claude, 2026-08-06): yes, member-to-container.** the
    ratified rust map is the largest single item INSIDE the language
    pack; (6) is the spec of the container. separable in time — the
    map can be ratified today — but ruling (6) first says where the
    map file lives and what sits beside it.



**2 — Anonymous nodes, the sleeper.** Ids count anonymous tokens (`{`, `,`, `->`) — that's constitutive, from idgen. But do they each become a `ur.Node`? The corpus numbers make this real: 544k total nodes, 304k named — so **~240k anonymous nodes, 44% of everything**. Materialize them all and the UR tree nearly doubles for tokens that carry no intention; skip them and child *positions* must still count them or every id breaks. Middle paths exist (count positions, materialize only named, keep the anon info recoverable from spans) but each has a cost, and this decision shapes the mapper's inner loop more than any other.

* these anonymous token nodes depend on their neighboring nodes, very compressible -- so i would think that we could have language specific sub-graph stencil pattern for each.

* not sure how that manifests in the ledger. perhaps its some kind of an origin language class instance attribute of the ledger. more meta-data than data.

* thoughts?
  * **answer (Claude, 2026-08-06): the instinct is right and goes one
    step further — per-instance, ZERO anonymous storage may be
    needed.** three facts stack: (1) the id freezes the positional
    arithmetic at mint time — the mapper walks the REAL tree-sitter
    tree when minting, so child indices count anon tokens then, and
    after that moment the count is baked into the id; (2) the
    retained bytes recover exact text including which operator sat in
    a span gap — substrate-plus-bytes is already lossless; (3) the
    stencils (per-kind patterns of where `(`, `,`, `)` must sit) are
    grammar facts and belong exactly where the owner's second bullet put
    them: META-DATA in the language pack (question 6), used for
    validation and census, never stored per row.
  * so the ledger manifestation is NOWHERE per row: rows simply never
    contain anon nodes; the pack carries the stencil table.
  * caveat kept visible: not every anon token is stencil-determined —
    the operator in a `binary_expression` varies by instance (`+` vs
    `*`). its identity lives in the bytes, recoverable; if a consumer
    wants it structurally, the mapper lifts it into one `semantic`
    slot (`operator: "+"`) — a cheap escape hatch, not a redesign.



**3 — Macros at mapping time — the biggest cluster.** Your sequencing says step 1 delivers "kinds one and two *expanded*." So the mapper (or a co-writer beside it) must do four things whose boundaries are undrawn: mark each `token_tree` opaque (ruled); re-parse contents under the per-macro shape table (log_010: 20 shapes → 83%, and a seventh "match-arm-pattern" shape would close most of the 17% — table unratified); run the kind-one engine (`macro_engine.py`, pulled into ledgerer scope) producing `GeneratedOrigin` sub-trees; and mint sub-addressed ids for injected nodes (ruled yes in principle — the *concrete spelling* of the sub-address is unpicked, and log_010's finding applies: offsets need the arithmetic remap, not `included_ranges` alone).

* macro_engine.py is Rust specific isnt it? also does it use tree-sitter? and i want to caution the acceptance of components that exist from failed project versions -- which is almost every project in Programming due to LLM drift.
  * **answer (Claude, 2026-08-06), measured against the file
    (`PseudoCoup_v5/Research/macro_engine.py`, 259
    lines):**
    - rust-specific: the MECHANISM is, deliberately — it implements
      macro-by-example (pattern + template + `$` metavariables),
      rustc's kind-one semantics. the engine is data-driven (macros
      as data) but the matching rules are Rust's. kind one is a Rust
      classification, so this is fitting, not accidental.
    - tree-sitter: NO — `import re` is its only import; it carries
      its own tiny lexer and bracket-grouper. integration question
      this raises for the mapper: at ingest it should probably
      consume the token_tree the parse already produced rather than
      re-lexing text. noted for the walk design.
    - provenance: NOT from a failed version. header reads "Written
      2026-08-02" — during THIS campaign's macro study (the logs
      003-005 stretch), with its two found-while-writing bugs kept
      as comments where they bit. the caution still applies in a
      softer form: it is research-grade prototype, so the treatment
      is the same as every harvest source — take the DESIGN (proven
      feasible at 259 lines), write the plan-conformant version
      fresh when the expansion writer is built. nothing transplants
      as-is.



**4 — The error files.** 5 of 111 corpus files carry ERROR nodes (nightly `decl_macro` syntax the stable grammar rejects). Three recorded options, none ruled: refuse those files honestly; admit them with the ERROR stretches as opaque nodes (the refusal posture applied to form — consistent with everything else); or patch the grammar, which log_002 called the cheap fix *because the pin is already ours*. This decides whether `TryFromU32`'s definition file is ingestible.

**5 — Pinning and census, one ratification.** Everything's designed, nothing's ratified: `ts_to_ur` as owner of the vendored pinned grammars, the runtime pin check (`semantic_version` against the manifest), and the census discipline — unknown kind at ingest → refuse, or WFL-style justified baseline. One yes makes it plan.

**6 — What a language pack *is*.** The per-language sub-module's shape, concretely: presumably {pinned grammar, the kind map, the query files, the macro shape table, the census baseline} — all data — plus nothing per-language in code. Saying so explicitly is what keeps language two cheap.

My read on order: 2 and 3 are the real design conversations (they shape the code); 1, 5 are ratifications of work already done; 4 is one ruling; 6 falls out of the others. The natural move is a log_002-style brainstorm for this node opening with the anonymous-nodes numbers and the macro pipeline — want me to draft it, or walk them here one at a time like we did for the ledger?
