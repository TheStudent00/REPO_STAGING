# HARVEST_constructs.md — what is left of the construct pass

## NOTHING PENDING — closed 2026-08-19

The value-grain tail described below was harvested in full. All six
steps ran, in order, with the manifest cross-check at step 3.
**481,978 of 481,978 probes, all nine checked languages COMPLETE, zero
suspect rows.** kotlin 64,782 and kv_dart_04's 8,000 were the last of
it; kotlin's re-dropped shard 05 folded once, verified by row count
against its manifest. CHECK 5t is CLOSED. The completion postscript is
at the end of
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_038_constructs_value_grain.md`.

**There is nothing pending in this file.** Everything below is kept as
the record of how it was done and as the fault list, which is still the
fault list.

---

REWRITTEN 2026-08-19 with log 038. The eight construct lanes this file
was originally written for all ran; log 037 closed them. What is left
now is the tail of the VALUE-GRAIN pass, which is a different and
smaller thing, and it is described first. The original instruction
sheet is kept below it, unchanged, because its fault list is still the
fault list.

Read `construct_design.md` for the design of record and
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_038_constructs_value_grain.md`
for what the value grain is and why it was needed.

---

## the value-grain tail — what is left

Two lanes, 72,782 probes, 15.1 percent of the pass. They are QUEUED and
RUNNING on the serial lane. Do not re-drop them; check their status
files.

```
lane              probes   as of 19:30 local
kv_kotlin_00..08  64,782   shard 00 RUNNING at 87 ms a
                           probe, eight queued behind.
                           ~105 min for acceptance,
                           plus the execution stages
kv_dart_04.sh      8,000   queued.  its six siblings
                           took about 30 s each
kv_swift_00..02   13,334   LANDED 2026-08-19 19:23 and
                           FOLDED.  855 s, 64 ms a probe
```

What is ALREADY folded, gated and in the artifacts: typescript 40,700,
csharp 85,587, java 89,698, rust 47,736, go 39,104, cpp 49,170, swift
13,334 and six of dart's seven shards, 43,867 — **409,196 rows of
481,978, 84.9 percent, every one COMPLETE and zero suspect rows**.

## the value-grain tail — how to harvest it

Every step is a script already on disk and already run once.

```
1  check state=done AND exit=0 in
   SandboxDesign/agent/status/kv_<lang>_<nn>.sh.status
   exit 0 is not evidence.  it is permission
   to look.

2  python3 l3_value_fold.py
   reads agent/out directly, no copy step.
   prints the gate and the suspect-row count.
   stop on SHORT or CONTAMINATED.

3  check the gate against the MANIFESTS.
   the gate's planned column comes from the
   shard summary lines, so an EMPTY shard file
   contributes zero planned AND zero rows and
   the gate reads COMPLETE one shard short.
   sum manifest_value_<lang>_*.json instead:
   481,978 in total, dart 51,867, kotlin
   64,782, swift 13,334.

4  python3 l3_construct_read.py
   python3 l3_value_report.py
   IN THAT ORDER.  the first rewrites
   truthiness.json at the grain its LANES
   table names; the second reads
   truthiness_holder037.json, log 037's frozen
   baseline, to say what MOVED.  pointing it
   at truthiness.json compares the run with
   itself and prints no movement at all.

5  python3 l3_construct_cluster.py
   python3 l3_joint_cluster.py
   python3 make_dendrogram_constructs.py

6  node domstub.js dendrogram_constructs.html
   expect: 1 script run, 0 threw, #count
   non-empty.  extract domstub.js from
   agent/drop/.done/*__vz_domstub.sh.
```

## two faults log 038 adds to the list below

```
a script in drop is not a script queued
    the daemon fires on a file EVENT.  ten
    shards sat in drop unrun because their
    events had been spent on an earlier run
    that refused for want of scratch.  re-write
    the file in place — cp to a temp name and
    mv it back — to fire the event again.
a baseline overwritten cannot be a baseline
    truthiness.json is rewritten by
    l3_construct_read.py at whatever grain its
    LANES table currently names.  log 037's
    holder-grain baseline is frozen separately
    as truthiness_holder037.json and movement
    is measured against that.
```

---
---

# the original sheet, kept unchanged

