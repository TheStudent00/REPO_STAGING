"""SailModel.strip -- the pure form of every execute clause, proposed by
one syntactic rule and certified by Lean.

Plan leaf hq.research.lean_proof_path_resistant_to_churn
.sail_model.strip (log 274 §4; the fourth launch's design, 2026-09-14):

  the proposal   Python reads the clause the sail compiler's Lean backend
                 emitted and applies ONE rule: a register read becomes a
                 parameter, the pure `let`s are kept verbatim, the value
                 handed to the register write is the result. A clause
                 that does anything else (reads the PC, a CSR or memory,
                 branches on machine state, throws) is REFUSED with the
                 construct named. The rule names no instruction.
  the certificate  Lean proves, for every parameter, that the emitted
                 clause IS the program "read, read, write the proposal,
                 retire". If the proposal is wrong the theorem fails and
                 the clause is a refusal row. Nothing is trusted from
                 Python.

Two shapes are accepted, both general:
  straight     reads (as `let x <- rX_bits r` lines or inline `(<- (rX_bits r))`
               occurrences, hoisted in textual order), pure lets, one
               `wX_bits rd VALUE`, then `pure RETIRE_SUCCESS`.
  alias        the body is `pure (ExecuteAs (CTOR args))`: the clause
               re-dispatches to another instruction (the compressed
               forms). The pure form is that instruction.
A value that is a `match` on a parameter with inline reads in its arms is
the straight shape with a case split in the certificate, provided every
arm reads the same registers in the same order (else refused).
"""
import json
import os
import re
import sys
import subprocess
import time

CLAUSE_HEAD = re.compile(
    r"^(?:noncomputable )?def (execute_\w+)\s*(.*?)\s*:\s*(SailM ExecutionResult := do|ExecutionResult :=)\s*$")
PURE_ALIAS = re.compile(r"^\(ExecuteAs\s+\((.*)\)\)\s*$", re.S)
REGX = r"(\w+|\((?:[^()]|\([^()]*\))*\))"          # a register argument: a name or a parenthesised expression
READ_LINE = re.compile(r"^let (\w+) ← (?:do )?\(?\s*rX_bits " + REGX + r"\s*\)?\s*$")
INLINE_READ = re.compile(r"\(←\s*\(rX_bits\s+" + REGX + r"\)\)|\(←\s*rX_bits\s+(\w+)\)")
PURE_LET = re.compile(r"^let (\w+)\s*(?::\s*(.+?))?\s*:=\s*(.*)$", re.S)
PURE_ACTION = re.compile(r"^let (\w+)\s*(?::\s*(.+?))?\s*←\s*(?:do\s*)?\(pure\s+(.*)\)\s*$", re.S)
WRITE = re.compile(r"^\(wX_bits " + REGX + r"\s+(.*)\)\s*$", re.S)
END = re.compile(r"^\(pure RETIRE_SUCCESS\)\s*$")
ALIAS = re.compile(r"^\(pure\s+\(ExecuteAs\s+\((.*)\)\)\)\s*$", re.S)
ARM = re.compile(r"^\|\s*(\.\w+)\s*=>\s*(.*)$", re.S)


DECL_RE = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+|private\s+|protected\s+)*"
                     r"(?:(def|abbrev)\s+([A-Za-z0-9_'.]+)|theorem|instance|structure|inductive|namespace|end|section|open|set_option|/--)", re.M)


def emitted_defs(lean_dir):
    """name -> text of every def/abbrev in the emitted model (the pure forms
    and every helper Sail's own prelude gave them), by a scan, no list."""
    defs = {}
    for root, _, files in os.walk(lean_dir):
        for f in files:
            if not f.endswith(".lean"):
                continue
            text = open(os.path.join(root, f)).read()
            ms = list(DECL_RE.finditer(text))
            for i, m in enumerate(ms):
                if not m.group(1):
                    continue
                end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
                defs[m.group(2)] = text[m.start():end]
    return defs


LIBRARY_INDEX = {}      # unqualified def name -> qualified, from the lean-sail package (set by library_index)


def library_index(project):
    """Index lean-sail's own definitions by namespace, from the package's
    sources under the proof project: name -> Namespace.name. The emit
    calls many of them unqualified (`open Sail`), so the unfolding rule
    must know them by their short names too."""
    global LIBRARY_INDEX
    idx = {}
    root = os.path.join(project, ".lake", "packages")
    for base, _, files in os.walk(root) if os.path.isdir(root) else []:
        for f in files:
            if not f.endswith(".lean"):
                continue
            ns = []
            for ln in open(os.path.join(base, f), errors="replace"):
                m = re.match(r"^namespace\s+(\S+)", ln)
                if m:
                    ns.append(m.group(1))
                    continue
                m = re.match(r"^end\s+(\S+)\s*$", ln)
                if m and ns and ns[-1] == m.group(1):
                    ns.pop()
                    continue
                # the whole dotted name as declared (`abbrev Vector.length` is `Sail.Vector.length`, and
                # `Vector` alone names nothing): the index is keyed by that dotted spelling
                m = re.match(r"^(?:@\[[^\]]*\]\s*)?(?:protected\s+|noncomputable\s+)*(?:def|abbrev)\s+([A-Za-z_][A-Za-z0-9_'.]*[A-Za-z0-9_'])", ln)
                if m and not ln.lstrip().startswith("private"):      # a private def cannot be named from outside
                    q = ".".join(ns + [m.group(1)])
                    idx.setdefault(m.group(1), q)
    LIBRARY_INDEX = idx
    # An empty index is a PATH fault, not an absence of helpers, and it is
    # silent where it hurts most: every `simp only` set comes out missing the
    # lean-sail helpers, `bv_decide` abstracts them as opaque variables, and
    # the run reports UNDECIDED as though the mathematics were hard. That is
    # exactly what happened to 6 of the 12 pairs in gate_emul (2026-09-16):
    # the cache project carried no `.lake/packages`, so `shift_bits_left` was
    # never named and a shift by the literal 0 stayed opaque. Say so loudly.
    if not idx:
        sys.stderr.write(
            "leanpath: WARNING -- no lean-sail definitions indexed under %s\n"
            "leanpath:            simp sets will omit every library helper and\n"
            "leanpath:            bv_decide will abstract them as opaque variables,\n"
            "leanpath:            reporting UNDECIDED for a path fault. Point the\n"
            "leanpath:            proof project at a BUILT tree (one with Sail/Common.lean).\n" % root)
    return idx


