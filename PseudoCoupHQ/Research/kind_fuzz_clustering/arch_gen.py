#!/usr/bin/env python3
"""arch_gen.py -- the ARCH-UNIT generator.

An ARCH-UNIT is  (operator, lhs holder index, rhs holder index)
              -> instruction sequence.

There is no input-value axis.  One compiled function covers every input,
because the function takes its two operands as PARAMETERS.  Constants are
banned on purpose: a constant operand is folded away at compile time and
the operation we came to measure disappears.

Each arch-unit records BOTH columns, and this is a ruling, not a
preference -- they are not collapsed into one:

    bytes   the raw hex machine encoding
    mnem    the mnemonic sequence as objdump prints it

A third column, `layout`, was added later.  It is not a normalization
and it is not a judgement: it is the address and the byte count objdump
printed for each instruction, kept so that the READER can tell which
bytes belong to which instruction and can express a branch target as an
offset from the instruction's own address.  Neither fact is recoverable
from a flattened byte list, so refusing to record it would have made
canonicalization impossible rather than merely inconvenient.  The
`bytes` and `mnem` columns are untouched by its arrival, except that
`mnem` now KEEPS objdump's `<symbol+offset>` annotation instead of
throwing it away -- `call 412aa0 <runtime.morestack_noctxt>` names the
operation being performed, and that name is not the reader's to invent.
All stripping happens in arch_read.py, never here.

Where the type spellings come from
----------------------------------
`l3_accept.py` built the acceptance runs by unifying, per language, the
layer-2 file `../data_representation/representations_<lang>.json` into a
holder list; the holder INDEX in `space_<lang>.json` is the position in
that unified list.  The literal type spelling of a holder is therefore
recoverable from the same declaration text `l3_accept.py` emitted into
its probes -- `let v: i32 = 42;` yields `i32`, `std::vector<int64_t> v =
{1,2,3};` yields `std::vector<int64_t>`.  This file re-uses
`l3_accept.holders()` directly so the indices cannot drift.

A holder whose declaration carries no spellable type is recorded as
SKIPPED with a reason.  It is never guessed at and never silently
dropped.  Where a spelling DOES exist and only the declaration text hid
it -- a rust tuple written with inference, a C++ `auto` tuple, a go
`list.New()` -- the spelling is supplied by hand in the SPELLED table
below, with the reasoning attached to it.  See that table.

What it emits
-------------
  arch_manifest_<lang>.json   n -> {op, i, j, lhs_rep, rhs_rep,
                              lhs_form, rhs_form}, plus the skipped units
                              and the recovered holder type table
  lanes/arch_<lang>.sh        a self-contained lane carrying its own
                              units and its own driver

Lane output, one line per unit, written to /out/arch_<lang>.txt:

  af_<n>|OK|<hex bytes space separated>|<mnemonics separated by ;>
        |<addr:bytecount per instruction, separated by ;>
  af_<n>|BUILDFAIL|<first line of compiler error, truncated to 200>
  af_<n>|NOSYM|<note>

usage:
  arch_gen.py <lang> [<lang> ...]           full lanes
  arch_gen.py rust --smoke 20 --also '+,3,3' --also '+,7,7'
             --name arch_rust_smoke --drop
"""

import argparse
import base64
import gzip
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import l3_accept as L3                                       # noqa: E402

LANGS = ["cpp", "rust", "go", "swift"]

DROP = "<WORKSPACE_DIR>/Airlock/agent/drop"

SCALAR_FORMS = {"whole", "fractional", "truth"}

# rust: an arithmetic or bitwise operator's result is the operator
# trait's own associated Output type.  Nothing is assumed about what that
# Output turns out to be.
RUST_TRAIT = {
    "+": "Add", "-": "Sub", "*": "Mul", "/": "Div", "%": "Rem",
    "&": "BitAnd", "|": "BitOr", "^": "BitXor", "<<": "Shl", ">>": "Shr",
}
CMP_OPS = {"<", "<=", ">", ">=", "==", "!=", "&&", "||"}


# --------------------------------------------------------------- helpers

def sub(text):
    """collapse whitespace runs -- declaration texts are hand-written."""
    return " ".join(text.split())


# ------------------------------------------------- holder type recovery
#
# Each recoverer returns (type_spelling, [prelude fragments], reason).
# reason is None on success and a sentence on refusal.

RUST_ANNOT = re.compile(r"\blet\s+(?:mut\s+)?v\s*:\s*(.+?)\s*=")
RUST_BARE = re.compile(r"\blet\s+(?:mut\s+)?v\s*=\s*([A-Za-z_]\w*)\s*[({;:]")
RUST_LET = re.compile(r"\blet\s+(?:mut\s+)?v\b")


