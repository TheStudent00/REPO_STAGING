#!/usr/bin/env python3
"""Flatten a loop-free, memory-free LLVM function into ONE basic block of pure
arithmetic: no branches, no memory, no calls.

Input: a module with exactly one `define`, every block named (run
`opt -passes='function(instnamer)'` first), no loops, and no load / store /
alloca / call-to-a-real-function left.  That is what slice_specialised.py +
localise.py + sroa produce for the RISC-V float operations.

The four things the shape needs
-------------------------------
path conditions   entry is `true`; `br i1 %c, T, F` carries cond(P) and %c
                  into T and cond(P) and not %c into F; a `switch` arm carries
                  cond(P) and (v == case), its default the negation of the or
                  of the arms; a block with several predecessors takes the `or`
                  of its incoming edge conditions.  Conditions live in a
                  hash-consed and/or/not DAG, so a condition reached twice is
                  computed once.

hoisting          every non-phi, non-terminator instruction of every block is
                  emitted into the one block, blocks in topological order,
                  instructions in their original order.  SSA dominance makes
                  that legal: a definition's block precedes every use's block
                  in any topological order of a DAG.

phis              or_i (v_i and mask(edge_i)), mask = the i1 condition itself
                  for i1 values and sext(cond) for wider ones; structs are
                  taken apart field by field.  Exactly one incoming edge
                  condition is true whenever the block is reached, so the
                  all-zero answer on the arms not taken adds nothing.
                  Conjuncts common to every arm are factored out of the or,
                  which is what keeps the count at a hand lowering's level.
                  Several `ret` blocks are combined the same way, as a phi at
                  a virtual exit.

selects           `select i1 c, a, b` -> `(a and m) or (b and not m)`, m = c
                  (sext for wider types).  Without this the RISC-V backend
                  puts a branch back, because base RV64IM has no conditional
                  move.

Speculation safety
------------------
Hoisting runs an instruction that used to be guarded, so anything whose
guardedness was load-bearing is repaired:

  udiv sdiv urem srem  are IMMEDIATE undefined behaviour on a zero divisor
        (and sdiv INT_MIN / -1 overflows).  The divisor is rewritten to
        `(d and sext c) or zext(not c)`: d itself when the path condition
        holds, the constant 1 when it does not.  Each one is recorded.

  shl lshr ashr        are POISON on an oversized shift amount, and poison is
        NOT killed by `and x, 0`.  The result is wrapped in `freeze`, which
        costs zero machine instructions.  Same for llvm.ctlz / cttz / abs,
        poison at zero / INT_MIN.

  flags                nsw nuw exact disjoint nneg samesign inbounds are
        stripped everywhere.  After that nothing in the flattened body can
        produce poison, so the masks really do erase the arms not taken.

  unreachable          a block ending in `unreachable` is dropped whole:
        reaching it was already undefined behaviour.

Anything it cannot prove safe - a loop, a surviving load / store / alloca, a
call to a real function - it refuses by name rather than guessing.
"""
import re
import sys

FLAGS = {"nsw", "nuw", "exact", "disjoint", "nneg", "samesign", "inbounds",
         "nusw", "fast", "nnan", "ninf", "nsz", "arcp", "contract", "afn",
         "reassoc"}
TERMINATORS = {"br", "switch", "ret", "unreachable", "indirectbr", "resume",
               "invoke", "callbr", "catchswitch", "catchret", "cleanupret"}
MEMORY_OPS = {"load", "store", "alloca", "cmpxchg", "atomicrmw", "fence",
              "getelementptr"}
DIVREM = {"udiv", "sdiv", "urem", "srem"}
SHIFTS = {"shl", "lshr", "ashr"}
POISON_INTRINSICS = ("llvm.ctlz", "llvm.cttz", "llvm.abs")
DROP_INTRINSICS = ("llvm.lifetime", "llvm.dbg", "llvm.assume", "llvm.expect",
                   "llvm.experimental.noalias", "llvm.invariant")

META_RE = re.compile(r",\s*![a-zA-Z_][\w.]*\s+![\w.]+")
VAL_RE = re.compile(r"%[-a-zA-Z$._0-9]+")
ZEROS = {"0", "false", "zeroinitializer", "null", "undef", "poison"}


class Refuse(Exception):
    pass


# --------------------------------------------------------------- lexing -----
def strip_meta(s):
    prev = None
    while prev != s:
        prev, s = s, META_RE.sub("", s)
    return s.strip()


