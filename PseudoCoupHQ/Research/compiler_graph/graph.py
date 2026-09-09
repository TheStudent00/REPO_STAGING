#!/usr/bin/env python3
"""graph.py -- the class the plan tree names.

Plan node: hq.research.compiler_graph.graph
(Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_9_graph/
CORE_0_3_5_9_graph.md). Code carries the node's name: the class is
`Graph`, its attributes are `static_structure`, `dynamic_structure`,
`frontier`, `variant_structure`, its methods are `build`, `diary`,
`query_path`, `coverage`, `super_ops`, `variant_connections` --
exactly the names the CORE's `## design` block states, in that shape.

SUPERSEDES AS RECORDS (not deleted, not edited beyond one header
line each): build_graph.py (lap one, go only), build_graph2.py (lap
two, the cpp generalization), build_graph3.py (lap three, the widened
LLVM SelectionDAG region).

WHAT IS IMPLEMENTED, WHAT IS STUBBED BY DESIGN -- stated here so
nothing is stubbed silently:

  build          IMPLEMENTED. Region rule -> static_structure, for
                 every language whose pack exists below.
  query_path     IMPLEMENTED. Breadth-first walk over
                 static_structure; returns a path or a NAMED
                 frontier saying which unresolved reference stopped
                 the walk.
  coverage       IMPLEMENTED as the join. It reads diary files that
                 task 72 produces; with zero diary files on disk it
                 reports "0 probes" and the whole node set as
                 never-visited, which is the honest state today.
  diary          HALF IMPLEMENTED, and the half is named. The
                 READER (diary file -> dynamic_structure) is here
                 and works. The PRODUCER (inject id-emission into
                 compiler source at node coordinates, rebuild the
                 compiler in Airlock, compile a probe, collect the
                 stream) is NOT here: it is task 72's work, and
                 inject_diary.py is its go-only ancestor. Calling
                 Graph.diary() with no diary directory returns an
                 empty dynamic_structure and says so; it never
                 invents a path.
  super_ops      IMPLEMENTED (task 75). Diaries are read one file at
                 a time and encoded to a compact integer stream on
                 disk; recurring contiguous sub-paths are counted
                 Apriori-style with at most two length levels live,
                 closed against their one-step extensions, and joined
                 to the arch-units the probes produced. IT RUNS IN
                 BOUNDED MEMORY BY RULE: every bound is a parameter,
                 every parameter is written onto the artifact, and the
                 method aborts by name (MemoryCeilingReached) rather
                 than exhausting the machine. See the block above the
                 method for the incident that settled that rule.
  variant_connections
                 IMPLEMENTED (task 87). THE THIRD CONNECTION KIND: per
                 operator traced variant, the nodes that variant's own
                 traces enter and the visited-next edges between them,
                 each marked shared or exclusive to that variant. The
                 variant is identified by MACHINE FORM ONLY (see
                 VARIANT_IDENTITY_STATED). Where a language has a graph
                 and no diaries it returns
                 UNMEASURED_BY_ABSENCE_OF_DIARIES carrying its caller's
                 stated reason, and approximates nothing.
  arch_opcode_nodes
                 IMPLEMENTED (task 95). THE ARCH-OPCODE-NODE: which
                 definition nodes of a compiler's own source produce a
                 machine instruction, marked in FOUR STATES from SOURCE
                 ALONE, with no run of the compiler and no diary. It
                 therefore reaches rust and swift, which this machine
                 cannot instrument. See the ARCH_OPCODE_RULES block above
                 `class Graph` for the states, for where each region's
                 emitter was LOCATED rather than assumed, and for the
                 named frontiers where a hop does not resolve.

LANGUAGE-AGNOSTIC BY CONSTRUCTION, the CORE's rule, realized the way
PCv5's ledgerer realizes it (Tools/ledgerer/ts_to_ur.py,
class LanguagePack): per-language DATA, one universal mapper. Adding
a sixth compiler means writing a pack -- a table of tree-sitter node
type names -- not writing code. The mapper below never names a
language.

"DEFINED IN" VERSUS "DOES", the CORE's rule: dispatch is by FILE
EXTENSION, to the grammar of the language the file is WRITTEN in.
A function about x86 registers that is written in Go is read by the
Go grammar and sits in the Go region.

THE SPELLING BAN (the owner, absolute): no operator token appears in any
key, grouping, pairing, row structure, candidate selection or
comparison scope produced by this file. Node ids are
file-plus-source-coordinate; edge keys are structural relation
names.

A NODE ID IS A MACHINE COORDINATE AND CARRIES NO NAME:
`<file>#<line>#<kind>#<ordinal>`. It was `<file>:<line>:<name>` until
the guard was run over the four graphs and refused three of them --
compilers contain functions whose own names ARE operator tokens
(`new` in rustc, `consume` in swift and llvm, `as` in swift), so an
id built from a name puts a token into every edge's `src` and `dst`,
which is a row structure. The name now lives ONLY in the `label`
field of the node record, which carries `language` and `id` and is
therefore a unit object -- the one place the ban permits a token.
For the same reason a call edge carries no `callee_text`: its file
and line locate the call in the compiler's own source, which is
where the text belongs.

check_no_spelling_keys.py, unmodified, is run over every
graph_<lang>.json this file writes, and its transcript is pasted in
the report.

PINS. Sources are read with `git show <pin>:<path>` from the pinned
repository, NEVER from a working tree (every one of the four trees
sits at a different commit than the pin). Grammar versions are read
at run time from installed package metadata and written into the
output; they are not typed in.
"""

from __future__ import annotations

import argparse
import array
import hashlib
import json
import re
import resource
import subprocess
import sys
import time
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path

from importlib.metadata import version as pkg_version

from tree_sitter import Language, Parser

HERE = Path(__file__).resolve().parent
SOURCES = Path.home() / "Programming" / "Sources"


VARIANT_CONNECTIONS_ARE = (
    "the THIRD connection kind of this graph: per OPERATOR TRACED "
    "VARIANT, the compiler-source nodes that variant's own traces enter "
    "and the visited-next edges between them, each marked shared or "
    "exclusive to that variant. It is not the union over probes -- the "
    "union (Graph.coverage) holds no edges and has no notion of a "
    "variant, so it cannot tell a connection one variant walks apart "
    "from one every variant walks"
)

VARIANT_IDENTITY_STATED = (
    "a digest over four MACHINE-FORM facts read off the unit's own ship "
    "code, in this order: the emitted body bytes, the same body as "
    "read, the entry contract, and the ledger's block / size / type / "
    "produced-by shape. NO OPERATOR TOKEN ENTERS IT. The token is "
    "written onto each member afterwards as a display label on a typed "
    "unit object and is read back by nothing"
)


def machine_form(unit):
    """The four machine-form facts a variant is identified by.

    THE SPELLING BAN. Nothing here reads `operator`, `n`, a probe name
    or any intention. Every field is what the compiler actually emitted
    for this unit, or how that emission was read.
    """
    ledger_shape = []
    for row in (unit.get("ledger") or []):
        produced_by = row.get("produced_by") or {}
        ledger_shape.append([row.get("block"), row.get("size"),
                             row.get("type"), produced_by.get("kind")])
    return {
        "bytes": unit.get("body_bytes"),
        "text": unit.get("body_text"),
        "entry_contract": unit.get("entry_contract"),
        "ledger_shape": ledger_shape,
    }


def machine_form_identity(form):
    """The variant id: a digest of the machine form, and nothing else.

    A digest rather than the form itself because the id is used as a
    dict key, and the ban is absolute about what may sit in a key: a
    machine coordinate or a digest of machine evidence, never a
    spelling."""
    text = json.dumps(form, sort_keys=True, separators=(",", ":"))
    return "var_" + hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def probe_unit_id(stem, default_language=""):
    """A diary file's stem -> the unit id it belongs to.

    Two shapes are on disk and both are the diary producer's, not this
    reader's invention: `<language>__<unit>` in the joint and
    regenerated directories, and a bare `<unit>` in the single-language
    ones, where the language is the directory's."""
    if "__" in stem:
        language, _, rest = stem.partition("__")
        return "%s/%s" % (language, rest)
    return "%s/%s" % (default_language, stem)


def expand_unit_sources(sources):
    """Every path a `--units` argument names, one file at a time.

    A directory expands to its `*.json` files, sorted, so the
    regenerated store's 326 shards are read one after another and none
    of them stays live."""
    out = []
    for source in sources:
        path = Path(source)
        if path.is_dir():
            out.extend(sorted(str(x) for x in path.glob("*.json")))
        elif path.exists():
            out.append(str(path))
        else:
            raise NotYetBuilt("no unit source at %s" % path)
    return out


class NotYetBuilt(Exception):
    """Refuse by name, never silently (AgentMemory, refusal posture)."""


class SpellingKeyRefused(Exception):
    """A stage's OWN output was refused by the unmodified spelling guard.
    Raised by name so the refusal is a measurement, never a silent pass.
    """


class MemoryCeilingReached(Exception):
    """The miner's stated memory bound was reached, so it stops itself.

    Recorded 2026-09-03 (task 75) after the first shape of `super_ops`
    reached 13.2 GB resident, exhausted this machine's swap and had to
    be stopped from outside. A stop by the operating system is not a
    measurement; a refusal by name is."""


# ------------------------------------------------------------- packs ----


@dataclass
class LanguagePack:
    """Per-language DATA, no per-language code.

    Every field is a set or map of tree-sitter node type names, taken
    from that grammar's own node vocabulary. The mapper below reads
    these and nothing else, so a new language is a new pack.
    """

    language: str
    extensions: tuple
    module: str
    # node types that DECLARE a callable unit
    def_types: tuple = ()
    # field names tried, in order, to find a def's name node
    name_fields: tuple = ("name", "declarator")
    # declarator wrappers to descend through before taking the name
    name_descend: tuple = ()
    # node types that declare one parameter
    param_types: tuple = ()
    # node types that declare a local value
    local_types: tuple = ()
    # node type of a call, with the field holding the callee
    call_types: tuple = ()
    call_callee_field: str = "function"
    # node types that are a bare reference to a name
    ref_types: tuple = ()
    # node types of `base.member`, with the field holding the member
    member_types: tuple = ()
    member_field: str = "field"
    # node types of an assignment, with its two sides
    assign_types: tuple = ()
    assign_left_field: str = "left"
    assign_right_field: str = "right"

    _language_object = None

    def grammar_version(self) -> str:
        return pkg_version(self.module.replace("_", "-"))

    def parser(self) -> Parser:
        if self._language_object is None:
            module = __import__(self.module)
            self._language_object = Language(module.language())
        return Parser(self._language_object)


PACK_GO = LanguagePack(
    language="go",
    extensions=(".go",),
    module="tree_sitter_go",
    def_types=("function_declaration", "method_declaration", "func_literal"),
    name_fields=("name",),
    param_types=("parameter_declaration", "variadic_parameter_declaration"),
    local_types=("var_spec", "const_spec", "short_var_declaration"),
    call_types=("call_expression",),
    ref_types=("identifier", "type_identifier", "field_identifier"),
    member_types=("selector_expression",),
    member_field="field",
    assign_types=("assignment_statement", "short_var_declaration"),
)

PACK_CPP = LanguagePack(
    language="cpp",
    extensions=(".cpp", ".cc", ".h", ".hpp"),
    module="tree_sitter_cpp",
    def_types=("function_definition", "lambda_expression"),
    name_fields=("declarator",),
    name_descend=(
        "pointer_declarator",
        "reference_declarator",
        "function_declarator",
    ),
    param_types=("parameter_declaration", "optional_parameter_declaration"),
    local_types=("declaration", "init_declarator"),
    call_types=("call_expression",),
    ref_types=("identifier", "type_identifier", "field_identifier"),
    member_types=("field_expression",),
    member_field="field",
    assign_types=("assignment_expression",),
)

PACK_C = LanguagePack(
    language="c",
    extensions=(".c",),
    module="tree_sitter_c",
    def_types=("function_definition",),
    name_fields=("declarator",),
    name_descend=("pointer_declarator", "function_declarator"),
    param_types=("parameter_declaration",),
    local_types=("declaration", "init_declarator"),
    call_types=("call_expression",),
    ref_types=("identifier", "type_identifier", "field_identifier"),
    member_types=("field_expression",),
    member_field="field",
    assign_types=("assignment_expression",),
)

PACK_RUST = LanguagePack(
    language="rust",
    extensions=(".rs",),
    module="tree_sitter_rust",
    def_types=("function_item", "closure_expression"),
    name_fields=("name",),
    param_types=("parameter", "self_parameter"),
    local_types=("let_declaration", "const_item", "static_item"),
    call_types=("call_expression",),
    ref_types=("identifier", "type_identifier", "field_identifier"),
    member_types=("field_expression",),
    member_field="field",
    assign_types=("assignment_expression",),
)

PACK_SWIFT = LanguagePack(
    language="swift",
    extensions=(".swift",),
    module="tree_sitter_swift",
    def_types=("function_declaration", "lambda_literal"),
    name_fields=("name",),
    param_types=("parameter",),
    local_types=("property_declaration",),
    call_types=("call_expression",),
    ref_types=("simple_identifier", "type_identifier"),
    member_types=("navigation_expression",),
    member_field="suffix",
    assign_types=("assignment",),
)

PACKS = [PACK_GO, PACK_CPP, PACK_C, PACK_RUST, PACK_SWIFT]

PACK_BY_EXTENSION = {}
for _pack in PACKS:
    for _ext in _pack.extensions:
        PACK_BY_EXTENSION[_ext] = _pack

# Data tables are not code and get no grammar. The CORE names them
# separately: ".td/.rules/.ad as data-table nodes".
DATA_TABLE_EXTENSIONS = (".td",)


# ------------------------------------------------------- data tables ----

DEFM_HEAD = re.compile(r"^defm\s+(\w+)\s*:\s*(\w+)\s*<", re.MULTILINE)
MULTICLASS_HEAD = re.compile(r"^multiclass\s+(\w+)\s*<", re.MULTILINE)
SET_PATTERN = re.compile(r"\[\(set[^\]]*\)\]")


def balanced_block(text: str, open_position: int):
    """Index just past the '}' matching the first '{' at or after
    open_position. Returns None rather than guessing when the block
    never closes."""
    start = text.find("{", open_position)
    if start < 0:
        return None
    depth = 0
    cursor = start
    while cursor < len(text):
        character = text[cursor]
        if character == "{":
            depth = depth + 1
        elif character == "}":
            depth = depth - 1
            if depth == 0:
                return cursor + 1
        cursor = cursor + 1
    return None


# ------------------------------------------------------------ regions ---


@dataclass
class Region:
    """One compiler's lowering region: the pinned repository, the pin,
    the directories, and the rule that decides file membership.

    The minimality rule of the super-node's CORE governs what goes in:
    "model what is easy; build only enough to prove which low-level
    operands are which high-level variables". Each region below is the
    lowering path -- where a named argument becomes a machine
    location -- and nothing wider.
    """

    name: str
    repository: Path
    pin: str
    directories: tuple
    keep_extensions: tuple
    skip_suffixes: tuple = ()
    skip_path_contains: tuple = ()
    skip_generated: bool = False
    note: str = ""


