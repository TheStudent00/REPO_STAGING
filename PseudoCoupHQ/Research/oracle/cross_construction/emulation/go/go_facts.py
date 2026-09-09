#!/usr/bin/env python3
"""go_facts.py -- task g1, step 1: what the go toolchain ITSELF does,
read off its own emission, for every rule the go renderer will need.

Node: hq.research.arch_unit_oracle.cross_construction
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/CORE_0_3_2_2_cross_construction.md`,
FROZEN for term-level composition; task o7 opened the emulation route
with c as the target, task o11 added rust, and this task adds go and
swift, which asks the same question of two more compilers and does not
unfreeze the node).

WHAT THIS FILE IS, one sentence, in relation: it is the evidence under
the go column of task g1's spelling table -- one small go function per
question, built at the SAME flags the go arch-unit corpus was built
with, carved with the SAME objdump reader -- so every row of that table
is the compiler's own emission rather than a recollection of go's
rules.

WHY IT EXISTS: task o11 section 3.1 (log 226) is the shape this task
was told to copy: before a spelling is written, the target is MEASURED.
Three of task o11's twenty rust spellings changed on what the probes
came back with, so the measurement is not a formality.

THE QUESTIONS, each one probe below:
  * do plain `+`, `-`, `*` and unary `-` wrap at the corpus's ship
    flags, or do they check?
  * what does a variable shift count emit -- does go's own rule (a
    count at or above the width answers with the fill) cost a branch,
    and does a count the source has already masked cost one?
  * does `/` check the zero divisor, and does the signed form check
    the extreme case as well?  (Both are EDGE REGIONS this task
    records rather than hides: the brief's rule is to render `/` and
    let the gate report the region.)
  * how are the bits of a float read and written without reaching the
    standard library?
  * what do the integer/float conversions emit?
  * which holders exist -- is there a 128-bit integer, is there a
    16-bit float?
  * which registers does a go function's arrivals land in, and does a
    small leaf function carry a stack-growth prologue that would sit
    in every carved body?

WHAT IS REUSED RATHER THAN COPIED: `emulate.pipeline_extractor()`
(task o7's lift of `lane_gen.DRIVER`'s `extract`, the objdump reader
that carved every unit of the corpus) carves each probe body.  The
ship flags and the module file are read off `lane_gen.py`'s go branch
and are not retyped by hand -- `ship_flags_source()` prints that
branch itself.

MEMORY BOUND, stated as the law requires: one process, no forks; the
probes are a few kilobytes of source and objdump text, and `go build`
writes one executable per build into a temporary directory; peak
resident size is printed at the end; the named abort is
ABORT_MEMORY_G1 at 4 GB, the same ceiling the run lane uses.  Nothing
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
campaign's cross-language matrix (caught by the owner 2026-08-25); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

Nothing here groups or pairs units at all: the probes are hand-written
go functions written to answer a question about the COMPILER, they are
not arch-units of the corpus, and no pool member is read.  Each row is
keyed by its own probe NAME and its `question` field names a
machine-level behaviour, never a language operator token used as a key.

Coding discipline: no compound one-liner statements.

usage:
  go_facts.py probe      build every probe, carve, write go_facts.json
  go_facts.py show <name> ...   the carved body of the named probes
"""

import json
import os
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

FACTS = os.path.join(HERE, "go_facts.json")

GO = "go"

# read off `lane_gen.py` compile_probe, the go branch, LITERAL:
#     if LANG == "go":
#         open(os.path.join(d, "go.mod"), "w").write(GOMOD)
#         open(os.path.join(d, "main.go"), "w").write(p["source"])
#         obj = os.path.join(d, "bin_%s" % mode)
#         cmd = ["go", "build"]
#         if mode == "anchor":
#             cmd.append("-gcflags=-N -l")
#         cmd.extend(["-o", obj, "."])
#         rc, so, se = sh(cmd, cwd=d, timeout=300)
# so the SHIP build is a plain `go build` with no gcflags at all, and
# the artifact is a linked executable rather than an object file.
SHIP_ARGS = ["build"]
ANCHOR_ARGS = ["build", "-gcflags=-N -l"]
GOMOD = "module opprobe\n\ngo 1.26\n"

