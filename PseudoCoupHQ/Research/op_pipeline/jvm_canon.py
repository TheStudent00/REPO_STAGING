#!/usr/bin/env python3
"""jvm_canon.py -- the JVM unit, stripped of its runtime furniture and
renamed into THE CANONICAL RUNNABLE FORM.

What this file does
-------------------
`interp_jvm.json` holds two units the JVM printed for itself: the
machine code its C2 compiler produced for two warmed Java methods.
The bytes are the JVM's own testimony; the mnemonics are objdump's
reading of those bytes.

An nmethod is not a C function.  Around the arithmetic the JVM puts
runtime furniture: an entry barrier, a return safepoint poll, a frame
that exists to serve them, and out-of-line stubs.  `arch_read` already
strips Go's stack check the same way -- mechanically, by a named rule,
refusing when the pattern does not match.  This file does the same for
the JVM, rule by rule:

  RULE F1  FRAME PUSH.  A leading run of stack-frame instructions:
           `sub $N,%rsp`, `push %rbp`, `mov %rbp,N(%rsp)`, and the
           stack-bang store `mov %eax,-N(%rsp)`.
  RULE B1  ENTRY BARRIER.  Exactly `cmpl $0x0,0x20(%r15)` followed by
           `jne <target>`.  %r15 is the JVM's thread register; the
           JVM's own annotation names the target
           `{runtime_call Stub::method_entry_barrier}`.
  RULE F2  FRAME POP.  A run of `add $N,%rsp`, `pop %rbp`,
           `mov N(%rsp),%rbp`.
  RULE P1  RETURN SAFEPOINT POLL.  Exactly `cmp 0x28(%r15),%rsp`
           followed by `ja <target>`.  The JVM annotates that target
           `{poll_return}` and the block it reaches
           `{runtime_call SafepointBlob}`.
  RULE R1  THE RETURN.  `ret`.
  RULE O1  OUT-OF-LINE REMAINDER.  Everything after the return.  It is
           dropped only when both stripped branch targets land inside
           it, so it is reachable from the furniture and from nothing
           else.

CONSERVATIVE, and this is the whole posture: an unmatched pattern is a
REFUSAL with the reason and the offending line, never a guess.  Two
further checks run before anything is stripped:

  * the residual core may not mention %rsp, %rbp or %r15.  If it does,
    the frame is not "furniture only" and the strip is refused.
  * the residual core must be one straight run with no branch.  If it
    branches, this file refuses and says so; that unit needs the full
    multi-block machinery, not this one.

THE RENAME.  The JVM's ABI is not the C one.  The JVM states its own
in the dump: `parm0: rsi`, `parm1: rdx`.  THE CANONICAL RUNNABLE FORM
(ratified 2026-08-25) is a -> %rdi, b -> %rsi, result -> %rax.  So the
rename is per VALUE, as canon.py does it: the value that arrived in
%rsi becomes %rdi, the value that arrived in %rdx becomes %rsi.

TRACED-VARIABLES-PRIORITY applies: a traced variable owns its
designated register and an untraced occupant is evicted to a temp.
This file does NOT implement eviction.  It CHECKS for the condition
that would need one -- a rename target read or written by anything
other than the value being renamed into it -- and REFUSES, naming the
register and the line, rather than producing a wrong rename.  canon.py
is where eviction lives.

EVIDENCE CLASS, stated on the product because it is weaker than the
rest of the table: these bytes are the JVM's testimony about code it
generated at run time, carved out of a print by our lane.  They are
not an ELF section a compiler wrote to disk.  Nothing downstream may
read this member as the same class of evidence as a c or rust unit.

usage:
  jvm_canon.py [--in DIR] [--out DIR] [--cc as] [--dump objdump]
"""

import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))

# one objdump line: address, bytes, text.  A line with no text is a
# continuation carrying the tail bytes of the instruction above it.
LINE = re.compile(r"^\s*([0-9a-f]+):\s*((?:[0-9a-f]{2}\s*)+?)\s*(\t(.*))?$")

