"""Language -- one language PCHQ covers, with its compiler at ship flags,
its corpus of compiled units, and the swap table `operator_for` that
pass A fills. Plan leaf: lean_proof_path.language, with methods compile,
render, compose_at_width and the attribute operator_for.

The only thing written per language is how to invoke its compiler and
cut a body out, which is plumbing -- and it is not even written here:
`compile` calls the routes rv3/rv6 already use (inherit_rv3.py's
compile_and_carve: c and c++ by clang at `-std=c17 -O1
--target=riscv64-linux-gnu --gcc-toolchain=/usr`, rust by rustc at
`--target=riscv64gc-unknown-linux-gnu --emit=obj -C opt-level=1`, go by
`GOARCH=riscv64 GOOS=linux go build`; the carve by llvm-objdump
`-M no-aliases --mattr=+m,+a,+f,+d,+c,+zba,+zbb,+zbs`).
"""

import os
import sys

AWAITS_BUILT_MODEL = "AWAITS_BUILT_MODEL"
NOT_RUN_YET = "NOT_RUN_YET"

RV_DIR = "PseudoCoupHQ/Research/oracle/riscv"
GENERAL_DIR = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general"


class Language:
    """attributes: name, toolchain (compiler command at ship flags,
    target riscv64), corpus (list of ArchUnit), operator_for
    (SailPrimitive -> ArchUnit, filled by pass A, never by hand)."""

    def __init__(self, name, toolchain):
        self.name = name
        self.toolchain = toolchain
        self.corpus = []
        self.operator_for = {}

    @staticmethod
    def compile(language, source, work, symbol=None):
        """compile(language, source) -> its ArchUnit, cut out of the
        binary at the function symbol: write the source; invoke the
        compiler for riscv64 at ship flags; cut the body out with
        llvm-objdump from the symbol to its return (rv3's routes, called,
        not re-typed); a compile failure is a refusal with the compiler's
        literal output."""
        from .arch_unit import ArchUnit
        for d in (RV_DIR, GENERAL_DIR):
            if d not in sys.path:
                sys.path.insert(0, d)
        import riscv_carve as CARVE                     # noqa: E402
        import inherit_rv3 as INH3                      # noqa: E402
        CARVE.MATTR = "+m,+a,+f,+d,+c,+zba,+zbb,+zbs"
        if symbol is not None:
            # rv1's units carry their own symbol; the route's symbol finder
            # looks for an emu_ name, so the carve is called directly here
            os.makedirs(work, exist_ok=True)
            if language == "c":
                path = os.path.join(work, "unit.c"); obj = path + ".o"
                open(path, "w").write(source)
                cmd = [CARVE.CLANG] + INH3.SHIP_C + ["-c", path, "-o", obj]
                rc, out, err = CARVE.sh(cmd)
                if rc != 0:
                    return {"refusal": "compile failed", "command": " ".join(cmd), "diagnostic": (err or out)[:600]}
                got, err2 = CARVE.disassemble(obj, symbol, True)
            elif language == "go":
                open(os.path.join(work, "go.mod"), "w").write(CARVE.GOMOD)
                open(os.path.join(work, "main.go"), "w").write(source)
                obj = os.path.join(work, "bin_rv")
                cmd = ["go", "build", "-o", obj, "."]
                rc, out, err = CARVE.sh(cmd, cwd=work, env=CARVE.GO_ENV, timeout=600)
                cmd = ["GOARCH=riscv64", "GOOS=linux"] + cmd
                if rc != 0:
                    return {"refusal": "compile failed", "command": " ".join(cmd), "diagnostic": (err or out)[:600]}
                got, err2 = CARVE.disassemble(obj, symbol, True)
            else:
                return {"refusal": "no symbol-named route for %s" % language}
            if got is None:
                return {"refusal": "carve found no symbol", "command": " ".join(cmd), "diagnostic": (err2 or "")[:600]}
            raw, body = got
            return {"unit": ArchUnit(language, source, symbol, raw), "body": body, "command": " ".join(cmd)}
        got, command, diag = INH3.compile_and_carve(source, language, work)
        if got is None:
            return {"refusal": "compile or carve failed", "command": command, "diagnostic": (diag or "")[:600]}
        raw, body = got
        return {"unit": ArchUnit(language, source, INH3.IN.symbol_of(source), raw), "body": body, "command": command}

    @staticmethod
    def render(language, definition):
        """render(language, definition) -> source text whose compiled body
        should compute the definition: at each primitive at width w the
        operator operator_for[(primitive, w)] holds, in the language's
        own spelling from that unit's source; compose_at_width where none
        exists; the two guards of a definition as the language's
        conditional; one candidate, never a search. Pass B is not run in
        lp1 (the brief's lanes stop at pass A)."""
        return {"refusal": NOT_RUN_YET}

    @staticmethod
    def compose_at_width(language, primitive, width):
        """compose_at_width(language, primitive, width) -> the same
        function from the language's operators at narrower widths (the
        construction for the kind); expected unused for c, c++, rust, go
        on rv64 (log 274 section 5.4)."""
        return {"refusal": NOT_RUN_YET}
