import os
#!/usr/bin/env python3
"""Extract Sail primitive (external) val declarations and operator bindings
from (1) the Sail compiler library and (2) the sail-riscv model.

A primitive == a `val` whose declaration carries an EXTERNAL BODY rather than a
Sail `function` definition.  Spellings handled:
   val N = pure   {t: "s", ...} : T
   val N = monadic{t: "s", ...} : T
   val N = impure {t: "s", ...} : T
   val N = pure   "s"           : T
   val N = impure "s"           : T
   val N =        {t: "s", ...} : T     (no purity keyword)
   val N =        "s"           : T     (no purity keyword)
   val "s" : T                          (old style; name == extern symbol)
   $[extern ...] attribute style        (searched for; reported if present)
Read-only.  Writes only into the scratchpad.
"""
import json, os, re, sys, collections

HOME = os.path.expanduser("~")   # no machine path is written into this file

SCRATCH = "/tmp/claude-1000/-home-<user>-Programming/6fc7a103-e75c-45df-aff2-b85555e7a824/scratchpad"
TREES = [
    ("lib",   os.path.join(SCRATCH, "saillib")),
    ("model", HOME + "/Programming/SOURCES/sail-riscv/model"),
]

OPEN, CLOSE = "([{", ")]}"

# ---------------------------------------------------------------- comments --
def strip_comments(src):
    """Return a string of the same length with comments blanked to spaces.
    String literals are preserved.  Handles // , /* */ (nesting)."""
    out = list(src)
    i, n = 0, len(src)
    depth = 0                      # block-comment nesting depth
    while i < n:
        c = src[i]
        if depth > 0:
            if src.startswith("/*", i):
                depth += 1; out[i] = out[i+1] = " "; i += 2; continue
            if src.startswith("*/", i):
                depth -= 1; out[i] = out[i+1] = " "; i += 2; continue
            if c != "\n":
                out[i] = " "
            i += 1; continue
        if c == '"':               # string literal: skip verbatim
            i += 1
            while i < n:
                if src[i] == "\\":
                    i += 2; continue
                if src[i] == '"':
                    i += 1; break
                i += 1
            continue
        if src.startswith("//", i):
            while i < n and src[i] != "\n":
                out[i] = " "; i += 1
            continue
        if src.startswith("/*", i):
            depth = 1; out[i] = out[i+1] = " "; i += 2; continue
        i += 1
    return "".join(out)

def line_starts(src):
    starts, pos = [0], 0
    for ch in src:
        pos += 1
        if ch == "\n":
            starts.append(pos)
    return starts

def lineno_of(starts, idx):
    lo, hi = 0, len(starts) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if starts[mid] <= idx: lo = mid
        else: hi = mid - 1
    return lo + 1

# ------------------------------------------------------------- tiny scanner --
def scan(code, i, stop_at=None, stop_depth0=True):
    """Advance from i tracking delimiter depth, skipping strings.
    Stops before a char in stop_at seen at depth 0.  Returns (index, depth)."""
    depth = 0
    n = len(code)
    while i < n:
        c = code[i]
        if c == '"':
            i += 1
            while i < n:
                if code[i] == "\\": i += 2; continue
                if code[i] == '"': i += 1; break
                i += 1
            continue
        if c in OPEN: depth += 1
        elif c in CLOSE: depth -= 1
        elif stop_at and depth == 0 and c in stop_at:
            return i, depth
        i += 1
    return i, depth

def split_top(text, sep):
    """Split on `sep` (a string) occurring at depth 0 outside string literals."""
    parts, buf, depth, i, n = [], [], 0, 0, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            buf.append(c); i += 1
            while i < n:
                buf.append(text[i])
                if text[i] == "\\":
                    i += 1
                    if i < n: buf.append(text[i]); i += 1
                    continue
                if text[i] == '"': i += 1; break
                i += 1
            continue
        if c in OPEN: depth += 1
        elif c in CLOSE: depth -= 1
        if depth == 0 and text.startswith(sep, i):
            parts.append("".join(buf)); buf = []; i += len(sep); continue
        buf.append(c); i += 1
    parts.append("".join(buf))
    return parts