FRAME_PUSH = [
    re.compile(r"^sub\s+\$0x[0-9a-f]+,%rsp$"),
    re.compile(r"^push\s+%rbp$"),
    re.compile(r"^mov\s+%rbp,0x[0-9a-f]+\(%rsp\)$"),
    re.compile(r"^mov\s+%eax,-0x[0-9a-f]+\(%rsp\)$"),
]

FRAME_POP = [
    re.compile(r"^add\s+\$0x[0-9a-f]+,%rsp$"),
    re.compile(r"^pop\s+%rbp$"),
    re.compile(r"^mov\s+0x[0-9a-f]+\(%rsp\),%rbp$"),
]

BARRIER_TEST = re.compile(r"^cmpl\s+\$0x0,0x20\(%r15\)$")
BARRIER_JUMP = re.compile(r"^jne\s+0x([0-9a-f]+)$")

POLL_TEST = re.compile(r"^cmp\s+0x28\(%r15\),%rsp$")
POLL_JUMP = re.compile(r"^ja\s+0x([0-9a-f]+)$")

RET = re.compile(r"^ret$")

BRANCHY = re.compile(r"^(j\w+|call|ret|hlt|loop\w*)\b")

REGISTER = re.compile(r"%([a-z0-9]+)")

# the register families, so a rename of `rsi` also rewrites `esi`,
# `si` and `sil`.  Same table canon.py works from, restated here
# because this file is handed one unit and not the pipeline's records.
FAMILY = {
    "rax": ["rax", "eax", "ax", "al"],
    "rbx": ["rbx", "ebx", "bx", "bl"],
    "rcx": ["rcx", "ecx", "cx", "cl"],
    "rdx": ["rdx", "edx", "dx", "dl"],
    "rsi": ["rsi", "esi", "si", "sil"],
    "rdi": ["rdi", "edi", "di", "dil"],
    "rbp": ["rbp", "ebp", "bp", "bpl"],
    "rsp": ["rsp", "esp", "sp", "spl"],
}
for _i in range(8, 16):
    _q = "r%d" % _i
    FAMILY[_q] = [_q, _q + "d", _q + "w", _q + "b"]

WIDE = {}
for _q in FAMILY:
    for _name in FAMILY[_q]:
        WIDE[_name] = _q


class Refused(Exception):

    def __init__(self, rule, why, line=None):
        Exception.__init__(self, why)
        self.rule = rule
        self.why = why
        self.line = line


def parse_lines(objdump):
    """[(address int, [byte strings], text)] -- continuation lines
    folded into the instruction above them."""
    out = []
    for raw in objdump:
        m = LINE.match(raw.rstrip())
        if m is None:
            raise Refused("PARSE", "a dump line did not parse", raw)
        addr = int(m.group(1), 16)
        chunk = m.group(2).split()
        text = (m.group(4) or "").strip()
        text = re.sub(r"\s+", " ", text)
        if not text:
            if not out:
                raise Refused("PARSE", "a continuation line with no "
                                       "instruction above it", raw)
            out[-1][1].extend(chunk)
            continue
        out.append([addr, chunk, text, raw])
    return out


def matches_any(text, patterns):
    for p in patterns:
        if p.match(text):
            return True
    return False


