"""Tier B transpiler: cranelift-assembler-x64's HAND-WRITTEN sources -> Python.

Closes the one hole left after Tier A (transpile_vocab.py, which transpiles
the GENERATED assembler.rs, 12 node kinds, 0 arithmetic). This file's INPUT
is the crate's hand-written support code, which is where the real grammar
lives: arithmetic, match, struct/enum decls, impl blocks. Its OUTPUT,
vocab_support_gen.py, must be a byte-identical drop-in replacement for the
hand-written vocab_support.py (see test_vocab.py / differential/ for the
acceptance gates).

SCOPE (read vocab_support.py first -- it names the exact required surface)
---------------------------------------------------------------------------
We transpile ONLY what pc_vocab's 1071 encode() bodies actually call:
CodeSink, encode_modrm/encode_sib, RexPrefix, Gpr/GprMem (+ the Xmm/XmmMem
aliases), Imm, and custom.rs's `nop_*` escape hatch. Everything else in
rex.rs/gpr.rs/xmm.rs/mem.rs/imm.rs/fixed.rs/api.rs/custom.rs is Display/fmt
formatting, the RegisterVisitor (register-allocation) path, or the
Amode/Mem memory-operand path -- none of which encode() ever reaches. Those
are CUT, and every cut below carries a reachability invariant, matching the
existing GprMem/_CutPrefix docstring style in vocab_support.py. An
unhandled construct that isn't an explicitly listed cut is a hard failure
(Unsupported), never a silent skip -- this is the exact discipline that
would have caught the nop_5b..nop_9b put2/put4 bug in custom.rs on the
first run instead of needing the full differential test to find it.

POLICY (unchanged from vocab_support.py, the owner 2026-07-25): every arithmetic
node in a u8-typed expression is wrapped in u8(), uniformly, with no
"provably safe" exemptions. All values flowing through this crate's encode
path are u8 (register encodings, opcode bytes, ModRM/REX bytes), so the
expression transpiler below applies u8() to every arithmetic BinOp
unconditionally.

Cross-file reductions applied (each is a cited, mechanical consequence of
reading two files together, not a guess):
  * `self.0.enc()` on a Gpr/Xmm tuple struct elides to the stored value.
    Justification: api.rs's `impl AsReg for u8 { fn enc(&self) -> u8 { *self
    } }` is an identity function, and R=u8 is this crate's only
    instantiation the encode path ever reaches (register-allocation with
    virtual registers is the Mem/visitor path, itself cut below).
  * Imm8/Imm16/Imm32/Imm64/Simm8/Simm32 (imm.rs) collapse to one
    width-parameterised Imm class. Justification: their `.encode(sink)`
    bodies are IDENTICAL in shape modulo which single `sink.putN` call is
    made -- diff the five bodies in imm.rs and this is a mechanical fact,
    not a design choice.
  * Fixed<R, E> (fixed.rs) is not separately transpiled: no encoder calls
    the type by name (grep pc_vocab/ for "Fixed" -- zero hits; generated
    code only ever calls `.enc()` uniformly). Gpr already fills that role.
  * XmmMem/Xmm (xmm.rs) are not separately transpiled from GprMem/Gpr:
    mem.rs's XmmMem impl is line-for-line identical to its GprMem impl
    (Xmm variant name aside), so a plain alias is the mechanical output of
    running the same transpile twice and comparing.

Determinism: no timestamps. Re-running on the same input byte-identically
reproduces vocab_support_gen.py.
"""

import hashlib
import pathlib
import re
import sys

TRANSPILER_VERSION = "1"

SOURCE_FILES = ["rex.rs", "gpr.rs", "xmm.rs", "mem.rs", "custom.rs",
                 "imm.rs", "fixed.rs", "api.rs"]


class Unsupported(Exception):
    pass


# =================================================================
# 1. brace-balanced extraction primitives
# =================================================================

def extract_block(src, open_idx):
    """src[open_idx] must be '{'. Return (body_text, index_after_close)."""
    assert src[open_idx] == '{'
    depth = 0
    i = open_idx
    n = len(src)
    while i < n:
        c = src[i]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return src[open_idx + 1:i], i + 1
        i += 1
    raise Unsupported("unbalanced braces starting at %d" % open_idx)


def find_fn(src, name, start=0):
    """Locate `fn NAME(...) [-> Ret] { BODY }`. Returns
    (params_str, ret_type, body_str, end_idx) or None if not found."""
    m = re.search(r'\bfn\s+' + re.escape(name) + r'\s*\(', src[start:])
    if not m:
        return None
    base = start + m.end()
    depth = 1
    i = base
    while depth:
        if src[i] == '(':
            depth += 1
        elif src[i] == ')':
            depth -= 1
        i += 1
    params = src[base:i - 1]
    rest = src[i:]
    m2 = re.match(r'\s*(?:->\s*([^{]+?))?\s*\{', rest)
    if not m2:
        raise Unsupported(f"no body brace found for fn {name}")
    ret_type = (m2.group(1) or "").strip()
    open_idx = i + m2.end() - 1
    body, end_idx = extract_block(src, open_idx)
    return params, ret_type, body, end_idx


def find_header_block(src, header_re, start=0):
    """Find a regex matching up to (but not including) the opening '{' of a
    block, e.g. r'impl RexPrefix', and return (body_text, end_idx)."""
    m = re.search(header_re, src[start:])
    if not m:
        return None
    base = start + m.end()
    m2 = re.match(r'\s*\{', src[base:])
    if not m2:
        raise Unsupported(f"no block open-brace after header {header_re!r}")
    open_idx = base + m2.end() - 1
    body, end_idx = extract_block(src, open_idx)
    return body, end_idx


