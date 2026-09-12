#!/usr/bin/env python3
"""rv4_off.py -- THE TIMED ROUND: every RISC-V cell whose term the lifter
states, on every target that has no proved certificate for it, rendered by
the general tier, compiled for riscv64 WITH OPTIMIZATION OFF, carved, walked
through the RISC-V reference and gated -- eight worker processes, a hard
wall clock of nine minutes, and a row for every pair the clock did not
reach.

Node: hq.research.arch_unit_oracle.architectures.riscv64
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/PROGRESS.md`).
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_rv4_brief.md`.
Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, all of it.

WHAT THIS FILE IS, one sentence: a DRIVER BESIDE `rv_general.py` -- task
t4's RISC-V leg, which is imported and CALLED here and not rewritten --
that changes exactly three things about a run of it and measures what that
does.

THE THREE THINGS, each with its reason.
  1. THE COMPILE IS OPTIMIZATION-OFF.  Task t4 measured the cause of its
     misses: the body is checked at SHIPPING optimization, where the
     compiler rewrites a gate-level multiplier into another multiplier and
     z3 cannot decide the two are equal.  the owner's ruling of 2026-09-11 is
     that this is a flag and not a research problem -- compile the backstop
     with optimization off, so the body follows the source one statement at
     a time.  The routes below are task rv3's own four routes
     (`inherit_rv3.py`), with the optimization level and NOTHING ELSE
     changed.
  2. THE GATE TRIES THE TEXT FIRST.  `Term.normalize` prints a term to a
     canonical text; two terms with the same text are the same computation
     and no solver call is needed.  `rv_general.py` states in its own
     docstring why it does not print: the multiplier at 8 bits is 190
     distinct nodes and at or above 200,000 written out.  So the shortcut
     here is BOUNDED BY THREE MEASURED NUMBERS (distinct nodes,
     printed size and depth): a term
     above it is not printed at all and goes straight to the solver.  The
     shortcut is installed as a wrapper around `inherit.decide`, so the
     machinery it wraps is unchanged.
  3. THE RUNS ARE SPREAD OVER EIGHT WORKER PROCESSES and every one of them
     reads the wall clock before each pair.  At the deadline a worker stops
     cleanly and the rest of its slice is written out as
     NOT_REACHED_IN_BUDGET.  Nothing is dropped silently.

THE OBJECTS, one sentence each, in relation.
  * A CELL is one (`mnem`, operand shape, `key_width`) row of
    `model_table_rv.json`, and `twins.json` holds one row per cell -- 255
    of them.
  * THE POPULATION is every cell whose term the lifter states AND whose
    written place is one a compiled function answers in, paired with each
    of the three compiled targets that has no proved certificate for it in
    task rv2's loop store, task rv3's inheritance store or task t4's
    general-tier store.
  * THE RENDER is `render_general.render` under the `native_first` policy:
    the target's own operator where it has one, the backstop construction
    where it has none.
  * THE COMPILE, THE CARVE, THE WALK AND THE GATE are `rv_general.one_run`,
    called, with the three changes above installed on the modules it calls.

WHAT DECIDES THE POPULATION IS MACHINE FORM, NEVER A NAME.  A cell is left
out when its written place is not a place the calling convention answers in
(the model table's own place name begins `mem_` or is the branch
condition), or when the reference's own `reads` field for that cell names
memory or the program counter.  Those two fields are the reference's own
structural statement about the instruction; no mnemonic is matched anywhere
in this file.

MEMORY: bound 6 GB resident PER WORKER, named abort ABORT_MEMORY_RV4,
checked after every run.  The instance's own ceiling is 20g for all eight
workers together and is stated in `instances/rv4.conf`.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope, anywhere
in this line -- not in matching, not in "which pairs get compared", not in
report rows, not in dropdowns.  The candidate set for comparison comes from
machine-form evidence (clusters, connections, type pairs) or from ratified
intention -- never from the token.  The token appears exactly once per
unit: as a display label on the member.  HISTORY OF VIOLATIONS, so the
pattern is visible: (1) the arch campaign's cross-language matrix (caught
by the owner 2026-08-24); (2) verdicts.py's row pairing (caught by the owner
2026-08-25 -- the fix brief itself reintroduced it as "same-operator
pairs").  MECHANICAL GUARD REQUIRED: every pipeline stage that groups or
pairs units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste this
paragraph verbatim."

usage:
  rv4_off.py population <project root> <out population.json>
  rv4_off.py sample <project root> <population.json> <count> <prefix>
                    <src dir> <work root>
  rv4_off.py shard <project root> <population.json> <index> <count>
                   <deadline epoch seconds> <prefix> <src dir> <work root>
  rv4_off.py round <project root> <population.json> <workers>
                   <budget seconds> <prefix> <src dir> <work root>
  rv4_off.py tables <project root> <population.json> <prefix>

Coding discipline (the owner's ruling): no compound one-liner statements.
"""

import json
import os
import resource
import signal
import subprocess
import sys
import time

STARTED = time.time()
"""the driver's own clock: the nine minutes are measured from the moment
this process began, so the setup is inside the budget and not beside it."""

ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_RV4"
SOLVER_MS = 3000
TARGETS = ["c", "go", "rust"]
POLICY = "native_first"

TEXT_NODE_CEILING = 20000
TEXT_TREE_CEILING = 20000
TEXT_DEPTH_CEILING = 60
"""the three ceilings the identical-text shortcut is bounded by: distinct
nodes over the shared graph, PRINTED size (the same graph expanded into the
tree the printer writes), and DEPTH.

`rv_general.py` measured the first reason: a multiplier at 8 bits is 190
distinct nodes and at or above 200,000 characters written out, so printing
is not free.  The first round of this task (lane `rv4_l2`) measured the
second and third: a node count alone bounds nothing, because the printer
expands the shared graph, and the printer is recursive, so a term deeper
than the interpreter's own stack allows raises
`ctypes.ArgumentError: argument 1: RecursionError` after it has already
spent the time.  A term above any of the three is not printed and the
solver is asked instead."""

CAUSE_TEXT_TOO_LARGE = ("the term is above one of the identical-text "
                        "shortcut's three ceilings -- distinct nodes, "
                        "printed size, depth -- so the text was not "
                        "taken and the solver was asked")

ANSWER_HOME = "a0"
"""the register the riscv64 calling convention answers in for a rendered
emulation.  Every place is rendered into a general-register answer (the
render is handed the place under the general home `reg_rdi`, which is
`rv_general.one_run`'s own choice and is unchanged here), so a float place's
emulation answers in `a0` like any other."""


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    peak = peak_kb()
    if peak > ABORT_KB:
        raise SystemExit("%s: %d kB at %s" % (ABORT_NAME, peak, where))
    return peak


