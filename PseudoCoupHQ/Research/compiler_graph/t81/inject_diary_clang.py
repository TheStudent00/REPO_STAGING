#!/usr/bin/env python3
"""inject_diary_clang.py -- the EDIT half of `Graph.diary`'s producer,
for clang. The co-file of `t72/inject_diary_region.py`, which does the
same job for go.

Plan node: hq.research.compiler_graph.graph, method `diary`
(Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_9_graph/
CORE_0_3_5_9_graph.md).

WHERE IT RUNS
-------------
Inside the Airlock instance, on the checked-out llvm tree, where
tree-sitter is not installed. Standard library only, exactly as task
72's go injector is, and for the same reason.

WHAT IS DIFFERENT FROM THE GO CO-FILE, AND WHY
----------------------------------------------
1. THE TARGET COORDINATE IS A LINE, NOT A BYTE SPAN. Task 72 read the
   AUGUST graph, whose node ids are `<file>:<start_byte>-<end_byte>`.
   The current graph's ids are `file#line#kind#ordinal` and carry no
   byte offsets, so this program converts the line to a byte offset
   FROM THE FILE IT IS ABOUT TO EDIT. The conversion is exact and it
   is done on BYTES: several files of this region hold non-ASCII
   characters, and indexing a decoded string with a byte offset lands
   in the wrong place in exactly those files, silently. That defect is
   recorded from task 72 and is not repeated here.

2. THE BODY BRACE IS CHOSEN BY WHERE IT CLOSES. C++ puts braces at
   round-bracket depth zero that do not open a body: a constructor's
   member initializer can be `: member{1}`, and a return type can be an
   inline-defined class. So a candidate `{` is accepted only when its
   MATCHING `}` closes on the definition's own last line. A target whose
   brace is not found that way is SKIPPED and recorded with its cause,
   never guessed.

3. THE HELPER IS PER TRANSLATION UNIT, AND THE COUNTER IS NOT. C++ has
   no import, so the helper block is written into each edited file --
   the shape proved to build in-tree by task 72's clang hook lane
   (exit 0, 10 s, log_175 section 6.2). Its state lives in C++17 INLINE
   VARIABLES at namespace scope, which the linker merges into one
   instance program-wide, so the sequence number is one running count
   across the whole compiler rather than one per file.

4. THE DIARY PATH CARRIES THE PROCESS ID. `clang` forks a `-cc1`
   process, so two processes would append to one file and a buffered
   write could split a line across them. Each process opens
   `<COMPILER_DIARY>.<pid>` instead, and the lane reports every
   pid-file it finds with its line count rather than merging them.

WHAT IS DELIBERATELY NOT INSTRUMENTED, each a NAMED FRONTIER
------------------------------------------------------------
  * a body declared in a `.h` file (1,664 of the region's 10,789
    definitions) -- one edit there is carried into every translation
    unit that includes the header;
  * a body with no declared name (17) -- a lambda, which tree-sitter
    records with an empty label;
  * a `constexpr` or `consteval` body -- calling the hook from one
    would make the function unusable in a constant expression;
  * a body whose brace this program could not find inside the
    definition's own lines.
Each cause is counted in the report this program writes, so the
coverage join says "not observable by this instrument" rather than "no
probe visited it" -- the CORE's settled rule that an uninstrumented
node is a frontier, never a never-visited node.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24);
(2) verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix
brief itself reintroduced it as "same-operator pairs"). MECHANICAL
GUARD REQUIRED: every pipeline stage that groups or pairs units must
run the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim.

Coding discipline of this node (CORE 0_3_5): no complex statements.
"""

import argparse
import collections
import json
import os
import sys


# The helper, written once at the top of every edited translation unit.
# `inline` at namespace scope gives ONE instance program-wide, so `seq`
# is a single running count and not one per file.
HELPER = b'''/* t81 diary hook -- injected by t81/inject_diary_clang.py.
   Each instrumented body of the region writes its own graph node id
   here AS IT IS ENTERED, so the ORDER of visits survives. With
   COMPILER_DIARY unset the compiler behaves exactly as before.
   The three columns are go's, unchanged: a running sequence number, the
   SUBJECT (whose code the compiler had in hand), and the unit record. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
namespace t81diary {
inline FILE *out = nullptr;
inline bool tried = false;
inline long seq = 0;
inline char subject[256] = {'-', 0};
inline void flush() {
  if (out) {
    fflush(out);
  }
}
inline void note(const char *record) {
  if (!tried) {
    tried = true;
    const char *path = getenv("COMPILER_DIARY");
    if (path) {
      char full[4096];
      snprintf(full, sizeof(full), "%s.%ld", path, (long)getpid());
      out = fopen(full, "a");
      if (out) {
        atexit(t81diary::flush);
      }
    }
  }
  if (!out) {
    return;
  }
  seq = seq + 1;
  fprintf(out, "%ld\\t%s\\t%s\\n", seq, subject, record);
}
/* THE SUBJECT IS SET, NOT STACKED, and the difference is a fact about
   the probes rather than a shortcut. go's compiler compiles several
   functions at once, so task 72 needed a per-goroutine stack. A c or
   cpp probe is one translation unit holding exactly ONE function and no
   main, compiled with `-c`, so once the subject is set it stays correct
   for the rest of that compilation -- including the backend, which runs
   after the front end has finished with the only function there is. */
inline void enter(const char *spot, const char *data, int size) {
  if (size > 255) {
    size = 255;
  }
  if (size < 0) {
    size = 0;
  }
  memcpy(subject, data, (size_t)size);
  subject[size] = 0;
  char marker[512];
  snprintf(marker, sizeof(marker), "-|subject_enter:%s|-", spot);
  note(marker);
}
}
'''

