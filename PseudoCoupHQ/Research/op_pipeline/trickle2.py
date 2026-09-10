#!/usr/bin/env python3
"""trickle2.py -- drive the probe regeneration through AIRLOCK'S FRONT DOOR.

WHAT THIS REPLACES, AND WHY

`trickle.py` (2026-09-02) ran its chunks by reaching into a container with
`podman exec`, against a COPY of Airlock at `AirlockTrickle`.
The copy existed because Airlock bound its container names and its caps to
the install, so a second sandbox at half the cores could not be asked for.

Airlock now has INSTANCES. A second sandbox is a name and a settings file
inside Airlock itself:

    PUBLIC/Airlock/instances/trickle.conf
    bash PUBLIC/Airlock/up.sh --instance trickle

So this program submits lanes the documented way -- `airlock submit` --
polls the status file, and reads the product out of the instance's own
`agent/out`. **Nothing here runs podman.** The project side never reaches
past the airlock; that is the contract.

WHAT ONE CHUNK IS, WITH VALUES MOVING

A chunk is a slice of one language's regeneration manifest -- by default
400 candidates, say `rust` probes 800..1199. For that slice:

  1. `trickle.probes_for("rust", 800, 1199)` reads the manifest and returns
     400 probe records.
  2. `lane_gen_verbatim.lane_verbatim` renders them into one bash lane,
     `regen_rust_c0002.sh`, whose product will open with the marker line
     `#verbatim-escape v1`.
  3. `airlock --instance trickle submit regen_rust_c0002.sh --no-batch`
     writes it hidden into the instance's drop folder and renames it. The
     daemon inside `trickle-runner` sees the rename and runs it.
  4. This program polls
     `instances/trickle/agent/status/regen_rust_c0002.sh.status` until it
     reads `state=done`, then reads `exit=` off the same file.
  5. The product at `instances/trickle/agent/out/regen_rust_c0002.txt` is
     copied beside the run, folded by `trickle.fold_chunk`, and the chunk
     is marked `done` in `trickle2_state.json`.

Step 5 is the checkpoint, exactly as in `trickle.py`: a chunk marked done
is never rerun, a chunk that was in flight when a run stopped is redone
from its start, and a chunk is the smallest unit of atomicity.

ONE BEHAVIOURAL DIFFERENCE, STATED RATHER THAN HIDDEN

`trickle.py` ran six chunks AT ONCE inside the container, because
`podman exec` starts a process whenever it is asked. Airlock's daemon runs
lanes SERIALLY, by design -- "concurrent heavy runs are what exhaust
scratch space" (daemon/watcher.py). So this program submits one chunk at a
time and waits.

The instance's `--cpus 6` cap still applies, and a lane may use all six
cores itself; what is lost is the overlap between one chunk's compile and
the next chunk's. Whether an Airlock instance should be able to run N lanes
concurrently is a question for Airlock, not something to work around from
this side: reaching in with `podman exec` to get concurrency back is
exactly the move that produced the copy.

usage:
    python3 trickle2.py --plan
    python3 trickle2.py --run
    python3 trickle2.py --run --langs go rust
    python3 trickle2.py --run --minutes 30
    python3 trickle2.py --status
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time

import trickle
import lane_gen_verbatim

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- where Airlock is, and which instance -------------------------------
AIRLOCK_ROOT = os.environ.get(
    "AIRLOCK_ROOT", os.path.expanduser("PUBLIC/Airlock"))
INSTANCE = os.environ.get("AIRLOCK_INSTANCE", "trickle")

STATE = os.path.join(HERE, "trickle2_state.json")
STORE_DIR = os.path.join(HERE, "trickle_store")
RAW_DIR = os.path.join(HERE, "trickle_raw")
LANE_DIR = os.path.join(HERE, "trickle_lanes")
# Lanes are handed to `airlock submit` from here, not written into the
# instance's drop folder by hand: submit is what validates a lane before it
# becomes a run.
OUTBOX = os.path.join(HERE, "trickle2_outbox")

DEFAULT_CHUNK = 400
# A lane's own driver has a 180s per-compile timeout; this is the ceiling on
# waiting for one whole chunk to come back, generous at ~0.3s a probe.
CHUNK_TIMEOUT_S = 3600
POLL_SECONDS = 2


# ---------------------------------------------------- the instance's paths

def instance_settings():
    """Every AL_* setting for this instance, asked of Airlock itself.

    Airlock's own instance.sh is the single place a name or a path is
    derived. This asks it rather than rebuilding the derivation here, so a
    project can never hold a stale copy of Airlock's naming.
    """
    library = os.path.join(AIRLOCK_ROOT, "instance.sh")
    if not os.path.isfile(library):
        raise SystemExit(
            "REFUSE: no Airlock instance library at %s\n"
            "        set AIRLOCK_ROOT to the Airlock checkout." % library)
    script = (
        'set -e\n'
        'source "$1"\n'
        'AIRLOCK_INSTANCE="$2"\n'
        'airlock_instance_load "$3"\n'
        'env | grep "^AL_"\n'
    )
    done = subprocess.run(
        ["bash", "-c", script, "bash", library, INSTANCE, AIRLOCK_ROOT],
        capture_output=True, text=True, timeout=30)
    if done.returncode != 0:
        raise SystemExit("REFUSE: could not read instance %r: %s"
                         % (INSTANCE, done.stderr.strip()))
    settings = {}
    for line in done.stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            settings[key] = value
    return settings


class Instance(object):
    """The four folders of one Airlock instance's agent lane."""

    def __init__(self):
        self.settings = instance_settings()
        self.name = self.settings["AL_INSTANCE"]
        self.agent = self.settings["AL_AGENT_DIR"]
        self.drop = os.path.join(self.agent, "drop")
        self.status = os.path.join(self.agent, "status")
        self.logs = os.path.join(self.agent, "logs")
        self.out = os.path.join(self.agent, "out")
        self.cli = os.path.join(AIRLOCK_ROOT, "airlock")

    def describe(self):
        return ("instance %s  runner %s  cpus %s  agent %s"
                % (self.name, self.settings.get("AL_RUNNER", "?"),
                   self.settings.get("AL_CPUS", "?"), self.agent))

    def status_path(self, lane_name):
        return os.path.join(self.status, "%s.status" % lane_name)

    def read_status(self, lane_name):
        """The status file as a dict, or {} if it is not there yet."""
        path = self.status_path(lane_name)
        if not os.path.isfile(path):
            return {}
        fields = {}
        try:
            for line in open(path):
                if "=" in line:
                    key, value = line.rstrip("\n").split("=", 1)
                    fields[key] = value
        except OSError:
            return {}
        return fields

    def submit(self, lane_path):
        """Hand one lane to Airlock. Returns (ok, the command's output).

        --no-batch is deliberate: this program keeps its own manifest of
        chunks in trickle2_state.json, and a batch label per chunk would
        mean a new denominator every four hundred probes.
        """
        command = [sys.executable, self.cli, "--instance", self.name,
                   "submit", lane_path, "--no-batch"]
        done = subprocess.run(command, capture_output=True, text=True,
                              timeout=120)
        return done.returncode == 0, (done.stdout + done.stderr)

    def wait(self, lane_name, timeout_s):
        """Poll one lane's status file until it says done. Returns the
        status dict, with state='timeout' if the ceiling was reached."""
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            fields = self.read_status(lane_name)
            if fields.get("state") == "done":
                return fields
            time.sleep(POLL_SECONDS)
        return {"state": "timeout"}

    def lane_log(self, lane_name):
        """The newest log for one lane on the host side, or None."""
        if not os.path.isdir(self.logs):
            return None
        tail = "__%s.log" % lane_name
        found = [os.path.join(self.logs, f)
                 for f in os.listdir(self.logs) if f.endswith(tail)]
        if not found:
            return None
        return max(found, key=os.path.getmtime)


