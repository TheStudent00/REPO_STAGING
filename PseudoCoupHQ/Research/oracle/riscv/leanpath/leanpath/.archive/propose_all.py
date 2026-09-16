"""propose_all -- a proposal for EVERY execute clause of the Sail emit, not
only the register-only ones: the reads of the machine (registers, the
PC, memory) become inputs, the writes (a register, the PC, memory, a
branch condition) become outputs, and the value of each output is the
Lean text of the clause with those substitutions. Nothing is certified
here: this is the construction stage, and the proposal is what the
printer emulates and the eye checks. The Lean check is the later stage.

The one rule of `strip.propose` (register reads to parameters, the
register write to the result) is kept for the clauses it covers; this
file adds the readings of four more effects, each one line:

  * `(← (rX_bits R))`, `let v ← rX_bits R`   a register read: input r_R
  * `(← readReg PC)`, `get_arch_pc ()`        the PC: input pc
  * `get_next_pc ()`                          the next PC: input next_pc
  * `vmem_read R off w ...` giving `data`     a memory read: input mem_data
                                              of 8*w bits; output mem_addr
  * `vmem_write R off w data ...`             a memory write: outputs
                                              mem_addr and mem_data
  * `jump_to (T)`                             the PC written: output pc
  * `if taken then jump_to T else ...`        a branch: outputs
                                              branch_condition (0/1) and pc

A clause that does anything else (vector loops, floats through the
softfloat functions, CSRs, atomics, traps) is DEFERRED with the element
named, exactly as `strip.propose` refuses.
"""
import re

from . import strip as ST


def rewrite_reads(text):
    """the monadic reads of the machine as plain names"""
    text = re.sub(r"\(← \(rX_bits (\w+)\)\)", lambda m: "r_%s" % m.group(1), text)
    text = re.sub(r"\(← \(count_ones (.*?)\)\)", lambda m: "(count_ones %s)" % m.group(1), text)   # monadic only for its counter
    text = re.sub(r"\(← readReg PC\)", "pc", text)
    text = re.sub(r"\(← \(get_arch_pc \(\)\)\)", "pc", text)
    text = re.sub(r"\(← \(get_next_pc \(\)\)\)", "next_pc", text)
    text = re.sub(r"let (\w+(?: : [^←\n]+)?) ← do \(get_next_pc \(\)\)\s*$", r"let \1 := next_pc", text, flags=re.M)
    text = re.sub(r"let (\w+(?: : [^←\n]+)?) ← do \(rX_bits (\w+)\)\s*$", r"let \1 := r_\2", text, flags=re.M)
    text = re.sub(r"let (\w+(?: : [^←\n]+)?) ← \(rX_bits (\w+)\)\s*$", r"let \1 := r_\2", text, flags=re.M)
    return text


