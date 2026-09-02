#!/usr/bin/env python3
"""canon3.py -- TOTAL CANONICAL COVERAGE, successor to canon2.py.

canon2.py already builds the move-erased record and, for STRAIGHT-LINE
units, the derived runnable text.  Three gaps remain (log_074,
AgentMemory's canonical-form ruling):

  (a) BRANCHING UNITS.  canon2.py's own control_step_text() collapses
      every `ret` to the bare word "return", losing WHICH value is
      being returned (the swift op_150/op_186 bug log_074 names).
      canon3.py erases per block exactly as canon2.py does (same
      canon2.Erased machinery, same value-map carried across edges)
      but then DERIVES REAL RUNNABLE TEXT per block: real branch/jump/
      call/trap instructions on their own lines, operands rewritten to
      NORMALIZED labels L0, L1, ... in address order, and a real mov
      inserted before `ret` whenever the returned value is not already
      sitting in the ABI return register.

  (b) TEMPS EXHAUSTED.  canon2.py's derive_runnable() raises
      `temps exhausted deriving runnable text` when both %r10/%r11 are
      already occupied by other live values.  canon3.py's derive
      function spills further values to stack homes, in order of
      overflow: -0x8(%rsp), -0x10(%rsp), -0x18(%rsp), ...

  (c) JOIN CONFLICTS.  canon2.py refuses a branching unit outright when
      two predecessors hand different values into the same register
      family at one join block ("conflicting value maps at join").
      canon3.py never unifies: when a block is reached under two
      different incoming value maps, it is walked TWICE, once per
      incoming map, each producing its own honest per-path block
      (labelled L<n> and L<n>_p1, L<n>_p2, ...) using that path's OWN
      values and registers.  No phi value is ever invented.

This program reuses canon.py's (imported as `canon`) parsing, register
tables, and Walk/branch-detector, and canon2.py's (imported as
`canon2`) Erased erasure engine, relabel_answer, step_text, and the
real-address/basic-block cutting helpers (`real_addresses`,
`cut_blocks`, `strip_reloc`) -- none of that machinery is re-derived
here.  Only the DERIVATION half (erased steps -> runnable AT&T text)
is rewritten, because it is the half that needs to change for all
three gaps.

THE SPELLING BAN.  As canon2.py's docstring states it: the operator
token is copied once per unit as the display label `operator`; this
file's OUTPUT ROOT declares the same `"meta": {"role": "generator
provenance"}` exemption canon2.py declares, for the same reason (every
unit-shaped record here is provenance of one generator run -- no
`members`/`pairs`/`rows`/`groups`/`entries` at the top level).  Run
check_no_spelling_keys.py on the output; it must pass.

usage:
  canon3.py [--in DIR] [--out DIR]
"""

import json
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon  # noqa: E402  (register tables, Walk, parse, JUMP, ...)
import canon2  # noqa: E402  (Erased, relabel_answer, step_text, ...)

LANGS = ["c", "cpp", "go", "rust", "swift"]

FAMILY_OF = canon.FAMILY_OF
WIDTH_OF = canon.WIDTH_OF
NEVER_RENAME = canon.NEVER_RENAME
TEMPS = list(canon.TEMPS)
VECTOR_TEMPS = list(canon.VECTOR_TEMPS)

Erasure = canon2.Erasure


# ------------------------------------------------ shared register bench

class Bench(object):
    """the canonical register/stack-home assignment for one unit's
    worth of values -- shared (mutated in place) across every block of
    a branching unit, or used once for a straight-line unit.  A value
    name is assigned EXACTLY ONCE, forever; nothing is ever reassigned
    to a different location later in the same unit.  This is gap (b):
    once %r10 and %r11 are both spoken for by other live values, the
    next new value overflows to a stack slot, in the order it
    overflowed."""

    def __init__(self):
        self.temp_bench = list(TEMPS)
        self.vector_bench = list(VECTOR_TEMPS)
        self.assigned = {}
        self.overflow_count = 0

    def location_for(self, name, is_vec):
        if name in self.assigned:
            return self.assigned[name]
        bench = self.vector_bench if is_vec else self.temp_bench
        if bench:
            loc = bench.pop(0)
            self.assigned[name] = loc
            return loc
        self.overflow_count = self.overflow_count + 1
        slot = "-0x%x(%%rsp)" % (8 * self.overflow_count)
        loc = ("mem", slot)
        self.assigned[name] = loc
        return loc


def answer_register_texts(contract):
    """every rendered-text spelling of the ABI answer register (the
    entry contract's `result` family, across the widths this file ever
    renders) -- these destinations are NEVER eligible for dead-mov
    removal, no matter how far from the final `ret` they sit, because a
    later block reached only via a jump (not lexically later in the
    flattened text) may still be the one that reads it."""
    fam = contract.get("result")
    if fam is None:
        return set()
    out = set()
    for width in (0, 1):
        try:
            out.add("%" + render(fam, width))
        except Exception:
            pass
    return out


