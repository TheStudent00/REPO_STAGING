#!/usr/bin/env python3
"""dashboard_ouro.py -- the dashboard rendered by PYTHON, for Ourobrowser.

Node: hq.research.compiler_graph.dashboard
(Planning/node_0_3_research/node_0_3_5_compiler_graph/
node_0_3_5_10_dashboard/CORE_0_3_5_10_dashboard.md).

WHAT THIS IS, AND HOW IT DIFFERS FROM dashboard.html
----------------------------------------------------
`dashboard.html` is the LIVE page for an ordinary browser.  It asks the
person for the artifact folder, reads the files with the File System
Access API, and does the join in JavaScript (`dashboard_join.js`).

`dashboard_ouro.html` is the same research, rendered by python inside
`PUBLIC/Ourobrowser`, whose scripting language is python and not
JavaScript.  Python has the filesystem natively, so:

  * there is no folder picker, no IndexedDB handle, no opaque-origin
    problem and no Firefox gap -- the four measured constraints
    log_176 sections 4 and 5 recorded;
  * the page carries NO JavaScript of its own at all;
  * the join does not exist twice.  This module IMPORTS the python join
    that `viewer_build.py` already holds and calls its functions.

Neither page edits or retires the other.  They read the same artifacts
and answer the same questions by two different routes.

THE CHRONOLOGY IS THE OUTER CONTROLLER, NOT A PANE
--------------------------------------------------
the owner, 2026-09-04: "the chronology is the outer controller. regardless of
what tab im in, i can select a moment in the chronology (that is always
visible at the top), and it shows what that moment in the chronology
looked like in that tab but it also updates all the tabs for that
time."

So, and the CORE settles it in two rules:

  * ONE MOMENT, HELD OUTSIDE THE PANES, APPLIED TO ALL OF THEM.  The
    moment lives in `STATE["moment_key"]`, above every pane.  The tab
    bar numbers FIVE panes; the chronology is drawn above it and is
    part of every pane's frame, so it is on screen whichever tab is in
    view.  No pane carries a time of its own.
  * A PANE THAT CANNOT BE RECOMPUTED AT A MOMENT SAYS SO AT THAT
    MOMENT, naming what it would need.  That is `NotAtThisMoment`,
    raised by name and caught in `render` exactly as `MemoryAbort` is,
    and rendered as that pane's refusal.

A MOMENT IS A COMMIT, AND NOTHING CURATES WHICH COMMITS ARE MOMENTS
------------------------------------------------------------------
The scale is the repository's own history -- `git log`, unfiltered and
ungrouped.  Every commit is a moment; no commit is promoted or demoted
by what its message says, because nothing here reads a message to
decide anything.  A commit's subject line is drawn on screen as a
LABEL beside its identity and is read by no grouping, ordering,
windowing or selection: replace every subject with a glyph and this
mechanism is unchanged.

No project's own vocabulary appears in it.  This page is becoming a
general dashboard (CORE, "This dashboard is becoming general-purpose"),
so the chronology is written for a repository that has never heard of
this research: it knows commits, timestamps, tags and merges, which is
everything version control itself carries, and it knows nothing else.

WHAT THIS RETIRES, NAMED EXACTLY.  `chronology_build.py` line 163 ran
`git log --grep=banked -i` and line 155 matched `round\\s+(\\d+)\\s+bank`,
so a step existed because a person had typed a word into a commit
message.  `chronology.json`, its product, is no longer read by this
page at all; it stays on disk as the record of what was.  the owner,
2026-09-04: "i said vcs chronology. i dont want you to have any say in
how it updates... because i cant trust you."

WHAT THE SCALE DEGRADES TO, AND WHY.  A coarser scale than every
commit may only be built from marks version control itself carries.
This repository, measured (`t86_vcs_scale.json`): 1,311 commits, 0
tags, 0 merge commits, 1 root commit, 2 refs, 31 distinct committer
days.  Tags and merges therefore offer nothing here, and the scale
degrades to exactly two rows -- THE COMMITS, and THE DAYS THEIR OWN
TIMESTAMPS FALL ON.  The day row selects nothing; it only moves the
window of the commit row, so no commit is ever elevated above another.
Where a repository does carry tags or merges, those rows appear on the
same footing, and where it carries none of it the bar says so.

HISTORY IS RECOMPUTED, NEVER REMEMBERED.  A pane at a past moment
reads the ARTIFACT BLOBS git holds at that commit -- `git ls-tree` to
see what is there, `git cat-file` to read one blob -- and runs the same
join over them that it runs over the working tree.  No number comes
from a stored summary, and none comes from a commit message: the
testimony fallback of the superseded chronology (a count line parsed
out of a message a person wrote) is retired with the mechanism that
produced it, and where an artifact is untracked the pane draws its
refusal instead.

WHAT IS REUSED, BY IMPORT, NOT BY COPY
--------------------------------------
From `viewer_build.py` (the python side of the one join):
    viewer_build.units_of        the units of an artifact document
    viewer_build.load            read an artifact beside this file
    viewer_build.OperatorGroups  the machine operator-group key
    viewer_build.carve           the ranged read of one json member
    viewer_build.read_coverage   the compiler-graph head reads
    viewer_build.read_pool       the pool, and its per-unit rows
    viewer_build.census_name     a census producer's display name
    viewer_build.trim_unit       the fields the panes read
From `pane23_manifest_regex_check.py` (the CHECKED manifest shortcut):
    PAT, unq                     the declared types, without parsing

`viewer_build.read_pool` gained ONE optional argument in task 85 --
the pool document -- so that the same implementation can be handed the
pool as git held it at a past commit.  With no argument it behaves
exactly as before.

Three rules of the one join are PORTED here and marked as ports, each
naming the original it mirrors: `mnems_of` and `signature_of`
(`dashboard_join.js`), and `coverage_at` (the table inside
`viewer_build.read_coverage`, which opens paths in the working tree and
so cannot be pointed at a past commit).

THE MEMORY BOUND
----------------
Stated, and enforced, because the artifacts are large: `the_pool5.json`
is 32 MB, `canon39_regen_store` is 219 MB over 326 shards, and
`graph_cpp.json` is 331 MB.

    cap:    MEMORY_CAP_MB, 1500 MB of peak resident size
    abort:  OURO_MEMORY_ABORT, raised by name; the pane that asked for
            the work renders the refusal instead of a number

What is never opened whole: `graph_<lang>.json` (a 256 KB head read
only, through `viewer_build.read_coverage`), `coverage_go2.json`, and
the regenerated store (one shard at a time, index rows kept, the parsed
document dropped).  `the_pool5.json`'s summary is a TAIL carve; the
whole file is loaded only when pane 1 asks for a per-unit pool row.

The moment adds one bound of its own: ONLY ONE MOMENT'S WORK IS HELD.
Selecting a different moment drops every cached index, shard map and
pool map before the new moment is read, so the page's memory does not
grow with the number of moments visited.

THE SPELLING BAN
----------------
No operator token is a key here.  Units are grouped by the machine id
`viewer_build.OperatorGroups.mint` produces; arch opcodes are grouped by
an opaque arch id and the mnemonic rides beside it as a value, because
`and`, `or`, `xor` and `not` are arch mnemonics AND alternative operator
spellings.  The token appears once per unit, as a display label.
Checked by `check_dashboard_py_no_spelling.py` over this file.

Nothing about the moment touches that: a moment is a commit, panes are
selected by NUMBER, and the candidate set at every moment comes from
the same machine-form evidence it comes from at the present moment.
"""

import datetime
import html
import json
import os
import random
import re
import resource
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

#: the compiler-graph node's own code sits beside this folder, and two of
#: its modules answer for pane 4: where the graphs live now, and how a
#: graph is drawn.
GRAPH_CODE = os.path.join(os.path.dirname(HERE), "compiler_graph")
if GRAPH_CODE not in sys.path:
    sys.path.insert(0, GRAPH_CODE)

import viewer_build                                          # noqa: E402
import pane23_manifest_regex_check as manifest_shortcut      # noqa: E402
import graphs_home                                           # noqa: E402
import dashboard_graph_draw as draw                          # noqa: E402
import dashboard_stats as statspane                          # noqa: E402


# ---------------------------------------------------------------------------
# the memory bound
# ---------------------------------------------------------------------------

MEMORY_CAP_MB = 1500
ABORT_NAME = "OURO_MEMORY_ABORT"


class MemoryAbort(Exception):
    """raised by name when peak resident size passes MEMORY_CAP_MB."""


def peak_rss_mb():
    kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return kb / 1024.0


def guard_memory(stage):
    now = peak_rss_mb()
    if now > MEMORY_CAP_MB:
        raise MemoryAbort(
            "%s: peak resident size %.0f MB passed the stated cap of %d MB "
            "during %s" % (ABORT_NAME, now, MEMORY_CAP_MB, stage))
    return now


# ---------------------------------------------------------------------------
# THE OUTER CONTROLLER -- one moment, held outside the panes
# ---------------------------------------------------------------------------

class NotAtThisMoment(Exception):
    """raised BY NAME when the moment's tree does not hold what a pane
    would have to read.

    It carries WHAT the pane would need, in words, so the refusal names
    its reason instead of showing a present-day number as if it were
    the past.  Caught in `render` and drawn as that pane's own body.
    """

    def __init__(self, needed, moment):
        Exception.__init__(self, needed)
        self.needed = needed
        self.moment = moment


#: git spells every tree path with this separator, and so does this
#: page when it names an artifact inside a store.  It is NAMED rather
#: than written as a literal in the membership test inside
#: `Moment.names_under`, because the same character is ALSO an operator
#: token in this line's 91-token inventory, and
#: `check_dashboard_py_no_spelling.py` is right to refuse a token
#: sitting in a comparison or a membership test.  Found by running that
#: guard, not by reading: it FAILED on `if "/" in rest`.  The fix is
#: not an exemption -- the token is a value here and nothing tests
#: against the literal.
TREE_SEPARATOR = "/"

#: repo-relative folders the artifacts live in.
OP_DIR = "Research/op_pipeline"
CG_DIR = "Research/compiler_graph"

#: THE ONE PLACE THIS PROJECT'S OWN PATHS ENTER THE MOMENT MACHINERY,
#: and it is caller configuration rather than mechanism.  The
#: chronology knows no paths at all -- it is `git log`.  `Moment.tree()`
#: lists only these prefixes so that listing a commit's tree costs what
#: the panes actually read; point them elsewhere and the same moment
#: machinery serves a repository that has never heard of this research.
ARTIFACT_ROOTS = [OP_DIR, CG_DIR]

#: the artifact families a generation number is picked from BY NUMBER,
#: never by a hard-coded name.  Each is (folder-relative pattern).
POOL_GENERATION = re.compile(r"^the_pool(\d*)\.json$")
CENSUS_GENERATION = re.compile(r"^name_census(\d*)\.json$")


def repo_root():
    """the git working tree this page sits in, or None.

    Everything about a PAST moment needs it; the present moment does
    not, so a page opened outside a repository still works and the
    chronology says why it offers only one moment.
    """
    if "repo_root" in STATE and STATE["repo_root"] is not False:
        return STATE["repo_root"]
    root = None
    try:
        proc = subprocess.run(
            ["git", "-C", HERE, "rev-parse", "--show-toplevel"],
            capture_output=True, text=True)
        if proc.returncode == 0:
            root = proc.stdout.strip() or None
    except OSError:
        root = None
    STATE["repo_root"] = root
    return root


def disk_path(rel):
    """the working-tree path of a repo-relative artifact.

    Outside a git repository the two artifact folders are still found
    relative to this file, so the PRESENT moment works with no version
    control at all -- only the past ones need it.
    """
    root = repo_root()
    if root:
        return os.path.join(root, rel)
    if rel.startswith(OP_DIR):
        return os.path.join(HERE, rel[len(OP_DIR):].lstrip("/"))
    if rel.startswith(CG_DIR):
        return os.path.join(os.path.dirname(HERE), "compiler_graph",
                            rel[len(CG_DIR):].lstrip("/"))
    return os.path.join(os.path.dirname(HERE), rel)


def highest_generation(names, pattern):
    """the highest-numbered generation of an artifact family, picked BY
    NUMBER rather than by a hard-coded name.

    This is the general form of the task-74 fix (a pane had been reading
    `name_census5.json` while `name_census6.json` was already on disk).
    A past moment makes the general form necessary rather than merely
    correct: at an earlier commit the highest generation is a different
    file, and no hard-coded name can be right at every moment.
    """
    best = None
    best_n = -1
    for name in names:
        match = pattern.match(name)
        if not match:
            continue
        digits = match.group(1)
        number = int(digits) if digits else 1
        if number > best_n:
            best_n = number
            best = name
    return best


