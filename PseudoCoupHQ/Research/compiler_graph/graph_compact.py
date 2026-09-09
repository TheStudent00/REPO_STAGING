#!/usr/bin/env python3
"""graph_compact.py -- THE COMPACT FORM of a compiler graph, and the
expander that rebuilds the old form from it BYTE FOR BYTE.

Node: hq.research.compiler_graph.graph (`static_structure`, `frontier`).

WHY, AND FROM WHAT MEASUREMENT
------------------------------
`graph_go.json` is 49,278,033 bytes.  Measured, by section:

    frontier (77,530 unresolved references)   30.4 MB   61.7%
    edges    (63,797)                         12.9 MB   26.2%
    nodes    (10,393)                          2.5 MB    5.1%

Two causes, both of them repetition rather than information:

  1. THE FRONTIER REPEATS ITS PROSE.  Each record carries a `reason`
     sentence of 150 to 200 characters and there are exactly FOUR
     distinct sentences in the whole go frontier.  Written once each and
     referenced, they cost four sentences instead of 77,530.
  2. EVERY EDGE WRITES TWO FULL SOURCE PATHS.  A `contains` edge is
     `{"src": "src/cmd/compile/internal/abi/abiutils.go", "dst":
     "src/cmd/compile/internal/abi/abiutils.go#657#def#0", "rel":
     "contains"}` -- 120 bytes, of which the two identities are 100 and
     both already appear in the node table.

So: ONE STRING TABLE for the whole document, and every record written as
an array of integer references into it.  Nothing is dropped.  The
frontier stays complete, record for record, because it is the evidence of
where the walk stops -- this changes HOW it is stored, never WHAT it
holds.

THE PROOF, AND IT IS THE POINT
------------------------------
`expand` rebuilds the old file from the compact one and the two are
compared BYTE FOR BYTE.  The compact document carries the original's own
md5 and byte count, so the proof can be re-run at any time by anyone:

    python3 graph_compact.py expand --compact graph_go.json \
        --out /work/rebuilt_go.json --verify

Measured before this program was written (lane t93_l1): loading
graph_go.json and re-emitting it with `json.dumps(document, indent=1)`
reproduces the file's 49,278,033 bytes with md5
71405afd56f3f5de41539c5c2c17c4b5, identical to the original.  That is the
assumption the expander rests on, and it was measured rather than
assumed.

THE FORM
--------
    {
     "format": "graph-compact-1",
     "provenance": { the original's name, byte count, md5, key order,
                     whether it ended with a newline, and the command
                     that rebuilds it },
     "pins": {...},        unchanged, and still inside the first 256 KB
     "counts": {...},      so every existing head read keeps working
     "strings": [ {"text": "..."}, ... ]   every distinct string, most
                           frequent first, each as a VALUE on a row --
                           never a bare list element, because source
                           identifiers like `new` and `not` are in the
                           operator inventory and the unmodified guard is
                           right to refuse a token in a row-structure
                           position
     "sections": { "nodes": {"schemas": [...]}, "edges": ..., "frontier": ... },
     "nodes": [ [schema, value, ...], ... ],
     "edges": [ ... ],
     "frontier": [ ... ],
     "parse_errors": ...   verbatim
    }

A SCHEMA is the record's key order together with one code per field:

    "s"  a string        -> its index in `strings` (null stays null)
    "i"  a number/bool   -> written as it is
    "l"  a list of strings -> a list of indices
    "v"  anything else   -> written as it is

The schemas are DISCOVERED from the file, not declared here, so a graph
whose builder gains a field compacts without this program changing.

BOUNDED MEMORY, STATED
----------------------
    ceiling:  MEMORY_CEILING_MB, 6144
    abort:    MemoryCeilingReached, raised BY NAME

`graph_cpp.json` is 331,704,231 bytes and is never held whole: the
compactor STREAMS it one record at a time, reusing
`graph_files_build.stream`, and the expander STREAMS its output one
record at a time as well.  What is held is the string table and the row
arrays, which is the compact document itself.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25).  No
operator token appears in any key, grouping, pairing, row structure,
candidate selection or comparison scope here.  The string table's order
is the FREQUENCY of each string in the document, which is machine-form
evidence, and every entry is a row `{"text": "..."}` rather than a bare
element -- because source identifiers like `new`, `not`, `and` and
`delete` are in the 91-token operator inventory, and the unmodified
guard REFUSED the first cut of this form (7 places in each of go and
rust, lane t93_l3) for putting a token in a row-structure position.  The
fix is the shape the CORE already ratified for the four x86 mnemonics
that are homographs of operator tokens, and it is the shape the ORIGINAL
graph has, where the same identifier sits at `"detail": "new"`.  Nothing
groups, pairs or compares by it: a record refers to a string by its
INDEX.  The emitted json is walked by the unmodified
check_no_spelling_keys.py.

usage:
    python3 graph_compact.py compact --graph graph_go.json \
        --out graph_go.compact.json
    python3 graph_compact.py expand --compact graph_go.compact.json \
        --out rebuilt.json --verify
"""