# `proxy = no` in the instance conf: the module has no requirements, so
# nothing is fetched, and these two settings make that explicit rather
# than leaving it to a timeout.
GO_ENV = {"GOFLAGS": "-mod=mod", "GOPROXY": "off", "GO111MODULE": "on"}


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
    """the go branch of `lane_gen.py` compile_probe, LITERAL, so the
    flags are quoted from the pipeline rather than retyped."""
    path = os.path.join(OP, "lane_gen.py")
    text = open(path).read()
    start = text.index('    if LANG == "go":')
    end = text.index('    if LANG == "swift":')
    return text[start:end].rstrip()


def go_version():
    done = subprocess.run([GO, "version"], capture_output=True,
                          text=True, timeout=120)
    return done.stdout.strip() or done.stderr.strip()


# ==================================================================
# section 1: THE PROBES
# ==================================================================
#
# One probe is one whole go function plus the `main` that keeps it
# alive.  `//go:noinline` is the corpus's own probe shape
# (`probe_gen.emit_go`), and the symbol is `main.<name>`, also the
# corpus's own.

def probe(name, question, params, result, body, extra=""):
    return {
        "name": name,
        "question": question,
        "params": params,
        "result": result,
        "body": body,
        "extra": extra,
    }


PROBES = [
    probe("plain_sum_u32",
          "does plain two-place arithmetic wrap or check, at ship flags",
          "a uint32, b uint32", "uint32", "return a + b"),
    probe("plain_difference_u32",
          "the same for subtraction",
          "a uint32, b uint32", "uint32", "return a - b"),
    probe("plain_product_u64",
          "the same for multiplication",
          "a uint64, b uint64", "uint64", "return a * b"),
    probe("plain_negate_u32",
          "does unary negation of an unsigned holder wrap",
          "a uint32", "uint32", "return -a"),
    probe("plain_left_shift_u32",
          "what a variable left-shift count emits: go defines a count "
          "at or above the width as answering zero, and the machine's "
          "own shift masks the count, so one of the two costs a branch",
          "a uint32, b uint32", "uint32", "return a << b"),
    probe("masked_left_shift_u32",
          "the same with the count already masked to the width in the "
          "source, which is the shape the model table's own term has",
          "a uint32, b uint32", "uint32", "return a << (b & 31)"),
    probe("masked_right_shift_u32",
          "the logical right shift with the count already masked",
          "a uint32, b uint32", "uint32", "return a >> (b & 31)"),
    probe("masked_arith_shift_i32",
          "the arithmetic right shift with the count already masked",
          "a int32, b uint32", "int32", "return a >> (b & 31)"),
    probe("masked_arith_shift_via_unsigned",
          "the arithmetic right shift as the renderer would spell it "
          "from an unsigned holder: convert, shift, convert back",
          "a uint32, b uint32", "uint32",
          "return uint32(int32(a) >> (b & 31))"),
    probe("plain_quotient_u32",
          "does the unsigned quotient check the zero divisor at ship "
          "flags",
          "a uint32, b uint32", "uint32", "return a / b"),
    probe("plain_quotient_i32",
          "does the signed quotient check the zero divisor AND the "
          "extreme case (the most negative value over minus one, which "
          "go's own specification defines as wrapping)",
          "a int32, b int32", "int32", "return a / b"),
    probe("plain_remainder_i32",
          "the same for the signed remainder",
          "a int32, b int32", "int32", "return a % b"),
    probe("plain_quotient_i64",
          "the signed quotient one width up",
          "a int64, b int64", "int64", "return a / b"),
    probe("guarded_quotient_i32",
          "what an explicit guard in the source does to those checks",
          "a int32, b int32", "int32",
          "if b == 0 {\n\t\treturn 0\n\t}\n\tif a == -2147483648 && "
          "b == -1 {\n\t\treturn a\n\t}\n\treturn a / b"),
    probe("widen_u8_to_u32",
          "is a widening conversion free, or does it emit a move",
          "a uint8", "uint32", "return uint32(a)"),
    probe("narrow_u32_to_u8",
          "what a narrowing conversion emits",
          "a uint32", "uint8", "return uint8(a)"),
    probe("sign_extend_i8_to_i64",
          "what a sign-extending conversion emits",
          "a int8", "int64", "return int64(a)"),
    probe("select_u64",
          "THE CONDITIONAL.  Go has no conditional expression at all, "
          "so the renderer needs a helper function; does a small helper "
          "inline to a conditional move, or does it stay a call",
          "c bool, x uint64, y uint64", "uint64",
          "return sel64(c, x, y)",
          "func sel64(c bool, x uint64, y uint64) uint64 {\n"
          "\tif c {\n\t\treturn x\n\t}\n\treturn y\n}"),
    probe("select_inline_u64",
          "the same written out in the function itself, so the helper "
          "and the direct form can be compared",
          "c bool, x uint64, y uint64", "uint64",
          "if c {\n\t\treturn x\n\t}\n\treturn y"),
    probe("compare_u32",
          "what an unsigned comparison answering a truth value emits",
          "a uint32, b uint32", "uint32",
          "return sel32(a < b, 1, 0)",
          "func sel32(c bool, x uint32, y uint32) uint32 {\n"
          "\tif c {\n\t\treturn x\n\t}\n\treturn y\n}"),
    probe("f64_bits_math",
          "reading a float's bits through the standard library's own "
          "function -- is it a call or one instruction",
          "a float64", "uint64", "return math.Float64bits(a)",
          "__import_math__"),
    probe("bits_f64_math",
          "writing a float from its bits, the same way",
          "a uint64", "float64", "return math.Float64frombits(a)",
          "__import_math__"),
    probe("f32_bits_math",
          "the same at 32 bits",
          "a float32", "uint32", "return math.Float32bits(a)",
          "__import_math__"),
    probe("bits_f32_math",
          "the same at 32 bits, the other way",
          "a uint32", "float32", "return math.Float32frombits(a)",
          "__import_math__"),
    probe("f64_bits_unsafe",
          "reading a float's bits with no import of the standard "
          "library's math, in case the library form is a call",
          "a float64", "uint64",
          "return *(*uint64)(unsafe.Pointer(&a))",
          "__import_unsafe__"),
    probe("sum_f32",
          "float addition at 32 bits",
          "a float32, b float32", "float32", "return a + b"),
    probe("sum_f64",
          "float addition at 64 bits",
          "a float64, b float64", "float64", "return a + b"),
    probe("int_to_f64",
          "the signed-integer-to-float conversion",
          "a int64", "float64", "return float64(a)"),
    probe("uint_to_f64",
          "the unsigned-integer-to-float conversion",
          "a uint64", "float64", "return float64(a)"),
    probe("f64_to_int",
          "the float-to-integer conversion: does it truncate straight "
          "to the machine's own instruction, or does it check",
          "a float64", "int64", "return int64(a)"),
    probe("absolute_f64",
          "the float absolute value with no standard-library call: the "
          "sign bit cleared through the bits",
          "a float64", "float64",
          "return math.Float64frombits(math.Float64bits(a) & "
          "0x7fffffffffffffff)",
          "__import_math__"),
    probe("wide_holder_128",
          "is there a 128-bit integer holder in go",
          "a uint128, b uint128", "uint128", "return a + b"),
    probe("float16_holder",
          "is there a 16-bit float holder in go",
          "a float16, b float16", "float16", "return a + b"),
    probe("arrival_registers_six",
          "WHICH REGISTERS the arrivals land in, read off a function "
          "that reads all six of them in order",
          "a uint64, b uint64, c uint64, d uint64, e uint64, f uint64",
          "uint64",
          "return a - b - c - d - e - f"),
    probe("arrival_registers_float",
          "the same for float arrivals",
          "a float64, b float64, c float64", "float64",
          "return a - b - c"),
    probe("leaf_prologue",
          "does the smallest possible function carry a stack-growth "
          "prologue that would sit in every carved emulation body",
          "a uint64", "uint64", "return a"),
]