def strip_outer_parens(t):
    t = t.strip()
    if not (t.startswith("(") and t.endswith(")")):
        return t, False
    depth = 0
    for k, c in enumerate(t):
        if c == '"':
            pass
        if c in OPEN: depth += 1
        elif c in CLOSE:
            depth -= 1
            if depth == 0 and k != len(t) - 1:
                return t, False           # parens close early -> not outer
    return t[1:-1].strip(), True

# ------------------------------------------------------- declaration finder --
VAL_RE   = re.compile(r"^[ \t]*(?:private[ \t]+)?val\b", re.M)
CONT_END = ("->", ",", ".", "=", "&", "|", "+", "-", "*", ":", "<", ">", "(", "[", "{")
CONT_START = ("->", ",", ")", "]", "}", "&", "|")
DECL_KW = ("val", "function", "overload", "infix", "infixl", "infixr", "type",
           "enum", "struct", "union", "let", "register", "mapping", "default",
           "scattered", "end", "newtype", "bitfield", "private", "outcome",
           "instantiation", "import", "$")

def decl_extent(code, start, starts):
    """Given index of the `val` keyword, return (end_index_exclusive)."""
    i = start
    n = len(code)
    # find the top-level ':' that introduces the type
    j, _ = scan(code, i, stop_at=":")
    if j >= n:
        return None, None
    colon = j
    # now consume the type
    k = colon + 1
    depth = 0
    while k < n:
        c = code[k]
        if c == '"':
            k += 1
            while k < n:
                if code[k] == "\\": k += 2; continue
                if code[k] == '"': k += 1; break
                k += 1
            continue
        if c in OPEN: depth += 1
        elif c in CLOSE: depth -= 1
        elif c == "\n":
            if depth <= 0:
                seg = code[colon + 1:k].strip()
                if seg and not seg.endswith(CONT_END):
                    # peek at the next non-blank code line
                    m = k + 1
                    while m < n and code[m] in " \t\n":
                        m += 1
                    nxt = code[m:m + 40].lstrip()
                    if not nxt.startswith(CONT_START):
                        first = re.match(r"[A-Za-z_$]+", nxt)
                        tok = first.group(0) if first else ""
                        if nxt == "" or tok in DECL_KW or nxt.startswith("$") \
                           or re.match(r"^[A-Za-z_][A-Za-z_0-9]*\s*[:(]", nxt) is None:
                            return colon, k
                        return colon, k
        k += 1
    return colon, n

PURITY = ("pure", "monadic", "impure")

def parse_targets(spec):
    """spec is either  "string"  or  {k: "v", ...}  -> dict"""
    spec = spec.strip()
    if spec.startswith('"'):
        m = re.match(r'"((?:[^"\\]|\\.)*)"\s*$', spec)
        return {"_": m.group(1)} if m else None
    if spec.startswith("{") and spec.endswith("}"):
        body, out = spec[1:-1], {}
        for part in split_top(body, ","):
            part = part.strip()
            if not part: continue
            kv = split_top(part, ":")
            if len(kv) < 2:
                out[part] = None; continue
            key = kv[0].strip()
            val = ":".join(kv[1:]).strip()
            mm = re.match(r'"((?:[^"\\]|\\.)*)"\s*$', val)
            out[key] = mm.group(1) if mm else val
        return out
    return None

def classify_result(rt):
    t = rt.strip()
    if t.startswith("{") and t.endswith("}"):       # existential: {'v, C. T}
        inner = t[1:-1]
        idx, _ = scan(inner, 0, stop_at=".")
        if idx < len(inner):
            t = inner[idx + 1:].strip()
    base = re.match(r"[A-Za-z_][A-Za-z_0-9]*", t)
    b = base.group(0) if base else ""
    if b in ("bits", "bitvector"): return "bitvector"
    if b in ("int", "range", "nat", "atom"): return "integer"
    if b == "bool": return "boolean"
    if b == "string": return "string"
    if b == "unit": return "unit"
    if b == "real": return "real"
    return "other"