Written 2026-08-19 with log 036. It is the instruction sheet for the
eight construct lanes that have NOT run, so that the next session can
pick them up without reconstructing anything.

Read `construct_design.md` first. It is the design of record and this
file assumes it.

---

## what is done

Four languages are measured, gated and folded.

```
python   59,797 probes   COMPLETE   16.9 s
ruby     48,297 probes   COMPLETE    0.8 s
php      33,660 of 33,680 probes
                         20 short    10.4 s
go        1,710 probes   COMPLETE   26.8 s
```

php's twenty short probes are php FATALS. A php fatal is not catchable
and kills the process; the lane restarts past the corpse and the fatal
costs exactly one probe, which is the DEATH standing that
`answers_encoding.md` already gives such a thing. Twenty restarts, twenty
lost probes, each one recorded in the lane log with the probe number it
died on. Re-running them one at a time would recover them; nobody has.

---

## what is left

Eight languages. Each needs an acceptance lane and then an execution
lane over the probes acceptance scored ACCEPT. The probe counts are
already derived and printed by `construct_space.py`:

```
language     accept    answers
rust           2112      47746
cpp            2472      49180
swift           696      13344
dart           2675      51877
csharp         3840      85597
kotlin         2912      64782
java           4320      89857
typescript     2277      40710
```

Cost order, cheapest instrument first, which is the order to launch in:
**typescript, csharp, kotlin** (in-process checkers, route A1),
then **rust, cpp** (check-only invocation, route A2), then **dart**,
then **java**, then **swift** last because swift needs the FULL
compiler and not `-typecheck` (log 034).

---

## how to build each one

`l3_construct_go.py` is the worked example and it is meant to be copied.
It has four parts and only the first two change per language.

1. **PRELUDE** — the trace recorder and the value encoder, written in
   that language, producing `answers_encoding.md` payloads. go's is 60
   lines of reflection. Each language needs its own; the encodings are
   fixed and listed in `answers_encoding.md`.
2. **SCAF** — the scaffold per construct, in that language's syntax.
   Fixed, minimal, inert (decision 4). Skip any construct the catalogue
   marks ABSENT for that language.
3. **gen_acceptance** — unchanged. It walks holders and holder pairs and
   fills the slots.
4. **the lane driver** — replace `go build` with that language's own
   proven instrument. The commands are already written and proven in
   `lanes/ac_<lang>.sh` from the operator pass; lift the command, not
   the probe generation.

---

## the faults not to repeat

Every one of these has already cost a run once.

```
scratch fills silently
    /work is memory backed and capped at
    4 GB.  check `df -Pm /work` at the head
    of the lane, which every generated lane
    already does, and read it.
exit 0 is not evidence
    a lane can be killed mid-run and still
    exit 0.  the completeness gate in
    l3_construct_read.py is the evidence.
dead-code lint severity
    dart scores a legal probe as refused
    unless the lint severity is lowered.
    see lanes/dx_dart_lints.sh.
word operators need parentheses
    php and ruby.  the construct scaffolds
    already parenthesise every slot.
-typecheck is not the swift compiler
    swiftc -typecheck accepts lines the full
    compiler refuses.  use the full compiler
    and record CODEGEN_REFUSE.
positional ids need manifests
    every lane freezes
    manifest_construct_<lang>.json before it
    runs.  do not skip it.
imports live at the file head
    go, and the same shape in java and rust.
    a holder's `pre` line is an import and
    must be lifted out of the function body.
    this cost the go lane two runs.
a class cannot be declared twice
    php and java.  the declared name is
    suffixed per probe.  see uniqcls() in
    the php driver.
ruby interpolates in double quotes
    a scaffold written as a double-quoted
    ruby string has its `#{...}` evaluated
    when the DRIVER is parsed, not when the
    probe runs.  escape it.  this cost the
    ruby lane one run.
```

---

## how to fold what comes back

Add the language to `LANES` in `l3_construct_read.py`, with grain
`holder` for a statically checked language and `value` for an executed
one. Then:

```
python3 l3_construct_read.py
```

which re-runs the gate over everything, rewrites the construct
signatures, and rebuilds `truthiness_table.md` and `trace_compare.md`
with the new language filled in. Nothing else needs touching.
