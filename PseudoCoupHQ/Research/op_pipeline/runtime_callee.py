#!/usr/bin/env python3
"""runtime_callee.py -- THE COMPILER'S OWN RUNTIME, FOLLOWED.

Node: `hq.research.compiler_graph.arch_unit.runtime_callee`
CORE: Planning/node_0_3_research/node_0_3_5_compiler_graph/
      node_0_3_5_1_arch_unit/node_0_3_5_1_8_runtime_callee/
      CORE_0_3_5_1_8_runtime_callee.md

TASK 59, round 12 (log_158).  The code carries the node's name, and the
class carries the node's `## design`: attribute `archive_paths`;
methods `is_runtime_routine`, `extract_callee`, `attach`.

WHAT THIS FILE IS FOR.  A body that transfers to `__divti3`,
`__udivti3`, `__modti3` or `__umodti3` leaves its answer in a routine
the compiler SHIPPED WITH ITSELF as its own lowering of an operation
the hardware has no single instruction for.  the owner, 2026-09-03: "if its
within the compiler, its not a library call.  if the compiler is
importing something as a standard feature, also not a library call."
That ruling SUPERSEDES the verdict recorded the same day in
`out_of_scope_library_calls.json`; that file's LIST of 308 units
stands, and this file's supersession note is written as a NEW file,
`out_of_scope_library_calls_superseded.json` -- the recorded file is
never edited.

WHERE THE CALLEE COMES FROM.  From the archive on THIS machine,
located by asking the TOOLCHAIN ITSELF where its archive is
(`gcc -print-libgcc-file-name`, `clang -print-file-name=...`,
`rustc --print sysroot` and the one `compiler_builtins` rlib under
it).  No path in this file is typed in by hand; every path is read
back from a toolchain's own output and recorded beside the command
that produced it, so the record is a pin and not a claim.

WHAT COUNTS AS A RUNTIME ROUTINE is decided by MACHINE-FORM EVIDENCE,
never by a list of names this file believes in: a callee name is a
runtime routine when `nm --print-armap` reports that name DEFINED in
one of the archives the toolchains named.  A name no archive defines
is not one.

--------------------------------------------------------------------
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

No operator token appears in this file as a key, a grouping or a row
structure.  Every mnemonic sits under `mnem`; every routine name sits
under `callee`, beside `bytes` and `mnem`, as machine form.

Coding discipline: no compound one-liner statements.
"""

import glob
import json
import os
import re
import shutil
import subprocess
import tempfile


# ------------------------------------------------------------------
# asking a toolchain where its own archive is
# ------------------------------------------------------------------

def run_command(argv):
    """(exit code, stdout text, stderr text).  Never raises."""
    try:
        done = subprocess.run(argv, capture_output=True, text=True,
                              timeout=120)
    except FileNotFoundError:
        return 127, "", "no such executable: %s" % argv[0]
    except subprocess.TimeoutExpired:
        return 124, "", "timed out: %s" % " ".join(argv)
    return done.returncode, done.stdout, done.stderr


class Probe(object):
    """one toolchain question and the answer it gave, kept together so
    a path is always readable as the output of the command beside it."""

    def __init__(self, toolchain, argv):
        self.toolchain = toolchain
        self.argv = list(argv)
        code, out, err = run_command(self.argv)
        self.exit_code = code
        self.stdout = out.strip()
        self.stderr = err.strip()

    def path(self):
        """the answer, when it is an absolute path that exists."""
        if self.exit_code != 0:
            return None
        if not self.stdout:
            return None
        first = self.stdout.splitlines()[0].strip()
        if not os.path.isabs(first):
            return None
        if not os.path.exists(first):
            return None
        return first

    def as_record(self):
        return {
            "toolchain": self.toolchain,
            "command": " ".join(self.argv),
            "exit_code": self.exit_code,
            "stdout_first_line": (self.stdout.splitlines()[0]
                                  if self.stdout else ""),
            "stderr_first_line": (self.stderr.splitlines()[0]
                                  if self.stderr else ""),
            "path": self.path(),
        }