def recover_rust(h, decl):
    pre = [ln.strip() for ln in (h.get("pre") or "").splitlines()
           if ln.strip().startswith("use ")]
    m = RUST_LET.search(decl)
    head = decl[:m.start()] if m else ""
    tail = decl[m.start():] if m else decl
    for frag in head.split(";"):
        frag = frag.strip()
        if not frag:
            continue
        if frag.startswith("use "):
            pre.append(frag + ";")
        else:
            pre.append(frag)
    a = RUST_ANNOT.search(tail)
    if a:
        return sub(a.group(1)), pre, None
    b = RUST_BARE.search(tail)
    if b:
        return b.group(1), pre, None
    return None, [], ("no type annotation and no named type in %r -- the "
                      "type is inferred, and inferring it here would be a "
                      "guess" % sub(decl)[:90])


# cpp: the last `<type> v =` or `<type> v{` in the declaration text.  A
# `{` or a `;` cannot occur inside a type spelling, so whatever precedes
# the winning match is a local type declaration that must be hoisted.
CPP_DECL = re.compile(r"([A-Za-z_][A-Za-z_0-9:<>,\s\*&]*?)\s*\bv\s*(=|\{)")


def recover_cpp(h, decl):
    incs = [ln.strip() for ln in (h.get("pre") or "").splitlines()
            if ln.strip().startswith("#include")]
    ms = list(CPP_DECL.finditer(decl))
    if not ms:
        return None, [], ("no `<type> v =` in %r -- a C array parameter "
                          "would decay to a pointer and change the "
                          "operation being measured" % sub(decl)[:90])
    m = ms[0]
    ty = sub(m.group(1))
    if ty in ("auto", "const auto", "auto&", "const auto&"):
        return None, [], ("declared `auto` in %r -- the type is deduced, "
                          "and `auto` is not a parameter type spelling"
                          % sub(decl)[:90])
    pre = list(incs)
    head = decl[:m.start()].strip()
    if head:
        pre.append(head)
    # a bare identifier type may be declared in the holder's own pre block
    if re.fullmatch(r"[A-Za-z_]\w*", ty) and not ty.startswith("std"):
        block = (h.get("pre") or "").strip()
        if block and re.search(r"\b(struct|class|using|typedef)\s+%s\b"
                               % re.escape(ty), block):
            pre = [block]
    return ty, pre, None


GO_VAR = re.compile(r"^\s*var\s+v\s+(.+?)\s*=", re.M)
GO_ASSIGN = re.compile(r"^\s*v\s*:=\s*(.+?)\s*$", re.M)


def go_literal_type(expr):
    """the type in front of a composite literal: []int64{...} -> []int64."""
    depth = 0
    for k, c in enumerate(expr):
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
        elif c == "{" and depth == 0:
            return expr[:k].strip() or None
    return None


def recover_go(h, decl):
    pre = []
    for ln in decl.splitlines():
        if ln.strip().startswith("type "):
            pre.append(ln.strip())
    m = GO_VAR.search(decl)
    ty = None
    if m:
        ty = sub(m.group(1))
    else:
        a = GO_ASSIGN.search(decl)
        if a:
            ty = go_literal_type(a.group(1))
            if ty:
                ty = sub(ty)
    if not ty:
        return None, [], ("no `var v <type>` and no composite literal in "
                          "%r -- the type is only known to the library "
                          "that returns it" % sub(decl)[:90])
    # an import is carried only when the type spelling actually names it
    for ln in (h.get("pre") or "").splitlines():
        q = re.findall(r'"([^"]+)"', ln)
        for path in q:
            if path.split("/")[-1] + "." in ty:
                pre.append('import "%s"' % path)
    return ty, pre, None


SWIFT_ANNOT = re.compile(r"^\s*let\s+v\s*:\s*(.+?)\s*=", re.M)
SWIFT_BARE = re.compile(r"^\s*let\s+v\s*=\s*([A-Za-z_]\w*)\s*[.(]", re.M)
SWIFT_TYPEDECL = re.compile(
    r"^\s*(?:indirect\s+|final\s+|public\s+)*(?:struct|class|enum)\s+\w+")


def recover_swift(h, decl):
    pre = [ln.strip() for ln in decl.splitlines()
           if SWIFT_TYPEDECL.match(ln)]
    a = SWIFT_ANNOT.search(decl)
    if a:
        return sub(a.group(1)), pre, None
    b = SWIFT_BARE.search(decl)
    if b:
        return b.group(1), pre, None
    return None, [], ("no type annotation and no named type in %r -- the "
                      "type is inferred, and inferring it here would be a "
                      "guess" % sub(decl)[:90])


RECOVER = dict(cpp=recover_cpp, rust=recover_rust, go=recover_go,
               swift=recover_swift)


