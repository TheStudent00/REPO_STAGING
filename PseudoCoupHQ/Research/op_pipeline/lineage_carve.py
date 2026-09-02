#!/usr/bin/env python3
"""lineage_carve.py -- TASK 27, part 2: the ARRIVAL / COMPUTATION carve
by LINEAGE CONFLUENCE.

THE RULE THIS IMPLEMENTS (the owner, 2026-08-31, AgentMemory: "THE ARRIVAL /
COMPUTATION BOUNDARY IS LINEAGE CONFLUENCE, NOT 'WHERE THE ARGUMENTS
MEET'").  The retired rule was "the arch opcode where the arguments
first meet"; it fails whenever the ORIGINALS never meet, because one
side was transformed first.  The correct boundary is the first node
whose super-chain includes BOTH lineages -- a's derivatives and b's
derivatives.  ARRIVAL is the maximal prefix of each lineage that
touches one lineage only.  COMPUTATION begins at the first confluence
and runs to the answer.

HOW IT IS COMPUTED HERE, mechanically:

  1. The reachable instruction set comes from `block_cutter.walk_reachable`
     -- the task-20 FIXED cutter (a ret/jmp never falls through into
     alignment padding; a bare <other_symbol> jump target is an
     external exit, never offset 0 into this unit).
  2. Two lineages are seeded by a per-language SEED POLICY (below).
  3. Taint is propagated instruction by instruction over the reachable
     set in address order, through registers (with 32/16/8-bit names
     folded onto their 64-bit family) and through memory slots named by
     their textual addressing form (which is what the -O0 spill/reload
     pattern needs: `mov %rdi,-0x8(%rbp)` then `mov -0x8(%rbp),%rax`).
  4. The CONFLUENCE is the first instruction that reads a value from
     lineage A and a value from lineage B in the same instruction.
  5. If no such instruction exists in the unit, this program REFUSES,
     names the reason, and carves nothing.  A refusal is a result.

SEED POLICIES, declared rather than assumed:

  * `sysv_two_registers` -- the first two integer arguments of a C
     function arrive in %rdi and %rsi.  Evidence class: human
     interpretation of stated design (the x86-64 SysV calling
     convention), cross-checked here against the handler's own DWARF
     formal-parameter list (two parameters, 8 bytes each), which is
     the tool's own testimony.
  * `php_opline_slots` -- php's specialized executor handlers take no
     formal parameters at all (measured: `dwarf_typed_key_t27.json`
     records ZERO formal parameters for all three ZEND_ADD handlers,
     at BOTH the clean anchor and the clean ship build).  Their
     operands are read out of the VM frame.  So a lineage is seeded at
     each distinct `movslq <disp>(%r15),reg` -- an operand-slot offset
     taken from the instruction word -- and the value lineage follows
     that offset into the `(%r14,reg,1)` load.  Exactly two distinct
     displacements are required; anything else is a refusal.  WHICH
     lineage is the left operand is NOT decided by this program: the
     carve needs two distinct lineages, not their order.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim.

Run:
  /tmp/reconnect_venv/bin/python3 lineage_carve.py
"""

import json
import os
import re
import sys

import canon
import canon2
import block_cutter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "lineage_carve.json")

REG = re.compile(r"%([a-z0-9]+)")

FAMILY = {}
for wide, rest in [
    ("rax", ["eax", "ax", "al", "ah"]),
    ("rbx", ["ebx", "bx", "bl", "bh"]),
    ("rcx", ["ecx", "cx", "cl", "ch"]),
    ("rdx", ["edx", "dx", "dl", "dh"]),
    ("rsi", ["esi", "si", "sil"]),
    ("rdi", ["edi", "di", "dil"]),
    ("rbp", ["ebp", "bp", "bpl"]),
    ("rsp", ["esp", "sp", "spl"]),
    ("r8", ["r8d", "r8w", "r8b"]),
    ("r9", ["r9d", "r9w", "r9b"]),
    ("r10", ["r10d", "r10w", "r10b"]),
    ("r11", ["r11d", "r11w", "r11b"]),
    ("r12", ["r12d", "r12w", "r12b"]),
    ("r13", ["r13d", "r13w", "r13b"]),
    ("r14", ["r14d", "r14w", "r14b"]),
    ("r15", ["r15d", "r15w", "r15b"]),
]:
    FAMILY[wide] = wide
    for r in rest:
        FAMILY[r] = wide