REGIONS = {
    "go": Region(
        name="go",
        repository=SOURCES / "golang_src",
        pin="9f1012d9a1aa0831ff44ac9c767e96f9943d13fe",
        directories=(
            "src/cmd/compile/internal/ssagen",
            "src/cmd/compile/internal/abi",
            "src/cmd/compile/internal/amd64",
            "src/cmd/compile/internal/ssa",
        ),
        keep_extensions=(".go", ".rules", ".s"),
        skip_suffixes=("_test.go",),
        skip_path_contains=("/ssa/_gen/", "/ssa/testdata/"),
        skip_generated=True,
        note=(
            "ssa/testdata holds go programs that are TEST INPUT to the "
            "compiler, not compiler logic; they are named out of the region "
            "here. "
            ".rules and .s files are LISTED and then recorded as a named "
            "frontier (no reader dispatched), which is what lap one did "
            "with them too -- the rewrite-rule language and assembly have "
            "no reader on this lap. "
            "ssa/_gen holds the rewrite-rule GENERATOR and its vendored "
            "library. It is compiler tooling that runs before the compiler "
            "is built, never source a probe's compilation walks, so the "
            "minimality rule keeps it out. Lap one excluded it by not "
            "recursing into subdirectories; this rule states the exclusion "
            "rather than inheriting it from a listing accident. "
            "The region rule of lap one (build_graph.py) unchanged, so the "
            "two graphs are comparable: whole ssagen / abi / amd64 packages, "
            "and from ssa the hand-written files only -- the generated "
            "rewrite tables are about twelve megabytes of machine output "
            "and carry no logic a probe's compilation walks as source."
        ),
    ),
    "cpp": Region(
        name="cpp",
        repository=SOURCES / "llvm-project",
        pin="llvmorg-21.1.8",
        directories=(
            "clang/lib/CodeGen",
            "llvm/lib/Target/X86",
        ),
        keep_extensions=(".cpp", ".h", ".td"),
        note=(
            "clang serves BOTH c and cpp: one driver, one CodeGen library, "
            "one x86 backend; the two languages differ in the front end this "
            "region does not contain. So there is no separate graph_c.json, "
            "and this file says so rather than shipping a duplicate. "
            "clang/lib/CodeGen is where a named parameter becomes an LLVM "
            "argument with an ABI classification; llvm/lib/Target/X86 is "
            "where that argument becomes a physical register. The .td files "
            "are read as data tables, not as code."
        ),
    ),
    "rust": Region(
        name="rust",
        repository=SOURCES / "rust",
        pin="7c329d6c76e11ca40c5673818ab0439c1be8962c",
        directories=(
            "compiler/rustc_codegen_ssa",
            "compiler/rustc_codegen_llvm",
            "compiler/rustc_middle/src/mir",
        ),
        keep_extensions=(".rs",),
        note=(
            "PIN FRONTIER, recorded rather than papered over: the corpus was "
            "compiled by rustc 1.96.1 (31fca3adb 2026-06-26), a rustup "
            "toolchain. The rust source checkout on this machine does not "
            "contain commit 31fca3adb; its own head is 7c329d6c, dated "
            "2026-08-03. So this graph is built from a NEARBY rustc source, "
            "not from the exact source that compiled the corpus. Every claim "
            "read off it is bounded by that gap, and a diary joined to it "
            "(task 72) will need the matching source or a restated pin."
        ),
    ),
    "swift": Region(
        name="swift",
        repository=SOURCES / "swift-6.0.3-RELEASE",
        pin="6a862d2eb7128ff1f317b07e8ad1a6da939775f3",
        directories=(
            "lib/SILGen",
            "lib/IRGen",
        ),
        keep_extensions=(".cpp", ".h"),
        note=(
            "SILGen turns a named parameter into a SIL argument; IRGen turns "
            "a SIL argument into an LLVM argument with an explosion schema "
            "and a physical location. The x86 register assignment itself "
            "happens inside LLVM, which is the cpp region -- so the swift "
            "walk is expected to stop at the region boundary, and that stop "
            "is a named frontier, not a failure."
        ),
    ),
}


def is_generated(text: str) -> bool:
    for line in text.splitlines()[:8]:
        if "Code generated" in line and "DO NOT EDIT" in line:
            return True
    return False


# -------------------------------------------------------------- graph ---


# ======================= THE ARCH-OPCODE-NODE, task 95 =====================
#
# CORE 0_3_5_9, the heading "the arch-opcode-node -- a shape this node
# lacks, added 2026-09-05".  the owner, the same day: "is there a way to know
# which parts of the compiler produces arch-opcodes (arch-units)? ... i
# mean just by analyzing the compiler source code. like if the compiler
# produces an arch opcode, its an arch-opcode-node."
#
# FOUR STATES, one per DEFINITION NODE of a region, and the third is a
# CATEGORY rather than a failure:
#
#   1  names_its_opcode      a call site of the region's instruction
#                            emitter passes a CONSTANT.  Which opcodes is
#                            recorded.
#   2  one_static_hop        the opcode argument reads a STATIC TABLE.  In
#                            go that is the generated op table
#                            (ssa/opGen.go's `opcodeTable`, reached through
#                            `Op.Asm()`); in the X86 backend it is a static
#                            helper or a `static const TableEntry[]` in the
#                            same file.  The hop is FOLLOWED and the
#                            opcodes it yields recorded; where it does not
#                            resolve, the site says so with a named reason.
#   3  emits_opcode_dynamic  an emitter whose opcode cannot be named from
#                            source.  NEVER a guess, never an inference.
#   4  emits_nothing         everything else -- the set that may be dropped
#                            without losing opcode-production information.
#
# LANGUAGE-AGNOSTIC BY CONSTRUCTION, the same way `build` is: everything
# per-language is DATA in ARCH_OPCODE_RULES below -- the arch-opcode
# namespace, the pseudo-opcode namespace, the emitter openers and which
# argument of each carries the opcode.  The walk itself never names a
# language.
#
# WHERE EACH REGION'S EMITTER CAME FROM.  Located from source, by lanes
# t95_l2_recon.sh, t95_l3_recon2.sh, t95_l4_recon3.sh and t95_l5_recon4.sh,
# never assumed from go's shape:
#
#   go     -- the machine-form rule "a function of the region declaring a
#             parameter of the ARCH OPCODE TYPE `obj.As`" answers 7
#             functions.  Three TAKE one and so emit: `(*State).Prog`
#             (ssagen/ssa.go:6742), `(*State).Br` (6771) and `opregreg`
#             (amd64/ssa.go:175).  Four RETURN one and so are TABLES, not
#             emitters: `loadByRegWidth`, `storeByRegWidth`,
#             `moveByRegsWidth` and `Op.Asm` -- which is exactly the hop
#             the CORE names.
#   cpp    -- 724 `BuildMI(`, 57 `.setDesc(`, 53 `MCInstBuilder(` and 36
#             `.setOpcode(` sites.  BuildMI and setDesc carry the opcode
#             inside their `get(...)`; the other two carry it first.
#   rust   -- LOCATED AND FOUND TO BE OUTSIDE THE REGION.  The whole rust
#             checkout contains 0 files naming `BuildMI(`, `MCInst`,
#             `MachineInstr` or an X86 instruction namespace: rustc's
#             region emits LLVM IR and LLVM emits the instruction, and
#             LLVM is the cpp region.  Its inline-assembly path carries a
#             template the COMPILED PROGRAM supplies, not one the compiler
#             spells.  Both are named frontiers below, not approximations.
#   swift  -- the same, with ONE measured exception: `llvm::InlineAsm::get`
#             at lib/IRGen/IRGenSIL.cpp:5578 hands over the fixed template
#             `nop`, which the source's own comment calls "not
#             architecture independent".  So swift's emitter is the
#             inline-assembly constructor, and its opcode argument is the
#             template string.
#
# THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
# second violation).  No operator token may appear in ANY key, grouping,
# pairing, row structure, candidate selection, or comparison scope.  An
# ARCH OPCODE (`MOVQ`, `ADDQ`) is MACHINE FORM and is a legitimate key --
# the opcode index pane already keys by it.  An OPERATOR TOKEN is not, and
# none appears here.  Every opcode entry is a TYPED ROW `{"text": "..."}`
# rather than a bare list element, the shape task 93 settled, because an
# arch mnemonic can be a homograph of an operator-inventory word and the
# unmodified guard is right to refuse a bare token in a row-structure
# position.

#: how deep a static hop may follow a callee that returns another callee.
ARCH_HOP_DEPTH = 4

ARCH_OPCODE_RULES = {
    "go": {
        "extensions": (".go",),
        "arch_token": r"\bx86\.A([A-Z][A-Za-z0-9_]*)\b",
        "pseudo_token": r"\bobj\.A([A-Z][A-Za-z0-9_]*)\b",
        "emitter_parameter_type": r"\bobj\.As\b",
        # a DECLARATION is not a call site: the opener names the function,
        # so a declaration is exactly the keyword (and any receiver) sitting
        # immediately before it.
        "declaration_line": r"^\s*func\s+(?:\([^)]*\)\s*)?$",
        "openers": (
            {"label": "Prog", "open": r"\.Prog\s*\(", "argument": 0},
            {"label": "Br", "open": r"\.Br\s*\(", "argument": 0},
            {"label": "opregreg", "open": r"\bopregreg\s*\(", "argument": 1},
        ),
        "generated_tables": (
            {
                "name": "opcodeTable in src/cmd/compile/internal/ssa/opGen.go",
                "call_suffix": ".Asm",
                "file": "src/cmd/compile/internal/ssa/opGen.go",
                "row": r"asm:\s+x86\.A([A-Za-z0-9_]+)",
            },
        ),
        "return_statement": r"\breturn\s+([^\n;]+)",
        "function_definition":
            r"^func\s+(?:\([^)]*\)\s*)?%s\s*\([^\n]*\{",
        "macro_definition": None,
        "table_in_file": None,
        "note": (
            "the emitter is the function that TAKES obj.As; the hop target "
            "is the function that RETURNS one."
        ),
    },
    "cpp": {
        "extensions": (".cpp", ".h"),
        "arch_token": r"\bX86::([A-Z][A-Za-z0-9_]*)\b",
        "pseudo_token": r"\bTargetOpcode::([A-Z][A-Za-z0-9_]*)\b",
        "emitter_parameter_type": None,
        "openers": (
            {"label": "BuildMI", "open": r"\bBuildMI\s*\(",
             "argument": "inner_get"},
            {"label": "setDesc", "open": r"\.setDesc\s*\(",
             "argument": "inner_get"},
            {"label": "MCInstBuilder", "open": r"\bMCInstBuilder\s*\(",
             "argument": 0},
            {"label": "setOpcode", "open": r"\.setOpcode\s*\(",
             "argument": 0},
        ),
        "inner_get": r"(?:\bTII\s*(?:->|\.)\s*get|\bget)\s*\(",
        "generated_tables": (),
        "return_statement": r"\breturn\s+([^\n;]+);",
        "function_definition":
            r"^[A-Za-z_][A-Za-z0-9_:<>,&* \t]*\b%s\s*\([^;{]*\)[^;{]*\{",
        "macro_definition": r"^#define\s+%s\s*\(([^)]*)\)\s*(.*)$",
        "table_in_file": r"static\s+const\s+TableEntry\s+([A-Za-z_]\w*)\s*\[\]",
        #: the target-independent pseudo opcodes every backend shares.  Read
        #: from LLVM's own table at the region's pin, never recognised by
        #: name -- see `_arch_pseudo_names`.
        "pseudo_table_file": "llvm/include/llvm/Support/TargetOpcodes.def",
        "pseudo_table_row":
            r"^HANDLE_TARGET_OPCODE\w*\(\s*([A-Za-z_][A-Za-z0-9_]*)",
        "td_table_frontier": (
            "the_td_files_are_not_a_complete_instruction_table -- the CORE "
            "names LLVM's .td as the static table the hop reads, and the "
            "region does keep all 61 of them, but a plain `def <name>` scan "
            "of them answers 7,227 records and MISSES the instructions X86 "
            "defines through `defm` multiclasses: 100 call sites naming a "
            "real instruction (CMP64rr, ADD32ri, XOR32rr and so on) were "
            "read as `not a .td record` when the table was used that way "
            "(lane t95_l3_recon2.sh step 3). The complete enumeration lives "
            "in X86GenInstrInfo.inc, which TableGen writes at BUILD time and "
            "which is not on this disk. So the arch-opcode namespace X86:: "
            "is what identifies an instruction here, taken from the "
            "argument's POSITION in the call, and the hop reads the "
            "in-region static helpers and `static const TableEntry[]` "
            "arrays instead. The .td shortfall is written down, not worked "
            "around."
        ),
        "note": (
            "an X86:: name that is also one of LLVM's shared pseudo opcodes "
            "is counted as a pseudo, not as a machine instruction; and "
            "X86::EAX-style register names never reach here because the "
            "opcode argument is taken from its POSITION in the call."
        ),
    },
    "rust": {
        "extensions": (".rs",),
        "arch_token": None,
        "pseudo_token": None,
        "emitter_parameter_type": None,
        "openers": (
            {"label": "InlineAsmCall", "open": r"\bInlineAsmCall\s*\(",
             "argument": 0, "argument_is_a_template": True},
            {"label": "LLVMRustInlineAsm",
             "open": r"\bLLVMRustInlineAsm\s*\(", "argument": 1,
             "argument_is_a_template": True},
            {"label": "inline_asm_call", "open": r"\binline_asm_call\s*\(",
             "argument": 1, "argument_is_a_template": True},
        ),
        "generated_tables": (),
        "return_statement": r"\breturn\s+([^\n;]+)",
        "function_definition": r"^\s*(?:pub\s+)?fn\s+%s\s*[(<]",
        "declaration_line": r"^\s*(?:pub(?:\([^)]*\))?\s+)?(?:default\s+)?(?:const\s+)?(?:async\s+)?(?:unsafe\s+)?(?:extern\s+\S+\s+)?fn\s+$",
        "macro_definition": None,
        "table_in_file": None,
        "unmeasured_by_absence_of_an_emitter": (
            "arch_opcode_emitter_outside_the_region -- measured, not "
            "assumed: 0 files of the whole rust checkout name BuildMI(, "
            "MCInst, MachineInstr or an X86 instruction namespace (lane "
            "t95_l3_recon2.sh step 4). rustc's region emits LLVM IR; the "
            "machine instruction is emitted by LLVM, whose source IS the "
            "cpp region, where it is measured. The inline-assembly path "
            "carries a template the COMPILED PROGRAM supplies, which is "
            "not the compiler naming an opcode."
        ),
        "note": "no arch-opcode namespace exists anywhere in this checkout.",
    },
    "swift": {
        "extensions": (".cpp", ".h"),
        "arch_token": None,
        "pseudo_token": None,
        "emitter_parameter_type": None,
        "openers": (
            {"label": "InlineAsm", "open": r"\bllvm::InlineAsm::get\s*\(",
             "argument": 1, "argument_is_a_template": True},
        ),
        "generated_tables": (),
        "return_statement": r"\breturn\s+([^\n;]+);",
        "function_definition":
            r"^[A-Za-z_][A-Za-z0-9_:<>,&* \t]*\b%s\s*\([^;{]*\)[^;{]*\{",
        "macro_definition": None,
        "table_in_file": None,
        "note": (
            "the swift region reaches x86 only through LLVM, which is the "
            "cpp region -- except where it spells an instruction itself in "
            "an inline-assembly template, which is what the opener reads."
        ),
    },
}


def arch_text_row(text):
    """ONE piece of machine-form text -- an opcode, an argument
    expression, the name of a table a hop read -- as a TYPED ROW rather
    than a bare string on a structure field.

    THE SHAPE IS THE RATIFIED ONE (task 93, and the CORE for the four x86
    mnemonics that are homographs of operator-inventory words): a value
    the unmodified spelling guard would otherwise read as a token sitting
    in a row-structure position rides as a VALUE on a row instead.

    MEASURED, not anticipated: the first artifact this pass wrote was
    REFUSED by the unmodified guard at
    `$.call_sites[223].argument` -- go's own emitter is
    `func (s *State) Prog(as obj.As)` and 8 of its call sites hand over
    the parameter, whose name `as` is one of the 91 operator tokens.
    Lane t95_l8_split_and_guard.sh holds that refusal; this row shape is
    the fix, and the pass now refuses its own output the same way.
    """
    return {"text": text}