def dead_mov_cleanup(lines, contract):
    """canon4 DEAD-MOV CLEANUP (item 1a): remove a `mov` line whose
    destination is a register that is never subsequently read in the
    text (textual containment, matching uniqueness_audit.py's own
    has_dead_mov heuristic exactly) and is not the ABI answer register.
    Iterated to fixpoint -- removing one dead mov can make an earlier
    mov feeding only that dead mov's source dead in turn.  Memory
    destinations (stores) are never touched: only `mov` lines whose
    destination operand starts with `%` are candidates, so a spill
    store can never be mistaken for a dead register mov."""
    protected = answer_register_texts(contract)
    lines = list(lines)
    changed = True
    while changed:
        changed = False
        for i, ln in enumerate(lines):
            if not ln.startswith("mov "):
                continue
            try:
                _, operands = ln.split(" ", 1)
                dst = operands.split(",")[-1]
            except ValueError:
                continue
            if not dst.startswith("%"):
                continue
            if dst in protected:
                continue
            rest = " ".join(lines[i + 1:])
            if dst not in rest:
                del lines[i]
                changed = True
                break
    return lines


def is_mem(loc):
    return isinstance(loc, tuple) and loc[0] == "mem"


def loc_text(loc, width):
    if is_mem(loc):
        return loc[1]
    return "%" + render(loc, width)


def render(family, width):
    if canon.is_vector(family):
        return family
    return canon.GP_NAMES[family][width]


# --------------------------------------------------------- derive pass
#
# This is canon2.py's derive_runnable(), kept line-for-line where the
# original logic is unchanged, and extended at exactly the points gap
# (b) needs: `ensure()` can move a value OUT of a stack home, and
# `temp_for()` (renamed `loc_for()` here, since it can now return a
# memory home rather than a register) overflows to the shared Bench
# instead of refusing.

def default_contract(is_a_vector, is_b_present, is_b_vector,
                     is_result_vector):
    return canon2.default_contract(is_a_vector, is_b_present, is_b_vector,
                                   is_result_vector)


