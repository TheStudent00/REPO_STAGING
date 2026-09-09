# hub

The hub, as this version has it. **In version 5 it is inert.**

Versions of PseudoCoup are turns of the bootstrap cycle, and the hub
is what tells them apart: this version runs before a hub exists, so
what is here is a surface that refuses. The next version's `hub/`
holds the hub PseudoIR built.

The folder exists in every version so the layout does not change
between them and a version-to-version diff stays readable.

## What is here

- `__init__.py` — a surface with no declared names. Importing it is
  fine; touching anything in it raises `InertHubError` naming what
  was wanted and where the real hub is defined.
- `test_hub_is_inert.py` — the acceptance test. 7 checks, green.
  Run: `python3 -m pytest ~/Programming/PseudoCoup_v5/hub -q`

## Two decisions worth knowing before editing this

**It refuses rather than doing nothing.** A surface whose names exist
and quietly no-op is the worse failure: transpiled code resolves
against it, runs, and produces wrong answers with nothing reporting a
problem. Refusing is inert in the sense that matters — it computes
nothing — while being impossible to mistake for a working hub.

**It declares no names of its own.** The real surface is described in
PseudoIR's plan and only there, and it is unsettled. Listing guessed
names here would invent that surface in the wrong repo, so the module
answers to any name through `__getattr__` instead.

## Do not describe the hub here

`~/Programming/PseudoIR/Planning/node_0_2_hub/` describes what the
hub IS. This folder holds the artifact. A second description growing
here is the duplication the project split exists to prevent.

## When PseudoIR delivers

This module is replaced, not extended. It is a placeholder, not a
design.