def scan_type(s, i=0):
    """(type_text, index_after).  iN, ptr, {..}, [N x T], <N x T>, %named."""
    while i < len(s) and s[i].isspace():
        i += 1
    start = i
    if i < len(s) and s[i] in "{[<":
        opens = {"{": "}", "[": "]", "<": ">"}
        stack = [opens[s[i]]]
        i += 1
        while i < len(s) and stack:
            if s[i] in opens:
                stack.append(opens[s[i]])
            elif s[i] == stack[-1]:
                stack.pop()
            i += 1
    else:
        while i < len(s) and (s[i].isalnum() or s[i] in "._%"):
            i += 1
        if s[start:i] == "ptr" and s[i:].lstrip().startswith("addrspace"):
            i = s.index(")", i) + 1
    while i < len(s) and s[i] == "*":
        i += 1
    return s[start:i], i


def split_top(s, sep=","):
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch in "([{<":
            depth += 1
        elif ch in ")]}>":
            depth -= 1
        if ch == sep and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [x.strip() for x in out]


def split_flags(rest):
    """`add nuw nsw i64 %a, %b` -> ('add', 'i64 %a, %b'); flags dropped."""
    toks = rest.split(None, 1)
    op, tail = toks[0], (toks[1] if len(toks) > 1 else "")
    while op in ("tail", "musttail", "notail"):
        toks = tail.split(None, 1)
        op, tail = toks[0], (toks[1] if len(toks) > 1 else "")
    while True:
        t = tail.split(None, 1)
        if t and t[0] in FLAGS:
            tail = t[1] if len(t) > 1 else ""
            continue
        break
    return op, tail


RET_ATTRS = {"zeroext", "signext", "inreg", "noalias", "nonnull", "noundef",
             "nofree", "immarg", "returned", "writeonly", "readonly"}
RET_ATTRS_P = {"range", "dereferenceable", "dereferenceable_or_null", "align",
               "nofpclass", "captures", "initializes", "alignstack"}


def strip_ret_attrs(s):
    """`range(i32 16, 33) i32 @llvm.ctlz.i32(...)` -> `i32 @llvm.ctlz.i32(...)`.
    LLVM 21 puts return attributes in front of a call's result type, and
    reading one of those as the type is how `freeze range %x` gets written."""
    while True:
        s = s.lstrip()
        m = re.match(r"([a-z_]+)(\(|\s|$)", s)
        if not m:
            return s
        w = m.group(1)
        if w in RET_ATTRS:
            s = s[len(w):]
            continue
        if w in RET_ATTRS_P and m.group(2) == "(":
            d, i = 0, s.index("(")
            for j in range(i, len(s)):
                if s[j] == "(":
                    d += 1
                elif s[j] == ")":
                    d -= 1
                    if d == 0:
                        s = s[j + 1:]
                        break
            continue
        if w in RET_ATTRS_P:
            s = re.sub(r"^%s\s+\d+" % w, "", s)
            continue
        return s


def struct_fields(ty):
    t = ty.strip()
    if t.startswith("{") and t.endswith("}"):
        return split_top(t[1:-1].strip())
    return None


def is_zero(v):
    return v.strip() in ZEROS


# ------------------------------------------------------------- IR model -----
class Block:
    def __init__(self, label):
        self.label, self.phis, self.insts, self.term, self.succs = \
            label, [], [], None, []


def parse_module(text):
    lines = text.splitlines()
    di = [i for i, l in enumerate(lines) if l.startswith("define ")]
    if len(di) != 1:
        raise Refuse("module has %d definitions, expected 1" % len(di))
    d = di[0]
    e = next(i for i in range(d, len(lines)) if lines[i].rstrip() == "}")
    header, body = lines[d], lines[d + 1:e]

    # `switch` spans several lines; join any instruction whose brackets are
    # still open.  Reading it line by line turns the arms into bogus
    # instructions and the CFG into nonsense.
    joined, acc, depth = [], "", 0
    for raw in body:
        s = raw.split(";")[0].rstrip() if not raw.strip().startswith(";") else ""
        if not s.strip():
            continue
        acc = (acc + " " + s.strip()) if acc else s.strip()
        depth += s.count("[") - s.count("]")
        if depth <= 0:
            joined.append(acc)
            acc, depth = "", 0
    if acc:
        joined.append(acc)

    blocks, order = {}, []
    lab_re = re.compile(r'^([-a-zA-Z$._0-9]+):')
    cur = Block("%.entry")
    blocks[cur.label] = cur
    order.append(cur.label)
    for raw in joined:
        s = raw.strip()
        if not s or s.startswith(";"):
            continue
        m = lab_re.match(s)
        if m:
            lab = "%" + m.group(1)
            if cur.label == "%.entry" and not cur.insts and not cur.phis \
                    and cur.term is None and len(order) == 1:
                del blocks["%.entry"]
                order = []
            cur = Block(lab)
            blocks[lab] = cur
            order.append(lab)
            continue
        s = strip_meta(s)
        if not s:
            continue
        name, rest = None, s
        if " = " in s and s.split(" = ", 1)[0].startswith("%"):
            name, rest = s.split(" = ", 1)
        op = rest.split(None, 1)[0]
        if op in TERMINATORS:
            cur.term = rest
        elif op == "phi":
            cur.phis.append(parse_phi(name, rest))
        else:
            cur.insts.append((name, rest))
    if not order:
        raise Refuse("no blocks")
    return lines[:d], header, blocks, order, lines[e + 1:]