# ------------------------------------------------------------------
# THE SECOND SET.  The first set answered the arithmetic, the shifts,
# the division and the arrival registers.  These are the questions the
# first set's answers RAISED: the standard library's own bit-cast
# carries a `nop` and the pointer-cast form does not, so the other
# three directions are measured too; go refused the two absent holders
# with a banner rather than a diagnostic, so those two are re-run with
# the pipeline's own three-pass reading of a go refusal
# (`lane_gen.firstline`); and the conditional helper is measured at
# every width and sort the renderer will ask it for.
# ------------------------------------------------------------------

SEL = ("func sel%s(c bool, x %s, y %s) %s {\n"
       "\tif c {\n\t\treturn x\n\t}\n\treturn y\n}")

PROBES2 = [
    probe("bits_f64_unsafe",
          "writing a float from its bits with a pointer cast rather "
          "than the standard library's own function, which carried a "
          "`nop`",
          "a uint64", "float64",
          "return *(*float64)(unsafe.Pointer(&a))",
          "__import_unsafe__"),
    probe("f32_bits_unsafe",
          "reading a 32-bit float's bits with a pointer cast",
          "a float32", "uint32",
          "return *(*uint32)(unsafe.Pointer(&a))",
          "__import_unsafe__"),
    probe("bits_f32_unsafe",
          "writing a 32-bit float from its bits with a pointer cast",
          "a uint32", "float32",
          "return *(*float32)(unsafe.Pointer(&a))",
          "__import_unsafe__"),
    probe("complement_u32",
          "the bitwise complement",
          "a uint32", "uint32", "return ^a"),
    probe("bitwise_three_u32",
          "the three two-place bitwise operations in one body",
          "a uint32, b uint32", "uint32",
          "return (a & b) | (a ^ b)"),
    probe("signed_compare_i32",
          "a signed comparison answering a truth value, spelled from "
          "unsigned holders as the renderer will spell it",
          "a uint32, b uint32", "uint32",
          "return sel32(int32(a) < int32(b), 1, 0)",
          SEL % ("32", "uint32", "uint32", "uint32")),
    probe("equality_u64",
          "an equality answering a truth value",
          "a uint64, b uint64", "uint64",
          "return sel64(a == b, 1, 0)",
          SEL % ("64", "uint64", "uint64", "uint64")),
    probe("select_f64",
          "the conditional with FLOAT arms, which the renderer needs "
          "for a float-valued conditional",
          "c bool, x float64, y float64", "float64",
          "return selfp64(c, x, y)",
          SEL % ("fp64", "float64", "float64", "float64")),
    probe("nested_select_u64",
          "two conditionals nested in one expression, so the helper is "
          "seen to inline more than once",
          "c bool, d bool, x uint64, y uint64", "uint64",
          "return sel64(c, sel64(d, x, y), y)",
          SEL % ("64", "uint64", "uint64", "uint64")),
    probe("concat_shift_or_u64",
          "the two-word join the c renderer writes as a shift and an "
          "or",
          "a uint32, b uint32", "uint64",
          "return (uint64(a) << 32) | uint64(b)"),
    probe("zero_extend_after_narrow",
          "a narrowing followed by a widening, the shape a masked "
          "extract takes",
          "a uint64", "uint64", "return uint64(uint32(a))"),
    probe("narrow_arrival_u8",
          "WHAT ARRIVES in a narrow holder: does the go callee read "
          "the whole register or only its low bits, which is the "
          "question task o7's caller-extension re-pose asks",
          "a uint8, b uint8", "uint32",
          "return uint32(a) + uint32(b)"),
    probe("narrow_arrival_u16",
          "the same one width up",
          "a uint16, b uint16", "uint32",
          "return uint32(a) + uint32(b)"),
    probe("truth_arrival",
          "what a truth-valued arrival looks like in the register",
          "a bool", "uint64", "return sel64(a, 1, 0)",
          SEL % ("64", "uint64", "uint64", "uint64")),
    probe("int32_to_f64",
          "the 32-bit signed-integer-to-float conversion",
          "a int32", "float64", "return float64(a)"),
    probe("int32_to_f32",
          "the same to a 32-bit float",
          "a int32", "float32", "return float32(a)"),
    probe("f64_to_f32",
          "the float-to-float narrowing",
          "a float64", "float32", "return float32(a)"),
    probe("f32_to_f64",
          "the float-to-float widening",
          "a float32", "float64", "return float64(a)"),
    probe("wide_holder_128_again",
          "the 128-bit integer holder again, so the refusal is read by "
          "the pipeline's own three-pass rule rather than by the first "
          "non-empty line, which was go's package banner",
          "a uint128, b uint128", "uint128", "return a + b"),
    probe("float16_holder_again",
          "the 16-bit float holder, read the same way",
          "a float16, b float16", "float16", "return a + b"),
]