# ------------------------------------------------- hand-supplied spellings
#
# The recoverers above read a spelling OUT of the declaration text.  A
# few holders were written in a way that hides a spelling which
# nonetheless exists -- `auto v = std::make_tuple(...)` names a real
# type, it simply declines to write it down.  Refusing those units
# threw away 82 measurements to protect against a guess that was not
# actually being made, so each one is spelled here by hand, with the
# justification attached and the compiler as the arbiter: a spelling
# that does not compile comes back as BUILDFAIL carrying the compiler's
# own words, never as a silent omission.
#
# `param` is the parameter DECLARATION template and `{n}` is the
# parameter name.  It is a separate field from `type` because C++'s
# reference-to-array declarator wraps the name -- `int64_t (&a)[3]` --
# rather than preceding it, so "type" and "how you write a parameter of
# that type" are genuinely two different strings there.
#
# A holder may list MORE THAN ONE variant.  The first is primary; the
# rest become additional arch-units tagged with their own spelling, and
# they never replace the primary.

SPELLED = {
    ("cpp", 14): [
        dict(tag="ref", type="int64_t (&)[3]", param="int64_t (&{n})[3]",
             pre=["#include <cstdint>"],
             why="reference-to-array preserves BOTH the element type and "
                 "the extent, which is the array-ness the holder exists "
                 "to represent"),
        dict(tag="decayed", type="int64_t*", param="int64_t* {n}",
             pre=["#include <cstdint>"],
             why="the decayed pointer form -- what ordinary C++ actually "
                 "passes; recorded alongside the reference form, not "
                 "instead of it"),
    ],
    ("cpp", 18): [
        dict(tag="plain", type="std::tuple<int64_t,int64_t,int64_t>",
             param=None,
             pre=["#include <tuple>", "#include <cstdint>"],
             why="`std::make_tuple((int64_t)1,(int64_t)2,(int64_t)3)` has "
                 "exactly this return type; only the declaration said "
                 "`auto`"),
    ],
    ("rust", 16): [
        dict(tag="plain", type="(i64, i64, i64)", param=None, pre=[],
             why="`(1i64, 2i64, 3i64)` is a fully suffixed literal, so no "
                 "inference is involved in reading its type off"),
    ],
    ("swift", 16): [
        dict(tag="plain", type="(Int, Int, Int)", param=None, pre=[],
             why="an unsuffixed swift integer literal defaults to Int, so "
                 "`(1, 2, 3)` is (Int, Int, Int)"),
    ],
    ("go", 15): [
        dict(tag="plain", type="*list.List", param=None,
             pre=['import "container/list"'],
             why="`container/list.New()` is declared to return *list.List; "
                 "the type is in the library's signature, not hidden"),
    ],
}


def variants_for(lang, n, ty, pre):
    """the spelling variants a holder offers, primary first.  A holder
    with no recovered type and no hand spelling offers none, and that is
    what keeps its units skipped."""
    sp = SPELLED.get((lang, n))
    if sp:
        return [dict(tag=v["tag"], type=v["type"], param=v["param"],
                     pre=list(v["pre"]), why=v["why"]) for v in sp]
    if ty is None:
        return []
    return [dict(tag="plain", type=ty, param=None, pre=list(pre), why=None)]


def holder_types(lang):
    """holder index -> {type, pre, form, rep, reason, variants}."""
    hs, _spell = L3.holders(lang)
    out = []
    for n, h in enumerate(hs):
        _vc, decl = L3.base_value(h)
        ty, pre, why = RECOVER[lang](h, decl)
        vs = variants_for(lang, n, ty, pre)
        rec = dict(i=n, form=h["form"], rep=h["rep"], decl=sub(decl),
                   type=ty, pre=pre, reason=why, variants=vs,
                   hand_spelled=bool(SPELLED.get((lang, n))))
        if rec["hand_spelled"]:
            rec["type"] = vs[0]["type"]
            rec["pre"] = list(vs[0]["pre"])
            rec["reason"] = None
            rec["hand_spelling_why"] = vs[0]["why"]
        out.append(rec)
    return out


def param_of(v, name):
    """how a parameter of this variant's type is written."""
    if v["param"]:
        return v["param"].replace("{n}", name)
    return "%s %s" % (v["type"], name)


# ------------------------------------------------------ the result type

def result_type(lang, op, lt, rt):
    """the spelling of what the operator hands back, derived by the
    language's own rule.  Never guessed from the operand kind."""
    if lang == "cpp":
        return None                       # `auto` deduction does the work
    if lang == "rust":
        if op in CMP_OPS:
            return "bool"
        if op == "..":
            return "core::ops::Range<%s>" % lt
        tr = RUST_TRAIT.get(op)
        if tr is None:
            return None
        return "<%s as core::ops::%s<%s>>::Output" % (lt, tr, rt)
    if lang in ("go", "swift"):
        if op in CMP_OPS:
            return "bool" if lang == "go" else "Bool"
        return lt                          # arithmetic/bitwise/shift: lhs
    raise KeyError(lang)


