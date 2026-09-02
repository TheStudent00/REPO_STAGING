#!/usr/bin/env python3
"""diag_caller_destination.py -- TASK 26 part 1: what "the answer
value never entered a tracked register" means mechanically.

THE REFUSAL, verbatim from canon4_units_rust.json (2 units, rust/807
and rust/814):

  "erasure_refused: the answer value never entered a tracked register
   (a passthrough this builder does not model)"

WHAT IT ACTUALLY IS. Both units store their answer THROUGH A POINTER
that arrives in %rdi and return that same pointer in %rax. That is
the x86-64 System V memory-return convention: when a function's
return value does not fit the return registers, the CALLER allocates
the space and passes its address as a hidden FIRST argument; the
callee writes the answer there and returns the address. The declared
arguments then shift one register to the right.

THE EVIDENCE IS FORCED BY CONSTRUCTION, not read off a convention
document. The corpus contains the same intention at four different
answer sizes, compiled by the same compiler in the same run, and the
register roles change with the SIZE and nothing else:

  rust/op_721  answer 16 bytes  -> two return registers, args rdi/rsi
               mov %rsi,%rdx ; mov %rdi,%rax ; ret          CONVERGED
  rust/op_821  answer  3 bytes  -> one return register, args rdi/rsi
               shl $0x8,%esi ; lea (%rsi,%rdi,1),%eax ; ret CONVERGED
  rust/op_793  answer 24 bytes  -> memory return
               mov %rdi,%rax ; mov %rsi,(%rdi) ;
               mov %rdx,0x8(%rdi) ; movb $0x0,0x10(%rdi) ; ret REFUSED
  rust/op_814  answer 24 bytes, float operands -> memory return
               mov %rdi,%rax ; movsd %xmm0,(%rdi) ;
               movsd %xmm1,0x8(%rdi) ; movb $0x0,0x10(%rdi) ; ret
                                                            REFUSED

The only difference between op_721 and op_793 is how many bytes the
answer occupies. Nothing else in the probe changed. So the shift of
the arguments and the appearance of a destination address in %rdi are
CAUSED BY the answer's size -- one assumption only, the standing one
that the compiler compiled the program we wrote.

THE SECOND SYMPTOM IS THE SAME CAUSE. Three of the four units in the
"value w0 is read before it is defined or before the unit's entry
contract names it" bucket are op_786, op_793 and op_800 -- the
integer members of this same family. Their canon4 records declare
entry_contract {"a": "rdi", "b": "rsi", "result": "rax"}, which is
FACTUALLY WRONG for these units: %rdi holds the destination address,
`a` is in %rsi and `b` is in %rdx. The builder read %rdx, which its
own (wrong) contract never named, and refused "read before defined".
One cause, two refusal texts, five units.

WHY THIS IS NOT RENDERED THIS LAP -- a canonical-form question,
reserved for the owner. The ratified canonical runnable form names three
homes: a -> %rdi, b -> %rsi, answer -> %rax (float %xmm0), and the
canonical record is the move-erased form PLUS the ENTRY CONTRACT
(where each value must ARRIVE). These five units have an answer that
never occupies a register at all: it is a byte image at an address
the caller chose, and %rax carries the address rather than the value.
Rendering them needs two things the ratified form does not have:

  (1) a name and a designated register for the incoming DESTINATION
      ADDRESS, which also displaces `a` and `b` from their designated
      registers whenever it is present; and
  (2) an EXIT CONTRACT -- the dual of the entry contract -- saying
      the answer is the N-byte image at that address, laid out at
      stated offsets, rather than a value in a register.

Both are ontology: a new traced name, a new register assignment rule,
and a new half of the canonical record. AgentMemory's standing ruling
is "the owner decides architecture, ontology, naming. Flag, don't decide."
So this file NAMES the question with its evidence and stops. It does
not invent an exit contract.

This file writes a diagnosis artifact only. It changes no unit's
status and gates nothing.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

THE MEMBERSHIP KEY IS MACHINE FORM. A unit joins this family when its
own ship code satisfies BOTH shape tests, read off the instruction
text and nothing else:

  - the first instruction copies an incoming register into the answer
    register (`mov %rXX,%rax`), and
  - every store in the unit writes through that same incoming
    register as a base.

No operator token, no result-type name, no source expression takes
part in the test. The `result_type` and the operator spelling are
carried on each row for READING only, and the guard is run on the
output.

Coding discipline: no complex/compound one-liner statements.

usage:
  diag_caller_destination.py
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

LANGS = ["c", "cpp", "go", "rust", "swift"]

FIRST_COPY_RE = re.compile(r"^mov\s+%(r[a-z0-9]+),%rax$")
STORE_RE = re.compile(r",(?:(0x[0-9a-f]+))?\(%(r[a-z0-9]+)\)$")


def shape_test(mnem_lines):
    """(is_member, destination_register, store_offsets) -- the two
    machine-form tests, applied to the unit's own ship text."""
    if not mnem_lines:
        return False, None, []
    first = mnem_lines[0].strip()
    m = FIRST_COPY_RE.match(first)
    if m is None:
        return False, None, []
    base = m.group(1)
    if base == "rax":
        return False, None, []
    offsets = []
    stores = 0
    for line in mnem_lines[1:]:
        text = line.strip()
        s = STORE_RE.search(text)
        if s is None:
            continue
        if s.group(2) != base:
            return False, None, []
        stores = stores + 1
        if s.group(1) is None:
            offsets.append(0)
            continue
        offsets.append(int(s.group(1), 16))
    if stores == 0:
        return False, None, []
    return True, base, offsets


