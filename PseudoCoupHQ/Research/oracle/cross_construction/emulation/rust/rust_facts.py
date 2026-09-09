#!/usr/bin/env python3
"""rust_facts.py -- task o11, step 1: what rustc ITSELF does, read off
its own emission, for every rule the rust renderer will need.

Node: hq.research.arch_unit_oracle.cross_construction
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/CORE_0_3_2_2_cross_construction.md`,
FROZEN for term-level composition; task o7 opened the emulation route
and this task extends it to a second target language, which does not
unfreeze the node).

WHAT THIS FILE IS, one sentence, in relation: it is the evidence
under the rust column of task o11's coverage table -- one small rust
function per question, compiled at the SAME flags the rust arch-unit
corpus was built with, carved with the SAME objdump reader, so every
claim in that column is the compiler's own emission rather than a
recollection of rust's rules.

WHY IT EXISTS: the brief requires the rust specifics be recorded
"from rustc's own rules, not memory" -- whether plain `+` wraps or
panics under the ship flags, what a variable shift count does when it
is out of range, whether a zero divisor is checked, what `as` does
across widths and across the integer/float boundary, and whether
128-bit holders exist. Each is one probe below.

WHAT IS REUSED RATHER THAN COPIED: `emulate.pipeline_extractor()` (task
o7's lift of `lane_gen.DRIVER`'s `extract`, the objdump reader that
carved every unit of the corpus) carves each probe body. The ship
flags are read off `lane_gen.py` `compile_probe`'s rust branch and are
not retyped by hand -- `SHIP_FLAGS_RUST` below quotes that branch and
`ship_flags_source()` prints the branch itself.

MEMORY BOUND, stated as the law requires: one process, no forks; the
probes are a few dozen kilobytes of source and objdump text; peak
resident size is printed at the end; the named abort is
ABORT_MEMORY_O11 at 4 GB, the same ceiling the run lane uses. Nothing
here approaches it.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

Nothing here groups or pairs units at all: the probes are hand-written
rust functions written to answer a question about the COMPILER, they
are not arch-units of the corpus, and no pool member is read. The
`question` field of each row names a machine-level behaviour, never a
language operator token used as a key.

Coding discipline: no compound one-liner statements.

usage:
  rust_facts.py probe      compile every probe, carve, write the json
  rust_facts.py table      print the rust column of the coverage table
"""

import json
import os
import re
import resource
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
EMULATION = os.path.normpath(os.path.join(HERE, ".."))
OP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                   "op_pipeline"))
sys.path.insert(0, OP)
sys.path.insert(0, EMULATION)

FACTS = os.path.join(HERE, "rust_facts.json")
FACTS2 = os.path.join(HERE, "rust_facts2.json")
FACTS3 = os.path.join(HERE, "rust_facts3.json")
FACTS4 = os.path.join(HERE, "rust_facts4.json")

RUSTC = "rustc"

# read off `lane_gen.py` compile_probe, the rust branch, LITERAL:
#   if mode == "anchor":
#       opt = ["-C", "opt-level=0", "-g"]
#   else:
#       opt = ["-C", "opt-level=1", "-C", "debug-assertions=off"]
#   cmd = (["rustc", "--crate-type=lib", "--emit=obj"] + opt
#          + ["-o", obj, src])
SHIP_FLAGS_RUST = ["--crate-type=lib", "--emit=obj",
                   "-C", "opt-level=1",
                   "-C", "debug-assertions=off"]
DEBUG_FLAGS_RUST = ["--crate-type=lib", "--emit=obj",
                    "-C", "opt-level=1",
                    "-C", "debug-assertions=on"]

PRELUDE = "#![allow(dead_code, unused_parens, unconditional_panic)]\n"


def probe(name, question, body):
    """one probe: a whole rust function, its symbol, and the question
    its emitted body answers."""
    return {"name": name, "question": question, "source": body}