class Graph:
    """The compiler as a graph: static structure, dynamic structure,
    frontier -- and the four walks over them."""

    def __init__(self, language: str = ""):
        self.language = language
        self._ordinals = {}
        self.static_structure = {"nodes": {}, "edges": []}
        self.dynamic_structure = {}
        self.frontier = []
        self.pins = {}
        self.parse_errors = []
        self._by_file = {}
        self._out_edges = None
        # Per probe, the SUBJECT column of each kept diary line, index
        # for index with dynamic_structure[probe]. The subject is the
        # compiler entry point the event belongs to; without it two
        # goroutines' interleaved events read as one chain. Filled by
        # `diary`; folded in from coverage.py (task 72).
        self.diary_subjects = {}
        # THE THIRD CONNECTION KIND (CORE `## design`). Per operator
        # traced variant, the nodes its own traces enter and the
        # visited-next edges between them, each marked shared or
        # exclusive to that variant. Filled by `variant_connections`.
        self.variant_structure = {}

    # ------------------------------------------------------ primitives --

    def mint(self, file_name, line, kind):
        """A machine coordinate, never a name. See the module header:
        an id built from the compiler's own function name puts an
        operator token into every edge row, which the spelling ban
        forbids and the guard catches."""
        stem = "%s#%s#%s" % (file_name, line, kind)
        ordinal = self._ordinals.get(stem, 0)
        self._ordinals[stem] = ordinal + 1
        return "%s#%d" % (stem, ordinal)

    def add_node(self, node_id, **fields):
        if node_id not in self.static_structure["nodes"]:
            record = {"id": node_id}
            record.update(fields)
            self.static_structure["nodes"][node_id] = record
        return node_id

    def add_edge(self, source, target, relation, **fields):
        if source is None:
            return
        if target is None:
            return
        edge = {"src": source, "dst": target, "rel": relation}
        edge.update(fields)
        self.static_structure["edges"].append(edge)

    def add_frontier(self, kind, file_name, detail, **fields):
        record = {"kind": kind, "file": file_name, "detail": detail}
        record.update(fields)
        self.frontier.append(record)

    # ----------------------------------------------------------- build --

    def build(self, region: Region):
        """(source tree, region rule) -> static_structure.

        One pass reads every file and mints nodes; a second pass
        resolves calls against the whole region's name table, because
        a call may name a function declared in a file read later.
        """
        self.language = region.name
        self.pins = {
            "region": region.name,
            "repository": str(region.repository.name),
            "pin": region.pin,
            "pin_resolved": resolve_pin(region.repository, region.pin),
            "directories": list(region.directories),
            "region_note": region.note,
            "tree_sitter": pkg_version("tree-sitter"),
            "grammars": {},
        }
        universe = {}
        pending_calls = []
        files = list_region_files(region)
        for relative_path in files:
            text = show_file(region.repository, region.pin, relative_path)
            extension = Path(relative_path).suffix
            if region.skip_generated and is_generated(text):
                continue
            if extension in DATA_TABLE_EXTENSIONS:
                self.read_data_table(relative_path, text)
                continue
            pack = PACK_BY_EXTENSION.get(extension)
            if pack is None:
                self.add_frontier(
                    "no_reader_dispatched",
                    relative_path,
                    "extension %r has no grammar and no data-table reader"
                    % extension,
                )
                continue
            self.pins["grammars"][pack.language] = pack.grammar_version()
            self.read_code(pack, relative_path, text, universe, pending_calls)
        self.resolve_calls(universe, pending_calls)
        return self.static_structure

    def read_code(self, pack, relative_path, text, universe, pending_calls):
        """One source file -> def nodes, param nodes, local nodes, and
        the read / write / calls edges inside each def."""
        source = text.encode("utf-8")
        parser = pack.parser()
        tree = parser.parse(source)
        self.record_parse_errors(relative_path, tree.root_node)
        file_id = "%s" % relative_path
        self.add_node(
            file_id,
            kind="file",
            language=pack.language,
            file=relative_path,
        )
        self._by_file.setdefault(relative_path, [])
        for definition in find_definitions(pack, tree.root_node):
            self.read_definition(
                pack, relative_path, source, definition, universe,
                pending_calls, file_id,
            )

    def read_definition(
        self, pack, relative_path, source, definition, universe,
        pending_calls, file_id,
    ):
        name = definition_name(pack, source, definition)
        start_line = definition.start_point[0] + 1
        end_line = definition.end_point[0] + 1
        node_id = self.mint(relative_path, start_line, "def")
        self.add_node(
            node_id,
            kind="def",
            language=pack.language,
            file=relative_path,
            label=name or "",
            start_line=start_line,
            end_line=end_line,
        )
        self.add_edge(file_id, node_id, "contains")
        self._by_file[relative_path].append(node_id)
        if name:
            universe.setdefault(name, []).append(node_id)
            short = name.split("::")[-1]
            if short != name:
                universe.setdefault(short, []).append(node_id)
        local_names = {}
        self.read_slots(
            pack, relative_path, source, definition, node_id, local_names,
        )
        self.read_uses(
            pack, relative_path, source, definition, node_id, local_names,
            pending_calls,
        )

    def read_slots(
        self, pack, relative_path, source, definition, owner_id, local_names,
    ):
        """Params and locals of one def become nodes the def contains."""
        for slot_node, slot_kind in find_slots(pack, definition):
            slot_name = slot_declared_name(pack, source, slot_node)
            if not slot_name:
                continue
            line = slot_node.start_point[0] + 1
            slot_id = self.mint(relative_path, line, slot_kind)
            self.add_node(
                slot_id,
                kind=slot_kind,
                language=pack.language,
                file=relative_path,
                label=slot_name,
                start_line=line,
                owner=owner_id,
            )
            self.add_edge(owner_id, slot_id, "contains")
            local_names.setdefault(slot_name, slot_id)

    def read_uses(
        self, pack, relative_path, source, definition, owner_id, local_names,
        pending_calls,
    ):
        """Every reference inside one def becomes a read edge, a write
        edge, or a call -- or a frontier record naming what it was."""
        write_positions = set()
        for assignment in find_by_type(definition, pack.assign_types):
            left = assignment.child_by_field_name(pack.assign_left_field)
            if left is None:
                continue
            for reference in find_by_type(left, pack.ref_types):
                write_positions.add(reference.id)
        for call in find_by_type(definition, pack.call_types):
            callee = call.child_by_field_name(pack.call_callee_field)
            if callee is None:
                continue
            callee_text = node_text(source, callee)
            pending_calls.append(
                {
                    "from": owner_id,
                    "file": relative_path,
                    "line": call.start_point[0] + 1,
                    "callee_text": callee_text,
                }
            )
            for reference in find_by_type(callee, pack.ref_types):
                write_positions.add(reference.id)
        for reference in find_by_type(definition, pack.ref_types):
            reference_name = node_text(source, reference)
            if not reference_name:
                continue
            target = local_names.get(reference_name)
            if target is None:
                self.add_frontier(
                    "unresolved_reference",
                    relative_path,
                    reference_name,
                    at_line=reference.start_point[0] + 1,
                    from_node=owner_id,
                    reason=(
                        "the name is not a param or local of this def; it is "
                        "a package-level name, an imported name, a type, a "
                        "field of a value whose declaration this pass does "
                        "not follow, or the def's own name"
                    ),
                )
                continue
            if reference.id in write_positions:
                self.add_edge(
                    owner_id, target, "writes",
                    at_line=reference.start_point[0] + 1,
                    evidence="assignment_left_side_in_own_parse",
                )
            else:
                self.add_edge(
                    owner_id, target, "reads",
                    at_line=reference.start_point[0] + 1,
                    evidence="identifier_occurrence_in_own_parse",
                )

    def resolve_calls(self, universe, pending_calls):
        """Second pass: a call resolves against the whole region's name
        table, by full text first, then by trailing member name.

        A NAME THAT NAMES MORE THAN ONE DEF RESOLVES TO NOTHING. It
        becomes an `ambiguous_call` frontier record CARRYING ITS
        CANDIDATE SET, which is the CORE's frontier rule ("where the
        graph cannot follow, it says so by kind, with the candidate set
        where computable"). The alternative -- picking the first def
        that happens to carry the name -- manufactures edges: a call to
        `size()` in one file would land on whatever unrelated def in
        the region is also called `size`, and a path query would then
        walk through a connection that does not exist. That defect was
        measured on this region before this rule was written.
        """
        for call in pending_calls:
            text = call["callee_text"]
            trailing = text.split(".")[-1].split("->")[-1].split("::")[-1]
            candidates = universe.get(text)
            matched_on = "callee_text"
            if not candidates:
                candidates = universe.get(trailing)
                matched_on = "trailing_name"
            if not candidates:
                self.add_frontier(
                    "unresolved_call",
                    call["file"],
                    text,
                    at_line=call["line"],
                    from_node=call["from"],
                    reason=(
                        "no def with this name was read anywhere in the "
                        "region: the callee is outside the region, is "
                        "reached by virtual dispatch, or is a local closure "
                        "this pass does not name"
                    ),
                )
                continue
            distinct = [c for c in dict.fromkeys(candidates)
                        if c != call["from"]]
            if len(distinct) == 1:
                self.add_edge(
                    call["from"], distinct[0], "calls",
                    at_line=call["line"],
                    matched_on=matched_on,
                    evidence="call_node_in_own_parse_resolved_by_unique_name",
                )
                continue
            if not distinct:
                continue
            self.add_frontier(
                "ambiguous_call",
                call["file"],
                text,
                at_line=call["line"],
                from_node=call["from"],
                candidate_count=len(distinct),
                candidates=distinct[:12],
                reason=(
                    "the name matches more than one def in the region, so "
                    "no single edge is evidenced; the candidate set is "
                    "carried instead of a guess"
                ),
            )

    def record_parse_errors(self, relative_path, root):
        stack = [root]
        while stack:
            node = stack.pop()
            if node.type == "ERROR" or node.is_missing:
                self.parse_errors.append(
                    {
                        "file": relative_path,
                        "line": node.start_point[0] + 1,
                        "type": node.type,
                    }
                )
                self.add_frontier(
                    "parse_error",
                    relative_path,
                    "%s at line %d" % (node.type, node.start_point[0] + 1),
                )
                continue
            for child in node.children:
                stack.append(child)

    def read_data_table(self, relative_path, text):
        """A data table is not code. Each row is a node; nothing is
        parsed as a language."""
        spans = {}
        for match in MULTICLASS_HEAD.finditer(text):
            end = balanced_block(text, match.end())
            if end is None:
                self.add_frontier(
                    "unterminated_data_table_block",
                    relative_path,
                    match.group(1),
                )
                continue
            spans[match.group(1)] = (match.start(), end)
        file_id = relative_path
        self.add_node(
            file_id, kind="file", language="tablegen_data",
            file=relative_path,
        )
        for match in DEFM_HEAD.finditer(text):
            row_name = match.group(1)
            table_name = match.group(2)
            line = text.count("\n", 0, match.start()) + 1
            span = spans.get(table_name)
            body = text[span[0]:span[1]] if span else ""
            patterns = SET_PATTERN.findall(body)
            node_id = self.mint(relative_path, line, "data_row")
            self.add_node(
                node_id,
                kind="data_row",
                language="tablegen_data",
                file=relative_path,
                label=row_name,
                table=table_name,
                start_line=line,
                pattern_count=len(patterns),
            )
            self.add_edge(file_id, node_id, "contains")
        self.add_frontier(
            "data_table_backend_not_built",
            relative_path,
            "the generated instruction-selection matcher is produced by "
            "TableGen at build time and is not in the source tree; the rows "
            "read here are the source-level facts available without a build",
        )

    # ------------------------------------------------------ query_path --

    def index_edges(self):
        """Both directions are indexed, because the identity question
        is a CONNECTION question, not a control-flow one. Lap one's own
        acceptance path took its first hop against the arrow (it
        printed `--resolves_to (reversed)-->`); a walk that may only
        move with the arrows cannot leave a parameter node at all,
        since every edge that names a parameter points AT it. Each step
        records which way it went, so nothing is hidden."""
        self._out_edges = {}
        for edge in self.static_structure["edges"]:
            self._out_edges.setdefault(edge["src"], []).append(
                (edge["dst"], edge, "forward")
            )
            self._out_edges.setdefault(edge["dst"], []).append(
                (edge["src"], edge, "reversed")
            )
        return self._out_edges

    def query_path(self, start, goal, steps=None, avoid_kinds=("file",),
                   limit=400000):
        """(node a, node b) -> a path through static_structure, or a
        NAMED frontier saying which unresolved reference stopped the
        walk. Breadth-first, so the path returned is a shortest one.

        `goal` may be a node id or a callable predicate over a node
        record, so the question "where does a parameter reach a
        register assignment" can be asked without knowing the answering
        node's id in advance.

        `steps` is the set of (relation, direction) pairs the walk may
        take. IT IS NOT A CONVENIENCE FILTER; it is what keeps the
        answer meaningful, and leaving it open produces connections
        that are not connections. Two shapes were measured on this
        region and rejected: a walk allowed to take `contains` in
        reverse from a def reaches the def's FILE and then every other
        def in that file, so any two defs in one file are three hops
        apart; a walk allowed to take `calls` in reverse joins two defs
        merely because both call one shared helper. The identity shape
        -- lap one's own -- is: leave the parameter for the def that
        contains it (contains, reversed), then follow calls FORWARD.
        `avoid_kinds` keeps file nodes out of the walk for the same
        reason.
        """
        if self._out_edges is None:
            self.index_edges()
        nodes = self.static_structure["nodes"]
        if start not in nodes:
            return {"found": False, "reason": "start node not in graph",
                    "start": start}
        if callable(goal):
            reached = goal
        else:
            reached = lambda record: record["id"] == goal
        if steps is None:
            steps = (("contains", "reversed"), ("calls", "forward"))
        allowed = set(steps)
        seen = {start: None}
        queue = deque([start])
        visited_count = 0
        while queue:
            current = queue.popleft()
            visited_count = visited_count + 1
            if visited_count > limit:
                break
            if current != start and reached(nodes[current]):
                return {"found": True,
                        "path": self.rebuild_path(seen, current),
                        "visited": visited_count}
            for target, edge, direction in self._out_edges.get(current, []):
                if (edge["rel"], direction) not in allowed:
                    continue
                if target in seen:
                    continue
                if target not in nodes:
                    continue
                if nodes[target].get("kind") in avoid_kinds:
                    continue
                seen[target] = (current, edge, direction)
                queue.append(target)
        return {"found": False,
                "reason": "no path under the allowed steps %s"
                          % (sorted(allowed),),
                "visited": visited_count,
                "frontier_at_boundary": self.frontier_near(seen)}

    def rebuild_path(self, seen, node_id):
        steps = []
        cursor = node_id
        while seen.get(cursor) is not None:
            previous, edge, direction = seen[cursor]
            steps.append({"from": previous, "rel": edge["rel"], "to": cursor,
                          "direction": direction,
                          "at_line": edge.get("at_line")})
            cursor = previous
        steps.reverse()
        return steps

    def frontier_near(self, seen):
        """Frontier honesty: when the walk stops, say WHICH unresolved
        references sat on the boundary it stopped at, by kind."""
        touched = set(seen)
        counts = {}
        examples = {}
        for record in self.frontier:
            if record.get("from_node") not in touched:
                continue
            kind = record["kind"]
            counts[kind] = counts.get(kind, 0) + 1
            examples.setdefault(kind, []).append(
                {"detail": record["detail"], "file": record.get("file"),
                 "at_line": record.get("at_line")}
            )
        return {"by_kind": counts,
                "examples": {k: v[:5] for k, v in examples.items()}}

    # ----------------------------------------------------------- diary --

    def diary(self, diary_directory):
        """diary file -> dynamic_structure.

        THE READER IS HERE; THE PRODUCER IS TASK 72, and task 72's
        output is now on disk. A diary file is one probe's ordered list
        of visited compiler units, one per line, in visit order -- a
        diary, never a tally: the order is the point, and this reader
        preserves it including repeats.

        THE FILE FORMAT, as task 72's injector writes it (literal, one
        line of diaries/go/op_0.txt):

            1\t-\tsrc/.../abiutils.go:12127-13356:method|ABIAnalyzeFuncType|src/.../abiutils.go:353

        Three tab fields: a sequence number, a marker column, and the
        unit record. The unit record's three pipe-fields are the byte
        span, the unit's own name, and -- the one this reader uses --
        the DECLARATION SITE as `file:line`. That last field is the
        join key, because it is the one coordinate both id schemes
        carry: task 72's ids are byte spans, graph.py's ids are
        `file#line#kind#ordinal`, and neither can be rewritten into the
        other. Joining on the declaration coordinate is therefore the
        honest join, and it is exact rather than approximate.

        Lines whose unit record is a marker (`-|subject_enter:NAME|-`)
        are kept separately: they say which compiler entry point the
        probe was in, not which unit it visited.

        With no directory on disk this returns an empty
        dynamic_structure and records a frontier saying so. It never
        substitutes a coverage count for an order.
        """
        directory = Path(diary_directory)
        if not directory.is_dir():
            self.add_frontier(
                "no_diaries_on_disk",
                str(directory),
                "the instrumented build and probe replay that produce diary "
                "files are task 72's work; dynamic_structure is empty, and "
                "no coverage claim may be made from it",
            )
            self.dynamic_structure = {}
            return self.dynamic_structure
        for path in sorted(directory.glob("*.txt")):
            probe = path.stem
            visited = []
            subjects = []
            markers = []
            for line in path.read_text(errors="replace").splitlines():
                record = diary_record(line)
                if record is None:
                    continue
                if record.startswith("-|subject_enter:"):
                    markers.append(record)
                    continue
                key = diary_join_key(record)
                if key is None:
                    self.add_frontier(
                        "diary_record_without_declaration_site",
                        str(path),
                        record,
                        reason="the record carries no `file:line` third "
                               "pipe-field, so it cannot be joined",
                    )
                    continue
                visited.append(key)
                subjects.append(diary_subject(line))
            self.dynamic_structure[probe] = visited
            self.diary_subjects[probe] = subjects
            if markers:
                self.dynamic_structure.setdefault("_markers", {})
        return self.dynamic_structure

    # -------------------------------------------------------- coverage --

    def coverage(self, instrumented=None):
        """static_structure x dynamic_structure -> per node, which
        probes visited it; per probe, its path; the never-visited set.

        The join is on the DECLARATION COORDINATE `file:line`, which
        both id schemes carry (see `diary`). Every number carries its
        population, because the caller writes it into a report -- and
        the population that matters most is the one named
        `visited_keys_outside_the_region`: diary records for compiler
        units this region does not contain are NOT coverage failures,
        they are the region rule showing its own edge.
        """
        nodes = self.static_structure["nodes"]
        by_coordinate = {}
        walkable = []
        for node_id, record in nodes.items():
            if record.get("kind") != "def":
                continue
            walkable.append(node_id)
            coordinate = "%s:%s" % (record.get("file"),
                                    record.get("start_line"))
            by_coordinate.setdefault(coordinate, []).append(node_id)
        visitors = {}
        outside = {}
        probes = 0
        for probe, visited in self.dynamic_structure.items():
            if not isinstance(visited, list):
                continue
            probes = probes + 1
            for key in visited:
                targets = by_coordinate.get(key)
                if targets is None:
                    outside[key] = outside.get(key, 0) + 1
                    continue
                for node_id in targets:
                    bucket = visitors.setdefault(node_id, [])
                    if probe not in bucket:
                        bucket.append(probe)
        # THE INSTRUMENTED POPULATION (folded in from coverage.py, task
        # 72). An entry hook can only sit in a function body an edit was
        # actually placed in. `instrumented` is a list of declaration
        # coordinates `file:line` -- task 72's own target list. Given
        # one, `never_visited` is over THAT population only, and every
        # def outside it is a NAMED FRONTIER, never a never-visited
        # node. Given none, the older behaviour stands and the report
        # says the instrumented population is unknown.
        instrumented_ids = None
        uninstrumented_defs = []
        if instrumented is not None:
            wanted = set(instrumented)
            instrumented_ids = []
            for node_id in walkable:
                record = nodes[node_id]
                coordinate = "%s:%s" % (record.get("file"),
                                        record.get("start_line"))
                if coordinate in wanted:
                    instrumented_ids.append(node_id)
                else:
                    uninstrumented_defs.append(node_id)
        population = instrumented_ids if instrumented_ids is not None \
            else walkable
        never = [i for i in population if i not in visitors]
        never_rows = []
        never_by_file = {}
        for node_id in never:
            record = nodes[node_id]
            file_name = record.get("file")
            never_by_file[file_name] = never_by_file.get(file_name, 0) + 1
            # THE ROW IS A TYPED UNIT OBJECT, and that is the whole
            # reason `language` is on it. `label` carries the compiler
            # function's OWN name, and one of the region's functions is
            # named `consume`, which is also one of the 91 operator
            # tokens the corpus probes. The spelling guard read that
            # label as a spelling on an object it could not tell was a
            # single unit, and refused the artifact (task 81, 2026-09-04,
            # log_190). The ruled remedy for a flagged machine-form
            # value is a typed-object SHAPE, never a role key and never
            # a field whitelist: the row now carries a language field
            # beside its unit id, so it identifies ONE unit and its
            # label is what a label is -- a display name on that unit.
            never_rows.append({
                "id": node_id,
                "language": self.language,
                "file": file_name,
                "start_line": record.get("start_line"),
                "label": record.get("label"),
            })
        never_rows.sort(key=lambda row: (row["file"] or "",
                                         row["start_line"] or 0))
        visited_in_population = [i for i in population if i in visitors]
        return {
            "population_region_nodes": len(nodes),
            "population_defs": len(walkable),
            "population_instrumented":
                len(population) if instrumented is not None else None,
            "population_probes": probes,
            "defs_visited_by_at_least_one_probe": len(visitors),
            "instrumented_visited_by_at_least_one_probe":
                len(visited_in_population),
            "uninstrumented_defs_a_named_frontier":
                len(uninstrumented_defs),
            "never_visited_count": len(never),
            "never_visited": never,
            "never_visited_rows": never_rows,
            "never_visited_by_file": dict(
                sorted(never_by_file.items(), key=lambda row: -row[1])
            ),
            "visited_keys_outside_the_region": len(outside),
            "outside_the_region_by_key": outside,
            "per_node_visitors": visitors,
            "per_probe_path": {
                probe: visited
                for probe, visited in self.dynamic_structure.items()
                if isinstance(visited, list)
            },
        }

    # ------------------------------------------------------- super_ops --

    # ------------------------------ the diary producer's target list --
    # Folded in from coverage.py (task 72) on 2026-09-03, task 75, with
    # task 71's file settled. coverage.py's `class Graph(graph.Graph)`
    # exists only as the superseded record of that lap.

    AUGUST_BODY_KINDS = ("func", "method")

    @classmethod
    def load_august(cls, path):
        """Read a graph written by build_graph3.py (the August lap),
        whose ids are `<file>:<start_byte>-<end_byte>:<kind>`. Kept
        apart from `load` because the two files are different shapes
        and pretending otherwise is how a join goes quietly wrong. It
        is still needed: an entry hook is placed at a BYTE coordinate,
        and this file's own ids record only lines."""
        payload = json.loads(Path(path).read_text())
        instance = cls("go")
        instance.pins = {"graph_form": "august",
                         "written_by": "build_graph3.py",
                         "file": str(path)}
        for record in payload["nodes"]:
            instance.static_structure["nodes"][record["id"]] = record
            instance._by_file.setdefault(record.get("file"), []).append(
                record["id"])
        instance.static_structure["edges"] = payload.get("edges", [])
        instance.frontier = payload.get("frontier", [])
        return instance

    def diary_targets(self):
        """static_structure (August form) -> one injection target per
        function body: the SELECTION half of the diary producer. Every
        body of the region, so that the never-visited set is a
        statement about the region and not about a neighbourhood."""
        targets = []
        for record in self.static_structure["nodes"].values():
            if record.get("kind") not in self.AUGUST_BODY_KINDS:
                continue
            targets.append({
                "id": record["id"],
                "kind": record["kind"],
                "file": record["file"],
                "name": record.get("name") or "anonymous",
                "start_line": record["start_line"],
                "start_byte": record["start_byte"],
                "end_byte": record.get("end_byte"),
            })
        targets.sort(key=lambda item: (item["file"], item["start_line"]))
        return targets

    # ------------------------------------------------------- super_ops --
    #
    # THE MEMORY BOUND IS A SETTLED RULE OF THIS METHOD, recorded after
    # an incident on 2026-09-03 (task 75). The first shape of this miner
    # read all 590 diaries into `dynamic_structure` (10,015,022 event
    # strings) and then held, for every length at once, a dictionary of
    # every run of that length with the list of probes it occurred in.
    # Both parts are unbounded in the corpus: the strings are O(events),
    # and the run dictionaries are O(events) PER LENGTH with no cap on
    # length. The process reached 13.2 GB resident, exhausted the
    # machine's 4 GB of swap and had to be stopped. Nothing about the
    # result was wrong; the shape was.
    #
    # THE BOUND NOW, stated so it can be checked:
    #
    #   1. Diaries are read ONE FILE AT A TIME and never all held. Each
    #      is encoded to a compact array of 4-byte integers in a cache
    #      file on disk. Live cost of this phase: one diary's own stream
    #      plus the coordinate alphabet.
    #   2. The Apriori passes read that cache one probe at a time. At
    #      most TWO length levels are live: the one being counted and
    #      the one being extended. Each level holds ints, not probe
    #      lists; the probes of a candidate are collected in one final
    #      pass, for the surviving candidates only.
    #   3. `max_length` caps the number of passes. `max_runs_per_level`
    #      caps the width of one pass. `memory_ceiling_mb` is checked
    #      after every pass and every 25 probes with
    #      `resource.getrusage`, and the miner ABORTS BY NAME
    #      (`MemoryCeilingReached`) rather than taking the machine down.
    #
    # Every one of those is a PARAMETER and every one is written onto
    # the artifact.

    SUBJECT_NOT_A_COMPILER_ENTRY_POINT = ("-", "main")

    def encode_diaries(self, diary_directory, cache_path,
                       subject="probe_own", collapse_repeats=True,
                       memory_ceiling_mb=6144):
        """Every diary -> one compact array of integer codes, on disk.

        THE SUBJECT PARAMETER, and why it is not optional. One diary
        interleaves several compiler entry points, because the compiler
        runs concurrently (log_175 §2.3). Read by order alone, two
        unrelated chains read as one, and a sub-path mined out of that
        mixture would be an artefact of the scheduler. Three settings:

            "probe_own"  the events whose subject is neither `-` nor
                         `main` -- the compilation of the probe's own
                         expression, which is what a super-op is about
            "main"       the events of the probe file's own `main`
            "all"        every event, subject ignored (kept only so the
                         mixture can be measured, never as a default)

        `collapse_repeats` folds a run of the same coordinate entered
        back to back into one occurrence, so recurrence measures the
        SHAPE of a path and not how many times a loop turned.

        Returns (probes, alphabet, index) where `index` maps a probe to
        (offset, count) in the cache file. Memory here is one diary.
        """
        directory = Path(diary_directory)
        if not directory.is_dir():
            raise NotYetBuilt("no diary directory at %s" % directory)
        alphabet = {}
        index = {}
        probes = []
        offset = 0
        handle = open(cache_path, "wb")
        number = 0
        for path in sorted(directory.glob("*.txt")):
            probe = path.stem
            row = array.array("i")
            previous = -1
            with open(path, "r", errors="replace") as diary_file:
                for line in diary_file:
                    fields = line.rstrip("\n").split("\t")
                    if len(fields) < 3:
                        continue
                    if subject != "all":
                        here = fields[1].strip() or "-"
                        if subject == "main" and here != "main":
                            continue
                        if subject == "probe_own":
                            if here in self.SUBJECT_NOT_A_COMPILER_ENTRY_POINT:
                                continue
                    record = fields[2].strip()
                    if not record or record.startswith("-|subject_enter:"):
                        continue
                    key = diary_join_key(record)
                    if key is None:
                        continue
                    code = alphabet.get(key)
                    if code is None:
                        code = len(alphabet)
                        alphabet[key] = code
                    if collapse_repeats and code == previous:
                        continue
                    previous = code
                    row.append(code)
            row.tofile(handle)
            index[probe] = (offset, len(row))
            offset = offset + len(row)
            probes.append(probe)
            number = number + 1
            if number % 25 == 0:
                self.check_memory(memory_ceiling_mb, "encoding diaries")
        handle.close()
        self.check_memory(memory_ceiling_mb, "encoding diaries")
        return probes, alphabet, index

    @staticmethod
    def check_memory(ceiling_mb, phase):
        """Peak resident set so far, in MB, against the ceiling. Aborts
        BY NAME -- an out-of-memory stop by the operating system is not
        a measurement and takes the machine with it."""
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
        if ceiling_mb and peak > ceiling_mb:
            raise MemoryCeilingReached(
                "peak resident %.0f MB exceeds the stated ceiling of %d MB "
                "during %s; the miner refuses rather than exhausting the "
                "machine" % (peak, ceiling_mb, phase)
            )
        return peak

    @staticmethod
    def read_stream(handle, offset, count):
        row = array.array("i")
        handle.seek(offset * 4)
        if count:
            row.fromfile(handle, count)
        return row

    def super_ops(self, diary_directory=None, arch_units=None,
                  min_length=3, min_support=2, subject="probe_own",
                  collapse_repeats=True, max_length=12,
                  max_runs_per_level=2000000, memory_ceiling_mb=6144,
                  language="go", cache_path=None):
        """Recurring sub-paths of dynamic_structure across probes,
        ranked by recurrence, each joined to the arch-units those probes
        produced. THE detector (the owner, log_081 §5; CORE `## design`).

        A candidate is a CONTIGUOUS run of compiler-source coordinates
        that occurs in the streams of at least `min_support` distinct
        probes. Support is counted in PROBES, never in occurrences: a
        path one probe walks a thousand times has recurred across one
        probe and is not a recurrence across the corpus.

        Only CLOSED candidates are returned: a run is dropped when a
        one-step extension of it has exactly the same probe support,
        because the shorter run then carries no evidence the longer one
        does not.

        THE PARAMETERS ARE ARGUMENTS AND ARE WRITTEN ONTO THE ARTIFACT:
        `min_length`, `min_support`, `subject`, `collapse_repeats`,
        `max_length`, `max_runs_per_level`, `memory_ceiling_mb`.
        Nothing is hidden inside the body. The memory bound is stated
        in the block above this method and enforced, not hoped for.

        THE SPELLING BAN. Every key here is a machine coordinate (the
        `file:line` of the compiler's own source, or a task-71 node
        id). No operator token enters any key, any grouping, or the
        choice of what is compared with what: candidates are grouped by
        the SOURCE NODE IDS they consist of. A compiler function's name
        rides once per node, on `label`, for reading.
        """
        if cache_path is None:
            cache_path = str(Path(diary_directory).parent
                             / ("_streams_%s.i32" % subject))
        started = time.time()
        probes, alphabet, index = self.encode_diaries(
            diary_directory, cache_path, subject=subject,
            collapse_repeats=collapse_repeats,
            memory_ceiling_mb=memory_ceiling_mb)
        if not probes:
            raise NotYetBuilt("no diaries under %s" % diary_directory)
        spelling = {code: key for key, code in alphabet.items()}
        total_events = sum(count for _, count in index.values())
        lengths = [count for _, count in index.values()]

        handle = open(cache_path, "rb")
        levels_width = {}
        closed = []          # (support, length, run) for closed runs
        previous_counts = None
        previous_length = 0
        length = min_length
        while length <= max_length:
            counts = {}
            for number, probe in enumerate(probes):
                offset, count = index[probe]
                row = self.read_stream(handle, offset, count)
                here = set()
                for start in range(0, max(0, len(row) - length + 1)):
                    run = tuple(row[start:start + length])
                    if previous_counts is not None:
                        if run[:-1] not in previous_counts:
                            continue
                        if run[1:] not in previous_counts:
                            continue
                    here.add(run)
                for run in here:
                    counts[run] = counts.get(run, 0) + 1
                if len(counts) > max_runs_per_level:
                    raise MemoryCeilingReached(
                        "runs of length %d exceeded max_runs_per_level "
                        "(%d) -- raise min_support or lower max_length "
                        "rather than letting the pass grow"
                        % (length, max_runs_per_level))
                if number % 25 == 0:
                    self.check_memory(memory_ceiling_mb,
                                      "counting runs of length %d" % length)
            frequent = {run: n for run, n in counts.items()
                        if n >= min_support}
            del counts
            levels_width[str(length)] = len(frequent)
            # CLOSURE, marked between two adjacent levels only, which is
            # exact for contiguous runs: a run is absorbed only by its
            # own one-step extensions.
            if previous_counts is not None:
                absorbed = set()
                for run, support in frequent.items():
                    for half in (run[:-1], run[1:]):
                        if previous_counts.get(half) == support:
                            absorbed.add(half)
                for run, support in previous_counts.items():
                    if run not in absorbed:
                        closed.append((support, previous_length, run))
                del absorbed
            if not frequent:
                previous_counts = None
                break
            previous_counts = frequent
            previous_length = length
            self.check_memory(memory_ceiling_mb,
                              "level %d complete" % length)
            length = length + 1
        if previous_counts:
            for run, support in previous_counts.items():
                closed.append((support, previous_length, run))

        closed.sort(key=lambda row: (-row[0], -row[1]))

        # ONE final pass for the probes of the surviving candidates.
        wanted = {}
        for support, run_length, run in closed:
            wanted.setdefault(run_length, {})[run] = []
        for number, probe in enumerate(probes):
            offset, count = index[probe]
            row = self.read_stream(handle, offset, count)
            for run_length, table in wanted.items():
                seen = set()
                for start in range(0, max(0, len(row) - run_length + 1)):
                    run = tuple(row[start:start + run_length])
                    if run in table and run not in seen:
                        seen.add(run)
                        table[run].append(probe)
            if number % 25 == 0:
                self.check_memory(memory_ceiling_mb,
                                  "collecting the probes of the candidates")
        handle.close()

        nodes = self.static_structure["nodes"]
        by_coordinate = {}
        for node_id, record in nodes.items():
            if record.get("kind") != "def":
                continue
            coordinate = "%s:%s" % (record.get("file"),
                                    record.get("start_line"))
            by_coordinate.setdefault(coordinate, []).append(node_id)

        candidates = []
        for ordinal, (support, run_length, run) in enumerate(closed):
            coordinates = [spelling[code] for code in run]
            node_ids = []
            spans = []
            off_region = []
            for coordinate in coordinates:
                found = by_coordinate.get(coordinate)
                if not found:
                    off_region.append(coordinate)
                    node_ids.append(None)
                    spans.append({"coordinate": coordinate,
                                  "in_the_region_graph": False})
                    continue
                node_id = found[0]
                record = nodes[node_id]
                node_ids.append(node_id)
                spans.append({
                    "coordinate": coordinate,
                    "in_the_region_graph": True,
                    "node_id": node_id,
                    "file": record.get("file"),
                    "start_line": record.get("start_line"),
                    "end_line": record.get("end_line"),
                    "label": record.get("label"),
                })
            walked = wanted[run_length][run]
            candidates.append({
                "candidate_id": "cand_%05d" % ordinal,
                "length": run_length,
                "probe_support": support,
                "source_node_ids": node_ids,
                "source_coordinates": coordinates,
                "source_spans": spans,
                "coordinates_outside_the_region_graph": off_region,
                "probes": walked,
                "arch_unit_ids": ["%s/%s" % (language, probe)
                                  for probe in walked],
            })
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
        return {
            "parameters": {
                "min_length": min_length,
                "min_support": min_support,
                "subject": subject,
                "collapse_repeats": collapse_repeats,
                "max_length": max_length,
                "max_runs_per_level": max_runs_per_level,
                "memory_ceiling_mb": memory_ceiling_mb,
                "support_is_counted_in": "distinct probes",
                "closure": "closed contiguous runs only",
            },
            "populations": {
                "probes": len(probes),
                "distinct_coordinates_in_the_streams": len(alphabet),
                "stream_length_min": min(lengths),
                "stream_length_max": max(lengths),
                "stream_length_total": total_events,
                "frequent_runs_by_length": levels_width,
                "candidates_after_closure": len(candidates),
            },
            "cost": {
                "wall_seconds": round(time.time() - started, 1),
                "peak_resident_mb": round(peak, 1),
                "stream_cache": str(cache_path),
            },
            "candidates": candidates,
        }

    # ------------------------------------------ variant_connections --
    #
    # THE THIRD CONNECTION KIND (CORE `## design`, `variant_structure` /
    # `variant_connections`; the owner, 2026-09-04: a completed compiler graph
    # carries "connections that are structural, dynamic, and are part of
    # each operator traced variant").
    #
    # WHAT IT IS, IN ONE SENTENCE. Per operator traced variant, the
    # compiler-source nodes that variant's own traces enter and the
    # visited-next edges between them, each marked SHARED or EXCLUSIVE
    # to that variant.
    #
    # WHAT IT IS NOT. It is not `coverage`. `coverage` is the UNION over
    # probes: per node, which probes entered it. It has no notion of a
    # variant, it holds no edges at all, and it cannot tell a node that
    # one variant reaches many times apart from a node every variant
    # reaches. The third kind partitions the dynamic edges by variant
    # and names the discriminating ones.
    #
    # THE SPELLING BAN, AND WHY THIS IS THE METHOD WHERE IT IS EASIEST
    # TO BREAK. A "variant of an operator" invites grouping by the
    # operator's token. It is forbidden. The grouping key here is
    # `machine_form_identity` below: a digest over four facts read off
    # the unit's OWN ship code -- the emitted body bytes, the same body
    # as read, the entry contract, and the ledger's block / size / type
    # / produced-by shape. The token is written onto each MEMBER
    # afterwards, as a display label on a typed unit object, and is read
    # back by nothing in this file.
    #
    # THE MEMORY BOUND, STATED BEFORE THE PASS.
    #   * the graph in memory is the FIXED cost and it is measured, not
    #     guessed: 163.6 MB for graph_go.json, 1,043.1 MB for
    #     graph_cpp.json (lane t87_l1);
    #   * unit records are read ONE FILE AT A TIME and only a digest and
    #     a small member record survive each file, so the corpus's
    #     bodies are never all live;
    #   * diaries are streamed by `encode_diaries`, one file at a time,
    #     into an int32 file on disk -- the same streamer the miner uses;
    #   * the live tables are then O(distinct coordinates) and
    #     O(distinct transitions), plus ONE variant's own two sets;
    #     nothing enumerates sub-paths, which is the shape that reached
    #     13.2 GB on 2026-09-03;
    #   * `max_transitions` caps the transition table and
    #     `memory_ceiling_mb` is checked with `check_memory` at every
    #     phase and every 25 probes. Both refuse BY NAME
    #     (`MemoryCeilingReached`). A stop by the operating system is not
    #     a measurement.
    # Every bound is an argument and every argument is written onto the
    # artifact.

    def variant_connections(self, diary_directory=None, unit_sources=None,
                            default_language="", subject="probe_own",
                            collapse_repeats=True, memory_ceiling_mb=6144,
                            max_transitions=8000000, exclusive_examples=8,
                            cache_path=None, unmeasured_reason=None):
        """(diaries, unit records) -> variant_structure.

        `unit_sources` is a list of paths. A path may be a JSON file
        carrying a `units` mapping, or a DIRECTORY of such files (the
        regenerated store's shards); either way they are read one file
        at a time and only the machine form of the probes actually
        diaried is kept.

        With NO diaries on disk this does not approximate anything. It
        returns a payload whose state is
        `UNMEASURED_BY_ABSENCE_OF_DIARIES`, carrying the reason its
        caller passed in `unmeasured_reason` -- and saying that the
        reason is ABSENT when none was passed, rather than inventing
        one.
        """
        started = time.time()
        directory = Path(diary_directory) if diary_directory else None
        stems = []
        if directory is not None and directory.is_dir():
            stems = sorted(path.stem for path in directory.glob("*.txt"))
        parameters = {
            "subject": subject,
            "collapse_repeats": collapse_repeats,
            "memory_ceiling_mb": memory_ceiling_mb,
            "max_transitions": max_transitions,
            "exclusive_examples_per_variant": exclusive_examples,
            "default_language": default_language,
            "variant_identity": VARIANT_IDENTITY_STATED,
            "support_is_counted_in": "distinct operator traced variants",
        }
        if not stems:
            self.add_frontier(
                "third_connection_kind_unmeasured",
                str(directory) if directory else "(no directory given)",
                "there are no diaries for this language, so the "
                "connections belonging to each operator traced variant "
                "are UNMEASURED BY ABSENCE OF MEASUREMENT; they are not "
                "approximated from the static structure",
                reason=unmeasured_reason or "ABSENT -- no reason was "
                                            "supplied by the caller",
            )
            return {
                "what_this_is": VARIANT_CONNECTIONS_ARE,
                "state": "UNMEASURED_BY_ABSENCE_OF_DIARIES",
                "reason": unmeasured_reason or "ABSENT -- no reason was "
                                               "supplied by the caller",
                "parameters": parameters,
                "populations": {
                    "diaries_on_disk": 0,
                    "probes_with_a_machine_form": 0,
                    "operator_traced_variants": 0,
                    "distinct_nodes_entered": 0,
                    "distinct_transitions": 0,
                },
                "census": {},
                "static_backing": {},
                "probes_without_a_machine_form": [],
                "variants": [],
            }

        # ---- 1. the machine form of every diaried probe -------------
        wanted = {}
        for stem in stems:
            wanted[probe_unit_id(stem, default_language)] = stem
        forms = {}
        members = {}
        for path in expand_unit_sources(unit_sources or []):
            payload = json.loads(Path(path).read_text())
            units = payload.get("units")
            if not isinstance(units, dict):
                continue
            for unit_id, unit in units.items():
                if unit_id not in wanted:
                    continue
                if unit_id in forms:
                    continue
                form = machine_form(unit)
                forms[unit_id] = form
                members[unit_id] = {
                    "id": unit_id,
                    "language": unit.get("lang") or default_language,
                    "operator": unit.get("operator"),
                    "population": unit.get("population"),
                    "outcome": unit.get("outcome"),
                }
            del payload
            del units
            self.check_memory(memory_ceiling_mb, "reading unit records")
        missing = []
        for unit_id, stem in sorted(wanted.items()):
            if unit_id in forms:
                continue
            missing.append({"id": unit_id,
                            "language": unit_id.split("/")[0],
                            "diary": stem})
            self.add_frontier(
                "probe_without_a_machine_form",
                str(directory),
                "this probe has a diary but no arch-unit record on disk, "
                "so no machine-form identity can be derived for it -- and "
                "the operator's token is the one thing that may never be "
                "used instead",
                unit=unit_id,
            )
        by_probe_variant = {}
        variant_members = {}
        for unit_id, form in forms.items():
            variant_id = machine_form_identity(form)
            by_probe_variant[wanted[unit_id]] = variant_id
            bucket = variant_members.setdefault(variant_id,
                                                {"form": form, "members": []})
            bucket["members"].append(members[unit_id])
        self.check_memory(memory_ceiling_mb, "grouping probes into variants")

        # ---- 2. the diaries, streamed --------------------------------
        if cache_path is None:
            cache_path = str(Path(diary_directory).parent
                             / ("_variant_streams_%s.i32" % subject))
        probes, alphabet, index = self.encode_diaries(
            diary_directory, cache_path, subject=subject,
            collapse_repeats=collapse_repeats,
            memory_ceiling_mb=memory_ceiling_mb)
        spelling = {code: key for key, code in alphabet.items()}
        handle = open(cache_path, "rb")

        # ---- 3. attribute every node and every transition ------------
        by_variant_probes = {}
        for probe in probes:
            variant_id = by_probe_variant.get(probe)
            if variant_id is None:
                continue
            by_variant_probes.setdefault(variant_id, []).append(probe)
        node_owner = {}
        edge_owner = {}
        counted = 0
        for variant_id in sorted(by_variant_probes):
            nodes_here, edges_here = self._variant_sets(
                handle, index, by_variant_probes[variant_id])
            for code in nodes_here:
                row = node_owner.get(code)
                if row is None:
                    node_owner[code] = [1, variant_id]
                else:
                    row[0] = row[0] + 1
            for pair in edges_here:
                row = edge_owner.get(pair)
                if row is None:
                    edge_owner[pair] = [1, variant_id]
                else:
                    row[0] = row[0] + 1
            if len(edge_owner) > max_transitions:
                handle.close()
                raise MemoryCeilingReached(
                    "the transition table passed max_transitions (%d) at "
                    "variant %s -- this method refuses rather than growing "
                    "an unbounded table" % (max_transitions, variant_id))
            counted = counted + 1
            if counted % 25 == 0:
                self.check_memory(memory_ceiling_mb,
                                  "attributing transitions to variants")
        self.check_memory(memory_ceiling_mb, "attribution complete")

        # ---- 4. the static structure, for the join and the spans -----
        nodes = self.static_structure["nodes"]
        by_coordinate = {}
        for node_id, record in nodes.items():
            if record.get("kind") != "def":
                continue
            coordinate = "%s:%s" % (record.get("file"),
                                    record.get("start_line"))
            by_coordinate.setdefault(coordinate, []).append(node_id)
        static_calls = set()
        coordinate_of = {}
        for node_id, record in nodes.items():
            coordinate_of[node_id] = "%s:%s" % (record.get("file"),
                                                record.get("start_line"))
        for edge in self.static_structure["edges"]:
            if edge.get("rel") != "calls":
                continue
            source = coordinate_of.get(edge.get("src"))
            target = coordinate_of.get(edge.get("dst"))
            if source is None or target is None:
                continue
            static_calls.add((source, target))
        del coordinate_of
        self.check_memory(memory_ceiling_mb, "indexing the static structure")

        def span(code):
            coordinate = spelling[code]
            found = by_coordinate.get(coordinate)
            if not found:
                # A TYPED UNIT OBJECT even when the coordinate is outside
                # the region graph: `label` is a compiler function's own
                # name and one of the region's functions is named the
                # same as one of the 91 operator tokens (task 81,
                # log_190 section 3.5). The ruled remedy for a flagged
                # machine-form value is a typed-object SHAPE -- never a
                # role key, never a field whitelist.
                return {"id": coordinate,
                        "language": self.language,
                        "coordinate": coordinate,
                        "in_the_region_graph": False,
                        "label": None}
            node_id = found[0]
            record = nodes[node_id]
            return {"id": node_id,
                    "language": self.language,
                    "coordinate": coordinate,
                    "in_the_region_graph": True,
                    "file": record.get("file"),
                    "start_line": record.get("start_line"),
                    "end_line": record.get("end_line"),
                    "label": record.get("label")}

        # ---- 5. per variant, its own connections ---------------------
        rows = []
        counted = 0
        for variant_id in sorted(by_variant_probes):
            probe_list = by_variant_probes[variant_id]
            nodes_here, edges_here = self._variant_sets(
                handle, index, probe_list)
            exclusive_nodes = [c for c in nodes_here
                               if node_owner[c][0] == 1]
            exclusive_edges = [e for e in edges_here
                               if edge_owner[e][0] == 1]
            backed = 0
            for source, target in edges_here:
                if (spelling[source], spelling[target]) in static_calls:
                    backed = backed + 1
            bucket = variant_members[variant_id]
            languages = sorted({m["language"] for m in bucket["members"]
                                if m.get("language")})
            populations = sorted({m["population"] for m in bucket["members"]
                                  if m.get("population")})
            outcomes = {}
            for member in bucket["members"]:
                key = member.get("outcome") or "(none recorded)"
                outcomes[key] = outcomes.get(key, 0) + 1
            examples = []
            for source, target in sorted(exclusive_edges)[:exclusive_examples]:
                examples.append({"from": span(source), "to": span(target),
                                 "backed_by_a_static_call_edge":
                                     (spelling[source], spelling[target])
                                     in static_calls})
            rows.append({
                "variant_id": variant_id,
                "member_count": len(bucket["members"]),
                "languages": languages,
                "populations": populations,
                "outcomes": outcomes,
                "machine_form": bucket["form"],
                "members": sorted(bucket["members"], key=lambda m: m["id"]),
                "probes_with_a_diary": len(probe_list),
                "nodes_entered": len(nodes_here),
                "nodes_exclusive_to_this_variant": len(exclusive_nodes),
                "transitions": len(edges_here),
                "transitions_exclusive_to_this_variant": len(exclusive_edges),
                "transitions_backed_by_a_static_call_edge": backed,
                "exclusive_transition_examples": examples,
            })
            counted = counted + 1
            if counted % 25 == 0:
                self.check_memory(memory_ceiling_mb,
                                  "building the variant rows")
        handle.close()
        rows.sort(key=lambda row: (-row["transitions_exclusive_to_this_variant"],
                                   -row["member_count"], row["variant_id"]))

        # ---- 6. the census: THE ANSWER THE UNION CANNOT GIVE ---------
        def histogram(owner):
            # `walked_by_every_variant` OVERLAPS the band above it and is
            # counted separately on purpose: the four bands partition the
            # population, and the fifth number is the tail of the last
            # band called out by name. The rows must never be added up,
            # and the artifact says so beside them.
            out = {"walked_by_exactly_one_variant": 0,
                   "walked_by_2_to_10_variants": 0,
                   "walked_by_11_to_100_variants": 0,
                   "walked_by_more_than_100_variants": 0,
                   "walked_by_every_variant": 0}
            total = len(by_variant_probes)
            for row in owner.values():
                n = row[0]
                if n == total:
                    out["walked_by_every_variant"] += 1
                if n == 1:
                    out["walked_by_exactly_one_variant"] += 1
                elif n <= 10:
                    out["walked_by_2_to_10_variants"] += 1
                elif n <= 100:
                    out["walked_by_11_to_100_variants"] += 1
                else:
                    out["walked_by_more_than_100_variants"] += 1
            return out

        backed_total = 0
        for source, target in edge_owner:
            if (spelling[source], spelling[target]) in static_calls:
                backed_total = backed_total + 1
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
        self.variant_structure = {
            "what_this_is": VARIANT_CONNECTIONS_ARE,
            "state": "MEASURED",
            "parameters": parameters,
            "populations": {
                "diaries_on_disk": len(stems),
                "probes_with_a_machine_form": len(forms),
                "probes_without_a_machine_form": len(missing),
                "probes_with_a_stream": len(probes),
                "probes_placed_in_a_variant": sum(
                    len(v) for v in by_variant_probes.values()),
                "operator_traced_variants": len(by_variant_probes),
                "distinct_nodes_entered": len(node_owner),
                "distinct_transitions": len(edge_owner),
                "distinct_coordinates_in_the_streams": len(alphabet),
            },
            "census": {
                "how_to_read_this": (
                    "the first four bands PARTITION the population; "
                    "`walked_by_every_variant` is the tail of the last "
                    "band named separately and OVERLAPS it. Do not add "
                    "the five numbers"
                ),
                "nodes": histogram(node_owner),
                "transitions": histogram(edge_owner),
            },
            "static_backing": {
                "static_call_edges_between_defs": len(static_calls),
                "transitions_backed_by_a_static_call_edge": backed_total,
                "transitions_with_no_static_call_edge":
                    len(edge_owner) - backed_total,
                "what_an_unbacked_transition_is":
                    "two compiler bodies entered one after the other with "
                    "no resolved call edge between them in the static "
                    "structure: either the region rule's own edge (the "
                    "caller is outside the region), or an unresolved call "
                    "already in this graph's frontier",
            },
            "probes_without_a_machine_form": missing,
            "cost": {
                "wall_seconds": round(time.time() - started, 1),
                "peak_resident_mb": round(peak, 1),
                "stream_cache": str(cache_path),
            },
            "variants": rows,
        }
        return self.variant_structure

    def _variant_sets(self, handle, index, probe_list):
        """The nodes and the visited-next transitions ONE variant's own
        traces contribute. Live memory here is one variant's two sets
        plus one probe's stream -- never the corpus."""
        nodes_here = set()
        edges_here = set()
        for probe in probe_list:
            offset, count = index[probe]
            row = self.read_stream(handle, offset, count)
            previous = None
            for code in row:
                nodes_here.add(code)
                if previous is not None:
                    edges_here.add((previous, code))
                previous = code
        return nodes_here, edges_here

    # ------------------------------------------- the arch-opcode-node --
    #
    # See the ARCH_OPCODE_RULES block above the class for what the four
    # states are, where each region's emitter was located, and why an
    # opcode is a legitimate key while an operator token is not.

    @staticmethod
    def _arch_balanced(text, open_at):
        """text[open_at] is '('; answer (inside, index of its ')')."""
        depth, j = 0, open_at
        while j < len(text):
            if text[j] == "(":
                depth += 1
            elif text[j] == ")":
                depth -= 1
                if depth == 0:
                    return text[open_at + 1:j], j
            j += 1
        return None, len(text)

    @staticmethod
    def _arch_split(body):
        """the call's arguments, split at depth zero."""
        out, depth, last = [], 0, 0
        for k, ch in enumerate(body):
            if ch in "([{":
                depth += 1
            elif ch in ")]}":
                depth -= 1
            elif ch == "," and depth == 0:
                out.append(body[last:k])
                last = k + 1
        out.append(body[last:])
        return [one.strip() for one in out]

    @staticmethod
    def _arch_branches(text):
        """A conditional between two named constants still NAMES its
        opcodes, so the grader sees the branches rather than the whole
        expression. `A ? X86::PUSH64r : X86::PUSH32r` answers the two
        constants; the condition `A` is not a value the instruction can
        take and is dropped."""
        text = " ".join(text.split())
        depth = 0
        for k, ch in enumerate(text):
            if ch in "([{":
                depth += 1
            elif ch in ")]}":
                depth -= 1
            elif ch == "?" and depth == 0:
                rest = text[k + 1:]
                depth2 = 0
                for j, ch2 in enumerate(rest):
                    if ch2 in "([{":
                        depth2 += 1
                    elif ch2 in ")]}":
                        depth2 -= 1
                    elif ch2 == ":" and depth2 == 0 and \
                            rest[j:j + 2] != "::" and \
                            (j == 0 or rest[j - 1] != ":"):
                        out = []
                        for part in (rest[:j], rest[j + 1:]):
                            out.extend(Graph._arch_branches(part))
                        return out
                break
        return [text.strip()]

    def _arch_read_region(self, region, rules):
        """every source file of the region, read FROM THE PIN."""
        texts = {}
        for relative in list_region_files(region):
            if not relative.endswith(rules["extensions"]):
                continue
            texts[relative] = show_file(region.repository, region.pin,
                                        relative)
        return texts

    def _arch_pseudo_names(self, region, rules):
        """LLVM's shared pseudo opcodes, READ from the toolchain's own
        table at the region's pin. Nothing here recognises a name."""
        path = rules.get("pseudo_table_file")
        if not path:
            return set(), None
        try:
            text = show_file(region.repository, region.pin, path)
        except Exception:
            return set(), "%s ABSENT at the pin" % path
        return set(re.findall(rules["pseudo_table_row"], text, re.M)), path

    def _arch_hop(self, name, argument_text, region, rules, texts, pseudo,
                  depth, trail):
        """ONE STATIC HOP, memoised. A region has 269 files and a hop
        scans all of them, so the same callee is followed once."""
        cached = getattr(self, "_arch_hop_cache", None)
        if cached is None:
            cached = self._arch_hop_cache = {}
        key = (name, argument_text, tuple(trail))
        if key not in cached:
            cached[key] = self._arch_hop_uncached(
                name, argument_text, region, rules, texts, pseudo, depth,
                trail)
        return cached[key]

    def _arch_hop_uncached(self, name, argument_text, region, rules, texts,
                           pseudo, depth, trail):
        """Follow `name` into the table it reads.

        Answers (opcodes, pseudo_opcodes, resolved, reason, hop_name).
        A hop that does not resolve says WHY, per site, and never guesses.
        """
        if depth > ARCH_HOP_DEPTH:
            return set(), set(), False, "hop_deeper_than_%d" % ARCH_HOP_DEPTH, name
        if name in trail:
            return set(), set(), False, "hop_returns_to_itself", name
        trail = trail + [name]
        arch_re = rules.get("arch_token")

        # (a) a GENERATED TABLE the region rule names -- go's op table.
        for table in rules.get("generated_tables", ()):
            if name.endswith(table["call_suffix"]):
                text = show_file(region.repository, region.pin, table["file"])
                found = set(re.findall(table["row"], text))
                return (found, set(), bool(found),
                        "" if found else "generated_table_yielded_nothing",
                        table["name"])

        bare = name.split("::")[-1].split(".")[-1].split(">")[-1]
        if not re.fullmatch(r"[A-Za-z_]\w*", bare):
            return set(), set(), False, "callee_is_not_a_plain_name", name

        # (b) a MACRO.
        pattern = rules.get("macro_definition")
        if pattern:
            for relative, text in texts.items():
                m = re.search(pattern % re.escape(bare), text, re.M)
                if not m:
                    continue
                parameter, replacement = m.group(1).strip(), m.group(2)
                if "##" in replacement:
                    # One branch pastes a suffix onto the parameter. The
                    # pasted name CANNOT BE READ as a constant from source,
                    # so it is not recorded -- "never infer an opcode you
                    # cannot read". The pass-through branch is literal and
                    # is resolved from the call's own argument.
                    passed = re.findall(arch_re, argument_text) if arch_re \
                        else []
                    return (set(passed), set(), bool(passed),
                            "token_pasting_suffix_not_readable_from_source",
                            "%s in %s" % (bare, relative))
                inner = replacement.replace(parameter, argument_text) \
                    if parameter else replacement
                found = set(re.findall(arch_re, inner)) if arch_re else set()
                return (found, set(), bool(found),
                        "" if found else "macro_named_no_constant",
                        "%s in %s" % (bare, relative))

        # (c) a FUNCTION of the region: grade every one of its returns.
        definition = rules.get("function_definition")
        for relative, text in texts.items():
            m = re.search(definition % re.escape(bare), text, re.M)
            if not m:
                continue
            brace = text.find("{", m.start())
            end = balanced_block(text, m.start())
            if end is None or brace < 0:
                continue
            body = text[brace:end]
            opcodes, pseudos, unresolved = set(), set(), []
            returns = re.findall(rules["return_statement"], body)
            if not returns:
                return (set(), set(), False, "callee_body_has_no_return",
                        "%s in %s" % (bare, relative))
            for expression in returns:
                sub_ops, sub_pseudo, sub_state, sub_reasons, _ = \
                    self._arch_grade(expression, region, rules, texts,
                                     pseudo, depth + 1, trail)
                opcodes |= sub_ops
                pseudos |= sub_pseudo
                if sub_state == "emits_opcode_dynamic":
                    # the return reads a static array declared beside it --
                    # the CORE's "the argument reads a static table".
                    table_pattern = rules.get("table_in_file")
                    resolved_here = False
                    if table_pattern and arch_re:
                        for table_name in re.findall(table_pattern, text):
                            if table_name in body:
                                block = text[text.index(table_name):]
                                block = block[:block.find("};") + 2]
                                found = set(re.findall(arch_re, block))
                                if found:
                                    opcodes |= found
                                    resolved_here = True
                    if not resolved_here:
                        unresolved.extend(sub_reasons or
                                          ["return_is_not_a_named_constant"])
            return (opcodes, pseudos, not unresolved and bool(opcodes),
                    "; ".join(sorted(set(unresolved))),
                    "%s in %s" % (bare, relative))
        return (set(), set(), False, "callee_not_declared_inside_the_region",
                name)

    def _arch_grade(self, argument_text, region, rules, texts, pseudo,
                    depth=0, trail=()):
        """ONE opcode argument -> (arch opcodes, pseudo opcodes, state,
        reasons, hops). The state is one of the CORE's first three."""
        arch_re = rules.get("arch_token")
        pseudo_re = rules.get("pseudo_token")
        opcodes, pseudos, reasons, hops = set(), set(), [], []
        hopped = False
        unnamed = 0
        for branch in self._arch_branches(argument_text):
            if not branch:
                continue
            if arch_re:
                exact = re.fullmatch(arch_re.replace(r"\b", ""), branch)
                if exact:
                    name = exact.group(1)
                    if name in pseudo:
                        pseudos.add(name)
                    else:
                        opcodes.add(name)
                    continue
            if pseudo_re:
                exact = re.fullmatch(pseudo_re.replace(r"\b", ""), branch)
                if exact:
                    pseudos.add(exact.group(1))
                    continue
            call = re.match(r"^([A-Za-z_][A-Za-z0-9_:.>\[\]()-]*?)\s*\(",
                            branch)
            if call:
                inside, _ = self._arch_balanced(branch, branch.index("("))
                got, got_pseudo, ok, why, hop_name = self._arch_hop(
                    call.group(1), inside or "", region, rules, texts,
                    pseudo, depth + 1, list(trail))
                opcodes |= got
                pseudos |= got_pseudo
                hops.append(hop_name)
                if ok:
                    hopped = True
                    if why:
                        reasons.append(why)
                else:
                    unnamed += 1
                    reasons.append(why or "hop_did_not_resolve")
                continue
            unnamed += 1
            reasons.append("argument_is_not_a_named_constant")
        if unnamed:
            state = "emits_opcode_dynamic"
        elif hopped:
            state = "one_static_hop"
        elif opcodes or pseudos:
            state = "names_its_opcode"
        else:
            state = "emits_opcode_dynamic"
            reasons.append("argument_named_nothing")
        return opcodes, pseudos, state, reasons, hops

    def _arch_template_grade(self, argument_text):
        """An inline-assembly TEMPLATE is the opcode argument of a
        compiler that has no instruction namespace of its own. A string
        literal the COMPILER spells names its opcodes; an empty literal
        emits no instruction at all; anything else is dynamic."""
        text = argument_text.strip()
        literal = re.fullmatch(r'"((?:[^"\\]|\\.)*)"', text)
        if literal is None:
            return set(), "emits_opcode_dynamic", \
                ["template_is_not_a_string_literal_in_this_region"]
        body = literal.group(1)
        words = re.findall(r"(?:^|[;\n]|\\n|\\t)\s*([A-Za-z][A-Za-z0-9_.]*)",
                           body)
        if not body.strip():
            return set(), "emits_nothing", \
                ["empty_template_emits_no_instruction"]
        if not words:
            return set(), "emits_opcode_dynamic", \
                ["template_names_no_mnemonic"]
        return set(words), "names_its_opcode", []

    def arch_opcode_nodes(self, region=None, out_path=None,
                          memory_ceiling_mb=6144):
        """(compiler source at the region pin) x static_structure ->
        per DEFINITION NODE one of four states, the inverse index from
        each arch opcode to the definitions that emit it, and the
        emits-nothing set.

        STATIC ONLY. The compiler is never run and no diary is read, which
        is the whole point: it reaches the compilers this machine cannot
        instrument.
        """
        started = time.time()
        language = self.language or self.pins.get("region", "")
        if region is None:
            region = REGIONS[language]
        rules = ARCH_OPCODE_RULES[language]
        pseudo, pseudo_source = self._arch_pseudo_names(region, rules)
        texts = self._arch_read_region(region, rules)
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
        if peak > memory_ceiling_mb:
            raise MemoryCeilingReached(
                "arch_opcode_nodes reached %.1f MB reading the region, "
                "over the stated ceiling of %d MB" % (peak, memory_ceiling_mb)
            )

        # --- where the definitions are, so a call site finds its owner ---
        spans = {}
        defs_by_file = {}
        for node_id, record in self.static_structure["nodes"].items():
            if record.get("kind") != "def":
                continue
            defs_by_file.setdefault(record.get("file"), []).append(
                (record.get("start_line") or 0,
                 record.get("end_line") or 0, node_id)
            )
            spans[node_id] = record
        for rows in defs_by_file.values():
            rows.sort()

        def owner(relative, line):
            best = None
            for start, end, node_id in defs_by_file.get(relative, ()):
                if start <= line <= end:
                    if best is None or start >= best[0]:
                        best = (start, node_id)
            return best[1] if best else None

        # --- the emitter census, so an ABSENT opener is measured -------
        census = {}
        for opener in rules["openers"]:
            census[opener["label"]] = 0
        emitter_declarations = []
        parameter_type = rules.get("emitter_parameter_type")
        if parameter_type:
            # THE MACHINE-FORM RULE that separates an emitter from a table,
            # and it is read off the declaration rather than off a name: a
            # function that TAKES the arch opcode type emits an instruction
            # with it; one that RETURNS the type is a table the hop reads.
            for relative, text in texts.items():
                for n, line in enumerate(text.splitlines(), 1):
                    if not re.search(r"^func .*" + parameter_type, line):
                        continue
                    after = line[line.index("func") + 4:]
                    if after.lstrip().startswith("("):
                        # a method: skip the receiver's own parentheses.
                        receiver_at = after.index("(")
                        _, closed = self._arch_balanced(after, receiver_at)
                        after = after[closed + 1:]
                    parameters = ""
                    if "(" in after:
                        parameters, closed = self._arch_balanced(
                            after, after.index("("))
                        returns = after[closed + 1:]
                    else:
                        returns = after
                    takes = bool(re.search(parameter_type, parameters or ""))
                    emitter_declarations.append({
                        "file": relative, "line": n,
                        "language": language,
                        "declaration": line.strip(),
                        "role": ("takes the arch opcode type -- an EMITTER"
                                 if takes else
                                 "returns the arch opcode type -- a TABLE"),
                        "returns": returns.strip().rstrip("{").strip(),
                    })

        # --- every call site of every emitter opener -------------------
        sites = []
        declarations_skipped = {}
        for relative, text in sorted(texts.items()):

            def line_of(position, _text=text):
                return _text.count("\n", 0, position) + 1

            declaration_line = rules.get("declaration_line")
            for opener in rules["openers"]:
                for m in re.finditer(opener["open"], text):
                    open_at = text.find("(", m.start())
                    if open_at < 0:
                        continue
                    # A DECLARATION IS NOT A CALL SITE. `func opregreg(s
                    # *ssagen.State, op obj.As, ...)` and `fn
                    # inline_asm_call(&mut self, asm: &str, ...)` both match
                    # the opener; grading either would report the
                    # PARAMETER as a dynamic opcode and invent an emitter
                    # that emits nothing. Measured on the first run of this
                    # pass: one such site in go and one in rust.
                    line_start = text.rfind("\n", 0, m.start()) + 1
                    if declaration_line and re.match(
                            declaration_line, text[line_start:m.start()]):
                        declarations_skipped.setdefault(
                            opener["label"], []).append(
                                "%s:%d" % (relative, line_of(m.start())))
                        continue
                    body, _ = self._arch_balanced(text, open_at)
                    if body is None:
                        continue
                    census[opener["label"]] += 1
                    argument, why = None, ""
                    if opener["argument"] == "inner_get":
                        g = re.search(rules["inner_get"], body)
                        if g is None:
                            why = "the_call_carries_no_instruction_" \
                                  "descriptor_argument"
                        else:
                            inner_at = body.index("(", g.start())
                            argument, _ = self._arch_balanced(body, inner_at)
                    else:
                        parts = self._arch_split(body)
                        index = opener["argument"]
                        if index < len(parts):
                            argument = parts[index]
                        else:
                            why = "the_call_has_no_argument_in_the_opcode_" \
                                  "position"
                    site = {
                        "language": language,
                        "file": relative,
                        "line": line_of(m.start()),
                        "emitter": opener["label"],
                        # A TYPED ROW, not a bare string: an argument
                        # expression can BE an operator-inventory word (go
                        # hands over the parameter named `as`), and the
                        # unmodified guard is right to refuse one in a
                        # row-structure position.
                        "argument": arch_text_row(
                            " ".join((argument or "").split())[:160]),
                    }
                    if argument is None:
                        site["state"] = "emits_opcode_dynamic"
                        site["reasons"] = [why]
                        site["opcodes"] = []
                        site["pseudo_opcodes"] = []
                        site["hops"] = []
                    elif opener.get("argument_is_a_template"):
                        found, state, reasons = \
                            self._arch_template_grade(argument)
                        site["state"] = state
                        site["reasons"] = reasons
                        site["opcodes"] = [arch_text_row(o)
                                           for o in sorted(found)]
                        site["pseudo_opcodes"] = []
                        site["hops"] = []
                    else:
                        found, found_pseudo, state, reasons, hops = \
                            self._arch_grade(argument, region, rules, texts,
                                             pseudo)
                        site["state"] = state
                        site["reasons"] = sorted(set(reasons))
                        site["opcodes"] = [arch_text_row(o)
                                           for o in sorted(found)]
                        site["pseudo_opcodes"] = [arch_text_row(o)
                                                  for o in sorted(found_pseudo)]
                        site["hops"] = [arch_text_row(one)
                                        for one in sorted(set(hops))]
                    site["definition"] = owner(relative, site["line"])
                    sites.append(site)
                    peak = max(peak, resource.getrusage(
                        resource.RUSAGE_SELF).ru_maxrss / 1024.0)
                    if peak > memory_ceiling_mb:
                        raise MemoryCeilingReached(
                            "arch_opcode_nodes reached %.1f MB, over the "
                            "stated ceiling of %d MB"
                            % (peak, memory_ceiling_mb))

        # --- the four-state marking, per DEFINITION NODE ---------------
        ORDER = ("names_its_opcode", "one_static_hop",
                 "emits_opcode_dynamic", "emits_nothing")
        marking = {}
        for site in sites:
            node_id = site["definition"]
            if node_id is None:
                continue
            row = marking.setdefault(node_id, {
                "id": node_id,
                "language": language,
                "file": spans[node_id].get("file"),
                "start_line": spans[node_id].get("start_line"),
                "label": spans[node_id].get("label"),
                "state": "emits_nothing",
                "sites": 0,
                "opcodes": set(),
                "pseudo_opcodes": set(),
                "reasons": set(),
            })
            row["sites"] += 1
            row["opcodes"] |= {one["text"] for one in site["opcodes"]}
            row["pseudo_opcodes"] |= {one["text"]
                                      for one in site["pseudo_opcodes"]}
            row["reasons"] |= set(site["reasons"])
            if ORDER.index(site["state"]) < ORDER.index(row["state"]):
                row["state"] = site["state"]
        rows = []
        for node_id, row in marking.items():
            row = dict(row)
            row["opcodes"] = [arch_text_row(o) for o in sorted(row["opcodes"])]
            row["pseudo_opcodes"] = [arch_text_row(o)
                                     for o in sorted(row["pseudo_opcodes"])]
            row["reasons"] = sorted(row["reasons"])
            rows.append(row)
        rows.sort(key=lambda one: (one["file"] or "", one["start_line"] or 0))

        by_state = {name: 0 for name in ORDER}
        for row in rows:
            by_state[row["state"]] += 1
        # A definition whose ONLY call sites emit nothing (swift's three
        # empty inline-assembly templates) is in `rows` and is already
        # counted above; the rest of the region joins it here. The four
        # states sum to the definition population, and that is checked.
        emitting = [row for row in rows if row["state"] != "emits_nothing"]
        by_state["emits_nothing"] = len(spans) - len(emitting)
        assert sum(by_state.values()) == len(spans), (
            "the four states must partition the definition population")

        # --- CO-LOCATION, measured and labelled as NOT a promotion -----
        # Many a state-3 definition names arch opcodes elsewhere in its own
        # body (a switch that fills a local, which the emitter then hands
        # over). That is CO-LOCATION, not resolution: the source does not
        # say which of them this call site emits, so the state does not
        # change and no opcode is recorded for it. It is counted here
        # because leaving it out would look like the region names nothing.
        co_located = 0
        arch_re = rules.get("arch_token")
        if arch_re:
            for row in rows:
                if row["state"] != "emits_opcode_dynamic":
                    continue
                text = texts.get(row["file"], "")
                if not text:
                    continue
                lines = text.splitlines()
                start = (row["start_line"] or 1) - 1
                end = spans[row["id"]].get("end_line") or (start + 1)
                if re.search(arch_re, "\n".join(lines[start:end])):
                    co_located += 1

        # --- the inverse index: per opcode, the definitions emitting it -
        inverse = {}
        for row in rows:
            for one in row["opcodes"]:
                inverse.setdefault(one["text"], []).append(row["id"])
        inverse_rows = [
            {"opcode": arch_text_row(name),
             "language": language,
             "definitions": sorted(set(where)),
             "definition_count": len(set(where))}
            for name, where in sorted(inverse.items())
        ]

        # --- what may be dropped, and what the graph shrinks to --------
        emitters = {row["id"] for row in emitting}
        callers = {}
        for edge in self.static_structure["edges"]:
            if edge.get("rel") != "calls":
                continue
            callers.setdefault(edge["dst"], set()).add(edge["src"])
        one_hop = set(emitters)
        for node_id in emitters:
            one_hop |= callers.get(node_id, set())
        one_hop &= set(spans) | emitters
        transitive, frontier_of_walk = set(emitters), list(emitters)
        while frontier_of_walk:
            node_id = frontier_of_walk.pop()
            for source in callers.get(node_id, ()):
                if source not in transitive and source in spans:
                    transitive.add(source)
                    frontier_of_walk.append(source)

        def induced(keep):
            n = 0
            for edge in self.static_structure["edges"]:
                if edge["src"] in keep and edge["dst"] in keep:
                    n += 1
            return n

        peak = max(peak,
                   resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0)
        document = {
            "generated_by": "graph.py Graph.arch_opcode_nodes (task 95)",
            "node": "hq.research.compiler_graph.graph -- the arch-opcode-node",
            "language": language,
            "pins": self.pins,
            "region_directories": list(region.directories),
            "how_the_emitter_was_located": rules.get("note", ""),
            "pseudo_opcode_table": pseudo_source,
            "pseudo_opcode_names": len(pseudo),
            "states": {
                "names_its_opcode":
                    "a call site of the emitter passes a constant",
                "one_static_hop":
                    "the opcode argument reads a static table, and the hop "
                    "was followed",
                "emits_opcode_dynamic":
                    "an emitter whose opcode cannot be named from source; a "
                    "category, never a guess",
                "emits_nothing":
                    "no emitter call site -- droppable without losing "
                    "opcode-production information",
            },
            "populations": {
                "region_nodes": len(self.static_structure["nodes"]),
                "definitions": len(spans),
                "emitter_call_sites": len(sites),
                "definitions_with_at_least_one_call_site": len(rows),
                "emitter_call_sites_outside_any_definition":
                    sum(1 for one in sites if one["definition"] is None),
            },
            "emitter_census": census,
            "declarations_skipped_because_they_are_not_call_sites":
                declarations_skipped,
            "emitter_declarations": emitter_declarations,
            "by_state": by_state,
            "by_state_of_call_sites": {
                name: sum(1 for one in sites if one["state"] == name)
                for name in ORDER
            },
            "state_three_definitions_that_name_arch_opcodes_elsewhere_in_"
            "their_own_body": co_located,
            "what_that_number_is_not": (
                "CO-LOCATION, never resolution. The source does not say "
                "which of the opcodes named in the body this call site "
                "emits, so the definition stays in state 3 and none of "
                "them is recorded against it."
            ),
            "hop_not_resolved_by_reason": {
                reason: sum(1 for one in sites
                            if reason in one.get("reasons", []))
                for reason in sorted({r for one in sites
                                      for r in one.get("reasons", [])})
            },
            # STATE 1 SPLIT. A call site may name a PSEUDO opcode -- go's
            # `obj.ACALL`, `obj.AFUNCDATA`; LLVM's `TargetOpcode::COPY`.
            # It still NAMES its opcode, so it is state 1; but a pseudo is
            # not a machine instruction, so the inverse index carries only
            # arch opcodes and the split is reported rather than blurred.
            "names_its_opcode_with_at_least_one_arch_opcode": sum(
                1 for row in rows
                if row["state"] == "names_its_opcode" and row["opcodes"]),
            "names_its_opcode_naming_only_pseudo_opcodes": sum(
                1 for row in rows
                if row["state"] == "names_its_opcode" and not row["opcodes"]),
            "distinct_arch_opcodes": len(inverse),
            "distinct_pseudo_opcodes": len({
                one["text"] for row in rows for one in row["pseudo_opcodes"]}),
            "shrink": {
                "definitions": len(spans),
                "emitters_only": len(emitters),
                "emitters_and_their_direct_callers": len(one_hop),
                "emitters_and_all_their_callers": len(transitive),
                "edges_all": len(self.static_structure["edges"]),
                "edges_induced_on_emitters_only": induced(emitters),
                "edges_induced_on_emitters_and_direct_callers":
                    induced(one_hop),
                "edges_induced_on_emitters_and_all_callers":
                    induced(transitive),
            },
            "unmeasured_by_absence_of_an_emitter":
                rules.get("unmeasured_by_absence_of_an_emitter", ""),
            "named_frontiers": [
                one for one in (
                    rules.get("td_table_frontier", ""),
                    rules.get("unmeasured_by_absence_of_an_emitter", ""),
                ) if one
            ],
            "cost": {
                "wall_seconds": round(time.time() - started, 1),
                "peak_resident_mb": round(peak, 1),
                "memory_ceiling_mb": memory_ceiling_mb,
                "refusal_name": "MemoryCeilingReached",
                "region_files_read": len(texts),
            },
            "definitions_marked": rows,
            "inverse_index": inverse_rows,
            "call_sites": sites,
            "emits_nothing": sorted(set(spans) - emitters),
        }
        if out_path:
            Path(out_path).write_text(json.dumps(document, indent=1))
            # THE MECHANICAL GUARD, and the stage REFUSES ITS OWN OUTPUT.
            # The ban's own rule: every pipeline stage that groups or pairs
            # units runs check_no_spelling_keys.py and refuses on failure.
            # This is not decoration -- the first artifact this pass wrote
            # was refused at `$.call_sites[223].argument`, go's `as`.
            guard = HERE.parent / "op_pipeline" / "check_no_spelling_keys.py"
            if guard.exists():
                verdict = subprocess.run(
                    [sys.executable, str(guard), str(out_path)],
                    capture_output=True, text=True)
                document["spelling_guard"] = {
                    "program": str(guard),
                    "exit": verdict.returncode,
                    "transcript": verdict.stdout.strip().splitlines()[-4:],
                }
                if verdict.returncode != 0:
                    raise SpellingKeyRefused(
                        "%s was refused by the unmodified spelling guard:\n%s"
                        % (out_path, verdict.stdout))
                Path(out_path).write_text(json.dumps(document, indent=1))
        return document

    # ------------------------------------------------------------ save --

    def counts(self):
        by_kind = {}
        for record in self.static_structure["nodes"].values():
            kind = record.get("kind")
            by_kind[kind] = by_kind.get(kind, 0) + 1
        by_relation = {}
        for edge in self.static_structure["edges"]:
            relation = edge["rel"]
            by_relation[relation] = by_relation.get(relation, 0) + 1
        by_frontier = {}
        for record in self.frontier:
            kind = record["kind"]
            by_frontier[kind] = by_frontier.get(kind, 0) + 1
        return {
            "nodes": len(self.static_structure["nodes"]),
            "edges": len(self.static_structure["edges"]),
            "frontier": len(self.frontier),
            "parse_errors": len(self.parse_errors),
            "nodes_by_kind": by_kind,
            "edges_by_relation": by_relation,
            "frontier_by_kind": by_frontier,
            "files": len(self._by_file),
        }

    def save(self, path):
        payload = {
            "pins": self.pins,
            "counts": self.counts(),
            "nodes": list(self.static_structure["nodes"].values()),
            "edges": self.static_structure["edges"],
            "frontier": self.frontier,
            "parse_errors": self.parse_errors,
        }
        Path(path).write_text(json.dumps(payload, indent=1))
        return payload["counts"]

    @classmethod
    def load(cls, path):
        """read a graph on disk, IN EITHER FORM.

        THE GRAPHS MOVED AND SHRANK, 2026-09-04 (task 93).  They live in
        the companion folder `PseudoCoupGraphs` and are stored in the
        COMPACT form: one string table for the whole document and every
        record an array of references into it, 8 to 10 times smaller,
        with `graph_compact.expand` rebuilding the old file byte for
        byte.  This reader accepts either, so every caller of
        `Graph.load` is unchanged.
        """
        import graph_compact
        if graph_compact.is_compact(str(path)):
            payload = graph_compact.expanded_document(str(path))
        else:
            payload = json.loads(Path(path).read_text())
        graph = cls(payload["pins"].get("region", ""))
        graph.pins = payload["pins"]
        for record in payload["nodes"]:
            graph.static_structure["nodes"][record["id"]] = record
            graph._by_file.setdefault(record.get("file"), []).append(
                record["id"]
            )
        graph.static_structure["edges"] = payload["edges"]
        graph.frontier = payload["frontier"]
        graph.parse_errors = payload.get("parse_errors", [])
        return graph