# ------------------------------------------------- rust borrow lifetimes

RUST_LIFETIME = "'a"


def rust_needs_lifetime(lt, rt, res):
    """RULE.  rust elides a borrow's lifetime in RETURN position only
    when the input list offers exactly one source to elide to.  Two
    operands that both carry a borrow -- `a: &str, b: &str` -- give the
    elider two candidates and no rule for choosing, so it refuses with
    E0106 instead.  `..` on `&str` and on `&[i64]` are exactly that
    shape: the return type `core::ops::Range<&str>` names a borrow whose
    source the signature never states.

    The condition is mechanical and is read off the spellings, not
    guessed: the result type must itself name a borrow, and the operand
    list must offer other than exactly one.  Where the count IS one --
    `String + &str` -- elision already has its unique answer and the
    signature is left exactly as it was."""
    if "&" not in (res or ""):
        return False
    return (lt.count("&") + rt.count("&")) != 1


def rust_bind_lifetime(spelling):
    """name every borrow in a type spelling with the one lifetime the
    signature declares.  `&str` becomes `&'a str`, `&[i64]` becomes
    `&'a [i64]`.  Purely a naming of what was already there: a lifetime
    is erased before code generation, so the machine code an annotated
    unit compiles to is the code the un-annotated one would have
    compiled to had it been accepted."""
    return re.sub(r"&(?!\s*')", "&%s " % RUST_LIFETIME, spelling)


# ------------------------------------------------------ source emission

def emit_cpp(n, op, pa, pb, pre):
    head = ["#include <compare>", "#include <cstdint>"]
    for p in pre:
        if p not in head:
            head.append(p)
    return ("// arch unit %d -- %s\n%s\n\nextern \"C\" auto af_%d(%s, %s) "
            "{ return a %s b; }\n"
            % (n, op, "\n".join(head), n, pa, pb, op))


def emit_rust(n, op, lt, rt, pre, res):
    """Returns (source, lifetime_bound).  The lifetime parameter has to
    be declared on the function HEAD as well as spelled inside the
    operand and result types, which is why it is applied here rather
    than in result_type() -- that function is handed no signature to
    add a parameter to."""
    seen, head = set(), []
    for p in pre:
        if p not in seen:
            seen.add(p)
            head.append(p)
    gen = ""
    bound = rust_needs_lifetime(lt, rt, res)
    if bound:
        gen = "<%s>" % RUST_LIFETIME
        lt = rust_bind_lifetime(lt)
        rt = rust_bind_lifetime(rt)
        res = rust_bind_lifetime(res)
    return ("// arch unit %d -- %s\n%s\n\n#[no_mangle]\npub fn af_%d%s(a: %s, "
            "b: %s) -> %s { a %s b }\n"
            % (n, op, "\n".join(head), n, gen, lt, rt, res, op), bound)


def emit_go(n, op, lt, rt, pre, res):
    seen, imps, decls = set(), [], []
    for p in pre:
        if p in seen:
            continue
        seen.add(p)
        (imps if p.startswith("import ") else decls).append(p)
    head = ["package main", "", "import \"fmt\""] + imps + [""] + decls
    return ("// arch unit %d -- %s\n%s\n\n//go:noinline\nfunc af_%d(a %s, "
            "b %s) %s { return a %s b }\n\nvar ga %s\nvar gb %s\n"
            "var sink interface{}\n\nfunc main() {\n\tsink = af_%d(ga, gb)"
            "\n\tfmt.Println(sink)\n}\n"
            % (n, op, "\n".join(head), n, lt, rt, res, op, lt, rt, n))


def emit_swift(n, op, lt, rt, pre, res, cdecl):
    seen, head = set(), []
    for p in pre:
        if p not in seen:
            seen.add(p)
            head.append(p)
    tag = "@_cdecl(\"af_%d\")\n" % n if cdecl else ""
    return ("// arch unit %d -- %s\n%s\n\n%spublic func af_%d(_ a: %s, "
            "_ b: %s) -> %s { return a %s b }\n"
            % (n, op, "\n".join(head), tag, n, lt, rt, res, op))


# ---------------------------------------------------------- unit build

def accepted(lang):
    p = os.path.join(HERE, "acceptance_%s_A2.json" % lang)
    d = json.load(open(p))
    out = []
    for key, cell in d["cells"].items():
        if cell["verdict"] != "ACCEPT":
            continue
        # the operator itself may contain a pipe -- `|||3|3` is `||` on
        # holder 3 against holder 3 -- so the split comes from the right
        op, i, j = key.rsplit("|", 2)
        out.append((op, int(i), int(j), cell))
    return out


