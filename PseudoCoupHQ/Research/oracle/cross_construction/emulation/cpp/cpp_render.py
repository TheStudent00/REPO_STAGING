#!/usr/bin/env python3
"""cpp_render.py -- task ex1: AutoPoly with CPP as the FIFTH compiled
target.

Node: hq.research.arch_unit_oracle.cross_construction
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/CORE_0_3_2_2_cross_construction.md`).

THE OBJECTS, one sentence each, in relation.
  * A TERM is one place of one arch-opcode written as a z3 expression
    over `seed_<register family>` symbols.
  * AN EMULATION is a cpp translation unit whose one exported function's
    body is that term written in cpp's own operations over cpp's
    holders, produced by the ONE renderer below (`CppRenderer`, which
    DERIVES from task o7's `emulate.Renderer`).
  * THE SHIP BUILD is `/usr/bin/clang++ -std=c++20 -O1 -c`, read off
    `lane_gen.py`'s own cpp branch -- the build every cpp unit of the
    corpus was made with.

WHAT WAS MEASURED BEFORE A SPELLING WAS WRITTEN (task o11 section 3.1's
rule).  cpp is c's renderer with cpp's holders and ship flags, and the
question this file exists to answer is what, if anything, cpp spells
differently at those holders.  The measurement is the corpus's own:
every c source task ap4's loop rendered (309 of them under
`autopoly/src4/`) handed to clang++ at the cpp ship flags.  Lane
`ex1_l2_cpp_and_value_model_probes.sh`, on the tower at
`<runs>/ex1/agent/logs/*__ex1_l2_cpp_and_value_model_probes.sh.log`,
answered, LITERAL:

    c sources task ap4's loop rendered: 309
    compiled by clang++ VERBATIM: 305 of 309
    refused, by the compiler's own first error line:
          2  error: expression is not assignable
             first: lea_mem_gpr_32__primitive__c.c
          1  error: ISO C++17 does not allow incrementing expression of type bool [-Wincrement-bool]
             first: mov_imm_gpr_8__primitive__c.c
          1  error: cannot decrement expression of type bool
             first: xor_imm_gpr_8__primitive__c.c

and the four refusals are all on the PRIMITIVE route, where the text
rendered is the corpus row's own operator on the corpus row's own
holders -- a c row, so a c spelling.  cpp's primitive route renders
cpp's own rows, which are the rows clang++ itself accepted.  The TERM
route, which is the other 305, is unchanged text for text.

Two things about cpp are therefore the whole of this file:
  * THE SYMBOL.  cpp mangles a function name unless it is declared
    `extern "C"`.  Lane `ex1_l1_toolchains_and_runners.sh` measured it,
    LITERAL:
        0000000000000000 g     F .text  0000000000000004 _Z10plain_namejj
        0000000000000010 g     F .text  0000000000000004 c_name
    and the carve asks objdump for the symbol by name, so an emulation
    whose name is mangled cannot be carved.  `extern "C"` is emitted.
    This is also the corpus's own shape: `probe_gen.emit_cpp` writes
    `extern "C" auto` over every cpp probe.
  * THE HEADERS.  The corpus's own cpp probe includes `<cstdint>`, and
    the helper the renderer writes for a float's bits needs `memcpy`,
    which in cpp is `<cstring>`.  Both were measured to give the
    unqualified names this renderer writes (`uint32_t`, `UINT32_C`,
    `memcpy`), lane `ex1_l2` section [3/9].

The holders were each asked of clang++ separately, same lane, and all
five ACCEPTED: `unsigned __int128`, `_Float16`, `long double` (which
carves to `fldt`/`faddp`, the same x87 form c's does), the `UINT32_C`
macros, and the C-style cast chain the renderer emits.  So the holder
table is c's, unchanged, and this file states no holder of its own.

WHAT IS REUSED RATHER THAN COPIED, said out loud.  Nothing under
`Research/op_pipeline/` is edited and `emulate.py` is imported, never
forked: `emulate.Renderer` is DERIVED FROM and every `emit` method,
the width planning, the free-symbol check, the helper texts and the
refusal causes are inherited unchanged.  cpp's arrival contract is the
SysV one (`canon37_gate.sequences_for` answers with the SysV sequence
for every language except go), so `emulate.recorded_facts` and
`emulate.expected_c_families` apply unchanged and are called rather
than restated.

MEMORY BOUND: this file allocates nothing of its own and runs inside
the driver's one collecting process under its stated 6 GB resident
bound and named abort ABORT_MEMORY_EX1.

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

Nothing here keys, groups, pairs or selects anything.  This file is a
printer and a compiler call.

Coding discipline: no compound one-liner statements.

usage:
  cpp_render.py flags     the ship flags and their source, LITERAL
  cpp_render.py probe     the one probe this file's own claims rest on
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
EMULATION = os.path.normpath(os.path.join(HERE, ".."))
CROSS = os.path.normpath(os.path.join(HERE, "..", ".."))
OP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                   "op_pipeline"))
sys.path.insert(0, OP)
sys.path.insert(0, CROSS)
sys.path.insert(0, EMULATION)

import emulate as E                                             # noqa: E402

TARGET = "cpp"

# `lane_gen.py` line 289, LITERAL: CLANGXX = "/usr/bin/clang++"
CLANGXX = "/usr/bin/clang++"
SHIP_FLAGS = ["-std=c++20", "-O1", "-c"]
SHIP_FLAGS_SOURCE = ("lane_gen.py compile_probe, cpp branch: "
                     "`opt = [\"-O0\", \"-g\"] if mode == \"anchor\" "
                     "else [\"-O1\"]`; `cmd = [CLANGXX, \"-std=c++20\"] "
                     "+ opt + [\"-c\", src, \"-o\", obj]` -- the ship "
                     "build of every cpp unit in the corpus")

# THE TWO SPELLINGS THAT ARE NOT c's, each measured (see the header).
LINKAGE = 'extern "C"'
HEADER_FIXED_WIDTH = "#include <cstdint>"
HEADER_MEMCPY = "#include <cstring>"


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def clangxx_answer():
    """what running clang++ actually does on the machine this runs on:
    the literal answer, whatever it is.  Re-read at run time rather
    than pasted from a previous lane."""
    try:
        done = subprocess.run([CLANGXX, "--version"],
                              capture_output=True, text=True,
                              timeout=120)
    except OSError as problem:
        return "%s: %s" % (CLANGXX, problem.strerror)
    if done.returncode != 0:
        text = (done.stderr or done.stdout).strip()
        first = "(no diagnostic)"
        if text:
            first = text.splitlines()[0]
        return "%s exited %d: %s" % (CLANGXX, done.returncode, first)
    return (done.stdout or done.stderr).strip().splitlines()[0]


# ==================================================================
# section 1: THE RENDERER   z3 term -> cpp source
# ==================================================================

class CppRenderer(E.Renderer):
    """the ONE cpp renderer: a z3 term over `seed_<family>` symbols ->
    one cpp translation unit.  DERIVES from task o7's
    `emulate.Renderer`; every `emit` method, the width planning, the
    free-symbol check, the helper texts and the refusal causes are
    inherited UNCHANGED, because clang++ accepts them -- 305 of the 309
    sources task ap4's loop rendered compile verbatim, and the four
    that do not are c primitive rows and not term-route text.

    What is overridden is the FILE, and only the two things measured to
    differ: the linkage that keeps the symbol carvable, and the header
    names.

    attributes:
        families        the term's arrival families, IN order
        result_family   the answer home
        result_width    its width in bits
        params          per family: name, holder text, kind, bits
    methods:
        render          -> (source text, function symbol)
    """

    def __init__(self, families, result_family, result_width, label):
        E.Renderer.__init__(self, families, result_family, result_width,
                            label)

    def render(self, term, text):
        """the whole cpp translation unit.

        `emulate.Renderer.render`'s own body, with three lines changed
        and nothing else: `<stdint.h>` becomes `<cstdint>`,
        `<string.h>` becomes `<cstring>`, and `extern "C"` is emitted
        before the return type so the symbol the carve asks objdump for
        is the one the object file carries."""
        self.plan_parameters(term)
        self.check_symbols(term)
        root_text, root_kind, root_width = self.emit(term)
        return_type, body = self.answer(root_text, root_kind, root_width)
        symbol = "emu_%s" % self.label
        lines = []
        lines.append("/* task ex1 emulation -- rendered by cpp_render.py "
                     "CppRenderer from the layer-4 term of %s.  The "
                     "term's layer-5 text, LITERAL:" % self.label)
        lines.append("   %s */" % " ".join(text.split()))
        lines.append(HEADER_FIXED_WIDTH)
        if self.helpers:
            lines.append(HEADER_MEMCPY)
        for helper in sorted(self.helpers):
            lines.append(self.helper_text(helper))
        params = []
        for param in self.params:
            params.append("%s %s" % (param["holder"], param["name"]))
        if not params:
            params.append("void")
        lines.append("")
        lines.append(LINKAGE)
        lines.append("%s" % return_type)
        lines.append("%s(%s)" % (symbol, ", ".join(params)))
        lines.append("{")
        lines.append("    return %s;" % body)
        lines.append("}")
        lines.append("")
        return "\n".join(lines), symbol


# ==================================================================
# section 2: COMPILE AND CARVE   clang++ at the corpus's ship flags
# ==================================================================

def compile_and_carve(source, symbol):
    """the cpp corpus's own ship compile and carve: clang++ at
    SHIP_FLAGS, objdump read by `emulate.pipeline_extractor()`, which
    is `lane_gen.DRIVER`'s own `extract`."""
    extract = E.pipeline_extractor()
    work = tempfile.mkdtemp(prefix="ex1_", dir=os.environ.get("TMPDIR"))
    src = os.path.join(work, "unit.cpp")
    obj = os.path.join(work, "unit_ship.o")
    handle = open(src, "w")
    handle.write(source)
    handle.close()
    command = [CLANGXX] + SHIP_FLAGS + [src, "-o", obj]
    done = subprocess.run(command, capture_output=True, text=True,
                          timeout=180)
    if done.returncode != 0 or not os.path.exists(obj):
        E.cleanup(work)
        return None, E.firstline(done.stderr or done.stdout)
    done = subprocess.run(["objdump", "-dr", "--disassemble=" + symbol,
                           obj], capture_output=True, text=True,
                          timeout=180)
    got = extract(done.stdout, symbol, True)
    E.cleanup(work)
    if got is None:
        return None, "objdump found no symbol %s" % symbol
    return got, None


