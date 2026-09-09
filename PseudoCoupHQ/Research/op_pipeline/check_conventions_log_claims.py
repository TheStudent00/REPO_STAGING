#!/usr/bin/env python3
"""check_conventions_log_claims.py -- re-run the commands a DevComms log
pasted, and say which of its claims actually reproduce.

Node: hq.conventions (Planning/node_0_2_conventions/CORE_0_2_conventions.md).
The node owns "how the owner wants to be worked with" -- the two-list rule, the
"every 'I verified X' pastes command and output" rule.  This program is the
MECHANICAL side of that rule: it does not need the agent that wrote the log
to be present or honest.

Task 90, 2026-09-04, from the owner: "i want to make sure youre not fucking me
over... please tell me how we can hold you accountable."  The artifacts of
this line were already checkable (the dashboard counts files at open time,
check_no_spelling_keys.py runs unmodified, the chronology is raw git log).
The gap was PROSE.  This closes it.

WHAT A CLAIM IS, derived from the six logs read first (190-195), not invented
--------------------------------------------------------------------------
Reading log_190, log_191, log_192, log_193, log_194 and log_195 first, the
house shape is not one shape, it is four, and the tool names all four:

  A. SHELL TRANSCRIPT.  A fenced block whose lines begin `$ `.  Each `$ `
     line is a command; the lines under it, up to the next `$ ` or the end
     of the block, are its pasted output.  This is the only shape that
     carries something to re-run.  Present in logs 191, 192, 194, 195.

  B. ATTRIBUTION.  A fenced block introduced by a lead-in naming where the
     content came from -- `**LITERAL**, lane 11 §[4/6]`, `printed by lane 6
     from the module itself`, `**LITERAL**, `graph.py`, `VARIANT_IDENTITY_
     STATED``.  It cites an artifact.  It carries NO command.  This is the
     dominant shape of logs 190 and 193, which have 26 fenced blocks each
     and zero `$ ` lines between them.

  C. BARE PASTE.  A fenced block with neither a `$ ` line nor an
     attribution lead-in.

  D. PROSE VERIFICATION.  A sentence outside any fence asserting a check --
     "verified", "confirmed", "proved", "re-ran", "zero regressions" --
     with no fenced block beside it.

B, C and D are UNVERIFIABLE and are counted as such.  A log that says
"I verified X" with nothing to re-run appears in that bucket, by name, with
its line number.  THE UNVERIFIABLE BUCKET IS THE POINT OF THIS TOOL: a log
does not pass merely because nothing failed.

THE OUTCOMES (five, and no sixth)
---------------------------------
  MATCHES         ran inside Airlock; output equals what the log pasted,
                  after the normalisation stated in `normalise()` and
                  nothing else.
  DIFFERS         ran; output disagrees.  Both are shown, as a diff.
  UNVERIFIABLE    the claim carries no reproducing command at all.
  REFUSED         the command would write, delete, install or submit.  It
                  is named, with the rule that fired.  Never run.  Also
                  fires, before any comparison, for:
                    log_unreachable       the command names a path (a
                                          token starting `/`, `~` or
                                          `./`) that does not exist from
                                          the instance running THIS
                                          verify -- e.g. another
                                          instance's `agent/logs`.  Ran
                                          nowhere; scored REFUSED, never
                                          DIFFERS, because a missing-file
                                          error is not the claim
                                          disagreeing with the paste.
  NOT_RERUNNABLE  it carries a command, but re-running it cannot decide
                  anything, for a stated CAUSE.  Causes seen in the real
                  logs, each with its own name:
                    out_of_sandbox        names a host path Airlock does
                                          not mount (`~/Programming/Airlock`,
                                          `~/Programming/Ourobrowser`)
                    elided_command        the command text itself carries
                                          `...` in place of a real path
                    moving_reference      it reads a target that moves --
                                          `HEAD`, the working tree, a
                                          wall-clock `--since=`
                    no_output_pasted      a command with nothing under it
                    output_elided         the paste is visibly abridged
                                          (`...`, a mid-token cut), so an
                                          exact comparison is impossible
                    output_annotated      the paste carries hand-written
                                          prose inside it, so it is not a
                                          transcript
                    tool_absent           the program is not in the image
                    timeout_<n>s          it did not finish in <n>s
                  A NOT_RERUNNABLE claim is NEVER counted as matching.

THE SANDBOX CONSTRAINT
----------------------
This program re-runs commands read out of text files.  That is dangerous by
construction, so:

  * It runs ONLY inside Airlock.  `--verify` refuses to start unless the
    lane protocol's own folders -- `/drop`, `/logs`, `/out` -- and the work
    directory are present, which they are only inside `sandbox-runner`.  On
    the host, use `--emit-lane` to write the lane and submit it with
    `airlock submit`; the refusal was demonstrated, not asserted, in lane
    t90_l2 of task 90.
  * A command is allowed only if EVERY stage of every pipeline has a head
    program on ALLOWED_HEADS -- deny by default, not deny by list -- and no
    stage matches a REFUSE_TOKENS rule, and no stage redirects into a path.
  * A refused command is reported as REFUSED with the rule name, never
    silently skipped.

MEMORY BOUND
------------
Stated before any pass: this program holds one log's text (the largest of
the six is 886 lines / 34 KB) plus captured output capped at
CAPTURE_CAP_BYTES per command.  The bound is 512 MB; the guard aborts by
name -- `ABORT: MEMORY_BOUND_EXCEEDED` -- at MEMORY_CEILING_MB (6,144 MB),
checked after every command with resource.getrusage.  (`/usr/bin/time -v`
is not in the Airlock image; log_194 §Memory recorded that.)

USAGE
-----
  # on the host: write a lane that will do the work inside Airlock
  python3 check_conventions_log_claims.py --emit-lane <lane.sh> <log.md>...
  cd ~/Programming/Airlock && ./airlock submit <lane.sh> --no-batch

  # inside the sandbox (what the lane runs):
  python3 check_conventions_log_claims.py --verify <log.md>...
  python3 check_conventions_log_claims.py --extract-only <log.md>...
  # options: --timeout <s>  --json <path>  --diff-lines <n>
"""