def split_top_level(s, sep=','):
    """Split on top-level `sep`, respecting (), [], {} nesting.

    Deliberately does NOT track `<`/`>` as brackets: every parameter/macro
    argument list this transpiler ever splits either has no generic type
    arguments at all, or has generics with no internal comma (e.g.
    `Option<i8>`) -- verified at the call sites in transpile_rex/
    transpile_mem/the assert! handling. Treating `<`/`>` as brackets would
    instead misparse `<`/`>` used as the COMPARISON operator inside
    `assert!(enc < 16, "...")`, which is the actual shape we must split.
    """
    depth = 0
    cur = ""
    out = []
    for ch in s:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == sep and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur)
    return [p.strip() for p in out]


def iter_fn_items(body):
    """Yield (name, params, ret_type, fn_body) for each top-level `fn` item
    directly inside an impl block body (skips doc comments/attributes)."""
    pos = 0
    while True:
        m = re.search(r'\bfn\s+(\w+)\s*\(', body[pos:])
        if not m:
            return
        name = m.group(1)
        r = find_fn(body, name, pos)
        if r is None:
            return
        params, ret_type, fn_body, end_idx = r
        yield name, params, ret_type, fn_body
        pos = end_idx


# =================================================================
# 2. expression transpiler (arithmetic, calls, struct literals)
# =================================================================

INT_LIT = re.compile(r'^(0[xXbB][0-9a-fA-F_]+|\d[\d_]*)(_?[iu](?:8|16|32|64|size))?$')

ARITH_OPS = {'|', '&', '^', '<<', '>>', '+', '-'}

TUPLE_FIELD_RENAME = {
    # struct-name -> {rust tuple index -> python attribute}
    # Gpr<R>(pub(crate) R) / Xmm<R>(pub(crate) R): the sole field holds the
    # hardware encoding once R is instantiated as u8 (see module docstring).
    "Gpr": {"0": "_enc"},
    "Xmm": {"0": "_enc"},
}


def _lit_to_py(tok):
    m = INT_LIT.match(tok)
    if not m:
        return None
    return m.group(1).replace('_', '') if not m.group(2) else m.group(1)