# The toolchains that BUILT the units of this pipeline, and the
# question each one is asked.  `lane_gen.py` records what built each
# language: c -> /usr/bin/clang, cpp -> /usr/bin/clang++,
# rust -> rustc, swift -> /persist/swift/usr/bin/swiftc.  gcc is asked
# too, because it is the other system toolchain on this machine and
# its answer is part of the record.
TOOLCHAIN_QUESTIONS = (
    ("gcc", ["gcc", "-print-libgcc-file-name"]),
    ("clang", ["clang", "-print-file-name=libclang_rt.builtins-x86_64.a"]),
    ("clang++", ["clang++",
                 "-print-file-name=libclang_rt.builtins-x86_64.a"]),
    ("rustc", ["rustc", "--print", "sysroot"]),
    ("swiftc", ["swiftc", "-print-target-info"]),
)

# Which toolchain built which language.  Read off `lane_gen.py`'s own
# `compile_probe`, not assumed.
TOOLCHAIN_OF_LANGUAGE = {
    "c": "clang",
    "cpp": "clang++",
    "rust": "rustc",
    "swift": "swiftc",
    "go": "go",
}

RUST_BUILTINS_GLOB = os.path.join(
    "lib", "rustlib", "x86_64-unknown-linux-gnu", "lib",
    "libcompiler_builtins-*.rlib")


# ------------------------------------------------------------------
# reading an archive
# ------------------------------------------------------------------

ARMAP_LINE = re.compile(r"^(\S+) in (\S+)$")


def defined_symbols(archive):
    """{symbol name -> the archive member that defines it}, read from
    the archive's own index with `nm --print-armap`."""
    code, out, err = run_command(["nm", "--print-armap", archive])
    if code != 0:
        return {}, err.strip()
    table = {}
    for line in out.splitlines():
        hit = ARMAP_LINE.match(line.strip())
        if hit is None:
            continue
        name = hit.group(1)
        member = hit.group(2)
        if name in table:
            continue
        table[name] = member
    return table, ""


DISASSEMBLY_LINE = re.compile(
    r"^\s*[0-9a-f]+:\s+((?:[0-9a-f]{2} )+)\s*\t(.*)$")

# a line objdump prints with bytes and no text: the tail of an
# instruction whose encoding is too long for one line.
BYTES_ONLY_LINE = re.compile(r"^\s*[0-9a-f]+:\s+((?:[0-9a-f]{2} ?)+)$")

# `nm -S --defined-only` prints "<address> <size> <type> <name>".  A
# symbol with no size prints three columns instead of four.
SYMBOL_SIZE_LINE = re.compile(
    r"^([0-9a-f]+)\s+([0-9a-f]+)\s+(\S)\s+(\S+)$")

# the relocation objdump -dr prints on its own line UNDER the
# instruction it belongs to: "\t\t\t33: R_X86_64_PC32\t.LCPI0_0-0x4"
RELOCATION_LINE = re.compile(
    r"^\s+([0-9a-f]+):\s+(R_\S+)\s+(\S+)\s*$")


def member_symbols(member_path):
    """{symbol name -> (address, size)} for one archive member, read
    with `nm -S --defined-only`.

    WHY ADDRESS AND SIZE, and not the name alone: one address in a
    member carries several names.  clang's `comparetf2.c.o` defines
    `__cmptf2`, `__eqtf2`, `__netf2`, `__letf2` and `__lttf2` at
    address 0 with size 0xb9, and `objdump --disassemble=__netf2`
    prints an EMPTY body for it, because objdump labels the address
    with the first name it holds.  Disassembling the address RANGE
    answers for every one of those names.
    """
    code, out, err = run_command(
        ["nm", "-S", "--defined-only", member_path])
    if code != 0:
        return {}, err.strip()
    table = {}
    for line in out.splitlines():
        hit = SYMBOL_SIZE_LINE.match(line.rstrip())
        if hit is None:
            continue
        address = int(hit.group(1), 16)
        size = int(hit.group(2), 16)
        name = hit.group(4)
        if size == 0:
            continue
        table[name] = (address, size)
    return table, ""