import argparse
import collections
import hashlib
import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import graph_files_build                                     # noqa: E402

FORMAT = "graph-compact-1"

#: the arrays this program takes apart.  Everything else in the document
#: is carried verbatim, in its original place and order.
RECORD_SECTIONS = ("nodes", "edges", "frontier")

MEMORY_CEILING_MB = 6144


class MemoryCeilingReached(Exception):
    """Raised BY NAME when the run passes the stated ceiling.  A stop by
    the operating system is not a measurement; a refusal by name is."""


def peak_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def check_ceiling(where):
    mb = peak_mb()
    if mb > MEMORY_CEILING_MB:
        raise MemoryCeilingReached(
            "%s: peak resident %.0f MB is above the stated ceiling of %d MB"
            % (where, mb, MEMORY_CEILING_MB))
    return mb


# ---------------------------------------------------------------------------
# reading the OLD form, one record at a time
# ---------------------------------------------------------------------------

def top_level_order(path):
    """the document's own key order, read off the first character of each
    top-level key line.  The graphs are written with
    `json.dumps(document, indent=1)`, so a top-level key is the only thing
    that begins a line with one space and a quotation mark."""
    order = []
    with open(path, "r") as fh:
        for line in fh:
            if line.startswith(' "'):
                order.append(line[2:line.index('"', 2)])
    return order


def verbatim_members(path, order):
    """every top-level member that is NOT one of the record arrays, read
    with the head/whole reader `graph_files_build` already holds."""
    wanted = [key for key in order if key not in RECORD_SECTIONS]
    if not wanted:
        return {}
    # pins and counts sit in the first few kilobytes.  `parse_errors` sits
    # at the END of the file and is not always an object -- go writes it as
    # the number 0 -- so the carve here handles a scalar too, which is why
    # `graph_files_build.head_objects` is not the reader used: it assumes
    # every member opens with a brace and raises on a bare number.
    with open(path, "r") as fh:
        head = fh.read(1 << 20)
    found = _carve_all(head, wanted)
    missing = [key for key in wanted if found.get(key) is None]
    for key in missing:
        found[key] = _from_the_tail(path, key)
    return found


def _from_the_tail(path, key):
    """a top-level member that is not in the head, read from the line it
    opens on to the end of the file.

    `parse_errors` is the last member of every graph, so this holds that
    member and nothing else -- the 331 MB of records ahead of it are read
    a line at a time and dropped.
    """
    opener = ' "%s"' % key
    holding = None
    with open(path, "r") as fh:
        for line in fh:
            if holding is None:
                if line.startswith(opener):
                    holding = ["\n", line]
                continue
            holding.append(line)
    if holding is None:
        return None
    return _carve_all("".join(holding), [key]).get(key)