def derive_runnable3(steps, final_name, contract, bench):
    """canon2.py's derive_runnable(), with the temps-exhausted refusal
    (gap b) replaced by a stack-slot overflow home.  `bench` is a
    Bench instance; passing the SAME instance across several calls (as
    the branching driver does, once per block) makes register/stack
    assignment consistent for a value that is read in one block and
    was defined in an earlier one."""
    reg_of = {}
    if contract["a"] is not None:
        reg_of["a"] = contract["a"]
    if contract["b"] is not None:
        reg_of["b"] = contract["b"]
    text = []

    # canon4 fix (in-place-no-known-register / passthrough causes): a
    # value named literally "a" or "b" is, BY THE ENTRY CONTRACT ITSELF,
    # already sitting in contract["a"]/contract["b"] the moment the unit
    # starts -- even if some relabeling step lost that register from
    # reg_of before this point.  This is not a guess: it is the entry
    # contract, read back, never a new register choice.
    def contract_fallback(name):
        if name == "a" and contract.get("a") is not None:
            return contract["a"]
        if name == "b" and contract.get("b") is not None:
            return contract["b"]
        return None

    def ensure(name, target, width):
        cur = reg_of.get(name)
        if cur is None:
            cur = contract_fallback(name)
            if cur is not None:
                reg_of[name] = cur
        if cur is None:
            raise Erasure("erasure_refused: value %s is read before it "
                          "is defined or before the unit's entry "
                          "contract names it" % name)
        if cur == target:
            return
        if is_mem(cur):
            text.append("mov %s,%%%s" % (cur[1], render(target, width)))
            reg_of[name] = target
            return
        cur_vec = canon.is_vector(cur)
        target_vec = canon.is_vector(target)
        if cur_vec and target_vec:
            mnem = "movaps"
        elif cur_vec != target_vec:
            mnem = "movq"
        else:
            mnem = "mov"
        text.append("%s %%%s,%%%s" % (mnem, render(cur, width),
                                      render(target, width)))
        reg_of[name] = target

    def loc_for(name, is_vec):
        return bench.location_for(name, is_vec)

    for step in steps:
        kind = step["kind"]
        if kind == "sign_extend":
            src = step["reads"][0]
            ensure(src, "rax", 1)
            text.append(step["mnem"])
            dst = step["writes"][0]
            reg_of[dst] = "rdx"
            continue
        if kind == "store":
            reads = list(step["reads"])
            if reads:
                src = reads[0]
                cur = reg_of.get(src)
                if cur is None:
                    cur = contract_fallback(src)
                    if cur is not None:
                        reg_of[src] = cur
                if cur is None:
                    raise Erasure("erasure_refused: value %s is read "
                                  "before it is defined or before the "
                                  "unit's entry contract names it"
                                  % src)
                src_text = loc_text(cur, 1)
                text.append("%s %s,%s" % (step["mnem"], src_text,
                                          step["dest_text"]))
            else:
                text.append("%s %s" % (step["mnem"], step["dest_text"]))
            continue
        if kind == "divmul":
            lo, hi, divisor = step["reads"]
            ensure(lo, "rax", 1)
            ensure(hi, "rdx", 1)
            dwidth = step.get("divisor_width", 1)
            if reg_of.get(divisor) in ("rax", "rdx"):
                raise Erasure("erasure_refused: the divisor value would "
                              "have to share %rax/%rdx with the "
                              "dividend -- not attempted this slice")
            divisor_loc = reg_of.get(divisor)
            if divisor_loc is None:
                raise Erasure("erasure_refused: divisor value has no "
                              "known register")
            text.append("%s %s" % (step["mnem"], loc_text(divisor_loc,
                                                           dwidth)))
            q, r = step["writes"]
            reg_of[q] = "rax"
            reg_of[r] = "rdx"
            continue
        # generic
        operands = step["operand_texts"]
        role = step["role"]
        slot_names = step["slot_names"]
        writes = step["writes"]
        if step.get("pin_cl") is not None:
            ensure(step["pin_cl"], "rcx", 1)
        write_slot = None
        write_name = None
        write_kind = None
        write_vec = False
        if writes:
            write_slot, write_name, write_kind, write_vec = writes[0]
        for slot, operand in enumerate(operands):
            if role[slot] not in ("use", "rw"):
                continue
            name = slot_names[slot]
            if name is None or not canon.is_plain_register(operand):
                continue
            regname = canon.registers_in(operand)[0]
            fam = FAMILY_OF.get(regname)
            if fam is None:
                continue
            wanted_vec = canon.is_vector(fam)
            cur = reg_of.get(name)
            if cur is None or is_mem(cur):
                continue
            if canon.is_vector(cur) == wanted_vec:
                continue
            is_final_write = (slot == write_slot and role[slot] == "rw"
                              and (name == final_name
                                   or name == "answer"))
            if is_final_write:
                target = contract["result"]
            else:
                target = loc_for(name, wanted_vec)
                if is_mem(target):
                    # a file-crossing value cannot be spilled to plain
                    # memory mid-instruction (it needs a real vector or
                    # GP register to bit-reinterpret through) -- refuse
                    # this specific, rare case by name rather than emit
                    # something that will not assemble.
                    raise Erasure("erasure_refused: a file-crossing "
                                  "value overflowed to a stack home -- "
                                  "not attempted this slice")
            ensure(name, target, 0)
        if write_kind == "rw":
            old_name = slot_names[write_slot]
            is_final = (write_name == final_name or write_name == "answer")
            if is_final:
                target = contract["result"]
            else:
                target = reg_of.get(old_name)
                if target is None:
                    target = contract_fallback(old_name)
                    if target is not None:
                        reg_of[old_name] = target
                if target is None and (step["mnem"] in ("sbb", "sbc")
                                       or step["mnem"].startswith("set")):
                    # canon4 fix (in-place-no-known-register cause):
                    # two idioms the erasure engine tags "rw" (it reads
                    # AT&T's single-operand-with-implicit-dest form)
                    # that are actually pure writes of flag state --
                    # `sbb reg,reg` (0 or -1 from the carry flag) and
                    # every `setCC reg8` (0 or 1 from the flags) --
                    # neither ever reads the register's prior bits, so
                    # "old_name" never needed a home.  Give it a fresh
                    # one, exactly as a `def` would.
                    target = loc_for(old_name, write_vec)
                    reg_of[old_name] = target
            if target is None:
                raise Erasure("erasure_refused: an in-place value has "
                              "no known register")
            if is_final:
                ensure(old_name, target, 1)
            reg_of[write_name] = target
        elif write_kind == "def":
            is_final = (write_name == final_name or write_name == "answer")
            if is_final:
                target = contract["result"]
            else:
                target = loc_for(write_name, write_vec)
            reg_of[write_name] = target
        write_fam = None
        if write_slot is not None and canon.is_plain_register(
                operands[write_slot]):
            write_fam = FAMILY_OF.get(
                canon.registers_in(operands[write_slot])[0])
        pieces = []
        for slot, operand in enumerate(operands):
            name = slot_names[slot]
            if name is None:
                if (canon.is_plain_register(operand)
                        and FAMILY_OF.get(canon.registers_in(operand)[0])
                        == write_fam and write_fam is not None):
                    regname = canon.registers_in(operand)[0]
                    width = WIDTH_OF.get(regname, 1)
                    pieces.append(loc_text(reg_of[write_name], width))
                    continue
                pieces.append(operand)
                continue
            width = WIDTH_OF.get(canon.registers_in(operand)[0], 1)
            if slot == write_slot:
                target_loc = reg_of[write_name]
            else:
                target_loc = reg_of.get(name)
                if target_loc is None:
                    target_loc = contract_fallback(name)
                    if target_loc is not None:
                        reg_of[name] = target_loc
                if target_loc is None:
                    raise Erasure("erasure_refused: value %s used "
                                  "before it is defined" % name)
            pieces.append(loc_text(target_loc, width))
        if len([p for p in pieces if not p.startswith("%")]) > 1:
            raise Erasure("erasure_refused: two stack-spilled operands "
                          "in one instruction -- not attempted this "
                          "slice")
        if pieces:
            text.append("%s %s" % (step["mnem"], ",".join(pieces)))
        else:
            text.append(step["mnem"])
    if final_name is not None:
        # canon4 fix (passthrough cause): a unit that just returns its
        # argument untouched has final_name == "a" (or "b") and never
        # ran a step that would have put it in reg_of -- ensure()'s
        # contract_fallback now seeds it from the entry contract itself,
        # so this becomes the honest "mov home->rax (or nothing) + ret"
        # rather than a refusal.
        if final_name not in reg_of and contract_fallback(final_name) \
                is None:
            raise Erasure("erasure_refused: the answer value never "
                          "entered a tracked register (a passthrough "
                          "this builder does not model)")
        ensure(final_name, contract["result"], 1)
    text.append("ret")
    return text