def strip(unit):
    """the residual core, and the record of what each rule removed."""
    runs = unit["arch_unit"]
    if len(runs) != 1:
        raise Refused("SHAPE", "the unit is not one contiguous run: "
                               "%d runs" % len(runs))
    lines = parse_lines(runs[0]["objdump"])

    removed = []
    i = 0

    # RULE F1
    f1 = []
    while i < len(lines) and matches_any(lines[i][2], FRAME_PUSH):
        f1.append(lines[i][2])
        i = i + 1
    if not f1:
        raise Refused("F1", "no frame push at the top of the unit",
                      lines[0][2] if lines else None)
    removed.append(dict(rule="F1", what="frame push", lines=f1))

    # RULE B1
    if i + 1 >= len(lines):
        raise Refused("B1", "the unit ends before the entry barrier")
    if not BARRIER_TEST.match(lines[i][2]):
        raise Refused("B1", "the instruction after the frame push is "
                            "not the entry barrier test "
                            "`cmpl $0x0,0x20(%r15)`", lines[i][2])
    m = BARRIER_JUMP.match(lines[i + 1][2])
    if m is None:
        raise Refused("B1", "the entry barrier test is not followed by "
                            "`jne <target>`", lines[i + 1][2])
    barrier_target = int(m.group(1), 16)
    removed.append(dict(rule="B1", what="entry barrier",
                        lines=[lines[i][2], lines[i + 1][2]],
                        target=hex(barrier_target)))
    i = i + 2

    # THE CORE: everything up to the frame pop
    core_start = i
    while i < len(lines) and not matches_any(lines[i][2], FRAME_POP):
        i = i + 1
    if i == core_start:
        raise Refused("CORE", "the frame pop follows the entry barrier "
                              "immediately: there is no core to keep")
    if i >= len(lines):
        raise Refused("F2", "no frame pop was found after the core")
    core = lines[core_start:i]

    # RULE F2
    f2 = []
    while i < len(lines) and matches_any(lines[i][2], FRAME_POP):
        f2.append(lines[i][2])
        i = i + 1
    removed.append(dict(rule="F2", what="frame pop", lines=f2))

    # RULE P1
    if i + 1 >= len(lines):
        raise Refused("P1", "the unit ends before the safepoint poll")
    if not POLL_TEST.match(lines[i][2]):
        raise Refused("P1", "the instruction after the frame pop is not "
                            "the return poll test "
                            "`cmp 0x28(%r15),%rsp`", lines[i][2])
    m = POLL_JUMP.match(lines[i + 1][2])
    if m is None:
        raise Refused("P1", "the poll test is not followed by "
                            "`ja <target>`", lines[i + 1][2])
    poll_target = int(m.group(1), 16)
    removed.append(dict(rule="P1", what="return safepoint poll",
                        lines=[lines[i][2], lines[i + 1][2]],
                        target=hex(poll_target)))
    i = i + 2

    # RULE R1
    if i >= len(lines) or not RET.match(lines[i][2]):
        raise Refused("R1", "the poll is not followed by `ret`",
                      lines[i][2] if i < len(lines) else None)
    ret_line = lines[i]
    i = i + 1

    # RULE O1
    tail = lines[i:]
    tail_lo = ret_line[0]
    for target, name in ((barrier_target, "the entry barrier"),
                         (poll_target, "the safepoint poll")):
        if target <= tail_lo:
            raise Refused("O1", "%s branches BACKWARD into the body, "
                                "so the out-of-line remainder is not "
                                "reachable from the furniture alone"
                          % name)
    removed.append(dict(rule="O1", what="out-of-line remainder",
                        line_count=len(tail),
                        first=tail[0][2] if tail else None,
                        note="dropped because both stripped branches "
                             "land inside it"))

    # the two checks that make the strip conservative
    for rec in core:
        for name in REGISTER.findall(rec[2]):
            wide = WIDE.get(name)
            if wide in ("rsp", "rbp", "r15"):
                raise Refused("CORE", "the residual core mentions "
                                      "%%%s, so the frame and the "
                                      "thread register are not "
                                      "furniture only" % name, rec[2])
    for rec in core:
        if BRANCHY.match(rec[2]):
            raise Refused("CORE", "the residual core branches; this "
                                  "file handles one straight run only",
                          rec[2])

    return core, removed, ret_line