def main():
    members = {}
    for lang in LANGS:
        path = os.path.join(HERE, "canon4_units_%s.json" % lang)
        units = json.load(open(path))["units"]
        for n, rec in units.items():
            mnem = rec.get("mnem") or []
            ok, base, offsets = shape_test(mnem)
            if not ok:
                continue
            key = "%s/%s" % (lang, n)
            members[key] = {
                "lang": lang,
                "n": n,
                "destination_register_in": base,
                "store_offsets": offsets,
                "answer_bytes_touched": (max(offsets) + 1
                                         if offsets else 0),
                "declared_entry_contract": rec.get("entry_contract"),
                "erasure": rec.get("erasure"),
                "derive_refused": rec.get("derive_refused"),
                "mnem": mnem,
                "result_type_for_reading":
                    (rec.get("meta") or {}).get("result_type"),
                "operator": (rec.get("meta") or {}).get("operator"),
            }
    doc = {
        "meta": {
            "produced_by": "diag_caller_destination.py",
            "role": "grouping artifact -- checked in full by "
                    "check_no_spelling_keys.py, no provenance "
                    "exemption claimed",
            "what": "the caller-provided-destination (memory-return) "
                    "family: units whose answer is a byte image at "
                    "an address the caller passed in, never a value "
                    "in a register",
            "membership_key": "machine form: first instruction copies "
                              "an incoming register into %rax AND "
                              "every store writes through that same "
                              "register as base",
            "disposition": "the owner-reserved -- rendering these needs a "
                           "name and designated register for the "
                           "incoming destination address, and an "
                           "EXIT CONTRACT as the dual of the entry "
                           "contract. Both are ontology.",
            "member_count": len(members),
        },
        "members": members,
    }
    out = os.path.join(HERE, "diag_caller_destination.json")
    fh = open(out, "w")
    json.dump(doc, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()
    print("wrote diag_caller_destination.json -- %d members"
          % len(members))
    for key in sorted(members):
        row = members[key]
        print("   %-12s dest=%%%s  offsets=%r  refusal=%r"
              % (key, row["destination_register_in"],
                 row["store_offsets"],
                 (row["derive_refused"] or row["erasure"])))


if __name__ == "__main__":
    main()