import argparse
import difflib
import json
import os
import re
import resource
import shlex
import shutil
import subprocess
import sys

# ---------------------------------------------------------------------------
# the sandbox map.  Copied from ~/Programming/Airlock/mounts.conf, which is
# per-machine and is NOT itself mounted into the container, so it cannot be
# read at run time.  Every entry is verified to exist before use and the map
# actually used is printed in the report -- so a stale copy shows up as a
# missing root rather than as a wrong verdict.
# ---------------------------------------------------------------------------
SANDBOX_ROOTS = {
    "~/Programming/PseudoCoupHQ": "/projects/PseudoCoupHQ",
    "~/Programming/PseudoCoup_v5": "/projects/PseudoCoup_v5",
    "~/Programming/PseudoCoup_v6": "/projects/PseudoCoup_v6",
    "~/Programming/PlanPlan": "/projects/PlanPlan",
    "~/Programming/PseudoCoupGraphs": "/projects/PseudoCoupGraphs",
    "~/Programming/Sources": "/sources",
}
WORKDIR = "/projects/PseudoCoupHQ"          # what the logs' relative paths assume
CAPTURE_CAP_BYTES = 256 * 1024
MEMORY_CEILING_MB = 6144                     # abort by name at this
DEFAULT_TIMEOUT_S = 120

# ---------------------------------------------------------------------------
# the refusal rules.  Derived from what the commands in the six real logs
# actually do, plus the classes the brief names.  Each is (rule_name, regex).
# A match REFUSES and the rule name is printed -- refusal by name.
# ---------------------------------------------------------------------------
REFUSE_TOKENS = [
    ("writes_the_tree__generator",
     r"\bhq\.sh\b|\bbash\s+hq\.sh\b|\btrack\.py\b"),
    ("writes_version_control",
     r"\bgit\s+(commit|push|add|rm|mv|checkout|switch|reset|restore|clean"
     r"|stash|apply|revert|merge|rebase|tag|fetch|pull|gc|filter-branch)\b"),
    ("removes_or_moves_files",
     r"(^|[|;&(\s])(rm|rmdir|mv|cp|install|shred|truncate|dd|unlink)\s"),
    ("creates_files",
     r"(^|[|;&(\s])(touch|mkdir|mktemp|ln)\s"),
    ("edits_in_place",
     r"\bsed\s+(-[a-zA-Z]*i|--in-place)\b|\bperl\s+-[a-zA-Z]*i\b|\btee\b"),
    ("changes_permissions",
     r"(^|[|;&(\s])(chmod|chown|chgrp|umask)\s"),
    ("installs",
     r"\b(pip|pip3|apt|apt-get|dnf|yum|npm|cargo\s+install|go\s+install"
     r"|gem\s+install)\s+(install|add|-U)"),
    ("submits_or_moves_the_sandbox",
     r"\bairlock\s+(submit|down|up|prune)\b|\b(up|down|submit|batch)\.sh\b"),
    ("touches_the_container_host",
     r"\b(podman|docker|systemctl|systemd-run|loginctl|sudo|su)\b"),
    ("reaches_the_network",
     r"(^|[|;&(\s])(curl|wget|ssh|scp|rsync|nc|ping)\s"),
    ("writes_via_python",
     r"open\s*\([^)]*['\"][arw]\+?[bt]?['\"]|\bos\.(remove|unlink|rename|mkdir"
     r"|makedirs|rmdir)\b|\bshutil\.|\bsubprocess\.|\bPath\([^)]*\)\.write"),
]

# deny by default: the head of every pipeline stage must be one of these.
# The list is exactly the read-only programs the six logs actually invoke,
# plus the shell keywords their loops use.
ALLOWED_HEADS = set("""
awk basename cat cksum cmp comm cut date df diff dirname du echo env expr
file find fold git grep head jq ls md5sum nl node od paste printf python
python3 readlink realpath sed seq sha1sum sha256sum sort stat strings tail
tr uniq wc which xxd yes true false test [ [[ printenv column
cd pushd popd time
for do done if then else elif fi while case esac in
""".split())

# git subcommands that only read.  Anything else under `git` is refused by
# the writes_version_control rule above; this is the positive side of it.
GIT_READ_ONLY = {"log", "show", "diff", "status", "ls-files", "ls-tree",
                 "cat-file", "rev-parse", "rev-list", "blame", "describe",
                 "shortlog", "grep", "config", "count-objects", "for-each-ref"}