# ----------------------------------------------------- tree helpers -----


def diary_record(line):
    """The unit record of one diary line: the third tab field."""
    fields = line.rstrip("\n").split("\t")
    if len(fields) < 3:
        return None
    record = fields[2].strip()
    return record or None


def diary_subject(line):
    """The SUBJECT of one diary line: the second tab field. `-` means
    no compiler entry point was open. Folded in from coverage.py."""
    fields = line.rstrip("\n").split("\t")
    if len(fields) < 2:
        return "-"
    return fields[1].strip() or "-"


def diary_join_key(record):
    """The declaration coordinate `file:line` of a diary record: the
    third pipe-field. Returns None when the record has no such field."""
    parts = record.split("|")
    if len(parts) < 3:
        return None
    site = parts[2].strip()
    if ":" not in site:
        return None
    return site


def node_text(source, node):
    return source[node.start_byte:node.end_byte].decode("utf-8", "replace")


def find_by_type(root, types):
    """Every node of one of `types` under root, root itself excluded."""
    if not types:
        return
    wanted = set(types)
    stack = list(root.children)
    while stack:
        node = stack.pop()
        if node.type in wanted:
            yield node
        for child in node.children:
            stack.append(child)


def find_definitions(pack, root):
    """Top-down: a def nested inside a def is still a def (a closure),
    so the walk does not stop when it finds one."""
    wanted = set(pack.def_types)
    stack = [root]
    while stack:
        node = stack.pop()
        if node.type in wanted:
            yield node
        for child in node.children:
            stack.append(child)