def source_for(row):
    """one whole go program: the probe function, whatever helper it
    names, the package globals that keep it reachable, and `main`."""
    lines = []
    lines.append("// task g1 probe -- %s" % row["name"])
    lines.append("package main")
    lines.append("")
    if row["extra"] == "__import_math__":
        lines.append('import "math"')
        lines.append("")
    elif row["extra"] == "__import_unsafe__":
        lines.append('import "unsafe"')
        lines.append("")
    elif row["extra"]:
        lines.append(row["extra"])
        lines.append("")
    lines.append("//go:noinline")
    lines.append("func %s(%s) %s {" % (row["name"], row["params"],
                                       row["result"]))
    lines.append("\t%s" % row["body"])
    lines.append("}")
    lines.append("")
    names = []
    for index, declaration in enumerate(row["params"].split(", ")):
        parts = declaration.split(" ")
        lines.append("var g%d %s" % (index, parts[1]))
        names.append("g%d" % index)
    lines.append("var sink interface{}")
    lines.append("")
    lines.append("func main() {")
    lines.append("\tsink = %s(%s)" % (row["name"], ", ".join(names)))
    lines.append("\t_ = sink")
    lines.append("}")
    return "\n".join(lines) + "\n"


# ==================================================================
# section 2: THE BUILD AND THE CARVE
# ==================================================================

