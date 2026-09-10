#!/bin/bash
# bank1_l10_the_changed_artifacts.sh -- task bank1, lane 10.
#
# WHAT THIS LANE DOES: the seven audited triples whose re-derived source
# hashed differently from the certificate's, read one by one -- which
# pass wrote the certificate, what the two sha256s are, what the
# re-derivation answered, and the first line of source on which the two
# artifacts differ.  These seven are the finding this task carries out,
# caught by the audit rather than by a whole re-run: a renderer moved,
# so the same cell now yields a DIFFERENT artifact, and the old proof
# describes the old one.
#
# It appends its own captured output to bank1.md as section 9; lane 9
# wrote sections 1 to 8 the same way, by capture and never by hand.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_BANK1.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bank1_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
M="$A/bank1.md"
total=2

i=1
echo "[$i/$total] the seven changed artifacts, one by one"
python3 - "$A" <<'PY' | tee /tmp/bank1_changed.txt
import hashlib, json, sys

here = sys.argv[1]
document = json.load(open(here + "/bank1_delta.json"))
changed = []
for row in document["audit"]:
    if row["reading"] != "the artifact changed":
        continue
    changed.append(row)

wanted = set()
for row in changed:
    wanted.add((row["cell"]["mnem"], row["cell"]["shape"],
                row["cell"]["key_width"], row["target"], row["place"]))

certificate = {}
handle = open(here + "/certificates.jsonl")
for line in handle:
    text = line.strip()
    if not text:
        continue
    cert = json.loads(text)
    key = (cert["cell"]["mnem"], cert["cell"]["shape"],
           cert["cell"]["key_width"], cert["target"], cert["place"])
    if key not in wanted:
        continue
    if not cert["preferred"]:
        continue
    certificate[key] = cert
handle.close()

rederived = {}
handle = open(here + "/bank1_delta_runs.jsonl")
for line in handle:
    text = line.strip()
    if not text:
        continue
    run = json.loads(text)
    for place in run.get("places") or []:
        key = (run["mnem"], run["shape"], run["key_width"], run["lang"],
               place.get("writes"))
        if key not in wanted:
            continue
        rederived[key] = (run, place)
handle.close()


def first_difference(left, right):
    if left is None or right is None:
        return ("-- no source --", "-- no source --")
    one = left.split("\n")
    two = right.split("\n")
    for index in range(max(len(one), len(two))):
        a = one[index].strip() if index < len(one) else "-- ends --"
        b = two[index].strip() if index < len(two) else "-- ends --"
        if a == b:
            continue
        return (a, b)
    return ("-- identical text --", "-- identical text --")


print("Table D7 -- the seven audited triples whose artifact changed. "
      "`the certificate's source` and `the re-derivation's source` are "
      "the FIRST line on which the two rendered sources differ, which "
      "is the measurement; the several hundred characters of preamble "
      "they share are not shown.")
print("")
print("| `mnem` | shape | `key_width` | target | place | certificate's "
      "pass | certificate | re-derived | the certificate's source | the "
      "re-derivation's source |")
print("|---|---|---|---|---|---|---|---|---|---|")
for row in changed:
    key = (row["cell"]["mnem"], row["cell"]["shape"],
           row["cell"]["key_width"], row["target"], row["place"])
    cert = certificate.get(key)
    held = rederived.get(key)
    new_source = None
    if held is not None:
        new_source = held[1].get("source")
    old_source = None
    left = "-- the store keeps the sha256, not the text --"
    right = "-- the store keeps the sha256, not the text --"
    # the certificate's own source text is on the pass's store, so it is
    # read from the source FILE the certificate names, which is the same
    # artifact the sha256 was taken over.
    path = (cert["source"] or {}).get("path") if cert else None
    if path is not None:
        import os
        direct = os.path.join(here, "..", path)
        if os.path.exists(direct):
            old_source = open(direct).read()
    if old_source is not None and new_source is not None:
        left, right = first_difference(old_source, new_source)
    print("| `%s` | %s | %s | %s | `%s` | `%s` | %s | %s | `%s` | `%s` |"
          % (row["cell"]["mnem"], row["cell"]["shape"],
             row["cell"]["key_width"], row["target"], row["place"],
             row["certificate_pass"], row["certificate_kind"],
             row["rederived_kind"], left[:150], right[:150]))
print("")
for row in changed:
    key = (row["cell"]["mnem"], row["cell"]["shape"],
           row["cell"]["key_width"], row["target"], row["place"])
    cert = certificate.get(key)
    held = rederived.get(key)
    print("%s %s %s on %s at %s"
          % (key[0], key[1], key[2], key[3], key[4]))
    print("   the certificate: pass %s, kind %s, source %s, sha256 %s"
          % (row["certificate_pass"], row["certificate_kind"],
             (cert["source"] or {}).get("path") if cert else "--",
             row["certificate_sha256"]))
    print("   the re-derivation: kind %s, sha256 %s"
          % (row["rederived_kind"], row["rederived_sha256"]))
    if held is not None:
        place = held[1]
        check = place.get("check") or {}
        print("   the re-derivation's verdict: %s -- %s"
              % (check.get("outcome"), check.get("reason")))
        if place.get("refusal_cause"):
            print("   the re-derivation's refusal cause: %s"
                  % place["refusal_cause"])
        if place.get("refusal_detail"):
            print("   the re-derivation's refusal detail: %s"
                  % place["refusal_detail"])
    print("")
PY
echo

i=2
echo "[$i/$total] appending it to bank1.md as section 9"
cat >> "$M" <<'H9'

## 9. The seven artifacts that changed, one by one

The audit re-derived 58 certified triples and 51 came back identical.
The seven below did not: the renderer moved between the certificate's
pass and this one, so the same cell now yields a DIFFERENT artifact.
None is an alarm — an alarm is a differing verdict on IDENTICAL inputs
— and none replaces its certificate; each is a new certificate beside
the old one, which is the whole of what a bank is for.

H9
echo "**LITERAL**, lane \`bank1_l10_the_changed_artifacts.sh\`:" >> "$M"
echo >> "$M"
echo '```' >> "$M"
cat /tmp/bank1_changed.txt >> "$M"
echo '```' >> "$M"
echo "  bank1.md is now $(wc -l < "$M") line(s)"
echo
echo "lane done"
