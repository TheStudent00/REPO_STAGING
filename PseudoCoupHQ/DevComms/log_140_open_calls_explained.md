# log 140 — the open calls after round 9, explained

Date: 2026-09-02. Written at the owner's request ("please explain the open
calls using the comms protocol"). Each call is stated so it can be
answered from this page alone (protocol §3.4): the facts it rests on,
shown as real rows first; then the mechanism; then the question in
plain words. Every figure names its population (§3.4a). Nothing here
decides anything; the decisions are the owner's.

Sources, by full path:
- `PseudoCoupHQ/DevComms/log_135_task43_universal_form_redone.md`
  (calls 1, 2, 3)
- `PseudoCoupHQ/DevComms/log_137_task45_type_second_witness.md`
  (call 4)
- `PseudoCoupHQ/DevComms/log_138_airlock_instances_feature.md`
  (calls 5, 6, 7)
- `PseudoCoupHQ/DevComms/log_126_task37_testimony_defect.md`
  and `log_131_task40_regeneration_trickle.md` (call 8)

Glossary, for the terms that carry weight below:

```
region
    the standardized virtual memory every unit's
    values live in under the redone form: one
    0x408-byte area whose base is the register
    %r15, mapped at run time to %rsp - 0x400.
    example tied to context:
        `mov 0x0(%r15),%r10` in c/op_31's text
        loads argument a from input block 0 of
        the region.

block
    one typed slice of the region, one per
    lineage (input, constant, temp, result,
    own-address, guard-outcome), eight bytes.
    example tied to context:
        0x200(%r15) is the result block; the
        gate reads the answer from there.

lineage
    every value that descends from one origin —
    an argument, a literal, a temporary — as it
    is transformed through the unit.
    example tied to context:
        in `a + b`, a's lineage is the load of a
        and every register that carries a or a
        derivative until it meets b's.

materialize
    to write a value out to its block, not only
    keep it in a register.
    example tied to context:
        the result IS materialized (stored to
        0x200(%r15)); a temporary that lives only
        in %r10 between two instructions is NOT.

instance (Airlock)
    one running sandbox under one Airlock
    install; named, with its own settings file.
    example tied to context:
        `sandbox` (the default, running now) and
        `trickle` (six cores, no proxy, brought
        down after its proof lane).
```

---

# 1. Four units whose own text uses `%r15`

## 1.1 The instance

Population: the original corpus, 1,779 compiled units. Four of them
were REFUSED by the redone form, reason quoted from log_135 §13.2:

> `cpp/op_765`, `cpp/op_770`, `swift/op_703`, `swift/op_739` spend
> `%r15` themselves.

"Spend" means: the unit's own ship code already writes to `%r15` as a
scratch register. Under the redone form `%r15` is the region's base —
every load and store is `0xNN(%r15)`. If the unit overwrites `%r15`
mid-way, every later block address points somewhere else. Rule R4 in
`region36.py` therefore forbids renaming into `%r15`, and these four
units cannot be rendered without breaking that rule. They are refused
by name, not silently wrong.

## 1.2 The mechanism, one step at a time

- The region needs an anchor: some way for `0x200(%r15)` to mean "the
  result block" at run time.
- A base REGISTER was chosen (`%r15`) because it is callee-saved and
  every `disp32(base)` operand assembles as ordinary x86-64.
- The cost: one register is reserved for the whole unit. 1,775 of
  1,779 never touch it; 4 do.
- The alternative named in log_135: an ABSOLUTE virtual address range
  instead of a base register — `0x200 + BASE` as a fixed number the
  loader relocates, so no register is reserved at all.

## 1.3 The question

Should the region's base be a reserved register (`%r15`, as built:
runnable today, 4 units refused) or an absolute address range (no
register reserved, all 1,779 reachable, but every text needs a
relocation step before it runs)? The two are not a spelling choice:
they change what "runnable" means for every unit.

---

