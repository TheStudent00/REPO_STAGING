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

Lap two adds a SUBJECT to every event: the name of the function OF THE
PROBE that the compiler was working on when the spot ran.  See
SUBJECT_SPOTS below for where that name is reachable and how it is
carried.  Where no subject is open the event carries `-`.

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

# ----------------------------------------------------------- subject spots
#
# A diary event says WHICH SPOT of the compiler ran.  It did not say WHOSE
# code the compiler was working on.  These are the places where the name of
# the function under analysis IS reachable in a local value.
#
# It is NOT reachable at the spots the acceptance chain runs in:
#   ABIAnalyzeFuncType(ft *types.Type)   -- a function TYPE has no name
#   assignParam(typ, name, isResult)     -- `name` is the PARAMETER's name
#   tryAllocRegs(typ) / allocateRegs(..) -- only a type and the assign state
# so the name is taken one level higher and carried down, per goroutine, by
# diary.Enter / the func it returns.  Every spot that runs inside an open
# Enter reports that subject; everything else reports `-`.
#
# Each record:
#   file    path under src/, as the map spells it
#   anchor  the exact declaration line; the injection point is the body
#           brace found by scanning forward from it
#   label   what goes in the diary as the subject-boundary marker
#   expr    a Go expression, valid at that spot, giving the name
SUBJECT_SPOTS = (
    {
        "file": "src/cmd/compile/internal/ssagen/ssa.go",
        "anchor": "func buildssa(fn *ir.Func, worker int, isPgoHot bool) *ssa.Func {",
        "label": "buildssa",
        "expr": "fn.Sym().Name",
    },
    {
        "file": "src/cmd/compile/internal/ssagen/ssa.go",
        "anchor": "func genssa(f *ssa.Func, pp *objw.Progs) {",
        "label": "genssa",
        "expr": "f.Name",
    },
    {
        "file": "src/cmd/compile/internal/gc/compile.go",
        "anchor": "func enqueueFunc(fn *ir.Func, symABIs *ssagen.SymABIs) {",
        "label": "enqueueFunc",
        "expr": "fn.Sym().Name",
    },
    {
        "file": "src/cmd/compile/internal/ssa/debug.go",
        "anchor": "func PopulateABIInRegArgOps(f *Func) {",
        "label": "PopulateABIInRegArgOps",
        "expr": "f.Name",
    },
    {
        "file": "src/cmd/compile/internal/ssa/debug.go",
        "anchor": "func BuildFuncDebugNoOptimized(ctxt *obj.Link, f *Func, "
                  "loggingEnabled bool, stackOffset func(LocalSlot) int32, "
                  "rval *FuncDebug) {",
        "label": "BuildFuncDebugNoOptimized",
        "expr": "f.Name",
    },
)

DIARY_PACKAGE = '''// Code generated by inject_diary.py. DO NOT EDIT.
//
// The diary: each instrumented spot of the compiler writes its own map
// node id here AS IT IS ENTERED, so the ORDER of visits survives.
// Set COMPILER_DIARY to a file path to switch it on; with the variable
// unset the compiler behaves exactly as before.
//
// Lap two adds the SUBJECT: the name of the function the compiler was
// working on.  Enter opens a subject for the calling goroutine and returns
// the func that closes it again; Note stamps every event with the innermost
// subject open on ITS OWN goroutine, or "-" when none is open.

package diary

import (
	"os"
	"runtime"
	"strconv"
	"sync"
)

var lock sync.Mutex
var out *os.File
var opened bool
var seq int64
var subjects = make(map[int64][]string)

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

// goroutineID reads the number off the first line of this goroutine's own
// stack dump.  The compiler compiles several functions at once, so the
// subject has to be per goroutine and not one global.
func goroutineID() int64 {
	var buf [64]byte
	size := runtime.Stack(buf[:], false)
	text := string(buf[:size])
	head := "goroutine "
	if len(text) < len(head) {
		return 0
	}
	if text[:len(head)] != head {
		return 0
	}
	text = text[len(head):]
	end := 0
	for end < len(text) {
		if text[end] < '0' {
			break
		}
		if text[end] > '9' {
			break
		}
		end = end + 1
	}
	value, err := strconv.ParseInt(text[:end], 10, 64)
	if err != nil {
		return 0
	}
	return value
}

func writeEvent(record string, subject string) {
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
	line = line + subject
	line = line + "\\t"
	line = line + record
	line = line + "\\n"
	out.WriteString(line)
	lock.Unlock()
}

func currentSubject(id int64) string {
	lock.Lock()
	stack := subjects[id]
	subject := "-"
	if len(stack) > 0 {
		subject = stack[len(stack)-1]
	}
	lock.Unlock()
	return subject
}

// Note writes one diary event.  The record is fixed at injection time and
// carries the map node id, the spot's name, and its original file:line.
func Note(record string) {
	id := goroutineID()
	subject := currentSubject(id)
	writeEvent(record, subject)
}

// Enter opens a subject for the calling goroutine and returns the func that
// closes it.  Injected as a single statement: defer diary.Enter(...)().
func Enter(spot string, subject string) func() {
	if subject == "" {
		subject = "?"
	}
	id := goroutineID()
	lock.Lock()
	stack := subjects[id]
	stack = append(stack, subject)
	subjects[id] = stack
	lock.Unlock()
	record := "-|subject_enter:" + spot + "|-"
	writeEvent(record, subject)
	return func() {
		leave(id)
	}
}

func leave(id int64) {
	lock.Lock()
	stack := subjects[id]
	if len(stack) > 0 {
		stack = stack[:len(stack)-1]
	}
	if len(stack) == 0 {
		delete(subjects, id)
	} else {
		subjects[id] = stack
	}
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

    subjects_by_file = collections.defaultdict(list)
    for spot in SUBJECT_SPOTS:
        subjects_by_file[spot["file"]].append(spot)

    touched = set(by_file)
    touched |= set(subjects_by_file)

    total = 0
    total_subjects = 0
    for rel_path in sorted(touched):
        records = by_file.get(rel_path, [])
        spots = subjects_by_file.get(rel_path, [])
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
        if "diary.Enter(" in text:
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

        for spot in spots:
            at = text.find(spot["anchor"])
            if at < 0:
                print("NO ANCHOR in %s: %s" % (full, spot["anchor"]))
                sys.exit(5)
            brace = find_body_brace(text, at)
            if brace < 0:
                print("NO BODY BRACE for subject spot %s" % spot["label"])
                sys.exit(3)
            statement = '\n\tdefer diary.Enter("' + spot["label"] + '", '
            statement = statement + spot["expr"] + ')()'
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
        total = total + len(records)
        total_subjects = total_subjects + len(spots)
        print("instrumented %3d spots + %d subject spots in %s"
              % (len(records), len(spots), full))

    print("total spots: %d" % total)
    print("total subject spots: %d" % total_subjects)


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
