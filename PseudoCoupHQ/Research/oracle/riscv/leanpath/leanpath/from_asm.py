"""Step 2 without the decoder.

An arch-unit is a sequence of arch-opcodes and every arch-opcode has a Lean
expression, so the unit's expression is those composed.  The one thing that
needs saying is WHICH arch-opcode a line is, with which operands.

`walk.py` asks Sail's own decoder, in Lean, on the instruction word.  That
decoder is `noncomputable` in the proof emit, so `#eval` cannot run it, and
the walk has always needed a second executable emit of the model to get it.

It is not needed.  llvm-objdump already named the mnemonic and the operands,
and the model's own `assembly_forwards` clause says, per constructor, exactly
which operand sits in which position -- the same clause `SailModel.key_of`
already reads for the mnemonic.  Reading the REST of that clause turns a
disassembly line back into (constructor, components), which is what the
decoder would have returned.  Nothing here is written by hand: every pattern
comes out of the emitted model.
"""
import glob
import os
import re

ASM = (r'^def assembly_forwards \(arg_ : instruction\) : SailM String := do\n'
       r'  match arg_ with\n(.*?)(?=\n\n)')

# the pieces an assembly clause is built from
TOK = re.compile(
    r'"([^"]*)"'                                          # 1 literal
    r'|\(?←? ?\(?(spc|sep|opt_spc)_forwards \(\)\)?'      # 2 separator
    r'|\(?←? ?\(?([A-Za-z0-9_]*(?:reg|freg)[A-Za-z0-9_]*_name[A-Za-z0-9_]*)'
    r'_forwards ([A-Za-z0-9_]+)\)?'                       # 3 kind 4 arg
    r'|\(?←? ?\(?(hex_bits[A-Za-z0-9_]*)_forwards '
    r'(\((?:[^()]|\((?:[^()]|\([^()]*\))*\))*\)'
    r'|[A-Za-z0-9_]+)'                                    # 6 arg
    r'|\(?←? ?\(?([A-Za-z0-9_]+_forwards) \(\)\)?'         # 7 nullary
    r'|\(?←? ?\(?([A-Za-z0-9_]+_forwards) ([A-Za-z0-9_]+)\)?')   # 8 map 9 arg

HEX = re.compile(r'hex_bits_(?:signed_)?(\d+)')
BITS = re.compile(r'^0b([01]+)$')
FLI = re.compile(r'^(?:noncomputable )?def execute_(FLI_[HSD]) \([^\n]*\n'
                 r'(.*?)(?=\n\ndef )', re.M | re.S)
# `((uimm : (BitVec 6)) +++ 0b000#3)` -- printed value is uimm shifted up
CONCAT = re.compile(r'\(?\(?([A-Za-z0-9_]+)\s*:\s*\(BitVec (\d+)\)\)?'
                    r'\s*\+\+\+\s*0b([01]+)#\d+')


def _imm_arg(tok):
    """(argument name, bits the printed value is shifted up by, its width)."""
    tok = tok.strip()
    m = CONCAT.search(tok)
    if m:
        return m.group(1), len(m.group(3)), int(m.group(2))
    m = re.search(r'([A-Za-z0-9_]+)', tok)
    return (m.group(1) if m else tok), 0, None


def model_text(lean_dir):
    return "".join(open(f).read() for f in sorted(glob.glob(
        os.path.join(lean_dir, "*.lean"))))


def literal_map(text, name):
    """`def <name> ... match arg_ with | <pat> => "<s>"` -> {pat: s}."""
    m = re.search(r'^(?:noncomputable )?def %s \([^\n]*\n(.*?)(?=\n\n)'
                  % re.escape(name), text, re.M | re.S)
    if not m:
        return {}
    return {p.strip(): s for p, s in
            re.findall(r'\| (.+?) => \(?(?:pure )?"([^"]*)"\)?', m.group(1))}


def _named(text, which):
    out, wild, width = {}, None, 5
    for pat, s in literal_map(text, which).items():
        b = BITS.match(pat.strip())
        if b:
            out[s] = int(b.group(1), 2)
            width = len(b.group(1))
        elif pat.strip() == "_":
            wild = s
    if wild is not None and wild not in out:
        left = set(range(1 << width)) - set(out.values())
        if len(left) == 1:
            out[wild] = left.pop()
    return out