def library_refs(defs, names, extra_texts=()):
    """The lean-sail library helpers the given emitted definitions call,
    read from their own text: the qualified ones (`Sail.BitVec.zeroExtend`)
    and, through the library index, the unqualified ones
    (`shift_bits_left` is `Sail.shift_bits_left`). Unfolded alongside, by
    the same rule."""
    refs = []
    for text in [defs.get(n, "") for n in names] + list(extra_texts):     # the pure forms are generated, not emitted: their text comes in extra_texts
        for m in re.findall(r"\bSail\.[A-Za-z_][A-Za-z0-9_.']*[A-Za-z0-9_']", text):
            # a qualified name whose last segment is capitalised is a type or a namespace
            # (`Sail.Vector`, `Sail.BitVec`), not a definition to unfold: Lean's own convention
            if m not in refs and not m.rsplit(".", 1)[-1][:1].isupper():
                refs.append(m)
        for w in set(re.findall(r"[A-Za-z_][A-Za-z0-9_'.]*[A-Za-z0-9_']|[A-Za-z_]", text)):    # dotted tokens whole
            q = LIBRARY_INDEX.get(w) or _index_suffix(w)
            if q and w not in defs and q not in refs and w not in ("def", "let", "if", "then", "else", "match", "with", "fun"):
                refs.append(q)
    return refs


def _index_suffix(w):
    """A PARTIALLY qualified call matched to its full library name.

    The index is keyed by the name as declared -- `toNatInt`, declared inside
    `namespace Sail.BitVec` -- but the emit writes it partially qualified, as
    `BitVec.toNatInt`. The whole-dotted-token lookup then misses, the helper
    never enters the `simp only` set, and `bv_decide` abstracts the term as an
    opaque variable (gate_emul_fix, 2026-09-16: `BitVec.toNatInt` left opaque
    on au_319 and au_407 for exactly this reason).

    The last segment finds the candidate; the qualified name must then END with
    the whole dotted spelling, so `BitVec.toNatInt` matches
    `Sail.BitVec.toNatInt` and never some unrelated `Other.toNatInt`."""
    if "." not in w:
        return None
    q = LIBRARY_INDEX.get(w.rsplit(".", 1)[-1])
    return q if q and (q == w or q.endswith("." + w)) else None


def reachable(defs, seed_text, limit=400, skip=lambda n: False):
    """The emitted definitions a text mentions, transitively: the unfolding
    the integer level needs to see Sail's helpers down to Lean's own
    arithmetic (the rule; nothing is named)."""
    ident = lambda s: set(re.findall(r"[A-Za-z_][A-Za-z0-9_']*", s))
    seen, todo = [], sorted(w for w in ident(seed_text) if w in defs and not skip(w))
    while todo and len(seen) < limit:
        n = todo.pop(0)
        if n in seen:
            continue
        seen.append(n)
        todo += sorted(w for w in ident(defs[n]) if w in defs and not skip(w) and w not in seen and w not in todo)
    return seen


def split_params(sig):
    """'(a : T) (b : (U V))' -> [(name, type_text)], balancing parentheses."""
    out, depth, cur = [], 0, ""
    for ch in sig:
        if ch == "(":
            depth += 1
            if depth == 1:
                cur = ""
                continue
        elif ch == ")":
            depth -= 1
            if depth == 0:
                name, _, typ = cur.partition(":")
                out.append((name.strip(), typ.strip()))
                continue
        if depth >= 1:
            cur += ch
    return out


def clauses_of(lean_dir):
    """Every execute clause of the emitted tree: name, params, body lines."""
    found = []
    for fn in sorted(os.listdir(lean_dir)):
        if not fn.endswith(".lean"):
            continue
        lines = open(os.path.join(lean_dir, fn)).read().split("\n")
        i = 0
        while i < len(lines):
            m = CLAUSE_HEAD.match(lines[i])
            if not m:
                i += 1
                continue
            name, sig = m.group(1), m.group(2)
            monadic = m.group(3).startswith("SailM")
            body = []
            j = i + 1
            while j < len(lines) and lines[j].strip() != "":
                body.append(lines[j])
                j += 1
            found.append({"name": name, "params": split_params(sig), "body": body,
                          "file": fn, "line": i + 1, "monadic": monadic})
            i = j
    return found


def elements(body):
    """Top-level do-elements: a line at the body's own indentation starts one;
    deeper lines continue it."""
    if not body:
        return []
    base = len(body[0]) - len(body[0].lstrip(" "))
    els = []
    for ln in body:
        ind = len(ln) - len(ln.lstrip(" "))
        if ind == base and els:
            els.append([ln[base:]])
        elif not els:
            els.append([ln[base:]])
        else:
            els[-1].append(ln[base:])
    return ["\n".join(e) for e in els]


def strip_outer_parens(t):
    t = t.strip()
    while t.startswith("(") and t.endswith(")"):
        depth = 0
        ok = True
        for k, ch in enumerate(t):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0 and k != len(t) - 1:
                    ok = False
                    break
        if not ok:
            break
        t = t[1:-1].strip()
    return t


def hoist_inline(text, reads, regs, counter):
    """Replace inline reads by variables, appending (var, reg) to reads in
    textual order. Returns the new text."""
    def repl(m):
        r = m.group(1) or m.group(2)
        key = re.sub(r"\W+", "_", r).strip("_")
        counter[key] = counter.get(key, 0) + 1
        var = "v_%s" % key if counter[key] == 1 else "v_%s_%d" % (key, counter[key])
        reads.append((var, r))
        return var
    return INLINE_READ.sub(repl, text)


