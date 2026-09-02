#!/usr/bin/env python3
"""audit_altered_testimony.py -- how much stored testimony the
`lane_gen.py` substitution altered, measured record by record.

THE DEFECT (restated so this file stands alone)
-----------------------------------------------
`lane_gen.py`'s embedded driver stores each compiler diagnostic after
`text.replace("|", "/")` (lines 365, 368, 371, 373) and each DWARF
attribute after `text.replace("|", "/")` and `text.replace(";", ",")`
(line 192, `clean`).  Wherever a compiler quoted `|` or `;`, the store
holds a character the compiler did not emit.

HOW A RECORD IS JUDGED, AND WHY IT IS NOT JUDGED BY THE SPELLING
-----------------------------------------------------------------
Nothing here selects, groups, keys or pairs records by an operator
token.  The population is EVERY stored string that holds compiler
words, in every `op_units_*.json` on disk.  Two machine-form tests
decide each record:

  TEST 1, on the stored text alone -- is there a `/` in TOKEN
  POSITION?  A `/` is `path-like` when a word character sits on both
  sides of it in the way a file path puts one there
  (`/work/op_c/u/n9/unit.c`).  Anything else -- a `/` with a space, a
  quote, a backtick, a bracket or another `/` beside it -- is in
  token position, which is where a substituted character lands.

  TEST 2, on the probe's OWN authored source text (the manifest
  record of what was handed to the compiler; the generator-provenance
  exemption in check_no_spelling_keys.py covers reading it): does that
  source contain a `|` character at all?
     * source has `|`, and no `/`  -> ALTERED.  The compiler was
       quoting the source, and the character it quoted cannot have
       been a `/` because the source had none.
     * source has no `|`           -> GENUINE.  Nothing could have
       been substituted; the `/` is the compiler's own.
     * source has BOTH             -> UNDECIDABLE per occurrence.
       Counted separately and never guessed.

DETECTION LIMITS, STATED HONESTLY
---------------------------------
 1. A diagnostic that quoted `|` but placed it where a `/` is also
    plausible cannot be told apart by test 1 alone; test 2 rescues
    those whose source has no `/`, and the UNDECIDABLE bucket holds
    the rest.  The bucket is counted, not hidden.
 2. The reconstruction this program offers is a SUSPECTED original,
    not the original.  The raw compiler output is not retained
    anywhere: the driver writes only the folded record, and the
    Airlock lane log holds the banner and the tally.  Verified:
    `grep -c "" logs/20260825T055504Z__op_rust.sh.log` -> 26 lines,
    and `grep -n "implementation"` on it -> no match.  So no
    unaltered copy exists to compare against; re-capture is the only
    route to true verbatim text.
 3. The `;` -> `,` substitution touched DWARF attribute text only
    (`clean` is called from the DWARF reader, nowhere else -- verified
    by `grep -n "clean(" lane_gen.py`, which shows the definition at
    190 and two call sites at 263/264).  It is audited separately and
    its detection is weaker, because a comma is common in ordinary
    attribute text.
 4. Truncation at 200 characters is NOT alteration and is not
    counted here: it removes tail, it does not change words.

OUTPUT
------
  audit_altered_testimony.json   per-record findings and the counts
  audit_altered_testimony.md     the same counts as a reading table

Neither output is grouping-shaped, and both are checked with
check_no_spelling_keys.py.
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

WORDISH = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
              "0123456789_.-")


def token_slashes(text):
    """indexes of every `/` that is NOT sitting inside a file path.

    A path puts a word character on the RIGHT of every separator --
    `/work/op_c/u/n9/unit.c` -- including the leading one at the start
    of an absolute path, where nothing sits on the left.  So the test
    is on the right neighbour: a `/` followed by a word character is
    path-like.  Everything else -- `/` beside a space, a quote, a
    backtick, an `=`, a bracket, or another `/` -- is in token
    position, which is where a substituted character lands.

    THE LIMIT THIS LEAVES (stated, not hidden): a substituted bar that
    happened to be followed by a word character and preceded by a
    space cannot be told from the start of an absolute path.  Such an
    occurrence is invisible to this detector.
    """
    got = []
    for i, c in enumerate(text):
        if c != "/":
            continue
        right = text[i + 1] if i + 1 < len(text) else ""
        if right in WORDISH:
            continue
        got.append(i)
    return got


def manifest_sources():
    """probe id -> its authored source text, per language file stem."""
    src = {}
    for path in sorted(glob.glob(os.path.join(HERE, "probe_manifest_*.json"))):
        lang = os.path.basename(path)[len("probe_manifest_"):-len(".json")]
        doc = json.load(open(path))
        table = {}
        for k, rec in doc.get("probes", {}).items():
            table[str(k)] = rec.get("source", "")
        src[lang] = table
    return src


def stem(fname):
    return os.path.basename(fname)[len("op_units_"):-len(".json")]


def source_for(sources, lang, key, rec):
    """the adjudication scope: the probe's OWN EXPRESSION.

    The scope must be the expression, not the whole probe file.  A
    probe file carries includes, comments and a `main`, and any of
    those can hold a `/` that has nothing to do with the operand the
    compiler was complaining about; adjudicating against the whole
    file therefore makes every record UNDECIDABLE and measures
    nothing.  The expression is the text the diagnostic quotes.

    The whole-file text is still read, and returned beside it, so the
    weaker second view can be reported rather than assumed.
    """
    tbl = sources.get(lang)
    if tbl is None and lang.startswith("asg_"):
        tbl = sources.get(lang[len("asg_"):])
    whole = tbl.get(key, "") if tbl else ""
    expr = (rec.get("meta") or {}).get("expression")
    if isinstance(expr, str) and expr:
        return expr, "probe expression", whole
    if whole:
        return whole, "whole probe file (no expression recorded)", whole
    return "", "none", whole


def diag_fields(rec):
    """(field path, text) for every stored string holding compiler words."""
    got = []
    if isinstance(rec.get("refused"), str):
        got.append(("refused", rec["refused"]))
    for slot in ("anchor", "ship"):
        side = rec.get(slot)
        if not isinstance(side, dict):
            continue
        for f in ("nosym", "buildfail", "nodwarf"):
            if isinstance(side.get(f), str):
                got.append(("%s.%s" % (slot, f), side[f]))
    return got


def dwarf_fields(rec):
    got = []
    for slot in ("anchor", "ship"):
        side = rec.get(slot)
        if not isinstance(side, dict):
            continue
        for j, row in enumerate(side.get("dwarf", []) or []):
            if not isinstance(row, dict):
                continue
            for f in ("name", "location"):
                if isinstance(row.get(f), str):
                    got.append(("%s.dwarf[%d].%s" % (slot, j, f), row[f]))
    return got


def rebuild(text, idxs):
    out = list(text)
    for i in idxs:
        out[i] = "|"
    return "".join(out)


def audit():
    sources = manifest_sources()
    # every store on disk, not only this directory's -- the consumer
    # scan showed Research/stage_asg holds its own copies.
    files = sorted(glob.glob(os.path.join(HERE, "op_units_*.json"))
                   + glob.glob(os.path.join(HERE, "..", "*",
                                            "op_units_*.json")))
    files = sorted({os.path.normpath(f) for f in files})
    per_file = []
    findings = []
    comma_notes = []
    for path in files:
        lang = stem(path)
        if lang.endswith("_verbatim"):
            continue
        doc = json.load(open(path))
        probes = doc.get("probes", {})
        row = dict(file=os.path.relpath(path, os.path.join(HERE, "..")),
                   stem=lang,
                   records=len(probes), with_diagnostic=0,
                   token_slash_records=0, altered=0, genuine=0,
                   undecidable=0, no_source=0,
                   dwarf_fields=0, dwarf_comma_records=0)
        for key in sorted(probes, key=lambda x: int(x) if x.isdigit() else x):
            rec = probes[key]
            fields = diag_fields(rec)
            if fields:
                row["with_diagnostic"] += 1
            src, how, whole = source_for(sources, lang, key, rec)
            hit_any = False
            for fname, text in fields:
                idxs = token_slashes(text)
                if not idxs:
                    continue
                hit_any = True
                has_bar = "|" in src
                has_slash = "/" in src
                if how == "none":
                    verdict = "NO_SOURCE"
                elif has_bar and not has_slash:
                    verdict = "ALTERED"
                elif has_bar and has_slash:
                    verdict = "UNDECIDABLE"
                else:
                    verdict = "GENUINE"
                findings.append(dict(
                    file=os.path.relpath(path, os.path.join(HERE, "..")),
                    stem=lang, record=key,
                    field=fname, verdict=verdict, source_seen_via=how,
                    stored=text,
                    suspected_original=(rebuild(text, idxs)
                                        if verdict == "ALTERED" else None),
                    token_slash_count=len(idxs)))
                row[{"ALTERED": "altered", "GENUINE": "genuine",
                     "UNDECIDABLE": "undecidable",
                     "NO_SOURCE": "no_source"}[verdict]] += 1
            if hit_any:
                row["token_slash_records"] += 1
            dw = dwarf_fields(rec)
            row["dwarf_fields"] += len(dw)
            if any("," in t for _, t in dw):
                row["dwarf_comma_records"] += 1
                comma_notes.append(dict(
                                        file=os.path.relpath(
                                            path, os.path.join(HERE, "..")),
                                        record=key,
                                        fields=[f for f, t in dw if "," in t]))
        per_file.append(row)

    totals = {}
    for k in ("records", "with_diagnostic", "token_slash_records", "altered",
              "genuine", "undecidable", "no_source", "dwarf_fields",
              "dwarf_comma_records"):
        totals[k] = sum(r[k] for r in per_file)
    return per_file, totals, findings, comma_notes


def main():
    per_file, totals, findings, comma_notes = audit()
    out = dict(
        what="audit of testimony altered by lane_gen.py's | -> / substitution",
        method_note=__doc__.strip(),
        per_file=per_file,
        totals=totals,
        findings=findings,
        dwarf_comma_notes=comma_notes)
    jpath = os.path.join(HERE, "audit_altered_testimony.json")
    fh = open(jpath, "w")
    json.dump(out, fh, indent=1)
    fh.close()

    lines = []
    lines.append("# audit -- testimony altered by the `|` -> `/` "
                 "substitution\n")
    lines.append("Counts are per STORE FILE, never per operator spelling.\n")
    lines.append("| store file | records | with diagnostic | records with a "
                 "token-position `/` | ALTERED fields | GENUINE fields | "
                 "UNDECIDABLE | no source |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for r in per_file:
        lines.append("| %s | %d | %d | %d | %d | %d | %d | %d |"
                     % (r["file"], r["records"], r["with_diagnostic"],
                        r["token_slash_records"], r["altered"], r["genuine"],
                        r["undecidable"], r["no_source"]))
    lines.append("| **total** | %d | %d | %d | %d | %d | %d | %d |"
                 % (totals["records"], totals["with_diagnostic"],
                    totals["token_slash_records"], totals["altered"],
                    totals["genuine"], totals["undecidable"],
                    totals["no_source"]))
    lines.append("")
    lines.append("DWARF attribute fields examined: %d; records where a DWARF "
                 "field carries a comma (the `;` -> `,` substitution's weak "
                 "fingerprint): %d.\n"
                 % (totals["dwarf_fields"], totals["dwarf_comma_records"]))
    alt = [f for f in findings if f["verdict"] == "ALTERED"]
    lines.append("## the first ten ALTERED fields, stored vs suspected\n")
    lines.append("| store file | record | field | stored | suspected original |")
    lines.append("| --- | ---: | --- | --- | --- |")
    for f in alt[:10]:
        lines.append("| %s | %s | %s | `%s` | `%s` |"
                     % (f["file"], f["record"], f["field"],
                        f["stored"][:90].replace("|", "\\|"),
                        (f["suspected_original"] or "")[:90].replace("|",
                                                                     "\\|")))
    mpath = os.path.join(HERE, "audit_altered_testimony.md")
    fh = open(mpath, "w")
    fh.write("\n".join(lines) + "\n")
    fh.close()

    for r in per_file:
        print("%-34s records %5d  diag %5d  tokenslash %5d  ALTERED %5d  "
              "GENUINE %5d  UNDEC %4d  NOSRC %4d"
              % (r["file"], r["records"], r["with_diagnostic"],
                 r["token_slash_records"], r["altered"], r["genuine"],
                 r["undecidable"], r["no_source"]))
    print("TOTALS %s" % json.dumps(totals))
    print("wrote %s\nwrote %s" % (jpath, mpath))
    return 0


if __name__ == "__main__":
    sys.exit(main())