PROBES = [
    probe("plain_sum_u32",
          "does plain two-place arithmetic wrap or check, at ship flags",
          '#[no_mangle]\npub extern "C" fn plain_sum_u32(a: u32, b: u32)'
          " -> u32 { a + b }"),
    probe("wrapping_sum_u32",
          "what the explicit wrapping form emits, at ship flags",
          '#[no_mangle]\npub extern "C" fn wrapping_sum_u32(a: u32,'
          " b: u32) -> u32 { a.wrapping_add(b) }"),
    probe("plain_product_u64",
          "does plain multiplication wrap or check, at ship flags",
          '#[no_mangle]\npub extern "C" fn plain_product_u64(a: u64,'
          " b: u64) -> u64 { a * b }"),
    probe("wrapping_product_u64",
          "what the explicit wrapping multiplication emits",
          '#[no_mangle]\npub extern "C" fn wrapping_product_u64(a: u64,'
          " b: u64) -> u64 { a.wrapping_mul(b) }"),
    probe("plain_negate_i32",
          "does plain negation wrap or check, at ship flags",
          '#[no_mangle]\npub extern "C" fn plain_negate_i32(a: i32)'
          " -> i32 { -a }"),
    probe("wrapping_negate_i32",
          "what the explicit wrapping negation emits",
          '#[no_mangle]\npub extern "C" fn wrapping_negate_i32(a: i32)'
          " -> i32 { a.wrapping_neg() }"),
    probe("plain_left_shift_u32",
          "what a VARIABLE shift count does when it can exceed the width",
          '#[no_mangle]\npub extern "C" fn plain_left_shift_u32(a: u32,'
          " b: u32) -> u32 { a << b }"),
    probe("wrapping_left_shift_u32",
          "what the explicit wrapping shift emits (count masked to the"
          " width)",
          '#[no_mangle]\npub extern "C" fn wrapping_left_shift_u32(a: u32,'
          " b: u32) -> u32 { a.wrapping_shl(b) }"),
    probe("guarded_left_shift_u32",
          "the renderer's own out-of-range rule: zero above the width",
          '#[no_mangle]\npub extern "C" fn guarded_left_shift_u32(a: u32,'
          " b: u32) -> u32 { if b < 32 { a.wrapping_shl(b) } else { 0 } }"),
    probe("plain_right_shift_i32",
          "does the arithmetic right shift keep the sign",
          '#[no_mangle]\npub extern "C" fn plain_right_shift_i32(a: i32,'
          " b: u32) -> i32 { a.wrapping_shr(b) }"),
    probe("plain_quotient_u32",
          "is a zero divisor checked in the emitted body, at ship flags",
          '#[no_mangle]\npub extern "C" fn plain_quotient_u32(a: u32,'
          " b: u32) -> u32 { a / b }"),
    probe("plain_remainder_u32",
          "is a zero divisor checked for the remainder too",
          '#[no_mangle]\npub extern "C" fn plain_remainder_u32(a: u32,'
          " b: u32) -> u32 { a % b }"),
    probe("plain_quotient_i32",
          "the signed quotient: which checks the body carries",
          '#[no_mangle]\npub extern "C" fn plain_quotient_i32(a: i32,'
          " b: i32) -> i32 { a / b }"),
    probe("unchecked_quotient_u32",
          "the unguarded division idiom: does it emit a bare divide",
          '#[no_mangle]\npub extern "C" fn unchecked_quotient_u32(a: u32,'
          " b: u32) -> u32 { unsafe { a.unchecked_div(b) } }"),
    probe("unchecked_quotient_i32",
          "the unguarded SIGNED division idiom",
          '#[no_mangle]\npub extern "C" fn unchecked_quotient_i32(a: i32,'
          " b: i32) -> i32 { unsafe { a.unchecked_div(b) } }"),
    probe("unchecked_remainder_u32",
          "the unguarded remainder idiom",
          '#[no_mangle]\npub extern "C" fn unchecked_remainder_u32(a: u32,'
          " b: u32) -> u32 { unsafe { a.unchecked_rem(b) } }"),
    probe("widen_u8_to_u32",
          "is there implicit widening, or does it take a cast",
          '#[no_mangle]\npub extern "C" fn widen_u8_to_u32(a: u8) -> u32'
          " { a as u32 }"),
    probe("narrow_u32_to_u8",
          "what a narrowing cast emits",
          '#[no_mangle]\npub extern "C" fn narrow_u32_to_u8(a: u32) -> u8'
          " { a as u8 }"),
    probe("sign_extend_i8_to_i64",
          "what a signed widening cast emits",
          '#[no_mangle]\npub extern "C" fn sign_extend_i8_to_i64(a: i8)'
          " -> i64 { a as i64 }"),
    probe("sum_u128",
          "does a 128-bit holder exist and what does it emit",
          '#[no_mangle]\npub extern "C" fn sum_u128(a: u128, b: u128)'
          " -> u128 { a.wrapping_add(b) }"),
    probe("quotient_u128_from_u64",
          "the widening-division shape task o7's c renderer used",
          '#[no_mangle]\npub extern "C" fn quotient_u128_from_u64(a: u64,'
          " b: u64) -> u64 { unsafe { ((a as u128).unchecked_div("
          "b as u128)) as u64 } }"),
    probe("sum_f64",
          "float arithmetic at 64 bits",
          '#[no_mangle]\npub extern "C" fn sum_f64(a: f64, b: f64) -> f64'
          " { a + b }"),
    probe("sum_f32",
          "float arithmetic at 32 bits",
          '#[no_mangle]\npub extern "C" fn sum_f32(a: f32, b: f32) -> f32'
          " { a + b }"),
    probe("f64_bits",
          "reading a float's bits without a memory round trip",
          '#[no_mangle]\npub extern "C" fn f64_bits(a: f64) -> u64'
          " { a.to_bits() }"),
    probe("bits_f64",
          "writing a float from its bits",
          '#[no_mangle]\npub extern "C" fn bits_f64(a: u64) -> f64'
          " { f64::from_bits(a) }"),
    probe("saturating_f64_to_i64",
          "what the plain float-to-integer cast does out of range",
          '#[no_mangle]\npub extern "C" fn saturating_f64_to_i64(a: f64)'
          " -> i64 { a as i64 }"),
    probe("truncating_f64_to_i64",
          "the unguarded float-to-integer idiom, matching the machine",
          '#[no_mangle]\npub extern "C" fn truncating_f64_to_i64(a: f64)'
          " -> i64 { unsafe { a.to_int_unchecked::<i64>() } }"),
    probe("i64_to_f64",
          "the integer-to-float cast",
          '#[no_mangle]\npub extern "C" fn i64_to_f64(a: i64) -> f64'
          " { a as f64 }"),
    probe("u64_to_f64",
          "the unsigned integer-to-float cast",
          '#[no_mangle]\npub extern "C" fn u64_to_f64(a: u64) -> f64'
          " { a as f64 }"),
    probe("f64_to_f32",
          "the float narrowing cast",
          '#[no_mangle]\npub extern "C" fn f64_to_f32(a: f64) -> f32'
          " { a as f32 }"),
    probe("choose_u32",
          "the conditional expression",
          '#[no_mangle]\npub extern "C" fn choose_u32(c: u32, a: u32,'
          " b: u32) -> u32 { if (c & 1) != 0 { a } else { b } }"),
    probe("less_signed_i32",
          "a signed comparison, answered as a 0/1 holder",
          '#[no_mangle]\npub extern "C" fn less_signed_i32(a: i32, b: i32)'
          " -> u32 { if a < b { 1 } else { 0 } }"),
    probe("less_unsigned_u32",
          "an unsigned comparison, answered as a 0/1 holder",
          '#[no_mangle]\npub extern "C" fn less_unsigned_u32(a: u32,'
          " b: u32) -> u32 { if a < b { 1 } else { 0 } }"),
    probe("complement_u32",
          "the bit complement",
          '#[no_mangle]\npub extern "C" fn complement_u32(a: u32) -> u32'
          " { !a }"),
    probe("f16_exists",
          "is there a 16-bit float holder in this rustc",
          '#[no_mangle]\npub extern "C" fn f16_exists(a: u16) -> u16'
          " { a }"),
    probe("wide_arrival_u8",
          "what the callee assumes about the bits above a narrow"
          " argument",
          '#[no_mangle]\npub extern "C" fn wide_arrival_u8(a: u8, b: u8)'
          " -> u8 { a.wrapping_add(b) }"),
]