# a secondary spelling of the same accepted triple gets its own unit
# number, offset far enough that it can never collide with a primary.
VARIANT_BASE = 100000


def build(lang):
    types = holder_types(lang)
    units, manifest = [], {}
    for n, (op, i, j, cell) in enumerate(accepted(lang)):
        ha, hb = types[i], types[j]
        base = dict(op=op, i=i, j=j,
                    lhs_rep=cell["lhs"]["holder"], rhs_rep=cell["rhs"]["holder"],
                    lhs_form=cell["lhs"]["form"], rhs_form=cell["rhs"]["form"])
        if not ha["variants"] or not hb["variants"]:
            bad = ha if not ha["variants"] else hb
            side = "lhs" if not ha["variants"] else "rhs"
            rec = dict(base)
            rec["emitted"] = False
            rec["skipped"] = ("%s holder %d (%s): %s"
                              % (side, bad["i"], bad["rep"], bad["reason"]))
            manifest[str(n)] = rec
            continue
        # slot 0 is the primary spelling of both sides.  A further slot
        # exists only when a side offers a second spelling, and then the
        # second spelling is taken on EVERY side that offers one, so the
        # two sides are never described inconsistently within one unit.
        slots = [(0, 0)]
        if len(ha["variants"]) > 1 or len(hb["variants"]) > 1:
            slots.append((min(1, len(ha["variants"]) - 1),
                          min(1, len(hb["variants"]) - 1)))
        for slot, (ka, kb) in enumerate(slots):
            va, vb = ha["variants"][ka], hb["variants"][kb]
            un = n if slot == 0 else VARIANT_BASE * slot + n
            rec = dict(base)
            rec["base_n"] = n
            rec["lhs_spelling"] = va["tag"]
            rec["rhs_spelling"] = vb["tag"]
            rec["spelling"] = (va["tag"] if va["tag"] != "plain"
                               else vb["tag"])
            lt, rt = va["type"], vb["type"]
            res = result_type(lang, op, lt, rt)
            if lang != "cpp" and res is None:
                rec["emitted"] = False
                rec["skipped"] = ("no result-type rule for operator %r in %s"
                                  % (op, lang))
                manifest[str(un)] = rec
                continue
            pre = list(va["pre"]) + list(vb["pre"])
            if lang == "cpp":
                src = emit_cpp(un, op, param_of(va, "a"), param_of(vb, "b"),
                               pre)
                sym, exact = "af_%d" % un, True
            elif lang == "rust":
                src, bound = emit_rust(un, op, lt, rt, pre, res)
                if bound:
                    rec["lifetime_bound"] = RUST_LIFETIME
                sym, exact = "af_%d" % un, True
            elif lang == "go":
                src = emit_go(un, op, lt, rt, pre, res)
                sym, exact = "main.af_%d" % un, True
            else:
                cdecl = (ha["form"] in SCALAR_FORMS
                         and hb["form"] in SCALAR_FORMS)
                src = emit_swift(un, op, lt, rt, pre, res, cdecl)
                sym, exact = "af_%d" % un, cdecl
            rec["emitted"] = True
            rec["lhs_type"] = lt
            rec["rhs_type"] = rt
            rec["result_type"] = res
            rec["symbol"] = sym
            manifest[str(un)] = rec
            units.append(dict(n=un, src=src, sym=sym, exact=exact))
    return types, units, manifest


# ------------------------------------------------------------- the lane

