#!/usr/bin/env python3
"""Build LLM_communication_protocol_cases.md from the archived v2, verbatim,
and check that nothing was dropped and every pointer resolves."""
import re, sys, pathlib

DC = pathlib.Path.home() / "Programming/DevComms"
V1 = DC / "0_Archive/LLM_communication_protocol_v1.md"
V2 = DC / "0_Archive/LLM_communication_protocol_v2.md"
V3 = DC / "LLM_communication_protocol.md"
OUT = DC / "LLM_communication_protocol_cases.md"

# v2 section number -> cards it now feeds
CARDS = {
    "header": ["(provenance — kept here in full)"],
    "0": ["§0 of v3 (kept verbatim in the rulebook)"],
    "1": ["names.* (family heading)"],
    "1.1": ["names.keep-my-words", "names.build-on-my-framing"],
    "1.2": ["names.define-in-sentence", "names.glossary-form",
            "names.measured-register"],
    "1.3": ["names.banned-socio-familial", "names.banned-death-words",
            "names.third-party-terms", "names.tribal-vocabulary"],
    "1.4": ["names.anchor-abstractions"],
    "1.5": ["names.cold-re-entry"],
    "1.6": ["names.level-named"],
    "1.8": ["names.what-is-it-first"],
    "1.7": ["names.one-name-one-thing"],
    "2": ["shape.* (family heading)"],
    "2.1": ["shape.one-idea-per-sentence"],
    "2.2": ["shape.contrast-visible"],
    "2.3": ["shape.no-unrequested-optionality"],
    "3": ["shape.one-tree", "§2 Precedence of v3"],
    "3.1": ["order.answer-first-when-self-standing", "§2 Precedence of v3"],
    "3.2": ["order.model-before-conclusion", "order.name-before-use"],
    "3.3": ["order.first-sentence-rests-on-nothing-later"],
    "3.4": ["order.question-states-its-facts"],
    "3.4a": ["order.project-not-session"],
    "3.5": ["order.walkthrough-before-numbers"],
    "3.6": ["order.interpretation-conditional"],
    "4": ["media.* (family heading)"],
    "4.1": ["media.pick-per-idea", "media.figure-says-what-it-is",
            "object.instance-before-mechanism", "§2 Precedence of v3"],
    "4.2": ["shape.levels-complete", "shape.one-sentence-per-bullet",
            "§2 Precedence of v3"],
    "4.3": ["media.pipe-tables"],
    "4.4": ["media.text-diagrams"],
    "4.5": ["media.raw-blocks-last-resort"],
    "4.6": ["object.machine-state-stepped"],
    "4.7": ["shape.heading-names-content"],
    "5": ["object.* (family heading)"],
    "5.1": ["object.quote-then-characterize", "object.unverified-marked"],
    "5.1a": ["object.literal-gloss-analogy"],
    "5.2": ["object.full-mechanism-four-parts", "object.metaphor-beside",
            "names.no-nicknames"],
    "5.3": ["object.report-by-cause"],
    "5.4": ["object.inherited-assumptions"],
    "6": ["media.structural-overview, scope.code-shape (family heading)"],
    "6.1": ["media.structural-overview", "media.call-flow-arrows"],
    "6.2": ["scope.code-shape — text lives in "
            "PseudoCoupHQ/plan_and_code.md §1–§2"],
    "6.3": ["scope.code-shape — text moved to "
            "PseudoCoupHQ/plan_and_code.md §7"],
    "7": ["scope.* (family heading)"],
    "7.1": ["scope.who-decides"],
    "7.2": ["scope.do-what-was-asked"],
    "7.3": ["scope.no-compliments"],
    "8": ["refs.full-paths", "refs.carry-context", "refs.hyperlink",
          "refs.command-as-typed", "refs.non-local-said"],
    "9": ["scope.* (family heading)"],
    "9.1": ["scope.completion-shows-report"],
    "9.2": ["scope.long-output-to-log", "scope.three-stores",
            "refs.log-citation"],
    "10": ["§10 Checklist of v3 (now generated from the cards' TEST lines)"],
    "11": ["names.measured-register"],
    "A": ["object.instance-before-mechanism", "shape.heading-names-content",
          "object.pointers-at-end"],
    "B": ["shape.one-tree", "order.name-before-use"],
}

