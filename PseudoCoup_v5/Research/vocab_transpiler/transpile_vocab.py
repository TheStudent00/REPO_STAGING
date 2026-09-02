"""Tier A transpiler: cranelift-assembler-x64 generated Rust -> Python.

WHY THE GENERATED OUTPUT AND NOT THE GENERATOR (decision 3, explained)
---------------------------------------------------------------------
`assembler.rs` does not exist in Cranelift's repository. It is WRITTEN
AT BUILD TIME by a separate crate (cranelift-assembler-x64-meta) from
instruction descriptions. So there are two things we could transpile:

  the generator   ordinary hand-written Rust: traits, iterators,
                  string building, file IO. Transpiling it would let
                  our Python regenerate the vocabulary for any future
                  Cranelift. But it needs a large transpiler grammar,
                  and large grammars are where inference creeps back
                  in — the exact failure this tool exists to prevent.

  the output      the 9.3 MB file the generator produced. Its grammar
                  is 12 node kinds (survey: 1071 encode fns, 14876
                  lines, zero unclassified) because the generator
                  already flattened every decision into longhand.

We take the output. Same rule as ISLE: cut from generated code, never
from the DSL that generates it. The cost is that the result is pinned
to one Cranelift version — which is not a defect here but the point:
the emitted Python is PseudoCoup's STABILITY LAYER. It changes when we
choose to re-run this tool, not when upstream moves.

Determinism: no timestamps in output. Re-running on the same input
produces byte-identical files, so `git diff` shows real changes only.

Usage:  python3 transpile_vocab.py <path-to-assembler.rs> [outdir]
"""

import hashlib
import pathlib
import re
import sys
from collections import defaultdict

TRANSPILER_VERSION = "1"

# ---------------------------------------------------------------
# node transpilers: one per Rust construct in the surveyed grammar
# ---------------------------------------------------------------

INT_LIT = re.compile(r'^(0x[0-9a-fA-F]+|\d+)(_[iu]\d+)?$')


def rhs(expr: str) -> str:
    """Transpile an expression node."""
    e = expr.strip()
    if e.startswith('&'):
        e = e[1:]                       # &x -> x (borrow is a no-op)
    if e == 'true':
        return 'True'
    if e == 'false':
        return 'False'
    if e == 'None':
        return 'None'
    m = INT_LIT.match(e)
    if m:
        return m.group(1)               # 0x8_u8 -> 0x8
    m = re.match(r'^Some\((.*)\)$', e)
    if m:
        return rhs(m.group(1))
    # crate::custom::encode::f(..) -> custom_encode.f(..)
    # (the generated file's escape hatch into hand-written custom.rs;
    #  those functions live in the support layer, second grammar)
    e = re.sub(r'\bcrate::custom::encode::', 'custom_encode.', e)
    # Type::assoc_fn(args) -> Type.assoc_fn(args)
    e = re.sub(r'\b([A-Z]\w*)::', r'\1.', e)
    if '::' in e:
        raise Unsupported(f"unhandled path expression: {e}")
    # strip numeric suffixes inside call args
    e = re.sub(r'\b(0x[0-9a-fA-F]+|\d+)_[iu]\d+\b', r'\1', e)
    return e


class Unsupported(Exception):
    pass


def transpile_body(body: str, out, indent="        "):
    """Transpile an encode() body. Brace depth -> Python indent."""
    depth = 0
    for raw in body.splitlines():
        line = re.sub(r'\s*//.*$', '', raw).strip()
        if not line:
            continue
        pad = indent + "    " * depth

        if line == '}':
            depth -= 1
            continue

        # if let Enum::Variant(binding) = expr {
        m = re.match(r'^if let (\w+)::(\w+)\((\w+)\) = (.+?) \{$', line)
        if m:
            _enum, variant, binding, expr = m.groups()
            src = rhs(expr)
            if variant == 'Some':
                out.append(f"{pad}{binding} = {src}")
                out.append(f"{pad}if {binding} is not None:")
            else:
                out.append(f"{pad}if isinstance({src}, {variant}):")
                out.append(f"{pad}    {binding} = {src}")
            depth += 1
            continue

        # if let Some(binding) = expr {
        m = re.match(r'^if let Some\((\w+)\) = (.+?) \{$', line)
        if m:
            binding, expr = m.groups()
            out.append(f"{pad}{binding} = {rhs(expr)}")
            out.append(f"{pad}if {binding} is not None:")
            depth += 1
            continue

        # let [mut] name[: Type] = expr;
        m = re.match(r'^let (?:mut )?(\w+)(?:\s*:\s*[^=]+)?\s*=\s*(.+);$',
                     line)
        if m:
            name, expr = m.groups()
            out.append(f"{pad}{name} = {rhs(expr)}")
            continue

        # statement call:  target(args);
        m = re.match(r'^(.+);$', line)
        if m:
            out.append(f"{pad}{rhs(m.group(1))}")
            continue

        raise Unsupported(line)


