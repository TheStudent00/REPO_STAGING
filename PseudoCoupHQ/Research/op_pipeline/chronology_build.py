#!/usr/bin/env python3
"""chronology_build.py -- SUPERSEDED 2026-09-04 BY TASK 86.  Kept on disk
as the record of what it was, and no longer read by the python page.

WHY.  Line 163 below runs `git log --grep=banked -i` and line 155 matches
`round\\s+(\\d+)\\s+bank`, so a step of the chronology existed because a
person had written a word into a commit message.  That made the rounds
the mechanism and version control only its substrate, which is the
opposite of what was asked for.  the owner, 2026-09-04: "i said vcs
chronology. i dont want you to have any say in how it updates... because
i cant trust you."

WHAT REPLACED IT.  `dashboard_ouro.py` reads `git log` itself, at the
moment the page is drawn: every commit is a moment, nothing is filtered,
nothing is grouped, and no message is read to decide anything.  There is
no build step left to run and no `chronology.json` to keep in step with
the repository.  See the CORE's rule "The chronology is version control,
and nothing curates it", and `DevComms/log_192_task86_vcs_chronology.md`.

`chronology.json`, this program's product, also stays on disk.  The
JavaScript route's `dashboard_pane6.js` still reads it; that route was
not touched by task 86.

--- what it was, unchanged below this line -----------------------------

chronology_build.py -- the line's progress, read off the version control
history instead of off memory.

Node: hq.research.compiler_graph.dashboard, the `chronology` method
(Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_10_dashboard/
CORE_0_3_5_10_dashboard.md).  the owner, 2026-09-03: "i would like the dashboard to
also have a chronology based on vcs so i can step through the history to see
progress."

WHAT IT DOES.  It walks two scales of the repository's own history:

  ROUND SCALE   every commit whose message says a round was banked
                (`git log --grep=banked -i`), one step per round.
  DAY SCALE     the last commit of every day since 2026-07-31.

At each step it asks git for the stat artifacts AS THEY WERE AT THAT COMMIT
(`git cat-file` on the blob the commit's tree names) and RECOMPUTES the stats
pane's numbers from them.  No number is ever copied out of a log or a commit
message while an artifact can be recomputed.  Where the artifact was never
tracked -- `the_pool1.json` is 18 MB and answers `git ls-files` with nothing,
so round 9 cannot be recomputed -- the bank message's own count line is parsed
instead and that number is marked `testimony`.  The `source` field is PER
NUMBER, not per step: a step can be recomputed for its unit counts and
testimony for its pool.

HOW THE ARTIFACTS ARE FOUND.  Not from a hand-written table.  Each commit's
tree is listed and the HIGHEST GENERATION present of each family is taken:

    canon<N>_wrapped_<lang>.json + canon<N>_interp.json
                                 + canon<N>_regen_store/*.json   the corpus
    term<N>_store/*.json  or  layer4<x>_terms_*.json (+ interp, + regen store)
                                                                 the terms
    the_pool<N>.json                                             the pool
    the_families<N>.json                                         the families
    name_census<N>.json                                          the census

That rule agrees with what the bank messages name (round 13's message says
"term/pool/census rebuilt as term65/pool5/census6"; the rule picks exactly
those), and it keeps working for generations not yet written.

HOW THE NUMBERS ARE RECOMPUTED.

  arch-units extracted   sum of the `tally` object at the head of every
                         corpus file (the same 4 KB head read the browser
                         loader makes); per language from the file name.
  wrapped and proved     the tally's WRAPPED_TEXT_PROVED entry.
  term states            one row per unit, partitioned by the two gate
                         routes.  The two artifact generations spell the
                         routes differently and are read accordingly:
                           term<N>_store: term_state / verdict_ship.outcome
                                          / verdict_source.outcome
                           layer4<x>:     term_built / gate_ship_verdict
                                          / gate_textorder_verdict
                         proved if either route proved; withdrawn if either
                         disproved; undecided if a term was built and neither
                         did; no term if none was built.
  distinct computations  the pool file's `summary.entries`, and the rest of
                         the summary beside it.
  dominant families      the length of the families file's `families`.
  census producers       the length of the census file's `entries`.

RUNNING IT.  It is a step of every bank task from now on -- run it after the
round's artifacts are committed and before the posterity message is written,
so the chronology grows by itself:

    /tmp/reconnect_venv/bin/python3 \
        ~/Programming/PseudoCoupHQ/Research/op_pipeline/chronology_build.py --append

  --append   adds only steps chronology.json does not already carry, and is
             idempotent: running it twice changes nothing.  This is the mode
             a bank task calls.
  (no flag)  rebuilds every step from scratch.
  --print    writes the table to standard output as well.

OUTPUT.  `chronology.json` beside this file, tracked, small (one record per
step, no unit bodies).  Read by `dashboard_pane6.js`, which draws pane 6.

THE SPELLING BAN.  This program groups nothing by an operator token: its
steps are keyed by commit hash, its numbers by artifact family.  The emitted
`chronology.json` is walked by the UNMODIFIED `check_no_spelling_keys.py` and
this program REFUSES ITS OWN OUTPUT when the guard fails.
"""