def parse_phi(name, rest):
    body = rest[len("phi"):].strip()
    while body.split(None, 1)[0] in FLAGS:
        body = body.split(None, 1)[1]
    ty, i = scan_type(body)
    pairs = [(m.group(1).strip(), m.group(2)) for m in
             re.finditer(r"\[\s*([^,\]]+?)\s*,\s*(%[-a-zA-Z$._0-9]+)\s*\]",
                         body[i:])]
    return (name, ty, pairs)


# ------------------------------------------------------ condition algebra ---
class C:
    _pool = {}

    def __init__(self, kind, kids=(), var=None):
        self.kind, self.kids, self.var = kind, tuple(kids), var

    @staticmethod
    def get(kind, kids=(), var=None):
        kk = tuple(sorted((id(k) for k in kids))) if kind in "AO" \
            else tuple(id(k) for k in kids)
        key = (kind, kk, var)
        if key not in C._pool:
            C._pool[key] = C(kind, kids, var)
        return C._pool[key]


TRUE, FALSE = C.get("T"), C.get("F")
_vars = {}


def cvar(name):
    if name not in _vars:
        _vars[name] = C.get("V", var=name)
    return _vars[name]


def cnot(a):
    if a is TRUE:
        return FALSE
    if a is FALSE:
        return TRUE
    if a.kind == "N":
        return a.kids[0]
    return C.get("N", (a,))


def conj(a):
    return set(a.kids) if a.kind == "A" else (set() if a is TRUE else {a})


def cand(*xs):
    parts = set()
    for x in xs:
        if x is FALSE:
            return FALSE
        parts |= conj(x)
    if any(cnot(p) in parts for p in parts):
        return FALSE
    # x and (x or y) = x
    parts = {p for p in parts
             if not (p.kind == "O" and any(k in parts for k in p.kids))}
    if not parts:
        return TRUE
    if len(parts) == 1:
        return next(iter(parts))
    return C.get("A", sorted(parts, key=id))


_or_cache = {}


def cor(*xs):
    """or, with the two Boolean laws that matter here applied to a fixpoint:

      absorption   P or (P and Q) = P
      consensus    (S and Q) or (S and not Q) = S

    Without consensus the condition of a join block - `or` over every way in -
    stays a large expression where it is in fact just the condition of the
    block that dominates the join, very often plain `true`.  That is the
    difference between masking a value that never needed masking and emitting
    nothing at all."""
    flat = []
    for x in xs:
        if x is TRUE:
            return TRUE
        if x is FALSE:
            continue
        flat.extend(x.kids if x.kind == "O" else [x])
    key = frozenset(id(p) for p in flat)
    if key in _or_cache:
        return _or_cache[key]

    sets = []
    for p in flat:
        s = frozenset(conj(p)) if p.kind == "A" else frozenset([p])
        if s not in sets:
            sets.append(s)

    result = None
    changed = True
    while changed and len(sets) <= 64:
        changed = False
        keep = [a for i, a in enumerate(sets)
                if not any(j != i and sets[j] < a for j in range(len(sets)))]
        if len(keep) != len(sets):
            sets, changed = keep, True
        merged_any = False
        for i in range(len(sets)):
            for j in range(i + 1, len(sets)):
                a, b = sets[i], sets[j]
                da, db = a - b, b - a
                if len(da) == 1 and len(db) == 1 \
                        and cnot(next(iter(da))) is next(iter(db)):
                    m = a & b
                    if not m:
                        result = TRUE
                    sets = [s for k, s in enumerate(sets) if k not in (i, j)]
                    if m and m not in sets:
                        sets.append(m)
                    changed = merged_any = True
                    break
            if merged_any or result is not None:
                break
        if result is not None:
            break

    if result is None:
        if not sets:
            result = FALSE
        else:
            nodes = [next(iter(s)) if len(s) == 1 else cand(*s) for s in sets]
            nodes = sorted(set(nodes), key=id)
            result = nodes[0] if len(nodes) == 1 else C.get("O", nodes)
    _or_cache[key] = result
    return result


