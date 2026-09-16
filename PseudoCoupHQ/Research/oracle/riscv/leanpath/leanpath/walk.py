"""ArchUnit.meaning -- the walk: a compiled body's meaning as one Lean
expression, by Sail's own decoder and Sail's own execute, certified.

Plan leaves hq...lean_proof_path.arch_unit.{meaning,decode,compose}
(log 274 §4; the fourth launch's design, 2026-09-14):

  decode      each word of the body is handed to Sail's own decoder,
              EVALUATED in the executable variant of the emit (`#eval`);
              what comes back is the `instruction` value, printed by its
              own `Repr`, which is valid Lean syntax. No table of
              mnemonics anywhere: the disassembler's text is kept only as
              the display label.
  compose     the proposal: thread a register file of Lean names through
              the certified pure forms (SailModel.strip) of the decoded
              instructions, in address order; an alias clause re-dispatches
              to its target; the answering register's expression is the
              unit's proposed meaning. Register arguments that are not
              literal indices (`creg2reg_idx rsdc`) are evaluated by the
              same `#eval` route.
  meaning     the certificate: a Lean theorem that running the decoded
              instructions through the model's own `execute` from any state
              holding the arguments in the ABI registers ends with the
              proposal in the answering register. Proved by `simp` with the
              strip certificates and the model's own register functions.
              If the proposal is wrong, the theorem fails: a refusal row.

The return at the end of a carved body is not walked (it writes the PC);
its word is decoded and recorded, so that the record shows what was
excluded and why.
"""
import json
import os
import re
import shutil
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

# let-sharing in compose: OFF by default so existing runs are bit-identical.
# Set WALK_LET_SHARING=1 to bind each instruction's result to a name instead of
# substituting it, which keeps the term linear in the instruction count.
LET_SHARING = os.environ.get("WALK_LET_SHARING", "") not in ("", "0", "no")

ABI_ARGS = {10: "a", 11: "b", 12: "c", 13: "d"}   # a0..a3 -> the unknowns; the answer is a0 (x10)
ANSWER = 10
# floats (2026-09-15): the float argument registers fa0..fa3 (f10..f13) -> the float unknowns. The
# answer is the ABI answer register the body writes LAST, a0 (x10) or fa0 (f10): machine form, since
# the corpus's own sources state the result type as the compiler's `__typeof__`. A body that writes
# no float register answers a0 exactly as before.
FABI_ARGS = {10: "fa0", 11: "fa1", 12: "fa2", 13: "fa3"}
MAX_WORDS = int(os.environ.get("WALK_MAX_WORDS", "64"))   # a resource bound, not a spelling


def sh(cmd, cwd=None, timeout=1800, env=None):
    t0 = time.time()
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env)
    return p.returncode, time.time() - t0, p.stdout + p.stderr


def lean_run(project, path, timeout_s=900):
    try:
        return sh(["lake", "env", "lean", path], cwd=project, timeout=timeout_s)
    except subprocess.TimeoutExpired:
        return -1, timeout_s, "TIMEOUT after %ds" % timeout_s


# ------------------------------------------------------------------ carve
OBJDUMP = "llvm-objdump -d -M no-aliases --mattr=+m,+a,+f,+d,+c,+zba,+zbb,+zbs"
DIS_LINE = re.compile(r"^\s*([0-9a-f]+):\s+((?:[0-9a-f]{2}\s+)+|[0-9a-f]{4,8})\s*(\S+)?\s*(.*)$")


def carve(obj_path, symbol):
    """The instructions of one symbol: [(hex word, mnemonic, operands)]."""
    rc, _, out = sh(OBJDUMP.split() + ["--disassemble-symbols=%s" % symbol, obj_path])
    rows = []
    for ln in out.split("\n"):
        m = DIS_LINE.match(ln)
        if not m or not m.group(3):
            continue
        enc = m.group(2).strip()
        if " " in enc:                       # byte pairs, little-endian -> one word
            bs = enc.split()
            enc = "".join(reversed(bs))
        rows.append((enc.lower(), m.group(3), m.group(4).strip()))
    # the padding after a function (zero words up to the next alignment) is not the body: a zero word
    # is the architecture's defined-illegal encoding, never an instruction a compiler meant
    while rows and set(rows[-1][0]) == {"0"}:
        rows.pop()
    return rc, out, rows


def compile_c(src_path, out_obj, flags):
    cmd = flags.split() + ["-c", src_path, "-o", out_obj]
    return sh(cmd)


def compile_unit(u, obj, out_dir):
    """One source to one riscv64 object or binary by the language's own route
    (the unit's `flags`, whose leading K=V tokens are environment); returns
    (rc, seconds, output, the symbol to carve)."""
    lang = u.get("lang", "c")
    toks = u["flags"].split()
    env = dict(os.environ)
    while toks and "=" in toks[0] and not toks[0].startswith("-"):
        k, v = toks.pop(0).split("=", 1)
        env[k] = v
    if lang == "go":
        d = os.path.join(out_dir, u["name"] + "_go")
        os.makedirs(d, exist_ok=True)
        shutil.copyfile(u["source"], os.path.join(d, "main.go"))
        open(os.path.join(d, "go.mod"), "w").write("module unit\n\ngo 1.26\n")
        rc, secs, out = sh(toks + ["-o", obj, "."], cwd=d, env=env)
        return rc, secs, out, "main." + u["symbol"]
    if lang == "rust":
        rc, secs, out = sh(toks + ["-o", obj, u["source"]], env=env)
        return rc, secs, out, u["symbol"]
    rc, secs, out = sh(toks + ["-c", u["source"], "-o", obj], env=env)
    return rc, secs, out, u["symbol"]


