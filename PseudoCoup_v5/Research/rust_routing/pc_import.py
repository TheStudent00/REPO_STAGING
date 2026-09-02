"""INVOCATION RING — import hook for .pc hub modules.

Stock CPython cannot parse `a r./ b`, and forking the parser is the
PCv6 question. The hook gets real surface spelling without touching
the parser: it intercepts the module between file and compile, and
rewrites qualified operators into calls on the runtime.

    a r./ b     ->    a |_r_div| b
    r.i64(7)    ->    _pc_i64(7)

Everything downstream (Ledger, routing, encoding, mounting) then
runs at first execution of the expression.

Install with:  import pc_import; pc_import.install()
Then:          import demo          # loads demo.pc
"""

import importlib.abc
import importlib.machinery
import importlib.util
import re
import sys
from pathlib import Path

from pc_runtime import NAMESPACE

# qualified operator spellings -> infix runtime names
OPERATORS = {
    r"r\./": "_r_div",
    r"r\.%": "_r_rem",
    r"r\.\+": "_r_add",
    r"r\.-": "_r_sub",
    r"r\.\*": "_r_mul",
}
_TYPE_CALL = re.compile(r"\br\.i64\s*\(")


def rewrite(source: str) -> str:
    """Qualified spellings -> valid Python. Greppable both ways."""
    out = source
    for pattern, name in OPERATORS.items():
        out = re.sub(pattern, f"|{name}|", out)
    out = _TYPE_CALL.sub("_pc_i64(", out)
    return out


class PCLoader(importlib.abc.Loader):
    def __init__(self, path):
        self.path = path

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        source = Path(self.path).read_text()
        code = compile(rewrite(source), self.path, "exec")
        module.__dict__.update(NAMESPACE)
        exec(code, module.__dict__)


class PCFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        name = fullname.rpartition(".")[2]
        for entry in (path or sys.path):
            candidate = Path(entry) / f"{name}.pc"
            if candidate.is_file():
                return importlib.util.spec_from_loader(
                    fullname, PCLoader(str(candidate)),
                    origin=str(candidate))
        return None


_installed = False


def install():
    global _installed
    if not _installed:
        sys.meta_path.insert(0, PCFinder())
        _installed = True