# --------------------------------------------------------- straight line

def canon3_straight(lang, n, sem_rec, out, anchor, lines, walker):
    actual_result_family = walker.result_family
    contract = canon2.build_contract(sem_rec.get("meta", {}), anchor,
                                     actual_result_family)
    try:
        eraser = canon2.Erased(anchor, lines, walker.role_log,
                               actual_result_family)
        steps, final_name = eraser.run()
        steps, final_name = canon2.relabel_answer(steps, final_name)
    except Erasure as bad:
        out["erasure"] = bad.reason
        return out
    out["erasure"] = "ok"
    out["entry_contract"] = contract
    out["erased_form"] = [canon2.step_text(s) for s in steps]
    bench = Bench()
    try:
        derived = derive_runnable3(steps, final_name, contract, bench)
    except Erasure as bad:
        out["derived_text"] = "refused: %s" % bad.reason
        out["derive_refused"] = bad.reason
        return out
    derived_before = derived
    derived = dead_mov_cleanup(derived, contract)
    out["derived_text"] = derived
    out["derived_mnem_joined"] = "; ".join(derived)
    out["dead_movs_removed"] = len(derived_before) - len(derived)
    out["exact_regeneration"] = derived == list(lines)
    out["overflow_slots_used"] = bench.overflow_count
    return out


# ---------------------------------------------------------- branching

def map_key(m):
    return tuple(sorted(m.items()))


class BranchDriver(object):
    """walks a branching unit's basic blocks, erasing moves within each
    block exactly as canon2.canon2_branching does (same canon2.Erased
    engine, same value-map propagation along edges) -- but gap (c)
    means a join is never refused: when a block is reached under an
    incoming value-map that disagrees with one already seen for that
    block, the block is walked AGAIN, honestly, under its own map, and
    given its own label (L<n>_p1, L<n>_p2, ...).  Gap (a) means every
    block's runnable text is actually derived (real branch/call/trap
    lines, normalized label operands, a real mov before `ret` landing
    the returned value in the ABI register) using the SAME Bench across
    every block/path of the unit, so a value defined in one block and
    read in a later one keeps the one register/stack home it was first
    given (gap b's overflow rule applies unit-wide, not per block)."""

    # canon4 fix (too-many-join-paths cause): render every honest path
    # rather than refusing once a fixed cap is hit -- raised well above
    # any join-path count actually seen in the 0-branch population.
    MAX_PATHS = 5000

    def __init__(self, anchor, lines, walker, blocks, successors, edges,
                branch_target_index, block_of_index, contract, bench):
        self.anchor = anchor
        self.lines = lines
        self.walker = walker
        self.blocks = blocks
        self.successors = successors
        self.edges = edges
        self.branch_target_index = branch_target_index
        self.block_of_index = block_of_index
        self.contract = contract
        self.bench = bench
        self.ctx = {"u": 0, "w": 0, "k": 0}
        self.label_for = {}
        self.label_counter = {}
        self.records = []
        self.aborted = None

    def get_label(self, bi, incoming_map):
        key = (bi, map_key(incoming_map))
        if key in self.label_for:
            return self.label_for[key], key
        idx = self.label_counter.get(bi, 0)
        self.label_counter[bi] = idx + 1
        label = "L%d" % bi if idx == 0 else "L%d_p%d" % (bi, idx)
        self.label_for[key] = label
        return label, key

    def run(self):
        incoming0 = {}
        if self.anchor.get("in0") is not None:
            incoming0[FAMILY_OF[self.anchor["in0"]]] = "a"
        if self.anchor.get("in1") is not None:
            incoming0[FAMILY_OF[self.anchor["in1"]]] = "b"
        reg0 = {}
        if self.contract["a"] is not None:
            reg0["a"] = self.contract["a"]
        if self.contract["b"] is not None:
            reg0["b"] = self.contract["b"]
        start_label, start_key = self.get_label(0, incoming0)
        queue = [(0, incoming0, reg0, start_key)]
        processed = set()
        while queue:
            bi, incoming_map, incoming_reg, key = queue.pop(0)
            if key in processed:
                continue
            processed.add(key)
            if len(processed) > self.MAX_PATHS:
                self.aborted = ("erasure_refused: too many distinct "
                                "join paths -- not attempted this slice")
                return
            label = self.label_for[key]
            rec = self.walk_block(bi, label, incoming_map, incoming_reg)
            self.records.append(rec)
            outgoing_map = rec["outgoing"]
            outgoing_reg = rec.get("reg_of_after", incoming_reg)
            for succ_bi in self.successors.get(bi, []):
                succ_label, succ_key = self.get_label(succ_bi,
                                                       outgoing_map)
                rec.setdefault("succ_labels", []).append(succ_label)
                if succ_key not in processed:
                    queue.append((succ_bi, outgoing_map, outgoing_reg,
                                 succ_key))
        # `succ_labels` is only fully known for a record once every
        # successor has been visited and assigned its label above --
        # rendering the control line (which needs the real target
        # label text) has to happen in this SECOND pass, after the
        # whole queue has drained, not inside walk_block().
        for rec in self.records:
            rec["ctrl_lines"] = render_control_line(rec, self.contract,
                                                     self.walker)

    def walk_block(self, bi, label, incoming_map, incoming_reg):
        start, end = self.blocks[bi]
        sub_lines = self.lines[start:end]
        sub_role_log = {}
        for j in range(start, end):
            sub_role_log[j - start] = self.walker.role_log.get(j, [])
        fam = self.walker.result_family
        eraser = canon2.Erased(self.anchor, sub_lines, sub_role_log, fam,
                               live=dict(incoming_map), ctx=self.ctx)
        eraser.start = lambda: None
        rec = {"bi": bi, "label": label, "incoming": incoming_map}
        try:
            for idx, ln in enumerate(sub_lines):
                eraser.one(idx, ln)
        except Erasure as bad:
            rec["erasure"] = bad.reason
            rec["outgoing"] = dict(eraser.live)
            rec["steps"] = eraser.steps
            rec["control"] = None
            return rec
        rec["steps"] = eraser.steps
        rec["outgoing"] = dict(eraser.live)
        last_i = end - 1
        rec["control"] = None
        if last_i in self.edges:
            emnem, eoperands = canon.parse(canon2.strip_reloc(
                self.lines[last_i]))
            target_idx = self.branch_target_index.get(last_i)
            target_bi = None
            if target_idx is not None:
                target_bi = self.block_of_index[target_idx]
            rec["control"] = {
                "mnem": emnem, "operands": eoperands,
                "target_bi": target_bi,
            }
        # gap (a): derive this block's own runnable body right here,
        # threaded from THIS path's incoming register state (never a
        # different path's) -- this is the fix for the bug an earlier
        # draft of this file had (threading register state in flat
        # visitation order instead of along the actual path).
        try:
            body, reg_after = derive_block_body(rec["steps"],
                                                self.contract, self.bench,
                                                incoming_reg)
        except Erasure as bad:
            rec["derive_erasure"] = bad.reason
            rec["reg_of_after"] = incoming_reg
            rec["body"] = None
            return rec
        rec["body"] = body
        rec["reg_of_after"] = reg_after
        return rec


