#!/usr/bin/env bash
# cg_diary_l1 — build THE DIARY for the compiler graph node.
#
# The tally (coverage) lost order. This lane edits a copy of the Go
# compiler's own source so that 56 chosen spots write their map node id
# into a file AS THEY ARE ENTERED, rebuilds cmd/compile, compiles the
# probe by the replay recipe of coverage_meta.md, and collects the diary.
set -u
OUT=/out/cg_diary_l1.txt
exec > >(tee "$OUT") 2>&1
say(){ echo "=== $* ==="; }

SRC=/persist/gosrc
export GOROOT="$SRC"; export PATH="$SRC/bin:$PATH"
export GOTOOLCHAIN=local GOPROXY=off GOFLAGS=-mod=mod GOCACHE=/persist/gocache
GO="$SRC/bin/go"

say recon
date -u +%Y-%m-%dT%H:%M:%SZ
python3 -c 'import sys; print("python", sys.version.split()[0])' || { echo FATAL_NO_PYTHON; exit 80; }
"$GO" version || { echo FATAL_NO_TOOLCHAIN; exit 81; }
ls -l "$SRC/bin/go"

say "restore the five touched files from the read-only vendored tree"
for f in cmd/compile/internal/abi/abiutils.go \
         cmd/compile/internal/amd64/galign.go \
         cmd/compile/internal/amd64/ggen.go \
         cmd/compile/internal/amd64/ssa.go \
         cmd/compile/internal/ssagen/ssa.go ; do
  cp -f "/sources/golang_src/src/$f" "$SRC/src/$f" || exit 82
  echo "restored $f"
done
rm -rf "$SRC/src/cmd/compile/internal/diary"

mkdir -p /work/diary

say 'write the instrumenter and its target list into /work/diary'
cat > /work/diary/inject_diary.py <<'INJECT_DIARY_PY_EOF'
#!/usr/bin/env python3
"""inject_diary.py — the diary instrumenter for the compiler graph node.

The map (graph_go.json) already names every function of cmd/compile by
a node id of the form  <file>:<start_byte>-<end_byte>:<kind>.  This tool
edits a COPY of the compiler's source so that each chosen spot writes
its own map node id into a file AS IT IS ENTERED.  Order is therefore
preserved: that is the whole point of a diary as against a tally.

Two modes.

  select   read the map, choose the target spots, write diary_targets.json
  inject   read diary_targets.json, edit a copy of the compiler source

Never point `inject` at a read-only original tree.  It rewrites files in
place.  In this node the copy is the Airlock path /persist/gosrc/src.

Coding discipline of this node (CORE 0_3_5): no complex statements.  If a
statement can be split over several lines, it is split.
"""

import argparse
import collections
import json
import os
import sys


# ---------------------------------------------------------------- select

SEED_FILE = "src/cmd/compile/internal/abi/abiutils.go"

NEIGHBOUR_DIRS = (
    "/ssagen/",
    "/amd64/",
)

# How many call hops out of the seed file we follow before we stop.
HOP_LIMIT = 3

# The map has NO path from abi into internal/amd64 — that is the named
# frontier recorded in acceptance_query.txt leg 2.  So the amd64 side
# cannot be reached by the map, and these entry points are named by hand.
# They are marked hand_picked in the target records so the report can say
# which spots the map chose and which a person chose.
AMD64_BY_NAME = (
    "ssaGenValue",
    "ssaGenBlock",
    "ssaMarkMoves",
    "zeroRange",
    "ginsnop",
    "Init",
)

# The loop region inside ABIAnalyzeFuncType.  It is not a function, so it
# is named by the map node of the loop's own variable, which is where the
# acceptance path starts.
LOOP_TARGETS = (
    {
        "file": SEED_FILE,
        "start_line": 362,
        "kind": "local_var",
        "name": "param",
    },
)


def load_map(path):
    handle = open(path)
    graph = json.load(handle)
    handle.close()
    return graph


def function_nodes(graph):
    result = {}
    for node in graph["nodes"]:
        if node["kind"] == "func":
            result[node["id"]] = node
        if node["kind"] == "method":
            result[node["id"]] = node
    return result