# ---------------------------------------------------------------- emitter ---
class Emitter:
    def __init__(self):
        self.out = []            # list of instruction texts
        self.n = 0
        self.memo = {}
        self.rename = {}
        self.guarded = []
        self.tables = []

    def fresh(self, hint="g"):
        self.n += 1
        return "%%.%s%d" % (hint, self.n)

    def add(self, text, hint="g"):
        name = self.fresh(hint)
        self.out.append("%s = %s" % (name, text))
        return name

    def named(self, name, text):
        self.out.append("%s = %s" % (name, text))
        return name

    def raw(self, text):
        self.out.append(text)

    def bind(self, name, value):
        """The original instruction's name now denotes `value`."""
        if name is not None and name != value:
            self.rename[name] = value

    def cval(self, c):
        if c is TRUE:
            return "true"
        if c is FALSE:
            return "false"
        if c in self.memo:
            return self.memo[c]
        if c.kind == "V":
            v = c.var
        elif c.kind == "N":
            v = self.add("xor i1 %s, true" % self.cval(c.kids[0]), "n")
        else:
            op = "and" if c.kind == "A" else "or"
            vs = [self.cval(k) for k in c.kids]
            v = vs[0]
            for x in vs[1:]:
                v = self.add("%s i1 %s, %s" % (op, v, x), "c")
        self.memo[c] = v
        return v

    def mask(self, c, ty):
        if ty == "i1":
            return self.cval(c)
        key = ("m", c, ty)
        if key in self.memo:
            return self.memo[key]
        b = self.cval(c)
        v = "-1" if b == "true" else "0" if b == "false" \
            else self.add("sext i1 %s to %s" % (b, ty), "m")
        self.memo[key] = v
        return v


def combine(em, ty, arms):
    """arms = [(value_text, C)] -> one value of type ty equal to
    or_i (v_i and mask(c_i)), with the conjuncts common to every arm factored
    out of the or and applied once."""
    arms = [(v, c) for v, c in arms if c is not FALSE and not is_zero(v)]
    if not arms:
        return "false" if ty == "i1" else "0"
    if len(arms) == 1 and arms[0][1] is TRUE:
        return arms[0][0]
    if len(set(v for v, _ in arms)) == 1 and cor(*[c for _, c in arms]) is TRUE:
        return arms[0][0]

    common = set(conj(arms[0][1]))
    for _, c in arms[1:]:
        common &= conj(c)
    rest = [(v, cand(*[k for k in conj(c) if k not in common]))
            for v, c in arms]

    fields = struct_fields(ty)
    if fields is not None:
        acc = "undef"
        for idx, fty in enumerate(fields):
            parts = [(em.add("extractvalue %s %s, %d" % (ty, v, idx), "e"), c)
                     for v, c in rest]
            fv = combine(em, fty, parts)
            if common:
                m = em.mask(cand(*common), fty)
                if m != "-1":
                    fv = em.add("and %s %s, %s" % (fty, fv, m), "a")
            acc = em.add("insertvalue %s %s, %s %s, %d"
                         % (ty, acc, fty, fv, idx), "i")
        return acc

    acc = None
    for v, c in rest:
        if c is TRUE:
            t = v
        else:
            m = em.mask(c, ty)
            t = em.add("and %s %s, %s" % (ty, v, m), "a")
        acc = t if acc is None else em.add("or %s %s, %s" % (ty, acc, t), "o")
    if common:
        m = em.mask(cand(*common), ty)
        if m != "-1":
            acc = em.add("and %s %s, %s" % (ty, acc, m), "a")
    return acc


# ------------------------------------------------------------- lowering -----
def lower_select(em, name, tail):
    """select i1 c, TY a, TY b -> mask arithmetic, defining `name`."""
    cty, i = scan_type(tail)
    if cty != "i1":
        raise Refuse("select on a `%s` condition (vector select)" % cty)
    parts = split_top(tail[i:])
    if len(parts) != 3:
        raise Refuse("unparsed select: " + tail)
    cond = parts[0].strip()
    aty, j = scan_type(parts[1])
    a = parts[1][j:].strip()
    bty, k = scan_type(parts[2])
    b = parts[2][k:].strip()
    if aty != bty:
        raise Refuse("select arms disagree: %s vs %s" % (aty, bty))
    ty = aty
    if cond in ("true", "false"):
        em.bind(name, a if cond == "true" else b)
        return
    if struct_fields(ty) is not None:
        cc = cvar(cond)
        em.bind(name, combine(em, ty, [(a, cc), (b, cnot(cc))]))
        return
    if ty == "i1":
        if a == "true":
            em.named(name, "or i1 %s, %s" % (cond, b))
        elif a == "false":
            nc = em.add("xor i1 %s, true" % cond, "n")
            em.named(name, "and i1 %s, %s" % (nc, b))
        elif b == "false":
            em.named(name, "and i1 %s, %s" % (cond, a))
        elif b == "true":
            nc = em.add("xor i1 %s, true" % cond, "n")
            em.named(name, "or i1 %s, %s" % (nc, a))
        else:
            ia = em.add("and i1 %s, %s" % (a, cond), "a")
            nc = em.add("xor i1 %s, true" % cond, "n")
            ib = em.add("and i1 %s, %s" % (b, nc), "a")
            em.named(name, "or i1 %s, %s" % (ia, ib))
        return
    m = em.add("sext i1 %s to %s" % (cond, ty), "m")
    if is_zero(b):
        em.named(name, "and %s %s, %s" % (ty, a, m))
        return
    if is_zero(a):
        nm = em.add("xor %s %s, -1" % (ty, m), "n")
        em.named(name, "and %s %s, %s" % (ty, b, nm))
        return
    ia = em.add("and %s %s, %s" % (ty, a, m), "a")
    nm = em.add("xor %s %s, -1" % (ty, m), "n")
    ib = em.add("and %s %s, %s" % (ty, b, nm), "a")
    em.named(name, "or %s %s, %s" % (ty, ia, ib))


