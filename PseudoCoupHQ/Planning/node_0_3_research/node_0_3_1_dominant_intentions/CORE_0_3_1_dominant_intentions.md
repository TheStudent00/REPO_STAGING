---
id: hq.research.dominant_intentions
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: dominant_intentions
    path: Planning/node_0_3_research/node_0_3_1_dominant_intentions/CORE_0_3_1_dominant_intentions.md
super_node:
    name: research
    path: ../CORE_0_3_research.md
sub_nodes: []
---

# CORE 0_3_1 — dominant_intentions

## metadata

- **id:** hq.research.dominant_intentions
- **level:** 2
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [research](../CORE_0_3_research.md)

## sub_nodes

*(none yet)*

## definition

Empirical grounding of dominant intentions by RUNTIME equivalence,
so they stop being almost entirely by hand (the owner, 2026-08-13).

the owner's definition of record: intentions represent what developers
mean while using a language's features; a DOMINANT intention is an
object satisfying all sub-intentions, such that (once defined or
polyfilled in every language) it can hot-swap with its
sub-equivalent object in any language without disturbing functional
logic — the unused parts of the dominant intention are inert.

That definition is operationally testable (behavioral subsumption):
for every input in the sub-object's domain, the dominant and the
sub-object must produce the same result. So dominant intentions can
be ESTABLISHED BY EXECUTION — synthesized test vectors run through
each language's native object and the candidate dominant — with the
hand seeding candidates and ruling residue, exactly as in
kind_clustering.

## the standing shape

- **scope: the 12 target languages** (not the 411): runtime analysis
  needs installed toolchains. Swift EXCLUDED for now (the owner,
  2026-08-13) unless the container install lands; 11 active.
- **relation to kind_clustering (the co-node)**: that line measured
  FORM and located its boundary — intentions are mostly
  shape-invisible (PCHQ log_015 V2). This line is the instrument
  for the far side of that boundary; kind_clustering supplies the
  syntax-side anchors.
- **designed precedent, not from scratch**: PseudoIR's Tier-1
  registry (`<WORKSPACE_DIR>/PseudoIR/pseudoir/registry/data/ops.json`
  — "id, signature, semantic test vectors, per-language columns...
  filled by the probers") is this architecture at operator level;
  this node scales it to objects.
- **runner**: the Airlock agent lane
  (`python3 <WORKSPACE_DIR>/Airlock/airlock submit ...`, `airlock status`);
  results as data.
- **start: basic data structures**, two-level per the 2026-08-13
  discussion — the machine basis {fixed-width integer, IEEE float,
  address} where featureless is actually true, and the unanimous
  high-level costumes over it, seed order: boolean, float
  (machine-identical calibration case), integer (the deepest
  costume fracture: bignum vs fixed vs float-only), string (a
  composite wearing one name), list, then dict. Fracture points ARE
  the test vectors.

## support

- [SUPPORT_BRAINSTORM_basis_data_structures.md](SUPPORT_BRAINSTORM_basis_data_structures.md) — the two-level
  basis list this node measures against: level 0, what the machine
  itself has, closed; level 1, the composites built on it, proposed
  2026-08-13 and since ruled by the owner.

## plan (draft, walking slowly at the owner's pace)

0. inventory — what exists: ops.json rows and prober state; which
   toolchains run in the container today. measurement only.
1. harness design — vector synthesis, per-language runners, the
   equivalence report format.
2. data structures — the seed list above; verify/tweak by hand at
   the end (the owner: unavoidable, and correctly last). DONE 2026-08-14
   (census verified, corrections ruled).
3. **GRADUATED 2026-08-14 to its own co-node,
   [kind_fuzzing](../node_0_3_2_kind_fuzzing/CORE_0_3_2_kind_fuzzing.md)**
   — the owner named it ("to cluster kinds using an automated fuzzer")
   and it carries the full design. This node's contribution to it
   is the INSTRUMENTS: the verified six dominants are the known
   inputs every probe is measured against. Summary kept here for
   readers who stop at this page:
   "establish the basic data structures so that we can fuzz the
   rest of the vocabulary. without having to have a corpus. we
   generate the scripts based on vocab tokens (that we know what
   it wants for input and its output type) in order to observe how
   it processes data structures. and then use those changes to
   cluster across languages."
   - **the method**: for each vocabulary token, GENERATE a minimal
     script applying it to known inputs; the known inputs are the
     six verified dominants. Run it. Record the answer, the raise,
     or the compile refusal — that triple is the token's BEHAVIOR
     SIGNATURE. Cluster signatures across the 11 languages: the
     rest of the vocabulary discovers itself, and a token matching
     nothing is genuinely private to its language.
   - **why phase 2 had to come first**: an output is only readable
     if the input is known exactly. `+` answering
     9223372036854775808 is a bignum, a wrap, or a float that lost
     precision — distinguishable only because integer's page now
     says, verified, what each language's integer IS. The
     dominants are the calibrated instruments.
   - **where the vocabulary comes from**: the grammar supplies
     OPERATORS (anonymous tokens — 115 in rust) and KEYWORDS for
     free. It does NOT supply builtins (`len`, `push`, `map` are
     library names, not syntax) — those need a small separate
     per-language harvest (stdlib reflection or a hand list of the
     core few).
   - **the engineering crux, before anyone builds it**: in typed
     languages one bad probe kills the whole program, so probes
     cannot simply be batched into one file; and one compile per
     probe is unaffordable (kotlinc ~1 min; thousands of probes).
     Fix: BISECT — compile a batch, on refusal split and recompile;
     valid probes cost log-many compiles and each refusal isolates
     to its exact token, which is the measurement wanted anyway
     (compile-refusal is a first-class camp answer as of
     2026-08-14). Scale: ~40 binary operators x ~36 operand
     pairings ~ 1,400 probes per language.
   - NOT designed yet — phase 3 opens with its own brainstorm at
     the owner's pace. The harness
     (`Research/dominant_intentions/harness/`) is its skeleton:
     same vectors → runners → lane → compare pipeline, with
     GENERATED probes replacing hand-written ones.