def call_edges(graph, funcs):
    """Lift the map's call edges up to function-to-function edges.

    In the map a call node is CONTAINED by a function and CALLS another
    function; the two edges together give one function-to-function edge.
    """
    owner = {}
    for edge in graph["edges"]:
        if edge["type"] != "contains":
            continue
        if edge["src"] not in funcs:
            continue
        owner[edge["dst"]] = edge["src"]

    outward = collections.defaultdict(set)
    inward = collections.defaultdict(set)
    for edge in graph["edges"]:
        if not edge["type"].startswith("calls"):
            continue
        source = owner.get(edge["src"])
        if source is None:
            continue
        target = edge["dst"]
        if target not in funcs:
            continue
        outward[source].add(target)
        inward[target].add(source)
    return outward, inward


def in_neighbour_dir(path):
    for fragment in NEIGHBOUR_DIRS:
        if fragment in path:
            return True
    return False


def select(graph_path, out_path):
    graph = load_map(graph_path)
    funcs = function_nodes(graph)
    outward, inward = call_edges(graph, funcs)

    seeds = set()
    for node_id, node in funcs.items():
        if node["file"] == SEED_FILE:
            seeds.add(node_id)

    reached = set(seeds)
    for _ in range(HOP_LIMIT):
        wave = set()
        for node_id in reached:
            wave |= outward[node_id]
            wave |= inward[node_id]
        reached |= wave

    chosen = {}
    for node_id in seeds:
        chosen[node_id] = "seed_file"
    for node_id in reached:
        if node_id in chosen:
            continue
        if not in_neighbour_dir(funcs[node_id]["file"]):
            continue
        chosen[node_id] = "map_neighbourhood"

    for node_id, node in funcs.items():
        if "/amd64/" not in node["file"]:
            continue
        if node["name"] not in AMD64_BY_NAME:
            continue
        if node_id in chosen:
            continue
        chosen[node_id] = "hand_picked"

    targets = []
    for node_id, reason in chosen.items():
        node = funcs[node_id]
        record = {
            "id": node_id,
            "target_kind": "func_body",
            "reason": reason,
            "file": node["file"],
            "name": node["name"],
            "start_line": node["start_line"],
            "start_byte": node["start_byte"],
        }
        targets.append(record)

    by_key = {}
    for node in graph["nodes"]:
        key = (node["file"], node["start_line"], node["kind"], node["name"])
        if key in by_key:
            continue
        by_key[key] = node

    for want in LOOP_TARGETS:
        key = (want["file"], want["start_line"], want["kind"], want["name"])
        node = by_key.get(key)
        if node is None:
            print("MISSING loop target in the map: %r" % (key,))
            sys.exit(2)
        record = {
            "id": node["id"],
            "target_kind": "loop_body",
            "reason": "acceptance_path_start",
            "file": node["file"],
            "name": "ABIAnalyzeFuncType.params_loop",
            "start_line": node["start_line"],
            "start_byte": node["start_byte"],
        }
        targets.append(record)

    targets.sort(key=lambda item: (item["file"], item["start_line"]))
    handle = open(out_path, "w")
    json.dump(targets, handle, indent=1)
    handle.write("\n")
    handle.close()

    print("targets: %d" % len(targets))
    per_file = collections.Counter()
    for record in targets:
        per_file[record["file"]] += 1
    for name, count in sorted(per_file.items()):
        print("  %4d  %s" % (count, name))


# ---------------------------------------------------------------- inject

DIARY_IMPORT = "cmd/compile/internal/diary"

DIARY_PACKAGE = '''// Code generated by inject_diary.py. DO NOT EDIT.
//
// The diary: each instrumented spot of the compiler writes its own map
// node id here AS IT IS ENTERED, so the ORDER of visits survives.
// Set COMPILER_DIARY to a file path to switch it on; with the variable
// unset the compiler behaves exactly as before.

package diary

import (
	"os"
	"strconv"
	"sync"
)

var lock sync.Mutex
var out *os.File
var opened bool
var seq int64

func openDiary() {
	path := os.Getenv("COMPILER_DIARY")
	if path == "" {
		return
	}
	flags := os.O_CREATE
	flags = flags | os.O_WRONLY
	flags = flags | os.O_APPEND
	handle, err := os.OpenFile(path, flags, 0o644)
	if err != nil {
		return
	}
	out = handle
}

// Note writes one diary event.  The record is fixed at injection time and
// carries the map node id, the spot's name, and its original file:line.
func Note(record string) {
	lock.Lock()
	if !opened {
		opened = true
		openDiary()
	}
	if out == nil {
		lock.Unlock()
		return
	}
	seq++
	line := strconv.FormatInt(seq, 10)
	line = line + "\\t"
	line = line + record
	line = line + "\\n"
	out.WriteString(line)
	lock.Unlock()
}
'''


