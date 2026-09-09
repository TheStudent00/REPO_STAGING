# log 121 — state of the round-6 conversation

# (learned / learning / will learn)

Date: 2026-09-01. Written at the owner's instruction to
preserve this conversation's content for the project.

## 1. Things we have LEARNED (measured or ruled)

- Type inventories are EXTRACTED, never hand-written
  (the owner's ruling; log_116 built it). Validation of the
  extracted inventory against the 4,440-candidate /
  1,779-accepted corpus: zero holes (no accepted probe
  uses a type outside the inventory), and the
  load-bearing split — the type PAIR alone explains
  ~71% of go/rust/swift refusals and 0.0% of c/cpp
  refusals (0/140, 0/232). c/cpp legality lives in
  the operator's own category rules (implicit scalar
  conversion), not the pair.
- swift has no EXTRACTED authority yet — its grammar
  spells types as identifiers (no type tokens; go
  shares this) and no swift compiler source is checked
  out. THIS IS NOT A BLOCKER: routes, cheapest first —
  (a) the installed toolchain's own stdlib interface
  files on disk; (b) swiftc emitting the stdlib module
  interface (tool's own testimony); (c) git clone of
  the swift repo at the tag matching `swiftc
  --version` into Sources/, read via
  git show at the pin like llvm-project; (d) DWARF
  from swift optimizer-off builds.
- The DWARF witness in log_116 was refused on a FALSE
  ground: the sub-agent looked for /persist on the
  host; /persist exists only inside the Airlock
  container (tasks 24/27 read it through lanes the
  same day). Lesson of record: a path check proves
  which SIDE OF THE CONTAINER WALL you are on before
  it proves absence.
- lane_gen.py firstline() runs text.replace("|","/")
  on stored diagnostics, so stored refusal testimony
  is altered wherever the compiler quoted `|`
  (rust probe 178 stores "i32 / f64" for `a | b`).
  Violates verbatim-testimony; recorded, not yet
  fixed (the owner's call on remediation + re-capture).
- Result-destination seat works: all 5 rust sret
  units PROVED (log_117); exactly 5 such units exist
  in the 1,779 (exhaustive survey). One cause: the
  seat allocator handed out System V seats from
  index 0, mislabeling the caller's answer address
  as `a`.
- Designated memory works: 36 of the 74 remaining
  units PROVED, 0 disproved (log_118). The old
  "two stack-spilled operands" refusal hid two
  faults (immediates miscounted; a two-register
  temp pool surviving the 2026-08-28 "standardized,
  not limited" ruling). The refusal fires against
  SHIP, not anchor — the round-6 brief's premise
  was wrong and is corrected by measurement.
- Arrival mode is measured, not asserted: 1,776/1,779
  compiled units plain; the 3 exceptions are exactly
  the sret units, found by an independent test —
  two grounds agreeing. All 24 proved
  interpreter/compiled pairs differ in arrival mode,
  as the pointer-arrival ruling predicted.

## 2. Things we are LEARNING (in flight)

- Task 32 (interpreter table / join / union, the
  three-views construction) was lost mid-run when
  its host process exited; it must be relaunched,
  checking disk for partial canon33-consuming
  artifacts first. Its inputs are all landed
  (log_111/113/118 machinery).
- Whether the 5 sret proofs (log_117) and the 36
  designated-memory proofs (log_118) advance the
  recorded count is DEE'S CALL: would move
  1,635 recorded / 1,622 honest to 1,676 / 1,663
  (13 withdrawn stay a separate population).
- Whether the canonical form may carry a prologue:
  six go units need more than the 16 red-zone
  designated slots.

## 3. Things we WILL learn (the ruled plan)

- Probe regeneration, the owner's direction (this
  conversation): rely on THE INTELLIGENT WAY —
  glossary entry below — to derive legal probes
  from the sources, and only compile the residue.
  Steps in order: (1) obtain swift's authority;
  (2) compute filtered-vs-naive counts per language
  (naive: 9,320 at the two-authority core, 145,082
  at the full core) and REPORT THE REDUCTION to the owner
  before compiling anything; (3) stand up a
  CPU-capped copy of Airlock (renamed containers —
  the same no-shared-names constraint as
  Airlock/SandboxDesign) so the machine never
  overheats; (4) trickle the residual probes through
  it in checkpointed chunks.

## 4. Glossary (pinned meanings from this conversation)

the intelligent way (probe filtering)
    deriving the set of LEGAL probes from the
    authorities' own rules -- reading the compiler /
    compiler-graph / tree-sitter sources to capture
    every operator variant with its admissible type
    combinations -- instead of compiling the entire
    type cross product and letting refusals sort it.
    example tied to context:
        go's extracted type table already predicts
        ~71% of its refusals from the pair alone;
        c/cpp need the operator-category rules read
        out of clang's semantic analysis, because
        the pair predicts 0%.

anchor / ship
    the ratified pipeline's two builds of every probe
    (AgentMemory, 2026-08-24): ANCHOR = optimizer off,
    where identity is established from the compiler's
    debug tables; SHIP = optimized, where matching
    runs. A cold term — reintroduce it on return.

## 5. Process lessons this conversation added

- A sub-agent's refusal reason is testimony, not
  fact: verify which side of the container wall a
  path check ran on before relaying "absent".
- Current disk state is not a blocker statement:
  "no checkout exists" must never be presented as
  "cannot be obtained".
- A coined phrase ("the intelligent way") is adopted
  only WITH its content; repeating the phrase while
  dropping its definition is the drift mechanism
  the owner named, and the glossary entry is the fix.
