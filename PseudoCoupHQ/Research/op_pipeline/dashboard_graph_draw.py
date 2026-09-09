#!/usr/bin/env python3
"""dashboard_graph_draw.py -- PANE 4, DRAWN.  The compiler graph as a
picture, emitted as inline SVG by python, with no JavaScript anywhere.

Node: hq.research.compiler_graph.dashboard (`coverage_view`, pane 4),
drawing hq.research.compiler_graph.graph.

WHAT DEE ASKED FOR, AND WHAT EACH FIGURE ANSWERS
------------------------------------------------
the owner, 2026-09-04: "i want to be able to see the graph in a visualization.
i dont want a messy massive un-organized graph like graphiz or whatever.
i want it well structure since the compiler/interpreters are well
structured."  And, on what the graph is for: "the graph is to verify that
youre not fucking lying to me about actually extracting everything ive
intended for us to extract.  i want to be able to see a basic structure
and dynamic connections and the traced directional connections made by
our probes."

So three figures, in his three words, over ONE layout:

  1. BASIC STRUCTURE -- the compiler's own organisation.  Directories are
     bands, in the order the source tree has them; files are boxes inside
     their own directory, in path order; a box's height is the number of
     definitions the file holds.  Nothing is thrown at a force layout and
     nothing moves between renders: a file's place is a function of its
     path, so the picture IS the compiler's shape and a reader can
     recognise it.  The inter-file `calls` edges are drawn as arcs.
  2. DYNAMIC CONNECTIONS -- which parts our probes actually entered.  The
     SAME boxes, in the SAME places, filled in proportion to the bodies a
     probe entered.  A file no probe ever entered is drawn hollow and
     named.  Where coverage was never measured the boxes carry the
     not-measured hatch and the figure says so by name.
  3. THE TRACED DIRECTIONAL CONNECTIONS -- direction of travel through
     the compiler.  Again the same boxes.  In AGGREGATE: every ordered
     file-to-file transition the corpus's diaries walk, drawn as an
     arrow whose weight is how many probes walk it.  PER PROBE: one
     probe's own ordered walk, numbered in the order it happened.  PER
     OPERATOR TRACED VARIANT: the transitions EXCLUSIVE to one variant --
     the connections the union over all probes cannot tell apart from
     ubiquity.

NO JAVASCRIPT.  The python page has none by its own settled rule.  Every
figure is inline SVG that this module emits as text; every control is an
`onclick="python:..."` the engine rewrites into an attribute its own
delegated listener reads.  Nothing executable is written into the page.

THE MEMORY RULE.  `graph_cpp.json` is 331 MB and is NEVER OPENED HERE, in
whole or in part.  Every figure is drawn from the small tracked summaries
the CORE already names:

    graph_<lang>_files.json     41 KB - 184 KB   the structure
    graph_<lang>_defs.json      0.6 - 3.3 MB     one file's definitions,
                                                 read only on expanding it
    coverage_<lang>_files.json  2.6 MB           the dynamic layer and the
                                                 aggregate direction
    coverage_<lang>_summary.json                 the populations
    variant_connections_<lang>.json  0.6-3.2 MB  the third kind

THE CHRONOLOGY.  Every read goes through the caller's `Moment`, so the
drawing is as of the page's one selected moment, and a summary version
control does not hold at that commit makes the figure DRAW ITS REFUSAL
and name the file -- never an approximation, and never a present-day
number standing in for the past.

A COMPILER WITH NO GRAPH SAYS SO BY NAME.  java, cpython, php and ruby
have no graph at all; rust and swift have a graph and no probe traces.
Both are drawn as what they are.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25).  No
operator token is a key, a grouping, a pairing, a row structure, a
candidate selection or a comparison scope here.  Boxes are keyed by
SOURCE PATH, edges by a pair of paths, variants by the machine-form
digest `variant_id` their own artifact carries.  An operator token
appears exactly once per unit, as a display label on a variant's member
list, and is read back by nothing -- replace every label with a glyph and
every figure is unchanged.  Checked by
`check_dashboard_py_no_spelling.py` over this file.
"""

import json
import os