DRIVER = r'''
import json, os, re, shutil, subprocess, sys, time

ROOT = sys.argv[1]
T = json.load(open(os.path.join(ROOT, "table.json")))
LANG = T["language"]
UNITS = T["units"]
OUT = T["out"]
out = open(OUT, "w")
WORK = os.path.join(ROOT, "u")

print("arch lane %s: %d units" % (LANG, len(UNITS)))
sys.stdout.flush()


def sh(cmd, cwd=None, timeout=120):
    try:
        p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=timeout)
        return (p.returncode,
                p.stdout.decode("utf-8", "replace"),
                p.stderr.decode("utf-8", "replace"))
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT after %ds" % timeout
    except OSError as e:
        return 125, "", "OSError %s" % e


LABEL = re.compile(r"^([0-9a-f]+)\s+<(.+)>:\s*$")
INSN = re.compile(r"^\s*([0-9a-f]+):\t(.*)$")
# objdump -dr prints a relocation on its own line under the instruction
# it applies to:  "\t\t\t1d: R_X86_64_PLT32\t_ZSt...-0x4".  A colon
# followed by a SPACE, where an instruction line has a colon followed by
# a TAB, is what tells the two apart.
RELOC = re.compile(r"^\s+([0-9a-f]+): (R_\S+)\t(.+?)\s*$")


def extract(text, sym, exact):
    """the three columns for one symbol.

    bytes   every byte objdump printed, in order, flattened
    mnem    the instruction text, VERBATIM apart from objdump's own
            trailing `# ...` comment, which is arithmetic objdump did
            for the reader and not part of the instruction.  The
            `<symbol+offset>` annotation is KEPT: on a linked go binary
            it is the only place the name `runtime.morestack_noctxt`
            appears, and a name is not something a later stage can
            invent.  Anything that needs stripping gets stripped in
            arch_read.py, which is where the canonical column lives.
            An instruction that carries a RELOCATION gets the
            relocation appended as ` !!reloc=<type>:<symbol>`.  In an
            object file the call displacement is literally zero and the
            callee's name lives only in the relocation, so without this
            a go unit would keep `call runtime.concatstring2` while the
            same call from clang or rustc read `call ADDR` -- an
            asymmetry in the record, invented by the harness rather than
            by the compilers.  `!!` is used because objdump never emits
            it.
    layout  `<address>:<byte count>` per instruction, so a reader can
            say which bytes belong to which instruction and how far a
            branch jumps from where it stands.  A continuation line
            carries bytes and no text; its bytes fold into the
            instruction above it, in both columns.
    """
    lines = text.splitlines()
    k = -1
    for idx, ln in enumerate(lines):
        m = LABEL.match(ln)
        if not m:
            continue
        lab = m.group(2)
        if (lab == sym) if exact else (sym in lab):
            k = idx
            break
    if k < 0:
        return None
    raw, mn, lay = [], [], []
    for ln in lines[k + 1:]:
        if LABEL.match(ln):
            break
        m = INSN.match(ln)
        if not m:
            r = RELOC.match(ln)
            if r and mn:
                mn[-1] = "%s !!reloc=%s:%s" % (mn[-1], r.group(2), r.group(3))
            continue
        addr = m.group(1)
        parts = m.group(2).split("\t")
        bs = parts[0].split()
        raw.extend(bs)
        txt = parts[1] if len(parts) > 1 else ""
        txt = txt.split("#")[0]
        txt = " ".join(txt.split())
        if txt:
            mn.append(txt)
            lay.append([addr, len(bs)])
        elif lay:
            lay[-1][1] += len(bs)
    return raw, mn, lay


def disasm(obj, sym, exact):
    rc, so, se = sh(["objdump", "-dr", "--disassemble=" + sym, obj])
    got = extract(so, sym, exact) if rc == 0 else None
    if got is None:
        rc, so, se = sh(["objdump", "-dr", obj], timeout=600)
        got = extract(so, sym, exact)
    return got


GOMOD = "module archunit\n\ngo 1.26\n"


def compile_unit(u, d):
    if LANG == "cpp":
        src = os.path.join(d, "unit.cpp")
        obj = os.path.join(d, "unit.o")
        open(src, "w").write(u["src"])
        rc, so, se = sh(["/usr/bin/clang++", "-std=c++20", "-O1",
                         "-c", src, "-o", obj])
        return rc, obj, (se or so)
    if LANG == "rust":
        src = os.path.join(d, "unit.rs")
        obj = os.path.join(d, "unit.o")
        open(src, "w").write(u["src"])
        rc, so, se = sh(["rustc", "--crate-type=lib", "--emit=obj",
                         "-C", "opt-level=1", "-C", "debug-assertions=off",
                         "-o", obj, src])
        return rc, obj, (se or so)
    if LANG == "go":
        open(os.path.join(d, "go.mod"), "w").write(GOMOD)
        open(os.path.join(d, "main.go"), "w").write(u["src"])
        obj = os.path.join(d, "bin")
        rc, so, se = sh(["go", "build", "-o", obj, "."], cwd=d, timeout=300)
        return rc, obj, (se or so)
    if LANG == "swift":
        src = os.path.join(d, "unit.swift")
        obj = os.path.join(d, "unit.o")
        open(src, "w").write(u["src"])
        rc, so, se = sh(["/persist/swift/usr/bin/swiftc", "-O", "-c",
                         src, "-o", obj], timeout=300)
        return rc, obj, (se or so)
    raise KeyError(LANG)


def firstline(txt):
    """the compiler's own words for why it refused.  The FIRST line is
    not reliably the reason -- clang leads with a -W warning and puts
    the error underneath it -- so the first line that actually says
    `error` wins, and the plain first line is the fallback when nothing
    does."""
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    for ln in lines:
        if re.search(r"\berror\b", ln, re.I):
            return ln.replace("|", "/")[:200]
    return lines[0].replace("|", "/")[:200] if lines else "(no diagnostic)"


t0 = time.time()
tally = {"OK": 0, "BUILDFAIL": 0, "NOSYM": 0}
for k, u in enumerate(UNITS):
    d = os.path.join(WORK, "n%d" % u["n"])
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    rc, obj, err = compile_unit(u, d)
    if rc != 0 or not os.path.exists(obj):
        out.write("af_%d|BUILDFAIL|%s\n" % (u["n"], firstline(err)))
        tally["BUILDFAIL"] += 1
    else:
        got = disasm(obj, u["sym"], u["exact"])
        if got is None:
            rc2, so2, se2 = sh(["objdump", "-t", obj])
            hit = [l for l in so2.splitlines() if u["sym"] in l]
            out.write("af_%d|NOSYM|symbol %s absent; %d near matches\n"
                      % (u["n"], u["sym"], len(hit)))
            tally["NOSYM"] += 1
        else:
            raw, mn, lay = got
            out.write("af_%d|OK|%s|%s|%s\n"
                      % (u["n"], " ".join(raw), ";".join(mn),
                         ";".join("%s:%d" % (a, c) for a, c in lay)))
            tally["OK"] += 1
    out.flush()
    shutil.rmtree(d, ignore_errors=True)
    if (k + 1) % 50 == 0 or (k + 1) == len(UNITS):
        el = time.time() - t0
        print("[progress] %s [%d/%d] elapsed %.1fs  mean %.2fs  "
              "OK %d BUILDFAIL %d NOSYM %d"
              % (LANG, k + 1, len(UNITS), el, el / (k + 1),
                 tally["OK"], tally["BUILDFAIL"], tally["NOSYM"]))
        sys.stdout.flush()

out.close()
print("done: OK %d BUILDFAIL %d NOSYM %d -> %s"
      % (tally["OK"], tally["BUILDFAIL"], tally["NOSYM"], OUT))
'''