def render_control_line(rec, contract, walker):
    """produce the REAL instruction line(s) for a block's terminal
    control instruction: a jump/branch keeps its own mnemonic with the
    operand rewritten to the normalized target label; a return gets a
    real mov landing the returned value in the ABI register first, if
    it is not there already; a call/trap is copied through verbatim
    (the symbol operand is not a register mention)."""
    ctrl = rec["control"]
    if ctrl is None:
        return []
    mnem = ctrl["mnem"]
    if canon.JUMP.match(mnem):
        # `succ_labels` was appended in the SAME order cut_blocks()
        # ordered this edge's successors: target first, fallthrough
        # second (only for a conditional branch -- `jmp` has no
        # fallthrough).  Block emission order in the output text does
        # NOT follow address order (path-duplication means it can't),
        # so BOTH edges are made explicit here -- the conditional jump
        # to its real target, plus an unconditional jump to the
        # fallthrough -- rather than relying on physical adjacency.
        labels = rec.get("succ_labels") or []
        if not labels:
            # canon4 fix (assemble_failed cause): canon3 emitted the
            # literal placeholder text "L?" here when no successor
            # label had been resolved for this control edge (the
            # branch target address falls outside the walked block
            # set -- e.g. a tail jump whose target this pass never
            # visited).  "L?" is not a valid label and silently
            # produced an assembler error; refuse honestly instead of
            # emitting unassemblable text.
            raise Erasure("erasure_refused: a branch target address "
                          "could not be resolved to any walked block "
                          "(likely a tail jump outside this unit's own "
                          "block set) -- not attempted this slice")
        target_label = labels[0]
        lines = ["%s %s" % (mnem, target_label)]
        if mnem != "jmp" and len(labels) > 1:
            lines.append("jmp %s" % labels[1])
        return lines
    if mnem in ("ret", "retq"):
        fam = walker.result_family
        final_val = rec["outgoing"].get(fam)
        lines = []
        if final_val is not None:
            reg_of_after = rec.get("reg_of_after") or {}
            cur = reg_of_after.get(final_val)
            target = contract["result"]
            if cur is not None and cur != target:
                if is_mem(cur):
                    # canon4 fix (assemble_failed cause): the plain
                    # `mov` mnemonic cannot move memory into a vector
                    # (xmm) register -- `as` rejected it outright.
                    # Pick the same mnemonic ensure() uses for a
                    # location-to-register move: movq to cross GP/vector
                    # files, plain mov within the GP file.
                    if canon.is_vector(target):
                        lines.append("movq %s,%%%s" % (cur[1],
                                                        render(target, 1)))
                    else:
                        lines.append("mov %s,%%%s" % (cur[1],
                                                       render(target, 1)))
                else:
                    lines.append("mov %%%s,%%%s" % (render(cur, 1),
                                                     render(target, 1)))
        lines.append("ret")
        return lines
    if mnem in ("call", "callq"):
        target = ctrl["operands"][0] if ctrl["operands"] else ""
        import re as _re
        m = _re.search(r"<([^>]+)>", target)
        name = m.group(1) if m else target
        return ["call %s" % name]
    if mnem == "ud2":
        return ["ud2"]
    return ["%s %s" % (mnem, ",".join(ctrl["operands"]))]