def find_body_brace(text, start):
    """Index of the `{` that opens a body, scanning forward from start.

    The body brace is the first `{` whose rest of line is blank.  A brace
    of a composite type (`struct{}`, `map[string]struct{}`) is followed by
    other text on the same line, so this rule steps over those.
    """
    index = start
    limit = len(text)
    while index < limit:
        char = text[index]
        if char == "{":
            probe = index + 1
            while probe < limit and text[probe] in " \t":
                probe = probe + 1
            if probe < limit and text[probe] == "\n":
                return index
        index = index + 1
    return -1


def add_import(text):
    if DIARY_IMPORT in text:
        return text, False
    marker = "\nimport (\n"
    at = text.find(marker)
    if at < 0:
        return text, False
    cut = at + len(marker)
    line = '\t"' + DIARY_IMPORT + '"\n'
    new_text = text[:cut] + line + text[cut:]
    return new_text, True


def inject(targets_path, src_root, dry_run):
    handle = open(targets_path)
    targets = json.load(handle)
    handle.close()

    by_file = collections.defaultdict(list)
    for record in targets:
        by_file[record["file"]].append(record)

    package_dir = os.path.join(src_root, "cmd", "compile", "internal", "diary")
    package_file = os.path.join(package_dir, "diary.go")
    if not dry_run:
        os.makedirs(package_dir, exist_ok=True)
        handle = open(package_file, "w")
        handle.write(DIARY_PACKAGE)
        handle.close()
    print("diary package: %s" % package_file)

    total = 0
    for rel_path, records in sorted(by_file.items()):
        # map paths start with "src/"; src_root already IS that src dir
        trimmed = rel_path
        if trimmed.startswith("src/"):
            trimmed = trimmed[4:]
        full = os.path.join(src_root, trimmed)
        handle = open(full, encoding="utf-8")
        text = handle.read()
        handle.close()

        if "diary.Note(" in text:
            print("SKIP already instrumented: %s" % full)
            continue

        edits = []
        for record in records:
            brace = find_body_brace(text, record["start_byte"])
            if brace < 0:
                print("NO BODY BRACE for %s" % record["id"])
                sys.exit(3)
            payload = record["id"]
            payload = payload + "|" + record["name"]
            payload = payload + "|" + rel_path
            payload = payload + ":" + str(record["start_line"])
            statement = '\n\tdiary.Note("' + payload + '")'
            edits.append((brace + 1, statement))

        edits.sort(key=lambda item: item[0], reverse=True)
        for offset, statement in edits:
            text = text[:offset] + statement + text[offset:]

        text, added = add_import(text)
        if not added:
            print("NO IMPORT BLOCK in %s" % full)
            sys.exit(4)

        if not dry_run:
            handle = open(full, "w", encoding="utf-8")
            handle.write(text)
            handle.close()
        total = total + len(edits)
        print("instrumented %3d spots in %s" % (len(edits), full))

    print("total spots: %d" % total)


# ------------------------------------------------------------------ main

def main():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest="mode", required=True)

    p_select = subs.add_parser("select")
    p_select.add_argument("--graph", required=True)
    p_select.add_argument("--out", required=True)

    p_inject = subs.add_parser("inject")
    p_inject.add_argument("--targets", required=True)
    p_inject.add_argument("--src", required=True)
    p_inject.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()
    if args.mode == "select":
        select(args.graph, args.out)
        return
    inject(args.targets, args.src, args.dry_run)


if __name__ == "__main__":
    main()