def parse_type(tp):
    tp = " ".join(tp.split())
    constraints = ""
    rest = tp
    if re.match(r"^forall\b", tp):
        # constraint prefix runs to the first depth-0 '.'
        idx, _ = scan(tp, 0, stop_at=".")
        if idx < len(tp):
            constraints = tp[:idx + 1].strip()
            rest = tp[idx + 1:].strip()
    arrow = split_top(rest, "->")
    if len(arrow) < 2:
        return constraints, [], rest.strip(), False
    args_txt = arrow[0].strip()
    res_txt = "->".join(arrow[1:]).strip()
    inner, had = strip_outer_parens(args_txt)
    if inner == "" or inner == "unit":
        arg_types = []
    elif had:
        arg_types = [a.strip() for a in split_top(inner, ",") if a.strip()]
    else:
        arg_types = [] if args_txt == "unit" else [args_txt]
    return constraints, arg_types, res_txt, True

# ------------------------------------------------------------------- main ----
primitives, op_bindings, unclassified, stats = [], [], [], collections.Counter()
spellings = collections.Counter()
multiline = 0

OVERLOAD_RE = re.compile(
    r"^[ \t]*overload[ \t]+(operator[ \t]+)?(\S+)[ \t]*=[ \t]*\{([^}]*)\}")
INFIX_RE = re.compile(r"^[ \t]*(infixl|infixr|infix)[ \t]+(\d+)[ \t]+(\S+)")

for tree, root in TREES:
    files = []
    for dirpath, _dirs, names in os.walk(root):
        for nm in sorted(names):
            if nm.endswith(".sail"):
                files.append(os.path.join(dirpath, nm))
    files.sort()
    stats[tree + ":files"] = len(files)
    for path in files:
        rel = tree + "/" + os.path.relpath(path, root)
        raw = open(path, encoding="utf-8", errors="replace").read()
        code = strip_comments(raw)
        starts = line_starts(raw)
        stats[tree + ":lines"] += raw.count("\n")

        # ---- preprocessor guard chain per line ($ifdef/$ifndef/$else) ----
        guards, stack = [], []
        for line in raw.split("\n"):
            st = line.strip()
            if st.startswith("$ifdef"):
                stack.append(st.split(None, 1)[1].strip() if " " in st else "?")
            elif st.startswith("$ifndef"):
                stack.append("!" + (st.split(None, 1)[1].strip() if " " in st else "?"))
            elif st.startswith("$else"):
                if stack:
                    t = stack[-1]
                    stack[-1] = t[1:] if t.startswith("!") else "!" + t
            elif st.startswith("$endif"):
                if stack: stack.pop()
            guards.append(" & ".join(stack))

        # ---- operator bindings (line based; verified none span lines) ----
        for ln, line in enumerate(code.split("\n"), 1):
            m = OVERLOAD_RE.match(line)
            if m:
                op_bindings.append(dict(
                    symbol=m.group(2),
                    binds_to=[x.strip() for x in m.group(3).split(",") if x.strip()],
                    source="overload",
                    is_operator=bool(m.group(1)),
                    fixity=None, file=rel, line=ln,
                    declared_text=raw.split("\n")[ln - 1].rstrip()))
                stats[tree + ":overload"] += 1
                continue
            m = INFIX_RE.match(line)
            if m:
                op_bindings.append(dict(
                    symbol=m.group(3), binds_to=[], source=m.group(1),
                    is_operator=True,
                    fixity=int(m.group(2)), file=rel, line=ln,
                    declared_text=raw.split("\n")[ln - 1].rstrip()))
                stats[tree + ":" + m.group(1)] += 1
            if re.match(r"^[ \t]*\$\[extern", line):
                stats[tree + ":extern_attr"] += 1

        # ---- val declarations ----
        for m in VAL_RE.finditer(code):
            vstart = m.end() - 3          # index of 'v' in 'val'
            colon, end = decl_extent(code, vstart, starts)
            if colon is None:
                unclassified.append((rel, lineno_of(starts, vstart),
                                     raw[vstart:vstart + 120].split("\n")[0]))
                continue
            header = code[vstart + 3:colon]
            tp_code = code[colon + 1:end]
            ln = lineno_of(starts, vstart)
            end_ln = lineno_of(starts, max(colon, end - 1))
            if end_ln > ln: multiline += 1
            declared_text = "\n".join(
                raw.split("\n")[ln - 1:end_ln]).rstrip()
            stats[tree + ":val_total"] += 1

            h = header.strip()
            kind, name, targets, spelling = None, None, None, None

            om = re.match(r'^"((?:[^"\\]|\\.)*)"\s*$', h)
            if om:                                  # val "name" : T
                name = om.group(1)
                kind = "unspecified"
                targets = {"_": name}
                spelling = 'val "<name>" : <type>'
            else:
                # Split name from optional extern body.  The name may itself be
                # an operator containing '=' (e.g. `operator <=_s`), so the name
                # is lexed first rather than splitting the header on '='.
                nm = re.match(r"^operator\s+(\S+)", h)
                if nm:
                    name = "operator " + nm.group(1)
                    rhs = h[nm.end():].strip()
                else:
                    nm = re.match(r"^([A-Za-z_?][A-Za-z_0-9?#']*)", h)
                    if not nm:
                        unclassified.append((rel, ln, declared_text.split("\n")[0]))
                        continue
                    name = nm.group(1)
                    rhs = h[nm.end():].strip()
                if rhs == "":
                    stats[tree + ":val_plain"] += 1
                    continue                        # ordinary val, not a primitive
                if not rhs.startswith("="):
                    unclassified.append((rel, ln, declared_text.split("\n")[0]))
                    continue
                rhs = rhs[1:].strip()
                pm = re.match(r"^(pure|monadic|impure)\b(.*)$", rhs, re.S)
                if pm:
                    kind = pm.group(1)
                    spec = pm.group(2).strip()
                else:
                    kind = "unspecified"
                    spec = rhs
                targets = parse_targets(spec)
                if targets is None:
                    unclassified.append((rel, ln, declared_text.split("\n")[0]))
                    continue
                shape = "{...}" if spec.startswith("{") else '"..."'
                spelling = ("val <name> = %s %s : <type>" % (kind, shape)
                            if kind != "unspecified"
                            else "val <name> = %s : <type>" % shape)

            tp_raw = " ".join(tp_code.split())
            constraints, arg_types, result_type, ok = parse_type(tp_raw)
            if not ok:
                unclassified.append((rel, ln, "NO ARROW IN TYPE: " +
                                     declared_text.split("\n")[0]))
            spellings[spelling] += 1
            stats[tree + ":primitive"] += 1
            primitives.append(dict(
                name=name, file=rel, line=ln, kind=kind, type=tp_raw,
                arg_types=arg_types, result_type=result_type,
                constraints=constraints, targets=targets,
                guard=guards[ln - 1] if ln - 1 < len(guards) else "",
                result_family=classify_result(result_type),
                declared_text=declared_text))