# ---------------------------------------------------------------------------
# the compilers this pane speaks about, and what answers for each
# ---------------------------------------------------------------------------

#: (display name, the key its artifacts are named with, what the graph
#: covers).  THE TABLE IS THE ONLY PLACE A COMPILER IS NAMED.
DRAWN_COMPILERS = [
    ("go", "go", "the go compiler, cmd/compile"),
    ("c and cpp (clang)", "cpp", "clang and llvm, serving both c and cpp"),
    ("rust", "rust", "rustc"),
    ("swift", "swift", "the swift compiler"),
]

#: a compiler with NO GRAPH AT ALL.  Named, never approximated.
NO_GRAPH_AT_ALL = [
    ("java", "the JIT's own source is the compiler here; it has not been "
             "built as a graph"),
    ("cpython", "the interpreter's handler C source is the compiler here; "
                "it has not been built as a graph"),
    ("php", "the interpreter's handler C source is the compiler here; it "
            "has not been built as a graph"),
    ("ruby", "the interpreter's handler C source is the compiler here; it "
             "has not been built as a graph"),
]

#: the coverage summary that answers for a graph, where one exists.  A
#: compiler absent from this table has no probe traces and the dynamic and
#: directional figures say so by name rather than drawing nothing.
COVERAGE_SUMMARY_OF = {
    "go": "coverage_go_files.json",
    "cpp": "coverage_cpp_files.json",
}

VARIANTS_OF = {
    "go": "variant_connections_go.json",
    "cpp": "variant_connections_c_and_cpp.json",
    "rust": "variant_connections_rust.json",
    "swift": "variant_connections_swift.json",
}

#: THE PRINTED CEILINGS.  Every one of them is drawn on the figure beside
#: the population it was cut from, because a ceiling that is not printed
#: is a hidden sample (the rule pane 3 already carries).
EDGE_CEILING = 100
ARROW_CEILING = 80
VARIANT_MENU_CEILING = 40
PROBE_MENU_CEILING = 24

#: the figure's own geometry.  Fixed, so a box's place is a function of
#: its path and nothing else -- the same file is in the same place at
#: every moment and in every figure.
SHEET_WIDTH = 1180
MARGIN = 10
BAND_HEAD = 20
BAND_GAP = 10
ROW_GAP = 5