def propose(clause):
    """The rule. Returns a dict with shape, reads, lets, value, or a refusal."""
    regs = [n for n, t in clause["params"] if t == "regidx"]
    others = [(n, t) for n, t in clause["params"] if t != "regidx"]
    split = merge_var_arms(clause) if clause.get("monadic", True) else None
    if split is not None:
        proposals = []
        for ctor, sub in split:
            proposals.append((ctor, sub, propose(sub)))
        usable = [t for t in proposals if "refused" not in t[2]]
        if not usable:
            return {"refused": "every merge_var arm refused: %s"
                    % proposals[0][2].get("refused", "")[:70]}
        return {"shape": "merge_arms", "merge_arms": proposals,
                "regs": regs, "others": others}
    els = elements(clause["body"])
    reads, lets, write, value, alias = [], [], None, None, None
    ended = False
    counter = {}
    if not clause.get("monadic", True):
        # zero or more pure lets, then the re-dispatch: an alias whose target
        # has the lets substituted (a let may shadow a parameter, so the
        # substitution goes in order, later lets over earlier ones)
        lets_here = []
        for e in els[:-1]:
            m = PURE_LET.match(e)
            if not m or "←" in e:
                return {"refused": "a pure clause with an element that is not a let: %s" % e.split("\n")[0]}
            lets_here.append((m.group(1), m.group(3).strip()))
        m = PURE_ALIAS.match(els[-1]) if els else None
        if not m:
            return {"refused": "a pure clause that is not an ExecuteAs alias: %s" % els[-1].split("\n")[0]}
        target = one_line(m.group(1).strip())
        for name, val in reversed(lets_here):
            target = re.sub(r"\b%s\b" % re.escape(name), "(" + val + ")", target)
        return {"shape": "alias", "alias": target, "pure_clause": True, "regs": regs, "others": others}
    if len(els) == 1 and ALIAS.match(els[0]):
        return {"shape": "alias", "alias": one_line(ALIAS.match(els[0]).group(1).strip()),
                "pure_clause": False, "regs": regs, "others": others}
    for e in els:
        if ended:
            return {"refused": "an element after RETIRE_SUCCESS: %s" % e.split("\n")[0]}
        m = READ_LINE.match(e)
        if m:
            var, r = m.group(1), m.group(2)
            reads.append((var, r))
            continue
        m = PURE_ACTION.match(e)
        if m:
            var, typ, val = m.group(1), m.group(2), m.group(3)
            try:
                val = hoist_inline(val, reads, regs, counter)
            except ValueError as ex:
                return {"refused": str(ex)}
            if "←" in val:
                return {"refused": "an effect inside a pure-wrapped let: %s" % val.strip().split("\n")[0]}
            lets.append((var + (" : " + typ if typ else ""), val))
            continue
        m = PURE_LET.match(e)
        if m and "←" not in e.split(":=", 1)[0]:
            var, typ, val = m.group(1), m.group(2), m.group(3)
            try:
                val = hoist_inline(val, reads, regs, counter)
            except ValueError as ex:
                return {"refused": str(ex)}
            if "←" in val:
                return {"refused": "an effect inside a let: %s" % val.strip().split("\n")[0]}
            lets.append((var + (" : " + typ if typ else ""), val))
            continue
        m = WRITE.match(e)
        if m:
            if write is not None:
                return {"refused": "two register writes"}
            write = m.group(1)
            value = m.group(2).strip()
            continue
        if END.match(e):
            ended = True
            continue
        return {"refused": "an element the rule does not know: %s" % e.split("\n")[0].strip()}
    if write is None:
        return {"refused": "no register write"}
    if not ended:
        return {"refused": "no RETIRE_SUCCESS at the end"}
    case_on = None
    inner = value
    if inner.startswith("(← do"):
        inner = strip_outer_parens(inner)      # "← do\n match ..."
        inner = inner[1:].strip()              # drop ←
        assert inner.startswith("do")
        inner = inner[2:].strip()
        mm = re.match(r"^match (\w+) with\s*(.*)$", inner, re.S)
        if not mm:
            return {"refused": "an effectful value that is not a match: %s" % inner.split("\n")[0]}
        case_on = mm.group(1)
        if case_on not in [n for n, _ in others]:
            return {"refused": "match on something that is not a parameter: %s" % case_on}
        arms_text = mm.group(2)
        # split arms at top-level "| "
        arms, depth, cur = [], 0, ""
        for ch in arms_text:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            if ch == "|" and depth == 0 and cur.strip() != "":
                arms.append(cur)
                cur = ""
                continue
            cur += ch
        if cur.strip():
            arms.append(cur)
        arms = [a.strip() for a in arms if a.strip()]
        order = None
        new_arms = []
        impure_arms = []          # (ctor, first line) for arms this rule cannot express
        for a in arms:
            am = ARM.match("| " + a if not a.startswith("|") else a)
            if not am:
                am = ARM.match("|" + a)
            if not am:
                return {"refused": "an arm the rule does not know: %s" % a.split("\n")[0]}
            ctor, rhs = am.group(1), am.group(2).strip()
            rhs = strip_outer_parens(rhs)
            if not rhs.startswith("pure"):
                return {"refused": "an arm that is not pure: %s" % rhs.split("\n")[0]}
            rhs = rhs[4:].strip()
            arm_reads, arm_counter = [], {}
            try:
                rhs2 = hoist_inline(rhs, arm_reads, regs, arm_counter)
            except ValueError as ex:
                return {"refused": str(ex)}
            if "←" in rhs2:
                # An arm with an effect does NOT condemn its siblings. Sail writes
                # several instructions into one clause (UTYPE is LUI and AUIPC; LUI
                # is a bare immediate, AUIPC reads the program counter), and the
                # pure arms are usable on their own. Record it and carry on; the
                # clause is certified PER ARM below (shape "arms"), never as a whole,
                # so no definition is ever emitted for an arm we cannot express.
                impure_arms.append((ctor, rhs2.split("\n")[0]))
                continue
            seq = [r for _, r in arm_reads]
            if order is None:
                order = seq
                reads.extend(arm_reads)
            elif seq != order:
                return {"refused": "read-order-differs across arms: %s vs %s" % (order, seq)}
            new_arms.append((ctor, rhs2))
        if impure_arms and not new_arms:
            return {"refused": "every arm has an effect beyond register reads: %s" % impure_arms[0][1]}
        value = "match %s with\n" % case_on + "\n".join(
            "  | %s => %s" % (c, r) for c, r in new_arms)
    else:
        impure_arms = []
        try:
            value = hoist_inline(value, reads, regs, counter)
        except ValueError as ex:
            return {"refused": str(ex)}
        if "←" in value:
            return {"refused": "an effect in the written value beyond register reads: %s" % value.split("\n")[0]}
        value = strip_outer_parens(value) if value.startswith("(") else value
    # a pure let whose name is used as a register argument (of a read or of
    # the write) is a register-index let: it stays in the monadic program,
    # before the reads, and is repeated in the pure form only if the value
    # uses it too
    reg_args = [r for _, r in reads] + [write]
    def used_in(name, texts):
        return any(re.search(r"\b%s\b" % re.escape(name), tx) for tx in texts)
    index_lets = [(v, val) for v, val in lets if used_in(v.split(":")[0].strip(), reg_args)]
    value_texts = [val for _, val in lets] + [value]
    pure_lets = [(v, val) for v, val in lets
                 if (v, val) not in index_lets or used_in(v.split(":")[0].strip(), value_texts)]
    shape = "straight"
    if case_on and impure_arms:
        # some arms pure, some not: certify each pure arm on its own
        shape = "arms"
    return {"shape": shape, "reads": reads, "lets": pure_lets, "index_lets": index_lets,
            "write": write, "value": value, "case_on": case_on, "regs": regs, "others": others,
            "pure_arms": [arm_ident(c) for c, _ in new_arms] if case_on else [],
            "arm_values": new_arms if case_on else [],
            "impure_arms": impure_arms}


def one_line(text):
    """A term on one line: a structure literal the emitter split over lines
    loses its field separators when re-indented, so the fields get commas."""
    s = re.sub(r"\s*\n\s*", " ", text)
    while True:
        s2 = re.sub(r"(:=\s*[^,{}]+?)\s+(\w+\s*:=)", r"\1, \2", s, count=1)
        if s2 == s:
            return s
        s = s2


def reindent(text, n):
    pad = " " * n
    return "\n".join(pad + ln if ln.strip() else ln for ln in text.split("\n"))


def header_of(lean_dir, lib):
    """The emitted file's own preamble (set_option, open, namespace lines),
    with its imports replaced by the library root, so names resolve exactly
    as they do in the emitted clause. Returns (head lines, closing lines)."""
    path = os.path.join(lean_dir, "InstsEnd.lean")
    head, closers = ["import %s" % lib], []
    for ln in open(path):
        s = ln.rstrip("\n")
        if s.startswith("import "):
            continue
        if s.startswith(("set_option ", "open ", "noncomputable section", "namespace ")):
            head.append(s)
            if s.startswith("namespace "):
                closers.insert(0, "end " + s.split()[1])
            if s.startswith("noncomputable section"):
                closers.append("end")
            continue
        if s.strip() == "" or s.startswith("--"):
            continue
        break
    return head, closers


