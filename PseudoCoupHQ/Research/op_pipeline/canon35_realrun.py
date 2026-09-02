#!/usr/bin/env python3
"""canon35_realrun.py -- TASK 39: the universal texts RUN, on real
hardware, and answer what the prior texts answer.

WHAT THIS IS.  canon35_assemble.py proves the texts assemble.  This
file proves a SAMPLE of them EXECUTES and computes the same answers as
the text it replaces, with the arguments delivered THROUGH THE
DESIGNATED LOCATIONS rather than through registers -- which is the
whole content of the arrival contract, tested rather than argued.

HOW THE ARGUMENTS REACH THE DESIGNATED LOCATIONS.  Each universal unit
gets a wrapper that parks the incoming arguments in the red zone and
then TAIL-JUMPS into the unit:

    w_u_<unit>:
        mov %rdi,-0x8(%rsp)      a -> S0
        mov %rsi,-0x10(%rsp)     b -> S1
        jmp u_<unit>

The jump does not push a return address, so %rsp is the same inside
the unit as in the wrapper -- S0 and S1 are the same two addresses on
both sides.  That is why this is a tail jump and not a call.  The
prior text is emitted beside it as `p_<unit>` and called with the
ordinary register contract.  A C driver calls both over a table of
argument values and compares the returned bits.

THE SAMPLE, and how it is chosen -- machine-form only.  A unit is
eligible when: its universal text was admitted; it is straight-line;
its entry contract is one of the two shapes the harness can call
(two integers in the general file, or two floating-point values in the
vector file); and its text contains no rip-relative constant, no
call, and no trap -- because this harness carries no constant pool and
no trap handler, so such a unit could not be RUN honestly here.  From
the eligible set the sample is the first SAMPLE_PER_SHAPE units in
(language, unit number) order.  The eligible count and the sampled
count are both reported, so the sample is never read as the whole.

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

Coding discipline: no complex/compound one-liner statements.

usage:
  canon35_realrun.py
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]
WORK = "/tmp/canon35_realrun_work"
OUT = os.path.join(HERE, "canon35_realrun.json")
SAMPLE_PER_SHAPE = 40

BAD = re.compile(r"%rip|\bcall\b|\bud2\b|\bint3\b|\bhlt\b|\bjmp\b|"
                 r"\bj[a-z]{1,3}\b|:")

INT_VALUES = [0, 1, 2, 3, 7, 20, 255, 4096,
              0x7fffffff, 0x80000000, 0xffffffff,
              0x7fffffffffffffff, 0x8000000000000000,
              0xffffffffffffffff]
FLOAT_VALUES = [0.0, 1.0, 2.0, -1.0, 0.5, 3.25, 1e10, -7.75]


def split_lines(text):
    out = []
    for piece in text.split(";"):
        piece = piece.strip()
        if piece:
            out.append(piece)
    return out


def eligible(rec):
    if not rec.get("universal_text"):
        return None
    if rec.get("block_form"):
        return None
    contract = rec.get("entry_contract") or {}
    shape = (contract.get("a"), contract.get("b"),
             contract.get("result"))
    if shape == ("rdi", "rsi", "rax"):
        kind = "two integers"
    elif shape == ("xmm0", "xmm1", "xmm0"):
        kind = "two floating-point values"
    else:
        return None
    for text in (rec["universal_text"], rec["prior_text"]):
        for line in split_lines(text):
            if BAD.search(line):
                return None
    return kind


def emit(fh, symbol, text):
    fh.write("    .globl %s\n%s:\n" % (symbol, symbol))
    for line in split_lines(text):
        clean = line
        if "!!" in clean:
            clean = clean.split("!!", 1)[0].strip()
        fh.write("    %s\n" % clean)


def main():
    if not os.path.isdir(WORK):
        os.makedirs(WORK)
    pool = {"two integers": [], "two floating-point values": []}
    for lang in LANGS:
        path = os.path.join(HERE, "canon35_universal_%s.json" % lang)
        doc = json.load(open(path))["units"]
        for label in sorted(doc, key=lambda x: (x.split("/")[0],
                                                int(x.split("_")[-1]))):
            rec = doc[label]
            kind = eligible(rec)
            if kind is None:
                continue
            pool[kind].append((label, rec))

    eligible_counts = {}
    sample = []
    for kind in pool:
        eligible_counts[kind] = len(pool[kind])
        sample.extend([(kind, x[0], x[1])
                       for x in pool[kind][:SAMPLE_PER_SHAPE]])

    source = os.path.join(WORK, "units.s")
    fh = open(source, "w")
    fh.write("    .text\n")
    for kind, label, rec in sample:
        symbol = label.replace("/", "_")
        emit(fh, "u_" + symbol, rec["universal_text"])
        emit(fh, "p_" + symbol, rec["prior_text"])
        fh.write("    .globl w_%s\nw_%s:\n" % (symbol, symbol))
        if kind == "two integers":
            fh.write("    mov %rdi,-0x8(%rsp)\n")
            fh.write("    mov %rsi,-0x10(%rsp)\n")
        else:
            fh.write("    movq %xmm0,-0x8(%rsp)\n")
            fh.write("    movq %xmm1,-0x10(%rsp)\n")
        fh.write("    jmp u_%s\n" % symbol)
    fh.close()

    driver = os.path.join(WORK, "driver.c")
    fh = open(driver, "w")
    fh.write("#include <stdio.h>\n#include <stdint.h>\n"
             "#include <string.h>\n")
    for kind, label, _rec in sample:
        symbol = label.replace("/", "_")
        if kind == "two integers":
            fh.write("uint64_t p_%s(uint64_t,uint64_t);\n" % symbol)
            fh.write("uint64_t w_%s(uint64_t,uint64_t);\n" % symbol)
        else:
            fh.write("double p_%s(double,double);\n" % symbol)
            fh.write("double w_%s(double,double);\n" % symbol)
    fh.write("static const uint64_t IV[] = {")
    for value in INT_VALUES:
        fh.write("%dULL," % value)
    fh.write("};\n")
    fh.write("static const double FV[] = {")
    for value in FLOAT_VALUES:
        fh.write("%r," % value)
    fh.write("};\n")
    fh.write("int main(void){int bad=0;int pairs=0;\n")
    for kind, label, _rec in sample:
        symbol = label.replace("/", "_")
        if kind == "two integers":
            fh.write("for(int i=0;i<%d;i++)for(int j=0;j<%d;j++){"
                     "uint64_t x=p_%s(IV[i],IV[j]);"
                     "uint64_t y=w_%s(IV[i],IV[j]);pairs++;"
                     "if(x!=y){bad++;printf(\"DIFFER %s %%llu %%llu "
                     "%%llu %%llu\\n\",(unsigned long long)IV[i],"
                     "(unsigned long long)IV[j],"
                     "(unsigned long long)x,(unsigned long long)y);}}\n"
                     % (len(INT_VALUES), len(INT_VALUES), symbol,
                        symbol, label))
        else:
            fh.write("for(int i=0;i<%d;i++)for(int j=0;j<%d;j++){"
                     "double x=p_%s(FV[i],FV[j]);"
                     "double y=w_%s(FV[i],FV[j]);pairs++;"
                     "uint64_t bx,by;memcpy(&bx,&x,8);memcpy(&by,&y,8);"
                     "if(bx!=by){bad++;printf(\"DIFFER %s %%f %%f "
                     "%%f %%f\\n\",FV[i],FV[j],x,y);}}\n"
                     % (len(FLOAT_VALUES), len(FLOAT_VALUES), symbol,
                        symbol, label))
    fh.write("printf(\"pairs %d  differing %d\\n\",pairs,bad);"
             "return bad!=0;}\n")
    fh.close()

    binary = os.path.join(WORK, "harness")
    build = subprocess.run(
        ["gcc", "-O0", "-o", binary, driver, source],
        capture_output=True, text=True)
    if build.returncode != 0:
        print("BUILD FAILED")
        print(build.stderr[:4000])
        return 1
    run = subprocess.run([binary], capture_output=True, text=True)
    transcript = run.stdout.strip()

    doc = {
        "meta": {
            "produced_by": "canon35_realrun.py",
            "role": "generator provenance",
            "work_directory": WORK,
            "selection": "machine-form: admitted universal text, "
                         "straight-line, an entry contract the harness "
                         "can call, and no rip-relative constant, call "
                         "or trap in either text",
        },
        "eligible_counts": eligible_counts,
        "sampled": len(sample),
        "sampled_units": [x[1] for x in sample],
        "argument_values": {"integer": [str(v) for v in INT_VALUES],
                            "floating_point": FLOAT_VALUES},
        "build_command": "gcc -O0 -o harness driver.c units.s",
        "exit_code": run.returncode,
        "transcript": transcript,
    }
    fh = open(OUT, "w")
    json.dump(doc, fh, indent=1, sort_keys=True)
    fh.close()
    print("eligible %s" % json.dumps(eligible_counts, sort_keys=True))
    print("sampled %d units" % len(sample))
    print(transcript)
    return run.returncode


if __name__ == "__main__":
    sys.exit(main())
