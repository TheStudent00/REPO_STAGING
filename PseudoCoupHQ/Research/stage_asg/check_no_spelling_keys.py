#!/usr/bin/env python3
"""check_no_spelling_keys.py -- the mechanical guard for THE SPELLING BAN.

The ban (AgentMemory, restated by the owner 2026-08-25): no operator token
may appear in ANY key, grouping, pairing, row structure, candidate
selection, or comparison scope anywhere in this line.  The token
appears exactly once per unit: as a display label on the member.

What this program does
----------------------
It reads a JSON document that some stage of the pipeline wrote, walks
every node of it, and reports every place where an operator token
appears somewhere that is NOT a per-unit display label.  It exits
nonzero and names the path of each finding.

The operator inventory is not hand-written here.  It is read from the
probe manifests in this directory (`probe_manifest_*.json`), taking the
`operator` field of every probe.  NOTE, stated because the brief said
otherwise: the manifests carry no top-level `operators` list; the
inventory is the set of `probes[*].operator` values.  That is the same
set, derived rather than declared.

What counts as a violation
--------------------------
1. A DICT KEY whose text is an operator token, or whose text is a
   token joined to something else by `/`, `|`, `:` or `,` (the shapes
   a keyed grouping actually takes: "+", "rust/+", "+|i32,i32").
2. A LIST element that is a bare operator token, when the list is not
   one of the label lists in the except-list below.
3. A STRING VALUE that is a bare operator token, when it sits on a
   GROUPING OBJECT.  A grouping object is a dict that carries any of
   `members`, `pairs`, `rows`, `groups`, `entries` -- that is, an
   object whose job is to hold several units.  A token on such an
   object is what verdicts.py did: the row was keyed by the spelling.

The except-list (each entry is a per-unit label, never a key)
-------------------------------------------------------------
  * `operator`, `token`, `spelling`, `label`, `display` -- when the
    field sits on a UNIT OBJECT: a dict that identifies one single
    unit, which here means it carries a language field (`lang` or
    `language`) AND a unit id field (`n`, `unit`, `op`, `id`).  This
    is the one place a token is allowed: the display label on a member.
  * `meta` sub-objects: anything under a key named `meta` is the
    unit's own recorded metadata, copied from the probe manifest.
  * `spelling_labels`, `labels`, `member_labels`, `display_labels` --
    lists of display labels attached to a group.  Elements of these
    are allowed to be tokens or `lang/token` strings.
  * documentation/prose fields: `detail`, `why`, `note`, `notes`,
    `text`, `condition`, `description`, `docstring`, `expression`,
    `source`, `refusal`, `reason`, `mnem`, `bytes`, `key`, `sem_key`.
    `key` is exempt because a byte/sem key is a machine form, and
    machine forms contain characters like `+` only as part of a
    lifted expression, never as a spelling.
  * the whole subtree under `excluded_rows` and `sem_unkeyed`: those
    are per-unit exclusion records.

THE GENERATOR-PROVENANCE EXEMPTION (the owner, 2026-08-26)
-----------------------------------------------------
the owner ruled he is agnostic on MECHANISM; the ban is on spell-MATCHING.
A probe manifest records what the generator asked the compiler for --
it is the provenance of the probe, and it never participates in
matching, grouping, pairing or candidate selection.  So a file whose
TOP-LEVEL `meta` (or top-level `role` field) declares

    "role": "generator provenance"

is exempt, and this program reports it as exempt by name rather than
walking it.

Three things the exemption deliberately does NOT do:

  1. It is read at the ROOT of the checked file ONLY.  A
     manifest-shaped object nested inside a matching or grouping
     artifact is walked exactly as before and still FAILS.  Nesting a
     manifest inside verdicts-shaped output remains a violation.
  2. It does not shrink the operator inventory.  `inventory()` still
     reads every `probe_manifest_*.json`, exempt or not, so the tokens
     the guard hunts for are unchanged.
  3. It is refused if the declaring document also carries a grouping
     field (`members`/`pairs`/`rows`/`groups`/`entries`) at its top
     level -- a matching artifact cannot buy its way out by stamping
     the declaration on itself.  That refusal condition is not one of
     the owner's rulings; it is this program's own, and it is named in the
     failure line so it can be struck.

usage:
  check_no_spelling_keys.py FILE.json [FILE.json ...]
  check_no_spelling_keys.py --html FILE.html    (checks the JSON
                            embedded in a `const DATA = {...};` line)
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

PROVENANCE_ROLE = "generator provenance"

LABEL_FIELDS = set(["operator", "token", "spelling", "label", "display"])

LABEL_LISTS = set(["spelling_labels", "labels", "member_labels",
                   "display_labels"])

PROSE_FIELDS = set(["detail", "why", "note", "notes", "text", "condition",
                    "description", "docstring", "expression", "source",
                    "refusal", "reason", "mnem", "bytes", "key", "sem_key",
                    "lifted", "meta"])

EXEMPT_SUBTREES = set(["meta", "excluded_rows", "sem_unkeyed"])

GROUPING_FIELDS = set(["members", "pairs", "rows", "groups", "entries"])

UNIT_LANG_FIELDS = set(["lang", "language"])

UNIT_ID_FIELDS = set(["n", "unit", "op", "id"])

SPLITTERS = re.compile(r"[/|:,]")


def inventory():
    """every operator token any probe manifest in this directory
    recorded, as a set of strings."""
    out = set()
    names = os.listdir(HERE)
    names = [x for x in names if x.startswith("probe_manifest_")]
    names = [x for x in names if x.endswith(".json")]
    for name in sorted(names):
        path = os.path.join(HERE, name)
        doc = json.load(open(path))
        probes = doc.get("probes")
        if not isinstance(probes, dict):
            continue
        for _n, p in probes.items():
            tok = p.get("operator")
            if not isinstance(tok, str):
                continue
            if not tok.strip():
                continue
            out.add(tok)
    return out


def is_unit_object(node):
    """a dict that identifies one single unit."""
    if not isinstance(node, dict):
        return False
    has_lang = False
    for f in UNIT_LANG_FIELDS:
        if f in node:
            has_lang = True
    has_id = False
    for f in UNIT_ID_FIELDS:
        if f in node:
            has_id = True
    return has_lang and has_id


def is_grouping_object(node):
    """a dict whose job is to hold several units."""
    if not isinstance(node, dict):
        return False
    for f in GROUPING_FIELDS:
        if f in node:
            return True
    return False


def token_hit(text, toks):
    """does this string carry a bare operator token, either whole or as
    a piece joined by / | : , ?"""
    if not isinstance(text, str):
        return None
    if text in toks:
        return text
    parts = SPLITTERS.split(text)
    if len(parts) < 2:
        return None
    for part in parts:
        if part in toks:
            return part
    return None


def walk(node, toks, path, findings, in_label_list=False):
    if isinstance(node, dict):
        for k in sorted(node.keys(), key=str):
            v = node[k]
            here = "%s.%s" % (path, k)
            hit = token_hit(str(k), toks)
            if hit is not None:
                findings.append((here, "dict key is the operator token "
                                       "%r" % hit))
            if k in EXEMPT_SUBTREES:
                continue
            if k in LABEL_LISTS:
                walk(v, toks, here, findings, in_label_list=True)
                continue
            if k in PROSE_FIELDS:
                continue
            if isinstance(v, str):
                if is_unit_object(node) and k in LABEL_FIELDS:
                    continue
                hit = token_hit(v, toks)
                if hit is not None:
                    if is_grouping_object(node):
                        what = "grouping object (it holds several units)"
                    elif k in LABEL_FIELDS:
                        what = "object that does not identify one unit"
                    else:
                        what = "structure field"
                    findings.append(
                        (here, "operator token %r on a %s -- this is a "
                               "grouping/row key, not a per-unit label"
                               % (hit, what)))
                continue
            walk(v, toks, here, findings)
        return

    if isinstance(node, list):
        for i, v in enumerate(node):
            here = "%s[%d]" % (path, i)
            if in_label_list:
                continue
            if isinstance(v, str):
                if v in toks:
                    findings.append((here, "list element is the bare "
                                           "operator token %r" % v))
                continue
            walk(v, toks, here, findings)
        return

    return


HTML_DATA = re.compile(r"const\s+DATA\s*=\s*(\{.*?\});\s*$",
                       re.S | re.M)

HTML_SCRIPT = re.compile(
    r"<script[^>]*type=\"application/json\"[^>]*id=\"data\"[^>]*>"
    r"(.*?)</script>", re.S)


def load_html_data(path):
    """the JSON a generated explorer page embeds, in either of the two
    shapes these pages use: a `<script type="application/json"
    id="data">` block, or a `const DATA = {...};` line."""
    text = open(path).read()
    m = HTML_SCRIPT.search(text)
    if m is not None:
        return json.loads(m.group(1))
    m = HTML_DATA.search(text)
    if m is None:
        return None
    return json.loads(m.group(1))


def declares_provenance_role(doc):
    """does this document declare, at its TOP LEVEL, that it is
    generator provenance?

    the owner ruled 2026-08-26 that he is agnostic on mechanism: the ban is
    on spell-MATCHING.  A probe manifest is the record of what the
    generator emitted; it never participates in matching, grouping or
    candidate selection, so the operator it asked the compiler for is
    provenance, not a key.  The declaration is read from the top-level
    `meta.role`, or from a top-level `role` field."""
    if not isinstance(doc, dict):
        return False
    meta = doc.get("meta")
    if isinstance(meta, dict):
        if meta.get("role") == PROVENANCE_ROLE:
            return True
    if doc.get("role") == PROVENANCE_ROLE:
        return True
    return False


def exemption_refused(doc):
    """the exemption is for provenance files only.  If a document
    declares the provenance role and ALSO carries a grouping field at
    its top level, it is a matching/grouping artifact wearing the
    declaration, and the exemption is refused by name.

    This condition is not one of the owner's; it is the hole the declaration
    would otherwise open, closed here.  Named loudly so a reader can
    strike it if he wants the declaration taken at its word."""
    if not isinstance(doc, dict):
        return None
    for f in sorted(GROUPING_FIELDS):
        if f in doc:
            return f
    return None


def check(path, toks):
    if path.endswith(".html"):
        doc = load_html_data(path)
        if doc is None:
            print("!! %s: no `const DATA = {...};` line found" % path)
            return 2
    else:
        doc = json.load(open(path))
    name = os.path.basename(path)
    refused = False

    if declares_provenance_role(doc):
        refused_on = exemption_refused(doc)
        if refused_on is None:
            print("PASS %s -- exempt: top-level meta declares role "
                  "%r, so this file is generator provenance and never "
                  "participates in matching" % (name, PROVENANCE_ROLE))
            return 0
        print("FAIL %s -- the provenance exemption is REFUSED: this "
              "document declares role %r but carries the grouping "
              "field %r at its top level, so it is a matching/grouping "
              "artifact.  Checking it in full."
              % (name, PROVENANCE_ROLE, refused_on))
        refused = True

    findings = []
    walk(doc, toks, "$", findings)
    if findings:
        print("FAIL %s -- %d spelling-keyed place(s)" % (name,
                                                         len(findings)))
        for where, why in findings[:20]:
            print("     %s" % where)
            print("         %s" % why)
        if len(findings) > 20:
            print("     ... and %d more" % (len(findings) - 20))
        return 1
    if refused:
        print("FAIL %s -- no spelling-keyed place found, but the "
              "provenance exemption was refused above" % name)
        return 1
    print("PASS %s -- no operator token in any key, grouping, pairing "
          "or row structure" % name)
    return 0


def main(argv):
    args = [a for a in argv[1:] if a != "--html"]
    if not args:
        print(__doc__)
        return 2
    toks = inventory()
    print("operator inventory: %d tokens read from probe_manifest_*.json"
          % len(toks))
    worst = 0
    for path in args:
        rc = check(path, toks)
        if rc > worst:
            worst = rc
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv))