def lean_file(clause, prop, lib, namespaces, lean_dir=None):
    """The Lean text: the pure form and its certificate."""
    name = clause["name"]
    short = name[len("execute_"):]
    params_sig = " ".join("(%s : %s)" % (n, t) for n, t in clause["params"])
    params_call = " ".join(n for n, _ in clause["params"])
    if lean_dir:
        head, closers = header_of(lean_dir, lib)
        head = head + ["set_option linter.unusedVariables false", ""]
    else:
        head = ["import %s" % lib,
                "open Sail Sail.ConcurrencyInterfaceV1 PreSail %s" % " ".join(namespaces),
                "set_option maxHeartbeats 1000000000",
                "set_option maxRecDepth 100000",
                "set_option linter.unusedVariables false",
                "noncomputable section",
                "namespace Leanpath", ""]
        closers = ["end Leanpath"]
    return "\n".join(head + lean_body(clause, prop) + closers + [""])


# ------------------------------------------------ the tuple-match shape ----
# A THIRD ARM SHAPE, and the most common refusal in the model. `UTYPE` puts its
# match inside the WRITTEN VALUE; these put it at the top of the do-block, over
# a tuple of every parameter, and each arm is a COMPLETE body with its own
# reads, its own write and its own retire:
#
#     def execute_F_UN_TYPE_X_S (arg0 : fregidx) (arg1 : regidx)
#                               (arg2 : f_un_op_x_S) : SailM … := do
#       let merge_var := (arg0, arg1, arg2)
#       match merge_var with
#       | (rs1, rd, .FCLASS_S) => (do … wX_bits rd … ; pure RETIRE_SUCCESS)
#       | (rs1, rd, .FMV_X_W)  => (do … wX_bits rd … ; pure RETIRE_SUCCESS)
#
# So an arm cannot share one `write` and one `value` with its siblings the way
# the UTYPE arms do; each needs the WHOLE rule run on it. That is what this
# does: it splits the clause into one synthetic sub-clause per arm, with the
# arm's binders standing in for the parameters and the dispatch parameter
# pinned to the arm's constructor, and `propose` recurses into each.
#
# 16 clauses in the model take this shape, and they expand to 218 arch-opcodes
# -- the largest single block of refusals there is.
# NAMES: MERGE_LET, TUPLE_LET, TUPLE_MATCH and TUPLE_ARM are ALL already
# taken in this file, with different capture groups. Collided with two of
# them before checking. These three are prefixed so they cannot.
ARMSPLIT_LET = re.compile(r"^let\s+(\w+)\s*:=\s*\(([^()]*)\)\s*$")
ARMSPLIT_MATCH = re.compile(r"^match\s+(\w+)\s+with\s*$")
ARMSPLIT_ARM = re.compile(r"^\|\s*\(([^)]*)\)\s*=>\s*(.*)$", re.S)


def merge_var_arms(clause):
    """[(ctor, sub-clause)] for the tuple-match shape, or None if not it.

    Returns None rather than a refusal: a clause that is not this shape must
    fall through to the ordinary rule untouched."""
    els = elements(clause["body"])
    if len(els) < 3:
        return None
    m0 = ARMSPLIT_LET.match(els[0].strip())
    m1 = ARMSPLIT_MATCH.match(els[1].strip())
    if not m0 or not m1 or m1.group(1) != m0.group(1):
        return None
    names = [x.strip() for x in m0.group(2).split(",")]
    params = [n for n, _ in clause["params"]]
    if names != params:
        return None                      # the tuple must BE the parameter list
    out = []
    for e in els[2:]:
        ma = ARMSPLIT_ARM.match(e.strip())
        if ma is None:
            return None
        pat = [x.strip() for x in ma.group(1).split(",")]
        if len(pat) != len(params):
            return None
        dispatch = [i for i, x in enumerate(pat) if x.startswith(".")]
        if len(dispatch) != 1:
            return None                  # exactly one position selects the arm
        i = dispatch[0]
        body = ma.group(2).strip()
        if not body.startswith("(do"):
            return None
        # `elements` takes a LIST OF LINES and splits on the first line's
        # indentation; handing it a string makes `body[0]` a character and it
        # degenerates into one element per character. So the arm's body is
        # rebuilt as lines: strip the `(do … )` wrapper, drop the `do` line,
        # and keep the rest at their own indentation, which is then the base.
        inner = strip_outer_parens(body)
        lines = inner.split("\n")
        if not lines or lines[0].strip() != "do":
            return None
        lines = [ln for ln in lines[1:] if ln.strip()]
        if not lines:
            return None
        sub = {"name": clause["name"], "monadic": True, "body": lines,
               "params": [(pat[j], clause["params"][j][1])
                          for j in range(len(pat)) if j != i],
               "arm_binders": pat, "case_pos": i}
        out.append((pat[i], sub))
    return out or None


def arm_ident(ctor):
    """The bare constructor name. The emit writes arms as `.LUI` (Lean's
    anonymous constructor) and sometimes fully qualified; a Lean identifier
    can carry neither, so take the last segment."""
    return str(ctor).strip().lstrip(".").split(".")[-1]


def lean_body_arms(clause, prop):
    """A clause some of whose arms this rule cannot express: certify each PURE
    arm on its own.

    Sail writes several instructions into one clause and selects between them
    with a match on an enumerated parameter. `UTYPE` is the example: the `LUI`
    arm is a bare immediate, the `AUIPC` arm reads the program counter. The
    whole-clause form cannot be written, because there is nothing honest to put
    in the AUIPC arm -- but the LUI arm is a function of its reads and nothing
    else.

    So one definition and one certificate per pure arm, each stated with the
    CONCRETE constructor substituted for the case parameter. No definition is
    emitted for an arm we cannot express, so no false statement about it can be
    made; an instruction decoded to such an arm is refused by the walk.
    """
    name = clause["name"]
    short = name[len("execute_"):]
    case_on = prop["case_on"]
    read_sig = " ".join("(%s : BitVec 64)" % v for v, _ in prop["reads"])
    other_sig = " ".join("(%s : %s)" % (n, t) for n, t in prop["others"] if n != case_on)
    pure_sig = (read_sig + " " + other_sig).strip()
    pure_call = " ".join([v for v, _ in prop["reads"]]
                         + [n for n, _ in prop["others"] if n != case_on])
    lets = "".join("  let %s := %s\n" % (v, reindent(val, 4).lstrip()) for v, val in prop["lets"])
    out = ["/-- %d of %d arms are a function of the reads; the rest are named and left alone -/"
           % (len(prop["arm_values"]), len(prop["arm_values"]) + len(prop["impure_arms"])),
           "-- not expressible: " + ", ".join(arm_ident(c) for c, _ in prop["impure_arms"]), ""]
    for ctor, val in prop["arm_values"]:
        arm = "%s_%s" % (short, arm_ident(ctor))
        params_sig = " ".join("(%s : %s)" % (n, t) for n, t in clause["params"] if n != case_on)
        params_call = " ".join((ctor if n == case_on else n) for n, _ in clause["params"])
        rhs_reads = "".join("      let %s := %s\n" % (v, reindent(v2, 8).lstrip())
                            for v, v2 in prop.get("index_lets", []))
        rhs_reads += "".join("      let %s ← rX_bits %s\n" % (v, r) for v, r in prop["reads"])
        out += [
            "def pure_%s %s : BitVec 64 :=" % (arm, pure_sig),
            lets.rstrip("\n") if lets else "",
            reindent(val, 2), "",
            "theorem strip_%s %s :" % (arm, params_sig),
            "    %s %s =" % (name, params_call),
            "    (do",
            rhs_reads.rstrip("\n"),
            "      wX_bits %s (pure_%s %s)" % (prop["write"], arm, pure_call),
            "      pure RETIRE_SUCCESS) := by",
            "  first",
            "  | rfl",
            "  | simp only [%s, pure_%s, bind_assoc, pure_bind]" % (name, arm),
            ""]
    return [ln for ln in out if ln is not None]