def paths_of(root):
    out = {}
    out["root"] = root
    out["op"] = os.path.join(root, "Research", "op_pipeline")
    out["emulation"] = os.path.join(root, "Research", "oracle",
                                    "cross_construction", "emulation")
    out["riscv"] = os.path.join(root, "Research", "oracle", "riscv")
    out["general"] = os.path.join(out["emulation"], "construct", "general")
    out["twins"] = os.path.join(out["riscv"], "twins.json")
    out["model_table"] = os.path.join(out["riscv"], "model_table_rv.json")
    out["rv2_store"] = os.path.join(out["riscv"], "rv_loop.jsonl")
    out["rv3_store"] = os.path.join(out["riscv"],
                                    "certificates_riscv64_rv3.jsonl")
    out["t4_store"] = os.path.join(out["general"], "rv_general.jsonl")
    return out


# ==================================================================
# section 1: the three changes, installed on the machinery that is
# called
# ==================================================================

SHIP_C_OFF = ["-std=c17", "-O0", "--target=riscv64-linux-gnu",
              "--gcc-toolchain=/usr"]
RUST_OFF = ["--crate-type=lib", "--emit=obj", "-C", "opt-level=0",
            "-C", "debug-assertions=off",
            "--target=riscv64gc-unknown-linux-gnu"]
GO_OFF = ["-gcflags", "all=-N -l"]

TRIPLES_OFF = {
    "c": "riscv64-linux-gnu (clang --target, --gcc-toolchain=/usr, -O0)",
    "rust": "riscv64gc-unknown-linux-gnu (rustc --target, --emit=obj, "
            "-C opt-level=0)",
    "go": "GOARCH=riscv64 GOOS=linux (go build -gcflags='all=-N -l')",
}

KEPT_SOURCES = {"dir": None}
"""where each rendered source is kept, so the record holds the source the
compiler was handed and not only its verdict."""

COMPILE_SECONDS = {"last": None}

SHORTCUT = {"calls": []}
"""the identical-text shortcut's own record for the run in hand: one entry
per gate call, saying whether the text decided it and what it cost."""


def keep_source(label, source, suffix):
    where = KEPT_SOURCES.get("dir")
    if not where:
        return None
    if not os.path.isdir(where):
        os.makedirs(where, exist_ok=True)
    path = os.path.join(where, "%s%s" % (label, suffix))
    handle = open(path, "w")
    handle.write(source)
    handle.close()
    return path


def compile_and_carve_off(source, target, work):
    """(the carved body, the compile command, the diagnostic) for one
    rendered source aimed at riscv64 WITH OPTIMIZATION OFF.

    Task rv3's four routes, with the optimization level and nothing else
    changed, and the clang route's own `-nostdlibinc` already dropped by
    rv3 in favour of the riscv64 gcc toolchain's headers."""
    import riscv_carve as CARVE
    import inherit as INH
    if not os.path.isdir(work):
        os.makedirs(work, exist_ok=True)
    name = INH.symbol_of(source)
    if name is None:
        return None, "", "no emu_ symbol found in the rendered source"
    started = time.time()
    got = None
    if target == "c":
        path = os.path.join(work, "unit.c")
        obj = os.path.join(work, "unit.o")
        open(path, "w").write(source)
        keep_source(name, source, ".c")
        command = [CARVE.CLANG] + SHIP_C_OFF + ["-c", path, "-o", obj]
        rc, out, err = CARVE.sh(command, timeout=compile_seconds())
        COMPILE_SECONDS["last"] = round(time.time() - started, 3)
        if rc != 0:
            return None, " ".join(command), (err or out)
        got, err = CARVE.disassemble(obj, name, True)
        if got is None:
            return None, " ".join(command), err
        return got, " ".join(command), ""
    if target == "rust":
        path = os.path.join(work, "unit.rs")
        obj = os.path.join(work, "unit_rs.o")
        open(path, "w").write(source)
        keep_source(name, source, ".rs")
        command = ["rustc"] + RUST_OFF + ["-o", obj, path]
        rc, out, err = CARVE.sh(command, timeout=compile_seconds())
        COMPILE_SECONDS["last"] = round(time.time() - started, 3)
        if rc != 0:
            return None, " ".join(command), (err or out)
        got, err = CARVE.disassemble(obj, name, False)
        if got is None:
            return None, " ".join(command), err
        return got, " ".join(command), ""
    if target == "go":
        open(os.path.join(work, "go.mod"), "w").write(CARVE.GOMOD)
        open(os.path.join(work, "main.go"), "w").write(source)
        keep_source(name, source, ".go")
        obj = os.path.join(work, "bin_rv")
        command = ["go", "build"] + GO_OFF + ["-o", obj, "."]
        rc, out, err = CARVE.sh(command, cwd=work, env=CARVE.GO_ENV,
                                timeout=compile_seconds())
        COMPILE_SECONDS["last"] = round(time.time() - started, 3)
        printed = "GOARCH=riscv64 GOOS=linux " + " ".join(command)
        if rc != 0:
            return None, printed, (err or out)
        got, err = CARVE.disassemble(obj, "main." + name, True)
        if got is None:
            return None, printed, err
        return got, printed, ""
    return None, "", "no riscv64 route for target %r" % target


DEADLINE = {"at": None}


def compile_seconds():
    """the compiler's own timeout, cut to what is left of the budget.

    A pair that starts just before the deadline must not carry the lane
    past it, so the compiler is given the smaller of its usual ceiling and
    the time that remains, with a floor so a build is never given an
    impossible one."""
    usual = 120
    if DEADLINE["at"] is None:
        return usual
    left = DEADLINE["at"] - time.time()
    if left >= usual:
        return usual
    if left < 20:
        return 20
    return int(left)


def triple_of_off(target):
    return TRIPLES_OFF.get(target)