MARKER = b"t81diary::note("
SUBJECT_MARKER = b"t81diary::enter("

# WHERE THE SUBJECT IS OPENED. One spot, the co-spot of go's `buildssa`:
# the point at which clang has an LLVM function in hand and is about to
# emit its body. `Fn->getName()` is a StringRef, which is not
# null-terminated, so the length is passed beside the data.
SUBJECT_SPOTS = (
    {
        "file": "clang/lib/CodeGen/CodeGenFunction.cpp",
        "anchor": "void CodeGenFunction::GenerateCode(GlobalDecl GD, "
                  "llvm::Function *Fn,",
        "label": "GenerateCode",
        "expr": "Fn->getName().data(), (int)Fn->getName().size()",
    },
)

# A body carrying one of these before its brace is not instrumented.
REFUSED_SPECIFIERS = (b"constexpr", b"consteval")


# --------------------------------------------------------- byte scans ---
#
# EVERYTHING BELOW WORKS ON BYTES. The region holds non-ASCII characters
# and a byte offset applied to a decoded string lands in the wrong place
# in exactly those files, silently. Task 72 measured that defect on the
# go region; it is not repeated here.


def line_offsets(text):
    """Byte offset of the first character of each line, 1-based index."""
    offsets = [0, 0]
    index = 0
    while True:
        found = text.find(b"\n", index)
        if found < 0:
            break
        offsets.append(found + 1)
        index = found + 1
    return offsets


def skip_quoted(text, index, limit):
    """Index just past the string or character literal at `index`."""
    quote = text[index:index + 1]
    index = index + 1
    while index < limit:
        char = text[index:index + 1]
        if char == b"\\":
            index = index + 2
            continue
        if char == quote:
            return index + 1
        index = index + 1
    return limit


def step_over(text, index, limit):
    """One step of the scan that is not a bracket. Returns the next
    index when this position was comment, string or character text, and
    -1 when the caller should look at this byte itself."""
    char = text[index:index + 1]
    if char == b"/" and index + 1 < limit:
        following = text[index + 1:index + 2]
        if following == b"/":
            stop = text.find(b"\n", index)
            if stop < 0:
                return limit
            return stop + 1
        if following == b"*":
            stop = text.find(b"*/", index)
            if stop < 0:
                return limit
            return stop + 2
    if char == b'"' or char == b"'":
        return skip_quoted(text, index, limit)
    return -1


def matching_brace(text, open_index, limit):
    """Index of the `}` that closes the `{` at `open_index`, or -1."""
    depth = 0
    index = open_index
    while index < limit:
        stepped = step_over(text, index, limit)
        if stepped >= 0:
            index = stepped
            continue
        char = text[index:index + 1]
        if char == b"{":
            depth = depth + 1
        elif char == b"}":
            depth = depth - 1
            if depth == 0:
                return index
        index = index + 1
    return -1


def body_brace(text, start, limit, close_low, close_high):
    """Index of the `{` opening the body of the definition that starts
    at `start`, or -1.

    A candidate is a `{` at round- and square-bracket depth zero. It is
    accepted only when its matching `}` lands between `close_low` and
    `close_high` -- the byte range of the definition's own last line.
    That is what separates a body from a member initializer's braced
    value and from an inline-defined return type.
    """
    index = start
    round_depth = 0
    square_depth = 0
    while index < limit:
        stepped = step_over(text, index, limit)
        if stepped >= 0:
            index = stepped
            continue
        char = text[index:index + 1]
        if char == b"(":
            round_depth = round_depth + 1
        elif char == b")":
            round_depth = round_depth - 1
        elif char == b"[":
            square_depth = square_depth + 1
        elif char == b"]":
            square_depth = square_depth - 1
        elif char == b"{":
            if round_depth == 0 and square_depth == 0:
                close = matching_brace(text, index, limit)
                if close >= close_low and close <= close_high:
                    return index
                if close < 0:
                    return -1
                index = close
                continue
        index = index + 1
    return -1