def recorded_facts(label, key, raw_bytes, mnem):
    """task o7's `emulate.recorded_facts`, unchanged, then relabelled.

    `canon37_gate.sequences_for` returns the SysV sequence for both "c"
    and "cpp", so the arrival contract it reads is the same object; the
    `lang` field is set to cpp afterwards because `term.py` reads it to
    pick the toolchain whose runtime-callee bodies a `call` resolves
    to, and its own table already names cpp's
    (`term.Walk.TOOLCHAIN_OF`, LITERAL: `"cpp": "clang++"`)."""
    recorded = E.recorded_facts(label, key, raw_bytes, mnem)
    recorded["lang"] = TARGET
    return recorded


# ==================================================================
# section 3: THE SPELLING TABLE, each row with the probe that measured it
# ==================================================================

def spelling_rows():
    """the rows of this target's spelling table.  Each row names the
    lane whose log carries the object it rests on; nothing here is
    read out of a language reference."""
    return [
        {"what": "the holders",
         "spelling": "c's own, unchanged: uint8_t .. uint64_t, "
                     "unsigned __int128, float, double, _Float16, "
                     "long double",
         "probe": "ex1_l2 [3/9] holder_u128, holder_f16, "
                  "holder_long_double: each ACCEPTED by clang++ at the "
                  "ship flags, and long double carved to "
                  "`fldt 0x18(%rsp); fldt 0x8(%rsp); faddp %st,%st(1); "
                  "ret`, the same x87 form c's gives"},
        {"what": "the fixed-width header",
         "spelling": HEADER_FIXED_WIDTH,
         "probe": "ex1_l2 [3/9] cstdint_unqualified and macro_uint32_c: "
                  "`uint64_t`, `int64_t` and `UINT32_C` are reached "
                  "unqualified through it"},
        {"what": "the header the float-bits helper needs",
         "spelling": HEADER_MEMCPY,
         "probe": "ex1_l2 [3/9] memcpy_helper: the helper c's renderer "
                  "writes, ACCEPTED verbatim under this header"},
        {"what": "the linkage",
         "spelling": LINKAGE,
         "probe": "ex1_l1 [5/6]: without it the symbol table carries "
                  "`_Z10plain_namejj` and the carve asks objdump for "
                  "`plain_name`"},
        {"what": "the expression text",
         "spelling": "c's own, unchanged -- every emit method is "
                     "inherited",
         "probe": "ex1_l2 [1/9]: 305 of the 309 c sources task ap4's "
                  "loop rendered compile under clang++ verbatim; the "
                  "four that do not are c PRIMITIVE rows (`bool` "
                  "increment, an unassignable expression), which cpp's "
                  "own primitive rows are not"},
        {"what": "the ship flags",
         "spelling": " ".join([CLANGXX] + SHIP_FLAGS),
         "probe": SHIP_FLAGS_SOURCE},
    ]


