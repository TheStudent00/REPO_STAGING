#!/usr/bin/env python3
"""lane_gen2.py -- the compile-or-refuse / anchor+ship / extract lanes
for the compound-assignment probes.

This is lane_gen.py with ONE thing changed: which manifest it reads
and what the lane output is called.  lane_gen.py's own `load` already
keys on a name, so `load("asg_c")` reads
`probe_manifest_asg_c.json`; and its `lane` takes the real language
separately, which is what the toolchain check needs.  So this file
composes those two functions and writes nothing of its own.

The lanes are named `op_asg_<lang>`, so their output lands at
`/out/op_asg_<lang>.txt` and `fold2.py` can fold it under the
pseudo-language name `asg_<lang>` without touching the first run's
files.

usage:
  lane_gen2.py c cpp go rust swift [--shard N] [--smoke N] [--drop]
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import lane_gen as LG                                         # noqa: E402

LANGS = LG.LANGS


def main():
    langs = []
    shard = 0
    smoke = 0
    drop = False
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--shard":
            i = i + 1
            shard = int(args[i])
        elif a == "--smoke":
            i = i + 1
            smoke = int(args[i])
        elif a == "--drop":
            drop = True
        else:
            langs.append(a)
        i = i + 1

    if not langs:
        print(__doc__)
        return 2

    lanedir = os.path.join(HERE, "lanes")
    if not os.path.isdir(lanedir):
        os.makedirs(lanedir)

    for lang in langs:
        if lang not in LANGS:
            print("skip %s -- no lane template" % lang)
            continue
        probes = LG.load("asg_%s" % lang)
        if smoke:
            probes = probes[:smoke]
        base = "op_asg_%s" % lang
        groups = []
        if shard:
            k = 0
            while k < len(probes):
                groups.append(probes[k:k + shard])
                k = k + shard
        else:
            groups.append(probes)
        for idx, grp in enumerate(groups):
            name = base
            if len(groups) > 1:
                name = "%s_s%d" % (base, idx)
            text = LG.lane(lang, name, grp, name)
            # the established habit: archive beside the co-lanes
            # BEFORE dropping.
            lpath = os.path.join(lanedir, "%s.sh" % name)
            fh = open(lpath, "w")
            fh.write(text)
            fh.close()
            os.chmod(lpath, 0o755)
            print("%-6s %-18s %4d probes  %8d bytes  %s"
                  % (lang, name, len(grp), len(text), lpath))
            if drop:
                dpath = os.path.join(LG.DROP, "%s.sh" % name)
                fh = open(dpath, "w")
                fh.write(text)
                fh.close()
                print("       dropped %s" % dpath)
    return 0


if __name__ == "__main__":
    sys.exit(main())