def rename_core(core, ret_line, parm_registers):
    """the core rewritten into the canonical runnable form."""
    # the traced values, in the JVM's own words: parm0 and parm1.
    plan = {}
    plan[parm_registers[0]] = "rdi"
    plan[parm_registers[1]] = "rsi"

    targets = set(plan.values())
    sources = set(plan.keys())

    # TRACED-VARIABLES-PRIORITY: a rename target touched by anything
    # that is not the value moving into it needs an eviction.  This
    # file refuses instead of guessing one.
    for rec in core:
        for name in REGISTER.findall(rec[2]):
            wide = WIDE.get(name)
            if wide is None:
                continue
            if wide in targets and wide not in sources:
                raise Refused("RENAME", "%%%s is a canonical target and "
                                        "is occupied by a value this "
                                        "file does not trace; an "
                                        "eviction would be needed and "
                                        "canon.py is where eviction "
                                        "lives" % wide, rec[2])

    out = []
    for rec in core:
        text = rec[2]
        out.append(rewrite_one(text, plan))
    out.append("ret")
    del ret_line
    return out, plan


def rewrite_one(text, plan):
    """rename every register mention of one instruction, all at once.

    The substitution is SIMULTANEOUS: each mention is looked up in the
    plan built from the ORIGINAL text, so a permutation like
    rsi -> rdi, rdx -> rsi cannot rename a register twice.
    """

    def one(m):
        name = m.group(1)
        wide = WIDE.get(name)
        if wide is None:
            return m.group(0)
        if wide not in plan:
            return m.group(0)
        width = FAMILY[wide].index(name)
        return "%" + FAMILY[plan[wide]][width]

    return REGISTER.sub(one, text)