# the probes whose answer differs between the ship build and the
# debug build; each is compiled twice so the contrast is on the page.
CONTRAST = ["plain_sum_u32", "plain_product_u64", "plain_negate_i32",
            "plain_left_shift_u32", "plain_quotient_u32"]


# ---------------------------------------------------------------------
# the second set, run after the first: lane 1 showed that plain `/` and
# `%` carry a zero-divisor check and a call to a panic routine in BOTH
# builds, and that the method `unchecked_div` does not exist on stable
# rustc 1.96.1.  So the division cell of the coverage table needs an
# IDIOM, and this set is the search for one that emits a bare divide.
# It also closes two gaps lane 1 left: whether a 16-bit float holder
# exists, and what the 128-bit division shape emits.
# ---------------------------------------------------------------------

PROBES2 = [
    probe("nonzero_quotient_u32",
          "does dividing by a NonZero holder drop the zero check",
          '#[no_mangle]\npub extern "C" fn nonzero_quotient_u32(a: u32,'
          " b: u32) -> u32 { unsafe {"
          " a / core::num::NonZeroU32::new_unchecked(b) } }"),
    probe("nonzero_remainder_u32",
          "the same for the remainder",
          '#[no_mangle]\npub extern "C" fn nonzero_remainder_u32(a: u32,'
          " b: u32) -> u32 { unsafe {"
          " a % core::num::NonZeroU32::new_unchecked(b) } }"),
    probe("nonzero_quotient_u64",
          "the same at 64 bits",
          '#[no_mangle]\npub extern "C" fn nonzero_quotient_u64(a: u64,'
          " b: u64) -> u64 { unsafe {"
          " a / core::num::NonZeroU64::new_unchecked(b) } }"),
    probe("nonzero_quotient_u128",
          "the same at 128 bits",
          '#[no_mangle]\npub extern "C" fn nonzero_quotient_u128(a: u128,'
          " b: u128) -> u128 { unsafe {"
          " a / core::num::NonZeroU128::new_unchecked(b) } }"),
    probe("nonzero_quotient_i32",
          "is there a signed NonZero division, and does it drop BOTH"
          " checks (zero and the signed extreme)",
          '#[no_mangle]\npub extern "C" fn nonzero_quotient_i32(a: i32,'
          " b: i32) -> i32 { unsafe {"
          " a / core::num::NonZeroI32::new_unchecked(b) } }"),
    probe("branch_quotient_u32",
          "does an explicit zero guard let the optimizer drop rustc's"
          " own",
          '#[no_mangle]\npub extern "C" fn branch_quotient_u32(a: u32,'
          " b: u32) -> u32 { if b != 0 { a / b } else { 0 } }"),
    probe("branch_quotient_i32",
          "the signed guard written out: zero divisor and the signed"
          " extreme",
          '#[no_mangle]\npub extern "C" fn branch_quotient_i32(a: i32,'
          " b: i32) -> i32 { if b != 0 && !(a == i32::MIN && b == -1)"
          " { a / b } else { 0 } }"),
    probe("checked_quotient_u32",
          "the Option-returning form, unwrapped to a constant",
          '#[no_mangle]\npub extern "C" fn checked_quotient_u32(a: u32,'
          " b: u32) -> u32 { a.checked_div(b).unwrap_or(0) }"),
    probe("wrapping_quotient_i32",
          "does the wrapping form drop the signed-extreme check",
          '#[no_mangle]\npub extern "C" fn wrapping_quotient_i32(a: i32,'
          " b: i32) -> i32 { a.wrapping_div(b) }"),
    probe("intrinsic_quotient_u32",
          "is the compiler intrinsic reachable on this stable rustc",
          '#[no_mangle]\npub extern "C" fn intrinsic_quotient_u32(a: u32,'
          " b: u32) -> u32 { unsafe { core::intrinsics::unchecked_div("
          "a, b) } }"),
    probe("float16_holder",
          "is there a 16-bit float holder on this rustc",
          '#[no_mangle]\npub extern "C" fn float16_holder(a: f16, b: f16)'
          " -> f16 { a + b }"),
    probe("float128_holder",
          "is there a 128-bit float holder on this rustc",
          '#[no_mangle]\npub extern "C" fn float128_holder(a: f128,'
          " b: f128) -> f128 { a + b }"),
    probe("truncating_f64_to_u64",
          "the unguarded float-to-UNSIGNED-integer idiom",
          '#[no_mangle]\npub extern "C" fn truncating_f64_to_u64(a: f64)'
          " -> u64 { unsafe { a.to_int_unchecked::<u64>() } }"),
    probe("truncating_f32_to_i32",
          "the same at 32 bits",
          '#[no_mangle]\npub extern "C" fn truncating_f32_to_i32(a: f32)'
          " -> i32 { unsafe { a.to_int_unchecked::<i32>() } }"),
    probe("f32_bits",
          "reading a 32-bit float's bits",
          '#[no_mangle]\npub extern "C" fn f32_bits(a: f32) -> u32'
          " { a.to_bits() }"),
    probe("bits_f32",
          "writing a 32-bit float from its bits",
          '#[no_mangle]\npub extern "C" fn bits_f32(a: u32) -> f32'
          " { f32::from_bits(a) }"),
    probe("absolute_f64",
          "the float absolute value without the standard library's"
          " math",
          '#[no_mangle]\npub extern "C" fn absolute_f64(a: f64) -> f64'
          " { f64::from_bits(a.to_bits() & 0x7fff_ffff_ffff_ffff) }"),
    probe("is_nan_f64",
          "the not-a-number test",
          '#[no_mangle]\npub extern "C" fn is_nan_f64(a: f64) -> u32'
          " { if a != a { 1 } else { 0 } }"),
    probe("is_infinite_f64",
          "the infinity test without the standard library's math",
          '#[no_mangle]\npub extern "C" fn is_infinite_f64(a: f64) -> u32'
          " { if (a.to_bits() & 0x7fff_ffff_ffff_ffff)"
          " == 0x7ff0_0000_0000_0000 { 1 } else { 0 } }"),
    probe("sign_bit_f64",
          "the sign-bit test",
          '#[no_mangle]\npub extern "C" fn sign_bit_f64(a: f64) -> u32'
          " { if (a.to_bits() >> 63) != 0 { 1 } else { 0 } }"),
    probe("concat_u64_pair",
          "the two-word join the c renderer wrote as a 128-bit shift"
          " and or",
          '#[no_mangle]\npub extern "C" fn concat_u64_pair(a: u64,'
          " b: u64) -> u128 { (((a as u128) << 64) | (b as u128)) }"),
    probe("sign_extend_narrow_field",
          "the sign-extension idiom over a field narrower than its"
          " holder",
          '#[no_mangle]\npub extern "C" fn sign_extend_narrow_field('
          "a: u32) -> u32 { (((a << 20) as i32) >> 20) as u32 }"),
    probe("saturating_i128_quotient",
          "the 128-bit signed division shape",
          '#[no_mangle]\npub extern "C" fn saturating_i128_quotient('
          "a: i128, b: i128) -> i128 { unsafe {"
          " a / core::num::NonZeroI128::new_unchecked(b) } }"),
]


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def firstline(text):
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped.replace("|", "/")[:300]
    return "(no diagnostic)"