def flatten_label(label):
    """One line, no quote, no backslash -- the label as it can safely
    ride inside a C string literal.

    A definition's name is taken from its declarator text, and a
    declarator wraps across lines when the signature does: 202 of the
    9,108 targets carry a newline inside their label, and one of them
    (`CodeGenFunction::` continued on the next line, CGExpr.cpp:489)
    ended the injected string literal in the middle and broke the whole
    translation unit. Measured on the first build attempt of this lap,
    exit 2 in 68 s with `use of undeclared identifier 'E'` twenty times
    over -- the compiler reading the rest of the function as string
    text. The label is a DISPLAY LABEL and nothing joins on it, so
    collapsing its whitespace loses nothing that is read.
    """
    text = " ".join(str(label).split())
    text = text.replace("\\", " ")
    text = text.replace('"', " ")
    return text


def no_brace_cause(record, head):
    """Which of the three things a body-less definition actually is.

    Reported apart rather than as one bucket, because two of the three
    are not bodies at all and the third is the only one that would be a
    defect of this program.

      defaulted_or_deleted_body   `Foo::~Foo() = default;` -- tree-sitter
                                  records it as a definition; there is no
                                  body to enter.
      lambda_body                 a lambda has no declarator, so
                                  `graph.py` names it by its parameter
                                  list and the label begins with `(`.
      no_body_brace_in_own_lines  the residue: a definition whose brace
                                  this program could not find inside its
                                  own lines.
    """
    if b"= default" in head or b"= delete" in head:
        return "defaulted_or_deleted_body"
    label = record.get("label") or ""
    if label.startswith("("):
        return "lambda_body"
    return "no_body_brace_in_own_lines"


def header_insertion_point(text):
    """Byte offset the helper block is written at: the very top of the
    file. Chosen over "after the last include" because an include can
    sit inside a conditional block, and a helper made conditional would
    be absent exactly where the calls are not."""
    return 0


def first_body_brace(text, start, limit):
    """Index of the first `{` at round- and square-bracket depth zero
    after `start`. Used for the SUBJECT SPOTS only, which are anchored
    by their own signature text rather than by a recorded span, so
    there is no closing line to check against."""
    index = start
    round_depth = 0
    square_depth = 0
    while index < limit:
        stepped = step_over(text, index, limit)
        if stepped >= 0:
            index = stepped
            continue
        char = text[index:index + 1]
        if char == b"(":
            round_depth = round_depth + 1
        elif char == b")":
            round_depth = round_depth - 1
        elif char == b"[":
            square_depth = square_depth + 1
        elif char == b"]":
            square_depth = square_depth - 1
        elif char == b"{":
            if round_depth == 0 and square_depth == 0:
                return index
        index = index + 1
    return -1


def inject_subject_spots(src_root, dry_run):
    """Open the subject at each spot of SUBJECT_SPOTS.

    Kept as its own pass so it can be run alone (`--subject-only`)
    against a tree whose bodies are already instrumented: the note
    statements are unchanged and only one object has to be rebuilt.
    """
    placed = []
    for spot in SUBJECT_SPOTS:
        full = os.path.join(src_root, spot["file"])
        if not os.path.exists(full):
            placed.append(dict(spot, cause="file_not_on_disk"))
            continue
        handle = open(full, "rb")
        text = handle.read()
        handle.close()
        if SUBJECT_MARKER in text:
            placed.append(dict(spot, cause="already_placed"))
            continue
        at = text.find(spot["anchor"].encode())
        if at < 0:
            placed.append(dict(spot, cause="anchor_not_found"))
            continue
        brace = first_body_brace(text, at, len(text))
        if brace < 0:
            placed.append(dict(spot, cause="no_body_brace"))
            continue
        statement = '\n  t81diary::enter("' + spot["label"] + '", '
        statement = statement + spot["expr"] + ');\n'
        text = text[:brace + 1] + statement.encode() + text[brace + 1:]
        if MARKER not in text:
            at = header_insertion_point(text)
            text = text[:at] + HELPER + text[at:]
        if not dry_run:
            handle = open(full, "wb")
            handle.write(text)
            handle.close()
        placed.append(dict(spot, cause="placed"))
        print("subject spot %-16s placed in %s" % (spot["label"],
                                                   spot["file"]))
    return placed


# ------------------------------------------------------------- the pass --