# opcodes that WRITE their last AT&T operand and READ the earlier ones
WRITE_LAST_READ_ALL = set([
    "add", "addq", "addl", "sub", "subq", "subl", "and", "andq", "andl",
    "or", "orq", "orl", "xor", "xorq", "xorl", "imul", "adc", "sbb",
    "sar", "sarq", "shr", "shl", "sal", "ror", "rol", "btc", "bts",
    "addsd", "addss", "subsd", "mulsd", "divsd", "orpd", "andpd",
])

# opcodes that WRITE their last operand and read only the source
MOVES = set([
    "mov", "movq", "movl", "movw", "movb", "movabs", "movslq", "movsxd",
    "movzbl", "movzwl", "movsbl", "movswl", "lea", "movsd", "movss",
    "cvtsi2sd", "cvtsi2ss", "cvttsd2si", "pxor",
])

# opcodes that READ both operands and write only flags
READ_ONLY = set(["cmp", "cmpq", "cmpl", "cmpb", "test", "testb", "testl",
                 "ucomisd", "comisd"])


def fold(name):
    return FAMILY.get(name, name)


def regs_in(text):
    out = []
    for m in REG.finditer(text):
        out.append(fold(m.group(1)))
    return out


def is_memory(text):
    return "(" in text or text.startswith("0x") and ")" in text


def mem_key(text):
    """textual addressing form, used as a memory-slot name."""
    return text.strip()


def reads_and_writes(mnem, operands):
    """-> (reads, writes) as lists of place names.  A place is either a
    register family name or a memory slot's textual form.  Deliberately
    simple and explicit; every opcode this pipeline's interpreter slices
    actually contain is covered, and anything else is reported as
    unmodelled by the caller."""
    reads = []
    writes = []
    if not operands:
        return reads, writes, mnem in ("ret", "leave", "endbr64", "nop",
                                       "cltq", "cqto", "cdqe")
    if mnem in MOVES and len(operands) >= 2:
        src = operands[0]
        dst = operands[-1]
        if mnem == "lea":
            # lea computes an ADDRESS: it reads the registers inside the
            # addressing form and never the memory the form names.
            reads.extend(regs_in(src))
        else:
            reads.extend(place_reads(src))
        writes.extend(place_writes(dst))
        return reads, writes, True
    if mnem in WRITE_LAST_READ_ALL and len(operands) >= 2:
        src = operands[0]
        dst = operands[-1]
        reads.extend(place_reads(src))
        reads.extend(place_reads(dst))
        writes.extend(place_writes(dst))
        return reads, writes, True
    if mnem in READ_ONLY:
        for o in operands:
            reads.extend(place_reads(o))
        return reads, writes, True
    if mnem in ("push", "pushq"):
        reads.extend(place_reads(operands[0]))
        return reads, writes, True
    if mnem in ("pop", "popq"):
        writes.extend(place_writes(operands[0]))
        return reads, writes, True
    if mnem in ("neg", "not", "inc", "dec", "sete", "setne", "setg",
                "seta", "sarq", "shrq"):
        reads.extend(place_reads(operands[0]))
        writes.extend(place_writes(operands[0]))
        return reads, writes, True
    if canon.JUMP.match(mnem):
        return reads, writes, True
    if mnem in ("call", "callq"):
        # a call is a lineage sink for this program: whatever the callee
        # does is not in this unit.  Recorded, never modelled.
        for o in operands:
            reads.extend(place_reads(o))
        writes.append("rax")
        return reads, writes, True
    return reads, writes, False