def definition_name(pack, source, definition):
    for field_name in pack.name_fields:
        candidate = definition.child_by_field_name(field_name)
        while candidate is not None and candidate.type in pack.name_descend:
            inner = candidate.child_by_field_name("declarator")
            if inner is None:
                break
            candidate = inner
        if candidate is not None:
            return node_text(source, candidate)
    return None


def find_slots(pack, definition):
    """Params and locals of ONE def: the walk does not descend into a
    nested def, because those slots belong to that def."""
    inner = set(pack.def_types)
    params = set(pack.param_types)
    locals_ = set(pack.local_types)
    stack = list(definition.children)
    while stack:
        node = stack.pop()
        if node.type in params:
            yield node, "param"
            continue
        if node.type in locals_:
            yield node, "local"
        if node.type in inner:
            continue
        for child in node.children:
            stack.append(child)


NAME_LEAF_TYPES = (
    "identifier",
    "simple_identifier",
    "field_identifier",
    "type_identifier",
    "pattern",
)


def slot_declared_name(pack, source, slot_node):
    """The declared name inside a param or local declaration: the first
    plain name leaf, descending through declarators."""
    stack = [slot_node]
    while stack:
        node = stack.pop(0)
        if node.type in NAME_LEAF_TYPES:
            return node_text(source, node)
        for child in node.named_children:
            stack.append(child)
    return None