def pipeline_firstline(text):
    """the PIPELINE's own reading of a compiler refusal, imported from
    `lane_gen.py` rather than re-implemented.

    Its docstring says why this matters for go in particular: go leads
    with a banner naming the package (`# opprobe`) and its diagnostics
    never contain the word `error`, so a rule that reads the first
    non-empty line records the banner and throws the testimony away --
    which is exactly what `firstline` above did to the two absent-holder
    probes of the first set.

    It is defined INSIDE `lane_gen.DRIVER` (the lane's embedded python),
    not at module level, so it is taken out of that text at run time --
    the same way `emulate.pipeline_extractor` takes `extract` out of it,
    and by the same slice-compile-exec, so the function that runs here
    is the function the corpus's own lanes ran."""
    import re
    import lane_gen as LG
    if "firstline" not in REFUSAL_READER:
        driver = LG.DRIVER
        start = driver.index("DIAG = re.compile")
        end = driver.index("def write_unit(")
        namespace = {"re": re}
        exec(compile(driver[start:end], "lane_gen.DRIVER[firstline]",
                     "exec"), namespace)
        REFUSAL_READER["firstline"] = namespace["firstline"]
    return REFUSAL_READER["firstline"](text)


REFUSAL_READER = {}


def build_and_carve(source, symbol, args):
    """the go corpus's own build and carve: `go build` in a module
    directory, objdump read by `emulate.pipeline_extractor()`, which is
    `lane_gen.DRIVER`'s own `extract`."""
    import emulate as E
    extract = E.pipeline_extractor()
    work = tempfile.mkdtemp(prefix="g1_go_", dir=os.environ.get("TMPDIR"))
    handle = open(os.path.join(work, "go.mod"), "w")
    handle.write(GOMOD)
    handle.close()
    handle = open(os.path.join(work, "main.go"), "w")
    handle.write(source)
    handle.close()
    binary = os.path.join(work, "bin_ship")
    environment = dict(os.environ)
    environment.update(GO_ENV)
    environment["HOME"] = work
    environment["GOCACHE"] = os.path.join(work, "gocache")
    environment["GOPATH"] = os.path.join(work, "gopath")
    command = [GO] + args + ["-o", binary, "."]
    done = subprocess.run(command, capture_output=True, text=True,
                          timeout=600, cwd=work, env=environment)
    if done.returncode != 0 or not os.path.exists(binary):
        raw_text = done.stderr or done.stdout
        refusal = {
            "first_non_empty_line": firstline(raw_text),
            "the_pipelines_own_reading": pipeline_firstline(raw_text),
            "whole_diagnostic": raw_text.strip()[:800],
        }
        cleanup(work)
        return None, None, refusal
    done = subprocess.run(["objdump", "-dr", "--disassemble=" + symbol,
                           binary], capture_output=True, text=True,
                          timeout=300)
    got = extract(done.stdout, symbol, True)
    cleanup(work)
    if got is None:
        return None, None, "objdump found no symbol %s" % symbol
    raw, mnem = got
    return raw, mnem, None


