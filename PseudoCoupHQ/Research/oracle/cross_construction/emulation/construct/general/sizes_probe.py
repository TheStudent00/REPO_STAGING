#!/usr/bin/env python3
"""sizes_probe.py -- THE TWO SIZES OF A CONSTRUCTION, side by side: the
distinct nodes it has, and the nodes it has WRITTEN OUT.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_t4_brief.md`.

WHY THE TWO ARE KEPT APART, and it is the one number task t2's
`construct/lean/OWED.md` section 3 is about: a construction is a
sequence of steps and a step reads its own previous step more than once,
so the DISTINCT node count is small and the WRITTEN-OUT count -- what a
printed term, a Lean statement without `let`, and the old renderer's
nested expression all carry -- grows like a power of the width.  Every
ceiling in this task is stated on the second number, and this file is
the measurement behind them.

Coding discipline: no compound one-liner statements.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import z3                                                        # noqa: E402
import build as B                                                # noqa: E402
import check_constructions as CC                                 # noqa: E402

CEILING = 200000


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def one(label, node, word):
    built = B.joined(CC.constructed(node, word, {}))
    distinct = B.node_count(built, CEILING)
    written = B.unfolded_size(built, CEILING)
    mark = ""
    if written >= CEILING:
        mark = " (at or above the ceiling)"
    say("| %s | %d | %d | %d%s |" % (label, word, distinct, written,
                                     mark))
    return


def main():
    say("| the construction | word | distinct nodes | nodes WRITTEN OUT "
        "(ceiling %d) |" % CEILING)
    say("|---|---|---|---|")
    for width in (8, 16, 32, 64):
        left = z3.BitVec("a", width)
        right = z3.BitVec("b", width)
        one("add at %d" % width, left + right, 64)
        one("multiply at %d" % width, left * right, 64)
        one("divide unsigned at %d" % width, z3.UDiv(left, right), 64)
        one("shift left at %d" % width, left << right, 64)
        continue
    return 0


if __name__ == "__main__":
    sys.exit(main())
