"""Shared instruction-field parsing and operand-choice logic.

Used by BOTH gen_rust_harness.py (emits Rust) and run_python_side.py (drives
pc_vocab) so that the two generators pick IDENTICAL operand values for the
same instruction + operand key. This is the crux of the differential test:
if both sides build "the same instruction" out of the same field values,
any byte-level mismatch is either a transpiler bug or a genuine encoding
divergence.

Parsing strategy
-----------------
We do NOT write a Rust parser. `assembler.rs` is machine generated in a very
regular shape:

    pub struct NAME<R> where R: Registers {
        pub field1: Type1,
        ...
    }
    impl<R: Registers> NAME<R> {
        pub fn new(field1: impl Into<Type1>, ...) -> Self { ... }
        ...
    }

or, for instructions with no register-generic parameter (jumps, zo-form
instructions, etc.):

    pub struct NAME  {
        pub field1: Type1,
    }
    impl NAME {
        pub fn new(field1: impl Into<Type1>) -> Self { ... }
    }

We locate each `pub struct NAME` occurrence (in enum-variant order, which is
also file order) and scan forward to the next `pub struct` to get that
instruction's private text chunk. Within the chunk we regex out the
`pub fn new(...) -> Self {` parameter list, split it on top-level commas
(respecting `<...>` nesting), and classify each `name: TYPE` (or
`name: impl Into<TYPE>`) pair into an OperandKind.

Field type -> OperandKind mapping (from crate source, cranelift-assembler-x64
0.134.2):

    Gpr<R>                              -> gpr
    GprMem<R, R>                        -> gprmem
    Xmm<R>                              -> xmm
    XmmMem<R, R>                        -> xmmmem
    Fixed<R, { gpr::enc::RAX }>         -> fixed (reg=0)
    Fixed<R, { gpr::enc::RCX }>         -> fixed (reg=1)
    Fixed<R, { gpr::enc::RDX }>         -> fixed (reg=2)
    Fixed<R, { gpr::enc::RBX }>         -> fixed (reg=3)
    Fixed<R, { xmm::enc::XMM0 }>        -> fixed_xmm (reg=0)
    Imm8 / Simm8                        -> imm8 / simm8   (1 byte)
    Imm16                               -> imm16          (2 bytes)
    Imm32 / Simm32                      -> imm32 / simm32 (4 bytes)
    Imm64                               -> imm64          (8 bytes)
    TrapCode                            -> trap (unused value; GPR path
                                                  never reads it)
    Amode<R>                            -> UNSUPPORTED (bare memory operand;
                                                  no GprMem/XmmMem wrapper to
                                                  fall back to a register
                                                  choice) -> instruction is
                                                  skipped entirely.

Anything else observed is also treated as UNSUPPORTED and the instruction is
skipped (recorded with the literal unrecognized type string as the reason).
"""

import re
from collections import OrderedDict

GPR_FIXED_ENC = {
    "gpr::enc::RAX": 0,
    "gpr::enc::RCX": 1,
    "gpr::enc::RDX": 2,
    "gpr::enc::RBX": 3,
}
XMM_FIXED_ENC = {
    "xmm::enc::XMM0": 0,
}

# Register encodings, x86-64 hardware numbering.
RAX, RCX, RDX, RBX, RSP, RBP, RSI, RDI = range(8)
R8, R9, R10, R11, R12, R13, R14, R15 = range(8, 16)

OPERAND_KEYS = ("low", "r14")

# Cycling pools of GPR/XMM encodings used to fill successive gpr/gprmem or
# xmm/xmmmem fields within one instruction. "low" never needs a REX.B/.R/.X
# bit; "r14" forces REX.B (and friends) on every register-carrying field so
# the REX-prefix computation is exercised on both sides.
_LOW_GPR_POOL = [RAX, RSI, RDX, RCX, RBX, RBP, RDI]
_HIGH_GPR_POOL = [R14, R15, R13, R12, R11, R10, R9, R8]
_LOW_XMM_POOL = [0, 1, 2, 3, 4, 5, 6, 7]
_HIGH_XMM_POOL = [14, 15, 13, 12, 11, 10, 9, 8]