def shape_of(term, node_ceiling, tree_ceiling, depth_ceiling):
    """(distinct nodes, printed size, depth) for one term, each counted
    over the SHARED graph with a memo and each saturating at its own
    ceiling, so the measurement itself is bounded.

    WHY THREE NUMBERS AND NOT ONE, and it is the defect the first round
    measured (lane `rv4_l2`, worker 4): the distinct-node count bounds
    nothing about printing.  `z3`'s printer expands the shared graph into
    a TREE, so a term of 190 distinct nodes can print as hundreds of
    thousands of characters, and `term.ordering_key` builds a key string
    the same way.  The printer is also RECURSIVE, several Python frames
    per level, so a DEEP term exhausts the interpreter's own stack before
    it exhausts memory -- which is what
    `ctypes.ArgumentError: argument 1: RecursionError` was, thirty times
    in one worker.  So the shortcut is offered a term only when its
    PRINTED SIZE and its DEPTH are both under a ceiling."""
    nodes = {}
    order = []
    stack = [(term, False)]
    while stack:
        node, expanded = stack.pop()
        key = node.get_id()
        if key in nodes and nodes[key] is not None:
            continue
        try:
            below = node.children()
        except Exception:                                     # noqa: BLE001
            below = []
        if not expanded:
            if key in nodes:
                continue
            nodes[key] = None
            if len(nodes) > node_ceiling:
                return len(nodes), tree_ceiling + 1, depth_ceiling + 1
            stack.append((node, True))
            for sub_node in below:
                stack.append((sub_node, False))
                continue
            continue
        size = 1
        deep = 1
        for sub_node in below:
            held = nodes.get(sub_node.get_id())
            if held is None:
                held = (1, 1)
            size = size + held[0]
            if held[1] + 1 > deep:
                deep = held[1] + 1
            continue
        if size > tree_ceiling:
            size = tree_ceiling + 1
        if deep > depth_ceiling:
            deep = depth_ceiling + 1
        nodes[key] = (size, deep)
        order.append(key)
        continue
    held = nodes.get(term.get_id())
    if held is None:
        return len(nodes), tree_ceiling + 1, depth_ceiling + 1
    return len(nodes), held[0], held[1]


HOLDER = {"term": None}


def holder_of():
    """the one `term.Term` this process prints with.  It is built ONCE:
    `Term.__init__` reads a json document off disk, and the first round
    built one per gate call."""
    if HOLDER["term"] is None:
        import term as TERMS
        HOLDER["term"] = TERMS.Term()
    return HOLDER["term"]


def decide_with_the_text_first(left, right, timeout_ms):
    """`inherit.decide`, with `Term.normalize` asked first.

    THE SHORTCUT IS THE BRIEF'S OWN LINE: if the two terms print the same
    canonical text they are the same computation and no solver is called.
    A term whose printed size or whose depth is above the ceilings is not
    printed at all and goes straight to the solver, and the row says which
    ceiling it was."""
    import inherit as INH
    record = {"text_taken": False, "cause": None, "seconds": 0.0,
              "left_nodes": None, "right_nodes": None,
              "left_printed": None, "right_printed": None,
              "left_depth": None, "right_depth": None}
    started = time.time()
    try:
        left_shape = shape_of(left, TEXT_NODE_CEILING, TEXT_TREE_CEILING,
                              TEXT_DEPTH_CEILING)
        right_shape = shape_of(right, TEXT_NODE_CEILING,
                               TEXT_TREE_CEILING, TEXT_DEPTH_CEILING)
    except Exception as problem:                              # noqa: BLE001
        record["cause"] = "%s: %s" % (type(problem).__name__,
                                      ("%s" % problem)[:200])
        record["seconds"] = round(time.time() - started, 3)
        SHORTCUT["calls"].append(record)
        return INH.decide(left, right, timeout_ms)
    record["left_nodes"] = left_shape[0]
    record["right_nodes"] = right_shape[0]
    record["left_printed"] = left_shape[1]
    record["right_printed"] = right_shape[1]
    record["left_depth"] = left_shape[2]
    record["right_depth"] = right_shape[2]
    too_large = False
    if left_shape[1] > TEXT_TREE_CEILING or right_shape[1] > TEXT_TREE_CEILING:
        too_large = True
    if left_shape[2] > TEXT_DEPTH_CEILING or right_shape[2] > TEXT_DEPTH_CEILING:
        too_large = True
    if left_shape[0] > TEXT_NODE_CEILING or right_shape[0] > TEXT_NODE_CEILING:
        too_large = True
    if too_large:
        record["cause"] = CAUSE_TEXT_TOO_LARGE
        record["seconds"] = round(time.time() - started, 3)
        SHORTCUT["calls"].append(record)
        return INH.decide(left, right, timeout_ms)
    try:
        holder = holder_of()
        same = holder.normalize(left) == holder.normalize(right)
    except Exception as problem:                              # noqa: BLE001
        record["cause"] = "%s: %s" % (type(problem).__name__,
                                      ("%s" % problem)[:200])
        record["seconds"] = round(time.time() - started, 3)
        SHORTCUT["calls"].append(record)
        return INH.decide(left, right, timeout_ms)
    record["seconds"] = round(time.time() - started, 3)
    if same:
        record["text_taken"] = True
        SHORTCUT["calls"].append(record)
        return "PROVED", None
    record["cause"] = "the two texts differ, so the solver was asked"
    SHORTCUT["calls"].append(record)
    return INH.decide(left, right, timeout_ms)


def install(paths):
    """put the three changes in place on the machinery that is called, and
    leave everything else of `rv_general.py`, `inherit.py` and
    `render_general.py` alone."""
    import inherit as INH
    import rv_general as RVG
    INH.compile_and_carve = compile_and_carve_off
    INH.triple_of = triple_of_off
    INH.decide = decide_with_the_text_first
    RVG.INH = INH
    RVG.POLICIES = (POLICY,)
    RVG.ABORT_NAME = ABORT_NAME
    RVG.SOLVER_MS = SOLVER_MS
    import claim_check as CC
    for target in ("rust",):
        CC.X86_INTEGER[target] = list(CC.X86_INTEGER["c"])
        CC.X86_FLOAT[target] = list(CC.X86_FLOAT["c"])
        CC.RISCV_INTEGER[target] = list(CC.RISCV_INTEGER["c"])
        CC.RISCV_FLOAT[target] = list(CC.RISCV_FLOAT["c"])
        continue
    return INH, RVG


def bring_in(paths):
    """every module this driver calls, imported in the one order that
    chooses the reference before anything that imports it runs."""
    sys.path.insert(0, paths["general"])
    sys.path.insert(0, os.path.join(paths["emulation"], "construct"))
    sys.path.insert(0, paths["riscv"])
    sys.path.insert(0, os.path.join(paths["emulation"], "handful"))
    sys.path.insert(0, os.path.join(paths["emulation"], "autopoly"))
    sys.path.insert(0, paths["emulation"])
    sys.path.insert(0, os.path.join(paths["emulation"], "rust"))
    sys.path.insert(0, os.path.join(paths["emulation"], "go"))
    sys.path.insert(0, os.path.join(paths["emulation"], "swift"))
    import twins as TW
    got = TW.bring_in(paths["op"], paths["op"])
    digest = got[4]
    import rv_loop as RL
    import riscv_reference as RV_REF
    import handful as H
    import construct as CONS
    import rv_general as RVG
    INH, RVG = install(paths)
    held = {"RL": RL, "RV_REF": RV_REF, "H": H, "CONS": CONS,
            "RVG": RVG, "INH": INH, "digest": digest}
    return held