# ----------------------------------------------------------------- decode
def lib_of(project):
    """The lean_lib name of a lake project, from its lakefile."""
    t = open(os.path.join(project, "lakefile.toml")).read()
    m = re.search(r"\[\[lean_lib\]\]\s*\nname = \"([^\"]+)\"", t)
    return m.group(1)


STATE_EXPR = "s0"     # the state the decoder runs on, built by state_defs below


def registers_of(lean_dir):
    """The constructors of the emitted `Register` type (one-line inductive)."""
    t = open(os.path.join(lean_dir, "Defs.lean")).read()
    m = re.search(r"^inductive Register(?:\s*:\s*Type)?\s+where(.*?)(?=^\s*deriving|^\S)", t, re.S | re.M)
    if not m:
        raise ValueError("no `inductive Register where` in %s" % lean_dir)
    body = m.group(1)
    names = []
    for x in body.split("|"):
        x = x.strip().split()
        if x and re.match(r"^[A-Za-z_]\w*$", x[0]):
            names.append(x[0])
    return names


def state_defs(lean_dir):
    """The state the model's own emulator runs on (lean_emulator/LeanRiscv.lean):
    every register written with a value first (the emulator writes each one
    with `undefined_*`; here `default`), then sail_model_init (the 36 with
    initializers), then init_model (reset: misa and the rest). The generated
    init alone leaves the other registers absent, and reset reads them."""
    regs = registers_of(lean_dir)
    lines = ["/-- a blank machine state, as the emulator's own main starts from -/",
             "def blank : SequentialState RegisterType trivialChoiceSource :=",
             "  { regs := ∅, choiceState := (), mem := ∅, tags := (), cycleCount := 0, sailOutput := #[] }",
             "/-- every register present, with a default value (the emulator's own first step) -/",
             "def filled : SequentialState RegisterType trivialChoiceSource :=",
             "  match ((do"]
    lines += ["      PreSail.writeReg Register.%s default" % r for r in regs]
    lines += ["      pure ()) : SailM Unit) blank with | .ok _ s => s | .error _ s => s",
              "/-- then the model's own init and reset -/",
              "def s0 : SequentialState RegisterType trivialChoiceSource :=",
              "  match ((do sail_model_init (); init_model \"\") : SailM Unit) filled with | .ok _ s => s | .error _ s => s", ""]
    return lines


def eval_file(exec_project, lib, evals, path):
    """One Lean file of #evals in the executable variant; returns the printed
    lines in order (one per #eval), or errors."""
    from . import strip as ST
    ns = ST.namespaces_of(os.path.join(exec_project, lib))
    head = ["import %s" % lib,
            "open Sail Sail.ConcurrencyInterfaceV1 PreSail %s" % " ".join(ns),
            "set_option maxHeartbeats 1000000000",
            "set_option maxRecDepth 100000", ""] + state_defs(os.path.join(exec_project, lib))
    body = []
    for tag, expr in evals:
        body.append('#eval IO.println ("%s\\t" ++ (%s))' % (tag, expr))
    open(path, "w").write("\n".join(head + body) + "\n")
    rc, secs, out = lean_run(exec_project, path)
    got, cur = {}, None
    for ln in out.split("\n"):
        if ln.startswith("TODO:") or ln.startswith("PANIC") or ln.strip() == "":
            continue
        if "\t" in ln and not ln.startswith(" "):
            tag, _, val = ln.partition("\t")
            cur = tag.strip()
            got[cur] = val.strip()
        elif cur is not None and ln.startswith(" ") and "error" not in ln:
            got[cur] += " " + ln.strip()          # a value continued on the next line
        else:
            cur = None
    errs = [ln for ln in out.split("\n") if "error" in ln][:8]
    return rc, secs, got, errs


def decode_expr(word_hex):
    """The #eval expression for one word: Sail's decoder on the model's own
    initial state (extensions as the config enables them)."""
    n = len(word_hex) * 4
    dec = "encdec_backwards" if n == 32 else "encdec_compressed_backwards"
    return ("(match (%s (0x%s#%d)) (%s) with "
            "| .ok i _ => toString (repr i) | .error _ _ => \"ERROR\")" % (dec, word_hex, n, STATE_EXPR))


# ----------------------------------------------------- the Repr as a term
REPR_CTOR = re.compile(r"^(?:[A-Za-z_][\w.]*\.)?instruction\.(\w+)\s*(.*)$", re.S)