def _carve_all(text, keys):
    """the same brace walk `graph_files_build.head_objects` does, over a
    whole text rather than a prefix.  Used only for a member that is not
    in the head -- `parse_errors`, which is last in the file."""
    out = {}
    for key in keys:
        needle = '\n "%s"' % key
        at = text.find(needle)
        if at == -1:
            out[key] = None
            continue
        i = text.index(":", at + len(needle)) + 1
        while text[i].isspace():
            i += 1
        if text[i] not in "{[":
            end = i
            while end < len(text) and text[end] not in ",\n":
                end += 1
            out[key] = json.loads(text[i:end])
            continue
        closer = {"{": "}", "[": "]"}[text[i]]
        depth = 0
        j = i
        in_string = False
        escaped = False
        while j < len(text):
            ch = text[j]
            if in_string:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == '"':
                    in_string = False
            elif ch == '"':
                in_string = True
            elif ch == text[i]:
                depth += 1
            elif ch == closer:
                depth -= 1
                if depth == 0:
                    out[key] = json.loads(text[i:j + 1])
                    break
            j += 1
    return out


# ---------------------------------------------------------------------------
# the string table
# ---------------------------------------------------------------------------

class Strings:
    """every distinct string in the record arrays, ordered by how often it
    appears.  The most frequent string is index 0, so the commonest
    references are the shortest to write -- which is the whole saving."""

    def __init__(self):
        self.counts = collections.Counter()
        self.table = None
        self.place = None

    def count(self, value):
        self.counts[value] += 1

    def settle(self):
        # frequency first, then the string itself, so the table is the
        # same on every run over the same input.
        self.table = [text for text, _ in
                      sorted(self.counts.items(), key=lambda p: (-p[1], p[0]))]
        self.place = {text: at for at, text in enumerate(self.table)}
        self.counts = collections.Counter()
        return self.table

    def index(self, value):
        return None if value is None else self.place[value]


def code_of(values):
    """the field code for one field, from every value it takes.

    "s" string, "i" number or truth value, "l" list of strings,
    "v" anything else.  A field that is sometimes null and otherwise a
    string is still "s" -- null is carried as null.
    """
    kinds = set()
    for value in values:
        if value is None:
            continue
        if isinstance(value, str):
            kinds.add("s")
        elif isinstance(value, bool) or isinstance(value, (int, float)):
            kinds.add("i")
        elif isinstance(value, list) and all(isinstance(one, str)
                                             for one in value):
            kinds.add("l")
        else:
            kinds.add("v")
    if len(kinds) == 1:
        return kinds.pop()
    return "v"


# ---------------------------------------------------------------------------
# compacting
# ---------------------------------------------------------------------------