# ==================================================================
# section 2: the population -- machine form only
# ==================================================================

ANSWER_PLACES = ("reg_", "freg_")
"""the two place kinds a compiled function answers in.  A place named
`mem_...` is a store and a place named `branch_condition` is a branch: no
compiled function's answer carries either, so neither is in the population.
This is the model table's own place name, not a mnemonic."""

CAUSE_NOT_AN_ANSWER_PLACE = ("the cell's written place is not a place a "
                             "compiled function's answer arrives in")
CAUSE_READS_MEMORY = ("the reference's own reads field for this cell names "
                      "memory, so the cell's term is not a function of its "
                      "arguments alone")
CAUSE_READS_THE_COUNTER = ("the reference's own reads field for this cell "
                           "names the program counter, so the cell's term "
                           "is not a function of its arguments alone")
CAUSE_NO_TERM = "the lifter states no term for this cell's written place"


def model_rows(path):
    """(cell key) -> the model table's own row for it, first row wins,
    which is `rv_loop.riscv_terms`'s own rule."""
    out = {}
    document = json.load(open(path))
    for row in document["rows"]:
        if row["outcome"] != "TRANSLATED":
            continue
        if not row.get("mapping"):
            continue
        key = (row["mnem"], row["shape"], row["key_width"])
        if key in out:
            continue
        out[key] = row
        continue
    return out


def proved_before(paths):
    """(target) -> the set of cell keys that already carry a proved
    certificate on that target, over the three stores of record."""
    out = {}
    sources = [("rv2", paths["rv2_store"], ("proved",)),
               ("rv3", paths["rv3_store"], ("proved",)),
               ("t4", paths["t4_store"], ("proved",))]
    where = {}
    for name, path, kinds in sources:
        if not os.path.exists(path):
            continue
        handle = open(path)
        for line in handle:
            text = line.strip()
            if not text:
                continue
            row = json.loads(text)
            if row.get("kind") not in kinds:
                continue
            cell = row.get("cell") or {}
            if not cell:
                continue
            key = (cell.get("mnem"), cell.get("shape"),
                   cell.get("key_width"))
            target = row.get("target")
            held = out.setdefault(target, set())
            held.add(key)
            where.setdefault((target, key), []).append(name)
            continue
        handle.close()
        continue
    return out, where


def union_of_the_stores(paths):
    """(the union of cells with a proved riscv64 emulation before this
    round, and the three sets it is made of).

    THE READING IS TASK t4's OWN, so the number stands beside its 119:
    task rv2's loop store counts a cell when its row is `proved`; task
    rv3's inheritance store counts a cell when its row is `proved` or
    `agreed` (an `agreed` row is one of the 434 interpreted targets whose
    certificate transfers unchanged); task t4's general-tier store counts
    a cell when its row is `proved`.  `rv_general.py count` prints the
    same three sets from the same three files."""
    held = {}
    held["rv2"] = set()
    held["rv3"] = set()
    held["t4"] = set()
    plan = [("rv2", paths["rv2_store"], ("proved",)),
            ("rv3", paths["rv3_store"], ("proved", "agreed")),
            ("t4", paths["t4_store"], ("proved",))]
    for name, path, kinds in plan:
        if not os.path.exists(path):
            continue
        handle = open(path)
        for line in handle:
            text = line.strip()
            if not text:
                continue
            row = json.loads(text)
            if row.get("kind") not in kinds:
                continue
            cell = row.get("cell") or {}
            if not cell:
                continue
            held[name].add((cell.get("mnem"), cell.get("shape"),
                            cell.get("key_width")))
            continue
        handle.close()
        continue
    whole = set()
    for name in held:
        for key in held[name]:
            whole.add(key)
            continue
        continue
    return whole, held