def flags_command():
    say("cpp ship flags, LITERAL: %s" % " ".join([CLANGXX] + SHIP_FLAGS))
    say("their source: %s" % SHIP_FLAGS_SOURCE)
    say("clang++, as this machine answers it: %s" % clangxx_answer())
    return 0


def probe_command():
    """the one probe this file's own claims rest on, run here so the
    file is self-checking: a rendered source with a helper in it,
    compiled and carved by this file's own two functions."""
    import z3
    seed = z3.BitVec("seed_rdi", 64)
    other = z3.BitVec("seed_rsi", 64)
    term = z3.ZeroExt(32, z3.Extract(31, 0, seed) + z3.Extract(31, 0, other))
    renderer = CppRenderer(["rdi", "rsi"], "rdi", 64, "probe_cpp")
    source, symbol = renderer.render(term, "Concat(0, Extract(31, 0, v0) "
                                           "+ Extract(31, 0, v1))")
    say("the rendered source, LITERAL:")
    for line in source.splitlines():
        say("   %s" % line)
    got, problem = compile_and_carve(source, symbol)
    if got is None:
        say("the compile or the carve refused: %s" % problem)
        return 1
    raw, mnem = got
    say("the carved body, LITERAL: %s" % "; ".join(mnem))
    say("its bytes: %s" % " ".join(raw))
    return 0


def main(argv):
    if not argv:
        say(__doc__)
        return 2
    if argv[0] == "flags":
        return flags_command()
    if argv[0] == "probe":
        return probe_command()
    say(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