def lean_body(clause, prop):
    """The pure form and its certificate, without header or closers, so a
    unit's file can inline the clauses it walks."""
    if prop.get("shape") == "effects":            # the effects rule (floats), below
        return lean_body_effects(clause, prop)
    if prop.get("shape") == "arms":               # some arms pure, some not
        return lean_body_arms(clause, prop)
    name = clause["name"]
    short = name[len("execute_"):]
    params_sig = " ".join("(%s : %s)" % (n, t) for n, t in clause["params"])
    params_call = " ".join(n for n, _ in clause["params"])
    if prop["shape"] == "alias":
        others_sig = " ".join("(%s : %s)" % (n, t) for n, t in clause["params"])
        rhs = ("(ExecuteAs (alias_%s %s))" if prop.get("pure_clause") else "(pure (ExecuteAs (alias_%s %s)))") % (short, params_call)
        return [
            "/-- the alias: this clause re-dispatches to another instruction -/",
            "def alias_%s %s : instruction :=" % (short, others_sig),
            "  (%s)" % prop["alias"], "",
            "theorem strip_%s %s :" % (short, params_sig),
            "    %s %s = %s := by" % (name, params_call, rhs),
            "  rfl", ""]
    read_sig = " ".join("(%s : BitVec 64)" % v for v, _ in prop["reads"])
    other_sig = " ".join("(%s : %s)" % (n, t) for n, t in prop["others"])
    pure_sig = (read_sig + " " + other_sig).strip()
    pure_call = " ".join([v for v, _ in prop["reads"]] + [n for n, _ in prop["others"]])
    lets = "".join("  let %s := %s\n" % (v, reindent(val, 4).lstrip()) for v, val in prop["lets"])
    value = reindent(prop["value"], 2)
    rhs_reads = "".join("      let %s := %s\n" % (v, reindent(val, 8).lstrip()) for v, val in prop.get("index_lets", []))
    rhs_reads += "".join("      let %s ← rX_bits %s\n" % (v, r) for v, r in prop["reads"])
    proof = ["  first", "  | rfl"]
    if prop["case_on"]:
        proof.append("  | (cases %s <;> simp only [%s, pure_%s, bind_assoc, pure_bind])" % (prop["case_on"], name, short))
    proof.append("  | simp only [%s, pure_%s, bind_assoc, pure_bind]" % (name, short))
    body = [
        "/-- the proposal: the clause's pure form, by the one rule -/",
        "def pure_%s %s : BitVec 64 :=" % (short, pure_sig),
        lets.rstrip("\n") if lets else "",
        value, "",
        "/-- the certificate: the emitted clause IS read, read, write the proposal, retire -/",
        "theorem strip_%s %s :" % (short, params_sig),
        "    %s %s =" % (name, params_call),
        "    (do",
        rhs_reads.rstrip("\n"),
        "      wX_bits %s (pure_%s %s)" % (prop["write"], short, pure_call),
        "      pure RETIRE_SUCCESS) := by",
    ] + proof + [""]
    return [ln for ln in body if ln is not None]


def namespaces_of(lean_dir):
    """The namespaces the emitted clauses live in, read from the files."""
    seen = []
    for fn in sorted(os.listdir(lean_dir)):
        if not fn.endswith(".lean"):
            continue
        stack = []
        for ln in open(os.path.join(lean_dir, fn)):
            m = re.match(r"^namespace (\S+)", ln)
            if m:
                stack.append(m.group(1))
                full = ".".join(stack)
                if full not in seen:
                    seen.append(full)
            elif re.match(r"^end (\S+)", ln) and stack:
                stack.pop()
        if seen:
            break
    return seen


def run(project, lib, out_dir, timeout_s=900, only=None):
    """Generate one Lean file per clause, compile each with `lake env lean`
    inside the built project, and record the verdicts."""
    lean_dir = os.path.join(project, lib)
    os.makedirs(out_dir, exist_ok=True)
    namespaces = namespaces_of(lean_dir)
    rows = []
    defs = None
    for clause in clauses_of(lean_dir):
        if only and clause["name"] not in only:
            continue
        prop = propose(clause)
        if "refused" in prop:
            # the effects rule reads only where the one rule refuses, so every clause the one
            # rule certifies is read exactly as before
            if defs is None:
                defs = emitted_defs(lean_dir)
            eprop = propose_effects(clause, defs)
            if "refused" not in eprop:
                prop = eprop
        row = {"clause": clause["name"], "file": clause["file"], "line": clause["line"],
               "params": clause["params"]}
        if "refused" in prop:
            row.update({"verdict": "REFUSED", "why": prop["refused"]})
            rows.append(row)
            print("  %-28s REFUSED  %s" % (clause["name"], prop["refused"]), flush=True)
            continue
        text = lean_file(clause, prop, lib, namespaces, lean_dir=lean_dir)
        path = os.path.join(out_dir, "Strip_%s.lean" % clause["name"][len("execute_"):])
        open(path, "w").write(text)
        t0 = time.time()
        try:
            p = subprocess.run(["lake", "env", "lean", path], cwd=project, capture_output=True,
                               text=True, timeout=timeout_s)
            rc, outp = p.returncode, (p.stdout + p.stderr)
        except subprocess.TimeoutExpired:
            rc, outp = -1, "TIMEOUT after %ds" % timeout_s
        secs = time.time() - t0
        errs = [ln for ln in outp.split("\n") if "error" in ln][:6]
        row.update({"shape": prop["shape"], "reads": prop.get("reads", []),
                    "write": prop.get("write"), "alias": prop.get("alias"),
                    "index_lets": prop.get("index_lets", []),
                    "case_on": prop.get("case_on"), "lean_file": path,
                    "verdict": "CERTIFIED" if rc == 0 else "FAILED", "rc": rc,
                    "seconds": round(secs, 1), "errors": errs})
        if prop.get("shape") == "effects":
            row.update({k: prop[k] for k in EFFECTS_ROW_KEYS})
        if prop.get("shape") == "arms":
            # which arms this clause is certified FOR. The walk must refuse an
            # instruction whose concrete arm is not in `pure_arms`: no definition
            # exists for it, so nothing can be stated about it.
            row.update({"pure_arms": prop.get("pure_arms", []),
                        "impure_arms": [arm_ident(c) for c, _ in prop.get("impure_arms", [])],
                        "others": prop.get("others", [])})
        rows.append(row)
        print("  %-28s %-9s %-8s %6.1fs %s" % (clause["name"], row["verdict"], prop["shape"],
                                                secs, ("; ".join(errs)[:120] if errs else "")), flush=True)
    summary = {"certified": sum(r["verdict"] == "CERTIFIED" for r in rows),
               "certified_per_arm": sum(1 for r in rows
                                        if r.get("shape") == "arms" and r["verdict"] == "CERTIFIED"),
               "arms_not_expressible": sorted({"%s.%s" % (r["clause"][len("execute_"):], a)
                                               for r in rows if r.get("shape") == "arms"
                                               for a in r.get("impure_arms", [])}),
               "failed": sum(r["verdict"] == "FAILED" for r in rows),
               "refused": sum(r["verdict"] == "REFUSED" for r in rows),
               "of": len(rows), "namespaces": namespaces, "lib": lib, "project": project}
    doc = {"summary": summary, "rows": rows}
    json.dump(doc, open(os.path.join(out_dir, "strip.json"), "w"), indent=1, sort_keys=True)
    print("  strip: certified %d, failed %d, refused %d, of %d" % (
        summary["certified"], summary["failed"], summary["refused"], summary["of"]), flush=True)
    return doc