# 2. Whether temp and guard-outcome lineages are materialized

## 2.1 The instance

Population: every unit rendered under the redone form. Today's
render for c/op_31 (log_135 §3.2):

```
mov 0x0(%r15),%r10        load a from its input block
mov %r10d,0x3f8(%r15)     store into the own-address block
lea 0x3f8(%r15),%r11      take the address
mov %r11,0x200(%r15)      store the answer to the result block
ret
```

What IS written to a block here: the inputs, the result, literals,
the unit's own stack addresses. What is NOT: `%r10` and `%r11` — the
temporaries between instructions. They exist only in registers. A
guard's outcome (the flag a branch reads) is likewise allocated a
block kind but not written to it.

## 2.2 The mechanism

- the owner's statement (AgentMemory, REFINEMENT): "everything is loading
  from memory and storing in memory."
- The current render satisfies that sentence for the plumbing (how
  values arrive and leave) and not for the computation's interior
  (temporaries stay in registers).
- Completing the sentence means: after every instruction that
  produces an intermediate, store it to its temp block; before every
  instruction that consumes one, load it back. Every unit's text
  roughly doubles; every register-resident idiom disappears.
- log_135's own words on why this is not an implementation choice:
  "it rewrites the computation rather than its plumbing — so it is a
  ruling."

## 2.3 The question

Is the form's sentence satisfied by materializing inputs, result,
constants and own addresses (as built), or must every temporary and
every guard outcome also be written to its block? The second reading
is more universal and more expensive; it also changes which units
compare equal, because two units that differ only in how many
temporaries they keep would then render to different texts.

---

# 3. The 1,479 units that read a vector register's upper lanes

## 3.1 The instance

Population: the regenerated corpus, 29,288 accepted units; 1,479 of
them REFUSED. The sighting, verbatim from log_135 §4:

> Sighting: cpp/regen_12934, `pextrw $0x0,%xmm0,%eax`.

`%xmm0` is a 16-byte register. `pextrw` extracts one 16-bit lane. The
instruction as written reads lane 0, but the unit's other
instructions operate on the whole register, so the answer can depend
on bytes 8..15 — the "upper lanes".

## 3.2 The mechanism

- A block is eight bytes. An input block holds a 64-bit value.
- A vector arrival is sixteen bytes. Loading it from an eight-byte
  block loses the upper eight, and the gate cannot bind a symbol to
  bytes that have no home.
- log_135 refused these by name rather than truncating, and states
  the two ways out:
  1. the input block for a vector lineage becomes sixteen bytes; or
  2. a vector arrival is a different ARRIVAL KIND (beside
     plain / pointer / tagged), with its own block shape.
- Both change the form's vocabulary — the block-size rule or the
  arrival-kind list — which is ontology, hence a ruling.

## 3.3 The question

Do sixteen-byte values get a wider block of the same kind, or a new
arrival kind? (1) keeps one arrival vocabulary and lets block size
vary by type. (2) keeps blocks uniform and grows the arrival
vocabulary. Whichever is chosen, 1,479 refusals become attempts.

---

# 4. The swift probe emitter's `@_cdecl` test (F45-4)

## 4.1 The instance

Population: the regenerated corpus, 129,553 compiled; 276 refusals
share this one cause. log_137 §F45-4:

> the swift probe emitter's `@_cdecl` test reads the result type and
> ignores the parameter types.

Concretely: `probe_gen.py :: emit_swift` attaches `@_cdecl` (which
asks swiftc to export the function with a C calling convention) when
the RESULT type is C-representable. A 128-bit PARAMETER is not
C-representable, so swiftc refuses the whole function. The refusal is
the compiler's, but the cause is the generator's, not the operator's.

## 4.2 The mechanism

- The fix is one line of logic: attach `@_cdecl` only when the result
  AND every parameter is C-representable.
- It was NOT made in round 9, for a reason stated in log_137: changing
  the emitter changes what a future regeneration generates. The
  banked 29,288 accepted units were produced by the current emitter;
  a fixed emitter produces a different population next time.