INJECT_DIARY_PY_EOF
cat > /work/diary/diary_targets.json <<'DIARY_TARGETS_JSON_EOF'
[
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:1212-1281:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "Config",
  "start_line": 39,
  "start_byte": 1212
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:1283-1366:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "InParams",
  "start_line": 43,
  "start_byte": 1283
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:1368-1453:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "OutParams",
  "start_line": 47,
  "start_byte": 1368
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:1455-1535:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "InRegistersUsed",
  "start_line": 51,
  "start_byte": 1455
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:1537-1619:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "OutRegistersUsed",
  "start_line": 55,
  "start_byte": 1537
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:1621-1711:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "InParam",
  "start_line": 59,
  "start_byte": 1621
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:1713-1805:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "OutParam",
  "start_line": 63,
  "start_byte": 1713
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:1807-1891:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "SpillAreaOffset",
  "start_line": 67,
  "start_byte": 1807
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:1893-1971:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "SpillAreaSize",
  "start_line": 71,
  "start_byte": 1893
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:2251-2372:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "ArgWidth",
  "start_line": 79,
  "start_byte": 2251
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:3590-3746:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "Offset",
  "start_line": 108,
  "start_byte": 3590
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:3926-4369:func",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "RegisterTypes",
  "start_line": 118,
  "start_byte": 3926
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:4371-4703:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "RegisterTypesAndOffsets",
  "start_line": 137,
  "start_byte": 4371
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:4705-5956:func",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "appendParamTypes",
  "start_line": 148,
  "start_byte": 4705
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:6150-7404:func",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "appendParamOffsets",
  "start_line": 197,
  "start_byte": 6150
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:7924-8299:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "FrameOffset",
  "start_line": 249,
  "start_byte": 7924
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:8941-9161:func",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "NewABIConfig",
  "start_line": 277,
  "start_byte": 8941
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:9195-9260:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "Which",
  "start_line": 282,
  "start_byte": 9195
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:9477-9557:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "LocalsOffset",
  "start_line": 289,
  "start_byte": 9477
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:9746-9858:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "FloatIndexFor",
  "start_line": 296,
  "start_byte": 9746
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:10004-10281:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "NumParamRegs",
  "start_line": 303,
  "start_byte": 10004
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:10699-11833:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "ABIAnalyzeTypes",
  "start_line": 315,
  "start_byte": 10699
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:12127-13356:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "ABIAnalyzeFuncType",
  "start_line": 353,
  "start_byte": 12127
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:12455-12460:local_var",
  "target_kind": "loop_body",
  "reason": "acceptance_path_start",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "ABIAnalyzeFuncType.params_loop",
  "start_line": 362,
  "start_byte": 12455
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:13858-14278:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "ABIAnalyze",
  "start_line": 397,
  "start_byte": 13858
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:14280-15210:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "updateOffset",
  "start_line": 410,
  "start_byte": 14280
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:15375-15614:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "regString",
  "start_line": 438,
  "start_byte": 15375
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:15732-16297:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "ToString",
  "start_line": 449,
  "start_byte": 15732
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:16413-16802:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "String",
  "start_line": 469,
  "start_byte": 16413
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:17224-17314:func",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "align",
  "start_line": 492,
  "start_byte": 17224
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:17389-17489:func",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "alignTo",
  "start_line": 497,
  "start_byte": 17389
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:17546-17681:func",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "nextSlot",
  "start_line": 505,
  "start_byte": 17546
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:17900-19209:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "allocateRegs",
  "start_line": 514,
  "start_byte": 17900
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:19681-20459:func",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "setup",
  "start_line": 573,
  "start_byte": 19681
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:20680-21192:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "assignParam",
  "start_line": 603,
  "start_byte": 20680
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:21321-21801:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "tryAllocRegs",
  "start_line": 623,
  "start_byte": 21321
 },
 {
  "id": "src/cmd/compile/internal/abi/abiutils.go:22668-23277:method",
  "target_kind": "func_body",
  "reason": "seed_file",
  "file": "src/cmd/compile/internal/abi/abiutils.go",
  "name": "ComputePadding",
  "start_line": 657,
  "start_byte": 22668
 },
 {
  "id": "src/cmd/compile/internal/amd64/galign.go:266-603:func",
  "target_kind": "func_body",
  "reason": "hand_picked",
  "file": "src/cmd/compile/internal/amd64/galign.go",
  "name": "Init",
  "start_line": 14,
  "start_byte": 266
 },
 {
  "id": "src/cmd/compile/internal/amd64/ggen.go:663-1127:func",
  "target_kind": "func_body",
  "reason": "hand_picked",
  "file": "src/cmd/compile/internal/amd64/ggen.go",
  "name": "ginsnop",
  "start_line": 28,
  "start_byte": 663
 },
 {
  "id": "src/cmd/compile/internal/amd64/ssa.go:545-1041:func",
  "target_kind": "func_body",
  "reason": "hand_picked",
  "file": "src/cmd/compile/internal/amd64/ssa.go",
  "name": "ssaMarkMoves",
  "start_line": 24,
  "start_byte": 545
 },
 {
  "id": "src/cmd/compile/internal/amd64/ssa.go:5467-60141:func",
  "target_kind": "func_body",
  "reason": "hand_picked",
  "file": "src/cmd/compile/internal/amd64/ssa.go",
  "name": "ssaGenValue",
  "start_line": 227,
  "start_byte": 5467
 },
 {
  "id": "src/cmd/compile/internal/amd64/ssa.go:76094-77590:func",
  "target_kind": "func_body",
  "reason": "hand_picked",
  "file": "src/cmd/compile/internal/amd64/ssa.go",
  "name": "ssaGenBlock",
  "start_line": 2454,
  "start_byte": 76094
 },
 {
  "id": "src/cmd/compile/internal/ssagen/ssa.go:1924-11068:func",
  "target_kind": "func_body",
  "reason": "map_neighbourhood",
  "file": "src/cmd/compile/internal/ssagen/ssa.go",
  "name": "InitConfig",
  "start_line": 80,
  "start_byte": 1924
 },
 {
  "id": "src/cmd/compile/internal/ssagen/ssa.go:13891-25634:func",
  "target_kind": "func_body",
  "reason": "map_neighbourhood",
  "file": "src/cmd/compile/internal/ssagen/ssa.go",
  "name": "buildssa",
  "start_line": 294,
  "start_byte": 13891
 },
 {
  "id": "src/cmd/compile/internal/ssagen/ssa.go:26600-27229:method",
  "target_kind": "func_body",
  "reason": "map_neighbourhood",
  "file": "src/cmd/compile/internal/ssagen/ssa.go",
  "name": "zeroResults",
  "start_line": 645,
  "start_byte": 26600
 },
 {
  "id": "src/cmd/compile/internal/ssagen/ssa.go:61602-80770:method",
  "target_kind": "func_body",
  "reason": "map_neighbourhood",
  "file": "src/cmd/compile/internal/ssagen/ssa.go",
  "name": "stmt",
  "start_line": 1663,
  "start_byte": 61602
 },
 {
  "id": "src/cmd/compile/internal/ssagen/ssa.go:105960-128635:method",
  "target_kind": "func_body",
  "reason": "map_neighbourhood",
  "file": "src/cmd/compile/internal/ssagen/ssa.go",
  "name": "exprCheckPtr",
  "start_line": 3028,
  "start_byte": 105960
 },
 {
  "id": "src/cmd/compile/internal/ssagen/ssa.go:128637-129230:method",
  "target_kind": "func_body",
  "reason": "map_neighbourhood",
  "file": "src/cmd/compile/internal/ssagen/ssa.go",
  "name": "resultOfCall",
  "start_line": 3754,
  "start_byte": 128637
 },
 {
  "id": "src/cmd/compile/internal/ssagen/ssa.go:131885-142332:method",
  "target_kind": "func_body",
  "reason": "map_neighbourhood",
  "file": "src/cmd/compile/internal/ssagen/ssa.go",
  "name": "append",
  "start_line": 3848,
  "start_byte": 131885
 },
 {
  "id": "src/cmd/compile/internal/ssagen/ssa.go:157560-159965:func",
  "target_kind": "func_body",
  "reason": "map_neighbourhood",
  "file": "src/cmd/compile/internal/ssagen/ssa.go",
  "name": "softfloatInit",
  "start_line": 4681,
  "start_byte": 157560
 },
 {
  "id": "src/cmd/compile/internal/ssagen/ssa.go:164185-166433:method",
  "target_kind": "func_body",
  "reason": "map_neighbourhood",
  "file": "src/cmd/compile/internal/ssagen/ssa.go",
  "name": "openDeferSave",
  "start_line": 4837,
  "start_byte": 164185
 },
 {
  "id": "src/cmd/compile/internal/ssagen/ssa.go:183949-184368:method",
  "target_kind": "func_body",
  "reason": "map_neighbourhood",
  "file": "src/cmd/compile/internal/ssagen/ssa.go",
  "name": "canSSA",
  "start_line": 5371,
  "start_byte": 183949
 },
 {
  "id": "src/cmd/compile/internal/ssagen/ssa.go:196580-196781:method",
  "target_kind": "func_body",
  "reason": "map_neighbourhood",
  "file": "src/cmd/compile/internal/ssagen/ssa.go",
  "name": "putArg",
  "start_line": 5761,
  "start_byte": 196580
 },
 {
  "id": "src/cmd/compile/internal/ssagen/ssa.go:213184-223907:method",
  "target_kind": "func_body",
  "reason": "map_neighbourhood",
  "file": "src/cmd/compile/internal/ssagen/ssa.go",
  "name": "dottype1",
  "start_line": 6298,
  "start_byte": 213184
 },
 {
  "id": "src/cmd/compile/internal/ssagen/ssa.go:253200-256624:func",
  "target_kind": "func_body",
  "reason": "map_neighbourhood",
  "file": "src/cmd/compile/internal/ssagen/ssa.go",
  "name": "defframe",
  "start_line": 7533,
  "start_byte": 253200
 },
 {
  "id": "src/cmd/compile/internal/ssagen/ssa.go:269565-270774:func",
  "target_kind": "func_body",
  "reason": "map_neighbourhood",
  "file": "src/cmd/compile/internal/ssagen/ssa.go",
  "name": "deferstruct",
  "start_line": 8100,
  "start_byte": 269565
 }
]
DIARY_TARGETS_JSON_EOF
wc -l /work/diary/inject_diary.py /work/diary/diary_targets.json