# ------------------------------------------------------------------ the effects rule (floats)
# Written 2026-09-15 for the float clauses (plan leaf sail_model.strip). Where the one rule
# refuses, ONE more rule reads a clause whose effects go beyond one integer register write:
# float register reads and writes, a rounding mode selected from the control register, flags
# accrued. It reads the SIGNATURES of the emitted helpers a clause calls, never their names:
#
#   a READ     `let v ← do (F p)`   F : (i : T) : SailM (BitVec k), p a parameter of type T:
#                                   the pure form takes v
#   a SELECT   `match (← (F p)) with | none => X | .some v => (do REST)`
#                                   F : (x : T) : SailM (Option U), p a parameter of type T:
#                                   the pure form takes v : U; X stays in the monadic program
#   an EFFECT  `(F e)`              F : (x : BitVec k) : SailM Unit: e is an OUTPUT
#   a WRITE    `(F p e)`            F : (i : T) (data : BitVec k) : SailM Unit, p a parameter
#                                   of type T: e is the last OUTPUT
#   pure lets  `let x := e`, `let x : T := e`, `let (x, y) : T := e`
#   the retire `(pure RETIRE_SUCCESS)`
#
# A clause `let m := (p1, .., pn); match m with | (n1, .., .C, ..) => (do ARM) | ..` is that
# shape per alternative: every alternative must read, select, affect and write alike, and the
# pure form is a match on the parameter the constructors stand in.
#
# The pure form returns the outputs as one tuple (the effect values, then the written value).
# The certificate: the emitted clause IS "the reads and the selections, then the pure form's
# outputs handed to the effects and to the write in the emitted order, then the retire".
# Lean proves it or the row fails; nothing is trusted from Python.

EFFECT_READ = re.compile(r"^let (\w+) ← (?:do )?\(?\s*(\w+)\s+(\w+)\s*\)?\s*$")
EFFECT_SELECT = re.compile(r"^match \(←\s*\((\w+)\s+(\w+)\)\) with\s*\n(.*)$", re.S)
EFFECT_CALL = re.compile(r"^\((\w+)\s+(.*)\)\s*$", re.S)
TUPLE_LET = re.compile(r"^let \(([\w'\s,]+)\)\s*(?::\s*(.+?))?\s*:=\s*(.*)$", re.S)
MERGE_LET = re.compile(r"^let (\w+) := \(([^()]*)\)\s*$")
EFFECTS_ROW_KEYS = ("read_fns", "read_kinds", "prefix", "selects", "effects", "write_fn",
                    "write_kind", "write_type", "tail", "pure_params")


def signature(defs, name):
    """([(param, type)] of the explicit binders, the return type) of an emitted
    definition, read off its own header; None when there is no such definition."""
    text = defs.get(name)
    if not text:
        return None
    head = text.split(":=", 1)[0].strip()
    m = re.match(r"^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+|private\s+|protected\s+)*(?:def|abbrev)\s+[A-Za-z0-9_'.]+\s*", head)
    if not m:
        return None
    rest = head[m.end():]
    depth, i = 0, 0
    while i < len(rest):
        ch = rest[i]
        if ch in "({[":
            depth += 1
        elif ch in ")}]":
            depth -= 1
        elif ch == ":" and depth == 0:
            break
        i += 1
    if i >= len(rest):
        return None
    binders = re.sub(r"\{[^{}]*\}|\[[^\[\]]*\]", " ", rest[:i])
    return split_params(binders), re.sub(r"\s+", " ", rest[i + 1:].strip())


def _in_monad(ret):
    m = re.match(r"^SailM\s+(.*)$", ret or "")
    return strip_outer_parens(m.group(1)) if m else None


def _is_bits(t):
    return strip_outer_parens(t or "").startswith("BitVec")


def _mentions(name, text):
    return re.search(r"(?<![\w'])%s(?![\w'])" % re.escape(name), text) is not None


def join_match_arms(els):
    """A `match ... with` element takes the `| ...` elements after it as its
    alternatives (the emitter writes them at the element's own indentation)."""
    out, open_match = [], False
    for e in els:
        if open_match and e.startswith("|"):
            out[-1] += "\n" + e
            continue
        out.append(e)
        first = e.split("\n")[0].rstrip()
        open_match = first.startswith("match ") and first.endswith("with")
    return out


def split_arms(text):
    """[(pattern, right-hand side)] of a match's alternatives, split at the lines
    that open an alternative at the least indentation."""
    lines = text.split("\n")
    starts = [ln for ln in lines if ln.lstrip().startswith("|")]
    if not starts:
        return []
    base = min(len(ln) - len(ln.lstrip()) for ln in starts)
    arms, cur = [], None
    for ln in lines:
        if ln.lstrip().startswith("|") and len(ln) - len(ln.lstrip()) == base:
            if cur is not None:
                arms.append(cur)
            cur = ln.strip()[1:]
        elif cur is not None:
            cur += "\n" + ln
    if cur is not None:
        arms.append(cur)
    out = []
    for a in arms:
        pat, sep, rhs = a.partition("=>")
        if not sep:
            return []
        out.append((pat.strip(), rhs))
    return out