def assemble(mnem, as_tool, dump_tool):
    """the bytes an assembler produces from the canonical text."""
    work = tempfile.mkdtemp(prefix="jvm_canon_")
    spath = os.path.join(work, "u.s")
    opath = os.path.join(work, "u.o")
    body = ["        .text", "        .globl u_java", "u_java:"]
    for line in mnem:
        body.append("        %s" % line)
    fh = open(spath, "w")
    fh.write("\n".join(body) + "\n")
    fh.close()
    proc = subprocess.run([as_tool, "-o", opath, spath],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise Refused("ASSEMBLE", "the canonical text did not "
                                  "assemble: %s" % proc.stderr[:400])
    proc = subprocess.run([dump_tool, "-d", opath],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise Refused("ASSEMBLE", "the disassembly failed: %s"
                      % proc.stderr[:400])
    out = []
    back = []
    for raw in proc.stdout.splitlines():
        m = LINE.match(raw.rstrip())
        if m is None:
            continue
        out.extend(m.group(2).split())
        text = (m.group(4) or "").strip()
        if text:
            back.append(re.sub(r"\s+", " ", text))
    return " ".join(out), back


def pick_unit(doc):
    """which unit this pass canonicalises.

    Chosen by MACHINE-FORM facts recorded on the unit -- arity 2,
    operand types (int32, int32), result type int32 -- and by the size
    of its residual body.  The unit's label plays no part in the
    choice; it is carried as a display label and nothing else.
    """
    wanted = []
    for u in doc["units"]:
        if u.get("arity") != 2:
            continue
        if u.get("operand_types") != ["int32", "int32"]:
            continue
        if u.get("result_type") != "int32":
            continue
        wanted.append(u)
    if not wanted:
        return None, "no unit of interp_jvm.json carries arity 2 on "\
                     "(int32, int32) returning int32"
    wanted.sort(key=lambda u: u["bytes_recovered"])
    return wanted[0], None


def parm_registers(unit):
    """the two argument registers, read from the JVM's OWN comment
    lines in the dump.  Not from a calling convention document."""
    got = {}
    for line in unit["parameter_comments"]:
        m = re.match(r"^#\s*parm(\d+):\s*(\w+)\s*=", line.strip())
        if m is None:
            continue
        got[int(m.group(1))] = m.group(2)
    if 0 not in got or 1 not in got:
        raise Refused("ABI", "the dump does not state parm0 and parm1")
    return [got[0], got[1]], [line for line in unit["parameter_comments"]
                              if "parm" in line]


def main():
    indir = HERE
    outdir = HERE
    as_tool = "as"
    dump_tool = "objdump"
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--in":
            i = i + 1
            indir = args[i]
        elif args[i] == "--out":
            i = i + 1
            outdir = args[i]
        elif args[i] == "--cc":
            i = i + 1
            as_tool = args[i]
        elif args[i] == "--dump":
            i = i + 1
            dump_tool = args[i]
        i = i + 1

    doc = json.load(open(os.path.join(indir, "interp_jvm.json")))
    unit, why = pick_unit(doc)
    out = {}
    out["what_this_is"] = "the JVM unit stripped of its runtime "\
                          "furniture and renamed into the canonical "\
                          "runnable form"
    out["source"] = "interp_jvm.json"
    out["pin"] = doc["pin"]
    out["evidence_class"] = "the JVM's own testimony about code it "\
                            "generated at run time, carved out of a "\
                            "print by our lane.  NOT an ELF section a "\
                            "compiler wrote to disk.  This is weaker "\
                            "provenance than every other member of "\
                            "the table and must be marked as such "\
                            "wherever this unit appears."
    out["strip_posture"] = "each removal is a NAMED RULE with a "\
                           "literal pattern; an unmatched pattern is a "\
                           "refusal with the offending line, never a "\
                           "guess"

    if unit is None:
        out["refused"] = dict(rule="SELECT", why=why)
        write(out, outdir)
        print("!! REFUSED: %s" % why)
        return 4

    out["unit"] = dict(id=unit["id"], lang=unit["lang"],
                       operator=unit["label"], method=unit["method"],
                       arity=unit["arity"],
                       operand_types=unit["operand_types"],
                       result_type=unit["result_type"],
                       compiler_tier=unit["compiler_tier"],
                       bytes_recovered=unit["bytes_recovered"])
    out["dump"] = unit["arch_unit"][0]["objdump"]

    try:
        parms, parm_lines = parm_registers(unit)
        out["abi"] = dict(
            parm0=parms[0], parm1=parms[1],
            stated_by="the JVM's own comment lines in the dump",
            lines=parm_lines,
            evidence_class="the tool's own testimony")
        core, removed, ret_line = strip(unit)
        out["stripped"] = removed
        out["residual_core_before_the_rename"] = [r[2] for r in core]
        out["residual_core_bytes_before_the_rename"] = " ".join(
            b for r in core for b in r[1])
        mnem, plan = rename_core(core, ret_line, parms)
        out["rename_map"] = [dict(role="a", was=parms[0], now="rdi"),
                             dict(role="b", was=parms[1], now="rsi")]
        out["rename_note"] = "the substitution is SIMULTANEOUS, so a "\
                             "permutation cannot rename a register "\
                             "twice"
        out["evictions"] = []
        out["canonical_form"] = "; ".join(mnem)
        out["canonical_mnem"] = mnem
        canon_bytes, back = assemble(mnem, as_tool, dump_tool)
        out["canonical_bytes"] = canon_bytes
        out["assembler_read_back"] = back
        out["assembler_self_consistent"] = (back == mnem)
        del plan
    except Refused as exc:
        out["refused"] = dict(rule=exc.rule, why=exc.why, line=exc.line)
        write(out, outdir)
        print("!! REFUSED by rule %s: %s" % (exc.rule, exc.why))
        if exc.line:
            print("   at: %s" % exc.line)
        return 4

    write(out, outdir)
    print("unit                %s (%s)" % (unit["id"], unit["method"]))
    print("parm registers      parm0=%s parm1=%s" % (parms[0], parms[1]))
    for rec in out["stripped"]:
        print("rule %-3s %-24s %s"
              % (rec["rule"], rec["what"],
                 rec.get("lines") or "%d line(s)" % rec["line_count"]))
    print("residual core       %s"
          % "; ".join(out["residual_core_before_the_rename"]))
    print("canonical form      %s" % out["canonical_form"])
    print("canonical bytes     %s" % out["canonical_bytes"])
    print("self consistent     %s" % out["assembler_self_consistent"])
    return 0


def write(out, outdir):
    path = os.path.join(outdir, "jvm_canon.json")
    fh = open(path, "w")
    json.dump(out, fh, indent=1)
    fh.write("\n")
    fh.close()
    print("wrote %s" % path)


if __name__ == "__main__":
    sys.exit(main())