def ship_flags_source():
    """the rust branch of `lane_gen.py` compile_probe, LITERAL, so the
    flags are quoted from the pipeline rather than retyped."""
    path = os.path.join(OP, "lane_gen.py")
    text = open(path).read()
    start = text.index('    if LANG == "rust":')
    end = text.index('    if LANG == "go":')
    return text[start:end].rstrip()


def rustc_version():
    done = subprocess.run([RUSTC, "--version"], capture_output=True,
                          text=True, timeout=120)
    return done.stdout.strip() or done.stderr.strip()


def compile_crate(source, flags, work):
    src = os.path.join(work, "facts.rs")
    obj = os.path.join(work, "facts.o")
    handle = open(src, "w")
    handle.write(source)
    handle.close()
    command = [RUSTC] + flags + ["-o", obj, src]
    done = subprocess.run(command, capture_output=True, text=True,
                          timeout=600)
    if done.returncode != 0 or not os.path.exists(obj):
        return None, firstline(done.stderr or done.stdout)
    return obj, None


def carve(obj, symbol):
    import emulate as E
    extract = E.pipeline_extractor()
    done = subprocess.run(["objdump", "-dr", "--disassemble=" + symbol,
                           obj], capture_output=True, text=True,
                          timeout=180)
    got = extract(done.stdout, symbol, True)
    if got is None:
        return None, None
    raw, mnem = got
    return raw, mnem