def do_block_elements(rhs):
    """The do-elements of an alternative's `(do ...)` block, or None."""
    t = strip_outer_parens(rhs.strip())
    lines = t.split("\n")
    if lines[0].strip() != "do" or len(lines) < 2:
        return None
    return join_match_arms(elements([ln for ln in lines[1:] if ln.strip()]))


def effect_steps(els, params, defs, binding):
    """The clause's steps by the effects rule, or a refusal. `binding` maps a
    name a tuple pattern binds to the parameter it stands for."""
    ptype = dict(params)
    steps = []
    for idx, e in enumerate(els):
        first = e.split("\n")[0].strip()
        m = EFFECT_READ.match(e)
        if m:
            var, fn, p = m.group(1), m.group(2), binding.get(m.group(3), m.group(3))
            sig = signature(defs, fn)
            inner = _in_monad(sig[1]) if sig else None
            if not (sig and len(sig[0]) == 1 and p in ptype and sig[0][0][1] == ptype[p] and _is_bits(inner)):
                return {"refused": "a monadic let that is not a register read by its helper's signature: %s" % first}
            steps.append({"kind": "read", "var": var, "fn": fn, "param": p, "reg_type": ptype[p], "type": inner})
            continue
        m = EFFECT_SELECT.match(e)
        if m:
            fn, p, rest = m.group(1), binding.get(m.group(2), m.group(2)), m.group(3)
            sig = signature(defs, fn)
            inner = _in_monad(sig[1]) if sig else None
            om = re.match(r"^Option\s+(.+)$", inner or "")
            if not (sig and len(sig[0]) == 1 and p in ptype and sig[0][0][1] == ptype[p] and om):
                return {"refused": "a match on an effect that is not a selection by its helper's signature: %s" % first}
            none_rhs, some_var, some_rhs = None, None, None
            for pat, rhs in split_arms(rest):
                if pat == "none":
                    none_rhs = one_line(rhs.strip())
                else:
                    sm = re.match(r"^\.?some\s+(\w+'*)$", pat)
                    if sm:
                        some_var, some_rhs = sm.group(1), rhs
            if none_rhs is None or some_var is None or idx != len(els) - 1:
                return {"refused": "a selection that is not `none` / `some v` closing the clause: %s" % first}
            inner_els = do_block_elements(some_rhs)
            if inner_els is None:
                return {"refused": "a selection whose `some` alternative is not a do block: %s" % first}
            sub = effect_steps(inner_els, params, defs, binding)
            if "refused" in sub:
                return sub
            steps.append({"kind": "select", "var": some_var, "fn": fn, "param": p,
                          "type": strip_outer_parens(om.group(1)), "none": none_rhs})
            return {"steps": steps + sub["steps"]}
        if END.match(e):
            if idx != len(els) - 1:
                return {"refused": "an element after RETIRE_SUCCESS: %s" % first}
            steps.append({"kind": "retire"})
            continue
        m = TUPLE_LET.match(e)
        if m and "←" not in e:
            steps.append({"kind": "let", "pattern": "(%s)" % ", ".join(x.strip() for x in m.group(1).split(",")),
                          "type": m.group(2), "value": m.group(3).strip()})
            continue
        m = PURE_LET.match(e)
        if m and "←" not in e:
            steps.append({"kind": "let", "pattern": m.group(1), "type": m.group(2), "value": m.group(3).strip()})
            continue
        m = EFFECT_CALL.match(e)
        if m and strip_outer_parens(e.strip()) != e.strip() and "←" not in e:
            fn, args = m.group(1), m.group(2).strip()
            sig = signature(defs, fn)
            if sig and _in_monad(sig[1]) == "Unit":
                ps = sig[0]
                am = re.match(r"^(\w+)\s+(.+)$", args, re.S)
                p = binding.get(am.group(1), am.group(1)) if am else None
                if len(ps) == 2 and am and p in ptype and ps[0][1] == ptype[p] and _is_bits(ps[1][1]):
                    steps.append({"kind": "write", "fn": fn, "param": p, "reg_type": ptype[p],
                                  "value": am.group(2).strip(), "type": ps[1][1]})
                    continue
                if len(ps) == 1 and _is_bits(ps[0][1]):
                    steps.append({"kind": "effect", "fn": fn, "value": args, "type": ps[0][1]})
                    continue
            return {"refused": "a statement that is neither a register write nor an effect with a value, by its helper's signature: %s" % first}
        return {"refused": "an element the effects rule does not know: %s" % first}
    return {"steps": steps}


def _skeleton(steps):
    out = []
    for s in steps:
        if s["kind"] == "read":
            out.append(("read", s["var"], s["fn"], s["param"]))
        elif s["kind"] == "select":
            out.append(("select", s["var"], s["fn"], s["param"], s["none"]))
        elif s["kind"] == "effect":
            out.append(("effect", s["fn"]))
        elif s["kind"] == "write":
            out.append(("write", s["fn"], s["param"]))
        elif s["kind"] == "retire":
            out.append(("retire",))
    return out


def propose_effects(clause, defs):
    """The effects rule. Returns a proposal of shape `effects`, or a refusal."""
    if not clause.get("monadic", True):
        return {"refused": "a pure clause"}
    params = clause["params"]
    els = join_match_arms(elements(clause["body"]))
    if len(els) == 2 and MERGE_LET.match(els[0]) and els[1].startswith("match "):
        mvar, comps_text = MERGE_LET.match(els[0]).groups()
        comps = [c.strip() for c in comps_text.split(",")]
        mm = re.match(r"^match (\w+) with\s*\n(.*)$", els[1], re.S)
        if not mm or mm.group(1) != mvar:
            return {"refused": "a tuple match that is not on the tuple: %s" % els[1].split("\n")[0]}
        alts = split_arms(mm.group(2))
        if not alts:
            return {"refused": "a tuple match with no alternative the rule reads"}
        case_pos, arms = None, []
        for pat, rhs in alts:
            pm = re.match(r"^\((.*)\)$", pat)
            parts = [x.strip() for x in pm.group(1).split(",")] if pm else []
            if len(parts) != len(comps):
                return {"refused": "an alternative whose pattern is not the tuple: %s" % pat}
            binding, ctor, pos = {}, None, None
            for k, x in enumerate(parts):
                if re.match(r"^\.\w+$", x):
                    if ctor is not None:
                        return {"refused": "an alternative with two constructors: %s" % pat}
                    ctor, pos = x, k
                elif re.match(r"^\w+$", x):
                    binding[x] = comps[k]
                else:
                    return {"refused": "an alternative pattern the rule does not read: %s" % pat}
            if ctor is None or (case_pos is not None and pos != case_pos):
                return {"refused": "alternatives that do not case on one component: %s" % pat}
            case_pos = pos
            inner = do_block_elements(rhs)
            if inner is None:
                return {"refused": "an alternative that is not a do block: %s" % pat}
            sub = effect_steps(inner, params, defs, binding)
            if "refused" in sub:
                return sub
            for s in sub["steps"]:               # a name the pattern binds, used in a value, is its parameter
                for key in ("value",):
                    if key in s:
                        for n, prm in binding.items():
                            s[key] = re.sub(r"(?<![\w'])%s(?![\w'])" % re.escape(n), prm, s[key])
            arms.append((ctor, sub["steps"]))
        if any(_skeleton(st) != _skeleton(arms[0][1]) for _, st in arms):
            return {"refused": "alternatives that read, select, affect or write differently"}
        return effects_prop(clause, arms, comps[case_pos])
    sub = effect_steps(els, params, defs, {})
    if "refused" in sub:
        return sub
    return effects_prop(clause, [(None, sub["steps"])], None)