# ---------------------------------------------------------------------------
# not-rerunnable detectors, on the command text
# ---------------------------------------------------------------------------
MOVING_REFERENCE = [
    (r"\bHEAD\b", "reads HEAD, which moves"),
    (r"\bgit\s+log\b(?![^|]*\b[0-9a-f]{7,40}\b)", "git log with no pinned revision"),
    (r"\bgit\s+status\b", "reads the working tree, which moves"),
    (r"\bgit\s+diff\s*(\||$)", "git diff of the working tree, which moves"),
    (r"--since=", "names a wall-clock time"),
    (r"\bdate\b(?!\w)", "reads the clock"),
]
ELIDED_IN_COMMAND = r"(?<![.\w])\.\.\.(?![.\w])|/\.\.\./"
VERIFY_VERBS = re.compile(
    r"\b(i verified|we verified|verified|verifies|confirmed|confirms|"
    r"re-?ran|rerun|reproduced|reproduces|proved|proves|proven|"
    r"zero regressions|no regressions|cross-?checked|cross-?validated|"
    r"was checked|were checked|has been checked)\b", re.I)
ATTRIBUTION = re.compile(
    r"\bLITERAL\b|\bprinted by\b|\bquoted (from|whole)\b|\bread (out )?of\b|"
    r"\bread by\b|\bas .* wrote it\b|\bfrom the (module|function|binary)\b|"
    r"\bpasted (verbatim )?from\b|\bits (whole )?output\b|\bthe command, from\b",
    re.I)
NO_OUTPUT_MARKERS = {"(no output)", "(none)", "(empty)"}


# ---------------------------------------------------------------------------
# extraction
# ---------------------------------------------------------------------------