# ---------------------------------------------------------------- state

def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return None


def save_state(state):
    """Written to a temporary name and renamed, so a stop mid-write can
    never leave a truncated state file behind."""
    tmp = STATE + ".tmp"
    handle = open(tmp, "w")
    json.dump(state, handle, indent=1)
    handle.write("\n")
    handle.close()
    os.replace(tmp, STATE)


def plan(instance, chunk_size):
    """Build the chunk plan. Refuses to overwrite an existing one, because
    overwriting it would discard the resume state."""
    if os.path.exists(STATE):
        raise SystemExit(
            "REFUSE: %s already exists. Overwriting it would discard the "
            "resume state; delete it by hand to start over." % STATE)
    state = trickle.plan(chunk_size)
    state["driver"] = "trickle2.py -- airlock submit, no podman"
    state["airlock_root"] = AIRLOCK_ROOT
    state["instance"] = instance.name
    state["agent_tree"] = instance.agent
    state.pop("container", None)
    save_state(state)
    return state


# ------------------------------------------------------------- one chunk

def run_chunk(instance, chunk):
    """Render one chunk's lane, submit it, wait, fold the product."""
    lang = chunk["language"]
    prefix = chunk.get("manifest_prefix", "probe_manifest2")
    name = "%s_%s" % (chunk.get("lane_prefix", "regen"), chunk["chunk_id"])
    lane_name = "%s.sh" % name

    probes, manifest = trickle.probes_for(
        lang, chunk["first_probe"], chunk["last_probe"], prefix)
    text = lane_gen_verbatim.lane_verbatim(lang, name, probes, name)

    for folder in (LANE_DIR, RAW_DIR, STORE_DIR, OUTBOX):
        if not os.path.isdir(folder):
            os.makedirs(folder)

    lane_path = os.path.join(OUTBOX, lane_name)
    handle = open(lane_path, "w")
    handle.write(text)
    handle.close()
    os.chmod(lane_path, 0o755)
    # a copy of the exact script that ran, kept beside the products
    open(os.path.join(LANE_DIR, lane_name), "w").write(text)

    started = time.time()
    ok, submit_output = instance.submit(lane_path)
    if not ok:
        return {"ok": False, "rc": None,
                "seconds": round(time.time() - started, 1),
                "reason": "airlock submit refused this lane",
                "submit_output": submit_output}

    fields = instance.wait(lane_name, CHUNK_TIMEOUT_S)
    elapsed = time.time() - started

    log_path = instance.lane_log(lane_name)
    kept_log = os.path.join(RAW_DIR, "%s.console.log" % name)
    if log_path and os.path.isfile(log_path):
        shutil.copyfile(log_path, kept_log)
    else:
        open(kept_log, "w").write("no lane log found for %s\n" % lane_name)

    if fields.get("state") != "done":
        return {"ok": False, "rc": None, "seconds": round(elapsed, 1),
                "reason": "the lane did not finish within %ds"
                          % CHUNK_TIMEOUT_S,
                "console_log": kept_log}

    rc = fields.get("exit")
    product = os.path.join(instance.out, "%s.txt" % name)
    if rc != "0" or not os.path.exists(product):
        return {"ok": False, "rc": rc, "seconds": round(elapsed, 1),
                "reason": "lane exited %s or wrote no product" % rc,
                "console_log": kept_log}

    kept = os.path.join(RAW_DIR, "%s.txt" % name)
    open(kept, "w").write(open(product).read())

    record = trickle.fold_chunk(lang, name, kept, manifest, chunk)
    record["ok"] = record.get("ok", True)
    record["rc"] = rc
    record["seconds"] = round(elapsed, 1)
    record["console_log"] = kept_log
    record["lane_product"] = kept
    record["lane_status"] = instance.status_path(lane_name)
    return record