def abi_names(text):
    """register number -> the name objdump prints."""
    out = {}
    for pat, s in literal_map(text, "reg_abi_name_raw_forwards").items():
        b = BITS.match(pat.strip())
        if b:
            out[s] = int(b.group(1), 2)
    return out


def mnemonic_maps(text):
    """map name -> {pattern: string}.  Sail writes some of these under a
    `get_config_use_abi_names` guard, which the plain clause regex misses, so
    the `_backwards` direction is read too: it is a clean string table and it
    is the direction a disassembly line needs anyway."""
    maps = {}
    for m in re.finditer(r'^def ([A-Za-z0-9_]+_forwards) \(arg_ : [^)]*\)'
                         r' : (?:SailM )?String :=(?: do)?\n(.*?)(?=\n\n)',
                         text, re.M | re.S):
        table = {p.strip(): s for p, s in
                 re.findall(r'\| (.+?) => \(?(?:pure )?"([^"]*)"\)?', m.group(2))}
        if table:
            maps[m.group(1)] = table
    for m in re.finditer(r'^def ([A-Za-z0-9_]+)_backwards \(arg_ : String\)'
                         r' : (?:SailM )?[A-Za-z0-9_ ()]+ :=(?: do)?\n(.*?)(?=\n\n)',
                         text, re.M | re.S):
        table = {}
        for s_, v in re.findall(r'\| "([^"]*)" => \(?(?:pure )?([A-Za-z0-9_.]+)\)?',
                                m.group(2)):
            table[v.strip()] = s_
        # the backwards table names every string, where a forwards table can
        # end in `| _ => "d"` and leave that value unrecoverable
        name = m.group(1) + "_forwards"
        if table:
            merged = dict(maps.get(name, {}))
            merged.update(table)
            maps[name] = merged
    return maps


def nullary_literal(text, name):
    """`X_forwards ()` -- a guarded def whose first string literal is the ABI
    spelling objdump prints."""
    m = re.search(r'^(?:noncomputable )?def %s \(arg_ : Unit\)[^\n]*\n(.*?)(?=\n\n)'
                  % re.escape(name), text, re.M | re.S)
    if not m:
        return None
    lit = re.search(r'"([^"]+)"', m.group(1))
    return lit.group(1) if lit else None


def fli_tables(text):
    """FLI_D and friends spell their operand as a 5-bit index, and objdump
    prints the VALUE that index stands for.  The model's own execute clause
    carries the table, so the inverse is read from it, never written out."""
    out = {}
    for m in FLI.finditer(text):
        table = {}
        for pat, val, _w in re.findall(
                r'\| (0b[01]+) => (0x[0-9A-Fa-f]+)#(\d+)', m.group(2)):
            table[int(val, 16)] = int(pat[2:], 2)
        if table:
            out[m.group(1)] = table
    return out


def _as_bits(text, width):
    """the float objdump printed, as the bit pattern of that width."""
    import struct
    try:
        v = float(text)
    except ValueError:
        return None
    if width == 64:
        return struct.unpack("<Q", struct.pack("<d", v))[0]
    if width == 32:
        return struct.unpack("<I", struct.pack("<f", v))[0]
    if width == 16:
        return struct.unpack("<H", struct.pack("<e", v))[0]
    return None