def fold_relocations(objdump_text, symbol_comment_suffix=None):
    """objdump -dr output -> (body lines, bytes as hex text).

    Every relocation objdump prints on its own line is FOLDED onto
    the instruction above it as `!!reloc=<type>:<symbol>`, which is
    exactly the annotation the corpus's own bodies carry.  That
    annotation is the only place a callee's name survives in an
    UNLINKED body: the `call` itself disassembles as a transfer to an
    address inside the same member (log_161's finding).
    """
    lines = []
    byte_pieces = []
    for raw in objdump_text.splitlines():
        hit = DISASSEMBLY_LINE.match(raw)
        if hit is not None:
            byte_pieces.append(hit.group(1).strip())
            text = hit.group(2)
            text = text.split("#", 1)[0]
            text = " ".join(text.split())
            if not text:
                continue
            lines.append(text)
            continue
        hit = RELOCATION_LINE.match(raw)
        if hit is not None:
            if not lines:
                continue
            annotation = "!!reloc=%s:%s" % (hit.group(2), hit.group(3))
            lines[-1] = "%s %s" % (lines[-1], annotation)
            continue
        hit = BYTES_ONLY_LINE.match(raw)
        if hit is not None:
            if byte_pieces:
                byte_pieces[-1] = "%s %s" % (byte_pieces[-1],
                                             hit.group(1).strip())
            continue
    return lines, " ".join(byte_pieces)


def disassemble_range(member_path, address, size):
    """(the body's lines with relocations folded in, the body's bytes
    as hex text, trouble).  The range is the symbol's own address and
    size, so an address carrying several names answers for all of
    them."""
    argv = [
        "objdump", "-dr",
        "--start-address=0x%x" % address,
        "--stop-address=0x%x" % (address + size),
        member_path,
    ]
    code, out, err = run_command(argv)
    if code != 0:
        return None, None, err.strip()
    lines, byte_text = fold_relocations(out)
    if not lines:
        return None, None, (
            "objdump printed no instruction in the range "
            "0x%x..0x%x of %s" % (address, address + size,
                                  os.path.basename(member_path)))
    return lines, byte_text, ""


TRANSFER_STEM = re.compile(r"^(call|callq|jmp|jmpq)\b")


def nested_callees(body_lines):
    """the names this body transfers to, read off the relocation on
    each transfer line, in first-seen order and without repeats."""
    out = []
    for line in body_lines:
        if TRANSFER_STEM.match(line) is None:
            continue
        if "!!reloc=" not in line:
            continue
        piece = line.split("!!reloc=", 1)[1]
        if ":" not in piece:
            continue
        name = piece.split(":", 1)[1]
        name = name.split("-")[0]
        name = name.split("+")[0]
        name = name.strip()
        if not name:
            continue
        if name in out:
            continue
        out.append(name)
    return out


def disassemble(member_path, symbol):
    """(the body's lines, the body's bytes as hex text).

    The text is objdump's own AT&T text with the address column and
    the byte column removed and inner whitespace collapsed, which is
    the shape every other body in this pipeline is stored in.
    """
    code, out, err = run_command(
        ["objdump", "-d", "--disassemble=%s" % symbol, member_path])
    if code != 0:
        return None, None, err.strip()
    lines = []
    byte_pieces = []
    started = False
    for raw in out.splitlines():
        if raw.strip().endswith("<%s>:" % symbol):
            started = True
            continue
        if not started:
            continue
        if not raw.strip():
            if lines:
                break
            continue
        hit = DISASSEMBLY_LINE.match(raw)
        if hit is None:
            continue
        byte_pieces.append(hit.group(1).strip())
        text = hit.group(2)
        text = text.split("#", 1)[0]
        text = " ".join(text.split())
        if not text:
            continue
        lines.append(text)
    if not lines:
        return None, None, "objdump printed no body for %s" % symbol
    return lines, " ".join(byte_pieces), ""


# ------------------------------------------------------------------
# the arrival contract, read off the callee's own text
# ------------------------------------------------------------------

PURE_WRITE_MNEMONICS = frozenset([
    "mov", "movl", "movq", "movb", "movw", "movabs",
    "movzbl", "movzwl", "movzbq", "movzwq", "movsbl", "movswl",
    "movsbq", "movswq", "movslq", "movsbw", "movzbw",
    "lea", "movss", "movsd", "movaps", "movapd", "movdqa", "movdqu",
    "movd", "set", "xorps", "pxor",
])

