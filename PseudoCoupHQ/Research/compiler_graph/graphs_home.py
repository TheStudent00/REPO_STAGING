#!/usr/bin/env python3
"""graphs_home.py -- THE ONE PLACE that answers where the compiler graphs
live, now that they live beside this repository rather than inside it.

Node: hq.research.compiler_graph.graph, read by
hq.research.compiler_graph.dashboard (pane 4).

WHY THE GRAPHS MOVED, 2026-09-04
--------------------------------
the owner: "we can have a separate companion folder for the graphs and we will
use local git to track changes every 30 seconds.  we will update the
graphs as we progress along."

`PseudoCoupGraphs` is that folder.  Its own README states
the two reasons: the graphs, the coverage joins and the diaries are
gigabytes, and PseudoCoupHQ pushes to GitHub, which refuses a file past
its own wall -- one such artifact stops the whole push.  And the folder
has NO REMOTE, deliberately: repo-daemon commits a remote-less repository
locally every thirty seconds and never attempts a push, so the graphs get
version control for free and nothing is ever uploaded.  DO NOT ADD AN
ORIGIN.

WHAT LIVES THERE, AND WHAT DOES NOT
-----------------------------------
There:      graph_<lang>.json, coverage_<lang>*.json,
            super_ops_<lang>.json, variant_connections_*.json, diaries/
Not there:  anything a person reads -- the programs, the reports, the
            plans, the dashboard, and the SMALL SUMMARIES the page reads
            (graph_<lang>_files.json, graph_<lang>_defs.json,
            coverage_<lang>_files.json, coverage_<lang>_summary.json).
            Those stay in PseudoCoupHQ, tracked, because they are what
            the chronology recomputes a pane from.

HOW THE FOLDER IS FOUND, in order, first hit wins
-------------------------------------------------
  1. the environment variable PSEUDOCOUP_GRAPHS, if it names a folder
     that exists.  This is how a lane inside Airlock points at the
     container's own mount without a host path in its text;
  2. PseudoCoupGraphs, the Airlock mount, when it exists;
  3. a sibling of this repository's working tree, `../PseudoCoupGraphs`;
  4. `PseudoCoupGraphs`.

If none exists the folder is ANSWERED ANYWAY (the fourth), and
`exists()` says false, so a caller can refuse by name rather than
silently reading a stale copy inside the repository.

THE SPELLING BAN.  Nothing here groups, pairs or compares units; it
answers a directory.  No operator token appears in any key.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))

#: the folder name, in every candidate location.  Named once.
FOLDER = "PseudoCoupGraphs"

ENVIRONMENT_KEY = "PSEUDOCOUP_GRAPHS"

#: where Airlock's mounts.conf exposes it inside the container.
CONTAINER_MOUNT = os.path.join("/projects", FOLDER)


def candidates():
    """every place the folder is looked for, in order, as absolute paths."""
    found = []
    named = os.environ.get(ENVIRONMENT_KEY)
    if named:
        found.append(os.path.abspath(os.path.expanduser(named)))
    found.append(CONTAINER_MOUNT)
    # HERE is <repo>/Research/compiler_graph, so three levels up is the
    # folder the repository itself sits in.
    beside = os.path.abspath(os.path.join(HERE, "..", "..", "..", FOLDER))
    found.append(beside)
    found.append(os.path.expanduser(os.path.join("~", "Programming", FOLDER)))
    ordered = []
    for one in found:
        if one not in ordered:
            ordered.append(one)
    return ordered


def home():
    """the folder the graphs live in.  Always answers a path."""
    tried = candidates()
    for one in tried:
        if os.path.isdir(one):
            return one
    return tried[-1]


def exists():
    return os.path.isdir(home())


def path(*parts):
    """one artifact inside the graph folder."""
    return os.path.join(home(), *parts)


def where_from():
    """which of the four rules answered, for a report line."""
    named = os.environ.get(ENVIRONMENT_KEY)
    place = home()
    if named and os.path.abspath(os.path.expanduser(named)) == place:
        return "the %s environment variable" % ENVIRONMENT_KEY
    if place == CONTAINER_MOUNT:
        return "the Airlock mount %s" % CONTAINER_MOUNT
    return "the folder beside this repository"


if __name__ == "__main__":
    print("graphs home: %s" % home())
    print("found by:    %s" % where_from())
    print("exists:      %s" % exists())
    for one in candidates():
        print("  candidate %-44s %s"
              % (one, "present" if os.path.isdir(one) else "absent"))