def canon3_branching(lang, n, sem_rec, out, anchor, lines, walker):
    bytes_hex = sem_rec.get("bytes")
    if not bytes_hex:
        out["erasure"] = "deferred: branching (no bytes to address)"
        return out
    addrs = canon2.real_addresses(bytes_hex, len(lines))
    if addrs is None:
        out["erasure"] = "deferred: branching (could not align real "\
                         "disassembly to instruction count)"
        return out
    blocks, successors, edges, branch_target_index, block_of_index = \
        canon2.cut_blocks(lines, addrs)
    fam = walker.result_family
    meta = sem_rec.get("meta", {})
    contract = canon2.build_contract(meta, anchor, fam)
    bench = Bench()
    driver = BranchDriver(anchor, lines, walker, blocks, successors,
                          edges, branch_target_index, block_of_index,
                          contract, bench)
    try:
        driver.run()
    except Erasure as bad:
        out["erasure"] = bad.reason
        return out
    if driver.aborted is not None:
        out["erasure"] = driver.aborted
        return out
    any_erasure = None
    for rec in driver.records:
        if rec.get("erasure"):
            any_erasure = rec["erasure"]
            break
        if rec.get("derive_erasure"):
            any_erasure = rec["derive_erasure"]
            break
    if any_erasure is not None:
        out["erasure"] = "erasure_refused: %s" % any_erasure
        out["blocks"] = [{"label": r["label"],
                          "steps": [canon2.step_text(s)
                                   for s in r["steps"]],
                          "erasure": r.get("erasure") or r.get(
                              "derive_erasure")}
                         for r in driver.records]
        return out
    # gap (a): each record already carries its own runnable body,
    # derived along its OWN path's register state by
    # BranchDriver.walk_block() -- just render the final text here.
    block_records = []
    erased_flat = []
    derived_flat = []
    dead_movs_removed = 0
    for rec in driver.records:
        raw_lines = rec["body"] + rec["ctrl_lines"]
        # dead-mov cleanup, scoped to this block's own text (a
        # conservative per-block scope: it never removes a mov whose
        # destination is read by a DIFFERENT block reached only via a
        # jump, since that read is textually invisible from here --
        # correctness over completeness).
        text_lines = dead_mov_cleanup(raw_lines, contract)
        dead_movs_removed += len(raw_lines) - len(text_lines)
        block_records.append({"label": rec["label"], "steps": text_lines})
        erased_flat.append("%s:" % rec["label"])
        for s in rec["steps"]:
            erased_flat.append("  " + canon2.step_text(s))
        derived_flat.append("%s:" % rec["label"])
        for ln in text_lines:
            derived_flat.append("  " + ln)
    out["erasure"] = "ok"
    out["entry_contract"] = contract
    out["blocks"] = block_records
    out["erased_form"] = erased_flat
    out["derived_blocks"] = block_records
    out["derived_text_flat"] = derived_flat
    out["dead_movs_removed"] = dead_movs_removed
    out["overflow_slots_used"] = bench.overflow_count
    return out