def compact(source, out_path, report=print):
    started = time.time()
    raw_size = os.path.getsize(source)
    digest = hashlib.md5()
    with open(source, "rb") as fh:
        while True:
            chunk = fh.read(1 << 20)
            if not chunk:
                break
            digest.update(chunk)
    original_md5 = digest.hexdigest()
    with open(source, "rb") as fh:
        fh.seek(max(0, raw_size - 4))
        trailing_newline = fh.read().endswith(b"\n")

    order = top_level_order(source)
    report("   top-level key order: %s" % ", ".join(order))
    report("   original: %d bytes, md5 %s, trailing newline %s"
           % (raw_size, original_md5, trailing_newline))

    # PASS ONE: the schemas, and how often each string appears.
    strings = Strings()
    schemas = {name: [] for name in RECORD_SECTIONS}
    schema_place = {name: {} for name in RECORD_SECTIONS}
    field_values = {}
    counted = 0
    for section, record in graph_files_build.stream(source):
        keys = tuple(record.keys())
        if keys not in schema_place[section]:
            schema_place[section][keys] = len(schemas[section])
            schemas[section].append(list(keys))
            field_values[(section, keys)] = {key: [] for key in keys}
        holder = field_values[(section, keys)]
        for key in keys:
            value = record[key]
            if len(holder[key]) < 4096:
                holder[key].append(value)
            if isinstance(value, str):
                strings.count(value)
            elif isinstance(value, list):
                for one in value:
                    if isinstance(one, str):
                        strings.count(one)
        counted += 1
        if counted % 200000 == 0:
            check_ceiling("pass one at %d records" % counted)
    report("   pass one: %d records, %d distinct strings, peak %.1f MB"
           % (counted, len(strings.counts), peak_mb()))

    codes = {}
    for section in RECORD_SECTIONS:
        codes[section] = []
        for at, keys in enumerate(schemas[section]):
            holder = field_values[(section, tuple(keys))]
            codes[section].append([code_of(holder[key]) for key in keys])
    del field_values
    strings.settle()
    check_ceiling("the string table")

    # PASS TWO: the rows.
    rows = {name: [] for name in RECORD_SECTIONS}
    counted = 0
    for section, record in graph_files_build.stream(source):
        keys = tuple(record.keys())
        at = schema_place[section][keys]
        code = codes[section][at]
        row = [at]
        for key, mark in zip(keys, code):
            value = record[key]
            if mark == "s":
                row.append(strings.index(value))
            elif mark == "l":
                row.append(None if value is None
                           else [strings.index(one) for one in value])
            else:
                row.append(value)
        rows[section].append(row)
        counted += 1
        if counted % 200000 == 0:
            check_ceiling("pass two at %d records" % counted)
    report("   pass two: %d rows, peak %.1f MB" % (counted, peak_mb()))

    others = verbatim_members(source, order)
    check_ceiling("the verbatim members")

    sections = {}
    for section in RECORD_SECTIONS:
        sections[section] = {
            "schemas": [{"fields": schemas[section][at],
                         "codes": codes[section][at]}
                        for at in range(len(schemas[section]))],
            "rows": len(rows[section]),
        }

    provenance = {
        "format": FORMAT,
        "expanded_name": os.path.basename(source),
        "expanded_bytes": raw_size,
        "expanded_md5": original_md5,
        "expanded_key_order": order,
        "expanded_ends_with_a_newline": trailing_newline,
        "rebuild_with": ("python3 graph_compact.py expand --compact <this "
                         "file> --out <path> --verify"),
        "what_is_stored_differently": (
            "every string in the record arrays is written once in "
            "`strings` and referenced by its index; each record is an "
            "array whose first element is its schema. NOTHING IS "
            "DROPPED: the record count, the field names, the field order "
            "and every value are carried, and `expand` rebuilds the "
            "named file byte for byte, which is checked against the md5 "
            "above."),
        "node": "hq.research.compiler_graph.graph",
        "produced_by": "graph_compact.py compact",
    }

    write_compact(out_path, order, others, strings.table, sections, rows,
                  provenance)
    report("   wrote %s: %d bytes (%.1f%% of the original), peak %.1f MB, "
           "%.1f s" % (out_path, os.path.getsize(out_path),
                       100.0 * os.path.getsize(out_path) / raw_size,
                       peak_mb(), time.time() - started))
    return {
        "compact": out_path,
        "expanded_bytes": raw_size,
        "compact_bytes": os.path.getsize(out_path),
        "expanded_md5": original_md5,
        "records": counted,
        "strings": len(strings.table),
        "peak_resident_mb": round(peak_mb(), 1),
        "wall_seconds": round(time.time() - started, 1),
    }