# ---- does a Sail `function` body also exist for this name?  A val whose
# target map names only some backends (e.g. {lean: "..."}) is external for
# those backends and falls back to the Sail body for the rest. ----
tree_src = {}
for tree, root in TREES:
    buf = []
    for dp, _d, ns in os.walk(root):
        for nm_ in sorted(ns):
            if nm_.endswith(".sail"):
                buf.append(strip_comments(open(os.path.join(dp, nm_),
                           encoding="utf-8", errors="replace").read()))
    tree_src[tree] = "\n".join(buf)
NAMECH = re.compile(r"[A-Za-z_0-9?#']")
for p in primitives:
    body = tree_src[p["file"].split("/")[0]]
    nm_ = p["name"]
    found = False
    for m_ in re.finditer(r"^[ \t]*(?:private[ \t]+)?function[ \t]+" + re.escape(nm_),
                          body, re.M):
        nxt = body[m_.end():m_.end() + 1]
        if not NAMECH.match(nxt):
            found = True; break
    p["has_sail_fallback"] = found
    p["targets_all_backends"] = "_" in (p["targets"] or {})

primitives.sort(key=lambda d: (d["file"], d["line"]))
op_bindings.sort(key=lambda d: (d["file"], d["line"]))
for d in primitives: d.pop("result_family", None) or None

with open(os.path.join(SCRATCH, "primitives.json"), "w") as f:
    json.dump(primitives, f, indent=2)
    f.write("\n")
with open(os.path.join(SCRATCH, "operator_bindings.json"), "w") as f:
    json.dump(op_bindings, f, indent=2)
    f.write("\n")

# ------------------------------------------------------------------ report ---
print("== files / lines ==")
for tree, _ in TREES:
    print("  %-6s files=%d lines=%d" % (tree, stats[tree + ":files"], stats[tree + ":lines"]))
print("\n== val declarations ==")
for tree, _ in TREES:
    print("  %-6s val total=%-4d primitives(external)=%-4d plain(sail-defined)=%d"
          % (tree, stats[tree + ":val_total"], stats[tree + ":primitive"],
             stats[tree + ":val_plain"]))