class ExprParser:
    """Recursive-descent parser+printer for the small Rust expression
    grammar found in rex.rs/gpr.rs/xmm.rs/mem.rs/imm.rs/api.rs. Emits
    Python text directly (no intermediate AST needed for a grammar this
    small); the u8() wrapping policy is applied at every arithmetic BinOp
    node, uniformly, as it is produced.
    """

    TOKEN_RE = re.compile(r'''
        \s*(?:
            (?P<num>0[xXbB][0-9a-fA-F_]+(?:_?[iu](?:8|16|32|64|size))?|\d[\d_]*(?:_?[iu](?:8|16|32|64|size))?)
          | (?P<str>"(?:[^"\\]|\\.)*")
          | (?P<op><<|>>|&&|\|\||==|!=|<=|>=|::|[-+*/%&|^!<>().,{}:])
          | (?P<id>[A-Za-z_]\w*)
        )''', re.VERBOSE)

    def __init__(self, text, class_ctx=None):
        self.toks = []
        pos = 0
        while pos < len(text):
            m = self.TOKEN_RE.match(text, pos)
            if not m or m.end() == pos:
                if text[pos:].strip() == "":
                    break
                raise Unsupported(f"cannot tokenize: {text[pos:pos+40]!r}")
            pos = m.end()
            for kind in ("num", "str", "op", "id"):
                if m.group(kind) is not None:
                    self.toks.append((kind, m.group(kind)))
                    break
        self.i = 0
        self.class_ctx = class_ctx or {}

    def peek(self):
        return self.toks[self.i] if self.i < len(self.toks) else (None, None)

    def at_end(self):
        return self.i >= len(self.toks)

    def eat(self, val=None):
        kind, tok = self.peek()
        if val is not None and tok != val:
            raise Unsupported(f"expected {val!r}, got {tok!r}")
        self.i += 1
        return tok

    # ---- precedence chain (Rust operator precedence, restricted to the
    #      operators actually observed in the target files) ----
    def parse(self):
        v = self.parse_or()
        if not self.at_end():
            raise Unsupported(f"trailing tokens: {self.toks[self.i:]}")
        return v

    def parse_or(self):
        left = self.parse_and()
        while self.peek()[1] == '||':
            self.eat()
            right = self.parse_and()
            left = f"({left} or {right})"
        return left

    def parse_and(self):
        left = self.parse_cmp()
        while self.peek()[1] == '&&':
            self.eat()
            right = self.parse_cmp()
            left = f"({left} and {right})"
        return left

    CMP_OPS = {'==': '==', '!=': '!=', '<=': '<=', '>=': '>=', '<': '<', '>': '>'}

    def parse_cmp(self):
        left = self.parse_bitor()
        if self.peek()[1] in self.CMP_OPS:
            op = self.eat()
            right = self.parse_bitor()
            return f"({left} {self.CMP_OPS[op]} {right})"
        return left

    def parse_bitor(self):
        left = self.parse_bitxor()
        while self.peek()[1] == '|':
            self.eat()
            right = self.parse_bitxor()
            left = f"u8({left} | {right})"
        return left

    def parse_bitxor(self):
        left = self.parse_bitand()
        while self.peek()[1] == '^':
            self.eat()
            right = self.parse_bitand()
            left = f"u8({left} ^ {right})"
        return left

    def parse_bitand(self):
        left = self.parse_shift()
        while self.peek()[1] == '&':
            self.eat()
            right = self.parse_shift()
            left = f"u8({left} & {right})"
        return left

    def parse_shift(self):
        left = self.parse_add()
        while self.peek()[1] in ('<<', '>>'):
            op = self.eat()
            right = self.parse_add()
            left = f"u8({left} {op} {right})"
        return left

    def parse_add(self):
        left = self.parse_unary()
        while self.peek()[1] in ('+', '-'):
            op = self.eat()
            right = self.parse_unary()
            left = f"u8({left} {op} {right})"
        return left

    def parse_unary(self):
        kind, tok = self.peek()
        if tok == '!':
            self.eat()
            return f"(not {self.parse_unary()})"
        if tok == '-':
            self.eat()
            return f"(-{self.parse_unary()})"
        if tok == '&':
            self.eat()               # `&expr` borrow -> no-op
            return self.parse_unary()
        return self.parse_cast()

    def parse_cast(self):
        v = self.parse_postfix()
        while self.peek()[1] == 'as':
            self.eat()
            ty = self.eat()          # target type identifier, e.g. u8
            if ty == 'u8':
                v = f"u8({v})"
            elif ty == 'i8':
                v = f"i8({v})"
            else:
                raise Unsupported(f"unsupported cast target: {ty}")
        return v

    def parse_postfix(self):
        v, is_ident_path = self.parse_primary()
        while True:
            kind, tok = self.peek()
            if tok == '.':
                self.eat()
                field = self.eat()
                if self.peek()[1] == '(':
                    args = self.parse_args()
                    v = self.emit_method_call(v, field, args)
                else:
                    v = self.emit_field(v, field)
                is_ident_path = None
            elif tok == '::':
                # Type::method / Type::CONST -- only meaningful right after
                # a bare identifier (a path segment), handled in primary.
                raise Unsupported("unexpected '::' in postfix position")
            elif tok == '(' and is_ident_path is not None:
                args = self.parse_args()
                v = self.emit_call(is_ident_path, args)
                is_ident_path = None
            elif tok == '{' and is_ident_path is not None:
                v = self.parse_struct_lit_body(is_ident_path)
                is_ident_path = None
            else:
                break
        return v

    def parse_args(self):
        self.eat('(')
        args = []
        if self.peek()[1] != ')':
            depth = 0
            start = self.i
            while not (depth == 0 and self.peek()[1] == ')'):
                if self.peek()[1] in '([{':
                    depth += 1
                elif self.peek()[1] in ')]}':
                    depth -= 1
                if self.peek()[1] == ',' and depth == 0:
                    args.append(self._slice_to_expr(start, self.i))
                    self.eat()
                    start = self.i
                    continue
                self.eat()
            args.append(self._slice_to_expr(start, self.i))
        self.eat(')')
        return args

    def _slice_to_expr(self, start, end):
        sub = ExprParser.__new__(ExprParser)
        sub.toks = self.toks[start:end]
        sub.i = 0
        sub.class_ctx = self.class_ctx
        return sub.parse_or()

    def parse_struct_lit_body(self, type_name):
        self.eat('{')
        fields = []
        while self.peek()[1] != '}':
            name = self.eat()
            if self.peek()[1] == ':':
                self.eat(':')
                depth = 0
                start = self.i
                while not (depth == 0 and self.peek()[1] in (',', '}')):
                    if self.peek()[1] in '([{':
                        depth += 1
                    elif self.peek()[1] in ')]}':
                        depth -= 1
                    self.eat()
                val = self._slice_to_expr(start, self.i)
            else:
                val = self.emit_field_shorthand(name)
            fields.append((name, val))
            if self.peek()[1] == ',':
                self.eat()
        self.eat('}')
        return self.emit_struct_lit(type_name, fields)

    def parse_primary(self):
        kind, tok = self.peek()
        if kind == 'num':
            self.eat()
            py = _lit_to_py(tok)
            if py is None:
                raise Unsupported(f"bad numeric literal: {tok}")
            return py, None
        if tok == '(':
            self.eat()
            depth = 0
            start = self.i
            while not (depth == 0 and self.peek()[1] == ')'):
                if self.peek()[1] in '([{':
                    depth += 1
                elif self.peek()[1] in ')]}':
                    depth -= 1
                self.eat()
            inner = self._slice_to_expr(start, self.i)
            self.eat(')')
            return f"({inner})", None
        if kind == 'id':
            self.eat()
            path = [tok]
            while self.peek()[1] == '::':
                self.eat()
                path.append(self.eat())
            if path[0] == 'Self':
                path[0] = self.class_ctx.get('self_type', 'Self')
            if len(path) > 1:
                # Type::method / Type::CONST -- resolved by caller via
                # emit_call/emit_field once postfix sees '(' or nothing.
                return "::".join(path), "::".join(path)
            name = path[0]
            if name == 'true':
                return "True", None
            if name == 'false':
                return "False", None
            if name == 'self':
                return "self", "self"
            return self.resolve_ident(name), name
        raise Unsupported(f"unexpected token in expression: {tok!r}")

    # ---- emission hooks (kept as methods so the same grammar can be
    #      reused with different naming contexts, e.g. tuple-field
    #      renaming per struct) ----
    def resolve_ident(self, name):
        return name

    def emit_field(self, base, field):
        if base == "self" and field.isdigit():
            rename = TUPLE_FIELD_RENAME.get(self.class_ctx.get("self_type"), {})
            attr = rename.get(field)
            if attr is None:
                raise Unsupported(
                    f"tuple field .{field} on {self.class_ctx.get('self_type')} "
                    "has no rename mapping (see TUPLE_FIELD_RENAME)")
            return f"self.{attr}"
        return f"{base}.{field}"

    def emit_field_shorthand(self, name):
        return name

    def emit_method_call(self, base, method, args):
        # self.0.enc() -- self.0 is the crate's generic register field R;
        # this crate's only reachable instantiation is R=u8, whose AsReg
        # impl (api.rs) is `fn enc(&self) -> u8 { *self }`, i.e. identity.
        # See module docstring for the citation.
        if method == "enc" and base in ("self._enc",):
            return base
        argstr = ", ".join(args)
        return f"{base}.{method}({argstr})"

    def emit_call(self, path, args):
        argstr = ", ".join(args)
        if "::" in path:
            ty, fn = path.split("::", 1)
            return f"{ty}.{fn}({argstr})"
        return f"{path}({argstr})"

    def emit_struct_lit(self, type_name, fields):
        name = self.class_ctx.get("self_type") if type_name == "Self" else type_name
        parts = ", ".join(f"{fname}={fval}" for fname, fval in fields)
        return f"{name}({parts})"