def propose_any(clause):
    """{"inputs": [...], "lets": [(name, text)], "outputs": {place: text},
    "notes": [...]} or {"deferred": why}. Register-only clauses come from
    strip.propose unchanged in meaning."""
    p = ST.propose(clause)
    if p.get("shape") == "straight":
        inputs = [("r_%s" % reg, "bv", 64) for _, reg in p["reads"]]
        lets = [(n, v) for n, v in p.get("lets", [])]
        # the strip names the read values (v_rs1); the general form names them by register (r_rs1)
        ren = {vname: "r_%s" % reg for vname, reg in p["reads"]}
        sub = lambda s: re.sub(r"\b(%s)\b" % "|".join(map(re.escape, ren)), lambda m: ren[m.group(1)], s) if ren else s
        return {"inputs": inputs, "lets": [(n, sub(v)) for n, v in lets], "outputs": {"rd": sub(p["value"])},
                "write": p.get("write"), "case_on": p.get("case_on"), "others": p.get("others", []), "notes": []}
    if p.get("shape") == "alias":
        return {"deferred": "an alias of %s; the target clause carries the proposal" % (p.get("alias") or "?")[:60]}
    body = "\n".join(clause["body"])
    notes = []
    lines = []
    for ln in body.split("\n"):
        s = ln.strip()
        if s.startswith("assert "):
            notes.append("an assert dropped: " + s[:60])
            continue
        if s.startswith("(update_elp_state"):
            notes.append("control-flow-integrity state not modelled: " + s[:40])
            continue
        lines.append(ln)
    text = rewrite_reads("\n".join(lines))
    inputs = []
    seen = set()
    for r in re.findall(r"\br_(\w+)\b", text):
        if r not in seen:
            seen.add(r)
            inputs.append(("r_%s" % r, "bv", 64))
    if re.search(r"\bpc\b", text):
        inputs.append(("pc", "bv", 64))
    if re.search(r"\bnext_pc\b", text):
        inputs.append(("next_pc", "bv", 64))
    lets = []
    outputs = {}
    # `let X ← do (pure (E))`, `let X ← do (get_next_pc ())` (already rewritten), `let X := E`
    text = re.sub(r"let (\w+(?: : [^←\n]+)?) ← do \(pure (\(.*\))\)\s*$", r"let \1 := \2", text, flags=re.M)
    text = re.sub(r"let (\w+(?: : [^←\n]+)?) ← do \(next_pc\)\s*$", r"let \1 := next_pc", text, flags=re.M)
    text = re.sub(r"let (\w+(?: : [^←\n]+)?) ← do next_pc\s*$", r"let \1 := next_pc", text, flags=re.M)
    # `let X ← (( do match op with | .K => (pure E) ... ) : SailM T )` -> a pure match
    m = re.search(r"let (\w+) ← \(\( do\n(.*?)\) : SailM \w+ \)", text, re.S)
    if m:
        arms = re.sub(r"\(pure (\(.*?\))\)", r"\1", m.group(2))
        text = text[:m.start()] + "let %s := %s" % (m.group(1), arms.strip()) + text[m.end():]
    # a memory read: `match (← (vmem_read R off w (Load Data) ...)) with | .Ok data => (do BODY) | .Err e => (pure e)`
    m = re.search(r"match \(← \(vmem_read (\w+) (\w+) (\w+) .*?\)\) with\n\s*\| \.Ok (\w+) =>\n\s*\(do\n(.*?)\)\n\s*\| \.Err \w+ => \(pure \w+\)", text, re.S)
    if m:
        reg, off, width, data, inner = m.groups()
        if ("r_%s" % reg, "bv", 64) not in inputs:
            inputs.append(("r_%s" % reg, "bv", 64))
        inputs.append(("mem_data", "bv", "8*%s" % width))
        outputs["mem_addr"] = "(r_%s + %s)" % (reg, off)
        lets.append((data, "mem_data"))
        text = text[:m.start()] + inner + text[m.end():]
    # a memory write: `match (← (vmem_write R off w data ...)) with | .Ok _ => (pure RETIRE_SUCCESS) | .Err e => (pure e)`
    m = re.search(r"match \(← \(vmem_write (\w+) (\w+) (\w+) (\w+) .*?\)\) with\n\s*\| \.Ok _ => \(pure RETIRE_SUCCESS\)\n\s*\| \.Err \w+ => \(pure \w+\)", text, re.S)
    if m:
        reg, off, width, data = m.groups()
        if ("r_%s" % reg, "bv", 64) not in inputs:
            inputs.append(("r_%s" % reg, "bv", 64))
        outputs["mem_addr"] = "(r_%s + %s)" % (reg, off)
        outputs["mem_data"] = data
        text = text[:m.start()] + text[m.end():]
    # a jump with a link: `match (← (jump_to (T))) with | .Retire_Success () => (do (wX_bits rd L) (pure ...)) | failure => (pure failure)`
    m = re.search(r"match \(← \(jump_to (.*?)\)\) with\n\s*\| \.Retire_Success \(\) =>\n\s*\(do\n\s*\(wX_bits (\w+) (.+?)\)\n\s*\(pure \(Retire_Success \(\)\)\)\)\n\s*\| failure => \(pure failure\)", text, re.S)
    if m:
        outputs["pc"] = m.group(1)
        outputs["rd"] = m.group(3)
        text = text[:m.start()] + text[m.end():]
    # a branch: `if (taken : Bool) then (jump_to (T)) else (pure RETIRE_SUCCESS)`
    m = re.search(r"if \((\w+) : Bool\)\n\s*then \(jump_to (.*?)\)\n\s*else \(pure RETIRE_SUCCESS\)", text, re.S)
    if m:
        outputs["branch_condition"] = m.group(1)
        outputs["pc"] = m.group(2)
        text = text[:m.start()] + text[m.end():]
    # a register write with a monadic match inside: `(wX_bits rd\n (← do\n match op with | .K => (pure E) ...))`
    m = re.search(r"\(wX_bits (\w+)\n\s*\(← do\n(.*?)\)\)\n", text, re.S)
    if m:
        arms = re.sub(r"\(pure (\(.*?\)|\w+)\)", r"\1", m.group(2))
        outputs["rd"] = arms.strip()
        text = text[:m.start()] + text[m.end():]
    # a plain register write: `(wX_bits rd (E))` on one line
    m = re.search(r"^\s*\(wX_bits (\w+) (.+)\)\s*$", text, re.M)
    if m and "rd" not in outputs:
        outputs["rd"] = m.group(2)
        text = text[:m.start()] + text[m.end():]
    # what is left must be lets and the retire
    rest = []
    for ln in text.split("\n"):
        s = ln.strip()
        if not s or s in ("(pure RETIRE_SUCCESS)", "(pure (Retire_Success ()))"):
            continue
        mm = re.match(r"^let (\w+(?: : [^:=]+?)?) := (.*)$", s)
        if mm:
            lets.append((mm.group(1), mm.group(2)))
            continue
        rest.append(s)
    # a let whose value continues on following lines (a match) was split: rejoin by indentation
    if rest:
        joined = []
        for s in rest:
            if s.startswith("|") and lets:
                n, v = lets[-1]
                lets[-1] = (n, v + "\n" + s)
                continue
            joined.append(s)
        rest = joined
    if rest:
        return {"deferred": "an element the readings do not know: %s" % rest[0][:80], "notes": notes}
    if not outputs:
        return {"deferred": "no output found", "notes": notes}
    others = [(n, t) for n, t in clause["params"] if t.strip("() ") != "regidx"]
    return {"inputs": inputs, "lets": lets, "outputs": outputs, "others": others, "notes": notes}
