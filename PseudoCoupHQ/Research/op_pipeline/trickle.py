#!/usr/bin/env python3
"""trickle.py -- run the probe regeneration through the CPU-capped copy of
the Airlock runner, in checkpointed chunks, on the verbatim-capture path.

WHAT ONE CHUNK IS, WITH VALUES MOVING

A chunk is a slice of one language's regeneration manifest -- by default
400 candidates, say `rust` probes 800..1199.  For that slice this program:

  1. renders a lane script with `lane_gen_verbatim.lane_verbatim`, so the
     driver ESCAPES the compiler's words instead of substituting them;
     the lane's output file opens with the line `#verbatim-escape v1`.
  2. writes it into the trickle tree's drop folder and runs it inside
     `trickle-runner` with `podman exec`.
  3. reads the lane's product back, decodes the escaped fields, folds it
     into a chunk store of its own, and writes the chunk's tally.
  4. marks the chunk `done` in `trickle_state.json`.

Step 4 is the checkpoint.  A run that is stopped anywhere -- between
chunks, in the middle of a chunk, by the machine going away -- resumes by
re-reading that file and skipping every chunk already marked done.  A
chunk that was running when the run stopped is simply not done, so it is
redone from the start; a chunk is the unit of atomicity, nothing smaller.

WHY THE STORES ARE PER-CHUNK AND NEW

Every chunk writes its OWN store file.  Nothing is appended to, nothing
existing is rewritten, and the 4,440-candidate corpus's stores are not
touched at all.  Two chunks can therefore be in flight at once with no
shared writer, and an interrupted chunk can leave at most its own file
half-written -- which the state file will not have marked done, so it is
overwritten on the retry.

CONCURRENCY, AND THE CAP

`trickle-runner` is capped at half the machine's cores.  This program runs
several chunks at once inside it, defaulting to that same number, so the
cap -- not this program -- is what decides how much of the machine the
work can take.  Raising the worker count above the cap cannot exceed the
cap; it only queues.

THE SPELLING BAN.  Chunks are slices of a manifest in probe-number order.
No key, grouping, pairing, chunk boundary or candidate selection anywhere
here is an operator token.  The token rides only in the `operator`
display field of each probe record, in a document declaring the generator
provenance role.  Every store and state file this program writes is walked
by `check_no_spelling_keys.py`, and the program deletes its own output on
a failure.

usage:
    /tmp/reconnect_venv/bin/python3 trickle.py --plan
    /tmp/reconnect_venv/bin/python3 trickle.py --run
    /tmp/reconnect_venv/bin/python3 trickle.py --run --langs go rust
    /tmp/reconnect_venv/bin/python3 trickle.py --run --minutes 30
    /tmp/reconnect_venv/bin/python3 trickle.py --status
"""

import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
import time

import threading

import fold
import lane_gen_verbatim
import verbatim_diag as V

# `lane_gen_verbatim.lane_verbatim` swaps the module-global
# `lane_gen.DRIVER` for the duration of one call and restores it after.
# That is safe on one thread and NOT safe on several: two workers
# rendering at once leave the second one editing an already-edited driver,
# and its own assertion fires --
#   "edit did not apply as expected: clean(): drop the two substitutions
#    -- found 0, wanted 1"
# which is exactly what happened on the first run (10 chunks failed that
# way, and were retried on resume). Rendering is milliseconds, so
# serialising it costs nothing; the compiling, which is the work, stays
# parallel.
RENDER_LOCK = threading.Lock()

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]

TRICKLE_ROOT = os.environ.get(
    "TRICKLE_ROOT", os.path.expanduser("<WORKSPACE_DIR>/AirlockTrickle"))
AGENT = os.path.join(TRICKLE_ROOT, "agent")
CONTAINER = "trickle-runner"

STATE = os.path.join(HERE, "trickle_state.json")
STORE_DIR = os.path.join(HERE, "trickle_store")
RAW_DIR = os.path.join(HERE, "trickle_raw")
LANE_DIR = os.path.join(HERE, "trickle_lanes")