IMM_FIXED_VALUES = {
    "imm8": 0x12,
    "simm8": 0x12,
    "imm16": 0x1234,
    "imm32": 0x1234,
    "simm32": 0x1234,
    "imm64": 0x123456789A,
}
IMM_WIDTH_BYTES = {
    "imm8": 1, "simm8": 1,
    "imm16": 2,
    "imm32": 4, "simm32": 4,
    "imm64": 8,
}


class Field:
    __slots__ = ("name", "kind", "fixed_reg", "raw_type")

    def __init__(self, name, kind, fixed_reg=None, raw_type=""):
        self.name = name
        self.kind = kind
        self.fixed_reg = fixed_reg
        self.raw_type = raw_type

    def __repr__(self):
        return f"Field({self.name!r}, {self.kind!r})"


class Instruction:
    __slots__ = ("name", "mnemonic", "generic", "fields", "skip_reason")

    def __init__(self, name, mnemonic, generic):
        self.name = name
        self.mnemonic = mnemonic
        self.generic = generic
        self.fields = []
        self.skip_reason = None

    def __repr__(self):
        return f"Instruction({self.name!r}, fields={self.fields!r})"


def _split_top_level_commas(s):
    depth = 0
    cur = ""
    parts = []
    for ch in s:
        if ch in "<(":
            depth += 1
        elif ch in ">)":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


def _classify(fname, raw_type):
    ty = re.sub(r"R::\w+", "R", raw_type).strip()

    if ty == "Gpr<R>":
        return Field(fname, "gpr", raw_type=raw_type)
    if ty == "GprMem<R, R>":
        return Field(fname, "gprmem", raw_type=raw_type)
    if ty == "Xmm<R>":
        return Field(fname, "xmm", raw_type=raw_type)
    if ty == "XmmMem<R, R>":
        return Field(fname, "xmmmem", raw_type=raw_type)
    if ty == "TrapCode":
        return Field(fname, "trap", raw_type=raw_type)
    if ty in ("Imm8",):
        return Field(fname, "imm8", raw_type=raw_type)
    if ty in ("Simm8",):
        return Field(fname, "simm8", raw_type=raw_type)
    if ty in ("Imm16",):
        return Field(fname, "imm16", raw_type=raw_type)
    if ty in ("Imm32",):
        return Field(fname, "imm32", raw_type=raw_type)
    if ty in ("Simm32",):
        return Field(fname, "simm32", raw_type=raw_type)
    if ty in ("Imm64",):
        return Field(fname, "imm64", raw_type=raw_type)

    m = re.match(r"Fixed<R, \{ (gpr::enc::\w+) \}>", ty)
    if m:
        return Field(fname, "fixed", fixed_reg=GPR_FIXED_ENC[m.group(1)],
                      raw_type=raw_type)
    m = re.match(r"Fixed<R, \{ (xmm::enc::\w+) \}>", ty)
    if m:
        return Field(fname, "fixed_xmm", fixed_reg=XMM_FIXED_ENC[m.group(1)],
                      raw_type=raw_type)

    if ty.startswith("Amode<"):
        return Field(fname, "amode", raw_type=raw_type)

    return Field(fname, "unknown", raw_type=raw_type)


def _enum_variant_order(text):
    m = re.search(r"pub enum Inst<R: Registers> \{(.*?)\n\}", text, re.S)
    body = m.group(1)
    return re.findall(r"^\s*(\w+)\(", body, re.M)