# v1 section -> v2 section (from the v2 refactor) -> card
V1MAP = [
    ("1 Language / Keep my words", "1.1", "names.keep-my-words"),
    ("1 / When my word is inaccurate", "1.1", "names.keep-my-words"),
    ("1 / When you introduce a new term", "1.2", "names.define-in-sentence"),
    ("1 / Banned: socio-familial", "1.3", "names.banned-socio-familial"),
    ("1 / Banned: death/kill", "1.3", "names.banned-death-words"),
    ("1 / Avoid tribal vocabulary", "1.3", "names.tribal-vocabulary"),
    ("1 / Abstract words need anchors", "1.4", "names.anchor-abstractions"),
    ("2 Structural overviews", "6.1", "media.structural-overview"),
    ("2a Plan and code share names", "6.2", "scope.code-shape → plan_and_code.md §1–§2"),
    ("2b Coding style: methods do not need the instance", "6.3", "scope.code-shape → plan_and_code.md §7"),
    ("3 Diagrams", "4.4", "media.text-diagrams"),
    ("3 / BANNED: whitespace-aligned tables", "4.3", "media.pipe-tables"),
    ("3 / Raw text blocks", "4.5", "media.raw-blocks-last-resort"),
    ("4 Glossary entries", "1.2", "names.glossary-form"),
    ("5 Explanation style", "0, 2.3", "§0; shape.no-unrequested-optionality"),
    ("5 / Nested bullets", "4.2", "shape.levels-complete"),
    ("5 / one idea per bullet", "4.2", "shape.one-sentence-per-bullet"),
    ("5a Contrast must be visible", "2.2", "shape.contrast-visible"),
    ("5b One idea per sentence", "2.1", "shape.one-idea-per-sentence"),
    ("6 Decision-making", "7.1", "scope.who-decides"),
    ("7 Artifacts and writing", "7.2", "scope.do-what-was-asked"),
    ("8 Self-checks", "10", "§10 Checklist"),
    ("9 Assume I'm missing context", "3.2", "order.model-before-conclusion"),
    ("9a The first sentence rests on nothing later", "3.3", "order.first-sentence-rests-on-nothing-later"),
    ("9b Cold words re-enter", "1.5", "names.cold-re-entry"),
    ("10 The root rule", "0", "§0"),
    ("11 Full mechanism or nothing", "5.2", "object.full-mechanism-four-parts; object.metaphor-beside"),
    ("11a Every claim names its level", "1.6", "names.level-named"),
    ("12 Claims come with evidence", "5.1", "object.quote-then-characterize; object.unverified-marked"),
    ("12a Quote the object", "5.1", "object.quote-then-characterize"),
    ("12b Use the medium that carries the idea", "4.1", "media.pick-per-idea"),
    ("13 Report by cause", "5.3", "object.report-by-cause"),
    ("14 Make references findable", "8", "refs.full-paths; refs.carry-context"),
    ("14a A command appears as it is typed", "8", "refs.command-as-typed"),
    ("15 Interpretation and certainty", "3.6", "order.interpretation-conditional"),
    ("15a A question states the facts it rests on", "3.4", "order.question-states-its-facts"),
    ("16 Hyperlink to Files", "8", "refs.hyperlink"),
    ("17 No Compliments", "7.3", "scope.no-compliments"),
    ("18 Presentation of Reports", "9.1", "scope.completion-shows-report"),
    ("18a Long output goes in a DevComms log", "9.2", "scope.long-output-to-log; scope.three-stores; refs.log-citation"),
    ("18b Walkthrough before numbers", "3.5", "order.walkthrough-before-numbers"),
    ("19 My vocabulary", "11", "names.measured-register"),
    ("— (added in v2)", "1.7", "names.one-name-one-thing"),
    ("— (added in v2)", "1.8", "names.what-is-it-first"),
    ("— (added in v2)", "3.4a", "order.project-not-session"),
    ("— (added in v2)", "4.6", "object.machine-state-stepped"),
    ("— (added in v2)", "4.7", "shape.heading-names-content"),
    ("— (added in v2)", "5.1a", "object.literal-gloss-analogy"),
    ("— (added in v2)", "5.4", "object.inherited-assumptions"),
    ("— (added in v2)", "A", "object.instance-before-mechanism (worked comparison)"),
    ("— (added in v2)", "B", "shape.one-tree (the exemplar)"),
]

HEAD = re.compile(r"^(## |### )(.*)$")
NUM = re.compile(r"^(?:Appendix ([AB])|(\d+(?:\.\d+)?[ab]?)\.?)\b")

def top_sections(lines):
    """Split v2 into (key, title, body_lines) at '## ' headings only;
    '### ' subsections stay inside their section body, verbatim."""
    out, key, title, body = [], "header", "v2 header", []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("## "):
            out.append((key, title, body))
            t = ln[3:].strip()
            # Appendix B's heading spans two lines in v2
            if t.startswith("Appendix B") and i + 1 < len(lines) and lines[i+1].startswith("## "):
                t = t + " " + lines[i+1][3:].strip(); i += 1
            m = NUM.match(t)
            key = (m.group(1) or m.group(2)) if m else t
            title, body = t, []
        else:
            body.append(ln)
        i += 1
    out.append((key, title, body))
    return out

def sub_keys(body):
    ks = []
    for ln in body:
        if ln.startswith("### "):
            m = NUM.match(ln[4:].strip())
            if m: ks.append(m.group(1) or m.group(2))
    return ks

v2 = V2.read_text().splitlines()
secs = top_sections(v2)