GLOBAL_RE = re.compile(
    r"^@([\w.$]+) = [^\n]*constant \[(\d+) x i(\d+)\] \[([^\]]*)\]")


def parse_tables(prologue):
    """Constant arrays of small integers - SoftFloat's two 16-entry reciprocal
    and reciprocal-square-root seed tables."""
    tabs = {}
    for line in prologue:
        m = GLOBAL_RE.match(line)
        if not m:
            continue
        name, n, w = m.group(1), int(m.group(2)), int(m.group(3))
        vals = []
        for e in m.group(4).split(","):
            e = e.strip()
            mm = re.match(r"i\d+\s+(-?\d+)$", e)
            if not mm:
                vals = None
                break
            vals.append(int(mm.group(1)) & ((1 << w) - 1))
        if vals and len(vals) == n:
            tabs[name] = (n, w, vals)
    return tabs


def lower_table_load(em, name, table, idx, where):
    """table[idx] as arithmetic.  The entries are packed into 64-bit words and
    the word is chosen with the constant-select identity
    `select(c, A, B) = B xor ((A xor B) and sext c)`, then the entry is shifted
    out of it.  The index is masked to the table size first: in range that is a
    no-op, and out of range the original load was already reading off the end
    of the array, which is undefined, so any answer refines it."""
    n, w, vals = table
    if n & (n - 1) or 64 % w or (64 // w) == 0:
        raise Refuse("table @%s is %d x i%d, not a shape this lowers" %
                     (where, n, w))
    epw = 64 // w
    nw = max(1, (n + epw - 1) // epw)
    if nw & (nw - 1):
        raise Refuse("table @%s packs into %d words, not a power of two"
                     % (where, nw))
    words = []
    for k in range(nw):
        acc = 0
        for j in range(epw):
            if k * epw + j < n:
                acc |= vals[k * epw + j] << (j * w)
        words.append(acc)

    mi = em.add("and i64 %s, %d" % (idx, n - 1), "t")
    lo = em.add("and i64 %s, %d" % (mi, epw - 1), "t")
    bits = []
    if nw > 1:
        hi = em.add("lshr i64 %s, %d" % (mi, (epw - 1).bit_length()), "t")
        for k in range(nw.bit_length() - 1):
            src = hi if k == 0 else em.add("lshr i64 %s, %d" % (hi, k), "t")
            b = em.add("trunc i64 %s to i1" % src, "t")
            bits.append(em.add("sext i1 %s to i64" % b, "t"))

    def rec(base, cnt, k):
        if cnt == 1:
            return ("c", words[base])
        h = cnt // 2
        a = rec(base, h, k - 1)
        b = rec(base + h, h, k - 1)
        m = bits[k]
        if a[0] == "c" and b[0] == "c":
            d = (a[1] ^ b[1]) & 0xFFFFFFFFFFFFFFFF
            t = em.add("and i64 %s, %d" % (m, d), "t")
            return ("v", em.add("xor i64 %s, %d" % (t, a[1]), "t"))
        av = a[1] if a[0] == "v" else str(a[1])
        bv = b[1] if b[0] == "v" else str(b[1])
        d = em.add("xor i64 %s, %s" % (bv, av), "t")
        t = em.add("and i64 %s, %s" % (m, d), "t")
        return ("v", em.add("xor i64 %s, %s" % (t, av), "t"))

    sel = rec(0, nw, len(bits) - 1)
    word = sel[1] if sel[0] == "v" else str(sel[1])
    sh = em.add("shl i64 %s, %d" % (lo, w.bit_length() - 1), "t")
    sr = em.add("lshr i64 %s, %s" % (word, sh), "t")
    em.named(name, "trunc i64 %s to i%d" % (sr, w))


MINMAX = {"umax": "ugt", "umin": "ult", "smax": "sgt", "smin": "slt"}
MINMAX_RE = re.compile(r"@llvm\.(umax|umin|smax|smin)\.i(\d+)\((.*)\)\s*$")


def lower_minmax(em, name, tail):
    """llvm.umax/umin/smax/smin as mask arithmetic.  Base RV64IM has no
    instruction for these and no conditional move, so the backend lowers the
    intrinsic as a compare and a BRANCH - one branch is one branch too many
    here, and it is the only one left in the sqrt family."""
    m = MINMAX_RE.search(tail)
    if not m:
        raise Refuse("unparsed min/max intrinsic: " + tail)
    kind, w = m.group(1), m.group(2)
    ty = "i" + w
    args = split_top(m.group(3))
    if len(args) != 2:
        raise Refuse("min/max with %d arguments" % len(args))
    vs = []
    for a in args:
        _, i = scan_type(strip_ret_attrs(a))
        vs.append(strip_ret_attrs(a)[i:].strip())
    a, b = vs
    c = em.add("icmp %s %s %s, %s" % (MINMAX[kind], ty, a, b), "p")
    msk = em.add("sext i1 %s to %s" % (c, ty), "m")
    d = em.add("xor %s %s, %s" % (ty, a, b), "x")
    t = em.add("and %s %s, %s" % (ty, d, msk), "a")
    em.named(name, "xor %s %s, %s" % (ty, t, b))


def guard_divisor(em, op, ty, a, b, cond, name, where):
    """(d and sext c) or zext(not c): the divisor itself when the block runs,
    the constant 1 when it does not, so the hoisted division is always
    defined."""
    cv = em.cval(cond)
    nc = em.add("xor i1 %s, true" % cv, "n")
    m = em.mask(cond, ty)
    t = em.add("and %s %s, %s" % (ty, b, m), "a")
    z = em.add("zext i1 %s to %s" % (nc, ty), "z")
    d = em.add("or %s %s, %s" % (ty, t, z), "d")
    em.guarded.append({"instruction": name, "opcode": op, "type": ty,
                       "block": where, "divisor": b, "forced_to": d})
    em.named(name, "%s %s %s, %s" % (op, ty, a, d))


# ---------------------------------------------------------------- driver ----
def flatten(text, new_name=None):
    pro, header, blocks, order, epi = parse_module(text)
    entry = order[0]

    dead = set()
    for lab in order:
        b = blocks[lab]
        if b.term is None:
            raise Refuse("block %s has no terminator" % lab)
        op = b.term.split(None, 1)[0]
        if op == "unreachable":
            dead.add(lab)
            continue
        if op in ("invoke", "callbr", "indirectbr", "resume", "catchswitch",
                  "catchret", "cleanupret"):
            raise Refuse("terminator `%s` in %s" % (op, lab))
        b.succs = re.findall(r"label (%[-a-zA-Z$._0-9]+)", b.term)
    if entry in dead:
        raise Refuse("entry block is unreachable")
    live = [l for l in order if l not in dead]
    for l in live:
        blocks[l].succs = [s for s in blocks[l].succs if s not in dead]

    # A getelementptr into one of SoftFloat's constant seed tables, feeding
    # only loads, is data rather than memory: it is lowered to arithmetic.
    tables = parse_tables(pro)
    gep_re = re.compile(r"getelementptr[\w. ]*\s*\[\d+ x i(\d+)\], ptr "
                        r"@([\w.$]+), i64 0, (?:i\d+ )?(\S+)\s*$")
    tab_ptr = {}
    for lab in live:
        for name, rest in blocks[lab].insts:
            op, tail = split_flags(rest)
            if op != "getelementptr":
                continue
            m = gep_re.match(rest.strip())
            if m and m.group(2) in tables and name:
                tab_ptr[name] = (tables[m.group(2)], m.group(3).strip(),
                                 m.group(2))

    for lab in live:
        for name, rest in blocks[lab].insts:
            op, tail = split_flags(rest)
            if op == "getelementptr" and name in tab_ptr:
                continue
            if op == "load":
                m = re.match(r"load i\d+, ptr (%[-a-zA-Z$._0-9]+)",
                             rest.strip())
                if m and m.group(1) in tab_ptr:
                    continue
            if op in MEMORY_OPS:
                raise Refuse("memory operation `%s` survives in block %s"
                             % (op, lab))
            if op == "call":
                cn = re.search(r"@([\w.$]+)", rest)
                cn = cn.group(1) if cn else "?"
                if not cn.startswith("llvm."):
                    raise Refuse("call to @%s survives in block %s" % (cn, lab))

    preds = {l: set() for l in live}
    for l in live:
        for s in blocks[l].succs:
            preds[s].add(l)
    pending = {l: set(preds[l]) for l in live}
    topo, q, done = [], [entry], set()
    while q:
        l = q.pop(0)
        topo.append(l)
        done.add(l)
        for s in sorted(set(blocks[l].succs)):
            pending[s].discard(l)
            if not pending[s] and s not in done and s not in q:
                q.append(s)
    if len(topo) != len(live):
        raise Refuse("CFG is not acyclic: only %d of %d blocks could be "
                     "ordered, so there is a loop" % (len(topo), len(live)))

    em = Emitter()
    cond, edge, rets, ret_ty = {entry: TRUE}, {}, [], None

    for lab in topo:
        b = blocks[lab]
        if lab != entry:
            cond[lab] = cor(*[edge[(p, lab)] for p in sorted(preds[lab])])

        for name, ty, pairs in b.phis:
            arms = []
            for v, p in pairs:
                if p in dead or (p, lab) not in edge:
                    continue
                arms.append((v, edge[(p, lab)]))
            em.bind(name, combine(em, ty, arms))

        for name, rest in b.insts:
            op, tail = split_flags(rest)
            if op == "getelementptr":
                continue                             # folded into its loads
            if op == "load":
                m = re.match(r"load i\d+, ptr (%[-a-zA-Z$._0-9]+)",
                             rest.strip())
                tbl, idx, tname = tab_ptr[m.group(1)]
                lower_table_load(em, name, tbl, idx, tname)
                em.tables.append({"instruction": name, "table": tname,
                                  "entries": tbl[0], "width": tbl[1],
                                  "block": lab})
                continue
            if op == "call":
                cn = re.search(r"@([\w.$]+)", rest)
                cn = cn.group(1) if cn else ""
                if any(cn.startswith(d) for d in DROP_INTRINSICS):
                    continue
                if name and MINMAX_RE.search(tail):
                    lower_minmax(em, name, tail)
                    continue
                risky = any(cn.startswith(p) for p in POISON_INTRINSICS)
                if name and risky and cond[lab] is not TRUE:
                    rty, _ = scan_type(strip_ret_attrs(tail))
                    t = em.add("call " + tail, "k")
                    em.named(name, "freeze %s %s" % (rty, t))
                elif name:
                    em.named(name, "call " + tail)
                else:
                    em.raw("call " + tail)
                continue
            if op == "select":
                lower_select(em, name, tail)
                continue
            if op in DIVREM:
                ty, i = scan_type(tail)
                aa, bb = split_top(tail[i:])
                guard_divisor(em, op, ty, aa.strip(), bb.strip(),
                              cond[lab], name, lab)
                continue
            if op in SHIFTS and cond[lab] is not TRUE:
                ty, _ = scan_type(tail)
                t = em.add("%s %s" % (op, tail), "sh")
                em.named(name, "freeze %s %s" % (ty, t))
                continue
            if name:
                em.named(name, "%s %s" % (op, tail))
            else:
                em.raw("%s %s" % (op, tail))

        t = b.term
        top = t.split(None, 1)[0]
        if top == "ret":
            body = t[3:].strip()
            if body == "void":
                ret_ty = "void"
            else:
                ty, i = scan_type(body)
                ret_ty = ty
                rets.append((body[i:].strip(), ty, cond[lab]))
        elif top == "br":
            if t.startswith("br label"):
                s = b.succs[0]
                edge[(lab, s)] = cor(edge.get((lab, s), FALSE), cond[lab])
            else:
                m = re.match(r"br i1 (\S+), label (\S+), label (\S+)", t)
                if not m:
                    raise Refuse("unparsed br: " + t)
                c, tl, fl = m.group(1), m.group(2), m.group(3)
                cc = TRUE if c == "true" else FALSE if c == "false" \
                    else cvar(c)
                if tl == fl:
                    edge[(lab, tl)] = cor(edge.get((lab, tl), FALSE),
                                          cond[lab])
                else:
                    edge[(lab, tl)] = cor(edge.get((lab, tl), FALSE),
                                          cand(cond[lab], cc))
                    edge[(lab, fl)] = cor(edge.get((lab, fl), FALSE),
                                          cand(cond[lab], cnot(cc)))
        elif top == "switch":
            body = t[len("switch"):].strip()
            ty, i = scan_type(body)
            m = re.match(r"\s*(\S+)\s*,\s*label\s+(\S+)\s*\[(.*)\]\s*$",
                         body[i:], re.S)
            if not m:
                raise Refuse("unparsed switch: " + t)
            val, deflab, arms = m.group(1), m.group(2), m.group(3)
            allc = FALSE
            for am in re.finditer(r"(\S+)\s+(\S+)\s*,\s*label\s+(\S+)", arms):
                cst, tgt = am.group(2), am.group(3)
                cc = cvar(em.add("icmp eq %s %s, %s" % (ty, val, cst), "q"))
                allc = cor(allc, cc)
                edge[(lab, tgt)] = cor(edge.get((lab, tgt), FALSE),
                                       cand(cond[lab], cc))
            edge[(lab, deflab)] = cor(edge.get((lab, deflab), FALSE),
                                      cand(cond[lab], cnot(allc)))
        else:
            raise Refuse("terminator `%s`" % top)

    if ret_ty == "void" or not rets:
        em.raw("ret void")
    else:
        ty = rets[0][1]
        if any(r[1] != ty for r in rets):
            raise Refuse("return types disagree across ret blocks")
        # One `ret` block: every defined execution leaves through it, so its
        # path condition is a tautology whether or not the algebra can see it.
        arms = [(rets[0][0], TRUE)] if len(rets) == 1 \
            else [(v, c) for v, _, c in rets]
        em.raw("ret %s %s" % (ty, combine(em, ty, arms)))

    body = resolve(em.out, em.rename)
    body = sweep(body)
    body = schedule(body)

    hdr = re.sub(r"\s*#\d+\s*\{\s*$", " {", header)
    hdr = re.sub(r"range\([^)]*\)\s*", "", hdr)
    hdr = hdr.replace(" local_unnamed_addr", "")
    if new_name:
        hdr = re.sub(r"@[\w.$]+\(", "@%s(" % new_name, hdr, count=1)
    out = list(pro) + [hdr] + ["  " + t for t in body] + ["}"]
    out += [l for l in epi if not l.startswith("attributes #")]
    return "\n".join(out) + "\n", em


def resolve(body, rename):
    """Apply the phi/select bindings (an original name -> the value that now
    holds it), following chains."""
    if not rename:
        return body
    final = {}

    def res(v, seen=()):
        if v in final:
            return final[v]
        if v not in rename or v in seen:
            return v
        r = res(rename[v], seen + (v,))
        final[v] = r
        return r

    out = []
    for txt in body:
        lhs, sep, rhs = txt.partition(" = ")
        tgt = rhs if sep else txt
        tgt = VAL_RE.sub(lambda m: res(m.group(0)), tgt)
        out.append(lhs + " = " + tgt if sep else tgt)
    return [t for t in out
            if not (" = " in t and t.split(" = ", 1)[0].strip() in rename)]


def schedule(body):
    """Reorder the single block to hold fewer values live at once.

    Topological-by-block order is correct but wasteful: it computes every
    block's values up front and keeps them all live to the masks at the end,
    and RV64IM has 27 usable registers, so the allocator spills.  Every
    instruction here is pure, so any order that respects the data dependences
    is equally correct; this picks, among the ready instructions, the one that
    kills the most live values and creates the fewest (the Sethi-Ullman greedy
    choice), which is what turns spill traffic back into registers."""
    n = len(body)
    if n < 3:
        return body
    defs, uses = {}, []
    for i, t in enumerate(body):
        lhs, sep, _ = t.partition(" = ")
        if sep:
            defs[lhs.strip()] = i
    for t in body:
        rhs = t.split(" = ", 1)[1] if " = " in t else t
        uses.append([v for v in dict.fromkeys(VAL_RE.findall(rhs))
                     if v in defs])
    defname = [t.split(" = ", 1)[0].strip() if " = " in t else None
               for t in body]
    users = {}
    for u in uses:
        for v in u:
            users[v] = users.get(v, 0) + 1

    unmet = [len(u) for u in uses]
    waiters = {}
    for i, u in enumerate(uses):
        for v in u:
            waiters.setdefault(v, []).append(i)
    left = dict(users)
    ready = sorted(i for i in range(n - 1) if unmet[i] == 0)
    order, placed = [], 0
    while ready:
        best, bestkey = None, None
        for i in ready:
            killed = sum(1 for v in uses[i] if left[v] == 1)
            born = 1 if users.get(defname[i], 0) else 0
            key = (born - killed, i)
            if bestkey is None or key < bestkey:
                best, bestkey = i, key
        ready.remove(best)
        order.append(best)
        placed += 1
        for v in uses[best]:
            left[v] -= 1
        d = defname[best]
        if d:
            for j in waiters.get(d, []):
                unmet[j] -= 1
                if unmet[j] == 0 and j != n - 1:
                    ready.append(j)
    if placed != n - 1:
        return body                                  # something is off: keep
    return [body[i] for i in order] + [body[n - 1]]


def sweep(body):
    """Keep only what the final `ret` depends on."""
    defs = {t.split(" = ", 1)[0].strip(): i for i, t in enumerate(body)
            if " = " in t}
    keep, work = set(), [len(body) - 1]
    while work:
        i = work.pop()
        if i in keep:
            continue
        keep.add(i)
        rhs = body[i].split(" = ", 1)[1] if " = " in body[i] else body[i]
        for v in VAL_RE.findall(rhs):
            if v in defs and defs[v] not in keep:
                work.append(defs[v])
    return [t for i, t in enumerate(body) if i in keep]


def main():
    try:
        out, em = flatten(open(sys.argv[1]).read(),
                          sys.argv[3] if len(sys.argv) > 3 else None)
    except Refuse as ex:
        sys.stderr.write("REFUSED: %s\n" % ex)
        return 2
    open(sys.argv[2], "w").write(out)
    for g in em.guarded:
        print("  guarded %s = %s %s (divisor %s, block %s)"
              % (g["instruction"], g["opcode"], g["type"], g["divisor"],
                 g["block"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