def parse_repr(text):
    """`LeanIMZ.instruction.DIVW (LeanIMZ.regidx.Regidx 11#5, ..., false)`
    -> (ctor, [component texts]); components split at top-level commas of
    the outer tuple; a single non-tuple argument is one component."""
    m = REPR_CTOR.match(text.strip())
    if not m:
        return None, []
    ctor, rest = m.group(1), m.group(2).strip()
    if rest == "":
        return ctor, []
    if rest.startswith("(") and rest.endswith(")"):
        inner = rest[1:-1]
        comps, depth, cur = [], 0, ""
        for ch in inner:
            if ch in "([{":
                depth += 1
            elif ch in ")]}":
                depth -= 1
            if ch == "," and depth == 0:
                comps.append(cur.strip())
                cur = ""
                continue
            cur += ch
        if cur.strip():
            comps.append(cur.strip())
        return ctor, comps
    return ctor, [rest]


REGIDX_LIT = re.compile(r"^(?:[\w.]*\.)?Regidx\s+(0x[0-9a-fA-F]+|\d+)#5$")


def reg_number(text):
    s = text.strip()
    while s.startswith("(") and s.endswith(")"):
        s = s[1:-1].strip()
    m = REGIDX_LIT.match(s)
    return int(m.group(1), 0) if m else None


FREGIDX_LIT = re.compile(r"^(?:[\w.]*\.)?Fregidx\s+(0x[0-9a-fA-F]+|\d+)#5$")


def freg_number(text):
    """A float register index literal (`Fregidx 10#5`) -> its number."""
    s = text.strip()
    while s.startswith("(") and s.endswith(")"):
        s = s[1:-1].strip()
    m = FREGIDX_LIT.match(s)
    return int(m.group(1), 0) if m else None


# ---------------------------------------------------------------- compose
class Strip:
    """The certified pure forms, read from strip.json."""
    def __init__(self, strip_json):
        d = json.load(open(strip_json))
        self.rows = {r["clause"][len("execute_"):]: r for r in d["rows"]}
        self.aliases = {}
        for name, r in self.rows.items():
            if r.get("shape") == "alias" and r["verdict"] == "CERTIFIED":
                text = r.get("alias")
                if not text:                       # an older record: read the certificate file
                    lf = open(r["lean_file"]).read()
                    m = re.search(r"def alias_%s [^\n]*:=\n\s*\((.*?)\)\n\ntheorem" % re.escape(name), lf, re.S)
                    text = m.group(1).strip() if m else None
                self.aliases[name] = text

    def certified(self, name):
        r = self.rows.get(name)
        return r is not None and r["verdict"] == "CERTIFIED"


def bind_params(row, comps):
    """The clause's parameters bound to the decoded components, positionally."""
    names = [n for n, _ in row["params"]]
    if len(names) != len(comps):
        return None
    return dict(zip(names, comps))


def subst(expr, binding):
    """Replace parameter names in a register expression by their bound texts."""
    out = expr
    for n, v in sorted(binding.items(), key=lambda kv: -len(kv[0])):
        out = re.sub(r"\b%s\b" % re.escape(n), "(" + v + ")", out)
    return out


def resolve_alias(strip, ctor, comps):
    """Follow ExecuteAs aliases to the executing clause: returns (ctor, comps)
    of the target, or None if an alias is unknown."""
    seen = 0
    while ctor in strip.aliases and seen < 4:
        row = strip.rows[ctor]
        binding = bind_params(row, comps)
        if binding is None or strip.aliases[ctor] is None:
            return None
        target = subst(strip.aliases[ctor], binding)
        m = re.match(r"^(\w+)\s*\((.*)\)$", target, re.S)
        if not m:
            return None
        ctor = m.group(1)
        inner = m.group(2)
        comps, depth, cur = [], 0, ""
        for ch in inner:
            if ch in "([{":
                depth += 1
            elif ch in ")]}":
                depth -= 1
            if ch == "," and depth == 0:
                comps.append(cur.strip())
                cur = ""
                continue
            cur += ch
        if cur.strip():
            comps.append(cur.strip())
        seen += 1
    return ctor, comps