def one_build(label, probes, flags, work):
    """compile every probe in ONE crate and carve each symbol."""
    parts = [PRELUDE]
    for row in probes:
        parts.append(row["source"])
        parts.append("")
    source = "\n".join(parts)
    obj, refusal = compile_crate(source, flags, work)
    out = {}
    if obj is None:
        for row in probes:
            out[row["name"]] = {"compiled": False, "refusal": refusal}
        return out, source, refusal
    for row in probes:
        raw, mnem = carve(obj, row["name"])
        if raw is None:
            out[row["name"]] = {"compiled": True,
                                "carved": False,
                                "note": "objdump found no symbol"}
            continue
        out[row["name"]] = {
            "compiled": True,
            "carved": True,
            "body_text": "; ".join(mnem),
            "body_bytes": " ".join(raw),
            "byte_count": len(raw),
            "instruction_count": len(mnem),
            "calls": [m for m in mnem if m.startswith("call")],
        }
    return out, source, None


def probe_each_alone(probes, flags, work):
    """a probe that does not compile inside the shared crate is tried
    on its own, so one refusal does not take the whole crate down."""
    out = {}
    for row in probes:
        source = PRELUDE + row["source"] + "\n"
        obj, refusal = compile_crate(source, flags,
                                     tempfile.mkdtemp(dir=work))
        if obj is None:
            out[row["name"]] = {"compiled": False, "refusal": refusal}
            continue
        raw, mnem = carve(obj, row["name"])
        if raw is None:
            out[row["name"]] = {"compiled": True, "carved": False,
                                "note": "objdump found no symbol"}
            continue
        out[row["name"]] = {
            "compiled": True,
            "carved": True,
            "body_text": "; ".join(mnem),
            "body_bytes": " ".join(raw),
            "byte_count": len(raw),
            "instruction_count": len(mnem),
            "calls": [m for m in mnem if m.startswith("call")],
        }
    return out


