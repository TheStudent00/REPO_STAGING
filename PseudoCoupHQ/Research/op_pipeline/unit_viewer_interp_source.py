"""unit_viewer_interp_source.py -- hq.research.compiler_graph.dashboard
(the unit_viewer sub-node, the interpreter units).

An interpreter arch-unit is carved out of a handler the interpreter's
own C source defines.  The dashboard's pane 1 shows that C source where
a record on disk carries it and says "no source recorded" where none
does.  Deciding which is which at draw time would mean the page
searching a dozen artifacts, so the join is made here, once, into a
sidecar the page reads: canon39_interp_source.json.

The rule, and it is mechanical:

  - the unit id's second half is the handler's name
    (`cpython/long_add_fastpath` -> `long_add_fastpath`);
  - the declared artifacts below are walked for rows that carry a C
    file, a line number and the source line at it;
  - a row belongs to the handler when the row's enclosing definition
    starts with the handler's name, with a `_fastpath` tail (the
    carve's own word, not the source's) dropped first;
  - a unit with no such row gets no source and the cause is written
    down.

Nothing here is keyed by an operator token: the key is the unit id.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "canon39_interp_source.json"

# every artifact searched, named so the search scope is on the page and
# not in an agent's memory.
SEARCHED = [
    "interp_cpython.json",
    "interp_php.json",
    "interp_php_handlers.json",
    "interp_ruby.json",
    "interp_ruby_handlers.json",
    "interp_jvm.json",
    "interp_canon35.json",
    "canon_interp_units_cpython.json",
    "canon_interp_units_java.json",
    "canon_interp_units_ruby_php.json",
]

C_SUFFIX = (".c", ".h", ".c.h", ".inc")


def rows_of(doc):
    """every row anywhere in a document that carries file + line + source."""
    found = []

    def walk(node):
        if isinstance(node, dict):
            f = node.get("file")
            line = node.get("line")
            src = node.get("source")
            if isinstance(f, str) and f.endswith(C_SUFFIX) and src is not None:
                found.append({
                    "file": f,
                    "line": line,
                    "source": src,
                    "enclosing_definition": node.get("enclosing_definition"),
                    "evidence": node.get("evidence"),
                })
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(doc)
    return found


def handler_of(uid):
    name = uid.split("/", 1)[1] if "/" in uid else uid
    if name.endswith("_fastpath"):
        name = name[:-len("_fastpath")]
    return name


def build():
    interp = json.load(open(os.path.join(HERE, "canon39_interp.json")))
    corpus = []
    for path in SEARCHED:
        full = os.path.join(HERE, path)
        if not os.path.exists(full):
            continue
        try:
            doc = json.load(open(full))
        except ValueError:
            continue
        for row in rows_of(doc):
            row["read_from"] = path
            corpus.append(row)
    units = {}
    with_source = 0
    without = {}
    for uid in sorted(interp["units"]):
        handler = handler_of(uid)
        mine = []
        for row in corpus:
            enc = row.get("enclosing_definition") or ""
            if enc.startswith(handler + "(") or enc.startswith(handler + " "):
                mine.append(row)
        if mine:
            with_source += 1
            mine.sort(key=lambda r: (r["file"], r["line"] or 0))
            seen = set()
            once = []
            for r in mine:
                mark = (r["file"], r["line"], r["source"])
                if mark in seen:
                    continue
                seen.add(mark)
                once.append(r)
            mine = once
            units[uid] = {
                "unit": uid,
                "handler": handler,
                "source_recorded": True,
                "read_from": mine[0]["read_from"],
                "file": mine[0]["file"],
                "lines": [
                    {"line": r["line"], "text": r["source"]} for r in mine
                ],
                "evidence": mine[0].get("evidence"),
            }
        else:
            cause = (
                "no artifact of the searched set carries a C line whose "
                "enclosing definition is '%s'" % handler)
            units[uid] = {
                "unit": uid,
                "handler": handler,
                "source_recorded": False,
                "cause": cause,
            }
            without[uid] = cause
    doc = {
        "meta": {
            "node": "hq.research.compiler_graph.dashboard",
            "generated_by": "unit_viewer_interp_source.py",
            "population": "the 11 interpreter arch-units of canon39_interp.json",
            "searched": SEARCHED,
            "note": (
                "a sidecar: canon39_interp.json is not edited.  The key is "
                "the unit id."),
        },
        "tally": {
            "interpreter_units": len(units),
            "units_with_the_handler_c_source": with_source,
            "units_with_no_source_recorded": len(without),
        },
        "units": units,
        "units_with_no_source_recorded_and_why": without,
    }
    path = os.path.join(HERE, OUT)
    json.dump(doc, open(path, "w"), indent=1, sort_keys=True)
    print(json.dumps(doc["tally"], indent=1))
    for uid, rec in units.items():
        state = "C source" if rec["source_recorded"] else "no source recorded"
        print("  %-64s %s" % (uid, state))
    print("wrote %s (%d bytes)" % (OUT, os.path.getsize(path)))


if __name__ == "__main__":
    build()