def place_reads(text):
    """every place an operand READS when used as a source."""
    text = text.strip()
    if text.startswith("$"):
        return []
    if is_memory(text):
        out = regs_in(text)
        out.append(mem_key(text))
        return out
    return regs_in(text)


def place_writes(text):
    """the place an operand WRITES when used as a destination.  A memory
    destination writes the slot, not the registers inside its address."""
    text = text.strip()
    if is_memory(text):
        return [mem_key(text)]
    return regs_in(text)


def successors(i, mnem, operands, addr_to_index, unit_base, own_symbol, n):
    """the control-flow successors of ONE instruction, by the same rules
    block_cutter uses (its classify() and its checked jump-target
    resolver are imported, not re-implemented, so defects A and B stay
    fixed here too)."""
    kind = block_cutter.classify(mnem)
    if kind == "ret":
        return []
    if kind == "trap":
        return []
    if kind == "jump":
        outs = []
        for operand in operands:
            off, is_external = block_cutter.find_jump_target_offset_checked(
                operand, own_symbol)
            if is_external:
                continue
            if off is None:
                continue
            target = addr_to_index.get(unit_base + off)
            if target is None:
                continue
            outs.append(target)
        if mnem != "jmp" and i + 1 < n:
            outs.append(i + 1)
        return outs
    if i + 1 < n:
        return [i + 1]
    return []


def transfer(state, reads, writes):
    """-> the state after one instruction.  A written place takes the
    union of the lineages the instruction read; a written place that
    read nothing loses its lineage."""
    out = dict(state)
    seen = set()
    for r in reads:
        seen |= state.get(r, set())
    for w in writes:
        if seen:
            out[w] = set(seen)
        elif w in out:
            del out[w]
    return out, seen