def parse_instructions(assembler_rs_path):
    """Parse assembler.rs and return an OrderedDict name -> Instruction.

    Every one of the 1071 enum variants gets an entry. Instructions whose
    field list can't be fully classified (Amode-only operands, or anything
    unrecognized) have `.skip_reason` set to a human-readable string;
    everything else has `.skip_reason is None` and a concrete `.fields`
    list ready to drive construction.
    """
    text = open(assembler_rs_path, "r").read()
    order = _enum_variant_order(text)

    # Byte offsets of every `pub struct NAME` declaration, in file order.
    struct_starts = [(m.start(), m.group(1))
                      for m in re.finditer(r"\npub struct (\w+)", text)]
    struct_starts.sort()
    name_to_chunk = {}
    for i, (start, name) in enumerate(struct_starts):
        end = struct_starts[i + 1][0] if i + 1 < len(struct_starts) else len(text)
        name_to_chunk[name] = text[start:end]

    result = OrderedDict()
    for name in order:
        chunk = name_to_chunk.get(name)
        inst = Instruction(name, mnemonic=None, generic="<R>" in (chunk or "")[:200])
        if chunk is None:
            inst.skip_reason = "no matching 'pub struct' found in assembler.rs"
            result[name] = inst
            continue

        mm = re.search(r'Cow::Borrowed\("([^"]*)"\)', chunk)
        inst.mnemonic = mm.group(1) if mm else name

        newm = re.search(r"pub fn new\((.*?)\) -> Self \{", chunk, re.S)
        if not newm:
            inst.skip_reason = "no 'pub fn new(...)' found (likely custom-encoded, e.g. nop_Nb)"
            result[name] = inst
            continue

        args = newm.group(1)
        parts = _split_top_level_commas(args)
        fields = []
        bad = []
        for p in parts:
            fm = re.match(r"(\w+):\s*impl Into<(.*)>$", p)
            if fm:
                fname, ty = fm.group(1), fm.group(2)
            else:
                fm2 = re.match(r"(\w+):\s*(.*)$", p)
                if not fm2:
                    bad.append(p)
                    continue
                fname, ty = fm2.group(1), fm2.group(2)
            field = _classify(fname, ty)
            if field.kind in ("amode", "unknown"):
                bad.append(f"{fname}: {ty}")
            fields.append(field)

        if bad:
            inst.skip_reason = "unsupported field type(s): " + "; ".join(bad)
        inst.fields = fields
        result[name] = inst

    return result


def build_operand_values(inst, key):
    """Return a list of (field, value) pairs for the given operand key.

    `value` semantics by field.kind:
      gpr, gprmem, xmm, xmmmem, fixed, fixed_xmm -> int register encoding (0-15)
      imm8/simm8/imm16/imm32/simm32/imm64        -> int immediate value
      trap                                       -> None (unused by either
                                                     side on the register-only
                                                     path we exercise)
    """
    assert inst.skip_reason is None, f"{inst.name} is not constructible: {inst.skip_reason}"
    assert key in OPERAND_KEYS

    gpr_pool = _LOW_GPR_POOL if key == "low" else _HIGH_GPR_POOL
    xmm_pool = _LOW_XMM_POOL if key == "low" else _HIGH_XMM_POOL
    gi = [0]
    xi = [0]

    def next_gpr():
        v = gpr_pool[gi[0] % len(gpr_pool)]
        gi[0] += 1
        return v

    def next_xmm():
        v = xmm_pool[xi[0] % len(xmm_pool)]
        xi[0] += 1
        return v

    out = []
    for f in inst.fields:
        if f.kind in ("gpr", "gprmem"):
            out.append((f, next_gpr()))
        elif f.kind in ("xmm", "xmmmem"):
            out.append((f, next_xmm()))
        elif f.kind in ("fixed",):
            out.append((f, f.fixed_reg))
        elif f.kind in ("fixed_xmm",):
            out.append((f, f.fixed_reg))
        elif f.kind in IMM_FIXED_VALUES:
            out.append((f, IMM_FIXED_VALUES[f.kind]))
        elif f.kind == "trap":
            out.append((f, None))
        else:
            raise AssertionError(f"unexpected field kind {f.kind!r} on constructible instruction")
    return out


def constructible_instructions(instructions):
    """Split into (ok_dict, skipped_dict) by skip_reason."""
    ok = OrderedDict()
    skipped = OrderedDict()
    for name, inst in instructions.items():
        if inst.skip_reason is None:
            ok[name] = inst
        else:
            skipped[name] = inst
    return ok, skipped
