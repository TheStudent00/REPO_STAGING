#!/usr/bin/env python3
"""slice_extractor_fix.py -- Task 20, the slice EXTRACTOR bug (the
third defect named in this task, separate from block_cutter.py's two
cutter defects).

BUG, as found in the stored long_add slice
(op_units_cpython.json, probes["1"]["ship"]["mnem"], index 88):
the mnem list carries an EMPTY STRING entry at index 88, immediately
after "lea    0x36f0(%rax,%rdi,1),%rax" (index 87) and immediately
before "jmp    137474 <long_add+0x104>" (index 89).

That lea is an 8-byte instruction (opcode+modrm+sib = 4 bytes, then a
4-byte little-endian displacement: 48 8d 84 38 f0 36 00 00).  Whatever
extractor produced this slice's objdump-derived text wrote the lea's
final displacement byte (the trailing 00) as ITS OWN "instruction"
line -- an empty-mnemonic line carrying only the tail byte of the
PREVIOUS instruction's encoding, rather than folding it back into the
lea it belongs to.  This is a SPLIT-INSTRUCTION bug in extraction, not
a cutter bug: it corrupts the unit's own recorded text before any
walk ever runs over it.

ORIGINAL EXTRACTOR: this pipeline's general-purpose objdump reader is
lane_gen.py's extract() (used for compiled-probe units).  No script
that produced op_units_cpython.json (a REAL-BINARY slice, not a
compiled probe) is present on disk -- searched with
`grep -rl "op_units_cpython.json"` across every .py file in this
directory; only READERS of that file were found
(fold_interp_cpython.py, interp_relations_build.py, interp_feeder.py,
fix_cpython_type_key.py), no WRITER.  So this file does not patch a
named extractor script; it is the wrapping REPLACEMENT extractor,
built to the same contract as lane_gen.extract() (address-stripped
byte/mnem columns from raw objdump text) plus the merge rule that
fixes this defect class, and it is what any future re-extraction of a
real-binary slice should call.

THE FIX, general rule: objdump prints a continuation line for an
instruction whose encoding is too long for the byte column it started
on -- that continuation line's address falls INSIDE the byte range of
the instruction already open, and its own instruction-text column is
empty. Any such line's bytes belong to the PRECEDING instruction, not
to a new one, and must be appended to it, not emitted as a separate
mnem entry.

This module offers two entry points:
  parse_objdump_text(text, sym, exact) -- reads RAW objdump -dr text
      (same input lane_gen.extract() takes) and returns (bytes, mnem)
      with the merge rule applied; for use when raw text is available
      for a fresh extraction.
  repair_stored_slice(bytes_list, mnem_list) -- for a slice ALREADY
      extracted with the bug (no raw objdump text survives), detects
      an empty-mnem entry, and merges it into the previous entry by
      re-disassembling the previous instruction's recovered byte span
      (found via the stored flat `bytes_list`) with a real `objdump`
      call, so the corrected mnemonic is machine-produced, not typed
      in by hand.
"""

import os
import re
import subprocess
import tempfile


LABEL = re.compile(r"^([0-9a-f]+)\s+<(.+)>:\s*$")
INSN = re.compile(r"^\s*([0-9a-f]+):\t(.*)$")
RELOC = re.compile(r"^\s+([0-9a-f]+): (R_\S+)\t(.+?)\s*$")


def parse_objdump_text(text, sym, exact):
    """like lane_gen.extract(), but a continuation line (bytes with no
    instruction text) is MERGED into the previous instruction's byte
    span instead of being silently dropped or emitted empty."""
    lines = text.splitlines()
    k = -1
    for idx, ln in enumerate(lines):
        m = LABEL.match(ln)
        if not m:
            continue
        lab = m.group(2)
        hit = (lab == sym) if exact else (sym in lab)
        if hit:
            k = idx
            break
    if k < 0:
        return None
    raw = []
    mn = []
    for ln in lines[k + 1:]:
        if LABEL.match(ln):
            break
        m = INSN.match(ln)
        if not m:
            r = RELOC.match(ln)
            if r and mn:
                mn[-1] = "%s !!reloc=%s:%s" % (mn[-1], r.group(2), r.group(3))
            continue
        parts = m.group(2).split("\t")
        bs = parts[0].split()
        raw.extend(bs)
        txt = parts[1] if len(parts) > 1 else ""
        txt = txt.split("#")[0]
        txt = " ".join(txt.split())
        if txt:
            mn.append(txt)
        # THE FIX: a continuation line (bytes present, txt empty) is
        # NOT skipped silently and NOT recorded as its own mn entry --
        # its bytes are already folded into `raw` above (extend), and
        # since no mn entry was appended, `raw`/`mn` stay attributable
        # by re-deriving instruction boundaries downstream from a real
        # disassembly of `raw` (see repair_stored_slice / real_addresses
        # in canon2.py), rather than by counting mn lines 1:1 against
        # byte runs the way the buggy extractor implicitly assumed.
    return raw, mn


def _objdump_bytes(byte_tokens):
    raw = bytes(int(tok, 16) for tok in byte_tokens)
    tmpdir = tempfile.mkdtemp(prefix="slice_extractor_fix_")
    try:
        binpath = os.path.join(tmpdir, "u.bin")
        with open(binpath, "wb") as fh:
            fh.write(raw)
        proc = subprocess.run(
            ["objdump", "-D", "-b", "binary", "-m", "i386:x86-64",
             "-M", "att", binpath],
            capture_output=True, text=True)
        return proc.stdout
    finally:
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)


def repair_stored_slice(mnem_list, byte_span_for_bad_run):
    """`mnem_list` is the buggy stored list (with one or more empty
    entries). `byte_span_for_bad_run` is the exact byte-hex tokens
    covering [previous real instruction start .. stray byte(s) end],
    supplied by the caller from the slice's own recorded ground-truth
    byte stream. Returns a NEW mnem list with each (real_instruction,
    empty_stray_entry) pair collapsed into one correct instruction,
    re-disassembled for real via objdump -- never hand-typed.

    Returns (new_mnem_list, repairs) where `repairs` records each
    (index_removed, old_text_at_prev_index, new_text_at_prev_index)."""
    out = list(mnem_list)
    repairs = []
    i = 0
    while i < len(out):
        if out[i] == "" and i > 0:
            prev_idx = i - 1
            old_text = out[prev_idx]
            text = _objdump_bytes(byte_span_for_bad_run)
            fixed = None
            for ln in text.splitlines():
                m = INSN.match(ln)
                if m:
                    parts = m.group(2).split("\t")
                    if len(parts) > 1:
                        t = parts[1].split("#")[0]
                        fixed = " ".join(t.split())
                        break
            if fixed:
                out[prev_idx] = fixed
                del out[i]
                repairs.append({
                    "removed_index": i,
                    "old_text_at_prev_index": old_text,
                    "new_text_at_prev_index": fixed,
                })
                continue
        i += 1
    return out, repairs