print("  multi-line declarations joined: %d" % multiline)
print("\n== operator bindings ==")
for tree, _ in TREES:
    tot = (stats[tree + ":overload"] + stats[tree + ":infix"]
           + stats[tree + ":infixl"] + stats[tree + ":infixr"])
    print("  %-6s overload=%-4d infix=%-3d infixl=%-2d infixr=%-2d TOTAL=%d"
          % (tree, stats[tree + ":overload"], stats[tree + ":infix"],
             stats[tree + ":infixl"], stats[tree + ":infixr"], tot))
print("  of the overloads, `overload operator X` = %d, `overload name` = %d"
      % (sum(1 for b in op_bindings if b["source"] == "overload" and b["is_operator"]),
         sum(1 for b in op_bindings if b["source"] == "overload" and not b["is_operator"])))
print("\n== distinct external spellings encountered ==")
for sp, c in spellings.most_common():
    print("  %-46s %d" % (sp, c))
print("  $[extern ...] attribute occurrences: lib=%d model=%d"
      % (stats["lib:extern_attr"], stats["model:extern_attr"]))
print("\n== kind ==")
kc = collections.Counter((p["file"].split("/")[0], p["kind"]) for p in primitives)
for k in sorted(kc): print("  %-6s %-12s %d" % (k[0], k[1], kc[k]))
print("\n== result-type family ==")
fam = collections.Counter()
for p in primitives:
    fam[(p["file"].split("/")[0], classify_result(p["result_type"]))] += 1
famtot = collections.Counter()
for (t, f), c in fam.items(): famtot[f] += c
order = ["bitvector", "integer", "boolean", "string", "unit", "real", "other"]
print("  %-11s %6s %6s %6s" % ("family", "lib", "model", "TOTAL"))
for f in order:
    print("  %-11s %6d %6d %6d" % (f, fam[("lib", f)], fam[("model", f)], famtot[f]))
print("  %-11s %6d %6d %6d" % ("ALL",
      sum(fam[("lib", f)] for f in order), sum(fam[("model", f)] for f in order),
      sum(famtot.values())))
others = sorted(set(p["result_type"] for p in primitives
                    if classify_result(p["result_type"]) == "other"))
print("  'other' result types: " + ", ".join(others))
with open(os.path.join(SCRATCH, "primitive_locations.txt"), "w") as f:
    for p in primitives:
        f.write("%s:%d\t%s\n" % (p["file"], p["line"], p["name"]))
# sanity: no declared_text may swallow a following declaration
bad = [p for p in primitives
       if re.search(r"^\s*(function|overload|infix|private\s+val|val)\b",
                    "\n".join(p["declared_text"].split("\n")[1:]), re.M)]
fb = [p for p in primitives if p["has_sail_fallback"]]
print("\n== primitives that ALSO have a Sail `function` body (partial externs) ==")
print("  total=%d   of which target map has a `_` catch-all=%d"
      % (len(fb), sum(1 for p in fb if p["targets_all_backends"])))
print("  lib=%d model=%d"
      % (sum(1 for p in fb if p["file"].startswith("lib/")),
         sum(1 for p in fb if p["file"].startswith("model/"))))
print("  true atoms (no Sail body anywhere): lib=%d model=%d TOTAL=%d"
      % (sum(1 for p in primitives if p["file"].startswith("lib/") and not p["has_sail_fallback"]),
         sum(1 for p in primitives if p["file"].startswith("model/") and not p["has_sail_fallback"]),
         sum(1 for p in primitives if not p["has_sail_fallback"])))

g = [p for p in primitives if p["guard"]]
print("\n== preprocessor-guarded primitives: %d ==" % len(g))
import collections as _c
for k, v in _c.Counter(p["guard"] for p in g).most_common():
    print("  %-40s %d" % (k, v))
print("\n== SANITY: declarations that swallowed a following decl: %d ==" % len(bad))
for p in bad[:10]:
    print("  %s:%d %s" % (p["file"], p["line"], p["name"]))
print("\n== UNCLASSIFIED (%d) ==" % len(unclassified))
for rel, ln, txt in unclassified:
    print("  %s:%d  %s" % (rel, ln, txt))