say "inject"
cd /work/diary
python3 inject_diary.py inject --targets diary_targets.json --src "$SRC/src"
INJ=$?
echo "inject_exit=$INJ"
[ "$INJ" -ne 0 ] && exit 83
grep -c 'diary.Note(' "$SRC/src/cmd/compile/internal/abi/abiutils.go"

say "rebuild cmd/compile (no coverage; the diary replaces the tally)"
cd "$SRC/src/cmd" || exit 84
set -x
"$GO" build -o /persist/compile_diary cmd/compile
B=$?
set +x
echo "build_exit=$B"
if [ "$B" -ne 0 ]; then echo FATAL_BUILD_FAILED; exit 85; fi
ls -l /persist/compile_diary

say "probe"
P=/work/probe; rm -rf $P; mkdir -p $P; cd $P
printf 'module probe\n\ngo 1.28\n' > go.mod
cat > probe.go <<'EOF'
package main

//go:noinline
func af(a, b int32) int32 { return a - b }

func main() {
	println(af(7, 3))
}
EOF

say "capture the real compile command line"
"$GO" build -a -work -x -o /work/probe.bin . > /work/x.stdout 2> /work/x.log
echo "build_exit=$?"
WORKDIR=$(grep -m1 '^WORK=' /work/x.log | cut -d= -f2)
CMDLINE=$(grep -F "$GOROOT/pkg/tool/linux_amd64/compile" /work/x.log | grep -F 'probe.go' | tail -1)
echo "WORKDIR=$WORKDIR"
echo "$CMDLINE"
[ -z "$CMDLINE" ] && { echo FATAL_NO_CMDLINE; exit 86; }