# ------------------------------------------------------------- pins -----


def run_git(repository, arguments):
    result = subprocess.run(
        ["git"] + arguments,
        cwd=repository, capture_output=True, text=True, check=True,
    )
    return result.stdout


def resolve_pin(repository, pin):
    return run_git(repository, ["rev-list", "-n1", pin]).strip()


def show_file(repository, pin, relative_path):
    return run_git(repository, ["show", "%s:%s" % (pin, relative_path)])


def list_region_files(region):
    """Every file of the region, listed from the PIN -- never from the
    working tree, which sits at a different commit in all four repos."""
    out = []
    for directory in region.directories:
        listing = run_git(
            region.repository,
            ["ls-tree", "-r", "--name-only", region.pin, directory],
        )
        for line in listing.splitlines():
            path = line.strip()
            if not path:
                continue
            if Path(path).suffix not in region.keep_extensions:
                continue
            if any(path.endswith(s) for s in region.skip_suffixes):
                continue
            if any(fragment in path for fragment in region.skip_path_contains):
                continue
            out.append(path)
    return sorted(out)


# ------------------------------------------------------------- main -----


def command_join(arguments):
    """The re-join: task 71's own graph x task 72's diaries."""
    instance = Graph.load(arguments.graph)
    instance.diary(arguments.diaries)
    instrumented = None
    if arguments.instrumented:
        records = json.loads(Path(arguments.instrumented).read_text())
        instrumented = ["%s:%s" % (record["file"], record["start_line"])
                        for record in records]
    result = instance.coverage(instrumented=instrumented)
    result["provenance"] = {
        "graph": str(arguments.graph),
        "graph_form": "task71 (graph.py, ids file#line#kind#ordinal)",
        "join_key": "the declaration coordinate file:line",
        "diaries": str(arguments.diaries),
        "instrumented_list": str(arguments.instrumented or ""),
    }
    Path(arguments.out).write_text(json.dumps(result, indent=1) + "\n")
    for name in ("population_region_nodes", "population_defs",
                 "population_instrumented", "population_probes",
                 "defs_visited_by_at_least_one_probe",
                 "instrumented_visited_by_at_least_one_probe",
                 "uninstrumented_defs_a_named_frontier",
                 "never_visited_count",
                 "visited_keys_outside_the_region"):
        print("%-48s %s" % (name, result.get(name)))
    print("wrote %s" % arguments.out)