DEFAULT_CHUNK = 400
DEFAULT_WORKERS = max(1, (os.cpu_count() or 2) // 2)
# The lane's own driver has a 180s per-compile timeout; this is the
# ceiling on a whole chunk, generous by a wide margin at ~0.3s a probe.
CHUNK_TIMEOUT_S = 3600


# ---------------------------------------------------------------- state

def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return None


def save_state(state):
    """Written to a temporary name and renamed, so a stop mid-write can
    never leave a truncated state file behind."""
    tmp = STATE + ".tmp"
    fh = open(tmp, "w")
    json.dump(state, fh, indent=1)
    fh.write("\n")
    fh.close()
    os.replace(tmp, STATE)


def plan(chunk_size):
    chunks = []
    for lang in LANGS:
        path = os.path.join(HERE, "probe_manifest2_%s.json" % lang)
        doc = json.load(open(path))
        keys = sorted(int(k) for k in doc["probes"])
        k = 0
        idx = 0
        while k < len(keys):
            part = keys[k:k + chunk_size]
            chunks.append({
                "chunk_id": "%s_c%04d" % (lang, idx),
                "language": lang,
                "first_probe": part[0],
                "last_probe": part[-1],
                "probes": len(part),
                "state": "pending",
            })
            k = k + chunk_size
            idx = idx + 1
    state = {}
    state["generated_by"] = "trickle.py --plan"
    state["what_this_is"] = (
        "the resume state of the probe regeneration. A chunk marked done "
        "is never rerun; a chunk in any other state is redone from its "
        "start. This file IS the resume mechanism -- delete it and the "
        "whole trickle restarts.")
    state["chunk_size"] = chunk_size
    state["container"] = CONTAINER
    state["agent_tree"] = AGENT
    state["store_dir"] = STORE_DIR
    state["capture_path"] = (
        "lane_gen_verbatim.lane_verbatim -- the driver escapes the "
        "compiler's words; every lane product carries the "
        "'#verbatim-escape v1' marker and is refused if it does not")
    state["chunks"] = chunks
    state["totals"] = {
        "chunks": len(chunks),
        "probes": sum(c["probes"] for c in chunks),
    }
    return state


# ------------------------------------------------------------ one chunk

def probes_for(lang, first, last, prefix="probe_manifest2"):
    path = os.path.join(HERE, "%s_%s.json" % (prefix, lang))
    doc = json.load(open(path))
    out = []
    for n in range(first, last + 1):
        rec = doc["probes"].get(str(n))
        if rec is None:
            continue
        out.append({f: rec[f] for f in
                    ("n", "symbol", "symbol_exact", "source")})
    return out, doc


def run_chunk(chunk):
    """Compile one chunk inside the capped container.  Returns a record."""
    lang = chunk["language"]
    prefix = chunk.get("manifest_prefix", "probe_manifest2")
    name = "%s_%s" % (chunk.get("lane_prefix", "regen"), chunk["chunk_id"])
    probes, manifest = probes_for(lang, chunk["first_probe"],
                                  chunk["last_probe"], prefix)
    with RENDER_LOCK:
        text = lane_gen_verbatim.lane_verbatim(lang, name, probes, name)

    for d in (LANE_DIR, RAW_DIR, STORE_DIR,
              os.path.join(AGENT, "drop"), os.path.join(AGENT, "out")):
        if not os.path.isdir(d):
            os.makedirs(d)

    lane_path = os.path.join(AGENT, "drop", "%s.sh" % name)
    fh = open(lane_path, "w")
    fh.write(text)
    fh.close()
    os.chmod(lane_path, 0o755)
    # a copy of the exact script that ran, kept beside the products
    open(os.path.join(LANE_DIR, "%s.sh" % name), "w").write(text)

    started = time.time()
    cmd = ["podman", "exec", CONTAINER, "sh", "/drop/%s.sh" % name]
    try:
        done = subprocess.run(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              timeout=CHUNK_TIMEOUT_S)
        rc = done.returncode
        console = done.stdout.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        rc = 124
        console = "ABORT: the chunk exceeded %ds" % CHUNK_TIMEOUT_S
    elapsed = time.time() - started

    log_path = os.path.join(RAW_DIR, "%s.console.log" % name)
    open(log_path, "w").write(console)

    product = os.path.join(AGENT, "out", "%s.txt" % name)
    if rc != 0 or not os.path.exists(product):
        return {"ok": False, "rc": rc, "seconds": round(elapsed, 1),
                "reason": "lane exited %d or wrote no product" % rc,
                "console_log": log_path}

    kept = os.path.join(RAW_DIR, "%s.txt" % name)
    open(kept, "w").write(open(product).read())

    record = fold_chunk(lang, name, kept, manifest, chunk)
    record["ok"] = True
    record["rc"] = rc
    record["seconds"] = round(elapsed, 1)
    record["console_log"] = log_path
    record["lane_product"] = kept
    return record


def fold_chunk(lang, name, product_path, manifest, chunk):
    """Fold one chunk's lane product into its own store, decoding the
    verbatim escapes.  Refuses an unmarked product rather than decoding
    it -- decoding a legacy line would rewrite a backslash the compiler
    really emitted, which is the defect this path exists to end."""
    first_line = open(product_path).readline().rstrip("\n")
    if first_line != V.MARKER:
        return {"ok": False,
                "reason": "product carries no %r marker: %s"
                          % (V.MARKER, product_path)}

    rows = fold.read_lanes([product_path])
    folded = {}
    tally = {"submitted": 0, "accepted": 0, "refused": 0,
             "extracted_ship": 0, "extracted_anchor": 0,
             "extracted_dwarf": 0, "no_line": 0}
    for n in range(chunk["first_probe"], chunk["last_probe"] + 1):
        rec = manifest["probes"].get(str(n))
        if rec is None:
            continue
        meta = dict(rec)
        meta.pop("source", None)
        entry = {"meta": meta}
        tally["submitted"] = tally["submitted"] + 1
        mine = rows.get(n)
        if not mine:
            entry["missing"] = "no line for op_%d in %s" % (n, product_path)
            tally["no_line"] = tally["no_line"] + 1
            folded[str(n)] = entry
            continue
        accepted = True
        for parts in mine:
            tag = parts[1]
            if tag == "REFUSED":
                entry["refused"] = V.decode(parts[2]) if len(parts) > 2 else ""
                accepted = False
                continue
            if tag not in ("ANCHOR", "SHIP"):
                continue
            what = parts[2]
            slot = "anchor" if tag == "ANCHOR" else "ship"
            side = entry.setdefault(slot, {})
            if what == "OK":
                side["bytes"] = [V.decode(x) for x in parts[3].split()]
                side["mnem"] = ([V.decode(x) for x in parts[4].split(";")]
                                if parts[4] else [])
                if slot == "anchor":
                    tally["extracted_anchor"] = tally["extracted_anchor"] + 1
                else:
                    tally["extracted_ship"] = tally["extracted_ship"] + 1
            elif what == "DWARF":
                rows_out = []
                for row in fold.dwarf_rows(parts[3]):
                    rows_out.append({
                        "name": V.decode(row["name"]),
                        "location": (V.decode(row["location"])
                                     if row["location"] is not None else None),
                    })
                side["dwarf"] = rows_out
                tally["extracted_dwarf"] = tally["extracted_dwarf"] + 1
            elif what == "BUILDFAIL":
                side["buildfail"] = V.decode(parts[3])
            elif what == "NODWARF":
                side["nodwarf"] = V.decode(parts[3])
            elif what == "NOSYM":
                side["nosym"] = V.decode(parts[3])
        if accepted:
            tally["accepted"] = tally["accepted"] + 1
        else:
            tally["refused"] = tally["refused"] + 1
        folded[str(n)] = entry

    doc = {}
    doc["generated_by"] = "trickle.py"
    doc["language"] = lang
    doc["chunk_id"] = chunk["chunk_id"]
    doc["capture"] = ("verbatim -- the lane product carried %r and every "
                      "escaped field was decoded back to the compiler's "
                      "own characters" % V.MARKER)
    doc["manifest"] = "%s_%s.json" % (chunk.get(
        "manifest_prefix", "probe_manifest2"), lang)
    doc["id_space"] = ("probe_manifest2_<lang>.json's numbering, which is "
                       "NOT the 4,440-candidate corpus's op_<n> space")
    doc["tally"] = tally
    doc["probes"] = folded
    store = os.path.join(
        STORE_DIR, "%s_%s.json" % (chunk.get("store_prefix", "op_units2"),
                                  chunk["chunk_id"]))
    tmp = store + ".tmp"
    fh = open(tmp, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()
    os.replace(tmp, store)
    return {"store": store, "tally": tally}


# ------------------------------------------------------------- driving

def guard(paths):
    cmd = [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py")]
    cmd.extend(paths)
    done = subprocess.run(cmd, capture_output=True, text=True)
    return done.returncode, done.stdout.strip(), done.stderr.strip()


def refuse_own_output_on_spelling_failure(paths):
    rc, out, err = guard(paths)
    print(out)
    if rc != 0:
        print(err)
        for path in paths:
            if os.path.exists(path):
                os.remove(path)
        raise SystemExit("REFUSED OWN OUTPUT: spelling guard failed")


def container_is_up():
    done = subprocess.run(
        ["podman", "ps", "--filter", "name=%s" % CONTAINER,
         "--format", "{{.Names}}"], capture_output=True, text=True)
    return CONTAINER in done.stdout


def run(state, langs, workers, minutes, limit):
    if not container_is_up():
        raise SystemExit(
            "trickle: %s is not running. Start it:  bash trickle_up.sh"
            % CONTAINER)
    deadline = None
    if minutes:
        deadline = time.time() + minutes * 60.0
    pending = []
    for chunk in state["chunks"]:
        if chunk["state"] == "done":
            continue
        if langs and chunk["language"] not in langs:
            continue
        pending.append(chunk)
    if limit:
        pending = pending[:limit]
    print("%d chunks to run (%d probes) with %d workers"
          % (len(pending), sum(c["probes"] for c in pending), workers))

    index = {}
    for chunk in state["chunks"]:
        index[chunk["chunk_id"]] = chunk

    pool = concurrent.futures.ThreadPoolExecutor(max_workers=workers)
    inflight = {}
    queue = list(pending)
    done_count = 0

    def submit_more():
        while queue and len(inflight) < workers:
            if deadline and time.time() > deadline:
                return
            chunk = queue.pop(0)
            inflight[pool.submit(run_chunk, chunk)] = chunk

    submit_more()
    while inflight:
        finished, _ = concurrent.futures.wait(
            list(inflight.keys()),
            return_when=concurrent.futures.FIRST_COMPLETED)
        for future in finished:
            chunk = inflight.pop(future)
            live = index[chunk["chunk_id"]]
            try:
                record = future.result()
            except Exception as exc:
                record = {"ok": False, "reason": "%s: %s"
                                                 % (type(exc).__name__, exc)}
            if record.get("ok"):
                rc_guard, out, _err = guard([record["store"]])
                if rc_guard != 0:
                    os.remove(record["store"])
                    live["state"] = "refused_by_the_spelling_guard"
                    live["detail"] = out
                else:
                    live["state"] = "done"
                    live["tally"] = record["tally"]
                    live["seconds"] = record["seconds"]
                    live["store"] = record["store"]
                    live["lane_product"] = record["lane_product"]
                    done_count = done_count + 1
                    t = record["tally"]
                    print("  %-14s %5d submitted  %5d accepted  %5d refused"
                          "  %5d extracted   %6.1fs"
                          % (chunk["chunk_id"], t["submitted"], t["accepted"],
                             t["refused"], t["extracted_ship"],
                             record["seconds"]))
            else:
                live["state"] = "failed"
                live["detail"] = record.get("reason")
                live["seconds"] = record.get("seconds")
                print("  %-14s FAILED: %s"
                      % (chunk["chunk_id"], record.get("reason")))
            save_state(state)
        if deadline and time.time() > deadline:
            queue = []
            if not inflight:
                print("  time budget reached; stopping cleanly with "
                      "%d chunks banked" % done_count)
        submit_more()
    save_state(state)
    return done_count


def status(state):
    by = {}
    for chunk in state["chunks"]:
        key = (chunk["language"], chunk["state"])
        by[key] = by.get(key, 0) + 1
    print("chunk size %d ; %d chunks ; %d probes"
          % (state["chunk_size"], state["totals"]["chunks"],
             state["totals"]["probes"]))
    tot = {"submitted": 0, "accepted": 0, "refused": 0,
           "extracted_ship": 0, "extracted_anchor": 0, "extracted_dwarf": 0}
    for lang in LANGS:
        parts = []
        for key in sorted(by):
            if key[0] != lang:
                continue
            parts.append("%s %d" % (key[1], by[key]))
        probes_done = 0
        for chunk in state["chunks"]:
            if chunk["language"] != lang or chunk["state"] != "done":
                continue
            probes_done = probes_done + chunk["probes"]
            for field in tot:
                tot[field] = tot[field] + chunk["tally"][field]
        print("  %-6s %-40s  %6d probes banked" % (lang, ", ".join(parts),
                                                   probes_done))
    print("  totals: submitted %d  accepted %d  refused %d  "
          "extracted ship %d anchor %d dwarf %d"
          % (tot["submitted"], tot["accepted"], tot["refused"],
             tot["extracted_ship"], tot["extracted_anchor"],
             tot["extracted_dwarf"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--chunk", type=int, default=DEFAULT_CHUNK)
    ap.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    ap.add_argument("--langs", nargs="*", default=None)
    ap.add_argument("--minutes", type=float, default=0)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    state = load_state()
    if args.plan or state is None:
        if state is not None:
            print("a plan already exists; --plan refuses to overwrite it "
                  "because that would discard the resume state. Delete "
                  "%s deliberately if a fresh plan is wanted." % STATE)
        else:
            state = plan(args.chunk)
            save_state(state)
            print("planned %d chunks over %d probes (chunk size %d)"
                  % (state["totals"]["chunks"], state["totals"]["probes"],
                     state["chunk_size"]))
            refuse_own_output_on_spelling_failure([STATE])
    if args.run:
        run(state, args.langs, args.workers, args.minutes, args.limit)
        refuse_own_output_on_spelling_failure([STATE])
    if args.status or args.run:
        status(state)


if __name__ == "__main__":
    main()
