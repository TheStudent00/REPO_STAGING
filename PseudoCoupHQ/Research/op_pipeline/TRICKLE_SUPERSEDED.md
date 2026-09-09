# The three `trickle_*.sh` scripts are SUPERSEDED — 2026-09-02

`trickle_up.sh`, `trickle_down.sh` and `trickle_doctor.sh` are superseded by
Airlock's own instances. They are left on disk untouched, as the record of
what was done; **do not run them.**

## What they did, and why that was wrong

They started, stopped and inspected a container called `trickle-runner`,
built from a COPY of Airlock at `~/Programming/AirlockTrickle`. The copy was
made because Airlock had no way to ask for a second sandbox at half the
cores beside the default one: its container, network and volume names, and
its caps, were bound to the install.

the owner's rule, 2026-09-02: *"its not supposed to be a repo that is modified for
use for a specific project ... if i wanted to use Numpy, i wouldnt clone
Numpy in order to modify Numpy source. Airlock source isnt meant to be
modified. its an application."*

A copy was made where a feature was required.

## What replaces each one

| superseded | replaced by |
|---|---|
| `bash trickle_up.sh` | `bash ~/Programming/Airlock/up.sh --instance trickle --cpus 6` |
| `bash trickle_down.sh` | `bash ~/Programming/Airlock/down.sh --instance trickle` |
| `bash trickle_down.sh --pause` | `podman stop trickle-runner`, or just `down.sh` — an instance is cheap to recreate |
| `bash trickle_doctor.sh` | `~/Programming/Airlock/airlock doctor` — it lists every instance and whether each is running |
| `trickle.py --run` (`podman exec`) | `python3 trickle2.py --run` — submits through `airlock submit`, polls the status file, reads `agent/out` |

The instance's settings — 6 cores, 8g, no proxy, the default instance's
`sandbox-persist` volume mounted read-only — live in
`~/Programming/Airlock/instances/trickle.conf`. Nothing about the instance
lives in this repository.

## The standing rule this enforces

**Nothing on the project side runs `podman`.** `trickle2.py` does not, and
neither should anything that follows it. A project hands Airlock a bash
script and reads four folders back; that is the whole interface. If
something cannot be done through it, the fix is a feature request against
Airlock, not a reach past it.

`trickle.py` itself is kept: `trickle2.py` imports its planner, its manifest
reader and its folder, and replaces only the step that ran the lane.