def carve(mnems, addrs, own_symbol, seeds, start_index=0, post_seeds=None):
    """-> a carve record, or the material for a refusal.

    Taint is propagated ALONG CONTROL FLOW to a fixpoint, not in address
    order.  Address order was tried first and is wrong for exactly the
    unit this task is about: ruby's optimised rb_fix_plus places its
    slow (coercion) path at LOWER addresses than its fast path, and a
    call on that slow path clobbered the lineage before the walk ever
    reached the fast path's own instructions.  A join over control-flow
    super-nodes (the union of the states arriving from every reachable
    predecessor) does not have that defect."""
    walk = block_cutter.walk_reachable(
        mnems, addrs, own_symbol, start_index=start_index)
    reached = [x["index"] for x in walk["instructions"]]
    reached_set = set(reached)
    n = len(mnems)
    unit_base = addrs[0] if addrs else 0
    addr_to_index = {}
    for i, a in enumerate(addrs):
        addr_to_index[a] = i

    parsed = {}
    unmodelled = []
    for i in reached:
        line = mnems[i]
        if not line.strip():
            parsed[i] = ("", [], [], [], True)
            continue
        mnem, operands = canon.parse(line)
        reads, writes, modelled = reads_and_writes(mnem, operands)
        parsed[i] = (mnem, operands, reads, writes, modelled)
        if not modelled:
            unmodelled.append({"at_index": i, "instruction": line})

    incoming = {}
    for i in reached:
        incoming[i] = {}
    for place, lineage in seeds.items():
        incoming[start_index][place] = set([lineage])
    # A POST-SEED is a lineage that BEGINS at a named instruction rather
    # than at the unit's entry: php's handlers do not receive operands,
    # they read each operand's stack slot out of the instruction word, so
    # the lineage starts on the instruction that performs that read and
    # must be applied AFTER that instruction's own write, not before it.
    if post_seeds is None:
        post_seeds = {}

    # every reached instruction is processed at least once, then again
    # whenever a super-node's outgoing state grows -- otherwise an
    # instruction that STARTS a lineage (a post-seed) would never run,
    # because nothing had changed upstream of it.
    work = list(reversed(reached))
    rounds = 0
    while work:
        rounds += 1
        if rounds > 200000:
            break
        i = work.pop()
        mnem, operands, reads, writes, _m = parsed[i]
        state, _seen = transfer(incoming[i], reads, writes)
        for place, lineage in post_seeds.get(i, {}).items():
            state[place] = set([lineage])
        outs = successors(i, mnem, operands, addr_to_index, unit_base,
                          own_symbol, n)
        for s in outs:
            if s not in reached_set:
                continue
            changed = False
            for place, lineages in state.items():
                have = incoming[s].get(place, set())
                if not lineages <= have:
                    incoming[s][place] = have | lineages
                    changed = True
            if changed:
                work.append(s)

    trace = []
    confluence = None
    for i in reached:
        mnem, operands, reads, writes, _m = parsed[i]
        seen = set()
        if i in post_seeds:
            trace.append({
                "index": i,
                "instruction": mnems[i],
                "lineages_touched": sorted(post_seeds[i].values()),
                "note": "this instruction STARTS a lineage (post-seed)",
            })
        for r in reads:
            seen |= incoming[i].get(r, set())
        if seen:
            trace.append({
                "index": i,
                "instruction": mnems[i],
                "lineages_touched": sorted(seen),
            })
        if len(seen) >= 2 and confluence is None:
            place_lineages = {}
            for r in sorted(set(reads)):
                have = incoming[i].get(r, set())
                if have:
                    place_lineages[r] = sorted(have)
            confluence = {
                "index": i,
                "address": hex(addrs[i]) if i < len(addrs) else None,
                "instruction": mnems[i],
                "lineages_read": sorted(seen),
                "places_read": sorted(set(reads)),
                "place_lineages": place_lineages,
            }
    return {
        "walk_instruction_count": len(reached),
        "walk_external_exits": walk["external_exits"],
        "walk_unresolved_exits": walk["unresolved_exits"],
        "seeds": dict((k, v) for k, v in seeds.items()),
        "fixpoint_rounds": rounds,
        "confluence": confluence,
        "lineage_trace": trace,
        "unmodelled_instructions": unmodelled,
        "reached_indices": reached,
        "incoming_states": incoming,
    }


def slice_sides(doc, n, side):
    p = doc["probes"][str(n)][side]
    if not p.get("present"):
        return None, p.get("reason")
    return p, None


def addresses_for(side):
    """real instruction addresses for a slice, from its own bytes, offset
    to the symbol's recorded load address."""
    bytes_hex = " ".join(side["bytes"])
    rel = canon2.real_addresses(bytes_hex, expect_count=len(side["mnem"]))
    if rel is None:
        return None
    base = int(side.get("load_address") or "0x0", 16)
    return [base + a for a in rel]