REGISTER_TOKEN = re.compile(r"%([a-z][a-z0-9]*)")


def arrival_families(body_lines, family_of):
    """the register families the text READS BEFORE IT WRITES THEM, in
    first-read order.

    This is canon35_universal.infer_entry_contract's own rule -- "a
    family is an ARRIVAL when the text reads it before it writes it" --
    with its four-family horizon removed, because a 128-bit runtime
    routine takes its two arguments in FOUR general registers and a
    horizon of four named families would answer for a shape that is
    not this one.  The rule is unchanged; only what it ranges over is.
    """
    written = set()
    arrives = []
    for line in body_lines:
        pieces = line.split(" ", 1)
        mnemonic = pieces[0]
        if len(pieces) == 1:
            continue
        operand_text = pieces[1]
        operands = [one.strip() for one in operand_text.split(",")]
        for position, operand in enumerate(operands):
            for token in REGISTER_TOKEN.findall(operand):
                family = family_of(token)
                if family is None:
                    continue
                is_write = position == len(operands) - 1
                if is_write:
                    if operand.startswith("%"):
                        if mnemonic in PURE_WRITE_MNEMONICS:
                            written.add(family)
                            continue
                if family in written:
                    continue
                if family in arrives:
                    continue
                arrives.append(family)
    return arrives


# ------------------------------------------------------------------
# the class the node names
# ------------------------------------------------------------------