def cleanup(work):
    for root, dirs, files in os.walk(work, topdown=False):
        for name in files:
            try:
                os.unlink(os.path.join(root, name))
            except OSError:
                pass
        for name in dirs:
            try:
                os.rmdir(os.path.join(root, name))
            except OSError:
                pass
    try:
        os.rmdir(work)
    except OSError:
        pass


def one_probe(row):
    source = source_for(row)
    symbol = "main.%s" % row["name"]
    raw, mnem, refusal = build_and_carve(source, symbol, SHIP_ARGS)
    record = {
        "name": row["name"],
        "question": row["question"],
        "source": source,
        "symbol": symbol,
    }
    if raw is None:
        record["built"] = False
        record["refusal"] = refusal
        return record
    record["built"] = True
    record["body_text"] = "; ".join(mnem)
    record["body_bytes"] = " ".join(raw)
    record["byte_count"] = len(raw)
    record["instruction_count"] = len(mnem)
    calls = []
    for line in mnem:
        if line.startswith("call"):
            calls.append(line)
    record["calls"] = calls
    return record


def probe_command():
    document = {
        "task": "g1",
        "go_version": go_version(),
        "ship_args": SHIP_ARGS,
        "anchor_args": ANCHOR_ARGS,
        "ship_flags_source": ship_flags_source(),
        "gomod": GOMOD,
        "probes": [],
    }
    asked = PROBES + PROBES2
    total = len(asked)
    for index, row in enumerate(asked):
        say("[%d/%d] %s" % (index + 1, total, row["name"]))
        record = one_probe(row)
        document["probes"].append(record)
        if record.get("built"):
            say("   %s" % record["body_text"])
        else:
            say("   NOT BUILT, the pipeline's own reading: %s"
                % (record.get("refusal") or {}).get(
                    "the_pipelines_own_reading"))
            say("   NOT BUILT, the whole diagnostic: %s"
                % (record.get("refusal") or {}).get("whole_diagnostic"))
    document["peak_kb"] = peak_kb()
    handle = open(FACTS, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    say("")
    say("go: %s" % document["go_version"])
    say("wrote %s" % FACTS)
    say("peak resident: %d kB (ceiling ABORT_MEMORY_G1 at 4 GB)"
        % document["peak_kb"])
    return 0


def show_command(names):
    document = json.load(open(FACTS))
    for record in document["probes"]:
        if names and record["name"] not in names:
            continue
        if record.get("built"):
            say("%-28s %s" % (record["name"], record["body_text"]))
        else:
            say("%-28s REFUSED %s" % (record["name"],
                                      record.get("refusal")))
    return 0


def main(argv):
    if not argv:
        say(__doc__)
        return 2
    if argv[0] == "probe":
        return probe_command()
    if argv[0] == "show":
        return show_command(argv[1:])
    say("unknown command %r" % argv[0])
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