TOOLCHECK = {
    "cpp": ("/usr/bin/clang++ --version",
            "/usr/bin/clang++ is not runnable in this container"),
    "rust": ("rustc --version", "rustc is not runnable in this container"),
    "go": ("go version", "go is not runnable in this container"),
    "swift": ("/persist/swift/usr/bin/swiftc --version",
              "swiftc is not runnable in this container"),
}


def payload(obj):
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as g:
        g.write(json.dumps(obj).encode("utf-8"))
    b = base64.b64encode(buf.getvalue()).decode("ascii")
    return "\n".join(b[k:k + 76] for k in range(0, len(b), 76))


def lane(lang, name, units, outname):
    check, why = TOOLCHECK[lang]
    table = dict(language=lang, out="/out/%s.txt" % outname, units=units)
    body = []
    body.append("#!/bin/sh")
    body.append("# layer-3 ARCH lane -- %s -- generated by" % lang)
    body.append("# Research/kind_fuzz_clustering/arch_gen.py .  "
                "Do not hand-edit.")
    body.append("# One compiled function per arch-unit: the operator applied")
    body.append("# to two PARAMETERS, never to constants, so the operation")
    body.append("# survives to the object file.  objdump is the single")
    body.append("# disassembler for every language here.")
    body.append("set -u")
    body.append("export HOME=/work")
    body.append("export PATH=/persist/dart-sdk/bin:$PATH")
    body.append("export GOTOOLCHAIN=local")
    body.append("export GOPROXY=off")
    body.append("export GOFLAGS=-mod=mod")
    body.append("ROOT=/work/%s" % name)
    body.append("export GOCACHE=\"$ROOT/gocache\"")
    body.append("export GOPATH=\"$ROOT/gopath\"")
    body.append("# swift's binaries want libncurses.so.6 and the image ships")
    body.append("# only libncursesw.so.6.6; the symlink lives in the image's")
    body.append("# own /usr/lib and does NOT survive a container restart.")
    body.append("if [ -f /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 ]; then")
    body.append("  ln -sf /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 \\")
    body.append("     /usr/lib/x86_64-linux-gnu/libncurses.so.6 2>/dev/null")
    body.append("  ldconfig 2>/dev/null")
    body.append("fi")
    body.append("echo \"=== layer-3 ARCH -- %s -- %d units ===\""
                % (lang, len(units)))
    body.append("date -u +%Y-%m-%dT%H:%M:%SZ")
    body.append("# refuse in seconds rather than in an hour")
    body.append("if ! %s >/dev/null 2>&1; then" % check)
    body.append("  echo \"!! REFUSING TO START: %s.\"" % why)
    body.append("  echo \"!! tried: %s\"" % check)
    body.append("  exit 4")
    body.append("fi")
    body.append("%s 2>&1 | head -2" % check)
    body.append("if ! objdump --version >/dev/null 2>&1; then")
    body.append("  echo \"!! REFUSING TO START: objdump is not runnable.\"")
    body.append("  exit 4")
    body.append("fi")
    body.append("objdump --version 2>&1 | head -1")
    body.append("rm -rf \"$ROOT\"; mkdir -p \"$ROOT\" \"$GOCACHE\" \"$GOPATH\"")
    body.append("df -Pm /work | awk 'NR==2{print \"free /work: \" $4 \" MB\"}'")
    body.append("FREE=`df -Pm /work | awk 'NR==2{print $4}'`")
    body.append("if [ \"$FREE\" -lt 400 ]; then")
    body.append("  echo \"!! REFUSING TO START: only $FREE MB free on /work,"
                " need 400\"")
    body.append("  exit 3")
    body.append("fi")
    body.append("base64 -d <<'T_EOF' | gunzip > \"$ROOT/table.json\"")
    body.append(payload(table))
    body.append("T_EOF")
    body.append("echo \"payload bytes: $(wc -c < \"$ROOT/table.json\")\"")
    body.append("python3 - \"$ROOT\" <<'PY_EOF'")
    body.append(DRIVER)
    body.append("PY_EOF")
    body.append("echo \"--- lane finished, rc=$?\"")
    body.append("date -u +%Y-%m-%dT%H:%M:%SZ")
    return "\n".join(body) + "\n"