def command_super_ops(arguments):
    # The diaries are NOT preloaded into dynamic_structure here: the
    # miner streams them one file at a time, which is the whole point
    # of its memory bound.
    instance = Graph.load(arguments.graph)
    result = instance.super_ops(
        diary_directory=arguments.diaries,
        min_length=arguments.min_length,
        min_support=arguments.min_support,
        subject=arguments.subject,
        max_length=arguments.max_length,
        max_runs_per_level=arguments.max_runs_per_level,
        memory_ceiling_mb=arguments.memory_ceiling_mb,
        language=arguments.language,
        cache_path=arguments.cache or None,
    )
    result["provenance"] = {
        "graph": str(arguments.graph),
        "diaries": str(arguments.diaries),
        "produced_by": "graph.py super-ops (Graph.super_ops)",
    }
    Path(arguments.out).write_text(json.dumps(result, indent=1) + "\n")
    print(json.dumps(result["parameters"], indent=1))
    print(json.dumps(result["populations"], indent=1))
    print(json.dumps(result["cost"], indent=1))
    print("wrote %s" % arguments.out)


def command_variant_connections(arguments):
    """THE THIRD CONNECTION KIND, from the command line."""
    instance = Graph.load(arguments.graph)
    result = instance.variant_connections(
        diary_directory=arguments.diaries,
        unit_sources=arguments.units,
        default_language=arguments.language,
        subject=arguments.subject,
        memory_ceiling_mb=arguments.memory_ceiling_mb,
        max_transitions=arguments.max_transitions,
        exclusive_examples=arguments.exclusive_examples,
        cache_path=arguments.cache or None,
        unmeasured_reason=arguments.unmeasured_reason or None,
    )
    result["provenance"] = {
        "graph": str(arguments.graph),
        "diaries": str(arguments.diaries),
        "unit_sources": list(arguments.units),
        "produced_by": "graph.py variant-connections "
                       "(Graph.variant_connections)",
        "node": "hq.research.compiler_graph.graph",
    }
    Path(arguments.out).write_text(json.dumps(result, indent=1) + "\n")
    print(json.dumps(result["parameters"], indent=1))
    print(json.dumps(result["populations"], indent=1))
    print(json.dumps(result.get("census", {}), indent=1))
    print(json.dumps(result.get("static_backing", {}), indent=1))
    print(json.dumps(result.get("cost", {}), indent=1))
    print("wrote %s" % arguments.out)