def clauses(text):
    """constructor -> (argument names in constructor order, token list).

    A token is one of
      ("lit", s) ("spc",) ("sep",) ("opt",)
      ("reg", kind, arg) ("imm", width, arg) ("map", map_name, arg)
    """
    m = re.search(ASM, text, re.M | re.S)
    if not m:
        return {}
    out = {}
    for piece in re.split(r'\n  \| \.', m.group(1)):
        piece = piece.lstrip("| .")
        head = re.match(r'([A-Za-z0-9_]+)\s*(\(([^)]*)\)|([A-Za-z0-9_]+))?\s*=>',
                        piece)
        if not head:
            continue
        ctor = head.group(1)
        if head.group(3) is not None:
            args = [a.strip() for a in head.group(3).split(",") if a.strip()]
        elif head.group(4):
            args = [head.group(4)]
        else:
            args = []
        rest = piece[head.end():]
        # a guarded clause is `if g then <the assembly> else assert false`;
        # only the `then` branch spells anything
        for stop in ("\n      else\n", "\n        else\n", "assert false"):
            cut = rest.find(stop)
            if cut != -1:
                rest = rest[:cut]
        toks = []
        for t in TOK.finditer(rest):
            if t.group(1) is not None:
                if t.group(1):
                    toks.append(("lit", t.group(1)))
            elif t.group(2):
                toks.append({"spc": ("spc",), "sep": ("sep",),
                             "opt_spc": ("opt",)}[t.group(2)])
            elif t.group(3):
                toks.append(("reg", t.group(3), t.group(4)))
            elif t.group(5):
                w = HEX.search(t.group(5))
                arg, shift, src_w = _imm_arg(t.group(6))
                toks.append(("imm", int(w.group(1)) if w else None, arg,
                             shift, src_w))
            elif t.group(7):
                toks.append(("nul", t.group(7), None))
            elif t.group(8):
                toks.append(("map", t.group(8), t.group(9)))
        if toks:
            out.setdefault(ctor, []).append((args, toks))
    return out