def php_seeds(mnems, addrs, own_symbol):
    """php's specialized handlers take no formal parameters at all
    (measured: dwarf_typed_key_t27.json records ZERO formal parameters
    for all three ZEND_ADD handlers, at the clean anchor build AND at
    the clean ship build).  Their operands are read out of the VM frame
    through the instruction word.

    SEED RULE, in two phases, so that it works at BOTH optimisation
    levels with one mechanism rather than a per-build special case:

      phase 1 -- find every place that holds the instruction-word
                 pointer, by running the same dataflow with a single
                 seed on %r15.  At the ship build the handler reads
                 `0x8(%r15)` directly; at the anchor build it first
                 copies (`mov %r15,%rax`) and then reads `0x8(%rax)`.
                 One rule covers both.
      phase 2 -- every read of `<displacement>(place)` where that place
                 holds the instruction-word pointer STARTS a lineage,
                 one lineage per DISTINCT displacement.

    Which displacement is the left operand is NOT decided here.  The
    carve needs two distinct lineages, not their order; a displacement
    whose lineage is only ever written to (the destination slot) simply
    never reaches a confluence, and that is visible in the record.

    -> (seeds, notes, post_seeds)"""
    seeds = {}
    post = {}
    notes = []
    phase1 = carve(mnems, addrs, own_symbol, {"r15": "instruction_word"})
    holds = {}
    for entry in phase1["lineage_trace"]:
        holds[entry["index"]] = True
    # rebuild the per-instruction state cheaply: re-run the dataflow and
    # keep the incoming map this time.
    states = phase1.get("incoming_states") or {}
    slot = re.compile(r"^(-?0x[0-9a-f]+)\((%[a-z0-9]+)\)$")
    by_disp = {}
    for i in phase1["reached_indices"]:
        line = mnems[i]
        if not line.strip():
            continue
        mnem, operands = canon.parse(line)
        if mnem not in ("movslq", "movsxd", "mov", "movl"):
            continue
        if len(operands) < 2:
            continue
        m = slot.match(operands[0].strip())
        if m is None:
            continue
        base = fold(m.group(2).lstrip("%"))
        state = states.get(i, {})
        if "instruction_word" not in state.get(base, set()):
            continue
        disp = m.group(1)
        places = place_writes(operands[-1].strip())
        if not places:
            continue
        if disp not in by_disp:
            by_disp[disp] = "slot_lineage_%d" % (len(by_disp) + 1)
        name = by_disp[disp]
        seeds[places[0]] = name
        post.setdefault(i, {})[places[0]] = name
        notes.append({
            "lineage": name,
            "seeded_at_index": i,
            "instruction": line,
            "instruction_word_displacement": disp,
            "instruction_word_held_in": base,
        })
    return seeds, notes, post


def out_parameter_first_seeds():
    """php's generic routine declares three formal parameters, all one
    type: `add_function(zval *result, zval *op1, zval *op2)` (DWARF, in
    dwarf_typed_key_t27.json).  The FIRST is where the answer is written,
    so the two operand lineages are the SECOND and THIRD parameters,
    which arrive in %rsi and %rdx under the SysV convention.  The rule is
    stated rather than assumed, and it is recorded on the record."""
    return {"rsi": "argument_lineage_1", "rdx": "argument_lineage_2"}


def ruby_seeds():
    return {"rdi": "argument_lineage_1", "rsi": "argument_lineage_2"}