def command_arch_opcode_nodes(arguments):
    """THE ARCH-OPCODE-NODE (task 95): which definitions of a compiler's
    own source produce a machine instruction, read from SOURCE ALONE."""
    instance = Graph.load(arguments.graph)
    document = instance.arch_opcode_nodes(
        out_path=arguments.out,
        memory_ceiling_mb=arguments.memory_ceiling_mb,
    )
    summary = {key: value for key, value in document.items()
               if key not in ("definitions_marked", "call_sites",
                              "emits_nothing", "inverse_index")}
    summary["inverse_index_size"] = len(document["inverse_index"])
    summary["emits_nothing_size"] = len(document["emits_nothing"])
    if arguments.summary:
        Path(arguments.summary).write_text(json.dumps(summary, indent=1))
    sys.stderr.write("%s: %s\n" % (arguments.out, json.dumps(
        {"by_state": document["by_state"],
         "call_sites": document["populations"]["emitter_call_sites"],
         "distinct_arch_opcodes": document["distinct_arch_opcodes"],
         "peak_resident_mb": document["cost"]["peak_resident_mb"]})))


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("join", "super-ops",
                                             "variant-connections",
                                             "arch-opcode-nodes"):
        parser = argparse.ArgumentParser(description=__doc__)
        subs = parser.add_subparsers(dest="mode", required=True)
        p_join = subs.add_parser("join")
        p_join.add_argument("--graph", required=True)
        p_join.add_argument("--diaries", required=True)
        p_join.add_argument("--instrumented", default="")
        p_join.add_argument("--out", required=True)
        p_join.set_defaults(run=command_join)
        p_ops = subs.add_parser("super-ops")
        p_ops.add_argument("--graph", required=True)
        p_ops.add_argument("--diaries", required=True)
        p_ops.add_argument("--min-length", type=int, default=3,
                           dest="min_length")
        p_ops.add_argument("--min-support", type=int, default=2,
                           dest="min_support")
        p_ops.add_argument("--max-length", type=int, default=12,
                           dest="max_length")
        p_ops.add_argument("--max-runs-per-level", type=int,
                           default=2000000, dest="max_runs_per_level")
        p_ops.add_argument("--memory-ceiling-mb", type=int, default=6144,
                           dest="memory_ceiling_mb")
        p_ops.add_argument("--cache", default="")
        p_ops.add_argument("--subject", default="probe_own",
                           choices=("probe_own", "main", "all"))
        p_ops.add_argument("--language", default="go")
        p_ops.add_argument("--out", required=True)
        p_ops.set_defaults(run=command_super_ops)
        p_var = subs.add_parser("variant-connections")
        p_var.add_argument("--graph", required=True)
        p_var.add_argument("--diaries", required=True)
        p_var.add_argument("--units", action="append", default=[],
                           help="a JSON file with a `units` mapping, or a "
                                "directory of them; may be repeated")
        p_var.add_argument("--language", default="",
                           help="the language of a diary directory whose "
                                "stems carry no `<language>__` prefix")
        p_var.add_argument("--subject", default="probe_own",
                           choices=("probe_own", "main", "all"))
        p_var.add_argument("--memory-ceiling-mb", type=int, default=6144,
                           dest="memory_ceiling_mb")
        p_var.add_argument("--max-transitions", type=int, default=8000000,
                           dest="max_transitions")
        p_var.add_argument("--exclusive-examples", type=int, default=8,
                           dest="exclusive_examples")
        p_var.add_argument("--cache", default="")
        p_var.add_argument("--unmeasured-reason", default="",
                           dest="unmeasured_reason",
                           help="the reason a language has no diaries, "
                                "quoted from the cost page; written onto "
                                "the artifact when none exist")
        p_var.add_argument("--out", required=True)
        p_var.set_defaults(run=command_variant_connections)
        p_arch = subs.add_parser("arch-opcode-nodes")
        p_arch.add_argument("--graph", required=True)
        p_arch.add_argument("--memory-ceiling-mb", type=int, default=6144,
                            dest="memory_ceiling_mb")
        p_arch.add_argument("--summary", default="")
        p_arch.add_argument("--out", required=True)
        p_arch.set_defaults(run=command_arch_opcode_nodes)
        arguments = parser.parse_args()
        arguments.run(arguments)
        return
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("region", choices=sorted(REGIONS))
    parser.add_argument("--out", default=None)
    arguments = parser.parse_args()
    region = REGIONS[arguments.region]
    graph = Graph()
    graph.build(region)
    out_path = arguments.out or (HERE / ("graph_%s.json" % region.name))
    counts = graph.save(out_path)
    sys.stderr.write("%s: %s\n" % (out_path, json.dumps(counts)))


if __name__ == "__main__":
    main()