# ------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("langs", nargs="+")
    ap.add_argument("--smoke", type=int, default=0,
                    help="keep only the first N emitted units")
    ap.add_argument("--also", action="append", default=[],
                    help="op,i,j -- force this unit into a smoke lane")
    ap.add_argument("--holders", default=None,
                    help="comma separated holder indices; keep only units "
                         "that touch one of them (verification smoke for a "
                         "newly spelled holder)")
    ap.add_argument("--name", default=None, help="lane base name")
    ap.add_argument("--drop", action="store_true",
                    help="also write the lane into Airlock's drop directory")
    args = ap.parse_args()

    for lang in args.langs:
        if lang not in LANGS:
            print("skip %s -- no arch template" % lang)
            continue
        types, units, manifest = build(lang)

        print("== %s: holder index -> type spelling" % lang)
        for t in types:
            if not t["variants"]:
                print("  %2d %-12s %-42s UNSUPPORTED -- %s"
                      % (t["i"], t["form"], t["rep"], t["reason"]))
            else:
                tags = ", ".join("%s=%s" % (v["tag"], v["type"])
                                 for v in t["variants"])
                mark = "  [hand-spelled]" if t["hand_spelled"] else ""
                print("  %2d %-12s %-42s %s%s"
                      % (t["i"], t["form"], t["rep"],
                         t["type"] if len(t["variants"]) == 1 else tags, mark))
        skipped = [k for k, v in manifest.items() if not v["emitted"]]
        extra = [u for u in units if u["n"] >= VARIANT_BASE]
        print("   %d accepted triples, %d units emitted (%d of them a second"
              " spelling), %d skipped"
              % (len(manifest) - len(extra), len(units), len(extra),
                 len(skipped)))

        mpath = os.path.join(HERE, "arch_manifest_%s.json" % lang)
        json.dump(dict(language=lang,
                       accepted=len(manifest),
                       emitted=len(units),
                       skipped=len(skipped),
                       holder_types=[{k: t[k] for k in
                                      ("i", "form", "rep", "type", "reason",
                                       "variants", "hand_spelled")}
                                     for t in types],
                       units=manifest),
                  open(mpath, "w"), indent=1)
        print("   wrote %s" % mpath)

        keep = units
        if args.holders:
            want = set(int(x) for x in args.holders.split(",") if x.strip())
            keep = [u for u in keep
                    if manifest[str(u["n"])]["i"] in want
                    or manifest[str(u["n"])]["j"] in want]
            print("   holders %s: %d units" % (sorted(want), len(keep)))
            units = keep
        if args.smoke:
            want = set()
            for spec in args.also:
                op, i, j = spec.rsplit(",", 2)
                want.add((op, int(i), int(j)))
            head = units[:args.smoke]
            have = set(u["n"] for u in head)
            extra = [u for u in units
                     if u["n"] not in have
                     and (manifest[str(u["n"])]["op"],
                          manifest[str(u["n"])]["i"],
                          manifest[str(u["n"])]["j"]) in want]
            keep = head + extra
            print("   smoke: %d units (%d head + %d forced)"
                  % (len(keep), len(head), len(extra)))

        name = args.name or ("arch_%s" % lang)
        text = lane(lang, name, keep, name)
        lpath = os.path.join(HERE, "lanes", "%s.sh" % name)
        open(lpath, "w").write(text)
        os.chmod(lpath, 0o755)
        print("   wrote %s (%d bytes)" % (lpath, len(text)))
        if args.drop:
            dpath = os.path.join(DROP, "%s.sh" % name)
            open(dpath, "w").write(text)
            print("   dropped %s" % dpath)


if __name__ == "__main__":
    main()