def carve_language(path, seed_policy, side_order):
    doc = json.load(open(os.path.join(HERE, path)))
    out = []
    for n in sorted(doc["probes"], key=lambda x: int(x)):
        rec = doc["probes"][n]
        sym = rec["meta"]["symbol"]
        for side in side_order:
            here = {
                "unit": "%s/%s" % (doc["meta"]["language"], sym),
                "language": doc["meta"]["language"],
                "symbol": sym,
                "build": side,
                "seed_policy": seed_policy,
                "provenance_is_weaker": True,
            }
            s, why = slice_sides(doc, n, side)
            if s is None:
                here["outcome"] = "REFUSED"
                here["refusal"] = (
                    "no slice exists for this symbol at this build: %s" % why)
                out.append(here)
                continue
            addrs = addresses_for(s)
            if addrs is None:
                here["outcome"] = "REFUSED"
                here["refusal"] = (
                    "the captured bytes do not disassemble to the recorded "
                    "instruction count, so no address list can be built")
                out.append(here)
                continue
            walk = block_cutter.walk_reachable(s["mnem"], addrs, sym)
            reached = [x["index"] for x in walk["instructions"]]
            post = None
            policy = seed_policy
            if sym == "add_function":
                # this one is an ordinary C routine with declared
                # parameters, not a specialized executor handler; the
                # frame-slot policy does not apply to it.
                policy = "sysv_out_parameter_first"
                here["seed_policy"] = policy
            if policy == "php_opline_slots":
                seeds, notes, post = php_seeds(s["mnem"], addrs, sym)
                here["seed_notes"] = notes
                # count DISTINCT LINEAGES, not distinct destination
                # registers: at the anchor build all three slot reads
                # land in %rax one after another, so a register-keyed
                # count reads 1 where there are really three lineages.
                lineage_names = set()
                for _i, mapping in post.items():
                    lineage_names |= set(mapping.values())
                if len(lineage_names) < 2:
                    here["outcome"] = "REFUSED"
                    here["refusal"] = (
                        "fewer than two operand-slot lineages could be seeded "
                        "in this unit (found %d): the handler does not read "
                        "its operands out of the instruction word here"
                        % len(lineage_names))
                    out.append(here)
                    continue
            elif policy == "sysv_out_parameter_first":
                seeds = out_parameter_first_seeds()
            else:
                seeds = ruby_seeds()
            if post is not None:
                got = carve(s["mnem"], addrs, sym, {}, post_seeds=post)
            else:
                got = carve(s["mnem"], addrs, sym, seeds)
            # the per-instruction states are working material for the
            # seed phase, not a record: they hold python sets and they
            # are large.  They never reach the artifact.
            got.pop("incoming_states", None)
            here.update(got)
            if got["confluence"] is None:
                here["outcome"] = "REFUSED"
                here["refusal"] = refusal_reason(s, got)
                out.append(here)
                continue
            ci = got["confluence"]["index"]
            arrival = [i for i in got["reached_indices"] if i < ci]
            computation = [i for i in got["reached_indices"] if i >= ci]
            here["outcome"] = "CARVED"
            here["arrival"] = {
                "what": "the maximal prefix of each lineage that touches one lineage only",
                "instruction_indices": arrival,
                "instructions": [
                    {"index": i, "addr": hex(addrs[i]), "mnem": s["mnem"][i]}
                    for i in arrival],
            }
            here["boundary"] = got["confluence"]
            here["computation_begins_at"] = ci
            # THE COMPUTATION PART is the confluence instruction plus the
            # straight run that continues to work on the joined value in
            # registers.  It stops at the first branch, call, or memory
            # write -- the same separation interp_fastpath.json made for
            # cpython, where the computation was ONE instruction and
            # everything after it was boxing the answer.
            core = []
            core_places = set()
            j = ci
            while j in set(computation):
                line = s["mnem"][j]
                if not line.strip():
                    break
                mnem, operands = canon.parse(line)
                if block_cutter.classify(mnem) != "other":
                    if j != ci:
                        break
                reads, writes, _mod = reads_and_writes(mnem, operands)
                writes_memory = False
                for w in writes:
                    if "(" in w:
                        writes_memory = True
                if writes_memory and j != ci:
                    break
                if j != ci:
                    joined = False
                    for r in reads:
                        if len(got["confluence"]["lineages_read"]) >= 2:
                            if r in core_places:
                                joined = True
                    if not joined:
                        break
                core.append(j)
                core_places = set()
                for w in writes:
                    core_places.add(w)
                j += 1
            after = [i for i in computation if i not in core]
            here["computation_core"] = {
                "what": "the confluence instruction, plus the straight run that keeps working on the joined value in registers; it stops at the first branch, call or memory write",
                "instruction_indices": core,
                "instructions": [
                    {"index": i, "addr": hex(addrs[i]), "mnem": s["mnem"][i]}
                    for i in core],
            }
            here["after_the_answer"] = {
                "what": "everything else the unit does once the joined value exists -- storing it into the frame, writing the result's type tag, advancing the interpreter, the stack-guard check.  Recorded separately rather than folded into the computation, the same separation interp_fastpath.json made for cpython's boxing step.",
                "instruction_indices": after,
                "instructions": [
                    {"index": i, "addr": hex(addrs[i]), "mnem": s["mnem"][i]}
                    for i in after],
            }
            here["computation"] = {
                "what": "from the first confluence to the answer",
                "instruction_indices": computation,
                "instructions": [
                    {"index": i, "addr": hex(addrs[i]), "mnem": s["mnem"][i]}
                    for i in computation],
            }
            out.append(here)
    return out