def compose(strip, decoded, reg_eval):
    """decoded: [(ctor, comps)] in address order, the return excluded.
    reg_eval(expr) -> register number for a non-literal register expression
    (evaluated by Lean). Returns (proposal, env, steps) or a refusal."""
    env = {0: "zero_reg"}
    for k, v in ABI_ARGS.items():
        env[k] = v
    steps = []
    shared = []               # (name, call) in order, when LET_SHARING is on
    fenv, selects, answer = dict(FABI_ARGS), [], "x"      # floats: the float register file, the selections
    for ctor, comps in decoded:
        res = resolve_alias(strip, ctor, comps)
        if res is None:
            return {"refused": "alias of %s could not be followed" % ctor}
        ctor2, comps2 = res
        if ctor2 in getattr(strip, "no_effect", set()):
            # a clause whose body is only the retire (an alignment `nop`, a hint) changes no register:
            # the state passes through; the certificate unfolds its execute clause to `pure RETIRE_SUCCESS`
            steps.append({"ctor": ctor2, "binding": {}, "reads": [], "write": None, "call": None, "no_effect": True})
            continue
        if strip.certified(ctor2) and strip.rows[ctor2].get("shape") == "effects":
            res = compose_effects(strip.rows[ctor2], ctor2, comps2, env, fenv, reg_eval, selects)
            if "refused" in res:
                return res
            steps.append(res["step"])
            if res["answer"]:
                answer = res["answer"]
            continue
        arm_form = None
        if strip.certified(ctor2) and strip.rows[ctor2].get("shape") == "arms":
            # Sail put several instructions in one clause and chose between them
            # with a match. Only some arms are a function of their reads, so the
            # clause is certified PER ARM. Take the arm this instruction actually
            # decoded to; refuse if it is one of the arms with no definition.
            row = strip.rows[ctor2]
            binding = bind_params(row, comps2)
            if binding is None:
                return {"refused": "arity of %s: %d params, %d components" % (
                    ctor2, len(row["params"]), len(comps2))}
            case_on = row.get("case_on")
            arm = binding.get(case_on)
            arm = re.sub(r"^.*\.", "", str(arm).strip().strip("()")) if arm is not None else None
            if arm is None:
                return {"refused": "%s: the arm is not resolved from the decode" % ctor2}
            if arm not in row.get("pure_arms", []):
                return {"refused": "%s arm %s has no pure form (not expressible: %s)" % (
                    ctor2, arm, ", ".join(row.get("impure_arms", [])))}
            arm_form = "%s_%s" % (ctor2, arm)
        elif not strip.certified(ctor2) or strip.rows[ctor2].get("shape") != "straight":
            return {"refused": "no certified pure form for %s (%s)" % (
                ctor2, strip.rows.get(ctor2, {}).get("why", strip.rows.get(ctor2, {}).get("verdict", "absent")))}
        row = strip.rows[ctor2]
        binding = bind_params(row, comps2)
        if binding is None:
            return {"refused": "arity of %s: %d params, %d components" % (ctor2, len(row["params"]), len(comps2))}
        args = []
        for var, rexpr in row["reads"]:
            rtext = subst(rexpr, binding)
            k = reg_number(rtext)
            if k is None:
                k = reg_eval(rtext)
            if k is None:
                return {"refused": "register of read %s not resolved" % rtext}
            if k not in env:
                return {"refused": "reads x%d, outside the ABI arguments" % k}
            args.append(env[k])
        for n, t in row["params"]:
            if t != "regidx" and not (n in [x for x in binding] and False):
                pass
        others = [binding[n] for n, t in row["params"] if t != "regidx"]
        if arm_form is not None:
            # the arm is baked into the name, so it is not an argument
            others = [binding[n] for n, t in row["params"]
                      if t != "regidx" and n != row.get("case_on")]
        # the pure form's parameter order: reads, then the non-register params in header order
        # (regidx params consumed by reads/writes are not parameters of the pure form)
        call = "(pure_%s %s)" % (arm_form or ctor2,
                                 " ".join(["(%s)" % a for a in args] + ["(%s)" % o for o in others]))
        if LET_SHARING:
            # Substituting each register's value into every later use copies a
            # value used twice, so the term's depth grows with the body and Lean's
            # kernel gives up ("deep recursion detected"). Bind each instruction's
            # result to a name instead: the term is then linear in the instruction
            # count and a shared value is written once. log 278 section 7.3.
            nm = "w%d" % len(shared)
            shared.append((nm, call))
            call = nm
        wtext = subst(row["write"], binding)
        wk = reg_number(wtext)
        if wk is None:
            wk = reg_eval(wtext)
        if wk is None:
            return {"refused": "register of write %s not resolved" % wtext}
        if wk != 0:
            env[wk] = call
        if wk == ANSWER:
            answer = "x"
        steps.append({"ctor": ctor2, "binding": binding, "reads": args, "write": wk, "call": call,
                      "form": arm_form or ctor2})
    if ANSWER not in env:
        return {"refused": "the answering register was never written"}
    def wrap(term):
        """The answer under every binding, in order. Each binding references only
        earlier names and the ABI unknowns, so keeping them all is correct by
        construction; an unused one is harmless and `simp` drops it. Pruning was
        tried and removed: getting the reachability wrong drops a needed binding
        and the term stops typechecking, which is a worse failure than a few
        spare lets."""
        if not shared:
            return term
        return "(" + "".join("let %s := %s;\n" % (nm, cl) for nm, cl in shared) + term + ")"
    out = {"proposal": wrap(env[ANSWER]), "env": env, "steps": steps, "shared": shared}
    if answer == "f" or selects or any(st.get("effects") for st in steps):
        out.update({"proposal": wrap(fenv[ANSWER] if answer == "f" else env[ANSWER]),
                    "answer_reg": "%s%d" % (answer, ANSWER), "fenv": fenv, "selects": selects})
    return out