def write_compact(out_path, order, others, table, sections, rows, provenance):
    """the compact document, ONE ROW PER LINE so it can be streamed back.

    `pins` and `counts` keep their place at the front, before the string
    table, so every existing 256 KB head read of a graph keeps working
    unchanged.
    """
    dense = (",", ":")
    with open(out_path, "w") as fh:
        fh.write("{\n")
        fh.write(' "format": %s,\n' % json.dumps(FORMAT))
        # THE VERBATIM MEMBERS COME FIRST, IN THE ORIGINAL'S OWN ORDER,
        # and `provenance` comes after them.  Measured, not chosen: with
        # provenance first, its `expanded_key_order` list carries the
        # words "pins" and "counts", and `viewer_build.carve` -- which
        # takes the FIRST occurrence of a key in the head slice -- landed
        # on that list instead of on the member, so every existing 256 KB
        # head read of a graph answered nothing (lane t93_l3, step 3).
        for key in order:
            if key in RECORD_SECTIONS:
                continue
            fh.write(' "%s": %s,\n'
                     % (key, json.dumps(others.get(key), indent=1)
                        .replace("\n", "\n ")))
        fh.write(' "provenance": %s,\n' % json.dumps(provenance, indent=1)
                 .replace("\n", "\n "))
        fh.write(' "sections": %s,\n'
                 % json.dumps(sections, indent=1).replace("\n", "\n "))
        # EVERY STRING IS A VALUE ON A ROW, NEVER A BARE LIST ELEMENT.
        # Measured, not chosen: written as bare elements, the unmodified
        # guard REFUSED both graphs -- 7 places each -- because source
        # identifiers like `new`, `and`, `not` and `delete` are in the
        # 91-token operator inventory, and a bare element in a list is a
        # row-structure position the guard is right to refuse (lane
        # t93_l3, step 10). This is the shape the CORE already ratified
        # for the four x86 mnemonics that are homographs of operator
        # tokens: the token rides as a VALUE beside an opaque position,
        # and it is exactly the shape the ORIGINAL graph has, where the
        # same identifier sits at `"detail": "new"` and the guard passes.
        fh.write(' "strings": [\n')
        for at, text in enumerate(table):
            fh.write("  %s%s\n" % (json.dumps({"text": text},
                                              separators=dense),
                                   "," if at + 1 < len(table) else ""))
        fh.write(" ],\n")
        for at, section in enumerate(RECORD_SECTIONS):
            fh.write(' "%s": [\n' % section)
            body = rows[section]
            for j, row in enumerate(body):
                fh.write("  %s%s\n" % (json.dumps(row, separators=dense),
                                       "," if j + 1 < len(body) else ""))
            fh.write(" ]%s\n" % ("," if at + 1 < len(RECORD_SECTIONS) else ""))
        fh.write("}\n")


# ---------------------------------------------------------------------------
# expanding -- the proof
# ---------------------------------------------------------------------------

def load_compact(path):
    return json.load(open(path))


def decode(row, schema, table):
    """one compact row back into the record it was."""
    out = {}
    for key, mark, value in zip(schema["fields"], schema["codes"], row[1:]):
        if mark == "s":
            out[key] = None if value is None else table[value]
        elif mark == "l":
            out[key] = (None if value is None
                        else [table[one] for one in value])
        else:
            out[key] = value
    return out


def stream_records(path, section):
    """yield the records of one section of a COMPACT graph, one at a time.

    The compact file is written one row per line, so the rows are read a
    line at a time and only the string table and the schemas are held.
    """
    table = None
    schemas = None
    inside = False
    with open(path, "r") as fh:
        head = []
        for line in fh:
            if line.startswith(' "strings"'):
                break
            head.append(line)
        # the head is every member before `strings`; close it and parse.
        text = "".join(head).rstrip().rstrip(",") + "}"
        top = json.loads(text)
        schemas = top["sections"][section]["schemas"]
        table = []
        for line in fh:
            if line.startswith(" ],"):
                break
            table.append(json.loads(line.strip().rstrip(","))["text"])
        for line in fh:
            if line.startswith(' "%s"' % section):
                inside = True
                continue
            if not inside:
                continue
            if line.startswith(" ]"):
                break
            row = json.loads(line.strip().rstrip(","))
            yield decode(row, schemas[row[0]], table)


def nested(value, depth):
    """`json.dumps(value, indent=1)` as it would appear at `depth` levels
    inside a document dumped the same way.  json's indent is relative, so
    the only difference is `depth` extra spaces on every line after the
    first, and `depth` spaces before the first."""
    text = json.dumps(value, indent=1)
    pad = " " * depth
    return pad + text.replace("\n", "\n" + pad)