say "replay that exact command line with the diary compiler substituted"
RAW=/work/diary.raw
rm -f "$RAW"
NEW=$(printf '%s' "$CMDLINE" | sed "s#$GOROOT/pkg/tool/linux_amd64/compile #/persist/compile_diary #")
cd $P
env WORK="$WORKDIR" COMPILER_DIARY="$RAW" bash -c "$NEW"
echo "instrumented_compile_exit=$?"
ls -l $P "$RAW"

say "shape the diary"
python3 - "$RAW" /out/diary_go.txt <<'PY'
import sys
raw = open(sys.argv[1])
out = open(sys.argv[2], "w")
count = 0
for line in raw:
    line = line.rstrip("\n")
    if line == "":
        continue
    seq, record = line.split("\t", 1)
    parts = record.split("|")
    node_id = parts[0]
    name = parts[1]
    where = parts[2]
    out.write("%s\t%s\t%s\t%s\n" % (seq, node_id, name, where))
    count = count + 1
raw.close()
out.close()
print("events=%d" % count)
PY
echo "shape_exit=$?"
wc -l /out/diary_go.txt

say "distinct spots and their visit counts"
cut -f3 /out/diary_go.txt | sort | uniq -c | sort -rn

say "acceptance excerpt: the abi chain in order"
grep -nE 'ABIAnalyzeFuncType.params_loop|assignParam|tryAllocRegs|allocateRegs' /out/diary_go.txt | head -60

say "first 40 events"
head -40 /out/diary_go.txt

say disk
du -sh /persist/gosrc /persist/gocache /persist/compile_diary
df -h /work /persist | sed -n 1,4p
echo DONE_OK