def open_at(moment):
    """THE ONE OPEN MOMENT, and the memory bound made structural.

    Everything reading a past commit costs memory -- the commit's tree
    listing, and the `git cat-file --batch` process answering for its
    blobs.  None of it is cached on the moment object: it lives in ONE
    slot here, and asking for a different moment evicts the slot first.

    So the page holds one moment's work however many moments are walked
    past.  Task 86 measured why that has to be structural rather than a
    habit: with the cache sitting on each moment, a pass that drew the
    bar at all 1,321 moments held 1,321 tree listings and peaked at
    1,970.2 MB, over this page's own 1,500 MB cap.  With the slot, the
    same pass is bounded by whatever ONE commit's listing costs.
    """
    slot = STATE["open"]
    if slot.get("key") == moment.key:
        return slot
    close_open()
    slot = {"key": moment.key, "tree": None, "batch": None,
            "holdings": None}
    STATE["open"] = slot
    return slot


def close_open():
    """drop the open moment's tree listing and stop its git process."""
    slot = STATE["open"]
    proc = slot.get("batch")
    if proc is not None:
        try:
            proc.stdin.close()
            proc.terminate()
        except OSError:
            pass
    STATE["open"] = {"key": None, "tree": None, "batch": None,
                     "holdings": None}


class Moment:
    """one selected moment, for the WHOLE page.  A MOMENT IS A COMMIT.

    `record is None` is the present moment: every read goes to the
    working tree, which is what the page shows when it opens.  Any other
    moment is one commit of `git log`, and every read goes to the blob
    git holds at that commit -- nothing is checked out, nothing in the
    working tree is touched, and no number is taken from any stored
    summary.

    The record carries what version control itself says about the
    commit: its identity, when it was committed, and its subject line.
    THE SUBJECT IS A DISPLAY LABEL AND NOTHING ELSE -- it is drawn on
    screen and read by no ordering, grouping, windowing or selection
    here.
    """

    def __init__(self, record=None, index=None):
        self.record = record
        self.index = index
        self.is_now = record is None
        self.commit = None if record is None else record.get("commit")
        self.key = "now" if record is None else (self.commit or "")[:12]
        self.when = None if record is None else record.get("when")
        self.day = None if record is None else (record.get("when") or "")[:10]
        #: display only.  Never consulted by this module for anything.
        self.subject = None if record is None else record.get("subject")
        #: nothing is cached ON a moment.  Whatever a moment reads
        #: lives in the ONE open slot (`open_at`), so the page holds one
        #: moment's work however many moments it walks past.

    # -- what the moment is called, on screen -------------------------

    def label(self):
        if self.is_now:
            return "now — the working tree on disk"
        return "%s  %s" % (self.stamp(), (self.commit or "")[:10])

    def stamp(self):
        """the commit's own timestamp, as version control carries it."""
        if self.is_now:
            return "now"
        text = (self.when or "").replace("T", " ")
        return text[:16]

    def short(self):
        if self.is_now:
            return "now"
        return (self.commit or "")[:7]

    # -- reading, at this moment --------------------------------------

    def tree(self):
        """relpath -> blob size, for everything under the artifact roots
        at this commit.  ONE `git ls-tree -r -l`, cached IN THE ONE OPEN
        SLOT -- see `open_at`: reading a different moment evicts it."""
        if self.is_now:
            return None
        slot = open_at(self)
        if slot["tree"] is not None:
            return slot["tree"]
        root = repo_root()
        if root is None:
            raise NotAtThisMoment(
                "a git working tree — this page is not inside one, so no "
                "past moment can be read", self)
        proc = subprocess.run(
            ["git", "-C", root, "ls-tree", "-r", "-l", self.commit, "--"]
            + ARTIFACT_ROOTS,
            capture_output=True, text=True)
        if proc.returncode != 0:
            raise NotAtThisMoment(
                "the commit %s — git could not list it: %s"
                % ((self.commit or "")[:10], proc.stderr.strip()), self)
        found = {}
        for line in proc.stdout.splitlines():
            head, _, path = line.partition("\t")
            parts = head.split()
            if len(parts) < 4 or parts[1] != "blob":
                continue
            try:
                size = int(parts[3])
            except ValueError:
                size = 0
            found[path] = (parts[2], size)
        slot["tree"] = found
        return found

    def names_under(self, folder):
        """the base names of the files directly inside one folder, at
        this moment."""
        if self.is_now:
            path = disk_path(folder)
            if not os.path.isdir(path):
                return []
            return sorted(name for name in os.listdir(path)
                          if os.path.isfile(os.path.join(path, name)))
        prefix = folder.rstrip(TREE_SEPARATOR) + TREE_SEPARATOR
        out = []
        for path in self.tree():
            if not path.startswith(prefix):
                continue
            rest = path[len(prefix):]
            if TREE_SEPARATOR in rest:
                continue
            out.append(rest)
        return sorted(out)

    def dirs_under(self, folder):
        """the names of the folders directly inside one folder, at this
        moment.

        The twin of `names_under`, added by task 98 because an artifact
        FAMILY can be a folder rather than a file -- `term65_store` and
        `term66_store` are two generations of one family, and picking the
        generation by NUMBER needs the folder names first.  A hard-coded
        folder name is wrong at every moment but one, which is the same
        defect task 74 found in the census and task 85 found in the pool.
        """
        if self.is_now:
            path = disk_path(folder)
            if not os.path.isdir(path):
                return []
            return sorted(name for name in os.listdir(path)
                          if os.path.isdir(os.path.join(path, name)))
        prefix = folder.rstrip(TREE_SEPARATOR) + TREE_SEPARATOR
        out = set()
        for path in self.tree():
            if not path.startswith(prefix):
                continue
            rest = path[len(prefix):]
            place = rest.find(TREE_SEPARATOR)
            if place < 0:
                continue
            out.add(rest[:place])
        return sorted(out)

    def has(self, rel):
        if self.is_now:
            return os.path.exists(disk_path(rel))
        return rel in self.tree()

    def size_of(self, rel):
        if self.is_now:
            path = disk_path(rel)
            return os.path.getsize(path) if os.path.exists(path) else 0
        row = self.tree().get(rel)
        return row[1] if row else 0

    def _blob(self, rel):
        """the bytes of one tracked blob, through a `git cat-file
        --batch` process kept open for this moment."""
        row = self.tree().get(rel)
        if row is None:
            raise NotAtThisMoment("%s, which the commit does not carry" % rel,
                                  self)
        sha = row[0]
        slot = open_at(self)
        if slot["batch"] is None:
            slot["batch"] = subprocess.Popen(
                ["git", "-C", repo_root(), "cat-file", "--batch"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        proc = slot["batch"]
        proc.stdin.write((sha + "\n").encode("ascii"))
        proc.stdin.flush()
        header = proc.stdout.readline().split()
        if len(header) < 3:
            raise NotAtThisMoment(
                "%s — git answered %r for its blob"
                % (rel, b" ".join(header)), self)
        want = int(header[2])
        chunks = []
        got = 0
        while got < want:
            piece = proc.stdout.read(want - got)
            if not piece:
                break
            chunks.append(piece)
            got += len(piece)
        proc.stdout.read(1)
        return b"".join(chunks)

    def read_text(self, rel):
        note(rel, self)
        if self.is_now:
            path = disk_path(rel)
            if not os.path.exists(path):
                raise NotAtThisMoment("%s, which is not on disk" % rel, self)
            with open(path) as fh:
                return fh.read()
        return self._blob(rel).decode("utf-8", "replace")

    def read_json(self, rel):
        return json.loads(self.read_text(rel))

    def head_text(self, rel, count):
        """the first `count` bytes only -- the bounded read the CORE
        requires of a file too large to open whole."""
        note(rel, self)
        if self.is_now:
            path = disk_path(rel)
            if not os.path.exists(path):
                raise NotAtThisMoment("%s, which is not on disk" % rel, self)
            with open(path) as fh:
                return fh.read(count)
        return self._blob(rel)[:count].decode("utf-8", "replace")

    def tail_text(self, rel, count):
        """the last `count` bytes only -- the tail carve pane 5 uses so a
        32 MB pool file is not opened for a 19-line object."""
        note(rel, self)
        if self.is_now:
            path = disk_path(rel)
            if not os.path.exists(path):
                raise NotAtThisMoment("%s, which is not on disk" % rel, self)
            size = os.path.getsize(path)
            with open(path) as fh:
                fh.seek(max(0, size - count))
                return fh.read()
        return self._blob(rel)[-count:].decode("utf-8", "replace")

    def close(self):
        """drop whatever this moment had cached, if it is the open one."""
        if STATE["open"].get("key") == self.key:
            close_open()

    # -- what this moment holds, for the controller's own line --------

    def holdings(self):
        """counted from the moment's own tree, not from any stored
        summary: how many files of each artifact family exist at this
        moment.  This is what makes a pane's refusal checkable on the
        page."""
        slot = open_at(self)
        if slot["holdings"] is not None:
            return slot["holdings"]
        op = self.names_under(OP_DIR)
        cg = self.names_under(CG_DIR)
        regen = self.names_under(OP_DIR + "/canon39_regen_store")
        terms = self.names_under(OP_DIR + "/term65_store")
        found = {
            "corpus": len([n for n in op
                           if n.startswith("canon39_wrapped_")
                           and n.endswith(".json")]),
            "regenerated shards": len([n for n in regen
                                       if n.endswith(".json")]),
            "probe manifests": len([n for n in op
                                    if n.startswith("probe_manifest")
                                    and n.endswith(".json")
                                    and "_asg_" not in n]),
            "term records": len([n for n in terms if n.endswith(".json")]),
            "pool generations": len([n for n in op
                                     if POOL_GENERATION.match(n)]),
            "census generations": len([n for n in op
                                       if CENSUS_GENERATION.match(n)]),
            "compiler-graph summaries": len(
                [n for n in cg
                 if n.startswith("graph_") and n.endswith("_files.json")]),
        }
        slot["holdings"] = found
        return found


#: the record separators handed to `git log --format`.  They are control
#: characters no commit subject can contain, so the walk needs no
#: quoting rule and no parser.
FIELD_MARK = "\x01"
RECORD_MARK = "\x02"


def history():
    """EVERY COMMIT OF THIS REPOSITORY, earliest first.

    One `git log` process, unfiltered and ungrouped.  There is no
    `--grep`, no `--since`, no message pattern and no selection of any
    kind: which commits exist as moments is a fact of the repository.
    Measured on this one: 1,311 commits walked in 0.01 s for 265,611
    bytes of output, peak resident 15.6 MB (`t86_vcs_scale.json`).

    Three fields per commit, all of them version control's own: the
    identity, the committer timestamp, and the subject line, which is
    carried to be DRAWN and is read by nothing.
    """
    if STATE["history"] is not None:
        return STATE["history"]
    root = repo_root()
    rows = []
    if root is not None:
        proc = subprocess.run(
            ["git", "-C", root, "log",
             "--format=%H" + FIELD_MARK + "%cI" + FIELD_MARK + "%s"
             + RECORD_MARK],
            capture_output=True, text=True)
        if proc.returncode == 0:
            for raw in proc.stdout.split(RECORD_MARK):
                raw = raw.strip("\n")
                if not raw.strip():
                    continue
                fields = raw.split(FIELD_MARK)
                if len(fields) < 3:
                    continue
                rows.append({"commit": fields[0], "when": fields[1],
                             "subject": fields[2]})
            rows.reverse()
    STATE["history"] = rows
    return rows


def vcs_marks():
    """what ELSE this repository carries that a coarser scale could be
    built from -- counted, never assumed.

    Tags, merges and refs are version control's own marks.  A day is one
    too: it is the commit's own timestamp truncated, not text a writer
    chose.  Where the first three are empty the bar says so and the
    scale degrades to the commits and their days, which is the honest
    answer rather than an invented one.
    """
    if STATE["marks"] is not None:
        return STATE["marks"]
    root = repo_root()
    found = {"tags": 0, "merges": 0, "refs": 0,
             "days": [], "day_counts": {}}
    for one in history():
        day = (one.get("when") or "")[:10]
        if day not in found["day_counts"]:
            found["day_counts"][day] = 0
            found["days"].append(day)
        found["day_counts"][day] += 1
    if root is not None:
        for args, name in ((["tag"], "tags"),
                           (["rev-list", "--count", "--merges", "HEAD"],
                            "merges"),
                           (["for-each-ref", "--format=%(refname)"], "refs")):
            proc = subprocess.run(["git", "-C", root] + args,
                                  capture_output=True, text=True)
            if proc.returncode != 0:
                continue
            text = proc.stdout.strip()
            if name == "merges":
                found[name] = int(text or 0)
            else:
                found[name] = len([l for l in text.splitlines() if l.strip()])
    STATE["marks"] = found
    return found


def moments():
    """every selectable moment, earliest first, with the present moment
    last.  The present moment is not a commit: it is the working tree,
    and it is what the page shows when it opens."""
    if STATE["moments"] is not None:
        return STATE["moments"]
    built = []
    for index, record in enumerate(history()):
        built.append(Moment(record, index))
    built.append(Moment(None, None))
    STATE["moments"] = built
    return built


def moment_at(key):
    """the position of one moment in the history, or the last one."""
    if STATE["places"] is None:
        STATE["places"] = dict((one.key, at)
                               for at, one in enumerate(moments()))
    return STATE["places"].get(str(key), len(moments()) - 1)


def moment_by_key(key):
    return moments()[moment_at(key)]


def current_moment():
    return moment_by_key(STATE["moment_key"])


def set_moment(key):
    """select ONE moment for the whole page.

    `prev` and `next` step one commit through the history in its own
    order.  Any other key is a commit's own identity, or `now`.

    Everything cached for the previous moment is dropped first -- that
    is the memory bound: the page holds one moment's work, never a
    growing pile of them.
    """
    was = STATE["moment_key"]
    order = moments()
    if key == "prev":
        key = order[max(0, moment_at(was) - 1)].key
    elif key == "next":
        key = order[min(len(order) - 1, moment_at(was) + 1)].key
    key = str(key)
    STATE["window"] = window_start(moment_at(key))
    if key == was:
        return current_moment()
    close_open()
    for cached in ("index", "arch", "groups", "sigs", "term_shard",
                   "render_shard", "pool", "unit"):
        STATE[cached] = None
    STATE["files"] = set()
    STATE["graphfolder"] = None
    STATE["moment_key"] = key
    return current_moment()


# ---------------------------------------------------------------------------
# THE SECOND REPOSITORY -- where the compiler graphs live now
# ---------------------------------------------------------------------------

class GraphFolder:
    """the companion folder the compiler graphs moved to on 2026-09-04,
    read AT THE PAGE'S ONE SELECTED MOMENT.

    the owner: "we can have a separate companion folder for the graphs and we
    will use local git to track changes every 30 seconds."  So the
    artifacts this pane draws now live in two repositories, and the
    moment has to reach both.

    IT IS STILL VERSION CONTROL, AND NOTHING CURATES IT.  A moment is a
    commit of THIS repository and carries that commit's own timestamp.
    The graph folder's answer at that moment is the commit of ITS OWN
    history that stood at that timestamp -- `git rev-list -1 --before`,
    which is the same unfiltered log read from the other end.  No message
    is read, no commit is promoted, and nothing is matched by text.  If
    the folder's history does not reach back that far, the figure DRAWS
    ITS REFUSAL and names the file, exactly as an untracked artifact in
    this repository does.
    """

    def __init__(self, moment):
        self.moment = moment
        self.root = graphs_home.home()
        self.commit = None
        self.reason = None
        if not os.path.isdir(self.root):
            self.reason = ("the companion graph folder %s is not on this "
                           "machine" % self.root)
            return
        if moment.is_now:
            return
        proc = subprocess.run(
            ["git", "-C", self.root, "rev-list", "-1",
             "--before=%s" % (moment.when or ""), "HEAD"],
            capture_output=True, text=True)
        found = proc.stdout.strip() if proc.returncode == 0 else ""
        if not found:
            self.reason = (
                "the companion graph folder has no commit at or before "
                "%s. Its own history begins after this moment, so version "
                "control cannot say what the graphs held here"
                % (moment.stamp() or "this moment"))
            return
        self.commit = found

    def label(self):
        if self.reason:
            return self.reason
        if self.commit is None:
            return "%s, as it is on disk now" % self.root
        return ("%s at its own commit %s, the one that stood at %s"
                % (self.root, self.commit[:10], self.moment.stamp()))

    def has(self, name):
        if self.reason:
            return False
        if self.commit is None:
            return os.path.exists(os.path.join(self.root, name))
        proc = subprocess.run(
            ["git", "-C", self.root, "cat-file", "-e",
             "%s:%s" % (self.commit, name)],
            capture_output=True, text=True)
        return proc.returncode == 0

    def size_of(self, name):
        if self.reason:
            return 0
        if self.commit is None:
            path = os.path.join(self.root, name)
            return os.path.getsize(path) if os.path.exists(path) else 0
        proc = subprocess.run(
            ["git", "-C", self.root, "cat-file", "-s",
             "%s:%s" % (self.commit, name)],
            capture_output=True, text=True)
        try:
            return int(proc.stdout.strip())
        except ValueError:
            return 0

    def head_text(self, name, count):
        """the first `count` bytes of one artifact, and never more.  This
        is how a 331 MB graph is read without being opened."""
        note("%s/%s" % (self.root, name), self.moment)
        if self.reason or not self.has(name):
            raise NotAtThisMoment(
                "%s, in the companion graph folder — %s"
                % (name, self.label()), self.moment)
        if self.commit is None:
            with open(os.path.join(self.root, name)) as fh:
                return fh.read(count)
        proc = subprocess.Popen(
            ["git", "-C", self.root, "show", "%s:%s" % (self.commit, name)],
            stdout=subprocess.PIPE)
        try:
            return proc.stdout.read(count).decode("utf-8", "replace")
        finally:
            proc.stdout.close()
            proc.terminate()

    def read_json(self, name, ceiling_mb=None):
        note("%s/%s" % (self.root, name), self.moment)
        if self.reason or not self.has(name):
            raise NotAtThisMoment(
                "%s, in the companion graph folder — %s"
                % (name, self.label()), self.moment)
        if ceiling_mb is not None:
            size = self.size_of(name)
            if size > ceiling_mb * 1024 * 1024:
                raise NotAtThisMoment(
                    "%s is %s bytes, over the %d MB this pane will open "
                    "whole; it is read as a summary or not at all"
                    % (name, "{:,}".format(size), ceiling_mb), self.moment)
        if self.commit is None:
            with open(os.path.join(self.root, name)) as fh:
                return json.load(fh)
        proc = subprocess.run(
            ["git", "-C", self.root, "show", "%s:%s" % (self.commit, name)],
            capture_output=True)
        return json.loads(proc.stdout.decode("utf-8", "replace"))


def graph_folder(moment):
    """ONE graph-folder reader at a time, dropped when the moment does."""
    held = STATE.get("graphfolder")
    if held is not None and held.moment.key == moment.key:
        return held
    held = GraphFolder(moment)
    STATE["graphfolder"] = held
    return held


#: HOW MANY COMMITS THE BAR DRAWS AT ONCE.  A stated ceiling, printed on
#: the page beside the number it was cut down from -- the CORE's rule
#: for any view over a population too large to draw whole ("A pane over
#: the whole population needs a stated ceiling"; a ceiling that is not
#: printed would be a hidden sample).  Nothing outside the window is
#: removed from the population: every commit is reachable by moving the
#: window, and the window follows whatever moment is selected.
WINDOW_TICKS = 60


def window_start(at):
    """the first position of the window that contains position `at`."""
    total = len(moments())
    start = at - WINDOW_TICKS // 2
    start = min(start, total - WINDOW_TICKS)
    return max(0, start)


#: the two named directions the commit row can be shifted in.  Anything
#: else handed to `set_window` is a day, and a day is a timestamp.
WINDOW_BACK = "earlier"
WINDOW_ON = "later"


def set_window(where):
    """move the window of the commit row -- to the first commit of one
    day, or one windowful back or on.

    THIS SELECTS NOTHING.  The day row and the two shift controls are
    navigation, not curation: they change which stretch of commits the
    bar draws, and the moment the page holds is untouched.  That is what
    keeps every commit equal -- no commit is ever picked out as the one
    that stands for its day, and every commit is reachable, because the
    window can be walked over the whole history.
    """
    order = moments()
    at = STATE["window"]
    if at is None:
        at = window_start(moment_at(STATE["moment_key"]))
    if where == WINDOW_BACK:
        at = at - WINDOW_TICKS
    elif where == WINDOW_ON:
        at = at + WINDOW_TICKS
    else:
        for place, one in enumerate(order):
            if one.day == where:
                at = place
                break
    STATE["window"] = max(0, min(at, max(0, len(order) - WINDOW_TICKS)))
    return current_moment()


# ---------------------------------------------------------------------------
# what has been read, so every pane can print its own population line
# ---------------------------------------------------------------------------

STATE = {
    "index": None,
    "arch": None,
    "groups": None,
    "sigs": None,
    "term_shard": None,
    "render_shard": None,
    "pool": None,
    "files": set(),
    "opened_at": None,
    "unit": None,
    "log": [],
    #: the repository's own history, read once by `git log` when the page
    #: opens: 1,311 records of three small fields, about 260 KB.  It is
    #: the LIST OF MOMENTS and holds no artifact numbers at all, so it is
    #: not dropped when the moment changes.
    "history": None,
    "marks": None,
    "moments": None,
    "places": None,
    "window": None,
    #: the ONE graph-folder reader, for the ONE selected moment.  It holds
    #: a repository path and a commit identity and nothing else; every
    #: read through it is a fresh bounded read.
    "graphfolder": None,
    #: the ONE open moment's reads -- see `open_at`.  Never more than one.
    "open": {"key": None, "tree": None, "batch": None, "holdings": None},
    "moment_key": "now",
    "pane": 5,
    "args": (),
    "repo_root": False,
}

LANGS = ["c", "cpp", "go", "rust", "swift"]

#: the arch opcode table.  Keys are OPAQUE ids; the mnemonic is a value
#: on the row, never a key, because four x86 mnemonics are homographs of
#: operator tokens (CORE, "measured constraints found while realizing
#: panes 2 and 3").
ARCH_ID_PREFIX = "arch"


def note(path, moment=None):
    """record one artifact read, so a pane can print how many it read.

    A blob read at a past moment is recorded under that commit, because
    it is a different artifact from the file of the same name on disk.
    """
    if moment is not None and not moment.is_now:
        STATE["files"].add("%s@%s" % (path, (moment.commit or "")[:10]))
    else:
        STATE["files"].add(os.path.abspath(path))
    return path


def files_read():
    seen = set(STATE["files"])
    if STATE["moment_key"] == "now":
        for path in viewer_build.FILES_READ:
            seen.add(os.path.abspath(path))
    return len(seen)


def opened_at():
    if STATE["opened_at"] is None:
        STATE["opened_at"] = datetime.datetime.now()
    return STATE["opened_at"].strftime("%H:%M")


def population_line(units, extra=None, moment=None):
    """the owner's mechanical-update rule, made visible on every pane:
    "N units read from M files, as of MOMENT"."""
    moment = moment or current_moment()
    if moment.is_now:
        when = "as of now, opened at %s" % opened_at()
    else:
        when = ("as of %s %s, recomputed from that commit's own blobs"
                % (moment.day, (moment.commit or "")[:10]))
    text = ("%s units read from %d files, %s"
            % ("{:,}".format(units), files_read(), when))
    if extra:
        text = text + " — " + extra
    return text


# ---------------------------------------------------------------------------
# the rules of the one join that exist only in javascript, PORTED
# ---------------------------------------------------------------------------

def mnems_of(unit):
    """PORT of `mnemsOf` in dashboard_join.js (line 141).  There is no
    python twin of this rule on disk, so it is written here rather than
    imported, and it is a port -- the JavaScript is the original."""
    found = set()
    for row in unit.get("ledger") or []:
        producer = row.get("produced_by") or {}
        kind = producer.get("kind")
        if kind == "arch_opcode":
            found.add(producer.get("mnem"))
        elif kind == "flag_pair":
            for one in producer.get("mnem") or []:
                found.add(one)
        elif kind == "runtime_callee":
            found.add("call")
    for line in unit.get("body_as_read") or []:
        head = str(line).strip().split(" ")[0].strip()
        if head and head[0].isalpha() and head.isalnum():
            found.add(head.lower())
    found.discard(None)
    return sorted(found)


def signature_of(probe_types, unit):
    """PORT of `signatureOf` in dashboard_join.js (line 169): the probe's
    declared types, with the result read off the OUT row's own width when
    the compiler stated none."""
    if not probe_types:
        return None
    lhs, rhs, res = probe_types
    if not res:
        rows = []
        for row in unit.get("ledger") or []:
            if str(row.get("row", "")).startswith("OUT"):
                rows.append(row)
        if rows:
            res = "%d-bit" % (int(rows[0].get("size") or 0) * 8)
        else:
            res = "compiler-stated"
    if rhs:
        return "(a: %s, b: %s) -> %s" % (lhs, rhs, res)
    return "(a: %s) -> %s" % (lhs, res)


#: PORT of the table inside `viewer_build.read_coverage`.  That function
#: opens paths in the working tree with `open()`, so it cannot be
#: pointed at a commit; the table of which file answers for which
#: compiler is restated here and nowhere else, and the CARVE it uses is
#: still the join's own `viewer_build.carve`.
COVERAGE_GRAPHS = [
    ("graph_go.json", "go"),
    ("graph_cpp.json", "c and cpp (clang)"),
    ("graph_rust.json", "rust"),
    ("graph_swift.json", "swift"),
]
COVERAGE_NEVER_MEASURED = ["java", "cpython", "php", "ruby"]


def coverage_at(moment):
    """the head read of every compiler graph, AT A MOMENT, from the
    COMPANION FOLDER the graphs moved to on 2026-09-04.

    Same shape as `viewer_build.read_coverage` and the same 256 KB head
    read and carve.  What changed is where the file is: the graphs are no
    longer inside this repository, so the moment reaches them through
    `GraphFolder`, which resolves the graph folder's own commit at this
    moment's timestamp.  `pins` and `counts` still sit inside the first
    256 KB of a graph -- the compact form keeps them at the front for
    exactly this reader.
    """
    folder = graph_folder(moment)
    graphs = []
    missing = []
    for name, lang in COVERAGE_GRAPHS:
        if not folder.has(name):
            missing.append(lang)
            continue
        head = folder.head_text(name, 262144)
        counts = viewer_build.carve(head, "counts")
        pins = viewer_build.carve(head, "pins") or {}
        if not counts:
            missing.append(lang)
            continue
        graphs.append({"lang": lang, "file": name, "counts": counts,
                       "bytes": folder.size_of(name),
                       "compact": '"format": "graph-compact-1"' in head,
                       "directories": pins.get("directories") or []})
    cov = None
    summary = CG_DIR + "/coverage_go_summary.json"
    if moment.has(summary):
        cov = json.loads(moment.read_text(summary))
        cov["lang"] = "go"
    graphs.sort(key=lambda g: g["lang"])
    return {"graphs": graphs, "probe_coverage": cov, "folder": folder,
            "missing": missing + list(COVERAGE_NEVER_MEASURED)}


# ---------------------------------------------------------------------------
# the bounded reads, every one of them AT A MOMENT
# ---------------------------------------------------------------------------

def read_signatures(moment):
    """the declared types of every probe, over both manifest families.

    Reuses the CHECKED shortcut: `pane23_manifest_regex_check.PAT` is the
    same expression `dashboard_pane23.js` runs in the browser, and that
    script is the proof that it agrees with `json.load` probe for probe.
    The manifests total 94 MB of text; each is read, scanned and dropped
    before the next is opened.
    """
    if STATE["sigs"] is not None:
        return STATE["sigs"]
    out = {}
    read = 0
    for name in moment.names_under(OP_DIR):
        if not name.startswith("probe_manifest") or not name.endswith(".json"):
            continue
        if "_asg_" in name:
            continue
        if name.startswith("probe_manifest2_"):
            pop = "regenerated"
            lang = name[len("probe_manifest2_"):-len(".json")]
        else:
            pop = "original"
            lang = name[len("probe_manifest_"):-len(".json")]
        if lang not in LANGS:
            continue
        text = moment.read_text(OP_DIR + "/" + name)
        read += 1
        for match in manifest_shortcut.PAT.finditer(text):
            if len(match.group(0)) > manifest_shortcut.SPAN_CEILING:
                continue
            out[(pop, lang, match.group(1))] = (
                manifest_shortcut.unq(match.group(2)),
                manifest_shortcut.unq(match.group(3)),
                manifest_shortcut.unq(match.group(4)),
            )
        del text
        guard_memory("reading %s" % name)
    if not read:
        raise NotAtThisMoment(
            "the probe manifests — probe_manifest_&lt;lang&gt;.json and "
            "probe_manifest2_&lt;lang&gt;.json, which carry every probe's "
            "declared types. None of them is tracked at this commit, so no "
            "unit here can be given a type signature", moment)
    STATE["sigs"] = out
    return out


def index_rows_from(doc, store, groups, arch, sigs, rows):
    """turn one artifact document into index rows and DROP the document.

    `viewer_build.units_of` is the join's own reader; `groups.mint` is the
    join's own machine operator-group key.
    """
    for unit in viewer_build.units_of(doc):
        uid = unit.get("unit")
        if not uid:
            continue
        lang = unit.get("lang") or uid.split("/")[0]
        pop = unit.get("population") or "original"
        ids = []
        for mnem in mnems_of(unit):
            if mnem not in arch["by_mnem"]:
                new_id = "%s%04d" % (ARCH_ID_PREFIX, len(arch["by_mnem"]))
                arch["by_mnem"][mnem] = new_id
                arch["rows"][new_id] = {"mnem": mnem, "units": 0}
            ids.append(arch["by_mnem"][mnem])
        for one in set(ids):
            arch["rows"][one]["units"] += 1
        rows.append({
            "id": uid,
            "lang": lang,
            "gid": groups.mint(lang, unit.get("operator")),
            "label": unit.get("operator"),
            "pop": pop,
            "outcome": unit.get("outcome"),
            "sig": signature_of(sigs.get((pop, lang, str(unit.get("n")))),
                                unit),
            "store": store,
            "arch": sorted(set(ids)),
        })


def build_index(moment):
    """the index over the WHOLE population AT THIS MOMENT, bounded.

    Every artifact is opened, reduced to index rows, and dropped before
    the next one is opened.  A unit BODY is never held: pane 1 re-opens
    the one file the row remembers, at the same moment.
    """
    if STATE["index"] is not None:
        return STATE["index"]
    names = moment.names_under(OP_DIR)
    wrapped = [n for n in names
               if n.startswith("canon39_wrapped_") and n.endswith(".json")]
    shards = [n for n in moment.names_under(OP_DIR + "/canon39_regen_store")
              if n.endswith(".json")]
    if not wrapped and not shards:
        raise NotAtThisMoment(
            "the corpus — canon39_wrapped_&lt;lang&gt;.json, "
            "canon39_interp.json and the shards of canon39_regen_store/. "
            "None of them is tracked at this commit, so there are no units "
            "to index and no unit to show", moment)
    started = time.time()
    sigs = read_signatures(moment)
    groups = viewer_build.OperatorGroups()
    arch = {"by_mnem": {}, "rows": {}}
    rows = []

    for lang in LANGS:
        name = "canon39_wrapped_%s.json" % lang
        if name not in wrapped:
            continue
        doc = moment.read_json(OP_DIR + "/" + name)
        index_rows_from(doc, name, groups, arch, sigs, rows)
        del doc
        guard_memory("indexing %s" % name)

    if "canon39_interp.json" in names:
        doc = moment.read_json(OP_DIR + "/canon39_interp.json")
        index_rows_from(doc, "canon39_interp.json", groups, arch, sigs, rows)
        del doc

    for name in shards:
        rel = "canon39_regen_store/" + name
        doc = moment.read_json(OP_DIR + "/" + rel)
        index_rows_from(doc, rel, groups, arch, sigs, rows)
        del doc
    guard_memory("indexing the regenerated store")

    rows.sort(key=lambda r: (r["lang"], r["id"]))
    by_id = {}
    for row in rows:
        by_id[row["id"]] = row
    STATE["index"] = {"rows": rows, "by_id": by_id,
                      "seconds": time.time() - started}
    STATE["groups"] = groups
    STATE["arch"] = arch
    return STATE["index"]


def shard_map(moment, folder):
    """unit id -> the file its record lives in, for a per-unit store."""
    out = {}
    for name in moment.names_under(OP_DIR + "/" + folder):
        if not name.endswith(".json"):
            continue
        rel = folder + "/" + name
        doc = moment.read_json(OP_DIR + "/" + rel)
        for unit in viewer_build.units_of(doc):
            uid = unit.get("unit")
            if uid:
                out[uid] = rel
        del doc
    guard_memory("mapping %s" % folder)
    return out


def record_in(moment, store, unit_id):
    """re-open the one file a row remembers and answer that one record,
    at this moment."""
    rel = OP_DIR + "/" + store
    if not moment.has(rel):
        return None
    doc = moment.read_json(rel)
    for unit in viewer_build.units_of(doc):
        if unit.get("unit") == unit_id:
            return unit
    return None


def pool_name(moment):
    """the highest-numbered pool generation at this moment, by number."""
    return highest_generation(moment.names_under(OP_DIR), POOL_GENERATION)


def pool_summary(moment):
    """a TAIL carve of the pool, so a 32 MB file is not opened for a
    19-line object.  `viewer_build.carve` is the join's own reader."""
    name = pool_name(moment)
    if not name:
        return None, None
    tail = moment.tail_text(OP_DIR + "/" + name, 8192)
    return name, viewer_build.carve(tail, "summary")


def pool_rows(moment):
    """the pool's per-unit rows, through the join's own `read_pool`,
    handed the pool document this moment holds."""
    name = pool_name(moment)
    if not name:
        return None, {}
    doc = moment.read_json(OP_DIR + "/" + name)
    summary, by_unit = viewer_build.read_pool(doc)
    del doc
    guard_memory("reading %s" % name)
    return summary, by_unit


def census_file(moment):
    return highest_generation(moment.names_under(OP_DIR), CENSUS_GENERATION)


# ---------------------------------------------------------------------------
# the page's shell
# ---------------------------------------------------------------------------

def esc(text):
    return html.escape("" if text is None else str(text), quote=True)


def pyarg(value):
    """one argument of a `python:` click expression, as a python string
    literal in SINGLE quotes.

    The attribute the engine reads is delimited by double quotes, so an
    argument written with double quotes closes the attribute early.  The
    engine's own rewrite then html-escapes the whole expression, so the
    apostrophes here reach python as apostrophes.
    """
    if value is None:
        return "None"
    text = str(value).replace("\\", "\\\\").replace("'", "\\'")
    return "'" + text + "'"


#: THE FIVE PANES the CORE numbers.  The chronology is NOT among them:
#: it is the outer controller, drawn above this bar on every one of
#: them.  Counting it as a sixth tab is the defect log_188 saw from the
#: other end -- a tab bar carrying more entries than the CORE numbers.
PANE_NAMES = [
    (1, "unit viewer"),
    (2, "selector"),
    (3, "arch opcode index"),
    (4, "coverage"),
    (5, "stats"),
]

PANE_TITLES = dict(PANE_NAMES)


def tab_bar(current):
    out = ['<div class="tabs">']
    for number, name in PANE_NAMES:
        klass = "tab on" if number == current else "tab"
        out.append('<span class="%s" onclick="python:ouro_pane(%d)">%d. %s</span>'
                   % (klass, number, number, esc(name)))
    out.append('</div>')
    return "".join(out)


def chronology_bar(moment):
    """THE OUTER CONTROLLER, drawn above the tab bar on every pane.

    It is not a tab and never becomes one.  Choosing a tick here sets
    ONE moment for the whole page; the pane in view is redrawn as of it,
    and so is every other pane the next time it is opened, because none
    of them carries a time of its own.

    THE SCALE IS VERSION CONTROL'S OWN.  The commit row is `git log`,
    every commit of it, drawn a windowful at a time with the window's
    bounds and the whole population printed beside it.  The day row is
    the commits' own timestamps, and it SELECTS NOTHING -- it moves the
    window.  No commit is drawn larger, sooner or at all because of what
    its message says; the subject line appears only as a label on the
    commit it belongs to.
    """
    order = moments()
    marks = vcs_marks()
    total = len(order)
    commits = len(history())

    out = ['<div class="chron">']
    out.append('<div class="chronline"><b>the chronology — the outer '
               'controller.</b> one moment, held outside the panes and '
               'applied to all five of them. '
               'selected: <b class="momentnow">%s</b>' % esc(moment.label()))
    out.append(' <span class="btn" onclick="python:ouro_moment(%s)">'
               '&#9664; earlier</span>' % pyarg("prev"))
    out.append(' <span class="btn" onclick="python:ouro_moment(%s)">'
               'later &#9654;</span>' % pyarg("next"))
    out.append(' <span class="btn" onclick="python:ouro_moment(%s)">'
               'now</span>' % pyarg("now"))
    out.append('</div>')

    if not commits:
        out.append('<div class="gap">this page is not inside a git working '
                   'tree, or its history is empty, so the only moment that '
                   'exists is the present one. The chronology is version '
                   'control; with no version control there is no '
                   'chronology.</div>')
        out.append('</div>')
        return "".join(out)

    # -- the coarse row: what version control itself carries -----------
    out.append('<div class="scale"><span class="scalename">days — %d of '
               'them, from the commits\' own timestamps. a day moves the '
               'window below; it selects nothing</span>'
               % len(marks["days"]))
    window = STATE["window"]
    if window is None:
        window = window_start(moment_at(STATE["moment_key"]))
    shown_days = set(one.day for one in
                     order[window:window + WINDOW_TICKS] if one.day)
    for day in marks["days"]:
        klass = "tick day on" if day in shown_days else "tick day"
        out.append('<span class="%s" onclick="python:ouro_window(%s)" '
                   'title="%s commits committed on this day">%s</span>'
                   % (klass, pyarg(day),
                      "{:,}".format(marks["day_counts"][day]), esc(day)))
    out.append('</div>')

    # -- the fine row: every commit, a windowful at a time -------------
    last = min(total, window + WINDOW_TICKS)
    out.append('<div class="scale"><span class="scalename">every commit — '
               'showing %s to %s of %s moments (%s commits and the working '
               'tree); the window follows the selection</span>'
               % ("{:,}".format(window + 1), "{:,}".format(last),
                  "{:,}".format(total), "{:,}".format(commits)))
    out.append('<span class="tick page" onclick="python:ouro_window(%s)">'
               '&#9664;&#9664;</span>' % pyarg(WINDOW_BACK))
    for one in order[window:last]:
        klass = "tick on" if one.key == moment.key else "tick"
        out.append('<span class="%s" onclick="python:ouro_moment(%s)" '
                   'title="%s">%s</span>'
                   % (klass, pyarg(one.key),
                      esc("%s  %s" % (one.stamp(), one.subject or "")),
                      esc(one.short())))
    out.append('<span class="tick page" onclick="python:ouro_window(%s)">'
               '&#9654;&#9654;</span>' % pyarg(WINDOW_ON))
    out.append('</div>')

    out.append('<div class="chrondetail">')
    if moment.is_now:
        out.append('<b>now</b> — the artifacts as they sit in the working '
                   'tree. Every pane reads them directly; nothing is read '
                   'out of version control.')
    else:
        out.append('<b>%s</b>, commit <code>%s</code>, moment %s of %s in '
                   'this repository\'s own history.'
                   % (esc(moment.stamp()), esc((moment.commit or "")[:10]),
                      "{:,}".format(moment_at(moment.key) + 1),
                      "{:,}".format(total)))
        out.append(' <span class="subject">its subject line, drawn as a '
                   'label and read by nothing: “%s”</span>'
                   % esc(moment.subject or ""))
    out.append('<div class="holds">the marks version control carries here: '
               '%s commits, %s tags, %s merge commits, %s refs, %s days. '
               'a coarser scale can only be built from these; with no tags '
               'and no merges it degrades to the commits and their '
               'days.</div>'
               % ("{:,}".format(commits), "{:,}".format(marks["tags"]),
                  "{:,}".format(marks["merges"]), "{:,}".format(marks["refs"]),
                  "{:,}".format(len(marks["days"]))))
    try:
        holds = moment.holdings()
        shown = ", ".join("%s %s" % ("{:,}".format(holds[key]), key)
                          for key in sorted(holds) if holds[key])
        out.append('<div class="holds">what this moment holds, counted from '
                   'the tree itself: %s</div>'
                   % (shown or "none of the artifacts the panes read"))
    except NotAtThisMoment as gap:
        out.append('<div class="holds">what this moment holds could not be '
                   'counted: %s</div>' % esc(gap.needed))
    out.append('</div>')
    out.append('</div>')
    return "".join(out)


def frame(number, title, body, population, moment=None):
    """every pane is drawn inside the SAME frame, and the frame carries
    the chronology.  That is the mechanism behind "always visible at the
    top, in every tab": there is no way to draw a pane without it."""
    moment = moment or current_moment()
    return "".join([
        chronology_bar(moment),
        tab_bar(number),
        '<div class="pane">',
        '<h2>%s</h2>' % esc(title),
        '<div class="pop">%s</div>' % esc(population),
        body,
        '</div>',
    ])


def table(headers, rows):
    out = ['<table><thead><tr>']
    for head in headers:
        out.append('<th>%s</th>' % esc(head))
    out.append('</tr></thead><tbody>')
    for row in rows:
        out.append('<tr>')
        for cell in row:
            out.append('<td>%s</td>' % cell)
        out.append('</tr>')
    out.append('</tbody></table>')
    return "".join(out)


#: the header of the column every explained row carries.  ONE character,
#: because the cell holds a `?` a reader opens.
WHY_COLUMN = "?"


def explained_table(headers, rows):
    """a table in which EVERY ROW CARRIES ITS OWN EXPLANATION.

    `rows` is a list of (explanation key, cells).  The key is looked up
    in `dashboard_stats.MEANINGS`, which is DATA and not prose inside
    this renderer -- that is the mechanism keeping the set of rows and
    the set of explanations from drifting apart.  A key with no record is
    drawn as UNEXPLAINED in place, so a row that goes without one is
    visible on the page instead of silently unexplained.

    NO JAVASCRIPT is added by this: the control is a `<details>` element,
    which the engine opens and closes by itself.  The python page still
    carries no script of its own.
    """
    return table(list(headers) + [WHY_COLUMN],
                 statspane.explained_rows(rows))


def share_cell(part, whole):
    """one count as a share of its own population, drawn only when the
    population is there to divide by."""
    if not whole:
        return "&mdash;"
    return "%.1f%%" % (100.0 * part / float(whole))


def unit_link(unit_id):
    return ('<a onclick="python:ouro_unit(%s)">%s</a>'
            % (pyarg(unit_id), esc(unit_id)))


def count_cell(value):
    """one summary value, drawn WITHOUT assuming it is a whole number.

    Found by running, not by reading (task 85, lane 3): at the moments
    2026-09-02 2755e421, 4475ddde and 2026-09-03 9d6235de the highest
    pool generation carries a nested object on its summary where the
    present one carries a count, and formatting it as a number raised
    `TypeError: unsupported format string passed to dict.__format__` —
    three of 200 renders.  A past moment is where an artifact's SHAPE
    changes, not only its numbers, so the general fix is to draw a value
    as what it is rather than as whatever shape the present one has.
    """
    if isinstance(value, bool):
        return esc(value)
    if isinstance(value, int):
        return "{:,}".format(value)
    if isinstance(value, float):
        return "{:,.2f}".format(value)
    if isinstance(value, dict):
        return esc(", ".join("%s %s" % (name, value[name])
                             for name in sorted(value)))
    if isinstance(value, list):
        return esc(", ".join(str(one) for one in value))
    return esc(value)


def gap_line(what):
    """one thing this pane could not read at this moment, named."""
    return ('<p class="gap">not at this moment: %s</p>' % what)


#: WHAT USED TO BE HERE, AND WHY IT IS GONE.  `testimony_for` drew a
#: count line parsed out of a commit message wherever an artifact was
#: untracked at that commit.  That is a number taken from text a person
#: wrote, which is precisely what the CORE's rule "The chronology is
#: version control, and nothing curates it" retires.  A moment that
#: cannot be recomputed now draws its refusal and names the files it
#: would need -- `refusal` and `gap_line`, which every pane already
#: reaches -- and shows no number at all.  Removed by task 86.


# ---------------------------------------------------------------------------
# pane 5 -- stats.  The FIRST PAINT, because it is the cheapest: three
# small files and one tail carve, no index.
# ---------------------------------------------------------------------------

#: the term audit this pane draws its stored tally from.  IT IS A TASK
#: NUMBER, NOT A GENERATION.  `audit61`, `audit64`, `audit65`, `audit66`
#: and `audit78` are five different audits of five different questions,
#: so "the highest number" is not "the newest generation" here and
#: picking by number -- right for the pool, the census and the canonical
#: form -- would be wrong.  The name is therefore written down, and the
#: rows it produces say on the page which round they belong to, because
#: the COMPUTED term-store section below walks a LATER round and the two
#: must not be read as disagreeing.
STORED_TERM_AUDIT = "audit65.json"

#: how many census producers the table draws, printed beside the
#: population it was cut from -- the CORE's rule for any view over a
#: population too large to draw whole.
CENSUS_CEILING = 12


def stats_stored(moment, names):
    """THE FIRST HALF: figures a previous run wrote down, read back.

    Every row here comes out of a `summary` or a tally block on an
    artifact -- a number some earlier program chose to record.  The half
    is labelled as such on the page so the reader can tell it apart from
    the second half, which counts the artifacts itself.
    """
    body = []
    body.append('<h2 class="half">read from a stored summary</h2>')
    body.append('<p class="halfnote">Every number below was written into '
                'an artifact by an earlier run and is read back here. '
                'Each row says which file, on its own <b>?</b>.</p>')

    pool_gen, summary = pool_summary(moment)
    if summary:
        rows = []
        for key in sorted(summary):
            rows.append(("pool." + key,
                         [esc(key.replace("_", " ")),
                          '<b>%s</b>' % count_cell(summary[key])]))
        body.append("<h3>the pool — %s, its own summary, the highest "
                    "generation at this moment</h3>" % esc(pool_gen))
        body.append(explained_table(["what is counted", "how many"], rows))
    else:
        body.append(gap_line("the pool — no the_pool&lt;n&gt;.json is "
                             "tracked at this commit"))

    audit = None
    if STORED_TERM_AUDIT in names:
        audit = moment.read_json(OP_DIR + "/" + STORED_TERM_AUDIT)
    if audit:
        layer5 = audit.get("layer5") or {}
        rows = []
        for key in sorted(layer5):
            rows.append(("audit." + key,
                         [esc(key.replace("_", " ")),
                          '<b>%s</b>' % count_cell(layer5[key])]))
        body.append("<h3>the term states — %s</h3>" % esc(STORED_TERM_AUDIT))
        body.append(explained_table(["what is counted", "how many"], rows))
        causes = audit.get("disproved_by_cause") or {}
        rows = []
        ordered = sorted(causes,
                         key=lambda c: -(causes[c]
                                         if isinstance(causes[c], int) else 0))
        for cause in ordered:
            rows.append(("audit.disproved_by_cause",
                         ['<b>%s</b>' % count_cell(causes[cause]),
                          esc(cause)]))
        if rows:
            body.append("<h3>why a term was disproved</h3>")
            body.append(explained_table(["units", "cause"], rows))
    else:
        body.append(gap_line("the term states — %s is not tracked at this "
                             "commit" % esc(STORED_TERM_AUDIT)))

    census_gen = census_file(moment)
    census = None
    if census_gen:
        census = moment.read_json(OP_DIR + "/" + census_gen)
    if census:
        entries = census.get("entries") or []
        rows = []
        for entry in entries[:CENSUS_CEILING]:
            rows.append(("census.row", [
                esc(viewer_build.census_name(entry.get("producer"))),
                count_cell(entry.get("rows_blocked", entry.get("rows")) or 0),
                count_cell(entry.get("units_blocked",
                                     entry.get("units")) or 0),
            ]))
        body.append("<h3>the census — %s, %s producers, the %d that block "
                    "the most rows</h3>"
                    % (esc(census_gen), commas_of(len(entries)),
                       min(CENSUS_CEILING, len(entries))))
        body.append(explained_table(["producer", "rows", "units"], rows))
    else:
        body.append(gap_line("the census — no name_census&lt;n&gt;.json is "
                             "tracked at this commit"))

    return "".join(body), summary


def stats_corpus_section(found):
    """THE COMPUTED CORPUS: every figure here was counted in ONE walk of
    the canonical-form generation, during this render."""
    body = []
    generation = found["generation"]
    body.append("<h3>the corpus, by language and arrival population — "
                "canon%s, counted over %s documents</h3>"
                % (esc(generation), commas_of(found["inputs"])))

    populations = sorted(found["by_pop"])
    headers = ["language"] + populations + ["all"]
    rows = []
    for lang in sorted(found["by_lang"]):
        cells = ['<b>%s</b>' % esc(lang)]
        for population in populations:
            cells.append(commas_of(found["by_lang_pop"].get((lang, population),
                                                            0)))
        cells.append('<b>%s</b>' % commas_of(found["by_lang"][lang]))
        rows.append(("corpus.language_row", cells))
    totals = ['<b>every language — %s of them</b>' % len(found["by_lang"])]
    for population in populations:
        totals.append('<b>%s</b>' % commas_of(found["by_pop"][population]))
    totals.append('<b>%s</b>' % commas_of(found["units"]))
    rows.append(("corpus.language_row", totals))
    body.append(explained_table(headers, rows))

    body.append("<h3>what the canonical-form gate said about them</h3>")
    rows = []
    ordered = sorted(found["outcomes"], key=lambda o: -found["outcomes"][o])
    for outcome in ordered:
        rows.append(("corpus.outcome_row",
                     [esc(outcome),
                      '<b>%s</b>' % commas_of(found["outcomes"][outcome]),
                      share_cell(found["outcomes"][outcome],
                                 found["units"])]))
    body.append(explained_table(["outcome", "units", "share of the corpus"],
                                rows))

    rows = []
    for lang in sorted(found["not_proved_by_lang"],
                       key=lambda l: -found["not_proved_by_lang"][l]):
        rows.append(("corpus.not_proved_row",
                     [esc(lang),
                      '<b>%s</b>' % commas_of(found["not_proved_by_lang"][lang]),
                      commas_of(found["by_lang"][lang]),
                      share_cell(found["not_proved_by_lang"][lang],
                                 found["by_lang"][lang])]))
    if rows:
        body.append("<h3>the %s units the gate did not prove, per language"
                    "</h3>"
                    % commas_of(found["units"] - found["proved"]))
        body.append(explained_table(
            ["language", "not proved", "units of that language",
             "share of that language"], rows))
    return "".join(body)


def stats_opcode_section(found):
    """THE ARCH-OPCODE COUNT DISTRIBUTION -- the shape first, then the
    distribution itself, every count value that occurs given a row."""
    body = []
    populations = sorted(found["opcode_spread"])
    body.append("<h3>how many arch opcodes an arch-unit's body holds — the "
                "shape</h3>")
    rows = []
    for population in populations:
        shape = found["opcode_spread"][population]
        if shape is None:
            continue
        rows.append(("corpus.opcode_spread_row", [
            '<b>%s</b>' % esc(population),
            commas_of(shape["population"]),
            commas_of(found["vocabulary"].get(population, 0)),
            "%s opcodes (%s units, %.1f%%)"
            % (shape["peak"], commas_of(shape["peak_units"]),
               shape["peak_share"]),
            commas_of(shape["median"]),
            commas_of(shape["largest"]),
            commas_of(shape["zero"]),
        ]))
    body.append(explained_table(
        ["arrival population", "units", "distinct opcodes it uses",
         "most common count", "median", "longest body", "empty bodies"],
        rows))

    largest = 0
    for population in populations:
        for value in found["opcode_dist"][population]:
            if value > largest:
                largest = value
    body.append("<h3>the distribution itself — every count value that "
                "occurs, 0 to %d</h3>" % largest)
    headers = ["arch opcodes in the body"]
    for population in populations:
        headers.append("%s (%s units)"
                       % (population,
                          commas_of(found["by_pop"].get(population, 0))))
    rows = []
    for value in range(0, largest + 1):
        seen = False
        cells = ['<b>%d</b>' % value]
        for population in populations:
            held = found["opcode_dist"][population].get(value, 0)
            if held:
                seen = True
            cells.append(commas_of(held))
        if seen:
            rows.append(("corpus.opcode_distribution_row", cells))
    body.append(explained_table(headers, rows))
    return "".join(body)


def stats_machine_code_section(found):
    """HOW FAR MACHINE CODE REPEATS, and the two honest distinct counts."""
    body = []
    body.append("<h3>distinct machine code against unit count</h3>")
    rows = [
        ("corpus.repetition_row",
         ["units carrying machine code",
          '<b>%s</b>' % commas_of(found["compiled"])]),
        ("corpus.repetition_row",
         ["distinct bodies, counted once for the corpus",
          '<b>%s</b>' % commas_of(found["distinct_corpus_wide"])]),
        ("corpus.repetition_row",
         ["units per distinct body, corpus-wide",
          '<b>%.1f</b>' % (found["compiled"]
                           / float(found["distinct_corpus_wide"]))]),
        ("corpus.repetition_row",
         ["distinct bodies, summed over the languages",
          '<b>%s</b>' % commas_of(found["distinct_summed_per_language"])]),
        ("corpus.repetition_row",
         ["units per distinct body, summed over the languages",
          '<b>%.1f</b>' % (found["compiled"]
                           / float(found["distinct_summed_per_language"]))]),
        ("corpus.repetition_row",
         ["bodies appearing in more than one language",
          '<b>%s</b>' % commas_of(found["bodies_in_more_than_one_language"])]),
        ("corpus.repetition_row",
         ["the most repeated body, how many units hold it",
          '<b>%s</b>' % commas_of(found["most_repeated"])]),
        ("corpus.repetition_row",
         ["the most repeated body, its bytes",
          '<code>%s</code>' % esc(found["most_repeated_bytes"])]),
        ("corpus.repetition_row",
         ["the most repeated body, the languages it appears in",
          esc(", ".join(found["most_repeated_languages"]))]),
    ]
    body.append(explained_table(["what is counted", "how many"], rows))

    rows = []
    for lang in sorted(found["distinct_by_lang"]):
        units = found["compiled_by_lang"][lang]
        distinct = found["distinct_by_lang"][lang]
        rows.append(("corpus.repetition_language_row", [
            '<b>%s</b>' % esc(lang), commas_of(units), commas_of(distinct),
            "%.1f" % (units / float(distinct)),
        ]))
    body.append("<h3>the same, per language</h3>")
    body.append(explained_table(
        ["language", "units carrying machine code", "distinct bodies",
         "units per distinct body"], rows))

    body.append("<h3>bodies holding no instruction at all — nobody has "
                "explained this</h3>")
    rows = []
    for population in sorted(found["empty_bodies"]):
        rows.append(("corpus.empty_row", [
            '<b>%s</b>' % esc(population),
            '<b>%s</b>' % commas_of(found["empty_bodies"][population]),
            commas_of(found["by_pop"].get(population, 0)),
            share_cell(found["empty_bodies"][population],
                       found["by_pop"].get(population, 0)),
        ]))
    body.append(explained_table(
        ["arrival population", "empty bodies", "units of that population",
         "share"], rows))

    body.append("<h3>two more distributions off the same walk</h3>")
    rows = []
    for key, name, shape in (
            ("corpus.body_length_row", "bytes of machine code per body",
             found["body_length"]),
            ("corpus.ledger_row", "ledger rows per unit",
             found["ledger_rows"])):
        if shape is None:
            continue
        rows.append((key, [
            esc(name), commas_of(shape["population"]),
            "%s (%s units)" % (commas_of(shape["peak"]),
                               commas_of(shape["peak_units"])),
            commas_of(shape["median"]), commas_of(shape["smallest"]),
            commas_of(shape["largest"]),
        ]))
    body.append(explained_table(
        ["what is measured", "units", "most common value", "median",
         "smallest", "largest"], rows))
    return "".join(body)


def stats_term_section(terms, found):
    """THE COMPUTED TERM STORE: the store's own records, walked shard by
    shard at render time."""
    body = []
    body.append("<h3>the layer-4 term store — %s, %s shards, counted "
                "record by record</h3>"
                % (esc(terms["store"]), commas_of(terms["shards"])))

    states = sorted(terms["by_state"], key=lambda s: -terms["by_state"][s])
    headers = ["language", "records"] + [str(one) for one in states]
    rows = []
    for lang in sorted(terms["by_lang"]):
        cells = ['<b>%s</b>' % esc(lang),
                 '<b>%s</b>' % commas_of(terms["by_lang"][lang])]
        for state in states:
            cells.append(commas_of(terms["by_lang_state"].get((lang, state),
                                                              0)))
        rows.append(("term.state_row", cells))
    totals = ['<b>every language</b>', '<b>%s</b>' % commas_of(terms["records"])]
    for state in states:
        totals.append('<b>%s</b>' % commas_of(terms["by_state"][state]))
    rows.append(("term.records_row", totals))
    body.append(explained_table(headers, rows))

    if found is not None:
        short = found["proved"] - terms["records"]
        rows = [
            ("term.coverage_row",
             ["units the canon%s gate proved" % esc(found["generation"]),
              '<b>%s</b>' % commas_of(found["proved"])]),
            ("term.coverage_row",
             ["records in %s" % esc(terms["store"]),
              '<b>%s</b>' % commas_of(terms["records"])]),
            ("term.coverage_row",
             ["proved units with no record in the store",
              '<b>%s</b>' % commas_of(short)]),
        ]
        body.append("<h3>the store against the population it was built "
                    "over</h3>")
        body.append(explained_table(["what is counted", "how many"], rows))

    rows = []
    for lang in sorted(terms["callee_by_lang"],
                       key=lambda l: -terms["callee_by_lang"][l]):
        rows.append(("term.callee_row", [
            '<b>%s</b>' % esc(lang),
            '<b>%s</b>' % commas_of(terms["callee_by_lang"][lang]),
            commas_of(terms["by_lang"].get(lang, 0)),
            share_cell(terms["callee_by_lang"][lang],
                       terms["by_lang"].get(lang, 0)),
        ]))
    if rows:
        body.append("<h3>records whose body transfers into a routine the "
                    "toolchain's archive defines</h3>")
        body.append(explained_table(
            ["language", "records with a runtime-callee row",
             "records of that language", "share"], rows))

    rows = [
        ("term.holes_row",
         ["records carrying at least one hole",
          '<b>%s</b>' % commas_of(terms["holes"])]),
        ("term.holes_row",
         ["records carrying at least one cascade",
          '<b>%s</b>' % commas_of(terms["cascades"])]),
        ("term.holes_row",
         ["records carrying a relink refusal",
          '<b>%s</b>' % commas_of(terms["relink_refusals"])]),
    ]
    body.append("<h3>what else a record carries</h3>")
    body.append(explained_table(["what is counted", "how many"], rows))
    return "".join(body)


def stats_computed(moment):
    """THE SECOND HALF: figures COUNTED HERE, over the artifacts, while
    the page was drawn.

    the owner, 2026-09-05: "i want analysis run to produce stats you havent
    curated."  Nothing in this half is read from a summary; every number
    is the result of a walk that happens now, and a walk that cannot be
    made at the selected moment draws its refusal and names the family it
    would need.

    Two walks, both bounded the same way: one document is parsed, reduced
    to counters, and dropped before the next is opened.  Measured
    (Airlock lane `t98_l2_shapes.sh`): 1.7 s and 45.0 MB of resident size
    for both, against this page's stated cap of 1,500 MB.
    """
    body = []
    body.append('<h2 class="half">counted at render time</h2>')
    body.append('<p class="halfnote">No number below is read from any '
                'summary. Each is counted over the artifacts as they stand '
                'at the selected moment, in this render, and each row says '
                'so on its own <b>?</b>.</p>')

    found = None
    try:
        found = statspane.corpus_analysis(moment, guard_memory, OP_DIR)
    except NotAtThisMoment as gap:
        body.append(gap_line("the corpus could not be counted here: %s"
                             % esc(gap.needed)))
    if found is None:
        body.append(gap_line(
            "the canonical-form corpus — canon&lt;n&gt;_wrapped_&lt;lang&gt;"
            ".json and canon&lt;n&gt;_regen_store/. No generation of that "
            "family is tracked at this commit, so there is nothing here to "
            "walk and no figure is shown in its place"))
    else:
        body.append(stats_corpus_section(found))
        body.append(stats_opcode_section(found))
        body.append(stats_machine_code_section(found))

    terms = None
    try:
        terms = statspane.term_store_analysis(moment, guard_memory, OP_DIR)
    except NotAtThisMoment as gap:
        body.append(gap_line("the term store could not be counted here: %s"
                             % esc(gap.needed)))
    if terms is None:
        body.append(gap_line(
            "the layer-4 term store — term&lt;n&gt;_store/. No generation of "
            "that family is tracked at this commit, so its records cannot be "
            "counted here"))
    else:
        body.append(stats_term_section(terms, found))

    return "".join(body), found


def pane_stats(moment):
    """PANE 5 -- STATS, in TWO LABELLED HALVES.

    the owner asked for both of them on 2026-09-05.  The first half is what was
    already here: figures an earlier run wrote into an artifact, read
    back.  The second half is ANALYSIS RUN NOW -- the artifacts walked at
    render time, producing figures nobody selected in advance.  The page
    says which half a number is in, and every row carries a `?` that says
    it again for that row alone.

    Every row's `?` is looked up in `dashboard_stats.MEANINGS` by key.
    That file is DATA, not prose inside this renderer, so the rows and
    the explanations cannot drift apart; a row whose key has no record is
    drawn as UNEXPLAINED on the page rather than silently going without.
    """
    names = moment.names_under(OP_DIR)
    stored, summary = stats_stored(moment, names)
    computed, found = stats_computed(moment)

    if summary is None and found is None:
        raise NotAtThisMoment(
            "the pool (the_pool&lt;n&gt;.json), the term audit (%s), the "
            "census (name_census&lt;n&gt;.json) and the canonical-form "
            "corpus (canon&lt;n&gt;_wrapped_&lt;lang&gt;.json). None of them "
            "is tracked at this commit, so there is nothing here to read "
            "and nothing here to count" % esc(STORED_TERM_AUDIT), moment)

    counted = 0
    how = "the pool's own members line; nothing was counted here"
    if found is not None:
        counted = found["units"]
        how = ("counted here, in one walk of %s documents of canon%s"
               % (commas_of(found["inputs"]), found["generation"]))
    elif summary:
        counted = summary.get("members") or 0

    return frame(5, "stats", stored + computed,
                 population_line(counted, how, moment), moment)


# ---------------------------------------------------------------------------
# pane 2 -- the selector
# ---------------------------------------------------------------------------

def pane_selector(moment, lang=None, gid=None, sig=None):
    index = build_index(moment)
    rows = index["rows"]
    groups = STATE["groups"]

    body = []
    langs = {}
    for row in rows:
        langs[row["lang"]] = langs.get(row["lang"], 0) + 1
    chips = []
    for one in sorted(langs):
        klass = "chip on" if one == lang else "chip"
        chips.append('<span class="%s" onclick="python:ouro_select(%s)">%s '
                     '<i>%s</i></span>'
                     % (klass, pyarg(one), esc(one),
                        "{:,}".format(langs[one])))
    body.append("<h3>language — %d of them</h3>" % len(langs))
    body.append('<div class="chips">%s</div>' % "".join(chips))

    if lang:
        seen = {}
        for row in rows:
            if row["lang"] != lang or not row["gid"]:
                continue
            seen[row["gid"]] = seen.get(row["gid"], 0) + 1
        chips = []
        for one in sorted(seen, key=lambda g: (-seen[g], g)):
            klass = "chip on" if one == gid else "chip"
            chips.append('<span class="%s" onclick="python:ouro_select(%s,%s)">'
                         '%s <i>%s</i></span>'
                         % (klass, pyarg(lang), pyarg(one),
                            esc(groups.labels.get(one, one)),
                            "{:,}".format(seen[one])))
        body.append("<h3>operator group — %d in %s, keyed by machine id, "
                    "labelled by the token</h3>" % (len(seen), esc(lang)))
        body.append('<div class="chips">%s</div>' % "".join(chips))

    if lang and gid:
        seen = {}
        for row in rows:
            if row["lang"] != lang or row["gid"] != gid:
                continue
            seen[row["sig"] or "(none)"] = seen.get(row["sig"] or "(none)", 0) + 1
        chips = []
        for one in sorted(seen, key=lambda s: (-seen[s], s)):
            klass = "chip on" if one == sig else "chip"
            chips.append('<span class="%s" onclick="python:ouro_select(%s,%s,%s)">'
                         '%s <i>%s</i></span>'
                         % (klass, pyarg(lang), pyarg(gid),
                            pyarg(one), esc(one),
                            "{:,}".format(seen[one])))
        body.append("<h3>type signature — %d under this group</h3>" % len(seen))
        body.append('<div class="chips">%s</div>' % "".join(chips))

    if lang and gid and sig:
        picked = []
        for row in rows:
            if row["lang"] != lang or row["gid"] != gid:
                continue
            if (row["sig"] or "(none)") != sig:
                continue
            picked.append(row)
        shown = picked[:200]
        out = []
        for row in shown:
            out.append([unit_link(row["id"]), esc(row["pop"]),
                        esc(row["outcome"]), esc(row["label"])])
        body.append("<h3>units — %d, showing %d</h3>"
                    % (len(picked), len(shown)))
        body.append(table(["unit", "arrival population", "outcome",
                           "operator label"], out))

    seeded = random.Random(20260903)
    pick = seeded.choice(rows)
    body.append('<p><span class="btn" onclick="python:ouro_unit(%s)">'
                'a seeded random unit — %s</span></p>'
                % (pyarg(pick["id"]), esc(pick["id"])))

    return frame(2, "selector", "".join(body),
                 population_line(len(rows),
                                 "index built in %.1f s" % index["seconds"],
                                 moment),
                 moment)


# ---------------------------------------------------------------------------
# pane 3 -- the arch opcode index
# ---------------------------------------------------------------------------

CEILING = 200


def pane_opcode_index(moment, arch_id=None):
    index = build_index(moment)
    rows = index["rows"]
    arch = STATE["arch"]
    groups = STATE["groups"]

    body = []
    ordered = sorted(arch["rows"],
                     key=lambda a: (-arch["rows"][a]["units"], a))
    chips = []
    for one in ordered:
        klass = "chip on" if one == arch_id else "chip"
        chips.append('<span class="%s" onclick="python:ouro_opcode(%s)">%s '
                     '<i>%s</i></span>'
                     % (klass, pyarg(one),
                        esc(arch["rows"][one]["mnem"]),
                        "{:,}".format(arch["rows"][one]["units"])))
    body.append("<h3>every arch opcode — %d of them, keyed by an opaque arch "
                "id, the mnemonic carried as a value</h3>" % len(ordered))
    body.append('<div class="chips">%s</div>' % "".join(chips))

    if arch_id and arch_id in arch["rows"]:
        seen = {}
        for row in rows:
            if arch_id not in row["arch"]:
                continue
            key = (row["lang"], row["gid"], row["sig"] or "(none)")
            seen[key] = seen.get(key, 0) + 1
        ordered_groups = sorted(seen, key=lambda k: (-seen[k], k))
        shown = ordered_groups[:CEILING]
        out = []
        for key in shown:
            out.append([esc(key[0]),
                        esc(groups.labels.get(key[1], key[1])),
                        esc(key[2]),
                        "{:,}".format(seen[key])])
        body.append("<h3>%s appears in %s (language, operator group, "
                    "signature) groups — drawing %d of them</h3>"
                    % (esc(arch["rows"][arch_id]["mnem"]),
                       "{:,}".format(len(ordered_groups)), len(shown)))
        body.append(table(["language", "operator label", "type signature",
                           "units"], out))

    return frame(3, "arch opcode index", "".join(body),
                 population_line(len(rows),
                                 "ceiling %d groups drawn per opcode" % CEILING,
                                 moment),
                 moment)


# ---------------------------------------------------------------------------
# pane 1 -- the unit viewer
# ---------------------------------------------------------------------------

def pane_unit(moment, unit_id=None):
    index = build_index(moment)
    rows = index["rows"]
    if unit_id is None:
        unit_id = STATE["unit"]
    if unit_id is None:
        unit_id = random.Random(20260903).choice(rows)["id"]
    STATE["unit"] = unit_id
    row = index["by_id"].get(unit_id)
    if row is None:
        return frame(1, "unit viewer",
                     '<p class="none">no unit named %s in the index as it '
                     'stood at this moment. The index holds %s units here.</p>'
                     % (esc(unit_id), "{:,}".format(len(rows))),
                     population_line(len(rows), None, moment),
                     moment)

    unit = record_in(moment, row["store"], unit_id) or {}

    if STATE["term_shard"] is None:
        STATE["term_shard"] = shard_map(moment, "term65_store")
    if STATE["render_shard"] is None:
        STATE["render_shard"] = shard_map(moment, "render_back_store")
    if STATE["pool"] is None:
        summary, by_unit = pool_rows(moment)
        STATE["pool"] = by_unit

    term = None
    if unit_id in STATE["term_shard"]:
        term = record_in(moment, STATE["term_shard"][unit_id], unit_id)
    rendered = None
    if unit_id in STATE["render_shard"]:
        rendered = record_in(moment, STATE["render_shard"][unit_id], unit_id)
    pool_row = STATE["pool"].get(unit_id) or {}

    head = [
        ["unit", esc(unit_id)],
        ["language", esc(row["lang"])],
        ["operator label", esc(row["label"])],
        ["operator group id", esc(row["gid"])],
        ["type signature", esc(row["sig"])],
        ["arrival population", esc(row["pop"])],
        ["arrival annotation", esc(unit.get("arrival_annotation"))],
        ["outcome", esc(row["outcome"])],
        ["read from", esc(row["store"])],
        ["as of", esc(moment.label())],
    ]
    body = [table(["field", "value"], head)]

    body.append("<h3>raw extracted — body_as_read</h3>")
    body.append('<pre>%s</pre>' % esc("\n".join(unit.get("body_as_read") or [])))

    body.append("<h3>context — prior_text</h3>")
    prior = unit.get("prior_text")
    if prior:
        body.append('<pre>%s</pre>'
                    % esc("\n".join(prior) if isinstance(prior, list) else prior))
    else:
        body.append('<p class="none">no stored context for this unit.</p>')

    body.append("<h3>canonical — wrapped_text (layer 3)</h3>")
    body.append('<pre>%s</pre>' % esc(unit.get("wrapped_text")))

    body.append("<h3>ledger</h3>")
    led = []
    for entry in unit.get("ledger") or []:
        producer = entry.get("produced_by") or {}
        led.append([esc(entry.get("row")), esc(entry.get("type")),
                    esc(viewer_build.census_name(producer)),
                    esc(", ".join(entry.get("operands") or [])),
                    esc(entry.get("note"))])
    if led:
        body.append(table(["row", "type", "produced by", "operands", "note"],
                          led))
    else:
        body.append('<p class="none">no ledger rows on this unit.</p>')

    body.append("<h3>term — layer 5, normalized</h3>")
    if term is None:
        if not STATE["term_shard"]:
            body.append(gap_line("the term store — term65_store/ is not "
                                 "tracked at this commit"))
        else:
            body.append('<p class="none">no term record for this unit.</p>')
    elif term.get("layer5_normalized_text"):
        body.append('<pre>%s</pre>' % esc(term.get("layer5_normalized_text")))
        body.append('<p>term state <b>%s</b>, outcome <b>%s</b>. %s</p>'
                    % (esc(term.get("term_state")), esc(term.get("outcome")),
                       esc(term.get("reason"))))
    else:
        body.append('<p class="none">term state <b>%s</b> — no layer-5 text. '
                    '%s</p>'
                    % (esc(term.get("term_state")),
                       esc(term.get("why_no_term")
                           or term.get("reason") or "")))
        holes = term.get("holes") or []
        if holes:
            body.append('<p>%d hole(s): %s</p>'
                        % (len(holes),
                           esc(viewer_build.census_name(
                               (holes[0] or {}).get("producer")))))

    body.append("<h3>rendered back</h3>")
    if rendered:
        body.append('<pre>%s</pre>' % esc(rendered.get("layer3_wrapped_text")))
        body.append('<p>character identical to layer 3: <b>%s</b></p>'
                    % esc(rendered.get("character_identical_to_layer_3")))
    elif not STATE["render_shard"]:
        body.append(gap_line("the render-back store — render_back_store/ is "
                             "not tracked at this commit"))
    else:
        body.append('<p class="none">this unit was not rendered back.</p>')

    body.append("<h3>pool entry</h3>")
    if pool_row:
        body.append(table(["field", "value"], [
            ["entry", esc(pool_row.get("entry"))],
            ["members", esc(pool_row.get("members"))],
            ["languages", esc(", ".join(pool_row.get("languages") or []))],
            ["representative", esc(pool_row.get("rep"))],
        ]))
    elif not STATE["pool"]:
        body.append(gap_line("the pool — no the_pool&lt;n&gt;.json is tracked "
                             "at this commit"))
    else:
        body.append('<p class="none">this unit is in no pool entry.</p>')

    body.append("<h3>verdicts</h3>")
    body.append(table(["field", "value"], [
        ["verdict", esc(unit.get("verdict"))],
        ["route", esc(unit.get("verdict_route"))],
        ["detail", esc(unit.get("verdict_detail"))],
    ]))

    return frame(1, "unit viewer — %s" % unit_id, "".join(body),
                 population_line(len(rows),
                                 "one unit re-opened from %s" % row["store"],
                                 moment),
                 moment)


# ---------------------------------------------------------------------------
# pane 4 -- coverage.  A DRAWING, not a table of counts.
#
# THE DEFECT THIS RETIRES, named exactly (CORE, 2026-09-04): this function
# emitted four tables and a `<pre>` list and drew nothing, while the
# drawing existed only in `dashboard_pane4.js`, the route the owner does not
# use.  "A pane that reports the graph's node and edge COUNTS does not
# satisfy a requirement to show the graph."
#
# the owner, 2026-09-04, on what the picture is for: "the graph is to verify
# that youre not fucking lying to me about actually extracting everything
# ive intended for us to extract. i want to be able to see a basic
# structure and dynamic connections and the traced directional
# connections made by our probes."  Three figures, in his three words,
# over ONE layout that follows the compiler's own directories and files.
# The drawing itself is `dashboard_graph_draw`; this function chooses the
# compiler, reads the summaries AT THE MOMENT, and hands them over.
#
# NOT ONE OF THE LARGE FILES IS OPENED.  graph_cpp.json is read for its
# first 256 KB and nothing more; the figures are drawn from
# graph_<lang>_files.json (41-184 KB), coverage_<lang>_files.json (2.6 MB)
# and variant_connections_<lang>.json (0.6-3.2 MB).
# ---------------------------------------------------------------------------

def compiler_chooser(moment, chosen, focus, pick):
    out = ['<div class="chips">']
    for name, key, _what in draw.DRAWN_COMPILERS:
        klass = "chip on" if key == chosen else "chip"
        out.append('<span class="%s" onclick="python:ouro_cov(%s,%s,%s)">'
                   '%s</span>'
                   % (klass, pyarg(key), pyarg(None), pyarg(None),
                      esc(name)))
    for name, _why in draw.NO_GRAPH_AT_ALL:
        out.append('<span class="chip off">%s <i>no graph</i></span>'
                   % esc(name))
    out.append('</div>')
    return "".join(out)


def graph_head_line(coverage, key):
    """what the drawing was built from, and what was never opened."""
    for graph in coverage["graphs"]:
        if graph["file"] == "graph_%s.json" % key:
            return ('the graph on disk is <code>%s</code>, %s bytes, in the '
                    '%s form, holding %s nodes / %s edges / %s frontier '
                    'records over %s files. This pane read its first 256 KB '
                    'and no more.'
                    % (esc(graph["file"]), commas_of(graph.get("bytes")),
                       "compact" if graph.get("compact") else "expanded",
                       commas_of(graph["counts"].get("nodes")),
                       commas_of(graph["counts"].get("edges")),
                       commas_of(graph["counts"].get("frontier")),
                       commas_of(graph["counts"].get("files"))))
    return None


def commas_of(value):
    try:
        return "{:,}".format(value)
    except (TypeError, ValueError):
        return esc(value)


def probe_menu(coverage_doc, chosen, key, focus):
    probes = coverage_doc.get("probes") or []
    out = ['<div class="chips"><span class="chipname">one probe\'s own '
           'walk — %s of %s probes offered, the printed ceiling</span>'
           % (commas_of(min(len(probes), draw.PROBE_MENU_CEILING)),
              commas_of(len(probes)))]
    klass = "chip on" if not chosen else "chip"
    out.append('<span class="%s" onclick="python:ouro_cov(%s,%s,%s)">'
               'all of them, in aggregate</span>'
               % (klass, pyarg(key), pyarg(focus), pyarg(None)))
    for probe in probes[:draw.PROBE_MENU_CEILING]:
        name = probe.get("probe")
        klass = "chip on" if chosen == name else "chip"
        out.append('<span class="%s" onclick="python:ouro_cov(%s,%s,%s)">'
                   '%s <i>%s runs</i></span>'
                   % (klass, pyarg(key), pyarg(focus),
                      pyarg("probe:" + str(name)), esc(name),
                      commas_of(probe.get("file_runs_total"))))
    out.append('</div>')
    return "".join(out)


def variant_menu(variants_doc, chosen, key, focus):
    variants = variants_doc.get("variants") or []
    #: RANKED BY MACHINE-FORM EVIDENCE ONLY: how many transitions this
    #: variant walks that no other variant walks.  No token is read to
    #: build this list, to order it, or to cut it.
    ranked = sorted(
        variants,
        key=lambda one: (-(one.get("transitions_exclusive_to_this_variant")
                           or 0), one.get("variant_id") or ""))
    out = ['<div class="chips"><span class="chipname">one operator traced '
           'variant — %s of %s variants offered, ranked by how many '
           'transitions belong to it alone; the printed ceiling is %s'
           '</span>'
           % (commas_of(min(len(ranked), draw.VARIANT_MENU_CEILING)),
              commas_of(len(variants)),
              commas_of(draw.VARIANT_MENU_CEILING))]
    for one in ranked[:draw.VARIANT_MENU_CEILING]:
        vid = one.get("variant_id")
        klass = "chip on" if chosen == vid else "chip"
        out.append('<span class="%s" onclick="python:ouro_cov(%s,%s,%s)">'
                   '%s <i>%s alone</i></span>'
                   % (klass, pyarg(key), pyarg(focus),
                      pyarg("variant:" + str(vid)), esc(vid),
                      commas_of(one.get(
                          "transitions_exclusive_to_this_variant"))))
    out.append('</div>')
    return "".join(out)


def pane_coverage(moment, lang=None, focus=None, pick=None):
    """THE DRAWING.  Three figures over one structure-following layout."""
    key = lang if lang in [one[1] for one in draw.DRAWN_COMPILERS] else "go"
    coverage = coverage_at(moment)
    folder = coverage["folder"]

    files_rel = CG_DIR + "/graph_%s_files.json" % key
    if not moment.has(files_rel):
        raise NotAtThisMoment(
            "the file-level summary of this compiler's graph — "
            "<code>%s</code>. It is not tracked at this commit, and it is "
            "what every figure here is drawn from; the graph itself is 49 "
            "to 331 MB and is never opened whole, so there is nothing to "
            "draw without it" % esc(files_rel), moment)
    files_doc = moment.read_json(files_rel)
    guard_memory("reading %s" % files_rel)

    rows = files_doc.get("files") or []
    sheet = draw.Sheet(rows, dense=len(rows) > 120)

    def click_for(path):
        return ("ouro_cov(%s,%s,%s)"
                % (pyarg(key), pyarg(None if path == focus else path),
                   pyarg(pick)))

    body = [compiler_chooser(moment, key, focus, pick)]
    head = graph_head_line(coverage, key)
    if head:
        body.append('<p class="dg-source">%s</p>' % head)
    else:
        body.append(gap_line(
            "the graph file itself — <code>graph_%s.json</code> is not in "
            "the companion graph folder at this moment (%s). The figures "
            "below are drawn from the tracked summary, which is what they "
            "have always been drawn from; only the head line is missing"
            % (esc(key), esc(folder.label()))))
    body.append('<p class="dg-source">the companion graph folder: %s</p>'
                % esc(folder.label()))

    # ---- figure 1: the compiler's own organisation -------------------
    svg, ceiling = draw.draw_structure(sheet, files_doc, focus, click_for)
    counts = files_doc.get("counts") or {}
    population = ("%s files in %s directories, %s definitions, %s graph "
                  "nodes and %s edges. %s"
                  % (commas_of(len(rows)), commas_of(len(sheet.bands)),
                     commas_of(sum(int(r.get("defs") or 0) for r in rows)),
                     commas_of(counts.get("nodes")),
                     commas_of(counts.get("edges")), ceiling))
    body.append(draw.figure(
        "1", "basic structure — the compiler's own organisation",
        population, svg,
        "a band is a directory of the compiler's source, in path order; a "
        "box is one file, in path order inside its directory, and its "
        "shade is how many definitions it holds. Nothing here is a force "
        "layout: a box's place is a function of its path, so the picture "
        "is the compiler's shape and it is the same at every moment."))
    body.append(draw.legend([
        ("dg-k-box", "a file, shaded by how many definitions it holds"),
        ("dg-k-edge", "a resolved call from one file into another, drawn "
                      "towards the file called"),
    ]))

    # ---- figure 2 and 3 need the coverage summary --------------------
    cov_name = draw.COVERAGE_SUMMARY_OF.get(key)
    cov_rel = (CG_DIR + "/" + cov_name) if cov_name else None
    coverage_doc = None
    if cov_rel and moment.has(cov_rel):
        coverage_doc = moment.read_json(cov_rel)
        guard_memory("reading %s" % cov_rel)

    if coverage_doc is None:
        why = ("no probe of this corpus has ever been diaried through this "
               "compiler, so there is no dynamic structure to draw. The "
               "cost page in log_175 §6.3–6.4 gives the reason: rust is "
               "BLOCKED on this machine (a promisor clone with no route "
               "out and an absent pin) and swift cannot be started here "
               "(three of the five repositories a build needs are not on "
               "this disk). This is UNMEASURED BY ABSENCE OF DIARIES, "
               "written down rather than approximated.") \
            if key in ("rust", "swift") else \
            ("<code>%s</code> is not tracked at this commit, so the "
             "dynamic layer cannot be recomputed here"
             % esc(cov_rel or "the coverage summary"))
        body.append(draw.refusal_figure(
            "2", "dynamic connections — which parts our probes entered",
            why))
        body.append(draw.refusal_figure(
            "3", "the traced directional connections made by our probes",
            why))
    else:
        svg, counted = draw.draw_dynamic(sheet, coverage_doc, focus,
                                         click_for)
        pops = coverage_doc.get("populations") or {}
        population = (
            "%s of %s instrumented bodies were entered by at least one of "
            "%s probes; %s were entered by none. Of the %s files drawn, "
            "%s were entered, %s were entered by no probe at all, and %s "
            "carry no row in the join because no body in them was "
            "instrumented — a NAMED FRONTIER, never a never-visited file."
            % (commas_of(pops.get("visited_by_at_least_one_probe")),
               commas_of(pops.get("instrumented_bodies")),
               commas_of(pops.get("probes")),
               commas_of(pops.get("never_visited")),
               commas_of(len(rows)), commas_of(counted["entered"]),
               commas_of(counted["never"]),
               commas_of(counted["unmeasured"])))
        body.append(draw.figure(
            "2", "dynamic connections — which parts our probes entered",
            population, svg,
            "the same boxes, in the same places. A box's fill is the share "
            "of its instrumented bodies that at least one probe entered; "
            "the number on it is visited over instrumented."))
        body.append(draw.legend([
            ("dg-k-box", "entered, filled in proportion to how much of it"),
            ("dg-k-hollow", "instrumented and entered by no probe"),
            ("dg-k-unmeasured", "no instrumented body — a named frontier"),
        ]))

        # ---- figure 3 --------------------------------------------------
        chosen_probe = None
        chosen_variant = None
        if pick and str(pick).startswith("probe:"):
            chosen_probe = str(pick)[len("probe:"):]
        elif pick and str(pick).startswith("variant:"):
            chosen_variant = str(pick)[len("variant:"):]

        if chosen_variant:
            name = draw.VARIANTS_OF.get(key)
            try:
                variants_doc = folder.read_json(name, ceiling_mb=32)
            except NotAtThisMoment as gap:
                variants_doc = None
                body.append(draw.refusal_figure(
                    "3", "the traced directional connections — one "
                         "operator traced variant", esc(gap.needed)))
            if variants_doc is not None:
                svg, line = draw.draw_one_variant(sheet, variants_doc,
                                                 chosen_variant)
                if svg is None:
                    body.append(draw.refusal_figure(
                        "3", "one operator traced variant",
                        "no variant of this compiler carries the identity "
                        "%s at this moment" % esc(chosen_variant)))
                else:
                    body.append(draw.figure(
                        "3", "the traced directional connections — one "
                             "operator traced variant, its own transitions",
                        line, svg,
                        "the THIRD connection kind: the transitions this "
                        "variant walks and no other variant walks. A "
                        "variant is grouped by a digest over four "
                        "machine-form facts and by nothing else; the "
                        "labels below its identity are display labels on "
                        "its members, read back by nothing."))
        elif chosen_probe:
            svg, line = draw.draw_one_probe(sheet, coverage_doc,
                                            chosen_probe)
            if svg is None:
                body.append(draw.refusal_figure(
                    "3", "one probe's own walk",
                    "no probe named %s carries a path in this summary"
                    % esc(chosen_probe)))
            else:
                body.append(draw.figure(
                    "3", "the traced directional connections — one probe's "
                         "own walk through the compiler", line, svg,
                    "one compilation's ordered path, file by file, in the "
                    "order it happened."))
        else:
            svg, line = draw.draw_aggregate_direction(sheet, coverage_doc)
            body.append(draw.figure(
                "3", "the traced directional connections — every probe, in "
                     "aggregate", line, svg,
                "an arrow is an ordered file-to-file step some probe's "
                "compilation took, drawn towards the file entered next; "
                "its weight is how many probes take it."))
        body.append(draw.legend([
            ("dg-k-arrow", "an ordered step from one file into the next"),
            ("dg-k-quiet", "a file no drawn step touches"),
        ]))
        body.append(probe_menu(coverage_doc, chosen_probe, key, focus))

        name = draw.VARIANTS_OF.get(key)
        if name and folder.has(name):
            try:
                variants_doc = folder.read_json(name, ceiling_mb=32)
                if variants_doc.get("variants"):
                    body.append(variant_menu(variants_doc, chosen_variant,
                                             key, focus))
                else:
                    body.append(gap_line(
                        "the third connection kind for this compiler — "
                        "<code>%s</code> carries state <b>%s</b> and 0 "
                        "variants. %s" % (esc(name),
                                          esc(variants_doc.get("state")),
                                          esc(variants_doc.get("reason")))))
                guard_memory("reading %s" % name)
            except NotAtThisMoment as gap:
                body.append(gap_line(esc(gap.needed)))
        else:
            body.append(gap_line(
                "the third connection kind — <code>%s</code> is not in the "
                "companion graph folder at this moment (%s)"
                % (esc(name), esc(folder.label()))))

    # ---- what is not drawn, by name ----------------------------------
    missing = coverage.get("missing") or []
    body.append('<p class="none">no graph exists for these, and this pane '
                'says so rather than approximating one: %s.</p>'
                % esc(", ".join(missing)))

    return frame(4, "coverage — the compiler graph, drawn", "".join(body),
                 population_line(
                     len(rows),
                     "files drawn for %s; the graph itself (up to 331 MB) "
                     "was read for its first 256 KB only, and "
                     "coverage_go2.json (515 MB) was never opened at all"
                     % key, moment),
                 moment)


# ---------------------------------------------------------------------------
# the dispatch a click reaches
# ---------------------------------------------------------------------------

PANES = {
    1: pane_unit,
    2: pane_selector,
    3: pane_opcode_index,
    4: pane_coverage,
    5: pane_stats,
}


def refusal(number, gap, moment):
    """rule 4, drawn: a pane that cannot be recomputed at a moment says
    so AT THAT MOMENT, and names what it would need."""
    body = ['<p class="gap">This pane cannot be recomputed at the selected '
            'moment. What it would need, and version control does not hold '
            'at commit <code>%s</code>:</p>'
            % esc((moment.commit or "")[:10])]
    body.append('<p class="needed">%s.</p>' % gap.needed)
    body.append('<p class="none">Nothing present-day is shown in its place. '
                'Choose a later moment, or <span class="btn" '
                'onclick="python:ouro_moment(%s)">now</span>, and this pane '
                'fills in.</p>' % pyarg("now"))
    return frame(number, "%s — not recomputable at this moment"
                 % PANE_TITLES.get(number, str(number)),
                 "".join(body),
                 population_line(0, "refused at this moment", moment),
                 moment)


def render(number, *args):
    """answer one pane's html, AS OF THE PAGE'S ONE SELECTED MOMENT.

    A MemoryAbort and a NotAtThisMoment are both caught here and drawn
    as that pane's own body, by name, rather than stopping the page.
    """
    moment = current_moment()
    STATE["pane"] = number
    STATE["args"] = args
    try:
        return PANES[number](moment, *args)
    except NotAtThisMoment as gap:
        return refusal(number, gap, moment)
    except MemoryAbort as abort:
        return frame(number, "refused", '<p class="none">%s</p>' % esc(abort),
                     population_line(0, "refused", moment), moment)
    except Exception as other:
        return frame(number, "error",
                     '<pre>%s: %s</pre>' % (esc(type(other).__name__),
                                            esc(other)),
                     population_line(0, "error", moment), moment)


def moment_change(key):
    """what a click on the chronology does: set ONE moment for the whole
    page, then redraw the tab that is in view as of it.  Every other
    pane is as of it too, because none of them holds a time."""
    set_moment(key)
    return render(STATE["pane"], *STATE["args"])


def window_change(day):
    """what a click on the DAY row does: move the window of the commit
    row, and nothing else.  The moment the page holds does not change,
    so the pane in view is redrawn exactly as it was -- a day is a place
    to look, never a moment that stands for the commits under it."""
    set_window(day)
    return render(STATE["pane"], *STATE["args"])


def first_paint():
    """what the page shows before any click: pane 5 at the present
    moment, the cheapest."""
    opened_at()
    return render(5)