def read_lines(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read().split("\n")


def blocks_of(lines):
    """Every fenced block: (fence_info, start_line_1based, body_lines)."""
    out = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("```"):
            info = lines[i][3:].strip()
            start = i + 1
            body = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            out.append((info, start, body))
        i += 1
    return out


def lead_in_of(lines, fence_index_0based):
    """The PARAGRAPH above a fence -- the claim the block is evidence for.

    Markdown puts a blank line between a paragraph and the fence under it,
    and these logs are hard-wrapped, so a single line is a fragment.  Skip
    up to two blank lines, then take the whole blank-line-delimited
    paragraph (at most eight wrapped lines) and join it."""
    j = fence_index_0based - 1
    blanks = 0
    while j >= 0 and not lines[j].strip() and blanks < 2:
        j -= 1
        blanks += 1
    got = []
    while j >= 0 and len(got) < 8:
        s = lines[j].strip()
        if not s or s.startswith("```"):
            break
        got.append(s)
        j -= 1
    return " ".join(reversed(got))


def heading_at(lines, index_0based):
    for j in range(index_0based, -1, -1):
        if lines[j].startswith("#"):
            return lines[j].strip("# ").strip()
    return "(no heading)"


def join_continuations(body, start):
    """Read one `$ ` command starting at body[start].  Returns
    (command_text, next_index).  Handles trailing `\\` continuation and an
    unterminated quote (the `python3 -c "` shape logs 195 and 192 use)."""
    text = body[start][2:]
    i = start + 1
    while i < len(body):
        if body[i].startswith("$ "):
            break
        if text.rstrip().endswith("\\"):
            text = text.rstrip()[:-1] + " " + body[i].strip()
            i += 1
            continue
        if text.count('"') % 2 == 1 or text.count("'") % 2 == 1:
            text = text + "\n" + body[i]
            i += 1
            continue
        if shell_block_open(text):
            text = text + "\n" + body[i]
            i += 1
            continue
        break
    return text, i


def shell_block_open(text):
    """Is this command text a shell compound command that has not closed?

    log_195 pastes a `for f in ...; do ... done` sweep across four lines of
    one block.  Without this the first line alone is taken as the command
    and bash answers `syntax error: unexpected end of file`, which would be
    reported as the log's fault rather than the reader's.

    Only a command that BEGINS with a compound keyword counts.  Found by
    running this tool on its own log (lane t90_l8): a
    `python3 -c "... for k in [...] ..."` one-liner contains the word `for`,
    and without this restriction the tool swallowed the pasted output into
    the command and then refused it as an unknown program."""
    first = text.lstrip().split()
    if not first or first[0] not in ("for", "while", "until", "if", "case"):
        return False
    words = re.findall(r"[A-Za-z_]+", text)
    opens = sum(1 for w in words if w in ("do", "then", "case"))
    closes = sum(1 for w in words if w in ("done", "fi", "esac"))
    starts = sum(1 for w in words if w in ("for", "while", "until", "if"))
    return (starts > 0 or opens > 0) and closes < max(starts, opens)


def extract(path):
    """Every claim in one log, in file order."""
    lines = read_lines(path)
    claims = []
    fenced_line_numbers = set()

    fences = [i for i, l in enumerate(lines) if l.startswith("```")]
    for k in range(0, len(fences) - 1, 2):
        for n in range(fences[k], fences[k + 1] + 1):
            fenced_line_numbers.add(n)

    for info, start0, body in blocks_of(lines):
        fence_line = start0                      # 1-based line of the ``` itself
        lead = lead_in_of(lines, start0 - 1)
        head = heading_at(lines, start0 - 1)
        has_prompt = any(l.startswith("$ ") for l in body)

        if has_prompt:
            i = 0
            while i < len(body):
                if not body[i].startswith("$ "):
                    i += 1
                    continue
                cmd, nxt = join_continuations(body, i)
                out = []
                j = nxt
                while j < len(body) and not body[j].startswith("$ "):
                    out.append(body[j])
                    j += 1
                claims.append({
                    "log": os.path.basename(path),
                    "line": fence_line + 1 + i,
                    "section": head,
                    "shape": "shell_transcript",
                    "text": lead,
                    "command": cmd,
                    "pasted": "\n".join(out).rstrip(),
                })
                i = j
        else:
            shape = "attribution" if ATTRIBUTION.search(lead) else "bare_paste"
            claims.append({
                "log": os.path.basename(path),
                "line": fence_line,
                "section": head,
                "shape": shape,
                "text": lead,
                "command": None,
                "pasted": "\n".join(body).rstrip(),
                "source": cited_source(lead) if shape == "attribution" else None,
            })

    # prose verification claims: a whole PARAGRAPH outside any fence that
    # asserts a check, with no fenced block beside it.  Whole paragraphs,
    # not lines -- these logs are hard-wrapped, so a line is a fragment and
    # a fragment is not a claim anyone can read.
    for start, end, para in paragraphs(lines, fenced_line_numbers):
        if not VERIFY_VERBS.search(para):
            continue
        # a paragraph that leads into a fenced block within two lines is
        # already counted as that block's claim
        nxt = end + 1
        while nxt < len(lines) and not lines[nxt].strip():
            nxt += 1
        if nxt < len(lines) and lines[nxt].startswith("```"):
            continue
        claims.append({
            "log": os.path.basename(path),
            "line": start + 1,
            "section": heading_at(lines, start),
            "shape": "prose_verification",
            "text": para,
            "command": None,
            "pasted": "",
        })

    claims.sort(key=lambda c: c["line"])
    return claims


def paragraphs(lines, fenced):
    """Blank-line-delimited paragraphs outside every fence, as
    (start_index, end_index, joined_text).  Headings and table rows are
    skipped -- a heading is not a claim and a table row is a figure, not an
    assertion of having checked something."""
    out = []
    i = 0
    while i < len(lines):
        if i in fenced or not lines[i].strip():
            i += 1
            continue
        start = i
        got = []
        while i < len(lines) and i not in fenced and lines[i].strip():
            got.append(lines[i].strip())
            i += 1
        end = i - 1
        body = [g for g in got if not g.startswith("#")]
        if not body:
            continue
        if all(g.startswith("|") for g in body):
            continue
        out.append((start, end, " ".join(body)))
    return out


def cited_source(lead):
    """What an attribution block says its content came from."""
    m = re.search(r"`([^`]+)`", lead)
    if m:
        return m.group(1)
    m = re.search(r"(lane\s+\d+[^,.:]*)", lead, re.I)
    if m:
        return m.group(1).strip()
    return lead[:90]


# ---------------------------------------------------------------------------
# classification, before anything is run
# ---------------------------------------------------------------------------

def split_stages(cmd):
    """Every pipeline / list stage of a command line, crudely but on the
    real shapes: split on | ; && || and newline, outside quotes."""
    stages, cur, q = [], "", None
    i = 0
    while i < len(cmd):
        ch = cmd[i]
        if q:
            cur += ch
            if ch == q:
                q = None
            i += 1
            continue
        if ch in "\"'":
            q = ch
            cur += ch
            i += 1
            continue
        if ch == "|" and cmd[i:i + 2] != "|&":
            stages.append(cur)
            cur = ""
            i += 2 if cmd[i:i + 2] == "||" else 1
            continue
        if ch == "&" and cmd[i:i + 2] == "&&":
            stages.append(cur)
            cur = ""
            i += 2
            continue
        if ch in ";\n":
            stages.append(cur)
            cur = ""
            i += 1
            continue
        cur += ch
        i += 1
    stages.append(cur)
    # command substitutions are commands too, and must be vetted like any
    # other stage -- log_195's sweep runs `n=$(grep -c ... )` inside a loop
    subs = []
    for s in stages:
        for m in re.finditer(r"\$\(([^()]*)\)|`([^`]*)`", s):
            subs.extend(split_stages(m.group(1) or m.group(2) or ""))
    stages = [re.sub(r"\$\([^()]*\)|`[^`]*`", "", s) for s in stages] + subs
    return [s.strip() for s in stages if s.strip()]


def head_of(stage):
    s = stage.lstrip("( ")
    s = re.sub(r"^\s*\w+=\S*\s*", "", s)          # VAR=x cmd, and bare VAR=
    s = re.sub(r"^\s*(/usr/bin/|/bin/)", "", s)
    tok = s.split()
    return tok[0] if tok else ""


def writes_by_redirection(stage):
    """A `>` or `>>` whose target is a path.  `2>&1`, `>/dev/null` are not."""
    for m in re.finditer(r"(?<!\d)>>?\s*([^\s|;&]+)", stage):
        tgt = m.group(1)
        if tgt.startswith("&"):
            continue
        if tgt.rstrip("'\"") in ("/dev/null", "/dev/stdout", "/dev/stderr"):
            continue
        return tgt
    return None


def classify(cmd):
    """(verdict, reason) where verdict is 'run', 'REFUSED' or a cause name."""
    for rule, rx in REFUSE_TOKENS:
        m = re.search(rx, cmd)
        if m:
            return "REFUSED", "%s -- matched `%s`" % (rule, m.group(0).strip())

    for stage in split_stages(cmd):
        if re.match(r"^\w+=\S*$", stage):        # a bare assignment runs nothing
            continue
        tgt = writes_by_redirection(stage)
        if tgt:
            return ("REFUSED", "redirects_into_a_path -- an unquoted `>` whose "
                    "target is `%s`; as pasted, bash would truncate that "
                    "name" % tgt)
        h = head_of(stage)
        if h in ("time", "/usr/bin/time"):
            h = head_of(re.sub(r"^\s*(/usr/bin/)?time\s+(-\S+\s+)*", "", stage))
        if h.endswith(".sh") or h.endswith(".py"):
            return "REFUSED", "runs_a_script_whose_effects_are_unknown -- `%s`" % h
        if h not in ALLOWED_HEADS:
            return "REFUSED", "head_not_on_the_read_only_allowlist -- `%s`" % h
        if h == "git":
            sub = ""
            toks = shlex.split(stage, posix=True) if _lexable(stage) else stage.split()
            for t in toks[1:]:
                if not t.startswith("-"):
                    sub = t
                    break
            if sub and sub not in GIT_READ_ONLY:
                return "REFUSED", "git_subcommand_not_read_only -- `git %s`" % sub

    if re.search(ELIDED_IN_COMMAND, cmd):
        return "elided_command", "the command text carries `...` in place of a real path"

    host = re.search(r"(~|/home/[a-z]+)/Programming/([A-Za-z0-9_]+)", cmd)
    if host:
        name = "~/Programming/" + host.group(2)
        if name not in SANDBOX_ROOTS:
            return "out_of_sandbox", "names `%s`, which Airlock does not mount" % name
        if not os.path.isdir(SANDBOX_ROOTS[name]):
            return ("out_of_sandbox",
                    "names `%s`; mounts.conf maps it to %s but that mount is "
                    "absent in this container" % (name, SANDBOX_ROOTS[name]))

    for rx, why in MOVING_REFERENCE:
        if re.search(rx, cmd):
            return "moving_reference", why

    # is every program the command names actually in this image?  log_195
    # pastes `/usr/bin/time -v ...`, and /usr/bin/time is not in the Airlock
    # image (log_194 §Memory recorded that).  Detecting it here rather than
    # from the exit code matters because the log's own pipeline ends in
    # `grep`, which swallows the shell's "No such file" and returns 1.
    for stage in split_stages(cmd):
        for word in re.findall(r"(?:^|[|;&(\s])(/[\w./-]+|[\w.-]+)(?=\s)", stage):
            if word.startswith("/"):
                if not os.path.exists(word):
                    return "tool_absent", "`%s` is not in the Airlock image" % word
                break
            if word in ALLOWED_HEADS and shutil.which(word) is None \
               and word not in ("for", "do", "done", "if", "then", "else",
                                "elif", "fi", "while", "case", "esac", "in",
                                "test", "[", "[[", "true", "false", "echo",
                                "printf"):
                return "tool_absent", "`%s` is not in the Airlock image" % word
            break

    return "run", ""


def _lexable(s):
    try:
        shlex.split(s, posix=True)
        return True
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# running and comparing
# ---------------------------------------------------------------------------

def normalise(text):
    """The ONLY normalisation applied, stated so nobody reads MATCHES as
    fuzzy: trailing whitespace stripped per line, trailing blank lines
    dropped.  Nothing else -- no case folding, no whitespace collapsing, no
    number rounding."""
    lines = [l.rstrip() for l in text.split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def paste_is_elided(pasted):
    for l in pasted.split("\n"):
        s = l.strip()
        if s in ("...", "…", "[...]", "(truncated)", "[truncated]"):
            return "the paste carries an elision line (`%s`)" % s
        if s.endswith("...") and not s.startswith("$"):
            return "a pasted line ends in `...`"
    return None


def paste_is_annotated(pasted):
    for l in pasted.split("\n"):
        if re.search(r"—|–", l) and re.search(r"\bsee §|\bsee §", l):
            return "the paste carries a hand-written aside (`see §...`)"
        if re.search(r"\s->\s", l) and not l.startswith("$"):
            return "the paste carries an arrow gloss (`->`)"
    return None


def run_one(cmd, timeout_s):
    try:
        p = subprocess.run(["bash", "-c", cmd], cwd=WORKDIR,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=timeout_s)
    except subprocess.TimeoutExpired:
        return None, "timeout"
    except FileNotFoundError:
        return None, "no_bash"
    out = p.stdout[:CAPTURE_CAP_BYTES].decode("utf-8", "replace")
    truncated = len(p.stdout) > CAPTURE_CAP_BYTES
    return {"rc": p.returncode, "out": out, "truncated": truncated}, None


def peak_rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def unreachable_path_token(cmd):
    """The first path-like token in `cmd` that does not exist from where
    this process runs, or None.  A path-like token starts with `/`, `~`
    or `./` -- the restriction the brief for task 99 names, so a bare
    word or a flag is never mistaken for a path."""
    try:
        toks = shlex.split(cmd)
    except ValueError:
        toks = cmd.split()
    for t in toks:
        if t.startswith("/") or t.startswith("~") or t.startswith("./"):
            if not os.path.exists(os.path.expanduser(t)):
                return t
    return None


def verify(claims, timeout_s, diff_lines, do_run):
    total = len(claims)
    for i, c in enumerate(claims, 1):
        print("[%d/%d] %s:%d  %s" % (i, total, c["log"], c["line"], c["shape"]))
        sys.stdout.flush()

        if c["command"] is None:
            c["outcome"] = "UNVERIFIABLE"
            c["reason"] = {
                "attribution": "attribution_only -- cites `%s`, carries no command"
                               % (c.get("source") or "?"),
                "bare_paste": "pasted_without_source -- no command, no attribution",
                "prose_verification":
                    "prose_only -- a verification is asserted with nothing beside it",
            }[c["shape"]]
            continue

        verdict, reason = classify(c["command"])
        if verdict == "REFUSED":
            c["outcome"] = "REFUSED"
            c["reason"] = reason
            continue
        if verdict != "run":
            c["outcome"] = "NOT_RERUNNABLE"
            c["reason"] = "%s -- %s" % (verdict, reason)
            continue
        if not c["pasted"].strip():
            c["outcome"] = "NOT_RERUNNABLE"
            c["reason"] = "no_output_pasted -- the command has nothing under it"
            continue

        tok = unreachable_path_token(c["command"])
        if tok is not None:
            c["outcome"] = "REFUSED"
            c["reason"] = ("log_unreachable -- %s is not reachable from this "
                           "instance; re-run --verify from the instance whose "
                           "logs the claim cites" % tok)
            continue

        if not do_run:
            c["outcome"] = "WOULD_RUN"
            c["reason"] = ""
            continue

        got, err = run_one(c["command"], timeout_s)
        if err == "timeout":
            c["outcome"] = "NOT_RERUNNABLE"
            c["reason"] = "timeout_%ds -- it did not finish" % timeout_s
            continue
        if got is None:
            c["outcome"] = "NOT_RERUNNABLE"
            c["reason"] = "no_bash -- the shell is missing"
            continue

        rss = peak_rss_mb()
        if rss > MEMORY_CEILING_MB:
            print("ABORT: MEMORY_BOUND_EXCEEDED -- peak RSS %.1f MB over the "
                  "%d MB ceiling, at claim %d/%d" % (rss, MEMORY_CEILING_MB, i, total))
            sys.exit(3)

        fresh = got["out"]
        if got["truncated"]:
            c["outcome"] = "NOT_RERUNNABLE"
            c["reason"] = ("capture_truncated -- output exceeded %d bytes"
                           % CAPTURE_CAP_BYTES)
            continue
        if re.search(r"command not found|No such file or directory: '?bash",
                     fresh) and got["rc"] in (126, 127):
            c["outcome"] = "NOT_RERUNNABLE"
            c["reason"] = "tool_absent -- %s" % fresh.strip().split("\n")[0]
            c["fresh"] = fresh
            continue

        why = paste_is_elided(c["pasted"]) or paste_is_annotated(c["pasted"])
        if why:
            cause = "output_elided" if paste_is_elided(c["pasted"]) else "output_annotated"
            c["outcome"] = "NOT_RERUNNABLE"
            c["reason"] = "%s -- %s; an exact comparison is impossible" % (cause, why)
            c["fresh"] = fresh
            continue

        want = normalise(_strip_no_output(c["pasted"]))
        have = normalise(fresh)
        if want == have:
            c["outcome"] = "MATCHES"
            c["reason"] = ""
        elif is_long_listing(c["command"]) and same_listing_body(want, have):
            c["outcome"] = "NOT_RERUNNABLE"
            c["reason"] = ("host_specific_output -- an `ls -l` listing carries "
                           "the owner name and the LOCAL clock of the machine "
                           "it ran on; inside Airlock those are `root` and UTC. "
                           "The sizes and names do agree, line for line")
            c["fresh"] = fresh
        elif collapse_ws(want) == collapse_ws(have) and collapse_ws(want):
            c["outcome"] = "NOT_RERUNNABLE"
            c["reason"] = ("paste_reflowed -- the log hard-wrapped this output "
                           "to fit its width, so it is not a byte transcript. "
                           "Every non-whitespace character is identical")
            c["fresh"] = fresh
        else:
            c["outcome"] = "DIFFERS"
            c["reason"] = "the command runs; its output disagrees with the paste"
            c["diff"] = "\n".join(list(difflib.unified_diff(
                want.split("\n"), have.split("\n"),
                fromfile="pasted in the log", tofile="produced now",
                lineterm=""))[:diff_lines])
        c["fresh"] = fresh
    return claims


def collapse_ws(text):
    return " ".join(text.split())


def is_long_listing(cmd):
    """`ls` with a long-format flag, in any stage."""
    for stage in split_stages(cmd):
        toks = stage.split()
        if not toks or head_of(stage) != "ls":
            continue
        for t in toks[1:]:
            if t.startswith("-") and not t.startswith("--") and "l" in t:
                return True
    return False


LS_PERMS = re.compile(r"^[-dlcbps][rwxsStT-]{9}[.+]?$")


def same_listing_body(want, have):
    """Do two `ls -l` listings agree on what they actually report -- the
    ordered sequence of (size, basename) -- while differing only in the
    owner/group and time columns a different machine writes differently?

    This is deliberately narrow.  A different NUMBER of rows, a different
    size, a different name or a different ORDER all fall through to DIFFERS:
    `ls` sorts, so a reordered paste is an edited paste, not a machine
    difference.  Rows the pattern cannot read at all also fall through."""
    def body(text):
        rows = []
        for line in text.split("\n"):
            line = line.strip()
            if not line or line.startswith("total "):
                continue
            tok = line.split()
            # read the columns positionally: perms, links, owner, group,
            # SIZE, then a date of one to three fields, then the NAME last.
            # Read from both ends so a row with the date column removed by
            # hand still parses -- what is compared is size and name.
            if len(tok) < 5 or not LS_PERMS.match(tok[0]) or not tok[4].isdigit():
                return None
            name = os.path.basename(line.split(" -> ")[0].split()[-1])
            if name in (".", ".."):
                continue
            rows.append((tok[4], name))
        return rows or None
    a, b = body(want), body(have)
    return a is not None and a == b


def _strip_no_output(pasted):
    if pasted.strip().lower() in NO_OUTPUT_MARKERS:
        return ""
    return pasted


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------

ORDER = ["MATCHES", "DIFFERS", "UNVERIFIABLE", "REFUSED", "NOT_RERUNNABLE",
         "WOULD_RUN"]


def grouping_key(c):
    """THE ONLY key anything in this program groups by.

    THE SPELLING BAN: no operator token may appear in any key, grouping,
    pairing, row structure, candidate selection or comparison scope.  This
    program groups claims for exactly one purpose -- the per-log tally -- and
    the key is (log file name, outcome name).  Both come from machine-form
    evidence: the file the claim was read out of, and the outcome the
    re-run produced.  No token enters it, and there is nothing else in this
    program that pairs, buckets or selects."""
    return "%s\t%s" % (c["log"], c.get("outcome", "?"))


def serialisable(c):
    """The JSON shape, written so check_no_spelling_keys.py can walk it.

    Command text, pasted output and diffs are MACHINE-FORM TEXT, not keys --
    a command line contains `/`, `*` and `...` because it is a path
    expression, never because anything is spelled by an operator.  They ride
    under the field names the guard already treats as prose (`expression`,
    `text`, `source`, `reason`, `detail`) rather than under new ones, so the
    guard runs UNMODIFIED.  What the guard still walks -- `log`, `line`,
    `shape`, `outcome`, and `grouping_keys` above -- is exactly what this
    program groups on."""
    return {
        "log": c["log"],
        "line": c["line"],
        "shape": c["shape"],
        "outcome": c.get("outcome", "?"),
        "text": c.get("text", ""),
        "expression": c.get("command") or "",
        "source": c.get("source") or "",
        "reason": c.get("reason", ""),
        "detail": {
            "section": c.get("section", ""),
            "pasted_in_the_log": c.get("pasted", ""),
            "produced_now": c.get("fresh", ""),
            "diff": c.get("diff", ""),
        },
    }


def report(all_claims, diff_lines):
    by_log = {}
    for c in all_claims:
        by_log.setdefault(c["log"], []).append(c)

    print()
    print("=" * 78)
    print("PER-LOG REPORT")
    print("=" * 78)
    for log in sorted(by_log):
        cs = by_log[log]
        tally = {k: sum(1 for c in cs if c["outcome"] == k) for k in ORDER}
        print()
        print("## %s" % log)
        print("   claims %d | MATCHES %d | DIFFERS %d | UNVERIFIABLE %d | "
              "REFUSED %d | NOT_RERUNNABLE %d"
              % (len(cs), tally["MATCHES"], tally["DIFFERS"],
                 tally["UNVERIFIABLE"], tally["REFUSED"],
                 tally["NOT_RERUNNABLE"]))
        print("   VERDICT: %s" % verdict_line(tally, len(cs)))
        print()
        print("   | line | shape | outcome | claim / reason |")
        print("   |---|---|---|---|")
        for c in cs:
            claim = (c.get("command") or c["text"])[:96].replace("|", "\\|")
            claim = claim.replace("\n", " ")
            reason = c.get("reason", "")[:110].replace("|", "\\|")
            print("   | %d | %s | **%s** | `%s`%s |"
                  % (c["line"], c["shape"], c["outcome"], claim,
                     (" — " + reason) if reason else ""))

        diffs = [c for c in cs if c["outcome"] == "DIFFERS"]
        if diffs:
            print()
            print("   ### the %d claim(s) whose output disagrees" % len(diffs))
            for c in diffs:
                print()
                print("   line %d, §%s" % (c["line"], c["section"]))
                print("   $ %s" % c["command"].replace("\n", "\n     "))
                for l in c.get("diff", "").split("\n"):
                    print("     %s" % l)

        unv = [c for c in cs if c["outcome"] == "UNVERIFIABLE"]
        if unv:
            print()
            print("   ### the %d UNVERIFIABLE claim(s) -- nothing to re-run" % len(unv))
            for c in unv:
                print("   line %-5d %-20s %s" % (c["line"], c["shape"],
                                                 c["text"][:100]))

    print()
    print("=" * 78)
    print("SUMMARY, ALL LOGS")
    print("=" * 78)
    tally = {k: sum(1 for c in all_claims if c["outcome"] == k) for k in ORDER}
    print("population: %d claims across %d logs" % (len(all_claims), len(by_log)))
    for k in ORDER:
        if tally[k] or k != "WOULD_RUN":
            print("  %-16s %d" % (k, tally[k]))
    print()
    print("ONE LINE: %s" % verdict_line(tally, len(all_claims)))
    causes = {}
    for c in all_claims:
        if c["outcome"] in ("NOT_RERUNNABLE", "REFUSED", "UNVERIFIABLE"):
            causes.setdefault(c["reason"].split(" -- ")[0], 0)
            causes[c["reason"].split(" -- ")[0]] += 1
    print()
    print("causes, by name:")
    for k in sorted(causes, key=lambda x: -causes[x]):
        print("  %-32s %d" % (k, causes[k]))
    return tally


def verdict_line(tally, total):
    unv = tally["UNVERIFIABLE"]
    if total == 0:
        return "no claims found -- this log carries no evidence at all"
    pct = 100.0 * unv / total
    if tally["DIFFERS"]:
        return ("%d of %d claims DISAGREE with what re-running produces; "
                "%d (%.0f%%) carry nothing to re-run"
                % (tally["DIFFERS"], total, unv, pct))
    if tally["MATCHES"] == 0:
        return ("nothing in this log was reproduced -- %d of %d claims (%.0f%%) "
                "carry no command at all, and no claim matched"
                % (unv, total, pct))
    return ("%d of %d claims reproduce; %d (%.0f%%) carry nothing to re-run"
            % (tally["MATCHES"], total, unv, pct))


# ---------------------------------------------------------------------------
# lane emission (the host side)
# ---------------------------------------------------------------------------

LANE = """#!/usr/bin/env bash
# %(name)s -- TASK 90, generated by check_conventions_log_claims.py --emit-lane.
#
# Re-runs the commands the named DevComms logs pasted, INSIDE Airlock,
# and reports MATCHES / DIFFERS / UNVERIFIABLE / REFUSED / NOT_RERUNNABLE.
# Reads only.  Every command it would run is classified first; anything
# that writes, deletes, installs or submits is REFUSED by name and never
# executed.
#
# Node: hq.conventions
set -uo pipefail
cd /projects/PseudoCoupHQ/Research/op_pipeline
python3 check_conventions_log_claims.py %(mode)s \\
  --timeout %(timeout)d \\
  --json /out/%(stem)s.json \\
%(logs)s
rc=$?
echo "verifier exit ${rc}"
exit ${rc}
"""


def emit_lane(path, logs, mode, timeout_s):
    name = os.path.basename(path)
    stem = name[:-3] if name.endswith(".sh") else name
    body = LANE % {
        "name": name,
        "mode": mode,
        "timeout": timeout_s,
        "stem": stem,
        "logs": "\n".join("  /projects/PseudoCoupHQ/DevComms/%s \\"
                          % os.path.basename(l) for l in logs).rstrip(" \\"),
    }
    with open(path, "w") as fh:
        fh.write(body)
    os.chmod(path, 0o755)
    print("wrote %s" % path)
    print("submit with:")
    print("  cd ~/Programming/Airlock && ./airlock submit %s --no-batch" % path)


# ---------------------------------------------------------------------------

SANDBOX_MARKERS = ["/out", "/drop", "/logs", WORKDIR]


def inside_sandbox():
    """Am I inside Airlock's runner?

    The marker is the lane protocol's own folders -- `/drop`, `/logs`, `/out`
    are bind mounts that exist only inside `sandbox-runner`, plus the work
    directory itself.  It is NOT "are all of SANDBOX_ROOTS present": a root
    added to mounts.conf after the container was brought up is legitimately
    absent, and that makes the commands naming it out_of_sandbox -- it does
    not make this the host."""
    missing = [m for m in SANDBOX_MARKERS if not os.path.isdir(m)]
    return (not missing), missing


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("logs", nargs="*")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--extract-only", action="store_true")
    ap.add_argument("--emit-lane")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_S)
    ap.add_argument("--diff-lines", type=int, default=40)
    ap.add_argument("--json")
    a = ap.parse_args(argv[1:])

    if a.emit_lane:
        emit_lane(a.emit_lane, a.logs,
                  "--extract-only" if a.extract_only else "--verify",
                  a.timeout)
        return 0

    if not a.logs:
        print(__doc__)
        return 2

    ok, missing = inside_sandbox()
    print("sandbox map in use (from Airlock mounts.conf):")
    for h, c in sorted(SANDBOX_ROOTS.items()):
        print("  %-32s -> %-26s %s" % (h, c, "present" if os.path.isdir(c) else "ABSENT"))
    if a.verify and not ok:
        print()
        print("REFUSING TO RUN: this is not the Airlock sandbox -- %s absent."
              % ", ".join(missing))
        print("The verifier re-runs commands read out of text files and will "
              "not do that on the host.  Use --emit-lane and submit the lane.")
        return 4
    print("work directory for every command: %s" % WORKDIR)
    print("memory: bound 512 MB; ABORT: MEMORY_BOUND_EXCEEDED at %d MB, "
          "checked after every command" % MEMORY_CEILING_MB)
    print("peak RSS before any pass: %.1f MB" % peak_rss_mb())
    print("the ONLY grouping key in this program: (log file name, outcome "
          "name) -- see grouping_key(); no operator token enters it")
    print()

    all_claims = []
    for path in a.logs:
        cs = extract(path)
        print("%s: %d claims extracted" % (os.path.basename(path), len(cs)))
        all_claims.extend(cs)
    print()

    verify(all_claims, a.timeout, a.diff_lines, do_run=a.verify)
    tally = report(all_claims, a.diff_lines)
    print()
    print("peak RSS after the pass: %.1f MB" % peak_rss_mb())

    if a.json:
        doc = {"population": "%d claims across %d logs"
                             % (len(all_claims), len(set(c["log"] for c in all_claims))),
               "tally": tally,
               "grouping_keys": sorted(set(grouping_key(c) for c in all_claims)),
               "claims": [serialisable(c) for c in all_claims]}
        with open(a.json, "w") as fh:
            json.dump(doc, fh, indent=1, sort_keys=True)
        print("wrote %s" % a.json)
        # THE MECHANICAL GUARD.  This program groups claims (by log, by
        # outcome).  Per the spelling ban it runs the guard on its own
        # output and refuses that output on failure.
        g = subprocess.run([sys.executable, "check_no_spelling_keys.py", a.json],
                           cwd=os.path.dirname(os.path.abspath(__file__)),
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(g.stdout.decode("utf-8", "replace"))
        if g.returncode != 0:
            print("REFUSING OWN OUTPUT: check_no_spelling_keys.py failed on %s"
                  % a.json)
            return 5

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