def compose_effects(row, ctor, comps, env, fenv, reg_eval, selects):
    """One instruction whose clause the effects rule read (strip.propose_effects): each read
    comes from the integer or the float register file by its parameter's own type, a
    selection (the rounding mode) becomes an unknown of its own type stated as a hypothesis
    on the state, and the write goes to the file of its parameter's type. The effects (the
    accrued flags) are outputs of the pure form the walk does not follow. Returns
    {"step", "answer"} or a refusal."""
    binding = bind_params(row, comps)
    if binding is None:
        return {"refused": "arity of %s: %d params, %d components" % (ctor, len(row["params"]), len(comps))}

    def number(text, typ):
        k = reg_number(text) if typ == "regidx" else freg_number(text)
        return reg_eval(text) if k is None else k
    args = []
    for (var, rexpr), typ in zip(row["reads"], row["read_kinds"]):
        rtext = subst(rexpr, binding)
        files = env if typ == "regidx" else fenv
        k = number(rtext, typ)
        if k is None:
            return {"refused": "register of read %s not resolved" % rtext}
        if k not in files:
            return {"refused": "reads %s%d, outside the ABI arguments" % ("x" if typ == "regidx" else "f", k)}
        args.append(files[k])
    for s in row["selects"]:
        name = "sel%d" % len(selects)
        selects.append({"name": name, "fn": s["fn"], "arg": subst(s["param"], binding), "type": s["type"]})
        args.append(name)
    others = [binding[n] for n, _ in row["pure_params"] if n in binding]
    call = "(pure_%s %s)" % (ctor, " ".join("(%s)" % a for a in args + others))
    written = call + ".2" * len(row["effects"])          # the written value is the tuple's last output
    wtext = subst(row["write"], binding)
    wk = number(wtext, row["write_kind"])
    if wk is None:
        return {"refused": "register of write %s not resolved" % wtext}
    if row["write_kind"] == "regidx":
        if wk != 0:
            env[wk] = written
        answer = "x" if wk == ANSWER else None
    else:
        fenv[wk] = written
        answer = "f" if wk == ANSWER else None
    return {"step": {"ctor": ctor, "binding": binding, "reads": args, "write": wk,
                     "write_kind": row["write_kind"], "call": call, "effects": True},
            "answer": answer}


# ------------------------------------------------------- the certificate
def callbacks_of(lean_dir):
    """Every emitted `*_callback` definition: unfolded by the certificate."""
    names = set()
    for fn in os.listdir(lean_dir):
        if fn.endswith(".lean"):
            for m in re.finditer(r"^(?:noncomputable )?def ([A-Za-z_0-9]+_callback)\b", open(os.path.join(lean_dir, fn)).read(), re.M):
                names.add(m.group(1))
    return sorted(names)


def axioms_of(lean_dir):
    """The support file's axioms of type ... -> SailM Unit: the model declares
    them and defines nothing, so every certificate assumes each leaves the
    state as it is. Returns [(name, implicit binders, explicit arity)]."""
    path = os.path.join(lean_dir, "RiscvExtras.lean")
    out = []
    if not os.path.exists(path):
        return out
    for ln in open(path):
        m = re.match(r"^axiom (\w+)\s*((?:\{[^}]*\}\s*)*):\s*(.*?)\s*$", ln)
        if not m:
            continue
        name, implicits, typ = m.group(1), m.group(2).strip(), m.group(3)
        if not re.search(r"SailM (Unit|PUnit)\s*$", typ):
            continue
        args = [a.strip() for a in typ.split("→")[:-1]]      # the argument types, in order
        implicits = re.sub(r"\{(\w+)\}", r"{\1 : Type}", implicits)   # `{α}` needs its sort stated in a theorem binder
        out.append((name, implicits, args))
    return out


def hook_hyps(axioms):
    """(hypothesis text, names) for the theorem and the simp set."""
    hyps, names = [], []
    for i, (name, implicits, args) in enumerate(axioms):
        xs = " ".join("x%d" % k for k in range(len(args)))
        binders = (implicits + " " if implicits else "") + " ".join("(x%d : %s)" % (k, a) for k, a in enumerate(args))
        hyps.append("(hk%d : ∀ %s (s : St), (%s %s) s = EStateM.Result.ok () s)" % (i, binders, name, xs))
        names.append("hk%d" % i)
    return " ".join(hyps), names


def regidx_defs_of(lean_dir):
    """Every emitted definition whose result is a register index (the rule:
    the certificate unfolds what names a register, whatever it is called)."""
    names = []
    for root, _, files in os.walk(lean_dir):
        for f in files:
            if not f.endswith(".lean"):
                continue
            for m in re.finditer(r"^def ([A-Za-z0-9_']+)(?:\s*\([^)]*\))*\s*:\s*regidx\s*:=", open(os.path.join(root, f)).read(), re.M):
                if m.group(1) not in names:
                    names.append(m.group(1))
    return names