def run_probes():
    work = tempfile.mkdtemp(prefix="o11_facts_",
                            dir=os.environ.get("TMPDIR"))
    document = {
        "task": "o11",
        "rustc_version": rustc_version(),
        "ship_flags": SHIP_FLAGS_RUST,
        "ship_flags_source": ship_flags_source(),
        "debug_flags": DEBUG_FLAGS_RUST,
        "probes": [],
    }
    total = 3
    say("[1/%d] the whole crate at the ship flags" % total)
    ship, source, refusal = one_build("ship", PROBES, SHIP_FLAGS_RUST,
                                      work)
    document["crate_source"] = source
    if refusal is not None:
        say("    the shared crate refused: %s" % refusal)
        say("    falling back to one crate per probe")
        ship = probe_each_alone(PROBES, SHIP_FLAGS_RUST, work)
    say("[2/%d] the contrast probes at debug-assertions=on" % total)
    wanted = [row for row in PROBES if row["name"] in CONTRAST]
    debug, _source, drefusal = one_build("debug", wanted,
                                         DEBUG_FLAGS_RUST, work)
    if drefusal is not None:
        debug = probe_each_alone(wanted, DEBUG_FLAGS_RUST, work)
    say("[3/%d] writing %s" % (total, FACTS))
    for row in PROBES:
        entry = {
            "name": row["name"],
            "question": row["question"],
            "source": row["source"],
            "ship": ship.get(row["name"]),
        }
        if row["name"] in CONTRAST:
            entry["debug_assertions_on"] = debug.get(row["name"])
        document["probes"].append(entry)
    document["peak_kb"] = peak_kb()
    handle = open(FACTS, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    say("rustc: %s" % document["rustc_version"])
    say("peak resident: %d kB (ceiling ABORT_MEMORY_O11 at 4 GB)"
        % document["peak_kb"])
    for entry in document["probes"]:
        ship_row = entry["ship"] or {}
        if not ship_row.get("carved"):
            say("  %-26s NOT CARVED %s" % (entry["name"],
                                           ship_row.get("refusal")
                                           or ship_row.get("note")))
            continue
        say("  %-26s %s" % (entry["name"], ship_row["body_text"]))
    return 0


# ---------------------------------------------------------------------
# the third set.  Lane 2 found a division idiom that emits a bare
# divide for UNSIGNED holders (`a / NonZeroU32::new_unchecked(b)`) but
# none for signed ones -- `NonZero<i32>` has no division at all, and
# every other signed form keeps rustc's two checks (a zero divisor and
# the signed extreme, where the quotient does not fit).  This set tries
# the one remaining stable route: telling the optimizer the checks
# cannot fire, with `core::hint::assert_unchecked`.
# ---------------------------------------------------------------------

HINT_HEAD = ('#[no_mangle]\npub extern "C" fn %s(a: %s, b: %s) -> %s'
             " {\n    unsafe {\n")

PROBES3 = [
    probe("hinted_quotient_i32",
          "does an unchecked hint drop rustc's two signed checks",
          HINT_HEAD % ("hinted_quotient_i32", "i32", "i32", "i32")
          + "        core::hint::assert_unchecked(b != 0);\n"
            "        core::hint::assert_unchecked("
            "!(a == i32::MIN && b == -1));\n"
            "    }\n    a / b\n}"),
    probe("hinted_remainder_i32",
          "the same for the signed remainder",
          HINT_HEAD % ("hinted_remainder_i32", "i32", "i32", "i32")
          + "        core::hint::assert_unchecked(b != 0);\n"
            "        core::hint::assert_unchecked("
            "!(a == i32::MIN && b == -1));\n"
            "    }\n    a % b\n}"),
    probe("hinted_quotient_i64",
          "the same at 64 bits",
          HINT_HEAD % ("hinted_quotient_i64", "i64", "i64", "i64")
          + "        core::hint::assert_unchecked(b != 0);\n"
            "        core::hint::assert_unchecked("
            "!(a == i64::MIN && b == -1));\n"
            "    }\n    a / b\n}"),
    probe("hinted_quotient_u32",
          "does the same hint work for the unsigned holder, so one"
          " rule covers both readings",
          HINT_HEAD % ("hinted_quotient_u32", "u32", "u32", "u32")
          + "        core::hint::assert_unchecked(b != 0);\n"
            "    }\n    a / b\n}"),
    probe("hinted_remainder_u32",
          "the unsigned remainder under the same hint",
          HINT_HEAD % ("hinted_remainder_u32", "u32", "u32", "u32")
          + "        core::hint::assert_unchecked(b != 0);\n"
            "    }\n    a % b\n}"),
    probe("hinted_quotient_u128",
          "the 128-bit unsigned quotient under the same hint",
          HINT_HEAD % ("hinted_quotient_u128", "u128", "u128", "u128")
          + "        core::hint::assert_unchecked(b != 0);\n"
            "    }\n    a / b\n}"),
    probe("hinted_quotient_i128",
          "the 128-bit signed quotient under the same hint",
          HINT_HEAD % ("hinted_quotient_i128", "i128", "i128", "i128")
          + "        core::hint::assert_unchecked(b != 0);\n"
            "        core::hint::assert_unchecked("
            "!(a == i128::MIN && b == -1));\n"
            "    }\n    a / b\n}"),
    probe("hinted_quotient_i8",
          "the narrowest signed quotient under the same hint",
          HINT_HEAD % ("hinted_quotient_i8", "i8", "i8", "i8")
          + "        core::hint::assert_unchecked(b != 0);\n"
            "        core::hint::assert_unchecked("
            "!(a == i8::MIN && b == -1));\n"
            "    }\n    a / b\n}"),
    probe("hinted_quotient_u16",
          "the 16-bit unsigned quotient under the same hint",
          HINT_HEAD % ("hinted_quotient_u16", "u16", "u16", "u16")
          + "        core::hint::assert_unchecked(b != 0);\n"
            "    }\n    a / b\n}"),
    probe("widening_quotient_u64_pair",
          "the widening-division shape task o7's c renderer wrote, in"
          " rust",
          '#[no_mangle]\npub extern "C" fn widening_quotient_u64_pair('
          "a: u64, b: u64) -> u64 {\n    unsafe {\n"
          "        core::hint::assert_unchecked(b != 0);\n"
          "    }\n    (((a as u128) << 0) / (b as u128)) as u64\n}"),
]


# ---------------------------------------------------------------------
# the fourth set.  Lane 3 found that `core::hint::assert_unchecked`
# removes rustc's ZERO-divisor check at every unsigned width, but not
# the SIGNED-extreme check (the quotient of the most negative value by
# minus one does not fit, and rustc keeps a branch to a panic routine
# for it).  This set tries the remaining spellings of the same fact.
# ---------------------------------------------------------------------

PROBES4 = [
    probe("unreachable_quotient_i32",
          "does spelling the hint as an unreachable branch drop the"
          " signed-extreme check",
          '#[no_mangle]\npub extern "C" fn unreachable_quotient_i32('
          "a: i32, b: i32) -> i32 {\n    unsafe {\n"
          "        if b == 0 || (a == i32::MIN && b == -1) {\n"
          "            core::hint::unreachable_unchecked();\n"
          "        }\n    }\n    a / b\n}"),
    probe("two_hint_quotient_i32",
          "the two facts hinted separately rather than as one"
          " conjunction",
          '#[no_mangle]\npub extern "C" fn two_hint_quotient_i32('
          "a: i32, b: i32) -> i32 {\n    unsafe {\n"
          "        core::hint::assert_unchecked(b != 0);\n"
          "        core::hint::assert_unchecked(b != -1);\n"
          "    }\n    a / b\n}"),
    probe("widened_quotient_i32",
          "the signed division done at double width, where the extreme"
          " cannot arise, then narrowed",
          '#[no_mangle]\npub extern "C" fn widened_quotient_i32('
          "a: i32, b: i32) -> i32 {\n    unsafe {\n"
          "        core::hint::assert_unchecked(b != 0);\n"
          "    }\n    (((a as i64) / (b as i64)) as i32)\n}"),
    probe("widened_remainder_i32",
          "the same for the signed remainder",
          '#[no_mangle]\npub extern "C" fn widened_remainder_i32('
          "a: i32, b: i32) -> i32 {\n    unsafe {\n"
          "        core::hint::assert_unchecked(b != 0);\n"
          "    }\n    (((a as i64) % (b as i64)) as i32)\n}"),
    probe("widened_quotient_i8",
          "the narrowest signed quotient, done at 32 bits",
          '#[no_mangle]\npub extern "C" fn widened_quotient_i8('
          "a: i8, b: i8) -> i8 {\n    unsafe {\n"
          "        core::hint::assert_unchecked(b != 0);\n"
          "    }\n    (((a as i32) / (b as i32)) as i8)\n}"),
    probe("widened_quotient_i64",
          "the 64-bit signed quotient done at 128 bits",
          '#[no_mangle]\npub extern "C" fn widened_quotient_i64('
          "a: i64, b: i64) -> i64 {\n    unsafe {\n"
          "        core::hint::assert_unchecked(b != 0);\n"
          "    }\n    (((a as i128) / (b as i128)) as i64)\n}"),
    probe("both_hint_quotient_i64",
          "the 64-bit signed quotient with the unreachable spelling",
          '#[no_mangle]\npub extern "C" fn both_hint_quotient_i64('
          "a: i64, b: i64) -> i64 {\n    unsafe {\n"
          "        if b == 0 || (a == i64::MIN && b == -1) {\n"
          "            core::hint::unreachable_unchecked();\n"
          "        }\n    }\n    a / b\n}"),
]


def run_probes4():
    return run_named_set(PROBES4, FACTS4)


def run_probes3():
    return run_named_set(PROBES3, FACTS3)


def run_probes2():
    return run_named_set(PROBES2, FACTS2)


def run_named_set(probes, out_path):
    """one probe set, every probe on its OWN crate, because several are
    expected to be refused and one refusal must not take the rest
    down."""
    work = tempfile.mkdtemp(prefix="o11_facts_set_",
                            dir=os.environ.get("TMPDIR"))
    document = {
        "task": "o11",
        "rustc_version": rustc_version(),
        "ship_flags": SHIP_FLAGS_RUST,
        "probes": [],
    }
    total = len(probes)
    rows = {}
    for index, row in enumerate(probes):
        say("[%d/%d] %s" % (index + 1, total, row["name"]))
        rows.update(probe_each_alone([row], SHIP_FLAGS_RUST, work))
    for row in probes:
        document["probes"].append({
            "name": row["name"],
            "question": row["question"],
            "source": row["source"],
            "ship": rows.get(row["name"]),
        })
    document["peak_kb"] = peak_kb()
    handle = open(out_path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    say("peak resident: %d kB (ceiling ABORT_MEMORY_O11 at 4 GB)"
        % document["peak_kb"])
    for entry in document["probes"]:
        ship_row = entry["ship"] or {}
        if not ship_row.get("carved"):
            say("  %-28s REFUSED %s" % (entry["name"],
                                        ship_row.get("refusal")
                                        or ship_row.get("note")))
            continue
        say("  %-28s %s" % (entry["name"], ship_row["body_text"]))
    return 0


def show(names):
    """print one line per named probe: its name and the body rustc
    emitted for it at the ship flags.  A reader, so a report can cite
    the measured body by a command rather than by a paste."""
    rows = {}
    for path in (FACTS, FACTS2, FACTS3, FACTS4):
        if not os.path.exists(path):
            continue
        document = json.load(open(path))
        for entry in document["probes"]:
            rows[entry["name"]] = entry
    for name in names:
        entry = rows.get(name)
        if entry is None:
            say("%-28s NOT PROBED" % name)
            continue
        ship = entry["ship"] or {}
        if ship.get("carved"):
            say("%-28s %s" % (name, ship["body_text"]))
            continue
        say("%-28s REFUSED %s" % (name, ship.get("refusal")
                                  or ship.get("note")))
    return 0


def main(argv):
    if len(argv) < 2:
        say(__doc__)
        return 2
    if argv[1] == "probe":
        return run_probes()
    if argv[1] == "probe2":
        return run_probes2()
    if argv[1] == "probe3":
        return run_probes3()
    if argv[1] == "probe4":
        return run_probes4()
    if argv[1] == "show":
        return show(argv[2:])
    say("unknown command %s" % argv[1])
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