## 4.3 The question

Fix the emitter now (so the next regeneration recovers the 276, and is
no longer byte-comparable to this one), or leave it until a
regeneration is planned anyway? This is a sequencing call, not a
design call; the fix itself is not in doubt.

---

# 5. Airlock's ten naming choices

## 5.1 The instance

Population: the ten new names the instances feature introduced
(log_138 §7). The table, verbatim:

| # | the name I used | what it names | where it would be changed |
|---|---|---|---|
| 1 | `AIRLOCK_INSTANCE` | the environment variable naming which sandbox | `instance.sh` and one `elif` in `airlock`'s `main()` |
| 2 | `--instance` | the flag spelling of the same | the same two places |
| 3 | **"instance"** as the concept word | one running sandbox | prose only — README's Instances section, and the `AL_INSTANCE` variable name |
| 4 | `instances/<name>.conf` | where an instance's settings live | one line in `instance.sh`, plus one `.gitignore` stanza |
| 5 | the conf keys — `cpus`, `memory`, `pids_limit`, `tmp_size`, `work_size`, `proxy`, `proxy_memory`, `proxy_cpus`, `proxy_pids_limit`, `allowlist_file`, `mounts_file`, `agent_dir`, `runner_image`, `proxy_image`, `persist_volume`, `persist_mode`, `lane_nice`, `script_timeout`, `watch`, `daemon_file` | each setting | one `_airlock_conf_get` call each, all in one block of `instance.sh` |
| 6 | `<instance>-runner`, `<instance>-proxy`, `<instance>-internal`, `<instance>-egress` | the derived container and network names | five lines in `airlock_instance_load` |
| 7 | `AL_*` | the variable prefix the scripts read | `instance.sh` and the scripts that use them |
| 8 | `instances/<name>/agent` | a non-default instance's lane tree | one `default_agent` branch in `instance.sh` |
| 9 | `watch = poll` / `auto` | the polling doorbell | `daemon/watcher.py`'s `open_watcher`, plus the `watch` key |
| 10 | `daemon_file` | binding a host daemon over the image's | `instance.sh` and one block in `up.sh` |

## 5.2 The mechanism

Naming is the owner's by standing ruling (AgentMemory: "the owner decides
architecture, ontology, naming"). The implementer chose working names
so the feature could be built and proved, and put each in exactly one
place so a rename is a one-line edit. Two rows are more than
spelling and are called out separately below (calls 6 and 7).

## 5.3 The question

Keep, rename, or restructure each of the ten. A "keep" on all ten is
a valid answer; the list exists so that no name became permanent by
default.

---

# 6. Whether an Airlock instance may run several lanes at once

## 6.1 The instance

Airlock's daemon (`daemon/watcher.py`) runs lanes ONE AT A TIME. The
comment in that file, quoted in log_138 §6.4.1:

> "concurrent heavy runs are what exhaust scratch space"

The round-8 fork ran six chunks at once — by bypassing the daemon with
`podman exec`. The replacement, `trickle2.py`, submits through
`airlock submit` and therefore waits for each chunk: one chunk at a
time, each chunk free to use all six capped cores itself, no overlap
between chunks.

## 6.2 The mechanism

- Serial execution is a property of the application, decided when
  Airlock was written, for a stated reason (scratch space).
- A per-instance `workers = N` key would let an instance run N lanes
  concurrently under its own cap. That is the shape log_138 names.
- It was deliberately NOT added: doing so changes Airlock's behaviour
  for every caller, which is an application decision, not something a
  project's need should force through.

## 6.3 The question

Should an instance be allowed to run N lanes concurrently (a
`workers` key, default 1), accepting the scratch-space risk the daemon
comment warns about — or does serial stay the rule and long batches
simply take longer under the cap?

---

# 7. Where an instance's agent tree lives

## 7.1 The instance

