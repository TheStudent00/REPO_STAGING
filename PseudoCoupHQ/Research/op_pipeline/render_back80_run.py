#!/usr/bin/env python3
"""render_back80_run.py -- the driver for TASK 80: the same return
path as round 13, now with the CONDITIONAL template the one fixed rule
gained (`term.RenderBack.emit_condition` / `.emit_choice`).

CORE:
`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_6_term/node_0_3_5_6_5_render_back/CORE_0_3_5_6_5_render_back.md`

WHAT IS REUSED RATHER THAN COPIED.  This file imports
`render_back_run` and calls its `Assembler` (the `as` / `objdump -d`
round trip over `CanonicalForm.write_batch`), its `one_unit` (render,
wrap, assemble, gate), its `proved_terms_of` and its `new_tools`.
Nothing of the round-13 driver is re-typed here; what is new is only
WHERE the answers are written, so round 13's own store stays on disk
untouched as the record it is.

TWO POPULATIONS, the same two round 13 reported:

  1. the 158 members of pool entry `E00029` (one layer-5 text
     `v0 + v1`, seven languages) -- written to
     `render_back80_E00029.json`;
  2. every proved term of the whole population -- the 26,040 units of
     the 30,432 canon39-proved ones whose layer-4 term was proved --
     written to `render_back80_store/`, one shard per file.

MEMORY BOUND, stated as the round requires: one canon39 shard is
opened, walked and dropped before the next; the largest on disk is
under 5 MB and the store shard written back is of the same order.  The
bound is 6 GB resident, checked after every shard, with the named
abort `ABORT_MEMORY`.  The sample run of the first shard is pasted in
the report with its peak resident size.

ONE PROCESS.  Resumable: `render_back80_state.json` names the shards
already written.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

No operator token appears in this file.  The `operator` field of a unit
record is a display label this file copies onto the member and never
reads, never groups on and never pairs on.

Coding discipline: no compound one-liner statements.
"""

import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import render_back_run as RB                                     # noqa: E402

STORE = os.path.join(HERE, "render_back80_store")
STATE = os.path.join(HERE, "render_back80_state.json")
ENTRY_OUT = os.path.join(HERE, "render_back80_E00029.json")
POOL = os.path.join(HERE, "pool61.json")

MEMORY_CAP_KB = 6 * 1024 * 1024
PROVED = "WRAPPED_TEXT_PROVED"


def check_memory():
    used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if used > MEMORY_CAP_KB:
        raise SystemExit(
            "ABORT_MEMORY: peak resident %d kB passed the stated cap "
            "of %d kB" % (used, MEMORY_CAP_KB))
    return used


def load_state():
    if not os.path.exists(STATE):
        return {"done": [], "started": time.time()}
    return json.load(open(STATE))


def save_state(state):
    handle = open(STATE, "w")
    json.dump(state, handle, indent=1, sort_keys=True)
    handle.close()


def walk_one_shard(path, tools, assembler):
    """one canon39 shard -> its store shard.  The body of the loop is
    `render_back_run.one_unit`, called and not copied."""
    maker, renderer, gate, form = tools
    document = json.load(open(path))
    wanted = RB.proved_terms_of(path)
    out = {}
    skipped = 0
    for name in sorted(document.get("units", {})):
        unit = document["units"][name]
        if unit.get("outcome") != PROVED:
            continue
        record = wanted.get(name)
        if record is None:
            skipped = skipped + 1
            continue
        out[name] = RB.one_unit(maker, renderer, gate, name, unit,
                                record)
    rendered = []
    for name in sorted(out):
        if out[name].get("rendered_wrapped_text") is None:
            continue
        rendered.append((name, out[name]["rendered_wrapped_text"]))
    said = assembler.run(rendered)
    for name in said:
        out[name]["assembly"] = said[name]
    return out, skipped, len(rendered)


def run(budget_seconds):
    if not os.path.isdir(STORE):
        os.makedirs(STORE)
    state = load_state()
    done = set(state["done"])
    tools = RB.new_tools()
    assembler = RB.Assembler(tools[3])
    started = time.time()
    every = RB.shards()
    for path in every:
        key = os.path.relpath(path, HERE)
        if key in done:
            continue
        if time.time() - started > budget_seconds:
            print("budget spent; %d shards still to walk"
                  % (len(every) - len(done)))
            sys.stdout.flush()
            return False
        out, skipped, rendered = walk_one_shard(path, tools,
                                                assembler)
        written = os.path.join(STORE, key.replace("/", "__"))
        handle = open(written, "w")
        json.dump({"shard": key,
                   "skipped_no_proved_term": skipped,
                   "units": out}, handle, sort_keys=True)
        handle.close()
        done.add(key)
        state["done"] = sorted(done)
        save_state(state)
        peak = check_memory()
        print("%s: %d with proved terms, %d rendered, %d skipped, "
              "peak %d kB" % (key, len(out), rendered, skipped, peak))
        sys.stdout.flush()
    print("all %d shards walked" % len(done))
    return True


# ------------------------------------------------------------------
# POPULATION ONE -- the members of pool entry E00029
# ------------------------------------------------------------------

def entry_members():
    """the member names of pool entry `E00029`, read by round 13's own
    `members_of_the_entry` rather than by a second reader written here.
    The entry is named by its ID, which is a machine-form key: no token
    is read."""
    import render_back_E00029 as RBE
    members, entry = RBE.members_of_the_entry()
    return members


def run_entry():
    members = entry_members()
    if members is None:
        print("pool entry E00029 was not found in %s" % POOL)
        return
    wanted = set(members)
    tools = RB.new_tools()
    maker, renderer, gate, form = tools
    assembler = RB.Assembler(form)
    out = {}
    for path in RB.shards():
        document = json.load(open(path))
        found = wanted & set(document.get("units", {}))
        if not found:
            continue
        terms = RB.proved_terms_of(path)
        for name in sorted(found):
            unit = document["units"][name]
            record = terms.get(name)
            if record is None:
                continue
            out[name] = RB.one_unit(maker, renderer, gate, name, unit,
                                    record)
    rendered = []
    for name in sorted(out):
        if out[name].get("rendered_wrapped_text") is None:
            continue
        rendered.append((name, out[name]["rendered_wrapped_text"]))
    said = assembler.run(rendered)
    for name in said:
        out[name]["assembly"] = said[name]
    handle = open(ENTRY_OUT, "w")
    json.dump({"entry": "E00029",
               "members_named_by_the_pool": len(members),
               "units": out}, handle, indent=1, sort_keys=True)
    handle.close()
    print("E00029: %d members walked, %d rendered"
          % (len(out), len(rendered)))


if __name__ == "__main__":
    which = "two"
    budget = 36000
    if len(sys.argv) > 1:
        which = sys.argv[1]
    if len(sys.argv) > 2:
        budget = int(sys.argv[2])
    if which == "one":
        run_entry()
        sys.exit(0)
    finished = run(budget)
    if not finished:
        sys.exit(3)