def refusal_reason(side, got):
    """a real mechanical reason, read off the walk -- never a guess."""
    calls = []
    for i in got["reached_indices"]:
        line = side["mnem"][i]
        if not line.strip():
            continue
        mnem, operands = canon.parse(line)
        if mnem in ("call", "callq"):
            calls.append(line)
    if calls:
        return ("no instruction in this unit reads both lineages: the "
                "lineages leave this unit through a call, so the confluence "
                "is inside a callee, not here.  Call instructions reached: "
                + "; ".join(calls[:6]))
    if got["unmodelled_instructions"]:
        first = got["unmodelled_instructions"][0]
        return ("no confluence found, and this unit contains an instruction "
                "form this program does not model (index %d: %r), so the "
                "absence is not trustworthy and is refused rather than "
                "reported as a carve"
                % (first["at_index"], first["instruction"]))
    return ("no instruction in this unit reads a value from both lineages; "
            "the two lineages never meet inside these bytes")


def refuse_own_output_on_spelling_keys(path):
    """THE MECHANICAL GUARD.  Every pipeline stage that groups or pairs
    units must run the spelling-key check and REFUSE ITS OWN OUTPUT on
    failure.  This function is that refusal: it runs
    check_no_spelling_keys.py over the file just written and returns a
    nonzero exit code if the guard fails."""
    import subprocess
    proc = subprocess.run(
        [sys.executable,
         os.path.join(HERE, "check_no_spelling_keys.py"), path],
        capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    sys.stdout.write(proc.stderr)
    if proc.returncode != 0:
        print("REFUSING OWN OUTPUT: the spelling guard failed on %s" % path)
    return proc.returncode


def main():
    records = []
    records.extend(carve_language("op_units_ruby.json",
                                  "sysv_two_registers", ["anchor", "ship"]))
    records.extend(carve_language("op_units_php.json",
                                  "php_opline_slots", ["anchor", "ship"]))
    php_generic = []
    for r in records:
        if r["symbol"] == "add_function":
            php_generic.append(r)
    out = {
        "meta": {
            "generator": "lineage_carve.py",
            "task": "TASK 27 -- arrival/computation carve by lineage confluence, ruby and php",
            "rule": "AgentMemory 2026-08-31: the boundary is the first node whose super-chain includes BOTH lineages; arrival is the maximal prefix of each lineage that touches one lineage only.",
            "cutter": "block_cutter.walk_reachable (task 20, imported unmodified)",
            "propagation": "taint is propagated ALONG CONTROL FLOW to a fixpoint (join by union over reachable super-nodes), using block_cutter's own classify() and checked jump-target resolver for the successor rules.  Address-order propagation was tried first and was WRONG for one real unit here: ruby's optimised rb_fix_plus places its slow (coercion) path at LOWER addresses than its fast path, and a call on that slow path clobbered the lineage before the fast path was reached.",
            "approximation_stated": "the join is a MAY analysis: a place carries every lineage that could reach it on some path.  A confluence it reports is a real pair of reads on some path; it is not a claim about which path executes.",
            "provenance_is_weaker": True,
        },
        "records": records,
        "summary": {
            "records": len(records),
            "carved": len([r for r in records if r["outcome"] == "CARVED"]),
            "refused": len([r for r in records if r["outcome"] == "REFUSED"]),
        },
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote %s" % OUT)
    guard_code = refuse_own_output_on_spelling_keys(OUT)
    for r in records:
        line = "%-8s %-56s %-8s" % (r["build"], r["symbol"], r["outcome"])
        if r["outcome"] == "CARVED":
            line += " boundary=%s %s" % (r["boundary"]["address"],
                                         r["boundary"]["instruction"])
        else:
            line += " " + r["refusal"][:90]
        print(line)
    print("summary: %s" % out["summary"])
    return guard_code


if __name__ == "__main__":
    sys.exit(main())