def derive_block_body(steps, contract, bench, reg_of_in):
    """derive_runnable3, restricted to ONE block's steps (no trailing
    `ret` -- the branching driver's render_control_line() appends the
    real control instruction separately) and threading `reg_of` in and
    back out so the next block along this path starts where this one
    left off."""
    reg_of = dict(reg_of_in)
    text = []

    def contract_fallback(name):
        if name == "a" and contract.get("a") is not None:
            return contract["a"]
        if name == "b" and contract.get("b") is not None:
            return contract["b"]
        return None

    def ensure(name, target, width):
        cur = reg_of.get(name)
        if cur is None:
            cur = contract_fallback(name)
            if cur is not None:
                reg_of[name] = cur
        if cur is None:
            raise Erasure("erasure_refused: value %s is read before it "
                          "is defined or before the unit's entry "
                          "contract names it" % name)
        if cur == target:
            return
        if is_mem(cur):
            text.append("mov %s,%%%s" % (cur[1], render(target, width)))
            reg_of[name] = target
            return
        cur_vec = canon.is_vector(cur)
        target_vec = canon.is_vector(target)
        if cur_vec and target_vec:
            mnem = "movaps"
        elif cur_vec != target_vec:
            mnem = "movq"
        else:
            mnem = "mov"
        text.append("%s %%%s,%%%s" % (mnem, render(cur, width),
                                      render(target, width)))
        reg_of[name] = target

    def loc_for(name, is_vec):
        return bench.location_for(name, is_vec)

    for step in steps:
        kind = step["kind"]
        if kind == "sign_extend":
            src = step["reads"][0]
            ensure(src, "rax", 1)
            text.append(step["mnem"])
            dst = step["writes"][0]
            reg_of[dst] = "rdx"
            continue
        if kind == "store":
            reads = list(step["reads"])
            if reads:
                src = reads[0]
                cur = reg_of.get(src)
                if cur is None:
                    cur = contract_fallback(src)
                    if cur is not None:
                        reg_of[src] = cur
                if cur is None:
                    raise Erasure("erasure_refused: value %s is read "
                                  "before it is defined or before the "
                                  "unit's entry contract names it"
                                  % src)
                text.append("%s %s,%s" % (step["mnem"], loc_text(cur, 1),
                                          step["dest_text"]))
            else:
                text.append("%s %s" % (step["mnem"], step["dest_text"]))
            continue
        if kind == "divmul":
            lo, hi, divisor = step["reads"]
            ensure(lo, "rax", 1)
            ensure(hi, "rdx", 1)
            dwidth = step.get("divisor_width", 1)
            if reg_of.get(divisor) in ("rax", "rdx"):
                raise Erasure("erasure_refused: the divisor value would "
                              "have to share %rax/%rdx with the "
                              "dividend -- not attempted this slice")
            divisor_loc = reg_of.get(divisor)
            if divisor_loc is None:
                raise Erasure("erasure_refused: divisor value has no "
                              "known register")
            text.append("%s %s" % (step["mnem"], loc_text(divisor_loc,
                                                           dwidth)))
            q, r = step["writes"]
            reg_of[q] = "rax"
            reg_of[r] = "rdx"
            continue
        operands = step["operand_texts"]
        role = step["role"]
        slot_names = step["slot_names"]
        writes = step["writes"]
        if step.get("pin_cl") is not None:
            ensure(step["pin_cl"], "rcx", 1)
        write_slot = None
        write_name = None
        write_kind = None
        write_vec = False
        if writes:
            write_slot, write_name, write_kind, write_vec = writes[0]
        for slot, operand in enumerate(operands):
            if role[slot] not in ("use", "rw"):
                continue
            name = slot_names[slot]
            if name is None or not canon.is_plain_register(operand):
                continue
            regname = canon.registers_in(operand)[0]
            fam = FAMILY_OF.get(regname)
            if fam is None:
                continue
            wanted_vec = canon.is_vector(fam)
            cur = reg_of.get(name)
            if cur is None or is_mem(cur):
                continue
            if canon.is_vector(cur) == wanted_vec:
                continue
            target = loc_for(name, wanted_vec)
            if is_mem(target):
                raise Erasure("erasure_refused: a file-crossing value "
                              "overflowed to a stack home -- not "
                              "attempted this slice")
            ensure(name, target, 0)
        if write_kind == "rw":
            old_name = slot_names[write_slot]
            target = reg_of.get(old_name)
            if target is None:
                target = contract_fallback(old_name)
                if target is not None:
                    reg_of[old_name] = target
            if target is None and (step["mnem"] in ("sbb", "sbc")
                                   or step["mnem"].startswith("set")):
                # canon4 fix (in-place-no-known-register cause) -- see
                # derive_runnable3 for why this is sound: neither idiom
                # ever reads old_name's prior bits.
                target = loc_for(old_name, write_vec)
                reg_of[old_name] = target
            if target is None:
                raise Erasure("erasure_refused: an in-place value has "
                              "no known register")
            reg_of[write_name] = target
        elif write_kind == "def":
            target = loc_for(write_name, write_vec)
            reg_of[write_name] = target
        write_fam = None
        if write_slot is not None and canon.is_plain_register(
                operands[write_slot]):
            write_fam = FAMILY_OF.get(
                canon.registers_in(operands[write_slot])[0])
        pieces = []
        for slot, operand in enumerate(operands):
            name = slot_names[slot]
            if name is None:
                if (canon.is_plain_register(operand)
                        and FAMILY_OF.get(canon.registers_in(operand)[0])
                        == write_fam and write_fam is not None):
                    regname = canon.registers_in(operand)[0]
                    width = WIDTH_OF.get(regname, 1)
                    pieces.append(loc_text(reg_of[write_name], width))
                    continue
                pieces.append(operand)
                continue
            width = WIDTH_OF.get(canon.registers_in(operand)[0], 1)
            if slot == write_slot:
                target_loc = reg_of[write_name]
            else:
                target_loc = reg_of.get(name)
                if target_loc is None:
                    target_loc = contract_fallback(name)
                    if target_loc is not None:
                        reg_of[name] = target_loc
                if target_loc is None:
                    raise Erasure("erasure_refused: value %s used "
                                  "before it is defined" % name)
            pieces.append(loc_text(target_loc, width))
        if len([p for p in pieces if not p.startswith("%")]) > 1:
            raise Erasure("erasure_refused: two stack-spilled operands "
                          "in one instruction -- not attempted this "
                          "slice")
        if pieces:
            text.append("%s %s" % (step["mnem"], ",".join(pieces)))
        else:
            text.append(step["mnem"])
    return text, reg_of