class RuntimeCallee(object):
    """the compiler's own runtime, located, extracted and attached.

    attributes:
        archive_paths   the libgcc / compiler-rt / compiler_builtins
                        archives on this machine, per toolchain, each
                        recorded beside the command that named it
    methods:
        is_runtime_routine
        extract_callee
        attach
    """

    def __init__(self, family_of=None):
        self.probes = []
        self.archive_paths = {}
        self.symbol_tables = {}
        self.not_located = {}
        self.family_of = family_of
        self._locate()

    # ---------------------------------------------------------- locate
    def _locate(self):
        for toolchain, argv in TOOLCHAIN_QUESTIONS:
            probe = Probe(toolchain, argv)
            self.probes.append(probe)
            answer = probe.path()
            if answer is None:
                self.not_located[toolchain] = probe.as_record()
                continue
            if toolchain == "rustc":
                pattern = os.path.join(answer, RUST_BUILTINS_GLOB)
                found = sorted(glob.glob(pattern))
                if not found:
                    record = probe.as_record()
                    record["then_looked_for"] = pattern
                    record["found"] = []
                    self.not_located[toolchain] = record
                    continue
                self.archive_paths[toolchain] = found[0]
                continue
            if not answer.endswith(".a"):
                record = probe.as_record()
                record["why_not_an_archive"] = (
                    "the toolchain answered with something that is "
                    "not an archive file")
                self.not_located[toolchain] = record
                continue
            self.archive_paths[toolchain] = answer
        for toolchain, archive in self.archive_paths.items():
            table, trouble = defined_symbols(archive)
            self.symbol_tables[toolchain] = table
            if trouble:
                self.not_located[toolchain + " (index)"] = {
                    "archive": archive,
                    "trouble": trouble,
                }

    def location_record(self):
        """every question asked and every answer given, for the log."""
        return {
            "probes": [one.as_record() for one in self.probes],
            "archive_paths": dict(self.archive_paths),
            "not_located": dict(self.not_located),
            "symbols_indexed": {
                key: len(value)
                for key, value in self.symbol_tables.items()
            },
        }

    # ------------------------------------------------ is_runtime_routine
    def is_runtime_routine(self, callee, toolchain=None):
        """(yes/no, the toolchains whose archive DEFINES this name).

        Machine-form evidence: the archive's own symbol index.  A name
        no archive defines is not a runtime routine, whatever it looks
        like.
        """
        where = []
        for name, table in self.symbol_tables.items():
            if toolchain is not None:
                if name != toolchain:
                    continue
            if callee in table:
                where.append(name)
        return len(where) > 0, where

    # ------------------------------------------------- extract_callee
    def extract_callee(self, callee, toolchain):
        """archive + callee name -> a further ArchUnit: its own bytes,
        text and arrival contract."""
        archive = self.archive_paths.get(toolchain)
        if archive is None:
            return None, ("no archive was located for toolchain %r"
                          % toolchain)
        table = self.symbol_tables.get(toolchain) or {}
        member = table.get(callee)
        if member is None:
            return None, ("the archive %s does not define %s"
                          % (archive, callee))
        work = tempfile.mkdtemp(prefix="runtime_callee_")
        try:
            code, out, err = run_command(
                ["ar", "x", "--output", work, archive, member])
            if code != 0:
                return None, ("`ar x` refused: %s" % err.strip())
            member_path = os.path.join(work, os.path.basename(member))
            if not os.path.exists(member_path):
                return None, ("`ar x` wrote no %s" % member)
            placed, trouble = member_symbols(member_path)
            if trouble:
                return None, ("`nm -S` refused: %s" % trouble)
            where = placed.get(callee)
            if where is None:
                return None, ("the member %s defines no sized symbol "
                              "named %s" % (member, callee))
            address, size = where
            lines, byte_text, trouble = disassemble_range(
                member_path, address, size)
            if lines is None:
                return None, trouble
        finally:
            shutil.rmtree(work, ignore_errors=True)
        arrives = []
        if self.family_of is not None:
            arrives = arrival_families(lines, self.family_of)
        labelled, label_record = self.positional_form(lines, byte_text)
        unit = {
            "unit": "runtime/%s/%s" % (toolchain, callee),
            "callee": callee,
            "kind": "runtime_callee",
            "toolchain": toolchain,
            "archive": archive,
            "archive_member": member,
            "symbol_address": address,
            "symbol_size": size,
            "body_as_read": list(lines),
            "body_verbatim": labelled,
            "branch_labels": label_record,
            "body_text": "; ".join(lines),
            "body_bytes": byte_text,
            "body_source": "the runtime archive this toolchain names "
                           "as its own, read with `ar x` and "
                           "`objdump -dr` over the symbol's own "
                           "address range",
            "instruction_count": len(lines),
            "arrival_families": arrives,
            "arrival_source": "the families the callee's own text "
                              "reads before it writes them",
            "nested_callees": nested_callees(lines),
            "nested_callee_source": "the relocation on each `call` "
                                    "line of this body; an unlinked "
                                    "`call` disassembles as an "
                                    "in-member transfer, so the "
                                    "relocation is the only place "
                                    "the name survives",
        }
        return unit, ""

    @staticmethod
    def positional_form(lines, byte_text):
        """the body in the pipeline's own positional-label form, so an
        attached body reads exactly like every other stored body."""
        try:
            import ledger
        except ImportError:
            return list(lines), {}
        return ledger.positional_labels(list(lines), byte_text)

    # -------------------------------------------------- extract_closure
    def extract_closure(self, callee, toolchain, seen=None):
        """callee -> {unit name -> unit} for that callee AND every
        callee its body names through a relocation, followed the same
        way.  `seen` is the cycle guard: a name already extracted is
        never extracted a second time, so a routine that reaches
        itself terminates."""
        if seen is None:
            seen = set()
        units = {}
        trouble_by_name = {}
        pending = [callee]
        while pending:
            name = pending.pop(0)
            key = "%s/%s" % (toolchain, name)
            if key in seen:
                continue
            seen.add(key)
            defined, where = self.is_runtime_routine(name, toolchain)
            if not defined:
                trouble_by_name[key] = (
                    "the archive index of toolchain %r defines no "
                    "symbol named %s" % (toolchain, name))
                continue
            unit, trouble = self.extract_callee(name, toolchain)
            if unit is None:
                trouble_by_name[key] = trouble
                continue
            units[key] = unit
            for further in unit["nested_callees"]:
                further_key = "%s/%s" % (toolchain, further)
                if further_key in seen:
                    continue
                pending.append(further)
        return units, trouble_by_name

    # ---------------------------------------------------------- attach
    def attach(self, caller_record, callee_unit):
        """caller ArchUnit + callee ArchUnit -> a NEW caller record
        whose `runtime_callees` references the callee and whose answer
        row is produced by it.

        The caller record handed in is never mutated; the reference is
        written on a copy, so the recorded canon38 unit stays exactly
        as it was recorded.
        """
        out = dict(caller_record)
        references = list(out.get("runtime_callees") or [])
        already = False
        for one in references:
            if one.get("callee") == callee_unit["callee"]:
                already = True
        if not already:
            references.append({
                "callee": callee_unit["callee"],
                "unit": callee_unit["unit"],
                "toolchain": callee_unit["toolchain"],
                "archive": callee_unit["archive"],
                "archive_member": callee_unit["archive_member"],
                "instruction_count": callee_unit["instruction_count"],
                "arrival_families": list(
                    callee_unit["arrival_families"]),
            })
        out["runtime_callees"] = references
        rows = out.get("ledger")
        if rows is None:
            return out, "this caller record carries no ledger"
        answer_name = out.get("out_row") or "OUT-0"
        fresh = []
        touched = 0
        for row in rows:
            if row.get("row") != answer_name:
                fresh.append(row)
                continue
            copy = dict(row)
            copy["produced_by"] = {
                "kind": "runtime_callee",
                "callee": callee_unit["callee"],
            }
            # A body may transfer into the runtime more than once.
            # Each attachment repoints the answer row, so the LAST
            # transfer in the body's own text order is the one left
            # standing -- and `produced_by_was` keeps the ORIGINAL
            # producer, not the previous attachment's.
            if "produced_by_was" in row:
                copy["produced_by_was"] = row.get("produced_by_was")
            else:
                copy["produced_by_was"] = row.get("produced_by")
            copy["note"] = (
                "the answer; it is produced by the compiler's own "
                "runtime routine %s, whose body is attached as the "
                "arch unit %s" % (callee_unit["callee"],
                                  callee_unit["unit"]))
            fresh.append(copy)
            touched = touched + 1
        out["ledger"] = fresh
        if touched == 0:
            return out, ("this caller record has no row named %s"
                         % answer_name)
        return out, ""