class Reader(object):
    """turns one llvm-objdump line into (constructor, components)."""

    def __init__(self, lean_dir):
        text = model_text(lean_dir)
        self.regs = _named(text, "reg_abi_name_raw_forwards")
        self.fregs = _named(text, "freg_abi_name_raw_forwards")
        self.vregs = _named(text, "vreg_name_raw_forwards")
        self.maps = mnemonic_maps(text)
        self.text = text
        self._nul = {}
        self._rm = None
        self._rm_args = {}
        self.fli = fli_tables(text)
        self.clauses = clauses(text)
        self.rules = []
        self.unreadable = {}
        for ctor, arms in sorted(self.clauses.items()):
            for args, toks in arms:
                try:
                    self.rules.append((ctor, args) + self._rule(ctor, toks))
                except ValueError as why:
                    self.unreadable[ctor] = str(why)
        # longest mnemonic first: `c.addi4spn` must not lose to `c.addi`
        self.rules.sort(key=lambda r: -len(r[3]))

    def _rule(self, ctor, toks):
        """(compiled regex, the literal mnemonic prefix, [(group, token)])."""
        pat, binds, mnem_lit, seen_spc = ["^"], [], "", False
        for tok in toks:
            kind = tok[0]
            if kind == "lit":
                if not seen_spc:
                    mnem_lit += tok[1]
                pat.append(re.escape(tok[1]))
            elif kind == "spc":
                seen_spc = True
                pat.append(r"[ \t]+")
            elif kind == "sep":
                pat.append(r"\s*,\s*")
            elif kind == "opt":
                pat.append(r"\s*")
            elif kind in ("reg", "imm"):
                g = "g%d" % len(binds)
                binds.append(tok)
                pat.append(r"(?P<%s>[^,()\s]+)" % g)
            elif kind == "nul":
                if tok[1] not in self._nul:
                    self._nul[tok[1]] = nullary_literal(self.text, tok[1])
                lit = self._nul[tok[1]]
                if lit is None:
                    raise ValueError("no nullary %s" % tok[1])
                pat.append(re.escape(lit))
                if not seen_spc:
                    mnem_lit += lit
            elif kind == "map":
                table = self.maps.get(tok[1])
                if table is None:
                    raise ValueError("no map %s" % tok[1])
                g = "g%d" % len(binds)
                binds.append(tok)
                alts = sorted(set(table.values()), key=len, reverse=True)
                group = "(?P<%s>%s)" % (g, "|".join(re.escape(a)
                                                    for a in alts))
                if tok[1].startswith("frm_") and pat and pat[-1] == r"\s*,\s*":
                    # objdump prints no rounding mode when the architecture
                    # ignores it; the encoding still carries one
                    pat[-1] = r"(?:\s*,\s*" + group + ")?"
                    self._rm_args.setdefault(ctor, set()).add(tok[2])
                else:
                    pat.append(group)
                if not seen_spc:
                    mnem_lit += min(alts, key=len)
            else:
                raise ValueError("token %r" % (tok,))
        pat.append(r"\s*$")
        return re.compile("".join(pat)), mnem_lit, binds

    def rounding_modes(self):
        """the encoding the model gives each rounding mode: 0b111 -> .RM_DYN."""
        if self._rm is None:
            self._rm = {}
            for pat, v in re.findall(
                    r'\| (0b[01]+) => \(?(?:pure )?(RM_[A-Z]+)\)?',
                    re.search(r'^def encdec_rounding_mode_backwards \([^\n]*\n'
                              r'(.*?)(?=\n\n)', self.text,
                              re.M | re.S).group(1)):
                self._rm[int(pat[2:], 2)] = "." + v
        return self._rm

    def read(self, line, word=None):
        """word is the instruction's own encoding, when the record kept it.
        llvm-objdump omits an operand the architecture ignores -- fcvt.d.w's
        rounding mode, because that conversion is exact -- so the text alone
        cannot name every constructor argument.  The encoding can."""
        got = self._read(line)
        if got[0] is not None or word is None:
            return got
        return self._read(line, word)

    def _read(self, line, word=None):
        line = re.sub(r"\s*<[^>]*>\s*$", "", line.strip())
        for ctor, args, rx, _mn, binds in self.rules:
            m = rx.match(line)
            if not m:
                continue
            slot = {}
            ok = True
            for i, tok in enumerate(binds):
                got = m.group("g%d" % i)
                if got is None:
                    continue
                val = self._component(tok, got, ctor)
                if val is None:
                    ok = False
                    break
                slot[tok[2]] = val
            if not ok:
                continue
            if word is not None:
                # the one operand objdump leaves out is the rounding mode;
                # RISC-V carries it in bits 14:12 of the word
                for tok in binds:
                    pass
                for a in args:
                    if a in slot:
                        continue
                    if a in self._rm_args.get(ctor, ()):
                        rm = self.rounding_modes().get(
                            (int(word, 16) >> 12) & 0b111)
                        if rm is not None:
                            slot[a] = rm
            comps, ok2 = [], True
            for a in args:
                if a in slot:
                    comps.append(slot[a])
                    continue
                b = BITS.match(a.strip())
                if b:
                    comps.append("0x%0*x#%d" % ((len(b.group(1)) + 3) // 4,
                                                int(b.group(1), 2),
                                                len(b.group(1))))
                    continue
                ok2 = False
                break
            if not ok2:
                continue
            return ctor, comps, None
        return None, None, "no assembly clause matches %r" % line

    def _component(self, tok, got, ctor=None):
        kind = tok[0]
        if kind == "reg":
            compressed = "creg" in tok[1] or "cfreg" in tok[1]
            if got in self.fregs:
                n, holder = self.fregs[got], "fregidx.Fregidx"
                if compressed:
                    holder = "cfregidx.Cfregidx"
            elif got in self.vregs:
                n, holder = self.vregs[got], "vregidx.Vregidx"
            elif got in self.regs:
                n, holder = self.regs[got], "regidx.Regidx"
                if compressed:
                    holder = "cregidx.Cregidx"
            else:
                return None
            if holder.startswith(("cregidx", "cfregidx")):
                if not 8 <= n <= 15:
                    return None
                return "%s 0x%x#3" % (holder, n - 8)
            return "%s 0x%02x#5" % (holder, n)
        if kind == "imm":
            try:
                v = int(got, 0)
            except ValueError:
                table = self.fli.get(ctor or "")
                if table is None:
                    return None
                width = {"FLI_H": 16, "FLI_S": 32, "FLI_D": 64}[ctor]
                bits = _as_bits(got, width)
                if bits is None or bits not in table:
                    return None
                v = table[bits]
            shift, src_w = tok[3], tok[4]
            if shift:
                v = v >> shift
            w = src_w or tok[1] or 12
            return "0x%0*x#%d" % ((w + 3) // 4, v & ((1 << w) - 1), w)
        table = self.maps.get(tok[1], {})
        back = {}
        for pat, s in table.items():
            if pat.strip() == "_":      # a catch-all names no value
                continue
            back.setdefault(s, pat)
        pat = back.get(got)
        if pat is None:
            return None
        b = BITS.match(pat.strip())
        if b:
            return "0x%x#%d" % (int(b.group(1), 2), len(b.group(1)))
        if re.match(r'^\d+$', pat.strip()):
            return pat.strip()
        return pat.strip()