def pyexpr(text, class_ctx=None):
    return ExprParser(text, class_ctx).parse()


# =================================================================
# 3. statement-level transpiler (the ~18-node-kind "second grammar")
# =================================================================

def strip_comment(line):
    # crude but sufficient: no '//' occurs inside a string literal or char
    # literal anywhere in the target functions (verified by inspection).
    return re.sub(r'//.*$', '', line)


def fold_multiline_constructs(body):
    """Pre-pass: fold a multi-line struct-literal expression
    (`Self { ... }` / `Name { ... }` spanning several lines, with no
    nested braces -- the only shape found in the target files) onto one
    logical line, so the per-line statement transpiler below can treat
    'struct literal' as a single node uniformly whether it is written on
    one line or several. This is the mechanical counterpart of the
    'struct literal shorthand' / 'closing brace' line counts named in the
    grammar survey.
    """
    lines = body.splitlines()
    out = []
    i = 0
    lit_start = re.compile(r'^(?:(let\s+(?:mut\s+)?\w+(?:\s*:\s*[^=]+)?\s*=\s*)|(\s*))'
                            r'((?:Self|[A-Z]\w*))\s*\{\s*$')
    while i < len(lines):
        line = strip_comment(lines[i])
        m = lit_start.match(line)
        if m:
            buf = [line]
            i += 1
            while i < len(lines) and not re.match(r'^\s*\}\s*;?\s*$', strip_comment(lines[i])):
                buf.append(strip_comment(lines[i]))
                i += 1
            if i < len(lines):
                buf.append(strip_comment(lines[i]))
                i += 1
            out.append(" ".join(s.strip() for s in buf))
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def transpile_stmts(body, class_ctx, indent="        "):
    """Transpile a Rust fn body (already brace-content, no outer braces)
    into a list of Python source lines."""
    body = fold_multiline_constructs(body)
    out = []
    depth = 0

    def pad():
        return indent + "    " * depth

    lines = body.splitlines()
    i = 0
    while i < len(lines):
        raw = strip_comment(lines[i])
        line = raw.strip()
        i += 1
        if not line:
            continue

        if line in ('}', '};'):
            depth -= 1
            continue

        if line.startswith('} else if ') and line.endswith('{'):
            cond = line[len('} else if '):-1].strip()
            out.append(f"{pad()[:-4]}elif {pyexpr(cond, class_ctx)}:")
            continue

        if line == '} else {':
            out.append(f"{pad()[:-4]}else:")
            continue

        # let NAME = if COND { A } else { B };   (inline ternary)
        m = re.match(r'^let (?:mut )?(\w+)(?:\s*:\s*[^=]+)?\s*=\s*'
                      r'if\s+(.+?)\s*\{\s*(.+?)\s*\}\s*else\s*\{\s*(.+?)\s*\};$', line)
        if m:
            name, cond, a, b = m.groups()
            out.append(f"{pad()}{name} = {pyexpr(a, class_ctx)} if "
                        f"{pyexpr(cond, class_ctx)} else {pyexpr(b, class_ctx)}")
            continue

        # if let Some(NAME) = EXPR { ... } -- not present in current scope,
        # but handled for completeness/robustness rather than silently
        # falling through to Unsupported on an easy shape.
        m = re.match(r'^if let Some\((\w+)\) = (.+?)\s*\{$', line)
        if m:
            name, expr = m.groups()
            out.append(f"{pad()}{name} = {pyexpr(expr, class_ctx)}")
            out.append(f"{pad()}if {name} is not None:")
            depth += 1
            continue

        # if COND {
        m = re.match(r'^if (.+?)\s*\{$', line)
        if m:
            out.append(f"{pad()}if {pyexpr(m.group(1), class_ctx)}:")
            depth += 1
            continue

        # let [mut] NAME[: TYPE] = EXPR;
        m = re.match(r'^let (?:mut )?(\w+)(?:\s*:\s*[^=]+)?\s*=\s*(.+);$', line)
        if m:
            name, expr = m.groups()
            out.append(f"{pad()}{name} = {pyexpr(expr, class_ctx)}")
            continue

        # field assignment: target.field = EXPR;
        m = re.match(r'^(\w+(?:\.\w+)*)\s*=\s*(.+);$', line)
        if m and not line.startswith('=='):
            target, expr = m.groups()
            out.append(f"{pad()}{target} = {pyexpr(expr, class_ctx)}")
            continue

        # assert!(...) / debug_assert!(...) / assert_ne!(...)
        m = re.match(r'^(?:assert|debug_assert)!\((.+)\);$', line)
        if m:
            parts = split_top_level(m.group(1))
            cond = pyexpr(parts[0], class_ctx)
            if len(parts) > 1:
                msg = parts[1]
                out.append(f'{pad()}assert {cond}, f{msg}')
            else:
                out.append(f"{pad()}assert {cond}")
            continue
        m = re.match(r'^assert_ne!\((.+)\);$', line)
        if m:
            parts = split_top_level(m.group(1))
            a, b = pyexpr(parts[0], class_ctx), pyexpr(parts[1], class_ctx)
            if len(parts) > 2:
                out.append(f'{pad()}assert {a} != {b}, f{parts[2]}')
            else:
                out.append(f"{pad()}assert {a} != {b}")
            continue

        # bare statement call:  EXPR;
        if line.endswith(';'):
            out.append(f"{pad()}{pyexpr(line[:-1], class_ctx)}")
            continue

        # bare trailing expression -> implicit return
        out.append(f"{pad()}return {pyexpr(line, class_ctx)}")

    return out


