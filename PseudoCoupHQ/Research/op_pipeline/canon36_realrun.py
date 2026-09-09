#!/usr/bin/env python3
"""canon36_realrun.py -- TASK 43: the region form RUNS.

WHAT IS EXECUTED, and why the harness is shaped this way.

A region-form unit reads and writes ONLY region-relative addresses,
`0xNN(%r15)`.  So the caller must do three things before handing
control over, and they are exactly the arrival contract region36
states:

    1. reserve REGION_EXTENT bytes of real stack;
    2. put that block's base address in %r15;
    3. write each argument into its input block and each materialized
       literal into its constant block.

and afterwards it reads the answer out of the RESULT BLOCK.  The
wrapper emitted below does precisely that:

    w_u_<unit>:
        push %r15                 %r15 is callee-saved: save the
                                  caller's
        sub  $0x408,%rsp          reserve the region
        mov  %rsp,%r15            the ruled base
        mov  %rdi,0x0(%r15)       argument 1 into input block 0
        mov  %rsi,0x8(%r15)       argument 2 into input block 1
        ...                       one line per materialized literal
        call u_<unit>
        mov  0x200(%r15),%rax     the answer, read from the result
                                  block
        add  $0x408,%rsp
        pop  %r15
        ret

THE RULED MAPPING AND THE HARNESS, stated so they are not confused.
region36 rules the mapping %r15 = %rsp - REGION_SIZE at hand-over.
That statement is what makes an ADDRESS-OF unit's answer the same byte
its original addressed, and it is what the gate binds.  At RUN TIME a
unit is insensitive to where the region actually sits, because it
names no %rsp-relative address at all -- so this harness simply places
the region below its own stack pointer and hands over the base.  The
consequence is recorded rather than hidden: a unit whose ANSWER IS AN
ADDRESS is EXCLUDED from the comparison here, since its answer is an
address in this harness's region and the original's answer is an
address in the original's frame.  Those units are proved by the gate,
under the binding, not by this harness.

The original text is emitted beside each region text and called with
the ordinary register contract, and the two answers are compared over
every ordered pair of a fixed value list.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation).  No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns.  The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label
on the member.  HISTORY OF VIOLATIONS, so the pattern is visible: (1)
the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25
-- the fix brief itself reintroduced it as "same-operator pairs").
MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste
this paragraph verbatim."
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon35_assemble as A35                                   # noqa: E402
import region36 as R36                                           # noqa: E402

WORK = "/tmp/canon36_realrun_work"
OUT = os.path.join(HERE, "canon36_realrun.json")
SAMPLE = 90

VALUES = [0, 1, 2, 3, 7, 20, 255, 4096,
          0x7FFFFFFF, 0x80000000,
          0x7FFFFFFFFFFFFFFF, 0x8000000000000000,
          0xFFFFFFFF, 0xFFFFFFFFFFFFFFFF]


def eligible(record):
    """a unit this harness can honestly call."""
    text = record.get("universal_text")
    if not text:
        return False, "no region text"
    if record.get("block_form"):
        return False, "the text is a block list"
    for line in R36.split_lines(text):
        if "(%rip)" in line:
            return False, "the text names a rip-relative constant"
        head = line.split(" ", 1)[0]
        if head in ("call", "jmp", "ud2", "int3"):
            return False, "the text leaves through %s" % head
        if head.startswith("j"):
            return False, "the text branches"
        # a divide traps the process on a zero or overflowing divisor,
        # and this harness sweeps every ordered pair including b = 0.
        # Measured at first observation: the first sample aborted with
        # SIGFPE.  Those units are excluded here and are proved by the
        # gate instead.
        if head.startswith("div"):
            return False, "the text divides"
        if head.startswith("idiv"):
            return False, "the text divides"
    for entry in record.get("block_directory") or []:
        if entry.get("kind") == "own-address":
            return False, ("the answer or a value of this unit is an "
                           "address in its own region")
    contract = record.get("entry_contract") or {}
    for designation in ("a", "b"):
        family = contract.get(designation)
        if family is None:
            continue
        if family.startswith("xmm"):
            return False, "a vector arrival; this harness passes "\
                          "integers"
    if contract.get("a") is None:
        return False, "no arrival"
    for designation in ("c", "d", "e", "f", "g", "h"):
        if contract.get(designation) is not None:
            return False, "more than two arrivals"
    return True, None


def wrapper(symbol, record):
    lines = []
    lines.append("    push %r15")
    lines.append("    sub $0x%x,%%rsp" % R36.REGION_EXTENT)
    lines.append("    mov %rsp,%r15")
    lines.append("    mov %%rdi,%s" % R36.block_text(R36.INPUT_BASE))
    contract = record.get("entry_contract") or {}
    if contract.get("b") is not None:
        lines.append("    mov %%rsi,%s"
                     % R36.block_text(R36.INPUT_BASE + 8))
    for entry in record.get("block_directory") or []:
        if entry.get("kind") != "constant":
            continue
        if not entry.get("materialized"):
            continue
        lines.append("    movabs $0x%x,%%rax" % entry["value"])
        lines.append("    mov %%rax,%s" % entry["text"])
    lines.append("    call %s" % symbol)
    lines.append("    mov %s,%%rax" % R36.block_text(R36.RESULT_BASE))
    lines.append("    add $0x%x,%%rsp" % R36.REGION_EXTENT)
    lines.append("    pop %r15")
    lines.append("    ret")
    return lines


def main():
    if not os.path.isdir(WORK):
        os.makedirs(WORK)
    chosen = []
    reasons = {}
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        path = os.path.join(HERE, "canon36_universal_%s.json" % lang)
        if not os.path.exists(path):
            continue
        for label, record in sorted(
                json.load(open(path))["units"].items()):
            ok, why = eligible(record)
            if not ok:
                reasons[why] = reasons.get(why, 0) + 1
                continue
            chosen.append((label, record))
    stride = max(1, len(chosen) // SAMPLE)
    sampled = chosen[::stride][:SAMPLE]

    body = ["    .text"]
    names = []
    for label, record in sampled:
        symbol = "u_" + label.replace("/", "_")
        prior_symbol = "p_" + label.replace("/", "_")
        wrap = "w_" + label.replace("/", "_")
        lines, _count, _notes = A35.normalize(symbol,
                                              record["universal_text"])
        body.append("    .globl %s" % symbol)
        body.append("%s:" % symbol)
        body.extend(lines)
        plines, _c, _n = A35.normalize(prior_symbol,
                                       record["prior_text"])
        body.append("    .globl %s" % prior_symbol)
        body.append("%s:" % prior_symbol)
        body.extend(plines)
        body.append("    .globl %s" % wrap)
        body.append("%s:" % wrap)
        body.extend(wrapper(symbol, record))
        names.append((label, wrap, prior_symbol,
                      record.get("result_width") or 64))
    source = os.path.join(WORK, "units.s")
    handle = open(source, "w")
    handle.write("\n".join(body) + "\n")
    handle.close()

    driver = []
    driver.append("#include <stdio.h>")
    driver.append("#include <stdint.h>")
    for _label, wrap, prior_symbol, _width in names:
        driver.append("extern uint64_t %s(uint64_t, uint64_t);" % wrap)
        driver.append("extern uint64_t %s(uint64_t, uint64_t);"
                      % prior_symbol)
    driver.append("static uint64_t V[] = {%s};"
                  % ",".join("%dULL" % v for v in VALUES))
    driver.append("int main(void){ long pairs=0, diff=0;")
    for label, wrap, prior_symbol, width in names:
        driver.append("  for(int i=0;i<%d;i++) for(int j=0;j<%d;j++){"
                      % (len(VALUES), len(VALUES)))
        driver.append("    uint64_t a=V[i], b=V[j];")
        # COMPARE AT THE ANSWER'S OWN DECLARED WIDTH.  The prior text
        # leaves whatever it likes in the upper bytes of its answer
        # register; the region form's result block is zero-extended by
        # rule.  Comparing all 64 bits asked a question neither text
        # answers -- measured at first observation: 960 differing pairs,
        # every one of them an 8- or 32-bit answer (cpp/op_473 is the
        # instance printed in the log).
        driver.append("    uint64_t m=%s;"
                      % ("~0ULL" if width >= 64
                         else "((1ULL<<%d)-1ULL)" % width))
        driver.append("    uint64_t x=%s(a,b)&m, y=%s(a,b)&m;"
                      % (wrap, prior_symbol))
        driver.append("    pairs++;")
        driver.append("    if(x!=y){ diff++; if(diff<6) "
                      "printf(\"DIFF %s a=%%llu b=%%llu region=%%llu "
                      "prior=%%llu\\n\",(unsigned long long)a,"
                      "(unsigned long long)b,(unsigned long long)x,"
                      "(unsigned long long)y); }" % label)
        driver.append("  }")
    driver.append("  printf(\"pairs %ld differing %ld\\n\", pairs, "
                  "diff); return 0; }")
    driver_path = os.path.join(WORK, "driver.c")
    handle = open(driver_path, "w")
    handle.write("\n".join(driver) + "\n")
    handle.close()

    binary = os.path.join(WORK, "harness")
    build = subprocess.run(
        ["gcc", "-O0", "-o", binary, driver_path, source],
        capture_output=True, text=True)
    if build.returncode != 0:
        print("BUILD FAILED")
        print(build.stderr[:3000])
        return 1
    run = subprocess.run([binary], capture_output=True, text=True)
    document = {
        "meta": {
            "produced_by": "canon36_realrun.py",
            "role": "generator provenance",
            "harness": "the region is reserved below the harness's own "
                       "stack pointer and its base handed over in %r15; "
                       "arguments are written into their input blocks "
                       "and materialized literals into their constant "
                       "blocks; the answer is read from the result "
                       "block",
        },
        "eligible_of_the_original_population": len(chosen),
        "sampled": len(sampled),
        "ineligible_by_reason": reasons,
        "stdout": run.stdout,
        "stderr": run.stderr[:2000],
        "returncode": run.returncode,
        "units_sampled": [label for label, _record in sampled],
    }
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    print("eligible %d  sampled %d" % (len(chosen), len(sampled)))
    print(run.stdout.strip()[-600:])
    return 0


if __name__ == "__main__":
    sys.exit(main())
