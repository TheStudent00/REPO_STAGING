# Task pub1 — the public record: finish the scrub of REPO_STAGING under the protocol's cardinal rule, and audit every other public repository against it (read-only)

Read first, ALL of it: `PRIVATE/DevComms/LLM_communication_protocol.md`
— its first card, "CARDINAL SIN: NEVER PUT SENSITIVE INFORMATION IN A
PUBLIC REPO", outranks everything else in this brief. Then
`PUBLIC/REPO_STAGING/stage.sh` and `scrub_patterns.tsv` (how the
public snapshot is scrubbed: tracked files copied into a private area,
patterns applied, a survivor stops the run), and the memory of the rule's
classes: real names / account names / handles; network identity; absolute
or machine paths outside the project root; secrets; machine or environment
fingerprints. DO THE WORK YOURSELF: no sub-agents. Nothing here is a
sandbox computation: it is text over local files. Do NOT run any command
that pushes to a public repository except `bash stage.sh` as §1 says, and
only after its own check says "clean".

## 1. REPO_STAGING: finish the scrub, then refresh once
the owner's rulings of 2026-09-09: machine and environment fingerprints are
scrubbed from PUBLIC repos (kept in private ones); his working name `the owner`
is scrubbed too ("if its an easy change, do it"); toolchain versions
INSIDE the sandbox image (`rustc 1.96.1`, `Swift 6.0.3`, `go1.26`,
`Python 3.13.15`, `Lean 4.24.0`) are KEPT — they are measured facts the
research depends on and fingerprint the published image, not a machine;
`/opt/elan`, `/opt/venv` are the image's paths and are kept.
1. In `PUBLIC/REPO_STAGING/.stage_tmp/` (run `bash stage.sh --no-push`
   once to fill it; it will REFUSE at the check if the new patterns are not
   yet complete — that is fine, the private area is what you inspect),
   find every file that carries a fingerprint of a MACHINE: OS names and
   versions (`<os>`, `<os>`), kernel strings
   (`Linux <kernel>`, `<kernel>`), podman versions, the
   tower's and laptop's memory / core counts / CPU model
   (`31 GB`, `32 GiB`, `<vcpu>`, `<cores>`, `<cpu>`), the tower OS
   version, disk sizes, MAC addresses, container ids (`3cea19671248`),
   hostnames not yet covered. List them by file and pattern in your report
   BEFORE writing patterns.
2. Add patterns to `scrub_patterns.tsv` (format: `<regex><TAB><replacement>`,
   sed -E, applied in order) for each machine fingerprint class, with
   placeholders in angle brackets (`<os>`, `<kernel>`, `<ram>`, `<cores>`,
   `<cpu>`), and `\bDee\b` → `the owner`. Do NOT add a pattern that would
   catch a sandbox toolchain version. Show the added lines LITERAL.
3. Run `bash stage.sh --no-push`; it must print "clean". Then audit the
   private area yourself with greps for every class in the card (names,
   handles, addresses, hostnames, paths outside the project root, secrets,
   fingerprints) and paste each grep and its count; a count above zero is a
   pattern to add, then run again. Only when every class is zero: run
   `bash stage.sh` (which pushes). Paste the commit line.
4. Report: the added patterns; the class-by-class counts before and after
   on the private area; the tip's commit id.

## 2. The other public repositories: AUDIT ONLY, no edits, no pushes
`{Airlock, GraphModel, Ourobrowser, PseudoCoup, ZSpectralCompression}`
are PUBLIC (and `flutter` is an upstream clone, out of scope). For each,
over its TRACKED files (`git ls-files`), the same class-by-class greps as
§1.3: files per class, three example lines per class LITERAL with file and
line number. Airlock has its own guard, `scrub_check.sh`: run it and paste
its output beside your greps. Do not change any of these repositories:
what to do about a finding is the owner's, not this task's.

## 3. Deliverable
One report at `PRIVATE/PseudoCoupHQ/DevComms/log_<next free number>_task_pub1_public_record_scrub_and_audit.md`
(check `ls PRIVATE/PseudoCoupHQ/DevComms | tail` right before
writing; the tower may be writing logs too): §1 what the objects are;
§2 REPO_STAGING before/after with the patterns; §3 the audit per public
repo, a table repo × class with counts, then the examples; §4 by cause
what could not be scrubbed by pattern (a binary file, a spelling that
needs judgement) — flagged, not forced; the two lists (decided / awaiting
the owner). Every count carries the command that produced it. Reply with the
repo × class table, the REPO_STAGING tip commit, and the two lists.