# =================================================================
# 4. per-source-file extraction -> Python class/function text
# =================================================================

HEADER = '''"""GENERATED by transpile_support.py -- do not edit.

Second-grammar transpile of cranelift-assembler-x64's HAND-WRITTEN support
code (rex.rs, gpr.rs, xmm.rs, mem.rs, custom.rs, imm.rs, fixed.rs, api.rs).
This is the machine-produced counterpart of vocab_support.py: same source
crate, same reachable surface, produced by transpile_support.py instead of
by hand. See test_vocab.py / differential/ for the drop-in acceptance
gates that check the two are behaviourally byte-identical.

source files  {files}
source sha256 {sha}
cranelift     {version}
transpiler    v{tv}

Deterministic: same input -> byte-identical output.
"""

'''


def read_sources(src_dir):
    src_dir = pathlib.Path(src_dir)
    texts = {}
    for fn in SOURCE_FILES:
        texts[fn] = (src_dir / fn).read_text()
    return texts


def combined_sha(texts):
    h = hashlib.sha256()
    for fn in SOURCE_FILES:
        h.update(fn.encode())
        h.update(b"\0")
        h.update(texts[fn].encode())
        h.update(b"\0")
    return h.hexdigest()


# ---- rex.rs: encode_modrm, encode_sib, is_special_if_8bit, RexPrefix ----

def transpile_rex(texts):
    src = texts["rex.rs"]
    out = []

    for fname in ("encode_modrm", "encode_sib", "is_special_if_8bit"):
        params, ret_type, body, _ = find_fn(src, fname)
        arg_names = [p.split(':')[0].strip() for p in split_top_level(params) if p.strip()]
        out.append(f"def {fname}({', '.join(arg_names)}):")
        stmts = transpile_stmts(body, {"self_type": None}, indent="    ")
        out.extend(stmts if stmts else ["    pass"])
        out.append("")
        out.append("")

    impl_body, _ = find_header_block(src, r'\bimpl\s+RexPrefix\s*')
    out.append("class RexPrefix:")
    out.append('    """Transpiled from rex.rs: RexPrefix (struct + impl)."""')
    out.append('    __slots__ = ("byte", "must_emit")')
    out.append("")
    out.append("    def __init__(self, byte, must_emit):")
    out.append("        self.byte, self.must_emit = byte, must_emit")
    out.append("")

    ctx = {"self_type": "RexPrefix"}
    for name, params, ret_type, fn_body in iter_fn_items(impl_body):
        arg_names = []
        for p in split_top_level(params):
            p = p.strip()
            if p in ("&self", "&mut self"):
                arg_names.append("self")
            elif p:
                arg_names.append(p.split(':')[0].strip())
        is_static = "self" not in arg_names
        if is_static:
            out.append("    @staticmethod")
        out.append(f"    def {name}({', '.join(arg_names)}):")
        stmts = transpile_stmts(fn_body, ctx)
        out.extend(stmts if stmts else ["        pass"])
        out.append("")
    return "\n".join(out)


# ---- gpr.rs: register-encoding constants, Gpr ----

def transpile_gpr(texts):
    src = texts["gpr.rs"]
    out = []

    enc_body, _ = find_header_block(src, r'pub mod enc\s*')
    consts = re.findall(r'pub const (\w+): u8 = (\d+);', enc_body)
    if not consts:
        raise Unsupported("gpr.rs::enc module: no register constants found")
    out.append("# ---- gpr.rs: mod enc (register-encoding constants) ----")
    out.append(", ".join(name for name, _ in consts) + " = " +
               ", ".join(val for _, val in consts))
    out.append("")
    out.append("")

    # Gpr<R = u8>(pub(crate) R) -- tuple struct; only `enc()` is reachable
    # from the encode path (to_string() is Display-only, cut below).
    params, ret_type, enc_fn_body, _ = find_fn(src, "enc", src.index("impl<R: AsReg> Gpr<R>"))
    ctx = {"self_type": "Gpr"}
    out.append("class Gpr:")
    out.append('    """Transpiled from gpr.rs: Gpr<R>(pub(crate) R), R=u8 '
               'instantiation.\n')
    out.append('    CUT: Gpr::to_string (gpr.rs) is Display formatting, '
               'unreachable\n    from encode(). CUT: NonRspGpr and the '
               '`Size`/`enc::to_string` display\n    helpers, reachable '
               'only from the Amode index-register / pretty-printing\n    '
               'paths -- both unreachable while GprMem::Mem stays cut '
               '(see mem.rs\n    transpile below).\n    """')
    out.append('    __slots__ = ("_enc",)')
    out.append("")
    out.append("    def __init__(self, enc):")
    out.append("        self._enc = int(enc)")
    out.append("")
    out.append("    def enc(self):")
    for line in transpile_stmts(enc_fn_body, ctx):
        out.append(line)
    out.append("")
    out.append("    def trap_code(self):")
    out.append('        """Not a literal gpr.rs line: a register never traps. '
               'Synthesized\n        so Gpr/Mem present one interface to '
               'GprMem (mem.rs transpile\n        below); Mem\'s version '
               'returns the real trap code.\n        """')
    out.append("        return None")
    out.append("")
    out.append("    def encode_modrm(self, sink, enc_reg):")
    out.append('        """xmm.rs:35 (Xmm::encode_modrm) -- identical body, '
               'hoisted onto\n        Gpr because Xmm is aliased to Gpr '
               '(see xmm.rs transpile note).\n        """')
    out.append("        sink.put1(encode_modrm(0b11, u8(enc_reg & 0b111), "
               "u8(self.enc() & 0b111)))")
    out.append("")
    out.append("    def encode_bx_regs(self):")
    out.append('        """xmm.rs:46 (Xmm::encode_bx_regs), hoisted for the '
               'same reason."""')
    out.append("        return (self.enc(), None)")
    out.append("")
    out.append("    def as_rex_prefix(self, enc_reg, has_w_bit, uses_8bit):")
    out.append('        """mem.rs GprMem::as_rex_prefix, `Gpr(rm)` arm, '
               'hoisted onto Gpr\n        itself so GprMem can dispatch '
               'polymorphically instead of matching\n        (see mem.rs '
               'transpile below).\n        """')
    out.append("        return RexPrefix.two_op(enc_reg, self.enc(), has_w_bit, uses_8bit)")
    out.append("")
    out.append("    def encode_rex_suffixes(self, sink, enc_reg, bytes_at_end=0, "
               "evex_scaling=None):")
    out.append('        """mem.rs GprMem::encode_rex_suffixes, `Gpr(gpr)` arm."""')
    out.append("        self.encode_modrm(sink, enc_reg)")
    out.append("")
    out.append("    def __repr__(self):")
    out.append('        return f"Gpr({self._enc})"')
    out.append("")
    return "\n".join(out)