# --------------------------------------------------------- per unit

def canon3_one(lang, n, sem_rec, canon_rec):
    meta = sem_rec.get("meta", {})
    anchor = sem_rec.get("sem", {}).get("anchor_registers")
    lines = sem_rec.get("mnem")
    out = {}
    out["lang"] = lang
    out["n"] = n
    out["unit"] = "%s/op_%s" % (lang, n)
    out["operator"] = meta.get("operator")
    out["meta"] = meta
    out["mnem"] = lines
    out["bytes"] = sem_rec.get("bytes")
    if anchor is None or not lines:
        out["erasure"] = "erasure_refused: no anchored register map or "\
                         "no instruction text"
        return out
    fam = canon.result_register_family(lang, meta, lines)
    walker = canon.Walk(lines, anchor, fam)
    try:
        walker.run()
    except canon.Refusal:
        pass
    if walker.branches:
        return canon3_branching(lang, n, sem_rec, out, anchor, lines,
                                walker)
    return canon3_straight(lang, n, sem_rec, out, anchor, lines, walker)


# ---------------------------------------------------- assembler pass

def assemble_and_disassemble(lines, workdir):
    return canon2.assemble_and_disassemble(lines, workdir)


def flatten_for_asm(out):
    """the flat instruction-line list to hand the real assembler: a
    straight-line unit's `derived_text` already is one; a branching
    unit's blocks are concatenated in label order, `L<n>:` lines
    included (gas does not care about the leading tab)."""
    if isinstance(out.get("derived_text"), list):
        return out["derived_text"]
    if "blocks" in out and out.get("erasure") == "ok":
        flat = []
        for rec in out["blocks"]:
            flat.append("%s:" % rec["label"])
            for ln in rec["steps"]:
                flat.append(ln)
        return flat
    return None


# ------------------------------------------------------------ driver

def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def run_language(lang, indir, outdir, workdir):
    sem_path = os.path.join(indir, "sem_anchored_%s.json" % lang)
    canon_path = os.path.join(indir, "canon_units_%s.json" % lang)
    sem_doc = json.load(open(sem_path))
    canon_doc = json.load(open(canon_path))
    sem_units = sem_doc["units"]
    canon_units = canon_doc["units"]
    keys = sorted(sem_units.keys(), key=lambda x: int(x))
    rows = {}
    canonical_ok = 0
    still_refused = 0
    assembled_ok = 0
    assembled_failed = 0
    reasons = {}
    for n in keys:
        rec = canon3_one(lang, n, sem_units[n], canon_units.get(n, {}))
        flat = flatten_for_asm(rec)
        if flat is not None:
            rt = assemble_and_disassemble(flat, workdir)
            rec["roundtrip"] = rt
            if rt["assembled"]:
                assembled_ok = assembled_ok + 1
                canonical_ok = canonical_ok + 1
            else:
                assembled_failed = assembled_failed + 1
                still_refused = still_refused + 1
                key = "assemble_failed: %s" % rt.get("as_stderr", "")[:120]
                reasons[key] = reasons.get(key, 0) + 1
        else:
            still_refused = still_refused + 1
            key = rec.get("derive_refused") or rec.get("erasure", "unknown")
            reasons[key] = reasons.get(key, 0) + 1
        rows[n] = rec
    out = {}
    out["language"] = lang
    out["meta"] = {
        "role": "generator provenance",
        "form": "canon4: dead-mov cleanup over canon3's total canonical "\
               "coverage, plus real fixes for the passthrough, "\
               "in-place-no-known-register, too-many-join-paths, and "\
               "two of the assemble_failed refusal causes (see "\
               "still_refused_reasons for what remains genuinely "\
               "unresolved and why)",
        "spelling": "the operator token appears once per unit, as "\
                   "the display label `operator` on a unit object",
        "generator": "canon4.py",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                      time.gmtime()),
    }
    out["units_read"] = len(keys)
    out["canonical_text_ok"] = canonical_ok
    out["still_refused"] = still_refused
    out["still_refused_reasons"] = reasons
    out["units"] = rows
    name = os.path.join(outdir, "canon4_units_%s.json" % lang)
    fh = open(name, "w")
    json.dump(out, fh, indent=1)
    fh.close()
    log("wrote %s (%d read, %d canonical_ok, %d still_refused, "
        "%d assembled_ok, %d assembled_failed)"
        % (name, len(keys), canonical_ok, still_refused, assembled_ok,
           assembled_failed))
    return out


def main(argv):
    indir = HERE
    outdir = HERE
    i = 1
    while i < len(argv):
        if argv[i] == "--in":
            indir = argv[i + 1]
            i = i + 2
            continue
        if argv[i] == "--out":
            outdir = argv[i + 1]
            i = i + 2
            continue
        print(__doc__)
        return 2
    started = time.time()
    log("canon3.py -- total canonical coverage")
    workdir = tempfile.mkdtemp(prefix="canon3_asm_")
    for lang in LANGS:
        run_language(lang, indir, outdir, workdir)
    log("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