def population_command(root, out_path):
    paths = paths_of(root)
    held = bring_in(paths)
    RL = held["RL"]
    say("[1/3] the cells and the terms the lifter states")
    document = json.load(open(paths["twins"]))
    cells = []
    for row in document["rows"]:
        cells.append({"mnem": row["mnem"], "shape": row["shape"],
                      "key_width": row["key_width"],
                      "places": [p["writes"] for p in row["places"]]})
        continue
    say("   %d cells in twins.json" % len(cells))
    terms, _operands = RL.riscv_terms(paths["model_table"])
    table = model_rows(paths["model_table"])
    say("   %d (cell, place) terms the lifter states" % len(terms))

    say("[2/3] the population, decided on machine form")
    rows = []
    left_out = []
    for cell in cells:
        key = (cell["mnem"], cell["shape"], cell["key_width"])
        row = table.get(key)
        reads = []
        row_id = None
        builder = None
        if row is not None:
            reads = row.get("reads") or []
            row_id = row.get("row_id")
            builder = row.get("builder")
        reads_memory = False
        reads_counter = False
        for what in reads:
            if "memory" in what:
                reads_memory = True
            if "program counter" in what:
                reads_counter = True
            continue
        for place in cell["places"]:
            record = {"mnem": cell["mnem"], "shape": cell["shape"],
                      "key_width": cell["key_width"], "place": place,
                      "row_id": row_id, "builder": builder,
                      "reads": reads}
            answer_place = False
            for prefix in ANSWER_PLACES:
                if place.startswith(prefix):
                    answer_place = True
                continue
            if terms.get((key, place)) is None:
                record["cause"] = CAUSE_NO_TERM
                left_out.append(record)
                continue
            if not answer_place:
                record["cause"] = CAUSE_NOT_AN_ANSWER_PLACE
                left_out.append(record)
                continue
            if reads_memory:
                record["cause"] = CAUSE_READS_MEMORY
                left_out.append(record)
                continue
            if reads_counter:
                record["cause"] = CAUSE_READS_THE_COUNTER
                left_out.append(record)
                continue
            record["float_place"] = place.startswith("freg_")
            record["float_operands"] = "fpr" in cell["shape"]
            rows.append(record)
            continue
        continue
    say("   %d cells in the population, %d left out"
        % (len(rows), len(left_out)))

    say("[3/3] the pairs: each population cell on each target with no "
        "proved certificate")
    already, where = proved_before(paths)
    pairs = []
    for record in rows:
        key = (record["mnem"], record["shape"], record["key_width"])
        for target in TARGETS:
            held_set = already.get(target) or set()
            if key in held_set:
                continue
            pair = dict(record)
            pair["target"] = target
            pair["unproved_before"] = "no proved certificate on this "\
                                      "target in any of the three stores"
            pairs.append(pair)
            continue
        continue
    pairs.sort(key=lambda item: (item["row_id"] or "", item["place"],
                                 item["target"]))
    for index, pair in enumerate(pairs):
        pair["number"] = index
        continue
    census = {}
    for record in left_out:
        census[record["cause"]] = census.get(record["cause"], 0) + 1
        continue
    by_builder = {}
    for record in rows:
        by_builder[record["builder"]] = by_builder.get(record["builder"],
                                                       0) + 1
        continue
    by_target = {}
    for pair in pairs:
        by_target[pair["target"]] = by_target.get(pair["target"], 0) + 1
        continue
    proved_counts = {}
    for target in TARGETS:
        proved_counts[target] = len(already.get(target) or set())
        continue
    document = {
        "meta": {
            "task": "rv4",
            "what": "every RISC-V cell whose term the lifter states, on "
                    "each of the three compiled targets that has no "
                    "proved certificate for it",
            "targets": list(TARGETS),
            "cells_in_twins": len(cells),
            "cells_in_the_population": len(rows),
            "cells_left_out": len(left_out),
            "left_out_by_cause": census,
            "population_by_builder": by_builder,
            "pairs": len(pairs),
            "pairs_by_target": by_target,
            "cells_already_proved_by_target": proved_counts,
            "x86_reference_sha256": held["digest"],
            "peak_kb": peak_kb(),
            "memory_bound_kb": ABORT_KB,
            "memory_abort": ABORT_NAME,
            "seconds": round(time.time() - STARTED, 1),
        },
        "rows": pairs,
        "left_out": left_out,
    }
    handle = open(out_path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    say("   %d pairs written to %s" % (len(pairs), out_path))
    for cause in sorted(census):
        say("   left out: %-70s %d" % (cause[:70], census[cause]))
        continue
    for target in TARGETS:
        say("   pairs on %-5s %d (cells already proved there: %d)"
            % (target, by_target.get(target, 0), proved_counts[target]))
        continue
    say("peak RSS: %d kB" % peak_kb())
    return 0


# ==================================================================
# section 3: one pair, and one worker's slice of them
# ==================================================================

def outcome_of(row, took_the_text):
    """the brief's own five verdicts, read off the attempt the machinery
    returned."""
    verdict = row.get("verdict") or {}
    outcome = verdict.get("outcome")
    if outcome == "PROVED":
        if took_the_text:
            return "PROVED_IDENTICAL"
        return "PROVED"
    if outcome == "DISPROVED":
        return "DISPROVED"
    if outcome == "UNDECIDED":
        return "UNDECIDED"
    return "REFUSED"


def refused_row(pair, problem, seconds):
    """one pair the machinery raised on, written out as a refused row with
    the literal exception, so a worker is never ended by one pair."""
    return {
        "arch": "riscv64",
        "route": "general_optimization_off",
        "cell": {"mnem": pair["mnem"], "shape": pair["shape"],
                 "key_width": pair["key_width"],
                 "places": [pair["place"]]},
        "place": pair["place"],
        "target": pair["target"],
        "row_id": pair.get("row_id"),
        "builder": pair.get("builder"),
        "number": pair.get("number"),
        "policy": POLICY,
        "kind": "refused",
        "outcome": "REFUSED",
        "verdict": {"outcome": "RAISED",
                    "reason": "%s: %s" % (type(problem).__name__,
                                          ("%s" % problem)[:400])},
        "seconds": round(seconds, 3),
        "peak_kb": peak_kb(),
    }


def one_pair(held, reference, pair, terms, work_root, number):
    RVG = held["RVG"]
    RL = held["RL"]
    H = held["H"]
    INH = held["INH"]
    CONS = held["CONS"]
    cell = {"mnem": pair["mnem"], "shape": pair["shape"],
            "key_width": pair["key_width"],
            "places": [pair["place"]]}
    key = (pair["mnem"], pair["shape"], pair["key_width"])
    term = terms.get((key, pair["place"]))
    started = time.time()
    SHORTCUT["calls"] = []
    COMPILE_SECONDS["last"] = None
    if term is None:
        row = {"arch": "riscv64", "cell": dict(cell),
               "place": pair["place"], "target": pair["target"],
               "kind": "refused",
               "verdict": {"outcome": "NO_TERM",
                           "reason": CAUSE_NO_TERM}}
    else:
        row = RVG.one_run(H, RL, INH, CONS, reference, cell,
                          pair["place"], term, pair["target"],
                          work_root, number)
    seconds = time.time() - started
    attempt = {}
    attempts = row.get("attempts") or []
    if attempts:
        attempt = attempts[0]
    took_the_text = False
    calls = SHORTCUT["calls"]
    if calls:
        took_the_text = bool(calls[0].get("text_taken"))
    out = {
        "arch": "riscv64",
        "route": "general_optimization_off",
        "cell": dict(cell),
        "place": pair["place"],
        "target": pair["target"],
        "row_id": pair.get("row_id"),
        "builder": pair.get("builder"),
        "number": pair.get("number"),
        "policy": POLICY,
        "kind": row.get("kind"),
        "outcome": outcome_of(row, took_the_text),
        "verdict": row.get("verdict"),
        "verdict_at_the_whole_place":
            attempt.get("verdict_at_the_whole_place"),
        "instructions": attempt.get("instructions"),
        "statements": attempt.get("statements"),
        "native_nodes": attempt.get("native_nodes"),
        "constructed_nodes": attempt.get("constructed_nodes"),
        "compiler": attempt.get("compiler"),
        "seconds": round(seconds, 3),
        "compile_seconds": COMPILE_SECONDS["last"],
        "gate_calls": list(calls),
        "peak_kb": peak_kb(),
    }
    return out


def sample_command(root, population_path, count, prefix, src_dir,
                   work_root):
    """the sample the law asks for before a round: a few pairs, run one
    after another in one process, each with its own seconds and the peak
    resident the whole sample reached.

    THE PAIRS ARE SPREAD EVENLY over the population's own order, which is
    the model table's row order, so the sample is not all one builder and
    not all one target."""
    paths = paths_of(root)
    held = bring_in(paths)
    RL = held["RL"]
    RV_REF = held["RV_REF"]
    H = held["H"]
    KEPT_SOURCES["dir"] = src_dir
    if not os.path.isdir(src_dir):
        os.makedirs(src_dir, exist_ok=True)
    if not os.path.isdir(work_root):
        os.makedirs(work_root, exist_ok=True)
    H.SRC_DIR = src_dir
    reference = RV_REF.RiscvReference()
    terms, _operands = RL.riscv_terms(paths["model_table"])
    document = json.load(open(population_path))
    pairs = document["rows"]
    say("   setup took %.1f s, peak %d kB"
        % (time.time() - STARTED, peak_kb()))
    picked = []
    if pairs:
        step = len(pairs) // count
        if step < 1:
            step = 1
        position = 0
        while len(picked) < count and position < len(pairs):
            picked.append(pairs[position])
            position = position + step
            continue
    rows = []
    for pair in picked:
        started_at = time.time()
        try:
            row = one_pair(held, reference, pair, terms, work_root,
                           pair["number"])
        except Exception as problem:                          # noqa: BLE001
            row = refused_row(pair, problem, time.time() - started_at)
        rows.append(row)
        say("   pair %d: `%s` `%s` %s %s on %s -> %s, %.2f s, %s "
            "instructions, peak %d kB"
            % (pair["number"], pair["mnem"], pair["shape"],
               pair["key_width"], pair["place"], pair["target"],
               row["outcome"], row["seconds"], row.get("instructions"),
               peak_kb()))
        check_memory("sample pair %d" % pair["number"])
        continue
    handle = open(prefix + ".jsonl", "w")
    for row in rows:
        handle.write(json.dumps(row, sort_keys=True) + "\n")
        continue
    handle.close()
    seconds = []
    for row in rows:
        seconds.append(row["seconds"])
        continue
    mean_seconds, max_seconds = statistics(seconds)
    document = {
        "meta": {
            "task": "rv4",
            "what": "the sample before the round: %d (cell, target) "
                    "pairs spread over the population" % count,
            "pairs": len(rows),
            "seconds_per_pair_mean": mean_seconds,
            "seconds_per_pair_max": max_seconds,
            "setup_seconds": round(time.time() - STARTED, 1),
            "peak_kb": peak_kb(),
            "memory_bound_kb": ABORT_KB,
            "memory_abort": ABORT_NAME,
        },
        "rows": rows,
    }
    handle = open(prefix + ".json", "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    say("   seconds per pair: mean %s, max %s"
        % (mean_seconds, max_seconds))
    say("peak RSS: %d kB" % peak_kb())
    return 0


def shard_command(root, population_path, index, count, deadline, prefix,
                  src_dir, work_root):
    DEADLINE["at"] = deadline
    paths = paths_of(root)
    held = bring_in(paths)
    RL = held["RL"]
    RV_REF = held["RV_REF"]
    H = held["H"]
    KEPT_SOURCES["dir"] = src_dir
    if not os.path.isdir(src_dir):
        os.makedirs(src_dir, exist_ok=True)
    if not os.path.isdir(work_root):
        os.makedirs(work_root, exist_ok=True)
    H.SRC_DIR = src_dir
    reference = RV_REF.RiscvReference()
    terms, _operands = RL.riscv_terms(paths["model_table"])
    document = json.load(open(population_path))
    mine = []
    for pair in document["rows"]:
        if pair["number"] % count != index:
            continue
        mine.append(pair)
        continue
    say("[worker %d/%d] %d pairs, setup took %.1f s, deadline in %.1f s"
        % (index, count, len(mine), time.time() - STARTED,
           deadline - time.time()))
    path = "%s.worker%d.jsonl" % (prefix, index)
    handle = open(path, "w")
    done = 0
    for pair in mine:
        if time.time() >= deadline:
            row = {
                "arch": "riscv64",
                "route": "general_optimization_off",
                "cell": {"mnem": pair["mnem"], "shape": pair["shape"],
                         "key_width": pair["key_width"],
                         "places": [pair["place"]]},
                "place": pair["place"],
                "target": pair["target"],
                "row_id": pair.get("row_id"),
                "builder": pair.get("builder"),
                "number": pair.get("number"),
                "kind": "not_reached",
                "outcome": "NOT_REACHED_IN_BUDGET",
                "verdict": {"outcome": "NOT_REACHED_IN_BUDGET",
                            "reason": "the driver's own wall clock "
                                      "ended before this pair started"},
                "seconds": 0.0,
            }
            handle.write(json.dumps(row, sort_keys=True) + "\n")
            handle.flush()
            continue
        started_at = time.time()
        try:
            row = one_pair(held, reference, pair, terms, work_root,
                           pair["number"])
        except Exception as problem:                          # noqa: BLE001
            row = refused_row(pair, problem, time.time() - started_at)
        handle.write(json.dumps(row, sort_keys=True) + "\n")
        handle.flush()
        done = done + 1
        check_memory("worker %d run %d" % (index, done))
        continue
    handle.close()
    say("[worker %d/%d] %d pairs run, %.1f s, peak %d kB"
        % (index, count, done, time.time() - STARTED, peak_kb()))
    return 0


# ==================================================================
# section 4: the round -- eight workers and the merge
# ==================================================================

def round_command(root, population_path, workers, budget, prefix, src_dir,
                  work_root):
    deadline = STARTED + budget
    say("[1/3] %d workers, the budget ends %.0f s after this process "
        "began" % (workers, budget))
    running = []
    for index in range(workers):
        command = [sys.executable, os.path.abspath(__file__), "shard",
                   root, population_path, "%d" % index, "%d" % workers,
                   "%.3f" % deadline, prefix, src_dir,
                   os.path.join(work_root, "w%d" % index)]
        log_path = "%s.worker%d.log" % (prefix, index)
        log = open(log_path, "w")
        started = subprocess.Popen(command, stdout=log,
                                   stderr=subprocess.STDOUT)
        running.append({"index": index, "process": started, "log": log,
                        "log_path": log_path})
        continue
    drain = deadline + 30
    stopped = []
    for held in running:
        left = drain - time.time()
        if left < 1:
            left = 1
        try:
            held["process"].wait(timeout=left)
        except subprocess.TimeoutExpired:
            held["process"].terminate()
            stopped.append(held["index"])
            try:
                held["process"].wait(timeout=10)
            except subprocess.TimeoutExpired:
                # the ABORT of last resort: the operating system stops
                # the worker.  `SIGKILL` is the system's own spelling.
                held["process"].send_signal(signal.SIGKILL)
        held["log"].close()
        continue

    say("[2/3] the merge")
    rows = []
    seen = set()
    for held in running:
        path = "%s.worker%d.jsonl" % (prefix, held["index"])
        held["rows"] = 0
        if not os.path.exists(path):
            say("   worker %d wrote no rows, exit code %s"
                % (held["index"], held["process"].returncode))
            continue
        handle = open(path)
        for line in handle:
            text = line.strip()
            if not text:
                continue
            row = json.loads(text)
            rows.append(row)
            seen.add(row["number"])
            held["rows"] = held["rows"] + 1
            continue
        handle.close()
        say("   worker %d wrote %d rows, exit code %s"
            % (held["index"], held["rows"], held["process"].returncode))
        continue
    document = json.load(open(population_path))
    for pair in document["rows"]:
        if pair["number"] in seen:
            continue
        rows.append({
            "arch": "riscv64",
            "route": "general_optimization_off",
            "cell": {"mnem": pair["mnem"], "shape": pair["shape"],
                     "key_width": pair["key_width"],
                     "places": [pair["place"]]},
            "place": pair["place"],
            "target": pair["target"],
            "row_id": pair.get("row_id"),
            "builder": pair.get("builder"),
            "number": pair.get("number"),
            "kind": "not_reached",
            "outcome": "NOT_REACHED_IN_BUDGET",
            "verdict": {"outcome": "NOT_REACHED_IN_BUDGET",
                        "reason": "no worker wrote a row for this pair "
                                  "before the round ended"},
            "seconds": 0.0,
        })
        continue
    rows.sort(key=lambda item: item["number"])
    handle = open(prefix + ".jsonl", "w")
    for row in rows:
        handle.write(json.dumps(row, sort_keys=True) + "\n")
        continue
    handle.close()

    say("[3/3] the census")
    census = {}
    per_target = {}
    for row in rows:
        outcome = row["outcome"]
        census[outcome] = census.get(outcome, 0) + 1
        held_target = per_target.setdefault(row["target"], {})
        held_target[outcome] = held_target.get(outcome, 0) + 1
        continue
    for outcome in sorted(census):
        say("   %-24s %d" % (outcome, census[outcome]))
        continue
    worker_peaks = {}
    for held in running:
        code = held["process"].returncode
        worker_peaks["%d" % held["index"]] = code
        continue
    meta = {
        "task": "rv4",
        "what": "the timed round: the general tier compiled with "
                "optimization off for riscv64, gated, eight workers, a "
                "nine-minute wall clock",
        "targets": list(TARGETS),
        "policy": POLICY,
        "workers": workers,
        "budget_seconds": budget,
        "seconds": round(time.time() - STARTED, 1),
        "census": census,
        "per_target": per_target,
        "worker_exit_codes": worker_peaks,
        "workers_stopped_at_the_drain": stopped,
        "solver_timeout_ms": SOLVER_MS,
        "text_node_ceiling": TEXT_NODE_CEILING,
        "text_printed_ceiling": TEXT_TREE_CEILING,
        "text_depth_ceiling": TEXT_DEPTH_CEILING,
        "gate_instruction_ceiling": 4000,
        "compile_c": " ".join(["clang"] + SHIP_C_OFF + ["-c"]),
        "compile_go": "GOARCH=riscv64 GOOS=linux go build "
                      "-gcflags='all=-N -l'",
        "compile_rust": " ".join(["rustc"] + RUST_OFF),
        "carve": "llvm-objdump -dr -M no-aliases --mattr=+m,+a,+f,+d,+c "
                 "--disassemble-symbols=<symbol>",
        "answer_home": ANSWER_HOME,
        "memory_bound_kb": ABORT_KB,
        "memory_abort": ABORT_NAME,
        "peak_kb": peak_kb(),
    }
    handle = open(prefix + ".json", "w")
    json.dump({"meta": meta, "census": census, "per_target": per_target},
              handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    say("   workers stopped at the drain: %s" % (stopped or "none"))
    say("   seconds: %.1f" % (time.time() - STARTED))
    say("peak RSS: %d kB" % peak_kb())
    return 0


# ==================================================================
# section 5: the tables
# ==================================================================

def load_rows(path):
    out = []
    handle = open(path)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        out.append(json.loads(text))
        continue
    handle.close()
    return out


def statistics(values):
    if not values:
        return None, None
    total = 0.0
    biggest = values[0]
    for value in values:
        total = total + value
        if value > biggest:
            biggest = value
        continue
    return total / len(values), biggest


def tables_command(root, population_path, prefix):
    paths = paths_of(root)
    population = json.load(open(population_path))
    rows = load_rows(prefix + ".jsonl")
    already, where = proved_before(paths)

    say("### table 1 -- the population")
    say("")
    say("| what | cells |")
    say("|---|---|")
    say("| cells `twins.json` holds | %d |"
        % population["meta"]["cells_in_twins"])
    for cause in sorted(population["meta"]["left_out_by_cause"]):
        say("| left out: %s | %d |"
            % (cause, population["meta"]["left_out_by_cause"][cause]))
        continue
    say("| **cells in the population** | **%d** |"
        % population["meta"]["cells_in_the_population"])
    say("")
    say("| the population by the reference's own builder | cells |")
    say("|---|---|")
    for builder in sorted(population["meta"]["population_by_builder"]):
        say("| `%s` | %d |"
            % (builder,
               population["meta"]["population_by_builder"][builder]))
        continue
    say("")
    floats = 0
    integers = 0
    for record in population["rows"]:
        if record.get("float_place") or record.get("float_operands"):
            floats = floats + 1
        else:
            integers = integers + 1
        continue
    say("| pairs by kind | pairs |")
    say("|---|---|")
    say("| floating point (the place is a float register or the operand "
        "form names one) | %d |" % floats)
    say("| integer | %d |" % integers)
    say("| **pairs in the round** | **%d** |" % len(population["rows"]))
    say("")
    say("| target | cells already proved before | pairs in the round |")
    say("|---|---|---|")
    for target in TARGETS:
        say("| `%s` | %d | %d |"
            % (target, len(already.get(target) or set()),
               population["meta"]["pairs_by_target"].get(target, 0)))
        continue

    say("")
    say("### table 2 -- the round, per target")
    say("")
    outcomes = ["PROVED_IDENTICAL", "PROVED", "DISPROVED", "UNDECIDED",
                "REFUSED", "NOT_REACHED_IN_BUDGET"]
    say("| target | " + " | ".join(outcomes) + " | rows |")
    say("|---|" + "---|" * (len(outcomes) + 1))
    for target in TARGETS:
        counts = {}
        held = []
        for row in rows:
            if row["target"] != target:
                continue
            held.append(row)
            counts[row["outcome"]] = counts.get(row["outcome"], 0) + 1
            continue
        line = "| `%s` | " % target
        parts = []
        for outcome in outcomes:
            parts.append("%d" % counts.get(outcome, 0))
            continue
        parts.append("%d" % len(held))
        say(line + " | ".join(parts) + " |")
        continue
    say("")
    say("| target | proved cells before | proved cells after | seconds "
        "per pair, mean | seconds per pair, max | instructions, mean | "
        "instructions, max |")
    say("|---|---|---|---|---|---|---|")
    gained_all = set()
    for target in TARGETS:
        before = set(already.get(target) or set())
        after = set(before)
        seconds = []
        instructions = []
        for row in rows:
            if row["target"] != target:
                continue
            if row["outcome"] in ("PROVED", "PROVED_IDENTICAL"):
                cell = row["cell"]
                after.add((cell["mnem"], cell["shape"],
                           cell["key_width"]))
                gained_all.add((cell["mnem"], cell["shape"],
                                cell["key_width"]))
            if row.get("seconds"):
                seconds.append(row["seconds"])
            if row.get("instructions"):
                instructions.append(row["instructions"])
            continue
        mean_seconds, max_seconds = statistics(seconds)
        mean_instructions, max_instructions = statistics(instructions)
        say("| `%s` | %d | %d | %s | %s | %s | %s |"
            % (target, len(before), len(after),
               "%.2f" % mean_seconds if mean_seconds is not None else "--",
               "%.2f" % max_seconds if max_seconds is not None else "--",
               "%.1f" % mean_instructions
               if mean_instructions is not None else "--",
               "%d" % max_instructions
               if max_instructions is not None else "--"))
        continue
    say("")
    say("| the refusals, by cause | rows |")
    say("|---|---|")
    causes = {}
    for row in rows:
        if row["outcome"] != "REFUSED":
            continue
        verdict = row.get("verdict") or {}
        cause = "%s: %s" % (verdict.get("outcome"),
                            (verdict.get("reason") or "")[:90])
        causes[cause] = causes.get(cause, 0) + 1
        continue
    for cause in sorted(causes, key=lambda item: -causes[item]):
        say("| %s | %d |" % (cause, causes[cause]))
        continue
    say("")
    say("| the gate | rows |")
    say("|---|---|")
    text_taken = 0
    text_asked = 0
    text_too_large = 0
    for row in rows:
        calls = row.get("gate_calls") or []
        if not calls:
            continue
        text_asked = text_asked + 1
        if calls[0].get("text_taken"):
            text_taken = text_taken + 1
        if calls[0].get("cause") == CAUSE_TEXT_TOO_LARGE:
            text_too_large = text_too_large + 1
        continue
    say("| rows whose gate was reached | %d |" % text_asked)
    say("| of those, decided by the identical text, no solver call | %d |"
        % text_taken)
    say("| of those, the term was above the node ceiling, so the solver "
        "was asked | %d |" % text_too_large)

    say("")
    say("### table 3 -- the cells with a proved riscv64 emulation")
    say("")
    document = json.load(open(paths["twins"]))
    whole = len(document.get("rows") or [])
    union_before, parts = union_of_the_stores(paths)
    union_after = set(union_before)
    for key in gained_all:
        union_after.add(key)
        continue
    say("| what | cells | share of the %d |" % whole)
    say("|---|---|---|")
    say("| RISC-V cells `twins.json` holds | %d | 100%% |" % whole)
    say("| reached by an INHERITED certificate, rv3 | %d | %.1f%% |"
        % (len(parts["rv3"]), 100.0 * len(parts["rv3"]) / whole))
    say("| PROVED by task rv2's own loop | %d | %.1f%% |"
        % (len(parts["rv2"]), 100.0 * len(parts["rv2"]) / whole))
    say("| PROVED by task t4's general tier | %d | %.1f%% |"
        % (len(parts["t4"]), 100.0 * len(parts["t4"]) / whole))
    say("| union with a proved riscv64 emulation BEFORE this round "
        "(rv2, rv3, t4) | %d | %.1f%% |"
        % (len(union_before), 100.0 * len(union_before) / whole))
    say("| cells THIS round proved | %d | %.1f%% |"
        % (len(gained_all), 100.0 * len(gained_all) / whole))
    say("| **union AFTER this round** | **%d** | **%.1f%%** |"
        % (len(union_after), 100.0 * len(union_after) / whole))
    say("")
    say("| cells only this round reaches | place | builder |")
    say("|---|---|---|")
    new_cells = []
    for key in sorted(gained_all):
        if key in union_before:
            continue
        new_cells.append(key)
        continue
    for key in new_cells:
        place = "--"
        builder = "--"
        for row in rows:
            cell = row["cell"]
            if (cell["mnem"], cell["shape"], cell["key_width"]) != key:
                continue
            place = row["place"]
            builder = row.get("builder") or "--"
            break
        say("| `%s` `%s` %s | %s | `%s` |"
            % (key[0], key[1], key[2], place, builder))
        continue
    if not new_cells:
        say("| none | -- | -- |")
    say("")
    say("| target | proved cells, rv3's inheritance | proved cells "
        "before this round, all three stores | proved cells after this "
        "round |")
    say("|---|---|---|---|")
    for target in TARGETS:
        rv3_only = set()
        for pair in where:
            if pair[0] != target:
                continue
            if "rv3" not in where[pair]:
                continue
            rv3_only.add(pair[1])
            continue
        before = set(already.get(target) or set())
        after = set(before)
        for row in rows:
            if row["target"] != target:
                continue
            if row["outcome"] not in ("PROVED", "PROVED_IDENTICAL"):
                continue
            cell = row["cell"]
            after.add((cell["mnem"], cell["shape"], cell["key_width"]))
            continue
        say("| `%s` | %d | %d | %d |"
            % (target, len(rv3_only), len(before), len(after)))
        continue

    say("")
    say("### table 4 -- every DISPROVED with its counterexample")
    say("")
    say("| cell | place | target | instructions | the counterexample |")
    say("|---|---|---|---|---|")
    found = 0
    for row in rows:
        if row["outcome"] != "DISPROVED":
            continue
        found = found + 1
        cell = row["cell"]
        verdict = row.get("verdict") or {}
        model = verdict.get("counterexample") or {}
        shown = []
        for name in sorted(model):
            shown.append("`%s` = `%s`" % (name, model[name]))
            continue
        say("| `%s` `%s` %s | %s | `%s` | %s | %s |"
            % (cell["mnem"], cell["shape"], cell["key_width"],
               row["place"], row["target"],
               row.get("instructions"), ", ".join(shown) or "none"))
        continue
    if found == 0:
        say("| none | -- | -- | -- | -- |")
    say("")
    say("peak RSS: %d kB" % peak_kb())
    return 0


def main():
    command = sys.argv[1]
    if command == "population":
        return population_command(sys.argv[2], sys.argv[3])
    if command == "sample":
        return sample_command(sys.argv[2], sys.argv[3], int(sys.argv[4]),
                              sys.argv[5], sys.argv[6], sys.argv[7])
    if command == "shard":
        return shard_command(sys.argv[2], sys.argv[3], int(sys.argv[4]),
                             int(sys.argv[5]), float(sys.argv[6]),
                             sys.argv[7], sys.argv[8], sys.argv[9])
    if command == "round":
        return round_command(sys.argv[2], sys.argv[3], int(sys.argv[4]),
                             float(sys.argv[5]), sys.argv[6],
                             sys.argv[7], sys.argv[8])
    if command == "tables":
        return tables_command(sys.argv[2], sys.argv[3], sys.argv[4])
    raise SystemExit("unknown command %r" % command)


if __name__ == "__main__":
    sys.exit(main())