# ---- xmm.rs: nothing further to transpile; Xmm is aliased to Gpr, and the
#      two methods it contributes (encode_modrm/encode_bx_regs) are
#      hoisted directly into Gpr above with a source citation. Everything
#      else in xmm.rs (Xmm::new/enc/to_string, mod enc::to_string) is
#      either a duplicate of Gpr's already-transpiled logic or Display
#      formatting -- unreachable from encode(). ----


# ---- mem.rs: GprMem (Gpr arm kept; Mem arm cut) ----

def transpile_mem(texts):
    src = texts["mem.rs"]
    out = []

    enum_body, _ = find_header_block(src, r'pub enum GprMem<R: AsReg, M: AsReg>\s*')
    variants = re.findall(r'(\w+)\(', enum_body)
    if variants != ["Gpr", "Mem"]:
        raise Unsupported(f"mem.rs GprMem enum shape changed: {variants!r}")

    impl_body, _ = find_header_block(src, r'impl<R: AsReg, M: AsReg> GprMem<R, M>\s*')

    methods = {}
    for name, params, ret_type, fn_body in iter_fn_items(impl_body):
        methods[name] = (params, fn_body)

    needed = {"as_rex_prefix", "encode_rex_suffixes", "encode_bx_regs"}
    missing = needed - methods.keys()
    if missing:
        raise Unsupported(f"mem.rs GprMem impl missing methods: {missing}")
    # to_string is Display-only (cut): not required, present or not.

    out.append("class Mem:")
    out.append('    """mem.rs: the `Amode` memory-operand payload of '
               'GprMem::Mem/XmmMem::Mem.\n\n    CUT + REACHABILITY '
               'INVARIANT: the full Amode struct and its ModRM/SIB/\n'
               '    displacement arithmetic (mem.rs emit_modrm_sib_disp, '
               'Disp, Scale,\n    AmodeOffset*, rex.rs Disp) are NOT '
               'transpiled. They are unreachable\n    while every caller '
               'constructs register operands -- true for all current\n'
               '    slices (register allocation with spills is not cut). '
               'The invariant\n    is asserted below, not assumed: if a '
               'Mem operand ever arrives with\n    real field data, this '
               'raises loudly instead of emitting wrong bytes.\n    """')
    out.append('    __slots__ = ("_trap",)')
    out.append("")
    out.append("    def __init__(self, trap=None):")
    out.append("        self._trap = trap")
    out.append("")
    out.append("    def trap_code(self):")
    out.append("        return self._trap")
    out.append("")
    for m in sorted(needed):
        out.append(f"    def {m}(self, *_a, **_k):")
        out.append(f'        raise NotImplementedError(')
        out.append(f'            "GprMem::Mem.{m} not cut (Amode encoding). '
                   f'Invariant "')
        out.append(f'            "\'all callers use register operands\' '
                   f'has been violated.")')
        out.append("")
    out.append("")

    out.append("class GprMem:")
    out.append('    """Transpiled from mem.rs: enum GprMem<R, M> { Gpr(R), '
               'Mem(Amode<M>) }.\n\n    Each match in the Rust impl (below) '
               'has exactly two arms: `Gpr(x)`\n    dispatches to a method '
               'of the same name already defined on Gpr\n    (gpr.rs '
               'transpile, citing the exact mem.rs match arm each one\n'
               '    replaces); `Mem(amode)` dispatches to the identically-'
               'named method on\n    the Mem class above, which raises per '
               'its own cut invariant. This\n    turns a match-per-call-site '
               'into ordinary polymorphism -- the same\n    refactor for '
               'every method, so it is applied uniformly rather than\n    '
               'once by hand.\n    """')
    out.append('    __slots__ = ("value",)')
    out.append("")
    out.append("    def __init__(self, value):")
    out.append("        self.value = value if isinstance(value, (Gpr, Mem)) else Gpr(value)")
    out.append("")
    out.append("    def _require_gpr(self):")
    out.append("        if isinstance(self.value, Mem):")
    out.append("            raise NotImplementedError(")
    out.append('                "GprMem::Mem arm not cut (Amode encoding). Invariant "')
    out.append('                "\'all callers use register operands\' has been violated.")')
    out.append("        return self.value")
    out.append("")
    out.append("    def trap_code(self):")
    out.append("        return self.value.trap_code()")
    out.append("")

    for m in ("as_rex_prefix", "encode_rex_suffixes", "encode_bx_regs"):
        params, fn_body = methods[m]
        arg_names = []
        for p in split_top_level(params):
            p = p.strip()
            if p in ("&self", "&mut self"):
                arg_names.append("self")
            elif p:
                nm = p.split(':')[0].strip()
                arg_names.append(nm)
        # find the Gpr(binding) => expr arm to confirm the citation line
        # (fails loudly if the source's match shape has drifted)
        arm_re = re.search(r'GprMem::Gpr\((\w+)\)\s*=>\s*\{?(.+?)\}?\s*(?:,|\n\s*GprMem::Mem)',
                            fn_body, re.S)
        if not arm_re:
            raise Unsupported(f"mem.rs GprMem::{m}: cannot locate Gpr(..) match arm")
        sig = ", ".join(["self"] + arg_names[1:])
        out.append(f"    def {m}({sig}):")
        out.append(f'        """mem.rs GprMem::{m} -- delegates to '
                   f'Gpr.{m} (Gpr arm) or\n        Mem.{m} (Mem arm, cut) '
                   f'via polymorphism; see class docstring."""')
        out.append(f"        return self.value.{m}({', '.join(arg_names[1:])})")
        out.append("")

    out.append("")
    out.append("# xmm.rs's XmmMem<R, M> / Xmm<R> are structurally identical to")
    out.append("# GprMem<R, M> / Gpr<R> for every path encode() reaches (compare")
    out.append("# mem.rs's XmmMem impl to its GprMem impl above -- same bodies,")
    out.append("# `Xmm`/`Gpr` variant names aside). Transpiling them a second time")
    out.append("# would emit the same class twice; alias instead.")
    out.append("XmmMem = GprMem")
    out.append("Xmm = Gpr")
    out.append("")
    return "\n".join(out)