# ---------------------------------------------------------------
# structure extraction
# ---------------------------------------------------------------

# Two declaration forms in the generated file:
#   pub struct NAME<R> where R: Registers {..}   register operands
#   pub struct NAME  {..}                        register-free
#                                                (jumps, hlt, int3, callq_d)
STRUCT_RE = re.compile(
    r'pub struct (\w+)(<R> where R: Registers)? +\{(.*?)\n\}', re.S)
FIELD_RE = re.compile(r'pub (\w+):')


def extract(src: str):
    """Yield (name, fields, mnemonic, encode_body) per instruction."""
    for m in STRUCT_RE.finditer(src):
        name, generic, fieldblock = m.group(1), m.group(2), m.group(3)
        fields = FIELD_RE.findall(re.sub(r'\s*//.*', '', fieldblock))

        impl_pat = (r'impl<R: Registers> ' + re.escape(name) + r'<R> \{(.*?)\n\}\n'
                    if generic else
                    r'impl ' + re.escape(name) + r' \{(.*?)\n\}\n')
        impl = re.search(impl_pat, src[m.end():], re.S)
        if not impl:
            continue
        block = impl.group(1)

        mn = re.search(r'Cow::Borrowed\("([^"]+)"\)', block)
        enc = re.search(
            r'pub fn encode\(&self, buf: &mut impl CodeSink\) \{(.*?)\n    \}',
            block, re.S)
        if not enc:
            continue
        yield name, fields, (mn.group(1) if mn else name), enc.group(1)


HEADER = '''"""GENERATED — do not edit. Regenerate with transpile_vocab.py.

source        {src_name}
source sha256 {sha}
cranelift     {version}
transpiler    v{tv}

Deterministic: same input -> byte-identical output.
"""

from vocab_support import *      # noqa: F401,F403
'''


def emit_class(name, fields, mnemonic, body):
    out = []
    out.append(f"class {name}:")
    out.append(f'    """{mnemonic}"""')
    out.append(f"    MNEMONIC = {mnemonic!r}")
    out.append(f"    FIELDS = {tuple(fields)!r}")
    out.append("")
    args = ", ".join(fields)
    out.append(f"    def __init__(self, {args}):" if fields
               else "    def __init__(self):")
    for f in fields:
        out.append(f"        self.{f} = {f}")
    if not fields:
        out.append("        pass")
    out.append("")
    out.append("    def encode(self, buf):")
    start = len(out)
    transpile_body(body, out)
    if len(out) == start:
        out.append("        pass")
    out.append("")
    return "\n".join(out)


def main(src_path, outdir="pc_vocab"):
    src_file = pathlib.Path(src_path)
    src = src_file.read_text()
    sha = hashlib.sha256(src.encode()).hexdigest()
    version = re.search(r'cranelift-assembler-x64-([\d.]+)',
                        str(src_file.resolve()))
    version = version.group(1) if version else "unknown"

    out = pathlib.Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    groups = defaultdict(list)
    registry, failed = [], []
    for name, fields, mnemonic, body in extract(src):
        try:
            groups[name[0].lower()].append(emit_class(name, fields,
                                                      mnemonic, body))
            registry.append(name)
        except Unsupported as e:
            failed.append((name, str(e)))

    hdr = HEADER.format(src_name=src_file.name, sha=sha, version=version,
                        tv=TRANSPILER_VERSION)
    for letter, classes in sorted(groups.items()):
        (out / f"{letter}.py").write_text(hdr + "\n" + "\n".join(classes))

    init = [hdr, "", "INSTRUCTIONS = {}", ""]
    for letter in sorted(groups):
        init.append(f"from .{letter} import *          # noqa: F401,F403")
    init.append("")
    init.append("import sys as _sys")
    init.append("_mod = _sys.modules[__name__]")
    init.append(f"for _n in {sorted(registry)!r}:")
    init.append("    INSTRUCTIONS[_n] = getattr(_mod, _n)")
    (out / "__init__.py").write_text("\n".join(init) + "\n")

    print(f"transpiled {len(registry)} instructions -> {out}/"
          f" ({len(groups)} modules)")
    if failed:
        print(f"UNSUPPORTED NODES: {len(failed)}")
        for n, l in failed[:10]:
            print(f"  {n}: {l[:70]}")
    return len(failed)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1],
                          sys.argv[2] if len(sys.argv) > 2 else "pc_vocab"))