def walk_file(lib, header_lines, closers, unit_name, instr_terms, proposal, unknowns, strip_names, hyps_regs, callbacks=(), axioms=(),
              answer_reg=None, fhyps_regs=(), selects=()):
    """The Lean text: runsTo, step, walk, and the theorem for one unit. The three
    float arguments (2026-09-15) are empty for a unit with no effects-rule step, and
    then the text is exactly what it was."""
    hyps = " ".join("(h%d : s.regs.get? .x%d = some %s)" % (k, k, v) for k, v in hyps_regs)
    khyps, knames = hook_hyps(axioms)
    fhyps = " ".join("(hf%d : s.regs.get? .f%d = some %s)" % (k, k, v) for k, v in fhyps_regs)
    shyps = " ".join("(hs%d : (%s (%s)) s = EStateM.Result.ok (some %s) s)" % (i, sl["fn"], sl["arg"], sl["name"])
                     for i, sl in enumerate(selects))
    hyps = " ".join(x for x in (hyps, fhyps, khyps, shyps) if x).strip()
    unk = " ".join(["(%s : BitVec 64)" % v for v in unknowns] + ["(%s : %s)" % (sl["name"], sl["type"]) for sl in selects])
    answer_reg = answer_reg or ("x%d" % ANSWER)
    strips = ", ".join(strip_names) or "RETIRE_SUCCESS"     # a unit with no instruction walks nothing
    lines = header_lines + ["set_option linter.unusedVariables false", "",
        "abbrev St := SequentialState RegisterType trivialChoiceSource", "",
        "/-- the program ends in a state whose answering register holds v -/",
        "def runsTo (m : SailM ExecutionResult) (s : St) (v : BitVec 64) : Prop :=",
        "  match m s with",
        "  | .ok _ s' => s'.regs.get? .%s = some v" % answer_reg,
        "  | .error _ _ => False", "",
        "/-- one instruction through the model's own execute; an ExecuteAs re-dispatches once -/",
        "def step (i : instruction) : SailM ExecutionResult := do",
        "  match (← execute i) with",
        "  | .ExecuteAs j => execute j",
        "  | r => pure r", "",
        "def walk : List instruction → SailM ExecutionResult",
        "  | [] => pure RETIRE_SUCCESS",
        "  | i :: is => do let _ ← step i; walk is", "",
        "/-- the unit's meaning: its proposal, certified -/",
        "theorem meaning_%s (s : St) %s %s :" % (unit_name, unk, hyps),
        "    runsTo (walk [%s]) s" % (", ".join(instr_terms)),
        "      (%s) := by" % proposal,
        "  simp (config := {decide := true}) [runsTo, walk, step, execute, %s," % strips,
        "    rX_bits, rX, wX_bits, wX, regval_from_reg, regval_into_reg, PreSail.readReg, PreSail.writeReg,",
        "    RETIRE_SUCCESS, reg_name_forwards, to_bits, zero_reg,",
        "    %s" % (", ".join(callbacks) + "," if callbacks else ""),
        "    bind, pure, get, getThe, modify, modifyGet, set, throw,",
        "    EStateM.bind, EStateM.pure, EStateM.get, EStateM.set, EStateM.modifyGet, EStateM.throw,",
        "    EStateM.instMonad, EStateM.instMonadStateOf, MonadStateOf.get, MonadStateOf.set,",
        "    MonadStateOf.modifyGet, MonadState.get, MonadState.set, MonadState.modifyGet,",
        "    BitVec.toNatInt, Std.ExtDHashMap.get?_insert_self, Std.ExtDHashMap.get?_insert,",
        "    %s]" % ", ".join(["h%d" % k for k, _ in hyps_regs] + knames + ["hf%d" % k for k, _ in fhyps_regs]
                            + ["hs%d" % i for i, _ in enumerate(selects)]),
        ""] + closers + [""]
    return "\n".join(lines)