def inject(targets_path, src_root, report_path, dry_run,
           subject_only=False):
    if subject_only:
        placed = inject_subject_spots(src_root, dry_run)
        report = {
            "generated_by": "t81/inject_diary_clang.py --subject-only",
            "subject_spots": placed,
        }
        if report_path:
            handle = open(report_path, "w")
            json.dump(report, handle, indent=1)
            handle.write("\n")
            handle.close()
        for row in placed:
            print("   %-16s %s" % (row["label"], row["cause"]))
        return
    handle = open(targets_path)
    payload = json.load(handle)
    handle.close()
    targets = payload["targets"]

    by_file = collections.defaultdict(list)
    for record in targets:
        by_file[record["file"]].append(record)

    instrumented = []
    skipped = []
    files_edited = 0

    for relative_path in sorted(by_file):
        records = by_file[relative_path]
        full = os.path.join(src_root, relative_path)
        if not os.path.exists(full):
            for record in records:
                skipped.append(dict(record, cause="file_not_on_disk"))
            continue
        handle = open(full, "rb")
        text = handle.read()
        handle.close()

        if MARKER in text:
            for record in records:
                skipped.append(dict(record, cause="already_instrumented"))
            continue

        offsets = line_offsets(text)
        edits = []
        for record in records:
            start_line = record["start_line"]
            end_line = record["end_line"]
            if end_line + 1 >= len(offsets):
                skipped.append(dict(record, cause="span_past_end_of_file"))
                continue
            start = offsets[start_line]
            close_low = offsets[end_line]
            close_high = offsets[end_line + 1]
            limit = close_high
            # The DECLARATION HEAD: the definition's own bytes up to
            # its first brace. `close_low` alone is empty for a
            # one-line definition, which is exactly where
            # `= default;` lives, so the span runs to the end of the
            # last line and is then cut at the first brace.
            span = text[start:close_high]
            cut = span.find(b"{")
            head = span
            if cut >= 0:
                head = span[:cut]
            refused = False
            for word in REFUSED_SPECIFIERS:
                if word in head:
                    skipped.append(
                        dict(record, cause="constexpr_or_consteval"))
                    refused = True
                    break
            if refused:
                continue
            brace = body_brace(text, start, limit, close_low, close_high)
            if brace < 0:
                skipped.append(dict(record, cause=no_brace_cause(record, head)))
                continue
            note = record["id"]
            note = note + "|" + flatten_label(record["label"])
            note = note + "|" + relative_path
            note = note + ":" + str(start_line)
            statement = '\n  t81diary::note("' + note + '");\n'
            edits.append((brace + 1, statement.encode()))
            instrumented.append(record)

        if not edits:
            continue

        edits.sort(key=lambda item: item[0], reverse=True)
        for offset, statement in edits:
            text = text[:offset] + statement + text[offset:]

        at = header_insertion_point(text)
        text = text[:at] + HELPER + text[at:]

        if not dry_run:
            handle = open(full, "wb")
            handle.write(text)
            handle.close()
        files_edited = files_edited + 1
        print("instrumented %5d bodies in %s" % (len(edits), relative_path))

    subject_spots = inject_subject_spots(src_root, dry_run)

    causes = collections.Counter(record["cause"] for record in skipped)
    report = {
        "subject_spots": subject_spots,
        "generated_by": "t81/inject_diary_clang.py",
        "targets_read": len(targets),
        "files_edited": files_edited,
        "instrumented": len(instrumented),
        "skipped": len(skipped),
        "skipped_by_cause": dict(sorted(causes.items())),
        "dry_run": bool(dry_run),
        "instrumented_coordinates": [
            "%s:%s" % (record["file"], record["start_line"])
            for record in instrumented
        ],
        "instrumented_ids": [record["id"] for record in instrumented],
        "skipped_records": skipped,
        "frontier_note": (
            "Every skipped body is a NAMED FRONTIER of the coverage join, "
            "never a never-visited node. The two populations the target "
            "file itself excluded -- bodies in header files and bodies "
            "with no declared name -- are counted in "
            "t81/diary_targets_cpp.json, not here."
        ),
    }
    if report_path:
        handle = open(report_path, "w")
        json.dump(report, handle, indent=1)
        handle.write("\n")
        handle.close()
    print("targets read : %d" % report["targets_read"])
    print("files edited : %d" % files_edited)
    print("instrumented : %d" % report["instrumented"])
    print("skipped      : %d" % report["skipped"])
    for cause, count in sorted(causes.items()):
        print("   %-32s %d" % (cause, count))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", required=True)
    parser.add_argument("--src", required=True)
    parser.add_argument("--report", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--subject-only", action="store_true",
                        help="place only the subject spots, leaving the "
                             "note statements as they are")
    arguments = parser.parse_args()
    inject(arguments.targets, arguments.src, arguments.report,
           arguments.dry_run, arguments.subject_only)
    return 0


if __name__ == "__main__":
    sys.exit(main())