def esc(text):
    """the caller's escape, restated here so this module imports nothing
    from the page it draws into."""
    return (str("" if text is None else text)
            .replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def commas(number):
    try:
        return "{:,}".format(number)
    except (TypeError, ValueError):
        return esc(number)


# ---------------------------------------------------------------------------
# THE LAYOUT.  The compiler's own organisation, and nothing else.
# ---------------------------------------------------------------------------

class Sheet:
    """where every file box sits.  Directories in path order, files inside
    their directory in path order, boxes on a fixed grid.

    There is no physics here and no randomness: run it twice on the same
    summary and every box is at the same coordinate.  That is what makes
    the picture the compiler's shape rather than a picture of a layout
    algorithm.
    """

    def __init__(self, rows, dense=False):
        self.dense = dense
        self.box_w = 84 if dense else 138
        self.box_h = 17 if dense else 24
        self.font = 8 if dense else 10
        self.columns = max(1, (SHEET_WIDTH - 2 * MARGIN)
                           // (self.box_w + ROW_GAP))
        self.boxes = {}
        self.order = []
        self.bands = []
        self._place(rows)

    def _place(self, rows):
        by_directory = {}
        for row in rows:
            path = row.get("file") or ""
            folder = os.path.dirname(path) or "."
            by_directory.setdefault(folder, []).append(row)
        top = MARGIN
        biggest = 1
        for row in rows:
            biggest = max(biggest, int(row.get("defs") or 0))
        for folder in sorted(by_directory):
            members = sorted(by_directory[folder],
                             key=lambda r: r.get("file") or "")
            band_top = top
            top += BAND_HEAD
            for at, row in enumerate(members):
                column = at % self.columns
                line = at // self.columns
                x = MARGIN + column * (self.box_w + ROW_GAP)
                y = top + line * (self.box_h + ROW_GAP)
                path = row["file"]
                self.boxes[path] = {
                    "x": x, "y": y, "w": self.box_w, "h": self.box_h,
                    "row": row, "file": path,
                    "name": os.path.basename(path),
                    "weight": (int(row.get("defs") or 0)) / float(biggest),
                }
                self.order.append(path)
            lines = (len(members) + self.columns - 1) // self.columns
            top += lines * (self.box_h + ROW_GAP) + BAND_GAP
            self.bands.append({"folder": folder, "top": band_top,
                               "bottom": top, "files": len(members),
                               "defs": sum(int(r.get("defs") or 0)
                                           for r in members)})
        self.height = top + MARGIN

    def centre(self, path):
        box = self.boxes.get(path)
        if not box:
            return None
        return (box["x"] + box["w"] / 2.0, box["y"] + box["h"] / 2.0)

    def has(self, path):
        return path in self.boxes


# ---------------------------------------------------------------------------
# the SVG primitives
# ---------------------------------------------------------------------------

def open_sheet(sheet, title):
    return ('<svg class="dg" viewBox="0 0 %d %d" width="100%%" '
            'preserveAspectRatio="xMinYMin meet" role="img" '
            'aria-label="%s"><defs>'
            '<marker id="dgtip" viewBox="0 0 8 8" refX="7" refY="4" '
            'markerWidth="5" markerHeight="5" orient="auto">'
            '<path d="M0,0 L8,4 L0,8 z" class="dg-tip"/></marker>'
            '<pattern id="dghatch" width="6" height="6" '
            'patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            '<line x1="0" y1="0" x2="0" y2="6" class="dg-hatchline"/>'
            '</pattern></defs>'
            % (SHEET_WIDTH, int(sheet.height), esc(title)))


def close_sheet():
    return "</svg>"


def bands_of(sheet):
    out = []
    for band in sheet.bands:
        out.append('<rect class="dg-band" x="%d" y="%d" width="%d" '
                   'height="%d" rx="4"/>'
                   % (MARGIN - 4, band["top"] - 2,
                      SHEET_WIDTH - 2 * MARGIN + 8,
                      band["bottom"] - band["top"] - BAND_GAP + 4))
        out.append('<text class="dg-band-name" x="%d" y="%d">%s '
                   '<tspan class="dg-dim">%d files, %s definitions</tspan>'
                   '</text>'
                   % (MARGIN, band["top"] + 12, esc(band["folder"]),
                      band["files"], commas(band["defs"])))
    return "".join(out)


def box_of(sheet, path, fill, klass, label_note, tip, click=None):
    box = sheet.boxes[path]
    name = box["name"]
    #: THE NOTE OWNS THE RIGHT-HAND END OF THE BOX, so the name is cut to
    #: what is left.  Found by looking at the drawing rather than at the
    #: code: with the name given the whole width, a long file name ran
    #: straight through its own count ("addressingmodes2go", "9/51"
    #: overlapping "intrinsics.go") and both became unreadable.
    per = sheet.font * 0.64
    taken = (len(str(label_note)) + 1) * per if label_note else 0
    room = int((box["w"] - 12 - taken) / per)
    shown = name if len(name) <= room else name[:max(1, room - 1)] + "…"
    opener = ('<g class="dg-hit" onclick="python:%s">' % click) if click \
        else "<g>"
    return ("".join([
        opener,
        '<title>%s</title>' % esc(tip),
        '<rect class="%s" x="%d" y="%d" width="%d" height="%d" rx="3" '
        'fill-opacity="%.3f"/>' % (klass, box["x"], box["y"], box["w"],
                                   box["h"], fill),
        '<text class="dg-file" x="%d" y="%d" font-size="%d">%s</text>'
        % (box["x"] + 4, box["y"] + box["h"] - 5, sheet.font, esc(shown)),
        ('<text class="dg-note" x="%d" y="%d" font-size="%d">%s</text>'
         % (box["x"] + box["w"] - 3, box["y"] + box["h"] - 5,
            sheet.font, esc(label_note))) if label_note else "",
        "</g>",
    ]))


def arc(sheet, a, b, klass, weight=1.0, directed=False):
    """one connection, as a curve that bows away from the straight line so
    two files joined both ways do not draw on top of each other."""
    one = sheet.centre(a)
    two = sheet.centre(b)
    if not one or not two:
        return ""
    (x1, y1), (x2, y2) = one, two
    mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    span = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 or 1.0
    bow = min(60.0, span * 0.18)
    cx = mx - (y2 - y1) / span * bow
    cy = my + (x2 - x1) / span * bow
    tip = ' marker-end="url(#dgtip)"' if directed else ""
    return ('<path class="%s" d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" '
            'stroke-width="%.2f"%s/>'
            % (klass, x1, y1, cx, cy, x2, y2, weight, tip))


def legend(items):
    out = ['<div class="dg-legend">']
    for mark, words in items:
        out.append('<span class="dg-key"><i class="%s"></i>%s</span>'
                   % (mark, esc(words)))
    out.append("</div>")
    return "".join(out)


def figure(number, heading, population, svg, note=None):
    return "".join([
        '<div class="dg-fig">',
        '<h3>figure %s — %s</h3>' % (number, esc(heading)),
        '<div class="dg-pop">%s</div>' % population,
        ('<div class="dg-note-line">%s</div>' % note) if note else "",
        '<div class="dg-sheet">%s</div>' % svg,
        '</div>',
    ])


def refusal_figure(number, heading, what):
    return "".join([
        '<div class="dg-fig">',
        '<h3>figure %s — %s</h3>' % (number, esc(heading)),
        '<p class="gap">not drawn: %s</p>' % what,
        '</div>',
    ])


# ---------------------------------------------------------------------------
# figure 1 -- BASIC STRUCTURE
# ---------------------------------------------------------------------------

def draw_structure(sheet, files_doc, focus=None, click=None):
    rows = files_doc.get("files") or []
    edges = files_doc.get("file_edges") or []
    #: file_edges is [index into files, index into files, relation, count].
    #: The relation is a value on the row and is never a key.
    named = []
    for one in edges:
        if len(one) < 4:
            continue
        a, b, relation, many = one[0], one[1], one[2], one[3]
        if a >= len(rows) or b >= len(rows) or a == b:
            continue
        named.append((rows[a].get("file"), rows[b].get("file"),
                      relation, int(many or 0)))
    if focus:
        kept = [one for one in named if focus in (one[0], one[1])]
        cut_from = len(named)
        shown = kept
        ceiling_line = ("%s of %s inter-file connections — the ones that "
                        "touch <b>%s</b>. Click the file again to release it."
                        % (commas(len(kept)), commas(cut_from), esc(focus)))
    else:
        shown = sorted(named, key=lambda one: -one[3])[:EDGE_CEILING]
        ceiling_line = ("the %s heaviest of %s inter-file connections; the "
                        "printed ceiling is %s. Click a file to see its own "
                        "connections alone."
                        % (commas(len(shown)), commas(len(named)),
                           commas(EDGE_CEILING)))

    heaviest = max([one[3] for one in shown] or [1])
    out = [open_sheet(sheet, "the compiler's own organisation"), bands_of(sheet)]
    for a, b, _relation, many in shown:
        weight = 0.4 + 2.6 * (many / float(heaviest))
        klass = "dg-edge hot" if focus and focus in (a, b) else "dg-edge"
        out.append(arc(sheet, a, b, klass, weight, directed=True))
    for path in sheet.order:
        box = sheet.boxes[path]
        row = box["row"]
        kinds = row.get("nodes_by_kind") or {}
        tip = ("%s — %s definitions, %s graph nodes, %s frontier records"
               % (path, commas(row.get("defs")), commas(row.get("nodes")),
                  commas(row.get("frontier"))))
        klass = "dg-box on" if path == focus else "dg-box"
        out.append(box_of(sheet, path, 0.08 + 0.45 * box["weight"], klass,
                          commas(row.get("defs")), tip,
                          click and click(path)))
        del kinds
    out.append(close_sheet())
    return "".join(out), ceiling_line


# ---------------------------------------------------------------------------
# figure 2 -- DYNAMIC CONNECTIONS
# ---------------------------------------------------------------------------

def draw_dynamic(sheet, coverage_doc, focus=None, click=None):
    by_file = {}
    for row in coverage_doc.get("by_file") or []:
        by_file[row.get("file")] = row
    entered = 0
    never = 0
    unmeasured = 0
    out = [open_sheet(sheet, "which parts our probes entered"),
           bands_of(sheet)]
    for path in sheet.order:
        row = by_file.get(path)
        if row is None:
            unmeasured += 1
            tip = ("%s — this file carries no row in the coverage join: no "
                   "body in it was instrumented, so it is a NAMED FRONTIER "
                   "of the join and not a never-visited file" % path)
            out.append(box_of(sheet, path, 1.0, "dg-box unmeasured", "",
                              tip, click and click(path)))
            continue
        instrumented = int(row.get("instrumented") or 0)
        visited = int(row.get("visited") or 0)
        share = (visited / float(instrumented)) if instrumented else 0.0
        if row.get("entered"):
            entered += 1
            klass = "dg-box on" if path == focus else "dg-box"
            out.append(box_of(
                sheet, path, 0.07 + 0.55 * share, klass,
                "%d/%d" % (visited, instrumented),
                "%s — %s of %s instrumented bodies entered by at least one "
                "probe, %s entered by none"
                % (path, commas(visited), commas(instrumented),
                   commas(row.get("never"))),
                click and click(path)))
        else:
            never += 1
            out.append(box_of(
                sheet, path, 0.0, "dg-box hollow", "0",
                "%s — NO PROBE EVER ENTERED THIS FILE. %s bodies were "
                "instrumented in it and none was reached"
                % (path, commas(instrumented)),
                click and click(path)))
    out.append(close_sheet())
    return "".join(out), {"entered": entered, "never": never,
                          "unmeasured": unmeasured}


# ---------------------------------------------------------------------------
# figure 3 -- THE TRACED DIRECTIONAL CONNECTIONS
# ---------------------------------------------------------------------------

def aggregate_transitions(coverage_doc):
    """every ordered file-to-file transition the corpus walks, and how many
    probes walk it.

    The source is each probe's own file-level path -- `file_runs`, runs of
    consecutive events in the same file, in the order the compilation
    happened.  Two consecutive runs ARE one directional connection.
    """
    order = coverage_doc.get("file_order") or []
    walkers = {}
    carried = 0
    total_runs = 0
    for probe in coverage_doc.get("probes") or []:
        runs = probe.get("file_runs") or []
        total_runs += int(probe.get("file_runs_total") or len(runs))
        carried += len(runs)
        seen = set()
        for at in range(len(runs) - 1):
            a = runs[at][0]
            b = runs[at + 1][0]
            if a == b or a >= len(order) or b >= len(order):
                continue
            seen.add((order[a], order[b]))
        for pair in seen:
            walkers[pair] = walkers.get(pair, 0) + 1
    return walkers, {"probes": len(coverage_doc.get("probes") or []),
                     "runs_carried": carried, "runs_total": total_runs}


def draw_aggregate_direction(sheet, coverage_doc):
    walkers, counted = aggregate_transitions(coverage_doc)
    ranked = sorted(walkers.items(), key=lambda pair: (-pair[1], pair[0]))
    shown = [one for one in ranked
             if sheet.has(one[0][0]) and sheet.has(one[0][1])][:ARROW_CEILING]
    heaviest = max([one[1] for one in shown] or [1])
    touched = set()
    for (a, b), _many in shown:
        touched.add(a)
        touched.add(b)
    out = [open_sheet(sheet, "the direction of travel through the compiler"),
           bands_of(sheet)]
    for (a, b), many in shown:
        out.append(arc(sheet, a, b, "dg-arrow",
                       0.5 + 3.0 * (many / float(heaviest)), directed=True))
    for path in sheet.order:
        out.append(box_of(sheet, path, 0.30 if path in touched else 0.05,
                          "dg-box" if path in touched else "dg-box quiet",
                          "", path))
    out.append(close_sheet())
    line = ("%s of %s distinct ordered file-to-file transitions, the "
            "heaviest first; the printed ceiling is %s. A transition's "
            "weight is how many of the %s probes walk it — the heaviest "
            "here is walked by %s. Read off %s file runs carried in the "
            "summary out of %s the probes actually walked; the rest are one "
            "ranged read away in the join itself."
            % (commas(len(shown)), commas(len(walkers)),
               commas(ARROW_CEILING), commas(counted["probes"]),
               commas(heaviest), commas(counted["runs_carried"]),
               commas(counted["runs_total"])))
    return "".join(out), line


def draw_one_probe(sheet, coverage_doc, probe_id):
    order = coverage_doc.get("file_order") or []
    found = None
    for probe in coverage_doc.get("probes") or []:
        if probe.get("probe") == probe_id:
            found = probe
            break
    if found is None:
        return None, None
    runs = found.get("file_runs") or []
    steps = []
    for at in range(len(runs) - 1):
        a, b = runs[at][0], runs[at + 1][0]
        if a >= len(order) or b >= len(order) or a == b:
            continue
        steps.append((order[a], order[b]))
    out = [open_sheet(sheet, "one probe's own walk"), bands_of(sheet)]
    touched = {}
    for at, (a, b) in enumerate(steps):
        if not (sheet.has(a) and sheet.has(b)):
            continue
        out.append(arc(sheet, a, b, "dg-arrow one", 1.1, directed=True))
        touched.setdefault(a, at + 1)
        touched.setdefault(b, at + 2)
    for path in sheet.order:
        at = touched.get(path)
        out.append(box_of(sheet, path, 0.35 if at else 0.04,
                          "dg-box" if at else "dg-box quiet",
                          str(at) if at else "", path))
    out.append(close_sheet())
    line = ("<b>%s</b> — %s file runs carried of %s the probe walked, "
            "%s ordered file-to-file steps drawn; the number on a box is "
            "the step it was first entered at. %s diary events in all."
            % (esc(probe_id), commas(len(runs)),
               commas(found.get("file_runs_total") or len(runs)),
               commas(len(steps)), commas(found.get("events"))))
    return "".join(out), line


def draw_one_variant(sheet, variants_doc, variant_id):
    found = None
    for one in variants_doc.get("variants") or []:
        if one.get("variant_id") == variant_id:
            found = one
            break
    if found is None:
        return None, None
    steps = []
    for example in found.get("exclusive_transition_examples") or []:
        a = (example.get("from") or {}).get("file")
        b = (example.get("to") or {}).get("file")
        if a and b:
            steps.append((a, b, example))
    out = [open_sheet(sheet, "one operator traced variant's own transitions"),
           bands_of(sheet)]
    touched = set()
    for a, b, _example in steps:
        if not (sheet.has(a) and sheet.has(b)):
            continue
        out.append(arc(sheet, a, b, "dg-arrow only", 1.6, directed=True))
        touched.add(a)
        touched.add(b)
    for path in sheet.order:
        out.append(box_of(sheet, path, 0.30 if path in touched else 0.04,
                          "dg-box" if path in touched else "dg-box quiet",
                          "", path))
    out.append(close_sheet())
    #: the display labels of this variant's members.  THE ONLY PLACE A
    #: TOKEN APPEARS, and nothing reads it back: the variant was grouped
    #: by the machine-form digest above, which is what `variant_id` is.
    labels = []
    for member in found.get("members") or []:
        mark = member.get("operator")
        if mark is not None and mark not in labels:
            labels.append(mark)
    machine = found.get("machine_form") or {}
    line = ("<b>%s</b> — %s members, %s nodes entered, %s transitions, of "
            "which %s are walked by this variant and no other and %s are "
            "backed by a static call edge. %s of those exclusive "
            "transitions are carried as examples and are the arrows drawn "
            "here. Its machine form: <code>%s</code> — <code>%s</code>. "
            "Display labels on its members, read back by nothing: %s."
            % (esc(variant_id), commas(found.get("member_count")),
               commas(found.get("nodes_entered")),
               commas(found.get("transitions")),
               commas(found.get("transitions_exclusive_to_this_variant")),
               commas(found.get("transitions_backed_by_a_static_call_edge")),
               commas(len(steps)), esc(machine.get("bytes")),
               esc(machine.get("text")),
               esc(", ".join(labels)) or "none"))
    return "".join(out), line
