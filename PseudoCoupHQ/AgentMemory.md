# AgentMemory — PseudoCoup line

**Session handoff active (2026-08-13):** the working plan for the
next days is `DevComms/log_018_handoff_plan_2026_08_13.md` — read
it before starting work; it names the work packages, the reserved
decisions, and this week's failure modes.

Created 2026-08-12 at the owner's instruction, after a session-compression
loss ("I don't have the ratified list of the 12" — the list was never
lost, it was never loaded). This file holds what must be loaded to
work correctly AT ALL on any PC repo. It is durable understanding,
not a log (§18a's three stores: plan nodes say what a thing IS,
DevComms logs say what happened on a day, THIS says what an agent
must know before either).

## the 12 languages (ratified since ~PCv0/v1, unchanged)

python, typescript, java, csharp, go, rust, ruby, php, kotlin, cpp,
dart, swift

- source of record:
  `PRIVATE/PseudoIR/pseudoir/registry/data/xforms.json`
  (`"languages"` key; ops.json carries the same per-language
  columns).

## the vision (the owner's words, recorded 2026-08-05)

The Hub is the center of intention: all intentions of the 12
languages are contained within it (compiler slices transpiled into
the Python hub). The ledger's job is INGRESS infrastructure —
lossless, faithful multiple-round-trip transpilation through all 12
and back. The reconstruction oracle is built into the objective:
source → ledger → equivalent source → ledger → identical equivalent
source. "Faithful convergence" (the owner's name): first pass normalizes
to canonical form, every later pass is a fixed point. Ingress into
the Hub was the key objective, not egress.

## current focus

PCv5 `pcv5.tools.ledgerer` deep dive. Development order ruled:
ur → ledger → ts_to_ur → ur_to_ledger → builder. ur.py, ledger.py,
ts_to_ur.py written and test-verified (17/17, 2026-08-12).
PseudoIR and PCv6 changes are DEFERRED by recorded ruling.

## standing rulings an agent must not re-litigate

- the owner decides architecture, ontology, naming. Flag, don't decide.
  Work only at the depth the owner has opened.
- BANNED vocabulary everywhere (prose, code comments, generated
  docs): parent/child/children/sibling/ancestor/descendant/orphan.
  Use super-node/sub-node/co-node/sub-tree/unlinked.
- Every entry in a ledger is a `ur.Node`. No source copies anywhere;
  content lives on nodes (`text`), form in the pack's tables.
- Token tables are GRAMMAR-AUTHORED (the pinned grammar.js is a
  closed enumeration); the compiler INFORMS AND VERIFIES (staleness
  diff, empirical stencil recovery, compile-as-oracle); a corpus is
  test material only. (Rulings of 2026-08-11/12; PCv5 logs 018-019.)
- Mirror tree-sitter's pin; pin bump before compiler fallback.
- Refusal posture: refuse by name, never silently; UNRESOLVABLE is
  a value; unknown kind refuses.
- cranelift is BANNED (`PRIVATE/PseudoCoupHQ/CRANELIFT_IS_BANNED.md`).
- `SUPPORT_BRAINSTORM_` / `SUPPORT_FUTURE_` filename convention for
  stage visibility (2026-08-12; PlanPlan
  `Planning/SUPPORT_FUTURE_stage_labels.md`). `.archive/` stays as
  is; VCS is the ultimate archive.

## where things are

- planning framework of record:
  `PRIVATE/PlanPlan/framework/PROTOCOL.md`; conformance sweep:
  `bash PRIVATE/PseudoCoupHQ/hq.sh check`.
- intentions vocabulary (11 objects + categories A-J):
  `PRIVATE/PseudoIR/Tools/intentions/pc_intentions.json`;
  minimum-set argument: `.../minimum_intention_set.md`.
- PCv5 ledgerer code: `PRIVATE/PseudoCoup_v5/Tools/ledgerer/`
  (ur.py, ledger.py, ts_to_ur.py, test_ts_to_ur.py); research
  scripts: `PRIVATE/PseudoCoup_v5/Research/`.
- pins: tree-sitter==0.26.0, tree-sitter-rust==0.24.2.
- session records: per-repo `DevComms/log_NNN_*.md`; PCv5 state as
  of 2026-08-12: `PseudoCoup_v5/DevComms/log_020_session_state_2026_08_12.md`.
- sandbox/toolchain: `PUBLIC/Airlock` since 2026-08-22, derived
  from `SandboxDesign` (which still works and is not
  retired, but shares container names, so never run both at once).
  Way in: `python3 PUBLIC/Airlock/airlock submit <lane.sh>
  --batch <label> --weight <n>`, then `airlock status` (`watch` to
  refresh) and `airlock doctor`. `bash PUBLIC/Airlock/progress.sh`
  still exists and still works (`-w` refreshes). Underneath, the file
  protocol is unchanged: write `agent/drop/x.sh`, poll `agent/status/`,
  read `agent/logs/`, collect `agent/out/`; container has Rust 1.96.1.
  Migration record:
  `PRIVATE/PseudoCoupHQ/DevComms/log_060_sandbox_to_airlock_migration.md`.

## the kinds vocabulary rulings of 2026-08-12 (basis-report walk)

- objects gained `import`, `try`, `pair`, `interpolation`; forms
  gained `container-form` (evidence: PCHQ logs 014–015; walk:
  log_016). Python-naming rule: no universal claim → Python's word.
- classification is TWO-LAYERED: shape (grammar evidence, mapped
  now) and intention (resolution, layered later). A/B/C/E/G/H/I are
  shape-invisible ecosystem-wide — ledger-resolved facts.
- sum types refuted as a shape; record-dual-choice stands on data.
- mapping strategy split (P9): roled grammars via clusters;
  zero-role/outliers (kotlin, ruby, c-sharp) via counterpart+name
  evidence.

## the research node's three lines (as of 2026-08-14)

`PCHQ Planning/node_0_3_research/` holds three co-nodes. All three
are CLUSTERING lines; they differ in their evidence:

- **kind_signature_clustering** (was `kind_clustering`) — clusters
  kinds by DECLARED SIGNATURE (arity, slot types, supertypes), 411
  languages. Done through step 4 + the rust pack generator.
  Artifacts renamed to match, 2026-08-15: now `Research/kind_signature_clustering/`
  (the folder was `kind_clustering`, directly under `Research/`), via
  PlanPlan's new `rename_node.py`.
- **dominant_intentions** — the six basic data structures verified
  by execution across 11 languages (the calibrated INSTRUMENTS).
  Seed tier complete, zero contradictions.
- **kind_fuzz_clustering** — clusters the SAME kinds by MEASURED
  BEHAVIOR: a generated script per kind against those instruments,
  no corpus, then relate (nests/overlaps/contradicts) and cluster.
  Founded 2026-08-14; phase 0 is kind extraction + probe-space size.

The two kind lines are mutually checkable: agreement is strong
evidence, disagreement is itself a finding.

**THE THREE-LAYER ANCHOR (the owner, 2026-08-15 — every research work
package must state which layer it serves):** layer 1 DATA (static
content, no language, no dynamics — seven forms + nesting +
identity marks, ruled complete-for-content, behavior excluded);
layer 2 REPRESENTATION (how a language holds that content — one
datum, several representations per language); layer 3 OPERATION
(what the COMPILER can do to a representation — the measured
dynamics, never builtins). Home: `node_0_3_0_4_data_representation`
(owns 1+2; layer 3 is kind_fuzz_clustering's). The census pages
are re-read as layer-3 measurements of specific layer-2
representations. `type_vocabulary` (node_0_3_3) is SUPERSEDED —
its union is raw reference only; the 59-row ruling was cancelled.
Lesson recorded: Opus's step-A drift happened because no purpose
anchor existed for phases to answer to; this anchor is the fix.

## communication — load-bearing, re-read EVERY session (2026-08-24)

- `PRIVATE/DevComms/LLM_communication_protocol_v2.md` is the
  protocol of record (refactored 2026-08-24; v1 preserved beside
  it). Read it at session start and hold it every turn, alongside
  this file. the owner has had to demand this repeatedly; each repeat
  burns his money and trust.
- The failure mode that keeps recurring: naming a mechanism I built
  ("the join", "the sem form", "re-key") as if the owner holds my private
  meaning, then describing around it. The fix is not defining the
  term on request — it is SHOWING the thing: the actual lines, the
  actual rows, the two lists side by side, before any word refers
  to them. When the owner flags one phrase, the instruction is to
  re-express EVERYTHING at that register, not to explain the one
  phrase.
- Plain words beat coined terms: "the map" (static graph), "the
  tally" (coverage counts), "the diary" (execution-order trace,
  not yet built). Coin a term only with a glossary entry and its
  contextual example.

## the operator-equivalence pipeline (RATIFIED by the owner, 2026-08-24)

Home: Planning/node_0_3_research/node_0_3_1_operator_equivalence (the
ratified-pipeline section) and logs 072/073. The steps, in order:

1. probe generation from the grammar's operator vocabulary ×
   holder types, gated by COMPILE-OR-REFUSE — the compiler's own
   type checker is the acceptance oracle; refusal text recorded.
2. every probe compiles TWICE: ANCHOR (optimizer off — clang -O0,
   rustc opt-level=0, go -N -l, swiftc -Onone) and SHIP
   (optimized). Identity is established at the anchor (name ->
   memory home, stated by the compiler's debug table); matching
   happens on ship; the anchor/ship DIFF carries identity across.
3. arch-unit extraction (objdump, one notation).
4. argument identity anchored (DWARF at anchor + forced probe +
   route detour as independent grounds).
5. normalization (canon + lifted sem with anchored operand ids).
6. match by byte/sem identity — spelling is a LABEL, never a key.

**THE CANONICAL RUNNABLE FORM (ratified by the owner, 2026-08-25).**
Normalized units are RUNNABLE machine code, not formulas: registers
renamed to the standard — a -> %rdi(/%edi, float %xmm0),
b -> %rsi(/%esi, float %xmm1), result -> %rax (float %xmm0),
temps -> %r10, %r11. The C calling rule promoted to canon, so
c/cpp/rust/swift units are already canonical; go is renamed.
TRACED-VARIABLES-PRIORITY: a traced variable owns its designated
register; an untraced occupant is evicted to a temp; two values
never share a register silently; temps exhausted -> loud refusal.
Level 1 matching = byte identity after canonicalization (stronger
than formula-text match: still bytes, and executable — the probe
judge applies directly). The lifted formula remains what it is:
the proof checker's input, one level up. Level-2 (z3-proved,
deduction over bit arithmetic) edges ARE class-forming, with the
class's weakest-evidence marker saying so. RESULT TYPE is part of
every class key (operand types alone let bit-coincident units of
different result types merge — the empty-core defect of
2026-08-25).

**AMENDMENT: MOVES ARE ERASED BY SUBSTITUTION (the owner, 2026-08-26).**
A pure move (`mov` that only re-parks a value) is each compiler's
bookkeeping for its own calling rule, not computation. The sound
operation is DELETE-AND-SUBSTITUTE as one act: erase the move AND
rewrite every downstream read of the destination to the value's
name — never bare deletion (deleting `lhs = a` while the body still
says `lhs` severs the flow; the owner's example). The canonical record
becomes: the move-erased form (values named a/b/answer) PLUS the
entry contract (where each value must arrive — the default is the
designated registers; an instruction-pinned unit declares the pin,
e.g. `cltd` requires a in %rax). Runnable text is DERIVED on
demand: value-here + needed-there produces the adapter mov by
rule, in either direction; for c it regenerates exactly what its
compiler wrote. This replaces canon.py's refusals ("pinned to
%rax", "modifies an argument in place", the cross-block rename
refusal where the block's reads are substitutable) — 90 of 1,779
units, 58 of go's 107, fall back to the lifted string today for
want of exactly this. The lifted (pyvex) form already does the
substitution (its expressions say in0/in1, never a parked
register), so meaning-level matching was always sound; the gap was
only the runnable-text renamer. NOT YET IMPLEMENTED — see the
compiler_graph node's PROGRESS for the work list.

**THE CANONICAL FORM IS ENFORCED (the owner, 2026-08-26, after the
log_074 audit found matching 75% byte-ground / 23% non-runnable
notations and only ~2% canonical text).** the owner's canonical form,
his words: normalized arch opcodes; standardized designated
registers for traced variables AND all others; each call on its
own line; arch-units runnable with their standardized and
normalized context. Ratified elaborations: the entry contract's
adapter movs are part of the standardized context (own lines);
branch labels normalized positionally (L0.. in address order).
ENFORCEMENT: the canonical form is the HOME REPRESENTATION —
the default material for matching, analysis, AND presentation.
Erased units re-rendered as instructions ARE canonical; the
pseudo-step notation (u0 = cltd(a)) is retired to comments only.
Tools may transform (lift, z3-simplify, e-graphs) ONLY with a
RETURN PATH: a valid simplified expression is rendered back into
canonical runnable instructions; a result that cannot return is
an intermediate, not a result. Every stored unit representation
carries its canonical text; every report shows canonical text.
Prior grounds are kept (accumulate ruling) but the canonical
text is the primary material and the presented one. This ruling
was preceded by silent drift — matching was built on bytes and
lifted strings while the ratified form sat unused; that drift is
the failure mode this paragraph exists to prevent recurring.

**A PROVED UNIT IS A COUNTED UNIT (the owner, 2026-09-01).** Gate-proved
convergence advances the recorded count in the same lap,
automatically — never ask permission per round; asking was the
bookkeeping's invention, not the owner's. The withdrawn units remain
the one separate population, because withdrawal is an evidence
event. Every report states the single authoritative count with
its population line ("converged N of 1,779, compiled five;
withdrawn listed separately").

**THE MEMORY-WRAPPED FORM + THE PROVENANCE LEDGER (the owner,
2026-09-02, supersedes the scratch-register rewrite).** the owner's
words: "keeping the arch-unit usage of registers as is but with
our insertion of loading from memory … we get the consistent
symbolics for z3 and a functioning arch-unit." RULED: (1) the
compiler's body is kept VERBATIM — its register use is
compiler-proven conflict-free and is never renamed; a
standardized prelude loads inputs from ledger blocks into the
registers the compiler expects (arrival contract), a standardized
epilogue stores the compiler's result register to OUT-0; (2) the
ledger lives at an ABSOLUTE address — no register is ever
reserved as a region base (round 9's %r15 anchor is superseded;
its four refusals were self-inflicted); (3) ledger rows carry
PROVENANCE — kind, type, value-at-run, PRODUCED BY, OPERANDS —
for every value including temporaries and guard outcomes: the
ledger IS the dataflow graph as a table; (4) the z3 form is a
transcription of the ledger from OUT-0 downward, and the census
of unmodelled operations is the filter "rows whose producer has
no term" — no instruction-sequence mining; (5) the fixed-rule
re-render is the TEXTUAL NORMALIZER applied after proof, never the
only route to a text. Seven layers of record: original,
context, arrival contract, wrapped unit, ledger-transcribed z3
form, normalized re-render, the proof, the pool. Briefs: log_142.

**ROUND 10 RULINGS (the owner, 2026-09-02, after the round-10 audit,
log_150).** (1) THE POOL MERGES ON THREE GROUNDS: layer-5 text
identity (proved terms only), proved edges, AND layer-3
wrapped-text identity — identical wrapped text is identical bytes,
equivalence by construction; the brief-strict two-ground count
(8,140 vs 5,274) is recorded, not used. (2) THE LEDGER GETS TWO
MORE BLOCK KINDS, STACK and X87 — push/pop (4,298 rows) and the
x87 compare pairs (1,072 rows) are lineages the form lacked.
(3) IMPLICIT DESTINATIONS are per-opcode rules in ledger47
(idiv/div/mul/one-operand imul write unnamed registers; cltd/cqto
make rows); an unconditional jmp is never a flag reader.
(4) BRANCH LABELS ARE POSITIONAL (`L0..` in address order) in the
wrapped text — already ruled for the canonical form, now binding on
layer 3. (5) EVERY ARTIFACT THE PIPELINE READS IS WALKED BY THE
UNMODIFIED GUARD: no `role: generator provenance` on any file that
feeds grouping; producers are typed objects `{kind, mnem}` (log_147
§13's shape) — task 47's canon37 files failed this with 579 places
in c alone (log_150 §3). (6) AIRLOCK: keep all ten names from
log_138; serial execution stays (no `workers` key) — a trickle
jams only its own instance, so the convention is ONE INSTANCE PER
TASK, and `down` REFUSES while a lane's status is `running`
(`--force` overrides); the default agent tree for a non-default
instance moves OUTSIDE the checkout to `<runs>/<name>/agent`;
`daemon_file` is dropped after the next image build. the owner: "idc as
long as it works for you … if its a problem we can revisit."
Briefs: log_151.

**THE PLAN TREE GOVERNS THE PIPELINE (the owner, 2026-09-03: "we have
completely drifted away from the use of PlanPlan. unacceptable …
plan out every fucking step").**
`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_operator_equivalence/`
now has nine ratified level-3 nodes —
probes, arch_unit, canonical_form, ledger, reference, gate, term,
pool, guard — and 31 level-4 nodes, each with designation,
definition, §2-form design, settled rules with decision sources, and
a realization table naming the files on disk. RULES: (1) a round is
"code the nodes whose PROGRESS says planned"; (2) code carries the
node's name (canonical_form.py, ledger.py, reference.py, gate.py,
term.py, pool.py, guard.py) — the canon*/gate48/layer4* names are
superseded records; (3) a shape the tree lacks is added to the tree
FIRST (PROTOCOL §2), never to an artifact alone; (4) no "open call"
reaches the owner unless it is ontology or naming — implementation choices
are decided against the tree by the coordinator, and a question
already answered in AgentMemory or a CORE is not a question (the
2026-09-03 `call`-producer error). (5) A `call` into the compiler's
OWN runtime (libgcc / compiler-rt: __divti3 family) is IN SCOPE and
followed — the owner: "if its within the compiler, its not a library call";
the "out of scope" note of 2026-09-03 is superseded, its 308-unit
list stands. Render:
`python3 PRIVATE/PlanPlan/framework/render_plan.py PRIVATE/PseudoCoupHQ/Planning -o PRIVATE/PseudoCoupHQ/DevComms/renders/plan_<date>.html`.

**THE VIRTUAL-MEMORY FORM — SEE LOG 141 (2026-09-02).** The full
saved understanding, accepted by the owner, lives in
`PRIVATE/PseudoCoupHQ/DevComms/log_141_virtual_memory_form_explained.md`.
Two additions over the refinement below: (1) NO CONTIGUITY
ASSUMPTION — blocks are addressed through a LEDGER (an array of
block base pointers, fixed order IN/CONST/TEMP/OWN/GUARD/OUT, one
known base), two-step addressing (load ledger entry -> load row),
so blocks may live anywhere and the text names nothing about the
machine's layout; (2) the arch-unit/runner contract: the unit
knows only the ledger base, block order and row offsets; the
runner allocates blocks, fills the ledger and IN rows, reads
OUT-0. Equivalence is evaluated on the ledger-relative text alone.
Speed is explicitly not a goal; universality and runnability are.

**REFINEMENT OF THE UNIVERSAL FORM — NO DESIGNATED REGISTERS AT
ALL (the owner, 2026-09-02).** the owner's restatement, his words: "no longer
use designated registers at all (meaning that registers are not
single purpose things but they are still used in standardized/
normalized ways) FOR ANY OF THEM. instead using a virtual memory
that is standardized in terms of the types of allocations. the
lineage of an input argument in its own block. same for results
being in their own block. everything is loading from memory and
storing in memory." Reasons: (1) never work around register
scarcity; (2) evaluate equivalence between units that use memory.
So the form is: standardized virtual memory with TYPED ALLOCATION
BLOCKS — one block per input argument's lineage, one for the
result, temps in their own block — every value loaded from and
stored to its block; registers are scratch vehicles chosen by one
fixed rule, never designated homes. The round-8 migration
(canon35_universal_*) is NOT this: it kept designated registers
as the load targets (a->%rdi etc.) and placed only three slots
(S0..S2) in the red zone below %rsp. That shortfall is why the
address-of units (c/op_31 etc.) collided: an answer that IS a
stack address moved when the directory took the red zone. Under
the owner's refinement the directory base is a ruled virtual region,
not %rsp-relative slots, and a unit's own stack addresses are a
lineage of their own. The migration must be redone to this
statement.

**THE UNIVERSAL CANONICAL FORM: VIRTUAL MEMORY FOR EVERY UNIT,
STANDARDIZED LOADS, ARRIVAL ANNOTATED (the owner, 2026-09-01).** The
designated-register description (a->%rdi, b->%rsi, answer->%rax)
is SUPERSEDED as the primary statement. The ruled form: every
arch-unit's values live in the DESIGNATED VIRTUAL MEMORY system
(the directory of standardized locations), and the way data is
LOADED from those locations into registers is itself
standardized — one load pattern for everyone. The registers
remain the standardized vehicles the loads use; they are no
longer the definition. Purpose, the owner's words: "the most universal
canonical form as possible" — special structures like pointers
and the bulk of register-friendly binary operators MEET IN THE
MIDDLE on the same memory-based form, with HOW the value arrived
(plain / pointer / tagged) carried as annotation, never as a
separate dialect. CONSEQUENCES: (1) the "may canonical form carry
a prologue?" question is DISSOLVED — standardized loads at the
top of a unit are part of the form, so the six go units needing
more than 16 slots are ordinary, not exceptional; (2) register
scarcity can never again refuse a unit; (3) comparison keys read
the memory-form text, and arrival annotations are information
for grouping decisions (ruled 2026-09-01 earlier: same
instructions + different modes = a finding to record).

**`branch-to-alternate-computation` — A THIRD DETECTION ROUTE
(the owner approved, 2026-08-31).** Every mode route so far detects a
branch leading to a trap or a panic call. CPython's integer
addition branches to a DIFFERENT COMPUTATION (the arbitrary-
precision digit loop) when its operands are not both compact.
The mode row measured this session:
    condition:  the operands are not both compact
    response:   grows
    detection:  branch-to-alternate-computation
`growing` was already in the ratified interval-probe vocabulary,
recorded as occurring ZERO times in the compiled corpus; this is
its first measured instance.

**THE ARRIVAL / COMPUTATION BOUNDARY IS LINEAGE CONFLUENCE, NOT
"WHERE THE ARGUMENTS MEET" (the owner corrected this backslide,
2026-08-31).** The retired core rule was "the arch opcode where
the arguments first meet"; it fails whenever the ORIGINALS never
meet — a cast, an unpack, any transformation on one side (the owner's
func_1 example: `result = machine_op_3(a_2, a_1, b_1)`, where
a_0 and b_0 never appear together). The correct boundary: the
first node whose ancestors include BOTH lineages — a's
derivatives and b's derivatives. ARRIVAL is the maximal prefix of
each lineage that touches one lineage only; COMPUTATION begins at
the first confluence and runs to the answer. This is a boundary
for the arrival/computation SPLIT only; it does NOT redefine the
seed, which remains the whole normal-path graph.

**BANKING IS A MESSAGE, NOT A COMMIT (the owner, 2026-08-31).** A
daemon commits and pushes every 30 seconds, deliberately: the owner
wants the highest-resolution history that is within reason, and
the cost is small. So NEVER write "staged, not committed — the owner
banks"; the daemon has already committed. What "banking" now
means: a message written FOR POSTERITY, to make the history
searchable, and it is fine for that message to land slightly
AFTER the commits it describes. Do not attempt to hold work back
from the daemon, and do not report commit state without reading
`git log` (round 3's log claimed staged-not-committed while the
daemon had already committed every artifact including the logs).

**THE REPRESENTATIVE RULE (the owner, 2026-08-29).** When arch-units
are DETERMINED EQUIVALENT (proved — byte identity, z3, or the
gated convergence chain), the group's canonical form becomes the
SIMPLEST member: fewest bytes of machine code; ties broken by
first-in-list order (deterministic, no judgment). The original
raw extracted arch-units are KEPT for records — the
representative replaces nothing in the evidence, it names the
group. This was NOT implicit before: convergence re-derived each
unit's text from its own expression, so proved-equal units could
carry different canonical texts (measured: 220 proved-equal
float units formed no dom_op families because their texts
differ). The representative is the cross-unit step that makes
proved equivalence visible to text-keyed grouping.

**SEEDED GROUPING UNDER CONDITIONS (the owner, 2026-08-29, ratified —
"yes to all of it. we are aligned"; full record in DevComms
log_081).** The narrow core definition is SUPERSEDED; it is now
the depth-one special case. The rulings:

- TRACE FOLLOWS TRANSFORMATIONS INDEFINITELY. the owner: "if a traced
  variable is transformed by an operator, the result of that
  transformation takes on the responsibility." Any tracer depth
  or single-path limit is an implementation defect, never policy.
- ARCH-UNITS ARE DATAFLOW GRAPHS (fan-out allowed: one value
  feeds many readers; sending a message does not consume it).
  Seed equality is GRAPH equality, so write-once-vs-write-twice
  compiler choices never split seeds.
- SEED = the normal-path computation graph, arguments to answer.
- GUARDED CONTAINMENT is the cross-unit relation: unit X
  "contains seed S under condition C" when a branch of X holds S
  and C gates that branch; within C the two are computationally
  equivalent. C is kept as data (mode rows extract it). Measured
  instance: go modulo L3 == c modulo whole-unit under
  b != 0 and b != -1.
- TWO GROUPING AXES, both automated, never merged: OPERATOR
  families group by seed; EXCEPTION families group by guard
  component (condition + response), across operators and
  languages. Unbiased whole-graph similarity is REJECTED because
  guard machinery dominates guarded units and would group unlike
  operators by their shared exceptions.
- SUPER-LOGICAL COMPILER-OPERATORS: an idiom recurring across
  arch-units is the compiler's logic, not the operator's (e.g.
  the halve-convert-double unsigned-to-float routine).
  **THE DETECTOR IS THE COMPILER GRAPH (the owner's ruling; corrected
  2026-09-03, log_173).** A super-op is a recurring PATH through
  the compiler's OWN SOURCE — the static structure (tree-sitter
  CST + call/read/write edges) joined to the dynamic structure
  (the diary of nodes each probe's compilation visited, in
  order) — the same structural+dynamic design the PCv5 ledgerer
  uses. Recurrence is counted over compiler-source paths across
  probes, and each candidate is joined to the arch-units it
  produced. the owner, 2026-08-29 (log_081 §5): "the compiler-graph
  instrument can measure the path"; the owner, 2026-09-03: "i
  specifically asked for the compilers/interpreters to be analyzed
  as a graph -- especially wrt to super-op mining."
  SUPERSEDED, and recorded as a divergence I introduced without a
  ruling: the sentence that stood here from 2026-08-29 to
  2026-09-03 — "Detector: the component miner's recurrence counts
  x unmodelled lifter names" — named an OUTPUT-side instrument
  (`super_op_miner.py`, over arch-unit bodies) as the detector.
  Every later brief cited it as ratified. It was not. Home of the
  corrected work: `Planning/.../node_0_3_1_9_graph`.
- The lifter was measured NOT to be the limiting factor
  (cvtsi2ss lifts fully as I32StoF64 + F64toF32); the limit was
  our own name->z3 translation table. Fix tables, not tools.

**TESTED AND NOT NEEDED — the `quiet-continue` lean was checked
against real float units on 2026-08-29 and does not apply to this
corpus.** The three float-comparison units were read: c/cpp/rust/
swift use ONE instruction (`cmpeqsd`) that answers the unordered
case itself; go uses `ucomisd` plus `setnp`/`setp` folded in with
`and`/`or`. Across 8 measured rows (equality and not-equal, over
2.0/2.0, 2.0/3.0, NaN/2.0, NaN/NaN) the ANSWERS AGREE EVERYWHERE —
1,0,0,0 and 0,1,1,1 in both forms. So the languages do not differ
on NaN at all; they differ in instruction selection, exactly like
`lea` versus `mov`+`add` for integer addition. No mode row is
needed and no fifth response kind is needed. SIGN TWO from the
original note is what appeared (the difference is in the answer,
not in a guard) — and following it showed there is no difference
in the answer either. RE-OPEN only if a language turns up whose
float comparison returns a third value rather than 0 or 1; none
exists in this corpus. The original provisional paragraph is kept
below for its record of how the question was framed.

**PROVISIONAL, SUPERSEDED BY THE PARAGRAPH ABOVE — `quiet-continue`
AS A FIFTH MODE RESPONSE (Fable's lean, the owner unblocked it
2026-08-29 WITHOUT confirming it; he said he did not fully
understand it yet).**

WHAT WAS DECIDED: a float operation whose operands are unordered
(one of them NaN) records a mode row like any guard —
`{condition: operands unordered, response: quiet-continue}` — so
two float operations differing ONLY in NaN handling are ONE
operator with a recorded difference, not two operators. The name
is IEEE 754's own: an operation that hits an invalid case, does
not signal, returns a default result, and continues, is "quiet"
(hence "quiet NaN"). The shape matches the existing responses
`wrap-continue` and `clamp-continue`.

WHY IT IS PROVISIONAL: no float unit has been through the
core-and-modes stage, because float is the unconverged bucket. So
the claim "NaN handling shows up as a detectable mode row" is
REASONING, not measurement. It is the one link in the argument
that has never been checked against data.

WHAT TO LOOK FOR IF IT GOES WRONG — the three failures that would
break it, in the order they would appear:

1. NaN handling turns out NOT to be a branch-to-response at all.
   Every mode found so far was detected by a branch leading to a
   trap or a call. Float comparison sets flags and continues with
   NO branch — the "response" may be invisible to the detector
   that finds every other mode. SIGN: float units converge but
   produce EMPTY mode lists while the languages demonstrably
   differ on NaN.
2. The difference is in the ANSWER, not in a response. C's
   unordered compare answers false; a language with a three-way
   comparison answers its third value. If the divergence lands in
   the returned value rather than in a guard, it belongs in the
   class key, not in a mode row — which would make these two
   operators after all, and would be a genuine ontology question
   for the owner. SIGN: two float units with identical cores whose
   returned values differ only on unordered inputs.
3. `quiet-continue` collapses distinctions. If several different
   NaN behaviours all get the one name, the name is hiding a
   split. SIGN: units in one family whose NaN behaviour differs
   in ways the mode row does not record.

RE-OPEN THE QUESTION WITH DEE if any of the three signs appears.
Do not defend this paragraph; it was adopted to unblock, and it
has one unmeasured link by construction.

**TEMP REGISTERS ARE STANDARDIZED, NOT LIMITED (the owner, 2026-08-28,
correcting an invented rule).** There is NO two-temp limit and
never was. the owner's ruling covers the TRACED registers — a, b, and
the return register — and even those may flex under exception
conditions (hardware pins). Temporary registers matter ONLY in
that their selection is standardized so two arch-units can match.
So: a fixed ORDERED POOL of temps, assigned in first-needed
order, as many as the unit needs; standardized stack slots only
after the pool is exhausted. Any code or report saying "the two
available temp registers" is stating an invented constraint, not
a ruling. the owner's words: "why the fuck would anyone think that
there should be a limit of two temp registers? ... as long as the
selection of temp registers are standardized so that arch-units
can match, why would it matter otherwise?"

**FIX A CAUSE AT FIRST OBSERVATION (the owner, 2026-08-28).** A named,
understood, mechanical gap — e.g. an 8-bit answer needing the
zero-extend-into-the-answer-register form that the corpus already
shows — is fixed when first seen, not carried as a recurring
line in a report. Reporting a known-mechanical gap twice is a
process failure.

**CANONICALIZATION INCLUDES THE TRANSFORM-AND-RETURN STEP —
STOP RE-LITIGATING THIS (the owner, 2026-08-26, said in anger after
the same correction had to be made repeatedly).** Two errors keep
recurring and are BANNED:

- ERROR 1: writing or implying that canon-text is "a string
  representation" or "text-only". IT IS NOT. Canon-text is ARCH
  OPCODES — the same instructions as the bytes, printed. Measured
  proof, forced by construction: 508 canonical texts <-> 508
  assembled byte-strings, ZERO violations in either direction
  (canon_roundtrip / canon4 bijection check). Text and bytes are
  one thing in two printings. Never rank them against each other
  and never describe one as more real than the other.
- ERROR 2: treating normalization/simplification layers (z3,
  e-graphs, lifted forms) as sitting ABOVE the canonical form, or
  saying "canonical text will never catch X". Those layers are
  INSIDE canonicalization: canon-text is transformed into
  whatever a tool needs, the tool simplifies, and THE RESULT IS
  RETURNED TO CANON-TEXT. A result that cannot return is an
  intermediate, not a result.

THE CONSEQUENCE, which is the correct reading of any residual
difference: when two units compute the same thing but render
differently — e.g. c's `lea (%rdi,%rsi,1),%eax` vs go's
`mov %edi,%eax` + `add %esi,%eax` for i32 addition (measured, 6
such groups) — CANONICALIZATION IS NOT FINISHED ON THOSE UNITS.
It is not evidence that the form is insufficient. The fix is to
run the simplifier and bring the result back so the two converge
to one canonical text. Convergence is a canonicalization duty,
not an outside layer's achievement.

the owner's standing complaint, recorded so it is not repeated: prior
work treated the accumulated matching grounds as the real
machinery and his canonical form as a presentation requirement
bolted on. That inversion is how his projects get messy. The
canonical form is the machinery.

**COMPOSITIONAL MATCHING (the owner, 2026-08-26).** The class key is
NEITHER the whole function NOR the core alone. Arch-units are
treated as mathematical statements composed of components, level
by level: alphas are the simplest recurring units (defined by "no
smaller component recurs elsewhere", NOT by line count — cltd+idiv
travel as one alpha because the hardware splits one operation
across two instructions), betas compose alphas and fresh opcodes,
gammas compose {opcodes, alphas, betas}, and so on. A component at
any level is a LITERAL sub-term (same characters, in the erased
form's a/b/uN naming), never a description. Sameness is a relation
between terms: go's modulo CONTAINS c's modulo (the cltd+idiv
beta, verbatim in block L3) plus two guard components; the table
rows carry which components are shared and which are added,
instead of one flat verdict. Components are found by matching
step sub-sequences — machine form throughout, spelling ban
untouched. Starting line-count for mining is free (empty levels
are fine); the level definition is recurrence, not length.

**THE DIRECTIONAL BRIDGE / DOMINANCE RULING (the owner, 2026-08-26).**
Result-type split STANDS (C's int-comparison and C++'s
bool-comparison are different classes — the transplant test:
substituting the bool-form where int-form is expected miscompiles
callers that read all 32 bits). Between split classes the relation
is a DIRECTIONAL BRIDGE: "X dominates Y on projection P" — at
every reading Y's callers perform, X answers identically, plus X
answers readings Y cannot. The bridge carries: the projection
(which bits/outputs), the proof scope, and THE ADAPTER (the glue
an emitter inserts to substitute the dominated form the other way,
e.g. movzbl %al,%eax). Dominance is decidable with existing
machinery: prove equality on the reader's projection, record
direction. It is also the right relation for the
different-live-result-count residue (one side leaves extra
outputs: same answer plus more).

**THE DOM_OP CONSTRUCTION RULE (the owner, 2026-08-26).** Dominant
operators are DISCOVERED from machine evidence by matching, never
asserted: nodes are (language, grammar-operator, ARITY) — provenance
of the probe, not a cross-language token; edges only BETWEEN
languages, weighted by shared equivalence-class count; each node
keeps its single STRONGEST counterpart per foreign language, kept
only when MUTUAL; connected components of the mutual-best graph are
the dominant operators. Measured effect: the naive class-sharing
graph's 29-node coincidence blob dissolved into clean families —
including the bitwise-not family found across five different
spellings (c `~`, cpp `compl`, go unary `^`, rust `!`, swift `~`).
Weak coincidences (xor==not-equal on bool) survive as class
structure but cannot outvote a strong counterpart. Arity is part of
node identity because one token can be two operators (go's `^`).

**THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25
after a second violation).** No operator token may appear in ANY
key, grouping, pairing, row structure, candidate selection, or
comparison scope, anywhere in this line — not in matching, not in
"which pairs get compared", not in report rows, not in dropdowns.
The candidate set for comparison comes from machine-form evidence
(clusters, connections, type pairs) or from ratified intention —
never from the token. The token appears exactly once per unit: as
a display label on the member. HISTORY OF VIOLATIONS, so the
pattern is visible: (1) the arch campaign's cross-language matrix
(caught by the owner 2026-08-24); (2) verdicts.py's row pairing (caught
by the owner 2026-08-25 — the fix brief itself reintroduced it as
"same-operator pairs"). MECHANICAL GUARD REQUIRED: every pipeline
stage that groups or pairs units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output
on failure. A brief handed to any subagent for this line MUST
paste this paragraph verbatim.
7. three verdicts: MATCHED / DIFFERS-BY-DESIGN (guards, traps —
   the mismatch IS the finding, the divergence condition) /
   UNMATCHED -> solver (z3) then probe-refutation, honest
   UNDECIDED bin.
8. deliverable: the dominant-operator table (equivalence classes +
   divergence conditions per operator intention), feeding ur_kind
   and the ledger. Compiled languages only.

## coding discipline (the owner, 2026-08-24)

- **No complex statements.** If a statement can be split into
  multiple lines, split it. A compound one-liner hides
  information; that is an anti-pattern for developing and
  maintaining code. Applies to every artifact on every PC repo.

## the evidence doctrine (the owner, 2026-08-24, recorded at his request)

The thesis is, in a sense, one giant proof connecting languages: if
the research is sound, assumptions are minimized to the greatest
extent possible. Every claim an agent makes on this line must know
which class it sits in, and must not present a lower class as a
higher one:

- **forced by construction** — the fact is derived from artifacts
  we built, by a comparison that only the fact itself can explain.
  Example: which register holds the first argument is proven by
  compiling `a - b` beside `b - a` (an order-sensitive operation)
  and reading which register the difference lands on. Rests on ONE
  assumption, stated once: the compiler compiled the program we
  wrote. Everything in the line already rests on that.
- **the tool's own testimony** — machine-readable statements a tool
  emits about its own output: debug-information tables mapping
  each parameter to its location, a compiler's intermediate forms
  (`--emit=llvm-ir`, `-gcflags=-S`), a grammar's `node-types.json`.
  Specific to the artifact at hand, but still the tool reporting on
  itself — testimony, not proof.
- **human interpretation of stated design** — a specification plus
  the assumption that the tool obeys it (the x86-64 calling
  convention, a language reference). Weakest class: a promise about
  tools in general, not a fact about the binary in front of us, and
  it must be re-interpreted per language, per version, per time.
- Sampled observation refutes; it never proves (unless exhaustive,
  as in the 8-bit modulo sweep). Solver analysis over a lifted form
  proves — about the MODEL of the machine, which is itself
  testimony (the lifter's).

Practice: prefer forced-by-construction; use testimony as the
cross-check; when only interpretation is available, SAY SO on the
claim ("unverified", "per the convention"). Two independent classes
agreeing is the standing pattern (author + judge); their
disagreement is a finding, never noise. The 2026-08 arch campaign
is the worked example: spelling-keyed comparison was banned (two
operators are the same only by machine-form equivalence, never by
token), the lifter's operand anonymization was caught false-merging
`<` with `>` precisely because it re-derived by guesswork a fact we
could have carried by construction, and the repair is to record the
fact at generation time rather than reconstruct it downstream.

## open research thread (2026-08-12)

Objective kind clustering: replace hand-judged ts_kind → ur_kind
bucketing with machinery over grammar-shipped features —
`src/node-types.json` per grammar carries arity
(`multiple`/`required`), input types (per-slot allowed kind sets),
output types (supertype memberships), uniformly across languages.
Cross-language type connection to be exportable/importable data.
Home: PCHQ `Planning/node_0_3_research` + `Research/`. First
handful: rust, python, kotlin, dart, c/cpp.

## the rulings of 2026-09-04 / 2026-09-05 (the owner, in session)

**THE UNIT'S BOUNDARY IS A FUNCTION BODY.** From just after the
wrapper-function call to just before the return. For a compiled probe
the wrapper is the probe function we wrote; for an interpreter there
is no wrapper of ours, so the interpreter's OWN handler function is
the wrapper. Bounds are READ, from the symbol table and DWARF —
never computed by taint propagation. the owner: "everything is wrapped in a
function. it should be just after the wrapper-function call to just
before the return statement. no?" This retires `lineage_carve.py`'s
BOUNDARY use (its propagation stays as evidence for arrival
lineages). What it cost, accepted with the ruling: all 11 interpreter
units moved PROVED → UNDECIDED, because a whole handler writes memory
and answers with a pointer where a four-instruction slice did not. A
verdict that moves this way is a CORRECTION, not a regression — the
old proof rested on a boundary someone chose.

**THE CANONICAL FORM WAS MISREAD, and the correct reading is the owner's.**
His 2026-09-02 ruling ("everything is loading from memory and storing
in memory") means: **the arch-unit is essentially UNCHANGED except
for the loading and unloading of registers into a virtual memory.**
`region36.py` read it as "rewrite every location relative to a ruled
base register", which is why it claims `%r15` for a whole body.
`canonical_form.py` (canon40) already does the right thing — loads at
the front, THE BODY VERBATIM in the middle, a store at the back,
addressed rip-relative through the ledger — and zero of its 1,779
compiled units' wrapped texts contain `%r15`. The eleven interpreter
units are on the wrong form and belong on `canonical_form.py`.

**THE `%r15` COLLISION IS AN ARTIFACT OF THAT MISREADING**, not a
design conflict. php's handlers use `%r15` as a bytecode pointer and
`add $0x20,%r15` moves it mid-body; HotSpot uses it as the thread
pointer. Under the correct form nothing claims the register and the
refusal disappears. Do not "solve" it by moving the region base.

**A SEVENTH BLOCK KIND IS NEEDED: an arriving addressable area.**
`region36.py`'s six kinds are input / constant / temp / result /
own-address / guard-outcome. Five hold ONE VALUE each; `own-address`
is already an addressable AREA the unit reaches into at its own
offsets. php's frame is the same shape but ARRIVES rather than being
the unit's own scratch. the owner's observation, which is correct: a unit
that works through pointers is already in the virtual-memory form by
default — it is the compiled units that need wrapping. So this is one
new kind with a working precedent, not a redesign.

**"COMPLETED" FOR THE COMPILER GRAPH IS NOT AN OPEN QUESTION.** It
means an actual implementation of what was specified: all three
connection kinds — structural, dynamic, and per operator traced
variant — over the compilers and interpreters in scope. A machine
limit is a measured obstacle to report, never a redefinition. the owner:
"completed compiler graph? when theres an actual graph that is an
implementation of what ive asked. what the fuck is that question?"
Never offer a reduced deliverable as a reading of a requirement.

**THE CHRONOLOGY IS VERSION CONTROL AND NOTHING CURATES IT.** A
moment is a commit; the scale is `git log`, unfiltered and ungrouped;
no project vocabulary ("round", "banked", "lap") may appear in the
mechanism. The defect this retires: `chronology_build.py` ran `git log
--grep=banked -i` and matched `round\s+(\d+)\s+bank`, so its steps
existed because an agent had written a word into a commit message.
The dashboard is becoming a general PlanPlan dashboard, so anything
that only works for PseudoCoup is a defect in that node.

**PANE 4 CANNOT EXIST BEFORE THE OBJECT IT DRAWS DOES.** Do not
manufacture something to display in place of a missing deliverable.

**THE ARCH-OPCODE-NODE**, added 2026-09-05: a compiler-graph node the
SOURCE shows producing a machine instruction, detected statically,
with no run of the compiler. Four states — names its opcode /
resolvable by one static hop / emits with a dynamic opcode / emits
nothing. It reaches compilers this machine cannot instrument. Not for
interpreters: an interpreter emits nothing, it dispatches, and its
equivalent is the handler function itself.

**A REPORT'S CLAIMS MUST BE RE-RUNNABLE.**
`check_conventions_log_claims.py` re-runs a DevComms log's commands
inside Airlock and sorts each claim into matches / differs /
unverifiable. Measured on six logs: 127 of 171 claims (74%) carried
nothing to re-run, and three transcripts in log_195 could not be the
output of the command above them — tidied after the fact, with the
underlying facts true. An attribution block must NAME ITS LANE LOG
FILE.

## communication, added 2026-09-05 after an hour was wasted

**ANSWER "WHAT IS IT" IN ONE SENTENCE, IN RELATION, FIRST.** See
protocol §1.8. "A term is the arch-unit expressed as a z3 expression"
is the answer that took an hour to reach because every attempt
explained what a term was FOR instead of what it IS. Name the thing
in relation to what it sits between, in the first sentence, before
any purpose, motivation or walkthrough. Withholding the definition
while explaining around it reads as bad faith.

## the arch-opcode emulation line, rulings and state of 2026-09-07 → 2026-09-10 (re-read before any work on it)

THE GLOSSARY IS `Research/GLOSSARY.md`, in the owner's form. Every word of this
line (cell, term, tier, gate, bank, reading, carve, lifter, ...) is
defined there. A reply to the owner defines each one it uses, in place, before
it carries weight; the loop is shown as a code block, never inline.

the owner's four names, the loop, and where each thing lives. This is the
whole line in one place; the logs (233–256) hold the evidence.

`set_of_unique_arch_opcodes`
- every arch opcode any compiler or interpreter in the corpus produced,
  one instance each — 162 mnemonics (`Research/oracle/arch_opcodes/unique_opcodes.json`).
- RULING 2026-09-08: a mnemonic alone is a SPELLING. The machine-form key
  is (mnemonic, operand form, width); the mnemonic sits in the field
  `mnem`, which the spelling guard exempts as machine form. Whether two
  cells compute the same mapping is z3's verdict on their terms, never a
  reading of names (`add` and `lea` share a value and differ on flags).
- at that key the corpus uses 253 attested cells over 134 mnemonics
  (`Research/oracle/arch_opcodes/model/model_table.json`, tasks m1/m1b).

`cell`
- one row of the model table: the reference's mapping of that opcode
  at that form and width, as a z3 term per written place (destination,
  flags, accumulator pair, memory), plus the corpus's attestation.
- a cell's term is architecture-neutral; only the reading opcode → term
  (the reference) is x86's.

`find_emulation(cell, target)` — the running algorithm, exactly
```
term   = cell.mapping                       # from the model table
source = render(term, target)               # one spelling per z3 operator; the target's
                                            #   own primitive where one lowers to this cell
body   = carve(compile(source, ship flags)) # the target's compiler does the optimising
verdict = z3(walk(body) == term)            # per written place; no search anywhere
```
- no branch is keyed on an opcode name (checked, 2026-09-10; the one
  `ret` is the carver's). The contract rules (a vector place projects to
  its lane; memory and flag reads are parameters; a 128-bit place is two
  halves; a derived arrival is a region; an immediate is an input; an
  empty body is the identity; a flag consumer is rendered over EVERY
  attested setter) are general and unconditional since task ap6.
- the driver is `emulation/handful/handful.py` + `autopoly/autopoly.py`;
  renderers for c, cpp, rust, go, swift; the interpreted route
  (`emulation/interp/`) renders in cpython, php, ruby, java, javascript,
  dart, csharp and CHECKS by the fuzz method (edge values first in every
  sample; an agreement is evidence, never a proof).
- the SECOND TIER (task t2, running): where a target lacks a primitive
  at a width or kind, construct it from `& | ^ ~`, a conditional and
  variables, smallest width first; both routes per cell, bank whichever
  proves; proof canonical-form first, the schema's lemma second, z3 last
  and bounded. the owner: "whoever gets there first"; the guarantee is that a
  Turing-complete language with full arithmetic has every logic gate.

`the bank` (`emulation/autopoly/certificates.jsonl`, task bank1)
- the polyfill library: one certificate per (cell, target, place, setter):
  term text, rendered source and its sha256, compiler and flags, carved
  body, verdict, the code version that produced it. A certificate never
  regresses; only the machinery can fail to reproduce it.
- the loop runs `autopoly.py --bank`: uncertified keys plus a 5% audit;
  a differing verdict on identical inputs is an ALARM and a STOP.
- pass-over-pass full re-derivation (ap1–ap5) was a DESIGN ERROR: it
  re-did 75–98% of known work per pass and lost 19 proved pairs once.
- THE HEADLINE IS ALWAYS THREE READINGS: strict (every written place),
  destination-only, corpus-needed (flags only where the corpus's
  flag-pair rows show a consumer). On all four compiled targets, as of
  ap6: strict 94 cells / 49.4% of attested rows; destination-only 147 /
  73.1%; corpus-needed 137 / 68.0%. All seven interpreters agree on 184
  cells / 87.2% (ex2). cpp is c's twin.

`the Hub` (`Research/oracle/hub/`, tasks hub1/hub2)
- source composition: tree-sitter + go/types resolve each operator node
  to a cell (else the setter+consumer PAIR, else the operator's whole
  lowered body = its pool entry); each node becomes a call of the
  dictionary's proved emulation; the target's compiler lowers ACROSS the
  calls (measured: `a + b - c` → `lea; sub; ret`); the gate proves body
  B against go's own body A. Over 590 corpus go units: c composes 325 /
  proves 290, rust 276 / 260, disproved 3 on each.

`level 0` (the reference, `Research/op_pipeline/reference.py`)
- VEX's reading of Intel's prose; RATIFIED ground truth for every term.
- 2026-09-10, task ref1: checked against the K-framework x86-64 semantics
  (Strata's chip-tested formulas, in `Sources/X86-64-semantics`, read from
  `/sources`, never copied): 383 disagreeing places over 144 cells, ALL
  resting on four lines — `full64` zero-extends 8/16-bit writes (the
  hardware keeps the upper bits), `build_carry_binary` leaves the carry
  out of the flags, `cond_to_z3` computes every condition as L−R,
  `sub`/`sbb` missing from `WIDTH_IS_NOT_A_SUFFIX`. Intel's undefined
  flags recorded as regions. NOTHING DECIDED; task ref2 (written) fixes
  the four and re-derives everything that rests on them — on the owner's word.

`the layout, 2026-09-10` (DevComms log_001, §13–§15)
- the laptop's `~/Programming` is split: this repo is
  `PRIVATE/PseudoCoupHQ`, Airlock is
  `PUBLIC/Airlock`, DevComms `PRIVATE/DevComms`. The old
  names DO NOT EXIST (links retired); a path that fails is meant to.
  The tower stays flat; `remote_lane.sh` maps either spelling both
  ways; sync args stay `Programming/PseudoCoupHQ/...`; container paths
  `...` unchanged. Lane scripts under Research are tower-side
  and keep the flat spelling on purpose.

`the tower`
- all lanes run on the VM on the owner's tower over ssh, through
  `PUBLIC/Airlock/remote_lane.sh` (LAW.md's tower section);
  waits in short calls under 110 s (a tool call is cut at 120 s).
- the law is `Research/LAW.md`; briefs live in `Research/briefs/`; never
  the session scratchpad (wiped twice).

`the ruling of 2026-09-10 evening: the guarantee tier is top priority`
- the owner: the general construction from primitives "is meant to be capable
  of proving as a guarantee" — top priority. t2's eight schemas were
  patterns for the refused shapes, NOT the method; that was my
  sequencing error. t4 builds the method (one construction per
  operation kind, general in width and word, proved once, composed over
  any term with named intermediates; native operator wins) and measures
  every unproved cell with a named cause. Runs from 2026-09-10 evening,
  ahead of t3 and rv3b.

`the general tier, closed 2026-09-11 (t4, log_262)` — THE GUARANTEE, MEASURED
- constructions exist for every kind; 246 places proved by Lean lemma
  alone (bitwise/complement/equality/conditional/wiring at 8–64 bits on
  c/cpp/rust). The edge: multiply/divide/remainder/floats at ≥16 bits
  construct but no prover closes (Lean SAT times out at 16-bit multiply;
  z3 30–3,000 s then memory). go/swift: word 64 → constructions of
  ~19k instructions, not gated. Pass partial: 304 of 654 runs. Readings
  x86 unchanged 96/154/141; RISC-V 119/255. Collapse: LANDED 27 of 335.
  OWED: Lean lemma general in width (bv_decide is fixed-width);
  algebraic lemma for mul/div; delta pass over the 350 left behind.

`level 0 corrected, 2026-09-10 (ref2, log_261)`
- four hardware-fact defects fixed; the independent K-framework reading
  now disagrees at NONE of 1,779 places (was 383); table, term store,
  canon40 proofs re-derived beside the old (nothing overwritten). The
  bank's re-attempt rule must hash the reference too (t3 takes it).
  The corrected stores are what t4 measures on.

`the second tier, closed 2026-09-10 (t2, log_257)`
- 14 constructed places proved (adc/sbb/shld/shrd at 64 on go and
  swift), every one by the schema's Lean lemma; the compiler collapsed
  NONE (LANDED 0 of 14; bodies 4–17 instructions for the one the cell
  names). That is the measured answer to the owner's question "can the
  c-compiler simplify the constructions": no — it supports his IP claim
  (proof-carrying simplification rules generated from arch-unit
  equivalences). Bank 24,758 certificates; strict 96 / destination 154
  (75.2%) / corpus-needed 141.
- what blocks the rest, each a named thing and each mechanical: the
  renderers print one nested expression (no intermediates → divider,
  softfloats unstatable); the x87 family refused at the arrival
  contract (80-bit value as two integer words fixes it); the tier's
  source outside code_version (full pass instead of delta). Task t3
  (brief written) does those three, after ref2.

`the bit-blast route, 2026-09-12 (bb1, log_267)`
- z3's own circuits, no authored arithmetic: go 203, rust 202, c/c++
  136 of 255 (the lifter lacks bexti/orn/c.not). Three routes together
  251 of 255 on some language, 235 on all four; only mulh/mulhsu 64
  remain. Divide-family circuits: 75–85k gates, 100k–250k
  instructions, over the 4,000 ceiling.

`the reach of the proofs, 2026-09-12 (cov1, log_266)`
- expressible = every arch-opcode of a unit proved on the target.
  RISC-V: c→rust 369/369, go→rust 105/105. x86: c→c 44%, rust→rust
  71%, go→go 27%, swift→swift 19% of units; the blockers everywhere are
  `cmp`, `test`, `push`, `movslq` — flags-only, stack and widening
  cells, not arithmetic. The worklist is those few cells; each unblocks
  thousands of units. `Research/oracle/coverage/`.

`RISC-V, 2026-09-12: 251 of 255 arch-opcodes proved on at least one of c, c++, rust, go; 231 on all four (rv6, log_265)`
- every table row carries "of 255" (the owner). The four left are mulh/mulhsu
  64 (the 128-bit product's high half). bb1 = the bit-blast route
  (z3's own tactic, no authored arithmetic), running; then the other
  PCHQ languages. The compiled go divide (lane rv7) shows the compiler
  DOES simplify our emulations: the upstream zero case removed go's own
  check and panic call.

`RISC-V, 2026-09-12: 244 of 255 arch-opcodes proved (rv5, log_264)`
- the loop over EVERY RISC-V cell, both routes, ship flags, one process,
  five minutes. From 117: the earlier loop skipped every cell that had
  an x86 twin, proved or not — a population filter, not a method limit.
  NEVER filter a loop's population by bookkeeping again; run it over
  the whole set and let refusals be rows. The 12 left are divide,
  multiply-high, float subtraction and unsigned-64-to-float.
- rv4 (log_263): optimization OFF made the check WORSE (36 proved of
  188 vs 144 at ship flags); the cause I wrote ("no memory model") is
  retracted; the lifter models loads and stores on named cells.

`RISC-V` (exploration, not a pivot; rv1 CLOSED 2026-09-10, log_258; rv2 running)
- rv1: ten units carved on riscv64; level 0 for RV64IM = `riscv_reference.py`
  checked at 860,304 points against the ratified Sail simulator, 0
  disagree (a check at points, not an equality); the claim on 10 units:
  7 IDENTICAL after normalize, 3 DIFFER for contract causes only (the
  ABI's narrow-argument extension; `idiv` traps where `divw` defines);
  the surface 2,644 lines in 5 files, the lifter 44% — the term store,
  table, bank and proofs transferred untouched.
- rv2 (log_259): the transfer measured. 255 RISC-V cells; a TWIN = an
  x86 cell with an equal term: 102 at the whole place, 161 at the
  cell's own width (RISC-V's 32-bit forms sign-extend into the register,
  x86's zero-extend — a contract, stated per row). Inherited
  certificates compiled for riscv64 and gated: 103 proved, 0 disproved.
  The loop over the untwinned proved 82 cells. 116 of 255 (45.5%) hold
  a proved riscv64 emulation. Readings coincide on RISC-V (no flags).
  Owed (rv3): Zba/Zbb/Zbs in the lifter; twins vs ref2's table; rust
  `riscv64gc-unknown-linux-gnu` + `g++-riscv64-linux-gnu` headers in
  the image (rebuild queued); the 734 certificates into the bank.
  FOR DEE: does the Hub's dictionary key carry the extension rule.
- rv3 part 1 (log_260): the lifter gained `c.zext.w add.uw c.mul bseti
  fsgnjn.d` (99,968 Sail points, 0 disagree); the inheritance re-run on
  the sixth image: 244 PROVED / 0 DISPROVED / 0 UNDECIDED of 734 (c 58,
  cpp 54, go 71, rust 61; swift 56 not attempted: no swiftc for
  riscv64), against rv2's 103. Twins on the corrected table and the
  bank merge WAIT FOR ref2 (a follow-on lane, rv3b). the owner owns a planning
  sub-node for RISC-V (wanted, not created).
- the ratified Sail model is level 0 for free; no flags at all; the
  library transfers by TERM identity (a certificate says "this source
  computes this term", architecture-neutral); only the compiler's
  backend is re-verified. The image gains the rust riscv64 target, Sail
  (0.20.2) and the sail-riscv C simulator `sail_riscv_sim` (Isla dropped:
  unbuildable against a released Sail); sixth build adds the rust
  `riscv64gc-unknown-linux-gnu` target and `g++-riscv64-linux-gnu`
  (glibc/libstdc++ headers at /usr/riscv64-linux-gnu; clang takes
  `--target=riscv64-linux-gnu --gcc-toolchain=/usr`). On the tower
  2026-09-10 evening.

communication, 2026-09-10 (cards in the protocol, cases Appendix D): the
model of how to write is the owner's own message in cases Appendix C.1 —
plain vocabulary, terms loudly defined, a loop, a few sentences that
hold the big picture; not a prose block, not a cold telegraph.