# ------------------------------------------------------------------- run

def run(instance, langs, limit, minutes):
    state = load_state()
    if state is None:
        raise SystemExit("REFUSE: no plan yet. Run --plan first.")

    deadline = None
    if minutes:
        deadline = time.time() + minutes * 60

    pending = [c for c in state["chunks"] if c.get("state") != "done"]
    if langs:
        pending = [c for c in pending if c["language"] in langs]
    if limit:
        pending = pending[:limit]

    print(instance.describe())
    print("%d chunk(s) to run, one at a time (Airlock runs lanes serially)"
          % len(pending))

    for chunk in pending:
        if deadline and time.time() > deadline:
            print("  time budget reached; everything run so far is banked")
            break
        name = "%s_%s" % (chunk.get("lane_prefix", "regen"),
                          chunk["chunk_id"])
        record = run_chunk(instance, chunk)
        chunk["state"] = "done" if record.get("ok") else "failed"
        chunk["record"] = record
        save_state(state)
        if record.get("ok"):
            tally = record.get("tally", {})
            print("  %-18s %5s submitted %5s accepted %5s refused  %6.1fs"
                  % (name, tally.get("submitted", "?"),
                     tally.get("accepted", "?"), tally.get("refused", "?"),
                     record["seconds"]))
        else:
            print("  %-18s FAILED: %s" % (name, record.get("reason")))
    return 0


def show_status(instance):
    state = load_state()
    if state is None:
        print("no plan yet (%s absent)" % STATE)
        return 0
    print(instance.describe())
    print("chunk size %s ; %s chunks ; %s probes"
          % (state.get("chunk_size"), state["totals"]["chunks"],
             state["totals"]["probes"]))
    by_lang = {}
    for chunk in state["chunks"]:
        row = by_lang.setdefault(chunk["language"], {"done": 0, "left": 0})
        if chunk.get("state") == "done":
            row["done"] += 1
        else:
            row["left"] += 1
    for lang in sorted(by_lang):
        row = by_lang[lang]
        print("  %-6s done %-5d  not done %d"
              % (lang, row["done"], row["left"]))
    return 0


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--chunk", type=int, default=DEFAULT_CHUNK)
    parser.add_argument("--langs", nargs="*", default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--minutes", type=int, default=None)
    args = parser.parse_args(argv)

    instance = Instance()

    if args.plan:
        state = plan(instance, args.chunk)
        print("planned %d chunks over %d probes"
              % (state["totals"]["chunks"], state["totals"]["probes"]))
        return 0
    if args.run:
        return run(instance, args.langs, args.limit, args.minutes)
    if args.status:
        return show_status(instance)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