# ------------------------------------------------------------- the driver
def cmd_walk(argv, say, write_json, check_memory):
    """units.json: [{"name", "obj" or "words": [...], "symbol", "lang", "source"}]
    Each unit is carved (if obj/source given), decoded, composed, certified."""
    from . import strip as ST
    proof_project, exec_project, lib, strip_json, units_json, out_dir = argv[:6]
    timeout_s = int(argv[6]) if len(argv) > 6 else 900
    exec_lib = lib_of(exec_project)
    say("  proof lib %s; executable lib %s; decoder state: %s" % (lib, exec_lib, STATE_EXPR))
    os.makedirs(out_dir, exist_ok=True)
    lean_dir = os.path.join(proof_project, lib)
    header, closers = ST.header_of(lean_dir, lib)
    strip = Strip(strip_json)
    clauses = {c["name"][len("execute_"):]: c for c in ST.clauses_of(lean_dir)}
    # a clause whose whole body is the retire, bare (`RETIRE_SUCCESS`, how a hint is emitted) or under `pure`
    NO_EFFECT = re.compile(r"^\(?(pure )?RETIRE_SUCCESS\)?\s*$")
    strip.no_effect = {nm for nm, cl in clauses.items()
                       if len(ST.elements(cl["body"])) == 1 and NO_EFFECT.match(str(ST.elements(cl["body"])[0]).strip())}
    say("  no-effect clauses (the body is the retire): %d" % len(strip.no_effect))
    defs_index = ST.emitted_defs(lean_dir)
    lib_index = ST.library_index(proof_project)
    say("  emitted definitions scanned: %d; lean-sail definitions indexed: %d" % (len(defs_index), len(lib_index)))
    units = json.load(open(units_json))
    rows = []
    # 1. carve what needs carving
    for u in units:
        if "words" in u:
            u["body"] = [(w, u.get("text", [""] * len(u["words"]))[i], "") for i, w in enumerate(u["words"])]
            continue
        obj = os.path.join(out_dir, u["name"] + ".o")
        rc, secs, out, symbol = compile_unit(u, obj, out_dir)
        if rc != 0:
            u["refused"] = "compile rc=%d: %s" % (rc, out.strip().split("\n")[-1][:160])
            continue
        rc, out, body = carve(obj, symbol)
        u["body"] = body
        u["carve_seconds"] = round(secs, 1)
        if not body:
            u["refused"] = "carve found no instructions for %s" % symbol
        elif len(body) > MAX_WORDS:
            u["refused"] = "%d instructions, above the walk's bound of %d" % (len(body), MAX_WORDS)
    # 2. decode every distinct word, one Lean run
    evals, first_label = [], {}
    for u in units:
        if "refused" in u:
            continue
        for i, (w, mn, ops) in enumerate(u.get("body", [])):
            if w not in first_label:
                first_label[w] = "%s#%d" % (u["name"], i)
                evals.append((first_label[w], decode_expr(w)))
    t0 = time.time()
    rc, secs, got, errs = eval_file(exec_project, exec_lib, evals, os.path.join(out_dir, "Decode.lean"))
    say("  decode: %d words, lean rc=%d, %.1fs%s" % (len(evals), rc, secs, ("; " + "; ".join(errs)) if errs else ""))
    # 3. compose and certify, per unit
    pending_regs = {}
    def reg_eval(expr):
        return pending_regs.get(expr)
    # a first pass collects register expressions that need evaluation
    need = set()
    for u in units:
        if "refused" in u:
            continue
        dec = []
        for i, (w, mn, ops) in enumerate(u["body"]):
            txt = got.get(first_label.get(w, ""), "").replace(exec_lib + ".", lib + ".")
            ctor, comps = parse_repr(txt)
            dec.append((ctor, comps, txt))
        u["decoded"] = dec
        for ctor, comps, txt in dec[:-1]:
            res = resolve_alias(strip, ctor, comps) if ctor else None
            if not res or not strip.certified(res[0]) or strip.rows[res[0]].get("shape") != "straight":
                continue
            row = strip.rows[res[0]]
            binding = bind_params(row, res[1])
            if binding is None:
                continue
            for _, rexpr in row["reads"]:
                rt = subst(rexpr, binding)
                if reg_number(rt) is None:
                    need.add(rt)
            wt = subst(row["write"], binding)
            if reg_number(wt) is None:
                need.add(wt)
    if need:
        # these expressions carry the proof library's prefix; the evaluable build has its own
        evs = [("r%d" % i, "(toString (repr (%s)))" % e.replace(lib + ".", exec_lib + ".")) for i, e in enumerate(sorted(need))]
        rc2, secs2, got2, errs2 = eval_file(exec_project, exec_lib, evs, os.path.join(out_dir, "Regs.lean"))
        for i, e in enumerate(sorted(need)):
            k = reg_number(got2.get("r%d" % i, ""))
            if k is not None:
                pending_regs[e] = k
        say("  register expressions evaluated: %d of %d (%.1fs)" % (len(pending_regs), len(need), secs2))
    jobs = int(os.environ.get("WALK_JOBS", "1"))
    pool = ThreadPoolExecutor(max_workers=jobs)
    futures = []
    say("  certifying with %d Lean job(s) at a time" % jobs)
    for u in units:
        row = {"unit": u["name"], "lang": u.get("lang"), "cell_display": u.get("cell_display")}
        if "refused" in u:
            row.update({"verdict": "REFUSED", "why": u["refused"]})
            rows.append(row)
            say("  %-40s REFUSED  %s" % (u["name"], u["refused"]))
            continue
        dec = u["decoded"]
        row["instructions"] = [{"word": w, "display": (mn + " " + ops).strip(), "decoded": txt}
                               for (w, mn, ops), (_, _, txt) in zip(u["body"], dec)]
        bad = [d for d in dec if d[0] is None]
        if bad:
            row.update({"verdict": "REFUSED", "why": "a word Sail's decoder did not give a constructor for: %s" % bad[0][2][:120]})
            rows.append(row)
            say("  %-40s REFUSED  %s" % (u["name"], row["why"][:110]))
            continue
        walked = [(c, comps) for c, comps, _ in dec[:-1]]     # the return excluded
        row["return"] = dec[-1][2]
        comp = compose(strip, walked, reg_eval)
        if "refused" in comp:
            row.update({"verdict": "REFUSED", "why": comp["refused"]})
            rows.append(row)
            say("  %-40s REFUSED  %s" % (u["name"], comp["refused"][:110]))
            continue
        # the certificate file: the clauses it walks (their pure forms and strip theorems, re-proved), then the theorem
        used = []
        form_clause = {}      # the per-arm form name -> the clause it came from
        no_effect_used = []
        for st in comp["steps"]:
            if st.get("no_effect"):
                if st["ctor"] not in no_effect_used:
                    no_effect_used.append(st["ctor"])
                continue
            # a per-arm clause is certified as `<clause>_<arm>`; the proof must
            # name THAT theorem, not the whole-clause one, which does not exist
            for nm in (st.get("form") or st["ctor"],):
                form_clause[nm] = st["ctor"]
                if nm not in used:
                    used.append(nm)
        alias_used = []
        for c, comps in walked:
            if c in strip.aliases and c not in alias_used:
                alias_used.append(c)
        bodies = []
        emitted = set()
        for nm in alias_used + used:
            cl = clauses[form_clause.get(nm, nm)]      # a per-arm name resolves to its clause
            if cl["name"] in emitted:                  # one emission per clause, all its arms at once
                continue
            emitted.add(cl["name"])
            prop = ST.propose(cl)
            if "refused" in prop:                  # a clause the effects rule read (floats)
                prop = ST.propose_effects(cl, defs_index)
            bodies += ST.lean_body(cl, prop)
        # the unknowns: every argument register the proposal mentions (a unit that walks nothing proposes `a`)
        unknowns = [ABI_ARGS[k] for k in sorted(ABI_ARGS)
                    if any(ABI_ARGS[k] in " ".join(st["reads"]) for st in comp["steps"]) or re.search(r"\b%s\b" % ABI_ARGS[k], comp["proposal"])]
        hyps_regs = [(k, ABI_ARGS[k]) for k in sorted(ABI_ARGS) if ABI_ARGS[k] in unknowns]
        # floats: the float argument registers the steps read or the proposal mentions (empty for a unit
        # with no effects-rule step)
        funknowns = [FABI_ARGS[k] for k in sorted(FABI_ARGS) if "fenv" in comp and (
                     any(re.search(r"\b%s\b" % FABI_ARGS[k], r) for st in comp["steps"] for r in st["reads"])
                     or re.search(r"\b%s\b" % FABI_ARGS[k], comp["proposal"]))]
        fhyps_regs = [(k, FABI_ARGS[k]) for k in sorted(FABI_ARGS) if FABI_ARGS[k] in funknowns]
        instr_terms = [txt for _, _, txt in dec[:-1]]
        # an alias's definition must unfold too, or `execute (alias_X ..)` sticks on the redispatch
        strip_names = ["strip_%s" % nm for nm in alias_used + used] + ["alias_%s" % nm for nm in alias_used]
        strip_names += ["execute_%s" % nm for nm in no_effect_used]        # a no-effect clause unfolds to the retire
        # the rule: the certificate unfolds every emitted definition reachable from the clauses it walks,
        # the register-index definitions and the callbacks (the dispatcher and its clauses excepted:
        # the strip theorems stand for those); nothing is named
        # the pure forms stay opaque (the proposal is stated in them; their helpers are the equals stage's
        # business), and the callbacks are unfolded but not expanded (their name maps are large)
        seeds = re.sub(r"^def pure_.*?(?=^theorem|\Z)", "", "\n".join(bodies), flags=re.S | re.M) + " " + " ".join(regidx_defs_of(lean_dir))
        unfold = list(callbacks_of(lean_dir))
        unfold += [d for d in ST.reachable(defs_index, seeds, skip=lambda n: n == "execute" or n.startswith("execute_") or n.endswith("_callback")) if d not in unfold]
        unfold += ST.library_refs(defs_index, unfold, extra_texts=[seeds])
        text = walk_file(lib, header + bodies, closers, re.sub(r"\W", "_", u["name"]), instr_terms,
                         comp["proposal"], unknowns + funknowns, strip_names, hyps_regs,
                         callbacks=unfold, axioms=axioms_of(lean_dir),
                         answer_reg=comp.get("answer_reg"), fhyps_regs=fhyps_regs, selects=comp.get("selects", ()))
        path = os.path.join(out_dir, "Walk_%s.lean" % re.sub(r"\W", "_", u["name"]))
        open(path, "w").write(text)
        row.update({"proposal": comp["proposal"], "steps": comp["steps"], "lean_file": path})
        if "answer_reg" in comp:
            row["answer_reg"] = comp["answer_reg"]
        rows.append(row)
        if os.environ.get("WALK_NO_CERTIFY") == "1":      # the construction stage: L composed, the certificate deferred
            row.update({"verdict": "COMPOSED", "rc": None, "seconds": 0, "errors": []})
            say("  %-40s %-9s %s" % (u["name"], "COMPOSED", row["proposal"][:90]))
            continue
        futures.append((row, u, pool.submit(lean_run, proof_project, path, timeout_s)))
    for row, u, fut in futures:
        rc, secs, out = fut.result()
        errs = [ln for ln in out.split("\n") if "error" in ln][:6]
        row.update({"verdict": "CERTIFIED" if rc == 0 else "FAILED", "rc": rc, "seconds": round(secs, 1), "errors": errs})
        say("  %-40s %-9s %6.1fs  %s" % (u["name"], row["verdict"], secs, row["proposal"][:90]))
        if errs:
            for e in errs[:3]:
                say("      " + e[:200])
    pool.shutdown()
    summary = {"composed": sum(r["verdict"] == "COMPOSED" for r in rows),
               "certified": sum(r["verdict"] == "CERTIFIED" for r in rows),
               "failed": sum(r["verdict"] == "FAILED" for r in rows),
               "refused": sum(r["verdict"] == "REFUSED" for r in rows), "of": len(rows),
               "driver_peak_resident_kB": check_memory("walk end")}
    write_json(os.path.join(out_dir, "walk.json"), {"summary": summary, "rows": rows})
    say("  walk: certified %d, failed %d, refused %d, of %d" % (summary["certified"], summary["failed"], summary["refused"], summary["of"]))
    return 0