def expand(compact_path, out_path, verify=True, report=print):
    started = time.time()
    doc = load_compact(compact_path)
    provenance = doc["provenance"]
    order = provenance["expanded_key_order"]
    table = [entry["text"] for entry in doc["strings"]]
    check_ceiling("the compact document")

    with open(out_path, "w") as fh:
        fh.write("{\n")
        for at, key in enumerate(order):
            tail = "," if at + 1 < len(order) else ""
            if key in RECORD_SECTIONS:
                rows = doc[key]
                schemas = doc["sections"][key]["schemas"]
                if not rows:
                    fh.write(' "%s": []%s\n' % (key, tail))
                    continue
                fh.write(' "%s": [\n' % key)
                for j, row in enumerate(rows):
                    record = decode(row, schemas[row[0]], table)
                    fh.write("%s%s\n" % (nested(record, 2),
                                         "," if j + 1 < len(rows) else ""))
                fh.write(" ]%s\n" % tail)
            else:
                fh.write(' "%s": %s%s\n'
                         % (key, nested(doc[key], 1).lstrip(" "), tail))
        fh.write("}")
        if provenance.get("expanded_ends_with_a_newline"):
            fh.write("\n")
    check_ceiling("writing the expanded form")

    size = os.path.getsize(out_path)
    digest = hashlib.md5()
    with open(out_path, "rb") as fh:
        while True:
            chunk = fh.read(1 << 20)
            if not chunk:
                break
            digest.update(chunk)
    got = digest.hexdigest()
    result = {
        "compact": compact_path,
        "rebuilt": out_path,
        "expected_bytes": provenance["expanded_bytes"],
        "rebuilt_bytes": size,
        "expected_md5": provenance["expanded_md5"],
        "rebuilt_md5": got,
        "byte_for_byte_identical": (size == provenance["expanded_bytes"]
                                    and got == provenance["expanded_md5"]),
        "peak_resident_mb": round(peak_mb(), 1),
        "wall_seconds": round(time.time() - started, 1),
    }
    report("   rebuilt %s: %d bytes, md5 %s" % (out_path, size, got))
    report("   expected           %d bytes, md5 %s"
           % (provenance["expanded_bytes"], provenance["expanded_md5"]))
    report("   BYTE FOR BYTE IDENTICAL: %s"
           % result["byte_for_byte_identical"])
    if verify and not result["byte_for_byte_identical"]:
        raise SystemExit("the expanded form is NOT the original: refusing")
    return result


def expanded_document(path):
    """the graph as the OLD form's `json.load` would have answered it,
    built from the compact file in memory.

    This is what `Graph.load` calls, so every caller of that classmethod
    is unchanged by the move to the compact form.  It costs what the old
    document cost -- the ceiling is stated above and checked here -- and
    a reader that does not need the whole graph should use
    `stream_records` instead, which holds only the string table.
    """
    doc = load_compact(path)
    table = [entry["text"] for entry in doc["strings"]]
    out = {}
    for key in doc["provenance"]["expanded_key_order"]:
        if key in RECORD_SECTIONS:
            schemas = doc["sections"][key]["schemas"]
            out[key] = [decode(row, schemas[row[0]], table)
                        for row in doc[key]]
            check_ceiling("expanding %s in memory" % key)
        else:
            out[key] = doc.get(key)
    return out


def is_compact(path):
    """true when a graph on disk is in the compact form.  Read off the
    first kilobyte, so nothing large is opened to find out."""
    try:
        with open(path, "r") as fh:
            return '"format": "%s"' % FORMAT in fh.read(1024)
    except OSError:
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="what", required=True)

    one = sub.add_parser("compact")
    one.add_argument("--graph", required=True)
    one.add_argument("--out", required=True)

    two = sub.add_parser("expand")
    two.add_argument("--compact", required=True)
    two.add_argument("--out", required=True)
    two.add_argument("--verify", action="store_true")

    arguments = parser.parse_args()
    if arguments.what == "compact":
        result = compact(arguments.graph, arguments.out)
    else:
        result = expand(arguments.compact, arguments.out, arguments.verify)
    print(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