# ------------------------------------------------------------------
# reading the recorded list of callers
# ------------------------------------------------------------------

RECORDED_LIST = "out_of_scope_library_calls.json"
SUPERSESSION = "out_of_scope_library_calls_superseded.json"


def recorded_callers(here=None):
    """the 308 units of the recorded list.  The file is READ and never
    written; its verdict is superseded, its list stands."""
    if here is None:
        here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, RECORDED_LIST)
    doc = json.load(open(path))
    return doc


def supersession_note(doc):
    """the NEW file that records the supersession.  The recorded file
    is not edited; this note stands beside it and cites the ruling."""
    return {
        "what_this_is": "the supersession note for "
                        "out_of_scope_library_calls.json.  That file "
                        "is not edited and not deleted; this file "
                        "records that its VERDICT no longer holds "
                        "while its LIST of 308 units stands.",
        "supersedes": RECORDED_LIST,
        "the_verdict_that_no_longer_holds":
            doc.get("what_this_is"),
        "the_ruling_that_supersedes_it":
            "the owner, 2026-09-03: \"if its within the compiler, its not a "
            "library call.  if the compiler is importing something as "
            "a standard feature, also not a library call.\"  A `call` "
            "into the compiler's OWN runtime is followed: the "
            "callee's body is extracted from the archive on this "
            "machine and attached as a further arch unit the caller "
            "references, and the caller's answer row is produced by "
            "{\"kind\": \"runtime_callee\", \"callee\": ...}.",
        "recorded_in":
            "DevComms/log_158_claude_code_task_briefs_round12.md, "
            "TASK 59; and "
            "Planning/node_0_3_research/node_0_3_5_compiler_graph/"
            "node_0_3_5_1_arch_unit/node_0_3_5_1_8_runtime_callee/"
            "CORE_0_3_5_1_8_runtime_callee.md",
        "the_list_stands": {
            "count": doc.get("count"),
            "by_callee": doc.get("by_callee"),
            "by_language": doc.get("by_language"),
            "count_note": doc.get("count_note"),
        },
        "written_by": "runtime_callee.py",
    }