def effects_prop(clause, arms, case_on):
    steps0 = arms[0][1]
    kinds = [s["kind"] for s in steps0]
    writes = [s for s in steps0 if s["kind"] == "write"]
    if len(writes) != 1:
        return {"refused": "%d register writes" % len(writes)}
    if not kinds or kinds[-1] != "retire":
        return {"refused": "no RETIRE_SUCCESS at the end"}
    first_out = min(i for i, k in enumerate(kinds) if k in ("effect", "write"))
    if any(k in ("read", "select", "let") for k in kinds[first_out:]):
        return {"refused": "a read, a selection or a let after an effect or the write"}
    reads = [s for s in steps0 if s["kind"] == "read"]
    selects = [s for s in steps0 if s["kind"] == "select"]
    effects = [s for s in steps0 if s["kind"] == "effect"]
    tail = [["effect", effects.index(s)] if s["kind"] == "effect" else ["write", 0] for s in steps0[first_out:-1]]
    arm_rows = []
    for ctor, steps in arms:
        arm_rows.append({"ctor": ctor,
                         "lets": [{"pattern": s["pattern"], "type": s["type"], "value": s["value"]}
                                  for s in steps if s["kind"] == "let"],
                         "effect_values": [s["value"] for s in steps if s["kind"] == "effect"],
                         "write_value": [s["value"] for s in steps if s["kind"] == "write"][0]})
    pure_text = " ".join([l["value"] for a in arm_rows for l in a["lets"]] +
                         [v for a in arm_rows for v in a["effect_values"] + [a["write_value"]]])
    others = [(n, t) for n, t in clause["params"] if n == case_on or _mentions(n, pure_text)]
    pure_params = [(r["var"], r["type"]) for r in reads] + [(s["var"], s["type"]) for s in selects] + others
    consumed = {s["param"] for s in reads + selects} | {writes[0]["param"]}
    return {"shape": "effects", "reads": [[r["var"], r["param"]] for r in reads],
            "read_fns": [r["fn"] for r in reads], "read_kinds": [r["reg_type"] for r in reads],
            "prefix": [dict({"kind": s["kind"], "var": s["var"], "fn": s["fn"], "param": s["param"]},
                            **({"none": s["none"], "type": s["type"]} if s["kind"] == "select" else {}))
                       for s in steps0 if s["kind"] in ("read", "select")],
            "selects": [{"var": s["var"], "fn": s["fn"], "param": s["param"], "type": s["type"], "none": s["none"]}
                        for s in selects],
            "effects": [{"fn": e["fn"], "type": e["type"]} for e in effects],
            "write": writes[0]["param"], "write_fn": writes[0]["fn"], "write_kind": writes[0]["reg_type"],
            "write_type": writes[0]["type"], "tail": tail, "arms": arm_rows, "case_on": case_on,
            "pure_params": pure_params, "regs": [n for n, _ in clause["params"] if n in consumed],
            "others": others}


def lean_body_effects(clause, prop):
    """The pure form of a clause read by the effects rule, and its certificate."""
    name = clause["name"]
    short = name[len("execute_"):]
    params_sig = " ".join("(%s : %s)" % (n, t) for n, t in clause["params"])
    params_call = " ".join(n for n, _ in clause["params"])
    pure_sig = " ".join("(%s : %s)" % (n, t) for n, t in prop["pure_params"])
    pure_call = " ".join(n for n, _ in prop["pure_params"])
    out_types = [e["type"] for e in prop["effects"]] + [prop["write_type"]]
    ret = " × ".join("(%s)" % strip_outer_parens(t) for t in out_types)
    tup = lambda vals: ("(" + ", ".join(vals) + ")") if len(vals) > 1 else vals[0]

    def arm_lines(arm, ind):
        out = []
        for l in arm["lets"]:
            typ = " : %s" % l["type"] if l["type"] else ""
            out.append("%slet %s%s := %s" % (" " * ind, l["pattern"], typ, reindent(l["value"], ind + 2).lstrip()))
        out.append(" " * ind + tup(arm["effect_values"] + [arm["write_value"]]))
        return out

    body = ["/-- the proposal: the clause's pure form by the effects rule; its outputs are the values",
            "handed to the effects and to the register write, in that order -/",
            "def pure_%s %s : %s :=" % (short, pure_sig, ret)]
    if prop["case_on"]:
        body.append("  match %s with" % prop["case_on"])
        for arm in prop["arms"]:
            body.append("  | %s =>" % arm["ctor"])
            body += arm_lines(arm, 4)
    else:
        body += arm_lines(prop["arms"][0], 2)
    outs = ["out_%d" % k for k in range(len(out_types))]
    rhs, ind = ["    (do"], 6
    for s in prop["prefix"]:
        if s["kind"] == "read":
            rhs.append("%slet %s ← %s %s" % (" " * ind, s["var"], s["fn"], s["param"]))
        else:
            rhs.append("%smatch (← %s %s) with" % (" " * ind, s["fn"], s["param"]))
            rhs.append("%s| none => %s" % (" " * ind, s["none"]))
            rhs.append("%s| .some %s =>" % (" " * ind, s["var"]))
            ind += 2
            rhs.append("%sdo" % (" " * ind))
            ind += 2
    rhs.append("%slet %s := pure_%s %s" % (" " * ind, tup(outs), short, pure_call))
    for kind, k in prop["tail"]:
        if kind == "effect":
            rhs.append("%s%s %s" % (" " * ind, prop["effects"][k]["fn"], outs[k]))
        else:
            rhs.append("%s%s %s %s" % (" " * ind, prop["write_fn"], prop["write"], outs[-1]))
    rhs.append("%spure RETIRE_SUCCESS) := by" % (" " * ind))
    unfold = "%s, pure_%s, bind_assoc, pure_bind" % (name, short)
    proof = ["  first", "  | rfl"]
    if prop["case_on"]:
        proof.append("  | (cases %s <;> rfl)" % prop["case_on"])
    proof.append("  | (simp only [%s])" % unfold)
    if prop["case_on"]:
        proof.append("  | (cases %s <;> simp only [%s])" % (prop["case_on"], unfold))
    return body + ["",
                   "/-- the certificate: the emitted clause IS the reads and the selections, then the pure",
                   "form's outputs handed to the effects and to the write, then the retire -/",
                   "theorem strip_%s %s :" % (short, params_sig),
                   "    %s %s =" % (name, params_call)] + rhs + proof + [""]