out = []
w = out.append
w("# Communication Protocol — cases")
w("")
w("The account behind every rule in")
w("`DevComms/LLM_communication_protocol.md` (v3). Each")
w("v2 section is reproduced here VERBATIM — its rule text, its dated")
w("failure, and every quote — under the card or cards it now feeds.")
w("Nothing from v2 was dropped; the rulebook carries the distilled")
w("card, this file carries how the rule was reached. Per")
w("`scope.three-stores`: the rulebook says what a rule IS; this file")
w("is the working record of why.")
w("")
w("Built 2026-09-06 from")
w("`DevComms/0_Archive/LLM_communication_protocol_v2.md`")
w("by `build_cases.py` (kept beside this file). To add a case: append")
w("a dated entry under the card's section; do not edit the verbatim")
w("v2 text.")
w("")
w("---")
w("")
w("## 0. Id map — v1 section → v2 section → v3 card")
w("")
w("Older logs cite v1 numbers (§18a, §14a, §5a) or v2 numbers (§5.1a,")
w("§1.7). Resolve them here.")
w("")
w("| v1 section | v2 section | v3 card |")
w("|---|---|---|")
for a, b, c in V1MAP:
    w(f"| {a} | §{b} | `{c}` |")
w("")
w("---")
w("")
w("## 1. The v2 text, section by section")
w("")
for key, title, body in secs:
    cards = CARDS.get(key)
    if cards is None:
        print(f"UNMAPPED v2 section: {key!r} {title!r}", file=sys.stderr); sys.exit(1)
    label = "v2 header" if key == "header" else (f"v2 Appendix {key}" if key in "AB" else f"v2 §{key}")
    w(f"### {label} — {title}" if key != "header" else "### v2 header")
    w("")
    w("→ cards: " + "; ".join(f"`{c}`" for c in cards))
    subs = sub_keys(body)
    for s in subs:
        if s in CARDS and s != key:
            w(f"→ §{s} within: " + "; ".join(f"`{c}`" for c in CARDS[s]))
    w("")
    # verbatim body, with headings demoted one level so the tree stays one tree
    for ln in body:
        if ln.startswith("### "):
            w("#### " + ln[4:])
        else:
            w(ln)
    w("")
OUT.write_text("\n".join(out).rstrip() + "\n")
print(f"wrote {OUT} ({len(out)} lines)")

# ---------- checks ----------
errs = []
cases = OUT.read_text()
# 1. every v2 heading appears verbatim in the cases file
for ln in v2:
    if ln.startswith("## ") or ln.startswith("### "):
        t = ln.split(" ", 1)[1].strip()
        if t not in cases:
            errs.append(f"v2 heading missing from cases: {t!r}")
# 2. every non-blank v2 line appears in the cases file (verbatim move)
v2set = set(l for l in v2 if l.strip() and not l.startswith("## "))
case_lines = set(cases.splitlines())
missing = [l for l in v2set if l not in case_lines and ("#### " + l[4:]) not in case_lines]
if missing:
    errs.append(f"{len(missing)} v2 lines not found verbatim in cases, e.g. {missing[:3]}")
# 3. every card id named in the CARDS map exists in v3; every v3 card is mapped
v3 = V3.read_text()
v3_ids = set(re.findall(r"^#### ([a-z]+\.[a-z0-9-]+)$", v3, re.M))
mapped = set()
for cs in CARDS.values():
    for c in cs:
        for m in re.findall(r"\b([a-z]+\.[a-z0-9-]+)\b", c):
            if "." in m and not m.endswith(".md"): mapped.add(m)
for c in sorted(mapped - v3_ids):
    if not c.endswith(".*"):
        errs.append(f"card named in map but not in v3: {c}")
for c in sorted(v3_ids - mapped):
    errs.append(f"v3 card not fed by any v2 section: {c}")
# 4. every CASE pointer in v3 resolves to a v2 section present in cases
for m in re.finditer(r"\*\*CASE\.\*\* (.*?)(?:\n- \*\*|\n\n|\n---)", v3, re.S):
    for ref in re.findall(r"cases (?:§([0-9.ab]+)|Appendix ([AB]))", m.group(1)):
        k = ref[0] or ref[1]
        k = k.rstrip(".")
        if k not in CARDS:
            errs.append(f"v3 CASE pointer to unknown v2 section: {k}")
# 5. the checklist has exactly one line per TEST (count TEST lines vs checklist bullets)
tests = len(re.findall(r"^- \*\*TEST\.\*\*", v3, re.M))
chk = v3.split("## 10. Checklist before sending", 1)[1]
chk_items = len(re.findall(r"^- ", chk, re.M))
print(f"cards={len(v3_ids)} TEST lines={tests} checklist items={chk_items}")
if tests != chk_items:
    errs.append(f"checklist has {chk_items} items but there are {tests} TEST lines")
if errs:
    print("CHECK FAILED:"); [print("  " + e) for e in errs]; sys.exit(1)
print("CHECK PASSED: every v2 line present verbatim; every card mapped; every CASE pointer resolves; checklist complete")