As built, a non-default instance's drop/status/logs/out tree is
`instances/<name>/agent/` INSIDE the Airlock checkout, gitignored
(`.gitignore` stanza `instances/*/`). The default instance's tree is
`agent/` at the top of the checkout, as it always was.

The fork had put its tree OUTSIDE the checkout
(`AirlockTrickle/agent`), deliberately, so the 30-second
commit daemon would never see run records.

## 7.2 The mechanism

- Inside the checkout: one place to look, `airlock doctor` finds every
  instance by listing `instances/`, and `.gitignore` keeps the daemon
  out. Cost: run records sit next to source, protected only by the
  ignore rule.
- Outside the checkout (`agent_dir` in the conf can already point
  anywhere): run records never share a directory with source, at the
  cost of a second place to look and per-machine paths in the conf.

## 7.3 The question

Is the checkout the right home for an instance's run records
(gitignored), or should the default be outside it? The conf key
already allows either; the question is which is the DEFAULT.

---

# 8. The 118 testimony findings from the assignment run

## 8.1 The instance

Population: the 336 altered-testimony findings from the `|`→`/`
substitution audit (log_126), of which 218 were superseded by verbatim
re-capture in round 8 and 118 were not. One altered record, verbatim
(log_126 §3.3):

| store | record | stored (altered) | suspected original |
|---|---:|---|---|
| op_units_rust | 178 | ``error[E0277]: no implementation for `i32 / f64` `` | ``error[E0277]: no implementation for `i32 \| f64` `` |

## 8.2 The mechanism

- Two probe runs exist. The PLAIN run (operators like `a + b`) and the
  ASSIGNMENT run (operators like `a += b`, lanes `op_asg_*`, generated
  by `asg_stage.py`, not by `probe_gen.py`).
- Round 8's regeneration and re-capture went through `probe_gen.py`,
  which EXCLUDES the assignment bucket by its own `EXCLUDED_BUCKETS`.
  So every plain-run altered record got a verbatim counterpart and was
  marked superseded; no assignment-run record did.
- The 118 = go 33 + rust 26 distinct captures, each appearing in two
  stores (`op_units_asg_*` and the `stage_asg` union copies).
- Nothing about them is unknown: the substitution is understood, the
  suspected originals are reconstructions (not testimony), and the
  three `op_asg_*` lanes still exist.

## 8.3 The question

Re-capture the three assignment lanes through the verbatim path (a
few minutes of sandbox time; the six plain lanes took 234.5 s) so the
118 are superseded like the 218 were — or leave them marked as
altered, since no derived artifact's conclusion rests on them
(log_126 §4)? Re-capture is the route that leaves testimony rather
than reconstruction; it is the same route the owner chose for the plain
run.

---

# 9. The eight calls, in one table

| # | population | what is asked | the two shapes |
|---|---|---|---|
| 1 | 4 of 1,779 original units | region base | reserved register `%r15` (4 refused) vs absolute range (relocation step) |
| 2 | every rendered unit | how far "everything stores to memory" goes | plumbing only (as built) vs every temporary and guard outcome too |
| 3 | 1,479 of 29,288 regenerated | vector arrivals | 16-byte block of the same kind vs a new arrival kind |
| 4 | 276 of 129,553 compiled | when to fix the swift emitter | now (next regeneration differs) vs with the next planned regeneration |
| 5 | 10 names | keep / rename each | any answer; listed so none is permanent by default |
| 6 | Airlock, every caller | concurrent lanes per instance | `workers` key vs serial stays |
| 7 | Airlock, every caller | default home of an instance's run records | inside checkout (gitignored, as built) vs outside |
| 8 | 118 of 336 altered captures | assignment-run testimony | re-capture three lanes vs leave marked |

Calls 1–3 change the canonical form's vocabulary and so change which
units compare equal. Calls 4 and 8 are sequencing. Calls 5–7 are
Airlock's shape as an application.