# ---- custom.rs: pub mod encode { nop_1b .. nop_9b } ----

def transpile_custom(texts):
    src = texts["custom.rs"]
    mod_body, _ = find_header_block(src, r'pub mod encode\s*')

    out = []
    out.append("class _CustomEncode:")
    out.append('    """Transpiled from custom.rs: pub mod encode (the '
               'generated file\'s escape\n    hatch for instructions '
               'assembler-x64-meta cannot template).\n\n    CUT: '
               '`pub mod mnemonic`, `pub mod display`, `pub mod visit` in '
               'the same\n    file are, respectively, mnemonic-string, '
               'Display/fmt, and\n    RegisterVisitor (register-allocation) '
               'code -- none reachable from\n    encode(). Handling every '
               'put1/put2/put4/put8 call uniformly here is\n    exactly '
               'the fix for the bug the differential test caught: an '
               'earlier\n    hand extraction matched only put1 and '
               'silently dropped put2/put4,\n    under-emitting '
               'nop_5b..nop_9b by 2-4 bytes.\n    """')

    fn_names = re.findall(r'pub fn (nop_\d+b)\(', mod_body)
    if not fn_names:
        raise Unsupported("custom.rs: no nop_*b functions found")
    ctx = {"self_type": "_CustomEncode"}
    for name in fn_names:
        params, ret_type, fn_body, _ = find_fn(mod_body, name)
        out.append("    @staticmethod")
        out.append(f"    def {name}(_inst, buf):")
        stmts = transpile_stmts(fn_body, ctx)
        out.extend(stmts if stmts else ["        pass"])
    out.append("")
    out.append("custom_encode = _CustomEncode()")
    out.append("")
    return "\n".join(out)


# ---- imm.rs: merge Imm8/Imm16/Imm32/Imm64/Simm8/Simm32 -> Imm(value,width) ----

def transpile_imm(texts):
    src = texts["imm.rs"]
    # Verify the mechanical fact the merge relies on: every N-bit encode()
    # body is `sink.putN(self.0 [as uN]);` with no other logic. If any of
    # these has grown extra logic, fail loudly instead of silently merging
    # something that no longer matches.
    checks = [
        ("Imm8", "put1", r'sink\.put1\(self\.0\);'),
        ("Simm8", "put1", r'sink\.put1\(self\.0 as u8\);'),
        ("Imm16", "put2", r'sink\.put2\(self\.0\);'),
        ("Simm16", "put2", r'sink\.put2\(self\.0 as u16\);'),
        ("Imm32", "put4", r'sink\.put4\(self\.0\);'),
        ("Simm32", "put4", r'sink\.put4\(self\.0 as u32\);'),
        ("Imm64", "put8", r'sink\.put8\(self\.0\);'),
    ]
    for type_name, _putn, body_re in checks:
        impl_body, _ = find_header_block(src, r'impl\s+' + type_name + r'\s*')
        _params, _ret, fn_body, _ = find_fn(impl_body, "encode")
        if not re.search(body_re, fn_body):
            raise Unsupported(
                f"imm.rs {type_name}::encode body no longer matches the "
                f"shape the Imm merge relies on: {fn_body.strip()!r}")

    out = []
    out.append("class Imm:")
    out.append('    """Merged transpile of imm.rs Imm8/Imm16/Imm32/Imm64/'
               'Simm8/Simm16/Simm32.\n\n    MERGE, not a guess: each of '
               'those seven `encode(&self, sink)` bodies\n    is exactly '
               '`sink.putN(self.0 [as uN]);` (verified above, at transpile\n'
               '    time, before this class is emitted) -- one line, '
               'parameterised only\n    by which `sink.putN` is called. '
               'Collapsing seven near-identical\n    classes into one '
               'width-keyed dispatch is the same kind of mechanical\n    '
               'reduction as aliasing XmmMem to GprMem.\n    """')
    out.append('    __slots__ = ("value", "width")')
    out.append("")
    out.append("    def __init__(self, value, width=4):")
    out.append("        self.value, self.width = int(value), width")
    out.append("")
    out.append("    def encode(self, sink):")
    out.append("        {1: sink.put1, 2: sink.put2, 4: sink.put4,")
    out.append("         8: sink.put8}[self.width](self.value)")
    out.append("")
    out.append("    def trap_code(self):")
    out.append('        """Not a literal imm.rs line: an immediate never '
               'traps. Synthesized\n        for interface uniformity with '
               'Gpr/GprMem/Mem (all reachable operand\n        types '
               'present `.trap_code()`).\n        """')
    out.append("        return None")
    out.append("")
    return "\n".join(out)