import argparse
import collections
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
PREFIX = "Research/op_pipeline/"
OUT = os.path.join(HERE, "chronology.json")
GUARD = os.path.join(HERE, "check_no_spelling_keys.py")

FIRST_DAY = "2026-07-31"
LANGS = ["c", "cpp", "go", "rust", "swift"]


# ------------------------------------------------------------------
# 0.  git, spoken to once per question
# ------------------------------------------------------------------

def git(*args):
    return subprocess.run(
        ["git"] + list(args), cwd=REPO,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout.decode("utf-8", "replace")


class Blobs(object):
    """one long-lived `git cat-file --batch` process, so a step that reuses a
    blob another step already named costs one write and one read."""

    def __init__(self):
        self.proc = subprocess.Popen(
            ["git", "cat-file", "--batch"], cwd=REPO,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        )

    def read(self, sha):
        self.proc.stdin.write((sha + "\n").encode())
        self.proc.stdin.flush()
        header = self.proc.stdout.readline().decode().strip()
        parts = header.split()
        if len(parts) != 3:
            raise RuntimeError("git cat-file said: " + header)
        n = int(parts[2])
        buf = b""
        while len(buf) < n:
            buf += self.proc.stdout.read(n - len(buf))
        self.proc.stdout.read(1)
        return buf

    def json(self, sha):
        return json.loads(self.read(sha).decode("utf-8", "replace"))

    def close(self):
        try:
            self.proc.stdin.close()
            self.proc.wait(timeout=10)
        except Exception:
            pass


# ------------------------------------------------------------------
# 1.  the steps: the banking commits, and the last commit of each day
# ------------------------------------------------------------------

ROUND_RE = re.compile(r"round\s+(\d+)\s+bank", re.I)


def bank_commits():
    """`git log --grep=banked -i`, then keep only the messages that name a
    round.  Two commits carry the same round-4 text and two carry the same
    round-10 text (the daemon committed the same file twice); the EARLIEST
    commit of each round is the step, and the duplicate is recorded."""
    raw = git("log", "--grep=banked", "-i", "--format=%H%x01%cI%x01%B%x02")
    out = []
    for rec in raw.split("\x02"):
        rec = rec.strip("\n")
        if not rec.strip():
            continue
        sha, date, body = rec.split("\x01", 2)
        m = ROUND_RE.search(body)
        out.append({
            "commit": sha, "date": date, "message": body.strip(),
            "round": int(m.group(1)) if m else None,
        })
    by_round = {}
    skipped = []
    for r in out:
        if r["round"] is None:
            skipped.append(r)
            continue
        prev = by_round.get(r["round"])
        if prev is None or r["date"] < prev["date"]:
            if prev is not None:
                prev["duplicate_of_round"] = True
            by_round[r["round"]] = r
        else:
            r["duplicate_of_round"] = True
    return [by_round[k] for k in sorted(by_round)], skipped, out


def day_commits():
    raw = git("log", "--format=%cI%x01%H", "--since=" + FIRST_DAY + " 00:00:00")
    seen = {}
    for line in raw.splitlines():
        if "\x01" not in line:
            continue
        date, sha = line.split("\x01", 1)
        day = date[:10]
        if day < FIRST_DAY:
            continue
        if day not in seen:            # git log is newest first, so this is
            seen[day] = (date, sha)    # the LAST commit of that day
    return [{"commit": v[1], "date": v[0], "day": k, "round": None,
             "message": ""} for k, v in sorted(seen.items())]


# ------------------------------------------------------------------
# 2.  the artifact set at one commit, discovered from the tree
# ------------------------------------------------------------------

GEN = {
    "wrapped": re.compile(r"^canon(\d+)_wrapped_([a-z]+)\.json$"),
    "interp": re.compile(r"^canon(\d+)_interp\.json$"),
    "regen": re.compile(r"^canon(\d+)_regen_store/op_units2_([a-z]+)_c\d+\.json$"),
    "pool": re.compile(r"^the_pool(\d+)\.json$"),
    "families": re.compile(r"^the_families(\d+)\.json$"),
    "census": re.compile(r"^name_census(\d*)\.json$"),
    "termstore": re.compile(r"^term(\d+)_store/.+\.json$"),
    "l4terms": re.compile(r"^layer4([a-z]*)_terms_([a-z]+)\.json$"),
    "l4interp": re.compile(r"^layer4([a-z]*)_interp\.json$"),
    "l4regen": re.compile(r"^layer4([a-z]*)_regen_store/.+\.json$"),
}


def tree(commit):
    """path (relative to Research/op_pipeline) -> blob sha, for one commit."""
    raw = git("ls-tree", "-r", commit, "--", PREFIX)
    out = {}
    for line in raw.splitlines():
        meta, path = line.split("\t", 1)
        bits = meta.split()
        if bits[1] != "blob":
            continue
        if path.startswith(PREFIX):
            out[path[len(PREFIX):]] = bits[2]
    return out


def rank(token):
    """generation order: '' < 'a' < 'b' < 'c' for the layer4 letters, and
    numeric for everything else."""
    if token.isdigit():
        return (1, int(token), "")
    return (0, 0, token)


def pick(paths, which):
    """the highest generation of one family present at this commit."""
    rx = GEN[which]
    best = None
    hits = collections.defaultdict(list)
    for p in paths:
        m = rx.match(p)
        if m:
            hits[m.group(1)].append(p)
    for gen in hits:
        if best is None or rank(gen) > rank(best):
            best = gen
    if best is None:
        return None, []
    return best, sorted(hits[best])


def artifacts_at(paths):
    a = {}
    for which in ["wrapped", "interp", "regen", "pool", "families", "census",
                  "termstore", "l4terms", "l4interp", "l4regen"]:
        gen, files = pick(paths, which)
        a[which] = {"generation": gen, "files": files}
    # the term family: a term<N>_store supersedes the layer4 generation.
    if a["termstore"]["generation"] is not None:
        a["terms"] = {
            "kind": "term_store",
            "generation": a["termstore"]["generation"],
            "files": a["termstore"]["files"],
        }
    elif a["l4terms"]["generation"] is not None:
        gen = a["l4terms"]["generation"]
        files = list(a["l4terms"]["files"])
        for which in ["l4interp", "l4regen"]:
            if a[which]["generation"] == gen:
                files += a[which]["files"]
        a["terms"] = {"kind": "layer4", "generation": gen,
                      "files": sorted(files)}
    else:
        a["terms"] = {"kind": None, "generation": None, "files": []}
    # the corpus family: the wrapped generation plus its own interp and shards.
    gen = a["wrapped"]["generation"]
    files = list(a["wrapped"]["files"])
    for which in ["interp", "regen"]:
        if a[which]["generation"] == gen:
            files += a[which]["files"]
    a["corpus"] = {"generation": gen, "files": sorted(files)}
    for k in ["wrapped", "interp", "regen", "termstore", "l4terms",
              "l4interp", "l4regen"]:
        del a[k]
    return a


# ------------------------------------------------------------------
# 3.  the recomputation
# ------------------------------------------------------------------

LANG_OF_SHARD = re.compile(r"op_units2_([a-z]+)_c\d+\.json$")
LANG_OF_WRAPPED = re.compile(r"^canon\d+_wrapped_([a-z]+)\.json$")


def carve_tally(text):
    """the value of "tally" out of the head of a corpus file, by balanced
    brace scan -- the python twin of the browser loader's carveObject."""
    i = text.find('"tally"')
    if i < 0:
        return None
    i = text.find("{", i)
    if i < 0:
        return None
    depth = 0
    for j in range(i, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[i:j + 1])
                except ValueError:
                    return None
    return None


def corpus_numbers(blobs, paths, files):
    per_lang = {}
    for name in files:
        m = LANG_OF_SHARD.search(name) or LANG_OF_WRAPPED.match(name)
        text = blobs.read(paths[name])[:8192].decode("utf-8", "replace")
        tally = carve_tally(text)
        if tally is None:
            continue
        if m:
            lang = m.group(1)
            rows = [(lang, tally)]
        else:
            # canon<N>_interp.json: several languages in one file, and the
            # tally does not split them.  Counted as the interpreter
            # population, which is how every bank message states it.
            rows = [("interpreter", tally)]
        for lang, t in rows:
            row = per_lang.setdefault(lang, {"units": 0, "proved": 0})
            row["units"] += sum(t.values())
            row["proved"] += t.get("WRAPPED_TEXT_PROVED", 0)
    units = sum(r["units"] for r in per_lang.values())
    proved = sum(r["proved"] for r in per_lang.values())
    return per_lang, units, proved


def term_state(row, kind):
    if kind == "term_store":
        if row.get("term_state") != "TERM":
            return "no term"
        outs = []
        for key in ["verdict_ship", "verdict_source"]:
            v = row.get(key)
            if isinstance(v, dict):
                outs.append(v.get("outcome"))
            elif v:
                outs.append(v)
        if row.get("proved") is True:
            return "proved"
    else:
        if not row.get("term_built"):
            return "no term"
        outs = [row.get("gate_ship_verdict"), row.get("gate_textorder_verdict")]
    if "PROVED_EQUAL" in outs:
        return "proved"
    if "DISPROVED" in outs:
        return "withdrawn"
    return "undecided"


def term_numbers(blobs, paths, terms):
    if not terms["files"]:
        return None
    counts = collections.Counter()
    for name in terms["files"]:
        doc = blobs.json(paths[name])
        u = doc.get("units", doc)
        rows = list(u.values()) if isinstance(u, dict) else u
        for r in rows:
            if isinstance(r, dict):
                counts[term_state(r, terms["kind"])] += 1
    return {
        "proved": counts["proved"],
        "withdrawn": counts["withdrawn"],
        "undecided": counts["undecided"],
        "no term": counts["no term"],
        "rows": sum(counts.values()),
    }


def recompute(blobs, paths, arts):
    n = {}
    src = {}
    per_lang, units, proved = ({}, None, None)
    if arts["corpus"]["files"]:
        per_lang, units, proved = corpus_numbers(
            blobs, paths, arts["corpus"]["files"])
        n["units"] = units
        n["wrapped_and_proved"] = proved
        src["units"] = "recomputed"
        src["wrapped_and_proved"] = "recomputed"
    t = term_numbers(blobs, paths, arts["terms"])
    if t:
        n["proved_terms"] = t["proved"]
        n["withdrawn_terms"] = t["withdrawn"]
        n["undecided_terms"] = t["undecided"]
        n["no_term"] = t["no term"]
        for k in ["proved_terms", "withdrawn_terms", "undecided_terms",
                  "no_term"]:
            src[k] = "recomputed"
    if arts["pool"]["files"]:
        summary = blobs.json(paths[arts["pool"]["files"][0]]).get("summary", {})
        members = summary.get("members")
        if members is None:
            # the pool2 / pool3 generations state the member population as a
            # split by arrival population and never as one number.
            by_arrival = summary.get("units_by_arrival_population")
            if isinstance(by_arrival, dict):
                members = sum(v for v in by_arrival.values()
                              if isinstance(v, int))
        n["pool_entries"] = summary.get("entries")
        n["pool_members"] = members
        n["pool_multi_language"] = summary.get(
            "entries_spanning_more_than_one_language")
        for k in ["pool_entries", "pool_members", "pool_multi_language"]:
            if n.get(k) is not None:
                src[k] = "recomputed"
    if arts["families"]["files"]:
        fam = blobs.json(paths[arts["families"]["files"][0]])
        f = fam.get("families", fam)
        n["families"] = len(f)
        src["families"] = "recomputed"
    if arts["census"]["files"]:
        cen = blobs.json(paths[arts["census"]["files"][0]])
        # the ungenerationed name_census.json counts the same thing under a
        # different name: it has no `entries` list, it has a count.
        if isinstance(cen.get("entries"), list):
            n["census_producers"] = len(cen["entries"])
        elif isinstance(cen.get("distinct_unmodelled_names"), int):
            n["census_producers"] = cen["distinct_unmodelled_names"]
        if n.get("census_producers") is not None:
            src["census_producers"] = "recomputed"
    return n, src, per_lang


# ------------------------------------------------------------------
# 4.  testimony: the bank message's own count line, parsed, for the steps
#     whose artifacts were never tracked
# ------------------------------------------------------------------

TESTIMONY = [
    # (number, pattern, group)  -- each pattern is anchored on words the bank
    # message itself uses, so what is being read is visible in the message.
    ("pool_entries", r"([\d,]+)\s+entries over", 1),
    ("pool_members", r"entries over\s+(?:the full\s+)?([\d,]+)[- ]member", 1),
    ("pool_members", r"entries over\s+([\d,]+)\s+member units", 1),
    ("units", r"wrapped\s+([\d,]+)\s+units", 1),
    ("units", r"transcribed\s+([\d,]+)\s+to ledger terms", 1),
    ("proved_terms", r"([\d,]+)\s+proved\b", 1),
]


def testimony_numbers(message):
    n = {}
    src = {}
    for name, pat, g in TESTIMONY:
        if name in n:
            continue
        m = re.search(pat, message, re.I)
        if m:
            n[name] = int(m.group(g).replace(",", ""))
            src[name] = "testimony"
    return n, src


# ------------------------------------------------------------------
# 5.  the round's logs, found in the tree rather than listed by hand
# ------------------------------------------------------------------

def logs_of(step, paths_all):
    """the DevComms logs named in the bank message, plus every log added by
    the commit itself."""
    named = sorted(set(re.findall(r"log_(\d{3})", step.get("message") or "")))
    files = git("show", "--name-only", "--format=", step["commit"]).splitlines()
    added = sorted(set(
        p for p in files if p.startswith("DevComms/log_") and p.endswith(".md")))
    by_number = []
    for num in named:
        hit = [p for p in git("ls-tree", "-r", "--name-only", step["commit"],
                              "--", "DevComms/").splitlines()
               if p.startswith("DevComms/log_" + num + "_")]
        by_number.extend(hit)
    return sorted(set(by_number + added))


# ------------------------------------------------------------------
# 6.  build
# ------------------------------------------------------------------

def build(steps, blobs, cache):
    out = []
    for step in steps:
        paths = tree(step["commit"])
        arts = artifacts_at(paths)
        fingerprint = hashlib.sha1(("|".join(
            sorted(paths[f] for group in arts.values() for f in group["files"])
        )).encode()).hexdigest()
        if fingerprint in cache:
            n, src, per_lang = cache[fingerprint]
            n, src, per_lang = dict(n), dict(src), dict(per_lang)
        else:
            n, src, per_lang = recompute(blobs, paths, arts)
            cache[fingerprint] = (n, src, per_lang)
        if step.get("message"):
            tn, tsrc = testimony_numbers(step["message"])
            for k, v in tn.items():
                if k not in n or n[k] is None:
                    n[k] = v
                    src[k] = tsrc[k]
        rec = {
            "commit": step["commit"],
            "date": step["date"],
            "day": step["date"][:10],
            "round": step.get("round"),
            "scale": step["scale"],
            "numbers": n,
            "source": src,
            "per_lang": per_lang,
            "artifacts": {k: {"generation": v["generation"],
                              "file_count": len(v["files"]),
                              "example": (v["files"][0] if v["files"] else None)}
                          for k, v in arts.items()},
            "bank_message": step.get("message") or "",
            "logs": logs_of(step, paths) if step.get("message") else [],
            "artifact_fingerprint": fingerprint,
        }
        out.append(rec)
        sys.stderr.write("  %s %s %-8s %s\n" % (
            rec["day"], rec["commit"][:9], rec["scale"],
            json.dumps(rec["numbers"], sort_keys=True)[:110]))
    return out


def guard(path):
    r = subprocess.run(
        [sys.executable, GUARD, path],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    text = r.stdout.decode("utf-8", "replace")
    return r.returncode, text


COLS = [("units", "extracted"), ("pool_entries", "distinct"),
        ("families", "dominant"), ("proved_terms", "proved terms")]


def table(records):
    lines = []
    head = "%-6s %-10s %-10s %10s %10s %9s %12s  %s" % (
        "round", "date", "commit", "extracted", "distinct", "dominant",
        "proved terms", "source")
    lines.append(head)
    lines.append("-" * len(head))
    for r in records:
        vals = []
        for key, _ in COLS:
            v = r["numbers"].get(key)
            vals.append("-" if v is None else "{:,}".format(v))
        # the tag reads EVERY number of the step, not only the four columns:
        # a step can carry a census count and none of these four.
        srcs = sorted(set(r["source"].values()))
        counts = collections.Counter(r["source"].values())
        if not srcs:
            tag = "no artifact tracked"
        elif len(srcs) == 1:
            tag = "%s (%d numbers)" % (srcs[0], counts[srcs[0]])
        else:
            tag = "mixed: " + ", ".join(
                "%s=%s" % (COLS[i][1], r["source"].get(COLS[i][0], "-"))
                for i in range(len(COLS)) if r["source"].get(COLS[i][0]))
        lines.append("%-6s %-10s %-10s %10s %10s %9s %12s  %s" % (
            r["round"] if r["round"] else ("day" if r["scale"] == "day" else ""),
            r["day"], r["commit"][:9], vals[0], vals[1], vals[2], vals[3], tag))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--append", action="store_true",
                    help="add only steps chronology.json lacks (idempotent); "
                         "this is the mode a bank task runs")
    ap.add_argument("--print", dest="show", action="store_true")
    args = ap.parse_args()

    banks, skipped, all_bank_matches = bank_commits()
    days = day_commits()
    for b in banks:
        b["scale"] = "round"
    bank_shas = set(b["commit"] for b in banks)
    steps = list(banks)
    for d in days:
        if d["commit"] in bank_shas:
            continue
        d["scale"] = "day"
        steps.append(d)
    steps.sort(key=lambda s: s["date"])

    have = {}
    if args.append and os.path.exists(OUT):
        old = json.load(open(OUT))
        # A DAY STEP IS THE LAST COMMIT OF ITS DAY, and while the day is still
        # running that commit moves -- the daemon commits every 30 s.  So a
        # day already carried is REPLACED by its newest last-commit rather
        # than added beside it; that is what makes --append idempotent and
        # keeps today's step from multiplying once per run.
        last_of_day = dict((s["date"][:10], s["commit"])
                           for s in steps if s["scale"] == "day")
        for r in old.get("steps", []):
            if r.get("scale") == "day":
                now = last_of_day.get(r.get("day"))
                if now is not None and now != r.get("commit"):
                    continue        # that day's last commit has moved on
            have[r["commit"]] = r
        steps = [s for s in steps if s["commit"] not in have]
        sys.stderr.write("append: %d step(s) to build (%d carried forward "
                         "unchanged)\n" % (len(steps), len(have)))

    blobs = Blobs()
    cache = {}
    try:
        records = build(steps, blobs, cache)
    finally:
        blobs.close()

    records = sorted(list(have.values()) + records, key=lambda r: r["date"])

    doc = {
        "meta": {
            "node": "hq.research.compiler_graph.dashboard",
            "generated_by": "chronology_build.py",
            "built_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "repo": "PseudoCoupHQ",
            "head": git("rev-parse", "HEAD").strip(),
            "commits_in_history": int(git("rev-list", "--count", "HEAD") or 0),
            "first_day": FIRST_DAY,
            "population": "every commit whose message says a round was banked, "
                          "plus the last commit of every day since " + FIRST_DAY,
            "rule": "every number is recomputed from the artifact blob the "
                    "commit's tree names; a number that cannot be is read off "
                    "the bank message's own count line and marked testimony",
            "bank_matches": len(all_bank_matches),
            "bank_steps": len(banks),
            "bank_matches_naming_no_round": [
                {"commit": s["commit"], "date": s["date"],
                 "first_line": s["message"].splitlines()[0][:120]}
                for s in skipped],
        },
        "steps": records,
    }
    with open(OUT, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)

    code, text = guard(OUT)
    sys.stderr.write("\n--- check_no_spelling_keys.py " + OUT + " ---\n")
    sys.stderr.write(text)
    if code != 0:
        os.unlink(OUT)
        sys.stderr.write("REFUSED: the guard failed; chronology.json removed\n")
        return 2

    rec = doc["steps"]
    n_rec = sum(1 for r in rec if "recomputed" in r["source"].values())
    n_tes = sum(1 for r in rec if "testimony" in r["source"].values())
    n_non = sum(1 for r in rec if not r["source"])
    sys.stderr.write(
        "\nwrote %s  (%d steps: %d with a recomputed number, %d with a "
        "testimony number, %d with no tracked artifact; %d bytes)\n" % (
            OUT, len(rec), n_rec, n_tes, n_non, os.path.getsize(OUT)))
    if args.show:
        print(table(rec))
    return 0


if __name__ == "__main__":
    sys.exit(main())