# ---- fixed.rs: nothing to transpile. See module docstring: Fixed<R,E> is
#      never referenced by name from the generated encode() bodies (grep
#      pc_vocab/ for "Fixed" -- zero hits); Gpr already fills that role.


# ---- api.rs: impl CodeSink for Vec<u8> ----

def transpile_api(texts):
    src = texts["api.rs"]
    impl_body, _ = find_header_block(src, r'impl CodeSink for Vec<u8>\s*')

    methods = {}
    for name, params, ret_type, fn_body in iter_fn_items(impl_body):
        methods[name] = fn_body

    for m in ("put1", "put2", "put4", "put8", "add_trap"):
        if m not in methods:
            raise Unsupported(f"api.rs impl CodeSink for Vec<u8>: missing {m}")

    out = []
    out.append("class CodeSink:")
    out.append('    """Transpiled from api.rs: `impl CodeSink for Vec<u8>` -- '
               'the crate\'s\n    own reference CodeSink used for testing. '
               'Vec<u8> becomes a\n    bytearray; `.bytes()` is added '
               'scaffolding (Rust\'s Vec<u8> IS the\n    buffer, so no '
               'equivalent accessor exists to transpile -- same kind of\n'
               '    templated boilerplate as the `__init__` transpile_vocab.py\n'
               '    synthesizes from struct fields, not a literal source '
               'line).\n\n    CUT: `use_target`/`known_offset` (api.rs) are '
               'RIP-relative-relocation\n    and known-offset plumbing, '
               'reachable only from the Amode path --\n    unreachable '
               'while GprMem::Mem stays cut. `add_trap` IS transpiled: '
               'the\n    Vec<u8> reference impl is a literal no-op '
               '(`fn add_trap(&mut self, _:\n    TrapCode) {}`), matched '
               'here exactly.\n    """')
    out.append("    def __init__(self):")
    out.append("        self.buf = bytearray()")
    out.append("")
    out.append("    def put1(self, b): self.buf.append(u8(b))")
    out.append("")
    out.append("    def put2(self, v):")
    out.append('        v &= 0xFFFF')
    out.append('        self.buf += bytes((v & 0xFF, (v >> 8) & 0xFF))')
    out.append("")
    out.append("    def put4(self, v):")
    out.append("        v = u32(v)")
    out.append('        self.buf += v.to_bytes(4, "little")')
    out.append("")
    out.append("    def put8(self, v):")
    out.append('        self.buf += (v & 0xFFFFFFFFFFFFFFFF).to_bytes(8, "little")')
    out.append("")
    out.append("    def add_trap(self, code):")
    out.append('        """api.rs: `fn add_trap(&mut self, _: TrapCode) {}` -- literal no-op."""')
    out.append("        pass")
    out.append("")
    out.append("    def bytes(self): return bytes(self.buf)")
    out.append("")
    return "\n".join(out)


# =================================================================
# 5. assembly of the output module
# =================================================================

POLYFILLS = '''
# ---------------- polyfills (class-1, value-model) ----------------
#
# Not a transpile of any single Rust line: these implement Rust's
# fixed-width unsigned-integer wrapping semantics, which the type system
# gives for free in Rust and Python does not. UNIFORM policy: every
# arithmetic node in a u8-typed expression is wrapped in u8(), with no
# exemptions, so an unwrapped node is unambiguously a bug rather than a
# possibly-intentional omission (see module docstring).

def u8(x: int) -> int:
    return x & 0xFF


def u32(x: int) -> int:
    return x & 0xFFFFFFFF


def i8(x: int) -> int:
    """`as i8` cast: reduce mod 256 into Python's signed-friendly range."""
    x &= 0xFF
    return x - 256 if x >= 128 else x

'''

VEX_CUT = '''
# ---------------- cuts: SIMD prefixes ----------------
#
# vex.rs / evex.rs are OUT OF SCOPE for this transpiler (see module
# docstring's file list) -- VEX/EVEX prefixes are reachable only from
# AVX/AVX-512 instructions, and no current slice emits those; the GPR
# integer vocabulary transpiled by transpile_vocab.py never constructs one.

class _CutPrefix:
    @staticmethod
    def _cut(*_a, **_k):
        raise NotImplementedError(
            "VEX/EVEX prefix encoding not cut (SIMD path). Invariant "
            "'no AVX instruction is reached' has been violated.")

    two_op = three_op = _cut


VexPrefix = _CutPrefix
EvexPrefix = _CutPrefix

'''


def main(src_dir, outfile="vocab_support_gen.py"):
    texts = read_sources(src_dir)
    sha = combined_sha(texts)
    version_m = re.search(r'cranelift-assembler-x64-([\d.]+)', str(pathlib.Path(src_dir).resolve()))
    version = version_m.group(1) if version_m else "unknown"

    sections = [
        HEADER.format(files=" ".join(SOURCE_FILES), sha=sha, version=version,
                     tv=TRANSPILER_VERSION),
        POLYFILLS,
        "# ---------------- api.rs ----------------\n",
        transpile_api(texts),
        "\n# ---------------- rex.rs ----------------\n",
        transpile_rex(texts),
        "\n# ---------------- gpr.rs ----------------\n",
        transpile_gpr(texts),
        "\n# ---------------- mem.rs ----------------\n",
        transpile_mem(texts),
        VEX_CUT,
        "\n# ---------------- imm.rs ----------------\n",
        transpile_imm(texts),
        "\n# ---------------- custom.rs ----------------\n",
        transpile_custom(texts),
    ]
    text = "\n".join(sections)
    pathlib.Path(outfile).write_text(text)
    print(f"transpiled -> {outfile} ({len(text.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: transpile_support.py <cranelift-src-dir> [outfile]", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "vocab_support_gen.py"))
